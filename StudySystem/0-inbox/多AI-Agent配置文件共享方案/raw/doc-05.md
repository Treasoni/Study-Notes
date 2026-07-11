# ai-agent-config: 基于符号链接的配置文件共享方案

## Source

GitHub: casoon/ai-agent-config -- https://github.com/casoon/ai-agent-config

## Overview

This project implements a **single-source-of-truth via symlinks** approach for sharing AI agent configuration between Claude Code and Codex CLI. Files live in one neutral directory tree, and install scripts create symlinks from each tool's expected config location back into that tree. Editing a file in the repo instantly updates the live config for all connected tools -- no copying or synchronization step is needed.

## File Layout

```
./
├── GLOBAL.md                    # Global instructions -> CLAUDE.md / AGENTS.md
├── agents/                      # Subagent sources (Markdown + YAML frontmatter)
├── codex-agents/                # Generated from agents/ -- do not edit by hand
├── skills/                      # Reusable skills (one folder with SKILL.md each)
├── codex-config.example.toml    # Codex baseline profiles (tracked in git)
├── codex-config.toml            # Live Codex config (git-ignored, seeded from example)
├── scripts/
│   └── render-codex-agents.py   # Converts Markdown agents to Codex TOML format
├── .githooks/
│   └── pre-commit               # Regenerates codex-agents/ on commit
└── install/
    ├── link-claude.sh
    ├── link-codex.sh
    └── link-all.sh
```

## Symlink Map

| Source (in repo) | Claude Target | Codex Target |
|---|---|---|
| `GLOBAL.md` | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| `agents/` | `~/.claude/agents` | -- (uses codex-agents/) |
| `codex-agents/` | -- | `~/.codex/agents` |
| `skills/` | `~/.claude/skills` | `~/.codex/skills` |
| `codex-config.toml` | -- | `~/.codex/config.toml` |

## Key Design Decisions

### Different Filenames, Same File

The same source file maps to different filenames under each tool's config directory. For example, `GLOBAL.md` becomes `~/.claude/CLAUDE.md` for Claude but `~/.codex/AGENTS.md` for Codex -- each tool reads the file name it expects, but both point back to the same underlying file.

### Format Transformation for Subagents

Agent prompts are authored in Markdown (`agents/*.md`), which Claude consumes directly. For Codex, a pre-commit hook runs `python3 scripts/render-codex-agents.py` to generate TOML files in `codex-agents/`, which then symlink to `~/.codex/agents`. This keeps Markdown as the single place to edit agent prompts while serving both tools in their native formats.

### Skills Shared Identically

Skills are the easiest to share -- `skills/` symlinks to both `~/.claude/skills` and `~/.codex/skills` without any transformation, since both agents use the same `SKILL.md` + directory format.

## Setup

```bash
git clone <repo>
./install/link-all.sh
git config core.hooksPath .githooks
```

Existing non-symlink targets are backed up as `<path>.bak` before symlink creation. Existing symlinks are replaced silently.

## Security & Privacy

- Machine-specific or secret-bearing files are git-ignored
- The live `codex-config.toml` is seeded from a tracked `codex-config.example.toml`
- Personal preferences go into a designated "private section" of `GLOBAL.md`

## Pros and Cons

**Pros:**
- Single source of truth; edit once, update everywhere
- Uses OS-native symlinks (no runtime daemon needed)
- Supports format transformation for agent-specific requirements
- Git-tracked for version control and team sharing

**Cons:**
- Only supports Claude Code and Codex (not CodeBuddy, Gemini, etc.)
- Requires manual pre-commit hook setup for Codex agent transformation
- Per-machine setup needed (clone repo + run install script)
- No built-in backup/rollback mechanism
