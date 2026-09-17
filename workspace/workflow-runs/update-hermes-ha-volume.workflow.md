---
workflow_id: batch-note-update-flow
workflow_name: 批量旧笔记更新工作流
workflow_version: 1
state_file_type: workflow-run
run_id: "update-hermes-ha-volume"
task: "Hermes × Home Assistant 实战 分册：「Hub 里没有现成 HA skill」错误结论的批量补正"
created_from: ".claude/workflows/batch-note-update-flow/state-template.md"
topic: "Hermes × Home Assistant 实战 分册：「Hub 里没有现成 HA skill」错误结论的批量补正"
project_slug: "update-hermes-ha-volume"
created_at: "2026-09-18"
last_updated: "2026-09-18"
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
> 主题：Hermes × Home Assistant 实战 分册：「Hub 里没有现成 HA skill」错误结论的批量补正
> 运行标识：update-hermes-ha-volume
> 项目标识：update-hermes-ha-volume
> 创建时间：2026-09-18
> 当前阶段：完成
> 状态图例：⬜ 未开始 | 🔲 进行中 | ✅ 已完成 | ⏭️ 跳过

---

## 阶段 0：批量更新意图确认
- [x] source_path/source_scope/source_glob 已确认
- [x] update_goal 已确认
- [x] destination_mode 已确认
- [x] batch_size 已确认
- [x] shared_research 策略已确认
- [x] 批量更新意图已保存：`./00_batch_update_intent.md`

**说明**：source_path = `AI学习/Hermes Agent/Hermes × Home Assistant 实战/`（all / `*.md`，11 个文件）；
附带走 `workspace/hermes-home-assistant/` 的两份研究档（02_deep_research / 01_explore_result），属勘误不属笔记正文。
destination_mode 取 `patch-in-place`；batch_size = 2。shared_research 判定为「已就绪、不新开 P3」——
证据快照 `workspace/hermes-home-assistant/sources/HUB-homeassistant-skills.json`（56,846 B，64 条明示 HA + 13 条 smart-home）
与 `hass-cli` / `homeassistant-ai/skills` 的 API 核实均已在 P0 前完成，届时按 P3 可选阶段 `skip` 并写明原因。
本阶段为**零写入**阶段：未改动分册中任何文件。

> [P0] ✅ 已完成 {complete}

---

## 阶段 1：更新清单
- [x] 已扫描目标范围内的 Markdown 笔记
- [x] 已记录 frontmatter、标题、目录、更新时间和关键词命中
- [x] 已标记 candidate/ready/needs-review/skip
- [x] 更新清单已保存：`./01_update_inventory.md`
- [x] 机器清单已保存：`./update_inventory.csv`

**说明**：扫描 13 个文件（分册 11 + 研究档 2）。**要动 6 个**：N01 `03-路线选型.md`（18 处）、
N02 `01-结论先行与能力地图.md`（11 处）、N03 `02_deep_research.md`（5 处）、N04 `01_explore_result.md`（4 处）、
N05 `04-落地-社区ha-mcp.md`（1 处，首轮漏检、补模式后命中）、N12 `10-附录`（补来源条目）。
其余 7 个 0 命中 → skip。**三处与原方案的差异**已记在清单第 5 节：README 撤销、04 新增、`output/final_note.md` 提交拍板。
另发现同一正文有**三份活副本**（`chapters/` 源 → 分册 → `output/final_note.md`），本次 scope 只覆盖中间一份，机制待定（清单第 4 节，甲/乙/丙）。
本阶段仍为零写入：未改动分册与两份研究档中的任何文件。

> [P1] ✅ 已完成 {complete}

---

## 阶段 2：批量更新计划
- [x] 已按主题、版本、目录或优先级分组
- [x] 每篇笔记已标注动作：update/flag-only/skip/needs-review
- [x] 第一批处理列表已生成
- [x] 覆盖风险和需用户确认项已列出
- [x] 批量更新计划已保存：`./02_batch_update_plan.md`
- [x] 用户已确认计划后才进入下一阶段

**说明**：机制甲的执行链 = 改 `chapters/` 源 → `assemble_note.py` → `publish_volume.py` → hash 验收（8 篇 + README 逐字节不变）。
**读源码发现一处契约边界**：`normalize_chapters.py` 的 `verify()` 不变量是「只改导航/标题写法、正文逐字不变」，
本次新增整节会触发它「无法追溯的新行」并拒绝写盘——**这不是缺陷，是职责边界**，故内容修改后不跑它，
改为「改前预检（期望 10/10 无变化）+ 改后由 assemble/publish 的断言守卫」。
分批：批 1 = N01 ch03 + N02 ch01（同一句话的两处表述）；批 2 = N05 ch04 + N12 附录；批 3 = N03/N04 研究档；批 4 = 父流程重生成。
P3 改为「编制 source_bank.md（不新收集）」而非 skip（与 P0 记录的差异，将写进最终报告）。
新增节拟插为 3.2，代价 5 个标题顺延 + **2 处**交叉引用（L67、L255）。

> [P2] ✅ 已完成 {complete}

---

## 阶段 3：共享资料收集（可选）
- [x] 已确定共享资料适用的笔记范围
- [x] 已收集最小必要资料
- [x] 每条资料已记录 URL、日期、适用范围和摘要
- [x] 来源库已保存：`./shared_research/source_bank.md`

**说明**：P0 曾判「已就绪、P3 记 `skip`」，P2 改为 **start → 编制 → complete**（不新开收集）：产物
`shared_research/source_bank.md` 本来就是本工作流规定的共享资料位，跳过它会让措辞锁没有落点。
本文件是**全局措辞与数字锁**，供批 1–3 逐字引用——锁定 7 个数字（97,986 / 64 / 52 / 12 / 13 / 150 / 8 类源）、
5 段可直接引用的措辞（含 `hass-cli` 的「HA Ecosystem 组织、非 HA core 官方」精确写法）、26 条逐字安装命令、
A/B/C/D 四级判据、**3 条禁令 + 2 条注意事项**（不得写回原错误结论、不得称 `hass-cli` 官方、
不得把未验证的 `home-assistant/core` 那件写成官方出品）、以及 D-1…D-5 五条资料（URL + 日期 + 适用范围 + 摘要）。
适用笔记范围 = 全部 6 个目标（N01–N05 + N12）。
本阶段仍为零写入：未改动分册与两份研究档中任何文件；新增仅 `workspace/update-hermes-ha-volume/` 下的本阶段产物。

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
| P0 | 确认更新范围（分册 + 2 份研究档）、目标、`patch-in-place`、批大小 2；同意 P3 暂记「已就绪」 | 2026-09-18 01:4x |
| P1 | 确认清单可信；**选机制甲**（改 `chapters/` 源头 → 重生成 ② ③，而非只改发布件） | 2026-09-18 01:4x |
| P2 | 确认分批（1=ch03+ch01 / 2=ch04+附录 / 3=研究档 / 4=父流程重生成）、动作表；**新增节插为 3.2**（5 标题顺延 + 2 处交叉引用）；N12 按 `flag-only`；研究档带日期勘误块、不动 `00_intent`/`03_outline`/`probe-*` | 2026-09-18 01:49 |

---

## 跳过记录

| 阶段 | 确认内容 | 原因 | 时间 |
|------|----------|------|------|
| | | | |

---

## 异常记录

| 时间 | 阶段 | 问题描述 | 处理方式 |
|------|------|---------|---------|
| 2026-09-18 02:20 | P4（批 2 收口） | `chapters/06-事件驱动与定时任务.md` 与 `chapters/10-附录.md` 本就是纯 CRLF，其余 8 篇与整个分册是 LF（**非本轮引入**） | 改为**按文件保留原行尾**写回，交付物仍强制 LF。06 是 `skip` 项，保持 CRLF 逐字节未变 |
| 2026-09-18 02:55 | P4（批 3） | N03 子代理自建 `.tmp_n03_apply.py`，写盘目标指向发布源 `02_deep_research.md`，等于绕过父流程的确定性验收 | 写盘前叫停、令其删除脚本并补齐四份产物；`git status` 全程无该文件改动，sha256 保持 `9feb03c4…` 未变 |
| 2026-09-18 02:55 | P4（批 3） | 派发稿给的 3 处 N03 行号与文件实际不符（HMS-12 稿 L92→实 L95、`两个工具坑` 稿 L340→实 L335、§5.8 插入点实际为 L356 的 `---` 之后） | 子代理全程按锚点定位，未受影响；已记入 `updates/N03/update_plan.md` 的「编号失配记录」 |

---

## 批处理记录

| 时间 | 批次 | 文件数 | 成功 | 需复核 | 输出位置 |
|------|------|--------|------|--------|----------|
| 2026-09-18 01:57 | 批 1（N02、N01） | 2 | 2 | 0 | `chapters/01-结论先行与能力地图.md`、`chapters/03-路线选型.md` |
| 2026-09-18 02:20 | 批 2（N05、N12） | 2 | 2 | 0 | `chapters/04-落地-社区ha-mcp.md`、`chapters/10-附录.md` |
| 2026-09-18 02:52 | 批 3（N04、N03） | 2 | 2 | 0 | `01_explore_result.md`、`02_deep_research.md` |
| 2026-09-18 02:35 | 批 4（父流程重生成） | 11 | 11 | 0 | 分册 11 个文件 + `output/final_note.md` |

---

## 最终产出

- **源路径**：`AI学习/Hermes Agent/Hermes × Home Assistant 实战/`
- **更新目标**：修正「Skills Hub 里没有现成 HA skill」这一事实性错误结论，并在第 3 章新增 `### 3.2 Hub 里现成可装的 HA skill 清单`
- **处理文件数**：13（分册 11 + 研究档 2）
- **更新文件数**：6（`chapters/` 4 篇 + 研究档 2 份），另有 `output/final_note.md` 随重生成变动
- **跳过文件数**：7（分册中逐字节未变：02、05、06、07、08、09 + README）
- **需复核文件数**：0
- **输出模式**：`patch-in-place`（机制甲：改上游 `chapters/` 发布源 → 重生成分册与 `output/final_note.md`）
- **文件路径**：`workspace/update-hermes-ha-volume/04_batch_update_report.md`
- **Obsidian Vault**：本仓库根（vault 即当前工作目录）
- **MOC 路径**：`AI学习/Hermes Agent/Hermes Agent MOC.md`（已同步：索引项补「Hub 现成 HA skill 清单」，未新增行、未复制正文）
