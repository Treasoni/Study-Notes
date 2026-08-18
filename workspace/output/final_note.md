# 如何写 DeepSeek-Harness hook 扩展点插件

- [[#第 1 章：导读与定位——本篇讲什么、不重复什么]]
- [[#第 2 章：语义模型——工具执行流水线与 next() 瀑布]]
- [[#第 3 章：五个扩展点逐个拆解——职责、类型与选型]]
- [[#第 4 章：实战起步——permission-gate 权限门]]
- [[#第 5 章：实战进阶——手写 guard / post-execute / result 三个示例]]
- [[#第 6 章：验证命令链——复用 08 章跑通]]
- [[#第 7 章：迁移对照——从 Claude Code hooks 到 dsh]]
- [[#第 8 章：小结与下一步]]

## 第 1 章：导读与定位——本篇讲什么、不重复什么

> [!summary] 本章导读
> 动手写代码前，先回答三个问题：本篇在系列里站在哪？哪些内容**不归本篇讲**？接下来怎么走？本章把坐标、边界、路线图一次说清，免得你带着 03 章「搬配置」的预期来读一篇「写代码」的教程。

### 1.1 系列坐标：01 章速览的教学落地

本篇是插件开发教程分册的第 11 章，任务是把你已经见过的「hook 扩展点」从**目录表格**变成**能跑的代码**。01 章 3.5 给了一张五个扩展点的速览表，每个点一句话用途；本篇把 `tools/pre-execute`、`ctx.tools.guard()`、`tools/execute`、`tools/post-execute`、`tools/result` 逐个讲透语义、逐个写出可运行的 TypeScript 插件[^c1-s2]。

> [!tip] 大白话
> 把 01 章的速览表想成**菜单**：只告诉你店里有哪些菜、一句话卖点。本篇是**后厨菜谱**：同一家店，教你把每道菜一步步做出来。看菜单五分钟，照着菜谱做菜要一小时。

### 1.2 与 03 章「配置实战」的边界

03 章讲**搬配置**：装 `@deepseek-ai/dsh-hooks-claude-code` 桥，把现成的 Claude Code `hooks.json` 用一行 `cordis.yml` 配置接进 dsh。本篇讲**写代码**：在 dsh 插件里用 `apply(ctx)` + `ctx.on(...)` 亲手实现扩展点，得到类型化返回、完整 `ctx`、无序列化边界的原生 hook[^c1-s1]。一句话分界：想「原样跑起现有 hooks」看 03；想「写新的、复杂的策略」读本篇。

### 1.3 三块结构预览：A → B → C

- **A 语义模型**（第 2–3 章）：地基。工具执行流水线的固定顺序、`next()` 瀑布、五个扩展点各自的职责与选型。
- **B 实战代码**（第 4–6 章）：主体。官方 permission-gate 起步 → 手写 guard / post-execute / result 三例 → 用 08 章验证命令链跑通。
- **C 迁移对照**（第 7 章）：决策。官方映射表、`updatedInput` 差异、配置桥限制，回答「何时搬配置、何时写代码」。

### 1.4 读者画像与前置

适合已读 01 章 3.5 + 系列 04–10 实战分册、熟悉 Claude Code 扩展体系（hooks / `settings.json` / `hookSpecificOutput`）的读者。本地 dsh 源码仓库就绪（clone → `pnpm install` → `pnpm run build`），命令统一在仓库根目录执行。

## 本章小结

> [!summary]
> - 本篇 = 01 章 3.5 hook 速览的教学落地：速览给目录表格，本篇给逐点代码；
> - 与 03 章边界：03 搬配置（配置桥），本篇写代码（`apply(ctx)` + `ctx.on`）；
> - 路线图 A→B→C：语义模型 → 实战代码 → 迁移对照；
> - 前置：01 章 3.5 + 04–10 分册 + 熟悉 Claude Code 扩展体系 + dsh 源码就绪。

下一章进入 A 块地基：工具执行不是黑盒，而是一条固定顺序的流水线——`next()` 瀑布从那里展开。

## 第 2 章：语义模型——工具执行流水线与 next() 瀑布

> [!summary] 本章导读
> 写 hook 扩展点之前，脑子里必须先装一张「工具执行地图」：一次工具调用从发起到收尾，会**依次**经过哪些点、每个点能做什么不能做什么。本章讲这张地图本身——流水线顺序、三类角色分工，以及贯穿所有决策点的 `next()` 瀑布语义。本章不写代码，类型签名集中到第 3 章。

### 2.1 工具执行不是黑盒：一条固定流水线

工具不是黑盒。模型决定调用工具后，执行会沿一条**固定顺序**的流水线走完，官方文档把这条流水线的阶段写死，不随插件乱序[^c2-pipeline]：

```text
模型请求调用工具
      │
      ▼
┌ tools/pre-execute ─────────┐  allow / deny / ask（决策点）
│  可变换瀑布                  │  ask 经 ctx.approval 呈现；无 mount → deny
└──────────┬─────────────────┘
           ▼
┌ ctx.tools.guard() ──────────┐  string = 最终 deny；undefined = 弃权
│  只否决，单调不可撤销          │
└──────────┬─────────────────┘
           ▼
┌ tools/execute ──────────────┐  包装 dispatch（超时 / 重试 / 指标）
└──────────┬─────────────────┘
           ▼
        工具体 execute()         ← 真活在这
           │
           ▼
┌ tools/post-execute ─────────┐  改汇报：替换 content 或 value
└──────────┬─────────────────┘
           ▼
        归一化 canonical 结果
           │
           ▼
┌ finalizeContent ────────────┐  definition-owned，恰一次，只换 content
└──────────┬─────────────────┘
           ▼
┌ tools/result ───────────────┐  只读观察不可变结果
└──────────┬─────────────────┘
           ▼
     durable `tool/result` 事件
```

这条顺序是**固定**的：扩展点不会乱序、不会跳过。你在哪个点能做什么，由流水线位置决定——这正是下一节三类角色要回答的。它同时也是插件间协作的契约：不同插件可以各自挂在不同的点上，互不抢跑道，各自只对自己负责的那一段生效。理解这点，读第 4–6 章的多扩展点叠加才不会晕。

### 2.2 三类角色分工

五个扩展点按「能对执行做什么」分成三类[^c2-roles]：

| 角色 | 扩展点 | 能做什么 |
|---|---|---|
| 可变换瀑布 | `pre-execute` / `execute` / `post-execute` | 改写执行流：跑前拦截 / 包装 dispatch、跑后换结果 |
| 只否决的 guard | `ctx.tools.guard()` | 只 deny-or-abstain，单调不可撤销 |
| 只读观察 | `finalizeContent` / `tools/result` | 只看不改：只换展示 content、观察不可变结果 |

- **可变换瀑布**：三个点都能**改写**执行流。`pre-execute` 在跑前做决策；`execute` 包装真实的 dispatch（加超时、重试、指标）；`post-execute` 在跑后替换给模型看的内容或返回值。
- **只否决的 guard**：不能改写任何东西，只能二选一——返回字符串 = 最终拒绝，返回 `undefined` = 弃权。它是「一票否决」，后面没人能翻案[^c2-guard]。
- **只读观察**：`finalizeContent` 只换给模型看的 content（动不了 canonical 值），且对每个归一化结果恰好执行一次；`tools/result` 观察不可变的 lossless-JSON 结果，用于审计、日志、指标[^c2-roles]。

> [!tip] 大白话
> 把流水线想成一条**餐厅出菜线**：`pre-execute` 是门口接单的领班（决定接不接）；`guard()` 是食品安全一票否决（说不合格就退菜，改不了）；`execute` 是大厨掌勺；`post-execute` 是摆盘换装（菜还是那道菜，但可以换摆盘给你看）；`finalizeContent` 是菜单上怎么写这道菜；`result` 是门口监控（只录像，碰不到菜）。三类角色的区别就是「能不能动手碰菜」。

### 2.3 next() 瀑布语义：委派放行 vs 短路拦截

`pre-execute` / `execute` / `post-execute` 是**串行瀑布**：同一扩展点上可以挂多个监听器，按注册顺序依次执行[^c2-waterfall]。每个监听器收到 `(exec, next)`，有两条路：

- **`return next()`** = 委派放行：把执行继续交给下一个监听器，一路放到底。这是「允许」的委派写法——官方 permission-gate 示例里放行就是这么写的，没有显式写 `{kind:'allow'}` 字面量[^c2-s2]。
- **不调用 next、直接 return 决策** = 短路拦截：当前监听器给出最终答复，后面的监听器不再执行。拒绝、请示都属于短路。

举个纯文字的例子：假设权限门上挂了两个监听器，第一个做黑白名单，第二个做按工具名的精细规则。`return next()` 让第一个放行后，第二个还能接着判断；一旦第一个 `deny`，第二个连参数都看不到——瀑布已经被短路（本例为依据 waterfall 语义构造的示意，非官方示例）。

> [!warning] 别踩的坑
> 短路不是「拒绝这一次」而是「瀑布到此为止」：一旦某个监听器 `return {kind:'deny'}`，后续监听器根本没机会跑。所以挂多个策略时，谁先谁后要想清楚（第 3、5 章展开）。

### 2.4 ask 决策：经 ctx.approval，无 mount 降级为 deny

`pre-execute` 的决策有三态（`PreToolDecision`）：`allow` 放行、`deny` 拒绝、`ask` 请示用户[^c2-decision]。其中 `ask` 不是自己弹窗——它由注入服务 `ctx.approval` 代为呈现；**如果当前没有挂载 approval 服务，`ask` 会降级为 `deny`**（宁可拒绝也不放行）[^c2-ask]。这也是 dsh「默认安全」取向的一个体现。

### 2.5 PreToolDecision 三态引入（细节留到第 3 章）

本节先把三态记下：`{kind:'allow'} | {kind:'deny', reason} | {kind:'ask', reason?}`[^c2-decision]。`deny` 必须带 `reason`（模型或用户要看得到原因）；`allow` 通常不写字面量——`return next()` 就是它的委派写法；`ask` 可带原因。三态和角色呼应：`allow` 让执行沿瀑布正常往下走，`deny` 是本点即可拦下，`ask` 把最终裁决交给 `approval` 服务。类型签名、`exec.arguments` 不可改写等约束，第 3 章逐个扩展点拆。

## 本章小结

> [!summary]
> - 工具执行走**固定流水线**：pre-execute → guard →（ask）→ execute → 工具体 → post-execute → 归一化 → finalizeContent → result → durable `tool/result` 事件；
> - 三类角色：**可变换瀑布**（pre/execute/post-execute）、**只否决 guard**（单调不可撤销）、**只读观察**（finalizeContent / result）；
> - `next()` 瀑布：`return next()` = 委派放行；直接返回决策 = 短路拦截；监听器按注册序串行；
> - `ask` 经 `ctx.approval` 呈现，**无 mount 时降级为 deny**；
> - `PreToolDecision` 三态：`allow / deny / ask`，`deny` 必带 reason，`allow` 常用 `return next()` 表达。

下一章把五个扩展点逐个拆开，给每个点的类型签名与最小写法——语义地图已就位，接下来开始认路。

## 第 3 章：五个扩展点逐个拆解——职责、类型与选型

第 2 章给了流水线全景，但「知道顺序」和「会选点」之间还有一道坎：五个扩展点看起来都能拦截工具，到底该用哪个？本章把 5 个扩展点加 `finalizeContent` 逐个拆开，讲清各自职责、决策/返回类型、触发时机与硬约束，最后给出一条选型口诀。

### 3.1 `tools/pre-execute`：权限门决策点

**职责**：流水线第一道决策门，在工具真正执行前运行，回答「这个工具调用允不允许」。做权限控制、拦截危险工具时，这是首选挂载点 [^c3-pipe]。

**决策类型** `PreToolDecision` 是三态 [^c3-pretype]：

```ts
type PreToolDecision =
  | { kind: 'allow' }                // 放行（更常见的委派写法是 return next()）
  | { kind: 'deny', reason: string } // 拒绝，reason 是给用户/模型的理由
  | { kind: 'ask', reason?: string } // 询问，走 ctx.approval 服务
```

**触发时机**：每次工具调用前，先于 guard 与 execute。`ask` 需要 `ctx.approval` 服务处于 mounted 状态；未挂载时降级为 `deny` [^c3-pretype]。

**关键约束**：**不能改写 `exec.arguments`**。这是与 Claude Code `updatedInput` 的关键差异 [^c3-limits]——S1 在 Known Limitations 里明确：记录/渲染的入参会与实际运行的入参脱同步。

> [!tip] 大白话
> 把 `pre-execute` 想成机场安检员：他只能决定「放行 / 拒载 / 叫领导来问（ask）」，但绝不能替你把行李箱里的东西换掉。所以他能决策，不能改 `exec.arguments` 里的工具入参。这也解释了为什么 dsh 没有 CC 那种 `updatedInput` 改入参的能力——改了，就没人知道工具实际跑的是哪份参数了。

最小写法（挂载在 `apply(ctx)` 内）：

```ts
// src/index.ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  if (isBlocked(exec)) {
    return { kind: 'deny', reason: '该工具调用被权限门拦截' }
  }
  return next() // 委派放行，等价于 allow
})
```

### 3.2 `ctx.tools.guard()`：一票否决的单调守卫

**职责**：只否决、不变换。签名是 [^c3-guard]：

```ts
ctx.tools.guard((execution) => string | undefined)
```

- 返回 `string` = 最终拒绝（final deny），该字符串即拒绝理由
- 返回 `undefined` = 弃权（abstain），交给后面的监听者继续判断

**语义关键点** [^c3-guard]：
- guard 是**单调（monotonic）**的：一旦某个 guard 返回字符串，后续 waterfall 监听者**不能撤销**——这是它与可变换监听器最本质的区别
- guard 不可重排：`ask` 决策先经 approval 解析，guard 在其后 [^c3-pipe]
- 被 guard 拒绝的工具调用会路由到 `tools/post-execute`（走失败路径），跳过工具体

> [!tip] 大白话
> 把 guard 想成公司的一票否决制保安队长：他说「不行」就是最终裁决，后面排队的人（其他监听者）没有翻案权；他说「我不管」（undefined）就相当于弃权，让下一个人决定。所以需要「谁都不能推翻的底线」时用 guard，而不是 pre-execute。

### 3.3 `tools/execute`：包装 dispatch

**职责**：包装工具调度（dispatch）环节，用来加超时、重试、指标采集。**硬约束**：只能替换 `exec.signal`（取消/超时信号），**不能换 `exec.arguments`**；canonical（权威）结果属于单一不可变 dispatch token [^c3-execute]。

```ts
ctx.on('tools/execute', async (exec, next) => {
  // 只能对 exec.signal 做手脚（如接超时兜底），arguments 不能动
  return next()
})
```

> [!tip] 大白话
> 把 execute 想成外卖平台的调度员：你能给骑手加一个「超时自动取消」的闹钟（换 signal），但改不了顾客点的菜（arguments）。订单的最终状态记录在唯一的订单号（dispatch token）上，方便追溯超时/重试次数。

### 3.4 `tools/post-execute`：显式结果变换

**职责**：工具跑完之后、归一化之前，对结果做显式变换。决策类型 `PostToolDecision` [^c3-poste]：

- `accept`：可替换 `content`（给模型看的文本）**或** `value`（结构化值），**两者二选一，不能同时换**；还可以附加 `additionalContexts`
- `block`：带 `feedback` 转为失败——valueless failure（没有返回值的失败）

```ts
ctx.on('tools/post-execute', async (exec, next) => {
  // 返回 accept（换 content 或 value，二选一）或 block（带 feedback）
  return next()
})
```

> [!tip] 大白话
> 把 post-execute 想成厨师出菜后的服务员：他要么改报菜名（content），要么换一道菜（value），但绝不能同时改两样；要是菜有问题，他可以整单退掉（block）并说明原因（feedback）。

### 3.5 `tools/result`：只读观察

**职责**：流水线最后阶段，订阅不可变的 lossless-JSON 结果，**只能看不能改**，用于审计、日志、指标 [^c3-result]。它是同步的 live notification（实时通知）。

```ts
ctx.on('tools/result', async (exec, result) => {
  // 只读：记录 result，不返回任何决策
})
```

> [!tip] 大白话
> 把 result 想成店里的监控摄像头：它把每一单完整录下来（lossless-JSON）供事后审计，但摄像头自己永远不会去改订单。

### 3.6 `finalizeContent`：definition-owned 内容收尾

**职责**：归 definition（工具定义）所有，对每个归一化结果**恰好执行一次**，只换 `content`，且必须同步、total（对任何输入都有确定返回，不抛异常）[^c3-finalize]。它不属于插件监听器，而是 `defineTool` 定义侧的一个配置项：

```ts
finalizeContent(content) {
  return `包装后的内容：${content}`
}
```

### 3.7 选型口诀与常见坑

五扩展点选型口诀（引述 S2 选择规则 [^c3-rules]）：

| 想做的事 | 选哪个 |
| --- | --- |
| 权限门：拦截危险调用 | `tools/pre-execute` |
| 单调最终拒绝，谁也翻不了案 | `ctx.tools.guard()` |
| 超时 / 重试 / 指标采集 | `tools/execute` |
| 改结果 / 附加上下文 | `tools/post-execute` |
| 只看不改（审计 / 日志） | `tools/result` |

常见坑：

1. **guard 与 pre-execute 叠加语义**：pre-execute 放行 ≠ 绕过 guard。guard 独立于 waterfall，仍可能一票否决，两者职责别混。
2. **post-execute 替换 vs result 只读的取舍**：要改给模型看的汇报 → post-execute；要留痕审计 → result。不要为了「顺便改一下」去用 result。
3. **卸载自动清理**：`ctx.on` 注册即 effect，插件卸载时自动清理，无需手动 removeListener。
4. **别用 pre-execute 改 arguments**：违反 S1 硬约束，会让记录与实际运行脱同步。

> [!summary] 本章小结
> - 五个扩展点按「能否变换」分三类：可变换瀑布（pre-execute / execute / post-execute）、只否决（guard）、只读观察（result / finalizeContent）。
> - `pre-execute` 三态 allow/deny/ask，不能改 `exec.arguments`。
> - `guard` 返回 string = 最终单调拒绝，undefined = 弃权，不可被后续监听者撤销。
> - `post-execute` 换 content 或 value 二选一；`result` 只读。
> - 选型口诀：权限门→pre-execute；最终拒绝→guard；超时重试→execute；改结果→post-execute；只看不改→result。

下一章把口诀落到代码：用官方唯一的 hook 插件示例 permission-gate 走一遍真实写法，再扩展成三态 + 可配置规则列表。

## 第 4 章：实战起步——permission-gate 权限门

第 3 章给了选型口诀：权限门落在 `tools/pre-execute`。这一章把官方唯一的 hook 插件示例 permission-gate 逐行拆开（先睹为快，再看逐段讲解），然后扩展成 allow/deny/ask 三态 + 可配置规则列表。

### 4.1 官方示例逐行拆解

官方 permission-gate 是 `dsh` 文档中唯一给出完整 TS 代码的 hook 插件示例 [^c4-official]。骨架如下（`isBlocked` 判断体是示意实现，签名与 deny/allow 行为依 S2 文档，`exec.arguments` 字段依 S1 语义）：

```ts
// src/index.ts —— permission-gate 骨架
import type { Context } from 'cordis'
import type { PreToolDecision } from '@deepseek-ai/dsh-tools'

export const name = 'permission-gate'

export function apply(ctx: Context) {
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    if (isBlocked(exec)) {
      return { kind: 'deny', reason: '该工具调用被权限门拦截' }
    }
    return next()
  })
}
```

逐行看：

- `ctx.on('tools/pre-execute', …)`：把监听器挂到流水线的权限门拦截点，每次工具调用前都会触发 [^c4-official]。
- `async (exec, next): Promise<PreToolDecision>`：监听器返回一个类型化决策对象；`exec` 是本次工具执行上下文，`next` 是瀑布的下一个监听器。
- `return { kind: 'deny', reason: '…' }`：**拒绝**。返回类型化对象，`reason` 是给用户/模型的拒绝理由，最终会进入失败路径。
- `return next()`：**放行**。把决策委派给下一个监听器；全部通过后，工具正常执行。

> [!note] 核心概念：为什么没有显式 `{kind:'allow'}` 字面量
> S1 的类型定义里 `PreToolDecision` 含 `allow` 分支，但 S2 官方示例里**没有出现 `{kind:'allow'}` 字面量**——放行统一写成 `return next()`。这是「`next()` 作为 allow 的委派写法」的体现：显式 `allow` 存在但少见 [^c4-wording]。

> [!tip] 大白话
> 把 permission-gate 想成小区门口新增的保安岗：`apply(ctx)` 是上岗手续，`ctx.on('tools/pre-execute', …)` 是保安站的岗亭位置。保安只有三种动作——挥手放行（`next()`）、抬手拒绝（`{kind:'deny'}`）、喊业主确认（`{kind:'ask'}`）。他不是外部安保公司的协议接口，就是小区自己的员工。

### 4.2 原生 hook = 普通 Cordis 插件

官方示例的关键定位：**原生 hook 就是一个普通 Cordis 插件，挂到某个拦截点，没有外部协议** [^c4-cordis]。这意味着：

- 不需要写 JSON 配置，不需要解析 `settings.json`，没有独立于插件体系的「hook 协议」
- 在 `apply(ctx)` 内用 `ctx.on(...)` 注册监听器即可
- 插件照常走 Cordis 的 mount/卸载生命周期，`ctx.on` 注册即 effect，卸载自动清理

三种决策的行为汇总（`ask` 行为呼应第 3 章）：

| 决策 | 写法 | 效果 |
| --- | --- | --- |
| allow（放行） | `return next()` | 交给下一个监听器，最终执行工具 |
| deny（拒绝） | `return { kind: 'deny', reason }` | 拦截，带拒绝理由 |
| ask（询问） | `return { kind: 'ask', reason? }` | 走 `ctx.approval`；无挂载时降级为 deny [^c4-pretype] |

### 4.3 扩展成三态 + 可配置规则列表

单一 `if` 的权限门很快不够用。参考真实社区插件 dsh-guardian 的「最严格者胜出：deny > ask > allow」策略 [^c4-guardian]，把判断拆成可配置规则列表，按文件职责分放：`src/index.ts` 做注册中心（挂载），规则函数拆到 `src/hooks/`。

**规则定义与合并逻辑**（`src/hooks/gate-rules.ts`）：

```ts
// src/hooks/gate-rules.ts —— 规则定义与合并逻辑
import type { PreToolDecision } from '@deepseek-ai/dsh-tools'

export type GateDecision = 'deny' | 'ask'

export interface GateRule {
  name: string
  match: (exec: ToolExecution) => boolean
  decision: GateDecision
}

// 最严格者胜出：deny > ask > allow
export function evaluateRules(
  exec: ToolExecution,
  rules: GateRule[],
): PreToolDecision | undefined {
  let asked: string | undefined
  for (const rule of rules) {
    if (!rule.match(exec)) continue
    if (rule.decision === 'deny') {
      return { kind: 'deny', reason: `命中规则「${rule.name}」` }
    }
    // ask 先暂存，继续找有没有更严的 deny
    asked = asked ?? `命中规则「${rule.name}」`
  }
  if (asked) return { kind: 'ask', reason: asked }
  return undefined // 未命中任何规则 → 放行（走 next()）
}
```

**挂载函数**（`src/hooks/permission-gate.ts`）：

```ts
// src/hooks/permission-gate.ts —— 挂载函数
import type { Context } from 'cordis'
import type { PreToolDecision } from '@deepseek-ai/dsh-tools'
import { evaluateRules, type GateRule } from './gate-rules'

export function applyPermissionGate(ctx: Context, rules: GateRule[]) {
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    const decision = evaluateRules(exec, rules)
    if (decision) return decision
    return next()
  })
}
```

**注册中心**（`src/index.ts`）：

```ts
// src/index.ts —— 注册中心：装配规则并挂载
import type { Context } from 'cordis'
import { applyPermissionGate } from './hooks/permission-gate'
import { SHELL_DANGEROUS_RULES } from './hooks/rules.shell'

export const name = 'permission-gate'

export function apply(ctx: Context) {
  applyPermissionGate(ctx, SHELL_DANGEROUS_RULES)
}
```

**示例规则**（`src/hooks/rules.shell.ts`，匹配逻辑为示意，按你要管控的工具 schema 调整）：

```ts
// src/hooks/rules.shell.ts —— 示例规则：拦截危险 shell 命令
import type { GateRule } from './gate-rules'

export const SHELL_DANGEROUS_RULES: GateRule[] = [
  {
    name: 'block-rm-rf',
    match: (exec) => String(exec.arguments?.command ?? '').includes('rm -rf'),
    decision: 'deny',
  },
  {
    name: 'ask-destructive-git',
    match: (exec) => String(exec.arguments?.command ?? '').includes('git push --force'),
    decision: 'ask',
  },
]
```

> [!example] 规则合并跑一遍
> 模型请求执行 `git push --force`：`block-rm-rf` 不命中，`ask-destructive-git` 命中 → 返回 `{kind:'ask'}`，走 approval。若某条命令同时命中一条 deny 和一条 ask 规则，返回 `{kind:'deny'}`——最严格者胜出。

> [!warning] 常见坑
> - 别把 `ask` 当成「更高级的 allow」：`ask` 无 approval 挂载时**降级为 `deny`**，不是放行 [^c4-pretype]。
> - 合并顺序不要先到先得：遇到 `ask` 先暂存，继续找有没有更严的 `deny`；遇到 `deny` 可立即短路返回。
> - `exec.arguments` 的具体字段（如 `command`）依实际工具 schema 而定，这里 `command` 只是示意字段，接入时先核对工具入参结构。

> [!summary] 本章小结
> - 官方 permission-gate = 一个 `ctx.on('tools/pre-execute', …)`：deny 返回 `{kind:'deny', reason}`，放行走 `return next()`。
> - 无显式 `{kind:'allow'}` 字面量：`next()` 是 allow 的委派写法（S2 示例 vs S1 类型的表述差异）。
> - 原生 hook 就是普通 Cordis 插件挂到拦截点，无外部协议，`apply(ctx)` 内注册。
> - 扩展三态 + 规则列表：`src/index.ts` 挂载，规则函数拆到 `src/hooks/`，按「最严格者胜出 deny > ask > allow」合并。
> - `ask` 无 approval 挂载时降级为 `deny`。

下一章挑战：guard / post-execute / result 这三个官方没有 TS 示例的扩展点，我们依据 S1 语义手写实现，并验证瀑布与观察点各自触发。

## 第 5 章：实战进阶——手写 guard / post-execute / result 三个示例

上一章的 permission-gate 只用到了 `pre-execute`。这一章手写剩下三个扩展点：`guard` 一票否决、`post-execute` 改汇报、`result` 只读观察，最后把四个扩展点叠进同一个 `apply(ctx)`，看瀑布与观察点如何各司其职。

> [!warning] 构造声明
> 官方 cookbook（S2）对 guard / post-execute / result 只有选择规则和功能表提及，**没有可运行的 TS 示例** [^c5-s2]。本章三例均依据 S1 语义自行构造 [^c5-s1]，字段名是 paraphrase，落地前对照 `@deepseek-ai/dsh-tools` 源码核一遍 [^c5-s4]。

### 5.1 guard：一票否决，后面监听者无法翻案

> [!tip] 大白话
> 把 guard 想成「保安的一票否决」：一个保安喊"不许进"就黄了，其他保安只能跟着反对或装没看见，**不能**放行。所以 guard 只有「拒绝」或「弃权」，没有「放行」。

S1 语义：`(execution) => string | undefined`；string = 最终单调 deny，undefined = abstain（弃权）；一旦 deny，后续监听者**无法撤销** [^c5-s1]。与 pre-execute 的区别：pre-execute 的 deny 可被更严格决策覆盖，guard 的 deny 是最终态，适合「不该发生」的硬底线。

> [!note] 基于 S1 语义构造（constructed from S1 semantics）
> S2 无 guard TS 示例，以下代码按 S1 的 guard 语义自行构造。

```ts
// src/hooks/guard.ts —— 基于 S1 语义构造（S2 无 guard TS 示例）
import { Context } from 'cordis'

export function installGuard(ctx: Context) {
  ctx.tools.guard((execution) => {
    // 返回 string = 一票否决
    if (execution.name === 'bash' && /rm -rf/.test(execution.arguments.command)) {
      return 'guard: 高危 bash 命令（rm -rf）被一票否决'
    }
    return undefined // 弃权，交给后续监听者 / 工具体
  })

  // 第二个监听者想「放行」也只能弃权——无法撤销上面的 deny
  ctx.tools.guard(() => undefined)
}
```

guard 也支持 agent-scoped：约束某个 agent 时，把 guard 挂到它的 `agent.ctx` 上。

```ts
// agent-scoped：用 agent.ctx 限定作用域（事件名为转述，以实际为准）
ctx.on('agent/created', (agent) => {
  agent.ctx.tools.guard((execution) => {
    if (execution.name === 'http') return '该 agent 禁止发起网络请求'
    return undefined
  })
})
```

### 5.2 post-execute：改汇报内容 / 换 value / block 转失败

> [!tip] 大白话
> 把 post-execute 想成「收银员打小票前先看一眼」：能改小票上的字（content）、把金额换成机器码（value），还能贴一张说明条（additionalContexts）；觉得有问题就拒绝出票并写明原因（block + feedback）。

S1 语义：`accept` 可替换 content **或** value（**不同时**）+ 附 `additionalContexts`；`block` 带 feedback 转 valueless failure [^c5-s1]。社区 dsh-guardian 正是用 post-execute 做凭据 redact，是真实落地佐证 [^c5-s7]。

> [!note] 基于 S1 语义构造（constructed from S1 semantics）
> S2 无 post-execute TS 示例，以下代码按 S1 的 PostToolDecision 语义自行构造。

```ts
// src/hooks/postExecute.ts —— 基于 S1 语义构造（S2 无 post-execute TS 示例）
import { Context } from 'cordis'

export function installPostExecute(ctx: Context) {
  ctx.on('tools/post-execute', async (exec, next): Promise<PostToolDecision> => {
    const decision = await next() // 等下游监听者 / 工具体跑完

    if (decision.kind === 'accept') {
      // 二选一：替换 content（给模型看的汇报文案）
      if (containsSecret(decision.content)) {
        return {
          ...decision,
          content: `[敏感字段已打码] ${redact(decision.content)}`,
          additionalContexts: [
            ...(decision.additionalContexts ?? []),
            { role: 'assistant', content: 'post-execute：敏感字段已脱敏。' },
          ],
        }
      }
      return { ...decision, value: normalizeValue(decision.value) } // 或换 value，不同时换
    }

    if (decision.kind === 'block') {
      return { kind: 'block', feedback: 'post-execute 校验未通过，工具调用按失败处理' }
    }

    return decision
  })
}
```

> [!warning] 字段名是 paraphrase
> `content` / `value` / `additionalContexts` / `feedback` 为 S1 语义转述，TS 类型以 `@deepseek-ai/dsh-tools` 源码为准 [^c5-s4]。

### 5.3 result：只读观察，只看不改

> [!tip] 大白话
> 把 result 想成「考场监控摄像头」：只能录，不能帮忙答题。拿到的是只读副本，可以存档、计数，但改不了模型看到的内容。

S1 语义：订阅**不可变 lossless-JSON 结果**，只能观察不能变换，同步 live notification [^c5-s3]。分工一句话：**要改汇报 → post-execute；只看不改成审计/指标 → result** [^c5-s2]。

> [!note] 基于 S1 语义构造（constructed from S1 semantics）
> S2 无 result TS 示例，以下代码按 S1 的 result 只读语义自行构造。

```ts
// src/hooks/resultObserver.ts —— 基于 S1 语义构造（S2 无 result TS 示例）
import { Context } from 'cordis'

export function installResultObserver(ctx: Context) {
  // 只读观察：订阅不可变结果做审计 / 日志 / 指标，不 return
  ctx.on('tools/result', (result) => {
    auditLog.push({ tool: result.name, at: Date.now(), snapshot: result })
    metrics.inc(`tool.call.${result.name}`)
  })
}
```

### 5.4 叠加：pre-execute + guard + post-execute + result 共存

把三个手写示例和上一章的权限门叠进同一个 `apply(ctx)`，验证瀑布与观察点各自触发 [^c5-s3]。

```ts
// src/index.ts —— 一个插件里 4 类扩展点共存
import { Context } from 'cordis'
import { installGuard } from './hooks/guard'
import { installPostExecute } from './hooks/postExecute'
import { installResultObserver } from './hooks/resultObserver'

export function apply(ctx: Context) {
  // 1) pre-execute 权限门
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    if (exec.name === 'bash' && /rm -rf/.test(exec.arguments.command)) {
      return { kind: 'deny', reason: 'pre-execute: 高危命令' }
    }
    return next() // 委派放行
  })

  installGuard(ctx)          // 2) guard 一票否决
  installPostExecute(ctx)    // 3) post-execute 改汇报
  installResultObserver(ctx) // 4) result 只读审计
}
```

触发顺序对齐第 2 章流水线：pre-execute → guard →（execute）→ 工具体 → post-execute → finalizeContent → result；deny 命中时短路到 post-execute、跳过工具体 [^c5-s3]。

### 5.5 卸载自动清理

> [!note] effect 语义
> `apply(ctx)` 里 `ctx.on(...)` / `ctx.tools.guard(...)` 注册的都是 **effect**：卸载时自动 dispose，无需手动 `removeListener`。所以注册必须写进 `apply(ctx)`，写在 apply 外框架管不到。

> [!summary] 本章小结
> - guard：返回 string = 一票否决，undefined = 弃权；后续监听者无法撤销；agent-scoped 挂到 `agent.ctx`。
> - post-execute：accept 替换 content **或** value（二选一）+ 附 `additionalContexts`；block 带 feedback 转失败。
> - result：只读观察不可变结果，做审计 / 日志 / 指标，不能变换。
> - 四类扩展点可叠加在同一个 `apply(ctx)`，按流水线位置各自触发；deny 短路跳过工具体。
> - `ctx.on` 注册即 effect，卸载自动清理，无需手动 removeListener。

下一章预告：代码写完要能证明它真的挂上了——第 6 章用验证命令链跑通，并教你怎么观测 hook 行为、排查扩展点不触发的问题。

## 第 6 章：验证命令链——复用 08 章跑通

上一章写完了四个扩展点，怎么证明它们真的挂上了？这一章复用教程 08 章的验证命令链，从「加载」到「端到端」四步跑通，并教你观测 hook 行为、排查扩展点不触发的问题。

> [!note] 来源说明
> S1–S9 中没有任何一条给出验证命令链（S2 的 runnable wirings 也缺这套）[^c6-s2]。本命令链**显式复用本教程第 8 章**，命令统一在 dsh 仓库根目录执行。

### 6.1 验证四连（复用 08 章）

```bash
# 第 1 步：加载检查 —— 插件能被 dsh 识别并加载
pnpm dsh web --patch
# 第 2 步：配置层 —— 确认插件配置合并进当前 profile
pnpm dsh --dump-config
# 第 3 步：bundle 默认 —— 确认产物内置的默认配置
pnpm dsh --dump-default-config
# 第 4 步：端到端 —— headless 跑一次真实调用，验证权限门真的拦截
pnpm dsh --profile headless
```

四步分工：第 1 步验「插件被加载」，第 2 步验「配置层生效」，第 3 步验「打包默认值」，第 4 步验「真实调用里的行为」。

### 6.2 怎么观测 hook 行为

**用 console.log 加载日志确认扩展点挂载**：在 `apply(ctx)` 每个注册点打一行加载日志，看到日志 = 扩展点确实挂上了。

```ts
export function apply(ctx: Context) {
  ctx.on('tools/pre-execute', async (exec, next) => {
    console.log('[dsh-guard] pre-execute 已挂载') // 加载期日志
    /* … */
  })
  ctx.tools.guard(() => {
    console.log('[dsh-guard] guard 已挂载')
    return undefined
  })
}
```

**用 headless 端到端验证权限门真的拦截**：输入一条含 `rm -rf` 的命令，预期走 deny。若 guard / pre-execute 正确拦截，模型不会被授予执行、调用以拒绝结束，退出码与「未装插件放行」时不同——对比跑一次即可看出差异。社区 dsh-guardian 也是用类似脚本验证 deny / redact 行为的 [^c6-s7]。

### 6.3 常见排查

- **扩展点没触发**：检查 `ctx.on` / `ctx.tools.guard` 是否在 `apply(ctx)` **内部**注册——写在 apply 外的监听器不属于插件生命周期，不会挂载。
- **依赖没就绪**：`inject` 注入的服务是否在 `apply(ctx)` 里声明可用；依赖未就绪时注册会失败或被跳过。
- **验证顺序错**：第 4 步 headless 跑不通前，先确认第 1 步加载日志已出现，缩小排查范围。

> [!summary] 本章小结
> - 验证四连复用 08 章：加载 → `--dump-config` → `--dump-default-config` → headless 端到端。
> - `console.log` 加载日志 = 确认扩展点已挂载；headless = 验证权限门真实拦截（deny 时模型被拒、退出码语义）。
> - 扩展点不触发先查两处：`ctx.on` 是否在 `apply(ctx)` 内注册、`inject` 依赖是否就绪。

下一章预告：跑通之后，第 7 章看如何把现有 Claude Code hooks 迁移到 dsh——官方映射表、updatedInput 差异与配置桥限制。

## 第 7 章：迁移对照——从 Claude Code hooks 到 dsh

如果你手里已经有一堆 Claude Code hooks 配置，能直接搬到 dsh 吗？能搬多少、哪些搬不过去、搬过去后行为是否一致？本章用官方 `dsh-hooks-claude-code` 配置桥（S5）的映射表回答这些问题，并给你一个「走桥还是手写」的判断标准。

### 7.1 官方映射表：六类事件一次对上

官方桥给出的映射表很简洁，Claude Code 的 6 类常用事件都有落点 [^c7-1]：

| Claude Code 事件 | dsh 扩展点 | 属性 |
| --- | --- | --- |
| `PreToolUse` | `tools/pre-execute` | waterfall 决策点 |
| `PostToolUse` | `tools/post-execute` | waterfall 决策点 |
| `UserPromptSubmit` | `agent/pre-step` | waterfall 决策点 |
| `Stop` | `agent/turn-stopping` | waterfall 决策点 |
| `SessionStart` | `agent/session-start` | emit 观察 |
| `SubagentStart` | `subagent/start` | emit 观察 |
| `SubagentStop` | `subagent/end` | emit 观察 |

对照第 2–3 章的语义模型就能看懂：左半边（工具、提示词、回合结束）在 dsh 侧都是「决策点」，右半边（会话/子代理生命周期）是「观察点」。这正好对应 7.6 的 emit vs waterfall 分界。

### 7.2 支持范围：约 7 个，其余在解析前忽略

官方桥**只支持约 7 个事件**，其余一律忽略 [^c7-2]。注意：这不代表配置加载会失败——**不支持的 hook 事件在 group 解析前就被忽略，不会使整条桥配置失效**。也就是说，你的 `settings.json` 里混着 20 个不支持的 matcher，桥照样能跑，只是那些事件永远不触发。

> [!warning] 别纠结「30 还是 31」
> 官方桥文档写的是「CC 当前 30 个事件里的 23 个不支持」，而 CC 官方参考页面的事件表列了 31 个。两个数字对不上，是**来源时间点不同**造成的口径差。教学上记得「约 7 个支持 / 其余不支持」这个结论即可，别把绝对总数当铁律。

### 7.3 `updatedInput` 差异：改写不了入参，就走「附加 context」模式

这是迁移时最容易踩的坑。Claude Code 的 hook 可以通过 `hookSpecificOutput.updatedInput` **改写工具入参**（比如给 `Bash` 悄悄加上 `--no-input`），这是 CC 的招牌能力 [^c7-3]。

dsh **没有对应能力**。回到第 3 章讲过的那条：`tools/pre-execute` 不能改写 `exec.arguments`，否则记录/渲染的参数会与实际运行脱同步。既然改写不了，就把「想改什么」用 `additionalContexts`（post-execute）或注入上下文**附加给下游**，让模型或后续决策点自己判断，而不是静默替换入参 [^c7-4]。

> [!tip] 大白话
> 把 `updatedInput` 想成「偷改顾客的订单」——CC 允许 hook 在厨房里把菜悄悄换掉；dsh 不允许改单，只许你在订单上**贴一张备注纸条**，由做菜的人（下游）自己决定怎么处理。所以迁移时别问「怎么改入参」，要问「怎么把改写意图传下去」。

### 7.4 配置桥限制：能跑什么、不能跑什么

即使走了官方桥，也不是所有 CC hook 配置都能照搬。S5 明确列出三处限制 [^c7-5]：

1. **只有 shell-form `type: 'command'` 的 handler 会执行**；`http` / `mcp_tool` / `prompt` / `agent` 这四类 handler 解析后直接跳过并打告警。
2. **分层发现 + live reload 未实现**：CC 侧 project/user/plugin/policy 四层自动合并、配置热更新，桥都不做——`configPath` 必填，进程级解析一次，相对启动目录读取。
3. **匹配 handler 串行执行、不去重**：CC 是并行 + 按 event+matcher 去重，桥是逐条串行跑，同一命令可能被执行多次。

顺带一提：`UserPromptSubmit` 过桥时用的是 600s 超时，而不是 CC 事件专属的 30s [^c7-5]。

### 7.5 桥 vs 手写代码：怎么选

桥的价值是**快**：现有 CC 命令型 hook 配置，填个 `configPath` 就能跑。但它的天花板正好卡在 7.3 / 7.4：不能类型化决策、不能改参、handler 类型受限、串行不去重。

- **什么时候走官方桥（S5）**：存量 CC 配置以 `command` handler 为主，先让它在 dsh 里「活过来」，不追求行为完全一致。
- **什么时候手写插件（本篇主线）**：需要 `guard()` 单调否决、`post-execute` 改汇报、`result` 审计、`PreToolDecision` 类型化决策——这些桥给不了，只能在 `apply(ctx)` 里写代码。

> [!warning] 小心第三方桥的「原样运行」
> 社区有 `dsh-bridges`（S9）宣称 CC hooks 能「原样运行」，但它是无映射表的黑盒，仅 registry 核实、代码未核 [^c7-6]。官方桥至少逐事件列了映射和已知限制；对「原样运行」这种一口应承的宣称，迁移前务必自己逐事件验证一遍。

### 7.6 emit vs waterfall：两类触发的本质区别

映射表最后补一刀：同样是「支持」，两类事件在 dsh 里的语义完全不同 [^c7-1]。

- **emit（不可阻塞，仅注入/观察）**：`SessionStart`、`SubagentStart`、`SubagentStop`——dsh 只负责把事件广播给监听者，监听者不能拦住流程，只能做注入或观察。
- **waterfall / serial（决策点）**：`PreToolUse`、`PostToolUse`、`UserPromptSubmit`、`Stop`——每个监听者都能参与决策，`next()` 串行瀑布，返回决策对象短路拦截。

把 CC 的 `PreToolUse` 迁移到 `tools/pre-execute` 后，你得到的不只是「能触发」，而是「能像第 4–5 章那样返回 `deny/ask`、走 `next()` 瀑布」的完整决策能力——这就是手写比桥更值的场景。对照示例：

```json
// Claude Code settings.json（CC 侧写法，桥可直接读这类配置）
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "node guard-bash.js" }
        ]
      }
    ]
  }
}
```

```ts
// dsh 手写等价物（本篇主线写法）
// src/index.ts
export const apply = (ctx: Context) => {
  ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
    if (exec.tool === 'Bash' && dangerous(exec.arguments)) {
      return { kind: 'deny', reason: 'guard-bash: dangerous command blocked' };
    }
    return next(); // 放行 = CC 里 command handler 正常退出
  });
};
```

> [!summary] 本章小结
> - 官方桥把 CC 6 类事件映射到 dsh 扩展点：决策类走 `tools/pre-execute`、`tools/post-execute`、`agent/pre-step`、`agent/turn-stopping`，生命周期类走 `agent/session-start`、`subagent/start|end`。
> - 支持约 7 个事件，其余**解析前忽略**，配置不失效；绝对总数「30 vs 31」是来源时间点口径差，不必纠结。
> - `updatedInput` 改写入参在 dsh 无对应能力，改走「附加 context + 下游决策」模式。
> - 桥只执行 `command` handler、无分层发现/live reload、串行不去重——适合快速迁移存量配置，深度控制还得手写。
> - emit 类（生命周期）不可阻塞，waterfall 类（工具/提示/停止）才是真正决策点。

下一章我们收个尾：把 5 个扩展点的选型口诀、本篇产出文件清单和 4 项开放问题汇总成一张「下一步」地图。

## 第 8 章：小结与下一步

到这一章，我们从语义模型一路走到了迁移对照。收个尾：把 5 个扩展点的选型口诀、本篇产出文件清单、与 01 章 3.5 速览的闭合关系，以及接下来的路整理成一张地图。

### 8.1 五扩展点选型口诀

第 3 章引用了官方选型规则 [^c8-1]，第 4–5 章逐条落地。完整口诀如下：

| 需求 | 选型 |
| --- | --- |
| 权限门（allow / deny / ask） | `tools/pre-execute` |
| 单调最终拒绝（一票否决） | `ctx.tools.guard()` |
| 超时 / 重试 / 指标（包装 dispatch） | `tools/execute` |
| 改结果 / 附加 context | `tools/post-execute` |
| 只看不改（审计 / 日志） | `tools/result` |

> [!tip] 大白话
> 把这 5 个扩展点想成「5 个工位」：要进门找 `pre-execute`，要一票否决找 `guard()`，要包一层防护找 `execute`，要改汇报找 `post-execute`，只想记台账找 `result`。每个需求对应一个工位，别走错门。

### 8.2 本篇产出文件清单

- `src/index.ts`：注册中心，在 `apply(ctx)` 里挂载 4 类扩展点（`pre-execute` 权限门 + `guard()` + `post-execute` 改汇报 + `result` 审计）。
- `src/hooks/`：规则与变换函数（危险命令分类、redact、内容替换逻辑），与注册中心解耦。
- 验证命令链：复用 08 章四连——`pnpm dsh web --patch` 验加载 → `--dump-config` 验配置层 → `--dump-default-config` 验 bundle 默认 → `pnpm dsh --profile headless` 验端到端拦截 [^c8-2]。

### 8.3 与 01 章 3.5 速览闭合

《插件开发核心》01 章 3.5 给了 hook 扩展点目录速览表；本篇就是它的**教学落地**——速览里的一行行扩展点，在第 2–6 章被拆成流水线语义、类型签名和可运行插件。如果你能回头把 3.5 表格里的每个点对应到本章的口诀，这套知识就闭环了。

### 8.4 下一步

- **参照社区插件**：S7 `dsh-guardian`（实测插件，`deny > ask > allow` 最严格胜出 + `post-execute` redact，是最佳落地样板）、S8 `dsh-permission-rules`（声明式规则）、S9 `dsh-bridges`（第三方桥，代码未核，谨慎）[^c8-3]。
- **4 项开放问题**（来自深研交接，待你动手时核对）[^c8-4]：① `PostToolDecision` 的 accept「content/value 二选一」具体字段名，建议直接核 `@deepseek-ai/dsh-tools` 类型源码；② `tools/result` 与 durable `tool/result` 事件在 agent loop 里的消费方；③ `ctx.approval` 的 `ask` 交互在 CLI/UI 如何呈现；④ 桥不支持的事件（23 个）是否值得整理成一张迁移附录表。

> [!summary] 全篇收束
> - 选型口诀是决策入口：权限门、单调否决、包装、改汇报、只读观察各归其位。
> - 产出 = 注册中心 + 规则函数 + 验证四连，三者缺一不可。
> - 本篇补完了 01 章速览与 03 章配置实战之间缺失的「写代码」一环。
> - 下一步从社区插件读源码、从 4 项开放问题里挑一个亲手验证，就是最好的巩固。

至此，你已具备从零手写 dsh hook 扩展点插件、并用验证链跑通的能力。去写你的第一个权限门吧。

## 参考资料

[^c1-s2]: S2「扩展插件形态 Cookbook」——官方 hook 扩展点选择规则与唯一 permission-gate 示例所在源；本篇定位为 01 章 3.5 的教学落地（2026-08 master HEAD）。
[^c1-s1]: S1「dsh-tools 工具作者参考」——原生 hook 的类型化返回、完整 `ctx`、无序列化边界等语义的定义源（2026-08 master HEAD）。
[^c2-pipeline]: S3「工具执行流水线」§ Tool Execution Pipeline——固定顺序：pre-execute → 单调 guard →（ask 经 `ctx.approval`）→ execute → 工具体 → post-execute → 归一化 → finalizeContent → result → durable `tool/result` 事件（2026-08 master HEAD）。
[^c2-roles]: S3 § Tool Execution Pipeline——三个 transformable waterfall（pre-execute / execute / post-execute）、guard 只 deny-or-abstain、finalizeContent 仅内容、`tools/result` 只读观察。
[^c2-guard]: S1「dsh-tools 工具作者参考」§ dsh-tools/guard + S3 stage 4——guard 签名 `(execution) => string | undefined`，返回 string = 最终单调 deny，undefined = abstain，后续 waterfall 监听者不能撤销。
[^c2-waterfall]: S1 § dsh-tools/guard——waterfall 串行与「后续监听者」表述来自此源；「按注册顺序」为本篇依据 waterfall 语义作出的推断（S1/S2 未逐字给出）。
[^c2-s2]: S2「扩展插件形态 Cookbook」§ a-hook-plugin-permission-gate-example——放行走 `return next()`、deny 返回 `{kind:'deny', reason}`，示例无显式 allow 字面量。
[^c2-decision]: S1 § Injected services / Key types——`PreToolDecision = {kind:'allow'} | {kind:'deny', reason} | {kind:'ask', reason?}`。
[^c2-ask]: S1 § Injected services——ask 由 `ctx.approval` 服务，无 mount 时降级为 deny。
[^c3-pipe]: S3 § Tool Execution Pipeline：固定顺序 `tools/pre-execute` → 单调 guard →（ask 经 `ctx.approval`）→ `tools/execute` → 工具体 → `tools/post-execute` → 归一化 → `finalizeContent` → `tools/result` → durable `tool/result` 事件。
[^c3-pretype]: S1 § Injected services / Key types：`PreToolDecision = {kind:'allow'} | {kind:'deny', reason} | {kind:'ask', reason?}`；`ask` 由 `ctx.approval` 服务，无挂载时降级为 `deny`。
[^c3-limits]: S1 § Known Limitations：`tools/pre-execute` 不能改写 `exec.arguments`，记录/渲染参数会与实际运行脱同步——与 CC `updatedInput` 的关键差异。
[^c3-guard]: S1 § dsh-tools/guard；S3 stage 4：`ctx.tools.guard()` 签名 `(execution) => string | undefined`；返回 string = 最终单调 deny，undefined = abstain；后续 waterfall 监听者不能撤销。
[^c3-execute]: S1 § Key types：`tools/execute` 包装 dispatch，仅可替换 `exec.signal`，不可换 arguments；canonical 结果属单一不可变 dispatch token。
[^c3-poste]: S1 § Key types：`PostToolDecision` accept 可替换 content 或 value（不同时）+ 附加 additionalContexts；block 带 feedback 转 valueless failure。
[^c3-result]: S1 § dsh-tools；S3 stage 14：`tools/result` 观察不可变 lossless-JSON 结果，不能变换；同步 live notification。
[^c3-finalize]: S1 § Key types：`finalizeContent` definition-owned，对每个归一化结果恰一次，只换 content，必须同步且 total。
[^c3-rules]: S2 § a-hook-plugin-permission-gate-example（引述 adding-a-tool.md）：选择规则引语——单调最终拒绝用 `guard()`；包装 dispatch（超时/重试/metrics，仅 signal 可换）用 `execute`；显式结果变换用 `post-execute`；只读观察用 `result`。
[^c4-official]: S2 § a-hook-plugin-permission-gate-example：官方唯一 hook 插件示例，`ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`；deny 返回 `{kind:'deny', reason}`，allow 走 `next()`。判断体为示意实现，签名与行为依 S2 文档。
[^c4-wording]: S1 § Key types vs S2 示例：`PreToolDecision` 类型含 `allow` 分支，但官方示例无显式 `{kind:'allow'}` 字面量，`next()` 是 allow 的委派写法。
[^c4-cordis]: S2 § a-hook-plugin-permission-gate-example：原生 hook 是普通 Cordis 插件挂到拦截点，无外部协议；`apply(ctx)` 内注册。
[^c4-pretype]: S1 § Injected services / Key types：`PreToolDecision` 三态；`ask` 由 `ctx.approval` 服务，无挂载时降级为 `deny`。
[^c4-guardian]: S7 § Policy behavior（dsh-guardian）：pre-execute 将危险命令分类 deny/ask/unchanged，「最严格者胜出 deny > ask > allow」。
[^c5-s1]: S1 — dsh-tools 工具作者参考（packages/core/tools/README）：guard 的 `(execution) => string | undefined` 语义、PostToolDecision 的 content/value/additionalContexts、result 只读观察，均为本章构造示例的依据。
[^c5-s2]: S2 — 扩展插件形态 Cookbook（docs/cookbook/extension-cookbook）：唯一官方 TS 示例是 permission-gate；guard/post-execute/result 只有选择规则与功能表提及，无 TS 代码。
[^c5-s3]: S3 — 工具执行流水线（docs/tool-execution-pipeline）：固定顺序 pre-execute→guard→execute→post-execute→finalizeContent→result；guard 不可重排、denial 短路到 post-execute、result 只读。
[^c5-s4]: S4 — @deepseek-ai/dsh-tools（npm）：类型包存在性已核实（0.1.0-rc.6），代码未直接核实；PostToolDecision 字段名以源码为准。
[^c5-s7]: S7 — dsh-guardian（社区插件，lonelymoon87）：pre-execute 分类 deny/ask/unchanged、post-execute 做凭据 redact，是 guard + post-execute 组合的真实落地佐证。
[^c6-s2]: S2 — 扩展插件形态 Cookbook（docs/cookbook/extension-cookbook）：runnable wirings 不含 load / dump-config / headless 验证命令链，故本章复用教程 08 章。
[^c6-s7]: S7 — dsh-guardian（社区插件，lonelymoon87）：自带脚本验证 deny / redact 行为，是「跑一遍证明行为」这一验证思路的实践佐证。
[^c7-1]: S5 官方 `dsh-hooks-claude-code` README 映射表与 emit/waterfall 说明（packages/hooks/hooks-claude-code，master HEAD，2026-08）。
[^c7-2]: S5 README unsupported-events：「Unsupported hook events (23 of Claude Code's current 30)」，事件在 group 解析前忽略。
[^c7-3]: S6 Claude Code Hooks reference：`hookSpecificOutput` 含 `permissionDecision`/`additionalContext`/`updatedInput`/`systemMessage`，输出 cap 10,000 字符。
[^c7-4]: S1 dsh-tools Known Limitations：`tools/pre-execute` 不能改写 `exec.arguments`；S5 partial-support 亦确认。
[^c7-5]: S5 README config / partial-support：仅 shell-form `command` 执行，`http`/`mcp_tool`/`prompt`/`agent` 跳过并告警；分层发现 + live reload 未实现；串行不去重；`UserPromptSubmit` 600s 超时。
[^c7-6]: S9 dsh-bridges（npm，v0.1.0，2026-08-15）：第三方桥，宣称 CC hooks 原样运行，无映射表；仅 registry 核实，代码未核。
[^c8-1]: S2 extension-cookbook 选择规则（引述 adding-a-tool.md）：单调最终拒绝用 `guard()`；包装 dispatch 用 `execute`；显式结果变换用 `post-execute`；只读观察用 `result`。
[^c8-2]: S2 确认无验证命令链，复用本教程 08 章验证四连（load → dump-config → dump-default-config → headless）。
[^c8-3]: S7 dsh-guardian（实测社区插件，target DSH 0.1.0-rc.6）；S8 dsh-permission-rules（registry 核实 v0.4.2，代码未核）；S9 dsh-bridges（registry 核实 v0.1.0，代码未核）。
[^c8-4]: 开放问题 4 项见 `02_deep_research.md` Open Questions：PostToolDecision 字段名、result 消费方、ask 交互呈现、桥不支持事件附录。
