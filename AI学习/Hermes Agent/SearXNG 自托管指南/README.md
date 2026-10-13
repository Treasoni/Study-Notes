---
title: "SearXNG 自托管指南"
tags:
  - AI学习
  - Agent
  - Hermes
  - SearXNG
  - 自托管
created: 2026-10-07
updated: 2026-10-07
status: 已完成
source_project: searxng-hermes
---

# SearXNG 自托管指南

本册讲一件事：**把 SearXNG 这个元搜索引擎自托管在你自己的机器上，再用一个环境变量 `SEARXNG_URL` 把它接给 Hermes Agent**。六章从「它是什么」一路走到「接通了、验证过、出问题知道怎么查」。

> [!summary] 一句话看懂
> SearXNG 是一个**元搜索引擎**：你把问题交给它，它替你去 Google、Bing、维基等几十个入口各问一遍，再把答案汇总回来——但那几十家看到的只是**你的实例**，不是**你**。把这份中介换成跑在**你本机 Docker** 上的一个实例，再用一个环境变量 `SEARXNG_URL` 指给 Hermes，你就得到了一个**不追踪、不画像、也不需要 API key** 的搜索后端。本册就是带你把这条路走通，从「它是什么」一直走到「接通了、验证过、知道出问题怎么查」。

## 这本册子讲什么

六章，按「是什么 → 怎么搭 → 怎么接 → 怎么验 → 还能调什么」推进。**第 2–4 章是强顺序**：端口口径（容器内 8080 / 宿主 8888）与 JSON 开关状态会在后面反复用到，跳读会让 `SEARXNG_URL` 与宿主端口对不上。

| 章 | 讲什么 | 读多久 |
| --- | --- | --- |
| 第 1 章 | SearXNG 是什么：元搜索与隐私模型 | ~5 分钟 |
| 第 2 章 | 动手：用 Docker 把 SearXNG 跑起来（两条路径） | ~20 分钟 |
| 第 3 章 | 开启 JSON API —— Hermes 的硬前提 | ~10 分钟 |
| 第 4 章 | 接入 Hermes：把搜索后端指向本地实例 | ~10 分钟 |
| 第 5 章 | 验证与排错：curl、403 与 extract 边界 | ~10 分钟 |
| 第 6 章 | 进阶可选：引擎裁剪、端口、升级与公共实例 | ~10 分钟（可跳过） |

## 目录

1. [[01-SearXNG是什么与隐私模型|第 1 章：SearXNG 是什么：一句话看懂 + 隐私模型]]
2. [[02-动手用Docker把SearXNG跑起来|第 2 章：动手：用 Docker 把 SearXNG 跑起来]]
3. [[03-开启JSON-API|第 3 章：开启 JSON API —— Hermes 的硬前提]]
4. [[04-接入Hermes|第 4 章：接入 Hermes：把搜索后端指向本地实例]]
5. [[05-验证与排错|第 5 章：验证与排错：curl、403 与 extract 边界]]
6. [[06-进阶可选|第 6 章：进阶可选：引擎裁剪、端口、升级与公共实例]]

## 阅读顺序

```
01 是什么 → 02 搭起来 → 03 开 JSON → 04 接 Hermes → 05 验证排错 → 06 进阶可选
```

- **只想尽快接上 Hermes（最省事）**：01 → 02 的**路径①** → 03 → 04 → 05。
- **想跟着上游官方走**：02 的**路径②**（双服务 `core` + `valkey`）+ 06 的升级与钉版本。
- **想调引擎/端口/公共实例**：直接看 06，前五章跑通后它是可选的。
- **只想知道为什么值得自托管**：01 + 05.4（`web_extract` 不走 SearXNG 的边界）。

## 与其他分册的关系

| 分册 | 主题 | 入口 |
|------|------|------|
| [[Hermes Agent 上手实战/README|上手实战]] | 定位、安装、模型、记忆、技能、多平台、委派、Docker 部署 | 10 章 + 附录 |
| [[Hermes Docker 部署指南/README|Docker 部署]] | Hermes 自身怎么用 Docker 常驻，以及国内消息平台接入 | 11 章 |
| **本册（SearXNG 自托管）** | 把**搜索后端**换成本地自托管实例：是什么、怎么搭、怎么接、怎么验证 | 6 章 |

本册只解决「搜索这一条链路」：SearXNG 提供搜索，Hermes 通过 `SEARXNG_URL` 消费它。它与《Docker 部署指南》互补——那册讲 Hermes 自身怎么容器化，本册讲 Hermes **依赖的一个外部服务**怎么容器化。

## 快速上手

```bash
docker compose up -d                       # 起 SearXNG 实例；配置目录已挂到宿主（第 2 章）
# 直接编辑宿主上的 settings.yml，在 search.formats 里补上 json，再重启容器（第 3 章）
curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c \
  "import sys,json; print(len(json.load(sys.stdin)[\"results\"]), 'results')"   # 第 5 章自检
# Hermes 侧：设 SEARXNG_URL 指向宿主端口，web.search_backend 设为 searxng（第 4 章）
```

## 更新记录

- **2026-10-07**：新分册《SearXNG 自托管指南》发布，6 章独立笔记 + README 入口；由 `learning-note-flow` 工作流产出（run `searxng-hermes`），并同步更新 [[Hermes Agent MOC]]。