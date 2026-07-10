# Codex CLI Comprehensive Configuration Guide (everything-openai-codex)

Source: https://github.com/mturac/everything-openai-codex/blob/main/the-shortform-guide.md
Fetched: 2026-07-11

## Skills & Commands

Skills live at `~/.codex/skills/` and are reusable prompts, structures, supporting files, and codemaps. They serve as the primary workflow surface.

Legacy commands remain at `~/.codex/commands/` but are legacy slash-entry compatibility during migration. Durable logic should live in skills.

**Example skill structure:**
```
~/.codex/skills/
 pmx-guidelines.md        # Project-specific patterns
 coding-standards.md      # Language best practices
 tdd-workflow/            # Multi-file skill with SKILL.md
 security-review/         # Checklist-based skill
```

## Hooks

Six hook types identified:

1. **PreToolUse** — fires before a tool executes (validation, reminders)
2. **PostToolUse** — fires after a tool finishes (formatting, feedback loops)
3. **UserPromptSubmit** — when you send a message
4. **Stop** — when Codex finishes responding
5. **PreCompact** — before context compaction
6. **Notification** — permission requests

**Example PreToolUse for tmux reminder:** matches Bash calls for `npm|pnpm|yarn|cargo|pytest`, checks if `$TMUX` is set, outputs a reminder if not.

**Common hook configs:**
- **PreToolUse:** tmux reminder for long-running commands; blocks `.md` writes unless README/CODEX; opens editor for review on `git push`
- **PostToolUse:** auto-runs `prettier --write` after editing `.ts/.tsx/.js/.jsx`; runs `tsc --noEmit` after TypeScript edits; greps for `console.log` warnings
- **Stop:** checks all modified files for `console.log`

## Subagents (Agents Configuration)

Subagents are processes your main Codex can delegate tasks to with limited scopes. They can run in background or foreground.

**Directory:** `~/.codex/agents/`

Subagents pair well with skills — a subagent capable of executing a subset of your skills can be delegated tasks and use those skills autonomously. They can also be sandboxed with specific tool permissions.

**Recommended:** Configure allowed tools, MCPs, and permissions per subagent for proper scoping.

**Agent lineup example:**
```
~/.codex/agents/
 planner.md               # Break down features
 architect.md             # System design
 tdd-guide.md             # Write tests first
 code-reviewer.md         # Quality review
 security-reviewer.md     # Vulnerability scan
 build-error-resolver.md
 e2e-runner.md            # Playwright tests
 refactor-cleaner.md      # Dead code removal
 doc-updater.md           # Keep docs synced
```

## Rules and Memory

The `.rules` folder holds `.md` files with best practices Codex should ALWAYS follow.

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
 performance.md           # Model selection
 hooks.md                 # Hook documentation
```

## MCPs (Model Context Protocol)

MCPs connect Codex to external services directly. Key rule: keep 20-30 MCPs in config, but keep under 10 enabled / under 80 tools active.

Navigate via `/plugins` or `/mcp` commands.

**Author's configured MCPs** (14 total, ~5-6 enabled per project):
- github, firecrawl, supabase, memory, sequential-thinking, vercel, railway, cloudflare-docs, cloudflare-workers-bindings, clickhouse, AbletonMCP, magic

## Plugins

Plugins package tools for easy installation. Install via:
```
codex plugin marketplace add https://github.com/mixedbread-ai/mgrep
```
Then open Codex, run `/plugins`, find the new marketplace, and install.

**Plugin types:** LSP plugins are particularly useful if you run Codex outside editors frequently, providing real-time type checking and intelligent completions.

## Custom Status Line

Configured via `/statusline`. Shows user, directory, git branch with dirty indicator, context remaining %, model, time, and todo count.
