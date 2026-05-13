---
name: evaluate
description: 质量评估阶段。对已完成美化的笔记进行五维度评分（完整性/准确性/可读性/实用性/关联性），交叉验证已整理资料，生成结构化评估报告。触发时机：用户审核通过 beautify 产出并明确要求评估后，Phase 5。
---

# Skill: evaluate（质量评估）

## 触发时机
用户审核通过 beautify 产出后，且用户明确要求评估质量时。

## 输入
- `OUTPUT_PATH`: 最终美化笔记的路径，如 `{VAULT_PATH}/StudySystem/3-published/{topic}/{topic}.md`
- `SYSTEM_ROOT`: StudySystem 根路径，如 `{VAULT_PATH}/StudySystem`
- `topic`: 主题名称

## 五维度评分标准（各 0-10）

### 1. Completeness（完整性）
Are core concepts covered thoroughly?
- 10: full coverage with depth
- 7-9: main topics covered, minor gaps
- 4-6: some important topics missing
- 0-3: severely incomplete

### 2. Accuracy（准确性）
Does the content match the source materials?
- Spot-check 3-5 key claims against files in `{SYSTEM_ROOT}/1-curated/{topic}/`
- 10: all pass / 7-9: minor inaccuracies / 4-6: some errors / 0-3: major errors

### 3. Readability（可读性）
Is the note easy to follow?
- 10: clear structure, well-paced / 7-9: mostly clear / 4-6: hard to follow in places / 0-3: confusing

### 4. Practicality（实用性）
Are there actionable examples or guides?
- 10: rich examples / 7-9: decent examples / 4-6: not practical enough / 0-3: pure theory, no examples

### 5. Connectivity（关联性）
Are wikilinks and cross-references accurate and useful?
- 10: rich knowledge links / 7-9: good / 4-6: some but insufficient / 0-3: almost no links

## 执行步骤

### Step 1: 阅读最终笔记
读取 `{OUTPUT_PATH}`，理解完整内容和结构。

### Step 2: 交叉验证已整理资料
读取 `{SYSTEM_ROOT}/1-curated/{topic}/` 中的文件（尤其是 `core-concepts.md`）。
抽查笔记中的 3-5 个关键论断，与整理资料核对。
记录验证通过和有问题的论断。

### Step 3: 各维度评分
为所有 5 个维度评分，并附具体观察。评分低于 7 的维度说明具体缺失了什么。

### Step 4: 计算总分和等级
```
Total = Completeness + Accuracy + Readability + Practicality + Connectivity
```
Grade:
- >= 40 且所有维度 >= 5: **Excellent** -- ready to use
- 30-39: **Good** -- minor improvements suggested
- < 30 或任一维度 < 5: **Needs Rework**

### Step 5: 生成改进建议
针对每个评分 < 7 的维度，给出具体、可操作的建议和示例。

### Step 6: 写入评估报告
写入 `{SYSTEM_ROOT}/4-meta/evaluation/{topic}-eval.md`：

```markdown
---
topic: {topic}
evaluated: YYYY-MM-DD
total_score: {N}/50
grade: {grade}
---

# Evaluation: {topic}

## Score Summary

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | X/10 | ... |
| Accuracy | X/10 | ... |
| Readability | X/10 | ... |
| Practicality | X/10 | ... |
| Connectivity | X/10 | ... |
| **Total** | **X/50** | |

## Verified Claims

| # | Claim | Source | Result |
|---|-------|--------|--------|
| 1 | ... | ... | pass / issue |

## Improvement Suggestions

### {Dimension} (X/10)
- **Issue**: ...
- **Suggestion**: ...

## Overall Assessment

{brief summary paragraph}
```

## 产出
写入 `{SYSTEM_ROOT}/4-meta/evaluation/{topic}-eval.md`：
- 评分汇总表格
- 验证通过的论断列表
- 改进建议
- 总体评价

## 禁止行为
- 不要修改笔记本身 -- 只做评估
- 不要虚高或压低分数 -- 保持诚实
- 不要跳过交叉验证
- 不要给出模糊反馈 -- 始终引用笔记中的具体例子
- 不要调用其他技能
- 不要记录学习日志或错误日志 -- 那是 digest 阶段的事

## 硬停止 (Hard Stop)

本阶段任务完成。向用户展示评估结果（评分汇总、验证结果、改进建议）。

**严禁进行任何形式的自我改进或学习记录。**
询问用户："需要根据建议修改吗？" 或 "评估完成，可以结束了吗？"
