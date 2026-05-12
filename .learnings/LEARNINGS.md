# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260512-001] best_practice

**Logged**: 2026-05-12T00:00:00Z
**Priority**: medium
**Status**: pending
**Area**: config

### Summary
defuddle 对某些官方站点返回 403 时，opencli web read 是有效的替代方案

### Details
在 Harness Engineering 的 collect 阶段：
- defuddle parse 对 openai.com 返回 403
- defuddle parse 对 zhuanlan.zhihu.com 返回 403
- defuddle parse 对 langchain.com 和 softwareimprovementgroup.com 超时
- 改用 `opencli web read --url <url>` 后成功获取了 OpenAI（~23KB）、LangChain（~19KB）、Medium（~19KB）、SIG（~25KB）的内容

结论：defuddle 和 opencli web read 可作为互补工具组合使用，搜索阶段先用 defuddle 尝试，失败后 fallback 到 web read。

### Suggested Action
在 Study System 的 collect 阶段说明中，将 opencli web read 列为 defuddle 的标准 fallback

### Metadata
- Source: experience
- Tags: collect, defuddle, opencli, fallback
- Pattern-Key: network-fallback.defuddle-webread
- See Also: RULES.md (network-fallback.opencli)

---

## [LRN-20260512-002] correction

**Logged**: 2026-05-12T00:00:00Z
**Priority**: medium
**Status**: pending
**Area**: writing

### Summary
笔记中 SDD 标题被笔误写成 CDD，需在 beautify 阶段增加标题核对步骤

### Details
在 beautify 后的笔记中，"SDD vs Harness Engineering" 章节的标题被误写为 "CDD vs Harness Engineering"。虽然正文内容全部正确使用了 SDD，但标题一处笔误被 evaluate 阶段发现。

原因：书写 draft 和 beautify 两个阶段都未对标题做专门的准确性核查。

### Suggested Action
在 beautify 阶段的自检清单中加入一条：检查所有小标题与正文内容的一致性，确保无笔误

### Metadata
- Source: self_review
- Tags: beautify, writing, quality
- Pattern-Key: writing.title-typo

---

## [LRN-20260512-003] insight

**Logged**: 2026-05-12T00:00:00Z
**Priority**: low
**Status**: pending
**Area**: workflow

### Summary
首次完整运行 Study System 六阶段管线（collect→curate→write→beautify→evaluate→digest）成功

### Details
本次 Harness Engineering 学习任务是第一次完整经历 Study System 全部六个阶段。关键发现：
1. Phase 0 的路径配置检查成功拦截了错误的 vault 路径
2. collect 阶段的 source diversity 策略（中英文、官方/社区、文章/视频）效果好
3. beautify 阶段新增的 Mermaid 图和 Callout 设置标准可复用到未来笔记
4. evaluate 阶段发现了一处 beautify 未能捕获的笔误
5. 整体流程顺畅，但 defuddle 的 fallback 机制需要标准化

### Suggested Action
保持当前流程不变，将 defuddle fallback 流程标准化

### Metadata
- Source: experience
- Tags: workflow, study-system, pipeline
---
