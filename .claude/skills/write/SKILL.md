---
name: write
description: 写笔记阶段。根据整理好的资料和用户偏好的笔记类型（概念/实战/对比/速查/心得），选择模板，提取关键信息，用学习者友好的语言生成笔记初稿。触发时机：用户审核通过 curate 产出后（研究驱动型），或用户审核通过 review 产出后（心得笔记），Phase 3。
---

# Skill: write（写笔记）

## 触发时机
- 研究驱动型笔记：用户审核通过 curate 产出后
- 心得笔记：用户审核通过 review 产出后

## 输入
- `{SYSTEM_ROOT}/1-curated/{topic}/` 中整理好的资料
- 用户偏好的笔记类型：concept / practice / compare / cheat-sheet / experience

## 执行步骤

### Step 1: 选择模板
根据笔记类型匹配模板：
- 概念笔记 → `concept-template.md`
- 实战笔记 → `practice-template.md`
- 对比笔记 → `compare-template.md`
- 速查表 → `cheat-sheet-template.md`
- 心得笔记 → `experience-template.md`

### Step 2: 提取关键信息

**研究驱动型笔记** (concept/practice/compare/cheat-sheet) — 从整理资料中读取：
- `core-concepts.md` → 定义、原理
- `practices.md` → 示例、代码、步骤
- `overview.md` → 结构、关系
- `references.md` → 来源引用

**心得笔记** (experience) — 从用户输入中读取：
- 读取 `0-inbox/{topic}/raw-input.md`（用户在 review 阶段提供的原始内容）
- 提取：背景、过程、心得、踩坑、代码示例、延伸方向
- 来源标注为 `[来源: 个人经验]`
- 如有经过 mini collect→curate 验证的补充内容，标注对应来源 `[来源: R1]`

### Step 3: 填充模板
- 用学习者友好的语言（像给同事讲解一样）
- 加入类比帮助理解
- 插入代码示例（来自源材料）
- 描述有助于理解的图表
- 内联引用来源：`[来源: R1]`

### Step 3.5: 验证 wikilink

填充模板中的 wikilink 占位符时，必须验证目标文件是否存在：
- 用 `Glob **/目标名.md` 检查 vault 中是否已有对应笔记
- 文件存在 → 填入 `[[目标名]]`
- 文件不存在 → 改用**纯文本**（不加双链括号），或标记 `[待创建: 概念名]`
- 禁止凭空编造 wikilink 指向不存在的文件

### Step 4: 生成思考题
3-5 个有深度的问题：
- 概念理解检查
- 应用场景
- 边界情况思考

### Step 5: 自检

**研究驱动型笔记：**
- 每个观点都能追溯到来源？
- 有无未覆盖的缺口？有则标记 `[待补充]`
- 难度是否匹配目标层次？

**心得笔记：**
- 用户原始内容的要点是否都已覆盖？
- 用户审核时标记的 `[待验证]` 是否已处理（验证/修正/保留）？
- 是否有未经用户批准而添加的内容？如有则删除

## 产出
写入 `{SYSTEM_ROOT}/2-drafts/{topic}/`：
- `{topic}-笔记.md`：主体笔记初稿（含 YAML frontmatter + 内联引用 + 思考题）

## 禁止行为
- 不要做美化排版（beautify 的事）
- 不要添加 curate 阶段未确认的内容
- 不要编造引用
- 不要创建指向不存在文件的 wikilink —— 先用 Glob 验证
- 不要省略来源标注
- 对于心得笔记：不要改变用户原始内容的整体结构和行文风格
- 对于心得笔记：不要添加用户未批准的外部信息

## 硬停止 (Hard Stop)

本阶段任务完成。向用户展示笔记初稿（结构、准确性、缺失内容）。

**严禁调用 `/beautify`。严禁进入 Phase 4。**
必须等待用户明确确认后才能进入 beautify。
