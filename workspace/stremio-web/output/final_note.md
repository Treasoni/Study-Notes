---
title: "stremio-web 实战：从 1080p 采集源到 4K/Remux Debrid 观影路线"
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

# stremio-web 实战：从 1080p 采集源到 4K/Remux Debrid 观影路线

> [!summary] 本篇笔记
> 本篇是一条完整的「高质量观影」实战路线：先认识 stremio-web 的定位与三层架构（React UI ↔ stremio-core ↔ stremio-video），再对比客户端选型（避开 Electron 打包锁 1080p 的坑），接着动手用 Docker/Node 自托管 Web UI，接入 Torrentio addon 与 Real-Debrid 高质量源链路，最后用量化码率数据把 lunatv 采集源与 Stremio torrent+Debrid 两条路线放在一起对比，结合中国网络环境给出最终选型与合规提示。核心结论：stremio-web 本身只是「壳」，画质由「源文件质量 + addon 过滤 + 播放器是否原生解码」决定；走 torrent + Debrid 路线可达 4K/Remux。

## 目录

1. [[#第一章：认识 stremio-web——一个不含资源的「聚合客户端」|第一章：认识 stremio-web——一个不含资源的「聚合客户端」]]
2. [[#第二章：客户端选型——为什么 Electron 版会锁 1080p|第二章：客户端选型——为什么 Electron 版会锁 1080p]]
3. [[#第三章：自托管 stremio-web：把 Web UI 跑起来|第三章：自托管 stremio-web：把 Web UI 跑起来]]
4. [[#第四章：Addon 机制与 Torrentio——给 Stremio 接上影视资源|第四章：Addon 机制与 Torrentio——给 Stremio 接上影视资源]]
5. [[#第五章：Real-Debrid——把 4K/Remux 真正拉起来|第五章：Real-Debrid——把 4K/Remux 真正拉起来]]
6. [[#第六章：画质对比——lunatv 采集源 vs Stremio torrent+Debrid|第六章：画质对比——lunatv 采集源 vs Stremio torrent+Debrid]]

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

# 第二章：客户端选型——为什么 Electron 版会锁 1080p

部署 stremio-web 之前，先要决定一件事：用什么「壳」来看它？同一个 Web UI，放进浏览器、Electron、还是官方桌面 app，画质上限完全不同。选错了，装完才发现 4K 全锁死。

## 2.1 三条路线对比

| 路线 | 形态 | 播放器 | 画质上限 | 适合谁 |
|------|------|--------|---------|--------|
| **A. 自托管 Web UI** | 浏览器打开 stremio-web | 浏览器原生解码 | 受浏览器解码能力约束（[A1]） | 轻量体验 |
| **B. Electron 打包** | stremio-web-desktop | Chromium 播放管线 | 硬性锁 1080p、无原生 4K（[A5]） | 不推荐 |
| **C. 官方桌面 app** | stremio-shell + `--webui-url` | 原生播放器（Qt6） | 原生 4K / Remux（[A5]） | 追求 4K/Remux |

**路线 A**：stremio-web 是官方 Web UI，可自托管，也可直接用 `web.stremio.com`。浏览器能解什么码，画质就停在哪一层，这就是 A 的天花板（[A1]）。

**路线 B**：Electron 打包本质是把同一个网页塞进 Chromium 窗口，播放管线能力不足，于是强制转码、锁死 1080p（[A5]）。这是三条路线里唯一明确封顶的方案。

**路线 C**：官方桌面 app 是 stremio-shell（Qt6），自带原生播放器；加 `--webui-url` 指向 v5 Web UI，就能「既要新界面、又要原生播放」（[A5]）。

> [!tip] 大白话
> 把 Web UI 想成「同一个网页」，播放器想成「机顶盒」。同一网页换到不同机顶盒上，画质天差地别：浏览器盒子看天，Electron 盒子贴了张「1080p 封条」，原生 app 盒子才是满血 4K。

## 2.2 Electron 锁 1080p 的事实与机理

**事实**：stremio-web-desktop 的免责声明（Disclaimer）白纸黑字写着「强制转码，锁 1080p，无原生 4K」（[A5]），是项目方自己承认的硬限制。

**机理**：源材料未解释。目前最合理的推测是——浏览器/Electron 播放管线缺原生解码与 DRM，喂不进系统硬解，于是回退服务端 ffmpeg 转码，输出被限制在 1080p。**这是推测，不是官方说法**（[A5]）。

> [!warning] 关键判断
> 「Electron 锁 1080p」是事实；「为什么会锁」目前只是推测。装任何打包版前先翻它的 Disclaimer，别等装完才发现画质封顶。

## 2.3 选型结论

- **追求 4K / Remux**：官方桌面 app（stremio-shell）+ `--webui-url=https://web.stremio.com/`，原生播放才是正路。
- **只想轻量体验**：自托管 Web UI，或直接用 `web.stremio.com`。

终端启动：

```bash
stremio --webui-url=https://web.stremio.com/
```

Windows 想固定参数：右键快捷方式 → 属性 → 在「目标(Target)」末尾追加（[A5]）：

```text
"C:\Program Files\Stremio\Stremio.exe" --webui-url=https://web.stremio.com/
```

## 本章小结

- Web UI 只是壳，客户端选型决定画质上限：A 看天、B 锁 1080p、C 满血 4K。
- Electron 锁 1080p 是明说的硬限制；「为什么锁」属推测，要与事实分开标注。
- 追求 4K/Remux 用官方桌面 app + `--webui-url`；轻量体验用自托管 Web UI。

下一章动手自托管 stremio-web，把 Web UI 这台「壳」搭起来。

---

# 第三章：自托管 stremio-web：把 Web UI 跑起来

上一章解决了「用哪个客户端」的选型问题。这一章直接动手，把 stremio-web 装到自己机器上，亲眼看到它长什么样，并建立一个贯穿全书的关键认知：**Web UI 只是一层壳**，资源要靠第四章的 addon、高质量要靠第五章的 Debrid 才接得上来。

## 3.1 Docker 部署

官方 README 推荐的第一条路径就是 Docker，几行命令就能起来（[A1]）：

```bash
# 1. 拉取官方源码
git clone https://github.com/stremio/stremio-web
cd stremio-web

# 2. 构建镜像（第一次较久，要拉基础镜像 + 装依赖）
docker build -t stremio-web .

# 3. 运行，把容器内 8080 端口映射到宿主机 8080
docker run -p 8080:8080 stremio-web
```

> [!tip] 大白话
> 把 Docker 想成「一次性装修队」：`build` 是按图纸把房子（镜像）盖好，`run` 是让装修队进场干活。`-p 8080:8080` 是给房子开了扇门——把容器里的 8080 端口映射到你电脑的 8080 端口，这样浏览器才能从外面进来敲门。

构建并启动完成后，打开浏览器访问 `http://localhost:8080`，看到 Stremio 的主界面，就说明部署成功了（[A1]）。

## 3.2 非 Docker 方式（Node 22+ / pnpm 11+）

不想用 Docker 的话，官方也支持直接用 Node 环境跑（[A1]），前提是 **Node.js 22+ 与 pnpm 11+**：

```bash
git clone https://github.com/stremio/stremio-web
cd stremio-web
pnpm install   # 安装依赖
pnpm start     # 启动开发服务器，同样监听 localhost:8080
```

> [!warning] 版本要求
> 项目明确要求 Node.js 22+ 与 pnpm 11+，版本不够会在 `install` 阶段直接报错。pnpm 没装的话，用 `corepack enable` 或 `npm i -g pnpm` 先装上。

## 3.3 部署后的认知：Web UI 只是壳

跑起来之后，先别急着找资源。这里要建立本章最重要的一条认知（[A1]）：

1. **它是可安装的 PWA**：浏览器地址栏会出现「安装」按钮，可以把它像原生 App 一样固定到桌面或任务栏。
2. **它只是一层「壳」**：界面上现在看不到任何影视资源是正常的。stremio-web 只负责渲染界面和播放，本身不托管任何内容。资源要靠 addon（第四章 Torrentio）、高质量要靠 Debrid（第五章 Real-Debrid 链路）来接。

> [!note] 验证部署成功的检查点
> 打开 `http://localhost:8080`，能正常显示主界面、且地址栏出现 PWA 安装入口，即可视为部署成功。此时「首页空空如也」不是 bug——说明壳已经立好，只差接源了。

## 本章小结

- Docker 三连：`git clone` → `docker build -t stremio-web .` → `docker run -p 8080:8080 stremio-web`，然后访问 localhost:8080（[A1]）
- 非 Docker 用 Node 22+ / pnpm 11+：`pnpm install && pnpm start`，开发服务器同在 8080（[A1]）
- Web UI 可安装为 PWA，但它只是壳，本身不含任何资源（[A1]）
- 部署成功的标志 = 主界面能打开 + 地址栏出现 PWA 安装入口；首页没内容属正常现象

壳已经跑起来了，下一步自然是给它接上资源。下一章我们装第一个 addon——Torrentio，让这层壳真正「有东西可看」。

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

# 第五章：Real-Debrid——把 4K/Remux 真正拉起来

上一章装好了 Torrentio，你会发现流列表确实多了，但纯 P2P 拉种子又慢又容易卡，4K/Remux 更是想都别想。这一章解决「怎么让 4K/Remux 真正秒开」——核心就是接入一个 Debrid 服务商（以 Real-Debrid 为例），并学会判断哪些资源值得播。

## 5.1 Debrid 是什么、为什么能秒播 4K

### 5.1.1 一个「帮你先下好种子的服务器」

Debrid（解锁/中转服务）本质上是一个代下载 + 缓存的代理服务。你把磁力链接或种子交给 Real-Debrid（简称 RD）这类服务商，它们的服务器先把 torrent 下完，再把文件缓存在自己这里；你播放时，客户端是从 RD 的服务器上直接拉 HTTP 流，而不是走 P2P 网络（[C2][C4]）。

这样做换了三个好处：

1. **不用等种子慢慢下载**——下载发生在 RD 的高带宽服务器上，而不是你家宽带。
2. **不暴露自己的 IP**——你全程在跟 RD 的服务器通信，不需要给其他 peer 上传。
3. **带宽够大**——服务器带宽远大于家用上行，能扛住 4K/Remux 的高码率。

> [!tip] 大白话
> 把 Debrid 想成「视频仓库 + 代下单」。它把你想要的东西提前搬进仓库（缓存），你看的时候直接从仓库出货，不用自己种地（P2P）。「已缓存」的资源就像外卖柜里的现成餐，扫码就出餐；没缓存的，就是它先帮你下单做，做好再告诉你来取。

### 5.1.2 历史机制：已缓存即播（instant availability）

RD 最经典的卖点是「已缓存即播（instant availability）」：热门种子大概率早已在 RD 服务器上下过并存着。只要种子在缓存里，一点播放就秒开，4K/Remux 也不在话下（[C2]）。这也是社区里「RD 秒播 4K」说法的来源。

### 5.1.3 2024-11 变化：缓存检查端点被移除（区分历史与现状）

这里有个必须澄清的时间线。历史上，Torrentio 会调用 RD 的「检查已缓存 info hash」端点，精确告诉客户端哪些条目能秒播。但 **2024-11 起 RD 移除了这个端点**，Torrentio 无法再精确判断哪些是可即时播放的条目，短期还一度丢失结果（[C2]）。

现在的兜底方案是：Torrentio 自建了一个 **8 小时短期缓存**，只覆盖「经 Torrentio 添加且下载完成」的条目，用这个近似信号代替原来的精确查询。但 RD 会周期性清理缓存，所以这个判断**可能不准确，是临时方案**（[C2]）。

> [!warning] 别把「秒播」理解成机制被删了
> 「RD 秒播 4K」仍然成立，但它的实现已经从「精确查询缓存」变成了「8 小时短期缓存 + 所有链接统一标 `[RD download]`」的新常态。看到链接标 `[RD download]`，意思是这个种子可能还没在 RD 缓存里，点下去会先触发 RD 下载，**不代表立刻能播**。所以 Torrentio 配置里不要勾选「Don't show download to debrid links」，否则 2024-11 后可能一个结果都看不到（[C2]）。

## 5.2 Real-Debrid 接入实操

### 5.2.1 注册 RD 并获取 API Key

1. 打开 `real-debrid.com` 注册账号。
2. 充值（需要海外支付渠道，通常是虚拟信用卡或加密货币）。
3. 在账户页面找到 **API Key**（一般在「Account → API Key」，或页面底部的授权区块）。

> [!warning] 付款前关 VPN
> RD 会拦截来自 VPN 的付款请求（风控）。充值或付款时先关掉 VPN，否则可能被拒甚至触发风控（[WebSearch]）。

> [!tip] 大白话
> API Key 相当于 RD 发给你的「临时工牌」。Torrentio 拿着这张工牌代替你向 RD 下单拉流，你不用把账号密码告诉别人。它只授权「帮我取流」这一件事，不是万能钥匙。

### 5.2.2 在 Torrentio 里填 Debrid Provider

1. 打开 Torrentio 配置页 `https://torrentio.strem.fun/configure`。
2. **Debrid Provider** 选 `RealDebrid`。
3. 粘贴上一步拿到的 API Key（[B2/C1]）。
4. 重新生成安装链接（INSTALL / Copy Link），装进 Stremio。

### 5.2.3 Video Size Limit 实战

配置页里三个关键参数：**Debrid Provider / Exclude Resolutions / Video Size Limit**。其中 Video Size Limit 用逗号分隔两个值，**第一个=电影、第二个=剧集**：

```
10GB,2GB
```

含义是：电影单文件 ≤10GB、剧集单文件 ≤2GB 才显示（[B2/C1]）。想更激进地奔着 4K Remux 去，可以把电影阈值拉到 30–60GB，但记住码率越大对网络链路要求越高，别让列表里全是自己带宽扛不动的大文件。

> [!tip] 大白话
> Video Size Limit 像「点菜时的预算」。给电影 10GB 预算、剧集 2GB 预算，Torrentio 只把预算内的「菜」端上桌给你挑，超预算的直接不显示——避免列一堆你根本播不动的大文件占满视野。

## 5.3 判断资源画质

### 5.3.1 别只看分辨率标签

同样是「4K」，码率可以差到 8 倍。快速估算码率（Mbit/s）的公式：

```
码率 ≈ 文件大小(GB) × 8 × 1024 ÷ 时长(秒)
```

社区给的大致参考：**Netflix ≈ 2–3 Mbit/s；1080p 转码源 ≈ 6–7 Mbit/s；4K ≈ 10–80 Mbit/s**（[C4]）。一个 2 小时的电影，如果只有 5GB，即使标着 4K，码率也只有约 5.7 Mbit/s，画质大概率不如 15GB 的 1080p Remux。

### 5.3.2 优先编码：10-bit HEVC / AV1

码率不等于画质。同样码率下，**10-bit HEVC（H.265）/ AV1** 的压缩效率更高，画质/体积比更好，应优先选这类资源（[C4]）。

### 5.3.3 网络要求：4K 高码率需 ≥100Mbit

Remux（30+GB 的 4K 原盘提取）实测可以在 **RD 已缓存 + ≥100Mbit 链路**下流畅播放，有人用 Stremio + RD 跑满千兆（[C4]）。所以 4K 高码率的底线网络建议是 ≥100Mbit，低于这个带宽，先降低片源体积或码率。

## 5.4 Debrid 替代：中国用户场景

RD 不是唯一选择。如果遇到付款风控、VPN 屏蔽或地区可用性问题，可以考虑以下替代（[WebSearch]）：

| 服务商 | 特点 | 适用场景 |
|--------|------|----------|
| TorBox | 较新的 Debrid，定价灵活 | 想找 RD 平替、RD 风控场景 |
| Premiumize | 老牌，多合一（云盘 + 代理） | 需要云盘/多用途功能 |
| AllDebrid | 老牌，价格相对亲民 | 预算敏感、基础需求 |

> [!tip] 大白话
> Debrid 服务商像外卖平台，RD 是最大那家，TorBox / Premiumize / AllDebrid 是竞争者。哪家在你所在的「配送区」（地区/网络）稳、哪家付款方便，就选哪家。目前没有中国本地化的 Debrid 服务，海外支付是绕不开的一步。

---

## 本章小结

- **Debrid 的本质**：代下载 + 缓存的中转服务器，客户端从它那里直接拉 HTTP 流，免 P2P、免暴露 IP、带宽足够大（[C2][C4]）。
- **历史 vs 现状**：RD 历史上「已缓存即播」靠精确查询；2024-11 移除缓存检查端点后，Torrentio 改用 8 小时短期缓存兜底，所有链接统一标 `[RD download]`，该缓存是临时方案、可能不准（[C2]）。
- **接入三步**：注册 RD 拿 API Key（付款前关 VPN）→ Torrentio 选 RealDebrid 填 Key → Video Size Limit 设 `10GB,2GB`（电影/剧集）（[B2/C1][WebSearch]）。
- **判断画质**：用「文件大小 × 时长」估算码率，优先 10-bit HEVC / AV1，4K 高码率需 ≥100Mbit 链路（[C4]）。
- **替代方案**：TorBox / Premiumize / AllDebrid 可应对 RD 风控或地区可用性问题（[WebSearch]）。

下一章做最终收尾：用量化数据把 lunatv 采集源和 Stremio torrent+Debrid 放在一张表里对比，明确回答「stremio-web 到底能不能看高质量资源」，并结合中国网络环境给出最终选型与合规提示。

---

# 第六章：画质对比——lunatv 采集源 vs Stremio torrent+Debrid

到这里，我们已经把 stremio-web 的架构、客户端选型、部署和接源链路都走了一遍。这一章把散点收拢，用数据回答最初的核心问题：**stremio-web 到底能不能看高质量资源？** 我们把「lunatv 采集源」和「Stremio torrent + Debrid」两条路线放在同一张桌上对比，最后结合中国网络环境给出选型与合规提示。

## 6.1 码率量化对照

「画质好不好」不能只看分辨率标签，更可靠的指标是**码率**（bitrate）——每秒传输的画面数据量，单位 Mbit/s。相同分辨率下，码率越高，细节越丰富、动态场景越不容易糊。以下是社区实测给出的量化区间（[C4]）：

| 画质档位 | 典型码率 | 一句话说明 |
|---|---|---|
| Netflix 流媒体 | ≈ 2–3 Mbit/s | 为互联网带宽做的高压缩转码，够看但细节有损 |
| 1080p 转码源 | ≈ 6–7 Mbit/s | 常见 Web-DL / 压制组，画质明显好一档 |
| 4K | ≈ 10–80 Mbit/s | 视编码（HEVC/AV1）与码率策略差异很大 |
| 4K Remux | 单部 30+GB，码率可破 80 Mbit/s | 原盘提取、未重压，最接近原盘画质 |

> [!tip] 大白话
> 把码率想成「水管的粗细」。同样是 1080p，影视站那条水管很细（低码率高压缩），画面一快就糊成一片；Remux 那条水管粗到能灌满整块屏幕。所以分辨率只是「管径标签」，码率才是「实际流量」。

注意两点。第一，**码率 ≠ 画质**：编码效率同样关键，HEVC(10-bit) / AV1 能在更低码率下达到接近的画质，选资源优先认这两个编码（[C4]）。第二，没有工具时怎么判断码率？用「文件大小 × 时长」反推：`码率(Mbit/s) ≈ 文件大小(GB) × 8000 ÷ 时长(秒)`。比如一部 2 小时（7200 秒）20GB 的电影，算下来约 22 Mbit/s，妥妥的高质量 4K 档。

那 Remux 这种 30+GB 的「巨物」在家里能流播吗？社区实测是**能**——前提是 RD 已缓存该种子、且链路有 **≥100Mbit** 带宽（[C4]）。这正是 Debrid 路线的意义：种子躺在 Debrid 服务器上，你用 HTTP 直连拉流，而不是 P2P 慢慢等。

## 6.2 lunatv vs Stremio 对比表

两条路线的差异，本质是「源从哪来」。lunatv 走影视站网页采集，Stremio 走磁力/Debrid 缓存，这决定了画质上限（[C3]）：

| 维度 | lunatv（影视站采集源） | Stremio（torrent + Debrid） |
|---|---|---|
| 画质上限 | 封顶 1080p | 可达 4K / Remux |
| 资源路径 | 网页采集影视站 | 磁力链 / Debrid 服务器缓存 |
| 同 1080p 画质 | 低码率高压缩，动态易糊 | 远优于影视站同档内容 |
| 生态特色 | 内置网盘搜索（PanSou 等） | 走 Debrid 路线；网盘直链无成熟等价物（待探索） |

> [!warning] 一个容易误判的点
> 对比时别只比「有没有 4K」。哪怕同样锁在 1080p，Stremio 拿到的源通常也是高码率压制组作品，动态场景比影视站低码率高压缩的内容干净得多（[C3]）。

生态差异值得单独说一句：lunatv 把网盘搜索内置了，而 Stremio 社区基本清一色走 Debrid 路线，类似 lunatv 那种「网盘直链」在 Stremio 生态里**没有成熟的等价物**——这点标注为待探索，后续出现成熟方案再补充。

## 6.3 中国网络环境与合规

先讲可用的部分：Stremio 本体是开源软件、本身不托管任何内容，法律上站得住；用 Debrid 或 HTTP 直链拉流时**通常不需要 VPN**，也**比 P2P 直连更安全**——你的 IP 不会暴露给其他 peer（[WebSearch]）。

再看现实风险（[WebSearch]）：

- **Torrentio 可能屏蔽 VPN**：换节点可解；Real-Debrid 对来自 VPN 的付款有风控，**付款前记得关 VPN**。
- **P2P 直连会暴露 IP**：种子下载时其他节点能看到你的 IP，存在 ISP 发版权通知的风险。
- **支付门槛**：Debrid 需要海外支付，一般用**虚拟信用卡或加密货币**；目前没有中国本地化的 Debrid 服务，替代方案是 **TorBox / Premiumize / AllDebrid**。

合规层面必须如实说明：torrent 类插件在**美/欧/英法律**下，技术上构成版权侵权风险，Debrid 只是降低而非消除风险（[WebSearch]）。至于**中国《著作权法》**下如何定性，当前资料没有结论——**标注为未知**，请咨询法律专业人士后再做判断。

## 6.4 最终结论与选型建议

回到开篇的问题：**stremio-web 能看高质量资源吗？能。** 但要记住全篇反复强调的那句话——**Web UI 本身不管画质**。画质由三件事决定：源文件质量 + addon 过滤 + 播放器是否原生解码。

> [!tip] 大白话
> stremio-web 就像一台「空电视」，频道（addon）和信号质量（源）才是画质的关键。把天线接到 Debrid 这颗「卫星」上，就能看到 4K/Remux；接影视站采集源，就只是 1080p。

一句话选型建议：

- **追求 4K / Remux**：官方桌面 app（stremio-shell）+ `--webui-url=https://web.stremio.com/`，或自托管 Web UI + Torrentio/Real-Debrid 接源；
- **只想轻量体验**：自托管 stremio-web + Torrentio（免费源）即可，但要接受画质上限；
- **别走 Electron 打包**：stremio-web-desktop 强制转码锁 1080p，与高质量路线相悖。

## 本章小结

- 码率是比分辨率更靠谱的画质指标：Netflix ≈ 2–3 Mbit/s，1080p 转码源 ≈ 6–7 Mbit/s，4K ≈ 10–80 Mbit/s（[C4]）。
- Remux（30+GB 4K）可流播，前提是 RD 已缓存 + ≥100Mbit 链路（[C4]）。
- lunatv 采集源封顶 1080p；Stremio torrent+Debrid 可达 4K/Remux，同 1080p 时源也更干净（[C3]）。
- 中国网络下 Debrid/HTTP 流通常不需要 VPN、比 P2P 安全；但存在 VPN 屏蔽、付款风控、版权合规等现实风险（[WebSearch]）。
- 结论：能看高质量资源，走 torrent+Debrid 路线；Web UI 只是壳，画质由源 + 播放器决定。

至此六章全部讲完。下一步把这些章节组装成一篇完整笔记，做 Obsidian 美化后发布到你的 `GitHub项目/` 目录——LunaTV 那篇笔记旁边。

---

## 参考资料

> 正文中的 `[A#]` / `[B#]` / `[C#]` 编号与 `[WebSearch]` 对应以下来源。检索日期均为 2026-08-26。

| 编号 | 来源 | 类型 |
|------|------|------|
| [A1] | [stremio/stremio-web（官方仓库）](https://github.com/stremio/stremio-web) | 官方仓库（架构、Docker、PWA） |
| [A2] | [Stremio Addon Guide · Step 5: Providing streams](https://stremio.github.io/stremio-addon-guide/step5) | 官方文档（stream 指针机制） |
| [A3] | [官方博客 · stremio-web alpha 开源公告](https://blog.stremio.com/stremio-web-alpha-is-now-open-source/) | 官方博客（streaming server、MSE，2020 口径） |
| [A4] | [stremio-addon-sdk · Stream Object 参考](https://stremio.github.io/stremio-addon-sdk/api/responses/stream.html) | 官方文档（stream 字段、fileIdx、behaviorHints） |
| [A5] | [Zaarrg/stremio-web-desktop](https://github.com/Zaarrg/stremio-web-desktop) | GitHub 社区实现（Electron 锁 1080p、官方替代方案） |
| [B2/C1] | [Torrentio 配置页](https://torrentio.strem.fun/configure) | 工具官方（Debrid Provider / Exclude Resolutions / Video Size Limit） |
| [C2] | [Torrentio-scraper Issue #305 · RD integration](https://github.com/TheBeastLT/torrentio-scraper/issues/305) | GitHub issue（RD 已缓存即播机制与 2024-11 变化） |
| [C3] | [Viren070's Guides · Stremio Intro](https://guides.viren070.me/stremio/intro) | 社区教程（影视站 vs torrent 画质定性对比） |
| [C4] | [Streaming with high bit rates（码率深度讨论）](https://piefed.jeena.net/post/53866) | 社区讨论（码率量化、Remux 流播实测） |
| [WebSearch] | WebSearch 综合（中国网络环境 / 合规 / Debrid 替代） | 多源综合 |
