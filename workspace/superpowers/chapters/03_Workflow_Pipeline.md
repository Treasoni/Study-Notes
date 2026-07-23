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
