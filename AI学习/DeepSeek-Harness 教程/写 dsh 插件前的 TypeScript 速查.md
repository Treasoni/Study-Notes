---
title: "写 dsh 插件前的 TypeScript 速查"
tags: [deepseek-harness, typescript, 速查, 前置, 教程]
created: 2026-08-15
updated: 2026-08-15
status: published
source_project: deepseek-harness
---

# 写 dsh 插件前的 TypeScript 速查

> [!summary] 本篇导读
> 面向**学过 Python + C、没学过 TypeScript**、想写 [[DeepSeek-Harness 插件开发核心|dsh 插件]] 的读者。一句话结论：你的已有基础覆盖写插件所需 TS 的 **80%**，真正要补的是三件事——**ESM 模块语法、结构化类型（interface + 泛型）、「编译期类型 ≠ 运行时校验」的心智模型**。
> 本篇按优先级分 P0（必学）/ P1（常碰）/ P2（用到再学），每项都从本系列笔记抽真实代码做例子。配套正文见 [[DeepSeek-Harness 插件开发核心]] 与 [[DeepSeek-Harness 从零写插件]]。

## 你已有的基础：C/Python → TS 迁移对照表

| 你已经会的                  | TS 里对应                    | 例子（来自本系列）                                        |
| ---------------------- | ------------------------- | ------------------------------------------------ |
| Python dict            | 对象字面量 `{}`                | `{ name: 'greet', description: '...' }`          |
| Python list            | 数组 `[]`                   | `inject: ['tools']`                              |
| Python f-string        | 模板字符串 `` `...${name}` ``  | `` `[${name}] plugin loaded!` ``                 |
| Python async/await     | async/await + Promise     | `async execute(args) { ... }`                    |
| Python class / super() | class / extends / super() | `class GreeterService extends Service`           |
| C struct               | interface                 | `export interface Config { maxCommits: number }` |
| C 的静态类型直觉              | TS 类型标注                   | `function apply(ctx: Context)`                   |

## P0 · 必须学（每个插件文件都出现）

### 1. ESM 模块语法 — `import` / `export` / `import type`

你所有插件的第一行几乎都是：

```ts
import type { Context } from '@deepseek-ai/cordis'
```

- `import type`：**纯类型导入**，编译后被擦掉，不产生运行时代码；
- `export const name` / `export function apply` / `export interface Config`：插件靠命名导出暴露契约；
- 对照：Python 的 `from x import y` / `import x` 最接近；但 ESM 是静态解析、必须显式导出。

> [!note] 在 Claude Code 里相当于
> 插件入口文件的初始化回调 + manifest 声明。区别是 cordis 用「导出 `apply` + `name`」作为唯一约定。

### 2. interface 与类型标注 — 对应 C 的 struct

```ts
export interface Config {
  maxCommits: number
}
```

- 对应 C 的 `struct`，但核心是**结构化类型**（duck typing）：结构对上就兼容，无需显式继承；
- `interface` 只存在于编译期，运行时不存在；
- dsh 里最典型的用法就是 **Config 两段式**（见 P1 泛型）。

### 3. 对象字面量 + 解构 + 展开

`defineTool({...})` 整坨就是一个对象字面量：

```ts
ctx.tools.register(defineTool({
  name: 'git_log',
  description: '查看 git 提交历史',
  parameters: { type: 'object', properties: { path: { type: 'string', required: true } } },
  output: { schema: { type: 'string' }, render: (_args, value) => [{ type: 'text', text: value }] },
  async execute(args) { /* ... */ },
}))
```

数组解构（来自 [[DeepSeek-Harness 从零写插件]] 的 `git_log` 工具）：

```ts
const [hash, ...rest] = line.split(' ')
```

> Python dict → JS object 的心智转换：key 不用引号、`?` 表示可选字段、对象是「引用」而非「拷贝」。

### 4. 函数与 async/await

```ts
async execute(args) {
  const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', '5'], {
    cwd: args.path,
  })
  return { commits }  // 返回 canonical 值，不返回展示文本
}
```

- 语法和 Python asyncio 几乎一样；
- **核心差异**：JS 是**单线程事件循环**，`await` 只提供并发、不提供真正的并行；长计算任务别指望多核加速（要并行得用 worker）。

## P1 · 经常碰（值得专门学）

### 5. 泛型 Generics — 从 C/Python 迁移时唯一真正的新概念

dsh 的 API 骨架全是泛型：`Schema<Config>`、`defineTool`。

```ts
export interface Config {
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})
```

- 类比：Python `list[int]` / `typing.Generic`；C 无直接对应（最接近 `#define` / `void*`，但不安全）；
- 这就是 **Config 两段式**：`interface Config` 管编译期类型，`const Config: Schema<Config>` 管运行时校验。字段名写错，编译期就报错。

> [!warning] 不要导出普通对象作 Config
> `export const Config = { maxCommits: 5 }` 只是 plain object，没有实现 Standard Schema 接口，Cordis 无法用它校验，插件不会被正确加载。第二段必须是 `Schema.object({...})` 这类校验器。

### 6. 类与继承 — Service 形态

```ts
export class GreeterService extends Service {
  constructor(ctx: Context) {
    super(ctx, 'greeter')
  }
  greet(who: string) { return `Hello, ${who}!` }
}
```

- 你有 Python 类基础，补三样：`constructor` 构造器、访问修饰符、字段类型标注；
- 用在「向其他插件提供服务」时（详见 [[DeepSeek-Harness 插件开发核心|插件开发核心 3.3 服务与依赖]]）。

### 7. 可选链 / 空值合并 / undefined vs null / strict

插件 tsconfig 开 `strict: true`，意味着必须处理「可能为 undefined」：

```ts
const greeter = ctx.get('greeter')    // 拿不到返回 undefined
greeter?.greet('world')               // 可选链：undefined 时安全跳过
const limit = config.maxCommits ?? 5  // 空值合并：null/undefined 时用默认值
```

- `undefined` ≈ Python `None`；`null` 在 TS 里一般少用；
- `strict` 模式 ≈ C 编译器 `-Wall -Werror` 的等价物——宁可编译期拦下，不放到运行时炸。

### 8. 错误处理 — throw + 类型断言

```ts
throw new Error(`git log 执行失败: ${(err as Error).message}`)
```

- 基础设施失败用 `throw`（= isError，框架捕获、不泄漏给模型）；
- 业务成功态放 canonical 返回值（空结果也是成功）；
- `(err as Error)` 是类型断言；安全优先用 `unknown` 再收窄，别用 `any`。

## P2 · 用到再学（不阻塞起步）

| 主题 | 什么时候遇到 | 例子 |
|---|---|---|
| `declare module` 模块增强 | 做「对外提供服务」时 | `declare module '@deepseek-ai/cordis' { interface Context { greeter: ... } }` |
| Node.js 基础（child_process / fs） | 写 `git_log` 这类系统工具时 | `execFileAsync('git', ...)` |
| tsconfig / 构建链 | 工程化打包时 | `strict` / `outDir` / `declaration` 字段含义（见 [[DeepSeek-Harness 从零写插件|从零写插件 第 6 章]]） |

## 明确不用学（跳过）

- **前端全家桶**：DOM、JSX/React、CSS —— dsh 插件是纯 Node 端，无关；
- **类型体操**：conditional types、mapped types、infer、装饰器 —— 写插件用不上；
- **后端框架**：express、nestjs 等 —— 不是 dsh 生态。

## 学习路径建议

1. 过一遍 TS 官方手册前几章：**Modules → Basic Types → Interfaces → Functions → Classes → Generics**（1~2 天）；
2. 打开 [[DeepSeek-Harness 从零写插件]]，**从第 2 章最小 2 文件开始**边写边查——会同时遇到 P0+P1 里 80% 的语法；
3. 卡住时对照 [[DeepSeek-Harness 插件开发核心]] 的 defineTool 五件套和 Service 例子；
4. 编译报错先看是不是 `strict` 的 undefined/null 问题——新手最高频的坑。

## 核心心智模型：编译期类型 ≠ 运行时校验

> [!warning] C 程序员最容易踩的坑
> TS 的类型是**编译期存在、运行时被擦除**的——不产生任何代码、没有内存布局。你在 dsh 里看到的「运行时校验」全部来自 **schemastery**（`Schema.object`），那是另一层真实存在的 JS 对象。
> 一句话：**类型给开发期兜底，schema 给运行时兜底**。抓住这一点，就抓住了 dsh 插件的精髓。

---

## 更新记录

- 2026-08-15 创建（单页速查，面向 Python + C 背景读者）
