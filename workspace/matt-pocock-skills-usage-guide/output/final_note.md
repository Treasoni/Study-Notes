# 使用 Matt Pocock Skills — 实操使用指南

这是一份 Matt Pocock Skills 的实操使用指南，与深度解析笔记《Matt Pocock Skills — Agent 框架设计深度解析》互补：那篇讲「为什么」，这篇讲「怎么做」。全文按「安装初始化 → 清单总览 → 逐个上手 → 配置定制 → 实战演练 → 排错 → 落地到自己的项目 → 附录速查」组织，所有命令均可直接复制，目标是让你把这套 22 个 skill 的框架真正用起来。

## 目录

- [第一章 快速上手 — 安装与初始化](#第一章-快速上手--安装与初始化)
- [第二章 完整 skill 清单与触发方式总览](#第二章-完整-skill-清单与触发方式总览)
- [第三章 user-invoked skills 逐个使用详解](#第三章-user-invoked-skills-逐个使用详解)
- [第四章 model-invoked skills 逐个使用详解](#第四章-model-invoked-skills-逐个使用详解)
- [第五章 配置与定制](#第五章-配置与定制)
- [第六章 工作流实战演练](#第六章-工作流实战演练)
- [第七章 常见问题与排错](#第七章-常见问题与排错)
- [第八章 把 skills 应用到自己的项目](#第八章-把-skills-应用到自己的项目)
- [附录：命令速查卡](#附录-命令速查卡)

---

## 第一章 快速上手 — 安装与初始化

你已经从深度解析笔记里理解了 [[Matt Pocock Skills]] 的设计原理，这一步要把 22 个 skill 真正装进你的环境。本章解决三个实际问题：两条安装路线（npx skills 与 Claude Code Plugin）如何二选一、各自怎么一步步操作，以及每个新仓库第一次使用前必须做的初始化。全程只讲"怎么做"，命令可直接复制。

### 1.1 两条互斥安装路线怎么选

Matt Pocock Skills 提供两种互斥的安装方式，先想清楚再动手，因为两者会互相干扰。

| 维度 | npx skills 安装器 | Claude Code Plugin |
|------|------------------|--------------------|
| 入口命令 | `npx skills@latest add mattpocock/skills` | `/plugin marketplace add` + `/plugin install` |
| 文件形态 | 可编辑的普通文件，写入仓库 `.claude/` | 只读，由 marketplace 自动更新 |
| 触发方式 | `/skill-name` | `/插件名:skill名` |
| 更新方式 | `npx skills update` | 改仓库后 `/plugin marketplace update` |
| 版本控制 | 只下载最新版，无法回退 | 版本由 marketplace 控制 |

两者最关键的区别在**文件形态**和**触发方式**：

- **npx 路线把 skill 作为普通文件拷进仓库 `.claude/`**，你可以直接编辑、定制甚至 fork。触发时用斜杠命令，比如 `/grill-with-docs`。
- **Plugin 路线是只读的**，skill 以插件名做命名空间，触发时带前缀，比如 `/mattpocock-skills:grill-with-docs`。更新由 marketplace 统一管理，适合团队保持版本一致。

> [!warning] 二选一，不要混用
> 两条机制会重复安装同一批 skill。npx 是"可编辑副本"，Plugin 是"只读自动更新"。混用时同一命令可能出现两个版本，你无法确定哪个生效，排错成本极高。

怎么选：个人项目、想改 skill 行为 → npx；团队 3 人以上、要求版本一致且自动更新 → Plugin。选定后不要中途混装。

### 1.2 npx skills 安装器逐步操作

npx 路线适合个人，四步装完。

**1. 安装**

```bash
npx skills@latest add mattpocock/skills
```

> [!tip] `@latest` 的含义
> `npx skills@latest` 确保你用的是 skills CLI 的最新版本本身，而不是本地缓存的旧版 CLI。

**2. 勾选需要的 skill**

CLI 会列出可安装的 skill 清单（Engineering + Productivity 共 22 个），交互式勾选。首次建议至少勾选 `/setup-matt-pocock-skills`，它是后续初始化的入口。

**3. 确认写入仓库**

选中后 skill 以普通文件写入仓库 `.claude/`，之后用斜杠命令触发：

```text
/setup-matt-pocock-skills
/grill-with-docs
/to-tickets
```

**4. 后续更新**

```bash
npx skills update
```

> [!warning] 无法回退旧版
> CLI 只下载最新版。若想固定在某个旧版本，需要先手动定位旧版文件再复制进仓库自建，没有一键回退。

### 1.3 Claude Code Plugin 安装逐步操作

Plugin 路线适合团队，打开 Claude Code 后按顺序执行。

**1. 添加官方插件市场**

官方市场通常已自动添加；若没有：

```text
/plugin marketplace add anthropics/claude-plugins-official
```

**2. 安装插件**

```text
/plugin install mattpocock-skills@anthropics
```

也可以直接输入 `/plugin install` 进入交互式选择。

**3. 选择作用域**

安装时 Claude Code 会询问作用域，三选一：

| 作用域 | 生效范围 | 写入位置 |
|--------|---------|---------|
| User | 你的所有项目 | 全局用户配置 |
| Project | 本仓库所有协作者 | `.claude/settings.json` |
| Local | 仅本仓库本人 | 本地覆盖 |

> [!note] 团队私有市场
> 团队私有插件仓库通过 `extraKnownMarketplaces` 写入 `.claude/settings.json` 分发：

```json
{
  "extraKnownMarketplaces": [
    {
      "name": "my-team",
      "owner": "my-org",
      "repo": "my-private-plugins",
      "type": "git"
    }
  ]
}
```

添加后同样用 `/plugin install <名>@my-team` 安装。

**4. 重新加载生效**

```text
/reload-plugins
```

之后触发 skill 要带命名空间：

```text
/mattpocock-skills:grill-with-docs
```

### 1.4 新仓库初始化：/setup-matt-pocock-skills

装完后，**每个新仓库第一次使用前**运行一次初始化。它让 skills 了解你的仓库上下文（issue tracker、标签、文档布局），是 to-tickets / triage / to-spec 的硬依赖。

```text
/setup-matt-pocock-skills
```

skill 会走 Explore → Present → Confirm → Write 流程：

1. **Explore**：探索仓库——用哪个 issue tracker（GitHub / Linear / 本地）、用了什么标签、文档怎么布局。
2. **Present**：把发现和建议分段展示给你。
3. **Confirm**：逐段确认，修改不符合实际的地方。
4. **Write**：把 `## Agent skills` 块写入 CLAUDE.md（以及 AGENTS.md，供 Codex 等跨平台使用），并生成 `docs/agents/` 辅助文档。

写入 CLAUDE.md 的 `## Agent skills` 块大致长这样：

```markdown
## Agent skills

- `/grill-with-docs` — 有状态盘问，产出 ADR 与词汇表
- `/to-spec` — 把对话合成 spec，发布到 issue tracker
- `/to-tickets` — 把 spec 拆成纵向切片 tickets
- `/implement` — 基于 spec/tickets 实现，内部驱动 tdd → code-review
```

> [!tip] 配置 issue tracker 是硬依赖
> `/to-spec` 发布 spec、`/to-tickets` 发布 tickets、`/triage` 分类 issue 都依赖第 1 步确认的 issue tracker 与标签。跳过会导致这些 skill 找不到发布目标，跑完即废。

初始化完成后，检查 CLAUDE.md 是否出现 `## Agent skills` 块，并确认 issue tracker 配置正确，就可以进入第 2 章的全景总览了。

### 本章小结

- 两条安装路线互斥：npx skills 是可编辑副本 + `/skill-name`，Plugin 是只读自动更新 + `/插件名:skill名`，不要混用。
- npx 路线四步：`npx skills@latest add mattpocock/skills` → 勾选 → 写入 `.claude/` → `npx skills update` 更新；无法回退旧版。
- Plugin 路线：加市场 → `/plugin install` → 选作用域（User / Project / Local）→ `/reload-plugins`；团队私有市场用 `extraKnownMarketplaces`。
- 每个新仓库运行一次 `/setup-matt-pocock-skills`，产出 CLAUDE.md / AGENTS.md 的 `## Agent skills` 块 + `docs/agents/`。
- issue tracker 与标签是 to-spec / to-tickets / triage 的硬依赖，初始化时务必确认。

---

## 第二章 完整 skill 清单与触发方式总览

第 1 章装好了环境，但要开始使用之前，你需要一张全局地图：这 22 个 [[Agent Skills]] 各自做什么、由谁来触发。本章把完整清单、user-invoked / model-invoked 分组、以及调用边界一次性讲清。读完你会知道哪些命令可以自己敲，哪些要让模型在对话中自动接手。

### 2.1 22 个 skill 全景总表

[[Matt Pocock Skills]] 在 plugin.json v1.2.0 中共收录 22 个 skill，分成 **Engineering（17 个）** 与 **Productivity（5 个）** 两类。下表以 plugin.json v1.2.0 为基准，触发类型以各 SKILL.md frontmatter 实测为准（个别与 plugin.json 表格标记不一致处以后者为准）[github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

**Engineering（17 个）**

| Skill | 触发类型 | 一句话作用 |
|-------|---------|-----------|
| ask-matt | user | 中央路由器，推荐当前情境最合适的 skill / flow |
| grill-with-docs | user | 有状态盘问，副产品产出 ADR + [[CONTEXT.md]] 词汇表 |
| triage | user | issue / PR 分类状态机，产出 agent-ready brief |
| to-spec | user | 把对话合成 PRD spec，发布到 issue tracker |
| to-tickets | user | 把 plan / spec 拆成纵向切片 tickets |
| implement | user | 基于 spec / tickets 实现，内部驱动 tdd → code-review → commit |
| setup-matt-pocock-skills | user | 初始化仓库配置（每个新仓库一次） |
| diagnosing-bugs | model | 建反馈回路诊断 bug |
| tdd | model | 红-绿-重构，一次一个纵向切片 |
| code-review | model | 双路并行子代理审查 diff |
| domain-modeling | model | 敲定术语，写 CONTEXT.md 词汇表 + [[ADR]] |
| prototype | model | 一次性原型回答单一设计问题（LOGIC / UI 分支） |
| improve-codebase-architecture | model | 霰弹式给出架构改进方案 |
| wayfinder | model | 拆 Decision ticket（决策而非构建） |
| research | model | 处理研究类工作 |
| codebase-design | model | 深模块词汇表（共享参考） |
| resolving-merge-conflicts | model | 解决合并冲突 |

**Productivity（5 个）**

| Skill | 触发类型 | 一句话作用 |
|-------|---------|-----------|
| grill-me | user | 无状态盘问，委托 grilling，跑完即止 |
| teach | user | workspace 内持续教师，维护学习状态 |
| writing-great-skills | user | skill 写作原则参考（纯参考） |
| grilling | model | 核心盘问原语（触发词 "grill me"） |
| handoff | model | 压缩会话为交接文档，保存到系统临时目录 |

> [!tip] 表中没有 /compact
> 全仓库扫描确认 `compact` 已从仓库删除。同会话继续用 Claude Code 内置 compact；跨会话交接用 `/handoff`（详见第 4 章 4.4）。

### 2.2 user-invoked vs model-invoked 分组

22 个 skill 按"谁触发"分成两组，这是整个框架最核心的分类。

**user-invoked（10 个，人类显式调用）**

```text
/ask-matt, /grill-with-docs, /grill-me, /to-spec, /to-tickets,
/implement, /triage, /setup-matt-pocock-skills, /teach, /writing-great-skills
```

这组的触发方式是**斜杠命令**：你在输入框敲 `/skill-name`，模型才会运行它。它们的 SKILL.md 前端设置了 `disable-model-invocation: true`，模型不会自作主张调用。

**model-invoked（12 个，模型自动调用）**

```text
/grilling, /tdd, /code-review, /domain-modeling, /prototype, /diagnosing-bugs,
/improve-codebase-architecture, /wayfinder, /research, /codebase-design,
/resolving-merge-conflicts, /handoff
```

这组的触发方式是 **description 触发词**：SKILL.md 的 description 面向模型，包含 "Use when..." 触发短语。模型在对话中判断"现在该 grilling 了"，就自动套用该 skill 的流程。例如你或上级 skill 说了 "grill me"，模型就会触发 `/grilling`；谈到 "test-first"、"red-green-refactor" 会触发 `/tdd`。

| 维度 | user-invoked | model-invoked |
|------|--------------|---------------|
| 谁触发 | 人类 | 模型 |
| 触发机制 | 斜杠命令 `/skill-name` | description 触发词（"Use when..."） |
| 入口 | 用户显式输入 | 对话上下文或上级 skill 委托 |
| 数量 | 10 个 | 12 个 |
| 前端开关 | `disable-model-invocation: true` | 默认允许隐式调用 |

> [!note] 一句记法
> 斜杠命令是"人按开关"，触发词是"模型看上下文自动接力"。绝大多数情况下你不会直接敲一个 model-invoked skill——它是被上层流程带出来的。

### 2.3 调用边界与依赖规则

skill 之间不是任意互相调用的，依赖是**单向的**，违反会破坏整个流程设计。

**单向依赖链：user-invoked → model-invoked → 共享参考，不可逆向**

- user-invoked skill 可以委托 model-invoked skill。例如 `/grill-with-docs` 内部委托 `/grilling` + `/domain-modeling`；`/implement` 内部驱动 `/tdd` → `/code-review`；`/grill-me` 是 3 行薄封装，直接委托 `/grilling`。
- model-invoked skill 可以引用共享参考类 skill。例如 `/domain-modeling` 会交叉引用 `/codebase-design` 的深模块词汇表。
- **不可逆向**：model-invoked 不会反向委托 user-invoked skill；共享参考也不会被当作入口直接调用。

**user-invoked 不能调用另一个 user-invoked**

两个斜杠命令之间没有互相委托。`/to-spec` 不会内部调用 `/to-tickets`，`/to-tickets` 也不会调用 `/implement`——它们由你在流程中按顺序手动触发（第 6 章的主流程就是靠人把这些命令串起来）。

**依赖用 /skill 散文式引用表达**

skill 之间的依赖不是深度交叉引用（不会把一个 skill 的完整内容嵌进另一个），而是在 SKILL.md 里用一句"委托 `/grilling`"这样的散文式引用表达。这样每个 skill 保持独立可读，也符合 ≤100 行的体积约束。

> [!warning] 常见违规
> 让一个 user-invoked skill 去"自动继续"另一个 user-invoked skill，或者期望 model-invoked skill 反过来弹出斜杠命令，都属于调用边界违规。遇到这种情况，说明流程断点应该由你手动接管。

### 本章小结

- plugin.json v1.2.0 共 22 个 skill：Engineering 17 个 + Productivity 5 个；触发类型以 SKILL.md frontmatter 实测为准。
- user-invoked（10 个）用斜杠命令由人显式触发；model-invoked（12 个）靠 description 触发词由模型按上下文自动调用。
- 依赖是单向的：user-invoked → model-invoked → 共享参考，不可逆向。
- user-invoked 之间不互相调用；流程推进靠你在会话里按顺序手动触发。
- skill 依赖用 `/skill` 散文式引用表达，不做深度交叉引用，保持每个 skill 独立可读。

---

## 第三章 user-invoked skills 逐个使用详解

第 2 章给了全局地图，这一章把 [[Matt Pocock Skills]] 里 10 个 user-invoked skill 逐个讲透（其中 `/setup-matt-pocock-skills` 已在第 1 章 1.4 讲完，本章覆盖其余 9 个）。它们全部用斜杠命令触发，按职责分四组：盘问类把模糊想法打磨清楚，规划类把想法变成 spec 与 tickets，执行类真正动手写代码，治理辅助类负责分类、教学与参考。每个 skill 都按「是什么 → 怎么触发 → 典型步骤 → 什么时候用它」展开，命令可直接复制 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

### 3.1 盘问类：/grill-with-docs 与 /grill-me

#### 3.1.1 /grill-with-docs 有状态盘问

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

#### 3.1.2 /grill-me 无状态盘问

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

### 3.2 规划类：/to-spec 与 /to-tickets

#### 3.2.1 /to-spec 合成 spec

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

#### 3.2.2 /to-tickets 拆 tickets

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

### 3.3 执行类：/implement 与 /ask-matt

#### 3.3.1 /implement 实现

`/implement` 是**执行器**：基于已就绪的 spec / ticket 写代码，内部自动驱动完整质量流程。

```text
/implement
```

**内部驱动链**：`/tdd`（红-绿-重构，先写测试）→ 完成后 `/code-review`（双路审查）→ commit。

**定位：手不是头**。`/implement` 假设思考已经在 grilling + to-spec 阶段完成——你调用它时方案已经定了，它只负责把手头的方案变成代码。如果实现过程中需要大改方案，说明前置的盘问/规划没做完，应退回上一步，而不是在 implement 里补思考。

> [!warning] 从新会话开始
> 上下文卫生原则（第 6 章详述）要求：**每个 `/implement` 从新会话开始**。同一会话跑完 to-spec / to-tickets 后，开新会话再敲 `/implement`，避免上下文过长污染实现质量。

**什么时候用它**：`ready-for-agent` 的 spec / ticket 已就绪时，一次只处理一个切片。

#### 3.3.2 /ask-matt 中央路由器

`/ask-matt` 是**中央路由器**：你不需要记住 22 个 skill 各自该什么时候用，只记这一个命令。

```text
/ask-matt
```

它根据当前情境（你在做什么、做到哪一步）推荐最合适的 skill 或 flow。刚开新仓库，它指向 `/setup-matt-pocock-skills`；想法还模糊，它建议 `/grill-with-docs`；spec 写好了，它指向 `/to-tickets`。

**什么时候用它**：刚上手、或不确定下一步该敲哪个命令时。它是零成本入口——敲错也不会执行任何东西，只是拿建议。

> [!tip] 记忆负担最小化
> 全框架最低记忆成本就是 `/ask-matt`。不确定就敲它让模型帮你路由，而不是背 10 个斜杠命令。

### 3.4 治理与辅助类：/triage、/teach、/writing-great-skills

#### 3.4.1 /triage issue 分类

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

#### 3.4.2 /teach 持续教师

`/teach` 是在 **workspace 内持续教学**的教师角色，维护一份学习状态，随对话推进持续讲解你正在接触的代码库与概念。

```text
/teach
```

它不像一次性提问，而是「持续」——你在 workspace 里工作得越久，它越了解你的进度，讲解越贴合上下文。

**什么时候用它**：正在一个不熟悉的代码库里工作，希望每动一处都有人解释「这是在干什么、为什么这么写」。适合学习期，不属于生产主流程。

#### 3.4.3 /writing-great-skills 写作参考

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

### 本章小结

- 盘问类：`/grill-with-docs` 有状态、产 [[CONTEXT.md]] 与 [[ADR]]，适合关键决策；`/grill-me` 无状态、跑完即止，适合快速验证。
- 规划类：`/to-spec` 合成六段式 spec 并打 `ready-for-agent` 标签；`/to-tickets` 拆纵向切片 tickets，发布前用 quiz 跟你确认。
- 执行类：`/implement` 是「手不是头」，内部驱动 tdd → code-review → commit，且从新会话开始；`/ask-matt` 是中央路由器，只记一个命令。
- 治理辅助类：`/triage` 分类 issue（Gather / Recommend / Verify / Grill / Apply），`/teach` 在 workspace 内持续教学，`/writing-great-skills` 提供写 skill 的六项质量关卡。
- 10 个 user-invoked 中，`/setup-matt-pocock-skills` 已在第 1 章 1.4 讲完；其余 9 个全部用斜杠命令触发，相互之间不调用，由你在流程中按顺序手动串联。

---

## 第四章 model-invoked skills 逐个使用详解

第 3 章那 10 个 user-invoked skill 是你亲手敲斜杠命令触发的；这一章的 12 个 model-invoked skill 恰好相反——**你几乎不会直接敲它们**。它们由对话情境或上级 skill 自动带出：你在对话里说 "grill me"，模型就套用 [[Grilling]]；`/implement` 内部自动驱动 `/tdd` 与 `/code-review`。本章逐个讲清它们是什么、被什么触发、内部走什么步骤，以及什么时候它们会悄悄出现。素材来自 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

### 4.1 核心工程原语：/grilling、/tdd、/code-review、/diagnosing-bugs

这组是框架的"引擎"。第 3 章所有 user-invoked skill 内部驱动的就是它们，理解这组等于理解了整个框架的质量机制。

#### 4.1.1 /grilling 盘问原语

一句话：`/grilling` 是框架的核心盘问引擎，一次一个问题地拷问你的方案。

**怎么被触发**：不通过斜杠命令触发，只有两种方式——你在对话里说了触发词 "grill me"（比如「grill me，看看这个方案有什么漏洞」）；或上级 skill 委托它（第 3 章的 `/grill-with-docs` 与 `/grill-me` 内部都是调它）。

**典型步骤**：

1. **一次一问，带推荐答案**：先给出它的推荐答案，再问你「这样对吗」，让你在低认知负担下逐点确认，而不是被十个问题砸脸。
2. **走决策树分支**：根据你的回答沿决策树继续深入，直到覆盖你没想清楚的分支。
3. **事实查环境、决策问用户**：涉及仓库事实（「这个接口存在吗」）它自己去查代码，不烦你；涉及取舍（「用 A 还是 B」）才把问题抛给你。
4. **达成共识才行动**：每个分支确认一致后才进下一个，不带着分歧往前。

**什么时候它会出现**：当你主动要求被盘问，或调用 grill-with-docs / grill-me 时——你敲的是斜杠命令，真正干活的却是这个你从未直接敲过的 model-invoked skill。

> [!note] 为什么你不能直接敲它
> 它的 frontmatter 面向模型而非人类：description 里写的是触发短语 "grill me"，不是一行给人看的摘要。触发机制是"看上下文"而非"读命令"，所以它永远被情境带出，而不是被你点名。

#### 4.1.2 /tdd 测试驱动

一句话：`/tdd` 把「红-绿-重构」纪律注入实现过程，是 `/implement` 的内部第一棒。

**怎么被触发**：对话出现 "test-first"、"red-green-refactor" 触发词时；更常见的是 `/implement`（第 3 章）内部驱动它。

**典型步骤**：

```bash
# 红：先写一个会失败的测试，定义期望行为（先看它失败）
# 绿：写最小实现让测试通过
# 重构：通过后清理代码，测试保持在绿
```

1. **Red before green**：先写测试、先看它失败。测试是实现之前的行为契约，不是实现之后补的验证。
2. **一次一个切片**：一次只处理一个纵向切片（tracer bullet），做完再进下一个，不一次性写一大块。
3. **重构不进循环**：重构是独立的绿后环节；不要在红绿循环里边写边改结构，把"写对"和"改好"分开。

> [!warning] 期望值要来自独立真值源
> `/tdd` 特别强调：测试断言里的期望值必须来自 spec、需求或业务规则这类独立真值源，而不是把实现代码的逻辑原样抄进断言。否则测试永远和实现"互相印证"，行为改坏了也测不出来——这就是循环论证。

**什么时候它会出现**：每个 `/implement` 的开场。你敲 `/implement` 时它自动接管测试环节，你甚至不需要知道它的名字。

#### 4.1.3 /code-review 双路审查

一句话：`/code-review` 同时派出两个子代理，一路对照编码标准、一路对照 spec，双路并行审查 diff。

**怎么被触发**：`/implement` 实现完成后自动触发；或你在对话里让它审查某个 diff。

**典型步骤**：

```text
Pin fixed point → Identify spec source → Identify standards sources
→ Spawn both sub-agents → Aggregate
```

1. **Pin fixed point**：先钉死审查基准（当前 commit / diff 范围），避免子代理看错版本。
2. **Identify spec source**：找到这次改动对应的 spec / PRD（`ready-for-agent` 的 issue 在这里被引用）。
3. **Identify standards sources**：找到项目的编码规范 / 最佳实践来源。
4. **Spawn both sub-agents**：派两个子代理并行——一个对照编码标准，一个对照 spec / PRD。
5. **Aggregate**：汇总两份报告。

输出是并排报告：

```text
## Standards
- 违反了哪条编码规范 …

## Spec
- 与 spec 的哪条描述不符 …
```

**什么时候它会出现**：每个 `/implement` 的收尾，与第 3 章 `/implement` 的驱动链直接衔接——`/implement` 内部 `/tdd` 写完 → `/code-review` 审完 → commit。

#### 4.1.4 /diagnosing-bugs

一句话：`/diagnosing-bugs` 诊断 bug，核心信条是——**90% 的工作在建反馈回路**。

**怎么被触发**：你在对话里报告一个 bug（复现步骤、现象）时，模型自动按它的流程接管诊断。

**典型步骤**：

1. **先建反馈回路**：把「现象可观测、改动可验证」的回路搭起来——能稳定复现、每一步都有输出可对照。反馈回路不通，后面所有推断都不可信。
2. **缩小范围**：沿回路二分定位，逐步排除可疑代码。
3. **验证根因**：做出修复假设后用回路验证「改这里确实解决」，而不是靠猜。

**什么时候它会出现**：当你描述「这个功能坏了、现象是这样」时。注意它出现的前提是你给了足够的现象描述——反馈回路建不起来时，它大概率会反过来先问你要复现步骤。

> [!tip] 报 bug 的姿势
> 想让 `/diagnosing-bugs` 高效，先说清三件事：做了什么、期望什么、实际得到什么。反馈回路的前半段——复现——本来就依赖这些素材。

### 4.2 架构与术语类：/domain-modeling、/codebase-design、/improve-codebase-architecture

这组处理「架构与语言」层面：术语统一、模块划分、架构改进。

#### 4.2.1 /domain-modeling 术语敲定

一句话：`/domain-modeling` 敲定项目术语，把模糊说法精炼成统一词汇，沉淀到 [[CONTEXT.md]] 与 [[ADR]]。

**怎么被触发**：对话里出现含糊术语时自动触发；更常见的是被 `/grill-with-docs`（第 3 章）内部委托。

**典型步骤**：

```text
Challenge → Sharpen fuzzy language → Discuss scenarios
→ Cross-reference with code → Update CONTEXT.md → Offer ADRs
```

1. **Challenge**：质疑模糊表述（「你说的 order 是下单，还是订单状态？」）。
2. **Sharpen fuzzy language**：把含糊词改成精确术语。
3. **Discuss scenarios**：用具体场景验证术语在真实用法下不冲突。
4. **Cross-reference with code**：回到代码核对术语与现有命名是否一致。
5. **Update [[CONTEXT.md]]**：把敲定的词汇写进词汇表。
6. **Offer [[ADR]]**：涉及架构取舍时，提议写架构决策记录。

**什么时候它会出现**：当一场「这个名词到底指什么」的讨论需要落地时。`/grill-with-docs` 之所以是"有状态"盘问，正是因为内部调用了它——盘问产出的术语被它写成了文件。

#### 4.2.2 /codebase-design 深模块词汇表

一句话：`/codebase-design` 是一份**共享参考**，提供设计讨论时的统一词汇——它不执行流程，而是给其他 skill 和模型提供语言 [复用素材](workspace/matt-pocock-skills/02_deep_research.md)。

**怎么被触发**：主要作为共享参考被 `/domain-modeling` 交叉引用（第 2 章 2.3 的依赖链：model-invoked → 共享参考）。模型讨论模块划分时自动套用它的术语，它从不"单独跑起来"。

**五个核心术语**（源自《A Philosophy of Software Design》）：

| 术语 | 含义 |
|------|------|
| Module | 模块：一组相关功能的高内聚封装 |
| Interface | 接口：模块对外暴露的入口，越简单越好 |
| Depth | 深度：模块「隐藏复杂度 vs 暴露接口复杂度」之比 |
| Seam | 缝：可替换实现而不动调用方的地方 |
| Adapter | 适配器：转换两套接口差异的层 |

其中最有实操价值的是**删除测试**：判断一个抽象该不该存在——**如果把它删掉系统照样工作，说明它没有在提供价值，是多余的层**。讨论「这个模块要不要抽」时，用删除测试能最快结束争论。

> [!tip] 把删除测试当日常尺子
> 每次犹豫「要不要加一层抽象」，先问：删掉它，调用方需要改吗？如果不用改，这就是纯装饰层。

**什么时候它会出现**：当设计讨论需要精确语言时——它是词汇表不是入口，你不会看到它"被调用"，只会看到它的术语出现在讨论里。

#### 4.2.3 /improve-codebase-architecture

一句话：`/improve-codebase-architecture` 霰弹式地给你一份架构改进建议清单。

**怎么被触发**：你问「这个代码库的架构怎么改进」时自动触发。

**典型步骤**：扫描代码库 → 按模块 / 耦合 / 可测性等维度列出改进点 → 给出建议清单。它的特点是不深挖单个问题，而是**广度覆盖**，一口气把所有看得到的问题摆出来。

> [!warning] 别把它并进 grill（Issue #274）
> 社区实测发现，把它加进 grill 流程后，模型会对每个小问题都给出长篇改进建议，把简单盘问拖成话痨 [Issue #274](https://github.com/mattpocock/skills/issues/274)。要架构意见时单独问它、且限定范围（「只看 X 模块」），不要让它常驻盘问流程。

**什么时候它会出现**：当「看看整体架构有什么问题」被提出时。注意它给的是建议清单，不是可直接执行的 spec——真要落地还要回到 `/to-spec`。

### 4.3 决策与研究类：/wayfinder、/research

这组处理「还没到写代码」的工作：做决策、做研究。

#### 4.3.1 /wayfinder 拆 Decision ticket

一句话：`/wayfinder` 把一个悬而未决的决策**拆成 Decision ticket**——它的产出是「要做的决策」，不是「要建的代码」。

**怎么被触发**：对话遇到阻碍进展的关键决策点时自动触发。

**典型步骤**：识别阻塞决策 → 列出决策选项与权衡 → 把决策拆成一张可独立处理的 Decision ticket → 记录做出决策所需的信息与验证方式。

**什么时候它会出现**：当「这里得先定个方案才能继续」时。它和 `/to-tickets` 的区别：to-tickets 拆的是实现切片（怎么建），wayfinder 拆的是决策（先定哪个方向）。

> [!note] 决策也是工作单元
> 把「决策」当成一张可跟踪的 ticket，是 wayfinder 的核心思路——决策不该悬在对话里，而该像任务一样被记录、被追踪、被关闭。

#### 4.3.2 /research 研究类工作

一句话：`/research` 处理研究类工作：查文档、对比方案、收集证据。

**怎么被触发**：对话需要「先调研一下再定」时自动触发。

**典型步骤**：明确研究问题 → 检索文档 / 代码 / 社区 → 整理证据 → 给出结论或选项对比。

**什么时候它会出现**：当你说「看看有没有更好的方案 / 查一下这个库怎么用」时。它通常发生在 grill 之前——研究是收集事实，盘问是打磨决策，二者互补。

### 4.4 协作与交接类：/prototype、/handoff、/resolving-merge-conflicts

这组负责「临时实验」与「跨会话协作」。

#### 4.4.1 /prototype 一次性原型

一句话：`/prototype` 用一次性原型回答**单个设计问题**，做完就扔。

**怎么被触发**：你提出「不确定能不能行，先试一下」的设计问题时自动触发。

**两个分支**：

| 分支 | 适用 | 产出 |
|------|------|------|
| LOGIC.md | 终端逻辑型 app | 聚焦核心逻辑的原型 |
| UI.md | 界面方案对比 | 多个 UI 变体供你挑 |

**四条硬规则**：

1. **一条命令可跑**：原型必须能用一条命令跑起来，不折腾构建配置。
2. **内存态**：不接持久化，状态放内存即可——原型只验证可行性，不求真实性。
3. **最少打磨**：够用就行，不做生产级健壮性。
4. **throwaway branch**：跑在一个用完即弃的分支上，验证完就丢。

> [!example] 什么时候该开原型
> 不确定「这个交互逻辑对不对」→ 开 LOGIC.md 原型；不确定「这个 UI 走哪个方向」→ 开 UI.md 原型。验证完，回答的是设计问题，不是交付功能。

**什么时候它会出现**：主流程里常被 `/handoff` 带出——第 6 章会看到「handoff 出去 → prototype → handoff 回来」的绕行模式。

#### 4.4.2 /handoff 跨会话交接

一句话：`/handoff` 把当前会话压缩成一份**交接文档**，供下个会话无缝接力。

**怎么被触发**：上下文接近上限、或你明确说要换会话继续时自动触发。

**规则**：

- **保存到系统临时目录，不是工作区**：交接文档不污染仓库。
- **含 suggested skills**：文档里列出下个会话建议调用的 skill。
- **引用而非复制工件**：文档指向工件位置，不把代码 / 文档内容复制进来，保持轻量。
- **脱敏**：交接文档移除敏感信息（密钥、私有细节）。
- **支持参数描述下个会话焦点**：触发时可用一句话告诉它下个会话要解决什么。

handoff 文档模板大致长这样：

```markdown
# Handoff: <主题>
## 目标
<下个会话要解决的问题>
## 现状
<关键决策与已完成部分（引用而非复制）>
## 建议
- 调用 /<skill-name> …
- 参考 <工件路径>
```

> [!warning] 与 compact 的分工
> 全仓库扫描确认**仓库中已无 `/compact` 独立 skill**（已删除 / 更名）。现在的分工是：**同会话上下文过长，用 Claude Code 内置 compact 继续；跨会话交接，用 `/handoff`**。别再找 `/compact` 这个命令了。

**什么时候它会出现**：多会话构建的分叉点。它是第 6 章「上下文卫生」的关键工具——Smart Zone 约 12 万 token，超限就 `/handoff` 分叉后开新会话。

#### 4.4.3 /resolving-merge-conflicts

一句话：`/resolving-merge-conflicts` 解决 git 合并冲突。

**怎么被触发**：合并 / rebase 出现冲突时自动触发。

**典型步骤**：定位冲突文件 → 逐块理解两侧意图 → 结合 spec 决定保留哪边或合并 → 验证冲突解决不破坏行为。

**什么时候它会出现**：多分支并行开发时。它依赖你对「哪个意图是对的」的判断——模型能帮你读代码、比对差异，但最终取舍仍需你确认。

### 本章小结

- 12 个 model-invoked skill 由触发词或上级 skill 自动带出，你几乎不会直接敲它们；触发靠 description 里的 "Use when..." 触发短语。
- 核心工程原语：`/grilling` 一次一问盘问、`/tdd` 红-绿-重构、`/code-review` 双路子代理审查、`/diagnosing-bugs` 先建反馈回路——它们正是第 3 章 `/grill-with-docs`、`/implement` 内部驱动的引擎。
- 架构术语类：`/domain-modeling` 敲定术语写 [[CONTEXT.md]] + [[ADR]]；`/codebase-design` 提供 Module / Interface / Depth / Seam / Adapter 五词与删除测试；`/improve-codebase-architecture` 霰弹式列改进点（别并入 grill，会话痨）。
- 决策研究类：`/wayfinder` 拆 Decision ticket（决策而非构建）；`/research` 处理研究类工作。
- 协作交接类：`/prototype` 一次性原型（LOGIC / UI 两分支）；`/handoff` 写交接文档到系统临时目录；`/resolving-merge-conflicts` 解冲突；`/compact` 已删除，同会话用内置 compact、跨会话用 `/handoff`。
- 与第 3 章的配合是单向委托：user-invoked（`/grill-with-docs`、`/grill-me`、`/implement`）调用 model-invoked，model-invoked 再引用共享参考（`/codebase-design`）。

---

## 第五章 配置与定制

第 4 章结尾的问题——为什么 `/grill-me` 只能被你亲手敲，而 `/grilling` 会在你说 "grill me" 时自动出现——其实不是魔法，背后是 SKILL.md 的 frontmatter 和一套配置文件在起作用。这一章解决三件事：装完之后四类配置文件各归谁管、怎么改；调用模型 frontmatter 每个字段的真实含义；以及怎么写一个自己的 [[Agent Skill]] 接入这套框架。命令与示例可直接复制。

### 5.1 配置文件体系怎么改

先看清四类配置文件的分工。它们不是平等的：每一份都有一个"管理者" skill 负责自动维护，你手动改之前要先知道会不会被覆盖 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

| 文件 | 职责 | 管理者 | 默认谁来写 |
|------|------|--------|-----------|
| `CLAUDE.md` | Claude Code 的仓库规则 + `## Agent skills` 块 | `/setup-matt-pocock-skills` | 初始化时自动写 |
| `AGENTS.md` | Codex 跨平台契约，内容与 CLAUDE.md 一致 | `/setup-matt-pocock-skills` | 初始化时自动写 |
| [[CONTEXT.md]] | 项目术语词汇表 | `/domain-modeling`、`/grill-with-docs` | 每次盘问 / 建模时更新 |
| `.agents/adr/` | 架构决策记录（[[ADR]]） | `/domain-modeling` | 有决策时写入 |

**CLAUDE.md / AGENTS.md 归 `/setup-matt-pocock-skills` 管。** 第 1 章 1.4 讲过初始化流程：它探索仓库后把 `## Agent skills` 块写进这两个文件，同时生成 `docs/agents/`。需要你手动改的是 `## Agent skills` 块**之外**的"项目专属规则"——比如「本仓库测试一律用 Vitest」「发布前必须跑 typecheck」这类与 skill 无关的工程约束。块内那一列斜杠命令与说明留给初始化工具维护，你手改后下次重跑初始化可能被覆盖。

`## Agent skills` 块结构大致长这样（比第 1 章 1.4 的示例多了仓库级配置记录——这正是 setup 先问 issue tracker 与标签的原因）：

```markdown
## Agent skills

本仓库使用 [[Matt Pocock Skills]] 框架。
issue tracker：GitHub Issues；标签：`ready-for-agent`、`needs-spec`、`triage`。

- `/grill-with-docs` — 有状态盘问，产出 ADR 与词汇表
- `/to-spec` — 把对话合成 spec，发布到 issue tracker
- `/to-tickets` — 把 spec 拆成纵向切片 tickets
- `/implement` — 基于 spec/tickets 实现，内部驱动 tdd → code-review
```

**[[CONTEXT.md]] 归 `/domain-modeling` 和 `/grill-with-docs` 管。** 它是领域词汇表，第 4 章 4.2 看到 `/domain-modeling` 的步骤里有 "Update CONTEXT.md"，重跑盘问会覆盖你手动改的内容。**什么时候需要手动补**？当仓库里有 skills 探测不到的业务黑话时——把「销售口中的 pipeline 指商机阶段，不是 CI 管道」这种领域知识写进去，后续所有 skill 都受益。

**`.agents/adr/` 由 `/domain-modeling` 在有架构决策时写入。** ADR 记录的是决策 + 被拒方案 + 原因（仓库里 ADR-0001 记硬/软依赖分离、ADR-0002 记 Plugin 分发决策）。它是**审阅对象，不是编辑对象**——决策落盘后你来审、必要时要求改写，但不要在 skill 没有产出时自己造一份。

> [!tip] 一句话记住分工
> CLAUDE.md / AGENTS.md 管"仓库有哪些 skill 和规则"，setup 写；CONTEXT.md 管"术语怎么叫"，domain-modeling 写；`.agents/adr/` 管"为什么这么定"，domain-modeling 写、你审。最安全的手动编辑区是 CLAUDE.md 里 `## Agent skills` 块之外的工程规则。

### 5.2 调用模型：user-invoked 与 model-invoked 的 frontmatter

第 2 章 2.2 用一张表区分了两组 skill，这一节看它们的 SKILL.md 到底写了什么。调用模型只有一个轴——**invocation（调用方式）**——由仓库内 `.agents/invocation.md` 统一定义，落到每个 SKILL.md 的 frontmatter [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

**user-invoked 的双保险**（看 `/grill-me`）：

```yaml
---
name: grill-me
description: 快速无状态盘问，委托 grilling 原语，跑完即止。
disable-model-invocation: true
policy:
  allow_implicit_invocation: false
---
```

两个字段各管一层：

- `disable-model-invocation: true`：**模型不能凭上下文自动触发它**。模型不会在对话里判断"该 grill-me 了"然后自己跑，只有你敲 `/grill-me` 才会执行。
- `policy.allow_implicit_invocation: false`：**其他 skill 也不能隐式调用它**。这是对"user-invoked 不能被别的 skill 触发"的显式声明，配合第 2 章 2.3 的调用边界使用。

**model-invoked 的默认状态**（看 `/grilling`）：

```yaml
---
name: grilling
description: |
  Use when a plan or design needs to be stress-tested before building.
  Also use when the user says "grill me" or asks "is this solid?".
  Asks one question at a time with a recommended answer.
---
```

**description 面向两个完全不同的读者，写法因此相反：**

| 维度 | user-invoked | model-invoked |
|------|--------------|---------------|
| 读者 | 人类 | 模型 |
| 内容 | 一行摘要，无触发词 | "Use when..." 触发短语 + 行为描述 |
| 作用 | 告诉你这个命令是干嘛的 | 模型每轮加载，用来匹配当前上下文 |
| 加载成本 | 低 | 高（每轮都进上下文） |

> [!note] 为什么 model-invoked 的 description 必须写触发词
> 模型每轮对话都会读一遍所有 model-invoked skill 的 description，用它判断"当前上下文该不该触发这个 skill"。触发词就是匹配信号——你说 "grill me"，模型在 description 里命中 "user says 'grill me'"，于是套用 `/grilling` 的流程。触发词越贴近真实触发场景，触发越可靠；写成一行含糊摘要，模型就不知道该不该用。

> [!warning] user-invoked 的 description 别写触发词
> 如果给 user-invoked 的 description 也写 "Use when..."，模型可能误以为它可被上下文触发，和 `disable-model-invocation: true` 自相矛盾。一行人类可读的摘要就够了。

### 5.3 自定义 skill 接入本框架

装别人的 skill 只是开始，这套框架真正的价值是把**你自己的流程**写成 [[Agent Skill]] 接进来。skill 是指令集、不是插件——它不增强模型能力，只结构化对话，所以一份好的 SKILL.md 通常不超过 100 行 [Skills vs Plugins](https://github.com/johnlarkin1/claude-code-extensions/blob/main/claude-docs/skills-vs-plugins.md)。

**SKILL.md 模板**（可直接复制）：

```markdown
---
name: my-skill
description: |
  Use when <什么情境该触发>。
  <一行说明做什么>。
---

# 目标
<这个 skill 解决什么问题，一句话>

## 步骤
1. <第一步动作> — 完成标准：<可检查的结果>
2. <第二步动作> — 完成标准：<可检查的结果>

## 参考
- <按需查阅的规则 / 术语，不塞进步骤>

## 依赖
- 运行 `/some-model-skill` 获取 <上下文>
```

**写完后用六项质量关卡自查**（第 3 章 3.4 引出的清单）：

| 关卡 | 要求 | 常见反例 |
|------|------|---------|
| description 触发词 | model-invoked 的 description 含 "Use when..." 触发短语 | 只写 "处理 bug" 这种模糊摘要 |
| 篇幅 | SKILL.md ≤ 100 行 | 写了 300 行，把每种情况都条件化 |
| 无时间敏感 | 不含日期、版本声明等会过期的信息 | "Claude Code v2.5 的新特性" |
| 术语一致 | 与 [[CONTEXT.md]] 词汇表对齐 | 一会儿 order 一会儿 ticket |
| 含具体示例 | 有可参考的实例，防模型幻觉 | 只有抽象描述 |
| 引用仅一级深度 | 依赖用 `/skill` 散文式引用 | 把一个 skill 完整嵌进另一个 |

> [!tip] 写完先用 /writing-great-skills 过一遍
> 写完别急着发布，先触发 `/writing-great-skills`（第 3 章 3.4.3）让它按这份清单审你的草稿——它就是干这个的参考 skill。

**发布到 Plugin 分发给团队。** 要像 mattpocock/skills 那样把多个 skill 打包成团队市场，需在插件仓库根目录放 `.claude-plugin/marketplace.json`，声明市场本身和它包含的插件 [plugin-marketplaces 文档](https://code.claude.com/docs/en/plugin-marketplaces)：

```json
{
  "name": "my-team-skills",
  "owner": "my-org",
  "plugins": [
    {
      "name": "my-team-skills",
      "repo": "my-org/my-team-skills",
      "description": "团队私有 skills 市场，可与 mattpocock/skills 并存"
    }
  ]
}
```

`name` 与 `owner` 组合构成市场标识，`plugins[]` 列出市场分发的插件（每个插件仓库内还有自己的 `plugin.json` 声明包含哪些 skill）。团队拿到后通过 `extraKnownMarketplaces` 或 `/plugin marketplace add my-org/my-team-skills` 安装即可。单人自用则不用走这一步——直接把 skill 放进仓库 `.claude/skills/` 或 `npx skills add` 即可。

> [!example] 何时才需要 marketplace.json
> 3 人以上团队、要求所有成员技能版本一致、不想让成员各自复制维护 SKILL.md 时，才需要建市场。单人项目直接放仓库 `.claude/` 就行，别为一个小 skill 建整个市场。

### 本章小结

- 配置文件各有管理者：CLAUDE.md / AGENTS.md 归 `/setup-matt-pocock-skills`，[[CONTEXT.md]] 归 `/domain-modeling` + `/grill-with-docs`，`.agents/adr/` 由 domain-modeling 写、你来审；最安全的手动编辑区是 CLAUDE.md 里 `## Agent skills` 块之外的工程规则。
- user-invoked 用 `disable-model-invocation: true` + `policy.allow_implicit_invocation: false` 双保险，description 是面向人类的一行摘要；model-invoked 靠 description 里的 "Use when..." 触发短语由模型每轮匹配上下文触发。
- 自定义 skill 用 SKILL.md 模板起步、控制在 100 行内，过六项质量关卡（触发词 / 篇幅 / 无时间敏感 / 术语一致 / 具体示例 / 一级引用）。
- 团队分发才需要 `.claude-plugin/marketplace.json`（name、owner、plugins[]）；单人自用直接放仓库 `.claude/skills/`。

---

## 第六章 工作流实战演练

第 3、4 章把 [[Matt Pocock Skills]] 的 22 个 skill 拆开讲了，但真实工作是把它们串成一条从想法到交付的流水线。这一章用一个真实感的小例子——给订单列表加一个「导出 CSV」的功能——把主流程完整走一遍，并讲清上下文卫生与两种分叉（原型绕行、多会话构建）。所有命令都可以照着敲。

### 6.1 ask-matt 主流程：idea → ship 全演练

先明确 `/ask-matt` 的位置：它是路由器，记不住全流程时敲它，它会按情境把你引到下面这条主流程；流程本身从 `/grill-with-docs` 开始 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

**场景设定**：仓库是一个订单管理系统，列表页展示订单（数据暂存内存），需求是「加一个导出 CSV 的功能」。

**第一步：`/grill-with-docs` 盘问打磨。** 你敲：

```text
/grill-with-docs 给订单列表加一个导出 CSV 的功能
```

它内部委托 `/grilling` 一次一问地拷问：导出的是筛选结果还是全部订单？中文列名用 UTF-8 还是带 BOM？空数据导出空文件还是报错？同时 `/domain-modeling` 敲定「导出 / 下载」两个词，写进 [[CONTEXT.md]]；编码取舍记成 [[ADR]]。产出三样：盘清楚的方案、词汇表、决策记录——后面 `/to-spec` 直接引用。

**第二步：分支——需要原型验证吗？** 盘问中冒出一个真问题：CSV 中文编码在 Excel 打开会不会乱码，属于「不确定能不能行，先试一下」的单一设计问题，按第 4 章的绕行模式处理：

```text
/handoff "验证 CSV 导出在 Excel 中的中文编码表现"   → 新会话
/prototype                                          → UI.md 分支，跑在 throwaway branch
/handoff "结论：采用 UTF-8 BOM，Excel 中文显示正常"  → 回原会话
```

**第三步：分支——单会话还是多会话？** 判据是能否拆成多个可独立交付的纵向切片：

| 用单会话 | 用多会话 |
|----------|----------|
| 改动小，一个纵向切片就能做完 | 能拆多个切片，每个都要独立验证 |
| 不想付跨会话交接成本 | 切片有先后依赖，或 planning 上下文已很大 |

CSV 导出能拆成 3 个切片，选多会话：

```text
/to-spec     → 六段式 spec + ready-for-agent 标签（issue #12）
/to-tickets  → 拆成 3 个纵向切片（issue #13 #14 #15）
```

**第四步：`/implement` 实现。** 每个 ticket 从新会话敲一次 `/implement`，内部驱动 `/tdd`（红-绿-重构）→ `/code-review`（双路审查）→ commit。

> [!example] 完整命令序列（可照抄）
> ```text
> # 会话 A —— 规划
> /grill-with-docs 给订单列表加一个导出 CSV 的功能
>   （盘问导出范围 / 编码 / 空数据；写 CONTEXT.md + ADR-0003）
> /handoff "验证 CSV 导出在 Excel 中的中文编码表现"
>   （新会话 B）
> /prototype
>   （UI.md 分支，生成最小导出按钮 + 样例 CSV，验证 UTF-8 BOM）
> /handoff "结论：采用 UTF-8 BOM"
>   （回会话 A）
> /to-spec
>   （发布 issue #12，打 ready-for-agent）
> /to-tickets
>   （拆 issue #13 #14 #15，quiz 确认）
>
> # 会话 C1 / C2 / C3 —— 每个 ticket 一个新会话
> /implement "issue #13：CSV 生成核心逻辑（转义规则）"
>   （内部 /tdd → /code-review → commit）
> /implement "issue #14：导出入口（按钮 + 下载）"
> /implement "issue #15：边界处理（空数据 / 超大导出）"
> ```

### 6.2 上下文卫生（Context Hygiene）策略

为什么反复强调「新会话」「不 compact」？因为上下文窗口有限，且模型在不同长度区间表现差异很大。

**规则一：步骤 1-3 在同一上下文窗口完成，不 compact 不清除直到 `/to-tickets`。** 规划三步是一条连续对话：grill 的问答、敲定的术语、spec 的取舍，下游 skill 都要靠它。中途 compact 会打断这条链——直到 `/to-tickets` 把切片发布到 issue tracker，才允许关闭规划会话。

> [!warning] 规划阶段别急着 compact
> 仓库里没有 `/compact` 独立 skill（第 4 章已更正），同会话压缩用 Claude Code 内置 compact。规划阶段（grill → spec → tickets）**不要**用它——产物一旦落到 issue tracker，规划会话才失去保留价值；每个 `/implement` 又在新会话里跑，不靠压缩续命。

**规则二：每个 `/implement` 从新会话开始。** 实现是长任务，且 ticket + spec 已在 issue tracker 里，契约完整。拖着一整段规划对话去实现，既浪费 token 又可能被讨论细节带偏；新会话里敲 `/implement "issue #13"`，读 ticket 就够了。

**规则三：Smart Zone 约 12 万 token，超限用 `/handoff` 分叉。** 上下文不是「还有空间就还能用」——模型在约 12 万 token 的 Smart Zone 内注意力最好，超过后 recall 与遵循度明显下降。规划三步尽量压在 Smart Zone 内；万一没规划完就接近上限，用 `/handoff` 把进展压缩成交接文档，开新会话继续。

```text
上下文窗口
├─ Smart Zone（约 12 万 token）：注意力最佳，规划三步在这里完成
├─ 饱和区：还差一点没做完 → /handoff 分叉，开新会话
└─ 上限区：再往上是硬挤，质量崩坏，必须分叉
```

### 6.3 原型绕行与多会话构建演练

上一节讲了「为什么」，这一节看「怎么操作」。

**原型绕行：`/handoff` 出去 → `/prototype` → `/handoff` 回来。** 具体三步：

1. 在规划会话里敲 `/handoff "验证 CSV 导出在 Excel 中的中文编码表现"`。它会写一份 [[Handoff]] 交接文档到系统临时目录（不污染仓库），含 suggested skills（此处指向 `/prototype`），作为下个会话的启动指引。
2. 开新会话，敲 `/prototype`。按第 4 章规则它跑在 throwaway branch，用一条命令可跑的最小原型回答设计问题。你验证 UTF-8 BOM 方案，得到结论。
3. 在原型会话里再敲 `/handoff "结论：采用 UTF-8 BOM，Excel 中文正常"`，回到原会话。规划对话原封不动，只多了一条已验证结论，接着 `/to-spec`。

> [!tip] handoff 是一句话传递焦点
> `/handoff` 支持用一句话描述下个会话焦点。绕行出去写「要验证什么」，回来写「结论是什么」——交接文档会自动带上，新会话不会跑偏。

**多会话构建：每 ticket 一个 `/implement`。** `/to-tickets` 发布后，切片间可能有声明好的阻塞边。逐个开新会话实现，有依赖按顺序，无依赖可并行：

```text
会话 A（规划，保持不 compact 不清除）
 ├─ /grill-with-docs ──→ CONTEXT.md + ADR
 ├─ /handoff ──→ 会话 B /prototype ──→ /handoff 回 A
 ├─ /to-spec ──→ issue #12（ready-for-agent）
 └─ /to-tickets ──→ issue #13 #14 #15（quiz 确认）

会话 C1（新会话）: /implement #13 → /tdd → /code-review → commit
会话 C2（新会话）: /implement #14 → /tdd → /code-review → commit
会话 C3（新会话）: /implement #15 → /tdd → /code-review → commit
```

> [!warning] 有阻塞边就别并行
> 如果 ticket #14 依赖 #13 的接口，并行实现会互相踩踏。`/to-tickets` 会在切片上标出阻塞边，实现时照它排顺序，不要贪并行。

### 6.4 社区最佳实践：从 4 个核心 skill 起步

社区实测（[dev.to 评测](https://dev.to/evan-dong/i-tried-the-claude-code-skills-repo-that-got-77k-stars-here-is-what-works-and-what-does-not-57a4)）的建议很直接：**不要一次全装，从 4 个核心 skill 起步**——`/grill-with-docs`（想清楚）、`/tdd`（写对）、`/diagnosing-bugs`（修 bug）、`/code-review`（把关）。这四条覆盖最常用的回路；grill-with-docs 内部会委托 `/grilling` 与 `/domain-modeling`，随它一起装齐，实际就 6 个。

**一次全装太多的问题**（社区实测时仓库一度有 28 个 skill，当前 plugin.json v1.2.0 是 22 个）[plugin.json](https://raw.githubusercontent.com/mattpocock/skills/main/plugin.json)：

- 每个 model-invoked 的 description 每轮都进上下文，全装 = 每轮白付大量 token；
- 场景重叠导致误触发，模型经常用错 skill；
- 22 个斜杠命令记不住，反而不知道用哪个。

**按需扩展策略**：先用 4 个核心跑通一个真实小功能 → 每遇到「这个场景我缺个 skill」就补一个：做大功能规划补 `/to-spec`、`/to-tickets`；跨会话协作补 `/handoff`；设计验证补 `/prototype`；写自定义 skill 补 `/writing-great-skills`。拿不准补谁时，让 `/ask-matt` 告诉你。

> [!note] 4 个核心也是第 8 章的起点
> 这套「少而精、按需扩展」的选择逻辑，正是第 8 章「为自己的项目挑选与裁剪 skill」的方法论基础。

### 本章小结

- 主流程：`/grill-with-docs` →（原型绕行）→ `/to-spec` → `/to-tickets` → 每 ticket 一个 `/implement`；`/implement` 内部驱动 `/tdd` → `/code-review` → commit。
- 上下文卫生三条：步骤 1-3 同一窗口不 compact 不清除直到 `/to-tickets`；每个 `/implement` 从新会话开始；Smart Zone 约 12 万 token，超限用 `/handoff` 分叉。
- 原型绕行是「handoff 出去 → prototype → handoff 回来」，规划会话原封不动，只带回已验证的结论。
- 多会话构建按纵向切片逐个 `/implement`，有阻塞边就按顺序，别贪并行。
- 社区最佳实践：从 grill-with-docs、tdd、diagnosing-bugs、code-review 四个核心起步，按需扩展，别一次全装。

---

## 第七章 常见问题与排错

第 6 章把主流程跑通了，但跑起来之后才是坑的开始。这一章按「现象 → 处理」的方式收集真实会踩的问题：装不上、不触发、行为怪、选型错、版本回退不了。每条命令都可以直接复制，先记一句总纲——**排错先分锅：是安装问题、行为问题，还是选型问题**，再按小节对号入座。

### 7.1 安装与触发排错

先处理最打击人的一类：装完了，skill 却不出现。下面是四个高频现象、原因与处理命令 [中文安装教程](https://cloud.tencent.com.cn/developer/article/2697381)：

| 现象 | 原因 | 处理 |
|------|------|------|
| `/plugin install` 报 plugin "not found" | 本地市场元数据过期，找不到插件 | `/plugin marketplace update <市场名>` 再重装 |
| skill 装了却不出现 | 插件缓存损坏 / 未刷新 | `rm -rf ~/.claude/plugins/cache` 后重启重装 |
| npx 和 Plugin 两条路线 skill 重复 | 两套机制同时装了同类 skill | 二选一，删除其中一种（见下方说明） |
| URL 型市场相对路径插件报 "path not found" | 市场用 URL 指向、插件按相对路径引用解析失败 | 改 Git 源（`owner/repo`）规避 |

对应命令序列：

```bash
# 现象一：plugin not found —— 先更新市场元数据，再重装
/plugin marketplace update <市场名>
/plugin install <插件名>@<市场名>

# 现象二：skill 装了不出现 —— 清缓存后重启重装
rm -rf ~/.claude/plugins/cache
# 重启 Claude Code，再执行 /plugin install <插件名>@<市场名>
```

> [!tip] 先更新市场，再谈重装
> plugin "not found" 十有八九是市场元数据没刷新，不是插件真的不存在。先 `/plugin marketplace update <市场名>` 再重装，能省掉大半清缓存的操作。

**重复问题：两种方式 skill 重复。** npx 路线把 SKILL.md 作为**可编辑副本**写进仓库 `.claude/`；Plugin 路线是**只读自动更新**。想留哪个，取决于你要哪种特性：想项目内可改，删 Plugin；想跟随仓库推送自动同步，删 npx 副本。二选一删除其中一种后重启即可。

**URL 型市场相对路径问题。** 市场地址写成 URL、且插件以相对路径引用自身文件时，Claude Code 解析不到插件目录。规避方法是把市场换成 Git 源（`owner/repo`），让插件按仓库名解析，绕开相对路径歧义。

### 7.2 行为类问题

装好也触发了，但行为不对劲。四类高频问题：

**grill 话痨。** 这是社区反馈最多的一个问题（[Issue #274](https://github.com/mattpocock/skills/issues/274)）：`/grilling` 的核心是「一次一问、达成共识才行动」，但问得足够细时，一个简单问题可能触发 10-100 个追问。三种规避：

1. **直接声明时间不够**——告诉 agent `我时间不够，直接给我推荐答案`，让它跳过高频提问；
2. **改成 opt-in**——按第 5 章 frontmatter 加 `disable-model-invocation: true`，只有你显式敲 `/grilling` 才盘问；
3. **用 `/grill-me` 控制篇幅**——它是无状态薄封装，跑完即止，比 `/grill-with-docs` 的话痨概率低。

**模型差异大。** 社区实测发现同一个 skill 在不同模型上表现差异明显：反馈 Opus 4.6 下正常、4.7 表现差 [社区实测](https://dev.to/evan-dong/i-tried-the-claude-code-skills-repo-that-got-77k-stars-here-is-what-works-and-what-does-not-57a4)。这属于平台侧差异，不是 skill 指令本身的问题。排法：先确认「是哪个模型下的问题」，同样的 prompt 换个模型复现一次，把锅甩对地方再决定要不要换模型跑盘问类流程。

> [!warning] 排错先分锅
> skill 行为异常时，先分清是 skill 指令问题还是模型遵循问题。同样的 prompt 换个模型复现一次，能立刻区分——复现不了是 skill 指令问题，复现了是模型问题。

**CONTEXT.md 漂移。** 项目代码变化后，`/domain-modeling` 之前写入的 [[CONTEXT.md]] 术语可能过时。处理方式不是手动改词汇表，而是重跑一次盘问：`/grill-with-docs` 或 `/domain-modeling` 会重新 cross-reference with code，自动更新词汇表与 ADR。

**识别非官方 skill。** 仓库只有 22 个官方 skill，但社区流传一些声称「同款」的 skill（如 `caveman`）。识别方法：核对 plugin.json v1.2.0 的官方清单，或看 skill 的 source 是否指向 mattpocock/skills。非官方 skill 在正文里要谨慎引用，避免被幻觉内容带偏。

### 7.3 Skill vs Plugin vs MCP vs Hook：怎么选

这一节是本章重点。四个概念常被混淆，但解决的是**四类完全不同的问题** [Skills vs Plugins](https://github.com/johnlarkin1/claude-code-extensions/blob/main/claude-docs/skills-vs-plugins.md) [Skills vs MCP vs Plugins](https://www.morphllm.com/claude-code-skills-mcp-plugins)：

| 维度 | Skill | Plugin | MCP | Hook |
|------|-------|--------|-----|------|
| 本质 | 单个能力模块（SKILL.md 指令集） | 分发容器，打包 skills / commands / hooks / MCP | 外部数据与工具连接协议 | 生命周期事件自动化脚本 |
| 解决什么 | 结构化对话、流程/SOP | 团队统一分发与版本一致 | 接外部数据源 / 工具 | 特定时机自动触发动作 |
| 触发方式 | 斜杠命令 / 上下文自动 | 安装后命名空间调用 | MCP tools 工具调用 | 事件触发（PreToolUse / PostToolUse 等） |
| 作用范围 | 跨 Claude.ai / API / Code | 仅 Claude Code | 跨客户端 | 仅 Claude Code |
| 适用场景 | 单人自用、流程/SOP | 团队 3 人以上统一分发 | 要连数据库 / API / 内部服务 | 生命周期自动化（校验 / 审计 / 通知） |
| 复杂度 | 低 | 中 | 高（需维护服务端） | 中 |

> [!note] Plugin 是容器，不是与 Skill 互斥
> 一个 Plugin 可以同时打包 skills、注册 hooks、挂载 MCP servers。所以正确的问法不是「Plugin 还是 Skill」，而是「我的场景属于流程、分发、数据、时机里的哪一类，再决定用哪个容器装它」。

**决策框架**（按你的诉求对号入座）：

- **流程 / SOP 用 Skill。** 想把「每次做 X 都按这五步走」固化成指令，写一份 SKILL.md 即可，单人自用零成本，按需触发。
- **团队 3 人以上统一分发用 Plugin。** 要让所有成员技能版本一致、不用各自维护副本，把 skills 打包成 Plugin 市场分发（第 5 章 5.3 的 `marketplace.json`）。
- **外部数据连接用 MCP。** 要接数据库、内部 API、第三方服务，用 MCP server 暴露工具，让模型能调用真实数据而不是靠猜。
- **生命周期自动化用 Hook。** 想在特定时机（工具调用前、会话结束后）自动执行动作——比如提交前强制跑检查、敏感操作拦截——用 Hook。

> [!tip] 一句话选型
> 单人固化流程用 Skill；团队统一分发用 Plugin；要接外部数据用 MCP；要在生命周期「自动动手」用 Hook。遇到模糊需求，先问「我要解决的是流程、分发、数据还是时机」，答案就是选型。

### 7.4 版本管理限制

版本回退是这套框架的硬伤，两条路线都受限（[Issue #274](https://github.com/mattpocock/skills/issues/274)）：

- **npx skills 只下载最新版，无法回退。** `npx skills update` 永远拉到最新，没有 `--version` 指定旧版的能力。想要旧版，唯一办法是手动从仓库历史定位旧版 SKILL.md，复制到仓库 `.claude/` 自建一份可编辑副本——代价是后续更新要自己维护。
- **Plugin 自动更新，团队版本由 marketplace 控制。** Plugin 的更新跟随市场推送，成员端拿到的是市场最新版，个体无法锁定到某个历史版本。要控制团队版本，只能在市场侧（插件仓库 tag）管理，成员端统一跟随。

> [!warning] 两个「无法回退」的共同后果
> 因为无法干净回退，升级前把当前可用的 skill 复制一份到仓库 `.claude/` 或独立目录，是最简单有效的「软回退」手段。npx 路线尤其建议保留仓库里那份可编辑副本——它就是你的版本快照。

### 本章小结

- 安装排错按「现象 → 处理」查：plugin not found 先 `/plugin marketplace update <市场名>` 再重装；skill 不出现清 `~/.claude/plugins/cache` 后重启；两条路线重复二选一删一个；URL 型市场相对路径报错改 Git 源规避。
- 行为问题分四类：grill 话痨（声明时间不够 / 改 opt-in / 用 `/grill-me`）；模型差异先换模型复现分锅；[[CONTEXT.md]] 漂移重跑盘问更新；非官方 skill 核对官方清单识别。
- 选型一句话：流程 / SOP 用 Skill，团队 3 人以上统一分发用 Plugin，外部数据连接用 MCP，生命周期自动化用 Hook；Plugin 是能装下另三种的容器。
- 版本回退是硬伤：npx 只给最新版，Plugin 跟随市场推送；升级前在仓库保留副本做「软回退」。

---

## 第八章 把 skills 应用到自己的项目

第 7 章讲完排错，但到这一步还只是"会用"——能不能把 [[Matt Pocock Skills]] 这套方法论变成你自己的，才是分水岭。这一章是正文的收尾，回答三个实操问题：怎么按自己项目的工作流挑选和裁剪 skill、怎么写第一个自定义 [[Agent Skill]] 并分发出去、以及在一个已经跑着 Claude Code 甚至 Codex 的既有仓库里如何稳妥接入。读完你可以在半小时内给任意项目配上一套"少而精"的 skills 组合。

### 8.1 为自己的项目挑选与裁剪 skill

装 skill 不是把仓库搬过来，而是给项目配流程。最大的坑是全盘照搬：`npx skills@latest add` 后 22 个全选。第 6 章 6.4 已经说过全装的代价——每个 model-invoked 的 description 每轮都进上下文、场景重叠导致误触发、22 个斜杠命令记不住。所以这里给一套三步骤选型思路。

**第一步：先画主工作流。** 别从"仓库里有哪些 skill"出发，从"我的项目反复发生哪几类任务"出发。列出 3~5 类最高频的工作，在下面的表里对号入座：

| 项目主工作流 | 起步 skill | 跑通后按需补 |
|------------|-----------|-------------|
| 新功能从想法到交付 | `/grill-with-docs`（连 `/grilling` + `/domain-modeling`） | `/to-spec`、`/to-tickets`、`/implement` |
| 排查 bug | `/diagnosing-bugs` | `/grill-me` 先问清上下文 |
| 写测试、保证正确性 | `/tdd` | `/code-review` 双路审查 |
| 跨会话长任务 | `/handoff` | `/prototype` 设计验证 |

这四行覆盖了大部分项目的主回路，正好是 6.4 说的"从 4 个核心起步"。注意 `/grill-with-docs` 内部会委托 `/grilling` 和 `/domain-modeling`，起步时连同它们一起装，实际是 6 个 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

**第二步：反选法裁剪。** 列出你**绝不会用**的 skill，直接不装。最实用的裁剪依据是硬依赖——第 1 章说过 `/to-spec`、`/to-tickets`、`/triage` 都依赖 issue tracker 和标签。如果项目不用 GitHub Issues / Linear（比如一个没有 issue 流程的个人项目），这三个 skill 装上去也找不到发布目标，跑完即废，干脆不装。

> [!tip] 裁剪比安装更重要
> 少装的每个 model-invoked skill，都是每轮对话省下的 token 和少一次误触发的机会。宁可用的时候敲 `/ask-matt` 让它推荐，也不要让一个用不到的 skill 常驻上下文。

**第三步：跑一个真实功能再扩展。** 用裁完的起步组合完成一个小功能，然后每遇到"这个场景我缺个 skill"补一个（沿用 6.4 的扩展策略）。这套"少而精、按需补齐"的节奏更接近作者本意——核心 skill 大多只有 12 行左右，作者赌的是"模型大多做对的事"，靠最小锚点而非全量指令 [仓库精读](https://cloud.tencent.com.cn/developer/article/2704288)。

### 8.2 编写自己的第一个 skill 并接入

选型是"用什么"，这一节是"写什么"。第 5 章 5.3 给了 SKILL.md 模板（frontmatter + `# 目标` + `## 步骤` + `## 参考` + `## 依赖`）和六项质量关卡，这里给一个能直接跑起来的完整实例，可以整段复制进自己的仓库。

**实例：一个 model-invoked 的 `draft-release-notes` skill**——用户说"帮我起草发布说明"时自动触发，把两次 tag 之间的 commit 整理成发布说明。

```markdown
---
name: draft-release-notes
description: |
  Use when the user asks to draft release notes or a changelog
  for the upcoming release. Summarizes the git diff since the
  last tag into user-facing change notes.
---

# 目标
把两次 tag 之间的 commit 整理成给用户看的发布说明。

## 步骤
1. 找上一个 tag：`git describe --tags --abbrev=0`
   — 完成标准：拿到一个 tag 名；没有 tag 则提示先打一个。
2. 生成提交清单：`git log <上一个tag>..HEAD --oneline`
   — 完成标准：得到 commit 列表。
3. 按前缀归类：feat / fix / docs / refactor / chore
   — 完成标准：每条 commit 分到一类。
4. 改写成用户视角：feat 写"新增了什么"，fix 写"修好了什么"
   — 完成标准：每类至少一句人话。
5. 输出 Markdown：标题带版本号与日期占位符
   — 完成标准：文档可直接发布。

## 参考
- 类型前缀约定见仓库 CONTRIBUTING.md；没有则按 Conventional Commits 默认归类。

## 依赖
- 可选：运行 `/code-review` 对发布说明做一次双路检查。
```

写完后按 5.3 的六项质量关卡自查，这个实例这样过关：

| 关卡 | 本实例怎么过关 |
|------|--------------|
| description 触发词 | 面向模型的 description 含 "Use when the user asks to draft release notes..." |
| 篇幅 | 约 20 行，远低于 100 行上限 |
| 无时间敏感 | 不写版本号 / 日期，用占位符 |
| 术语一致 | 通篇用 git tag / commit / release notes，不换说法 |
| 含具体示例 | 每一步都给了命令与可检查的完成标准 |
| 引用仅一级深度 | 只在依赖里散文式引用 `/code-review` |

> [!note] 三个字段的意图
> `name` 是触发名；`description` 面向模型、必须写清"什么情境该触发"（第 5 章 5.2 讲过的 model-invoked 写法）；步骤里"完成标准"是 5.3 模板的核心——它让模型知道"做到什么程度算完"，防过早完成。

**三种分发方式，按团队规模选** [plugin-marketplaces 文档](https://code.claude.com/docs/en/plugin-marketplaces)：

| 方式 | 做法 | 适用 |
|------|------|------|
| 仓库内自用 | 放 `.claude/skills/draft-release-notes/SKILL.md` | 单人项目，本仓库立刻可用 |
| GitHub + npx skills | 推到 `your-org/your-skills`，别的仓库执行 `npx skills@latest add your-org/your-skills` | 想分享、允许别人拿到可编辑副本 |
| 团队 Plugin | 加 `.claude-plugin/marketplace.json`（第 5 章 5.3 模板），成员 `/plugin marketplace add your-org/your-skills` | 3 人以上，要求版本一致、自动更新 |

三种方式按第 1 章的互斥规则，同一台机器同一批 skill 只走一种，别混装。单人项目直接用方式一，别为一个小 skill 建整个市场。

### 8.3 与本地/现有框架集成注意事项

真实项目多半不是从零开始的——仓库里可能已经有 CLAUDE.md、甚至同时跑 Codex。接入时注意三件事。

**双分发机制先对齐。** mattpocock/skills 自己就是"npx 可编辑副本 + Plugin 只读自动更新"双轨分发 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。你的自定义 skill 也要在接入时就选好轨道。集成进既有仓库前，先检查 `.claude/skills/` 下是否已有同名 skill——第 7 章 7.1 讲过两条路线重复的排错成本，别让一个仓库里同时躺着同名可编辑副本和同名插件。

**AGENTS.md 是跨平台契约，两边都要同步。** `/setup-matt-pocock-skills` 会把 `## Agent skills` 块同时写进 CLAUDE.md 和 AGENTS.md，因为两者各读各的：Claude Code 读 CLAUDE.md，Codex 读 AGENTS.md，对方默认忽略另一个。所以两块内容必须保持一致——你在 CLAUDE.md 手改 `## Agent skills` 块之外的工程规则时，同步改 AGENTS.md，反过来同理。只改一边，换工具时契约就丢一半。

> [!warning] 别只在一边加规则
> 如果仓库同时被 Claude Code 和 Codex 使用，只在 CLAUDE.md 里写"本仓库用 Vitest"，Codex 侧看不到；只在 AGENTS.md 里写，Claude Code 看不到。规则要么同步写进两份，要么维护一个同步脚本把一份镜像成另一份。

**与 Codex 同步的差异点。** 既有仓库如果像 mattpocock/skills 那样用同步脚本维持 CLAUDE.md / AGENTS.md 镜像，接入 skills 时要注意平台分发能力的不对称。这记在仓库的 [[ADR]]-0002 里：Claude Code 的 plugin.json 接受 skill 路径**数组**，能精确挑选要发布的子集；Codex 只接受单个路径**字符串**，无法从分桶结构中挑子集，所以 Codex Plugin 分发被**推迟**，先发能发的 Claude Code Plugin——这就是 deferred symmetry（刻意的不对称）[github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

对你的直接启示有两点：一是别把 Claude Code 的 plugin 行为迁移到 Codex 侧期待同样结果；二是这类"平台差异导致的延后"不是临时的，把原因、被拒方案写进 ADR，未来的维护者不用重新论证一遍为什么两边不对称。

### 本章小结

- 选型三步：画主工作流 → 从 4 个核心起步 → 反选法裁剪；有硬依赖的 `/to-spec`、`/to-tickets`、`/triage` 在没有 issue tracker 的仓库直接砍。
- 自定义 skill 用第 5 章 5.3 的模板起步，过六项质量关卡；`draft-release-notes` 实例约 20 行，可直接复制。
- 三种分发方式：仓库内 `.claude/skills/`（自用）、GitHub + `npx skills add`（分享）、marketplace.json Plugin（团队版本一致），同一批 skill 只走一种。
- 集成注意：CLAUDE.md / AGENTS.md 各读各的、内容必须同步；平台分发能力不对称（ADR-0002 的 deferred symmetry），把这类决策记成 [[ADR]]。

到这里，正文八章收尾。下一篇附录是命令速查卡，把安装、更新、初始化、触发、排错命令和 22 个 skill 的触发方式汇总成一页，日常随查随用。

---

## 附录 命令速查卡

> 使用指南的日常速查。命令按「安装 → 初始化 → 触发 → 排错 → 配置」分组，可直接复制。

---

### A. 安装与更新

#### A.1 npx skills 路线（可编辑副本，写入仓库 `.claude/`）

```bash
# 安装（交互式勾选 skill）
npx skills@latest add mattpocock/skills

# 更新
npx skills update
```

- 触发方式：`/skill-name`
- 局限：只下载最新版，无法回退旧版（需手动复制自建）

#### A.2 Claude Code Plugin 路线（只读自动更新）

```text
/plugin marketplace add anthropics/claude-plugins-official   # 官方市场缺失时
/plugin install mattpocock-skills@anthropics                # 安装
/reload-plugins                                             # 生效
```

- 触发方式：`/插件名:skill名`，如 `/mattpocock-skills:grill-with-docs`
- 作用域：**User**（所有项目）/ **Project**（写 `.claude/settings.json`）/ **Local**（仅本库本人）

> [!warning] 二选一
> 两种安装路线互斥，不要混装同一批 skill。

---

### B. 初始化

```text
/setup-matt-pocock-skills
```

- 每个新仓库第一次使用前运行一次
- 流程：Explore → Present → Confirm → Write
- 产出：CLAUDE.md / AGENTS.md 的 `## Agent skills` 块 + `docs/agents/`
- 配置项：issue tracker（GitHub / Linear / 本地）、triage 标签、文档保存位置
- 是 `/to-spec`、`/to-tickets`、`/triage` 的**硬依赖**（不配则这些 skill 跑完即废）

---

### C. 22 个 skill 触发速查表

#### C.1 user-invoked（10 个，斜杠命令，人显式触发）

| Skill | 作用 |
|-------|------|
| `/setup-matt-pocock-skills` | 初始化仓库配置（新仓库一次） |
| `/ask-matt` | 中央路由器，推荐当前情境最合适的 skill / flow |
| `/grill-with-docs` | 有状态盘问，副产品 CONTEXT.md + ADR |
| `/grill-me` | 无状态盘问，委托 grilling，跑完即止 |
| `/to-spec` | 合成六段式 spec，发布 issue tracker 打 `ready-for-agent` |
| `/to-tickets` | 拆纵向切片 tickets，quiz 确认后发布 |
| `/implement` | 基于 spec/tickets 实现，驱动 tdd → code-review → commit |
| `/triage` | issue/PR 分类状态机（Gather/Recommend/Verify/Grill/Apply） |
| `/teach` | workspace 内持续教师 |
| `/writing-great-skills` | skill 写作原则参考（纯参考） |

#### C.2 model-invoked（12 个，description 触发词，模型自动调用）

| Skill | 触发词示例 / 作用 |
|-------|------------------|
| `/grilling` | "grill me"；核心盘问原语 |
| `/tdd` | "test-first"、"red-green-refactor"；红-绿-重构 |
| `/code-review` | 审查分支/PR/WIP；双路并行子代理 |
| `/domain-modeling` | 敲定术语，更新 CONTEXT.md + ADR |
| `/prototype` | 一次性原型（LOGIC / UI 分支），throwaway branch |
| `/diagnosing-bugs` | 诊断 bug，建反馈回路 |
| `/improve-codebase-architecture` | 霰弹式架构改进方案 |
| `/wayfinder` | 拆 Decision ticket（决策而非构建） |
| `/research` | 研究类工作 |
| `/codebase-design` | 深模块词汇表（共享参考） |
| `/resolving-merge-conflicts` | 解决合并冲突 |
| `/handoff` | 压缩会话为交接文档到系统临时目录 |

> [!note] 调用边界
> user-invoked → model-invoked → 共享参考，不可逆向。user-invoked 不能调用另一个 user-invoked。

---

### D. 排错命令

| 现象 | 处理 |
|------|------|
| plugin "not found" | `/plugin marketplace update <市场名>` 再重装 |
| skill 不出现 | `rm -rf ~/.claude/plugins/cache` 后重启重装 |
| 两种方式 skill 重复 | 二选一，删除其中一种安装 |
| URL 型市场相对路径插件报 "path not found" | 改用 Git 源规避 |
| grill 话痨（Issue #274） | 直接说"我时间不够，跳过高频提问"；或用 `/grill-me` 控制篇幅 |
| 模型表现差异大 | 换模型验证；不同模型对同一 skill 遵循度不同 |

---

### E. 常用配置项速查

#### E.1 团队私有市场（`.claude/settings.json`）

```json
{
  "extraKnownMarketplaces": [
    {
      "name": "my-team",
      "owner": "my-org",
      "repo": "my-private-plugins",
      "type": "git"
    }
  ]
}
```

#### E.2 SKILL.md frontmatter 关键字段

```yaml
---
name: my-skill
description: >-
  Use when [触发场景]. [触发词放在描述开头]
disable-model-invocation: true   # user-invoked；省略 = model-invoked
policy:
  allow_implicit_invocation: false  # 与 disable-model-invocation 配套
---
```

- user-invoked：description 面向人类（一行摘要，无触发词）
- model-invoked：description 面向模型（含 "Use when..." 触发短语）

#### E.3 分发到 Plugin 市场（`.claude-plugin/marketplace.json`）

```json
{
  "name": "my-market",
  "owner": "my-org",
  "plugins": [
    { "name": "my-plugin", "source": "./my-plugin", "version": "1.0.0" }
  ]
}
```

---

> 参考：正文各章 + `02_deep_research.md` 素材索引 [U1]~[U9]。
