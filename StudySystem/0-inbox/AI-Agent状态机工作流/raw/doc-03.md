# Human-in-the-Loop and Interrupts in LangGraph

**URL**: https://docs.langchain.com/oss/python/langgraph/interrupts

## Core Concept

Interrupts enable human-in-the-loop patterns by pausing graph execution at specific points to wait for external input before continuing.

## Key Features

- Dynamic interrupts can be placed anywhere in code and made conditional
- Requires a checkpointer to persist graph state
- Uses `thread_id` to identify which state to resume
- Interrupt payloads surface via `stream.interrupts` when using event streaming

## Basic Usage Pattern

```
interrupt("message") → pauses graph → returns value on resume
```

## Approval Workflow Pattern

```
interrupt({"question": "...", "details": state["action_details"]})
→ resume with True/False to approve/reject
→ use Command(goto="proceed" or "cancel") to route
```

## Important Rules

- Do not wrap `interrupt()` in try/except blocks
- Do not conditionally skip or loop `interrupt()` calls (order must be consistent)
- Pass only JSON-serializable values to interrupts
- Side effects before interrupts must be idempotent (or place them after)

## Resuming Execution

```
graph.stream_events(Command(resume=value), config=config, version="v3")
```

## Multiple Interrupts

When resuming parallel branches, map interrupt IDs to resume values in a dictionary.
