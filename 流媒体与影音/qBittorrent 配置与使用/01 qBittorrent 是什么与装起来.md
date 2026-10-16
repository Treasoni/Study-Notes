---
title: qBittorrent 配置与使用（上册）：是什么与装起来
aliases:
  - qBittorrent 上册
  - qBittorrent 是什么与装起来
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

> 📖 总览：[[流媒体与影音/qBittorrent 配置与使用/qBittorrent 配置与使用（总览）|总览]] ｜ 下一册：[[流媒体与影音/qBittorrent 配置与使用/02 qBittorrent 配好|02 配好 →]]

# qBittorrent 配置与使用（上册）：是什么与装起来

> [!summary] 一句话看懂
> qBittorrent 是家庭影院里的**「后厨」**——把种子 / 磁力链接变成硬盘上文件的 BT 下载器。本册先讲清它**是什么**（含 BT/P2P、Tracker、`info_hash` 名词扫盲），再在 fnOS + Docker 上把它**装起来**：**选镜像 → 映两个目录 → 拿首登口令**。

本册是三册中的第一册，收录全局第 1–2 章。第 1 章回答「qBittorrent 是什么」——它在 MoviePilot 那套家庭影院里扮演什么角色，以及 BT / P2P / 种子 / Tracker / `info_hash` 这些名词是什么意思；第 2 章回答「怎么装」——在 fnOS + Docker 上选哪个镜像、怎么映射两个目录、首次登录口令怎么拿。这两章是后面两册的前提：装不起来，配和用都无从谈起。读完本册，你会对 qBittorrent 的定位有清楚的印象，并把它在自己机器上跑起来。

## 目录

- 第 1 章 qBittorrent 是什么，以及它在你家庭影院里的位置
  - 1.1 一句话看懂：它是干什么的
  - 1.2 它在上级分册里的位置（只被当「前提」，没被教怎么装）
  - 1.3 三个名词先扫盲：BT/P2P、种子、Tracker 与 `info_hash`
  - 1.4 官方版 vs「增强版」：两个不同项目（F4）＋ 大小写规范（F3）
- 第 2 章 装起来：镜像三选一、卷映射与首次登录
  - 2.1 结论先行：装起来只需三件事
  - 2.2 三选一：三个镜像，差在环境变量前缀
  - 2.3 卷映射：两个根目录，`/config` 与 `/downloads`
  - 2.4 WebUI 首次登录：口令随版本变（F1）
  - 2.5 WebUI 的对外访问与安全：默认防护是开着的
  - 2.6 动手实践（新手可跳过）

## 第 1 章 qBittorrent 是什么，以及它在你家庭影院里的位置

上级分册《nastool 家庭影院 fnOS 部署》只把 qBittorrent 当「前提条件」列出：第 3 章给了最低版本，第 7 章给了两行对接配置，却没教它怎么装、怎么配。**一句话看懂：qBittorrent 是一个 BT 下载器，负责把「种子」变成你硬盘上的文件**——在 MoviePilot 那套家庭影院里，它是干活的手，不是指挥的脑。认清位置，后面几册（装、配、用）才有落点。

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
| 下载目录映射成 `/downloads`，且与 MoviePilot 一致 | 第 7 章[^c1-up3] | 目录为何必须同根、硬链接怎么生效（见中册第 3 章） |
| 「下载完成时运行外部程序」，填一条 `curl` | 第 7 章[^c1-up4] | 这条回调的占位符怎么写（见中册第 4 章） |

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

**再做种。** 官方原话：在你让下载器退出之前，它会一直上传[^c1-lc1-49]——这是 BT「分享」的来源，也关系到私种（PT）的账号安全（见下册第 6 章）。

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

### 引文对照（原文 / 中译 / 出处）

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

### 脚注

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

## 第 2 章 装起来：镜像三选一、卷映射与首次登录

上一章认清了 qBittorrent 的位置，这一章把它装起来。在 fnOS + Docker 上，装 qBittorrent 只有三件事：**选一个镜像、把两个目录映射进去、拿到首次登录口令**。看着简单，每件都有坑——镜像选错会让环境变量静默失效，目录写成相对路径会直接报错，口令取法还取决于版本号。本章把三件事逐个讲清，最后给两版可照抄的 `docker-compose.yml`。

### 2.1 结论先行：装起来只需三件事

先把三件事和各自的坑摆出来：

| 要做的事 | 怎么做 | 常见坑 |
| --- | --- | --- |
| 选镜像 | 官方 / LinuxServer / 增强版社区镜像 三选一 | 换镜像后环境变量名不一样（2.2） |
| 映两个目录 | 给容器开两扇「门」，通向你的硬盘：`/config` 与 `/downloads` | 写相对路径会直接起不来（2.3） |
| 拿首登口令 | 看版本：≥ `4.6.1` 去容器日志抄临时口令 | 只记住一种取法（2.4） |

> [!tip] 大白话
> 把容器想成**一台租来的、没有硬盘的电脑**：它一重建就把东西忘光，所以得把你自己硬盘上的两个文件夹「租」给它——一个放配置（`/config`），一个放下载的文件（`/downloads`）。这个「租房」动作就是**卷映射**，门必须开在你硬盘上的一个真实路径，不能是容器里的一条相对路径。

### 2.2 三选一：三个镜像，差在环境变量前缀

| | 官方镜像 | LinuxServer 镜像 | 增强版社区镜像 |
| --- | --- | --- | --- |
| 镜像坐标 | `qbittorrentofficial/qbittorrent-nox`[^c2-la1-3] | `lscr.io/linuxserver/qbittorrent`[^c2-la2-11] | 无官方 Docker 镜像（见下） |
| WebUI 端口变量 | `QBT_WEBUI_PORT`[^c2-la1-61] | `WEBUI_PORT`[^c2-la2-100] | 视第三方镜像而定 |
| BT 端口变量 | `QBT_TORRENTING_PORT`[^c2-la1-58] | `TORRENTING_PORT`[^c2-la2-101] | 视第三方镜像而定 |
| 默认端口 | 8080 / 6881[^c2-la1-63][^c2-la1-60] | 8080 / 6881[^c2-la2-91] | 视第三方镜像而定 |
| 首登口令 | 有版本分界（2.4）[^c2-la1-144] | 临时口令打到容器日志[^c2-la2-24] | 视第三方镜像而定 |

**这里最关键的一行是「环境变量名」**：官方镜像用带前缀的 `QBT_*`，LinuxServer 用不带前缀的 `WEBUI_PORT` / `TORRENTING_PORT`——**两套名字互不识别**[^c2-la1-58][^c2-la2-101]。你从网上抄一份别人的 compose 贴到自己的镜像上，名字对不上就会被**静默忽略**：容器照常启动，端口却还是默认值，你怎么改都不生效。这是新手最常见的坑。

至于「增强版」：它**没有官方 Docker 镜像**，本册不给它的容器坐标——其 README 的 Repository 一节只列 AppImage / AUR / Debian / openSUSE / Ubuntu / macOS / Windows 原生包[^c2-la3-37]。要容器化只能另找社区维护的第三方镜像，多一层不可控。**本册主线用官方镜像**，需要别的口味时再自行评估。

一句话选法：跟着本册主线就选官方镜像；如果你这一套别的容器都已经在用 LinuxServer 生态，那就选 LinuxServer 版，两者功能等价，差别只在环境变量名。无论选谁，**记牢你选的那套变量名**，别混用。

顺带统一写法：镜像名和文档里一律是 `qBittorrent`（`q` 小写、`B` 大写），这是官方规范写法[^c2-la1-1]；网上 `Qbittorrent`、`QBittorrent` 等写法都非规范。

### 2.3 卷映射：两个根目录，`/config` 与 `/downloads`

卷映射就是把你硬盘上的两个目录「接」进容器，容器里用固定的内部路径去访问：

| 容器内路径 | 装什么 | 你该给它配什么 |
| --- | --- | --- |
| `/config` | qBittorrent 的全部配置（含 `qBittorrent.conf`、种子状态）[^c2-la2-105] | 一个专属于它的空目录 |
| `/downloads` | 下载下来的文件[^c2-la2-106] | 你的下载目录（要和 MoviePilot 看到的一致，见中册第 3 章） |

**两条硬规则**。第一条，卷必须写**宿主机上的绝对路径**，官方有明确原话：

| 它管什么 | 官方原文 | 说人话 |
| --- | --- | --- |
| 卷路径怎么写 | 「Using a relative path will not work.」[^c2-la1-67] | 卷必须写宿主机上的绝对路径；写相对路径，容器直接起不来。 |

第二条，`/config` 单独给一个干净目录，别和别的程序共用，否则配置文件会互相覆盖。一句话记法：**`/config` 一人一个抽屉，`/downloads` 大家一起用**（它要和 MoviePilot 的下载目录是同一个，详见中册第 3 章）。

> [!tip] 大白话
> 把 `/config` 想成 qBittorrent 的**记事本**，`/downloads` 想成它的**收件箱**。记事本要放在只属于它的抽屉里（否则和别人的笔记混在一起），收件箱则要和 MoviePilot 的收件箱**是同一个**（否则 MoviePilot 收不到快递，详见中册第 3 章）。

### 2.4 WebUI 首次登录：口令随版本变（F1）

装好后，浏览器打开 `http://<你的设备地址>:<WebUI 端口>`（默认 8080）[^c2-la1-142]。登录口令**取决于版本**，两种情形都要记清，别只会一种：

| 版本 | 首登怎么拿口令 | 出处 |
| --- | --- | --- |
| ≥ `4.6.1`（新） | 启动时**生成一个临时口令打印到容器日志**，用 `docker logs` 抄出来 | 官方镜像 README[^c2-la1-144] |
| < `4.6.1`（旧） | 用**默认口令**，无需去日志里找 | 官方镜像 README[^c2-la1-152] |

官方对「新版本」这一幕有原话，资格够硬，单独摆出来：

| 官方原文 | 说人话 |
| --- | --- |
| 「For newer qBittorrent versions (≥ 4.6.1), qBittorrent will generate a temporary password and print it to the console (via stdout).」[^c2-la1-144] | 较新的版本启动时会生成一个**临时口令**，并打印到控制台（标准输出）——这就是你要抄下来的那串。 |

没有附着控制台，就用这条命令看日志[^c2-la1-149]：`docker logs qbittorrent-nox`。LinuxServer 镜像同理，它的临时口令也会打到容器日志里[^c2-la2-24]。

而**旧版本（< `4.6.1`）**没有这个机制，直接用默认账号口令登录就行，不必去日志里翻[^c2-la1-152]。所以「口令到底去哪拿」这件事，先看清你装的是哪个版本——这就是 `4.6.1` 这个分界的由来。

登录后**立刻改密码**[^c2-la1-154]：WebUI 里 `Tools` 菜单 → `Options...` → `WebUI` 标签页 → `Authentication`。不改的话，很多镜像**每次启动都会重新生成一个临时口令**，你下次又登不进去[^c2-la2-25]。

### 2.5 WebUI 的对外访问与安全：默认防护是开着的

**一句话看懂**：WebUI 是你远程管理 qB 的入口，它默认「监听所有网卡、端口 `8080`、用户名 `admin`」；同时**四个防护开关默认都是开着的**。要做的第一件事是**改掉默认口令**，而不是去关防护。

> [!tip] 大白话
> 把 WebUI 想成**你家的门**：`IP address` 是门开在哪面墙（默认 `*`，四面墙都开）、`Port` 是门牌号（默认 `8080`）、`Username` / `Password` 是门锁（默认用户名 `admin`、口令留空待设）。那一组防护开关则是**门链和猫眼**——默认就挂着，别为了图方便先拆掉。

**先认清 `Options` → `WebUI` 这一页的字段**（界面原串与默认值取自官方源码 @ `df402f91d456`）：

| 界面原文 | 配置键 | 源码默认 | 说人话 |
| --- | --- | --- | --- |
| `Web User Interface (Remote control)` | `WebUI\Enabled` | 视构建而定（**不猜**） | 整个 WebUI 的总开关 |
| `IP address:` | `WebUI\Address` | `*`[^c2-lb10-855] | 门开在哪面墙；官方写明 `*` 表示 IPv4 与 IPv6 **都**监听[^c2-lb10-3777] |
| `Port:` | `WebUI\Port` | `8080`[^c2-lb10-868] | 门牌号，就是 §2.4 里用的那个端口 |
| `Use UPnP / NAT-PMP to forward the port from my router` | `WebUI\UseUPnP` | `false`[^c2-lb10-882] | 让路由器自动开端口，默认**不开** |
| `Use HTTPS instead of HTTP`（配 `Certificate:` / `Key:`） | `WebUI\HTTPS\Enabled` / `CertificatePath` / `KeyPath` | `false`[^c2-lb10-1038] | 加密入口；默认**关**，要用得填证书与私钥 |
| `Username:` / `Password:` | `WebUI\Username` / `Password_PBKDF2` | `admin`[^c2-lb10-895] / 空 | 门锁；默认用户名 `admin`，口令留空待设 |

**再看那四个「默认就开着」的防护**（都在同一页的 `Security` 区）：

| 界面原文 | 配置键 | 源码默认 | 它挡什么 |
| --- | --- | --- | --- |
| `Enable Cross-Site Request Forgery (CSRF) protection` | `WebUI\CSRFProtection` | **`true`**[^c2-lb10-999] | 跨站伪造请求 |
| `Enable Host header validation`（配 `Server domains:`） | `WebUI\HostHeaderValidation` / `ServerDomains` | **`true`**[^c2-lb10-1025] / `*`[^c2-lb10-842] | 防 **DNS rebinding**：只接受 Host 头在白名单内的请求[^c2-lb10-4225] |
| `Enable clickjacking protection` | `WebUI\ClickjackingProtection` | **`true`**[^c2-lb10-986] | 被别的站点套进框架里骗点击 |
| `Enable cookie Secure flag (requires HTTPS or localhost connection)` | `WebUI\SecureCookie` | **`true`**[^c2-lb10-1012] | 只在 HTTPS / localhost 下发送登录 Cookie |

> [!warning] 不要为了「浏览器不跳 https」去关防护
> 本章 §2.6 记过一条**社区经验**：改 `qBittorrent.conf`，设 `WebUI\HostHeaderValidation=false` 与 `WebUI\CSRFProtection=false`，好绕开某些浏览器强制 https 的跳转。现在有源码口径了——这两个键**默认就是 `true`**[^c2-lb10-1025][^c2-lb10-999]，设成 `false` 是在**关掉**默认开启的防护。要用这条社区做法，请清楚自己是在拿**安全性**换方便。

> [!tip] 想从公网访问？走加密，别拆门链（新手可跳过）
> 要让 WebUI 在局域网外可用，正规做法有两条：① 在同一页勾 `Use HTTPS instead of HTTP` 并填 `Certificate:` / `Key:`[^c2-lb10-1038]；② 在前面挂一个**反向代理**，并在 WebUI 页勾 `Enable reverse proxy support`，把代理地址填进 `Trusted proxies list`（源码默认**关**[^c2-lb10-1129]；官方说明该列表是为了取用转发后的客户端地址，即 `X-Forwarded-For` 头[^c2-lb10-4285]）。具体怎么配属环境相关，照官方 wiki 的「Reverse proxy setup」示例即可（源码界面里就链到那一页），本册不代你给一份「万能 nginx」。

### 2.6 动手实践（新手可跳过）

> [!tip] 新手可跳过
> 这一节是可直接照抄的配制。不打算自己写 compose 的读者可以跳过，直接照搬下面的文件、改掉路径即可。

**官方镜像版**（环境变量用 `QBT_*`[^c2-la1-58][^c2-la1-61]）：

```yaml
# docker-compose.yml（官方镜像版）
services:
  qbittorrent:
    image: qbittorrentofficial/qbittorrent-nox:latest   # 也可换 GitHub 镜像 ghcr.io/qbittorrent/docker-qbittorrent-nox:latest
    container_name: qbittorrent-nox
    environment:
      - QBT_LEGAL_NOTICE=confirm        # 只有你已阅读其法律声明才填 confirm
      - QBT_TORRENTING_PORT=6881        # BT 端口，默认 6881
      - QBT_WEBUI_PORT=8080             # WebUI 端口，默认 8080
      - PUID=1000                       # 运行身份，默认 1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - /vol1/1000/docker/qbittorrent/config:/config      # 绝对路径，不能用相对路径
      - /vol1/1000/media/downloads:/downloads
    ports:
      - 8080:8080
      - 6881:6881                       # BT，tcp
      - 6881:6881/udp                   # BT，udp（两个都要）
    read_only: false                    # 用了 PUID/PGID 就必须关掉只读
    stop_grace_period: 30m              # 官方要求：默认 10s 太短，会损坏文件
    restart: unless-stopped
```

**LinuxServer 镜像版**（环境变量**不带** `QBT_` 前缀[^c2-la2-100][^c2-la2-101]）：

```yaml
# docker-compose.yml（LinuxServer 镜像版）
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - WEBUI_PORT=8080                 # 注意：不带 QBT_ 前缀
      - TORRENTING_PORT=6881            # 注意：不带 QBT_ 前缀
    volumes:
      - /vol1/1000/docker/qbittorrent/config:/config
      - /vol1/1000/media/downloads:/downloads
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    stop_grace_period: 10s
    restart: unless-stopped
```

几个必须照做的小点：

- **路径改成你自己的**：`/vol1/1000/...` 是 fnOS 常见的卷布局示意，按你机器上的实际路径替换[^c2-la1-67]。
- **官方镜像的 `stop_grace_period` 不能省**：官方镜像警告默认只有 10 秒，太短会打断关闭流程、损坏文件，要求改成 30 分钟（官方版 compose 已写 `stop_grace_period: 30m`）[^c2-la1-118]；上面的 **LinuxServer 版**沿用其文档示例的 `10s`[^c2-la2-60]，两者各随镜像口径，别混用。
- **用了 `PUID`/`PGID` 就要关只读**：官方镜像默认以只读文件系统运行，而 `PUID`/`PGID` 与只读不兼容，必须写 `read_only: false`[^c2-la1-123]。
- **想省掉端口映射也有别的写法**：社区配方里出现过 `network_mode: host`，让容器直接用宿主机网络[^c2-la5-32]；代价是它会把服务直接暴露在宿主网络上、并和其它占端口的程序冲突，本册不默认采用。
- **改端口要「两侧同改」**：只改环境变量、不改 `ports:` 映射，或反过来，都会不生效——这正是中册第 3 章要讲透的一件事。

取首登口令（≥ `4.6.1`）[^c2-la1-149]：

```shell
docker logs qbittorrent-nox
```

> [!warning] 可选：改 conf 去掉 https 跳转（社区经验）
> 有人会先停容器、再编辑 `qBittorrent.conf`，在 `[Preferences]` 里加 `WebUI\HostHeaderValidation=false` 与 `WebUI\CSRFProtection=false`，以绕开某些浏览器强制 https 的问题[^c2-la4-35]。这是**社区经验**（非官方口径）；它同时**降低了安全性**（关掉了跨站请求防护），请只在你清楚后果时使用，并记得**先停容器再改**，否则配置会被重置[^c2-la4-42]。这两个键的**默认值与语义**见 §2.5。

一个小提醒：上面的镜像名、端口、卷路径都回官方镜像 README 与 LinuxServer 文档核对过；网上社区配方（含 fnOS 论坛）只作交叉参考，不作为精确口径——曾见过配方里 `PUID`/`PGID` 给成 `0`（以 root 运行），本册不放这种值[^c2-la5-20]。

### 本章小结

- 装起来只需三件事：**选镜像 → 映两个目录（`/config`、`/downloads`）→ 拿首登口令**。
- 三个镜像的功能等价，最容易踩的差别是**环境变量前缀**：官方用 `QBT_*`，LinuxServer 用不带前缀的名字，两套互不识别，抄错会被静默忽略（F2）。
- 卷必须写**宿主机上的绝对路径**；`/config` 要独占一个干净目录，`/downloads` 要和 MoviePilot 看到的**是同一个**。
- 首登口令**随版本变**：`≥ 4.6.1` 去容器日志抄临时口令，`< 4.6.1` 用默认口令；进去后**立刻改密码**（F1）。
- WebUI 页的**四个防护开关默认都开着**（CSRF / Host 头校验 / 点击劫持 / Secure Cookie）[^c2-lb10-999][^c2-lb10-1025][^c2-lb10-986][^c2-lb10-1012]；要暴露到公网请走 HTTPS 或反向代理，**别关防护**。
- 官方镜像两个必改项：`stop_grace_period: 30m`（默认 10 秒太短，会损坏文件）、用了 `PUID`/`PGID` 就要 `read_only: false`。

### 下一章预告

容器起来了，但「装好」不等于「配好」。中册第 3 章讲**配好**的两件核心事：**BT 端口要映射、改端口必须「两侧同改」**，以及下载目录与硬链接口径——为什么下载目录必须和媒体端**映射同一个宿主目录**，否则硬链接会失效。

### 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Using a relative path will not work.` | 用相对路径不行。 | `LA-1 · sources/l1-1_official-docker-readme.md:69` |
| 2 | `For newer qBittorrent versions (≥ 4.6.1), qBittorrent will generate a temporary password and print it to the console (via stdout).` | 对于较新的 qBittorrent 版本（≥ 4.6.1），qBittorrent 会生成一个临时口令并打印到控制台（标准输出）。 | `LA-1 · sources/l1-1_official-docker-readme.md:144` |
| 3 | `You must then change username/password in the web UI section of settings.` | 随后你必须在设置的 Web UI 一栏里修改用户名/口令。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:25` |

### 脚注

[^c2-la1-1]: LA-1 · `sources/l1-1_official-docker-readme.md:1`。
[^c2-la1-3]: LA-1 · `sources/l1-1_official-docker-readme.md:3`（官方镜像仓库坐标）。
[^c2-la1-58]: LA-1 · `sources/l1-1_official-docker-readme.md:58-60`（`QBT_TORRENTING_PORT`，未设时默认 `6881`）。
[^c2-la1-60]: LA-1 · `sources/l1-1_official-docker-readme.md:60`。
[^c2-la1-61]: LA-1 · `sources/l1-1_official-docker-readme.md:61-63`（`QBT_WEBUI_PORT`，未设时默认 `8080`）。
[^c2-la1-63]: LA-1 · `sources/l1-1_official-docker-readme.md:63`。
[^c2-la1-67]: LA-1 · `sources/l1-1_official-docker-readme.md:67-72`（`/config` 与 `/downloads` 卷说明）。
[^c2-la1-118]: LA-1 · `sources/l1-1_official-docker-readme.md:115-118`（`stop_grace_period: 30m`）。
[^c2-la1-123]: LA-1 · `sources/l1-1_official-docker-readme.md:121-125`（`PUID`/`PGID` 默认 `1000`，与只读不兼容）。
[^c2-la1-142]: LA-1 · `sources/l1-1_official-docker-readme.md:142`。
[^c2-la1-144]: LA-1 · `sources/l1-1_official-docker-readme.md:144-145`。
[^c2-la1-149]: LA-1 · `sources/l1-1_official-docker-readme.md:146-150`。
[^c2-la1-152]: LA-1 · `sources/l1-1_official-docker-readme.md:152`。
[^c2-la1-154]: LA-1 · `sources/l1-1_official-docker-readme.md:154-156`（登录后改密码的路径）。
[^c2-la2-11]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:11`。
[^c2-la2-24]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:24`。
[^c2-la2-25]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:25`。
[^c2-la2-60]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:60`（LinuxServer 的 compose 示例 `stop_grace_period:"10s"`，标注 `#optional`）。
[^c2-la2-91]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:91-93`（端口表：`8080:8080` / `6881:6881` / `6881:6881/udp`）。
[^c2-la2-100]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:100`。
[^c2-la2-101]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:101`。
[^c2-la2-105]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:105`（`/config` 卷）。
[^c2-la2-106]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:106`（`/downloads` 卷）。
[^c2-la3-37]: LA-3 · `sources/l1-3_enhanced-fork-readme.md:37-82`（Repository 节）。
[^c2-la4-35]: LA-4 · `sources/l1-4_fnOS-community-1.md:35-36`（社区经验，非官方口径）。
[^c2-la4-42]: LA-4 · `sources/l1-4_fnOS-community-1.md:42`。
[^c2-la5-20]: LA-5 · `sources/l1-5_fnOS-community-2.md:20`（社区 compose 示例，仅作交叉参考）。
[^c2-la5-32]: LA-5 · `sources/l1-5_fnOS-community-2.md:24,32`（社区 compose 出现 `network_mode: host`；第 24 行「或者使用host模式」，仅作交叉参考）。
[^c2-lb10-855]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:855`（`WebUI/Address` 默认 `*`）。
[^c2-lb10-3777]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:3777-3779`（`IP address` 的官方 tooltip：`*` 表示 IPv4 与 IPv6 都监听）。
[^c2-lb10-868]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:868`（`WebUI/Port` 默认 `8080`）。
[^c2-lb10-882]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:882`（`WebUI/UseUPnP` 默认 `false`）。
[^c2-lb10-1038]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:1038`（`WebUI/HTTPS/Enabled` 默认 `false`）。
[^c2-lb10-895]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:895`（`WebUI/Username` 默认 `admin`）。
[^c2-lb10-999]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:999`（`WebUI/CSRFProtection` 默认 `true`）。
[^c2-lb10-1025]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:1025`（`WebUI/HostHeaderValidation` 默认 `true`）。
[^c2-lb10-842]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:842`（`WebUI/ServerDomains` 默认 `*`）。
[^c2-lb10-4225]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:4225-4229`（`Server domains` 的官方 tooltip：过滤 HTTP `Host` 头，防 DNS rebinding）。
[^c2-lb10-986]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:986`（`WebUI/ClickjackingProtection` 默认 `true`）。
[^c2-lb10-1012]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:1012`（`WebUI/SecureCookie` 默认 `true`）。
[^c2-lb10-1129]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:1129`（`WebUI/ReverseProxySupportEnabled` 默认 `false`）。
[^c2-lb10-4285]: LB-10 · `sources/l1-10_webui-access-security-official-source.md:4285-4287`（`Trusted proxies list` 的官方 tooltip：用于取 `X-Forwarded-For` 转发地址）。

## 更新记录

| 日期 | 变更 | 来源 |
| --- | --- | --- |
| 2026-10-16 | 新增 §2.5「WebUI 的对外访问与安全」：给出 WebUI 页字段与四个防护开关的**源码默认值**，把 §2.6 那条 LA-4 社区经验（关 `HostHeaderValidation`/`CSRFProtection`）按官方口径补齐并加警示；原 §2.5 动手实践顺延为 §2.6 | LB-10 · `sources/l1-10_webui-access-security-official-source.md` |
