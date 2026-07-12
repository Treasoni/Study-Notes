# Workflow Routing

Use this rule file to decide which named workflow to use and where to find active run state.

## Workflow Directory Layout

```text
.claude/workflows/{workflow-id}/workflow.md        # workflow definition
.claude/workflows/{workflow-id}/state-template.md # state file template
workspace/workflow-runs/*.workflow.md            # active or historical run state
```

## Available Workflows

| Workflow ID | When To Use | Definition | State File Pattern |
| --- | --- | --- | --- |
| `example-flow` | Replace with the trigger scenario. | `.claude/workflows/example-flow/workflow.md` | `workspace/workflow-runs/{task}.workflow.md` |

## Routing Rules

- Before starting a multi-step task, choose the matching `workflow_id` from the table.
- If a matching run already exists under `workspace/workflow-runs/`, resume it instead of creating a duplicate.
- If no run exists, create a named state file from the workflow's `state-template.md`.
- Name state files after the task or feature, not `todo.md`, unless the project has exactly one workflow.
- Every phase must read the active state file before acting.
- Phase state must be changed only through `.claude/scripts/todo-state.sh`.

## Active Runs

| State File | Workflow ID | Task | Current Phase | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
