## 第一章：结论先行与能力地图——4 个内置工具的天花板

你的 Hermes 已经连上 Home Assistant 了：`HASS_TOKEN` 配好，会话里四个 `ha_*` 工具能正常调用。但从这一步往下，最常见的误解是「既然连上了，让它干点什么只是提示词写得好不好的问题」。这一章要回答的不是「怎么调这四个工具」——那件事已经在既有笔记 06 里做完了——而是另一个问题：**在不动任何配置的前提下，这四个工具究竟能把你带到哪儿，从哪一步开始必须换一条路走**。答案会决定你后面八章该怎么读。

### 1.1 三条结论先行

先把结论摆出来，后面各节只是它们的证据。

**结论一：能做什么由路线决定，不由「接入成功」决定。**

「接入成功」这四个字的准确含义，在源码里其实只有一句话（`tools/homeassistant_tool.py`，SRC-01）：

```python
# tools/homeassistant_tool.py
def _check_ha_available() -> bool:
    """Tool is only available when HASS_TOKEN is set."""
    return bool(get_secret("HASS_TOKEN"))
```

它是一个**通道开关**，不是能力清单。你能做的事，等于这四个工具各自封装的 HA REST 端点之和——整份源码里出现的路径一共四条：`/api/states`、`/api/states/{entity_id}`、`/api/services`、`/api/services/{domain}/{service}`（SRC-01）。除此之外的 HA 能力，无论它在 HA 里多么成熟，对这四个工具来说都不存在。

落一个具体例子。你问 agent「客厅温度过去 24 小时的最高值是多少」，它手上能做的最接近的动作是 `ha_get_state(entity_id="sensor.living_room_temperature")`，返回的是这样一份东西：

```json
{
  "entity_id": "sensor.living_room_temperature",
  "state": "23.4",
  "attributes": {
    "unit_of_measurement": "°C",
    "device_class": "temperature",
    "friendly_name": "客厅温度"
  },
  "last_changed": "2026-09-18T09:12:03.221000+00:00",
  "last_updated": "2026-09-18T09:12:03.221000+00:00"
}
```

注意到问题在哪了吗——这里唯一的数值是「现在的 23.4」。缺的不是推理能力，是**数据本身**：24 小时的时间序列根本没有被取回来。所以这类需求的解法不是换提示词、不是换模型，而是换路线。

**结论二：Hub 里有可装的 HA skill——但可装不等于能补能力。**

两层依据。第一层是范围核对：**official 支**（Hermes 仓库内的 optional skills）的 smart-home 分类下只有一个条目，是 `openhue`——原文描述为 “Control Philips Hue lights, scenes, rooms via OpenHue CLI.”；bundled skills 目录里连 smart-home 这个分类都还没有；而技能系统的说明页 `website/docs/user-guide/features/skills.md`（HMS-05）全文未出现 Home Assistant。但这三条说的都只是 `official` 这一支：HMS-05 自己写着，Hub 的搜索由一份**联邦索引**回答，覆盖 `official` 之外的外部注册表（skills.sh、ClawHub、LobeHub、browse.sh、well-known 端点、GitHub taps），`official`（Hermes 仓库内的 optional/bundled skills）只是其中一支——「Hub 里只有 `openhue` 一个」这句话，说的只是它。

第二层是更根本的原因，这里只点一句、第 3 章展开：**skill 不是能力，是知识**。它教 agent 怎么调已有的工具，不新增工具；而 HA 场景**有**可调的 CLI——`hass-cli` 指的是 `home-assistant-ecosystem/home-assistant-cli`，**Home Assistant Ecosystem 组织**维护的命令行工具，是社区里的事实标准，**不是 HA core 官方出品**（Hub 里 `clawhub/homeassistant-cli` 条目的自述称其为 “official”，措辞不精确，本册不沿用）；Hub 里也**有**封装它的 skill（`clawhub/homeassistant-cli`）。所以这条路的准确说法不是「搜不到」，而是「搜得到、装得上，但装完仍然**不提供新能力**」。

> [!tip] 大白话
> 把 skill 想成一份「岗位说明书」：它告诉你现有这几台机器怎么操作，但不会凭空给你添一台新机器。机器有（`hass-cli`），说明书得自己找——Hub 里有；但说明书再全，机器还是那几台。

**结论三：社区 ha-mcp 的 Setup Wizard 已经把 Hermes 列为受支持客户端——但它自己的 README 里没提。**

这一条是给结论二做对照用的：外部生态对 Hermes 的支持，可能比 Hermes 自己的文档走得更快。

- **向导侧算一等公民**（COM-23）。`ha-mcp` 的 Setup Wizard 客户端列表里有独立的一项 “Hermes Agent / Nous Research”，配置位置 `~/.hermes/config.yaml`；生成配置的代码里有一段以 `state.client.id === 'hermes'` 开头的专属分支（因为 Hermes 的 `mcp_servers` 是按 server 名做键的映射，与其他客户端的列表结构不同形），并且附了一整块 “Hermes Notes”，内容包括工具名形态 `mcp__home_assistant__<tool>`、`tools.include` / `tools.exclude` 要写**原始**工具名、以及改完配置后在会话里跑 `/reload-mcp`。这份照料程度，比它对多数客户端的通用模板要细。
- **README 侧不算**（COM-01）。`ha-mcp` 仓库的 README 全文**零次**出现 “Hermes”。它的客户端清单里没有 Hermes。
- 顺带留一个埋点：向导给 Hermes 声明的传输列表是 `["stdio","sse","streamable-http"]`，可向导自己的说明又写着 ha-mcp 端点是 Streamable HTTP only、切 SSE 会吃到 405。同一个页面对同一件事的两种说法——这类现象第 8 章会成建制地处理。

所以准确的写法是「**受支持，但 README 未列**」，而不是「官方支持 Hermes」。这个区别在你按文档排错时很重要：跟着向导走能跑通，跟着 README 找 Hermes 会一无所获。

### 1.2 你现在的起点：4 个内置工具

内置的 HA 工具**恰好四个**，一个不多一个不少。源码 docstring 的原文是一行枚举：“Registers ``ha_list_entities``, ``ha_get_state``, ``ha_list_services``, ``ha_call_service``.”（SRC-01）

| 工具 | 参数 | 必填 | 它事实上能做什么 |
|---|---|---|---|
| `ha_list_entities` | `domain`、`area` | 无 | 列出实体及其实时状态与 friendly_name |
| `ha_get_state` | `entity_id` | `entity_id` | 取单个实体的当前 state 与全部 attributes |
| `ha_list_services` | `domain` | 无 | 列出可调用的 service 及其参数 |
| `ha_call_service` | `domain`、`service`、`entity_id`、`data` | `domain`、`service` | 调用一个 service 去控制设备 |

这四个工具的注册是同一段循环做的，源码长这样（SRC-01）：

```python
# tools/homeassistant_tool.py
for _schema, _handler in (
    (HA_LIST_ENTITIES_SCHEMA, lambda args, **kw: _dispatch(
        _async_list_entities(domain=args.get("domain"), area=args.get("area")),
        "ha_list_entities", "Failed to list entities")),
    (HA_GET_STATE_SCHEMA, _handle_get_state),
    (HA_LIST_SERVICES_SCHEMA, lambda args, **kw: _dispatch(
        _async_list_services(domain=args.get("domain")), "ha_list_services", "Failed to list services")),
    (HA_CALL_SERVICE_SCHEMA, _handle_call_service)):
    registry.register(
        name=_schema["name"], toolset="homeassistant", schema=_schema, handler=_handler,
        check_fn=_check_ha_available, emoji="🏠")
```

循环体只有四项。这就是全部。

**启用开关条件**也是三处一致的：

- 工具侧：`check_fn=_check_ha_available`，即上面那段 `bool(get_secret("HASS_TOKEN"))`（SRC-01）。
- 文档侧：`homeassistant` toolset 一行写着 “Smart home control via Home Assistant. Only available when `HASS_TOKEN` is set.”；`hermes-homeassistant` 这个 toolset 名“Same as `hermes-cli` (the Home Assistant tools are already present by default and activate when `HASS_TOKEN` is set).”（HMS-03）
- 反向也成立：`hermes-acp` 会 “Drops … all four Home Assistant tools”；而 “Capability-gated tools (browser, `computer_use`, `code_execution`, Feishu, Home Assistant, cronjob) appear only when their backend/credential prerequisite is configured.”——注意这句的言下之意：`--toolsets all` 这类通配**不会**把 HA 工具打开（HMS-03）。会话里想临时开关，走 `/tools enable homeassistant`。

> [!tip] 大白话
> 把 `HASS_TOKEN` 想成一张门禁卡，这四个工具就是这张卡能刷开的四扇门：查房间列表、看某个房间的现状、看有哪些操作可做、执行一个操作。卡是真的，门也是真的——但走廊尽头那扇写着「历史数据」「改配置」「看摄像头」的门，不在这张卡的授权清单里。你再用力刷也不会开，要找的是另一张卡。

**与既有笔记 06 的分工**：`AI学习/Hermes Agent/Hermes Agent 上手实战/06-多平台接入与定时任务.md` 的「Home Assistant：智能家居双向接入」一节已经讲完了 LLT 怎么建、`HASS_TOKEN`/`HASS_URL` 怎么填、这四个 `ha_*` 工具各自的**用法与调用示例**、`watch_domains` 白名单怎么写、以及事件转发默认全关这个事实。本章不重述其中任何一条，只引用它的结论。本章的增量是**天花板**：这四个工具之外还有什么，以及为什么那些东西补不进来。

### 1.3 三类能力缺口

把上一节的四条 REST 路径当作分母，缺口就很好定位了。下表的「场景」列直接取自 P1 阶段那份场景探测表（`research/probe-03-scenarios.md`）的行名，本章末尾的清单会用到同一批行名。

| 缺口 | 对应场景（probe-03 行名） | 4 工具为什么做不到 |
|---|---|---|
| 历史与统计 | 结合传感器历史的建议；异常告警（LLM 学基线，而非阈值） | 四个工具里没有历史/统计端点，`ha_get_state` 只给当前值 |
| 写配置即自动化 | 自然语言生成并注册自动化 | 没有配置类端点；`ha_call_service` 只能触发已存在的对象 |
| 摄像头 / 结构化 AI 任务 | 结构化数据 / 摄像头判断；对话式建议按钮 | 参数模型里没有「附件 / 媒体」这个概念，图像进不来 |

**第一类：历史与统计。** 4 工具能取回的永远是一个**时间点**，不是一段时间。缺口的 HA 侧对应机制是 recorder 的长期统计——`recorder.get_statistics`，官方描述为 “Retrieves long-term statistics for one or more entities.”。要让 agent 回答「上周客厅最高温多少」，它至少需要七天连续样本；而在内置路径下它能拿到的只有「现在 23.4 °C」这一个数。这不是精度差别，是**零和一**的差别。

**第二类：写配置。** 这里有一个容易被误判的细节：`automation` 这个 domain 并不在源码的黑名单里（黑名单见 1.4），所以 `ha_call_service` 可以把它传进去。但那个调用触发的是**已经存在**的自动化对象；「新建一条自动化」这个动作在内置工具里没有任何表达方式——四个工具全部指向状态与服务，没有一个指向配置。

**第三类：摄像头与结构化 AI 任务。** camera 实体在 `/api/states` 里的样子是一个普通字符串（比如 `idle`），图像本身不在返回载荷里。所以「让 agent 看一眼门口有没有人」这类需求，在内置路径下连原料都取不到。HA 侧对应的机制是 AI Task 集成（`ai_task.generate_data`），它可以在自动化、脚本、模板实体里直接调 AI 并带结构化的输出约束——注意这条路是 **HA 调 AI**，不是 Hermes 调 HA，方向正好相反，第 2 章会专门讲这个方向差异。

> [!tip] 大白话
> 这三类缺口可以类比成三种「不在授权清单上」的操作：查档案（历史数据在另一个柜子里，门禁卡没这个权限）、改规则（你能按现有的按钮，但没法改按钮背后连的是什么）、看图（摄像头画面的传输通道压根没接进来）。共同点是——它们都不是「模型不够聪明」，而是「通道里没有这条线」。

### 1.4 硬防线：blocked domains、`area` 语义、4096 截断

这一节讲三处「源码里写死、但笔记 06 没覆盖」的边界。前两处是你今天就会撞上的，第三处本章只埋点。

**blocked domains：六个常量。** `ha_call_service` 在真正发请求之前会过一道黑名单，定义是这样的（SRC-01）：

```python
# tools/homeassistant_tool.py
# Domains that allow arbitrary code/command execution on the HA host or SSRF on the
# local network. HA has zero service-level access control; all safety lives here.
_BLOCKED_DOMAINS = frozenset({
    "shell_command",    # arbitrary shell commands as root in HA container
    "command_line",     # sensors/switches that execute shell commands
    "python_script",    # sandboxed but can escalate via hass.services.call()
    "pyscript",         # scripting integration with broader access
    "hassio",           # addon control, host shutdown/reboot, stdin to containers
    "rest_command",     # HTTP requests from HA server (SSRF vector)
})
```

| 被挡下的 domain | 源码给的理由（逐字） |
|---|---|
| `shell_command` | arbitrary shell commands as root in HA container |
| `command_line` | sensors/switches that execute shell commands |
| `python_script` | sandboxed but can escalate via `hass.services.call()` |
| `pyscript` | scripting integration with broader access |
| `hassio` | addon control, host shutdown/reboot, stdin to containers |
| `rest_command` | HTTP requests from HA server (SSRF vector) |

上面那段注释里最要紧的是最后半句：“HA has zero service-level access control; all safety lives here.”——HA 的服务层本身不做访问控制，所以这道黑名单是仅有的那道闸。

**校验顺序同样是防线的一部分**，源码注释写得很直白：`# Format check BEFORE the blocklist: rejects "shell_command/../light" style bypasses.` 顺序具体是这样：

```python
# tools/homeassistant_tool.py
# Domain/service names are interpolated into /api/services/{domain}/{service}, so only
# [a-z0-9_] is allowed: anything else enables SSRF via path traversal
# (domain="../../api/config") or blocklist bypass (domain="shell_command/../light").
_SERVICE_NAME_RE = re.compile(r"^[a-z][a-z0-9_]*$")

def _handle_call_service(args: dict, **kw) -> str:
    domain = args.get("domain", "")
    service = args.get("service", "")
    if not domain or not service:
        return tool_error("Missing required parameters: domain and service")
    # Format check BEFORE the blocklist: rejects "shell_command/../light" style bypasses.
    if not _SERVICE_NAME_RE.match(domain):
        return tool_error(f"Invalid domain format: {domain!r}")
    if not _SERVICE_NAME_RE.match(service):
        return tool_error(f"Invalid service format: {service!r}")
    if domain in _BLOCKED_DOMAINS:
        return tool_error(
            f"Service domain '{domain}' is blocked for security. "
            f"Blocked domains: {', '.join(sorted(_BLOCKED_DOMAINS))}")
```

为什么顺序不能反？代入具体值就清楚了。假设黑名单先跑：你传 `domain="shell_command/../light"`，它和集合里的六个字符串**一个都不相等**，黑名单直接放行；随后这个字符串被拼进 `/api/services/shell_command/../light`，路径穿越归一化之后实际打到的就是 `shell_command`。反过来先跑格式校验：这个值含 `/` 和 `.`，不匹配 `^[a-z][a-z0-9_]*$`，第一步就被拒。同一份黑名单，仅仅调换两行的位置，效果就从「形同虚设」变成「真的挡得住」。

> [!tip] 大白话
> 黑名单像门口保安手里那张「禁止入内」的名单。但光有名单不够——有人可以报个假名字：“我是张三（顺带一提，我不是李四）”，名单上查不到就放进去了。所以保安的做法是**先验身份证格式**（只允许字母数字下划线），格式不对的当场拦下，格式对的才去对名单。先验格式后对名单，这两步的顺序就是防线本身。

**`ha_list_entities` 的 `area` 参数：它不查 HA 的 area registry。** 这是四个工具里最容易用错的一处。工具 schema 里对它的描述是 “Area/room name to filter by (e.g. 'living room', 'kitchen'). Matches against entity friendly names.”；实现处的 docstring 稍微补全了一点：`area matches friendly_name or area attr`。落到代码上是两次字符串包含判断（SRC-01）：

```python
# tools/homeassistant_tool.py
def _filter_and_summarize(states: list, domain: Optional[str] = None, area: Optional[str] = None) -> Dict:
    """Filter raw HA states by domain/area (area matches friendly_name or area attr) and compact them."""
    if area:
        area_lower = area.lower()
        states = [
            s for s in states
            if area_lower in (s.get("attributes", {}).get("friendly_name", "") or "").lower()
            or area_lower in (s.get("attributes", {}).get("area", "") or "").lower()]
```

把这段和上一节的路径拼起来，结论就很硬了：这个参数是在**已经取回的 `/api/states` 结果里做子串匹配**，它从来没有去问过 HA 的 area registry。

代入一个具体实体。你在 HA 里把 `light.ceiling_1` 的 area 设成「Living Room」，它的 friendly_name 是 “Ceiling 1”。现在调 `ha_list_entities(area="living room")`：取回的 state 里 friendly_name 是 “Ceiling 1”，不含 “living room”；`attributes` 里也没有 `area` 这个键——按 HA 的数据模型，area 属于实体注册表而不是状态属性。两次包含判断全部落空，这个实体**不会出现在结果里**，而你不会收到任何报错，只会看到一个少了几项的列表。可行的写法是改用 `domain="light"` 过滤，或者把房间名写进实体命名里。

这里顺带标注一下性质：源码确实写了 friendly_name 与 `area` 属性两路匹配，但「标准 HA 的 `/api/states` 通常不返回 `area` 属性、因此后半路多数时候取不到值」这一句，是**按 HA 数据模型做的推论**，源码本身没有这句话。

**4096 硬截断（本章只埋点）。** 第三处边界在出站方向。HA 通道给消息设了一个上限常量，发送时直接切片（`plugins/platforms/homeassistant/adapter.py`，SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
class HomeAssistantAdapter(...):
    MAX_MESSAGE_LENGTH = 4096
    ...
    async def send(self, ...):
        """Send a notification via HA REST API (persistent_notification.create)."""
        url = f"{self._hass_url}/api/services/persistent_notification/create"
        payload = {"title": "Hermes Agent", "message": content[:self.MAX_MESSAGE_LENGTH]}
```

关键在于这是 `content[:MAX_MESSAGE_LENGTH]`——**切片，不是分片**。超过 4096 的部分被直接丢弃，没有报错、没有截断标记、也不会自动改发第二条。平台基类里对应的开关默认是关的（`splits_long_messages: bool = False`，SRC-10），HA 适配器没有覆写它。所以一份 6000 字的巡检日报走 HA 通道时，你看到的将是一个看起来完整、实则少了一截的列表。

> [!tip] 大白话
> 把出站消息想成一张写着字数上限的便签纸。写满了不是换第二张纸接着写，而是**从第 4096 个字往后直接剪掉**——没人提醒你，你只会发现日报到一半就没了结尾。哪条分支会走这个通道、以及怎么绕开它，是第 6 章的正题。

### 1.5 落点清单

把 1.3 的三类缺口和 1.2 的四工具能力叠在一起，就得到本章的产物：一张「场景 × 该怎么走」的能力缺口清单。场景名逐条取自 `research/probe-03-scenarios.md` 的场景表（**共 15 行**），判定列是本章的结论。

| # | 场景（probe-03 表内名称） | 需要什么能力 | 判定 |
|---|---|---|---|
| 1 | 语音控制（Assist） | HA：Assist 管道 + 实体暴露 + conversation agent | ➖ HA 侧路线 |
| 2 | 自然语言控制与批量操作 | `ha_call_service` + HA 的 `target` 批量语义 | ✅ 4 工具内 |
| 3 | 事件驱动的主动响应 | 入站白名单 + 动作落 `ha_call_service` | ✅ 4 工具内（入站见笔记 06 与第 6 章） |
| 4 | HA 自己发起对话（官方对照路线） | HA 2025.7 起的能力 + conversation agent | ➖ HA 侧路线 |
| 5 | 日报与巡检 | 读：`ha_list_entities` / `ha_get_state`；投递走平台通道 | ✅ 4 工具内（投递见第 6 章） |
| 6 | 日报（无 LLM 的对照实现） | HA：service response data + 自动化 | ➖ 本来就该用自动化 |
| 7 | 异常告警（电池 / 漏水 / 离线） | HA：Alert 集成 + `numeric_state` 触发器 | ➖ 本来就该用自动化 |
| 8 | 异常告警（LLM 学基线，而非阈值） | 七天历史基线（z-score） | 🔁 换路线（历史） |
| 9 | 场景联动（离开家 / 回家） | HA：`zone` 触发器 | ➖ 本来就该用自动化 |
| 10 | 跨平台遥控（手机 IM 遥控家居） | 平台适配器 + `ha_call_service` | ✅ 4 工具内 |
| 11 | 跨平台遥控 + 危险操作闸门 | 同上 + MCP 审批面 | ✅ 4 工具内（闸门见第 7 章） |
| 12 | 结合传感器历史的建议 | `recorder.get_statistics` | 🔁 换路线（历史） |
| 13 | 自然语言生成并注册自动化 | 写配置 API | 🔁 换路线（写配置） |
| 14 | 结构化数据 / 摄像头判断 | `ai_task.generate_data` + camera 附件 | 🔁 换路线（摄像头） |
| 15 | 对话式建议按钮 | HA：AI Tasks 实体 | ➖ HA 侧路线 |

三类判定合计：✅ 落在 4 工具内 5 条，🔁 必须换路线 4 条，➖ 不属于 Hermes 路线 6 条。

这张表怎么读，有三点：

- **✅ 不是「推荐做法」，只是「做得成」。** 第 3 号事件驱动的主动响应做得成，但它要不要开、开多大，是成本与安全的问题（第 6、7 章）。
- **➖ 是本章刻意保留的一类。** 表里 6 条场景的答案不是「Hermes 也能做」，而是「这件事本来就更该由 HA 的确定性机制做」。把它们标出来，是为了让下一章的判据有落脚点——否则读者很容易把「agent 也能干」当成「agent 应该干」。
- **🔁 的四条全部指向同一条出路。** 历史、写配置、摄像头这三类缺口，在第 3 章的路线选型里会收敛到一个答案；第 4、5 章分别给出两条 MCP 子路线的可用配置。

### 本章小结

- 「接入成功」只等于 `HASS_TOKEN` 被设上、四个工具被挂载，它是一个开关，不是能力清单。
- 内置 HA 工具恰好四个，全部走 `/api/states` 与 `/api/services` 两组端点；历史/统计、写配置、摄像头与结构化 AI 任务三类能力，在内置路径下没有任何表达方式。
- 「装个现成 HA skill」这条路**有东西可装**，但**可装不等于能补能力**：Hub 的搜索由一份联邦索引回答，「只有 `openhue` 一个」说的只是 `official` 支；skill 本身仍然只是知识，不提供新工具。
- 反过来，社区 ha-mcp 的 Setup Wizard 已为 Hermes 写了专属配置分支与 Notes（`mcp__home_assistant__<tool>`、`/reload-mcp`），只是它自己的 README 尚未收录 Hermes——「受支持但 README 未列」。
- 三道源码级防线值得记住：六个 blocked domains 加「先格式校验后黑名单」的顺序、`area` 参数其实是子串匹配而非 area registry 查询、出站 4096 硬切不分片。

### 下一章预告

这张表里 ➖ 那一列已经埋下了下一章的种子——有 6 个场景的正确答案不是「换条路线接 agent」，而是「本来就该写成 HA 的确定性自动化」。那么，官方到底在哪里划这条线？第 2 章去看那句边界的原始出处，并给出「任务类型 → 建议路线」的判据表。

### 本章来源

SRC-01 `tools/homeassistant_tool.py`、SRC-02 `plugins/platforms/homeassistant/adapter.py`、SRC-10 `gateway/platforms/base.py`（均在 github.com/NousResearch/hermes-agent）；HMS-03 `website/docs/reference/toolsets-reference.md`；HMS-05 `website/docs/user-guide/features/skills.md`；COM-01 ha-mcp README（github.com/homeassistant-ai/ha-mcp）；COM-23 ha-mcp Setup Wizard（homeassistant-ai.github.io/ha-mcp/setup/）；COM-24 `home-assistant-ecosystem/home-assistant-cli`（github.com/home-assistant-ecosystem/home-assistant-cli；PyPI `homeassistant-cli` 1.0.0）。场景表来自 `research/probe-03-scenarios.md`，该表不在 canonical 注册表内，本章按其原文逐行核对后使用。
