---
name: beautify
description: 美化排版阶段。套用 Obsidian Markdown 规范，添加双链、标签、Callout 块、Mermaid 图表、YAML frontmatter 等 Obsidian 特性，优化段落长度和术语一致性。触发时机：用户审核通过 write 产出后，Phase 4。
---

# Skill: beautify（美化排版）

## 触发时机
用户审核通过 write 产出后。

## 输入
`{SYSTEM_ROOT}/2-drafts/{topic}/{topic}-笔记.md`

## 依赖技能

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| `obsidian-markdown` | Obsidian 语法规范（双链、Callout、frontmatter、标签、嵌入、Mermaid 等） | `Skill({skill: "obsidian-markdown"})` |
| `obsidian-cli` | 在 Obsidian 中创建笔记、设置属性、搜索已有笔记建立双链 | `obsidian <command>` |
| `json-canvas` | 生成知识地图 Canvas（可选） | `Skill({skill: "json-canvas"})` |
| `obsidian-bases` | 生成学习笔记索引 Base（可选） | `Skill({skill: "obsidian-bases"})` |

## 执行步骤

### Step 1: 加载语法规范

调用 `Skill({skill: "obsidian-markdown"})` 获取完整的 Obsidian Flavored Markdown 语法参考，后续步骤严格遵循其规范。

### Step 2: 检查基础 Markdown 规范
- 标题层级正确（不越级，最多 4 级）
- 统一格式（粗体、斜体、代码块标注语言）
- 段落不超过 6 行，大主题切换用 `---` 分隔
- 对比数据用表格

### Step 3: 添加 Obsidian 特性

按 `obsidian-markdown` 规范，依次添加：

#### 3a. YAML Frontmatter
```yaml
---
topic: ""
type: concept | practice | compare | cheat-sheet
difficulty: beginner | intermediate | advanced
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
concepts: []
---
```
参考 `obsidian-markdown` 的 [PROPERTIES.md](references/PROPERTIES.md) 了解全部属性类型。

#### 3b. 双链 `[[]]`

为笔记中出现的概念添加双链：
- 格式参考 `obsidian-markdown` 的 Internal Links 规范
- 优先用 `Glob **/概念名.md` 检查 vault 中是否已有对应笔记（文件系统检查，不依赖 Obsidian 运行）
- 可选：用 `obsidian-cli search query="<概念>"` 做模糊搜索辅助
- 文件存在 → `[[已有笔记]]`（使用实际文件名）
- 文件不存在 → **不创建 wikilink**，改用纯文本或标注 `[待创建: 概念名]`
- 外部链接仍用标准 Markdown `[text](url)`

#### 3c. 标签 `#tag`
根据内容添加行内标签和 frontmatter tags：
- 主题标签：`#react` `#hooks` `#frontend`
- 类型标签：`#concept` `#tutorial` `#cheatsheet`
- 难度标签：`#beginner` `#intermediate` `#advanced`
- 支持嵌套：`#topic/subtopic`

#### 3d. Callout 块
参考 `obsidian-markdown` 的 Callouts 规范，选用合适类型：
- `> [!note]` 补充说明
- `> [!warning]` 坑点/注意事项
- `> [!tip]` 最佳实践/技巧
- `> [!example]` 代码示例
- `> [!info]` 背景知识
- `> [!danger]` 严重警告
- 必要时使用折叠：`> [!note]- 点击展开`

#### 3e. Mermaid 图表
参考 `obsidian-markdown` 的 Diagrams 规范：
- 流程 → `flowchart TD`
- 序列 → `sequenceDiagram`
- 类关系 → `classDiagram`
- 节点可关联笔记：`class NodeName internal-link;`

#### 3f. 其他 Obsidian 特性（按需）
- `==高亮==` 标记关键句
- `%%注释%%` 隐藏编辑备注
- `![[嵌入]]` 引用相关笔记或图片
- `$LaTeX$` 数学公式

### Step 4: 术语统一
同一概念全文使用统一术语，不一致处修正。

### Step 5: 写入 Obsidian

用 `obsidian-cli` 将最终笔记写入目标路径：
```bash
obsidian create name="{topic}" path="{OUTPUT_PATH}/{topic}.md" content="<完整笔记内容>" silent overwrite
```
或直接写入文件后让 Obsidian 自动索引。

### Step 6 (可选): 生成知识地图

如果需要，调用 `Skill({skill: "json-canvas"})` 为该主题生成 `.canvas` 知识地图，节点为各子主题笔记，边为概念间关系。

### Step 7 (可选): 生成学习索引

如果需要，调用 `Skill({skill: "obsidian-bases"})` 为该主题创建 `.base` 索引文件，按标签/难度/类型过滤和展示相关笔记。

## 产出
写入 `{OUTPUT_PATH}/{topic}/`（或默认 `{SYSTEM_ROOT}/3-published/{topic}/`）：
- `{topic}.md`：最终格式化的 Obsidian 笔记
- `attachments/`：相关图片或文件（如果有）
- `{topic}.canvas`（可选）：知识地图
- `{topic}.base`（可选）：学习索引

## 禁止行为
- 不要修改笔记内容或含义
- 不要添加草稿中没有的信息
- 不要删除内容（只能调整呈现方式）
- 不要创建指向不存在文件的 wikilink —— 用 Glob 验证后再写
- 不要删除来源引用
- 不要硬编码 Obsidian 语法 —— 以 `obsidian-markdown` skill 为准

## 硬停止 (Hard Stop)

本阶段任务完成。向用户展示最终笔记。

**严禁调用 `/evaluate`。严禁进入 Phase 5。**
询问用户："需要修改吗？" 或 "要继续评估质量吗？"
仅当用户明确说"评估"或"继续"时才进入 Phase 5。
仅当用户说"完成"或"结束"时才结束任务。
