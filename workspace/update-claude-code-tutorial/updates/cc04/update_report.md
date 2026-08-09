# cc04 — 更新报告

## 更新摘要
- 过时点：12 处（4 处更新 + 8 处新增/补充）。
- 全部为局部 patch，未重写未过时段落，保留原结构和写作风格。
- 新增会话相关命令 `/fork` `/rewind` `/subtask` `/tasks`；`/status` 显示会话类型；Subagents 默认后台运行；AskUserQuestion 行为变化；transcript 写入失败与登录过期警告；更新记录。
- 核心概念补充了 `[!tip] 大白话`（Subagents、`/fork` `/rewind`）。
- 未嵌套表格在列表内；frontmatter 无含 `[]`/`:` 的值，无需加引号。

## 引用来源
- SB-02（Opus 5 成为默认 Opus 模型）→ CLI 模型示例更新。
- SB-06（Subagents 默认后台运行、`/subtask`、`/tasks`、并发 20）→ 新增小节与命令。
- SB-08（`/fork`、`/subtask`、agent 视图 `/resume`、`/rewind`）→ 新增命令与恢复小节。
- SB-21（会话管理行为变化：AskUserQuestion、transcript、`/status` 会话类型、登录过期警告）→ 更新与新增。
- SB-22（`/rewind` 恢复到 `/clear` 之前；不再符号/硬链接恢复或删除文件）→ 更新。
- 官方 changelog：https://code.claude.com/docs/en/changelog

## 未处理风险
1. **`.claude.local/settings.json` 本地配置路径**：当前官方规范为 `.claude/settings.local.json`，但 source bank 无对应条目，未改动；建议后续单独核对（涉及配置文件位置、记忆文件结构、FAQ 三处）。
2. **`/doctor` 与 `/checkup` 关系**：本笔记写「/doctor 已重命名为 /checkup」，与 SB-10（/doctor 为主、/checkup 为别名）不符；SB-10 适用笔记为 cc02/cc13，未越界修改，建议由对应笔记处理。
3. **配置优先级 mermaid 图**：保留了原图结构，仅补充文字 callout，未重构图表，避免改变原文叙事。
4. **`claude agents` 命令形式**：未验证应为 `claude --agents`，无来源支持，保持原样。

## 结论
- **是否需要 needs-review：是**。核心更新有 SB-06/08/21/22 支撑，但风险 1（本地配置路径）与风险 2（/doctor 命名关系）无法从 source bank 完全确认，建议人工或对应笔记复核后再发布到 vault。
