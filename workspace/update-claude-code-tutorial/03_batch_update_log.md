# 批处理日志

> 批次规则：每批 3 篇，先输出 `updates/{note_id}/`，用户确认后写回原文件（patch-in-place，git 可回滚）。

| 时间 | 批次 | 笔记 | 动作 | 输出 | 风险 |
| --- | --- | --- | --- | --- | --- |
| 2026-08-10 | 1 | cc01 如何使用Claude code | update + 写回 | updates/cc01/updated_note.md → 原文件 | stable 版本号待核；促销价 8/31 时效 |
| 2026-08-10 | 1 | cc06 settings.json 配置详解 | update + 写回 | updates/cc06/updated_note.md → 原文件 | 3 个新配置键 schema 为示意值 |
| 2026-08-10 | 1 | cc12 Claude Code 高级功能 | update + 写回 | updates/cc12/updated_note.md → 原文件 | credentialMasking.mode 路径为推断 |
