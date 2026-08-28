# 第 5 章 MCP 接入与排错

前几章我们摸清了 Hermes 的内置工具体系、Tool Gateway 云能力、以及「自己写一个工具」的完整路径。但真实世界里，绝大多数能力早就有人帮你封装好了——GitHub、数据库、浏览器栈、内部 API、SaaS 服务。本章就讲 Hermes 接入这些外部能力的标准通道：MCP（Model Context Protocol）。我们会从「MCP 是什么」建立心智模型，走通一个真实的 stdio 服务器接入，再掌握过滤、信任模型与命名规范，最后给出一份「工具不显示」的 5 步排查序列。版本锚定 v0.20.x，所有配置键以 `hermes doctor` 输出为准。

> 提示：本章与第 6 章安全基线是姊妹篇——MCP 的 `trust` 信任模型会在第 6 章和 approvals 审批体系一起收束成完整的安全姿态。

## 5.1 MCP 是什么：把外部能力接入普通工具注册表

MCP 是一套让 LLM 客户端连接外部工具服务器的协议。它允许 Hermes 使用 Hermes 之外的现成工具——GitHub、数据库、文件系统、浏览器栈、内部 API，无需先为每个外部能力写一个原生 Hermes 工具（来源 S4）。如果你想让 Hermes 用上「某个地方已经存在」的工具，MCP 通常是最干净的路径（来源 S4）。

> [!tip] 大白话
> 把 Hermes 想成一台主机，MCP 服务器就是「即插即用的外接设备」。你不用拆开主机去焊一个新的内部模块（写原生工具），只要往配置里插一根线，这个设备的全部功能就出现在 Hermes 的工具列表里了。所以「接入 MCP」≈「插上外接工具箱」。

MCP 接入后发生的事，可以归纳成四句话（来源 S4）：

1. **启动时自动发现并注册**：Hermes 启动时发现配置里启用的 MCP 服务器，把它们暴露的工具注册进普通工具注册表——和内置工具走同一个注册表，模型能像用内置工具一样调用它们。
2. **生成 runtime toolset**：每个贡献了至少 1 个工具的服务器，会生成一个运行时工具集 `mcp-<server>`（来源 S4）。这意味着你可以在 `hermes tools`、`--toolsets` 的语境里，按「服务器」这个粒度去思考和管理这批工具。
3. **工具命名带前缀**：为避免与内置工具名冲突，MCP 工具会被加前缀（具体命名见 5.5）。
4. **支持动态刷新**：服务器可以在运行时通知 Hermes 工具列表变了（`notifications/tools/list_changed`），Hermes 会自动重新拉取并更新注册表，无需手动 `/reload-mcp`（来源 S4）。

## 5.2 配置入口：`mcp_servers`（stdio 与 HTTP 共存于一 config）

MCP 的唯一配置入口是 `~/.hermes/config.yaml` 下的 `mcp_servers` 键（来源 S4）。一个 config 里可以同时混用两种 transport：

- **stdio 服务器**：以本地子进程方式运行，通过 stdin/stdout 与 Hermes 通信。用 `command` / `args` / `env` 描述。适合：服务器装在本地、要低延迟访问本地资源、或 MCP 服务器文档给了 `command` / `args` / `env` 示例（来源 S4）。
- **HTTP 服务器**：远程端点，Hermes 直接连过去。用 `url` / `headers` 描述。适合：服务器托管在别处、组织内部暴露了 MCP 端点、或你不想让 Hermes 为这个集成拉起本地子进程（来源 S4）。

两种服务器可以写在同一个 `mcp_servers` 块里，互不干扰。

> [!tip] 大白话
> stdio 服务器像「在你电脑上请了一位本地专员，他通过对话窗口跟你交流」；HTTP 服务器像「直接打电话给远程客服中心」。两者可以在同一份通讯录里各占一行。

每个服务器条目下的常用键（来源 S4、S10）：

| 键 | 类型 | 含义 |
| --- | --- | --- |
| `command` / `args` / `env` | string / list / map | stdio 服务器：可执行命令、参数、传给子进程的环境变量 |
| `url` / `headers` | string / map | HTTP 服务器：端点地址、请求头 |
| `enabled` | bool | `false` 时完全跳过该服务器 |
| `timeout` | number | 单次工具调用超时，默认 `300` 秒 |
| `connect_timeout` | number | 首次连接（含 MCP `initialize` 握手）超时，默认 `60` 秒 |
| `transport` | string | 仅 HTTP：默认 Streamable HTTP，设 `sse` 改用 SSE 传输（不同版本对默认值的标注有差异，以 `hermes doctor` 输出为准） |
| `protocol` | string | 协议时代协商：`auto`（默认，先走 legacy `initialize` 握手，服务器拒绝时回退到 `server/discover` 无状态探测）/ `stateless` / `legacy` |
| `supports_parallel_tool_calls` | bool | 该服务器工具是否允许并发执行，默认 `false`（串行） |
| `tools` | map | 工具过滤与 utility 策略（见 5.4） |
| `trust` | string | 信任层级：`full`（默认）或 `untrusted`（见 5.5） |

### `enabled: false`：完全跳过

`enabled: false` 的行为是「三不」：不连接、不发现、不注册——Hermes 甚至不会尝试连接（来源 S4、S10）。配置会保留在原处，方便以后重新启用。这是你在不删配置的前提下临时停用某个服务器、或排错时隔离某个嫌疑项的最快开关。

## 5.3 实操：接入一个 MCP 服务器（github 示例）

下面我们接入 GitHub 的官方参考 MCP 服务器 `@modelcontextprotocol/server-github`（stdio）。先看一眼完整配置（先睹为快），再逐段拆讲。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  github:
    transport: stdio
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${env:GITHUB_TOKEN}"
    enabled: true
    timeout: 300
    connect_timeout: 60
    protocol: auto
    tools:
      include: ["*"]
    trust: untrusted
```

逐段拆讲：

- **`github:`**——服务器名，也是后续工具名前缀和 runtime toolset 名的来源（`mcp-github`）。可以随意起名，但建议与服务器身份一致。
- **`transport: stdio`**——声明这是本机子进程型服务器。stdio 服务器靠 `command` 起进程，不写 `url`。
- **`command: npx` + `args: ["-y", "@modelcontextprotocol/server-github"]`**——用 npx 直接拉取并运行 GitHub 参考服务器。`-y` 表示自动确认安装。前提是本机有 Node.js（`node --version` / `npx --version` 可验证）。
- **`env:`**——传给子进程的环境变量。这里用 `GITHUB_PERSONAL_ACCESS_TOKEN` 填 PAT，值用 `${env:GITHUB_TOKEN}` 从环境变量引用（见 5.6），避免在 config.yaml 里明文写死。
- **`enabled: true`**——显式打开。省略时默认也是启用，但写出来更清楚。
- **`timeout: 300` / `connect_timeout: 60`**——调用超时与连接超时，用默认值即可；如果你的服务器个别工具特别慢，可以单独调大 `timeout`。
- **`protocol: auto`**——协议协商走默认，一般不需要动。
- **`tools: include: ["*"]`**——把这台服务器暴露的所有工具都注册进来（过滤见 5.4）。
- **`trust: untrusted`**——声明「这台服务器不完全可信」：凡是没带 `readOnlyHint: true` 注解的写工具，每次调用都会走审批（见 5.5）。

配置好后启动 `hermes chat`，Hermes 会在启动时自动发现并注册。你可以直接说「列出 github 仓库 open 的 issue」，模型会像调用内置工具一样使用这批 MCP 工具（来源 S4）。

> [!warning]
> GitHub 官方托管 MCP 需要每个客户端自带 OAuth App（通用动态客户端注册会被拒绝），所以 Hermes 的目录里**故意没有** GitHub——它用内置的 `github/*` skills 驱动 `gh` CLI 作为更强的集成（来源 S4）。上面我们手动接的是社区参考服务器，需要你自己提供 PAT。接其它 OAuth 型远程服务器时走 5.6 的 `auth: oauth`。

### 目录 CLI：一条命令装好审核过的 MCP

Hermes 自带一个经过 Nous 团队审核的 MCP 目录（来源 S4）。目录条目默认禁用，只装你真正需要的：

```bash
hermes mcp                # 交互式选择器（默认），可安装/启用/禁用/卸载
hermes mcp catalog        # 纯文本列表，适合脚本化
hermes mcp install n8n    # 按名安装一个目录条目
hermes mcp configure linear   # 重开该条目的工具勾选清单
hermes mcp login <server>     # 补 OAuth 登录 / 重新认证
hermes mcp add codex --preset codex   # 内置预设：填入 codex 的 command/args
```

目录条目存在 `optional-mcps/`，出现即代表 Nous 审核通过；安装会按其 manifest 执行 clone / bootstrap / 启动命令，所以**安装前仍建议读一下 manifest**（来源 S4）。`hermes mcp add codex --preset codex` 会写 `command: "codex"`、`args: ["mcp-server"]`（来源 S4），预设只填默认值，你同命令行传的 env / headers / 过滤仍优先生效。

### `/reload-mcp` 与动态刷新

两条刷新路径，适用不同场景（来源 S4）：

1. **服务器主动推送**：MCP 服务器可以在运行时发 `notifications/tools/list_changed` 通知（例如数据库加载了新 schema、服务下线了一批工具）。Hermes 收到后自动重新拉取工具列表并更新注册表，**不需要手动 `/reload-mcp`**。刷新有锁保护，同一服务器的连续通知不会造成重叠刷新。
2. **你改了配置**：手动改了 `mcp_servers` 里的内容后，在会话里执行 `/reload-mcp`，Hermes 会从配置重新加载服务器并刷新工具列表。

> [!tip] 大白话
> 第一条是「外接设备自己广播：我的按键布局变了，请重新识别」；第二条是「你亲手换了设备，重启一下让系统重新认」。两条路都能让工具列表保持最新，只是触发者不同。

## 5.4 工具过滤：`tools.include` / `tools.exclude`

一台 MCP 服务器可能暴露几十上百个工具（Cloudflare 的 API MCP 有约 3,300 个端点工具）。把不想让模型看到的工具挡在注册表之外，既省 token 也是安全控制（来源 S4、S10）。

- **`tools.include`**：白名单。设置后**只有**列出的工具被注册。
- **`tools.exclude`**：黑名单。设置且没有 `include` 时，除列出的外全部注册。
- **glob 通配**：两个列表都接受 fnmatch 风格模式（`*`、`?`、`[...]`，大小写敏感）。不含通配符的条目按精确名匹配（`docs` 只排除 `docs`，不会误伤 `docs_search`）。
- **优先级**：两个都写时，`include` 优先生效（来源 S4、S10）。例如 `include: [create_issue]` 与 `exclude: [create_issue, delete_issue]` 同时存在时，`create_issue` 仍然允许，`delete_issue` 被忽略。

> [!tip] 大白话
> `include` 像安检「只放行清单上的物品」，`exclude` 像「除清单外都可放行」。两个清单同时贴出来时，以「只放行」那张为准——白名单优先。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${env:GITHUB_TOKEN}"
    tools:
      include: [list_issues, create_issue, update_issue, search_code]  # 白名单：只注册这几个
      resources: false
      prompts: false
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authorization: "Bearer ${env:STRIPE_TOKEN}"
    tools:
      exclude: [delete_customer, refund_payment]   # 黑名单：去掉危险动作
```

### utility 过滤：resources / prompts

Hermes 在服务器支持时会额外注册四个工具：`list_resources`、`read_resource`、`list_prompts`、`get_prompt`。它们分别对应 MCP 的 resources（资源）与 prompts（提示词模板）能力（来源 S4）。

- `tools.resources: false` 关闭 `list_resources` + `read_resource`
- `tools.prompts: false` 关闭 `list_prompts` + `get_prompt`

而且注册是**能力感知**的：即使你开着 `resources: true`，如果服务器会话本身不支持资源操作，也不会注册这些包装工具（来源 S4）。所以「开了 prompts 却没看到 prompt 工具」通常是正常的——服务器不支持这个能力，而不是配错了。

**全过滤掉会怎样？** 如果配置把该服务器所有可调用工具都滤掉、且没有注册任何 utility 工具，Hermes **不会创建空的 runtime MCP toolset**，保持工具列表干净（来源 S4）。

> [!warning]
> 写 `include` / `exclude` 时用服务器的**原始工具名**（可能带连字符、点号），不要用注册后的净化名。例如服务器叫 `my-api`、工具叫 `list-items.v2`，过滤时写 `list-items.v2`，而不是 `mcp__my_api__list_items_v2`（来源 S10）。

## 5.5 工具命名与信任模型

### 命名：双下划线 `mcp__<server>__<tool>`

MCP 工具注册进 Hermes 后，名字带前缀以避免与内置工具冲突（来源 S2、S10）：

```text
mcp__<server>__<tool>
```

- `mcp__github__create_issue`
- `mcp__filesystem__read_file`
- `mcp__my_api__query_data`

服务器名和工具名中的非字母数字字符（连字符、点、空格等）会被替换成下划线：`my-api` 服务器、`list-items.v2` 工具 → `mcp__my_api__list_items_v2`（来源 S10）。双下划线分隔符对齐 Claude Code、Codex、OpenCode 的约定，即使服务器名或工具名本身带下划线，也不会混淆 server/tool 边界（来源 S10）。

> **版本差异标注**：部分旧文档页（如 S4 的「How Hermes registers MCP tools」）仍写单下划线 `mcp_<server>_<tool>`（例如 `mcp_filesystem_read_file`）。本书以双下划线 `mcp__<server>__<tool>` 为准——它与 main 分支配置参考及 Claude Code/Codex 对齐，更可信；具体命名**随版本核实**，以你本机 `hermes doctor` / 实际注册结果为准（来源 §4 矛盾表）。

实际使用中你通常不需要手动去叫这个带前缀的名字——Hermes 在推理时看到这些工具会自行选择调用（来源 S4）。

### 信任模型：`trust: untrusted`

`trust` 控制这台服务器的工具调用需要多少审批（来源 S10）：

- **`trust: full`（默认）**：不加额外审批门槛。
- **`trust: untrusted`**：服务器上**每一个写能力的工具调用**（即没有 `readOnlyHint: true` 注解的工具）都必须经用户审批通过后才会执行。

这里有一个容易被忽略的细节：`readOnlyHint` 是服务器**自己声称**的提示，不是 Hermes 验证过的保证（来源 S10）。一个撒谎的服务器最多能「跳过」审批去执行它声称只读的工具——它永远无法因此获得额外权限。所以在信任边界上：

- **任何你不完全控制的服务器都标记为 `untrusted`**（来源 S10）。
- **未识别的 `trust` 值按 `untrusted` 处理（fail-closed）**——拿不准时默认收紧，不会默认放开（来源 S10）。

> [!tip] 大白话
> `untrusted` 相当于给外接设备的操作员发一张「每次进房间都要你先点头」的门禁卡：他能干活，但每一道门（写操作）都得问你一句。而 `readOnlyHint` 只是操作员自报「我只是进去看看」，Hermes 信一半——他要是撒谎说自己是只读的，最多也就偷偷瞄一眼，绝拿不到你钥匙串上别的门。

安全上，过滤配置本身也是暴露控制：禁用危险的写工具、给敏感服务器只开最小白名单、关闭不想暴露的 resource/prompt 包装（来源 S4）。这套「白名单 + untrusted + 逐次审批」的组合，会在第 6 章安全基线里与 approvals 体系一起收束。

## 5.6 高级：变量替换、env 隔离、并行、回收、OAuth 与辅助调度

### 变量替换

服务器条目里任何字符串值（`env`、`headers`、`args`、`url` 等）都可以引用变量（来源 S10）：

- `${VAR}` 与 `${env:VAR}` 等价，都从 active profile 的 secret 作用域解析（回退到进程环境）。未设置的变量保留字面量并告警。
- Cursor 风格 context 变量（大小写敏感）：`${userHome}`、`${workspaceFolder}`、`${workspaceFolderBasename}`、`${pathSeparator}` / `${/}`。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  filesystem:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    env:
      CACHE_DIR: "${userHome}${/}.cache${/}mcp"
```

### stdio env 隔离：防止密钥泄漏

stdio 服务器启动子进程时，Hermes **不会盲目把你完整的 shell 环境传过去**，只传显式配置的 `env` 加一个安全基线（来源 S4）。这直接降低了「子进程能读到你的 API key 全家桶」的风险。所以密钥要**显式声明**在 `env` 里，并优先用 `${env:VAR}` 引用。

> [!tip] 大白话
> 就像装修师傅进门，你只递给他那几把指定的房间钥匙，而不是把整串家钥匙（包括保险柜的）都挂他腰上。

### 并行调用

默认 MCP 工具**串行**执行——一次一个。只有当你确认这台服务器的工具可以安全并发时，才打开 `supports_parallel_tool_calls: true`（来源 S4）。打开后，Hermes 会在同一个 tool-call 批次里并发执行该服务器的多个工具，行为和内置只读工具（`web_search`、`read_file` 等）一致。

> [!warning]
> 读写共享状态（共享文件、数据库、外部资源）的工具**不要**开并行，先评估读写竞态再决定。默认串行就是最稳的兜底。

### stdio 回收：`idle_timeout_seconds` / `max_lifetime_seconds`

某些 stdio 服务器内存很重（比如浏览器型服务器，一次调用后常驻几百 MB 的 Chromium）。可以给它们开「自动回收」：超过空闲/总寿命阈值就拆掉子进程，下次调用时透明重启（工具全程保持注册，不丢）（来源 S4）。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  playwright:
    command: npx
    args: ["-y", "@playwright/mcp@latest", "--headless"]
    idle_timeout_seconds: 900     # 15 分钟无工具调用则回收
    max_lifetime_seconds: 86400   # 无论如何每天至少重启一次
```

两个键都是 `0` = 永不回收（默认）。

### OAuth 与令牌落盘

需要 OAuth 的远程 HTTP 服务器设 `auth: oauth`，Hermes 自动处理发现、PKCE、token 交换与刷新（来源 S4）。首次连接会打印授权 URL 并打开浏览器；令牌缓存在 `~/.hermes/mcp-tokens/<server>.json`，权限 0o600，之后静默复用直到刷新失败才需要重新授权。`hermes mcp login <server>` 用来补登录或重认证。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  linear:
    url: "https://mcp.linear.app/mcp"
    auth: oauth
```

> [!tip] 大白话
> OAuth token 像是把「大门临时密码」锁进保险箱（`~/.hermes/mcp-tokens/<server>.json`），Hermes 要用时自己开箱取，不用你在配置文件里明文贴。这样即便配置被瞄到，也看不到真密码。

> 易错点：如果你**在运行中的会话里**编辑 config.yaml，CLI 会用 30 秒超时自动重载 MCP 连接——这不够完成交互式 OAuth。新增 OAuth 条目后，请从**新终端**跑 `hermes mcp login <server>`，它会等你完整 5 分钟完成授权（来源 S4）。

### 辅助调度 slot：`auxiliary.mcp`

MCP 工具调度本身也会消耗一次 LLM 调用（用于决定/编排调用哪个 MCP 工具），这个辅助任务走 `auxiliary.mcp` slot（来源 S11）。默认 `provider: auto`（跟随主模型）；在意成本/延迟时，可以给它指定一个便宜快速的模型：

```yaml
# ~/.hermes/config.yaml
auxiliary:
  mcp:
    provider: "auto"
    model: ""
    timeout: 30      # 秒
```

和所有 auxiliary slot 一样，`fallback_chain` 也可用（来源 S11）。这个 slot 平时不用管，只有当你观察到 MCP 调度这一步成为性能瓶颈时再调。

## 5.7 实操：MCP 工具不显示的排查序列（5 步）

工具「不显示」的根因通常藏在五个地方，按下面的顺序排查（来源 S9、S4）：

```text
① enabled  →  ② 过滤  →  ③ tools/list RPC  →  ④ 能力缺失  →  ⑤ /reload-mcp
```

**① `enabled: false`？**
先看这台服务器是不是被 `enabled: false` 整个跳过。`enabled: false` 不连接、不发现、不注册，直接没有工具（来源 S4）。如果是，去掉或改 `true`。

**② `tools.include` / `tools.exclude` 过滤？**
检查 `tools.include`、`tools.exclude`、`tools.resources`、`tools.prompts` 是否把目标工具滤掉了。`include` 优先于 `exclude`（来源 S4）。如果你本来就是有意过滤，那「不显示」是预期行为。

**③ 服务器是否响应 `tools/list` RPC？**
确认服务器进程真的活着、能响应 MCP 的 `tools/list` 方法。查 gateway/agent 日志里的 MCP 连接错误；stdio 服务器可以先手动跑一遍验证可执行文件与依赖：

```bash
cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"   # 确认 MCP 依赖在
node --version && npx --version                          # npm 系服务器要 Node
npx -y @modelcontextprotocol/server-filesystem /tmp      # 手动试跑服务器
```

> [!warning]
> 如果 MCP 服务器在请求中崩溃，Hermes 通常会**报超时**——这是「服务器挂了」的常见表象，不是网络慢。此时要去看服务器自己的日志（而不是只盯着 Hermes 日志）来定位根因（来源 S9）。

**④ 能力缺失？**
resource/prompt 工具只在「配置允许」且「服务器会话确实支持」时才注册（来源 S4）。如果某个服务器根本没有 resources 能力，`list_resources` 不出现是正常的。确认你期待的确实是服务器声明的能力。

**⑤ `/reload-mcp` 或重启会话**
改了配置后记得 `/reload-mcp`；还不行就重启 `hermes chat`。这是最后一步，也是「配置没生效」时最常被漏掉的一步（来源 S9）。

`hermes config show | grep -A 12 mcp_servers` 可以快速确认当前生效的 MCP 配置（来源 S9）。跑完 ①-⑤ 还找不到，再回到 ③ 深挖服务器进程。

## 本章小结

- `mcp_servers` 是 MCP 唯一配置入口；stdio（`command`/`args`/`env`）与 HTTP（`url`/`headers`）两种 transport 可共存于同一个 config，`enabled: false` 完全跳过该服务器。
- 启动时自动发现注册；服务器发 `tools/list_changed` 通知时动态刷新免 `/reload-mcp`，改配置后仍可手动 `/reload-mcp`。
- 过滤用 `tools.include`（白名单）与 `tools.exclude`（黑名单），支持 fnmatch glob，`include` 优先；`tools.resources` / `tools.prompts` 关闭 utility 包装，全过滤不建空 toolset。
- 工具命名以双下划线 `mcp__<server>__<tool>` 为准（对齐 Claude Code/Codex），旧文档单下划线随版本核实；写过滤时用原始工具名。
- 信任模型：`trust: untrusted` 下无 `readOnlyHint` 注解的写工具逐次审批，未识别值 fail-closed 按 untrusted 处理；任何不完全控制的服务器都应标 untrusted。
- 排错按 5 步走：enabled → 过滤 → `tools/list` RPC → 能力缺失 → `/reload-mcp`；服务器崩溃的表象是报超时，要看服务器自己的日志。

下一章，我们把工具、技能与记忆三者的关系收束成一张地图，并给出全局禁用与安全基线——届时 `trust` 模型、approvals 审批与 YOLO / hardline 会拼成完整的安全拼图。
