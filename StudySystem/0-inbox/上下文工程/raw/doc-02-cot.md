# Chain-of-Thought Prompting

- **Source**: https://www.promptingguide.ai/guide/techniques/cot
- **Author**: PromptingGuide.ai
- **Date**: 2024
- **Type**: guide

---

## Key Points

- **CoT Prompting** (Wei et al., 2022) enables complex reasoning by showing intermediate steps
- Works best when combined with few-shot examples demonstrating the reasoning process
- Described as an "emergent ability" in large language models
- Even a single example can be effective for some tasks

## Zero-shot CoT

- Simply adding "Let's think step by step" to prompts significantly improves reasoning
- Researched by Kojima et al., 2022
- Particularly useful when examples aren't available

## Auto-CoT

- Automates demonstration creation using LLMs
- Two stages: question clustering, then demonstration sampling
- Uses heuristics like question length and reasoning steps
- Reduces manual effort while maintaining effectiveness
