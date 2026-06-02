# LangGraph Persistence, Checkpointing, and State Management

**URL**: https://docs.langchain.com/oss/python/langgraph/persistence

## Core Persistence Concepts

LangGraph's persistence layer saves graph state as checkpoints at every execution step, organized into threads. This enables human-in-the-loop workflows, conversational memory, time travel debugging, and fault-tolerant execution.

**"A thread is a unique ID...that contains the accumulated state of a sequence of runs."**

**"A checkpoint is a snapshot of the graph state saved at each super-step."**

## Why Use Persistence

- **Human-in-the-loop**: Checkpointers allow humans to inspect, interrupt, and approve graph steps
- **Memory**: Enables conversation memory between interactions within a thread
- **Time travel**: Allows replaying past executions and forking state at checkpoints
- **Fault-tolerance**: Recovers from node failures at super-step boundaries
- **Pending writes**: Stores successful node outputs if other nodes in a super-step fail

## Key Components

### Threads and Checkpoints
- Threads use `thread_id` as the primary key for storage/retrieval
- A checkpoint is a `StateSnapshot` containing values, next nodes, config, metadata, and parent reference
- Super-steps represent single execution ticks where all scheduled nodes execute

### StateSnapshot Fields
| Field | Purpose |
|-------|---------|
| `values` | State channel values |
| `next` | Nodes to execute next |
| `config` | Thread ID and checkpoint ID |
| `metadata` | Source, writes, step counter |
| `parent_config` | Previous checkpoint reference |

### State Operations
- `graph.get_state(config)` — retrieve latest state
- `graph.get_state_history(config)` — retrieve full execution history
- `graph.update_state()` — create new checkpoint with modifications
- Replay from prior `checkpoint_id` to re-execute nodes

## Memory Store

The **Store** interface enables sharing information *across threads*, unlike checkpointers which are thread-specific.

**"The store allows us to store arbitrary information for access across threads."**

Features:
- Namespaced by tuples (e.g., `("user_id", "memories")`)
- Supports semantic search with embedding models
- Production options: PostgresStore, MongoDBStore, RedisStore

## Durability Modes

| Mode | Behavior | Trade-off |
|------|----------|-----------|
| `"exit"` | Persists only on completion/interrupt | Best performance |
| `"async"` | Persists asynchronously during execution | Good performance, small risk |
| `"sync"` | Persists synchronously before next step | High durability |

## Checkpointer Libraries

- `langgraph-checkpoint` — base interface with InMemorySaver
- `langgraph-checkpoint-sqlite` — SQLite for local workflows
- `langgraph-checkpoint-postgres` — Postgres for production
- `langchain-azure-cosmosdb` — Azure Cosmos DB support

Encryption is available via `EncryptedSerializer` using AES keys from `LANGGRAPH_AES_KEY`.
