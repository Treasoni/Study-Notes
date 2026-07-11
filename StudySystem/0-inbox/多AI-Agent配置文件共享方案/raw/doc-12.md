# Codex vs Claude Code: 技能共享策略与实践

## Source

Compiled from: docs.kanaries.net/articles/codex-vs-claude-code-skills, developer.aliyun.com article 1717262 (HagiCode)

## Overview

This document covers practical strategies for sharing skills and configurations between Codex and Claude Code, including portable SKILL.md authoring, symlink-based sharing, and tool-specific feature isolation.

## Shared Foundation: The Agent Skills Open Standard

Both tools root their skill systems in the same open standard. Each skill is a directory containing a `SKILL.md` file with YAML frontmatter (at minimum `name` and `description`) plus Markdown instructions. Progressive loading is common to both -- metadata loads first, full instructions load only when the agent decides to act.

## Key Differences in Skill Systems

### Discovery Paths

| Scope | Codex | Claude Code |
|-------|-------|-------------|
| Project | `.agents/skills/` | `.claude/skills/` |
| User (all projects) | `$HOME/.agents/skills/` | `~/.claude/skills/` |
| Enterprise/Admin | `/etc/codex/skills/` | Enterprise managed settings |

### Activation UX

- **Codex**: Skills in a `/skills` list, referenced via `$` mentions. Selection is implicit based on `description`.
- **Claude Code**: Each skill becomes a slash command (`/skill-name`). Automatic invocation also triggers based on `description`.

### Claude-Specific Skill Extensions

Claude Code adds extended frontmatter not found in Codex:

- **`disable-model-invocation: true`** -- prevents automatic triggering
- **`allowed-tools`** -- restricts which tools the skill can use
- **`context: fork`** -- runs the skill in a separate subagent context
- **`` `command` ``** -- dynamic shell command preprocessing before prompt injection
- **`agent: Explore`** -- routes execution to a specialized subagent
- **`$ARGUMENTS` / `$ARGUMENTS[N]`** -- passes positional arguments to skills

### Codex-Specific Features

- **`agents/openai.yaml`** -- UI metadata and dependency declarations (e.g., MCP servers)
- **`[[skills.config]]`** -- TOML entries with `enabled = false` to disable without deleting
- **`$skill-creator`** -- Scaffolding helper for new skills
- **`$skill-installer`** -- Pulls skills from external sources

## Strategy 1: Symlinks from a Canonical Source

Maintain a single source-of-truth folder and symlink into each agent's discovery path.

**Project-level setup:**
```bash
# Codex
mkdir -p .agents/skills
ln -s ~/shared-agent-skills/code-review .agents/skills/code-review

# Claude Code
mkdir -p .claude/skills
ln -s ~/shared-agent-skills/code-review .claude/skills/code-review
```

**User-wide setup (all projects):**
```bash
# Codex
ln -s ~/shared-agent-skills/code-review $HOME/.agents/skills/code-review

# Claude Code
ln -s ~/shared-agent-skills/code-review ~/.claude/skills/code-review
```

### Symlink Support Caveats

- Codex **explicitly supports** symlinked skill folders and follows the symlink target during scanning
- Claude Code works with symlinks for direct invocation (`/skill-name`), but `/skills` listing **may not detect symlinked skills** in some versions
- Even if invisible in the list, the skill can still be invoked by name

## Strategy 2: Shared Git Repo with Automation Script

```
shared-agent-skills/
├── code-review/
│   ├── SKILL.md
│   └── references/
├── test-writer/
│   ├── SKILL.md
│   └── scripts/
├── setup-links.sh          # Automates symlinking
└── README.md
```

The `setup-links.sh` script iterates over each skill subdirectory and creates symlinks into both `$HOME/.agents/skills/` and `~/.claude/skills/`.

## Portable SKILL.md Template

For cross-agent compatibility, stick to spec-required fields:

```yaml
---
name: code-review
description: >
  Perform a structured code review for correctness, security,
  performance, and readability.
license: MIT
metadata:
  owner: platform-team
  version: "1.0.0"
---
```

Keep `name` matching parent directory, lowercase with hyphens, 1-64 characters. Use relative paths from the skill root for supporting files. Keep references one level deep.

## Isolating Tool-Specific Features

Layer rather than mix:

- **Codex-specific**: Add `agents/openai.yaml` alongside the skill. Other tools ignore it.
- **Claude-specific**: Place extended frontmatter (`allowed-tools`, `context: fork`, etc.) in a separate Claude-scoped skill or override file, not in the shared `SKILL.md`.

Neither tool chokes on unknown fields -- they simply ignore them. But separating features is cleaner practice.

## HagiCode Multi-Agent Architecture (Practical Production Example)

The HagiCode project demonstrates a production multi-agent setup using a unified Provider interface (`IAIProvider`) and factory pattern:

| Agent | Provider | Role |
|-------|----------|------|
| ClaudeCodeCli | Anthropic | Generate technical proposals |
| CodexCli | OpenAI/Zed | Execute precise code changes |
| CodebuddyCli | Zhipu GLM | Optimize documentation |
| IFlowCli | Zhipu GLM | Archive proposals |

Their **ACP protocol** (based on JSON-RPC 2.0) standardizes communication between agents, and task pipelines route work to the agent best suited for each stage.

## Best Practices Summary

1. Keep portable content (spec fields, relative references) in the shared canonical folder
2. Isolate tool-specific power features in their respective extension files
3. Use a shared Git repo with a `setup-links.sh` installer for team distribution
4. Version your skills by including a `version` field in metadata and tagging releases
5. Test symlinked skills by direct invocation name, not just by listing commands
