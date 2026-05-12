---
name: moc
description: 扫描目录生成 Obsidian MOC（Map of Content）索引笔记，包含按子目录分组的 wikilink 列表和 Mermaid 结构图。触发时机：用户要求创建 MOC、索引文件夹、映射目录结构、或导航 Obsidian vault 中的笔记时。
---

# Skill: moc（目录索引生成）

## 触发时机

用户要求为某个目录生成 MOC、索引、目录地图时。

## 输入

- 目标目录路径（用户指定，或询问后确认）

## 执行步骤

### Step 1: 确认目标目录

- 用户已指定路径 → 直接使用
- 未指定 → 询问："要索引哪个目录？"
- 确认目录存在（`ls` 或 `find` 检查）

### Step 2: 扫描目录

用 `find` 递归扫描目标目录下所有 `.md` 文件：

**排除规则（必须）：**
1. **隐藏目录/文件**：忽略所有以 `.` 开头的路径（`.obsidian`、`.git`、`.claude`、`.learnings` 等）
2. **已有 MOC 文件**：跳过文件名以 `MOC.md` 结尾或名为 `_index.md` 的文件
3. 使用 `find {dir} -not -path '*/\.*' -name '*.md'` 获取文件列表

**分组规则：**
- 按文件相对于目标目录的第一级子目录分组
- 直接在目标目录根下的文件归入 `根目录` 组

**元数据提取：**
- 标题：读取每个文件的前 5 行，提取第一个 `# ` 开头的标题；无 H1 则用文件名（不含扩展名）
- Tags：读取 YAML frontmatter 中的 `tags` 字段

### Step 3: 构建 MOC 内容

按以下顺序生成内容：

**3a. YAML frontmatter**
```yaml
---
title: "{目录名} MOC"
tags: [moc]
created: {当前日期}
updated: {当前日期}
---
```

**3b. `## 目录结构`** — Mermaid 图表

| 笔记总数 | 图表策略 |
|----------|----------|
| ≤15 | 画出完整层级：目录 → 子目录 → 具体笔记节点。对笔记节点应用 `class NodeName internal-link;` 使其可点击。 |
| >15 | **降维**：仅画出目录和子目录节点及其关系，不画具体笔记节点。避免 50+ 节点的"面条图"。 |

```mermaid
graph TD
    Root[{目录名}]
    Root --> SubA[子目录A]
    Root --> SubB[子目录B]
    SubA --> Note1[笔记1]
    SubA --> Note2[笔记2]
    class Note1,Note2 internal-link;
```

**3c. `## 笔记索引`** — 按组列出

```markdown
### {组名}
- [[笔记标题]] #tag1 #tag2
- [[另一篇笔记]]
```

- 用文件名（不含 `.md`）作为 wikilink 显示文本
- 若有 frontmatter tags，以 inline `#tag` 形式追加在链接后

**3d. `## 概览`**

```markdown
- 📂 目录：`{path}`
- 📝 笔记总数：{N}
- 📁 子目录数：{M}
- 📅 生成日期：{YYYY-MM-DD}
```

### Step 4: 写入文件

- 路径：`{target_dir}/{dir_name} MOC.md`
- 使用 Obsidian Markdown 规范（wikilink、frontmatter、Mermaid）

## 产出

- 目标目录下的 `{目录名} MOC.md` 索引文件

## /update 联动

当用户在已有 MOC 上执行 `/update --mode refresh` 时：
- 重新扫描目录
- 刷新 笔记索引 列表（新增/移除变更的笔记）
- 若笔记数跨越 15 阈值，同步更新 Mermaid 图表策略
- 更新 frontmatter `updated` 字段

## 禁止行为

- 不要扫描隐藏目录（`.` 开头）
- 不要把生成的 MOC 文件列入自己的索引
- 不要移动或重命名任何笔记文件
- 不要对 >15 篇笔记的目录绘制完整 Mermaid 节点图
