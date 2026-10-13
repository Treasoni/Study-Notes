---
title: 第 2 章 为什么主线是 MoviePilot V3（原版 nastool 已成历史）
tags:
  - 流媒体
  - MoviePilot
  - nastool
  - Docker
  - 入门教程
created: 2026-10-07
updated: 2026-10-07
status: draft
source_project: nastool-fnos-deploy
---

# 第 2 章 为什么主线是 MoviePilot V3（原版 nastool 已成历史）

> [!summary] 一句话看懂
> 原版 **nastool 仓库已于 2023 年归档、只读**，作者把它重做成了 **MoviePilot**；现在的主线是 **V3**。而且 V3 改了初始化方式——**首次进网页自己建管理员**，网上旧教程照抄 V2 写法，会在「找初始密码」这步卡死。

这一章解决两个问题：**为什么不再讲 nastool 原版**（最短交代，不展开沿革），以及**提前拆掉一个照抄陷阱**（V2 口径的 Compose 会让你在 V3 上卡在初始化）。看完这一章，你在第 4 章照做时就不会被旧教程带偏。

## 2.1 原版 nastool 的结局：归档、只读、旧地址 404

三句话说完：

- 原版仓库 `NAStool/nas-tools` 已被作者归档，仓库页横幅明确写着：归档于 2023-05-16，现为只读[^c2-arch]。
- 它的旧地址 `jxxghp/nas-tools` 现在打开是 404——页面标题就是 GitHub 的「`Page not found`」（页面未找到）[^c2-404]。
- 所以任何「照 nastool 装」的老教程，本质是在教一个**已停更两年多**的软件——我们不跟。

这里不展开它的历史沿革。你只需要记住：**nastool 原版是上一代——看它了解背景可以，照它部署不行。**

## 2.2 同作者的换代：MoviePilot 是什么定位

MoviePilot 是同一作者基于 nastool 部分代码**重新设计**的作品，官方自述的定位是「聚焦自动化核心需求，减少问题、更易于扩展和维护」[^c2-readme-1]。

| 它的定位 | 官方原文 | 说人话 |
| --- | --- | --- |
| 自述定位 | 「基于 NAStool 部分代码重新设计，聚焦自动化核心需求，减少问题同时更易于扩展和维护。」 | 不是从零新写，而是把 nastool 拆解重做：砍掉杂项，只留自动化主线。 |

**一句话概括**：MoviePilot 是 nastool 的「重制版」，主线职责就是影视自动化。

它的 Docker 镜像也和旧版分开命名——V3 用独立镜像 `jxxghp/moviepilot-v3`，V2 和旧版镜像保持原名[^c2-readme-2]。**标准 V3 是普通用户的默认选择**[^c2-v2v3]。

## 2.3 V2 → V3 的分水岭：初始化方式变了

这是本章最实用的一节。V2 和 V3 最大的区别不在功能，而在**「管理员账号从哪来」**：

- **V2 的老做法**：在环境变量里预先写好超级管理员用户名 / 密码（`SUPERUSER` / `SUPERUSER_PASSWORD`），甚至预先填好 `API_TOKEN`。
- **V3 的新做法**：**什么都不预置**。首次打开网页时，系统进入初始化页面，你现场填管理员用户名、密码（填两次）并生成 API Key，保存后才跳到登录页[^c2-install-1]。

> [!warning] V3 模板里不需要这些变量
> V3 全新安装时，Docker 模板中**不需要**填写 `SUPERUSER`、`SUPERUSER_PASSWORD`、`API_TOKEN`[^c2-install-2]。这三个是 V2 口径，写到 V3 里没用。

## 2.4 照抄陷阱对照：「V2 式」写法 vs V3 正确写法

网上大量视频 / 博客的 Compose 仍是 **V2 口径**。照抄到 V3 上，最常见的结果是「容器起来了，但不知道密码是什么」——因为在 V3 里，你写进去的 `SUPERUSER_PASSWORD` 根本不会被当作初始密码。

| 你看到的旧教程（V2 口径） | V3 应该怎么做 |
| --- | --- |
| 环境变量写 `SUPERUSER=admin` / `SUPERUSER_PASSWORD=你的初始登录密码` | **删掉，别写**；改为首次访问网页时手动创建管理员 |
| 环境变量写 `API_TOKEN=建议大于16位的复杂字符串` | **删掉**；API Key 在首次初始化时自动生成并展示 |
| 「第一次启动去日志里搜『超级管理员』找密码」 | V3 **没有这一步**：密码是你自己首次访问时设的 |

> [!note] 为什么 V2 要预置、V3 不用
> V2 把初始化摊在「启动阶段」——启动前就得把账号密码灌进去；V3 把它挪到「首次访问」——容器先干干净净跑起来，你进网页再设。**这处改动，正是「照抄旧教程会卡死」的根源。**

> [!tip] 大白话
> 把初始化想成**新手机开箱**：V2 相当于「出厂就把你的名字和密码刻在机身上」；V3 相当于「出厂是空白的，开机第一屏让你自己设」。你要是拿着 V2 的「刻名字清单」去挑 V3 的手机，当然找不到该填哪儿。

**下一章预告**：知道主线是 V3 之后，动手前还有三件事必须先想清楚——网络通不通、目录怎么规划（直接决定硬链接成不成立）、配套软件装哪些。下一章就讲这三件事。

---

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与对照如下；英文引文给出中译，中文引文的「中译 / 说人话」列给的是说人话的复述。「出处」列写不出具名来源的记 `—`；产品文件名不是来源件，不列为出处。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `This repository was archived by the owner on May 16, 2023. It is now read-only.` | 该仓库已由所有者于 2023 年 5 月 16 日归档，现为只读。 | `sources/gh/nastool_repo_page.html` |
| 2 | `Page not found · GitHub · GitHub` | 页面未找到 · GitHub | `sources/gh/nas-tools_github_page_status.txt` |
| 3 | `基于 NAStool 部分代码重新设计，聚焦自动化核心需求，减少问题同时更易于扩展和维护。` | 基于 NAStool 部分代码重新设计，聚焦自动化核心需求 | `sources/gh/MoviePilot_v3_README.md:15` |
| 4 | ``推荐优先使用 Docker 部署。V3 使用独立镜像 `jxxghp/moviepilot-v3`，V2 和旧版镜像保持原命名。`` | 推荐优先用 Docker 部署；V3 用独立镜像，V2 与旧版镜像保持原名 | `sources/gh/MoviePilot_v3_README.md:30` |
| 5 | `标准 V3 是普通用户的默认选择。` | 标准 V3 是普通用户默认该选的版本 | `sources/gh/v2-to-v3-overview.md:465` |
| 6 | `V3 全新启动不会预置管理员用户、密码或 API Key，首次访问 Web 地址时会进入初始化页面，填写管理员用户名、密码（需确认两次）并生成 API Key 后保存，再跳转到登录页面。` | V3 首次启动不预置管理员 / 密码 / API Key，首次访问网页进初始化页自建管理员 | `sources/wiki/install.txt:40` |
| 7 | `V3 全新安装无需在 Docker 模板中填写 SUPERUSER、SUPERUSER_PASSWORD 或 API_TOKEN：首次访问 Web 地址会进入初始化页面，保存后才会写入管理员账号、密码和 API Key。` | V3 模板不用填 SUPERUSER / SUPERUSER_PASSWORD / API_TOKEN | `sources/wiki/install.txt:456-464` |

[^c2-arch]: GitHub · `NAStool/nas-tools` 仓库页（归档横幅）— [github.com/NAStool/nas-tools](https://github.com/NAStool/nas-tools)
[^c2-404]: GitHub · 旧地址 404 存证 — [github.com/jxxghp/nas-tools](https://github.com/jxxghp/nas-tools)
[^c2-readme-1]: MoviePilot 仓库 README（v3 分支）— [raw.githubusercontent.com/jxxghp/MoviePilot/v3/README.md](https://raw.githubusercontent.com/jxxghp/MoviePilot/v3/README.md)
[^c2-readme-2]: MoviePilot 仓库 README（v3 分支，安装使用）— 同上
[^c2-v2v3]: MoviePilot · V2 到 V3 变化总览（仓库内）— [docs/v2-to-v3-overview.md](https://github.com/jxxghp/MoviePilot/blob/v3/docs/v2-to-v3-overview.md)
[^c2-install-1]: MoviePilot Wiki · 安装指引 — [wiki.movie-pilot.org/install](https://wiki.movie-pilot.org/install)
[^c2-install-2]: MoviePilot Wiki · 安装指引（V3 模板说明）— 同上
