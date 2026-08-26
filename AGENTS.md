# Study System - Codex Project Guidance

本项目同时保留两套 runtime 配置。Codex 工作时必须遵守下面的隔离规则：

1. 默认不要搜索或读取 `.claude/` 下的任何文件，除非用户明确要求维护 Claude Code 配置，或执行本项目规定的同步操作。
2. 专用配置、规则、hooks 和脚本只放在本项目对应 runtime 的配置目录（目录映射见 `.agent-sync/agents/*.yaml` 的 `paths`）；可跨 runtime 的 skill 放在 canonical skills 目录（见 `.codex/platform/registry.yaml` 的 `discovery.Skill`）。两者都不写入全局 runtime 配置目录。
3. 项目级长期规则以本文件为入口；更细规则见 `.codex/rules/`。
4. 需要使用技能时，优先读取 `.agents/skills/{skill-name}/SKILL.md` 作为入口，完整理解后再执行；只在任务需要时继续读取其引用的模板、示例和资料，避免预加载无关内容。
5. 需要模拟原 Claude agent 时，读取 `.codex/agents/{agent-name}.md`，按其中角色、输入、输出和检查点执行。
6. 各区域 canonical source 由 `.agent-sync/agents/*.yaml` 的 `paths` 定义（skills canonical 见 `.codex/platform/registry.yaml` 的 `discovery.Skill`；rules/hooks/scripts/workflows canonical 在 `.codex/` 下对应目录）。修改后，先运行 `.agent-sync/sync_agents.py --root . --check --scope <area>`，再 `--apply`，最后运行全量 `--check`。生成目标目录（如 `.claude/`）不手工编辑；hook 变更后额外运行 `.agent-sync/bootstrap.py --root . --apply` 与 `--check`。

## Agent Platform Manifest

Workflow、Skill、Subagent 和 Hook 都必须在各自工件目录下的 `manifest.yaml` 中声明统一契约（工件目录由 `.codex/platform/registry.yaml` 的 `discovery` 定义，跨 runtime 共享）。manifest 负责自动发现、版本、入口、能力、依赖和请求权限；它不自行授予任何工具权限，运行时仍以平台策略和用户授权为准。

- 新增、删除、重命名或实质修改上述工件时，同步更新其 manifest 的版本、依赖和最小权限。
- 入口路径相对 manifest 目录解析，且不得离开该工件的配置根目录。
- 变更后运行 `python3 .codex/platform/manifest-registry.py --root . validate`；Hook 还必须继续在 `.codex/hooks.json` 中注册。
- 复用到其他项目时，使用项目内 `manifest-platform` Skill 的安装脚本，不把该平台配置写入全局配置目录（如 `~/.codex/`、`~/.claude/`）。

## Core Workflow

学习笔记生产流程保持与 Claude Code 版一致：

```text
research-planner -> workflow-orchestrator -> research-collector
-> outline-generator -> chapter-writer -> note-assembler
-> note-beautifier -> moc-organizer
```

已有旧笔记批量接入使用独立流程：

```text
legacy-note-importer -> note-beautifier
-> note-updater（可选） -> moc-organizer
```

已有多篇旧笔记批量更新使用独立流程：

```text
batch-note-updater -> note-updater
-> moc-organizer（可选）
```

每个阶段启动前必须读取命名 workflow state file（`workspace/workflow-runs/*.workflow.md`），确认当前阶段和前置状态。`todo.md` 只作为历史兼容概念，不作为新运行的状态文件。不能跳过阶段，不能绕过用户确认检查点。

## Mandatory Workflow Dispatch

在进行任何会修改项目文件、运行项目命令或调用外部服务的操作前，必须先读取 `.codex/rules/workflow-routing.md`，使用用户原始请求匹配其中的正向触发条件与排除条件。

- 命中 `Required: yes` 的工作流时，必须读取对应 `.codex/workflows/{workflow-id}/workflow.md`，创建或恢复命名 workflow state file，并通过 `.codex/scripts/todo-state.sh` 启动当前 phase 后才能执行。
- 无法判断工作流是否命中时，先请求用户确认；不得直接绕过工作流执行。
- 每次工作流新增、修改、重命名或删除后，必须运行 `.codex/scripts/sync-workflow-routing.sh`，并确保 `.codex/scripts/sync-workflow-routing.sh --check` 通过。

项目工作区默认使用 `WORKSPACE_PATH=./workspace`。不要写死 `/workspace`。最终笔记位置由用户指定；未指定时只写入项目工作区的 `output/`。

## Skill Routing

当用户请求匹配下面场景时，使用对应 Codex skill：

| Skill | Trigger |
| --- | --- |
| `research-planner` | 想学、帮我整理、研究一下、不知道从哪开始、explore topic |
| `workflow-orchestrator` | 工作流、开始学习、新建学习项目、生成状态文件 |
| `workflow-todo-state` | 可复用 workflow 状态机、命名状态文件、恢复流程、阶段状态脚本、workflow routing |
| `manifest-platform` | 统一 manifest、Agent 平台注册、工件自动发现、权限声明、版本和依赖校验 |
| `prompt-cache-optimizer` | 缓存命中优化、降低 token 成本、LLM 调用审计、提示词缓存优化 |
| `research-collector` | 收集资料、研究资料、搜集信息、资料整理、research |
| `legacy-note-importer` | 旧笔记导入、已有笔记、一堆笔记、批量整理、迁移到这个项目、按项目规范 |
| `batch-note-updater` | 批量更新旧笔记、多篇笔记过时、更新一个目录的笔记、refresh multiple notes |
| `note-beautifier` | 美化笔记、Obsidian、优化格式、beautify |
| `note-updater` | 更新旧笔记、笔记过时、refresh note、同步旧 Obsidian 笔记 |
| `moc-organizer` | 生成 MOC、整理目录、加入索引、Map of Content |
| `tool-discovery` | 可用工具、工具列表、收集工具 |
| `digest` | 记录学习、总结经验、消化、digest |

如果用户要求创建或优化 skill，使用 `skill-creator`；将跨 runtime skill 写入 canonical skills 目录（`.agent-sync/agents/*.yaml` 的 `paths.skills`，见 `.codex/platform/registry.yaml` 的 `discovery.Skill`），再由 `.agent-sync` 生成各 runtime 副本。

## Rules

执行任务时按需读取：

- `.agents/skills/{skill-name}/SKILL.md`
- `.codex/rules/common/skill-invocation.md`
- `.codex/rules/common/agent-invocation.md`
- `.codex/rules/common/git-workflow.md`
- `.codex/rules/common/env.md`
- `.codex/rules/common/token-optimization.md`
- `.codex/rules/common/sync-workflow.md`
- `.codex/rules/workflow-routing.md`
- `.codex/rules/obsidian/note-system.md`
- `.codex/rules/research-tools.md`

项目本地 hooks 使用本 runtime 的 hook 注册文件（见 `.agent-sync/agents/*.yaml` 的 `paths.hook_config`）注册，脚本放在本 runtime 的 hooks 目录。该注册文件由 `.agent-sync/bootstrap.py` 在当前机器生成；不要把本项目 hooks 写到全局配置目录；如果当前 runtime 提示信任 hook，仅信任本项目路径。

## Project Safety

- 不提交真实 `.env`、密钥、Token 或本地个人配置。
- 不硬编码用户机器绝对路径到项目产物中。
- 编辑前先检查 `git status --short`，不要覆盖用户未提交改动。
- Git 提交消息遵守 `.codex/rules/common/git-workflow.md`。

<!-- env-template:codex:begin -->
## Environment Variables

- Follow `.codex/rules/common/env.md` whenever creating, updating, migrating, or auditing `.env`, `.env.example`, or environment-variable documentation.
- Keep committed env templates minimal, project-specific, and free of real secrets or machine-local absolute paths.
- After env template changes, run `.codex/scripts/check-env-template.sh`. Use `--strict` when you want unused documented variables to fail the check.
<!-- env-template:codex:end -->

<!-- prompt-cache-bootstrap:codex:begin -->
## Prompt Cache

- Follow `.codex/rules/common/prompt-cache.md` for high-frequency prompt design.
- Keep stable instructions and output formats before dynamic user input, file excerpts, dates, IDs, and runtime state.
- Reuse canonical templates and load long context only when needed.
<!-- prompt-cache-bootstrap:codex:end -->

<!-- workflow-todo-state:start -->
## Workflow Todo State

Named workflow state files are the source of truth while a routed workflow is active.

- Workflow definitions live under `.codex/workflows/{workflow-id}/`.
- Workflow state files live under `workspace/workflow-runs/` and should be named after the task, for example `payment-refactor.workflow.md`.
- Before any action that changes project files, runs project commands, or calls external services, read `.codex/rules/workflow-routing.md` and match the user's original request against its triggers and exclusions.
- When a `Required: yes` workflow matches, read its `workflow.md`, create or resume its state file, and start the current phase before doing the work. Do not take the ordinary execution path instead.
- If the route is ambiguous, ask the user before acting.
- Read the active workflow state file before starting any phase; do not skip prerequisite phases.
- Change phase state only through `.codex/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始 {not_started}`.
- The final phase requires `quality_gate: passed`; a temporary waiver also requires an owner and due date.
- Completed run states follow the repository retention policy and do not replace changelogs or release records.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
- Each workflow directory must contain a `routing.yaml`. After creating, changing, renaming, or deleting a workflow, run `.codex/scripts/sync-workflow-routing.sh`; the update is incomplete until `.codex/scripts/sync-workflow-routing.sh --check` passes.
<!-- workflow-todo-state:end -->
