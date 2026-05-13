# Tree of Thoughts (ToT)

- **Source**: https://www.promptingguide.ai/guide/techniques/tot
- **Author**: Yao et al., 2023
- **Date**: 2023
- **Type**: research

---

## What is ToT?

Tree of Thoughts is a framework (Yao et al., 2023; Long, 2023) that generalizes chain-of-thought prompting. It maintains a tree structure where "thoughts" are coherent language sequences serving as intermediate problem-solving steps.

## Key Features

- Enables language models to self-evaluate progress through deliberate reasoning
- Combines thought generation/evaluation with search algorithms (BFS, DFS, beam search)
- Supports lookahead exploration and backtracking

## Applications

Works best for complex tasks requiring strategic planning, like the Game of 24 mathematical reasoning task. Results significantly outperform other prompting methods on such problems.

## Simpler Variant

Hulbert (2023) proposed Tree-of-Thought Prompting, a simplified version using a single prompt to evaluate intermediate thoughts.
