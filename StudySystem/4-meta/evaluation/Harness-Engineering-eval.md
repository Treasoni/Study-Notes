---
topic: Harness Engineering（系统治理工程）
evaluated: 2026-05-12
total_score: 43/50
grade: Excellent
---

# Evaluation: Harness Engineering（系统治理工程）

## Score Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Completeness（完整性）** | 8/10 | 覆盖全面，但缺 Agent 失败模式章节 |
| **Accuracy（准确性）** | 9/10 | 一处标题笔误：CDD → SDD |
| **Readability（可读性）** | 9/10 | 结构清晰，递进合理，图表丰富 |
| **Practicality（实用性）** | 8/10 | 有实战路径，但缺具体 AGENTS.md 示例 |
| **Connectivity（关联性）** | 9/10 | 8 个双链 + Mermaid 关系图，丰富 |
| **Total** | **43/50** | **Excellent** |

## Verified Claims

| # | Claim | Source | Result |
|---|-------|--------|--------|
| 1 | "人类掌舵，智能体执行" 是核心哲学 | doc-01 OpenAI 原文: "Humans steer. Agents execute." | ✅ pass |
| 2 | Mitchell Hashimoto 在 2026 年 2 月 5 日提出 Engineer the Harness | doc-02 + doc-07（菜鸟教程确认日期） | ✅ pass |
| 3 | OpenAI 5 个月产出百万行代码，零行人工 | doc-01 原文: "在过去五个月里...没有一行代码是人工编写的" | ✅ pass |
| 4 | 3 人 → 7 人团队，人均 3.5 PR/天，~1500 PR | doc-01 原文数据 | ✅ pass |
| 5 | LangChain Terminal Bench 52.8% → 66.5%，排名 30 → 5 | doc-07（菜鸟教程引用 LangChain 公开数据） | ✅ pass |
| 6 | Harness ⊃ Context ⊃ Prompt 三层包含关系 | Martion Fowler 框架 + 已有笔记确认 | ✅ pass |

**1 issue found:**

| # | Issue | Location | Correction |
|---|-------|----------|------------|
| 1 | 标题笔误: "CDD vs Harness Engineering" → 应为 "SDD" | 第 304 行 | 内容中均正确使用 SDD，仅标题一处 |

## 各维度详细评估

### Completeness（完整性）8/10

**覆盖良好的部分：**
- ✅ 术语起源（Mitchell → OpenAI → Fowler → LangChain 时间线）
- ✅ 核心原理（公式、类比、前馈+反馈框架）
- ✅ OpenAI 实战案例（六大组件、文档结构、效率数据）
- ✅ 进阶内容（Harness 组件架构、子代理防火墙、Harnessability）
- ✅ SDD 对比视角
- ✅ 常见误区
- ✅ 最小可行实践路径
- ✅ 思考题

**缺口：**
- Agent 常见失败模式（One-shotting、过早宣布胜利等）在整理资料中有专门章节（core-concepts.md §7），但未在笔记中体现
- 建议在"为什么存在"部分后新增一节展示典型失败模式

### Accuracy（准确性）9/10

- ⚠️ **第 304 行标题**："CDD vs Harness Engineering" — CDD 应为 SDD（Spec-Driven Development）
- 其余 6 个验证点全部通过
- 关键数据（百万行、5 个月、1500 PR、3.5 PR/天）均与原始资料完全一致
- 引用的对比、比喻、框架均忠实反映来源

### Readability（可读性）9/10

**优点：**
- "入门 → 进阶" 的递进结构清晰，适合不同水平读者
- 10 个 Callout 块种类多样，有效区分信息类型
- 4 个 Mermaid 图表大幅提升概念理解效率
- 避免了大段文字，表格和列表配合得当

**可改进：**
- difficulty 标签设为 "beginner" 偏保守，实际内容覆盖 beginner + intermediate，建议调整为多值

### Practicality（实用性）8/10

**优点：**
- OpenAI 案例提供了真实可参考的六大组件体系
- 四步实践路径（Start → 结构化 → 自动化 → 规模化）可操作
- SDD 对比帮助已有 SDD 实践的读者更好落地

**改进建议：**
- 缺少一个**具体的 AGENTS.md 示例文件**（从源材料中提取或简化）
- 缺少一个**最小 Harness 配置的代码示例**（如 CLI Agent 的配置片段）
- 可加入"检查清单"形式的运维指南

### Connectivity（关联性）9/10

- 8 个双链，6 个指向 vault 中已有笔记
- 2 个占位符链接（Prompt Engineering、Context Engineering）合理，已在导言中说明
- Mermaid 关系图清晰地展示了概念间的层次和关联
- 参考资料按类型分组（官方源 / 深度分析 / 实战指南 / 中文资源），方便查找

## Improvement Suggestions

### Accuracy (9/10)
- **Issue**: 标题 "CDD vs Harness Engineering" 是笔误
- **Suggestion**: 将第 304 行 "CDD" 改为 "SDD"

### Practicality (8/10)
- **Issue**: 缺少具体的 AGENTS.md 示例
- **Suggestion**: 在"最小可行实践"部分加入一个简化的 AGENTS.md 片段，如：
  ```markdown
  # AGENTS.md
  - Always run `npm test` after modifying source files
  - Before making changes, read the relevant docs in `/docs/`
  - Keep PRs focused on a single concern
  - Use `git log --oneline -10` to understand recent changes
  ```

### Completeness (8/10)
- **Issue**: 缺少 Agent 常见失败模式章节
- **Suggestion**: 在"为什么存在"之后加入简短的 Agent 失败模式表格（从 core-concepts.md §7 提取）

## Overall Assessment

这份笔记以 **Excellent** 评级通过评估。它在概念解读、理论框架、实战案例、知识关联四个维度上都表现出色，体现了对多个权威来源的忠实梳理和融会贯通。唯一的技术性错误是标题笔误（CDD → SDD），修复后即可视为完整交付。

建议在后续迭代中补充一个具体的 AGENTS.md 示例和 Agent 失败模式小节，以进一步提升实用性。整体而言，这是一份高质量的概念笔记，可直接用于学习和参考。
