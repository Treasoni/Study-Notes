# Zero-Shot Prompting

- **Source**: https://www.promptingguide.ai/techniques/zeroshot
- **Author**: PromptingGuide.ai
- **Date**: 2024
- **Type**: guide

---

## Definition

Zero-shot prompting is a technique where prompts contain no examples or demonstrations—instructions are given directly to the model to perform a task.

## Key Points

- Large language models (e.g., GPT-3.5, GPT-4, Claude 3) can perform tasks without examples due to large-scale training
- Example: "Classify the text into neutral, negative or positive. Text: I think the vacation is okay. Sentiment:" → "Neutral"
- Instruction tuning improves zero-shot learning (Wei et al., 2022)
- RLHF (reinforcement learning from human feedback) helps align models to human preferences
- When zero-shot fails, few-shot prompting with demonstrations is recommended
