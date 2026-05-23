---
title: Claude Code Subagent 与 Skill 调度机制
tags:
  - claude-code
  - subagent
  - skill
  - 工作流编排
created: 2026-05-24
source: 个人经验
---

# Claude Code Subagent 与 Skill 调度机制

## 背景

在使用 Claude Code 处理复杂项目时，我发现上下文窗口（Context Window）是一个关键瓶颈。长时间的纠错、阅读冗长日志、反复执行测试会产生大量"垃圾信息"，导致主 Agent 变笨、遗忘目标或产生幻觉。

经过实践，我总结出一套 Subagent 与 Skill 的调度机制来解决这个问题。

---

## 核心理念：上下文隔离

Subagent 的核心使命是处理"脏活累活"。它的运行实例是完全临时（阅后即焚）的：

- **任务完成后** → 只向主 Agent 返回精简总结
- **随后立刻销毁** → 绝不污染主干上下文
- **主 Agent 保持清醒** → 专注于核心任务

---

## Subagent 的两种形态

### 形态 A：临时 Subagent（"临时工"）

**创建方式**：
- 命令行：`/agents` 手动创建
- 主 Agent 根据临时需求随时拉起

**特点**：
- 零配置、随口即用
- 通常继承默认全量权限

**适用场景**：
- 突发性的探路试错（如"新建个沙盒跑一下这三个 API"）
- 隔离单次长日志查阅（如"帮我看看这 3000 行报错说了啥"）
- 避免打断主 Agent 当前的连续思考

### 形态 B：固化 Subagent（"专职员工"）

**创建方式**：在项目根目录 `.claude/agents/` 或全局 `~/.claude/agents/` 下编写 Markdown/YAML 配置文件

**特点**：
- 拥有固定的职责、系统提示词和严格的权限
- 跨会话/跨项目永久可用

**适用场景**：
- 流程化、重复性高的标准化任务
- 代码审查、跑测试、安全扫描

---

## 核心对比

| 对比维度 | 固化 Subagent | 临时 Subagent |
|---------|---------------|---------------|
| **复用性** | 跨会话/跨项目永久可用 | 阅后即焚，不可复用 |
| **权限控制** | 物理级隔离，可限制仅 `[Read, Grep]` | 继承默认全量权限 |
| **成本优化** | 可指定 Haiku 等低成本模型 | 跟随主 Agent 模型 |
| **稳定性** | 严格遵循预设 System Prompt | 依赖临时传话准确度 |

---

## 高阶实践：Operator Pattern

把整个系统想象成一个团队：
- `.claude/agents/` → **员工名册**
- Skill → **SOP（标准作业程序）**
- 主 Agent → **项目经理**

### Step 1: 定义固化 Subagent

```yaml
---
name: code-reviewer
description: 代码审查专家。当需要 Review 代码时调用。
model: sonnet
tools: Read, Grep, Glob
---

你是一个严苛的代码审查专家。阅读主 Agent 传给你的代码，
挑出逻辑漏洞，直接输出 Review 报告，不得修改代码。
```

### Step 2: 在 Skill 中编排工作流

```markdown
# 自动化重构与审查工作流

执行代码重构时，请严格作为主调度员按以下步骤执行：

1. **你（主 Agent）** 负责分析架构，执行代码重写。
2. 完成后，调用 `code-reviewer` 代理（Agent），把代码路径和修改意图传给它，要求其输出审查意见。
3. 根据 `code-reviewer` 的意见，由你完成最终的代码微调。
```

---

## Best Practices

### 1. 做好上下文传递

调用 Subagent 时必须把文件路径、当前报错等背景信息交代清楚。避免信息衰减导致 Subagent 输出不准确。

### 2. 设定退出条件

防止 Subagent 陷入死循环。例如：
> "最多尝试修复 3 次，失败则带回报错终止"

### 3. 善用固化 Subagent 的工具限制

```yaml
tools: Read, Grep, Glob  # 不给 Write/Edit，防止误删改
```

---

## 踩坑记录

1. **不要用 `/subagent`**：Claude Code 的命令是 `/agents`，不是 `/subagent`
2. **tools 字段用逗号分隔**：正确格式是 `tools: Read, Grep, Glob`，不是数组格式
3. **model 用别名**：用 `sonnet`/`haiku`/`opus`，不要用完整模型 ID

---

## 来源

[来源: 个人经验]

经官方文档核实：
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents.md)
- [Tools reference - Claude Code Docs](https://code.claude.com/docs/en/tools-reference.md)

---

## 思考题

1. **在什么场景下，临时 Subagent 比固化 Subagent 更合适？**

2. **如果一个任务需要 Subagent 多次调用才能完成，你会如何设计退出条件和重试机制？**

3. **固化 Subagent 的"物理级权限隔离"具体是如何实现的？**

4. **Operator Pattern 中，主 Agent、Subagent、Skill 三者的职责边界应该如何划分？**

5. **对于团队协作场景，如何设计跨项目的固化 Subagent 共享机制？**
