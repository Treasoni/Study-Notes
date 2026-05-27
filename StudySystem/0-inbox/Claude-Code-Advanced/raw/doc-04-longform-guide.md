# The Longform Guide to Everything Claude Code
- **Source**: https://x.com/affaan/status/2014040193557471352
- **Author**: @affaan
- **Date**: 2026-01-17
- **Type**: blog/tutorial

---
# The Longform Guide to Everything Claude Code

## Overview

This longform guide covers techniques that separate productive sessions from wasteful ones. Themes: token economics, memory persistence, verification patterns, parallelization strategies, and compound effects of building reusable workflows.

## Context & Memory Management

### Session Persistence Pattern

For sharing memory across sessions:
- Create a skill that summarizes progress and saves to `.tmp` file in `.claude` folder
- Append until end of session
- Next day, use that file as context and pick up where you left off
- Create new file for each session to avoid polluting old context
- Eventually back up or prune session logs

### Session State File Pattern

Claude creates a file summarizing current state. Review it, ask for edits if needed, then start fresh. Provide file path for new conversation. Useful when hitting context limits.

Files should contain:
- What approaches worked (verifiably with evidence)
- Which approaches were attempted but did not work
- Which approaches have not been attempted
- What's left to do

### Clearing Context Strategically

Once plan is set and context cleared (default option in plan mode):
- Work from the plan
- Useful when you've accumulated exploration context that's no longer relevant
- For strategic compacting: disable auto compact, manually compact at logical intervals
- Create a skill that suggests compaction upon defined criteria

### Advanced: Dynamic System Prompt Injection

Instead of putting everything in CLAUDE.md or `.claude/rules/`, use CLI flags to inject context dynamically:

```bash
claude --system-prompt "$(cat memory.md)"
```

Difference from @ file references:
- [@file.md](@file.md) or `.claude/rules/`: Claude reads via Read tool during conversation (tool output)
- `--system-prompt`: Injected into actual system prompt before conversation starts

System prompt content has higher authority hierarchy:
1. System prompt (highest)
2. User messages
3. Tool results (lowest)

### Practical Setup

Use `.claude/rules/` for baseline project rules, then CLI aliases for scenario-specific context:

```bash
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

### Advanced: Memory Persistence Hooks

Three key hooks for memory:
- **PreCompact Hook**: Before context compaction, save important state to file
- **SessionComplete Hook**: On session end, persist learnings to file
- **SessionStart Hook**: On new session, load previous context automatically

Chain these together for continuous memory across sessions without manual intervention.

## Continuous Learning / Memory

When Claude discovers something non-trivial:
- Save knowledge as a new skill
- Next time similar problem arises, skill loads automatically

**The Problem**: Wasted tokens, context, time, frustration from repeating same corrections.

**The Solution**: Stop hook evaluates session at end, extracts patterns worth extracting (error resolutions, debugging techniques, workarounds, project-specific patterns) and saves them as reusable skills in `~/.claude/skills/learned/`.

## Token Optimization

### Primary Strategy: Subagent Architecture

Delegate the cheapest possible model sufficient for the task:
- Trial and error to learn Haiku vs Sonnet vs Opus
- Haiku: repetitive tasks, clear instructions, "worker" in multi-agent setup
- Sonnet: 90% of coding tasks
- Opus: first attempt failed, task spans 5+ files, architectural decisions, security-critical code

Price comparison: Haoku vs Opus is 5x cost difference. Sonnet vs Opus is only 1.67x.

### Tool-Specific Optimizations

Replace grep with mgrep - can reduce tokens by ~50%.

### Background Processes

Run background processes outside Claude when you don't need Claude to process the entire output. Use tmux, take terminal output and summarize what you need. Saves on input tokens.

### Modular Codebase Benefits

- More modular codebase with reusable utilities
- Main files hundreds of lines instead of thousands
- Helps both token optimization AND getting task right on first try
- Avoids repeated file reading and context loss

### System Prompt Slimming (Advanced)

Claude Code's system prompt takes ~18k tokens. Can be reduced to ~10k with patches, saving ~41% of static overhead.

## Verification Loops and Evals

### Observability Methods

- tmux processes hooked to trace thinking stream and output when skill triggers
- PostToolUse hook that logs what Claude specifically enacted and exact change/output

### Benchmarking Workflow

Compare task with skill vs without skill using worktrees, check diff at end.

### Eval Pattern Types

**Checkpoint-Based Evals**:
- Set explicit checkpoints in workflow
- Verify against defined criteria at each checkpoint
- Good for linear workflows with clear milestones

**Continuous Evals**:
- Run every N minutes or after major changes
- Full test suite, build status, lint
- Good for long-running sessions, exploratory refactoring

### Grader Types

- **Code-Based Graders**: String match, binary tests, static analysis, outcome verification. Fast, cheap, objective, but brittle.
- **Model-Based Graders**: Rubric scoring, natural language assertions, pairwise comparison. Flexible, handles nuance, but non-deterministic, expensive.
- **Human Graders**: SME review, crowdsourced judgment, spot-check. Gold standard, but expensive and slow.

### Key Metrics

- **pass@k**: At least ONE of k attempts succeeds. Higher k = higher odds.
- **pass^k**: ALL k attempts must succeed. Higher k = harder (consistency).

## Parallelization

### My Preferred Pattern

Main chat: working on code changes. Forks: questions about codebase, research on external services.

### On Arbitrary Terminal Counts

Don't set arbitrary terminal amounts. Addition of terminal should be out of true necessity and purpose. Use scripts when possible.

### When Scaling Instances

If using multiple instances working on overlapping code:
- Use git worktrees
- Have very well-defined plan for each
- Use `/rename` to name all chats

### Git Worktrees for Parallel Instances

```bash
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
cd ../project-feature-a && claude
```

Benefits: No git conflicts, clean working directory, easy to compare outputs, benchmark across approaches.

### The Cascade Method

- Open new tasks in new tabs to the right
- Sweep left to right, oldest to newest
- Maintain consistent direction flow
- Focus on at most 3-4 tasks at a time

## Groundwork

### The Two-Instance Kickoff Pattern

**Instance 1: Scaffolding Agent**
- Lays down scaffold and groundwork
- Creates project structure
- Sets up configs (CLAUDE.md, rules, agents)
- Establishes conventions

**Instance 2: Deep Research Agent**
- Connects to all services, web search
- Creates detailed PRD
- Creates architecture mermaid diagrams
- Compiles references with actual clips

### llms.txt Pattern

Find llms.txt on documentation by doing `/llms.txt` on docs page. Gives clean, LLM-optimized version.

### Philosophy: Build Reusable Patterns

Investment in patterns > investment in specific model tricks. All workflows transferable to other agents like Codex.

## Best Practices for Agents & Sub-Agents

### The Sub-Agent Context Problem

Sub-agents exist to save context by returning summaries. But orchestrator has semantic context sub-agent lacks. Summaries often miss key details.

### Iterative Retrieval Pattern

To fix:
1. Orchestrator dispatch with query + objective
2. Sub-agent returns summary
3. Orchestrator evaluates: sufficient?
4. If no: ask follow-up questions, sub-agent fetches answers
5. Max 3 cycles to prevent infinite loops

Pass objective context, not just the query.

### Pattern: Orchestrator with Sequential Phases

```
Phase 1: RESEARCH (Explore agent)
Phase 2: PLAN (planner agent)
Phase 3: IMPLEMENT (tdd-guide agent)
Phase 4: REVIEW (code-reviewer agent)
Phase 5: VERIFY (build-error-resolver if needed)
```

Key rules:
- Each agent gets ONE clear input, produces ONE clear output
- Outputs become inputs for next phase
- Never skip phases
- Use `/clear` between agents
- Store intermediate outputs in files

### Agent Abstraction Tierlist

**Tier 1: Direct Buffs (Easy to Use)**
- Subagents
- Metaprompting
- Asking user more at beginning

**Tier 2: High Skill Floor (Harder to Use Well)**
- Long-running agents
- Parallel multi-agent
- Role-based multi-agent
- Computer use agents

Takeaway: Start with Tier 1 patterns. Only graduate to Tier 2 when mastered basics and have genuine need.

## Tips and Tricks

### MCPs are Replaceable

MCPs for version control, databases, deployment - these platforms already have robust CLIs. Instead of having GitHub MCP loaded at all times, create `/gh-pr` command wrapping `gh pr create`. Instead of Supabase MCP, create skills using Supabase CLI directly.

With lazy loading, context window issue mostly solved. But CLI + skills approach is still token optimization method.

## References

- Anthropic: Demystifying evals for AI agents (Jan 2026)
- Anthropic: Claude Code Best Practices (Apr 2025)
- Fireworks AI: Eval Driven Development with Claude Code (Aug 2025)
- YK: 32 Claude Code Tips (Dec 2025)
- Addy Osmani: My LLM coding workflow going into 2026
- @PerceptualPeak: Sub-Agent Context Negotiation
- @menhguin: Agent Abstractions Tierlist
- @omarsar0: Compound Effects Philosophy
- RLanceMartin: Session Reflection Pattern
- @alexhillman: Self-Improving Memory System
