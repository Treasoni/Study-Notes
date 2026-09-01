---
title: 掌握度路径（Mastery Path）与 Course Study
tags:
  - obsidian/学习笔记
  - github项目
  - ai/agent
created: 2026-09-01
updated: 2026-09-01
status: 完成
source_project: deeptutor
---

# 掌握度路径（Mastery Path）与 Course Study

第 3 章我们把教材喂进知识库、让 DeepTutor 出题和深研，解决了"学什么、怎么练"的供给问题。但学习不能只靠"练得多"，还得回答"到底学会了没有"。本章讲 DeepTutor 给出的答案：用 **Mastery Path** 做分级掌握度验证，用 **Course Study** 把学习固定在某个课程上下文里（版本锚点 v1.6.2，具体功能以官方文档为准 [S1]）。

## 4.1 Mastery Path 是什么：分级掌握门控与 /learning 仪表盘

Mastery Path 是 DeepTutor 的功能面之一，与 Chat、Quiz、Solve 等共享同一个能力运行时与会话上下文，只是它的循环专门为"掌握度练习"设计 [S1]。在界面里，它和 Immersive Reading 一样是**独立的侧边栏工作区**，而不是首页上的一个按钮 [S1]。

它的核心机制叫**分级掌握门控**（progressive mastery gating）。自 v1.4.5 起，Guided Learning 重建在 chat agent loop 之上，为每种类型设置了硬性门控（hard per-type mastery gate），并配上 `/learning` 仪表盘统一展示进度 [S1]。可以把路径理解成被切成多个知识点关卡，每个关卡按类型（概念、计算、推理等）出题，**达标了才放行到下一级，没达标就卡住、回到对应材料重练**。这种"按类型卡进度"的设计，让掌握度验证不是笼统打一个分，而是能明确指出你的短板落在哪个类型上。

[!tip] 大白话
把 Mastery Path 想成"闯关游戏"：每一关没打满血条就不让你进下一关。所以它先暴露你在哪些类型上薄弱，再用题目验证你到底补上没有，而不是一路闷头往下学。

用法上，进入 Mastery Path 工作区后选一个学习目标，系统会在 `/learning` 仪表盘上显示各类型的掌握状态，逐级练习直到门控通过 [S1]。批改过的掌握度题目还会自动流入 **Question Bank**，成为后续可复用的题目资产 [S1]；这些已过关的题之后也能被第 5 章的 Book 等场景引用，作为生成材料的一部分。CLI 层同样保留了 mastery_path、course_study 两个能力入口，方便用脚本单轮触发 [S1]。

## 4.2 Course Study：课程绑定上下文的小班式学习

如果说 Mastery Path 是按"知识点"组织，Course Study 就是按"课程"组织。它与 Chat、Quiz 共享同一能力运行时，但**保持课程绑定的上下文**（course-bound context）[S1]。在 v1.6.0 中，课程自带 **Little Tutor** 与 **Ask Questions** 两个能力，由 [[Agent]] 在该课程的上下文内讲解和提问 [S1]。

[!tip] 大白话
把 Course Study 想成"小班教室"：一个班有自己的教材、聊天记录和作业。你在这个班里提问、被讲解，上下文不会串到别的科目，老师（Agent）记得你在这门课学到哪了。

支撑它的还有 Learning Space 里的 **My courses**：把每个科目的会话归组，tutor 线程嵌套在父课程之下，聊天历史可按课程或线程类型过滤 [S1]。所以课程不是一次性的聊天会话，而是有归属、可归档、可过滤的长期上下文。Course Study 因此适合按"一门课"推进：一门课一个上下文，学习材料、对话、出题都留在这个封闭范围内，不会互相串味。

## 4.3 与第 3 章核心玩法如何串联：从知识库 → 出题 → 掌握度验证

第 3 章和第 4 章其实是同一个闭环的两半。第 3 章在 Knowledge Center 建好知识库（[[RAG]] 可检索索引），用 Ask Questions / Quiz 生成习题；第 4 章的 Mastery Path 把这些内容变成"验证关卡"。

1. **知识库**（第 3 章）：上传教材，建立可检索索引，为回答和出题提供依据。
2. **出题**（第 3 章）：Ask Questions 针对某个知识点提问，Quiz 生成习题。
3. **掌握度验证**（本章）：Mastery Path 用分级门控逐级测你，通过后把批改过的题沉淀进 Question Bank [S1]，反过来再供第 3 章的场景（问答、习题、Living Book）复用。

[!tip] 实践建议
一个顺手的循环：进 Course Study 选定课程 → 用第 3 章的知识库问答和 Quiz 出题 → 到 Mastery Path 逐级验证 → 没通过的回到 Ask Questions 精讲该知识点 → 全部通过后题目进 Question Bank 成为资产。

[!summary] 本章小结
- Mastery Path 用分级掌握门控验证"是否真的学会"，`/learning` 仪表盘统一展示进度 [S1]。
- 掌握度题批改后自动流入 Question Bank，沉淀为可复用的题目资产 [S1]。
- Course Study 保持课程绑定上下文，课程自带 Little Tutor 与 Ask Questions，适合按门课推进 [S1]。
- 与第 3 章串联成"知识库 → 出题 → 掌握度验证"的闭环，即"学—练—验"。

下一章进入进阶玩法：把知识库、题库与聊天历史编译成交互式 **Living Book**，并让 **Partners/TutorBot** 在 IM 渠道上陪你学。
