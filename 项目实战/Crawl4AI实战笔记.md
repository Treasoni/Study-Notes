---
title: WebFetch vs Skill vs MCP 概念辨析与开源工具选型
tags:
  - Claude Code
  - MCP
  - Skill
  - WebFetch
  - 资料收集
  - 工具选型
created: 2026-08-14
updated: 2026-08-14
status: 已完成
source_project: study-system
---

# WebFetch vs Skill vs MCP 概念辨析与开源工具选型

> [!summary]
> 本次会话两件事：① 厘清 WebFetch / Skill / MCP 三者的定位区别；② 为本项目（学习笔记自动化系统）选定资料收集与 AI/Agent 工作流方向的开源工具。

## 核心概念：WebFetch vs Skill vs MCP

> [!note] 三者不是同层级的"三个选项"，而是「零件 / 流程 / 扩展能力」的关系

| | 定位 | 类比 |
|---|---|---|
| **WebFetch** | Claude Code 内置的单步工具：抓单个 URL → 转 Markdown → 小模型回答 | 一把螺丝刀 |
| **Skill** | 打包的方法论 + 流程 + 项目规范，内部编排多个工具 | 说明书 + 整个工具箱 |
| **MCP** | 协议，把外部工具/数据源接进 Claude Code，扩展原生没有的能力 | 新买的电动工具 |

关键认知：

- **Skill 内部会调用 WebFetch**——`research-collector` 的精读阶段（Phase 2）就是用 WebFetch 深读的，所以不是"二选一"
- WebFetch 只管"读某个确定 URL"，不做搜索、去重、过滤、综合、落盘
- Skill 解决的是"从**未知位置**系统性找资料"，还有 token 优化（隔离 subagent + 150 字摘要约束）
- MCP 解决的是 WebFetch 做不到的能力：JS 动态渲染、登录态、真实浏览器 DOM、调 API

选型建议：已知 URL 快读 → WebFetch；系统性研究 → research-collector；动态页/认证/数据库 → MCP。

## 开源项目选型

按选定方向「**资料收集/研究工具** + **AI/Agent 工作流工具**」检索后选出：

### 资料收集 / 研究工具

| 项目 | 落点 |
|---|---|
| **Crawl4AI** | 强化 research-collector 精读：批量并发、干净 Markdown、结构化提取、本地缓存（最终选定） |
| **Trafilatura** | 轻量正文净化，不想上重型爬虫时的备选 |
| **Firecrawl** | 自托管 API 服务，自带反爬，可作 MCP 接入 |
| **RSSHub** | 万物转 RSS，配合 [[N8N定时抓取热点资讯指南]] 扩展数据源 |
| **ScrapeGraphAI** | AI 驱动爬虫，自然语言指定提取字段的备选 |

### AI / Agent 工作流工具

| 项目 | 落点 |
|---|---|
| **anthropics/skills** | 官方 skills 仓库，用其最佳实践复盘本项目 50+ 自定义 skill |
| **fastmcp** | Python 构建 MCP server，可把收集逻辑包装成自建 MCP |
| **playwright-mcp** | 浏览器自动化 MCP，和现有 `browser-cdp` 互补/替代 |
| **DeerFlow** | 深度研究多智能体框架，作为**架构参考**（非替换） |
| **context7** | 给 LLM 提供最新库文档，写技术笔记时降低幻觉 |
| **awesome-mcp-servers** | MCP 生态目录索引 |

> [!tip] 落地优先级
> ① Crawl4AI（质变）→ ② anthropics/skills（审 skill 体系）→ ③ playwright-mcp 或 fastmcp（二选一）。RSSHub 是零改代码的补充。
