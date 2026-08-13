# DeepSeek-Harness 配置使用教程 - 深度研究素材

收集时间: 2026-08-13
搜索关键词: deepseek-harness 安装 / 快速上手 / 配置 / CLI / 对比迁移 / 成本
已选方向: 快速上手 + 对比迁移（A + D）
素材来源: deepseek-ai/deepseek-harness 官方仓库与文档、技术博客、新闻报道

---

## 第一部分：产品定位

- **deepseek-harness（dsh）**：DeepSeek 官方开源的 agent harness，2026-08-13 发布 v0.1 开发者预览，MIT 协议，约 26.5k stars。
- 核心公式：**Model + Harness = Agent**。它不是新模型、不是 API 客户端，而是「把模型接入文件系统、终端、网页、代码工具并组织上下文/工具调用/任务执行」的运行框架。
- 核心架构：**「一切皆插件」**（Everything is a Plugin），由 Cordis 框架驱动，无特权核心——模型适配器、工具注册表、会话日志、Agent loop、沙箱均可替换。
- 官方对标：Claude Code 与 OpenAI Codex；中文报道称其「不只是 DeepSeek 版 Claude Code」，更接近可组装的 agent 运行时。
- **开发状态警告**：README 明确 "THERE WILL BE COMPATIBILITY-BREAKING CHANGES."，当前迭代很快，接口可能不兼容。
- 反馈渠道：官方**不开 GitHub Issues**，bug/建议一律走 GitHub Discussions；社区还有 Discord 与微信群。
- 易混淆：注意同名第三方包（`pip install deepseek-harness`、`npx @deepseek-harness/mcp` 均非官方）；官方包名为 `@deepseek-ai/dsh` 与 `deepseek-harness-sdk`。

## 第二部分：安装与快速上手

### 安装三路径

| 方式 | 命令 | 前置要求 |
|---|---|---|
| **npm（推荐）** | `npx @deepseek-ai/dsh web` | 仅需 Node.js |
| **源码构建** | `git clone https://github.com/deepseek-ai/deepseek-harness.git` → `pnpm install` → `pnpm run build` → `pnpm dsh web` | Node `^22.19 \|\| >=24` + pnpm |
| **Python SDK** | `pip install deepseek-harness-sdk` | Python 3.10+；Linux x64/arm64 或 macOS 14+ arm64；运行时无需系统 Node.js |

> 官方未发布预构建二进制；安装方式为 npm（npx）或源码构建。

### 首次配置与跑通第一个会话（Web UI）

1. 运行 `npx @deepseek-ai/dsh web`，浏览器打开 **http://127.0.0.1:3080**（默认地址）。
2. **Settings → Models** 填 DeepSeek API Key，保存即生效（无需重启）。密钥 **write-only**：页面只回显脱敏描述，明文存于 `$DSH_HOME/.credentials.yaml`。
3. 点 **Choose workspace** 选择项目目录（**不选工作区无法开始会话**）；dsh 以调用目录作为默认文件系统根。
4. 新建会话发送首个任务，官方示例：`Summarize this repository and identify its main packages.`
5. 涉及需审批的操作会按当前权限策略弹出确认（新会话默认 `workspace-write` 权限预设）。

### CLI 快速验证（headless 一次性任务）

```bash
dsh --profile headless "run the tests"
```

- 提交任务 → 等待 agent 静默 → 打印最后一条非空助手消息 → 退出。
- 退出码：`0` 表示 completed，`1` 表示失败；不开监听端口、无交互跟进面，适合 CI。
- 每次调用创建新 agent，无 resume 机制；每次任务创建全新持久化会话。

### 常见安装/上手坑

1. Web 端口被占 → `dsh web --port <空闲端口>`。
2. npm 装插件 ERESOLVE peer 冲突 → `--legacy-peer-deps`。
3. Windows 下多插件重复注册 `ctx.bash` → 报 "service bash has been registered" 启动失败。
4. 官方不开 Issues，问题只能走 GitHub Discussions。
5. developer preview 期，升级注意破坏性变更。
6. 谨防与官方同名的第三方包。

## 第三部分：配置体系

### 配置机制（不是 config.toml！）

dsh 的配置是 **YAML 补丁树**，在空根上按顺序叠加：

1. **bundle 补丁**：profile manifest 中 `dsh.profile.bundles` 列表命名的每个 bundle 补丁；
2. **profile 自身 `cordis.patch.yml`**；
3. **home 级 `$DSH_HOME/cordis.patch.yml`**（机器级偏好，所有 profile 共享）；
4. **`--patch <path>` 覆盖层**（按 argv 顺序）。

补丁语义：**"Later layers win per row"** —— 后层按行覆盖，**替换目标行的完整 config 值，不做深合并**，可插入新行。

检查合成配置：
```bash
dsh --profile web --dump-default-config          # 只看 bundle 层
dsh --profile web --patch ./extra.yml --dump-config  # 含 profile/home 补丁与 --patch 覆盖层
```

### 两级配置

- **Profile（进程级）**：决定装哪些 bundle。`web`（base + web-app）与 `headless`（base + headless）首次使用自动从模板初始化；其他缺失 profile 需 `dsh plugin --profile <name> add <package>`。
- **Agent Preset（会话级）**：工具/提示词/skill/子代理。内置 **4 个预设**：`minimal` / `standard` / `code` / `cordis`。作用域解析：`agent → preset → global`。
  - `minimal` 固定系统提示 "You are a helpful software engineer assistant."，只组合 `bash` + `str_replace_editor` 两个工具。

### 权限与安全

- 新会话默认 **`workspace-write`** 权限预设。
- Bash 与文件系统变更被限制在**会话工作区与平台临时根**；读、网络访问、进程可见性不加限制。
- `DSH_PERMISSION_MODE` 改变进程级回退预设。
- 权限审批弹窗 + `ctx.sandbox` 进程隔离 + fs provider + 启动命令 env 清洗（`*KEY*/*SECRET*/*TOKEN*/*PASSWORD*`）+ 0700 临时目录。
- 核心不变量：**"Model-visible means logged"**（模型可见即已记录）——会话日志是模型上下文的唯一来源。

### 模型 / Provider / API 配置

- **默认模型**：DeepSeek **V4-Flash** / **V4-Pro**（1M 上下文，maxTokens 默认 256,000），字段含 thinking、reasoningEffort（off/high/max）、retryPolicy。
- **API Key**：Web UI Settings→Models 填（write-only）；CLI 用 `apiKeyEnv` 引用环境变量，默认 `DEEPSEEK_API_KEY`；config 中**不存字面 key**。
- **凭据解析顺序**：inherited env → `$DSH_HOME/.credentials.yaml` → 调用目录 `.env` → `$DSH_HOME/.env`。
- **Base URL**：默认 `https://api.deepseek.com`，可被 `DEEPSEEK_BASE_URL` 覆盖（接入兼容网关/本地代理）。
- **第三方 Provider**（约 40 家目录内）：Add provider 挑 Anthropic/OpenAI 等填 key 即可；Bedrock/Vertex/Azure/Codex 走各自原生认证，不能只填 key。
- **自定义 OpenAI-compatible provider**：写 `$DSH_HOME/settings.yaml` 的 `llm-pi-ai.providers` 下：
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
- **常见错误**：`MISSING_CREDENTIAL`（未配 key）、`UNKNOWN_MODEL`（模型未配置）、模型发现返回 401（检查 key；发现逻辑调 OpenAI 兼容的 `GET /models`）。

### 环境变量速查

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

### 默认装载与边界

- 基础 bundle 装载：原生 DeepSeek 适配器、settings/credentials provider、稳定的 `web_search`、遥测默认关闭。
- **`web_fetch` 默认禁用**，除非 patch 层插入 provider 并启用。
- MCP 客户端 `@deepseek-ai/dsh-mcp-client` 作为依赖存在，但**默认不启用任何 MCP server**（server 命令是沙箱外受信可执行代码）。
- 会话内容索引使用内存 SQLite；所有模式将**调用目录作为默认工作区根**，加载适用的 `AGENTS.md` 或 `CLAUDE.md`，渲染预算 65,536 字节。

## 第四部分：CLI 完整参考

- **launcher 规则**：launcher 标志必须在 app 参数之前；launcher 解析器消费一个 `--`（app 参数要字面 `--` 需写 `-- --`）；launcher 标志在第一个无法识别的 token 处结束，其余原样交给 profile（`ctx.cmdlineArgs`）。首个 app 参数等于 `web` 或 `plugin` 时选择对应子命令。

| 命令 | 用途 |
|---|---|
| `dsh web` | 硬编码别名 `--profile web`；参数 `--host`、`--port`、可重复 `--trusted-host`；**刻意不支持 `--host 0.0.0.0`** |
| `dsh --profile headless "任务"` | 一次性任务，适合 CI；退出码 0/1 |
| `dsh --profile <name>` | 启动指定 profile |
| `dsh plugin --profile <name> <args...>` | 转发给 pnpm（以 profile 目录为工作目录），支持 `add`/`remove`/`why`/`update` 等 |
| `dsh --dump-config` / `--dump-default-config` | 打印合成配置（含来源文件注释）；`!!js` 表达式保持未求值 |
| `dsh --help` / `-V` / `--version` | 帮助/版本 |

- **插件管理后协调**：每次 pnpm 成功后，`dsh.profile.bundles` 与已安装状态对齐；声明了 `dsh.bundle.patch` 的依赖加入层栈，被移除的依赖离开层栈。
- **热重载**：profile 启动时监听 profile 与 home 两个 `cordis.patch.yml` 的编辑并事务性重放；但活动编辑不能重置已占用的端口。
- **关闭行为**：进程关闭给插件树最多 5 秒清理；首个 SIGINT/SIGTERM 触发优雅排空（SIGTERM 退出码 0，SIGINT 报 130），第二个信号强制立即退出。

## 第五部分：与 Claude Code 对照 / 迁移

### 概念对照表

| 维度 | Claude Code | deepseek-harness (dsh) |
|---|---|---|
| 定位 | 开箱即用的闭源 CLI 成品 | 开源（MIT）可组装的 agent 运行时 |
| 架构 | 单体核心 + 扩展 | 一切皆插件，无特权核心 |
| 一次性任务 | `claude -p "..."` | `dsh --profile headless "..."` |
| 配置文件 | `settings.json` / `CLAUDE.md` / `.mcp.json` | YAML 补丁树（bundle / `cordis.patch.yml` / `--patch`）+ Profile + Agent Preset |
| 权限模式 | 权限提示 + 命令行 flag | `workspace-write` 默认预设 + `DSH_PERMISSION_MODE` |
| 工作区根 | 启动目录 | 调用目录（headless 模式） |
| 上下文文件 | 自动加载 `CLAUDE.md` | 自动加载 `AGENTS.md` 或 `CLAUDE.md`（65,536 字节预算） |
| 模型 | 绑定 Claude | 默认 DeepSeek V4，可换 ~40 家 + OpenAI-compatible |
| MCP | 成熟支持 | 仅桥 tools（stdio + streamable-http），Resources/Prompts 尚无消费者 |
| 成熟度 | 成熟稳定 | developer preview，有破坏性变更 |

### 成本对比（90% 输入缓存命中、每任务 80K 输入 + 20K 输出）

| 模型 | 输入价 /1M | 输出价 /1M | 每任务成本 | 每 $100 任务数 |
|---|---|---|---|---|
| Claude Opus 4.8 | $5.00 | $25.00 | ~$0.54 | ~185 |
| Claude Sonnet 4.6 | — | — | ~$0.13 | ~770 |
| DeepSeek V4 Pro | $0.435 | $0.87 | ~$0.021 | ~4,760 |
| DeepSeek V4 Flash | $0.14 | $0.28 | ~$0.007 | ~14,300 |

- 输出定价差距约 **28 倍**（V4 Pro $0.87 vs Opus $25.00 /1M）。
- 规模化：每天 5,000 任务，Opus 月成本约 $79,000 vs V4 Pro 约 $3,150。

### 性能对比

| 基准 | Claude Opus 4.8 | DeepSeek V4 Pro |
|---|---|---|
| SWE-bench Pro（仓库级） | 69.2% | 55.4% |
| SWE-bench Verified | 88.6% | 80.6%（V4 Pro Max） |
| LiveCodeBench Pass@1 | 88.8% | 93.5%（V4 Pro Max） |
| Terminal-Bench | 65.4% | 67.9% |
| MCPAtlas Public（工具调用） | ~73.6 | 73.6（平手） |

结论：**harness 与工具 schema 设计比模型选择更重要**；Opus 在仓库级多文件架构一致性领先，V4 Pro 在有界算法任务与终端代理任务上反超。

### 迁移策略（三选）

1. **整体换 harness**：`npx @deepseek-ai/dsh web` 直接上手 dsh，配置从 settings.json/CLAUDE.md 迁移到 cordis.patch.yml / Agent Preset。
2. **DeepClaude 模式（保留 Claude Code，换底模）**——DeepSeek 官方支持：
   ```bash
   export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
   export ANTHROPIC_API_KEY="your-deepseek-api-key"
   ```
   结构性便宜 10–25 倍。权衡：失去 Opus 特有推理行为，部分 Anthropic API 参数映射不完整。
3. **按复杂度路由**（核心建议）：
   - 琐碎改动/样板/单文件修复/测试编写 → **V4 Flash**
   - 标准功能实现与调试 → **V4 Pro**
   - 多文件架构重构、安全敏感变更 → **Opus**
   - 默认用 DeepSeek 后端跑所有会话，保留 Anthropic key 供显式升级（"95% 任务不付 Opus 价"）。

### 选择建议

- **选 Claude Code**：跨模块仓库级重构、团队已有 Claude Code 肌肉记忆、安全审计/支付系统/生产数据库迁移等高风险任务、需要 Anthropic 专属功能（子代理、上下文压缩、安全对齐）。
- **选 DeepSeek/dsh**：高频低成本循环（PR 审查、测试生成、文档更新）、并行子代理（16 个 V4 Flash worker 经济可行）、自托管/数据主权（V4 权重 MIT 可下载）、构建非编码类自定义 agent、非开发者想要 GUI。

### DeepSeek V4 协议坑（第三方整理，供迁移时规避）

- thinking 默认开启，会烧 token；多轮对话必须回传 `reasoning_content`，否则 HTTP 400；必须设 `max_tokens`（否则 reasoning 流可达 26KB/84s 撑爆客户端）；thinking 模式下 `tool_choice` 只能 `auto`。

---

## 综合分析

1. **dsh 定位清晰**：作为 DeepSeek 官方 agent harness，核心卖点是「一切皆插件」的可组装性与开源（MIT），官方目标是提供可替换的 agent 运行时，而非与 Claude Code 正面对拼成熟度。
2. **快速上手路径明确**：对熟悉 Claude Code 的用户，安装（npx）→ 配 Key（Settings→Models 或 DEEPSEEK_API_KEY）→ Choose workspace → 首个任务，5 分钟内可跑通；headless 模式适合测试连通性与 CI。
3. **配置心智模型不同**：Claude Code 的 settings.json/CLAUDE.md 是「声明式文件」，dsh 是「多层 YAML 补丁树 + Profile + Agent Preset」，迁移重点在于理解「后层整行替换、不做深合并」与「一切皆插件」。
4. **成本是主要驱动**：V4 Flash/Pro 相对 Claude 有 7–77 倍成本优势；「保留 Claude Code + DeepSeek Anthropic 兼容端点」是低摩擦迁移方案。
5. **现实差距**：dsh 处于 developer preview，CLI 尚无完整交互式 REPL、MCP 仅桥 tools、插件生态约 300 但成熟度待验证、官方不开 Issues；适合尝鲜与低成本任务，关键工程仍需 Claude Code/Opus 兜底。
