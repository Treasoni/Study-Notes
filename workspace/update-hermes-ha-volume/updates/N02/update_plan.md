# N02 更新计划 — `chapters/01-结论先行与能力地图.md`

- **Note ID**：N02 ｜ **动作**：`update`（局部 patch，非重写）
- **destination_mode**：`patch-in-place`（父流程把本目录的 `updated_note.md` 应用到发布源；本代理**未**改动发布源、未改动 `chapters/` 下任何文件）
- **目标（发布源）**：`D:\Study-Notes\workspace\hermes-home-assistant\chapters\01-结论先行与能力地图.md`
- **措辞与数字锁**：`workspace\update-hermes-ha-volume\shared_research\source_bank.md`（第 1、2、3、6、7 节）

## 1. 改动边界

- **只改 6 行**：发布源 L40、L42、L44、L47、L252（= 计划第 4 节 N02 表的 L55、L57、L59、L62、L267，分册行号 = 发布源行号 + 15）**＋ 父流程追加批准的 L262（分册 L277）**。
- 其余 **256 行逐字节不变**（含标点、全角符号、空行、代码围栏、行尾）；文件行数不变（262 行）、小节编号不变、无新增/删除小节。
- **不新增数字**：本篇不出现 97,986 / 64 / 52 / 12 / 13 / 150 中的任何一个，因此不涉及时点限定句；数字与清单留在 N01（`03-路线选型.md`）新增节。
- **不列命令**：本篇不写 `hermes skills install …`，保持「结论先行」章的结论式表述（可装 ≠ 能补能力），避免与 N01 的清单重复。
- **不新增 `[[双链]]`**、不新增或删除脚注、不改 `###` 标题层级、不改「本章来源」行。
- 输出行尾统一 LF，UTF-8 无 BOM。

## 2. 逐行改法

### 2.1 发布源 L40（结论二标题）— 重写

- 旧：`**结论二：「装个现成 skill 就能用」在 HA 场景不成立。**`
- 新：`**结论二：Hub 里有可装的 HA skill——但可装不等于能补能力。**`
- 依据：计划第 4 节 N02 L55「改为准确表述（可装 ≠ 能补能力）」；`source_bank.md` 第 6 节禁令 1。
- 保留性：仍然是**结论式**一句话，不变成清单。

### 2.2 发布源 L42（第一层依据）— 加范围限定 + 点明联邦索引

- 「第一层是**事实**核对」→「第一层是**范围**核对」（对齐计划第 1 节「第一层（范围错）」的诊断）。
- 「Hermes 官方 optional skills 目录的」→「**official 支**（Hermes 仓库内的 optional skills）的」（对齐 `source_bank.md` 第 3 节的锁定叫法）。
- 该行前半段其余文字**逐字保留**：`openhue`、「只有一个条目」、逐字英文描述、bundled 无 smart-home 分类、HMS-05 全文未出现 Home Assistant。
- 行末**追加**范围限定与联邦索引说明，取自 `source_bank.md` 第 3 节「关于 Hub 是什么」的锁定措辞：
  > Skills Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表（skills.sh、ClawHub、LobeHub、browse.sh、well-known 端点、GitHub taps）；`official`（Hermes 仓库内的 optional/bundled skills）只是其中一支。
- 收尾一句把范围说死：「「Hub 里只有 `openhue` 一个」这句话，说的只是它。」

### 2.3 发布源 L44（第二层依据）— 换举证，不换结论

- **删除**：`；而 HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI`（计划第 4 节 N02 L59 明确要求删）。
- **替换为** `source_bank.md` 第 3 节「关于 `hass-cli`」的锁定措辞：
  > `hass-cli` 指的是 `home-assistant-ecosystem/home-assistant-cli`——**Home Assistant Ecosystem 组织**维护的命令行工具，是社区里的事实标准，**不是 HA core 官方出品**（Hub 里 `clawhub/homeassistant-cli` 条目的自述称其为 “official”，措辞不精确，本册不沿用）
- 并补一句「Hub 里也**有**封装它的 skill（`clawhub/homeassistant-cli`）」（`source_bank.md` 第 3 节「关于洞察的保留」）。
- **重写末句**：「所以「搜一个 HA skill 装上」这条路，在能搜到的那一刻之前就已经断了」→「所以这条路的准确说法不是「搜不到」，而是「搜得到、装得上，但装完仍然**不提供新能力**」」。
- **逐字保留**：`**skill 不是能力，是知识**` 与「它教 agent 怎么调已有的工具，不新增工具」；以及「这里只点一句、第 3 章展开」这句前向指引（第 3 章本次会新增 3.2 节，指引仍然成立）。

### 2.4 发布源 L47（大白话末句）— 换落点，保留隐喻

- 旧末句：`HA 场景现在缺的是机器，不是说明书。`
- 新末句：`机器有（\`hass-cli\`），说明书得自己找——Hub 里有；但说明书再全，机器还是那几台。`
- 依据：计划第 4 节 N02 L62「大白话末句改」；与 N01 L108 计划用同一句「机器有（`hass-cli`）」，保持同批措辞一致。
- 保留：`把 skill 想成一份「岗位说明书」：……但不会凭空给你添一台新机器。` 逐字不动。

### 2.5 发布源 L252（本章小结对应条目）— 重写

- 旧：`- 「装个现成 HA skill」这条路不存在：官方 optional skills 的 smart-home 分类下只有 \`openhue\` 一个，而 skill 本身也不提供新能力。`
- 新：`- 「装个现成 HA skill」这条路**有东西可装**，但**可装不等于能补能力**：Hub 的搜索由一份联邦索引回答，「只有 \`openhue\` 一个」说的只是 \`official\` 支；skill 本身仍然只是知识，不提供新工具。`
- 依据：计划第 4 节 N02 L267；`source_bank.md` 第 3 节两条锁定措辞。
- 小结其余 4 条、以及小节标题 `### 本章小结` 不动。

### 2.6 发布源 L262（`### 本章来源`）— 追加 COM-24【父流程追加批准】

- **性质**：**对已批准计划的扩展**（父流程决定；原计划第 4 节 N02 表未列此行）。理由：本次在 L44 新引入一条事实性断言（`hass-cli` 存在、由 Home Assistant Ecosystem 组织维护），本册 README 自述「每条事实性结论都标注来源档位」，不给它挂来源就违反本册引用纪律——这一条是补正的收尾，不是美化。
- **插入位置**：来源枚举内、`COM-23 …（homeassistant-ai.github.io/ha-mcp/setup/）` 之后、`。场景表来自` 之前。即 `；COM-24 …` 的 `；` 与枚举既有的分隔符同形，段末的「场景表来自……」收尾句仍居末位。
  > 说明：`；` 前缀意味着新条目并入既有枚举；若真按「整行最末」追加会得到 `……核对后使用。；COM-24 …` 这种断句不成立的形式，故取枚举末尾。若父流程要求的是字面意义的整行最末，请指出，可一行改回。
- **新增文本（逐字）**：`；COM-24 \`home-assistant-ecosystem/home-assistant-cli\`（github.com/home-assistant-ecosystem/home-assistant-cli；PyPI \`homeassistant-cli\` 1.0.0）`
- **编号**：只用 **COM-24**。已实测 `workspace/hermes-home-assistant/` 全域 `COM-01`…`COM-23` 全部占用（23 个唯一 ID），24 为下一个空闲号，无撞号。
- **数字纪律**：只写 `PyPI \`homeassistant-cli\` 1.0.0`（`source_bank.md` **D-2** 逐字）；**不写**星数、不写 pushed 日期（D-2 有 596★ / 2026-08-04，但父流程给的格式未含，且第 0 节纪律为「不得自行新增数字」→ 宁缺勿增）。
- **Hub 侧证据不另立来源**：正文「Hub 里也**有**封装它的 skill」的依据是 Hub 中央索引快照（截至 2026-09-18），而该索引正是**已列的 HMS-05** 指过去的——只属指路，**不编新 ID**、**不写成新来源行**，也未在段内另加散文句。
- **逐字保留**：枚举中既有 `SRC-01` / `SRC-02` / `SRC-10` / `HMS-03` / `HMS-05` / `COM-01` / `COM-23` 及其路径与 URL 写法；段末「场景表来自 `research/probe-03-scenarios.md`，该表不在 canonical 注册表内，本章按其原文逐行核对后使用。」一字不动。

## 3. 落笔前的核对清单（执行时逐条做过，结果见 `update_report.md`）

| # | 要核对的表述 | 核对处 | 结论 |
|---|---|---|---|
| 1 | `official` 支 150 条、其 smart-home 分类只有 `openhue` | 快照 `smart_home_category_other` | 成立（该条 `installCmd` = `hermes skills install official/smart-home/openhue`，`source` 字段写作 `optional`） |
| 2 | `openhue` 的逐字描述 | 快照同条 `description` | 与原文逐字一致 |
| 3 | Hub 是联邦索引、8 类源 | `source_bank.md` D-4（HMS-05 L708 起 `## Skills Hub`） | 成立 |
| 4 | 64 条明示 HA、52 + 12 拆分 | 快照 `home_assistant_explicit` | 成立（本篇**未**使用该数字） |
| 5 | `hass-cli` / `home-assistant-ecosystem/home-assistant-cli` 存在，非 HA core 官方 | `source_bank.md` D-2 | 成立（本篇按锁定措辞引用） |
| 6 | Hub 里有封装 `hass-cli` 的 skill | 快照 `clawhub/homeassistant-cli`（`installCmd` = `hermes skills install clawhub/homeassistant-cli`） | 成立 |
| 7 | 「bundled skills 目录里连 smart-home 这个分类都还没有」 | 快照 `smart_home_category_other` 13 条中无 bundled/built-in 条目 | 成立，逐字保留 |

## 4. 验收

- 用脚本（执行后已删除）按行号替换（含追加的 L262），并断言：除 L40/42/44/47/252/**262** 外**无任何行差异**、总行数仍 262、输出为 LF/UTF-8 无 BOM。
- 产出 `diff.patch`（`difflib.unified_diff`，`ensure_ascii=False`，LF）与 `diff_check.txt`（差异与作用域自检记录）。
- **不跑** `normalize_chapters.py` / `assemble_note.py` / `publish_volume.py`（父流程负责）；不改 `chapters/`、不改 `workspace/workflow-runs/`。
