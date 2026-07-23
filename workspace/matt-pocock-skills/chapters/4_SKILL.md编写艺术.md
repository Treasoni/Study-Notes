# 第 4 章：SKILL.md 编写艺术

> 素材引用: [R6], [R7], [E4], [E6]
> 核心参考: writing-great-skills/SKILL.md + GLOSSARY.md

---

这是全书最重要的一章。如果说前 3 章是"理解别人的架构"，这一章是**你写出自己的 skill 的工艺手册**。Matt 把这项能力封装为一个 skill（`writing-great-skills`），本文将它展开为系统的指南。

## 4.1 核心美德：可预测性

> "A skill exists to wrangle determinism out of a stochastic system."

这是整个 skill 设计体系的出发点。**可预测性（Predictability）** 不是指每次都产生相同输出（一个发散性头脑风暴 skill 应该每次都发散，这才是可预测的），而是指 Agent 每次运行都遵循**相同的过程**。

换句话说：可预测的 skill = Agent 每次都做同样的事情，至于结果是什么（是 tight 的代码还是发散的创意）取决于 skill 的职责。

### 为什么不是"一致性"或"可靠性"？

GLOSSARY.md 明确禁止这些替代词：

> 不用：consistency, reliability, robustness, output-determinism

因为这些词暗示输出层面的重复性，而非过程层面的重复性。一个发散式头脑风暴 skill 在"输出"层面是随机的，但在"过程"层面（每次都会问同样类型的问题、按同样顺序推进）是可预测的。

### 可预测性是一切设计决策的衡量标准

当你在这个章节中看到任何一个设计模式，都可以问：**这个模式如何增进可预测性？**

- 信息层级 → 减少 Agent 在"该从哪里读"上的随机性
- Completion Criterion → 减少 Agent 在"该不该继续"上的随机性
- Leading Words → 减少 Agent 在"用什么方式思考"上的随机性
- 修剪 → 减少 Agent 在"该执行哪条指令"上的随机性

---

## 4.2 信息层级（Information Hierarchy）

这是 SKILL.md 中最核心的结构设计。内容按"Agent 需要它的紧急程度"分为三个梯级：

```
梯级 1: In-Skill Step          ← 最紧急，Agent 直接执行
   SKILL.md 中的有序动作

梯级 2: In-Skill Reference     ← 按需查阅
   SKILL.md 中的定义、规则、事实

梯级 3: External Reference     ← 仅当 context pointer 触发
   从 SKILL.md 推到独立文件
```

### 梯级 1：步骤（Steps）

Steps 是**有序的动作序列**。当 skill 执行时，Agent 按顺序做这些事。每个 step 以 **completion criterion** 结束（见 4.3 节）。

步骤应该是"顺序依赖"的——第二步依赖第一步的结果。如果各步骤是独立的，那它们不是步骤，而是不同类型的 reference。

**好的步骤**（来自 implement/SKILL.md）：
```markdown
1. Use /tdd where possible, at pre-agreed seams.
2. Run typechecking regularly, single test files regularly.
3. Once done, use /code-review to review the work.
4. Commit your work to the current branch.
```

每一步都清晰、可检查、依赖前一步完成。

### 梯级 2：行内参考（In-Skill Reference）

参考是**定义、规则、事实**，Agent 在需要时查阅。它们不是有序的——专业审阅 skill 的所有审查规则都是对等的。

```
Review Rules:
- Check for naming consistency
- Verify error handling coverage
- Confirm test coverage meets threshold
```

当所有行内参考都是对等的（flat peer-set），这是一个合法的安排，不需要硬塞进步骤里。

### 梯级 3：外部参考（External Reference）

当行内参考太多导致 SKILL.md 膨胀时，把一部分推到外部文件，通过 **context pointer** 链接：

```markdown
See [GLOSSARY.md](GLOSSARY.md) for full definitions.
```

外部参考按需加载——只有当 Agent 觉得需要查阅时才会读取。这节省了 token。

### Progressive Disclosure（渐进式披露）

这是信息层级中最关键的操作：**把细节沿梯级向下推，保持顶层可读**。

什么样的细节该向下推？看是否所有分支都需要它：

- **所有分支都需要** → 留在行内 step/reference
- **仅某些分支需要** → 推到外部 reference，通过 context pointer 按需加载

branching 是最干净的 disclosure 测试——如果你有一个 skill 分为 path A 和 path B，path A 需要的细节就不应该出现在 path B 的 Agent 面前。

### Context Pointer 的措辞

这是极易被忽视但极其重要的细节。Context pointer **的措辞决定触发可靠性**，而非目标文件的内容：

```markdown
# 好的 pointer
See [GLOSSARY.md](GLOSSARY.md) for the meaning of bold terms.

# 差的 pointer
More information is available in the reference file if needed.
```

好的 pointer 明确告诉 Agent 什么情况下该去查阅，差的 pointer 太模糊，Agent 可能忽略。

### Co-location

与 progressive disclosure 相对的原则：**处于同一梯级的相关内容应该放在一起，不分散。**

```
# 好的 co-location
## Error Handling
- All functions must return Result types
- Network errors should be retried 3 times
- Timeout after 30 seconds

# 差的散落
## Section A
- All functions must return Result types

## Section B (50 行后)
- Network errors should be retried 3 times
```

Co-location 与 progressive disclosure 不是矛盾的——前者关注同一梯级内的组织，后者关注梯级间的分配。

---

## 4.3 Completion Criterion（完成标准）

每个 step 都必须有一个完成标准——告诉 Agent "这一步做完了"的条件。这是防止 Agent **过早完成**（premature completion）的第一道防线。

### 完成标准的两个维度

**Clarity（清晰度）**：Agent 能否明确判断完成与否？

```
# 清晰（好的）
"All modified models accounted for in the migration doc"
  ↓ Agent 可以逐项检查

# 模糊（差的）
"Understanding reached"
  ↓ Agent 可以声称"我理解了"然后跳到下一步
```

**Demand（要求度）**：完成标准需要 Agent 做多少 Legwork？

```
# 高 demand（好的）
"Every error path covered by a test case"
  ↓ Agent 必须穷尽所有路径

# 低 demand（差的）
"Write tests for the main feature"
  ↓ Agent 只写最明显的测试
```

最强的完成标准是**既可检查又穷尽**。可检查保证 Agent 知道该不该停，穷尽保证它停下来时工作确实完成了。

### Completion Criterion 也适用于纯参考型 Skill

这是一个重要的洞察。即使是没有步骤的纯参考型 skill（如 code-review 只有审查规则），也需要一个完成标准来确保 Agent 覆盖了所有规则。否则 Agent 可能只检查了前 3 条规则就宣布完成。

---

## 4.4 Leading Words（引导词）

这是 Matt 体系中最巧妙的设计。**Leading word** 是一个"已经存在于模型预训练中的紧凑概念"，Agent 用它来思考。

### 原理

假设你写了一行："Be thorough in your code review." Agent 可能（也可能不）严格执行。但如果你写："Conduct a **relentless** code review."——`relentless` 是模型预训练中已经携带的行为描述，Merriam-Webster 式的定义"不放弃"意味着 Agent 会更严格。

关键洞察：**leading word 调用的是模型已有的先验知识，不需要你重新解释。**

### 双倍效果

Leading word 在两个地方生效：

1. **Body 中→锚定执行**：每次出现，Agent 都用同样的方式思考
2. **Description 中→锚定调用**：当你的 prompt、docs、代码库中使用同一个词时，Agent 更可靠地触发对应的 skill

### 实用的 Leading Words

| 好的 Leading Word | 替代的冗长描述 |
|---|---|
| `tight` | "fast, deterministic, low-overhead" |
| `red` | "a loop you believe in"（把模糊门禁转为二值状态） |
| `lesson` | "a reusable insight from experience" |
| `fog of war` | "decisions that depend on other decisions" |
| `tracer bullet` | "a thin end-to-end slice that validates the approach" |

### 如何发现 Leading Word 机会

一个好的练习：检查 SKILL.md 中是否有 "一组近义词描述同一个概念" 的现象。

```markdown
# 发现：三个词描述同一件事
"Run typechecking regularly, single test files regularly,
and the full test suite once at the end."

# 如果这里有一个 leading word 如 "tight loop"
# 可以压缩为：
"Keep a tight loop: typecheck, test, repeat."
```

Leading word 的双赢：更少 token + 更精确的 Agent 行为锚定。

### 自制 Leading Word 的陷阱

> "Coining your own works if you define it clearly, but a made-up word recruits no priors — you pay in definition tokens what a pretrained word gives free."

如果你编一个新词（如 `zigzag-iteration`），你需要花 token 解释它的含义——抵消了 leading word 的优势。优先从模型的预训练词汇中寻找。

---

## 4.5 修剪原则

SKILL.md 需要持续修剪，就像代码需要重构。

### Single Source of Truth（单一真相源）

每个含义只在一个权威位置。如果一个概念（如"什么是 deep module"）出现在 codebase-design 中又出现在 tdd 中，修改时需要在两处同步，容易产生不一致。

**测试方法**：如果你发现一个概念在多个 SKILL.md 中出现，考虑把它提取到共享的 model-invoked reference skill 中，或在 CONTEXT.md 中定义。

### Relevance（相关性）

每行问一个问题："这一行是否还与 skill 的核心职能有关？"

相关性会随时间衰退：
- 新 API 版本发布 → 旧示例过时
- 工作流变化 → 旧步骤不适用
- 其他 skill 合并 → 职责重叠

**测试方法**：逐行运行。如果一行内容不再相关，删除它。不要改为"不那么相关"——要么相关，要么删除。

### No-Op Test（空操作测试）

> "Does it change behavior versus the default?"

这是最强大的修剪工具。如果一个指令被移除后 Agent 的行为不变，那它就是 no-op。付出 token，没有回报。

常见的 no-op 陷阱：

```markdown
# No-op（Agent 本来就会这么做）
"Write clean, well-structured code."

# 非 no-op（明确了具体方向）
"Prefer small, focused modules over large utility files."
```

**重要**：No-op 不是"坏指令"——它只是在当前模型上不生效。换一个模型可能就不是 no-op。所以 no-op 的裁决是模型相对的。

**更微妙的情况**：一个 leading word 太弱也会变成 no-op。

```
# No-op（"thorough" 不够强，Agent 本来就会比较 thorough）
"Be thorough in your testing."

# 非 no-op（"relentless" 更强，改变了行为）
"Be relentless in your testing: every edge case documented."
```

---

## 4.6 六种失败模式

这是 GLOSSARY.md 中定义的六种失败模式，每种都有明确的定义、识别信号和修复方案。

### 1. Premature Completion（过早完成）

**定义**：Agent 在步骤未真正完成时提前结束，注意力从"做工作"滑向"结束工作"。

**识别信号**：Agent 生成看起来完整但实际上遗漏了细节的输出。

**修复步骤**（按顺序尝试）：
1. 先强化 completion criterion（最便宜、最本地化的方案）
2. 只有当 completion criterion 无法明确化且确实观察到 rush 时，才隐藏后续步骤（通过 sequence split）

### 2. Duplication（重复）

**定义**：同一含义出现在多个位置。

**识别信号**：不同 SKILL.md 中有相似的段落，或同一 SKILL.md 中有重复的指令。

**修复方案**：归并到单一真相源。如果多个 skill 共享同一个术语定义，把它放到 CONTEXT.md 或共享 reference skill 中。

### 3. Sediment（沉积）

**定义**：过时内容在 skill 中沉淀积累，因为"增加是安全的，删除是有风险的"。

**识别信号**：SKILL.md 中存在多年未更新的段落、引用已废弃的 API、描述已经不存在的流程。

**修复方案**：定期修剪纪律——设定每月/每季度的 review 周期。

### 4. Sprawl（蔓延）

**定义**：SKILL.md 长度失控。蔓延不同于沉积（蔓延是即使每行都是活跃且独特的，文件也过长）。

**识别信号**：SKILL.md 超过 100 行——即使每行都有用。

**修复方案**：使用信息层级——把 reference 推到外部文件，按 branch 或 sequence 拆分。

### 5. No-Op（无效指令）

**定义**：指令不改变 Agent 的默认行为。

**识别信号**：删除某行后 Agent 行为不变。

**修复方案**：删除（不是重写——大多数 no-op 不值得救）。如果是一个弱的 leading word，换更强的。

### 6. Negation（否定陷阱）

**定义**：通过禁止来引导行为——"不要想大象"，大象反而在 Agent 的注意力中更突出。

**识别信号**：SKILL.md 含有 "不要"、"Never"、"Avoid" 开头的指令，且这些指令没有对应的正面替代。

**修复方案**：用正面描述替代。只在不法用正面表述的硬性护栏上保留否定，并且一定配上"应该做什么"的正面指引。

```
# 否定（差）
"Never write verbose comments."

# 正面（好）
"Write one-line comments that explain why, not what."
```

---

## 4.7 质量关卡（社区实践经验）

基于 Matt 的方法论，社区衍生出六项强制质量关卡。每创建一个新 SKILL.md，应该用这个列表自检：

| # | 关卡 | 检查方法 | 说明 |
|---|------|---------|------|
| 1 | **Description 含触发词** | 是否包含 "Use when..." / "mentions..." | model-invoked 必检，user-invoked 可选 |
| 2 | **SKILL.md ≤ 100 行** | `wc -l SKILL.md` | 超过 100 行意味着需要修剪或拆分 |
| 3 | **无时间敏感信息** | 检查版本号、日期、过时 API 引用 | 否则需要频繁维护 |
| 4 | **术语一致** | grep 检查是否有同义词替代核心术语 | 同一概念始终用同一词汇 |
| 5 | **含具体示例** | 检查是否有代码示例或使用场景 | 防 Agent 幻觉 |
| 6 | **引用仅一级深度** | 检查 reference 文件是否再有 reference | 深层嵌套导致 Agent 放弃查阅 |

### 使用建议

- 新 skill 的前三个版本都应该逐项检查
- 后续版本至少检查 2、4、6（行数、术语、引用深度）
- 如果某个 skill 频繁出现质量问题，优先检查 3 和 5（时效性和示例）

---

## 4.8 代码示例：高质量的 SKILL.md 模板

以下是结合上述原则的 SKILL.md 模板。它不是一个"完美示范"，而是可以直接填入内容的框架：

```markdown
---
name: my-skill
description: >-
  Use when [触发场景 1], [触发场景 2], or [触发场景 3].
  [Leading word 放在描述开头，增强调用锚定]
disable-model-invocation: true    # 或省略 = model-invoked
argument-hint: "[参数说明]"       # 可选，仅 user-invoked
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

> 技巧：如果第二步会导致 Agent 提前完成第一步，考虑把第二步拆到独立 skill。

## Rules

- **[关键规则 1]**: [清晰定义，含具体示例]
- **[关键规则 2]**: [清晰定义]
- **正面表述**所有规则，无否定指令

## Reference

See [GLOSSARY.md](GLOSSARY.md) for core vocabulary.
See [DEEPENING.md](DEEPENING.md) for advanced scenarios.
```

### 模板使用原则

1. **行数**：30-50 行是理想区间。如果在 100 行内写不下，说明该拆分了。
2. **Frontmatter**：description 是 user-invoked（一行摘要）还是 model-invoked（含触发词）决定了一半的调用体验。
3. **Steps**：只有在顺序依赖时才使用 steps，否则用 rules。
4. **Completion Criterion**：每个 step 必须有。习惯了这个节奏后，你看到没有 completion criterion 的 step 会感觉不完整。
5. **Reference**：`GLOSSARY.md` 是 progressive disclosure 的经典形式。一个 skill 可以没有 GLOSSARY.md，但最好至少有外部的引用链接。

---

## 本章要点

1. **可预测性**是核心美德——不是相同输出，而是相同过程
2. **信息层级**：步骤 > 行内参考 > 外部参考，用 progressive disclosure 保持顶层可读
3. **Completion Criterion**：每个 step 必须有可检查且穷尽的完成标准
4. **Leading Words**：借用模型先验的紧凑概念，比冗长描述更省 token 更精确
5. **修剪**：单一真相源 + 相关性 + No-Op 测试——假设每行都是垃圾，除非证明它有价值
6. **六种失败模式**是诊断语言——遇到质量问题时使用，而不是瞎猜"哪里不对"
7. **质量关卡**：新 skill 自检，维护期抽检

> **对你自建框架的启示**：第 8 章会提供一份完整自检清单，但这六个关卡和模板可以从你创建第一个 skill 就开始用。不要等到 skill 数量多了再"规范化"——从第一个 skill 就建立质量标准，未来的自己会感谢现在的你。

> **下一章**：对话边界澄清的实践——Socratic Sparring 的三层抽象。
