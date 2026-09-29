# 学习笔记大纲：《自托管 AI Agent 平台选型（Octop / OpenClaw / Hermes）》

- **笔记类型**：对比笔记（选型决策型），辅以可落地的配置片段、目录结构与机制锚点
- **目标读者**：已实际用过 OpenClaw / Hermes 类 agent 的读者（有了解，非零基础）；核心诉求是**选型判断依据**，不是单个产品入门教程
- **学习深度**：上手 —— 同类能力给出可比的具体证据（原文引文 + 文件锚点），不做源码级剖析，不实际部署
- **总字数预估**：约 12,400–15,100 字
- **章节总数**：7
- **贯穿全文的主轴**：**不是产品同质，是术语同质。** 三方在同一批词（「多用户 / 多租户 / 隔离 / 权限」）上做的是不同的事，所以功能清单必然叠影；选型困惑的根源是**同词异指**，而不是产品雷同。

**主轴的因果链（第 7 章是前六章的收口，不是另起的建议清单）：**

第 1 章**先建立坐标**——按「是否常驻服务 × 服务的用户数是单数还是复数」把 agent 分成三层（本地 CLI 阵营 / 个人助手 harness / 多用户平台），再指出「感觉都一样」是**范畴错误**（把不同层的东西放进同一张功能清单对读）→ 第 2 章定位错因：**「多用户」一词三义**，三方原文并置 → 第 3 章把这三义翻译成一条**可测量、可排序的隔离强度梯度**（不提供隔离 → 准入 + 很窄分级 → 行级归属）→ 第 4 章在已被判定**同层**的 OpenClaw / Hermes 内部，找出第一根可直接决策的差异轴（部署姿态：本机 vs 不绑本机）→ 第 5 章说明 Octop 的「多用户」**不是同一根轴上的更强档，而是另一个问句的答案**（单实例多用户平台 vs 单用户助手）→ 第 6 章用「谁引用谁 / 谁迁移谁 / 谁零提及」把三方的站位显形，作为对前五章的反向校验 → 第 7 章收敛成决策树，落到读者的真实场景。

**全文硬约束（来自 `02_deep_research.md` §6、§7）：**
- 任何位置**不得**不加限定语地使用「多用户」；首次出现必须指明是三层语义中的哪一层（同一信任域内的协作 / 准入与很窄的分级 / 行级归属）。
- 不引用 P1 来源 #11、#14（抓取失败，仅搜索摘要）。
- 引用 OpenClaw 15 行属性对照表时必须标注「OpenClaw 单方制作」。
- 引用 `workspace/hermes-agent/chapters/*` 时必须标为「本仓库二次加工」。
- 不使用 Star 数作为选型依据。
- 不把聊天端点只挂 `Depends(current_user)` 写成「Octop 读访问无权限控制」。
- 不给 Octop 的任何并发人数上限（官方无容量数据）。
- 不把 Hermes / Octop 各那一处 `tenant` 字段读成租户模型（两者都是消息路由字段）。

---

### 第 1 章 为什么「感觉都一样」是范畴错误 —— 从功能清单叠影说起

- **篇幅**：中，约 1,800–2,400 字
- **回答什么**：agent 领域的**层**怎么分（本地 CLI 阵营 / 个人助手 harness / 多用户平台），以及为什么「OpenClaw 和 Hermes 看起来干的是同一件事」不是产品缺陷，而是**比较方法本身失效**；为什么在「同类」之间做二选一是伪命题，选型必须往上问一层。
- **不回答什么**：不介绍任何一方的功能列表，不给出任何选型结论，不比较三者优劣；**不展开第 1 层（本地 CLI 阵营）**。
- **素材引用**：
  - `02_deep_research.md` §4.1（arXiv 2606.20683：agent 性能是**模型–harness 配对**的属性；`a task is not merely an application label but a pressure profile over observation, context, control, action, state, and governance`；六职责表）
  - `02_deep_research.md` §4.2（awesome-list 五类分类，`Each project appears once, under the category that best matches its main use.`；**`coding agents` 是独立一类**，与 OpenClaw / Hermes 所在的 `AI coworkers and teammates` 节并列）
  - `02_deep_research.md` §3.3 A6（ACP 事实：Octop 命名的外部 agent 工具**只有 ACP runner，内置 7 个**——`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi`，方向为 **outbound** 委派，`research/octop/docs/acp.md:8,29-38`。**注意不是「唯一是 `claude_code`」**）
  - `02_deep_research.md` §5 C2（Star 数互相矛盾，标注不可靠，不作选型证据）
  - `00_intent.md`「诊断假设」段（工具先于场景落位）
  - 锚点：`research/framework/13_arxiv_2606.20683v1_fulltext.md`、`research/framework/abs/01_arxiv_org.md`、`research/framework/17_awesome-ai-agent-platforms_README.md`
- **示例**：**有**。① **三层坐标表**（新增，列：层 / 判据① 是否常驻服务 / 判据② 用户数是单数还是复数 / 代表 / 本文处理方式）；②「六职责压力剖面」对照表（同一职责在三个平台由谁承担），用来演示「问对问题」的清单长什么样；③「功能清单叠影示意」小表，说明为什么列功能必然撞车。
- **写作要点**：
  1. **先建立坐标，再谈范畴错误**：开篇先给出分层判据，再说明「感觉都一样」之所以是范畴错误，正是因为把不同层的东西放进了同一张清单。
  2. **给出判据而不是清单**：三层的划分必须落在**同一根轴的两问**上——① 是不是常驻服务（进程内 CLI 用完即退 vs 常驻 gateway / 服务进程）② 服务的用户数是单数还是复数。让读者看到这是**一根轴上的三段**，不是三个并列的类别。
  3. 用 arXiv 的**压力剖面**透镜替换「功能清单」透镜：比较单位从「有什么功能」变成「同一职责谁来扛」。
  4. 明确写出两组**看起来同层**的客观证据（awesome-list 同归类；作者自己把 OpenClaw / Hermes 当同类用），为第 2 章的术语切分铺路。
  5. 单独一段处理 Star 数：**明确标注其不可作为选型依据**（§5 C2），并说明为何有人拿它当依据。

**（本章落点）先建立坐标：三层归位**

判据是一根轴上的两个问题，而不是三条并列的分类标准：

| 层 | 判据① 是否常驻服务 | 判据② 服务的用户数 | 代表 | 本文处理方式 |
| --- | --- | --- | --- | --- |
| 第 1 层 本地 CLI 阵营 | 否 —— 进程内启动、用完即退，不是常驻服务 | 单数 | Claude Code / Codex CLI 等 | **只作坐标系，不展开** |
| 第 2 层 个人助手 harness | 是 —— 常驻 gateway / 长驻进程 | 单数 | OpenClaw、Hermes | 本文比较对象 |
| 第 3 层 多用户平台 | 是 —— 常驻服务，单实例承载多用户 | 复数 | Octop | 本文比较对象 |

- **判据来源与证据边界（必须显式写出）**：这一层的证据在 `02_deep_research.md` 中**最弱**，只能引用两处 —— §4.2 的 awesome-list 五类分类（其中 `coding agents` 是**独立一类**，与 `AI coworkers and teammates` 并列），以及 §3.3 A6 的 ACP 事实（Octop 命名的外部 agent 工具**只有 ACP runner，内置 7 个且全是编码类 CLI**，关系是**集成 / 委派**而非竞品）。**把 7 个逐个归入「本地 CLI 阵营」属推断**，官方未使用该分类词。
- **显式声明**：第 1 层在本文中**只作坐标系**，本文的比较对象是**第 2、3 层**；第 1 层不展开，也不得引用 `01_explore_result.md` 候选表里未落盘的条目（例如 #16 OpenHands issue）作为证据。
- **为什么必须在这里做这一步**：「感觉都一样」的范畴错误，本质就是把第 1 / 2 / 3 层的东西放进同一张功能清单比较；先把坐标立起来，后面五章的比较才有共同刻度。

---

### 第 2 章 「多用户」一词三义 —— 三方原文并置

- **篇幅**：长，约 2,200–2,600 字（全文核心章）
- **回答什么**：三方都说「支持多用户」，但说的是三件不同的事。逐方给出限定语后的准确语义，并说明为什么这就是「功能清单叠影」的根因。
- **不回答什么**：不讲隔离的具体实现机制（留给第 3 章），不讲部署形态（留给第 4、5 章），不给选型建议。
- **素材引用**：
  - `02_deep_research.md` §6（主线 T′ 三行表与「硬结论：多用户平台 ≠ 多租户平台」）
  - §3.1 A2：`Multi-user mode lets several trusted people operate the same OpenClaw agent.` / `Every session carries up to three layers of attribution` / `usability features, not security boundaries` / `It is not an authorization or isolation boundary.` / `This is account-selection convenience inside one trust domain, not isolation`（锚点 `research/openclaw/03_docs_openclaw_ai.md`、`research/openclaw/05_docs_openclaw_ai.md`）
  - §3.2 A2：`**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` / `Allowlists answer "can this person reach the bot at all?" The **admin / user split** answers "now that they're in, what are they allowed to do?"` / `Sender routing selects a profile; it is not deny-by-default authorization.`（锚点 `research/hermes/03_..._messaging-index.md`、`research/hermes/02_..._multi-profile-gateways.md`）
  - §3.3 A2：`Agent ownership is enforced at the **row** level` / `Octop is a self-hosted AI assistant platform for households and small teams.` / `**家庭共享** — 一个管理员账号，全家共用`（锚点 `research/octop/docs/architecture.md:71`、`README.md:69`、`README_CN.md:76`）
  - §7 禁止事项（首现必须加限定语）
  - `01b_thesis_verification.md`「关键修正 3」（三方原文并置原始裁决记录）
- **示例**：**有**。核心是一张**三方原文并置对照表**（列：平台 / 限定语后的准确语义 / 关键原文 / 锚点），这是全篇最重要的一张表，第 3、5、7 章都复用它。
- **写作要点**：
  1. 三种语义各自**只用官方原话**定义，不用转述；每行必须带限定语，禁止出现裸的「多用户」。
  2. 点明这是「同词异指」而非「产品雷同」，并解释为何这必然导致功能清单叠影（大家都在同一批词上做不同的事）。
  3. 明确边界：**多用户平台 ≠ 多租户平台**；三方中只有 OpenClaw 有租户词汇且自带 experimental 标注。
  4. 必须并列记录「假阳性」：Hermes 与 Octop 各有且仅有一处 `tenant`，**都是消息路由字段**（Slack workspace / `tenant_id=agent_id`），不得读成租户模型。

---

### 第 3 章 隔离强度梯度 —— 不提供隔离 / 准入加很窄的分级 / 行级归属

- **篇幅**：长，约 2,000–2,400 字
- **回答什么**：把第 2 章的三义翻译成一条**可测量、可排序**的轴：三方的多用户隔离强度不同，且能按强度排出梯度。这是本文第一次出现可直接用于决策的量化维度。
- **不回答什么**：不讨论部署形态与运维成本（第 4、5 章），不讨论三方互相引用关系（第 6 章），不给最终选型建议。
- **素材引用**：
  - `02_deep_research.md` §6（隔离强度梯度表：三档与官方措辞）
  - §3.1 A2/A7：`usability features, not security boundaries` / `It is not an authorization or isolation boundary.` / `The normal admission limit is 32 identities per logical session.` / `not hostile multi-tenant isolation inside one shared Gateway`（锚点 `research/openclaw/03_...multi-user`、`04_...multi-tenant-hosting`）
  - §3.2 A2：`Every allowed user falls into one of two tiers per scope` / `**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.`（锚点 `research/hermes/02_..._multi-profile-gateways.md`、`03_..._messaging-index.md`）
  - §3.3 裁决 1（三层机制表：① 准入 JWT + 白名单豁免 ② 模块权限键管管理页 / 写操作 ③ `agents.user_id` 行级归属）+ 字面读法被推翻的修正（`research/octop/src/octop/api/deps.py:65-89`、`src/octop/infra/users/permissions.py:3-4`、`src/octop/api/common/agent.py:18-23,26-31,51-53`、`src/octop/api/routers/users.py:270-272`）。⚠️ `src/octop/api/middleware/jwt_auth.py` **未落盘**，不得引用其逐字句；该文件存在由 `src/octop/api/app.py:16,137` 佐证
  - §3.3 A4（归身边界延伸到运维动作：`只选当前用户自己的 agent，不包含其他用户或共享 agent`，`research/octop/docs/memory-slim.md:87`）
  - §6 硬结论（多用户平台 ≠ 多租户平台）
- **示例**：**有**。两张表：① **隔离强度梯度表**（三档 + 官方措辞 + 一句话后果）；② **Octop 三层机制表**（准入 / 权限键 / 归属各自的机制、边界与锚点）。
- **写作要点**：
  1. 三档必须**从弱到强**排列，每档给出「这意味着什么」的现实后果（例：OpenClaw 档意味着多用户是协作便利，不是安全边界）。
  2. Hermes 档必须写出「分级很窄」的实证：分档目前**只管 slash 命令**，普通对话不受限；sender 路由是选 profile，**不是** deny-by-default 授权。
  3. Octop 档必须**分层陈述**：权限键管**管理页与写 / 配置动作**，数据隔离由 `user_id` **行级归属**另负；明确写出 admin 域读端点确实要 `require_permission`，**禁止**写成「读访问无权限控制」。
  4. 补一句「隔离可由 owner 主动放宽」（专家共享 / `is_shared`），说明强隔离档也不是密不透风，并指出其治理能力（RBAC `0.9.24`、按用户配额 `0.9.33`）是**增量加入**而非初版即有。

---

### 第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」vs Hermes「It's not tied to your laptop」

- **篇幅**：中，约 1,500–1,900 字
- **回答什么**：在已被判定同层的 OpenClaw 与 Hermes 之间，有没有一根能**直接回答「什么场景用哪个」**的差异轴？答案是有：部署姿态（本机常驻 vs 不绑本机）。
- **不回答什么**：不再重复第 2、3 章的术语与隔离比较；不展开 Octop（第 5 章）；不下最终结论（第 7 章）。
- **素材引用**：
  - `02_deep_research.md` §7 第 3 条（层内差异轴）
  - §3.1 A1/A3：`OpenClaw is an open-source AI assistant that runs on your own computer` / `A single long-lived **Gateway** owns all messaging surfaces` / `One Gateway per host.` / `The Gateway binds to loopback by default.`（锚点 `research/openclaw/06_raw_githubusercontent_com.md`、`research/openclaw/01_docs_openclaw_ai.md`、`05_docs_openclaw_ai.md`）
  - §3.2 A1/A3：`Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop` / `Standalone (one gateway per profile)` / `With gateway.multiplex_profiles: true one process serves the default profile plus every live directory under profiles/` / `Seven terminal backends`（锚点 `research/hermes/01_raw_githubusercontent_com_README.md`、`research/hermes/gw/01_...md`）
  - §3.1 A4 / §3.2 A4（记忆落盘位置随部署姿态变化：OpenClaw 记忆 = 工作区里的 Markdown；Hermes 内置记忆有硬上限约 1,300 token + Honcho 建模）。**Hermes 侧的硬上限数字锚点**：`research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15,302`（官方文档页，2026-09-29 重抓，`MEMORY.md 2,200 chars (~800 tokens)` / `USER.md 1,375 chars (~500 tokens)` / `Capacity ~1,300 tokens total`）；**不得**引用 `workspace/hermes-agent/` 下的同名抓取件路径
  - §5 C8（时效：本地件 2026-08-27 与远程 2026-09-29 内容一致，无冲突；多用户结论时效为 2026-08-27）
- **示例**：**有**。一张 **OpenClaw vs Hermes 部署姿态对照表**（列：产品主语 / 在哪跑 / 常驻形态 / 记忆落盘 / 典型场景），末尾附一条「时效说明」注。
- **写作要点**：
  1. 找到那句正面分野的原文并**并置引用**：`runs on your own computer` **对** `It's not tied to your laptop`，让差异自己说话。
  2. 把「部署姿态」翻译成场景语言：本机常驻 → 与本地文件系统 / 桌面环境耦合的场景；VPS / serverless → 7×24 常驻、按需计费、多端接入的场景。
  3. 补上架构落点：OpenClaw 一主机一 Gateway 默认绑 loopback，扩展靠插件；Hermes 单进程接 20+ 平台，默认一 profile 一网关、可多路复用。
  4. 明确声明两者的**相同面**（同为常驻 gateway + 本地文件记忆 + 技能目录扩展），避免读者误以为这是「谁更好」的比较。

---

### 第 5 章 Octop 回答的是不是另一个问题 —— 单实例多用户平台，家庭与小团队

- **篇幅**：长，约 2,000–2,400 字
- **回答什么**：Octop 的「多用户」是不是第 3 章那根隔离梯度轴上的**更强档**？答案：不是。它是**另一个问句的答案**——「一台机器上的实例如何服务多个用户」，而不是「一个人的助手跑在哪台机器上」。
- **不回答什么**：不讲它与其他两方的互相引用（第 6 章），不给引入与否的建议（第 7 章）。
- **素材引用**：
  - `02_deep_research.md` §3.3 A1：`支持多用户、多 Agent 的自托管 AI 助手` / `Octop is a self-hosted AI assistant platform for households and small teams.` / `同时为每个用户配备一组可按场景切换的专业 Agent` / `**个人助理** — 让专属 Agent 帮你写周报、整理资料、定日程`（锚点 `research/octop/README_CN.md:6,70,75`、`README.md:69`、`AGENTS.md:37`）
  - §3.3 A2（邀请制 1–365 天；`role-template public id: admin | user | custom ULID`；`权限：新增按用户模块权限（RBAC）及管理员绕过` 见 `CHANGELOG.md:396`；`按用户限制存储根目录与 Token 配额` 见 `CHANGELOG.md:192`）
  - §3.3 A3（`The whole stack is one process.` / `There is no external queue (Redis, RabbitMQ, Celery), no separate worker process` / `单进程架构。重启后从控制面数据库重建状态` / `| OCTOP_DATABASE_DRIVER | sqlite | postgresql |`，锚点 `research/octop/docs/architecture.md:32`、`docs/adr/001-single-process-model.md:10,14`、`docs/adr/002-database-backends.md:44-45`、`docs/configuration.md:158`）
  - §3.3 A4（octop-memory 随工作区迁移：`{workspace}/memory.sqlite`；PG 按 `agent_<id>` schema 分片；`no automatic SQLite→PG memory data migration.`）
  - §3.3 裁决 2（**官方无任何并发量 / 吞吐 / 压测数字**，只有定性权衡）+ §8 开放问题 1
  - §5 C1（「核心未开源」已在 2026-09-24 之后不成立，主仓库含 harness 源码）
- **示例**：**有**。三份材料：① 部署形态清单（脚本安装 / PyPI / Docker / 桌面客户端 Wails / 飞牛 NAS fpk）；② **单进程模型 Trade-offs 表**（收益与代价成对：零外部依赖 ↔ 只能垂直扩展；简单部署 ↔ 重 CPU 任务阻塞事件循环）；③ Roadmap 未完成项列表。
- **写作要点**：
  1. 开篇立论：Octop 不回答「哪个助手更好」，它回答「一台机器怎么服务多个人」；官方 Scope 限定是**家庭与小团队**。
  2. 明确写出**硬边界**：单进程、无外部队列、只支持垂直扩展（一台机器）、no horizontal worker scaling —— 并且**不给出任何并发人数上限**，只给这条硬边界。
  3. 用「个人助理」被官方承认这一点，说明单用户是它的退化形态（一行 user 记录），而不是另一个产品模式；桌面端只是 Wails 外壳，无独立单用户模式。
  4. 记忆形态单独一段：octop-memory 分层 + 全文检索，落 agent 工作区，随工作区迁移；并给出 SQLite→PG 的两条迁移限制。

---

### 第 6 章 「谁把谁当参照」—— 迁移命令、对照专页、双向零提及说明什么

- **篇幅**：中长，约 1,700–2,000 字
- **回答什么**：三方的**站位**如何从「谁引用谁」显形。这是对第 2–5 章结论的**反向校验**：如果同层判断是对的，证据应该出现在它们的互相引用里。
- **不回答什么**：不做机制比较（已在第 3、4 章完成），不导新结论，只提供旁证与校验。
- **素材引用**：
  - `02_deep_research.md` §3.1 A6：`The recurring comparison is [Hermes Agent]` / `condenses the source-verified contrast with Hermes` / `Hermes is built by Nous Research, a venture-funded company` / README 全文对 `hermes`、`octop` 提及均为 0（锚点 `research/openclaw/02_docs_openclaw_ai.md`、`extra2/01`、`06_raw_githubusercontent_com.md`、`05_docs_openclaw_ai.md`）
  - §3.2 A6：`## Migrating from OpenClaw` / `If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.` / `hermes claw migrate` / 源码 `_OPENCLAW_DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot")` / 36 个具名迁移项 / `Secrets are never included implicitly`（锚点 `research/hermes/01_raw_githubusercontent_com_README.md`、`src/claw.py:1,29,33-34`、`src/openclaw_to_hermes.py:40-190`）
  - §3.3 A6：Octop 全库检索 `openclaw|hermes` **零命中**；命名的外部 agent 工具**只有 ACP runner，内置 7 个**（`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi`）（锚点 `research/octop/docs/acp.md:8,29-38`）。**不是「唯一是 `claude_code`」**
  - §4.2（Octop / Tencent 未被 awesome-list 收录）
  - §5 C1、C4（README 零提及 vs docs 站有专页，并列记录；开源冲突已裁决）
  - §6 层判断旁证（Octop 的邻近参照物是本地 CLI 阵营）
  - §7 禁止事项（15 行属性对照表必须标注**OpenClaw 单方制作**；`workspace/hermes-agent/chapters/*` 必须标为**本仓库二次加工**）
- **示例**：**有**。① **参照关系表**（行：OpenClaw / Hermes / Octop；列：是否提及对方 / 形式 / 方向 / 层级标注）；② `hermes claw migrate` 迁移内容清单（含 36 项具名迁移项摘要与「密钥默认不迁」的说明）。
- **写作要点**：
  1. 开篇给判据：同层与否不看功能，看**互相引用与互迁**；这是可证伪的硬证据。
  2. OpenClaw 侧：有官方 15 行属性对照专页，但 README 全文零提及 —— 门面与文档深度不一致，**并列记录不合并**；引用对照表时**必须标注「OpenClaw 单方制作」**，不是中立评测。
  3. Hermes 侧：迁移命令是双向同层的铁证（README 与源码三处交叉一致）；点出密钥默认不迁这一安全姿态；引用本仓库既有章节时必须标为「本仓库二次加工」。
  4. Octop 侧：双向零提及，且它命名的外部 agent 工具只有 ACP runner（内置 7 个，全是编码类 CLI）—— 回指第 1 章的三层坐标：它的邻近参照物落在**第 1 层**。**注意**：把这 7 个逐个归入「本地 CLI 阵营」属**推断**（官方未使用该分类词），写作时必须标注为推断，不得当成官方口径。

---

### 第 7 章 选型框架 + 落到你场景的决策树（个人助手 / 企业多人）

- **篇幅**：长，约 2,100–2,500 字
- **回答什么**：把前六章的结论收敛成一个**可复用、可迁移**的选型框架，并针对读者的两类真实场景（个人助手 / 企业多人）给出可执行的决策路径。新出现的 agent 也能用这套框架自行归位。
- **不回答什么**：不引入前六章未论证过的新事实；不推荐具体部署方案；不给出 Octop 的容量承诺；不展开第 1 层（本地 CLI 阵营）。
- **素材引用**：
  - `02_deep_research.md` §7 四条轴（术语轴 / 隔离强度轴 / 层内差异轴 / 框架轴）
  - §6 层判断（OpenClaw 与 Hermes 同层；Octop 同层不同重心）
  - §4.1 选型透镜（用**压力剖面**而非功能清单提问）
  - §4.2 五类用途定位（新 agent 归位时的第一跳）
  - §3.3 裁决 2 + §8 开放问题 1（Octop 只给硬边界，不给人数上限）
  - `00_intent.md`「用户实际使用场景」表（Hermes = 个人助手 + 部分企业工作；OpenClaw = 与 Hermes 用途重叠、先试的那一个；Octop = 尚未使用的新选项）
- **示例**：**有**。① **决策树**（根节点沿用第 1 章三层坐标：第 1 层 → 层内不展开，直接指向层内选型方法；第 2、3 层 → 分支：部署姿态 / 隔离强度 / 是否多租户 → 叶子：具体平台 + 硬边界）；② **选型框架表**（四轴 + 每轴的提问 + 三平台站位）；③ **用户场景映射表**（读者两类场景 → 该走哪条分支 → 现用工具是否需要变）。
- **写作要点**：
  1. 决策树必须是**前六章的收口**：第一层分支直接复用第 1 章的三层坐标（先归位到层，再谈层内），此后每一层分支都要回指前面的章（术语轴回第 2 章、隔离强度回第 3 章、部署姿态回第 4 章、Octop 归位回第 5 章、互相引用校验回第 6 章），不能凭空出现。
  2. 第一层分支就是第 1、2 章结论的直接应用：先问「你要的是哪一层——本地 CLI / 个人助手 harness / 多用户平台」；若答案是第 1 层，本文不展开（只指向层内选型方法），若是第 2、3 层则进入后续分支。
  3. 落到用户场景：个人助手 + 部分企业工作 → 在 OpenClaw / Hermes 之间按部署姿态分（第 4 章轴）；企业多人 → 再问「同一信任域内的协作还是需要跨租户隔离」，并明确 OpenClaw 档的协作 guardrails 不构成安全边界、Octop 档的规模限定是家庭与小团队、无人数上限数据。
  4. 结尾给一份**可迁移的提问清单**（三层坐标 + 四轴 + 压力剖面），让读者面对下一个新 agent 时能自行归位，并列出本文的开放问题（Octop 容量、多用户治理的版本边界、归属表清单）作为后续观察点。

---

## 学习路径说明

### 前置要求

- 已实际使用过至少一个自托管 agent（OpenClaw 或 Hermes 类），具备「agent + 工具 + 记忆 + 通道」的基本语感
- 能读懂 Docker / 配置文件 / 目录结构级别的描述（本笔记停在「上手」深度，不要求读源码）
- 不需要预先了解 Octop，也不需要搭建任何环境（本篇不实际部署）

### 学完能做什么

- 用「是否常驻服务 × 用户数是单数还是复数」这套判据，把一个新的 agent 先**归位到层**（本地 CLI / 个人助手 harness / 多用户平台），再谈层内选择
- 用「同词异指」这一根轴，解释清楚为什么拿功能清单比较自托管 agent 必然撞车
- 准确区分三方对「多用户」的三种不同语义，并在任何场合加限定语使用这个词
- 用隔离强度梯度（不提供隔离 / 准入 + 很窄分级 / 行级归属）给任一自托管 agent 定档
- 在同一层内（OpenClaw / Hermes）按部署姿态做出可辩护的选择
- 判断一个新出现的 agent 是否与手上工具构成直接竞品
- 针对「个人助手」与「企业多人」两类场景，走通决策树得到一个可解释的结论

### 建议学习顺序

1. **第 1 章**（约 20 分钟）—— 先建立三层坐标，再接受「比较方法需要换」这个前提；否则后面会一直想回到功能清单
2. **第 2 章**（约 25 分钟，全文最重要）—— 三义切分是后面所有论证的地基，建议对照原文并置表逐行读
3. **第 3 章**（约 20 分钟）—— 把三义转成可排序的梯度，这是第一次能量出来的维度
4. **第 4 章**（约 15 分钟）—— 同层内部的第一根实用差异轴，读完即可用于 OpenClaw / Hermes 二选一
5. **第 5 章**（约 20 分钟）—— 理解 Octop 是另一个问句的答案，把它移出二选一
6. **第 6 章**（约 15 分钟）—— 用作反向校验：如果前面的判断对，证据应该长这样
7. **第 7 章**（约 20 分钟）—— 收口章，先走决策树再回读四轴框架；建议结合自己手上工具的实际用法对号入座
