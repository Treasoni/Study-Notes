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
> 主题：小雅 fnOS 单容器部署笔记集：统一为 monlor 镜像单一路线，彻底删除官方 xiaoyaliu/alist 路线
> 运行标识：update-xiaoya-fnos-routes
> 项目标识：xiaoya-fnos-deploy
> 创建时间：2026-10-06
> 当前阶段：完成
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

> [P3] ⏭️ 跳过 {skipped}

---

## 阶段 4：逐篇局部更新
- [x] 已按 batch_size 分批处理（批 1 = 04/03/07；批 2 = 01/总览；收口 = 03 小节回填 + 合并件重装配）
- [x] 每篇笔记已生成 stale map（见 `./02_batch_update_plan.md` 的逐篇 stale 表，覆盖 5 个 update 篇）
- [x] 每篇笔记已局部更新或标记需复核（update 篇全部落地，无 needs-review）
- [x] 原文未被覆盖，除非 destination_mode 为 patch-in-place 且用户已确认（P0 已确认 patch-in-place + 全副本同步）
- [x] 批处理日志已追加：`./03_batch_update_log.md`

> [P4] ✅ 已完成 {complete}

---

## 阶段 5：汇总与 MOC 同步
- [x] 已汇总更新、跳过、失败和需复核数量（8 处理 / 6 更新 / 2 跳过 / 0 失败 / 0 需复核）
- [x] 已汇总每篇输出路径和风险（见 `./04_batch_update_report.md` 第二、五节）
- [x] 如提供 MOC，已同步索引且未复制正文（`流媒体与影音 MOC.md` 指向未改名的入口页，无需改动）
- [x] 批量更新报告已保存：`./04_batch_update_report.md`

> [P5] ✅ 已完成 {complete}

---

## 用户确认记录

| 阶段 | 确认内容 | 时间 |
|------|----------|------|
| P4 | 批 1（04/03/07）+ 批 2（01/总览）+ 收口（03 小节回填、合并件重装配）全部落地；三副本逐字节一致 | 2026-10-06 21:11 |
| P2 | 用户确认批量计划：新章名「单容器小雅（monlor 镜像）」；4.1 与原 4.4 合并为「为什么用 monlor 镜像」；批 1 = 04/03/07，批 2 = 01/总览 | 2026-10-06 20:57 |
| P1 | 用户确认更新清单可信（update 5 篇 / skip 3 篇）；并确认第 4 章 4.2 整节删除（含整合脚本入口） | 2026-10-06 20:55 |
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
| 2026-10-06 20:57 | P3 | 跳过阶段：shared_research: no；本轮结论全部回源到 workspace/xiaoya-fnos-deploy/sources/ 已有素材（用户已确认） | 继续推进到下一未完成阶段 |
| 2026-10-06 21:08 | P4/P5 | 并行会话（claude-03）同期改动第 5 章（MediaWarp 结论更正），与本运行编辑面不重叠；共享写点仅合并件 `output/final_note.md`（幂等） | 保持只读 05；收口前复跑 `publish_copies.py --check` 与 `note-citation-check.py`，快照确认 C 族 0 差异、三副本全 `==` |
| 2026-10-06 | 收口后 | 用户实战反证：WebDAV 默认用户是 `guest`，原稿据 monlor env 注释写成「用户名固定 `dav`」（方向写反） | 按 `note-updater` 就地修正 03 §3.3.2 与 04 自检/小结/引文对照，补独立来源回源；`publish_copies.py --apply`（03/04）+ `assemble_final.py --apply`，复跑三项校验全通过（详见 `03_batch_update_log.md` 收口 3） |
| | | | |

---

## 批处理记录

| 时间 | 批次 | 文件数 | 成功 | 需复核 | 输出位置 |
|------|------|--------|------|--------|----------|
| 2026-10-06 | 批 1 | 3 | 3 | 0 | `chapters/` 04、03、07 → `output/` 与 vault 三副本已同步 |
| 2026-10-06 | 批 2 | 2 | 2 | 0 | `chapters/` 01 + 入口页`（总览）` → `output/` 与 vault 已同步 |
| 2026-10-06 | 收口 | 2 | 2 | 0 | `chapters/` 03 小节回填；合并件 `output/final_note.md` 重装配 |

---

## 最终产出

- **源路径**：`workspace/xiaoya-fnos-deploy/chapters/`
- **更新目标**：小雅 fnOS 单容器部署笔记集全篇统一为 monlor 单一路线，删除官方 `xiaoyaliu/alist` 镜像路线
- **处理文件数**：8（7 章 + 入口页；另重装配合并件 1）
- **更新文件数**：6（第 1、3、4、7 章 + 入口页 + 合并件）
- **跳过文件数**：2（第 5、6 章；第 2 章亦未变）
- **需复核文件数**：0
- **输出模式**：`patch-in-place` + 全副本同步
- **文件路径**：`workspace/xiaoya-fnos-deploy/output/`（7 分册 + `final_note.md` + `（总览）.md`）
- **Obsidian Vault**：`流媒体与影音/小雅 fnOS 单容器部署/`
- **MOC 路径**：`流媒体与影音 MOC.md`（无需改动）
- **质量门**：`quality_gate: passed`（引文校验 ✅ / 三副本全 `==` / 结构自检 0 处）
