# 共享资料库 / 全局措辞与数字锁 — `update-hermes-ha-volume`

**阶段**：P3 ｜ **产出**：本文件 ｜ **性质**：本批 6 个目标**共用**的措辞与数字基准

> **这不是新收集**（P0 已定 `shared_research: 已有`）。本文件只把 P0 前已核验的证据**编成一个位**，
> 让批 1–3 的每个执行单元**逐字引用同一套数字、命令与分级**，防止同一条事实在 5 个文件里被写成 5 个版本。
> 所有证据取自 `sources/HUB-homeassistant-skills.json`（56,846 B 快照）与 GitHub/PyPI API 核实。

## 0. 使用纪律（给批 1–3 的执行单元）

1. **本节锁定的数字与命令必须逐字使用**，不得改写、四舍五入、换算或补零。
2. **不得自行新增数字**。需要本文件没有的数字时，停下来回报，不要推算。
3. **不得把「未验证」写成「已验证」**——第 6 节列了三条专项禁令。
4. 每处事实性表述**必须带时点限定**（本文件第 1 节给的固定写法），因为索引是联邦缓存、随时变化。
5. 改动范围以外的一律不动；新增内容**直接写成最终形态**（`###` 小节标题、脚注体来源块）。

## 1. 时点限定（固定写法，照抄）

> **截至 2026-09-18 的 Hub 中央索引快照**

凡出现 97,986 / 64 / 52 / 12 / 13 / 150 这些数字的地方，**必须同句带一处此时点限定**；同一自然段内多次出现时，至少首次出现处带。

## 2. 锁定的数字

| 数字 | 含义 | 可复验取回方式 |
|---|---|---|
| **97,986** | Hub 中央索引条目总数 | `https://nousresearch.github.io/hermes-agent/docs/api/skills.json`（60.8 MB 单行 JSON） |
| **64** | 索引中**明示 Home Assistant** 的 skill 条数 | 同上；抽取脚本 `workspace/hermes-home-assistant/extract_hub_ha.py` |
| **52 / 12** | 上述 64 条按来源拆分：ClawHub 52 + skills.sh 12 | 同上 |
| **13** | `category: smart-home` 但**未点名** HA 的条数 | 同上 |
| **150** | 索引中 `official` 支条数；其中 smart-home 分类**只有 `openhue`** 一个 | 同上 |
| **8** | Hub 支持的来源类型数：`official` / `skills-sh` / `well-known` / `url` / `github` / `clawhub` / `lobehub` / `browse-sh` | HMS-05 原文「Supported hub sources」表 |
| 索引总源分布 | ClawHub 75,785 ／ skills.sh 20,000 ／ GitHub 513 ／ LobeHub 505 ／ browse.sh 469 ／ NVIDIA 365 ／ **official 150** ／ built-in 58 ／ gstack 53 ／ OpenAI 44 ／ HuggingFace 25 ／ Anthropic 19 | 同中央索引 |

## 3. 锁定的措辞（可直接引用）

**关于 Hub 是什么**（第一层补正的核心）：

> Skills Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表（skills.sh、ClawHub、LobeHub、browse.sh、well-known 端点、GitHub taps）；`official`（Hermes 仓库内的 optional/bundled skills）只是其中一支。

**关于原册那层事实（它是对的，要保住）**：

> 「official 支的 smart-home 分类下只有 `openhue` 一个」——这句话**本身没错**，错在把它当成了整个 Hub 的结论。

**关于 `hass-cli`**（第二层补正的核心，措辞必须精确）：

> `hass-cli` 指的是 `home-assistant-ecosystem/home-assistant-cli`——**Home Assistant Ecosystem 组织**维护的命令行工具，是社区里的事实标准，**不是 HA core 官方出品**（Hub 里 `clawhub/homeassistant-cli` 条目的自述称其为 “official”，措辞不精确，本册不沿用）。

**关于洞察的保留**：

> 「**skill 是知识，不是能力**」这条判断成立，而且是本册的骨架。补正的是**举证**，不是**结论**：HA 场景**有**可调的 CLI（`hass-cli`），Hub 里也**有**封装它的 skill；但这些 skill 仍然只是**知识件**，不新增任何工具。

**关于 `homeassistant-ai` 这个组织（与第 4 章的接点）**：

> `homeassistant-ai/skills`（749★）与第 4 章的主角 `homeassistant-ai/ha-mcp`（4762★）**是同一个组织**。第 4 章只讲了它的 MCP server（**服务件**），漏了它的 skills 仓库（**知识件**）——补上即构成完整答案。

## 4. 锁定的安装命令（逐字，来自索引快照的 `installCmd` 字段）

A 级：

```
hermes skills install skills-sh/homeassistant-ai/skills/home-assistant-best-practices
```

B 级（有明确 CLI/API 依托）：

```
hermes skills install clawhub/homeassistant-cli
hermes skills install clawhub/py-homeassistant-cli
hermes skills install clawhub/homeassistant-assist
hermes skills install clawhub/home-assistant-agent-secure
hermes skills install clawhub/mcp-hass
hermes skills install skills-sh/aahl/skills/mcp-hass
hermes skills install clawhub/homeassistant-mcp
hermes skills install clawhub/hass-builder
hermes skills install skills-sh/aahl/skills/hass-builder
hermes skills install clawhub/home-assistant-master
hermes skills install clawhub/haos-ssh-maintenance
```

C 级（领域件）：

```
hermes skills install clawhub/grid-aware-energy-load-shifter
hermes skills install clawhub/smart-home-energy-saver
hermes skills install clawhub/smart-home-assistant
hermes skills install clawhub/home-assistant-causal-incident-analysis
hermes skills install clawhub/home-assistant-hub
hermes skills install clawhub/music-assistant
hermes skills install clawhub/location-awareness
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-automation-scripts
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-awtrix
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-custom-integration
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-dashboards-cards
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-entities-services
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-esphome
hermes skills install skills-sh/bradsjm/hassio-addons/home-assistant-integrations-addons
```

> 正文里**不必**把这 26 条全列出——按能力路径分组给代表条目即可，但**凡列出的命令必须逐字照抄本表**。

## 5. 质量分级（锁定的判据）

| 级 | 判据 | 代表条目 |
|---|---|---|
| **A** | 有真实项目背书（星数、持续维护）、走开放标准、与本书既有内容有真实接点 | `skills-sh/homeassistant-ai/skills/home-assistant-best-practices`（749★，pushed 2026-09-16，Agent Skills 标准 agentskills.io，含决策流 + 反模式表） |
| **B** | 能指出它所依赖的**具体 CLI / API**，即「能力真实存在、skill 只是教怎么用」 | `clawhub/homeassistant-cli`（包 `hass-cli`）、`clawhub/py-homeassistant-cli`（自带 REST CLI，无外部依赖）、Assist/Conversation API 两件、MCP 桥三件、`hab` CLI 两件、HAOS 运维两件 |
| **C** | 领域窄但用途明确，能对应到一个具体场景 | 能源三件、故障归因、监控告警（`home-assistant-hub`：服务调用 hard-deny）、音乐、位置、`bradsjm/hassio-addons/*` 七件 |
| **D** | 存在可指认的质量问题或来源无法验证 | 见第 6 节 |

## 6. 三条禁令（不得写反）

1. **不得写「Hub 里没有现成 HA skill」「没有可装的东西」「不存在可调的 `ha` CLI」。** 这三句是本次要补正的错误原文。
2. **不得宣称 `hass-cli` 是 HA 官方工具**——它是 HA **Ecosystem** 组织的社区工具（第 3 节给了锁定措辞）。
3. **不得把 `skills-sh/home-assistant/core/home-assistant-integration-knowledge` 写成官方出品或已验证**。它的来源**存疑、未验证**：`home-assistant/core` 仓库**顶层没有 `skills/` 目录**（请求 404），GitHub 代码搜索需要鉴权、未能执行。归 **D 级**并标明未验证。

**另两条注意事项**：

- skills.sh 那 12 条在索引里**只有名字与作者、无描述**——不得据索引推断内容质量，必须写「装前先 `hermes skills inspect` 看真身」。
- ClawHub 是开放注册表，**有重复件与凑数件**：三个条目同名 `Home Assistant`；`clawhub/home-assistant` 与 `clawhub/home-assistant-backup` 的 `description` **逐字相同**；`clawhub/homeassistant-toolkit` 的描述是通用模板腔（“Reference tool for life — covers intro, quickstart, patterns and more”）。

## 7. 逐条资料（URL + 日期 + 适用范围 + 摘要）

### D-1 ｜ Hub 中央索引（本次最核心的新证据）

- **URL**：`https://nousresearch.github.io/hermes-agent/docs/api/skills.json`（HMS-05 指明的中央索引）
- **日期**：快照取回 2026-09-18；索引为**联邦缓存**，随时变化
- **本地快照**：`workspace/hermes-home-assistant/sources/HUB-homeassistant-skills.json`（56,846 B，含 64 条明示 HA 记录 + 13 条 smart-home 记录，逐条带 `installCmd` / `source` / `category` / `tags`）
- **适用范围**：全部 6 个目标；数字与命令的**唯一**来源
- **摘要**：60.8 MB 单行 JSON，97,986 条记录。`source` 字段共 12 个取值，其中 `official`（= Hermes 仓库内的 optional/bundled）仅 150 条，而联邦外部注册表占 97,758 条。按 HA 词族（`home.assistant|hass|homeassistant`）匹配 `name`/`description`/`tags`/`installIdentifier` 得 64 条明示 HA 的 skill；另有 13 条 `category: smart-home` 未点名 HA。**原册结论只覆盖了 150 条那一支。**
- ⚠️ 60.8 MB 原始索引**未保留**（避免进 git），重取约 9 分钟。

### D-2 ｜ `hass-cli`（第二层补正的物证）

- **URL**：`https://github.com/home-assistant-ecosystem/home-assistant-cli` ／ PyPI 包 `homeassistant-cli`
- **日期**：仓库 pushed 2026-08-04；PyPI 版本 1.0.0；核实于 2026-09-18
- **适用范围**：N01（ch03 3.2 节与新增节）、N05（ch04 L24 举证从句）
- **摘要**：596★，**未归档**，最近一次 push 在 2026-08（活跃）。PyPI summary 为 “Command-line tool for Home Assistant”。归属 **Home Assistant Ecosystem**（社区组织），非 HA core。Hub 里的 `clawhub/homeassistant-cli` 自述 “Advanced Home Assistant control using the official hass-cli tool. Features auto-completion, event monitoring, history qu…”，即**包这个 CLI** 的 skill——「HA 场景没有可调 CLI」的反例。
- 附注：Hub 里另有两条同类封装 `clawhub/py-homeassistant-cli`（自带 REST CLI、无外部依赖）与 `clawhub/home-assistant-bridge-python`（条目名 `minos`），可一并作为「有 CLI 依托」的旁证。

### D-3 ｜ `homeassistant-ai/skills`（A 级首推的物证，且与第 4 章同组织）

- **URL**：`https://github.com/homeassistant-ai/skills` ／ 索引条目 `skills-sh/homeassistant-ai/skills/home-assistant-best-practices`
- **日期**：749★；pushed 2026-09-16；核实于 2026-09-18
- **适用范围**：N01（新增节的 A 级）、N02（ch01 结论二的替代举证）
- **摘要**：仓库自述 “Home Assistant skills for agents”，遵循开放的 **Agent Skills 标准**（agentskills.io），含一个 skill `home-assistant-best-practices`：决策工作流 + 反模式表（原生 trigger/condition 优于 Jinja 模板、`entity_id` 优于 `device_id`、运动灯应 `mode: single`），覆盖 Authoring / Dashboards / Operations / AppDaemon。安装方式除 `hermes skills install` 外，官方 README 亦给 `npx skills add homeassistant-ai/skills`。
- **关键接点**：该组织**同时**是第 4 章主角 `homeassistant-ai/ha-mcp`（4762★，自述 87 tools）的维护方。

### D-4 ｜ HMS-05（原册自己的来源，被读漏的那一半）

- **URL**：`website/docs/user-guide/features/skills.md`
- **本地快照**：`workspace/hermes-home-assistant/sources/raw-skills.md`（56,911 B）
- **日期**：原册采集于 2026-09-18
- **适用范围**：全部；用于证明「联邦 Hub」这一事实**一直在原册自己的来源里**
- **摘要**：该文件 L708 起为 `## Skills Hub`，写明搜索由**中央索引**回答、给出 `hermes skills browse/search/inspect/install` 子命令、并列出「Supported hub sources」表（8 类）与「Integrated hubs and registries」。**全文 grep `home.assistant|hass|smart.home` 零命中**——证明原册的「没有 HA skill」结论**不来自** HMS-05 正文，而是只从 `optional-skills/` 目录清单推出来的。

### D-5 ｜ `homeassistant-ai/ha-mcp`（既有来源，用于组织接点）

- **URL / ID**：索引条目与第 4 章一致（`COM-01` 仓库 README、`COM-23` Setup Wizard）
- **日期**：原册采集于 2026-09-18
- **适用范围**：N01（新增节的组织接点句）、N02（可选互见）
- **摘要**：4762★，自述 87 tools。其 Setup Wizard 已为 Hermes 写专属配置分支与 Notes（`mcp__home_assistant__<tool>`、`/reload-mcp`），但 README 未收录 Hermes——即原册第 1 章的「受支持但 README 未列」。**本次不重查该仓库**，沿用原册已核验结论。

---

**本阶段仍是零写入**：未改动分册与两份研究档中任何文件；新增仅本文件。
