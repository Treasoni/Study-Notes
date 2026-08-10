# cdx05 更新报告：Agents 与 MCP

## 概览

- **源文件**：`AI学习/Codex/05 Agents 与 MCP.md`
- **目标文件**：`AI学习/Codex/03-进阶应用/Agents 与 MCP.md`（已写入）
- **处理方式**：patch-in-place（重构既有笔记，非新建）
- **日期**：2026-08-10

## 变更内容

1. **标题与编号**：去掉书籍章号前缀（`第五章：Agents 子代理与 MCP 服务配置`），标题改为 `Agents 与 MCP`；旧 `### Part N` / `#### N.M` 编号子节全部转为 `##` / `###` 两级标题（Part 1 → `## Agents 子代理系统`、Part 2 → `## MCP 服务配置`）。
2. **Frontmatter**：`title` 改为 `Agents 与 MCP`；`tags` 改为 `[codex, ai, 工具使用, 进阶应用, agents, mcp]`；`created` 保持 `2026-07-31`；`updated` 改为 `2026-08-10`；`status` 改为 `updated`；`source_project` 保持 `codex-config`。
3. **新增教程风格章节**：`> [!info] 文档定位`（紧随 H1）；`## 常见问题`（3 个 Q&A：Agent vs Skill、审批模式选择、STDIO vs Streamable HTTP）；`## 最佳实践`（Do's / Don'ts）；`## 相关文档` 表格；`## 参考资料`（官方链接）；`## 更新记录`。
4. **删除旧导航**：移除 `> [!note] 导航` 章回导航块，替换为 `## 相关文档` 表格（4 个参数指定的 wikilink）。
5. **Callout 规范化**：原文内嵌引用块格式化为 Obsidian Callout，正文未改：
   - `> **一句话总结**` → `> [!note] 一句话总结`
   - `> **本章小结**` → 独立 `## 小结` 章节
6. **布局**：大型主题以 `---` 分隔；全文仅使用 `##` / `###` 两级标题；`> [!info] 文档定位` 紧随 H1。

## 内容保全

所有实质性技术内容完整保留，未删改、未改写：
- 全部代码块（代理配置路径、`code-explorer.toml` 完整示例、`[agents]` 全局设置、MCP `[mcp_servers.*]` 配置位置、STDIO 本地进程示例、Streamable HTTP 远程 API 示例、工具白名单/黑名单示例、`codex mcp add` 命令）。
- 全部表格（代理字段表、三种内置代理表、Codex vs Claude Code Agents 对比表、审批模式表、Codex vs Claude Code MCP 对比表）。
- 全部 Callout / 引用块正文（含"一句话总结""本章小结"全文，后者并入 `## 小结`）。

## 新增内容来源

FAQ、最佳实践、小结均从原文事实提炼，未引入新技术事实；相关文档双链仅使用参数指定的 4 个文件名（`[[Skills 技能系统]]`、`[[Hooks 与插件]]`、`[[config.toml 核心配置]]`、`[[Codex MOC]]`）；参考资料仅使用官方 Codex 链接（OpenAI Codex 文档、OpenAI Codex GitHub）。

## 产物文件

- `workspace/codex-config-update/updates/cdx05/stale_map.md`
- `workspace/codex-config-update/updates/cdx05/updated_note.md`
- `workspace/codex-config-update/updates/cdx05/update_report.md`
- `AI学习/Codex/03-进阶应用/Agents 与 MCP.md`（目标 vault 文件，patch-in-place 写入）
