---
title: "Matt Pocock Skills — Agent 框架设计深度解析"
subtitle: "从 184K+ Stars 仓库中提取可复用的 Agent 技能设计方法论"
tags:
  - agent-framework
  - skill-design
  - llm-patterns
  - matt-pocock
  - architecture
created: 2026-07-23
updated: 2026-07-23
status: completed
source_project: matt-pocock-skills
source_repo: https://github.com/mattpocock/skills.git
note_type: concept + practice
learning_depth: mastery
---

# Matt Pocock Skills — Agent 框架设计深度解析

> **副标题**：从 184K+ Stars 仓库中提取可复用的 Agent 技能设计方法论

本笔记系统拆解 Matt Pocock 的 skills 仓库——一个 184K+ Stars 的开源项目，专门存放高质量 Agent 技能（skills）。全书共 8 章，从前 7 章对仓库的逐层拆解，到第 8 章的综合应用指南，回答一个核心问题：**如何用工程纪律驯服 Agent，使其输出从"随机"变为"可预测"？**

**核心目标**：不仅理解 Matt 的设计模式，更将其应用于构建你自己的 Agent 项目框架。

---

## 目录

- [第 1 章：项目概览与设计哲学](#第-1-章项目概览与设计哲学)
- [第 2 章：仓库架构与目录组织](#第-2-章仓库架构与目录组织)
- [第 3 章：调用模型深度解析](#第-3-章调用模型深度解析)
- [第 4 章：SKILL.md 编写艺术](#第-4-章skillmd-编写艺术)
- [第 5 章：对话边界澄清 — Socratic Sparring 模式](#第-5-章对话边界澄清--socratic-sparring-模式)
- [第 6 章：上下文管理 — Handoff 与 Context Compaction](#第-6-章上下文管理--handoff-与-context-compaction)
- [第 7 章：可组合工作流设计](#第-7-章可组合工作流设计)
- [第 8 章：实战应用 — 构建你自己的 Agent 框架](#第-8-章实战应用--构建你自己的-agent-框架)

---

# 第 1 章：项目概览与设计哲学

> 素材引用: [R1], [R2], [R3], [R4]

## 1.1 Skills 仓库不是什么

在深入了解之前，先明确边界。

Matt Pocock 的 skills 仓库**不是**一个 SDK、**不是**一个库、也**不是**一个 CLI 工具。它是一个**可分发、可复用的 Agent 指令集**——一系列 Markdown 文件，告诉 AI Agent（特别是 Claude Code）在特定场景下应该怎么做。

这意味着：
- **不需要 import**：没有 npm install 的过程
- **不需要编译**：纯 Markdown，人类和 AI 都能读
- **不是黑盒**：每个 skill 的内容完全开放，你可以逐行审查

## 1.2 四大问题域

Matt 的设计解决的不只是一个问题，而是四个完全不同类型的问题。理解这四个问题域是理解整个体系的关键。

| 问题域 | 核心问题 | Matt 的方案 | 关键概念 |
|--------|---------|-------------|---------|
| 认知负载 | 用户记不住所有 Skill | Router + 命名约定 | Cognitive Load |
| 上下文负载 | 每轮调用消耗 token | Model-invoked description | Context Load |
| 可预测性 | Agent 行为不一致 | Completion Criterion | Predictability |
| 分发 | 怎么分享 Skill | Plugin + Market Place | Bucketed Curation |

如果要找一句话总结 Matt 的整个设计哲学，就是：**在 Agent 框架中，每一次不确定性都是有代价的——要么消耗用户的认知，要么消耗模型的上下文。**

## 1.3 核心设计哲学

### 四大原则

**原则 1：小胜于大**

超过 100 行的 skill 需要修剪或拆分。小的 skill 更容易维护、审计和替换。

**原则 2：语言即架构**

共享的精准术语比冗长的解释更有价值。Leading words 是这一原则的极致体现。

**原则 3：边界即纪律**

每一道边界（User/Model 调用边界、事实/决策边界、思考/执行边界）都减少了 Agent 的不确定性。

**原则 4：修剪胜于添加**

好的 skill 是通过持续删除而非持续增加来塑造的。No-op test 是最强大的修剪工具。

## 1.4 关键数据

- **仓库规模**：184K+ Stars
- **Skill 数量**：约 20 个 active skills + 数个 deprecated
- **核心 Skill（grilling）**：仅 12 行
- **对比**：同类项目 "superpowers" 用了 689 行实现类似功能
- **发布渠道**：Claude Code Plugin + Marketplace + 社区 fork

---

# 第 2 章：仓库架构与目录组织

> 素材引用: [R1], [R3], [R4], [R5], [E3]

## 2.1 Bucketed Curation 的核心思想

Matt 仓库的目录结构看起来很简单，但背后有一个核心概念：**Bucketed Curation（分桶管理）**——用目录结构而非配置文件来管理技能的发布状态。

### 目录结构

```
skills/
├── engineering/     # 工程实践（已推广）
│   ├── implement/
│   ├── tdd/
│   ├── code-review/
│   └── diagnosing-bugs/
├── productivity/    # 生产力（已推广）
│   ├── grill-me/
│   ├── grill-with-docs/
│   ├── wayfinder/
│   └── research/
├── misc/            # 杂项（已推广）
│   ├── handoff/
│   ├── compact/
│   └── teach/
├── personal/        # 个人工具
├── in-progress/     # 草稿
└── deprecated/      # 废弃
```

"promoted" 目录中的 skill 是稳定的、面向用户的。"in-progress" 中的是还在试的草稿。Matt 每月检查一次 in-progress 目录——promote 成熟的，删除没用的，标注废弃的。

## 2.2 宪法文件体系

Matt 的仓库有三份顶层文件，合起来构成整个系统的"宪法"。

### CLAUDE.md

CLAUDE.md 是 Claude Code 的默认系统指令，定义了结构规则、调用规则、维护纪律。它只定义"结构"而不定义"内容"——什么放在哪个目录、怎么命名、什么可以提交什么不可以。

### AGENTS.md

Claude Code 独有的跨平台契约。结构与 CLAUDE.md 相同，但会被 Codex 忽略，反之亦然。两份文件保持内容一致。

### CONTEXT.md（没有独立的文件，但概念贯穿）

定义核心术语、Avoid 指令、关系模型。在 Matt 的体系中，CONTEXT.md 是给 AI 读的词典——确保所有 skill 用同样的语言描述事物。

## 2.3 双分发机制

Matt 的仓库设计了一套双分发架构：

**Claude Code Plugin（优先）**
- 通过 skills.sh 脚本安装
- 创建符号链接到 `~/.claude/skills/`
- 支持 `disable-model-invocation` 前端的 skill
- 用户键入 `/skill-name` 触发

**Codex 兼容**
- 通过 `.codex/skills/` 目录同步
- 通过 `sync-codex-to-claude.sh` 双向同步脚本
- AGENTS.md 作为跨平台入口

ADR-0002 记录了平台差异处理策略：Claude Code 优先，Codex 适配后续。

## 2.4 ADR 目录

Matt 在 `.agents/adr/` 中记录了关键的架构决策：

**ADR-0001**：Hard/soft dependencies for setup pointers
- **Hard dependencies**：Agent 必须先执行的 skill
- **Soft dependencies**：Agent 可以考虑但不必须的 skill

**ADR-0002**：Platform-specific distribution
- Claude Code 现在优先（plugin 分发）
- Codex 适配后续（通过 AGENTS.md + 同步脚本）

---

# 第 3 章：调用模型深度解析

> 素材引用: [R1], [R5], [E1], [E2]

## 3.1 核心二分法

这是整个技能设计体系中最基础的架构决策。每个 skill 都有且仅有一种调用方式：**User-invoked** 或 **Model-invoked**。

### User-Invoked（用户调用）

- **触发方式**：用户键入 `/skill-name`
- **认知负载**：高（用户需要记住这个 skill 的存在）
- **上下文负载**：零（不占 description 的 token）
- **互相不可见**：user-invoked skills 不能互相调用

### Model-Invoked（模型调用）

- **触发方式**：模型根据对话内容自动触发
- **认知负载**：零（用户不需要知道它的存在）
- **上下文负载**：高（description 在每轮对话中都消耗 token）
- **互相可见**：可以被其他 skill 调用

### 决策树

```
需要 Agent 自主触发？ → Model-invoked（付 context load）
其他 skill 需要调用它？ → Model-invoked
否则 → User-invoked（付 cognitive load）
```

## 3.2 Invocation 设置方式

在 SKILL.md 的 frontmatter 中通过 `disable-model-invocation` 控制：

```yaml
# User-invoked（显式禁用模型调用）
disable-model-invocation: true

# Model-invoked（默认，省略该字段）
# 不需要写 disable-model-invocation: false
```

## 3.3 认知负载 vs 上下文负载

这是 Matt 体系中最核心的权衡。

**认知负载（Cognitive Load）**：用户必须记住 skill 存在的负担。每个 user-invoked skill 都在用户的"技能清单"上占据一个位置。当用户记不住有哪些 skill 时，就需要 router。

**上下文负载（Context Load）**：模型每次处理 description 消耗的 token。每个 model-invoked skill 的 description 都在每轮对话中被读取。当 model-invoked skills 太多时，上下文被大量 description 占据。

**平衡策略**：
- 超过 5-7 个 user-invoked → 引入 router
- 多个 model-invoked → 缩减 description 长度
- 核心路径上的 model-invoked → 优先保 description quality

## 3.4 调用边界规则

这是 Matt 体系中一条硬性的架构规则：

> User-invoked → Model-invoked → 共享参考，不可逆向。

即：
- User-invoked 可以调用 Model-invoked ✓
- Model-invoked 可以引用共享参考 ✓
- User-invoked 调用另一个 User-invoked ✗（架构违规）
- Model-invoked 调用 User-invoked ✗（逻辑不通）

这意味着 user-invoked skills 之间如果需要共享逻辑，必须通过 model-invoked skill 或共享的 reference 文件间接引用。

## 3.5 Router 模式

当 user-invoked 技能数量超过用户的记忆上限（约 5-7 个）时，需要 router。

**ask-matt 的设计原则**：
1. **User-invoked** — 不占 context load
2. **不执行，只指路** — 告诉你去哪个 skill，但不帮你调用
3. **条件分支** — 判断条件嵌入在 router 的描述中
4. **上下文纪律** — 明确何时用同一个窗口、何时新会话

Router 本身也是一个 user-invoked skill。它的存在是为了让用户只需要记住一个 skill（/ask-matt）就能找到所有 skill。

---

# 第 4 章：SKILL.md 编写艺术

> 素材引用: [R6], [R7], [E4], [E6]
> 核心参考: writing-great-skills/SKILL.md + GLOSSARY.md

## 4.1 核心美德：可预测性

> "A skill exists to wrangle determinism out of a stochastic system."

可预测性（Predictability）不是指每次都产生相同输出，而是指 Agent 每次运行都遵循**相同的过程**。

GLOSSARY.md 明确禁止这些替代词：

> 不用：consistency, reliability, robustness, output-determinism

因为这些词暗示输出层面的重复性，而非过程层面的重复性。

### 可预测性是一切设计决策的衡量标准

- 信息层级 → 减少 Agent 在"该从哪里读"上的随机性
- Completion Criterion → 减少 Agent 在"该不该继续"上的随机性
- Leading Words → 减少 Agent 在"用什么方式思考"上的随机性
- 修剪 → 减少 Agent 在"该执行哪条指令"上的随机性

## 4.2 信息层级

内容按"Agent 需要它的紧急程度"分为三个梯级：

```
梯级 1: In-Skill Step          ← 最紧急，Agent 直接执行
   SKILL.md 中的有序动作

梯级 2: In-Skill Reference     ← 按需查阅
   SKILL.md 中的定义、规则、事实

梯级 3: External Reference     ← 仅当 context pointer 触发
   从 SKILL.md 推到独立文件
```

### Progressive Disclosure（渐进式披露）

把细节沿梯级向下推，保持顶层可读。什么样的细节该向下推？看是否所有分支都需要它：

- **所有分支都需要** → 留在行内 step/reference
- **仅某些分支需要** → 推到外部 reference，通过 context pointer 按需加载

### Context Pointer 的措辞

```
# 好的 pointer
See [GLOSSARY.md](GLOSSARY.md) for the meaning of bold terms.

# 差的 pointer
More information is available in the reference file if needed.
```

## 4.3 Completion Criterion（完成标准）

每个 step 都必须有一个完成标准，防止 Agent **过早完成**（premature completion）。

两个维度：

**Clarity（清晰度）**：Agent 能否明确判断完成与否？
```
# 清晰（好的）
"All modified models accounted for in the migration doc"

# 模糊（差的）
"Understanding reached"
```

**Demand（要求度）**：完成标准需要 Agent 做多少 Legwork？
```
# 高 demand（好的）
"Every error path covered by a test case"

# 低 demand（差的）
"Write tests for the main feature"
```

最强的完成标准是**既可检查又穷尽**。

## 4.4 Leading Words（引导词）

这是 Matt 体系中最巧妙的设计。**Leading word** 是一个"已经存在于模型预训练中的紧凑概念"，Agent 用它来思考。

| 好的 Leading Word | 替代的冗长描述 |
|---|---|
| `tight` | "fast, deterministic, low-overhead" |
| `relentless` | "thorough, no-stone-unturned" |
| `red` | "a loop you believe in" |
| `lesson` | "a reusable insight from experience" |
| `fog of war` | "decisions that depend on other decisions" |
| `tracer bullet` | "a thin end-to-end slice that validates the approach" |

**自制 Leading Word 的陷阱**：
> "Coining your own works if you define it clearly, but a made-up word recruits no priors — you pay in definition tokens what a pretrained word gives free."

## 4.5 修剪原则

### Single Source of Truth（单一真相源）

每个含义只在一个权威位置。如果一个概念出现在多个 SKILL.md 中，提取到共享的 model-invoked reference skill 或 CONTEXT.md 中。

### No-Op Test

> "Does it change behavior versus the default?"

```
# No-op（Agent 本来就会这么做）
"Write clean, well-structured code."

# 非 no-op（明确了具体方向）
"Prefer small, focused modules over large utility files."
```

## 4.6 六种失败模式

| # | 失败模式 | 定义 | 修复方案 |
|---|---------|------|---------|
| 1 | **Premature Completion** | Agent 提前结束步骤 | 强化 completion criterion |
| 2 | **Duplication** | 同一含义多个位置 | 归并到单一真相源 |
| 3 | **Sediment** | 过时内容沉淀 | 定期修剪 |
| 4 | **Sprawl** | SKILL.md 长度失控 | 使用信息层级拆分 |
| 5 | **No-Op** | 指令不改变行为 | 删除（大多数救不了） |
| 6 | **Negation** | 否定指令强化目标行为 | 正面表述替代 |

## 4.7 质量关卡

| # | 关卡 | 检查方法 |
|---|------|---------|
| 1 | Description 含触发词 | 是否包含 "Use when..." |
| 2 | SKILL.md ≤ 100 行 | `wc -l SKILL.md` |
| 3 | 无时间敏感信息 | 检查版本号、日期、过时 API |
| 4 | 术语一致 | 检查同义词替代 |
| 5 | 含具体示例 | 检查代码示例或使用场景 |
| 6 | 引用仅一级深度 | 检查 reference 文件是否再有 reference |

## 4.8 高质量 SKILL.md 模板

```markdown
---
name: my-skill
description: >-
  Use when [触发场景 1], [触发场景 2], or [触发场景 3].
  [Leading word 放在描述开头]
disable-model-invocation: true
argument-hint: "[参数说明]"
---

# My Skill

[1-2 句话的核心行为描述，包含 leading word]

## Steps

1. **[第一步名称]**
   - [具体动作 1]
   - [具体动作 2]
   **完成标准**: [可检查且穷尽的条件]

2. **[第二步名称]**
   - [具体动作]
   **完成标准**: [可检查且穷尽的条件]

## Rules

- **[关键规则 1]**: [清晰定义，含具体示例]
- **[关键规则 2]**: [清晰定义]
- **正面表述**所有规则

## Reference

See [GLOSSARY.md](GLOSSARY.md) for core vocabulary.
```

---

# 第 5 章：对话边界澄清 — Socratic Sparring 模式

> 素材引用: [R8], [R9], [R10], [E2], [E3]

## 5.1 三层抽象架构

Matt 围绕"盘问"这个行为设计了三个不同的 skill，体现了精妙的分层抽象：

```
用户层 (User-Invoked):
┌──────────────────────────────────────────────────┐
│  grill-me          grill-with-docs                │
│  (3行, 无状态)     (3行, 有状态)                  │
└──────────────────────────────────────────────────┘
        │                   │
        └────────┬──────────┘
                 ▼
核心层 (Model-Invoked):
┌──────────────────────────────────────────────────┐
│  grilling (10行)                                  │
│  核心盘问原语                                     │
└──────────────────────────────────────────────────┘
                 │
                 ▼
状态层 (Model-Invoked):
┌──────────────────────────────────────────────────┐
│  domain-modeling                                   │
│  生成 CONTEXT.md + ADR                             │
└──────────────────────────────────────────────────┘
```

### 为什么需要三层？

因为**行为相同但状态策略不同**。
- `grill-me`：无状态，跑完就结束
- `grill-with-docs`：有状态，每做一个决策就写进 CONTEXT.md 和 ADR

## 5.2 Grilling 核心原语详解

grilling 完整内容仅 10 行指令：

```markdown
1. Interview me relentlessly about every aspect of this
2. until we reach a shared understanding.
3. Walk down each branch of the decision tree,
4. resolving dependencies between decisions one-by-one.
5. For each question, provide your recommended answer.
6. Ask the questions one at a time,
7. waiting for feedback on each question before continuing.
8. Asking multiple questions at once is bewildering.
9. If a fact can be found by exploring the environment,
   look it up rather than asking me.
10. The decisions, though, are mine --
    put each one to me and wait for my answer.
11. Do not act on it until I confirm
    we have reached a shared understanding.
```

### 关键设计点

**第 1 句**：`relentlessly` 是 leading word。不是普通的 interview，是不放弃、不遗漏、穷尽的 interview。

**第 5 句**：推荐答案是最关键的设计决策。Agent 给出自己的推荐答案，用户只需要确认/修正/拒绝。这把"开放式问题"变成了"选择题"。

**第 9 句**：事实/决策的边界划分——"Facts → look up, Decisions → ask me"。不浪费用户时间去回答 Agent 能从环境找到的信息。

## 5.3 为什么 12 行就够了

1. **"Grill" 是 Leading Word**：这个词在模型预训练中承载了大量含义
2. **决策树遍历是已知模式**：模型在预训练中已经知道
3. **推荐答案减少模糊性**：选择题比填空题省力
4. **事实/决策边界**：排除 Agent 最常见的偷懒行为

## 5.4 有状态 vs 无状态设计

| 维度 | grill-me（无状态） | grill-with-docs（有状态） |
|------|-------------------|------------------------|
| 适用场景 | 纯 brainstorming，不留痕迹 | 正式工作，需记录决策 |
| 行为 | 跑完 grilling 就结束 | 跑完后调用 domain-modeling |
| 输出 | 无 | CONTEXT.md + ADR |

**模式复用**：不是"盘问"才会用到这个分层。任何"有时需要保存、有时不需要"的操作都可以用这个模式。

---

# 第 6 章：上下文管理 — Handoff 与 Context Compaction

> 素材引用: [R11], [R12], [E2], [E3]

## 6.1 Context Hygiene（上下文卫生）

Matt 在 ask-matt 的 router skill 中明确规定了上下文纪律：

```
同一个窗口完成（不分叉）：
  1. /grill-with-docs  — 盘问对齐
  2. /to-spec          — 生成规格说明
  3. /to-tickets       — 拆分为任务
  ── 在此之后可以 compact 或 handoff ──

新会话开始（每个任务）：
  4a. /implement (ticket 1)  ← 新会话
  4b. /implement (ticket 2)  ← 新会话
  4c. /implement (ticket 3)  ← 新会话
```

为什么前 3 步要在一个窗口完成？因为它们是**互相依赖的认知工作**。盘问产生的理解是规格说明的输入，规格说明又是任务拆分的输入。

为什么每个 implement 要新会话？因为实现是**执行性的工作**，只需要规格，不需要盘问的完整细节。

### Smart Zone

约 **12 万 token**——模型还能清晰推理的窗口范围。接近上限时用 handoff 分叉，不要推着 Agent 在退化状态下工作。

## 6.2 Handoff 机制详解

Handoff 的完整实现只有 7 条规则：

```markdown
1. Write a handoff document summarising the current conversation
   so a fresh agent can continue the work.
2. Save to the temporary directory — not the current workspace.
3. Include a "suggested skills" section.
4. Do not duplicate content already captured in other artifacts.
   Reference them by path or URL instead.
5. Redact any sensitive information.
6. If the user passed arguments, treat them as a description of
   what the next session will focus on.
```

### 逐条分析

**规则 1**：保存到临时目录而非工作区——交接文档是临时的，读一次后无价值。

**规则 2**：包含 "suggested skills"——这是最巧妙的规则。不仅告诉新 Agent 之前发生了什么，还告诉它接下来该用什么 skill。

**规则 3**：不重复已有内容——交接文档是索引，不是仓库。已有文件通过路径引用。

**规则 5**：参数定制——支持 `argument-hint`，只生成下一个 session 需要的部分。

## 6.3 Handoff vs Built-in Compact

| 维度 | Handoff | Compact |
|------|---------|---------|
| 方向 | 分叉 → 新会话 | 继续 → 同会话 |
| 输出 | 结构化 Markdown 文档 | 内置上下文摘要 |
| 可控性 | 高 | 低 |
| 丢失风险 | 低（显式包含） | 中（可能被摘要丢失） |
| 适用场景 | 长时间中断、大任务分拆 | 阶段间平滑过渡 |

**实用原则**：不想丢失任何细节时用 handoff，愿意接受一定程度摘要时用 compact。

## 6.4 Handoff 文档模板

```markdown
# Handoff: [项目/任务名称]

## 当前状态
[1-2 段描述已完成的步骤、进行中的工作]

## 关键决策
- [决策 1]: [内容]，记录在 [ADR 路径]

## 未完成的工作
- [剩余步骤 1]

## 参考文件
- [路径/URL 1] — [说明]

## 建议使用的 Skills
- `/grilling` — 如果还有未决问题
- `/implement` — 下一阶段是落地实现
```

---

# 第 7 章：可组合工作流设计

> 素材引用: [R12], [R13], [R14], [E1]

## 7.1 ask-matt 路由器 — 工作流的"全息图"

ask-matt 是所有 user-invoked skills 的中央路由器。它的核心设计原则是：**你不需要记住所有 skill，只需要记住 `/ask-matt`。**

### 功能地图

```
主流程 (Main Flow): idea → ship
  1. /grill-with-docs → 盘问对齐
  2. 分支: 需要原型? → handoff → /prototype → handoff 回来
  3. 分支: 多会话构建?
     ├── 是 → /to-spec → /to-tickets → 每 ticket /implement
     └── 否 → 直接 /implement
  4. 每个 /implement 内部链: /tdd → typecheck → test → /code-review → commit
```

### 什么时候需要 Router

- **不需要**：<5 个 user-invoked skills
- **考虑**：5-10 个，偶尔犹豫
- **必须**：>10 个，经常查找

Matt 说：大多数用户只需要 4 个核心 skill（grill-with-docs、to-spec、implement、code-review）就能覆盖 80% 的工作流。

## 7.2 Implement 管线

Implement 是"从想法到代码"的最终执行者。它用户触发的 user-invoked skill，内部委托给 model-invoked skills：

```
/implement (user-invoked)
  ├── 使用 → /tdd (model-invoked)
  │     └── red-green-refactor 循环
  ├── 类型检查 → 单测 → 全量测试
  ├── 使用 → /code-review (model-invoked)
  └── commit
```

### Pre-agreed Seams（预约定边界）

Implement 的核心设计概念：**在实现之前，已经通过盘问和规格确定了两件事：**
1. 测试边界：在哪层接口上测试
2. 交付顺序：tickets 的依赖顺序已解决

Implement 不做决策，只执行。它是"手，不是头"。

## 7.3 词汇表即架构 — codebase-design

codebase-design 是一个不包含步骤、全部是参考的 model-invoked skill。

| 术语 | 定义 | 禁止词 |
|------|------|--------|
| Module | 有 interface 和 implementation 的任何东西 | unit, component, service |
| Interface | 调用者必须知道的所有信息 | API, signature |
| Depth | 每单位 interface 能调用的行为量 | — |
| Seam | 可改变行为而无需在那里编辑的地方 | boundary |

### 删除测试（Deletion Test）

> "Imagine deleting the module. If complexity vanishes, it was a pass-through. If complexity reappears across N callers, it was earning its keep."

## 7.4 三种组合模式

### 模式 1：链式委托（Chained Delegation）

User-invoked → Model-invoked 的单向调用。

```
grill-me → grilling
implement → tdd → code-review
```

### 模式 2：状态组合（Stateful Composition）

相同行为核心 + 不同状态策略。

```
grill-me (无状态) → grilling
grill-with-docs (有状态) → grilling + domain-modeling
```

### 模式 3：并行子代理（Parallel Sub-Agents）

多 Agent 从不同角度同时工作。

```
code-review:
  ├── 子代理 1: 代码规范
  └── 子代理 2: 规格一致性
```

| 你的需求 | 用什么模式 |
|---------|----------|
| 入口 skill 调用内部逻辑 | 链式委托 |
| 同一行为有/无持久化 | 状态组合 |
| 多角度评审 | 并行子代理 |

---

# 第 8 章：实战应用 — 构建你自己的 Agent 框架

> 素材引用: 全章综合

这是全书的最终章。前 7 章拆解了 Matt Pocock 的设计模式，这章回答这个问题：**你要怎么把这些模式用到自己的 Agent 框架中？**

## 8.1 设计原则清单

从前 7 章提炼出的核心原则：

### 1. Bucketed Curation

**原则**：用目录结构管理发布状态，而非配置文件。

```
your-framework/
  skills/
    promoted/       # 已发布、面向用户的技能
    experimental/   # 在试的草稿
    personal/       # 你私人的工具
    deprecated/     # 不再使用
```

**检查**：每月检查一次 experimental 目录——promote 成熟的，删除没用的，标注废弃的。

### 2. Invocation 二分法

**原则**：User-invoked（付认知负载）vs Model-invoked（付上下文负载）。

每个新 skill 跑一遍决策树——

```
需要 Agent 自主触发？→ Model-invoked
其他 skill 需要调用它？→ Model-invoked
否则 → User-invoked
```

### 3. 单一真相源

**原则**：每个含义只在一个权威位置。

如果同一个概念在两个 SKILL.md 中出现，提取到 CONTEXT.md 或共享 reference skill。

### 4. 信息层级

**原则**：Skill 内容按"Agent 需要它的紧急程度"分梯级，用 progressive disclosure 保持顶层可读。

SKILL.md 超过 100 行？→ 向下推 reference。

### 5. Leading Words

**原则**：利用模型预训练中已有的紧凑概念，替代冗长描述。

SKILL.md 中是否有 3 个以上同义词描述同一件事？→ 压缩为一个 leading word。

### 6. Completion Criterion

**原则**：每个 step 以可检查且穷尽的完成标准结束。

Agent 经常跳过关键步骤？→ completion criterion 不够清晰。

### 7. No-op Test

**原则**：每条指令必须改变 Agent 的默认行为。

删除某行后行为不变？→ 它是 no-op，删除它。

### 8. 调用边界规则

**原则**：User-invoked → Model-invoked → 共享参考，不可逆向。

User-invoked skill 调用另一个 user-invoked？→ 架构违规。

## 8.2 目录结构模板

```
your-agent-framework/
│
├── CLAUDE.md              # 宪法：结构规则、调用规则、维护纪律
├── AGENTS.md              # 跨平台契约
├── CONTEXT.md             # 词典：核心术语、Avoid 指令
├── README.md              # 对外文档
│
├── skills/
│   ├── core/              # [已推广] 稳定的核心技能
│   │   ├── router/SKILL.md
│   │   └── entry-1/SKILL.md
│   ├── shared/            # [已推广] 共享词汇
│   │   └── vocabulary/SKILL.md
│   ├── experimental/      # [草稿]
│   └── deprecated/        # [废弃]
│
├── docs/                  # 对外文档
│
├── .agents/
│   ├── adr/               # 架构决策记录
│   │   ├── 0001-*.md
│   │   └── 0002-*.md
│   └── invocation.md      # 调用模型规则
│
└── .claude-plugin/        # 分发（如果需要）
    ├── plugin.json
    └── marketplace.json
```

## 8.3 你的第一个 Skill

### User-Invoked Skill 示例

```markdown
---
name: your-first-skill
description: A quick sanity check before starting work.
disable-model-invocation: true
---

Run a /grilling session.
```

### Model-Invoked Skill 示例

```markdown
---
name: your-check
description: >-
  Check the current state of affairs.
  Use when the user asks to verify, check, or review something.
---

## Steps
1. **Gather context**
   - Check current file state, git status, recent changes
   **Completion**: All context sources collected

2. **Analyze**
   - Compare state against expected norms
   **Completion**: Deviations identified and documented
```

### 扩展策略

```
阶段 1（第 1 周）
  ├── 1 个 user-invoked entry skill
  └── 1 个 model-invoked skill

阶段 2（第 2-3 周）
  ├── 再增加 1-2 个 user-invoked
  └── 创建 CONTEXT.md（至少 3-5 个术语）

阶段 3（第 4 周以后）
  ├── 达到 5-7 个 user-invoked → 创建 router
  ├── 定期修剪（no-op test）
  └── 记录 ADR（关键决策）
```

## 8.4 质量保障 — 自检清单

### 基础（必须通过）

- [ ] SKILL.md ≤ 100 行
- [ ] Frontmatter 完整：name + description + invocation
- [ ] Description 有触发词（model-invoked）
- [ ] 描述无否定指令
- [ ] 有具体示例

### 结构（建议通过）

- [ ] Completion Criterion 存在（每个 step）
- [ ] 术语一致
- [ ] 引用仅一级深度
- [ ] 无 No-op
- [ ] 无时间敏感信息

### 维护（定期检查）

- [ ] Relevance：每行是否仍然相关？
- [ ] Sediment：是否有过时内容？
- [ ] Sprawl：行数是否在 100 以下？
- [ ] Duplication：是否有内容在其他 SKILL.md 中出现？

## 8.5 常见陷阱与对策

### 陷阱 1：过早引入太多 Skill

**症状**：第一周就建了 15 个 skill，大部分没用过。

**对策**：从 2-3 个开始。每周最多新增 1 个。

### 陷阱 2：不维护 CONTEXT.md

**症状**：语汇漂移——Agent 越来越困惑。

**对策**：建立 CONTEXT.md（至少 3-5 条），严格执行 `_Avoid_` 指令。

### 陷阱 3：不做 Pruning

**症状**：沉积——半年后还有"参考旧版 API"的指令。

**对策**：每季度做一次全面 pruning。删除比重写更常见。

### 陷阱 4：无视上下文窗口

**症状**：会话持续到 15 万 token，Agent 开始"失忆"。

**对策**：设定硬性的上下文管理规则。接近 12 万 token 时主动 handoff。

### 陷阱 5：把 Skill 当 Plugin

**症状**：期望 skill 能做"安装后自动运行的事"。

**对策**：Skill 是指令集，不是插件。如果需要自动行为，了解 Claude Code 的 hooks 机制。

## 8.6 从 Matt 体系到你的体系 — 模式映射表

| Matt 的模式 | 你的项目中对应什么 | 优先级 |
|------------|-------------------|--------|
| Bucket 目录 | core / experimental / deprecated | ★★★ 立即 |
| User/Model-invoked 划分 | 入口 skill vs 内部 skill | ★★★ 立即 |
| CONTEXT.md 词汇表 | 项目核心术语 | ★★★ 立即 |
| Completion Criterion | 步骤完成检查 | ★★☆ 第一周 |
| Leading Words | 核心指令词汇 | ★★☆ 第二周 |
| Router（ask-matt） | 多入口时的导航 | ★★☆ >5 个 skill |
| Grilling 三层抽象 | 意图澄清 + 资料收集 | ★☆☆ 按需 |
| Handoff 机制 | 会话恢复 | ★☆☆ 按需 |
| Pruning（no-op test） | 季度维护 | ★☆☆ 季度 |
| ADR | 重要决策留档 | ★☆☆ 有决策时 |

### 行动路线

**今天就可以做的**：
- 创建你的目录结构（core / experimental / deprecated）
- 写第一份 CONTEXT.md（至少 5 个核心术语）
- 创建一个 user-invoked 入口 skill

**第一周**：
- 为每个 SKILL.md 添加 completion criterion
- 建立 .agents/adr/ 目录
- 写 CLAUDE.md 定义结构规则

**第二周**：
- 引入 leading words 概念
- 创建 model-invoked 共享 reference skill
- 跑一次全面 no-op test

**每月**：
- Pruning 审查——每个 SKILL.md 过一遍
- 检查沉积/蔓延/重复

## 8.7 全书总结

Matt Pocock Skills 仓库的核心价值不在于某个具体的 skill——无论是 12 行的 grilling 还是 ask-matt 的路由逻辑。它的价值在于**示范了一套用工程纪律驯服 Agent 的方法论**。

贯穿全书的核心思想：

1. **小胜于大**：小于 100 行的 skill 更容易维护、更容易审计、更容易替换
2. **语言即架构**：共享的精准术语比冗长的解释更有价值
3. **边界即纪律**：每一道边界都减少了 Agent 的不确定性
4. **修剪胜于添加**：好的 skill 是通过持续删除而非持续增加来塑造的
5. **上下文是货币**：省 token 不是可有可无的优化——它直接决定了 Agent 能在多长时间内保持高质量工作

最后，回到 Matt 那句话：

> "Your skills are the upper limit of what AI can achieve."

你的框架的质量决定了 AI 在你的项目中能发挥的上限。

---

## 附录 A：术语对照表

| 英文 | 中文 | 简要说明 |
|------|------|---------|
| Predictability | 可预测性 | 相同过程，非相同输出 |
| Context Load | 上下文负载 | Model-invoked 的 description 每轮消耗 |
| Cognitive Load | 认知负载 | 用户必须记住 skill 存在的负担 |
| Leading Word | 引导词 | 利用模型先验的紧凑概念 |
| Progressive Disclosure | 渐进式披露 | 沿信息层级向下推细节 |
| Completion Criterion | 完成标准 | 步骤完成的检查条件 |
| Premature Completion | 过早完成 | 步骤未完成就跳转 |
| No-Op | 无效指令 | 不改变行为的指令 |
| Negation | 否定陷阱 | 负面指令反而强化目标行为 |
| Smart Zone | 智能区间 | 模型能稳定推理的上下文大小（~12 万 token） |

## 附录 B：快速参考卡 — 最有价值的 5 个模式

### 1. 调用决策树

```
Agent 需要自主触发？→ Model-invoked（付 context load）
其他 skill 需要调用？→ Model-invoked
否则 → User-invoked（付 cognitive load）
```

### 2. 信息层级梯级

```
1. In-skill step（SKILL.md 中，有序执行）
2. In-skill reference（SKILL.md 中，按需查阅）
3. External reference（独立文件，按需加载）
4. Progressive disclosure = 不必要的东西向下推
```

### 3. 修剪检查清单

```
- [ ] Single source of truth: 每含义一个位置
- [ ] Relevance: 每行还与 skill 相关吗？
- [ ] No-op test: 删掉它会改变行为吗？
- [ ] Negation: 有否定指令吗？
- [ ] Skimmability: 前 5 行能看懂 skill 做什么吗？
```

### 4. Grilling 核心指令

```
- 一次问一个问题，带推荐答案
- 走决策树每个分支，逐个解决依赖
- 事实查环境，决策问用户
- 直到共享理解才行动
```

### 5. Handoff 决策矩阵

```
窗口接近上限？→ /handoff
需要完全不同方向的任务？→ /handoff
阶段间平稳过渡？→ /compact
长时间中断（跨天）？→ /handoff
```
