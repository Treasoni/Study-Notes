---
title: "DeepSeek-Harness 配置体系"
tags: [deepseek-harness, ai, agent, 教程, 配置]
created: 2026-08-13
updated: 2026-08-14
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 配置体系：从 settings.json 到 YAML 补丁树

> [!summary] 本章导读
> Claude Code 用 `settings.json` / `CLAUDE.md` 这种「声明式文件」管理配置；dsh 完全不同——它是「多层 YAML 补丁树 + Profile + Agent Preset」。这是全书的配置核心，也是从 [[Claude Code MOC|Claude Code]] 迁移时最需要扭转的心智模型。

## 3.1 配置机制：多层 YAML 补丁树

dsh 的配置不是 `config.toml`，也不是单文件，而是在空根上按顺序叠加的 **YAML 补丁树**[^1]：

1. **bundle 补丁**：profile manifest 中 `dsh.profile.bundles` 列表命名的每个 bundle 补丁；
2. **profile 自身 `cordis.patch.yml`**；
3. **home 级 `$DSH_HOME/cordis.patch.yml`**（机器级偏好，所有 profile 共享）；
4. **`--patch <path>` 覆盖层**（按 argv 顺序）。

补丁语义：**"Later layers win per row"**——后层按行覆盖，**替换目标行的完整 config 值，不做深合并**，可插入新行。

检查合成配置[^1]：

```bash
dsh --profile web --dump-default-config          # 只看 bundle 层
dsh --profile web --patch ./extra.yml --dump-config  # 含 profile/home 补丁与 --patch 覆盖层
```

> [!tip] 大白话
> 把补丁树想成一层层铺在桌上的透明纸。后铺的纸会盖住先铺的同一位置，但不会去改下面那层的其他内容——「整行替换，不做深合并」。

## 3.2 两级配置：Profile 与 Agent Preset

- **Profile（进程级）**：决定装哪些 bundle。`web`（base + web-app）与 `headless`（base + headless）首次使用自动从模板初始化；其他缺失 profile 需 `dsh plugin --profile <name> add <package>`[^1]。
- **Agent Preset（会话级）**：决定工具/提示词/skill/子代理。内置 4 个预设：`minimal` / `standard` / `code` / `cordis`。作用域解析：`agent → preset → global`[^1]。

其中 `minimal` 固定系统提示 "You are a helpful software engineer assistant."，只组合 `bash` + `str_replace_editor` 两个工具。

## 3.3 权限与安全

- 新会话默认 **`workspace-write`** 权限预设；
- Bash 与文件系统变更限制在**会话工作区与平台临时根**；读、网络访问、进程可见性不加限制；
- `DSH_PERMISSION_MODE` 改变进程级回退预设；
- 权限审批弹窗 + `ctx.sandbox` 进程隔离 + fs provider + 启动命令 env 清洗（`*KEY*/*SECRET*/*TOKEN*/*PASSWORD*`）+ 0700 临时目录；
- 核心不变量：**"Model-visible means logged"**（模型可见即已记录）——会话日志是模型上下文的唯一来源[^1]。

> [!tip] 大白话
> dsh 的权限像一张「授权清单」：默认给写工作区的权利，读文件、联网不设限；密钥类环境变量会被自动清洗，模型看不到明文。

## 3.4 模型 / Provider / API 配置

- **默认模型**：DeepSeek **V4-Flash** / **V4-Pro**（1M 上下文，maxTokens 默认 256,000），字段含 thinking、reasoningEffort（off/high/max）、retryPolicy；
- **API Key**：Web UI Settings→Models 填（write-only）；CLI 用 `apiKeyEnv` 引用环境变量，默认 `DEEPSEEK_API_KEY`；config 中**不存字面 key**；
- **凭据解析顺序**：inherited env → `$DSH_HOME/.credentials.yaml` → 调用目录 `.env` → `$DSH_HOME/.env`；
- **Base URL**：默认 `https://api.deepseek.com`，可被 `DEEPSEEK_BASE_URL` 覆盖（接入兼容网关/本地代理）；
- **第三方 Provider**（约 40 家目录内）：Add provider 挑 Anthropic/OpenAI 等填 key 即可；Bedrock/Vertex/Azure/Codex 走各自原生认证，不能只填 key；
- **自定义 OpenAI-compatible provider**：写 `$DSH_HOME/settings.yaml` 的 `llm-pi-ai.providers` 下[^1]：

```yaml
providers:
  my-gateway:
    displayName: My Gateway
    apiKeyEnv: GATEWAY_API_KEY
    api: openai-completions
    baseURL: https://gateway.example/v1
    models:
      - id: my-model
        input: [text, image]   # 省略则纯文本
    defaultInput: [text]
```

Provider ID **永久**（请求/会话/默认值/凭据引用都用它），重命名只能新建再删旧。

> [!warning] 常见模型错误
> - `MISSING_CREDENTIAL`：未配 key，检查凭据解析顺序；
> - `UNKNOWN_MODEL`：模型未配置，检查 provider models；
> - 模型发现返回 401：检查 key；发现逻辑调 OpenAI 兼容的 `GET /models`。

## 3.5 环境变量速查

| 变量 | 作用 |
|---|---|
| `DSH_HOME` | profile 目录根（`$DSH_HOME/profiles/<name>`）；含 `cordis.patch.yml`、`.credentials.yaml`、`.env` |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `DEEPSEEK_BASE_URL` | 覆盖默认 `https://api.deepseek.com` |
| `DEEPSEEK_SEARCH_BASE_URL` | 搜索可用的替代 base URL |
| `DSH_PERMISSION_MODE` | 改变进程权限回退 |
| `DSH_TOOLS_MODE` | `native` / `code` / `both`；其他值启动失败 |
| `DSH_TELEMETRY_MODE=FULL` | 每个 session 事件以 OTLP/HTTP 日志流出 |
| `DSH_TELEMETRY_DISABLED` | 任意非空值即硬性退出遥测 |
| `NODE_USE_ENV_PROXY=1` | 让 Node 遵循 `HTTP_PROXY`/`HTTPS_PROXY` |

## 3.6 默认装载与边界

- 基础 bundle 装载：原生 DeepSeek 适配器、settings/credentials provider、稳定的 `web_search`、遥测默认关闭；
- **`web_fetch` 默认禁用**，除非 patch 层插入 provider 并启用；
- [[MCP协议|MCP]] 客户端 `@deepseek-ai/dsh-mcp-client` 作为依赖存在，但**默认不启用任何 MCP server**（server 命令是沙箱外受信可执行代码）；
- 会话内容索引使用内存 SQLite；**所有模式**将**调用目录作为默认工作区根**，加载适用的 `AGENTS.md` 或 `CLAUDE.md`，渲染预算 65,536 字节[^1]。

## 3.7 CLI 完整参考

- **launcher 规则**：launcher 标志必须在 app 参数之前；launcher 解析器消费一个 `--`（app 参数要字面 `--` 需写 `-- --`）；launcher 标志在第一个无法识别的 token 处结束，其余原样交给 profile（`ctx.cmdlineArgs`）。首个 app 参数等于 `web` 或 `plugin` 时选择对应子命令[^1]。

| 命令 | 用途 |
|---|---|
| `dsh web` | 硬编码别名 `--profile web`；参数 `--host`、`--port`、可重复 `--trusted-host`；**刻意不支持 `--host 0.0.0.0`** |
| `dsh --profile headless "任务"` | 一次性任务，适合 CI；退出码 0/1 |
| `dsh --profile <name>` | 启动指定 profile |
| `dsh plugin --profile <name> <args...>` | 转发给 pnpm（以 profile 目录为工作目录），支持 `add`/`remove`/`why`/`update` 等 |
| `dsh --dump-config` / `--dump-default-config` | 打印合成配置（含来源文件注释）；`!!js` 表达式保持未求值 |
| `dsh --help` / `-V` / `--version` | 帮助/版本 |

- **插件管理后协调**：每次 pnpm 成功后，`dsh.profile.bundles` 与已安装状态对齐；声明了 `dsh.bundle.patch` 的依赖加入层栈，被移除的依赖离开层栈；
- **热重载**：profile 启动时监听 profile 与 home 两个 `cordis.patch.yml` 的编辑并事务性重放；但活动编辑不能重置已占用的端口；
- **关闭行为**：进程关闭给插件树最多 5 秒清理；首个 SIGINT/SIGTERM 触发优雅排空（SIGTERM 退出码 0，SIGINT 报 130），第二个信号强制立即退出。

## 3.8 插件开发基础：第一个插件

dsh 的「一切皆插件」不是口号——官方用一整页教你写第一个插件[^2]。前提：已完成源码运行路径（README 的 run from source）。

### 插件是什么

插件是导出 `apply` 函数的 TypeScript 模块。框架加载时调用 `apply` 并传入 `ctx`（上下文对象），通过 `ctx` 注册能力[^2]：

```ts
import type { Context } from '@deepseek-ai/cordis'

export const name = 'my-plugin'

export function apply(ctx: Context) {
  // Register capabilities here.
}
```

### 创建并注册

```bash
mkdir -p scratch-plugin/src          # 在仓库根创建临时项目
```

创建 `scratch-plugin/src/my-plugin.ts` 后，在仓库根运行 `pwd` 拿绝对路径，写 `scratch-plugin/cordis.yml`：

```yaml
- insert:
    - id: hello
      name: '/absolute/path/to/deepseek-harness/scratch-plugin/src/my-plugin.ts'
```

> [!warning] 插件路径必须是绝对路径
> patch 文件只贡献配置，不会改变 loader 解析模块路径时使用的 profile 目录——相对路径会失效。

启动并验证：

```bash
pnpm dsh web --patch ./scratch-plugin/cordis.yml
# 打开 http://127.0.0.1:3080，终端应打印 [hello-plugin] plugin loaded!
```

### 自动清理与依赖

- 通过 `ctx` 注册的任何东西（事件监听、工具、定时器）在插件卸载时自动清理，无需手动 removeListener / clearInterval；
- 需要手动清理的资源用 `ctx.effect()`；
- 使用其他服务（如 `tools`、`llm`）时声明 `inject`，框架保证依赖就绪后才加载插件。

### 插件的三种形态

- **函数形式**：具名导出 `name` + `apply`（多数情况足够）；
- **对象形式**：`export default { name, inject, apply(ctx) { ... } }`；
- **类形式**：继承 `Service`，`static inject = ['tools']`，构造函数同步初始化，`super(ctx, 'myService')`——适用于向其他插件提供服务的场景。

## 3.9 system-prompt 子系统：系统提示词如何组装

`system-prompt` 包（`packages/core/system-prompt`）是负责**在每次模型调用前组装最终系统提示词**的注册表服务 `ctx.systemPrompt`[^3]。想理解 dsh 的提示词体系，这是权威参考。

### 提示词段落 PromptSection

```ts
interface PromptSection {
  readonly name: string        // 必须唯一，重复注册抛错
  readonly order: number       // 升序拼接
  readonly text: string | ((context) => string)  // 可含 {{variable}} 占位符
  readonly complete?: boolean  // true = 该段即完整系统提示词
}
```

**order 约定**：`-100` harness 身份 → `0` 部署人格（persona）→ 其他负数在人格前 → `100–199` 工具指导。

**complete 语义**：`complete: true` 的段表示「贡献就是完整系统提示词」。组装仍会跑协作瀑布（解析工具/上下文/变量），随后把该段恢复为唯一提示词段；多个生效 complete 段 → 组装失败。

### 作用域与遮蔽

- 作用域级段落/变量/动态上下文**遮蔽**（shadow）全局同名项；
- 工具提供方例外：全局与匹配作用域**共同贡献**；
- 变量名匹配 `[a-z][a-z0-9_]*`，`{{variable}}` 在渲染期由 `renderPrompt` 插值，不是组装期。

### 事件

- `system-prompt/assemble`（waterfall）：返回值权威，监听者可修改 assembly；已注册 complete 段在瀑布后恢复，监听者不能再向该系统提示词增删内容；
- `system-prompt/change`（emit）：任何提示词提供方变化时发出，未过滤。

### 关键防错与持久化

- `knownNames`：区分「配置名拼写错误」与「已知工具在作用域内被有意隐藏」；
- `PromptContext`：缓存安全的动态上下文，物化为 durable user-role snapshot，仅当快照变化或被 compaction 移除时才追加到模型历史——避免每回合重复写入。

---

## 本章小结

> [!summary]
> - 配置是**多层 YAML 补丁树**：bundle → profile → home → `--patch`，后层整行替换、不做深合并，用 `--dump-config` 排查；
> - **两级配置**：Profile（进程级，决定 bundle）与 Agent Preset（会话级，内置 `minimal`/`standard`/`code`/`cordis` 四预设）；
> - 权限默认 `workspace-write`，密钥 env 自动清洗，核心不变量「模型可见即已记录」；
> - 模型层默认 V4-Flash/Pro，可换约 40 家第三方 provider 或自定义 OpenAI-compatible provider；
> - CLI 有严格 launcher 规则：标志须在 app 参数前；
> - 进阶：插件开发走 `cordis.yml` patch + `apply(ctx)`（三种形态）；系统提示词由 `ctx.systemPrompt` 注册表按 order 组装，`complete` 段可独占。

下一章做迁移决策：[[DeepSeek-Harness 与ClaudeCode对照迁移|换还是留？]]

---

## 更新记录

- 2026-08-14：新增 3.8 插件开发基础（第一个插件）、3.9 system-prompt 子系统参考，依据官方文档 develop/basic 与 reference/subsystems/system-prompt。

---

[^1]: 素材来源：DeepSeek Harness 官方仓库与文档（2026-08-13 收集）。
[^2]: 素材来源：DeepSeek Harness 官方文档「开发基础：第一个插件」（2026-08-14 收集）。
[^3]: 素材来源：DeepSeek Harness 官方文档「system-prompt 子系统参考」（2026-08-14 收集）。
