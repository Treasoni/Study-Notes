
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
| `dataviz` | 创建图表、图形、仪表盘等数据可视化 | chart、graph、plot、数据可视化、dashboard |
| `excalidraw-diagram` | 生成 Excalidraw 流程图、思维导图、架构图 | 画图、流程图、思维导图、Excalidraw、可视化、diagram |
| `json-canvas` | 生成 JSON Canvas 格式的可视化画布 | canvas、画布、JSON Canvas |

#### 资料研究

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `research-collector` | 使用多策略进行高效资料收集：Fork Subagent 隔离收集、两阶段粗筛+精读、格式约束优化 token 消耗、本地缓存复用。 | 收集资料、研究资料、搜集信息、资料整理、research、gather information、collect资料 |
| `research-planner` | 学习笔记需求澄清与引导。分析用户学习需求，引导明确学习目标和方向，调用 workflow-orchestrator 生成项目结构。 | 想学、帮我整理、研究一下、了解一下、不知道从哪开始、research planning、explore topic |
| `deep-research` | 多渠道深度研究，多源验证并生成带引用报告 | 深度研究、研究报告、deep research、全面研究 |

#### 学习笔记工作流

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `batch-note-updater` | 多篇既有学习笔记的批量更新编排。用于用户想一次更新一个目录、文件列表、Obsidian vault 子目录或多篇旧笔记 | 批量更新这些笔记、多篇笔记过时了、把一组笔记更新到新版本、refresh multiple notes |
| `note-updater` | 更新过时的既有学习笔记。用于用户说“更新这篇笔记”“这篇笔记过时了”“根据新资料刷新旧笔记”“同步到 Obsidian 旧笔记”等场景。先定位旧笔记、判断… | 更新这篇笔记、这篇笔记过时了、根据新资料刷新旧笔记、同步到 Obsidian 旧笔记 |
| `workflow-orchestrator` | 工作流编排器。由各 planner 技能调用，接收工作流名称和参数，从模板生成 todo.md。不直接面向用户。 | 工作流编排器 |
| `note-assembler` | 将章节组装成完整笔记（由 agent 调用） | 组装、合并章节、收尾、拼装、assemble |

#### 内容提取

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `defuddle` | 从网页提取正文内容 | 提取网页、网页正文、defuddle |

#### 工具发现

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `tool-discovery` | 查看当前环境中可用于资料收集的工具，包括内置工具、MCP 工具和已安装的 skills。当用户想了解有哪些工具可以用来搜索、提取、分析资料时使用此技能。 | 可用工具、有哪些工具、工具列表、收集工具、search tools、available tools |

#### 自我学习

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `digest` | 自我学习阶段。回顾本次会话，记录真实发生的学习点和错误到 .learnings/； | 自我学习阶段 |
| `maintain-learnings` | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则失效问题聚类诊断，追溯并修改对应 skill、模板、hook、校验脚本或项目规则； | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则… |

#### Obsidian 相关

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `legacy-note-importer` | 旧笔记批量导入、盘点和规范化。用于用户已经有一堆 Markdown/Obsidian/零散学习笔记 | 旧笔记导入、已有笔记、一堆笔记、批量整理、迁移到这个项目、按项目规范、import existing notes、normalize notes |
| `moc-organizer` | 为 Obsidian 生成或更新 MOC（Map of Content）目录笔记。 | 生成 MOC、整理目录、把新笔记加入目录、每次加入笔记自动更新索引 |
| `note-beautifier` | Obsidian 笔记智能美化与发布。用于将最终学习笔记处理成 Obsidian Markdown，补 frontmatter、标签、Callout、双链 | 美化、Obsidian、优化格式、笔记美化、发布到 vault、beautify |

#### 未分类

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `skill-creator` | Create new skills, modify and improve existing skills | Create new skills, modify and improve ex… |

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
