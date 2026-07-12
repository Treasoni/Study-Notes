
# 技能调用指南

当用户请求涉及技能（skill）领域时，优先调用对应技能，而非自行实现。

## 核心原则

1. **技能优先**：用户请求匹配到已有技能时，必须通过 `Skill` 工具调用，不要手动实现技能已覆盖的功能
2. **精准匹配**：根据用户意图和触发词选择最合适的技能，避免误触发或漏触发
3. **不要猜测**：不确定是否有对应技能时，查阅下方技能列表再决定
4. **单一技能**：每次调用一个技能；如需多个技能协作，按顺序逐个调用

## Obsidian 说明

本项目不依赖全局 Obsidian plugin skills。Obsidian 相关能力由项目本地规则和 skills 承担：

- `note-beautifier`：处理 Obsidian Markdown、frontmatter、标签、Callout、双链和发布位置。
- `legacy-note-importer`：处理已有旧笔记的批量盘点、迁移计划和规范化入口。
- `batch-note-updater`：处理多篇旧笔记的批量更新计划、批次编排和逐篇 note-updater 调用。
- `moc-organizer`：生成或更新 MOC 目录笔记。
- `.claude/rules/obsidian/note-system.md`：Obsidian 输出规范。

## 技能列表

#### 图表与可视化

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `excalidraw-diagram` | 生成 Excalidraw 流程图、思维导图、架构图 | 画图、流程图、思维导图、Excalidraw、可视化、diagram |
| `json-canvas` | 生成 JSON Canvas 格式的可视化画布 | canvas、画布、JSON Canvas |

#### Obsidian 相关（项目本地）

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `legacy-note-importer` | 旧笔记批量导入、盘点、迁移到本项目规范 | 旧笔记导入、已有笔记、一堆笔记、批量整理、迁移到这个项目、import existing notes |
| `batch-note-updater` | 多篇旧笔记批量更新和逐篇局部 patch 编排 | 批量更新旧笔记、多篇笔记过时、更新一个目录的笔记、refresh multiple notes |
| `note-beautifier` | 处理 Obsidian Markdown 与发布位置 | Obsidian、wikilink、双链、Callout、美化、发布 |
| `moc-organizer` | 生成或更新 MOC 目录笔记 | MOC、目录、索引、Map of Content |
#### 资料研究

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `research-planner` | 资料收集前的需求澄清与引导 | 想学、帮我整理、研究一下、了解一下、不知道从哪开始、帮我看看、research planning、explore topic |
| `research-collector` | 多策略高效资料收集 | 收集资料、研究资料、搜集信息、资料整理、research、gather information、collect资料 |

#### 学习笔记工作流

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `workflow-orchestrator` | 工作流编排器，选择工作流模板并生成 todo.md | 工作流、流程、开始学习、新建项目、workflow、orchestrator |
| `workflow-todo-state` | 为多阶段 agent 项目创建或改造可恢复的 todo.md 状态机 | 可复用 todo、状态机、恢复流程、阶段状态、其他项目复用 workflow todo |
| `legacy-note-importer` | 将已有一批旧笔记接入项目工作流并按规范处理 | 旧笔记、已有笔记、一堆笔记、批量导入、normalize notes |
| `batch-note-updater` | 将多篇既有笔记按批次更新，逐篇调用 note-updater | 批量更新、多篇笔记、旧笔记过时、refresh multiple notes |
| `note-assembler` | 将章节组装成完整笔记（由 agent 调用） | 组装、合并章节、收尾、拼装、assemble |
| `note-beautifier` | Obsidian 笔记智能美化专家 | 美化、Obsidian、优化格式、笔记美化、beautify |
| `note-updater` | 更新已有过时笔记 | 更新旧笔记、过时、refresh、update |
| `moc-organizer` | 同步 MOC 目录 | MOC、目录、索引、整理 |


#### 内容提取

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `defuddle` | 从网页提取正文内容 | 提取网页、网页正文、defuddle |

#### 工具发现

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `tool-discovery` | 查看可用的资料收集工具 | 可用工具、有哪些工具、工具列表、收集工具、search tools |

#### 自我学习

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `digest` | 回顾会话，记录学习心得和错误，压缩去重 | 记录学习、总结经验、记录心得、消化、digest |

#### 开发工具

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `skill-creator` | 创建新的 Claude Code 技能 | 创建 skill、新技能、写一个 skill |

### 1. 分析意图

- 用户想做什么？（创建、读取、修改、删除、转换）
- 涉及什么文件类型？（.pdf、.docx、.xlsx、.md）
- 是否属于特定平台？（Obsidian、Excalidraw）

### 2. 匹配技能

- 优先匹配**最具体**的技能
- 触发词可能出现在用户消息的任何位置
- 中英文触发词同等对待


### 错误处理

- 技能调用失败时，向用户说明原因并建议替代方案
- 不要静默失败，明确告知用户发生了什么
- 如果技能不支持某个操作，如实告知而非强行实现
