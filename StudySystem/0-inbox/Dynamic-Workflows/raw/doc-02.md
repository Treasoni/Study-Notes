# Run Agents in Parallel - Official Documentation

> Source: https://code.claude.com/docs/en/agents.md
> Title: Run agents in parallel

## Overview

Subagents, agent view, agent teams, and dynamic workflows each parallelize work in a different way. The right one depends on whether you want to stay in each conversation yourself, hand tasks off and check back later, or have Claude coordinate a group of workers for you.

## Comparison Table

| Approach | What it gives you | Use it when |
|---|---|---|
| **Subagents** | Delegated workers inside one session that do a side task in their own context and return a summary | A side task would flood your main conversation with search results, logs, or file contents you won't reference again |
| **Agent view** | One screen to dispatch and monitor sessions running in the background, opened with `claude agents`. Research preview | You have several independent tasks and want to hand them off, check status at a glance, and step in only when one needs you |
| **Agent teams** | Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead. Experimental and disabled by default | You want Claude to split a project into pieces, assign them, and keep the workers in sync |
| **Dynamic workflows** | A script that runs many subagents and cross-checks their results, for work too big to coordinate one turn at a time or that needs more than a single pass | A job outgrows a handful of subagents, or you want findings verified against each other: a codebase-wide audit, a 500-file migration, cross-checked research, or a plan drafted from several angles |

In every approach the workers are Claude sessions. To involve a different tool, expose it to Claude as an MCP server.

## Supporting Tools

Two more tools support this work without being a way to run agents themselves:

- **Worktrees** give each session a separate git checkout, so parallel sessions never edit the same files. Use them for sessions you run yourself. Agent view moves each dispatched session into its own worktree automatically, and subagents you spawn can each get one too.
- **`/batch`** is a skill that has Claude split one large change into 5 to 30 worktree-isolated subagents that each open a pull request. It's a packaged use of subagents and worktrees, not a separate coordination style.

## Other Related Features (Not Parallel Agent Runners)

- A **background bash command** runs one shell command without blocking the conversation. It doesn't spawn an agent.
- A **forked subagent** is a subagent that inherits your full conversation context instead of starting fresh. It's a way to spawn a subagent, not a separate surface.
- A **routine** runs a session on a schedule in Anthropic's cloud, not in parallel on your machine.

**Note:** Running several sessions or subagents at once multiplies token usage. See Costs for usage and rate-limit details.

## Choosing an Approach

The right approach depends on who coordinates the work, whether the workers need to communicate, and whether they edit the same files:

**Who coordinates the work?**
- Claude delegates and collects results inside one conversation: subagents
- You hand off independent tasks and check back later: agent view
- Claude plans, assigns, and supervises a group of workers: agent teams (experimental and disabled by default)
- A script holds the plan instead of Claude's turn-by-turn judgment: dynamic workflows

**Do the workers need to talk to each other?**
- Subagents report results back to the conversation that spawned them
- Agent view sessions report only to you
- Teammates in an agent team share a task list and message each other directly

**Do the tasks touch the same files?**
- Isolate the work with worktrees
- Subagents and sessions you run yourself can each use a separate worktree
- Agent teams don't isolate teammates in worktrees, so partition the work so each teammate owns a different set of files

## Checking on Running Work

| Approach | How to check |
|---|---|
| Background sessions | `claude agents` opens agent view |
| Subagents in current session | `/agents` opens a panel with Running and Library tabs |
| Anything in background of current session | `/tasks` lists each item |
| Dynamic workflows | `/workflows` lists running and completed runs, the phase each is in, and how many agents have finished |

## Key Takeaway

Dynamic workflows are positioned as the "scale" option when subagents are insufficient. Where subagents handle a few delegated tasks per turn, workflows can orchestrate dozens to hundreds of agents with cross-checking of results - making them ideal for jobs that outgrow subagent coordination or that need adversarial verification.
