---
name: workflow-todo-state
description: Create or retrofit reusable todo.md workflow state machines for multi-step agent projects. Use when a project needs recoverable progress tracking, phase gates, restart-safe agent workflows, explicit skipped/blocked states, or reusable todo templates across repositories.
---

# Workflow Todo State

Use this skill to make long-running agent workflows recoverable from a project-local `todo.md`. The pattern combines human-readable Markdown checklists with machine-readable YAML frontmatter and a deterministic state script.

## Quick Start

Install into another project:

```bash
.claude/skills/workflow-todo-state/scripts/install.sh /path/to/target-project --with-skill --update-agents
```

Then:

1. Create or update the workflow `todo.md` from `references/basic-todo-template.md`.
2. Ensure every phase has exactly one status line:
   ```markdown
   > [P0] ⬜ 未开始
   ```
3. Make every workflow skill or agent read `todo.md` before starting work.
4. Update state only through the script:
   ```bash
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" start P1
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P1
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" skip P2 "not needed"
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" block P3 "waiting for user input"
   ```

## Required Todo Shape

Each reusable workflow todo should contain:

- YAML frontmatter with `workflow`, `topic`, `project_slug`, `created_at`, `last_updated`, `current_phase`, `current_status`, `mode`, and `blocked_reason`.
- A visible line beginning with `> 当前阶段：`.
- One unique phase status line per phase, using `> [PN] ...`.
- An `## 异常记录` table if `skip` or `block` should append history.

See `references/basic-todo-template.md` for a minimal portable template and `references/integration.md` for retrofit instructions.

## State Rules

- `start PN` requires all previous phases to be `✅ 已完成` or `⏭️ 跳过`.
- `complete PN` requires the phase to be `🔲 进行中`.
- `skip PN` refuses completed phases and records a reason.
- `block PN` marks the current phase in progress, writes `current_status: blocked`, and records a reason.
- After `complete` or `skip`, the script advances `current_phase` to the next `⬜ 未开始` phase, or to `done` when no pending phase remains.

## When Retrofitting A Project

Keep the change small:

1. Add the script.
2. Add frontmatter and unique phase lines to existing `todo.md` templates.
3. Replace ad hoc `sed` or manual status edits in skills/agents with `todo-state.sh`.
4. Add one rule to the project entry instructions: every phase must read `todo.md` before acting.
5. Test one happy path and one blocked/invalid transition.

Do not force a project to adopt this exact workflow structure. Preserve local phase names, output files, and user confirmation gates.
