---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: update-mirror-config
task: 镜像加速器笔记过时信息批量修复
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: 镜像加速器笔记过时信息批量修复
project_slug: update-mirror-config
created_at: "2026-08-08"
last_updated: "2026-08-08"
current_phase: P2
current_status: in_progress
mode: standard
confirmed_phases: "P0,P1"
skippable_phases: "P3"
mode_dependent_skips: ""
allowed_modes: ""
mode_change_phase: ""
blocked_reason: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：镜像加速器笔记过时信息批量修复
> 运行标识：update-mirror-config
> 项目标识：update-mirror-config
> 创建时间：2026-08-08
> 当前阶段：阶段 2
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：批量更新意图确认
- [x] source_path/source_scope/source_glob 已确认：docker/ 目录（仅镜像加速器相关 4 篇）
- [x] update_goal 已确认：修复 Docker Desktop 不读 ~/.docker/daemon.json 的误导 + 已失效镜像源（USTC/NJU/SJTU）
- [x] destination_mode 已确认：patch-in-place
- [x] batch_size 已确认：3（实际更新 2 篇，单批完成）
- [x] shared_research 策略已确认：yes（复用上一轮已核实资料）
- [x] 批量更新意图已保存：`./00_batch_update_intent.md`

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

> [P2] 🔲 进行中

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
| P1 | 清单可信：2 update + 2 skip，与已确认范围一致 | 2026-08-08 18:52 |
| P0 | 范围与输出模式已确认 | 2026-08-08 18:51 |
| P0 | 范围=docker/ 镜像加速器笔记；输出=patch-in-place | 2026-08-08 |

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

- **源路径**：docker/（镜像加速器相关 4 篇）
- **更新目标**：修复 ~/.docker/daemon.json 误导 + 已失效镜像源
- **处理文件数**：4
- **更新文件数**：2
- **跳过文件数**：2
- **需复核文件数**：
- **输出模式**：patch-in-place
- **文件路径**：docker/ 原笔记（直接 patch）
- **Obsidian Vault**：docker/
- **MOC 路径**：docker/Docker MOC.md
