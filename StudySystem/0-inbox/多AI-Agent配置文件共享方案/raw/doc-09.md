# swarmskills: 跨45+Agent技能管理工具

## Source

himcp.ai/server/swarmskills, npm package swarmskills

## Overview

swarmskills is both a CLI and an MCP server for managing skills across approximately 45 code-oriented CLI agents. It uses a standardized `SKILL.md` + YAML-frontmatter format and knows where each agent expects to find its skills. MIT-licensed by SwarmClaw AI, distributed as an npm package.

## Supported Agents (~45 built-in)

Includes: Claude Code, Cursor, Codex, Goose, Gemini CLI, OpenCode, GitHub Copilot, Windsurf, OpenHands, Qwen Code, Cline, Continue, Crush, iFlow, Junie, Kiro, Kode, Roo Code, Kilo Code, Antigravity, Amp, Droid, Firebender, Replit, Warp, Augment, Bob, **CodeBuddy**, Command Code, Cortex Code, Deep Agents, Kimi, MCPJam, Mistral Vibe, OpenClaw, TRAE, TRAE CN, Mux, Neovate, Pi, Pochi, Qoder, Zencoder, AdaL, and Hermes.

Users can also register custom agents via `swarmskills tools add-custom`.

## MCP Server (18 Tools)

Configured in any MCP-aware client, runs via `npx -y swarmskills-mcp`. HTTP transport variant: `swarmskills-mcp-http --port 4100`.

| Category | Tools |
|----------|-------|
| **Skill discovery** | `list_skills`, `show_skill`, `search_skills` |
| **Tool/agent registry** | `list_tools`, `detect_tool`, `add_custom_tool`, `remove_custom_tool` |
| **Default tool management** | `get_default_tool`, `set_default_tool`, `clear_default_tool` |
| **Skill sync** | `sync_skill` |
| **Plugin management** | `list_plugins`, `enable_plugin`, `disable_plugin`, `install_plugin`, `uninstall_plugin` |
| **Marketplace management** | `list_marketplaces`, `list_marketplace_catalog`, `add_marketplace`, `remove_marketplace`, `refresh_marketplace` |

## Skill Management

**Discover:** List and fuzzy-search skills for any single tool or across all detected tools simultaneously.

**Install/Enable:** Full lifecycle management for Claude Code plugins -- install, uninstall, enable, disable. Register new marketplaces (`marketplace add owner/repo`) and refresh them via `git pull`.

**Sync:** Mirror skills between tools using symlinks (default) or file copies, with optional force-overwrite. Supports syncing a single skill or `--all` skills from one tool to others.

## Key Design Decisions

- **Multi-agent awareness**: Detects which of the ~45 agents are actually installed on the machine
- **Default tool resolution**: Precedence: explicit `--tool=` flag -> `SWARMSKILLS_DEFAULT_TOOL` env var -> config file -> falls back to `claude-code`
- **Restart caveat**: Mutating operations return `requiresRestart: true` because most CLI agents read their skill state at session start
- **State location**: `~/.claude/skills/`, `~/.claude/plugins/`, `~/.claude/settings.json`, and `~/.config/swarmskills/config.json`
- **Atomic writes**: All writes go to `.tmp` then rename
- **XDG compliance**: `.config/...` paths honor `XDG_CONFIG_HOME` when set

## Setup

```bash
npm install -g swarmskills
```
Requires Node.js 20+.

## Agent-Specific Path Support

swarmskills understands each agent's skill discovery paths, including:
- `.claude/skills/`, `.agents/skills/`, `.opencode/skills/`
- Agent-specific global paths like `~/.claude/skills`, `~/.agents/skills`, `~/.config/.../skills/`

This makes it a powerful cross-agent synchronization tool since it knows exactly where each agent looks for skills.
