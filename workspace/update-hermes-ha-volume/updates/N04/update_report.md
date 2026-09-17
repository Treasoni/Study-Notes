# N04 update report — `01_explore_result.md` F2 勘误

**轮次**：`update-hermes-ha-volume` ｜ **批次**：3 ｜ **项**：N04 ｜ **日期**：2026-09-18
**目标文件**：`workspace/hermes-home-assistant/01_explore_result.md`（159 行 → 166 行）
**产出**：`updated_note.md`（本目录）

## 1. 做了什么

对 F2 做日期化勘误。原文断言「装个现成 skill」这条路在 HA 场景不存在，实际只查过 `official` 支（150 条）却当成整个 Hub 的结论；而本文档自己的来源 HMS-05 已写明 Hub 是**联邦索引**。已按 `source_bank.md` 锁定的数字与措辞改写旧 L8 / L29 / L31 / L33，插入勘误块（新 L9–L12），并登记 `HMS-13` / `COM-24` / `COM-25` 三条新来源。**洞察与路线结论未改**。

## 2. 编辑表（锚点 → 旧行 → 结果）

| # | 旧行 | 锚点（原文逐字） | 新行 | 结果 |
|---|---|---|---|---|
| 1 | L8 | `而"推荐个 skill 装上就行"这条最省事的路，在 HA 场景**不存在**。` | L8 | 只换末句 →「有东西可装…64 条…知识件…补不了能力」 |
| 2 | L29 | `### F2 "装个现成 skill"这条路不存在` | L33 | → `### F2 "装个现成 skill"这条路：有东西可装，但补不了能力` |
| 3 | L31 | `- Skills Hub 全部 bundled + optional skill 中，smart-home 类**只有 `openhue` 一个**；**没有 Home Assistant skill**（来源 HMS-04、HMS-05）` | L35 | 收窄 `official` 支 ＋ 联邦索引 ＋ 97,986 / 64 ＋ 时点限定；来源 → `HMS-04、HMS-05、HMS-13` |
| 4 | L33 | `- 结论：HA 场景下 skill 路线 = **自建** SKILL.md` | L37 | 仅补「可装的是知识件 / 不新增工具」限定；结论逐字保留 |
| 5 | 插入 L8 后 | L10 锚点 `## 二、五批探测记录` | L9–L12 | 新增 `## 勘误（2026-09-18，轮次 `update-hermes-ha-volume`）` ＋ 1 段 |
| 6 | 插入 L107 后 | `\| HMS-10 \| …use-mcp-with-hermes…` | L112 | 新增 `\| HMS-13 \| https://nousresearch.github.io/hermes-agent/docs/api/skills.json（…联邦索引、8 类来源；明示 HA 的 skill 64 条） \|` |
| 7 | 插入 L122 后 | `\| COM-10 \| 社区帖 1003703…` | L128 / L129 | 新增 `COM-24`（hass-cli：596★ / pushed 2026-08-04 / 未归档 / PyPI 1.0.0 / HA Ecosystem 组织，非 core 官方）与 `COM-25`（homeassistant-ai/skills：749★ / pushed 2026-09-16 / agentskills.io / 含 `home-assistant-best-practices` / 与 COM-01 同组织） |

**7 个锚点全部命中，无一失败。** difflib 复核：非 equal 块 **6 个**。

## 3. ID 清单（改前 → 改后，证据）

- **改前**：`HAS-01…HAS-16`（16）、`HMS-01…HMS-10`（10）、`COM-01…COM-10`（10）＝ 36 条。
- **改后**：上述 **36 条全部逐字保留**（`removed = []`）＋ 新增 `HMS-13`、`COM-24`、`COM-25`（`added = 3`）。
- 表行计数：HAS 16 → 16（不变）；HMS 10 → 11；COM 10 → 12。
- 未使用 `COM-11` / `COM-12` 等本地号；未重编号、未改写任何既有行。

## 4. 验证结果

| 检查 | 结果 |
|---|---|
| `\r` 计数 | **0** |
| BOM | **无**（首 3 字节非 `EF BB BF`） |
| 结尾换行 | 恰好 **1 个**（不以 `\n\n` 结尾） |
| 未预期行字节一致 | **通过**：difflib 的每个 equal 块内零字符差异 |
| 新 ID 出现次数 | `COM-24` = 1、`COM-25` = 1；**`HMS-13` = 2**（见 §5 偏差 1） |
| 新数字与 bank §2 逐字一致 | 97,986 / 64 ✓；时点限定 `截至 2026-09-18 的 Hub 中央索引快照` 同句出现 ✓ |
| `[[双链]]` 计数 | 0 → **0**（未新增） |
| 脚注 `[^` 计数 | 0 → **0**（未新增） |
| 表结构 | 未加列（HMS 2 列 / COM 3 列） |
| 残留错误断言 | L31 已无「没有 Home Assistant skill」；全文 `不存在` 仅剩勘误块内的**引言**（新 L12，标为「曾断言」） |
| 未触碰文件 | `00_intent.md`、`02_deep_research.md`、`03_outline.md`、`chapters/**`、`research/**`、`sources/**`、发布卷 —— 零改动 |

## 5. 偏差与遗留问题（3 条，需父流程知悉）

1. **`HMS-13` 出现 2 次而非 1 次**。这是任务自身要求的必然结果：编辑 3 要求 L31 来源列表写成 `HMS-04、HMS-05、HMS-13`（引用 1 次），编辑 6a 要求在 HMS 表登记该行（登记 1 次）。`COM-24` / `COM-25` 未被正文引用，故各 1 次。父验收若按「恰好 1 次」硬检，请对 `HMS-13` 放行至 2。
2. **旧 L32（社区 MCP bullet）逐字保留**。复核判定它不构成错误断言（说的是 ha-mcp 属 MCP 路线、不是 skill 路线），故未改，以守住「未预期行字节一致」。
3. **勘误块内含 `不存在` / `没有 Home Assistant skill` 的引言**。这是「说明原断言是什么」的必要代价，已用「曾断言」「据此写成」＋ `「」` 标记为被更正的旧话。若验收脚本对这两个词做全文禁用扫描，需豁免新 L12。
