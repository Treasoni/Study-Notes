---
created: 2026-05-12
updated: 2026-05-12
type: experience
topic: Claude Code 工作流遵守
tags:
  - AI工程
  - ClaudeCode
  - 工作流
  - PromptDrift
  - 经验总结
sources:
  - 个人经验
  - AI辅助分析
---

# Claude Code 工作流遵守问题与解决方案

## 问题描述

在使用 Claude Code 执行多阶段工作流时，模型有时会跳过人工确认环节，直接推进到下一步。

> [!note] 这不是架构问题
> 这是 LLM 底层的 "Prompt Drift"（提示词漂移）现象，是大语言模型的固有特性。

## 根本原因

| 原因 | 解释 |
|------|------|
| **LLM 是概率预测机，不是状态机** | 大模型通过预测下一个词生成内容。当它觉得上下文足够完成目标时，会直接"顺滑"地冲到最终结果，跳过中间的暂停点 |
| **上下文稀释** | 长对话中，早期指令（如 "Pause here"）的权重被新内容稀释，模型注意力集中在近期抓取的知识上 |

## 三道防线

### 第一道：否定约束（Negative Constraints）

将温和提示改为绝对否定句：

> [!warning] 关键约束
> ```markdown
> 🛑 **CRITICAL WORKFLOW CONSTRAINT**:
> After presenting the summary/draft, YOU MUST STOP GENERATING.
> ABSOLUTELY DO NOT proceed to the next Phase.
> You must wait for the user to type an explicit approval command.
> ```

> [!tip] 原理
> 大模型对否定句的服从度远高于肯定句。

### 第二道：状态播报（State Broadcasting）

在每个 phase 边界强制显式打印状态框：

```markdown
---
📍 **Current Phase**: Phase 2 Curate
⏳ **Status**: PAUSED. Waiting for user approval.
⏭️ **Next Phase**: Phase 3 Write (LOCKED until user confirms)
---
```

> [!tip] 原理
> 模型在生成这段文本时，实际上是在对自己进行心理暗示，强化"暂停"状态。

### 第三道：技能级硬停止（Skill-Level Hard Stops）

在每个技能的 SKILL.md 最后一行加入刹车指令：

> [!quote] 刹车指令模板
> "任务完成。请向用户展示结果并询问确认。收到用户确认前，严禁调用下一步技能。"

> [!tip] 原理
> 每次调用技能时重新读取刹车指令，确保防线不因上下文稀释而失效。

## 总结

> [!abstract] 核心要点
> Prompt Drift 是 LLM 的固有特性，无法根除，只能通过多层防御来缓解。三道防线从不同层级（全局规则、phase 边界、技能内部）构建约束，叠加使用效果最佳。

## 相关概念

- [[Prompt Drift]]
- [[LLM 状态机]]
- [[上下文稀释]]

---

*来源: 个人经验 + AI 辅助分析*
