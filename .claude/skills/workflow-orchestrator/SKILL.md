---
name: workflow-orchestrator
description: 业务工作流实例化器。由 planner 技能调用，接收 workflow_id、topic、project_slug 等参数，按 .claude/workflows/{workflow-id}/state-template.md 生成 workspace/workflow-runs/{run-id}.workflow.md。不直接面向用户；通用状态格式和状态流转由 workflow-todo-state 负责。
---

# Workflow Orchestrator - 工作流实例化器

本技能只负责把“已选择的业务工作流”实例化成一次可恢复的运行状态文件。通用状态机规范、命名规则、目录布局和 `todo-state.sh` 属于 `workflow-todo-state`。

## 边界

| 组件 | 职责 |
| --- | --- |
| planner | 理解用户意图，选择 `workflow_id`，准备参数 |
| `.claude/rules/workflow-routing.md` | 汇总可用工作流和适用场景 |
| `workflow-orchestrator` | 根据 `workflow_id` 生成命名 workflow state file |
| `workflow-todo-state` | 定义状态文件格式、目录布局、状态流转脚本和恢复规则 |

本技能不要重新定义状态机格式，不要手写阶段状态流转规则，不要把所有运行文件统一命名为 `todo.md`。

## 输入

planner 传入结构化参数：

```yaml
required:
  workflow_id: "learning-note-flow"
  topic: "React Server Components"

recommended:
  project_slug: "react-server-components"
  run_id: "react-server-components"

optional:
  depth: "上手"
  level: "有了解"
  purpose: "实战"
  output_target: "project-output" # or obsidian
  vault_path: ""
  note_folder: ""
  moc_path: ""
```

兼容旧 planner 时，也接受 `workflow`，并映射为 `workflow_id`。

## 输出

生成一次运行状态文件：

```text
workspace/workflow-runs/{run_id}.workflow.md
```

同时返回：

- `workflow_id`
- workflow 定义文件路径
- state template 路径
- run state file 路径
- 下一步应执行的阶段

## 目录约定

```text
.claude/workflows/{workflow-id}/workflow.md
.claude/workflows/{workflow-id}/state-template.md
.claude/rules/workflow-routing.md
workspace/workflow-runs/{run-id}.workflow.md
```

`workflow-orchestrator` 只使用 `.claude/workflows/{workflow-id}/state-template.md`。旧的 `templates/*-todo.md` 结构已经废弃，不再作为回退来源。

## 实例化流程

1. 读取 `.claude/rules/workflow-routing.md`，确认 `workflow_id` 存在。
2. 定位 `.claude/workflows/{workflow-id}/workflow.md` 和 `state-template.md`。
3. 生成或接收 `run_id`。默认从 `project_slug` 或 `topic` 派生，只使用小写字母、数字和连字符。
4. 检查 `workspace/workflow-runs/{run_id}.workflow.md` 是否已存在。
5. 如果已存在，返回该文件并要求恢复，不要覆盖。
6. 如果不存在，从 `state-template.md` 渲染状态文件。
7. 创建业务项目目录 `${WORKSPACE_PATH:-./workspace}/{project_slug}/`，用于保存阶段产物。
8. 返回 run state file 路径，后续阶段必须通过 `.claude/scripts/todo-state.sh` 更新状态。

## 渲染规则

替换模板中的通用占位符：

```text
{workflow_id}
{topic}
{project_slug}
{run_id}
{date}
{completed_chapters}
{total_chapters}
```

最小 shell 逻辑：

```bash
WORKFLOW_ID="${workflow_id:-${workflow}}"
TOPIC="${topic}"
PROJECT_SLUG="${project_slug:-$(printf '%s' "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')}"
RUN_ID="${run_id:-$PROJECT_SLUG}"
WORKSPACE_PATH="${WORKSPACE_PATH:-./workspace}"

WORKFLOW_DIR=".claude/workflows/${WORKFLOW_ID}"
STATE_TEMPLATE="${WORKFLOW_DIR}/state-template.md"
RUNS_DIR="${WORKSPACE_PATH}/workflow-runs"
RUN_STATE_FILE="${RUNS_DIR}/${RUN_ID}.workflow.md"
PROJECT_DIR="${WORKSPACE_PATH}/${PROJECT_SLUG}"

mkdir -p "$RUNS_DIR" "$PROJECT_DIR"

if [ -f "$RUN_STATE_FILE" ]; then
  echo "已有运行状态文件: $RUN_STATE_FILE"
  echo "请恢复该运行，不要重复创建。"
  exit 0
fi

sed -e "s/{workflow_id}/${WORKFLOW_ID}/g" \
    -e "s/{topic}/${TOPIC}/g" \
    -e "s/{project_slug}/${PROJECT_SLUG}/g" \
    -e "s/{run_id}/${RUN_ID}/g" \
    -e "s/{date}/$(date +%Y-%m-%d)/g" \
    -e "s/{completed_chapters}/0/g" \
    -e "s/{total_chapters}/待大纲确定/g" \
    "$STATE_TEMPLATE" > "$RUN_STATE_FILE"
```

## 可用工作流

以 `.claude/rules/workflow-routing.md` 为准。当前项目内的主要工作流：

| Workflow ID | Definition | State Template |
| --- | --- | --- |
| `learning-note-flow` | `.claude/workflows/learning-note-flow/workflow.md` | `.claude/workflows/learning-note-flow/state-template.md` |
| `legacy-note-import-flow` | `.claude/workflows/legacy-note-import-flow/workflow.md` | `.claude/workflows/legacy-note-import-flow/state-template.md` |
| `batch-note-update-flow` | `.claude/workflows/batch-note-update-flow/workflow.md` | `.claude/workflows/batch-note-update-flow/state-template.md` |

## 与 workflow-todo-state 的关系

生成状态文件后，本技能停止负责状态推进。后续阶段统一调用：

```bash
.claude/scripts/todo-state.sh "${RUN_STATE_FILE}" start P1
.claude/scripts/todo-state.sh "${RUN_STATE_FILE}" complete P1
.claude/scripts/todo-state.sh "${RUN_STATE_FILE}" skip P3 "原因"
.claude/scripts/todo-state.sh "${RUN_STATE_FILE}" block P2 "原因"
```

如果状态文件结构需要调整，先更新 `workflow-todo-state` 的规范和模板，再让本技能按新模板实例化。
