# 第 5 章：对话边界澄清 — Socratic Sparring 模式

> 素材引用: [R8], [R9], [R10], [E2], [E3]

---

如果说第 4 章是"怎么写好 SKILL.md"，这一章是"什么样的 Skill 最有价值"。在 Matt 的整个体系中，最受赞誉、被引用最多的 Skill 是 **grilling**——一套仅 12 行的盘问原语。

你可能觉得"12 行的 skill 能干什么？"答案出人意料：它能防止大约 80% 的重做灾难。

## 5.1 三层抽象架构

Matt 围绕"盘问"这个行为设计了三个不同的 skill，体现了精妙的分层抽象：

```
用户层 (User-Invoked):
┌──────────────────────────────────────────────────┐
│  grill-me          grill-with-docs                │
│  (3行, 无状态)     (3行, 有状态)                  │
│  委托 ↓            委托 ↓                         │
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

### 三层各自的职责

| Skill | Invocation | 行数 | 状态 | 职责 |
|-------|-----------|------|------|------|
| `grill-me` | User-invoked | 3 行 | 无状态 | 委托给 `grilling` |
| `grill-with-docs` | User-invoked | 3 行 | 有状态 | 委托给 `grilling` + `domain-modeling` |
| `grilling` | Model-invoked | 10 行 | — | 核心盘问原语 |
| `domain-modeling` | Model-invoked | — | — | 生成领域词汇和 ADR |

### 为什么需要三层？

因为**行为相同但状态策略不同**。

- `grill-me`：抛出一个想法，AI 来盘问你，但不留下任何文件。适合"我在等咖啡的时候想验证一个想法"的场景。
- `grill-with-docs`：同样的盘问过程，但每做一个决策就写进 CONTEXT.md 和 ADR。适合"开始一个正式项目之前"的场景。

两者使用同一套盘问逻辑（grilling），唯一区别是盘问结果是否持久化。

> 这个模式的关键启示：**核心逻辑应该与状态管理分离**。grilling 只负责"盘问"这个行为，`grill-with-docs` 才负责"盘问并保存"。如果你的 skill 也有"有状态"和"无状态"两个版本，考虑用同样的分层。

---

## 5.2 Grilling 核心原语详解

grilling 的完整内容只有 10 行指令。以下是逐句拆解：

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

逐句分析每一句的设计意图：

**第 1 句**：`Interview me relentlessly` — `relentlessly` 是 leading word。不是普通的 interview，是不放弃、不遗漏、穷尽每一条分支的 interview。

**第 2 句**：`until we reach a shared understanding` — 这是 completion criterion。"共享理解"是终点标志，在此之前不停止。

**第 3-4 句**：`Walk down each branch... resolving dependencies one-by-one` — 决策树的遍历算法。先解决父决策，再解决子决策。依赖关系决定顺序。

**第 5 句**：`For each question, provide your recommended answer` — 这是最关键的设计决策。Agent 不是抛出一个问题等着，而是给出**自己的推荐答案**，用户只需要确认/修正/拒绝。这极大地减少了"空白问题"带来的决策疲劳。

**第 6-8 句**：`Ask one at a time... Asking multiple is bewildering` — 单次一问是"不想让人困惑"的人性化设计。也防止 Agent 用多个问题来"假装工作"——如果在第一个问题有争议时继续问后续问题，Agent 可能忽略争议继续推进。

**第 9 句**：`Facts → look up, Decisions → ask me` — 这是最精妙的任务边界划分。不浪费用户时间去回答 Agent 能从环境找到的信息，但决策权保留给人类。

**第 11 句**：`Do not act until I confirm shared understanding` — 最终防护。防止 Agent 在还在盘问阶段时就动手写代码。

---

## 5.3 为什么 12 行就够了

一个价值 184K+ stars 仓库的核心 skill 只有 12 行，这本身就是一个值得深挖的现象。

### 原因 1："Grill" 是 Leading Word

`grill` 这个词在模型预训练中承载了大量含义：追问、盘问、不放过、深挖。不需要解释"请追问每个细节，不留死角"——`grill` 一个词就够了。

GLOSSARY.md 对这种现象的分析：

> "A leading word encodes a behavioural principle in the fewest possible tokens by invoking priors the model already holds."

### 原因 2：决策树遍历是已知模式

"Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one"——这不是教模型新知识，而是**激活**模型已经知道的决策树算法。模型在预训练中见过无数决策树的应用场景。

### 原因 3：推荐答案减少模糊性

`For each question, provide your recommended answer` 是一个被低估的设计。如果 Agent 只是提问（"你打算怎么处理用户认证？"），你得从零开始组织答案。但如果 Agent 说（"我建议用 JWT 做用户认证，因为...你觉得呢？"），你只需要确认或修正。

推荐答案把"开放式问题"变成了"选择题"。选择题比填空题省力得多。

### 原因 4：事实/决策的边界划分

"Facts → look up, Decisions → ask me" 这个规则排除了 Agent 最常见的偷懒行为——遇到不确定的事就问用户。被迫去查环境（文件、代码库、文档）意味着 Agent 做了 Legwork，而不是把 Legwork 转嫁给用户。

### 与 Superpowers 的对比

同一件事情，另一个项目 superpowers 用了 689 行实现。12 行 vs 689 行的差距说明了设计哲学的根本差异：

- Skills（12 行）：信任模型能力 + 利用模型先验 + 只设最小护栏
- Superpowers（689 行）：不信任模型 + 控制每步行为 + 完整流程描述

两种方法都能工作。但 12 行版本更容易维护、修改、适应不同场景。689 行版本虽然更精确，但维护成本高，适应性差。

---

## 5.4 有状态 vs 无状态设计

grill-me 和 grill-with-docs 是对"相同行为、不同状态策略"的完美示范。

### grill-me（无状态）

适用场景：
- 你没有项目目录（纯 brainstorming）
- 你不想在文件系统中留下痕迹
- 你在验证一个快速想法

行为：跑完 grilling 就结束，不写任何文件。

### grill-with-docs（有状态）

适用场景：
- 你有一个代码库，准备正式开始工作
- 你需要记录决策供后续引用
- 你想建立项目的共享词汇表

行为：跑完 grilling 后，调用 `domain-modeling` 生成 CONTEXT.md 和 ADR。

### 在你项目中的应用

这个"核心逻辑 + 状态包装"模式有很多应用场景。比如在一个研究笔记项目中：

| 无状态版本 | 有状态版本 |
|---|---|
| 快速收集想法 | 完整研究 + 保存笔记 |
| 临时验证假设 | 正式探索 + 记录探索结果 |
| 快速大纲 | 详细大纲 + 保存到 03_outline.md |

**模式复用**：不是"盘问"才会用到这个分层。任何"有时需要保存、有时不需要"的操作都可以用这个模式。

---

## 5.5 适合你的项目的简化版

### 场景 1：意图片段澄清

你的项目中有 00_intent.md 作为意图文件。如果把 grilling 的概念引入意图片段阶段，可以这样设计：

```markdown
# grill-intent（假设的 skill 名称）
用户的意图不明确时，逐条追问以下分支：
1. 学习目标是什么？
2. 现有基础如何？
3. 期望输出深度？
4. 是否有具体关注点？
每问带推荐答案："我建议从概念入手，因为..."
直到 intent 中的所有字段都已确认。
```

这和当前你的 research-planner 技能做的事情类似——但 grilling 的模式提供了一个更结构化的追问框架。

### 场景 2：验证素材质量

在深层资料收集后（02_deep_research.md 生成后），可以引入一个盘问步骤：

```markdown
# 素材质量检查
- 关键信源是否都覆盖了？
- 社区讨论和官方文档是否都有？
- 是否遗漏了重要的反方观点？
- 素材是否有时效性问题？
每问带推荐答案
直到用户确认素材质量
```

---

## 本章要点

1. **三层抽象**：grill-me（无状态封装）→ grilling（核心原语）→ grill-with-docs（有状态封装），行为相同，状态策略不同
2. **核心原语**：一次一问 + 推荐答案 + 决策树遍历 + 事实/决策分离 + 共享理解为终点
3. **12 行的力量**：leading word + 先验知识 + 推荐答案 + 边界划分 ≈ 0 冗余
4. **有/无状态分离**：核心逻辑与状态管理解耦，同一行为可以在两种模式下复用
5. **可迁移到你项目**：意图片段澄清、素材质量验证、大纲评审——任何需要"确认共识"的步骤都可以采用这个模式

> **对你自建框架的启示**：你的项目中"需要对齐意图"的场景——学习目标定义、资料收集方向确认、大纲确认——都是 grilling 模式的天然应用场景。把这些步骤从"扔给用户自己决定"升级为"结构化的共识对齐"，是提升 Agent 框架质量的最快路径。

> **下一章**：上下文管理——当会话窗口不够用时，Handoff 和 Context Compaction 策略。
