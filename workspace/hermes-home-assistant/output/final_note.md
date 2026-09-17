---
title: "用 Hermes Agent 控制 Home Assistant：能力地图与实现路线"
created: 2026-09-18
updated: 2026-09-18
status: draft
source_project: hermes-home-assistant
---

# 用 Hermes Agent 控制 Home Assistant：能力地图与实现路线

## 目录

- **[[#第 1 章：结论先行与能力地图——4 个内置工具的天花板]]**
  - [[#1.1 三条结论先行]]
  - [[#1.2 你现在的起点：4 个内置工具]]
  - [[#1.3 三类能力缺口]]
  - [[#1.5 落点清单]]
- **[[#第 2 章：三方对照轴——什么该交给 agent，什么本来就该用自动化]]**
  - [[#2.1 边界的官方原文在哪一页]]
  - [[#2.2 官方文档内部冲突：sentence triggers]]
  - [[#2.3 确定性能做的三件事]]
  - [[#2.4 两种相反的定位]]
  - [[#2.5 落点判据表]]
- **[[#第 3 章：路线选型——自建 skill / MCP server / 自定义 plugin 何时用]]**
  - [[#3.1 三条路线互补而非替代]]
  - [[#3.2 为什么自建 SKILL.md 补不了能力]]
  - [[#3.3 MCP 接线的硬规则]]
  - [[#3.4 自定义 plugin 的适用面]]
  - [[#3.5 落点决策表]]
- **[[#第 4 章：落地（一）——用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）]]**
  - [[#4.1 为什么先讲这条]]
  - [[#4.2 三种 transport 的 YAML]]
  - [[#4.3 鉴权两种写法]]
  - [[#4.4 传输与只读端点]]
  - [[#4.5 工具集裁剪与排错]]
  - [[#4.6 落点配置]]
- **[[#第 5 章：落地（二）——用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）]]**
  - [[#5.1 端点与「无官方 Hermes 示例」的事实]]
  - [[#5.2 鉴权：LLT bearer 优先]]
  - [[#5.3 OAuth / IndieAuth 的约束与未验证项]]
  - [[#5.4 反代与隧道]]
  - [[#5.5 跨版本行为相反]]
  - [[#5.6 工具集裁剪]]
  - [[#5.7 落点对照]]
- **[[#第 6 章：事件驱动与定时任务——白名单过滤、逐实体限流、投递两条分支与 4096 截断]]**
  - [[#6.1 入站：默认全关与逐实体限流]]
  - [[#6.2 出站两条分支：走哪条由执行位置决定，不由消息内容决定]]
  - [[#6.3 4096 硬截断：超长内容被静默砍尾]]
  - [[#6.5 落点配置]]
- **[[#第 7 章：安全与限界——LLT 权限真相、暴露列表的真实效力、最小化清单]]**
  - [[#7.1 LLT 权限模型的真相]]
  - [[#7.2 细粒度只读怎么做]]
  - [[#7.3 暴露列表：设计意图 ≠ 运行期边界]]
  - [[#7.4 MCP 侧审批面与白名单]]
  - [[#7.5 已知误报与事故机理]]
  - [[#7.6 落点清单：8 步安全最小化]]
- **[[#第 8 章：文档与代码不一致——12 条实例与自查方法]]**
  - [[#8.1 MCP 前缀：改名不彻底]]
  - [[#8.4 出站与 cron 的文档缺口]]
  - [[#8.5 SKILL.md frontmatter 两套字段表]]
  - [[#8.7 落点对照表]]
- **[[#第 9 章：成本与可靠性——工具 schema 常驻开销、误报机理、没有分母的误报率]]**
  - [[#9.1 常驻开销：工具 schema 每一次请求都要付]]
  - [[#9.2 实体数不是解释变量]]
  - [[#9.3 本地推理的门槛]]
  - [[#9.4 把限制做成配置]]
  - [[#9.5 误报机理与「没有分母的误报率」]]
  - [[#9.6 落点建议：token 预算与告警阈值]]
- **[[#附录：实机核对清单、未解决问题与延伸阅读]]**
  - [[#附录 A 实机核对清单（4 条命令）]]
  - [[#附录 B 未解决问题分级表]]
  - [[#附录 C 延伸阅读索引]]

---

## 第 1 章：结论先行与能力地图——4 个内置工具的天花板

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

**结论二：「装个现成 skill 就能用」在 HA 场景不成立。**

两层依据。第一层是事实核对：Hermes 官方 optional skills 目录的 smart-home 分类下**只有一个条目**，是 `openhue`——原文描述为 “Control Philips Hue lights, scenes, rooms via OpenHue CLI.”；bundled skills 目录里连 smart-home 这个分类都还没有；而技能系统的说明页 `website/docs/user-guide/features/skills.md`（HMS-05）全文未出现 Home Assistant。

第二层是更根本的原因，这里只点一句、第 3 章展开：**skill 不是能力，是知识**。它教 agent 怎么调已有的工具，不新增工具；而 HA 场景并不存在一个可以让 skill 去指挥的 `ha` CLI。所以「搜一个 HA skill 装上」这条路，在能搜到的那一刻之前就已经断了。

> [!tip] 大白话
> 把 skill 想成一份「岗位说明书」：它告诉你现有这几台机器怎么操作，但不会凭空给你添一台新机器。HA 场景现在缺的是机器，不是说明书。

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
- 「装个现成 HA skill」这条路不存在：官方 optional skills 的 smart-home 分类下只有 `openhue` 一个，而 skill 本身也不提供新能力。
- 反过来，社区 ha-mcp 的 Setup Wizard 已为 Hermes 写了专属配置分支与 Notes（`mcp__home_assistant__<tool>`、`/reload-mcp`），只是它自己的 README 尚未收录 Hermes——「受支持但 README 未列」。
- 三道源码级防线值得记住：六个 blocked domains 加「先格式校验后黑名单」的顺序、`area` 参数其实是子串匹配而非 area registry 查询、出站 4096 硬切不分片。

### 下一章预告

这张表里 ➖ 那一列已经埋下了下一章的种子——有 6 个场景的正确答案不是「换条路线接 agent」，而是「本来就该写成 HA 的确定性自动化」。那么，官方到底在哪里划这条线？第 2 章去看那句边界的原始出处，并给出「任务类型 → 建议路线」的判据表。

### 本章来源

SRC-01 `tools/homeassistant_tool.py`、SRC-02 `plugins/platforms/homeassistant/adapter.py`、SRC-10 `gateway/platforms/base.py`（均在 github.com/NousResearch/hermes-agent）；HMS-03 `website/docs/reference/toolsets-reference.md`；HMS-05 `website/docs/user-guide/features/skills.md`；COM-01 ha-mcp README（github.com/homeassistant-ai/ha-mcp）；COM-23 ha-mcp Setup Wizard（homeassistant-ai.github.io/ha-mcp/setup/）。场景表来自 `research/probe-03-scenarios.md`，该表不在 canonical 注册表内，本章按其原文逐行核对后使用。

---

## 第 2 章：三方对照轴——什么该交给 agent，什么本来就该用自动化

第 1 章那张能力缺口清单里，➖ 那一列有 6 个场景。它们的判定不是「Hermes 也能做，只是没必要」，而是「这件事本来就更该由 HA 的确定性机制做」。可「本来」两个字要有出处：它是官方写下的边界，还是社区经验之谈？这一章先找到这句边界的**原始出处**并把归属钉死，再顺着它往下问三层：官方为什么把线画在这里、HA 不靠 LLM 时用什么把同一件事做掉、以及两派社区项目为什么给出相反定位。最后收敛成一张「任务类型 → 建议路线」的判据表，接住上一章那 6 条。

### 2.1 边界的官方原文在哪一页

先把结论说明：这句边界**不在**讲对话代理总纲的那一页，也**不在**讲实体暴露的那一页，而是藏在**四个具体 LLM 集成页**里，作为 `Control Home Assistant` 这个配置项的说明文字出现。四页的这句原文逐字相同：

> If the model is allowed to interact with Home Assistant. It can only control or provide information about entities that are [exposed](https://www.home-assistant.io/voice_control/voice_remote_expose_devices/) to it.

注意它前面那一句限定条件——「If the model is allowed to interact with Home Assistant.」——这个配置项在语义上是**先开权限、再谈范围**：只有先允许模型碰 HA，后半句「只能控制已暴露的实体」才成为约束。把这两句拆开引用，会读成「模型天然只能控制已暴露实体」，那是另一回事。

归属对照如下，只有四页有这句：

| 页面 | canonical ID | 是否含「只控制已暴露实体」这句 |
|---|---|---|
| OpenAI Conversation | HAS-18 | 有（配置项 `Control Home Assistant` 描述内） |
| Anthropic | HAS-19 | 有（同上） |
| Google Generative AI Conversation | HAS-20 | 有（同上） |
| Ollama | HAS-21 | 有（同上，并多接一句「experimental」提示） |
| Conversation（内建代理总纲页） | HAS-17 | **无** |
| Voice control：Expose devices | HAS-09 | **无** |

这个归属值得较真：挂在 HAS-17 或 HAS-09 上，听起来像「HA 的整体设计就是暴露即边界」；挂在四个集成页的配置项里，它的真实身份是**一次配置项说明**，约束对象是「这个集成能不能碰 HA」，而不是一条全局安全承诺。

Ollama 那一页还有一句容易被截断引用的话，本册按完整句写（P2 已更正过 P1 的截断版）：

> Controlling Home Assistant is an experimental feature that provides the AI access to the Assist API of Home Assistant.

这句的分量在「experimental」和「Assist API」两处。前者是官方给本地模型路线的定性，后者点明了能力的来源——不是 HA 的内核，而是 Assist 那套 API。同一页给出的限制也是四条页面里最全的：建议**暴露少于 25 个实体**、**只有声明支持 Tools 的模型**才能控制 HA、小模型在开启控制后**对话可靠性会下降**，以及官方给的降级法——**同一个模型配两份 Ollama 集成，一份开控制、一份不开**，日常聊天走不开控制的那份（HAS-21）。

开发者文档把这条线说得更直接。HA 的开发者文档在讲内建 Assist API 时写了两句（HAS-16）：

> The Assist API is equivalent to the capabilities and exposed entities that are also accessible to the built-in conversation agent. No administrative tasks can be performed.

第一句说明「外部 agent 能用什么」这件事在官方设计里是同构的——等价于内建 conversation agent 的能力与可见实体，所以内建代理够不到的东西，接一个 LLM 也不会凭空多出来。第二句是一条硬否定：**管理类任务做不了**。这一条是本册反复要用的判据，到 2.5 的判据表会再见。

再往下就该讲暴露机制本身了。HAS-09 里能读到它被设计出来的动机（原文）：

> This is to avoid that sensitive devices, such as locks and garage doors, can inadvertently be controlled by voice commands.

锁和车库门被点名，是因为它们「误触发」的代价不可逆。但这里必须停一下贴标签：**这是设计意图，不是运行期强制边界**。官方 issue 里记录过「只读提问导致未暴露实体被 toggle」（COM-14，`not_planned` 关闭，无维护者解释），第三方实现者也直言「很难校验一次查询是否只用到了已暴露的实体」（COM-12）。所以正确读法是：**暴露列表是官方希望你遵守的设计意图；它被穿透是有记录的（第 7 章展开）**。把它当销售话术式的「安全边界」是不准确的。

> [!tip] 大白话
> 把这句边界想成商场门口的告示牌：「本店员工只能进你授权的那些仓库」。这是**规矩**，不是**墙**——告示牌不会物理拦住谁，靠的是员工自觉和事后追责。官方文档写的是规矩，issue 里记的是「有人真的走错过仓库」。所以做权限收紧时，不能只贴告示牌，还得真的配门禁（受限用户与权限粒度，第 7 章）。

### 2.2 官方文档内部冲突：sentence triggers

如果说 2.1 的归属问题只是「引用要引对地方」，这一节是**官方文档自己没对齐**。冲突的两边逐字如下：

| 页面 | canonical ID | 原句 |
|---|---|---|
| OpenAI / Anthropic / Google / Ollama 四页（逐字相同） | HAS-18/19/20/21 | This integration does not integrate with [sentence triggers](https://www.home-assistant.io/docs/automation/trigger/#sentence-trigger). |
| Conversation（内建代理总纲页） | HAS-17 | External conversation agents, such as OpenAI Conversation or Google Generative AI Conversation, only use sentence triggers when **Prefer handling commands locally** is enabled. |

一边是四个集成页**绝对否定**：这个集成不与 sentence triggers 集成。另一边是总纲页给出**有条件例外**：外部对话代理在开启 `Prefer handling commands locally` 时就会用 sentence triggers。同一个官方站点，同一类对象，两种说法。

更麻烦的是那个条件开关的归属。本册核验时的结果是：`Prefer handling commands locally` 这个串在上述**四个 LLM 集成页全文无命中**（P2 把它记为未解决项 G-7）。也就是说，总纲页让你去开一个开关，而具体集成页里找不到这个开关的说明。

本册的处置是**如实并列，不去替官方圆场**：把这一条当作「官方文档内部冲突」，落到实操上是——**如果你打算把 sentence triggers 当作事件入口，别只读文档，以你实机上的行为为准**。附录 A 的实机核对清单里有对应项，动配置之前先跑一遍。这一条也预告了第 8 章的主题：文档与代码不一致在本主题里是**常态**而不是例外，这里是它在 HA 官方文档内部的第一次露面。

> [!tip] 大白话
> 这就像两个官方客服给出相反答复：一个说「我们这个套餐不含这项服务」，另一个说「含的，你把那个开关打开就行」。你没法靠「官方文档肯定自洽」来消解它，只能自己去柜台试一次。文档在这里的作用是**告诉你有哪些可能性**，而不是**替你拍板**。

### 2.3 确定性能做的三件事

官方把边界画在这里，代价是「LLM 路线不管的事」需要有别的承担者。HA 侧的承担者不是一个，而是三组机制。理解这三组，是判据表能落地的前提。

**第一件：automation 的三段结构。** 这是 HA 自动化最底层的形状，官方原文（HAS-23）：

> All automations are made of at least a [trigger] and an [action]. Optionally combined with a [condition].

换成一句话：**触发器决定「什么时候看」，条件决定「这次算不算」，动作决定「做什么」**。官方同页的逐段说明是：trigger 通过则自动化启动，condition 通过才执行 action（HAS-23）。凡是能被写成「某状态满足某条件就做某动作」的需求，就已经落在这一段的射程内，不需要 LLM 参与。

**第二件：Alert 集成。** 上一章清单里第 7 号场景（电池 / 漏水 / 离线告警）正是它的典型用例。官方对该集成的定位原文（HAS-12，本轮回源官方文档源文件）：

> The **Alert** integration is designed to notify you when problematic issues arise. For example, if the garage door is left open, the `alert` integration can be used to remind you of this by sending you repeating notifications at customizable intervals. This is also used for low battery sensors, water leak sensors, or any condition that may need your attention.

它的价值在三个「不需要 LLM 就能得到」的性质：**重复提醒**（`repeat` 分钟数，问题不消失就反复通知）、**可确认**（实体有三态 `idle` / `on` / `off`，`off` 表示「条件仍为真但已被确认」）、以及 `done_message`（问题恢复时再发一条恢复通知）。官方给的最小配置逐字如下：

```yaml
# configuration.yaml（原文出自 HAS-12，notifiers 需换成本地已配置的通知目标）
alert:
  garage_door:
    name: Garage is open
    done_message: Garage is closed
    entity_id: input_boolean.garage_door
    state: "on"
    repeat: 30
    can_acknowledge: true
    skip_first: true
    notifiers:
      - ryans_phone
      - kristens_phone
```

**第三件：action response data + `response_variable`。** 前两件管「条件成立就通知」，这一件管「不靠 LLM 也能拼出内容」。官方定义原文（HAS-10）：

> Some actions may respond with data that can be used in automation. This data is called _action response data_. […] The action can specify a `response_variable`. This is the variable that contains the response data.

官方给的原始示例（逐字，HAS-10）：

```yaml
# scripts.yaml（原文出自 HAS-10 的官方示例）
action: calendar.get_events
target:
  entity_id: calendar.school
data:
  duration:
    hours: 24
response_variable: agenda
```

拿到 `agenda` 之后，同一个脚本里的下一条动作就能用模板把事件循环出来（官方示例的字段是 `agenda['calendar.school'].events`、`event.start`、`event.summary`，HAS-10）。这正是上一章第 6 号场景（无 LLM 的日报）的技术底座：**「取数据」是一次服务调用，「拼文字」是一次模板渲染，两件事都可以确定性完成**。

把三段结构、Alert、response data 接起来，一份「每天定点播报待办与告警」的自动化长这样。下面这段是**按上述三页机制拼出的组合示例（标注为拼接，未经官方或实机验证）**——机制各有官方出处，但这个具体组合不是官方范例：

```yaml
# automations.yaml（拼接示例：机制来自 HAS-23 / HAS-12 / HAS-10，未经实机验证）
- id: morning_briefing
  alias: 晨间简报
  trigger:
    - platform: time
      at: "07:30:00"
  condition:
    - condition: state
      entity_id: person.owner
      state: home
  action:
    - action: calendar.get_events
      target:
        entity_id: calendar.family
      data:
        duration:
          hours: 24
      response_variable: agenda
    - action: persistent_notification.create
      data:
        title: 今日简报
        message: >-
          {% for event in agenda['calendar.family'].events %}
          {{ event.start }} {{ event.summary }}
          {% endfor %}
```

这里出现的 `persistent_notification.create` 是 HA 的通知动作之一（HAS-15）。挑通知动作时有一处官方警告值得记住，它同样属于「文档明说、但很容易被忽略」的一类（HAS-24）：

> Send a notification (`notify.notify`): shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect. Choose a specific action or notify entity when the destination matters.

也就是说 `notify.notify` 是「发给第一个能找到的通道」，目标不确定。本册后面第 6 章讲 Hermes 出站投递时会再次撞上这条——脱 gateway 的那条分支正是走 `notify.notify`，届时这个「目标可能不在你预期处」的警告会变成真实风险。

还差**版本号**这一格。本册凡是讲 HA 能力的年份，都要落到具体版本，因为这几项能力是分两次发布的：

| 能力 | 版本 | 原文/来源 |
|---|---|---|
| HA 主动发起对话（`assist_satellite.ask_question`） | **2025.7** | HAS-26（该版 release notes 中逐字出现该 action） |
| 自动化编辑器 Suggest 按钮 | **2025.8** | HAS-27 |

Suggest 按钮还有一条容易被忽略的限定：官方原文说它「**This button is not visible by default and will only appear if you enable it in the “AI suggestions” settings.**」（HAS-27）。默认不可见，需要在设置里开。同时也提醒：生成文本会把自动化/脚本全文连同标签与其他命名一起发给 LLM（HAS-27）。

> [!warning] 版本记录的一处坑
> `research/probe-03-scenarios.md` 把「HA 主动发起对话」记成「2025.9 起」。那是 P1 阶段的旧记录，**以 HAS-26 的 release notes 为准：2025.7**。凡在别的材料里看到 2025.9+，按 2025.7 更正。

最后是一个反面注脚。官方博客那篇 AI 主题文章（HAS-07）读起来很适合当「HA 的 AI 规划」来引用，但它的两个特征是：**通篇不带版本号**，而且对其中一项能力给出的**只是 blueprint 链接，不是功能文档链接**。结论很实用——**别把博客当规格**：博客用来判断方向，版本与能力边界要去集成页和 release notes 里核。

> [!tip] 大白话
> 确定性机制三件套可以想成家里的三种「自动」：**automation 三段**是「门磁一开（trigger）且是夜里（condition），就开灯（action）」；**Alert** 是「这扇门没关就一直响，直到你按掉确认」；**response_variable** 是「先去日历把今天的条目抄下来，再把抄下来的东西念给你听」。这三件事没有一件需要「理解语义」，全都是「条件 → 动作」和「取数 → 填模板」。而 LLM 的长处恰恰不在这类事上——所以别用它去做本来不需要理解的事。

### 2.4 两种相反的定位

社区里做得比较认真的几个项目，对「LLM 该站在哪」给出了方向相反的答案——不是谁对谁错，而是两种可复用的定位范式。

第一种是**彻底不用 LLM**。`ha-household-briefing` 解决的就是上一章第 6 号场景（日报），它 README 的开头逐字（COM-03，本轮回源）：

> A plain-English briefing of your whole household — weather, today's calendar, who's home, what's open, unlocked, or left on, and what needs attention — composed entirely from the entities you already have.

紧接着的那句更关键：

> No cloud. No API keys. No LLM. No subscription. It reads your local state machine and writes sentences. Nothing leaves your network.

「读本地状态、写句子」——它证明了「生成一段读起来像人话的日报」这件事，**在不引入任何模型的前提下可以做到**。代价是它只会覆盖你事先为它设计好的字段，不会在异常时给你一个新角度的解释。

第二种是**让 LLM 参与判断，但不让它动手**。`home-generative-agent` 在讲它的 Sentinel 异常引擎时给出一句定位原文（COM-06，本轮逐字核验）：

> its Sentinel anomaly engine keeps safety decisions deterministic, with the LLM advising but never actuating.

这句话值得逐词读：「safety decisions deterministic」是决策层，`advising but never actuating` 是权限层——**LLM 可以「建议」，但「执行」始终在确定性那一侧**。它和第一种方案的区别在于允许 LLM 提供判断（比如给异常加一段解释），但在「谁按下开关」这一层做了严格切分。

需要给它补一句来源性质：该项目的安全机制在源码层是**静态筛查**（对 HA 的 action taxonomy 做 allowlist，无法解析的一律 fail closed）加 **PIN 门禁**，项目自陈了三类验证缺口（原始协议写入不筛查、运行时解析的 target 无法检视、蓝图型自动化只保证「审批时刻」成立）。也就是说，「LLM 只建议不执行」是它的设计目标与实现方向，不是一条已经封死的形式化保证。本册只把它当作**定位范式**引用，不作为可直接照搬的安全证明。

一个更细的参考来自第三类项目。`mylo` 把「确定性基线 + LLM 分工」做成了具体参数（COM-05，一手 README 逐字）：传感器异常用 **7 天基线**的 z-score，**3.5σ 且连续两次**才报（「so one-hour blips don't alert」）；权限分三层（只读免批准 / 修改类先 dry-run / 动作类显式确认）；token 预算做成显式配置键（`session_budget_usd` 默认 `0.50`）。它演示了「什么该交给确定性」的颗粒度可以细到什么程度——**连「多久算异常」都交给统计基线，而不是交给模型即兴判断**。

| 项目 | 定位口径 | 来源与性质 |
|---|---|---|
| ha-household-briefing | 「No cloud. No API keys. No LLM. No subscription.」 | COM-03，一手 README，本轮已回源逐字 |
| home-generative-agent | 「keeps safety decisions deterministic, with the LLM advising but never actuating」 | COM-06，一手 README，逐字核验 |
| mylo | 7 天基线 / 3.5σ × 连续两次 / 三层权限 / `session_budget_usd` | COM-05，一手 README，逐字核验 |
| haclaude | 夜间巡检 + 只读工具白名单（德文 README） | COM-04，**本轮未复核**，仅作线索 |

> [!tip] 大白话
> 这两派的分歧，用做饭打比方就清楚了。第一派说「凉菜本来就该冷着上，不需要动火」；第二派说「可以让帮厨**告诉你**这道菜咸了，但**加盐**这件事必须你自己来——因为加错了没法撤」。两派都同意一件事：**「谁最后按下那个不可逆的按钮」和「谁提供判断」必须是两个角色**。

### 2.5 落点判据表

把 2.1 到 2.4 收成一张表。这张表要接住第 1 章那 6 条 ➖，所以第一列先用「任务类型」而不是「场景名」，让判据可迁移到表外的新需求。

| 任务类型 | 判据（问自己一句） | 建议路线 | 来源 |
|---|---|---|---|
| 语音控制（Assist 管道） | 需求本身就是「用嘴说」 | HA 侧：Assist + 实体暴露 + conversation agent | HAS-09 |
| HA 主动发起对话 | 需要 HA 主动开口（播报/提问） | HA 侧：2025.7+ 的 `assist_satellite.ask_question` | HAS-26 |
| 日报 / 巡检文本（不需要模型解释） | 内容字段是事先能枚举的 | HA 确定性：`response_variable` + 模板 + 自动化 | HAS-10；对照实现 COM-03 |
| 阈值 / 时长 / 状态类告警 | 「条件成立就通知」能一句话说清 | HA 确定性：Alert 集成（可重复、可确认） | HAS-12 |
| 场景联动（离开家 / 回家） | 触发信号是地理围栏进出 | HA 确定性：`zone` 触发器 | HAS-11 |
| 对话式建议（起名 / 分类 / 描述） | 目标是「给你一个建议文本」 | HA 侧：2025.8 Suggest（默认不可见） | HAS-27 |
| 自然语言控制已有实体 | 动作最终落到 service 调用 | Hermes 内置 4 工具 | 第 1 章（SRC-01） |
| 基线学习型告警（「这次和以往不一样」） | 需要「学正常长什么样」 | 换路线：LLM + 历史数据（参考 7 天 / 3.5σ 参数） | COM-05 |
| 历史 / 统计查询 | 需要读 recorder | 换路线：MCP（第 3–5 章） | 第 1 章 A-3 |
| 读写配置（自动化 / 助手 / 仪表盘） | 需要写 HA 配置面 | 换路线：MCP（第 3–5 章） | 第 1 章 A-3 |
| 摄像头 / 结构化 AI 任务 | 需要看图像或产出结构化对象 | 换路线：MCP / `ai_task` | 第 1 章 A-3 |
| **管理类任务（重启 / 改系统配置 / 卸载）** | 是不是「管理」而不是「控制」 | **两条路线都不给** | HAS-16（No administrative tasks） |

最后一行要单独强调：管理类任务不是「换条路线就能做」，而是**官方明确说内建路线做不了**（HAS-16 的 `No administrative tasks can be performed.`）。至于换成 MCP 路线之后它的边界在哪，是第 5 章要处理的问题——那里会看到官方 `mcp_server` 的 admin 要求跨版本相反（2026.9 vs 2026.10），所以「能不能做管理类」这件事**必须带版本号回答**。

配合表格，再给四条顺序判断法，遇新需求从上往下问：

1. **能写成「条件 → 动作」吗？** 能，就先写成 HA 自动化；这能覆盖掉一大半的告警与联动需求，且没有 token 成本、没有误判率。
2. **需要「学基线」或「听懂自由表达」吗？** 需要，才考虑 LLM；这时先去 2.4 那类项目里找一个已有的参数起点（如 7 天基线、连续两次），不要从零拍阈值。
3. **需要读历史 / 写配置 / 看图吗？** 需要，就走 MCP 路线（第 3 章给选型，第 4、5 章给配置）。
4. **它是管理类任务吗？** 是，两条路线都要额外过权限关；内建 LLM 路线直接排除（HAS-16），MCP 路线看版本（HAS-25 / 第 5 章）。

### 本章小结

- 「只控制已暴露实体」这句边界的正确归属是**四个 LLM 集成页**（`HAS-18/19/20/21`）的 `Control Home Assistant` 配置项描述，前面还有一句「If the model is allowed to interact with Home Assistant.」；`HAS-17` 与 `HAS-09` 都没有这句。
- 开发者文档给了比集成页更硬的一条：Assist API 与内建 conversation agent 能力等价，且**管理类任务做不了**（HAS-16）。
- 「敏感设备默认不暴露」是官方**设计意图**（HAS-09 点名锁与车库门），不是运行期强制；它被穿透是有记录的（COM-14）。
- 官方文档内部存在冲突：四个集成页绝对否定 sentence triggers，`HAS-17` 却给出条件性例外，而那个条件开关 `Prefer handling commands locally` 在四页全文无命中。
- 确定性一侧的三件套是：automation 三段结构（HAS-23）、Alert 集成（HAS-12）、action response data + `response_variable`（HAS-10）；配上版本号，HA 主动发起对话是 **2025.7**（HAS-26），Suggest 按钮是 **2025.8 且默认不可见**（HAS-27）。
- 社区给出两种相反定位：彻底不用 LLM（COM-03）与「安全判断保持确定性、LLM 只建议不执行」（COM-06）；`mylo` 提供了可抄的参数颗粒度（COM-05）。

### 下一章预告

判据表里「换路线」那一列出现了四次，并且全部指向同一个出口——MCP。但 MCP 只是三条候选路线之一，另外两条（自建 SKILL.md、自定义 plugin）什么时候才有意义？第 3 章给出三条路线的互补关系、MCP 接线的硬规则（工具注册名从哪来、`trust` 的 fail-closed 语义、`tools.include` 用哪个名字），以及一张路线选型决策表。

### 本章来源

HAS-18 / HAS-19 / HAS-20 / HAS-21（四个 LLM 集成页，`Control Home Assistant` 配置项描述与 sentence triggers 句）；HAS-17 `conversation`（sentence triggers 条件性例外句）；HAS-16 开发者文档 `core/llm`（Assist API 等价句与「No administrative tasks」）；HAS-09 `voice_control/voice_remote_expose_devices`（设计意图句）；HAS-23 `docs/automation/basics`（三段结构）；HAS-11 `docs/automation/trigger`（`zone` 触发器，本轮回源）；HAS-12 `integrations/alert`（集成定位与 `alert` 最小配置，本轮回源官方文档源文件）；HAS-10 `docs/scripts/service-calls`（action response data / `response_variable` 与官方示例）；HAS-15 `integrations/persistent_notification`；HAS-24 `integrations/notify`（`notify.notify` 警告）；HAS-26 release notes 2025.7；HAS-27 release notes 2025.8；HAS-07 官方博客（无版本号的注脚）；COM-03 `archieboy-holdings/ha-household-briefing` README（本轮回源逐字）；COM-05 `Oasis-Enterprise/mylo` README；COM-06 `goruck/home-generative-agent` README（仅采用其定位原句）；COM-04 `cnc-lascercraft/haclaude`（未复核线索）；COM-14 / COM-12（暴露列表穿透的记录）。场景编号沿用 `research/probe-03-scenarios.md` 的表序。

---

## 第 3 章：路线选型——自建 skill / MCP server / 自定义 plugin 何时用

第 2 章的判据表里，「换路线」那一列出现了四次，而且四次都指向同一个出口：MCP。但 MCP 只是三条候选路线之一。这一章要回答的是**选型**问题：拿到一个能力需求，什么情况下该写一份 SKILL.md、什么情况下该接一个 MCP server、什么情况下才轮到自定义 plugin。这一章会先拆掉一个很常见的误解——把三条路线当成「初级 / 中级 / 高级」的强弱排序——然后给出各自的真实分工、MCP 接线的硬规则（注册名从哪来、`trust` 怎么判、工具白名单用哪个名字），最后收成一张决策表，供第 4、5 章按需抄配置。

### 3.1 三条路线互补而非替代

先说那个误解。很多人第一次接触这三样东西，会本能地按「能力大小」排队：skill 最弱（只是提示词）、plugin 最强（能写代码）、MCP 居中。这个排序在**本主题的具体语境下是错的**，因为它把三条放在不同轴上的路线强行压成了一条轴。

真实的差异在**它们各自补什么**：

| 路线 | 它到底提供什么 | 出发点 | 要改什么 |
|---|---|---|---|
| 自建 SKILL.md | **知识**：教 agent 怎么用**已有**的工具/CLI | 能力已经存在，缺的是「怎么调」 | 只加一个 Markdown 文件 |
| MCP server | **外部能力**：把别人做好的工具接进来 | 能力在进程外，已有 server 可复用 | 改 `config.yaml` + 一个 `mcp_servers` 条目 |
| 自定义 plugin | **进程内能力**：注册一个原生 tool / hook | 能力哪都没有，必须自己写 | 写 Python 插件并显式启用 |

三条路线并不互斥：一个成熟的配置里三者可以同时存在。真正需要判断的从来不是「哪个更强」，而是「我现在缺的是知识、外部能力、还是进程内能力」。

有一个前提在第 1 章已经确认过，这里要重申，因为它是本章的出发点：**Skills Hub 里没有现成的 Home Assistant skill**。bundled 与 optional skills 合起来，smart-home 分类下只有 `openhue` 一个，其余为空（HMS-05，optional-skills 目录逐字）。所以「装个现成 skill 就能控制 HA」这条路根本不成立——不是效果不好，是**没有可装的东西**。这也意味着，如果你的需求能用 skill 满足，你得自己写。

### 3.2 为什么自建 SKILL.md 补不了能力

这一节是本章最重要的一条否定结论：**SKILL.md 表达不了新能力**。

理由在 skills 系统的官方定义里就写着（HMS-05）：

> Skills are on-demand knowledge documents the agent can load when needed.

「knowledge documents」——**知识文档**，不是可执行单元。一份 skill 能做的事，是告诉 agent「你手上已有的某个工具该怎么用、什么时候用、哪里容易翻车」，它不会给 agent 增加任何一个可调用的工具。官方给的标准正文结构也印证了这一点：`## When to Use`（何时加载）/ `## Quick Reference`（命令速查）/ `## Procedure`（步骤）/ `## Pitfalls`（坑）/ `## Verification`（怎么验证），全是在描述「怎么用已有能力」。

那 `openhue` 为什么可以只靠一份 SKILL.md 就干活？因为**它描述的 CLI 真实存在**。它的 frontmatter 里有一条声明（逐字取自 `optional-skills/smart-home/openhue/SKILL.md`）：

```markdown
# ~/.hermes/skills/smart-home/openhue/SKILL.md（原文逐字，节选）
---
name: openhue
description: "Control Philips Hue lights, scenes, rooms via OpenHue CLI."
metadata:
  hermes:
    tags: [Smart-Home, Hue, Lights, IoT, Automation]
    homepage: https://www.openhue.io/cli
prerequisites:
  commands: [openhue]
---
```

`prerequisites.commands: [openhue]` 这一行是关键：**先有 `openhue` 这个命令，这份 skill 才有意义**。skill 做的是「把 CLI 的存在告诉 agent，并教它怎么拼参数」，能力本身来自 CLI。

把这个模式平移到 HA，问题立刻暴露：**HA 场景不存在一个可调的 `ha` CLI**。你没有一个能在终端里跑 `ha light turn_on --entity light.kitchen` 的命令——内置的四个 `ha_*` 工具是 Hermes 内部的 tool，不是 shell 命令，skill 无法「教 agent 调用它们」（agent 本来就会调）。所以结论是分层的：

- 如果能力**已经**由别的方式提供了（比如你自己写了一个包装 HA REST 的脚本、或用 `curl` + 长期令牌），那 SKILL.md 是**恰当的**——它把「怎么用这个脚本」固化下来，省掉每次在提示词里重复交代。
- 如果能力**还不存在**，写多少份 SKILL.md 都不会把它变出来。这时你要的是 3.3 或 3.4。

一份最小可用的 SKILL.md 长这样（结构来自 HMS-12 的官方格式说明；字段逐字取自其中的 frontmatter 清单）：

```markdown
# ~/.hermes/skills/smart-home/ha-rest/SKILL.md
---
name: ha-rest
description: 用 curl 调 HA REST API 做只读查询与场景调用
version: 1.0.0
author: your-name
license: MIT
metadata:
  hermes:
    tags: [Smart-Home, HomeAssistant, REST]
---

# HA REST 查询

## When to Use
需要读取 HA 状态但内置工具不够用时。

## Quick Reference
| 需求 | 命令 |
|---|---|
| 取实体状态 | `curl -H "Authorization: Bearer $HASS_TOKEN" $HASS_URL/api/states/<entity_id>` |

## Procedure
1. 从环境变量取 `HASS_URL` 与 `HASS_TOKEN`。
2. 按上表拼 URL，注意 `entity_id` 里的点号要原样保留。

## Pitfalls
令牌权限等于**创建它的用户**（源码级推论，见第 7 章），别用 admin 账号签发的令牌。

## Verification
返回 JSON 里含 `state` 字段即成功；收到 `401` 说明令牌或 `HASS_URL` 不对。
```

顺带记一个已知的文档缺口：SKILL.md 的 frontmatter 存在**两套互不覆盖的字段表**（HMS-12 与 HMS-05 各给一套，且没有「本表为准」的措辞，仓库里也没找到 schema 文件），本册以 HMS-12 为主表。这条属于第 8 章的清单，这里只作提醒。

> [!tip] 大白话
> SKILL.md 是**说明书**，不是**零件**。你买了一台新机器（`openhue` 命令），说明书能帮你少走弯路；但你手里没这台机器时，把说明书背得再熟，也拧不动一颗螺丝。HA 场景的尴尬就在于：大家以为「装个说明书就有机器了」，而实际是**机器根本还没到货**。

### 3.3 MCP 接线的硬规则

MCP 路线是三条里唯一能一次性补齐第 1 章那三类缺口（历史/统计、写配置、摄像头）的。正因为它要接外部进程，接线处有一批**不看源码就会搞错**的硬规则。这一节按「先搞清叠加关系，再搞清名字，最后搞清权限」的顺序排。

**规则一：同名的 MCP server 与内置 toolset 是叠加，不是遮蔽。** 这一条特别容易被想当然地搞反——很多人以为「我接的 server 也叫 `homeassistant`，那它应该会替换掉内置那四个工具」。官方文档原文（HMS-03，本轮已回源逐字）：

> If a server is named like a built-in toolset (`homeassistant`, `browser`), that name resolves to the built-in tools **plus** the server's `mcp__<server>__*` tools; neither side shadows the other.

所以你把 server 命名为 `homeassistant`，得到的不是「4 个工具被换掉」，而是**内置 4 个 + server 工具**。这一点有两个现实后果：其一，工具总数是**相加**的，而 tool schema 是常驻上下文开销（第 9 章展开）；其二，不遮蔽意味着你**无法通过命名来禁用内置工具**——想收窄只能走 `tools.include`，不能用「起个同名」蒙混。同一份文档还指出，插件注册的 toolset 也是走同一套机制叠加进来（HMS-06 同页：插件用 `ctx.register_tool()` 在初始化时注册，这些 toolset「appear alongside built-in toolsets」）。

**规则二：注册名的写法由源码定，不是文档说了算。** 注册名指 agent 实际看到的工具全名。这里是**源码级定论**（SRC-04）：

```python
# tools/mcp_tool_schema.py（SRC-04，逐字节选）
def sanitize_mcp_name_component(value: str) -> str:
    """Replace every char outside ``[A-Za-z0-9_]`` with ``_`` (hyphens included, the
    historical behavior) so generated names pass provider validation."""
    return re.sub(r"[^A-Za-z0-9_]", "_", str(value or ""))

# ``mcp__<server>__<tool>``: the convention shared by Claude Code, Codex and OpenCode. The
# double underscore disambiguates the server/tool boundary even when either contains
# underscores, and matches the Anthropic-OAuth wire form.
MCP_TOOL_NAME_PREFIX = "mcp__"

_MCP_TOOL_NAME_MAX_LENGTH = 64
_MCP_TOOL_NAME_HASH_LENGTH = 8

def mcp_prefixed_tool_name(server_name: str, tool_name: str) -> str:
    """Registry/wire name: ``mcp__<sanitizedServer>__<sanitizedTool>``, clamped to 64 chars with a
    stable hash suffix when the natural name is longer."""
```

把这段翻成人话，注册名有**三条**变换规则：

| 步骤 | 规则 | 例子 |
|---|---|---|
| 拼前缀 | `mcp__` + server 名 + `__` + 工具名（**双下划线**） | server `home-assistant` + tool `get_state` |
| 归一化 | 把 `-`、`.` 等非 `[A-Za-z0-9_]` 字符全部换成 `_` | `home-assistant` → `home_assistant` |
| 限长 | 超过 64 字符则截断，并追加 `_` + sha256 前 8 位 | 长名 → `..._a1b2c3d4` |

于是 `home-assistant` 这个 server 下的 `get_state`，注册名是 **`mcp__home_assistant__get_state`**——注意是**双下划线**，且连字符已经变成了下划线。

这里必须点一句文档漂移：官方的 MCP 指南页（HMS-10）与功能页（HMS-11）以及发布站上写的仍是**旧写法**（单下划线、`mcp_<server>_<tool>` 的形式），HMS-10 的正文里甚至直接用了 `mcp_chrome_devtools_win_list_pages` 这样的名字。以谁为准？**以源码为准**。第 8 章会把这条作为「文档与代码不一致」的实例展开，这里只需要记住结论：写配置、排错、看日志时按 `mcp__` 走。

**规则三：`tools.include` / `tools.exclude` 用原始工具名，不是注册名。** 这一条与规则二恰好相反，最容易踩。官方配置参考页（HMS-04）原文：

> | `include` | string or list | Whitelist **server-native** MCP tools. Entries may be exact names or fnmatch-style globs (`*_radar_*`, `get_zones_*`) |
> | `exclude` | string or list | Blacklist **server-native** MCP tools. Same exact-name / glob semantics as `include` |

并且给出了优先级：**「If both are set, `include` wins.」** 也就是说，白名单写 `get_state`（原始名），而不是 `mcp__home_assistant__get_state`（注册名）。实践上建议**只用 `include` 做白名单**、少用 `exclude` 黑名单——黑名单的失败模式是「server 一升级上了新工具，你的黑名单没跟上，新工具自动放行」。

**规则四：`trust` 是 fail-closed 的。** 官方对 `trust` 的定义原文（HMS-04）：

> Trust tier: `full` (default) or `untrusted`. On an `untrusted` server, every write-capable tool call (any tool without a `readOnlyHint: true` annotation) requires user approval through the standard approval surface before it runs. `readOnlyHint` is a server-supplied *hint* — a lying server can at most skip approval for tools it claims are read-only, never gain extra access — so mark any server you don't fully control as `untrusted`. […] Unrecognized values are treated as `untrusted` (fail-closed)

这段里有三个要点值得逐条拆：

1. **默认是 `full`，不是 `untrusted`。** 也就是说「不写 `trust`」不等于安全，等于「全信」。要用审批面兜底，必须**显式**写 `trust: untrusted`。
2. **判定写工具的依据是 `readOnlyHint: true` 这个注解在不在**，而非「工具名字听起来像不像写操作」。凡是没有这个注解的工具，在 `untrusted` 下都走审批。
3. **`readOnlyHint` 只是服务端自报的提示。** 它的上限是「一个说谎的 server 最多让自己声称只读的工具跳过审批，永远拿不到额外权限」；它的下限是——**它不能证明任何事**。一个服务端可以给自己所有工具都标上 `readOnlyHint: true`。所以这条注解的正确用法是「减少正常 server 的审批噪音」，而不是「作为信任的依据」。

最后一条还不止影响审批：**未识别的值一律按 `untrusted` 处理**（fail-closed）——写错一个 `trust: trusted`，你得到的是最严的那档，不是最松的那档。这个设计方向是保守的，可以放心。

**规则五：CLI 与会话内操作。** 配置改完之后有两组入口（HMS-07、HMS-10）：命令行侧是 `hermes mcp add <name> --url <URL>`、`hermes mcp list`、`hermes mcp test <name>`、`hermes mcp login <name>`（OAuth 强制重认证）、`hermes mcp configure <name>`（切换工具选择）；会话内则是 `/reload-mcp`，改完配置不用重启进程。

把上面五条规则落到一份配置上，形态如下（**按 HMS-04 的键拼出的示例，标注为拼接、未经实机验证**）：

```yaml
# ~/.hermes/config.yaml（拼接示例：键与语义来自 HMS-04，具体值未经实机验证）
mcp_servers:
  home-assistant:
    url: "${env:HA_MCP_URL}"        # ${env:VAR} / ${VAR} 从 ~/.hermes/.env 解析
    headers:
      Authorization: "Bearer ${env:HA_TOKEN}"
    trust: untrusted                # 显式收紧；不写默认是 full
    tools:
      include: [get_state, list_entities]   # 原始工具名（非注册名）
      exclude: []                            # 两者都写时 include 优先
```

**规则六（排错陷阱）：`hermes mcp test` 打印的是原始工具名，不能用来验证前缀。** 这一点本册核到了源码：`cmd_mcp_test` 打印的工具名来自 `_probe_single_server`，而该函数返回的是连接后遍历 `server._tools` 拿到的 `t.name`（SRC-07）——即 server 端自报的**原生名**，没有经过 `mcp_prefixed_tool_name` 加工。所以你会看到 `get_state` 而不是 `mcp__home_assistant__get_state`。用它验证「连得上吗、有几个工具」是对的；用它验证「注册名前缀对不对」是错的——后者只能让 agent 在会话里列出工具全名来看（核对步骤见附录 A）。

> [!tip] 大白话
> 把注册名和原始名的关系想成**工牌与真名**。server 交上来的花名册（`hermes mcp test` 打印的）写的是员工的**真名**；公司前台系统里挂的是**工牌号**（`mcp__home_assistant__get_state`，双下划线、连字符换成下划线、太长就截断加编号）。你要筛选谁能进门时，**填的是真名**（`tools.include`）；你要在日志里认人时，**看的是工牌号**。两边混用，就会出现「明明加了白名单却还是全都进来了」或者「照着日志里的名字写白名单，一个都没匹配上」。

### 3.4 自定义 plugin 的适用面

排除了「skill 能凭空补能力」之后，还剩一个场景：**能力既不在已有 CLI 里，也没有现成 MCP server 可用**。这时才轮到自定义 plugin。

官方对插件能力的定位可以一句话概括：plugin 是在**进程内**注册扩展点。最小可用的插件由两个文件组成，官方给的 hello-world 示例逐字如下（HMS-06）：

```yaml
# ~/.hermes/plugins/hello-world/plugin.yaml
name: hello-world
version: "1.0"
description: A minimal example plugin
```

```python
# ~/.hermes/plugins/hello-world/__init__.py
def register(ctx):
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "Name to greet"}},
            "required": ["name"],
        },
    }

    def handle_hello(params, **kwargs):
        del kwargs
        name = params.get("name", "World")
        return json.dumps({"success": True, "greeting": f"Hello, {name}!"})

    ctx.register_tool(
        name="hello_world",
        toolset="hello_world",
        schema=schema,
        handler=handle_hello,
    )
```

注册签名就是 `ctx.register_tool(name=..., toolset=..., schema=..., handler=...)`（HMS-06）。它注册出来的 toolset 会**和内建 toolset 并列**出现，用同一套开关控制。

那什么时候该动用它？本册把适用面收成三类：

1. **需要精确执行的原生操作**：操作序列必须严格按顺序、按字节执行，不能交给模型即兴发挥（例如需要「写临时文件 → 校验 → 原子替换 → 触发 reload」这种带回滚的事务）。
2. **二进制或流式数据**：要把摄像头帧、音频流这类不经过文本编码的数据接进来，MCP 的 JSON-RPC 工具面并不适合承载。
3. **必须走审批面的原生工具**：你希望这个操作出现在 Hermes 自己的审批流程里（而不是绕到外部 server 的鉴权里），插件注册的原生 tool 天然处在这条链路上。

**关于「默认 opt-in」，这里必须带上限定词。** 官方原文是（HMS-06）：

> **General plugins and user-installed backends are disabled by default** — discovery finds them (so they show up in `hermes plugins` and `/plugins`), but nothing with hooks or tools loads until you add the plugin's name to `plugins.enabled` in `~/.hermes/config.yaml`.

限定词落在 **General plugins and user-installed backends** 上。同一个页面紧接着给了一张**例外表**：bundled 的 platform 插件、bundled 后端、memory provider、context engine、model provider **全部自动加载**——理由是「they're part of Hermes' built-in surface and would break basic functionality if gated off by default」。官方自己的总结句是：**bundled "always-works" infrastructure loads automatically; third-party general plugins are opt-in.**

所以正确的说法是「**第三方通用插件默认不加载，需要 `plugins.enabled` 显式放行**」，**不能**缩写成「plugins 一律要手动启用」——那会漏掉整张例外表，也会让你在排查「为什么我装的插件没生效」时找错方向（先确认它属于哪一类）。启用方式是 `hermes plugins enable <name>`，或直接写进 `plugins.enabled`；写完后可以用 `hermes plugins doctor . --ci` 做校验。

> [!tip] 大白话
> 把 plugin 想成**自己造一个零件焊进机器**。它比「读说明书」重，但换来的是机器真的多个功能。而 opt-in 那条规则，想成「**公司原装的零件出厂就通电，外部采购的零件默认断电**」——不是所有插件都要你手动开，只有来历不明的那批需要你点头。所以看到「没生效」先别急着重装，先问一句：它是原装的，还是我塞进去的？

### 3.5 落点决策表

把 3.1 到 3.4 收成一张表。第一列不是「选哪条路线」，而是**你缺的是什么**，因为选型错误的根源通常不是选错工具，而是**没搞清缺口的性质**。

| 能力需求 | 缺的是什么 | 建议路线 | 成本 | 权限面 |
|---|---|---|---|---|
| 让 agent 知道「怎么用某个已有 CLI / 脚本」 | 知识 | 自建 SKILL.md | 低（一个 Markdown 文件） | 不变（复用已有工具权限） |
| 读历史 / 统计（recorder） | 外部能力 | MCP server | 中（一个 `mcp_servers` 条目） | `trust` 显式收紧 + `include` 白名单 |
| 读写配置（自动化 / 助手 / 仪表盘） | 外部能力 | MCP server | 中 | 同上；写操作必过审批（`untrusted`） |
| 摄像头 / 结构化 AI 任务 | 外部能力 | MCP server（或 HA 侧 `ai_task`） | 中 | 同上 |
| 复用别人写好的 HA 工具集 | 外部能力 | MCP server（社区实现） | 中（可抄模板） | 同上；注意其作用域可能比官方内建大 |
| 新增一个精确执行的原生工具 | 进程内能力 | 自定义 plugin | 高（要写并维护 Python） | 走 Hermes 原生审批面 |
| 二进制 / 流式数据接入 | 进程内能力 | 自定义 plugin | 高 | 同上 |
| 能力哪都不存在，且你要的是「问出答案」 | 知识 | **没有路线能补**——先解决能力来源 | — | — |

最后一行是这张表最该记住的一格：三条路线**没有一条能凭空造出能力**。skill 是说明书，MCP 是接线，plugin 是自己造零件——三者都需要「有个东西可接」。当你发现需求落在这张表外面，正确动作不是「再试一条路线」，而是回到第 2 章的判据表，看它是不是本来就该由 HA 的确定性机制承担。

配合表格使用的判断顺序是固定的三步：

1. **先看能力在不在**：有没有现成 CLI / 脚本 / MCP server 提供它？没有就去解决来源（自建 server、自写脚本），别急着选 route。
2. **再看缺的是知识还是能力**：能力已在、只是不知道怎么调 → SKILL.md；能力在进程外 → MCP；必须在进程内 → plugin。
3. **最后收权限**：MCP 一律先 `trust: untrusted` + `tools.include` 白名单起步；plugin 走原生审批面。这一层的细节在第 7 章统一处理。

### 本章小结

- 三条路线不是「强弱排序」而是**补不同东西**：SKILL.md 补**知识**、MCP server 补**外部能力**、自定义 plugin 补**进程内能力**，彼此互补。
- 自建 SKILL.md **表达不了新能力**——官方把它定义为「on-demand knowledge documents」（HMS-05），`openhue` 之所以能只靠一份 skill 干活，是因为 `prerequisites.commands: [openhue]` 声明的那个 CLI 真实存在；HA 场景不存在可调的 `ha` CLI，所以 SKILL.md 只在能力已由别的方式提供后才有意义。
- MCP 与内建 toolset **同名叠加、不遮蔽**（HMS-03 逐字），所以「起个同名禁用内置工具」这种想法行不通，收窄只能用 `tools.include`。
- MCP 注册名的硬规则来自源码（SRC-04）：`mcp__<server>__<tool>`、`-`/`.` → `_`、超 64 字符截断加 8 位 sha256 后缀；官方文档与发布站仍是旧写法（第 8 章展开）。
- `tools.include` / `tools.exclude` 用**原始工具名**，两者都写时 `include` 优先（HMS-04）；`trust` 是 fail-closed，默认 `full`，写 `untrusted` 才启用写操作审批，而 `readOnlyHint` 只是**服务端自报**的提示。
- 排错陷阱：`hermes mcp test` 打印的是**原生**工具名（SRC-07），只能验证连通性与工具数，不能验证注册名前缀。
- 自定义 plugin 适用于精确执行、二进制/流式、必须走原生审批面三类场景；「默认 opt-in」的准确范围是**第三方通用插件**，bundled 的 platform/后端、memory、context engine、model provider 均自动加载（HMS-06）。

### 下一章预告

决策表里「MCP server」占了四行，接下来两章就是它的两条子路线。第 4 章走**社区 ha-mcp**——它有一份把 Hermes 列为受支持客户端的 Setup Wizard，三种 transport 的 YAML 可以直接抄，但也有自己的一堆边界（`/readonly` 是连接级模式、端点只认 Streamable HTTP、作用域是「全部实体」而非「仅已暴露」）。第 5 章走**HA 官方 `mcp_server`**——那条路没有官方 Hermes 示例，配置得自己拼，而且鉴权要求跨版本相反，必须带版本号写。

### 本章来源

HMS-03 `website/docs/reference/toolsets-reference.md`（同名叠加不遮蔽句，本轮已回源逐字）；HMS-04 `website/docs/reference/mcp-config-reference.md`（`include`/`exclude` 语义与优先级、`trust` 与 `readOnlyHint` 原文、`tools` 结构）；HMS-05 `website/docs/user-guide/features/skills.md`（skills 定义；smart-home 仅 `openhue`）；HMS-06 `website/docs/user-guide/features/plugins.md`（`ctx.register_tool()` 签名、hello-world 最小示例、opt-in 限定词与例外表）；HMS-07 `website/docs/reference/cli-commands.md`（`hermes mcp` 子命令表）；HMS-10 `website/docs/guides/use-mcp-with-hermes.md`（旧前缀写法、`/reload-mcp`）；HMS-11 `website/docs/user-guide/features/mcp.md`（旧前缀写法）；HMS-12 `website/docs/developer-guide/creating-skills.md`（SKILL.md frontmatter 与正文五段结构）；SRC-04 `tools/mcp_tool_schema.py`（`MCP_TOOL_NAME_PREFIX`、`sanitize_mcp_name_component`、64 字符截断与 8 位 sha256）；SRC-07 `hermes_cli/mcp_config.py`（`cmd_mcp_test` 打印原生工具名）。`openhue` SKILL.md 片段与 optional-skills 目录清单经 `research/probe-02-hermes-tools.md`、`research/probe-05-recipes.md` 逐字采集，该二文件不在 canonical 注册表内，正文按其原文引用。

---

## 第 4 章：落地（一）——用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）

第 1 章盘完起点后留下一句话：内置的 4 个 `ha_*` 工具缺三块能力——历史/统计、写配置（自动化）、摄像头。这一章给出一条能一次性补齐三块的路：社区项目 ha-mcp。它值得放在第一条讲，理由不只是"能力强"，而是它的 Setup Wizard 里**已经有一个专门的 Hermes 分支**——给出的 YAML 是按 Hermes 的配置结构写好的，你不需要自己猜键名、试缩进。相对地，第 5 章的官方路线没有 Hermes 示例，那份配置是你拼的。

### 4.1 为什么先讲这条

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

### 4.2 三种 transport 的 YAML

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

### 4.3 鉴权两种写法

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

### 4.4 传输与只读端点

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

### 4.5 工具集裁剪与排错

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

### 4.6 落点配置

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

### 下一章预告

下一章换到另一条 MCP 子路线：Home Assistant 官方的 `mcp_server` 集成。它的能力比 ha-mcp 窄——实体作用域只有"已暴露给 Assist 的那些"，也没有写配置、历史、摄像头——但它最大的不同是：**官方页面给了 6 个第三方客户端示例，里面没有 Hermes**。所以第 5 章那份配置是拼出来的，会整份标注"拼接·未验证"，并且要在 2026.9 与 2026.10 两个 HA 版本之间分清一个行为相反的点。

---
### 本章来源

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

---

## 第 5 章：落地（二）——用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）

上一章走的是社区项目 ha-mcp。这一章换到另一条子路线：Home Assistant **自带**的 MCP Server 集成（`mcp_server`）。它的来源更权威、维护方就是 HA 官方，能力却明显更窄。而本章有一个必须先摆在最前面的前提：**官方页面给了 6 个第三方客户端的配置示例，里面没有 Hermes**。这意味着本章给出的 `mcp_servers` 条目不是官方口径，而是本册按官方端点规格拼出来的——**整份标"拼接，未经官方或实机验证"**，请按这个性质使用。

### 5.1 端点与「无官方 Hermes 示例」的事实

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

### 5.2 鉴权：LLT bearer 优先

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

### 5.3 OAuth / IndieAuth 的约束与未验证项

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

### 5.4 反代与隧道

如果你的 Hermes 不在 HA 同一网段、要通过 Cloudflare Tunnel 之类的反代接过去，官方有一段专门的提示：

> When accessing Home Assistant remotely through a reverse proxy or tunnel (such as Cloudflare Tunnel), the hostname used by the remote LLM client must match the configured **Internal URL** or **External URL** in Home Assistant… If an unconfigured hostname or proxy header mismatch is used, Home Assistant cannot resolve the `issuer` in `/.well-known/oauth-authorization-server` and returns relative paths, which causes conforming OAuth clients to reject the metadata.

[^c5-HAS01-PROXY]

关键点是**主机名必须落在 HA 已配置的 Internal URL 或 External URL 上**。失败模式也很具体：HA 解析不出 `issuer`，于是 metadata 里返回**相对路径**，而合规的 OAuth 客户端要求绝对路径——客户端在"读元数据"这一步就拒了，根本走不到登录。所以如果你看到的报错发生在授权之前、且措辞是"metadata 被拒"，先查主机名，不要查令牌。

官方在同一个提示框里还给了替代方案：**用 Home Assistant Cloud（`https://<your-id>.ui.nabu.casa`）是推荐做法，因为它避开了反代与隧道的配置坑**。[^c5-HAS01-PROXY]

注意这条提示出现在 `#### OAuth` 小节里——它讲的是 OAuth metadata 的解析。走 LLT bearer 的话，请求头里带着令牌直接打 `/api/mcp/assist`，不经过 metadata 发现那一环，所以这条约束对 LLT 路径不直接适用。但反过来理解也成立：**LLT 之所以在反代场景下更稳，部分原因就是它跳过了这条最容易踩的路径。**

### 5.5 跨版本行为相反

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

### 5.6 工具集裁剪

Hermes 侧的裁剪规则与第 4 章完全一致，不重复展开：用 `tools.include` / `tools.exclude`，写**服务端原生工具名**，两者都设时 `include` 优先。[^c5-HMS04-TOOLS] 差别只在于"原生名"是什么：第 4 章是 ha-mcp 的 `ha_get_state` 那一套；这里是**你所选 LLM API 暴露的工具名**（Assist 默认那套，形如 `HassTurnOn`、`GetLiveContext` 等）。[^c5-HAS01-TOOLS]

所以这里的操作顺序跟第 4 章略有不同：**先探测、再写白名单**。不要凭猜测往 `include` 里填名字——填错的效果是"白名单匹配不到任何工具，于是什么都不注册"，而且不会报错。先用 `hermes mcp test ha-official` 拿到真实工具清单，再挑需要的写进去。

顺带说明官方集成对 MCP 能力的支持范围，因为它决定了你能裁到什么：官方页面自陈目前只支持 MCP 特性的一部分——**Prompts 支持、Tools 支持、Resources 支持（仅 Assist）、Sampling 不支持、Notifications 不支持**。[^c5-HAS01-LIMITS] 没有 Sampling 与 Notifications，意味着这个 server 不会主动向客户端推消息，也不能让服务端反过来调用 LLM。

### 5.7 落点对照

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

### 下一章预告

下一章换一个方向：不再讨论"怎么把工具接进来"，而是讨论"接进来之后，谁来触发它"。事件转发默认一条都不开、逐实体限流、cron 把结果投回 HA 时有两条分支、以及长报告为什么会被静默砍尾——那是一份 `platforms.homeassistant.extra` 配置片段。

---
### 本章来源

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

---

## 第 6 章：事件驱动与定时任务——白名单过滤、逐实体限流、投递两条分支与 4096 截断

接入已经完成，白名单也照着文档配过了。但真把 Hermes 挂在 Gateway 上跑一夜，你会撞上三个文档没讲透的问题：**为什么半夜被 3000 条传感器消息刷屏**（限流到底是全局还是逐实体）、**为什么 cron 发的日报没进 HA 通知面板**（投递其实有两条分支）、**为什么一份写得挺全的日报到 HA 里只剩半截**（4096 硬截断，而且不分片）。

本章把这三件事逐个拆开，最后收敛成一份可直接抄的 `platforms.homeassistant.extra` 配置片段和一份 cron 投递写法。凡是官方没写、靠源码事实拼出来的地方，都会显式标记出来。

> [!note] 本章与既有笔记 06 的分工
> `watch_domains` / `watch_entities` / `ignore_entities` / `watch_all` 四个开关与「事件转发默认全关」这两件事，已在 `AI学习/Hermes Agent/Hermes Agent 上手实战/06-多平台接入与定时任务.md` 的「Home Assistant：智能家居双向接入」段讲完。本章不重述，只做引用，篇幅全部给三个增量：**逐实体限流 / 出站两条分支 / 4096 硬截断**。

### 6.1 入站：默认全关与逐实体限流

先把「默认全关」这条基石补一次源码侧的证词，然后进入本章第一个增量。

**默认全关：源码与文档的措辞可以互证**

你已经知道「不配白名单就一条都不转发」。这条在源码里的落点是 `HomeAssistantAdapter._passes_filters()`，它的 docstring 一句话就写死了策略（[`plugins/platforms/homeassistant/adapter.py`](https://github.com/NousResearch/hermes-agent/blob/main/plugins/platforms/homeassistant/adapter.py)，SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
def _passes_filters(self, entity_id: str) -> bool:
    """Closed by default: requires watch_domains, watch_entities, or watch_all."""
    if entity_id in self._ignore_entities:
        return False                                    # ignore 优先，先于任何白名单判断
    if self._watch_domains or self._watch_entities:
        return _domain_of(entity_id) in self._watch_domains or entity_id in self._watch_entities
    return self._watch_all                              # 三个都没配 → False
```

`connect()` 里还有一段启动期告警，逐字如下（SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
if not (self._watch_domains or self._watch_entities or self._watch_all):
    logger.warning(
        "[%s] No watch_domains, watch_entities, or watch_all configured. "
        "All state_changed events will be dropped. Configure filters in "
        "your HA platform config to receive events.",
        self.name)
```

Hermes 官方文档在 [`user-guide/messaging/homeassistant`](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant)（HMS-08）也有一句可直接对照的原文：

> By default, **no events are forwarded**. You must configure at least one of `watch_domains`, `watch_entities`, or `watch_all` to receive events. Without filters, a warning is logged at startup and all state changes are silently dropped.

两边措辞不同但结论一致：**默认丢弃，且是静默丢弃**（只在启动时打一条 warning）。注意 `ignore_entities` 在源码里排在最前面——它在白名单之前生效，所以「同一个实体既在 `watch_domains` 里又在 `ignore_entities` 里」的结果是**被忽略**，不是被转发。

**增量一：`cooldown_seconds` 是逐实体限流，不是全局限流**

这是本章第一个真正的增量，也是最容易配错的地方。

先看源码怎么写的（SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
self._cooldown_seconds: int = int(extra.get("cooldown_seconds", 30))
self._last_event_time: Dict[str, float] = {}   # entity_id -> last event ts
```

```python
# plugins/platforms/homeassistant/adapter.py（_handle_ha_event 内）
now = time.time()
if (now - self._last_event_time.get(entity_id, 0)) < self._cooldown_seconds:
    return
self._last_event_time[entity_id] = now
```

关键在第二行那个类型标注：**字典的 key 是 `entity_id`**。也就是说，限流窗口是**每一个实体各自一份**，而不是整个平台共用一个计时器。`cooldown_seconds: 30` 的含义是「**同一个实体**两次事件之间至少隔 30 秒」，而不是「整个 HA 平台每 30 秒最多放一条」。

Hermes 文档的配置表其实说对了这一半——HMS-08 的表格里 `cooldown_seconds` 的描述原文是 `Minimum seconds between events for the same entity`，「for the same entity」对上了。但文档没有把它推到**运维后果**那一步，而这正是你半夜被刷屏的原因。

**带具体值的可代入例子。** 假设你配置如下：

```yaml
# ~/.hermes/config.yaml（节选）
platforms:
  homeassistant:
    enabled: true
    extra:
      watch_domains: [sensor]
      cooldown_seconds: 30
```

家里有 12 个 `sensor.*` 实体在活跃上报（温度 3 个、湿度 2 个、电量 4 个、功率 2 个、还有 1 个光照）。每个实体各自 30 秒最多出一条，于是：

| 时间窗口 | 最坏情况条数 | 说明 |
|---|---|---|
| 30 秒 | 12 条 | 12 个实体各自踩着自己的 30 秒窗口 |
| 1 分钟 | 24 条 | 每条事件都会触发一次 agent 处理，即一次 LLM 调用 |
| 1 小时 | 1440 条 | 这还是「每个实体只变一次/30 秒」的保守估计 |
| 一整夜（8 小时） | 11520 条 | 电量类传感器常常比这更密 |

想让「平台级」限流到 30 秒一条，靠 `cooldown_seconds` 是**做不到**的——它压根没有全局计数器。

> [!tip] 大白话
> 把 `cooldown_seconds` 想成**每个员工各自一个打卡机**，而不是「整个公司共用一个门禁闸机」。你设 30 秒，意思是「同一个人 30 秒内只能刷一次卡」；但公司有 12 个人，每个人都能独立刷，所以 30 秒内最多能进来 12 次。想真正控总量，只能**减少上班的人数**——也就是收窄 `watch_entities`，而不是把 30 调大。
> 所以：`cooldown_seconds` 管的是「同一个实体别重复吵我」，管不了「一共别吵我太多次」。

**高密度事件域（传感器类）的调参思路**

既然限流是逐实体的，调参就必须**按实体**做，而不是按平台做。三条经验规则：

| 噪声场景 | 现象 | 建议做法 |
|---|---|---|
| 单个高频传感器（功率、电量、CPU/内存占用） | 该实体每 30 秒一条，全天数千条 | 放进 `ignore_entities`；或者干脆不把它所在域放进 `watch_domains` |
| 整类域全开（例如 `sensor`） | 条数 ≈ 活跃实体数 × (1/30s)，随设备增加线性膨胀 | 改成 `watch_entities` 逐个点名，只留你真正关心的那几个 |
| 需要即时性的门磁 / 人体存在（`binary_sensor`） | 拉长 cooldown 会漏掉「开了又关」 | 保留短 cooldown（甚至调小），但用 `watch_entities` 精确到具体设备；不要用 `watch_domains: [binary_sensor]` |
| 状态值抖动型（模拟量小幅跳变） | 同一实体在阈值附近反复触发 | 先在 HA 侧用 automation 或模板传感器做去抖/取整，再让 Hermes 看结果 |

这里有个常被忽略的结构性事实：源码里 `_format_state_change()` 会在**新旧值相同时直接返回 `None`**（SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
if old_val == new_val:
    return None
```

也就是说「值没变」的事件不会转发出去，但**同一次 `state_changed` 里哪怕属性变了、state 字符串没变，也不会转发**。这对传感器是好事（少了很多噪声），但也意味着「属性变化」类事件（例如 `current_temperature` 变了而 `state` 仍是 `heat`）你不会收到——这类需求要么走 HA 侧 automation，要么走 MCP 工具主动查询。

> [!warning] 一个容易踩的排查误区
> 配了 `cooldown_seconds: 300` 却仍觉得吵，第一反应往往是「限流没生效」。实际上更可能是 `watch_domains` 里开了整个 `sensor` 域，几十个实体各自 300 秒一条。**先用 `ignore_entities` 把最吵的那几个点名关掉，再考虑动 cooldown。**

**事件消息长什么样：模板决定了 agent 的输入**

还有一个和调参直接相关的问题：**转发出去的那条消息，内容是什么？** 你转发的不是原始 JSON，而是一句被模板渲染过的人话。源码里每个域一个模板（SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py
_TURNED = "[Home Assistant] {name}: turned {on_off}"
_DOMAIN_TEMPLATES = {
    "climate": (
        "[Home Assistant] {name}: HVAC mode changed from "
        "'{old}' to '{new}' (current: {temp}, target: {target})"
    ),
    "sensor": "[Home Assistant] {name}: changed from {old}{unit} to {new}{unit}",
    "binary_sensor": "[Home Assistant] {name}: {new_trig} (was {old_trig})",
    "light": _TURNED,
    "switch": _TURNED,
    "fan": _TURNED,
    "alarm_control_panel": "[Home Assistant] {name}: alarm state changed from '{old}' to '{new}'",
}
_DEFAULT_TEMPLATE = "[Home Assistant] {name} ({entity_id}): changed from '{old}' to '{new}'"
```

`name` 取值是 `attributes.friendly_name`，取不到才退回 `entity_id`；`unit` 取 `attributes.unit_of_measurement`。这带来两个实操结论：

| 现象 | 原因 | 怎么办 |
|---|---|---|
| 同一实体的事件文案一模一样，分不清是哪台设备 | 多个实体没设 `friendly_name`，或重名 | 在 HA 里给实体补 `friendly_name`；否则模板回退用 `entity_id`，可读性差 |
| 传感器消息里没有单位 | 该实体没设 `unit_of_measurement` | 在 HA 侧补上，模板会拼成 `21°C → 22°C` |
| 有些域的事件几乎没有信息量 | 未列在 `_DOMAIN_TEMPLATES` 里的域走 `_DEFAULT_TEMPLATE`，只有新旧值 | 接受它，或者在 HA 侧先把关键属性做成模板传感器 |

模板长度也是要记账的——每条事件消息都会占用上下文。开着整个 `sensor` 域时，模板会把它渲染成 `changed from 21°C to 22°C` 这样的短句，**短句本身不贵，贵的是「条数 × 每条一次 LLM 调用」**。这就是为什么 6.1.2 里那张表要按「条数」而不是「字数」来算账。

### 6.2 出站两条分支：走哪条由执行位置决定，不由消息内容决定

这是本章的核心增量，也是全册最重要的「文档与代码不一致」实例之一（第 8 章会把它作为索引条目再次点到，展开在这里）。

**两条分支的存在**

HA 平台适配器里有两套完全不同的出站实现——注意是**两套**，不是一套带开关：

```python
# plugins/platforms/homeassistant/adapter.py（gateway 进程内的适配器方法）
async def send(self, chat_id: str, content: str, ...) -> SendResult:
    """Send a notification via HA REST API (persistent_notification.create).

    REST rather than the WebSocket, to avoid racing the listener loop that
    reads from the same WS connection.
    """
    url = f"{self._hass_url}/api/services/persistent_notification/create"
    payload = {"title": "Hermes Agent", "message": content[:self.MAX_MESSAGE_LENGTH]}
```

```python
# plugins/platforms/homeassistant/adapter.py（脱离 gateway 的独立发送函数）
async def _standalone_send(pconfig, chat_id: str, message: str, ...) -> Dict[str, Any]:
    """Send via the HA ``notify.notify`` service without a live gateway adapter.
    ...
    """
    url = f"{hass_url}/api/services/notify/notify"
    payload = {"message": message, "target": chat_id}
```

注册处把两条路都挂上了（SRC-02）：

```python
# plugins/platforms/homeassistant/adapter.py（register() 内）
ctx.register_platform(
    name="homeassistant", label="Home Assistant", adapter_factory=HomeAssistantAdapter,
    ...
    standalone_sender_fn=_standalone_send,  # out-of-process cron delivery via notify.notify
    max_message_length=HomeAssistantAdapter.MAX_MESSAGE_LENGTH, emoji="🏠", allow_update_command=True)
```

`standalone_sender_fn` 这个字段本身登记在 gateway 的平台注册表里（[`gateway/platform_registry.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/platform_registry.py)，SRC-09）：

```python
# gateway/platform_registry.py
standalone_sender_fn: Optional[Callable[..., Awaitable[dict]]] = None
# 注释：prefer standalone_sender_fn when the standard send contract suffices.
```

**判定条件：唯一权威表述在源码 docstring 里**

现在关键问题：**什么时候走哪条？**

答案不在任何面向用户的文档页里，而在 `cron/scheduler_delivery.py` 的 `_deliver_result` docstring 中（[`cron/scheduler_delivery.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler_delivery.py)，SRC-08）。逐字原文是：

> With ``adapters``/``loop`` (gateway running) the live adapter is tried first (E2EE rooms can't use the standalone HTTP path), then standalone fallback.

函数签名里的参数默认值是 `_deliver_result(job, content, adapters=None, loop=None, ...)`。翻译成可判断的规则：

| 执行位置 | 判定依据 | 实际调用 | 消息形态 |
|---|---|---|---|
| **gateway 进程内执行** | `adapters` / `loop` 有值（gateway 在跑） | `POST /api/services/persistent_notification/create` | `{"title": "Hermes Agent", "message": ...}`，标题**固定**为 `Hermes Agent` |
| **脱离 gateway 执行** | `adapters is None` 且未命中外部 worker 标记 | `POST /api/services/notify/notify` | `{"message": ..., "target": chat_id}`，**没有 title 字段** |
| **detached worker** | `_HERMES_CRON_EXTERNAL_WORKER` 环境变量命中且 `adapters is None` | 不打 HTTP，进 `cron.delivery_queue` 持久队列 | 由当前/替补 gateway 用 live adapter 完成，最终仍是 persistent notification |

还有一条容易忽略的细节：第一条分支的 docstring 写的是「live adapter is tried first … **then standalone fallback**」——**gateway 内执行时 live adapter 失败，还会自动退到 standalone 路径**。也就是说「gateway 在跑」并不保证一定走 persistent notification，只是「优先走」。

> [!tip] 大白话
> 把两条分支想成两种转达方式。**第一条**是「让值班前台（gateway 进程）帮你登记到公告板」——登记完还留着，你看不看都在那儿（persistent notification 要手动 dismiss）。**第二条**是「前台下班了，你把纸条塞给大楼里第一个遇到的传达室」——谁收下就由谁决定送到哪。第二条件在源码里的名字，恰好就叫 `notify.notify`：HA 官方说它是「第一个能找到的 notify action」。
> 所以「消息发去哪」这件事，取决于**发消息时前台在不在岗**，跟你消息里写了什么、HA 怎么配的，都无关。

**官方文档只写了一条路（不完整陈述）**

Hermes 官方文档 `user-guide/messaging/homeassistant`（HMS-08）在 `### Agent Responses` 小节里，对这个问题的陈述是**无条件的**：

> Outbound messages from the agent are delivered as **Home Assistant persistent notifications** (via `persistent_notification.create`). These appear in the HA notification panel with the title "Hermes Agent".

同一页在 `### Connection Management` 里也只补了一句 `**REST API** for outbound notifications (separate session to avoid WebSocket conflicts)`。**该页通篇不提 cron、不提 `_standalone_send`、不提 `notify.notify`。**

> [!warning] 性质标注：这是「代码实际行为」，不是「官方说明」
> 上面那条分支规则（`adapters`/`loop` 有值走 live adapter、否则走 standalone）**唯一权威表述在源码 docstring**（SRC-08）。Hermes 官方文档只写了 persistent notification 一条路。因此本章写的分支行为，属于**源码级事实**，不是官方口径；如果哪天官方补了文档，两边应以代码为准。
> 另外，`plugin.yaml` 的 description 字段确实提了 `notify.notify`，但没有定义「out-of-process」的判定条件（SRC-03）。该文件复核阶段已补快照（`sources/SRC-03-ha-plugin.yaml`，820 字节全文）并逐字比对：description 原文只说 “Out-of-process cron delivery via the ``notify.notify`` service is also supported.”，确实只声明支持、不给条件——文档缺口成立。

**怎么判断自己撞上了哪条分支**

两条分支的**可观测差异**很明确，不用读源码也能分辨：

| 观察点 | 走 `persistent_notification.create` | 走 `notify.notify` |
|---|---|---|
| HA 通知面板（铃铛图标） | **有**这条通知，标题固定是 `Hermes Agent` | **不一定有**——目标由 HA 第一个能找到的 notify action 决定 |
| 消息标题 | 固定 `Hermes Agent`（源码里写死的 `"title": "Hermes Agent"`） | **没有 title 字段**，只有 `message` 和 `target` |
| 通知的消失方式 | 一直留着，直到用户手动 dismiss | 取决于实际接手的 notify action 是谁 |
| 目标选择 | 明确就是「当前这个 HA 前端」 | 由 `target` 参数 + HA 的 action 解析决定 |

排查动作也就三步：**先在 HA 通知面板里找标题为 `Hermes Agent` 的通知**；找得到，说明走的是 gateway 内分支；找不到但 agent 又说「已送达」，那大概率落到了 `notify.notify` 的不确定目标上——这时候要回头确认 cron 任务是不是在**脱离 gateway**的路径里跑的。还有一条更隐蔽的情况：gateway 内执行时 live adapter 尝试失败后会退到 standalone（docstring 里那句 `then standalone fallback`），这种「先失败后降级」不会在 HA 面板留下痕迹。

> [!tip] 大白话（再补一句）
> 判断方法其实很土：**看公告板上有没有你的纸条，以及纸条上有没有标题**。有标题（Hermes Agent）→ 前台登记了；没标题、或者公告板上找不到 → 纸条交给了「第一个遇到的传达室」，去哪全凭运气。

**两条分支在 HA 语义上并不同质**

第二条分支依赖的 `notify.notify`，是 HA 官方自己**明确警告过**的动作。HA 官方 [`integrations/notify`](https://www.home-assistant.io/integrations/notify/) 页（HAS-24）原文：

> **Send a notification** (`notify.notify`): shorthand for the first notify action Home Assistant can find. The destination is therefore not explicitly selected and the message might not be sent where you expect. Choose a specific action or notify entity when the destination matters.

对照一下第一条分支用的 [`persistent_notification.create`](https://www.home-assistant.io/integrations/persistent_notification/)（HAS-15）：它是 HA 内置的集成，动作定义是「Creates a persistent notification in the Home Assistant frontend」，参数为 `message`（必填）、`title`（可选）、`notification_id`（可选）；该集成同时还会以 `notify.persistent_notification` 的形式暴露成一个 notifier。**目标位置是确定的**——就在 HA 前端通知面板里。

于是结论很清楚：

- **第一条分支**：位置确定（HA 面板），有固定标题，**会一直留着直到用户手动 dismiss**。
- **第二条分支**：位置由 HA 「第一个能找到的 notify action」决定，**可能不在你预期的地方**，而且没有标题字段。

同一个 cron 任务，只因为执行位置不同，投递的**语义、落点、可见性**都会变。这就是为什么「我的日报明明发出去了，HA 面板里却没有」这类问题的根因常常在这里。

### 6.3 4096 硬截断：超长内容被静默砍尾

第三个增量，也是最容易造成「内容看起来发出去了、其实少了一半」的地方。

**源码：切片，不是分片**

```python
# plugins/platforms/homeassistant/adapter.py
class HomeAssistantAdapter(BasePlatformAdapter):
    MAX_MESSAGE_LENGTH = 4096
```

```python
# plugins/platforms/homeassistant/adapter.py（send() 内）
payload = {"title": "Hermes Agent", "message": content[:self.MAX_MESSAGE_LENGTH]}
```

`content[:4096]` 是**切片**——Python 的字符串切片在超界时不会报错，只会把多出来的部分**安静地丢掉**。没有分片、没有续传、没有「内容过长」的提示，`SendResult` 依然是 `success=True`（只要 HTTP 状态码小于 300）。

注册处还把这个上限抄了一份给平台注册表：`max_message_length=HomeAssistantAdapter.MAX_MESSAGE_LENGTH`（SRC-02）。

**对比：其他平台是分片的**

HA 通道**没有设置** `splits_long_messages`，而基类默认是 `False`（SRC-10 的定点记录，见下表）。其它主流平台在同样的基线里都把这位置成了 `True`：**当内容超过上限时切成多条依次发送**，而不是砍掉尾巴。

| 平台 | 单条上限 | 超限时行为 |
|---|---|---|
| **Home Assistant** | 4096 | **硬切**（`content[:4096]`），余下部分静默丢弃 |
| Telegram | 4096 | 分片 |
| Discord | 2000 | 分片 |
| Slack | 39000 | 分片 |
| Signal | 8000 | 分片 |

> [!note] 性质标注
> 上表 HA 一列是源码逐字事实（SRC-02：`MAX_MESSAGE_LENGTH = 4096` 与 `content[:self.MAX_MESSAGE_LENGTH]`）。其余四行的「上限 + 分片」来自 SRC-10 的定点记录（P2 阶段读取 `gateway/platforms/base.py` 与各平台适配器所得），**本章未逐平台回源核对**，仅作为对照参照。

**带具体值的可代入例子。** 你让 cron 每天 8 点把家里的日报投到 HA。agent 生成的正文字符数（含 Markdown）是 6200：

| 部分 | 字符区间 | 结果 |
|---|---|---|
| 标题段 + 天气 + 门窗状态 | 0 – 4096 | 送达，出现在 HA 通知面板 |
| 设备异常汇总 + 电量提醒 | 4096 – 6200 | **完全消失**，日志里没有任何报错 |
| `SendResult` | — | `success=True` |

2104 个字符无声蒸发，而你的 cron 任务状态是「投递成功」。

> [!tip] 大白话
> 把 HA 通道想成一个**只能装 4096 格子的文件柜**。别的平台（Telegram、Discord）是「一个柜子装不下就再开一个柜子，编号连着放」；HA 这里是「装到第 4096 格，把剩下的纸直接扔碎纸机」——而且不告诉你扔了。所以「日报为什么只有前半截」不是 bug，是切片的正常行为。

**怎么发现自己的内容被砍了**

截断最麻烦的地方是**它不留痕迹**：cron 任务状态是成功，HA 那边也没有报错，唯一的信号是「你看到的内容比预期短」。三个自查动作：

| 动作 | 看什么 | 判据 |
|---|---|---|
| 数一下 HA 面板里那条通知的字数 | 实际落地的长度 | 接近 4096 → 极可能被切了 |
| 把 HA 面板内容与 agent 产出的原文对一遍 | 结尾是否停在一个**断句/断词**处 | 结尾突兀、最后一个句子不完整 → 被切 |
| 直接量 agent 输出长度 | 生成内容的字符数 | 超过 4096 → 必然被切，且超出部分全丢 |

这里有个反直觉点值得单独说：**同一个 cron 任务，投到 HA 会被切，投到 Telegram 就不会**——因为 Telegram 通道是分片的。所以「内容太长」这件事本身不是错误，错误是**选了不分片的通道**。如果一份日报既要进 HA 面板、又要在 IM 里看全文，正确做法是同一个任务写两个投递目标（逗号分隔），让 HA 拿摘要、IM 拿全文。

**三条对策**

| 对策 | 做法 | 适用 |
|---|---|---|
| **压到 4096 以内** | 在 cron 的 prompt 里明确写「总长不超过 3500 字符」「只报异常项，正常项合并成一行」 | 日报/巡检类，最省事 |
| **分多次投递** | 把日报拆成多个 cron 任务，或用 `deliver: "telegram,homeassistant"` 同时投多个目标，让长文走分片平台 | 内容确实长的场景 |
| **换通道** | 长报告主投 Telegram / Discord（有分片），HA 侧只投一行摘要 | 人在 HA 面板看、长文在 IM 看 |

第三种在实践里最稳：HA 通知面板本来就是「一眼扫过去」的界面，塞 6000 字进去体验也不好。

### 6.4 cron → HA 的合法写法（按源码事实拼接）

**目标名 `homeassistant` 是合法的**

Hermes 官方 cron 文档（[`website/docs/user-guide/features/cron.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md)，HMS-09）的 `## Delivery options` 表里确实有这一行，逐字是：

```text
| `"homeassistant"` | Home Assistant | |
```

表头是 `| Option | Description | Example |`。**注意最后一列是空的**——相邻行都填了，例如 `"telegram"` 那行的 Example 列是 `Uses TELEGRAM_HOME_CHANNEL`、`"local"` 那行是 `Save to local files only (~/.hermes/cron/output/)`，**只有 `homeassistant` 这一行是空白**。

同时，目标名在代码侧是登记过的：`cron/scheduler_delivery.py` 里的 `_KNOWN_DELIVERY_PLATFORMS` 集合逐字包含 `"homeassistant"`（SRC-08）。对 HMS-09 全文（67495 字节）检索 `hass` / `Home Assistant` / `HASS_TOKEN` / `HASS_URL`，**只命中这一行**，没有任何配置片段、没有 `deliver: homeassistant` 的任务创建示例。

> [!warning] 拼接块：以下写法官方没有给过示例
> 本章 6.4.2 与 6.5 的 cron 配置写法，是**把「目标名合法」这一文档事实与「投递走哪条分支」这一源码事实拼起来的产物**，**没有任何一手端到端示例可抄，也未在实机上验证**。它的价值在于语法成立且行为可推演，但请按「先小范围试跑一次、确认落点后再上正式任务」的方式使用。

**写法（按源码事实拼接）**

先给一份可用形态。cron 任务有两种创建方式，先看 CLI 形态：

```bash
# 终端（Hermes CLI）
# 拼接写法，非官方示例：把每日巡检结果投到 HA 通知面板
hermes cron create "every day 08:00" \
  --deliver homeassistant \
  --name "home-daily-brief"
```

再看会话内让 agent 自己建的形态（`cronjob` 工具）：

```python
# Hermes 会话内，由 agent 调用的 cronjob 工具参数
# 拼接写法，非官方示例
cronjob(
    action="create",
    schedule="every day 08:00",
    deliver="homeassistant",
    name="home-daily-brief",
    prompt=(
        "汇总家里的状态并输出日报。"
        "总长严格控制在 3500 字符以内，只列异常项。"
    ),
)
```

三条必须记住的约束：

1. **`deliver` 只决定「投到哪个平台」，不决定「走哪条分支」。** 分支由执行位置决定（见 6.2）。同一份 `deliver: homeassistant` 的配置，在 gateway 进程内跑出来是 persistent notification，在脱 gateway 的调度路径里跑出来可能走 `notify.notify`——**目标位置可能不同**。
2. **prompt 里要显式限制长度**（本例写的是 3500 字符）。这不是保险起见，而是应对 6.3 的硬截断——不要指望通道帮你分片。
3. **如果日报需要固定落点**，就要确保任务在 gateway 进程内执行（即 gateway 常驻运行），否则会落到 `notify.notify` 的不确定目标上。

### 6.5 落点配置

**入站配置片段（`platforms.homeassistant.extra`）**

```yaml
# ~/.hermes/config.yaml
platforms:
  homeassistant:
    enabled: true
    extra:
      # --- 白名单：默认全关，这里逐个开 ---
      # 不要开整个 sensor 域（逐实体限流 → 实体数决定条数）
      watch_domains:
        - binary_sensor          # 门窗、人体存在：需要即时性
        - alarm_control_panel    # 报警面板状态变化
      # 传感器类改为逐个点名，只留真正关心的
      watch_entities:
        - sensor.front_door_battery
        - sensor.smoke_detector_battery
      # 已知的高频噪声源，显式关掉（ignore 优先于白名单）
      ignore_entities:
        - sensor.cpu_usage
        - sensor.memory_usage
        - sensor.uptime
        - sensor.router_power
      # --- 限流：逐实体，30 秒内同一实体只放一条 ---
      cooldown_seconds: 30
```

配套的配置说明（含文档里没有的「代价」一列）：

| 配置项 | 默认值 | 语义 | 配错的代价 |
|---|---|---|---|
| `watch_domains` | 无 | 只转发这些域的事件 | 开整个 `sensor` 域 → 条数随实体数线性膨胀 |
| `watch_entities` | 无 | 只转发这些具体实体 | 无 |
| `ignore_entities` | 无 | 永远忽略这些实体，**先于白名单生效** | 放错位置会误以为白名单失效 |
| `watch_all` | `false` | 转发所有 `state_changed` | 实际等于把整个 HA 的事件流灌进 LLM，不建议 |
| `cooldown_seconds` | `30` | **同一实体**两次事件的最小间隔 | 误以为是全局限流，调大后仍然吵 |

**cron 投递片段**

```yaml
# ~/.hermes/config.yaml（cron 相关，仅列出与本章相关的键）
cron:
  wrap_response: true        # 默认给输出加包装；要投原始输出可设 false
```

```bash
# 拼接写法（非官方示例）：日报投 HA，且限制长度以避开 4096 硬截断
hermes cron create "every day 08:00" \
  --deliver homeassistant \
  --name "home-daily-brief"
```

**落点自查清单**

上配置前逐条过一遍：

- [ ] `watch_domains` 里**没有**宽泛的 `sensor` 域（除非你确认过它的实体数量）
- [ ] 高频噪声实体进了 `ignore_entities`
- [ ] 理解 `cooldown_seconds` 是**逐实体**的，没有靠它来控总量
- [ ] 知道日报长度会被**硬切 4096**，prompt 里写了长度上限
- [ ] 知道 cron 投递有**两条分支**，走哪条取决于执行位置
- [ ] 需要固定落点（HA 通知面板）时，确认 gateway 常驻
- [ ] 记忆里有一条：平台适配器**熔断后不会自动恢复，需要 `/platform resume`**（这条既有笔记 06 已写，此处只引用，不展开）

> [!tip] 大白话
> 这一整章的配置，用一句话概括就是：**进来的门要一扇一扇开（白名单），吵闹的人单独打招呼（ignore_entities），别指望一个闸机管住全楼（cooldown 是逐实体的），出去的信要盯着它走哪个门（两条投递分支），而且信封只能装 4096 格（硬截断）。**

### 本章小结

- **入站默认全关**是源码里写死的策略（`_passes_filters` docstring：「Closed by default」），未配白名单时事件被**静默丢弃**，只在启动时打一条 warning。
- **`cooldown_seconds`（默认 30）是逐实体限流**：源码用 `Dict[str, float]` 以 `entity_id` 为 key 记时间戳。它的作用是「同一实体别重复吵」，**不是**平台级总量控制。高密度域（`sensor`）必须靠收窄 `watch_entities` + `ignore_entities` 来管。
- **出站有两条分支，判定依据是执行位置**：gateway 进程内（`adapters`/`loop` 有值）走 `persistent_notification.create`；脱离 gateway（`adapters is None`）走 `notify.notify`；detached worker 命中外部 worker 标记则进持久投递队列。**开关条件只写在源码 docstring 里**（SRC-08），官方文档只写了 persistent notification 一条路（HMS-08）。
- **两条分支不同质**：`notify.notify` 是 HA 官方警告过的「第一个能找到的 notify action」，「might not be sent where you expect」（HAS-24）。
- **HA 通道 `content[:MAX_MESSAGE_LENGTH]` 硬切 4096 且不分片**，超长内容被静默砍尾，`SendResult` 仍报成功；Telegram / Discord / Slack / Signal 均分片（SRC-02 + SRC-10）。
- **cron 目标名 `homeassistant` 合法**（HMS-09 表内一行 + SRC-08 的平台集合），但官方 cron 页该行 Example 列为空、无端到端示例；本章写法标为**按源码事实拼接**，未经官方或实机验证。

### 下一章预告

到这里，「怎么把事件接进来、把结果发出去」已经闭环。但还有一个更根本的问题没答：**这套通道的权限边界到底在哪**——你给 Hermes 的那张长期令牌，实际能碰多少东西？HA 的「暴露列表」是安全边界，还是只是设计意图？第 7 章会把 LLT 的权限真相、暴露列表的真实效力，和一份 8 步最小化清单一次讲清。

---

### 本章来源

| ID | 来源 | 类型 | 本章引用的锚点 |
|---|---|---|---|
| SRC-02 | [`plugins/platforms/homeassistant/adapter.py`](https://github.com/NousResearch/hermes-agent/blob/main/plugins/platforms/homeassistant/adapter.py) | 一手源码 | `MAX_MESSAGE_LENGTH = 4096`、`cooldown_seconds` 默认 30、`_last_event_time` 逐实体字典、`_passes_filters` docstring、`connect()` 告警、`send()` 的 `content[:…]` 与 payload、`_standalone_send()` 的 `notify/notify` 与 payload、`register()` 的 `standalone_sender_fn` |
| SRC-03 | `plugins/platforms/homeassistant/plugin.yaml` | 一手源码 | description 提到 `notify.notify` 但未给判定条件（快照 `sources/SRC-03-ha-plugin.yaml`，复核阶段逐字比对成立） |
| SRC-08 | [`cron/scheduler_delivery.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler_delivery.py) | 一手源码 | `_deliver_result` docstring（分支条件唯一权威表述）、`_KNOWN_DELIVERY_PLATFORMS` 含 `"homeassistant"`、`_HERMES_CRON_EXTERNAL_WORKER` 与 `cron.delivery_queue` |
| SRC-09 | [`gateway/platform_registry.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/platform_registry.py) | 一手源码 | `standalone_sender_fn` 字段声明 |
| SRC-10 | [`gateway/platforms/base.py`](https://github.com/NousResearch/hermes-agent/blob/main/gateway/platforms/base.py) + 各平台 adapter | 一手源码 | `splits_long_messages` 基线（HA 未设 → 硬截断；Telegram/Discord/Slack/Signal 分片） |
| HMS-08 | [Hermes 文档：Home Assistant 集成](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant) | 官方文档 | `### Event Filtering`、`### Agent Responses`、`### Connection Management`、配置表 `cooldown_seconds` 行 |
| HMS-09 | [`website/docs/user-guide/features/cron.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md) | 官方文档 | `## Delivery options` 表中 `"homeassistant"` 行（Example 列空） |
| HAS-15 | [HA 官方：Persistent Notification](https://www.home-assistant.io/integrations/persistent_notification/) | 官方文档 | 集成定位、三个动作、`notify.persistent_notification` 暴露形态 |
| HAS-24 | [HA 官方：Notify](https://www.home-assistant.io/integrations/notify/) | 官方文档 | `notify.notify` 语义警告原文 |

---

## 第 7 章：安全与限界——LLT 权限真相、暴露列表的真实效力、最小化清单

前面几章解决的是「怎么连上、怎么用起来」，本章解决的是「连上之后，它到底能动什么、不能动什么」。这个问题的答案和多数人的直觉相反：Home Assistant 的长期访问令牌（Long-Lived Token，下称 LLT）里**不装权限**，实体暴露列表**也不是运行期强制边界**。这两句话如果搞错，你会在「已经做了限制」的心理安慰下，把一个权限不受控的 agent 接进家庭网络。

本章的目标是给出一份**可以照着勾的 8 步最小化清单**（7.6 节）。在给出清单之前，需要先把每一条背后的依据、以及依据的可靠程度说清楚——哪些是官方原文，哪些是读源码推出来的，哪些只是社区自报。这个区分不是学术洁癖：本章至少有三条流传很广的说法，实际上没有官方原文可挂。

### 7.1 LLT 权限模型的真相

**一句话定位**：LLT 是一张「十年不过期的门禁卡」，卡片本身只写了编号和有效期，能进哪些门由刷卡那一刻系统查到的**用户身份**决定，而不是卡片里预存的权限清单。

**7.1.1 令牌里到底装了什么：一个看得见的产物**

要理解 LLT 的权限边界，最直接的办法是看它签发出来的字符串里有什么。HA core 签发 access token 的函数是 `async_create_access_token`，源码如下（`homeassistant/auth/__init__.py`，master 分支）：

```python
# homeassistant/auth/__init__.py
    def async_create_access_token(
        self, refresh_token: models.RefreshToken, remote_ip: str | None = None
    ) -> str:
        """Create a new access token."""
        self.async_validate_refresh_token(refresh_token, remote_ip)
        self._store.async_log_refresh_token_usage(refresh_token, remote_ip)

        now = int(time.time())
        expire_seconds = int(refresh_token.access_token_expiration.total_seconds())
        return jwt.encode(
            {
                "iss": refresh_token.id,      # 签发者：指向 refresh token 的 id
                "iat": now,                   # 签发时间
                "exp": now + expire_seconds,  # 过期时间
            },
            refresh_token.jwt_key,
            algorithm="HS256",
        )
```

JWT 的载荷里**只有三个字段**：`iss`（签发者，指向 refresh token 的 id）、`iat`（签发时间）、`exp`（过期时间）。**没有任何 scope / 权限字段**。这是「token 不带权限」这一结论的原始证据，全部来源就是这十几行。

再看校验侧。同一个文件里 `async_validate_access_token` 的返回类型标注是 `models.RefreshToken | None`——它做的事是「拿 `iss` 反查出 refresh token，再反查出用户」，而不是「读出 token 里预存的权限位」：

```python
# homeassistant/auth/__init__.py
    def async_validate_access_token(self, token: str) -> models.RefreshToken | None:
        """Return refresh token if an access token is valid."""
        try:
            unverif_claims = jwt_wrapper.unverified_hs256_token_decode(token)
        except jwt.InvalidTokenError:
            return None

        refresh_token = self.async_get_refresh_token(
            cast(str, unverif_claims.get("iss"))
        )
        # 之后是验签 + 检查 refresh_token.user.is_active，仍不看任何权限字段
```

> **来源类型说明**：以上两段属**一手源码**（canonical ID `SRC-14`），不是官方文档。正文凡引用此结论，都写成「源码里是……」，不写成「官方文档说……」。

**7.1.2 那「权限 = 创建者用户」这句话到底算什么**

**这里必须标一个性质：源码级推论，HA 文档从未明文写。**

推论的链条有三环，每一环都有源码或原文支撑：

| 环 | 证据 | 来源与档位 |
|---|---|---|
| ① 令牌绑到用户 | 创建 LLT 时传的是 `connection.user` | `SRC-14`（一手源码） |
| ② 令牌不带权限位 | JWT 载荷只有 `iss` / `iat` / `exp` | `SRC-14`（一手源码） |
| ③ 权限判定走用户 | 「These context objects also contain a user id, which is used for checking the permissions.」 | `HAS-06`（官方文档，逐字已核） |

三环合起来才能得出「LLT 的权限等于创建它的那个用户的权限」。链条是严密的，但它**不是官方的明文表述**——HA 的 auth 文档里没有一句话这么写，`auth_permissions` 页甚至**全页没有出现过 `token` 这个词**（已逐字检索，零命中）。所以落笔时不能加引号说「官方说……」，只能说「由 ① ② ③ 推出」。

这条纪律的实际后果是：当你在别处看到「HA 官方说 LLT 权限就是创建者权限」时，可以判断那个来源要么转述失真，要么是把推论写成了官方口径。

> [!tip] 大白话
> 把 LLT 想成一张**临时工牌**：卡面上只有「编号 + 有效期十年」，没有印「可以进 3 楼机房」。你刷卡时，闸机拿卡号去后台查「这张卡对应谁」，再查「这个人属于哪个组、组的权限清单是什么」。所以卡丢了不是最可怕的，**卡对应的那个人权限太大**才是最可怕的。

**7.1.3 有效期与吊销：两条必须拆开的链路**

这两件事经常被合并成一句「LLT 十年有效、也能吊销」，但它们其实是**两条独立的链路**，合并会推出错误结论。

**链路一：有效期。** 官方原文（`HAS-05`，逐字已核）：

> Long-lived access tokens are valid for 10 years.[^c7-1]

**链路二：吊销。** 官方原文（`HAS-05`，逐字已核）：

> Revoking a refresh token will immediately revoke the refresh token and all access tokens that it has ever granted.[^c7-2]

看清楚这句话的主语：是 **refresh token**；宾语是「**它签发过的**全部 access token」。它讲的是某个 refresh token 与**由它自己派生出来的** access token 之间的关系。

**为什么必须拆开写**：从链路二**不能**推出「吊销 refresh token 会撤销该用户的 LLT」。LLT 本身就是一种 refresh token（`SRC-14`：`token_type=TOKEN_TYPE_LONG_LIVED_ACCESS_TOKEN`），它被吊销时连带撤销的是它自己签发的 access token；它不会反向去撤销别的 refresh token。把两句并置而不拆开，读者很容易得出「我删掉那个 refresh token，这个用户的所有长期令牌就都失效了」——这是错的。

实践含义有两条。第一，LLT 的有效期是十年量级，「等它过期」这条兜底基本不存在，真正的兜底是**删掉这条 refresh token 或删掉这个用户**。第二，`HAS-05` 这一页**只正面写了有效期与 refresh token 的吊销语义，没有说明长期访问令牌本身如何被撤销**——用户删除、用户停用、改密码这些分支在该页都没有出现。这是一个明确的文档缺口，正文如实标注，不臆测。

可用的操作面在 WebSocket 命令上：`auth/refresh_tokens`（列出本人的 refresh token）、`auth/delete_refresh_token`、`auth/delete_all_refresh_tokens`。三者的装饰器都是 `ws_require_user`，且 `refresh_tokens` 遍历的是 `connection.user.refresh_tokens`——**只能看到本人的令牌**，看不到别人的（`SRC-14`，已逐字核对源码）。下面这段是删除逻辑的关键一行：

```python
# homeassistant/components/auth/__init__.py
@websocket_api.websocket_command(
    {vol.Required("type"): "auth/delete_refresh_token",
     vol.Required("refresh_token_id"): str}
)
@websocket_api.ws_require_user()          # 只要登录用户，不要 admin
def websocket_delete_refresh_token(hass, connection, msg) -> None:
    """Handle a delete refresh token request."""
    refresh_token = connection.user.refresh_tokens.get(msg["refresh_token_id"])
    if refresh_token is None:
        connection.send_error(msg["id"], "invalid_token_id", "Received invalid token")
        return
    ...
```

注意 `connection.user.refresh_tokens.get(...)`：查找范围是**当前用户自己的**令牌集合。这意味着一个普通用户能删自己的 LLT，但删不了别人的。

**7.1.4 一个常见误解：以为只有管理员能建 LLT**

不成立。`auth/long_lived_access_token` 这个 WebSocket 命令的装饰器是（`SRC-14`，逐字已核）：

```python
# homeassistant/components/auth/__init__.py
@websocket_api.websocket_command(
    {
        vol.Required("type"): "auth/long_lived_access_token",
        vol.Required("lifespan"): int,          # 天数
        vol.Required("client_name"): str,
        vol.Optional("client_icon"): str,
    }
)
@websocket_api.ws_require_user()                # 注意：不是 @require_admin
@websocket_api.async_response
async def websocket_create_long_lived_access_token(hass, connection, msg) -> None:
    refresh_token = await hass.auth.async_create_refresh_token(
        connection.user,                        # 令牌绑到当前用户
        client_name=msg["client_name"],
        client_icon=msg.get("client_icon"),
        token_type=TOKEN_TYPE_LONG_LIVED_ACCESS_TOKEN,
        access_token_expiration=timedelta(days=msg["lifespan"]),
    )
```

`ws_require_user()` 只要求「是一个已登录用户」，**不要求 admin**。对照 `HAS-06` 的原文——「If you need to check admin access, you can use the built-in `@require_admin` decorator.」——如果这个命令需要管理员，它就该用 `@require_admin`。

**这条为什么重要**：它把你从「LLT 只能用我的管理员账号建」这个前提里解放出来。7.2 节的细粒度只读方案**完全依赖**这一点：先建一个受限用户，再用这个用户的身份签发 LLT，令牌天然只带有受限用户的权限。

> [!tip] 大白话
> 「只有管理员能办工牌」是错觉——前台任何人都能办一张。所以正确的做法不是「少办卡」，而是**给这张卡配一个权限很小的身份**。卡的数量不重要，卡背后的身份才重要。

### 7.2 细粒度只读怎么做

**一句话定位**：想让 agent「只能读部分实体、不能写」，HA 里没有 token 级的开关，唯一的办法是把权限做在**用户 / 组**上，再用那个用户的身份发 LLT。

**7.2.1 权限模型长什么样**

`HAS-06` 原文给出三层结构，以下三句均已逐字核对：

1. **权限挂在组上**：「Permissions are attached to groups, of which a user can be a member. The combined permissions of all groups a user is a member of decides what a user can and cannot see or control.」
2. **组权限是一份 policy 字典**，当前实现只有 `entities` 一个类别，其下可分为 `entity_ids` / `device_ids` / `area_ids` / `domains`：
   「Entity permissions can be set on a **per entity and per domain basis** using the subcategories `entity_ids`, `device_ids`, `area_ids` and `domains`.」
3. **匹配顺序是 first-match**：「The system will return the **first matching result**, based on the order: `entity_ids`, `device_ids`, `area_ids`, `domains`, `all`.」

四档粒度逐字成立。下面是一份可以直接读懂的 policy（结构出自 `HAS-06` 的示例，补成完整形态）：

```json
// 组权限 policy（HA 前端「组 → 实体」编辑器保存的形态）
{
  "entities": {
    "domains": {
      "switch": true
    },
    "entity_ids": {
      "light.kitchen": {
        "read": true,
        "control": true
      }
    }
  }
}
```

注意值可以是 `true`（整块授权）或一个带 `read` / `control` / `edit` 三个子键的字典。`HAS-06` 原文：「You can either grant all access by setting the value to `True`, or you can specify each entity individually using the "read", "control", "edit" permissions.」——**「只读」在这里是 `read: true` 且不给 `control`**，这就是「细粒度只读」的全部实现方式。

**7.2.2 first-match 顺序：一个带具体值的坑**

匹配顺序 `entity_ids` → `device_ids` → `area_ids` → `domains` → `all` 意味着**前者一旦命中就返回，不再往下看**。举一个具体的例子：

假设你的 policy 是

```json
// 意图：light 域整体只读，但厨房灯要能控
{
  "entities": {
    "domains":   { "light": { "read": true } },
    "entity_ids": { "light.kitchen": { "read": true, "control": true } }
  }
}
```

这个写法**符合预期**：`light.kitchen` 先命中 `entity_ids`，拿到 `control`。

但如果把意图反过来——

```json
// 意图：灯整体可读可控，但厨房灯只读
{
  "entities": {
    "domains":   { "light": { "read": true, "control": true } },
    "entity_ids": { "light.kitchen": { "read": true } }
  }
}
```

这时 `light.kitchen` 会因为**先命中 `entity_ids`** 而只拿到 `read`，**不会被 `domains` 的 `control` 补回来**。结论：第一层的规则是「最终裁决」，不要把它当成「例外覆盖」。

**owner 豁免**：`HAS-06` 原文——「Permissions do not apply to the user that is flagged as "owner". This user will always have access to everything.」也就是说，如果你用 owner 账号建 LLT、再想靠 policy 收权限，**这套机制对你完全不生效**。这是 7.1.4「用受限用户建 LLT」的第二个理由，也是 7.6 清单第 1 条的来源。

**7.2.3 措辞上的一条硬约束**

有一个说法在社区流传很广：「权限是用户属性，不是 token 属性」。**`HAS-06` 这一页全页没有出现过 `token` 这个词**（零命中），所以这句话在这一页**无原文可挂**，正文不能加引号引它，也不能写成「官方说明」。

可以引、也足够支撑结论的，是同一页里的这一句（逐字）：

> These context objects also contain a user id, which is used for checking the permissions.

配合源码里「JWT 只装 `iss`/`iat`/`exp`」（`SRC-14`）与「命令装饰器是 `ws_require_user`」（`SRC-14`），结论同样成立——只是表述要换成「**判定以 user 对象 / `context.user_id` 为准**」，而不是「官方说权限不是 token 属性」。这不是文字游戏：前者可被官方原文与源码双重支撑，后者在两处都查不到。

> [!tip] 大白话
> 这就是「**授权清单贴在工位上，不贴在工牌上**」的区别。工牌丢了补一张就行；权限改了，改的是那份清单。审查安全时该盯的是清单（用户 / 组 policy），不是卡。所以清单给谁、给了什么，才是你真正要管的东西。

**7.2.4 操作路径（可执行）**

HA 里没有「给 LLT 设只读」的按钮，但有「给用户设权限」的界面。落到操作步骤：

| 步 | 做什么 | 界面位置 |
|---|---|---|
| 1 | 新建一个用户；**不要**勾选 owner，也不要把已有 owner 拿来用 | 设置 → 人员 → 添加人员 |
| 2 | 新建（或复用一个）组，把该用户放进组 | 设置 → 人员 → 组（或用户详情里的权限编辑） |
| 3 | 在组的实体权限里逐档收紧：优先 `entity_ids` 白名单，需要批量时用 `area_ids` / `domains` | 组编辑 → 实体权限 |
| 4 | 用**这个受限用户**的身份登录 HA，在其个人资料页底部创建 LLT | 用户个人资料 → 长期访问令牌 |
| 5 | 把这个 LLT 配给 Hermes（`HASS_TOKEN`） | `~/.hermes/.env` |

界面菜单名随 HA 版本会变，但「用户 → 组 → 实体 policy → 该用户签发 LLT」这条链在 `HAS-05` 与 `HAS-06` 两页原文里都成立。`HAS-05` 原句：「Long-lived access tokens can be created using the **"Long-Lived Access Tokens"** section at the bottom of a user's Home Assistant profile page.」

**一个必须说清的限界**：这套机制能做到「只读某些实体」，但它**做不到**「区分这是 agent 在读，还是人在读」。同一条令牌在 REST 上、在 MCP 上、在 WebSocket 上是同一份权限。

### 7.3 暴露列表：设计意图 ≠ 运行期边界

这是本章最重要的一节，也是全册唯一一处需要把「官方怎么设计的」和「实际运行时会怎样」分开写的地方。

**7.3.1 官方怎么设计的**

Assist 暴露列表的官方设计意图，原文一句话（`HAS-09`，逐字已核）：

> To be able to control your devices over a voice command, you must expose your entities to Assist. **This is to avoid that sensitive devices, such as locks and garage doors, can inadvertently be controlled by voice commands.**[^c7-3]

暴露粒度是**逐实体 + 多选批量**：文档只给了「选某个实体」和「点 Expose entities 按钮一次选多个」，**没有**按 domain 或按 area 批量暴露的入口。这一点 `HAS-09` 已回源（该页全文仅 1187 字），检索无 domain / area 批量路径。这对第 7.6 节清单第 2 条有直接影响：**「批量」这件事在暴露层做不到，只能到用户权限层去做**（后者有 `area_ids` / `domains`）。

**7.3.2 运行期它拦不住什么：三方证据并列**

把三份互相独立的材料摆在一起，结论就出来了。

**证据一（官方设计意图）**：就是 7.3.1 那句。注意它的动词是「to avoid」——要避免，是**目的陈述**。

**证据二（官方 issue 记录的穿透实例）**：`COM-14`（home-assistant/core issue #133460）记录了用户观察到的现象，原文（未删改，方括号内是原文此处即如此）：

> When I interact with the agent, such as asking it if a light is on in the house, it will [toggle a specific Input Boolean] helper called "Good night toggle". The wild thing is, that entity is not even [exposed to Assist]…

即「只读提问 → 未暴露实体被 toggle」。这条 issue 以 `not_planned` 关闭（2025-04-12），**无维护者解释**。

**证据三（第三方作者的自陈）**：`COM-12` 项目 README 的 FAQ 逐字：

> Can gpt query data that is not exposed?
> Yes, it is hard to validate whether a query is only using exposed entities.

连实现方自己都认为「查询是否只用了已暴露实体」这件事难以校验，于是它只能提供一个自评「minimum validation」的模板级折中（`is_exposed_entity_in_query` 配 `raise`）。

**另一边（把它当安全保证来陈述）**：另有第三方项目把「仅暴露实体」写在安全卖点位置。`COM-11`（`Moballo-LLC/ha-mcp-assist`）README 逐字：「the assistant only discovers and controls entities you expose」。而 `COM-01`（`homeassistant-ai/ha-mcp`）在对比表里更是直接把实体作用域当作两条路线的分界来陈述。

结论：**暴露列表是官方设计意图，不是运行期强制边界。** 你应当把它理解为「降低了模型误触的概率」，而不是「就算模型胡来也碰不到锁」。这也是为什么 7.1 / 7.2 的**用户级权限**才是本章真正的防线——暴露列表在应用层，用户权限在 API 层。

需要如实交代的是：`COM-14` 是**一手 issue（直读核验）**，可信度较高；`COM-11` / `COM-12` 是**一手项目 README（子代理采集，主流程未逐条回源）**，引用时为它们保留这个性质标注。

> [!tip] 大白话
> 暴露列表像**贴在冰箱上的「这些可以动」便签**：它表达了主人的意愿，也确实减少了误触。但它不是门锁。真正的门锁是 7.2 节那份用户权限清单——就算模型硬闯，API 层会把它拦下。检查安全时，别只看便签写得好不好，要去看看门锁上了没有。

**7.3.3 两条路线的实体作用域差异（官方明文）**

| 对比项 | HA 内置 `mcp_server` | 社区 `ha-mcp` |
|---|---|---|
| Entity scope | Only entities exposed to Assist | Everything in Home Assistant |

这两个单元格是 `COM-01` README 对比表里的**逐字原文**（同一文件内 `## 🆚 ha-mcp vs. Home Assistant's built-in MCP Server` 一节）。它不是推断，是官方路线与第三方路线的明文差异：走内置服务器时，你的暴露列表**会**起作用；走 ha-mcp 时，按它自己的陈述，实体范围是「Home Assistant 里的一切」。

把 7.3.2 和 7.3.3 放在一起看，就能理解为什么本册反复强调**先选路线再收权限**：不同路线的默认作用域根本不在一个量级上。选错路线之后，你再怎么精心维护暴露列表，也补不回那部分差异。

**7.3.4 一个已被修补的历史缺陷：不要当成当前行为**

`COM-13`（issue #177476）记录过一个静默失效：当 MCP 客户端用 area 过滤调用 `GetLiveContext` 时，**已暴露给 Assist 但没有分配 area 的实体会被静默漏掉**，响应里没有任何「跳过了实体」的提示。原文形容这「This is worse than an error」，因为 LLM 会据此得出自信的错误结论。

**必须写成「已修补」**：这个 issue 已于 2026-09-08 **closed as `completed`**，即**已经修复**。它现在的价值是作为一个**历史案例**，说明「暴露列表的维护存在静默失效的失败模式」；**不能**被当作当前版本的行为来引用。本册素材里把这条明确列为「已修复的历史缺陷要标注」，就是为了防止它被写成「HA 现在还会漏实体」。

### 7.4 MCP 侧审批面与白名单

HA 侧收完权限，MCP 侧还有一层。这层的配置项都在 Hermes 的 MCP 配置里，来源是 `HMS-04`（MCP 配置参考，官方文档，已逐字回源）。

**7.4.1 三条原则**

**原则一：`trust` 从严格侧起步。** `HMS-04` 原文：

> Trust tier: `full` (default) or `untrusted`. On an `untrusted` server, every write-capable tool call (any tool without a `readOnlyHint: true` annotation) requires user approval through the standard approval surface before it runs.[^c7-4]

默认是 `full`，也就是说**你不写 `trust`，它就不审**。同一段还明确 fail-closed：「Unrecognized values are treated as `untrusted` (fail-closed)」——写错值不会静默放行，这一点可以放心。

**原则二：不信 `readOnlyHint`。** 同一段原文继续：

> `readOnlyHint` is a server-supplied *hint* — a lying server can at most skip approval for tools it claims are read-only, never gain extra access — so mark any server you don't fully control as `untrusted`.

关键在「server-supplied」：这个提示是**服务端自己报的**。所以它不是安全机制，只是效率机制；安全边界由 `trust` 决定。文档甚至给出了失败上界：「a lying server can at most skip approval for tools it claims are read-only, never gain extra access」——最坏情况是少审几个它自称只读的工具，不会额外获得权限。

**原则三：白名单优于黑名单。** `HMS-04` 对两个键的定义分别是「Whitelist server-native MCP tools」与「Blacklist server-native MCP tools」，生效规则是「If `include` is set, only those server-native MCP tools are registered.」「If `exclude` is set and `include` is not, every server-native MCP tool except those names is registered.」，优先级是「If both are set, `include` wins.」。黑名单的问题在于**新工具默认放行**：第三方服务器发一个新版本、加一个写工具，你的 `exclude` 不会自动覆盖它，而 `include` 会。

一个容易踩的细节：`include` / `exclude` 里的名字要用**原始 MCP 工具名**（带连字符 / 点的那个），不是注册到 agent 里的 sanitize 之后的名字。`HMS-04` 原文：「Keep this in mind when writing `include` / `exclude` filters — use the **original** MCP tool name (with hyphens/dots), not the sanitized version.」

**7.4.2 配置形态**

```yaml
# ~/.hermes/config.yaml —— mcp_servers 片段
# 字段名与语义来自 HMS-04；具体值（URL / 工具名）需按你的环境替换
mcp_servers:
  home-assistant:
    url: "http://192.168.1.10:8123/api/mcp/assist"
    headers:
      Authorization: "Bearer ${env:HASS_TOKEN}"
    trust: untrusted           # 从严格侧起步：写工具一律过审批面
    tools:
      include:                 # 白名单：只注册这几个
        - "get_state"
        - "list_entities"
      # 不写 exclude；两者同时出现时 include 优先
```

**说明两点**。第一，`url` 指向 `/api/mcp/assist` 而不是 `/api/mcp`，原因是 7.6 清单第 3 条要求「只用 Assist API ID」。第二，`${env:HASS_TOKEN}` 形式的变量解析规则见第 4 章的接入段，本章不重复；这里只关心它与权限无关——**换 URL 不改变凭证权限**，这是 7.4.3 与清单第 7 条都要用到的前提。

**7.4.3 与第 5 章的交叉引用**

`/api/mcp/assist` 恒可用（`HAS-01` / `HAS-25` 原文：「the built-in Assist API is always available at `/api/mcp/assist`」），而**其他 API ID 是否要求管理员，在 2026.9 与 2026.10 两个版本之间行为相反**（`SRC-11` 的 2026.9 分支没有 `CONF_REQUIRE_ADMIN`、判断写死为 `if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin`；`SRC-12` 的 dev / 2026.10 分支新增了 `require_admin` 配置键与 `_validate_admin`）。这个跨版本差异的细节与写法在第 5 章展开，本章只用它得出一个操作结论：**如果你用的是非管理员账号，就只连 Assist，别连其他 API ID。**

> [!tip] 大白话
> 把 `trust: untrusted` 想成**给新来的外包同事配一个「动钱必须经理签字」的位置**。默认的 `full` 相当于「先签好一沓空白审批单」——省事，也意味着出事时没有刹车。`include` 白名单则像**只给他三把钥匙**，而不是给他一串钥匙再收回其中一把——后者总会漏掉新配的那把。

### 7.5 已知误报与事故机理

这一节只讲**机理与后果**：出的是什么事、为什么会出、后果能不能回滚。「这类事故发生的频率有多高」不是本章能回答的——第 9 章会说明为什么**没有任何一个来源给出过误报率的分母**。

四个已知形态：

| 形态 | 机理 | 后果 | 来源与性质 |
|---|---|---|---|
| 只读询问触发写动作 | 模型把「现在哪些灯开着」理解成一个需要执行的动作，调了服务 | 未暴露 / 未预期的实体被 toggle | `COM-14`（一手 issue，直读核验）；`COM-21`（社区帖，**社区自报，未复核**） |
| brightness 单位不一致 | 给 LLM 的是 0–255 的 `brightness`，而 `HassTurnOn` intent 期望 0–100 | 设「100%」实际约 38%，或反过来过亮 | `COM-15`（一手 issue，**子代理采集，主流程未逐条回源，未复核**） |
| 模型不支持 tools 却输出 JSON | 模型确实吐出了工具调用 JSON，但底层模型不带 tool calling 能力，调用未被执行 | 表现为「说了要做但没做」或静默失败 | `COM-20`（社区帖，**社区自报，未复核**） |
| 标签覆写导致 registry 损坏 | `ha_assign_label` 的作用是**替换**全部标签而非追加 | entity registry 受损、标签 UI 消失 | `COM-18`（一手项目相关社区帖，**子代理采集，未复核**） |

三个可以立刻用上的判断：

1. **形态一与形态三的后果方向相反**。前者是「不该动的动了」，后者是「该动的没动」。做告警设计时，这两类要分别设阈值，别用一个「异常」概括——它们需要的响应动作完全不同。
2. **单位不一致是配置层的错，不是模型的错**。`COM-15` 把责任指到了给 LLM 的值与 intent 期望范围之差这个具体位置。这类问题不能靠换模型解决，换模型只会让它以另一种方式表现出来。
3. **形态四是唯一「写权限直接造成资产损坏」的一种**，而且根因是**工具语义**（`assign` 到底是替换还是追加）而不是模型能力。这正是清单第 5 条（白名单）与第 8 条（写前 dry-run / 备份）要一起用的原因：白名单让你不引入这个工具，dry-run 与备份让你在必须用时还能退回来。

`COM-05`（`Oasis-Enterprise/mylo`，一手项目 README）给出的回滚设计可以直接抄，原文：

> Tier-2 file writes use atomic write → reload → verify → rollback-on-failure.

同项目在另一处把完整链路写成「dry-run preview → user approval → atomic write → HA reload → verification」，并说明 reload 失败会自动回滚、并告诉你哪里出了问题。

### 7.6 落点清单：8 步安全最小化

把前面六节收成一份可以逐条勾的表。顺序是有意义的：**先降身份，再收权限，再收工具面，最后才谈操作纪律**——因为前四步失效时，后面几步只能减少概率，不能兜住后果。

| # | 动作 | 依据 | 勾 |
|---|---|---|---|
| 1 | **不要用 admin / owner 账号建 LLT**，新建一个专用受限用户 | 非 admin 也能建 LLT（`SRC-14`：装饰器是 `ws_require_user`）；owner 豁免权限策略（`HAS-06` 原文） | ☐ |
| 2 | **收紧该用户的实体权限**：优先 `entity_ids` 白名单，批量用 `area_ids` / `domains`，注意 first-match 顺序 | 四档粒度 + first-match + 权限挂组（`HAS-06`，已回源逐字） | ☐ |
| 3 | **只用 Assist API ID**（`/api/mcp/assist`），不连其他 API ID | Assist 恒可用、其他 API ID 要求管理员，且该要求跨版本相反（`HAS-01` / `HAS-25`、`SRC-11` / `SRC-12`；细节见第 5 章） | ☐ |
| 4 | **`trust` 从严格侧起步**（写 `untrusted`），不接受默认值 | 默认是 `full`；未知值 fail-closed（`HMS-04` 原文） | ☐ |
| 5 | **用 `tools.include` 白名单**，不用 `exclude` 黑名单；名字用原始工具名 | 白名单生效时只注册列出的工具；黑名单会让新工具默认放行（`HMS-04`） | ☐ |
| 6 | **事件转发从「默认全关」开始**，逐个开 `watch_entities`，并按实体调 `cooldown_seconds` | 事件默认一条都不转发；`cooldown_seconds` 是**逐实体**限流（`SRC-02`，第 6 章已展开） | ☐ |
| 7 | **只读场景走 `/readonly` 端点** | `/readonly` 是**连接级**模式（`COM-01` README 原文：「This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint.」） | ☐ |
| 8 | **写配置前 dry-run / 备份 / 可回滚** | `COM-05` 的一手设计：dry-run → approval → atomic write → reload → verify → rollback | ☐ |

关于第 7 条要补一句限界：`/readonly` 只是「这条连接使用只读模式」，**同一份凭证换个端点照样能写**。所以它属于「操作纪律」，不属于「权限边界」——这也是它排在第 7 位而不是第 1 位的原因。真正的位置是：第 1–5 条是边界，第 6–8 条是纪律。

> [!warning] 本章最容易被误读的两句话
> 1. 「LLT 权限 = 创建者用户的权限」是**源码级推论**（`SRC-14`），HA 官方文档从未明文写。可引的官方原文只有「These context objects also contain a user id, which is used for checking the permissions.」（`HAS-06`），且该页全页未出现 `token` 一词。
> 2. 「暴露列表是安全边界」**不成立**——它是官方设计意图。运行期有 `COM-14` 记录的穿透实例（`not_planned` 关闭、无维护者解释），第三方作者也自陈难以校验（`COM-12`）。

### 本章小结

- LLT 的 JWT 载荷只有 `iss` / `iat` / `exp`，**不带 scope**；「权限 = 创建者用户」是**源码级推论**（`SRC-14`），不是官方明文。
- 「十年有效期」（`HAS-05`）与「吊销 refresh token 立即连带撤销其签发的全部 access token」（`HAS-05`）是**两条独立链路**，不能合并推出「吊销 refresh token 会撤销该用户的 LLT」。
- **非 admin 也能创建 LLT**（装饰器是 `ws_require_user`），这是「用受限用户建令牌」方案的前提。
- 细粒度只读只能靠**受限用户 / 组**：entity / domain / area / device 四档粒度已回源成立，还须记住 **first-match 顺序**与 **owner 豁免**。
- **暴露列表是设计意图，不是运行期强制边界**；内置 `mcp_server` 的作用域是「仅 Assist 暴露实体」，ha-mcp 自述是「Home Assistant 里的一切」。
- `COM-13` 记录的 area 过滤静默漏实体问题**已于 2026-09-08 修补**（closed as `completed`），不得当作当前行为。
- MCP 侧三层：`trust` 严格起步、不信 `readOnlyHint`、**白名单优于黑名单**。

### 下一章预告

安全讲完，下一章要处理的是另一个方向的失败：**你按文档配的东西，代码里可能根本不存在**。第 8 章会把本册收集到的 12 条「文档说 X、实际是 Y」摆成一张对照表，并给出一套「从仓库到分支到 docstring 到提交史」的自查路径——它同时也是本章多处结论（例如 `/api/mcp` 的 admin 要求、`Control Home Assistant` 这个开关）为什么必须带版本号的原因。

### 本章来源

| ID | 档位 | 位置 | 核对结果 |
|---|---|---|---|
| `SRC-14` | 一手源码 | `homeassistant/auth/__init__.py`、`homeassistant/components/auth/__init__.py`（master，2026-09-18 重取） | 逐字命中：`async_create_access_token` 只编码 `iss`/`iat`/`exp`（L607–615）；`auth/long_lived_access_token` 装饰器为 `ws_require_user`（L519–527）；`async_create_refresh_token(connection.user, ...)`（L533–539）；`connection.user.refresh_tokens` 只含本人 |
| `HAS-05` | 官方文档 | `developers.home-assistant.io/docs/auth_api/` | 逐字命中：「valid for 10 years」「immediately revoke the refresh token and all access tokens that it has ever granted」「created using the "Long-Lived Access Tokens" section at the bottom of a user's Home Assistant profile page」 |
| `HAS-06` | 官方文档 | `developers.home-assistant.io/docs/auth_permissions/` | 逐字命中：四档 `entity_ids`/`device_ids`/`area_ids`/`domains`、first-match 顺序、owner 豁免、`context` 的 user id 用于权限判定；**全页 `token` 零命中**（已检索确认） |
| `HAS-09` | 官方文档 | `home-assistant.io/voice_control/voice_remote_expose_devices/` | 逐字命中：锁 / 车库门设计意图句；暴露粒度仅逐实体 + 多选批量 |
| `HAS-01` / `HAS-25` | 官方文档 | `_integrations/mcp_server.markdown` | 逐字命中：`/api/mcp/assist` 恒可用；「Connecting to any API other than Assist requires the authenticated user to be an administrator.」 |
| `HMS-04` | 官方文档 | Hermes `reference/mcp-config-reference.md` | 逐字命中：`trust` 段全文、`include` / `exclude` 语义与 `include` 优先、`readOnlyHint` 为 server-supplied hint、原始工具名 |
| `SRC-11` / `SRC-12` | 一手源码 | HA core `components/mcp_server/` @ master / dev | 逐字命中：master 无 `CONF_REQUIRE_ADMIN`、判断写死 `api_id != llm.LLM_API_ASSIST and not is_admin`；dev 新增 `CONF_REQUIRE_ADMIN` 与 `_validate_admin` |
| `SRC-02` | 一手源码 | Hermes `plugins/platforms/homeassistant/adapter.py` | 事件默认不转发、`cooldown_seconds` 逐实体（本章仅引用，第 6 章已展开） |
| `COM-01` | 一手项目 README | `homeassistant-ai/ha-mcp` README | 逐字命中：Entity scope 对比两格；`/readonly` 段「This is a connection mode for automated agents, not a separate permission on the credential: the same credentials still work at the normal endpoint.」 |
| `COM-05` | 一手项目 README | `Oasis-Enterprise/mylo` README | 逐字命中：三层权限、`session_budget_usd` / `monthly_budget_usd`、atomic write → reload → verify → rollback |
| `COM-11` / `COM-12` | 一手项目 README（**子代理采集，主流程未逐条回源**） | `Moballo-LLC/ha-mcp-assist`、`XtracT/extended_deepseek_conversation` | 引用处已保留性质标注 |
| `COM-13` | 一手 issue | home-assistant/core #177476 | closed as `completed`，2026-09-08（**已修补**，不得当作当前行为） |
| `COM-14` | 一手 issue（直读核验） | home-assistant/core #133460 | 「未暴露实体被 toggle」；closed as `not_planned`，2025-04-12，无维护者解释 |
| `COM-15` | 一手 issue（**子代理采集，主流程未逐条回源**） | home-assistant/core #134848 | brightness 0–255 vs 0–100 单位不一致 |
| `COM-18` / `COM-20` / `COM-21` | 社区帖（**社区自报，未复核**） | HA 官方论坛 | 标签覆写 / 模型不支持 tools / 只读询问触发写动作 |

[^c7-1]: `HAS-05`，https://developers.home-assistant.io/docs/auth_api/ ，"Long-lived access token" 一节。
[^c7-2]: `HAS-05`，同上，"Revoking a refresh token" 一节。
[^c7-3]: `HAS-09`，https://www.home-assistant.io/voice_control/voice_remote_expose_devices/ 。
[^c7-4]: `HMS-04`，Hermes `website/docs/reference/mcp-config-reference.md`，`trust` 字段说明。

---

## 第 8 章：文档与代码不一致——12 条实例与自查方法

你在前面几章里已经见过好几次「文档这么说、代码那么写」了：`mcp__` 双下划线前缀、出站的两条分支、cron 页那行空白的 Example 列。它们不是偶发笔误，而是**同一类现象**：文档描述的是某个时间点的实现，代码继续往前走，两边没对齐。

这一章把这类现象集中起来，给 12 条可举证的实例，每条都能指回**具体文件、具体分支、具体行号或具体快照**——不是「文档经常不准」这种泛泛之谈，而是「这一句、在哪个版本、和哪个文件冲突」。最后给一套可复用的自查路径：以后遇到「我按文档配了却不生效」，你能自己判断是**你错了**还是**文档错了**。

### 8.1 MCP 前缀：改名不彻底

第一条，也是最能说明问题的一条。

**文档侧写的是旧写法。** Hermes 文档 `website/docs/user-guide/features/mcp.md`（HMS-11）在 `## How Hermes registers MCP tools` 小节里给的格式是：

```text
mcp_<server_name>_<tool_name>
```

并附了一张对照表，逐字如下：

| Server | MCP tool | Registered name |
|---|---|---|
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `create-issue` | `mcp_github_create_issue` |
| `my-api` | `query.data` | `mcp_my_api_query_data` |

小节末尾还写「These are registered per server with the same prefix pattern, for example: `mcp_github_list_resources`、`mcp_github_get_prompt`」。**同一个文件被发布到官方站上后，写法一模一样**——发布站的同页仍是 `mcp_<server_name>_<tool_name>` 与同样的三行对照表。另一份文档 `website/docs/guides/use-mcp-with-hermes.md`（HMS-10）举的实例也是旧写法：`mcp_chrome_devtools_win_list_pages`。

**代码侧是双下划线。** 源码 `tools/mcp_tool_schema.py`（SRC-04）里写得很硬：

```python
# tools/mcp_tool_schema.py
# ``mcp__<server>__<tool>``: the convention shared by Claude Code, Codex and OpenCode.
MCP_TOOL_NAME_PREFIX = "mcp__"

def mcp_prefixed_tool_name(server_name: str, tool_name: str) -> str:
    """Registry/wire name: ``mcp__<sanitizedServer>__<sanitizedTool>``, clamped to 64 chars with a ..."""
    full_name = f"{MCP_TOOL_NAME_PREFIX}{sanitize_mcp_name_component(server_name)}__{sanitize_mcp_name_component(tool_name)}"
```

**最讽刺的是同一仓库里还有一份写对了的文档。** `website/docs/reference/mcp-config-reference.md`（HMS-04）给的格式是正确的，逐字如下：

```text
mcp__<server>__<tool>
```

它还给了一组正确示例（`mcp__github__create_issue`、`mcp__filesystem__read_file`、`mcp__my_api__query_data`），并解释了为什么这么设计：「The double-underscore delimiter (`mcp__…__…`) matches the convention used by Claude Code, Codex, and OpenCode, and disambiguates the server/tool boundary even when either component contains underscores.」

所以这不是「Hermes 一直用单下划线所以文档没错」——**是同一个仓库里两页自相矛盾**：`features/mcp.md` 和 `guides/use-mcp-with-hermes.md` 写 `mcp_`，`reference/mcp-config-reference.md` 写 `mcp__`，而源码站在 `mcp__` 这边。

**改名不彻底：连 docstring 都没清干净。** 双下划线是某次改名（对应 issue #33533）之后的结果，但改得不彻底。两处源码文件的 docstring 至今还写着旧写法。

代码侧 `agent/anthropic_adapter.py`（SRC-05）的 `_normalize_to_mcp_wire()` docstring 逐字是：

> OAuth wire form of a tool name (no aliasing): ``mcp__<...>``. Anthropic's OAuth billing classifier treats a single-underscore ``mcp_`` tool name as a third-party-app fingerprint (HTTP 400 "Third-party apps now draw from extra usage"); ``mcp__foo`` is accepted. Both bare Hermes tools (``read_file``) and native MCP tools registered as ``mcp_<server>_<tool>`` must land on the double-underscore form. normalize_response reverses both via registry lookup.

注意最后那句：函数**把正确的双下划线写对了**，却顺手把「native MCP tools」描述成 `mcp_<server>_<tool>`（单下划线）——**同一段话里两种写法并存**。

测试侧更微妙。`tests/agent/test_anthropic_mcp_prefix_strip.py`（SRC-06）的模块 docstring 逐字是：

> Anthropic's subscription/OAuth billing classifier treats a **single-underscore** ``mcp_`` tool name as a third-party-app fingerprint and rejects the request with HTTP 400 "Third-party apps now draw from extra usage, not plan limits". So on the OAuth wire NOTHING may carry a single-underscore ``mcp_`` prefix:
>
> * bare native tools ``read_file`` -> ``mcp__read_file``
> * native MCP server tools ``mcp_linear_get_issue`` -> ``mcp__linear_get_issue``
>
> ``normalize_response`` reverses the ``mcp__`` wire name back to whatever the tool registry knows (the single-underscore ``mcp_<server>_<tool>`` form for MCP server tools, or the bare name for native tools) so the dispatcher is unaffected.

这里出现了两个不同的东西：**它的示例行用的是双下划线**（`mcp_linear_get_issue` 是改名前的注册名写法，被当成"旧名"来演示剥离），**它的结论句又说是单下划线**。而测试断言只覆盖裸工具名（`mcp__read_file` → `read_file`），**没有任何一条断言能区分两种命名约定**——也就是说，就算注册名是单下划线，这套测试照样全绿。

> [!tip] 大白话
> 把这件事想成**一条街上的门牌号改过一次**：新规是「两个短横线」，但有的路牌、有的老告示、甚至有的**施工图纸上的备注**还写着「一个短横线」。
> 你该信哪个？信**门头上实际钉着的那块牌子**（源码里的 `MCP_TOOL_NAME_PREFIX = "mcp__"`）。文档只是告示，告示抄漏了一处，门牌不会跟着抄漏。

**实用结论：** 写配置时按 `mcp__<server>__<tool>` 写；给 HA 官方或社区 MCP server 起名 `home-assistant` 时，注册名会是 `mcp__home_assistant__<tool>`（连字符被 sanitize 成下划线）。另外注意，`tools.include` / `tools.exclude` 里写的是**原始** MCP 工具名（带连字符/点的那个），不是注册名——这一条也是源码定的。

### 8.2 `Control Home Assistant`：文档有、代码无

第二条是本章唯一一条**无法定论**的。它值得写进来，正是因为它展示了这类问题的正确处理姿势：**两侧证据并列，不强行下判断。**

**文档侧：它长期存在。** HA 官方 `mcp_server` 集成文档（HAS-01）在 `## Configuration options` 小节里给的配置项，逐字是：

```text
{% configuration_basic %}
Control Home Assistant:
  description: If MCP clients are allowed to control Home Assistant. Clients can only
    control or provide information about entities that are [exposed](/voice_control/voice_remote_expose_devices/) to it.
{% endconfiguration_basic %}
```

而且 P2 阶段取回了**三段历史快照**（内容提交分别落在 2026-09-09、2026-06-12、2026-05-29），这三个时间点的 `Configuration options` 块**逐字完全相同**。这不是近期误改，是一个**长期存在的文档条目**。

**代码侧：任何分支、任何历史版本都查不到对应键。** 对照三份源码：

| 检查面 | 结果 |
|---|---|
| 当前 `master` / `rc` 分支（=HA 2026.9） | `const.py` 只有 `DOMAIN`、`TITLE`、`STATELESS_LLM_API`，**没有**任何 control / read-only 类常量 |
| `dev` 分支（=HA 2026.10） | 新增的是 `CONF_REQUIRE_ADMIN = "require_admin"`，**不是** `Control Home Assistant` |
| 目录提交史（44 条，截至 2026-09-13） | 只有两条相关：`#180713`「Add option to require an admin user for the MCP server endpoint」、`#180629`「Add options flow to MCP Server integration」；**没有任何一条**提及新增 control 或 read-only 类开关 |
| 集成首版（2025-01-02） | `config_flow.py` 从头就只使用 `CONF_LLM_HASS_API`；`strings.json` 里 `control` / `admin` 零命中 |

**dev 分支真正的那个开关，名称与语义都不是它。** `dev` 的 `strings.json` 里，选项的 UI 文案逐字是 `"require_admin": "Require an administrator account"`，说明是「Only allow administrator accounts to use the Model Context Protocol endpoint.」——它管的是**谁有权限访问端点**，不是「能不能控制设备」。`Control Home Assistant` 描述的是**能不能控制**，两者语义完全不同。

**结论：不判定真伪。** 文档侧有长期存在的证据，代码侧有「查无此项」的证据，两边都对不上。可能的解释至少有两种：它是「已删除选项的文档残留」，或者是「文档层的一种约定写法/占位」。要定论需要 HA 的 release notes 或 PR 讨论（记为本册未解决问题 **G-1**，如实留白）。

> [!tip] 大白话
> 像一本老菜谱上写着「加两勺秘制酱」，但你翻遍厨房所有调料架（`const.py`、`config_flow.py`、`strings.json`），甚至查了这个厨房**三年来买过的每一张购物小票**（44 条提交史），都没有这瓶酱。
> 有两种可能：酱被撤了、菜谱没改；或者「秘制酱」本来就是菜谱作者对某样东西的别称。**在尝到菜之前，别断言是哪一种。**

### 8.3 `/api/mcp` 的 admin 要求跨版本相反

第三条是本章唯一一条**必须带版本号才能写清楚**的。

同一个端点 `/api/mcp`，`master`/`rc` 分支（对应 HA 2026.9）与 `dev` 分支（对应 HA 2026.10）的**行为是相反的**。证据是两份 `http.py` 的模块 docstring，逐字对照：

| 分支 / 版本 | `/api/mcp` 的 docstring 原文 |
|---|---|
| `master` / `rc`（=2026.9，SRC-11） | This serves the configured LLM APIs and **does not require admin access**. |
| `dev`（=2026.10，SRC-12） | This serves the configured LLM APIs and **requires admin access when the config entry is configured to require it**. |

代码层面的配套变化也能对上：`dev` 版新增了 `_validate_admin(request, entry)`，函数体是

```python
# homeassistant/components/mcp_server/http.py（dev 分支）
def _validate_admin(request: web.Request, entry: MCPServerConfigEntry) -> None:
    if entry.data[CONF_REQUIRE_ADMIN] and not request["hass_user"].is_admin:
        raise Unauthorized
```

并把它加进了 SSE 视图、messages 视图和 Streamable 视图；`master`/`rc` 版根本没有这个函数。两个分支都保留的只有这一条：`/api/mcp/<API ID>` 里「非 Assist API 要求 admin」的判断（`if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin: raise Unauthorized`）。

> [!warning] 别把这句写成「官方要求 admin」
> 正确答案是**分版本**的：说「2026.9 的 `/api/mcp` 不要求 admin」和「2026.10 的 `/api/mcp` 在配置项打开时要求 admin」都对；只说一句「要求 admin」或「不要求」都是错的。参考手册里凡涉及这个端点的鉴权描述，务必带版本号。
> 另外 `dev` 是否最终进入 2026.10 正式版**尚未确认**（记为本册未解决问题 **G-2**：`dev` 有、`rc` 无，是否 revert 未知）。

**同一版本内，默认值还不一致。** 更绕的是 `dev` 版自己的行为：`CONF_REQUIRE_ADMIN` 的默认值**取决于这个配置项是怎么来的**：

| 场景 | 默认值 | 依据 |
|---|---|---|
| 新装的配置项 | `True`（走 `config_flow` 新建流程） | dev 的 `config_flow.py` |
| 从 1.1 迁移上来的老配置项 | `False` | dev 的 `__init__.py` `async_migrate_entry` 显式写入 `data={CONF_REQUIRE_ADMIN: False, **entry.data}`，minor_version 升到 2 |

源码自己的注释把原因写得明明白白，逐字是：

```python
# homeassistant/components/mcp_server/__init__.py（dev 分支）
# 1.1 -> 1.2: Endpoints served before this option existed stay open.
# A disabled config entry migrates only once enabled, so keep the
# choice the options flow may have saved in the meantime.
```

「**Endpoints served before this option existed stay open**」——意思是：升级前就已经在提供服务的老配置项，**保持开放**（不因为升级而突然把用户端口关掉）。所以「同版本内默认值不一致」在这里是**有意为之的兼容策略**，不是 bug；但如果只看文档或只看 UI，你会以为默认值是单一的。

> [!tip] 大白话
> 把这想成**小区换门禁**：新住户办卡时，物业默认给「刷卡才能进」（`True`）；但老住户的门本来就没锁，物业不会在换系统的当天把人锁在门外——所以老住户迁移过来时，默认还是「门开着」（`False`）。同一个小区、同一个系统，两种默认状态并存。
> 后果是：**你不能假设「别人家 HA 的 `/api/mcp` 和你家一个行为」**——先问版本，再问「你这个配置项是新装还是迁移来的」。

### 8.4 出站与 cron 的文档缺口

第四条和第五条已经在第 6 章展开过，这里只做索引，不重复论证。

| 缺口 | 文档怎么说 | 实际是怎样 | 详见 |
|---|---|---|---|
| **出站投递** | Hermes 文档说「Outbound messages from the agent are delivered as **Home Assistant persistent notifications**」——**无条件陈述**，该页通篇不提 cron / `notify.notify` | 代码里是**两条分支**，走哪条由执行位置决定（`adapters`/`loop` 有值 → live adapter；`adapters is None` → `notify.notify`） | 第 6 章 6.2 |
| **cron 投递目标** | cron 页 `## Delivery options` 表里有 `"homeassistant"` 一行，但 **Example 列是空的**（相邻平台都有值） | 目标名在代码里合法（`_KNOWN_DELIVERY_PLATFORMS` 含 `"homeassistant"`），但**文档层止于一行表项**——没有配置片段、没有端到端示例 | 第 6 章 6.4 |
| **`plugin.yaml` 的条件缺失** | `plugins/platforms/homeassistant/plugin.yaml` 的 description 提了 `notify.notify`，读起来像「一个可选的增强」 | 它**没有定义「out-of-process」的判定条件**；真正的判定条件只在 `cron/scheduler_delivery.py` 的 docstring 里 | 第 6 章 6.2 |

这一组的意义在于：**「文档没写」和「文档写错」是两种不同的失败模式**。前缀那一条是「文档写错」（写了旧写法）；这一组是「文档没写全」（只写了主路径，漏了旁路；只给了一行表项，没给例子）。后者更隐蔽——你不会觉得文档有问题，因为你看的那句话本身没错。

### 8.5 SKILL.md frontmatter 两套字段表

第六条，两份官方文档给出**互不覆盖**的字段表。

| 字段 | HMS-12（`developer-guide/creating-skills.md`） | HMS-05（`user-guide/features/skills.md`） |
|---|---|---|
| `name` / `description` / `version` / `platforms` | 有 | 有 |
| `author` / `license` | 有 | **无** |
| `metadata.hermes.tags` | 有 | 有 |
| `metadata.hermes.category` | **无** | 有（示例值 `devops`） |
| `metadata.hermes.related_skills` | 有 | **无** |
| `metadata.hermes.requires_toolsets` | 有 | 有 |
| `metadata.hermes.requires_tools` | 有 | 该文件的 `## SKILL.md Format` 示例块**无**（别的章节另有说明） |
| `metadata.hermes.fallback_for_toolsets` | 有 | 有 |
| `metadata.hermes.fallback_for_tools` | 有 | 该示例块**无**（别的章节另有说明） |
| `metadata.hermes.config` | 有 | 有 |
| `metadata.hermes.blueprint`（含 `schedule` / `deliver` / `prompt` / `no_agent`） | 有 | **无** |
| `required_environment_variables` | 有 | 该示例块**无**（别的章节另有说明） |
| `required_credential_files` | 有（在独立小节 `### Credential File Requirements`） | **无** |

两份文档都没有「本表为准」之类的措辞，仓库内也**没有找到 frontmatter 的机器可读 schema 文件**（记为本册未解决问题 **G-3**）。有一个字段尤其可疑：`related_skills` **仅在 HMS-12 出现 1 次**，HMS-05 里 0 次，且 HMS-12 没说明它的消费方是谁——是影响 `skills_list()` 的输出、还是参与检索排序，都未写（记为 **G-4**，疑似文档残留）。

**落笔取法：以 HMS-12 为主表，标注 HMS-05 的差异。** 理由有两条：HMS-12 的字段集是**超集**（HMS-05 缺的那些它都有）；它的示例块更接近「可直接抄」的完整形态。但 `category` 是个例外——HMS-05 的 L0 定义里写着 `skills_list() → [{name, description, category}, ...]`，说明 `category` 是**索引层的实字段**，HMS-12 的示例没有它更像是示例省略。

> [!tip] 大白话
> 这就像**同一道菜有两份菜谱**：一份写「盐、糖、酱油、料酒、八角」，另一份写「盐、糖、酱油、**辣椒**」。两份都不覆盖对方——你不能拿一份当另一份的勘误表，只能**两份都看**，然后按哪份更完整、更新的那份来定主表（这里 HMS-12 更新，2026-06-11 vs HMS-05 的 2026-09-17……注意：HMS-05 其实更晚，但它**缺字段**，所以字段表仍以 HMS-12 为主，只把 `category` 从 HMS-05 补回来）。
> 真正该记住的是：**没有 schema 文件时，权威性只能靠互证，不能靠断言。**

### 8.6 自查方法：仓库 → 分支 → docstring → 提交史

前面五条都是「结论」，这一节是「方法」。下次你按文档配了却不生效，按这四步走。

**第一步：先确认你看的是哪一份文档。** 同一份内容常常有三个副本：仓库内的 markdown 源文件、发布站上的渲染页、以及第三方转载。**仓库源文件是唯一能查提交时间的版本**。排查动作：在仓库里按文件名或小标题关键词定位源文件；找不到就用站点上的路径反推（本册就踩过这个坑——`creating-skills.md` 实际在 `developer-guide/` 下，P1 记的 `user-guide/features/` 路径在仓库中不存在、站点上返 404）。

**第二步：确认代码在哪个分支。** 同一个文件在不同分支可能是相反行为（见 8.3）。HA core 有 `master` / `rc` / `dev` 三条常用分支，Hermes 有 `main`。排查动作：查你要对标的版本号落在哪条分支，**先把分支名写进笔记，再下结论**。

**第三步：读 docstring，别只读实现。** 这一章里最关键的几条事实，全部来自 docstring 而不是函数体：出站分支的判定条件（`_deliver_result` 的 docstring）、`/api/mcp` 的 admin 要求（`http.py` 的模块 docstring）、两个发送路径各自的选择理由（`send()` 与 `_standalone_send()` 的 docstring）。**函数体告诉你「做了什么」，docstring 常常告诉你「为什么、在什么条件下」**。尤其注意：docstring 也是文档，也会过期（8.1 的两处就是），所以 docstring 与函数体冲突时，**以函数体为准**。

**第四步：查提交史。** 当你要判断「这个功能是根本没有，还是曾经有后来删了」，提交史是唯一手段。8.2 里「44 条提交、没有任何一条提及 control/read-only 类开关」这个结论，就是这么来的。排查动作：按目录路径拉提交列表，用关键词过滤，看有没有相关 PR 编号。

配套的症状对照表：

| 症状 | 大概率先查哪一层 |
|---|---|
| 配置项在文档里，写进去不生效 | **第二、三步**：先查版本分支，再在代码里搜这个键名是否存在（8.2 就是查无此项） |
| 配置生效了，但行为和预期相反 | **第二、三步**：多半是跨版本行为变了（8.3） |
| 文档给的字段名/格式，代码不认 | **第一、四步**：先确认文档副本是否过期，再查提交史里的改名记录（8.1） |
| 文档说「只有一种行为」，实际出现了另一种 | **第三步**：找 docstring 里的 `if … else …` 分支条件（8.4） |
| 两份文档说得不一样，且都不覆盖对方 | **全部四步**：按更新时间 + 完整度定主表，差异逐条标注（8.5） |

**顺带能查出的第九条：锚点失配。** 同一个目录提交史里还能发现更细的错位。HA `mcp_server` 的 `config_flow.py` 里定义了 `MORE_INFO_URL = "https://www.home-assistant.io/integrations/mcp_server/#configuration"`（master 与 dev 都有），而官方文档的实际标题是 `## Configuration options`，浏览器锚点是 `#configuration-options`——**`#configuration` 这个锚点在文档里并不存在**。点进去不会报错，只会停在页首，用户以为「文档没讲这块」。

> [!note] 同类现象的项目内注脚（用户 2026-09-18 裁决：保留一句）
> 这类「文档示例调用了不存在的子命令」的现象在写本册的项目里也发生过：脚本 `.claude/scripts/todo-state.sh` 实际只接受 `start|complete|skip|block` 四个子命令（脚本内的 usage 与 `case` 分支都只列这四个），而工作流文档的示例里写了它不支持的 `confirm` 与 `mode` 子命令。**与 Hermes / HA 无关，仅作为「这不是某个项目特有的毛病，而是文档与实现分头演进的通病」的注脚。**

### 8.7 落点对照表

把这一章的 12 条收敛成一张表。用法：遇到「文档说 X」时先在表里搜一眼，命中了就直接看「实际是 Y」和「我该怎么用」。

| # | 文档说 X | 实际是 Y | 来源 | 我该怎么用 |
|---|---|---|---|---|
| 1 | MCP 工具前缀 `mcp_<server>_<tool>` | `mcp__<server>__<tool>`（双下划线） | HMS-11 / HMS-10 / 发布站 vs SRC-04 | 按双下划线写配置与排查 |
| 2 | 同上（同一仓库的另一页写对了） | `reference/mcp-config-reference.md` 就是 `mcp__<server>__<tool>` | HMS-04 | 同仓库两页冲突时，**以源码为准** |
| 3 | — | 改名不彻底：`agent/anthropic_adapter.py` 与对应测试的 docstring 仍写旧写法 | SRC-05 / SRC-06 | 读 docstring 时留意它可能已过期；**冲突时以函数体为准** |
| 4 | — | 该测试的断言**无法区分两种命名**（只覆盖裸工具名） | SRC-06 | 别把「测试全绿」当成「命名约定正确」的证据 |
| 5 | 配置项 `Control Home Assistant`（三段历史快照逐字未变） | 任何分支、任何历史版本都**没有对应键**；44 条提交里从无 control / read-only 类选项 | HAS-01 vs SRC-11 / SRC-12 / SRC-13 | **不判定真伪**，两侧证据并列；未解决问题 G-1 |
| 6 | — | dev 分支真正的开关叫 `require_admin`，UI 文案 `Require an administrator account`，**名称与语义都不是它** | SRC-12 | 别把「管端点访问权」误读成「管设备控制权」 |
| 7 | `/api/mcp` 不要求 admin（2026.9） | 2026.10 改为「配置项打开时要求 admin」 | SRC-11 vs SRC-12 | **必须带版本号**；G-2 未定（是否进正式版） |
| 8 | — | `require_admin` **同版本内默认值不一致**：新装 `True`，1.1→1.2 迁移 `False` | SRC-12 | 不能假设「别人家 HA 和你家一个行为」；先问版本再问是否迁移 |
| 9 | 出站消息「delivered as persistent notifications」（无条件陈述） | 代码有**两条分支**，由执行位置决定；脱 gateway 走 `notify.notify` | HMS-08 vs SRC-08 / SRC-02 | 见第 6 章 6.2；要固定落点就让 gateway 常驻 |
| 10 | cron 页 `"homeassistant"` 行 **Example 列空** | 目标名在代码里合法，但**文档层止于一行表项** | HMS-09 + SRC-08 | 见第 6 章 6.4；写法标「按源码事实拼接」 |
| 11 | `plugin.yaml` 提了 `notify.notify` | 未定义「out-of-process」的判定条件，条件只在源码 docstring | SRC-03 vs SRC-08 | 读 description 时别当成完整规则 |
| 12 | SKILL.md frontmatter：`HMS-12` 与 `HMS-05` **两套互不覆盖的字段表** | 仓库内未找到 schema 文件；`related_skills` 疑似悬空 | HMS-12 vs HMS-05 | 以 HMS-12 为主表，标注 HMS-05 的差异（尤其 `category`）；G-3 / G-4 未定论 |

补充一条不算入 12 条的观察：`config_flow.py` 里的 `MORE_INFO_URL` 指向 `#configuration`，而文档实际锚点是 `#configuration-options`（见 8.6）。它属于同一类失配，但影响只在「点链接没跳到正确位置」，所以放在方法一节里当练习素材。

### 本章小结

- 这 12 条**不是「文档经常不准」的泛论**，每一条都能指回具体文件、分支、行号或快照；没有可举证来源的说法一条都没写进来。
- 失真分三类：**写错**（前缀旧写法）、**没写全**（出站分支、cron 示例）、**两侧对不上且无法定论**（`Control Home Assistant`）。三类要用不同的姿态处理——第一类以源码为准，第二类补全并标注，第三类并列证据、如实留白。
- **`/api/mcp` 的鉴权描述必须带版本号**（2026.9 vs 2026.10），否则必错；同版本内还有「新装 / 迁移」两种默认值，这是有意的兼容策略，源码注释自己写明了原因。
- **docstring 也是文档、也会过期**：`agent/anthropic_adapter.py` 与对应测试的 docstring 就是漂移的现场；判断命名约定要看常量（`MCP_TOOL_NAME_PREFIX = "mcp__"`），不看叙述。
- **自查四步**：仓库 → 分支 → docstring → 提交史。其中「提交史」是判断「曾经有、后来删了」还是「根本不存在」的唯一手段。

### 下一章预告

到这里，**「哪里会骗你」**这部分就收尾了。第 9 章换一个角度问同一个问题：就算文档和代码都对上了，这套东西**跑起来要花多少钱、会出什么样的错**？工具 schema 是常驻开销还是按需加载、成本是否随暴露实体数变化、以及为什么所有关于误报率的数字都**没有分母**。

---

### 本章来源

| ID | 来源 | 类型 | 本章引用的锚点 |
|---|---|---|---|
| HMS-04 | [`website/docs/reference/mcp-config-reference.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md) | 官方文档 | `mcp__<server>__<tool>` 正确写法与双下划线设计说明 |
| HMS-05 | [`website/docs/user-guide/features/skills.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md) | 官方文档 | `## SKILL.md Format` 示例块（含 `category: devops`）、L0 定义 `skills_list() → [{name, description, category}, ...]` |
| HMS-08 | [Hermes 文档：Home Assistant 集成](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/homeassistant) | 官方文档 | `### Agent Responses` 的无条件陈述 |
| HMS-09 | [`website/docs/user-guide/features/cron.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md) | 官方文档 | `## Delivery options` 表中 `"homeassistant"` 行（Example 列空） |
| HMS-10 | [`website/docs/guides/use-mcp-with-hermes.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-mcp-with-hermes.md) | 官方文档 | `mcp_chrome_devtools_win_list_pages`（旧写法实例） |
| HMS-11 | [`website/docs/user-guide/features/mcp.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md) + 发布站同名页 | 官方文档 | `## How Hermes registers MCP tools`（`mcp_<server_name>_<tool_name>` + 三行对照表） |
| HMS-12 | [`website/docs/developer-guide/creating-skills.md`](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md) | 官方文档 | frontmatter 逐字清单（`author` / `license` / `related_skills` / `blueprint` / `required_*`）；路径更正：在 `developer-guide/` 下 |
| HAS-01 | [HA 官方：MCP Server 集成](https://www.home-assistant.io/integrations/mcp_server/) | 官方文档 | `## Configuration options` 里的 `Control Home Assistant:` 块 |
| SRC-02 | [`plugins/platforms/homeassistant/adapter.py`](https://github.com/NousResearch/hermes-agent/blob/main/plugins/platforms/homeassistant/adapter.py) | 一手源码 | 出站两条发送路径与 `register()`（第 6 章 6.2 已展开） |
| SRC-03 | `plugins/platforms/homeassistant/plugin.yaml` | 一手源码 | description 提到 `notify.notify` 但未给判定条件 |
| SRC-04 | [`tools/mcp_tool_schema.py`](https://github.com/NousResearch/hermes-agent/blob/main/tools/mcp_tool_schema.py) | 一手源码 | `MCP_TOOL_NAME_PREFIX = "mcp__"`、`mcp_prefixed_tool_name()` |
| SRC-05 | [`agent/anthropic_adapter.py`](https://github.com/NousResearch/hermes-agent/blob/main/agent/anthropic_adapter.py) | 一手源码 | `_MCP_TOOL_PREFIX = "mcp__"`、`_normalize_to_mcp_wire()` docstring（含旧写法残留） |
| SRC-06 | [`tests/agent/test_anthropic_mcp_prefix_strip.py`](https://github.com/NousResearch/hermes-agent/blob/main/tests/agent/test_anthropic_mcp_prefix_strip.py) | 一手源码 | 模块 docstring（含旧写法残留）、断言只覆盖裸工具名 |
| SRC-08 | [`cron/scheduler_delivery.py`](https://github.com/NousResearch/hermes-agent/blob/main/cron/scheduler_delivery.py) | 一手源码 | 分支条件 docstring、`_KNOWN_DELIVERY_PLATFORMS` |
| SRC-11 | HA core `components/mcp_server/` @ `master` / `rc`（=2026.9） | 一手源码 | `const.py` 无 `CONF_REQUIRE_ADMIN`；`http.py` docstring「does not require admin access」；`config_flow.py` 的 `MORE_INFO_URL` 锚点 |
| SRC-12 | HA core `components/mcp_server/` @ `dev`（=2026.10） | 一手源码 | `CONF_REQUIRE_ADMIN = "require_admin"`、`strings.json` 的 `Require an administrator account`、`_validate_admin`、`async_migrate_entry` 迁移默认 `False` 与源码注释 |
| SRC-13 | HA core `mcp_server` 目录提交史（44 条，至 2026-09-13） | 一手源码史 | `#180713`、`#180629`；无任何 control / read-only 类选项；首版只有 `CONF_LLM_HASS_API` |

---

## 第 9 章：成本与可靠性——工具 schema 常驻开销、误报机理、没有分母的误报率

第 7 章回答的是「会不会出事」，本章回答的是「要花多少钱、能不能信」。这两个问题的材料质量很不一样：**机理**有明确来源（源码、issue、官方文档），**量级**却几乎全靠社区自报，而且这些自报值在引用时极易被写成「实测」。本章要做的第一件事，就是把这些数字的举证性质老老实实标回来。

本章的落点产物是一份 **token 预算与告警阈值的配置建议**（9.6 节）。在给出建议之前，9.1–9.5 需要先说明：钱花在哪、什么不是成本的决定因素、本地路线为什么不免费、以及为什么没人能给你一个误报率。

### 9.1 常驻开销：工具 schema 每一次请求都要付

**一句话定位**：接一个 MCP server 之后，它全部工具的**名字 + 描述 + 参数 JSON Schema** 会被塞进每一次请求的上下文，和这次对话用不用得上这些工具无关。

**9.1.1 这个开销的物理形态**

工具定义不是「用到才加载」的。一个工具的 schema 大致长这样（示意，字段名对齐 MCP 工具定义）：

```json
// 单个 MCP 工具的定义形态（示意；真实内容由 server 的 tools/list 返回）
{
  "name": "ha_config_set_automation",
  "description": "Create or update a Home Assistant automation ... (通常数十到数百字符)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "alias":      { "type": "string", "description": "..." },
      "trigger":    { "type": "array",  "description": "..." },
      "condition":  { "type": "array",  "description": "..." },
      "action":     { "type": "array",  "description": "..." },
      "mode":       { "type": "string", "enum": ["single","restart","queued","parallel"] }
    },
    "required": ["alias", "action"]
  }
}
```

这段 JSON 就是常驻成本的最小单位。工具越多、描述越详细、参数枚举越长，每次请求的固定支出越高。

Hermes 侧有一个可以直接看这个成本的入口（`SRC-07`，一手源码 `hermes_cli/mcp_config.py`）：

```python
# hermes_cli/mcp_config.py
            if details is not None:
                # Per-tool registry-schema sizes (the SAME converted schema the agent registers) so
                # the desktop can estimate per-call token cost. Best-effort, absent on failure.
                try:
                    import json as _json
                    from tools.mcp_tool_schema import _convert_mcp_schema

                    details["schema_chars"] = {
                        t.name: len(_json.dumps(_convert_mcp_schema(name, t), separators=(",", ":"), default=str))
                        for t in server._tools
                    }
```

注意两点。第一，它算的是「**agent 实际注册的那份转换后 schema**」（注释原文：the SAME converted schema the agent registers），不是 server 原始返回的字节数——这是有意义的，因为注册时名字会被 sanitize、schema 会被转换。第二，这个 `details` 是可选出参，`hermes mcp test <server>` 本身**只打印工具名与描述**，不打印这个字符数；填这个字段的是调用方（桌面端）。所以你在命令行里看不到它，只能自己算。

**自己量一遍的做法**（本册给的可执行替代）：对目标 server 调一次 `tools/list`，把返回的每个工具的 `name` + `description` + `inputSchema` 拼成一个 JSON，取字符数，再除以 4 得到粗略 token 数。

```bash
# 粗略估算某个 MCP server 的工具常驻开销（需要该 server 的 endpoint 与凭证）
# 思路：tools/list → 逐工具序列化 → 汇总字符数 → 除以 4
curl -s -X POST "$MCP_URL" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python -c "
import json,sys
d=json.load(sys.stdin)
tools=d.get('result',{}).get('tools',[])
total=sum(len(json.dumps(t,separators=(',',':'),ensure_ascii=False)) for t in tools)
print(f'工具数={len(tools)}  字符数={total}  约={total//4} tokens')
"
```

**这个「除以 4」不是官方口径**：`1 token is equal to approx 4 characters` 是 HA 论坛一位用户的转述经验值（`COM-22` 帖内 post 12，用户 rossk，原句前缀为 `From what I read`——**连他自己也是转述**）。定稿后已回源逐字核验并留下全文快照，**仍然不是官方口径**。把它当量级估算可以，当换算标准不行。

**9.1.2 社区报的量级：引用时必须降格**

社区里流传最广的一组数字来自 `COM-16`（simon42 社区德语帖，主题「ha-mcp 把上下文塞满」，2026-07-06）。**这组数字的举证性质必须降格后再写**，理由如下。

该帖的数字出处集中在 post 3，而 post 3 的段落开头就是 `Claude sagt dazu:`（德语「Claude 对此说」）——也就是说，这些数字是**模型对自己上下文占用的自然语言自述**，不是用 tokenizer 或计数工具跑出来的对照数据。楼主自己在 post 1 的原话只有：

> Die MCP Tools verbrauchen schon über 60k Tokens.（这些 MCP 工具已经消耗超过 60k tokens。）[^c9-1]

**「超过 60k」是楼主说的；带一位小数的精确值只存在于模型自述里。**

因此正文只能这样写：

> 社区用户报告，77 个工具的 schema 合计占用**超过 60k tokens**（其中约 60.3k 这一精确值系帖内 **Claude 的自述**，**不是 tokenizer 计数**），最贵的单工具区间报为 1.8k–3.4k tokens；**无第三方复现**。

**禁止**写成「实测 60.3k」。同样禁止把这个数字当成你自己的预算基线——它是一个量级信号，不是一条测量值。

同帖另有两条相邻引语（post 2 的「110k Tokens」、以及那张 `Bildschirmfoto 2026-07-06 um 09.34.51` 截图）。定稿后已回源核验：post 2（用户 Mercator）原句是 `Die Messages schnappen sich aktuell 110k Tokens.`，与 post 3 一样是在**转述 Claude 的回答**（post 3 的段落开头同样是 `Claude sagt dazu:`），截图也确实在 post 1。两者都不是 tokenizer 计数，因此**核验的结论是「不引用」，而不是「引用」**。

> [!tip] 大白话
> 工具 schema 像**每次开会前都发一遍的全套说明书**：哪怕今天只讨论一件事，你也得把 77 本手册抱进会议室。开会内容再简单，搬运成本不变。所以「把用不上的工具摘掉」不是省钱技巧，而是这项开销**唯一**有效的削减方式——这也正是第 7 章清单第 5 条（`tools.include` 白名单）在成本上的意义。

### 9.2 实体数不是解释变量

**一句话定位**：很多人以为「暴露的实体越少，成本越低」。这个直觉不能由现有材料支持。

**9.2.1 流传中的三个数字，以及它们为什么不能构成对照**

`COM-22`（HA 官方论坛帖 736566，2024-06-06 起）里出现了三个常被并列引用的量级[^c9-2]：

| 数字 | 出处（帖内） | 计量口径 |
|---|---|---|
| 约 230 个实体 → 36 次请求 / `339.000` context tokens / 1800 generated tokens（gpt-4o） | skycryer（post 1，楼主） | **context tokens** |
| 16 次请求 / `200 000` generated tokens | Kolossboss（post 2） | **generated tokens** |
| 242 个实体 | Ollijung（post 11） | 实体数 |
| 340 → 100 个实体后「Still Using 5000 Tokens for a simple request」 | Kolossboss（post 14） | 未注明口径 |

**为什么不能写成对照实验**：这三个数字分属**三个不同用户、不同会话、不同模型**，帖内**没有任何一次**「同一用户把实体数从 X 调到 Y、其余变量固定」的实验。而且**计量口径本身就混用**：post 1 给的是 context tokens，post 2 说的是 generated tokens——两者不是同一个指标，不能并到一张表里比较。

所以正文只能写「**社区多个用户报告的量级差异**」，**不得写成对照结论**，更不能写成「把实体从 340 降到 100 之后 token 用量下降 X%」。

两个读法上的注意：

- **`339.000` 是欧陆千分位写法，等于 339,000**，不是「339 个 token」。同帖还有 `200 000`、`130,000` 两种写法混用，引用时要统一并注明原写法。
- **帖子是 2024-06 的内容**。HA 的 Assist / LLM 管线此后有变更，引用时必须带这个时间戳，否则读者会以为它反映当前版本。
- 该帖的取回路径值得记一笔：HTML 直连被 Cloudflare 拦截，数字来自对 `/t/736566.json` 的抽取。**取回时未落盘可比对字节，当时判定置信度为「中」**；定稿后已重取并落盘全文快照（20 帖），上表四个数字与该帖所有引语均已逐字复核，**置信度升为「高」**。举证定性的降格（不是对照实验）**不因置信度升级而改变**。

**9.2.2 那么成本真正由什么决定**

从 9.1 可以看出，常驻开销与**工具数量 × 每个工具的 schema 大小**强相关。实体数影响的是另一条路径：如果某个工具（或某个上下文注入机制）会把暴露实体列表整体塞进上下文，那么实体数才有意义——而这条路是否成立，取决于你选的实现，不是一个通用结论。

一个可以对照看的一手项目：`COM-11`（`Moballo-LLC/ha-mcp-assist`）README 明确说它的做法是「**dynamic discovery instead of full entity dumps**」，并说明全量推送的后果是「gets expensive, slow, and unreliable as your home grows」。这句话本身也印证了「全量注入才是问题所在」——**是否全量注入是设计选项，不是实体数的必然结果**。（该项目是**一手项目 README，子代理采集，主流程未逐条回源**。）

> [!tip] 大白话
> 「实体多所以贵」这个想法，把**仓库大**和**送货贵**搞混了。真正贵的是「每次送货都把仓库清单抄一遍」。抄不抄，看的是你的实现怎么写的；不抄的实现在那里，抄的实现在那里——你得看它是哪一种，而不是数自己有多少件货。

### 9.3 本地推理的门槛

**一句话定位**：把模型换成本地跑，省的是 API 账单，不是成本；门槛转移到了显存与上下文窗口上。

`COM-19`（HA 官方论坛帖 927713）是一位用户的硬件自述（**社区自报，未复核**）：

> That takes a modern GPU with 16GB VRam at a MINIMUM
> At 16GB you can run an 8-16 K context window
> 8k is very small if you have any number of controlled entities

同帖还提到 eGPU 投入「approx $1200 usd for the setup」。把这些与 9.1 的常驻开销放在一起，张力就出来了：**工具 schema 是常驻支出**，如果它本身就占掉几千 token，而你的上下文窗口只有 8K，那么留给「对话历史 + 实体状态 + 模型输出」的空间会被压得很窄。

另一条本地路线的长期复盘（`COM-17`，HA 官方论坛帖 944860，**社区自报，未复核**）给出了延迟与实体数的自述：RTX 3090 24GB / RX 7900XTX 24GB 报「1 - 2 seconds」，RTX 5060Ti 16GB 报「1.5 - 3 seconds」，RTX 3050 8GB 报「3 seconds」；实体数上，作者自述「Right now I have 32.」，有回帖称「exposing just 53 entities makes it behave very unreliable」。作者本人的结论是「I definitely would not recommend this for the average Home Assistant user」。

**一个必须纠正的对照口径**：`COM-05`（mylo）把 Ollama 计为 `$0`，并因此**自动禁用预算告警**（README 原文：「Budget warnings are automatically disabled since cost is $0.」）。这是可复核的**设计取舍**，但它不是 TCO 口径——它把硬件、电费、延迟和可靠性全部排除在成本之外了。引用时要写明这是该项目的取舍，不是「本地免费」的证明。

### 9.4 把限制做成配置

**一句话定位**：可靠的 agent 不是靠「记得省」，而是把预算、权限和回滚全部变成配置里的显式键。

这一节可以引一手设计（`COM-05`，`Oasis-Enterprise/mylo`，**一手项目 README，可引**）。它把三件在本册前面分别讨论过的事情都做成了配置项：

**一、会话与月度预算键。**

```yaml
# Oasis-Enterprise/mylo 配置项（字段名与默认值逐字来自该项目 README）
session_budget_usd: 0.50    # 每次对话的成本上限
monthly_budget_usd: 15.00   # 每月成本上限
```

**二、三层权限**（README 的 `Safety model` 表，逐字）：

| Tier | Actions | Approval required | 例 |
|---|---|---|---|
| Tier 1 — Read | 查询实体、设备、自动化、日志；读配置文件 | No | `query_entities`、`memory_note` |
| Tier 2 — Modify | 写配置文件、改自动化、重命名实体、改 dashboard | Yes（先 dry-run） | `modify_automation`、`rename_entities` |
| Tier 3 — Action | 调用 HA 服务（灯、锁、窗帘、脚本、场景）、reload | Yes（显式确认） | `call_service`、`reload_config` |

**三、可回滚的写路径**（README 原文）：

> Tier-2 file writes use atomic write → reload → verify → rollback-on-failure.

另一处把完整链路写成「dry-run preview → user approval → atomic write → HA reload → verification」，并说明 reload 失败会自动回滚并告知原因。

这三个键的**共同点**是：把「人要记得做的事」变成「系统默认执行的事」。预算键让超支变成一次可见的拒绝，分层让写操作不能悄悄发生，回滚让写坏了还能回去。这比在提示词里写「请谨慎操作」有效一个量级——因为提示词是建议，配置是约束。

> [!tip] 大白话
> 这就像**给信用卡设额度、大额消费设二次确认、账单可退款**三件事一起做。只跟家人说「省着点花」没用；把额度设上、把确认打开、把退款通道留着，才是真的能兜住。

### 9.5 误报机理与「没有分母的误报率」

**机理部分见第 7 章 7.5 节，本节不重复展开。** 那里列出了四个已知形态（只读询问触发写动作、brightness 单位不一致、模型不支持 tools 却输出 JSON、标签覆写导致 registry 损坏），以及各自的后果方向与可回滚性。本节只处理第 7 章没有回答的那个问题：**这些事多久发生一次。**

答案是：**不知道，而且现有的任何数字都不足以算出一个比率。**

理由很直接：所有误报记录都是**单次事件叙述**——一条 issue、一条论坛回帖、一段用户自述。没有任何来源同时给出「发生了多少次」和「总共执行了多少次」，也就是**没有分母**。材料里把这一条记为 `G-9`（误报率无分母），性质是「如实标注为缺口」。

因此本章**不给任何百分比**。凡是你在别处看到「HA + LLM 的误报率大约是 X%」这类说法，先问它分母是什么——按本册的检索结果，分母不存在。

同样的缺口还有一条更重要的（`G-10`）：**没有任何来源同时给出「月度账单 + 暴露实体数 + 模型名」三者齐全的、跨度超过 6 个月的长期记录。** 现有材料里，有的有 token 数没有月账单，有的有每月预算没有实体数，有的有实体数没有模型名。这意味着「长期成本是多少」这个问题**在现有材料下无法定论**——本章 9.6 给出的预算建议是**可操作的设计**，不是**实测出的合理值**，两者不能混。

最后要交代的是检索覆盖面的缺口（`G-12`）：**Reddit 未被覆盖**。多轮检索均未返回 reddit.com 的结果。本册的成本数字集中在若干个论坛帖上，样本面很窄，读者应把它当作「有人报过这个量级」，而不是「行业普遍水平」。

### 9.6 落点建议：token 预算与告警阈值

把 9.1–9.5 收成一份可以直接抄进配置的建议。注意这些是**起手的保守值**，不是实测最优值——理由见 9.5 的 `G-10`。

```yaml
# ~/.hermes/config.yaml —— 成本与告警相关的起手配置
# 字段名与语义来自 HMS-04（mcp_servers）与 COM-05（mylo 的预算键命名思路）；
# 数值是本册给的起手建议，不是实测结论，按自己的量级调整
mcp_servers:
  home-assistant:
    url: "http://192.168.1.10:8123/api/mcp/assist"
    headers:
      Authorization: "Bearer ${env:HASS_TOKEN}"
    trust: untrusted
    tools:
      include:                 # 先只留真正会用的；这是唯一能砍常驻开销的键
        - "get_state"
        - "list_entities"

# 预算类键（命名参考 COM-05 的 session_budget_usd / monthly_budget_usd）
budget:
  session_budget_usd: 0.50     # 单次对话上限：超过就拒绝，别设成“提醒”
  monthly_budget_usd: 15.00    # 月度上限
  warn_at_pct: 80              # 到 80% 时提示（COM-05 的做法）
  local_provider_is_free: false # 本地推理不要按 $0 计，见 9.3
```

配套的四条阈值纪律：

| # | 纪律 | 依据 |
|---|---|---|
| 1 | **用白名单砍工具数，而不是靠提示词「少调用」** | 工具 schema 是常驻开销，不调用也要付（9.1） |
| 2 | **不要按实体数估预算** | 实体数不是成本的单调解释变量（9.2，`COM-22` 只能并列不能对照） |
| 3 | **本地路线也设预算键**，只是把单位从美元换成「上下文占用 + 延迟」 | 本地不是免费（9.3，`COM-19` 的门槛；`COM-05` 把 Ollama 计 $0 是它的取舍） |
| 4 | **告警阈值按事件类型分开设**，「不该动的动了」与「该动的没动」不能用同一个阈值 | 第 7.5 节四个形态的后果方向相反 |

**关于第 4 条再补一句**：由于没有分母（9.5），阈值只能按「单次事件是否严重」来设，不能按「发生率」来设。也就是说，你能做的是「这种事一出现就一定要有人看到」，而做不到「发生率超过 5% 就报警」。承认这一点，比编一个比率更有用。

> [!warning] 本章的引用红线
> 1. `COM-16` 的 token 数字**不是 tokenizer 计数**，是帖内 Claude 的自述；楼主原话只有「über 60k Tokens」。**禁止**写成「实测 60.3k」。
> 2. `COM-22` 的 230 / 340→100 / 242 **不是对照实验**：三个不同用户、不同会话、不同模型，且计量口径混用（context tokens vs generated tokens）。只能写「社区多个用户报告的量级差异」。
> 3. 误报率**无任何来源给出分母**（`G-9`），正文不得出现百分比。
> 4. 无「月账单 + 实体数 + 模型名」三者齐全的 >6 个月记录（`G-10`），长期成本结论**不可得**。

### 本章小结

- 工具 schema 是**常驻开销**：接上即付，与本次是否调用无关。能削它的只有 `tools.include` 一类的白名单。
- 社区报告 77 个工具约 60k+ tokens 量级，但**该精确值系模型自述而非 tokenizer 计数，无第三方复现**；最贵单工具区间报 1.8k–3.4k tokens。
- **实体数不是成本的单调解释变量**：流传的三个数字分属三个不同用户 / 会话 / 模型，不是对照实验，且口径混用。真正决定成本的是「是否全量注入」这类设计选择。
- **本地推理不是免费路线**：`COM-19` 的门槛是 16GB VRAM 起、仅 8–16K context；把 Ollama 计为 `$0` 是 `COM-05` 的设计取舍，不是 TCO。
- **把限制做成配置**（`COM-05` 一手设计）：会话 / 月度预算键、三层权限、atomic write → reload → verify → rollback。
- **误报率没有分母**（`G-9`），全部是单次事件叙述，本章不给任何百分比；长期成本因缺「三者齐全的 >6 个月记录」（`G-10`）而**不可定论**。
- Reddit 三轮未覆盖（`G-12`），社区数字集中在少数论坛帖，样本面窄。

### 下一章预告

九章正文到此结束。最后是附录：一份**实机核对清单**（4 条命令，每条都写明「答案会改变正文哪一句」）、一张**未解决问题分级表**（4 条阻塞项 + 13 条非阻塞缺口），以及一份**延伸阅读索引**——最后这份要如实说明：本轴素材薄弱，只有官方文档索引与项目清单，**没有体系化的进阶路径**。

### 本章来源

| ID | 档位 | 位置 | 核对结果 |
|---|---|---|---|
| `COM-16` | 社区帖（德语，**已回源，举证性质降格**） | `community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707` | 楼主 post 1 原话仅「über 60k Tokens」；`60,3k` 与 `1,8k–3,4k` 出处在 post 3，段落开头为 `Claude sagt dazu:`（**模型自述，非 tokenizer 计数**）。相邻引语「110k Tokens」（post 2）与截图（post 1）**已核验**，同为转述 Claude 的自述，故仍**不引用** |
| `COM-22` | 社区帖（**已回源，部分支持**） | `community.home-assistant.io/t/736566` | 数字逐字命中，但分属 skycryer（post 1，context tokens）/ Kolossboss（post 2、14，generated tokens）/ Ollijung（post 11）；**无单变量对照实验**；`339.000` = 339,000；帖为 2024-06；全文快照已落盘，置信度「**高**」 |
| `COM-19` | 社区帖（**社区自报，未复核**） | HA 官方论坛帖 927713 | 16GB VRAM 起、8–16K context、eGPU 约 $1200 |
| `COM-17` | 社区帖（**社区自报，未复核**） | HA 官方论坛帖 944860 | 延迟分档自述、32 / 53 实体、误报形态 |
| `COM-11` | 一手项目 README（**子代理采集，主流程未逐条回源**） | `Moballo-LLC/ha-mcp-assist` | 「dynamic discovery instead of full entity dumps」「gets expensive, slow, and unreliable as your home grows」 |
| `COM-05` | 一手项目 README（**可引**） | `Oasis-Enterprise/mylo` | 逐字命中：`session_budget_usd` 0.50、`monthly_budget_usd` 15.00、三层权限表、`atomic write → reload → verify → rollback-on-failure`、Ollama 预算告警自动禁用 |
| `SRC-07` | 一手源码 | Hermes `hermes_cli/mcp_config.py` | 逐字命中：`details["schema_chars"]` 逐工具注册 schema 字符数，注释说明用途为桌面端估算 per-call token 成本；`hermes mcp test` 只打印工具名与描述 |
| `G-9` / `G-10` / `G-12` | 缺口记录 | `02_deep_research.md` §7.2 | 误报率无分母 / 无三者齐全的 >6 个月记录 / Reddit 未覆盖 |

[^c9-1]: `COM-16`，https://community.simon42.com/t/ha-mcp-macht-den-kontext-voll/88707 ，post 1（Mathias42）、post 2（Mercator，`110k Tokens` 的出处）与 post 3（转述 Claude 回答）。全文快照已落盘。
[^c9-2]: `COM-22`，https://community.home-assistant.io/t/736566 ，post 1 / 2 / 11 / 14（另 post 5 给出 `13 API requests / 130,000 tokens / totalling 0.66$`，本册未引用）。全文快照已落盘（20 帖），上表四个数字与 `post 12` 引语均已逐字核验；原帖为 2024-06。

---

## 附录：实机核对清单、未解决问题与延伸阅读

九章正文里出现过若干处「本册只能写到这个程度」的地方：有的是因为手边没有 Hermes CLI，有的是因为官方文档本身不写，有的是因为社区数字只有一次叙述。这个附录把它们集中收口成三份查阅件：**A 是你在自己机器上花五分钟就能跑完的核对清单**，**B 是全部未解决问题的分级表**，**C 是延伸阅读索引**。

C 需要先说一句：本轴素材薄弱，它是一份「去哪看官方文档、有哪些可对照的项目」的索引，**不是一条体系化的进阶路径**。读完它不会让你「进阶」，只会让你知道下一站有哪些门。

### 附录 A 实机核对清单（4 条命令）

这四条命令都是为了让正文里若干处**带条件的措辞**能变成确定值。每一条都写明「为什么问它」和「答案会改变正文哪一句」——后者是关键：没有这一栏，就没有动力去跑。

**A-1｜`hermes --version`**

```bash
hermes --version
```

- **为什么问它**：MCP 工具的注册名前缀在文档与代码之间存在漂移。文档（与发布站）写的是旧写法 `mcp_<server>_<tool>`，而源码里的常量是 `MCP_TOOL_NAME_PREFIX = "mcp__"`（双下划线，`SRC-04`）。旧写法是某次改名（改名前的写法）之前的产物，所以你的 Hermes 版本落在哪个时期，决定正文里的前缀是否需要一个版本注解。
- **答案会改变正文哪一句**：第 3 章讲工具注册名时的那句「注册名 = `mcp__<server>__<tool>`」。若你的版本已确认在双下划线时期，该句可以写成无条件断言；若在旧时期，需要补一句「你的版本可能仍是单下划线写法，以会话内实测为准」。
- **对应记录**：`Q-1`。

**A-2｜会话内跑 `/reload-mcp`，然后让 agent 列出 MCP 工具全名**

```text
（在 Hermes 会话中输入）
/reload-mcp
请把你当前可用的 MCP 工具名完整列出，保留前缀原样，不要改写。
```

- **为什么问它**：这是对 A-1 的**互证**。`hermes --version` 给的是版本号，而这里给的是你机器上**实际注册出来的名字**。两者一致，才能把正文的前缀结论从「源码为准」升级为「实机确认」。
- **答案会改变正文哪一句**：同样是第 3 章的前缀句。此外，如果列出的名字与 `tools.include` 里写的名字对不上，还会反过来修订第 7 章 7.4.1 那句「`include` / `exclude` 用**原始**工具名，不是 sanitize 后的注册名」的实际操作说明。
- **对应记录**：`Q-2`。

**A-3｜`hermes mcp test <server>`**

```bash
hermes mcp test home-assistant
```

- **为什么问它**：源码里 `_probe_single_server` 打印的是 `t.name`，也就是 **server 返回的原生工具名**（`SRC-07`），不是注册进 agent 的那个 sanitize 后的名字。所以 `hermes mcp test` **不能**用来验证注册名前缀。这一点是**源码级判断，未经实机跑过**——需要跑一次确认它真的只打印原生名。
- **答案会改变正文哪一句**：第 3 章里排错建议的措辞。目前正文写的是「`hermes mcp test` 打印原生工具名，不能用来验证注册名前缀」；若实测发现它还额外打印了注册名，这句要改。
- **对应记录**：`Q-3`。

**A-4｜HA「关于」页查版本**

```text
HA 前端 → 设置 → 关于（About），读取版本号
```

- **为什么问它**：HA 的 `/api/mcp` 端点对非 Assist API ID 的管理员要求，在 **2026.9 与 2026.10 两个版本之间行为相反**：2026.9 的源码里这个判断是写死的（`if api_id != llm.LLM_API_ASSIST and not request["hass_user"].is_admin`，`SRC-11`），2026.10 的 dev 分支新增了 `require_admin` 配置项并改走 `_validate_admin`（`SRC-12`）。同一段行为在两个版本上结论不同，所以正文**必须带版本号**。
- **答案会改变正文哪一句**：第 5 章讲 `/api/mcp` 鉴权那一段的版本限定语。若你是 2026.9，写「要求管理员」是对的；若是 2026.10，则要改写成「取决于配置项」。
- **对应记录**：`Q-4`。

> [!tip] 大白话
> 这四条命令的作用，好比**买东西前先量一下家里的尺寸**。正文里的结论已经按「最小公倍数」写得很保守（源码为准 + 标版本），但保守措辞读起来总有点绕；跑一遍这四条，绕的地方就能换成确定值。

### 附录 B 未解决问题分级表

**阻塞项（4 条，需你实机执行）**：本册写作环境里没有 `hermes` CLI，因此这四条无法代验。它们**不阻塞开写**——正文已按「源码为准 + 标注版本差异」处理，回填只是把注解换成确定值。

| # | 问题 | 命令 / 位置 | 影响哪一章 | 现状 | 是否阻塞写作 |
|---|---|---|---|---|---|
| Q-1 | 你的 Hermes 处于单下划线还是双下划线时期 | `hermes --version` | 第 3 章 | 未执行 | 否（正文已加版本注解） |
| Q-2 | 本机实际注册名是什么 | 会话内 `/reload-mcp` 后让 agent 列出工具全名 | 第 3 章 | 未执行 | 否（与 Q-1 互证用） |
| Q-3 | `hermes mcp test` 是否真的只打印原生名 | `hermes mcp test <server>` | 第 3 章（排错措辞） | 未执行 | 否（源码级判断已足够落笔） |
| Q-4 | 你的 HA 是 2026.9 还是 2026.10 | HA「关于」页 | 第 5 章 | 未执行 | 否（正文已带版本号） |

**非阻塞缺口（13 条）**：这些是「材料里确实没有」，正文已按缺口如实标注，不阻塞写作。

| # | 缺口 | 影响哪一章 | 现状 | 是否阻塞写作 |
|---|---|---|---|---|
| G-1 | `Control Home Assistant` 的文档来源 | 第 8 章 | 代码侧查无对应键；需 HA release notes / PR 讨论才能定论 | 否（两侧证据并列写） |
| G-2 | `require_admin` 是否进 2026.10 正式版 | 第 5、8 章 | `dev` 有、`rc` 无，是否 revert 未知 | 否（带版本号写） |
| G-3 | SKILL.md frontmatter 的机器可读 schema | 第 3、8 章 | 仓库内未找到 schema / loader，只能靠两份官方文档互证 | 否（以主表 + 差异标注写） |
| G-4 | `related_skills` 的消费方 | 第 8 章 | 仅在一份官方文档中出现，作用未知 | 否（如实标注） |
| G-5 | `blueprint.schedule` 的 `"every 2h"` / ISO 写法 | 第 6 章 | 无语法定论 | 否（不给出断言） |
| G-6 | `_deliver_standalone` 如何取 `standalone_sender_fn` | 第 6 章 | 未逐行确认（文件 94267 字节） | 否（只写已验证的分支条件） |
| G-7 | `Prefer handling commands locally` 在哪个集成页有文档 | 第 2 章 | 四个 LLM 集成页全文无此串 | 否（写成官方文档内部冲突） |
| G-8 | HA 文档页均无「最后更新」时间戳 | 全册 | 站点不暴露；只能记抓取时间 | 否（记录为抓取时间） |
| G-9 | 误报率无分母 | 第 7、9 章 | 全部为单次事件叙述，无法算比率 | 否（不给百分比） |
| G-10 | 无「月账单 + 实体数 + 模型名」三者齐全的 >6 个月记录 | 第 9 章 | 最长记录缺项 | 否（长期成本结论写「不可得」） |
| G-11 | 未找到 HA 侧 prompt injection / 恶意实体名触发的实测帖 | 第 7 章 | 仅媒体定性警告（二手，未采信） | 否（**不写**） |
| G-12 | Reddit 未被覆盖 | 第 9 章、附录 C | 三轮精读均未返回 reddit.com 结果 | 否（在样本面说明中标注） |
| G-13 | 进阶路径 / 学习资源轴最薄 | 附录 C | 只有官方文档索引与项目清单，缺体系化路径 | 否（降格为索引，如实说明） |

需要特别点出两条的性质差异：**Q-1..Q-4 是「跑一下就有答案」**，属于可闭合项；**G-1..G-13 里有多条是「官方确实没写」的否定结论**（G-1、G-7、G-11），这类缺口不会因为再检索一次就消失，它们本身就是结论的一部分，正文里应当保留而不是隐去。

### 附录 C 延伸阅读索引

**先说清楚这份索引的性质**：本轴（进阶路径 / 学习资源）是全册素材里**最薄的一轴**（`G-13`）。它只有两类内容——官方文档索引与可对照的一手项目清单——**没有体系化的学习路径**，而且 Reddit 三轮检索均未覆盖（`G-12`）。所以，**读完这份索引不等于完成进阶**；它只负责告诉你官方文档在哪、有哪些实现可以对照着读。

**C.1 官方文档索引**

HA 侧：

| ID | 主题 | 位置 |
|---|---|---|
| `HAS-01` | MCP Server 集成（含 `## Configuration options`、6 个第三方 client 示例、`## Exposing an API over MCP` 锚点） | `home-assistant.io/integrations/mcp_server/` |
| `HAS-03` | REST API | `developers.home-assistant.io/docs/api/rest/` |
| `HAS-04` | WebSocket API | `developers.home-assistant.io/docs/api/websocket/` |
| `HAS-05` | Authentication API（LLT 有效期、refresh token 吊销语义） | `developers.home-assistant.io/docs/auth_api/` |
| `HAS-06` | Permissions（组、四档实体粒度、first-match 顺序、owner 豁免） | `developers.home-assistant.io/docs/auth_permissions/` |
| `HAS-16` | LLM 开发者接口（`API`/`APIInstance`/`Tool`/`LLMContext`，Assist API 的能力边界） | `developers.home-assistant.io/docs/core/llm/` |

Hermes 侧：

| ID | 主题 | 位置 |
|---|---|---|
| `HMS-04` | MCP 配置参考（`trust`、`readOnlyHint`、`include` / `exclude`、原始工具名） | 仓库 `website/docs/reference/mcp-config-reference.md` |
| `HMS-07` | CLI 命令参考（`hermes mcp` 全部子命令、`--version`） | 仓库 `website/docs/reference/cli-commands.md` |
| `HMS-10` | 用 MCP 搭配 Hermes（注意：该页的前缀写法**已过期**，见第 8 章） | 仓库 `website/docs/guides/use-mcp-with-hermes.md` |

官方 release notes 里值得单看的两条：`HAS-26`（2025.7 的 `assist_satellite.ask_question`，即「HA 主动发起对话」）与 `HAS-27`（2025.8 的自动化编辑器 Suggest 按钮，默认不可见、需在设置里开启）。

**C.2 可对照的一手项目清单**

以下项目的价值在于**对照**，不在于「照着装」。每个都标注了它的定位差异，其中两个方向恰好相反。

| ID | 项目 | 定位差异 | 备注 |
|---|---|---|---|
| `COM-01` | `homeassistant-ai/ha-mcp` | 独立 MCP server，面向**配置、搭建、调试**智能家居，而非仅控制；实体作用域自述为 `Everything in Home Assistant` | 工具数在同一份 README 内三处口径不一致（87 / 95+ / ~84），引用时不要给单值 |
| `COM-02` | `voska/hass-mcp` | 走 HA **WebSocket** API 的独立 server | 与走 HTTP 的项目形成传输方式对照 |
| `COM-04` | `cnc-lasercraft/haclaude` | **只读工具白名单型**：夜间巡检 + 严格只读 | 德文 README |
| `COM-07` | `tevonsb/homeassistant-mcp` | 较早的独立实现 | 最后 push 2026-01，**已滞后** |
| `COM-08` | `ganhammar/hass-mcp-server` | **HACS 组件型 + OAuth 2.0**：以 HA 自定义组件形式安装 | 与独立进程型项目形成安装方式对照 |
| `COM-09` | `allenporter/mcp-server-home-assistant` | — | **已归档，勿选** |
| `COM-11` | `Moballo-LLC/ha-mcp-assist` | **跟随暴露模型型**：自述「follows Home Assistant's conversation exposure model」，用动态发现替代全量注入 | 与 `COM-01` 的 `Everything` 作用域恰成对照 |
| `COM-23` | `homeassistant-ai/ha-mcp` 的 Setup Wizard 文档 | 提供 **Hermes Agent 专属 YAML 模板**、`/reload-mcp` 提示、`mcp__home_assistant__<tool>` 命名 | 本册第 4 章的接入依据 |

「已归档，勿选」的那一条（`COM-09`）不是凑数：它的存在本身说明这个生态有过更替，读到旧教程时值得先确认项目是否还在维护。

**C.3 关于「进阶路径」的如实说明**

如果读完索引你在找一条「下一步该学什么」的路线，这里必须直说：**本册没有提供，而且现有素材也不足以支撑一条**。

具体缺口是：

- **素材构成不均衡**：官方文档 28 条 / Hermes 文档 12 条 / 一手源码 14 条 / 社区 23 条，其中官方文档与源码很扎实，**学习资源与进阶路径几乎为空**。
- **Reddit 未覆盖**（`G-12`）：多轮检索均未返回 reddit.com 的结果，社区数字因此集中在少数几个论坛帖上，样本面很窄。
- **进阶路径轴最薄**（`G-13`）：本轴只有官方文档索引与项目清单，两者都**不是**路径。

一条可靠的进阶路线应当包含「按顺序做什么、做完会得到什么、卡住了看哪一份文档」——这些在当前素材里都没有可靠依据。把它们编出来会制造一种「读完就进阶了」的错觉，那比留白更糟：留白至少诚实，编出来的路径会让人按错误的顺序投入时间。本册的选择是留白并标注。

如果要接着往下走，可行的起点只有两个：一是按 C.1 的官方文档就地深挖（尤其 `HAS-16` 的 LLM 开发者接口，它解释了 Assist API 的能力上界从哪来）；二是按 C.2 挑一个与你现在路线不同的项目读它的 README，理解同一个能力在另一种设计下的取舍。

### 附录小结

- **附录 A 的 4 条命令**都是「跑一下就有答案」的：前缀版本、注册名互证、`mcp test` 的措辞确定性、HA 版本决定的跨版本写法。
- **附录 B 的 4 条阻塞项**需要实机执行，但**不阻塞写作**——正文已按「源码为准 + 标版本」写成保守措辞，回填只是把注解换成确定值。
- **附录 B 的 13 条非阻塞缺口**中有多条是「官方确实没写」的**否定结论**，它们本身就是结论，应当保留而非隐去。
- **附录 C 是索引，不是路径**：只有官方文档与项目清单，Reddit 未覆盖（`G-12`）、进阶路径轴最薄（`G-13`）。读完不等于进阶。

