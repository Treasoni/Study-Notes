# 03 学习笔记大纲 - 自建代理节点

> 笔记类型：实战笔记（前部概念铺垫 + 后部可照做的搭建流程）
> 方向：B 内核直配（Xray-core 原生配置，概念与字段对齐）
> 预计总篇幅：约 7500 字（目标区间 6000-9000）
> 章节数：6 章（概念 2 章 + 实战 4 章，概念章全部排在实战章之前）
> 信源基线：全部 tier-1；以下「素材引用」中的 ID 均对应 `02_deep_research.md` 信源表
> 写作边界：不写获取渠道、订阅链接、机场推荐或任何规避监管的操作指引；不做无信源的性能断言
> 推断标注：凡 `02_deep_research.md` 标为 inference 的内容，正文必须显式写「据官方文档归纳 / 推断」，不得写成官方口径

## 结构总览

- 概念部分（第 1-2 章）：先建立配置模型与 REALITY 原理，为第 4-5 章的字段配对提供依据。
- 实战部分（第 3-6 章）：VPS 硬化基线 → 服务端 → 客户端 → 连通校验，按官方示例的真实结构展开。

---

### 第一章：分层模型——代理协议之外的传输三件事

- **篇幅**：中（约 1200 字）
- **节结构**：
  - 1.1 为什么两端必须对齐（`streamSettings` 只管代理协议之外的数据传输；一端 WebSocket 另一端也必须 WebSocket）
  - 1.2 承载方式 method（取值域 `raw|xhttp|mkcp|grpc|websocket|httpupgrade|hysteria`，默认 `raw`；专属 Settings 只在对应 method 生效）
  - 1.3 安全层 security（`none|reality|tls`，默认 `none`；TLS 与全部七种承载方式可组合）
  - 1.4 组合硬约束（hysteria 必须 tls；raw/xhttp/grpc 在 none/tls/reality 下均可；REALITY 仅 RAW/XHTTP/gRPC）
  - 1.5 附加配置与直接出站（`finalmask` / `sockopt` 不参与协商；freedom 直接出站只有 `sockopt`）
- **覆盖要点**：三层分工、两端兼容约束、组合合法性、`security=none` 时 VLESS/Trojan 仅限私网
- **素材引用**：S-1
- **代码/配置示例**：有（`streamSettings` 最小 JSON 片段，标注各字段默认值）
- **含推断**：是——组合硬约束表为「据 S-1 官方速查表归纳」；附加配置层语义 confidence: medium，须标注

### 第二章：REALITY 原理——不是新协议，是 TLS 的变体

- **篇幅**：中（约 1300 字）
- **节结构**：
  - 2.1 设计意图与官方收益（借用目标站 TLS 外观与握手特征；Go 1.19.5 `tls` fork；消除服务端指纹、保持前向保密、证书链攻击失效、无需买域名）
  - 2.2 目标站要求（境外、支持 TLSv1.3 与 H2、域名不重定向；加分项：IP 邻近、握手后报文已加密、OCSP Stapling）
  - 2.3 鉴权与回落语义（鉴权失败直接转发至 `target`；代价与缓解；回落限速是特征、官方不建议启用）
  - 2.4 客户端证书三分支与 spider 模式（临时可信证书 / 真实证书 / 无效证书）
  - 2.5 适用边界与路线图（非 XTLS 协议配 REALITY 不推荐，会呈现 TLS-in-TLS 特征；prebuilt mode / 0-RTT）
- **覆盖要点**：REALITY 与 TLS 的关系、回落为何能成立、三分支语义、边界
- **素材引用**：S-2, S-6c（背景可参 S-3，但不逐字引用，因未精读）
- **代码/配置示例**：无（纯原理章；仅用 `dest`/`serverNames` 名称示意，不计为配置示例）
- **含推断**：是——回落被 CDN 偷跑流量的代价与缓解（confidence: medium）；限速本身是特征

### 第三章：落地前的 VPS 硬化与运维基线

- **篇幅**：中（约 1300 字，压缩为 1 章，按需取用 S-10 系列，不逐节搬）
- **节结构**：
  - 3.1 安全策略与风险模型（要保护什么/防什么/谁来做；Security is a process；短边界优于长边界；优先停用不需要的服务，包过滤是补充）
  - 3.2 防火墙 nftables（表/链/verdict 语义；`/etc/nftables.conf` 持久化与 `systemctl enable nftables`；`iptables-translate` 迁移路径）
  - 3.3 fail2ban（定位与机制、能力边界、配置四类文件、`jail.d/` 覆盖约定、默认 `bantime/findtime/maxretry = 10m/10m/5`）
  - 3.4 监控与完整性校验（logcheck 默认 server 模式、AIDE 基线库局限、`dpkg -V` 局限、suricata 按有效性约束）
  - 3.5 拥塞控制 sysctl（`tcp_congestion_control` / `tcp_available_congestion_control` / `tcp_allowed_congestion_control` / `tcp_ecn` / `tcp_slow_start_after_idle`）
  - 3.6 被入侵后的处置顺序（发现线索 → 断网 → 保全证据 → 重装 → 取证分析；成像/重装/分析存在交叠）
- **覆盖要点**：硬化最小集、fail2ban 正确改法、nftables 默认框架、处置顺序的官方交叠
- **素材引用**：S-10, S-10a, S-10b, S-10c, S-11, S-12
- **代码/配置示例**：有（nft 最小规则集、`jail.d` 片段、sysctl 键名）
- **含推断**：是——面向 VPS 的最小开放规则集为自行编写（S-10a 只给语法与装载方式，须标 inference）；切换拥塞算法前提 confidence: medium；BBR 未在内核文档点名，只写参数名不做性能断言

### 第四章：服务端配置——VLESS + XTLS Vision + REALITY

- **篇幅**：长（约 1600 字，核心实战章）
- **节结构**：
  - 4.1 服务端骨架（`inbounds[0]`：`port 443`、`protocol vless`、`network tcp`、`security reality`；`decryption: "none"`；`clients[0]` 的 `id`(UUID) 与 `flow: "xtls-rprx-vision"`）
  - 4.2 REALITY 服务端四参数（`target`(必填，旧称 `dest`)、`serverNames`(必填，不支持 `*`)、`privateKey`(`./xray x25519`)、`shortIds`(必填)）
  - 4.3 路由与嗅探（`sniffing.destOverride: [http,tls,quic]` + `routeOnly: true`；`outbounds` 单 freedom `tag: direct`）
  - 4.4 进阶字段（`mldsa65Seed`/`mldsa65Verify`、`xver`、`maxClientVer`/`minClientVer`/`maxTimeDiff`、`show`）
  - 4.5 新旧命名与字段表口径（`target` ↔ `dest` 别名；字段表一律以 `DOCSRC_reality.md` 为准，不抄抓取版）
- **覆盖要点**：可照抄的服务端配置结构、四参数生成与含义、嗅探路由、别名过渡
- **素材引用**：S-2, S-6a, S-6c
- **代码/配置示例**：有（完整服务端 `config.json`）
- **含推断**：否——字段语义均有官方原文/示例支撑；仅需交代新旧命名

### 第五章：客户端配置——结构对称与字段配对

- **篇幅**：中（约 1200 字）
- **节结构**：
  - 5.1 客户端骨架（本地 SOCKS 入站 `127.0.0.1:10808`、`settings.udp: true`）
  - 5.2 出站与传输层对齐（`protocol vless`、`address`/`port`/`id`/`encryption: "none"`/`flow`、`tag: "proxy"`；`id` 必须与服务端 `clients[0].id` 一致）
  - 5.3 客户端 REALITY 字段（`password`(旧称 `publicKey`)、`serverName`、`shortId`、`fingerprint`、`spiderX`）
  - 5.4 配对关系与地雷（`shortId` 长度为 2 的倍数、最大 16；`fingerprint` 不得用 `unsafe`；客户端绝不能填 `target`；指定 flow 后客户端必须启用 XTLS）
- **覆盖要点**：客户端与服务端传输层结构对称、五字段配对关系、易错点
- **素材引用**：S-2, S-6b, S-6c
- **代码/配置示例**：有（完整客户端 `config.json`）
- **含推断**：否——字段语义与约束均来自官方文档/示例

### 第六章：连通校验与字段对齐排错

- **篇幅**：中（约 1000 字）
- **节结构**：
  - 6.1 本地 SOCKS 自检（起客户端后经 `127.0.0.1:10808` 验证链路）
  - 6.2 字段配对检查清单（`id`、`password` ↔ `privateKey`、`serverName` ∈ `serverNames`、`shortId` ∈ `shortIds`、`flow` 一致）
  - 6.3 新旧命名对不上（S-6a/S-6b 用 `dest`/`publicKey`，S-2 用 `target`/`password`；两处都在 tier-1 官方源里）
  - 6.4 失败信号解读（`shortId` 奇数位报错并自动补 0、`serverName` 不匹配、进入 spider 模式的含义）
- **覆盖要点**：校验路径、配对清单、命名过渡陷阱、失败信号
- **素材引用**：S-6b, S-2, S-6c，并引 `02_deep_research.md` 第五节「矛盾、别名与注意点」
- **代码/配置示例**：有（校验用最小命令/片段）
- **含推断**：是——「连通校验」无官方端到端教程，校验方法与排错树为据配置结构归纳，全章须标注为推断；不写订阅/分享链接（无 tier-1 规范）

---

## 学习路径说明

### 前置要求

- Linux 基础：SSH 公钥登录、systemd 服务与 `journalctl` 日志
- 一台可自由配置的 VPS（本笔记只写技术方案与搭建流程，不涉及选购渠道）
- 能读 JSON/JSONC 配置；理解 TCP、端口、TLS 的基本概念（不必精通握手细节）
- 客户端侧代理概念（对应已有 `ubuntu-server-proxy-docker` 笔记，本篇不重复）

### 学完能做什么

- 说清 `streamSettings` 的三层分工与组合硬约束，能判断某个 method + security 组合是否合法
- 解释 REALITY 的伪装原理与回落语义，理解为何当前主线是 VLESS + XTLS Vision + REALITY
- 独立写出服务端与客户端 Xray 配置，并完成五字段配对
- 按最小开放原则硬化一台 VPS，用 fail2ban 与 sysctl 做基础运维，并知道被入侵后的处置顺序
- 配置对不上时，按检查清单定位到具体字段

### 建议学习顺序

- 按 1 → 6 顺序阅读；第 1-2 章是概念地基，务必先读，后续实战依赖其中的分层与字段依据
- 只想尽快部署：可 1 → 2 → 4 → 5 → 6，把第 3 章硬化在对外暴露 443 前回补
- 建议时长：概念（1-2 章）约 1.5 小时；实战（4-6 章）约 2-3 小时；硬化运维（3 章）约 1 小时

### 已知缺口（写作时按此处理，不补全）

- 分享链接与订阅格式无 tier-1 规范：本篇剔除，不在第 6 章展开
- BBR 未在内核文档点名：只写 sysctl 参数名，不做性能断言
- 协议横向对比无官方对照文档：不单列对比章；如涉及只标 inference
- 客户端 GUI（mihomo/Clash 系）未纳入本次方向：不立章
