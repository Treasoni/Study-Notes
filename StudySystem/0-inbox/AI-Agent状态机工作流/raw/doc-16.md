# LangGraph v0.2 Features (Checkpointer Ecosystem)

**URL**: https://www.langchain.com/blog/langgraph-v0-2

## New Checkpointer Libraries

LangGraph v0.2 introduces a new ecosystem of checkpointer libraries for building resilient LLM applications:

- **langgraph_checkpoint** - Base interface with `BaseCheckpointSaver` and `MemorySaver` for experimentation
- **langgraph_checkpoint_sqlite** - SQLite implementation for local workflows
- **langgraph_checkpoint_postgres** - Optimized Postgres checkpointer for production

## Core Capabilities

Checkpointers enable:
- Session memory
- Error recovery
- Human-in-the-loop features
- Time travel (forking threads)

## Postgres Optimizations

- **Write-side**: Postgres pipeline mode reduces database roundtrips; stores each channel value separately
- **Read-side**: Cursor-based fetching for efficient long thread histories

## Breaking Changes

- `thread_ts` → `checkpoint_id`
- `parent_ts` → `parent_checkpoint_id`
- Imports now require full paths (e.g., `from langgraph.checkpoint.sqlite import SqliteSaver`)
- SQLite checkpointer requires separate installation: `pip install langgraph-checkpoint-sqlite`

## Additional Context

LangGraph Cloud is available in open beta for LangSmith users on Plus or Enterprise plans, offering fault-tolerant scalability with the Postgres checkpointer built-in.
