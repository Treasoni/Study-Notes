---
title: Codex MOC
tags: [codex, ai, MOC, 索引]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# Codex MOC

> [!info] 目录导航
> **Codex 全套学习笔记**，按从入门到高级的顺序组织。共 9 篇，分 4 个层级。

---

## 📖 学习路径

```
01 入门 → 02 基础功能 → 03 进阶应用 → 04 高级功能
                ↘ 概念基础（AI学习/01-基础概念/）
```

---

## 01 入门

> 从这里开始，建立 Codex 配置体系的整体认知。

| 笔记 | 说明 |
|------|------|
| [[Codex 配置哲学概览]] | TOML vs JSON、目录结构、五层优先级 |

## 02 基础功能

> 日常使用必须掌握的核心功能。

| 笔记 | 说明 |
|------|------|
| [[config.toml 核心配置]] | 核心配置逐区块解读：sandbox、approval、permissions、profiles |
| [[Codex CLI 与调试]] | 核心命令、环境变量、配置验证与故障排查 |

## 03 进阶应用

> 掌握后可显著提升开发效率。

| 笔记 | 说明 |
|------|------|
| [[AGENTS.md 分层体系]] | 层级级联、CLAUDE.md fallback、Starlark 规则 |
| [[Skills 技能系统]] | 创建、注册、渐进加载、跨工具共享 |
| [[Agents 与 MCP]] | 子代理定义、MCP STDIO/HTTP、审批模式 |
| [[Hooks 与插件]] | 11 种生命周期事件、插件体系 |

## 04 高级功能

> 深度定制与迁移实战。

| 笔记 | 说明 |
|------|------|
| [[对照表与迁移实战]] | 21 维对照、四步迁移、陷阱与最佳实践 |
| [[快速参考卡片]] | 路径速查、命令速记、默认值 |

## 05 概念基础（交叉参考）

> 本系列笔记依赖的基础概念，位于 `AI学习/01-基础概念/`。

| 概念 | 说明 |
|------|------|
| [[Skills 是什么]] | Skills 基础概念 |
| [[SubAgent子代理]] | Subagent 基础概念 |
| [[Hook钩子]] | Hook 基础概念 |
| [[MCP协议]] | MCP 协议基础概念 |
| [[Agent智能体]] | AI Agent 通用概念 |

---

## 🗺️ 推荐阅读顺序

```
▸ 入门 + 基础功能（3 篇）
  ├── Codex 配置哲学概览        ← 从这里开始
  ├── config.toml 核心配置
  └── Codex CLI 与调试

▸ 进阶应用（4 篇）
  ├── AGENTS.md 分层体系
  ├── Skills 技能系统           ← 与 Claude Code 无缝共享
  ├── Agents 与 MCP
  └── Hooks 与插件

▸ 高级功能（2 篇）
  ├── 对照表与迁移实战          ← 从 Claude Code 迁移必读
  └── 快速参考卡片
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
