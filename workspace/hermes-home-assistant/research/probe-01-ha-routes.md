# 探测原始记录 01：HA 侧给 LLM Agent 控制 Home Assistant 的路线

> **性质**：原始证据记录，**不是**阶段 1 的交付物 `01_explore_result.md`，不推进任何阶段状态。
> **来源**：后台核验子代理（HA 侧），核对日期 2026-09-18。
> **引用纪律**：本文件内所有「官方口径」在写入正文前必须逐条回源比对；带「待核对」标记的内容不得直接引用。

## 路线 1 | HA 官方 MCP Server 集成（`mcp_server`） | 官方

- 位置：`home-assistant/core` 的 `components/mcp_server`；页面标注 2025.2 引入、IoT class "Local Push"、Silver quality
- 能力边界原文：
  - "Controlling Home Assistant is done by providing MCP clients with access to Home Assistant's Assist API."
  - "The tools used by the configured LLM API are exposed."
  - 支持矩阵："Tools: Supported / Prompts: Supported / Resources: Supported (Assist only) / Sampling: Not supported / Notifications: Not supported"
  - Resource 仅一个且带条件："When the configured LLM API includes the `GetLiveContext` tool" → 暴露 `homeassistant://assist/context-snapshot`
  - 端点 `https://<ha>/api/mcp`，可用 `/api/mcp/<api_id>`（Assist 恒为 `/api/mcp/assist`）
  - 权限："The Assist API stays available to non-administrator users"
- 鉴权：OAuth（IndieAuth）为主；Client ID 应为客户端应用 base URL，"It must never be your Home Assistant instance URL."；也支持 access token
- 配置项含："If MCP clients are allowed to control Home Assistant."（实体仍需 expose 给 Assist）
- 来源：https://www.home-assistant.io/integrations/mcp_server/
- 反向集成是另一页：https://www.home-assistant.io/integrations/mcp/（HA 作 client；仅 Tools 支持，SSE transport）

## 路线 2 | 社区 MCP server 项目（GitHub API 实测快照 2026-09-18）

| 项目 | stars | 许可 | 最后 push | 状态 | 备注 |
|---|---|---|---|---|---|
| `homeassistant-ai/ha-mcp` | 4762 | MIT | 2026-09-17 | 活跃 | README 自述 **87 tools**；含 Read Only Mode 与 per-tool 开关 |
| `voska/hass-mcp` | 342 | MIT | 2026-08-06 | 活跃 | 经 HA WebSocket API；`HA_URL` / `HA_TOKEN` |
| `tevonsb/homeassistant-mcp` | 576 | Apache-2.0 | 2026-01-25 | 滞后 | TypeScript；SSE 实时更新；token + rate limiting |
| `ganhammar/hass-mcp-server` | 69 | MIT | 2026-09-05 | 活跃 | HACS 自定义组件；HTTP transport；OAuth 2.0 + DCR；LLT 可选 |
| `allenporter/mcp-server-home-assistant` | 68 | — | 2025-03-02 | **已归档** | 不再维护 |

- `ha-mcp` 能力（README 表格自述）：`ha_call_service`、`ha_search`、`ha_get_state`、`ha_get_history`、`ha_config_set_automation`、`ha_manage_backup`、`ha_get_entity_exposure` 等
- `ha-mcp` 鉴权：HACS 组件模式 "no access token to manage"；Docker 模式需 URL + LLT；另有 OAuth/OIDC 与 webhook 认证 `ha_auth`
- `voska/hass-mcp` 工具：`get_version` / `get_entity` / `list_entities` / `search_entities_tool` / `list_automations` / `call_service_tool` / `get_history` / `get_statistics` / `get_error_log` / `get_entities_by_area` / dashboard 读写
- `ganhammar/hass-mcp-server` 原文："HTTP transport (not SSE) - works remotely, not just locally"
- 来源：各项目 GitHub 仓库

## 路线 3 | Assist 语音管道 + 内置 LLM conversation agent | 官方

- 暴露实体（控制前置）："To be able to control your devices over a voice command, you must expose your entities to Assist." 路径 Settings > Voice assistants > Expose tab；可分别 expose 给 "Assist, Google Assistant, and/or Alexa"；文档只提供逐实体/多选，**未提按 domain 批量**
- 支持的 LLM 集成：OpenAI Conversation、Anthropic、Google Generative AI（Gemini）、Ollama
- 四条一致的边界原文：
  - "Controlling Home Assistant is done by providing the AI access to the Assist API of Home Assistant."
  - "It can only control or provide information about entities that are exposed to it."
  - 四家均写 "This integration does not integrate with sentence triggers."
  - OpenAI 页另有 "This integration works only with the official OpenAI API endpoint"
- Ollama 独有边界："Controlling Home Assistant is an experimental feature"、"Only models that support Tools may control Home Assistant."、"we recommend exposing fewer than 25 entities"、"Smaller models may not reliably maintain a conversation when controlling Home Assistant is enabled."
- 来源：/integrations/openai_conversation/、/integrations/anthropic/、/integrations/google_generative_ai_conversation/、/integrations/ollama/、/integrations/conversation/、/voice_control/voice_remote_expose_devices/

## 路线 4 | REST API 与 WebSocket API | 官方

REST：

- 鉴权："All API calls have to be accompanied by the header `Authorization: Bearer TOKEN`"；LLT 由前端登录创建；"The API accepts and returns only JSON encoded objects."
- 端点：`GET /api/states`、`GET /api/states/<entity_id>`、`GET /api/services`、`GET /api/events`、`GET /api/history/period/<timestamp>`、`POST /api/services/<domain>/<service>`、`POST /api/template`、`POST /api/intent/handle`、`POST /api/events/<event_type>`、`DELETE /api/states/<entity_id>`
- 服务返回规则："If you don't use `return_response` when calling a service that must return data, the API will return a 400."
- **REST 页通篇无 WebSocket / subscribe / streaming 语句** → 事件只能一次性列举或 fire，不能订阅推送（否定性结论，待核对）
- 来源：https://developers.home-assistant.io/docs/api/rest/

WebSocket：

- "Home Assistant hosts a WebSocket API at `/api/websocket`."
- 鉴权握手："the server sends out `auth_required`" → "The first message from the client should be an auth message." → "You can authorize with an access token"；失败 "the server will reply with `auth_invalid` message and disconnect the session."
- 服务调用 "This will call a service action in Home Assistant." 且 "Right now there is no return value."
- 事件订阅："The command `subscribe_events` will subscribe your client to the event bus."、"You can either listen to all events or to a specific event type."（多类型需多次订阅）；另有 `subscribe_trigger`（"These are the same triggers syntax as used for" 自动化触发器）
- 来源：https://developers.home-assistant.io/docs/api/websocket/

## 待核对（子代理自报，未经二次验证不得引用）

1. 官方 MCP Server 暴露的**具体工具名清单**未能从一手源穷举——页面只点名 `GetLiveContext`，其余取决于所选 LLM API；`subscribe_entities` 在 WebSocket 官方页面未出现
2. "introduced in Home Assistant 2025.2" 来自 docs 页面摘要，未回溯 release notes
3. `ganhammar/hass-mcp-server` README 称官方集成 "supports SSE transport"，与官方页面自述的 Streamable HTTP 表述冲突，未定论
4. `homeassistant-ai/ha-mcp` 的 **87 tools** 为 README 自述，未逐条比对源码实际注册列表；star 数 / push 时间 / 87 均为 2026-09-18 的 GitHub API 快照
5. 各社区项目的"鉴权方式"仅取自 README 文字，未审读代码确认 token 存储与权限降级实现
6. REST/WS "不能订阅" 是从文档无相关语句反推的**否定性结论**，非官方明文；未做源码级核实
7. `community.home-assistant.io` 本次未采用任何论点（仅二次来源）
