# 第 5 章 Octop 回答的是不是另一个问题 —— 单实例多用户平台，家庭与小团队

## 本章要解决的问题

第 3 章把三方放在同一根隔离强度轴上，Octop 落在最强端（行级归属）。一个自然的追问随之出现：它是不是「同一个问题的更强答案」——把 OpenClaw 或 Hermes 那种个人助手，再加一档隔离，就是 Octop？

本章的回答是：不是。Octop 确实落在强端，但它问的与另两方**不是同一个问题**。OpenClaw 与 Hermes 问的是「一个人的助手跑在哪台机器上」，Octop 问的是「一台机器上的实例如何服务多个用户」。把它硬塞回「二选一」里比较，等于拿尺子去量温度——刻度是有的，但量的不是那回事。本章只定位它是什么：先换问句、再讲架构后果、再给硬边界，最后说明「个人助理」为什么只是它的退化形态。三方互相引用留到第 6 章，引入与否的建议留到第 7 章。

## 5.1 换一个问句：不是「哪台机器」，是「一台机器怎么服务多人」

分野最先出现在产品主语上。OpenClaw 与 Hermes 的主语是单数「你」，Octop 的主语是「一台机器上的实例」，收益归于「每个用户」：

- `支持多用户、多 Agent 的自托管 AI 助手 — 更聪明，更懂你。`（`research/octop/README_CN.md:6`）——引号内是官方 README 原句用词，不作改动；按第 2 章切分，此处的「多用户」是 ③ 行级归属这一层
- `Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）
- `同时为每个用户配备一组可按场景切换的专业 Agent。`（`research/octop/README_CN.md:70`）
- 面向 agent 的手册同调：`**Octop**：自托管 AI 助手平台（多用户、多 agent）`（`research/octop/AGENTS.md:37`）

所以它回答的问题可以写死成一句：**一台机器上的一个实例，怎么同时服务多个用户。**这句话在 OpenClaw 与 Hermes 的语境里根本不存在——两者的默认形态是「受信的单操作者助手」（`默认的 OpenClaw 是一个受信的单操作者助手`，`research/openclaw/02_docs_openclaw_ai.md`），③ 行级归属意义上的「多用户」在两者那里都是叠加上去的一层。Octop 反过来：「多用户」（③ 行级归属）是它的出发点，单用户才是要特判的少数情况。这一点下一节会展开。

> [!tip] 大白话
> 把 OpenClaw / Hermes 想成**你的私人笔记本**：问的是「你带哪台笔记本出门、它默认能不能被外面够到」。把 Octop 想成**家里的公用电脑**：它默认就是一台机器、好几个人用，问的是「这台电脑怎么让全家人各有各的账户和文件柜」。前者是「谁在哪」，后者是「一台怎么分给多个」。

## 5.2 官方 Scope 限定：家庭与小团队

Octop 没有把自己说成通用多租户平台，它的官方 Scope 是**家庭与小团队**：

- `Octop 是一个面向家庭与小团队的自托管 AI 助手平台`（`research/octop/README.md:69`）
- 家庭模型写得更直白：`**家庭共享** — 一个管理员账号，全家共用；按成员分配不同 Agent 与专家角色`（`research/octop/README_CN.md:76`）

也就是说，它的官方定位是「一个管理员 + 全家/小队共用」的模型，而不是「很多互不信任的组织共用一个 SaaS」。这条定位与第 3 章的强档并不矛盾：它是**单实例内**做行级归属，隔离强度高，但服务对象被限定在**一个信任圈层**里。规模口径因此也很清楚——家庭与小团队，不是「任意规模的租户池」。

## 5.3 架构是这份定位的直接后果：单进程

Octop 的架构不是「顺便长这样」，而是这份定位倒逼出来的。整套栈是**一个进程**：

- `整个技术栈就是一个进程：没有单独的 worker、没有外部队列，除了用户自己配置的 LLM 供应商之外不依赖任何外部服务`（`research/octop/docs/architecture.md:32`）
- `一切都跑在一个由 uvicorn 提供服务的 Python 进程里：没有外部队列（Redis、RabbitMQ、Celery），没有单独的 worker 进程，除了 LLM 供应商之外不需要任何后端服务`（`research/octop/docs/adr/001-single-process-model.md:14`）
- `Octop 不依赖外部消息队列或中间件，而是通过进程内的 HarnessProcessor 统一路由所有入口`（`research/octop/README_CN.md:107`）
- 重启语义：`单进程架构。重启后从控制面数据库重建状态（默认本地 SQLite；可选 PostgreSQL）。`（`research/octop/README_CN.md:483`）

为什么「服务多人」会推出一体式进程？因为一个实例要同时扛 web 服务、CLI、每个用户的 agent 运行时、IM 通道连接和定时调度：`Octop 需要同时跑 web 服务、CLI、每个用户的 Agent 运行时、IM 通道连接和定时调度`（`research/octop/docs/adr/001-single-process-model.md:10`）。工程师的取舍是「运维负担优先于扩展」——`对目标人群来说，加一个 Redis 或进程守护会成倍增加运维负担`（`research/octop/docs/adr/001-single-process-model.md`）——目标人群（家庭与小团队）不需要集群，需要的是「一个进程、一个端口、装完就能用」。

控制面后端可选 SQLite 或 PostgreSQL：`| OCTOP_DATABASE_DRIVER | sqlite | postgresql | sqlite | Storage backend |`（`research/octop/docs/configuration.md:158`），但只有全新安装才能选 PG：`「只支持全新安装——没有 SQLite→PG 的数据迁移工具」`（`research/octop/docs/adr/002-database-backends.md:45`）。

> [!example] 部署形态清单
> Octop 官方给出的安装方式覆盖了几种典型自托管姿势：脚本安装 / PyPI / Docker / 桌面客户端（Wails）/ 飞牛 NAS 应用包 `Octop-fnos-docker-<version>.fpk`（见 `research/octop/README_CN.md` 快速开始）。桌面端只是 **Wails 外壳**，底层仍是同一套服务，并不存在独立的「单用户桌面模式」。

## 5.4 硬边界：一台机器，不给人数上限

这一节是本章最需要读者记住的部分：Octop 的收益与代价是**成对声明**的，不要只抄收益。ADR-001 直接把权衡列成表：

| 收益 | 代价 |
| --- | --- |
| 零外部依赖 | 只支持垂直扩展（一台机器） |
| 部署简单（一个进程、一个端口） | 重 CPU 任务会阻塞事件循环 |
| 本地开发快 | 不支持 worker 的横向扩展 |

（三行分别见 `research/octop/docs/adr/001-single-process-model.md:27-29`。）

翻成人话：它**没有外部队列、没有独立 worker、只能垂直扩展**——也就是「换更强的机器」而不是「加更多的机器」。重 CPU 任务会阻塞事件循环；数据库也是单写者定位：`「同一时刻只有一个 Octop 写入者；不承诺多实例写入」`（`research/octop/docs/adr/002-database-backends.md:44`）。官方甚至预告了未来的扩展缝在哪：`将来要横向扩展，得把 worker 拆成独立进程并加一个队列`（`research/octop/docs/adr/001-single-process-model.md`）——注意用的是**将来时**，说明这还不是现状。

> [!warning] 不要给 Octop 编造人数上限
> 官方**没有发布任何并发用户数、吞吐或压测数字**，只有 `「只支持垂直扩展」`、`「不支持 worker 的横向扩展」`、`「同一时刻每个 agent 只有一个写入者」` 这类定性表述（`02_deep_research.md` §3.3 裁决 2、§8 开放问题 1）。所以本章只给「一台机器垂直扩展」这一条**硬边界**，**不给任何人数上限**。任何「支持 N 个用户」的说法都是杜撰。

> [!example] 官方 Roadmap 里的未完成项
> 更能说明「水平扩展还不是现状」的，是 Octop 自己列在 Roadmap 上的未完成项：`- [ ] **Managed Agents** — 平台托管的 Agent 生命周期（开通、伸缩与运维），无需自行维护完整自托管栈。`，以及同段的 `- [ ] **云边端一体** — 本地运行 Octop，同时可将选定任务调度到云端执行`（`research/octop/README_CN.md:172`）。两条都还打着未勾选的方框——「伸缩」「云端调度」是官方承认要做、但**当前没有**的能力。选型时按现状读，不要按 Roadmap 读。

## 5.5 「个人助理」是退化形态，不是另一个产品模式

既然 Octop 的主语是「一台机器服务多人」，那它还支不支持「就我一个人用」？支持——而且这正是它的退化形态（一个用户的一份记录），而不是另起一个产品：

- `**个人助理** — 让专属 Agent 帮你写周报、整理资料、定日程，记忆随工作区长期保留。`（`research/octop/README_CN.md:75`）

关键在于理解「退化」二字：单用户在 Octop 里就是**用户表里的一行**，走的是同一套 JWT、归属、模块权限——不是把「多用户」（③ 行级归属）那层能力关掉换一套单用户内核。所以它不像「个人助手 harness」，更像是「本来给多人用的平台，恰好只放了一个人」。这也解释了为什么第 1 章的三层坐标里，Octop 该归到第 3 层（多用户平台，此处「多用户」= ③ 行级归属），而不是第 2 层。

## 5.6 记忆：独立库，落工作区，随工作区迁移

Octop 的记忆是**独立子系统**（octop-memory），分层加全文检索，落在 agent 工作区里，随工作区一起迁移：

- `**Octop Memory** — 分层记忆与全文检索，让 Agent 的记忆随工作区一同迁移。`（`research/octop/README_CN.md:104`）
- 默认落盘：`控制面用 SQLite 时，agent 记忆留在 {workspace}/memory.sqlite`（`research/octop/docs/configuration.md:187`）

换到 PostgreSQL 时，记忆默认复用同一个 DSN、按 agent 分 schema：`控制面用 PostgreSQL 时，agent 记忆**默认复用同一个 DSN**`，schema 名为 `agent_<id>`（`research/octop/docs/configuration.md:189`）。这里藏着两条迁移限制，选型时要留意：官方明确 `「没有 SQLite→PG 的记忆数据自动迁移」`（`research/octop/docs/configuration.md:200`），且记忆表结构由 octop-memory 自己拥有（`「记忆表的 DDL 由 octop-memory 自己拥有」`，`research/octop/docs/architecture.md:115`）。

记忆的**归身边界还延伸到运维动作**，这一点和「行级归属」一脉相承：`对话的 --all 与本地管理 CLI 范围不同：只选当前用户自己的 agent，不包含其他用户或共享 agent。`（`research/octop/docs/memory-slim.md:87`）。另有两条当前限制：瘦身整理只支持 SQLite（`PG 瘦身，只支持 SQLite`，`research/octop/docs/memory-slim.md:57`），外部 IM 的记忆维护尚未开放（`外部 IM 的记忆维护需要已验证的发送者权限，暂未开放。`，`research/octop/README_CN.md:422`）。

## 本章小结

- Octop 不是隔离梯度上的「更强档」，而是**另一个问句的答案**：一台机器上的实例如何服务多个用户。
- 官方 Scope 限定为**家庭与小团队**（一个管理员 + 全家/小队共用），服务对象是一个信任圈层。
- 架构是这份定位的直接后果：**全栈单进程**，无外部队列、无独立 worker。
- 硬边界成对声明：零外部依赖 ↔ 只能垂直扩展；简单部署 ↔ 重任务阻塞事件循环；本地开发快 ↔ 无水平 worker 扩展。**官方无容量数据，不给人数上限。**
- 「个人助理」是单用户**退化形态**（用户表里一行），不是独立的单用户产品模式。
- 记忆是独立库（octop-memory），落工作区、随工作区迁移；SQLite→PG 无自动迁移、瘦身只支持 SQLite。

**下一章预告**：本章说 Octop 是「另一个问句的答案」。这个说法能不能被独立证据检验？第 6 章换一个角度看三方——**谁把谁当参照**：迁移命令、OpenClaw 的官方逐项对照页、以及 Octop 的双向零提及，会把前面第 2–5 章的结论反向校验一遍。

## 引文对照（原文 / 中译）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处与正文同源。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Octop is a self-hosted AI assistant platform for households and small teams.` | Octop 是一个面向家庭与小团队的自托管 AI 助手平台 | `research/octop/README.md:69` |
| 2 | `**Octop** — self-hosted AI assistant platform (multi-user, multi-agent).` | **Octop**：自托管 AI 助手平台（多用户、多 agent） | `research/octop/AGENTS.md:37` |
| 3 | `Default OpenClaw is a trusted single-operator assistant.` | 默认的 OpenClaw 是一个受信的单操作者助手 | `research/openclaw/02_docs_openclaw_ai.md` |
| 4 | `Octop is a self-hosted AI assistant platform for households and small teams.` | Octop 是一个面向家庭与小团队的自托管 AI 助手平台 | `research/octop/README.md:69` |
| 5 | `The whole stack is one process. There is no separate worker, no external queue, no required external services beyond whatever LLM provider the user configures.` | 整个技术栈就是一个进程：没有单独的 worker、没有外部队列，除了用户自己配置的 LLM 供应商之外不依赖任何外部服务 | `research/octop/docs/architecture.md:32` |
| 6 | `Everything runs in a single Python process served by uvicorn. There is no external queue (Redis, RabbitMQ, Celery), no separate worker process, and no required backing services beyond the LLM provider.` | 一切都跑在一个由 uvicorn 提供服务的 Python 进程里：没有外部队列（Redis、RabbitMQ、Celery），没有单独的 worker 进程，除了 LLM 供应商之外不需要任何后端服务 | `research/octop/docs/adr/001-single-process-model.md:14` |
| 7 | `Octop needs to run a web server, a CLI, per-user Agent runtimes, IM channel connections, and cron schedulers simultaneously.` | Octop 需要同时跑 web 服务、CLI、每个用户的 Agent 运行时、IM 通道连接和定时调度 | `research/octop/docs/adr/001-single-process-model.md:10` |
| 8 | `Adding Redis or a process supervisor doubles the ops burden for the primary audience.` | 对目标人群来说，加一个 Redis 或进程守护会成倍增加运维负担 | `research/octop/docs/adr/001-single-process-model.md` |
| 9 | `- Greenfield only — no SQLite→PG data migrator.` | 「只支持全新安装——没有 SQLite→PG 的数据迁移工具」 | `research/octop/docs/adr/002-database-backends.md:45` |
| 10 | `- Single active Octop writer; no multi-instance write promise.` | 「同一时刻只有一个 Octop 写入者；不承诺多实例写入」 | `research/octop/docs/adr/002-database-backends.md:44` |
| 11 | `Future scale-out would require extracting the worker into a separate process and adding a queue` | 将来要横向扩展，得把 worker 拆成独立进程并加一个队列 | `research/octop/docs/adr/001-single-process-model.md` |
| 12 | `Vertical scaling only` | 「只支持垂直扩展」 | `02_deep_research.md` |
| 13 | `No horizontal worker scaling` | 「不支持 worker 的横向扩展」 | `02_deep_research.md` |
| 14 | `one writer per agent at a time` | 「同一时刻每个 agent 只有一个写入者」 | `02_deep_research.md` |
| 15 | `- Control plane SQLite → agent memory stays {workspace}/memory.sqlite` | 控制面用 SQLite 时，agent 记忆留在 {workspace}/memory.sqlite | `research/octop/docs/configuration.md:187` |
| 16 | `Control plane PostgreSQL → agent memory **defaults to the same DSN**` | 控制面用 PostgreSQL 时，agent 记忆**默认复用同一个 DSN** | `research/octop/docs/configuration.md:189` |
| 17 | `no automatic SQLite→PG memory data migration.` | 「没有 SQLite→PG 的记忆数据自动迁移」 | `research/octop/docs/configuration.md:200` |
| 18 | `Agent memory DDL is owned by octop-memory.` | 「记忆表的 DDL 由 octop-memory 自己拥有」 | `research/octop/docs/architecture.md:115` |
