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

[^c4-official]: S2 § a-hook-plugin-permission-gate-example：官方唯一 hook 插件示例，`ctx.on('tools/pre-execute', async (exec, next): Promise<PreToolDecision> => …)`；deny 返回 `{kind:'deny', reason}`，allow 走 `next()`。判断体为示意实现，签名与行为依 S2 文档。
[^c4-wording]: S1 § Key types vs S2 示例：`PreToolDecision` 类型含 `allow` 分支，但官方示例无显式 `{kind:'allow'}` 字面量，`next()` 是 allow 的委派写法。
[^c4-cordis]: S2 § a-hook-plugin-permission-gate-example：原生 hook 是普通 Cordis 插件挂到拦截点，无外部协议；`apply(ctx)` 内注册。
[^c4-pretype]: S1 § Injected services / Key types：`PreToolDecision` 三态；`ask` 由 `ctx.approval` 服务，无挂载时降级为 `deny`。
[^c4-guardian]: S7 § Policy behavior（dsh-guardian）：pre-execute 将危险命令分类 deny/ask/unchanged，「最严格者胜出 deny > ask > allow」。
