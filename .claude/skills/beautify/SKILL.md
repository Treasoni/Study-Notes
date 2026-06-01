---
name: beautify
description: 美化排版阶段。调度 beautifier subagent 套用 Obsidian Markdown 规范，添加双链、标签、Callout 块、Mermaid 图表、YAML frontmatter 等 Obsidian 特性，优化段落长度和术语一致性。触发时机：用户审核通过 write 产出后，Phase 4。
---

# Skill: beautify（美化排版）

## 触发时机
用户审核通过 write 产出后。

## 输入
`{SYSTEM_ROOT}/2-drafts/{topic}/{topic}-笔记.md`

## 依赖技能

| 技能 | 用途 | 调用方 |
|------|------|--------|
| `obsidian-markdown` | Obsidian 语法规范 | beautifier subagent |
| `obsidian-cli` | 在 Obsidian 中创建笔记 | beautifier subagent |
| `json-canvas` | 生成知识地图 Canvas（可选） | beautifier subagent |
| `obsidian-bases` | 生成学习笔记索引 Base（可选） | beautifier subagent |

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为调度员，beautifier subagent 作为执行者。

```
主 Agent (PM)                    Beautifier Subagent (专员)
    │                                  │
    ├─ 传递 draft 路径 + 配置 ──────►│
    │                                  ├─ 加载 obsidian-markdown 规范
    │                                  ├─ 检查 Markdown 基础
    │                                  ├─ 添加 Obsidian 特性 (6 步)
    │                                  ├─ 术语统一
    │                                  ├─ 写入最终笔记
    │                                  ├─ [可选] 生成 canvas/base
    │◄──── 美化结果摘要 ──────────────┤
    │                                  │
    ├─ 展示给用户                      │ (销毁)
```

**核心原则**：主 Agent 不加载 Obsidian 语法规范、不执行 Glob 验证，避免上下文污染。

## 执行步骤

### Step 1: 确认配置

确认是否需要生成 Canvas 知识地图和 Base 学习索引。

### Step 2: Dispatch Beautifier Subagent

> **路径传递**：主 Agent 应从 TODO.md 读取上一个 phase 记录的 output 路径，作为本 phase 的 input 路径传给 subagent。

```typescript
Agent({
  subagent_type: "beautifier",
  prompt: `
Topic: {topic}
Draft: {SYSTEM_ROOT}/2-drafts/{topic}/{topic}-笔记.md  # 从 TODO.md Phase 3 output 获取
Output Path: {OUTPUT_PATH}/{topic}.md
Generate Canvas: {true|false}
Generate Base: {true|false}
  `,
  label: `beautify:${topic}`,
  phase: "Phase 4: Beautify"
})
```

### Step 3: 展示结果

beautifier subagent 返回摘要后，向用户展示：
- 应用的 Obsidian 特性统计
- 产出文件列表
- 需要用户确认的点

### Step 4: 硬停止

**严禁调用 `/evaluate`。严禁进入 Phase 5。**
询问用户："需要修改吗？" 或 "要继续评估质量吗？"

## 禁止行为

- 主 Agent 不要直接加载 obsidian-markdown skill（交给 beautifier）
- 主 Agent 不要执行 Glob 验证 wikilink（交给 beautifier）
- 不要跳过 subagent 调度手动美化
