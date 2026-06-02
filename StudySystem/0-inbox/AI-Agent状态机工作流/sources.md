# Sources for AI Agent 状态机工作流

| # | Title | URL | Author | Date | Type | Notes |
|---|-------|-----|--------|------|------|-------|
| 01 | LangGraph Overview | https://docs.langchain.com/oss/python/langgraph/overview | LangChain | 2025 | technical_docs | 核心概览：state/nodes/edges/graph 基础 |
| 02 | LangGraph Persistence, Checkpointing, and State Management | https://docs.langchain.com/oss/python/langgraph/persistence | LangChain | 2025 | technical_docs | 持久化、checkpoint、Store、三种 durability 模式 |
| 03 | Human-in-the-Loop and Interrupts in LangGraph | https://docs.langchain.com/oss/python/langgraph/interrupts | LangChain | 2025 | technical_docs | interrupt、approval pattern、resume |
| 04 | LangGraph Concepts (State, Nodes, Edges) | https://docs.langchain.com/oss/python/langgraph/overview | LangChain | 2025 | technical_docs | 与 doc-01 重复，提取视角不同 |
| 05 | LangGraph Functional API | https://docs.langchain.com/oss/python/langgraph/functional-api | LangChain | 2025 | technical_docs | @entrypoint、@task、short-term memory |
| 06 | LangGraph Observability with LangSmith | https://docs.langchain.com/oss/python/langgraph/observability | LangChain | 2025 | technical_docs | tracing 环境变量、metadata、anonymizer |
| 07 | LangGraph Graph API Overview | https://docs.langchain.com/oss/python/langgraph/graph-api | LangChain | 2025 | technical_docs | Command 原子、reducers、conditional edges |
| 08 | Building Effective AI Agents | https://www.anthropic.com/research/building-effective-agents | Anthropic | 2024 | technical_docs | workflows vs agents 基础原则 |
| 09 | CrewAI Multi-Agent Framework Overview | https://docs.crewai.com/concepts/crews | CrewAI | 2025 | technical_docs | Crew、Sequential/Hierarchical、checkpointing |
| 10 | Microsoft AutoGen Agent Framework | https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/framework/agent-and-agent-runtime.html | Microsoft | 2025 | technical_docs | AutoGen Core + AgentChat 概览 |
| 11 | LLM Agent Design Patterns (Lilian Weng) | https://lilianweng.github.io/posts/2023-06-23-agent/ | Lilian Weng | 2023-06 | blog_posts | ReAct、Planning、Memory、Tool use |
| 12 | Building LangGraph: Design Principles | https://www.langchain.com/blog/building-langgraph | LangChain | 2024 | blog_posts | 架构设计、BSP/Pregel 算法 |
| 13 | LangGraph Workflow & Agent Patterns | https://docs.langchain.com/oss/python/langgraph/workflows-agents | LangChain | 2025 | technical_docs | prompt chaining、parallelization、orchestrator |
| 14 | Lyft's Self-Serve AI Agent Platform | https://www.langchain.com/blog/lyft-built-a-self-serve-ai-agent-platform-for-customer-support-with-langgraph-and-langsmith | Akshay Sharma | 2026-05 | blog_posts | 生产级 case study、DynamoDBSaver |
| 15 | LangSmith Observability Overview | https://www.langchain.com/langsmith | LangChain | 2025 | technical_docs | SmithDB、tracing、监控告警 |
| 16 | LangGraph v0.2 Features (Checkpointer Ecosystem) | https://www.langchain.com/blog/langgraph-v0-2 | LangChain | 2024 | blog_posts | checkpointer 库拆分、Postgres 优化 |
| 17 | LangGraph Subgraphs: Parent/Child Graph Composition | https://docs.langchain.com/oss/python/langgraph/use-subgraphs | LangChain | 2025 | technical_docs | 多 agent 组合、persistence 模式 |
| 18 | CrewAI Memory System | https://docs.crewai.com/concepts/memory | CrewAI | 2025 | technical_docs | scope 层级、scoring、consolidation |
| 19 | LangGraph Time Travel | https://docs.langchain.com/oss/python/langgraph/use-time-travel | LangChain | 2025 | technical_docs | Replay、Fork、subgraph time travel |
| 20 | State Machine Patterns in LangGraph | https://docs.langchain.com/oss/python/langgraph/graph-api | LangChain | 2025 | technical_docs | guardrails、recursion limit、RemainingSteps |
| 21 | Testing LangGraph Agents | https://docs.langchain.com/oss/python/langgraph/test | LangChain | 2025 | technical_docs | pytest、partial execution |
| 22 | LangGraph Multi-Agent Workflows (Blog) | https://www.langchain.com/blog/langgraph | LangChain | 2024 | blog_posts | 早期多 agent 介绍，内容较薄 |
| 23 | LangGraph GitHub README Overview | https://github.com/langchain-ai/langgraph | LangChain | 2025 | technical_docs | 项目主页、生态定位 |
