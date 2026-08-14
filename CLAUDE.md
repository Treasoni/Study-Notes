# Study System

学习笔记自动化生产系统。

## 可用工作流

每个工作流由「planner + orchestrator + workflow definition + state template」组成：

| 工作流 | 对应 planner | 定义文件 | 用途 |
|-------|-------------|-----------|------|
| learning-note-flow | `/research-planner` | `.claude/workflows/learning-note-flow/` | 完整学习笔记生产 + Obsidian 发布 + MOC 同步 |
| legacy-note-import-flow | `/legacy-note-importer` | `.claude/workflows/legacy-note-import-flow/` | 已有旧笔记批量导入、规范化、可选更新与 MOC 同步 |
| batch-note-update-flow | `/batch-note-updater` | `.claude/workflows/batch-note-update-flow/` | 多篇既有笔记批量更新、逐篇局部 patch 与 MOC 同步 |

> 新增工作流：在 `.claude/workflows/{workflow-id}/` 创建 `workflow.md`、`state-template.md` 和 `routing.yaml`，并新建对应 planner 或入口 skill。
> orchestrator 通常不直接面向用户，由各 planner 或入口 skill 调用。上游负责领域特定的意图澄清，orchestrator 负责生成 `workspace/workflow-runs/*.workflow.md`。

## 核心原则

### 必须执行 workflow state file

**每个技能/Agent 启动时必须:**
1. 读取 `workspace/workflow-runs/*.workflow.md` 中的当前运行状态文件
2. 确认当前阶段状态
3. 通过 `.claude/scripts/todo-state.sh` 启动或完成阶段
4. 不可跳步，不可不做

**状态流转（[PN] 标记精准定位，不跨阶段污染）**:
```
[PN] ⬜ 未开始 → [PN] 🔲 进行中 → [PN] ✅ 已完成
```

### 断点恢复机制

1. **读取状态**: 每个技能启动时读取当前 workflow state file
2. **验证前置**: 检查前置阶段是否为 ✅
3. **更新状态**: 开始时调用 `todo-state.sh start PN`，完成后调用 `todo-state.sh complete PN`
4. **阶段推进**: 由状态脚本更新 `当前阶段` 字段和 YAML recovery metadata

## 文件结构

```
${WORKSPACE_PATH:-./workspace}/
├── {topic-slug}/
│   ├── 00_intent.md
│   ├── 01_explore_result.md
│   ├── 02_deep_research.md
│   ├── 03_outline.md
│   ├── chapters/
│   └── output/
├── workflow-runs/
│   └── {run-id}.workflow.md
└── ...
```

## 技能依赖关系

核心链路：

```
research-planner → workflow-orchestrator（生成命名 workflow state file）
→ research-collector → outline-generator → chapter-writer
→ note-assembler → note-beautifier → moc-organizer
```

## 工作流执行规则

### 阶段完成检查点

每阶段结束都必须让用户确认后才进入下一阶段:

| 阶段 | 检查点内容 |
|------|-----------|
| 0 → 1 | 用户确认意图文件和研究计划 |
| 1 → 2 | 用户确认素材质量 |
| 2 → 3 | 用户确认大纲顺序和深度 |
| 3 → 4 | 用户确认大纲（大纲模式） |
| 4 → 5 | 所有章节写作完成 |
| 5 → 6 | 用户确认组装结果和 Obsidian 输出位置 |
| 6 → 7 | 用户确认是否同步 MOC |

### 错误处理

| 情况 | 处理方式 |
|------|---------|
| 缺少意图文件 | 重新调用 `/research-planner` |
| 缺少素材文件 | 重新调用 `/research-collector` |
| 缺少大纲文件 | 重新调用 `outline-generator` |
| 缺少章节文件 | 重新调用 `chapter-writer` |
| 缺少输出位置 | 先保存到项目 `output/`，等待用户指定 Obsidian 位置 |
| 已有一批旧笔记要接入项目 | 调用 `legacy-note-importer`，先盘点和生成迁移计划 |
| 多篇旧笔记过时 | 调用 `batch-note-updater`，先生成更新清单和批量计划 |
| 旧笔记过时 | 调用 `note-updater`，不要重跑完整新笔记流程 |

## Workflow Todo State

Named workflow state files are the source of truth for every routed workflow.

- Workflow definitions live under `.claude/workflows/{workflow-id}/`.
- Workflow state files live under `workspace/workflow-runs/` and should be named after the task.
- Before any action that changes project files, runs project commands, or calls external services, read `.claude/rules/workflow-routing.md` and match the user's original request against its triggers and exclusions.
- When a `Required: yes` workflow matches, read its `workflow.md`, create or resume its state file, and start the current phase before doing the work. Do not take the ordinary execution path instead.
- If the route is ambiguous, ask the user before acting.
- Read the active workflow state file before starting any phase; do not skip prerequisite phases.
- Change phase state only through `.claude/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始`.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
- Each workflow directory must contain a `routing.yaml`. After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`; the update is incomplete until `.claude/scripts/sync-workflow-routing.sh --check` passes.

<!-- prompt-cache-bootstrap:begin -->
## Prompt Cache

- Follow `.claude/rules/common/prompt-cache.md` for high-frequency prompt design.
- Keep stable instructions and output formats before dynamic user input, file excerpts, dates, IDs, and runtime state.
- Reuse canonical templates and load long context only when needed.
<!-- prompt-cache-bootstrap:end -->

## Agent skills

### Issue tracker

Issues and specs live in this repo's GitHub issues, operated via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Five default triage labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.

<!-- env-template:claude:begin -->
## Environment Variables

- Follow `.claude/rules/common/env.md` whenever creating, updating, migrating, or auditing `.env`, `.env.example`, or environment-variable documentation.
- Keep committed env templates minimal, project-specific, and free of real secrets or machine-local absolute paths.
- After env template changes, run `.claude/scripts/check-env-template.sh`. Use `--strict` when you want unused documented variables to fail the check.
<!-- env-template:claude:end -->


<!-- workflow-todo-state:start -->
## Workflow Todo State

Named workflow state files are the source of truth while a routed workflow is active.

- Workflow definitions live under `.claude/workflows/{workflow-id}/`.
- Workflow state files live under `workspace/workflow-runs/` and should be named after the task, for example `payment-refactor.workflow.md`.
- Before any action that changes project files, runs project commands, or calls external services, read `.claude/rules/workflow-routing.md` and match the user's original request against its triggers and exclusions.
- When a `Required: yes` workflow matches, read its `workflow.md`, create or resume its state file, and start the current phase before doing the work. Do not take the ordinary execution path instead.
- If the route is ambiguous, ask the user before acting.
- Read the active workflow state file before starting any phase; do not skip prerequisite phases.
- Change phase state only through `.claude/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始 {not_started}`.
- The final phase requires `quality_gate: passed`; a temporary waiver also requires an owner and due date.
- Completed run states follow the repository retention policy and do not replace changelogs or release records.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
- Each workflow directory must contain a `routing.yaml`. After creating, changing, renaming, or deleting a workflow, run `.claude/scripts/sync-workflow-routing.sh`; the update is incomplete until `.claude/scripts/sync-workflow-routing.sh --check` passes.
<!-- workflow-todo-state:end -->
