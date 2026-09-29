# 主线验证（P2 前置，定向反驳）

- **运行**: `ai-agent-platform-selection`
- **日期**: 2026-09-29
- **方法**: 3 个代理，每个负责一个平台，指令为**尝试反驳**子命题，默认裁决为「存疑」
- **被验证的原始论点 T**: 「OpenClaw 与 Hermes 同层（单机常驻个人助手 / agent harness）；Octop 是另一层（多用户平台）。」

---

## 裁决汇总

| 子命题 | 裁决 | 后果 |
|---|---|---|
| T1 Octop 是「面向多用户的平台」，多用户是一等公民 | **支持** | 保留，但需加规模限定 |
| T2 OpenClaw 处于「个人助手 / harness」层，多用户是配置项 | **支持**（措辞需修正） | 修正为「多用户协作是一等公民功能，多租户才是绕行隔离」 |
| T3 Hermes 同层 + `hermes claw migrate` 存在 + **Hermes 无官方多用户** | **反驳** | 合取命题的第三项被官方文档证伪，必须修正 |

---

## 关键修正 1：`hermes claw migrate` 成立 —— 同层判断未被动摇

最强证据，两版 README 与源码三方交叉一致，**无冲突**：

| 引文 | 锚点 |
|---|---|
| `## Migrating from OpenClaw` | `workspace/hermes-agent/research/06_github_com.md:195`（本地抓取件，scraped_at 2026-08-27） |
| ``hermes claw migrate # Migrate from OpenClaw`` | 同上 |
| `If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.` | 远程 README 当前版（retrieval 2026-09-29） |
| `"""hermes claw — OpenClaw migration commands."""` | `hermes_cli/claw.py` 第 1 行（源码） |
| `_OPENCLAW_DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot")` | `hermes_cli/claw.py` |
| `_OPENCLAW_SCRIPT = ... / Path("migration", "openclaw-migration", "scripts", "openclaw_to_hermes.py")` | `hermes_cli/claw.py` |

→ 本地件（2026-08-27）与远程（2026-09-29）内容一致，仅代码块语言标注差异，**不需并列记录冲突**。

---

## 关键修正 2：我原来的「Hermes 无官方多用户」是**错的**

Hermes 官方文档明确有多用户能力：

| 引文 | 锚点 |
|---|---|
| `**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` | `workspace/hermes-agent/research/07_raw_githubusercontent_com.md:327`（`## Security`） |
| `TELEGRAM_ALLOWED_USERS=123456789,987654321` | 同上 `:331` |
| `### Admins vs Regular Users` / `Every allowed user falls into one of two tiers per scope (DM vs group/channel):` | 同上 `:367`, `:371` |
| `Allowlists answer "can this person reach the bot at all?" The **admin / user split** answers "now that they're in, what are they allowed to do?"` | 同上 `:369` |
| `Sender routing selects a profile; it is not deny-by-default authorization.` | `/docs/user-guide/multi-profile-gateways`（页面 title `Running Many Gateways at Once`） |
| `To give one person a privileged profile and everyone else a restricted one, declare the privileged sender route first, add a platform-wide catch-all route to the restricted profile after it` | 同上 |

**但**（必须并列记录）：
- 全库检索 `multi-tenant` / `multitenant` / `multi-user` / `SaaS` —— **零命中**；唯一 1 处 `tenant` 指的是**消息平台的**租户命名空间（Slack workspace），不是 Hermes 自身的租户模型：
  - `Sender ids are also namespaced per tenant on some platforms — a Slack user id is workspace-local` — `research/hermes/02_..._multi-profile-gateways.md:643`
  - → 不得把这一处读成「Hermes 有租户能力」
- 上述能力全部落在**单机、单进程、单所有者**范围内，是**准入与分级**，不构成平台级多租户
- **分级的实际边界很窄**（P2 补）：
  - `**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.` — `research/hermes/03_raw_githubusercontent_com_messaging-index.md:378`
  - → Admin/Regular 分档**目前只管 slash 命令**，普通对话不受限
- **sender 路由不是授权**（P2 补）：
  - `Sender routing selects a profile; it is not deny-by-default authorization.` — 同上 `:645`
- Hermes 自身的定位语言仍是个人助手：`A personal assistant on one Telegram bot and a coding agent on another`（multi-profile-gateways 页面示例）

→ 因此我的措辞错误在于把「多用户」当成了一个二值属性。**精确说法：Hermes 有官方多用户准入/分级，没有多租户。**

---

## 关键修正 3：三方**都**「支持多用户」，但说的是三件不同的事

这是本次验证最有价值的产出。三方原文并置：

### OpenClaw —— 同一信任域内的多人协作是一等公民；多租户靠「一租户一实例」绕开

| 引文 | 锚点 |
|---|---|
| `or as a shared team deployment; configuration is the only difference` | README.md |
| `team operation is configuration, not a separate edition` | `docs.openclaw.ai/start/teams` |
| `A gateway is one trust domain.` | 同上，小节 `One trust boundary` |
| `serve mutually untrusted people or organizations, run one gateway per tenant` | 同上 |
| `collaboration guardrails inside the boundary, not isolation between adversaries` | 同上 |
| `not hostile multi-tenant isolation inside one shared Gateway` | `docs.openclaw.ai/gateway/multi-tenant-hosting` |
| `There is no enterprise edition.` | `docs.openclaw.ai/start/why-openclaw` |
| `A tenant self-service portal, billing plane, or delegated administration UI`（列于 "Fleet does not provide these surfaces:" 之下） | `gateway/multi-tenant-hosting` → `Current scope` |
| `Fleet is experimental` | 同上 |

**反证/张力（如实并列）**：`openclaw fleet` 是真实存在的多租户管理 CLI（`openclaw fleet create|status|upgrade|rm`，cell = 独立容器/状态/凭据/网络），构成一个多租户产品面，但被官方标注 experimental 且被 `Current scope` 明确限制。另有企业治理措辞出现于 why-openclaw（`Foundation-convened councils on ... enterprise deployment`、`the most mature, battle-tested agent for anyone, individual or enterprise, to build on`）—— 属**治理/生态**表述，非多租户产品定位。

### Hermes —— 单机单所有者范围内的准入 + 分级 + profile 路由

见「关键修正 2」。无多租户语汇。

### Octop —— 多用户是**架构内建**，但规模口径限定为家庭与小团队

| 引文 | 锚点 |
|---|---|
| `a self-hosted AI assistant platform for multiple users and agents` | `docs/architecture.md` 开篇 |
| `Every request is authenticated via JWT and resolved to a `User` row.` | `docs/architecture.md` §2 Per-user isolation |
| `Agent ownership is enforced at the **row** level` | 同上 |
| `Octop is a self-hosted AI assistant platform for households and small teams.` | README.md（英文）`📌 Overview` |
| `Vertical scaling only (one machine)` / `No horizontal worker scaling` | `docs/adr/001-single-process-model.md` §Trade-offs |
| `Single active Octop writer; no multi-instance write promise.` | `docs/adr/002-database-backends.md` §Control-plane adapter |
| `User-scoped custom MCP tools: (user_id, server_name, fingerprint) -> tools` | `src/octop/infra/agents/manager.py` |
| `Per-user named policies: workspace root, token quota, and future rows.` | `src/octop/infra/users/resource_policy.py` |

**需并列记录的歧义句**（字面可被读成「读访问不加门」，与行级归属共同解读时应为「权限键管管理页/写操作，数据隔离另由 user_id 归属保证」）：
- `Read access and agent use in chat are never gated. ``admin`` bypasses all.` — `src/octop/infra/users/permissions.py`

**其他限定**：RBAC 与按用户配额是后续版本增量加入（CHANGELOG `## [0.9.24] - 2026-08-15`、`## [0.9.33] - 2026-09-11`）；官方主动提供跨用户共享能力（`is_shared` / `user_id IS NULL`）；桌面端只是同一多用户服务端的 Wails 外壳，**没有独立的单用户模式**（单用户 = 只有一行 user 记录）。

---

## 修正后的主线 T′（建议采纳）

原 T 的问题在于把「多用户」当成二值属性，并据此断言 Octop 在「另一层」。修正后：

> **不是产品同质，是术语同质。「多用户」这个词在三个项目里指三件不同的事**——OpenClaw 指同一信任域内的协作（多租户靠一租户一实例绕开，且明确无企业版）；Hermes 指单机单所有者的准入与分级；Octop 指架构内建的多用户（JWT + 行级归属 + RBAC + 按用户配额），但官方限定为家庭与小团队单实例。
>
> 因此功能清单必然叠影——**大家都在同一批词上做不同的事**。选型困惑的根源是「同词异指」，而不是「产品雷同」。

**必须建立的区分**：**多用户平台 ≠ 多租户平台**。
- Octop = 多用户平台（家庭 / 小团队，单实例，垂直扩展）
- OpenClaw = 明确**拒绝**做多租户（`not hostile multi-tenant isolation inside one shared Gateway`），多租户靠一租户一 Gateway
- Hermes = 不在这条轴上（无 tenant 语汇）

**关于「层」**：OpenClaw 与 Hermes 同层成立（`hermes claw migrate` 未被撼动）。Octop 与它们的差异**不在「有更多用户」**，而在「多用户是产品的组织原则」。但以此断言「完全不同层」**证据强度不够** —— 更准确的说法是：**同层不同重心**。原 T 中「拆成两层来问」的建议仍成立，只是理由要换。

---

## 未解决 / 待补

- Octop 的 `Read access and agent use in chat are never gated.` 与行级归属的准确关系（需读 `permissions.py` 全文与调用点）
- OpenClaw `Fleet` 的实际成熟度（experimental 具体到什么程度）
- Hermes multi-profile 路由与 OpenClaw 多用户模式的**具体机制对照**（两者都能「一人一 profile」，差异在哪）
- Octop 单进程模型在多用户并发下的实际瓶颈（§P1 缺口，未解）
