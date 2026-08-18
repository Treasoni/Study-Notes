---
title: "DeepSeek-Harness 插件开发教程"
tags: [deepseek-harness, ai, agent, 教程, MOC, 导览, 插件]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 插件开发教程 · 系列导览

> [!summary] 系列入口
> 本文件是整套分册的入口（README / 导览），不含正文。正文分布在多篇独立分册中，按推荐顺序阅读即可。

## 这是什么

《DeepSeek-Harness 插件开发教程》是一套面向「熟悉 [[Claude Code MOC|Claude Code]] 的用户」的**插件开发教程**，共 4 篇主章分册 + 1 篇插件开发分册（00 速查 + 01 核心 + 02-03 配置 + 04-10 实战路径）+ 1 篇子系统开发分册，覆盖 dsh（deepseek-harness）的心智模型、环境准备、插件开发核心、配置体系、实战项目与日常速查。整套笔记以「**写你自己的 dsh 插件**」为核心视角，用 Claude Code 的扩展体系（hooks / CLAUDE.md / MCP / Skills）作桥。

- **主题**：deepseek-harness（dsh）——DeepSeek 官方开源的 agent harness
- **核心公式**：`Model + Harness = Agent`；`一切皆插件`，无特权核心
- **目标读者**：熟悉 Claude Code、想写自己的 dsh 插件（工具 / 提示词 / 服务）的用户
- **产出形态**：4 篇主章分册 + 1 篇插件开发分册（00-10 章，篇幅较长）+ 1 篇子系统开发分册 + 本导览（主章每篇约 1,000–2,500 字，整套正文约 3 万字）
- **发布目标**：Obsidian vault `AI学习/DeepSeek-Harness 教程/`

## 分册清单

| 序号 | 分册 | 一句话说明 | 读完能做什么 |
|---|---|---|---|
| 01 | [[DeepSeek-Harness 是什么]] | 心智模型：dsh 是「插件树 vs 单体 + 扩展」，你写的插件与官方对等 | 理解「为什么我写的插件能像官方插件一样有地位」 |
| 02 | [[DeepSeek-Harness 安装与快速上手]] | 环境准备：写插件必须走源码运行路径，5 分钟跑通 | 有能跑 `pnpm dsh web --patch` 的开发环境 |
| 03 | [[DeepSeek-Harness 插件开发教程/README\|DeepSeek-Harness 插件开发]] | 插件开发分册：00 速查 + 01 核心（apply/生命周期/依赖/工具 DSL/提示词）+ 02-03 配置专册 + 04-10 实战渐进路径（git_log 写→配→验证→打包→安装，改造/从零双入口） | 看懂核心、搞懂配置、独立写出并打包一个可复用插件 |
| 04 | [[DeepSeek-Harness 与ClaudeCode对照迁移]] | 实战项目：从零写一个自定义工具插件，每步对照 Claude Code | 独立完成一个自定义工具插件并打包 |
| 05 | [[DeepSeek-Harness 常见坑与速查]] | 插件开发速查：坑 / 命令 / 工具契约 / 配置引用 / 生态 | 写插件时遇到问题快速定位 |

> [!example] 配套脚手架
> `example-plugin/` 是本系列的完整示例插件（`repo_status` 自定义工具），可直接跑通并改成你自己的工具。

## 推荐阅读顺序

**主路径（推荐）**：第 1 → 2 → 3 → 4 → 5 章顺序阅读。

- 第 1 章转心智模型（Claude Code 单体+扩展 → dsh 插件树）；
- 第 2 章搭源码开发环境；
- 第 3 章深入插件开发分册 [[DeepSeek-Harness 插件开发教程/README|DeepSeek-Harness 插件开发]]（全书核心，篇幅最长）：先读 00-01（速查 + 核心），配置细节查 02-03，再走 04-10 实战渐进路径；
- 第 4 章动手写一个自定义工具插件（[[DeepSeek-Harness 与ClaudeCode对照迁移|对照迁移]] 分册每步对照 Claude Code）；
- 第 5 章作为日常速查随时翻阅。
- 每章阅读 + 实操约 30–40 分钟。

**急用路径**：先读第 2 章跑通环境 → 第 4 章照猫画虎写第一个工具 → 要搬现成配置时读 [[DeepSeek-Harness 插件开发教程/03-配置实战-接入skills-hooks-mcp-rules|配置实战]] → 回头补插件开发分册、第 5 章。

> [!warning] 不建议跳章
> 第 3 章是插件开发核心，第 4 章实战的每一步都引用其概念（apply / patch / inject / defineTool），不建议跳过。

## 系列约定

- **独立性**：各分册各自独立，不合并正文；每篇自带「本章小结」与素材来源脚注。
- **标题层级**：每篇 H1 为章标题（`第X章：...`），H2 为节标题（`X.Y ...`），H2「本章小结」收尾。
- **编号**：主章 01–05 与文件名一一对应，主章节编号与章号同步（X.Y）；配套专册使用独立编号（1–N），不混入主章号。
- **交叉引用**：分册间引用统一使用「第 X 章」/「5.3」式样，并用双链互相连接。
- **桥接视角**：核心概念均附 `[!note] 这在 Claude Code 里相当于`，降低迁移成本。

## 状态

- 组装模式：C（保持零散分册）
- 组装时间：2026-08-13
- 美化发布：2026-08-16（插件开发分册重组：TS 速查 / 插件开发核心 / 配置体系 / 配置实战 / 插件实战 / 从零写插件 六篇合并为 [[DeepSeek-Harness 插件开发教程/README|DeepSeek-Harness 插件开发]] 00-10 章）
