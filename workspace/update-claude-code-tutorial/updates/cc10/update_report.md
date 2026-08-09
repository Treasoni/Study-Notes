# 更新报告 — cc10 Claude Code Subagents 完整指南

## 基本信息

| 项 | 值 |
|----|----|
| note_id | cc10 |
| 原文件 | `C:\note\Study-Notes\AI学习\Claude Code 教程\03-进阶应用\Claude Code Subagents 完整指南.md` |
| 输出目录 | `C:\note\Study-Notes\workspace\update-claude-code-tutorial\updates\cc10\` |
| 原状态 | updated（updated 2026-07-12） |
| 新状态 | updated（updated 2026-08-10） |
| MOC | none（P5 统一处理） |

## 更新摘要

- **frontmatter**：`updated: 2026-07-12 → 2026-08-10`；`status: updated` 保持。
- **默认后台运行**：修正「后台 Subagents」`[!tip] 2026 更新` 版本号 v2.1.0+ → **v2.1.198+**，并说明无需显式 `background: true`（SB-06）。
- **并发与预算（新增小节）**：§后台 Subagents 新增「并发上限与预算控制」——默认并发 **20**（`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`）；`--max-budget-usd` 达上限自动停止后台子代理；`--forward-subagent-text` 透传子代理文本到 stream-json（SB-05/SB-06）。
- **/subtask（新增小节）**：§使用 Subagents 新增「`/subtask`：会话内子代理」——旧 in-session 子代理改为 `/subtask`（v2.1.212+），`/tasks` 保留已完成后台代理（SB-06/SB-08）。
- **嵌套规则**：统一把「最多 5 层 / 默认不可以」改为「默认最多 **3 层**（v2.1.219 恢复；v2.1.217 曾默认禁用），`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用嵌套」——覆盖 §关键行为、§FAQ、并新增「嵌套深度限制」小节；补 v2.1.224 移除每会话 200 spawn 上限说明（SB-06）。
- **Worktree 安全（新增小节）**：§Worktree 隔离新增「安全限制」——worktree 隔离子代理不能对主 checkout 执行破坏性 git 命令（含 `git -C`/`--git-dir`/`GIT_DIR` 重定向，v2.1.216+）；`EnterWorktree` 进入 `.claude/worktrees/` 之外需确认（v2.1.222+）（SB-07）。
- **去陈旧数值**：架构图子代理标注「20K tok」改为「独立窗口」；设计模式模型分层 Tier 1 Opus 4.8 追加 `[!note]` 提示默认 Opus 已更新（v2.1.219）。
- **大白话**：核心概念新增「专科医生」比喻；后台/并发预算、嵌套深度、`/subtask` 各补 `[!tip] 大白话`。
- **更新记录**：文末追加 2026-08-10 条目。
- 未重写未过时段落（快速开始、文件位置、配置格式、内置 Subagents、可恢复 Agents、链式、持久化记忆、Agent Teams、何时使用、最佳实践、示例 Subagents、实战练习等均保留原文）。

## 引用来源

| 来源 | 用途 |
|------|------|
| SB-05（CLI 新标志与环境变量） | `--forward-subagent-text`、`--max-budget-usd`、`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`、`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` |
| SB-06（Subagents 默认后台 + 并发/嵌套规则） | 默认后台 v2.1.198+、并发 20、v2.1.217 禁用嵌套→v2.1.219 恢复深度 3、v2.1.224 移除 200 spawn 上限、`/subtask`、`/tasks` |
| SB-07（子代理文件隔离与安全） | Worktree 破坏性 git 命令隔离（v2.1.216）、`EnterWorktree` 确认（v2.1.222） |
| SB-08（/fork、/subtask、/resume） | `/subtask` 取代旧 in-session 子代理佐证 |
| SB-02（默认 Opus 模型） | 设计模式模型分层 `[!note]` 提示（仅作提示，非正文表格改动） |

> 以 code.claude.com 现行文档为准（来源库约定：若与本文冲突，以官方文档为准）。

## 未处理风险

1. **版本号精确性**：并发默认 20、嵌套深度 3 等数值来自来源库（官方 changelog 转述），未逐一抓取官方页面核对原文；写回前建议对照 code.claude.com 现行 Subagents 文档确认。
2. **`/tasks` 与 `/subtask` 交互细节**：`/tasks` 的精确行为（保留范围、可否恢复）来源库仅一句描述，文中按 SB-06/SB-08 表述，未展开。
3. **架构图「独立窗口」为去数值化处理**：Subagent 上下文的具体容量随模型变化（1M 上下文模型下可能显著大于原 20K tok），文中未给出新数值以免过时；如需具体容量建议查官方文档。
4. **设计模式模型分层未改表格本体**：Tier 1 仍写 Opus 4.8，仅加 `[!note]` 提示。SB-02 适用笔记未含 cc10，保守处理；如需同步 Opus 5 可另行更新。
5. **`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`**：来源库未确认该变量是否仍有效，按原文保留，未做删除。
6. **未大范围联网**：本次仅用共享来源库（SB-05/06/07/08）核对，未逐一抓取官方 changelog 原始条目。

## 结论

- 发现过时点：**11 处**（6 处过时修正：frontmatter 日期、后台版本号、嵌套规则×3 处、架构图 20K tok、模型分层提示；5 处新增缺失项：并发上限、预算/透传、`/subtask`、200 spawn 上限移除、Worktree 安全限制）。
- **是否需要 needs-review：是**。本笔记为「核心大篇」（44KB），新增 4 个小节与 6 类行为变更，且版本号数值来自转述来源库；建议用户审阅 `updated_note.md` 并对照官方 Subagents 文档后，再写回原 vault 文件。
