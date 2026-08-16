---
title: "DeepSeek-Harness system-prompt 插件实战：代码级加人格与指令"
tags: [deepseek-harness, ai, agent, 插件, system-prompt, 教程]
created: 2026-08-16
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness system-prompt 插件实战：代码级加人格与指令

> [!summary] 导读
> [[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|插件开发核心 §3.6]] 讲了 system-prompt 子系统的**概念**（PromptSection、order 约定、complete、遮蔽、事件）；这篇专讲**怎么写**：第一段能抄的代码、六个注册 API、按 order 落笔、text 三种写法、`complete` 独占、作用域遮蔽、事件监听与避坑。
>
> 与 [[DeepSeek-Harness 插件开发教程/12-实战-写自己的AgentPreset|第 12 章]] 的分工：**第 12 章是配置级**（改 preset 的 `agent.cordis.yml`，不写代码）；**本篇是代码级**（写 TypeScript 插件调 `ctx.systemPrompt.section(...)`）。两条路径都能加人格/指令，选哪条看你想要「静态装配」还是「可编程逻辑」。

## 0. 一分钟结论

- **代码级加人格/指令** = `ctx.systemPrompt.section({ name, order, text })`，写在 `apply(ctx)` 里，走 Cordis effect 自动清理（卸载即摘除）；
- **常用 order 位**：`-100` harness 身份 → `0` 部署人格 → `100–199` 工具指导，其他负数在人格前；
- **`complete: true`** = 这段独占整份系统提示词，多个生效段会让组装失败；
- **作用域遮蔽**：作用域级的 section / context / variable 盖掉全局同名项，**tools 例外**（全局 + 作用域共同贡献）；
- **方法名**：官方是 `section()`，不是 `register()`（§3.6 早期写法已更正，见 [[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|§3.6]]）。

## 1. 最小人格插件：第一段能抄的代码

```ts
// src/index.ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'persona-plugin'
export const inject = ['systemPrompt']   // 服务依赖：systemPrompt 就绪才加载（见 3.3）

export function apply(ctx: Context) {
  ctx.systemPrompt.section({
    name: 'persona',
    order: 0,                  // 0 = 部署人格（order 约定见 §3）
    text: '你是一个有耐心的中文学习助手。',
  })
}
```

> **代码放哪**：`src/index.ts` 的 `apply(ctx)` 里（注册中心）；`name` / `inject` 在文件顶部。提示词段本体如果变复杂，可以抽到 `src/services/` 或 `src/prompts/` 独立文件，`apply` 里只留注册动作——和工具、服务同一套「注册中心 vs 本体」分工。

`section()` 返回 **Cordis effect disposer**：插件卸载时自动摘除这段提示词，不需要手动清理（3.2 的 effect 规则）。

> [!tip] 大白话
> `apply(ctx)` 是入职第一天，`ctx.systemPrompt.section(...)` 就是往公司「发言稿」里加你部门的一段。`order: 0` 表示这段话排在「人格位」——每次调模型，框架把各段按 order 从小到大拼成一份系统提示词，这段就在人格位置。

## 2. 注册 API 全貌：是 `section` 不是 `register`

> [!warning] 方法名更正
> [[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|§3.6]] 早期写法是 `ctx.systemPrompt.register({...})`——官方实际方法是 **`ctx.systemPrompt.section({...})`**（2026-08-16 抓取核对）。下面以官方为准。

`ctx.systemPrompt` 是「每次模型调用前组装系统提示词」的注册表服务，六个方法[^1]：

| 方法 | 作用 | 返回 |
|---|---|---|
| `section(section)` | 注册一段**有序提示词**（最常见） | disposer |
| `context(context)` | 注册**动态模型上下文**（user-role 持久快照） | disposer |
| `variable(name, provider)` | 提供 `{{name}}` 的**插值值** | disposer |
| `tools(provider)` | 为一次组装贡献**工具 schema** | disposer |
| `suppressRuntimeContext()` | 抑制运行时上下文注入 | disposer |
| `assemble(context)` | **手动组装**一次系统提示词（验证用） | `Promise<PromptAssembly>` |

- 全部「注册即 effect」：插件卸载自动清理，无需手动注销；
- `tools()` 通常不用自己调——工具注册后 schema 会自动流入组装[^3]（见 §3.3）。

> [!tip] 大白话
> `section` 是主入口，其余是配套：`context` 放「每次都带上的动态背景」，`variable` 给 `{{占位符}}` 供值，`tools` 管工具说明书，`assemble` 是「手动彩排」——你可以在代码里先拼一遍看看效果。

## 3. 按 order 落笔：三个常用档位

order 升序拼接，框架约定几档「标准位」[^1]：

| order | 角色 | 谁写 |
|---|---|---|
| `-100` | harness 身份 | 框架内置，通常别碰 |
| 其他负数 | 身份之后、**人格之前** | 想在人格前插入的指令 |
| `0` | 部署人格 | 你的 persona 插件（§1 示例） |
| `100–199` | 工具指导 | 工具 schema 自动流入；插件可手动补充 |

### 3.1 人格位：`order: 0`

即 §1 的最小示例，不重复。

### 3.2 人格前指令：负数 order

想放一段「必须先说、盖在人格前面」的约束（比如安全红线、公司政策）：

```ts
ctx.systemPrompt.section({
  name: 'pre-persona-policy',
  order: -10,                  // 负数 → 拼在人格（0）之前
  text: '涉及删除或覆盖用户数据时，必须先向用户确认。',
})
```

### 3.3 工具指导：`100–199`

注册工具后，schema **自动流入**系统提示词组装[^3]，通常不用手动写。但你可以补一段「工具使用守则」：

```ts
ctx.systemPrompt.section({
  name: 'tool-guidance',
  order: 150,                  // 100–199 = 工具指导区
  text: '使用 bash 工具时，先判断命令在 Windows 上是否可用，不可用则换等价方案。',
})
```

> [!tip] 大白话
> order 就是发言稿的**排座位表**：身份（-100）坐最前面，然后是你加的人格前指令（负数），接着人格（0），最后工具使用说明（100–199）压轴。排座号越小越靠前。

## 4. text 三种写法

`text` 可以是静态字符串、函数、或带 `{{variable}}` 占位符的字符串[^1]：

```ts
// ① 静态字符串：每次组装原样使用
text: '你是一个有耐心的中文学习助手。',

// ② 函数：每次组装时用 AssembleContext 求值（context.scope 是官方字段）
text: (context) =>
  context.scope ? `你正工作在作用域 ${context.scope}。` : '你是全局助手。',

// ③ 字符串 + {{variable}}：渲染期由 renderPrompt 插值，值由 variable() 提供
text: '今天是 {{today}}。',
ctx.systemPrompt.variable('today', () => '2026-08-16')
```

- **插值时机**：`{{variable}}` 不是注册时就替换，而是**组装渲染期**由 `renderPrompt` 插值[^1]——所以 provider 可以每次组装返回不同值；
- **变量命名**：必须匹配 `[a-z][a-z0-9_]*`，非法或重复的名字会抛错；
- **引用未定义变量会失败**：provider 返回 `undefined` 时，渲染引用该变量的 section 会失败——宁可返回空字符串也别返回 undefined。

> [!tip] 大白话
> 三种写法 = 三种「写稿方式」：① 写死（印刷体）；② 现场念（每次临时算）；③ 留白填空（稿子上写 `{{today}}`，到时候有人把今天的日期填进去）。留白要小心：填的人说「没有」，整段稿子就念不下去了。

## 5. `complete: true`：独占整份系统提示词

`complete: true` 表示「这段就是完整系统提示词」。组装仍会跑协作瀑布（让 tools / contexts / variables 都解析完），**之后**把这段恢复为唯一提示词段——所以工具还能用，但其他插件的文字段会被排掉[^1]。

```ts
ctx.systemPrompt.section({
  name: 'solo',
  order: 0,
  text: 'You are a minimal agent. Do one thing at a time.',
  complete: true,
})
```

- **超过一个生效的 complete 段 → 组装失败**；
- complete 段在 `system-prompt/assemble` 瀑布**之后**恢复，所以瀑布监听者也无法给它加东西或替换它。

> [!tip] 大白话
> 开会时有人说「都别说了，按我这份稿子来」——其他人准备的段落全不算数，但「工具」这类基础设施照常运转。要是两个人同时喊这句话（多个 complete），会议直接开不下去（组装失败）。

## 6. 作用域与遮蔽：作用域级盖全局

规则[^1]：

| 提供方 | 遮蔽规则 |
|---|---|
| `section` | 作用域级段**遮蔽**全局同名段；同一层内重名抛错 |
| `context` | 作用域级项**遮蔽**全局同名项 |
| `variable` | 作用域级值**遮蔽**全局同名变量 |
| `tools` | **例外**：全局与匹配作用域的 provider **共同贡献** |

作用域由 `AssembleContext.scope` 标识：有 scope 时，该作用域的 provider 和瀑布监听者参与；没有 scope 时，只有全局 provider 和「无 subject」的监听者参与[^1]。

```ts
// 全局（host 组合）注册的 persona
ctx.systemPrompt.section({ name: 'persona', order: 0, text: '全局人格' })

// 某个 agent 作用域里注册的同名 persona → 在该 agent 的组装中遮蔽全局版
ctx.systemPrompt.section({
  name: 'persona',
  order: 0,
  text: '作用域人格：你只处理前端问题。',
})
```

- 重复注册同名段**不是**静默覆盖：同一层内直接抛错；
- 非有限 order（如 `NaN` / `Infinity`）也会抛错[^1]。

> [!tip] 大白话
> 遮蔽 = 部门规则盖过公司规则：子公司（作用域）说「我们这里是这么写的」，就按子公司的来；但「工具」像水电煤——子公司和总公司各交各的费，两边都通（共同贡献）。

## 7. 事件监听：assemble 瀑布与 change 广播

两个事件[^1]：

```ts
// system-prompt/assemble：瀑布式，返回值为权威
// 作用域过滤：scoped 监听者只收到该 scope 的组装
ctx.on('system-prompt/assemble', async (assembly, context, next) => {
  // 读或改 assembly（例如统一追加一段公司政策）
  return next()   // 不修改就放行，让瀑布继续
})

// system-prompt/change：广播式，任何提供方变化时触发（全局变化影响所有 scope，不做过滤）
ctx.on('system-prompt/change', () => {
  console.log('system prompt 提供方有变化')
})
```

- `assemble` 的**返回值是权威**：监听者返回的 assembly 就是最终结果（唯一例外：complete 段之后仍会恢复独占）；
- `change` 用于缓存失效、UI 刷新、日志等「提示词变了」的通知场景。

> **代码放哪**：`ctx.on(...)` 写在 `src/index.ts` 的 `apply(ctx)` 里，与注册段同级。

> [!tip] 大白话
> `assemble` 是**评审会**：每段念完，下一个评委还能改，最后一个评委说了算（返回值权威）。`change` 是**广播**：有人说「稿子改了」，大家各自去刷新（缓存、界面），谁都能听见。

## 8. 避坑清单

| 坑 | 说明 |
|---|---|
| `register` 不是方法 | 官方是 `section()`；§3.6 早期写法已更正 |
| 同名段重复注册 | 同一层内直接抛错，不是静默覆盖 |
| 多个 `complete: true` | 生效段超过一个 → 组装失败 |
| `knownNames` | 工具配置校验用它区分「名字拼写错误」与「已知但被有意隐藏」的工具[^1] |
| 变量名不合法 | `{{x}}` 必须匹配 `[a-z][a-z0-9_]*`，非法/重复抛错 |
| provider 返回 `undefined` | 渲染引用该变量的 section 会失败 |
| 非有限 order | `NaN` / `Infinity` 之类直接抛错 |

## 9. 验证：怎么确认提示词真的拼进去了

- **手动组装**：在插件代码或调试脚本里调 `await ctx.systemPrompt.assemble({ scope })`，打印返回的 `PromptAssembly`，看你的段是否按预期顺序出现在结果里[^1]；
- **实机观察**：启动 dsh 进入会话，看系统提示词是否包含你的 text；
- **监听确认**：临时挂一个 `system-prompt/change` 监听，注册/卸载段时确认事件真的触发了。

## 本章小结

> [!summary]
> - 代码级加提示词 = `ctx.systemPrompt.section({ name, order, text })`，**不是 register**；注册即 effect，卸载自动清理；
> - order 约定：`-100` 身份 → 负数人格前指令 → `0` 人格 → `100–199` 工具指导；
> - `text` 三种写法：静态串 / `(context) => string` / `{{variable}}`（渲染期由 `renderPrompt` 插值，provider 别返回 `undefined`）；
> - `complete: true` 独占整份提示词，多个生效段组装失败；
> - 遮蔽：作用域级 section/context/variable 盖全局，**tools 例外**（共同贡献）；
> - 事件：`system-prompt/assemble`（瀑布，返回值权威）+ `system-prompt/change`（广播）；
> - 配置级（preset）走 [[DeepSeek-Harness 插件开发教程/12-实战-写自己的AgentPreset|第 12 章]]，代码级走本篇。

相关：[[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|插件开发核心（概念图）]] → 本篇（代码级实战）→ [[DeepSeek-Harness 插件开发教程/12-实战-写自己的AgentPreset|第 12 章（配置级实战）]]。

---

## 更新记录

- 2026-08-16：新建。依据官方 system-prompt 子系统参考（2026-08-16 抓取）；与 [[DeepSeek-Harness 插件开发教程/01-插件开发核心-从apply到system-prompt|§3.6]] 概念图互为表里，并更正 §3.6 的 `register` → `section`。

---

[^1]: 素材来源：官方「system-prompt 子系统参考」（2026-08-16 抓取）。
[^2]: 素材来源：官方 Cordis 教程 03「服务」——`inject` 服务消费模式（沿用自共享资料库 S8）。
[^3]: 素材来源：官方「Tool authoring reference」——工具 schema 自动流入组装（沿用自共享资料库 S3）。
