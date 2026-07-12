# Workflow Routing

本规则汇总项目内可用工作流，并说明什么时候使用哪个工作流。

## Directory Layout

```text
.claude/workflows/{workflow-id}/workflow.md
.claude/workflows/{workflow-id}/state-template.md
workspace/workflow-runs/{task}.workflow.md
```

## Available Workflows

| Workflow ID | When To Use | Definition | State File Pattern |
| --- | --- | --- | --- |
| `learning-note-flow` | 新主题学习笔记生产、资料收集、逐章写作、Obsidian 发布 | `.claude/workflows/learning-note-flow/workflow.md` | `workspace/workflow-runs/{topic}.workflow.md` |
| `legacy-note-import-flow` | 旧笔记批量导入、盘点、规范化、可选更新 | `.claude/workflows/legacy-note-import-flow/workflow.md` | `workspace/workflow-runs/import-{source}.workflow.md` |
| `batch-note-update-flow` | 多篇既有笔记批量更新、逐篇局部 patch | `.claude/workflows/batch-note-update-flow/workflow.md` | `workspace/workflow-runs/update-{scope}.workflow.md` |

## Routing Rules

- 多阶段任务开始前，先根据用户目标选择 `Workflow ID`。
- 如果 `workspace/workflow-runs/` 中已有匹配状态文件，优先恢复已有运行，不要重复创建。
- 如果没有状态文件，按对应 workflow 模板创建命名状态文件。
- 状态文件不要统一命名为 `todo.md`；除非项目只有一个固定工作流。
- 每阶段开始前必须读取当前状态文件。
- 阶段状态只能通过 `.claude/scripts/todo-state.sh` 更新。

## Active Runs

| State File | Workflow ID | Task | Current Phase | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
