# Building LangGraph: Design Principles

**URL**: https://www.langchain.com/blog/building-langgraph

## Why LangGraph Was Built

LangGraph emerged from feedback that LangChain was "easy to get started but hard to customize and scale." The team determined that LLMs are fundamentally different from traditional software—slower, flakier, and more open-ended—which required new infrastructure approaches.

Existing frameworks were inadequate: DAG frameworks couldn't handle the cyclical nature of agent loops, and durable execution engines like Temporal lacked streaming support and introduced noticeable latency between steps.

## Core Design Principles

The framework operates on two guiding principles:

1. **Minimize assumptions about AI's future**—the fewer baked-in assumptions, the more relevant the framework remains as the field evolves.

2. **"It should feel like code"**—every requirement placed on developers must justify itself by enabling high-value functionality. The biggest competitor to any framework is no framework.

## Technical Architecture

LangGraph separates its runtime (PregelLoop) from developer SDKs like StateGraph, allowing independent evolution. It implements a channel-and-node model based on the BSP/Pregel algorithm, which provides:

- Deterministic concurrency with full loop support
- Automatic parallelization when node dependencies allow
- No data races through isolated state copies during parallel execution
- Serialized checkpoints for fault tolerance and human-in-the-loop interruption

## Key Production Features

Six features address LLM agent challenges:

- **Parallelization** reduces actual latency
- **Streaming** improves perceived latency
- **Checkpointing** reduces retry costs
- **Task queues** minimize failure sources
- **Human-in-the-loop** enables user collaboration
- **Tracing** provides observability

The framework provides these as optional building blocks rather than enforcing them, staying low-level while remaining flexible as requirements change.
