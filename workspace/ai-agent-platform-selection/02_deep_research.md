# P2 深度素材 — 自托管 AI Agent 平台选型

- **运行**: `ai-agent-platform-selection`（learning-note-flow）
- **阶段**: P2 深度收集
- **日期**: 2026-09-29
- **状态**: 完成 — 三平台七轴齐备（Octop 轴见 §3.3）

---

## 1. 方法与范围

- 主线段落已定向验证并修正（见 `01b_thesis_verification.md`），采纳主线 **T′**（详见 §6）
- P2 由 3 个批量子代理按**七轴统一口径**提取 claim 级笔记；代理为 P2 前置验证轮的**续写**，不重读材料
- 全部 claim 落盘原文见 `research/{octop,openclaw,hermes,framework}/`
- 抓取走 `.claude/skills/research-collector/scripts/crawl.sh`（`WebFetch` 对相关域名被网络策略拦截）；Octop 侧改用 `curl https://raw.githubusercontent.com/...` 直取（`WebFetch` / `git clone` / codeload tarball 均被拒，与 `crawl.sh` 同一取数路径）

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
| `extra2/01` | **`start/why-openclaw/openclaw-and-hermes-agent`（官方 15 行属性对照表）** |

> **口径订正（2026-09-29）**：本节初稿把这张表记作「17 轴」。实测 `research/openclaw/extra2/01_docs_openclaw_ai.md` 中 `^|` 行共 **17 行**，其中含表头 1 行（`:15`）与分隔行 1 行（`:16`），**属性行实为 15 条**（`:17-31`）。现全库统一为「15 行属性对照表」；`01_explore_result.md`、`03_outline.md` 已同步订正。对照表出处、立场标注（OpenClaw 单方制作）与钉住的 commit（`6defe7eb6c`）均不变。

> **跨章口径统一（P4 验收，2026-09-29）**：P4 要求对「可照抄的配置块」做跨章比对（`workflow.md` 阶段 4）。两侧结果：
> 1. **配置键**：七章 **无围栏代码块**（全文停在「上手」深度，配置只用行内 code span），故无同名键多取值可统一；全库唯一的 `KEY=VALUE` 片段是 `TELEGRAM_ALLOWED_USERS=...`，仅出现 1 次，无冲突。
> 2. **冻结标签**：比对出 **1 处真实漂移**——Hermes 那一档在 ch.2 锚表写作「准入**与**很窄的分级」，在 ch.3/ch.7 写作「准入 **+** 很窄分级」。以 `03_outline.md:15` 硬约束行 + ch.2 §2.1 锚表（自称「全篇的锚」）为 canonical，**全库 33 处统一为「准入与很窄的分级」**（`01_explore_result.md` / `02_deep_research.md` / `03_outline.md` / 七章正文）。此为纯措辞归一，不涉及语义等价主张，故不标推断。
> 3. **其余冻结项复核**：层名（本地 CLI 阵营 / 个人助手 harness / 多用户平台）、另两档标签（不提供隔离 / 行级归属）、7 个 ACP runner 名单，跨章一致，无漂移。
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

### Octop — `research/octop/`（106 个文件，2.9 MB，顶层按仓库根镜像布局）
| 文件 | 对应内容 |
|---|---|
| `README_CN.md` / `README.md` / `AGENTS.md` | 定位与 Overview / 家庭共享 / 快速开始 / Roadmap |
| `CHANGELOG.md` | RBAC（`0.9.24`）与按用户配额（`0.9.33`）的引入记录 |
| `docs/architecture.md` | 五层分层、单进程启动树、`§ Per-user isolation`（行级归属） |
| `docs/adr/001-single-process-model.md` | 单进程决策与 Trade-offs |
| `docs/adr/002-database-backends.md` | SQLite / PG 控制面选型与限制 |
| `docs/configuration.md` / `memory-slim.md` / `acp.md` | 存储默认值与迁移边界 / 记忆维护的归身边界 / ACP 出入站 |
| `plugins/README_CN.md` | 插件契约与 `kind` 四类 |
| `src/octop/**`（79 个源文件） | `api/deps.py`、`api/common/agent.py`、`api/routers/**`、`infra/users/**` 等 |
| `tree.json` | GitHub API 全量文件树（3697 blobs） |
| `_crawl/` | `crawl.sh` 原生命名产物（带 `url` + `scraped_at`） |

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

**A6 与另两者的关系** — **官方专页对 Hermes 做 source-verified 对照（15 行属性）；Octop 零提及**
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

**A2「多用户」= 准入与很窄的分级 + profile 路由；无租户语汇**
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
- `| **MEMORY.md** | Agent's personal notes — environment facts, conventions, things learned | 2,200 chars (~800 tokens) |` / `| **USER.md** | User profile — your preferences, communication style, expectations | 1,375 chars (~500 tokens) |` — `research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15`
- `| **Capacity** | ~1,300 tokens total | Unlimited (all sessions) |` / `| **Cost** | Token cost in every prompt |` — 同上 `:302,304`
- **锚点说明（2026-09-29 补）**：该文件是本轮**重新抓取**的 Hermes 官方文档页 `https://hermes-agent.nousresearch.com/docs/user-guide/features/memory`。此前本节曾引用另一项目目录下的同名抓取件（`workspace/hermes-agent/research/gaps/06_...`，抓取于 2026-08-27），**内容逐字一致**、仅行号位移，现改为自包含锚点。旧路径不再引用。
- `**Dialectic reasoning** : After each conversation turn (gated by `dialecticCadence`), Honcho analyzes the exchange and derives insights about the user's preferences, habits, and goals.` — `research/04_..._honcho.md`
- Honcho 的「多 agent」是同一用户的多个 agent：`When multiple Hermes instances talk to the same user (e.g., a coding assistant and a personal assistant), Honcho maintains separate "peer" profiles.` — 同上 ← **再次印证「多用户」在不同产品里含义不同**
- 闭环：`A closed learning loop`（agent 策展记忆 + 自主技能创建 + 技能自我改进 + FTS5 会话检索 + Honcho 建模）— README
- 限制：`Don't point two agent processes at the same Hermes home directory. ... Memory is scoped per [profile] by design` — `research/hermes/05_hermes-agent_nousresearch_com_memory.md:18`

**A5 扩展** — 技能是按需加载的知识文档，agent 可自建自改自删
- `Skills are on-demand knowledge documents the agent can load when needed. They follow a **progressive disclosure** pattern to minimize token usage` — `research/hermes/06_hermes-agent_nousresearch_com_skills.md:9`
- `The agent can create, update, and delete its own skills via the `skill_manage` tool. This is the agent's **procedural memory**` — 同上 `:1066`
- 默认自由写：`By default the agent writes skills freely — including from the [background self-improvement review]` — 同上 `:1091`
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
- 记忆代价：`| **Token cost** | Fixed per session (~1,300 tokens) | On-demand (searched when needed) |` — `research/hermes/05_hermes-agent_nousresearch_com_memory.md:307`
- `The review fork can burn a meaningful share of total tokens on busy hosts.` — 同上 `:456`
- 多路复用的代价：`Collapsing such a fleet replaces a kernel-enforced boundary (file ownership, `User=`) with in-process isolation, which is an operator's decision.` — `multi-profile-gateways`

---

### 3.3 Octop

#### 两个遗留未决点的裁决

**裁决 1 —— `Read access and agent use in chat are never gated.` 的准确含义**

裁决：**是「权限键管管理页 / 写操作，数据隔离另由 `user_id` 归属保证」，但必须加一条修正——admin 域模块（users / user_roles / invites）连读也受权限键管。** 三层互相独立、不互相替代：

| 层 | 机制 | 锚点 |
|---|---|---|
| ① 准入 | 全局 JWT 中间件 + 白名单豁免。可引原文：`# Paths that bypass JWT middleware (setup wizard, health, login).`，其下列 `_JWT_EXEMPT_PREFIXES` 与 `_JWT_EXEMPT_EXACT`（`/api/health`、`/api/auth/{login,captcha,oidc/*,oauth/*,invite/validate,invite/redeem}`、`/api/docs`、`/api/openapi.json` 等） | `src/octop/api/deps.py:65-89`。⚠️ **中间件本体 `src/octop/api/middleware/jwt_auth.py` 未落盘**（该目录抓取为空），其存在由 `src/octop/api/app.py:16`（`from octop.api.middleware.jwt_auth import install as install_jwt_auth`）、`:137`（`install_jwt_auth(app, server)`）与 `docs/api.md:37` 佐证；**先前引用的逐字句 `Require JWT for all /api/* routes except an explicit allowlist.` 无法核对，已弃用，不得再引用** |
| ② 模块权限键 | `A permission is a module key (e.g. "browser", "users"). Possessing a key grants access to that module's management page and write/configure actions.` | `src/octop/infra/users/permissions.py:3-4` |
| ③ 归属（真正的隔离） | `Agent ownership is enforced at the **row** level (agents.user_id matched against the caller`；`if row.user_id is None or row.user_id != user.id: raise OctopError(ErrorCode.FORBIDDEN, "agent not owned by user")`；`_user_may_access` = 本人 / `agent_is_shared` / admin 三选一 | `docs/architecture.md:71`、`src/octop/api/common/agent.py:18-23, 26-31, 51-53` |

- **同模块内「读不加键、写加键」的硬证据**：`GET ""`(List installed plugins) 只用 `current_user`（`src/octop/api/routers/plugins.py:99-104`），而 `POST /reload` 用 `require_permission("plugins")`（`:110`）；`GET /market` 只用 `current_user`（`:207`），而 `POST /market/{plugin_id}/install` 用 `require_permission("plugins")`（`:221`）
- ⚠️ **修正（推翻该句的字面读法）**：admin 域的可读端点**确实加键** —— `GET ""`(list users) → `require_permission("users")`（`src/octop/api/routers/users.py:270-272`）、`GET /{user_id}` → 同（`:431-435`）、`GET ""`(list role templates) → 同（`src/octop/api/routers/user_roles.py:183-186`）。→ **「读访问完全不加门」不成立**
- 「agent use in chat never gated」的实证：聊天 / 会话读端点只挂 `Depends(current_user)`，无任何 `require_permission` — `src/octop/api/routers/chat/history.py:104,150,166,217,253,289`

**裁决 2 —— 单进程模型在多用户并发下的实际瓶颈**

裁决：**官方只给定性权衡，未给任何并发量 / 吞吐 / 压测数字。**

- `| Simple deployment (one process, one port) | Heavy CPU tasks block the event loop |` — `docs/adr/001-single-process-model.md:28`
- `| Zero external dependencies | Vertical scaling only (one machine) |` — 同上 `:27`
- `| Fast local dev | No horizontal worker scaling |` — 同上 `:29`
- `- **SQLite is sufficient:** Concurrent writes are rare (one writer per agent at a time); WAL mode handles the load.` — 同上 `:20`
- `- Single active Octop writer; no multi-instance write promise.` — `docs/adr/002-database-backends.md:44`
- 未来的扩展缝：`Future scale-out would require extracting the worker into a separate process and adding a queue; that seam is already partially visible in infra/gateway/processor.py.` — `adr/001` §Consequences
- → **无法据以判断实际可用人数上限**；选型时只能按「单机垂直扩展」这一条硬边界处理

#### 七轴

**A1 定位与产品主语** — 主语是「一台机器上的实例」，收益归于「每个用户」
- `支持多用户、多 Agent 的自托管 AI 助手 — 更聪明，更懂你。` — `README_CN.md:6`
- `Octop is a self-hosted AI assistant platform for households and small teams.` — `README.md:69`（中文同口径 `README_CN.md:68`）
- `同时为每个用户配备一组可按场景切换的专业 Agent。` — `README_CN.md:70`
- agent-facing 手册同调：`**Octop** — self-hosted AI assistant platform (multi-user, multi-agent).` — `AGENTS.md:37`
- **单用户用法被官方承认**：`**个人助理** — 让专属 Agent 帮你写周报、整理资料、定日程，记忆随工作区长期保留。` — `README_CN.md:75`

**A2「多用户」= 单实例内的多用户 + 行级归属；无租户语汇**
- 准入非自助注册：`交互式向导会在 ~/.octop/ 下创建 SQLite 数据库、JWT 密钥，并引导你设置首个管理员账号。` — `README_CN.md:259`
- 邀请制（1–365 天）：`class InviteCreateBody(BaseModel):` / `expires_in_days: int = Field(` — `src/octop/api/routers/invites.py:55,57`
- 分级：`role: str  # role-template public id: admin | user | custom ULID` — `src/octop/infra/users/identity.py:20`
- 权限键是枚举式模块目录（channels / connectors / knowledge_bases / terminal / browser / desktop / mobile / users / sso / plugins / security / backup / tls / update …）— `src/octop/infra/users/permissions.py:59`
- 归属粒度：`每位用户可创建多个专家；各自拥有独立工作区、供应商、通道和定时任务` — `README_CN.md:117`
- 但隔离**可由 owner 主动放宽**：`**专家共享** — 支持用户将自有专家共享给其他用户使用` — `README_CN.md:162`
- **官方模型是「一个管理员 + 全家共用」的家庭模型，不是平等多租户**：`**家庭共享** — 一个管理员账号，全家共用；按成员分配不同 Agent 与专家角色` — `README_CN.md:76`
- 按用户资源策略：`Per-user named policies: workspace root, token quota, and future rows.` — `src/octop/infra/users/resource_policy.py:1`
- **「租户」概念不存在**：文档全库检索无 `tenant`；唯一 1 处是消息路由字段把 agent id 复用为 tenant id —— `tenant_id=agent_id,` — `src/octop/api/routers/chat/turn.py:348` → **不得读成租户模型**（与 Hermes 的 `tenant` 假阳性**结构完全对称**：两侧各有且仅有一处，都是消息字段）
- 治理能力是增量加入，非初版即有：`权限：新增按用户模块权限（RBAC）及管理员绕过` — `CHANGELOG.md:396`（`## [0.9.24] - 2026-08-15`）；`按用户限制存储根目录与 Token 配额；创建专家可带默认知识库与连接器` — `CHANGELOG.md:192`（`## [0.9.33] - 2026-09-11`）

**A3 架构** — 全栈一个进程，无独立 worker、无外部队列；per-user runtime 是进程模型的前提
- `The whole stack is one process. There is no separate worker, no` — `docs/architecture.md:32`
- `Octop needs to run a web server, a CLI, per-user Agent runtimes, IM channel connections, and cron schedulers simultaneously.` — `docs/adr/001-single-process-model.md:10`
- `Everything runs in a single Python process served by uvicorn. There is no external queue (Redis, RabbitMQ, Celery), no separate worker process` — 同上 `:14`
- `Octop 不依赖外部消息队列或中间件，而是通过进程内的 HarnessProcessor 统一路由所有入口` — `README_CN.md:107`
- 重启语义：`单进程架构。重启后从控制面数据库重建状态（默认本地 SQLite；可选 PostgreSQL）。` — `README_CN.md:483`
- 控制面后端：`| OCTOP_DATABASE_DRIVER | sqlite | postgresql | sqlite | Storage backend |` — `docs/configuration.md:158`；`- Greenfield only — no SQLite→PG data migrator.` — `docs/adr/002-database-backends.md:45`
- 部署形态：脚本安装 / PyPI / Docker / 桌面客户端（Wails）/ 飞牛 NAS `Octop-fnos-docker-<version>.fpk` — `README_CN.md` 快速开始

**A4 记忆** — 独立库（octop-memory），分层 + 全文检索，落在 agent 工作区，随工作区迁移
- `| 🧠 | **可迁移记忆系统** | 基于 Octop Memory，记忆随工作区迁移 |` — `README_CN.md:56`
- `**Octop Memory** — 分层记忆与全文检索，让 Agent 的记忆随工作区一同迁移。` — `README_CN.md:104`
- 默认落盘：`- Control plane SQLite → agent memory stays {workspace}/memory.sqlite` — `docs/configuration.md:187`
- PG 路径：`Control plane PostgreSQL → agent memory **defaults to the same DSN**`，按 `agent_<id>` schema 分片 — 同上 `:189`；`Agent memory DDL is owned by octop-memory.` — `docs/architecture.md:115`；`no automatic SQLite→PG memory data migration.` — `docs/configuration.md:200`
- **归身边界延伸到运维动作**：`对话的 --all 与本地管理 CLI 范围不同：只选当前用户自己的 agent，不包含其他用户或共享 agent。` — `docs/memory-slim.md:87`
- 限制：`PG 瘦身，只支持 SQLite；本次未执行整理，可以继续聊天。` — `docs/memory-slim.md:57`；`外部 IM 的记忆维护需要已验证的发送者权限，暂未开放。` — `README_CN.md:422`

**A5 扩展** — 插件四类 `kind`，默认全局关闭需管理员开启；技能按 agent 挂载
- `| demo-turn-logger | hook | 注册 AgentMiddleware，在模型调用前后打日志 |` — `plugins/README_CN.md:17`（`kind` = tool / skill / hook / **ui**）
- **默认关闭是治理设计**：`并在 config.json 里写成 **全局关闭**；管理员在 Dashboard 插件页打开后再给 Agent 用。` — `plugins/README_CN.md:9`
- 契约：`├── plugin.yaml    # id、version、name、kind、entry；可选 icon / ui` — 同上 `:26`
- 技能：`@router.get("/agents/{agent_id}/skills")` — `src/octop/api/routers/skills.py:454`；另有全局技能包 `summary="Replace global skill packages mounted on an agent",` — 同上 `:531`
- 子智能体：`@router.get("/subagent-catalog", summary="List bundled subagent definitions")` — `src/octop/api/routers/subagents.py:112`
- 外部服务：`通过 **Connector**（OAuth + MCP）接入外部服务，通过 **ACP** 与 IDE / 终端 AI 工具双向协作。` — `README_CN.md:43`
- 安全层另计（不属扩展层）：`JWT 多用户隔离、工具审批、Shell 命令防护与敏感信息脱敏，数据留在本地` — `README_CN.md:53`

**A6 与另两者的关系** — **双向零提及**；唯一命名的外部 agent 工具是本地 CLI（走 ACP）
- 全库检索 `openclaw|hermes`（`README` / `README_CN` / `AGENTS.md` / `docs/` / `plugins/`）**零命中**
- **修正**：命名的外部 agent 工具**只有 ACP runner**，内置 **7 个**：`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi` — `docs/acp.md:29-38`（先前写成「唯一是 `claude_code`」有误，实为一张 7 行表；由 chapter-writer 回原文核对时发现）
- 方向定义：`| **Outbound** | OpenCode, CodeBuddy, … | Octop (acp_runner tool) | Octop agent delegates coding tasks |` — `docs/acp.md:8`
- → **Octop 的邻近参照物是「本地 CLI 阵营」（Claude Code / Codex），不是 OpenClaw / Hermes**；且这份关系是**集成**（委派编码任务），不是竞品对照
- 与 OpenClaw 侧对称：OpenClaw 官方为 Hermes 做了 15 行属性对照专页；Octop 未被 OpenClaw / Hermes 任一方提及，Octop 亦不提它们

**A7 运维成本与官方声明的限制**
- 收益 / 代价成对声明：`| Zero external dependencies | Vertical scaling only (one machine) |`、`| Simple deployment (one process, one port) | Heavy CPU tasks block the event loop |`、`| Fast local dev | No horizontal worker scaling |` — `docs/adr/001-single-process-model.md:27-29`
- 运维负担优先于扩展：`Adding Redis or a process supervisor doubles the ops burden for the primary audience.` — 同上 §Rationale
- 插件 UI 必须预构建：`请一并打入预构建的 ui/dist/（**不要**依赖服务器执行 npm install）。` — `plugins/README_CN.md:98`
- 升级：`refuse cross-engine restore.` — `docs/adr/002-database-backends.md` §Control-plane adapter
- 资源门槛：`现代多核 CPU，并预留数 GB 内存供进程与模型/Embedding 缓存使用` — `README_CN.md` 环境要求
- **Roadmap 未完成项**：`- [ ] **Managed Agents** — 平台托管的 Agent 生命周期（开通、伸缩与运维），无需自行维护完整自托管栈。` — `README_CN.md:172`；`- [ ] **云边端一体** — 本地运行 Octop，同时可将选定任务调度到云端执行` — 同段
- 进行中项：移动端客户端 `*（内测中）*`、AgentTeams 仍 Beta — `README_CN.md` 进行中段

---

## 4. 横向框架底稿

### 4.1 arXiv 2606.20683 — agent 能力是「模型–harness 配对」的属性

- 核心论断（逐字，取贡献句原文全句）：`We analyze the limits of model-centric scaling for long-horizon task completion and argue that agent performance is a property of the model–harness pairing.`；`Benchmark scores should therefore be interpreted as outcomes of a _model–harness pairing_`
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
| C1 | Octop harness 核心是否开源 | 社区称「核心未开源」**vs** 三库已于 2026-09-24 公开 | **已裁决**：主仓库本身即含 harness 源码（本轮实抓 `src/octop/**` 79 个源文件），另有三库独立公开。原「核心未开源」说法在 2026-09-24 之后**不成立** |
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
| Hermes | 单机单所有者范围内的**准入与很窄的分级**（分档目前只管 slash 命令）+ profile 路由 | `The admin / user split` / `What the tiers gate today: slash commands` |
| Octop | **架构内建**的多用户（JWT + 行级归属 + RBAC + 按用户配额），限定家庭与小团队单实例 | `Agent ownership is enforced at the **row** level` / `households and small teams` |

**硬结论**：**多用户平台 ≠ 多租户平台**。

**新增一条可分级、可验证的轴 —— 「多用户」的隔离强度（三方形成梯度）**：

| 强度 | 平台 | 官方措辞 |
|---|---|---|
| 明确声明**不提供**隔离 | OpenClaw | `usability features, not security boundaries` / `It is not an authorization or isolation boundary.` |
| 准入与很窄的分级 | Hermes | `The admin / user split` / `What the tiers gate today: slash commands` |
| **行级归属**（真正的数据隔离，且隔离边界延伸到运维动作） | Octop | `Agent ownership is enforced at the **row** level` / `只选当前用户自己的 agent，不包含其他用户或共享 agent` |

**租户语汇的分布本身也是证据**：三者中**只有 OpenClaw** 有租户词汇（`experimental per-tenant fleet cells`），且自带 experimental 标注；Hermes 与 Octop **各有且仅有一处** `tenant`，都是**消息路由字段**（Slack workspace / `tenant_id=agent_id`），均**不得**读成租户模型。

**层判断**：OpenClaw 与 Hermes **同层**（双向迁移 + 官方对照（15 行属性） + 权威清单同归类）；Octop 与之是**同层不同重心**，不是「层不同」。**一条旁证**：Octop 命名的外部 agent 工具只有 ACP runner，内置 7 个（`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi`，`docs/acp.md:29-38`），全是编码类且以命令行接入 —— 即它的邻近参照物落在**本地 CLI 阵营**（把 7 个逐个归入该层属**推断**，官方未使用这一分类词），而 OpenClaw 与 Hermes 互为对照物 —— 三方各自站位，在「谁把谁当参照」上再次显形。

**写作硬约束**：后续任何章节**不得**不加限定语地使用「多用户」一词；首次出现必须指明是上表三层语义中的哪一层。

---

## 7. 下游交接

### 可直接用作骨架的四条轴
1. **术语轴**（主线）：多用户 / 多租户 / 准入分级的三义切分
2. **隔离强度轴**：不提供隔离（OpenClaw）→ 准入与很窄的分级（Hermes）→ 行级归属（Octop）
3. **层内差异轴**：OpenClaw `runs on your own computer` / `personal assistant on a laptop` **vs** Hermes `It's not tied to your laptop`（$5 VPS / serverless）—— 同层内部最可直接回答「什么场景用哪个」的一根轴
4. **框架轴**：arXiv 六职责（观察 / 上下文 / 控制 / 动作 / 状态 / 验证与治理）作为**问对问题**的清单，配 awesome-list 的五类用途定位

### 可用素材位置
- Hermes 侧可直接复用：`workspace/hermes-agent/chapters/01_定位与核心理念.md`（已含 OpenClaw 竞品对照段）、`workspace/hermes-home-assistant/chapters/02-三方对照轴.md`（对照轴方法先例）
- OpenClaw 侧本轮已从零补齐（`research/openclaw/`）

### 禁止事项（传给下游 writer）
- 不得使用 P1 来源 #11、#14（均抓取失败，仅搜索摘要）
- 引用 OpenClaw 15 行属性对照表时**必须标注「OpenClaw 单方制作」**，不得当作中立评测
- 引用 `workspace/hermes-agent/chapters/*` 的内容时须标为**本仓库二次加工**，不得标为官方口径
- 不得使用 Star 数作为选型依据
- **不得**把聊天端点只挂 `Depends(current_user)` 写成「Octop 读访问无权限控制」——admin 域读端点确实要 `require_permission`（`users.py:270-272` 等），准确说法是**权限键管管理页 / 写操作，数据隔离由 `user_id` 行级归属另负**
- **不得**给出 Octop 的并发人数上限（官方无任何容量数据）
- **不得**把 Hermes 或 Octop 那一处 `tenant` 字段读成租户模型（两者都是消息路由字段）

---

## 8. 开放问题

1. **Octop 并发容量上限**：官方未发布任何并发用户数 / 吞吐 / 压测数据，只有 `Vertical scaling only`、`No horizontal worker scaling`、`one writer per agent at a time` 这类定性表述 → 笔记中**不得给出人数上限**，只能给硬边界
2. **多用户治理的版本边界**：RBAC（`0.9.24`）与按用户配额（`0.9.33`）确为增量加入，但「多用户」本身是否 1.0 之前即存在未验证（`docs/versioned-history.md` 未抓）
3. **Octop 归属的完整表清单**：只确认 `agents.user_id`，`knowledge_bases` / `usage_log` / `audit_log` 为间接证据，未逐表核对
4. `research/openclaw/community/01` 正文未抓全，「Hermes（大脑）+ OpenClaw（执行者）」协同架构**仅有标题与导语**，不足以支撑断言
5. **Hermes 侧对 OpenClaw 15 行属性对照表的回应**：未找到（未检索 Hermes 是否有反向对照页）
6. **P1 流程教训尚未落库 `.learnings/`**（见 `01_explore_result.md` §3.1）
