# 第二章：Skills 系统设计 — 可组合的行为约束引擎

## 本章目的

上一章我们看到了 Superpowers 的全貌——14 个技能、6+ 个平台、门控管线。但所有这些能力都建立在同一个核心抽象之上：**SKILL.md**。本章深入这个抽象：技能是什么格式？如何定义、发现和触发？编写技能时最关键的设计原则是什么？

理解 Skills 系统是理解整个 Superpowers 的钥匙——Pipeline 由技能串联，Subagent 由技能驱动，自举由技能注入。

---

## 2.1 什么是 Skill？

在 Superpowers 中，一个 Skill 是一个**行为约束单元**——它不是代码库，不是 API，而是以 Markdown 文档形式定义的 Agent 行为规范。每个 Skill 目录包含一个 `SKILL.md` 文件，Agent 在运行时读取它并按照其中的规则行动。

Skill 与传统的库或函数的区别：

| 维度 | 传统函数/库 | Superpowers Skill |
|------|------------|-------------------|
| 形态 | 可执行代码 | Markdown 文档 |
| 调用方式 | 代码调用（import / require） | 上下文触发（自动或手动） |
| 约束力 | 必须遵守（编译/运行时强制） | 行为约束（硬门控 + 描述触发） |
| 跨平台 | 需分别实现 | 同一文件，仅工具映射不同 |
| 版本管理 | npm / cargo 包管理 | Git 仓库 + 钩子注入 |

### 14 个技能速览

全部技能按类别分为 4 组：

**协作技能（9 个）** — 覆盖从需求到交付的完整开发流程：

| 技能 | 阶段 | 一句话描述 |
|------|------|-----------|
| brainstorming | 需求 | 通过结构化提问澄清需求，输出设计文档到 `docs/superpowers/specs/` |
| writing-plans | 计划 | 将设计分解为 2-5 分钟的原子任务，每步含完整代码 |
| executing-plans | 执行 | 内联执行已有计划（备选路径） |
| subagent-driven-development | 执行 | **旗舰引擎**：每任务派发独立 subagent + 审查 |
| dispatching-parallel-agents | 执行 | 多 subagent 并行处理独立问题域 |
| requesting-code-review | 审查 | 对 diff 进行审查，输出 Critical / Important / Minor |
| receiving-code-review | 审查 | 6 步接收模式：读 → 理解 → 验证 → 评估 → 回应 → 实施 |
| finishing-a-development-branch | 交付 | 测试验证 + 分支完成/合并/PR/丢弃 |
| using-git-worktrees | 环境 | 工作区隔离 + 测试基线验证 |

**测试技能（1 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| test-driven-development | RED-GREEN-REFACTOR 强制，零例外，预判 8 种 Agent 合理化借口 |

**调试技能（2 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| systematic-debugging | 4 阶段根因分析：观察 → 假设 → 验证 → 修复，禁止未调查就修复 |
| verification-before-completion | 修复后验证，确保真的修好了且没有引入新问题 |

**元技能（2 个）：**

| 技能 | 一句话描述 |
|------|-----------|
| using-superpowers | 引导程序 | 每个会话自动注入，声明 1% 规则和技能优先级 |
| writing-skills | 编写新技能的方法论，使用 TDD 驱动文档 |

---

## 2.2 SKILL.md 结构规范

每个技能必须遵循以下结构：

### YAML Frontmatter（必填）

```yaml
---
name: skill-name           # 仅字母、数字、连字符。无括号、无特殊字符
description: Use when...   # 触发条件，不是技能总结
---
```

`name` 要求：
- 仅小写字母、数字和连字符
- 例如：`test-driven-development`，不是 `TDD` 或 `test_driven_development`

`description` 要求：
- 必须以 **"Use when..."** 开头
- 描述**什么情况下触发**，不是技能做什么
- 不超过 1024 字符，尽量保持在 500 以下
- 使用第三人称

### 正文段落（推荐顺序）

```
## 概述（1-2 句核心原则）

## 何时使用
- 症状列表 / use cases
- 小内联流程图（用于非明显的决策点）

## 核心模式
- 对于技术/模式技能：before/after 代码对比
- 说明什么是好的模式，什么是不好的模式

## 快速参考（可选）
- 常用操作表，方便扫描

## 实现细节（可选）
- 简单模式内联
- 繁重内容或可复用工具链接到单独文件

## 常见错误
- 什么会出错 + 如何修复

## 真实世界影响（可选）
- 为何这个技能重要
```

### 三个技能类型

| 类型 | 描述 | 示例 | 特点 |
|------|------|------|------|
| **技术技能** | 有具体步骤的方法 | TDD, systematic-debugging | 步骤清晰，流程明确 |
| **模式技能** | 思考问题的方式 | flatten-with-flags, test-invariants | 范式转换，before/after 对比 |
| **参考技能** | API 语法、工具用法 | 快速参考表 | 表格为主，便于扫描 |

### Token 预算

| 技能类型 | 目标大小 |
|---------|---------|
| 入门工作流 | 每技能 <150 词 |
| 频繁加载的技能 | 总计 <200 词 |
| 其他技能 | <500 词 |

优化策略：
- 将细节移到工具帮助中（"运行 --help 获取详细信息"）
- 使用交叉引用（"必需背景：理解 superpowers:systematic-debugging"）
- 压缩示例，消除冗余

---

## 2.3 自动发现与触发机制

### 发现路径

Claude Code 自动扫描以下路径查找技能：

```
项目 .claude/ 目录下 → 自动发现
用户 ~/.claude/ 目录下 → 用户级技能
插件安装目录 → 通过 plugin.json 注册
```

对于 Superpowers，它作为插件安装后，其 `skills/` 目录被自动扫描。每个 `SKILL.md` 是一个可触发的技能。

### 触发条件

触发完全依赖 `description` 字段。Claude Code 在每次任务前会检查是否有匹配的技能：

```
用户说："帮我写一个 React 组件"
    ↓
模型检查 skills 匹配：
    brainstorming（"Use when building or designing new features..."）→ ✅ 匹配
    test-driven-development（"Use when implementing features..."）→ ✅ 匹配
    ↓
1% 规则触发 → 加载匹配的技能
```

### 关键发现：描述不要总结流程

这是 Superpowers 开发过程中最重要的经验发现之一。

**错误示例**（总结流程）：
```
description: "Use when reviewing code between tasks. Runs spec compliance check
then code quality check, reporting issues by severity."
```

这种描述的问题：Agent 读到 "runs spec compliance check then code quality check" 后，以为已经知道要做什么了，于是**直接按这个描述做了一次审查**——而不是去读完整的 SKILL.md 中的详细流程（那里定义的是**两次**独立审查，由不同的 reviewer prompt 执行）。

**正确示例**（只写触发条件）：
```
description: Use when a task implementation is complete and the changes need
review before being integrated.
```

Agent 读了这个描述会触发"需要加载技能"的判断，然后去读完整的 SKILL.md 来了解具体怎么做。

**规则**：Description 只写何时触发，不写技能做了什么。触发判断由描述驱动，执行细节由正文驱动。

### 技能优先级

当多个技能匹配时，按以下顺序加载：

1. **流程技能优先**（brainstorming, systematic-debugging）—— 它们设定方法
2. **然后实现技能**（frontend-design, mcp-builder 等）—— 它们执行方法

例如："让我们构建一个 React 应用" → 先加载 brainstorming（澄清需求），再加载实现技能。

---

## 2.4 技能的约束力层

理解 Skills 的约束力很重要——不是所有技能都有同等的约束强度：

```
硬门控 ─────────────────► 软参考

强制规则                    建议指导
禁止 + 借口表               最佳实践
红旗列表                    可参考的模板
不可跳过的检查清单           知识参考
```

- **TDD skill** 属于最左端：禁止写代码前没有失败测试，红旗列表预判 Agent 的借口
- **Writing skills** 属于中间：有明确步骤但 Agent 有一定自由度
- **参考技能** 属于最右端：主要是信息性内容

设计自己的 Skill 时，需要根据约束目标选择正确的位置。

---

## 2.5 实战：SKILL.md 模板

以下是一个最小 Skill 模板，基于 Superpowers 规范：

```markdown
---
name: my-custom-skill
description: Use when [触发条件]，不要总结做了什么
---

## 概述

[1-2 句核心原则]

## 何时使用

- [症状 1]
- [症状 2]

## 核心模式

### 好的做法
```code
```

### 不好的做法
```code
```

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| ... | ... | ... |
```

如果你的技能需要强制执行纪律（如"必须先做 A 再做 B"），**不要**只写软性指导（"最好先做 A"），而要使用**禁止 + 借口表**：

```markdown
## 禁止

- ❌ 禁止跳过 [步骤] 因为 [常见借口 1]
- ❌ 禁止用 [借口 2] 来绕过 [步骤]
- ❌ 禁止 [常见变通方法]

如果以上任何一条听起来很熟悉 → 停下来，回到 [步骤]。
```

---

## 本章小结

- Superpowers 的 14 个技能分为协作（9）、测试（1）、调试（2）、元技能（2）四大类
- 每个技能是一个包含 `SKILL.md` 的目录，由 YAML frontmatter（name + description）和结构化正文组成
- 技能通过 `description` 字段自动发现和触发，**描述只写触发条件，不总结流程**
- 总结流程的描述会诱使 Agent 走捷径，不读完整 SKILL.md
- Token 预算策略：入门 <150 词，高频 <200 词，其他 <500 词
- 约束力从"硬门控"到"软参考"是一个光谱，设计技能时要选择正确的位置
- 纪律性技能需要使用"禁止 + 借口表 + 红旗列表"而非软性指导

### 下一章预告

理解了 Skills 系统的基础后，下一章进入 Pipeline 核心：**7 阶段硬门控状态机**，看 Brainstorming → Writing Plans → TDD → Code Review 每个阶段的细节、门控条件和强制机制。
