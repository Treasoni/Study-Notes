---
title: "DeepSeek-Harness Subagent 开发 · 第2章 核心契约——`ctx.subagents` 注册表与 `SubagentProvider` 接口"
tags: [deepseek-harness, ai, agent, subagent, 教程, 开发]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
series: "DeepSeek-Harness Subagent 教程"
---

# 第二章 核心契约——`ctx.subagents` 注册表与 `SubagentProvider` 接口

> [!note] 分册导航
> [[DeepSeek-Harness Subagent 教程/README|📋 返回分册首页]] · [[01-心智模型-能力缝与三层结构|← 上一章]] · [[03-现成provider家族-选用挂载跑起来|下一章 →]]

> [!summary] 导读
> 第 1 章立了全景心智：subagent 是一条能力缝，三层结构各司其职。这一章下钻到「缝」的接口层，把三个问题讲透：调用方怎么通过 `ctx.subagents` 找到并调用 provider？一个 provider 要兑现哪些契约字段？一次委托请求带哪些选项、结果怎么解读？读完你会看懂 `ctx.subagents` 的注册与查询、`SubagentProvider` 每个字段的含义、以及一次委托从「请求 → 能力检查 → start → result」的完整语义——第 1 章埋的 `inheritsParentContext` 悬念也会在这里揭开。

## 2.1 `ctx.subagents` 注册表

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

## 2.2 `SubagentProvider` 契约

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

## 2.3 `SubagentStartRequest` 选项与能力检查

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

## 2.4 `SubagentRun` / `SubagentResult`：一次委托怎么结算

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

## 本章小结

- `ctx.subagents` 是总机：`registerProvider` 按名注册且 effect-scoped（移除阻止新 start、不撤销已返回 run）；`getProvider`/`list` 查询；事件 `provider-added/removed`、`start/end`（end 按 parent scope 分发）；`listChildren/listDescendants` 只读枚举。
- `SubagentProvider` 契约五块：`name` 唯一名；`capabilities` 四 flag（outputSchema/depthLimit/toolFilter/persona）是启动期静态声明；`inheritsParentContext` 只是「带没带对话种子」的描述性标注，不担保工具/服务/权限继承；`start` 在发布后返回 handle、发布前失败要清理；`prepareContinuable` 存在即能力。
- `SubagentStartRequest` 九个选项，后四个绑定能力；能力不匹配 → `UNSUPPORTED_CAPABILITY` 响亮失败，绝不静默。
- `SubagentRun` 是一次性前台委托：result 不因 child 级失败 reject（`stopReason:'error'` 正常 resolve），output 取最后一个非空 assistant 消息，stopReason 五值，ACP/dsh-sdk 映射遵循「不洁停止绝不报成功」。
- 埋的三个坑：① 能力不匹配响亮失败 ② outputSchema 请求了不保证 structured ③ inheritsParentContext 名不副实。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 注册方式 | 框架从 `.claude/agents/*.md` 自动发现 | `ctx.subagents.registerProvider` 显式注册，effect-scoped |
| 能力声明 | md frontmatter 里隐含 | `capabilities` 四 flag 静态声明，缺则拒 |
| 结果模型 | 「运行即结果」，失败即异常 | 显式 `SubagentRun`/`SubagentResult` + `stopReason` 五值 |
| 上下文继承 | 隐式 | `inheritsParentContext` 描述性标注，只担保对话种子 |
| 续写 | 一次 task 委派，无持久续写 | `prepareContinuable` / continuable 家族（第 5 章） |

迁移心智：Claude Code 把 subagent 的「注册、能力、结果」都收敛在框架和 md 文件里；dsh 把这三件事全部显式化、可编程化。你在 Claude Code 里「写一个 md 文件声明角色」的心智，对应到 dsh 是「实现一个 `SubagentProvider` 对象并注册」——而「结果长什么样、怎么结算」不再是框架替你兜底，你要按 `stopReason` / `output` 语义自己解读。这正是第 1 章说的「能力缝把一切暴露成可替换的契约」在接口层的落地。

## 更新记录

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


---

## 分册导航

- ← [[01-心智模型-能力缝与三层结构|上一章]]
- → [[03-现成provider家族-选用挂载跑起来|下一章]]
- [[DeepSeek-Harness Subagent 教程/README|返回分册首页]]
