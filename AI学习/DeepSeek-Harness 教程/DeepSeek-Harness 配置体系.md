---
title: "DeepSeek-Harness 插件开发核心"
tags: [deepseek-harness, ai, agent, 插件, 教程, 开发]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 插件开发核心：从 apply(ctx) 到发布

> [!summary] 本章导读
> 这是全书核心。用你熟悉的 Claude Code 作参照：在 Claude Code 里写「扩展」靠改配置文件 + 少量钩子；在 dsh 里写插件 = 写 TypeScript 模块 + 用 patch 装进插件树。本章按「是什么 → 怎么注册 → 生命周期 → 依赖 → 配置 → 写工具 → 策略 → 发布」完整讲清插件开发。

## 3.1 插件是什么：apply(ctx) + name

插件是导出 `apply` 函数的 TypeScript 模块。框架加载时调用 `apply` 并传入 `ctx`（上下文对象），通过 `ctx` 注册能力[^1]：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'hello-plugin'   // 仅诊断用，可省
export function apply(ctx: Context) {
  // Register capabilities here.
}
```

`name` 只是诊断元数据；真正的逻辑都在 `apply(ctx)` 里。**没有框架样板代码**——插件只描述自己贡献什么，`cordis.yml` 负责组合应用[^2]。

> [!tip] 大白话
> 插件像一个「应聘者」，`apply(ctx)` 是入职第一天：公司（框架）把工牌（ctx）发给你，你在工牌上挂上你的能力（工具、事件、服务）。离职时（插件卸载），挂上去的自动摘下来。

### 三种形态

| 形态 | 写法 | 适用 |
|---|---|---|
| 函数 | `export function apply(ctx) {}` | 多数情况足够 |
| 对象 | `export default { name, inject, apply(ctx) {} }` | 需要集中声明元数据 |
| 类（Service） | `class X extends Service { constructor(ctx){ super(ctx,'name') } }` | 向其他插件提供服务 |

函数形式直到你需要对外提供 service 都够用；类形式见 3.5[^2]。

## 3.2 注册机制：多层 YAML 补丁树

插件不是放进某个目录就生效，而是通过 **YAML 补丁树**装配。dsh 的配置在空根上按顺序叠加[^1]：

1. **bundle 补丁**：profile manifest 中 `dsh.profile.bundles` 列表命名的每个 bundle 补丁；
2. **profile 自身 `cordis.patch.yml`**；
3. **home 级 `$DSH_HOME/cordis.patch.yml`**（机器级偏好，所有 profile 共享）；
4. **`--patch <path>` 覆盖层**（按 argv 顺序）。

补丁语义：**"Later layers win per row"**——后层按行覆盖，**替换目标行的完整 config 值，不做深合并**，可插入新行。

> [!tip] 大白话
> 把补丁树想成一层层铺在桌上的透明纸。后铺的纸会盖住先铺的同一位置，但不会去改下面那层的其他内容——「整行替换，不做深合并」。

### 开发期注册：cordis.yml patch（路径必须绝对）

官方第一个插件教程的做法：在仓库根建 `scratch-plugin/src/`，写插件文件后，用 `cordis.yml` 插入插件行[^1]：

```yaml
# scratch-plugin/cordis.yml
- insert:
    - id: hello
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
```

> [!warning] 插件路径必须是绝对路径
> patch 文件只贡献配置，不会改变 loader 解析模块路径时使用的 profile 目录——相对路径会失效。这是新手第一坑。

启动并验证：

```bash
pnpm dsh web --patch ./scratch-plugin/cordis.yml
# 打开 http://127.0.0.1:3080，终端应打印 [hello-plugin] plugin loaded!
```

检查合成配置（排查利器）：

```bash
pnpm dsh --profile web --dump-default-config          # 只看 bundle 层
pnpm dsh --profile web --patch ./extra.yml --dump-config  # 含 profile/home 补丁与 --patch 覆盖层
```

## 3.3 两级配置：Profile 与 Agent Preset

- **Profile（进程级）**：决定装哪些 bundle。`web`（base + web-app）与 `headless`（base + headless）首次使用自动从模板初始化；其他缺失 profile 需 `dsh plugin --profile <name> add <package>`[^1]。
- **Agent Preset（会话级）**：决定工具/提示词/skill/子代理。内置 4 个预设：`minimal` / `standard` / `code` / `cordis`。作用域解析：`agent → preset → global`[^1]。

其中 `minimal` 固定系统提示 "You are a helpful software engineer assistant."，只组合 `bash` + `str_replace_editor` 两个工具。

## 3.4 生命周期与 effects：fiber 状态机

每个加载的插件实例持有一个 **fiber**（运行时句柄），状态机[^2]：

```
PENDING → LOADING → ACTIVE → UNLOADING → DISPOSED
                 ↘ FAILED
```

- **PENDING** — 声明了但必需服务（3.5）尚未就绪；
- **FAILED** — `apply` 或配置校验抛错；
- **UNLOADING / DISPOSED** — disposer 运行 / 全部拆除。

插件会因配置编辑、热重载、显式 dispose、依赖消失而卸载。**通过 `ctx` 注册的一切都是 effect**：事件监听、工具、定时器、子插件、service 注册——卸载时自动清理，无需手动 removeListener / clearInterval[^2]。

框架不管理的资源（网络连接、文件 watcher）用 `ctx.effect()` 包一层：

```ts
export function apply(ctx: Context) {
  ctx.effect(() => {
    const timer = setInterval(() => console.log('heartbeat'), 5000)
    return () => clearInterval(timer)   // 卸载时运行
  })
}
```

> [!tip] 大白话
> 「效果（effect）」像门禁卡的自动失效：离职那天门禁卡自动作废，你不用自己去前台注销。凡是走 `ctx` 挂的能力都自动失效；自己额外申请的资源（网络连接）用 `ctx.effect()` 声明「我离职时要做这些清理」。

## 3.5 服务与依赖：inject 与 Service

**Service** 是具名能力，一个插件提供、其他插件经 `ctx` 消费——`ctx.tools` / `ctx.llm` / `ctx.agents` 都是服务[^2]。

### 消费依赖：inject

```ts
export const name = 'my-tool-plugin'
export const inject = ['tools']          // 依赖就绪前不加载

export function apply(ctx: Context) {
  ctx.tools.register(/* ... */)          // ctx.tools 一定可用
}
```

`inject` 不是一次性启动检查：如果依赖运行中消失，依赖它的插件会一起被卸载，等服务恢复再重载。**文件顺序不决定加载序，依赖才决定**。

可选依赖：跳过 inject，用 `ctx.get('name')` 探测（拿不到返回 undefined，插件照常运行）。

### 提供服务：类形态

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context { greeter: GreeterService }   // 类型合并，让 ctx.greeter 有类型
}

export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter')                          // 注册为 ctx.greeter
  }
  greet(who: string) { return `Hello, ${who}!` }
}

export function apply(ctx: Context) {
  ctx.plugin(GreeterService)                       // 类本身也是插件
}
```

## 3.6 插件配置：Config schema

插件可接受 `cordis.yml` 传入的配置。导出同名 `Config` 接口 + **Schemastery** schema（不能用普通对象），默认值写在 schema 上[^1][^2]：

```ts
import Schema from '@deepseek-ai/schemastery'

export interface Config {
  greeting: string
  maxRetries: number
}
export const Config: Schema<Config> = Schema.object({
  greeting: Schema.string().default('Hello'),
  maxRetries: Schema.number().default(3),
})

export function apply(ctx: Context, config: Config) {
  console.log(config.greeting)   // 用户值或 schema 默认值
}
```

在 `cordis.yml` 里配：

```yaml
- insert:
    - id: hello
      name: './src/my-plugin.ts'
      config:
        greeting: 'Hi there'
        maxRetries: 5
```

- **原则**：两个部署可能想设不同的值，就做成配置字段（测试：`cordis.yml` 能否不改代码改值）[^1]；
- **失效即响亮失败**：无效配置让 fiber 进 FAILED，报错精确；
- **HMR**：配置编辑热替换插件，旧实例注册自动清理，不残留。

## 3.7 开发一个 Tool：defineTool DSL

工具是模型能调用的能力。用 `defineTool` 定义，经 `ctx.tools.register` 注册[^3]：

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',        // 模型看到的描述
    parameters: {
      name: { type: 'string', required: true, description: 'The name to greet' },
    },
    output: {
      schema: { type: 'string' },                  // canonical 返回值
      render: (_args, value) => [{ type: 'text', text: value }],  // 模型可见内容
    },
    async execute(args) {
      return `Hello, ${args.name}!`               // args 已按 parameters 校验并推断类型
    },
  }))
}
```

关键契约（完整参考见第 5 章 5.3）：
- **args 自动校验**：`defineTool` 在 `execute` 前校验模型生成的参数；
- **返回值**：`execute` 只返回 `output.schema` 声明的单一 canonical JSON 值，`output.render` 负责转成模型可见的文本——别在返回值里塞给人看的 prose；
- **抛错 = isError**：基础设施失败就 throw，业务成功态放进 canonical 值；
- **`exec.signal`**：需要时可取消进行中的工作；
- **注册即 effect**：插件卸载自动注销工具，schema 自动流入系统提示词组装[^4]。

## 3.8 工具策略与观察：hook 扩展点

工具不是黑盒——dsh 提供一组**扩展点**，让插件在工具执行前后插入策略[^4]：

| 扩展点 | 用途 |
|---|---|
| `tools/pre-execute` | allow / deny / ask 决策（权限门） |
| `ctx.tools.guard()` | 单调最终拒绝，后面的监听者无法撤销 |
| `tools/execute` | 包 dispatch 加超时、重试、指标 |
| `tools/post-execute` | 替换展示内容或返回值、附加上下文 |
| `tools/result` | 只读观察不可变的最终结果 |

示例（权限门 hook 插件）[^4]：

```ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  if (!(await isAllowed(exec))) {
    return { kind: 'deny', reason: 'Denied by policy.' }
  }
  return next()
})
```

> [!note] 与 Claude Code 对照
> 这就是「hook 插件」：Claude Code 的 `PreToolUse` hook ≈ `tools/pre-execute` 监听；官方 `dsh-hooks-claude-code` 桥能把 Claude Code 的 hook 配置文件直接映射到这些扩展点[^4]。

## 3.9 打包与安装：bundle 与 profile

开发期用 `--patch` 加载本地插件；要给别人用时打包成 **bundle**（npm 包）[^5]。

两个概念（都由 `package.json` 描述，但 manifest 不同）：
- **bundle**：携带配置层的 npm 包，声明 `dsh.bundle.patch`——回答「这个包贡献什么」；
- **profile**：`$DSH_HOME/profiles/<name>` 目录，声明 `dsh.profile.bundles` 有序列表——回答「装哪些 bundle、什么顺序」。你从不手写 profile，`dsh plugin` 自动维护。

最小 bundle：

```json
{
  "name": "dsh-hello-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

```yaml
# cordis.patch.yml（插件行按包名引用，不用相对路径）
- insert:
    - id: hello
      name: dsh-hello-plugin
```

安装进 profile：

```bash
dsh plugin --profile demo add ./hello-plugin     # 转发 pnpm，自动追加 bundle
dsh --profile demo --dump-config                  # 验证层
dsh --profile demo
```

> [!warning] git 安装的 build 坑
> `dsh plugin add github:you/hello-plugin` 拉的是**源码不是构建产物**。作者必须提供 `prepare` 脚本（pnpm 在 git 安装后运行），用户还需在 profile 的 `pnpm-workspace.yaml` 里 `allowBuilds` 放行——这等于「授权在安装时执行该包的代码」，只放行你信任的包，并 `#<sha>` 钉住 commit[^5]。

## 3.10 system-prompt 子系统：提示词怎么组装

写提示词类插件（加人格、加指令）直接相关的参考。`system-prompt` 包负责**在每次模型调用前组装最终系统提示词**，注册表服务 `ctx.systemPrompt`[^6]。

### PromptSection

```ts
interface PromptSection {
  readonly name: string        // 必须唯一，重复注册抛错
  readonly order: number       // 升序拼接
  readonly text: string | ((context) => string)  // 可含 {{variable}} 占位符
  readonly complete?: boolean  // true = 该段即完整系统提示词
}
```

**order 约定**：`-100` harness 身份 → `0` 部署人格（persona）→ 其他负数在人格前 → `100–199` 工具指导。

**complete 语义**：`complete: true` 的段表示「贡献就是完整系统提示词」。组装仍会跑协作瀑布，随后把该段恢复为唯一提示词段；多个生效 complete 段 → 组装失败。

### 作用域与遮蔽

- 作用域级段落/变量/动态上下文**遮蔽**（shadow）全局同名项；
- 工具提供方例外：全局与匹配作用域**共同贡献**；
- 变量名匹配 `[a-z][a-z0-9_]*`，`{{variable}}` 在渲染期由 `renderPrompt` 插值。

### 事件与防错

- `system-prompt/assemble`（waterfall）：返回值权威，监听者可修改 assembly；
- `system-prompt/change`（emit）：任何提示词提供方变化时发出；
- `knownNames`：区分「配置名拼写错误」与「已知工具被有意隐藏」；
- `PromptContext`：缓存安全的动态上下文，物化为 durable user-role snapshot，避免每回合重复写入[^6]。

---

## 本章小结

> [!summary]
> - 插件 = 导出 `apply(ctx)` 的 TS 模块；三种形态：函数 / 对象 / 类（Service）；
> - 注册靠**多层 YAML 补丁树**（bundle → profile → home → `--patch`，后层整行替换）；开发期用 `cordis.yml` patch，**路径必须绝对**，`--dump-config` 排查；
> - 生命周期：fiber 状态机；`ctx` 注册的一切都是 effect，自动清理；手动资源用 `ctx.effect()`；
> - 依赖：`inject` 声明硬依赖（未就绪保持 PENDING），`ctx.get()` 探测可选依赖；Service 类对外提供服务；
> - 插件配置：`Config` 接口 + Schemastery schema，坏配置响亮失败，HMR 热替换；
> - 工具：`ctx.tools.register(defineTool({...}))`，args 自动校验、canonical 返回值、注册即 effect；策略用 `tools/pre-execute` 等 hook 扩展点；
> - 发布：bundle（`dsh.bundle`）vs profile（`dsh.profile`），`dsh plugin add` 安装，git 安装注意 prepare + allowBuilds；
> - 提示词类插件看 `ctx.systemPrompt`：PromptSection 按 order 组装，`complete` 段可独占。

下一章动手写一个完整插件：[[DeepSeek-Harness 与ClaudeCode对照迁移|实战：自定义工具插件]]。

---

## 更新记录

- 2026-08-15：全套重构为「写自己的 dsh 插件」主线。插件开发内容从 3.8 一节扩展为全书核心章节；新增 3.4 生命周期 / 3.5 服务依赖 / 3.6 插件配置 / 3.7 工具 DSL / 3.8 策略扩展点 / 3.9 打包发布；原权限、模型、环境变量、CLI 内容精简移入第 5 章速查。

---

[^1]: 素材来源：DeepSeek Harness 官方文档「第一个插件 / 插件配置」（2026-08-15 收集）。
[^2]: 素材来源：官方 Cordis 教程 01–03/05（2026-08-15 收集）。
[^3]: 素材来源：官方「开发一个 Tool」（2026-08-15 收集）。
[^4]: 素材来源：官方「Tool authoring reference」与「扩展插件形态 Cookbook」（2026-08-15 收集）。
[^5]: 素材来源：官方「打包并安装插件」（2026-08-15 收集）。
[^6]: 素材来源：官方「system-prompt 子系统参考」（2026-08-14 收集）。
