---
title: "DeepSeek-Harness 配置使用教程"
tags: [deepseek-harness, ai, agent, 教程, MOC, 导览]
created: 2026-08-13
updated: 2026-08-13
status: new
source_project: deepseek-harness
---

# DeepSeek-Harness 配置使用教程 · 系列导览

> [!summary] 系列入口
> 本文件是整套分册的入口（README / 导览），不含正文。正文分布在 5 篇独立分册中，按推荐顺序阅读即可。

## 这是什么

《DeepSeek-Harness 配置使用教程》是一套面向「熟悉 [[Claude Code MOC|Claude Code]] 的用户」的实战配置教程，共 5 篇独立分册，覆盖 dsh（deepseek-harness）的定位、安装、配置、迁移决策与日常速查。整套笔记以「快速上手 + 从 Claude Code 对照迁移」为核心视角。

- **主题**：deepseek-harness（dsh）——DeepSeek 官方开源的 agent harness
- **核心公式**：`Model + Harness = Agent`
- **目标读者**：熟悉 Claude Code、想快速上手 dsh 或评估「换还是留」的用户
- **产出形态**：5 篇分册 + 本导览（每篇约 1,800–3,000 字，整套约 11,000 字）
- **发布目标**：Obsidian vault `AI学习/DeepSeek-Harness 教程/`

## 分册清单

| 序号 | 分册 | 一句话说明 | 读完能做什么 |
|---|---|---|---|
| 01 | [[DeepSeek-Harness 是什么]] | 建立心智模型：dsh 不是模型，而是「可组装的 agent 运行时」 | 知道 dsh 的定位、核心架构与同名包避坑 |
| 02 | [[DeepSeek-Harness 安装与快速上手]] | 安装三路径 + Web UI 首次配置，5 分钟跑通第一个会话 | 跑通 Web UI 第一个任务与 headless 一次性任务 |
| 03 | [[DeepSeek-Harness 配置体系]] | 全书核心：多层 YAML 补丁树 + Profile + Agent Preset + CLI 完整参考 | 看懂并修改 dsh 配置，接第三方/自定义 provider |
| 04 | [[DeepSeek-Harness 与ClaudeCode对照迁移]] | 概念 / 成本 / 性能三张对照表 + 三选迁移策略 | 判断哪些任务换 dsh、哪些留在 Claude Code |
| 05 | [[DeepSeek-Harness 常见坑与速查]] | 日常速查：坑清单、命令速查、V4 协议坑、生态资源 | 规避高频坑，知道遇到问题去哪里反馈 |

## 推荐阅读顺序

**主路径（推荐）**：第 1 → 2 → 3 → 4 → 5 章顺序阅读。

- 第 1 章建立心智模型；
- 第 2 章动手跑通；
- 第 3 章深入配置（全书核心，篇幅最长）；
- 第 4 章做迁移决策；
- 第 5 章作为日常速查随时翻阅。
- 每章阅读 + 实操约 30–40 分钟。

**急用路径**：先读第 2 章跑通环境 → 第 4 章做「换还是留」决策 → 回头补第 3、5 章。若暂不迁移，第 4 章可跳读成本与性能表格。

> [!warning] 不建议跳章
> 第 3 章是全书的配置核心，后续章节的迁移对比会大量引用其概念（补丁树、Profile、Agent Preset），不建议跳过。

## 系列约定

- **独立性**：5 篇分册各自独立，不合并正文；每篇自带「本章小结」与素材来源脚注。
- **标题层级**：每篇 H1 为章标题（`第X章：...`），H2 为节标题（`X.Y ...`），H2「本章小结」收尾。
- **编号**：章节号与分册文件名一一对应（01–05），节编号与章号同步（如第 3 章 3.1–3.7）。
- **交叉引用**：分册间引用统一使用「第 X 章」/「5.3」式样，并用双链互相连接。

## 相关文件

- 大纲：`../03_outline.md`（项目工作区）
- 素材：`../02_deep_research.md`
- 意图：`../00_intent.md`
- 章节源文件：`../chapters/`

## 状态

- 组装模式：C（保持零散分册）
- 组装时间：2026-08-13
- 美化发布：2026-08-13
