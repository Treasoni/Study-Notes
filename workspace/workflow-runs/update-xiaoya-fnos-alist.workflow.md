---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "update-xiaoya-fnos-alist"
task: "小雅 fnOS 单容器部署笔记集：把部署路线从已停维护的 monlor 镜像统一改写为持续维护的 xiaoyaDev/xiaoya-alist（DDSRem）一键菜单脚本"
topic: "小雅 fnOS 单容器部署笔记集：monlor 路线 → xiaoyaDev/xiaoya-alist（DDSRem）路线"
project_slug: "xiaoya-fnos-deploy"
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
created_at: "2026-10-07"
last_updated: "2026-10-07"
current_phase: done
current_status: complete
mode: standard
blocked_reason: ""
quality_gate: passed
quality_gate_owner: ""
quality_gate_due: ""
---

# 批量旧笔记更新工作流 - 执行检查清单

> 工作流：batch-note-update-flow
> 主题：小雅 fnOS 单容器部署笔记集：monlor 路线 → xiaoyaDev/xiaoya-alist（DDSRem）路线
> 运行标识：update-xiaoya-fnos-alist
> 项目标识：xiaoya-fnos-deploy
> 创建时间：2026-10-07
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

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：更新清单
- [ ] 已扫描目标范围内的 Markdown 笔记
- [ ] 已记录 frontmatter、标题、目录、更新时间和关键词命中
- [ ] 已标记 candidate/ready/needs-review/skip
- [ ] 更新清单已保存：`./01_update_inventory.md`
- [ ] 机器清单已保存：`./update_inventory.csv`

> [P1] ✅ 已完成 {complete}

---

## 阶段 2：批量更新计划
- [ ] 已按主题、版本、目录或优先级分组
- [ ] 每篇笔记已标注动作：update/flag-only/skip/needs-review
- [ ] 第一批处理列表已生成
- [ ] 覆盖风险和需用户确认项已列出
- [ ] 批量更新计划已保存：`./02_batch_update_plan.md`
- [ ] 用户已确认计划后才进入下一阶段

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：共享资料收集（可选）
- [ ] 已确定共享资料适用的笔记范围
- [ ] 已收集最小必要资料
- [ ] 每条资料已记录 URL、日期、适用范围和摘要
- [ ] 来源库已保存：`./shared_research/source_bank.md`

> [P3] ✅ 已完成 {complete}

---

## 阶段 4：逐篇局部更新
- [x] 已按 batch_size 分批处理
- [x] 每篇笔记已生成 stale map
- [x] 每篇笔记已局部更新或标记需复核
- [x] 原文未被覆盖，除非 destination_mode 为 patch-in-place 且用户已确认
- [x] 批处理日志已追加：`./03_batch_update_log.md`

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：汇总与 MOC 同步
- [x] 已汇总更新、跳过、失败和需复核数量
- [x] 已汇总每篇输出路径和风险
- [x] 如提供 MOC，已同步索引且未复制正文
- [x] 批量更新报告已保存：`./04_batch_update_report.md`

> [P5] ✅ 已完成 {complete}

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P2 | 用户确认：截图删掉两张 monlor 界面图；ch04 章名定为「第 4 章 部署实战——单容器小雅（一键脚本）」；批次 04→03→07 / 01→02→总览 / 05→06 通过 | 2026-10-07 08:06 |
| P0 | 用户确认：范围＝整套 8 篇统一改写；部署形态＝一键菜单脚本；主线＝保持单容器/飞牛影视 | 2026-10-07 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| 2026-10-07 09:00 | P4 | 全量 `publish_copies.py --check` 发现 ch04 的 output/vault 副本滞留在旧锚点（`:1302`、`:1290-1292`），`chapters/04` 已是修正后的 `:1304`、`:1293-1294` | 核对源码确认真值后 `--apply --only 04` 重发布；七章副本全部 OK；记入 `03_batch_update_log.md` P4 收口行 |
| 2026-10-07 09:20 | P5 | `note-citation-check.py` 误报：S4「出处列非法」72 处（出处取值域不认 `.sh`，而本主题逐字引文出自 `sources/xiaoyaDev/all_in_one.sh`） | canonical `.codex/scripts/` 中 `CITE_FULL` 扩展 `.sh`，`sync_agents.py --scope scripts --apply` 同步 |
| 2026-10-07 09:30 | P5 | `note-citation-check.py` 误报：S4「管道数 != 5」4 处（引文里引用 shell 管道 / 一行表格，单元格内竖线写成正确转义的 `\|`） | 改为只计未转义竖线并按未转义竖线切列；新增自测用例 G 守回归；同步 scripts |
| 2026-10-07 09:35 | P5 | V 逐字回源误报 4 处：ch05 §5.4.2 的 `docker compose config` 报错原文被当作英文散文引文 | 将该输出改为带语言标识的代码块（命令输出不是散文引文），重发布 ch05 并重装 final_note |

---

## 批处理记录

| 时间 | 批次 | 文件数 | 成功 | 需复核 | 输出位置 |
|------|------|--------|------|--------|----------|
| 2026-10-07 08:06 | 批 1 部署主线（ch04 → ch03 → ch07） | 3 | 3 | 0 | `chapters/04..07` + `updates/04..07/` |
| 2026-10-07 08:16 | 批 2 定位与选型（ch01 → ch02 → overview） | 3 | 3 | 0 | `chapters/01..02` + `output/…（总览）.md` + `updates/01..02/` |
| 2026-10-07 08:19 | 批 3 前端与避坑（ch05 → ch06 → 章名回灌） | 3 | 3 | 0 | `chapters/05..06` + overview/ch05 回灌 + `updates/05..06/` |

---

## 最终产出

- **源路径**：`流媒体与影音/小雅 fnOS 单容器部署/`（7 章 + 总览）
- **更新目标**：部署主线由 monlor 镜像统一改写为 `xiaoyaDev/xiaoya-alist`（DDSRem）一键菜单脚本
- **处理文件数**：8
- **更新文件数**：8
- **跳过文件数**：0
- **需复核文件数**：0
- **输出模式**：patch-in-place
- **文件路径**：`chapters/01..07`（= `updated_note`）；`output/01..07`、`output/final_note.md`、`output/小雅 fnOS 单容器部署（总览）.md`
- **Obsidian Vault**：`流媒体与影音/小雅 fnOS 单容器部署/`（7 章 + 总览，共 8 篇）
- **MOC 路径**：`流媒体与影音 MOC.md`（已含小雅条目，无需改动）
