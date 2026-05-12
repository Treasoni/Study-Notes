---
topic: "CLAUDE.md 放置策略"
evaluated: 2026-05-12
total_score: 46/50
grade: Excellent
---

# Evaluation: CLAUDE.md 放置策略

## Score Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 9/10 | 两个方案完整覆盖，含选择建议、决策流程、踩坑、示例 |
| Accuracy | 10/10 | 所有论断与原始输入一致，无事实错误 |
| Readability | 9/10 | 结构清晰，Mermaid 图表辅助理解，格式统一 |
| Practicality | 10/10 | 即用型方案，含可复制的代码示例和决策标准 |
| Connectivity | 8/10 | 关联 4 篇已有笔记，标签合理；缺少外部官方文档链接 |
| **Total** | **46/50** | **Grade: Excellent** |

## Verified Claims

| # | Claim | Source | Result |
|---|-------|--------|--------|
| 1 | Claude Code 读取当前终端所在目录的 CLAUDE.md | 个人经验 | pass |
| 2 | 不需要两个完全相同的 CLAUDE.md | 个人经验 | pass |
| 3 | 方案一适合功能单一、小团队项目 | 个人经验 | pass |
| 4 | 方案二适合多子系统、复杂项目 | 个人经验 | pass |
| 5 | 根目录 CLAUDE.md 示例代码语法正确 | 个人经验 | pass |

## Improvement Suggestions

### Connectivity (8/10)
- **Issue**: 缺少指向 Claude Code 官方文档的外部链接，如 CLAUDE.md 的官方说明
- **Suggestion**: 可在"延伸"部分添加：
  ```markdown
  - [Claude Code 官方文档 — CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/overview)
  ```

### Readability (9/10)
- **Issue**: "选择建议"中两个维度表结构相近，首次阅读容易混淆
- **Suggestion**: 当前结构已经合理，两个表格紧邻且对比清晰，Mermaid 决策图进一步降低了理解门槛，无需修改。

## Overall Assessment

这是一篇高质量的心得笔记。用户基于亲身实践，系统梳理了 CLAUDE.md 的两种放置策略，并给出了清晰的选择建议。笔记结构完整、逻辑递进，从问题引出到方案对比，再到决策指引和实际踩坑，最后以延伸思考收尾。Mermaid 图表的使用增强了可视化理解。4 条 wikilink 连接了 vault 中已有的相关笔记，形成了知识网络。整体达到 Excellent 级别，可以直接使用。
