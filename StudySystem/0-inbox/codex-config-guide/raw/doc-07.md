# Codex CLI Project Instructions (AGENTS.md / Rules Configuration)

Source: Various official and community resources
Fetched: 2026-07-11

## Overview

Codex CLI reads **`AGENTS.md`** as its primary project instructions file (the equivalent of Claude Code's `CLAUDE.md`). It can be configured to also read `CLAUDE.md` or other filenames as fallbacks.

## AGENTS.md Format

Create at project root:
```markdown
# Project Guidelines
- Use TypeScript with strict mode
- Follow the existing API pattern in /src/api
- Write tests in /tests directory
```

To scaffold an AGENTS.md, run `/init` inside Codex.

## File Discovery Priority (highest to lowest)

1. `.codex/AGENTS.override.md` (project-level override)
2. `.codex/AGENTS.md` (project-level)
3. `~/.codex/AGENTS.override.md` (global override)
4. `~/.codex/AGENTS.md` (global default)
5. Subdirectory `AGENTS.md` files (merged bottom-up)

**Merge rule:** At most one file per directory, concatenated from root downward.

## Configuration Precedence Complete Chain

1. CLI flags (`-c key=value`) — highest priority
2. Profile values
3. Project config (`.codex/config.toml`) — trusted projects only
4. User config (`~/.codex/config.toml`)
5. Built-in defaults

## Making Codex Read CLAUDE.md as Fallback

```toml
project_doc_fallback_filenames = ["CLAUDE.md", "AGENTS.md", "COPILOT.md"]
```

This tells Codex to search: `AGENTS.override.md` → `AGENTS.md` → `CLAUDE.md` → `AGENTS.md` (from fallback list) → etc.

## Project Doc Size Limits

```toml
project_doc_max_bytes = 32000  # default
project_doc_max_bytes = 65536  # custom limit
```

Default cap is 32 KiB. 150 lines is a useful heuristic.

## Cross-Tool Rule Sharing Strategies

| Strategy | Description |
|----------|-------------|
| **Symlink** | `ln -s AGENTS.md CLAUDE.md` — simple but loses tool-specific instructions |
| **Shared core + tool-specific** | `AGENTS.md` holds universal instructions; `CLAUDE.md` references it via `@AGENTS.md` plus Claude additions |
| **Single source of truth** | Everything in `AGENTS.md` (native to Codex), `CLAUDE.md` has `@AGENTS.md` for Claude Code |

## Rules System (`.codex/rules/`)

The `.rules` folder holds Markdown files with best practices Codex should ALWAYS follow. Two approaches:
1. Single `CODEX.md` (user or project level)
2. Modular rules folder with `.md` files grouped by concern

**Directory:** `~/.codex/rules/`

**Example rules structure:**
```
~/.codex/rules/
 security.md              # Mandatory security checks
 coding-style.md          # Immutability, file size limits
 testing.md               # TDD, 80% coverage
 git-workflow.md          # Conventional commits
 agents.md                # Subagent delegation rules
 patterns.md              # API response formats
 performance.md           # Model selection (Fast vs Standard vs Deep)
 hooks.md                 # Hook documentation
```

**Example rules content:**
- "No emojis in codebase"
- "Refrain from purple hues in frontend"
- "Always test code before deployment"
- "Prioritize modular code over mega-files"
- "Never commit console.logs"

## Execution Policy Rules (Starlark-based)

Experimental Starlark-based command execution policies using `prefix_rule()`:
```python
# Decisions: allow, prompt, forbidden
prefix_rule("npm install", "allow", "npm install is safe")
prefix_rule("git push --force", "prompt", "force push needs confirmation")
```

Test via `codex execpolicy check`.

## AGENTS.md Best Practices

- Keep it concise — 150 lines is a useful heuristic, but the limit is byte-based (32 KiB)
- Use AGENTS.override.md for personal preferences without affecting the team
- Any developer should be able to launch Codex, say "run the tests" and it works on the first try
- Keep codebases clean and finish migrations — partially migrated frameworks confuse models
- Use config.toml for harness-enforced behavior (approval, sandbox, model) — don't put behavioral rules in AGENTS.md when config.toml settings are deterministic
