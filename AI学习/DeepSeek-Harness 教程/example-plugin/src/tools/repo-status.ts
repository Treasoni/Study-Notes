import { defineTool } from '@deepseek-ai/dsh-tools'
import { execFile } from 'node:child_process'
import { promisify } from 'node:util'

const exec = promisify(execFile)

interface ToolOptions {
  defaultMaxEntries: number
  includeUntracked: boolean
}

// 你的自定义工具本体：把 execute 换成你真正想给 agent 的能力即可
export function repoStatusTool(options: ToolOptions) {
  return defineTool({
    // 模型看到的工具名与描述：描述决定「何时被调用」
    name: 'repo_status',
    description: 'Summarize the git working-tree state of the current workspace.',

    // 参数 schema：execute 前自动校验，并推断 args 的类型
    parameters: {
      maxEntries: {
        type: 'number',
        required: false,
        description: 'Max changed files to list (default from plugin config).',
      },
    },

    // 契约（第 3 章 3.7 / 第 5 章 5.3）：
    //   execute 只返回 output.schema 声明的单一 canonical JSON 值；
    //   render 负责转成模型可见文本；基础设施失败直接 throw（= isError）。
    output: {
      schema: { type: 'string' },
      render: (_args, value) => [{ type: 'text', text: value }],
    },

    async execute(args) {
      const max = args.maxEntries ?? options.defaultMaxEntries
      // 不是 git 仓库等基础设施错误会 reject → 框架标记 isError，模型能看到失败
      const { stdout } = await exec('git', ['status', '--short', '--branch'])
      return summarize(stdout, max, options.includeUntracked)
    },
  })
}

function summarize(raw: string, max: number, includeUntracked: boolean): string {
  const lines = raw.trim().split('\n').filter(Boolean)
  const head = lines.shift() ?? '(empty)'
  const rest = lines.filter((l) => includeUntracked || !l.startsWith('??'))
  const shown =
    rest.length > max ? [...rest.slice(0, max), `… and ${rest.length - max} more`] : rest
  return [head, ...shown].join('\n')
}
