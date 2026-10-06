# N01 update report — `chapters/03-路线选型.md`

**执行者**：note-updater（N01 单元）
**日期**：2026-09-18
**模式**：`patch-in-place`（正文只写入本目录，发布源未被本单元改动）
**输入**：`02_batch_update_plan.md` §2、§4（N01 表）；`shared_research/source_bank.md` 全文；快照 `workspace/hermes-home-assistant/sources/HUB-homeassistant-skills.json`

## 0. 交付物与规模

| 文件 | 说明 |
|---|---|
| `stale_map.md` | 逐行 stale map（含计划未逐行列位的顺延标题） |
| `update_plan.md` | 具体改法 + 标题顺延清单 |
| `updated_note.md` | 整篇更新后的完整文件（UTF-8、LF、无 BOM，354 行） |
| `update_report.md` | 本文件 |
| `diff.patch` | `difflib.unified_diff`（`n=3`，UTF-8 直出中文、未转义，行尾 LF；已用独立 applier 验证可**无损重建** `updated_note.md`） |
| `diff_check.txt` | 父流程验收器 `verify_update.py` 的输出（行位白名单机械复核） |

**改动规模**：

- 改动 hunk 数：**7**（`diff.patch` 的 `unified_diff(n=3)` 口径）／ **11**（父验收器 `SequenceMatcher(autojunk=False)` 的差异块口径，对应 11 个被改行位）。两个口径在收尾改动前后**均未变化**。
- diff 口径新增行数：**91**；diff 口径删除行数：**14**（`unified_diff` 口径，净 +77 行 = 277 → 354 行）
- 验收器口径：合计删除 **11** 行 / 新增 **88** 行（= 11 个既有行位 1:1 重写 + 77 行插入）
- 语义口径：**11 个既有行位被重写**（1:1 替换）＋ **77 行插入**（新增节 76 行正文 + 1 行分隔空行）。`unified_diff` 口径比语义口径各多 3 行，原因是 hunk 1 把「L19 段 + 空行 + L21 标题」三行整体划入替换块，其中空行与标题行被计为「删除 + 新增」而非上下文。
- **收尾扩展（父流程批准，见 §1 表第 13–14 行）不改动行位数、不新增 hunk**：两处都落在既有 11 个行位（L19 与 L277）内部，因此各口径计数在上表已合并呈现，未单独膨胀。

## 1. 逐处改动与依据

行号一律为**发布源行号**；`计划行 = 发布源行 + 15`。

| # | 发布源行 | 计划行 | 改了什么 | 为什么 | 引用的 source_bank 条目 |
|---|---|---|---|---|---|
| 1 | L19 | L34 | 整段重写。原「**Skills Hub 里没有现成的 Home Assistant skill**…smart-home 分类下只有 `openhue` 一个，其余为空…是**没有可装的东西**」→「**Skills Hub 的搜索由一份联邦索引回答**，`official`…只是其中一支」＋ 97,986 / 64 / 52+12 / 150 四个锁定数字 ＋ 前指 3.2、后指 3.3 | 第一层补正：原文把 `official` 支（150 条）当成了整个 Hub，并据此得出「没有可装的东西」；两层都必须从同一句里拆开 | §1（固定时点限定「截至 2026-09-18 的 Hub 中央索引快照」，照抄）、§2（97,986 / 64 / 52 / 12 / 150）、§3「关于 Hub 是什么」、§6 禁令 1 |
| 2 | L21 | L36 | `### 3.2 为什么自建 SKILL.md 补不了能力` → `### 3.3 …` | 新增 3.2 占位，原 3.2–3.5 顺延 | 计划 §4「新增 `### 3.2`」行 |
| 3 | L49 | L64 | 整段重写。原「**HA 场景不存在一个可调的 `ha` CLI**」→「HA 场景**有**可调的 CLI，只是它不叫 `ha`」＋ `home-assistant-ecosystem/home-assistant-cli`、HA Ecosystem 组织、社区事实标准、**不是 HA core 官方出品**、596★ / 未归档 / 核实于 2026-09-18 ＋ `clawhub/homeassistant-cli`（见 3.2） | 第二层补正：这一句是本次要推翻的事实错误；措辞必须精确到「Ecosystem ≠ core 官方」 | §3「关于 `hass-cli`」（逐字）、§6 禁令 1 与禁令 2、§7 D-2 |
| 4 | L52 | L67 | `3.3 或 3.4` → `3.4 或 3.5` | 新增节导致顺延 | 计划 §4「L67」行 |
| 5 | L93 | L108 | 只改大白话 tip 末句：「而实际是**机器根本还没到货**」→「**机器有**（`hass-cli`），但**说明书得自己找**——Hub 里有，就是 3.2 列的那几条」 | 原末句在补正后不再成立；说明书/零件的比喻骨架按计划保留 | 计划 §4「L108（大白话）」行；§3「关于洞察的保留」 |
| 6 | L95 | L110 | `### 3.3 MCP 接线的硬规则` → `### 3.4 …` | 顺延 | 计划 §4 新增节行 |
| 7 | L180 | L195 | `### 3.4 自定义 plugin 的适用面` → `### 3.5 …` | 顺延 | 同上 |
| 8 | L238 | L253 | `### 3.5 落点决策表` → `### 3.6 …` | 顺延 | 同上 |
| 9 | L240 | L255 | `把 3.1 到 3.4 收成一张表` → `把 3.1 到 3.5 收成一张表` | 顺延（新 3.2 计入区间） | 计划 §4「L255」行、§6 第 3 条 |
| 10 | L264 | L279 | 本章小结该条改半句。原「HA 场景不存在可调的 `ha` CLI，所以…」→「HA 场景也一样，**有**可调的 CLI（`hass-cli`），Hub 里也**有**封装它的 skill，所以准确的说法是「skill 这条路上游**有东西可装**，但它们**不提供新能力**」——…」 | 同 3；并把结论换成锁定的两段式 | §3「关于 `hass-cli`」「关于洞察的保留」、§6 禁令 1 |
| 11 | L277 | L292 | 本章来源：`（skills 定义；smart-home 仅 `openhue`）` → `（skills 定义；Hub 为联邦索引、支持 8 类来源，**official 支** smart-home 仅 `openhue`）`；并在 `SRC-07 …` 之后追加 Hub 中央索引（URL ＋ 时点限定 ＋ 本地快照路径） | 原文那句**本身没错**，错在范围；按锁定措辞收窄到 `official` 支，并补齐新数字的来源位 | §3「关于原册那层事实」、§2（8）、§7 D-1（URL 与快照路径） |
| 12 | 插入于 L20/L21 之间 | 新增节 | 新增 `### 3.2 Hub 里现成可装的 HA skill 清单`，76 行 | 计划 §4 骨架 1–5 点 | §1、§2、§3、§4、§5、§6、§7 D-1/D-2/D-3/D-5 |
| 13 | L19（**收尾扩展 ①**，同属上表第 1 行的行位） | — | `而**原册**据以立论的那一支` → `而**先前**据以立论的那一支`（同段其余文字逐字不动） | **术语对齐**：实测本分册全文「原册」出现 0 次，本册自称统一用「本轮」（`02` 6 次、`03` 2 次），而「本轮」在册中意为「本次修订」，用在此处语义不对。父流程要求改用「先前」，且不引入新的自称词 | 父流程收尾指令（对已批准计划的扩展）；不涉及 source_bank 条目 |
| 14 | L277（**收尾扩展 ②**，同属上表第 11 行的行位） | — | 本章来源段落**末尾追加两条**：`COM-24 `home-assistant-ecosystem/home-assistant-cli`（github.com/home-assistant-ecosystem/home-assistant-cli；PyPI `homeassistant-cli` 1.0.0）；COM-25 `homeassistant-ai/skills`（github.com/homeassistant-ai/skills；749★，pushed 2026-09-16；遵循 Agent Skills 标准 agentskills.io）。` | **补齐来源**：正文这轮新引入的事实性断言（`hass-cli` 的存在与归属、`homeassistant-ai/skills` 的星数与标准）在来源列表里没有对应条目，而本册 README 自述「每条事实性结论都标注来源档位」——补正是补正本身的收尾，非可选美化。这正是本报告上一版遗留问题 1 | §7 D-2（PyPI 版本 1.0.0）、§7 D-3（749★、pushed 2026-09-16、Agent Skills 标准 agentskills.io）；编号 `COM-24`/`COM-25` 由父流程实测 `COM-01…COM-23` 全占用后指定 |

> 来源编号核对：`updated_note.md` 全文出现的来源 ID 为 `HMS-03 / HMS-04 / HMS-05 / HMS-06 / HMS-07 / HMS-10 / HMS-11 / HMS-12 / SRC-04 / SRC-07 / COM-24 / COM-25`。**本轮新增的 ID 只有 `COM-24`、`COM-25` 两个**；未为 Hub 中央索引另编 ID（`HMS-05` 那条的括号说明已承担该职责，`HMS-05` 条目本身逐字未再改动）。

### 新增节里逐字引用的锁定内容

- **时点限定**（§1 固定写法，出现 3 次）：「截至 2026-09-18 的 Hub 中央索引快照」。
- **锁定数字**（§2）：97,986、64、52、12、13、150、8 类来源（八类名逐字：`official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh`）。除 §2/§7 明确给出的数字（749★、pushed 2026-09-16、4762★、596★、请求 404）外**未新增任何数字**。
- **锁定措辞**（§3）：「关于 Hub 是什么」句、「关于原册那层事实」句、「关于 `hass-cli`」句、「关于洞察的保留」句、「关于 `homeassistant-ai` 这个组织」的接点句；收尾用计划 §4 骨架第 5 点的两段式。
- **锁定命令**（§4）：A 级 1 条 + B 级 11 条 + C 级 14 条，共 **26** 条 `hermes skills install …`，逐字取自 §4 命令表（未从快照自行增补命令；D 级与小米/小爱系只写条目名、**不给**安装命令，因为它们不在 §4 表内）。
- **分级判据**（§5）：A / B / C / D 四级的判据文字与代表条目一一对应。
- **禁令与注意事项**（§6）：D 级明确写「来源存疑、未验证」并加粗「**不把它当官方出品。**」；纪律第 2 条写「只有名字与作者、无描述」并给 `hermes skills inspect`；第 3 条写「ClawHub 是开放注册表，有重复件与凑数件」。

## 2. 做过的核对动作

1. **发布源 ↔ 分册正文等价性核对**：`difflib.unified_diff` 比对 `chapters/03-路线选型.md`（277 行）与分册 `03-路线选型.md`（292 行），差异**只有** frontmatter/nav/`#` 标题 15 行与 9 处标题层级（`###` ↔ `##`）。据此确认「计划行号 = 发布源行号 + 15」全文恒定，并确认正文可 1:1 迁移。
2. **计划 §4 N01 表逐行覆盖核对**：11 个内容行位全部命中真实文本（L19 出发点、L49 `ha` CLI、L52 与 L240 交叉引用、L93 大白话、L264 小结、L277 来源，加 4 个顺延标题），无偏移、无空行。
3. **交叉引用全量复核**：对**全文 277 行、不加任何行号范围过滤**执行 `3\.\d` 扫描，命中仅 5 个既有标题 + L52 + L240；除计划列的 2 处外无其他 3.x 引用。**本条特意复现了计划 §6 第 3 条自曝的「范围过滤会连真命中一起滤掉」的错误场景，本次未使用任何行号范围过滤。**
4. **原件核对（快照）**：`sources/HUB-homeassistant-skills.json` 逐条核对——`total_index_records = 97986`、`home_assistant_explicit` 长度 = **64**、`smart_home_category_other` 长度 = **13**（其中 `openhue` 一条，快照里 `source: optional`、`installCmd: hermes skills install official/smart-home/openhue`）。逐条核对新增节引用的每一条 `installIdentifier` 与 `installCmd`（A 级 1 条、B 级 11 条、C 级 14 条；D 级 4 条 bullet 涉及 6 个标识 `oo-home-assistant` / `home-assistant` / `homeassistant-selora` / `home-assistant-backup` / `homeassistant-toolkit` / `skills-sh/home-assistant/core/home-assistant-integration-knowledge`；小米/小爱系 2 个标识 `clawhub/xiaomi-home-assistant-skill` / `clawhub/xiaoai-ha-control`）**全部存在**，26 条安装命令逐字一致。
5. **措辞交叉核对（快照 ↔ source_bank）**：`clawhub/homeassistant-cli` 的快照 `description` 确实自称 “the official hass-cli tool”——与 §6 禁令 2 的警告一致，新增节**未沿用** Hub 条目自述，改用 §3 的锁定措辞。`clawhub/home-assistant` 与 `clawhub/home-assistant-backup` 的 `description` 逐字相同、三个条目 `name` 同为 `Home Assistant`、`clawhub/homeassistant-toolkit` 的模板腔描述——均在快照中逐一验证。
6. **禁令扫描**：对 `updated_note.md` 全文扫描，「不存在一个可调的」「不存在可调的」「没有现成的 Home Assistant skill」「没有可装的东西」「官方 hass-cli」命中均为 **0**；「官方出品」命中 2 次，两处均为**否定式**（「**不是 HA core 官方出品**」「**不把它当官方出品。**」）。
7. **改动范围机械验证**：把 11 个被改行位之外的全部行逐一与原文比对，**mismatches = 0**；`[[` 命中 0（未新增任何双链）；代码围栏 18 个（偶数、配对，= 原 12 + 新增 6）。
8. **diff 可应用性验证**：用独立实现的 unified-diff applier 应用 `diff.patch`，重建结果与 `updated_note.md` **逐字节相等**。
9. **文件形态验证**：`updated_note.md` / `diff.patch` / `diff_check.txt` 均 `\r` 计数为 **0**（纯 LF），UTF-8 无 BOM。
10. **行位白名单机械复核（收尾改动后重跑）**：用 `SequenceMatcher(autojunk=False)` 取全部非 equal 块，断言每块的**旧侧行号集合 ⊆** 允许位 `{19, 21, 49, 52, 93, 95, 180, 238, 240, 264, 277}`，并用「equal 块照抄 + 非 equal 块替换」重建全文——结果：非 equal 块 **11** 个、**越界块 0** 个、重建结果与实际 `updated_note.md` **逐行相等**、11 个允许位**全部被触及且无遗漏**。这等价于证明「除这 11 个行位外没有任何差异」。
11. **父流程验收器复核**：运行 `verify_update.py N01 --allow-hunk 19-21 / 49-49 / 52-52 / 93-95 / 180-180 / 238-240 / 264-264 / 277-277`，输出 `diff_check.txt`：11 个差异块**全部** `✅ 在允许区内`，`## 问题 - 无`，合计删除 11 行 / 新增 88 行，发布源与 P4 预检基线 sha256 **一致**（本单元未改动发布源）。
12. **术语扫描**：收尾后全文「原册」计数 **0**、「先前」1（即改动处）、「本轮」2（均在本册原有语境，未新增）。

## 3. 其他差异声明

> **除计划第 4 节 N01 表列出的 11 个行位，以及计划指定的新增小节（`### 3.2`，含其导致的 4 个既有标题改号与 2 处交叉引用顺延）之外，`updated_note.md` 与原文之间没有其他任何差异。**
>
> **收尾扩展不改这条结论**：父流程批准的两处收尾改动（① L19 术语对齐、② L277 本章来源追加 `COM-24`/`COM-25`）都**落在上述 11 个行位内部**，**没有引入任何新的行位、新的 hunk 或新的差异块**；新增的 3.2 小节内容本轮**一字未动**。
>
> 验证方式（收尾后重跑）：① 行位白名单机械比对——非 equal 块 11 个、越界 0 个、重建全文逐行相等（第 2 节第 10 条）；② 父验收器——11 个差异块全部在允许区内、问题 0（第 2 节第 11 条）。

## 4. 遗留问题（未自行改方案，按计划最小改动，交父流程/用户裁决）

1. ~~**【来源缺口】新增节引入的事实未在本章来源声明中登记。**~~ → **已解决（收尾扩展 ②）**。父流程采纳本项并指定编号，已在 `本章来源` 末尾追加 `COM-24`（`home-assistant-ecosystem/home-assistant-cli`；PyPI `homeassistant-cli` 1.0.0）与 `COM-25`（`homeassistant-ai/skills`；749★，pushed 2026-09-16；Agent Skills 标准 agentskills.io）。两处数字均与 source_bank §7 D-2 / D-3 逐字一致。
   - 残留小项（不阻塞）：正文 L49 写了 `hass-cli` 的 **596★、未归档**，而 `COM-24` 条目按父流程给定格式**未含星数**。两者不冲突（条目是最小来源声明，星数留在正文），故未追加；若 P4 希望条目与正文对齐，可再补。
   - 残留小项（不阻塞）：`COM-24` / `COM-25` 两条追加在**整个段落末尾**（即既有那条 `openhue` SKILL.md 采集说明之后），这是对「段落末尾追加两条」的字面执行；若父流程更希望它们紧接在 `SRC-07` / Hub 中央索引条目之后、把末句保留为收尾，只需移动位置，内容不变。
2. **【计数口径】计划写「原 3.2–3.5 顺延为 3.3–3.6（5 个标题 + 2 处交叉引用）」，但既有需要改号的只有 4 个标题**（3.2→3.3、3.3→3.4、3.4→3.5、3.5→3.6），第 5 个是**新增**的 3.2 本身。已按 4 个既有点位执行（新增节算第 5 个），未改方案。
3. **【编号解读】计划 §4 新增节骨架里 B 级那行写「与第 3.3–3.5 三条路线一一对应」**，该范围只有按**改后**编号才成立（3.3 = skill、3.4 = MCP、3.5 = plugin）。新增节据此写成「正好对应 3.3–3.5 的三条路线」；若计划本意是改前编号，则该句应改为 3.2–3.4，请裁决。
4. **【可选一致性】L51 的 bullet「如果能力**已经**由别的方式提供了（比如你自己写了一个包装 HA REST 的脚本、或用 `curl` + 长期令牌），那 SKILL.md 是**恰当的**」** 在补正后仍成立、无矛盾，但也**没有**把 `clawhub/homeassistant-cli` 这个现成例子并进去。计划把 L51 划入保留区间，故未动；若要强化论证，可在 P4 追加半句（属内容扩写，超出本单元授权）。
5. **【字段命名差异，数字一致】快照把 `official` 那一支在 `source` 字段里记作 `optional`**（`source_distribution` 为 `optional: 150`、`built-in: 58`），而同一快照里 `openhue` 的 `installCmd` 写的是 `hermes skills install official/smart-home/openhue`，source_bank §2/§3 也一律用 `official`。**数字（150 / 58）两侧一致，仅字段命名不同**。本单元按 source_bank 的锁定措辞统一写 `official`；若 P4 收尾要用快照字段名做 grep 核对，需注意这一处别名，不要把「快照没有 `official` 关键字」误判成数字错误。
6. **【计划已排除】`chapters/../02_deep_research.md`、`01_explore_result.md` 的勘误属 N03/N04**，本单元未触碰；`00_intent.md`、`03_outline.md`、`research/probe-*.md` 亦未触碰。
7. **【未执行】`normalize_chapters.py` / `assemble_note.py` / `publish_volume.py` 均未运行**（父流程负责）。新增节已**直接写成最终形态**：`###` 小节标题层级与源文件既有 N.M 小节一致，未新增/删除脚注定义，未新增 `[[双链]]`（全文仍 0 个，`publish_volume.py` 的双链存在性断言不受影响）。

## 5. vault / workspace 漂移登记

本单元的产出**只写入** `workspace/update-hermes-ha-volume/updates/N01/`，**发布源与分册两侧都还没变**：

| 位置 | 当前状态 |
|---|---|
| 发布源 `workspace/hermes-home-assistant/chapters/03-路线选型.md` | **未改动**（仍含错误的 L19 / L49 / L264 表述），等待父流程应用 `updated_note.md` |
| 分册 `AI学习/Hermes Agent/Hermes × Home Assistant 实战/03-路线选型.md` | **未改动**，且与发布源正文逐字相同（仅标题层级 + frontmatter/nav 不同） |

**漂移风险**：父流程若只应用发布源而重跑 `publish_volume.py`，分册会随之更新、漂移消失；若跳过 `publish`，则分册会长期停留在旧表述（含被本次判定为**事实错误**的那句）。本单元按 `destination_mode: patch-in-place` 不自行回写任何一侧。另注：计划 §6 第 7 条已记录分册会被外部进程约每分钟自动 `vault backup` 提交，审计以本目录副本为准。
