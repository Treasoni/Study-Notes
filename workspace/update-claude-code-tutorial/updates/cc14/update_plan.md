# cc14 更新计划（update_plan）

> 笔记：Claude MCP 使用指南 · note_id：cc14
> 更新目标：同步到 2026-08 现状（SB-17 MCP 变更 + 任务要求）

## 过时点与处理计划

| # | 过时点 | 证据 | 处理动作 | 影响范围 |
|---|--------|------|---------|---------|
| 1 | MCP capability discovery 无自动重试说明 | SB-17（v2.1.191+） | 新增小节「Capability discovery 自动重试」：`tools/list`、`prompts/list`、`resources/list` 对瞬时网络错误自动重试 | §7 高级功能 |
| 2 | macOS keychain 超时导致 OAuth 401 突发未提及 | SB-17（v2.1.225+） | §2 OAuth 功能表后新增 `[!tip]` 修复说明；§12 故障排查新增排查项 | §2、§12 |
| 3 | `claude mcp list`/`get` 自批准行为与插件同意未提及 | SB-17 | §3 新增 `[!warning]`：list/get 不再自批准 `.mcp.json` 自带服务器；§4 新增 `[!warning]`：外部插件 MCP 需安装同意 | §3、§4 |
| 4 | 会话工作目录未加入 MCP roots | SB-17（v2.1.203+） | §7「动态工具更新」扩展为「动态工具更新与 roots 同步」，补充 `roots/list` 与 `notifications/roots/list_changed` | §7 高级功能 |
| 5 | 长耗时 MCP 工具调用无自动转后台说明 | SB-17（v2.1.224 附近） | 新增小节「长耗时工具调用自动转后台」：超 2 分钟转后台，`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` 可调 | §7 高级功能 |
| 6 | 核心概念缺「大白话」 | 任务要求 | §1 什么是 MCP、§1 传输方式各加一个 `[!tip] 大白话` callout | §1 |
| 7 | frontmatter `updated` / 章节编号重复 | 任务要求 + 结构核对 | `updated` → 2026-08-10；`status` 保持 `updated`；重复的 `## 12.`（CLI 命令速查）改为 `## 13.` | frontmatter、§12/§13 |
| 8 | 缺更新记录 | 任务要求 | 文末追加 `## 更新记录` 表（2026-08-10 行） | 文末 |

## 更新原则

- **局部 patch**：只改过时段落与新增必要小节，不重写未过时内容；保持原结构和写作风格。
- **不修改原 vault 文件**：全部产物写入 `updates/cc14/`，供用户审阅后写回。
- **不引入 source_bank 未覆盖的新事实**：版本号（v2.1.191/203/225）均来自 SB-17 摘要，未额外臆造。
- **Obsidian 规范**：新增说明用 `[!tip]`/`[!warning]`；核心概念用 `[!tip] 大白话`；列表内不嵌套表格；frontmatter 无特殊字符值，无需加引号。
- **§6 连接外部工具/数据源章节已核对**：filesystem/postgres/github/sentry 等推荐服务器仍为 2026-08 现状，保留不动。
