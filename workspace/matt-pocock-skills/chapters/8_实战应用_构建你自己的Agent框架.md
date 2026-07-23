# 第 8 章：实战应用 — 构建你自己的 Agent 框架

> 素材引用: 全章综合

---

这是全书的最终章。前 7 章拆解了 Matt Pocock 的设计模式，这章回答这个问题：**你要怎么把这些模式用到自己的 Agent 框架中？**

## 8.1 设计原则清单

从前 7 章提炼出的核心原则：

### 1. Bucketed Curation

**原则**：用目录结构管理发布状态，而非配置文件。

**你的项目**：
```
your-framework/
  skills/
    promoted/       # 已发布、面向用户的技能
    experimental/   # 在试的草稿
    personal/       # 你私人的工具
    deprecated/     # 不再使用
```

**检查**：每个月检查一次 experimental 目录——promote 成熟的，删除没用的，标注废弃的。

### 2. Invocation 二分法

**原则**：User-invoked（付认知负载）vs Model-invoked（付上下文负载）。

**检查**：每个新 skill 跑一遍决策树——
```
需要 Agent 自主触发？→ Model-invoked
其他 skill 需要调用它？→ Model-invoked
否则 → User-invoked
```

### 3. 单一真相源

**原则**：每个含义只在一个权威位置。

**检查**：如果同一个概念在两个 SKILL.md 中出现，提取到 CONTEXT.md 或共享 reference skill。

### 4. 信息层级

**原则**：Skill 内容按"Agent 需要它的紧急程度"分梯级，用 progressive disclosure 保持顶层可读。

**检查**：SKILL.md 超过 100 行？→ 向下推 reference。同一梯级内的相关内容分散了？→ 重新 co-locate。

### 5. Leading Words

**原则**：利用模型预训练中已有的紧凑概念，替代冗长描述。

**检查**：SKILL.md 中是否有 3 个以上同义词描述同一件事？→ 压缩为一个 leading word。有无自创词汇？→ 优先用模型已知的词。

### 6. Completion Criterion

**原则**：每个 step 以可检查且穷尽的完成标准结束。

**检查**：Agent 是否经常跳过关键步骤？→ completion criterion 不够清晰。Agent 是否做了表面工作就停下？→ demand 不够高。

### 7. No-op Test

**原则**：每条指令必须改变 Agent 的默认行为。

**检查**：删除某行后行为不变？→ 它是 no-op，删除它（不是重写它）。

### 8. 调用边界规则

**原则**：User-invoked → Model-invoked → 共享参考，不可逆向。

**检查**：是否有 user-invoked skill 调用另一个 user-invoked？→ 这是架构违规，要么改为 model-invoked，要么通过 router 间接引用。

---

## 8.2 目录结构模板

以下是可以直接用的目录结构模板：

```
your-agent-framework/
│
├── CLAUDE.md              # 宪法：结构规则、调用规则、维护纪律
├── AGENTS.md              # 跨平台契约（与 CLAUDE.md 内容相同）
├── CONTEXT.md             # 词典：核心术语、Avoid 指令、关系模型
├── README.md              # 对外文档：skill 列表与用途
│
├── skills/
│   ├── core/              # [已推广] 稳定的核心技能
│   │   ├── router/SKILL.md
│   │   ├── entry-1/SKILL.md
│   │   └── entry-2/SKILL.md
│   │
│   ├── shared/            # [已推广] 技能引用的共享词汇
│   │   ├── vocabulary/SKILL.md
│   │   └── quality-gates/SKILL.md
│   │
│   ├── experimental/      # [草稿] 在试的技能
│   └── deprecated/        # [废弃] 不再使用
│
├── docs/                  # 对外文档（镜像 core/ 和 shared/）
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

### 目录创建检查清单

- [ ] `CLAUDE.md` 写了吗？包含结构规则和调用规则
- [ ] `CONTEXT.md` 写了吗？即使只有 3-5 个术语
- [ ] 每个 SKILL.md 是否在正确的 bucket 中？
- [ ] `skills/core/` 中的 skill 有对外文档吗？
- [ ] `.agents/adr/` 目录存在吗？
- [ ] `scripts/link-skills.sh` 创建了吗（如果需要本地安装）？

---

## 8.3 你的第一个 Skill

从最简单的一个开始——模仿 grill-me 的"3 行 skill"模式。

### 示例：你的第一个 User-Invoked Skill

```markdown
---
name: your-first-skill
description: A quick sanity check before starting work.
disable-model-invocation: true
---

Run a /grilling session.
```

就这么简单。这个 skill 做了什么？它给了你一个 `/your-first-skill` 的快捷方式，当你想快速验证一个想法时调用它。

### 示例：你的第一个 Model-Invoked Skill

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
   - **Completion**: All context sources collected

2. **Analyze**
   - Compare state against expected norms
   - **Completion**: Deviations identified and documented

## References
- [Framework Rules](CONTEXT.md) — core vocabulary
```

### 扩展策略

从 2-3 个 skill 开始，按以下顺序扩展：

```
阶段 1（第 1 周）
  ├── 1 个 user-invoked entry skill（你的主入口）
  └── 1 个 model-invoked skill（共享逻辑）

阶段 2（第 2-3 周）
  ├── 再增加 1-2 个 user-invoked
  └── 创建 CONTEXT.md（至少 3-5 个术语）

阶段 3（第 4 周以后）
  ├── 达到 5-7 个 user-invoked → 创建 router
  ├── 定期修剪（no-op test）
  └── 记录 ADR（关键决策）
```

---

## 8.4 质量保障 — 自检清单

每个新 skill 创建时，逐项检查：

### 基础（必须通过）

- [ ] **SKILL.md ≤ 100 行**：`wc -l SKILL.md`，超过就修剪或拆分
- [ ] **Frontmatter 完整**：name + description + invocation 设置正确
- [ ] **Description 有触发词**（model-invoked）："Use when...", "mentions..." 等
- [ ] **描述无否定指令**：没有 "不要..."、"Never..."，全部正面表述
- [ ] **有具体示例**：至少一个使用场景或代码示例

### 结构（建议通过）

- [ ] **Completion Criterion 存在**：每个 step 都有可检查的完成标准
- [ ] **术语一致**：没有同义词替换核心术语
- [ ] **引用仅一级深度**：reference 文件的引用文件中不再有引用
- [ ] **无 No-op**：删除每行，确认行为会变化
- [ ] **无时间敏感信息**：无版本号、日期、过时 API 引用

### 维护（定期检查）

- [ ] **Relevance**：每行是否仍然和技能做的事情相关？
- [ ] **Sediment**：是否有夏季沉积的过时内容？
- [ ] **Sprawl**：行数是否在 100 以下？
- [ ] **Duplication**：是否有内容在其他 SKILL.md 中出现？

---

## 8.5 常见陷阱与对策

### 陷阱 1：过早引入太多 Skill

**症状**：第一周就建了 15 个 skill，大部分没用过。

**对策**：从 2-3 个开始。每周最多新增 1 个。skill 多的价值不在于数量，而在于**你实际用它们**。

### 陷阱 2：不维护 CONTEXT.md

**症状**：语汇漂移——一周说 "issue"，下周说 "ticket"，再下周说 "task"。Agent 越来越困惑。

**对策**：建立 CONTEXT.md（至少 3-5 条），严格执行 `_Avoid_` 指令。当发现新的术语歧义时，立即更新。

### 陷阱 3：不做 Pruning

**症状**：沉积——半年后 SKILL.md 里有"参考旧版 API"的指令，Agent 还在执行。

**对策**：每季度做一次全面 pruning。每个 SKILL.md 跑 no-op test。删除比重写更常见。

### 陷阱 4：无视上下文窗口

**症状**：一个会话持续到 15 万 token，Agent 开始"失忆"——忘记之前的决策、重复问同样的问题。

**对策**：设定硬性的上下文管理规则（类似 Matt 的"前 3 步同窗口，每 implement 新会话"）。接近 12 万 token 时主动 handoff。

### 陷阱 5：把 Skill 当 Plugin

**症状**：期望 skill 能做"安装后自动运行的事"——注册钩子、监听事件、自动触发。

**对策**：Skill 是指令集，不是插件。它告诉 Agent 怎么做，但不改变 Agent 的运行方式。如果需要自动行为，了解 Claude Code 的 hooks 或 plugin 机制——但 skill 不负责这个。

---

## 8.6 从 Matt 体系到你的体系 — 模式映射表

| Matt 的模式 | 你的项目中对应什么 | 优先级 |
|------------|-------------------|--------|
| Bucket 目录（engineering/productivity/...） | core / experimental / deprecated | ★★★ 立即 |
| User/Model-invoked 划分 | 入口 skill vs 内部 skill | ★★★ 立即 |
| CONTEXT.md 词汇表 | 项目核心术语 | ★★★ 立即 |
| Completion Criterion | 步骤完成检查 | ★★☆ 第一周 |
| Leading Words | 核心指令词汇 | ★★☆ 第二周 |
| Router（ask-matt） | 多入口时的导航 | ★★☆ >5 个 skill |
| Grilling 三层抽象 | 意图澄清 + 资料收集 | ★☆☆ 按需 |
| Handoff 机制 | 会话恢复 | ★☆☆ 按需 |
| Pruning（no-op test） | 季度维护 | ★☆☆ 季度 |
| ADR（架构决策记录） | 重要决策留档 | ★☆☆ 有决策时 |
| 并行子代理 | 多角度审查 | ★☆☆ 按需 |

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
- 引入 leading words 概念，优化现有 SKILL.md
- 创建 model-invoked 共享 reference skill
- 跑一次全面 no-op test

**每月**：
- Pruning 审查——每个 SKILL.md 过一遍
- 检查沉积/蔓延/重复
- 更新 CONTEXT.md（如有新术语）

**有决策时**：
- 写一个 ADR——记录被拒方案 + 技术原因 + 检查清单

---

## 8.7 全书总结

Matt Pocock Skills 仓库的核心价值不在于某个具体的 skill——无论是 12 行的 grilling 还是 ask-matt 的路由逻辑。它的价值在于**示范了一套用工程纪律驯服 Agent 的方法论**。

贯穿全书的核心思想：

1. **小胜于大**：小于 100 行的 skill 更容易维护、更容易审计、更容易替换
2. **语言即架构**：共享的精准术语比冗长的解释更有价值
3. **边界即纪律**：User/Model 调用边界、事实/决策边界、思考/执行边界——每一条边界都减少了 Agent 的不确定性
4. **修剪胜于添加**：好的 skill 是通过持续删除而非持续增加来塑造的
5. **上下文是货币**：省 token 不是可有可无的优化——它直接决定了 Agent 能在多长时间内保持高质量工作

最后，回到 Matt 那句话：

> "Your skills are the upper limit of what AI can achieve."

你的框架的质量决定了 AI 在你的项目中能发挥的上限。希望这本书能帮你把这个上限推得更高。

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
| Legwork | 幕后工作 | Agent 在一个步骤中做的探索性工作 |
| Context Pointer | 上下文指针 | 命名外部参考的触发条件 |
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
- [ ] Negation: 有"不要..."类的否定指令吗？
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
