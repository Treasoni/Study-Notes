# 过时映射（Stale Map）— cc08 Claude Code Hooks 使用指南

> 更新目标：同步到 2026-08 现状。来源库适用条目：SB-16、SB-19。

## 保留（Keep）

| 位置 | 理由 |
|------|------|
| 快速开始（最简配置示例 + `/hooks` 验证） | 现行，未过时 |
| 配置位置与优先级表（全局/项目/本地/托管/插件/Skill-Agent） | 现行，未过时 |
| 基本结构 JSON 骨架 | 现行 |
| Matcher 模式语法表与常用示例 | 主体现行，仅补充行为更新说明 |
| Hook 类型（Command / HTTP / Prompt / Agent / MCP Tool）5 种 | 现行，未过时 |
| 事件列表大部分事件行（SessionStart/End、InstructionsLoaded、UserPromptSubmit、PreToolUse/PostToolUse/PostToolUseFailure、PermissionRequest、SubagentStart/Stop、Stop/StopFailure、TaskCompleted/Created、TeammateIdle、ConfigChange、CwdChanged、FileChanged、PreCompact/PostCompact、WorktreeCreate/Remove、Elicitation/Result） | 现行，未过时 |
| 关键事件详解（PreToolUse / PostToolUse / Stop / SessionStart 主体） | 已核对，2026-08 描述仍准确，无需改动 |
| 输入输出格式（stdin JSON、退出码表、修改工具输入） | 现行，未过时 |
| 组件级 Hooks（frontmatter 附加，支持事件、Stop→SubagentStop 自动转换） | 现行，未过时 |
| 实战示例 1–9、调试与排错、最佳实践 | 现行，未过时 |
| 安全注意事项主体（免责声明、最佳实践对照、工作区信任、托管设置） | 现行，未过时 |
| 环境变量参考表、常见问题 | 现行，未过时 |
| 个人笔记、相关文档、参考资料 | 保留 |
| 原结构与写作风格、Callout 用法 | 保留 |

## 更新（Update）

| 位置 | 现状 | 改为 |
|------|------|------|
| frontmatter `updated` | 2026-07-12 | 2026-08-10 |
| 事件列表标题计数 | "24+ 个 Hook 事件（v2.1.83+ 新增文件系统事件）" | "25+ 个 Hook 事件"并注明 v2.1.198+ 新增 `DirectoryAdded` 与 `Notification` 子事件 |
| 事件列表「用户交互」Notification 行 | 仅「发送通知时」 | 补充子类型 `agent_needs_input` / `agent_completed` |
| Matcher 模式语法 | 未提及 `if:` 条件与连字符标识符行为 | 补充 v2.1.198+ 行为更新（单段 `dir/**` 只匹配 `<cwd>/dir`；连字符标识符精确匹配） |
| SessionStart 小节 | 未提及 headless 修复 | 补充 headless / unattended 会话事件流修复说明 |
| 安全注意事项 | 未含插件 shell 形式 hook 注入防护 | 补充插件 hooks / monitors / `headersHelper` 拒绝 `${user_config.*}` 说明 |

## 删除（Delete）

无。未发现正文中使用但已被官方废弃的 hook 事件或类型（PreToolUse/PostToolUse/Stop 等语义在 2026-08 仍现行）。

## 新增（Add）

| 位置 | 新增内容 | 来源 |
|------|---------|------|
| 事件列表「配置与环境」小节 | `DirectoryAdded` 事件（`/add-dir` 或 SDK `register_repo_root` 后触发） | SB-16 |
| 概述、事件列表开头 | `[!tip] 大白话` 通俗解释（Hook 是什么、事件是什么） | 用户偏好 |
| 安全注意事项 | 插件 `${user_config.*}` 拒绝的注入防护提醒 | SB-16, SB-19 |
| 文末 | 「更新记录」2026-08-10 条目 | 流程要求 |
