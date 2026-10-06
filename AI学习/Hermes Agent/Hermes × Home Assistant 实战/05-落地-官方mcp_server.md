---
title: "落地（二）——用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）"
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

> [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/04-落地-社区ha-mcp|⬅ 上一章]] · [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/README|📖 返回目录]] · [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/06-事件驱动与定时任务|下一章 ➡]]

# 落地（二）——用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）

上一章走的是社区项目 ha-mcp。这一章换到另一条子路线：Home Assistant **自带**的 MCP Server 集成（`mcp_server`）。它的来源更权威、维护方就是 HA 官方，能力却明显更窄。而本章有一个必须先摆在最前面的前提：**官方页面给了 6 个第三方客户端的配置示例，里面没有 Hermes**。这意味着本章给出的 `mcp_servers` 条目不是官方口径，而是本册按官方端点规格拼出来的——**整份标"拼接，未经官方或实机验证"**，请按这个性质使用。

## 5.1 端点与「无官方 Hermes 示例」的事实

先确认这条路线在协议层的形态。官方文档写它实现的是 Streamable HTTP：

> The Home Assistant Model Context Protocol Server integration implements the [Streamable HTTP protocol] allowing client-to-server communication using the stateless protocol.

[^c5-HAS01-PROTO]

端点的定义在同一页：

> The Home Assistant MCP server is exposed as `/api/mcp` and requires the client to provide an authentication token.

[^c5-HAS01-EP]

如果你有多个 LLM API 可用，可以把 API 的 ID 加到路径上，从 `/api/mcp` 变成 `/api/mcp/<api_id>`。这里有一个例外必须记牢——**Assist API 是恒定可用的**：

> For example, the built-in Assist API is always available at `/api/mcp/assist`.

[^c5-HAS01-EP] 拼 Hermes 配置时，最省事的就是直接用 `/api/mcp/assist`：它不需要额外的 API ID，也不会因为你在 HA 侧改了 API 选择而失效。

**然后是本章的关键事实。** 官方在同一页给了 6 个客户端示例，我把小标题逐个列出来：

| 序号 | 官方示例（`### Example:` 小标题） |
|---|---|
| 1 | Claude for Desktop |
| 2 | ChatGPT |
| 3 | Claude Code |
| 4 | Codex |
| 5 | Cursor |
| 6 | Antigravity CLI |

六个全部取自 HAS-01 的 `## Client configuration` 一节。[^c5-HAS01-EXAMPLES] **这 6 个里面没有 Hermes。** 官方也没有在别处给过 Hermes 的接法。

这个事实决定了本章的写法，得说清它到底意味着什么、又不意味着什么。

**不意味着 Hermes 不能接。** 这一页没有任何"仅限以上客户端"的措辞；反过来说，它明确写了自己是标准 MCP + Streamable HTTP，而 Hermes 也是标准 MCP 客户端。协议对得上，就能接。

**意味着的是：没有一方替你把这条路验过。** ha-mcp 那边有维护者写的 Hermes 模板（第 4 章）；这里两边都没有——官方没写 Hermes，Hermes 的 MCP 文档也没写 HA 官方集成。所以本章 YAML 的每一个键都要你自己在实机上确认一遍，尤其是鉴权部分。

> [!tip] 大白话
> 官方这 6 个示例，像同一款车型的接线图——照着接，厂家给你保证。Hermes 是另一款车：接口标准同样是那个标准，理论上能接，但厂家没出过这款车型的图。你现在手上这张（本章给的），是懂电路的人照着接口规格画的草图。能通电的概率很高，但第一次点火前最好先拿万用表量一遍。**这就是"拼接·未验证"四个字的实际含义。**

## 5.2 鉴权：LLT bearer 优先

官方把鉴权分成了两小节：`#### OAuth` 和 `#### Long-lived access tokens`。对 Hermes 来说，选哪条其实有官方给的一句话作依据——它就写在 long-lived token 那一节的开头：

> Some MCP clients may not support OAuth, but may support access tokens. You may create a [Long-lived access token] to allow the client to access the API.

[^c5-HAS01-LLT]

这句话的意思是：**OAuth 走不通的客户端，官方给了 LLT 这条路作为出路**。对本章的"配置形状未知"这个处境来说，LLT 是变量最少的一条——它只需要一个 HTTP 请求头，不需要回调地址、不需要客户端注册、不依赖浏览器。

官方给的 LLT 创建步骤是三步：

1. 进入「用户资料 > 安全」标签页。
2. 在「长期访问令牌」下选「创建令牌」。
3. 复制令牌，配置 MCP 客户端时使用。

[^c5-HAS01-LLT]

把这三步的产物接到 Hermes 上，就是下面这段——**注意这一整段是拼接，不是官方示例**：

```yaml
# ~/.hermes/config.yaml
# ⚠️ 拼接·未验证：HA 官方 mcp_server 文档未提供 Hermes 示例，本段由本册按官方端点规格拼出。
mcp_servers:
  ha-official:
    url: "http://192.168.1.10:8123/api/mcp/assist"
    headers:
      Authorization: "Bearer ${env:HA_LLT_TOKEN}"
    tools:
      include:
        - "HassTurnOn"
        - "GetLiveContext"
```

对应的环境变量仍按第 4 章的做法放进 `~/.hermes/.env`：

```bash
# ~/.hermes/.env
HA_LLT_TOKEN=eyJhbGciOi...     # HA「用户资料 > 安全」里创建的长期访问令牌
```

三个必须自己验的点：

**第一，URL 的形态。** 示例里写的是 `http://<你的HA>:8123/api/mcp/assist`。官方文档里给 Claude for Desktop 的 URL 是 `https://<your_home_assistant_external_url>/api/mcp`，给 Codex 的是 `http://<your_local_home_assistant_ip_or_url>:8123/api/mcp`。[^c5-HAS01-EXAMPLES] 我把它替换成了 Assist 专属端点并加了端口——**这一步替换本身没有官方示例佐证**，是依据 5.1 那条 `/api/mcp/assist` 恒可用的说明推的。

**第二，工具名。** 上面的 `HassTurnOn` / `GetLiveContext` 是示例值，**不是你系统里真实的工具名**。官方这一页对工具的说明只有一句："The tools used by the configured LLM API are exposed."——暴露的是**你所配置的那个 LLM API 的工具集**。[^c5-HAS01-TOOLS] 换句话说，工具清单取决于你在 HA 侧选的是哪一个 API、以及 Assist 暴露了哪些实体，不是一张固定的表。要拿到真实清单，用 `hermes mcp test ha-official` 探测（它给的是原生名，见第 4 章），或直接问会话里的 agent。

**第三，admin 要求带版本号。** 同一页写着：

> Connecting to any API other than Assist requires the authenticated user to be an administrator. The Assist API stays available to non-administrator users, just like the base `/api/mcp` endpoint.

[^c5-HAS01-EP] 这是 **2026.9 的文档口径**（对应的源码分支判定见 5.5）：Assist 之外要管理员身份，Assist 本身非管理员也能用。所以如果你按 5.2 的方案走 `/api/mcp/assist`，理论上可以配一个**非管理员**的受限用户来发 LLT——这正好接上第 7 章的最小化清单。但"理论上"三个字很关键，因为 5.5 会说明同一端点在 2026.10 的行为是相反的。

> [!tip] 大白话
> OAuth 像办门禁卡：要填表、要指认"卡寄回哪个地址"、地址对不上就拒。LLT 像直接配一把钥匙：不填表、不认地址，插上就能用。省事的代价是这把钥匙**有效期极长且不会自己换**——所以"先用 LLT"不是因为 LLT 更安全，恰恰是因为它更简单、变量更少，而本章的配置形状本来就没被任何一方验证过，变量越少越容易定位问题。

## 5.3 OAuth / IndieAuth 的约束与未验证项

如果 LLT 那条路你不满意（比如不想放一个十年有效的固定令牌），官方这条路也支持 OAuth。但它的约束比一般 OAuth 严得多，且**Hermes 侧能不能满足这些约束，本册未能验证**。

官方的 OAuth 走 IndieAuth，明说不需要预先注册 OAuth Client ID，"Client ID 就是发起请求的客户端应用的 base URL"。紧接着是对 Client ID 的硬约束：

> **Client ID**: The base URL of the LLM client application configuring the connector (for example, `https://claude.ai` for Claude, or `https://chatgpt.com` for ChatGPT). It must never be your Home Assistant instance URL. Home Assistant's IndieAuth implementation validates that the OAuth `redirect_uri` shares the same scheme and domain with the `client_id`. If you enter your Home Assistant instance URL as the Client ID, authentication fails because the client application's redirect URI does not match.

[^c5-HAS01-INDIE]

把这段拆成三条硬规则：

| 规则 | 原文依据 | 对 Hermes 的含义 |
|---|---|---|
| `client_id` 必须是**客户端应用的 base URL** | "the base URL of the LLM client application" | 要填 Hermes 自己的 URL，不是 HA 的 |
| `client_id` **绝不能**是 HA 实例 URL | "It must never be your Home Assistant instance URL" | 填成 HA 地址必然失败 |
| `redirect_uri` 必须与 `client_id` **同 scheme 同域** | "shares the same scheme and domain" | Hermes 的回调地址必须落在自己的域名下 |

再补两条同页的细节。**Client Secret 不被使用**：官方写 "This is not used by Home Assistant. If the field is required by the client application, enter any text; if it is optional, leave it blank."[^c5-HAS01-INDIE] **并且它不支持传统的动态客户端注册**：HA 实现的是 OAuth Client ID Metadata Document 规范（`client_id_metadata_document_supported: true`），而不是 RFC 7591 Dynamic Client Registration，**且不提供 RFC 7591 的 `registration_endpoint`**；严格依赖 RFC 7591 的客户端无法自动注册。[^c5-HAS01-DCR]

官方给的 Codex 示例，能让你看清这类本地客户端的典型形状：

```toml
# 官方 Codex 示例（HAS-01）
oauth = { client_id = "http://127.0.0.1:12345" }
```

并配了一句说明：

> The callback port and the port in `client_id` must match. The `client_id` value is the base URL of the local OAuth callback used by Codex; do not replace it with your Home Assistant URL.

[^c5-HAS01-CODEX]

**未验证项就落在这里：Hermes 侧是否有等价的本地回调机制？** 本册的素材里没有任何一份文档或源码能回答这个问题——Hermes 的 MCP 配置参考只说明了 `auth: oauth` 这个开关会"启用带 PKCE 的 OAuth 2.1"。[^c5-HMS04-AUTH] 至于它用什么 URL 作为 `client_id`、回调落在哪个端口、能否与 IndieAuth 的"同 scheme 同域"校验对齐，**均未验证**。所以本册对 OAuth 路径的结论只有一句：**先用 LLT；如果你坚持 OAuth，请先在实机上把上面三条硬规则逐条验证，失败了再退回 LLT。**

> [!tip] 大白话
> `client_id` 这条约束，可以理解成"报户口报的是你自己的门牌，不是你要去的那栋楼的门牌"。HA 要核对的是"来办卡的人"和"卡寄回的地址"是不是同一户——你把 HA 自己的住址填成自己的门牌，等于说"我住你家，请把卡寄到你家"，系统一眼看穿就拒了。所以难点从来不是"HA 支不支持 OAuth"，而是"**Hermes 有没有一块属于自己的、能收信的门牌**"——这一点本册没验出来。

## 5.4 反代与隧道

如果你的 Hermes 不在 HA 同一网段、要通过 Cloudflare Tunnel 之类的反代接过去，官方有一段专门的提示：

> When accessing Home Assistant remotely through a reverse proxy or tunnel (such as Cloudflare Tunnel), the hostname used by the remote LLM client must match the configured **Internal URL** or **External URL** in Home Assistant… If an unconfigured hostname or proxy header mismatch is used, Home Assistant cannot resolve the `issuer` in `/.well-known/oauth-authorization-server` and returns relative paths, which causes conforming OAuth clients to reject the metadata.

[^c5-HAS01-PROXY]

关键点是**主机名必须落在 HA 已配置的 Internal URL 或 External URL 上**。失败模式也很具体：HA 解析不出 `issuer`，于是 metadata 里返回**相对路径**，而合规的 OAuth 客户端要求绝对路径——客户端在"读元数据"这一步就拒了，根本走不到登录。所以如果你看到的报错发生在授权之前、且措辞是"metadata 被拒"，先查主机名，不要查令牌。

官方在同一个提示框里还给了替代方案：**用 Home Assistant Cloud（`https://<your-id>.ui.nabu.casa`）是推荐做法，因为它避开了反代与隧道的配置坑**。[^c5-HAS01-PROXY]

注意这条提示出现在 `#### OAuth` 小节里——它讲的是 OAuth metadata 的解析。走 LLT bearer 的话，请求头里带着令牌直接打 `/api/mcp/assist`，不经过 metadata 发现那一环，所以这条约束对 LLT 路径不直接适用。但反过来理解也成立：**LLT 之所以在反代场景下更稳，部分原因就是它跳过了这条最容易踩的路径。**

## 5.5 跨版本行为相反

这一节是本章最需要注意的地方：**`/api/mcp` 的 admin 要求，在 2026.9 与 2026.10 之间是相反的。** 本册的判定来自 HA core 的两个分支快照（`master` / `rc` 对应 2026.9，`dev` 对应 2026.10），不是文档转述。

| | 2026.9（`master` / `rc`） | 2026.10（`dev`） |
|---|---|---|
| 是否有 `CONF_REQUIRE_ADMIN` | **无** | 有（`CONF_REQUIRE_ADMIN = "require_admin"`） |
| Streamable 视图 docstring | "This serves the configured LLM APIs and **does not require admin access**." | "This serves the configured LLM APIs and **requires admin access when the config entry is configured to require it**." |
| 校验逻辑 | 视图内无 admin 校验；仅 `/api/mcp/<api_id>` 对非 Assist 的 API 要求 `is_admin` | 新增 `_validate_admin()`：`if entry.data[CONF_REQUIRE_ADMIN] and not request["hass_user"].is_admin` |
| UI 文案 | — | `"require_admin": "Require an administrator account"` |

源码位置：SRC-11（2026.9）、SRC-12（2026.10）。[^c5-SRC11][^c5-SRC12] 两边的 `/api/mcp/<api_id>` 逻辑是**没变**的——2026.10 里那段仍然是 `if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin`，即"Assist 之外要 admin"。[^c5-SRC12] 变的是**基础端点 `/api/mcp`**：从"一律不要 admin"变成"由配置项决定要不要"。

**还没完，2026.10 内部还有一个默认值不一致的问题。** 同一份 `dev` 快照里，两条路径给出的 `require_admin` 默认值是相反的：

| 路径 | 默认值 | 源码依据 |
|---|---|---|
| 新安装 | `True` | 创建条目时 `data={**user_input, CONF_REQUIRE_ADMIN: True}` |
| 1.1 → 1.2 迁移 | `False` | `data={CONF_REQUIRE_ADMIN: False, **entry.data}` |

[^c5-SRC12] 而且源码注释把"为什么迁移给 False"直接写了出来：

> `# 1.1 -> 1.2: Endpoints served before this option existed stay open.`

同一段注释还补了半句："A disabled config entry migrates only once enabled, so keep the choice the options flow may have saved in the meantime."[^c5-SRC12] 也就是说：**老配置升级上来的端点默认保持开放，新装的默认收紧**——同一版本内，两条路径的默认行为相反。

**这里要如实留白。** 以上判定全部基于源码分支快照，而 `require_admin` 是否真的会进入 2026.10 的**正式版**，本册**无法定论**：`dev` 分支有这套改动，`rc` 分支没有，期间是否 revert 未知（素材第 7.2 节的 G-2）。所以正确的做法是：**动手前先看你自己的 HA 版本**（HA 的「关于」页），再按上表对照；不要拿本章的结论当"2026.10 一定如此"的保证。

> [!tip] 大白话
> 同一个门，2026.9 的门卫手册写的是"这个门不查证件"，2026.10 的手册改成了"这个门要不要查证件，看这栋楼的设置"——而且同一栋楼里，**新住户默认设为"要查"，老住户搬家过来默认设为"不查"**。所以"官方说这个端点要不要 admin"这个问题，离开版本号和"新装还是升级"这两个前提，根本没法回答。

## 5.6 工具集裁剪

Hermes 侧的裁剪规则与第 4 章完全一致，不重复展开：用 `tools.include` / `tools.exclude`，写**服务端原生工具名**，两者都设时 `include` 优先。[^c5-HMS04-TOOLS] 差别只在于"原生名"是什么：第 4 章是 ha-mcp 的 `ha_get_state` 那一套；这里是**你所选 LLM API 暴露的工具名**（Assist 默认那套，形如 `HassTurnOn`、`GetLiveContext` 等）。[^c5-HAS01-TOOLS]

所以这里的操作顺序跟第 4 章略有不同：**先探测、再写白名单**。不要凭猜测往 `include` 里填名字——填错的效果是"白名单匹配不到任何工具，于是什么都不注册"，而且不会报错。先用 `hermes mcp test ha-official` 拿到真实工具清单，再挑需要的写进去。

顺带说明官方集成对 MCP 能力的支持范围，因为它决定了你能裁到什么：官方页面自陈目前只支持 MCP 特性的一部分——**Prompts 支持、Tools 支持、Resources 支持（仅 Assist）、Sampling 不支持、Notifications 不支持**。[^c5-HAS01-LIMITS] 没有 Sampling 与 Notifications，意味着这个 server 不会主动向客户端推消息，也不能让服务端反过来调用 LLM。

## 5.7 落点对照

先把落点配置给全。**再次强调：整段为拼接·未验证。**

```yaml
# ~/.hermes/config.yaml
# ⚠️ 拼接·未验证：HA 官方 mcp_server 文档未提供 Hermes 示例。
#    本段由本册按官方端点规格（HAS-01 / HAS-25）拼出，未经官方或实机验证。
mcp_servers:
  ha-official:
    url: "http://192.168.1.10:8123/api/mcp/assist"
    headers:
      Authorization: "Bearer ${env:HA_LLT_TOKEN}"
    trust: untrusted
    tools:
      # 下面的名字是占位示例，请先用 `hermes mcp test ha-official` 取真实原生名
      include:
        - "HassTurnOn"
        - "HassTurnOff"
        - "GetLiveContext"
```

落地步骤：

1. 在 HA 侧确认 `mcp_server` 集成已启用，并记下你选的是哪个 LLM API（默认 Assist）。
2. 创建长期访问令牌，写入 `~/.hermes/.env` 的 `HA_LLT_TOKEN`。[^c5-HAS01-LLT]
3. 按上面的 YAML 写入 `~/.hermes/config.yaml`（**这段是拼的**）。
4. 跑 `hermes mcp test ha-official`，拿到真实的原生工具名清单。
5. 用真实名字改写 `tools.include`，然后 `/reload-mcp`。
6. 在会话里确认 agent 能看到 `mcp__ha_official__*` 形态的注册名。

注意第 6 步的注册名形态：条目名是 `ha-official`，连字符同样会被 sanitize 成下划线（规则同第 4 章），所以注册名是 `mcp__ha_official__<tool>`。

**与第 4 章的选型对照：**

| 维度 | 第 4 章：社区 ha-mcp | 本章：官方 `mcp_server` |
|---|---|---|
| 配置来源 | 项目维护者写的 Hermes 模板（COM-23） | **本册拼接**，官方无 Hermes 示例（HAS-01） |
| 实体作用域 | `Everything in Home Assistant` | `Only entities exposed to Assist`（官方明文） |
| 写配置 / 历史 / 摄像头 | 有 | **无** |
| 端点数 | 工具数口径不一（87 / 95+ / ~84） | 取决于所选 LLM API 暴露的工具集 |
| 鉴权 | Bearer 或 OAuth，模板两者都给 | LLT bearer（官方推荐出路）或 OAuth/IndieAuth（Hermes 侧未验证） |
| 版本敏感度 | 低 | **高**：`/api/mcp` 的 admin 要求 2026.9 与 2026.10 相反 |

作用域那一行是**官方明文的路线差异**，不是社区项目自己的宣传：ha-mcp 的 README 直接把两条路的实体范围并列写了出来。[^c5-COM01-SCOPE] 落到选择上就是一句话：**要写配置、要历史、要摄像头，走第 4 章；只要官方来源、只做控制和查询，走本章。**

最后做一次交叉引用，不展开：本章配置里"读某个开关来控制 agent 能不能操作 HA"这件事，在第 8 章会有一个专门的坑——官方文档里长期存在的 `Control Home Assistant` 配置项，在代码侧查无对应键（E-3 / E-4）。那条留到第 8 章讲一次，本章不重复。

> [!summary] 本章小结
> - 端点 `/api/mcp`；Assist 恒为 `/api/mcp/assist`；官方实现的是 Streamable HTTP。
> - 官方给了 6 个客户端示例（Claude for Desktop / ChatGPT / Claude Code / Codex / Cursor / Antigravity CLI），**没有 Hermes** → 本章 YAML 整份标"拼接，未经官方或实机验证"。
> - 官方明说"不支持 OAuth 的客户端可以用 access token"，所以 **LLT bearer 是变量最少的接法**；OAuth/IndieAuth 是另一条路，且 `client_id` 必须是客户端应用自己的 base URL、绝不能是 HA 实例 URL，回调端口还须与 `client_id` 一致——**Hermes 侧是否有等价回调，未验证**。
> - 反代/隧道场景：主机名必须匹配 HA 的 Internal URL 或 External URL，否则 metadata 返回相对路径被拒；官方推荐直接用 Home Assistant Cloud 避开这个坑。
> - `/api/mcp` 的 admin 要求在 **2026.9 与 2026.10 相反**；且 2026.10 内部"新装默认收紧、迁移默认开放"两条路径不一致。`require_admin` 是否进正式版无法定论，如实留白。
> - 与第 4 章的路线差异是官方明文的：实体作用域、能力覆盖、鉴权模型、版本敏感度四项。

## 下一章预告

下一章换一个方向：不再讨论"怎么把工具接进来"，而是讨论"接进来之后，谁来触发它"。事件转发默认一条都不开、逐实体限流、cron 把结果投回 HA 时有两条分支、以及长报告为什么会被静默砍尾——那是一份 `platforms.homeassistant.extra` 配置片段。

---
## 本章来源

本章采用**脚注体**引用：正文里的上标与该章的脚注定义一一对应，下附脚注定义块即本章来源清单，每条开头标注 canonical ID（`HAS-*` / `HMS-*` / `SRC-*` / `COM-*`）。其余各章为来源表体，两处内容等价。


[^c5-COM01-SCOPE]: COM-01（ha-mcp README）对照表：官方 MCP Server 集成 `Only entities exposed to Assist` vs ha-mcp `Everything in Home Assistant`。本册 D-9 标记为"官方明文的路线差异"。

[^c5-HAS01-CODEX]: HAS-01 `### Example: Codex` 段原文：`oauth = { client_id = "http://127.0.0.1:12345" }`，及 "The callback port and the port in `client_id` must match…"。

[^c5-HAS01-DCR]: HAS-01 `#### OAuth` 小节 note 块：HA 实现 OAuth Client ID Metadata Document（`client_id_metadata_document_supported: true`），不提供 RFC 7591 `registration_endpoint`；严格依赖 RFC 7591 的客户端无法自动注册。

[^c5-HAS01-EP]: HAS-01 `### Exposing a specific LLM API` 段原文（`/api/mcp/<api_id>`、`/api/mcp/assist`、"Connecting to any API other than Assist requires the authenticated user to be an administrator."）。

[^c5-HAS01-EXAMPLES]: HAS-01 `### Example:` 小标题清单（L127 Claude for Desktop、L178 ChatGPT、L199 Claude Code、L222 Codex、L255 Cursor、L286 Antigravity CLI）。其中给 Claude for Desktop 的 URL 为 `https://<your_home_assistant_external_url>/api/mcp`，给 Codex 的为 `http://<your_local_home_assistant_ip_or_url>:8123/api/mcp`。

[^c5-HAS01-INDIE]: HAS-01 `#### OAuth` 段的 Client ID / Client Secret 两条原文。

[^c5-HAS01-LIMITS]: HAS-01 `## Known limitations`：Prompts / Tools 支持，Resources 支持（Assist only），Sampling / Notifications 不支持。

[^c5-HAS01-LLT]: HAS-01 `#### Long-lived access tokens` 段原文与三步创建流程。

[^c5-HAS01-PROXY]: HAS-01 `#### OAuth` 小节 tip 块原文（反代 / 隧道主机名须匹配 Internal URL 或 External URL；否则返回相对路径被拒；推荐 Home Assistant Cloud）。

[^c5-HAS01-PROTO]: HAS-01 `## Architecture overview` 段原文（以 Streamable HTTP 协议实现）。

[^c5-HAS01-TOOLS]: HAS-01 `## Supported functionality` → `### Tools`：`The tools used by the configured LLM API are exposed.`

[^c5-HMS04-AUTH]: HMS-04（Hermes `website/docs/reference/mcp-config-reference.md`），`auth` 键：`Set to oauth to enable OAuth 2.1 with PKCE`。**Hermes 侧 OAuth 的 `client_id` 与回调行为在素材中无依据，属未验证项。**

[^c5-HMS04-TOOLS]: HMS-04 `## tools policy keys` 与 `## Filtering semantics`：`include` / `exclude` 用服务端原生工具名，支持 fnmatch glob；两者都设时 `include` 优先。与第 4 章同一条规则。

[^c5-SRC11]: SRC-11（HA core `components/mcp_server/` @ `master`/`rc`，=2026.9）：`HAS-core-master-http.py` 视图 docstring 为 "does not require admin access"；无 `CONF_REQUIRE_ADMIN`；`/api/mcp/<api_id>` 处对非 Assist 要求 `is_admin`。

[^c5-SRC12]: SRC-12（HA core `components/mcp_server/` @ `dev`，=2026.10）：`HAS-core-dev-const.py` 定义 `CONF_REQUIRE_ADMIN = "require_admin"`；`HAS-core-dev-http.py` 的 `_validate_admin()` 为 `if entry.data[CONF_REQUIRE_ADMIN] and not request["hass_user"].is_admin`，视图 docstring 为 "requires admin access when the config entry is configured to require it"；`HAS-core-dev-strings.json` 文案 `Require an administrator account`；`HAS-core-dev-config_flow.py` 新装写入 `CONF_REQUIRE_ADMIN: True`、`_options_schema` 回落 `data.get(CONF_REQUIRE_ADMIN, False)`；`HAS-core-dev-__init__.py` 迁移 `1.1 -> 1.2` 写入 `CONF_REQUIRE_ADMIN: False` 并注释 `Endpoints served before this option existed stay open.`
