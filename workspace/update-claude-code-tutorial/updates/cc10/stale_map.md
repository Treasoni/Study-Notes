# 过时映射（Stale Map）— cc10 Claude Code Subagents 完整指南

> 更新目标：同步到 2026-08 现状。来源库适用条目：SB-05、SB-06、SB-07。

## 保留（Keep）

| 位置 | 理由 |
|------|------|
| frontmatter `title` / `tags` / `created` / `status` / `source_project` | 未过时；仅 `updated` 需推进 |
| §核心概念（是什么 / 为什么需要 / 通俗理解 / 架构图） | 概念性内容未过时；仅补充 `[!tip] 大白话` |
| §快速开始（`/agents`、直接创建文件） | 现行，未过时 |
| §文件位置与优先级（CLI / 项目 / 用户 / 插件） | 未过时 |
| §配置格式（YAML frontmatter 字段表、工具配置选项、CLI `--agents`） | 字段表现行；`background` 字段语义仍成立（默认后台后显式 `true` 为强制后台） |
| §内置 Subagents（general-purpose / Plan / Explore / Bash / statusline-setup / Guide） | 未过时 |
| §可恢复 Agents / 链式 Subagents / Subagent 持久化记忆 | 未过时 |
| §Agent Teams（对比表、启用、启动、显示模式、架构） | 未过时；实验性提示保留 |
| §何时使用 Subagents / 最佳实践 / 示例 Subagents / 与其他功能关系 | 未过时 |
| §实战练习 5 例 + 综合挑战 | 子代理类型与工具用法未过时，保留 |
| 原结构与写作风格、Callout 用法、列表/表格排版 | 保留 |

## 更新（Update）

| 位置 | 现状 | 改为 |
|------|------|------|
| frontmatter `updated` | 2026-07-12 | 2026-08-10 |
| §后台 Subagents `[!tip] 2026 更新` | 写「v2.1.0+ 默认后台」 | 改为「v2.1.198+ 默认后台运行，无需 `background: true`」 |
| §架构与上下文管理「关键行为·嵌套生成」 | 写「可嵌套最多 5 层」 | 改为「默认最多 3 层（v2.1.219 恢复；v2.1.217 曾默认禁用）；`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用嵌套」 |
| §常见问题「Q: Subagent 可以调用其他 Subagent 吗？」 | 写「默认不可以，需 `Agent(agent_name)` 显式允许」 | 改为「默认可以，最多 3 层；需禁嵌套用 env 变量；限制类型用 `Agent(agent_name)`」 |
| §架构与上下文管理 架构图 | 每个子代理标注「20K tok」 | 改为「独立窗口」（避免过时的固定上下文数值） |
| §多 Agent 设计模式·模型分层策略 | Tier 1 写 Opus 4.8 未加说明 | 追加 `[!note]` 提示「默认 Opus 模型已更新（v2.1.219），按项目可用模型调整」 |

## 删除（Delete）

无。未发现正文中仍在使用、但已被官方废弃的字段或命令。

## 新增（Add）

| 小节 | 新增内容 | 来源 |
|------|---------|------|
| §后台 Subagents → 新增「并发上限与预算控制」 | 默认并发 20（`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`）；`--max-budget-usd` 达上限停止后台子代理；`--forward-subagent-text` 透传文本到 stream-json；附 `[!tip] 大白话` | SB-05, SB-06 |
| §使用 Subagents → 新增「`/subtask`：会话内子代理」 | 旧 in-session 子代理改为 `/subtask`（v2.1.212+）；`/tasks` 保留已完成后台代理；附 `[!tip] 大白话` | SB-06, SB-08 |
| §限制可生成的 Subagents → 新增「嵌套深度限制」 | 默认嵌套深度 3；`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用嵌套；v2.1.224 移除每会话 200 spawn 上限；附 `[!note]` + `[!tip] 大白话` | SB-06 |
| §Worktree 隔离 → 新增「安全限制」 | worktree 隔离子代理不能对主 checkout 执行破坏性 git 命令（含 `git -C`/`--git-dir`/`GIT_DIR` 重定向）；`EnterWorktree` 进入 `.claude/worktrees/` 之外需确认；附 `[!warning]` | SB-07 |
| §核心概念 → 新增 `[!tip] 大白话` | 「专科医生」比喻，覆盖默认后台运行 | 完整性补全 |
| 文末 → 新增「更新记录」 | 2026-08-10 条目，记录本次 6 类变更 | 更新留痕 |
