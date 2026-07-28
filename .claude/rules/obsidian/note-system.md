# Obsidian Note System Rules

本项目最终笔记面向 Obsidian。美化、发布、更新、MOC 都应以 Obsidian 可用性为第一目标。

## User-Specified Destination

每次创建或发布笔记前必须确认目标位置：

```yaml
vault_path: "{用户指定的 Obsidian vault 根目录}"
note_folder: "{vault 内相对目录，如 Notes/Tech/React}"
asset_folder: "{可选，附件目录，如 Assets}"
moc_path: "{可选，MOC 文件，如 Maps/React MOC.md}"
publish_mode: copy | overwrite | patch
```

不要硬编码 Obsidian vault 路径。未提供时，先把最终笔记保存在项目工作区 `output/final_note.md`，并等待用户指定。

## Obsidian Formatting

1. 使用 YAML frontmatter 管理 `title`、`tags`、`created`、`updated`、`status`、`source_project`。
2. 双链只添加高价值概念，不要把每个名词都变成链接。
3. Callout 用于结构意义，不作为装饰：
   - `[!summary]` 总结
   - `[!note]` 核心概念
   - `[!tip]` 实践建议
   - `[!warning]` 易错点
   - `[!example]` 示例
4. 代码块必须带语言标识。
5. Dataview/Bases 只在用户 vault 支持时加入；不确定时保持普通 Markdown。

## Large Note Splitting

综合型笔记超过 3000 行时应拆分为多篇独立笔记：

1. 按主题/章节拆分为独立 `.md` 文件（每篇 300-800 行）
2. 放入一个专用文件夹（如 `linux/linux常用命令/`）
3. 创建轻量索引页汇总所有子篇链接（带一句话说明）
4. 每篇添加独立 YAML frontmatter
5. MOC 中每个子篇独立一条索引项，链接路径带文件夹前缀
6. 原有的旧笔记保持不动，不混入新文件夹

## MOC Rules

MOC 是目录型笔记，不应该复制正文。每次新增或更新笔记后，只追加或更新一条索引项：

```markdown
- [[笔记标题]] - 一句话说明 #tag
```

按主题分组，保持可扫描。不要在 MOC 中写长摘要。
