---
title: Claude Code 教程 MOC
tags: [claude-code, ai, MOC, 索引]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: claude-code-tutorial
---

# Claude Code 教程 MOC

> [!info] 目录导航
> **Claude Code 全套学习笔记**，按从入门到精通的顺序组织。共 19 篇，分 4 个层级。

---

## 📖 学习路径

```
01 入门 → 02 基础功能 → 03 进阶应用 → 04 高级功能
                ↘ 概念基础（AI学习/01-基础概念/）
```

---

## 01 入门

> 从这里开始，安装、配置、跑通第一个会话。

| 笔记 | 说明 |
|------|------|
| [[如何使用Claude code]] | 安装、免登录、配置、日常速查、记忆系统 |

## 02 基础功能

> 日常使用必须掌握的核心功能。

| 笔记 | 说明 |
|------|------|
| [[Claude Code 常用功能]] | 功能速查手册：快捷键、Slash 命令、文件操作、Git |
| [[Claude Code CLI 完整参考]] | CLI 启动参数、环境变量、管道模式 |
| [[Claude Code 会话管理]] | 上下文管理、会话恢复、配置优先级 |
| [[Claude Code 模型与推理设置]] | 模型选择、Effort Level、第三方平台配置 |
| [[settings.json 配置详解]] | 核心配置文件字段完整说明 |

## 03 进阶应用

> 掌握后可显著提升开发效率。

| 笔记 | 说明 |
|------|------|
| [[Claude Code Memory 完整指南]] | CLAUDE.md + Auto Memory + 参考文档三层体系 |
| [[Claude Code Subagents 完整指南]] | Subagent 创建/配置/实战，含设计模式与练习 |
| [[Claude Code Hooks 使用指南]] | 事件驱动自动化：PreToolUse、PostToolUse、Stop |
| [[Claude Code Checkpoints 使用指南]] | 时光机回滚：Rewind、对话恢复、代码还原 |
| [[Claude Code 插件系统使用指南]] | 插件安装、结构、自定义插件开发 |

## 04 高级功能

> 深度定制和大规模工作流。

| 笔记 | 说明 |
|------|------|
| [[Claude Code 高级功能]] | 总览：Planning Mode、Auto Mode、沙盒、桌面应用 |
| [[Claude Code Slash Commands 完整参考]] | 所有内置 Slash 命令 + 自定义命令编写 |
| [[Claude MCP 使用指南]] | MCP 协议：连接外部工具和数据源 |
| [[如何编写Skills]] | 自定义技能：编写、发布、渐进式披露 |
| [[CLAUDE.md 使用指南]] | 项目记忆文件编写与最佳实践 |
| [[Claude Code 定时任务自动化指南]] | Cron/loop/launchd 定时调度 |
| [[Claude Code Dynamic Workflows 使用指南]] | 多 Agent 编排：6 种模式、JS 脚本生成 |
| [[LLM-Prompt-Caching-提示缓存]] | 缓存原理、命中优化、成本节省 |

## 05 概念基础（交叉参考）

> 本系列笔记依赖的基础概念，位于 `AI学习/01-基础概念/`。

| 概念 | 说明 |
|------|------|
| [[Skills 是什么]] | Skills 基础概念 |
| [[SubAgent子代理]] | Subagent 基础概念 |
| [[Hook钩子]] | Hook 基础概念 |
| [[MCP协议]] | MCP 协议基础概念 |
| [[Agent Teams智能体团队]] | Agent Teams 基础概念 |
| [[Agent智能体]] | AI Agent 通用概念 |
| [[人工智能重要的六大概念体系]] | AI 学习知识框架 |
| [[Prompt提示词]] | Prompt 工程基础 |

---

## 🗺️ 推荐阅读顺序

```
▸ 第一周：入门 + 基础功能（6 篇）
  ├── 如何使用Claude code         ← 从这里开始
  ├── settings.json 配置详解
  ├── Claude Code 常用功能
  ├── Claude Code CLI 完整参考
  ├── Claude Code 会话管理
  └── Claude Code 模型与推理设置

▸ 第二周：进阶应用（5 篇）
  ├── Claude Code Memory 完整指南
  ├── Claude Code Subagents 完整指南   ← 最重要，含实战
  ├── Claude Code Hooks 使用指南
  ├── Claude Code Checkpoints 使用指南
  └── Claude Code 插件系统使用指南

▸ 第三周：高级功能（8 篇）
  ├── Claude Code 高级功能          ← 先看总览
  ├── Claude Code Slash Commands 完整参考
  ├── Claude MCP 使用指南
  ├── 如何编写Skills
  ├── CLAUDE.md 使用指南
  ├── Claude Code 定时任务自动化指南
  ├── Claude Code Dynamic Workflows 使用指南
  └── LLM-Prompt-Caching-提示缓存
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
