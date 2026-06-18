# Claude Code Commands - Official Reference (excerpt for Dynamic Workflows)

> Source: https://code.claude.com/docs/en/commands.md
> Title: Commands

## Overview

Commands control Claude Code from inside a session. They provide a quick way to switch models, manage permissions, clear context, **run a workflow**, and more.

Type `/` to see every command available to you, or type `/` followed by letters to filter.

## Commands Across a Typical Workflow

The command reference describes a typical user flow where commands are useful:

**First session in a repo.** Run `/init` to generate a starter `CLAUDE.md`, then `/memory` to refine it. Use `/mcp` and `/agents` to set up any servers or subagents the project needs, and `/permissions` to set the approval rules you want.

**During a task.** `/plan` switches into plan mode before a large change. `/model` and `/effort` adjust how much reasoning you're spending. When the conversation gets long, `/context` shows where the window is going and `/compact` summarizes it down; use `/btw` for a quick aside.

**Running work in parallel.** `/agents` opens the manager for the subagents Claude can delegate side tasks to, and `/tasks` lists what's running in the background of the current session. `/background` detaches the whole session to keep running as a background agent. **For a large change that spans the codebase, `/batch` decomposes it into independent units and runs each in its own worktree.** See Run agents in parallel for how these approaches relate.

**Before you ship.** `/diff` shows what changed, `/code-review` checks the diff for correctness bugs and cleanups and can apply the findings with `--fix`, and `/review` or `/security-review` give a deeper read-only pass. `/code-review ultra` runs a multi-agent review in the cloud.

## Key Commands for Dynamic Workflows

| Command | Type | Purpose |
|---|---|---|
| `/workflows` | Built-in | Open the workflow progress view to watch, pause, resume, or save running and completed workflows |
| `/deep-research <question>` | **Workflow** | Fan out web searches on a question, fetch and cross-check sources, and synthesize a cited report |
| `/effort [level\|auto]` | Built-in | Set the model effort level. Accepts `low`, `medium`, `high`, `xhigh`, `max`, or `ultracode`; available levels depend on the model. `ultracode` combines `xhigh` reasoning with automatic workflow orchestration |
| `/batch <instruction>` | **Skill** | Orchestrate large-scale changes across a codebase in parallel. Decomposes the work into 5 to 30 independent units and spawns one background subagent per unit in an isolated git worktree. Example: `/batch migrate src/ from Solid to React` |

## Command Type Legend

From the docs:
- **[Skill]** - a bundled skill. It works like skills you write yourself: a prompt handed to Claude, which Claude can also invoke automatically when relevant.
- **[Workflow]** - a bundled dynamic workflow that fans work out across many subagents and runs in the background.

## The `/effort` Command

> Set the model effort level. Accepts `low`, `medium`, `high`, `xhigh`, `max`, or `ultracode`; available levels depend on the model, and `max` and `ultracode` are session-only. `ultracode` is a Claude Code setting that combines `xhigh` reasoning with automatic workflow orchestration. `auto` resets to the model default. Without an argument, opens an interactive slider; use left and right arrows to pick a level and `Enter` to apply. Takes effect immediately without waiting for the current response to finish.

## The `/deep-research` Bundled Workflow

> **[Workflow].** Fan out web searches on a question, fetch and cross-check sources, and synthesize a cited report

This is the only bundled workflow. It requires the WebSearch tool to be available. Workflows you save yourself become commands the same way and appear in `/` autocomplete alongside the bundled ones.

## Distinguishing Commands, Skills, and Workflows

The command reference makes the distinction explicit:

| | How Claude learns about it | Where it runs | How it executes |
|---|---|---|---|
| **Built-in command** | Hardcoded in CLI | Main session | Coded logic in CLI |
| **Skill** | Description in context, full body loads when invoked | Main context or forked subagent | Claude reads the prompt and uses its tools |
| **Workflow** | Available via `/` autocomplete | Background process with isolated runtime | Script executes to orchestrate subagents |

This three-tier model is important: workflows are not just "another kind of skill." They are a fundamentally different execution model where the runtime is responsible for spawning and coordinating subagents, not Claude itself.

## Slash Command Naming Convention

When you save a custom workflow, the file name (or directory name) becomes the slash command. The command runs as `/<name>` in future sessions from either `.claude/workflows/` (project) or `~/.claude/workflows/` (personal).

If a project workflow and a personal workflow share a name, the project one runs.

## MCP Prompts

MCP servers can expose prompts that appear as commands. These use the format `/mcp__<server>__<prompt>` and are dynamically discovered from connected servers. This is yet another way custom commands can enter the system.
