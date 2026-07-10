# Codex CLI Hooks & Plugin Marketplace (from Community Resources)

Source: https://github.com/justrach/codedb/blob/main/docs/hooks-labs.md, fcakyon/claude-codex-settings
Fetched: 2026-07-11

## Hook Configuration Details

### Enabling Hooks

In `~/.codex/config.toml`:
```toml
[features]
codex_hooks = true
```

### Hook Discovery (Detailed Order)

Codex looks for hooks adjacent to active config layers:
1. `~/.codex/hooks.json` — user global
2. `~/.codex/config.toml` — user global inline hooks
3. `<repo>/.codex/hooks.json` — project level
4. `<repo>/.codex/config.toml` — project level inline hooks

**Important:** Project-local hooks load only when the project `.codex/` layer is trusted.

**Prefer one representation per layer** — don't mix hooks.json and inline `[hooks]` in the same layer.

### Complete hooks.json Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__codedb__codedb_remote",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/env bash \"$(git rev-parse --show-toplevel)/.codex/hooks/codedb_remote_guard.sh\"",
            "timeout": 5,
            "statusMessage": "Checking codedb_remote request"
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
            "command": "npx tsc --noEmit",
            "timeout": 30,
            "statusMessage": "Type checking..."
          }
        ]
      }
    ]
  }
}
```

### Guard Script Pattern

The guard script reads tool input from stdin via `$(cat)`, parses JSON with `jq`, and decides on denial:

```bash
#!/bin/bash
input=$(cat)
# To deny an action:
echo '{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Reason here"
  }
}'
# No output means permit
```

### Hook Events Summary

| Event | Purpose |
|-------|---------|
| PreToolUse | Block or ask before a tool call |
| PostToolUse | Summarize or log MCP output after it returns |
| PermissionRequest | Decide approval prompts |
| UserPromptSubmit | Add repo-specific context before prompt reaches model |
| Stop | Continue a turn when validation is still missing |

## Plugin Marketplace Installation

For community configuration collections like fcakyon/claude-codex-settings:

1. Clone the repo locally
2. Ensure `.agents/plugins/marketplace.json` exists
3. Restart Codex if it was open when marketplace file changed
4. In Codex, open `/plugins` -> select marketplace -> install desired plugins

## Notable: Codex Hook Limitations vs Claude Code

- Codex, Cursor, and Gemini CLI don't yet expose a comparable summary hook (for PreCompact events)
- The intelligent-compact plugin is Claude Code only
- Hooks execute arbitrary commands with your user permissions — do not use as the only security boundary
