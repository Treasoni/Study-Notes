---
name: collect
description: 收集学习资料阶段。调度 collector subagent 搜索官方文档和社区内容，抓取并保存原始资料。触发时机：用户确认学习计划后，Phase 1。
---

# Skill: collect（收集资料）

## 触发时机
用户确认学习计划后。

## 输入
- `topic`: 学习主题
- `direction`: 概念理解 / 实战上手 / 体系梳理 / 问题排查
- `depth`: 入门 / 进阶 / 深入原理

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为调度员，collector subagent 作为执行者。

```
主 Agent (PM)                    Collector Subagent (专员)
    │                                  │
    ├─ 确认可用源 ─────────────────►│
    │                                  ├─ 搜索官方文档
    │                                  ├─ 抓取内容
    │                                  ├─ 搜索社区
    │                                  ├─ 过滤 & 保存
    │◄──── 精简摘要 ─────────────────┤
    │                                  │
    ├─ 展示给用户                      │ (销毁)
```

**核心原则**：主 Agent 不直接执行搜索/抓取，避免上下文污染。

## 执行步骤

### Step 1: 确认可用搜索源

运行 `opencli list -f json` 确认当前可用的搜索源，传递给 collector。

### Step 2: Dispatch Collector Subagent

使用 Agent 工具调度 collector subagent，传入结构化信息：

```typescript
Agent({
  subagent_type: "collector",
  prompt: `
Topic: {topic}
Direction: {direction}
Depth: {depth}
Available Sources: {逗号分隔的可用源列表}
Output Dir: {SYSTEM_ROOT}/0-inbox/{topic}/raw/
  `,
  label: `collect:${topic}`,
  phase: "Phase 1: Collect"
})
```

### Step 3: 展示结果

collector subagent 返回精简摘要后，向用户展示：
- 来源数量（按类型分类）
- 覆盖的子主题
- 明显缺口

### Step 4: 硬停止

**严禁调用 `/curate`。严禁进入 Phase 2。**
必须等待用户明确确认（"继续" / "进入下一阶段" / "开始整理"）后才能进入 curate。

## 禁止行为

- 主 Agent 不要直接执行 opencli 搜索命令（交给 collector）
- 不要跳过 subagent 调度直接手动收集
- 不要编造 URL 或来源信息
