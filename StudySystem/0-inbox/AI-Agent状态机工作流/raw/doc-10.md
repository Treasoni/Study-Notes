# Microsoft AutoGen Agent Framework

**URL**: https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/framework/agent-and-agent-runtime.html

## Agents

Agents in AutoGen are entities defined by the base interface `Agent`, with unique identifiers (`AgentId`) and metadata (`AgentMetadata`). Most implementations subclass from `RoutedAgent`, which enables routing messages to handler methods via the `@message_handler()` decorator.

## Agent Runtime

The runtime provides infrastructure for agent communication, lifecycle management, security boundaries, and monitoring. For local development, `SingleThreadedAgentRuntime` can be embedded in Python applications.

## Agent Registration

Agent types are registered with factory functions using the `register()` method, associating a unique string type with a creation function. This enables automatic instance creation when needed.

## State Management and Group Chat

State management is not explicitly covered in the Core API. Group chat patterns appear in a separate section on "Multi-Agent Design Patterns."

## Key Classes Mentioned

- `Agent` and `RoutedAgent` (base classes)
- `SingleThreadedAgentRuntime` (local runtime)
- `AgentId`, `AgentType`, `AgentMetadata` (identity constructs)
- `MessageContext` (for message handling context)

The documentation notes that AgentChat agents differ from Core agents—they're created by application code rather than managed by the runtime.

## AutoGen AgentChat Quickstart

**URL**: https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/quickstart.html

AutoGen enables building multi-agent applications through AgentChat. The framework provides preset agents with tool-calling capabilities, supporting various models including OpenAI and Azure OpenAI.

### Core Components

- **AssistantAgent** - Configurable agents with reflection and streaming
- **Tool Use** - Custom functions agents can call during conversations
- **Teams** - Multi-agent collaboration workflows
- **Human-in-the-Loop** - Human intervention capabilities

### Advanced Multi-Agent Features

- Selector Group Chat
- Swarm orchestration
- Magentic-One
- GraphFlow workflows
- Memory and RAG integration

### Quick Setup

```python
pip install -U "autogen-agentchat" "autogen-ext[openai,azure]"
```

The framework supports serialization, logging, and distributed tracing for production deployments.
