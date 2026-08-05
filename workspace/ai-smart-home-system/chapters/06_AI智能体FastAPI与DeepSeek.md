---
title: "第六章 AI 智能体：FastAPI + DeepSeek Function Calling"
type: chapter
chapter: 6
tags:
  - Home-Assistant
  - AI智能体
  - DeepSeek
  - FastAPI
created: 2026-08-05
updated: 2026-08-05
status: 已完成
source_project: ai-smart-home-system
---

# 第六章 AI 智能体：FastAPI + DeepSeek Function Calling

> 笔记类型：实战构建指南（practice）｜学习深度：精通
> 素材来源：`02_deep_research.md` §4、§6（时效性修正 #2）、§7（#4、#7）
> 前置关联：第一章四层架构中的「智能体层」；`workspace/ai-smart-home-system/agent/` 可运行代码骨架

> [!summary] 本章回答三个问题
> 1. DeepSeek 在 2026-08 的 API 事实是什么？哪些旧教程写法会直接踩 400？
> 2. 一个「自然语言 → 设备控制」的最小 Agent 循环长什么样？
> 3. 把设备控制权交给 AI，怎么设计才不至于开出一个「口子」？

前面几章把 Home Assistant 跑起来、接入了品牌设备，现在系统已经有「耳朵」了，但还缺「大脑」。本章补上四层架构里的智能体层：一个轻量 Python（FastAPI）进程接收用户的自然语言，交给 DeepSeek Function Calling 解析成结构化工具调用，再通过 HA REST API 执行。你会拿到一份能跑的骨架（`workspace/ai-smart-home-system/agent/`），并理解它为什么绕开了 DeepSeek V4 的几个已知坑。

## 6.1 API 事实核对：2026-08 的 DeepSeek 现状

动笔前先核对 API 事实。DeepSeek 在 2026 年对模型命名、思考模式、`tool_choice` 都做了调整，网上大量旧教程会把你直接带进 400。[深度收集 §4](../02_deep_research.md)

| 事实 | 取值 | 为什么必须记住 |
|------|------|----------------|
| 模型名 | `deepseek-v4-flash` | 旧名 `deepseek-chat` / `deepseek-reasoner` 已于 2026-07-24 停用，传旧名直接报错 |
| 价格 | $0.14 / 1M 输入，$0.28 / 1M 输出 | 缓存命中约便宜 50 倍，高频提示词值得做静态化 |
| base_url | `https://api.deepseek.com` | OpenAI 兼容端点，直接用 openai SDK 即可 |
| tool_choice | 统一 `"auto"` | V4 思考模式下传 `"required"` 或指定函数名返回 HTTP 400 |
| thinking | MVP 显式关闭 | V4 默认开启，工具轮次要回传 `reasoning_content` 否则 400；关闭后更快更便宜且允许 `temperature` |

`tool_choice` 这一条最关键。旧教程里「强制模型必须调某个函数」的写法在 V4 思考模式下直接废掉，官方文档与 issue #1376 都确认了这一点。[DeepSeek API 文档](https://api-docs.deepseek.com) 本项目用三层替代「强制工具调用」：`tool_choice="auto"` + 系统提示「可执行指令先调一次工具」+ 应用层 N=1 循环保证最多执行一次。意图由模型自己判断，行为边界由应用层兜底。

## 6.2 Agent 主循环：main.py 的 N=1 tool-calling

主循环的职责很克制：**模型最多发起 1 次工具调用**（`MAX_TOOL_ROUNDS = 1`），执行后把结果回填，再请求一次拿到最终答复，然后收工。不做多步规划、不给模型第二次调工具的机会。对「单条命令控制」这个场景，这是最稳的做法——多步规划看着聪明，但每多一步就多一次幻觉和越权机会。

先看工具白名单，它定义了 Agent 能力的边界：[深度收集 §4](../02_deep_research.md)

```python
ENTITY_ID_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z0-9_]+$")
ALLOWED_DOMAINS = {"light", "switch", "fan", "cover", "media_player", "climate"}
ALLOWED_SERVICES: dict[str, set[str]] = {
    "light": {"turn_on", "turn_off", "toggle"},
    "switch": {"turn_on", "turn_off", "toggle"},
    "fan": {"turn_on", "turn_off", "toggle", "set_percentage"},
    "cover": {"open_cover", "close_cover", "stop_cover", "set_cover_position"},
    "media_player": {"turn_on", "turn_off", "toggle", "volume_set"},
    "climate": {"turn_on", "turn_off", "set_temperature", "set_hvac_mode"},
}
```

domain 白名单决定「能碰哪些类型的设备」，service 白名单决定「能对这类设备做什么」。另外还有一份给模型看的结构化元数据 `TOOL_DEFS`（两个工具的 JSON Schema），真正执行的是 `TOOL_HANDLERS`。函数名白名单、domain/service 双层白名单，就是 6.5 安全设计的执行骨架。

N=1 循环的核心逻辑（完整文件见 `agent/main.py` 的 `run_agent`）：

```python
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
messages = _build_messages(user_text)

first = await asyncio.to_thread(
    client.chat.completions.create,
    model=DEEPSEEK_MODEL, messages=messages, tools=TOOL_DEFS,
    tool_choice="auto", temperature=0.2,
    extra_body={"thinking": {"type": DEEPSEEK_THINKING}},   # 关闭思考，见 6.1
)
msg = first.choices[0].message
tool_calls = getattr(msg, "tool_calls", None) or []
if not tool_calls:                       # 模型认为无需调工具（闲聊/询问）
    return (msg.content or "（无回复）"), 0

# ---- N=1：只执行第一个工具调用 ----
tool_call = tool_calls[0]
messages.append({"role": "assistant", "content": msg.content or None,
                 "tool_calls": [tc.model_dump() for tc in tool_calls]})

try:
    args = _validate_tool_call(tool_call.function.name,
                               json.loads(tool_call.function.arguments or "{}"))
    result = await TOOL_HANDLERS[tool_call.function.name](**args)   # 白名单内的真实执行
except ValueError as exc:
    result = f"错误：参数校验未通过：{exc}"          # 校验失败转成模型可读的文本

messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
reply = (await asyncio.to_thread(
    client.chat.completions.create,
    model=DEEPSEEK_MODEL, messages=messages, temperature=0.2,
    extra_body={"thinking": {"type": DEEPSEEK_THINKING}},
)).choices[0].message.content or ""
return (reply, 1)
```

几个值得注意的工程点：

- `asyncio.to_thread` 把 OpenAI 的**阻塞**调用包成非阻塞，避免卡死 FastAPI 事件循环。
- assistant 消息里 `tool_calls` 必须**原样回传**（`tc.model_dump()`），格式不对 API 会拒收。
- 工具执行结果以 `role: "tool"` 回填，靠 `tool_call_id` 关联；下一次请求模型基于真实结果生成最终答复。
- 所有异常（参数校验失败、HA 调用失败、网络错误）都转成**面向模型的中文文本**，模型读得懂就能向用户解释，而不是抛给前端一个裸 500。

### 本地验证：curl 两个端点

FastAPI 暴露 `/health` 和 `/chat` 两个端点。先起服务，再 curl：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000

curl http://127.0.0.1:8000/health
# {"status":"ok","model":"deepseek-v4-flash","thinking":"disabled","ha_connected":true}

curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "打开客厅灯"}'
# {"reply":"好的，已为你打开客厅灯。","tool_calls":1}
```

`/health` 里的 `ha_connected` 来自 `HomeAssistantClient.ping()`，一上来就能确认 HA 侧认证是否配好。`tool_calls: 1` 表示这一轮真的执行了一次工具调用，是排查「模型是不是在瞎答」的第一信号。

## 6.3 工具层：tools.py 的 Home Assistant REST 封装

工具层把 HA REST API 封装成 `HomeAssistantClient`（httpx.AsyncClient），只暴露 `get_state` / `call_service` / `ping` 三个方法。[深度收集 §4](../02_deep_research.md) [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest/)

```python
self._headers = {
    "Authorization": f"Bearer {token}",   # 注意：Bearer 后必须有一个空格
    "Content-Type": "application/json",
}

async def call_service(self, domain, service, data=None):
    resp = await client.post(
        f"{self.base_url}/services/{domain}/{service}",
        headers=self._headers, json=data or {},
    )
    return self._handle(resp)             # 成功返回变更后的 state JSON 数组
```

对照官方 REST API 的映射关系：

| Agent 方法 | HTTP 请求 | 作用 |
|------------|-----------|------|
| `get_state(entity_id)` | `GET /api/states/{entity_id}` | 查询单个实体当前状态 |
| `call_service(domain, service, data)` | `POST /api/services/{domain}/{service}` | 调用服务，返回变更后的 state 数组 |
| `ping()` | `GET /api/` | 认证探活，供 `/health` 用 |

两个容易翻车的细节：`Authorization` 是 `Bearer ` 加 token，`Bearer` 后**有空格**，拼错直接 401；调用服务的请求体里必须带 `entity_id`（6.2 里 `control_device` 用 `data.setdefault("entity_id", eid)` 补上）。错误统一抛 `RuntimeError`，message 里带 HA 状态码和响应摘要（最多 500 字符），这样工具结果对模型足够友好——模型能直接读出「401 认证失败」并告诉用户。

## 6.4 实体映射：entity_map.yaml + rapidfuzz 模糊匹配

用户不会说 `light.living_room`，他说「客厅灯」。实体映射层负责把口语别名解析成 HA 实体 ID，避免让模型去猜 entity 命名。[深度收集 §4](../02_deep_research.md)

```yaml
entities:
  - entity_id: light.living_room
    name: 客厅灯
    aliases: [客厅主灯, living room light, living_room]
    domain: light
  - entity_id: climate.bedroom_ac
    name: 卧室空调
    aliases: [空调, bedroom ac]
    domain: climate
```

`EntityResolver.resolve()` 按固定顺序解析（完整逻辑见 `agent/entity_map.py`）：

1. **精确命中 entity_id**：`light.living_room` 直接命中，走 `_by_id` 字典。
2. **精确命中 name / alias**：大小写不敏感，走 `_label_to_id`。
3. **长得像 entity_id 但不在映射表**：直接返回 `None`，不再模糊——避免把乱串文本当实体匹配。
4. **rapidfuzz 模糊匹配**：对 name/alias 标签列表用 `WRatio` 打分，`score_cutoff=80`，低于阈值不认。

第 3 步「先拦截、再模糊」的顺序很关键：它既容忍「客厅的灯」这种口语变体，又不会把「客厅」这种合法前缀误匹配成别的实体。

映射表还反向供给提示词：`run_agent` 里 `SYSTEM_PROMPT.format(entities="、".join(resolver.list_entities()))` 把可用实体清单注入系统提示，并明确要求「提到设备时优先用用户说法，工具会自动解析」。模型负责说人话，解析交给确定性代码——这条分工是全章的核心思想。

## 6.5 安全设计：把「口子」收窄成「接口」

把设备控制权交给 LLM，最怕的不是模型笨，而是模型被**越权诱导**（prompt injection）或**手滑控制错误设备**。项目里的安全设计分层如下：[深度收集 §4](../02_deep_research.md)

- **专用受限 HA 用户 + LLAT**：为 Agent 单独建一个 HA 用户，用它生成 Long-Lived Access Token，不要用管理员主号。注意 LLAT 默认无 scope，**等同全管理员权限**，所以「受限用户」才是真正的隔离手段——让这个用户只能看到、控制这一批设备。`.env` 里的 `HA_TOKEN` 就是它。
- **函数名白名单**：模型返回的工具名只有出现在 `TOOL_HANDLERS` 里的才会被 `_validate_tool_call` 放行，其余一律拒绝。模型最多「提议」，执行权永远在应用层。
- **运行时参数校验**：`_validate_tool_call` 检查 `entity_id` 必须在映射表里、`service` 必须在白名单、`params` 必须是对象；`domain` / `service` 双重白名单在 `control_device` 里再查一遍。
- **控制前查 state（生产必加）**：当前骨架里 `control_device` 直接调 `call_service`。生产版本应在调用前先 `get_state`，若 `state` 为 `unavailable` / `unknown` 则拒绝并提示「设备离线」，避免对离线设备盲发指令。`get_device_state` 已经提供查询能力，把它接到控制路径即可。
- **brightness 量纲 0-255**：`params` 是透传给 HA 的，`light.turn_on` 的 `brightness` 量纲是 **0-255**（不是百分比 0-100）。模型常会输出 50 这种百分数，建议在工具层统一做量纲换算或钳制。
- **密钥不烤进镜像**：`.env` 用 `chmod 600` 保护、`.gitignore` 排除；`Dockerfile` 只 `COPY main.py tools.py entity_map.py entity_map.yaml ./`，密钥靠 `-e` / `--env-file` 注入。`.env.example` 里 `HA_TOKEN` / `DEEPSEEK_API_KEY` 都是占位符。

> [!warning] LLAT 没有 scope 概念
> LLAT 只是一个 token 字符串，默认拥有该用户全部权限。别因为「看起来是个 token」就放松警惕——隔离靠「专用受限 HA 用户」，不靠 token 本身。

容器化与依赖（完整文件见 `agent/` 目录）：

| 文件 | 作用 |
|------|------|
| `requirements.txt` | `fastapi` / `uvicorn[standard]` / `openai` / `httpx` / `pyyaml` / `python-dotenv` / `rapidfuzz` |
| `Dockerfile` | `python:3.12-slim`，`uvicorn main:app --host 0.0.0.0 --port 8000`，`EXPOSE 8000` |
| `.env.example` | `DEEPSEEK_MODEL=deepseek-v4-flash`、`DEEPSEEK_THINKING=disabled`、`HA_BASE_URL=http://127.0.0.1:8123` |

配合第 3 章的 `docker-compose`，Agent 以 sidecar 形式跑在 `network: host` 下，容器内直接 `127.0.0.1:8123` 连 HA，`depends_on: homeassistant: condition: service_healthy` 保证 HA 先就绪。

## 本章小结

- DeepSeek 2026-08 关键事实：模型名是 `deepseek-v4-flash`（旧名 2026-07-24 停用），`tool_choice` 必须用 `"auto"`，MVP 用 `extra_body` 关掉 thinking，否则工具轮次会踩 `reasoning_content` 回传的 400。
- 智能体主循环 = N=1：模型最多提议一次工具调用，应用层校验、执行、回填，再请求一次拿最终答复；不做多步规划。
- 能力边界用白名单收窄：`TOOL_HANDLERS` 函数白名单 + `ALLOWED_DOMAINS` / `ALLOWED_SERVICES` + 运行时参数校验，模型只能「提议」，执行权在代码。
- 口语 → entity 的解析交给确定性的 `entity_map.yaml` + rapidfuzz（WRatio，score_cutoff=80），不交给模型猜。
- 安全靠「专用受限 HA 用户 + LLAT + 白名单 + 控制前查 state」，密钥 `.env` chmod 600、不入镜像；生产必补 unavailable/unknown 拦截与 brightness 量纲换算。

---

下一章进入「场景」：HA 的自动化引擎。你会看到怎么把回家、离家、睡眠这些场景模板化成 packages 与 Blueprint，让整套系统不止会「听指令」，还会「自己判断该做什么」。
