# 第四章 写自己的 provider——三段式与最小实现

> [!summary] 导读
> 第 1 章给了「能力缝 + 三层结构」的地图，第 2 章把 `SubagentProvider` 契约逐字段拆开，但还没有一行能跑的代码。这一章把「写一个自己的 provider」从方法论落实到可运行骨架：先讲官方三段式怎么拆包、怎么命名、怎么设计（my-cap 三件套）；再给一个最小 `SubagentProvider` 骨架逐行拆解，并诚实标注哪些是「综合推断」、发布前要对照哪份源码；接着区分 `start()` 的 in-process 与 out-of-process 两条实现路径，讲清 effect-scoped 注册与卸载；最后给出三个写 provider 必踩的坑和 Claude Code 迁移映射。读完你就能照着骨架写一个能注册、能挂进插件树的 provider。

## 4.1 三段式方法论：三个包怎么拆、怎么命名、怎么设计

第 1 章 §1.5 说过「完整能力本身才是接缝，单一角色不是」——写一个 dsh 能力，就是按 ①②③ 三段把三件套补齐。[^S4-4.9-1] 这一节把它变成可操作的三条指令。

### 4.1.1 三件套代码走读（官方 my-cap 示例）

官方开发者实践教程用 `my-cap` 做了完整示范，三个包、三段代码：[^6.2]

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

- **① 定义包 `dsh-my-cap`**：`MyCapService` 是一个 cordis `Service` 子类，`super(ctx, 'myCap')` 把服务注册成 `ctx.myCap`；`execute(request): Promise<MyCapResult>` 是抽象签名，定义「调用方要传什么、会拿回什么」。[^S4-4.9-1] 6.2 代码里没展开但属于定义包的还有两样：`MyCapRequest` / `MyCapResult` 类型定义，以及 `declare module` 把 `ctx.myCap` 扩展进 `Context` 类型（这样消费方写 `ctx.myCap.execute(...)` 有类型提示）。这三样合起来才是「契约」。这套 cordis Service + `defineTool` 的写法与 [[DeepSeek-Harness 插件开发核心]] 里的插件结构同源。
- **② Provider 实现包 `dsh-my-cap-local`**：`MyCapLocal extends MyCapService` 真把 `execute` 实现了（这里就是 `input.toUpperCase()`）；`export function apply(ctx) { ctx.plugin(MyCapLocal) }` 是 cordis 插件入口，把实现挂上服务点。换实现 = 换这个包，定义和消费不动。
- **③ Consumer/Tool 包 `dsh-tool-my-cap`**：`export const inject = ['tools', 'myCap']` 声明这个插件要注入 `tools` 服务（用于注册工具）和 `myCap` 服务（用于调能力）；`defineTool({...})` 描述工具的形状；`ctx.tools.register(...)` 把它挂进工具表，模型就能调了。[^S4-4.9-1]

> [!tip] 大白话
> 把三件套想成「打印机生态」：定义包是 USB 接口标准（我的接口长这样、数据怎么传）；provider 是各家驱动（惠普的、佳能的，都实现同一个标准）；consumer/tool 是你电脑上的「打印」按钮。所以……换驱动不用换按钮，按钮只认标准——这就是「provider 与 consumer 只依赖定义包」的实际手感。

### 4.1.2 命名律：dsh-<cap> / <cap>-local / dsh-tool-<cap>

三件套的包名不是随便起的，官方命名律如下：[^S4-4.9-2]

| 角色 | 包名模式 | my-cap 实例 | subagent 家族实例 |
| --- | --- | --- | --- |
| ① Service Definition | `dsh-<cap>` | `dsh-my-cap` | `dsh-subagent` |
| ② Provider | `<cap>-local` | `dsh-my-cap-local` | `dsh-subagent-spawn-in-process` / `-fork` / `-acp` / `-dsh-sdk` |
| ③ Consumer/Tool | `dsh-tool-<cap>` | `dsh-tool-my-cap` | `dsh-tool-subagent` |

subagent 系列是这条律的忠实执行者：定义 `dsh-subagent`，工具 `dsh-tool-subagent`，各 provider 是 `dsh-subagent-<实现>`。你写自己的 provider 时，包名照 `<cap>-local` 或 `dsh-subagent-<实现>` 的样子起，别人一眼能看出它在三层里站哪层。

### 4.1.3 设计要点：三句官方戒律

三段式不只是「拆三个包」，官方还给了三条设计戒律：[^S4-4.9-3]

1. **Do not split preemptively（不要预防性拆包）**。三件套是目标架构，不是起步强制——只有某个角色需要**独立演进**（不同团队、不同发布节奏、要被单独复用）才把它拆成独立包。对 subagent 来说这条尤其省事：定义包 `dsh-subagent` 和工具包 `dsh-tool-subagent` 官方已经给你了，你写自己的 provider 时**只写 ②**，①③ 直接复用。你的「三段式」实际上是「一段半」：写 provider 包，配置里把工具指到你的 `name`。
2. **Request / Result 类型归定义包所有**。跨缝流动的数据形状只能由定义包定义，provider 与 consumer 都从定义包 import，谁也不准自己发明一份。这就是第 1 章「只依赖定义包」的类型级保证——换 provider 不换类型。
3. **默认值在显式 `resolve(request): Spec` 里处理，不在 `run()` 里藏 `?? default`**。请求在进入实现前先被规范化成一个完整 Spec；`run()` / `start()` 只处理已经解析好的值，不隐含 fallback。这样行为可预测、可单测，也避免「同样的入参在不同 provider 里默认值不一样」。

> [!tip] 大白话
> 把「不要在 run() 里藏默认值」想成餐厅后厨：下单（request）先经过前台收银系统（resolve）补全「默认少辣、默认热饮」，再递给后厨；后厨（run）只按单做菜，不再自己猜「要不要加辣」。所以……所有「没写就怎样」的逻辑集中在 resolve 一处，后厨永远拿到完整订单，出菜才一致。

## 4.2 最小 provider 骨架逐行拆解（综合推断标注）

现在把方法论套到 subagent 上：写一个 provider 包，`apply` 里 `ctx.subagents.registerProvider(...)`。

> [!warning] 综合推断标注
> **官方目前没有独立的「SubagentProvider 教程」**。下面这份骨架是把 S2 的契约定义（`name` / `capabilities` / `inheritsParentContext` / `start` / `prepareContinuable`）与 S4 的三段式拼合出来的**综合推断**，不是官方原样代码。[^6.1] 尤其 `start()` 里「经 `ctx.agents` 创建 child」这一句，**发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码核实**。[^S8]

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

- **import**：契约类型（`SubagentProvider` / `ResolvedSubagentStartRequest` / `SubagentRun`）全部从定义包 `@deepseek-ai/dsh-subagent` import，不从 provider 或 consumer 拿——这是 4.1.3 戒律②的类型级落地。[^S2-4.2]
- **`name`**：provider 在注册表里的身份证。`dsh-tool-subagent` 的 `config.provider` 字段拿它当值（例如配 `provider: my-provider` 就调到你）；`getProvider('my-provider')` 也靠它。重名注册会失败。[^S2-4.2]
- **`capabilities: {}`**：启动期静态声明。空对象是合法声明，意思是「四个可选启动能力我都不支持」。要支持哪个就写哪个（如 `{ outputSchema: true }`）；**不声明却收到对应请求 → `UNSUPPORTED_CAPABILITY` 响亮拒绝**（坑②，见 4.5）。[^S2-4.3]
- **`inheritsParentContext: false`**：描述性标注（第 2 章 §2.2.3 揭开的悬念）。spawn 类（全新 child）写 `false`，fork 类（从父对话种子启动）写 `true`。它只担保「对话种子」，不担保工具/服务/权限。[^S2-4.2]
- **`start()`**：真正干活的地方。输入是 `ResolvedSubagentStartRequest`——服务已经做完能力校验、解析好 descriptor，provider 拿到的不是裸请求。返回 `Promise<SubagentRun>`，**发布后**才 resolve handle；发布前失败要清理未发布资源（坑③）。两条实现路径见 4.3。[^S2-4.2]
- **`prepareContinuable?`（可选）**：**方法存在即能力**——服务端用 TypeScript 类型收窄发现「这 provider 支持续写」，不是查开关字段。它只返回 `ContinuableCreateSpec`（目前仅可选父历史种子 `seed`），不含 Agent/handle/投递/结果/dispose/恢复——那些归服务管。不写这个方法的 provider 只服务 one-shot 委托。[^S3-4.2-5]
- **`export const name` + `export function apply(ctx)`**：cordis 插件入口约定。`apply` 是必须的入口；`name` 是可选元数据。注意这里有两个「name」容易混：包级的 `export const name` 是插件名，provider 对象里的 `name` 是注册名——别写串。
- **`ctx.subagents.registerProvider(myProvider)`**：把 provider 挂上注册表。因为写在 `apply` 的插件作用域里，**effect-scoped**——插件卸载时自动注销（4.4 展开）。[^S2-4.2]

> [!tip] 大白话
> 把这份骨架想成「入职登记表」：`name` 是工号（唯一），`capabilities` 是写在胸牌背面的「我会什么」（没写的能力就别说会），`inheritsParentContext` 是「要不要带旧公司的交接文档」，`start()` 是「入职第一天真正开始干活」。所以……骨架的核心不是「写对每一行」，而是「把每行当成一次对服务端的承诺」——承诺了能力就得兑现，没承诺的请求会被当场拒绝。

## 4.3 start() 的两条实现路径：in-process 与 out-of-process

`start()` 的写法取决于 child 跑在哪：同一个进程，还是独立子进程。这两条路径是第 3 章「in-process vs out-of-process 大分流」在 provider 写作侧的对应物。[^S8][^S5][^S6]

| 维度 | in-process | out-of-process |
| --- | --- | --- |
| child 在哪 | 同进程，经 `ctx.agents` 创建 | 独立子进程 |
| 握手 | 无（同进程直接调用） | 有：ACP `initialize` / SDK `initialize` |
| 启动期能力 | 可全支持（spawn/fork 四项全开） | 通常全 false（无法远程强制） |
| 继承父上下文 | fork 可带对话种子 | 每次全新进程，无继承 |
| 成本 | 低 | 高（dsh-sdk 起完整 peer harness 更贵） |
| 典型样板 | `spawn` / `fork` | `acp` / `dsh-sdk` |

### 4.3.1 in-process：经 ctx.agents 创建 child

in-process 的 provider（如 `spawn`）在**同一进程**里经 `ctx.agents` 创建 child。[^S8] 因为是同进程，child 可以直接访问宿主进程里的服务、工具、注册表，所以 spawn 能把四个启动期能力**全开**（结构化输出、深度强制、工具过滤、persona 都是「进程内能强制」的事）。[^S8] 骨架里那句 `// in-process：经 ctx.agents 创建 child` 对应的就是这条路。

这一步的精确 API（`ctx.agents` 怎么调、child 怎么发布成 `SubagentRun`）官方没有独立教程，**必须对照 `subagent-spawn-in-process` 源码核实**——这正是发布前要做的核实动作。[^6.1] 方向性语义 S2 已经给足：child 建立后要先「发布」到运行状态，然后才 resolve `SubagentRun`；发布前失败要清理。[^S2-4.2]

### 4.3.2 out-of-process：spawn 子进程 → 握手

out-of-process 的 provider（`acp` / `dsh-sdk`）走另一条路：[^S5][^S6]

1. **spawn 子进程**：用配置的命令启动一个新进程（`acp` 起一个 ACP 客户端进程，`dsh-sdk` 起一个完整 peer harness runtime）。
2. **握手**：进程起来后先做协议握手——ACP 是 `initialize` 交换协议版本与能力；SDK 是 stdio JSON-RPC 的 initialize。握手之后才能开始委派 turn。
3. **返回 run**：握手成功后把「会话句柄」封装成 `SubagentRun` 返回。

因为能力被「远程化」了，out-of-process 的 provider **启动期能力通常全 false**——你没法在子进程外强制它的深度/过滤/persona/结构化输出。[^S5-4.7-3] 这也解释了第 2 章的能力表：`acp` 不声明任何 start-time capabilities，本地服务收到带这些选项的请求会拒绝而非静默忽略。

两个 out-of-process 的工程细节（写 provider 时照抄）：[^S5-4.7-6][^S5-4.7-7][^S6-4.7-6][^S6-4.7-7]

- **环境变量卫生**：子进程环境先**擦除「凭据形状」的变量与陈旧的 `DSH_*` 名**，再合并显式 `config.env`——避免把宿主进程的敏感环境意外泄漏给子进程。
- **cwd 规则**：配置了 `cwd` 就用配置值（load 时校验一次）；没配就用**委托方父会话的 cwd**——**绝不用 server 进程自身的 cwd**。子进程跑在哪个目录是委托语义的一部分，不能想当然。

> [!tip] 大白话
> 把 in-process vs out-of-process 想成「在自己家做饭 vs 点外卖」：自己家做饭（in-process），锅碗瓢盆都是现成的，想做多精细都行（能力全开），但得自己动手；点外卖（out-of-process），得先下单选店（spawn 子进程）、确认接单（握手 initialize），到了才能吃，而且「要几分辣」这种精细要求（能力）很多店做不了。所以……要能力全选 in-process（spawn/fork），要隔离或驱动外部协议选 out-of-process（acp/dsh-sdk）。

## 4.4 registerProvider：effect-scoped 注册与卸载

骨架里 `apply(ctx)` 内的 `ctx.subagents.registerProvider(myProvider)` 不是普通 map 赋值，而是挂在**当前 cordis effect 作用域**上的注册（第 2 章 §2.1.1 讲过语义）。[^S2-4.1]

对写 provider 的人，这带来一个免费福利：**你不需要写任何「注销」代码**。插件被卸载（手动停、热重载、生命周期结束）时，注册跟着 effect 作用域一起撤销。对应的语义是：

- **移除 provider**（effect 结束）：阻止**新的** start 请求，但**不撤销已经返回的 run**——已经跑起来的 child 继续跑到自然结束。
- 所以「卸载」不是「立即杀死」，是「不再接受新委托」。

这一点也呼应第 1 章「微内核主张」：你的 provider 只是挂在一个已文档化扩展点上的监听者，挂多久、什么时候摘，由 effect 生命周期说了算。

> [!note] 这在 Claude Code 里相当于
> Claude Code 里删掉 `.claude/agents/*.md` 文件，subagent 就消失了；dsh 里「卸载」由插件生命周期自动处理，且效果更温和——已派出去的 run 不会被连坐杀掉，跑完才结束。

## 4.5 三个坑：写 provider 必踩

写 provider 有三个已知坑，前两个在写之前就该知道，第三个是写 `start()` 时的卫生纪律。[^S5-4.9-4][^S6-4.9-4][^S2-4.2]

### 坑① 无默认导出：Cordis loader 解包会隐藏命名 inject 元数据

> [!warning] 埋坑 ①：subagent 相关包无默认导出
> subagent 相关包**没有默认导出**。Cordis loader 解包时，默认导出会把命名 `inject` 元数据藏起来（postmortem 0001 记录过这个坑）。所以写 consumer/provider 包时：**只用命名导出**（`export const name`、`export const inject`、`export function apply`），不要 `export default`。`inject` 尤其关键——loader 靠它知道要注入哪些服务，写成默认导出就看不见了。[^S5-4.9-4][^S6-4.9-4]

### 坑② capabilities 不声明 → UNSUPPORTED_CAPABILITY

> [!warning] 埋坑 ②：capabilities 不声明 = 请求被拒
> `capabilities` 是启动期**静态声明**。你 `capabilities: {}` 留空，就等于承诺「四个可选能力我都不支持」；这时任何带 `outputSchema` / `maxDepth` / `toolFilter` / `persona` 的 start 请求都会被 `UNSUPPORTED_CAPABILITY` 响亮拒绝（第 2 章 §2.3.1）。想支持哪个，就声明哪个并真正兑现——「声明了却不实现」和「没声明却被请求」都是 bug。[^S2-4.3]

### 坑③ start() 发布前失败必须清理未发布部分资源

> [!warning] 埋坑 ③：发布前失败不得留孤儿
> `start()` 的语义是「先发布 child，再 resolve handle」。如果 child 还没发布成功就失败，**必须把已经创建的那部分资源清理掉再 reject**——比如你已经 spawn 了子进程，却在握手阶段出错，那就得把子进程 dispose/kill，不能让它变成孤儿进程。官方把「fulfill 前失败须清理未发布部分资源」写成硬性要求，不是建议。[^S2-4.2]

> [!tip] 大白话
> 把坑③想成「装修被叫停」：你装了一半（创建了子进程/child），突然发现手续不全（握手/初始化失败），这时候不能扭头就走留下半拉子工地——得把已经装的部分拆掉还原（dispose），再跟业主说做不了。所以……`start()` 里「先分配后发布」的资源，每一份都要有对应的失败清理路径，一个都不能漏。

## 4.6 从 Claude Code subagent 迁移映射

这一章最后，把「写 dsh provider」映射回你最熟的 Claude Code 侧。Claude Code 里你「自定义 subagent + 脚本工具」做的事，到 dsh 被拆成了 provider 插件 + 工具实例。

| Claude Code | DeepSeek-Harness |
| --- | --- |
| `.claude/agents/*.md` 角色文件（description + system prompt） | `SubagentProvider` 契约对象（`name` + `capabilities` + `start()` 里把 prompt 交给 child） |
| 框架从文件自动发现 subagent | 显式 `ctx.subagents.registerProvider` + cordis 插件挂载（`cordis.patch.yml`）[^S4-4.9-1] |
| md 里限制可用工具（`tools:`） | `capabilities.toolFilter` + `agentOptions` / `toolFilter` 选项 |
| 模型通过 `task` 工具调用 subagent | `dsh-tool-subagent`（`config: { provider: 你的name }`）绑定你的 provider |
| 「运行」由框架内置执行器完成 | 你的 `start()` 实现（in-process / out-of-process） |
| 脚本工具 = 一个可执行入口 | consumer 包里的 `defineTool` + `ctx.tools.register` |

迁移心智一句话：**Claude Code 的 md 角色声明对应 dsh 的 `SubagentProvider` 契约声明**，但 dsh 把「角色声明」「执行引擎」「调用入口」拆成了三段——你在 Claude Code 里只写 md（声明），框架替你跑；在 dsh 里你得自己写 `start()`（执行引擎），再用现成的 `dsh-tool-subagent` 当调用入口。Claude Code 帮你隐掉的「执行」这一段，正是 dsh 换后端只改一行配置的前提。[^S4-4.9-1]

具体落地到「迁移一个现有 Claude Code subagent」：

1. 把 md 里的**角色名** → provider 的 `name`。
2. 把 md 里声明的**能力 / 工具限制** → `capabilities` + 启动时按 `request.agentOptions` / `toolFilter` 施加约束。
3. 把 md 里的**system prompt** → `start()` 创建 child 时注入的 prompt（配合 `request.prompt`）。
4. 把「模型怎么叫它」→ 复用 `dsh-tool-subagent`，`config.provider` 指到你的 `name`。

这一步映射做完，你对「写 dsh provider」的心智就和「写 Claude Code subagent」对上了——只是多了一层你要自己实现的 `start()`。挂载与配置细节（`cordis.patch.yml` 怎么插）见 [[DeepSeek-Harness 配置体系]] 与第 3 章。

## 本章小结

- 三段式方法论：① 定义包（抽象 Service 类 + Request/Result 类型 + `declare module`）→ ② Provider 实现包（`export function apply(ctx){ ctx.plugin(...) }`）→ ③ Consumer/Tool（`inject: ['tools','cap']` + `defineTool` + `ctx.tools.register`）；命名律 `dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>`。
- 三条设计戒律：Do not split preemptively（角色独立演进才拆包）；Request/Result 类型归定义包所有；默认值在显式 `resolve` 里处理，不在 `run()` 藏 `?? default`。
- 最小 provider 骨架 = `name` / `capabilities` / `inheritsParentContext` / `start()` / 可选 `prepareContinuable` + `apply` 里 `ctx.subagents.registerProvider`。骨架为 S2+S4 **综合推断**，`start()` 发布前须对照 `subagent-spawn-in-process` 源码核实。
- `start()` 两条路径：in-process（经 `ctx.agents` 同进程创建 child，能力可全开）vs out-of-process（spawn 子进程 → ACP/SDK initialize 握手 → 返回 run，能力通常全 false；注意环境变量卫生与 cwd 规则）。
- `registerProvider` 是 effect-scoped 注册：插件卸载自动注销，移除阻止新 start、不撤销已返回 run。
- 三个坑：① 无默认导出（loader 解包藏 inject 元数据）② capabilities 不声明 → UNSUPPORTED_CAPABILITY ③ start() 发布前失败必须清理未发布资源。
- Claude Code 迁移：md 角色声明 = SubagentProvider 契约声明；执行引擎从「框架内置」变成「你的 start()」。

## 与 Claude Code 对照

| 维度 | Claude Code | DeepSeek-Harness |
| --- | --- | --- |
| 声明 subagent | `.claude/agents/*.md` 一个角色文件 | `SubagentProvider` 对象 + `registerProvider` |
| 能力约束 | md frontmatter 隐含 | `capabilities` 四 flag 静态声明，缺则拒 |
| 执行引擎 | 框架内置，不可换 | 你的 `start()`，可选 in-process / out-of-process |
| 模型调用面 | 框架自动暴露 | `dsh-tool-subagent`（`config.provider` 绑定） |
| 脚本工具 | 可执行入口 | `defineTool` + `ctx.tools.register` |
| 卸载/清理 | 文件删除即消失 | effect-scoped 自动注销，但已跑 run 不撤销 |

迁移心智：Claude Code 把「声明 + 执行 + 调用面」压进一个 md 文件，框架替你跑；dsh 把它们拆成三段，执行那段要你亲自写 `start()`。代价是更陡的起步曲线，收益是执行后端从「不可换」变成「配置一个字符串」——你在 Claude Code 里写自定义 subagent 的心智（角色声明），正好对应 dsh 的契约声明，只是多了「实现执行」这一层。

## 更新记录

- **2026-08-16（成稿）**：本章基于 developer preview（2026-08-13 锚点）官方文档撰写。4.2 最小骨架为 **S2 契约 + S4 三段式综合推断**，官方无独立 SubagentProvider 教程；发布前必须对照 `packages/subagent/subagent-spawn-in-process` 真实源码核实 `start()` 的 in-process 实现。若 preview 更新改变三段式命名律、`SubagentProvider` 字段或 postmortem 0001 结论，本章 4.1-4.2、4.5 受影响，优先对照检查。

---

[^S4-4.9-1]: S4 · Three-role capability design §4.9-1——三段式三步走（定义包 → Provider → Consumer/Tool，含 `inject` + `defineTool` + `ctx.tools.register`）。
[^S4-4.9-2]: S4 §4.9-2——命名律（`dsh-<cap>` / `<cap>-local` / `dsh-tool-<cap>`）。
[^S4-4.9-3]: S4 §4.9-3——设计要点（Do not split preemptively、Request/Result 类型归定义包、默认值在显式 resolve）。
[^S2-4.1]: S2 · Subagent 子系统设计文档（中文）§4.1——`ctx.subagents` 注册表（registerProvider effect-scoped、移除阻止新 start、不撤销已返回 run）。
[^S2-4.2]: S2 §4.2——SubagentProvider 契约（name/capabilities/inheritsParentContext/start、发布后返回 handle、发布前失败清理）。
[^S2-4.3]: S2 §4.3——SubagentStartRequest 选项与能力检查（UNSUPPORTED_CAPABILITY 响亮失败）。
[^S3-4.2-5]: S3 · `@deepseek-ai/dsh-subagent` 核心包 README §4.2-5——prepareContinuable 存在即能力、只返回 ContinuableCreateSpec、冷恢复不经 provider 分发。
[^S8]: S8 · `subagent-spawn-in-process` README——in-process provider 样板（ctx.agents 创建 child、启动期能力全支持）。
[^S5]: S5 · `dsh-subagent-acp` README——out-of-process provider 样板（ACP 客户端驱动、initialize 握手）。
[^S5-4.7-3]: S5 §4.7-3——acp 不声明任何 start-time capabilities，本地服务拒绝而非静默忽略。
[^S5-4.7-6]: S5 §4.7-6——环境变量卫生（先擦除凭据形状变量与陈旧 `DSH_*` 名，再合并 `config.env`）。
[^S5-4.7-7]: S5 §4.7-7——cwd 规则（配置值或委托方父会话 cwd，绝不用 server 进程自身 cwd）。
[^S5-4.9-4]: S5 §4.9-4——subagent 相关包无默认导出（Cordis loader 解包隐藏命名 `inject` 元数据，postmortem 0001）。
[^S6]: S6 · `dsh-subagent-dsh-sdk` README——out-of-process provider 样板（stdio JSON-RPC 驱动、完整 peer harness、initialize 握手）。
[^S6-4.7-6]: S6 §4.7-6——环境变量卫生（同上，dsh-sdk 侧）。
[^S6-4.7-7]: S6 §4.7-7——cwd 规则（同上，dsh-sdk 侧）。
[^S6-4.9-4]: S6 §4.9-4——无默认导出坑（同上，dsh-sdk 侧）。
[^6.1]: 实操指南 6.1——最小 provider 骨架（S2+S4 综合推断，发布前对照 spawn-in-process 源码核实）。
[^6.2]: 实操指南 6.2——S4 官方 my-cap 三件套示例。
