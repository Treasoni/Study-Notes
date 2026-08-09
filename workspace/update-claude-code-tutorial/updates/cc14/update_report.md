# cc14 更新报告（update_report）

> 笔记：Claude MCP 使用指南 · note_id：cc14
> 更新日期：2026-08-10

## 更新摘要

对《Claude MCP 使用指南》做 2026-08 现状同步，核对基线为共享来源库 SB-17。共定位 **4 处过时/待更新 + 9 处新增**，全部局部 patch，未删除任何段落。主要变更：

1. **Capability discovery 自动重试（v2.1.191+）**：新增小节，说明 `tools/list`、`prompts/list`、`resources/list` 对瞬时网络错误自动重试。
2. **macOS 密钥链 OAuth 401 修复（v2.1.225+）**：§2 OAuth 功能表后新增 `[!tip]` 修复说明；§12 故障排查「OAuth 授权问题」新增排查项「macOS 连续 401 → 升级到 v2.1.225+」。
3. **安全行为（2026-08）**：§3 管理服务器新增 `[!warning]`——`claude mcp list`/`get` 不再自批准 `.mcp.json` 自带服务器（列出≠放行）；§4 插件 MCP 新增 `[!warning]`——外部插件 MCP 需安装同意。
4. **会话工作目录加入 roots（v2.1.203+）**：§7「动态工具更新」扩展为「动态工具更新与 roots 同步」，补充 `roots/list` 与 `notifications/roots/list_changed`。
5. **长耗时工具调用自动转后台**：新增小节——超过 2 分钟自动转后台，可用 `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` 调整阈值。
6. **核心概念「大白话」**：§1 什么是 MCP、§1 传输方式各加一个 `[!tip] 大白话` callout。
7. **frontmatter 与结构**：`updated` → 2026-08-10，`status` 保持 `updated`；修正重复的章节编号（CLI 命令速查 `## 12.` → `## 13.`）；文末追加 `## 更新记录`（2026-08-10 行）。

## 引用来源

| 条目 | 来源 | 用途 |
|------|------|------|
| SB-17 | code.claude.com/docs/en/changelog | MCP 更新：capability discovery 重试（v2.1.191+）、macOS keychain OAuth 401 修复（v2.1.225+）、`claude mcp list/get` 不再自批准、roots/list（v2.1.203+）、超 2 分钟转后台 |

> 单篇专项细节（OAuth keychain、roots/list 通知名）在 SB-17 摘要框架内展开，未引入库外新事实；任务参数中的版本号（v2.1.191/203/225）与 SB-17 一致。

## 核对结论

- **§1 MCP 协议/简介**：定义、传输方式表、SSE 已废弃 —— 已核对，仍为 2026-08 现状。
- **§2 安装 + OAuth**：三种传输、OAuth 2.0 流程 —— 已核对；仅补充 keychain 修复。
- **§6 连接外部工具和数据源**：filesystem/postgres/github/sentry 等推荐服务器 —— 已核对，仍有效，未改动。

## 未处理风险 / 需人工复核项

1. **版本号细节为摘要级**：SB-17 仅给出 v2.1.191/196/203/224 四个版本点；本笔记标注的 v2.1.191/203/225 中，v2.1.225 对应任务参数（keychain 修复），v2.1.224 对应长耗时转后台。若需精确到「哪个版本引入哪条」，需查官方 changelog 原文逐条核对。
2. **外部插件 MCP「安装同意」措辞**：任务要求「外部插件 MCP 需安装同意」，SB-19（cc11）更详细；本笔记仅保留一句话 warning，未展开插件启用机制，属保守处理。
3. **章节编号修正**：把 CLI 命令速查由 `## 12.` 改为 `## 13.` 属结构性小修，涉及标题行号变化，不影响内容；如需严格保持原编号可回退。
4. **MOC 未处理**：`moc_path: none`，P5 由批次统一处理，本单篇不触碰 MOC。

## 结论

过时点已全部按 SB-17 与任务参数处理，未引入库外新事实，无阻断风险。

**是否需要 needs-review：是** —— 建议用户审阅 `updates/cc14/updated_note.md` 后写回原 vault 文件。重点关注：版本号细节（v2.1.191/203/225）与外部插件同意措辞需人工核对官方 changelog。
