# 批处理日志

> 批次规则：每批 3 篇，先输出 `updates/{note_id}/`，用户确认后写回原文件（patch-in-place，git 可回滚）。

| 时间 | 批次 | 笔记 | 动作 | 输出 | 风险 |
| --- | --- | --- | --- | --- | --- |
| 2026-08-10 | 1 | cc01 如何使用Claude code | update + 写回 | updates/cc01/updated_note.md → 原文件 | stable 版本号待核；促销价 8/31 时效 |
| 2026-08-10 | 1 | cc06 settings.json 配置详解 | update + 写回 | updates/cc06/updated_note.md → 原文件 | 3 个新配置键 schema 为示意值 |
| 2026-08-10 | 1 | cc12 Claude Code 高级功能 | update + 写回 | updates/cc12/updated_note.md → 原文件 | credentialMasking.mode 路径为推断 |
| 2026-08-10 | 2 | cc02 Claude Code 常用功能 | update + 写回 | updates/cc02/updated_note.md → 原文件 | 快捷键速查无来源未核 |
| 2026-08-10 | 2 | cc03 Claude Code CLI 完整参考 | update + 写回 | updates/cc03/updated_note.md → 原文件 | 模型表 Opus 4.8 待后续统一核对 |
| 2026-08-10 | 2 | cc04 Claude Code 会话管理 | update + 写回（修 /doctor 别名方向） | updates/cc04/updated_note.md → 原文件 | .claude.local/settings.json 路径规范待核 |
| 2026-08-10 | 3 | cc05 Claude Code 模型与推理设置 | update + 写回 | updates/cc05/updated_note.md → 原文件 | opusplan 别名 200K 待核；促销价时效 |
| 2026-08-10 | 3 | cc07 Claude Code Checkpoints 使用指南 | update + 写回 | updates/cc07/updated_note.md → 原文件 | /checkpoint 与 autoCheckpoint 移除为推断 |
| 2026-08-10 | 3 | cc08 Claude Code Hooks 使用指南 | update + 写回 | updates/cc08/updated_note.md → 原文件 | 子类型版本归属为 v2.1.198+ 粗略 |
| 2026-08-10 | 4 | cc09 Claude Code Memory 完整指南 | update + 写回 | updates/cc09/updated_note.md → 原文件 | 移除 DISABLE_AUTO_MEMORY=0 语义待核；修 3 处乱码 |
| 2026-08-10 | 4 | cc10 Claude Code Subagents 完整指南 | update + 写回 | updates/cc10/updated_note.md → 原文件 | 版本号/数值建议对照官方文档 |
| 2026-08-10 | 4 | cc11 Claude Code 插件系统使用指南 | update + 写回 | updates/cc11/updated_note.md → 原文件 | breaking 安全变更版本归属待核 |
| 2026-08-10 | 5 | cc13 Claude Code Slash Commands 完整参考 | update + 写回 | updates/cc13/updated_note.md → 原文件 | /branch 与 /fork 关系待核 |
| 2026-08-10 | 5 | cc14 Claude MCP 使用指南 | update + 写回 | updates/cc14/updated_note.md → 原文件 | 版本号精确归属待核 |
| 2026-08-10 | 5 | cc15 如何编写Skills | update + 写回 | updates/cc15/updated_note.md → 原文件 | 叠加数量(5 vs 6)措辞按官方 docs |
| 2026-08-10 | 6 | cc16 CLAUDE.md 使用指南 | update + 写回 | updates/cc16/updated_note.md → 原文件 | 工作区信任表述待对照 docs |
| 2026-08-10 | 6 | cc17 Claude Code 定时任务自动化指南 | update + 写回 | updates/cc17/updated_note.md → 原文件 | /loop cron 兼容性待核；launchctl 未改 |
| 2026-08-10 | 6 | cc18 Claude Code Dynamic Workflows 使用指南 | update + 写回 | updates/cc18/updated_note.md → 原文件 | OTel/SendMessage 为 spec 转述；无「6种模式」章节 |
| 2026-08-10 | 7 | cc19 LLM-Prompt-Caching-提示缓存 | update + 写回（draft→updated） | updates/cc19/updated_note.md → 原文件 | 促销定价 8/31 时效；缓存参数沿用原文 |
