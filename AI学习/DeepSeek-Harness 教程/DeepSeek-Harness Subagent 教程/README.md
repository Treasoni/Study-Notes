---
title: "DeepSeek-Harness Subagent 开发——如何写 subagent（从能力缝到 provider）"
tags: [deepseek-harness, ai, agent, subagent, 教程, 开发]
created: 2026-08-16
updated: 2026-08-16
status: new
source_project: deepseek-harness
---


> [!info] 笔记信息
> - **系列归属**：DeepSeek-Harness 教程系列 · 新分册
> - **笔记类型**：概念理解 + 实战（上手）
> - **读者画像**：熟悉 Claude Code 扩展体系、已读 dsh 插件开发五章的「有了解」用户
> - **预计篇幅**：约 26-32 页（中长篇分册）
> - **版本锚点**：developer preview（2026-08-13 锚点）
> - **分册结构**：`DeepSeek-Harness Subagent 教程/` 目录（本首页 + 7 章独立文件，已从 135KB 单文件拆分）
> - **系列入口**：[[DeepSeek-Harness 教程/README|系列导览]] · [[DeepSeek-Harness MOC|教程 MOC]]

## 学习路径摘要

> 摘要取自系列大纲，先定位「我在哪、要去哪」。

### 前置要求

- 熟悉 Claude Code 扩展体系：`.claude/agents/*.md`、subagent 调用心智、工具定义
- 已读完 DeepSeek-Harness 插件开发五章：cordis 插件结构、`ctx.tools` / `defineTool`、`dsh plugin add`、`cordis.patch.yml`
- 能读 TypeScript 接口 / 泛型 / 可选方法签名（`SubagentProvider` 契约是类型收窄驱动的）

### 学完能做什么

- 说清 dsh subagent 的「能力缝 + 三层结构」心智模型，并迁移 Claude Code 的 subagent 心智
- 按需选择并挂载现成 provider（spawn / fork / acp / dsh-sdk），用 `dsh-tool-subagent` 暴露给模型
- 独立写一个最小 provider 插件，用 `ctx.subagents.registerProvider` 注册并挂进 cordis 插件树
- 理解 one-shot / continuable 生命周期与委派深度限制，避开 `UNSUPPORTED_CAPABILITY`、无默认导出等已知坑
- 给后续分册留好接口（codex / claude-code provider 配置、跨进程 continuable 社区方案）

### 建议学习顺序

- 顺序通读第 1-4 章（心智 → 契约 → 现成 provider → 写自己的 provider），这是主路径
- 第 5 章生命周期对只想快速上手的读者可先跳读，写 provider 遇到 `prepareContinuable` 或配置 backgroundMode 时再回来补
- 第 6 章工具化在动手「把 provider 给模型用」时精读；第 7 章速查在写作与排错时当索引用
- 预估时间：通读约 2-3 小时；动手写第一个 provider 另加 1-2 小时（含对照源码核实 6.1）
- 每章读完建议做一次「与 Claude Code 对照」的迁移笔记，沉淀进个人 Obsidian

> [!note] 诚实标注约定（贯穿全文，不得删除）
> 本系列对三类「信心等级」做显式标注：**综合推断**（官方无直接文档，由 S2 契约 + S4 方法论拼合，发布前须对照源码核实）、**未证实**（仅社区二手说法，不展开）、**未抓取**（本分册未收集，标注可扩展）。各章相关标注原样保留，第 7 章 7.3 集中收口。

## 章节目录

| 章 | 笔记 | 一句话定位 |
|----|------|-----------|
| 01 | [[01-心智模型-能力缝与三层结构|心智模型：能力缝与三层结构]] | subagent 为什么是「能力缝」、三层结构、微内核与三段式原则 |
| 02 | [[02-核心契约-ctxsubagents与SubagentProvider接口|核心契约：ctx.subagents 与 SubagentProvider]] | 注册表、provider 契约、StartRequest 选项、Run/Result 语义 |
| 03 | [[03-现成provider家族-选用挂载跑起来|现成 provider 家族]] | 选哪个、怎么挂、怎么跑：in-process vs out-of-process |
| 04 | [[04-写自己的provider-三段式与最小实现|写自己的 provider]] | 三段式方法论 + 最小骨架逐行拆解（综合推断标注） |
| 05 | [[05-生命周期深度-oneshot与continuable与委派深度|生命周期深度]] | one-shot / continuable 与委派深度机制 |
| 06 | [[06-工具化-把provider暴露成模型可调能力|工具化]] | 把 provider 暴露成模型可调能力（tool/control/report） |
| 07 | [[07-速查与避坑清单|速查与避坑清单]] | 避坑速查、决策速查、诚实标注收口 |

> 建议从 [[01-心智模型-能力缝与三层结构|第一章]] 开始顺序通读第 1-4 章（主路径），第 5-7 章按需精读。

---

