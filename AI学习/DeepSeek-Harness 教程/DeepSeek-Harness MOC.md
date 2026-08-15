---
title: DeepSeek-Harness 教程 MOC
tags: [deepseek-harness, ai, MOC, 索引]
created: 2026-08-13
updated: 2026-08-15
status: updated
source_project: deepseek-harness
---

# DeepSeek-Harness 教程 MOC

> [!info] 目录导航
> **DeepSeek-Harness（dsh）插件开发教程**，面向「熟悉 Claude Code 的用户」，以「写自己的 dsh 插件」为主线。共 5 篇主章分册 + 2 篇配置专册 + 1 篇实战分册 + 系列导览，零散分册模式，每篇可独立阅读。
> 读者定位：已熟悉 Claude Code，用其扩展体系（hooks / CLAUDE.md / MCP / Skills）作桥，讲解 dsh 插件开发。
> 系列入口：[[DeepSeek-Harness 教程/README|系列导览]]

---

## 📖 学习路径

```
01 心智模型 → 02 环境准备 → 03 插件开发核心 → 04 实战项目 → 05 速查与排错
                                        （03/04 各含 1 篇配置专册；04 另含 1 篇实战分册）
                                            ↘ 概念基础（AI学习/01-基础概念/）
```

---

## 分册索引

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
| [[DeepSeek-Harness 插件开发核心]] | apply(ctx) 三形态、fiber 生命周期、inject 依赖、defineTool 工具 DSL、hook 扩展点、system-prompt 子系统 |
| [[DeepSeek-Harness 配置体系]]（配套专册） | 配置：多层 YAML 补丁树、Profile 与 Agent Preset、Config schema、bundle 发布 |

### 04 实战项目

| 笔记 | 说明 |
|------|------|
| 04·A [[DeepSeek-Harness 与ClaudeCode对照迁移]] | 写插件实战：从零写自定义工具插件 walkthrough，骨架→greet→repo_status→配置→打包，每步对照 Claude Code |
| 04·B [[DeepSeek-Harness 配置实战]] | 配置接入实战：像 Claude Code 一样接入 skills/hooks/mcp/rules，rules/skills 零迁移，hooks/mcp 走 cordis.yml |
| 04·C [[DeepSeek-Harness 插件实战]] | 实战分册：把 example-plugin 脚手架改造成你自己的工具（git_log），走通写→配→验证→打包→安装全链路 |

### 05 速查与排错

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 常见坑与速查]] | 插件开发高频坑、命令速查（含 dsh plugin 全家族）、工具契约、配置引用、模型协议参考、生态 |

---

## 🗺️ 推荐阅读顺序

```
▸ 主路径（约 2.5–3.5 小时）
  ├── DeepSeek-Harness 是什么          ← 转心智模型（插件树 vs 单体+扩展）
  ├── DeepSeek-Harness 安装与快速上手   ← 源码环境，5 分钟跑通
  ├── DeepSeek-Harness 插件开发核心    ← 全书核心，篇幅最长
  ├── DeepSeek-Harness 配置体系        ← 配置专册（读核心时配套查）
  ├── DeepSeek-Harness 与ClaudeCode对照迁移  ← 实战：写第一个自定义工具插件
  ├── DeepSeek-Harness 配置实战        ← 实战：接入现成 skills/hooks/mcp/rules
  ├── DeepSeek-Harness 插件实战        ← 实战：把脚手架改造成自己的工具并打包发布
  └── DeepSeek-Harness 常见坑与速查     ← 日常速查

▸ 急用路径
  ├── 安装与快速上手  → 跑通源码环境
  ├── 与ClaudeCode对照迁移 → 照猫画虎写第一个工具
  ├── 配置实战 → 把现成 Claude Code 配置搬进 dsh
  └── 回头补 插件开发核心 + 配置体系 + 常见坑与速查
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
- [[Claude Code MOC]] — 本系列用作桥接的参照系列
