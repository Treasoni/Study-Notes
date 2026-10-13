## 第 1 章 qBittorrent 是什么，以及它在你家庭影院里的位置

上级分册《nastool 家庭影院 fnOS 部署》只把 qBittorrent 当「前提条件」列出：第 3 章给了最低版本，第 7 章给了两行对接配置，却没教它怎么装、怎么配。**一句话看懂：qBittorrent 是一个 BT 下载器，负责把「种子」变成你硬盘上的文件**——在 MoviePilot 那套家庭影院里，它是干活的手，不是指挥的脑。认清位置，后面五章（装、配、用）才有落点。

### 1.1 一句话看懂：它是干什么的

把家庭影院想成一家餐厅：**MoviePilot 是经理**（点单、查库存），**媒体服务器是服务员**（把片子摆成海报墙），**qBittorrent 是后厨**——把「菜」搬进你家的正是它[^c1-up1]。官方说它是用 C++ / Qt 编写、底层依赖 libtorrent 的 BT 客户端[^c1-la3-17]；产物很实在：给它一个 `.torrent` 文件或一条磁力链接，它就下载成你硬盘上的一个文件夹。

它和「浏览器另存为」的区别，在于**怎么拿到文件**——BitTorrent 官方规范开门见山：

| 官方原文 | 说人话 |
| --- | --- |
| 「BitTorrent is a protocol for distributing files.」[^c1-lc1-22] | 一套「分发文件」的协议：不是从一台服务器拉，而是从很多台机器一起来的。 |
| 「when multiple downloads of the same file happen concurrently, the downloaders upload to each other」[^c1-lc1-22] | 同一份文件被很多人同时下载时，这些下载者会**互相上传**给对方。 |

这就是 P2P（peer-to-peer，点对点）：**下载的人越多，速度反而越快**[^c1-lc1-22]。

> [!tip] 大白话
> 传统下载像「排队打饭」：人越多队越长。P2P 像「每人带个菜来拼桌」：人越多菜越全。qBittorrent 就是你坐下的那张椅子。

### 1.2 它在上级分册里的位置（只被当「前提」，没被教怎么装）

上级分册不是没提它，而是**只把它当条件列出**：

| 上级分册说了什么 | 在哪 | 本册补什么 |
| --- | --- | --- |
| 下载器最低版本 `>= 4.3.9` | 第 3 章[^c1-up2] | 具体怎么装（第 2 章） |
| 下载目录映射成 `/downloads`，且与 MoviePilot 一致 | 第 7 章[^c1-up3] | 目录为何必须同根、硬链接怎么生效（第 3 章） |
| 「下载完成时运行外部程序」，填一条 `curl` | 第 7 章[^c1-up4] | 这条回调的占位符怎么写（第 4 章） |

一句话概括：**上级分册把 qBittorrent 当「零件」写进采购清单，本册教你造出它、装上去、转起来。**

> [!note] 顺便统一一个写法
> 上级分册表格把它写作 `Qbittorrent`，是**非规范写法**；官方品牌写法是 `qBittorrent`——`q` 小写、`B` 大写[^c1-la1-1]。本册全文统一官方写法，你往后搜资料、贴命令也照这个拼。

### 1.3 三个名词先扫盲：BT/P2P、种子、Tracker 与 `info_hash`

一节之内冒出几个新词，先扫一遍：

| 名词 | 大白话 | 官方原文一句话 |
| --- | --- | --- |
| BT / P2P | 一群人互相拼文件，人越多越快 | 「a protocol for distributing files」[^c1-lc1-22] |
| 种子（metainfo） | 一份资源清单：叫什么、多大、分几块 | 「A static 'metainfo' file」[^c1-lc1-25] |
| Tracker | 「联络处」，告诉你谁手里有这些块 | 「A BitTorrent tracker」[^c1-lc1-26] |
| `info_hash` | 资源指纹，对得上就是「同一份文件」 | 「The 20 byte sha1 hash of the bencoded form of the info value」[^c1-lc1-83] |
| 做种 | 下完继续把手里的块传给别人 | 「it keeps uploading until this happens」[^c1-lc1-49] |

官方把一次分发拆成六种实体，主要有 metainfo 文件、tracker 和最终用户的下载器[^c1-lc1-23]——你扮演的就是最后一类。

**重点是 Tracker。** 把它想成小区门口的**公告栏**：你贴一张「我要《XX》」，它回你「谁家有」的名单；官方说它的响应是一本字典，装着 `peers`（同伴）和一个 `interval`（隔多久再问一次）[^c1-lc1-106]。所以 Tracker **自己不存文件**，只决定你**能不能找到人**。

**再做种。** 官方原话：在你让下载器退出之前，它会一直上传[^c1-lc1-49]——这是 BT「分享」的来源，也关系到私种（PT）的账号安全（第 6 章）。

### 1.4 官方版 vs「增强版」：两个不同项目（F4）＋ 大小写规范（F3）

你上网一搜，大概率撞见另一个名字：**「qBittorrent 增强版」**。先把结论立住——**它是社区分支（fork），不是 qBittorrent 的官方版本**。证据是它自己的自述，GitHub 仓库描述第一句就写着 `[Unofficial]`：

| 官方原文 | 中译 |
| --- | --- |
| 「[Unofficial] qBittorrent Enhanced, based on qBittorrent」[^c1-la3-29] | 「[非官方] qBittorrent 增强版，基于 qBittorrent」 |

两者对比：

| 对比项 | 官方 qBittorrent | 增强版（社区 fork） |
| --- | --- | --- |
| 谁维护 | 官方团队 | 第三方维护者 |
| 额外功能 | 无 | 自动屏蔽迅雷 / QQ / 百度等吸血客户端、自动更新公共 Tracker 列表[^c1-la3-6] |
| 容器镜像 | 官方有：`qbittorrentofficial/qbittorrent-nox`[^c1-la1-3] | README 的 Repository 一节只列 AppImage / AUR / Debian / openSUSE / Ubuntu / macOS / Windows 原生包，**不给 Docker 镜像坐标**[^c1-la3-37] |

结论：走容器化（本册主线）选官方镜像有背书；用增强版，容器镜像只能另找社区第三方镜像，多一层不可控（第 2 章细说）。写法再强调一次——官方是 `qBittorrent`[^c1-la1-1]，不是 `Qbittorrent`。

### 本章小结

- qBittorrent 是 BT 下载器，家庭影院里的「后厨」：把种子 / 磁力链接变成硬盘上的文件。
- P2P 的关键是「下载者互相上传」，人越多越快；Tracker 只牵线，自身不存文件。
- `info_hash` 是资源指纹，做种是「下完继续上传」——配私种时会反复用到。
- 上级分册只把它当前提条件，没教怎么装和配；本册补的正是这段缺口。
- 「增强版」是社区 fork（自述非官方），与官方是两个项目；本册统一官方写法 `qBittorrent`。

### 下一章预告

认清位置后，下一步是把它装起来。第 2 章给出镜像三选一的对比，以及 fnOS + Docker 下可照抄的 compose，并讲清最容易卡住新手的一件事：**首次登录 WebUI 的口令，在 `4.6.1` 前后取法完全不同**。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `BitTorrent is a protocol for distributing files.` | BitTorrent 是一套分发文件的协议。 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:22` |
| 2 | `when multiple downloads of the same file happen concurrently, the downloaders upload to each other` | 当同一份文件被多人同时下载时，下载者之间会互相上传。 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:22` |
| 3 | `A static 'metainfo' file` | 一份静态的 metainfo（元信息）文件 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:25` |
| 4 | `A BitTorrent tracker` | 一个 BitTorrent tracker | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:26` |
| 5 | `The 20 byte sha1 hash of the bencoded form of the info value` | metainfo 文件中 info 值经 bencoding 编码后的 20 字节 sha1 哈希 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:83` |
| 6 | `it keeps uploading until this happens` | 在你让它退出之前，它会一直上传。 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:49` |
| 7 | `[Unofficial] qBittorrent Enhanced, based on qBittorrent` | [非官方] qBittorrent 增强版，基于 qBittorrent。 | `LA-3 · sources/l1-3b_enhanced-fork-api.json:29` |
| 8 | `qBittorrent is a bittorrent client programmed in C++ / Qt that uses libtorrent` | qBittorrent 是一个用 C++ / Qt 编写、使用 libtorrent 的 BT 客户端。 | `LA-3 · sources/l1-3_enhanced-fork-readme.md:17-18` |

## 脚注

[^c1-up1]: 上游分册《nastool 家庭影院 fnOS 部署》第 1 章：`流媒体与影音/nastool 家庭影院 fnOS 部署/01 先看清楚要搭什么.md:30,51`。该分册不在本册 `sources/` 内，仅用于说明「位置」。
[^c1-up2]: 同上分册第 3 章：`流媒体与影音/nastool 家庭影院 fnOS 部署/03 动手前的准备.md:74`。
[^c1-up3]: 同上分册第 7 章：`流媒体与影音/nastool 家庭影院 fnOS 部署/07 对接下载器与媒体服务器.md:70-71`。
[^c1-up4]: 同上分册第 7 章：`流媒体与影音/nastool 家庭影院 fnOS 部署/07 对接下载器与媒体服务器.md:119-120`。
[^c1-la1-1]: LA-1 · `sources/l1-1_official-docker-readme.md:1`（官方镜像 README 标题写作 `qBittorrent-nox`）。
[^c1-la1-3]: LA-1 · `sources/l1-1_official-docker-readme.md:3`（官方镜像仓库坐标）。
[^c1-la3-6]: LA-3 · `sources/l1-3_enhanced-fork-readme.md:6,10`。
[^c1-la3-17]: LA-3 · `sources/l1-3_enhanced-fork-readme.md:17-18`。
[^c1-la3-29]: LA-3 · `sources/l1-3b_enhanced-fork-api.json:29`。
[^c1-la3-37]: LA-3 · `sources/l1-3_enhanced-fork-readme.md:37-82`（Repository 节）。
[^c1-lc1-22]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:22`。
[^c1-lc1-23]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:23-29`（六种实体清单）。
[^c1-lc1-25]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:25`。
[^c1-lc1-26]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:26`。
[^c1-lc1-49]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:49`。
[^c1-lc1-83]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:83`。
[^c1-lc1-106]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:106`。
