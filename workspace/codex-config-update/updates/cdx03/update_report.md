# cdx03 更新报告：AGENTS.md 分层体系

## 概览

- **源文件**：`AI学习/Codex/03 AGENTS.md 分层体系.md`
- **目标文件**：`AI学习/Codex/03-进阶应用/AGENTS.md 分层体系.md`（已写入）
- **处理方式**：patch-in-place（重构既有笔记，非新建）
- **日期**：2026-08-10

## 变更内容

1. **标题与编号**：去掉书籍章号前缀（`第三章：指令与规则`），标题改为 `AGENTS.md 分层体系`；旧 `### N.` / `#### N.M` 编号子节全部转为 `##` / `###` 两级标题。
2. **Frontmatter**：`title` 改为 `AGENTS.md 分层体系`；`tags` 改为 `[codex, ai, 工具使用, 进阶应用, 指令]`；`created` 保持 `2026-07-31`；`updated` 改为 `2026-08-10`；`status` 改为 `updated`；`source_project` 保持 `codex-config`。
3. **新增教程风格章节**：`> [!info] 文档定位`（紧随 H1）；`## 常见问题`（3 个 Q&A）；`## 最佳实践`（Do's / Don'ts）；`## 相关文档` 表格；`## 参考资料`（官方链接）；`## 更新记录`。
4. **删除旧导航**：移除 `> [!note] 导航` 章回导航块，替换为 `## 相关文档` 表格。
5. **Callout 规范化**：原文内嵌引用块格式化为 Obsidian Callout，正文未改：
   - `> **Claude Code 对照**` → `> [!note] Claude Code 对照`
   - `> **区分建议**` → `> [!note] 区分建议`
   - `> **核心差异一句话总结**` → `> [!note] 核心差异一句话总结`
   - `> **本章小结**` → 独立 `## 小结` 章节
6. **布局**：大型主题以 `---` 分隔；全文仅使用 `##` / `###` 两级标题。

## 内容保全

所有实质性技术内容完整保留，未删改、未改写：
- 全部代码块（发现路径、根到叶拼接图、fallback 查找图、容量分层树、`.codex/rules/` 目录树、Code Review Rules / Working Agreements 示例、Starlark `safety.rules` 完整示例、`codex status` / `codex --cd` 验证命令）。
- 全部表格（文件优先级、操作类型 allow/prompt/forbidden、Codex vs Claude Code 规则对比）。
- 全部 Callout 正文。

## 新增内容来源

FAQ、最佳实践、小结均从原文事实提炼，未引入新技术事实；相关文档双链仅使用参数指定的 4 个文件名；参考资料仅使用官方 Codex 链接。

## 产物文件

- `workspace/codex-config-update/updates/cdx03/stale_map.md`
- `workspace/codex-config-update/updates/cdx03/updated_note.md`
- `workspace/codex-config-update/updates/cdx03/update_report.md`
- `AI学习/Codex/03-进阶应用/AGENTS.md 分层体系.md`（目标 vault 文件，patch-in-place 写入）
