---
title: "Hermes Tool 配置指南"
tags:
  - AI学习
  - Agent
  - Hermes
  - 工具配置
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-tool-config
---

# Hermes Tool 配置指南

本册是《[[Hermes Agent 上手实战/README|Hermes Agent 上手实战]]》的姊妹分册，专讲 **Hermes Agent（Nous Research）的工具怎么配、怎么接**。上手实战第 5 章《技能体系》已覆盖 skill 的"是什么/生命周期"，本册不再重复；这里专注回答另一组问题：**内置工具默认开哪些？想让它搜网页、跑命令、开浏览器，该改 `config.yaml`、写 `.env` 还是跑 `hermes tools`？云能力怎么一次打通？能力不够怎么自己造 / 接 MCP？最后整机怎么锁？**

全篇 6 章，按「总览 → 内置全解 → 云能力 → 自定义 → MCP → 安全基线」推进，版本锚定 **v0.20.x**，所有键名/命令原样照抄官方文档，以 `hermes doctor` 输出为最终准绳。

## 目录

1. [[01-工具体系总览与配置入口|工具体系总览与配置入口：tool 是什么、三层配置入口]]
2. [[02-内置工具与toolsets全解|内置工具与 toolsets 全解：terminal 后端与 Docker]]
3. [[03-Tool Gateway 接入与权限审批|Tool Gateway 接入与权限审批：一次 OAuth 聚合云能力]]
4. [[04-自定义工具开发与注册|自定义工具开发与注册：registry.register 五要素]]
5. [[05-MCP 接入与排错|MCP 接入与排错：外部能力即插即用]]
6. [[06-Skills与工具关系-安全基线|Skills 与工具关系 · 安全基线]]

## 阅读顺序

```
01 总览与配置入口 → 02 内置工具全解（terminal/Docker） → 03 Tool Gateway 与审批
  → 04 自定义工具开发注册 → 05 MCP 接入排错 → 06 安全基线
```

- **只想知道怎么开工具**：读 01 + 02 就够。
- **想省掉一堆第三方 key**：03 的 Tool Gateway 一次 OAuth 打通 web 搜索 / 图像 / TTS / 云浏览器。
- **现成能力不够**：04（自己写 tool）或 05（接 MCP）二选一，先看 04.1 的 skill/tool 决策。
- **上生产前必读**：06 的安全基线 + Docker 检查清单。

## 与上手实战分册的关系

| 分册 | 主题 | 入口 |
|------|------|------|
| [[Hermes Agent 上手实战/README|上手实战]] | 定位、安装、模型、记忆、技能、多平台、委派、Docker 部署 | 10 章 + 附录 |
| **本册（工具配置）** | 工具怎么配、怎么接：内置 toolsets、Tool Gateway、自定义 tool、MCP、安全基线 | 6 章 |

两者互补：上手实战带你跑起来、学会技能体系；本册把"工具"这一层彻底打通。本册第 4 章的自定义工具开发、第 6 章的安全基线，分别与上手实战第 5 章《技能体系》、第 8 章《部署进阶》衔接。

## 快速上手

```bash
hermes tools                    # 交互式：按平台开关 toolset
hermes chat --toolsets "web,terminal,file"   # 本次会话临时带哪些工具
hermes config set terminal.backend docker    # 持久：terminal 切 docker 后端
hermes setup --portal           # 一次 OAuth 打通 Nous Provider + Tool Gateway
hermes doctor                   # 一切配置以它的输出为准
```

## 更新记录

- **2026-08-28**：新主题分册《Hermes Tool 配置指南》发布，6 章独立笔记 + README 入口；与《上手实战》第 5 章区分定位（本册专讲工具怎么配、怎么接），并同步更新 [[Hermes Agent MOC]]。
