# Testing LangGraph Agents

**URL**: https://docs.langchain.com/oss/python/langgraph/test

## Framework

The guide recommends using **pytest** for unit testing LangGraph agents.

## Key Patterns

### 1. Setup Per Test

Create and compile the graph before each test with a fresh checkpointer:

> "create your graph before each test where you use it, then compile it within tests with a new checkpointer instance."

### 2. Test Individual Nodes

Access nodes via `compiled_graph.nodes` to test them in isolation.

### 3. Partial Execution

Use `update_state()` with `as_node` parameter to simulate resuming from a specific point, then invoke with `interrupt_after` to stop at a target node.

## Test Checkpointer

For simple agents, the in-memory `MemorySaver` checkpointer works well for testing purposes.
