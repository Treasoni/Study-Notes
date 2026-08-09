# 更新计划 — cc10 Claude Code Subagents 完整指南

## 过时点清单

| 序号 | 位置 | 现状 | 过时原因 | 处理方式 |
|------|------|------|---------|---------|
| U1 | frontmatter `updated` | 2026-07-12 | 需同步 2026-08 现状 | `updated: 2026-08-10` |
| U2 | §后台 Subagents `[!tip] 2026 更新` | 写「v2.1.0+ 默认后台」 | SB-06：默认后台为 v2.1.198+ | 版本号改为 v2.1.198+，并说明无需 `background: true` |
| U3 | §关键行为「嵌套生成」+ §FAQ + §限制可生成 | 写「最多 5 层」「默认不可以」 | SB-06：v2.1.217 默认禁用 → v2.1.219 恢复深度 3 | 统一改为「默认最多 3 层；`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用嵌套」 |
| U4 | §架构与上下文管理 架构图 | 子代理标「20K tok」 | 固定数值过时 | 改为「独立窗口」 |
| U5 | §设计模式·模型分层 | Tier 1 写 Opus 4.8 | 2026-08 默认 Opus 已更新（v2.1.219，SB-02） | 追加 `[!note]` 提示按当前可用模型调整 |
| U6 | 全文 | 缺默认并发上限说明 | SB-06：默认并发 20 | 新增「并发上限与预算控制」小节 |
| U7 | 全文 | 缺 `/subtask` | SB-06/SB-08：旧 in-session 子代理改 `/subtask` | 新增「`/subtask`：会话内子代理」小节 |
| U8 | 全文 | 缺 CLI 预算/透传标志 | SB-05：`--max-budget-usd`、`--forward-subagent-text` | 并入 U6 小节 |
| U9 | 全文 | 缺每会话 200 spawn 上限已移除 | SB-06：v2.1.224 移除 | 并入「嵌套深度限制」小节的 `[!note]` |
| U10 | §Worktree 隔离 | 缺安全限制 | SB-07：破坏性 git 命令隔离 | 新增「安全限制」小节 + `[!warning]` |
| U11 | 文末 | 无更新记录 | 本次变更需留痕 | 追加「更新记录」2026-08-10 条目 |

## 新增内容与来源核对

| 新增项 | 来源 | 说明 |
|--------|------|------|
| 默认并发上限 20 + `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` | SB-06 | 调整并发生成的环境变量 |
| `--max-budget-usd` 停止后台子代理 | SB-05 | CLI 预算控制，达上限停止后台子代理 |
| `--forward-subagent-text` 透传 stream-json | SB-05 | 配合 `--output-format stream-json` 消费子代理文本 |
| `/subtask`（v2.1.212+）| SB-06, SB-08 | 取代旧 in-session 子代理；`/tasks` 保留已完成后台代理 |
| 嵌套默认深度 3（v2.1.219 恢复；v2.1.217 曾禁用）| SB-06 | 覆盖原文「最多 5 层」 |
| `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1` 禁用嵌套 | SB-06 | 环境变量控制嵌套深度 |
| v2.1.224 移除每会话 200 spawn 上限 | SB-06 | 移除旧上限说明 |
| Worktree 隔离 git 破坏性命令限制（`git -C`/`--git-dir`/`GIT_DIR`）| SB-07 | v2.1.216+ 安全限制 |
| `EnterWorktree` 进入 `.claude/worktrees/` 之外需确认 | SB-07 | v2.1.222+ 行为 |

## 执行步骤

1. 更新 frontmatter：`updated: 2026-07-12 → 2026-08-10`（`status: updated` 保持）。
2. 修正 §后台 Subagents `[!tip] 2026 更新` 版本号为 v2.1.198+。
3. §后台 Subagents 新增「并发上限与预算控制」小节（并发 20 + 预算/透传标志 + `[!tip] 大白话`）。
4. §使用 Subagents 新增「`/subtask`：会话内子代理」小节。
5. §限制可生成的 Subagents 新增「嵌套深度限制」小节（深度 3 + 禁用变量 + 200 spawn 上限移除 + `[!note]`/`[!tip]`）。
6. §Worktree 隔离新增「安全限制」小节（破坏性 git 命令隔离 + `EnterWorktree` 确认 + `[!warning]`）。
7. §关键行为「嵌套生成」与 §FAQ 嵌套问答改为「默认 3 层」。
8. 架构图「20K tok」改「独立窗口」；设计模式模型分层加 `[!note]` 提示。
9. 文末追加「更新记录」2026-08-10 条目。
10. 产出 `updated_note.md` 供用户审阅后写回原文件。

## 校验项

- [ ] YAML frontmatter 特殊值（`[]`/`:`）加引号；本次 tags 为纯词，无新增含特殊字符 YAML 值
- [ ] 不重写未过时段落，全部为局部 patch
- [ ] 列表内不嵌套表格（新增内容均为列表/代码块/表格独立成段）
- [ ] 未修改原 vault 文件，全部产物写入 `updates/cc10/`
