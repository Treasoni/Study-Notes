"""轻量智能家居 Agent —— FastAPI 入口。

架构：
  FastAPI (/health, /chat)
    └─ DeepSeek Function Calling（deepseek-v4-flash，OpenAI SDK）
         └─ 工具白名单：control_device / get_device_state
              └─ Home Assistant REST（tools.py）

单轮命令控制（N=1）：模型最多发起 1 次工具调用，执行后把结果回填，
再请求一次得到最终答复。不做多步规划，不给模型第二次调工具的机会。

2026-08 关键 API 事实：
  - 模型：deepseek-v4-flash（deepseek-chat / deepseek-reasoner 已于 2026-07-24 停用）
  - base_url：https://api.deepseek.com（OpenAI 兼容）
  - 思考模式：V4 默认开启；本服务通过 extra_body={"thinking": {"type": "disabled"}}
    显式关闭，避免工具轮次中 reasoning_content 必须回传导致的 400。
  - tool_choice：V4 在思考模式下拒绝 "required" 与指定函数（HTTP 400，官方 issue #1376）；
    因此统一用 "auto" + 系统提示约束，由应用层 N=1 循环保证单次工具调用。
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Callable

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field

from entity_map import EntityResolver
from tools import HomeAssistantClient

load_dotenv()  # 读取同目录 .env

logger = logging.getLogger("ha-agent")

# ---------------- 配置 ----------------
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash").strip()
DEEPSEEK_THINKING = os.getenv("DEEPSEEK_THINKING", "disabled").strip().lower()

HA_BASE_URL = os.getenv("HA_BASE_URL", "http://127.0.0.1:8123").strip()
HA_TOKEN = os.getenv("HA_TOKEN", "").strip()
HA_TIMEOUT = float(os.getenv("HA_TIMEOUT", "10"))

# 单轮命令控制：最多执行 1 次工具调用
MAX_TOOL_ROUNDS = 1

# 运行时校验用白名单
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

BASE_DIR = Path(__file__).resolve().parent

# ---------------- 全局依赖 ----------------
ha = HomeAssistantClient(base_url=HA_BASE_URL, token=HA_TOKEN, timeout=HA_TIMEOUT)
resolver = EntityResolver(BASE_DIR / "entity_map.yaml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await ha.close()  # 退出时释放 httpx 连接池


app = FastAPI(title="Lightweight HA Agent", version="0.1.0", lifespan=lifespan)

# ---------------- 工具实现（真正执行的逻辑） ----------------
async def control_device(
    entity_id: str, service: str, params: dict[str, Any] | None = None
) -> str:
    """控制设备：解析实体 -> 校验 domain/service -> 调用 HA 服务。"""
    eid = resolver.resolve(entity_id)
    if eid is None:
        known = "、".join(resolver.list_entities()) or "（无）"
        return f"错误：未找到实体「{entity_id}」。可用实体：{known}。"
    domain = eid.split(".", 1)[0]

    if domain not in ALLOWED_DOMAINS:
        return f"错误：不允许控制 domain「{domain}」。允许：{sorted(ALLOWED_DOMAINS)}"
    allowed = ALLOWED_SERVICES.get(domain, set())
    if service not in allowed:
        return f"错误：domain「{domain}」不支持服务「{service}」。允许：{sorted(allowed)}"

    data = dict(params or {})
    data.setdefault("entity_id", eid)  # HA 服务调用体需要 entity_id
    try:
        result = await ha.call_service(domain, service, data)
    except Exception as exc:  # 网络错误 / HA 错误
        return f"错误：调用 Home Assistant 失败：{exc}"

    return f"已执行 {eid} {service}，Home Assistant 返回：{json.dumps(result, ensure_ascii=False)[:800]}"


async def get_device_state(entity_id: str) -> str:
    """查询实体当前状态。"""
    eid = resolver.resolve(entity_id)
    if eid is None:
        known = "、".join(resolver.list_entities()) or "（无）"
        return f"错误：未找到实体「{entity_id}」。可用实体：{known}。"
    try:
        state = await ha.get_state(eid)
    except Exception as exc:
        return f"错误：查询 Home Assistant 失败：{exc}"
    return json.dumps(
        {
            "entity_id": state.get("entity_id"),
            "state": state.get("state"),
            "attributes": state.get("attributes", {}),
        },
        ensure_ascii=False,
    )


# ---------------- 工具元数据（给模型看）与白名单 ----------------
TOOL_DEFS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "control_device",
            "description": "控制一个设备：开/关、调温度、调亮度、开合窗帘等。"
            "entity_id 可以是 device_id 或用户口吻的名称（如“客厅灯”），系统会自动解析。",
            "parameters": {
                "type": "object",
                "properties": {
                    "entity_id": {
                        "type": "string",
                        "description": "设备 entity_id 或名称，如 light.living_room / 客厅灯",
                    },
                    "service": {
                        "type": "string",
                        "description": "要执行的服务，如 turn_on / turn_off / set_temperature",
                    },
                    "params": {
                        "type": "object",
                        "description": "可选附加参数，如 brightness、temperature、hvac_mode、position",
                        "additionalProperties": True,
                    },
                },
                "required": ["entity_id", "service"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_device_state",
            "description": "查询一个设备的当前状态（开/关、温度、亮度等）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "entity_id": {
                        "type": "string",
                        "description": "设备 entity_id 或名称，如 sensor.hall_temperature / 客厅温度",
                    },
                },
                "required": ["entity_id"],
            },
        },
    },
]

# 函数名白名单：只有这里出现的工具名才会被执行。
# 模型返回的任何其他函数名都会在校验阶段被拒绝。
TOOL_HANDLERS: dict[str, Callable[..., Any]] = {
    "control_device": control_device,
    "get_device_state": get_device_state,
}

SYSTEM_PROMPT = """你是家庭智能助手，通过工具控制 Home Assistant 中的设备。

规则：
1. 用户给出可执行指令（开灯、关灯、调温度、查询状态等）时，先调用一次工具。
2. 每次回复最多调用一次工具；拿到工具结果后直接给出最终答复，不要再调用第二次。
3. 如果用户只是闲聊或询问你能做什么，不要调用工具，直接回答。
4. 提到设备时优先使用用户的说法（如“客厅灯”），工具会自动解析成 entity_id。
5. 只执行明确指令；指令含糊时先向用户确认，不要猜测。
6. 最终答复要简短、自然、用中文。
可用实体：{entities}
"""


def _validate_tool_call(name: str, args: Any) -> dict[str, Any]:
    """运行时参数校验。不合法直接抛 ValueError，由调用方转成面向模型的结果。"""
    if name not in TOOL_HANDLERS:
        raise ValueError(f"工具名不在白名单：{name}")
    if not isinstance(args, dict):
        raise ValueError("工具参数必须是 JSON 对象")

    entity_id = args.get("entity_id")
    if not isinstance(entity_id, str) or not entity_id.strip():
        raise ValueError("参数 entity_id 必须是非空字符串")

    # 若用户直接给的是 entity_id 形态的字符串，先做格式校验
    if resolver.is_valid_entity_id(entity_id) and not resolver.has_entity_id(entity_id):
        raise ValueError(f"entity_id 不在映射表中：{entity_id}")

    if name == "control_device":
        service = args.get("service")
        if not isinstance(service, str) or not service.strip():
            raise ValueError("参数 service 必须是非空字符串")
        if "params" in args and args["params"] is not None and not isinstance(args["params"], dict):
            raise ValueError("参数 params 必须是对象")
    return args


# ---------------- Agent 主循环 ----------------
def _build_messages(user_text: str) -> list[dict[str, Any]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(entities="、".join(resolver.list_entities()))},
        {"role": "user", "content": user_text},
    ]


async def run_agent(user_text: str) -> tuple[str, int]:
    """执行单轮命令控制，返回 (最终答复, 实际工具调用次数)。"""
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=503, detail="缺少 DEEPSEEK_API_KEY")
    if not HA_TOKEN:
        raise HTTPException(status_code=503, detail="缺少 HA_TOKEN")

    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    messages = _build_messages(user_text)
    extra_body: dict[str, Any] = {"thinking": {"type": DEEPSEEK_THINKING}}

    async def first_call() -> Any:
        return await asyncio.to_thread(
            client.chat.completions.create,
            model=DEEPSEEK_MODEL,
            messages=messages,
            tools=TOOL_DEFS,
            tool_choice="auto",  # 见文件头注释：V4 下强制 tool_choice 会 400
            temperature=0.2,     # 思考关闭时允许采样参数
            extra_body=extra_body,
        )

    try:
        first = await first_call()
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=f"DeepSeek 首次调用失败：{exc}")

    msg = first.choices[0].message
    tool_calls = getattr(msg, "tool_calls", None) or []

    if not tool_calls:
        return (msg.content or "（无回复）"), 0

    # ---- N=1：只执行第一个工具调用 ----
    tool_call = tool_calls[0]
    messages.append(
        {
            "role": "assistant",
            "content": msg.content or None,
            "tool_calls": [tc.model_dump() for tc in tool_calls],  # 原样回传，满足 API 格式
        }
    )

    try:
        args = _validate_tool_call(tool_call.function.name, json.loads(tool_call.function.arguments or "{}"))
        handler = TOOL_HANDLERS[tool_call.function.name]
        result = await handler(**args)
    except json.JSONDecodeError as exc:
        result = f"错误：工具参数不是合法 JSON：{exc}"
    except ValueError as exc:
        result = f"错误：参数校验未通过：{exc}"
    except Exception as exc:  # 兜底：任何意外异常都转成模型可读的结果
        logger.exception("tool execution failed")
        result = f"错误：工具执行失败：{exc}"

    messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})

    async def final_call() -> Any:
        return await asyncio.to_thread(
            client.chat.completions.create,
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=0.2,
            extra_body=extra_body,
        )

    try:
        second = await final_call()
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=f"DeepSeek 最终答复调用失败：{exc}")

    reply = second.choices[0].message.content or ""
    return (reply, 1)


# ---------------- FastAPI 路由 ----------------
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="用户输入")
    session_id: str | None = Field(default=None, description="预留：本版本无状态，忽略")


class ChatResponse(BaseModel):
    reply: str
    tool_calls: int


class HealthResponse(BaseModel):
    status: str
    model: str
    thinking: str
    ha_connected: bool


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        model=DEEPSEEK_MODEL,
        thinking=DEEPSEEK_THINKING,
        ha_connected=await ha.ping(),
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    reply, calls = await run_agent(req.message)
    return ChatResponse(reply=reply, tool_calls=calls)
