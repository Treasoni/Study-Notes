---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "update-xiaoya-fnos-routes"
task: "小雅 fnOS 单容器部署笔记集：统一为 monlor 镜像单一路线，彻底删除官方 xiaoyaliu/alist 路线"
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: "小雅 fnOS 单容器部署笔记集：统一为 monlor 镜像单一路线，彻底删除官方 xiaoyaliu/alist 路线"
project_slug: "xiaoya-fnos-deploy"
created_at: "2026-10-06"
last_updated: "2026-10-06"
current_phase: P1
current_status: in_progress
mode: standard
blocked_reason: ""
quality_gate: pending
quality_gate_owner: ""
quality_gate_due: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：小雅 fnOS 单容器部署笔记集：统一为 monlor 镜像单一路线，彻底删除官方 xiaoyaliu/alist 路线
> 运行标识：update-xiaoya-fnos-routes
> 项目标识：xiaoya-fnos-deploy
> 创建时间：2026-10-06
> 当前阶段：阶段 1
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：批量更新意图确认
- [x] source_path/source_scope/source_glob 已确认（`workspace/xiaoya-fnos-deploy/chapters/`，glob `*.md`）
- [x] update_goal 已确认（统一 monlor 单一路线，彻底删除官方 `xiaoyaliu/alist` 路线）
- [x] destination_mode 已确认（`patch-in-place` + 全副本同步）
- [x] batch_size 已确认（3）
- [x] shared_research 策略已确认（`no`）
- [x] 批量更新意图已保存：`./00_batch_update_intent.md`

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：更新清单
- [x] 已扫描目标范围内的 Markdown 笔记（`chapters/` 7 章 + 入口页 1 个；同时核对 `output/` 与 vault 三副本）
- [x] 已记录 frontmatter、标题、目录、更新时间和关键词命中（8 类关键词逐篇计数）
- [x] 已标记 candidate/ready/needs-review/skip（本清单用 update/skip：update 5 篇、skip 3 篇）
- [x] 更新清单已保存：`./01_update_inventory.md`
- [x] 机器清单已保存：`./update_inventory.csv`

> [P1] 🔲 进行中 {in_progress}

---

## 阶段 2：批量更新计划
- [ ] 已按主题、版本、目录或优先级分组
- [ ] 每篇笔记已标注动作：update/flag-only/skip/needs-review
- [ ] 第一批处理列表已生成
- [ ] 覆盖风险和需用户确认项已列出
- [ ] 批量更新计划已保存：`./02_batch_update_plan.md`
- [ ] 用户已确认计划后才进入下一阶段

> [P2] ⬜ 未开始

---

## 阶段 3：共享资料收集（可选）
- [ ] 已确定共享资料适用的笔记范围
- [ ] 已收集最小必要资料
- [ ] 每条资料已记录 URL、日期、适用范围和摘要
- [ ] 来源库已保存：`./shared_research/source_bank.md`

> [P3] ⬜ 未开始

---

## 阶段 4：逐篇局部更新
- [ ] 已按 batch_size 分批处理
- [ ] 每篇笔记已生成 stale map
- [ ] 每篇笔记已局部更新或标记需复核
- [ ] 原文未被覆盖，除非 destination_mode 为 patch-in-place 且用户已确认
- [ ] 批处理日志已追加：`./03_batch_update_log.md`

> [P4] ⬜ 未开始

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
| P0 | 用户确认：范围=整套笔记统一；官方路线=彻底删除；destination_mode=patch-in-place + 全副本同步；batch_size=3 | 2026-10-06 20:47 |
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
