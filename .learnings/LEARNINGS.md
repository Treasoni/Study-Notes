# Learnings Log

<!-- New entries are appended below. Compress when this file exceeds 100 lines. -->

<!-- Latest session: 2026-05-14 - AI缓存命中与未命中 - No significant learnings to record (workflow completed smoothly) -->

<!-- Latest session: 2026-05-14 - AI学习 MOC 更新 -->
<!-- Learnings: -->
<!-- 1. MOC 路径使用相对路径（不含 vault 根），如 "AI学习/00-索引/" -->
<!-- 2. 扫描时用 find + grep 排除 sortspec.md 和 MOC.md -->
<!-- 3. Mermaid 图表特殊字符（如 { } 和深层嵌套）可能导致渲染问题 -->
<!-- 4. subgraph 分组 + 扁平结构可改善 Obsidian 渲染效果 -->

<!-- Latest session: 2026-05-14 - AI上下文工程学习 -->
<!-- Learnings: -->
<!-- 1. beautify 阶段用 Glob 验证双链目标是否存在，避免悬空链接 -->
<!-- 2. RAG 相关笔记存在于 "AI学习/03-技术专题/RAG技术入门指南.md" -->
<!-- 3. Agent 相关笔记存在于 "AI学习/01-基础概念/Agent智能体.md" -->
<!-- 4. 评估得分 42/50 Excellent，概念笔记结构可复用 -->

---

## [LRN-20260514-003] best_practice

**Logged**: 2026-05-14T
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
双链验证流程：Glob 检查优先于 beautify 阶段

### Details
本次 beautify 阶段使用 Glob 验证了双链目标（RAG、Agent）是否存在后再写入 wikilink，避免了悬空链接问题。建议将此流程固化为标准步骤。

### Suggested Action
在 beautify 的 Step 3b 双链部分添加 "预先用 Glob 验证"的强制步骤

---

## [LRN-20260514-004] evaluation_insight

**Logged**: 2026-05-14T
**Priority**: low
**Status**: pending
**Area**: docs

### Summary
概念笔记评估结果：42/50 Excellent，实用性维度有提升空间

### Details
评估发现：
- 实用性 7/10（示例偏少，缺少渐进式示例）
- Connectivity 9/10（双链正确）
- Accuracy 9/10（交叉验证全部通过）

### Suggested Action
对于入门级概念笔记，增加渐进式提示词示例可提升实用性评分

---

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
