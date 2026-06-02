# CrewAI Memory System

**URL**: https://docs.crewai.com/concepts/memory

## Unified Memory Architecture

CrewAI's unified memory provides a single `Memory` class that organizes information hierarchically using scopes (like a filesystem path structure). The system uses an LLM to analyze content when saving, inferring scope, categories, and importance automatically.

## Key Features

### Four Usage Patterns
- Standalone in scripts/notebooks
- Integrated with Crews (pass `memory=True` or a configured `Memory` instance)
- With Agents (scoped views for private context)
- Inside Flows (built-in `self.remember()`, `self.recall()`, `self.extract_memories()`)

### Memory Operations

```python
memory.remember("We chose PostgreSQL for the user database.")
matches = memory.recall("What database did we choose?")
memory.forget(scope="/project/old")
```

### Scoring System

Results ranked by composite score combining semantic similarity, recency (exponential decay), and importance weights.

### Privacy

Source tracking and private flags control memory visibility across users.

### Persistence

Default storage uses LanceDB at `./.crewai/memory`.

## Notable Capabilities

- **Non-blocking saves**: `remember_many()` runs in background threads
- **Memory consolidation**: Automatically deduplicates similar records using LLM analysis
- **Deep vs shallow recall**: Shallow is fast vector search; deep uses LLM query analysis for complex queries
- **Multiple embedder providers**: OpenAI, Ollama, Azure, Google, Cohere, VoyageAI, AWS Bedrock, Hugging Face, Jina, IBM WatsonX

The documentation emphasizes that memory integrates tightly with agent workflows—automatically extracting facts from task outputs and injecting relevant context before tasks run.
