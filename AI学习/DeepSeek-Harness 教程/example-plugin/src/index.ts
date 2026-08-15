import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'
import { repoStatusTool } from './tools/repo-status'

// === 插件配置（第 3 章 3.6）：可调参数都做成 Config schema ===
export interface Config {
  /** 默认列出的变更文件上限 */
  defaultMaxEntries: number
  /** 是否包含未跟踪文件（?? 行） */
  includeUntracked: boolean
}

export const Config: Schema<Config> = Schema.object({
  defaultMaxEntries: Schema.number().default(10),
  includeUntracked: Schema.boolean().default(true),
})

// === 插件入口 ===
export const name = 'repo-status-plugin'
// 硬依赖 tools 服务：就绪前保持 PENDING，不会先加载（第 3 章 3.5）
export const inject = ['tools']

export function apply(ctx: Context, config: Config) {
  // 注册即 effect：插件卸载时自动注销工具（第 3 章 3.4）
  ctx.tools.register(repoStatusTool(config))
}
