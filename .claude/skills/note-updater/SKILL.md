---
name: note-updater
description: 更新过时的既有学习笔记。用于用户说“更新这篇笔记”“这篇笔记过时了”“根据新资料刷新旧笔记”“同步到 Obsidian 旧笔记”等场景。先定位旧笔记、判断过时段落、收集最小必要新资料，再局部 patch，避免重写整篇和浪费 token。
---

# Note Updater

用于更新已有笔记，而不是从零生成新笔记。

## Inputs

必须先确认：

- `existing_note_path`: 旧笔记路径，可以在项目工作区或用户指定的 Obsidian vault 中。
- `update_goal`: 更新原因，如版本变化、概念过时、补充案例、修正错误。
- `destination_mode`: `patch-in-place`、`copy-updated` 或 `project-output-only`。
- `moc_path`: 可选，更新后同步 MOC。

## Workflow

1. **读取最小上下文**
   - 只读旧笔记的 frontmatter、目录、疑似过时段落。
   - 若用户指定具体段落，只处理该段落。
2. **生成 stale map**
   - 列出：保留、需要更新、需要删除、需要新增。
   - 不直接重写全文。
3. **最小资料收集**
   - 只搜索/读取与 stale map 对应的资料。
   - 每条资料保存 URL、日期、100-200 字摘要。
4. **局部更新**
   - 保留用户原有结构和写作风格。
   - 更新 `updated` frontmatter。
   - 追加 `## 更新记录`，记录日期和变更摘要。
   - 技术性笔记的核心概念若无通俗解释，用 insert 模式补 `[!tip] 大白话` Callout（只做加法、匹配原排版；类比库见 `.learnings/RULES.md`）。
5. **Obsidian 同步**
   - 如果目标在 vault 内，检查双链、标签、MOC。
   - 如提供 `moc_path`，调用 `moc-organizer` 同步索引。

## Output Files

默认在同目录生成：

- `update_plan.md`：过时点和更新计划
- `updated_note.md` 或直接 patch 原笔记
- `update_report.md`：更新摘要、来源、未处理风险

## Token Rules

- 不把整篇旧笔记复制进上下文，除非文件很短。
- 不重写未过时段落。
- 搜索结果只保留结构化摘要，不保存网页全文。
