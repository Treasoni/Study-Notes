# Claude Code Skills - Official Documentation

> Source: https://code.claude.com/docs/en/skills.md
> Title: Extend Claude with skills

## Overview

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it.

**Note:** Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working. Skills add optional features: a directory for supporting files, frontmatter to control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant.

Claude Code skills follow the **Agent Skills** open standard, which works across multiple AI tools.

## Bundled Skills

Claude Code includes a set of bundled skills available in every session:
- `/code-review` - Review the current diff for correctness bugs and cleanups
- `/batch` - Orchestrate large-scale changes in parallel
- `/debug` - Enable debug logging
- `/loop` - Run a prompt repeatedly
- `/claude-api` - Load Claude API reference material

The three run/verify skills work together:
| Skill | Purpose |
|---|---|
| `/run` | Launch and drive your app to see a change working |
| `/verify` | Build and run your app to confirm a code change does what it should |
| `/run-skill-generator` | Teach `/run` and `/verify` how to build and launch your project |

## Where Skills Live

| Location | Path | Applies to |
|---|---|---|
| Enterprise | See managed settings | All users in your organization |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

When skills share the same name across levels, enterprise overrides personal, and personal overrides project. A skill at any of these levels also overrides a bundled skill with the same name.

Skills also load from nested `.claude/skills/` directories below your working directory. When Claude reads or edits a file in a subdirectory, skills from that subdirectory's `.claude/skills/` become available.

## Skill Directory Structure

```text
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

## Frontmatter Reference

| Field | Required | Description |
|---|---|---|
| `name` | No | Display name shown in skill listings |
| `description` | Recommended | What the skill does and when to use it |
| `when_to_use` | No | Additional context for when Claude should invoke the skill |
| `argument-hint` | No | Hint shown during autocomplete |
| `arguments` | No | Named positional arguments for substitution |
| `disable-model-invocation` | No | true = prevent Claude from automatically loading |
| `user-invocable` | No | false = hide from the / menu |
| `allowed-tools` | No | Tools Claude can use without asking permission |
| `disallowed-tools` | No | Tools removed from Claude's available pool |
| `model` | No | Model to use when this skill is active |
| `effort` | No | Effort level when this skill is active |
| `context` | No | Set to `fork` to run in a forked subagent context |
| `agent` | No | Which subagent type to use when context: fork is set |
| `hooks` | No | Hooks scoped to this skill's lifecycle |
| `paths` | No | Glob patterns that limit when this skill is activated |
| `shell` | No | Shell to use for `!`command`` blocks (bash or powershell) |

## Control Who Invokes a Skill

Two frontmatter fields let you restrict invocation:

- **`disable-model-invocation: true`**: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`.
- **`user-invocable: false`**: Only Claude can invoke the skill. Use this for background knowledge that isn't actionable as a command.

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
|---|---|---|---|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

## Skills and Subagents Work Together in Two Directions

| Approach | System prompt | Task | Also loads |
|---|---|---|---|
| Skill with `context: fork` | From agent type | SKILL.md content | CLAUDE.md, except when the agent is Explore or Plan |
| Subagent with `skills` field | Subagent's markdown body | Claude's delegation message | Preloaded skills + CLAUDE.md |

## Inject Dynamic Context

The `!<command>` syntax runs shell commands before the skill content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
```

When this skill runs:
1. Each `!<command>` executes immediately (before Claude sees anything)
2. The output replaces the placeholder in the skill content
3. Claude receives the fully-rendered prompt with actual PR data

## Run Skills in a Subagent

Add `context: fork` to your frontmatter when you want a skill to run in isolation:

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

When this skill runs:
1. A new isolated context is created
2. The subagent receives the skill content as its prompt
3. The `agent` field determines the execution environment
4. Results are summarized and returned to your main conversation

## Relationship to Dynamic Workflows

Skills and dynamic workflows have a clear relationship:
- **Skills** are prompt-based, load into Claude's context, and run in the main session or forked subagent
- **Dynamic workflows** are JavaScript scripts that orchestrate many subagents in the background
- The `/deep-research` workflow is a **bundled workflow** (not a skill) - the distinction is that workflows run in the background via `/workflows` view, while skills run in the foreground

Per the docs: "To add your own commands, see skills." This shows that custom workflows are saved as commands, not as skills, because they have their own orchestration model.

## Available String Substitutions

- `$ARGUMENTS` - All arguments passed when invoking
- `$ARGUMENTS[N]` / `$N` - Specific argument by 0-based index
- `$name` - Named argument declared in arguments frontmatter
- `${CLAUDE_SESSION_ID}` - Current session ID
- `${CLAUDE_EFFORT}` - Current effort level (ultracode reports as xhigh)
- `${CLAUDE_SKILL_DIR}` - Directory containing SKILL.md
