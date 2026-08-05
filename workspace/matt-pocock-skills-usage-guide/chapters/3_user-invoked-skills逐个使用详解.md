# 第三章 user-invoked skills 逐个使用详解

第 2 章给了全局地图，这一章把 [[Matt Pocock Skills]] 里 10 个 user-invoked skill 逐个讲透（其中 `/setup-matt-pocock-skills` 已在第 1 章 1.4 讲完，本章覆盖其余 9 个）。它们全部用斜杠命令触发，按职责分四组：盘问类把模糊想法打磨清楚，规划类把想法变成 spec 与 tickets，执行类真正动手写代码，治理辅助类负责分类、教学与参考。每个 skill 都按「是什么 → 怎么触发 → 典型步骤 → 什么时候用它」展开，命令可直接复制 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

## 3.1 盘问类：/grill-with-docs 与 /grill-me

### 3.1.1 /grill-with-docs 有状态盘问

`/grill-with-docs` 是**有状态**的盘问：它不只拷问你的方案，还会把拷问产出的术语与决策写成文件，沉淀成项目资产。

**怎么触发**

```text
/grill-with-docs
```

**内部流程**

它内部委托两个 model-invoked skill（第 4 章细讲）：

- `/grilling`：核心盘问原语，一次一问、带推荐答案，逐层逼近你没想清楚的地方。
- `/domain-modeling`：敲定术语，把模糊说法精炼成统一词汇。

**副产品（这是它和 grill-me 的本质区别）**

| 文件 | 内容 | 维护者 |
|------|------|--------|
| [[CONTEXT.md]] | 项目术语词汇表 | `/grill-with-docs`、`/domain-modeling` 更新 |
| [[ADR]]（`.agents/adr/`） | 架构决策记录 | 有决策时写入 |

**什么时候用它**：开始新功能或模块之前、想法还模糊时。它强迫你先把「为什么这样做」想清楚，并留下团队可读的决策痕迹，是第 6 章主流程的起点。

> [!tip] 先争论后落笔
> 一次认真的有状态盘问之后，CONTEXT.md 里会多出几条术语、ADR 里多一条决策——这些是后面 `/to-spec` 可以直接引用的素材，不是白聊。

### 3.1.2 /grill-me 无状态盘问

`/grill-me` 是 `/grilling` 的 **3 行薄封装**：委托同一个盘问原语，但跑完即止、不留任何痕迹。

```text
/grill-me
```

它不写 CONTEXT.md，不产 ADR，盘问结束对话就回到原状。

| 维度 | /grill-with-docs | /grill-me |
|------|------------------|-----------|
| 状态 | 有状态，留文档 | 无状态，跑完即止 |
| 内部委托 | `/grilling` + `/domain-modeling` | 仅 `/grilling` |
| 产出 | CONTEXT.md + ADR | 无 |
| 适用 | 关键决策、需要沉淀 | 快速验证想法、不想要噪音 |

**什么时候用它**：只想快速被盘问一遍、确认没漏掉明显问题，又不想在仓库里留下文档。取舍很简单——**要沉淀用 grill-with-docs，只要一次盘问用 grill-me**。

> [!warning] 盘问类可能话痨
> 社区实测显示盘问类 skill 可能对简单问题追问 10-100 个问题（Issue #274）[社区实测](https://dev.to/evan-dong/i-tried-the-claude-code-skills-repo-that-got-77k-stars-here-is-what-works-and-what-does-not-57a4)。时间不够就直接说「我时间不够，跳过高频问题」，或改用 grill-me 控制篇幅。

## 3.2 规划类：/to-spec 与 /to-tickets

### 3.2.1 /to-spec 合成 spec

`/to-spec` 把盘问后的对话**合成一份结构化 PRD spec**，发布到你的 issue tracker。它是「从想法到可执行方案」的桥梁。

**怎么触发**

```text
/to-spec
```

**执行流程**

1. **Explore repo**：先摸清仓库现状，避免写出和现实脱节的 spec。
2. **Sketch seams**：画出改动涉及的边界（模块、接口、适配点）。
3. **Write spec**：按固定模板写正文。
4. **Publish**：发布到 issue tracker，并打上 `ready-for-agent` 标签。

spec 模板固定六段：

```markdown
# Problem
# Solution
# User Stories
# Implementation
# Testing
# Out of Scope
```

> [!note] `ready-for-agent` 标签的意义
> 这个标签是给 `/implement` 的「绿灯信号」：被打上 `ready-for-agent` 的 issue 意味着方案已定、可以直接交给 agent 实现。它是规划阶段和执行阶段的握手协议。

**什么时候用它**：grill 之后、动手之前。想法已经清晰，需要一份不因人而异、可直接执行的 spec。

### 3.2.2 /to-tickets 拆 tickets

`/to-tickets` 把 spec 进一步**拆成纵向切片（vertical slices）**，每个切片是一个可直接交给 `/implement` 的 ticket。

**怎么触发**

```text
/to-tickets
```

**执行流程**

1. **Gather context**：收集 spec 与相关上下文。
2. **Explore codebase**：确认代码库结构，让切片贴合实际。
3. **Draft vertical slices**：按 tracer bullet 思路拆。
4. **Quiz the user**：把切片方案抛给你确认，而不是闷头发布。
5. **Publish**：确认后发布到 issue tracker。

**两个关键机制**

- **纵向切片（tracer bullet）**：每个 ticket 是「从界面到数据」的一条纵贯线，而非按层横切（先做所有 UI、再做所有逻辑那种）。做完一个就有可演示的端到端结果。
- **声明阻塞边**：ticket 之间有先后依赖时明确标出「被谁阻塞」，避免并行实现踩踏。
- **Quiz 确认**：发布前必须经你点头，防止拆出来的粒度不符合你的预期。

> [!tip] 拆完逐个执行
> 拆出的每个 ticket 对应一次独立的 `/implement`，且每次从新会话开始（见 3.3.1）。切片越端到端，串起来越顺。

**什么时候用它**：spec 已就绪、需要把大任务拆成可独立交付的小块时。

## 3.3 执行类：/implement 与 /ask-matt

### 3.3.1 /implement 实现

`/implement` 是**执行器**：基于已就绪的 spec / ticket 写代码，内部自动驱动完整质量流程。

```text
/implement
```

**内部驱动链**：`/tdd`（红-绿-重构，先写测试）→ 完成后 `/code-review`（双路审查）→ commit。

**定位：手不是头**。`/implement` 假设思考已经在 grilling + to-spec 阶段完成——你调用它时方案已经定了，它只负责把手头的方案变成代码。如果实现过程中需要大改方案，说明前置的盘问/规划没做完，应退回上一步，而不是在 implement 里补思考。

> [!warning] 从新会话开始
> 上下文卫生原则（第 6 章详述）要求：**每个 `/implement` 从新会话开始**。同一会话跑完 to-spec / to-tickets 后，开新会话再敲 `/implement`，避免上下文过长污染实现质量。

**什么时候用它**：`ready-for-agent` 的 spec / ticket 已就绪时，一次只处理一个切片。

### 3.3.2 /ask-matt 中央路由器

`/ask-matt` 是**中央路由器**：你不需要记住 22 个 skill 各自该什么时候用，只记这一个命令。

```text
/ask-matt
```

它根据当前情境（你在做什么、做到哪一步）推荐最合适的 skill 或 flow。刚开新仓库，它指向 `/setup-matt-pocock-skills`；想法还模糊，它建议 `/grill-with-docs`；spec 写好了，它指向 `/to-tickets`。

**什么时候用它**：刚上手、或不确定下一步该敲哪个命令时。它是零成本入口——敲错也不会执行任何东西，只是拿建议。

> [!tip] 记忆负担最小化
> 全框架最低记忆成本就是 `/ask-matt`。不确定就敲它让模型帮你路由，而不是背 10 个斜杠命令。

## 3.4 治理与辅助类：/triage、/teach、/writing-great-skills

### 3.4.1 /triage issue 分类

`/triage` 是 **issue / PR 分类状态机**，把 issue tracker 里的一堆积压变成可执行的优先清单。

```text
/triage
```

**执行流程**

1. **Show attention buckets**：先展示分类桶，告诉你哪些 issue 需要关注。
2. **Triage specific item**：对单个 issue 走五个动作之一：
   - **Gather**：补齐信息；
   - **Recommend**：给出处理建议；
   - **Verify**：核实是否已解决；
   - **Grill**：盘问这个 issue 值不值得做；
   - **Apply**：直接套用某个 skill 处理。
3. **Quick override**：对个别 issue 手动覆盖分类结果。
4. **Resume**：回到流程继续处理下一个。

**什么时候用它**：issue 堆积、需要知道「先做哪个、哪些该关掉」时。它依赖第 1 章初始化时配置的 issue tracker。

### 3.4.2 /teach 持续教师

`/teach` 是在 **workspace 内持续教学**的教师角色，维护一份学习状态，随对话推进持续讲解你正在接触的代码库与概念。

```text
/teach
```

它不像一次性提问，而是「持续」——你在 workspace 里工作得越久，它越了解你的进度，讲解越贴合上下文。

**什么时候用它**：正在一个不熟悉的代码库里工作，希望每动一处都有人解释「这是在干什么、为什么这么写」。适合学习期，不属于生产主流程。

### 3.4.3 /writing-great-skills 写作参考

`/writing-great-skills` 是**纯参考** skill：不执行任何流程，只在你写自定义 skill 时提供写作原则。

```text
/writing-great-skills
```

它引出六个质量关卡（第 5 章 5.3 配置自定义 skill 时展开，这里先记住检查清单）：

| 关卡 | 要求 |
|------|------|
| description 触发词 | description 面向模型，含 "Use when..." 触发短语 |
| 篇幅 | SKILL.md 不超过 100 行 |
| 无时间敏感 | 不写会过期的信息 |
| 术语一致 | 与项目已有词汇保持一致 |
| 含具体示例 | 有可参考的实例 |
| 引用仅一级深度 | 依赖用 `/skill` 散文式引用，不做深度交叉引用 |

**什么时候用它**：写自己的第一个 skill 之前（第 5 章 5.3、第 8 章 8.2 都会回来用这份清单自查）。

## 本章小结

- 盘问类：`/grill-with-docs` 有状态、产 [[CONTEXT.md]] 与 [[ADR]]，适合关键决策；`/grill-me` 无状态、跑完即止，适合快速验证。
- 规划类：`/to-spec` 合成六段式 spec 并打 `ready-for-agent` 标签；`/to-tickets` 拆纵向切片 tickets，发布前用 quiz 跟你确认。
- 执行类：`/implement` 是「手不是头」，内部驱动 tdd → code-review → commit，且从新会话开始；`/ask-matt` 是中央路由器，只记一个命令。
- 治理辅助类：`/triage` 分类 issue（Gather / Recommend / Verify / Grill / Apply），`/teach` 在 workspace 内持续教学，`/writing-great-skills` 提供写 skill 的六项质量关卡。
- 10 个 user-invoked 中，`/setup-matt-pocock-skills` 已在第 1 章 1.4 讲完；其余 9 个全部用斜杠命令触发，相互之间不调用，由你在流程中按顺序手动串联。

下一章：model-invoked 的 12 个 skill——它们不被你直接敲，而是被对话情境或上级 skill 自动带出来，其中 `/grilling`、`/tdd`、`/code-review` 正是上一章所有 user-invoked 委托的内部引擎。
