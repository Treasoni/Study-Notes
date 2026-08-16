---
title: "实战：写工具 git_log 与四名分离"
tags: [deepseek-harness, ai, agent, 插件, 教程, 实战]
created: 2026-08-16
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# 实战：写工具 git_log 与四名分离

> [!summary] 本章导读
> 第 05 章的插件只能打印一行 `[git-log-plugin] plugin loaded!`，对模型来说它"存在但没用"。这一章把插件变成一个**真正能给模型干活**的插件：注册一个模型可见、可调用的工具 `git_log`。你会亲手写下 defineTool 五件套，理解 `execute` 的 canonical 值契约，并弄清楚为什么 `inject = ['tools']` 少写一行就会崩。这是全篇第一个"插件 ≠ 工具"的转折点。无论你从哪个入口起步，这一章的动作都一样：**只动两个文件**（新建 `src/tools/git-log.ts` + 升级 `src/index.ts`）。

## 1. 文件归属：工具本体放 `src/tools/git-log.ts`，`src/index.ts` 做注册中心

第 05 章只有一个文件 `src/index.ts`。现在要加工具，第一个问题是"代码放哪"。沿用插件开发核心的文件归属约定[^3]：

- `src/index.ts`：**注册中心**。负责 `apply(ctx)`、声明 `inject`、把工具注册进 `ctx.tools`，以及打加载日志。它只做"组装"，不做具体业务。
- `src/tools/git-log.ts`：**工具工厂**。导出一个返回 `defineTool({...})` 结果的函数，例如 `gitLogTool()`。一个文件一个工具，工厂每次调用返回一个新实例，状态天然隔离。

先建目录（第 05 章从零路线只建过 `src/`，现在要新增 `tools/` 子目录，和 §2.1 的 `mkdir -p src` 一个套路）：

```bash
mkdir -p src/tools
```

为什么工具本体要写成"工厂函数"，而不是直接导出一个 defineTool 对象？因为注册发生在 `apply` 阶段，工厂把"定义"和"注册"分开：`git-log.ts` 只负责"这个工具长什么样"，`index.ts` 负责"在什么时候把它装进去"。这也是第 07 章把配置传进工厂的入口。

> [!note] 这在 Claude Code 里相当于
> `src/index.ts` ≈ 插件入口文件，负责初始化；`src/tools/*.ts` ≈ 独立拆出去的"工具定义 + 处理函数"模块，入口只管注册。

## 2. defineTool 五件套：name / description / parameters / output / execute

`defineTool` 是 dsh-tools 提供的工具描述 DSL，它收**一个**配置对象，对象里有五个字段[^1]：

| 字段 | 作用 | 模型可见吗 |
| --- | --- | --- |
| `name` | 工具唯一标识，模型在对话里用它发起调用 | 是 |
| `description` | 一句话说明工具何时该用、怎么用 | 是 |
| `parameters` | 声明入参的结构与约束（类 JSON-schema） | 是 |
| `output` | 声明返回值的结构 + 怎么把结果渲染成文本 | 是（schema 部分） |
| `execute` | 真正干活的函数，接收已校验的 args，返回 canonical 值 | 否 |

`name` 就是我们一致性基线里模型可见的 `git_log`；`description` 写得越清楚，模型越不会在错误场景调用它；`parameters` / `output` 负责把"模型侧契约"和"代码侧契约"对齐；`execute` 是唯一有副作用的字段。

> [!note] 先睹为快：完整 `src/tools/git-log.ts`
> 下面整份代码就是这一章要写进 `git-log-plugin/src/tools/git-log.ts` 的**完整文件**。先整体扫一遍，看清五件套长在同一个 `defineTool({...})` 对象里；§3、§4 再逐段拆开讲，**每段都出自这份文件**。

```ts
// git-log-plugin/src/tools/git-log.ts
import { defineTool } from 'dsh-tools'
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const execFileAsync = promisify(execFile)

export function gitLogTool() {
  return defineTool({
    name: 'git_log',
    description: '查看指定 Git 仓库最近的 5 次提交',
    parameters: {
      type: 'object',
      properties: {
        path: {
          type: 'string',
          description: '目标 Git 仓库的绝对路径',
          required: true, // 属性级 required 布尔
        },
      },
    },
    output: {
      schema: {
        type: 'object',
        properties: {
          commits: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                hash: { type: 'string' },
                message: { type: 'string' },
              },
            },
          },
        },
      },
      render(value) {
        // value 是 execute 返回的 canonical 值；这里才做"给人看"的排版
        const lines = value.commits.map((c) => `${c.hash} ${c.message}`)
        return [{ type: 'text', text: lines.join('\n') || '(no commits)' }]
      },
    },
    async execute(args) {
      try {
        const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', '5'], {
          cwd: args.path,
        })
        const commits = stdout
          .trim()
          .split('\n')
          .filter(Boolean)
          .map((line) => {
            const [hash, ...rest] = line.split(' ')
            return { hash, message: rest.join(' ') }
          })
        // ✅ 业务成功态：返回 canonical 值，框架按 output.schema 序列化
        return { commits }
      } catch (err) {
        // ✅ 基础设施失败：throw = isError，注册表捕获，不泄漏给模型
        throw new Error(`git log 执行失败: ${(err as Error).message}`)
      }
    },
  })
}
```

这一章要新建的文件只有这一个：`src/tools/git-log.ts`（先建 `tools/` 子目录）。它**只导出 `gitLogTool` 工厂**，不含任何注册逻辑——怎么把它装进插件，由 §5 的 `src/index.ts` 完成。

> [!tip] 大白话：defineTool 是给机器人写岗位说明书
> 把 defineTool 想成「给机器人写一份岗位说明书」：名字（`name`）写在工牌上，职责（`description`）写清楚什么时候叫它，输入输出格式（`parameters`/`output`）是交接班的单据模板。机器人读到说明书就知道自己是什么岗位。而 `execute` 是「真干活的人」——它不需要操心怎么排版汇报，只要把结果按单据格式交回去就行。

> [!note] 这在 Claude Code 里相当于
> Claude Code 插件里 `tools` 数组的每一项：`name`/`description`/`parameters` 声明工具元数据，外加一个处理函数负责实际调用。`defineTool` 只是把"元数据 + 处理函数"打包成一条更严格的 DSL。

## 3. parameters 与 output：类 JSON-schema；output.schema + output.render

`parameters` 写在 `src/tools/git-log.ts` 的 `defineTool({...})` 里（完整文件见 §2「先睹为快」）。它是**类 JSON-schema** 结构：顶层 `type: 'object'`，`properties` 里每个属性用 `{ type, description, required }` 描述，其中 `required` 是**属性级的布尔值**，而不是 JSON-schema 传统的数组[^1]：

```ts
parameters: {
  type: 'object',
  properties: {
    path: {
      type: 'string',
      description: '目标 Git 仓库的绝对路径',
      required: true, // 属性级 required 布尔
    },
  },
},
```

`output` 同样写在 `defineTool({...})` 里，由两部分组成[^1]：

- `output.schema`：声明 `execute` 返回的 **canonical 值**长什么样，同样用类 JSON-schema。框架用它对返回值做校验与序列化。
- `output.render(value)`：把 canonical 值**转换**成给模型/界面展示的文本块 `[{ type: 'text', text: value }]`。canonical 值负责"机器可读"，render 负责"人可读"，两者职责分开。

```ts
output: {
  schema: {
    type: 'object',
    properties: {
      commits: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            hash: { type: 'string' },
            message: { type: 'string' },
          },
        },
      },
    },
  },
  render(value) {
    // value 是 execute 返回的 canonical 值；这里才做"给人看"的排版
    const lines = value.commits.map((c) => `${c.hash} ${c.message}`)
    return [{ type: 'text', text: lines.join('\n') || '(no commits)' }]
  },
},
```

有个省力点值得记住：`parameters` 的 schema 会**自动流入系统提示词的组装**，`description` 也会被模型读到，所以你不需要在 `description` 里手工复述参数格式——否则既重复、又容易在两处改漏[^2]。

> [!tip] 大白话：canonical 值 vs render
> `execute` 像仓库管理员，只交「入库单」（结构化数据，canonical 值）；`render` 像前台文员，把入库单誊成给老板看的报表。管理员绝不该自己写报表——否则换个展示形式（终端、Web UI、JSON）就全乱了。

## 4. execute(args) 契约：返回唯一 canonical JSON 值；抛错 / 非法值 = isError

`execute` 是五件套里唯一"干活"的字段，写在 `src/tools/git-log.ts` 的 `defineTool({...})` 里（完整文件见 §2「先睹为快」），它的契约是整个框架正确性的关键[^1][^2]：

1. **返回唯一 canonical JSON 值**：`execute(args)` 必须返回 `output.schema` 声明的那一个 JSON 值（我们的例子是 `{ commits: [...] }`），**不返回内容块**。框架拿到返回值后按 `output.schema` 序列化，再丢给 `output.render` 渲染。你如果在 `execute` 里提前返回 `[{ type: 'text', ... }]`，那是个数组，和 `output.schema` 对不上，会被判为非法值。
2. **`args` 是只读、已校验的**：框架根据 `parameters` schema 推断 `args` 类型、调用前自动校验；你的代码里不要改它。
3. **抛错 / 返回非法值 = isError**：注册表会捕获 `execute` 抛出的异常，标记为 `isError` 返回给上层，**不会把堆栈泄漏给模型**。
4. **基础设施失败要 `throw`**：git 没装、目录不是仓库、命令超时——这些是"环境问题"，不是"业务结果"，必须 `throw`，让框架标记失败。
5. **业务成功态放 canonical 值**：git 跑通了但仓库没有任何提交，这不是失败，返回 `{ commits: [] }` 即可——空结果也是成功。

```ts
async execute(args) {
  try {
    const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', '5'], {
      cwd: args.path,
    })
    const commits = stdout
      .trim()
      .split('\n')
      .filter(Boolean)
      .map((line) => {
        const [hash, ...rest] = line.split(' ')
        return { hash, message: rest.join(' ') }
      })
    // ✅ 业务成功态：返回 canonical 值，框架按 output.schema 序列化
    return { commits }
  } catch (err) {
    // ✅ 基础设施失败：throw = isError，注册表捕获，不泄漏给模型
    throw new Error(`git log 执行失败: ${(err as Error).message}`)
  }
}
```

反着写是三个最典型的错误：

```ts
// ❌ 错误 1：execute 返回内容块，而不是 canonical 值
async execute(args) {
  const commits = await readCommits(args.path)
  return [{ type: 'text', text: commits.join('\n') }] // 数组 ≠ output.schema 声明的对象 → isError
}

// ❌ 错误 2：把失败塞进返回值，而不是 throw
async execute(args) {
  try {
    return { commits: await readCommits(args.path) }
  } catch (err) {
    return { commits: [], error: String(err) } // 字段超纲 + 掩盖失败，模型会误以为成功
  }
}

// ❌ 错误 3：吞掉错误返回空结果
async execute(args) {
  try {
    return { commits: await readCommits(args.path) }
  } catch {
    return { commits: [] } // 基础设施失败被伪装成"没有提交"
  }
}
```

另一个注册即生效的细节：`ctx.tools.register` 是**注册即 effect**，插件 fiber 卸载时工具会自动注销，你不用手动清理[^2]。

> [!tip] 大白话：为什么 execute 不能自己排版
> 把 execute 想成流水线上的工人：他的活儿是「做出零件」（canonical 值），质检（`output.schema`）负责验收，包装（`output.render`）负责装箱。工人如果既做零件又自己写包装箱，质检就形同虚设——这次是纸箱、下次是木箱，下游全乱了。所以「只交零件，不碰包装」。

## 5. index.ts 升级：inject = ['tools'] + ctx.tools.register(...)

工具写好了，还要在 `src/index.ts` 里注册。注册动作两件事：声明 `inject = ['tools']`，然后 `ctx.tools.register(...)`[^1]。

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'
import { gitLogTool } from './tools/git-log'

export const name = 'git-log-plugin' // 诊断名：加载日志用

// 关键：声明依赖 'tools'，框架会先初始化工具注册表再调 apply
export const inject = ['tools']

export function apply(ctx: Context) {
  // 到这里 ctx.tools 一定可用（inject 保证）
  ctx.tools.register(gitLogTool())
  console.log('[git-log-plugin] plugin loaded!')
}
```

`inject` 是 cordis 的依赖注入声明。写 `['tools']` 的意思是"我的 `apply` 需要工具注册表就绪才能跑"，框架会保证执行顺序。**少写这一行会怎样？** `ctx.tools` 是 `undefined`，`ctx.tools.register(...)` 直接抛 `Cannot read properties of undefined`——而且是在加载阶段炸，插件起不来。这类错误发生在 apply 里，比工具执行时抛错更难排查，因为看起来像"框架崩了"。

> [!note] 这在 Claude Code 里相当于
> `inject = ['tools']` ≈ 插件初始化时显式声明"我需要工具注册表这个依赖"，拿到一个注册表引用来注册自己的工具。区别是 Claude Code 里注册顺序更宽松，而 cordis 用 `inject` 把顺序契约写死了。

## 6. 四名分离落地

现在你的工程里已经有多个名字在同时流动，把它们钉死才不会在第 09 章打包安装时翻车。这一章真正"活"的名字有两个，另外两个会在后续章节出现，先建立完整心智模型[^4]：

| 名字       | 固定值                  | 出现位置                                        | 本章状态        |
| -------- | -------------------- | ------------------------------------------- | ----------- |
| 诊断名      | `git-log-plugin`     | `export const name`，加载日志 `[git-log-plugin]` | ✅ 已用（第 05 章） |
| 包名       | `dsh-git-log-plugin` | package.json `name`                         | ⏳ 第 09 章     |
| patch id | `git-log`            | patch yml 的 `- insert: id`                  | ✅ 已用（第 05 章） |
| 工具名      | `git_log`            | `defineTool.name`，模型可见                      | ✅ 本章新增      |

改错每个名字的后果对照见 [[04-实战-结果预览与选路|第 04 章 §4]]。核心就一句：**`git-log-plugin` ≠ `dsh-git-log-plugin` ≠ `git-log` ≠ `git_log`**。前三个连字符命名各管各的（日志 / 包 / 补丁实例），只有 `git_log` 是下划线命名且直接暴露给模型。工具名是模型和你的代码之间的协议，一旦发布再改，所有依赖它的对话历史都会失效——所以 `git_log` 从这一章起就是冻结值。

## 7. 验证信号

改完重新加载：

```bash
# 在 dsh 源码仓库根目录执行
pnpm dsh web --patch ./git-log-plugin/dev-cordis.patch.yml
```

预期输出变成：

```
[git-log-plugin] plugin loaded!
```

（改造路线的读者：这一句从 `repo-status-plugin` 换成 `git-log-plugin`，就是「你写成了」的确认信号[^4]。）

## 本章小结

- 文件归属：工具本体放 `src/tools/git-log.ts`（工厂导出），`src/index.ts` 只做注册中心，职责分离。
- `defineTool` 五件套：`name` / `description` / `parameters` / `output` / `execute`；`parameters` 用属性级 `required` 布尔，`output` 拆成 `schema`（canonical 值结构）+ `render`（转文本块）。
- `execute` 契约：返回 `output.schema` 声明的**唯一 canonical JSON 值**，不返回内容块；基础设施失败 `throw`（=isError，注册表捕获不泄漏给模型），业务成功态放 canonical 值。
- `src/index.ts` 升级：`export const inject = ['tools']` + `ctx.tools.register(gitLogTool())`；漏写 `inject` 会让 `ctx.tools` 为 `undefined`，加载阶段直接崩。
- 四名分离落地：`git-log-plugin`（诊断）≠ `dsh-git-log-plugin`（包）≠ `git-log`（patch id）≠ `git_log`（模型可见工具名），`git_log` 从本章起冻结。

下一章，我们会给 `git_log` 加一个可调参数 `maxCommits`——届时 execute 里那句写死的 `-n 5` 会换成读取配置，正式引入 Config schema。

---

## 注释

[^1]: 素材来源：官方 `docs/user/develop/basic/tool.md`——defineTool 五件套；parameters 属性级 required；output.schema + output.render。
[^2]: 素材来源：官方 `docs/cookbook/adding-a-tool.md`——execute 契约（canonical 值 / throw=isError / 注册即 effect / schema 自动流入系统提示词）。
[^3]: 素材来源：本地 vault [[01-插件开发核心-从apply到system-prompt|插件开发核心]]——文件归属（src/index.ts 注册中心、src/tools/*.ts 工具工厂）/ apply 三形态 / defineTool 契约。
[^4]: 「四名分离改错对照 / 验证信号」来自原《DeepSeek-Harness 插件实战》分册第 3 节（已并入本教程 04-10 章），实操基底为本地 vault `example-plugin/*`。
