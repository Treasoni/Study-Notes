# Claude Code Subagent 与 Skill 调度机制 - 原始输入

> 收集时间：2026-05-24

## 内容

Claude Code 中的 Subagent 与 Skill 调度机制

1. 核心理念：上下文隔离 (Context Isolation)
在处理复杂项目时，大模型的"上下文窗口（Context Window）"极其宝贵。痛点：长时间的纠错、阅读冗长日志、反复执行测试会产生大量"垃圾信息"，导致主 Agent 变笨、遗忘目标或产生幻觉。解法：使用 Subagent（子代理）。Subagent 的核心使命是处理"脏活累活"，它的运行实例是完全临时（阅后即焚）的。任务完成后，只向主 Agent 返回精简总结，随后立刻销毁，绝不污染主干上下文。

2. Subagent 的两种"身份形态"
虽然 Subagent 跑完就销毁，但它们的身份定义分为两种：
形态 A：临时拉起的 Subagent（"临时工"）
创建方式：通过 /subagent 手动创建，或主 Agent 在对话中根据临时需求随时拉起。
特点：零配置、随口即用。
适用场景：突发性的探路试错（"新建个沙盒跑一下这三个 API，看哪个通"）。
隔离单次长日志查阅（"帮我看看这 3000 行报错说了啥"）。
避免打断主 Agent 当前的连续思考。

形态 B：固化的 Subagent（"专职员工"）
创建方式：在项目根目录 .claude/agents/ 或全局 ~/.claude/agents/ 下编写 Markdown/YAML 配置文件。
特点：拥有固定的职责、系统提示词和严格的权限。
适用场景：流程化、重复性高的标准化任务（如代码审查、跑测试、安全扫描）。

3. 核心区别对比 (临时工 vs 专职员工)
对比维度形态 B：固化的 Subagent (.claude/agents/)形态 A：临时拉起的 Subagent
复用性作为数字资产沉淀，跨会话/跨项目永久可用阅后即焚，不可复用
权限控制极强：物理级隔离，可限制仅拥有 [Read, Grep] 权限弱：通常继承默认全量权限，靠自然语言约束
成本/速度优化支持：可在配置中指定更便宜、更快的模型（如 Haiku）不支持：通常跟随当前主 Agent 的模型行为
稳定性极高，严格遵循预设的 System Prompt 和输出格式依赖主 Agent 临时传话的准确度，容易信息衰减

4. 高阶实践：Skill + 固化 Subagent 的操作员模式 (Operator Pattern)
将 .claude/agents/ 视作"员工名册"，将 Skill 视作"SOP（标准作业程序）"，主 Agent 视作"项目经理"。这能构建出极其强大且安全的自动化工作流。

Step 1: 定义固化 Subagent (员工名册)
在 .claude/agents/ 下创建组件。例如，创建一个只读权限的 Code Reviewer (code-reviewer.md)：
YAML
---
name: code-reviewer
description: 代码审查专家。当需要 Review 代码时调用。
model: claude-3-7-sonnet-20250219
tools: [Read, Grep, Glob] # 限制读权限，防止误删改
---
你是一个严苛的代码审查专家。阅读主 Agent 传给你的代码，挑出逻辑漏洞，直接输出 Review 报告，不得修改代码。

Step 2: 在 Skill 中编排工作流 (SOP)
在 .claude/skills/ 下编写指令，明确指派上述 Subagent：
Markdown
# 自动化重构与审查工作流

执行代码重构时，请严格作为主调度员按以下步骤执行：
1. **你（主 Agent）** 负责分析架构，执行代码重写。
2. 完成后，调用 `code-reviewer` 代理（Agent），把代码路径和修改意图传给它，要求其输出审查意见。
3. 根据 `code-reviewer` 的意见，由你完成最终的代码微调。

关键注意事项 (Best Practices)
做好上下文传递 (Context Passing)：在 Skill 中叮嘱主 Agent，调用 Subagent 时必须把文件路径、当前报错等背景信息交代清楚。
设定退出条件：防止 Subagent 陷入死循环（例如："最多尝试修复 3 次，失败则带回报错终止"）。
