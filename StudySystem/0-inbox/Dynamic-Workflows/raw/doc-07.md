# Claude Code Dynamic Workflows - Community Issues & Feedback

> Source: https://github.com/anthropics/claude-code/issues?q=is%3Aissue+ultracode+workflow
> Note: 53 issues related to ultracode and workflows. Aggregated community feedback from GitHub.

## Overview

This is a summary of community-reported issues, bugs, and feature requests for the dynamic workflows and ultracode features of Claude Code. The issues span from the initial release (v2.1.154, May 28, 2026) through mid-June 2026, painting a picture of a new and rapidly evolving feature.

## Critical Issues: Excessive Agent Spawning & Cost

| # | Title |
|---|---|
| 69166 | "I asked claude to research something with sonnet agents it started with 5 but then they spawn their agents in total 273 background agents" |
| 68285 | "Workflow fan-out inherits a premium-tier default with no per-agent cost ceiling, causing ~$1k in auto-purchased charges" |
| 67636 | "Parallel agent spawning causes excessive token consumption before crashing or hitting limits" |
| 66867 | "Fable 5 Ultracode spawns excessive parallel agents for single refactoring task" |
| 66023 | "Workflow tool: one invocation spawned 46 Opus subagents (~3M tokens) with no cost confirmation" |
| 66762 | "Ultracode mode can silently consume an entire 5-hour usage window on subagent fleets" |

## Key Themes

### 1. Agent Spawning Explosions
Multiple reports of ultracode/workflows spawning hundreds of subagents, burning millions of tokens. This suggests that without careful prompting, dynamic workflows can over-fan-out and create runaway cost situations.

### 2. Cost Control Gaps
No per-agent cost ceiling in workflow fan-out scenarios, leading to unexpected charges. One user reported ~$1k in auto-purchased charges from a single fan-out. Another reported 70 agents drained a plan limit in <10 minutes.

### 3. Model/Aggregation Bugs
Various UI inconsistencies (status line, effort slider) where ultracode state isn't properly reflected. The status line provides no way to distinguish `ultracode` from `xhigh`. Desktop app and VS Code extension effort pickers silently drop or hide ultracode state.

### 4. Resume/Compaction Issues
Workflow runs failing to resume correctly after auto-compaction. When resuming a failed workflow, all 26 Fetch-phase agents re-spawned and re-ran, burning ~19k tokens each (~494k tokens total waste). The `fetch:unknown` labels indicate non-deterministic prompt/label construction that breaks cache key matching.

### 5. Documentation Drift
Docs still reference `ultracode` as a trigger keyword in workflows. v2.1.178 only triggers on explicit phrases. Built-in Workflow tool description (~4k tokens) injected as conversation content every turn, with no way to disable.

### 6. Workflow Subagents Cannot Spawn Nested Subagents (Issue #69135)
Workflow `agent()` subagents currently cannot spawn nested subagents. Users want the Agent tool granted to workflow subagents to allow deeper nesting hierarchies.

### 7. Workflow Tool Arguments
Arguments passed to workflows arrive JSON-stringified rather than as native objects, causing parsing issues. Workaround: `const args = typeof args === 'string' ? JSON.parse(args) : args;`

### 8. Built-in Workflow Issues
- `deep-research` workflow aborts entire run when any schema-bound subagent fails to emit StructuredOutput
- Built-in dynamic workflows like `deep-research` have no model routing - all sub-agents inherit the main-loop model, burning Opus on grunt work unnecessarily

## Feature Requests

| # | Title |
|---|---|
| 65446 | "Allow the Dynamic Workflows sandbox to execute external code/tools" |
| 66703 | "Dynamic workflows should auto-select appropriate model instead of inheriting parent model" |

## Practical Observations from Users

- **Auto-authored fan-outs inherit expensive models by default** - need to explicitly request cheaper models per stage
- **Args parsing inconsistency** - args come as JSON strings, not native objects
- **Journal keys at `/workflows/<runId>/journal/`** - can be inspected for cache key debugging
- **Rate-limit failures mislabeled as refutation** - infrastructure failures end up in "refuted" array, killing valid claims
- **Best practice**: ensure `agent()` labels/prompts are pure functions of deterministic inputs to maintain cache key stability

## Implications for Users

1. **Start small** - Test workflows on a slice of the problem first to gauge cost
2. **Be explicit about model selection** - Ask Claude to use a smaller model for stages that don't need the strongest one
3. **Watch for runaway fan-out** - The dynamic nature means workflows can spawn more agents than you expect
4. **Use `/workflows` to monitor** - Track progress and stop runs that are spinning out
5. **Don't rely on ultracode for routine work** - Drop back to `/effort high` for normal sessions
