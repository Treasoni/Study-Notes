# 02 深度研究 · 如何写 subagent（DeepSeek-Harness）

> 项目：deepseek-harness-subagent ｜ 阶段：P2 深度收集 ｜ 检索日期：2026-08-16
> 用户方向：**A+B 组合**（全流程概念 → 写 provider → 工具化；并深度覆盖 provider 插件写作）
> 素材抓取：官方源为主；社区仅作经验标注。所有官方文档无显式发布日期，唯一时间锚点是 developer preview（2026-08-13）。

---

## 1. 研究范围（Scope）

承接 P1 方向 A+B，回答三组问题：

1. **心智模型**：subagent 为什么是「能力缝」而不是单一插件？三层结构（`ctx.subagents` 注册表 / `SubagentProvider` 提供方 / consumer 工具）怎么工作？
2. **写 provider**：`SubagentProvider` 契约是什么？`start` / `prepareContinuable` / `capabilities` 分别承担什么？in-process 与 out-of-process 两种写法的关键差异？三段式（Service Definition / Provider / Consumer）设计模式如何套用？
3. **工具化与配置**：写好的 provider 怎么注册、怎么用 `dsh-tool-subagent`（-control/-report）暴露成模型可调能力、怎么挂进 cordis 插件树、有哪些坑。

**排除**：`codex` / `claude-code` 两个外部 CLI provider 的逐键配置表（P2 未抓取，留给后续分册）；Claude Code 侧 `.claude/agents/*.md` 的完整对照（只保留与本笔记相关的迁移要点）。

---

## 2. 来源表（Source Table）

| ID | 标题 | Tier | 角色 | URL | 检索 |
|---|---|---|---|---|---|
| S1 | Subagent 子系统设计文档（EN） | official | 契约权威 | `docs/subsystems/subagent.md` | 2026-08-16（会话早前） |
| S2 | Subagent 子系统设计文档（中文） | official | 契约 + 坑清单 | `docs/subsystems/subagent.zh.md` | 2026-08-16 |
| S3 | `@deepseek-ai/dsh-subagent` 核心包 README | official | 一手代码包语义 | `packages/subagent/subagent/README.md` | 2026-08-16 |
| S4 | Three-role capability design（开发者实践教程） | official | 写 provider 方法论 | `docs/user/develop/practice/index.md` | 2026-08-16 |
| S5 | `dsh-subagent-acp` README | official | out-of-process provider 样板 | `packages/subagent/subagent-acp/README.md` | 2026-08-16 |
| S6 | `dsh-subagent-dsh-sdk` README | official | 第二个 out-of-process 样板 | `packages/subagent/subagent-dsh-sdk/README.md` | 2026-08-16 |
| S7 | `dsh-tool-subagent` README | official | 模型面委托工具 | `packages/subagent/tool-subagent/README.md` | 2026-08-16（会话早前） |
| S8 | `subagent-spawn-in-process` README | official | in-process 样板 | `packages/subagent/subagent-spawn-in-process/README.md` | 2026-08-16（会话早前） |
| S9 | `tool-subagent-control` / `-report` README | official | 控制/汇报工具 | `packages/subagent/tool-subagent-control/README.md` | 2026-08-16（会话早前） |
| S10 | 扩展 Cookbook | official | feature→mechanism 全景 | `docs/cookbook/extension-cookbook.md` | 2026-08-16 |
| C1 | dsh-plugin-product-subagents（npm 0.2.0） | community | 第三方 provider 插件样板 | npm | 2026-08-16（P1） |
| C2 | dsh-background-agents（PerryLink） | community | 续跑子代理社区补强 | GitHub | 2026-08-16（P1） |
| C3 | Discussion #1477 | community | 实战问题聚合 | GitHub | 2026-08-16（P1） |

---

## 3. 核心心智模型

### 3.1 subagent 是「能力缝」，不是单一插件

- 与 bash 同一类**可选能力缝（seam）**；但 bash 只允许单执行器，subagent 允许多提供方并存、按名注册——注册表模式仿照 LLM 适配器注册表（S1/S2 引言）。
- Cookbook 把它映射为两个 mechanism：**`ctx.subagents` provider registry**（spawn/fork/acp/codex/claude-code/dsh-sdk 六兄弟）+ **`dsh-tool-subagent`** 把其中一个 provider 暴露给模型（S10）。
- 官方 cookbook 的中心主张：*"Every product feature maps to a listener on a documented extension point — the microkernel claim made checkable"*，且 *"No row modifies the loop"*——核心循环固定，一切能力都是扩展点上的监听者（S10）。subagent 正是「在一个固定循环上叠加委派能力」的实例。
- 三段式原则（S4）：*"The complete capability is its seam. No individual role is a seam."*——完整能力本身才是接缝，单一角色（如只有 provider）不是。

### 3.2 三层结构

```
┌─────────────────────────────────────────────────────────────┐
│ ① Service Definition：dsh-subagent（ctx.subagents）          │
│    provider registry + request/result 契约 + 持久描述符 +     │
│    continuable-child 编排（S3 定位段）                        │
├─────────────────────────────────────────────────────────────┤
│ ② Service Provider：spawn / fork / acp / codex / claude-code │
│    / dsh-sdk（同名包）— 具体执行，互不依赖、可替换            │
├─────────────────────────────────────────────────────────────┤
│ ③ Consumer / Tool：dsh-tool-subagent 暴露一个 provider；      │
│    -control 全局控制；-report child→parent 汇报              │
└─────────────────────────────────────────────────────────────┘
```

关键：provider 与 consumer **互不依赖，只依赖定义包**（S4）——换实现只改 cordis 配置一行，定义与工具不动。

---

## 4. Claim/Source Map（按主题分组）

### 4.1 `ctx.subagents` 注册表

| # | 要点 | 来源 |
|---|---|---|
| 1 | `registerProvider(provider)` 按名注册同进程实现；**effect-scoped**——移除阻止新 start，但不撤销已返回的 run | S2/S3 |
| 2 | 重名注册失败；`getProvider(name)` / `list()` 查询 | S3 |
| 3 | 核心方法：`start`、`startContinuable`、`followup`、`interrupt`、`reportFrom`、`registerContinuableSetup`、`drainContinuableDescendants`、`listChildren`/`listDescendants` | S2 |
| 4 | 生命周期事件：`subagent/provider-added`、`provider-removed`、`start`/`end` 配对（后者按委派 parent scope 过滤分发） | S2/S3 |
| 5 | `listChildren`/`listDescendants` 只读枚举：不加载/恢复 child、不查 Activation map/Agent 注册表/提供方可用性 | S2 |

### 4.2 `SubagentProvider` 契约

| # | 要点 | 来源 |
|---|---|---|
| 1 | `name`：唯一注册名（如 `spawn`/`fork`/`acp`） | S2 |
| 2 | `capabilities`：四个启动时 flag——`outputSchema` / `depthLimit` / `toolFilter` / `persona`，与 `SubagentStartRequest` 选项一一对应（`depthLimit` ↔ `maxDepth`） | S2/S3 |
| 3 | `inheritsParentContext`：**描述性**——只说明对话种子注入（fork: true；spawn/acp: false），**不暗示工具/服务/权限继承** | S2 |
| 4 | `start(request: ResolvedSubagentStartRequest)`：建立一次性 child 并在**发布后**返回 handle；服务已校验能力并解析 `request.descriptor`；fulfill 前失败须清理未发布部分资源 | S2 |
| 5 | `prepareContinuable?(request)`：可选方法，**方法存在即能力**（TypeScript 类型收窄作发现机制）；只返回 `ContinuableCreateSpec`（目前仅可选父历史种子 `seed`），不含 Agent/handle/投递/结果/dispose/恢复 | S2/S3 |
| 6 | 冷恢复不经由 provider 分发；拥有 `prepareContinuable` 的 provider 仍可同时服务普通 one-shot 委托 | S2/S3 |
| 7 | 信任模型：provider 是受信任的同进程实现；调用方视描述符/返回值为借用的不可变数据；服务可对不同 child **并发**调用同一 provider，各 run 取消/失败/结算独立 | S2 |

### 4.3 `SubagentStartRequest` 选项与能力检查

| # | 要点 | 来源 |
|---|---|---|
| 1 | 选项：`label` / `prompt`（`ContentBlock[]`）/ `parent` / `signal` / `agentOptions` / `outputSchema` / `maxDepth` / `toolFilter` / `persona` | S2 |
| 2 | **能力不匹配在启动时响亮失败**：*"如果请求依赖提供方不具备的功能，会被明确拒绝（`SubagentError('UNSUPPORTED_CAPABILITY')`），绝不会被接受后静默忽略"* | S2 |
| 3 | `outputSchema`：强制 `assertObjectJsonSchema` 子集内的 object-rooted schema；成功时 child 返回 `SubagentResult.structured`；**请求了不保证得到** | S2 |
| 4 | `maxDepth`：可选绝对委派深度上限（非负安全整数）；要求 `depthLimit` 能力 | S2 |
| 5 | `toolFilter`：要求 `toolFilter` 能力；进程内用 scoped `tools.restrict()`——命名工具从 prompt 消失且拒绝执行（**可见性而非权限**）；未知名大声校验 | S2 |
| 6 | `persona`：要求 `persona` 能力；进程内注册 scoped `deployment:persona` section，只对该 child 遮蔽部署 persona | S2 |
| 7 | 解析后 `ResolvedSubagentStartRequest = SubagentStartRequest + descriptor: SubagentDescriptorData`（分离的一次性描述符）；**可继续 child 绝不到达 `SubagentProvider.start()`** | S2 |

### 4.4 `SubagentRun` / `SubagentResult`

| # | 要点 | 来源 |
|---|---|---|
| 1 | `SubagentRun` 是一次可 dispose 的前台委派、只有一个结果；消费方 await 结果并始终 dispose，直至完全停稳 | S2 |
| 2 | `result` 不因 child 级失败 reject——model/transport 失败以 `stopReason: 'error'` resolve，消费方映射为 `isError` 工具结果；仅基础设施故障 reject | S2/S3 |
| 3 | `output` 语义：取最后一个非空 assistant 消息内容；空内容消息（含 usage-only）跳过；无非空消息回退为累积 assistant 文本流；两者皆无则 `[]` | S2/S6 |
| 4 | `stopReason`（可合并扩展派生联合）：`completed` / `aborted` / `error` / `max-tokens` / `refusal`；非 `completed` 表示 output 可能不完整 | S2 |
| 5 | ACP 映射表：`end_turn→completed`、`max_tokens→max-tokens`、`refusal→refusal`、`cancelled→aborted`、`max_turn_requests` 或未知→`error` | S5 |
| 6 | dsh-sdk 映射：`completed`/`max-tokens`/`aborted` 原样；其余一切（error/interrupted/disposed/未来变体/无 turn）→`error`，**不洁停止绝不报成功** | S6 |

### 4.5 深度机制（delegationDepth / maxDepth）

| # | 要点 | 来源 |
|---|---|---|
| 1 | 双重表示：持久 `SessionHeader.delegationDepth` + 运行时字段 `AgentOptions.subagentDepth`；缺失=顶层 0，存在的较大值权威；两字段都归该 seam 所有，agent loop 不读不写 | S2 |
| 2 | 进程内 child 持久保存 **parent 深度 + 1**；*"冷恢复无法降低深度"* | S2 |
| 3 | 每次 start 拒绝超出安全整数域的派生深度，以及高于绝对 `request.maxDepth` 的派生深度 | S2 |
| 4 | `dsh-tool-subagent` 的 `maxDepth` **默认 3**，`0` 禁止委派 | S7 |
| 5 | 在 dsh-sdk provider 上部署时设 `maxDepth: 'provider-managed'`：表示子 harness 自己管理递归预算，父级不施加 | S6 |
| 6 | fork 种子：经 `CreateAgentOptions.seed` 传父日志平衡的已完成轮次前缀（到最后一个 `turn/end`），保证 seq 从 0 连续可回放 | S2 |

### 4.6 one-shot vs continuable 生命周期

| # | 要点 | 来源 |
|---|---|---|
| 1 | one-shot：前台（默认）/ 后台（`enableRunInBackground` + `backgroundMode`）；continuable：持久化可恢复 child | S2/S7 |
| 2 | `startContinuable(spec)` 建立持久 child 并投递初始 prompt；收件箱准入即 resolve 出 `{childId, messageId}`，**不等待轮次开始** | S2/S3 |
| 3 | `followup(parent, childId, content, options)`：唯一继续执行消息操作；路由仅看 Activation 状态——running 入队、waiting 唤醒、无 Activation 冷恢复 | S2 |
| 4 | `interrupt(targetSessionId, authority)`：唯一公开停止操作；同步鉴权后发 `Agent.cancel(cause, { keepInbox: true })`，**不等停稳即返回**；不存在目标为无害 no-op | S2/S3 |
| 5 | `reportFrom(child, content, options)`：可继续 child 向直接 parent 上报；child 是权威凭证，调用方不能指定接收方 | S2 |
| 6 | **无 host-user 续写**：`followup` 要求确切存活的直接父代；只有 `interrupt` 接受持久父地址的 human 权威 | S3 |
| 7 | **不能转向当前 turn**：续写消息/唤醒型 report 只入队后续 turn | S3 |
| 8 | 驻留仅限进程本地：Activation inbox 与所有权图不跨进程协调；多进程并发访问同一持久化库仍需持久 mailbox + 跨进程租约协议 | S3 |
| 9 | 已接受但未落日志的消息不可重放；无持久 report 邮箱（report 要存活直接父代） | S3 |

### 4.7 现成 provider 家族（in-process vs out-of-process）

| # | 要点 | 来源 |
|---|---|---|
| 1 | **spawn**（in-process）：全新 child、无父历史；四项启动期能力**全支持**；`providerName` 默认 `spawn` | S8 |
| 2 | **fork**（in-process）：从父已完成 turn 种子；`inheritsParentContext: true` | S1/S2 |
| 3 | **acp**（out-of-process）：每个 subagent 跑在独立子进程、作为 ACP 客户端驱动；**不声明任何 start-time capabilities**（无法在远程强制深度/filter/persona/结构化输出），本地服务会**拒绝**而非静默忽略；`inheritsParentContext: false`；每次运行全新进程（无池）；仅本地工作区 | S5 |
| 4 | **dsh-sdk**（out-of-process）：stdio JSON-RPC 驱动 harness SDK runtime，子进程是**完整 peer harness**（有自己的 cordis 组合/会话/模型路由/工具）；启动期 capabilities 全 false；`inheritsParentContext: false`；每次 run 全新 runtime 进程（成本高于 acp 典型子进程）；子进程 transcript 留在子进程自己的 session root | S6 |
| 5 | **codex / claude-code**：外部 CLI 后端（仅列名，P2 未抓配置表） | S1/S10 |
| 6 | 环境变量处理（acp/dsh-sdk 共用 `dsh-subprocess` 语义）：先擦除「凭据形状」变量与陈旧 `DSH_*` 名，再合并显式 `config.env` | S5/S6 |
| 7 | **cwd 规则**：配置了 `cwd` 用配置值（load 时校验一次），否则用委托方父会话的 cwd，**绝不用 server 进程自身 cwd** | S5/S6 |

### 4.8 委托/控制/汇报工具（consumer 面）

| # | 要点 | 来源 |
|---|---|---|
| 1 | `dsh-tool-subagent`：**一个 provider 绑一个 toolName**（默认 `subagent`）；config：`provider`（必填）/ `toolName` / `enableRunInBackground` / `backgroundMode`（one-shot|continuable）/ `agentOptions` / `persona` / `toolFilter` / `maxDepth`（默认 3） | S7 |
| 2 | `dsh-tool-subagent-control`：`send_message` / `interrupt_agent` / `list_agents` 全局控制工具 | S9 |
| 3 | `dsh-tool-subagent-report`：child→parent 汇报方向工具 | S9 |
| 4 | 内置 `dsh-tool-*` 家族含 subagent：*"bash, fs, web, subagent, todo"* | S10 |

### 4.9 写 provider 的方法论（三段式 + 已知坑）

| # | 要点 | 来源 |
|---|---|---|
| 1 | 三步走：① Service Definition（定义包：抽象 Service 类 + Request/Result 类型 + `declare module` 扩展 Context）→ ② Service Provider（实现包：`export const name` + `export function apply(ctx){ ctx.plugin(...) }`）→ ③ Consumer/Tool（`inject: ['tools', 'cap']` + `defineTool` + `ctx.tools.register`） | S4 |
| 2 | 命名约定：定义 `dsh-<cap>`；本地 provider `<cap>-local`；consumer `dsh-tool-<cap>`（官方 my-cap 示例；subagent 系列遵守此律） | S4 |
| 3 | 设计要点：*"Do not split preemptively"*（角色需要独立演进才拆包）；Request/Result 类型归定义包所有；默认值在显式 `resolve(request): Spec` 里处理，不在 `run()` 藏 `?? default` | S4 |
| 4 | 包级坑：subagent 相关包**无默认导出**（Cordis loader 解包会隐藏命名 `inject` 元数据，见 postmortem 0001） | S5/S6 |
| 5 | 委托沙箱策略（核心包实现）：`captureDelegatedPolicyOverrides(parent)` 快照父显式 sandbox 覆盖，并把子代理审批策略钉死为 `'never'`——需审批的升级请求（如 `sandbox_permissions`）确定性拒绝，而非等待无人观看的提示；`subagent:delegation` 运行时上下文声明越权不重试 | S3 |

---

## 5. 矛盾与细微差别（Contradictions & Nuances）

| # | 现象 | 说明 | 处理 |
|---|---|---|---|
| 1 | `inheritsParentContext` 与「继承」直觉相反 | 是**描述性** flag，只谈对话种子注入，不担保工具/服务/权限继承 | 笔记中明确用「描述性标注」措辞 |
| 2 | `maxDepth` 默认 3 vs `'provider-managed'` | 在 dsh-sdk 上设 `provider-managed` 表示子 harness 自管递归；spawn 等 in-process 才由父强制 | 按 provider 区分写 |
| 3 | spawn「无父历史」vs fork「有种子」 | 同属 in-process，继承语义相反 | 用对照表讲清 |
| 4 | 「outputSchema 不保证得到」 | 请求了 schema 不一定返回 `structured` | 消费者必须处理缺失 |
| 5 | 「subagent 无数量限制」 | 仅论坛二手说法（P1 已 403），**未经官方证实** | 笔记不写或标注未证实 |
| 6 | `dsh-tool-subagent` maxDepth 默认值 | S7 记录默认 3、0 禁止；与 S2 子系统文档「能力检查」一致 | 以 S7 工具层为准 |
| 7 | 官方无独立「SubagentProvider 教程」 | 最近是 S4 三段式 + S5/S6 两个 provider 源码样板 | P2 结论：写 provider 章以 S4+S5/S6 为主干，最小骨架标注「综合/推断」 |

---

## 6. 实操指南（Practical Guidance）

### 6.1 最小 provider 插件骨架（综合推断，需对照 `src/types.ts` 与 spawn-in-process 源码核实）

> ⚠️ 官方没有独立 SubagentProvider 教程，以下骨架由 S2 契约 + S4 三段式综合而成，**发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码校验**。

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'
import type {
  SubagentProvider,
  ResolvedSubagentStartRequest,
  SubagentRun,
} from '@deepseek-ai/dsh-subagent'

const myProvider: SubagentProvider = {
  // ① 唯一注册名（config.provider 用它）
  name: 'my-provider',
  // ② 启动时能力声明：outputSchema/depthLimit/toolFilter/persona
  //    不声明 → 请求这些能力的 start 会被 UNSUPPORTED_CAPABILITY 拒绝
  capabilities: {},
  // ③ 描述性：是否把父对话种子注入 child（fork 才 true）
  inheritsParentContext: false,
  // ④ 发布 child 并返回 handle；发布前失败要清理并 reject
  async start(request: ResolvedSubagentStartRequest): Promise<SubagentRun> {
    // in-process：经 ctx.agents 创建 child（对照 spawn-in-process 源码）
    // out-of-process：spawn 子进程 → 握手（ACP initialize / SDK initialize）→ 返回 run
    throw new Error('TODO: implement start()')
  },
  // ⑤ 可选：存在即支持续写（continuable）
  // async prepareContinuable(request) { return { seed: undefined } }
}

export const name = 'my-subagent-provider'
export function apply(ctx: Context) {
  ctx.subagents.registerProvider(myProvider)  // effect-scoped，卸载自动注销
}
```

### 6.2 三段式 Provider 的实现对照（S4 官方 my-cap 三件套）

```ts
// ① Service Definition：定义契约（dsh-my-cap）
export abstract class MyCapService extends Service {
  constructor(ctx: Context) { super(ctx, 'myCap') }
  abstract execute(request: MyCapRequest): Promise<MyCapResult>
}

// ② Provider：实现（dsh-my-cap-local）
class MyCapLocal extends MyCapService {
  async execute(request: MyCapRequest): Promise<MyCapResult> {
    return { output: request.input.toUpperCase() }
  }
}
export function apply(ctx: Context) { ctx.plugin(MyCapLocal) }

// ③ Consumer/Tool（dsh-tool-my-cap）
export const inject = ['tools', 'myCap']
export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'my_cap', description: 'Execute my capability.',
    parameters: { input: { type: 'string', required: true } },
    output: { schema: { type: 'string' }, render: (_a, v) => [{ type: 'text', text: v }] },
    async execute(args) { return (await ctx.myCap.execute({ input: args.input })).output },
  }))
}
```

### 6.3 注册 + 挂载 + 暴露为工具（配置层，A 方向核心）

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

要点：subagent 系列包都是**纯 Cordis 插件**（无 `dsh.bundle.patch`）→ `dsh plugin add` 只让包可解析，**必须手动在 cordis.patch.yml 插入**才能挂进插件树（既有配置体系笔记结论）。

### 6.4 选择 provider 的决策依据

| 需求 | 选 | 依据 |
|---|---|---|
| 想要结构化输出/工具过滤/persona/深度强制 | spawn / fork（in-process 能力全） | S8/S2 |
| 想要完整独立 harness（自管模型/组合/递归预算） | dsh-sdk | S6 |
| 想要驱动任意 ACP 协议 agent | acp | S5 |
| 想要子代理继承父对话上下文 | fork | S2 |
| 不想子代理看到父对话 | spawn / acp / dsh-sdk | S2/S5/S6 |

---

## 7. 开放问题（Open Questions）

1. **最小 provider 的 `start()` in-process 实现**：如何用 `ctx.agents` 创建 child 并满足「发布后返回 handle / 发布前清理」——需读 `subagent-spawn-in-process` 源码，写进章节前核对。
2. 「dsh 无内置 subagent 数量限制」未获官方证实 → 笔记不写或标注未证实。
3. `codex` / `claude-code` provider 的完整 config 表未抓取（本分册略过，MOC 里标注可扩展）。
4. `tool-subagent-report` README 细节未单独抓取（与 -control 同 README 族，写章节时补）。
5. continuable 跨进程所有权契约官方「未设计」（S3 已知限制）→ 社区方案（C2 dsh-background-agents）只作经验标注。
6. subagent 包手动 `cordis.patch.yml` 挂载的精确语法需对照配置体系笔记 + C1 第三方插件的 insert 示例（已收录 P1）。

---

## 8. 下游交接（Downstream Handoff）

**给 outline-generator 的建议骨架**（方向 A+B，约 5-6 章）：

1. 心智模型：能力缝 + 三层结构（S1/S2/S10）
2. 注册表与契约：`ctx.subagents` + `SubagentProvider`（S2/S3）
3. 现成 provider 选用：spawn/fork/acp/dsh-sdk 对照 + 配置挂载（S5/S6/S7/S8）
4. 写自己的 provider：三段式 + 最小骨架 + capabilities/能力检查（S4 + S2）
5. 工具化：dsh-tool-subagent/-control/-report + maxDepth + 委托沙箱（S7/S9/S3）
6. 坑与速查：UNSUPPORTED_CAPABILITY、spawn 无父历史、outputSchema 不保证、冷恢复深度不可降、postmortem 0001（S2/S3/S5）

**素材锚点**：章节引用直接指向第 4 节的表号（如 S2-4.2-5 = zh 文档 prepareContinuable）；代码示例以 6.1/6.2/6.3 为底稿但需在 P4 写章时对照源码核实 6.1。

**未解决冲突**：6.1 骨架标注「综合推断」；「数量限制」标注未证实——两者在成稿时保持显式标注或删除。
