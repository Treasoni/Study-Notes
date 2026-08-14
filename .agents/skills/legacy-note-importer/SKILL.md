---
name: legacy-note-importer
description: 旧笔记批量导入、盘点和规范化。用于用户已经有一堆 Markdown/Obsidian/零散学习笔记，想接入本项目工作区、按项目 Obsidian 规范补 frontmatter、标签、双链、Callout、MOC，并保留原始文件时使用。触发词：旧笔记导入、已有笔记、一堆笔记、批量整理、迁移到这个项目、按项目规范、import existing notes、normalize notes。
---

# Legacy Note Importer

把用户已有的一批笔记接入 Study System。此技能不从零研究主题，而是先盘点旧笔记，再生成迁移计划，按批次规范化为本项目可管理的 Obsidian Markdown。

## Boundary

- 保留原始笔记，不直接覆盖，除非用户明确选择 `overwrite` 或 `patch-in-place`。
- 默认只处理 Markdown：`.md`、`.markdown`。其他格式先列入清单并询问是否转换。
- 格式规范化交给 `note-beautifier`；内容过时修订交给 `note-updater`；目录索引交给 `moc-organizer`。
- 不把整个笔记库一次性读进上下文。先生成 inventory，再按批次读取和处理。
- 发布到 Obsidian 前必须确认 `vault_path`、`note_folder`、`asset_folder`、`moc_path`、`publish_mode`。

## Inputs

启动时确认或从用户消息中提取：

```yaml
source_path: "旧笔记目录或单个文件"
source_scope: all | glob | selected
source_glob: "*.md"
workspace_project: "默认 ./workspace/{project_slug}"
destination_mode: project-output-only | copy-to-vault | patch-in-place
vault_path: ""
note_folder: ""
asset_folder: ""
moc_path: ""
publish_mode: copy | overwrite | patch
stale_policy: skip | flag-only | update-with-note-updater
batch_size: 5
```

如果缺少 `source_path`，先询问用户给出旧笔记目录或文件路径。若缺少发布位置，先输出到项目工作区，不写入 vault。

## Workflow

### Step 0: 创建导入项目

使用 `workflow-orchestrator` 的 `legacy-note-import-flow` 创建项目目录和命名 workflow state file：

```text
${WORKSPACE_PATH:-./workspace}/{project_slug}/
```

写入 `00_import_intent.md`，记录来源、目标、发布策略、批处理大小和是否允许更新旧内容。创建后读取 workflow state file，确认当前阶段是 `[P0]`。

### Step 1: 生成旧笔记清单

只扫描文件名、相对路径、大小、修改时间和 Markdown 标题，不读取全文。输出：

- `01_inventory.md`：按主题、目录、状态分组的人类可读清单。
- `inventory.csv`：机器可读清单。

清单字段：

```csv
id,relative_path,title,heading_count,has_frontmatter,has_tags,has_wikilinks,has_callouts,size_bytes,mtime,status
```

`status` 可取：

- `ready`：可直接规范化。
- `needs-review`：标题缺失、结构混乱、疑似重复或格式异常。
- `non-markdown`：暂不处理，等待用户确认转换策略。
- `skip`：用户排除或明显不属于学习笔记。

### Step 2: 生成迁移计划并等待确认

根据清单输出 `02_migration_plan.md`，不要开始改文件。计划必须包含：

- 分组策略：按主题、课程、项目、日期或原目录。
- 每篇笔记的动作：`normalize`、`update`、`merge`、`split`、`skip`。
- 目标位置：项目 `normalized/`，或用户指定 vault 目录。
- 风险项：重复标题、破损链接、附件缺失、超大文件、非 Markdown 文件。
- 第一批建议处理列表，默认不超过 `batch_size`。

在用户确认计划前，不进入批量改写。

### Step 3: 按批次规范化

每批读取 workflow state file 和 `02_migration_plan.md`，只处理本批文件。对每篇 `normalize` 笔记：

1. 读取原文。
2. 应用 `.codex/rules/obsidian/note-system.md`。
3. 补齐 YAML frontmatter：`title`、`tags`、`created`、`updated`、`status`、`source_project`、`source_note_path`。
4. 只添加高价值双链，不把普通名词全部链接化。
5. 用 Callout 表达结构意义：总结、核心概念、实践建议、易错点、示例。
6. 代码块补语言；不确定语言时标为 `text`。
7. 输出到 `normalized/{safe-title}.md` 或用户确认的 vault 目标。

每批追加 `03_batch_log.md`：

```markdown
| 时间 | 原文件 | 输出文件 | 动作 | 风险 | 备注 |
| --- | --- | --- | --- | --- | --- |
```

### Step 4: 处理过时或冲突笔记

对计划中标为 `update` 的笔记，不在本技能内重写内容。逐篇调用 `note-updater`，并传入：

```yaml
existing_note_path: "源笔记或规范化后笔记"
update_goal: "迁移盘点发现的过时点"
destination_mode: "copy-updated 或 patch-in-place"
moc_path: "{可选}"
```

对 `merge` 或 `split`，先生成小范围建议并等待用户确认，再执行。

### Step 5: 发布与 MOC

如果用户提供 vault 目标：

- `copy`：复制规范化结果到 vault，不覆盖同名文件。
- `overwrite`：覆盖前列出将被覆盖文件并等待确认。
- `patch`：尽量保留目标笔记已有本地修改，只补项目规范缺失项。

如果提供 `moc_path`，调用 `moc-organizer`，只写索引项：

```markdown
- [[笔记标题]] - 一句话说明 #tag
```

最后输出 `04_import_report.md`，包含数量统计、跳过原因、风险、后续建议。

## Status Rules

- 每阶段开始前读取 `${WORKFLOW_STATE_FILE}`。
- 使用 `.codex/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" start PN` 将当前阶段改为 `[PN] 🔲 进行中`。
- 阶段产物写完、用户确认后，使用 `.codex/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" complete PN` 改为 `[PN] ✅ 已完成`。
- 可选阶段不执行时，使用 `.codex/scripts/todo-state.sh "${WORKFLOW_STATE_FILE}" skip PN "原因"` 明确跳过。
- 出现不确定覆盖、重复标题、大量破损链接时，记录到 workflow state file 异常记录并停在当前阶段。

## User-Facing Start

当用户问“我有一堆旧笔记怎么用这个项目”时，给出最短可执行入口：

```text
把旧笔记目录给我，例如 source_path=/path/to/notes。
我会先生成 inventory 和迁移计划，不会改原文件；你确认后再按批次规范化。
```
