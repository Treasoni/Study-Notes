---
name: note-starter
description: 启动新主题学习笔记。用于用户说“开始写笔记”“启动写笔记”“创建学习笔记”或明确想为新主题建立学习笔记时。检查可恢复运行后，委派给 research-planner 初始化 learning-note-flow；不用于旧笔记导入或更新。
---

# Note Starter

为新主题学习笔记提供唯一入口；复用已有 planner 和 workflow，不重复它们的职责。

## 输入

- 必填：学习主题。
- 可选：学习深度、已有基础、笔记目的、输出位置、`vault_path`、`note_folder`、`moc_path`。

## 流程

1. 没有主题时，只询问用户要学习的主题；不要创建文件或开始研究。
2. 若用户要导入旧笔记、更新单篇旧笔记或批量更新，分别转交 `legacy-note-importer`、`note-updater` 或 `batch-note-updater`，不要初始化新主题工作流。
3. 在任何状态变更前读取 `.codex/rules/workflow-routing.md`，确认请求命中 `learning-note-flow`。
4. 按 `workflow-orchestrator` 的小写连字符规则派生 `run_id`，检查 `workspace/workflow-runs/{run_id}.workflow.md`。
5. 状态文件已存在时，报告其路径并恢复当前阶段；绝不覆盖或新建重复运行。
6. 状态文件不存在时，将主题和所有已提供的可选信息交给 `research-planner`。由它澄清缺失信息、调用 `workflow-orchestrator`，并在阶段 0 的用户确认点停止。

## 边界

- 不自行收集资料、生成大纲、写正文、发布到 Obsidian 或更新 MOC。
- 不手动创建 workflow state、推进阶段状态或跳过用户确认。
