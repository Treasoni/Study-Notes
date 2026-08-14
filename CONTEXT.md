# Study System

学习笔记自动化生产系统：把一次学习意图（topic）经由命名工作流定义、分阶段状态文件与 skill/agent 依赖链，产出可发布到 Obsidian 的学习笔记。本 context 记录该系统自身的领域词汇。

## Language

### Workflow structure

**Workflow definition**:
The reusable spec of a named workflow, living in `.claude/workflows/{workflow_id}/` (`workflow.md` + `state-template.md` + `routing.yaml`).
_Avoid_: 工作流（当指运行实例时）

**Workflow run**:
One concrete execution of a workflow definition for a single topic, tracked by a run state file.
_Avoid_: 工作流（当指定义时）

**Run state file**:
The source-of-truth file at `workspace/workflow-runs/{topic}.workflow.md`: YAML frontmatter (`workflow_id`, `run_id`, `project_slug`, `current_phase`, `mode`, `confirmed_phases`) plus a phased checklist. Every skill/agent reads it before acting.
_Avoid_: todo、workflow file

**Phase**:
A numbered stage of a run (P0–P7 plus `done`), each with a checklist and a status (`⬜ 未开始` / `🔲 进行中` / `✅ 已完成` / `⏭️ 跳过`), advanced only through `.claude/scripts/todo-state.sh`.
_Avoid_: step

**Checkpoint**:
A phase-boundary gate that pauses the run for explicit user confirmation before the next phase begins; confirmed phases are recorded in `confirmed_phases`.
_Avoid_: review gate

**Mode**:
A run-level variant that changes which phases execute — `outline` runs outline generation (P3/P4), `freeform` skips it (`mode_dependent_skips`).
_Avoid_: —

### Workspace & identity

**Topic workspace**:
The per-topic directory `workspace/{project_slug}/` holding a run's artifacts (`00_intent.md`, `01_explore_result.md`, `02_deep_research.md`, `03_outline.md`, `chapters/`, `output/`).
_Avoid_: 项目（当指整个 vault 时）

**project_slug**:
ASCII dash-separated name of the topic workspace; usually equals `run_id`.
_Avoid_: —

**run_id**:
Identifier of a run state file; usually equals `project_slug`.
_Avoid_: —

**Intent file**:
`00_intent.md`, produced in P0; records the intent dimensions for the run.
_Avoid_: requirement doc

**Intent dimensions**:
The dimensions captured in P0 and stored in the intent file: note type (实战/概念/心得/对比), learning depth (入门/上手/精通), user level (零基础/有了解/熟悉), and output location (project output vs Obsidian vault).
_Avoid_: metadata

### Roles & outputs

**Planner skill**:
A user-facing entry skill that captures intent and hands off to the orchestrator (`research-planner`, `legacy-note-importer`, `batch-note-updater`).
_Avoid_: 引导 agent

**Orchestrator**:
The `workflow-orchestrator` skill that instantiates a workflow definition into a run (writes the run state file).
_Avoid_: —

**Domain agent**:
A specialized sub-agent invoked by the skill/agent chain to do one kind of work (`outline-generator`, `chapter-writer`, `note-assembler`).
_Avoid_: skill（当指执行角色时）

**Learning note**:
The final product: a Markdown note assembled from `chapters/`, beautified for Obsidian, and published to the vault with optional MOC sync.
_Avoid_: article、post

**MOC**:
A Map-of-Content directory note indexing notes per topic with one-line entries, maintained by `moc-organizer`.
_Avoid_: 目录（有歧义）
