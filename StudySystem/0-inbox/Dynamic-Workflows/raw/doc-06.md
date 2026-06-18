# Claude Code Hooks - Official Documentation

> Source: https://code.claude.com/docs/en/hooks-guide.md
> Title: Automate actions with hooks

## Overview

Hooks are user-defined shell commands that execute at specific points in Claude Code's lifecycle. They provide deterministic control over Claude Code's behavior, ensuring certain actions always happen rather than relying on the LLM to choose to run them. Use hooks to enforce project rules, automate repetitive tasks, and integrate Claude Code with your existing tools.

For decisions that require judgment rather than deterministic rules, you can also use **prompt-based hooks** or **agent-based hooks** that use a Claude model to evaluate conditions.

**For other ways to extend Claude Code:**
- **Skills** - giving Claude additional instructions and executable commands
- **Subagents** - running tasks in isolated contexts
- **Plugins** - packaging extensions to share across projects
- **Dynamic Workflows** - orchestrating many subagents in the background

## Hook Events

| Event | When it fires |
|---|---|
| `SessionStart` | When a session begins or resumes |
| `Setup` | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode |
| `UserPromptSubmit` | When you submit a prompt, before Claude processes it |
| `UserPromptExpansion` | When a user-typed command expands into a prompt |
| `PreToolUse` | Before a tool call executes. Can block it |
| `PermissionRequest` | When a permission dialog appears |
| `PermissionDenied` | When a tool call is denied by the auto mode classifier |
| `PostToolUse` | After a tool call succeeds |
| `PostToolUseFailure` | After a tool call fails |
| `PostToolBatch` | After a full batch of parallel tool calls resolves |
| `Notification` | When Claude Code sends a notification |
| `MessageDisplay` | While assistant message text is displayed |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent finishes |
| `TaskCreated` | When a task is being created via `TaskCreate` |
| `TaskCompleted` | When a task is being marked as completed |
| `Stop` | When Claude finishes responding |
| `StopFailure` | When the turn ends due to an API error |
| `TeammateIdle` | When an agent team teammate is about to go idle |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded |
| `ConfigChange` | When a configuration file changes during a session |
| `CwdChanged` | When the working directory changes |
| `FileChanged` | When a watched file changes on disk |
| `WorktreeCreate` | When a worktree is being created |
| `WorktreeRemove` | When a worktree is being removed |
| `PreCompact` | Before context compaction |
| `PostCompact` | After context compaction completes |
| `Elicitation` | When an MCP server requests user input |
| `ElicitationResult` | After a user responds to an MCP elicitation |
| `SessionEnd` | When a session terminates |

## Hook Types

- `"type": "command"` - Runs a shell command (most common)
- `"type": "http"` - POST event data to a URL
- `"type": "mcp_tool"` - Call a tool on an already-connected MCP server
- `"type": "prompt"` - Single-turn LLM evaluation
- `"type": "agent"` - Multi-turn verification with tool access (experimental)

## Exit Codes

- **Exit 0**: the hook reports no objection and the action proceeds normally
- **Exit 2**: the action is blocked. Write a reason to stderr, and Claude receives it as feedback
- **Any other exit code**: the action proceeds. The transcript shows a `<hook name> hook error` notice

## Common Patterns

### Auto-format code after edits
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

### Block edits to protected files
Use `PreToolUse` hook to validate operations before they execute.

### Re-inject context after compaction
Use `SessionStart` hook with `compact` matcher.

### SubagentStart / SubagentStop Hooks
Configure hooks in `settings.json` that respond to subagent lifecycle events in the main session:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

## Prompt-Based Hooks

For decisions that require judgment rather than deterministic rules, use `type: "prompt"` hooks. Claude Code sends your prompt and the hook's input data to a Claude model (Haiku by default) to make the decision.

- `"ok": true`: the action proceeds
- `"ok": false`: what happens depends on the event:
  - `Stop` and `SubagentStop`: the `reason` is fed back to Claude so it keeps working
  - `PreToolUse`: the tool call is denied and the `reason` is returned to Claude
  - `PostToolUse`, `PostToolBatch`, `UserPromptSubmit`, `UserPromptExpansion`: the turn ends

## Agent-Based Hooks (Experimental)

When verification requires inspecting files or running commands, use `type: "agent"` hooks. Unlike prompt hooks which make a single LLM call, agent hooks spawn a subagent that can read files, search code, and use other tools to verify conditions before returning a decision.

Agent hooks use the same `"ok"` / `"reason"` response format as prompt hooks, with a longer default timeout of 60 seconds and up to 50 tool-use turns.

## Relationship to Dynamic Workflows

Hooks work with subagents and dynamic workflows in these ways:

1. **SubagentStart / SubagentStop events** fire whenever a subagent is spawned or finishes, including those spawned by dynamic workflows
2. **PostToolUse with continueOnBlock** - lifecycle hooks like `PostToolUse` support `continueOnBlock` for workflow control (per the changelog)
3. **Workflow-level event hooks** - subagents inside a workflow run in `acceptEdits` mode, so PreToolUse hooks can still enforce policy even in workflow contexts

The hooks system is the "deterministic control" layer for Claude Code. While dynamic workflows give Claude autonomy to coordinate many agents, hooks enforce rules that apply regardless of what Claude decides.

## Hook Configuration Locations

| Location | Scope | Shareable |
|---|---|---|
| `~/.claude/settings.json` | All your projects | No, local to your machine |
| `.claude/settings.json` | Single project | Yes, can be committed to the repo |
| `.claude/settings.local.json` | Single project | No, gitignored |
| Managed policy settings | Organization-wide | Yes, admin-controlled |
| Plugin `hooks/hooks.json` | When plugin is enabled | Yes, bundled with the plugin |
| Skill or agent frontmatter | While the skill or agent is active | Yes, defined in the component file |

To disable hooks, set `"disableAllHooks": true` in your settings file.
