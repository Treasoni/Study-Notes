# Prompt Engineering - Wikipedia

- **Source**: https://en.wikipedia.org/wiki/Prompt_engineering
- **Author**: Wikipedia Contributors
- **Date**: 2024
- **Type**: official

---

## Definition

Prompt engineering is "the process of structuring natural language inputs (known as prompts) to produce specified outputs from a generative artificial intelligence (GenAI) model." It can also be described as "the practice of designing and refining input instructions given to a generative AI model to produce more accurate, relevant, or useful outputs."

## Key Techniques

**Multi-shot prompting** includes examples in the prompt for the model to learn from in context, called few-shot learning.

**Chain-of-thought (CoT)** prompting allows LLMs to solve problems as a series of intermediate steps before giving final answers. As originally proposed by Google, CoT uses input/output exemplars as a few-shot technique. Research found that simply appending "Let's think step-by-step" also worked as a zero-shot approach.

**Tree-of-thought** prompting generalizes chain-of-thought by generating multiple lines of reasoning in parallel, with the ability to backtrack or explore other paths.

**Self-consistency** performs several chain-of-thought rollouts, then selects the most commonly reached conclusion.

**Text-to-image prompting** involves describing desired subject, medium, style, lighting, color, and texture.

## Best Practices

Effective prompt engineering involves:
- Designing clear queries
- Refining wording
- Providing relevant context
- Specifying output style
- Assigning a character or role for the AI to mimic

## Context Engineering

A related discipline "focuses on the management of non-prompt contexts supplied to the GenAI model, such as metadata, API tools, and tokens."

## Automated Methods

**Retrieval-augmented generation (RAG)** enables models to retrieve and incorporate new information from specified documents.

**Gradient descent methods** like prefix-tuning and prompt tuning search floating-point vectors to maximize log-likelihood on outputs.

## Historical Note

The article notes that employees with the title "prompt engineer" were hired during the 2020s AI boom, though "the individual title has since lost traction amid AI models that produce better prompts than humans."
