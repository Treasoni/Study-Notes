---
name: batch-note-updater
description: 多篇既有学习笔记的批量更新编排。用于用户想一次更新一个目录、文件列表、Obsidian vault 子目录或多篇旧笔记，例如“批量更新这些笔记”“多篇笔记过时了”“把一组笔记更新到新版本”“refresh multiple notes”。先生成更新清单和批量计划，经用户确认后逐篇调用 note-updater 局部 patch，避免全文重写和批量误覆盖。
---

# Batch Note Updater

为多篇旧笔记做批量更新编排。本技能不直接重写每篇笔记正文；它负责筛选、排序、共享资料收集、批次控制和汇总报告，单篇内容更新必须交给 `note-updater`。

## Boundary

- 不把整目录笔记全文一次性读入上下文。
- 不直接批量覆盖原文件，除非用户明确选择 `patch-in-place` 并确认批量计划。
- 每篇笔记必须有独立 stale map、更新计划和更新报告。
- 多篇笔记共享同一更新目标时，先建立共享资料包，再让单篇 `note-updater` 只读取相关片段。
- 如果用户只是想统一格式或导入旧库，改用 `legacy-note-importer`。
- 如果用户只指定一篇笔记，改用 `note-updater`。

## Inputs

启动时确认或从用户消息中提取：

```yaml
source_path: "目录、单个文件，或文件列表"
source_scope: all | glob | selected | inventory
source_glob: "*.md"
update_goal: "更新原因，如 React 19、Python 3.14、补充最新案例"
destination_mode: patch-in-place | copy-updated | project-output-only
batch_size: 3
shared_research: auto | yes | no
moc_path: ""
stale_threshold: "可选，如 older-than:2025-01-01 或 contains:旧 API"
```

如果缺少 `source_path` 或 `update_goal`，先询问用户。未指定 `destination_mode` 时默认 `project-output-only`。

## Workflow

### Step 0: 创建批量更新项目

使用 `workflow-orchestrator` 的 `batch-note-update-flow` 创建项目目录和命名 workflow state file：

```text
${WORKSPACE_PATH:-./workspace}/{project_slug}/
```

写入 `00_batch_update_intent.md`：

```yaml
source_path:
source_scope:
source_glob:
update_goal:
destination_mode:
batch_size:
shared_research:
moc_path:
```

创建后读取 workflow state file，确认当前阶段是 `[P0]`。

### Step 1: 建立更新清单

只扫描轻量信息：frontmatter、标题、目录、更新时间、关键词命中、文件大小和路径。输出：

- `01_update_inventory.md`
- `update_inventory.csv`

CSV 字段：

```csv
id,relative_path,title,updated,status,reason,priority,size_bytes
```

`status` 可取：

- `candidate`：可能需要更新。
- `ready`：可进入更新计划。
- `needs-review`：范围不清、标题缺失、太大或结构异常。
- `skip`：不属于本次更新目标。

### Step 2: 生成批量更新计划并等待确认

输出 `02_batch_update_plan.md`，不要开始改正文。计划必须包含：

- 本次更新目标和判断依据。
- 笔记分组：按主题、版本、依赖、目录或优先级。
- 每篇笔记动作：`update`、`flag-only`、`skip`、`needs-review`。
- 是否需要共享资料包。
- 第一批处理列表，默认不超过 `batch_size`。
- 目标输出模式和覆盖风险。

用户确认前不能进入批量更新。

### Step 3: 共享资料收集（可选）

当多篇笔记使用同一更新目标，如同一框架版本、同一 API 变化时，创建：

- `shared_research/research_plan.md`
- `shared_research/source_bank.md`

资料规则：

- 只收集与 `update_goal` 相关的最小资料。
- 每条资料保留 URL、日期、适用笔记范围和 100-200 字摘要。
- 高时效或技术版本信息必须尽量使用官方文档或一手来源。
- 不保存网页全文。

如果每篇更新目标差异很大，跳过共享资料，让 `note-updater` 逐篇收集。

### Step 4: 按批次逐篇更新

每批开始前读取 workflow state file 和 `02_batch_update_plan.md`。对每篇 `update` 笔记调用 `note-updater`，传入：

```yaml
existing_note_path: "{源笔记路径}"
update_goal: "{本篇具体更新目标}"
destination_mode: "{patch-in-place | copy-updated | project-output-only}"
moc_path: "{可选}"
shared_source_bank: "shared_research/source_bank.md（如适用）"
```

每篇输出目录：

```text
updates/{note_id}/
├── stale_map.md
├── update_plan.md
├── updated_note.md
└── update_report.md
```

每批追加 `03_batch_update_log.md`：

```markdown
| 时间 | 批次 | 笔记 | 动作 | 输出 | 风险 |
| --- | --- | --- | --- | --- | --- |
```

### Step 5: 汇总与 MOC 同步

输出 `04_batch_update_report.md`：

- 更新总数、跳过数、失败数、需复核数。
- 每篇笔记的更新摘要和输出路径。
- 共享资料来源清单。
- 未处理风险和下一批建议。

如果提供 `moc_path`，调用 `moc-organizer` 更新索引项；不要把正文复制到 MOC。

## Status Rules

- 每阶段开始前读取 `${WORKFLOW_STATE_FILE}`。
- 使用 `.claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" start PN` 将当前阶段改为 `[PN] 🔲 进行中`。
- 阶段产物写完、用户确认后，使用 `.claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" complete PN` 改为 `[PN] ✅ 已完成`。
- 可选阶段不执行时，使用 `.claude/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" skip PN "原因"` 明确跳过。
- 批量更新中遇到覆盖冲突、来源不可信或更新目标不明确时，记录到异常记录并暂停该笔记。

## User-Facing Start

当用户说“批量更新多篇笔记”时，给出最短入口：

```text
给我 source_path 和 update_goal。
我会先生成更新清单和批量计划，不会直接改原文件；你确认后再按批次逐篇更新。
```
