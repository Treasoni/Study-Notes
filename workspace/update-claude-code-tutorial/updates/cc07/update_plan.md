# cc07 更新计划（Update Plan）

- **note_id**: cc07
- **模式**: 局部 patch（不重写未过时段落），保留原结构与写作风格
- **目标**: 同步 Checkpoints / Rewind 到 2026-08 现状（官方 changelog v2.1.191 / v2.1.216）
- **输出**: 全部写入 `workspace/update-claude-code-tutorial/updates/cc07/`，不修改原 vault 文件

## 变更清单（按应用顺序）

| # | 位置 | 动作 | 内容要点 |
|---|------|------|----------|
| 1 | frontmatter | 改 | `updated: 2026-07-12` → `2026-08-10`；`status: updated` 保持 |
| 2 | §1 核心概念 | 加 | `[!tip] 大白话`：存档点/时光机比喻 |
| 3 | §1 框图 | 改 | 修复乱码「���息历史」→「信息历史」 |
| 4 | §2 自动机制 | 改 | 「跨会话持久」措辞微调；「自动清理」补充 `cleanupPeriodDays` 与 100 快照 |
| 5 | §2（表后） | 加 | `[!warning]` 符号链接/硬链接不回滚（跳过并提示，v2.1.216+ 防逃逸） |
| 6 | §2（表后） | 加 | `[!warning]` 子代理编辑不一定能回滚（前台 fork 技能除外） |
| 7 | §3 快捷键 | 改 | 补充「输入框为空时」前提；有文字时连按 Esc 清空输入 |
| 8 | §3 斜杠命令 | 改 | 移除 `/checkpoint`，补充 `/resume` |
| 9 | §3 Rewind 选项图 | 改 | 5 → 6 个选项（新增 Summarize up to here） |
| 10 | §3 选项图后 | 加 | note：代码恢复选项条件出现；原 prompt 恢复到输入框 |
| 11 | §3 | 加 | 新小节「恢复 /clear 之前的对话」+ `[!tip] 大白话`（v2.1.191+） |
| 12 | §3 选项对比表 | 改 | Summarize 拆为 from here / up to here 两行 |
| 13 | §3 Summarize 详解 | 加 | up-to-here 说明、add context 引导、与 `/compact` / `/branch` 关系 |
| 14 | §6 配置选项 | 改 | 移除未验证 `autoCheckpoint`，改 `cleanupPeriodDays` + 默认开启/100 快照说明 |
| 15 | §8 常见问题 | 加 | 3 条 Q&A：/clear 恢复、symlink/hardlink、subagent |
| 16 | §9 故障排除 | 加 | 2 行：skipped N files、subagent 回滚 |
| 17 | 文末 | 加 | 追加 `## 更新记录` |

## 边界与取舍

- **不重写**：§4 场景、§5 工作流模式、§7 最佳实践、§8 既有 4 条 Q&A、参考资料全部保留。
- **删除依据**：`/checkpoint` 与 `autoCheckpoint` 均因「未出现在现行官方文档」而移除；若用户能提供二者存在的依据，可回退。列入低风险复核项。
- **版本门槛**：`/clear` 恢复标 v2.1.191+；符号链接/硬链接跳过标 v2.1.216+（依据 SB-22 与官方 docs）。
- **输出安全**：不触碰原文件；全部产物在 `updates/cc07/`。

## 风险

1. 移除 `/checkpoint`、`autoCheckpoint` 属「现行文档未收录」推断，非「明确不存在」→ 低风险，需用户复核。
2. 版本门槛（v2.1.191 / v2.1.216）来自官方 changelog，若用户运行版本更旧，新能力不生效 → 笔记中已标注门槛。
3. MOC（P5 统一处理，moc_path=none）。
