# DeepSeek-Harness 插件实战 · 从脚手架到打包发布

> [!summary] 本章导读
> 本分册是系列的「实战收尾」：不从头写（那是 [[DeepSeek-Harness 与ClaudeCode对照迁移|第 4 章]] 的活），而是把 `example-plugin`（repo_status）**改造成你自己的工具**，走通 **写 → 配 → 验证 → 打包 → 安装** 全链路。
> 每步都给：可复现命令 + 预期输出 + 出错排查。全文用 `git_log`（最近提交概览）做示范工具——它与 repo_status 同为 git 家族，改动最小、最容易照做；你的真实工具可以是任何 `defineTool` 能表达的东西（笔记检索、目录统计、API 封装）。
> **前置要求**：建议先读 [[DeepSeek-Harness 安装与快速上手|第 2 章]]（源码环境就绪）、[[DeepSeek-Harness 插件开发核心|第 3 章]]（插件概念）与 [[DeepSeek-Harness 配置体系|配置体系专册]]（补丁树 / bundle 术语）；本分册不重复讲概念，未读也可照做。

## 目录

1. [[#1. 先看结果——你要做出什么|1. 先看结果]]
2. [[#2. 环境确认 + 拷贝脚手架（5 分钟热身）|2. 环境确认 + 拷贝脚手架]]
3. [[#3. 写——把 repo_status 改造成 git_log|3. 写：把 repo_status 改造成 git_log]]
4. [[#4. 配——Config schema 加可调参数 + patch 传值|4. 配：加可调参数 + patch 传值]]
5. [[#5. 验证——加载、看配置层、让模型真正调用|5. 验证：加载、看配置层、让模型调用]]
6. [[#6. 打包——bundle 打包 + profile 安装 + git 安装的坑|6. 打包：bundle + profile 安装]]
7. [[#7. 小结与下一步——换成你自己的工具|7. 小结与下一步]]

## 1. 先看结果——你要做出什么

读完理论分册、环境也跑通了，可让你亲手写一个插件还是不知道从哪下手？本分册就是补这个缺口：不从头搭骨架，而是把现成的 `example-plugin`（repo_status）**改造成你自己的工具**，照着走就能跑通 **写 → 配 → 验证 → 打包 → 安装** 全链路[^S7]。整条链路最后交付两样东西：**① 一个新工具 `git_log`**——用 `defineTool` 声明，会出现在 Web UI 里、模型随时能调用[^S8]；**② 一个可安装的 bundle**——打包好的插件包，装进 profile 就能复用[^S5][^S9]。

> [!tip] 大白话
> 改造脚手架 = 领一套带精装修的模板房：不用从地基砌砖，先住进去，再按自己的喜好改客厅。所以别怕「不会写插件」——你不是从零盖房，只是改精装房。

> [!note] 这在 Claude Code 里相当于
> 本节要交付的 `git_log`，约等于你在 Claude Code 里声明一个自定义 tool（name + description + parameters），让 agent 能调用；「模型在 Web UI 里调用它」约等于「Claude Code 里 agent 调用你的自定义工具」。

### 你要走完的 8 步（先混个眼熟，细节后面每节拆开）

```bash
# ① 前提：源码环境已就绪（clone → pnpm install → pnpm run build），在 dsh 仓库根目录
#    —— 这一步得到：一个能跑 dsh 的本地源码仓库

# ② 拷贝脚手架：把 example-plugin 复制成「你自己的插件目录」
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin
#    —— 这一步得到：一份可以随便改、不碰原件的插件骨架

# ③ 改 dev-cordis.yml 的 name 为指向 src/index.ts 的绝对路径
#    —— 这一步得到：开发期 patch 指向你的入口（相对路径会静默失效，后面细讲）

# ④ 启动加载：确认插件被框架接住
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
#    —— 预期输出：[repo-status-plugin] plugin loaded!

# ⑤ 验证配置层：确认 patch 真的合进了合成配置
pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config
#    —— 预期输出：合成配置里出现 repo-status 行

# ⑥ 浏览器开 http://127.0.0.1:3080 新建会话，让模型调用 repo_status
#    —— 这一步得到：一个「模型能调用的工具」真的出现在 Web UI 里

# ⑦ 打包：装依赖 + 编译，产出可安装产物
cd example-plugin && pnpm install && pnpm run build
#    —— 这一步得到：dist/（bundle 的料理包本体）

# ⑧ 装进 profile：本地目录安装并验证
dsh plugin --profile demo add ./example-plugin
dsh --profile demo --dump-config
#    —— 预期输出：出现 "# == dsh-repo-status-plugin" 层
```

改造完成后，模型在 Web UI 里调用 `git_log` 的样子大致如下——`execute` 跑 `git log --oneline -n <max>`，`render` 把结果转成模型能读的文本：

```text
# 模型调用 git_log（参数 max=5）后，模型看到的输出：
最近 5 条提交：
db5f25c vault backup: 2026-08-15 18:17:40
99aa24a vault backup: 2026-08-15 18:16:37
d02e904 vault backup: 2026-08-15 18:15:13
c0da45b vault backup: 2026-08-15 18:11:16
4ced37b vault backup: 2026-08-15 18:08:53
```

接下来的每一节，就是把这 8 步**逐个拆开**，每步给你「可复现命令 + 预期输出 + 出错排查」——终点长什么样你已经看到了，现在从第 2 步（拷贝脚手架）开始动手。

## 2. 环境确认 + 拷贝脚手架（5 分钟热身）

第一节那 8 步能不能走完，取决于两块地基：环境是否可用、脚手架是否到手。本节只热身、不写代码——先把地基打好：确认环境 + 领到模板房。

### 环境确认三连

开工前花 1 分钟做个体检，缺哪步回第 2 章补课：

- [ ] dsh 源码仓库已 clone 到本地
- [ ] `pnpm install && pnpm run build` 已跑通
- [ ] 在仓库根目录 `pnpm dsh web --patch <某插件 dev patch>` 能起 Web UI

第 ③ 步的通过标准：终端打印 `plugin loaded!`，浏览器能开 http://127.0.0.1:3080 [^S1]。达标说明「脚手架 + 你的机器」没毛病，才值得动手改造。

### 拷贝脚手架

把 vault 里的模板房复制一份到自己工作区：

```bash
cp -r "<vault>/AI学习/DeepSeek-Harness 教程/example-plugin" ./example-plugin
```

拷贝 = 领一套带精装修的样板房：随便拆改，原件永不碰 [^S7]。拷完这些文件各司其职：

- `package.json` — 包名、构建脚本、`dsh.bundle.patch` 指向
- `tsconfig.json` — 编译配置（src → dist）
- `src/index.ts` — 注册中心：装配 Config + 注册工具
- `src/tools/repo-status.ts` — 工具本体：`repo_status` 的 defineTool
- `dev-cordis.yml` — 开发期 patch，`name` 指向本地绝对路径
- `cordis.patch.yml` — 打包期 patch，`name` 用 npm 包名

### 第一次跑通原版

把 `dev-cordis.yml` 的 `name` 改成指向 `./example-plugin/src/index.ts` 的**绝对路径**，然后加载：

```bash
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
```

```text
# 预期输出
[repo-status-plugin] plugin loaded!
```

这一步证明「脚手架 + 你的环境」是通的，第三节的改造才有基线可对比。

> [!tip] 大白话
> 环境确认 = 开工前检查水电煤气都通，别等砌到一半才发现没水；拷贝 = 领到模板房钥匙，原件锁在开发商那里，房间随便你装修。

> [!note] 这在 Claude Code 里相当于
> `--patch` 指向 dev-cordis.yml，≈ Claude Code 里用 `--append-system-prompt` 或加载本地插件源码目录——都是「开发期用本地代码、不发布」的姿势。

> [!warning] 两个坑，踩了会白忙
> `--patch` 循环必须在 dsh 源码仓库根目录跑，别用 `npx @deepseek-ai/dsh`；patch 的 `name` 必须是绝对路径，相对路径会静默失效、且没有任何报错 [^S11]。

地基稳了、模板房到手了——下一节，动手把 `repo_status` 改造成你自己的 `git_log`。

## 3. 写——把 repo_status 改造成 git_log

第二节证明了脚手架能跑（`[repo-status-plugin] plugin loaded!`），现在动手做本节唯一一件事：把 `repo_status` 改造成 `git_log`。只动两个文件，改完你会看到那句属于你的确认信号。

### 第一步：新建工具本体 `src/tools/git-log.ts`

`src/tools/` 是工具本体的家[^S8]，我们新建 `git-log.ts`，逐字粘贴下面的代码：

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const exec = promisify(execFile)

interface ToolOptions {
  maxCommits: number
}

export function gitLogTool(options: ToolOptions) {
  return defineTool({
    name: 'git_log',
    description: 'Show a compact summary of the most recent commits in the current workspace.',
    parameters: {
      max: {
        type: 'number',
        required: false,
        description: 'Max commits to list (default from plugin config).',
      },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      const max = args.max ?? options.maxCommits
      const { stdout } = await exec('git', ['log', '--oneline', '-n', String(max)])
      return stdout.trim() || '(no commits)'
    },
  })
}
```

逐句讲：`gitLogTool(options)` 是工厂函数，`options.maxCommits` 是插件配置给的默认上限（第 4 节会在 patch 里给它传值）。`defineTool({...})` 的字段就是给模型看的「招式表」[^S8]：`name: 'git_log'` 是模型调用时的工具名；`description` 决定模型**何时**调用它；`parameters.max` 是可选的参数 schema，`execute` 前框架会自动校验模型填的参数。`execute(args)` 是真正干活的地方——跑 `git log --oneline -n <max>` 拿最近提交概览。按工具契约[^S11]，它**只返回 `output.schema` 声明的单一 canonical 值**（这里是 string），不塞给人看的 prose；`output.render` 负责把它转成模型可见的文本块，展示层归它管。如果当前目录根本不是 git 仓库，`exec('git', ...)` 会 reject——**基础设施失败直接 throw**，框架标记 `isError`，模型能看到失败而不是拿到乱码；而「没有提交」是正常业务态，返回 `'(no commits)'` 让模型自己判断。

### 第二步：改注册中心 `src/index.ts`

`src/index.ts` 是注册中心：`name`/`inject` 写在这，`apply(ctx)` 里的注册动作也在这[^S8]。整体替换成：

```ts
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'
import { gitLogTool } from './tools/git-log'

export interface Config {
  /** git log 默认显示的提交数上限 */
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})

export const name = 'git-log-plugin'
export const inject = ['tools']

export function apply(ctx: Context, config: Config) {
  ctx.tools.register(gitLogTool(config))
}
```

只点三处改动，其余不用深究：import 从 `repoStatusTool` 换成新文件的 `gitLogTool`；注册动作变成 `ctx.tools.register(gitLogTool(config))`——`config` 直接喂给工厂，`maxCommits` 就成了工具默认上限，注册即 effect，插件卸载自动注销工具[^S8]；诊断名从 `repo-status-plugin` 改成 `git-log-plugin`。至于 `Config` 从两个字段简化为一个 `maxCommits`，这里先带过，schema 原理第 4 节专门讲。

### 灵魂：四处名字，别搞混

改造最容易翻车的就是名字——同一件事有四个名字，各管各的[^S7][^S11]：

| 名字 | 值（改造后） | 改在哪 | 改错了会怎样 |
|---|---|---|---|
| 诊断名 `export const name` | `git-log-plugin` | `src/index.ts` 顶部 | 只出现在日志/加载消息；错了仅日志难看，不影响功能 |
| 包名 `package.json` name | `dsh-git-log-plugin` | `package.json` | 打包后 bundle 层的 patch `name` 必须引用它（第 6 节），不一致加载失败 |
| 实例 id patch `id` | `git-log` | `dev-cordis.yml` / `cordis.patch.yml` | 合成配置里插件实例的标识；第 5 节 `--dump-config` 靠它辨认 |
| 模型可见工具名 defineTool `name` | `git_log` | `src/tools/git-log.ts` | Web UI 里模型真正调用的名字；改错模型根本找不到这个工具 |

> [!tip] 大白话
> `defineTool` 是**教模型一个新招式**：在招式表里登记 `name`（招名）+ `description`（啥时候用）+ `parameters`（要什么料），模型读了才会在合适的时机喊你。而四处 name 是三件不同的东西：**身份证**（诊断名，报名字用）≠ **工牌**（包名，发布分发用）≠ **花名**（工具名，模型嘴上喊的）；patch 的 `id` 则是你给这个实例起的内部编号。

> [!note] 这在 Claude Code 里相当于
> `defineTool({ name, description, parameters, output, execute })` ≈ Claude Code 里自定义 tool 的 `name + description + input_schema`——多出的 `output.schema/render` 就是把返回结果整理进对话的机制；`render` 把 canonical 值转成文本 ≈ 工具结果落进 conversation 给模型看的那一步。

### 验证信号

改完重新加载：`pnpm dsh web --patch ./example-plugin/dev-cordis.yml`，预期输出变成：

```
[git-log-plugin] plugin loaded!
```

这一句从 `repo-status-plugin` 换成 `git-log-plugin`，就是「你写成了」的确认信号。下一步（第 4 节）给这个工具加配置项，让它可调。

## 4. 配——Config schema 加可调参数 + patch 传值

第 3 节写完了工具，本节给 `git_log` 加一个「可调旋钮」——提交数上限 `maxCommits`。

### 为什么做成配置项

「不硬编码可调值」：不同项目想看 5 条还是 50 条提交，不该改代码。判断标准一句话：**两个部署可能设不同值 → 做成配置字段**[^S2]。这样换项目只改配置、不改源码。

### Config schema 两步

在 `src/index.ts` 里分两步声明「这个插件要什么参数、默认多少」：

```ts
export interface Config {
  /** git log 默认显示的提交数上限 */
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})
```

- ① `interface Config` 声明字段与类型（`maxCommits: number`）；
- ② 导出**同名 `Config`** 的 Schemastery schema。两个要点：**必须**用 `Schema.object` 导出（普通 JS 对象缺 Standard Schema 接口，框架读不了你的参数契约[^S2]）；默认值用 `.default()` 写在 schema 上，用户没传时兜底为 5[^S2]。

### 两份 patch 传值

改好 schema，让两个部署环境把值传进来。`dev-cordis.yml` 与 `cordis.patch.yml` 各加一个 `config:` 块，并统一把 `id` 改成 `git-log`：

```yaml
# 开发层 patch：插件路径必须是【绝对路径】（dsh 要求，相对路径会失效）
- insert:
    - id: git-log
      name: '/absolute/path/to/example-plugin/src/index.ts'
      config:
        maxCommits: 5
```

```yaml
# 打包层 patch：插件行按包名引用（Node resolution 从 profile node_modules 找已安装代码）
- insert:
    - id: git-log
      name: dsh-git-log-plugin
      config:
        maxCommits: 5
```

两份 patch 长得像、角色不同[^S7]：**dev 层 `name` 用绝对路径指向源码**，改完立刻生效；**bundle 层用包名 `dsh-git-log-plugin` 指向已安装产物**，发布后别人装的是这份[^S7]。`id: git-log` 两边一致，它只是给插件实例起的诊断名（模型可见的工具名是第三节 `defineTool` 里的 `git_log`，两者可以不同）。

> [!tip] 大白话
> Config schema = **岗位说明书 / 入职登记表**：提前声明「这个插件要什么参数、默认多少」。`config:` 传值 = **入职时在表上填你想要的默认值**：同一张登记表，不同项目填 5 还是 50，随你。

> [!note] 这在 Claude Code 里相当于
> Schemastery schema ≈ Claude Code tool 的 `input_schema`——声明参数的类型、必填、默认；`.default(5)` ≈ `input_schema` 里的 `default`；配置校验失败 ≈ 工具参数校验失败时直接报错给你看。

### 易错点三连

- **Schemastery 没有 `.optional()`**：字段默认就是可选的，要必填得显式 `.required(true)`[^S11]。
- **补丁树整行替换、不做深合并**：想覆盖某一行，必须把这一行需要的 key 全写上，别指望框架帮你补齐[^S9]。
- **坏配置加载即响亮失败**：报 ValidationError / fiber FAILED，不会静默兜底[^S4]——写错立刻发现，是好事。

配置就绪。下一节用命令链验证「改得对不对」。

## 5. 验证——加载、看配置层、让模型真正调用

前三节把脚手架的 `repo_status` 改造成了 `git_log`，第四节又把 `maxCommits` 接进了配置层——但「改了」不等于「能跑」。本节用「验证四连」逐层确认：插件被框架接住、配置层真的注入、模型能真正调用、headless 端到端生效；每连都给命令 + 预期输出 + 它证明了什么，最后附一张排查表。以下命令都在 dsh 源码仓库根目录执行（开发期不用 `npx @deepseek-ai/dsh`）。[^S1]

### 5.1 验证第一连：插件被框架接住

```bash
# dev-cordis.yml 的 name 已指向改造后的 src/index.ts（绝对路径）
pnpm dsh web --patch ./example-plugin/dev-cordis.yml
```

预期输出：

```
[git-log-plugin] plugin loaded!
```

**这一验证证明什么**：入口注册成功——`apply(ctx)` 被执行，加载消息与诊断名 `git-log-plugin` 一致；若看到 `repo-status-plugin`，说明加载的还是未改造的旧配置。[^S1][^S7]

### 5.2 验证第二连：配置层真的注入

```bash
pnpm dsh --profile web --patch ./example-plugin/dev-cordis.yml --dump-config
```

预期输出（节选）：

```yaml
# 合成配置中出现 git-log 层
git-log:
  maxCommits: 5
```

**这一验证证明什么**：patch 生效、Config 读到——`config:` 传的值进入了合成配置，`maxCommits` 落到实例上，没有被静默丢弃。[^S7][^S9]

> [!tip] 大白话
> 把 `--dump-config` 想成**切开千层饼看每一层**：默认配置、profile、patch 各自摊开一层摆在眼前，哪一层放了什么一眼看清。所以「patch 到底生效没有」不用猜，切一刀就知道。

> [!note] 这在 Claude Code 里相当于
> `--dump-config` ≈ Claude Code 里展开 `--settings` 看生效配置 + 检查插件是否注册。都是先看清楚运行时真正拿到的配置，再动手调试。

### 5.3 验证第三连：模型能真正调用

浏览器开 `http://127.0.0.1:3080` → 新建会话 → 让模型调用 `git_log`（可提示它「看看最近的提交」）→ 模型返回最近 N 条提交。

预期输出（模型回复，示意）：

```
最近的提交：
- a1b2c3d feat: 新增 git_log 工具
- d4e5f6a fix: 修正 repo_status 的参数名
- ...
```

**这一验证证明什么**：工具对模型可见、可执行、结果回传——defineTool 的 name/description 被模型读到，execute 被真正执行，返回被带回对话。[^S1]

### 5.4 验证第四连：端到端真实生效

```bash
dsh --profile headless "最近 5 条提交是什么？"
```

预期输出：

```
（模型调用 git_log 后作答，示意）
最近的 5 条提交是：a1b2c3d feat: 新增 git_log 工具 / d4e5f6a fix: 修正 repo_status 参数名 / ...
```

**这一验证证明什么**：不是只有 Web UI 才加载——headless 模式下插件同样被装配，工具在无界面会话里也能被调用并拿到结果。[^S11]

> [!tip] 大白话
> `--profile headless` 想成**不点页面、直接问一句看它答不答得上来**：Web UI 像有人陪着练，headless 是把陪练撤了直接开考——能答上来，才说明工具是「真会」而不是界面在兜底。

> [!note] 这在 Claude Code 里相当于
> headless 端到端 ≈ 在命令行直接让 agent 用工具完成任务（相当于 `claude -p "..."` 无交互模式）——验证「工具真的被模型执行并回传结果」，而不是只在界面上看得到。

### 5.5 错误排查表

验证失败先对号入座，不要盲目重来：

| 现象 | 可能原因 | 排查命令 / 动作 |
|---|---|---|
| `plugin loaded!` 一直不出现 | 拼写错 / patch `name` 不是绝对路径 | 先查 `src/index.ts` 路径与 `export const name` 拼写，再 `--dump-config` 看有没有 `git-log` 行 |
| 模型列表里没有 `git_log` | `inject` 的 tools 服务未就绪（PENDING 不加载） | 检查 `export const inject = ['tools']` 依赖声明 |
| `--patch` 配错但无报错 | dev patch `name` 是相对路径 / 写错（静默失败） | 确认 `dev-cordis.yml` 的 `name` 为绝对路径，对照第 2 节示例 [^S12] |
| 配置改了没生效 | 补丁树整行替换、不做深合并；HMR 热替换旧实例注册自动清理 | 重看第 4 节易错点：覆盖要重写所有需要的 key，改完确认 HMR 已重载 |
| 其他 | bundle 层错 vs 上层覆盖错 | `dsh --profile <name> --dump-default-config` 分层定位 |

## 6. 打包——bundle 打包 + profile 安装 + git 安装的坑

第 5 节证明了开发期插件能跑；本节把插件变成「能分发给别人的料理包」，装进 profile，让 `git_log` 在普通启动下也能被模型调用。

### 打包：产出 `dist/`

```bash
cd example-plugin && pnpm install && pnpm run build
```

**预期输出**：`tsc` 编译完成，`example-plugin/dist/` 下出现 `index.js`、`index.d.ts`。

动手前先看 `package.json` 三个关键点（S7 实测）[^S7]：

1. **入口 + 发布白名单**：`main: "dist/index.js"` + `files: ["dist", "cordis.patch.yml"]`——`npm publish` 只带这两样，源文件和 dev 配置不上架；
2. **build + prepare**：`scripts.build = "tsc -p tsconfig.json"`（rootDir=src → outDir=dist）、`scripts.prepare = "npm run build"`——`prepare` 是「装依赖时自动 build」的钩子，是后面 git 安装能用的前提；
3. **bundle 声明**：`dsh.bundle.patch = "./cordis.patch.yml"`——告诉 dsh「这个包贡献一层配置」。

先钉死两个词：**bundle** = 带 `dsh.bundle.patch` 声明的 npm 包（料理包）[^S5]；**profile** = 目录里声明 `dsh.profile.bundles` 的有序列表（上菜顺序单）[^S9]。`dsh plugin` 命令自动维护 profile，不用手写。

### 本地安装三步

```bash
# ① 把 ./example-plugin 装进 demo profile（dsh 命令在 dsh 源码仓库根目录或已安装 CLI 下运行）
dsh plugin --profile demo add ./example-plugin

# ② 打开 profile 的 package.json —— dsh.profile.bundles 应出现该包

# ③ 看合成配置：应出现 bundle 贡献的层
dsh --profile demo --dump-config
```

**预期输出**（③）：`--dump-config` 里出现

```text
# == dsh-git-log-plugin
```

这一行来自 bundle 的 `cordis.patch.yml`——注意 patch 的 `name` 必须等于 package.json 的 `name`（`dsh-git-log-plugin`），Node 才能从 profile 的 node_modules 里找到已安装代码[^S7]。

### git 安装的坑（警示为主）

官方没有独立的「安装命令」专页，命令族以 `dsh plugin` CLI 实测为准[^S11]：

```bash
dsh plugin --profile <name> add github:you/repo#<sha>
```

git 安装拉的是**源码**不是构建产物，所以三个坑：

1. 包必须带 **`prepare`** 脚本——装依赖时自动 build，否则装进去是缺 `dist/` 的半成品；
2. **pnpm≥10 默认拒绝跑 git 依赖的 `prepare`**——需要 **`allowBuilds`** 放行；
3. 用 **`#<sha>`** 钉死 commit，保证可复现。

> [!tip] 大白话
> - **bundle** = 料理包：预制好的菜，拿出来热一下就能上桌；**profile** = 上菜顺序单：先上哪个 bundle 的配置层。
> - **allowBuilds** = 给 git 依赖发一张「在我机器上跑 build 脚本」的门禁卡：pnpm 不放心陌生人喂的脚本，你签字它才跑。

> [!note] 这在 Claude Code 里相当于
> bundle 打包发布 ≈ Claude Code 插件市场：把自定义 slash command 或 MCP server 打包分发；`dsh plugin add` ≈ 安装第三方插件并启用。

安装后模型在 Web UI 里照样能调 `git_log`——现在你的插件已经能给别人用了。

## 7. 小结与下一步——换成你自己的工具

8 步走完，`example-plugin` 已被你改造成 `git_log`，写、配、验证、打包、安装整条 A→C 链路都亲手跑过[^S7]。收尾三件事：把全链路压成一张 checklist、记住三处最容易翻车的点、然后把它换成你自己的工具。

### A→C 全链路回顾

| 环节 | 做了什么 | 关键命令 / 文件 |
|---|---|---|
| ① 写 | 建 `src/tools/git-log.ts` 写 `defineTool`，改 `src/index.ts` 注册 | `defineTool`（name/description/parameters/output/execute）+ `ctx.tools.register` |
| ② 配 | Config schema 加可调参数，patch 里 `config:` 传值，不硬编码[^S2] | `dev-cordis.yml` / `cordis.patch.yml` |
| ③ 验证 | 加载成功 → 配置层注入 → 模型调用 → 端到端 | `pnpm dsh web --patch` → `--dump-config` → Web UI → `dsh --profile headless "..."` |
| ④ 打包 | 装依赖 + 编译出 dist/ | `cd example-plugin && pnpm install && pnpm run build` |
| ⑤ 安装 | 装进 profile，看到自己的配置层 | `dsh plugin --profile demo add ./example-plugin` → `--dump-config` 见 `# == dsh-...` |

### 自查清单（改别人工具 / 重写前对着过一遍）

- **第 2 节｜绝对路径**：dev patch 的 `name` 必须是指向 `src/index.ts` 的**绝对路径**，相对路径静默失效。
- **第 3 节｜四处名字**：`export const name`（诊断）/ package.json `name`（包名）/ patch `id`（实例）/ defineTool `name`（模型可见），别混[^S7]。
- **第 6 节｜打包三件套**：`prepare` 脚本 + pnpm≥10 的 `allowBuilds` 放行 + git 安装用 `#<sha>` 钉 commit；bundle patch `name` == package.json `name`[^S11]。

### 下一步：换成你自己的工具

| 工具想法 | defineTool 要改哪 | execute 换成什么 | 要不要加配置项 |
|---|---|---|---|
| API 封装（天气 / 股票 / 汇率） | name + description + parameters | `fetch('https://api...')` + 解析结果 | 建议：endpoint、key 做成 config |
| 笔记检索（在 vault 里搜） | name + description + parameters | `rg` 扫 vault 目录 + 组装结果 | 建议：vault 路径做成 config |
| 目录统计（各目录文件数） | name + description + parameters | `find <dir> -type f` + 汇总 | 可选：目录路径做成 config |
| 构建脚本（跑测试 / 编译） | name + description + parameters | `pnpm run build` / `tsc` | 视情况：目标路径做成 config |

任何「agent 能帮你做、但需要执行外部命令/查数据」的事，都能包成 dsh 工具[^S7]——改 `defineTool` 的 name/description/parameters 告诉模型它是什么、要什么参数，再换 `execute` 里的命令/调用。

> [!tip] 大白话
> 改造脚手架 = 拿到模板房钥匙后，自己决定每间房用来做什么。`git_log` 是改好的第一间；下一个工具只是给 `execute` 摆上不同的家具，钥匙（A→C 链路）已经在你手里。

> [!note] 这在 Claude Code 里相当于
> 「换成你自己的工具」≈ 在 Claude Code 里持续往工具包里加自定义 tool / MCP——一样是「一次声明（name + description + parameters）、到处调用」，攒多了就是你的工具箱。

## 本章小结

本分册没让你从零盖房：改造 `example-plugin` 脚手架走通了写 → 配 → 验证 → 打包 → 安装。核心就四招——四处名字别混、可调值进 Config schema 不硬编码、`--dump-config` 切层排查、打包靠 `prepare` + `allowBuilds` + `#<sha>`。第 4 章教你插件怎么从零长出来，本分册教你拿到现成的怎么快速改成自己的，两章合起来，从看懂到亲手交付就齐了。挑一个上表里的想法（或你自己的），照第三节到第六节再来一遍，就正式出师。本分册产出已同步系列 README 与 MOC。

## 注释

[^S1]: [官方 docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md)（raw 镜像抓取）· official · 2026-08-15 · 首插件五步、绝对路径要求、`plugin loaded!` 预期输出、inject+tools.register

[^S2]: [官方 docs/user/develop/basic/config.md「插件配置」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/config.md)（raw 镜像抓取）· official · 2026-08-15 · Config+Schemastery 模式、默认值、cordis.yml config、坏配置响亮失败、HMR

[^S4]: [官方 docs/cordis-tutorial/05-config.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-tutorial/05-config.md) · official · 2026-08-15 · 坏配置→fiber FAILED / ValidationError

[^S5]: 官方 [docs/architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md)（raw 镜像抓取）· official · 2026-08-15 · bundle / profile 分层概念

[^S7]: 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` · vault-note · 2026-08-15 · 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / dev-cordis.yml / cordis.patch.yml

[^S8]: 本地 vault `DeepSeek-Harness 插件开发核心.md`（第 3 章）· vault-note · 2026-08-15 · apply / 生命周期 / 依赖 / defineTool / hook / 提示词

[^S9]: 本地 vault `DeepSeek-Harness 配置体系.md` · vault-note · 2026-08-15 · 补丁树 / Profile vs Agent Preset / Config schema / bundle vs profile

[^S11]: 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章）· vault-note · 2026-08-15 · 分环节坑清单、dsh plugin 命令族、工具契约

[^S12]: [pingfanfan/hello-dsh](https://github.com/pingfanfan/hello-dsh) · community · 2026-08-15 · 零基础中文实例、checkpoint、`--patch` 静默失败实测坑（对照参考）

## 更新记录

- 2026-08-15：创建本分册。
