# Codex CLI Custom Prompts and Commands Configuration

Source: https://learn.chatgpt.com/docs/custom-prompts and community resources
Fetched: 2026-07-11

## Custom Prompts (Deprecated)

Custom prompts are deprecated. OpenAI recommends using **skills** instead for reusable instructions. Custom prompts require explicit invocation and live in your local Codex home directory (e.g., `~/.codex`).

## Directory Setup

Create `~/.codex/prompts/` — Codex scans only top-level Markdown files in that folder, ignoring subdirectories and non-Markdown files.

## File Format & Front Matter

Each prompt is a Markdown file with YAML frontmatter:

| Field | Purpose |
|-------|---------|
| `description:` | Shown under the command name in the slash-command popup |
| `argument-hint:` | Documents expected parameters, e.g., `KEY=<value>` |

## Placeholder System

| Syntax | Behavior |
|--------|----------|
| `$1` through `$9` | Expand from space-separated positional arguments |
| `$ARGUMENTS` | Includes all positional arguments |
| `$UPPERCASE_NAME` | Named placeholders; supply values as `KEY=value` |
| `$$` | Emits a single literal `$` in the expanded output |

Quote values containing spaces: `FOCUS="loading state"`

## Example File

A file at `~/.codex/prompts/draftpr.md`:
```markdown
---
description: Draft a PR description from changed files
argument-hint: FILES=<paths> PR_TITLE=<title>
---

Write a PR description covering $FILES with title $PR_TITLE.
```

## Usage

1. Type `/` to open the slash command menu
2. Enter `prompts:` or the prompt name, e.g., `/prompts:draftpr`
3. Supply arguments: `/prompts:draftpr FILES="src/index.astro" PR_TITLE="Add hero animation"`
4. Press Enter — Codex expands the Markdown content, replaces placeholders, and sends the result

## Skills vs Custom Prompts

| Aspect | Skills | Custom Prompts |
|--------|--------|---------------|
| Status | Current | Deprecated |
| Invocation | `$skill-name` or implicit | `/prompts:name` |
| Shareability | Via plugins, git | Local only |
| Auto-trigger | Yes (by description) | No |
| Subdirectories | Yes (scripts, references, assets) | No |
| Frontmatter required | name + description | description (optional) |

## Alternative: Custom Workflows via Commands

Codex CLI **reserves the `/` prefix for built-in commands only** — there is no project-level custom slash command registration.

For custom workflows, use:
1. **Skills** — the recommended approach for reusable workflows
2. **Hooks** — for lifecycle automation
3. **Subagents** — for delegated task execution

## Community Prompt Collections

| Collection | Description |
|------------|-------------|
| brucehart/codex-prompts | API docs, commits, PRs, refactors, explanations, tests |
| feiskyer/codex-settings | 40+ curated prompts and skills |
