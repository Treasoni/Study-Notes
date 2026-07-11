# ai-agent-rules: 带合并管线的配置管理方案

## Source

GitHub: wpfleger96/ai-agent-rules -- https://github.com/wpfleger96/ai-agent-rules

## Overview

This tool manages AI agent configurations through symlinks with a multi-stage merge pipeline. It keeps all configs in one git-tracked location and supports profile inheritance, user overrides, and cross-machine sync. Written in Python, distributed via PyPI.

## Supported Agents

| Agent | Config Dir | Skills Dir |
|-------|-----------|------------|
| Amp | `~/.config/amp/` | `~/.config/agents/skills/` |
| Claude Code | `~/.claude/` | `~/.claude/skills/` |
| Codex CLI | `~/.codex/` | `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/` | via `~/.agents/skills/` |
| Goose | `~/.config/goose/` | `~/.config/goose/skills/` |

A "Shared" category also manages `AGENTS.md` and skills across agents.

## Merge Pipeline

At install time, settings are assembled through a multi-stage pipeline:

1. **Base settings** -- loaded from the git-tracked source (e.g., `src/ai_rules/config/claude/settings.json`)
2. **Profile overrides** -- applied if a profile is active
3. **User overrides** -- from `~/.ai-agent-rules-config.yaml` (local, machine-specific)
4. **Preserved fields** -- merged from cache, protecting agent-managed fields (e.g., `enabledPlugins`, `hooks`, `extensions`)
5. **Cached** -- stored in `~/.ai-agent-rules/cache/<agent>/`
6. **Symlinked** -- to the agent's config directory

## Profile Inheritance

Three built-in profiles with inheritance chain: **default -> personal -> work**

A profile can `extends` another, accumulating settings parent-first. Key profile fields:

- `settings_overrides` -- Agent-specific setting overrides
- `plugins` -- Plugin lists
- `marketplaces` -- Marketplace registrations
- `agents_md_file` -- Custom AGENTS.md file path
- `exclude_symlinks` -- Glob patterns for symlink exclusion
- `mcp_overrides` -- MCP server overrides

The active profile persists in `~/.ai-agent-rules/state.yaml`.

## Symlink Strategy

The tool installs symlinks from the git-tracked source (under `src/ai_rules/config/`) to each agent's expected config directory. Users can exclude specific symlink targets via glob patterns. The `status` command checks symlink health with indicators (checkmark, cross, warning, circle) and shows diffs.

## Cross-Machine Sync

Achieved by:

- **Git-tracking** all config files in the source repo, then cloning across machines
- Using machine-specific **user overrides** in `~/.ai-agent-rules-config.yaml` for per-machine values (e.g., different Claude models on personal vs. work laptops)
- Profiles enable context switching between environments
- Local config always wins in the priority hierarchy

## Setup

**Requirements:** Python 3.10+ and `uv`.

```bash
# Install from PyPI (recommended)
uvx --from ai-agent-rules ai-agent-rules setup

# Development from GitHub
uvx --from ai-agent-rules ai-agent-rules setup --github
```

## Key Design Decisions

- **Merge pipeline over raw symlinks**: The tool doesn't just create symlinks -- it merges settings from multiple sources (base + profile + user) before writing, which allows different machines/users to have different overrides while sharing a common base
- **Profile inheritance**: Enables context-dependent configuration (work vs. personal)
- **Preserved fields**: Agent-managed fields are protected from being overwritten during sync
- **Git-tracked source**: All config changes are version-controlled, enabling cross-machine sync
