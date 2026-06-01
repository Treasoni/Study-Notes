---
name: write
description: 写笔记阶段。调度 writer subagent 根据整理好的资料和笔记类型，选择模板，提取关键信息，用学习者友好的语言生成笔记初稿。触发时机：用户审核通过 curate 产出后（研究驱动型），或用户审核通过 review 产出后（心得笔记），Phase 3。
---

# Skill: write（写笔记）

## 触发时机
- 研究驱动型笔记：用户审核通过 curate 产出后
- 心得笔记：用户审核通过 review 产出后

## 输入
- `{SYSTEM_ROOT}/1-curated/{topic}/` 中整理好的资料
- 用户偏好的笔记类型：concept / practice / compare / cheat-sheet / experience

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为调度员，writer subagent 作为执行者。

```
主 Agent (PM)                    Writer Subagent (专员)
    │                                  │
    ├─ 传递笔记类型 + 路径 ─────────►│
    │                                  ├─ 选择模板
    │                                  ├─ 读取 curated 资料
    │                                  ├─ 填充模板 + 验证 wikilink
    │                                  ├─ 生成思考题 + 自检
    │                                  ├─ 写入 draft
    │◄──── 撰写结果摘要 ──────────────┤
    │                                  │
    ├─ 展示给用户                      │ (销毁)
```

**核心原则**：主 Agent 不直接读取 curated 文件内容，避免上下文污染。

## 执行步骤

### Step 1: 确认笔记类型

确认用户偏好的笔记类型（跳过如果已在 Phase 0 确定）。

### Step 2: Dispatch Writer Subagent

> **路径传递**：主 Agent 应从 TODO.md 读取上一个 phase 记录的 output 路径，作为本 phase 的 input 路径传给 subagent。

```typescript
Agent({
  subagent_type: "writer",
  prompt: `
Topic: {topic}
Note Type: {concept|practice|compare|cheat-sheet|experience}
Curated Dir: {SYSTEM_ROOT}/1-curated/{topic}/  # 从 TODO.md Phase 2 output 获取
Output Dir: {SYSTEM_ROOT}/2-drafts/{topic}/
  `,
  label: `write:${topic}`,
  phase: "Phase 3: Write"
})
```

对于心得笔记，在 prompt 中额外指定：
```
Raw Input: {SYSTEM_ROOT}/0-inbox/{topic}/raw-input.md
```

### Step 3: 展示结果

writer subagent 返回摘要后，向用户展示：
- 笔记结构概览
- 自检结果
- 需要用户确认的点

### Step 4: 硬停止

**严禁调用 `/beautify`。严禁进入 Phase 4。**
必须等待用户明确确认后才能进入 beautify。

## 禁止行为

- 主 Agent 不要直接读取 curated/ 目录下的文件内容（交给 writer）
- 不要跳过 subagent 调度手动撰写
