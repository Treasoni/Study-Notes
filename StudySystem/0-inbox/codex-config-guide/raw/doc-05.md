# Codex CLI Hooks Configuration

Source: https://github.com/liewcf/codex-notify-macos, https://github.com/justrach/codedb/blob/main/docs/hooks-labs.md, and community resources
Fetched: 2026-07-11

## Overview

Hooks are trigger-based automations that fire on specific events in the Codex lifecycle. They allow user-defined shell scripts to inject into the agentic loop for logging, security scanning, validation, and custom automation.

## Enabling Hooks

In `~/.codex/config.toml`:
```toml
[features]
hooks = true
# or
codex_hooks = true
```

As of Codex 0.129, hooks require manual review and activation before they run.

## Hook Discovery Locations

Codex loads hooks from files adjacent to active config layers (in order):
1. `~/.codex/hooks.json`
2. `~/.codex/config.toml` (inline `[hooks]` tables)
3. `<project-root>/.codex/hooks.json`
4. `<project-root>/.codex/config.toml`

Project-local hooks load only when the project `.codex/` layer is trusted. Matching hooks from multiple files all run.

If a layer has both `hooks.json` and inline `[hooks]`, Codex loads both and warns — prefer one representation per layer.

## Supported Hook Events

| Event | Trigger | Use Case |
|-------|---------|----------|
| `SessionStart` | When a session begins | Inject context, env setup |
| `SessionEnd` | When a session ends | Cleanup |
| `UserPromptSubmit` | When user sends a message | Inject project context, secret detection |
| `PreToolUse` | Before a tool executes | Validation, guardrails, deny dangerous commands |
| `PostToolUse` | After a tool finishes | Formatting, type checking, logging |
| `PostToolUseFailure` | After a tool fails | Error handling |
| `Stop` | When Codex finishes responding | Save session memory, check for leftovers |
| `Notification` | Permission requests | Auto-approval strategy |
| `PreCompact` | Before context compaction | Preserve priorities |
| `SubagentStart` / `SubagentStop` | Subagent lifecycle | Subagent monitoring |

## hooks.json Format

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__codedb__codedb_remote",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/env bash \"/path/to/hooks/guard.sh\"",
            "timeout": 5,
            "statusMessage": "Checking request"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit && .ts/.tsx",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "grep -rn 'console.log' --include='*.ts' ."
          }
        ]
      }
    ]
  }
}
```

## Inline TOML Hook Format

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"

[[hooks.PreToolUse.hooks]]
type = "command"
command = '/usr/bin/python3 "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use_policy.py"'
timeout = 30
statusMessage = "Checking Bash command"
```

## Hook Script Contract

- Read JSON from **stdin**
- Write JSON to **stdout**
- Exit code `0` = continue
- Exit code `2` = block the action (for `PreToolUse` guardrails)

### Guard Script Example

```bash
#!/bin/bash
input=$(cat)
# Parse with jq, check conditions
# To deny:
echo '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Reason for denial"
  }
}'
# No output = permit
```

## Notify Hook (config.toml)

```toml
notify = ["/bin/bash", "/Users/<you>/.codex/notify-macos.sh"]
```

The notify script receives a JSON argument with fields: `type`, `thread-id`, `turn-id`, `cwd`, `input-messages`, `last-assistant-message`.

## Common Hook Use Cases

### Security Guardrails
- Block `git push --force`
- Block `rm -rf /`, `git reset --hard`
- Warn on push to main/master
- Secret scanning before commits

### Code Quality
- Auto-format with prettier after edits
- Run TypeScript compiler after edits
- Check for `console.log` remnants
- Run linters

### Workflow Automation
- Enforce running inside tmux for long commands
- Open editor for review before git push
- Branch SessionStart on `source` (`startup | resume | clear`) to skip heavy context on clear

## Limitations

- Codex's hook system is not yet on par with Claude Code for summary hooks
- Codex runs in a sandbox by default, which can interfere with hooks needing filesystem access
- Hooks support is still considered experimental
- Do not use hooks as the only security boundary — hooks execute arbitrary commands with your user permissions
