# Learnings Log

<!-- New entries are appended below. Compress when this file exceeds 100 lines. -->

<!-- Latest session: 2026-05-14 - AI缓存命中与未命中 - No significant learnings to record (workflow completed smoothly) -->

<!-- Latest session: 2026-05-14 - AI学习 MOC 更新 -->
<!-- Learnings: -->
<!-- 1. MOC 路径使用相对路径（不含 vault 根），如 "AI学习/00-索引/" -->
<!-- 2. 扫描时用 find + grep 排除 sortspec.md 和 MOC.md -->
<!-- 3. Mermaid 图表特殊字符（如 { } 和深层嵌套）可能导致渲染问题 -->
<!-- 4. subgraph 分组 + 扁平结构可改善 Obsidian 渲染效果 -->

<!-- Latest session: 2026-05-14 - 提示词工程学习 -->
<!-- Learnings: -->
<!-- 1. Phase 2 整理后用户可能要求补充特定缺口（如迭代方法、模型差异），而非从头重新 collect -->
<!-- 2. 评估发现双链目标笔记可能不存在，导致 Connectivity 评分低 -->
<!-- 3. 评估得分 39/50，常见短板：双链悬空 + 缺少快速模板 -->
<!-- 4. 用户深度选择"入门"时，进阶内容可标记 [待补充] 而非删除 -->

---

## [LRN-20260514-001] knowledge_gap

**Logged**: 2026-05-14T
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
用户可能在 Phase 2 后要求补充特定缺口，而非接受现有内容

### Details
本次会话中，用户在 Phase 2 完成后要求补充"提示词迭代方法"和"模型差异"。这说明：
- Phase 2 的缺口分析可能不够完善
- 用户对学习内容有明确预期

### Suggested Action
在 Phase 2 输出时，更主动地询问用户是否需要补充特定主题

---

## [LRN-20260514-002] best_practice

**Logged**: 2026-05-14T
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
评估阶段 Connectivity 评分低，需提前确认双链目标笔记存在

### Details
评估发现 [[大语言模型]] 等双链目标可能不存在，导致悬空链接。建议：
- beautify 阶段用 obsidian-cli search 验证双链目标
- 或在评估时提醒用户检查

### Suggested Action
在 beautify 后添加双链验证步骤

---
