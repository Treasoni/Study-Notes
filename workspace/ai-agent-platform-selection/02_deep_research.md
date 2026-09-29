# P2 深度素材 — 自托管 AI Agent 平台选型

- **运行**: `ai-agent-platform-selection`（learning-note-flow）
- **阶段**: P2 深度收集
- **日期**: 2026-09-29
- **状态**: **进行中** — Octop 轴待并入（见 §4）

---

## 1. 方法与范围

- 主线段落已定向验证并修正（见 `01b_thesis_verification.md`），采纳主线 **T′**（详见 §6）
- P2 由 3 个批量子代理按**七轴统一口径**提取 claim 级笔记；代理为 P2 前置验证轮的**续写**，不重读材料
- 全部 claim 落盘原文见 `research/{octop,openclaw,hermes,framework}/`
- 抓取走 `.claude/skills/research-collector/scripts/crawl.sh`（`WebFetch` 对相关域名被网络策略拦截）

**七轴口径**：A1 定位与产品主语 / A2「多用户」的具体语义 / A3 架构形态 / A4 记忆与上下文 / A5 工具与扩展体系 / A6 与另两者的显式关系 / A7 运维成本与官方限制

---

## 2. 已落盘原文（重建笔记时可复核锚点）

### OpenClaw — `research/openclaw/`
| 文件 | 对应页面 |
|---|---|
| `01_docs_openclaw_ai.md` | `concepts/architecture` |
| `02_docs_openclaw_ai.md` | `start/why-openclaw` |
| `03_docs_openclaw_ai.md` | `concepts/multi-user` |
| `04_docs_openclaw_ai.md` | `gateway/multi-tenant-hosting` |
| `05_docs_openclaw_ai.md` | `start/teams` |
| `06_raw_githubusercontent_com.md` | README |
| `extra/01..04` | `agent-runtimes` / `memory` / `security` / `tools-skills` |
| `extra2/01` | **`start/why-openclaw/openclaw-and-hermes-agent`（官方 17 轴对照表）** |
| `extra2/02` | `cli/fleet` |
| `community/01, 02` | 腾讯云开发者社区两篇（2026-04-13 / 2026-05-26） |

### Hermes — `research/hermes/`
| 文件 | 对应内容 |
|---|---|
| `01_raw_githubusercontent_com_README.md` | README（2026-09-29） |
| `02_..._multi-profile-gateways.md` | `/docs/user-guide/multi-profile-gateways` |
| `03_..._messaging-index.md` | messaging `index.md`（**2026-08-27 旧抓取件**） |
| `04_github_com_README-github-page.md` | GitHub README 页（**2026-08-27**） |
| `gw/01_...md` | `developer-guide/gateway-internals` |
| `src/claw.py`（531 行） | 迁移命令实现 |
| `src/openclaw_to_hermes.py`（3254 行） | 迁移脚本（36 个具名迁移项） |

### 横向框架 — `research/framework/`
| 文件 | 对应内容 |
|---|---|
| `13_arxiv_2606.20683v1_fulltext.md` | arXiv 全文 |
| `abs/01_arxiv_org.md` | abs 页（**与全文有一处措辞冲突，见 §5**） |
| `17_awesome-ai-agent-platforms_README.md` | 分类清单 |
| `zh/01_szhshp_org.md` | 社区替代源（2026-07-11） |

### 既有本地产物（第一手，非本轮抓取）
`workspace/hermes-agent/`（`output/final_note.md`、`chapters/01_定位与核心理念.md`、`research/` 7 份 + `gaps/`）、`hermes-tool-config/`、`hermes-home-assistant/`、`hermes-docker-deploy/`、`hermes-rules-config/`

---

## 3. claim 图谱

### 3.1 OpenClaw

**A1 定位** — 产品主语是「你的助手」，默认形态是「受信的单操作者助手」
- `OpenClaw is an open-source AI assistant that runs on your own computer` — README 首段
- `Default OpenClaw is a trusted single-operator assistant.` — `why-openclaw#what-we-do-not-claim`
- `as a hardened team deployment, with configuration as the only difference` — `why-openclaw`
- `There is no enterprise edition.` — 同上（另见 `no enterprise edition under a different license`）
- **并列不合并**：同页亦有 `battle-tested agent for anyone, individual or enterprise, to build on`（生态/受众措辞，非版本声明）

**A2「多用户」= 同一信任域内的协作（含三层署名），且明确不是安全边界**
- `Multi-user mode lets several trusted people operate the same OpenClaw agent.` — `concepts/multi-user`
- `Every session carries up to three layers of attribution` — 同上（Creator 不可变 / Owner 可指派 / Participants 历史）
- `usability features, not security boundaries` — 同上
- `It is not an authorization or isolation boundary.` — 同上
- 准入走 DM 配对码：`the first time a teammate DMs the bot they get a pairing code` — `start/teams`
- 分级靠命名角色：`Named operator roles bind authenticated profiles to a policy` — 同上
- `This is account-selection convenience inside one trust domain, not isolation` — `concepts/multi-user`
- `A single-user gateway therefore looks unchanged.` — 同上（多用户是叠加层）
- 参与上限：`The normal admission limit is 32 identities per logical session.` — 同上
- **多租户不在一个 Gateway 内**：`not hostile multi-tenant isolation inside one shared Gateway` — `gateway/multi-tenant-hosting`

**A3 架构** — 单长期存活 Gateway 拥有全部消息面，每主机一个，默认只绑 loopback
- `A single long-lived **Gateway** owns all messaging surfaces` — `concepts/architecture`
- `One Gateway per host.` — 同上
- `The Gateway binds to loopback by default.` — `start/teams`
- 扩展靠插件：`harnesses ship as plugins against a core that stays deliberately small` — `why-openclaw`
- 多租户形态：`Each cell has its own Gateway, state, credentials, channel accounts, container` — `cli/fleet`
- `Remote cell hosts are not supported.` — 同上
- `Resistance to a compromised host is a non-goal.` — `gateway/multi-tenant-hosting`

**A4 记忆** — 记忆就是工作区里的普通 Markdown，无隐藏状态
- `The model only remembers what gets saved to disk; there is no hidden state.` — `concepts/memory`
- 四类文件：`USER.md` / `MEMORY.md` / 每日笔记 / `DREAMS.md` — 同上
- `Dreaming is the default background consolidation path for memory.` — 同上
- 压缩前静默落盘：`Before compaction summarizes your conversation, OpenClaw runs a silent turn` — 同上
- 可从外部导入：`import existing local memory from Codex, Claude Code, and Hermes` — 同上
- `Memory can preserve approval context, but it does not enforce policy.` — 同上
- 限制：`Promoted memories have no time-based retention bound.` — `why-openclaw`

**A5 扩展** — 技能 = 带 `SKILL.md` 的目录，按来源优先级覆盖；插件进程内运行且不沙箱
- `Each skill lives in a directory containing a `SKILL.md` file` — `tools/skills`
- `File-backed skills load from these sources, **highest precedence first**` — 同上（workspace 最高、bundled 最低）
- `Native plugins run in-process and are not sandboxed.` — `why-openclaw`
- `The public plugin SDK publishes about 150 entrypoints` — 同上
- `ClawHub is OpenClaw's registry, with publishing, moderation, security audits` — 同上

**A6 与另两者的关系** — **官方专页对 Hermes 做 17 轴 source-verified 对照；Octop 零提及**
- `The recurring comparison is [Hermes Agent]` — `why-openclaw`
- `condenses the source-verified contrast with Hermes` — 同上 → `extra2/01`
- 官方逐字引用 Hermes 安全政策：`The only security boundary against an adversarial LLM is the operating system.` — 同上（引自 Hermes `SECURITY.md`）
- `Hermes is built by Nous Research, a venture-funded company` — 同上
- 对照表 `Roles and multi-user` 行对 Hermes 的判定：`Equal trust within an adapter's authorized set` — `extra2/01`
- 对照表把自身多租户工具标为 `experimental per-tenant fleet cells` — 同上
- **双向 grep：README 全文对 `hermes` / `octop` 提及次数均为 0**（README 不提，但 docs 站有专页 —— 门面与文档深度不一致，**并列记录**）

**A7 成本与限制**
- `Sandboxing and exec approvals are off by default.` — `why-openclaw`
- `Roles and session ownership are collaboration guardrails.` — 同上
- `Tenancy means one gateway cell per tenant, and fleet is still experimental.` — 同上
- Fleet 成熟度：`can change between releases without a deprecation window` — `cli/fleet`
- 明确不提供：`A tenant self-service portal, billing plane, or delegated administration UI` — `multi-tenant-hosting#Current scope`
- `multi-machine, identity-governed fleets require a separate control-plane layer` — 同上
- `No rung in this ladder changes the OpenClaw application trust model` — 同上#Isolation ladder
- `The Fleet operator and the host are trusted by every tenant.` — 同上#Trust boundary
- `container images default to an exposed bind` — `gateway/security`
- `Egress allowlisting covers cooperating traffic only.` — `why-openclaw`
- `gateway.roles` 仅存在于 2026-08 快照：`Check your installed version before depending on it.` — 同上

---

### 3.2 Hermes

**A1 定位** — 产品主语是单数「你」；**明确不绑本机**
- `**The self-improving AI agent built by [Nous Research](...).** It's the only agent with a built-in learning loop` — README
- `builds a deepening model of who you are across sessions` — 同上
- `Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop` — 同上 ← **与 OpenClaw 的「laptop」定位正面分野**
- 权威清单一句话定位：`[Hermes Agent](...) - Personal agent with memory, skills, tools, scheduled jobs, and messaging channels.` — `framework/17`

**A2「多用户」= 准入 + 很窄的分级 + profile 路由；无租户语汇**
- 负面结论：检索 `multi-tenant` / `multitenant` / `multi-user` / `SaaS` **零命中**；唯一 1 处 `tenant` 指**消息平台的**租户命名空间
  - `Sender ids are also namespaced per tenant on some platforms — a Slack user id is workspace-local` — `multi-profile-gateways`
- 准入：`**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` — messaging `index.md`
- 多用户 ID 列表：`TELEGRAM_ALLOWED_USERS=123456789,987654321` — 同上
- DM 配对：`unknown users receive a one-time pairing code when they DM the bot` — 同上
- 分级：`Every allowed user falls into one of two tiers per scope (DM vs group/channel):` — 同上
- 官方定性机制：`Allowlists answer "can this person reach the bot at all?" The **admin / user split** answers "now that they're in, what are they allowed to do?"` — 同上
- **分级边界很窄**：`**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.` — 同上
- profile 路由：`To give one person a privileged profile and everyone else a restricted one, declare the privileged sender route first, add a platform-wide catch-all route to the restricted profile after it` — `multi-profile-gateways`
- **但不是授权**：`Sender routing selects a profile; it is not deny-by-default authorization.` — 同上
- profile 的示例用途是「多个 agent」非「多个租户」：`A personal assistant on one Telegram bot and a coding agent on another` — 同上
- 隔离单位是 profile（会话命名空间 `agent:<profile>:…`、密钥、记忆）— 同上

**A3 架构** — 网关常驻单进程接 20+ 平台；默认一 profile 一网关，可多路复用
- `The messaging gateway is the long-running process that connects Hermes to 20+ external messaging platforms through a unified architecture.` — `gateway-internals`
- `Standalone (one gateway per profile)` — 同上
- `With `gateway.multiplex_profiles: true` one process serves the default profile plus every live directory under `profiles/`` — 同上
- `#### 1. Secondary profiles must not start their own gateway` — `multi-profile-gateways`
- supervisor 语义：退出码 `78` (`EX_CONFIG`) 表示永久失败，避免无限重启 — `gateway-internals`
- `Seven terminal backends — local, Docker, SSH, Singularity, Modal, Daytona, and Vercel Sandbox.` — README
- 限制：`Shared-ingress platforms (WhatsApp bridge, Relay) run on the default profile only` — `gateway-internals`

**A4 记忆** — 内置记忆小且有硬上限；Honcho 做辩证式用户建模
- `| **MEMORY.md** | Agent's personal notes ... | 2,200 chars (~800 tokens) |` — `gaps/06_..._memory.md`
- `| **Capacity** | ~1,300 tokens total | ... |` / `| **Cost** | Token cost in every prompt |` — 同上
- `**Dialectic reasoning** : After each conversation turn (gated by `dialecticCadence`), Honcho analyzes the exchange and derives insights about the user's preferences, habits, and goals.` — `research/04_..._honcho.md`
- Honcho 的「多 agent」是同一用户的多个 agent：`When multiple Hermes instances talk to the same user (e.g., a coding assistant and a personal assistant), Honcho maintains separate "peer" profiles.` — 同上 ← **再次印证「多用户」在不同产品里含义不同**
- 闭环：`A closed learning loop`（agent 策展记忆 + 自主技能创建 + 技能自我改进 + FTS5 会话检索 + Honcho 建模）— README
- 限制：`Don't point two agent processes at the same Hermes home directory. ... Memory is scoped per [profile] by design` — `gaps/06`

**A5 扩展** — 技能是按需加载的知识文档，agent 可自建自改自删
- `Skills are on-demand knowledge documents the agent can load when needed. They follow a **progressive disclosure** pattern to minimize token usage` — `gaps/07_..._skills.md`
- `The agent can create, update, and delete its own skills via the `skill_manage` tool. This is the agent's **procedural memory**` — 同上
- 默认自由写：`By default the agent writes skills freely — including from the [background self-improvement review]` — 同上
- `Compatible with the <a href="https://agentskills.io">agentskills.io</a> open standard.` — README
- ⚠️ 层级标注：`自改进的实质：改的是技能层，不是模型权重` 出自 **本仓库既有产物** `workspace/hermes-agent/chapters/01_定位与核心理念.md`，属**二次加工**，非官方原文

**A6 迁移 = 同层的铁证（双向）**
- `## Migrating from OpenClaw` / `If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.` — README
- `**During first-time setup:** The setup wizard (`hermes setup`) automatically detects `~/.openclaw` and offers to migrate before configuration begins.` — 同上
- 四种调用形态（含 `--dry-run` / `--preset user-data` / `--overwrite`）— 同上
- 迁移内容清单：`SOUL.md` / `Memories`（MEMORY.md + USER.md）/ `Skills`（→ `~/.hermes/skills/openclaw-imports/`）/ `Command allowlist` / `Messaging settings` / `API keys` / `TTS assets` / `Workspace instructions` — 同上
- 源码：`"""hermes claw — OpenClaw migration commands."""` — `src/claw.py:1`
- 源码兼容三代目录名：`_OPENCLAW_DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot")` — `src/claw.py:29`
- 脚本共 **36 个具名迁移项**（含 MCP servers / Cron / Hooks / Gateway / Session / Approval rules）— `src/openclaw_to_hermes.py:40-190`
- **密钥默认不迁**：`Secrets are never included implicitly: --migrate-secrets is required even under --preset full (OpenClaw's two-phase posture); no silent API-key import.` — `src/claw.py:33-34`
- 另有一条：`hermes honcho migrate # Step-by-step migration guide from openclaw-honcho` — `research/04_..._honcho.md`
- **与 Octop 的关系：无显式表述**（README/文档/源码未检索到 Octop 或腾讯）

**A7 成本与限制**
- `serverless infrastructure that costs nearly nothing when idle` — README
- 记忆代价：`| **Token cost** | Fixed per session (~1,300 tokens) | On-demand (searched when needed) |` — `gaps/06`
- `The review fork can burn a meaningful share of total tokens on busy hosts.` — 同上
- 多路复用的代价：`Collapsing such a fleet replaces a kernel-enforced boundary (file ownership, `User=`) with in-process isolation, which is an operator's decision.` — `multi-profile-gateways`

---

### 3.3 Octop

> ⏳ **P2 进行中，待并入。**
> 已确认的部分见 `01b_thesis_verification.md`（多用户为架构内建：全局 JWT 中间件、`agents.user_id` 行级归属、RBAC 权限目录、按用户配额与工作区策略；官方口径限定为 `households and small teams`，`Vertical scaling only (one machine)`；桌面端只是同一多用户服务端的 Wails 外壳，无独立单用户模式）。
> 本轮待补：① `permissions.py` 中 `Read access and agent use in chat are never gated.` 与行级归属的准确关系；② 单进程模型在多用户并发下的真实瓶颈。

---

## 4. 横向框架底稿

### 4.1 arXiv 2606.20683 — agent 能力是「模型–harness 配对」的属性

- 核心论断：`we argue that agent performance is a property of the model–harness pairing`；`Benchmark scores should therefore be interpreted as outcomes of a _model–harness pairing_`
- harness 形式化为六元组：`ℋ=⟨ℐobs,𝒞,ℒ,ℐact,𝒮,𝒱⟩`
- 六职责原始定义（逐字）：

| # | 职责 | 原始定义 |
|---|---|---|
| ① | Observation interface | `transforms raw environment signals into model-usable observations, including terminal output, file diffs, screenshots, DOM states, API responses, logs, retrieved passages, and event streams.` |
| ② | Context manager | `determines what information enters the model context, when it enters, and in what form, covering prompt construction, system instructions, retrieval, memory selection, compression, summarization, tool descriptions, and current task state.` |
| ③ | Control loop | `orchestrates the observe-reason-act-feedback cycle, including step scheduling, stopping criteria, retries, reflection, delegation, handoffs, and multi-agent coordination. In multi-model settings, ℒ additionally implements model routing and role assignment.` |
| ④ | Action interface | `maps model outputs to executable operations, such as function calls, MCP tools, shell or code execution, browser actions, file operations, API calls, and sub-agent invocations.` |
| ⑤ | State and artifact store | `persists execution state and products, including conversation history, plans, scratchpads, checkpoints, logs, traces, diffs, memory records, generated files, and task artifacts.` |
| ⑥ | Verification and governance layer | `checks, constrains, and repairs execution through tests, assertions, verifier models, sandbox policies, permission gates, rollback, retry, budget control, safety constraints, and audit traces.` |

- 组件非独立：`Although the six components are analytically separable, they do not operate independently. Design choices in one component often reshape the burden on others.`
- **选型透镜**：`a task is not merely an application label but a pressure profile over observation, context, control, action, state, and governance`
- ⚠️ **冲突未消解**：abs 页作 `observation, context, control, action, state, and verification`，HTML 全文作 `verification/governance`（同论文两版呈现差异，**并列记录，不合并**）

### 4.2 awesome-ai-agent-platforms — 分类体系

- 五类：`AI coworkers and teammates, agent builders and frameworks, workflow automation platforms, browser agents, and coding agents, with license and hosting notes for every entry.`
- AI coworker 定义：`AI coworkers are persistent agents that people delegate real work to: they sign in to tools, keep context, run on schedules, and come back with finished work.`
- 分类即用途定位：`Each project appears once, under the category that best matches its main use.`
- **OpenClaw 与 Hermes 同收在 `AI coworkers and teammates` 节下**
  - `[OpenClaw](...) - Assistant that connects models, tools, messaging channels, and companion applications through one gateway. License: MIT. Hosting: self-hosted on a device or server.`
  - Hermes 同节：`Personal agent with memory, skills, tools, scheduled jobs, and messaging channels.`
- **Octop / Tencent 未被收录**（全文件检索无命中）

---

## 5. 冲突与并行记录清单（不得静默合并）

| # | 冲突 | 各方 | 处理 |
|---|---|---|---|
| C1 | Octop harness 核心是否开源 | 社区称「核心未开源」**vs** 三库已于 2026-09-24 公开 | 时间点不同，待 Octop 轴并入时裁决 |
| C2 | 各项目 Star 数 | 自媒体 6 万~24 万+ 互相矛盾；GitHub API 直读 openclaw 390,772 / hermes 249,977 | **标注不可靠，不作选型证据** |
| C3 | OpenClaw 是否面向企业 | `anyone, individual or enterprise, to build on` / `councils on ... enterprise deployment` **vs** `There is no enterprise edition.` / `no enterprise edition under a different license` | 治理/受众措辞 vs 版本/许可声明，语义不同，并列 |
| C4 | OpenClaw 官方内部对 Hermes 提及深度 | README 全文 grep `hermes` = 0 **vs** docs 站有专页级对照与逐字引述 | 门面 vs 文档深度，并列 |
| C5 | OpenClaw「多用户是否一等公民」 | 完整概念页 + 三层署名 + 角色 + presence（功能面完备）**vs** 官方自称 `collaboration guardrails`、`usability features, not security boundaries`、`A single-user gateway therefore looks unchanged.` | 两点都真，措辞需同时呈现 |
| C6 | OpenClaw 记忆形态 | 社区称「偏运行上下文/追加日志」**vs** 官方 memory 页列出 MEMORY.md / USER.md / dreaming 晋升 | 并列，社区条目标注层级 |
| C7 | arXiv 第六条职责措辞 | abs 页 `verification` **vs** 全文 `verification/governance` | 同论文两版差异，并列 |
| C8 | 迁移命令时效 | 本地件（2026-08-27）与远程（2026-09-29） | `hermes claw migrate` **内容一致，无冲突**；messaging `## Security` 仅本地有，多用户结论时效为 2026-08-27 |

---

## 6. 主线 T′（已由用户确认，写作硬约束）

> **不是产品同质，是术语同质。「多用户」一词三义。**

| | 「多用户」在其语境中的实际含义 | 关键原文 |
|---|---|---|
| OpenClaw | 同一信任域内的**协作**；明确非安全边界。多租户靠一租户一 Gateway 绕开，且明确无企业版 | `usability features, not security boundaries` / `One gateway per tenant` / `There is no enterprise edition.` |
| Hermes | 单机单所有者范围内的**准入 + 很窄的分级**（分档目前只管 slash 命令）+ profile 路由 | `The admin / user split` / `What the tiers gate today: slash commands` |
| Octop | **架构内建**的多用户（JWT + 行级归属 + RBAC + 按用户配额），限定家庭与小团队单实例 | `Agent ownership is enforced at the **row** level` / `households and small teams` |

**硬结论**：**多用户平台 ≠ 多租户平台**。
**层判断**：OpenClaw 与 Hermes **同层**（双向迁移 + 官方 17 轴对照 + 权威清单同归类）；Octop 与之是**同层不同重心**，不是「层不同」。

**写作硬约束**：后续任何章节**不得**不加限定语地使用「多用户」一词；首次出现必须指明是上表三层语义中的哪一层。

---

## 7. 下游交接

### 可直接用作骨架的三条轴
1. **术语轴**（主线）：多用户/多租户/准入分级的三义切分
2. **层内差异轴**：OpenClaw `runs on your own computer` / `personal assistant on a laptop` **vs** Hermes `It's not tied to your laptop`（$5 VPS / serverless）—— 同层内部最可直接回答「什么场景用哪个」的一根轴
3. **框架轴**：arXiv 六职责（观察/上下文/控制/动作/状态/验证与治理）作为**问对问题**的清单，配 awesome-list 的五类用途定位

### 可用素材位置
- Hermes 侧可直接复用：`workspace/hermes-agent/chapters/01_定位与核心理念.md`（已含 OpenClaw 竞品对照段）、`workspace/hermes-home-assistant/chapters/02-三方对照轴.md`（对照轴方法先例）
- OpenClaw 侧本轮已从零补齐（`research/openclaw/`）

### 禁止事项（传给下游 writer）
- 不得使用 P1 来源 #11、#14（均抓取失败，仅搜索摘要）
- 引用 OpenClaw 17 轴对照表时**必须标注「OpenClaw 单方制作」**，不得当作中立评测
- 引用 `workspace/hermes-agent/chapters/*` 的内容时须标为**本仓库二次加工**，不得标为官方口径
- 不得使用 Star 数作为选型依据

---

## 8. 开放问题

1. **Octop 轴未并入**（§3.3）—— 阻塞 P3 大纲，因为三方对照表需要第三列
2. **C1** Octop harness 开源状态裁决
3. `research/openclaw/community/01` 正文未抓全，「Hermes（大脑）+ OpenClaw（执行者）」协同架构**仅有标题与导语**，不足以支撑断言
4. **Hermes 侧对 OpenClaw 17 轴对照表的回应**：未找到（未检索 Hermes 是否有反向对照页）
5. **P1 流程教训尚未落库 `.learnings/`**（见 `01_explore_result.md` §3.1）
