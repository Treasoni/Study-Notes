---
title: "插件开发核心——从 apply(ctx) 到 system-prompt"
tags: [deepseek-harness, ai, agent, 插件, 教程, 开发]
created: 2026-08-13
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# 插件开发核心——从 apply(ctx) 到 system-prompt

> [!summary] 本章导读
> 这是全书核心。用你熟悉的 Claude Code 作参照：在 Claude Code 里写「扩展」靠改配置文件 + 少量钩子；在 dsh 里写插件 = 写 TypeScript 模块 + 用 patch 装进插件树。本章讲插件**怎么写**：形态 → 生命周期 → 依赖 → 写工具 → 策略 → 提示词。插件怎么**注册 / 装配 / 发布**（补丁树、Profile、Config schema、bundle）见配套专册 [[02-配置体系-补丁树Profile与bundle|配置体系]]。

## 3.1 插件是什么：apply(ctx) + name

插件是导出 `apply` 函数的 TypeScript 模块。框架加载时调用 `apply` 并传入 `ctx`（上下文对象），通过 `ctx` 注册能力[^1]：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'hello-plugin'   // 仅诊断用，可省
export function apply(ctx: Context) {
  // Register capabilities here.
}
```

> **代码放哪**：这个文件就是 `src/index.ts`——插件入口骨架（目录结构参照同目录 `example-plugin/`）。通用原则：`src/index.ts` 是**注册中心**（所有 `apply(ctx)` 里的动作都在这），工具/服务本体各自成文件放 `src/tools/`、`src/services/`。

`name` 只是诊断元数据；真正的逻辑都在 `apply(ctx)` 里。**没有框架样板代码**——插件只描述自己贡献什么，`cordis.yml` 负责组合应用[^2]（怎么装进插件树见 [[02-配置体系-补丁树Profile与bundle|配置体系]]）。

> [!tip] 大白话
> 插件像一个「应聘者」，`apply(ctx)` 是入职第一天：公司（框架）把工牌（ctx）发给你，你在工牌上挂上你的能力（工具、事件、服务）。离职时（插件卸载），挂上去的自动摘下来。

### 三种形态

| 形态         | 写法                                                                  | 适用        |
| ---------- | ------------------------------------------------------------------- | --------- |
| 函数         | `export function apply(ctx) {}`                                     | 多数情况足够    |
| 对象         | `export default { name, inject, apply(ctx) {} }`                    | 需要集中声明元数据 |
| 类（Service） | `class X extends Service { constructor(ctx){ super(ctx,'name') } }` | 向其他插件提供服务 |

函数形式直到你需要对外提供 service 都够用；类形式见 3.3[^2]。

### 市场里的 5 种分发形态（分发形态 ≠ 代码形态）

上面三种是**代码怎么写**；插件市场里看到的花样是**包怎么分发、loader 怎么对待它**——两个维度，别混。市场里的插件按分发归为 5 种[^6]：

| 分发形态                  | 本质                        | 接入方式                                                           | 例子                                    |
| --------------------- | ------------------------- | -------------------------------------------------------------- | ------------------------------------- |
| ① 纯 Cordis 插件         | TS 模块导出 `apply(ctx)`      | `cordis.yml` insert 一行直接挂载                                     | `dsh-plugin-deepeye`（视觉工具）            |
| ② Bundle              | npm 包带 `dsh.bundle.patch` | `dsh plugin add <pkg>` 进 bundle 层                              | 官方 `dsh-tool-bash` / `dsh-web-search` |
| ③ MCP server          | 语言无关独立进程                  | `dsh.mcpServers` 声明或 mcp-client 包装，工具变 `mcp__<server>__<tool>` | `@modelcontextprotocol/server-*`      |
| ④ Skill               | `SKILL.md` 技能包            | `dsh.skills` 声明或适配器扫描 `.claude/skills/`                        | 你的 Claude Code skills                 |
| ⑤ Koishi/Cordis v3 插件 | 4000+ 机器人生态插件             | **不能直接用**，需按 Cordis v4 + `@deepseek-ai/cordis` 移植              | Koishi 市场插件                           |

loader 看 `package.json` 的 `dsh` 字段决定怎么对待一个包：

```
dsh.bundle      → 组合层补丁包（插入插件树）
dsh.mcpServers  → MCP server 集合（包装注册工具）
dsh.skills      → 技能包（SKILL.md 发现）
dsh.client      → 带浏览器 UI 的插件
```

> **代码放哪**：这些 `dsh.*` 字段写在 `package.json` 的 `dsh` 下（发布清单），与 `src/` 里的 TS 代码无关。

> [!note] 两个易混点
> - ①②③④ 大多是**不加修改被接纳**，只有⑤需要移植——所以市场里「不是 DeepSeek 格式」很正常；
> - 2026-08 起旧的 `dsh.plugin.json` / `dsh registry` CLI 已移除，只认 `dsh` 字段这套。

## 3.2 生命周期与 effects：fiber 状态机

每个加载的插件实例持有一个 **fiber**（运行时句柄），状态机[^2]：

```
PENDING → LOADING → ACTIVE → UNLOADING → DISPOSED
                 ↘ FAILED
```

- **PENDING** — 声明了但必需服务（3.3）尚未就绪；
- **FAILED** — `apply` 或配置校验抛错；
- **UNLOADING / DISPOSED** — disposer 运行 / 全部拆除。

插件会因配置编辑、热重载、显式 dispose、依赖消失而卸载。**通过 `ctx` 注册的一切都是 effect**：事件监听、工具、定时器、子插件、service 注册——卸载时自动清理，无需手动 removeListener / clearInterval[^2]。

框架不管理的资源（网络连接、文件 watcher）用 `ctx.effect()` 包一层：

```ts
export function apply(ctx: Context) {
  ctx.effect(() => {
    const timer = setInterval(() => console.log('heartbeat'), 5000)
    return () => clearInterval(timer)   // 卸载时运行
  })
}
```

> **代码放哪**：写在 `src/index.ts` 的 `apply(ctx)` 里（与工具注册同级）。

> [!tip] 大白话
> 「效果（effect）」像门禁卡的自动失效：离职那天门禁卡自动作废，你不用自己去前台注销。凡是走 `ctx` 挂的能力都自动失效；自己额外申请的资源（网络连接）用 `ctx.effect()` 声明「我离职时要做这些清理」。

## 3.3 服务与依赖：inject 与 Service

**Service** 是具名能力，一个插件提供、其他插件经 `ctx` 消费——`ctx.tools` / `ctx.llm` / `ctx.agents` 都是服务[^2]。

### 消费依赖：inject

```ts
export const name = 'my-tool-plugin'
export const inject = ['tools']          // 依赖就绪前不加载

export function apply(ctx: Context) {
  ctx.tools.register(/* ... */)          // ctx.tools 一定可用
}
```

> **代码放哪**：`name` / `inject` 写在 `src/index.ts` 顶部；`apply(ctx)` 里的 `ctx.tools.register(...)` 也在 `src/index.ts`。

`inject` 不是一次性启动检查：如果依赖运行中消失，依赖它的插件会一起被卸载，等服务恢复再重载。**文件顺序不决定加载序，依赖才决定**。

可选依赖：跳过 inject，用 `ctx.get('name')` 探测（拿不到返回 undefined，插件照常运行）。

> [!tip] 大白话
> 依赖像「入职时的部门声明」：`inject: ['tools']` 就是填表说"我需要工具部才能开工"——工具部没就绪我就不入职（PENDING），工具部中途解散我也跟着被"裁员"，等它重建我再回来。**可选依赖**则是"有就蹭，没有也能自己干"：用 `ctx.get('name')` 试一下，拿不到就算了。而 Service 类 = 当部门主管，把能力注册成 `ctx.xxx`，别人按名字来领。

### 提供服务：类形态

```ts
import { Service, type Context } from '@deepseek-ai/cordis'

declare module '@deepseek-ai/cordis' {
  interface Context { greeter: GreeterService }   // 类型合并，让 ctx.greeter 有类型
}

export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter')                          // 注册为 ctx.greeter
  }
  greet(who: string) { return `Hello, ${who}!` }
}

export function apply(ctx: Context) {
  ctx.plugin(GreeterService)                       // 类本身也是插件
}
```

> **代码放哪**：类（Service）本体单独放 `src/services/greeter.ts`；`apply(ctx)` 里的 `ctx.plugin(GreeterService)` 放 `src/index.ts`。

## 3.4 开发一个 Tool：defineTool DSL

工具是模型能调用的能力。用 `defineTool` 定义，经 `ctx.tools.register` 注册[^3]：

```ts
import { defineTool } from '@deepseek-ai/dsh-tools'

export const name = 'greet-tool'
export const inject = ['tools']

export function apply(ctx: Context) {
  ctx.tools.register(defineTool({
    name: 'greet',
    description: 'Greet someone by name.',        // 模型看到的描述
    parameters: {
      name: { type: 'string', required: true, description: 'The name to greet' },
    },
    output: {
      schema: { type: 'string' },                  // canonical 返回值
      render: (_args, value) => [{ type: 'text', text: value }],  // 模型可见内容
    },
    async execute(args) {
      return `Hello, ${args.name}!`               // args 已按 parameters 校验并推断类型
    },
  }))
}
```

> **代码放哪**：`defineTool({...})` 本体放 `src/tools/greet.ts`；`name` / `inject` / `ctx.tools.register(...)` 放 `src/index.ts`。

> [!tip] 大白话
> 工具 = 教给模型的一个**新招式**。`defineTool` 是一张「技能登记表」：`name` 是招名，`description` 说清何时用（模型读这段决定要不要调你），`parameters` 是要什么料，`execute` 是真干活。系统会**自动检查模型填的参数**，填错就不进 `execute`；干砸了（基础设施故障）就 `throw`，业务上没成功不算错，作为正常结果放返回值，让模型自己判断。

关键契约（完整参考见 [[DeepSeek-Harness 教程/DeepSeek-Harness 常见坑与速查|第 5 章 5.3]]）：
- **args 自动校验**：`defineTool` 在 `execute` 前校验模型生成的参数；
- **返回值**：`execute` 只返回 `output.schema` 声明的单一 canonical JSON 值，`output.render` 负责转成模型可见的文本——别在返回值里塞给人看的 prose；
- **抛错 = isError**：基础设施失败就 throw，业务成功态放进 canonical 值；
- **`exec.signal`**：需要时可取消进行中的工作；
- **注册即 effect**：插件卸载自动注销工具，schema 自动流入系统提示词组装[^4]。

## 3.5 工具策略与观察：hook 扩展点

工具不是黑盒——dsh 提供一组**扩展点**，让插件在工具执行前后插入策略[^4]：

| 扩展点 | 用途 |
|---|---|
| `tools/pre-execute` | allow / deny / ask 决策（权限门） |
| `ctx.tools.guard()` | 单调最终拒绝，后面的监听者无法撤销 |
| `tools/execute` | 包 dispatch 加超时、重试、指标 |
| `tools/post-execute` | 替换展示内容或返回值、附加上下文 |
| `tools/result` | 只读观察不可变的最终结果 |

> [!tip] 大白话
> 工具不是黑盒，门口能站保安：`tools/pre-execute` 是**门卫**——执行前先问"放行 / 拒绝 / 请示用户"；`ctx.tools.guard()` 是**一票否决**（保安说不行，后面的人改不了）；`tools/post-execute` 是**改汇报**（干完活换一份给模型看的内容）；`tools/result` 是**围观记录**（只看不改）。

示例（权限门 hook 插件）[^4]：

```ts
ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => {
  if (!(await isAllowed(exec))) {
    return { kind: 'deny', reason: 'Denied by policy.' }
  }
  return next()
})
```

> **代码放哪**：写在 `src/index.ts` 的 `apply(ctx)` 里（与工具注册同级）。

> [!note] 与 Claude Code 对照
> 这就是「hook 插件」：Claude Code 的 `PreToolUse` hook ≈ `tools/pre-execute` 监听；官方 `dsh-hooks-claude-code` 桥能把 Claude Code 的 hook 配置文件直接映射到这些扩展点[^4]。

## 3.6 system-prompt 子系统：提示词怎么组装

写提示词类插件（加人格、加指令）直接相关的参考。`system-prompt` 包负责**在每次模型调用前组装最终系统提示词**，注册表服务 `ctx.systemPrompt`[^5]。

### PromptSection

```ts
interface PromptSection {
  readonly name: string        // 必须唯一，重复注册抛错
  readonly order: number       // 升序拼接
  readonly text: string | ((context) => string)  // 可含 {{variable}} 占位符
  readonly complete?: boolean  // true = 该段即完整系统提示词
}
```

> **代码放哪**：这个接口是 `@deepseek-ai/system-prompt` 包提供的类型定义，**不用自己写**；你的注册动作 `ctx.systemPrompt.section({...})` 写在 `src/index.ts` 的 `apply(ctx)` 里。

> [!warning] 方法名更正
> 早期版本写作 `ctx.systemPrompt.register({...})`，官方实际方法是 **`ctx.systemPrompt.section({...})`**（2026-08-16 核对）。完整可抄示例见 [[DeepSeek-Harness 插件开发教程/13-实战-写system-prompt插件|第 13 章]]。

**order 约定**：`-100` harness 身份 → `0` 部署人格（persona）→ 其他负数在人格前 → `100–199` 工具指导。

**complete 语义**：`complete: true` 的段表示「贡献就是完整系统提示词」。组装仍会跑协作瀑布，随后把该段恢复为唯一提示词段；多个生效 complete 段 → 组装失败。

> [!tip] 大白话
> 每次调模型前，系统要**拼一份发言稿**：各插件的提示词段按 `order` 编号从小到大排（`-100` 身份 → `0` 人格 → `100–199` 工具指导）。`complete: true` = 有人说"别拼了，我这篇就是全部发言"（多个这样的人 → 会开不下去）。「遮蔽」= 部门规则盖过公司规则：作用域级段落/变量盖掉全局同名项。

### 作用域与遮蔽

- 作用域级段落/变量/动态上下文**遮蔽**（shadow）全局同名项；
- 工具提供方例外：全局与匹配作用域**共同贡献**；
- 变量名匹配 `[a-z][a-z0-9_]*`，`{{variable}}` 在渲染期由 `renderPrompt` 插值。

### 事件与防错

- `system-prompt/assemble`（waterfall）：返回值权威，监听者可修改 assembly；
- `system-prompt/change`（emit）：任何提示词提供方变化时发出；
- `knownNames`：区分「配置名拼写错误」与「已知工具被有意隐藏」；
- `PromptContext`：缓存安全的动态上下文，物化为 durable user-role snapshot，避免每回合重复写入[^5]。

---

## 本章小结

> [!summary]
> - 插件 = 导出 `apply(ctx)` 的 TS 模块；三种形态：函数 / 对象 / 类（Service）；
> - 生命周期：fiber 状态机；`ctx` 注册的一切都是 effect，自动清理；手动资源用 `ctx.effect()`；
> - 依赖：`inject` 声明硬依赖（未就绪保持 PENDING），`ctx.get()` 探测可选依赖；Service 类对外提供服务；
> - 工具：`ctx.tools.register(defineTool({...}))`，args 自动校验、canonical 返回值、注册即 effect；策略用 `tools/pre-execute` 等 hook 扩展点；
> - 提示词类插件看 `ctx.systemPrompt`：PromptSection 按 order 组装，`complete` 段可独占；
> - 注册 / 装配 / 发布（补丁树、Profile、Config schema、bundle）见 [[02-配置体系-补丁树Profile与bundle|配置体系专册]]。

下一章动手写一个完整插件：[[DeepSeek-Harness 教程/DeepSeek-Harness 与ClaudeCode对照迁移|实战：自定义工具插件]]。

---

## 更新记录

- 2026-08-16：3.6 方法名更正 `register` → `section`（官方 system-prompt 参考核对）；新增配套实战章节 [[DeepSeek-Harness 插件开发教程/13-实战-写system-prompt插件|第 13 章]]。
- 2026-08-15：各代码块补充「代码放哪」文件归属提示（`src/index.ts` 注册中心 / `src/tools/` 工具 / `package.json` 发布字段）。
- 2026-08-15：3.3–3.6 补充 `[!tip] 大白话` 通俗解释与类比，降低阅读门槛。
- 2026-08-15：全套重构为「写自己的 dsh 插件」主线。
- 2026-08-15：拆分「配置体系」：原 3.2（补丁树）/ 3.3（两级配置）/ 3.6（Config schema）/ 3.9（bundle 发布）移入新专册 [[02-配置体系-补丁树Profile与bundle|配置体系]]；本节重排为 3.1–3.6（形态 / 生命周期 / 依赖 / 工具 / 策略 / 提示词）。
- 2026-08-15：3.1 新增「市场里的 5 种分发形态」——区分代码形态与分发形态，补 `dsh` 字段路由机制（bundle / mcpServers / skills / client）。
- 2026-08-16：迁移入 [[DeepSeek-Harness 插件开发教程/README|插件开发教程]] 分册第 01 章，更新内部双链。

---

[^1]: 素材来源：DeepSeek Harness 官方文档「第一个插件 / 插件配置」（2026-08-15 收集）。
[^2]: 素材来源：官方 Cordis 教程 01–03/05（2026-08-15 收集）。
[^3]: 素材来源：官方「开发一个 Tool」（2026-08-15 收集）。
[^4]: 素材来源：官方「Tool authoring reference」与「扩展插件形态 Cookbook」（2026-08-15 收集）。
[^5]: 素材来源：官方「system-prompt 子系统参考」（2026-08-14 收集）。
[^6]: 素材来源：官方「架构」文档 + `plugin-registry/make-dsh-plugin`（2026-08-15 收集）。
