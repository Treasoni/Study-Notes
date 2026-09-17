---
title: "落地（一）——用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）"
tags:
  - AI学习
  - Agent
  - Hermes
  - HomeAssistant
created: 2026-09-18
updated: 2026-09-18
status: 已完成
source_project: hermes-home-assistant
---

> [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/03-路线选型|⬅ 上一章]] · [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/README|📖 返回目录]] · [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/05-落地-官方mcp_server|下一章 ➡]]

# 落地（一）——用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）

第 1 章盘完起点后留下一句话：内置的 4 个 `ha_*` 工具缺三块能力——历史/统计、写配置（自动化）、摄像头。这一章给出一条能一次性补齐三块的路：社区项目 ha-mcp。它值得放在第一条讲，理由不只是"能力强"，而是它的 Setup Wizard 里**已经有一个专门的 Hermes 分支**——给出的 YAML 是按 Hermes 的配置结构写好的，你不需要自己猜键名、试缩进。相对地，第 5 章的官方路线没有 Hermes 示例，那份配置是你拼的。

## 4.1 为什么先讲这条

先把"为什么是它"说清楚，再动手抄配置。

**理由一：它是唯一能一次补齐三类缺口的路。** 历史/统计、写配置、摄像头这三块，内置 4 工具没有对应工具，自建 `SKILL.md` 也表达不了——skill 只能教 agent 怎么调**已有**的命令行工具，HA 场景下并不存在这样一个 `ha` CLI。剩下能补能力的只有 MCP server 与自定义 plugin，而自定义 plugin 的成本明显更高。所以"要能力"这个需求，默认落点就是 MCP server。

**理由二：ha-mcp 与官方路径的能力边界，是官方明文的路线差异，不是营销话术。** ha-mcp 的 README 里有一张与 Home Assistant 自带 MCP Server 集成的对照表：官方那条建在 **Assist** 管道上，实体作用域是 `Only entities exposed to Assist`；ha-mcp 那侧写的是 `Everything in Home Assistant`，覆盖范围含 automations / dashboards / helpers / backups。[^c4-COM01-A]

**理由三：它把 Hermes 当一等公民。** Setup Wizard 的客户端清单里有 `Hermes Agent`（Nous Research），`configFormat` 为 `yaml`，`configLocation` 写作 `~/.hermes/config.yaml`，并单独配了一段 Hermes Notes。更关键的是它明确告诉你改完配置怎么生效：

> Run /reload-mcp in an active session after editing the config — Hermes picks up MCP changes without a restart.

这段是 COM-23（ha-mcp 的一手项目文档）原文。[^c4-COM23-RELOAD]

**一个必须说清的细节：Hermes 出现在 Setup Wizard 里，但没出现在 README 的客户端清单里。** 这两处属于同一个项目，却给出了不一致的印象：Setup Wizard 的客户端数组里有 `Hermes Agent`（`company` 写作 `Nous Research`），而 README 的客户端清单里没有 Hermes 这一项。本册的处置是写"**受支持但 README 未列**"——不写成"官方支持"，也不写成"不支持"。实际含义是：模板是项目维护者主动为 Hermes 写的（所以可信度高于你自行猜测的配置），但它没有被同步进 README 的受支持清单（所以你不能指望每个版本都保持最新）。[^c4-COM23-CLIENT] 这个区别在实操上落成一句话：**抄 Wizard 的模板，但抄完自己验一遍**——4.6 的步骤 4、5 就是干这个的。

> [!tip] 大白话
> 内置的 4 个工具，相当于设备出厂自带的一把螺丝刀——能用，但只能拧一种螺丝。MCP server 是另外买回来的一整套工具箱：装上之后，agent 手边同时有原来的螺丝刀和新箱子里所有工具，两边不互斥、也不互顶。所以"接 MCP"不是"换掉内置能力"，而是"在原有能力上追加"。

**条目名会决定工具名的形态。** Setup Wizard 给的条目名固定是 `home-assistant`。这个连字符在注册时会被替换掉：Hermes 的工具命名函数把组件里所有 `[A-Za-z0-9_]` 以外的字符（**包含连字符**）一律替换成下划线，注册前缀是 `MCP_TOOL_NAME_PREFIX = "mcp__"`。[^c4-SRC04] 于是：

| 层次 | 值 |
|---|---|
| 配置里的条目名 | `home-assistant` |
| 服务端原生工具名 | `ha_get_state` |
| Hermes 里的注册名 | `mcp__home_assistant__ha_get_state` |

这套命名不是 ha-mcp 定的，也不是 Hermes 独创的：源码注释写明 `mcp__<server>__<tool>` 是 Claude Code、Codex、OpenCode 共用的约定，双下划线用于在"服务器名"和"工具名"本身含下划线时仍能划清边界。[^c4-SRC04] 顺带一提，源码里同一段还处理了另一件事：因为 OpenAI 兼容的提供方对函数名有 `^[a-zA-Z0-9_-]{1,64}$` 的长度限制，超过 64 字符的名字会被截断并补一段确定性哈希后缀——所以极长名字下你看到的注册名可能带尾巴，这不是 bug。[^c4-SRC04]

## 4.2 三种 transport 的 YAML

Setup Wizard 的 Hermes 分支给出三种形态：HTTP、`uvx` stdio、Docker stdio。它们的区别只在"这个 server 跑在哪里、Hermes 怎么够到它"，配置键名完全不同。

先看一份完整的成品（选 HTTP 那条，`~/.hermes/config.yaml`；把 URL 换成你自己的）：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    url: "http://192.168.1.10:9584/private_<random>"
    headers:
      Authorization: "Bearer ${env:HA_TOKEN}"
    tools:
      include:
        - "ha_get_state"
        - "ha_get_history*"
        - "ha_call_write_tool"
    trust: untrusted
```

下面三条是 Wizard 生成的**原始形态**，我逐字对照过 HTML 快照。

**HTTP（Streamable HTTP）**

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    url: "{{MCP_SERVER_URL}}"
```

Wizard 里这条只有一个键：`url`。它对应的实际地址，来自 ha-mcp README 里给的两类入口：经反代的 `https://<your-ha-domain>/api/webhook/<webhook-id>`，或同网段直连的 `http://<ha-ip>:9584/private_<random>`。[^c4-COM01-B] 注意 README 同一段还写了不加 `/readonly` 的原样形态，见 4.4。

这条是**最省事也最该先试**的一条：不需要本地装 Docker 或 `uvx`，server 跑在 HA 那一侧；Hermes 只负责发 HTTP 请求。

**`uvx` stdio**

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    command: "uvx"
    args:
      - "ha-mcp@latest"
    env:
      HOMEASSISTANT_URL: "{{HOMEASSISTANT_URL}}"
      HOMEASSISTANT_TOKEN: "{{HOMEASSISTANT_TOKEN}}"
```

差别有两处值得点出。第一，`url` 键换成了 `command` + `args`：Hermes 会在本机起一个子进程，通过标准输入输出跟它说话。第二，凭据从 HTTP 那条的 `headers` 挪到了 `env` 块——因为 stdio 形态下这个进程就在你本机跑，直接给它环境变量即可。

**Docker stdio**

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    command: "docker"
    args:
      - "run"
      - "--rm"
      - "-i"
      - "-v"
      - "ha-mcp-data:/home/mcpuser/.ha-mcp"
      - "-e"
      - "HOMEASSISTANT_URL={{HOMEASSISTANT_URL}}"
      - "-e"
      - "HOMEASSISTANT_TOKEN={{HOMEASSISTANT_TOKEN}}"
      - "ghcr.io/homeassistant-ai/ha-mcp:latest"
```

这是 `uvx` 那条的容器化版本。Wizard 源码里对 `--rm` 配了段注释，解释为什么要挂 volume：`--rm` 会在**每次客户端会话结束后丢掉容器**，所以 `ha-mcp-data` 这个卷是唯一能让工具配置和功能开关活过重启的东西（注释指向 issue #2078）。[^c4-COM23-DOCKER]

三种形态的适用场景，可以压成一张表：

| 形态 | server 跑在哪 | 本机依赖 | 适合什么情况 |
|---|---|---|---|
| HTTP | HA 侧（组件 / 应用 / 反代） | 无 | 首选；已有反代或 Nabu Casa；想让多个客户端共用一份 |
| `uvx` stdio | 本机子进程 | 需要 `uvx` | 临时试用、本机快速验证 |
| Docker stdio | 本机容器 | 需要 Docker | 已习惯容器化、想锁死版本与隔离环境 |

**别把两个层次的选择混在一起。** 这里其实有两组独立的决定。第一组是"ha-mcp 这个 server 跑在哪里"——README 列举了自定义组件、HA 应用、Docker/PyPI、本地 stdio 四种装法。[^c4-COM01-INSTALL] 第二组才是"Hermes 怎么连上它"——也就是本节这三条 transport。两者的关系是：**前一组选定后，Hermes 那一侧只看一个入口（一个 URL，或一条 stdio 命令）**，所以 Hermes 的 YAML 会因前一组的选择而不同，而这三条模板恰好覆盖了最常见的三种组合。这也是 4.5 那条"只留一条条目"警告的根源——如果你在 HA 侧装了组件、又留着一个 `uvx` 条目，就等于同一个 server 在客户端里有两条路径。

> [!tip] 大白话
> transport 就是"送货方式"。HTTP 像外卖：你下单，餐在店里做好，送到你手上，你不占自家厨房。stdio 像自提食材回家做：Hermes 在你本机起一个小进程，通过"嘴对嘴"（标准输入输出）跟它说话，好处是不用开端口，代价是本机得装依赖。Docker stdio 则是"自提"但食材连锅一起打包好——环境隔离更干净，代价是多一层容器。

**一个必须提醒的反向证据。** 上面三种里，stdio 那两条（`uvx` 与 Docker）在 README 里被明确标注了传输层问题：

> ⚠️ **stdio has known transport issues.** The stdio transport has connection problems that streamable HTTP does not ([#1713](https://github.com/home-assistant-ai/ha-mcp/issues/1713)). It is recommended only for demo/testing tinkering — for a real setup, use the custom component or an HTTP method above.

这是 COM-01（ha-mcp README）原文。[^c4-COM01-C] 结论很直接：如果你是要长期用的正式环境，**优先选 HTTP 那条**；stdio 两条只适合临时验证。

## 4.3 鉴权两种写法

Wizard 对 HTTP 形态额外给了一段 "Alternative: With Authentication Headers"，原样如下：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    url: "{{MCP_SERVER_URL}}"
    headers:
      Authorization: "Bearer ${env:HA_TOKEN}"
```

配套的说明原文是：

> Hermes resolves `${env:VAR}` (and `${VAR}`) from `~/.hermes/.env`, so the token stays out of the config file. For an endpoint that speaks OAuth instead, drop the headers and set `auth: oauth` on the entry.

[^c4-COM23-AUTH]

这段话里有两个独立的事实，都值得单独记住：

**第一，两种引用语法等价。** `${env:VAR}` 是 Cursor 风格的 SecretRef 写法，`${VAR}` 是朴素写法，二者解析到同一个变量——Hermes 自己的 MCP 配置参考文档也是这么写的，并且说明这样做的目的是"从 Cursor / Claude 配置里抄过来的 MCP 片段可以原样使用"。[^c4-HMS04-ENV] 该文档还补了两条边界：值的解析顺序是"当前 profile 的 secret 作用域，回退到进程环境"；**未设置的变量会保留字面占位符**，不会变成空字符串——所以如果你看到 header 里原样躺着 `${env:HA_TOKEN}` 这几个字符，那不是编码问题，是这个变量在 `~/.hermes/.env` 里根本不存在。[^c4-HMS04-ENV]

**第二，OAuth 是另一条路，不是叠加项。** 原文说的是 "drop the headers and set `auth: oauth`"——把 headers 去掉，换成 `auth: oauth`。Hermes 侧的 `auth` 键定义是"设为 `oauth` 时启用带 PKCE 的 OAuth 2.1"。[^c4-HMS04-AUTH]

| 写法 | 凭据放哪 | 适用 | 代价 |
|---|---|---|---|
| `headers: Authorization: "Bearer ${env:HA_TOKEN}"` | `~/.hermes/.env` 里的 HA 长期令牌 | 端点用 Bearer token 保护 | 令牌长期有效，需自己管控 |
| `auth: oauth` | Hermes 的 OAuth 令牌缓存 | 端点实现 OAuth | 需走一次授权流程；headless 环境下浏览器打不开时不会自动续期 |

关于 OAuth 在无人值守环境下的行为，Hermes 的 MCP 功能文档另有一条明确警告：gateway、`/reload-mcp`、以及驻留服务器的周期性自检**都不会打开浏览器**（没有人在场完成流程），当 refresh token 失效时服务器会带着警告停驻在 `gateway.log` 里，需要你用 `hermes mcp login <server>` 重新授权一次。[^c4-HMS11-OAUTH] 如果你的 Hermes 以定时任务为主，这条要提前想清楚——用 Bearer 写法就没有这个失效面。

> [!tip] 大白话
> `${env:HA_TOKEN}` 这个写法，相当于配置文件里不写钥匙本身，只写一句"去门口保险箱拿 3 号那把"。真正那把钥匙放在 `~/.hermes/.env` 里。好处是你把这个 config.yaml 发给别人、或者提交到 Git 时，泄露的只是一张"取钥匙的纸条"，不是钥匙。而 `auth: oauth` 完全是另一套逻辑：不是放一把固定的钥匙，而是当场办一张有时效的门禁卡。

## 4.4 传输与只读端点

**传输必须是 Streamable HTTP**

Wizard 对 HTTP 形态的提醒原文：

> Leave the transport at its default. Hermes can switch a server to SSE, but the ha-mcp endpoint is Streamable HTTP only — it is POST-only and answers an SSE-style pre-flight with 405.

[^c4-COM23-SSE]

拆开看：ha-mcp 的端点是**只支持 Streamable HTTP**，而且**只接受 POST**；如果客户端按 SSE 的方式先发一个预检（pre-flight）请求，会拿到 **405** 而失败。

Hermes 侧确实存在切到 SSE 的开关——配置参考里 `transport` 键的说明就是"设为 `sse` 以使用 SSE 传输而非 Streamable HTTP"。[^c4-HMS04-TRANSPORT] 也就是说，这条路是**你在 Hermes 侧主动打开才会走上去**的：保持默认即可，别去设 `transport: sse`。

还有一条相邻的坑值得提前记下，因为它长得跟"连接失败"很像。Hermes 的 HTTP 客户端在连接前会做一次**快速的内容类型探测**（fail-fast content-type probe），如果某个端点对 HEAD / GET 请求返回的不是 MCP 的内容类型，这次探测就会把它判死。配置参考里为此留了一个旁路开关 `skip_preflight`：默认 `false`，设为 `true` 时跳过这次探测，用于"确实是合法的 Streamable HTTP 端点、但 HEAD / GET 答的不是 MCP 内容类型"的情况。[^c4-HMS04-SKIP] 注意适用边界很窄——它是给**合法的**端点绕开误判用的，不是给配错的 URL 硬撑用的。如果你连的是 ha-mcp 且 URL 正确，通常用不上它；但当你换到第 5 章的官方端点、或前面挂了一层反代时，先想起这个键，比反复怀疑网络要省时间。

**只读端点：`/readonly` 是连接级，不是凭证级**

如果只是想让 agent 看，不想让它写，README 给的做法是给 HTTP MCP 端点加 `/readonly` 后缀：

```text
Normal:     https://example.com/private_your_secret
Read-only:  https://example.com/private_your_secret/readonly
```

在 Hermes 里就是：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant-ro:
    url: "http://192.168.1.10:9584/private_<random>/readonly"
```

关于它的效果，README 有一段措辞必须原样引，因为它直接决定了你对这个功能的预期：

> Read-only connections hide write tools and block write calls, including calls through cached tools or search proxies. The global Read Only Mode setting still restricts both endpoints when enabled. Reconnect the client after changing its URL so it refreshes its tool list.
>
> This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint.

[^c4-COM01-RD]

最后那句是本节的要点：**这是"连接模式"，不是"凭证权限"**。同一个 token，指向 `/readonly` 端点时写操作被挡；指向正常端点时照样能写。所以它防的是"这条连接上的 agent 手滑"，**不防"拿到这把 token 的人换个 URL"**。如果你的安全模型要求"这把令牌物理上就写不了"，`/readonly` 满足不了，得回到第 7 章讲的凭据与用户侧收紧。

另外两处细节也值得记住：切 URL 后要**重连客户端**，否则客户端还在用缓存的工具列表；以及 Read Only Mode 若在服务端被全局打开，两个端点都会被限制。[^c4-COM01-RD]

> [!tip] 大白话
> `/readonly` 像给这条通道装了一道只能出不能进的旋转门——但这个"只能出不能进"是门的属性，不是钥匙的属性。你手里还是原来那把钥匙，走到旁边的普通门，照样能进。所以别把它当成"发了一把只读钥匙"，它只是"给这条接线换了一根只读的线"。

## 4.5 工具集裁剪与排错

**用 `tools.include` 裁剪，写原生名**

ha-mcp 暴露的工具很多，全量注入会挤占上下文。Wizard 给的做法是：

> Trimming the catalog: `tools.include` / `tools.exclude` on the server entry take exact tool names or globs. Use the original ha-mcp names (e.g. `ha_get_state`), not the prefixed ones.

[^c4-COM23-TRIM]

要点是最后半句：**写服务端原生名**（`ha_get_state`），**不是**写注册后的 `mcp__home_assistant__ha_get_state`。这条与 Hermes 自己的配置参考一致——那里对 `tools` 策略的说明是：`include` / `exclude` 接受"服务端原生 MCP 工具名"，条目可以是精确名，也可以是 fnmatch 风格的 glob（如 `*_radar_*`、`get_zones_*`）。[^c4-HMS04-TOOLS]

两条语义规则来自 Hermes 的配置参考，逐条列清：

| 规则 | 行为 |
|---|---|
| 只设 `include` | 只注册白名单里的原生工具 |
| 只设 `exclude` | 注册除黑名单外的全部原生工具 |
| 两个都设 | **`include` 优先**；同时出现在 `exclude` 里的名字被忽略 |

[^c4-HMS04-TOOLS]

所以推荐做法是**白名单**而不是黑名单：白名单默认拒绝、你要的才进；黑名单默认全开、你忘掉一个就漏一个。这个取向与第 7 章的最小化清单是同一条原则。

glob 的用处是把一整族工具一次收进来，而不用逐个点名——配置参考给的例子形态是 `*_radar_*`、`get_zones_*` 这类模式。[^c4-HMS04-TOOLS] 落到 ha-mcp 上，最常见的用法是历史类：与其把每个历史查询工具都列一遍，不如写 `ha_get_history*` 一次覆盖。代价是 glob 会随上游改名而"静默变宽或变窄"——上游把工具拆成两个，你的白名单就自动多收一个。**要确定性就逐个点名，要省事就用 glob，但每升一次 ha-mcp 版本重看一眼名单。**

**工具数不给单值**

ha-mcp 到底有多少工具？**这个问题没有单一答案，因为同一个 README 里有三个互不一致的数字**：

| 位置 | 数字 |
|---|---|
| 徽章 `tools-87-blue`，但 `alt` 文字写的是 | `95+ Tools` |
| 正文 "Complete Tool List (… tools)" | `87` |
| 正文 "the full tool catalog (… tools)" 与另一处 "instead of …" | `~84` / `84` |

三处均取自 COM-01 同一份 README。[^c4-COM01-COUNT] 本册不给单值——写"约 84–95，口径不一，以你 `hermes mcp test` 的实际探测结果为准"是唯一稳妥的说法。

**顺带埋一个点，第 9 章展开。** 工具集不是免费的：这些工具的 schema 会作为常驻开销进入上下文。社区有用户报告过 ha-mcp 的工具集占用**超过 60k tokens**——需要说明的是，这个帖子里 `60,3k` 与 `1,8k–3,4k` 两个更精确的数字，唯一出处是**帖内 Claude 的自述**（该段开头即 `Claude sagt dazu:`），**不是 tokenizer 计数**；楼主本人原话只有「über 60k Tokens」，且**无第三方复现**。[^c4-COM16] 所以正文只写"社区用户报告"，不写"实测"。这个量级意味着：一个不能延迟加载工具列表的客户端，光是把工具摆在那儿就要付这笔钱——第 9 章讲怎么算、怎么省。

**排错三则**

**第一则：同一个 server，不要在一个客户端里留两条条目。** README 有一条加粗警告，并且点了具体的翻车组合：

> ⚠️ **Configure exactly one install method per client.** The custom component, the app, Docker/PyPI, and local stdio are independent ways to run the same server — pick one and point your AI client at that single URL. Keeping two entries for the same server in one client (for example a local `uvx ha-mcp@latest` entry with `HOMEASSISTANT_URL` / `HOMEASSISTANT_TOKEN` alongside an app or component URL) is a known cause of connection hangs.

[^c4-COM01-DUP]

"known cause of connection hangs"——这是已知的连接挂起原因。翻译成操作纪律：4.2 的三条里，**只留一条**；从 `uvx` 换成 HTTP 时，把旧的那条删掉，而不是注释掉留着。

**第二则：`hermes mcp test` 只给原生名，别拿它验证前缀。** Hermes 的 `hermes mcp test <name>` 用来测试与 MCP server 的连接、并列出它发现的工具（`hermes mcp add` / `test` / `login` / `configure` 这组子命令见 CLI 文档）。[^c4-HMS07] 但看源码就知道它打印的是什么：探测函数遍历服务端返回的工具对象，取的是 `t.name` 原样入列表——也就是**服务端原生名**，注册前缀是在之后注册环节才加的。[^c4-SRC07]

这一点很实用：如果你用 `hermes mcp test` 看到工具叫 `ha_get_state`，而会话里 agent 报的是 `mcp__home_assistant__ha_get_state`，**两边不一致是正常的**，不是配置错了。想核验前缀，要看会话里的实际注册名，而不是 `mcp test` 的输出。

**第三则：改完配置用 `/reload-mcp`，不用重启。** Wizard 的 clientNote 已经写明了。[^c4-COM23-RELOAD] Hermes 侧的功能文档把这条讲得更细：`/reload-mcp` 会从配置重新加载 MCP server 并刷新工具列表，**它同时也是重新探测"可用性门控"工具的唯一显式方式**——一个会话的工具集是"冻结"的，所以在会话中途才出现的凭据或守护进程，只有在 `/reload-mcp`、`/new` 或上下文压缩时才会被拾取到。[^c4-HMS11-RELOAD]

还有一个容易忽略的例外：如果 Hermes 以**消息网关**形态在跑（`hermes gateway run`），它会自己盯着 `config.yaml`——你删掉一个 `mcp_servers` 条目或设 `enabled: false` 后大约一分钟内，那条连接会被拆掉；新加的条目会被连上。这种情况下**不需要**重启也不需要 `/reload-mcp`。[^c4-HMS11-RELOAD]

> [!tip] 大白话
> `tools.include` 白名单像出门只带三把钥匙：兜里清楚，丢不了。`tools.exclude` 黑名单像"除了这三把我全带上"——你今天记着锁了，明天忘了加一把，就多带了一把不该带的。工具集越大，越该用白名单。而 `hermes mcp test` 打印原生名这件事，好比快递单上写的是寄件人仓库里的编号，不是到你家门口后贴的门牌号——两个都对，只是编号体系不同。

## 4.6 落点配置

把本章内容收成一份可直接抄的成品。**只留一条条目**，选 HTTP 形态。

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant:
    url: "http://192.168.1.10:9584/private_<random>"
    headers:
      Authorization: "Bearer ${env:HA_TOKEN}"
    tools:
      include:
        - "ha_get_state"
        - "ha_get_history*"
        - "ha_get_overview"
        - "ha_call_write_tool"
    trust: untrusted
```

配套的 `~/.hermes/.env`：

```bash
# ~/.hermes/.env
HA_TOKEN=eyJhbGciOi...     # 你在 HA「用户资料 > 安全」里创建的长期令牌
```

只想要只读时，把 `url` 换成带后缀的那条，并把条目名一并改掉，与可写条目区分开：

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  home-assistant-ro:
    url: "http://192.168.1.10:9584/private_<random>/readonly"
    headers:
      Authorization: "Bearer ${env:HA_TOKEN}"
    tools:
      include:
        - "ha_get_state"
        - "ha_get_history*"
```

注意第二次强调：这条只读条目用的还是**同一个** `HA_TOKEN`，`/readonly` 挡的是这条连接，不是这把令牌。

**落地步骤：**

1. 在 HA 侧确认 ha-mcp 已就位，拿到你的连接 URL（反代的 webhook 形态，或同网段直连的 `http://<ha-ip>:9584/private_<random>`）。[^c4-COM01-B]
2. 在 HA 的「用户资料 > 安全」里创建长期令牌，写入 `~/.hermes/.env` 的 `HA_TOKEN`。
3. 按上面的 YAML 写入 `~/.hermes/config.yaml`。**确认这个 server 名下只有一条条目**。[^c4-COM01-DUP]
4. 跑 `hermes mcp test home-assistant` 验证连通性；看到的工具名是原生名，这是预期行为。[^c4-SRC07]
5. 在会话里执行 `/reload-mcp`，让会话刷新工具列表。[^c4-COM23-RELOAD]
6. 让 agent 列出它现在能看到的 `mcp__home_assistant__*` 工具，确认注册名形态正确。
7. 之后每次增删工具或改 URL，重复第 4–5 步。

**落地自检清单：**

- [ ] 传输保持默认（Streamable HTTP），没有设 `transport: sse`
- [ ] 同一个 server 在客户端里只有一条条目
- [ ] 令牌写在 `~/.hermes/.env`，配置文件里只有 `${env:HA_TOKEN}` 这样的引用
- [ ] `tools.include` 用的是原生名（`ha_get_state`），不是注册名
- [ ] 走 `trust: untrusted`，写操作会过审批面
- [ ] 改完配置执行过 `/reload-mcp`

> [!summary] 本章小结
> - ha-mcp 是唯一能一次补齐"历史/统计、写配置、摄像头"三类缺口的路；Setup Wizard 已含 Hermes 专属分支，YAML 可照抄。
> - 三种 transport（HTTP / `uvx` stdio / Docker stdio）是同一个 server 的三种跑法，**只能留一条**；正式环境优先 HTTP，stdio 官方自陈有已知传输问题。
> - 鉴权两种写法二选一：`headers` 里的 `Bearer ${env:HA_TOKEN}`（变量从 `~/.hermes/.env` 解析，`${env:VAR}` 与 `${VAR}` 等价），或 `auth: oauth`（无人值守环境下 refresh token 失效需手动 `hermes mcp login`）。
> - 传输必须 Streamable HTTP（POST-only）；按 SSE 发预检会吃到 **405**。
> - `/readonly` 是**连接级**模式而非凭证级权限——同一凭证在正常端点仍可写。
> - 条目名 `home-assistant` → 注册名 `mcp__home_assistant__<tool>`（连字符会被 sanitize 成下划线）；`tools.include` 用原生名。
> - 工具数不给单值（README 内 87 / 95+ / ~84 三处不一致）；工具集的 schema 常驻开销是真金白银，第 9 章展开。

## 下一章预告

下一章换到另一条 MCP 子路线：Home Assistant 官方的 `mcp_server` 集成。它的能力比 ha-mcp 窄——实体作用域只有"已暴露给 Assist 的那些"，也没有写配置、历史、摄像头——但它最大的不同是：**官方页面给了 6 个第三方客户端示例，里面没有 Hermes**。所以第 5 章那份配置是拼出来的，会整份标注"拼接·未验证"，并且要在 2026.9 与 2026.10 两个 HA 版本之间分清一个行为相反的点。

---
## 本章来源

本章采用**脚注体**引用：正文里的上标与该章的脚注定义一一对应，下附脚注定义块即本章来源清单，每条开头标注 canonical ID（`HAS-*` / `HMS-*` / `SRC-*` / `COM-*`）。其余各章为来源表体，两处内容等价。


[^c4-COM01-A]: COM-01（https://github.com/homeassistant-ai/ha-mcp，README），对照表一行：官方 MCP Server 集成 `Only entities exposed to Assist` vs ha-mcp `Everything in Home Assistant`。本册同时在 D-9 标记为"官方明文的路线差异"。

[^c4-COM01-B]: COM-01 README：`https://<your-ha-domain>/api/webhook/<webhook-id>`（经反代 / Nabu Casa）与 `http://<ha-ip>:9584/private_<random>`（同网段直连）。

[^c4-COM01-INSTALL]: COM-01 README 原文：`The custom component, the app, Docker/PyPI, and local stdio are independent ways to run the same server`。

[^c4-COM01-C]: COM-01 README 原文，`stdio has known transport issues`，指向 issue #1713。

[^c4-COM01-COUNT]: COM-01 README 三处：徽章 `tools-87-blue`（`alt` 为 `95+ Tools`）、`Complete Tool List (87 tools)`、正文 `the full tool catalog (~84 tools)` 与 `instead of 84`。

[^c4-COM01-DUP]: COM-01 README 原文，`Configure exactly one install method per client` 段，`known cause of connection hangs`。

[^c4-COM01-RD]: COM-01 README `### Read-only HTTP connections` 段原文，含 `This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint.` 与示例 URL。

[^c4-COM16]: COM-16（https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707，德语社区帖）。据 `02_deep_research.md` §5.7：`60,3k` 与 `1,8k–3,4k` 的唯一出处是帖内 Claude 自述（段落开头 `Claude sagt dazu:`），非 tokenizer 计数；楼主原话为「über 60k Tokens」；无第三方复现。**本章按降格后的措辞写，不得引作实测。**

[^c4-COM23-CLIENT]: COM-23 Setup Wizard 客户端数组含 `{"id":"hermes","name":"Hermes Agent","company":"Nous Research","transports":["stdio","sse","streamable-http"],"configFormat":"yaml","configLocation":"~/.hermes/config.yaml"}`；COM-01 README 的客户端清单中不含 Hermes。本册按"受支持但 README 未列"表述。

[^c4-COM23-AUTH]: COM-23（https://homeassistant-ai.github.io/ha-mcp/setup/），Setup Wizard 的 Hermes 分支 "Alternative: With Authentication Headers" 段原文，逐字对照 HTML 快照 `sources/COM-ha-mcp-setup-wizard.html`。

[^c4-COM23-DOCKER]: COM-23 Setup Wizard 源码内注释：`--rm` discards the container after every client session, so the `ha-mcp-data` volume is the only thing keeping tool config and feature flags across restarts (issue #2078)。

[^c4-COM23-RELOAD]: COM-23 Setup Wizard 的 Hermes clientNote 原文。

[^c4-COM23-SSE]: COM-23 Setup Wizard 原文，`Leave the transport at its default…` 段，含 `405`。

[^c4-COM23-TRIM]: COM-23 Setup Wizard 的 "Hermes Notes" → "Trimming the catalog" 原文。

[^c4-HMS04-AUTH]: HMS-04（Hermes `website/docs/reference/mcp-config-reference.md`），`auth` 键：`Set to oauth to enable OAuth 2.1 with PKCE`。

[^c4-HMS04-ENV]: HMS-04 `## Environment variable references`：`${VAR}` 与 `${env:VAR}` 解析到同一变量；值来自当前 profile 的 secret 作用域（回退进程环境）；未设置的变量保留字面占位符。

[^c4-HMS04-SKIP]: HMS-04 `skip_preflight` 键：`Bypass the fail-fast content-type probe for valid Streamable HTTP endpoints whose HEAD/GET answers a non-MCP content type (default: false)`。

[^c4-HMS04-TOOLS]: HMS-04 `## tools policy keys` 与 `## Filtering semantics`：`include` / `exclude` 用服务端原生工具名，支持 fnmatch glob；两者都设时 `include` 优先。

[^c4-HMS04-TRANSPORT]: HMS-04 `transport` 键：`Set to sse to use the SSE transport instead of Streamable HTTP`。

[^c4-HMS07]: HMS-07（Hermes `website/docs/reference/cli-commands.md`）`hermes mcp` 子命令表：`add` / `remove` / `list` / `test` / `configure` / `login` / `install` / `catalog` / `serve`。

[^c4-HMS11-OAUTH]: HMS-11（Hermes `website/docs/user-guide/features/mcp.md`）：gateway、`/reload-mcp` 与驻留服务器的周期性自检不会打开浏览器；refresh token 失效时服务器停驻并记录警告，需 `hermes mcp login <server>` 重新授权。

[^c4-HMS11-RELOAD]: HMS-11：`/reload-mcp` 从配置重载 MCP server 并刷新工具列表，也是重新探测可用性门控工具的显式方式；会话工具集默认冻结。同页另述 `hermes gateway run` 会自动监视 `config.yaml`，约一分钟内生效，无需重启或 `/reload-mcp`。

[^c4-SRC04]: SRC-04（Hermes `tools/mcp_tool_schema.py`）：`MCP_TOOL_NAME_PREFIX = "mcp__"`；`sanitize_mcp_name_component` 把 `[A-Za-z0-9_]` 以外的字符（含连字符）替换为 `_`；`_MCP_TOOL_NAME_MAX_LENGTH = 64`，超长时截断并补确定性哈希后缀（#81331）；注释说明 `mcp__<server>__<tool>` 为 Claude Code / Codex / OpenCode 共用约定（#33533）。

[^c4-SRC07]: SRC-07（Hermes `hermes_cli/mcp_config.py`）：`_probe_single_server()` 以 `tools_found.append((t.name, desc))` 收集 **服务端原生** 工具名，`_print_tools()` 原样打印；注册前缀在注册环节才加。
