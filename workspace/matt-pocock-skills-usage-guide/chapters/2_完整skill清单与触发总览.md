# 第二章 完整 skill 清单与触发方式总览

第 1 章装好了环境，但要开始使用之前，你需要一张全局地图：这 22 个 [[Agent Skills]] 各自做什么、由谁来触发。本章把完整清单、user-invoked / model-invoked 分组、以及调用边界一次性讲清。读完你会知道哪些命令可以自己敲，哪些要让模型在对话中自动接手。

## 2.1 22 个 skill 全景总表

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

## 2.2 user-invoked vs model-invoked 分组

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

## 2.3 调用边界与依赖规则

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

## 本章小结

- plugin.json v1.2.0 共 22 个 skill：Engineering 17 个 + Productivity 5 个；触发类型以 SKILL.md frontmatter 实测为准。
- user-invoked（10 个）用斜杠命令由人显式触发；model-invoked（12 个）靠 description 触发词由模型按上下文自动调用。
- 依赖是单向的：user-invoked → model-invoked → 共享参考，不可逆向。
- user-invoked 之间不互相调用；流程推进靠你在会话里按顺序手动触发。
- skill 依赖用 `/skill` 散文式引用表达，不做深度交叉引用，保持每个 skill 独立可读。

下一章开始逐个上手 user-invoked 的 10 个 skill：先讲盘问类（/grill-with-docs、/grill-me）与规划类（/to-spec、/to-tickets），学会把模糊想法打磨成可执行的 spec 与 tickets。
