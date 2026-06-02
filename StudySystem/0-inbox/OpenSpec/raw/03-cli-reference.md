Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md
(also synthesized from DeepWiki https://deepwiki.com/Fission-AI/OpenSpec/6.2-cli-reference)

# CLI Reference

Full command documentation for the OpenSpec CLI tool.

## Overview

The OpenSpec CLI (`openspec`) is the terminal interface for managing OpenSpec projects. Beyond the slash commands used in AI chat, these commands handle initialization, configuration, validation, and inspection.

## Core CLI Commands

### `openspec init`

Initialize OpenSpec in your project.

```bash
openspec init
```

This walks you through:
- Creating the `openspec/` directory structure
- Selecting your AI coding assistant tool
- Setting up the initial workflow profile
- Generating tool-specific skill files and command adapters

**What it creates:**
```
openspec/
├── specs/
├── changes/
├── config.yaml
├── AGENTS.md
├── .claude/skills/    (for Claude Code)
├── .cursor/commands/  (for Cursor)
└── ... (tool-specific directories)
```

### `openspec update`

Apply profile/configuration changes and regenerate AI instructions.

```bash
openspec update
```

Use this after changing your workflow profile or project configuration to refresh the AI skill files.

### `openspec config profile`

Select workflow profile.

```bash
openspec config profile
```

Interactive prompt to choose between:
- **core** (default) — Quick path with 5 essential workflows: propose, explore, apply, sync, archive
- **custom** — Expanded workflow with all 11 available commands

After selecting, run `openspec update` to apply the changes.

### `openspec list`

List all active changes.

```bash
openspec list
```

Shows all change folders currently in `openspec/changes/` with their status.

### `openspec show <name>`

View change details.

```bash
openspec show add-dark-mode
```

Displays the contents and status of a specific change's artifacts.

### `openspec validate <name>`

Validate spec formatting.

```bash
openspec validate add-dark-mode
```

Checks that spec files follow the proper structure (Purpose, Requirements, Scenarios, Given/When/Then format).

### `openspec view`

Interactive dashboard.

```bash
openspec view
```

Opens a terminal-based interactive view of all changes and specs.

### `openspec archive <name>`

Archive a change from CLI.

```bash
openspec archive add-dark-mode
openspec archive add-dark-mode -y              # Skip prompts
openspec archive add-dark-mode --skip-specs    # Don't merge delta specs
openspec archive add-dark-mode --no-validate   # Skip validation
```

### `openspec status`

Show the current state of changes and their artifact dependency graph. Provides real-time state to AI agents.

```bash
openspec status
openspec status --change add-dark-mode
```

### `openspec instructions`

Generate raw instruction content for AI agents. Shows what instructions are being sent to the AI for creating artifacts.

```bash
openspec instructions --change add-dark-mode --artifact proposal
```

## Schema Commands

### `openspec schema fork <source> <name>`

Copy an existing schema as a starting point for customization.

```bash
openspec schema fork spec-driven my-workflow
```

### `openspec schema init <name>`

Create a new custom schema from scratch.

```bash
# Interactive
openspec schema init research-first

# Non-interactive
openspec schema init rapid \
  --description "Rapid iteration workflow" \
  --artifacts "proposal,tasks" \
  --default
```

### `openspec schema validate <name>`

Validate a custom schema's structure.

```bash
openspec schema validate my-workflow
```

### `openspec schema which <name>`

Debug schema resolution — see where a specific schema resolves from.

```bash
openspec schema which my-workflow
openspec schema which --all
```

## Workspace Commands

### `openspec workspace setup`

Guided setup for coordination workspaces (beta).

```bash
# Interactive
openspec workspace setup

# Non-interactive
openspec workspace setup --no-interactive --name platform --link /repos/api --link web=/repos/web
openspec workspace setup --no-interactive --name platform --link /repos/api --opener codex-cli
```

### `openspec workspace list` / `openspec workspace ls`

See known workspaces from the local registry.

```bash
openspec workspace list
openspec workspace ls
```

### `openspec workspace link`

Add or repair links for the selected workspace.

```bash
openspec workspace link /repos/api
openspec workspace link api-service /repos/api
openspec workspace relink api-service /new/path/to/api
```

### `openspec workspace doctor`

Check what the current machine can resolve.

```bash
openspec workspace doctor
openspec workspace doctor --workspace platform
```

### `openspec workspace update`

Refresh workspace-local guidance and agent skills.

```bash
openspec workspace update
openspec workspace update --workspace platform --tools codex,claude
```

### `openspec workspace open`

Open the linked working set.

```bash
openspec workspace open
openspec workspace open platform --agent github-copilot
openspec workspace open --editor

# Open an initiative
openspec workspace open --initiative billing-launch --store platform
openspec workspace open --initiative billing-launch --store-path /repos/platform-context
```

## Output Formats

CLI commands support JSON output for scripting:

```bash
openspec list --json
openspec status --json
```

JSON responses keep primary data in `workspace`, `workspaces`, or `link` objects and report warnings or errors in `status` arrays.

## Version

```bash
openspec --version
```
