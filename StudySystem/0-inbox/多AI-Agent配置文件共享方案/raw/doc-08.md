# SkillCaddy: 中心化技能库+按项目符号链接启用

## Source

GitHub: chenweil/skillcaddy -- https://github.com/chenweil/skillcaddy

## Overview

SkillCaddy is a local AI skills management tool that maintains a central library of skill sources and uses a **two-layer symlink strategy** to deliver them into projects on demand. It solves the problems of skill duplication across repos, version drift, outdated local copies, and lack of coordination between agent-specific skill directories.

## Problem Solved

Users of multiple AI coding agents across projects face:
- Skill duplication across repos
- Version drift between copies
- Outdated local copies
- No coordination between agent-specific skill directories (`.claude/skills/`, `.agents/skills/`, etc.)

SkillCaddy solves all of these with a single source of truth.

## Central Library: `~/AISkills/`

A single `~/AISkills/` directory aggregates skills from five source categories:

- **official/** -- Upstream/official skills
- **github/** -- Skills cloned from GitHub repos
- **personal/** -- User's own original skills
- **archived/** -- Retired skills
- **skills/** -- Skills bundled with the SkillCaddy repo itself

The first four directories are gitignored. Each skill lives in its own subdirectory and includes a `SKILL.md` file as the agent-facing contract.

## Two-Layer Symlink Strategy

```
~/AISkills/official/my-skill/SKILL.md
       |
       | Layer 1
       v
project/.agents/skills/my-skill -> ~/AISkills/official/my-skill
       |
       | Layer 2
       v
project/.claude/skills/my-skill -> ../../.agents/skills/my-skill
```

**Layer 1**: Symlink from the target project's `.agents/skills/<alias>` back to the skill's actual location in `~/AISkills/<source>/<skill>/`. The `.agents/skills` path is the cross-agent standard path recognized by all supported agents.

**Layer 2**: Claude Code gets its own `.claude/skills/<alias>` symlink pointing back to `../../.agents/skills/<alias>`, keeping Claude-specific visibility independent.

This means enabling a skill once makes it available across agents, while disabling only removes the symlink without touching the source.

## Supported Agents

| Agent | Project Path | User Path |
|-------|-------------|-----------|
| Claude Code | `.claude/skills/` | `~/.claude/skills` |
| OpenCode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.claude/skills`, `~/.agents/skills` |
| Codex | `.agents/skills/` | `~/.agents/skills` |
| Pi | `.pi/skills/`, `.agents/skills/` | `~/.pi/agent/...`, `~/.agents/skills` |

## Installation & Setup

**Requirements**: Node.js >= 20.

```bash
# Clone and start web manager
git clone https://github.com/chenweil/skillcaddy.git
cd skillcaddy
npm start
# Web UI at http://127.0.0.1:4173

# Terminal UI (TUI) also available
npm run tui -- /path/to/project

# Make manager skill globally available to AI agents
npm run install:manager
npm run check:manager
```

## Key Features

- **Web UI** for managing skill enablement across projects
- **Terminal UI (TUI)** with full keyboard-driven interface
- Actions: enabling/disabling skills, syncing Claude Code, editing metadata, viewing diagnostics, batch-pulling GitHub sources
- **Recommendation system**: suggests skills based on context (empty library vs. development workflow)
- **Metadata**: human-facing notes, tags, auto-enable flags stored in sidecar `.skillcaddy/metadata/` files
- Cross-platform: macOS and Linux fully supported; Windows requires Developer Mode or Administrator
