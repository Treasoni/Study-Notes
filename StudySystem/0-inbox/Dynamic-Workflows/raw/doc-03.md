# Claude Code Subagents - Official Documentation

> Source: https://code.claude.com/docs/en/sub-agents.md
> Title: Create custom subagents

## Overview

Subagents are specialized AI assistants that handle specific types of tasks. Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary.

Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results.

**Note:** Subagents work within a single session. To run many independent sessions in parallel and monitor them from one place, see background agents (agent view). For sessions that communicate with each other, see agent teams.

## Why Use Subagents

- **Preserve context** by keeping exploration and implementation out of your main conversation
- **Enforce constraints** by limiting which tools a subagent can use
- **Reuse configurations** across projects with user-level subagents
- **Specialize behavior** with focused system prompts for specific domains
- **Control costs** by routing tasks to faster, cheaper models like Haiku

## Built-in Subagents

| Agent | Model | Tools | Purpose |
|---|---|---|---|
| **Explore** | Haiku (fast, low-latency) | Read-only tools (no Write, no Edit) | File discovery, code search, codebase exploration |
| **Plan** | Inherits from main | Read-only tools | Codebase research during plan mode |
| **General-purpose** | Inherits from main | All tools | Complex research, multi-step operations, code modifications |

Other helpers: `statusline-setup` (Sonnet, for /statusline), `claudi-code-guide` (Haiku, for feature questions).

Explore and Plan skip CLAUDE.md files and the parent session's git status to keep research fast and inexpensive. Every other built-in and custom subagent loads both.

## Subagent Configuration

Subagent definitions are stored in different locations depending on scope:

| Location | Scope | Priority | How to create |
|---|---|---|---|
| Managed settings | Organization-wide | 1 (highest) | Deployed via managed settings |
| `--agents` CLI flag | Current session | 2 | Pass JSON when launching Claude Code |
| `.claude/agents/` | Current project | 3 | Interactive or manual |
| `~/.claude/agents/` | All your projects | 4 | Interactive or manual |
| Plugin's `agents/` directory | Where plugin is enabled | 5 (lowest) | Installed with plugins |

## Supported Frontmatter Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Tools the subagent can use. Inherits all if omitted |
| `disallowedTools` | No | Tools to deny, removed from inherited list |
| `model` | No | sonnet, opus, haiku, fable, full model ID, or inherit |
| `permissionMode` | No | default, acceptEdits, auto, dontAsk, bypassPermissions, or plan |
| `maxTurns` | No | Maximum number of agentic turns before stopping |
| `skills` | No | Skills to preload into the subagent's context at startup |
| `mcpServers` | No | MCP servers available to this subagent |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | user, project, or local - enables cross-session learning |
| `background` | No | true = always run as a background task |
| `effort` | No | Effort level when active (low, medium, high, xhigh, max) |
| `isolation` | No | worktree = run in a temporary git worktree |
| `color` | No | Display color in task list and transcript |
| `initialPrompt` | No | Auto-submitted as first user turn |

## Running Subagents: Foreground vs Background

**Foreground subagents** block the main conversation until complete. Permission prompts pass through to you as they come up.

**Background subagents** run concurrently while you continue working. They run with permissions already granted in the session and auto-deny any tool call that would otherwise prompt. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

Claude decides whether to run subagents in the foreground or background based on the task. You can also:
- Ask Claude to "run this in the background"
- Press `Ctrl+B` to background a running task

## Spawning Nested Subagents

As of Claude Code v2.1.172, a subagent can spawn its own subagents. Use this when a delegated task itself splits into parallel subtasks.

- **Foreground subagents**: can spawn at any depth. Each level blocks its parent until it returns.
- **Background subagents**: a background subagent at depth five does not receive the Agent tool and cannot spawn further. The limit is fixed and not configurable, and exists to prevent runaway concurrent trees.

## Preloading Skills into Subagents

Use the `skills` field to inject skill content into a subagent's context at startup. This gives the subagent domain knowledge without requiring it to discover and load skills during execution.

```yaml
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---
```

The full content of each listed skill is injected into the subagent's context at startup. This field controls which skills are preloaded, not which skills the subagent can access.

## Pre/Post Tool Hooks for Subagents

Subagents can define hooks that run during the subagent's lifecycle:

```yaml
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

The most common events for subagents:
- `PreToolUse`: Before the subagent uses a tool
- `PostToolUse`: After the subagent uses a tool
- `Stop`: When the subagent finishes (converted to `SubagentStop` at runtime)

## Relationship to Dynamic Workflows

Subagents are the **worker primitive** that dynamic workflows orchestrate. Per the official docs:
> "Dynamic workflows orchestrate many subagents from a script Claude writes and you can rerun."

The dynamic workflows runtime uses subagents to do the actual work, but coordinates them through a JavaScript script that holds the loop, branching, and intermediate results in script variables. Subagents spawned by a workflow always run in `acceptEdits` mode and inherit the session's tool allowlist.

## Common Patterns

**Isolate high-volume operations:** Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent's context while only the relevant summary returns to your main conversation.

**Run parallel research:** For independent investigations, spawn multiple subagents to work simultaneously.

**Chain subagents:** For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.
