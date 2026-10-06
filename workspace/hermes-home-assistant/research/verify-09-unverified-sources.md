---
title: "P4 前置核验：9 组未复核来源的定点回源"
task: learning-note-flow / P4 前置核验
created: 2026-09-18
scope: 6 条（HMS-03 / HMS-06 / HAS-05 / HAS-06 / COM-16 / COM-22）
retrieval_agent: P4-precheck
---

# P4 前置核验：6 条未复核来源

回源纪律：每条只判定下方给定的**待核结论**（原文为「未核实概述」），不扩充其他来源；找不到原文即写「回源失败」，不用二手转述补位。

取回时间统一记为 2026-09-18（爬虫快照 frontmatter 内的 `scraped_at` 为 UTC，本地时区 UTC+8）。

---

### HMS-03 — Toolsets Reference

- **URL / 路径**：`https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/reference/toolsets-reference.md`（分支 `main`，直取原始 Markdown，13575 字节）
- **取回时间**：2026-09-18
- **待核结论（未核实概述）**：MCP server 提供的工具与内置 toolset 同名时两者**叠加、不互相遮蔽**。
- **原文逐字**：「This creates a `mcp-github` toolset you can reference in `--toolsets` or platform configs. The bare server name (`github`) works as an alias. If a server is named like a built-in toolset (`homeassistant`, `browser`), that name resolves to the built-in tools **plus** the server's `mcp__<server>__*` tools; neither side shadows the other.」
- **定位**：`website/docs/reference/toolsets-reference.md`，小节 `## Dynamic Toolsets` → `### MCP server toolsets` 末段（本地快照 `sources/_verify/HMS-03-toolsets-reference.md` 第 136 行）
- **判定**：支持
- **更正或补充**：原文把「不遮蔽」限定在**同名解析**这一条路径上，并同时给出别名的第二行为「The bare server name (`github`) works as an alias」。同一节还确认「Each configured MCP server generates a `mcp-<server>` toolset at runtime」。另有一处需要一并带上的周边事实：本文档 `### Plugin toolsets` 明确写「Plugins can register their own toolsets via `ctx.register_tool()` during plugin initialization.」（第 140 行）——这条可给 HMS-06 做交叉印证。注意同名叠加只对**工具集解析**成立；单工具层面的遮蔽是**另一套规则**（见 HMS-06 的 `override=True` 门禁），正文不要把两者混为一谈。
- **置信度**：高（`raw.githubusercontent.com` 直接取回原始 Markdown，HTTP 200、体积与文档规模相符，非 GitHub Pages 404 页）

---

### HMS-06 — Plugins（`user-guide/features/plugins.md` + `developer-guide/plugins/index.md`）

- **URL / 路径**：
  - `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/plugins.md`（48730 字节）
  - `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/developer-guide/plugins/index.md`（86045 字节）
- **取回时间**：2026-09-18
- **待核结论（未核实概述）**：自定义 plugin 可注册工具（形如 `ctx.register_tool(name=…, toolset=…, schema=…, handler=…)`）；plugins **默认 opt-in**，需显式启用命令。
- **原文逐字**：
  - 注册签名（`developer-guide/plugins/index.md`，`register()` 示例）：「`ctx.register_tool(name="calculate",    toolset="calculator",`」「`schema=schemas.CALCULATE,    handler=tools.calculate)`」
  - 注册签名（表格形式，`user-guide/features/plugins.md`）：「| Add tools | `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)` |」
  - opt-in 主句（`user-guide/features/plugins.md`，小节 `## Plugins are opt-in (with a few exceptions)`）：「**General plugins and user-installed backends are disabled by default** — discovery finds them (so they show up in `hermes plugins` and `/plugins`), but nothing with hooks or tools loads until you add the plugin's name to `plugins.enabled` in `~/.hermes/config.yaml`. This stops third-party code from running without your explicit consent.」
  - 例外表结论句：「In short: **bundled "always-works" infrastructure loads automatically; third-party general plugins are opt-in.** The `plugins.enabled` allow-list is the gate specifically for arbitrary code a user drops into `~/.hermes/plugins/`.」
  - 显式启用命令：「`hermes plugins enable <name>      # add to allow-list`」「`hermes plugins install user/repo --enable    # install AND enable (no prompt)`」
  - 项目本地插件另有一道门：「Project-local plugins under `./.hermes/plugins/` are disabled by default. Enable them only for trusted repositories by setting `HERMES_ENABLE_PROJECT_PLUGINS=true` before starting Hermes.」
- **定位**：
  - 注册签名 → `developer-guide/plugins/index.md` 第 551–553 行 / `user-guide/features/plugins.md` 第 101 行
  - opt-in 主句 → `user-guide/features/plugins.md` 小节 `## Plugins are opt-in (with a few exceptions)` 首段（第 149–151 行）
  - 例外表 → 同页 `### What the allow-list does NOT gate`（第 218–233 行）
  - 启用命令 → 同页命令清单（第 366–377 行）
  - 项目本地插件门 → 同页第 93 行
- **判定**：部分支持
- **更正或补充**：待核结论的两半要分开处理。
  1. **注册签名：支持。** `ctx.register_tool(name=…, toolset=…, schema=…, handler=…)` 在 `user-guide/features/plugins.md` 里就是原样表格条目，`developer-guide/plugins/index.md` 还有可用样例。另需补一句文档事实：注册也可带可选参数 `description=`、`check_fn=`；`override=True` 是**换掉**内置工具的另一条路，且受 `plugins.entries.<plugin_id>.allow_tool_override: true` 门禁，未授权会抛 `PluginToolOverrideError`（第 899–947 行）。
  2. **「plugins 默认 opt-in」：只有限定后才成立。** 原文限定词是「**General** plugins and user-installed backends」，且同页有整张**例外表**：Bundled platform plugins、Bundled backends、Memory providers、Context engines、Model providers 这几类**绕过** `plugins.enabled` 自动加载。正文若写成不带限定的「plugins 默认 opt-in」即为**过宽**，必须改写成「第三方/通用插件默认 opt-in；随 Hermes 一起分发的 bundled 平台/后端插件自动加载」。另：项目本地插件（`./.hermes/plugins/`）还有独立的 `HERMES_ENABLE_PROJECT_PLUGINS=true` 开关，与 `plugins.enabled` 不是同一个门。
- **置信度**：高（两个文件均从 `raw.githubusercontent.com` 直取 main 分支原始 Markdown；文本内部自洽，opt-in 主句与其后的例外表可互相校验）

---

### HAS-05 — Authentication API（Home Assistant 开发者文档）

- **URL / 路径**：`https://developers.home-assistant.io/docs/auth_api/`（快照 `sources/_verify/HAS-05/01_developers_home-assistant_io.md`，12686 字节）
- **取回时间**：2026-09-18
- **待核结论（未核实概述）**：长期访问令牌**有效期 10 年**；吊销 refresh token 会**立即连带撤销**它签发的全部 access token。
- **原文逐字**：
  - 「Long-lived access tokens are valid for 10 years. These are useful for integrating with third-party APIs and webhook-style integrations.」
  - 「To revoke a refresh token, make an HTTP POST request to `http://your-instance.com/auth/revoke` with the request body encoded in `application/x-www-form-urlencoded`. Revoking a refresh token will immediately revoke the refresh token and all access tokens that it has ever granted.」
- **定位**：两条都在同页；LLT 句在小节 `## Long-lived access token`（第 259 行），吊销句在小节 `### Revoking a refresh token`（第 232 行）
- **判定**：支持
- **更正或补充**：两个数字/语义都逐字成立，但**必须补上「两者是不同的 token 家族」这层限定**，否则正文会把两条拼成一条假因果：
  - 10 年有效期说的是 **long-lived access token**；吊销段说的是 **refresh token**。LLT 是由用户 profile 页或 WebSocket 命令 `auth/long_lived_access_token` 生成的**独立长期凭据**，不是 refresh token 签发链路的下游产物。因此「吊销 refresh token 会连带撤销它签发的 access token」**不能**推出「吊销某个 refresh token 会撤销该用户的 LLT」。
  - 原文另有两条支撑「LLT 属用户」的句子可一并引用：「will create a long-lived access token for the current user」「The access token string is not saved in Home Assistant; you must record it in a secure place.」
  - 若要写「LLT 怎么失效」，本页只提供了间接线索（`### Signed paths` 一节末：「If the user is deleted, the signed URL is no longer valid (because the refresh token will be deleted).」），**没有**直接说 LLT 的吊销路径——这一层不要凭本页外推。
- **置信度**：高（官方开发者文档页面，逐字可引）

---

### HAS-06 — Permissions（Home Assistant 开发者文档）

- **URL / 路径**：`https://developers.home-assistant.io/docs/auth_permissions/`（快照 `sources/_verify/HAS-06/01_developers_home-assistant_io.md`，12151 字节）
- **取回时间**：2026-09-18
- **待核结论（未核实概述）**：权限粒度可按 **entity / domain / area / device** 收紧到用户或组；且这是**用户属性、不是 token 属性**。
- **原文逐字**：
  - 「Permissions limit the things a user has access to or can control. Permissions are attached to groups, of which a user can be a member. The combined permissions of all groups a user is a member of decides what a user can and cannot see or control.」
  - 「Entity permissions can be set on a per entity and per domain basis using the subcategories `entity_ids`, `device_ids`, `area_ids` and `domains`.」
  - 「The system will return the first matching result, based on the order: `entity_ids`, `device_ids`, `area_ids`, `domains`, `all`.」
  - 「To check a permission, you will need to have access to the user object. Once you have the user object, checking the permission is easy.」
  - 「These context objects also contain a user id, which is used for checking the permissions.」
- **定位**：首段（第 9 行）、`## Entities` 小节（第 56–57 行）、`### Checking permissions` 小节（第 173 行）、`### The context object` 小节（第 227 行）
- **判定**：部分支持
- **更正或补充**：
  - **「entity / domain / area / device 四档 + 挂到用户或组」：支持，逐字。** 原文四档写作 `entity_ids` / `device_ids` / `area_ids` / `domains`；归属关系原文写作「attached to groups, of which a user can be a member」，且**组策略在运行时合并**（「the groups permission policies will be combined into a single policy at runtime」）。另需带上两条边界：`owner` 用户不受权限约束（「Permissions do not apply to the user that is flagged as "owner".」）；四档的匹配是**有顺序的 first-match**，不是取并集——写「收紧」时若漏掉顺序，行为会讲错。
  - **「这是用户属性、不是 token 属性」：本页无此表述，属推断，不能加引号引用。** 全页检索 `token` **零命中**。可用的**间接**原文是「To check a permission, you will need to have access to the user object.」和「These context objects also contain a user id, which is used for checking the permissions.」——它们说明**权限判定的输入是 user 对象 / context.user_id**，但**没有**任何一句把权限与 token 对照着说。因此这一半只能写成「按文档，权限挂在用户/组、判定以 user 对象为准」，**不要**写成带引号的「官方说不属于 token 属性」。
  - 与 HAS-05 联动注意：HA 页的语义是「token 属于某个 user」，把两页合起来讲链条时要标为拼接，不要冒充单页原文。
- **置信度**：中。「四档 + 用户/组」部分置信度高（逐字命中）；「不是 token 属性」部分为**推断，非原文**，全文无 `token` 字样可支撑

---

### COM-16 — Ha-mcp macht den Kontext voll（simon42 Community）

- **URL / 路径**：`https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707`（4 帖主题；用同站 Discourse JSON `https://community.simon42.com/t/88707.json` 取到**完整 4 帖正文**，19980 字节）
- **取回时间**：2026-09-18
- **待核结论（未核实概述）**：77 个工具 schema **常驻约 60.3k tokens**；最贵的单工具 **1.8k–3.4k tokens**。
- **原文逐字**（德语）：
  - 楼主 Mathias42（post 1）：「Ich nutze ha-mcp in Kombination mit Claude Code im CLI.」「Die MCP Tools verbrauchen schon über 60k Tokens.」
  - Mercator（post 2）：「Dein Home Assistant MCP-Server ballert Claude mit stolzen 77 Tools zu, Claude braucht im Alltag niemals 77 Tools gleichzeitig.」「Die Messages schnappen sich aktuell 110k Tokens.」
  - Mathias42（post 3，**转述 Claude 的回答**）：「Die 60k Tokens waren die Tool-Definitionen (Name + Beschreibung + JSON-Schema der Parameter) aller ~77 HA-MCP-Tools — nicht Nutzdaten, sondern reine Schema-Deklarationen, die bei jedem API-Call mitgeschickt werden müssen, damit ich weiß, was ich aufrufen kann.」
  - 同上，单工具峰值：「Die teuersten Einzeltools lagen bei 1,8k–3,4k Tokens (ha_config_set_helper, ha_get_integration, ha_config_set_dashboard, ha_config_set_automation).」
  - 同上，合计：「Summiert über 77 Tools kommen die 60,3k zusammen — bei anderen MCP-Servern mit 5–15 Tools sieht man das selten in dieser Größenordnung.」
  - 同上，结论句：「Verbundene MCP-Server kosten ihre volle Tool-Schema-Größe bei jeder Nachricht, unabhängig davon, ob man sie nutzt — nicht amortisiert.」
  - 楼主补一句（post 3 末）：「Man kann wohl auch keine einzelnen Tools deaktivieren oder nur die Namen lazy-loaden.」
- **定位**：主题第 1–4 帖；`60,3k` 与 `1,8k–3,4k` 均在 **post 3**（Mathias42，2026-07-06T08:48:43Z），`77 Tools` 在 **post 2**（Mercator，2026-07-06T08:01:16Z）
- **判定**：支持
- **更正或补充**：四条数字都能逐字命中，但**必须改掉来源的举证性质**——这是本轮核验最关键的一条更正：
  - **`60,3k` / `1,8k–3,4k` 不是独立测量值，而是 Claude 自述。** 该帖的全部数字出处在 post 3，开头即「Claude sagt dazu:」；也就是说这是**模型对自己上下文占用的自然语言自报**，不是用 tokenizer 或计数工具跑出来的对照数据。楼主自己在 post 1 只说了「über 60k Tokens」（超过 60k），**60,3k 这个带一位小数的精确值只存在于 Claude 的自述里**。
  - 因此正文引用时**只可写**：「社区用户报告（经 Claude 自述）77 个工具合计约 60.3k tokens，最贵单工具 1.8k–3.4k」并标注为**自报值、无第三方复现**；**不可**写成「实测 60.3k」。
  - 缺一个可直接引的锚：`1,8k–3,4k` 点名了四个工具（`ha_config_set_helper`、`ha_get_integration`、`ha_config_set_dashboard`、`ha_config_set_automation`），但**没有**给出任一个工具的单值明细，区间上下界对应哪个工具未说明。
  - 同帖另有未进本条的可用数字（如需引用须另行标注）：post 1 附了一张 1228×1090 的截图（`Bildschirmfoto 2026-07-06 um 09.34.51`，90.7 KB）；post 2 给出「110k Tokens」；帖子日期 2026-07-06。
- **置信度**：高（正文逐字来自同站 Discourse JSON，非 HTML 转文本残片；数字与帖内上下文自洽）。**但对「把该数字当作客观实测」的置信度：低**——理由是来源自认是模型自述

---

### COM-22 — New assist with LLM combination, lot of tokens?（HA 官方论坛）

- **URL / 路径**：`https://community.home-assistant.io/t/736566`（标题见正文「new assist with llm combination, lot of tokens」；原帖 2024-06-06 起）
- **取回时间**：2026-09-18
- **取回路径说明**：直连被 Cloudflare JS 挑战拦截（`crawl.sh` 返回 `Blocked by anti-bot protection: Cloudflare JS challenge`；`curl` 取 HTML 与 `/t/736566.json` 均为 HTTP 403 + `Just a moment...` 挑战页；jina 代理 403；allorigins/codetabs 代理 522；Wayback 服务当时整体离线，该 URL 也无快照）。最终经 `WebFetch` 打 `https://community.home-assistant.io/t/736566.json` 取到 post 1–20 的正文与字段。
- **待核结论（未核实概述）**：230 / 340 / 100 实体对照下的 token 实测数字。
- **原文逐字**（英文，均为帖内直接引语）：
  - skycryer（post 1，楼主）：「I had now 36 api request with got-4o and a usage of 339.000 context tokens and 1800 generated tokens.」「I have around 230 entities open to assist for usage, does the api send everything to chatGPT on api call to handle it?」
  - Kolossboss（post 2）：「I have 16 request and already 200 000 generated tokens.」
  - Ollijung（post 5）：「13 API requests」「130,000 tokens」「totalling 0.66$」
  - Ollijung（post 8）：「I set now to gpt 3.5 turbo and yeah it still uses 10000 tokens for turning on a light.」「Even with 1/10 of the price it's still 0.6 Cent per command.」
  - Ollijung（post 11）：「oh ok, I have 242 entities exposed to assist.」
  - Kolossboss（post 14）：「I reduced my exposed entities from 340 to 100.」「Still Using 5000 Tokens for a simple  request.」
  - rossk（post 12）：「From what I read 1 token is equal to approx 4 characters.」
- **定位**：Discourse 帖 736566；post 1（skycryer）、post 2（Kolossboss）、post 5 / 8 / 11（Ollijung）、post 14（Kolossboss）、post 12（rossk）。`230` 在 post 1，`340 → 100` 在 post 14，`10000 / 0.6 Cent` 在 post 8。注：抓到的 JSON 覆盖 post 1–20。
- **判定**：部分支持
- **更正或补充**：
  - **数字本身能逐字对上，但「230 / 340 / 100 实体对照」这个框架不成立。** 这些数字分属**三个不同用户、不同会话、不同模型**：post 1 是 skycryer 的 ~230 实体（gpt-4o，36 次请求 / 339.000 context tokens / 1800 generated）；post 14 是 **Kolossboss** 的 340→100 实体收紧（「Still Using 5000 Tokens for a simple request」）；post 11 的 242 实体又是 **Ollijung**。帖子里**没有**任何一次「同一用户把实体数从 X 调到 Y、其余变量固定」的对照实验。正文必须写成**多用户自报值的并列**，不能写成对照组。
  - **`339.000` 是欧陆千分位写法，等于 339,000**；同帖 `200 000`、`130,000` 混用空格/逗号，引用时需统一并注明原写法，避免读者误读为「339 个 token」。
  - 计量口径也不统一：post 1 给的是 **context tokens**，post 2 说的是 **generated tokens**（「200 000 generated tokens」）——两者不可比，别并到一张表里当同一指标。
  - 补两条可用但需各自标注的旁证：post 5「13 API requests / 130,000 tokens / totalling 0.66$」（同一用户的成本换算）、post 12「1 token is equal to approx 4 characters」（用户转述的经验值，非官方口径）。这两条**本轮未做独立回源**，引前需按同一标准核。
  - 该帖为 **2024-06** 内容，HA 的 Assist/LLM 管线此后有变更，正文引用时须带时间戳。
- **置信度**：中。理由是**取回路径**：直连全被 Cloudflare 拦截，最终数字来自 `WebFetch` 对 `/t/736566.json` 的抽取，**我未能拿到可留存比对的原始字节**；两次独立 WebFetch（HTML 页与 JSON 端点）给出的引语互相一致，且与 P2 期 probe-06 记录的同串引语一致，故判「引语可靠」；但「逐字到标点」这一级仍低于 HMS/HAS 各条的直取快照。**建议**：若正文要带引号引用 `339.000` 这类数字，先在有浏览器的环境重取一次 `https://community.home-assistant.io/t/736566.json` 存成快照，再定稿。

---

## 结论汇总

| ID | 判定 | 需要回填到 `02_deep_research.md` 的变更 |
|---|---|---|
| HMS-03 | **支持** | §2.3 表内 HMS-03 行「未复核」→「**已回源**（同名 MCP server = 内置 toolset + `mcp__<server>__*`，互不遮蔽；L136）」。§7.3 无需再列本条。 |
| HMS-06 | **部分支持** | §2.3 表内 HMS-06 行「未复核」→「**已回源**（`register_tool(name/toolset/schema/handler)` 逐字；opt-in **须限定为第三方/通用插件**，bundled 平台/后端插件自动加载，例外表见 plugins.md `### What the allow-list does NOT gate`）」。**新增一条更正**：P2 期若在 §3/§5 里写过不带限定的「plugins 默认 opt-in」，按上句收窄。 |
| HAS-05 | **支持** | §2.2 HAS 表对应行标「**已回源**（10 年、`/auth/revoke` 连带撤销，逐字）」。**新增§5 类更正**：正文凡把「10 年有效期」与「吊销 refresh token 连带撤销」并置时，须写明 **LLT 与 refresh token 是两条独立链路**，不可由后者推出「吊销 refresh token 会撤销该用户 LLT」。 |
| HAS-06 | **部分支持** | §2.2 HAS 表对应行标「**已回源**（四档 `entity_ids`/`device_ids`/`area_ids`/`domains`、挂组、first-match 顺序、owner 豁免——逐字）」。**新增§5 类更正**：「**权限不是 token 属性**」这半句在 auth_permissions 页**无原文**（全页 `token` 零命中），只能写成「判定以 user 对象 / `context.user_id` 为准」，**不得加引号**。 |
| COM-16 | **支持（举证性质须改写）** | §2.5 COM-16 备注「77 工具 schema 常驻 **60.3k tokens**，最贵单工具 1.8k–3.4k」→ 加限定语「**经 Claude 自述**（帖内 `Claude sagt dazu:`），楼主原始表述为 `über 60k Tokens`；无第三方复现」。§7.3 里把 COM-16 从「需回源」降级为「已回源，但**降格为自报值**」。**正文禁止**写成「实测 60.3k」。 |
| COM-22 | **部分支持** | §2.5 COM-22 备注「Assist + LLM token 实测（230/340/100 实体对照）」→ 改为「**多用户自报值并列，非对照实验**」（230/339.000 属 skycryer；340→100/5000 属 Kolossboss；242 属 Ollijung），并注明计量口径不一致（context tokens vs generated tokens）、帖子时间 2024-06。§7.3 由「需回源」改为「已回源，**但快照缺失**：仅有 WebFetch 抽取，建议定稿前重存快照」。 |

一句话风险排序：**COM-16 与 COM-22 的「数字」虽都逐字命中，但一条是模型自述、一条不是对照实验，二者都不宜以「实测」入正文**；HAS-06 的「不是 token 属性」半句无原文，须改写措辞；HAS-05 须补「LLT ≠ refresh token 链路」的限定；HMS-06 的 opt-in 须收窄到第三方插件。

---

## 仍未解决

1. **COM-22 无本地快照，直连仍被 Cloudflare 拦截。** 本条数字仅来自 `WebFetch` 对 `/t/736566.json` 的抽取，未落盘可比对字节。待办：在带浏览器的环境重取并存入 `sources/`，或等 Wayback 恢复后取快照；在此之前，正文若要带引号引用具体数字，须标注「未经本地快照核验」。
2. **COM-16 的 `60,3k` / `1,8k–3,4k` 无法升格为客观测量。** 唯一出处的帖子自认是 Claude 的回答；帖内那张 1228×1090 截图（`Bildschirmfoto 2026-07-06 um 09.34.51`）本次**未做 OCR**，无法判断截图里是否有独立于模型自述的计数。若正文需要「实测」级证据，须另找带可复现计数的来源，或退一步只写「社区用户报告」。
3. **HAS-05 未覆盖「LLT 的吊销路径」。** 本页只正面写了 10 年有效期与 refresh token 的吊销语义，没有说明长期访问令牌如何被撤销（用户删除 / 用户停用 / 重置密码等分支均未出现）。这是一个**明确的文档缺口**，正文若要讲「LLT 泄漏怎么办」须另找来源，或如实标注为缺口。
4. **HAS-06 的「token 属性」对照缺原文。** 本轮只在 `auth_permissions` 页内找，未去 HA 的 auth 架构页 / 源码找对照表述。若必须坐实「权限不是 token 属性」，需另起一次定点回源（候选：HA core `auth/` 源码，即 P2 的 SRC-14 范围），本轮**不做外推**。
5. **HMS-06 的 `override=True` 门禁未做代码侧交叉验证。** 本轮只核了文档口径（`allow_tool_override`、`PluginToolOverrideError`），**未**去 `plugins/` 源码确认该 gate 的实现与报错文案，也未确认 `plugins.enabled` 的读取位置。文档说「Plugins load after built-in tools」这一句同样只有文档支撑。
6. **本次未复核、仍在「未核实概述」状态的相邻条目**：COM-22 帖内 post 5 / post 12 的引语（`0.66$`、`1 token ≈ 4 characters`）随本条一并抓到时**未逐条回源**；COM-16 帖内 post 2 的 `110k Tokens` 同样未单独核验。三条若要用，须各自挂 ID 走一次回源。
