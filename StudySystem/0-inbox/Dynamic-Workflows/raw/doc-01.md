# Dynamic Workflows - Official Documentation

> Source: https://code.claude.com/docs/en/workflows.md
> Title: Orchestrate subagents at scale with dynamic workflows

## Overview

A **dynamic workflow** is a JavaScript script that orchestrates subagents at scale. Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive.

**Availability:** Requires Claude Code v2.1.154 or later. Available on all paid plans (Pro, Max, Team, Enterprise), with Anthropic API access, and on Amazon Bedrock, Google Cloud Vertex AI, and Microsoft Foundry. On Pro, enable from the Dynamic workflows row in `/config`.

## When to Use a Workflow

Reach for a workflow when:
- A task needs more agents than one conversation can coordinate
- You want the orchestration codified as a script you can read and rerun
- Examples include: codebase-wide bug sweep, 500-file migration, research cross-checked across sources, plan drafted from multiple independent angles

## Comparison: Subagents vs Skills vs Agent Teams vs Workflows

| | Subagents | Skills | Agent teams | Workflows |
|---|---|---|---|---|
| What it is | A worker Claude spawns | Instructions Claude follows | A lead agent supervising peer sessions | A script the runtime executes |
| Who decides what runs next | Claude, turn by turn | Claude, following the prompt | The lead agent, turn by turn | The script |
| Where intermediate results live | Claude's context window | Claude's context window | A shared task list | Script variables |
| What's repeatable | The worker definition | The instructions | The team definition | The orchestration itself |
| Scale | A few delegated tasks per turn | Same as subagents | A handful of long-running peers | Dozens to hundreds of agents per run |
| Interruption | Restarts the turn | Restarts the turn | Teammates keep running | Resumable in the same session |

**Key insight:** A workflow moves the plan into code. With subagents, skills, and agent teams, Claude is the orchestrator. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer. Workflows can also apply repeatable quality patterns (adversarial review, multi-angle drafting).

## How to Trigger Workflows

### 1. Run a bundled workflow
The built-in `/deep-research` workflow fans out web searches, cross-checks sources, and synthesizes a cited report.

### 2. Ask for a workflow in your prompt
Use the keyword `ultracode` or ask in your own words (e.g., "use a workflow"). Before v2.1.160 the trigger keyword was `workflow`; natural-language requests work in both versions.

```
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

The keyword is highlighted in violet in the prompt input. Press `Option+W` (Mac) or `Alt+W` (Windows/Linux) to dismiss the highlight.

### 3. Let Claude decide with `/effort ultracode`
Ultracode combines `xhigh` reasoning effort with automatic workflow orchestration. With it on, Claude plans a workflow for each substantive task. Ultracode lasts for the current session and resets when you start a new one.

### 4. Run a saved workflow
Workflows you save become commands in `/` autocomplete.

## Bundled Workflows

| Command | What it does |
|---|---|
| `/deep-research <question>` | Fans out web searches, fetches and cross-checks sources, votes on claims, returns a cited report. Requires the WebSearch tool. |

## Running and Watching Workflows

### Watch a run with `/workflows`
The progress view shows each phase with agent counts, token totals, and elapsed time.

**Keyboard controls:**
- `↑` / `↓`: Select a phase or agent
- `Enter` or `→`: Drill into the selected phase
- `Esc`: Back out one level
- `j` / `k`: Scroll within the agent detail
- `p`: Pause or resume the run
- `x`: Stop the selected agent, or stop the whole workflow when focus is on the run
- `r`: Restart the selected running agent
- `s`: Save the run's script as a command

## Approval and Permissions

The per-run prompt shows the planned phases with options:
- **Yes, run it**: start the run
- **Yes, and don't ask again for `<name>` in `<path>`**: start, and skip for this project from now on
- **View raw script**: read the script before deciding
- **No**: cancel

`Ctrl+G` opens the script in your editor. `Tab` lets you adjust the prompt before the run starts.

| Permission mode | When you're prompted |
|---|---|
| Default, accept edits | Every run, unless you've selected "don't ask again" |
| Auto | First launch only; later launches start without prompting. Skipped entirely when ultracode is on |
| Bypass permissions, `claude -p`, Agent SDK | Never. The run starts immediately |

**Important:** The subagents the workflow spawns always run in `acceptEdits` mode and inherit your tool allowlist, regardless of your session's mode. File edits are auto-approved. Shell commands, web fetches, and MCP tools not in your allowlist can still prompt you mid-run.

## Saving Workflows for Reuse

Run `/workflows`, select a run, and press `s`. Save locations:
- `.claude/workflows/` in your project: shared with everyone who clones the repo
- `~/.claude/workflows/` in your home directory: available in every project, visible only to you

A saved workflow can accept input through the `args` parameter. The script reads it as a global named `args`.

Example: `> Run /triage-issues on issues 1024, 1025, and 1030`

## How a Workflow Runs

The workflow runtime executes the script in an isolated environment, separate from your conversation. Intermediate results stay in script variables instead of landing in Claude's context.

Every run writes its script to a file under `~/.claude/projects/`. The runtime tracks each agent's result, making a run resumable within the same session.

### Behavior and Limits

| Constraint | Why |
|---|---|
| No mid-run user input | Only agent permission prompts can pause a run. For sign-off between stages, run each stage as its own workflow |
| No direct filesystem or shell access from the workflow itself | Agents read, write, and run commands. The script coordinates the agents |
| Up to 16 concurrent agents | Bounds local resource use |
| 1,000 agents total per run | Prevents runaway loops |

## Cost Considerations

A workflow spawns many agents, so a single run can use meaningfully more tokens than working through the same task in conversation. Runs count toward your plan's usage and rate limits. To control cost:
- Check `/model` before a large run
- Ask Claude to use a smaller model for stages that don't need the strongest one
- Run the workflow on a small slice first

## Turning Workflows Off

To turn workflows off for yourself:
- Toggle Dynamic workflows off in `/config` (persists across sessions)
- Set `"disableWorkflows": true` in `~/.claude/settings.json`
- Set `CLAUDE_CODE_DISABLE_WORKFLOWS=1`

To turn workflows off for your whole organization, set `"disableWorkflows": true` in managed settings.

When workflows are disabled, the bundled workflow commands are unavailable, the `ultracode` keyword no longer triggers a run, and `ultracode` is removed from the `/effort` menu.

## Example: How a Saved Workflow Accepts Input

```text
> Run /triage-issues on issues 1024, 1025, and 1030
```

Claude passes the list as structured data, so the script can call array and object methods on `args` directly without parsing it first. If `args` is omitted, the global is `undefined` inside the script.
