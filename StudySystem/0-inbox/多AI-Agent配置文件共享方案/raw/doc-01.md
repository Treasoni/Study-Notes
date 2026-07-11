# Claude Code .claude 目录结构与配置详解

## Source

Compiled from: computingforgeeks.com, cloud.tencent.cn developer article, morphllm.com

## Overview

Claude Code uses a two-tier `.claude/` directory system for configuration: project-level (shared via Git) and global/user-level (personal preferences). The directory serves as the central configuration hub, managing project instructions, tool permissions, custom capabilities, session rules, and persistent memory.

## Dual-Scope Directory System

| Scope | Location | Git | Purpose |
|-------|----------|-----|---------|
| Project-level | `your-project/.claude/` | Commit | Team-shared config, coding standards, tool commands |
| Global/user-level | `~/.claude/` | Never commit | Personal preferences, global rules across all projects |

The environment variable `CLAUDE_CONFIG_DIR` can redirect all `~/.claude/` paths to a custom directory.

## Project-Level Directory Layout

```
your-project/
├── CLAUDE.md                   # Core project instructions (loaded every session)
├── CLAUDE.local.md             # Personal overrides (auto-gitignored)
├── .mcp.json                   # MCP server config (team-shared, project root)
├── .worktreeinclude            # Worktree file copy rules
└── .claude/
    ├── settings.json           # Permissions, hooks, model config
    ├── settings.local.json     # Personal overrides (gitignored)
    ├── rules/                  # Path-scoped modular rules
    │   ├── code-style.md
    │   ├── testing.md
    │   └── api-design.md
    ├── skills/                 # Reusable workflows (folder + SKILL.md)
    │   └── deploy/
    │       ├── SKILL.md
    │       └── deploy-config.md
    ├── commands/               # Single-file slash commands (merged into skills)
    ├── agents/                 # Sub-agent definitions (*.md with YAML frontmatter)
    │   └── code-reviewer.md
    ├── agent-memory/           # Persistent sub-agent memory
    └── output-styles/          # Custom output formatting
```

### Global `~/.claude/` Core Structure

```
~/.claude/
├── settings.json        # Global defaults
├── rules/               # Universal rules
├── skills/              # Reusable skills across projects
├── agents/              # Global sub-agents
├── plugins/             # Installed plugin data
├── history.jsonl        # Prompt history (up-arrow recall)
├── stats-cache.json     # Token usage statistics
└── projects/            # Session run data per project
```

## Key Configuration Files

### 1. CLAUDE.md -- The Foundation

- Loaded every session into Claude's system prompt
- Keep under 200 lines for best adherence
- Contains: build/test commands, architecture decisions, conventions, gotchas
- Survives compaction (`/compact` re-reads it from disk)
- Supports `@path/to/file` imports (up to 5 levels deep)
- Priority: `CLAUDE.local.md` > `CLAUDE.md` > `~/.claude/CLAUDE.md` > Managed Policy

### 2. settings.json -- Hard Enforcement

- Technically enforced by the client (unlike CLAUDE.md which is advisory)
- Controls: `permissions` (allow/ask/deny), `hooks`, `env`, `model`
- Permissions merge across scopes (not override), with `deny` having highest priority
- Supports hot-reload for most fields except `model` and `outputStyle`

### 3. rules/ -- Path-Scoped Modular Rules

- Files with `paths:` YAML frontmatter only load when Claude works in matching directories
- Files without `paths:` load on every session
- Saves context tokens by loading only relevant rules

### 4. skills/ -- Reusable Workflows

- Each skill is a folder with `SKILL.md` + supporting files
- Progressive disclosure: only name/description (~30-50 tokens) preloads; full content loads on demand
- Can be auto-invoked by Claude or user-triggered via `/skill-name`
- Extended features: `allowed-tools`, `context: fork` (subagent isolation), `$ARGUMENTS`

### 5. agents/ -- Sub-Agents

- Each file defines a sub-agent with its own system prompt, tool restrictions, and optional model
- Runs in an isolated context window
- Can have dedicated `memory: project | local | user` persistence

### 6. MCP -- External Tool Connections

- Project-level: `.mcp.json` in project root
- User-level: `~/.claude.json` or `claude mcp add --scope user`
- Tool Search feature reduces MCP token overhead by ~85% via on-demand loading

## Configuration Priority (Highest to Lowest)

1. Enterprise managed policy (cannot be overridden)
2. CLI flags (`--permission-mode`, `--settings`)
3. High-priority env vars
4. `.claude/settings.local.json` (project local)
5. `.claude/settings.json` (project)
6. `~/.claude/settings.json` (global)
7. System defaults

## Best Practices for Team Collaboration

1. **Start small**: Most users only need `CLAUDE.md` + `settings.json`
2. **Commit**: `.claude/settings.json`, `rules/`, `skills/`, `agents/` -- share with team
3. **Gitignore**: `CLAUDE.local.md`, `settings.local.json`, `agent-memory-local/`
4. **Keep CLAUDE.md under 200 lines**; split into `rules/` when it grows
5. **Use path-scoped rules** to save context tokens
6. **Put security-sensitive rules in `settings.json`** (enforced), not `CLAUDE.md` (advisory)
7. **Principle of least privilege** -- Grant only necessary tool permissions

## Data Management

- Auto-cleanup: data older than 30 days auto-deleted at startup
- All session data stored as plaintext (unencrypted)
- Use `cleanupPeriodDays` to adjust retention
- Use permission rules to block reading credential files
