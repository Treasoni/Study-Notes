---
title: "DeepSeek-Harness 插件开发实战：自定义工具插件"
tags: [deepseek-harness, ai, agent, 插件, 教程, 实战, claude-code]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# 实战：从零写一个自定义工具插件（每一步对照 Claude Code）

> [!summary] 本章导读
> 前三章把 dsh 插件的零件讲完了。这一章把它们装成一辆车：从零写一个**自定义工具插件**，走完「搭骨架 → 写工具 → 加配置 → 加载跑通 → 打包发布」全程。每一步都标注「这在 Claude Code 里相当于」，让已经熟悉 Claude Code 的你不用二次建模。

## 4.1 项目定位与路线图

**目标**：写一个自定义工具插件，让 agent 多一个 `repo_status` 工具——返回当前仓库的变更状态摘要。你自己写插件时，只需替换工具的实现（如换成你的 API 封装、笔记检索、构建脚本），流程完全一样。

**前提**：已完成第 2 章的源码构建（clone → `pnpm install` → `pnpm run build`），在仓库根目录工作[^1]。

> [!example] 配套脚手架
> 本系列附带完整可跑的插件脚手架 **`example-plugin/`**（与本例同代码）：源码环境就绪后，把 `dev-cordis.yml` 的 `name` 改成你机器上的绝对路径即可跑通；想做成自己的插件，只换 `src/tools/repo-status.ts` 的 `execute`。

**路线图**：

| 步 | 做什么 | 产出 | 这在 Claude Code 里相当于 |
|---|---|---|---|
| 1 | 搭插件骨架 | `my-plugin.ts` + `cordis.yml` | 新建一个 `.claude/commands/*.md` 或 skill 目录 |
| 2 | 注册第一个工具 | `greet` 可被模型调用 | 让模型能调一个自定义 command/工具 |
| 3 | 写你自己的工具 | `repo_status` 插件本体 | 把「你常手工做的事」交给 agent |
| 4 | 加配置 | 可调参数，HMR 生效 | 给命令加可配置项 |
| 5 | 打包发布 | bundle 装进 profile | 发布成可复用的包 |

## 4.2 第一步：搭插件骨架

在源码仓库根建 `scratch-plugin/`（官方教程的标准做法）[^1][^2]：

```ts
// scratch-plugin/src/my-plugin.ts
export const name = 'my-plugin'              // 诊断元数据，可省
export function apply(ctx) {
  console.log('[my-plugin] plugin loaded!')  // 先确认被加载
}
```

```yaml
# scratch-plugin/cordis.yml
- insert:
    - id: my-plugin
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
```

> [!warning] 路径必须是绝对路径
> patch 层只贡献配置，不改变 loader 解析模块路径时用的 profile 目录。相对路径会找不到模块。这是新手第一坑，第 5 章 5.1 还会再点名。

加载验证：

```bash
pnpm dsh web --patch ./scratch-plugin/cordis.yml
# 打开 http://127.0.0.1:3080，终端应打印 [my-plugin] plugin loaded!
```

> [!note] 这在 Claude Code 里相当于
> 建 `.claude/skills/foo/SKILL.md` + 在设置里注册。Claude Code 是「改文件声明扩展」，dsh 是「写代码 + 用 patch 装进插件树」。

## 4.3 第二步：注册第一个工具（greet）

把 `apply` 改成注册一个工具。先照官方最小示例 `greet` 跑通「模型能调到你注册的工具」这条链路[^3]：

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']              // 依赖 tools 服务就绪后才加载

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',   // 模型看到的描述，决定何时被调用
    parameters: {
      name: { type: 'string', required: true, description: 'The name to greet' },
    },
    output: {
      schema: { type: 'string' },                            // canonical 返回值
      render: (_args, value) => [{ type: 'text', text: value }],  // 模型可见内容
    },
    async execute(args) {
      return `Hello, ${args.name}!`          // args 已按 parameters 校验并推断类型
    },
  }))
}
```

保存后重载页面，新建会话让模型「用 greet 打个招呼」——它应输出 `Hello, Ada!`。

> [!note] 这在 Claude Code 里相当于
> 在 Claude Code 里给模型加「工具」靠 MCP server。dsh 里一个工具就是一个 `defineTool` 对象直接注册，没有进程边界。

## 4.4 第三步：写你自己的工具（repo_status）

现在把 `greet` 换成你的工具。目标是**读当前仓库状态并返回紧凑摘要**——这是典型的「模型需要、但不想看一屏原文」的能力[^4]：

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const exec = promisify(execFile)

export const name = 'repo-status-tool'
export const inject = ['tools']

export function apply(ctx) {
  ctx.tools.register(defineTool({
    name: 'repo_status',
    description: 'Summarize the git working-tree state of the current workspace.',
    parameters: {
      maxEntries: {
        type: 'number', required: false,
        description: 'Max changed files to list (default 10).',
      },
    },
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },
    async execute(args) {
      // 基础设施失败就 throw（执行器会标记为 isError）
      const { stdout } = await exec('git', ['status', '--short', '--branch'])
      return summarize(stdout, args.maxEntries ?? 10)
    },
  }))
}

function summarize(raw: string, max: number): string {
  const lines = raw.trim().split('\n').filter(Boolean)
  const head = lines.shift() ?? '(empty)'
  const rest = lines.length > max ? [...lines.slice(0, max), `… and ${lines.length - max} more`] : lines
  return [head, ...rest].join('\n')
}
```

> [!note] 工具契约要点（完整见第 5 章 5.3）
> - `execute` 只返回 `output.schema` 声明的**单一 canonical JSON 值**，展示交给 `output.render`；
> - 业务成功态放进 canonical 值；**基础设施失败（如不是 git 仓库）直接 throw** → 模型看到 isError；
> - `args` 由框架在 execute 前按 `parameters` 自动校验。

## 4.5 第四步：加配置（可调，HMR 热替换）

「两个部署想设不同值」的字段就做成配置（测试：`cordis.yml` 不改代码能否改值）[^2][^5]：

```ts
import Schema from '@deepseek-ai/schemastery'
import { defineTool } from '@deepseek-ai/dsh-tools'

export interface Config {
  defaultMaxEntries: number
}
export const Config: Schema<Config> = Schema.object({
  defaultMaxEntries: Schema.number().default(10),
})

export const name = 'repo-status-tool'
export const inject = ['tools']

export function apply(ctx, config: Config) {
  ctx.tools.register(defineTool({
    name: 'repo_status',
    description: 'Summarize the git working-tree state of the current workspace.',
    parameters: {
      maxEntries: {
        type: 'number', required: false,
        description: 'Max changed files to list (default from config).',
      },
    },
    output: { schema: { type: 'string' }, render: (_a, v) => [{ type: 'text', text: v }] },
    async execute(args) {
      const max = args.maxEntries ?? config.defaultMaxEntries
      const { stdout } = await execFile('git', ['status', '--short', '--branch'])
      return summarize(stdout, max)
    },
  }))
}
```

在 `cordis.yml` 里配：

```yaml
- insert:
    - id: repo-status
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
      config:
        defaultMaxEntries: 20
```

改配置保存后**热替换**：旧实例自动清理，不残留。

## 4.6 第五步：打包成 bundle 并装进 profile

给别人用时，从 `--patch` 开发模式换成 **bundle**（npm 包，携带配置层）[^6]：

```
my-plugin/  (新目录，源码仓库根旁)
├── package.json       # 声明 dsh.bundle
├── cordis.patch.yml   # 装入 profile 时应用的层
└── index.js           # 插件代码（打包产物或手写 JS）
```

```json
{
  "name": "dsh-my-tool-plugin",
  "version": "0.1.0",
  "type": "module",
  "main": "index.js",
  "files": ["index.js", "cordis.patch.yml"],
  "dsh": { "bundle": { "patch": "./cordis.patch.yml" } }
}
```

```yaml
# cordis.patch.yml —— 插件行按包名引用（Node resolution 找已安装代码）
- insert:
    - id: repo-status
      name: dsh-my-tool-plugin
      config:
        defaultMaxEntries: 20
```

安装进 profile 并验证：

```bash
dsh plugin --profile demo add ./my-plugin        # 首次初始化 profile（@deepseek-ai/dsh-base 为第一个 bundle）+ 转发 pnpm + 追加 bundle
dsh --profile demo --dump-config                 # 应看到 "# == dsh-my-tool-plugin" 层
dsh --profile demo
```

> [!warning] git 安装（`github:you/my-plugin`）拉的是源码不跑 build
> 作者要提供 `prepare` 脚本（pnpm 在 git 安装后运行）自行构建产物；用户要在 profile 的 `pnpm-workspace.yaml` 里 `allowBuilds: dsh-my-tool-plugin: true` 放行，并 `#<sha>` 钉住 commit。想避开这套授权，直接发布预构建产物：npm 包或 `pnpm pack` 出的 tarball[^6]。

## 4.7 对照速查：Claude Code 概念 → 本实战

| 环节 | Claude Code | dsh（本实战） |
|---|---|---|
| 扩展载体 | skill / command / MCP server | 插件模块（`apply(ctx)`） |
| 给模型加能力 | MCP server / command | `ctx.tools.register(defineTool(...))` |
| 权限/前置检查 | `PreToolUse` hook | `ctx.on('tools/pre-execute', ...)` 返回 allow/deny |
| 可配置项 | 命令参数 / settings | `Config` schema + `cordis.yml` `config:` |
| 装到哪 | 全局/项目 settings | profile 的 `dsh.profile.bundles` |
| 分发给别人 | 发布 skill/MCP 包 | npm bundle（`dsh.bundle`） |

---

## 本章小结

> [!summary]
> - 路线五步：骨架 → 工具 → 自定义实现 → 配置 → 打包发布；
> - 骨架 = `apply(ctx)` + `cordis.yml` patch（**路径必须绝对**）+ `pnpm dsh web --patch`；
> - 工具 = `defineTool({name, description, parameters, output:{schema, render}, execute})`，`inject: ['tools']`；
> - 自定义工具的关键契约：canonical 返回值 + `render` 展示、基础设施失败 throw（= isError）；
> - 配置 = `Config` schema，`cordis.yml` `config:` 传入，HMR 热替换；
> - 发布 = bundle（`dsh.bundle.patch`）+ `dsh plugin --profile <name> add`；git 安装要 prepare + allowBuilds。

下一章收尾：[[DeepSeek-Harness 常见坑与速查|插件开发速查与排错]]——把坑、命令、工具契约、配置引用浓缩成常驻手边的速查。

---

## 更新记录

- 2026-08-15：从「与 Claude Code 对照迁移（换还是留 + 成本/性能对比）」整篇重构为「实战项目：自定义工具插件 walkthrough」。删除成本/性能对比表；改为从零到发布的完整示例，每步对照 Claude Code。

---

[^1]: 素材来源：官方「你的第一个插件」（2026-08-15 抓取）。
[^2]: 素材来源：官方「插件配置」（2026-08-15 抓取）。
[^3]: 素材来源：官方「开发一个 Tool」greet 示例（2026-08-15 抓取）。
[^4]: 素材来源：官方「Tool authoring reference」工具契约（2026-08-15 抓取）。
[^5]: 素材来源：官方 Cordis 教程 05「配置」（2026-08-15 抓取）。
[^6]: 素材来源：官方「打包并安装插件」（2026-08-15 抓取）。
