# agentalign: Agent配置统一引擎

## Source

GitHub: Jonathangadeaharder/agentalign -- https://github.com/Jonathangadeaharder/agentalign

## Overview

Agentalign is a **Rust CLI tool** that implements a canonical store pattern for AI agent configuration. It uses a single `~/.agents/` directory as the source of truth and propagates configurations outward to each agent's native config location and format. The tool is MIT-licensed and written in Rust.

## Architecture

The codebase is organized into modular strategy patterns:

- **`src/mcp/`** -- Format-specific adapters for each agent that handle reading/writing in each agent's native dialect
- **`src/sync/`** -- Transaction engine with backup, rollback, and delta merger for bidirectional sync
- **`src/agents/`** -- Subagent definition sync (canonical markdown to per-agent formats)
- **`src/migration/`** -- Secret splitting and local fallback storage
- **`src/tracking/`** -- Keychain integration via the `keyring` crate
- **`src/rules/`** -- Splits AGENTS.md into path-scoped rule files for Cursor (.mdc) and Claude (.md)

## Sync Domains

Agentalign syncs four things from `~/.agents/`:

1. **MCP servers** -- Canonical `mcp_config.json` propagated to each agent
2. **Agent definitions** -- `agents/*.md` files converted to each agent's format
3. **Instruction files** -- Symlinks pointing to `~/.agents/AGENTS.md`
4. **Skills** -- Symlinked skill directories

## Supported Agents (8+)

| Agent | Config Path | Format |
|-------|-------------|--------|
| Claude Code | `~/.claude/.mcp.json` | JSON |
| Cursor | `~/.cursor/mcp.json` | JSON (is_cursor flag) |
| Gemini CLI | `~/.gemini/config/mcp_config.json` | JSON ($VAR placeholders) |
| Codex CLI | `~/.codex/config.toml` | TOML (restricted key chars) |
| OpenCode | `~/.config/opencode/opencode.json` | JSON |
| Antigravity | `~/.gemini/antigravity/mcp_config.json` | JSON |
| ZCode | `~/.zcode/cli/config.json` | JSON (nested mcp.servers) |
| Grok | `~/.grok/config.toml` | TOML (Codex-style) |

## CLI Commands

- **`migrate`** -- Scans existing agent configs into the canonical store
- **`sync`** -- Pushes canonical config to all agents
- **`agents list` / `agents sync`** -- Manage subagent definitions
- **`add` / `remove`** -- Add or remove MCP servers with propagate (supports `--no-sync` and `--dry-run`)
- **`restore`** -- Rolls back the last sync transaction (by agent, by UUID, or lists history)
- **`magic`** -- Toggles automatic bidirectional sync via a macOS LaunchAgent
- **`watch`** -- Runs a file watcher daemon (uses the `notify` crate)

## Key Features

### 1. Transactional Sync

Every write includes a backup and SHA-256 checksum. The `restore` command enables full rollback.

### 2. Delta Merger

Bidirectional sync detects adds, updates, and removals between agent configs and canonical store.

### 3. Secret Splitting

Sensitive fields (api_key, token, password) are extracted to the OS keychain (or `~/.agents/local.json` as fallback) and replaced with `${ENV_AGENTALIGN_SECRET_*}` placeholders.

### 4. Environment Interpolation

Normalizes `${VAR}`, `$VAR`, and `${env:VAR}` across agent dialects.

### 5. Instruction Symlink Healing

Agent files like CLAUDE.md, GEMINI.md, CODEX.md are symlinks to the canonical source, with automatic healing.

### 6. Magic Mode

Installs a macOS LaunchAgent for automatic sync on login with 500ms debounce.

### 7. Local Entries Protection

`~/.agents/local_entries.json` preserves user-added keys during sync.

### 8. Per-Agent Skip List

`~/.agents/agent_skip.json` prevents specific MCP servers from being pushed to particular agents.

## Comparison with Symlink-Only Approaches

Agentalign is architecturally more advanced than simple symlink tools. Rather than each agent reading from a shared file (which many agents support natively), agentalign **actively propagates** changes outward to each agent's native config location in the format that agent expects. This is more invasive but ensures:

- Bidirectional sync (change in any agent can be detected and propagated)
- Transactional safety with rollback
- Secret management (keychain integration)
- Format transformation between agents

## Status

The project is in active development with no published releases yet. Source can be built with `cargo build`.
