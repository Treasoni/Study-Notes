# CLAUDE.md

This repository contains the **Study System** — a semi-automated technical learning note system built with Claude Code + Obsidian.

## Overview

1. User says "I want to learn X" or "I want to write about my experience with X" — use [Resource Discovery](#resource-discovery规则寻址) glob patterns to locate the right skill
2. For research-driven notes: Main Claude orchestrates 6 phases: collect → curate → write → beautify → evaluate → [digest]
3. For experience notes (心得笔记): user provides content → review → optional research → write → beautify → evaluate → [digest]
4. Each phase reads/writes files under `{VAULT_PATH}/StudySystem/`
5. User reviews and approves at each phase boundary

## Critical Rules

### Phase Boundary Rules (CRITICAL)

After completing ANY phase, you MUST STOP. DO NOT invoke the next phase's skill.
Present results to the user and WAIT for explicit confirmation (e.g. "继续", "proceed", "进入下一阶段").

NEVER chain phases together. NEVER skip a phase. NEVER assume user approval.

### Mandatory Triggered Reads（强制前置读取）

Before entering ANY of the following workflows, you MUST use the Read tool to load the corresponding doc. DO NOT guess the workflow steps from training data.

| Trigger | Must Read | Reason |
|---------|-----------|--------|
| User wants to learn X (Phase 0-6) | `docs/phases.md` | Phase steps, question scripts, execution plan format |
| User wants 心得笔记 | `docs/experience-notes.md` | Review rules, DO/DON'T table, research decision flow |
| User wants to update a note | `docs/updating-notes.md` | INSERT vs REFRESH modes, key update rules |
| Error occurs in Phase 1-4 | `docs/error-handling.md` | Recording protocol, retry/skip/abort procedure |
| Digest thresholds exceeded | `docs/learnings-digest.md` | Compression steps, archive procedure |
| Pre-task init fails | `docs/pre-task-init.md` | Vault path validation details |

If you skip the Read and invent workflow steps from memory, you WILL produce broken output (wrong file paths, skipped phases, missing user prompts).

### Quality Gates

Between each phase, check:
- Previous phase output files exist and are non-empty
- Output content is consistent with input
- If checks fail → log to error-log.md → ask user how to proceed

### Key Principles

1. All system files live under `StudySystem/` — don't pollute the vault root
2. Output path is set by user in Phase 0 — never hardcoded
3. Each skill only handles its own phase — no crossing boundaries
4. Data passes through files, not memory — each phase's output is the next phase's input
5. User reviews after every phase — no full automation
6. Prefer official docs and primary sources
7. Every claim must be traceable to its source

## Resource Discovery（规则寻址）

Claude uses glob patterns to discover project resources. No hardcoded paths. New resources are auto-discoverable when placed in the right directory with proper frontmatter `description`.

- **Skills**: `Glob .claude/skills/*/SKILL.md` → match YAML frontmatter `description` → invoke via `Skill(skill="{name}")`
- **Agents**: `Glob .claude/agents/*.md` → match frontmatter `name`, `description`, `tools` → invoke via `Agent(subagent_type="{name}")`
- **Templates**: `Glob templates/*.md` → match frontmatter `type` (concept / practice / compare / cheat-sheet / experience)
- **Learnings**: `Glob .learnings/RULES.md` → Read before each new task, internalize Do / Don't / Watch For
- **Config**: `Glob .obsidian-config.md` → Read for vault path

## Pre-Task Initialization

Before any Study System task, resolve the vault path and internalize past learnings. Full details: [docs/pre-task-init.md](docs/pre-task-init.md)

1. Read `.obsidian-config.md` → validate `VAULT_PATH` (ask user if empty, `ls` to verify if set)
2. Read `.learnings/RULES.md` → note what to do, avoid, watch for (skip if doesn't exist)
3. Resolve `SYSTEM_ROOT` and `OUTPUT_PATH` from config values

## Docs Map

| Doc | Content |
|-----|---------|
| [docs/phases.md](docs/phases.md) | Full Phase 0-6 details: requirement clarification, collect, curate, write, beautify, evaluate, digest |
| [docs/experience-notes.md](docs/experience-notes.md) | 心得笔记 7-step workflow: user-input-first, review rules, optional research |
| [docs/updating-notes.md](docs/updating-notes.md) | INSERT and REFRESH modes for existing notes |
| [docs/error-handling.md](docs/error-handling.md) | Error recording protocol (Phase 1-4), plain-text format |
| [docs/learnings-digest.md](docs/learnings-digest.md) | Digest thresholds, compression process, RULES.md format |
| [docs/pre-task-init.md](docs/pre-task-init.md) | Detailed vault path validation for first-run and subsequent sessions |
| [docs/architecture.md](docs/architecture.md) | Design rationale, file layout, skill isolation principle |
| [docs/changelog.md](docs/changelog.md) | System-level change history |

## Directory Convention

```
{VAULT_PATH}/StudySystem/
├── templates/       # Note templates (5 types)
├── 0-inbox/         # Phase 1: raw collected materials
├── 1-curated/       # Phase 2: organized and scored materials
├── 2-drafts/        # Phase 3: draft notes
├── 3-published/     # Phase 4: final beautified notes (default output)
└── 4-meta/          # Logs, errors, evaluations
```

## Configuration

- `.obsidian-config.md` — vault path, system root, default output path
- `.learnings/RULES.md` — compressed action rules from past sessions
- `.claude/settings.local.json` — permission allowlists

## Structure Integrity

Run `bash scripts/validate-structure.sh` after structural changes to verify:
- CLAUDE.md ≤ 120 lines
- All docs/ references resolve to existing files
- All skills and templates have valid frontmatter
- Config file has required fields
