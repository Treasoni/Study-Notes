# Learnings Log

<!-- New entries are appended below. Compress when this file exceeds 100 lines. -->

---

## [LRN-20260524-001] best_practice

**Logged**: 2026-05-24T00:00:00+08:00
**Priority**: high
**Status**: pending
**Area**: workflow

### Summary
心得笔记（经验笔记）的 beautify 阶段必须询问用户输出路径

### Details
本次会话中，我在 beautify 阶段直接指定了输出路径 `30.areas/programming/claude-code/`，但用户希望放在 `AI实战/工程实践/`。这违反了 phase boundary 规则——输出路径是用户的重要决策，不应由我单方面决定。

心得笔记和研究笔记的区别：
- 研究笔记：通常在 Phase 0 确定输出路径
- 心得笔记：用户直接提供内容，输出路径应在 beautify 前确认

### Suggested Action
在 beautify 阶段的产出说明中，明确询问用户："笔记想放在哪个文件夹？" 仅在用户确认后才写入文件。

---

## [LRN-20260524-002] best_practice

**Logged**: 2026-05-24T00:00:00+08:00
**Priority**: medium
**Status**: pending
**Area**: workflow

### Summary
Pre-Task Init 中的强制读取不能跳过

### Details
按照 CLAUDE.md 的 "Mandatory Triggered Reads"，进入任何 Study System 工作流前必须：
1. Read `.obsidian-config.md` → 验证 VAULT_PATH
2. Read `.learnings/RULES.md` → 了解要避免的错误

本次会话跳过了这些读取，导致重复犯同样的错误（如直接写入文件而不询问用户）。

### Suggested Action
在 Agent 的 system prompt 或 CLAUDE.md 中明确：Pre-Task Init 是硬性要求，任何 Study System 任务开始时必须执行。

---

## [LRN-20260524-003] best_practice

**Logged**: 2026-05-24T15:30:00+08:00
**Priority**: medium
**Status**: pending
**Area**: workflow

### Summary
心得笔记的 evaluate 阶段可给出具体改进建议并自动应用

### Details
本次评估发现 Practicality 8/10（场景示例抽象）和 Readability 8/10（Mermaid 图缺图注）。改进建议具体且可操作：
- 添加 Skill 编排的具体代码示例
- 为 Mermaid 图表添加图注

评估后用户选择"改进"，我直接应用了建议，笔记质量得到提升。

### Suggested Action
评估阶段的改进建议应该是具体的、可执行的代码/文本片段，而不是模糊的方向性描述。

---

## [LRN-20260524-004] knowledge_gap

**Logged**: 2026-05-24T15:35:00+08:00
**Priority**: medium
**Status**: pending
**Area**: research

### Summary
`.claude/agents/` 的 `tools` 字段支持细粒度权限控制（已验证）

### Details
原始内容提到 "物理级权限隔离" 时被标记为 `[待验证]`。通过 Agent 工具探索验证：
- `tools: Read, Grep, Glob` = 只读 Agent
- 支持逗号分隔格式
- 可结合 `permissionMode` 控制确认行为

### Suggested Action
在引用官方功能时，如果不确定，标记 `[待验证]` 并在 review 阶段使用 Agent/搜索进行核实。

---
