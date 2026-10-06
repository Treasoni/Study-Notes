# N04 update plan — `01_explore_result.md`

**模式**：`patch-in-place`（本目录产出 `updated_note.md`，由父流程应用到目标文件）
**性质**：`F2` 的**日期化勘误**（范围错误）＋ 3 条新来源登记
**来源基准**：`shared_research/source_bank.md`（§1 时点限定、§2 数字锁、§3 措辞锁、§6 禁令、§7 D-1/D-2/D-3）
**行号口径**：`旧行` = 改动前 `01_explore_result.md` 行号（1-based；本文件唯一编号，无偏移）；`新行` = `updated_note.md` 行号。

## 1. 改动清单（共 4 个既有行位 + 2 处插入）

| # | 旧行 | 定位锚点（原文逐字，父验收 allow-list 用） | 新行 | 改法 |
|---|---|---|---|---|
| 1 | L8 | `而"推荐个 skill 装上就行"这条最省事的路，在 HA 场景**不存在**。` | L8 | **只换末句**：`在 HA 场景**不存在**。` → `在 HA 场景**有东西可装**——**截至 2026-09-18 的 Hub 中央索引快照**里，明示 Home Assistant 的 skill 有 **64 条**，但它们只是**知识件**，补不了能力。` 该行前半句逐字不动 |
| 2 | L29 | `### F2 "装个现成 skill"这条路不存在` | L33 | 标题改断言：`不存在` → `：有东西可装，但补不了能力`（`F2` 标签与位置不变） |
| 3 | L31 | ``- Skills Hub 全部 bundled + optional skill 中，smart-home 类**只有 `openhue` 一个**；**没有 Home Assistant skill**（来源 HMS-04、HMS-05）`` | L35 | 整行重写（见 §2）：`openhue` 事实收窄到 `official` 支 ＋ 联邦索引 ＋ 97,986 / 64 ＋ 时点限定；来源改 `HMS-04、HMS-05、HMS-13` |
| 4 | L33 | `- 结论：HA 场景下 skill 路线 = **自建** SKILL.md` | L37 | 仅**补限定**（可装的是知识件、不新增任何工具）；结论「= 自建 SKILL.md」**逐字保留** |
| 5 | 插入于 L8 与 L9 之间 | 锚点：L9 = 空行、L10 = `## 二、五批探测记录` | L9–L12 | 新增 4 行：空行 ＋ `## 勘误（2026-09-18，轮次 `update-hermes-ha-volume`）` ＋ 空行 ＋ 1 段正文（见 §3） |
| 6a | 插入于 L107 之后 | 锚点：L107 = `\| HMS-10 \| https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes （`/reload-mcp`、排错） \|` | L112 | 新增 1 行 2 列表行 `\| HMS-13 \| … \|`（来源列 URL 后括号内带限定语） |
| 6b | 插入于 L122 之后 | 锚点：L122 = `\| COM-10 \| 社区帖 1003703（Telegram/OpenClaw skill）…` | L128 / L129 | 新增 2 行 3 列表行 `\| COM-24 \| … \| … \|`、`\| COM-25 \| … \| … \|`，不新增列 |

**共 7 个行位**（4 改 ＋ 1 段插入 ＋ 2 行插入）；difflib 复核为 **6 个 hunk**（相邻的勘误插入与 L8 改写归并为一个 replace 块）。

## 2. L31 重写后的正文（逐字）

`- `official` 支（Hermes 仓库内的 bundled + optional skill）里，smart-home 类**只有 `openhue` 一个**；但这只是整个 Hub 的一支——Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表；据**截至 2026-09-18 的 Hub 中央索引快照**，97,986 条记录中**明示 Home Assistant 的 skill 有 64 条**（来源 HMS-04、HMS-05、HMS-13）`

数字出处：97,986 / 64 ＝ bank §2；时点限定 ＝ bank §1 固定写法（照抄）；联邦索引措辞 ＝ bank §3「关于 Hub 是什么」。

## 3. 勘误块正文（逐字，无表格、无脚注、无双链）

`本文档 F2 曾断言「装个现成 skill」这条路在 HA 场景**不存在**，并据此写成「没有 Home Assistant skill」「HA 场景不存在可调的 `ha` CLI」。这是**范围错误**：当时的核对只覆盖了 `official` 支（Hermes 仓库内的 bundled / optional skill 目录，即索引里的 150 条），而本文档自己的来源 HMS-05 就已写明，Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表，`official` 只是其中一支。本轮重取中央索引复核：**截至 2026-09-18 的 Hub 中央索引快照**共 97,986 条记录，其中明示 Home Assistant 的 skill 有 64 条；`hass-cli`（`home-assistant-ecosystem/home-assistant-cli`）也确实存在。据此 F2 改了三处：标题改为「有东西可装，但补不了能力」；原「没有 Home Assistant skill」一句收窄为 `official` 支的范围并补上可装条数；结论 bullet 补上「可装的只是知识件」这一限定。新增来源已登记在第四节的来源索引里。**未改动**的是洞察与结论：skill 仍然只是**知识件**，不新增任何工具；skill 路线在 HA 场景仍然等于自建 SKILL.md，路线选型结论不变。`

块内对旧断言的引用一律用「曾断言」「据此写成」＋ `「」` 标记为**被更正的旧话**，不构成新断言。

## 4. 明确不动

- **既有 ID 行一律不改**：HAS-01…HAS-16、HMS-01…HMS-10、COM-01…COM-10 每一行逐字保留（未改号、未删除、未重排）。
- L32（社区 MCP 那条 bullet）逐字保留；L6 标题、L34 起的 F3 及其后全部章节。
- 不新增 `[[双链]]`（0 → 0）、不新增脚注（0 → 0）、不新增或修改代码围栏。
- 不写「官方口径」；不宣称 `hass-cli` 是 HA 官方（bank §6 禁令 2）；不把 `home-assistant/core/home-assistant-integration-knowledge` 写成官方或已验证（bank §6 禁令 3）。
- 未列出的行：逐字保持，含标点、全角符号、空行、行尾。
