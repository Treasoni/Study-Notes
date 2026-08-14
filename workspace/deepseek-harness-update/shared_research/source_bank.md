# 共享资料库 · DeepSeek-Harness 插件开发

> 收集时间：2026-08-15
> 适用范围：Ch1–Ch5（插件开发主线）
> 原则：只保留与「写自己的 dsh 插件（自定义工具插件）」相关的最小一手素材；每条含 URL、日期、适用笔记范围、100–200 字摘要。

## 来源清单

### S1 官方「你的第一个插件」（Your first plugin）
- **URL**: https://deepseek-harness.github.io/deepseek-harness/develop/basic/
- **日期**: 2026-08-15 抓取
- **适用**: Ch2 / Ch3
- **摘要**: 插件 = 导出 `apply` 的 TS 模块，框架加载时以 `ctx` 注册能力。在仓库根建 `scratch-plugin/src`，插件路径必须**绝对路径**；`pnpm dsh web --patch ./scratch-plugin/cordis.yml` 启动验证。`ctx` 注册的一切（事件/工具/定时器）卸载时自动清理；手动资源用 `ctx.effect()` 返回 disposer；消费其他服务用 `inject`。三种形态：函数 / 对象 / 类（Service）。

### S2 官方「开发一个 Tool」（Build a tool）★Ch4 直接素材
- **URL**: https://deepseek-harness.github.io/deepseek-harness/develop/basic/tool
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch4
- **摘要**: 完整工具插件示例：`export const inject = ['tools']` + `ctx.tools.register(defineTool({...}))`。`defineTool` 字段：`name` / `description`（模型可见）/ `parameters`（参数 schema，自动校验并推断 TS 类型）/ `output.schema`（canonical 返回值）/ `output.render`（模型可见内容）/ `async execute(args)`。示例 `greet` 工具，重启后 Web UI 让模型调用并返回 `Hello, Ada!`。

### S3 官方「Tool authoring reference」（工具编写参考）
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cookbook/adding-a-tool
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch4 / Ch5
- **摘要**: 工具契约全量参考。`execute` 规则：args 自动校验、返回值必须是 output.schema 声明的单一 canonical JSON、抛错即 `isError`、遵守 `exec.signal` 取消、`exec.agent.inject()` 异步通知。`run_in_background` 经 `ctx.jobs.start` 做长任务。策略与观察：`tools/pre-execute`（allow/deny/ask）、`ctx.tools.guard()`（单调拒绝）、`tools/execute`（包 dispatch 加超时/重试）、`tools/post-execute`、`tools/result`（只读观察）。Code Mode 中工具免费可用为 `await tools.<name>(args)`。UI 卡片用纯 `presentCall`/`presentResult`。

### S4 官方「插件配置」（Plugin configuration）
- **URL**: https://deepseek-harness.github.io/deepseek-harness/develop/basic/config
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch4
- **摘要**: 导出同名 `Config` 接口 + Schemastery schema，`apply(ctx, config)` 收到完整校验后的配置；默认值写在 schema 上。`cordis.yml` 的 entry 带 `config:` 块。原则：可调值都做成配置字段（测试：cordis.yml 能否不改代码改值）；无效配置加载即失败。配置编辑走 HMR 热替换，旧实例注册自动清理。

### S5 官方「打包并安装插件」（Package and install a plugin）★发布机制
- **URL**: https://deepseek-harness.github.io/deepseek-harness/develop/basic/publish
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch5
- **摘要**: **Bundle**（npm 包，声明 `dsh.bundle.patch`，携带配置层）与 **Profile**（`$DSH_HOME/profiles/<name>`，声明 `dsh.profile.bundles` 有序列表）两个概念。`dsh plugin --profile <name> add <package>` 转发 pnpm 并自动追加 bundle。加载顺序：bundle 列表 → profile cordis.patch.yml → home cordis.patch.yml → `--patch`（后层整行替换）。git 安装不跑 build，作者需 `prepare` 脚本 + 用户 `allowBuilds` 放行（视为安装时执行代码的授权）。

### S6 官方 Cordis 教程 01「第一个插件」
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cordis-tutorial/01-first-plugin
- **日期**: 2026-08-15 抓取
- **适用**: Ch3
- **摘要**: Cordis 微内核：插件模块具名导出 `apply`；`cordis.yml` 是插件条目列表（`name` 可为相对路径或 npm 包名），条目并发启动、顺序不保证加载序（由 `inject` 决定）。`name` 导出只是诊断元数据。插件加载失败是响亮失败（进程退出），而路径拼错则走 logger（可能丢失，先查拼写）。

### S7 官方 Cordis 教程 02「生命周期与 effects」
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cordis-tutorial/02-lifecycle-and-effects
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch5
- **摘要**: 插件可因配置编辑/热重载/显式 dispose/依赖消失而卸载。内置注册 API 都是 effect（`ctx.on`、`ctx.plugin`、service 注册、`ctx.tools.register` 自动挂回调用插件）；框架不管理的资源用 `ctx.effect()` 包一层返回 disposer。`ctx.plugin(fn)` 从代码装载子插件，返回 **fiber**（插件实例运行时句柄）。fiber 状态机：PENDING→LOADING→ACTIVE→UNLOADING→DISPOSED（可 FAILED）。

### S8 官方 Cordis 教程 03「服务」
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cordis-tutorial/03-services
- **日期**: 2026-08-15 抓取
- **适用**: Ch3 / Ch4
- **摘要**: **Service** = 具名能力，一个插件提供、其他插件经 `ctx` 消费（`ctx.tools`/`ctx.llm`/`ctx.agents` 都是服务）。提供：`class X extends Service { constructor(ctx){ super(ctx,'name') } }` + `declare module '@deepseek-ai/cordis'` 合并 Context 接口获得类型；类本身也是插件，`ctx.plugin(X)` 挂载。消费：`export const inject = ['greeter']`，依赖就绪前保持 PENDING。依赖消失会级联卸载消费者，恢复后重载。可选依赖跳过 inject 用 `ctx.get('name')` 探测。

### S9 官方 Cordis 教程 05「配置」
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cordis-tutorial/05-config
- **日期**: 2026-08-15 抓取
- **适用**: Ch3
- **摘要**: `cordis.yml` entry 可带 `config` 块，插件导出 `Config` schema 校验，坏配置加载失败且报错精确（`ValidationError`）。`!!js` 标签可在 `config` 与 `disabled` 字段算运行时值（如 `!!js process.env.X ?? 'Hello'`）。`apply` 永远收到完整、已校验配置。

### S10 官方「扩展插件形态 Cookbook」
- **URL**: https://deepseek-harness.github.io/deepseek-harness/cookbook/extension-cookbook
- **日期**: 2026-08-15 抓取
- **适用**: Ch1 / Ch3 / Ch4
- **摘要**: 扩展形态地图。工具插件（`ctx.tools.register`）；**hook 插件**（`ctx.on('tools/pre-execute', ...)` 返回 typed decision，权限门示例）；UI 插件（监听 `session/event` + `agent.followup()`）；协议驱动（对接 `ctx.agents`）。**feature→mechanism 表**：Claude Code 的 hook 系统 → 监听 `agent/session-start`/`agent/pre-step`/`tools/pre-execute` 等（`dsh-hooks-claude-code` 桥把 hook 配置文件映射到这些扩展点）；Skills → section + tool 注册；MCP → 每 server 一个插件 `ctx.tools.register`；子代理 → `ctx.subagents` 注册表。

### S11 官方 system-prompt 子系统（沿用上次更新素材）
- **URL**: https://deepseek-harness.github.io/deepseek-harness/reference/subsystems/system-prompt
- **日期**: 2026-08-14 抓取
- **适用**: Ch3（提示词类插件进阶）
- **摘要**: `ctx.systemPrompt` 注册表；PromptSection（name 唯一 / order 升序 / text 可含 `{{variable}}` / complete 段独占）；order 约定 -100 身份 → 0 人格 → 100–199 工具指导；作用域遮蔽；assemble/change 事件；knownNames 防拼写错；PromptContext 持久化快照。

## Claude Code 桥接要点（写作用）

- dsh 的「hook 插件」≈ Claude Code hooks：dsh 监听 `agent/session-start`、`agent/pre-step`、`agent/request`、`tools/pre-execute`、`tools/post-execute`、`agent/turn-stopping`；官方 `dsh-hooks-claude-code` 把 Claude Code 的 hook 配置文件直接映射到这些扩展点。
- dsh 的「skill」≈ section + tool 注册；「MCP server」≈ 一个插件 `ctx.tools.register`；「subagent」≈ `ctx.subagents` 提供方注册表。
- Claude Code 的 `settings.json`/`CLAUDE.md` = 声明式文件；dsh 的 `cordis.patch.yml`/bundle = 可编程插件组合。

## 未使用 / 待复核

- `packages/core/tools/README.md`（33KB）：tools 服务全量参考，作为 S3 的补充，写作时按需提取。
- `docs/cordis-tutorial/06-composition-and-hmr.md` / `07-into-the-harness.md`：未下载，涉及组合与 HMR 深水区，如需再取。
- 官方文档处于 developer preview，URL/API 可能变动；所有来源已标抓取日期。
