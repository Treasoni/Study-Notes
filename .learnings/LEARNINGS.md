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
