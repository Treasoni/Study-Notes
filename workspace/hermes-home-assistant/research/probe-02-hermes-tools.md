# 探测原始记录 02：Hermes 侧 HA 工具、平台适配器、skill / MCP / 自定义工具

> **性质**：原始证据记录，**不是**阶段 1 的交付物 `01_explore_result.md`，不推进任何阶段状态。
> **来源**：后台核验子代理（Hermes 侧），核对日期 2026-09-18；事实来自官方仓库一手源文件 + 官方文档站。
> **重要前提**：本地语料 `workspace/hermes-agent/research/` **不含 HA 专页**，仅有零散提及（cron 投递目标 `"homeassistant"`、`hermes skills install official/<category>/<skill>` 语法）。以下 HA 事实**无法用本地语料二次印证**。
> **引用纪律**：写入正文前逐条回源比对；带「待核对」标记的内容不得直接引用。

## 1. HA 工具集：只有 4 个，没有第 5 个

| 项目 | 事实（原文） | 来源 |
|---|---|---|
| 工具总数 | 只有 4 个。源码 docstring："Registers ``ha_list_entities``, ``ha_get_state``, ``ha_list_services``, ``ha_call_service``." | `tools/homeassistant_tool.py` |
| 无 area/device 维度工具 | 无 `ha_list_areas` / `ha_list_devices`；area 只是 `ha_list_entities` 的一个参数 | 同上 |
| 无历史查询工具 | 无 history/logbook 工具；`ha_get_state` 只返回当前 state | 同上 |
| 无模板渲染工具 | 无 `ha_render_template`；工具全部走 REST `/api/`，不含 `/api/template` | 同上 |
| 工具集定义 | "`homeassistant` \| `ha_call_service`, `ha_get_state`, `ha_list_entities`, `ha_list_services` \| Smart home control via Home Assistant. Only available when `HASS_TOKEN` is set." | `website/docs/reference/toolsets-reference.md` |
| 启用条件（gating） | `def _check_ha_available() -> bool: """Tool is only available when HASS_TOKEN is set.""" return bool(get_secret("HASS_TOKEN"))` | `tools/homeassistant_tool.py` |
| 注册调用真实签名 | `registry.register(name=_schema["name"], toolset="homeassistant", schema=_schema, handler=_handler, check_fn=_check_ha_available, emoji="🏠")` | 同上 |
| `ha_list_entities` 参数 | `domain`(optional) / `area`(optional)；`"required": []` | 同上 |
| `area` 的真实语义 | 不是 HA area registry，而是 "area matches friendly_name or area attr" | 同上 |
| `ha_get_state` | `entity_id`，`"required": ["entity_id"]`；返回 "state, all attributes, last changed/updated timestamps" | `tools/homeassistant_tool.py` + `website/docs/user-guide/messaging/homeassistant.md` |
| `ha_list_services` | `domain`(optional)，`"required": []` | 同上 |
| `ha_call_service` | `domain` + `service` 必填，`entity_id`、`data` 可选 | 同上 |
| `data` 兼容字符串 | "XML tool-calling mode delivers data as a JSON string"，代码会 `json.loads` 回退 | 同上 |

## 2. 安全边界（现有笔记 06 未覆盖）

- entity_id 校验：`_ENTITY_ID_RE = re.compile(r"^[a-z_][a-z0-9_]*\.[a-z0-9_]+$")`
- domain/service 校验：`_SERVICE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")`；注释："only [a-z0-9_] is allowed: anything else enables SSRF via path traversal"
- 校验顺序："Format check BEFORE the blocklist: rejects `shell_command/../light` style bypasses."
- **blocked domains**：`frozenset({"shell_command","command_line","python_script","pyscript","hassio","rest_command"})`，逐项带原因注释（如 hassio："addon control, host shutdown/reboot, stdin to containers"）

## 3. 平台适配器（events 入站 / 卡片出站）

| 项目 | 事实 | 来源 |
|---|---|---|
| `extra` 全部配置项 | 只有 5 个 + 1 个未文档化 url：`extra.get("url")` / `watch_domains` / `watch_entities` / `ignore_entities` / `watch_all` / `cooldown_seconds`。无事件消息格式配置 | `plugins/platforms/homeassistant/adapter.py` |
| `extra.url`（文档未列） | `extra.get("url") or _get_scoped_secret("HASS_URL","http://homeassistant.local:8123")` | 同上 |
| token 优先级 | `config.token or _get_scoped_secret("HASS_TOKEN","")` —— `platforms.homeassistant.token` 优先于环境变量（YAML 键名待核对） | 同上 |
| watch_all 默认 / cooldown 默认 | `bool(extra.get("watch_all", False))`；`int(extra.get("cooldown_seconds", 30))` | 同上 |
| 过滤优先级 | `if entity_id in self._ignore_entities: return False` → 再看 watch_domains/watch_entities → 否则 `return self._watch_all` | 同上 |
| 启动告警原文 | "No watch_domains, watch_entities, or watch_all configured. All state_changed events will be dropped." | 同上 |
| 事件去重 | `if old_val == new_val: return None` —— 状态值未变不发消息 | 同上 |
| 事件文案模板（精确字符串） | `"[Home Assistant] {name}: changed from {old}{unit} to {new}{unit}"`(sensor)；`"[Home Assistant] {name}: turned {on_off}"`(light/switch/fan)；`"[Home Assistant] {name}: {new_trig} (was {old_trig})"`(binary_sensor)，`_TRIGGERED = ("cleared","triggered")`；climate 模板含 `"(current: {temp}, target: {target})"`；默认模板含 entity_id | 同上 |
| 事件如何投递给 agent | `await self.handle_message(MessageEvent(text=message, message_type=MessageType.TEXT, source=source, ...))`，source 为 `build_source(chat_id="ha_events", chat_name="Home Assistant Events", chat_type="channel", user_id="homeassistant", user_name="Home Assistant")` | 同上 |
| 出站消息 | `send()` POST 到 `/api/services/persistent_notification/create`，payload `{"title": "Hermes Agent", "message": content[:4096]}`；注释 "REST rather than the WebSocket, to avoid racing the listener loop" | 同上 |
| cron 无进程投递 | `_standalone_send()` 走 `/api/services/notify/notify`，payload `{"message": message, "target": chat_id}` | 同上 |
| 连接管理 | `_BACKOFF_STEPS = [5, 10, 30, 60]`；`ws_connect(f"{ws_url}/api/websocket", heartbeat=30, timeout=30)` | 同上 |
| plugin 元数据 | `name: homeassistant-platform` / `kind: platform` / `requires_env: HASS_TOKEN` / `optional_env: HASS_URL` | `plugins/platforms/homeassistant/plugin.yaml` |
| 环境变量文档 | "`HASS_TOKEN` \| Home Assistant Long-Lived Access Token (enables HA platform + tools)"；"`HASS_URL` \| Home Assistant URL (default: `http://homeassistant.local:8123`)" | `website/docs/reference/environment-variables.md` |
| 平台键名 | 合法 platform key 含 `homeassistant`；cron 投递目标表含 `"homeassistant"` | `website/docs/user-guide/configuration.md`、本地语料 `gaps/05_...cron.md` |
| 不支持流式编辑 | "Platforms that don't support message editing (Signal, Email, Home Assistant) are auto-detected" | `website/docs/user-guide/configuration.md` |

## 4. toolset 差异与开关

- "`hermes-acp` \| Drops ... all four Home Assistant tools ..."
- "`hermes-homeassistant` \| Same as `hermes-cli` (the Home Assistant tools are already present by default and activate when `HASS_TOKEN` is set)."
- "Capability-gated tools (browser, `computer_use`, `code_execution`, Feishu, Home Assistant, cronjob) appear only when their backend/credential prerequisite is configured."（`all` 通配**不**启用 HA）
- 会话内开关：`/tools list`、`/tools disable browser`、`/tools enable homeassistant`；另 `hermes tools`（curses UI）、`hermes chat --toolsets all`
- 来源：`website/docs/reference/toolsets-reference.md`

## 5. MCP 路线（官方支持）

| 项目 | 事实 | 来源 |
|---|---|---|
| 配置入口 | "Hermes reads MCP config from `~/.hermes/config.yaml` under `mcp_servers`."；stdio 用 `command`/`args`/`env`，远程用 `url`/`headers` | `website/docs/user-guide/features/mcp` |
| CLI | `hermes mcp add <name> [--url URL] [--command CMD] [--auth oauth\|header] [--args ...]`、`remove` / `list` / `test <name>` / `configure <name>` / `login <name>` / `catalog` / `install <name>` | `website/docs/reference/cli-commands.md` |
| MCP ↔ toolset 关系 | "Each configured MCP server generates a `mcp-<server>` toolset at runtime."；同名不遮蔽："If a server is named like a built-in toolset (`homeassistant`, `browser`), that name resolves to the built-in tools **plus** the server's tools" | `website/docs/reference/toolsets-reference.md` |
| 权限审批 | `trust: full`（默认）/ `untrusted`："On an `untrusted` server, every write-capable tool call ... requires user approval through the standard approval surface"；`readOnlyHint` 仅为 hint | `website/docs/reference/mcp-config-reference.md` |
| 工具过滤 | `tools.include` / `tools.exclude`（支持 fnmatch glob）；"If both are set, `include` wins." | 同上 |
| 排错 | `/reload-mcp`；`hermes mcp test <name>`；`hermes mcp login <server>`；`uv pip install -e ".[mcp]"` | `website/docs/guides/use-mcp-with-hermes.md` |

## 6. Skills Hub：**没有 Home Assistant skill**

- 全部 bundled + optional skill 列表中，smart-home 类只有 1 个：`openhue`（"Control Philips Hue lights, scenes, rooms via OpenHue CLI."）
- **不存在 Home Assistant skill**
- 来源：`skills/`、`optional-skills/smart-home/openhue/SKILL.md`、`website/docs/user-guide/skills/optional/smart-home/smart-home-openhue.md`

skill 命令真实语法（`website/docs/reference/cli-commands.md`）：

```bash
hermes skills search react --source skills-sh
hermes skills install official/migration/openclaw-migration
hermes skills install skills-sh/anthropics/skills/pdf --force
hermes skills inspect official/security/1password
hermes skills browse --source official
```

- skill source 取值：`official` / `skills-sh` / `well-known` / `browse-sh`（+ 直接 `https://….md` URL）

## 7. 自定义工具：plugin 优先，不改仓库

- "Default to plugins for most custom tool creation."；core 路线需改仓库："This page is for adding a **built-in Hermes tool** to the repository itself."（`website/docs/developer-guide/adding-tools.md`）
- plugin 最小示例：目录 `~/.hermes/plugins/<name>/`（`plugin.yaml` + `__init__.py`）
  `def register(ctx): ... ctx.register_tool(name="hello_world", toolset="hello_world", schema=schema, handler=handle_hello)`
  （`website/docs/user-guide/features/plugins.md`）
- core 工具注册契约：2 文件 `tools/your_tool.py` + `toolsets.py`；`registry.register(name=, toolset=, schema=, handler=, check_fn=, requires_env=[])`；"Handlers **MUST** return a JSON string"；有顶层 `registry.register()` 的文件自动发现

## 待核对（子代理自报，未经二次验证不得引用）

1. HA 工具走 REST 的端点细节：源码只给 `/api/services/{domain}/{service}` 与 states 列表，具体 list/get 路径未逐条核验
2. MCP 工具命名前缀三处不一致：官方 MCP 页写 `mcp_<server_name>_<tool_name>`，toolsets 参考页写 `mcp__<server>__*`，use-mcp 指南示例为 `mcp_chrome_devtools_win_list_pages` —— 未定论
3. `platforms.homeassistant.token` 键：源码读 `config.token`，官方页只讲 `HASS_TOKEN`，YAML 键名未文档化确认
4. HA 工具是否走审批面：`tools/approval_floors.py`、`tools/approval_detection.py` 中未检索到 `ha_*` / `homeassistant` 引用，是否在别处列为需审批未验证
5. `notify.notify` 独立发送的触发条件（何时用 adapter.send vs `_standalone_send`）文档未说明，仅见源码注释
6. `display.platforms.homeassistant.tool_progress` 等 display 覆盖存在但未核验 HA 是否有额外 display 专属项
7. `hermes mcp add --preset codex` 出现在官方 MCP 页，但 `cli-commands.md` 的 `hermes mcp` 表未列 `--preset`，语法未交叉验证
8. 本地语料未覆盖：`research/` 与 `gaps/` 下没有 Home Assistant 专页，本次 HA 事实**无法用本地语料二次印证**
