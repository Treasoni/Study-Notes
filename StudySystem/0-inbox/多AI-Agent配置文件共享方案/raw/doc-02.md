# Codex CLI 配置结构与设置详解

## Source

Compiled from: composio.dev, developer.aliyun.com, GitHub (ogmios2/claude-code-codex-mcp), nylas.com docs

## Overview

Codex CLI uses TOML format for its configuration, stored in `.codex/config.toml`. It supports both global (`~/.codex/config.toml`) and per-project (`./.codex/config.toml`) configuration files, with a multi-layered priority system.

## Configuration File: config.toml

Projects must be marked as `trusted` for local `.codex/` config to be loaded:

```toml
[projects."/absolute/path/to/your/project"]
trust_level = "trusted"
```

## Top-Level Runtime Settings

```toml
# Approval & sandboxing
approval_policy = "on-request"     # on-request | never | on-failure | untrusted
sandbox_mode = "workspace-write"   # read-only | workspace-write | danger-full-access
web_search = "live"                # live | cached

# Multi-agent collaboration
[features]
multi_agent = true
hooks = true

# Persistent instructions (appended to every prompt)
persistent_instructions = "Follow project AGENTS.md guidelines."

# Fallback filenames for project instructions
project_doc_fallback_filenames = ["AGENTS.md", "CLAUDE.md"]
project_doc_max_bytes = 32768
```

## MCP Server Configuration

MCP servers are defined under `[mcp_servers.*]` sections with two transport types:

### STDIO-based servers
```toml
[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
startup_timeout_sec = 30
```

### HTTP/Streamable HTTP servers
```toml
[mcp_servers.vaadin]
url = "https://mcp.vaadin.com/docs"
```

### Bearer token auth (via env var)
```toml
[mcp_servers.nylas]
url = "https://mcp.us.nylas.com"
bearer_token_env_var = "NYLAS_API_KEY"
```

**Key options per server:**

| Option | Default | Description |
|--------|---------|-------------|
| `startup_timeout_sec` | 10 | Time to wait for initial connection |
| `tool_timeout_sec` | 60 | Max time per tool call |
| `enabled` | true | Toggle server on/off |
| `env` | -- | Inline env vars: `env = { "KEY" = "val" }` |

## Subagents

Codex stores subagents as individual TOML files in `.codex/agents/`:

```toml
# .codex/agents/reviewer.toml
name = "reviewer"
description = "Reviews diffs for correctness and style"
developer_instructions = """
Review the diff for correctness and style. Cite file and line for each issue.
"""
```

Subagents are configured in `config.toml`:

```toml
[agents]
max_threads = 6
max_depth = 1

[agents.explorer]
description = "Read-only codebase explorer"
config_file = "agents/explorer.toml"

[agents.reviewer]
description = "PR reviewer focused on correctness, security, and missing tests."
config_file = "agents/reviewer.toml"
```

## Hooks

Codex supports hooks via `[[hooks.*]]` in `config.toml`:

```toml
[[hooks.PreToolUse]]
matcher = "^Bash$"
  [[hooks.PreToolUse.hooks]]
  type = "command"
  command = "$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use.sh"
```

Supported events: `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, `PreCompact`, `PostCompact`.

## Profiles (switch with `codex -p <name>`)

```toml
[profiles.strict]
approval_policy = "on-request"
sandbox_mode = "read-only"
web_search = "cached"

[profiles.yolo]
approval_policy = "never"
sandbox_mode = "workspace-write"
web_search = "live"
```

## CLI Commands for MCP Management

```bash
# Add an HTTP/OAuth MCP server
codex mcp login <server-name>

# Add a stdio-based MCP server
codex mcp add <server-name> --env VAR1=VALUE1 -- <stdio-server-command>

# List active MCP servers (inside a session)
/mcp
```

## Migration from Claude Code (Codex 0.140+)

Codex includes a built-in importer:

```bash
codex          # start a session
/import        # runs the Claude Code -> Codex migration wizard
```

### Key Mappings

| Claude Code | Codex Equivalent |
|---|---|
| `CLAUDE.md` | `AGENTS.md` (or use `project_doc_fallback_filenames`) |
| `.mcp.json` (JSON) | `[mcp_servers.*]` in `config.toml` |
| `.claude/agents/*.md` | `.codex/agents/*.toml` |
| `.claude/skills/` | `[[skills.config]]` in config.toml |
| `settings.json` | `config.toml` + `profiles` |
| `permissions.allow/ask/deny` | `approval_policy` + `sandbox_mode` |

## Skill Discovery Paths

| Scope | Codex Path |
|---|---|
| Project | `.agents/skills/` |
| User (all projects) | `$HOME/.agents/skills/` |
| Enterprise/Admin | `/etc/codex/skills/` |

## Symlink Support

Codex explicitly supports symlinked skill folders and follows the symlink target during scanning. This is important for cross-agent configuration sharing.
