# -*- coding: utf-8 -*-
"""步骤 3 的数据：正文英译中对照表 + 周边散句修正。

三条纪律：

1. **键是逐字原文**（反引号 span 内的完整文本，不含定界符）。`04_apply.py`
   会断言每个键都能在笔记里命中 >= 1 次；命中 0 次即报错退出，绝不静默跳过。
2. 值必须是**单行**、不含 `|`（会写进 Markdown 表格）、**不含反引号**。
   反引号这条不是洁癖：原 span 大多只用 1 个反引号定界，而 1 个反引号的
   span 里**不能**再出现反引号——Markdown 会把它当成新的定界符，
   在那里提前闭合（`With gateway.multiplex_profiles: true …` 与
   `**During first-time setup:** …` 两条就是这么被撕开的）。字段名、
   配置键在中文里裸写即可，精确形态由每章末尾的「引文对照」表承担。
3. 只翻「成句的英文散文」。代码、命令、配置键、路径、文件名、产品名、单个
   技术术语（`Gateway` / `fleet` / `guardrails` / `README` …）一律保留原文。

`FIXES` 是 span 替换**之后**做的字面替换，用来修「英文表格单元格」「英文的
术语清单」和「中文引导语已经把引文意思说了一遍」造成的重复。
`VERBATIM_FIX` 是引文逐字订正：正文里那两句是**在源文件换行处被截断的半句**
（结尾悬挂 `no` / 无终止标点），附录「原文（逐字）」列按源文件全句给出。
"""

# ---------------------------------------------------------------- 正文英译中
TRANS = {
    # 第 1 章
    "A single long-lived **Gateway** owns all messaging surfaces":
        "一个长期存活的 **Gateway** 掌管全部消息面",
    "The messaging gateway is the long-running process that connects Hermes to 20+ external messaging platforms through a unified architecture.":
        "消息网关是一个常驻进程，通过统一的架构把 Hermes 接到 20 多个外部消息平台上",
    "Everything runs in a single Python process served by uvicorn.":
        "一切都跑在一个由 uvicorn 提供服务的 Python 进程里",
    "Octop is a self-hosted AI assistant platform for households and small teams.":
        "Octop 是一个面向家庭与小团队的自托管 AI 助手平台",
    "Default OpenClaw is a trusted single-operator assistant.":
        "默认的 OpenClaw 是一个受信的单操作者助手",
    "## What we do not claim":
        "「我们不做哪些声明」",
    "It is not an authorization or isolation boundary.":
        "「它不构成授权或隔离边界」",
    "**By default, the gateway denies all users who are not in an allowlist or paired via DM.**":
        "默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户",
    "with its own bot tokens, sessions, and memory":
        "各有自己的 bot token、会话与记忆",
    "We analyze the limits of model-centric scaling for long-horizon task completion and argue that agent performance is a property of the model–harness pairing.":
        "我们分析了以模型为中心的扩展在长程任务完成上的局限，并论证 agent 的表现是「模型–harness 配对」的属性",
    "transforms raw environment signals into model-usable observations, including terminal output, file diffs, screenshots, DOM states, API responses, logs, retrieved passages, and event streams.":
        "把原始环境信号转成模型可用的观察，包括终端输出、文件差异、截图、DOM 状态、API 响应、日志、检索到的段落与事件流",
    "determines what information enters the model context, when it enters, and in what form, covering prompt construction, system instructions, retrieval, memory selection, compression, summarization, tool descriptions, and current task state.":
        "决定哪些信息进入模型上下文、何时进入、以什么形式进入，涵盖提示词构造、系统指令、检索、记忆选取、压缩、摘要、工具描述与当前任务状态",
    "orchestrates the observe-reason-act-feedback cycle, including step scheduling, stopping criteria, retries, reflection, delegation, handoffs, and multi-agent coordination.":
        "编排「观察–推理–行动–反馈」循环，包括步骤调度、停止条件、重试、反思、委派、交接与多 agent 协同",
    "maps model outputs to executable operations, such as function calls, MCP tools, shell or code execution, browser actions, file operations, API calls, and sub-agent invocations.":
        "把模型输出映射为可执行操作，例如函数调用、MCP 工具、shell 或代码执行、浏览器动作、文件操作、API 调用与子 agent 调用",
    "persists execution state and products, including conversation history, plans, scratchpads, checkpoints, logs, traces, diffs, memory records, generated files, and task artifacts.":
        "持久化执行状态与产物，包括对话历史、计划、草稿本、检查点、日志、追踪、差异、记忆记录、生成的文件与任务工件",
    "checks, constrains, and repairs execution through tests, assertions, verifier models, sandbox policies, permission gates, rollback, retry, budget control, safety constraints, and audit traces.":
        "通过测试、断言、验证器模型、沙箱策略、权限闸、回滚、重试、预算控制、安全约束与审计追踪来检查、约束和修复执行",
    "observation, context, control, action, state, and verification":
        "「观察、上下文、控制、行动、状态与验证」",
    "a task is not merely an application label but a pressure profile over observation, context, control, action, state, and governance":
        "任务不只是一个应用标签，而是施加在观察、上下文、控制、行动、状态与治理之上的一个压力剖面",
    "Although the six components are analytically separable, they do not operate independently. Design choices in one component often reshape the burden on others.":
        "尽管这六个组件在分析上可以分开，它们并不独立运作：一个组件上的设计选择常常会重新分配其他组件上的负担",
    "AI coworkers and teammates, agent builders and frameworks, workflow automation platforms, browser agents, and coding agents":
        "AI 同事与队友、agent 构建工具与框架、工作流自动化平台、浏览器 agent 与编码 agent",
    "Each project appears once, under the category that best matches its main use.":
        "每个项目只出现一次，归在与其主要用途最匹配的那一类下",
    "AI coworkers and teammates":
        "「AI 同事与队友」",
    "Agents specialized in writing, editing, and shipping code.":
        "「专门写代码、改代码、发布代码的 agent」",
    "Inclusion is not an endorsement, and star counts, funding, and company size are not criteria.":
        "入选不等于推荐，星标数、融资额与公司规模都不是入选标准",
    "Octop agent delegates coding tasks":
        "「Octop agent 委派编码任务」",
    "The recurring comparison is [Hermes Agent]":
        "反复被拿来对照的对象是 Hermes Agent（原文此处带一个指向对方仓库的链接）",

    # 第 2 章
    "Multi-user mode lets several trusted people operate the same OpenClaw agent.":
        "多用户模式让多个受信的人操作同一个 OpenClaw agent",
    "usability features, not security boundaries":
        "「易用性功能，不是安全边界」",
    "Allowlists answer \"can this person reach the bot at all?\" The **admin / user split** answers \"now that they're in, what are they allowed to do?\"":
        "白名单回答「这个人能不能够到这个 bot」，而 **admin / user 分级**回答「进来之后允许他做什么」",
    "Every request is authenticated via JWT and resolved to a `User` row.":
        "每个请求都先过 JWT 认证，再落到一行 User 记录",
    "Agent ownership is enforced at the **row** level":
        "agent 归属在**行级**强制执行",
    "Every session carries up to three layers of attribution:":
        "每个会话最多携带三层归属信息：",
    "the first time a teammate DMs the bot they get a pairing code":
        "队友第一次私聊这个 bot 时会拿到一个配对码",
    "Named operator roles bind authenticated profiles to a policy":
        "命名操作者角色把已认证的 profile 绑定到一套策略上",
    "This is account-selection convenience inside one trust domain, not isolation from administrators or code running as the Gateway OS user.":
        "这只是一个信任域内部挑选账号的便利，而不是与管理员、或与以 Gateway 系统用户身份运行的代码隔离",
    "A single-user gateway therefore looks unchanged.":
        "因此单用户网关看起来几乎没有变化",
    "A gateway is one trust domain.":
        "一个 Gateway 就是一个信任域",
    "The normal admission limit is 32 identities per logical session.":
        "「每个逻辑会话的默认准入上限是 32 个身份」",
    "**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.":
        "目前分级管的是什么：斜杠命令。……普通对话不受影响——非管理员仍然可以和 agent 说话",
    "A personal assistant on one Telegram bot and a coding agent on another":
        "一个 Telegram bot 上跑私人助手、另一个上跑编码 agent",
    "Tenancy means one gateway cell per tenant, and fleet is still experimental.":
        "租户意味着一个租户一个 gateway cell，而 fleet 目前仍是实验性的",
    "OpenClaw's default security model is one trusted operator boundary per Gateway, not hostile multi-tenant isolation inside one shared Gateway.":
        "OpenClaw 的默认安全模型是「每个 Gateway 一个受信操作者边界」，而不是在共享的同一个 Gateway 内部做敌意多租户隔离",
    "There is no enterprise edition.":
        "没有企业版",
    "not hostile multi-tenant isolation inside one shared Gateway":
        "「不是在同一个共享 Gateway 内部做敌意多租户隔离」",
    "Sender ids are also namespaced per tenant on some platforms — a Slack user id is workspace-local":
        "在某些平台上，发送者 ID 也按租户加了命名空间——Slack 的用户 ID 是工作区局部的",
    "Sender routing selects a profile; it is not deny-by-default authorization.":
        "发送者路由只是在挑 profile，不是默认拒绝式的授权",
    "Every allowed user falls into one of two tiers per scope (DM vs group/channel):":
        "每个被放行的用户在每个作用域里（私聊 vs 群组 / 频道）都落在两档之一：",

    # 第 3 章
    "The admin / user split":
        "**admin / user 分级**",
    "What the tiers gate today: slash commands":
        "目前分级管的是什么：斜杠命令",
    "Read access and agent use in chat are never gated.":
        "读取权限与在对话中使用 agent 从不受分级限制",

    # 第 4 章
    "OpenClaw is an open-source AI assistant that runs on your own computer":
        "OpenClaw 是一个跑在你自己电脑上的开源 AI 助手",
    "Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop":
        "把它跑在一台 5 美元的 VPS、一个 GPU 集群，或者空闲时几乎不花钱的 serverless 基础设施上——它不绑在你的笔记本上",
    "runs on your own computer":
        "「跑在你自己的电脑上」",
    "It's not tied to your laptop":
        "「不绑在你的笔记本上」",
    "One Gateway per host.":
        "一台主机一个 Gateway",
    "The Gateway binds to loopback by default.":
        "Gateway 默认绑定到 loopback",
    "as a personal assistant on a laptop":
        "「作为笔记本上的私人助手」",
    "not tied to your laptop":
        "「不绑在你的笔记本上」",
    "talk to it from Telegram while it works on a cloud VM":
        "它在云上的 VM 里干活时，你可以从 Telegram 跟它说话",
    "With gateway.multiplex_profiles: true one process serves the default profile plus every live directory under profiles/":
        "把 gateway.multiplex_profiles: true 打开后，一个进程就同时服务默认 profile 和 profiles/ 下每一个活跃目录",
    "The model only remembers what gets saved to disk; there is no hidden state.":
        "模型只记得被写进磁盘的东西，没有隐藏状态",

    # 第 5 章
    "The whole stack is one process. There is no separate worker, no":
        "整个技术栈就是一个进程：没有单独的 worker、没有外部队列，除了用户自己配置的 LLM 供应商之外不依赖任何外部服务",
    "Everything runs in a single Python process served by uvicorn. There is no external queue (Redis, RabbitMQ, Celery), no separate worker process":
        "一切都跑在一个由 uvicorn 提供服务的 Python 进程里：没有外部队列（Redis、RabbitMQ、Celery），没有单独的 worker 进程，除了 LLM 供应商之外不需要任何后端服务",
    "**Octop** — self-hosted AI assistant platform (multi-user, multi-agent).":
        "**Octop**：自托管 AI 助手平台（多用户、多 agent）",
    "Manage the Octop system service (systemd on Linux, launchd on macOS).":
        "把 Octop 作为系统服务来管理（Linux 上用 systemd，macOS 上用 launchd）",
    "Octop needs to run a web server, a CLI, per-user Agent runtimes, IM channel connections, and cron schedulers simultaneously.":
        "Octop 需要同时跑 web 服务、CLI、每个用户的 Agent 运行时、IM 通道连接和定时调度",
    "Adding Redis or a process supervisor doubles the ops burden for the primary audience.":
        "对目标人群来说，加一个 Redis 或进程守护会成倍增加运维负担",
    "- Greenfield only — no SQLite→PG data migrator.":
        "「只支持全新安装——没有 SQLite→PG 的数据迁移工具」",
    "Future scale-out would require extracting the worker into a separate process and adding a queue":
        "将来要横向扩展，得把 worker 拆成独立进程并加一个队列",
    "No horizontal worker scaling":
        "「不支持 worker 的横向扩展」",
    "Vertical scaling only":
        "「只支持垂直扩展」",
    "one writer per agent at a time":
        "「同一时刻每个 agent 只有一个写入者」",
    "- Single active Octop writer; no multi-instance write promise.":
        "「同一时刻只有一个 Octop 写入者；不承诺多实例写入」",
    "Control plane PostgreSQL → agent memory **defaults to the same DSN**":
        "控制面用 PostgreSQL 时，agent 记忆**默认复用同一个 DSN**",
    "- Control plane SQLite → agent memory stays {workspace}/memory.sqlite":
        "控制面用 SQLite 时，agent 记忆留在 {workspace}/memory.sqlite",
    "no automatic SQLite→PG memory data migration.":
        "「没有 SQLite→PG 的记忆数据自动迁移」",
    "Agent memory DDL is owned by octop-memory.":
        "「记忆表的 DDL 由 octop-memory 自己拥有」",

    # 第 6 章
    "The [comparison table](...) condenses the source-verified contrast with Hermes.":
        "那张逐项对照专页压缩了与 Hermes 的、经来源逐条核实的差异（原文此处带一个指向该专页的链接）",
    "Use one cell for each tenant trust boundary; do not use one shared Gateway as a hostile multi-tenant boundary.":
        "每个租户信任边界用一个 cell；不要把共享的一个 Gateway 当作敌意多租户边界",
    "The Fleet operator and the host are trusted by every tenant. Resistance to a compromised host is a non-goal.":
        "Fleet 操作者与主机被所有租户所信任；抵抗被攻破的主机不是目标",
    "No rung in this ladder changes the OpenClaw application trust model: one Gateway remains one trusted operator domain.":
        "这条阶梯上的任何一级都不改变 OpenClaw 的应用信任模型：一个 Gateway 始终是一个受信操作者域",
    "The comparison below reflects source at 6defe7eb6c (reviewed August 27, 2026), not a live adversarial test or a guarantee about every deployment.":
        "下面这张对照表反映的是 6defe7eb6c 这个提交（复核于 2026 年 8 月 27 日）时的来源，它既不是实时的对抗性测试，也不构成对每一次部署的保证",
    "Governance":
        "治理",
    "Funding and revenue":
        "资金与营收",
    "Independent 501(c)(3) funded by donations":
        "独立 501(c)(3)，靠捐赠资助",
    "Venture-funded (Paradigm-led Series A)":
        "风险投资（Paradigm 领投的 A 轮）",
    "Hermes is built by Nous Research, a venture-funded company":
        "Hermes 由 Nous Research 打造，一家接受风险投资的公司",
    "Roles and multi-user":
        "「角色与多用户」",
    "Equal trust within an adapter's authorized set":
        "「在某个适配器的授权集合内是同等信任」",
    "experimental per-tenant fleet cells":
        "「实验性的每租户 fleet cell」",
    "## Migrating from OpenClaw":
        "从 OpenClaw 迁移",
    "If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.":
        "如果你是从 OpenClaw 过来的，Hermes 可以自动导入你的设置、记忆、技能和 API 密钥",
    "**During first-time setup:** The setup wizard (hermes setup) automatically detects ~/.openclaw and offers to migrate before configuration begins.":
        "**首次安装时：**安装向导（hermes setup）会自动检测 ~/.openclaw，并在配置开始前询问是否迁移",
    "Memories":
        "记忆",
    "Skills":
        "技能",
    "Command allowlist":
        "命令白名单",
    "Messaging settings":
        "消息设置",
    "API keys":
        "API 密钥",
    "TTS assets":
        "TTS 素材",
    "Workspace instructions":
        "工作区指令",
    "Secrets are never included implicitly: --migrate-secrets is required even under --preset full":
        "密钥默认不迁：即使加了 --preset full，也必须显式给出 --migrate-secrets",

    # 第 4 章（记忆上限的计量单位）
    "2,200 chars (~800 tokens)":
        "2,200 字符（约 800 token）",
    "1,375 chars (~500 tokens)":
        "1,375 字符（约 500 token）",
    "~1,300 tokens":
        "约 1,300 token",

    # 第 7 章（`coding agents` 在正文里是带反引号的，属 span）
    "coding agents":
        "编码 agent",
}

# 正文里被截断的半句引文：附录「原文（逐字）」列给出源文件全句。
VERBATIM_FIX = {
    "The whole stack is one process. There is no separate worker, no":
        "The whole stack is one process. There is no separate worker, no external queue, "
        "no required external services beyond whatever LLM provider the user configures.",
    "Everything runs in a single Python process served by uvicorn. "
    "There is no external queue (Redis, RabbitMQ, Celery), no separate worker process":
        "Everything runs in a single Python process served by uvicorn. There is no external queue "
        "(Redis, RabbitMQ, Celery), no separate worker process, and no required backing services "
        "beyond the LLM provider.",
}

# span 替换之后做的字面替换，**自上而下顺序敏感**：(旧, 新, 期望命中次数)。
# 旧串必须取「**本行之前所有条目都跑完**之后」的形态，不是成品最终形态：本轮
# 就踩过——按成品抄 `…每个用户的 agent runtime…`，可上面第 300 行已经把
# `agent runtime` 改成 `agent 运行时` 了，于是 got=0。对不上就报错，不静默跳过。
# 期望次数是**跨全部目标文件的总数**：每篇笔记有 4 份副本（分章文件、_merged、
# final_note、vault 笔记），所以「每份出现一次」= 4。0 表示只替换、不校验。
# 任何一条对不上，脚本报错退出——不静默跳过。
FIXES = [
    # —— 英文表格单元格 / 英文清单 ——
    ("| Zero external dependencies | Vertical scaling only (one machine) |",
     "| 零外部依赖 | 只支持垂直扩展（一台机器） |", 4),
    ("| Simple deployment (one process, one port) | Heavy CPU tasks block the event loop |",
     "| 部署简单（一个进程、一个端口） | 重 CPU 任务会阻塞事件循环 |", 4),
    ("| Fast local dev | No horizontal worker scaling |",
     "| 本地开发快 | 不支持 worker 的横向扩展 |", 4),
    ("session ownership、participant history、live presence、owner filtering",
     "会话归属、参与者历史、实时在场、按所有者过滤", 4),
    ("MCP servers / Cron / Hooks / Gateway / Session / Approval rules",
     "MCP 服务器 / 定时任务 / 钩子 / Gateway / 会话 / 审批规则", 4),
    # 六职责名（表格里是纯文本，不是 span）
    ("| ① | Observation interface |", "| ① | 观察接口 |", 4),
    ("| ② | Context manager |", "| ② | 上下文管理 |", 4),
    ("| ③ | Control loop |", "| ③ | 控制循环 |", 4),
    ("| ④ | Action interface |", "| ④ | 行动接口 |", 4),
    ("| ⑤ | State and artifact store |", "| ⑤ | 状态与工件存储 |", 4),
    ("| ⑥ | Verification and governance layer |", "| ⑥ | 验证与治理层 |", 4),
    ("`verification/governance`", "`验证/治理`", 4),
    # 代码清单里的英文旁注
    ("（List installed plugins）", "（列出已安装插件）", 4),
    ("（list users）", "（列出用户）", 4),
    ("（list role templates）", "（列出角色模板）", 4),
    # —— 夹在中文里的英文短语（产品名、路径名保留） ——
    ("README 零提及 vs docs 有专页", "README 零提及、docs 有专页", 4),
    ("（例如 #16 OpenHands issue）", "（例如 #16 这条 OpenHands issue）", 4),
    ("（Slack workspace）", "（Slack 工作区）", 4),
    ("把 agent id 复用为消息路由的 tenant id",
     "把 agent ID 复用为消息路由的租户 ID", 4),
    ("Hermes 的默认准入是 deny-by-default，", "Hermes 的默认准入策略是「默认拒绝」，", 4),
    ("plain chat", "普通对话", 4),
    ("每个用户的 agent runtime", "每个用户的 agent 运行时", 4),
    # —— 中文引导语已经说过一遍引文意思：删掉重复引导 ——
    ("两句自我限定。第一句是它属于易用性功能：", "两句自我限定。第一句：", 4),
    ("因此单用户网关看起来几乎没变：", "", 4),
    ("其一，整个 Gateway 就是一个信任域：", "其一，", 4),
    ("其二，参与者集合有默认上界：", "其二，", 4),
    ("每个请求先过 JWT，再落到一行用户记录：", "", 4),
    ("，并且明确无企业版：", "。", 4),
    ("，不是隔离边界。", "。", 4),
    # —— 兜底：上面那条「是 deny-by-default，」先命中，剩下单独出现的 ——
    ("deny-by-default", "默认拒绝", 0),
    # —— `slash` 放最后：上面的引导语编辑要按原文写法先命中 ——
    ("- 两档目前只管 slash 命令：", "- 目前分级只管斜杠命令：", 4),
    ("slash 命令", "斜杠命令", 0),   # 0 = 只替换、不校验次数
    # —— 译完之后引导语与中译撞车：把引导语缩成标签（实测只有这 3 处） ——
    # 判据：引导语以 `：` 收尾、紧跟一条反引号引文，且两者中译的 2-gram
    # 重叠 >= 6。见 _v3.txt。
    ("因为一个实例要同时扛 web 服务、CLI、每个用户的 agent 运行时、IM 通道连接和定时调度：",
     "因为一个实例要同时扛多项职责：", 4),
    ("换到 PostgreSQL 时，记忆默认复用同一个 DSN、按 agent 分 schema：", "记忆落点：", 4),
    # 这条引文自身就以「首次安装时：」起头，引导语再写一遍「安装向导」就是重复；
    # 直接让引文当条目，不再另起标签。
    ("- 首次安装向导会自动检测：", "- ", 4),
    # —— 英文词被译成中文之后，原来托着它的空格成了「中文 空格 中文」 ——
    # 只针对本轮译出来的词；「第 1 层 本地 CLI 阵营」那种刻意的标签空格不动，
    # 06_verify.py 会断言成品里不再有其它「中文 空格 中文」。
    (" 斜杠命令", "斜杠命令", 0),
    ("默认拒绝 的准入", "默认拒绝的准入", 0),
    ("普通对话 不受影响", "普通对话不受影响", 0),
    # —— 同一类，第二批：引导语或括注把引文的意思用中文又说了一遍 ——
    # 这一批由 _lcs.py 挑出（判据：引导语尾部与引文中译的**最长公共汉字子串**
    # >= 5），再逐条人工判过。上一批用的 2-gram 占比会漏掉长引文——
    # `密钥默认不迁：` 后面跟一条长引文，重复明明在，占比却被稀释到阈值以下。
    # 不算缺陷、故意不动的两类：① 表格「准确语义」列 vs 「关键原文（逐字）」
    # 列，概述与它引的原句本来就会重字；② 「术语 + 逐字出处」这种（如 545 行
    # 的「受信的单操作者助手」），引导语在立术语、括注在给出处。
    # 两种改法：把引导语缩成语题标签，或把括注里那截中译删掉、只留出处。
    ("官方有一张专页，逐轴对照的对象是 Hermes——", "官方有一张专页做逐轴对照：", 4),
    ("这里要点出与前两方的结构性差别：官方给的规模口径是家庭与小团队——",
     "这里要点出与前两方的结构性差别——官方规模口径：", 4),
    ("（`默认的 OpenClaw 是一个受信的单操作者助手`，", "（", 4),
    ("（`记忆表的 DDL 由 octop-memory 自己拥有`，", "（", 4),
    ("安全姿态也值得记一笔——密钥默认不迁：", "安全姿态也值得记一笔：", 4),
]

# 第 4 章标题里的英文句子（标题、目录、以及 03_outline 的章节标题共 5 处）。
# 计数按文件分别断言，见 rework_core.TITLE_EXPECT。
TITLE_FIX = ("第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」vs Hermes「It's not tied to your laptop」",
             "第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」对比 Hermes「不绑在你的笔记本上」")
