# Lyft's Self-Serve AI Agent Platform (LangGraph Case Study)

**URL**: https://www.langchain.com/blog/lyft-built-a-self-serve-ai-agent-platform-for-customer-support-with-langgraph-and-langsmith

**Author**: Akshay Sharma
**Date**: May 27, 2026

## Architecture Overview

Lyft built a **router multi-agent architecture** on LangGraph. A meta agent classifies incoming requests and dispatches to specialized subagents using `Command(goto=...)`. Separate routers handle riders and drivers, each routing to domain-specific subagents (lost items, charge disputes, earnings, etc.).

## Two Agent Types

**Specialized agents** are hand-built by MLEs for complex workflows (damage claims, fraud detection). **Configurable agents** form the self-serve layer—loaded from JSON config at runtime with prompts from LangSmith's Prompt Hub. Domain experts write prompts following a structured template; the platform handles graph construction, tool binding, safety gates, and state management.

## State Machine Design

Each subagent follows a **consistent node pattern** with safety checks running in parallel via LangGraph's fan-out before LLM reasoning. Handoffs between agents use `Command(goto=..., graph=Command.PARENT)` to return control to the meta agent for re-routing. State persists across turns using a custom **DynamoDBSaver** implementing LangGraph's `BaseCheckpointSaver` interface.

## Observability with LangSmith

- **Tracing**: Every agent invocation traces full graph execution, node inputs/outputs, tool calls, token usage, and latency
- **Custom metadata**: Enriches traces with user type, agent name, intent, conversation ID for filtering
- **LLM-as-a-Judge evaluation**: Runs automatically on production traces with baseline metrics and domain-specific checks
- **Monitoring dashboards**: Track run volume, error rates, p50/p95 latency, token usage, tool call success rates, and judge scores over time
- **PagerDuty alerts**: Triggered when error rate exceeds 5% or p95 latency crosses 10 seconds over 15 minutes

## Key Lessons Learned

> "The hardest part was **prompt quality**. Domain experts knew their issue types deeply but didn't always know how to translate that knowledge into instructions an LLM would follow reliably."

Lyft discovered the bottleneck wasn't infrastructure but **prompt discipline**. They built a structured framework with five components: identity, primary objective, scope (in-scope AND out-of-scope), phased workflow with explicit entry/exit conditions, and content guidelines with concrete examples. They also implemented a Git-backed CI pipeline with static checks (malformed variables, spelling errors) and LLM-powered checks (prompt injection, contradictory instructions, structural dead-ends). All violations block merge. Their principle: "Treat prompts like product specs, not code comments."

## Results

- Development time reduced from ~6 months to ~2 weeks
- AI resolution rate increased 16%
- Hallucination and contradiction rates decreased 20%
- Non-engineering team members now build and iterate agents independently
