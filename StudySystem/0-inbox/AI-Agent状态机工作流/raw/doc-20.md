# State Machine Patterns in LangGraph (Guardrails & Routing)

**URL**: https://docs.langchain.com/oss/python/langgraph/graph-api

## Core Components

"Nodes do the work, edges tell what to do next." State consists of schema plus reducer functions specifying state updates. Nodes (functions) receive current state, perform computation, return updates. Edges determine routing—either static or conditional based on state.

## FSM Routing Mechanisms

- **Normal edges** for fixed transitions
- **Conditional edges** for dynamic routing via routing functions
- **`Command` primitive** combines state updates and control flow
- **`Send`** for map-reduce patterns with dynamic edges

## Agent Guardrails

- **Recursion limits** (default 1000 steps) prevent infinite loops
- **`RemainingSteps` managed value** enables proactive limit handling
- **`interrupt()`** pauses graph for human review/approval
- **Graceful degradation** via fallback nodes when approaching limits

## Execution Model

- **Super-steps** as discrete iteration cycles
- **Parallel nodes** execute within same super-step
- **Nodes vote to halt** when no incoming messages
