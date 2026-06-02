# LangGraph Time Travel

**URL**: https://docs.langchain.com/oss/python/langgraph/use-time-travel

## Concept

LangGraph enables time travel through checkpoints, supporting two operations: **Replay** (retry from a prior checkpoint) and **Fork** (branch with modified state to explore alternatives).

## Replay

Replay uses `get_state_history` to locate checkpoints and `invoke` to resume execution. "Replay re-executes nodes—it doesn't just read from cache."

## Fork

Fork calls `update_state` on a prior checkpoint to create a branching path. "update_state does NOT roll back a thread. It creates a new checkpoint that branches from the specified point."

## Interrupts During Time Travel

Interrupts (for human-in-the-loop workflows) are always re-triggered during time travel. The node containing the interrupt re-executes and pauses for new input.

## Subgraphs and Time Travel

Subgraphs have limited time travel when using inherited checkpointers—the entire subgraph is treated as one step. Giving a subgraph its own checkpointer enables granular time travel within it.
