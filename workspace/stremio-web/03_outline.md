# 学习笔记大纲：《stremio-web 实战：从 1080p 采集源到 4K/Remux Debrid 观影路线》

> 笔记类型：实战笔记
> 面向读者：已跑通 lunatv 影视站采集源聚合（理解聚合播放器概念）、想升级到 4K/Remux 高质量观影路线的用户
> 核心问题：stremio-web 能看高质量资源吗？如何部署与接入影视资源？
> 预计总篇幅：约 6000-7500 字
> 章节数：6 章

---

### 第一章：认识 stremio-web：一个不含资源的「聚合客户端」

- **目标**：理解 stremio-web 是什么、与官方客户端/桌面 app 的关系，以及它为什么本身不提供资源；为后续配置 addon 和 Debrid 建立认知基础。
- **章节结构**：
  - ### 1.1 项目定位：官方 Web UI
    - stremio-web 是 Stremio 官方 Web 界面（React 应用），可安装为 PWA；官方线上实例为 web.stremio.com
    - 与桌面 app / 安卓 app 的关系：官方明确「Web 版不是桌面/安卓版的替代品」
  - ### 1.2 架构：React UI ↔ stremio-core (Rust→WASM) ↔ stremio-video
    - stremio-core 是 Rust 引擎编译为 WASM、跑在 Web Worker；「UI 渲染状态，core 计算状态」
    - 播放层由 stremio-video 抽象，按环境选择播放器实现
    - 时间线差异（标注为待核实）：2020 官方博客称非标准格式/BitTorrent 需连 streaming server；2026 README 已不再提及 stremio-server
  - ### 1.3 核心认知：流是指针，不是媒体
    - addon 返回的是「流的指针」（infoHash / url / ytId 等），不是视频文件本身
    - 画质由「源文件质量 + 播放/转码链路」决定，官方不承诺画质上限
- **篇幅估计**：约 700-900 字（短）
- **素材引用**：[A1]、[A2]、[A3]、[A4]
- **代码示例**：无（含一张架构关系图：React UI ↔ stremio-core ↔ stremio-video）

### 第二章：客户端选型：为什么 Electron 版会锁 1080p

- **目标**：在部署前做对客户端选型，避开「装完才发现看不了 4K」的坑；明确哪条路径能原生播放 4K。
- **章节结构**：
  - ### 2.1 三条路线对比
    - 路线 A：自托管 Web UI（stremio-web）——浏览器播放，受浏览器解码能力约束
    - 路线 B：Electron 打包（stremio-web-desktop）——硬性锁 1080p、无原生 4K
    - 路线 C：官方桌面 app（stremio-shell）+ `--webui-url=https://web.stremio.com/` 拿 v5 Web UI + 原生播放
  - ### 2.2 Electron 锁 1080p 的事实与机理
    - 事实：stremio-web-desktop 的 Disclaimer 明确「强制转码锁 1080p、无原生 4K」
    - 机理：源材料未解释，推测为浏览器播放管线缺原生解码/DRM、回退服务端 ffmpeg 转码（明确标注为推测）
  - ### 2.3 选型结论
    - 追求 4K/Remux：优先官方桌面 app + `--webui-url`
    - 仅想轻量体验：自托管 Web UI
- **篇幅估计**：约 800-1000 字（中）
- **素材引用**：[A1]、[A3]、[A5]
- **代码示例**：`stremio --webui-url=https://web.stremio.com/` 启动参数

### 第三章：自托管 stremio-web：把 Web UI 跑起来

- **目标**：动手完成 stremio-web 的 Docker/Node 自托管部署，验证能打开 UI，并理解「Web UI 只是壳」。
- **章节结构**：
  - ### 3.1 Docker 部署
    - `git clone https://github.com/stremio/stremio-web`
    - `docker build -t stremio-web .` 与 `docker run -p 8080:8080 stremio-web`
    - 打开 http://localhost:8080
  - ### 3.2 非 Docker 方式（Node 22+ / pnpm 11+）
    - `pnpm install && pnpm start`
  - ### 3.3 部署后的认知
    - 可安装为 PWA
    - Web UI 只是壳：资源要接 addon（第 4 章）、高质量要接 Debrid（第 5 章）
- **篇幅估计**：约 600-800 字（短）
- **素材引用**：[A1]
- **代码示例**：Docker 构建/运行命令、pnpm 启动命令

### 第四章：Addon 机制与 Torrentio：给 Stremio 接上影视资源

- **目标**：理解 addon 的 stream 协议，并把 Torrentio（torrent 资源聚合 addon）装进 Stremio，看到可播放的流列表。
- **章节结构**：
  - ### 4.1 Addon 机制与 stream 对象
    - 五选一指向字段：url / ytId / infoHash / nzbUrl / externalUrl
    - `fileIdx`：torrent/nzb 内视频文件下标，缺省取体积最大文件
    - `name` 表达画质、`description` 做描述（旧 `title` 已弃用）
    - `behaviorHints.notWebReady` 用于非 HTTPS/非 MP4 的 HTTP 直链
    - stream 最小示例：`{ "name": "4K", "infoHash": "...", "fileIdx": 0 }`
  - ### 4.2 Torrentio 三步接入
    - 打开配置页 `https://torrentio.strem.fun/configure`
    - 三个关键参数：Debrid Provider / Exclude Resolutions / Video Size Limit
    - 复制 INSTALL / Copy Link 装进 Stremio
  - ### 4.3 常见坑
    - 不要勾选「Don't show download to debrid links」，否则 2024-11 后可能看不到结果
    - 带 `[RD download]` 标记 = 需先下载到 Debrid，不代表立即播放
- **篇幅估计**：约 1200-1500 字（长）
- **素材引用**：[A2]、[A4]、[B2/C1]、[C2]
- **代码示例**：stream JSON 最小示例、Torrentio configure URL、Exclude Resolutions / Video Size Limit 参数示例

### 第五章：Real-Debrid：把 4K/Remux 真正拉起来

- **目标**：掌握 Debrid 高质量链路的核心——注册 RD、拿 API Key、配置过滤，理解「秒播 4K」的原理与 2024-11 后的新常态。
- **章节结构**：
  - ### 5.1 Debrid 是什么、为什么能秒播 4K
    - Debrid 服务商（RD 等）把 torrent 缓存到自己的服务器，客户端直接拉流
    - 历史机制：RD「已缓存即播（instant availability）」→ 无需等下载
    - 2024-11 变化：RD 移除缓存检查端点 → Torrentio 用 8 小时短期缓存兜底，所有链接标记为 `[RD download]`（区分历史机制与现状）
  - ### 5.2 Real-Debrid 接入实操
    - 注册 RD 并获取 API Key（付款前关 VPN，防风控）
    - Torrentio 选 Debrid Provider = RealDebrid + 填 API Key
    - Video Size Limit 实战：`10GB,2GB`（第一个=电影、第二个=剧集）
  - ### 5.3 判断资源画质
    - 别只看分辨率标签：用「文件大小 × 时长」估算码率
    - 优先 10-bit HEVC / AV1 编码资源
    - 4K 高码率需 ≥100Mbit 网络链路
- **篇幅估计**：约 1200-1500 字（长）
- **素材引用**：[B2/C1]、[C2]、[C4]
- **代码示例**：RD API Key 获取路径、Torrentio Debrid 配置项、Video Size Limit 示例

### 第六章：画质对比：lunatv 采集源 vs Stremio torrent+Debrid

- **目标**：用量化数据回答「stremio-web 能看高质量资源吗」，对比 lunatv 与 Stremio 两条路线的画质上限，并结合中国网络环境给出最终选型与合规提示。
- **章节结构**：
  - ### 6.1 码率量化对照
    - Netflix ≈ 2-3 Mbit/s；1080p 转码源 ≈ 6-7 Mbit/s；4K ≈ 10-80 Mbit/s
    - Remux（30+GB 4K）实测可流播（前提：RD 已缓存 + ≥100Mbit 链路）
  - ### 6.2 lunatv vs Stremio 对比表
    - 画质上限：影视站采集源封顶 1080p vs torrent+Debrid 可达 4K/Remux
    - 资源路径：网页采集 vs 磁力/Debrid 缓存
    - 同是 1080p 时：Stremio 源也远优于低码率高压缩的影视站内容
    - 生态差异：lunatv 有网盘搜索内置；Stremio 走 Debrid 路线，网盘直链无成熟等价物（标注为待探索）
  - ### 6.3 中国网络环境与合规
    - 可用性：Stremio 开源合法、不托管内容；Debrid/HTTP 流通常不需要 VPN，比 P2P 更安全
    - 风险：Torrentio 可能屏蔽 VPN；RD 付款风控；P2P 直连暴露 IP 有 ISP 通知风险
    - 支付：虚拟信用卡 / 加密货币；无中国本地化 Debrid 服务（替代：TorBox / Premiumize / AllDebrid）
    - 合规：torrent 类插件在美/欧/英法律下构成版权侵权风险；中国《著作权法》定性无现有结论（需咨询法律专业人士，标注为未知）
  - ### 6.4 最终结论与选型建议
    - 能看高质量资源：能，走 torrent+Debrid 路线可达 4K/Remux；Web UI 本身不管画质
    - 一句话选型：官方桌面 app（+`--webui-url`）或自托管 Web UI + Torrentio/Real-Debrid 接源
- **篇幅估计**：约 1200-1500 字（长）
- **素材引用**：[C3]、[C4]、[C2]、[A5] + WebSearch（中国网络/合规）
- **代码示例**：无（含码率对照表 + lunatv vs Stremio 对比表）

---

## 学习路径说明

### 前置要求
- 已跑通 lunatv 或任一影视站采集源聚合（聚合播放器概念相通）
- 有 Docker 基础，或 Node.js 22+ / pnpm 11+ 环境
- 理解磁力链/torrent 基本概念（种子、info hash）
- 走高质量路线需要海外支付渠道（虚拟信用卡/加密货币）以购买 Debrid 服务

### 学完能做什么
- 自托管 stremio-web Web UI 并理解其架构边界
- 选对客户端路线（避开 Electron 锁 1080p 的坑）
- 通过 Torrentio addon 为 Stremio 接入 torrent 影视资源
- 接入 Real-Debrid 并配置 4K/Remux 高质量源过滤
- 用「文件大小 × 时长 / 码率」等量化指标判断资源画质
- 明确 lunatv 与 Stremio 两条路线的定位差异，做出符合自身网络环境的选型

### 建议学习顺序
- 第 1 → 2 → 3 章顺序阅读（先理解架构与选型，再动手部署）
- 第 4、5 章建议连着做（addon 配置 + Debrid 链路是同一实操链路）
- 第 6 章是结论章，可随时参考
- 预计总耗时：2-3 小时（含部署与配置实操）
