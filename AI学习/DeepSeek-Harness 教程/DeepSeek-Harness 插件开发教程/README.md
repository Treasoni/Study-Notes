---
title: "DeepSeek-Harness 插件开发教程——从 apply(ctx) 到打包发布"
tags: [deepseek-harness, ai, agent, 插件, 教程, 开发]
created: 2026-08-16
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---


> [!info] 笔记信息
> - **系列归属**：DeepSeek-Harness 教程系列 · 插件开发分册
> - **笔记类型**：概念理解 + 实战（上手）
> - **读者画像**：熟悉 Claude Code 扩展体系、想写自己的 dsh 插件（工具 / 配置 / 发布）的用户
> - **预计篇幅**：约 40-50 页（中长篇分册，11 章 + 本导览）
> - **版本锚点**：developer preview（2026-08-13 锚点）
> - **分册结构**：`DeepSeek-Harness 插件开发教程/` 目录（本首页 + 00–10 章独立文件 + 11 章「写 hook 扩展点插件」子分册，由原 6 篇插件 / 配置笔记合并重构：TS 速查 + 插件开发核心 + 配置体系 + 配置实战 + 两篇实战分册）
> - **系列入口**：[[DeepSeek-Harness 教程/README|系列导览]] · [[DeepSeek-Harness MOC|教程 MOC]]

## 学习路径摘要

> 摘要取自系列大纲，先定位「我在哪、要去哪」。

### 前置要求

- 熟悉 Claude Code 扩展体系：`hooks` / `CLAUDE.md` / MCP / Skills
- 已读 [[DeepSeek-Harness 教程/DeepSeek-Harness 是什么|dsh 是什么]] 与 [[DeepSeek-Harness 教程/DeepSeek-Harness 安装与快速上手|安装与快速上手]]（源码运行路径就绪）
- 没写过 TypeScript 也不要紧：第 00 章是速查，覆盖写插件所需 TS 的 80%

### 学完能做什么

- 说清 dsh 插件的心智模型：`apply(ctx)` / fiber 生命周期 / `inject` 依赖 / `defineTool` 工具 DSL / 配置补丁树
- 从空目录**从零手写**一个带 `git_log` 工具 + `maxCommits` 可调配置的插件，走通 写 → 配 → 验证 → 打包 → 安装 全链路
- 也能从 `example-plugin` **脚手架改造**出同一个工具，两条路线共享同一基线、可互相参照
- 把现成 Claude Code 配置（rules / skills / hooks / mcp）按配置实战一章搬进 dsh

### 建议学习顺序

- **顺序通读第 01 → 02 章**（概念 + 配置理论），这是主路径的地基
- **动手从第 04 章开始**：04 先看结果与选路，05-09 是「从零写 + 脚手架改造」合并后的渐进步骤，10 收口
- 第 00 章（TS 速查）在遇到不认识的 TS 语法时当字典查；第 03 章（配置实战）在需要搬 Claude Code 配置时精读
- 预估时间：通读约 3-4 小时；动手写第一个插件另加 1-2 小时
- 每章读完建议做一次「与 Claude Code 对照」的迁移笔记，沉淀进个人 Obsidian

## 章节目录

| 章 | 笔记 | 一句话定位 |
|----|------|-----------|
| 00 | [[00-TypeScript速查-从C和Python迁移|TypeScript 速查]] | 前置：Python+C 背景读者补 TS，P0/P1/P2 + C/Python 对照表 |
| 01 | [[01-插件开发核心-从apply到system-prompt|插件开发核心]] | apply(ctx) 三形态、fiber 生命周期、inject 依赖、defineTool、hook 扩展点、system-prompt |
| 02 | [[02-配置体系-补丁树Profile与bundle|配置体系]] | 多层 YAML 补丁树、Profile 与 Agent Preset、Config schema、bundle 发布 |
| 03 | [[03-配置实战-接入skills-hooks-mcp-rules|配置实战]] | 像 Claude Code 一样接入 skills / hooks / mcp / rules |
| 04 | [[04-实战-结果预览与选路|实战：结果预览与选路]] | 8 文件户型图 / 四名分离基线 / 双起点选路（从零 vs 改造） |
| 05 | [[05-实战-起步-最小骨架与脚手架|实战：起步]] | 空目录 2 文件跑通 + 脚手架拷贝入口，看到 `plugin loaded!` |
| 06 | [[06-实战-写工具-git_log与四名分离|实战：写工具 git_log]] | 文件归属、defineTool 五件套、execute 契约、四名分离落地 |
| 07 | [[07-实战-加Config可调参数|实战：加 Config 可调参数]] | Config 两段式、默认值写 schema、patch config 传值、坏配置 fail loud |
| 08 | [[08-实战-验证命令链|实战：验证命令链]] | 加载 → dump-config → dump-default-config → headless，验证四连 |
| 09 | [[09-实战-工程化与打包发布|实战：工程化与打包发布]] | package.json / tsconfig / bundle / profile / pnpm pack / 安装 |
| 10 | [[10-小结与下一步|小结与下一步]] | 全文件清单、命令链收口、换成你自己的工具、双起点收尾 |
| 11 | [[11-实战-写hook扩展点插件/README|实战：写 hook 扩展点插件]] | 在 dsh 代码里实现 hook 扩展点：语义模型（流水线+next 瀑布）→ permission-gate → 手写 guard/post-execute/result → 验证四连 → 与 CC hooks 迁移对照（8 章子分册） |

> 建议从 [[04-实战-结果预览与选路|第四章]] 开始顺序动手，写工具时回翻 01 / 02 两章查概念，卡壳时对照 08 / 09 的验证与排查。

---

## 合并说明（2026-08-16）

本分册由原系列 6 篇插件 / 配置笔记合并重构而来，收纳为一个章节文件夹：

| 原笔记 | 去向 |
|---|---|
| `写 dsh 插件前的 TypeScript 速查` | → 第 00 章（内容原样） |
| `DeepSeek-Harness 插件开发核心` | → 第 01 章（内容原样） |
| `DeepSeek-Harness 配置体系` | → 第 02 章（内容原样） |
| `DeepSeek-Harness 配置实战` | → 第 03 章（内容原样） |
| `DeepSeek-Harness 插件实战`（脚手架改造） | → 并入 04-10 渐进路径（与从零写插件去重） |
| `DeepSeek-Harness 从零写插件` | → 并入 04-10 渐进路径（作为主干） |

原 6 篇文件已删除，所有指向它们的旧双链已改为新章节路径。
