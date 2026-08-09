# cc14 过时点地图（stale map）

> 笔记：Claude MCP 使用指南 · note_id：cc14
> 核对基线：`shared_research/source_bank.md`（SB-17）+ 官方 changelog 截至 2026-08-10
> 生成日期：2026-08-10

## 更新（UPDATE）

| # | 位置 | 原内容 | 过时原因 | 改为 |
|---|------|--------|---------|------|
| U1 | frontmatter `updated` | 2026-07-12 | 本次更新日期 | 2026-08-10 |
| U2 | §7 动态工具更新 | 仅描述 `list_changed` 通知 | SB-17：v2.1.203 起会话工作目录加入 MCP `roots/list` 并通知 `roots/list_changed` | 扩展为「动态工具更新与 roots 同步」，补充 roots/list 说明 |
| U3 | §12 故障排查 · OAuth 授权问题 | 无 macOS keychain 相关项 | SB-17：v2.1.225 修复 keychain 超时导致的 OAuth 401 突发 | 新增排查项「macOS 连续 401（密钥链超时）→ v2.1.225+ 已修复」 |
| U4 | §12/§13 章节编号 | 两个 `## 12.`（故障排查 + CLI 命令速查） | 结构性缺陷，编号重复 | CLI 命令速查 12 → 13 |

## 新增（ADD）

| # | 位置 | 新增内容 |
|---|------|---------|
| A1 | §1 什么是 MCP | `[!tip] 大白话` callout（MCP = AI 的 USB 接口） |
| A2 | §1 MCP 传输方式 | `[!tip] 大白话` callout（本地 stdio，云端 HTTP） |
| A3 | §2 OAuth 功能表后 | `[!tip]` macOS 密钥链超时导致 OAuth 401（v2.1.225+ 已修复） |
| A4 | §3 管理服务器 CLI 命令后 | `[!warning]` 安全行为：`claude mcp list`/`get` 不再自批准 `.mcp.json` 自带服务器 |
| A5 | §4 插件 MCP 工作原理后 | `[!warning]` 外部插件 MCP 需安装同意 |
| A6 | §7 高级功能 | 新小节「动态工具更新与 roots 同步」（含 roots/list、roots/list_changed，v2.1.203+） |
| A7 | §7 高级功能 | 新小节「Capability discovery 自动重试」（tools/list、prompts/list、resources/list 对瞬时网络错误重试，v2.1.191+） |
| A8 | §7 高级功能 | 新小节「长耗时工具调用自动转后台」（超 2 分钟转后台，`CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` 可调） |
| A9 | 文末 | `## 更新记录` 表格（2026-08-10 变更行） |

## 保留（KEEP）

- §1 MCP 简介：MCP 定义、核心价值、传输方式表、SSE 已废弃 warning —— 仍有效
- §2 安装：HTTP/SSE/stdio 三种传输配置、OAuth 2.0 认证、覆盖 OAuth 元数据发现、旧命令格式 tip —— 仍有效
- §3 管理服务器：`/mcp` 与 `claude mcp list` 区别 —— 仍有效
- §4 插件 MCP 服务器：工作原理、配置方式、功能、查看 —— 仍有效
- §5 MCP 安装范围：Local/Project/User 三级、范围优先级、环境变量扩展 —— 仍有效
- §6 常用 MCP 服务器推荐（连接外部工具与数据源章节）：filesystem/postgres/git/brave-search/github/sentry、add-json、实际示例、安全提示 —— 仍有效
- §7 其余：MCP 输出限制、Elicitation、工具描述 2KB 上限、工具搜索、资源、提示斜杠命令 —— 仍有效
- §8 Subagent-Scoped MCP、§9 托管 MCP 配置、§10 从 Claude Desktop 导入、§11 用作 MCP 服务器 —— 仍有效
- §12 故障排查其余、§13 CLI 命令速查、常见问题、最佳实践、参考资料 —— 仍有效

## 删除（DELETE）

无。未发现被废弃且需整段删除的内容。
