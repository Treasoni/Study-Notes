# Workflow Routing

Use this rule file to decide which named workflow to use and where to find active run state.

## Workflow Directory Layout

```text
.claude/workflows/{workflow-id}/workflow.md        # workflow definition
.claude/workflows/{workflow-id}/state-template.md # state file template
workspace/workflow-runs/*.workflow.md                   # active run state
```

## Available Workflows

<!-- workflow-routing:generated:start -->
| Workflow ID | Required | When To Use | Positive Triggers | Excludes | Definition | State File Pattern |
| --- | --- | --- | --- | --- | --- | --- |
| `batch-note-update-flow` | yes | 多篇既有笔记批量更新、逐篇局部 patch | 批量更新旧笔记；多篇笔记过时；更新一个目录的笔记；refresh multiple notes | 只更新单篇笔记；仅生成 MOC | `.claude/workflows/batch-note-update-flow/workflow.md` | `workspace/workflow-runs/update-{scope}.workflow.md` |
| `learning-note-flow` | yes | 新主题学习笔记生产、资料收集、逐章写作、Obsidian 发布 | 想学；帮我整理；研究一下；了解一下；不知道从哪开始；research planning；explore topic | 仅回答一般知识问题；仅修改既有笔记；仅生成 MOC | `.claude/workflows/learning-note-flow/workflow.md` | `workspace/workflow-runs/{topic}.workflow.md` |
| `legacy-note-import-flow` | yes | 旧笔记批量导入、盘点、规范化、可选更新 | 旧笔记导入；已有笔记；一堆笔记；批量整理；迁移到这个项目；按项目规范；import existing notes；normalize notes | 仅更新已有笔记内容；仅生成 MOC | `.claude/workflows/legacy-note-import-flow/workflow.md` | `workspace/workflow-runs/import-{source}.workflow.md` |
<!-- workflow-routing:generated:end -->

## Routing Rules

- Before any action that changes project files, runs project commands, or calls external services, choose the matching `workflow_id` from the table.
- Match the user's original request against positive triggers and exclusions. A matching `Required: yes` workflow cannot use the ordinary execution path.
- If multiple workflows match, choose the more specific workflow; if the route remains ambiguous, ask the user before acting.
- If a matching run already exists under `workspace/workflow-runs/`, resume it instead of creating a duplicate.
- Completed run states follow the repository retention policy; use changelogs, release notes, or ADRs for durable history.
- If no run exists, create a named state file from the workflow's `state-template.md`.
- Name state files after the task or feature, not `todo.md`, unless the project has exactly one workflow.
- Every phase must read the active state file before acting.
- Phase state must be changed only through `.claude/scripts/todo-state.sh`.
- Each workflow directory must have a `routing.yaml`; it is the source of truth for the generated table above.
- After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`. Use `.claude/scripts/sync-workflow-routing.sh --check` in pre-commit or CI.

## Active Runs

| State File | Workflow ID | Task | Current Phase | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
