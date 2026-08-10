---
title: DeepSeek-Reasonix 教程 MOC
tags: [deepseek-reasonix, ai, MOC, 索引]
created: 2026-08-10
updated: 2026-08-10
status: new
source_project: deepseek-reasonix-tutorial
---

# DeepSeek-Reasonix 教程 MOC

> [!info] 目录导航
> **DeepSeek-Reasonix 全套配置教程**，按从入门到精通的顺序组织。共 14 篇，分 4 个层级，风格对齐 Claude Code 教程。
> 读者定位：已熟悉 Claude Code，重点讲解安装配置、CLI 使用、成本优化与对比迁移。

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
| [[DeepSeek-Reasonix 使用指南]] | 安装 4 路径、setup 向导、第一个会话、日常速查表 |
| [[DeepSeek-Reasonix 是什么]] | 产品定位、前缀缓存原理、与 Claude Code 的关系概览 |

## 02 基础功能

> 日常使用必须掌握的核心功能。

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Reasonix CLI 完整参考]] | 命令全集、启动参数、无头/管道模式、结构化输出 |
| [[DeepSeek-Reasonix 会话与交互]] | 会话管理、斜杠命令、/init 记忆、恢复、快捷键 |
| [[reasonix.toml 配置详解]] | 配置全字段（providers/agent/tools/permissions）、优先级、API Key 安全 |
| [[DeepSeek-Reasonix 权限模式指南]] | 6 种权限模式、Shift+Tab、YOLO、fail-closed |

## 03 进阶应用

> 掌握后可显著提升开发效率。

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Reasonix 模型与运行模式]] | profile 三档、effort 推理深度、双模型协同 |
| [[DeepSeek-Reasonix MCP 使用指南]] | stdio/HTTP/SSE 三种传输、CLI 管理、配置声明 |
| [[DeepSeek-Reasonix 前缀缓存与成本优化]] | 缓存原理、三区上下文设计、命中率实测、预算控制 |
| [[DeepSeek-Reasonix 自动化与 CI]] | run 无头、json/stream-json 输出、事件遥测、CI 集成 |

## 04 高级功能

> 深度定制和大规模工作流。

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Reasonix ACP 协议指南]] | ACP v1、session 生命周期、编辑器/IDE 接入 |
| [[DeepSeek-Reasonix 插件与扩展开发]] | Extension Protocol Sidecar、插件声明与分发 |
| [[从 Claude Code 迁移到 DeepSeek-Reasonix]] | 命令/概念对照表、迁移步骤、成本对比 |
| [[DeepSeek-Reasonix 沙箱与安全]] | 沙箱（Seatbelt/bubblewrap/Windows off）、凭据保护 |

---

## 🗺️ 推荐阅读顺序

```
▸ 第一周：入门 + 基础功能（6 篇）
  ├── DeepSeek-Reasonix 使用指南       ← 从这里开始
  ├── DeepSeek-Reasonix 是什么
  ├── reasonix.toml 配置详解
  ├── DeepSeek-Reasonix CLI 完整参考
  ├── DeepSeek-Reasonix 会话与交互
  └── DeepSeek-Reasonix 权限模式指南

▸ 第二周：进阶应用（4 篇）
  ├── DeepSeek-Reasonix 模型与运行模式
  ├── DeepSeek-Reasonix MCP 使用指南
  ├── DeepSeek-Reasonix 前缀缓存与成本优化   ← 本系列特色，成本优化核心
  └── DeepSeek-Reasonix 自动化与 CI

▸ 第三周：高级功能（4 篇）
  ├── DeepSeek-Reasonix ACP 协议指南
  ├── DeepSeek-Reasonix 插件与扩展开发
  ├── DeepSeek-Reasonix 沙箱与安全
  └── 从 Claude Code 迁移到 DeepSeek-Reasonix   ← 熟悉 Claude Code 必读
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
