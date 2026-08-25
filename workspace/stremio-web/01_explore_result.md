# 探测结果 - stremio-web 项目：能看高质量资源吗？

> 项目：stremio-web · 阶段 1（探测式收集）· 2026-08-26
> 已确认方向：A（是什么+核心能力）+ B（部署与接入）+ C（高质量资源路线）

---

## 候选来源清单（按视角分组，已按 URL 去重）

### A. stremio-web 是什么 + 核心能力

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| A1 | [Stremio/stremio-web（官方仓库）](https://github.com/stremio/stremio-web) | GitHub | official | 5 | **核心**：官方 Web UI；React + stremio-core(Rust→WASM) + stremio-video 播放层；Docker 自托管；GPL-2.0 |
| A2 | [Stremio Addon Guide · Step 5: Providing streams](https://stremio.github.io/stremio-addon-guide/step5) | 官方文档 | official | 5 | stream 对象机制：torrent 流只需 infoHash；画质信息嵌在 title 文本（如 "4K"）而非结构化字段 |
| A3 | [官方博客 · stremio-web alpha 开源公告](https://blog.stremio.com/stremio-web-alpha-is-now-open-source/) | 官方博客 | official | 4.5 | 定位一手说明：高级流（非标准格式/BitTorrent）需连接 streaming server；MSE 播放 |
| A4 | [stremio-addon-sdk · Stream Object 参考](https://stremio.github.io/stremio-addon-sdk/api/responses/stream.html) | 官方文档 | official | 4 | stream 对象完整字段：fileIdx（torrent 选文件）、behaviorHints、sources（tracker/DHT） |
| A5 | [Zaarrg/stremio-web-desktop](https://github.com/Zaarrg/stremio-web-desktop) | GitHub | community | 3 | **画质上限关键**：Electron/Chromium 构建强制转码、无原生 4K（锁 1080p）；官方 stremio-shell 可原生 4K |

### B. 部署与接入

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| B1 | [Stremio/stremio-web（同 A1）](https://github.com/stremio/stremio-web) | GitHub | official | 5 | README 含官方 Docker 部署命令（`docker run -p 8080:8080 stremio-web`）；Node 22 + pnpm |
| B2 | [Torrentio 配置页](https://torrentio.strem.fun/configure) | 工具官方 | official | 5 | **接高质量源核心入口**：选 Debrid 提供商（RealDebrid 等）+ API Key、选 torrent 源、排除低清画质 |
| B3 | [mhdzumair/MediaFusion](https://github.com/mhdzumair/MediaFusion) | GitHub | implementation | 4 | 自托管一站式 Stremio addon：Docker Compose；聚合 Real-Debrid/AllDebrid/Premiumize/TorBox + Prowlarr/Jackett |
| B4 | [g0ldyy/annatar](https://github.com/g0ldyy/annatar) | GitHub | implementation | 4 | 极速（<3s）JIT torrent/debrid 搜索 addon，自托管 Torrentio 替代；docker-compose |
| B5 | [Stremio-Community/stremio-addons-list](https://github.com/Stremio-Community/stremio-addons-list) | GitHub | community | 3 | 社区 addon 总目录（2025-11 归档为只读，新目录迁往 stremio-addons.net） |

### C. 高质量资源路线

| # | 标题 | 来源 | tier | 评分 | 相关点 |
|---|------|------|------|------|--------|
| C1 | [Torrentio 配置页（同 B2）](https://torrentio.strem.fun/configure) | 工具官方 | official | 5 | Exclude Resolutions 分辨率过滤 + 视频大小上限设置，4K/Remux 画质筛选入口 |
| C2 | [Torrentio-scraper Issue #305 · RD integration](https://github.com/TheBeastLT/torrentio-scraper/issues/305) | GitHub | official | 5 | Real-Debrid「已缓存即播(instant availability)」机制与失效兜底，理解 4K Remux 秒播链路的一手来源 |
| C3 | [Viren070's Guides · Stremio Intro](https://guides.viren070.me/stremio/intro) | 教程 | implementation | 4 | 明确对比「影视站 1080p 低码率压缩」vs Stremio 高清 torrent/debrid 源；常规影视站大概率不支持 4K |
| C4 | [Streaming with high bit rates（码率深度讨论）](https://piefed.jeena.net/post/53866) | 社区 | community | 4 | 画质天花板量化：4K 约 10–80 Mbit/s、1080p 转码约 6–7 Mbit/s、Netflix 约 2–3 Mbit/s；30+GB Remux 可流播 |
| C5 | [Setup Stremio like a pro（r/Piracy 名帖转载）](https://programming.dev/comment/5583214) | 社区 | community | 3 | 一线实操：账号、设备选型（部分设备不支持 4K 流播）、无需 VPN、排障 |

> 去重说明：`stremio/stremio-web`（A1/B1）与 `torrentio.strem.fun/configure`（B2/C1）跨视角重复，分别保留在 A 与 C 组并在 P2 复用。

---

## 方向菜单（用户已选）

- **A. 是什么 + 核心能力**（推荐）→ 深读 A1/A2/A3/A4，把架构、stream 机制、画质上限讲透
- **B. 部署与接入** → 深读 B1/B3/B4，覆盖自部署、Torrentio/MediaFusion/Annatar 接 Debrid 高质量源
- **C. 高质量资源路线** → 深读 C1/C2/C3/C4，覆盖 4K/Remux 来源、RD 缓存机制、码率对比

用户已在阶段 0 选择 **A+B+C 全做**。

---

## 覆盖缺口（Gaps）

1. **中国网络环境**：Torrent 被墙、Real-Debrid 支付与访问、网盘替代方案（夸克/阿里云盘直链）缺一手来源。
2. **stremio-web 原生 4K 边界**：官方 stremio-web vs Electron 打包（锁 1080p）vs stremio-shell 的原生 4K 差异需在 P2 核实。
3. **与 lunatv 直接对比**：无一手来源直接对比「苹果CMS 采集源 vs Stremio+Debrid」；需 P2 用 C3/C4 数据整合推断。
4. **网盘直链接入 Stremio**：不像 lunatv 有内置网盘搜索模块，Stremio 网盘方案成熟度待查。
5. **法律/版权风险**：torrent/debrid 路线的合规提示需要补充。

---

## 预计 P2 范围

- **核心深读 5-6 个源**：A1（官方仓库/架构+Docker）、A2（addon stream 机制）、B2/C1（Torrentio 配置）、C2（RD 缓存机制）、C3（Viren070 对比）、B3（MediaFusion 自托管）。
- **补齐缺口**：画质上限边界（A5 佐证）、码率数据（C4）、与 lunatv 对比推断、中国网络环境与合规提示。
- **产出 `02_deep_research.md`**：scope、来源表、claim/source 映射、矛盾点、实操指引、开放问题。
