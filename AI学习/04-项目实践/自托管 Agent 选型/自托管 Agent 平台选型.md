---
tags: [ai-agent, 选型, 自托管, openclaw, hermes, octop, 对比]
created: 2026-09-29
updated: 2026-09-29
---

# 自托管 AI Agent 平台选型（Octop / OpenClaw / Hermes）

> [!info] 概述
> **一句话定义**：三个自托管 agent（Octop / OpenClaw / Hermes）「感觉都一样」不是产品同质，而是**术语同质**——同一批词（「多用户」「多租户」「隔离」）在三方原文里指的并不是同一件事。本篇先立分层坐标，再把「多用户」拆成三义、排成一条隔离强度梯度，最后收敛成选型决策树。
>
> **🎯 比喻**：这就像三个人都说自己「会游泳」——一个在泳池里游 25 米，一个在岸边浮潜，一个能横渡海峡。都写「会游泳」没有错，但把这三行放进同一张表比较「游泳能力」，那个「都有」毫无意义。你得先问清是哪种水、游多远。

## 目录

1. 第 1 章 为什么「感觉都一样」是范畴错误 —— 从功能清单叠影说起
2. 第 2 章 「多用户」一词三义 —— 三方原文并置
3. 第 3 章 隔离强度梯度 —— 不提供隔离 / 准入与很窄的分级 / 行级归属
4. 第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」对比 Hermes「不绑在你的笔记本上」
5. 第 5 章 Octop 回答的是不是另一个问题 —— 单实例多用户平台，家庭与小团队
6. 第 6 章 「谁把谁当参照」—— 迁移命令、官方对照页、双向零提及说明什么
7. 第 7 章 选型框架 + 落到你场景的决策树（个人助手 / 企业多人）

> [!note] 关于引文
> 正文里凡是**成句的英文**都给了中译；**代码、命令、配置键、路径、文件名、产品名与单个技术术语**保留原文。每处引文的**逐字原文**见该章末尾的「引文对照」表。
>
## 第 1 章 为什么「感觉都一样」是范畴错误 —— 从功能清单叠影说起

### 本章要解决的问题

本章先把三个自托管 agent 放回一个可比较的坐标里：按「是否常驻服务 × 服务的用户数是单数还是复数」，把 agent 分成「本地 CLI 阵营 / 个人助手 harness / 多用户平台」三层；再解释为什么「OpenClaw 和 Hermes 看起来干的是同一件事」不是产品缺陷，而是**比较方法本身失效**——把不同层的东西塞进同一张功能清单对读，是一次范畴错误。本章不给任何选型结论，也不评判三方优劣，更不展开第 1 层。

### 1.1 先立坐标：一根轴上的两个问题

在比较三个东西之前，得先确认它们能被放在同一把尺子上。本章用的尺子只有两个问题，而且是**同一根轴上的两问**，不是三条并列的分类标准：

- 判据①：**它是不是常驻服务？** 是「用完即退的进程」，还是「一直挂着的服务进程」。
- 判据②：**它服务的用户数是单数还是复数？** 单数指一个所有者；复数指一台机器同时服务多个账号。

两问交叉，得到三层：

| 层                            | 判据① 是否常驻服务           | 判据② 用户数单复数 | 代表                        | 本文处理方式        |
| ---------------------------- | -------------------- | ---------- | ------------------------- | ------------- |
| 第 1 层 本地 CLI 阵营              | 否——进程内启动、用完即退        | 单数         | Claude Code / Codex CLI 等 | **只作坐标系，不展开** |
| 第 2 层 个人助手 harness           | 是——常驻 gateway / 长驻进程 | 单数         | OpenClaw、Hermes           | 本文比较对象        |
| 第 3 层 多用户平台（此处「多用户」= ③ 行级归属） | 是——常驻服务，单实例承载多个账号    | 复数         | Octop                     | 本文比较对象        |

这三行不是三个并列的类别，而是同一根轴上的三段：从左到右，「常驻」和「复数」两个条件逐个亮起。

**判据怎么落到具体产物上？** 两问分开读原文。先要说清判据② 数的是什么：数的是**所有者 / 信任域的个数**，不是「能有几个人接触到这台实例」。

先看判据①（是不是常驻服务）：

- **OpenClaw**：`一个长期存活的 **Gateway** 掌管全部消息面`（`research/openclaw/01_docs_openclaw_ai.md:11`）。
- **Hermes**：`消息网关是一个常驻进程，通过统一的架构把 Hermes 接到 20 多个外部消息平台上`（`research/hermes/gw/01_hermes-agent_nousresearch_com.md:9`）。
- **Octop**：`一切都跑在一个由 uvicorn 提供服务的 Python 进程里`（`research/octop/docs/adr/001-single-process-model.md:14`），且启停交由系统服务托管——`把 Octop 作为系统服务来管理（Linux 上用 systemd，macOS 上用 launchd）`（`research/octop/docs/cli.md:120`）。

三家都是「一直挂着的服务进程」，没有一家是「用完即退」的，所以**三家都不在第 1 层**。

再看判据②：

- **Octop = 复数**：`Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）——一台实例、一个共用的控制面数据库，服务多个账号，每个账号在数据上归属自己。
- **OpenClaw = 单数**：`默认的 OpenClaw 是一个受信的单操作者助手`（`research/openclaw/02_docs_openclaw_ai.md:64`，出自官方 `我们不做哪些声明` 一节，是官方的自我限定而非本文推断）。它确实有「多用户」（① 同一信任域内的协作），但官方明说那属于易用性功能：`它不构成授权或隔离边界`（`research/openclaw/03_docs_openclaw_ai.md:118`）——所有者仍是单数。
- **Hermes = 单数**：`默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户`（`research/hermes/03_raw_githubusercontent_com_messaging-index.md:327`）——默认全拒，放行的也只是同一个所有者认可、且同处一个信任域的人（「多用户」= ② 准入与很窄的分级）。要给不同的人各自的 agent，官方的做法是多开 profile / 多开实例（每个 profile `各有自己的 bot token、会话与记忆`，`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:9`），**不是在一台实例里装多个账号**。

判据① 三家取值一致、判据② 一分为二：第 1 层由判据① 分出去（那里是「否」），第 2 层与第 3 层由判据② 分开（单数所有者 vs 复数账号）。三层至此分完。

> [!warning] 关于「多用户」这个词
> 本文任何位置都不裸用「多用户」。它至少有三层互不相同的限定语义，本文固定表述为：① 同一信任域内的协作；② 准入与很窄的分级；③ 行级归属。第 3 层的层名「多用户平台」，用的是 ③ 行级归属这一层语义。三种语义的逐方切分是第 2 章的主题，本章不展开。
> 另钉一条硬结论供后文复用：「多用户平台」**不等于**「多租户平台」，二者不是同一件事（第 2、3 章给出原文依据）。

> [!tip] 大白话
> 把判据想成给「助手」分宿舍：判据①问「他是住宿舍的（常驻），还是来一趟就走的（用完即退）」；判据②问「这间宿舍住一个人，还是住一屋人」。同样挂着「宿舍」的名，住的是一人还是一屋，是完全不同的两件事。

### 1.2 「看起来一样」是怎么发生的：功能清单叠影

为什么两个东西会「看起来一样」？因为**列功能清单这件事本身，会系统性地把差异抹掉**。大家都用同一批词做功能名（如「多用户」「记忆」「扩展」「常驻」），而同一行标签底下填进去的内容根本不是一件事：

| 清单行（大家都会写） | OpenClaw 这一行实际指向 | Hermes 这一行实际指向 | Octop 这一行实际指向 |
| --- | --- | --- | --- |
| 「多用户」 | 同一信任域内的协作 | 准入与很窄的分级 | 行级归属 |
| 「有记忆」 | 工作区里的 Markdown 文件 | 内置记忆（有硬上限）+ Honcho 建模 | 独立记忆库，随工作区迁移 |
| 「可扩展」 | 进程内原生插件（不沙箱） | agent 可自建自改的技能 | 插件 + Connector + ACP |
| 「能常驻」 | 本机长驻 gateway | 网关常驻，且不绑本机 | 单进程常驻服务 |

同一行标签，三方填进去的不是同一件事。第 2 章会逐方给出官方原话，把这几行真正拆开；本章只需读者记住一个结论：**功能清单的每一行是「同类词」，不是「同类事」**。

> [!tip] 大白话
> 把功能清单想成菜单。三家餐厅的菜单上都有「招牌套餐」这一行，点进去，一家是盖饭、一家是火锅、一家是自助。你盯着「都有招牌套餐」比对，永远比不出该去哪家——这一行只是名字相同，端的菜完全不同。

### 1.3 换一把尺子：从「有什么功能」到「同一职责谁来扛」

arXiv 2606.20683 的模型–harness 分析提供了一把更好的尺子。它的核心论断是（逐字引文，取该条贡献句原文全句）：`我们分析了以模型为中心的扩展在长程任务完成上的局限，并论证 agent 的表现是「模型–harness 配对」的属性`（`research/framework/13_arxiv_2606.20683v1_fulltext.md:61`）——agent 的能力不是模型单方面的属性，而是「模型 + harness 配对」的属性。

据此，论文把 harness 拆成六个耦合的运行时职责，逐字定义为（`research/framework/13_arxiv_2606.20683v1_fulltext.md:94-104`）：

| # | 职责 | 逐字定义 |
| --- | --- | --- |
| ① | 观察接口 | `把原始环境信号转成模型可用的观察，包括终端输出、文件差异、截图、DOM 状态、API 响应、日志、检索到的段落与事件流` |
| ② | 上下文管理 | `决定哪些信息进入模型上下文、何时进入、以什么形式进入，涵盖提示词构造、系统指令、检索、记忆选取、压缩、摘要、工具描述与当前任务状态` |
| ③ | 控制循环 | `编排「观察–推理–行动–反馈」循环，包括步骤调度、停止条件、重试、反思、委派、交接与多 agent 协同` |
| ④ | 行动接口 | `把模型输出映射为可执行操作，例如函数调用、MCP 工具、shell 或代码执行、浏览器动作、文件操作、API 调用与子 agent 调用` |
| ⑤ | 状态与工件存储 | `持久化执行状态与产物，包括对话历史、计划、草稿本、检查点、日志、追踪、差异、记忆记录、生成的文件与任务工件` |
| ⑥ | 验证与治理层 | `通过测试、断言、验证器模型、沙箱策略、权限闸、回滚、重试、预算控制、安全约束与审计追踪来检查、约束和修复执行` |

> [!warning] 一处需要并列记录的措辞差异
> 同一篇论文的 abs 页把第六条写成 `观察、上下文、控制、行动、状态与验证`（`research/framework/abs/01_arxiv_org.md:16`），全文写成 `验证/治理`。本文按全文口径，两版差异并列保留、不合并（另见 `02_deep_research.md` §5 C7）。

论文给的「选型透镜」是（逐字）：`任务不只是一个应用标签，而是施加在观察、上下文、控制、行动、状态与治理之上的一个压力剖面`（`research/framework/13_arxiv_2606.20683v1_fulltext.md:212`）。它还把话说死了：`尽管这六个组件在分析上可以分开，它们并不独立运作：一个组件上的设计选择常常会重新分配其他组件上的负担`（同文件 :209）——职责之间互相牵动，所以不能逐项独立打钩。

于是比较单位从「你有什么功能」变成「同一个职责，谁来扛、压在哪」。用这把尺子重问一遍，清单会长这样（本章只列机制名，逐条详证见后章）：

| 职责 | OpenClaw 由谁承接 | Hermes 由谁承接 | Octop 由谁承接 |
| --- | --- | --- | --- |
| ① 观察 | 长驻 Gateway 拥有全部消息面 | 网关接 20+ 消息平台 | 终端 / 浏览器 / 桌面 / 移动通道 |
| ② 上下文 | 工作区 Markdown 记忆 | 内置记忆（有硬上限）+ Honcho | 独立记忆库（分层 + 全文检索） |
| ③ 控制 | gateway + 技能 | 闭环学习（技能自建自改） | 进程内 HarnessProcessor 统一路由 |
| ④ 动作 | 进程内原生插件 | 七种终端后端 | 插件 + Connector + ACP |
| ⑤ 状态 | 工作区里的 Markdown | 按 profile 隔离的 home 目录 | `{workspace}/memory.sqlite` + 控制面库 |
| ⑥ 验证与治理 | 审批 / 沙箱默认关闭；角色是「协作 guardrails」 | allowlist 准入 + admin/user 分级 | JWT 准入 + 权限键 + 行级归属 |

注意左列不是「功能名」而是「职责名」：它问的是「这件事谁扛」，不是「你有没有这个功能」。本章到此为止，不评价任何一方在这些职责上做得好不好。

> [!tip] 大白话
> 把功能清单换成球队位置表。比较两支球队，不该问「你们有没有前锋」，而该问「进攻这个职责，谁在扛、扛到什么程度」。同一个位置名，在两支球队可能是完全不同的人、不同的踢法。问「有没有前锋」只会得到「都有」；问「谁来扛进攻」才分得出样子。

### 1.4 两组「看起来同层」的客观证据（本章不下同层结论）

本章先不判定谁和谁同层——那个判断只由第 6 章的互引互迁证据支撑。但有两组客观证据会让人产生「它们是一类」的直觉，先摆出来：

1. **权威清单同归类。** awesome-ai-agent-platforms 把项目按用途分成五类：`AI 同事与队友、agent 构建工具与框架、工作流自动化平台、浏览器 agent 与编码 agent`（`research/framework/17_awesome-ai-agent-platforms_README.md:10`），分类规则是 `每个项目只出现一次，归在与其主要用途最匹配的那一类下`（同文件 :112）。OpenClaw 与 Hermes 同收在 `AI 同事与队友` 一节下（同文件 :36、:41）；而 `编码 agent` 是**独立的一类**（该节定义 `专门写代码、改代码、发布代码的 agent`，同文件 :93），与前者并列而不混同。
2. **官方口径把对方当同类。** OpenClaw 官方有一张专页做逐轴对照：`反复被拿来对照的对象是 Hermes Agent（原文此处带一个指向对方仓库的链接）`（`02_deep_research.md` §3.1 A6）。这条本章只用来交代「看起来同层」的证据来自哪里，具体引用与站位判断留到第 6 章。

### 1.5 为什么不能拿 Star 数当依据

很多人拿 Star 数当选型依据，因为它是最容易拿到的一个数。但它恰恰最不可靠：

- **同一对象、同一时期的公开数字互相矛盾。** 围绕这几个仓库流传的 Star 口径彼此对不上、跨度极大，`02_deep_research.md` §5 C2 的处置是「**数据严重不一致，标注为不可靠，不作为选型证据**」。一个连口径都对不齐的数字，不该用来选型。
- **权威清单明确把它排除在入选标准之外。** `入选不等于推荐，星标数、融资额与公司规模都不是入选标准`（`research/framework/17_awesome-ai-agent-platforms_README.md:112`）。

Star 数量的是「有多少人注意到了它」，不是「它适不适合你的场景」。本文后续所有比较都不使用 Star 数。

### 1.6 本章落点：三层归位

三层坐标里，第 1 层的证据最弱，必须显式声明其边界。本章关于第 1 层只能说两件事：

- **分类上独立成类**：上一节已给出，`编码 agent` 在权威清单里是与 `AI 同事与队友` 并列的独立一类。
- **Octop 的邻近参照物落在第 1 层（本文的推断）**：Octop 全库检索 `openclaw|hermes` **零命中**；它在 ACP 文档里命名的外部 agent 工具**只有 ACP runner，内置 7 个**（`opencode`、`codebuddy`、`claude_code`、`codex`、`kimi_code`、`cursor_cli`、`pi`，`research/octop/docs/acp.md:29-38`），均为编码类、以命令行接入，方向是 **outbound 委派**——`Octop agent 委派编码任务`（同文件 :8）。

  需要说明的是：把这 7 个逐个归入「本地 CLI 阵营」是**本文的推断**——官方并未使用这个分类词，官方给的只有上面这张 runner 表。推断的依据是判据①（它们都不是常驻服务）与它的用途（承接编码类委派）；读者可以据此自行判断是否接受这一步。

因此显式声明：**第 1 层（本地 CLI 阵营）在本文中只作坐标系，本文的比较对象是第 2、3 层；第 1 层不展开。** 并且不得引用 `01_explore_result.md` 候选表里未落盘原文的条目（例如 #16 这条 OpenHands issue）作为证据。

### 本章小结

- 「感觉都一样」是把不同层的东西塞进同一张功能清单对读，属**范畴错误**，不是产品缺陷。
- 分层判据是**同一根轴上的两问**：是否常驻服务 × 服务的用户数是单数还是复数；两问交叉出「本地 CLI 阵营 / 个人助手 harness / 多用户平台」三层。
- 功能清单必然叠影，因为每一行是「同类词」而非「同类事」；同一行标签下三方填的不是同一件事。
- 换用 arXiv 的**压力剖面**透镜后，比较单位从「有什么功能」变成「同一个职责谁来扛」。
- Star 数不可作选型依据（数字互相矛盾，且权威清单明确排除）。
- 第 1 层只作坐标系，本文比较对象是第 2、3 层。

**下一章预告**：既然功能清单会叠影，就先拆开撞得最狠的那一行——「多用户」。第 2 章把三方在这一行上各自说的到底是哪件事，用官方原话逐方并置，你会看到这个词被用成了三种互不相同的语义。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `A single long-lived **Gateway** owns all messaging surfaces` | 一个长期存活的 **Gateway** 掌管全部消息面 | `research/openclaw/01_docs_openclaw_ai.md:11` |
| 2 | `The messaging gateway is the long-running process that connects Hermes to 20+ external messaging platforms through a unified architecture.` | 消息网关是一个常驻进程，通过统一的架构把 Hermes 接到 20 多个外部消息平台上 | `research/hermes/gw/01_hermes-agent_nousresearch_com.md:9` |
| 3 | `Everything runs in a single Python process served by uvicorn.` | 一切都跑在一个由 uvicorn 提供服务的 Python 进程里 | `research/octop/docs/adr/001-single-process-model.md:14` |
| 4 | `Manage the Octop system service (systemd on Linux, launchd on macOS).` | 把 Octop 作为系统服务来管理（Linux 上用 systemd，macOS 上用 launchd） | `research/octop/docs/cli.md:120` |
| 5 | `Octop is a self-hosted AI assistant platform for households and small teams.` | Octop 是一个面向家庭与小团队的自托管 AI 助手平台 | `research/octop/README.md:69` |
| 6 | `Default OpenClaw is a trusted single-operator assistant.` | 默认的 OpenClaw 是一个受信的单操作者助手 | `research/openclaw/02_docs_openclaw_ai.md:64` |
| 7 | `## What we do not claim` | 我们不做哪些声明 | `research/openclaw/03_docs_openclaw_ai.md:118` |
| 8 | `It is not an authorization or isolation boundary.` | 它不构成授权或隔离边界 | `research/openclaw/03_docs_openclaw_ai.md:118` |
| 9 | `**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` | 默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户 | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327` |
| 10 | `with its own bot tokens, sessions, and memory` | 各有自己的 bot token、会话与记忆 | `research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:9` |
| 11 | `We analyze the limits of model-centric scaling for long-horizon task completion and argue that agent performance is a property of the model–harness pairing.` | 我们分析了以模型为中心的扩展在长程任务完成上的局限，并论证 agent 的表现是「模型–harness 配对」的属性 | `research/framework/13_arxiv_2606.20683v1_fulltext.md:61` |
| 12 | `transforms raw environment signals into model-usable observations, including terminal output, file diffs, screenshots, DOM states, API responses, logs, retrieved passages, and event streams.` | 把原始环境信号转成模型可用的观察，包括终端输出、文件差异、截图、DOM 状态、API 响应、日志、检索到的段落与事件流 | — |
| 13 | `determines what information enters the model context, when it enters, and in what form, covering prompt construction, system instructions, retrieval, memory selection, compression, summarization, tool descriptions, and current task state.` | 决定哪些信息进入模型上下文、何时进入、以什么形式进入，涵盖提示词构造、系统指令、检索、记忆选取、压缩、摘要、工具描述与当前任务状态 | — |
| 14 | `orchestrates the observe-reason-act-feedback cycle, including step scheduling, stopping criteria, retries, reflection, delegation, handoffs, and multi-agent coordination.` | 编排「观察–推理–行动–反馈」循环，包括步骤调度、停止条件、重试、反思、委派、交接与多 agent 协同 | — |
| 15 | `maps model outputs to executable operations, such as function calls, MCP tools, shell or code execution, browser actions, file operations, API calls, and sub-agent invocations.` | 把模型输出映射为可执行操作，例如函数调用、MCP 工具、shell 或代码执行、浏览器动作、文件操作、API 调用与子 agent 调用 | — |
| 16 | `persists execution state and products, including conversation history, plans, scratchpads, checkpoints, logs, traces, diffs, memory records, generated files, and task artifacts.` | 持久化执行状态与产物，包括对话历史、计划、草稿本、检查点、日志、追踪、差异、记忆记录、生成的文件与任务工件 | — |
| 17 | `checks, constrains, and repairs execution through tests, assertions, verifier models, sandbox policies, permission gates, rollback, retry, budget control, safety constraints, and audit traces.` | 通过测试、断言、验证器模型、沙箱策略、权限闸、回滚、重试、预算控制、安全约束与审计追踪来检查、约束和修复执行 | — |
| 18 | `observation, context, control, action, state, and verification` | 观察、上下文、控制、行动、状态与验证 | `research/framework/abs/01_arxiv_org.md:16` |
| 19 | `a task is not merely an application label but a pressure profile over observation, context, control, action, state, and governance` | 任务不只是一个应用标签，而是施加在观察、上下文、控制、行动、状态与治理之上的一个压力剖面 | `research/framework/13_arxiv_2606.20683v1_fulltext.md:212` |
| 20 | `Although the six components are analytically separable, they do not operate independently. Design choices in one component often reshape the burden on others.` | 尽管这六个组件在分析上可以分开，它们并不独立运作：一个组件上的设计选择常常会重新分配其他组件上的负担 | `research/framework/13_arxiv_2606.20683v1_fulltext.md:212` |
| 21 | `AI coworkers and teammates, agent builders and frameworks, workflow automation platforms, browser agents, and coding agents` | AI 同事与队友、agent 构建工具与框架、工作流自动化平台、浏览器 agent 与编码 agent | `research/framework/17_awesome-ai-agent-platforms_README.md:10` |
| 22 | `Each project appears once, under the category that best matches its main use.` | 每个项目只出现一次，归在与其主要用途最匹配的那一类下 | `research/framework/17_awesome-ai-agent-platforms_README.md:10` |
| 23 | `AI coworkers and teammates` | AI 同事与队友 | `research/framework/17_awesome-ai-agent-platforms_README.md:10` |
| 24 | `coding agents` | 编码 agent | `research/framework/17_awesome-ai-agent-platforms_README.md:10` |
| 25 | `Agents specialized in writing, editing, and shipping code.` | 专门写代码、改代码、发布代码的 agent | `research/framework/17_awesome-ai-agent-platforms_README.md:10` |
| 26 | `The recurring comparison is [Hermes Agent]` | 反复被拿来对照的对象是 Hermes Agent（原文此处带一个指向对方仓库的链接） | `02_deep_research.md` |
| 27 | `Inclusion is not an endorsement, and star counts, funding, and company size are not criteria.` | 入选不等于推荐，星标数、融资额与公司规模都不是入选标准 | `research/framework/17_awesome-ai-agent-platforms_README.md:112` |
| 28 | `Octop agent delegates coding tasks` | Octop agent 委派编码任务 | `research/octop/docs/acp.md:29-38` |

## 第 2 章 「多用户」一词三义 —— 三方原文并置

### 本章要解决的问题

第 1 章指出「感觉都一样」是范畴错误，本章定位错因。三方**都**说「支持多用户」，但在官方原文里，这个词指的是三件互不相同的事。本章逐方给出限定语后的准确语义——OpenClaw 的「多用户」（同一信任域内的协作）、Hermes 的「多用户」（准入与很窄的分级）、Octop 的「多用户」（行级归属）——并说明为什么这正是「功能清单叠影」的根因。本章不讲隔离的具体实现机制（留给第 3 章），不讲部署形态（留给第 4、5 章），也不给选型建议。

### 2.1 三方都说「支持多用户」，但说的不是一件事

「都支持多用户」为什么不构成它们是一类的证据？因为「多用户」在功能清单里只是一个**标签**：标签可以共享，被标签指向的东西不必相同。下面先把三方各自的标签指向什么并排列出，再逐方看标签底下的语义——这正是第 1 章那把「压力剖面」尺子落到一个具体词上的样子。

先约定读法：从本章起，「多用户」这个词一旦出现，必定紧跟限定语，指明它说的是哪一层语义——① 同一信任域内的协作、② 准入与很窄的分级、③ 行级归属。下面这张表是全篇的锚，第 3、5、7 章会逐字复用它的列名与三行措辞：

| 平台       | 限定语后的准确语义                                                                    | 关键原文（逐字）                                                                                                                                                                                                                                                                                                                           | 锚点                                                                                                                                                         |
| -------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OpenClaw | **同一信任域内的协作**：多个受信的人操作同一个 agent、共享同一个信任域；此处「多用户」是「易用性功能」，明确不是安全边界            | `多用户模式让多个受信的人操作同一个 OpenClaw agent` / `易用性功能，不是安全边界` / `它不构成授权或隔离边界`                                                                                                                                               | `research/openclaw/03_docs_openclaw_ai.md:10,12,118`                                                                                                       |
| Hermes   | **准入与很窄的分级**：默认拒绝所有不在白名单、未配对的用户；进来后再分 admin / user 两档，且分级目前只管斜杠命令；无租户语汇 | ``默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户`` / `白名单回答「这个人能不能够到这个 bot」，而 **admin / user 分级**回答「进来之后允许他做什么」` / `发送者路由只是在挑 profile，不是默认拒绝式的授权` | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327,369`、`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:645` |
| Octop    | **行级归属**：JWT 准入 + 行级归属（`agents.user_id`）为真正的数据隔离；单实例承载多个账号，官方规模口径限定为家庭与小团队   | ``每个请求都先过 JWT 认证，再落到一行 User 记录`` / `agent 归属在**行级**强制执行` / `Octop 是一个面向家庭与小团队的自托管 AI 助手平台`                                                                                                                     | `research/octop/docs/architecture.md:69,71`、`research/octop/README.md:69`                                                                                  |

这张表的三行不是同一件事的三档强弱，而是三种不同的东西；至于它们能不能排在一条强度轴上，是第 3 章的任务。

### 2.2 OpenClaw：同一信任域内的协作

OpenClaw 的「多用户」（同一信任域内的协作）官方定义是：`多用户模式让多个受信的人操作同一个 OpenClaw agent`（`research/openclaw/03_docs_openclaw_ai.md:10`）。它由四件东西组成——会话归属、参与者历史、实时在场、按所有者过滤；每个会话最多带三层署名：

`每个会话最多携带三层归属信息：`（同文件 :19）

三层分别是不可变的 Creator、可指派的 Owner、按历史记录的 Participants。准入走 DM 配对码：`队友第一次私聊这个 bot 时会拿到一个配对码`（`research/openclaw/05_docs_openclaw_ai.md:38`）；分级靠命名角色：`命名操作者角色把已认证的 profile 绑定到一套策略上`（同文件 :49）。

关键在于官方给这套能力的两句自我限定。第一句：`易用性功能，不是安全边界`（`research/openclaw/03_docs_openclaw_ai.md:12`）。第二句更直接：`它不构成授权或隔离边界`（同文件 :118）。换句话说，OpenClaw 的「多用户」（① 同一信任域内的协作）是「让团队看清谁在做什么」的显示层，不是把用户彼此隔开的边界。官方还补了一句对照：`这只是一个信任域内部挑选账号的便利，而不是与管理员、或与以 Gateway 系统用户身份运行的代码隔离`（同文件 :72）。`因此单用户网关看起来几乎没有变化`（同文件 :91）。

还有两条边界值得记住。其一，`一个 Gateway 就是一个信任域`（`research/openclaw/05_docs_openclaw_ai.md:21`）——协作 guardrails 是在这个域**之内**生效的。其二，`每个逻辑会话的默认准入上限是 32 个身份`（`research/openclaw/03_docs_openclaw_ai.md:126`）。这两条一起说明：OpenClaw 的「多用户」（同一信任域内的协作）是往单用户模型上叠的一层，而不是把它换成多租户模型。

> [!tip] 大白话
> 把 OpenClaw 的「多用户」（同一信任域内的协作）想成一本全家共用的记账本：谁都能翻、能写、还看得出谁记了哪一笔（三层署名），但没有人被挡在账本外面。它管的是「看得清」，不是「防得住」。

### 2.3 Hermes：准入与很窄的分级

Hermes 的「多用户」（准入与很窄的分级）起点是一句默认拒绝：``默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户``（`research/hermes/03_raw_githubusercontent_com_messaging-index.md:327`）。进门靠白名单（`TELEGRAM_ALLOWED_USERS=123456789,987654321`，同文件 :331）或 DM 配对码。

进门之后只有两档：`每个被放行的用户在每个作用域里（私聊 vs 群组 / 频道）都落在两档之一：`（同文件 :371）。官方把它总结成两个问题的分工：`白名单回答「这个人能不能够到这个 bot」，而 **admin / user 分级**回答「进来之后允许他做什么」`（同文件 :369）。

但「分级」的实际边界很窄，必须把实证写出来：`目前分级管的是什么：斜杠命令。……普通对话不受影响——非管理员仍然可以和 agent 说话`（同文件 :378）。也就是说，这两档目前**只管斜杠命令**，普通对话不受限。

另一处容易误读的是 profile 路由。它不是授权：`发送者路由只是在挑 profile，不是默认拒绝式的授权`（`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:645`）。profile 的示例用途之一是「同一个人的多个 agent」，不是多个租户：`一个 Telegram bot 上跑私人助手、另一个上跑编码 agent`（同文件 :13）。

把这四句连起来读，Hermes 的「多用户」（准入与很窄的分级）可以概括成：一台机器、一个所有者，决定「谁能够到这个 bot」，以及「够到之后分几档」。它不是「一台机器服务多个互不信任的主体」——那恰恰是它通篇没有租户语汇的原因。

> [!tip] 大白话
> 把 Hermes 的「多用户」（准入与很窄的分级）想成公司门禁：刷卡才能进楼（白名单 / 配对），进楼后分「管理员」和「普通员工」两种卡——但这张卡目前只管你能不能按电梯里的少数几个按钮（斜杠命令），走廊里聊天说话（普通对话）根本没人拦。

### 2.4 Octop：行级归属

Octop 的「多用户」（行级归属）是架构内建的。``每个请求都先过 JWT 认证，再落到一行 User 记录``（`research/octop/docs/architecture.md:69`）。真正做数据隔离的机制是行级归属——agent 行的 `user_id` 必须匹配调用者：`agent 归属在**行级**强制执行`（同文件 :71，机制细节留到第 3 章）。准入也不是自助注册：首个管理员由安装向导创建，其余成员靠邀请制加入（`class InviteCreateBody(BaseModel):` / `expires_in_days: int = Field(`，`research/octop/src/octop/api/routers/invites.py:55,57`）。

这里要点出与前两方的结构性差别——官方规模口径：`Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）；中文口径把它说得更直白：`**家庭共享** — 一个管理员账号，全家共用；按成员分配不同 Agent 与专家角色`（`research/octop/README_CN.md:76`）。这是一个「一个管理员 + 成员」的模型，不是一个平等多租户模型。

> [!tip] 大白话
> 把 Octop 的「多用户」（行级归属）想成公司给每人分配了自己的文件柜格子：门禁（JWT）让你进楼，但你只能打开写着你名字的那几格——别人名字的格子，从数据那一行起就不归你。

### 2.5 同词异指，而不是产品雷同

把三节并起来看：三方都写「支持多用户」，但一个说的是同一信任域内的协作（看得清），一个说的是准入与很窄的分级（进得来、分两档），一个说的是行级归属（数据按行分给谁）。**这就是功能清单必然叠影的根因——大家在同一个词上做的是不同的事。**

回头对第 1 章那张叠影表：「多用户」这一行之所以会撞车，不是三方产品一样，而是三方共用了「多用户」这个**同类词**。差异不在功能名，在功能名底下的语义。这个机制一旦看清，就能解释一个常见现象：把三方的功能清单并排放，重合的行会显得很多（「多用户」「记忆」「技能」「常驻」……），但每一行的重合都只是**词面**重合。所以任何横向比较只要停在词面，都会得到「都有」；只有把词面逐个翻译成限定语义，比较才开始有信息量。这也是为什么第 1 章要把比较单位从「有什么功能」换成「同一职责谁来扛」——前者天然停在同一批词上。

> [!tip] 大白话
> 这就像三个人都说自己「会游泳」：一个在泳池里游 25 米，一个在岸边浮潜，一个能横渡海峡。都写「会游泳」没有错，但把这三行放进同一张表比较「游泳能力」，那个「都有」毫无意义——你得先问清是哪种水、游多远。

### 2.6 两个边界：多用户平台 ≠ 多租户平台，以及两处 tenant 假阳性

**硬结论：多用户平台 ≠ 多租户平台。** 三方中只有 OpenClaw 有租户词汇，且自带 experimental 标注：`租户意味着一个租户一个 gateway cell，而 fleet 目前仍是实验性的`（`research/openclaw/02_docs_openclaw_ai.md:65`）。它明确拒绝在一个 Gateway 内做多租户：`OpenClaw 的默认安全模型是「每个 Gateway 一个受信操作者边界」，而不是在共享的同一个 Gateway 内部做敌意多租户隔离`（`research/openclaw/04_docs_openclaw_ai.md:10`）。`没有企业版`（`research/openclaw/02_docs_openclaw_ai.md:20`）。Hermes 与 Octop 都不在这条轴上。

三方的站位因此是：Octop 是**多用户平台**（家庭与小团队、单实例、行级归属），OpenClaw 明确**拒绝**做多租户（`不是在同一个共享 Gateway 内部做敌意多租户隔离`），Hermes 根本没有租户语汇。把「多用户」和「多租户」当成同一件事，是本章最需要防住的一次混读。

> [!warning] 两处 `tenant` 是假阳性，别读成租户模型
> Hermes 与 Octop **各有且仅有一处** `tenant`，两处都是消息路由字段，结构完全对称：
> - Hermes：`在某些平台上，发送者 ID 也按租户加了命名空间——Slack 的用户 ID 是工作区局部的`（`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:643`）——这里的 tenant 指消息平台（Slack 工作区），不是 Hermes 自身的租户。
> - Octop：`tenant_id=agent_id,`（`research/octop/src/octop/api/routers/chat/turn.py:348`）——这是把 agent ID 复用为消息路由的租户 ID，同样不是租户模型。
> 把任一处的出现读成「某方有租户能力」，都属误读。

### 本章小结

- 三方都说「支持多用户」，但这词有三个互不相同的限定语义：OpenClaw = 同一信任域内的协作，Hermes = 准入与很窄的分级，Octop = 行级归属。
- OpenClaw 的这套能力被官方明确标注为 `易用性功能，不是安全边界`。
- Hermes 的默认准入策略是「默认拒绝」，但两档分级目前只管斜杠命令，profile 路由不是授权。
- Octop 方（③ 行级归属）：架构内建，数据隔离靠行级归属，规模口径限定为家庭与小团队。
- 功能清单叠影的根因是**同词异指**，不是产品雷同。
- 硬结论：多用户平台 ≠ 多租户平台；Hermes 与 Octop 各一处 `tenant` 都是消息字段，非租户。

**下一章预告**：三种语义目前还是三个并列的说法。第 3 章把它们翻译成一条**可测量、可排序**的轴——隔离强度梯度「不提供隔离 → 准入与很窄的分级 → 行级归属」，并给出每一档对应的现实后果。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Multi-user mode lets several trusted people operate the same OpenClaw agent.` | 多用户模式让多个受信的人操作同一个 OpenClaw agent | `research/openclaw/03_docs_openclaw_ai.md:10,12,118` |
| 2 | `usability features, not security boundaries` | 易用性功能，不是安全边界 | `research/openclaw/03_docs_openclaw_ai.md:10,12,118` |
| 3 | `It is not an authorization or isolation boundary.` | 它不构成授权或隔离边界 | `research/openclaw/03_docs_openclaw_ai.md:10,12,118` |
| 4 | `**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` | 默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户 | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327,369` |
| 5 | `Allowlists answer "can this person reach the bot at all?" The **admin / user split** answers "now that they're in, what are they allowed to do?"` | 白名单回答「这个人能不能够到这个 bot」，而 **admin / user 分级**回答「进来之后允许他做什么」 | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327,369` |
| 6 | `Sender routing selects a profile; it is not deny-by-default authorization.` | 发送者路由只是在挑 profile，不是默认拒绝式的授权 | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327,369` |
| 7 | ``Every request is authenticated via JWT and resolved to a `User` row.`` | 每个请求都先过 JWT 认证，再落到一行 User 记录 | `research/octop/docs/architecture.md:69,71` |
| 8 | `Agent ownership is enforced at the **row** level` | agent 归属在**行级**强制执行 | `research/octop/docs/architecture.md:69,71` |
| 9 | `Octop is a self-hosted AI assistant platform for households and small teams.` | Octop 是一个面向家庭与小团队的自托管 AI 助手平台 | `research/octop/docs/architecture.md:69,71` |
| 10 | `Every session carries up to three layers of attribution:` | 每个会话最多携带三层归属信息： | — |
| 11 | `the first time a teammate DMs the bot they get a pairing code` | 队友第一次私聊这个 bot 时会拿到一个配对码 | `research/openclaw/05_docs_openclaw_ai.md:38` |
| 12 | `Named operator roles bind authenticated profiles to a policy` | 命名操作者角色把已认证的 profile 绑定到一套策略上 | `research/openclaw/05_docs_openclaw_ai.md:38` |
| 13 | `This is account-selection convenience inside one trust domain, not isolation from administrators or code running as the Gateway OS user.` | 这只是一个信任域内部挑选账号的便利，而不是与管理员、或与以 Gateway 系统用户身份运行的代码隔离 | `research/openclaw/03_docs_openclaw_ai.md:12` |
| 14 | `A single-user gateway therefore looks unchanged.` | 因此单用户网关看起来几乎没有变化 | `research/openclaw/03_docs_openclaw_ai.md:12` |
| 15 | `A gateway is one trust domain.` | 一个 Gateway 就是一个信任域 | `research/openclaw/05_docs_openclaw_ai.md:21` |
| 16 | `The normal admission limit is 32 identities per logical session.` | 每个逻辑会话的默认准入上限是 32 个身份 | `research/openclaw/03_docs_openclaw_ai.md:126` |
| 17 | `Every allowed user falls into one of two tiers per scope (DM vs group/channel):` | 每个被放行的用户在每个作用域里（私聊 vs 群组 / 频道）都落在两档之一： | — |
| 18 | `**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.` | 目前分级管的是什么：斜杠命令。……普通对话不受影响——非管理员仍然可以和 agent 说话 | — |
| 19 | `A personal assistant on one Telegram bot and a coding agent on another` | 一个 Telegram bot 上跑私人助手、另一个上跑编码 agent | `research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:645` |
| 20 | `Tenancy means one gateway cell per tenant, and fleet is still experimental.` | 租户意味着一个租户一个 gateway cell，而 fleet 目前仍是实验性的 | `research/openclaw/02_docs_openclaw_ai.md:65` |
| 21 | `OpenClaw's default security model is one trusted operator boundary per Gateway, not hostile multi-tenant isolation inside one shared Gateway.` | OpenClaw 的默认安全模型是「每个 Gateway 一个受信操作者边界」，而不是在共享的同一个 Gateway 内部做敌意多租户隔离 | `research/openclaw/04_docs_openclaw_ai.md:10` |
| 22 | `There is no enterprise edition.` | 没有企业版 | `research/openclaw/02_docs_openclaw_ai.md:20` |
| 23 | `not hostile multi-tenant isolation inside one shared Gateway` | 不是在同一个共享 Gateway 内部做敌意多租户隔离 | — |
| 24 | `Sender ids are also namespaced per tenant on some platforms — a Slack user id is workspace-local` | 在某些平台上，发送者 ID 也按租户加了命名空间——Slack 的用户 ID 是工作区局部的 | `research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:643` |

## 第 3 章 隔离强度梯度 —— 不提供隔离 / 准入与很窄的分级 / 行级归属

### 本章要解决的问题

第 2 章给出了三方「多用户」的三种语义，但它们还是三个并列的说法。本章把它们翻译成一条**可测量、可排序**的轴：三方的「多用户」隔离强度不同，并能按强度排出梯度。这是本文第一次出现可直接用于决策的维度。本章不讨论部署形态与运维成本（第 4、5 章），不讨论三方互相引用关系（第 6 章），也不给最终选型建议。

### 3.1 从「三种语义」到「一条梯度」

为什么需要这条轴？第 2 章的三义是三个**并列**的说法，而并列的说法之间无法比较——你没法说「同一信任域内的协作」比「行级归属」更好还是更差，因为它们根本不同类。梯度把它们投射到同一维度上：一旦都改问「对越权的拒绝有多硬」，三种说法就变成三个可以排序的档位。

排序判据是：对一个用户能否碰到另一个用户的数据与能力，官方给出的**拒绝有多硬**。三档由弱到强是——**不提供隔离 → 准入与很窄的分级 → 行级归属**。

| 强度（由弱到强） | 平台 | 官方措辞（逐字） | 一句话后果 |
| --- | --- | --- | --- |
| 不提供隔离 | OpenClaw | `易用性功能，不是安全边界` / `它不构成授权或隔离边界` | 「多用户」是同一信任域内的协作便利，不是安全边界 |
| 准入与很窄的分级 | Hermes | `**admin / user 分级**` / `目前分级管的是什么：斜杠命令` | 挡在门外靠白名单；进来后只分两档，且只管斜杠命令 |
| 行级归属 | Octop | `agent 归属在**行级**强制执行` / `只选当前用户自己的 agent，不包含其他用户或共享 agent` | 数据按行归属，越权在数据层被拒 |

注意三档与第 2 章三义的对应是**逐字对齐**的：同一信任域内的协作 → 不提供隔离；准入与很窄的分级 → 准入与很窄的分级；行级归属 → 行级归属。后两档同名不是巧合——第 2 章回答的是「这是什么」，本章排的是「这在隔离轴上多强」，同一件事换了个提问方式而已。

> [!warning] 这张梯度的判据是官方措辞，不是性能实测
> 三档的排序依据是各方**自己怎么描述这套机制**（明确「不是边界」→ 只挡门、分两档 → 数据按行归属），不是吞吐或压测数据。它回答的是「官方怎么定义这套能力」，不是「它扛得住多少人」。

### 3.2 弱档：OpenClaw 明确声明不提供隔离

OpenClaw 这一档的强度是「不提供隔离」，而且这句话是官方自己反复说的：这些能力是 `易用性功能，不是安全边界`（`research/openclaw/03_docs_openclaw_ai.md:12`），`它不构成授权或隔离边界`（同文件 :118）。它不是「忘了做」，而是在产品定位里主动放弃：`没有企业版`（`research/openclaw/02_docs_openclaw_ai.md:20`）。

隔离既然不在一个 Gateway 内提供，跨信任域就靠「一租户一实例」绕开——`不是在同一个共享 Gateway 内部做敌意多租户隔离`（`research/openclaw/04_docs_openclaw_ai.md:10`）。这条绕行路线（fleet）留到第 6 章，本章只需记住：**OpenClaw 档意味着「多用户」是同一信任域内的协作便利，不是把互不信任的人隔开的安全机制**。参与者集合另有默认上界 `每个逻辑会话的默认准入上限是 32 个身份`（`research/openclaw/03_docs_openclaw_ai.md:126`），但那是会话内的记录上限，不是权限边界。

这一档对选型的含义是明确的：如果你的需求是把互不信任的人隔开，OpenClaw 这一档不提供答案——而这不是「配置没开对」，是产品模型本身如此（`没有企业版`）。要跨信任域，只能换形态：一个租户一个实例。

> [!tip] 大白话
> 这一档像合租公寓的公共厨房：大家共用同一套灶具，墙上贴了「谁用了哪口锅」的标签（署名）。标签让协作更顺，但它拦不住任何人拿你的锅——因为这里默认大家是互相信得过的室友。

### 3.3 中档：Hermes 准入与很窄的分级

Hermes 比 OpenClaw 多了一道「准入」，这是它排在中间的原因。默认就是拒绝：``默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户``（`research/hermes/03_raw_githubusercontent_com_messaging-index.md:327`）。

但准入之后的「分级」很薄，必须把实证写清楚，否则这一档会被高估：

- 只有两档，没有再细：`每个被放行的用户在每个作用域里（私聊 vs 群组 / 频道）都落在两档之一：`（同文件 :371）。
- 目前分级只管斜杠命令：`目前分级管的是什么：斜杠命令。……普通对话不受影响——非管理员仍然可以和 agent 说话`（同文件 :378）。
- profile 路由不是授权：`发送者路由只是在挑 profile，不是默认拒绝式的授权`（`research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:645`）。

所以中档的准确描述是「**准入与很窄的分级**」：门禁是真的（默认拒绝），进门后的隔离却很薄（两档、只覆盖斜杠命令）。它挡住的不是「恶意用户」，而是「不在名单上的人」。

> [!tip] 大白话
> 这一档像有前台的公司：名单外的人进不来（白名单），进来后前台给你一张「管理员」或「普通员工」的卡。但这张卡目前只管你能不能按电梯里少数几个按钮（斜杠命令），进了办公区怎么走、跟谁说话，没人再管。

### 3.4 强档：Octop 行级归属

Octop 这一档的强度最高，机制是**三层叠加、各管一段**：准入管进门，权限键管管理页与写 / 配置动作，行级归属管数据隔离。

| 层 | 机制 | 边界 / 锚点 |
| --- | --- | --- |
| ① 准入 | 全局 JWT；只有一份豁免白名单（`/api/health`、`/api/auth/*`、`/api/docs` 等） | `research/octop/src/octop/api/deps.py:65-89` |
| ② 模块权限键 | 权限是模块键（如 `"browser"`、`"users"`）；持有键才可访问该模块**管理页与写 / 配置动作** | `research/octop/src/octop/infra/users/permissions.py:3-4` |
| ③ 归属（真正的数据隔离） | agent 行的 `user_id` 匹配调用者；本人 / `agent_is_shared` / admin 三选一 | `research/octop/docs/architecture.md:71`、`research/octop/src/octop/api/common/agent.py:18-23,26-31,51-53` |

看一个带具体值的判定，理解第三层到底在做什么。设 agent X 行上 `user_id = 9`，调用者 Alice 的 id = 7。归属判定只有几行代码：`user_owns_agent` 要求 `row.user_id is not None and row.user_id == user.id`（`research/octop/src/octop/api/common/agent.py:14-15`）；`assert_agent_owner` 在非 admin 时，只要 `row.user_id is None or row.user_id != user.id` 就抛 `agent not owned by user`（同文件 :18-23）。代入数值：9 ≠ 7 且 Alice 非 admin，于是拒绝。唯一能放行的三种情形是——本人、`agent_is_shared(row)`、或 admin（同文件 :26-31）。**越权是在数据那一行上被拒的**，不是靠前端隐藏入口。

强档必须**分层陈述**，否则会掉进一个常见误读。`permissions.py` 的模块说明里有这么一句：`读取权限与在对话中使用 agent 从不受分级限制`——但这是就「模块权限键」这一层而言的，且**按字面读不成立**：

- 同模块内「读不加键、写加键」：`GET ""`（列出已安装插件）只挂 `Depends(current_user)`（`research/octop/src/octop/api/routers/plugins.py:99-104`），而 `POST /reload` 用 `require_permission("plugins")`（同文件 :110）；`GET /market` 只挂 `current_user`（:207），而 `POST /market/{plugin_id}/install` 用 `require_permission("plugins")`（:221）。
- admin 域的可读端点**确实加键**：`GET ""`（列出用户）→ `require_permission("users")`（`research/octop/src/octop/api/routers/users.py:270-272`）、`GET /{user_id}` → 同（同文件 :431-435）、`GET ""`（列出角色模板）→ 同（`research/octop/src/octop/api/routers/user_roles.py:183-186`）。
- 而聊天 / 会话读端点确实只挂 `Depends(current_user)`，无 `require_permission`（`research/octop/src/octop/api/routers/chat/history.py:104,150,166,217,253,289`）。

> [!warning] 别把它写成「读访问无权限控制」
> 准确说法是：**权限键管管理页与写 / 配置动作，数据隔离由 `user_id` 行级归属另负。** 把它简化成「Octop 读访问无权限控制」是错的——admin 域（users / user_roles）的读端点明确要 `require_permission("users")`。

这一档的隔离边界还延伸到运维动作：`对话的 --all 与本地管理 CLI 范围不同：只选当前用户自己的 agent，不包含其他用户或共享 agent。`（`research/octop/docs/memory-slim.md:87`）——即便是一个批量维护命令，也只作用于自己名下的 agent。

> [!tip] 大白话
> 这一档像给每个人配了带锁的文件柜：门禁（JWT）让你进楼，「admin」区还要单独钥匙（模块权限键），而柜子本身按行归属——`agents.user_id` 写的是谁，数据就只对谁开。别人名字的柜子，从数据那一行起就打不开。

### 3.5 强档也有例外：隔离可由 owner 主动放宽

强档不等于密不透风。Octop 的隔离是「默认按行归属」，但 owner 可以主动放宽：`**专家共享** — 支持用户将自有专家共享给其他用户使用`（`research/octop/README_CN.md:162`），机制上对应 `agent_is_shared(row)` 这条放行分支（`research/octop/src/octop/api/common/agent.py:51-53`）。也就是说，跨用户访问不是被技术禁止，而是默认关闭、需被授权者显式打开。

还要注意版本边界：这套治理能力是**增量加入**的，不是初版即有——RBAC（按用户模块权限）记在 `## [0.9.24] - 2026-08-15`（`research/octop/CHANGELOG.md:396`）、按用户存储与 Token 配额记在 `## [0.9.33] - 2026-09-11`（同文件 :192）。这意味着两件事：一是强档描述反映的是较新的版本；二是针对「多用户」的治理能力在这条产品线上是逐步长出来的，拿着旧版本对照本文可能会对不上。

### 本章小结

- 三方的「多用户」隔离强度可排成一条由弱到强的轴：**不提供隔离 → 准入与很窄的分级 → 行级归属**。
- 弱档（OpenClaw）：官方明确标注不是安全边界，「多用户」是同一信任域内的协作便利。
- 中档（Hermes）：默认拒绝的准入是真的，但分级只有两档且只管斜杠命令，profile 路由不是授权。
- 强档（Octop）：准入 + 模块权限键 + 行级归属三层叠加；权限键管管理页与写 / 配置动作，数据隔离由 `user_id` 行级归属另负，不能说成「读访问无权限控制」。
- 强档也有例外：隔离可由 owner 主动放宽（专家共享），且治理能力是增量加入的。

**下一章预告**：梯度讲的是「同一件事的强弱」。但 OpenClaw 与 Hermes 这两方在第 1 章的三层坐标里同属第 2 层（个人助手 harness），它们之间还有没有一根能直接回答「什么场景用哪个」的轴？第 4 章给出这根轴——部署姿态：本机常驻，还是「不绑本机」。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `usability features, not security boundaries` | 易用性功能，不是安全边界 | `research/openclaw/03_docs_openclaw_ai.md:12` |
| 2 | `It is not an authorization or isolation boundary.` | 它不构成授权或隔离边界 | `research/openclaw/02_docs_openclaw_ai.md:20` |
| 3 | `The admin / user split` | **admin / user 分级** | — |
| 4 | `What the tiers gate today: slash commands` | 目前分级管的是什么：斜杠命令 | — |
| 5 | `Agent ownership is enforced at the **row** level` | agent 归属在**行级**强制执行 | — |
| 6 | `There is no enterprise edition.` | 没有企业版 | `research/openclaw/02_docs_openclaw_ai.md:20` |
| 7 | `not hostile multi-tenant isolation inside one shared Gateway` | 不是在同一个共享 Gateway 内部做敌意多租户隔离 | `research/openclaw/04_docs_openclaw_ai.md:10` |
| 8 | `The normal admission limit is 32 identities per logical session.` | 每个逻辑会话的默认准入上限是 32 个身份 | `research/openclaw/03_docs_openclaw_ai.md:126` |
| 9 | `**By default, the gateway denies all users who are not in an allowlist or paired via DM.**` | 默认情况下，网关拒绝所有不在白名单内、也未通过 DM 配对的用户 | `research/hermes/03_raw_githubusercontent_com_messaging-index.md:327` |
| 10 | `Every allowed user falls into one of two tiers per scope (DM vs group/channel):` | 每个被放行的用户在每个作用域里（私聊 vs 群组 / 频道）都落在两档之一： | — |
| 11 | `**What the tiers gate today:** slash commands. ... Plain chat is not affected — non-admins can still talk to the agent.` | 目前分级管的是什么：斜杠命令。……普通对话不受影响——非管理员仍然可以和 agent 说话 | — |
| 12 | `Sender routing selects a profile; it is not deny-by-default authorization.` | 发送者路由只是在挑 profile，不是默认拒绝式的授权 | `research/hermes/02_hermes-agent_nousresearch_com_multi-profile-gateways.md:645` |
| 13 | `Read access and agent use in chat are never gated.` | 读取权限与在对话中使用 agent 从不受分级限制 | — |

## 第 4 章 同层内部怎么分 —— OpenClaw「跑在你自己电脑上」对比 Hermes「不绑在你的笔记本上」

### 本章要解决的问题

在 OpenClaw 与 Hermes 之间，有没有一根能**直接回答「什么场景用哪个」**的差异轴？本章的答案是：有。两方在第 1 章的三层坐标里同属第 2 层（个人助手 harness），部署姿态——本机常驻，还是「不绑本机」——就是那根轴。本章不再重复第 2、3 章的术语与隔离比较，不展开 Octop（第 5 章），也不下最终结论（第 7 章）。

先说明前提：本章按前文的工作假设，把 OpenClaw 与 Hermes 当作**同层**处理；这个判断的正面证据（互相引用与互迁）在第 6 章，本章先用它，不重复论证。

### 4.1 同层之后，第一根能直接决策的轴

同层意味着这两方不该在功能清单上二选一——它们的「记忆」「技能」「常驻」在词面上高度重合。但同层不等于完全相同：总有一些轴能把它们真正分开，问题只是先找**最能直接回答场景问题**的那一根。

本章找到的是**部署姿态**，也就是「助手跑在哪台机器上」。它之所以排第一，是因为它的问题最具体：不是「谁的功能多」，而是「你的助手默认住在哪、默认能不能被外面的设备够到」。这个问题一答，很多场景自然分流。

为什么不是别的轴？记忆、技能、常驻这几条轴在两方之间的词面重合度太高——第 2 章讲的同词异指在这里同样成立，一拿它们当第一跳，立刻会退回功能清单。部署姿态不同：它的答案是一个**具体位置**，而位置会连带决定后面一连串默认行为——默认能不能被外网够到、记忆落在哪个盘、延伸出什么典型场景。它先分出「住在哪」，再谈「能力多不多」。

### 4.2 两句正面分野的原文

差异最好让原文自己说。OpenClaw 的自我描述第一句就是本机：

`OpenClaw 是一个跑在你自己电脑上的开源 AI 助手`（`research/openclaw/06_raw_githubusercontent_com.md:25`）

Hermes 的自我描述则明确把「本机」列为要摆脱的默认：

`把它跑在一台 5 美元的 VPS、一个 GPU 集群，或者空闲时几乎不花钱的 serverless 基础设施上——它不绑在你的笔记本上`（`research/hermes/01_raw_githubusercontent_com_README.md:26`）

一边是 `跑在你自己的电脑上`，一边是 `不绑在你的笔记本上`——这两句并排放，分野自己就出来了。OpenClaw 的架构落点也是本机形态：`一台主机一个 Gateway`（`research/openclaw/01_docs_openclaw_ai.md:14`）、`Gateway 默认绑定到 loopback`（`research/openclaw/05_docs_openclaw_ai.md:24`）。Hermes 的落点则是跨机器：网关是常驻进程，`消息网关是一个常驻进程，通过统一的架构把 Hermes 接到 20 多个外部消息平台上`（`research/hermes/gw/01_hermes-agent_nousresearch_com.md:9`）。

### 4.3 部署姿态对照表

| 维度 | OpenClaw | Hermes |
| --- | --- | --- |
| 产品主语 | 你自己电脑上的助手 | 跨机器常驻、不绑本机的助手 |
| 在哪跑 | `跑在你自己的电脑上`；`作为笔记本上的私人助手` | `$5 VPS` / GPU 集群 / serverless；`不绑在你的笔记本上` |
| 常驻形态 | 一主机一 Gateway，默认绑 loopback | 单进程接 20+ 平台；默认一 profile 一网关，可多路复用 |
| 记忆落盘 | 工作区里的 Markdown（默认 `~/.openclaw/workspace`） | `~/.hermes/memories/` 下的 MEMORY.md / USER.md（有字符上限） |
| 典型场景 | 与本地文件系统 / 桌面环境耦合 | 7×24 常驻、按需计费、多端接入 |

两条架构细节各自支撑这个姿态。OpenClaw 一侧：`一台主机一个 Gateway` 加上默认绑 loopback，意味着它默认是本机可达、外网不可达，要开放得走「认证入口」而不是公网绑定。Hermes 一侧：网关默认一个 profile 一个，但可以多路复用——`把 gateway.multiplex_profiles: true 打开后，一个进程就同时服务默认 profile 和 profiles/ 下每一个活跃目录`（`research/hermes/gw/01_hermes-agent_nousresearch_com.md:451`）。

记忆的落盘位置也随部署姿态走。OpenClaw 的记忆就是工作区里的普通 Markdown，`模型只记得被写进磁盘的东西，没有隐藏状态`（`research/openclaw/extra/02_docs_openclaw_ai.md:10`）；Hermes 的记忆默认存在 `~/.hermes/memories/`，并且有硬字符上限——MEMORY.md `2,200 字符（约 800 token）`、USER.md `1,375 字符（约 500 token）`，合计约 `约 1,300 token` 固定注入（`research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15,302`）。

> [!tip] 大白话
> 这一轴像问「你的管家住哪」。OpenClaw 的管家住在你家里，顺手就能翻你的书柜、用你的厨房，但要让外面的朋友找他，得先给他开个门。Hermes 的管家住在云上的一间小办公室，7×24 在岗、从任何地方都能联系，但他够不到你家书柜，除非你自己往里搬东西。

### 4.4 把部署姿态翻译成场景

「跑在哪」翻译成场景，就是两组不同的默认耦合：

- **本机常驻 → 与本地文件系统 / 桌面环境耦合的场景**。助手默认和你的机器在同一台，直接读写本地文件最顺；代价是默认不能被外网够到（绑 loopback），要远程访问得额外配认证入口。适合「助手主要替我处理这台机器上的东西」的用法。
- **VPS / serverless → 7×24 常驻、按需计费、多端接入的场景**。助手常驻在云上，你从任何消息通道都能找到它——`它在云上的 VM 里干活时，你可以从 Telegram 跟它说话`（`research/hermes/01_raw_githubusercontent_com_README.md:26`）；serverless 形态还能在空闲时不产生成本。适合「我随时随地在多个设备上找它」的用法。

选择因此不是「谁的功能强」，而是「你的助手默认应该和谁待在一起」：和你的本地文件待在一起，还是和你的消息通道、以及全天候在线待在一起。前者把「够得到本机」当成默认前提，后者把「随时联系得上」当成默认前提，两者优化的是不同的默认值。

### 4.5 相同面：这不是「谁更好」的比较

必须把两者的相同面写清楚，避免这一章被读成优劣比较。OpenClaw 与 Hermes 同为常驻 gateway 形态、同用本地文件里的 Markdown 做记忆、同以技能目录作为扩展点——这些是它们的**共同底色**。第 3 章也讲过，两者在隔离强度上都属于偏低档（OpenClaw 不提供隔离，Hermes 准入与很窄的分级）。

所以这一轴不回答「哪个更强」，只回答「哪个的默认姿态更贴你的场景」。这也正是第 1 章那句话的兑现：同层的两方，本来就不该在功能清单上分高下，只该在**与场景直接挂钩的那根轴**上分。

> [!warning] 时效说明
> 本章 OpenClaw 引用来自 2026-09-29 抓取件，Hermes 的本地抓取件为 2026-08-27、远程为 2026-09-29，两者内容一致、无冲突（`02_deep_research.md` §5 C8）。涉及「多用户」三义（同一信任域内的协作 / 准入与很窄的分级 / 行级归属）的判断，其时效以 2026-08-27 为准。

### 本章小结

- 在 OpenClaw 与 Hermes 之间，第一根能直接决策的轴是**部署姿态**（跑在哪）。
- 两句原文正面对冲：OpenClaw `跑在你自己的电脑上`；Hermes `不绑在你的笔记本上`。
- 本机常驻耦合本地文件系统与桌面环境，默认绑 loopback；VPS / serverless 对应 7×24 常驻、按需计费、多端接入。
- 记忆落盘位置随姿态走：OpenClaw 用工作区 Markdown，Hermes 用 `~/.hermes/memories/` 下的定长文件。
- 两者有共同底色（常驻 gateway + 本地文件记忆 + 技能目录扩展），本章不是「谁更好」的比较。

**下一章预告**：OpenClaw 与 Hermes 的二选一在这根轴上能走通。但 Octop 根本不在这个二选一里——第 5 章说明：Octop 的「多用户」（行级归属）不是第 3 章那根梯度轴上的更强档，而是**另一个问句的答案**。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `OpenClaw is an open-source AI assistant that runs on your own computer` | OpenClaw 是一个跑在你自己电脑上的开源 AI 助手 | `research/openclaw/06_raw_githubusercontent_com.md:25` |
| 2 | `Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly nothing when idle. It's not tied to your laptop` | 把它跑在一台 5 美元的 VPS、一个 GPU 集群，或者空闲时几乎不花钱的 serverless 基础设施上——它不绑在你的笔记本上 | `research/hermes/01_raw_githubusercontent_com_README.md:26` |
| 3 | `runs on your own computer` | 跑在你自己的电脑上 | `research/openclaw/01_docs_openclaw_ai.md:14` |
| 4 | `It's not tied to your laptop` | 不绑在你的笔记本上 | `research/openclaw/01_docs_openclaw_ai.md:14` |
| 5 | `One Gateway per host.` | 一台主机一个 Gateway | `research/openclaw/01_docs_openclaw_ai.md:14` |
| 6 | `The Gateway binds to loopback by default.` | Gateway 默认绑定到 loopback | `research/openclaw/05_docs_openclaw_ai.md:24` |
| 7 | `The messaging gateway is the long-running process that connects Hermes to 20+ external messaging platforms through a unified architecture.` | 消息网关是一个常驻进程，通过统一的架构把 Hermes 接到 20 多个外部消息平台上 | `research/hermes/gw/01_hermes-agent_nousresearch_com.md:9` |
| 8 | `as a personal assistant on a laptop` | 作为笔记本上的私人助手 | — |
| 9 | `not tied to your laptop` | 不绑在你的笔记本上 | — |
| 10 | `With gateway.multiplex_profiles: true one process serves the default profile plus every live directory under profiles/` | 把 gateway.multiplex_profiles: true 打开后，一个进程就同时服务默认 profile 和 profiles/ 下每一个活跃目录 | `research/hermes/gw/01_hermes-agent_nousresearch_com.md:451` |
| 11 | `The model only remembers what gets saved to disk; there is no hidden state.` | 模型只记得被写进磁盘的东西，没有隐藏状态 | `research/openclaw/extra/02_docs_openclaw_ai.md:10` |
| 12 | `2,200 chars (~800 tokens)` | 2,200 字符（约 800 token） | `research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15,302` |
| 13 | `1,375 chars (~500 tokens)` | 1,375 字符（约 500 token） | `research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15,302` |
| 14 | `~1,300 tokens` | 约 1,300 token | `research/hermes/05_hermes-agent_nousresearch_com_memory.md:14-15,302` |
| 15 | `talk to it from Telegram while it works on a cloud VM` | 它在云上的 VM 里干活时，你可以从 Telegram 跟它说话 | `research/hermes/01_raw_githubusercontent_com_README.md:26` |

## 第 5 章 Octop 回答的是不是另一个问题 —— 单实例多用户平台，家庭与小团队

### 本章要解决的问题

第 3 章把三方放在同一根隔离强度轴上，Octop 落在最强端（行级归属）。一个自然的追问随之出现：它是不是「同一个问题的更强答案」——把 OpenClaw 或 Hermes 那种个人助手，再加一档隔离，就是 Octop？

本章的回答是：不是。Octop 确实落在强端，但它问的与另两方**不是同一个问题**。OpenClaw 与 Hermes 问的是「一个人的助手跑在哪台机器上」，Octop 问的是「一台机器上的实例如何服务多个用户」。把它硬塞回「二选一」里比较，等于拿尺子去量温度——刻度是有的，但量的不是那回事。本章只定位它是什么：先换问句、再讲架构后果、再给硬边界，最后说明「个人助理」为什么只是它的退化形态。三方互相引用留到第 6 章，引入与否的建议留到第 7 章。

### 5.1 换一个问句：不是「哪台机器」，是「一台机器怎么服务多人」

分野最先出现在产品主语上。OpenClaw 与 Hermes 的主语是单数「你」，Octop 的主语是「一台机器上的实例」，收益归于「每个用户」：

- `支持多用户、多 Agent 的自托管 AI 助手 — 更聪明，更懂你。`（`research/octop/README_CN.md:6`）——引号内是官方 README 原句用词，不作改动；按第 2 章切分，此处的「多用户」是 ③ 行级归属这一层
- `Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）
- `同时为每个用户配备一组可按场景切换的专业 Agent。`（`research/octop/README_CN.md:70`）
- 面向 agent 的手册同调：`**Octop**：自托管 AI 助手平台（多用户、多 agent）`（`research/octop/AGENTS.md:37`）

所以它回答的问题可以写死成一句：**一台机器上的一个实例，怎么同时服务多个用户。**这句话在 OpenClaw 与 Hermes 的语境里根本不存在——两者的默认形态是「受信的单操作者助手」（`research/openclaw/02_docs_openclaw_ai.md`），③ 行级归属意义上的「多用户」在两者那里都是叠加上去的一层。Octop 反过来：「多用户」（③ 行级归属）是它的出发点，单用户才是要特判的少数情况。这一点下一节会展开。

> [!tip] 大白话
> 把 OpenClaw / Hermes 想成**你的私人笔记本**：问的是「你带哪台笔记本出门、它默认能不能被外面够到」。把 Octop 想成**家里的公用电脑**：它默认就是一台机器、好几个人用，问的是「这台电脑怎么让全家人各有各的账户和文件柜」。前者是「谁在哪」，后者是「一台怎么分给多个」。

### 5.2 官方 Scope 限定：家庭与小团队

Octop 没有把自己说成通用多租户平台，它的官方 Scope 是**家庭与小团队**：

- `Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）
- 家庭模型写得更直白：`**家庭共享** — 一个管理员账号，全家共用；按成员分配不同 Agent 与专家角色`（`research/octop/README_CN.md:76`）

也就是说，它的官方定位是「一个管理员 + 全家/小队共用」的模型，而不是「很多互不信任的组织共用一个 SaaS」。这条定位与第 3 章的强档并不矛盾：它是**单实例内**做行级归属，隔离强度高，但服务对象被限定在**一个信任圈层**里。规模口径因此也很清楚——家庭与小团队，不是「任意规模的租户池」。

### 5.3 架构是这份定位的直接后果：单进程

Octop 的架构不是「顺便长这样」，而是这份定位倒逼出来的。整套栈是**一个进程**：

- `整个技术栈就是一个进程：没有单独的 worker、没有外部队列，除了用户自己配置的 LLM 供应商之外不依赖任何外部服务`（`research/octop/docs/architecture.md:32`）
- `一切都跑在一个由 uvicorn 提供服务的 Python 进程里：没有外部队列（Redis、RabbitMQ、Celery），没有单独的 worker 进程，除了 LLM 供应商之外不需要任何后端服务`（`research/octop/docs/adr/001-single-process-model.md:14`）
- `Octop 不依赖外部消息队列或中间件，而是通过进程内的 HarnessProcessor 统一路由所有入口`（`research/octop/README_CN.md:107`）
- 重启语义：`单进程架构。重启后从控制面数据库重建状态（默认本地 SQLite；可选 PostgreSQL）。`（`research/octop/README_CN.md:483`）

为什么「服务多人」会推出一体式进程？因为一个实例要同时扛多项职责：`Octop 需要同时跑 web 服务、CLI、每个用户的 Agent 运行时、IM 通道连接和定时调度`（`research/octop/docs/adr/001-single-process-model.md:10`）。工程师的取舍是「运维负担优先于扩展」——`对目标人群来说，加一个 Redis 或进程守护会成倍增加运维负担`（`research/octop/docs/adr/001-single-process-model.md`）——目标人群（家庭与小团队）不需要集群，需要的是「一个进程、一个端口、装完就能用」。

控制面后端可选 SQLite 或 PostgreSQL：`| OCTOP_DATABASE_DRIVER | sqlite | postgresql | sqlite | Storage backend |`（`research/octop/docs/configuration.md:158`），但只有全新安装才能选 PG：`只支持全新安装——没有 SQLite→PG 的数据迁移工具`（`research/octop/docs/adr/002-database-backends.md:45`）。

> [!example] 部署形态清单
> Octop 官方给出的安装方式覆盖了几种典型自托管姿势：脚本安装 / PyPI / Docker / 桌面客户端（Wails）/ 飞牛 NAS 应用包 `Octop-fnos-docker-<version>.fpk`（见 `research/octop/README_CN.md` 快速开始）。桌面端只是 **Wails 外壳**，底层仍是同一套服务，并不存在独立的「单用户桌面模式」。

### 5.4 硬边界：一台机器，不给人数上限

这一节是本章最需要读者记住的部分：Octop 的收益与代价是**成对声明**的，不要只抄收益。ADR-001 直接把权衡列成表：

| 收益 | 代价 |
| --- | --- |
| 零外部依赖 | 只支持垂直扩展（一台机器） |
| 部署简单（一个进程、一个端口） | 重 CPU 任务会阻塞事件循环 |
| 本地开发快 | 不支持 worker 的横向扩展 |

（三行分别见 `research/octop/docs/adr/001-single-process-model.md:27-29`。）

翻成人话：它**没有外部队列、没有独立 worker、只能垂直扩展**——也就是「换更强的机器」而不是「加更多的机器」。重 CPU 任务会阻塞事件循环；数据库也是单写者定位：`同一时刻只有一个 Octop 写入者；不承诺多实例写入`（`research/octop/docs/adr/002-database-backends.md:44`）。官方甚至预告了未来的扩展缝在哪：`将来要横向扩展，得把 worker 拆成独立进程并加一个队列`（`research/octop/docs/adr/001-single-process-model.md`）——注意用的是**将来时**，说明这还不是现状。

> [!warning] 不要给 Octop 编造人数上限
> 官方**没有发布任何并发用户数、吞吐或压测数字**，只有 `只支持垂直扩展`、`不支持 worker 的横向扩展`、`同一时刻每个 agent 只有一个写入者` 这类定性表述（`02_deep_research.md` §3.3 裁决 2、§8 开放问题 1）。所以本章只给「一台机器垂直扩展」这一条**硬边界**，**不给任何人数上限**。任何「支持 N 个用户」的说法都是杜撰。

> [!example] 官方 Roadmap 里的未完成项
> 更能说明「水平扩展还不是现状」的，是 Octop 自己列在 Roadmap 上的未完成项：`- [ ] **Managed Agents** — 平台托管的 Agent 生命周期（开通、伸缩与运维），无需自行维护完整自托管栈。`，以及同段的 `- [ ] **云边端一体** — 本地运行 Octop，同时可将选定任务调度到云端执行`（`research/octop/README_CN.md:172`）。两条都还打着未勾选的方框——「伸缩」「云端调度」是官方承认要做、但**当前没有**的能力。选型时按现状读，不要按 Roadmap 读。

### 5.5 「个人助理」是退化形态，不是另一个产品模式

既然 Octop 的主语是「一台机器服务多人」，那它还支不支持「就我一个人用」？支持——而且这正是它的退化形态（一个用户的一份记录），而不是另起一个产品：

- `**个人助理** — 让专属 Agent 帮你写周报、整理资料、定日程，记忆随工作区长期保留。`（`research/octop/README_CN.md:75`）

关键在于理解「退化」二字：单用户在 Octop 里就是**用户表里的一行**，走的是同一套 JWT、归属、模块权限——不是把「多用户」（③ 行级归属）那层能力关掉换一套单用户内核。所以它不像「个人助手 harness」，更像是「本来给多人用的平台，恰好只放了一个人」。这也解释了为什么第 1 章的三层坐标里，Octop 该归到第 3 层（多用户平台，此处「多用户」= ③ 行级归属），而不是第 2 层。

### 5.6 记忆：独立库，落工作区，随工作区迁移

Octop 的记忆是**独立子系统**（octop-memory），分层加全文检索，落在 agent 工作区里，随工作区一起迁移：

- `**Octop Memory** — 分层记忆与全文检索，让 Agent 的记忆随工作区一同迁移。`（`research/octop/README_CN.md:104`）
- 默认落盘：`控制面用 SQLite 时，agent 记忆留在 {workspace}/memory.sqlite`（`research/octop/docs/configuration.md:187`）

记忆落点：`控制面用 PostgreSQL 时，agent 记忆**默认复用同一个 DSN**`，schema 名为 `agent_<id>`（`research/octop/docs/configuration.md:189`）。这里藏着两条迁移限制，选型时要留意：官方明确 `没有 SQLite→PG 的记忆数据自动迁移`（`research/octop/docs/configuration.md:200`），且记忆表结构由 octop-memory 自己拥有（`research/octop/docs/architecture.md:115`）。

记忆的**归身边界还延伸到运维动作**，这一点和「行级归属」一脉相承：`对话的 --all 与本地管理 CLI 范围不同：只选当前用户自己的 agent，不包含其他用户或共享 agent。`（`research/octop/docs/memory-slim.md:87`）。另有两条当前限制：瘦身整理只支持 SQLite（`PG 瘦身，只支持 SQLite`，`research/octop/docs/memory-slim.md:57`），外部 IM 的记忆维护尚未开放（`外部 IM 的记忆维护需要已验证的发送者权限，暂未开放。`，`research/octop/README_CN.md:422`）。

### 本章小结

- Octop 不是隔离梯度上的「更强档」，而是**另一个问句的答案**：一台机器上的实例如何服务多个用户。
- 官方 Scope 限定为**家庭与小团队**（一个管理员 + 全家/小队共用），服务对象是一个信任圈层。
- 架构是这份定位的直接后果：**全栈单进程**，无外部队列、无独立 worker。
- 硬边界成对声明：零外部依赖 ↔ 只能垂直扩展；简单部署 ↔ 重任务阻塞事件循环；本地开发快 ↔ 无水平 worker 扩展。**官方无容量数据，不给人数上限。**
- 「个人助理」是单用户**退化形态**（用户表里一行），不是独立的单用户产品模式。
- 记忆是独立库（octop-memory），落工作区、随工作区迁移；SQLite→PG 无自动迁移、瘦身只支持 SQLite。

**下一章预告**：本章说 Octop 是「另一个问句的答案」。这个说法能不能被独立证据检验？第 6 章换一个角度看三方——**谁把谁当参照**：迁移命令、OpenClaw 的官方逐项对照页、以及 Octop 的双向零提及，会把前面第 2–5 章的结论反向校验一遍。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Octop is a self-hosted AI assistant platform for households and small teams.` | Octop 是一个面向家庭与小团队的自托管 AI 助手平台 | `research/octop/README.md:69` |
| 2 | `**Octop** — self-hosted AI assistant platform (multi-user, multi-agent).` | **Octop**：自托管 AI 助手平台（多用户、多 agent） | `research/octop/AGENTS.md:37` |
| 3 | `Default OpenClaw is a trusted single-operator assistant.` | 默认的 OpenClaw 是一个受信的单操作者助手 | `research/openclaw/02_docs_openclaw_ai.md` |
| 4 | `The whole stack is one process. There is no separate worker, no external queue, no required external services beyond whatever LLM provider the user configures.` | 整个技术栈就是一个进程：没有单独的 worker、没有外部队列，除了用户自己配置的 LLM 供应商之外不依赖任何外部服务 | `research/octop/docs/architecture.md:32` |
| 5 | `Everything runs in a single Python process served by uvicorn. There is no external queue (Redis, RabbitMQ, Celery), no separate worker process, and no required backing services beyond the LLM provider.` | 一切都跑在一个由 uvicorn 提供服务的 Python 进程里：没有外部队列（Redis、RabbitMQ、Celery），没有单独的 worker 进程，除了 LLM 供应商之外不需要任何后端服务 | `research/octop/docs/adr/001-single-process-model.md:14` |
| 6 | `Octop needs to run a web server, a CLI, per-user Agent runtimes, IM channel connections, and cron schedulers simultaneously.` | Octop 需要同时跑 web 服务、CLI、每个用户的 Agent 运行时、IM 通道连接和定时调度 | `research/octop/docs/adr/001-single-process-model.md:10` |
| 7 | `Adding Redis or a process supervisor doubles the ops burden for the primary audience.` | 对目标人群来说，加一个 Redis 或进程守护会成倍增加运维负担 | `research/octop/docs/adr/001-single-process-model.md` |
| 8 | `- Greenfield only — no SQLite→PG data migrator.` | 只支持全新安装——没有 SQLite→PG 的数据迁移工具 | `research/octop/docs/adr/002-database-backends.md:45` |
| 9 | `- Single active Octop writer; no multi-instance write promise.` | 同一时刻只有一个 Octop 写入者；不承诺多实例写入 | `research/octop/docs/adr/002-database-backends.md:44` |
| 10 | `Future scale-out would require extracting the worker into a separate process and adding a queue` | 将来要横向扩展，得把 worker 拆成独立进程并加一个队列 | `research/octop/docs/adr/001-single-process-model.md` |
| 11 | `Vertical scaling only` | 只支持垂直扩展 | `02_deep_research.md` |
| 12 | `No horizontal worker scaling` | 不支持 worker 的横向扩展 | `02_deep_research.md` |
| 13 | `one writer per agent at a time` | 同一时刻每个 agent 只有一个写入者 | `02_deep_research.md` |
| 14 | `- Control plane SQLite → agent memory stays {workspace}/memory.sqlite` | 控制面用 SQLite 时，agent 记忆留在 {workspace}/memory.sqlite | `research/octop/docs/configuration.md:187` |
| 15 | `Control plane PostgreSQL → agent memory **defaults to the same DSN**` | 控制面用 PostgreSQL 时，agent 记忆**默认复用同一个 DSN** | `research/octop/docs/configuration.md:189` |
| 16 | `no automatic SQLite→PG memory data migration.` | 没有 SQLite→PG 的记忆数据自动迁移 | `research/octop/docs/configuration.md:200` |
| 17 | `Agent memory DDL is owned by octop-memory.` | 记忆表的 DDL 由 octop-memory 自己拥有 | `research/octop/docs/architecture.md:115` |

## 第 6 章 「谁把谁当参照」—— 迁移命令、官方对照页、双向零提及说明什么

### 本章要解决的问题

前几章从机制和定位推出一个判断：OpenClaw 与 Hermes 同层，Octop 是另一个问句的答案。这个判断能不能被独立检验？本章提供一次**可证伪的反向校验**：如果它是对的，证据应该出现在三方**互相引用**的地方——因为一个产品把谁写进文档、为谁做迁移工具、和谁互相检索得到零，比它的功能表更能说明它把自己当成谁的同类。

本章只做校验：不重述第 3、4 章的机制比较，不展开 Octop 的定位（第 5 章已做），也不给选型建议（第 7 章）。判据先立清楚，再逐方看证据，最后合起来读。

### 6.1 判据：不看功能清单，看「谁把谁当参照」

功能清单会撞车（第 1 章的叠影），所以这里换一个方向问：**它把谁当参照物？**问题具体化成三件事，件件可检索、可执行：

- 它的文档**点名**了谁？（全文 grep 即可）
- 它为谁做了**迁移工具**？（迁移命令是可执行代码，不是宣传语）
- 它对谁**零提及**？（零命中同样是证据）

这三件事都比功能表硬：文档能 grep，命令能跑，零命中能复现。一个把对手写进「逐项对照」的产品，等于承认对方是自己要回答的同一类问题；一个对谁都不提、只对另一类工具做集成委派的产品，则是在说「我不在这一桌」。

### 6.2 OpenClaw 侧：有官方对照专页，README 却零提及

OpenClaw 对 Hermes 的引用是全篇最重的一处——有**官方专页级对照**：

- `反复被拿来对照的对象是 Hermes Agent（原文此处带一个指向对方仓库的链接）`（`research/openclaw/02_docs_openclaw_ai.md:17`）
- `那张逐项对照专页压缩了与 Hermes 的、经来源逐条核实的差异（原文此处带一个指向该专页的链接）`（`research/openclaw/02_docs_openclaw_ai.md:43`）

但同一份材料的 README 全文对 `hermes` 与 `octop` 的提及次数**均为 0**（`research/openclaw/06_raw_githubusercontent_com.md`、`research/openclaw/05_docs_openclaw_ai.md`）。门面（README）零提及、文档站却有专页——两条都真，**并列记录，不合并**：README 是入口门面，docs 站才是深度文档，深度不一致本身就是信息。

顺带补上第 3 章留给本章的那个细节：OpenClaw 并不是「不做多租户」，而是**不在一个 Gateway 内做**——它用 `openclaw fleet` 把每个租户放进独立的实例（cell），每个 cell 有自己的 Gateway、状态、凭据、通道账号和容器，文档直接给规则：`每个租户信任边界用一个 cell；不要把共享的一个 Gateway 当作敌意多租户边界`（`research/openclaw/extra2/02_docs_openclaw_ai.md:11`）。这条路自己也承认还不成熟：`租户意味着一个租户一个 gateway cell，而 fleet 目前仍是实验性的`（`research/openclaw/02_docs_openclaw_ai.md:65`）。而信任边界并不因分 cell 而改变——`Fleet 操作者与主机被所有租户所信任；抵抗被攻破的主机不是目标`（`research/openclaw/04_docs_openclaw_ai.md:23`），以及 `这条阶梯上的任何一级都不改变 OpenClaw 的应用信任模型：一个 Gateway 始终是一个受信操作者域`（同文件 :33）。一句话翻译：**它把「互不信任」的问题从进程内挪到了进程外**，而不是在进程内造隔离。

引用这张对照表时必须先说清它的性质。专页自己就写明它不是中立评测：

`下面这张对照表反映的是 6defe7eb6c 这个提交（复核于 2026 年 8 月 27 日）时的来源，它既不是实时的对抗性测试，也不构成对每一次部署的保证`（`research/openclaw/extra2/01_docs_openclaw_ai.md:8`）

> [!warning] 引用规则
> 这张对照表是 **OpenClaw 单方制作，不是中立评测**。它在 `治理` 与 `资金与营收` 两行把自身写成 `独立 501(c)(3)，靠捐赠资助`，把 Hermes 写成 `风险投资（Paradigm 领投的 A 轮）`——一行对照里就带着立场，不能当作客观横向测评来引。同时它引用的对方公司背景 `Hermes 由 Nous Research 打造，一家接受风险投资的公司`（`research/openclaw/02_docs_openclaw_ai.md`）也是**站在 OpenClaw 立场**转述的。

这张逐项对照表本次落盘件含 15 行属性（`research/openclaw/extra2/01_docs_openclaw_ai.md:17-31`），其中 `角色与多用户` 行对 Hermes 的判定是 `在某个适配器的授权集合内是同等信任`，对自身多租户工具则标为 `实验性的每租户 fleet cell`。注意：这两句都出自 OpenClaw 单方，转述时仍要带上这个标注。

### 6.3 Hermes 侧：迁移命令是双向同层的铁证

如果 OpenClaw 只是「单方面把 Hermes 当对手」，那还可能是蹭热度。Hermes 侧的证据把方向补全了——它为 OpenClaw 用户做了**可执行的迁移工具**：

- README 有专节：`从 OpenClaw 迁移`，正文 `如果你是从 OpenClaw 过来的，Hermes 可以自动导入你的设置、记忆、技能和 API 密钥`（`research/hermes/01_raw_githubusercontent_com_README.md`）
- `**首次安装时：**安装向导（hermes setup）会自动检测 ~/.openclaw，并在配置开始前询问是否迁移`
- 命令是 `hermes claw migrate`；源码兼容**三代**目录名：`_OPENCLAW_DIR_NAMES = (".openclaw", ".clawdbot", ".moltbot")`（`research/hermes/src/claw.py:29`）
- 迁移脚本共 **36 个具名迁移项**，覆盖 MCP 服务器 / 定时任务 / 钩子 / Gateway / 会话 / 审批规则（`research/hermes/src/openclaw_to_hermes.py:40-190`）

迁移内容清单（README）：`SOUL.md` / `记忆`（MEMORY.md + USER.md）/ `技能`（迁往 `~/.hermes/skills/openclaw-imports/`）/ `命令白名单` / `消息设置` / `API 密钥` / `TTS 素材` / `工作区指令`。安全姿态也值得记一笔：`密钥默认不迁：即使加了 --preset full，也必须显式给出 --migrate-secrets`（`research/hermes/src/claw.py:33-34`）。

为什么这是「铁证」而不只是「一处宣传」？因为它同时满足三条：README 与源码**三处交叉一致**；它是**可执行代码**而非形容词；兼容三个历史目录名说明这是长期维护的迁移路径。这正是第 4 章那个「同层」工作假设所需要的正面证据——本章在此**兑现**它。引用本仓库既有章节（如 `workspace/hermes-agent/chapters/*`）里的说法时，须标为**本仓库二次加工**，不是官方口径。

### 6.4 Octop 侧：双向零提及，参照物不在这一桌

Octop 在这张参照网上是完全缺席的：全库检索 `openclaw|hermes` **零命中**（README / README_CN / AGENTS.md / docs / plugins）。它不提它们，它们也不提它。

那 Octop 把谁当参照？答案在它的集成文档里——**命名的外部 agent 工具只有 ACP runner，内置 7 个**：`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi`（`research/octop/docs/acp.md:29-38`）。方向定义写得很清楚，这是**出站委派**，不是竞品对照：`| **Outbound** | OpenCode, CodeBuddy, … | Octop (acp_runner tool) | Octop agent delegates coding tasks |`（`research/octop/docs/acp.md:8`）。

把这一节回指第 1 章的三层坐标：Octop 的邻近参照物落在**第 1 层**（本地 CLI 阵营），而且关系是**集成**（把编码任务委派出去），不是「我要和它比功能」。

> [!warning] 一句必须标注为推断的话
> 把这 7 个 runner 逐个归入「本地 CLI 阵营」**属本文的推断**——官方**没有使用**「本地 CLI 阵营」这个分类词。可核对的是「Octop 命名的外部 agent 工具是这 7 个、方向是出站委派」；层归属是本文的归类动作，不得写成官方口径。

### 6.5 三张证据合起来说明什么

| 平台 | 是否提及另两方 | 形式 | 方向 | 层级标注 |
| --- | --- | --- | --- | --- |
| OpenClaw | 提及 Hermes；不提 Octop | 官方逐项 source-verified 对照专页 | 单向（OpenClaw 写 Hermes） | README 零提及、docs 有专页，并列；专页为 **OpenClaw 单方制作** |
| Hermes | 提及 OpenClaw；不提 Octop | `hermes claw migrate`（README + 源码三处一致，36 项） | 单向且可执行（自 OpenClaw 迁入） | 可执行代码，非宣传语 |
| Octop | 双方零提及 | 唯一命名的外部 agent 工具是 ACP runner（内置 7 个） | 无 | 7 个归入本地 CLI 阵营属**推断** |

三条合起来读：OpenClaw 与 Hermes **互相**出现在对方的参照系里——一方写了对照专页，另一方写了迁移工具，方向不同但都指向同一个「同层」。Octop 则双向零提及，它的参照物是第 1 层的编码类 CLI，且是集成关系。这**互证**了第 2–5 章的判断：OpenClaw 与 Hermes 是同一张牌桌上的两家，Octop 回答的是另一桌的问题。

> [!tip] 大白话
> 看两个人是不是同行，别比名片上的头衔，看他们**在文章里点谁的名、给谁做搬家服务**。OpenClaw 专门写了「我和 Hermes 的区别」，Hermes 专门做了「从 OpenClaw 搬家」的工具——这俩显然在互相盯着。Octop 则谁都不提，它推荐的是给「本地命令行工具」派活——它压根坐的是另一桌。

### 本章小结

- 判据：同层与否不看功能，看**互相引用与互迁**——可 grep、可执行、可复现。
- OpenClaw 有官方逐项对照专页（15 行属性），但 README 零提及；门面与文档深度不一致，**并列记录不合并**。引用时必须标注「**OpenClaw 单方制作，非中立评测**」。
- Hermes 有 `hermes claw migrate`：README 与源码三处交叉一致、36 个具名迁移项、密钥默认不迁——**双向同层的铁证**，第 4 章的「同层」工作假设在此兑现。
- Octop 双向零提及；唯一命名的外部 agent 工具是 ACP runner 内置 7 个，方向是**出站委派**，邻近参照物落在第 1 层。归入「本地 CLI 阵营」**属推断**。
- 三张证据互证：OpenClaw 与 Hermes 同层，Octop 是另一个问句的答案。

**下一章预告**：定位、术语、隔离、部署姿态、参照关系——六个维度看完了，该怎么用？第 7 章把它们收成一个**决策树**和一个**可迁移的提问清单**，并针对「个人助手」与「企业多人」两类真实场景给出可解释的结论。

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `The recurring comparison is [Hermes Agent]` | 反复被拿来对照的对象是 Hermes Agent（原文此处带一个指向对方仓库的链接） | `research/openclaw/02_docs_openclaw_ai.md:17` |
| 2 | `The [comparison table](...) condenses the source-verified contrast with Hermes.` | 那张逐项对照专页压缩了与 Hermes 的、经来源逐条核实的差异（原文此处带一个指向该专页的链接） | `research/openclaw/02_docs_openclaw_ai.md:43` |
| 3 | `Use one cell for each tenant trust boundary; do not use one shared Gateway as a hostile multi-tenant boundary.` | 每个租户信任边界用一个 cell；不要把共享的一个 Gateway 当作敌意多租户边界 | `research/openclaw/extra2/02_docs_openclaw_ai.md:11` |
| 4 | `Tenancy means one gateway cell per tenant, and fleet is still experimental.` | 租户意味着一个租户一个 gateway cell，而 fleet 目前仍是实验性的 | `research/openclaw/02_docs_openclaw_ai.md:65` |
| 5 | `The Fleet operator and the host are trusted by every tenant. Resistance to a compromised host is a non-goal.` | Fleet 操作者与主机被所有租户所信任；抵抗被攻破的主机不是目标 | `research/openclaw/04_docs_openclaw_ai.md:23` |
| 6 | `No rung in this ladder changes the OpenClaw application trust model: one Gateway remains one trusted operator domain.` | 这条阶梯上的任何一级都不改变 OpenClaw 的应用信任模型：一个 Gateway 始终是一个受信操作者域 | `research/openclaw/04_docs_openclaw_ai.md:23` |
| 7 | `The comparison below reflects source at 6defe7eb6c (reviewed August 27, 2026), not a live adversarial test or a guarantee about every deployment.` | 下面这张对照表反映的是 6defe7eb6c 这个提交（复核于 2026 年 8 月 27 日）时的来源，它既不是实时的对抗性测试，也不构成对每一次部署的保证 | `research/openclaw/extra2/01_docs_openclaw_ai.md:8` |
| 8 | `Governance` | 治理 | `research/openclaw/02_docs_openclaw_ai.md` |
| 9 | `Funding and revenue` | 资金与营收 | `research/openclaw/02_docs_openclaw_ai.md` |
| 10 | `Independent 501(c)(3) funded by donations` | 独立 501(c)(3)，靠捐赠资助 | `research/openclaw/02_docs_openclaw_ai.md` |
| 11 | `Venture-funded (Paradigm-led Series A)` | 风险投资（Paradigm 领投的 A 轮） | `research/openclaw/02_docs_openclaw_ai.md` |
| 12 | `Hermes is built by Nous Research, a venture-funded company` | Hermes 由 Nous Research 打造，一家接受风险投资的公司 | `research/openclaw/02_docs_openclaw_ai.md` |
| 13 | `Roles and multi-user` | 角色与多用户 | `research/openclaw/extra2/01_docs_openclaw_ai.md:17-31` |
| 14 | `Equal trust within an adapter's authorized set` | 在某个适配器的授权集合内是同等信任 | `research/openclaw/extra2/01_docs_openclaw_ai.md:17-31` |
| 15 | `experimental per-tenant fleet cells` | 实验性的每租户 fleet cell | `research/openclaw/extra2/01_docs_openclaw_ai.md:17-31` |
| 16 | `## Migrating from OpenClaw` | 从 OpenClaw 迁移 | `research/hermes/01_raw_githubusercontent_com_README.md` |
| 17 | `If you're coming from OpenClaw, Hermes can automatically import your settings, memories, skills, and API keys.` | 如果你是从 OpenClaw 过来的，Hermes 可以自动导入你的设置、记忆、技能和 API 密钥 | `research/hermes/01_raw_githubusercontent_com_README.md` |
| 18 | `**During first-time setup:** The setup wizard (hermes setup) automatically detects ~/.openclaw and offers to migrate before configuration begins.` | **首次安装时：**安装向导（hermes setup）会自动检测 ~/.openclaw，并在配置开始前询问是否迁移 | — |
| 19 | `Memories` | 记忆 | — |
| 20 | `Skills` | 技能 | — |
| 21 | `Command allowlist` | 命令白名单 | — |
| 22 | `Messaging settings` | 消息设置 | — |
| 23 | `API keys` | API 密钥 | — |
| 24 | `TTS assets` | TTS 素材 | — |
| 25 | `Workspace instructions` | 工作区指令 | — |
| 26 | `Secrets are never included implicitly: --migrate-secrets is required even under --preset full` | 密钥默认不迁：即使加了 --preset full，也必须显式给出 --migrate-secrets | — |

## 第 7 章 选型框架 + 落到你场景的决策树（个人助手 / 企业多人）

### 本章要解决的问题

前六章把「感觉都一样」的选型困惑拆开了——但拆开不是目的。本章要把它们收成一个**可复用、可迁移**的选型框架，并针对两类真实场景（**个人助手**、**企业多人**）给出可执行的决策路径；下次冒出一个新的自托管 agent，读者也能用同一套框架把它自行归位。

本章不引入前六章没论证过的新事实，不推荐具体部署方案，**不给 Octop 的容量承诺**，也不展开第 1 层（本地 CLI 阵营）。

### 7.1 决策树的根节点：先归位到层

整棵决策树只有一条主干规则：**先归位到层，再谈层内。**这一条直接复用第 1 章的三层坐标，判据就是第 1 章那两问——**是不是常驻服务**，以及**服务的用户数是单数还是复数**。

为什么根节点必须是「层」，而不是「功能」？因为第 1 章已经证明：层与层之间，功能清单会叠影——同一句「多用户」在不同层里根本不是一件事（第 2 章）。拿功能表当根节点，第一步就会滑回「感觉都一样」。所以层是先决条件，不是选项之一。

> [!tip] 大白话
> 这棵树的第一刀不是「你要什么功能」，而是「你到底进哪个门」。像找餐厅：先分清你要路边快餐、社区食堂，还是能摆宴席的酒店——不同门类的菜单本来就没法直接比。门进错了，后面比得再细也白搭。

### 7.2 第 1 层分支：本文不展开

如果归位结果是**第 1 层（本地 CLI 阵营）**——随用随起、不常驻、用户是单人——本文到此为止，不展开。原因很直接：本文六章都在回答「**常驻服务形态**内部怎么选」（个人助手 harness 与多用户平台），而第 1 层不是常驻服务，前提就不成立。

不展开不等于没有方法，只给一个方向：第 1 层内部的选型比的是另一组东西——**与本地终端 / 文件系统的耦合度、模型接入方式、能不能被脚本化编排**。它的相邻参照物正是第 6 章里 Octop 那 7 个 ACP runner（`opencode` / `codebuddy` / `claude_code` / `codex` / `kimi_code` / `cursor_cli` / `pi`）。记得带上第 6 章的标注：把这 7 个归入「本地 CLI 阵营」**是本文的推断**，官方未使用该分类词。

### 7.3 第 2 层分支：同层内部按部署姿态分（回第 4 章）

归位到**第 2 层（个人助手 harness）**，意味着你已经确定：要常驻服务，且用户是单人 / 单一所有者。此时第 4 章那根轴立刻可用——**部署姿态**：

- 要助手**本机常驻**、与本地文件系统和桌面环境耦合（`跑在你自己的电脑上`）→ 走 **OpenClaw** 分支。
- 要助手**不绑本机**、7×24 常驻、多端接入、按需计费（`不绑在你的笔记本上`）→ 走 **Hermes** 分支。

正如第 4 章强调的：这不是「谁更好」，而是「你的助手默认该和谁待在一起」。

### 7.4 第 3 层分支：先说清你要哪种「多用户」（回第 2、3 章）

归位到**第 3 层（多用户平台）**之后，选平台之前必须先回答一个前置问题：**你说的「多用户」是哪一层语义？**这一问回指第 2 章的三义与第 3 章的梯度：

- 你要的是**同一信任域内的协作**（几个人互相信得过，只是不想互相顶替）→ OpenClaw 档够用。硬边界：协作 guardrails **不是安全边界**；要真正跨信任域，只能「一租户一实例」（fleet，且官方自标 experimental）。
- 你要的是**单机单所有者的准入与很窄的分级** → Hermes 档。硬边界：分级目前只覆盖斜杠命令，普通对话不受影响。
- 你要的是**数据级隔离**（按行归属、越权在数据层被拒）→ **Octop**（行级归属）。

走到 Octop 这一支，第 5 章的三条硬边界必须一起读：**单进程、只垂直扩展（一台机器）、无水平 worker 扩展**；官方 Scope 限定**家庭与小团队**；且**官方没有任何人数上限数据**。所以这一支**不能**承诺「支持 N 个用户」。

> [!warning] 别把「多用户平台」读成「多租户平台」
> 这是第 2 章的硬结论。三者里只有 OpenClaw 有租户词汇（且带 experimental 标注）；Hermes 与 Octop 各有一处 `tenant` 都是消息路由字段，不得读成租户模型。第 3 层回答的是「一台机器如何服务多个用户」，不是「多个互不信任的组织共用一个 SaaS」。

### 7.5 四轴 + 压力剖面：一个可迁移的选型框架

把前六章的比较维度收成一张表。前三轴能直接指出平台站位，第四轴是对任何平台都适用的提问透镜：

| 轴 | 提问 | 回指 | OpenClaw | Hermes | Octop |
| --- | --- | --- | --- | --- | --- |
| 术语轴 | 它说的「多用户」是哪一层语义？ | 第 2 章 | 同一信任域内的协作 | 准入与很窄的分级 | 行级归属 |
| 隔离强度轴 | 越权被拒得有多硬？ | 第 3 章 | 不提供隔离 | 准入与很窄的分级 | 行级归属 |
| 层内差异轴 | 助手跑在哪台机器？ | 第 4 章 | `跑在你自己的电脑上` | `不绑在你的笔记本上` | 单机单进程平台 |
| 框架轴（提问透镜） | 你的压力压在哪一环？ | 第 1 章 | 对三方同样适用 | 对三方同样适用 | 对三方同样适用 |

第四轴的用法是把任务当**压力剖面**问，而不是当应用标签——`任务不只是一个应用标签，而是施加在观察、上下文、控制、行动、状态与治理之上的一个压力剖面`（`research/framework/13_arxiv_2606.20683v1_fulltext.md:212`）。翻成六问：**观察接口 / 上下文管理 / 控制循环 / 动作接口 / 状态与产物 / 验证与治理**——哪一环压力最大，就往那一环强的平台上靠。

这四轴之外还有一条**校验轴**：**它把谁当参照物**（第 6 章）。它不给平台打分，只做反向校验——如果前面的归位判断是对的，一个产品的参照关系应该与它的层吻合。OpenClaw 与 Hermes 互引互迁（同层），Octop 双向零提及、参照物落在第 1 层——与第 2–5 章的判断一致。

### 7.6 落到你的两类场景

把框架落到读者手上（`00_intent.md` 的使用场景表）：

| 你的场景 | 该走哪条分支 | 现用工具是否需要变 |
| --- | --- | --- |
| **个人助手**（现用 Hermes；也用于一部分企业工作） | 常驻 + 单数用户 → 第 2 层 → 第 4 章部署姿态 → 不绑本机 / 7×24 多端 → **Hermes** | 不变：Hermes 已在这条分支上 |
| **通用助手、先试的那一个**（现用 OpenClaw，与 Hermes 用途重叠） | 第 2 层 → 需本机耦合 / 本地文件 → **OpenClaw**；需 7×24 多端 → 转 **Hermes** | 取决于**部署姿态**，不取决于功能多少 |
| **企业多人**（尚未引入；Octop 是候选新选项） | 第 3 层 → 先问「同一信任域协作，还是要跨租户隔离」 | 需真正隔离时：OpenClaw 档**不是安全边界**；Octop 档限**家庭与小团队**、**无人数上限数据** |

一句话读法：OpenClaw 与 Hermes 之间的取舍由**部署姿态**决定，不靠功能对比；是否引入 Octop 由**你要不要数据级隔离、且能否接受单机垂直扩展**决定，不靠「是不是多用户」。

### 7.7 换一个新 agent 时的提问清单

下次遇到一个陌生的自托管 agent，按这个顺序问，就能自己把它归位（每问都回指前面的论证）：

1. **它常驻吗？服务的用户是单数还是复数？**（三层坐标，第 1 章）→ 先定层。
2. **它说的「多用户 / 多租户」是哪一层语义？**（术语轴，第 2 章）→ 加限定语再说。
3. **它把越权拒得有多硬？**（隔离强度轴，第 3 章）→ 定位到梯度哪一档。
4. **它默认跑在哪台机器上？**（层内差异轴，第 4 章）→ 同层内分流。
5. **它把谁当参照物？**（参照轴，第 6 章）→ 看它自己承认的同类是谁。
6. **你的压力剖面压在哪一环？**（观察 / 上下文 / 控制 / 动作 / 状态 / 验证与治理，第 1 章）→ 找那一环强的。

### 本章小结

- 决策树的根节点是**层**：先归位，再谈层内（第 1 章三层坐标）。
- 第 1 层不展开，只指向层内选型方法；第 2 层按**部署姿态**分 OpenClaw / Hermes（第 4 章）；第 3 层先问是哪种**「多用户」**（第 2、3、5 章）。
- 选型框架 = 三条比较轴（术语 / 隔离强度 / 层内差异）+ 一条提问透镜（压力剖面），另加一条校验轴（参照关系，第 6 章）。
- 落到场景：个人助手在两方之间按部署姿态选；企业多人先分清「协作」还是「隔离」——记住硬结论 **多用户平台 ≠ 多租户平台**。

#### 后续观察点（本文的开放问题，留待将来复核）

1. **Octop 的并发容量**：官方只给 `只支持垂直扩展`、`不支持 worker 的横向扩展` 这类定性表述，**没有任何人数上限数据**。将来若官方发布容量说明，本篇第 5、7 章的硬边界需据以更新。
2. **针对「多用户」的治理能力之版本边界**：RBAC（`0.9.24`）与按用户配额（`0.9.33`）确为增量加入，但「多用户」本身是否在 1.0 之前即存在**未验证**。拿旧版本对照时，第 3 章的分档描述可能对不上。
3. **归属表的完整清单**：目前只确认 `agents.user_id` 一个字段；`knowledge_bases` / `usage_log` / `audit_log` 只是间接证据，未逐表核对。清单补齐后，第 3 章「行级归属」的边界可写得更精确。

---

### 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。同一句话在本章出现多次只列一行；「出处」沿用正文该处标注的出处，正文该处没标出处的记 `—`。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `runs on your own computer` | 跑在你自己的电脑上 | — |
| 2 | `It's not tied to your laptop` | 不绑在你的笔记本上 | — |
| 3 | `a task is not merely an application label but a pressure profile over observation, context, control, action, state, and governance` | 任务不只是一个应用标签，而是施加在观察、上下文、控制、行动、状态与治理之上的一个压力剖面 | `research/framework/13_arxiv_2606.20683v1_fulltext.md:212` |
| 4 | `Vertical scaling only` | 只支持垂直扩展 | — |
| 5 | `No horizontal worker scaling` | 不支持 worker 的横向扩展 | — |

## 相关文档

- [[../openclaw/OpenClaw MOC]] - OpenClaw 学习索引
- [[../openclaw/选型层/OpenClaw与国内仿制品对比]] - 同一产品线内的另一类选型比较
- [[../../Hermes Agent/Hermes Agent MOC]] - Hermes Agent 学习索引
- [[../../00-索引/AI学习 MOC]] - AI 学习总索引
