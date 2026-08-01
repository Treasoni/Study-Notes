# 第四章 model-invoked skills 逐个使用详解

第 3 章那 10 个 user-invoked skill 是你亲手敲斜杠命令触发的；这一章的 12 个 model-invoked skill 恰好相反——**你几乎不会直接敲它们**。它们由对话情境或上级 skill 自动带出：你在对话里说 "grill me"，模型就套用 [[Grilling]]；`/implement` 内部自动驱动 `/tdd` 与 `/code-review`。本章逐个讲清它们是什么、被什么触发、内部走什么步骤，以及什么时候它们会悄悄出现。素材来自 [github.com/mattpocock/skills](https://github.com/mattpocock/skills)。

## 4.1 核心工程原语：/grilling、/tdd、/code-review、/diagnosing-bugs

这组是框架的"引擎"。第 3 章所有 user-invoked skill 内部驱动的就是它们，理解这组等于理解了整个框架的质量机制。

### 4.1.1 /grilling 盘问原语

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

### 4.1.2 /tdd 测试驱动

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

### 4.1.3 /code-review 双路审查

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

### 4.1.4 /diagnosing-bugs

一句话：`/diagnosing-bugs` 诊断 bug，核心信条是——**90% 的工作在建反馈回路**。

**怎么被触发**：你在对话里报告一个 bug（复现步骤、现象）时，模型自动按它的流程接管诊断。

**典型步骤**：

1. **先建反馈回路**：把「现象可观测、改动可验证」的回路搭起来——能稳定复现、每一步都有输出可对照。反馈回路不通，后面所有推断都不可信。
2. **缩小范围**：沿回路二分定位，逐步排除可疑代码。
3. **验证根因**：做出修复假设后用回路验证「改这里确实解决」，而不是靠猜。

**什么时候它会出现**：当你描述「这个功能坏了、现象是这样」时。注意它出现的前提是你给了足够的现象描述——反馈回路建不起来时，它大概率会反过来先问你要复现步骤。

> [!tip] 报 bug 的姿势
> 想让 `/diagnosing-bugs` 高效，先说清三件事：做了什么、期望什么、实际得到什么。反馈回路的前半段——复现——本来就依赖这些素材。

## 4.2 架构与术语类：/domain-modeling、/codebase-design、/improve-codebase-architecture

这组处理「架构与语言」层面：术语统一、模块划分、架构改进。

### 4.2.1 /domain-modeling 术语敲定

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

### 4.2.2 /codebase-design 深模块词汇表

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

### 4.2.3 /improve-codebase-architecture

一句话：`/improve-codebase-architecture` 霰弹式地给你一份架构改进建议清单。

**怎么被触发**：你问「这个代码库的架构怎么改进」时自动触发。

**典型步骤**：扫描代码库 → 按模块 / 耦合 / 可测性等维度列出改进点 → 给出建议清单。它的特点是不深挖单个问题，而是**广度覆盖**，一口气把所有看得到的问题摆出来。

> [!warning] 别把它并进 grill（Issue #274）
> 社区实测发现，把它加进 grill 流程后，模型会对每个小问题都给出长篇改进建议，把简单盘问拖成话痨 [Issue #274](https://github.com/mattpocock/skills/issues/274)。要架构意见时单独问它、且限定范围（「只看 X 模块」），不要让它常驻盘问流程。

**什么时候它会出现**：当「看看整体架构有什么问题」被提出时。注意它给的是建议清单，不是可直接执行的 spec——真要落地还要回到 `/to-spec`。

## 4.3 决策与研究类：/wayfinder、/research

这组处理「还没到写代码」的工作：做决策、做研究。

### 4.3.1 /wayfinder 拆 Decision ticket

一句话：`/wayfinder` 把一个悬而未决的决策**拆成 Decision ticket**——它的产出是「要做的决策」，不是「要建的代码」。

**怎么被触发**：对话遇到阻碍进展的关键决策点时自动触发。

**典型步骤**：识别阻塞决策 → 列出决策选项与权衡 → 把决策拆成一张可独立处理的 Decision ticket → 记录做出决策所需的信息与验证方式。

**什么时候它会出现**：当「这里得先定个方案才能继续」时。它和 `/to-tickets` 的区别：to-tickets 拆的是实现切片（怎么建），wayfinder 拆的是决策（先定哪个方向）。

> [!note] 决策也是工作单元
> 把「决策」当成一张可跟踪的 ticket，是 wayfinder 的核心思路——决策不该悬在对话里，而该像任务一样被记录、被追踪、被关闭。

### 4.3.2 /research 研究类工作

一句话：`/research` 处理研究类工作：查文档、对比方案、收集证据。

**怎么被触发**：对话需要「先调研一下再定」时自动触发。

**典型步骤**：明确研究问题 → 检索文档 / 代码 / 社区 → 整理证据 → 给出结论或选项对比。

**什么时候它会出现**：当你说「看看有没有更好的方案 / 查一下这个库怎么用」时。它通常发生在 grill 之前——研究是收集事实，盘问是打磨决策，二者互补。

## 4.4 协作与交接类：/prototype、/handoff、/resolving-merge-conflicts

这组负责「临时实验」与「跨会话协作」。

### 4.4.1 /prototype 一次性原型

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

### 4.4.2 /handoff 跨会话交接

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

### 4.4.3 /resolving-merge-conflicts

一句话：`/resolving-merge-conflicts` 解决 git 合并冲突。

**怎么被触发**：合并 / rebase 出现冲突时自动触发。

**典型步骤**：定位冲突文件 → 逐块理解两侧意图 → 结合 spec 决定保留哪边或合并 → 验证冲突解决不破坏行为。

**什么时候它会出现**：多分支并行开发时。它依赖你对「哪个意图是对的」的判断——模型能帮你读代码、比对差异，但最终取舍仍需你确认。

## 本章小结

- 12 个 model-invoked skill 由触发词或上级 skill 自动带出，你几乎不会直接敲它们；触发靠 description 里的 "Use when..." 触发短语。
- 核心工程原语：`/grilling` 一次一问盘问、`/tdd` 红-绿-重构、`/code-review` 双路子代理审查、`/diagnosing-bugs` 先建反馈回路——它们正是第 3 章 `/grill-with-docs`、`/implement` 内部驱动的引擎。
- 架构术语类：`/domain-modeling` 敲定术语写 [[CONTEXT.md]] + [[ADR]]；`/codebase-design` 提供 Module / Interface / Depth / Seam / Adapter 五词与删除测试；`/improve-codebase-architecture` 霰弹式列改进点（别并入 grill，会话痨）。
- 决策研究类：`/wayfinder` 拆 Decision ticket（决策而非构建）；`/research` 处理研究类工作。
- 协作交接类：`/prototype` 一次性原型（LOGIC / UI 两分支）；`/handoff` 写交接文档到系统临时目录；`/resolving-merge-conflicts` 解冲突；`/compact` 已删除，同会话用内置 compact、跨会话用 `/handoff`。
- 与第 3 章的配合是单向委托：user-invoked（`/grill-with-docs`、`/grill-me`、`/implement`）调用 model-invoked，model-invoked 再引用共享参考（`/codebase-design`）。

下一章：配置与定制——这些触发行为其实由 SKILL.md 的 frontmatter 控制，弄懂 CLAUDE.md / [[CONTEXT.md]] / [[ADR]] 的职责，你就能按自己的项目裁剪这套框架。
