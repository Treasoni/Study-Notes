---
title: "Superpowers Agentic Skills Framework — 从源码学习搭建 Agent 框架"
tags: [superpowers, agent-framework, workflow-pipeline, subagent, tdd, git-worktree, skills-system]
created: 2026-07-23
updated: 2026-07-23
status: completed
source_project: study-system
---

# Superpowers Agentic Skills Framework

> 从源码学习搭建 Agent 框架
>
> 基于 obra/superpowers v6.1.1 (MIT License, 259k+ Stars)
> 作者：Jesse Vincent @ Prime Radiant
> 学习笔记完成时间：2026-07-23

---

## 目录

1. [Superpowers 概览与哲学](#第一章-superpowers-概览与哲学)
2. [Skills 系统设计](#第二章-skills-系统设计--可组合的行为约束引擎)
3. [Workflow Pipeline — 7 阶段硬门控状态机](#第三章-workflow-pipeline--7-阶段硬门控状态机)
4. [Subagent Dispatching — 子 Agent 派发与审查引擎](#第四章-subagent-dispatching--子-agent-派发与审查引擎)
5. [Git Worktree 隔离执行](#第五章-git-worktree-隔离执行)
6. [Plugin 架构与跨平台部署](#第六章-plugin-架构与跨平台部署)
7. [启动钩子与自举机制](#第七章-启动钩子与自举机制)
8. [Writing-Skills — 框架的自我扩展机制](#第八章-writing-skills--框架的自我扩展机制)
9. [总结 — 如何借鉴 Superpowers 搭建自己的 Agent 框架](#第九章-总结--如何借鉴-superpowers-搭建自己的-agent-框架)

---




---

# 第一章：Superpowers 概览与哲学

## 本章目的

Superpowers 是一个开源的 Agentic Skills Framework，由 Jesse Vincent 在 Prime Radiant 创建，短短不到一年时间在 GitHub 上获得了 259k+ Stars。它不是一个普通的工具库——它是一套完整的软件开发方法论，旨在将 AI 编程 Agent 从"快"变成"可靠"。本章作为全篇的入口，带你了解 Superpowers 是什么、它的哲学基础、项目结构全貌，以及我们将在后续章节中深入学习的 7 个方向的关系。

---

## 1.1 什么是 Superpowers？

Superpowers 是一套**可组合的 AI Agent 技能体系 + 软件开发方法论**。它的核心思想很简单：当一个人 Coding Agent 开始一个项目时，不应该立刻写代码，而是遵循一套结构化的多阶段工作流：

1. 先通过提问细化需求（Brainstorming）
2. 在隔离环境中创建 Workspace（Git Worktrees）
3. 把工作分解成 2-5 分钟的原子任务（Writing Plans）
4. 通过 Subagent 派发逐一执行（Subagent-Driven Development）
5. 用 TDD 确保质量（RED-GREEN-REFACTOR）
6. 每个任务后进行代码审查（Code Review）
7. 最后完成分支整合（Finishing Branch）

这套流程不是建议性的"最佳实践"——它是**强制性的**。每个阶段之间都有二进制门控，不满足条件就无法进入下一阶段。

### 关键数据

| 指标 | 值 |
|------|-----|
| 版本 | v6.1.1 |
| 许可 | MIT License |
| Stars | 259k+ |
| 插件安装量 | 680k+ |
| 支持平台 | 10+（Claude Code, Codex, Cursor, Kimi Code, OpenCode, pi, Gemini CLI 等） |
| 技能数量 | 14 个 |
| 代码语言 | Shell 54%, JavaScript 39%, TypeScript 3% |

### 生态位置

Superpowers 属于 Agent 工作流框架这个新兴品类。它与以下框架有重叠但不同：

| 维度 | Superpowers | Matt Pocock Skills | Agent Skills (Addy Osmani) |
|------|-------------|-------------------|--------------------------|
| **核心假设** | 模型会偷懒找借口 | 模型大体上会做正确的事 | 需要多角色并行审查 |
| **触发方式** | 自动（1% 规则驱动） | 手动斜杠命令 | 混合 |
| **门控强度** | 硬门控，禁止跳过 | 软锚点，可跳过 | 硬门控 + 并行审查 |
| **Token 成本** | 高（v6 正在改善） | 低 | 中 |
| **最佳场景** | 纪律化长时间执行 | 快速需求澄清 | 企业级多维度验证 |

最核心的差异在于**对 AI 模型的基本假设**：Superpowers 假定模型在不受约束时会偷懒、会找借口绕过规则，因此用硬门控封堵每一条逃避路径。

---

## 1.2 核心哲学

### 硬门控，非软规则

这是 Superpowers 最根本的设计原则。项目的创建者 Jesse Vincent 曾分享过一个关键案例：

> 他让 Claude 实现一个 Todo List，Claude 看完了 Brainstorming 技能的说明后说："技能说以 200-300 字呈现设计。对于一个 Todo List 来说，这显得荒谬，所以我直接开始写代码。"

这个案例揭示了一个关键问题：LLM 会将建议性的语言合理化地忽略。如果技能写的是"应该先做设计"，模型会判断"这个场景太简单了，不需要"。因此 Superpowers 使用**硬门控（Hard Gate）**——不是"应该"，而是"没有用户审批就不能进入下一阶段"。

硬门控的三种形式：

1. **二进制门控**：不满足条件就无法通过（如：没有失败测试 → 不能写生产代码）
2. **强制检查清单**：必须逐项确认后才能继续
3. **物理隔离**：通过 Git Worktree 等技术手段隔离执行环境

### TDD 优先 — "没有失败测试，就没有生产代码"

TDD 在 Superpowers 中不是一种可选的方法论，而是**铁律**：

- 任何生产代码之前必须有一个失败测试
- 如果在写测试之前已经写了代码——**删除它**，重新开始
- 删除就是删除，不能保留作为参考，不能在写测试时去"适配"现有代码
- 不能找借口跳过（"太简单了"、"这是 UI 代码"、"时间紧迫"）

```
RED → 验证 RED → GREEN → 验证 GREEN → REFACTOR → 验证 GREEN 仍然通过 → NEXT
```

每个步骤之间的验证**必须通过 test runner 观察**，视觉确认不可接受。

### 1% 规则

这是整个系统自举的基石：

> 如果某个技能有 1% 的触发可能，Agent **必须**加载并遵循它。

这意味着 Agent 没有"我觉得这不适用"的自由裁量权。只要有技能匹配当前任务的迹象，就必须加载它。这个规则通过 `using-superpowers` 引导技能在每次会话启动时注入，Agent 的推理能力被用来**判断如何执行技能**，而不是**判断是否要跳过技能**。

### 指令优先级

```
用户/项目指令（CLAUDE.md, AGENTS.md, 用户直接请求）
    ↑ 优先于
Superpowers skills（SKILL.md 文件）
    ↑ 优先于
默认系统行为（工具内置默认值）
```

只有用户明确要求时，Agent 才能跳过技能流程。

### 系统化 over Ad-hoc

Superpowers 的哲学可以概括为：**有流程地做事，不靠猜测**。这个原则体现在每个层面：

- **Brainstorming** 不是随意聊天，而是 9 步结构化流程
- **Debugging** 不是胡乱猜测，而是 4 阶段根因分析
- **Code Review** 不是走过场，而是明确分级（Critical / Important / Minor）
- **任务划分** 不是大概的，而是精确到 2-5 分钟

---

## 1.3 项目结构全貌

### 目录架构

```
superpowers/
├── .claude-plugin/plugin.json       # Claude Code 插件注册
├── .codex-plugin/plugin.json        # Codex CLI 插件注册
├── .cursor-plugin/plugin.json       # Cursor 插件注册
├── .kimi-plugin/plugin.json         # Kimi Code 插件注册
├── .opencode/                       # OpenCode 集成
├── .pi/                             # pi 集成
├── gemini-extension.json            # Gemini CLI 集成
├── hooks/
│   ├── hooks.json                   # 钩子配置（SessionStart 事件）
│   ├── run-hook.cmd                 # 跨平台多语言包装器
│   └── session-start               # 自举脚本（核心入口）
├── skills/                          # 14 个可组合技能（核心资产）
│   ├── brainstorming/               # 协作 — 头脑风暴
│   ├── writing-plans/               # 协作 — 编写计划
│   ├── executing-plans/            # 协作 — 执行计划（备选）
│   ├── subagent-driven-development/ # 协作 — 子 Agent 驱动开发
│   ├── dispatching-parallel-agents/ # 协作 — 并行 Agent
│   ├── requesting-code-review/      # 协作 — 请求审查
│   ├── receiving-code-review/       # 协作 — 接收审查
│   ├── finishing-a-development-branch/ # 协作 — 完成分支
│   ├── using-git-worktrees/         # 协作 — Git Worktree 隔离
│   ├── test-driven-development/     # 测试 — TDD 强制
│   ├── systematic-debugging/        # 调试 — 4 阶段根因分析
│   ├── verification-before-completion/ # 调试 — 修复后验证
│   ├── using-superpowers/           # 元技能 — 引导程序
│   └── writing-skills/              # 元技能 — 编写新技能
├── docs/
│   ├── porting-to-a-new-harness.md  # 移植到新平台指南
│   ├── plans/                       # 执行计划存储
│   └── superpowers/specs/           # 设计文档存储
├── scripts/                         # 工具脚本
├── references/                      # 各平台工具映射
├── CLAUDE.md                        # 贡献者指南
└── RELEASE-NOTES.md                 # 发布说明
```

### 14 个技能分类

| 类别 | 技能 | 一句话角色 |
|------|------|-----------|
| **协作** (9) | brainstorming | 通过结构化提问澄清需求，输出设计文档 |
| | writing-plans | 将设计分解为 2-5 分钟的可执行任务 |
| | executing-plans | 内联执行计划（备选路径，subagent 不可用时） |
| | subagent-driven-development | 旗舰引擎：每任务派发独立 subagent |
| | dispatching-parallel-agents | 多 Agent 并行处理独立问题 |
| | requesting-code-review | 请求代码审查，输出分级发现 |
| | receiving-code-review | 6 步接收审查反馈模式 |
| | finishing-a-development-branch | 测试验证 + 分支完成/合并/PR |
| | using-git-worktrees | 工作区隔离，环境保障 |
| **测试** (1) | test-driven-development | RED-GREEN-REFACTOR 强制，零例外 |
| **调试** (2) | systematic-debugging | 4 阶段根因分析，禁止未调查就修复 |
| | verification-before-completion | 修复后验证，确保真的修好了 |
| **元** (2) | using-superpowers | 引导程序，每次会话自注入 |
| | writing-skills | 如何编写新技能（TDD 驱动文档） |

### 三组件架构

整个框架由三个不变的组件构成：

1. **Skills（平台无关）**：`skills/` 下的所有内容在所有平台上完全共享。技能描述**动作**（"调用一个技能"、"读取文件"、"派发子代理"），从不命名具体工具。
2. **Tool Mapping（每平台）**：动作词汇翻译为平台的真实工具名称。存放在 `references/<harness>-tools.md` 或引导注入器中内联。
3. **Bootstrap（每平台）**：每会话开始时将完整的 `using-superpowers/SKILL.md` 注入模型上下文，包裹在 `<EXTREMELY-IMPORTANT>` 标签中。

---

## 1.4 七个学习方向的关联

这本笔记覆盖 7 个方向，它们不是孤立的而是层层递进的：

```
                     ┌──────────────────┐
                     │  Plugin 架构      │ ← 跨平台部署能力
                     │  （方向 5）        │
                     └────────┬─────────┘
                              │ 支撑
                     ┌────────▼─────────┐
                     │  启动钩子/自举     │ ← 入口，每次会话触发
                     │  （方向 6）        │
                     └────────┬─────────┘
                              │ 注入
                     ┌────────▼─────────┐
                     │  1% 规则 +        │
                     │  Skills 系统设计   │ ← 行为约束引擎
                     │  （方向 4）        │
                     └────────┬─────────┘
                              │ 编排
              ┌───────────────┼───────────────┐
              │               │               │
     ┌────────▼──────┐ ┌─────▼──────┐ ┌──────▼────────┐
     │Workflow       │ │Subagent    │ │Git Worktree   │
     │Pipeline       │ │Dispatching │ │隔离执行        │
     │（方向 1）      │ │（方向 2）    │ │（方向 3）       │
     │阶段流转+门控   │ │执行引擎     │ │基础设施保障    │
     └───────────────┘ └────────────┘ └───────────────┘
                              │
                     ┌────────▼─────────┐
                     │  Writing-Skills   │ ← 框架如何扩展自身
                     │  （方向 7）        │
                     └──────────────────┘
```

阅读建议：
- **第 2-4 章**（Skills 系统 → Pipeline → Subagent）是核心，构成了 Superpowers 的主干
- **第 5-7 章**（Worktree → Plugin → 自举）是支撑层，深入理解需要但可跳读
- **第 8 章**（Writing-Skills）是元视角，理解后可以编写自己的技能
- **第 9 章** 是对前面所有内容的提炼，回答"如何借鉴来搭建自己的框架"

---

## 本章小结

- Superpowers 是一个可组合的 Agentic Skills Framework，核心方法是**硬门控状态机 + Subagent 执行引擎 + Skills 约束体系**
- 核心理念：**硬门控而非软规则**、**TDD 不可妥协**、**1% 规则强制触发**、**系统化 over ad-hoc**
- 项目结构由 14 个技能（4 大类）、6+ 平台插件目录、和自举钩子系统组成
- 14 个技能分为协作（9）、测试（1）、调试（2）、元技能（2）
- 三个不变组件：Skills（平台无关）+ Tool Mapping（每平台）+ Bootstrap（每平台）
- 7 个学习方向构成"入口 → 约束 → 编排 → 执行 → 设施 → 扩展"的递进结构

### 下一章预告

理解了 Superpowers 的全貌和哲学后，下一章我们将深入最核心的抽象——**Skills 系统设计**，看 14 个技能如何通过 SKILL.md 定义、自动发现和触发，以及描述优化的关键陷阱。




---

# 第二章：Skills 系统设计 — 可组合的行为约束引擎

## 本章目的

上一章我们看到了 Superpowers 的全貌——14 个技能、6+ 个平台、门控管线。但所有这些能力都建立在同一个核心抽象之上：**SKILL.md**。本章深入这个抽象：技能是什么格式？如何定义、发现和触发？编写技能时最关键的设计原则是什么？

理解 Skills 系统是理解整个 Superpowers 的钥匙——Pipeline 由技能串联，Subagent 由技能驱动，自举由技能注入。

---

## 2.1 什么是 Skill？

在 Superpowers 中，一个 Skill 是一个**行为约束单元**——它不是代码库，不是 API，而是以 Markdown 文档形式定义的 Agent 行为规范。每个 Skill 目录包含一个 `SKILL.md` 文件，Agent 在运行时读取它并按照其中的规则行动。

Skill 与传统的库或函数的区别：

| 维度 | 传统函数/库 | Superpowers Skill |
|------|------------|-------------------|
| 形态 | 可执行代码 | Markdown 文档 |
| 调用方式 | 代码调用（import / require） | 上下文触发（自动或手动） |
| 约束力 | 必须遵守（编译/运行时强制） | 行为约束（硬门控 + 描述触发） |
| 跨平台 | 需分别实现 | 同一文件，仅工具映射不同 |
| 版本管理 | npm / cargo 包管理 | Git 仓库 + 钩子注入 |

### 14 个技能速览

全部技能按类别分为 4 组：

**协作技能（9 个）** — 覆盖从需求到交付的完整开发流程：

| 技能 | 阶段 | 一句话描述 |
|------|------|-----------|
| brainstorming | 需求 | 通过结构化提问澄清需求，输出设计文档到 `docs/superpowers/specs/` |
| writing-plans | 计划 | 将设计分解为 2-5 分钟的原子任务，每步含完整代码 |
| executing-plans | 执行 | 内联执行已有计划（备选路径） |
| subagent-driven-development | 执行 | **旗舰引擎**：每任务派发独立 subagent + 审查 |
| dispatching-parallel-agents | 执行 | 多 subagent 并行处理独立问题域 |
| requesting-code-review | 审查 | 对 diff 进行审查，输出 Critical / Important / Minor |
| receiving-code-review | 审查 | 6 步接收模式：读 → 理解 → 验证 → 评估 → 回应 → 实施 |
| finishing-a-development-branch | 交付 | 测试验证 + 分支完成/合并/PR/丢弃 |
| using-git-worktrees | 环境 | 工作区隔离 + 测试基线验证 |

**测试技能（1 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| test-driven-development | RED-GREEN-REFACTOR 强制，零例外，预判 8 种 Agent 合理化借口 |

**调试技能（2 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| systematic-debugging | 4 阶段根因分析：观察 → 假设 → 验证 → 修复，禁止未调查就修复 |
| verification-before-completion | 修复后验证，确保真的修好了且没有引入新问题 |

**元技能（2 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| using-superpowers | 引导程序 | 每个会话自动注入，声明 1% 规则和技能优先级 |
| writing-skills | 编写新技能的方法论，使用 TDD 驱动文档 |

---

## 2.2 SKILL.md 结构规范

每个技能必须遵循以下结构：

### YAML Frontmatter（必填）

```yaml
---
name: skill-name           # 仅字母、数字、连字符。无括号、无特殊字符
description: Use when...   # 触发条件，不是技能总结
---
```

`name` 要求：
- 仅小写字母、数字和连字符
- 例如：`test-driven-development`，不是 `TDD` 或 `test_driven_development`

`description` 要求：
- 必须以 **"Use when..."** 开头
- 描述**什么情况下触发**，不是技能做什么
- 不超过 1024 字符，尽量保持在 500 以下
- 使用第三人称

### 正文段落（推荐顺序）

```
## 概述（1-2 句核心原则）

## 何时使用
- 症状列表 / use cases
- 小内联流程图（用于非明显的决策点）

## 核心模式
- 对于技术/模式技能：before/after 代码对比
- 说明什么是好的模式，什么是不好的模式

## 快速参考（可选）
- 常用操作表，方便扫描

## 实现细节（可选）
- 简单模式内联
- 繁重内容或可复用工具链接到单独文件

## 常见错误
- 什么会出错 + 如何修复

## 真实世界影响（可选）
- 为何这个技能重要
```

### 三个技能类型

| 类型 | 描述 | 示例 | 特点 |
|------|------|------|------|
| **技术技能** | 有具体步骤的方法 | TDD, systematic-debugging | 步骤清晰，流程明确 |
| **模式技能** | 思考问题的方式 | flatten-with-flags, test-invariants | 范式转换，before/after 对比 |
| **参考技能** | API 语法、工具用法 | 快速参考表 | 表格为主，便于扫描 |

### Token 预算

| 技能类型 | 目标大小 |
|---------|---------|
| 入门工作流 | 每技能 <150 词 |
| 频繁加载的技能 | 总计 <200 词 |
| 其他技能 | <500 词 |

优化策略：
- 将细节移到工具帮助中（"运行 --help 获取详细信息"）
- 使用交叉引用（"必需背景：理解 superpowers:systematic-debugging"）
- 压缩示例，消除冗余

---

## 2.3 自动发现与触发机制

### 发现路径

Claude Code 自动扫描以下路径查找技能：

```
项目 .claude/ 目录下 → 自动发现
用户 ~/.claude/ 目录下 → 用户级技能
插件安装目录 → 通过 plugin.json 注册
```

对于 Superpowers，它作为插件安装后，其 `skills/` 目录被自动扫描。每个 `SKILL.md` 是一个可触发的技能。

### 触发条件

触发完全依赖 `description` 字段。Claude Code 在每次任务前会检查是否有匹配的技能：

```
用户说："帮我写一个 React 组件"
    ↓
模型检查 skills 匹配：
    brainstorming（"Use when building or designing new features..."）→ ✅ 匹配
    test-driven-development（"Use when implementing features..."）→ ✅ 匹配
    ↓
1% 规则触发 → 加载匹配的技能
```

### 关键发现：描述不要总结流程

这是 Superpowers 开发过程中最重要的经验发现之一。

**错误示例**（总结流程）：
```
description: "Use when reviewing code between tasks. Runs spec compliance check
then code quality check, reporting issues by severity."
```

这种描述的问题：Agent 读到 "runs spec compliance check then code quality check" 后，以为已经知道要做什么了，于是**直接按这个描述做了一次审查**——而不是去读完整的 SKILL.md 中的详细流程（那里定义的是**两次**独立审查，由不同的 reviewer prompt 执行）。

**正确示例**（只写触发条件）：
```
description: Use when a task implementation is complete and the changes need
review before being integrated.
```

Agent 读了这个描述会触发"需要加载技能"的判断，然后去读完整的 SKILL.md 来了解具体怎么做。

**规则**：Description 只写何时触发，不写技能做了什么。触发判断由描述驱动，执行细节由正文驱动。

### 技能优先级

当多个技能匹配时，按以下顺序加载：

1. **流程技能优先**（brainstorming, systematic-debugging）—— 它们设定方法
2. **然后实现技能**（frontend-design, mcp-builder 等）—— 它们执行方法

例如："让我们构建一个 React 应用" → 先加载 brainstorming（澄清需求），再加载实现技能。

---

## 2.4 技能的约束力层

理解 Skills 的约束力很重要——不是所有技能都有同等的约束强度：

```
硬门控 ─────────────────► 软参考

强制规则                    建议指导
禁止 + 借口表               最佳实践
红旗列表                    可参考的模板
不可跳过的检查清单           知识参考
```

- **TDD skill** 属于最左端：禁止写代码前没有失败测试，红旗列表预判 Agent 的借口
- **Writing skills** 属于中间：有明确步骤但 Agent 有一定自由度
- **参考技能** 属于最右端：主要是信息性内容

设计自己的 Skill 时，需要根据约束目标选择正确的位置。

---

## 2.5 实战：SKILL.md 模板

以下是一个最小 Skill 模板，基于 Superpowers 规范：

```markdown
---
name: my-custom-skill
description: Use when [触发条件]，不要总结做了什么
---

## 概述

[1-2 句核心原则]

## 何时使用

- [症状 1]
- [症状 2]

## 核心模式

### 好的做法
```code
```

### 不好的做法
```code
```

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| ... | ... | ... |
```

如果你的技能需要强制执行纪律（如"必须先做 A 再做 B"），**不要**只写软性指导（"最好先做 A"），而要使用**禁止 + 借口表**：

```markdown
## 禁止

- ❌ 禁止跳过 [步骤] 因为 [常见借口 1]
- ❌ 禁止用 [借口 2] 来绕过 [步骤]
- ❌ 禁止 [常见变通方法]

如果以上任何一条听起来很熟悉 → 停下来，回到 [步骤]。
```

---

## 本章小结

- Superpowers 的 14 个技能分为协作（9）、测试（1）、调试（2）、元技能（2）四大类
- 每个技能是一个包含 `SKILL.md` 的目录，由 YAML frontmatter（name + description）和结构化正文组成
- 技能通过 `description` 字段自动发现和触发，**描述只写触发条件，不总结流程**
- 总结流程的描述会诱使 Agent 走捷径，不读完整 SKILL.md
- Token 预算策略：入门 <150 词，高频 <200 词，其他 <500 词
- 约束力从"硬门控"到"软参考"是一个光谱，设计技能时要选择正确的位置
- 纪律性技能需要使用"禁止 + 借口表 + 红旗列表"而非软性指导

### 下一章预告

理解了 Skills 系统的基础后，下一章进入 Pipeline 核心：**7 阶段硬门控状态机**，看 Brainstorming → Writing Plans → TDD → Code Review 每个阶段的细节、门控条件和强制机制。




---

# 第三章：Workflow Pipeline — 7 阶段硬门控状态机

## 本章目的

这是整本笔记最核心的一章。Superpowers 之所以能"把 AI 写代码从快变成可靠"，根本原因就是这条 7 阶段 pipeline。每个阶段之间有二进制门控，不满足条件就无法进入下一阶段。本章逐段拆解 Brainstorming → Writing Plans → TDD → Code Review → Finishing Branch 的完整流程、门控条件和强制机制。

---

## 3.1 完整管线总览

```
Phase 1: Brainstorming（头脑风暴）
    │ 门控：设计文档已写 + 用户已审批
    ▼
Phase 2: Git Worktrees（工作区隔离）
    │ 门控：隔离工作区已创建 + 测试基线通过
    ▼
Phase 3: Writing Plans（编写计划）
    │ 门控：计划文件已保存 + 用户选执行路径
    ▼
Phase 4: Subagent-Driven Development（执行）
    │ 或 Executing Plans（备选）
    │ 门控（每任务）：TDD RED → 验证 → GREEN → 验证 → REFACTOR
    ▼
Phase 5: Requesting Code Review（审查）
    │ 门控：Critical + Important 问题已修复
    ▼
Phase 6: Finishing Branch（分支完成）
    │ 门控：所有测试通过 + 用户选择整合方式
    ▼
Done
```

### 9 个硬门控

| 门控 | 从 → 到 | 条件 |
|------|---------|------|
| G1 | Brainstorming → Writing Plans | 设计文档完成 + 用户审批 |
| G1a | Brainstorming 内部 | 每节设计用户审批 |
| G1b | Brainstorming 内部 | 书面 spec 用户审批 |
| G2 | Writing Plans → Execution | 计划文件保存 + 用户选路径 |
| G3 | 任务开始 → TDD RED | 无生产代码存在 |
| G4 | RED → GREEN | 测试失败已通过 test runner 验证 |
| G5 | GREEN → REFACTOR | 测试通过已通过 test runner 验证 |
| G6 | 任务完成 → 下一任务 | 代码审查通过（Critical + Important 已修复） |
| G7 | 全部任务完成 → Finishing | 所有测试通过 |
| G8 | Finishing → Done | 用户选择操作 + merge 后测试通过 |

---

## 3.2 Phase 1: Brainstorming（头脑风暴）

### 目的

把模糊的想法变成完整的设计文档。**在读任何代码、写任何实现之前**，必须先通过这个阶段。

### 触发条件

**任何**创造性的工作——创建功能、构建组件、添加功能、修改行为。没有"太简单不需要设计"的豁免。

### 9 步严格流程

```
Step 1: 探索项目上下文 → 读取文件、文档、最近 commits
    │
Step 2: 按需提供视觉辅助（仅当问题用视觉表达更清晰时）
    │  每次只能一个消息，不能夹带其他内容
    │
Step 3: 提出澄清问题 → 一次只问一个，优先选择题
    │
Step 4: 提出 2-3 种方案 → 含权衡分析和推荐
    │
Step 5: 分节展示设计 → 每节需要用户审批
    │  ↓ 不通过 → 回到修改
    │  ↓ 通过 → 继续下一节
    │
Step 6: 写入设计文档 → docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
    │  并提交到 git
    │
Step 7: 自我审查 → 检查占位符、矛盾、歧义、范围蔓延
    │
Step 8: 用户审查书面 spec
    │  ↓ 要求修改 → 回到 Step 6
    │  ↓ 通过 → 进入下一阶段
    │
Step 9: 调用 writing-plans
```

### 关键规则

- **禁止实现技能**在设计中运行（如 `frontend-design`、`mcp-builder`）
- Design doc 覆盖：架构、组件、数据流、错误处理、测试策略
- 规模自适应：简单主题几句话，复杂主题每节 200-300 字
- 如果需求涉及多个独立子系统 → 立即分解，每个子项目独立走 brainstorm → plan → implementation 周期

---

## 3.3 Phase 2: Git Worktrees（工作区隔离）

> 详见第 5 章

此处只说明它在管线中的位置：在**计划开始前**，确保开发在一个隔离的工作区中进行。如果实现出问题，直接删除 worktree 重试。

---

## 3.4 Phase 3: Writing Plans（编写计划）

### 目的

把设计文档分解成可执行的原子任务。假设"执行者对我们代码库零上下文，而且品味可疑"，所以计划必须完整到每一个细节。

### 核心规则

**1. 范围分解**
如果 spec 跨越多个独立子系统 → 拆分，每个子系统一个计划。每个计划必须产出"独立可工作的可测试软件"。

**2. 先定文件结构，再定任务**
在定义具体任务之前，先列出所有要创建或修改的文件及其职责。"按职责拆分，不按技术层拆分。"

**3. 任务粒度**
一个任务是"最小可独立携带测试周期、值得独立审查员审查的单元"。每步 ~2-5 分钟：

```
1. 写失败测试代码 → 2. 运行看到它失败 → 3. 写最小实现 → 4. 运行看到它通过 → 5. commit
```

**4. 禁止占位符**
```
❌ TBD、TODO、implement later、fill in details
❌ add appropriate error handling
❌ similar to Task N
```
每步必须包含**完整、真实的代码**。

**5. 类型一致**
函数签名和属性名必须在任务间一致。不一致"是 bug"。

### 输出结构

```markdown
## 计划：[功能名称]

### 目标
[一句话]

### 架构
[关键架构决策]

### 技术栈
[技术选型]

### 全局约束
[设计约束]

---

### 任务 1：[任务名]
- **文件**：create: src/xxx.py | modify: tests/test_xxx.py
- **接口**：consumes: [类型] | produces: [类型]
- **步骤**：
  - [ ] 写测试：[代码]
  - [ ] 运行测试失败（预期错误：[信息]）
  - [ ] 实现：[代码]
  - [ ] 运行测试通过
  - [ ] git commit -m "..."

### 任务 2：[任务名]
...
```

### 两种执行路径

计划写完并保存到 `docs/superpowers/plans/` 后，用户选择：

1. **Subagent-Driven Development（推荐）**：每个任务由独立 subagent 执行 + 审查
2. **Inline Execution（备选）**：在同一会话中批量执行，有人工检查点

---

## 3.5 Phase 4: TDD — RED-GREEN-REFACTOR

这不是一个独立的阶段，而是**嵌入在每个任务执行过程中**的循环。

### 铁律

> 没有失败测试，就没有生产代码。

```
Step 1: RED —— 写一个最小的失败测试
    │  - 一件事
    │  - 清晰的测试名
    │  - 用真实代码（mock 只在不可避免时）
    │
Step 2: 验证 RED（强制）
    │  - 运行 test runner
    │  - 确认失败信息符合预期
    │  - 失败因为功能缺失，不是测试本身有 bug
    │  └─ 测试通过 → 修正测试；测试报错 → 修正错误
    │
Step 3: GREEN —— 写最简单的代码让测试通过
    │  - 不实现测试不要求的功能
    │
Step 4: 验证 GREEN（强制）
    │  - 运行 test runner
    │  - 确认新测试通过，其他测试也通过
    │  └─ 新测试失败 → 修正代码，不改测试；其他测试失败 → 立即修复
    │
Step 5: REFACTOR —— 清理代码
    │  - 去重、改名、提取辅助方法
    │  - 不添加新行为
    │  - 保持测试绿色
    │  └─ 测试不通过 → 回到验证 GREEN
    │
Step 6: NEXT —— 下一个失败测试，回到 Step 1
```

### 预判的 Agent 借口（红旗列表）

| Agent 的借口 | 系统的反驳 |
|-------------|-----------|
| "这太简单了，不需要 TDD" | 简单的事情会变得复杂。使用 TDD。 |
| "这是 UI 代码" | UI 代码也需要测试。使用 TDD。 |
| "时间紧迫" | TDD 节省时间。从测试开始。 |
| "先把代码写完再补测试" | 事后写的测试测试的是实现，不是行为。 |
| "让我先看看现有代码" | 先读技能，再探索代码。 |
| "我已经知道要怎么实现了" | 知道不等于测试。写测试。 |
| "这个改动太小了" | 小的改动也会破坏东西。写测试。 |

如果 Agent 在写测试前已经写了代码：

> 删除它。不要留着作为参考。不要在写测试时去适配它。不要看它。

---

## 3.6 Phase 5: Requesting Code Review（代码审查）

### 触发时机

**必须**：每个任务完成后、主要功能完成后、合并到 main 前
**可选**：卡住时、重构前、修复复杂 bug 后

### 审查流程

```
Step 1: 获取 BASE_SHA 和 HEAD_SHA（git）
    │
Step 2: 派发审查 subagent（只读）
    │  - 使用 code-reviewer.md 模板
    │  - 填充：{DESCRIPTION}、{PLAN_OR_REQUIREMENTS}
    │  - 填充：{BASE_SHA}、{HEAD_SHA}
    │
Step 3: 审查者评估 diff
    │  输出：
    │  - Strengths（正面的观察）
    │  - Issues（分级：Critical / Important / Minor）
    │  - Assessment（总体判定）
    │
Step 4: 按优先级修复
    │  1. Critical（阻塞进度）
    │  2. Important（必须修复）
    │  3. Minor（可选）
    │  对审查者有异议 → 用技术推理反驳，不是防御性回应
```

### 关键限制

- **禁止**跳过审查，因为"改动很简单"
- **禁止**忽略 Critical 问题继续
- **禁止**带着未修复的 Important 问题继续
- **禁止**与有效的技术反馈争论
- 审查者**只读**——不能修改代码，不能被说服跳过发现

### 审查分级

| 级别 | 含义 | 处理 |
|------|------|------|
| Critical | 功能错误、安全问题、数据丢失 | 阻塞进度，必须修复 |
| Important | 代码质量问题、设计问题 | 必须修复 |
| Minor | 风格问题、命名建议 | 可选，在最终审查时处理 |
| 计划冲突 | 与计划文本矛盾 | 上报人类决策 |

---

## 3.7 Phase 6: Finishing Branch（分支完成）

### 流程

```
Step 1: 验证测试 → 失败 → 停止；通过 → 继续
    │
Step 2: 检测环境 → 普通 repo / worktree / detached HEAD
    │
Step 3: 确定基准 → git merge-base HEAD main
    │
Step 4: 提供选项
    │  Option 1: Merge to main（合并 + 测试 + worktree 清理 + 分支删除）
    │  Option 2: Create PR（推送 + 打开 PR）
    │  Option 3: Keep branch（不做任何事）
    │  Option 4: Discard（确认输入 "discard" + worktree 清理 + 分支删除）
    │
Step 5: 执行选中的路径
    │
Step 6: 清理（仅 Option 1 和 4）
```

### 安全规则

- 合并前：**测试必须通过**
- 丢弃前：必须逐字输入 "discard"（不是 "yes" 或 "y"）
- 合并后：**必须重新测试**，合并本身可能引入问题
- 删除分支顺序：先 merge，再删 worktree，再删分支（反向顺序会失败）
- 溯源所有权：`.worktrees/` 下的 agent 可以删，其他位置的**不能动**

---

## 3.8 防跳过机制汇总

Superpowers 防止 Agent 跳过步骤的方式覆盖了多层：

| 防御层 | 机制 | 对应阶段 |
|--------|------|---------|
| 1% 规则 | 强制检查技能，不可协商 | 所有阶段 |
| 硬门控 | 不满足条件无法进入下一阶段 | 所有阶段 |
| 预判借口表 | 明确列举 Agent 可能用的借口 | Brainstorming, TDD |
| Subagent 隔离 | 每任务新鲜上下文，不能"偷懒" | SDD |
| 审查只读 | 审查者不能改代码，不能跳过发现 | Code Review |
| 逐字确认 | "discard" 必须逐字输入 | Finishing |
| 溯源所有权 | 区分 agent 和宿主环境 | Git Worktrees |
| 进度账本 | `.superpowers/sdd/progress.md` 持久化，支持断点恢复 | SDD |

---

## 本章小结

- Pipeline 由 7 个阶段组成，每个阶段之间有一个或多个硬门控
- Brainstorming（9 步流程）确保需求澄清后才进入实现
- Writing Plans 把设计分解为 2-5 分钟的原子任务，禁止 TODO/TBD
- TDD 是嵌入在每任务执行中的 RED-GREEN-REFACTOR 循环
- Code Review 由只读 subagent 执行，输出 Critical/Important/Minor 三级发现
- Finishing Branch 提供 4 种选项，有严格的测试和安全规则
- 9 个硬门控 + 多层防跳过机制确保流程不可绕过

### 下一章预告

Pipeline 定义了"做什么"，Subagent Dispatching 定义了"怎么做"。下一章进入**Subagent-Driven-Development**，看如何派发独立 subagent 执行每任务，以及四种状态报告协议如何驱动执行流程。




---

# 第四章：Subagent Dispatching — 子 Agent 派发与审查引擎

## 本章目的

Pipeline 定义了"做什么"，Subagent Dispatching 是"怎么做"。这是 Superpowers 的执行引擎核心——每个任务派发一个全新的 subagent，隔离上下文，执行完毕后由只读审查者把关。本章详解派发流程、状态协议、模型分层、审查机制和并行派发模式。

---

## 4.1 核心模式

### SDD 概述

Subagent-Driven-Development（SDD）是 Superpowers 的旗舰执行模式。核心思想：

> 每个任务派发一个新鲜的 subagent + 隔离上下文 + 强制两阶段审查 = 高质量、快迭代

对比传统在一个会话中顺序执行所有任务：

| 维度 | 内联执行 | Subagent-Driven Development |
|------|---------|---------------------------|
| 上下文 | 累积，越来越重 | 每个 subagent 新鲜 |
| 注意力 | 长会话后质量下降 | 每次都专注 |
| 审查 | 自审（偏见） | 独立审查者（客观） |
| 隔离 | 无 | Git Worktree + 上下文隔离 |
| 恢复 | 会话中断全丢 | 进度账本支持恢复 |

### 完整派发流程

```
Controller（主 Agent，编排者）
    │
    ├─ [准备] scripts/task-brief PLAN_FILE N
    │       提取任务 N 到独立文件 task-N-brief.md
    │
    ├─ [组装] Dispatch 消息：
    │   ├─ 1 行项目上下文定位
    │   ├─ brief 文件路径（需求唯一来源）
    │   ├─ 上游任务产出的接口/决策
    │   ├─ Controller 发现的歧义处理
    │   └─ report 文件路径
    │   └─ 指定模型（Haiku / Sonnet / Opus）
    │
    ├─ [派发] → Implementer Subagent
    │            │
    │            ├─ DONE               → 生成 review package → 派发 reviewer
    │            ├─ DONE_WITH_CONCERNS → 先阅读 concerns
    │            ├─ NEEDS_CONTEXT      → 补充信息，重新派发
    │            └─ BLOCKED            → 评估原因，分层处理
    │
    ├─ [审查] → Reviewer Subagent（只读）
    │            ├─ 输出：Strengths + Issues（Critical/Important/Minor）
    │            └─ 两种判定：Spec Compliance + Code Quality
    │
    └─ [修复] → Fix Subagent（如果发现问题）
                 ├─ 所有 Critical + Important 打包给一个 fix subagent
                 └─ 修复后重新派发 reviewer
```

---

## 4.2 派发细节

### Context 隔离原则

Subagent 不应继承 Controller 的任何上下文或历史。Controller 精确构造 subagent 需要的全部信息：

```
✅ 正确的做法：
  - 把任务需求写到 brief 文件，subagent 读文件
  - 把 diff 写到 review-package 文件，reviewer 读文件
  - 一个 dispatch 描述一个任务，不是整个会话的历史

❌ 错误的做法：
  - 让 subagent 读整个 plan 文件（包含其他任务的上下文）
  - 在 dispatch 中粘贴之前任务的摘要
  - 在同一 dispatch 中包含多个任务
```

### 任务切割原则

一个 task 应该是"最小可独立测试、值得独立审查的单元"。典型的标准：

- 每步 2-5 分钟
- 每步产出可测试的增量
- 步骤之间**不共享运行时状态**
- 如果两个步骤锁同一个文件 → 应该合并

### 模型选择策略

| 模型 | 用途 | 成本特征 |
|------|------|---------|
| **Haiku** | 机械性任务：转写、搜索、简单的 1-2 文件实现 | 最便宜，适合高吞吐 |
| **Sonnet** | 多文件集成、审查者角色 | 性价比最高，默认选择 |
| **Opus** | 架构决策、最终整分支审查 | 最贵，仅在关键节点使用 |

**规则**：每次派发必须显式指定模型。省略会默认使用会话模型（通常是最贵的），导致不必要的成本。

---

## 4.3 状态报告协议

Implementer 返回四种状态之一：

### DONE（完成）

任务完成。Controller 生成 review package 并派发 reviewer。

处理流程：
1. 获取 BASE_SHA（派发前记录的 commit）和 HEAD_SHA
2. 运行 `scripts/review-package BASE HEAD` → 产生 diff 文件
3. 派发 reviewer（使用 task-reviewer-prompt，不是 code-reviewer）
4. Reviewer 返回发现 → 如果有 Critical/Important → 派发一个 fix subagent

### DONE_WITH_CONCERNS（完成但有关注点）

Implementer 对某些决策有担忧。Controller 先阅读 concerns：

- **正确性疑虑** → 先验证和解决
- **观察性备注** → 记录在进度账本中，后续处理

### NEEDS_CONTEXT（需要上下文）

Implementer 发现信息不足以完成任务。Controller 补充信息后重新派发（可考虑升级模型）。

### BLOCKED（阻塞）

Implementer 无法继续。Controller 需要分类处理：

| 阻塞原因 | 处理方式 |
|---------|---------|
| **上下文缺口** | 补充上下文后用同一模型重新派发 |
| **推理缺口** | 升级到更强模型重新派发 |
| **任务太大** | 拆分成更小的任务重新派发 |
| **计划错误** | 上报人类，暂停进度 |

**规则**：不得忽略上报，不得在无变化时强制重试。

---

## 4.4 审查机制

### v5 → v6 演进

| 版本 | 审查方式 | 特点 |
|------|---------|------|
| v5 | 每个任务后两次独立审查 | Spec 合规 + 代码质量分别由不同 prompt 执行 |
| v6 | 一次 diff 通读，两个判定 | 合并为一个 task-reviewer-prompt，减少 token 消耗 50% |

v6 还增加了：
- **预飞行计划冲突检查**：派发前检查任务是否与已有工作冲突
- **文件传递 diff**：审查材料通过文件传递，不粘贴到上下文中
- **最终整分支审查**：所有任务完成后，用最强模型做一次全量审查

### 审查者限制

- **只读**：只能使用 Read、Grep、Glob、LS 等工具
- **不能修改代码**：审查者看到问题只能报告，不能直接改
- **不能跳过发现**：不能被说服或诱导忽略问题
- **隔离 diff**：审查者只看当前任务的 diff，不看整个会话历史

### 四级发现报告

| 级别 | 含义 | 处理 |
|------|------|------|
| Critical | 功能错误、安全问题 | 阻塞进度，必须修复 |
| Important | 代码质量问题 | 必须修复 |
| Minor | 风格命名等 | 记录，最终审查时处理 |
| 计划冲突 | 与计划文本矛盾 | 上报人类决策 |

多个 Critical/Important 发现 → **打包给一个 fix subagent**（不是每个发现一个）。

### 最终整分支审查

所有任务通过后，使用 `requesting-code-review` skill 的 `code-reviewer.md` 做全量审查：

```
Controller → 派发 code-reviewer → 输出全部分级发现
    │
    └─ 有发现 → 打包给一个 fix subagent → 修复 → 重新运行测试
    └─ 无发现 → 进入 Finishing Branch 阶段
```

---

## 4.5 持久化进度账本

SDD 使用 `.superpowers/sdd/progress.md` 文件持久化记录进度，支持**会话中断恢复**：

```
Task 1: complete (commits a1b2c3..d4e5f6, review clean)
Task 2: complete (commits f6g7h8..i9j0k1, review clean)
Task 3: in_progress (brief created, implementer dispatched)
```

恢复时：
1. 检查进度账本
2. 用 `git log` 验证 commit 范围
3. 已完成的跳过，未完成的继续
4. **不依赖内存**

---

## 4.6 Parallel Agent Dispatching（并行派发）

### 适用场景

SDD 的任务是**顺序执行**的。Parallel Dispatching 是另一个 skill，处理**可以同时进行**的独立问题：

- 3+ 个测试文件因不同根因失败
- 多个独立子系统需要同时修改
- 各子问题可以不用彼此上下文就理解

### 不适用场景

- 问题之间有共享状态
- 需要全系统上下文才能理解
- 探索性调试（尚不知问题是否独立）
- 多个 agent 会编辑同一文件

### 执行模式

```
Controller → 在单个响应中派发多个 subagent
    │
    ├─ Subagent 1: 处理子系统 A（scope: src/a/）
    ├─ Subagent 2: 处理子系统 B（scope: src/b/）
    └─ Subagent 3: 处理子系统 C（scope: src/c/）
    │
    全部返回后：
    ├─ 汇总每个 subagent 的发现
    ├─ 检查文件冲突（是否编辑了同一文件）
    ├─ 运行完整测试套件
    └─ 人工抽查系统性错误
```

### 与 SDD 的对比

| 维度 | SDD | Parallel Dispatching |
|------|-----|---------------------|
| 任务关系 | 顺序依赖 | 独立并发 |
| 上下文隔离 | 每个任务隔离 | 每个问题域隔离 |
| 同步机制 | Controller 顺序等待 | 无，完成后汇总 |
| 审查 | 每任务 + 最终 | 汇总后一次 |
| 使用场景 | 功能开发 | 多路调试/独立修复 |

---

## 4.7 实际案例：Builder.io 告警守护进程

Builder.io 团队用 SDD 构建了一个无状态告警守护进程（Go 语言），以下是关键数据：

| 指标 | 值 |
|------|-----|
| Brainstorming 产出 | 424 行规范文档 |
| 锁定的关键决策 | 3 个（冷却机制、通知器设计、互斥语义） |
| 计划覆盖 | 17 个文件，26 个任务 |
| 审查捕获 | 1 个命名不一致（审查发现了 BenchmarkEngineSwap vs EngineReinit） |
| 环境相关问题 | 10 个额外修复提交（BSD date, PID 等） |
| 最终测试 | 100 个延迟样本全部通过 |

案例教训：
1. **环境问题无法规划**——平台特定问题需要跳出工作流单独处理
2. **计划继承 spec 的错误**——配置解析器格式规范写错，导致所有基准脚本都错了
3. **三条不可妥协规则**：规范是唯一真理、先测试再代码、完成一项勾掉一项

---

## 本章小结

- SDD 是 Superpowers 的执行引擎：每任务派发全新 subagent + 隔离上下文 + 强制审查
- 四种状态报告（DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED）驱动执行流程
- 模型分层：Haiku（机械）→ Sonnet（默认）→ Opus（架构/最终审查）
- 审查者只读，输出 Critical / Important / Minor / 计划冲突四级发现
- v6 合并两阶段审查为一次 diff 通读，token 消耗减半
- 持久化进度账本支持会话中断恢复
- Parallel Dispatching 处理独立并发问题，与 SDD 互补

### 下一章预告

执行引擎需要环境保障。下一章看看 **Git Worktree 隔离**——如何在写任何代码前创建隔离工作区、验证测试基线，以及已知问题和规避方案。




---

# 第五章：Git Worktree 隔离执行

## 本章目的

Pipeline 的第 2 阶段是在写任何代码前创建隔离工作区。本章深入 Git Worktree 的 4 步流程：环境检测 → 工作区创建 → 依赖安装 → 基线验证，以及已知问题和规避方案。

---

## 5.1 为什么需要隔离

AI Agent 在同一个仓库中工作时会相互干扰：

| 问题 | 说明 |
|------|------|
| 分支冲突 | Subagent 1 切分支，Subagent 2 的 HEAD 也变了 |
| 脏状态 | 一个 agent 的未提交修改影响另一个的测试 |
| 无法回滚 | 实现出问题时，"撤销"变得复杂 |
| 测试干扰 | 一个 agent 的修改导致另一个的测试失败 |

Git Worktree 解决这些问题：每个 agent 有独立的 HEAD、Index 和分支状态，但共享同一个 `.git` 对象存储。

---

## 5.2 4 步工作流

### Step 0：环境检测

在创建任何东西之前，先检测当前是否已在隔离环境中：

```bash
# 检查是否在 worktree 中
GIT_DIR=$(git rev-parse --git-dir)
GIT_COMMON=$(git rev-parse --git-common-dir)
if [ "$GIT_DIR" != "$GIT_COMMON" ]; then
  # 已经在 worktree 中
fi

# 检查是否在 submodule 中
git rev-parse --show-superproject-working-tree

# 普通 checkout
```

三种情况：

| 当前状态 | 操作 |
|---------|------|
| 已在 Worktree | 跳过创建，直接用 |
| 在 Submodule | 视为普通仓库，不走 worktree |
| 普通 checkout | 请求用户同意后创建 |

### Step 1a：使用原生工具（优先）

如果平台提供原生 Worktree 工具（如 `EnterWorktree`、`WorktreeCreate`、`--worktree` 标志），**优先使用**。手动 `git worktree add` 会创建平台无法管理的"幽灵状态"。

### Step 1b：Git Worktree 回退

当没有原生工具时：

```bash
# 1. 检查目录是否被 gitignore
git check-ignore -q .worktrees
# 如果未被忽略，先添加到 .gitignore 并 commit

# 2. 目录优先级：
#    用户显式指定 > .worktrees/（隐藏，优先） > worktrees/

# 3. 创建 worktree
git worktree add "<path>" -b "<feature-branch>"
cd "<path>"
```

### Step 2：项目设置

自动检测项目类型并安装依赖：

| 检测文件 | 命令 |
|---------|------|
| package.json | npm install / yarn |
| Cargo.toml | cargo fetch |
| requirements.txt / pyproject.toml | pip install / poetry install |
| go.mod | go mod download |

### Step 3：基线验证

运行项目对应的测试命令，确认测试基线是干净的：

```bash
# 根据项目类型选择
npm test / cargo test / pytest / go test ./...

# 如果测试失败 → 报告用户，询问是否继续
# 不能静默地继续
```

### 输出报告

```
Worktree ready at /path/to/.worktrees/feature-x
Tests passing (142 tests, 0 failures)
Ready to implement feature-x
```

---

## 5.3 已知问题与规避

### 问题 1：Worktree 静默回退到父仓库

Claude Code 的 `isolation: "worktree"` 有时会**静默地**在父仓库中工作，而不是创建新的 worktree。Agent 以为自己隔离了，实际上没有。

**规避**：使用 clone 隔离代替 worktree 隔离：
```bash
git clone --dissociate --reference . --single-branch . "../isolated-$BRANCH"
```

### 问题 2：Subagent 分支切换改变父仓库 HEAD

在 worktree 中运行的 subagent 执行分支切换时，可能意外修改父仓库的 HEAD 指针。

**规避**：每个 subagent 创建独立的 worktree，严格隔离。不要共享 worktree。

### 问题 3：Worktree 文件被误提交

如果 `.worktrees/` 目录未被 `.gitignore` 包含，worktree 中的文件可能被意外提交到仓库。

**规避**：创建 worktree 前必须验证：
```bash
git check-ignore -q .worktrees || (echo ".worktrees" >> .gitignore && git add .gitignore && git commit -m "chore: ignore worktrees")
```

### 问题 4：macOS 环境差异

BSD 工具链与 GNU 工具链的差异（如 `date` 命令不支持纳秒），导致测试失败。

**规避**：在设计的早期阶段就识别环境差异，准备 Docker 或 CI 环境用于验证。

---

## 5.4 清理与溯源

### 溯源所有权规则

```
.worktrees/ 或 worktrees/ 下 → Agent 拥有，可以删除
其他位置的 worktree → 宿主环境拥有，不能删除
```

### 清理顺序

```
1. Merge 到目标分支
2. 运行测试确认通过
3. 删除 worktree（cd 回主仓库根目录）
4. git worktree prune
5. 删除分支
```

顺序很重要——如果先删分支再删 worktree，会导致 Git 报错。

---

## 本章小结

- Git Worktree 为每个 Subagent 提供独立的 HEAD、Index 和分支状态
- 原生工具优先，`git worktree add` 是备用方案
- 创建前验证 gitignore 状态，避免污染仓库
- 测试基线验证是门槛——基线不过不能开始实现
- 已知问题：静默回退、分支突变、macOS 差异——有对应的规避方案
- 清理顺序必须正确：merge → 测试 → 删 worktree → 删分支

### 下一章预告

隔离环境准备好后，框架如何在不同平台上工作？下一章看 **Plugin 架构与自举机制**——一个 skills 库如何部署到 10+ 个 AI 平台。




---

# 第六章：Plugin 架构与跨平台部署

## 本章目的

Superpowers 的 skills 是平台无关的，但 Agent 平台有完全不同的能力、工具和集成方式。本章看 Plugin-per-Harness 模式如何用"同一份 skills + 不同平台引导"支持 10+ 个平台。

---

## 6.1 三组件架构

整个跨平台方案基于三个不变的组件：

```
┌──────────────────────────────────────────────────────────┐
│                     Skills（平台无关）                      │
│  skills/*/SKILL.md — 描述"动作"，从不命名具体工具          │
│  在所有平台上完全相同                                     │
├──────────────────────────────────────────────────────────┤
│                    Tool Mapping（每平台）                   │
│  references/<harness>-tools.md                            │
│  将动作词汇翻译为平台的真实工具名称                          │
├──────────────────────────────────────────────────────────┤
│                    Bootstrap（每平台）                      │
│  每会话开始时将 using-superpowers + tool mapping 注入      │
│  包裹在 <EXTREMELY-IMPORTANT> 标签中                       │
└──────────────────────────────────────────────────────────┘
```

### 两条不变的规则

**规则 1：技能命名动作，不是工具**
```
✅ skills/SKILL.md 中写："派发一个 subagent"
❌ skills/SKILL.md 中写："使用 Task 工具"
```
工具映射在 references/ 中按平台解析，技能主体从不需要编辑来适配平台。

**规则 2：通过平台自身安装机制发布**
```
✅ .claude-plugin/plugin.json → Claude Code 市场
✅ .codex-plugin/plugin.json → Codex 插件系统
❌ 编辑用户的 ~/.claude/settings.json
❌ 手动复制文件到项目目录
```

---

## 6.2 Plugin-per-Harness 目录

```
superpowers/
├── .claude-plugin/plugin.json      # Claude Code
├── .codex-plugin/plugin.json       # Codex CLI
├── .cursor-plugin/plugin.json      # Cursor
├── .kimi-plugin/plugin.json        # Kimi Code
├── .opencode/plugins/superpowers.js # OpenCode
├── .pi/extensions/superpowers.ts   # pi
├── gemini-extension.json           # Gemini CLI
├── hooks/
│   ├── hooks.json                  # 钩子配置
│   └── session-start              # 自举脚本
├── references/                     # 各平台工具映射
└── skills/                         # 共享技能（14个）
```

### 平台注册差异

**Claude Code**（`.claude-plugin/plugin.json`）：

```json
{
  "name": "superpowers",
  "version": "6.1.1",
  "description": "Core skills library for Claude Code...",
  "keywords": ["skills", "tdd", "debugging"]
}
```

Claude Code 自动扫描 skills/ 目录和 hooks/hooks.json——不需要显式声明路径。

**Codex**（`.codex-plugin/plugin.json`）：

```json
{
  "name": "superpowers",
  "version": "6.1.1",
  "skills": "./skills/",
  "hooks": {},
  "interface": {
    "displayName": "Superpowers",
    "description": "...",
    "category": "Developer Tools"
  }
}
```

差异：

| 维度 | Claude Code | Codex |
|------|-------------|-------|
| 技能发现 | 自动扫描 | 需显式声明 skills 路径 |
| 钩子 | hooks/hooks.json 自动加载 | 空 hooks 对象，主动抑制钩子 |
| 界面 | 无 interface 块 | 有 interface 块用于市场展示 |
| 子 Agent | Task 工具 + 命名 agent 类型 | spawn_agent + worker 角色 |
| 安装 | 市场安装 | 市场安装 |

---

## 6.3 三种集成形态

### 形态 A：Shell-hook

**适用平台**：Claude Code、Cursor、Copilot CLI

**机制**：会话启动时运行 shell 命令，读取 stdout 注入上下文

```
用户启动会话
    ↓
平台触发 SessionStart 事件
    ↓
hooks/hooks.json 匹配 → 运行 hooks/session-start
    ↓
session-start 读取 using-superpowers/SKILL.md
    ↓
输出 JSON（含转义后的技能内容）
    ↓
平台将内容注入模型 system prompt
```

**实现要点**：
- 钩子匹配 `startup|clear|compact`（每次上下文重置时重新注入）
- 使用 `async: false` 同步执行，确保模型收到内容
- 输出 JSON 形状因平台而异（`hookSpecificOutput` vs `additionalContext`）

### 形态 B：进程内插件

**适用平台**：OpenCode、pi

**机制**：JS/TS 插件，具有会话/消息生命周期回调。在代码中构建引导内容，作为用户角色消息注入。

**实现要点**：
- 读取 SKILL.md → 去除 YAML frontmatter → 组装 `<EXTREMELY-IMPORTANT>` 标签
- 作为**用户角色消息**注入（不是系统消息——多系统消息会破坏一些模型）
- 每次 agent 步骤时检查去重标记，避免重复注入
- 压缩事件时重新注入（确保内容不被丢失）

### 形态 C：说明文件

**适用平台**：Gemini CLI

**机制**：扩展声明的上下文文件，平台始终加载。文件使用 `@`-include 语法拉入 SKILL.md 和工具映射。

**实现要点**：
- 上下文文件中 `@`-include 指向 `using-superpowers/SKILL.md`
- SKILL.md 自身携带 `<EXTREMELY-IMPORTANT>` 块
- 前端内容不去除（与形态 B 不同）
- 验证：确认 `@` 语法是保证的内联扩展，不是模型可能选择读取的文件引用

---

## 6.4 无技能工具平台的降级策略

如果平台没有原生 Skill 工具（Claude Code 的 `Skill` 工具不可用），降级方案：

1. **技能发现** → 直接读取对应 `SKILL.md` 文件
2. **技能调用** → 将读到的内容作为当前上下文的一部分
3. **文件操作** → 必要能力，无可替代
4. **Shell 命令** → 必要能力，无可替代
5. **Subagent 派发** → 可降级为内联执行或报告缺失能力

---

## 本章小结

- 三组件架构：Skills（平台无关）+ Tool Mapping（每平台）+ Bootstrap（每平台）
- 两条不变规则：技能命名动作不命名工具、通过平台安装机制发布
- Plugin-per-Harness：每个平台有独立的插件目录，共享 skills/
- 三种集成形态：Shell-hook（Claude Code）、进程内（OpenCode）、说明文件（Gemini）
- Claude Code vs Codex 核心差异：技能发现、钩子系统、Subagent 派发方式
- 无原生 Skill 工具时，可降级为直接读取 SKILL.md 文件

### 下一章预告

Plugin 架构中的核心入口——**启动钩子与自举机制**。下一章深入 hooks/session-start 脚本，看它是如何读取技能内容、转义 JSON、注入上下文的。




---

# 第七章：启动钩子与自举机制

## 本章目的

前几章我们看到 skills 系统如何工作、pipeline 如何流转、subagent 如何执行。但这一切的前提是——**框架必须在会话启动时被加载**。本章深入 hooks/session-start 脚本和 run-hook.cmd 包装器，看 Superpowers 如何实现跨平台的自动自举。

---

## 7.1 入口链

```
用户启动会话
    ↓
1. Claude Code 触发 SessionStart 事件
   - 匹配条件：startup | clear | compact
   - 每次上下文重置时重新触发
    ↓
2. hooks/hooks.json 匹配
   - 定位到 hooks/session-start 脚本
   - sync: false（模型等待）
    ↓
3. hooks/run-hook.cmd 定位 bash
   - Windows: 在标准路径找 bash.exe，再在 PATH 找
   - Unix: 直接 exec 执行
   - 找不到 bash 时静默退出 0（降级运行）
    ↓
4. hooks/session-start 执行
   - 读取 skills/using-superpowers/SKILL.md
   - 转义内容嵌入 JSON
   - 输出带 <EXTREMELY-IMPORTANT> 标签的 JSON
    ↓
5. 钩子系统将 stdout 作为 additionalContext 注入
    ↓
6. 模型现在拥有完整的 using-superpowers 技能指令
```

### 钩子触发条件

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "async": false
          }
        ]
      }
    ]
  }
}
```

- `startup` — 新会话开始
- `clear` — 清除上下文
- `compact` — 压缩上下文

每次都重新注入，保证引导内容不会被模型压缩掉。

---

## 7.2 session-start 脚本核心逻辑

脚本大致流程：

```bash
# 1. 读取 SKILL.md 全文
SKILL_CONTENT=$(cat "${SKILL_DIR}/using-superpowers/SKILL.md")

# 2. 转义 → 嵌入 JSON（通过 bash 参数替换）
# 比字符级循环快得多
ESCAPED=$(printf '%s' "$SKILL_CONTENT" | sed ...)

# 3. 组装注入内容
CONTENT="<EXTREMELY-IMPORTANT>
这是一条极其重要的系统指令，请在回应之前仔细阅读...

${SKILL_CONTENT}

## 平台适配
${TOOL_MAPPING}
</EXTREMELY-IMPORTANT>"

# 4. 输出 JSON（根据检测到的平台选择形状）
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
  # Cursor: { "additional_context": "..." }
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ] && [ -z "${COPILOT_CLI:-}" ]; then
  # Claude Code: { "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "..." } }
else
  # Copilot CLI / SDK standard: { "additionalContext": "..." }
fi
```

### JSON 形状对比

| 平台 | JSON 结构 | 说明 |
|------|----------|------|
| Claude Code | `{ hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: "..." } }` | 必须用 hookSpecificOutput 包装 |
| Cursor | `{ additional_context: "..." }` | 使用下划线命名 |
| Copilot CLI | `{ additionalContext: "..." }` | 使用驼峰命名，无包装 |

**陷阱**：输出错误的 JSON 字段名 → 引导内容永远不会注入到模型上下文中。

---

## 7.3 run-hook.cmd 跨平台设计

这是一个**单个文件**同时作为 Windows `.cmd` 脚本和 Unix Shell 脚本有效的技巧：

```
@echo off
rem ... Windows 端代码 ...
goto :CMDBLOCK

: Unix 端（被 Windows 跳过）
: << 'CMDBLOCK'
  # Unix shell 代码
  exec bash "$@"
exit
CMDBLOCK

: Windows 端继续
...
```

Windows 端：
- 在标准路径找 `bash.exe`（Git for Windows）
- 在 PATH 找
- 如果都找不到 → 静默退出 0，不阻塞会话启动
- 找到后运行对应的钩子脚本

Unix 端：
- `: << 'CMDBLOCK'` 使批处理块成为 no-op heredoc
- 直接用 `exec bash` 执行钩子脚本

### 文件命名规则

钩子脚本**无扩展名**（`session-start` 而不是 `session-start.sh`）：
- Claude Code 的 Windows 处理会在 `.sh` 扩展名前加上 `bash`
- 如果有 `.sh` 扩展名 → 最终命令是 `bash bash session-start.sh`（错误）
- 如果无扩展名 → 最终命令是 `bash session-start`（正确）

---

## 7.4 去重与重注入

### 去重机制

钩子的 `matcher: "startup|clear|compact"` 确保：

| 事件 | 是否注入 | 原因 |
|------|---------|------|
| 新会话 start | ✅ | 首次加载 |
| 用户 /clear | ✅ | 上下文被清除，需要重新注入 |
| 模型自动 compact | ✅ | 上下文被压缩，引导可能丢失 |
| 普通消息 | ❌ | 上下文未重置 |

### 进程内插件的去重

对于形态 B（进程内插件，如 OpenCode、pi），自己有额外的去重保护：

- 检查引导标记是否已存在于上下文
- 如果已存在 → 跳过注入
- 如果不存在 → 注入并设置标记
- 缓存解析后的内容，避免每次重新读取/解析

---

## 7.5 引导内容的核心声明

当 `using-superpowers` 被注入到模型上下文后，它声明了以下不可协商的规则：

```xml
<EXTREMELY-IMPORTANT>
如果你认为有哪怕 1% 的可能性某个技能适用于你正在做的事，
你绝对必须调用该技能。

如果某个技能适用于你的任务，你没有选择。你必须使用它。
这是不可协商的。你不能理性地说服自己逃脱。
</EXTREMELY-IMPORTANT>
```

加上：
- 在有任何回应或行动之前调用技能（包括澄清问题、探索代码库）
- 技能优先级：流程技能优先，然后实现技能
- 指令优先级：用户指令 > 技能 > 默认行为

以及**子代理停止指令**：

```
<SUBAGENT-STOP>
如果你是作为 subagent 被派发的，忽略 using-superpowers 技能
</SUBAGENT-STOP>
```

防止在每个 subagent 上下文中重新引导整个系统。

---

## 本章小结

- 入口链：SessionStart 事件 → hooks.json → run-hook.cmd → session-start 脚本 → 注入
- 钩子匹配 startup|clear|compact，每次上下文重置时重新注入
- run-hook.cmd 是单个文件同时支持 Windows 和 Unix 的双平台脚本
- 注入内容是 using-superpowers/SKILL.md + 平台工具映射，由 `<EXTREMELY-IMPORTANT>` 标签包裹
- Subagent 收到 `<SUBAGENT-STOP>` 指令，避免在每个 subagent 中重新引导
- 输出错误的 JSON 字段名会导致引导静默失败

### 下一章预告

理解了框架如何加载和运行，下一章看框架**如何扩展自身**——Writing-Skills 元技能。Superpowers 用 TDD 驱动文档的方法来创建新技能，这是一个元层面的方法论。




---

# 第八章：Writing-Skills — 框架的自我扩展机制

## 本章目的

前七章看的是 Superpowers 的技能**用起来**什么样子。这一章看技能**怎么写出来**。Writing-Skills 是 Superpowers 的元技能——它定义了编写新技能的方法论。最引人注目的是：这个方法论的本身是 TDD。

---

## 8.1 铁律：无失败测试 = 无技能

> 没有失败的测试优先，就没有技能。

这适用于新技能编写和现有技能的编辑。在任何技能文档（SKILL.md）被创建之前，必须先有一个**压力测试**——在无技能的情况下让 Agent 运行并观察它失败。

如果在测试之前写了技能 → **删除它，重新开始。**

| TDD 概念 | 技能创建等价物 |
|---------|--------------|
| 测试用例 | 使用子代理的压力场景（3+ 种组合） |
| 生产代码 | SKILL.md |
| RED（测试失败） | Agent 在无技能时违反规则 |
| GREEN（测试通过） | Agent 在有技能时合规 |
| REFACTOR | 在保持合规的同时堵上漏洞 |
| 先写测试 | 在写技能前运行基线场景 |
| 观察失败 | 记录 Agent 使用的确切合理化借口 |
| 最小代码 | 编写只解决特定违规行为的技能 |
| 观察通过 | 验证 Agent 现在合规 |
| 重构循环 | 找到新借口 → 堵上 → 重新验证 |

---

## 8.2 RED-GREEN-REFACTOR 循环

### RED：编写失败测试

1. **创建压力场景**
   - 纪律技能需要 3+ 种压力组合
   - 覆盖：正常路径、边缘情况、常见借口
   - 使用 subagent 执行

2. **在无技能情况下运行场景**
   - 逐字记录基线行为
   - 特别记录 Agent 用来跳过流程的"合理化借口"

3. **识别借口的模式**

例如，为 TDD 技能编写测试时，基线运行发现了这些借口：

```
"这太简单了，不需要测试" —— Agent 的借口
"我先写个快速原型，再补测试" —— Agent 的借口
"时间紧迫，先写代码" —— Agent 的借口
"这个改动太小了，不会出问题" —— Agent 的借口
```

每个借口都变成一个需要在技能中封堵的漏洞。

### GREEN：编写最小技能

1. **命名验证**：仅字母、数字、连字符
2. **Frontmatter 验证**：必须有 `name` 和 `description`，以 "Use when..." 开头
3. **关键词覆盖率**：确保涉及的关键概念都在描述中覆盖
4. **清晰的概述**：1-2 句核心原则
5. **有说服力的示例**：一个完整的示例胜过多个片段
6. **在有技能情况下运行场景** → 验证 Agent 现在合规

### REFACTOR：堵上漏洞

1. **识别测试中的新借口**
   - 无技能时记录了 N 个借口
   - 有技能后修复了 M 个，还剩 N-M 个

2. **添加显式的计数器**
   - 对于纪律技能：使用"禁止 + 借口表"而不是软性指导

3. **构建借口表**

```markdown
## 反合理化

| 你会说 | 你应该做 |
|--------|---------|
| "这太简单了" | 简单的事情会变得复杂。使用技能。 |
| "让我先看看代码" | 技能告诉你如何探索代码。先检查技能。 |
| "我记得这个技能" | 技能在进化。阅读当前版本。 |
```

4. **创建红旗列表**
   - 让 Agent 能在合理化时自我检查

5. **重新测试直到防弹**
   - 每次调用一个新鲜上下文样本
   - 始终包含一个无指导的对照
   - 每个变体 5+ 次重复（单个样本会撒谎）
   - 手动读取每个标记的匹配（自动化计数高估成功率）

---

## 8.3 指导形式选择矩阵

不同的失败形式需要不同的修复策略：

| 基线失败 | 正确形式 | 错误形式 |
|---------|---------|---------|
| 压力下跳过/违反规则 | **禁止 + 借口表 + 红旗** | 软指导（"最好..."、"考虑..."） |
| 输出形状错误 | **正面配方**：陈述输出是什么 | 禁止列表（"不要重述"） |
| 遗漏必需元素 | **结构化**：模板中必需的字段 | 模板附近的散文提醒 |
| 行为应取决于条件 | **条件语句**：以可观察谓词为条件 | 无条件规则 + 豁免条款 |

### 示例对比

**纪律技能**（如 TDD）——应该用"禁止 + 借口表"：

```markdown
## 必做
- 每个功能实现前，先写一个失败测试
- 运行测试 → 确认失败

## 禁止
- ❌ 因为"改动太小"而不写测试
- ❌ 先写实现再补测试
- ❌ 保留已写的实现代码去"适配"测试
```

**输出形状**（如"返回什么"）——应该用正面配方：

```markdown
## 输出
审查者必须返回：
1. Strengths：3-5 个正面观察
2. Issues：分级列表（Critical / Important / Minor）
3. Assessment：总体判定
```

---

## 8.4 Description 优化的关键发现

这是 writing-skills 中最有价值的经验发现之一：

> 如果 `description` 总结了技能的工作流，Agent 会**按描述走捷径**，不去读完整的 SKILL.md。

在测试中，描述说"在任务之间做代码审查，包括 spec 合规和代码质量两次审查"，Agent 看到后就认为自己知道怎么做了，**只做了一次审查**——而完整的 SKILL.md 定义的是两次。

**规则**：
- Description 只写**触发条件**，不写**过程**
- 描述"什么情况下用"，不是"用它做什么"
- 用具体的触发词、症状、情境
- 使用主动语态，以动词开头：`creating-skills` 而不是 `skill-creation`

---

## 8.5 部署检查清单

每个技能在部署前必须经过 25 项检查：

### RED 阶段（3 项）
- [ ] 压力场景已创建（纪律技能 3+ 种）
- [ ] 基线行为已记录
- [ ] 失败模式已识别

### GREEN 阶段（10 项）
- [ ] 命名验证通过（仅字母、数字、连字符）
- [ ] Frontmatter 验证通过（name + description）
- [ ] Description 以 "Use when..." 开头
- [ ] 关键词覆盖率已检查
- [ ] 清晰的概述
- [ ] 使用场景已列出
- [ ] 核心模式已说明
- [ ] 常见错误已记录
- [ ] 有效的示例
- [ ] 有技能→合规已验证

### REFACTOR 阶段（5 项）
- [ ] 借口表已构建
- [ ] 红旗列表已创建
- [ ] 反合理化已覆盖所有基线失败
- [ ] 边界情况已测试
- [ ] 防弹（5+ 重复样本验证）

### 质量检查（5 项）
- [ ] 不超过 Token 预算
- [ ] 交叉引用格式正确（`superpowers:skill-name`，非文件路径）
- [ ] 流程图仅用于非明显的决策点
- [ ] 约束力级别匹配（禁止 vs 指导 vs 参考）
- [ ] 无平台特定工具名

### 部署（2 项）
- [ ] 自动发现已验证
- [ ] 描述触发已验证

---

## 本章小结

- Writing-Skills 方法论本身是 TDD：先让 Agent 无技能失败，再编写最小技能让它通过
- RED：创建压力场景 + 记录基线 + 识别借口模式
- GREEN：编写最小 SKILL.md + 验证合规
- REFACTOR：构建借口表 + 红旗列表 + 防弹测试
- Description 只写触发条件，不总结流程（总结会破坏技能）
- 指导形式选择矩阵：不同失败类型用不同修复策略
- 部署清单 25 项，每个技能部署前必须全部通过

### 下一章预告

最后一章，把所有内容缝合起来——**如何借鉴 Superpowers 的设计模式搭建自己的 Agent 框架**。




---

# 第九章：总结 — 如何借鉴 Superpowers 搭建自己的 Agent 框架

## 本章目的

前八章我们从源码级别拆解了 Superpowers 的 7 个方向。这一章把这些内容缝合起来，提炼出可复用的设计模式，回答最初的目标：**如何借鉴这些模式来搭建自己的 Agent 框架。**

---

## 9.1 Superpowers 的核心抽象

全部分析归结为三个核心抽象：

```
约束层（Skills） → 定义 Agent 能做什么、不能做什么
编排层（Pipeline） → 定义多阶段流转和门控规则
执行层（Subagent） → 定义任务如何被隔离执行
```

这三层的关系：

```
                  ┌──────────┐
                  │  Skills  │ ← 行为约束（1% 规则、技能触发的入口）
                  │  约束层   │
                  └────┬─────┘
                       │ 触发
                  ┌────▼─────┐
                  │ Pipeline │ ← 阶段流转（7 阶段 + 9 硬门控）
                  │  编排层   │
                  └────┬─────┘
                       │ 执行
                  ┌────▼─────┐
                  │Subagent  │ ← 任务执行（隔离 + 审查 + 状态报告）
                  │  执行层   │
                  └──────────┘
```

---

## 9.2 可复用的设计模式

### 模式 1：硬门控 Pipeline

**问题**：Agent 需要在多阶段流程中工作，但会找借口跳过步骤。

**Superpowers 的方案**：每个阶段之间设置二进制门控——不满足条件不能进入下一阶段。

**可复用的实现方式**：

```
阶段 N → [门控条件] → 通过 → 阶段 N+1
              │
              └─ 不通过 → 停留在阶段 N
```

门控类型：

| 门控类型 | 例子 | 实现方式 |
|---------|------|---------|
| 用户审批 | "设计稿需要用户确认" | 等待用户输入 Y/N |
| 工具验证 | "测试必须通过 test runner" | Bash 运行测试，检查 exit code |
| 文件存在 | "计划文件必须存在" | 检查文件是否存在 |
| 内容确认 | "无 TODO/TBD 占位符" | grep 检查文件内容 |

**在自己的框架中**：在你的概念文件中定义阶段数组 + 阶段间的门控条件列表。每个阶段执行前检查门控，不通过就停在当前阶段。

### 模式 2：Subagent 隔离执行

**问题**：在同一个会话中累积执行多个任务，上下文越来越重，Agent 注意力下降。

**Superpowers 的方案**：每个任务派发一个全新 subagent，隔离上下文。Subagent 返回四种状态之一。

**可复用的实现方式**：

```
for each 任务:
  1. 将任务需求写入独立文件 (task-N-brief.md)
  2. 派发 subagent，传递 brief 文件路径
  3. Subagent 执行并返回状态（DONE / BLOCKED / NEEDS_CONTEXT）
  4. 如果是 DONE → 派发审查 subagent
  5. 根据审查结果决定是否进入下一个任务
```

**关键原则**：
- Subagent 不读取整个计划文件，只读自己的 brief
- Dispatch 消息只描述一个任务，不是会话历史
- 审查者只读，不能修改代码

### 模式 3：1% 规则自举

**问题**：框架只有在加载后才能工作，但加载需要 Agent 主动去做——这形成了一个先有鸡还是先有蛋的问题。

**Superpowers 的方案**：在会话启动时通过钩子系统注入引导指令，声明 1% 规则。

**可复用的实现方式**：

```
在会话开始时注入：
  <CRITICAL>
  如果当前有任何规则/技能可能适用于你的任务，
  你必须在任何行动之前加载它。
  </CRITICAL>
```

1. 如果你的平台支持钩子（SessionStart）→ 用钩子注入
2. 如果不支持 → 在项目根目录放一个 `CLAUDE.md`，写入引导指令
3. 或者在每次任务的 prompt 中首行声明规则

### 模式 4：TDD 驱动文档

**问题**：规则文档（SKILL.md）可能不起作用——Agent 可能不看，或者看了走捷径。

**Superpowers 的方案**：用 TDD 方法编写文档。先让 Agent 在没有文档的情况下运行压力测试，观察它如何失败，然后编写刚好的文档来堵住这些失败路径。

**可复用的实现方式**：

```
1. 定义你要约束的行为（如："必须先写测试再写代码"）
2. 创建压力测试场景（让 Agent 自由发挥，观察它找什么借口）
3. 记录所有借口的列表
4. 编写针对每个借口的禁止规则
5. 重新运行测试 → 验证 Agent 合规
6. 重复直到防弹
```

### 模式 5：规则优先级体系

**问题**：项目可能有多个规则来源（CLAUDE.md、SKILL.md、用户实时指令），Agent 不知道应该听谁的。

**Superpowers 的方案**：明确的优先级：用户指令 > 技能 > 默认行为。

**可复用的实现方式**：

```markdown
## 指令优先级
1. 用户/项目明确指令（CLAUDE.md, AGENTS.md）→ 最高
2. 本框架的技能规则（SKILL.md）→ 其次
3. 模型默认行为 → 最低

只有用户明确说"跳过"，才能跳过规则。
```

---

## 9.3 架构决策清单

搭建自己的 Agent 框架时，需要回答以下问题：

### 基础层
- [ ] **约束机制**：用硬门控还是软规则？什么场景用什么？
- [ ] **触发方式**：技能自动触发还是手动调用？如何避免 Agent 跳过？
- [ ] **优先级**：多个规则冲突时，按什么顺序裁决？

### 执行层
- [ ] **Subagent**：是否支持 subagent 派发？如何隔离上下文？
- [ ] **模型选择**：不同任务用不同模型，还是统一模型？
- [ ] **状态报告**：Subagent 如何报告状态？四种够吗？需要更多吗？

### 质量层
- [ ] **审查机制**：审查者只读还是可修改？发现如何分级？
- [ ] **TDD 强制**：测试驱动开发是可选的还是强制的？
- [ ] **审计线索**：如何追踪 agent 的决策和工作成果？

### 平台层
- [ ] **跨平台**：规则是否需要跨平台？如何做工具映射？
- [ ] **自举**：规则如何在会话启动时加载？
- [ ] **扩展性**：如何让用户添加新规则/技能？

---

## 9.4 与主流框架的对比

| 维度 | Superpowers | Matt Pocock Skills | Agent Skills (Addy Osmani) | 你自己的框架 |
|------|-------------|-------------------|--------------------------|------------|
| 哲学 | 流程纪律 | 流程工具 | 多角色审查 | _由你定义_ |
| 门控强度 | 硬（不可跳过） | 软（可选） | 中（并行审查） | _按需选择_ |
| 自动触发 | 是（1% 规则） | 否（12/18 隐藏） | 部分 | _看场景_ |
| Token 成本 | 高 | 低 | 中 | _平衡_ |
| 学习曲线 | 陡 | 平 | 中 | _由你控制_ |
| 最佳场景 | 长周期、高质量 | 快速澄清 | 企业级验证 | _匹配需求_ |

三种框架的选择不是好坏之分，而是**适用场景**之分。对于自己的框架，你可能不需要 1:1 复制 Superpowers——关键是从中提取**适合你场景**的模式。

---

## 9.5 实际效果参考

### Superpowers 在真实项目中的数据

| 项目 | 指标 | 效果 |
|------|------|------|
| chardet v7.0.0 | 2,161 测试文件，99 种编码 | 41 倍性能提升，准确率 94.5%→96.8% |
| Builder.io 告警守护进程 | 17 文件 26 任务 | 审查捕获 1 个命名不一致，100 个延迟样本全部通过 |
| 电话答录机系统 | 首晚 | Brainstorm + Spec + Plan + 3 CDK stacks + 4 Lambda + 测试 + CI |
| 一般开发效率 | 需求确认 / 返工 / 单模块耗时 | 方向跑偏→先问关键问题；3-4 轮→1 次；40 分→15 分（60%+ 提升） |

### 局限性

- **Token 消耗大**：完整 pipeline 的 token 开销显著（v6 正在优化）
- **小改动过重**：改一行文案走 7 阶段 pipeline 不合理
- **线性化流程**：强制顺序执行，不适合所有工作类型
- **已知 bug**：Claude Code worktree 隔离有静默回退问题
- **跨平台有缝**：不同平台的能力差异需要额外映射

---

## 9.6 你的下一步

如果你要搭建自己的 Agent 框架，建议的路径：

### 阶段 1：先在一个平台跑通最小闭环
1. 写一个 `CLAUDE.md` 声明 1-2 条核心规则
2. 用 hook 或项目文件注入引导
3. 验证 Agent 遵守规则

### 阶段 2：增加 Pipeline
1. 定义 3-5 个阶段（简化版）
2. 每个阶段之间设一个门控
3. 每个阶段结束时让用户确认

### 阶段 3：增加 Subagent
1. 把长任务拆成短任务
2. 每个任务派发 subagent
3. 添加审查者

### 阶段 4：平台化
1. 提取规则为独立的 SKILL.md
2. 添加 Plugin 注册
3. 做工具映射支持更多平台

---

## 全篇总结

### 关键原则

1. **硬门控 > 软规则** — Agent 会找借口，门控是唯一的保障
2. **先测试，再代码** — 没有失败测试就没有生产代码
3. **上下文隔离** — 每个 subagent 新鲜执行，不让会话历史累积污染
4. **描述只写触发，不写过程** — 否则 Agent 会走捷径
5. **TDD 驱动文档** — 先观察失败再写规则，不是凭想象写规则
6. **1% 规则自举** — 框架的启动由规则自身声明

### 7 个方向回顾

| 方向 | 学到什么 |
|------|---------|
| Workflow Pipeline | 7 阶段硬门控、9 个门控表、防跳过多层机制 |
| Subagent Dispatching | SDD 流程、四种状态、模型分层、审查只读 |
| Git Worktree 隔离 | 前置门控、清理规则、已知 bug 规避 |
| Skills 系统设计 | SKILL.md 结构、触发机制、描述优化陷阱 |
| Plugin 架构 | 三组件架构、三种集成形态、平台差异 |
| 启动钩子与自举 | 入口链、双平台脚本、去重重注入 |
| Writing-Skills | TDD 驱动文档、防弹技能、25 项部署清单 |

### 最后

Superpowers 不是一个你可以直接"安装就能用"的工具——它是一种**方法论的系统化表达**。理解了它的设计哲学，你就可以在自己的项目中应用这些模式：不管你用的是 Claude Code、Codex 还是其他 Agent 平台，Pipeline 的思维、Subagent 的隔离、硬门控的约束——这些原则是跨平台的。

