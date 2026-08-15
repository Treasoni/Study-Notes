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

## 注释

[^S1]: S1 | [官方 docs/user/develop/basic/index.md「第一个插件」](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md)（raw 镜像抓取） | official | 2026-08-15 | 首插件五步、绝对路径要求、`plugin loaded!` 预期输出、inject+tools.register

[^S7]: S7 | 本地 vault `AI学习/DeepSeek-Harness 教程/example-plugin/*` | vault-note | 2026-08-15 | 实战基底：README / package.json / tsconfig / src/index.ts / src/tools/repo-status.ts / cordis.patch.yml / dev-cordis.yml

[^S8]: S8 | 本地 vault `DeepSeek-Harness 插件开发核心.md`（第 3 章） | vault-note | 2026-08-15 | apply/生命周期/依赖/defineTool/hook/提示词

[^S11]: S11 | 本地 vault `DeepSeek-Harness 常见坑与速查.md`（第 5 章） | vault-note | 2026-08-15 | 分环节坑清单、dsh plugin 命令族、工具契约
