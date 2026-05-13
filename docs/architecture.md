# Architecture

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

## Design Rationale

Why this project is structured this way:

- **File-based data passing**: Each phase's output is the next phase's input, written to predictable paths under `SYSTEM_ROOT`. This makes each phase independently executable and debuggable without in-memory state.
- **Phase boundary enforcement**: Skills never cross phase boundaries. A skill invoked at Phase 3 cannot trigger Phase 4. This is enforced by CLAUDE.md's critical rules and by each skill's own trigger conditions.
- **Progressive disclosure**: CLAUDE.md is a map (~100 lines), not a manual. Skills own their detailed instructions in `.claude/skills/*/SKILL.md`. Extracted reference material lives in `docs/`. The map stays under 120 lines.

## File Layout

```
study-system/
├── CLAUDE.md                     # Top-level map (~100 lines)
├── README.md                     # User-facing overview
├── .obsidian-config.md           # Vault path, system root config
│
├── docs/                         # Extracted reference documentation
│   ├── phases.md                 # Phase 0-6 detailed steps
│   ├── pre-task-init.md          # Vault path validation details
│   ├── experience-notes.md       # 心得笔记 workflow
│   ├── updating-notes.md         # INSERT / REFRESH modes
│   ├── error-handling.md         # Error recording protocol
│   ├── learnings-digest.md       # Digest thresholds and process
│   ├── architecture.md           # This file
│   └── changelog.md              # System change history
│
├── .claude/
│   ├── settings.local.json       # Permission allowlists
│   └── skills/                   # 16 skill definitions
│       └── */SKILL.md            # Each skill: frontmatter + instructions
│
├── templates/                    # 5 note type templates
│   └── *.md                      # concept, practice, compare, cheat-sheet, experience
│
├── .learnings/                   # Self-improvement system
│   ├── RULES.md                  # Compressed action rules
│   ├── LEARNINGS.md              # Session learnings log
│   ├── ERRORS.md                 # Session errors log
│   └── archive/                  # Old digested entries
│
└── scripts/
    └── validate-structure.sh     # Structure integrity checker
```

## Skill Isolation Principle

Each `.claude/skills/<name>/SKILL.md` defines exactly one capability. Skills are discovered via glob, matched by frontmatter `description`, and invoked by directory name. No skill should call another skill's phase logic — orchestration is the sole responsibility of the main Claude instance following CLAUDE.md.
