---
title: Claude Code 技能过滤机制设计
date: 2026-06-02
tags:
  - AI工作流
  - ClaudeCode
  - Token优化
  - 架构设计
type: experience
---

# Claude Code 技能过滤机制设计

## 背景

在 Claude Code 工作流项目中，用于"开发/调试"的 skills 与"项目核心逻辑"（如学习、解题）的 skills 混杂在一起。主 Agent 在 Resource Discovery 阶段会把所有 skill 加载进上下文，导致：

- **Token 严重浪费**：消耗大量不必要的输入 Token。
- **Context Window 污染**：增加了大模型产生"幻觉"或执行偏离核心任务的概率。

> [!info] 现状备注
> `StudySystem` 已通过 [[.study-config.yaml]] 中的 `skills.mode: project | dev | all` 实现粗粒度过滤，但**目录范围匹配、Glob 通配符、公共池机制**均未支持。

## 踩坑

> [!warning] 坑点
> **现象**：每次 Resource Discovery 都把 dev / project 两类 skill 全部加载，LLM 上下文被"调试用脚本"和"解题用 skill"挤满。
> **原因**：现有 [[.study-config.yaml]] 的 `skills.mode` 只做整体模式开关，没有细粒度的"按文件 / 按目录"过滤能力；通配符与公共池机制也都缺失。
> **解决**：在 `.skill.yaml` 中新增配置项，主 Agent 在 Resource Discovery 阶段读取文件内容之前，根据配置的运行模式过滤 skill 列表。详见下文。

## 过程

### 核心思路：基于 YAML 的预过滤机制

在 `.skill.yaml` 中新增配置项，主 Agent 在 Resource Discovery 阶段读取文件内容之前，根据配置的运行模式过滤 skill 列表。

### 核心优势

- **精确阻击 Token 浪费**：在文件读取前进行拦截，真正实现降本。
- **零迁移成本**：不移动现有的 Skill 文件，不破坏原本的 Obsidian 链接或硬编码路径。
- **配置驱动**：灵活性高，可随时按需调整。

### 配置文件设计 (.skill.yaml)

建议将 Agent 的状态划分为不同模式（如 `dev` 和 `project`），并引入 `common` 公共池存放通用技能（如基础文件操作、Markdown 格式化规范）。

```yaml
# .skill.yaml 配置示例（文件名均为示意占位，不代表真实 skill）
current_mode: "project" # 运行模式切换：dev | project

skills:
  # 1. 公共技能：无论什么模式都加载
  common:
    - "core_file_ops.md"      # 示意占位
    - "standard_format.md"    # 示意占位

  # 2. 开发模式：用于调试、Prompt 调优、MCP 开发
  dev:
    - "mcp_debug.md"          # 示意占位
    - "dev_*.md"              # 建议支持 Glob 通配符，靠前缀区分
    - "scripts/**/*.md"       # 建议支持按目录范围匹配

  # 3. 生产/项目模式：核心业务流程（如考研学习流程）
  project:
    - "math_solver.md"        # 示意占位
    - "circuit_analysis.md"   # 示意占位
    - "todo_state_machine.md" # 示意占位
```

### 实现与优化建议

- 支持 **Glob 通配符**
- 主 Agent 读取逻辑：解析 YAML 规则 → 展开为具体 File List → 去重 → 提交给 LLM。这样可以避免每次新增 Skill 都需要修改配置文件。

## 心得

- "零迁移成本"是这个方案最值得保留的特质 —— 现有 [[CLAUDE.md]] 中已经描述的 Skill Filtering 流程、Obsidian 链接、硬编码路径都不需要动，只在文件读取前多一层过滤。
- "公共池 + 模式池"是两层结构：先合并 `common` 与当前模式对应的列表，再做去重，逻辑清晰且天然支持未来新增模式（如 `test`、`staging`）。
- 把过滤前移到"读取文件之前"是关键：如果只是过滤"加载到 prompt 的 skill 列表"，底层文件读取仍会消耗 token，等于没省。

## 代码/示例

完整 YAML 配置见上文"配置文件设计"一节。下方给出一个最小可运行读法的伪代码，对应主 Agent 读取逻辑：

```text
# 1. 读 .skill.yaml → 得到 current_mode + skills.{common, dev, project, ...}
# 2. 选池：pool = skills.common + skills[current_mode]
# 3. 展开通配符：把 "dev_*.md"、"scripts/**/*.md" 替换为真实文件列表
# 4. 去重：保留首次出现顺序
# 5. 把最终 File List 提交给 LLM
```

## 延伸

- 还想深入了解：
  - `skills.mode` 与 `current_mode` 的关系：前者是 [[.study-config.yaml]] 层面的总开关，后者是 `.skill.yaml` 内的运行时模式，是否需要二者协同？
  - 公共池是否也支持通配符？还是只允许显式列文件？
- 下一步计划：
  - 在 [[CLAUDE.md]] 的 Resource Discovery 章节里把"读取 .skill.yaml → 过滤 → 读文件"流程补完整。
  - 参考 [docs/todo-state-machine.md](docs/todo-state-machine.md) 的 Phase Gate 思路，给 skill 加载也设计一个"未通过过滤就不进入 Resource Discovery"的硬性 Gate。
  - 跑一轮对比实验：开启过滤前后，Resource Discovery 阶段实际消耗的 token 数与 LLM 行为偏差率。
- 相关笔记：
  - [[.study-config.yaml]]（现有 `skills.mode` 配置）
  - [[CLAUDE.md]]（Skill Filtering 章节）
