# LangGraph Overview

**URL**: https://docs.langchain.com/oss/python/langgraph/overview

## What It Is

LangGraph is "a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents." It is "focused entirely on agent **orchestration**" and "provides low-level supporting infrastructure for *any* long-running, stateful workflow or agent." Unlike higher-level frameworks, "LangGraph does not abstract prompts or architecture."

## Key Concepts

The framework uses a graph-based model with these core building blocks:

- **State**: Data that flows through the graph (shown as `MessagesState` in examples)
- **Nodes**: Processing units that transform state (added via `add_node()`)
- **Edges**: Connections that define flow between nodes (`add_edge()`)
- **Graph**: The complete workflow structure (`StateGraph`)

The code example shows how nodes connect from `START` to "mock_llm" to `END`—demonstrating state machine-like control flow.

## Core Capabilities

**Persistence**: "Build agents that persist through failures and can run for extended periods, resuming from where they left off."

**Human-in-the-loop**: "Incorporate human oversight by inspecting and modifying agent state at any point."

**Memory**: "Comprehensive memory" enables both short-term working memory and "long-term memory across sessions."

**Observability**: Integrates with LangSmith for "visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics."

## Ecosystem Position

The documentation positions LangGraph as the orchestration runtime layer—below LangChain's agent abstractions but above raw model/tool integrations. It draws inspiration from "Pregel and Apache Beam" and uses a "NetworkX"-inspired public interface.
