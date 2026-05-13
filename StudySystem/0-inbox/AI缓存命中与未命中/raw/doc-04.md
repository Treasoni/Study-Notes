# Prompt Caching in LLMs

## The Core Problem
Every agent turn sends the entire conversation history back to the LLM, including redundant system instructions and tool definitions already processed earlier. This creates significant wasted computation and cost.

## Static vs. Dynamic Context
- **Static prefix**: System instructions, tool definitions, project context—stays identical across turns
- **Dynamic suffix**: User messages, assistant responses, tool outputs—grows with every turn

## How KV Cache Works
During the prefill phase, transformers compute Query, Key, and Value vectors for each token. The Key and Value tensors are persisted on inference servers, indexed by a cryptographic hash of the token sequence.

> "The Key and Value tensors are persisted on inference servers, indexed by a cryptographic hash."

When a new request shares the same prefix, these tensors load from memory, skipping recomputation. This drops complexity from O(n²) to O(n) per generated token.

## Economics
- **Cache reads**: 0.1x base input price (90% discount)
- **Cache writes**: 1.25x base input price (25% premium)
- **Extended one-hour caching**: 2.0x base input price

## Critical Constraint
Hash-based caching means the full token sequence must remain identical. Even token order changes cause a cache miss.

> "If anything in that sequence changes, even just the order of two elements, the hash changes."

## Best Practices
1. Never modify tools mid-session
2. Never switch models mid-session
3. Never mutate the prefix to update state—append reminder tags to messages instead
4. Structure prompts: system instructions → tool definitions → reference context → conversation history

## Real-World Results
Claude Code demonstrates a **92% cache hit rate** and **81% cost reduction** in a 30-minute coding session.
