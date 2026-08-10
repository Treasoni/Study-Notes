---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "update-codex-config"
task: "Codex 笔记重构为 Claude Code 教程风格"
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: "Codex 笔记重构为 Claude Code 教程风格"
project_slug: "codex-config-update"
created_at: "2026-08-10"
last_updated: "2026-08-10"
current_phase: done
current_status: complete
mode: standard
confirmed_phases: "P0,P1,P2,P4,P5"
skippable_phases: "P3"
mode_dependent_skips: ""
allowed_modes: ""
mode_change_phase: ""
blocked_reason: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：Codex 笔记重构为 Claude Code 教程风格
> 运行标识：update-codex-config
> 项目标识：codex-config-update
> 创建时间：2026-08-10
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

> [P3] ⏭️ 跳过

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
| P5 | 用户确认 P5 汇总结果：9 篇+1 MOC 全部完成，旧 flat 文件已删除，MOC/索引已同步 | 2026-08-10 20:41 |
| P4 | 用户确认 9 篇逐篇更新结果：六区块齐全、title 唯一、updated/status 正确 | 2026-08-10 20:40 |
| P2 | 用户确认批量更新计划：分组/映射/patch-in-place/批次正确，开始 P4 | 2026-08-10 20:30 |
| P1 | 更新清单已生成：10 篇全部 ready，无 skip/needs-review | 2026-08-10 20:28 |
| P0 | 意图已由用户计划确认：source_path=AI学习/Codex/, update_goal=镜像Claude Code教程结构+套用模板, destination_mode=patch-in-place, batch_size=3, shared_research=no, moc_path=AI学习/Codex/Codex MOC.md | 2026-08-10 20:28 |
| | | |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| P3 | user approved skip | 纯排版重构，无需共享资料 | 2026-08-10 20:30 |
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| 2026-08-10 20:30 | P3 | 跳过阶段：纯排版重构，无需共享资料 | 继续推进到下一未完成阶段 |
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
