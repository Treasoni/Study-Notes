# LangGraph Graph API Overview

**URL**: https://docs.langchain.com/oss/python/langgraph/graph-api

## Nodes

Nodes are Python functions that accept state, config, and runtime arguments. They perform the actual work in your graph. You add nodes using `builder.add_node("name", function)`.

## Edges

Edges determine control flow—specifically which node executes next. There are normal edges (static routing) and conditional edges (dynamic routing). Use `add_edge()` for static transitions and `add_conditional_edges()` with a routing function for dynamic branching.

## Conditional Edges

Conditional edges accept a routing function that receives current state and returns the next node name(s). Multiple destination nodes execute in parallel as part of the next superstep. Optionally provide a mapping dictionary to translate function outputs to node names.

## The `Command` Primitive

The `Command` primitive combines state updates and control flow in one step. It accepts:
- `update` — state modifications
- `goto` — navigation
- `graph` — parent graph targeting
- `resume` — continuing after interrupts

Return `Command` from node functions to update state and route simultaneously.

## State Reducers

State reducers define how node updates are applied to the graph state. Each state key has its own reducer—default reducers overwrite values, while custom reducers like `operator.add` accumulate or transform updates. Use `Annotated` with type hints to specify reducer functions.

## Branches

Branches are implemented via conditional edges or `Command` returning different destinations based on state conditions.
