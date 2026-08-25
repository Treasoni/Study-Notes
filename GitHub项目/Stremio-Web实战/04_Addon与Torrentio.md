---
title: "第四章：Addon 机制与 Torrentio——给 Stremio 接上影视资源"
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

# 第四章：Addon 机制与 Torrentio——给 Stremio 接上影视资源

上一章我们把 stremio-web 跑起来了，但打开界面你会发现：**空荡荡，啥都没有**。这不是 bug——Stremio 本身不含任何资源，它只是一台「空播放器」。本章要回答的问题是：资源到底从哪来？答案是 addon（插件）。我们先讲清 addon 返回的 stream 对象到底是什么，再用最常用的 Torrentio 把影视资源真正接进来。

## 4.1 Addon 机制与 stream 对象

Addon 是 Stremio 生态的「内容供应商」，负责提供三类数据：目录（Catalog）、元数据（Meta）和流（Stream）。其中「流」是播放的入口，也是本节的重点。

### 4.1.1 流是指针，不是媒体

Stremio 官方指南有一句非常关键的话：**「streams are just shortcuts to the real media」——流只是通往真实媒体的快捷方式**（[A2]）。addon 不会把视频文件打包发给你，它只返回一个「指向」：告诉 Stremio 这个视频在哪、怎么取。

> [!tip] 大白话
> 把 stream 想成一张写着「收货地址」的便条，而不是货本身。addon 只负责给你地址，真正去取货的是播放器/下载器。所以 addon 可以做得非常轻——它手里永远没有视频文件。

### 4.1.2 stream 对象的五个指向字段

既然是指针，就必须有个「指到哪」的字段。根据 stream 对象规范，下面五个字段**五选一，必须有一个**（[A4]）：

| 字段 | 含义 |
|------|------|
| `url` | 直接的视频文件链接（HTTP/HTTPS） |
| `ytId` | YouTube 视频 ID |
| `infoHash` | torrent 的 info hash，配合 `fileIdx` 定位种子里的文件 |
| `nzbUrl` | Usenet 的 NZB 文件链接 |
| `externalUrl` | 外部播放地址（如跳转到第三方网页） |

对应到 Torrent 场景，最关键的是 `infoHash`——它相当于种子的「身份证号」，播放器靠它去 P2P 网络或 Debrid 服务里找到文件。

### 4.1.3 辅助字段：fileIdx、name、behaviorHints

光有 infoHash 还不够，一个种子包里往往有好几个视频文件。这时用 `fileIdx` 指定要第几个文件（下标从 0 开始）；**省略时 Stremio 默认取体积最大的那个文件**（[A4]）——通常就是主影片。

画质信息放在 `name` 字段里（官方明确它「usually used for stream quality」，常写成 4K / 1080p / HEVC 等）；具体描述放 `description`。旧的 `title` 字段已弃用（[A4]）。

还有个细节：`behaviorHints.notWebReady`。当 `url` 是**非 HTTPS 或非 MP4 的 HTTP 直链**时，要把它设为 `true`，告诉 Stremio 这个链接需要额外处理（比如走代理或转码），否则可能无法直接播放（[A4]）。

一个最小的 Torrent stream 对象长这样：

```json
{
  "name": "4K",
  "infoHash": "0123456789abcdef0123456789abcdef01234567",
  "fileIdx": 0
}
```

> [!tip] 大白话
> 把 infoHash 想成「门牌号」，fileIdx 想成「这栋楼里的第几层」。addon 只告诉你「门牌号 + 楼层」，至于楼里有没有货、怎么搬运，那是 Stremio 和播放器的事。

## 4.2 Torrentio 三步接入

理解了 stream 协议，下一步就是用一个真正产出这些流的 addon。**Torrentio** 是最流行的 torrent 资源聚合 addon，会从多个源抓取种子，转成 Stremio 认识的 stream 列表。

**第一步：打开配置页** `https://torrentio.strem.fun/configure`（[B2/C1]）。

**第二步：设置三个关键参数**：

| 参数 | 作用 | 建议 |
|------|------|------|
| Debrid Provider | 是否接 Debrid 服务商（RealDebrid / Premiumize / AllDebrid 等），默认 None | 追求高质量选 RealDebrid，下一章细讲；先用 None 体验 P2P |
| Exclude Resolutions | 排除指定分辨率，如排除 720p 以下 | 想要高清就排除低分辨率 |
| Video Size Limit | 文件大小上限，`5GB` 或逗号分隔 `10GB,2GB` | **第一个=电影、第二个=剧集**（[B2/C1]） |

例如想看高清电影又不介意大文件，可以填 `10GB,2GB`：电影过滤 10GB 以内的、剧集过滤 2GB 以内的。

**第三步：装进 Stremio**。配置页底部有 `INSTALL` 和 `Copy Link` 两个按钮：`INSTALL` 会直接推送到已连接的 Stremio 客户端；`Copy Link` 复制链接后，在 Stremio 的「Addons → Install from URL」里粘贴安装。装完打开任意影视条目，就能看到 Torrentio 返回的流列表了。

## 4.3 常见坑

**坑一：别勾选「Don't show download to debrid links」。** 2024 年 11 月，Real-Debrid 移除了「检查已缓存 info hash」的接口，Torrentio 无法再精确判断哪些种子能秒播，只能靠一个 8 小时短期缓存兜底，并把所有链接统一标记为 `[RD download]`（[C2]）。如果你在配置页勾选了「不显示需要下载到 Debrid 的链接」，这个标记会把它们全藏起来——结果就是**可能一个结果都看不到**（[C2]）。

**坑二：看到 `[RD download]` 不等于立即播放。** 这个标记表示该流需要先下载到你的 Debrid 云盘，再拉回本地播放（[C2]）。RD 已缓存的会秒播；没缓存的要等下载完成。选流时别看到标记就以为是坏的，先试试，下载快的依然好用。

> [!warning] 易错点
> 「看不到结果」和「能看但慢」是两回事。前者多半是坑一里的勾选问题，后者才是正常的 Debrid 下载过程。

---

## 本章小结

- addon 返回的 stream 只是指向真实媒体的指针，不是视频文件本身（[A2]）。
- stream 五个指向字段五选一：`url` / `ytId` / `infoHash` / `nzbUrl` / `externalUrl`；`fileIdx` 缺省取体积最大文件（[A4]）。
- 画质用 `name`、描述用 `description`；非 HTTPS/MP4 的直链要设 `behaviorHints.notWebReady`（[A4]）。
- Torrentio 三步接入：打开配置页 → 设 Debrid Provider / Exclude Resolutions / Video Size Limit → 复制 INSTALL / Copy Link 安装（[B2/C1]）。
- 别勾选「Don't show download to debrid links」，否则 2024-11 后可能看不到结果；`[RD download]` 只是需要先下载（[C2]）。

**下一章预告**：现在流列表有了，但默认 None 走的是 P2P，慢、不稳、还有 IP 暴露风险。下一章我们接入 Real-Debrid，把 4K/Remux 真正「秒播」起来。

---

[[03_自托管部署|上一章]] ｜ [[README|返回首页]] ｜ [[05_Real-Debrid链路|下一章]]
