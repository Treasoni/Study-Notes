# 探测原始记录 04：HA 权限模型 与 Hermes 侧审批/成本控制

> **性质**：原始证据记录，**不是**阶段 1 的交付物 `01_explore_result.md`，不推进任何阶段状态。
> **来源**：后台核验子代理（权限与成本探测），核对日期 2026-09-18；结论为**源码级核验**或官方文档原文。
> **引用纪律**：写入正文前逐条回源比对；标「待核对」的内容（尤其第 1、2、3、6 条）不得当结论使用。

## 一、HA 权限模型

| # | 结论 | 原文关键句 | 来源 |
|---|---|---|---|
| 1 | **LLT 权限 = 创建它的那个用户** | "Send websocket command auth/long_lived_access_token will create a long-lived access token for current user." / "The access token is used to access the Home Assistant APIs." | `developers.home-assistant.io/docs/auth_api/` + `homeassistant/components/auth/__init__.py`：`hass.auth.async_create_refresh_token(connection.user, ..., token_type=TOKEN_TYPE_LONG_LIVED_ACCESS_TOKEN, ...)` |
| 2 | **token 本身不带 scope claim** | 源码 `async_create_access_token` 只编码 `{"iss": refresh_token.id, "iat": now, "exp": ...}`；`async_validate_access_token` 返回 `models.RefreshToken \| None` | `homeassistant/auth/__init__.py` L599-682 |
| 3 | **权限判定走用户上下文，不走 token** | "These context objects also contain a user id, which is used for checking the permissions." / "The combined permissions of all groups a user is a member of decides what a user can and cannot see or control." | `developers.home-assistant.io/docs/auth_permissions/` |
| 4 | **LLT 无只读 / 单 domain 限制手段** | 三页文档均无 token scope 语句；仅存在**用户/组级**实体粒度策略："Entity permissions can be set on a per entity and per domain basis" + `entity_ids, device_ids, area_ids, domains`（**是用户属性，不是 token 属性**） | auth_api / auth_index / auth_permissions |
| 5 | **non-admin 可以创建 LLT** | 命令装饰器为 `@websocket_api.ws_require_user()`（**非** `@require_admin`）；对照 "If you need to check admin access, you can use the built-in @require_admin decorator." | `components/auth/__init__.py` L519-547 |
| 6 | **Assist expose 粒度 = 逐实体 + 多选批量，无 domain/area 批量** | "To expose multiple entities at once, to all the assistants, select the Expose entities button" / "In the pop-up, select all assistants to which the entity should be exposed to: Assist, Google Assistant, and/or Alexa." | `voice_control/voice_remote_expose_devices/` |
| 7 | **mcp_server 的 "Control Home Assistant" 语义** | "If MCP clients are allowed to control Home Assistant. Clients can only control or provide information about entities that are exposed to it."（**文档未给 YAML 键名**） | `www.home-assistant.io/integrations/mcp_server/` |
| 8 | **mcp_server 对 admin / 非 admin 的差异** | "Connecting to any API other than Assist requires the authenticated user to be an administrator. The Assist API stays available to non-administrator users, just like the base /api/mcp endpoint."；源码 `if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin: raise Unauthorized` | docs + `components/mcp_server/http.py` L338-339 |
| 9 | **吊销与有效期** | "Long-lived access tokens are valid for 10 years." / "Revoking a refresh token will immediately revoke the refresh token and all access tokens that it has ever granted."；可列举/删除：`auth/refresh_tokens`、`auth/delete_refresh_token`、`auth/delete_all_refresh_tokens`（均 `ws_require_user`，`connection.user.refresh_tokens` 只含本人） | `docs/auth_api/` + `auth/__init__.py` L550-609 |

## 二、Hermes 侧审批与成本控制

| # | 结论 | 原文关键句 | 来源 |
|---|---|---|---|
| 1 | **MCP `trust`** | "Trust tier: full (default) or untrusted." / "On an untrusted server, every write-capable tool call (any tool without a readOnlyHint: true annotation) requires user approval through the standard approval surface before it runs." / "Unrecognized values are treated as untrusted (fail-closed)"。**文档从未明写 `full` 会跳过审批** | `docs/reference/mcp-config-reference` |
| 2 | **`readOnlyHint` 只是服务端声明的提示** | "readOnlyHint is a server-supplied hint" / "a lying server can at most skip approval for tools it claims are read-only, never gain extra access" / "mark any server you don't fully control as untrusted" | 同上 |
| 3 | **`tools.include` / `tools.exclude`** | "Whitelist server-native MCP tools. Entries may be exact names or fnmatch-style globs"（例 `*_radar_*`、`get_zones_*`）/ "If include is set, only those server-native MCP tools are registered." / 优先级 "If both are set, include wins." / 过滤用原始名："the original MCP tool name (with hyphens/dots), not the sanitized version" | 同上 |
| 4 | **`cooldown_seconds`（默认 30）是逐实体限流，不是全局** | 源码 `if (now - self._last_event_time.get(entity_id, 0)) < self._cooldown_seconds: return`；类 docstring "...with domain/entity filtering and per-entity cooldowns." | `plugins/platforms/homeassistant/adapter.py` L68-89, L235 |
| 5 | **cron `wakeAgent`** | "When wakeAgent is omitted, the default is true (wake the agent as usual)." / "The wakeAgent gate gives you a $0 way to decide whether a scheduled job should spend any LLM tokens at all." | `docs/user-guide/features/cron`（本地快照 `gaps/05_...cron.md` L1429, L1431） |
| 6 | **cron `no_agent`** | "No tokens, no model, no provider fallback — the job never touches the inference layer." / "Empty stdout → silent tick" / "Non-zero exit or timeout → an error alert is delivered" | 同上 L861-895 |
| 7 | **出站截断：HA 是硬切 4096，不分片** | 源码 `payload = {"title": "Hermes Agent", "message": content[:self.MAX_MESSAGE_LENGTH]}` + `MAX_MESSAGE_LENGTH = 4096`，且**未**设 `splits_long_messages`；基类默认 `splits_long_messages: bool = False`。对比：Telegram 4096/True、Discord 2000/True、Slack 39000/True、Signal 8000/True（**均分片**） | `plugins/platforms/homeassistant/adapter.py` L70, L277, L352；`gateway/platforms/base.py` L1835；`plugins/platforms/{telegram,discord,slack}/adapter.py`、`gateway/platforms/signal.py` |

## 三、待核对

1. **docs 的 "Control Home Assistant" 没有对应代码开关**：`2026.9.0` 的 `mcp_server/config_flow.py` 只有 `CONF_LLM_HASS_API`，无任何 control 布尔；`dev` 分支新增的是 `require_admin`（`strings.json`："Only allow administrator accounts to use the Model Context Protocol endpoint."）。docs 该条是过期描述还是查错分支，**未定论**
2. **`require_admin` 默认值与 docs 冲突**：`async_step_user` 新装写入 `CONF_REQUIRE_ADMIN: True`，而 `async_setup` 的 v1→v2 迁移把旧条目补成 `False`；`_validate_admin` 又在 base `/api/mcp` 视图上调用，与 docs "just like the base /api/mcp endpoint" 存在张力。二者是否在同一版本共存**未定论**
3. **HA 文档从未明文说「token 权限等同创建者用户」**：该结论由 `connection.user` 建令牌 + JWT 无 scope + `hass_user` 反查链条推出，属**源码级推论**而非官方明文
4. **LLT 的 UI 删除路径**：`auth_api` 只有刷新令牌的 `/auth/revoke`；profile 页删除 LLT 的官方语句未找到（文档未涉及）
5. **LLT 轮换（rotation）机制**：全部一手源均无（文档未涉及）；只有 lifespan 参数与删除命令
6. **`full` 是否等于「完全不审批」**：docs 只标 `(default)`，未写行为，属反向推论
7. **审批被拒 / 超时的后果**：docs 未涉及
8. **Telegram 入站截断**：搜索称接收路径无 `MAX_MESSAGE_LENGTH` 限制，来源为第三方技能页与 PR 描述，未回一手源
9. **`notify.notify` 与 `persistent_notification` 的分支触发条件**（probe-02 待核对第 5 条）本轮未核，仍待定
