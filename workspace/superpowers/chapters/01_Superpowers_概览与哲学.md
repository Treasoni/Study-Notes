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
