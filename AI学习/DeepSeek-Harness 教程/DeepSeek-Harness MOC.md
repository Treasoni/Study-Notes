---
title: DeepSeek-Harness 教程 MOC
tags: [deepseek-harness, ai, MOC, 索引]
created: 2026-08-13
updated: 2026-08-13
status: new
source_project: deepseek-harness
---

# DeepSeek-Harness 教程 MOC

> [!info] 目录导航
> **DeepSeek-Harness（dsh）全套配置教程**，面向「熟悉 Claude Code 的用户」，按「快速上手 + 对照迁移」视角组织。共 5 篇独立分册 + 系列导览，零散分册模式，每篇可独立阅读。
> 读者定位：已熟悉 Claude Code，重点讲解 dsh 的定位、安装、配置体系、迁移决策与日常速查。
> 系列入口：[[DeepSeek-Harness 教程/README|系列导览]]

---

## 📖 学习路径

```
01 是什么 → 02 安装上手 → 03 配置体系 → 04 对照迁移 → 05 常见坑与速查
                                      ↘ 概念基础（AI学习/01-基础概念/）
```

---

## 分册索引

### 01 定位

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 是什么]] | 建立心智模型：Model + Harness = Agent、一切皆插件、与 Claude Code 的关系 |

### 02 安装上手

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 安装与快速上手]] | 安装三路径、Web UI 首次配置、headless 一次性任务、高频坑 |

### 03 配置体系（全书核心）

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 配置体系]] | 多层 YAML 补丁树 + Profile + Agent Preset、权限安全、模型/Provider、CLI 完整参考 |

### 04 对照迁移

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 与ClaudeCode对照迁移]] | 概念/成本/性能三张对照表、三选迁移策略、按复杂度路由建议 |

### 05 日常速查

| 笔记 | 说明 |
|------|------|
| [[DeepSeek-Harness 常见坑与速查]] | 坑清单、命令速查、V4 协议坑、生态资源与下一步 |

---

## 🗺️ 推荐阅读顺序

```
▸ 主路径（约 2.5–3.5 小时）
  ├── DeepSeek-Harness 是什么          ← 建立心智模型
  ├── DeepSeek-Harness 安装与快速上手   ← 5 分钟跑通
  ├── DeepSeek-Harness 配置体系        ← 全书核心，篇幅最长
  ├── DeepSeek-Harness 与ClaudeCode对照迁移  ← 换还是留
  └── DeepSeek-Harness 常见坑与速查     ← 日常速查

▸ 急用路径
  ├── 安装与快速上手  → 跑通环境
  ├── 与ClaudeCode对照迁移 → 做「换还是留」决策
  └── 回头补 配置体系 + 常见坑与速查
```

---

## 相关索引

- [[AI学习 MOC]] — 整个 AI 学习目录的总入口
- [[Claude Code MOC]] — 对照迁移的参照系列
