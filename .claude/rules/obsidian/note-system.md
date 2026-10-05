# Obsidian Note System Rules

本项目最终笔记面向 Obsidian。美化、发布、更新、MOC 都应以 Obsidian 可用性为第一目标。

> 本文件只管**格式**（frontmatter、标签、Callout、双链、MOC）。**内容可读性**标准见 `note-style.md`（小白友好写作契约，入门优先 + 参考类豁免），产出或改写笔记内容的环节必须同时遵守。

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
6. Callout 内要放表格或分多段时，**中间每个空行也必须写成 `>`**：裸空行会终止 callout，
   其后的表格 / 段落掉出框外、渲染散架。这与「表格不嵌进列表项」同类——都是**合法 Markdown
   却渲染异常**的形态，内容校验（引文 / 副本一致性）查不到，必须单独跑结构自检
   （`.claude/scripts/check-md-structure.py`，见 `note-beautifier` Step 4）。**生成阶段**就要写对，
   不要留到美化阶段回改。

## 引文语言（所有笔记的默认要求）

笔记正文里的**成句英文引文一律给中译**——用户明确要求「那个英文我不是很想看，我更想直接看中文」，
并定为**生成笔记时的默认**。分界：**代码、命令、配置键、路径、文件名、产品名、单个技术术语保留原文**，
只译成句的英文引文。

逐字原文随后必须留档：每章（或每个分节）末尾加「引文对照（原文 / 中译 / 出处）」表。
只译不留档等于剪断引用链，读者再也无法回源核对。「出处」列**宁空不猜**——查不到就写 `—`，
并在表前引导句里说明 `—` 的含义；正文里列举的**产品文件名**不是来源件，标成出处会让读者去查错文件。

这是**生成阶段**的要求，不要留到美化阶段再回改；美化阶段对应的条目是验收（多份副本逐字比对、
撞车与边界叠字复扫），见 `note-beautifier` 的 Step 4 清单。

## MOC Rules

MOC 是目录型笔记，不应该复制正文。每次新增或更新笔记后，只追加或更新一条索引项：

```markdown
- [[笔记标题]] - 一句话说明 #tag
```

按主题分组，保持可扫描。不要在 MOC 中写长摘要。
