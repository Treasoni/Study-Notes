# N02 更新报告 — `chapters/01-结论先行与能力地图.md`

**Note ID**：N02 ｜ **动作**：`update`（局部 patch）｜ **destination_mode**：`patch-in-place`（父流程应用）
**目标（发布源）**：`D:\Study-Notes\workspace\hermes-home-assistant\chapters\01-结论先行与能力地图.md`
**措辞锁**：`workspace\update-hermes-ha-volume\shared_research\source_bank.md`

---

## 1. 改动量（对发布源，逐字节比对结果）

> 本节为**追加改动后重跑**的结果（父流程追加批准 `### 本章来源` 的 COM-24 条目，见 §2.6）。重跑命令即本目录曾用的 `_apply_n02_v2.py`，断言 + `difflib` 全量重算，已删除该临时脚本。

| 指标 | 值 |
|---|---|
| 改动 hunk 数 | **3** |
| 改动新增行数 | **10** |
| 改动删除行数 | **10** |
| 其中**净变化行**（内容真正不同的行） | **6 行替换 = 6 删 + 6 增** |
| 净变化以外的 diff 记录 | 4 行「伪改动」：3 行空行 + 1 行 `> [!tip] 大白话` 标记行。它们在新旧文本中**逐字节相同**，只是 `difflib` 为对齐 hunk `@@ -37,14 +37,14 @@` 而重复输出，非真实改动 |
| 文件行数 | 262 → **262**（不变） |
| 小节标题数 / 编号 | **不变**（无新增、无删除、无顺延） |
| 代码围栏 | 不变（14 行围栏标记，未触及） |
| 行尾 / 编码 | LF / UTF-8 无 BOM（源文件本身 CRLF 计数为 0） |
| 源文件 sha256（未改动） | `df3c581cde764c8d1b1444fc617caf91717d4d18d6b7a3d47472b95e0c197517` |
| `updated_note.md` sha256 | `6dc74b32f4c9ae2df079888302d97af137ac7e3ce60c795babfb9c415bfa9671` |

**改动行（发布源 = 分册行号 − 15）**：`L40 / L42 / L44 / L47 / L252`（计划第 4 节 N02 表 5 行，分册 L55/L57/L59/L62/L267）**＋ `L262`**（分册 L277，父流程追加批准）。

**明确声明**：除上述 **6 行**外，**没有任何其他差异**。已用脚本断言 `changed == [40, 42, 44, 47, 252, 262]`（全 262 行逐位置相等）方才写盘；`updated_note.md` 回读后与计算结果逐行相等。完整自检记录见 `diff_check.txt`。

---

## 2. 逐处改动：改了什么、为什么、引 `source_bank.md` 哪一条

### 2.1 发布源 L40（分册 L55）｜结论二标题 — 整句重写

- **旧**：`**结论二：「装个现成 skill 就能用」在 HA 场景不成立。**`
- **新**：`**结论二：Hub 里有可装的 HA skill——但可装不等于能补能力。**`
- **为什么**：原句是本次要补正的事实性错误结论的**标题形态**。按计划第 4 节 N02「L55 改为准确表述（可装 ≠ 能补能力）」重写；仍是**结论式**一句话，未变成清单或教程。
- **引用**：`source_bank.md` **第 6 节禁令 1**（不得写「Hub 里没有现成 HA skill／没有可装的东西／不存在可调的 `ha` CLI」）；口径取自计划第 4 节 N02 L55。

### 2.2 发布源 L42（分册 L57）｜第一层依据 — 保留事实、加范围限定

- **改**：①「第一层是**事实**核对」→「第一层是**范围**核对」；②「Hermes 官方 optional skills 目录的」→「**official 支**（Hermes 仓库内的 optional skills）的」；③行末追加范围限定与联邦索引说明。
- **逐字保留**：`openhue`；「smart-home 分类下只有一个条目」；`“Control Philips Hue lights, scenes, rooms via OpenHue CLI.”`；「bundled skills 目录里连 smart-home 这个分类都还没有」；「技能系统的说明页 `website/docs/user-guide/features/skills.md`（HMS-05）全文未出现 Home Assistant」。
- **追加的限定句（逐字取自锁）**：`Hub 的搜索由一份**联邦索引**回答，覆盖 \`official\` 之外的外部注册表（skills.sh、ClawHub、LobeHub、browse.sh、well-known 端点、GitHub taps）；\`official\`（Hermes 仓库内的 optional/bundled skills）只是其中一支`。
- **为什么**：计划第 1 节诊断「第一层（范围错）：把 Hermes 仓库内 `optional-skills/` 目录（= 索引里的 `official` 支）当成了整个 Skills Hub」，计划第 4 节 N02 L57 要求「保留 `official` 支只有 `openhue` 这个事实，加上范围限定，并点明 Hub 是联邦索引」。
- **引用**：`source_bank.md` **第 3 节「关于 Hub 是什么」**（联邦索引锁定措辞）、**第 3 节「关于原册那层事实」**（「official 支的 smart-home 分类下只有 `openhue` 一个」本身没错）。

### 2.3 发布源 L44（分册 L59）｜第二层依据 — 换举证，不换结论

- **删**：`；而 HA 场景并不存在一个可以让 skill 去指挥的 \`ha\` CLI`（计划第 4 节 N02 L59 点名要删）。
- **改末句**：「所以「搜一个 HA skill 装上」这条路，在能搜到的那一刻之前就已经断了。」→「所以这条路的准确说法不是「搜不到」，而是「搜得到、装得上，但装完仍然**不提供新能力**」。」
- **增（逐字取自锁）**：`\`hass-cli\` 指的是 \`home-assistant-ecosystem/home-assistant-cli\`，**Home Assistant Ecosystem 组织**维护的命令行工具，是社区里的事实标准，**不是 HA core 官方出品**（Hub 里 \`clawhub/homeassistant-cli\` 条目的自述称其为 “official”，措辞不精确，本册不沿用）；Hub 里也**有**封装它的 skill（\`clawhub/homeassistant-cli\`）。`
- **逐字保留**：`**skill 不是能力，是知识**`；「它教 agent 怎么调已有的工具，不新增工具」；「这里只点一句、第 3 章展开」（ch03 本次将新增 3.2 节，前向指引仍成立）。
- **为什么**：计划第 1 节诊断「第二层（事实错）」，计划第 4 节 N02 L59「删…改为「`hass-cli` 存在，Hub 里有封装它的 skill」；保留「skill 是知识不是能力」」。原句末句是由错误举证推出的错误结论，必须同处替换，否则留着仍是否定句。
- **引用**：`source_bank.md` **第 3 节「关于 `hass-cli`」**（精确归属 ＋ 不沿用它自述的 “official”）、**第 3 节「关于洞察的保留」**（补的是举证、不是结论；这些 skill 仍只是知识件，不新增任何工具）、**第 6 节禁令 2**（不得宣称 `hass-cli` 是 HA 官方工具）、**第 6 节注意事项**（ClawHub 条目自述措辞不可沿用）。

### 2.4 发布源 L47（分册 L62）｜大白话末句

- **旧末句**：`HA 场景现在缺的是机器，不是说明书。`
- **新末句**：`机器有（\`hass-cli\`），说明书得自己找——Hub 里有；但说明书再全，机器还是那几台。`
- **逐字保留**：`把 skill 想成一份「岗位说明书」：它告诉你现有这几台机器怎么操作，但不会凭空给你添一台新机器。`
- **为什么**：旧末句与「`hass-cli` 存在」直接矛盾，必须改；计划第 4 节 N02 L62「大白话末句改」。沿用计划给 N01 L108 的同一句「机器有（`hass-cli`）」，保证同批两章措辞一致，且隐喻骨架（说明书 / 机器）不变。
- **引用**：`source_bank.md` **第 3 节「关于洞察的保留」**。

### 2.5 发布源 L252（分册 L267）｜本章小结对应条目 — 重写

- **旧**：`- 「装个现成 HA skill」这条路不存在：官方 optional skills 的 smart-home 分类下只有 \`openhue\` 一个，而 skill 本身也不提供新能力。`
- **新**：`- 「装个现成 HA skill」这条路**有东西可装**，但**可装不等于能补能力**：Hub 的搜索由一份联邦索引回答，「只有 \`openhue\` 一个」说的只是 \`official\` 支；skill 本身仍然只是知识，不提供新工具。`
- **为什么**：小结复述了与 L40/L42 同一处错误，必须同步；计划第 4 节 N02 L267「本章小结对应条目改」。
- **引用**：`source_bank.md` **第 3 节「关于 Hub 是什么」＋「关于原册那层事实」＋「关于洞察的保留」**。

### 2.6 发布源 L262（分册 L277）｜`### 本章来源` — 追加 COM-24【父流程追加批准，对已批准计划的扩展】

- **追加文本（逐字）**：`；COM-24 \`home-assistant-ecosystem/home-assistant-cli\`（github.com/home-assistant-ecosystem/home-assistant-cli；PyPI \`homeassistant-cli\` 1.0.0）`
- **插入位置**：来源枚举内，紧跟 `COM-23 ha-mcp Setup Wizard（homeassistant-ai.github.io/ha-mcp/setup/）`，在 `。场景表来自` 之前。`；` 与枚举既有分隔符同形；段末「场景表来自 `research/probe-03-scenarios.md`，该表不在 canonical 注册表内，本章按其原文逐行核对后使用。」一字未动，仍居末位。
  > 落点说明：父流程写「段落末尾追加」并给了 `；COM-24` 的前缀。`；` 前缀只有在并入既有枚举时才成立；若按字面追加到整行最末，会得到 `……核对后使用。；COM-24 …` 这种断句不成立的形式。故取「枚举末尾」。如需字面意义的整行最末，一行即可改回。
- **为什么**：本次在 L44 新引入一条事实性断言（`hass-cli` 存在、由 Home Assistant Ecosystem 组织维护）。本册自述「每条事实性结论都标注来源档位」，不给它挂来源就违反本册引用纪律——因此这是**补正的收尾**，非可选美化。此项关闭了上一版报告的**遗留问题 1**。
- **新 ID 只用 `COM-24`**：已实测 `workspace/hermes-home-assistant/` 全域 `COM-01`–`COM-23` 全部占用（23 个唯一 ID，见 `02_deep_research.md` L121–L144 的 COM 表），**24 为下一个空闲号，无撞号**。未另编任何新 ID。
- **数字纪律**：只写 `PyPI \`homeassistant-cli\` 1.0.0`（逐字取自 `source_bank.md` **D-2**「PyPI 版本 1.0.0」）。**未写** 596★、**未写** 2026-08-04 —— D-2 里都有，但父流程给的格式未含，且 `source_bank.md` **第 0 节**纪律是「不得自行新增数字」，故宁缺勿增。未引入第 2 节锁定数字集中任何一个。
- **Hub 侧证据按指示不另立来源**：正文「Hub 里也**有**封装它的 skill」的依据是 Hub 中央索引快照（`nousresearch.github.io/hermes-agent/docs/api/skills.json`，截至 2026-09-18），而该索引正是**已列的 HMS-05** 指过去的——按指示**未**为它编新 ID、**未**写成新的来源条目，段内也**未**另加散文说明句。
- **引用**：`source_bank.md` **第 7 节 D-2**（`home-assistant-ecosystem/home-assistant-cli`；PyPI `homeassistant-cli` 1.0.0）。

---

| # | 核对项 | 核对工具 / 位置 | 结果 |
|---|---|---|---|
| 1 | `official` 支 150 条，其 smart-home 分类只有 `openhue` | 快照 `sources\HUB-homeassistant-skills.json` → `smart_home_category_other`（13 条，其中仅 1 条 `source: optional`） | ✅ 成立；该条 `installCmd` = `hermes skills install official/smart-home/openhue` |
| 2 | `openhue` 的逐字英文描述 | 快照同条 `description` | ✅ 与原文逐字一致，故逐字保留 |
| 3 | 「bundled 里连 smart-home 分类都没有」 | 快照 `smart_home_category_other` 13 条中无 built-in / bundled 条目 | ✅ 成立，逐字保留 |
| 4 | 索引总数 97,986 | 快照 `total_index_records` | ✅ 成立（本篇**未**使用该数字） |
| 5 | 明示 HA 64 条 = ClawHub 52 + skills.sh 12 | 快照 `home_assistant_explicit`（len 64，`Counter` = ClawHub 52 / skills.sh 12） | ✅ 成立（本篇**未**使用该数字，留给 N01） |
| 6 | `clawhub/homeassistant-cli` 存在、`installCmd` 正确 | 快照同条 | ✅ 成立；其 `description` 自称 “the official hass-cli tool”，印证 `source_bank.md` 第 3 节的「措辞不精确，本册不沿用」判断 |
| 7 | `hass-cli` 归属 Home Assistant Ecosystem、非 HA core 官方、社区事实标准 | `source_bank.md` **D-2**（GitHub `home-assistant-ecosystem/home-assistant-cli`，596★，pushed 2026-08-04，未归档；PyPI `homeassistant-cli` 1.0.0） | ✅ 按锁定措辞引用 |
| 8 | Hub 的搜索由联邦索引回答、8 类源 | `source_bank.md` **D-4**（HMS-05 `website/docs/user-guide/features/skills.md` L708 起 `## Skills Hub`） | ✅ 成立；HMS-05 已在本章「本章来源」内，故未新增来源行 |
| 9 | `homeassistant-ai/skills` / `home-assistant-best-practices` | 快照同条 + `source_bank.md` **D-3** | ✅ 成立（本篇**未**使用，属 N01 新增节内容） |
| 10 | ch01 内是否存在指向 ch03 新节的编号交叉引用 | `grep -n "第 3 章\|3\.2\|3\.3\|3\.4"` | ✅ 只有两处「第 3 章」（L44、L246），**无** `3.x` 数字编号引用 → N01 的 3.2–3.5 顺延不影响本章，本章也无需改号 |
| 11 | ch01 内是否已有 `[[双链]]` | `grep -n "\[\["` | ✅ 零命中；本次**未新增任何双链**，不存在「指向不存在笔记」的风险 |
| 12 | 脚注 | 通读 | 本章无脚注定义与引用；本次未新增/删除脚注 |
| 13 | 计划行号口径 | 对比发布源与 vault 分册 | ⚠️ 计划第 4 节 N02 的行号是**分册行号**（= 发布源 + 15），已按内容锚点重新映射（L55→L40、L57→L42、L59→L44、L62→L47、L267→L252），5 行**全部命中、无漏列** |
| 14 | 写盘安全 | 应用脚本断言 | ✅ `changed == [40,42,44,47,252,262]`（重跑后）；输出 262 行、LF、UTF-8 无 BOM；临时脚本执行后已删除 |
| 15 | **COM-24 是否为下一个空闲号** | `grep -rhoE "COM-[0-9]{2}"` 遍历 `workspace/hermes-home-assistant/**.md,\*.json` | ✅ 命中且仅命中 `COM-01`…`COM-23` 共 23 个唯一 ID，`COM-24` 零命中 → 24 空闲，无撞号 |
| 16 | 输出内是否出现计划外的新 ID | 对 `updated_note.md` 全文正则抽取 `(SRC\|HMS\|HAS\|COM)-\d+` | ✅ 仅 `COM-01 / COM-23 / COM-24 / HMS-03 / HMS-05 / SRC-01 / SRC-02 / SRC-10`；新引入的只有 `COM-24` |
| 17 | L262 插入锚点唯一性 | 断言 `lines[261].count(anchor) == 1` | ✅ 锚点唯一，替换恰好发生一次；段末「场景表来自……」句逐字保留 |

**实际核对过的来源 ID**：`source_bank.md` 第 2 节（数字锁）、第 3 节（措辞锁）、第 6 节（禁令）、**D-2**（`hass-cli`）、**D-4**（HMS-05）、**D-3**（`homeassistant-ai/skills`，仅核对未使用）；原始材料 `sources\HUB-homeassistant-skills.json`（`total_index_records`、`source_distribution`、`home_assistant_explicit`、`smart_home_category_other`）。

---

## 4. 遗留问题（本代理按计划做最小改动，未自行改方案）

1. ~~**「本章来源」（发布源 L262）出现来源缺口 —— 计划未列，未动。**~~
   **已处置（父流程追加批准）**：L262 已追加 `COM-24 \`home-assistant-ecosystem/home-assistant-cli\`（github.com/home-assistant-ecosystem/home-assistant-cli；PyPI \`homeassistant-cli\` 1.0.0）`，缺口关闭（见 §2.6）。原本要说明的是：正文新引入的两条事实性表述里，「Hub 的搜索由一份联邦索引回答」由**已列**的 HMS-05 覆盖，只有 `hass-cli` 缺条目。
   **残余提醒**：vault 分册此后不再是「发布源 + 15 行」的线性关系（分册 L277 就是 `### 本章来源` 段，插入只发生在这段内部，未新增行），行数关系不变，仍为 262 / 277 行。
2. **保留的 HMS-05 从句，语义角色已变。**
   L42 保留了「（HMS-05）全文未出现 Home Assistant」。该句在原文里是「查无此物」的旁证；补正后它只能说明 HMS-05 没有 HA 专条（`source_bank.md` **D-4** 已证：原册结论**不来自** HMS-05 正文，而是只从 `optional-skills/` 目录清单推出）。按计划「保留该事实」逐字未动；若希望更显豁，可改写为「HMS-05 只描述联邦索引机制、不含 HA 专条」——**超出计划范围，未做**。
3. ~~**计划行号口径未注明，易导致错位改动。**~~
   **已采纳（父流程回填）**：计划 §4 现加了口径说明——计划/P1 清单行号一律是「已发布分册」行号，发布源 = 分册 − 15，并附换算实测（N02 即 L55/57/59/62/267 → L40/42/44/47/252）。本报告与 `diff_check.txt` 均按此双口径标注（追加行：分册 L277 → 发布源 L262）。
4. **`official` 的字段别名。**
   `source_bank.md` 第 2 节与计划称 `official` 支；快照里该支的 `source` 字段实际取值是 **`optional`**（150 条），而 `openhue` 的 `installCmd` 是 `hermes skills install official/smart-home/openhue`。本篇按锁定措辞写「`official` 支」（installCmd 命名空间佐证），**未**自行改写快照字段名。若下游需要精确对齐字段名，需先回到锁文件更新措辞。
5. **本篇不出现任何锁定数字，故无时点限定句。**
   97,986 / 64 / 52 / 12 / 13 / 150 均未在 ch01 出现（数字与清单留在 N01 新增节）。这是**刻意的**：计划第 4 节 N02 表只要求「加范围限定」，不要求给数字；而若在 ch01 落数字，就必须同句带「截至 2026-09-18 的 Hub 中央索引快照」。**追加改动没有改变这一点**：L262 新增的 COM-24 条目只含 PyPI 版本号 `1.0.0`（D-2 逐字），不属于第 2 节的锁定数字集；596★ 与 2026-08-04 按纪律**未写**。若父流程希望 ch01 也带数字，需同步补时点限定句。
6. **N02 ↔ N01 的措辞一致性只能单向保证。**
   本代理按 `source_bank.md` 锁定措辞落笔，**未读、未改** N01（`chapters\03-路线选型.md`）的任何文件。两章共用同一套锁定句（「联邦索引 / `official` 支 / `hass-cli` 归属 / 机器有（`hass-cli`）」）；若实际产物出现不一致，以 `source_bank.md` 为准，不要以任一篇的产物为准。
7. **发布源 / `output/final_note.md` / vault 分册三方漂移。**
   本次只产出 `updates\N02\updated_note.md`（LF，262 行）；发布源、`output\final_note.md`、vault 分册 `AI学习\Hermes Agent\Hermes × Home Assistant 实战\01-结论先行与能力地图.md` 在父流程重生成前**全部仍是旧文本**。vault 分册另带 12 行 frontmatter + 2 行导航（相差 15 行），不能直接把 `updated_note.md` 整篇盖过去，必须按 patch 应用。分册由外部进程每约 1 分钟 `vault backup` 自动提交，审计请以本目录副本 + `diff.patch` 为准。
8. **未执行的下游步骤（按分工留给父流程）**：`normalize_chapters.py`（本次改内容，**不得**再跑，契约边界见计划第 2 节）、`assemble_note.py`、`publish_volume.py`、hash 验收、MOC 同步（本篇未提供 `moc_path`）。

---

## 5. 产出物清单（`workspace\update-hermes-ha-volume\updates\N02\`）

| 文件 | 说明 |
|---|---|
| `stale_map.md` | 逐行 stale 定位（覆盖计划第 4 节 N02 全部 5 行；L59 拆为两处独立缺陷；第 6 行为追加批准的 L262） |
| `update_plan.md` | 逐行改法与依据（含 §2.6 追加项）、落笔前核对清单、验收方式 |
| `updated_note.md` | **整篇更新后的完整文件**（262 行，UTF-8 无 BOM，LF） |
| `diff.patch` | `difflib.unified_diff`（`ensure_ascii=False`，LF），3 hunk / 10 增 10 删（净 6 行替换） |
| `diff_check.txt` | 差异与作用域自检记录：双口径行号、hunk/增删计数、LF/BOM/围栏/标题/双链/脚注检查、COM-ID 命名空间核验、「无其他差异」声明 |
| `update_report.md` | 本文件 |

**本代理未改动**：`chapters\` 下任何文件、`workspace\workflow-runs\` 下任何文件、vault 分册、`output\final_note.md`、`source_bank.md`、`02_batch_update_plan.md`。发布源仍是原文。
