# LangGraph Subgraphs: Parent/Child Graph Composition

**URL**: https://docs.langchain.com/oss/python/langgraph/use-subgraphs

## Core Concept

A subgraph is a graph used as a node within another graph. This compositional pattern enables modular, reusable workflows.

**Key benefits:**
- Multi-agent system architecture
- Node reuse across multiple graphs
- Distributed team development with independent subgraph ownership

## Two Communication Patterns

| Pattern | Use When | Implementation |
|---------|----------|----------------|
| **Call subgraph inside a node** | Different state schemas (no shared keys) | Wrapper function transforms parent ↔ subgraph state |
| **Add subgraph as a node** | Shared state keys | Pass compiled subgraph directly to `add_node` |

### Pattern 1: Different State Schemas

The node function manually transforms parent state to subgraph input and output back to parent state:

```python
def call_subgraph(state: State):
    subgraph_output = subgraph.invoke({"bar": state["foo"]})
    return {"foo": subgraph_output["bar"]}
```

### Pattern 2: Shared State Schemas

Pass the compiled subgraph directly—no transformation needed:

```python
builder.add_node("node_1", subgraph)  # reads/writes parent's channels
```

## Subgraph Persistence Modes

| Mode | `checkpointer=` | Memory | Interrupts |
|------|-----------------|--------|------------|
| Per-invocation (default) | `None` | Fresh each call | Supported |
| Per-thread | `True` | Accumulates | Supported |
| Stateless | `False` | None | Not supported |

**Per-invocation** is recommended for most multi-agent systems where subagents handle independent requests. **Per-thread** suits subagents that need conversation memory across calls (e.g., research assistants building context).

## Multi-Level Nesting

Subgraphs can nest arbitrarily deep. Each level maintains its own state isolation—parent keys are inaccessible within child graphs, and child keys are invisible to grandparents.
