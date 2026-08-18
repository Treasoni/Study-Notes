# 第五章 生命周期深度——one-shot / continuable 与委派深度

> [!summary] 导读
> 第 2 章结尾留下了两条尾巴：`SubagentRun` 是一次性委托、用完要 dispose；而 `prepareContinuable`「存在即能力」意味着还有一条更长的生命周期。这一章把这两条路讲透：一次委托到底是一次性（one-shot）还是可持续（continuable）？可恢复 child 从出生（`startContinuable`）到继续执行（`followup`）、停止（`interrupt`）、反向上报（`reportFrom`）四个动作各是什么语义？以及贯穿始终的委派深度（delegationDepth）是怎么记账、怎么设限、为什么冷恢复降不下来深度。读完你会理解「持久化子代理」和「一次性 task」的本质差别，也能看懂 `maxDepth`、`'provider-managed'` 这些配置背后的机制。

## 5.1 两条生命周期：one-shot 与 continuable

dsh 的委托分成两个家族：[^S2-4.6]

- **one-shot（一次性）**：建一个 child、跑一轮、拿结果、收尾。它**默认前台**执行——调用方 await 结果；也可以配置为**后台**运行（`enableRunInBackground` + `backgroundMode`），把结果异步回传（后台 one-shot 的结果走 task 工具那条路，第 6 章展开）。
- **continuable（可持续）**：建一个**持久化、可恢复**的 child。它不随一轮结束而消失，可以在之后被 `followup` 续写、被 `interrupt` 停止、并允许 child 通过 `reportFrom` 反向汇报。

一句话分界：**one-shot 是「派单 → 收货」，continuable 是「开一扇长期往来的门」。**

> [!tip] 大白话
> 把 one-shot 想成打一次车：下单、到目的地、下车、结账，交易结束。把 continuable 想成你雇了一个长期助理：今天交个任务，明天再补一句，随时可以叫停，助理也能主动向你汇报。所以……one-shot 适合「一次问答一次结果」，continuable 适合「一个任务要反复推进、甚至跨会话」的场景。

第 2 章讲过，这两种 child 走 provider 的不同入口：one-shot 走 `SubagentProvider.start()`；continuable 走 `prepareContinuable`——**可继续 child 绝不会到达 `start()`**。[^S2-4.2] 接下来看 continuable 这条路的四个编排 API。

## 5.2 continuable 编排四 API 语义

continuable 的编排集中在 `ctx.subagents` 上，四个方法各管一件事：[^S2-4.6]

| 方法 | 方向 | 一句话职责 |
| --- | --- | --- |
| `startContinuable(spec)` | parent → child | 建立持久 child 并投递初始 prompt |
| `followup(parent, childId, content, options)` | parent → child | 唯一继续执行消息操作 |
| `interrupt(targetSessionId, authority)` | 任意 → child | 唯一公开停止操作 |
| `reportFrom(child, content, options)` | child → parent | 可继续 child 向直接 parent 上报 |

### 5.2.1 startContinuable：收件箱准入即 resolve

`startContinuable` 建立持久 child 并投递初始 prompt。它的 resolve 时机很特别：[^S2-4.6][^S3-4.6]

> 收件箱准入即 resolve 出 `{childId, messageId}`，**不等待轮次开始**。

也就是说，`startContinuable` 的返回不代表「child 已经回答了什么」，只代表「这条消息已经被 child 的收件箱接受、这笔账记上了」。轮次什么时候跑、跑成什么样，是之后的事。这个「先确认入账、不等待执行」的语义，是它和 `start` 的根本区别——`start` 是前台等结果，`startContinuable` 是「投递即回执」。

### 5.2.2 followup：唯一继续执行消息操作

`followup(parent, childId, content, options)` 是「唯一继续执行消息操作」——想让一个 continuable child 继续干，只有这一条路。它的路由只看 **Activation 状态**：[^S2-4.6]

| child 当前 Activation 状态 | followup 的行为 |
| --- | --- |
| running（正在跑） | **入队**，等当前轮次结束再处理 |
| waiting（在等消息） | **唤醒**，直接进入新轮次 |
| 无 Activation（冷态/未被加载） | **冷恢复**，先把 child 从持久化恢复再处理 |

注意「只看 Activation 状态」这个措辞：followup 不查消息队列、不查历史，就根据 child 现在「活没活、在不在跑」决定怎么投递。

### 5.2.3 interrupt：唯一公开停止操作

`interrupt(targetSessionId, authority)` 是「唯一公开停止操作」。语义有三条：[^S2-4.6][^S3-4.6]

- **同步鉴权后**发 `Agent.cancel(cause, { keepInbox: true })`——`keepInbox: true` 表示保留收件箱，为将来恢复留门；
- **不等停稳即返回**：它不等待 child 真正停下来，而是「发令」即返回；
- **不存在目标为无害 no-op**：interrupt 一个不存在的 child 不会报错，是一个无害的空操作。

> [!warning] 埋坑 ③（之一）：interrupt 是「发令」不是「等到停」
> `interrupt` 不等 child 完全停稳就返回，别把它当「同步停止」。如果你需要「确认停稳」之后的动作，得靠自己轮询/订阅后续状态——这在 Claude Code 里几乎不会出现，因为那里没有「可持久恢复的 child」这个概念。

### 5.2.4 reportFrom：child 向直接 parent 上报

`reportFrom(child, content, options)` 是可继续 child 向**直接 parent** 上报的方向工具。语义要点：[^S2-4.6]

> **child 是权威凭证，调用方不能指定接收方。**

也就是说，`reportFrom` 的第一个参数是 child（凭证），上报的目的地由「child 的直接 parent」决定，调用方没有权利指定「我要发给谁」。这个「不能指定接收方」的约束，和 `followup` 里「要确切存活直接父代」的限制是一体的（见 5.4）。

> [!tip] 大白话
> 把 `reportFrom` 想成孩子给家长写纸条：纸条上写「家长收」，但谁是这个孩子的家长是登记好的，你不能替孩子指定「把纸条递给隔壁王叔叔」。所以……上报方向是系统按父子关系钉死的，调用方只能决定「报什么」，不能决定「报给谁」。

### 5.2.5 语义示意（非可运行代码）

以下不是可运行代码，只是把四个 API 的调用语义画出来，帮助你建立「谁调谁、带什么、何时返回」的坐标（S2/S3 语义示意）：[^S2-4.6]

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

## 5.3 委派深度：双重表示、只能增、不能降

委派深度（delegation depth）是「这个 child 在委派树里离根有多远」的记账。dsh 用**双重表示**管理它：[^S2-4.5]

| 字段 | 位置 | 性质 |
| --- | --- | --- |
| `SessionHeader.delegationDepth` | 持久化会话头 | 持久表示 |
| `AgentOptions.subagentDepth` | 运行时 agent 选项 | 运行时字段 |

- 两者都**缺失** = 顶层（深度 0）。
- 两者**都存在时，较大的值权威**。
- 两个字段都归 subagent 这个能力缝（seam）所有，**agent loop 不读不写**——这是第 1 章「微内核」主张的又一次体现：核心循环不掺和委派深度的记账，它只是被 seam 维护的一个数据。呼应第 2 章的 `subagent/start` / `subagent/end` 事件：`end` 按委派 parent scope 过滤分发，这个 scope 和委派深度是同一套父子账本——监听者只关心自己委派链上的结束事件。[^S2-4.1]

深度只会往深里走：

- **进程内 child 持久保存 parent 深度 + 1**。[^S2-4.5]
- **冷恢复无法降低深度**。[^S2-4.5]

> [!warning] 埋坑 ①：冷恢复无法降低委派深度
> 「冷恢复」只是把持久化的 child 重新加载，深度是从会话头里读回来的——它不会因为你「重启了一次进程」就归零。所以不要指望「冷启动一次 = 深度重置」。深度只会被父级 +1，恢复时原样读回，想降低只能换一条新的委派链。

深度还有上界校验：**每次 start 都会拒绝两类派生深度**——超出安全整数域的深度，以及高于绝对 `request.maxDepth` 的深度。[^S2-4.5]

### 5.3.1 maxDepth：默认 3、0 禁止、'provider-managed' 特例

`maxDepth` 是绝对委派深度上限，来自 `dsh-tool-subagent` 的配置：[^S7-4.5]

- **默认 3**；
- **`0` 禁止委派**（这个 child 不能再往下派）；
- 在 **dsh-sdk** provider 上部署时，设 `maxDepth: 'provider-managed'`——表示**子 harness 自己管理递归预算**，父级不施加限制。[^S6-4.5]

> [!tip] 大白话
> 把委派深度想成「转包链的长度」：默认最多允许 3 层转包；`maxDepth: 0` 等于「这单不许再转包」；`'provider-managed'` 等于「把发包方换成包工头自己管——他说能转几层就几层」。所以……默认 3 是「防失控转包」的安全阀，`'provider-managed'` 是你明确信任某个 provider 完全自治时才用的开关。

结合第 2 章：`maxDepth` 要求 `depthLimit` 能力（acp/dsh-sdk 不声明 start-time capabilities，所以「强制深度」这种能力只有 spawn/fork 这种 in-process provider 提供）。[^S2-4.3] 这里同样适用「能力不匹配响亮失败」的规则。

## 5.4 已知限制与社区经验

continuable 是 developer preview 里的新机制，官方明确了一批限制，写进自己的系统前必须先知道：[^S3-4.6]

1. **无 host-user 续写**：`followup` 要求**确切存活的直接父代**——你没法「代父代发起续写」，也没有「宿主用户直接续写 child」的路。**只有 `interrupt` 接受持久父地址的 human 权威**。
2. **不能转向当前 turn**：续写消息/唤醒型 report 只**入队后续 turn**，不能插入当前正在跑的轮次。
3. **驻留仅限进程本地**：Activation inbox 与所有权图**不跨进程协调**；多进程并发访问同一持久化库，仍需要**持久 mailbox + 跨进程租约协议**自行保证。
4. **已接受但未落日志的消息不可重放**；并且**没有持久 report 邮箱**——`reportFrom` 要成功，目标直接父代必须存活。
5. **跨进程 continuable ownership 官方「未设计」**。[^C2]

> [!warning] 埋坑 ②：消息不可重放 + report 需存活直接父代
> 「已接受但未落日志的消息不可重放」——`startContinuable`/`followup` 返回的 `messageId` 只能当「入账凭证」，不代表这条消息已经进了可回放的日志。系统崩溃后，这笔账可能就没了，别指望重放恢复。同样地，`reportFrom` 没有持久邮箱，父代一旦不存活，上报就投不出去——所以「先确认直接父代活着，再让 child 上报」是编排方要自己保证的。

### 5.4.1 社区经验：dsh-background-agents（仅作标注）

跨进程的持久化续跑，官方「未设计」。[^C2] 社区有一个补强方案 **dsh-background-agents**（PerryLink）试图补齐「后台续跑子代理」这块。[^C2]

> [!warning] 埋坑 ③：跨进程 continuable ownership 官方未设计
> 这是「未设计」，不是「未实现好」——官方没有给出跨进程谁拥有、谁恢复、怎么防双写的契约。社区方案只能作为经验参考（C2 标注），**不能当成官方能力**写进生产设计。真要跨进程，官方建议自己上「持久 mailbox + 租约」这套通用原语（见 5.4 第 3 条）。

## 本章小结

- 两条生命周期：one-shot（前台默认 / 后台 `enableRunInBackground`+`backgroundMode`）与 continuable（持久化可恢复 child）；continuable 走 `prepareContinuable`，不经过 `start()`。
- 四 API 语义：`startContinuable` 收件箱准入即 resolve（不等轮次开始）；`followup` 唯一续写、按 Activation 路由（running 入队 / waiting 唤醒 / 冷恢复）；`interrupt` 唯一停止、同步鉴权后发 cancel(keepInbox:true)、不等停稳、不存在目标为无害 no-op；`reportFrom` child 向直接父代上报、child 是权威凭证、调用方不能指定接收方。
- 委派深度双重表示（持久 `SessionHeader.delegationDepth` + 运行时 `AgentOptions.subagentDepth`，较大值权威，归 seam 不归 loop）；进程内 child 保存 parent+1；冷恢复无法降低深度；start 校验安全整数域与 `maxDepth` 上界。
- `maxDepth` 默认 3、`0` 禁止委派；dsh-sdk 上 `'provider-managed'` 表示子 harness 自管递归预算。
- 已知限制：无 host-user 续写（followup 要确切存活直接父代，只有 interrupt 接受 human 权威）；不能转向当前 turn；驻留仅进程本地（跨进程要持久 mailbox + 租约）；跨进程 ownership 官方「未设计」，dsh-background-agents 仅社区经验标注。
- 埋的坑：① 冷恢复无法降低深度 ② 已接受未落日志的消息不可重放、report 需存活直接父代 ③ 跨进程 continuable ownership 官方未设计。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 委派形态 | 一次性 `task` 委派，结果即返回 | one-shot（前台/后台）+ continuable（持久可恢复）两族 |
| 续写 | 无持久续写——每次 task 重新派 | `followup` 唯一续写，按 Activation 状态路由 |
| 停止 | 取消当前调用即止 | `interrupt` 唯一停止，发 cancel(keepInbox:true) 不等停稳 |
| 反向上报 | 无独立方向工具 | `reportFrom` child 向直接父代上报，方向由父子关系钉死 |
| 深度控制 | 无显式委派深度记账 | `delegationDepth`/`subagentDepth` 双重表示 + `maxDepth` 上限（默认 3、0 禁止、`'provider-managed'` 特例） |

迁移心智：Claude Code 的 subagent 心智是「一次 task = 一次结果，用完即焚」；dsh 的 continuable 把「子代理」从一次性工具升级成了**有状态的工作对象**——能续写、能叫停、能反向汇报、有委派深度记账。你在 Claude Code 里习惯的「派一次、收一次」对应 dsh 的 one-shot 路；如果你需要「一个长期推进的子任务」，dsh 的 continuable + followup/interrupt 是 Claude Code 目前没有的编排面。

## 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方子系统文档（S2 §4.6/§4.5）、核心包 README（S3 §4.6）、工具 README（S7 §4.5、S6 §4.5）撰写。continuable 编排四 API 与委派深度机制均出自官方契约；`dsh-background-agents`（C2）仅作社区经验标注，非官方能力。若 preview 更新改动 `followup` 路由规则、`interrupt` 语义或深度字段，本章 5.2-5.4 受影响，优先对照检查。

---

[^S2-4.6]: S2 · Subagent 子系统设计文档（中文）§4.6——one-shot vs continuable、startContinuable/followup/interrupt/reportFrom 语义。
[^S3-4.6]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.6——无 host-user 续写、不能转向当前 turn、驻留仅进程本地、已接受未落日志不可重放、无持久 report 邮箱。
[^S2-4.5]: S2 §4.5——委派深度双重表示、进程内 parent+1、冷恢复无法降低深度、上界校验。
[^S7-4.5]: S7 · `dsh-tool-subagent` README §4.5——maxDepth 默认 3、0 禁止委派。
[^S6-4.5]: S6 · `dsh-subagent-dsh-sdk` README §4.5——`maxDepth: 'provider-managed'` 子 harness 自管递归预算。
[^S2-4.1]: S2 §4.1——核心方法总览与 `subagent/start|end` 事件按委派 parent scope 过滤分发。
[^S2-4.2]: S2 §4.2——prepareContinuable 存在即能力；可继续 child 不到达 start()。
[^S2-4.3]: S2 §4.3——maxDepth 要求 depthLimit 能力。
[^C2]: C2 · dsh-background-agents（PerryLink，社区）——跨进程后台续跑子代理补强；官方「未设计」，仅作经验标注。
