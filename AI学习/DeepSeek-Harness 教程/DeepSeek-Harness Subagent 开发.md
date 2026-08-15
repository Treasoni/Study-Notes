---
title: "DeepSeek-Harness Subagent 开发——如何写 subagent（从能力缝到 provider）"
tags: [deepseek-harness, ai, agent, subagent, 教程, 开发]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
---


> [!info] 笔记信息
> - **系列归属**：DeepSeek-Harness 教程系列 · 新分册
> - **笔记类型**：概念理解 + 实战（上手）
> - **读者画像**：熟悉 Claude Code 扩展体系、已读 dsh 插件开发五章的「有了解」用户
> - **预计篇幅**：约 26-32 页（中长篇分册）
> - **版本锚点**：developer preview（2026-08-13 锚点）
> - **本文件**：`AI学习/DeepSeek-Harness 教程/DeepSeek-Harness Subagent 开发.md`（已发布）
> - **系列入口**：[[DeepSeek-Harness 教程/README|系列导览]] · [[DeepSeek-Harness MOC|教程 MOC]]

## 学习路径摘要

> 摘要取自系列大纲，先定位「我在哪、要去哪」。

### 前置要求

- 熟悉 Claude Code 扩展体系：`.claude/agents/*.md`、subagent 调用心智、工具定义
- 已读完 DeepSeek-Harness 插件开发五章：cordis 插件结构、`ctx.tools` / `defineTool`、`dsh plugin add`、`cordis.patch.yml`
- 能读 TypeScript 接口 / 泛型 / 可选方法签名（`SubagentProvider` 契约是类型收窄驱动的）

### 学完能做什么

- 说清 dsh subagent 的「能力缝 + 三层结构」心智模型，并迁移 Claude Code 的 subagent 心智
- 按需选择并挂载现成 provider（spawn / fork / acp / dsh-sdk），用 `dsh-tool-subagent` 暴露给模型
- 独立写一个最小 provider 插件，用 `ctx.subagents.registerProvider` 注册并挂进 cordis 插件树
- 理解 one-shot / continuable 生命周期与委派深度限制，避开 `UNSUPPORTED_CAPABILITY`、无默认导出等已知坑
- 给后续分册留好接口（codex / claude-code provider 配置、跨进程 continuable 社区方案）

### 建议学习顺序

- 顺序通读第 1-4 章（心智 → 契约 → 现成 provider → 写自己的 provider），这是主路径
- 第 5 章生命周期对只想快速上手的读者可先跳读，写 provider 遇到 `prepareContinuable` 或配置 backgroundMode 时再回来补
- 第 6 章工具化在动手「把 provider 给模型用」时精读；第 7 章速查在写作与排错时当索引用
- 预估时间：通读约 2-3 小时；动手写第一个 provider 另加 1-2 小时（含对照源码核实 6.1）
- 每章读完建议做一次「与 Claude Code 对照」的迁移笔记，沉淀进个人 Obsidian

> [!note] 诚实标注约定（贯穿全文，不得删除）
> 本系列对三类「信心等级」做显式标注：**综合推断**（官方无直接文档，由 S2 契约 + S4 方法论拼合，发布前须对照源码核实）、**未证实**（仅社区二手说法，不展开）、**未抓取**（本分册未收集，标注可扩展）。各章相关标注原样保留，第 7 章 7.3 集中收口。

## 目录

1. [第一章 subagent 心智模型——能力缝与三层结构](#第一章-subagent-心智模型能力缝与三层结构)
2. [第二章 核心契约——`ctx.subagents` 注册表与 `SubagentProvider` 接口](#第二章-核心契约ctxsubagents-注册表与-subagentprovider-接口)
3. [第三章 现成 provider 家族——选用、挂载、跑起来](#第三章-现成-provider-家族选用挂载跑起来)
4. [第四章 写自己的 provider——三段式与最小实现](#第四章-写自己的-provider三段式与最小实现)
5. [第五章 生命周期深度——one-shot / continuable 与委派深度](#第五章-生命周期深度one-shot-continuable-与委派深度)
6. [第六章 工具化——把 provider 暴露成模型可调能力](#第六章-工具化把-provider-暴露成模型可调能力)
7. [第七章 速查与避坑清单](#第七章-速查与避坑清单)

---

## 第一章 subagent 心智模型——能力缝与三层结构

> [!summary] 导读
> 在 Claude Code 里，「subagent」的心智是：往 `.claude/agents/` 丢一个 `.md` 角色文件，模型就能把它当工具调用。这套心智带到 DeepSeek-Harness（dsh）会立刻撞墙——dsh 里根本不存在「一个 subagent 插件」。本章先把 dsh 的全景心智模型立起来：为什么 subagent 是一个「能力缝」而不是单一插件，这条缝背后是哪三层结构，以及为什么这么拆能换来「换执行后端只改一行配置」。读完你会得到一张能套用到后面所有章节的地图，也能立刻看懂 dsh 的 subagent 生态为什么是「六个 provider 兄弟 + 一个工具」，而不是「一个插件」。

### 1.1 为什么 subagent 是「能力缝」而不是单一插件

先放下 Claude Code 的「角色文件」心智，换一个问法：dsh 的核心 agent 循环需要一种能力——「把一个任务委托给另一个 agent 去跑」。这个「委托」能力在 dsh 里被设计成一个**能力缝（seam）**，而不是一个具体插件。[^c1-S1][^c1-S2]

什么叫能力缝？它是一段**定义好的边界**：核心循环只知道「这里有口子，往里插实现，按约定返回结果」，但不知道也不关心插进来的是谁。dsh 里跟它同类的能力缝还有 bash——bash 也是一个可选能力缝，宿主不自己实现终端，只声明「有 bash 这个口子」。

> [!tip] 大白话
> 把能力缝想成墙上的标准电源插座：插座定义了「电从哪来、插头长什么样、怎么接」的约定，但它不关心插进来的是手机充电器还是电风扇。所以……subagent 在 dsh 里是一个「约定好的接缝」，不是某个具体的插件——你往里插谁是后面配置的事。

subagent 这条缝和 bash 有一个关键差异：**bash 只允许挂一个执行器，subagent 允许多个 provider 并存、按名注册**。[^c1-S1][^c1-S2] 在同一个上下文里，`spawn`、`fork`、`acp`、`dsh-sdk` 可以同时注册，谁被调用取决于配置里写的 provider 名字，而不是「一次只能装一个 subagent 插件」。这个注册表模式是 dsh 仿照它自己的 **LLM 适配器注册表**做的——同一个模型接口可以挂多家实现、按名取用，subagent 的 `ctx.subagents` 就是这套模式的复制。[^c1-S1]

一句话记法：**subagent 不是一个插件，而是一条允许多家实现的委托缝。**

### 1.2 三层结构：定义 → 提供 → 消费

扩展 Cookbook 把这条能力缝映射成两个机制：`ctx.subagents` provider 注册表 + `dsh-tool-subagent` 工具。[^c1-S10] 展开来看是清晰的三层结构：

```text
┌──────────────────────────────────────────────────────────────┐
│ ① Service Definition —— dsh-subagent（ctx.subagents）        │
│    provider 注册表 + 请求/结果契约 + 持久描述符               │
│    + continuable-child 编排（定义「subagent 是什么」）        │
├──────────────────────────────────────────────────────────────┤
│ ② Service Provider —— 六个兄弟，真正干活的执行后端           │
│    spawn / fork / acp / codex / claude-code / dsh-sdk        │
│    （同名包，互不依赖、可替换）                              │
├──────────────────────────────────────────────────────────────┤
│ ③ Consumer / Tool —— 把 provider 暴露给模型                  │
│    dsh-tool-subagent（委托）+ -control（全局控制）            │
│    + -report（child→parent 反向汇报）                        │
└──────────────────────────────────────────────────────────────┘
```

- **① Service Definition（定义层）**：`dsh-subagent` 核心包，向 `ctx.subagents` 注册表提供整套契约——provider 怎么注册、请求（Request）带哪些字段、结果（Result）长什么样、可恢复子代理怎么编排。它定义「subagent 是什么」，自己不干活。[^c1-S3]
- **② Service Provider（提供层）**：`spawn` / `fork` / `acp` / `codex` / `claude-code` / `dsh-sdk` 六个兄弟，各自实现同一个契约。真正执行委托的是它们——`spawn` 在进程内新建一个 child，`acp` 起一个独立子进程用 ACP 协议驱动，`dsh-sdk` 起一个完整 peer harness。怎么选、怎么配是第 3 章的事，这里先记住「六个都是同一个口子的实现」。其中 `codex` / `claude-code` 是外部 CLI 后端，本分册只列名不展开配置。
- **③ Consumer / Tool（消费层）**：`dsh-tool-subagent` 把**某一个** provider 包成模型可见的工具；`-control` 提供 `send_message` / `interrupt_agent` / `list_agents` 全局控制；`-report` 打通 child 向 parent 汇报的方向。[^c1-S7][^c1-S9]

> [!tip] 大白话
> 把三层想成一家餐厅：菜单（Service Definition）定义「这道菜是什么、配料有哪些」；后厨（Service Provider）负责真正把菜做出来——换一个后厨团队，菜单不用改；服务员（Consumer/Tool）把菜端到顾客面前。所以……模型（顾客）只跟服务员（工具）打交道，点菜时根本不用知道后厨是 spawn 还是 acp。

数据流方向值得顺手记住：**模型 → 工具（③）→ 注册表/契约（①）→ provider（②）→ 真正的 child**。第 2 章会在这个方向上逐层展开细节。

### 1.3 provider 与 consumer 互不依赖：只依赖定义包

三层结构里最反直觉的一条设计主张来自 S4：**provider 与 consumer 互不依赖，只依赖定义包**。[^c1-S4]

- `dsh-tool-subagent` 不知道也不关心背后跑的是 `spawn` 还是 `acp`——它只面向 ① 的契约编程。
- `spawn` 这个 provider 也不知道自己被哪个工具消费——它只实现 ① 的契约。
- 两者之间唯一的共同引用是 ① 定义包。

这个「只依赖定义包」的约束带来最实用的收益：**换实现只改一行配置**。想从 `acp` 换到 `spawn`，把 `cordis.patch.yml` 里那行 `config: { provider: acp }` 改成 `provider: spawn`，定义包和工具一行都不用动（配置语法详见 [[DeepSeek-Harness 配置体系]]）。[^c1-S4]

> [!tip] 大白话
> 把「只依赖定义包」想成 USB-C 充电线：你的手机（consumer）只认 USB-C 这个接口标准，不认充电头是哪个牌子（provider）。所以……今天用 A 家充电头、明天换 B 家，只要都是 USB-C，线都不用换。dsh 里那个「USB-C 标准」就是定义包，「充电头」就是 provider。

对照 Claude Code 更能看出差别：Claude Code 的 subagent 执行器是**内置的唯一实现**，你想换执行后端等于换产品；dsh 把「执行后端」降级成了配置里的一个字符串。

### 1.4 微内核主张：核心循环固定，一切能力是扩展点上的监听者

能力缝不是孤立的特例，它背后是 dsh 整个扩展体系的中心主张。扩展 Cookbook 说得最直白：[^c1-S10]

> *"Every product feature maps to a listener on a documented extension point — the microkernel claim made checkable."* 且 *"No row modifies the loop."*

拆开看两条：

1. **一切产品特性都是「已文档化扩展点上的一个监听者」**。bash、fs、web、subagent、todo……dsh 内置的 `dsh-tool-*` 家族全是这么长的。[^c1-S10] 没有任何特性是「改核心」得来的。
2. **没有任何一行（插件代码）修改核心循环**。核心的 agent 循环（读消息 → 调工具 → 产消息）是固定的、插件不可碰的。你写的所有东西——包括 subagent provider——都只能挂在扩展点上当监听者，不能改主循环本身。

subagent 正是「在一条固定循环上叠加委派能力」的实例：核心循环不新增「委派」这个动作，`ctx.subagents` 只是一个扩展点，provider 注册上去、工具暴露出来，循环本身一行没改。[^c1-S10]

> [!tip] 大白话
> 把核心循环想成高铁主干线：发车、到站、报站的调度逻辑是固定的；加一条支线（subagent 能力）只是「在某个站台接出一条匝道」，主干线的时刻表一行都不用动。所以……你写 provider 不是在改高铁调度，而是在主干线的一个站点上挂了一条新支线——这也是为什么你必须守契约，因为主线不迁就支线。

对写插件的人，这条主张的实际含义是：**不要试图 hack 核心，只在你被允许的扩展点上工作**。第 4 章写 provider 时会看到，所有「能力」都是通过声明式字段（`capabilities`）挂在扩展点上的，而不是靠改循环。

### 1.5 三段式原则：完整能力本身才是接缝

「能力缝」听起来像是一种结构，但 S4 给了一个更狠的收窄：**完整能力本身才是接缝，单一角色不是。**[^c1-S4]

> *"The complete capability is its seam. No individual role is a seam."*

意思是：`provider` 单独拿出来**不构成**能力缝。一条缝必须三段齐全——定义（契约）+ provider（实现）+ consumer（消费面）——合在一起才算「一个完整能力」，才有资格被叫做接缝。只写一个 provider 实现，却没有定义包和工具，那只是一段孤儿代码，模型够不到它。这套三段式写法和 [[DeepSeek-Harness 插件开发核心]] 里的 cordis 插件结构同源，但多了一个「角色必须拆全」的要求。

配套的还有一条命名律，本系列后面会反复用到（第 4 章详细落地）：[^c1-S4]

| 角色 | 包名模式 | subagent 家族实例 |
| --- | --- | --- |
| ① Service Definition | `dsh-<cap>` | `dsh-subagent` |
| ② Provider | `<cap>-local`（本地实现） | `dsh-subagent-spawn-in-process` / `-fork` / `-acp` / `-dsh-sdk` |
| ③ Consumer/Tool | `dsh-tool-<cap>` | `dsh-tool-subagent` |

subagent 系列全部遵守这条律：定义是 `dsh-subagent`，工具是 `dsh-tool-subagent`，各 provider 是 `dsh-subagent-<实现>`。[^c1-S4]

> [!tip] 大白话
> 把「完整能力才是接缝」想成一次完整的搬家服务：光有一个搬家公司（provider）不算「搬家」；搬家公司 + 价目表/合同（定义）+ 客服下单渠道（工具）合起来，才是一个顾客能用的「搬家服务」。所以……只写 provider 等于只有搬家公司没有下单渠道，模型这个「顾客」根本叫不到你——三段缺一不可。

这一节为第 4 章埋下主方法论的种子：写一个 dsh 能力，就是按 ①②③ 三段把三件套补齐。

### 1.6 本章悬念与诚实标注

这一章是概念铺垫，不涉及具体代码坑，但有两件事要提前打好标记：

1. **悬念预告：`inheritsParentContext` 与「继承」直觉相反**。字面上它像「子代理继承父上下文」，但官方定位是**描述性标注**——它只说明「是否把父对话种子注入 child」（fork 为 true，spawn/acp 为 false），**不暗示工具/服务/权限的继承**。[^c1-S2] 这个「名不副实」的 flag 会在第 2 章讲契约时展开，现在先在心里挂个问号。
2. **developer preview（2026-08-13 锚点）生态尚未稳定**。整个 dsh subagent 生态锚定在 2026-08-13 的 developer preview 上：包名、配置、契约都可能破坏性变更。本系列每章末放「更新记录」，成稿时若发现与你读到的版本对不上，先查更新记录与官方 release notes。

### 本章小结

- subagent 在 dsh 里是「能力缝」不是单一插件：与 bash 同类，但允许多个 provider 并存、按名注册，仿照 LLM 适配器注册表。
- 三层结构 = ① 定义（`dsh-subagent` / `ctx.subagents`）→ ② 提供（spawn/fork/acp/codex/claude-code/dsh-sdk 六兄弟）→ ③ 消费（`dsh-tool-subagent` 家族）。
- provider 与 consumer 互不依赖、只依赖定义包 → 换执行后端只改一行配置。
- 微内核主张：核心循环固定，一切能力是扩展点上的监听者（"No row modifies the loop"）。
- 三段式原则：完整能力才是接缝，单一角色不是；命名律 `dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>` 是后续章节的地图。
- 埋了两个标记：`inheritsParentContext` 名不副实（第 2 章展开）；生态处于 developer preview，变更要查更新记录。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 声明方式 | `.claude/agents/*.md` 一个角色文件 | 注册表 + provider + 工具三段式三件套 |
| 执行后端 | 内置唯一实现，不可换 | 六个 provider 可替换，配置一行切换 |
| 心智单元 | 「写一个 md 文件 = 一个 subagent」 | 「定义 + 实现 + 消费 = 一个完整能力缝」 |
| 扩展边界 | 角色文件是入口 | 完整能力（三件套）才是入口，单一角色不是 |

迁移心智：在 Claude Code 里，「做一个 subagent」的心智是写一个角色 md 文件；到 dsh 要换成「补一个能力缝」——你写的不是「一个文件」，而是把「定义 / 实现 / 消费」三段补齐，让这条缝能挂到固定的核心循环上。Claude Code 的「角色声明」对应 dsh 的「Provider 契约声明」，但 dsh 多出定义包与工具两个必填角色——Claude Code 帮你隐掉的这两段，恰恰是 dsh 换执行后端只改一行配置的前提。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档撰写。subagent 能力缝、三层结构、微内核主张、三段式原则均引自官方子系统文档与扩展 Cookbook；若后续 preview 更新改变「能力缝 / 三层」表述，本章 1.1-1.5 是受影响区域，优先对照检查。

---

[^c1-S1]: S1 · Subagent 子系统设计文档（EN）— `docs/subsystems/subagent.md`（dsh 源码仓库，检索 2026-08-16）。能力缝定位、与 bash 并列、注册表仿照 LLM 适配器注册表。
[^c1-S2]: S2 · Subagent 子系统设计文档（中文）— `docs/subsystems/subagent.zh.md`（检索 2026-08-16）。同上契约与坑清单，`inheritsParentContext` 描述性标注出处。
[^c1-S3]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README — `packages/subagent/subagent/README.md`。定义层定位段（注册表 / 契约 / 持久描述符 / continuable 编排）。
[^c1-S4]: S4 · Three-role capability design（开发者实践教程）— `docs/user/develop/practice/index.md`。「完整能力才是接缝」「互不依赖只依赖定义包」与命名律。
[^c1-S7]: S7 · `dsh-tool-subagent` README — `packages/subagent/tool-subagent/README.md`。消费层委托工具定位。
[^c1-S9]: S9 · `tool-subagent-control` / `-report` README — `packages/subagent/tool-subagent-control/README.md`。control / report 定位。
[^c1-S10]: S10 · 扩展 Cookbook — `docs/cookbook/extension-cookbook.md`。feature→mechanism 映射、微内核主张（"No row modifies the loop"）。

---

> 第 1 章的地图已经铺好——subagent 是一条「能力缝」，三层结构各司其职。下一站落到接口层，看这条缝的「总机」`ctx.subagents` 和 provider 要兑现的契约。

## 第二章 核心契约——`ctx.subagents` 注册表与 `SubagentProvider` 接口

> [!summary] 导读
> 第 1 章立了全景心智：subagent 是一条能力缝，三层结构各司其职。这一章下钻到「缝」的接口层，把三个问题讲透：调用方怎么通过 `ctx.subagents` 找到并调用 provider？一个 provider 要兑现哪些契约字段？一次委托请求带哪些选项、结果怎么解读？读完你会看懂 `ctx.subagents` 的注册与查询、`SubagentProvider` 每个字段的含义、以及一次委托从「请求 → 能力检查 → start → result」的完整语义——第 1 章埋的 `inheritsParentContext` 悬念也会在这里揭开。

### 2.1 `ctx.subagents` 注册表

`ctx.subagents` 是能力缝的「总机」：provider 在这里按名注册，调用方在这里按名取用，生命周期事件在这里广播。[^c2-S2-4.1][^c2-S3-4.1]

### 2.1.1 registerProvider：按名注册 + effect-scoped

`registerProvider(provider)` 把同一进程内的实现注册进注册表，以 `provider.name` 作为唯一键；**重名注册会失败**。[^c2-S3-4.1]

```ts
// 注册一行：provider 对象实现 SubagentProvider 契约（见 2.2）
ctx.subagents.registerProvider(myProvider)
```

关键语义是 **effect-scoped**：注册的生命周期跟随注册时的 cordis effect（通常是插件 apply 的作用域）。[^c2-S2-4.1]

- **移除 provider**（effect 结束或手动注销）：阻止**新的** start 请求，但**不撤销已经返回的 run**——已经跑起来的 child 继续跑到自然结束。
- 这和你直觉里的「卸载 = 立即杀死」不一样：卸载只关「进不去」，不关「出不来」。

> [!tip] 大白话
> 把 effect-scoped 想成员工离职：离职（移除注册）只是 HR 把工牌停了，他**已经接的活还会继续干完**，但不会再给他派新活。所以……注册表里的「移除」是「不再接受新委托」，不是「终止已接受的委托」——已接受的 run 要自己等结果并 dispose（见 2.4）。

### 2.1.2 查询：getProvider / list

- `getProvider(name)`：按名取 provider 实例。
- `list()`：枚举当前注册的所有 provider。

这两个是只读查询，不改注册表状态。[^c2-S3-4.1]

### 2.1.3 核心方法总览

注册表不只是「存 provider 的 map」，它还是整个 subagent 服务的门面。核心方法总览如下：[^c2-S2-4.1]

| 方法 | 一句话职责 | 深挖章节 |
| --- | --- | --- |
| `start` | 发起一次性（one-shot）前台委托 | 本章 2.4 |
| `startContinuable` | 建立持久可恢复 child 并投递初始 prompt | 第 5 章 |
| `followup` | 向可恢复 child 发送继续执行消息 | 第 5 章 |
| `interrupt` | 停止一个可恢复 child | 第 5 章 |
| `reportFrom` | child 向直接 parent 上报 | 第 5 章 |
| `registerContinuableSetup` | 注册冷恢复时的 setup | 第 5 章 |
| `drainContinuableDescendants` | 排空某个 child 的 continuable 后代 | 第 5 章 |
| `listChildren` / `listDescendants` | 只读枚举委派树 | 本章 2.1.4 |

### 2.1.4 生命周期事件与只读枚举

注册表会广播两类事件：[^c2-S2-4.1]

- `subagent/provider-added`、`subagent/provider-removed`：provider 上下线。
- `subagent/start`、`subagent/end`：委托开始/结束的配对事件，`end` 按**委派 parent scope** 过滤分发——只有直接 parent 相关的监听者收到，避免事件风暴。

`listChildren` / `listDescendants` 是**只读枚举**：它只列「有哪些 child」，不加载/恢复 child、不查 Activation map、不查 Agent 注册表、不验证 provider 可用性。[^c2-S2-4.1] 想要「活的」child 状态，得走 continuable 家族的 API（第 5 章）。

> [!note] 这在 Claude Code 里相当于
> `ctx.subagents` ≈ Claude Code 的 subagent 运行时注册中心，但更显式：Claude Code 里 subagent 由框架从 `.claude/agents/*.md` 自动发现，你基本不碰「注册」这件事；dsh 里 provider 注册、查询、事件监听都是可编程的一等公民。

### 2.2 `SubagentProvider` 契约

provider 是一个实现 `SubagentProvider` 契约的对象。下面是契约速览（类型以 S2/S3 为准，非完整实现，仅作字段地图）：[^c2-S2-4.2][^c2-S3-4.2]

```ts
const myProvider: SubagentProvider = {
  // ① 唯一注册名：getProvider / config.provider 都靠它
  name: 'my-provider',
  // ② 启动时能力声明：outputSchema / depthLimit / toolFilter / persona
  //    不声明 → 请求对应能力的 start 会被 UNSUPPORTED_CAPABILITY 拒绝
  capabilities: {},
  // ③ 描述性标注：是否把父对话种子注入 child（fork 才 true）
  inheritsParentContext: false,
  // ④ 建立一次性 child，发布后返回 handle
  async start(request: ResolvedSubagentStartRequest): Promise<SubagentRun> {
    throw new Error('TODO: implement start()')
  },
  // ⑤ 可选：方法存在即支持续写（continuable）
  // async prepareContinuable(request) { return { seed: undefined } }
}
```

### 2.2.1 name：唯一注册名

`name` 是 provider 在注册表里的身份证。`spawn` / `fork` / `acp` / `dsh-sdk` 这些内置 provider 的 `name` 就是它们被调用的那个名字；`dsh-tool-subagent` 的 `config.provider` 字段直接拿它当值。重名注册会失败。[^c2-S2-4.2][^c2-S3-4.1]

### 2.2.2 capabilities：四个启动时 flag

`capabilities` 声明这个 provider **在启动时能提供哪些能力**，四个 flag 与 `SubagentStartRequest` 选项一一对应：[^c2-S2-4.2][^c2-S3-4.2]

| capabilities flag | 对应请求选项 | 含义 |
| --- | --- | --- |
| `outputSchema` | `outputSchema` | 能对 child 做结构化输出约束 |
| `depthLimit` | `maxDepth` | 能强制委派深度上限 |
| `toolFilter` | `toolFilter` | 能过滤 child 可见/可用的工具 |
| `persona` | `persona` | 能为 child 遮蔽部署 persona |

capabilities 是**启动期静态声明**：服务在 start 前就查它来决定要不要拒绝请求（见 2.3），不做事后诸葛亮。

> [!tip] 大白话
> 把 capabilities 想成餐厅门口贴的资质清单：「本店能：外送 / 宴席 / 包间」。你（调用方）按这张清单点单；清单上没写的能力，服务员会当场告诉你做不了。所以……capabilities 不是「运行时能力检测」，而是 provider 自己拍胸脯承诺的启动期声明——承诺了就得兑现。

### 2.2.3 inheritsParentContext：解开第 1 章的悬念

第 1 章埋的悬念现在揭开：**`inheritsParentContext` 与「继承」直觉相反**——它是**描述性标注**，只说明「是否把父对话种子注入 child」，**不暗示工具 / 服务 / 权限的继承**。[^c2-S2-4.2]

| provider | inheritsParentContext | 含义 |
| --- | --- | --- |
| fork | `true` | 从父已完成 turn 种子启动，child 能接续父对话 |
| spawn / acp / dsh-sdk | `false` | 全新 child，不带父对话 |

为什么说它「名不副实」：`inherit` 这个词容易让你以为「父有什么，子就继承什么」——工具、服务、权限、sandbox 策略。官方明确否定了这个联想：它只担保「对话种子」这一件事，其余一概不继承。[^c2-S2-4.2] 这也解释了为什么 fork 只复用「已完成 turn 的日志前缀」，而不是复制父的整套运行时。

> [!warning] 埋坑 ③：inheritsParentContext 只是描述性标注
> 看到 `inheritsParentContext: true` 别以为「父的工具/服务/权限都会跟过去」。它只说明「child 带了父的对话种子」，工具、服务、权限一概不继承。想给 child 授工具或权限，得显式通过 `agentOptions` / `toolFilter` 等选项做，不能指望这个 flag 顺带继承。

> [!tip] 大白话
> 把「继承」想成「带了个 U 盘」：`inheritsParentContext: true` 只是说「child 上岗时，把父的对话记录拷进 U 盘带过去」，不是说「child 继承了父的银行卡、门禁卡和工牌」。所以……看到这个 flag 别兴奋，它担保的只有对话种子，工具/服务/权限一概不跟着走。

### 2.2.4 start：发布后返回 handle

`start(request: ResolvedSubagentStartRequest): Promise<SubagentRun>` 是 provider 的「干活入口」，语义有两处要精确理解：[^c2-S2-4.2]

1. **输入是 `ResolvedSubagentStartRequest`** = `SubagentStartRequest` + `descriptor`。服务在调 `start` 之前已经完成了能力校验、并解析好了分离的一次性描述符（`SubagentDescriptorData`）——provider 拿到的不是裸请求，而是「校验过 + 解析好」的版本。
2. **发布后返回 handle**：provider 要先把 child「发布」到运行状态，然后才 resolve 出 `SubagentRun`。如果 fulfill 之前失败，**必须清理未发布部分的资源，不得留孤儿**——这是写 provider 的硬性卫生要求，第 4 章会展开。

另外：**可继续（continuable）child 绝不会到达 `SubagentProvider.start()`**——它们走 `prepareContinuable` 那条路（2.2.5）。[^c2-S2-4.2]

### 2.2.5 prepareContinuable：存在即能力

`prepareContinuable?(request)` 是可选方法，语义是：**方法存在即能力**——服务端用 TypeScript 类型收窄来发现「这个 provider 支不支持续写」，而不是查某个开关字段。[^c2-S2-4.2][^c2-S3-4.2]

- 它只返回 `ContinuableCreateSpec`，目前仅一个字段：可选的父历史种子 `seed`。**不含** Agent / handle / 投递 / 结果 / dispose / 恢复——那些是服务端的事。
- 冷恢复**不经由 provider 分发**；拥有 `prepareContinuable` 的 provider 仍可同时服务普通 one-shot 委托。

一句话：`prepareContinuable` 是 provider 向服务表白的入口——「我能生可持续恢复的孩子」，但孩子怎么养（投递/恢复/编排）归服务管。细节在第 5 章。

### 2.2.6 信任模型

官方还明确了一个心智前提：**provider 是受信任的同进程实现**；调用方把描述符/返回值当作「借用的不可变数据」，不会去改它。服务可以对不同 child **并发**调用同一个 provider，各 run 的取消/失败/结算互相独立。[^c2-S2-4.2] 这意味着你写 provider 时不用操心「并发安全」之外的全局状态，但也不能指望服务帮你串行化。

### 2.3 `SubagentStartRequest` 选项与能力检查

调用方发起委托时，可以带一组选项。总览如下：[^c2-S2-4.3]

| 选项 | 含义 | 要求的能力 |
| --- | --- | --- |
| `label` | 委托的显示标签（日志/UI 用） | — |
| `prompt` | `ContentBlock[]` 初始指令 | — |
| `parent` | 父级会话/代理标识 | — |
| `signal` | 取消信号（AbortSignal 类） | — |
| `agentOptions` | 子代理运行选项（如深度字段） | — |
| `outputSchema` | object-rooted JSON Schema | `outputSchema` |
| `maxDepth` | 绝对委派深度上限（非负安全整数） | `depthLimit` |
| `toolFilter` | 命名工具过滤 | `toolFilter` |
| `persona` | 遮蔽部署 persona | `persona` |

前五个是无条件选项；后四个各绑定一个 `capabilities` flag。

### 2.3.1 UNSUPPORTED_CAPABILITY：响亮失败，绝不静默

最重要的能力检查规则：**请求依赖了提供方不具备的能力，启动时会被明确拒绝——`SubagentError('UNSUPPORTED_CAPABILITY')`——绝不会被接受后静默忽略**。[^c2-S2-4.3]

> [!warning] 埋坑 ①：能力不匹配绝不静默
> 不要写「provider 没声明 outputSchema 就试着硬跑」的代码。服务在 start 前就查 capabilities，缺什么拒绝什么，错误类型统一是 `UNSUPPORTED_CAPABILITY`。消费者侧也一样：收到这个错误，说明 provider 选错了（该换 spawn/fork 而不是 acp），不是重试能解决的。

> [!tip] 大白话
> 把 UNSUPPORTED_CAPABILITY 想成点菜时服务员直接说「这道菜我们做不了」——而不是假装下单然后端上来一盘糊的。所以……dsh 的哲学是「拒绝得越早越响越好」，宁可启动时给你一个明确错误，也不让你在结果里猜为什么不对。

### 2.3.2 outputSchema：请求了不保证得到

`outputSchema` 会强制 `assertObjectJsonSchema` 子集内的 object-rooted schema；**成功时** child 返回 `SubagentResult.structured`。[^c2-S2-4.3] 但注意措辞——**请求了不保证得到**：

> [!warning] 埋坑 ②：outputSchema 不保证 structured
> 你请求了 schema，只是「有权拿到 structured」，不是「一定拿到」。消费者必须处理 `structured` 缺失的情况，回退到 `output` 文本。第 4 章写 provider 时也会看到，provider 侧是「尽力约束」，不是「绝对保证」。

### 2.3.3 toolFilter / persona / maxDepth

- **`toolFilter`**（要求 `toolFilter` 能力）：进程内用 scoped `tools.restrict()` 实现——命名工具从 child 的 prompt 消失且拒绝执行。官方强调这是**可见性而非权限**：工具不是「被禁用」，而是「从视野里拿掉」。未知名字会大声校验。[^c2-S2-4.3]
- **`persona`**（要求 `persona` 能力）：进程内注册 scoped `deployment:persona` section，只对该 child 遮蔽部署 persona。[^c2-S2-4.3]
- **`maxDepth`**（要求 `depthLimit` 能力）：可选绝对委派深度上限，非负安全整数。[^c2-S2-4.3] 深度的双重表示与 `'provider-managed'` 特例在第 5 章展开，这里先记住「要强制深度，必须选有 `depthLimit` 能力的 provider」。

### 2.4 `SubagentRun` / `SubagentResult`：一次委托怎么结算

`start` 返回的是 `SubagentRun`——一个**一次性的前台委派**：只有一个结果，消费方 await 结果并**始终 dispose**，直至完全停稳。[^c2-S2-4.4]

> [!note] 这在 Claude Code 里相当于
> `SubagentRun` ≈ 一次 `task` 工具调用返回的句柄，但 dsh 把「用完要收尾」变成显式纪律：dispose 不是可选项，而是每次委托的收尾动作。写消费方时把它当成「try/finally 里必须执行的清理」，别等 GC。

### 2.4.1 result 不因 child 级失败 reject

最反直觉的一条：**`result` 不因 child 级失败 reject**。[^c2-S2-4.4][^c2-S3-4.2]

- model / transport 层面的失败（超时、拒绝、模型报错……）以 `stopReason: 'error'` **正常 resolve**，消费方把结果映射为 `isError` 工具结果。
- 只有**基础设施故障**（框架级崩溃、进程消失这类）才 reject。

> [!tip] 大白话
> 把这次委托想成「点了外卖」：外卖员半路车坏了（child 级失败）——骑手（promise）还是会带着「这单没送到」的消息回来，你收到的是 `stopReason: 'error'` 的正常结果；只有骑手本人人间蒸发（基础设施故障）你才会接到「查无此人」的异常。所以……写消费方时，「处理 stopReason='error'」和「处理 reject」是两件不同的事，前者是常态路径。

### 2.4.2 output 语义：取最后一个非空 assistant 消息

`SubagentResult.output` 的取值规则：[^c2-S2-4.4][^c2-S6-4.4]

1. 取**最后一个非空** assistant 消息内容；
2. 空内容消息（含 usage-only）跳过；
3. 无非空消息 → 回退为累积的 assistant 文本流；
4. 两者皆无 → `[]`。

### 2.4.3 stopReason：五个值 + ACP/dsh-sdk 映射

`stopReason` 是一个可合并扩展的派生联合，当前五值：[^c2-S2-4.4]

| stopReason | 含义 | output 状态 |
| --- | --- | --- |
| `completed` | 正常完成 | 完整 |
| `aborted` | 被取消/中断 | 可能不完整 |
| `error` | 模型/传输失败 | 可能不完整 |
| `max-tokens` | 触达 token 上限 | 可能不完整 |
| `refusal` | 模型拒绝 | 可能不完整 |

非 `completed` 的 stopReason 都表示 output **可能不完整**。

外部后端（out-of-process provider）会把它们自己的终止码映射到这套五值：[^c2-S5-4.4][^c2-S6-4.4]

**ACP（`dsh-subagent-acp`）映射：**

| ACP 终止码 | → stopReason |
| --- | --- |
| `end_turn` | `completed` |
| `max_tokens` | `max-tokens` |
| `refusal` | `refusal` |
| `cancelled` | `aborted` |
| `max_turn_requests` / 未知 | `error` |

**dsh-sdk（`dsh-subagent-dsh-sdk`）映射：**

| SDK 终止 | → stopReason |
| --- | --- |
| `completed` / `max-tokens` / `aborted` | 原样透传 |
| 其余一切（error / interrupted / disposed / 未来变体 / 无 turn） | `error` |

dsh-sdk 的规则尤其值得记住一句话：**不洁停止绝不报成功**——只要不是明确地 completed/max-tokens/aborted，一律落到 `error`，绝不粉饰太平。[^c2-S6-4.4]

### 本章小结

- `ctx.subagents` 是总机：`registerProvider` 按名注册且 effect-scoped（移除阻止新 start、不撤销已返回 run）；`getProvider`/`list` 查询；事件 `provider-added/removed`、`start/end`（end 按 parent scope 分发）；`listChildren/listDescendants` 只读枚举。
- `SubagentProvider` 契约五块：`name` 唯一名；`capabilities` 四 flag（outputSchema/depthLimit/toolFilter/persona）是启动期静态声明；`inheritsParentContext` 只是「带没带对话种子」的描述性标注，不担保工具/服务/权限继承；`start` 在发布后返回 handle、发布前失败要清理；`prepareContinuable` 存在即能力。
- `SubagentStartRequest` 九个选项，后四个绑定能力；能力不匹配 → `UNSUPPORTED_CAPABILITY` 响亮失败，绝不静默。
- `SubagentRun` 是一次性前台委托：result 不因 child 级失败 reject（`stopReason:'error'` 正常 resolve），output 取最后一个非空 assistant 消息，stopReason 五值，ACP/dsh-sdk 映射遵循「不洁停止绝不报成功」。
- 埋的三个坑：① 能力不匹配响亮失败 ② outputSchema 请求了不保证 structured ③ inheritsParentContext 名不副实。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 注册方式 | 框架从 `.claude/agents/*.md` 自动发现 | `ctx.subagents.registerProvider` 显式注册，effect-scoped |
| 能力声明 | md frontmatter 里隐含 | `capabilities` 四 flag 静态声明，缺则拒 |
| 结果模型 | 「运行即结果」，失败即异常 | 显式 `SubagentRun`/`SubagentResult` + `stopReason` 五值 |
| 上下文继承 | 隐式 | `inheritsParentContext` 描述性标注，只担保对话种子 |
| 续写 | 一次 task 委派，无持久续写 | `prepareContinuable` / continuable 家族（第 5 章） |

迁移心智：Claude Code 把 subagent 的「注册、能力、结果」都收敛在框架和 md 文件里；dsh 把这三件事全部显式化、可编程化。你在 Claude Code 里「写一个 md 文件声明角色」的心智，对应到 dsh 是「实现一个 `SubagentProvider` 对象并注册」——而「结果长什么样、怎么结算」不再是框架替你兜底，你要按 `stopReason` / `output` 语义自己解读。这正是第 1 章说的「能力缝把一切暴露成可替换的契约」在接口层的落地。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方子系统文档与核心包 README。`SubagentProvider` 类型速览为 S2/S3 契约的地图式整理，非完整实现；若 preview 更新改动注册表方法签名、capabilities 四 flag 或 stopReason 联合，本章 2.1-2.4 受影响，优先对照检查。

---

[^c2-S2-4.1]: S2 · Subagent 子系统设计文档（中文）§4.1——`ctx.subagents` 注册表（registerProvider effect-scoped、核心方法总览、start/end 事件、listChildren 只读枚举）。
[^c2-S3-4.1]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.1——重名注册失败、getProvider/list。
[^c2-S2-4.2]: S2 §4.2——SubagentProvider 契约（name/capabilities/inheritsParentContext/start/prepareContinuable/trust model）。
[^c2-S3-4.2]: S3 §4.2——capabilities 与请求选项一一对应、prepareContinuable 存在即能力、冷恢复不经 provider。
[^c2-S2-4.3]: S2 §4.3——SubagentStartRequest 选项、UNSUPPORTED_CAPABILITY 响亮失败、outputSchema/toolFilter/persona/maxDepth 细节。
[^c2-S2-4.4]: S2 §4.4——SubagentRun/SubagentResult 语义（dispose、result 不 reject、output 取最后非空、stopReason 五值）。
[^c2-S5-4.4]: S5 · `dsh-subagent-acp` README §4.4——ACP 终止码 → stopReason 映射表。
[^c2-S6-4.4]: S6 · `dsh-subagent-dsh-sdk` README §4.4——dsh-sdk 映射（不洁停止绝不报成功）。

---

> 契约清楚了，但六兄弟各自长什么样、怎么选、怎么挂还没讲。这一章进入现成 provider 家族的选型与挂载。

## 第三章 现成 provider 家族——选用、挂载、跑起来

> [!summary] 导读
> 第 1 章说「六个 provider 兄弟 + 一个工具」，第 2 章把 `SubagentProvider` 契约讲透了。这一章落地到三个实际问题：**选哪个、怎么挂、怎么跑**。六个兄弟不是等价复制品，它们从根上分两个世界——in-process（spawn / fork）和 out-of-process（acp / dsh-sdk），每个都有自己擅长的场景和注定做不到的事。读完你会得到一张决策地图：什么时候选 spawn、什么时候选 fork、什么时候值得上 acp 或 dsh-sdk，以及把选好的 provider 挂进 cordis 插件树、让模型真正调得到它的完整动作。第 1 章承诺的「换执行后端只改一行配置」，这一章你会亲手做一遍。

### 3.1 in-process vs out-of-process：从根上分两个世界

选 provider 的第一个问题不是「哪个能力多」，而是**child 住在哪**。dsh 的 provider 家族从根上分成两派：[^c3-S5-4.7-3][^c3-S6-4.7-4]

- **in-process（进程内）**：child 跑在宿主 harness **同一个进程**里，共享运行时、agent 注册表、工具系统。启动快、开销小，而且因为大家共用一套运行时，**启动期 capabilities（outputSchema / depthLimit / toolFilter / persona）能完整落地**——约束是在同进程内直接施加的。[^c3-S8-4.7-1]
- **out-of-process（独立子进程）**：child 是**独立子进程**，宿主通过协议（ACP / SDK JSON-RPC）握手驱动。隔离更强、更像「把活外包出去」，但代价是**跨进程传不过去的能力约束**——你没法远程强制对方「深度最多几层、只用这几个工具、按这个 schema 输出」。[^c3-S5-4.7-3][^c3-S6-4.7-4]

| 维度 | in-process（spawn / fork） | out-of-process（acp / dsh-sdk） |
| --- | --- | --- |
| child 位置 | 宿主同一进程 | 独立子进程 |
| 启动期 capabilities | 能完整落地 | 受限于协议，多为 false |
| 启动开销 | 低 | 高（每次全新进程） |
| 隔离性 | 弱（共享运行时） | 强 |
| 适合 | 要能力约束、要快 | 要隔离、要驱动外部 agent |

> [!tip] 大白话
> 把 in-process 想成「同一间办公室里的新工位」：新同事（child）和你共用复印机、门禁、前台（宿主运行时和工具系统），随时能叫、启动快，公司内部的各种资质（能力约束）直接就能给；把 out-of-process 想成「把活外包给楼外一家公司」：只能通过合同（协议）对接，对方有没有资质你说了不算。所以……选哪个先看你要不要「跨进程传不过去的能力约束」——要，就走 in-process；要隔离或要驱动外部 agent，才值得上 out-of-process。

> [!note] 这在 Claude Code 里相当于
> Claude Code 的 subagent 永远是框架内置执行，进程模型是框架内部细节，你根本不感知。dsh 把「child 住哪」变成你的显式选择——这是「执行后端可替换」的第一步，也是 Claude Code 用户最需要重建直觉的地方。

### 3.2 四兄弟逐个看

### 3.2.1 spawn：能力全开、空手入职（in-process）

`dsh-subagent-spawn-in-process` 是 in-process 的默认选择：[^c3-S8-4.7-1]

- **四项启动期能力全支持**——`outputSchema` / `depthLimit` / `toolFilter` / `persona` 都能落地，这是它最大的卖点。
- **全新 child、无父历史**——child 从零开始，**看不到父会话聊过什么**。
- `providerName` 默认 `spawn`，配置里不写 provider 名时通常落到它。

> [!warning] 埋坑 ①：spawn 全新 child、无父历史
> 「全新 child」不是小细节，而是继承语义的正反两面：spawn 的能力**全开**，但历史**全无**。如果你想让子代理「接着父对话往下聊」，spawn 给不了——那是 fork 的活（3.2.2）。选 spawn 前先确认「子代理不需要父对话上下文」这个前提成立。

### 3.2.2 fork：唯一带对话种子的 in-process

`fork` 和 spawn 同属 in-process，能力同样全，但**继承语义恰好相反**：[^c3-S1-4.7-2][^c3-S2-4.7-2]

- 从父的**已完成 turn** 种子启动——child 能顺着父对话的思路接续。
- `inheritsParentContext: true`——第 2 章已经拆过，这个 flag 只担保「带对话种子」这一件事，工具 / 服务 / 权限一概不继承。

| 维度 | spawn | fork |
| --- | --- | --- |
| 进程模型 | in-process | in-process |
| 启动期 capabilities | 全支持 | 全支持 |
| 父对话历史 | 无（全新 child） | 有（已完成 turn 种子） |
| `inheritsParentContext` | false | **true** |
| 适合 | 子代理不应被父对话带偏 | 子代理要延续父对话上下文 |

> [!tip] 大白话
> 把 spawn 想成「空手入职的新员工」，fork 想成「接上一任工作笔记的老员工」。新员工工位电脑全配齐（能力全开），但桌上没有前任的笔记——从零干起；老员工入职时把父会话的已完成对话拷进 U 盘带过去，能顺着前面的思路接。所以……能力上 spawn / fork 没差别，差别只在「带不带话」：要子代理接续父对话，就选 fork；要子代理别被父对话带偏，就选 spawn。

### 3.2.3 acp：独立子进程、零启动期能力（out-of-process）

`dsh-subagent-acp` 是 out-of-process 的第一个代表，它把每个 subagent 跑在**独立子进程**里，作为 **ACP（Agent Client Protocol）客户端**驱动。[^c3-S5-4.7-3]

- **不声明任何启动期 capabilities**：acp 无法在远程强制深度 / 工具过滤 / persona / 结构化输出，所以这四项它**全不声明**。
- **本地服务拒绝而非静默忽略**：请求依赖了 acp 不具备的能力，服务会以 `UNSUPPORTED_CAPABILITY` 响亮拒绝（呼应第 2 章），而不是「假装支持、结果不对」。这不是 bug，是设计——**别选 acp 却想要 spawn 的能力**。
- `inheritsParentContext: false`；**每次运行全新进程、无进程池**——跑一次开一个，跑完就销毁。
- 仅限本地工作区。

> [!warning] 埋坑 ②：acp 不声明任何启动期 capabilities
> 想在 acp 上用结构化输出 / 工具过滤 / persona / 强制深度？**别选它**。acp 一个都不声明，请求这些能力的 start 会被 `UNSUPPORTED_CAPABILITY` 响亮拒绝（第 2 章）。这不是「能力弱一点」的降级，而是「明确拒绝」——本地服务宁可拒绝也不静默忽略。要这些能力，回 in-process（spawn / fork）。

> [!tip] 大白话
> 把 acp 想成「外包公司派来的驻场团队」：他们很专业，但拿不到你公司内部的资格清单（没有启动期 capabilities）——你没法远程强制他们「深度最多 3 层、只能用这几个工具、按这个 schema 输出」。所以……acp 适合「只要能跑 ACP 协议的任意 agent」这类场景，但别指望它对子代理做细粒度能力约束——你要的约束对方在墙外接不住，本地服务会**直接拒绝**而不是糊弄你。

### 3.2.4 dsh-sdk：完整 peer harness（out-of-process）

`dsh-subagent-dsh-sdk` 是 out-of-process 的第二个代表，也是最「重」的一个：[^c3-S6-4.7-4]

- 通过 **stdio JSON-RPC** 驱动 harness SDK runtime，子进程是一个**完整 peer harness**——有自己的 cordis 组合、会话、模型路由、工具系统。它不是「一个被驱动的脚本」，而是「一整套独立运行的 dsh」。
- 启动期 capabilities 全 false（和 acp 同理：跨进程传不过去）；`inheritsParentContext: false`。
- **每次 run 都是全新的 runtime 进程**，启动成本**高于 acp 的典型子进程**。
- 子进程的 transcript 留在**子进程自己的 session root**，不跟父会话混在一起。

> [!note] 这在 Claude Code 里相当于
> dsh-sdk 大概是 Claude Code 里最没有直接对应物的一个：它像是「为单个子代理单独起一个完整的 Claude Code 实例」——重、独立、自管一切。Claude Code 里你不会想为一次 task 委派起一个全新实例，但 dsh-sdk 正是为此设计的「完整隔离档位」。

### 3.2.5 codex / claude-code：只列名的外部 CLI 后端

家族里还剩两个外部 CLI 后端：`codex` 和 `claude-code`。[^c3-S1-4.7-5][^c3-S10-4.7-5] 本分册**只列名、不展开**——它们的完整配置表未抓取，属于「本分册未抓取，可扩展」项（第 7 章诚实标注清单会集中列）。你只需要知道：它们和 acp / dsh-sdk 一样属于「外部后端」一族，将来若需要驱动 Codex CLI 或 Claude Code CLI 作为子代理，接口上仍是同一个 provider 口子。

### 3.2.6 全家福对照

| provider | 进程模型 | 启动期 capabilities | 父对话 | 特点 | 成本 |
| --- | --- | --- | --- | --- | --- |
| spawn | in-process | 全支持 | 无 | 能力全、空手 | 低 |
| fork | in-process | 全支持 | **有种子** | 唯一带话的 in-process | 低 |
| acp | out-of-process | 全不声明 | 无 | 驱动任意 ACP agent、每次全新进程（无池） | 中 |
| dsh-sdk | out-of-process | 全 false | 无 | 完整 peer harness、自管模型/组合/递归预算 | 高 |
| codex / claude-code | 外部 CLI | 未抓取 | 未抓取 | 仅列名，可扩展 | — |

### 3.3 环境变量与 cwd：out-of-process 的公共规矩

acp 和 dsh-sdk 虽然是两个 provider，但它们的子进程管理共用同一套 `dsh-subprocess` 语义——两条规矩在写配置时必须遵守。[^c3-S5-4.7-6][^c3-S6-4.7-6][^c3-S5-4.7-7][^c3-S6-4.7-7]

### 3.3.1 环境变量：先擦除、再合并

子进程的环境不是「父环境的复刻」，而是经过两道工序：[^c3-S5-4.7-6][^c3-S6-4.7-6]

1. **先擦除**：「凭据形状」的变量（像 `*_API_KEY` / `*_TOKEN` 这类形似密钥的）和**陈旧的 `DSH_*` 名**（可能残留旧版本的 harness 配置）一律清掉；
2. **再合并**：把显式 `config.env` 里写的变量合进去。

> [!tip] 大白话
> 把环境变量想成「出门前清空口袋再按清单装东西」：先确保口袋里没有上一趟留下的凭据（擦除凭据形状变量）和过期旧证件（陈旧 `DSH_*` 名），再按清单（`config.env`）装你要带的。所以……子进程的环境是「消毒后按需注入」，不是父环境的复制品——目的是防止父会话的密钥或过期配置泄漏进子代理。

### 3.3.2 cwd：绝不用 server 进程自身 cwd

cwd 的优先级是一句背下来的规则：[^c3-S5-4.7-7][^c3-S6-4.7-7]

1. 配置了 `cwd` → 用配置值（在 load 时校验一次）；
2. 没配置 → 用**委托方父会话**的 cwd；
3. **绝不用 server 进程自身的 cwd**。

> [!tip] 大白话
> 把 cwd 想成「在哪张桌上干活」：server 进程自己的 cwd 是「安装地点」，跟这次委托没关系；子代理应该在「叫活的人所在的那张桌」（委托方父会话的 cwd）上干活。所以……cwd 永远先看配置、再看父会话，唯独不看 server 自己站在哪——否则子代理会在一个跟任务无关的目录里乱跑，读写全都落错地方。

### 3.4 挂载：cordis.patch.yml 两行跑起来

选好 provider 之后，把它挂进插件树、暴露给模型，是**配置层**的动作。以 acp 为例，`cordis.patch.yml` 需要两行——一行 provider、一行 tool（底稿见 02 素材 6.3）：[^c3-6.3]

```yaml
# cordis.patch.yml 示例：provider + tool 两行（纯 Cordis 插件，需手动 insert）
- id: subagent-acp
  name: '@deepseek-ai/dsh-subagent-acp'
  config:
    providerName: acp
    command: node
    args: ['--import', 'tsx', './packages/examples/acp-demo/src/bin.ts']
    permission: reject
    env:
      DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config: { provider: acp, toolName: subagent }
```

逐行读：

- **provider 行**（`id: subagent-acp`）：加载 `dsh-subagent-acp` 包。`config.providerName: acp` 是注册进 `ctx.subagents` 的名字（spawn 的默认值就是 `spawn`，这里显式写 `acp`）；`command` / `args` 定义子进程怎么拉起；`permission: reject` 是子进程权限策略；`env` 是显式注入的环境变量——正好用上 3.3.1 的「先擦除再合并」。
- **tool 行**（`id: tool-subagent`）：加载 `dsh-tool-subagent`，`config: { provider: acp, toolName: subagent }` 把 **acp 这个 provider** 绑成一个模型可见的、名叫 `subagent` 的工具——**一个 provider 绑一个 toolName**，toolName 全局唯一（默认 `subagent`，工具层的完整字段在第 6 章展开）。[^c3-S7-4.8-1]

> [!warning] 埋坑 ③：subagent 系列是纯 Cordis 插件，必须手动 insert
> 第 1 章提过、这里落地：subagent 系列包**都是纯 Cordis 插件**（没有 `dsh.bundle.patch`）。这意味着 `dsh plugin add` 只让包「可被解析」，**并不会把它挂进插件树**——你还得手动在 `cordis.patch.yml` 里 insert 一条，它才会真正被加载。这是和「自带 bundle 配置」的插件最不一样的地方，忘了 insert，包装好了却毫无作用。

> [!tip] 大白话
> 把 `dsh plugin add` 想成「把新书记进书店的进货清单」：仓库（包解析）知道有这本书了，但书还没摆上货架（插件树）。纯 Cordis 插件要再「手动上架」——在 `cordis.patch.yml` 里 insert 一条，它才会真正被顾客（模型）看到。所以……subagent 包 add 完不等于能用，记得手动 insert。

两点诚实标注（本分册约定，成稿时保留）：

1. **acp 命令参数以 02 素材 6.3 为准**（示例里是一个 demo bin 路径），**需对照 S5 README 核实**后再用于你的项目；
2. **手动 insert 的精确语法**标注为**需对照配置体系笔记 + C1 第三方插件示例核实**——`cordis.patch.yml` 的完整 schema 细节见 [[DeepSeek-Harness 配置体系]]。

### 3.5 选择 provider：一张决策表

把上面的特性收敛成选择依据（02 素材 6.4）：[^c3-6.4]

| 需求 | 选 | 依据 |
| --- | --- | --- |
| 想要结构化输出 / 工具过滤 / persona / 深度强制 | spawn / fork | in-process 能力全（S8/S2） |
| 想要完整独立 harness（自管模型 / 组合 / 递归预算） | dsh-sdk | 完整 peer harness（S6） |
| 想要驱动任意 ACP 协议 agent | acp | ACP 客户端驱动（S5） |
| 想要子代理继承父对话上下文 | fork | 唯一带种子的 in-process（S2） |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | 均无父历史（S2/S5/S6） |

用法建议：

1. **默认问句**：子代理要不要父对话？要 → fork；不要 → 继续往下问。
2. **第二问句**：要不要 in-process 才能给的能力约束（结构化输出 / 工具过滤 / persona / 强制深度）？要 → spawn；不要 → 看第三问。
3. **第三问句**：要驱动外部 agent 吗？驱动任意 ACP 协议 agent → acp；要完整独立 harness（连模型路由都自己管）→ dsh-sdk；驱动 Codex / Claude Code CLI → 留给后续分册扩展。

第 1 章那句「换执行后端只改一行配置」，到这里就是：把 `cordis.patch.yml` 里 tool 行的 `config.provider` 从 `acp` 改成 `spawn`，再换上对应 provider 行——定义包和工具一行都不用动。写自己的 provider（第 4 章）时，in-process 的 `start()` 走 `ctx.agents`，out-of-process 的 `start()` 要握手 ACP / SDK initialize，这两条路在第 4 章分别展开。

### 本章小结

- provider 家族从根上分两派：in-process（spawn / fork）能力全、开销低；out-of-process（acp / dsh-sdk）隔离强、但跨进程能力约束传不过去。
- spawn 能力全开、全新 child 无父历史；fork 是唯一带对话种子的 in-process（`inheritsParentContext: true`，但只担保对话种子）。
- acp 不声明任何启动期 capabilities，本地服务**拒绝而非静默忽略**；每次运行全新进程（无池）；dsh-sdk 是完整 peer harness，自管模型 / 组合 / 递归预算，每次全新 runtime 进程、成本最高。
- codex / claude-code 仅列名，配置表本分册未抓取，可扩展。
- out-of-process 公共规矩：环境变量先擦除凭据形状变量与陈旧 `DSH_*` 名、再合并 `config.env`；cwd 优先配置、其次父会话 cwd，**绝不用 server 进程自身 cwd**。
- 挂载是配置层动作：`cordis.patch.yml` 的 provider + tool 两行；subagent 系列是纯 Cordis 插件，`dsh plugin add` 之后必须手动 insert 才生效。
- 选择决策：父对话 → fork；能力约束 → spawn；驱动外部 agent → acp / dsh-sdk；换执行后端只改配置一行。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 执行后端 | 内置唯一实现，不可换 | provider 全家桶，配置一行切换 |
| 首问 | 「subagent 用什么引擎跑」不是个问题 | 第一问题：spawn / fork / acp / dsh-sdk |
| 进程模型 | 框架内部细节，用户不感知 | in-process vs out-of-process 是显式选择 |
| 上下文继承 | 隐式 | fork 显式带种子（`inheritsParentContext: true`） |
| 挂载 | 丢一个 md 文件即自动发现 | 纯 Cordis 插件需手动 insert 进 `cordis.patch.yml` |

迁移心智：Claude Code 里「执行后端」是个伪问题——内置唯一实现，你没得选；dsh 把它降级成配置里的一个字符串，于是「选哪个 provider」成了使用 subagent 的第一决策点。Claude Code 用户最容易踩的三处是：以为所有 provider 能力一样（其实 acp 零能力约束）、以为 add 包就能用（其实要手动 insert）、以为父对话会自动继承（其实只有 fork 带种子）。这三条分别对应本章埋的 ①③② 三个坑，跑起来之前先对一遍。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档。provider 特性对照引自 S8 / S1/S2 / S5 / S6 README 与子系统文档；`cordis.patch.yml` 底稿来自 02 素材 6.3，acp 命令参数需对照 S5 README 核实、手动 insert 精确语法需对照 [[DeepSeek-Harness 配置体系]] + C1 第三方插件示例核实。若 preview 更新改变 provider 的 capabilities 声明、子进程环境/cwd 语义或配置 schema，本章 3.2-3.4 是受影响区域，优先对照检查。codex / claude-code 配置表未抓取，留待后续分册扩展。

---

[^c3-S8-4.7-1]: S8 · `subagent-spawn-in-process` README §4.7——spawn：in-process、全新 child 无父历史、四项启动期能力全支持、`providerName` 默认 `spawn`。
[^c3-S1-4.7-2]: S1 · Subagent 子系统设计文档（EN）§4.7——fork 从父已完成 turn 种子启动。
[^c3-S2-4.7-2]: S2 · Subagent 子系统设计文档（中文）§4.7——fork 的 `inheritsParentContext: true`。
[^c3-S5-4.7-3]: S5 · `dsh-subagent-acp` README §4.7——acp：out-of-process、独立子进程、ACP 客户端驱动、零启动期 capabilities、本地服务拒绝而非静默忽略、每次全新进程（无池）、仅本地工作区。
[^c3-S6-4.7-4]: S6 · `dsh-subagent-dsh-sdk` README §4.7——dsh-sdk：stdio JSON-RPC 驱动、完整 peer harness（自管 cordis 组合/会话/模型路由/工具）、启动期 capabilities 全 false、每次 run 全新 runtime 进程、成本更高、transcript 留在子进程自己的 session root。
[^c3-S1-4.7-5]: S1 §4.7——codex / claude-code 外部 CLI 后端仅列名。
[^c3-S10-4.7-5]: S10 · 扩展 Cookbook §4.7——provider 家族全景（六兄弟 + tool）。
[^c3-S5-4.7-6]: S5 §4.7——acp 环境变量处理（dsh-subprocess 语义：先擦除凭据形状变量与陈旧 `DSH_*` 名，再合并显式 `config.env`）。
[^c3-S6-4.7-6]: S6 §4.7——dsh-sdk 同用 `dsh-subprocess` 环境变量语义。
[^c3-S5-4.7-7]: S5 §4.7——acp cwd 规则（配置优先且在 load 时校验一次、否则父会话 cwd、绝不用 server 进程自身 cwd）。
[^c3-S6-4.7-7]: S6 §4.7——dsh-sdk 同 cwd 规则。
[^c3-S7-4.8-1]: S7 · `dsh-tool-subagent` README §4.8——一个 provider 绑一个 toolName（默认 `subagent`）、`config.provider` 必填、toolName 全局唯一。
[^c3-6.3]: 02 深度研究 §6.3——`cordis.patch.yml` 挂载底稿（acp provider + tool 两行）；acp 命令参数以 6.3 为准、需对照 S5 README 核实；纯 Cordis 插件需手动 insert。
[^c3-6.4]: 02 深度研究 §6.4——选择 provider 决策依据表。

---

> 选型、挂载都跑通了，但如果六兄弟不够用，就该自己写一个 provider 了——这一章把三段式方法论落到可运行的最小骨架。

## 第四章 写自己的 provider——三段式与最小实现

> [!summary] 导读
> 第 1 章给了「能力缝 + 三层结构」的地图，第 2 章把 `SubagentProvider` 契约逐字段拆开，但还没有一行能跑的代码。这一章把「写一个自己的 provider」从方法论落实到可运行骨架：先讲官方三段式怎么拆包、怎么命名、怎么设计（my-cap 三件套）；再给一个最小 `SubagentProvider` 骨架逐行拆解，并诚实标注哪些是「综合推断」、发布前要对照哪份源码；接着区分 `start()` 的 in-process 与 out-of-process 两条实现路径，讲清 effect-scoped 注册与卸载；最后给出三个写 provider 必踩的坑和 Claude Code 迁移映射。读完你就能照着骨架写一个能注册、能挂进插件树的 provider。

### 4.1 三段式方法论：三个包怎么拆、怎么命名、怎么设计

第 1 章 §1.5 说过「完整能力本身才是接缝，单一角色不是」——写一个 dsh 能力，就是按 ①②③ 三段把三件套补齐。[^c4-S4-4.9-1] 这一节把它变成可操作的三条指令。

### 4.1.1 三件套代码走读（官方 my-cap 示例）

官方开发者实践教程用 `my-cap` 做了完整示范，三个包、三段代码：[^c4-6.2]

```ts
// ===== ① Service Definition：定义契约（包名 dsh-my-cap） =====
// 抽象 Service 类：声明「myCap 这个能力长什么样」，不写实现
export abstract class MyCapService extends Service {
  constructor(ctx: Context) { super(ctx, 'myCap') }
  abstract execute(request: MyCapRequest): Promise<MyCapResult>
}

// ===== ② Provider：实现（包名 dsh-my-cap-local） =====
class MyCapLocal extends MyCapService {
  async execute(request: MyCapRequest): Promise<MyCapResult> {
    return { output: request.input.toUpperCase() }
  }
}
export function apply(ctx: Context) { ctx.plugin(MyCapLocal) }

// ===== ③ Consumer/Tool：暴露给模型（包名 dsh-tool-my-cap） =====
export const inject = ['tools', 'myCap']   // 注入 tools 服务 + 本能力
export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'my_cap', description: 'Execute my capability.',
    parameters: { input: { type: 'string', required: true } },
    output: { schema: { type: 'string' }, render: (_a, v) => [{ type: 'text', text: v }] },
    async execute(args) { return (await ctx.myCap.execute({ input: args.input })).output },
  }))
}
```

三段的职责（对照第 1 章的三层结构图）：

- **① 定义包 `dsh-my-cap`**：`MyCapService` 是一个 cordis `Service` 子类，`super(ctx, 'myCap')` 把服务注册成 `ctx.myCap`；`execute(request): Promise<MyCapResult>` 是抽象签名，定义「调用方要传什么、会拿回什么」。[^c4-S4-4.9-1] 6.2 代码里没展开但属于定义包的还有两样：`MyCapRequest` / `MyCapResult` 类型定义，以及 `declare module` 把 `ctx.myCap` 扩展进 `Context` 类型（这样消费方写 `ctx.myCap.execute(...)` 有类型提示）。这三样合起来才是「契约」。这套 cordis Service + `defineTool` 的写法与 [[DeepSeek-Harness 插件开发核心]] 里的插件结构同源。
- **② Provider 实现包 `dsh-my-cap-local`**：`MyCapLocal extends MyCapService` 真把 `execute` 实现了（这里就是 `input.toUpperCase()`）；`export function apply(ctx) { ctx.plugin(MyCapLocal) }` 是 cordis 插件入口，把实现挂上服务点。换实现 = 换这个包，定义和消费不动。
- **③ Consumer/Tool 包 `dsh-tool-my-cap`**：`export const inject = ['tools', 'myCap']` 声明这个插件要注入 `tools` 服务（用于注册工具）和 `myCap` 服务（用于调能力）；`defineTool({...})` 描述工具的形状；`ctx.tools.register(...)` 把它挂进工具表，模型就能调了。[^c4-S4-4.9-1]

> [!tip] 大白话
> 把三件套想成「打印机生态」：定义包是 USB 接口标准（我的接口长这样、数据怎么传）；provider 是各家驱动（惠普的、佳能的，都实现同一个标准）；consumer/tool 是你电脑上的「打印」按钮。所以……换驱动不用换按钮，按钮只认标准——这就是「provider 与 consumer 只依赖定义包」的实际手感。

### 4.1.2 命名律：dsh-<cap> / <cap>-local / dsh-tool-<cap>

三件套的包名不是随便起的，官方命名律如下：[^c4-S4-4.9-2]

| 角色 | 包名模式 | my-cap 实例 | subagent 家族实例 |
| --- | --- | --- | --- |
| ① Service Definition | `dsh-<cap>` | `dsh-my-cap` | `dsh-subagent` |
| ② Provider | `<cap>-local` | `dsh-my-cap-local` | `dsh-subagent-spawn-in-process` / `-fork` / `-acp` / `-dsh-sdk` |
| ③ Consumer/Tool | `dsh-tool-<cap>` | `dsh-tool-my-cap` | `dsh-tool-subagent` |

subagent 系列是这条律的忠实执行者：定义 `dsh-subagent`，工具 `dsh-tool-subagent`，各 provider 是 `dsh-subagent-<实现>`。你写自己的 provider 时，包名照 `<cap>-local` 或 `dsh-subagent-<实现>` 的样子起，别人一眼能看出它在三层里站哪层。

### 4.1.3 设计要点：三句官方戒律

三段式不只是「拆三个包」，官方还给了三条设计戒律：[^c4-S4-4.9-3]

1. **Do not split preemptively（不要预防性拆包）**。三件套是目标架构，不是起步强制——只有某个角色需要**独立演进**（不同团队、不同发布节奏、要被单独复用）才把它拆成独立包。对 subagent 来说这条尤其省事：定义包 `dsh-subagent` 和工具包 `dsh-tool-subagent` 官方已经给你了，你写自己的 provider 时**只写 ②**，①③ 直接复用。你的「三段式」实际上是「一段半」：写 provider 包，配置里把工具指到你的 `name`。
2. **Request / Result 类型归定义包所有**。跨缝流动的数据形状只能由定义包定义，provider 与 consumer 都从定义包 import，谁也不准自己发明一份。这就是第 1 章「只依赖定义包」的类型级保证——换 provider 不换类型。
3. **默认值在显式 `resolve(request): Spec` 里处理，不在 `run()` 里藏 `?? default`**。请求在进入实现前先被规范化成一个完整 Spec；`run()` / `start()` 只处理已经解析好的值，不隐含 fallback。这样行为可预测、可单测，也避免「同样的入参在不同 provider 里默认值不一样」。

> [!tip] 大白话
> 把「不要在 run() 里藏默认值」想成餐厅后厨：下单（request）先经过前台收银系统（resolve）补全「默认少辣、默认热饮」，再递给后厨；后厨（run）只按单做菜，不再自己猜「要不要加辣」。所以……所有「没写就怎样」的逻辑集中在 resolve 一处，后厨永远拿到完整订单，出菜才一致。

### 4.2 最小 provider 骨架逐行拆解（综合推断标注）

现在把方法论套到 subagent 上：写一个 provider 包，`apply` 里 `ctx.subagents.registerProvider(...)`。

> [!warning] 综合推断标注
> **官方目前没有独立的「SubagentProvider 教程」**。下面这份骨架是把 S2 的契约定义（`name` / `capabilities` / `inheritsParentContext` / `start` / `prepareContinuable`）与 S4 的三段式拼合出来的**综合推断**，不是官方原样代码。[^c4-6.1] 尤其 `start()` 里「经 `ctx.agents` 创建 child」这一句，**发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码核实**。[^c4-S8]

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'
import type {
  SubagentProvider,
  ResolvedSubagentStartRequest,
  SubagentRun,
} from '@deepseek-ai/dsh-subagent'

// 契约对象：满足 SubagentProvider 接口（类型来自定义包 dsh-subagent）
const myProvider: SubagentProvider = {
  // ① 唯一注册名：config.provider 与 getProvider() 都靠它；重名注册失败
  name: 'my-provider',

  // ② 启动期能力声明：outputSchema / depthLimit / toolFilter / persona
  //    不声明 → 请求这些能力的 start 会被 UNSUPPORTED_CAPABILITY 拒绝
  capabilities: {},

  // ③ 描述性标注：是否把父对话种子注入 child（fork 才 true）
  inheritsParentContext: false,

  // ④ 建立一次性 child，发布后返回 handle；发布前失败要清理并 reject
  async start(request: ResolvedSubagentStartRequest): Promise<SubagentRun> {
    // in-process：经 ctx.agents 创建 child（对照 spawn-in-process 源码）
    // out-of-process：spawn 子进程 → 握手（ACP initialize / SDK initialize）→ 返回 run
    throw new Error('TODO: implement start()')
  },

  // ⑤ 可选：方法存在即支持续写（continuable）
  // async prepareContinuable(request) { return { seed: undefined } }
}

// cordis 插件入口约定：export const name + export function apply
export const name = 'my-subagent-provider'
export function apply(ctx: Context) {
  ctx.subagents.registerProvider(myProvider)  // effect-scoped，卸载自动注销
}
```

逐行拆解：

- **import**：契约类型（`SubagentProvider` / `ResolvedSubagentStartRequest` / `SubagentRun`）全部从定义包 `@deepseek-ai/dsh-subagent` import，不从 provider 或 consumer 拿——这是 4.1.3 戒律②的类型级落地。[^c4-S2-4.2]
- **`name`**：provider 在注册表里的身份证。`dsh-tool-subagent` 的 `config.provider` 字段拿它当值（例如配 `provider: my-provider` 就调到你）；`getProvider('my-provider')` 也靠它。重名注册会失败。[^c4-S2-4.2]
- **`capabilities: {}`**：启动期静态声明。空对象是合法声明，意思是「四个可选启动能力我都不支持」。要支持哪个就写哪个（如 `{ outputSchema: true }`）；**不声明却收到对应请求 → `UNSUPPORTED_CAPABILITY` 响亮拒绝**（坑②，见 4.5）。[^c4-S2-4.3]
- **`inheritsParentContext: false`**：描述性标注（第 2 章 §2.2.3 揭开的悬念）。spawn 类（全新 child）写 `false`，fork 类（从父对话种子启动）写 `true`。它只担保「对话种子」，不担保工具/服务/权限。[^c4-S2-4.2]
- **`start()`**：真正干活的地方。输入是 `ResolvedSubagentStartRequest`——服务已经做完能力校验、解析好 descriptor，provider 拿到的不是裸请求。返回 `Promise<SubagentRun>`，**发布后**才 resolve handle；发布前失败要清理未发布资源（坑③）。两条实现路径见 4.3。[^c4-S2-4.2]
- **`prepareContinuable?`（可选）**：**方法存在即能力**——服务端用 TypeScript 类型收窄发现「这 provider 支持续写」，不是查开关字段。它只返回 `ContinuableCreateSpec`（目前仅可选父历史种子 `seed`），不含 Agent/handle/投递/结果/dispose/恢复——那些归服务管。不写这个方法的 provider 只服务 one-shot 委托。[^c4-S3-4.2-5]
- **`export const name` + `export function apply(ctx)`**：cordis 插件入口约定。`apply` 是必须的入口；`name` 是可选元数据。注意这里有两个「name」容易混：包级的 `export const name` 是插件名，provider 对象里的 `name` 是注册名——别写串。
- **`ctx.subagents.registerProvider(myProvider)`**：把 provider 挂上注册表。因为写在 `apply` 的插件作用域里，**effect-scoped**——插件卸载时自动注销（4.4 展开）。[^c4-S2-4.2]

> [!tip] 大白话
> 把这份骨架想成「入职登记表」：`name` 是工号（唯一），`capabilities` 是写在胸牌背面的「我会什么」（没写的能力就别说会），`inheritsParentContext` 是「要不要带旧公司的交接文档」，`start()` 是「入职第一天真正开始干活」。所以……骨架的核心不是「写对每一行」，而是「把每行当成一次对服务端的承诺」——承诺了能力就得兑现，没承诺的请求会被当场拒绝。

### 4.3 start() 的两条实现路径：in-process 与 out-of-process

`start()` 的写法取决于 child 跑在哪：同一个进程，还是独立子进程。这两条路径是第 3 章「in-process vs out-of-process 大分流」在 provider 写作侧的对应物。[^c4-S8][^c4-S5][^c4-S6]

| 维度 | in-process | out-of-process |
| --- | --- | --- |
| child 在哪 | 同进程，经 `ctx.agents` 创建 | 独立子进程 |
| 握手 | 无（同进程直接调用） | 有：ACP `initialize` / SDK `initialize` |
| 启动期能力 | 可全支持（spawn/fork 四项全开） | 通常全 false（无法远程强制） |
| 继承父上下文 | fork 可带对话种子 | 每次全新进程，无继承 |
| 成本 | 低 | 高（dsh-sdk 起完整 peer harness 更贵） |
| 典型样板 | `spawn` / `fork` | `acp` / `dsh-sdk` |

### 4.3.1 in-process：经 ctx.agents 创建 child

in-process 的 provider（如 `spawn`）在**同一进程**里经 `ctx.agents` 创建 child。[^c4-S8] 因为是同进程，child 可以直接访问宿主进程里的服务、工具、注册表，所以 spawn 能把四个启动期能力**全开**（结构化输出、深度强制、工具过滤、persona 都是「进程内能强制」的事）。[^c4-S8] 骨架里那句 `// in-process：经 ctx.agents 创建 child` 对应的就是这条路。

这一步的精确 API（`ctx.agents` 怎么调、child 怎么发布成 `SubagentRun`）官方没有独立教程，**必须对照 `subagent-spawn-in-process` 源码核实**——这正是发布前要做的核实动作。[^c4-6.1] 方向性语义 S2 已经给足：child 建立后要先「发布」到运行状态，然后才 resolve `SubagentRun`；发布前失败要清理。[^c4-S2-4.2]

### 4.3.2 out-of-process：spawn 子进程 → 握手

out-of-process 的 provider（`acp` / `dsh-sdk`）走另一条路：[^c4-S5][^c4-S6]

1. **spawn 子进程**：用配置的命令启动一个新进程（`acp` 起一个 ACP 客户端进程，`dsh-sdk` 起一个完整 peer harness runtime）。
2. **握手**：进程起来后先做协议握手——ACP 是 `initialize` 交换协议版本与能力；SDK 是 stdio JSON-RPC 的 initialize。握手之后才能开始委派 turn。
3. **返回 run**：握手成功后把「会话句柄」封装成 `SubagentRun` 返回。

因为能力被「远程化」了，out-of-process 的 provider **启动期能力通常全 false**——你没法在子进程外强制它的深度/过滤/persona/结构化输出。[^c4-S5-4.7-3] 这也解释了第 2 章的能力表：`acp` 不声明任何 start-time capabilities，本地服务收到带这些选项的请求会拒绝而非静默忽略。

两个 out-of-process 的工程细节（写 provider 时照抄）：[^c4-S5-4.7-6][^c4-S5-4.7-7][^c4-S6-4.7-6][^c4-S6-4.7-7]

- **环境变量卫生**：子进程环境先**擦除「凭据形状」的变量与陈旧的 `DSH_*` 名**，再合并显式 `config.env`——避免把宿主进程的敏感环境意外泄漏给子进程。
- **cwd 规则**：配置了 `cwd` 就用配置值（load 时校验一次）；没配就用**委托方父会话的 cwd**——**绝不用 server 进程自身的 cwd**。子进程跑在哪个目录是委托语义的一部分，不能想当然。

> [!tip] 大白话
> 把 in-process vs out-of-process 想成「在自己家做饭 vs 点外卖」：自己家做饭（in-process），锅碗瓢盆都是现成的，想做多精细都行（能力全开），但得自己动手；点外卖（out-of-process），得先下单选店（spawn 子进程）、确认接单（握手 initialize）、到了才能吃，而且「要几分辣」这种精细要求（能力）很多店做不了。所以……要能力全选 in-process（spawn/fork），要隔离或驱动外部协议选 out-of-process（acp/dsh-sdk）。

### 4.4 registerProvider：effect-scoped 注册与卸载

骨架里 `apply(ctx)` 内的 `ctx.subagents.registerProvider(myProvider)` 不是普通 map 赋值，而是挂在**当前 cordis effect 作用域**上的注册（第 2 章 §2.1.1 讲过语义）。[^c4-S2-4.1]

对写 provider 的人，这带来一个免费福利：**你不需要写任何「注销」代码**。插件被卸载（手动停、热重载、生命周期结束）时，注册跟着 effect 作用域一起撤销。对应的语义是：

- **移除 provider**（effect 结束）：阻止**新的** start 请求，但**不撤销已经返回的 run**——已经跑起来的 child 继续跑到自然结束。
- 所以「卸载」不是「立即杀死」，是「不再接受新委托」。

这一点也呼应第 1 章「微内核主张」：你的 provider 只是挂在一个已文档化扩展点上的监听者，挂多久、什么时候摘，由 effect 生命周期说了算。

> [!note] 这在 Claude Code 里相当于
> Claude Code 里删掉 `.claude/agents/*.md` 文件，subagent 就消失了；dsh 里「卸载」由插件生命周期自动处理，且效果更温和——已派出去的 run 不会被连坐杀掉，跑完才结束。

### 4.5 三个坑：写 provider 必踩

写 provider 有三个已知坑，前两个在写之前就该知道，第三个是写 `start()` 时的卫生纪律。[^c4-S5-4.9-4][^c4-S6-4.9-4][^c4-S2-4.2]

### 坑① 无默认导出：Cordis loader 解包会隐藏命名 inject 元数据

> [!warning] 埋坑 ①：subagent 相关包无默认导出
> subagent 相关包**没有默认导出**。Cordis loader 解包时，默认导出会把命名 `inject` 元数据藏起来（postmortem 0001 记录过这个坑）。所以写 consumer/provider 包时：**只用命名导出**（`export const name`、`export const inject`、`export function apply`），不要 `export default`。`inject` 尤其关键——loader 靠它知道要注入哪些服务，写成默认导出就看不见了。[^c4-S5-4.9-4][^c4-S6-4.9-4]

### 坑② capabilities 不声明 → UNSUPPORTED_CAPABILITY

> [!warning] 埋坑 ②：capabilities 不声明 = 请求被拒
> `capabilities` 是启动期**静态声明**。你 `capabilities: {}` 留空，就等于承诺「四个可选能力我都不支持」；这时任何带 `outputSchema` / `maxDepth` / `toolFilter` / `persona` 的 start 请求都会被 `UNSUPPORTED_CAPABILITY` 响亮拒绝（第 2 章 §2.3.1）。想支持哪个，就声明哪个并真正兑现——「声明了却不实现」和「没声明却被请求」都是 bug。[^c4-S2-4.3]

### 坑③ start() 发布前失败必须清理未发布部分资源

> [!warning] 埋坑 ③：发布前失败不得留孤儿
> `start()` 的语义是「先发布 child，再 resolve handle」。如果 child 还没发布成功就失败，**必须把已经创建的那部分资源清理掉再 reject**——比如你已经 spawn 了子进程，却在握手阶段出错，那就得把子进程 dispose/kill，不能让它变成孤儿进程。官方把「fulfill 前失败须清理未发布部分资源」写成硬性要求，不是建议。[^c4-S2-4.2]

> [!tip] 大白话
> 把坑③想成「装修被叫停」：你装了一半（创建了子进程/child），突然发现手续不全（握手/初始化失败），这时候不能扭头就走留下半拉子工地——得把已经装的部分拆掉还原（dispose），再跟业主说做不了。所以……`start()` 里「先分配后发布」的资源，每一份都要有对应的失败清理路径，一个都不能漏。

### 4.6 从 Claude Code subagent 迁移映射

这一章最后，把「写 dsh provider」映射回你最熟的 Claude Code 侧。Claude Code 里你「自定义 subagent + 脚本工具」做的事，到 dsh 被拆成了 provider 插件 + 工具实例。

| Claude Code | DeepSeek-Harness |
| --- | --- |
| `.claude/agents/*.md` 角色文件（description + system prompt） | `SubagentProvider` 契约对象（`name` + `capabilities` + `start()` 里把 prompt 交给 child） |
| 框架从文件自动发现 subagent | 显式 `ctx.subagents.registerProvider` + cordis 插件挂载（`cordis.patch.yml`）[^c4-S4-4.9-1] |
| md 里限制可用工具（`tools:`） | `capabilities.toolFilter` + `agentOptions` / `toolFilter` 选项 |
| 模型通过 `task` 工具调用 subagent | `dsh-tool-subagent`（`config: { provider: 你的name }`）绑定你的 provider |
| 「运行」由框架内置执行器完成 | 你的 `start()` 实现（in-process / out-of-process） |
| 脚本工具 = 一个可执行入口 | consumer 包里的 `defineTool` + `ctx.tools.register` |

迁移心智一句话：**Claude Code 的 md 角色声明对应 dsh 的 `SubagentProvider` 契约声明**，但 dsh 把「角色声明」「执行引擎」「调用入口」拆成了三段——你在 Claude Code 里只写 md（声明），框架替你跑；在 dsh 里你得自己写 `start()`（执行引擎），再用现成的 `dsh-tool-subagent` 当调用入口。Claude Code 帮你隐掉的「执行」这一段，正是 dsh 换后端只改一行配置的前提。[^c4-S4-4.9-1]

具体落地到「迁移一个现有 Claude Code subagent」：

1. 把 md 里的**角色名** → provider 的 `name`。
2. 把 md 里声明的**能力 / 工具限制** → `capabilities` + 启动时按 `request.agentOptions` / `toolFilter` 施加约束。
3. 把 md 里的**system prompt** → `start()` 创建 child 时注入的 prompt（配合 `request.prompt`）。
4. 把「模型怎么叫它」→ 复用 `dsh-tool-subagent`，`config.provider` 指到你的 `name`。

这一步映射做完，你对「写 dsh provider」的心智就和「写 Claude Code subagent」对上了——只是多了一层你要自己实现的 `start()`。挂载与配置细节（`cordis.patch.yml` 怎么插）见 [[DeepSeek-Harness 配置体系]] 与第 3 章。

### 本章小结

- 三段式方法论：① 定义包（抽象 Service 类 + Request/Result 类型 + `declare module`）→ ② Provider 实现包（`export function apply(ctx){ ctx.plugin(...) }`）→ ③ Consumer/Tool（`inject: ['tools','cap']` + `defineTool` + `ctx.tools.register`）；命名律 `dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>`。
- 三条设计戒律：Do not split preemptively（角色独立演进才拆包）；Request/Result 类型归定义包所有；默认值在显式 `resolve` 里处理，不在 `run()` 藏 `?? default`。
- 最小 provider 骨架 = `name` / `capabilities` / `inheritsParentContext` / `start()` / 可选 `prepareContinuable` + `apply` 里 `ctx.subagents.registerProvider`。骨架为 S2+S4 **综合推断**，`start()` 发布前须对照 `subagent-spawn-in-process` 源码核实。
- `start()` 两条路径：in-process（经 `ctx.agents` 同进程创建 child，能力可全开）vs out-of-process（spawn 子进程 → ACP/SDK initialize 握手 → 返回 run，能力通常全 false；注意环境变量卫生与 cwd 规则）。
- `registerProvider` 是 effect-scoped 注册：插件卸载自动注销，移除阻止新 start、不撤销已返回 run。
- 三个坑：① 无默认导出（loader 解包藏 inject 元数据）② capabilities 不声明 → UNSUPPORTED_CAPABILITY ③ start() 发布前失败必须清理未发布资源。
- Claude Code 迁移：md 角色声明 = SubagentProvider 契约声明；执行引擎从「框架内置」变成「你的 start()」。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 声明 subagent | `.claude/agents/*.md` 一个角色文件 | `SubagentProvider` 对象 + `registerProvider` |
| 能力约束 | md frontmatter 隐含 | `capabilities` 四 flag 静态声明，缺则拒 |
| 执行引擎 | 框架内置，不可换 | 你的 `start()`，可选 in-process / out-of-process |
| 模型调用面 | 框架自动暴露 | `dsh-tool-subagent`（`config.provider` 绑定） |
| 脚本工具 | 可执行入口 | `defineTool` + `ctx.tools.register` |
| 卸载/清理 | 文件删除即消失 | effect-scoped 自动注销，但已跑 run 不撤销 |

迁移心智：Claude Code 把「声明 + 执行 + 调用面」压进一个 md 文件，框架替你跑；dsh 把它们拆成三段，执行那段要你亲自写 `start()`。代价是更陡的起步曲线，收益是执行后端从「不可换」变成「配置一个字符串」——你在 Claude Code 里写自定义 subagent 的心智（角色声明），正好对应 dsh 的契约声明，只是多了「实现执行」这一层。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档撰写。4.2 最小骨架为 **S2 契约 + S4 三段式综合推断**，官方无独立 SubagentProvider 教程；发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码核实 `start()` 的 in-process 实现。若 preview 更新改变三段式命名律、`SubagentProvider` 字段或 postmortem 0001 结论，本章 4.1-4.2、4.5 受影响，优先对照检查。

---

[^c4-S4-4.9-1]: S4 · Three-role capability design §4.9-1——三段式三步走（定义包 → Provider → Consumer/Tool，含 `inject` + `defineTool` + `ctx.tools.register`）。
[^c4-S4-4.9-2]: S4 §4.9-2——命名律（`dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>`）。
[^c4-S4-4.9-3]: S4 §4.9-3——设计要点（Do not split preemptively、Request/Result 类型归定义包、默认值在显式 resolve）。
[^c4-S2-4.1]: S2 · Subagent 子系统设计文档（中文）§4.1——`ctx.subagents` 注册表（registerProvider effect-scoped、移除阻止新 start、不撤销已返回 run）。
[^c4-S2-4.2]: S2 §4.2——SubagentProvider 契约（name/capabilities/inheritsParentContext/start、发布后返回 handle、发布前失败清理）。
[^c4-S2-4.3]: S2 §4.3——SubagentStartRequest 选项与能力检查（UNSUPPORTED_CAPABILITY 响亮失败）。
[^c4-S3-4.2-5]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.2-5——prepareContinuable 存在即能力、只返回 ContinuableCreateSpec、冷恢复不经 provider 分发。
[^c4-S8]: S8 · `subagent-spawn-in-process` README——in-process provider 样板（ctx.agents 创建 child、启动期能力全支持）。
[^c4-S5]: S5 · `dsh-subagent-acp` README——out-of-process provider 样板（ACP 客户端驱动、initialize 握手）。
[^c4-S5-4.7-3]: S5 §4.7-3——acp 不声明任何 start-time capabilities，本地服务拒绝而非静默忽略。
[^c4-S5-4.7-6]: S5 §4.7-6——环境变量卫生（先擦除凭据形状变量与陈旧 `DSH_*` 名，再合并 `config.env`）。
[^c4-S5-4.7-7]: S5 §4.7-7——cwd 规则（配置值或委托方父会话 cwd，绝不用 server 进程自身 cwd）。
[^c4-S5-4.9-4]: S5 §4.9-4——subagent 相关包无默认导出（Cordis loader 解包隐藏命名 `inject` 元数据，postmortem 0001）。
[^c4-S6]: S6 · `dsh-subagent-dsh-sdk` README——out-of-process provider 样板（stdio JSON-RPC 驱动、完整 peer harness、initialize 握手）。
[^c4-S6-4.7-6]: S6 §4.7-6——环境变量卫生（同上，dsh-sdk 侧）。
[^c4-S6-4.7-7]: S6 §4.7-7——cwd 规则（同上，dsh-sdk 侧）。
[^c4-S6-4.9-4]: S6 §4.9-4——无默认导出坑（同上，dsh-sdk 侧）。
[^c4-6.1]: 实操指南 6.1——最小 provider 骨架（S2+S4 综合推断，发布前对照 spawn-in-process 源码核实）。
[^c4-6.2]: 实操指南 6.2——S4 官方 my-cap 三件套示例。

---

> provider 能自己写了，但委托的生命周期还有一条更长的路——one-shot 之外还有可持续恢复的 continuable。这一章讲生命周期深度与委派深度。

## 第五章 生命周期深度——one-shot / continuable 与委派深度

> [!summary] 导读
> 第 2 章结尾留下了两条尾巴：`SubagentRun` 是一次性委托、用完要 dispose；而 `prepareContinuable`「存在即能力」意味着还有一条更长的生命周期。这一章把这两条路讲透：一次委托到底是一次性（one-shot）还是可持续（continuable）？可恢复 child 从出生（`startContinuable`）到继续执行（`followup`）、停止（`interrupt`）、反向上报（`reportFrom`）四个动作各是什么语义？以及贯穿始终的委派深度（delegationDepth）是怎么记账、怎么设限、为什么冷恢复降不下来深度。读完你会理解「持久化子代理」和「一次性 task」的本质差别，也能看懂 `maxDepth`、`'provider-managed'` 这些配置背后的机制。

### 5.1 两条生命周期：one-shot 与 continuable

dsh 的委托分成两个家族：[^c5-S2-4.6]

- **one-shot（一次性）**：建一个 child、跑一轮、拿结果、收尾。它**默认前台**执行——调用方 await 结果；也可以配置为**后台**运行（`enableRunInBackground` + `backgroundMode`），把结果异步回传（后台 one-shot 的结果走 task 工具那条路，第 6 章展开）。
- **continuable（可持续）**：建一个**持久化、可恢复**的 child。它不随一轮结束而消失，可以在之后被 `followup` 续写、被 `interrupt` 停止、并允许 child 通过 `reportFrom` 反向汇报。

一句话分界：**one-shot 是「派单 → 收货」，continuable 是「开一扇长期往来的门」。**

> [!tip] 大白话
> 把 one-shot 想成打一次车：下单、到目的地、下车、结账，交易结束。把 continuable 想成你雇了一个长期助理：今天交个任务，明天再补一句，随时可以叫停，助理也能主动向你汇报。所以……one-shot 适合「一次问答一次结果」，continuable 适合「一个任务要反复推进、甚至跨会话」的场景。

第 2 章讲过，这两种 child 走 provider 的不同入口：one-shot 走 `SubagentProvider.start()`；continuable 走 `prepareContinuable`——**可继续 child 绝不会到达 `start()`**。[^c5-S2-4.2] 接下来看 continuable 这条路的四个编排 API。

### 5.2 continuable 编排四 API 语义

continuable 的编排集中在 `ctx.subagents` 上，四个方法各管一件事：[^c5-S2-4.6]

| 方法 | 方向 | 一句话职责 |
| --- | --- | --- |
| `startContinuable(spec)` | parent → child | 建立持久 child 并投递初始 prompt |
| `followup(parent, childId, content, options)` | parent → child | 唯一继续执行消息操作 |
| `interrupt(targetSessionId, authority)` | 任意 → child | 唯一公开停止操作 |
| `reportFrom(child, content, options)` | child → parent | 可继续 child 向直接 parent 上报 |

### 5.2.1 startContinuable：收件箱准入即 resolve

`startContinuable` 建立持久 child 并投递初始 prompt。它的 resolve 时机很特别：[^c5-S2-4.6][^c5-S3-4.6]

> 收件箱准入即 resolve 出 `{childId, messageId}`，**不等待轮次开始**。

也就是说，`startContinuable` 的返回不代表「child 已经回答了什么」，只代表「这条消息已经被 child 的收件箱接受、这笔账记上了」。轮次什么时候跑、跑成什么样，是之后的事。这个「先确认入账、不等待执行」的语义，是它和 `start` 的根本区别——`start` 是前台等结果，`startContinuable` 是「投递即回执」。

### 5.2.2 followup：唯一继续执行消息操作

`followup(parent, childId, content, options)` 是「唯一继续执行消息操作」——想让一个 continuable child 继续干，只有这一条路。它的路由只看 **Activation 状态**：[^c5-S2-4.6]

| child 当前 Activation 状态 | followup 的行为 |
| --- | --- |
| running（正在跑） | **入队**，等当前轮次结束再处理 |
| waiting（在等消息） | **唤醒**，直接进入新轮次 |
| 无 Activation（冷态/未被加载） | **冷恢复**，先把 child 从持久化恢复再处理 |

注意「只看 Activation 状态」这个措辞：followup 不查消息队列、不查历史，就根据 child 现在「活没活、在不在跑」决定怎么投递。

### 5.2.3 interrupt：唯一公开停止操作

`interrupt(targetSessionId, authority)` 是「唯一公开停止操作」。语义有三条：[^c5-S2-4.6][^c5-S3-4.6]

- **同步鉴权后**发 `Agent.cancel(cause, { keepInbox: true })`——`keepInbox: true` 表示保留收件箱，为将来恢复留门；
- **不等停稳即返回**：它不等待 child 真正停下来，而是「发令」即返回；
- **不存在目标为无害 no-op**：interrupt 一个不存在的 child 不会报错，是一个无害的空操作。

> [!warning] 埋坑 ③（之一）：interrupt 是「发令」不是「等到停」
> `interrupt` 不等 child 完全停稳就返回，别把它当「同步停止」。如果你需要「确认停稳」之后的动作，得靠自己轮询/订阅后续状态——这在 Claude Code 里几乎不会出现，因为那里没有「可持久恢复的 child」这个概念。

### 5.2.4 reportFrom：child 向直接 parent 上报

`reportFrom(child, content, options)` 是可继续 child 向**直接 parent** 上报的方向工具。语义要点：[^c5-S2-4.6]

> **child 是权威凭证，调用方不能指定接收方。**

也就是说，`reportFrom` 的第一个参数是 child（凭证），上报的目的地由「child 的直接 parent」决定，调用方没有权利指定「我要发给谁」。这个「不能指定接收方」的约束，和 `followup` 里「要确切存活直接父代」的限制是一体的（见 5.4）。

> [!tip] 大白话
> 把 `reportFrom` 想成孩子给家长写纸条：纸条上写「家长收」，但谁是这个孩子的家长是登记好的，你不能替孩子指定「把纸条递给隔壁王叔叔」。所以……上报方向是系统按父子关系钉死的，调用方只能决定「报什么」，不能决定「报给谁」。

### 5.2.5 语义示意（非可运行代码）

以下不是可运行代码，只是把四个 API 的调用语义画出来，帮助你建立「谁调谁、带什么、何时返回」的坐标（S2/S3 语义示意）：[^c5-S2-4.6]

```ts
// ① 建立持久 child：投递即回执，不等待轮次开始
const { childId, messageId } = await ctx.subagents.startContinuable({
  provider: 'spawn',        // 走支持 prepareContinuable 的 provider
  prompt: [{ type: 'text', text: '长期跟进：调研 X 方案' }],
  // ... 其余同 SubagentStartRequest 选项
})

// ② 继续执行：按 Activation 状态路由（running 入队 / waiting 唤醒 / 冷恢复）
await ctx.subagents.followup(
  currentSession,           // 直接父代（必须确切存活）
  childId,
  [{ type: 'text', text: '上一条结论太粗，给一份明细' }],
)

// ③ 停止：同步鉴权后发 cancel(keepInbox:true)，不等停稳即返回
await ctx.subagents.interrupt(targetSessionId, {
  authority: { type: 'human', sessionId: '...' },  // 只有 interrupt 接受 human 权威
})

// ④ child 侧反向上报：child 是权威凭证，接收方由系统按直接父代决定
await ctx.subagents.reportFrom(child, [
  { type: 'text', text: '第一阶段完成，等你下一步指令' },
])
```

### 5.3 委派深度：双重表示、只能增、不能降

委派深度（delegation depth）是「这个 child 在委派树里离根有多远」的记账。dsh 用**双重表示**管理它：[^c5-S2-4.5]

| 字段 | 位置 | 性质 |
| --- | --- | --- |
| `SessionHeader.delegationDepth` | 持久化会话头 | 持久表示 |
| `AgentOptions.subagentDepth` | 运行时 agent 选项 | 运行时字段 |

- 两者都**缺失** = 顶层（深度 0）。
- 两者**都存在时，较大的值权威**。
- 两个字段都归 subagent 这个能力缝（seam）所有，**agent loop 不读不写**——这是第 1 章「微内核」主张的又一次体现：核心循环不掺和委派深度的记账，它只是被 seam 维护的一个数据。呼应第 2 章的 `subagent/start` / `subagent/end` 事件：`end` 按委派 parent scope 过滤分发，这个 scope 和委派深度是同一套父子账本——监听者只关心自己委派链上的结束事件。[^c5-S2-4.1]

深度只会往深里走：

- **进程内 child 持久保存 parent 深度 + 1**。[^c5-S2-4.5]
- **冷恢复无法降低深度**。[^c5-S2-4.5]

> [!warning] 埋坑 ①：冷恢复无法降低委派深度
> 「冷恢复」只是把持久化的 child 重新加载，深度是从会话头里读回来的——它不会因为你「重启了一次进程」就归零。所以不要指望「冷启动一次 = 深度重置」。深度只会被父级 +1，恢复时原样读回，想降低只能换一条新的委派链。

深度还有上界校验：**每次 start 都会拒绝两类派生深度**——超出安全整数域的深度，以及高于绝对 `request.maxDepth` 的深度。[^c5-S2-4.5]

### 5.3.1 maxDepth：默认 3、0 禁止、'provider-managed' 特例

`maxDepth` 是绝对委派深度上限，来自 `dsh-tool-subagent` 的配置：[^c5-S7-4.5]

- **默认 3**；
- **`0` 禁止委派**（这个 child 不能再往下派）；
- 在 **dsh-sdk** provider 上部署时，设 `maxDepth: 'provider-managed'`——表示**子 harness 自己管理递归预算**，父级不施加限制。[^c5-S6-4.5]

> [!tip] 大白话
> 把委派深度想成「转包链的长度」：默认最多允许 3 层转包；`maxDepth: 0` 等于「这单不许再转包」；`'provider-managed'` 等于「把发包方换成包工头自己管——他说能转几层就几层」。所以……默认 3 是「防失控转包」的安全阀，`'provider-managed'` 是你明确信任某个 provider 完全自治时才用的开关。

结合第 2 章：`maxDepth` 要求 `depthLimit` 能力（acp/dsh-sdk 不声明 start-time capabilities，所以「强制深度」这种能力只有 spawn/fork 这种 in-process provider 提供）。[^c5-S2-4.3] 这里同样适用「能力不匹配响亮失败」的规则。

### 5.4 已知限制与社区经验

continuable 是 developer preview 里的新机制，官方明确了一批限制，写进自己的系统前必须先知道：[^c5-S3-4.6]

1. **无 host-user 续写**：`followup` 要求**确切存活的直接父代**——你没法「代父代发起续写」，也没有「宿主用户直接续写 child」的路。**只有 `interrupt` 接受持久父地址的 human 权威**。
2. **不能转向当前 turn**：续写消息/唤醒型 report 只**入队后续 turn**，不能插入当前正在跑的轮次。
3. **驻留仅限进程本地**：Activation inbox 与所有权图**不跨进程协调**；多进程并发访问同一持久化库，仍需要**持久 mailbox + 跨进程租约协议**自行保证。
4. **已接受但未落日志的消息不可重放**；并且**没有持久 report 邮箱**——`reportFrom` 要成功，目标直接父代必须存活。
5. **跨进程 continuable ownership 官方「未设计」**。[^c5-C2]

> [!warning] 埋坑 ②：消息不可重放 + report 需存活直接父代
> 「已接受但未落日志的消息不可重放」——`startContinuable`/`followup` 返回的 `messageId` 只能当「入账凭证」，不代表这条消息已经进了可回放的日志。系统崩溃后，这笔账可能就没了，别指望重放恢复。同样地，`reportFrom` 没有持久邮箱，父代一旦不存活，上报就投不出去——所以「先确认直接父代活着，再让 child 上报」是编排方要自己保证的。

### 5.4.1 社区经验：dsh-background-agents（仅作标注）

跨进程的持久化续跑，官方「未设计」。[^c5-C2] 社区有一个补强方案 **dsh-background-agents**（PerryLink）试图补齐「后台续跑子代理」这块。[^c5-C2]

> [!warning] 埋坑 ③：跨进程 continuable ownership 官方未设计
> 这是「未设计」，不是「未实现好」——官方没有给出跨进程谁拥有、谁恢复、怎么防双写的契约。社区方案只能作为经验参考（C2 标注），**不能当成官方能力**写进生产设计。真要跨进程，官方建议自己上「持久 mailbox + 租约」这套通用原语（见 5.4 第 3 条）。

### 本章小结

- 两条生命周期：one-shot（前台默认 / 后台 `enableRunInBackground`+`backgroundMode`）与 continuable（持久化可恢复 child）；continuable 走 `prepareContinuable`，不经过 `start()`。
- 四 API 语义：`startContinuable` 收件箱准入即 resolve（不等轮次开始）；`followup` 唯一续写、按 Activation 路由（running 入队 / waiting 唤醒 / 冷恢复）；`interrupt` 唯一停止、同步鉴权后发 cancel(keepInbox:true)、不等停稳、不存在目标为无害 no-op；`reportFrom` child 向直接父代上报、child 是权威凭证、调用方不能指定接收方。
- 委派深度双重表示（持久 `SessionHeader.delegationDepth` + 运行时 `AgentOptions.subagentDepth`，较大值权威，归 seam 不归 loop）；进程内 child 保存 parent+1；冷恢复无法降低深度；start 校验安全整数域与 `maxDepth` 上界。
- `maxDepth` 默认 3、`0` 禁止委派；dsh-sdk 上 `'provider-managed'` 表示子 harness 自管递归预算。
- 已知限制：无 host-user 续写（followup 要确切存活直接父代，只有 interrupt 接受 human 权威）；不能转向当前 turn；驻留仅进程本地（跨进程要持久 mailbox + 租约）；跨进程 ownership 官方「未设计」，dsh-background-agents 仅社区经验标注。
- 埋的坑：① 冷恢复无法降低深度 ② 已接受未落日志的消息不可重放、report 需存活直接父代 ③ 跨进程 continuable ownership 官方未设计。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 委派形态 | 一次性 `task` 委派，结果即返回 | one-shot（前台/后台）+ continuable（持久可恢复）两族 |
| 续写 | 无持久续写——每次 task 重新派 | `followup` 唯一续写，按 Activation 状态路由 |
| 停止 | 取消当前调用即止 | `interrupt` 唯一停止，发 cancel(keepInbox:true) 不等停稳 |
| 反向上报 | 无独立方向工具 | `reportFrom` child 向直接父代上报，方向由父子关系钉死 |
| 深度控制 | 无显式委派深度记账 | `delegationDepth`/`subagentDepth` 双重表示 + `maxDepth` 上限（默认 3、0 禁止、`'provider-managed'` 特例） |

迁移心智：Claude Code 的 subagent 心智是「一次 task = 一次结果，用完即焚」；dsh 的 continuable 把「子代理」从一次性工具升级成了**有状态的工作对象**——能续写、能叫停、能反向汇报、有委派深度记账。你在 Claude Code 里习惯的「派一次、收一次」对应 dsh 的 one-shot 路；如果你需要「一个长期推进的子任务」，dsh 的 continuable + followup/interrupt 是 Claude Code 目前没有的编排面。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方子系统文档（S2 §4.6/§4.5）、核心包 README（S3 §4.6）、工具 README（S7 §4.5、S6 §4.5）撰写。continuable 编排四 API 与委派深度机制均出自官方契约；`dsh-background-agents`（C2）仅作社区经验标注，非官方能力。若 preview 更新改动 `followup` 路由规则、`interrupt` 语义或深度字段，本章 5.2-5.4 受影响，优先对照检查。

---

[^c5-S2-4.6]: S2 · Subagent 子系统设计文档（中文）§4.6——one-shot vs continuable、startContinuable/followup/interrupt/reportFrom 语义。
[^c5-S3-4.6]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.6——无 host-user 续写、不能转向当前 turn、驻留仅进程本地、已接受未落日志不可重放、无持久 report 邮箱。
[^c5-S2-4.5]: S2 §4.5——委派深度双重表示、进程内 parent+1、冷恢复无法降低深度、上界校验。
[^c5-S7-4.5]: S7 · `dsh-tool-subagent` README §4.5——maxDepth 默认 3、0 禁止委派。
[^c5-S6-4.5]: S6 · `dsh-subagent-dsh-sdk` README §4.5——`maxDepth: 'provider-managed'` 子 harness 自管递归预算。
[^c5-S2-4.1]: S2 §4.1——核心方法总览与 `subagent/start|end` 事件按委派 parent scope 过滤分发。
[^c5-S2-4.2]: S2 §4.2——prepareContinuable 存在即能力；可继续 child 不到达 start()。
[^c5-S2-4.3]: S2 §4.3——maxDepth 要求 depthLimit 能力。
[^c5-C2]: C2 · dsh-background-agents（PerryLink，社区）——跨进程后台续跑子代理补强；官方「未设计」，仅作经验标注。
> 生命周期理清了，模型却还「摸不到」provider——它只是后台实现，模型能调用的只有工具。这一章把 provider 暴露成模型可调能力，接上全局控制、反向汇报与委托沙箱策略。

## 第六章 工具化——把 provider 暴露成模型可调能力

> [!summary] 导读
> 前面几章把 provider 写好、把生命周期理清，但模型还是「摸不到」它——provider 只是后台实现，模型能调用的只有工具。这一章接上最后一段：用 `dsh-tool-subagent` 把一个 provider 包成模型可见的工具，用 `-control` 拿到全局控制权，用 `-report` 打通 child 反向汇报，并讲清委托时 sandbox 策略为什么会被「钉死」成确定性拒绝。读完你会得到一张「provider + tool + control/report」三件套的完整接线图，能把第 3 章挂载的 provider 真正暴露给模型用，也看得懂为什么子代理永远不会「卡在等人审批」上。

### 6.1 `dsh-tool-subagent`：一个 provider 绑一个 toolName

`dsh-tool-subagent` 是三层结构里的 Consumer/Tool 层：它的职责是把**某一个** provider 包装成模型能调的工具。[^c6-S7-4.8-1] 它是 dsh 内置 `dsh-tool-*` 家族的一员——这个家族还有 `bash` / `fs` / `web` / `todo`，subagent 跟它们平级，都是「把某个能力暴露成模型工具」的消费层。[^c6-S10-4.8-4] 记住它的核心设计一句话：**一个 tool-subagent 实例，绑定一个 provider，暴露成一个 toolName。**

- **绑定一个 provider**：`config.provider` 是必填字段，值就是 provider 的注册名（`acp` / `spawn` / `fork` / `dsh-sdk`…）。一个实例只服务一个 provider，不搞「一个工具背后轮询多家」。
- **暴露成一个 toolName**：模型看到的工具名由 `config.toolName` 决定，默认是 `subagent`。工具名在**全局工具注册表里必须唯一**——这也是埋坑 ① 的来源。
- 想同时暴露两个 provider？那就开**两个** tool-subagent 实例，各绑一个 provider、各取一个不重名的 toolName。

> [!tip] 大白话
> 把每个 tool-subagent 实例想成给模型发的一张**临时工牌**：工牌上印着「你只能找 acp 这位同事」（一个 provider 绑一个 toolName），而且全公司工牌号不能重号（全局唯一）。所以……想同时暴露 acp 和 spawn 两个 provider，就得发两张不同工号的工牌（不同 toolName），不能两个人都挂同一张「subagent」牌。

### 6.1.1 config 全字段

`dsh-tool-subagent` 的 config 全部字段如下（字段名与 `SubagentStartRequest` 选项一一呼应，第 2 章的能力检查在这里就是「把请求选项写进配置」）：[^c6-S7-4.8-1]

| config 字段 | 必填 | 默认 | 作用 |
| --- | --- | --- | --- |
| `provider` | ✅ | — | 绑定哪个已注册 provider，值 = provider 的 `name`（如 `acp`） |
| `toolName` | — | `subagent` | 模型可见的工具名，**全局唯一** |
| `enableRunInBackground` | — | `false` | 是否允许 one-shot 后台运行（不阻塞当前 turn） |
| `backgroundMode` | — | `one-shot` | 后台模式：`one-shot` 一次性 / `continuable` 持久可恢复 |
| `agentOptions` | — | — | 透传给子代理的运行选项（如深度相关字段） |
| `persona` | — | — | 为 child 遮蔽部署 persona（要求 provider 有 `persona` 能力） |
| `toolFilter` | — | — | 命名工具过滤（要求 provider 有 `toolFilter` 能力） |
| `maxDepth` | — | `3` | 委派深度上限；`0` 表示禁止委派 |

`persona` / `toolFilter` / `maxDepth` 三个字段分别要求 provider 声明了对应 `capabilities`（第 2 章 2.2.2），否则启动时被 `UNSUPPORTED_CAPABILITY` 拒绝——这个检查规则在工具配置层同样生效。

> [!warning] 埋坑 ①：重复 toolName 冲突
> 一个 provider 绑一个 toolName，且 toolName 需**全局唯一**。如果你再加一个 tool-subagent 实例、却仍用默认 `toolName: subagent`，工具注册时就会撞名——这跟 `ctx.tools.register` 的重名语义一致，不是「覆盖」，而是失败。想暴露第二个 provider，必须显式改 `toolName`（比如 `subagent_acp` / `subagent_spawn`）。

### 6.1.2 最小配置行

只暴露一个 provider 时，配置可以极简（第 3 章 6.3 底稿就是这么写的）：[^c6-6.3]

```yaml
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config: { provider: acp, toolName: subagent }
```

`provider` 必填，`toolName` 不写就用默认值 `subagent`。第 6.4 节会给一份全字段展开的版本。

### 6.2 控制与汇报：`-control` 三件套 + `-report`

单靠 `dsh-tool-subagent`，模型只能「发起委派」，还不能「管」运行中的 agent、也不能让 child「说回来」。这两件事由两个兄弟工具补齐：[^c6-S9-4.8-2][^c6-S9-4.8-3]

### 6.2.1 `dsh-tool-subagent-control`：全局控制三件套

`dsh-tool-subagent-control` 注册三个**全局控制**工具，方向是「模型 → 任意 agent」，不绑定某个 provider：[^c6-S9-4.8-2]

| 工具名 | 作用 | 对应核心包方法 |
| --- | --- | --- |
| `send_message` | 向一个运行中的 continuable agent 发送消息 | `followup` |
| `interrupt_agent` | 中断一个运行中的 agent | `interrupt` |
| `list_agents` | 枚举当前已知/运行中的 agent | `listChildren` / `listDescendants` |

注意「全局」的定位：`subagent` 工具只能「开新委派」，而这三个工具能跨 provider、跨 child 去发消息、掐断、枚举——是给模型的一台调度台。`send_message` / `interrupt_agent` 的语义细节与第 5 章 `followup` / `interrupt` 的编排规则一致（比如 interrupt 是同步鉴权后发 cancel、不等停稳即返回）。

> [!tip] 大白话
> 把 `-control` 想成**总机**：`list_agents` 是「查分机表」、`send_message` 是「给某个分机转电话」、`interrupt_agent` 是「强行掐断某条线」。所以……它不是给某个 provider 单独用的，而是面向所有运行中 agent 的全局调度台——这跟 6.1 那个「只认一个 provider 的临时工牌」是两种粒度。

### 6.2.2 `dsh-tool-subagent-report`：child→parent 反向汇报

`dsh-tool-subagent-report` 打通的是**反向**方向：child 通过它向自己的**直接 parent** 汇报。[^c6-S9-4.8-3]

- 方向是「child → 直接 parent」，与委派工具（模型 → child）正好相反；这也呼应第 5 章 `reportFrom` 的语义——child 是权威凭证，调用方不能指定接收方。
- 汇报要求**存活的直接父代**（第 5 章 S3-4.6-5：report 需要存活直接父代，无持久 report 邮箱）。

> [!warning] 诚实标注：`-report` 细节待补
> 本分册 P2 只抓到了 `-report` 的**定位**（child→parent 汇报方向，来源 S9-4.8-3），**没有单独抓取 `tool-subagent-report` 包的 README 细节**（字段、示例、与 `reportFrom` 的对应关系）。本节按定位写，具体 config 与调用示例需对照 `packages/subagent/tool-subagent-control/README.md` 家族核实后再补——第 7 章速查里也会把它列进「未抓取项」。

### 6.3 委托沙箱策略：核心包的确定性拒绝

工具层把 provider 暴露给模型之后，还有一个安全面要处理：**子代理在什么权限下运行、能不能向人要更高权限？** 这个策略在核心包（`dsh-subagent`）里实现，三条规则值得单列：[^c6-S3-4.9-5]

1. **快照父的显式 sandbox 覆盖**：`captureDelegatedPolicyOverrides(parent)` 在委托发生时，把父级**显式设置**的 sandbox 覆盖快照下来，作为子代理运行的沙箱基准。注意是「快照那一刻的显式授权」，不是「继承父的整套运行时」——跟第 2 章 `inheritsParentContext` 的克制是同一个味道。
2. **子代理审批策略钉死为 `'never'`**：子代理的审批策略被硬性设为「永不审批」。任何需要人工审批的升级请求（比如 `sandbox_permissions` 提权）都会被**确定性拒绝**，而不是弹出一个提示等人点——因为子代理运行时背后**没有人在看**，等审批提示等于死锁。
3. **`subagent:delegation` 运行时上下文声明越权不重试**：子代理的运行上下文标记 `subagent:delegation`，一旦某次授权越权被拒，**不重试**——拒绝是确定性的，不存在「再试一次说不定就过了」的循环。

把第 3 章 6.3 的 provider 配置翻出来看，你会发现 `permission: reject` 正是这条策略在 provider 侧的落点：acp provider 的 config 里写 `permission: reject`，等于把「审批」这道门从配置层面焊死。[^c6-6.3]

> [!tip] 大白话
> 把子代理想成拿**临时门禁卡**的实习生：卡上写死「无审批权限」。他想进机房（升级 sandbox 权限）——门禁直接拒，而不是呼叫保安（等待人工审批），因为值班室根本没人。所以……「确定性拒绝」不是 bug，是**防死锁设计**：宁可当场说 No，也不让整个委派任务卡在一个无人观看的审批提示上干等。

### 6.4 完整接线示例：provider + tool + control/report 三件套

把 6.1/6.2/6.3 合起来，就是一份「三件套」齐活的 `cordis.patch.yml`。下面以第 3 章 6.3 底稿为骨架扩展：[^c6-6.3]

```yaml
# cordis.patch.yml —— provider + tool + control/report 三件套接线骨架
# 前提：subagent 系列包都是纯 Cordis 插件，先 dsh plugin add 让包可解析，
#       再手动 insert 进插件树（既有配置体系笔记结论）

# ① Provider：acp（out-of-process，独立子进程驱动）
- id: subagent-acp
  name: '@deepseek-ai/dsh-subagent-acp'
  config:
    providerName: acp
    command: node
    args: ['--import', 'tsx', './packages/examples/acp-demo/src/bin.ts']
    permission: reject          # 审批策略钉死 reject：升级请求确定性拒绝（见 6.3）
    env:
      DEEPSEEK_API_KEY: !!js process.env.DEEPSEEK_API_KEY

# ② Consumer/委托工具：把 acp 包成模型可见工具
- id: tool-subagent
  name: '@deepseek-ai/dsh-tool-subagent'
  config:
    provider: acp               # 绑定的 provider 注册名（必填）
    toolName: subagent          # 模型可见工具名，全局唯一
    enableRunInBackground: true # 允许 one-shot 后台运行
    backgroundMode: one-shot    # one-shot | continuable
    maxDepth: 3                 # 默认 3；0 禁止委派

# ③ Consumer/控制工具：全局控制三件套
- id: tool-subagent-control
  name: '@deepseek-ai/dsh-tool-subagent-control'
  config:
    # send_message / interrupt_agent / list_agents 三件套默认注册
    # 具体 config 字段以 README 为准（本分册素材未逐字段收录）

# ④ Consumer/汇报工具：child→parent 反向汇报
- id: tool-subagent-report
  name: '@deepseek-ai/dsh-tool-subagent-report'
  # 细节待补：本分册未单独抓取该包 README（见 6.2 诚实标注）
```

接线要点：

- **换 provider 只改两处**：把 ① 的 provider 条目换成另一个（比如 `dsh-subagent-spawn-in-process`），再把 ② 的 `config.provider` 改成对应注册名。定义层与工具层一行不动——第 1 章「换实现只改一行配置」在这里落地成「换 provider + 改 provider 字段」两处。
- **想暴露第二个 provider**：再复制一份 ②，改 `toolName`（如 `subagent_spawn`），否则撞名（埋坑 ①）。

### 6.4.1 埋坑 ②：maxDepth 的三态

`maxDepth` 有三个状态要分清：[^c6-S7-4.8-1][^c6-S6-4.5-5]

| 值 | 含义 |
| --- | --- |
| 不写 / `3` | 默认 3，子代理最多往下委派 3 层 |
| `0` | **禁止委派**——child 不能再往下派活 |
| `'provider-managed'` | **只在 dsh-sdk 上有效**：表示子 harness 自己管理递归预算，父级不施加上限 |

注意 `'provider-managed'` 不是通用值：它是 dsh-sdk 这种「完整 peer harness」的特权——子进程自管递归预算，父级不越俎代庖。spawn 这类 in-process provider 上别指望它生效（第 5 章 §5#2 的区分在这里收口）。

### 6.4.2 埋坑 ③：后台 one-shot 结果走 task 工具回传

`enableRunInBackground: true` + `backgroundMode: one-shot` 时，委派不阻塞当前 turn——child 在后台跑，结果**不**直接出现在委派处，而是经由 **task 工具**回传。[^c6-S7-4.8-1][^c6-S2-4.6-1] 这对写工具消费方的意义是：

- 别期待「await 工具调用 = 拿到 child 最终输出」；后台 one-shot 的结算路径绕了一圈，结果由 task 工具带回来。
- 如果这个模式对你太绕，前台 one-shot（默认）就是「等结果再回来」的直觉路径——后台是给「不想卡住当前 turn」的场景用的。

### 本章小结

- `dsh-tool-subagent` 把**一个** provider 包成一个模型工具：`provider` 必填、`toolName` 默认 `subagent` 且全局唯一；`enableRunInBackground` / `backgroundMode` / `agentOptions` / `persona` / `toolFilter` / `maxDepth` 是其余 config 字段。
- `dsh-tool-subagent-control` 是全局调度台：`send_message` / `interrupt_agent` / `list_agents` 三件套，方向是「模型 → 任意 agent」。
- `dsh-tool-subagent-report` 打通反向：child → 直接 parent 汇报；本分册只抓了定位、细节待补（诚实标注）。
- 委托沙箱策略三连：快照父显式 sandbox 覆盖（`captureDelegatedPolicyOverrides`）→ 审批钉死 `'never'` → `subagent:delegation` 越权不重试；`permission: reject` 是它在 provider 配置侧的落点。
- 埋了三个坑：① 重复 toolName 撞名 ② `maxDepth` 默认 3、`0` 禁止、`'provider-managed'` 仅 dsh-sdk ③ 后台 one-shot 结果走 task 工具回传，不是「await 即结果」。

下一章把这些坑连同第 2-5 章埋的坑汇总成一张避坑速查表，写作与排错时当索引用。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 委派调用面 | `task` 工具内嵌 subagent 调用 | `dsh-tool-subagent` 把 provider 包成工具，一个 provider 绑一个 toolName |
| 全局控制 | 内置的任务/会话管理 UI | `dsh-tool-subagent-control` 三件套（send_message / interrupt_agent / list_agents） |
| 反向汇报 | 无独立汇报工具，结果经 task 返回 | `dsh-tool-subagent-report`：child → 直接 parent 反向汇报 |
| 后台运行 | `task` 后台任务 | `enableRunInBackground` + `backgroundMode`（one-shot / continuable） |
| 沙箱审批 | 交互式审批提示（有人看） | 审批钉死 `'never'`：无人审批 → 升级请求确定性拒绝 |

迁移心智：Claude Code 里「subagent + task 工具 + 任务管理」是框架收敛在一起的一组能力；dsh 把它们拆成**三个方向**的工具——`subagent` 委派（模型→child）、`control` 全局控制（模型→任意 agent）、`report` 反向汇报（child→parent）。你在 Claude Code 里「发起一个 task、看任务列表、收结果」的心智，到 dsh 要拆成「调 subagent 发起、调 list_agents 看、调 send_message 续写、由 report/task 收口」。安全模型也不同：Claude Code 把审批弹窗给「看着屏幕的人」，dsh 直接假设子代理背后没人，把审批焊死成拒绝——这是「无人值守」假设带来的必然差异。

### 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档撰写。`dsh-tool-subagent` 全字段、`-control` 三件套、委托沙箱策略均引自官方 README/核心包；**`-report` README 细节本分册未抓取，6.2.2 按定位写并标注待补**。若 preview 更新改动工具 config 字段或沙箱策略表述，本章 6.1 / 6.3 是受影响区域，优先对照检查。

---

[^c6-S7-4.8-1]: S7 · `dsh-tool-subagent` README §4.8-1——一个 provider 绑一个 toolName（默认 `subagent`）、config 全字段（provider/toolName/enableRunInBackground/backgroundMode/agentOptions/persona/toolFilter/maxDepth）、maxDepth 默认 3 / 0 禁止委派。
[^c6-S9-4.8-2]: S9 · `tool-subagent-control` / `-report` README §4.8-2——`send_message` / `interrupt_agent` / `list_agents` 全局控制工具。
[^c6-S9-4.8-3]: S9 · `tool-subagent-control` / `-report` README §4.8-3——`dsh-tool-subagent-report` child→parent 汇报方向（本分册未单独抓取细节，见 6.2.2 诚实标注）。
[^c6-S10-4.8-4]: S10 · 扩展 Cookbook §4.8-4——内置 `dsh-tool-*` 家族含 subagent（"bash, fs, web, subagent, todo"），subagent 是消费层工具家族的成员。
[^c6-S3-4.9-5]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.9-5——委托沙箱策略：`captureDelegatedPolicyOverrides(parent)` 快照父显式 sandbox 覆盖、子代理审批钉死 `'never'`（`sandbox_permissions` 等升级请求确定性拒绝）、`subagent:delegation` 运行时上下文声明越权不重试。
[^c6-S2-4.6-1]: S2 · Subagent 子系统设计文档（中文）§4.6-1——one-shot 前台（默认）/ 后台（`enableRunInBackground` + `backgroundMode`）区分；后台结算语义。
[^c6-S6-4.5-5]: S6 · `dsh-subagent-dsh-sdk` README §4.5-5——`maxDepth: 'provider-managed'`：子 harness 自管递归预算，父级不施加。
[^c6-6.3]: 02 深度研究 §6.3——`cordis.patch.yml` 注册 + 挂载 + 暴露为工具示例（provider + tool 两行、`permission: reject`、纯 Cordis 插件需手动 insert）。

---

> 坑位攒了不少，最后一章不再讲新内容，只把第 2–6 章埋的坑、三个选型速查与三类诚实标注集中收口成一张可扫的速查索引。

## 第七章 速查与避坑清单

> [!summary] 导读
> 前六章把 subagent 从心智模型一路讲到工具化，信息量不小。这一章不做新内容，只做三件事：把第 2–6 章埋下的坑汇总成一屏可扫的索引表；把三个高频决策（选 provider / 选 one-shot vs continuable / 选 in-process vs out-of-process）压成速查；并把全系列的诚实标注（综合推断 / 未证实 / 未抓取）集中列明，方便写作与排错时快速定位。它不替代前面的任何一章——当你遇到报错或拿不准选型时，回这里翻表，再回到对应章节看细节。

### 7.1 避坑速查表（一屏索引）

下表索引第 2–6 章埋下的坑，只给「坑名 → 出处 → 一句话规避」。每条坑的完整论证与代码上下文，回到出处章查看；素材源头见 02 深度研究 §5 矛盾表与 S2/S3/S5/S6/S7 要点汇总。[^c7-R5]

| 坑名 | 出处章 | 一句话规避 |
|---|---|---|
| UNSUPPORTED_CAPABILITY 响亮失败 | 第 2 章（2.3.1） | 能力不匹配启动即拒、绝不静默；要能力选 spawn/fork，收到此错不是重试能解决 [^c7-S2] |
| outputSchema 不保证 | 第 2 章（2.3.2） | 请求了 schema 不一定拿到 `structured`；消费方回退 `output` 文本 [^c7-S2] |
| inheritsParentContext 反直觉 | 第 2 章（2.2.3） | 只担保对话种子；工具/服务/权限要显式走 agentOptions / toolFilter [^c7-S2] |
| spawn 无父历史 | 第 3 章（provider 家族） | 想让孩子接父对话用 fork；spawn 是全新 child [^c7-S8] |
| acp 零能力 | 第 3 章（acp） | acp 不声明任何启动期能力；要能力强制换 in-process [^c7-S5] |
| 纯 Cordis 需手动 insert | 第 3 章（挂载） | `dsh plugin add` 只让包可解析；必须手动在 `cordis.patch.yml` insert 才挂进插件树 |
| codex/claude-code 未抓配置 | 第 3 章（外部后端） | 本分册未抓 config 表；需要时查官方，别当已完整 |
| 无默认导出（postmortem 0001） | 第 4 章（包级坑） | subagent 系列包无默认导出，Cordis loader 解包会隐藏命名 `inject` 元数据；用命名导出 [^c7-S56] |
| capabilities 不声明即拒绝 | 第 4 章（契约） | 不声明 → 请求对应能力的 start 被 `UNSUPPORTED_CAPABILITY` 拒绝；按需声明四 flag [^c7-S2] |
| start 发布前清理 | 第 4 章（start） | fulfill 前失败必须清理未发布资源，别留孤儿 [^c7-S2] |
| 6.1 骨架综合推断 | 第 4 章（6.1） | 官方无独立教程，骨架是 S2+S4 拼合；发布前对照 `subagent-spawn-in-process` 源码核实 [^c7-R7] |
| 冷恢复不可降深度 | 第 5 章（委派深度） | 冷恢复无法降低 delegationDepth；别指望冷恢复缩深度 [^c7-S2] |
| 消息不可重放 | 第 5 章（continuable） | 已接受未落日志的消息不可重放；别依赖重放恢复 [^c7-S3] |
| report 需存活父代 | 第 5 章（report） | report 需存活直接父代；父代已死则上报不可达 [^c7-S3] |
| 跨进程 ownership 未设计 | 第 5 章（已知限制） | 官方未设计跨进程 continuable ownership；多进程共享要持久 mailbox + 租约，C2 只作经验 [^c7-S3] |
| toolName 全局唯一 | 第 6 章（dsh-tool-subagent） | 一个 provider 绑一个 toolName；重复会冲突，全局唯一命名 [^c7-S7] |
| maxDepth 默认 3 / provider-managed | 第 6 章（maxDepth） | 默认 3、0 禁止委派；dsh-sdk 上设 `'provider-managed'` 才由子 harness 自管递归预算 [^c7-S7][^c7-S6] |
| 后台结果走 task 工具 | 第 6 章（后台 one-shot） | 后台 one-shot 结果经 task 工具回传；消费方监听 task 回传而非前台 await [^c7-S7] |

> [!tip] 大白话
> 把这张表想成药盒上的「不良反应速查」：你不需要背每一种坑，只需要在症状出现时回来对一下。所以……这章的价值不是「多讲了几条知识」，而是把前六章的知识点压成了「出错时能翻到的索引」。

### 7.2 决策速查

三个高频选型，各一张表。规则都一样：先对需求，再选实现，最后回头查 7.1 的坑。

### 7.2.1 选 provider

| 需求 | 选 | 一句依据 |
|---|---|---|
| 要结构化输出 / toolFilter / persona / 深度强制 | spawn / fork | in-process 四项启动期能力全支持 [^c7-S8][^c7-S2] |
| 要子代理继承父对话上下文 | fork | `inheritsParentContext: true`，带对话种子 [^c7-S2] |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | 三者均 `inheritsParentContext: false` [^c7-S2][^c7-S5][^c7-S6] |
| 要驱动任意 ACP 协议 agent | acp | 独立子进程、ACP 客户端驱动 [^c7-S5] |
| 要完整独立 harness（自管模型/组合/递归预算） | dsh-sdk | 子进程是完整 peer harness；可设 `maxDepth: 'provider-managed'` [^c7-S6] |

### 7.2.2 选 one-shot vs continuable

| 场景 | 选 |
|---|---|
| 一次性委派，await 结果，用完 dispose | one-shot（前台，默认） |
| 一次性委派，不想阻塞，跑完回传 | one-shot（后台：`enableRunInBackground` + `backgroundMode`） |
| 需要跨 turn 续写、可恢复、可中断 | continuable（`startContinuable` + `followup` / `interrupt`） |
| 需要 child 反向上报给 parent | continuable（`reportFrom`） |
| 注意 | 两者驻留都仅进程本地；continuable 不跨进程协调 |

### 7.2.3 选 in-process vs out-of-process

| 维度 | in-process（spawn/fork） | out-of-process（acp/dsh-sdk） |
|---|---|---|
| 运行位置 | 同进程新建 child | 独立子进程（ACP / SDK 握手） |
| 启动期能力 | spawn 四项全支持 / fork 支持 | acp 零能力 / dsh-sdk 全 false |
| 继承语义 | spawn:false、fork:true | 均 false |
| 隔离与成本 | 无进程隔离、成本低 | 环境变量擦除 + 独立 session root；dsh-sdk 成本更高 |
| 适用 | 要能力强制、快速上手 | 要隔离 / 驱动外部协议 / 完整 peer harness |

决策箭头：要能力强制 → in-process；要进程隔离或驱动外部 ACP agent → acp；要完整 peer harness（自管递归预算）→ dsh-sdk。

> [!tip] 大白话
> 把决策速查想成餐厅的「点单对照」：先说自己要什么（需求），服务员再给你指对应的菜（provider / 模式）。所以……别从「哪个 provider 最好」开始问，要从「我这单要什么能力」开始对表。

### 7.3 诚实标注清单（集中列明）

全系列三类「信心等级」在此集中收口，不散落各章。写作或排错时若引用下列任一项，请保持标注。[^c7-R5][^c7-R7]

| 类型 | 项 | 状态 | 处置 |
|---|---|---|---|
| 综合推断 | 第 4 章 6.1 最小 provider 骨架（尤其 `start()` 的 in-process 实现） | 官方无独立 SubagentProvider 教程，由 S2 契约 + S4 三段式拼合 | 发布前对照 `subagent-spawn-in-process` 真实源码核实 |
| 未证实 | 「dsh 无内置 subagent 数量限制」 | 仅社区二手说法（P1 已 403），未经官方证实 | 本系列不展开；需要时查官方 |
| 未抓取 | codex / claude-code provider 完整 config 表 | 本分册 P2 未抓取 | MOC 标注可扩展，留给后续分册 |
| 未抓取 | tool-subagent-report README 细节 | 未单独抓取（与 -control 同 README 族） | 写第 6 章时补齐；本章只索引 |
| 未抓取 | cordis.patch.yml 手动 insert 精确语法 | 未对照 C1 第三方插件 insert 示例核实 | 写第 3 章时对照配置体系笔记核实 |

> [!tip] 大白话
> 把三个等级想成「信心标签」：综合推断 =「我们拼出来的，别当定论」；未证实 =「网传，官方没认」；未抓取 =「这页书我们还没读」。所以……看到这三个词，你就知道哪些话能直接引用、哪些要先核实再用。

### 本章小结

- 第 2–6 章共埋约 18 个坑，全部收进 7.1 一屏索引；排错先对表、再回出处章看细节。
- 三个选型速查：选 provider 看能力需求与继承语义；one-shot 看要不要跨 turn；in/out-of-process 看要不要隔离与能力强制。
- 诚实标注集中在 7.3：综合推断（6.1 骨架）、未证实（数量限制）、未抓取（codex/claude-code 配置表、tool-subagent-report、cordis.patch.yml 语法）。
- 本系列到此收尾：1 章心智 → 2 章契约 → 3 章选型 → 4 章写 provider → 5 章生命周期 → 6 章工具化 → 7 章速查。

### 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness | 迁移动作 |
|---|---|---|---|
| 心智单元 | 写一个 `.md` 角色文件 | 三段式三件套（定义 + provider + 工具） | 把「一个 subagent」换成「一条能力缝」 |
| 声明方式 | `.claude/agents/*.md` 框架自动发现 | `ctx.subagents.registerProvider` 显式注册（effect-scoped） | 写 provider 插件并注册 |
| 执行后端 | 内置唯一实现，不可换 | 六 provider 可替换，配置一行切换 | 换执行只改 `config.provider` |
| 能力声明 | md frontmatter 隐含 | `capabilities` 四 flag 静态声明，缺则拒 | 显式声明 outputSchema / depthLimit / toolFilter / persona |
| 结果模型 | 「运行即结果」，失败即异常 | `SubagentRun` / `Result` + stopReason 五值 | 处理 stopReason；result 不因 child 失败 reject |
| 上下文继承 | 隐式 | `inheritsParentContext` 描述性标注（只担保对话种子） | 别指望 flag 带工具/服务/权限 |
| 续写能力 | 一次性 task 委派 | continuable + followup / interrupt / reportFrom | 要跨 turn 恢复用 continuable |
| 工具调用面 | 框架自动暴露 subagent | dsh-tool-subagent / -control / -report 三件套 | 配置工具实例暴露给模型 |
| 委派深度 | 无显式概念 | maxDepth / delegationDepth（默认 3） | 按 provider 区分配置 |

迁移心智：Claude Code 把 subagent 的「注册、能力、结果、续写」都收敛在框架和 md 文件里，上手快但扩展面小；dsh 把这些全部显式化——代价是你要记更多契约字段和坑，收益是执行后端可替换、生命周期可编程。速查表的使用方式一样：在 Claude Code 侧你查「subagent 怎么写」的文档，在 dsh 侧你查「能力缝怎么补全」的这张表。

### 更新记录与开放问题

> [!warning] developer preview（2026-08-13 锚点）破坏性变更风险
> 整个 dsh subagent 生态锚定在 2026-08-13 的 developer preview：包名、配置、契约都可能破坏性变更。本系列第 2–6 章的坑位、7.1 索引与 7.2 决策依据都以此版本为准；若你读到的版本与本文不一致，先查官方 release notes 与各章更新记录，再决定是否调整选型。

**开放问题（索引，源自 02 素材 §7）：**[^c7-R7]

1. **6.1 骨架 `start()` in-process 实现**——如何用 `ctx.agents` 创建 child 并满足「发布后返回 handle / 发布前清理」，需对照 `subagent-spawn-in-process` 源码。
2. **「无内置 subagent 数量限制」未获官方证实**——本系列按未证实处理，不展开。
3. **codex / claude-code provider 完整 config 表未抓取**——MOC 标注可扩展。
4. **tool-subagent-report README 细节未单独抓取**——写第 6 章时补。
5. **continuable 跨进程所有权契约官方「未设计」**——社区方案 dsh-background-agents（C2）只作经验标注。
6. **cordis.patch.yml 手动挂载精确语法**——需对照配置体系笔记 + C1 第三方插件 insert 示例核实。

- **2026-08-16（成稿）**：本章为全系列速查索引，不新增内容。避坑表、决策表、诚实标注清单分别汇总第 2–6 章坑位、选型依据与三类信心等级；若 preview 更新改变坑位或决策依据，7.1 / 7.2 是受影响区域，优先对照检查。

---

[^c7-S2]: S2 · Subagent 子系统设计文档（中文）——第 2 章坑位契约（UNSUPPORTED_CAPABILITY、outputSchema、inheritsParentContext、start 清理）与委派深度机制出处。
[^c7-S3]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README——第 5 章坑位（消息不可重放、report 需存活父代、跨进程 ownership 未设计）。
[^c7-S5]: S5 · `dsh-subagent-acp` README——acp 零能力、独立子进程语义（§4.7）。
[^c7-S6]: S6 · `dsh-subagent-dsh-sdk` README——dsh-sdk 完整 peer harness、`'provider-managed'`（§4.5/§4.7）。
[^c7-S7]: S7 · `dsh-tool-subagent` README——toolName 唯一、maxDepth 默认 3、后台 one-shot 走 task 工具（§4.8）。
[^c7-S8]: S8 · `subagent-spawn-in-process` README——spawn 无父历史、in-process 四项能力全支持（§4.7）。
[^c7-S56]: S5/S6 §4.9——subagent 系列包无默认导出（postmortem 0001）。
[^c7-R5]: 02 深度研究 §5 矛盾表——坑与细微差别的集中汇总。
[^c7-R7]: 02 深度研究 §7 开放问题——开放问题与 6.1 综合推断的出处。
