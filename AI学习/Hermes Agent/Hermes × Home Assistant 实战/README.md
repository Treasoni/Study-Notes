---
title: "Hermes × Home Assistant 实战"
tags:
  - AI学习
  - Agent
  - Hermes
  - HomeAssistant
created: 2026-09-18
updated: 2026-09-18
status: 已完成
source_project: hermes-home-assistant
---

# Hermes × Home Assistant 实战

你已经让 Hermes 连上了 Home Assistant——`HASS_TOKEN` 配好、会话里四个 `ha_*` 工具能正常调用。这份分册回答的是下一步：**这四个工具究竟能把你带到哪儿、从哪一步开始必须换一条路走、换路之后哪条更值得走**。

全篇按「能力地图 → 选型 → 两条落地路线 → 事件与定时 → 安全 → 文档与代码不一致 → 成本」的顺序展开，九章正文加一个附录。两条 MCP 路线是分开写的：社区 ha-mcp 有官方模板可以照抄，HA 官方 `mcp_server` 没有 Hermes 示例、那份配置是按端点规格拼的，**性质差异在正文里逐处标注**。

## 目录

1. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/01-结论先行与能力地图|结论先行与能力地图：4 个内置工具的天花板]]
2. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/02-三方对照轴|三方对照轴：什么该交给 agent，什么本来就该用自动化]]
3. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/03-路线选型|路线选型：自建 skill / MCP server / 自定义 plugin 何时用]]
4. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/04-落地-社区ha-mcp|落地（一）：用社区 ha-mcp 接 Hermes（有官方模板，照抄即可）]]
5. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/05-落地-官方mcp_server|落地（二）：用 HA 官方 mcp_server 接 Hermes（无官方示例，拼接并标注）]]
6. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/06-事件驱动与定时任务|事件驱动与定时任务：白名单过滤、逐实体限流、投递两条分支与 4096 截断]]
7. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/07-安全与限界|安全与限界：LLT 权限真相、暴露列表的真实效力、最小化清单]]
8. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/08-文档与代码不一致|文档与代码不一致：12 条实例与自查方法]]
9. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/09-成本与可靠性|成本与可靠性：工具 schema 常驻开销、误报机理、没有分母的误报率]]
10. [[AI学习/Hermes Agent/Hermes × Home Assistant 实战/10-附录-核对清单与延伸阅读|附录：实机核对清单、未解决问题与延伸阅读]]

## 怎么读

- **只想看结论**：第 1 章给全部结论，第 2 章给「什么该交给 agent、什么该留给确定性自动化」的判据表。
- **准备动手**：第 3 章定路线，第 4 章（照抄）或第 5 章（拼接，需自行验证）落地。
- **已经跑起来了**：第 6 章讲事件与定时任务里三个文档没写透的坑；第 7 章是最小化清单。
- **在意可信度**：第 8 章把 12 处「文档和代码不一致」逐条举证；第 9 章把成本与误报率的举证性质标回原样。

关于引用纪律：每条事实性结论都标注来源档位（官方文档 / 一手源码 / 社区自报），官方原文、源码事实与本册推论分开写。附录 B 集中列出全部未解决问题及其分级——**没写死的地方没有被写死**。

## 相关笔记

- [[AI学习/Hermes Agent/Hermes Agent 上手实战/06-多平台接入与定时任务|上手实战 06：Home Assistant 双向接入]] —— LLT 怎么建、四个 `ha_*` 工具怎么用、`watch_domains` 白名单、事件转发默认全关。本册不重述，只引用。
- [[AI学习/Hermes Agent/Hermes Tool 配置指南/README|Hermes Tool 配置指南]] —— 工具怎么配、MCP 怎么接、Tool Gateway 与权限审批。
- [[AI学习/Hermes Agent/Hermes Agent MOC|Hermes Agent MOC]] —— Hermes 系列全部分册的索引。
- [[homeassistant/Home Assistant MOC|Home Assistant MOC]] —— HA 侧的部署、集成与自动化笔记。
- [[homeassistant/ai-smart-home-system/06_AI智能体FastAPI与DeepSeek|自建 AI 智能体（FastAPI + DeepSeek）]] —— 除 Hermes 与 HA 内建 LLM 之外的第三条 agent 路线，可作第 2 章对照轴的实例。
