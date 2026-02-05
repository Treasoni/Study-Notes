
# Prompt（提示词）

## 1. User Prompt（用户提示词）

在 AI 刚兴起的时候（如 OpenAI 发布 GPT），AI 就像一个聊天框。我们通过聊天框给 AI 模型发送消息，AI 模型会自动生成一个回复。这里我们给 AI 模型发送的信息就是 **用户提示词（User Prompt）**。

## 2. System Prompt（系统提示词）

但是单纯的聊天模式下，AI 只能给出通用的回答。如果我们想要 AI 具有特定人设，可以在消息中指定，比如：「你是我的女朋友，我的肚子痛。」

这样 AI 就会从「女朋友」的角度来回复消息，实现不同人设做出不同回答。但每次都要在用户消息中写人设很不方便，于是出现了 **系统提示词（System Prompt）**。

System Prompt 用于预先设置人设、角色、行为准则等信息。之后每次发送 User Prompt 时，会自动把 System Prompt 一起发给 AI 模型。

### Prompt 的角色分工

| 类型 | 作用 | 位置 | 示例 |
|------|------|------|------|
| **System Prompt** | 定义角色、人设、行为准则 | 最先发送 | 「你是一个专业的程序员助手」 |
| **User Prompt** | 用户的实际输入 | 中间发送 | 「帮我写一个快速排序」 |
| **Assistant Message** | AI 的回复 | 最后返回 | AI 生成的回答内容 |


# Agent（智能体）

## 1. 为什么需要 Agent？

按照上面的模型，AI 可以根据不同的人设做出不同的回答。但我们不想只把 AI 当成一个聊天工具，而是希望它能够实现具体功能、执行操作。

因此就出现了 **Agent（智能体）**。

## 2. Agent 的工作原理

Agent 的核心是 **Tools（工具）**——一些可以被调用的函数。这些函数把自己的功能名称、描述、参数格式等信息注册到 Agent 中。

Agent 的工作流程：

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Agent 收集所有 Tools 的信息（名称、功能、参数格式）           │
│  2. Agent 将这些信息构造成 System Prompt，告诉 AI 有哪些工具可用  │
│  3. Agent 发送 System Prompt + User Prompt 给 AI 模型             │
│  4. AI 决定是否需要调用工具，返回调用请求                          │
│  5. Agent 接收请求，执行对应的 Tool 函数                           │
│  6. Tool 执行完将结果返回给 Agent                                 │
│  7. Agent 将结果发送给 AI，AI 基于结果继续生成内容                 │
│  8. 如果还需要调用工具，重复 4-7 步，否则返回最终答案给用户        │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Agent 的关键组件

| 组件 | 作用 |
|------|------|
| **Agent Framework** | Agent 框架，协调 AI 和工具之间的交互 |
| **Tools** | 可被调用的函数，提供具体功能（如天气查询、文件操作等） |
| **Tool Registry** | 工具注册表，存储所有工具的元信息 |
| **AI Model** | 大语言模型，负责理解意图和决策 |

# Function Calling（函数调用）

## 1. 为什么需要 Function Calling？

在早期的 Agent 实现中，Agent 通过自然语言（大白话）告诉 AI 模型应该如何使用工具、返回什么格式。但 AI 是一个概率模型，输出可能不稳定，有时返回正确的调用格式，有时则不会。为了保证可靠性，可能需要多次尝试或重试。

为了解决这个问题，出现了 **Function Calling（函数调用）**——一种标准化的工具调用机制。

## 2. Function Calling 的改进

| 方式 | 描述格式 | 稳定性 |
|------|----------|--------|
| **自然语言描述** | 用文字描述工具和返回格式 | 不稳定，AI 可能不遵循格式 |
| **Function Calling** | 用 JSON Schema 规范描述工具 | 稳定，强制格式约束 |

Function Calling 的核心改进：

1. **工具描述标准化**：每个 Tool 用 JSON Schema 对象进行描述
2. **调用格式标准化**：规定了 AI 使用工具时应返回的固定格式
3. **返回值类型约束**：明确定义参数类型（string、number、array 等）

### Function Calling 的工具描述示例

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "获取指定城市的天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称"
        }
      },
      "required": ["city"]
    }
  }
}
```

## 3. 目前的现状

Function Calling 原本是一个通用概念，但不同大模型厂商的实现方式不同（OpenAI、Anthropic、Google 等的 API 格式都不完全一致）。

因此目前实践中：
- **标准 Function Calling**：用于主流 AI 厂商的专用格式
- **System Prompt 方式**：用于兼容性或特殊场景
- 两种方式根据具体需求选择使用


# MCP（Model Context Protocol，模型上下文协议）

## 1. 为什么需要 MCP？

上面讨论的都是 Agent 与 AI 大模型之间的交互方式。但是 Agent 如何与 Tools 通信呢？

每个开发者可能用不同的方式实现 Tools：
- 不同的接口格式
- 不同的通信方式
- 不同的参数定义

这导致不同 Agent 之间很难共享工具。

为了解决这个问题，出现了 **MCP（Model Context Protocol，模型上下文协议）**。

## 2. MCP 的角色

| 原有概念 | MCP 概念 |
|----------|----------|
| Agent Tools | **MCP Server** |
| Agent | **MCP Client** |

## 3. MCP 协议规范

MCP 规定了 MCP Server 和 MCP Client 之间的通信标准：

### 3.1 通信方式

MCP 支持多种传输方式：
- **stdio**：标准输入输出，适用于本地进程
- **SSE（Server-Sent Events）**：服务器推送事件，适用于 Web 场景

### 3.2 MCP Server 必须提供的接口

| 接口 | 作用 |
|------|------|
| `tools/list` | 获取 Server 中所有可用的 Tool 列表 |
| `tools/call` | 调用指定的 Tool 并返回结果 |
| `prompts/list` | 获取可用的 Prompt 模板（可选） |
| `resources/list` | 获取可用资源列表（可选） |

### 3.3 MCP 的优势

1. **标准化**：统一的工具描述和调用格式
2. **可复用**：一个 MCP Server 可以被多个 Agent 使用
3. **跨语言**：不限制编程语言，任何语言都能实现 MCP 协议
4. **分布式**：工具可以部署在不同的服务器上


# 总结：完整的工作流程

## 整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│    用户                                                                  │
│     │                                                                   │
│     │ User Prompt                                                       │
│     ↓                                                                   │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │         Agent (作为 MCP Client)                                  │    │
│  │  ┌───────────────────────────────────────────────────────────┐  │    │
│  │  │  1. 连接 MCP Servers，获取所有 Tools 信息                   │  │    │
│  │  │  2. 将 Tool 信息转化为 System Prompt 或 Function Calling   │  │    │
│  │  │  3. 发送 System Prompt + User Prompt 给 AI 模型            │  │    │
│  │  └───────────────────────────────────────────────────────────┘  │    │
│  │         │                                                    │    │
│  │         │ AI 响应（文本或工具调用请求）                        │    │
│  │         ↓                                                    │    │
│  │  ┌───────────────────────────────────────────────────────────┐  │    │
│  │  │  如果需要调用工具：                                       │  │    │
│  │  │  4. 解析 AI 返回的工具调用请求                             │  │    │
│  │  │  5. 通过 MCP 协议调用对应的 MCP Server                    │  │    │
│  │  │  6. 将工具执行结果返回给 AI 继续处理                       │  │    │
│  │  │  7. 重复直到 AI 生成最终答案                              │  │    │
│  │  └───────────────────────────────────────────────────────────┘  │    │
│  │         │                                                    │    │
│  │         │ 最终答案                                            │    │
│  │         ↓                                                    │    │
│  └────────────────────────────────────────────────────────────────┘    │
│     │                                                                   │
│     │ 返回结果                                                           │
│     ↓                                                                   │
│    用户                                                                  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │              MCP Servers (提供各种工具)                         │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │  │
│  │  │   Weather MCP    │  │  Filesystem MCP  │  │  GitHub MCP  │ │  │
│  │  │   Server         │  │  Server          │  │  Server      │ │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────┘ │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 核心概念关系

| 概念 | 作用层 | 核心作用 |
|------|--------|----------|
| **Prompt** | 用户↔AI | 定义对话内容和人设 |
| **Agent** | AI↔Tool | 协调 AI 调用工具 |
| **Function Calling** | Agent↔AI | 标准化工具调用描述 |
| **MCP** | Agent↔Tool | 标准化工具服务通信 |


# 如何写 Agent 代码（以 Python 为例）

## 1. 准备工作

### 1.1 定义工具函数

先写好你的工具函数，最好单独用一个文件存放，便于管理和维护。

```python
# tools.py
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 这里调用天气 API
    return f"{city} 的天气是晴天，25℃"

def search_files(query: str) -> list[str]:
    """搜索文件"""
    # 这里实现文件搜索逻辑
    return [f"找到文件: {query}"]
```

### 1.2 配置环境变量

获取大语言模型的 API Key，不要直接写在代码中。使用 `.env` 文件存储敏感信息：

```bash
# .env
OPENAI_API_KEY=sk-your-api-key-here
```

然后在代码中加载：

```python
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件到环境变量
```

## 2. 配置 Agent（使用 Pydantic AI）

```python
from pydantic_ai import Agent, RunContext
from tools import get_weather, search_files

# 创建 Agent 对象
agent = Agent(
    model='openai:gpt-4o',              # 指定模型
    system_prompt='你是一个有用的助手',    # 系统提示词（可选）
    deps_type=dict,                      # 依赖类型（可选）
)

# 注册工具函数
@agent.tool
def weather_tool(ctx: RunContext[dict], city: str) -> str:
    """获取城市天气信息"""
    return get_weather(city)

@agent.tool
def file_search_tool(ctx: RunContext[dict], query: str) -> list[str]:
    """搜索本地文件"""
    return search_files(query)
```

## 3. 运行 Agent

```python
# 主程序
def main():
    # 获取用户输入
    user_input = input("请输入你的问题: ")

    # 运行 Agent（同步方式）
    result = agent.run_sync(user_input)

    # 输出结果
    print(result.data)

    # 查看工具调用历史
    if result.tool_calls:
        print("调用的工具:", result.tool_calls)
```

## 4. 保持对话上下文

如果希望 AI 记住之前的对话内容，需要保存消息历史：

```python
# 保存所有消息历史
message_history = []

def chat_loop():
    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # 将之前的消息历史作为参数传入
        result = agent.run_sync(
            user_input,
            message_history=message_history  # 传递历史消息
        )

        print(f"\nAI: {result.data}")

        # 更新消息历史
        message_history.extend(result.all_messages())
```

## 完整示例

```python
# main.py
import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

# 加载环境变量
load_dotenv()

# 创建 Agent
agent = Agent(
    'openai:gpt-4o',
    system_prompt='你是一个有帮助的 AI 助手'
)

# 注册工具
@agent.tool
def calculator(ctx: RunContext[dict], expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"

# 运行
if __name__ == '__main__':
    while True:
        user_input = input("\n你: ")
        if user_input == 'exit':
            break

        result = agent.run_sync(user_input)
        print(f"\nAI: {result.data}")
```)

