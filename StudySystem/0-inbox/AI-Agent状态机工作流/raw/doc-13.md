# LangGraph Workflow & Agent Patterns

**URL**: https://docs.langchain.com/oss/python/langgraph/workflows-agents

## Workflows vs. Agents

LangGraph distinguishes between **workflows** (predetermined code paths) and **agents** (dynamic, self-directed with tool usage).

## Core Workflow Patterns

1. **Prompt Chaining**: Sequential LLM calls where each processes the previous output—ideal for translation or content verification.

2. **Parallelization**: Multiple LLM calls run simultaneously to increase speed or validate outputs through redundancy.

3. **Routing**: Inputs are classified then directed to specialized processing paths (e.g., pricing vs. refunds queries).

4. **Orchestrator-Worker**: An orchestrator breaks down tasks, delegates subtasks to workers, and synthesizes results. Uses LangGraph's `Send` API for dynamic worker creation.

5. **Evaluator-Optimizer**: A generator creates responses while an evaluator critiques them. Iterates until acceptable output is produced.

## Agents

Agents combine LLMs with tools in feedback loops, making autonomous decisions about tool usage. The `ToolNode` prebuilt component handles parallel execution and error handling.

**Note**: This documentation doesn't include a dedicated "supervisor" pattern—the orchestrator-worker pattern serves similar coordination functions.
