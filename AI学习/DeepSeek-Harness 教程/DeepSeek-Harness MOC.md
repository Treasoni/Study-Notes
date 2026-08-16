---
title: DeepSeek-Harness 教程 MOC
tags: [deepseek-harness, ai, MOC, 索引]
created: 2026-08-13
updated: 2026-08-16
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 教程 MOC

> [!info] 目录导航
> **DeepSeek-Harness（dsh）插件开发教程**，面向「熟悉 Claude Code 的用户」，以「写自己的 dsh 插件」为主线。共 4 篇主章分册 + 1 篇插件开发分册（00-11 章）+ 1 篇子系统开发分册 + 系列导览，零散分册模式，每篇可独立阅读。
> 读者定位：已熟悉 Claude Code，用其扩展体系（hooks / CLAUDE.md / MCP / Skills）作桥，讲解 dsh 插件开发。
> 系列入口：[[DeepSeek-Harness 教程/README|系列导览]]

---

## 📖 学习路径

```
01 心智模型 → 02 环境准备 → 03 插件开发核心 → 04 实战项目 → 05 速查与排错
                                        （03 插件开发分册 00-11 章：速查/核心/配置/实战路径 + 写 hook 扩展点插件）
                                        （06 子系统开发：Subagent 能力缝 + provider）
                                            ↘ 概念基础（AI学习/01-基础概念/）
```

---

## 分册索引

### 00 前置准备

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 插件开发教程/00-TypeScript速查-从C和Python迁移|TypeScript 速查]] | 前置速查：Python+C 背景读者补 TS，P0/P1/P2 + C/Python 对照表 |

### 01 心智模型

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 是什么]] | 插件树 vs 单体 + 扩展：Model+Harness=Agent、一切皆插件、Claude Code 扩展模型对照表 |

### 02 环境准备

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 安装与快速上手]] | 源码运行路径（写插件前提）、Web UI 首配、headless 验证、npm 快跑边界 |

### 03 插件开发核心（全书核心）

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 插件开发教程/README\|DeepSeek-Harness 插件开发]] | 插件开发分册（00-11 章）：00 前置 TS 速查 · 01 核心（apply 三形态/生命周期/inject/defineTool/hook/提示词）· 02-03 配置专册（补丁树/Profile 与 Agent Preset/Config schema/bundle 发布/接入 skills-hooks-mcp-rules）· 04-10 实战渐进路径（git_log 写→配→验证→打包→安装，改造/从零双入口）· 11 写 hook 扩展点插件（8 章子分册） |

### 04 实战项目

| 笔记 | 说明 |
|------|------|
| 04·A [[DeepSeek-Harness 与ClaudeCode对照迁移]] | 写插件实战：从零写自定义工具插件 walkthrough，骨架→greet→repo_status→配置→打包，每步对照 Claude Code |

### 05 速查与排错

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 常见坑与速查]] | 插件开发高频坑、命令速查（含 dsh plugin 全家族）、工具契约、配置引用、模型协议参考、生态 |

### 06 子系统开发

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness Subagent 教程/README\|DeepSeek-Harness Subagent 开发]] | 子系统开发：subagent 能力缝与三层结构、ctx.subagents 契约、写自己的 provider（三段式）、one-shot/continuable、工具化暴露，7 章概念+实战分册 |

---

## 🗺️ 推荐阅读顺序

```
▸ 主路径（约 3.5–4.5 小时）
  ├── DeepSeek-Harness 是什么          ← 转心智模型（插件树 vs 单体+扩展）
  ├── DeepSeek-Harness 安装与快速上手   ← 源码环境，5 分钟跑通
  ├── DeepSeek-Harness 插件开发        ← 核心+配置+实战：00 速查 → 01 核心 → 02-03 配置 → 04-10 渐进路径
  ├── DeepSeek-Harness 与ClaudeCode对照迁移  ← 实战：写第一个自定义工具插件
  ├── DeepSeek-Harness Subagent 开发    ← 进阶：写 subagent 能力缝（provider + 工具），概念+实战
  └── DeepSeek-Harness 常见坑与速查     ← 日常速查

▸ 急用路径
  ├── 安装与快速上手  → 跑通源码环境
  ├── 与ClaudeCode对照迁移 → 照猫画虎写第一个工具
  ├── 配置实战 → 把现成 Claude Code 配置搬进 dsh
  └── 回头补 插件开发分册 + 常见坑与速查
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
- [[Claude Code MOC]] — 本系列用作桥接的参照系列
