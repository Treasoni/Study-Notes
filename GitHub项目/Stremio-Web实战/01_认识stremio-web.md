---
title: "第一章：认识 stremio-web——一个不含资源的「聚合客户端」"
tags:
  - stremio
  - 影视聚合
  - Debrid
  - 4K
  - 自建媒体
created: 2026-08-26
updated: 2026-08-26
status: 进行中
source_project: stremio-web
---

# 第一章：认识 stremio-web——一个不含资源的「聚合客户端」

在动手部署之前，先回答最基础的一个问题：stremio-web 到底是什么？它和我们熟悉的影视站采集源（比如 lunatv）有什么区别？这一章讲清它的定位、三层架构，以及一个贯穿全篇的核心认知——**stremio-web 本身不含任何资源，它只是一个「聚合客户端」**。

## 1.1 项目定位：官方 Web UI

stremio-web 是 Stremio 官方出的 Web 界面，一个 React 应用，可安装为 PWA（网页应用），官方线上实例在 `web.stremio.com`（[A1]）。注意「官方 Web UI」这个定语，两层含义：

- 它是 Stremio 在浏览器里的入口，相当于桌面 app、安卓 app 的「网页表亲」；
- 官方在 alpha 开源博客里明确说过：Web 版**不是**桌面/安卓版的替代品（[A3]）。

> [!tip] 大白话
> 把 stremio-web 想成「一个空荡荡的影音大厅」——它只负责装修门面（界面、搜索、列表），但不负责往大厅里摆资源。资源要靠后面的章节里 addon 插件「接进来」。

这正是「聚合客户端」的含义：它聚合的是各种 addon 返回的流，而不是自己存片子。

## 1.2 架构：React UI ↔ stremio-core ↔ stremio-video

从仓库 README 的「How it works」看，它由三层组成（[A1]）：

```text
+------------------+      +--------------------------+      +------------------+
|   React UI       | <--> |   stremio-core           | <--> |   stremio-video  |
|  （渲染界面）     |      |   Rust 引擎 → WASM       |      |  （播放层）       |
|   管「长相」      |      |   跑在 Web Worker        |      |  按环境选播放器    |
|                  |      |   管「脑子」              |      |  管「放片」       |
+------------------+      +--------------------------+      +------------------+
```

- **React UI** 只负责「渲染状态」：页面长什么样、按钮点了什么。
- **stremio-core** 负责「计算状态」：它是 Rust 引擎编译成 WebAssembly（WASM）、跑在 Web Worker 里，处理元数据、addon 请求、播放列表等核心逻辑（[A1]）。
- **stremio-video** 是播放层抽象：根据当前环境（浏览器、桌面等）选择合适的播放器实现（[A1]）。

一句话：UI 管长相，core 管脑子，video 管放片。

**时间线差异（待核实）**：2020 年的官方博客说，非标准格式 / 本地文件 / BitTorrent 需要连接 streaming server 才能播（[A3]）；但 2026 年的 README 已经不再提 stremio-server 这回事（[A1]）。streaming server 现在是否还必需，官方口径存在差异，这里如实标注为**待核实**——后续章节实测时再确认。

## 1.3 核心认知：流是指针，不是媒体

这是全篇最重要的一句话。Stremio 官方 addon 指南的原话是：流的本质是「通往真实媒体的捷径」——addon 返回的 stream 对象里，真正指向媒体的字段是**五选一**的 `url` / `ytId` / `infoHash` / `nzbUrl` / `externalUrl`（[A2]）（[A4]）。也就是说：

- `infoHash` 只是种子的信息哈希（一串指纹），不是视频文件；
- `ytId` 只是 YouTube 视频 ID；
- `url` 只是一个 HTTP 链接。

> [!tip] 大白话
> 把流想成「一张外卖订单」：上面写着「到某某餐厅取某个菜」，但餐厅里现在有没有这个菜、菜好不好吃，订单本身不管。播放器拿着订单（指针）去取，取不取得到、画质好不好，取决于源和链路。

所以画质由「**源文件质量 + 播放/转码链路**」决定，官方对画质上限没有任何量化承诺（[A2]）（[A4]）。这也为后面章节埋下伏笔：为什么同一个 stremio-web，有时只能看 1080p，有时却能看 4K/Remux。

## 本章小结

- stremio-web 是官方 Web UI（React + PWA），线上实例在 web.stremio.com，官方明确它**不是**桌面/安卓版的替代品。
- 三层架构：React UI（渲染）↔ stremio-core（Rust→WASM，计算）↔ stremio-video（播放）。
- 2020 博客提到 streaming server，2026 README 已不提——是否仍必需**待核实**。
- **流是指针不是媒体**：addon 只返回 infoHash/url/ytId 等指针，本身不含视频。
- 画质由「源文件质量 + 播放/转码链路」决定，官方不承诺上限。

下一章我们把「选型」这件事一次做对：为什么有人装了客户端后才发现看不了 4K？Electron 打包版锁 1080p 的坑到底是怎么来的。

---

[[README|返回首页]] ｜ [[02_客户端选型|下一章]]
