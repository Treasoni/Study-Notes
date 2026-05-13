# Context Engineering Guide

- **Source**: https://www.promptingguide.ai/guides/context-engineering-guide
- **Author**: PromptingGuide.ai
- **Date**: 2024
- **Type**: guide

---

## What is Context Engineering?

Context engineering is the refined evolution of prompt engineering—a systematic approach to designing and optimizing all context provided to an LLM's context window. It encompasses tuning system prompts, managing dynamic elements, structuring inputs/outputs, implementing RAG, and orchestrating tools and memory systems.

## Core Components

- **System Prompt**: The foundational instruction set defining the agent's role and capabilities
- **Instructions**: High-level directives specifying exact tasks
- **User Input**: Structured with delimiters for clarity
- **Structured Outputs**: JSON schemas ensuring consistent, parseable results
- **Tools**: Dynamic context (like date/time) that eliminate assumptions
- **RAG & Memory**: Vector stores for caching and retrieval optimization
- **States & Historical Context**: Managing revision phases and prior outputs

## Practical Example

The guide demonstrates a Search Planner agent for deep research. It requires explicit field definitions ("priority: int # 1 (highest) to 5 (lowest)") and date range inference to generate proper search subtasks.

## Key Insight

"Context engineering is not just about optimizing your prompt; it's about choosing the right context for the goals you are targeting."

## Advanced Considerations

Context compression, management techniques, safety, and effectiveness evaluation remain active areas of development.
