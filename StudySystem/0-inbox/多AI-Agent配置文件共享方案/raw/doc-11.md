# AgentSync: 快速可移植的Agent配置同步CLI

## Source

GitHub: dallay/agentsync -- https://github.com/dallay/agentsync

## Overview

AgentSync is a fast, portable CLI tool for synchronizing AI agent configurations and MCP servers across multiple AI coding assistants using symbolic links. Written in Rust, distributed as a single static binary with no runtime dependencies. Also available as an npm package. MIT-licensed.

## Core Idea

**Symlinks over copies** -- any change propagates instantly. Rather than maintaining separate config files for each AI tool, users define everything once in a canonical `.agents/` directory. AgentSync then creates symbolic links pointing each tool's expected config location back to that single source of truth.

## Workflow

1. **`agentsync init`** -- Creates or migrates configuration into `.agents/agentsync.toml`
2. **`agentsync apply`** -- Creates or refreshes all symlinks
3. **`agentsync status`** -- Inspects the sync state
4. **`agentsync skill ...`** -- Manages installed skills

## Supported Agents

| Tool | Instructions File | Commands | Skills |
|------|------------------|----------|--------|
| Claude Code | `CLAUDE.md` | `.claude/commands/` | `.claude/skills/` |
| GitHub Copilot | `.github/copilot-instructions.md` | -- | -- |
| Gemini CLI | `GEMINI.md` | `.gemini/commands/` | `.gemini/skills/` |
| Cursor | `.cursor/rules/agentsync.mdc` | -- | `.cursor/skills/` |
| VS Code | -- | -- | -- |
| OpenCode | `AGENTS.md` | `.opencode/command/` | `.opencode/skills/` |
| OpenAI Codex | `AGENTS.md` | -- | `.codex/skills/` |

## Configuration Format (`.agents/agentsync.toml`)

```toml
source_dir = ".agents"
compress_agents_md = true
default_agents = ["claude", "copilot"]

[gitignore]
enabled = true
marker = "AgentSync managed"
entries = ["agents/mcp.json", "agents/agents.json"]

[agents.claude]
enabled = true
description = "Anthropic Claude Code"

[agents.claude.targets]
  [agents.claude.targets.instructions]
  source = "AGENTS.md"
  destination = "CLAUDE.md"
  type = "symlink"

  [agents.claude.targets.skills]
  source = "skills"
  destination = ".claude/skills"
  type = "symlink-contents"
  pattern = "*/SKILL.md"
```

### Target Types

- **`symlink`**: For a single file -- creates `destination -> source` symlink
- **`symlink-contents`**: For directory contents -- creates per-item symlinks filtered by glob `pattern`

## CLI Commands

| Command | Purpose |
|---------|---------|
| `agentsync init` | Create fresh configuration |
| `agentsync init --wizard` | Interactive migration from existing files |
| `agentsync apply` | Create/refresh symlinks from config |
| `agentsync apply --clean` | Clean existing symlinks before applying |
| `agentsync apply --dry-run` | Preview changes without making them |
| `agentsync apply --agents claude,copilot` | Filter by specific agents |
| `agentsync apply --no-gitignore` | Skip gitignore reconciliation |
| `agentsync clean` | Remove all managed symlinks |
| `agentsync status` | Show managed symlink state |
| `agentsync status --json` | Machine-readable JSON output |
| `agentsync doctor` | Run diagnostic and health check |
| `agentsync skill install <id>` | Install a skill from curated collection |
| `agentsync skill update <id>` | Update an installed skill |
| `agentsync skill uninstall <id>` | Remove a skill |

## Key Features

- **TOML-based** configuration (compatible with Codex's format)
- Automatic **`.gitignore` management** for canonical files
- Safe backups before replacing files
- Cross-platform (Linux, macOS, Windows)
- **CI-friendly** -- non-interactive, exit codes indicate status
- Curated skill collection at [dallay/agents-skills](https://github.com/dallay/agents-skills)

## Installation

```bash
# npm
npm install -g @dallay/agentsync
# Cargo
cargo install agentsync
# Pre-built binaries from GitHub Releases
```
