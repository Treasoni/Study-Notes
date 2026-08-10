# cdx09 更新报告：快速参考卡片

> 运行：codex-config-update / 批次 3 / cdx09
> 日期：2026-08-10
> 模式：patch-in-place（就地重构）

## 1. 变更概览

- **旧路径**：`AI学习/Codex/附录 快速参考卡片.md`
- **新路径**：`AI学习/Codex/04-高级功能/快速参考卡片.md`
- **标题**：`Codex 完整配置体系` → `快速参考卡片`
- **标签**：`[codex, claude-code, configuration]` → `[codex, ai, 工具使用, 高级功能, 速查]`
- **状态**：`completed` → `updated`；`updated` 字段更新为 `2026-08-10`

## 2. 结构调整

1. **Frontmatter**：标题、标签、状态、更新时间套用 Claude Code 教程模板；`created: 2026-07-31`、`source_project: codex-config` 保留。
2. **标题层级**：`# 附录：快速参考卡片` → `# 快速参考卡片`；原 `###` 速查小节提升为 `##` 独立主题分节。
3. **文档定位**：H1 后新增 `> [!info] 文档定位` callout，定位为速查卡片。
4. **分节规范**：大主题用 `---` 分隔，仅保留 `##` / `###` 两级。
5. **新增教程区块**：常见问题（3 条 Q&A）、最佳实践（Do's/Don'ts）、小结、相关文档表格、参考资料、更新记录。
6. **移除旧导航**：`> [!note] 导航` 章节导航块替换为「相关文档」wikilink 表格；文末出版说明块移除，发布日期信息并入 frontmatter 与更新记录。

## 3. 内容保留

- 三张速查表**逐行原样保留**：配置文件路径速查（11 行）、常用 CLI 命令速记（11 行）、关键配置项默认值一览（13 行）。
- 全部行内代码、`—` 占位符、表格列头与分隔线均未改动。
- 未新增任何超出原文的技术事实；新增 FAQ / 最佳实践 / 小结全部由原文三张表提炼。

## 4. 新增内容来源

| 新增区块 | 来源 |
|----------|------|
| 常见问题 Q1 | 配置文件路径速查表（Codex vs Claude Code 对应关系） |
| 常见问题 Q2 | 常用 CLI 命令速记表（`codex -c key=val`、`codex --profile NAME`） |
| 常见问题 Q3 | 关键配置项默认值一览表（sandbox/approval/agents/MCP 默认值） |
| 最佳实践 Do's | `--profile`、`-c key=val`、`--cd`、`codex mcp add`、`/config` 等命令 |
| 最佳实践 Don'ts | 路径速查表与默认值表的安全/性能注意点 |
| 小结 | 精炼三张速查表的定位 |

## 5. 相关文档链接

- `[[Codex CLI 与调试]]`
- `[[config.toml 核心配置]]`
- `[[对照表与迁移实战]]`
- `[[Codex MOC]]`

## 6. 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

## 7. 输出文件

| 文件 | 说明 |
|------|------|
| `workspace/codex-config-update/updates/cdx09/stale_map.md` | 旧结构 → 新结构映射表 |
| `workspace/codex-config-update/updates/cdx09/updated_note.md` | 完整新笔记正文 |
| `AI学习/Codex/04-高级功能/快速参考卡片.md` | 已写入 vault 目标路径 |
