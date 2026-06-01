---
name: curate
description: 整理学习资料阶段。调度 curator subagent 遍历所有原始资料，按权威性/时效性/完整性/可读性打分，去重，分类归入核心概念/实战示例/进阶原理，标记信息缺口。触发时机：用户审核通过 collect 产出后，Phase 2。
---

# Skill: curate（整理资料）

## 触发时机
用户审核通过 collect 产出后。

## 输入
`{SYSTEM_ROOT}/0-inbox/{topic}/` 中的所有原始资料。

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为调度员，curator subagent 作为执行者。

```
主 Agent (PM)                    Curator Subagent (专员)
    │                                  │
    ├─ 确认输入目录 ────────────────►│
    │                                  ├─ 遍历 raw/ 所有文件
    │                                  ├─ 四维度打分
    │                                  ├─ 去重 & 分类
    │                                  ├─ 标记信息缺口
    │                                  ├─ 写入 5 个 curated 文件
    │◄──── 整理结果摘要 ──────────────┤
    │                                  │
    ├─ 展示给用户                      │ (销毁)
```

**核心原则**：主 Agent 不直接读取 raw 文件内容，避免上下文污染。

## 执行步骤

### Step 1: 确认输入目录

验证 `{SYSTEM_ROOT}/0-inbox/{topic}/raw/` 存在且有文件。

### Step 2: Dispatch Curator Subagent

使用 Agent 工具调度 curator subagent：

```typescript
Agent({
  subagent_type: "curator",
  prompt: `
Topic: {topic}
Input Dir: {SYSTEM_ROOT}/0-inbox/{topic}/raw/
Sources File: {SYSTEM_ROOT}/0-inbox/{topic}/sources.md
Output Dir: {SYSTEM_ROOT}/1-curated/{topic}/
  `,
  label: `curate:${topic}`,
  phase: "Phase 2: Curate"
})
```

### Step 3: 展示结果

curator subagent 返回摘要后，向用户展示：
- 知识地图概览
- 舍弃的资料及原因
- 信息缺口

### Step 4: 硬停止

**严禁调用 `/write`。严禁进入 Phase 3。**
必须等待用户明确确认后才能进入 write。

## 禁止行为

- 主 Agent 不要直接读取 raw/ 目录下的文件内容（交给 curator）
- 不要跳过 subagent 调度手动整理
