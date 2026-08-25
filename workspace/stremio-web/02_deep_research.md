# 深度研究 - stremio-web 项目：能看高质量资源吗？

> 项目：stremio-web · 阶段 2（深度收集）· 2026-08-26
> 已确认方向：A（是什么+核心能力）+ B（部署与接入）+ C（高质量资源路线）
> 精读来源：9 个（官方 6 / 社区教程 1 / 社区讨论 1 / 实现 1），另有 WebSearch 补齐中国网络与合规缺口

---

## 一、范围（Scope）

本篇回答三个问题：

1. **stremio-web 是什么**：与官方客户端的关系、架构组成（React + stremio-core WASM + stremio-video）、能播什么。
2. **怎么部署与接入**：Docker 自托管、Addon（Torrentio）配置、Debrid（Real-Debrid）高质量源链路。
3. **高质量资源怎么来**：4K/Remux 路径、码率量化对比（vs 影视站 1080p）、与 lunatv 对比、中国环境与合规风险。

---

## 二、来源表（Source Table）

| ID | 来源 | 类型 | tier | 评分 | 检索日期 | 覆盖点 |
|----|------|------|------|------|---------|--------|
| A1 | [stremio/stremio-web](https://github.com/stremio/stremio-web) | GitHub 官方仓库 | official | 5 | 2026-08-26 | 架构、Docker、PWA |
| A2 | [Stremio Addon Guide · Step 5](https://stremio.github.io/stremio-addon-guide/step5) | 官方文档 | official | 5 | 2026-08-26 | stream 指针机制 |
| A3 | [官方博客 · stremio-web alpha 开源](https://blog.stremio.com/stremio-web-alpha-is-now-open-source/) | 官方博客 | official | 4.5 | 2026-08-26 | streaming server、MSE（2020 口径） |
| A4 | [stremio-addon-sdk · Stream Object](https://stremio.github.io/stremio-addon-sdk/api/responses/stream.html) | 官方文档 | official | 4 | 2026-08-26 | stream 字段、fileIdx、behaviorHints |
| A5 | [Zaarrg/stremio-web-desktop](https://github.com/Zaarrg/stremio-web-desktop) | GitHub 社区实现 | community | 3 | 2026-08-26 | Electron 锁 1080p |
| B2/C1 | [Torrentio 配置页](https://torrentio.strem.fun/configure) | 工具官方 | official | 5 | 2026-08-26 | Debrid 提供商、分辨率/大小过滤 |
| C2 | [Torrentio-scraper Issue #305](https://github.com/TheBeastLT/torrentio-scraper/issues/305) | GitHub issue | official | 5 | 2026-08-26 | RD instant availability 机制变化 |
| C3 | [Viren070's Guides · Stremio Intro](https://guides.viren070.me/stremio/intro) | 社区教程 | implementation | 4 | 2026-08-26 | 影视站 vs torrent 画质定性对比 |
| C4 | [Streaming with high bit rates](https://piefed.jeena.net/post/53866) | 社区讨论 | community | 4 | 2026-08-26 | 码率量化、Remux 流播实测 |
| — | WebSearch（中国网络 / 合规） | 多源 | community | 3 | 2026-08-26 | 支付风控、替代方案、法律提示 |

---

## 三、Claim / Source 映射

### 3.1 stremio-web 是什么、怎么组成（方向 A）

| # | 结论 | 依据 |
|---|------|------|
| 1 | stremio-web 是 **Stremio 官方 Web UI**（React 应用），可装为 PWA，官方线上实例在 `web.stremio.com` | A1 README「Freedom to Stream」「the official web UI of Stremio」「📱 Installable」 |
| 2 | 架构：`React UI <--> stremio-core`；**stremio-core 是 Rust 引擎编译为 WebAssembly、跑在 Web Worker**；「UI 渲染状态，core 计算状态」 | A1「How it works」 |
| 3 | 播放层走 **stremio-video** 抽象，按环境选择播放器实现 | A1「How it works」 |
| 4 | 2020 年 alpha 博客口径：播放用 HTML5 `<video>` + **MSE**；**非标准格式 / 本地文件 / BitTorrent 需连 streaming server**；当时 iPhone 不支持 MSE | A3「under the hood」「streaming section」 |
| 5 | **差异点**：当前 README 已不提 stremio-server / streaming server；2020 博客提。现状是「streaming server 是否仍必需」待核实 | A1 vs A3 对比 |
| 6 | 官方明确 Web 版**不是**桌面/安卓版的替代品 | A3「Final thoughts」 |
| 7 | Docker 自托管：`docker build -t stremio-web . && docker run -p 8080:8080 stremio-web`（端口 8080） | A1「🐳 Docker」 |
| 8 | 非 Docker：Node.js 22+、pnpm 11+，`pnpm install && pnpm start` | A1「Getting Started」 |
| 9 | 官方对**画质上限无明确量化说明**；画质由「源文件质量 + 播放/转码链路」决定 | A1/A3 均未给出数字 |

### 3.2 Addon 机制：stream 对象与 torrent 流（方向 A/B）

| # | 结论 | 依据 |
|---|------|------|
| 10 | 流的本质是**指针不是媒体**：「streams are just shortcuts to the real media」 | A2「Add streams」引言 |
| 11 | 指向类字段五选一必须：`url` / `ytId` / `infoHash` / `nzbUrl` / `externalUrl`；`infoHash` = torrent 的 info hash | A4「Stream Object」 |
| 12 | **`fileIdx`** 选 torrent/nzb/压缩包内视频文件下标；**省略时默认取体积最大文件** | A4「Stream Object」 |
| 13 | 画质通过 **`name`** 字段表达（「usually used for stream quality」）；描述用 `description`（旧 `title` 已弃用） | A4「Additional properties」 |
| 14 | `behaviorHints.notWebReady: true` 用于非 HTTPS 或非 MP4 的 HTTP 直链；`proxyHeaders` 依赖它 | A4「behaviorHints」 |
| 15 | `sources`（tracker/DHT 节点）可增强 torrent 的 peer 发现；DHT 可能违反私服规则 | A4「Additional properties」 |

### 3.3 Torrentio 配置 + Real-Debrid 链路（方向 B/C）

| # | 结论 | 依据 |
|---|------|------|
| 16 | Torrentio 支持的 Debrid：**RealDebrid / Premiumize / AllDebrid / DebridLink / EasyDebrid / Offcloud / TorBox / Put.io**，默认 None | B2/C1 配置页 |
| 17 | 画质过滤项：**Exclude Resolutions**（排除指定分辨率）+ **Video Size Limit**（`5GB` 或逗号分隔 `10GB,2GB`，**第一个=电影、第二个=剧集**） | B2/C1 配置页 |
| 18 | API Key 从所选 Debrid 服务商获取（「Find API Key →」入口；具体步骤需真实页面核实） | B2/C1 配置页（JS 渲染，未全量抓到） |
| 19 | RD「已缓存即播(instant availability)」原理：种子已在 RD 服务器缓存 → 无需等下载，直接拉流秒播 4K/Remux | C2 Issue #305 背景 |
| 20 | **2024-11 RD 移除「检查已缓存 info hash」端点** → Torrentio 短期丢失结果、无法再精确判断可即时播放的条目，**所有链接现标记为 `[RD download]`** | C2 Issue #305 |
| 21 | **坑**：不要勾选 Torrentio 的「Don't show download to debrid links」，否则可能看不到任何结果 | C2 Issue #305 |
| 22 | Torrentio 自建 **8 小时短期缓存**作替代信号，仅覆盖「经 Torrentio 添加且下载完成」的条目；RD 会周期清理缓存，故该缓存可能不准确；是临时方案 | C2 Issue #305 |

### 3.4 画质对比：影视站 vs Stremio torrent/debrid（方向 C）

| # | 结论 | 依据 |
|---|------|------|
| 23 | 影视站**很可能不支持 4K**；即使支持，画质也不如 torrent/debrid 源 | C3「Why should I use it over a movie website」 |
| 24 | Stremio 拿到的 **1080p 远优于影视站低码率高压缩内容** | C3 同段落 |
| 25 | 码率量化：**Netflix ≈ 2–3 Mbit/s；1080p 转码源 ≈ 6–7 Mbit/s；4K ≈ 10–80 Mbit/s**，建议 ≥100Mbit 链路 | C4 社区实测 |
| 26 | **Remux（30+GB 4K）可流播**：实测 Stremio + RD 跑满千兆；前提 RD 已缓存 + ≥100Mbit 链路 | C4 社区实测 |
| 27 | 码率 ≠ 画质：结合**文件大小 × 时长**估算；HEVC(10-bit)/AV1 压缩效率更高，优先 10-bit HEVC | C4 社区讨论 |
| 28 | **Electron 打包（stremio-web-desktop）强制转码锁 1080p、无原生 4K**；官方 stremio-shell（Qt6）才原生 4K | A5 README Disclaimer |
| 29 | 补救：官方桌面 app 加 `--webui-url=https://web.stremio.com/` 可拿 v5 Web UI + 原生播放 | A5 README「Solution」 |
| 30 | **Electron 锁 1080p 的技术机理源材料未解释**（推测：浏览器播放管线缺原生解码/DRM，回退服务端 ffmpeg 转码）——标注为推测 | A5（推断） |

### 3.5 中国网络环境 + 合规（缺口补齐）

| # | 结论 | 依据 |
|---|------|------|
| 31 | 架构上 Stremio 开源合法、不托管内容；用 Debrid 或 HTTP 流通常**不需要 VPN**，比 P2P 更安全 | WebSearch（stremio-perfect-setup 等） |
| 32 | **Torrentio 可能屏蔽 VPN**（换节点可解）；RD 阻止来自 VPN 的付款（付款前关 VPN） | WebSearch（Down On The Street / TROYPOINT） |
| 33 | 无中国本地化 Debrid 服务证据；支付需**虚拟信用卡或加密货币**；替代：TorBox / Premiumize / AllDebrid | WebSearch |
| 34 | 插件替代：Debridio（$10/年、不屏蔽 VPN）、Jackettio（接私服）、AIOStreams（自托管+代理）、Comet、MediaFusion | WebSearch |
| 35 | 合规：Stremio 本体合法；**torrent 类插件在美/欧/英法律下技术上构成版权侵权**；P2P 暴露 IP 有 ISP 通知风险；**Debrid 降低但不消除风险** | WebSearch（Dark Skies 等） |
| 36 | **中国《著作权法》定性无现有搜索结论**，需咨询中国法律专业人士——标注为未知 | WebSearch（无结果） |

---

## 四、矛盾点与不确定性（Contradictions）

1. **streaming server 是否仍必需**：2020 官方博客说「非标准格式/BitTorrent 需连 streaming server」；2026 官方 README 不再提 stremio-server。→ 建议以 README + 实测为准，笔记中如实呈现时间线差异。
2. **RD instant availability 现状**：Issue #305（2024-11）说 RD 移除了 cached-hash 端点；但社区普遍仍称「RD 秒播 4K」——实为 Torrentio 8h 短期缓存 + `[RD download]` 兜底的新常态，不等于机制被删。笔记需区分「历史机制」与「2024-11 后现状」。
3. **画质上限无官方数字**：官方从不明说 4K 上限；4K 能力取决于「播放器是否原生解码 + 源文件 + Debrid 缓存」。Electron 锁 1080p 是唯一明确的硬性限制。

---

## 五、实操指引（Practical Guidance）

### 部署 stremio-web（自托管 Web UI）
```bash
git clone https://github.com/stremio/stremio-web
cd stremio-web
docker build -t stremio-web .
docker run -p 8080:8080 stremio-web   # 打开 http://localhost:8080
```
或 Node 22+ / pnpm 11+：`pnpm install && pnpm start`。

> 注意：Web UI 只是壳。要「原生 4K 播放」优先用官方桌面 app（stremio-shell）加 `--webui-url`；Electron 打包方案会强制转码锁 1080p。

### 接高质量源（Torrentio + Real-Debrid）
1. 注册 Real-Debrid，拿 API Key（付款时关 VPN，防风控）。
2. 打开 `https://torrentio.strem.fun/configure`：选 Debrid Provider = RealDebrid + 填 API Key。
3. 画质过滤：Exclude Resolutions 排除 720p 以下；Video Size Limit 设 `10GB,2GB`（电影 10GB / 剧集 2GB）。
4. 安装链接（INSTALL / Copy Link）装进 Stremio。
5. **不要勾选「Don't show download to debrid links」**，否则 2024-11 后可能看不到结果。
6. 播放时优先选带 4K / REMUX / HEVC 标记的流；种子标 `[RD download]` = 需先下载到 RD，不代表立即播放。

### 判断资源画质
- 看「文件大小 × 时长」估算码率，别只看分辨率标签。
- 优先 10-bit HEVC / AV1 编码资源（画质/体积比好）。
- 4K 高码率需 ≥100Mbit 网络链路。

### 中国用户现实路径
- 工具可用性：Stremio 本体可访问性无一手证据；Torrentio 可能屏蔽 VPN → 换 Debridio/Jackettio 或自托管 AIOStreams。
- 支付：虚拟信用卡或加密货币；付款前关 VPN。
- 免费方案：P2P 直连（需 VPN，版权风险高）；HTTP 流插件（较安全但慢）。

---

## 六、开放问题（Open Questions）

1. **stremio-web 自托管后播放 torrent 到底需不需要额外 streaming server/stremio-server？**（官方口径 2020 vs 2026 差异）
2. **web.stremio.com / 自托管 Web UI 在浏览器里播 4K 的实际边界？**（Chromium 播放管线、解码能力）
3. **中国网络下 Stremio 生态的实际可用性？**（GFW 具体封锁情况无一手证据）
4. **RD 之外的 Debrid 性价比对比？**（TorBox/Premiumize 在 RD 风控场景的替代表现）
5. **网盘直链接入 Stremio 的成熟方案？**（类似 lunatv 的 PanSou 网盘路径在 Stremio 生态的等价物——暂无清晰答案，社区多为 Debrid 路线）

---

## 七、下游交接（Handoff to Outline）

### 核心叙事线
> 影视站采集源封顶 1080p（lunatv 路线）→ Stremio 走 torrent + Debrid 能到 **4K / Remux**（10–80 Mbit/s）→ 但 Web UI 本身不管画质，画质由「源 + addon 过滤 + 播放器是否原生解码」决定 → Electron 打包锁 1080p，官方桌面 app 才原生 4K → 部署建议：官方桌面 app + `--webui-url` 或自托管 Web UI + Torrentio/RD 接源。

### 可复用素材
- **stremio 架构图**：React UI ↔ stremio-core (Rust→WASM) + stremio-video
- **stream 对象最小示例**：`{ "title": "4K", "infoHash": "...", "fileIdx": 0 }`
- **Torrentio 配置命令/URL** 与三个关键参数（Debrid Provider / Exclude Resolutions / Video Size Limit）
- **码率对照表**：Netflix 2–3 / 1080p 转码 6–7 / 4K 10–80 Mbit/s；Remux 30+GB 实测可流播
- **Electron 锁 1080p 事实** + 官方替代（stremio-shell + `--webui-url`）
- **与 lunatv 对比表**：采集源（上限 1080p）vs torrent/debrid（4K/Remux）；lunatv 有网盘搜索内置，Stremio 走 Debrid 路线

### 需要标注为推断/待验证
- Electron 锁 1080p 技术机理（推测）
- 中国 GFW 对 Stremio/RD 的具体封锁（无一手证据）
- 中国著作权法适用性（需法律专业人士）
- streaming server 是否仍必需（官方口径差异）
