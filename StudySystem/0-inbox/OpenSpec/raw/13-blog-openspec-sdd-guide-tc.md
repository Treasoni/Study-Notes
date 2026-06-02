Source: https://recca0120.github.io/2026/03/08/openspec-sdd/

# OpenSpec: Rang AI Coding Assistant Zhao Guige Zuo Shi, Buyao Luan Xie

**Date:** March 8, 2026
**Author:** recca0120
**Language:** Traditional Chinese
**Categories:** Tools, DevOps
**Tags:** openspec, AI, SDD, Claude-Code, Cursor, Developer-Tools, Workflow

## Summary

AI coding assistants often produce code that doesn't match what you intended. OpenSpec tackles this by having the AI produce a specification document before writing any code, ensuring alignment on both the "what" and the "how."

## Core Architecture

Two areas:
- **Specs** -- the system's source of truth describing current behavior
- **Changes** -- in-progress modifications, each in its own folder

```
openspec/
├── specs/
│   ├── auth/
│   │   └── spec.md
│   └── payments/
│       └── spec.md
└── changes/
    ├── add-dark-mode/
    └── archive/
```

## Basic Workflow: propose -> apply -> archive

### 1. Propose

`/opsx:propose add-dark-mode` generates four artifacts simultaneously:

| Artifact | Question Answered |
|---|---|
| `proposal.md` | Why do it? What's the scope? |
| `specs/` | What system behavior changed? (Delta) |
| `design.md` | How technically? What architecture? |
| `tasks.md` | How many implementation steps? Progress? |

### 2. Apply

AI works through `tasks.md` item by item. Won't deviate from the list. Can resume if interrupted.

### 3. Archive

1. Delta spec merges into `openspec/specs/`
2. Change folder moves to `openspec/changes/archive/`

## Delta Spec Format

Three sections with archive behavior:

| Section | Meaning | Archive Action |
|---|---|---|
| ADDED | New behavior | Added to main spec |
| MODIFIED | Changed behavior | Replaces original |
| REMOVED | Removed behavior | Deleted from main spec |

## Key Insights

- **In-scope/out-of-scope** in proposal.md prevents AI from adding unwanted extras
- **design.md** forces technical decisions before implementation, catching flawed approaches early
- AI "no longer goes off course" -- in new conversations, AI reads `openspec/specs/` and understands context immediately
- **Not suitable for:** changing a single CSS line or fixing a typo

## Comparison

OpenSpec vs Spec Kit vs Kiro:
- OpenSpec: lightweight, fluid, brownfield-friendly via delta specs, 30+ tools
- Spec Kit (GitHub): heavyweight, strict phase gates, tied to GitHub
- Kiro (AWS): IDE-locked, limited models, limited brownfield support

## Stats

v1.2.0 (February 2026), 28k+ GitHub stars, MIT license.
