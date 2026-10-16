---
title: qBittorrent 配置与使用（总览）
aliases:
  - qBittorrent 配置与使用
  - qBittorrent 教程
  - qBittorrent 上册
tags:
  - 流媒体
  - qBittorrent
  - fnOS
  - Docker
  - BT下载
  - 入门教程
created: 2026-10-07
updated: 2026-10-16
status: active
source_project: qbittorrent-config-usage
---

# qBittorrent 配置与使用（总览）

> [!summary] 一句话看懂
> qBittorrent 是家庭影院里的**「后厨」**——把种子 / 磁力链接变成硬盘上文件的 BT 下载器。这套分册补上上级分册留下的缺口：**上级分册只把 qBittorrent 当「前提条件」列出，从没教它怎么装、怎么配**；本分册用三册把这段补透：装起来 → 配好 → 用起来。

## 三册目录

1. [[流媒体与影音/qBittorrent 配置与使用/01 qBittorrent 是什么与装起来|上册 · qBittorrent 是什么与装起来（第 1–2 章）]]
   - 第 1 章 它是什么、在家庭影院里的位置（BT/P2P、Tracker、`info_hash` 名词扫盲）
   - 第 2 章 装起来：镜像三选一、卷映射、首次登录口令（含可照抄的两版 `docker-compose.yml`）
2. [[流媒体与影音/qBittorrent 配置与使用/02 qBittorrent 配好|中册 · qBittorrent 配好（第 3–4 章）]]
   - 第 3 章 配好（上）：四条路径 + BT 端口映射、改端口「两侧同改」、硬链接的目录口径
   - 第 4 章 配好（下）：分类 / 标签、队列 / 限速、代理，以及完成回调（通知 MoviePilot 整理）
3. [[流媒体与影音/qBittorrent 配置与使用/03 qBittorrent 用起来|下册 · qBittorrent 用起来（第 5–6 章）]]
   - 第 5 章 加种、Tracker、DHT/PeX/LPD 与 RSS
   - 第 6 章 分享率、H&R 与「没速度」按官方清单自查

## 先读哪一册

| 你的情况 | 建议 |
| --- | --- |
| 完全没装过 | 按 上册 → 中册 → 下册 顺序通读 |
| 容器已在跑，只想接进家庭影院 | 直接读 **中册第 3–4 章**（目录口径 + 完成回调） |
| 已是老手，卡在「没速度」 | 直接读 **下册第 6 章**（按官方清单自查） |

## 与上级分册的关系

本分册是 [[流媒体与影音/nastool 家庭影院 fnOS 部署/在飞牛 fnOS 上搭建 nastool 家庭影院（总览）|《nastool 家庭影院 fnOS 部署》]] 的配套缺口篇：

- 上级分册 [[流媒体与影音/nastool 家庭影院 fnOS 部署/03 动手前的准备|第 3 章 动手前的准备]] 只给出 qBittorrent 的**最低版本要求**（`>= 4.3.9`）；
- 上级分册 [[流媒体与影音/nastool 家庭影院 fnOS 部署/07 对接下载器与媒体服务器|第 7 章 对接下载器与媒体服务器]] 只给**两行对接配置**（下载目录映射、完成回调填 `curl`）；
- 本分册补的正是「**怎么装、怎么配、怎么用**」这段被跳过的内容，并与上级分册的对接口径保持一致（下载目录同根、完成回调）。

> [!note] 另有一组更早的散记（已归档）
> 本目录下的 `旧散记/` 子文件夹里是四篇更早的散记（2026-02 ~ 2026-04）：[[流媒体与影音/qBittorrent 配置与使用/旧散记/qBittorrent的使用|qBittorrent 使用指南]]、[[流媒体与影音/qBittorrent 配置与使用/旧散记/qBittorrent配置代理|qBittorrent 代理配置指南]]、[[流媒体与影音/qBittorrent 配置与使用/旧散记/qBittorrent的Tracker|qBittorrent Tracker 配置详解]]、[[流媒体与影音/qBittorrent 配置与使用/旧散记/qBittorrent PT站点与分享率|qBittorrent PT 站点与分享率管理]]。
> 它们**已归档、不再维护**，只在翻历史细节时作补充参考；版本号、字段取值、站点规则一律**以本分册为准**（四篇各自的过时点已写在各自文首的归档提示里）。

> [!warning] 边界：通用机制 ≠ 某站规则
> 「私种关 DHT / PeX / LPD」「分享率 / H&R 的阈值 / 最低做种时长」在本分册里讲的都是**通用机制**，**不是 qBittorrent 的官方规定，也不是某个站的规则**。**具体是否要关、阈值是多少，一律以你目标站的 rules / FAQ 为准**——本分册不给任何站的达标线。

---

## 更新记录

| 日期 | 变更 | 来源 |
| --- | --- | --- |
| 2026-10-16 | 「另有一组更早的散记」改为 `旧散记/` 双链 + 归档口径；旧散记迁入本目录并标记归档 | `workspace/qbittorrent-config-usage/updates/01/update_report.md` |
