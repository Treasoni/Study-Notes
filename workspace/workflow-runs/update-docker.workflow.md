---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: update-docker
task: Docker 笔记批量更新
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: Docker 笔记批量更新
project_slug: update-docker
created_at: "2026-08-03"
last_updated: "2026-08-04"
current_phase: done
current_status: complete
mode: standard
confirmed_phases: "P0,P1,P2,P3,P4,P5"
skippable_phases: "P3"
mode_dependent_skips: ""
allowed_modes: ""
mode_change_phase: ""
blocked_reason: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：Docker 笔记批量更新
> 运行标识：update-docker
> 项目标识：update-docker
> 创建时间：2026-08-03
> 当前阶段：完成
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

> [P4] ✅ 已完成

---

## 阶段 5：汇总与 MOC 同步
- [ ] 已汇总更新、跳过、失败和需复核数量
- [ ] 已汇总每篇输出路径和风险
- [ ] 如提供 MOC，已同步索引且未复制正文
- [ ] 批量更新报告已保存：`./04_batch_update_report.md`

> [P5] ✅ 已完成

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P5 | 用户指示直接完成：8篇更新+报告+MOC副本完成，原文件未发布待确认 | 2026-08-04 00:05 |
| P4 | 用户指示直接完成（不再逐批询问）：8篇全部更新完成，无 needs-review | 2026-08-04 00:04 |
| P3 | 用户确认来源库可信 | 2026-08-03 23:55 |
| P2 | 用户确认批量计划与Batch1，需共享资料 | 2026-08-03 23:53 |
| P1 | 用户确认清单：6篇正文更新+2篇补frontmatter+4篇skip | 2026-08-03 23:51 |
| P0 | 用户确认意图：docker/ 目录，全面刷新到最新，project-output-only，批大小3 | 2026-08-03 23:49 |
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
| 2026-08-03 | 1 | 3 | 3 | 0 | workspace/update-docker/updates/ |
| 2026-08-04 | 2 | 3 | 3 | 0 | workspace/update-docker/updates/ |
| 2026-08-04 | 3 | 2 | 2 | 0 | workspace/update-docker/updates/ |

---

## 最终产出

- **源路径**：docker/
- **更新目标**：全面刷新 Docker / Docker Desktop / WSL2 到 2026 最新版本与最佳实践
- **处理文件数**：12
- **更新文件数**：8
- **跳过文件数**：4
- **需复核文件数**：0
- **输出模式**：project-output-only
- **文件路径**：workspace/update-docker/updates/{note_id}/updated_note.md
- **Obsidian Vault**：（未发布，待用户确认）
- **MOC 路径**：docker/Docker MOC.md（更新副本在 updates/docker-moc/，原文件未动）
