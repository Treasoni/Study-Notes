---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "update-claude-code-tutorial"
task: "Claude Code 教程 同步到 2026-08 最新版"
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: "Claude Code 教程 同步到 2026-08 最新版"
project_slug: "update-claude-code-tutorial"
created_at: "2026-08-09"
last_updated: "2026-08-10"
current_phase: P4
current_status: in_progress
mode: standard
confirmed_phases: "P0,P1,P2,P3"
skippable_phases: "P3"
mode_dependent_skips: ""
allowed_modes: ""
mode_change_phase: ""
blocked_reason: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：Claude Code 教程 同步到 2026-08 最新版
> 运行标识：update-claude-code-tutorial
> 项目标识：update-claude-code-tutorial
> 创建时间：2026-08-09
> 当前阶段：阶段 4
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：批量更新意图确认
- [ ] source_path/source_scope/source_glob 已确认
- [ ] update_goal 已确认
- [ ] destination_mode 已确认
- [ ] batch_size 已确认
- [ ] shared_research 策略已确认
- [ ] 批量更新意图已保存：`./00_batch_update_intent.md`

> [P0] ✅ 已完成

---

## 阶段 1：更新清单
- [ ] 已扫描目标范围内的 Markdown 笔记
- [ ] 已记录 frontmatter、标题、目录、更新时间和关键词命中
- [ ] 已标记 candidate/ready/needs-review/skip
- [ ] 更新清单已保存：`./01_update_inventory.md`
- [ ] 机器清单已保存：`./update_inventory.csv`

> [P1] ✅ 已完成

---

## 阶段 2：批量更新计划
- [ ] 已按主题、版本、目录或优先级分组
- [ ] 每篇笔记已标注动作：update/flag-only/skip/needs-review
- [ ] 第一批处理列表已生成
- [ ] 覆盖风险和需用户确认项已列出
- [ ] 批量更新计划已保存：`./02_batch_update_plan.md`
- [ ] 用户已确认计划后才进入下一阶段

> [P2] ✅ 已完成

---

## 阶段 3：共享资料收集（可选）
- [ ] 已确定共享资料适用的笔记范围
- [ ] 已收集最小必要资料
- [ ] 每条资料已记录 URL、日期、适用范围和摘要
- [ ] 来源库已保存：`./shared_research/source_bank.md`

> [P3] ✅ 已完成

---

## 阶段 4：逐篇局部更新
- [ ] 已按 batch_size 分批处理
- [ ] 每篇笔记已生成 stale map
- [ ] 每篇笔记已局部更新或标记需复核
- [ ] 原文未被覆盖，除非 destination_mode 为 patch-in-place 且用户已确认
- [ ] 批处理日志已追加：`./03_batch_update_log.md`

> [P4] 🔲 进行中

---

## 阶段 5：汇总与 MOC 同步
- [ ] 已汇总更新、跳过、失败和需复核数量
- [ ] 已汇总每篇输出路径和风险
- [ ] 如提供 MOC，已同步索引且未复制正文
- [ ] 批量更新报告已保存：`./04_batch_update_report.md`

> [P5] ⬜ 未开始

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P3 | 用户确认共享资料库足够且来源可信(source_bank 23条) | 2026-08-10 00:07 |
| P2 | 用户确认批量计划:分组A/B/C、19篇update、第一批cc01/cc06/cc12 | 2026-08-10 00:01 |
| P1 | 用户确认更新清单可信(19篇ready+4篇skip) | 2026-08-10 00:00 |
| P0 | 用户已确认：source_path=AI学习/Claude Code 教程；update_goal=同步到 2026-08 最新版；destination_mode=patch-in-place(先git备份)；moc_path=Claude Code MOC.md；batch_size=3；shared_research=auto | 2026-08-09 23:58 |
| | | |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| | | | |

---

## 批处理记录

| 时间 | 批次 | 文件数 | 成功 | 需复核 | 输出位置 |
|------|------|--------|------|--------|----------|
| | | | | | |

---

## 最终产出

- **源路径**：
- **更新目标**：
- **处理文件数**：
- **更新文件数**：
- **跳过文件数**：
- **需复核文件数**：
- **输出模式**：
- **文件路径**：
- **Obsidian Vault**：
- **MOC 路径**：
