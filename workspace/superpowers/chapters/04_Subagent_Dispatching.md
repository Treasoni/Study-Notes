# 第四章：Subagent Dispatching — 子 Agent 派发与审查引擎

## 本章目的

Pipeline 定义了"做什么"，Subagent Dispatching 是"怎么做"。这是 Superpowers 的执行引擎核心——每个任务派发一个全新的 subagent，隔离上下文，执行完毕后由只读审查者把关。本章详解派发流程、状态协议、模型分层、审查机制和并行派发模式。

---

## 4.1 核心模式

### SDD 概述

Subagent-Driven-Development（SDD）是 Superpowers 的旗舰执行模式。核心思想：

> 每个任务派发一个新鲜的 subagent + 隔离上下文 + 强制两阶段审查 = 高质量、快迭代

对比传统在一个会话中顺序执行所有任务：

| 维度 | 内联执行 | Subagent-Driven Development |
|------|---------|---------------------------|
| 上下文 | 累积，越来越重 | 每个 subagent 新鲜 |
| 注意力 | 长会话后质量下降 | 每次都专注 |
| 审查 | 自审（偏见） | 独立审查者（客观） |
| 隔离 | 无 | Git Worktree + 上下文隔离 |
| 恢复 | 会话中断全丢 | 进度账本支持恢复 |

### 完整派发流程

```
Controller（主 Agent，编排者）
    │
    ├─ [准备] scripts/task-brief PLAN_FILE N
    │       提取任务 N 到独立文件 task-N-brief.md
    │
    ├─ [组装] Dispatch 消息：
    │   ├─ 1 行项目上下文定位
    │   ├─ brief 文件路径（需求唯一来源）
    │   ├─ 上游任务产出的接口/决策
    │   ├─ Controller 发现的歧义处理
    │   └─ report 文件路径
    │   └─ 指定模型（Haiku / Sonnet / Opus）
    │
    ├─ [派发] → Implementer Subagent
    │            │
    │            ├─ DONE               → 生成 review package → 派发 reviewer
    │            ├─ DONE_WITH_CONCERNS → 先阅读 concerns
    │            ├─ NEEDS_CONTEXT      → 补充信息，重新派发
    │            └─ BLOCKED            → 评估原因，分层处理
    │
    ├─ [审查] → Reviewer Subagent（只读）
    │            ├─ 输出：Strengths + Issues（Critical/Important/Minor）
    │            └─ 两种判定：Spec Compliance + Code Quality
    │
    └─ [修复] → Fix Subagent（如果发现问题）
                 ├─ 所有 Critical + Important 打包给一个 fix subagent
                 └─ 修复后重新派发 reviewer
```

---

## 4.2 派发细节

### Context 隔离原则

Subagent 不应继承 Controller 的任何上下文或历史。Controller 精确构造 subagent 需要的全部信息：

```
✅ 正确的做法：
  - 把任务需求写到 brief 文件，subagent 读文件
  - 把 diff 写到 review-package 文件，reviewer 读文件
  - 一个 dispatch 描述一个任务，不是整个会话的历史

❌ 错误的做法：
  - 让 subagent 读整个 plan 文件（包含其他任务的上下文）
  - 在 dispatch 中粘贴之前任务的摘要
  - 在同一 dispatch 中包含多个任务
```

### 任务切割原则

一个 task 应该是"最小可独立测试、值得独立审查的单元"。典型的标准：

- 每步 2-5 分钟
- 每步产出可测试的增量
- 步骤之间**不共享运行时状态**
- 如果两个步骤锁同一个文件 → 应该合并

### 模型选择策略

| 模型 | 用途 | 成本特征 |
|------|------|---------|
| **Haiku** | 机械性任务：转写、搜索、简单的 1-2 文件实现 | 最便宜，适合高吞吐 |
| **Sonnet** | 多文件集成、审查者角色 | 性价比最高，默认选择 |
| **Opus** | 架构决策、最终整分支审查 | 最贵，仅在关键节点使用 |

**规则**：每次派发必须显式指定模型。省略会默认使用会话模型（通常是最贵的），导致不必要的成本。

---

## 4.3 状态报告协议

Implementer 返回四种状态之一：

### DONE（完成）

任务完成。Controller 生成 review package 并派发 reviewer。

处理流程：
1. 获取 BASE_SHA（派发前记录的 commit）和 HEAD_SHA
2. 运行 `scripts/review-package BASE HEAD` → 产生 diff 文件
3. 派发 reviewer（使用 task-reviewer-prompt，不是 code-reviewer）
4. Reviewer 返回发现 → 如果有 Critical/Important → 派发一个 fix subagent

### DONE_WITH_CONCERNS（完成但有关注点）

Implementer 对某些决策有担忧。Controller 先阅读 concerns：

- **正确性疑虑** → 先验证和解决
- **观察性备注** → 记录在进度账本中，后续处理

### NEEDS_CONTEXT（需要上下文）

Implementer 发现信息不足以完成任务。Controller 补充信息后重新派发（可考虑升级模型）。

### BLOCKED（阻塞）

Implementer 无法继续。Controller 需要分类处理：

| 阻塞原因 | 处理方式 |
|---------|---------|
| **上下文缺口** | 补充上下文后用同一模型重新派发 |
| **推理缺口** | 升级到更强模型重新派发 |
| **任务太大** | 拆分成更小的任务重新派发 |
| **计划错误** | 上报人类，暂停进度 |

**规则**：不得忽略上报，不得在无变化时强制重试。

---

## 4.4 审查机制

### v5 → v6 演进

| 版本 | 审查方式 | 特点 |
|------|---------|------|
| v5 | 每个任务后两次独立审查 | Spec 合规 + 代码质量分别由不同 prompt 执行 |
| v6 | 一次 diff 通读，两个判定 | 合并为一个 task-reviewer-prompt，减少 token 消耗 50% |

v6 还增加了：
- **预飞行计划冲突检查**：派发前检查任务是否与已有工作冲突
- **文件传递 diff**：审查材料通过文件传递，不粘贴到上下文中
- **最终整分支审查**：所有任务完成后，用最强模型做一次全量审查

### 审查者限制

- **只读**：只能使用 Read、Grep、Glob、LS 等工具
- **不能修改代码**：审查者看到问题只能报告，不能直接改
- **不能跳过发现**：不能被说服或诱导忽略问题
- **隔离 diff**：审查者只看当前任务的 diff，不看整个会话历史

### 四级发现报告

| 级别 | 含义 | 处理 |
|------|------|------|
| Critical | 功能错误、安全问题 | 阻塞进度，必须修复 |
| Important | 代码质量问题 | 必须修复 |
| Minor | 风格命名等 | 记录，最终审查时处理 |
| 计划冲突 | 与计划文本矛盾 | 上报人类决策 |

多个 Critical/Important 发现 → **打包给一个 fix subagent**（不是每个发现一个）。

### 最终整分支审查

所有任务通过后，使用 `requesting-code-review` skill 的 `code-reviewer.md` 做全量审查：

```
Controller → 派发 code-reviewer → 输出全部分级发现
    │
    └─ 有发现 → 打包给一个 fix subagent → 修复 → 重新运行测试
    └─ 无发现 → 进入 Finishing Branch 阶段
```

---

## 4.5 持久化进度账本

SDD 使用 `.superpowers/sdd/progress.md` 文件持久化记录进度，支持**会话中断恢复**：

```
Task 1: complete (commits a1b2c3..d4e5f6, review clean)
Task 2: complete (commits f6g7h8..i9j0k1, review clean)
Task 3: in_progress (brief created, implementer dispatched)
```

恢复时：
1. 检查进度账本
2. 用 `git log` 验证 commit 范围
3. 已完成的跳过，未完成的继续
4. **不依赖内存**

---

## 4.6 Parallel Agent Dispatching（并行派发）

### 适用场景

SDD 的任务是**顺序执行**的。Parallel Dispatching 是另一个 skill，处理**可以同时进行**的独立问题：

- 3+ 个测试文件因不同根因失败
- 多个独立子系统需要同时修改
- 各子问题可以不用彼此上下文就理解

### 不适用场景

- 问题之间有共享状态
- 需要全系统上下文才能理解
- 探索性调试（尚不知问题是否独立）
- 多个 agent 会编辑同一文件

### 执行模式

```
Controller → 在单个响应中派发多个 subagent
    │
    ├─ Subagent 1: 处理子系统 A（scope: src/a/）
    ├─ Subagent 2: 处理子系统 B（scope: src/b/）
    └─ Subagent 3: 处理子系统 C（scope: src/c/）
    │
    全部返回后：
    ├─ 汇总每个 subagent 的发现
    ├─ 检查文件冲突（是否编辑了同一文件）
    ├─ 运行完整测试套件
    └─ 人工抽查系统性错误
```

### 与 SDD 的对比

| 维度 | SDD | Parallel Dispatching |
|------|-----|---------------------|
| 任务关系 | 顺序依赖 | 独立并发 |
| 上下文隔离 | 每个任务隔离 | 每个问题域隔离 |
| 同步机制 | Controller 顺序等待 | 无，完成后汇总 |
| 审查 | 每任务 + 最终 | 汇总后一次 |
| 使用场景 | 功能开发 | 多路调试/独立修复 |

---

## 4.7 实际案例：Builder.io 告警守护进程

Builder.io 团队用 SDD 构建了一个无状态告警守护进程（Go 语言），以下是关键数据：

| 指标 | 值 |
|------|-----|
| Brainstorming 产出 | 424 行规范文档 |
| 锁定的关键决策 | 3 个（冷却机制、通知器设计、互斥语义） |
| 计划覆盖 | 17 个文件，26 个任务 |
| 审查捕获 | 1 个命名不一致（审查发现了 BenchmarkEngineSwap vs EngineReinit） |
| 环境相关问题 | 10 个额外修复提交（BSD date, PID 等） |
| 最终测试 | 100 个延迟样本全部通过 |

案例教训：
1. **环境问题无法规划**——平台特定问题需要跳出工作流单独处理
2. **计划继承 spec 的错误**——配置解析器格式规范写错，导致所有基准脚本都错了
3. **三条不可妥协规则**：规范是唯一真理、先测试再代码、完成一项勾掉一项

---

## 本章小结

- SDD 是 Superpowers 的执行引擎：每任务派发全新 subagent + 隔离上下文 + 强制审查
- 四种状态报告（DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED）驱动执行流程
- 模型分层：Haiku（机械）→ Sonnet（默认）→ Opus（架构/最终审查）
- 审查者只读，输出 Critical / Important / Minor / 计划冲突四级发现
- v6 合并两阶段审查为一次 diff 通读，token 消耗减半
- 持久化进度账本支持会话中断恢复
- Parallel Dispatching 处理独立并发问题，与 SDD 互补

### 下一章预告

执行引擎需要环境保障。下一章看看 **Git Worktree 隔离**——如何在写任何代码前创建隔离工作区、验证测试基线，以及已知问题和规避方案。
