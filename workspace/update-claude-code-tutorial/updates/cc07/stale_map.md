# cc07 过时点地图（Stale Map）

- **note_id**: cc07
- **笔记**: Claude Code Checkpoints 使用指南
- **源文件**: `AI学习/Claude Code 教程/03-进阶应用/Claude Code Checkpoints 使用指南.md`
- **核对来源**: SB-22（官方 changelog）+ https://code.claude.com/docs/en/checkpointing（2026-08-10 核验）+ https://code.claude.com/docs/en/commands
- **结论**: 过时点 19 处（更新 10 / 新增 9）。核心过时集中在「Rewind 菜单选项」「/clear 恢复」「符号链接/硬链接防逃逸」「/checkpoint 别名」「配置项」。

---

## 一、frontmatter

| 字段 | 现状 | 问题 | 动作 | 依据 |
|------|------|------|------|------|
| `updated` | `2026-07-12` | 落后于 2026-08 现状 | **更新** → `2026-08-10` | 任务要求 |
| `status` | `updated` | 正确 | 保留 | — |

## 二、正文各节

| 位置 | 现状 | 问题/过时点 | 动作 | 依据 |
|------|------|-------------|------|------|
| §1 核心概念（类比表下方） | 已有「概述」通俗比喻 | 任务要求核心概念加「大白话」 | **新增** `[!tip] 大白话`（存档点/时光机） | update_goal #4 |
| §1「Checkpoint 包含什么？」框图 | `📝 ���息历史` | 乱码字符 | **更新** → `📝 信息历史` | 排版修复 |
| §1「与 Git 的对比」表 | 范围/持久性/粒度/速度/分享 | 仍准确 | 保留 | docs |
| §2 自动机制「特点」 | 跨会话持久：重启后仍可访问 | 正确但可更贴合官方表述 | **更新**（微调措辞：Checkpoint 与会话一起保存） | docs |
| §2 自动清理 | 30 天后自动删除（可配置） | 正确 | **更新**（补充 `cleanupPeriodDays` 与 100 快照细节） | docs |
| §2 追踪的文件操作表 + Bash warning | Write/Edit/NotebookEdit 追踪；Bash rm/mv/cp 不追踪 | 正确 | 保留 | docs |
| §2（表后） | 无符号链接/硬链接说明 | **缺新限制** | **新增** `[!warning]`：`/rewind` 不再经符号链接/硬链接恢复或删除文件，跳过并提示（v2.1.216+ 防逃逸） | SB-22 / docs；update_goal #2 |
| §2（表后） | 无子代理说明 | **缺新限制** | **新增** `[!warning]`：子代理编辑不一定能回滚（前台 fork 技能除外） | docs |
| §3 快捷键 | `Esc + Esc`（连按两次 Esc） | 未说明「输入框为空时」前提 | **更新**：输入框有文字时连按 Esc 会清空输入（↑ 可召回），不打开菜单 | docs |
| §3 斜杠命令 | `/rewind` 主命令 + `/checkpoint` 别名 | `/checkpoint` **不在**官方命令列表 | **更新**：移除 `/checkpoint`，补充 `/resume` | commands 页 |
| §3 Rewind 选项图 | 5 个选项 | **缺 Summarize up to here** | **更新**：5 → 6 个选项 | docs |
| §3 Rewind 选项图后 | 无场景说明 | **缺条件说明** | **新增** note：代码恢复选项仅当 checkpoint 之后有被追踪文件修改时出现；Restore conversation / Summarize from here 后原 prompt 恢复到输入框 | docs |
| §3（新） | 无 `/clear` 恢复说明 | **缺新能力** | **新增** 小节「恢复 /clear 之前的对话」+ `[!tip] 大白话`（v2.1.191+） | SB-22 / docs；update_goal #1 |
| §3 选项对比表 | 4 行 | **缺 Summarize up to here**，Summarize 未区分方向 | **更新**：拆成 Summarize from here / up to here 两行 | docs |
| §3 Summarize 详解 | 仅 from-here 方向 | **缺 up-to-here、引导摘要、与 /compact 关系** | **新增**：Summarize up to here 说明 + add context 引导 + /compact 对比 | docs |
| §6 配置选项 | `autoCheckpoint: true` | `autoCheckpoint` 未在现行 docs 出现 | **更新**：移除，改用官方 `cleanupPeriodDays`；说明默认开启、100 快照 | docs |
| §8 常见问题 | 4 条 Q&A | **缺 /clear 恢复、symlink/hardlink、subagent 三问** | **新增** 3 条 Q&A | SB-22 / docs |
| §9 故障排除表 | 3 行 | **缺 skipped N files、subagent 回滚** | **新增** 2 行 | docs |
| 文末 | 无更新记录 | 任务要求追加 | **新增** `## 更新记录` | 任务要求 |

## 三、保留不动

- §1 类比表（游戏存档 / Git Commit / 时光机）
- §2 自动创建时间线、追踪/不追踪表、Bash warning
- §4 典型使用场景（4 个场景）
- §5 工作流模式（分支探索 / 安全重构 / 上下文管理）
- §7 最佳实践（推荐做法 / 避免做法）
- §8 既有 4 条 Q&A
- 「个人笔记」「相关文档」「参考资料」

## 四、删除项（并入上方更新）

| 项 | 原因 |
|----|------|
| `/checkpoint` 别名 | 官方命令列表未收录，作为 `/rewind` 别名依据不足 |
| `autoCheckpoint` 配置项 | 现行文档未提及该设置名 |
