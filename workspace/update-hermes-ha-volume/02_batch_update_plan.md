# 批量更新计划 — `update-hermes-ha-volume`

**阶段**：P2 ｜ **机制**：甲（用户已确认）｜ **批大小**：2 ｜ **产出**：本文件

## 1. 更新目标与判断依据

**目标**：把「Skills Hub 里没有现成的 Home Assistant skill / 没有可装的东西」这一**事实性错误结论**从分册与两份研究档中补正，并在第 3 章新增一节给出 Hub 里**真实可装**的 HA skill 清单。

**判断依据**（2026-09-18，全部可复验；详细证据见 `00_batch_update_intent.md`）：

| 事实 | 值 | 取回方式 |
|---|---|---|
| Hub 中央索引条目 | 97,986 | `nousresearch.github.io/hermes-agent/docs/api/skills.json` |
| 明示 HA 的 skill | **64** 条（ClawHub 52 + skills.sh 12） | 同上，快照 `sources/HUB-homeassistant-skills.json` |
| smart-home 分类、未点名 HA | 13 条 | 同上 |
| official 支（150 条）中的 smart-home | **确实只有 `openhue`** | 同上 |
| `hass-cli` | `home-assistant-ecosystem/home-assistant-cli`，596★，2026-08-04 pushed，未归档；PyPI `homeassistant-cli` 1.0.0 | GitHub API |
| `homeassistant-ai/skills` | 749★，2026-09-16，含 `home-assistant-best-practices` | GitHub API + README 原文 |

**错误的两层结构**（补正必须分开处理，不能一锅端）：

- **第一层（范围错）**：把「Hermes 仓库内 `optional-skills/` 目录」（= 索引里的 `official` 支）当成了整个 Skills Hub。**HMS-05 自己就写着 Hub 是联邦注册表**，这一层错在没读全自己的来源。
- **第二层（事实错）**：断言「HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI」。`hass-cli` 存在，Hub 里 `clawhub/homeassistant-cli` 正是包它的。

**必须保留的部分**：「**skill 是知识，不是能力**」这条洞察成立，是本册骨架。补正方向是把它用在正确的地方——Hub 里的 HA skill 主要是**知识件**与**既有能力路径的封装**（最佳实践 / `hass-cli` 封装 / Assist API 封装 / MCP 桥 / HAOS 运维），而不是「凭空补能力」。

## 2. 机制甲的执行链（含一处脚本契约边界）

**编辑对象 = `workspace/hermes-home-assistant/chapters/*.md`（发布源）。分册与 `output/final_note.md` 是重生成产物，不手工改。**

链条（`normalize → assemble → publish`，均已确认 I/O）：

| 脚本 | 输入 → 输出 | 本轮的守卫作用 |
|---|---|---|
| `normalize_chapters.py` | `chapters/*.md` → 原地 | 归一到最终形态（`###` 小节标题、脚注体） |
| `assemble_note.py` | `chapters/` → `output/final_note.md` | 章标题数 / 目录条目 / 脚注定义与引用 / 代码围栏 断言 |
| `publish_volume.py` | `chapters/` → vault 分册 10 篇 + `README.md` | **小节标题层级一致性** + **全部 `[[双链]]` 目标存在性** |

### ⚠️ 契约边界：内容修改后**不能**再跑 `normalize_chapters.py`

读源码发现 `verify()` 的不变量是**保内容**的：

```
正向：新出现的行必须逐字来自原文，或属于 FIXED_NEW，或是原文某行剥掉前缀后的后缀
反向：消失的行必须命中已知旧导航形态（OLD_NAV）
```

也就是说它的契约是「**只改导航/标题写法，正文逐字不变**」。一旦按本次目标**新增一整节**，正向断言必然判定「出现了无法追溯的新行」并**拒绝写盘**（打印「断言未通过，未写盘」）。

**这不是缺陷，是它的职责边界**。因此执行链调整为：

1. **预检**：跑 `normalize_chapters.py`，期望 10/10 报「无变化」（证明当前源已是归一形态）；同时记录 10 篇的 sha256 基线。
2. **改内容**：只在 `chapters/` 上做本次的逐处补正 + 新增节（新增内容**直接写成最终形态**：`###` 小节标题、脚注体来源块）。
3. **不跑 normalize**（契约边界已说明，理由写进最终报告）。
4. 跑 `assemble_note.py` + `publish_volume.py`；两者的断言即内容修改的守卫（尤其是双链目标存在性——**新增节里不许出现指向不存在笔记的双链**）。
5. **hash 验收**：未触及的 8 篇必须**逐字节不变**，README 也必须逐字节不变（它是 `readme(outnames)` 从 CH 列表生成的，本次不动章节列表）；变了就说明重生成有附带改动，回头查。

## 3. 分组与批次

按「改动相互依赖」分组，不按文件顺序：

| 批次 | 目标 | 为什么放一起 |
|---|---|---|
| **批 1** | **N01 `03-路线选型.md`**（含新增节）+ **N02 `01-结论先行与能力地图.md`** | ch01 的「结论二」与 ch03 的「出发点」是同一句话的两处表述，必须同一批、用同一套措辞 |
| **批 2** | **N05 `04-落地-社区ha-mcp.md`** + **N12 `10-附录`**（补来源） | ch04 那句是 ch03 论断的下游引用；附录 C 补来源条目 |
| **批 3** | **N03 `02_deep_research.md`** + **N04 `01_explore_result.md`** | 研究档勘误，与正文分开，避免与研究记录混改 |
| **批 4** | 父流程：重生成 + hash 验收（不派子代理） | 确定性步骤，交脚本 |

每篇动作：**N01–N05 = `update`**；**N12 = `flag-only`**（只补一条来源，不改正文）；**N06–N11、N13 = `skip`**（P1 已 0 命中）。

## 4. 每篇的具体改动

> ⚠️ **行号口径（批 1 执行时发现并订正）**：本节与 P1 清单里的行号，全是**已发布分册**（vault 内 `*.md`）的行号，
> **不是** `chapters/` 发布源的行号。两者相差**恒为 +15 行**（分册 = 源 + 15：frontmatter 12 行 + 导航 3 行），
> N01、N02 均已实测确认。P4 改的是**发布源**，所以每一处都必须**先按内容锚点定位、再换算**；
> 照抄分册行号会整体偏 15 行、改错位置。若同一小节在分册里是 `## N.M`、在源里是 `### N.M`（升一级变换），
> 也一并按源里的层级写。
>
> **偏移已实测为全册恒定**（10 篇逐篇比对 `wc -l`：01 262→277、02 246→261、03 277→292、04 400→415、05 288→303、
> 06 487→502、07 433→448、08 277→292、09 265→280、10 150→165，**全部 +15**），所以「源 = 分册 − 15」可全册套用；
> 但仍要求**先按内容锚点定位、再用算式交叉验一遍**，不要只信算式。
>
> 换算表（分册 → 源，均已 grep 实测）：N01 `L34→L19`、`L64→L49`、`L67→L52`、`L108→L93`、`L255→L240`、`L279→L264`、`L290→L275`、`L292→L277`；
> N02 `L55→L40`、`L57→L42`、`L59→L44`、`L62→L47`、`L267→L252`；
> **N05 `L24→L9`**（批 2 补）；**N12 分册 `L119`「Hermes 侧：」+ 表体 `L121–125` → 源 `L104` + `L106–110`**（批 2 补）。

### N01 `chapters/03-路线选型.md`

| 位置 | 改法方向 |
|---|---|
| L34（出发点） | **整段重写**为「Hub 是联邦索引，明示 HA 的 skill 有 64 条；official 支只有 `openhue`」+ 前向指向新增节 |
| L46–L62（`openhue` 论证） | **保留**（论据正确），只改「平移到 HA」的落点 |
| L64 | **重写**：删「HA 场景不存在一个可调的 `ha` CLI」，改为「有 `hass-cli`（`home-assistant-ecosystem/…`，社区事实标准，非 HA core 官方）+ Hub 里有封装它的 skill」 |
| L67 | 交叉引用 `3.3 或 3.4` → `3.4 或 3.5`（因新增节导致顺延） |
| L108（大白话） | 保留说明书/零件骨架，末句改为「机器有（`hass-cli`），但说明书得自己找——Hub 里有」 |
| L279（本章小结） | 改「HA 场景不存在可调的 `ha` CLI」这半句 |
| L292（本章来源） | 「skills 定义；smart-home 仅 `openhue`」→ 收窄为「**official 支**仅 `openhue`」，并补 Hub 中央索引来源 |
| **新增 `### 3.2`** | 原 3.2–3.5 顺延为 **3.3–3.6**（5 个标题 + **2 处**交叉引用：L67「3.3 或 3.4」→「3.4 或 3.5」、L255「把 3.1 到 3.4 收成一张表」→「3.1 到 3.5」） |

**新增节内容骨架**（`### 3.2 Hub 里现成可装的 HA skill 清单`）：

1. 一句话说清 Hub 是什么（联邦索引，8 类源：`official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh`），附中央索引 URL 与「截至 2026-09-18 快照」的时点限定。
2. 数字：97,986 条索引中明示 HA 的 64 条；official 支 150 条里 smart-home 只有 `openhue`（原册那层事实**是对的**）。
3. **分级清单**（每项给 `hermes skills install …` 真实命令 + 押在哪条能力路径上）：

| 级 | 条目 | 押在哪条路径 |
|---|---|---|
| **A（首推）** | `skills-sh/homeassistant-ai/skills/home-assistant-best-practices`（749★，**与第 4 章主角 `homeassistant-ai/ha-mcp` 同组织**） | 知识件：决策流 + 反模式表（原生 trigger/condition 优于 Jinja、`entity_id` 优于 `device_id`） |
| **B（有明确 CLI/API 依托）** | `clawhub/homeassistant-cli`（包 `hass-cli`）、`clawhub/py-homeassistant-cli`（自带 REST CLI，无外部依赖）、`clawhub/homeassistant-assist` + `clawhub/home-assistant-agent-secure`（Assist/Conversation API）、`clawhub/mcp-hass` + `skills-sh/aahl/skills/mcp-hass` + `clawhub/homeassistant-mcp`（MCP 桥，对应第 4/5 章）、`clawhub/hass-builder` + `skills-sh/aahl/skills/hass-builder`（`hab` CLI）、`clawhub/home-assistant-master` / `clawhub/haos-ssh-maintenance`（HAOS 运维） | 与第 3.3–3.5 三条路线一一对应 |
| **C（领域件，窄但用途明确）** | `clawhub/grid-aware-energy-load-shifter`、`clawhub/smart-home-energy-saver`、`clawhub/smart-home-assistant`（能源）、`clawhub/home-assistant-causal-incident-analysis`（故障归因）、`clawhub/home-assistant-hub`（监控+告警+TTS+Telegram，服务调用 hard-deny）、`clawhub/music-assistant`、`clawhub/location-awareness`、`skills-sh/bradsjm/hassio-addons/*`（7 件）、小米/小爱系 | 窄场景起手件 |
| **D（谨慎）** | 三个同名 `Home Assistant`（`oo-home-assistant` / `home-assistant` / `homeassistant-selora`）；`clawhub/home-assistant` 与 `clawhub/home-assistant-backup` **描述逐字相同**；`clawhub/homeassistant-toolkit`（模板味）；`skills-sh/home-assistant/core/home-assistant-integration-knowledge`（**来源存疑**：`home-assistant/core` 顶层无 `skills/` 目录，404；代码搜索需鉴权，未验证） | 标注「装前先 inspect」 |

4. **三条使用纪律**（写进正文，不写成脚注）：
   - 索引是**联邦缓存**，数字带时点；变动快，装前先 `hermes skills inspect` 看真身。
   - skills.sh 那 12 条在索引里**只有名字与作者、无描述**——不得据索引推断内容质量。
   - 装前跑自带安全扫描；ClawHub 是开放注册表。
5. **收尾一句**：所以正确的说法是「skill 这条路上游**有东西可装**，但它们**不提供新能力**」——把原册那句否定结论换成准确的两段式。

### N02 `chapters/01-结论先行与能力地图.md`

| 位置 | 改法方向 |
|---|---|
| L55 | 「结论二」改为准确表述（可装 ≠ 能补能力） |
| L57 | 保留「official 支只有 `openhue`」这个事实，**加上范围限定**，并点明 Hub 是联邦索引 |
| L59 | 删「HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI」，改为「`hass-cli` 存在，Hub 里有封装它的 skill」；保留「skill 是知识不是能力」 |
| L62 | 大白话末句改 |
| L267 | 本章小结对应条目改 |

### N05 `chapters/04-落地-社区ha-mcp.md`

**源 L9**（分册 L24）。只改该段的举证从句——现文「skill 只能教 agent 怎么调**已有**的命令行工具，HA 场景下并不存在这样一个 `ha` CLI」。
改为「skill 只能教 agent 怎么调**已有**的命令行工具。HA 侧并非没有这样的 CLI（`hass-cli` 即 `home-assistant-ecosystem/home-assistant-cli`，社区维护、非 HA core 官方），Hub 里也有封装它的 skill——但**这类技能件都不提供新能力**」。

**该段主论断（自建 SKILL.md 补不了能力 → 默认落点 MCP）不动**——补正的是举证从句，不是结论。措辞一律取自 `source_bank.md` §3。

### N12 `chapters/10-附录.md`

**源 L110 之后**（分册 L125 之后）在附录 C「C.1 官方文档索引 · **Hermes 侧**」表内插入一行：

```markdown
| `HMS-13` | Skills Hub **中央索引**（联邦索引，8 类来源：`official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh`；截至 2026-09-18 快照明示 Home Assistant 的 skill 64 条） | `nousresearch.github.io/hermes-agent/docs/api/skills.json` |
```

- `HMS-13` 已核实为空闲（全册占用 HMS-01…HMS-12）。
- 三列格式与该表既有三条（`HMS-04` / `HMS-07` / `HMS-10`）一致：ID / 主题 / 位置；「仓库内路径」换成 URL。
- **不动**附录 C 的 `COM-` 表（它本就是「有价值对照」的**子集**清单，不列全量，无需补 `COM-24`/`COM-25`）。
- **不动**附录 A、附录 B、附录小结与任何正文。

### N03 `chapters/../02_deep_research.md`、N04 `01_explore_result.md`

- B-1 表行 / L364 结论 1 / L516 交接表 / L320「维持」→ 全部改为**推翻**，并写明确认方式（查中央索引，非仅 `optional-skills/`）。
- `01_explore_result.md`：L29 小节标题、L31、L102 来源表；**新增来源续编新 ID**（该文件的 HMS-/HAS- 编号是本 run 私有命名空间，**不改写既有 ID**，避免与分册正文的 HMS-05 混淆）。
- 两份研究档均以**带日期的勘误块**形式记录，不做静默改写。
- `02_deep_research.md` §5.7 工具坑**新增一条**：「核对 Hermes Skills Hub 必须查中央索引；Hub ≠ 仓库内 `optional-skills/` 目录」。
- 明确**不动**：`00_intent.md`、`03_outline.md`、`research/probe-01..05-*.md`（历史记录与原始证据，改了等于伪造审计链）。

## 5. 共享资料

**不新开收集**，但**不跳过 P3**：把既有已核验证据编成 `shared_research/source_bank.md`（P3 的指定产物），作为**全局措辞与数字锁**——所有批次逐字引用其中的数字、命令与分级，不得自行改写。

> P0 曾记「P3 直接 skip」。改为「start → 编制 → complete」：产物本来就是这条工作流规定的共享资料位，跳过它会让措辞锁没有落点。差异会写进最终报告。

## 6. 覆盖风险

1. **措辞漂移**：同一数字/命令出现在 5 个文件里。→ 由 `source_bank.md` 锁定，逐字引用；P4 收尾 grep 全部 64 / 97,986 / 8 类源 / `hass-cli` 的拼写与数字是否一致。
2. **重生成引入附带改动**：→ hash 验收（8 篇 + README 逐字节不变）是硬门槛。
3. **交叉引用断裂**：新增节导致 3.2–3.5 顺延。→ 分册内共 **2 处**引用 3.x：L67 与 L255；研究档内 0 处。改完再 grep 复核。
   > 自查留痕：我第一次 grep 时给 03 加了「排除 200–299 行」的过滤，**把 L255 一起排掉了**，因此一度写成「仅 1 处」。范围过滤会连真命中一起滤掉——这类过滤只该用来压缩输出，不该用来判定。P4 收尾复核不再加任何行号范围过滤。
4. **索引时效**：联邦索引随时变化。→ 所有数字带「截至 2026-09-18 快照」限定。
5. **`hass-cli` 的官方性措辞**：ClawHub 条目自述「the official hass-cli tool」，实际是 **HA Ecosystem 组织**的社区事实标准，不是 HA core 官方。→ 措辞必须精确，不沿用 Hub 条目的自述。
6. **来源存疑件**：`skills-sh/home-assistant/core/…` 无法验证（404 + 代码搜索需鉴权）。→ 归入 D 级并标明未验证，不写成「官方出品」。
7. **分册已被外部进程自动提交**（`git log` 显示每约 1 分钟一次 `vault backup`）。→ 改动会被它自动入库；审计以 `updates/{note_id}/` 的副本为准，不以 git diff 为唯一线索。

## 7. 需用户确认（P2 门）

1. **批次划分与动作**（第 3 节）是否认可。
2. **新增节的位置**：推荐插为 **3.2**（编辑上最顺：紧跟路线总表，为 3.3「为什么自建 SKILL.md 补不了能力」铺垫），代价是 5 个标题顺延 + 2 处交叉引用。
   - 替代方案：插为 **3.6**（3.5 之后、小结之前），**零改号**，但离它要补正的那段话较远。
3. **N12 附录** 按 `flag-only`（只补来源一条）处理是否可以。
4. **研究档的处理**：带日期勘误块 + 不动 `00_intent` / `03_outline` / `probe-*`，是否认可。

---

**本阶段仍是零写入**：未改动分册与两份研究档中任何文件；本批新增仅 `workspace/update-hermes-ha-volume/` 下的 P2 产物。
