# Building Effective AI Agents (Anthropic)

**URL**: https://www.anthropic.com/research/building-effective-agents

## Key Distinction: Workflows vs. Agents

**Workflows** are orchestrated through predefined code paths. **Agents** dynamically direct their own processes and tool usage.

## When to Use Agents vs. Simpler Solutions

- For many applications, "optimizing single LLM calls with retrieval and in-context examples is usually enough"
- Agentic systems trade latency and cost for better task performance
- Workflows suit well-defined, predictable tasks
- Agents suit open-ended problems where required steps can't be hardcoded

## Building Blocks & Workflows

1. **The Augmented LLM** — LLM enhanced with retrieval, tools, and memory
2. **Prompt Chaining** — Sequential steps where each LLM call processes the previous output
3. **Routing** — Classifying input to direct it to specialized follow-up tasks
4. **Parallelization** — Sectioning (breaking into independent subtasks) or voting (running same task multiple times)
5. **Orchestrator-Workers** — Central LLM dynamically breaks down tasks, delegates, and synthesizes results
6. **Evaluator-Optimizer** — One LLM generates while another provides feedback in a loop

## Three Core Agent Principles

1. Maintain **simplicity** in design
2. Prioritize **transparency** by showing planning steps
3. Craft your agent-computer interface (ACI) through thorough tool **documentation and testing**

## Tool Design Tips

- Give models enough tokens to "think" before writing
- Keep formats close to naturally occurring text
- Eliminate formatting overhead
- Invest in ACI like you would in HCI
