# 更新报告 — cc08 Claude Code Hooks 使用指南

## 基本信息

| 项 | 值 |
|----|----|
| note_id | cc08 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\03-进阶应用\Claude Code Hooks 使用指南.md` |
| 输出目录 | `C:\note\Study-Notes\workspace\update-claude-code-tutorial\updates\cc08\` |
| 原状态 | updated（updated 2026-07-12） |
| 新状态 | updated（updated 2026-08-10） |
| MOC | none（P5 统一处理） |

## 更新摘要

- **`Notification` 事件补全**：`用户交互` 事件表新增子类型说明 `agent_needs_input` / `agent_completed`（SB-16）。
- **新增 `DirectoryAdded` 事件**：`配置与环境` 事件表新增一行，注明 `/add-dir` 或 SDK `register_repo_root` 后触发（SB-16）。
- **matcher 行为更新**：Matcher 语法后新增 `[!warning]` 说明 v2.1.198+ 行为——单段 `dir/**` 的 `if:` 条件只匹配 `<cwd>/dir`；带连字符的 hook 标识符精确匹配（SB-16）。
- **SessionStart headless 修复**：补充 v2.1.198+ 无头 / unattended 会话事件流修复说明（SB-16）。
- **插件注入防护**：安全注意事项新增「插件 Hook 注入防护」——shell 形式 hooks / monitors / `headersHelper` 拒绝 `${user_config.*}`（SB-16, SB-19）。
- **`[!tip] 大白话`**：概述与事件列表开头各新增一条通俗解释（用户偏好）。
- **frontmatter**：`updated: 2026-07-12 → 2026-08-10`，`status: updated` 保持。
- **更新记录**：追加 2026-08-10 条目。
- 未重写未过时段落；PreToolUse / PostToolUse / Stop 等关键事件章节已核对，描述在 2026-08 仍准确，未改动。

## 引用来源

| 来源 | 用途 |
|------|------|
| SB-16（Hooks 更新） | `Notification` 子类型、`DirectoryAdded`、matcher `if:` / 连字符精确匹配、SessionStart headless 修复、插件 `${user_config.*}` 拒绝 |
| SB-19（插件系统安全变化） | `headersHelper:${user_config.*}` 被拒绝的注入修复佐证 |

> 以 code.claude.com 现行文档为准（来源库约定：若与本文冲突，以官方文档为准）。

## 未处理风险

1. **版本号未逐条归属**：SB-16 跨 v2.1.198 / v2.1.214 / v2.1.219 多个版本，本文对 `Notification` 子类型、`DirectoryAdded`、`if:` 行为、headless 修复统一标为 v2.1.198+，未逐条核对具体版本号；如写回前需要精确版本，请对照官方 changelog。
2. **matcher `if:` 语义细节**：单段 `dir/**` 只匹配 `<cwd>/dir` 的行为为来源库摘要，未抓取官方 matcher 文档原文；"显式写完整相对路径"为建议性表述。
3. **插件注入修复场景有限**：`${user_config.*}` 拒绝针对插件 shell 形式 hooks / monitors / `headersHelper`；`pluginConfigs` 不再从项目 settings 读取、archive 安装来源等其余插件变更（SB-19）属 cc11 插件篇适用范围，本笔记未纳入。
4. **未大范围联网**：本次仅用共享来源库核对，未逐一抓取官方 hooks 页面。

## 结论

- 发现过时点：7 处（frontmatter 日期、事件计数、Notification 行、缺 DirectoryAdded、matcher 行为、SessionStart headless、插件注入防护）+ 2 处 `[!tip] 大白话` 增强 + 更新记录。
- **是否需要 needs-review：否**。本次均为来源库明确描述的增量更新与行为补充，无需要推断的精确结构；建议用户在写回前快速审阅 `updated_note.md`。
