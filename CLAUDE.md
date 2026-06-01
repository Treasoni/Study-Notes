# CLAUDE.md

This repository contains the **Study System** — a semi-automated technical learning note system built with Claude Code + Obsidian.

## Overview

1. User says "I want to learn X" — **requirement discovery** clarifies intent, generates execution plan
2. Research-driven: 5 phases (discover → collect → write → beautify → [evaluate] → [digest])
3. Experience notes: user content → review → optional research → write → beautify → [evaluate] → [digest]
4. **Autonomy levels** (0-3) control confirmation frequency per `.study-config.yaml`
5. **Hybrid note types** — combine multiple types (e.g., concept + practice)
6. All system files under `{SYSTEM_ROOT}` — user reviews every phase boundary

## Critical Rules

### Phase Boundary Rules (CRITICAL)

After completing ANY phase, you MUST STOP. WAIT for explicit confirmation ("继续", "proceed", "进入下一阶段").
NEVER chain phases. NEVER skip a phase. NEVER assume user approval.

### TODO.md State Machine (CRITICAL)

Use explicit tool names (Read/Write/Bash) — NEVER natural-language verbs like "check" or "mark".

- **Resume Check**: MUST Read tool on `{SYSTEM_ROOT}/TODO.md` at session start. If exists → read `[x]` → ask: "Resume from Phase [N]?"
- **Create**: After user confirms plan → Write tool: create `{SYSTEM_ROOT}/TODO.md` with phases as `- [ ]`
- **Check**: Before ANY phase skill → Read tool on TODO.md → verify prior phases `[x]` → if not, STOP
- **Mark**: After ANY phase completes → Write tool: update `[x]` for that phase
- **Delete**: When done → Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"`

Quality gate: verify prior phases `[x]`, check output files exist and non-empty. If fail → log to error-log.md → ask user.

### Mandatory Triggered Reads（强制前置读取）

| Trigger | Must Read |
|---------|-----------|
| User wants to learn X | `docs/phases.md` |
| User wants 心得笔记 | `docs/experience-notes.md` |
| User wants to update a note | `docs/updating-notes.md` |
| Before any phase skill | `{SYSTEM_ROOT}/TODO.md` |
| Session start | `.study-config.yaml` |
| Error in Phase 1-3 | `docs/error-handling.md` |

DO NOT guess workflow steps from memory — you WILL produce broken output.

### Key Principles

1. System files under `StudySystem/` — no vault root pollution
2. Output path set by user in Phase 0 — never hardcoded
3. Each skill handles its own phase only
4. Data passes through files, not memory
5. Respect autonomy level (0-3) at every phase boundary
6. Every claim traceable to its source
7. Hybrid notes reuse templates via `templates/hybrid-sections.yaml`

## Resource Discovery

Claude uses glob patterns — no hardcoded paths.

- **Skills**: `Glob .claude/skills/*/SKILL.md` → match YAML frontmatter → `Skill(skill="{name}")`
- **Agents**: `Glob .claude/agents/*.md` → match frontmatter → `Agent(subagent_type="{name}")`
- **Templates**: `Glob templates/*.md` → match frontmatter `type` (concept/practice/compare/cheat-sheet/experience)
- **Config**: `Glob .obsidian-config.md` → Read for vault path

## Pre-Task Initialization

Before any Study System task. Full details: [docs/pre-task-init.md](docs/pre-task-init.md)

0. MUST Read tool on `{SYSTEM_ROOT}/TODO.md`. If exists → ask: "Detected unfinished workflow. Resume from Phase [N]?"
1. Read `.obsidian-config.md` → validate `VAULT_PATH`
2. Read `.study-config.yaml` → autonomy level, discovery settings, hybrid limits
3. Read `.learnings/RULES.md` → internalize Do/Don't/Watch For (skip if missing)
4. Resolve `SYSTEM_ROOT` and `OUTPUT_PATH`

## Docs Map

| Doc | Content |
|-----|---------|
| [docs/phases.md](docs/phases.md) | Phase 0-5: requirement discovery, collect+curate, write, beautify, evaluate, digest |
| [docs/experience-notes.md](docs/experience-notes.md) | 心得笔记 7-step workflow: user-input-first, review rules |
| [docs/updating-notes.md](docs/updating-notes.md) | INSERT and REFRESH modes for existing notes |
| [docs/error-handling.md](docs/error-handling.md) | Error recording protocol (Phase 1-3) |
| [docs/learnings-digest.md](docs/learnings-digest.md) | Digest thresholds, compression process |
| [docs/pre-task-init.md](docs/pre-task-init.md) | Vault path validation |
| [docs/architecture.md](docs/architecture.md) | Design rationale, file layout, skill isolation |
| [docs/changelog.md](docs/changelog.md) | System-level change history |

## Directory Convention

```
{VAULT_PATH}/StudySystem/
├── templates/       # Note templates (5 types)
├── 0-inbox/         # Phase 1: collected and curated materials
├── 2-drafts/        # Phase 2: draft notes
├── 3-published/     # Phase 3: final beautified notes (default output)
└── 4-meta/          # Logs, errors, evaluations
```

## Configuration

- `.obsidian-config.md` — vault path, system root, default output path
- `.study-config.yaml` — autonomy level (0-3), subagent settings, requirement discovery, hybrid limits
- `.learnings/RULES.md` — compressed action rules from past sessions

## Autonomy Levels

| Level | Behavior | Confirmation Points |
|-------|----------|-------------------|
| 0 | Full confirmation | Every step |
| 1 | Phase confirmation (default) | Phase boundaries only |
| 2 | Key point confirmation | Note type, execution plan, final result |
| 3 | Full auto | Final result review only |

Set via `autonomy.level` or `autonomy.overrides` in `.study-config.yaml`.

## Requirement Discovery

Before note generation, system asks 4-6 structured questions. Triggered by "I want to learn X".

**Questions:** 1) Purpose (exam/work/interest) 2) Audience (self/team/community) 3) Depth (beginner/advanced/expert) 4) Usage (review/learning/sharing) 5) *(optional)* Focus areas 6) *(optional)* Knowledge level

System recommends hybrid note type combination. User can accept or override. See [docs/phases.md](docs/phases.md) for Phase 0 details. Can be skipped (defaults: concept, level 1, intermediate).

## Hybrid Note Types

Combine multiple types (max 2 per config). Section ordering in `templates/hybrid-sections.yaml`.

| Combination | Key Sections |
|-------------|-------------|
| concept + practice | Core Concept → Practical Examples → Patterns |
| compare + cheat_sheet | Comparison → Quick Reference → Decision Framework |
| experience + concept | Background → Core Concept → Insights |
| concept + cheat_sheet | Core Concept → Key Points → Quick Reference |

Single-type notes fully supported. Hybrid notes require `[来源: R1]` attribution per section.

## Structure Integrity

Run `bash scripts/validate-structure.sh` after structural changes to verify:
- CLAUDE.md ≤ 160 lines, all docs/ references resolve, valid frontmatter, required config fields
