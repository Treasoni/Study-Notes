# ai-config (azat-io): 统一配置安装管理器

## Source

GitHub: azat-io/ai-config -- https://github.com/azat-io/ai-config

## Overview

A unified configuration manager for AI coding assistants that synchronizes settings across Claude Code, Codex, Gemini CLI, and OpenCode. It deploys consistent instructions, commands, skills, and MCP integrations through a single `npx` installer. The project exists because "every agent uses a different format and directory layout" and keeping them in sync manually is slow and error-prone.

## Supported Agents & Feature Compatibility

| Agent | Instructions | Commands | Skills | Subagents | Hooks | MCP |
|-------|-------------|----------|--------|-----------|-------|-----|
| Claude Code | Yes | Yes | Yes | Yes | Yes | Yes |
| Codex | Yes | No | Yes | Yes | No | Yes |
| Gemini CLI | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenCode | Yes | Yes | Yes | Yes | No | Yes |

## Installer

```bash
npx @azat-io/ai-config
```

The installer interactively prompts for:
1. Which agents to install
2. Install scope (project or home)
3. Which MCP servers to install

**Requirements:** Node.js v22+, `gh` CLI (for GitHub operations), `uv` (for `uvx`, only if using built-in MCP servers).

## Install Scopes

### Project (local) -- Creates dot-folders in the project directory:

| Agent | Files Created |
|-------|--------------|
| Claude Code | `.claude/commands/`, `.claude/agents/`, `.claude/skills/`, `.claude/hooks/`, `.claude/settings.json`, `CLAUDE.md` |
| Codex | `.codex/agents/*.toml`, `.codex/skills/`, `.codex/config.toml`, `AGENTS.md` |
| Gemini CLI | `.gemini/commands/`, `.gemini/agents/`, `.gemini/skills/`, `.gemini/hooks/`, `.gemini/settings.json`, `GEMINI.md` |
| OpenCode | `.opencode/commands/`, `.opencode/agents/`, `.opencode/skill/`, `opencode.json`, `AGENTS.md` |

### Home (global) -- Uses user-level config directories:

`~/.claude/`, `~/.codex/`, `~/.gemini/`, `~/.config/opencode/`

## Configuration Sources

Sources reside in the repository and are copied into each agent's config:

- **`instructions/global.md`** -- Shared agent instructions
- **`commands/`** -- Slash commands: `/blueprint`, `/code-review`, `/commit`, `/discovery`, `/docs`, `/implement`, `/refactor`, `/research`, `/test`
- **`agents/`** -- Subagent definitions: code-reviewer, documentation-writer, explorer, implementer, test-writer
- **`skills/`** -- Reusable techniques: blueprinting, creating-skills, creating-subagents, discovering, implementing, refactoring, researching
- **`hooks/`** -- Lifecycle hooks (for agents that support them)
- **`settings/mcp.ts`** -- MCP server configuration for Fetch and Sequential Thinking

## Key Design Decisions

- **Copy-based, not symlink-based**: Unlike other tools, ai-config copies files into each agent's directory rather than symlinking. This means changes to the source don't automatically propagate -- you need to re-run the installer.
- **Agent-specific format mapping**: The tool knows how to translate the same source content into each agent's expected format (e.g., Markdown agents for Claude, TOML for Codex)
- **Interactive installer**: Guides users through setup with prompts for which agents and features to install
- **Two scopes**: Project-local (per-repo) or global (home directory), giving flexibility for shared vs. personal setup
