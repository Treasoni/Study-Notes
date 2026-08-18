---
title: "实战：加 Config 可调参数"
tags: [deepseek-harness, ai, agent, 插件, 教程, 实战]
created: 2026-08-16
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# 实战：加 Config 可调参数

> [!summary] 本章导读
> 第 06 章让插件装上了工具 `git_log`。可 `git_log` 现在一次只会看最近 5 条提交——用户想改成 10 条，难道要改代码重新加载？这一章解决的就是「不改代码也能调参数」：给插件加可配置项 `maxCommits`，通过 patch 的 `config` 块传值、在 apply 里读取。这正是 dsh 插件与一段硬编码脚本的分水岭：任何「两个部署可能想要不同值」的东西，都应该是配置字段，而不是写死的常量[^1]。

## 1. 为什么做成配置项

「不硬编码可调值」：不同项目想看 5 条还是 50 条提交，不该改代码。判断标准一句话：**两个部署可能设不同值 → 做成配置字段**[^1]。这样换项目只改配置、不改源码。反例是 `const LIMIT = 5` 这种硬编码常量。

> [!tip] 大白话
> Config schema = **岗位说明书 / 入职登记表**：提前声明「这个插件要什么参数、默认多少」。`config:` 传值 = **入职时在表上填你想要的默认值**：同一张登记表，不同项目填 5 还是 50，随你。

## 2. Config 两段式：`export interface Config` + `export const Config`

插件的配置项由「两个同名导出」共同声明：`export interface Config` 描述类型，`export const Config: Schema<Config> = Schema.object({...})` 描述运行时校验与默认值[^1]。类型只在编译期存在、会被擦除；schema 在插件加载时真实运行。两者同名，dsh 的 patch loader 拿到运行时校验器，你写代码时拿到类型提示[^2]。

```ts
// src/index.ts（新增部分；name 与 apply 第 05/06 章已有）
import type { Context } from '@deepseek-ai/cordis'
import Schema from '@deepseek-ai/schemastery'   // 新增依赖

export interface Config {
  maxCommits: number
}

export const Config: Schema<Config> = Schema.object({
  maxCommits: Schema.number().default(5),
})
```

注意两点。第一，`Schema.object({...})` 的返回值要标注成 `Schema<Config>`，让每个字段和 interface 互相核对，写错字段名或类型在编译期就能暴露。第二，**不要导出普通对象作 Config**：`export const Config = { maxCommits: 5 }` 只是个 plain object，没有实现 Standard Schema 接口，Cordis 无法用它校验，插件不会被正确加载。第二段必须是 `Schema.object({...})` 这类校验器[^1][^2]。

> [!tip] 大白话
> 把 schema 想成一张「配置体检表」。插件加载时先体检：字段名、类型对不对？缺的项用默认值补上？全部合格才放行开工。不合格直接拒之门外，绝不让你带病半启动——§7 会看到被拒时报错长什么样。

> [!note] 这在 Claude Code 里相当于
> 插件入口里声明 settings schema（用 zod 校验）：类型与运行时校验合在一个定义里，读配置的代码永远拿到的都是「已验证」的值。

## 3. 默认值写 schema：`Schema.number().default(5)`

关键约定：**默认值写在 schema 上，不写在业务逻辑里**[^1]。`Schema.number().default(5)` 表示「这是一个 number，调用方没传时自动填 5」。于是 patch 里漏传 `maxCommits`，插件照样拿到 5；传了就优先用传的值。官方给的判断标准很直接：`cordis.yml`（或 patch）能不能不改代码就改变这个值——能，它才配叫配置字段；不能，就该把它做成配置项[^1]。

> [!note] 这在 Claude Code 里相当于
> `Schema.number().default(5)` ≈ `z.number().default(5)`：默认值由校验器统一管理，读配置时永远有值，业务代码不需要再写 `?? 5` 这种兜底。

## 4. 校准注记：必填用 `.required()`，不用 `.required(true)` / `.optional()`

schema 里的字段默认都是可选的。必填的字段用 `.required()` 显式标记；可选的字段在 interface 层用 TS 的 `?` 表示，**不要**在 schema 上写 `.optional()`。官方从不用 `.required(true)` 这种带参数的写法[^1]。

```ts
export const Config: Schema<Config> = Schema.object({
  apiKey: Schema.string().required(),     // 必填：缺了直接校验失败
  maxCommits: Schema.number().default(5), // 可选：不写 .required()，且有默认值
})
```

> [!warning] 校准注记（合并时统一口径）
> 原《插件实战》§4 的口径是「无 `.optional()`，必填用 `.required(true)`」。官方文档明确：必填一律 `.required()`，从不用 `.required(true)` 或 `.optional()`。本教程以官方为准，对照旧笔记时请留意这一处差异。

| 写法 | 含义 | 本教程 |
| --- | --- | --- |
| `.required()` | 必填 | 采用（官方口径） |
| `.required(true)` | 必填 | 不用（旧笔记写法） |
| `.optional()` | 可选 | 不用（官方从不用） |
| TS `?` | 可选 | 采用（interface 层） |

## 5. 在 patch 的 `config` 块传值

配置值不写在代码里，而是由 patch 的 `config` 块传进来。回到第 05 章的 `dev-cordis.patch.yml`，给 `git-log` 条目补上 `config`，键名与 interface 字段一一对应[^2]：

```yaml
# dev-cordis.patch.yml（开发期，用 --patch 加载）
- insert:
    - id: git-log
      name: '/Users/me/git-log-plugin/src/index.ts'   # 绝对路径（第 05 章）
      config:
        maxCommits: 10   # 覆盖 schema 默认的 5
```

改造路线的读者注意：`dev-cordis.yml` 与 `cordis.patch.yml` **各加一个 `config:` 块**，并统一把 `id` 改成 `git-log`：

```yaml
# 打包层 patch：插件行按包名引用（Node resolution 从 profile node_modules 找已安装代码）
- insert:
    - id: git-log
      name: dsh-git-log-plugin
      config:
        maxCommits: 5
```

两份 patch 长得像、角色不同[^3]：**dev 层 `name` 用绝对路径指向源码**，改完立刻生效；**bundle 层用包名 `dsh-git-log-plugin` 指向已安装产物**，发布后别人装的是这份。`id: git-log` 两边一致，它只是给插件实例起的诊断名（模型可见的工具名是第 06 章 `defineTool` 里的 `git_log`，两者可以不同）。这一步先只改 dev patch；09 章把 bundle patch 定型时，把同一份 `config` 块原样复制过去——两份 patch 传值的位置完全一致，装成包后用户也在同一个位置配置。

> [!note] 这在 Claude Code 里相当于
> patch 的 `config` 块 ≈ 在 settings.json 里给插件写配置；apply 第二参数收到的 config ≈ 插件初始化时框架注入的「默认值 + 用户覆盖」合并结果。

## 6. apply 里读取完整校验后的 config

插件加载时 schema 先跑一遍；校验通过后，Cordis 把「填好默认值、校验过的完整 config」作为 apply 的第二参数传进来[^2]：

```ts
export function apply(ctx: Context, config: Config) {
  // config 已校验 + 已填默认值，直接读
  const limit = config.maxCommits
  ctx.tools.register(gitLogTool(config))   // 整个 config 传给第 06 章的工具工厂
  console.log(`[git-log-plugin] plugin loaded! maxCommits=${limit}`)
}
```

顺带把第 06 章工具工厂升级为接收 config——`execute` 里那句写死的 `-n 5` 换成 `-n config.maxCommits`：

```ts
export function gitLogTool(config: Config) {
  // ...
  async execute(args) {
    const { stdout } = await execFileAsync('git', ['log', '--oneline', '-n', String(config.maxCommits)], {
      cwd: args.path,
    })
    // ...
  }
}
```

核心认知：**apply 总收到完整校验后的 config**[^2]。patch 漏传 `maxCommits`，它自动被 `default(5)` 填成 5；patch 传 `10`，到手就是 10。所以 apply 里不需要、也不应该再手写一遍 config 校验——那是 schema 的活，重复校验既啰嗦，又容易和 schema 口径不一致。官方文档里 config 始终以 apply 第二参数的形式出现；若在旧资料里看到 `ctx.config` 的写法，那是早期框架的习惯，本教程按官方签名来。

> [!note] 这在 Claude Code 里相当于
> `apply(ctx, config)` 的 config ≈ Claude Code 插件初始化时框架注入的「settings 默认值 + 用户覆盖」合并结果；读配置的代码永远拿到的是已验证、已填默认值的值。

## 7. 坏配置行为：ValidationError / fiber FAILED / 永不半启动

把 config 传错，插件不会带病运行——schema 在插件加载时就执行，坏配置直接让加载失败[^1][^2]：

```yaml
# dev-cordis.patch.yml —— 故意传错类型
- insert:
    - id: git-log
      name: '/Users/me/git-log-plugin/src/index.ts'
      config:
        maxCommits: 'ten'   # 错：number 字段传了字符串
```

加载时 dsh 打印：

```text
ValidationError: invalid config:
  - $.maxCommits expected number but got string (at maxCommits)
```

随后这个插件的 fiber 进入 FAILED，加载流程报错退出，插件**永不半启动**[^2]。好处是配置错误在加载那一刻就被精确抓出，而不是运行到一半才诡异崩掉，或带着错误配置静默跑很久。这也是配置体系里「fail loud」原则的落地。

> [!tip] 大白话
> 还是那张「配置体检表」。你填「身高：十厘米」这种明显不合格的项，体检当场打回、贴出不合格单（ValidationError），连门都不让进（fiber FAILED）。绝不会出现「先进来上班、干着干着才发现不合格」的半启动状态。

## 8. 易错点三连（合并去重后的完整清单）

1. **Schemastery 没有 `.optional()`**：字段默认就是可选的，要必填得显式 `.required()`（官方口径，不是 `.required(true)`）——见 §4。
2. **补丁树整行替换、不做深合并**：想覆盖某一行，必须把这一行需要的 key 全写上，别指望框架帮你补齐——这是配置体系补丁树的语义，08 章验证、09 章打包都会再碰到。
3. **坏配置加载即响亮失败**：报 ValidationError / fiber FAILED，不会静默兜底[^2]——写错立刻发现，是好事。

## 本章小结

- Config 是「两段式」：`export interface Config` 管类型，`export const Config: Schema<Config> = Schema.object({...})` 管运行时校验与默认值，两者同名；不能导出普通对象作 Config。
- 默认值写在 schema 上：`Schema.number().default(5)`，patch 漏传时自动补默认值，业务逻辑不写兜底。
- 必填用 `.required()`；官方从不用 `.required(true)` 或 `.optional()`，可选用 TS `?`（原《插件实战》§4 旧口径不同，以官方为准）。
- 传值走 patch 的 `config` 块；dev patch 与 bundle patch 传值位置一致。
- apply 的第二参数就是完整校验后的 config，直接读、别二次校验；坏配置 → ValidationError / fiber FAILED，永不半启动。

配置能声明、能传、能读了，可怎么确认它真的生效、又落在哪一层？下一章用 `--dump-config` 把分层配置一张张打出来验一遍。

---

## 注释

[^1]: 素材来源：官方 `docs/user/develop/basic/config.md`（Plugin configuration）——Config 两段式、`.default()` 默认值、`.required()` 必填口径、禁止导出普通对象作 Config。
[^2]: 素材来源：官方 `docs/cordis-tutorial/05-config.md`（Cordis 教程第 5 章）——`config` 块、ValidationError 输出、fiber FAILED、apply 总收到完整校验后的 config。
[^3]: 「两份 patch 传值 / 易错点」来自原《DeepSeek-Harness 插件实战》分册第 4 节（已并入本教程 04-10 章）；其 `.required(true)` 旧口径已按官方 `.required()` 修正，见 §4 校准注记。
