---
name: workflow-todo-state
description: Create or retrofit reusable named workflow state machines for multi-step agent projects. Use when a project needs recoverable workflow state files, multiple workflow definitions, phase gates, restart-safe agent workflows, explicit skipped/blocked states, workflow routing rules, or reusable workflow templates across repositories.
---

# Workflow Todo State

Use this skill to make long-running agent workflows recoverable from named workflow state files. The pattern combines human-readable Markdown checklists with machine-readable YAML frontmatter and a deterministic state script.

## Quick Start

Install into another project:

```bash
.claude/skills/workflow-todo-state/scripts/install.sh /path/to/target-project --with-skill --init-layout --update-agents
```

Then:

1. Create workflow definitions under `.claude/workflows/{workflow-id}/`.
2. Create run state files under `workspace/workflow-runs/{task-or-feature}.workflow.md`.
3. Register workflow routing in `.claude/rules/workflow-routing.md`.
4. Create or update the state file from `references/basic-state-template.md`.
5. Ensure every phase has exactly one status line:
   ```markdown
   > [P0] ⬜ 未开始
   ```
6. Make every workflow skill or agent read the relevant workflow state file before starting work.
7. Update state only through the script:
   ```bash
   .claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" start P1
   .claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" complete P1
   .claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" skip P2 "not needed"
   .claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" block P3 "waiting for user input"
   ```

## Recommended Layout

Use separate files for workflow definitions and workflow runs:

```text
.claude/
  workflows/
    feature-development/
      workflow.md
      state-template.md
    release-check/
      workflow.md
      state-template.md
  rules/
    workflow-routing.md
workspace/
  workflow-runs/
    payment-refactor.workflow.md
    release-v1-2.workflow.md
```

Do not name every run `todo.md` when a project can have multiple workflows. Prefer descriptive state files:

- `{feature-name}.workflow.md`
- `{task-name}.workflow.md`
- `{workflow-id}-{run-id}.workflow.md`

Use `todo.md` only for a single-purpose project where one workflow will ever exist.

## Required State File Shape

Each reusable workflow state file should contain:

- YAML frontmatter with `workflow_id`, `workflow_name`, `workflow_version`, `state_file_type`, `run_id`, `task`, `created_from`, `current_phase`, `current_status`, `mode`, and `blocked_reason`.
- A visible line beginning with `> 当前阶段：`.
- One unique phase status line per phase, using `> [PN] ...`.
- An `## 异常记录` table if `skip` or `block` should append history.

See `references/basic-state-template.md` for a minimal portable state template, `references/workflow-routing-template.md` for routing rules, and `references/integration.md` for retrofit instructions.

## State Rules

- `start PN` requires all previous phases to be `✅ 已完成` or `⏭️ 跳过`.
- `complete PN` requires the phase to be `🔲 进行中`.
- `skip PN` refuses completed phases and records a reason.
- `block PN` marks the current phase in progress, writes `current_status: blocked`, and records a reason.
- After `complete` or `skip`, the script advances `current_phase` to the next `⬜ 未开始` phase, or to `done` when no pending phase remains.

## When Retrofitting A Project

Keep the change small:

1. Add the script.
2. Add `.claude/workflows/`, `workspace/workflow-runs/`, and `.claude/rules/workflow-routing.md`.
3. Add frontmatter and unique phase lines to existing state files.
4. Replace ad hoc `sed` or manual status edits in skills/agents with `todo-state.sh`.
5. Add one rule to the project entry instructions: every phase must read the relevant workflow state file before acting.
6. Test one happy path and one blocked/invalid transition.

Do not force a project to adopt this exact workflow structure. Preserve local phase names, output files, and user confirmation gates.
