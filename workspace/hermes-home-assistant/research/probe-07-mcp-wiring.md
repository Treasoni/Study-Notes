# 探测原始记录 07：MCP 接线层（Hermes ↔ Home Assistant）

> **性质**：原始证据记录，**不是**阶段 2 的交付物 `02_deep_research.md`，不推进任何阶段状态。
> **来源**：P2 精读子代理 A「MCP wiring gap」，检索日期 2026-09-18。
> 仓库：`NousResearch/hermes-agent`（default_branch `main`）、`home-assistant/core`、`home-assistant/home-assistant.io`、`homeassistant-ai/ha-mcp`。
> **本记录解决了 P1 遗留缺口 1、2、3、8**（缺口 1 由**源码定论**，不再依赖实机；实机只需回填版本号）。
> **引用纪律**：源码级结论可作结论使用；标「未代验」的命令输出形态属推断。

---

## 待确认项 1：Hermes MCP 工具命名前缀 —— 已由源码定论

| 来源 ID | 标题 | URL | 档位 | 日期 | 锚点 | 主张（逐字） |
|---|---|---|---|---|---|---|
| HMS-M1 | `website/docs/user-guide/features/mcp.md` | raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/features/mcp.md | 官方文档 | 最后内容提交 2026-09-17 | `## How Hermes registers MCP tools`（L464）、代码块 L469、表格 L474–478、L498 | **已核对**：写 `mcp_<server_name>_<tool_name>`，示例表 `| filesystem | read_file | mcp_filesystem_read_file |`、`| github | create-issue | mcp_github_create_issue |`、`| my-api | query.data | mcp_my_api_query_data |`。**与源码不符** |
| HMS-M2 | `website/docs/reference/mcp-config-reference.md` | raw…/main/website/docs/reference/mcp-config-reference.md | 官方文档 | 最后内容提交 2026-09-17 | `## Tool naming`（L290）、L295、L299–307、L309、`### Name sanitization`（L311）、L318 | **已核对**：`mcp__<server>__<tool>`；"The double-underscore delimiter (`mcp__…__…`) matches the convention used by Claude Code, Codex, and OpenCode"；sanitize 例 `mcp__my_api__list_items_v2`。**与源码一致** |
| HMS-M3 | `website/docs/guides/use-mcp-with-hermes.md` | raw…/main/website/docs/guides/use-mcp-with-hermes.md | 官方文档 | 最后内容提交 **2026-06-21**（三处中最旧） | `### Typical prompt`（L161）、L163、L166 | **已核对**：`调用 MCP 工具 mcp_chrome_devtools_win_list_pages，列出当前浏览器标签页。`——单下划线。**与源码不符** |
| HMS-M4 | `tools/mcp_tool_schema.py`（实现） | raw…/main/tools/mcp_tool_schema.py | **一手源码** | 最后内容提交 2026-09-15 | L137–140、L143–149、L162–173、L176–182 | **定论来源**：`MCP_TOOL_NAME_PREFIX = "mcp__"`；`mcp_prefixed_tool_name()` → `full_name = f"{MCP_TOOL_NAME_PREFIX}{sanitize_mcp_name_component(server_name)}__{sanitize_mcp_name_component(tool_name)}"`；`sanitize_mcp_name_component` 用 `re.sub(r"[^A-Za-z0-9_]", "_", ...)`。模块 docstring 首行即 "mcp__server__tool naming" |
| HMS-M5 | 同文件迁移注释 | 同上 | 一手源码 | 2026-09-15 | L143–148 | "It also aligns native registration with the Anthropic-OAuth wire form (`_MCP_TOOL_PREFIX` in anthropic_adapter.py), **removing the single->double rewrite that path previously had to perform. See #33533.**" → 证明这是一次**尚未同步到全部文档的重命名** |
| HMS-M6 | `agent/anthropic_adapter.py` | raw…/main/agent/anthropic_adapter.py | 一手源码 | — | L246、L437–446 | `_MCP_TOOL_PREFIX = "mcp__"`；`_normalize_to_mcp_wire()`：`if name.startswith("mcp__"): return name  # already correct, don't double-prefix` 然后 `return _MCP_TOOL_PREFIX + name.removeprefix("mcp_")`。**其 docstring 仍写 "native MCP tools registered as `mcp_<server>_<tool>`"——注释本身也已过期** |
| HMS-M7 | `tests/agent/test_anthropic_mcp_prefix_strip.py` | raw…/main/tests/… | 一手源码（测试） | — | 模块 docstring L1–14 | 同样遗留旧描述："the single-underscore `mcp_<server>_<tool>` form for MCP server tools"。测试断言本身喂的是硬编码串，**通过与否无法区分两种命名** |
| HMS-M8 | 已发布文档站同名页 | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp | 官方文档（发布态） | 无日期；crawl 于 2026-09-18 | crawl 产物 `sources/02_hermes-agent_nousresearch_com.md` L712 | **已核对**：发布站仍输出 `mcp_<server_name>_<tool_name>` → 用户实际读到的是过期写法 |
| HMS-M9 | `hermes_cli/mcp_config.py` | raw…/main/hermes_cli/mcp_config.py | 一手源码 | — | L761 `def cmd_mcp_test`、L795、L444–446 | `tools_found.append((t.name, desc))`——`hermes mcp test <name>` 打印的是 **MCP 原生工具名**，不是注册名；`hermes mcp add`/`configure` 写入 `tools.include` 的也是原生名（L995 `server_config.setdefault("tools", {})["include"] = chosen_names`） |
| HMS-M10 | `website/docs/reference/cli-commands.md` | raw…/main/website/docs/reference/cli-commands.md | 官方文档 | — | L1509–1527、L1569–1579；`--version` L23 | `hermes mcp` 子命令表：`add` / `remove`(`rm`) / `list`(`ls`) / `test <name>` / `configure <name>` / `login <name>` / `serve` / `catalog` / `install <name>`；`hermes --version`、`-V` |
| COM-M1 | ha-mcp Setup Wizard（第三方独立旁证） | https://homeassistant-ai.github.io/ha-mcp/setup/ | 一手项目文档（第三方） | crawl 2026-09-18 | `sources/COM-ha-mcp-setup-wizard.html`，hermes 分支 JS | **已核对**：`Tool names: ha-mcp tools show up as mcp__home_assistant__<tool> (Hermes replaces the hyphen in the server name with an underscore).` → 与源码 `sanitize_mcp_name_component` 语义完全吻合 |

**待确认项 1 结论：文档不一致 + 版本遗留，不是"两派说法"**
- 现网实现是 **`mcp__<server>__<tool>`**（HMS-M4 逐字）；HMS-M2 正确，HMS-M1 / HMS-M3 是**同一仓库内未随 #33533 更新**的旧写法，发布站也未更新（HMS-M8）。
- 服务器名/工具名中的 `-`、`.` 会被替换为 `_`（HMS-M4 的 `sanitize_mcp_name_component`）；超 64 字符会截断并加 8 位 sha256 后缀（L154–173）。

**用户实机核实的确切命令（本机无 hermes CLI，未代验）**
```bash
hermes --version                 # 先记录版本
hermes mcp list                  # 确认 mcp_servers 条目名（如 home-assistant）
hermes mcp test home-assistant   # 只证明连通与"原生工具数"，打印的是 ha_get_state 之类的原生名，不能验证前缀
# 会话内：
/reload-mcp                      # 然后让 agent 报出它看到的 MCP 工具全名
```
若本机能对上 Hermes 安装包（源码 / site-packages）且 `tools/` 可导入，可直接跑：
```bash
python -c "from tools.mcp_tool_schema import MCP_TOOL_NAME_PREFIX as P, mcp_prefixed_tool_name as p; print(P); print(p('filesystem','read_file')); print(p('home-assistant','ha_get_state'))"
```
预期输出 `mcp__` / `mcp__filesystem__read_file` / `mcp__home_assistant__ha_get_state`。命令能否跑通取决于该版本的包是否暴露 `tools` 顶层包，**未代验**。

---

## 待确认项 2：HA 官方 `mcp_server` 连接方式

| 来源 ID | 标题 | URL | 档位 | 日期 | 锚点 | 主张（逐字） |
|---|---|---|---|---|---|---|
| HAS-M1 | `source/_integrations/mcp_server.markdown`（ha.io repo, branch `current`） | raw.githubusercontent.com/home-assistant/home-assistant.io/current/source/_integrations/mcp_server.markdown | 官方文档 | 最后内容提交 **2026-09-09**（`ac1f6676d` "Clarify MCP server OAuth configuration and troubleshooting (#47989)"） | L67–68 | "The Home Assistant MCP server is exposed as `/api/mcp` and requires the client to provide an authentication token." |
| HAS-M2 | 同上 | 同上 | 官方文档 | 同 | L76–85 | "`/api/mcp/<api_id>`"；**"For example, the built-in Assist API is always available at `/api/mcp/assist`."**；"If you request an API ID that does not exist, Home Assistant responds with a 404 Not Found error."；"Connecting to any API other than Assist requires the authenticated user to be an administrator. The Assist API stays available to non-administrator users, just like the base `/api/mcp` endpoint." |
| HAS-M3 | 同上 | 同上 | 官方文档 | 同 | L89–99（`#### OAuth`） | "Home Assistant has adopted IndieAuth and does not require you to pre-define an OAuth Client ID. Instead, the Client ID is the base URL of the client application making the request"；**"Client ID: The base URL of the LLM client application configuring the connector (for example, `https://claude.ai` for Claude, or `https://chatgpt.com` for ChatGPT). It must never be your Home Assistant instance URL."**；"validates that the OAuth `redirect_uri` shares the same scheme and domain with the `client_id`"；"Client Secret: This is not used by Home Assistant." |
| HAS-M4 | 同上 | 同上 | 官方文档 | 同 | L105–108（note 块） | "Home Assistant implements the OAuth Client ID Metadata Document specification (`client_id_metadata_document_supported: true`) rather than traditional Dynamic Client Registration (RFC 7591), and does not provide an RFC 7591 `registration_endpoint`." |
| HAS-M5 | 同上 | 同上 | 官方文档 | 同 | L111–115（tip 块） | 反代/隧道场景 hostname 必须匹配 **Internal URL** 或 **External URL**，否则 `/.well-known/oauth-authorization-server` 返回相对路径，规范客户端会拒绝 metadata |
| HAS-M6 | 同上 | 同上 | 官方文档 | 同 | L118–126 | "Some MCP clients may not support OAuth, but may support access tokens."（LLT 路径） |
| HAS-M7 | 同上：**第三方 client 配置示例清单** | 同上 | 官方文档 | 同 | L127 / L178 / L199 / L222 / L255 / L286 | **官方页面确实给了 6 个第三方 client 的完整示例**：`### Example: Claude for Desktop`、`### Example: ChatGPT`、`### Example: Claude Code`、`### Example: Codex`、`### Example: Cursor`、`### Example: Antigravity CLI`。**没有任何 Hermes 示例** |
| HAS-M8 | 同上：Codex 示例内的本地回调 client_id | 同上 | 官方文档 | 同 | L239–243 | `oauth = { client_id = "http://127.0.0.1:12345" }`；"The callback port and the port in `client_id` must match. The `client_id` value is the base URL of the local OAuth callback used by Codex; do not replace it with your Home Assistant URL." |
| HAS-M9 | 同上：Cursor 示例（stdio 经 mcp-proxy） | 同上 | 官方文档 | 同 | L255–276 | `"command": "mcp-proxy", "args": ["--transport=streamablehttp","--stateless","http://<…>:8123/api/mcp"], "env": {"API_ACCESS_TOKEN": "<your_access_token_here>"}` |
| HAS-M10 | 同上：Antigravity 示例（header 直连） | 同上 | 官方文档 | 同 | L286–303 | `"serverUrl": "https://<your_home_assistant_url>/api/mcp"`, `"headers": {"Authorization": "Bearer ${HOMEASSISTANT_TOKEN}"}` |
| HAS-M11 | 同上：frontmatter | 同上 | 官方文档 | 同 | L1–19 | `ha_release: 2025.2`、`ha_domain: mcp_server`、`ha_codeowners: ['@allenporter']`、`ha_quality_scale: silver`、`ha_config_flow: true` |

---

## 待确认项 3：`homeassistant-ai/ha-mcp` README 与 Setup Wizard

| 来源 ID | 标题 | URL | 档位 | 日期 | 锚点 | 主张（逐字） |
|---|---|---|---|---|---|---|
| COM-M2 | ha-mcp README | raw.githubusercontent.com/homeassistant-ai/ha-mcp/master/README.md | 一手项目 README | crawl 2026-09-18（README 顶部标注 `Breaking change (v7.3.0)`） | 全文 grep | **README 中 "hermes" 出现次数 = 0**。L176–178 客户端清单原文：`### 🧙 Setup Wizard for 15+ clients` / "**Claude Code, Gemini CLI, ChatGPT, Open WebUI, VSCode, Cursor, and more.**" |
| COM-M3 | 同 README：`/private_<random>` | 同上 | 一手项目 README | 同 | L51 | "For clients on the same network, the server is also reachable directly at `http://<ha-ip>:9584/private_<random>`."（属 **HA-MCP Custom Component / HACS in-process** 模式）；远端走 `https://<your-ha-domain>/api/webhook/<webhook-id>`（本地 `http://<ha-host>:8123/api/webhook/<webhook-id>`） |
| COM-M4 | 同 README：`/readonly` 后缀 | 同上 | 一手项目 README | 同 | L379–403（`### Read-only HTTP connections`） | "Append `/readonly` to the server's HTTP MCP endpoint to restrict that connection to the existing Read Only Mode while other clients keep normal access"；示例 `Normal: https://example.com/private_your_secret` / `Read-only: https://example.com/private_your_secret/readonly`；"OAuth and OIDC connections use the same login/provider: for example, `https://example.com/mcp/readonly`. No additional secret or server is required."；"This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint."；HA webhook 形式 `https://your-ha.example/api/webhook/<webhook-id>/readonly` 需更新版内嵌组件或 Webhook Proxy dev app |
| COM-M5 | 同 README：HACS 组件模式鉴权 | 同上 | 一手项目 README | 同 | L37–56 | "It is the easiest setup in every case, **with no access token to manage**."；"**Optional authentication:** set **Webhook authentication** to `ha_auth` to require a Home Assistant account sign-in **instead of using the secret URL as the credential**."；"an admin-only **HA-MCP** panel appears in the Home Assistant sidebar" |
| COM-M6 | 同 README：app(add-on) 与 Docker 模式鉴权 | 同上 | 一手项目 README | 同 | L65–75、L85–88 | add-on：L75 "Connect your AI client to that URL — **no token or credential setup needed**."；Docker：L85 "run `ghcr.io/homeassistant-ai/ha-mcp` in HTTP mode, pointed at your Home Assistant URL **and a long-lived token**, and connect your client to its secret URL."；L88 "**OIDC authentication:** gate remote access behind an external identity provider (Authentik, Keycloak, Auth0, etc.) **instead of a secret URL** — all authenticated users share the server's Home Assistant credentials." |
| COM-M7 | 同 README：与官方内建 MCP 的定位对比 | 同上 | 一手项目 README | 同 | L263–280 | "Home Assistant ships its own MCP Server integration. It is built on the **Assist** pipeline…"；表格列 Built-in 的 Entity scope = "Only entities exposed to Assist"，ha-mcp = "Everything in Home Assistant"；Create/edit automations / dashboards / traces / helpers / backups 均为 Built-in "No" |
| COM-M8 | 同 README：只跑一种安装 | 同上 | 一手项目 README | 同 | L77（⚠️ 块）、L109（⚠️ 块） | "**Keep two entries for the same server in one client** … is a known cause of connection hangs."；"- **Local stdio (not recommended):** … has known transport issues (#1713)" |
| COM-M9 | **ha-mcp Setup Wizard：确实支持 Hermes Agent** | https://homeassistant-ai.github.io/ha-mcp/setup/ | 一手项目文档（第三方，同一维护方） | crawl 2026-09-18 | client JSON：`{"id":"hermes","name":"Hermes Agent","company":"Nous Research","logo":"/ha-mcp/logos/hermes.png","transports":["stdio","sse","streamable-http"],"configFormat":"yaml","configLocation":"~/.hermes/config.yaml","accuracy":4,"order":21}`；`clientNote`："Run /reload-mcp in an active session after editing the config — Hermes picks up MCP changes without a restart." | **README 无、Setup Wizard 有**——结论：Hermes 是 ha-mcp 的**一等受支持客户端**，只是没写进 README |
| COM-M10 | 同 Setup Wizard：Hermes 专属 YAML 模板 | 同上 | 一手项目文档 | 同 | JS `state.client.id === 'hermes'` 分支 | HTTP：`mcp_servers:\n  home-assistant:\n    url: "${mcpUrl}"`；uvx stdio：`command: "uvx"` / `args: - "ha-mcp@latest"` / `env: HOMEASSISTANT_URL / HOMEASSISTANT_TOKEN`；Docker stdio：`command: "docker"` / `args: ["run","--rm","-i","-v","ha-mcp-data:/home/mcpuser/.ha-mcp","-e","HOMEASSISTANT_URL=…","-e","HOMEASSISTANT_TOKEN=…","ghcr.io/homeassistant-ai/ha-mcp:latest"]` |
| COM-M11 | 同 Setup Wizard：Hermes 鉴权与传输注意事项 | 同上 | 一手项目文档 | 同 | 同上 instructions | header 形式：`headers: { Authorization: "Bearer ${env:HA_TOKEN}" }`；"**Hermes resolves `${env:VAR}` (and `${VAR}`) from `~/.hermes/.env`**, so the token stays out of the config file. For an endpoint that speaks OAuth instead, drop the headers and set `auth: oauth` on the entry."；"Hermes can switch a server to SSE, but the ha-mcp endpoint is **Streamable HTTP only** — it is POST-only and answers an SSE-style pre-flight with **405**."；"Trimming the catalog: `tools.include` / `tools.exclude` on the server entry take exact tool names or globs. **Use the original ha-mcp names (e.g. `ha_get_state`), not the prefixed ones.**" |

**待确认项 3 结论**：README **不含** Hermes；同项目 Setup Wizard **含** Hermes Agent（专属 YAML 模板 + `/reload-mcp` 提示 + `mcp__home_assistant__<tool>` 命名说明）。`/private_<random>` 是 HACS 内嵌组件的直连端口 9584 形式；`/readonly` 是任何 HTTP 端点都可追加的连接级只读后缀，**不是凭证级权限**。

---

## 待确认项 4：`Control Home Assistant` vs `require_admin`

| 来源 ID | 标题 | URL | 档位 | 日期 | 锚点 | 主张（逐字） |
|---|---|---|---|---|---|---|
| HAS-M12 | `source/_integrations/mcp_server.markdown` | 同 HAS-M1 | 官方文档 | 2026-09-09 | L33–40 | `## Configuration options` / "The integration provides the following configuration options:" / `{% configuration_basic %}` **`Control Home Assistant:`** / `description: If MCP clients are allowed to control Home Assistant. Clients can only control or provide information about entities that are exposed to it.` / `{% endconfiguration_basic %}` |
| HAS-M13 | 同上，历史版本核对 | raw…/home-assistant.io/{ac1f6676d, ea0f717fe, 1053179b6}/… | 官方文档（历史快照） | 2026-09-09 / 2026-06-12 / 2026-05-29 | 同一 block | 三个历史快照的 `Configuration options` 块**逐字完全相同** → 该文案长期未变 |
| HAS-M14 | `homeassistant/components/mcp_server/` @ **`master`（=2026.9）** | raw…/home-assistant/core/master/homeassistant/components/mcp_server/{const,config_flow,strings}.{py,json} | **一手源码** | 2026-09 发布分支 | `const.py` 全文；`config_flow.py` L1–70；`strings.json` 全文 | `const.py` 只有 `DOMAIN`、`TITLE`、`STATELESS_LLM_API`——**无 `CONF_REQUIRE_ADMIN`**；`config_flow.py` `VERSION = 1`，无 options flow，无 admin 相关键；`strings.json` 无 `require_admin` |
| HAS-M15 | 同上 @ **`rc`（=2026.9）** | raw…/core/rc/… | 一手源码 | 2026-09 | 同 | 同 `master`：`const.py` 无 `CONF_REQUIRE_ADMIN`、`strings.json` 无 `require_admin`；`http.py` 只有 L328 `if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin:` |
| HAS-M16 | 同上 @ **`dev`（=2026.10）** | raw…/core/dev/homeassistant/components/mcp_server/{const,config_flow,strings,http,__init__}.{py,json} | **一手源码** | dev 分支 | `const.py` L4：`CONF_REQUIRE_ADMIN = "require_admin"`；`config_flow.py` `MINOR_VERSION = 2`、`_options_schema(...)`、`async_step_user` 末 `data={**user_input, CONF_REQUIRE_ADMIN: True}`；options 默认 `self.config_entry.data.get(CONF_REQUIRE_ADMIN, False)`；`strings.json` `"require_admin": "Require an administrator account"` + `data_description` "Only allow administrator accounts to use the Model Context Protocol endpoint."；`http.py` L96–98 `def _validate_admin(...): if entry.data[CONF_REQUIRE_ADMIN] and not request["hass_user"].is_admin: raise Unauthorized`；`__init__.py` `async_migrate_entry` 1.1→1.2：`data={CONF_REQUIRE_ADMIN: False, **entry.data}`，注释 "Endpoints served before this option existed stay open." | **开关确实存在于 dev，但名字/语义都不是 "Control Home Assistant"** |
| HAS-M17 | 同上 @ `dev`：端点级鉴权文案 | raw…/core/dev/…/http.py | 一手源码 | dev | L11–15、L306–310、L326–329 | dev 版 docstring：`/api/mcp` "requires admin access **when the config entry is configured to require it**"；`/api/mcp/<API ID>` "require admin access, except for the Assist API" |
| HAS-M18 | 同上 @ `master` | raw…/core/master/…/http.py | 一手源码 | 2026-09 | L11–15、L297–300 | master 版 docstring：`/api/mcp` "serves the configured LLM APIs and **does not require admin access**"；`ModelContextProtocolStreamableView` docstring 同句 |
| HAS-M19 | core 目录提交史（44 条） | api.github.com/repos/home-assistant/core/commits?path=homeassistant/components/mcp_server&per_page=100 | 一手源码史 | 至 2026-09-13 | `867436ed6` (2026-08-30) | "**Add option to require an admin user for the MCP server endpoint (#180713)**"；另有 `58076228e` (2026-08-30) "Add options flow to MCP Server integration (#180629)"。44 条提交中**没有任何一条**提及新增 control/read-only 类开关 |
| HAS-M20 | 初始版本核对 | raw…/core/a5d0c3528/homeassistant/components/mcp_server/{config_flow.py,strings.json} | 一手源码（历史） | 2025-01-02 | 全文 grep | 首版 `config_flow.py` 只 import/使用 `CONF_LLM_HASS_API`；`strings.json` 无 "control"/"admin" 任何匹配 |

**待确认项 4 结论（事实 / 未定）**
- **事实 1**：官方 markdown 的原文是 `Control Home Assistant:` + `If MCP clients are allowed to control Home Assistant. Clients can only control or provide information about entities that are exposed to it.`（HAS-M12，逐字）。
- **事实 2**：`2026.9` 发布分支（`master` 与 `rc`）**没有**任何 admin 开关——`const.py` 无 `CONF_REQUIRE_ADMIN`、`strings.json` 无 `require_admin`、`http.py` 无 `_validate_admin`，且 docstring 明说 `/api/mcp` "does not require admin access"（HAS-M14/15/18）。
- **事实 3**：`dev`（2026.10）**有**开关，但键是 `require_admin`，UI 文案是 **"Require an administrator account"**，与文档的 "Control Home Assistant" **名称和语义都不同**（HAS-M16）。
- **事实 4**：新装默认 `True`，`1.1→1.2` 迁移条目默认 `False`（"Endpoints served before this option existed stay open"）→ 同版本内两条路径默认值不一致（HAS-M16）。
- **事实 5**：44 条目录提交里从未出现过 "control" 类选项；首版起就只有 `CONF_LLM_HASS_API`（HAS-M19/20）。
- **未定**：文档那句 `Control Home Assistant` 究竟对应什么。它在代码里**没有可对应的键**（无论 master/rc/dev，也无论历史），但三段历史快照逐字未变，说明它是长期存在的文档条目而非近期误改。无法从代码侧判定它是「已删除选项的残留」还是「文档占位/约定写法」。需结合具体 HA 版本（用户实例是 2026.9 还是 2026.10）与 release notes 才能定论。
- 附带存疑（低影响）：代码里 `MORE_INFO_URL = "https://www.home-assistant.io/integrations/mcp_server/#configuration"`，而文档标题是 `## Configuration options`，锚点应为 `#configuration-options`——该 `#configuration` 锚点在文档中不存在。

---

## 矛盾与存疑

1. **Hermes 前缀：三处文档两种写法，源码站定双下划线**。HMS-M1/M3 与 HMS-M8（发布站）为单下划线；HMS-M2 与 HMS-M4（源码 `MCP_TOOL_NAME_PREFIX = "mcp__"`）为双下划线。第三方旁证 COM-M1 亦为双下划线。
2. **过期注释仍在仓库内**：HMS-M6（`anthropic_adapter._normalize_to_mcp_wire` docstring）与 HMS-M7（测试模块 docstring）都还写着旧的 `mcp_<server>_<tool>`——说明这是**部分完成的改名**，不是文档间分歧。
3. **HA 文档 vs 代码**：`Control Home Assistant`（HAS-M12）在任何分支、任何历史版本都没有对应代码键（HAS-M14/15/16/19/20）；dev 上真正的开关叫 `require_admin`（HAS-M16）。**不可把二者当作同一个开关**——名称与语义均不匹配。
4. **HA 同一特性跨分支行为相反**：`/api/mcp` 在 `master`/`rc`(2026.9) 是"不需要 admin"，在 `dev`(2026.10) 变成"按配置可能要求 admin"（HAS-M16/17/18）。写笔记时必须带版本号。
5. **`require_admin` 同版本内默认值不一致**：新装 `True` vs 迁移 `False`（HAS-M16），源码注释自认 "Endpoints served before this option existed stay open"。
6. **ha-mcp 客户端清单口径不一**：README 不含 Hermes（COM-M2），Setup Wizard 含 Hermes 且有专属模板（COM-M9/M10/M11）。README 的 "15+ clients" 与 Wizard 的 `order:21` 条目不同步。

## 未解决项

1. **`hermes mcp test <server>` 是否真的只打印原生名**——依据是源码 `tools_found.append((t.name, desc))`（HMS-M9），未在实机跑过。**实机待验**。
2. **`hermes mcp test` 之外的官方"列出注册名"入口是否存在**——已查 `hermes mcp`/`hermes tools` 全部子命令（HMS-M10）与 dashboard 路由（`/api/mcp/servers/{name}/test` 的 `schema_chars` 亦以原生名为 key），**未找到**；未穷尽桌面端 UI。
3. **用户实机 Hermes 版本号未知**——无法判定其实例处于单下划线还是双下划线时期；`hermes --version` 结果需回填（HMS-M10 有该命令）。
4. **`Control Home Assistant` 的文档来源**——需 HA release notes 或 PR 讨论才能定论；本轮受 API 额度与检索面限制未定。
5. **`require_admin` 是否会在 2026.10 进入正式发布**——`dev` 上有、`rc` 上无，是否会被 revert 未知。
6. **ha-mcp README 未列 Hermes 是有意还是遗漏**——无 issue/PR 证据。
7. **三份 Hermes 文档的 `version`/`last updated` 显示值**——文档站页面上是否标注版本未采集；只能给 git 内容提交时间（HMS-M1 2026-09-17 / HMS-M3 2026-06-21）。
8. **`agent/anthropic_adapter.py` 与 `tests/agent/test_anthropic_mcp_prefix_strip.py` 的最后提交日期**——本轮未取，因此无法给"过期注释"排序。

**已保存原始件**（`D:\Study-Notes\workspace\hermes-home-assistant\sources\`）：`HMS-docs-features-mcp.md`、`HMS-docs-mcp-config-reference.md`、`HMS-docs-use-mcp-with-hermes.md`、`HMS-docs-cli-commands.md`、`HMS-src-tools_mcp_tool_schema.py`、`HMS-src-agent_anthropic_adapter.py`、`HMS-src-hermes_cli_mcp_config.py`、`HMS-test-anthropic_mcp_prefix_strip.py`、`HAS-src-mcp_server.markdown`、`HAS-core-{dev,master}-{config_flow.py,strings.json,http.py,const.py,__init__.py}`、`COM-ha-mcp-README.md`、`COM-ha-mcp-setup-wizard.html`、`01_homeassistant-ai_github_io.md`、`02_hermes-agent_nousresearch_com.md`。

**未复核（遵守参数要求）**：内置 4 个 `ha_*` 工具清单、blocked domains 黑名单、事件白名单机制——`research/probe-02-hermes-tools.md` 已覆盖，本轮未重查。

---

## 新增来源 ID（续编）

| ID | 来源 |
|---|---|
| HMS-M1 | `website/docs/user-guide/features/mcp.md`（前缀写法之一：单下划线，**过期**） |
| HMS-M2 | `website/docs/reference/mcp-config-reference.md`（前缀写法之二：双下划线，**正确**） |
| HMS-M3 | `website/docs/guides/use-mcp-with-hermes.md`（前缀写法之三，**过期**） |
| HMS-M4 | `tools/mcp_tool_schema.py`（**定论源码**：`MCP_TOOL_NAME_PREFIX = "mcp__"`） |
| HMS-M5 | 同文件 L143–148（迁移注释，引 #33533） |
| HMS-M6 | `agent/anthropic_adapter.py`（`_MCP_TOOL_PREFIX`、`_normalize_to_mcp_wire`） |
| HMS-M7 | `tests/agent/test_anthropic_mcp_prefix_strip.py` |
| HMS-M8 | https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp （发布站，仍为旧写法） |
| HMS-M9 | `hermes_cli/mcp_config.py`（`cmd_mcp_test` 打印原生名） |
| HMS-M10 | `website/docs/reference/cli-commands.md`（`hermes mcp` 子命令表、`--version`） |
| HAS-M1..M11 | https://www.home-assistant.io/integrations/mcp_server/ （端点、OAuth IndieAuth、6 个 client 示例、frontmatter `ha_release: 2025.2`） |
| HAS-M12..M13 | 同上（`Control Home Assistant` 文案 + 三段历史快照一致） |
| HAS-M14..M18 | `home-assistant/core` 的 `mcp_server` 组件 @ `master`/`rc`/`dev`（`require_admin` 跨分支差异） |
| HAS-M19 | core 提交史 44 条（`#180713` / `#180629`） |
| HAS-M20 | `mcp_server` 首版（2025-01-02） |
| COM-M1 | https://homeassistant-ai.github.io/ha-mcp/setup/ （命名说明：`mcp__home_assistant__<tool>`） |
| COM-M2..M8 | https://github.com/homeassistant-ai/ha-mcp （README：客户端清单、`/private_`、`/readonly`、各模式鉴权、对比表） |
| COM-M9..M11 | 同 Setup Wizard（**Hermes 受支持**：client JSON、YAML 模板、`${env:VAR}` 解析、Streamable HTTP only、`tools.include` 用原生名） |
