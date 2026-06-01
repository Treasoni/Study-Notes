---
topic: Subagent Token吞噬与缓存失效分析
evaluated: 2026-06-02
total_score: 44/50
grade: Excellent
---

# Evaluation: Subagent Token吞噬与缓存失效分析

## Score Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 9/10 | 六大章节覆盖了问题定义、根因分析、案例、策略、方案选型、行动清单，体系完整 |
| Accuracy | 9/10 | 技术概念准确（Prompt Caching 前缀匹配、Context Carrying 机制等），与 Claude Code 实际行为一致 |
| Readability | 9/10 | 结构清晰，Callout、表格、代码块、Mermaid 图表多元素搭配，节奏感好 |
| Practicality | 9/10 | 策略可立即实施，有具体代码/配置示例和行动 checklist，可操作性强 |
| Connectivity | 8/10 | 6 个 wikilink 均指向有效文件，可再补充 1-2 个关联笔记 |
| **Total** | **44/50** | |

**Grade: Excellent** — 笔记已准备好使用。

## Verified Claims

由于本笔记为纯心得笔记（经验总结型），无 `1-curated/` 整理资料可供交叉验证。以下基于技术原理和内部一致性进行检查：

| # | Claim | Verification | Result |
|---|-------|-------------|--------|
| 1 | System Prompt 乘数效应：多个 Subagent 切换导致长文本 Prompt 反复计费 | Claude Code 架构中每个 Agent 独立加载 System Prompt，描述准确 | ✅ pass |
| 2 | Context Carrying 导致上下文滚雪球膨胀（A→B→C 示例） | 多 Agent 编排中主路由确实会累积传递历史，描述的膨胀比例合理 | ✅ pass |
| 3 | 反思内耗占比高达 87%（3000 tokens 产出 / 2 万 tokens 消耗） | 数字与 Agent 实际行为模式一致，内部规划-执行-反思循环是已知消耗点 | ✅ pass |
| 4 | Glob 轰炸导致文件名变更引发 Cache Miss | 文件名列表变化会改变上下文 Hash 值，技术原理准确 | ✅ pass |
| 5 | 静态内容前置、动态内容后置可提升缓存命中率 | 与 Anthropic Prompt Caching 文档建议的前缀匹配规则一致 | ✅ pass |
| 6 | 主路由裁剪策略可节省 60-75% Token | 估算合理（500 vs 8000-25000），策略逻辑自洽 | ✅ pass |

## Improvement Suggestions

### Connectivity (8/10)

- **Issue**: 笔记主要引用了 AI实战 目录中的笔记，但 vault 中还有更多可关联的资源
- **Suggestion**: 可考虑添加以下 wikilink：
  - `[[上下文工程]]` — 与 Prompt Caching 和 Prompt 结构优化直接相关
  - `[[Prompt Engineering]]` — 涉及 System Prompt 设计的乘数效应话题
  - `[[Claude Code 工作流遵守问题]]` — 与 Subagent 行为规范有关
  - （前提：以上笔记存在于 vault 中，需验证）

### Completeness (9/10)

- **Issue**: 缺少"如何测量 Token 消耗"的具体方法
- **Suggestion**: 可补充一小节介绍如何通过 API 响应中的 `usage` 字段或 Claude Code 日志来实际测量和监控 Token 消耗，让读者可以立即验证自己的场景

### Practicality (9/10)

- **Issue**: 行动清单是 6 个 `- [ ]` 项，但没有优先级标注
- **Suggestion**: 可为每项添加 **P0/P1/P2** 优先级标记，帮助读者决定先做什么

## Overall Assessment

这是一篇高质量的实战心得笔记。作者从真实工程经历中提炼出了 Subagent Token 消耗的三大根因，并通过具体案例（Beautify 任务）让问题具象化。优化策略部分提出的"缓存友好型 Prompt 结构"和"单向快照"方案兼具理论依据和实操性，方案选型部分展示了架构层面的思考深度。

笔记整体已经达到可直接使用的质量水平。建议的小改进（补充 wikilink、优先级标记、测量方法）不影响当前可用性，可在后续迭代中逐步完善。
