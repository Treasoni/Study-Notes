# LangGraph Concepts: State, Nodes, Edges

**URL**: https://docs.langchain.com/oss/python/langgraph/overview

## State

The runtime data that flows through the graph. The example uses `MessagesState` as the state schema, typed as a parameter in node functions.

## Nodes

Processing units that receive state, transform it, and return updates. Added via `graph.add_node(mock_llm)`.

## Edges

Direct connections defining flow between nodes. Created with `graph.add_edge(START, "mock_llm")` and `graph.add_edge("mock_llm", END)`.

## Conditional Edges

Not explicitly shown in this overview but implied by the "orchestration" focus.

## State Schema

Defined using typed structures like `MessagesState`, ensuring type safety for the state object passed to nodes.

## Relation to State Machines

LangGraph "is inspired by Pregel and Apache Beam" and draws from "NetworkX." While not explicitly a state machine framework, its graph-based architecture with defined nodes, edges, and state transitions naturally mirrors state machine patterns for agent orchestration—particularly for managing complex, multi-step workflows with durable execution.
