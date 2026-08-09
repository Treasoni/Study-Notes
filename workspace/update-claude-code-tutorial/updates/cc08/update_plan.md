# 更新计划 — cc08 Claude Code Hooks 使用指南

## 过时点清单

| 序号 | 位置 | 现状 | 过时原因 | 处理方式 |
|------|------|------|---------|---------|
| U1 | frontmatter `updated` | 2026-07-12 | 需同步 2026-08 现状 | `updated: 2026-08-10`（`status: updated` 保持） |
| U2 | 事件列表标题计数 | "24+ 个 Hook 事件（v2.1.83+ 新增文件系统事件）" | SB-16：新增 `DirectoryAdded` 事件、`Notification` 子事件 | 更新计数与版本注记 |
| U3 | 事件列表「用户交互」Notification 行 | 仅「发送通知时」 | SB-16：Notification 新增 `agent_needs_input` / `agent_completed` 子类型 | 补充子类型说明 |
| U4 | 事件列表「配置与环境」小节 | 无 `DirectoryAdded` | SB-16：`/add-dir` 或 SDK `register_repo_root` 后触发 | 新增一行事件 |
| U5 | Matcher 模式语法 | 未提及 `if:` 条件与连字符标识符行为 | SB-16：单段 `dir/**` 的 `if:` 条件只匹配 `<cwd>/dir`；连字符标识符精确匹配 | 新增行为更新警示块 |
| U6 | SessionStart 小节 | 未提及 headless 修复 | SB-16：headless 会话中事件流修复 | 新增修复说明 |
| U7 | 安全注意事项 | 未含插件 shell 形式 hook 注入防护 | SB-16, SB-19：shell hooks / monitors / `headersHelper` 拒绝 `${user_config.*}` | 新增警示小节 |
| U8 | 核心概念 | 无 `[!tip] 大白话` | 用户偏好 | 概述与事件列表各加一条大白话 |
| U9 | 文末 | 无本次变更留痕 | 流程要求 | 追加「更新记录」2026-08-10 条目 |

## 新增/更新内容与来源核对

| 变更 | 来源 | 说明 |
|------|------|------|
| `Notification` 子类型 `agent_needs_input` / `agent_completed` | SB-16 | 事件行补充子类型，触发时「发送通知时」 |
| `DirectoryAdded` 事件 | SB-16 | `/add-dir` 或 SDK `register_repo_root` 后触发，不可阻止，用于新目录初始化 |
| matcher `if:` 行为 | SB-16 | 单段 `dir/**` 只匹配 `<cwd>/dir`；其他路径需显式完整相对路径 |
| 连字符标识符精确匹配 | SB-16 | `my-hook` 之类不再通配/正则展开 |
| SessionStart headless 修复 | SB-16 | headless / unattended 会话事件不再丢失 |
| 插件 `${user_config.*}` 拒绝 | SB-16, SB-19 | shell 形式 hooks / monitors / `headersHelper` 注入防护，替代配置传递方式 |

## 执行步骤

1. 更新 frontmatter：`updated: 2026-08-10`（`status: updated` 保持）。
2. 概述后新增 `[!tip] 大白话`。
3. 事件列表：更新标题计数与版本注记；Notification 行补子类型；配置与环境小节新增 `DirectoryAdded` 行；列表开头新增 `[!tip] 大白话`。
4. Matcher 模式语法后新增 `[!warning]` 行为更新块（`if:` 单段 `dir/**` + 连字符精确匹配）。
5. SessionStart 小节新增 headless 修复 `[!note]`。
6. 安全注意事项新增「插件 Hook 注入防护」`[!warning]`（`${user_config.*}` 被拒绝）。
7. 追加「更新记录」2026-08-10 条目。
8. 产出 `updated_note.md` 供用户审阅后写回原文件。

## 校验项

- [ ] YAML frontmatter 特殊值（`[]`/`:`）加引号；本次 tags 为纯词，无需引号
- [ ] 不重写未过时段落，局部 patch
- [ ] 列表内不嵌套表格
- [ ] 未修改原 vault 文件，全部产物写入 updates/cc08/
- [ ] PreToolUse / PostToolUse / Stop 事件章节已核对，无过时描述
