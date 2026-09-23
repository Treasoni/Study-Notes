# 02 深度素材 - VPS 自建节点零基础全流程（面板流）

- **运行标识**: vps-node-panel-tutorial
- **阶段**: P2（深度收集）
- **检索日期**: 2026-09-23（抓取）／2026-09-24（父流程复核）
- **来源总数**: 21（全部落盘于 `./sources/{ID}.md`，全部经 curl 或 crawl 实际取回，无编造条目）
- **tier 分布**: official 20 / primary-research 1（A-2）／community 0（原定 B-5 未能取回，见 §3）
- **派发记录**: 第一轮 3 个并发子代理（概念与协议 / 落地与厂商 / 域名与加固）；第二轮 1 个顺序子代理（缺口补读）

---

## 1. 范围与写作约束

### 1.1 本项目的硬约束（下游写作必须遵守）

1. **来源视频无字幕轨**（人工、自动均无，经 yt-dlp 多 player client 与 watch 页 `ytInitialPlayerResponse` 双重核验）。
   因此**视频的口播结论不可引用、不可转述**。视频只用作**章节顺序骨架**，正文事实一律来自本文件的来源。
   凡涉及"视频里说……"的表述一律禁止。
2. **每条事实性论断必须挂来源 ID + anchor**，格式见 §4。anchor 指向 `./sources/{ID}.md` 中的小节名或字段名，写作时可回源核对。
3. **价格、套餐、版本号均标注观测日 2026-09-23**，属易失信息，正文须写明"以观测日为准"。
4. **不得把行业通用说法写成官方口径**。§6 列出的无官方来源项，正文必须显式降级表述。

### 1.2 素材可用度总览

| 状态 | 来源 |
|---|---|
| 完整可用 | A-1 ~ A-8、B-1、B-2、B-4、B-6、C-1、C-2、C-3、C-4、C-5、C-6、C-7、C-8 |
| 部分可用（正文被 JS 门控） | **B-3**（搬瓦工：仅 KiwiVM 说明与 OS 列表可用，套餐与价格不可得） |
| 未能取回 | **B-5**（作者 Notion 配套文档：Playwright 导航 60s 超时，Notion 在本网络不可达） |

---

## 2. 来源表

| ID | 标题 | URL | Tier | 文件 | 观测日 |
|---|---|---|---|---|---|
| A-1 | 出站代理（Mux、XUDP）\| Project X | https://xtls.github.io/config/outbound.html | official | `sources/A-1.md` | 常青页 |
| A-2 | Understanding the "Airport" Censorship Circumvention Ecosystem in China | https://arxiv.org/abs/2606.18427 | primary-research | `sources/A-2.md` | 2026-06-16 |
| A-3 | MHSanaei/3x-ui 官方仓库 | https://github.com/MHSanaei/3x-ui | official | `sources/A-3.md` | 常青页 |
| A-4 | Shadowsocks SIP022（2022 版协议规范） | https://shadowsocks.org/doc/sip022.html | official | `sources/A-4.md` | 常青页 |
| A-5 | VLESS（XTLS Vision Seed）\| Project X | https://xtls.github.io/config/outbounds/vless.html | official | `sources/A-5.md` | 常青页 |
| A-6 | VMess \| Project X | https://xtls.github.io/config/outbounds/vmess.html | official | `sources/A-6.md` | 常青页 |
| A-7 | Trojan \| Project X | https://xtls.github.io/config/outbounds/trojan.html | official | `sources/A-7.md` | 常青页 |
| A-8 | Shadowsocks（Xray 出站）\| Project X | https://xtls.github.io/config/outbounds/shadowsocks.html | official | `sources/A-8.md` | 常青页 |
| B-1 | 3x-ui 官方 Installation 文档 | https://github.com/MHSanaei/3x-ui/wiki/Installation | official | `sources/B-1.md` | 常青页 |
| B-2 | RackNerd KVM VPS 官方产品页 | https://racknerd.com/kvm-vps | official | `sources/B-2.md` | 2026-09-23 |
| B-3 | BandwagonHost VPS Hosting（部分） | https://bandwagonhost.com/vps-hosting.php | official | `sources/B-3.md` | 2026-09-23 |
| B-4 | FinalShell 官网下载与版本页 | https://www.hostbuf.com/t/988.html | official | `sources/B-4.md` | 2025-05-21 |
| B-6 | CloudCone 官方 VPS 产品页 | https://cloudcone.com/vps/ | official | `sources/B-6.md` | 2026-09-23 |
| C-1 | Cloudflare DNS — Proxy status | https://developers.cloudflare.com/dns/proxy-status/ | official | `sources/C-1.md` | 常青页 |
| C-2 | Cloudflare DNS — Proxying limitations | https://developers.cloudflare.com/dns/proxy-status/limitations/ | official | `sources/C-2.md` | 常青页 |
| C-3 | fail2ban jail.conf(5) 手册页（Debian bookworm） | https://manpages.debian.org/bookworm/fail2ban/jail.conf.5.en.html | official | `sources/C-3.md` | 常青页 |
| C-4 | OpenSSH sshd_config(5) 手册页 | https://man.openbsd.org/sshd_config | official | `sources/C-4.md` | 常青页 |
| C-5 | DigitalOcean — How to Rebuild Droplets | https://docs.digitalocean.com/products/droplets/how-to/rebuild/ | official | `sources/C-5.md` | 常青页 |
| C-6 | 阿里云 ECS 产品概览 | https://help.aliyun.com/zh/ecs/product-overview/what-is-ecs | official | `sources/C-6.md` | 常青页 |
| C-7 | Vultr — How to configure networking | https://docs.vultr.com/how-to-configure-networking-on-vultr-cloud-servers | official | `sources/C-7.md` | 常青页 |
| C-8 | Vultr — Do Snapshots Retain the IP Address…? | https://docs.vultr.com/support/products/compute/do-snapshots-retain-... | official | `sources/C-8.md` | 常青页 |

---

## 3. 素材可用性问题（写作前必读）

1. **B-5（作者 Notion 配套文档）未能取回。** Playwright 导航 60s 超时，重试与 curl 均不稳定（曾返回 `000`）。
   后果：**视频作者自述的操作顺序与参数取值无法作为来源**。面板安装步骤一律以 B-1（官方 wiki）为准。
   正文如需提及"视频配套文档"，只能作为延伸阅读链接出现，且不得引用其内容。
2. **B-3（搬瓦工）套餐区被 JS 门控**，抓取结果仅剩 `Loading...`。仅 KiwiVM 能力与可选 OS 列表可用。
   后果：**不要写搬瓦工的具体套餐与价格**；如正文需要第三方厂商价格对照，只能用 B-2（RackNerd）与 B-6（CloudCone）。
3. **A-1 的定位需修正。** P1 曾把 A-1 标为"四种代理协议的权威定义来源"，实际抓回的是 **Mux / XUDP 出站通用配置**页，
   只列协议名而不给定义。该缺口已由 **A-5 / A-6 / A-7 / A-8** 四个协议专页补齐（第二轮补抓）。
   A-1 现用途：出站通用字段、Mux 语义、UDP/443 处理。
4. **C-3 / C-4 的部分条目属"归属推断"。** 两个 man page 抓取后 `[DEFAULT]` / `KEYWORDS` 的 `<dt>` 参数名被剥离并合并为长段落，
   子代理按字母顺序与行内交叉引用推定了参数归属并已标注 `| inferred`。
   父流程已回源验证参数名**确实出现在文件内**（`bantime`×2、`findtime`×3、`maxretry`×2、`ignoreip`×2、
   `PermitRootLogin`×1、`MaxAuthTries`×2 等），故语义可用；但**引用具体默认数值前必须回源人工确认**。
5. **A-4（Shadowsocks SIP022 规范）深度远超本篇需要。** 它是协议规范（密钥派生、重放保护窗口、salt 保存时长），
   对零基础读者过深；本篇只取"2022 版定义 + 不提供前向保密"两条，其余不入正文。

---

## 4. Claim / Source 映射

> 格式：`claim` ｜ `来源ID` ｜ `anchor` ｜（可选）原文短引
> 下游写作时按 ID 回 `sources/{ID}.md` 核对，**不要直接沿用本文件的措辞**。

### 4.1 「什么是 VPS / 云服务器」

- 云服务器 ECS 是 IaaS 级云计算服务，免去采购硬件、即开即用可弹性伸缩 ｜ C-6 ｜ 开篇定义段 ｜ quote: "IaaS（Infrastructure as a Service）级别云计算服务"
- 计费资源含 vCPU/内存、镜像、块存储、公网带宽、快照 ｜ C-6 ｜ 产品计费
- 计费方式含包年包月、按量付费、抢占式实例等 ｜ C-6 ｜ 产品计费
- 实例创建后地域等元数据确定，**无法更换地域** ｜ C-6 ｜ 部署建议
- DDoS 基础防护默认开启且免费，提供不超过 5 Gbps 防护 ｜ C-6 ｜ 部署建议-安全方案
- 官方推荐使用 VPC 并自行规划私网 IP；安全组免费 ｜ C-6 ｜ 部署建议
- ⚠ C-6 **通篇未使用"VPS"一词**，只讲"云服务器 ECS"。正文使用"VPS"时须说明这是业界俗称，并给出与 ECS 的对应关系（**此为推断**，需在正文标注）。

### 4.2 四种代理协议（面板里要选的那个东西）

**VLESS**
- 无状态轻量传输协议，分入站与出站 ｜ A-5 ｜ 简介段 ｜ quote: "无状态的轻量传输协议"
- 与 VMess 不同，**不依赖系统时间**，认证用 UUID ｜ A-5 ｜ 简介段
- ⚠ WARNING：**必须配合传输安全层**；仅对端为 private 地址且链路受信、或已启用 `VLESS Encryption` 时，才允许 `security: "none"` ｜ A-5 ｜ WARNING
- `encryption` 不能留空，禁用须显式设 `"none"` ｜ A-5 ｜ `encryption`
- `flow` 取值：空（普通 TLS）、`xtls-rprx-vision`、`xtls-rprx-vision-udp443` ｜ A-5 ｜ `flow`
- XTLS 仅在 TCP+TLS/REALITY，或无底层传输限制的 VLESS Encryption 下可用 ｜ A-5 ｜ `flow`
- `id` 可为任意小于 30 字节字符串或合法 UUID ｜ A-5 ｜ `id`

**VMess**
- 加密传输协议 ｜ A-6 ｜ 首段
- ⚠ DANGER：**依赖系统时间**，UTC 误差须在 120 秒内（时区无关） ｜ A-6 ｜ DANGER ｜ quote: "误差在 120 秒之内，时区无关"
- `security` 取值 `aes-128-gcm` / `chacha20-poly1305` / `auto`，默认 `auto`，服务端自动识别 ｜ A-6 ｜ `security`
- 服务端无 AES 加速时仍须手动设 `chacha20-poly1305` ｜ A-6 ｜ `security`
- 性能：支持 AES 加速时 Chacha20 比 AES-128-GCM 慢约 48%；不支持时 AES-128-GCM 耗时高出 2000% 以上 ｜ A-6 ｜ `security`
- **VMess 页无传输安全层强制告警**（与 VLESS/Trojan 不同） ｜ A-6 ｜ 全页

**Trojan**
- ⚠ WARNING：**必须配合 TLS** ｜ A-7 ｜ WARNING ｜ quote: "必须配合传输安全"
- ⚠ 公网还要求启用 Mux；否则内层载荷若也是 TLS 就形成 TiT，**很容易被检测**（附 PoC Trojan-killer） ｜ A-7 ｜ WARNING ｜ quote: "很容易被检测"
- `address` / `password` 必填 ｜ A-7 ｜ `address`、`password`

**Shadowsocks（Xray 出站）**
- 支持 TCP 与 UDP，UDP 可选择关闭 ｜ A-8 ｜ 兼容性
- 推荐加密：`2022-blake3-aes-128-gcm` / `2022-blake3-aes-256-gcm` / `2022-blake3-chacha20-poly1305` ｜ A-8 ｜ 推荐加密方式
- 2022 版提升性能并带**完整重放保护**，解决旧协议四类问题（AEAD 设计漏洞、TCP 重放误报随时间增加、**无 UDP 重放保护**、可用于主动探测的 TCP 行为） ｜ A-8 ｜ 兼容性
- 2022 用类似 WireGuard 的预共享密钥，`openssl rand -base64 <长度>` 生成；密钥长度 16 / 32 / 32 ｜ A-8 ｜ `password` 密钥长度表
- 旧加密方法密码不限长度，但建议 16 字符或更长 ｜ A-8 ｜ `password`

**Shadowsocks（协议规范侧，仅两条入正文）**
- SIP022 定义 Shadowsocks 2022 版 ｜ A-4 ｜ Abstract
- **不提供前向保密** ｜ A-4 ｜ 1. Overview ｜ quote: "does not provide forward secrecy"

**出站通用 / 进阶（A-1）**
- `protocol` 可选值含 blackhole/dns/freedom/http/loopback/shadowsocks/socks/trojan/vless/vmess/hysteria/wireguard ｜ A-1 ｜ protocol
- 出站 `tag` 非空时须全局唯一 ｜ A-1 ｜ tag ｜ quote: "必须在所有 `tag` 中 **唯一**"
- Mux 目标是降低 TCP 握手延迟**而非提升吞吐**，看视频/下载/测速通常反效果，只需客户端启用 ｜ A-1 ｜ MuxObject ｜ quote: "而非提高连接的吞吐量"
- `mux.concurrency` 范围 1–128，省略或 0 均为 8 ｜ A-1 ｜ concurrency
- `xudpProxyUDP443` 默认 `reject`，浏览器一般回落 TCP HTTP2 ｜ A-1 ｜ xudpProxyUDP443

### 4.3 面板：3x-ui 是什么、装什么

- 3X-UI 是管理 Xray-core 服务器的开源 Web 控制面板 ｜ A-3 ｜ Features 前导段 ｜ quote: "an advanced, open-source web control panel"
- 是原 X-UI 的增强 fork，新增更广协议支持与按客户端流量统计 ｜ A-3 ｜ Features 前导段
- 支持入站协议含 VLESS、VMess、Trojan、Shadowsocks、WireGuard、AmneziaWG、TUIC v5、Hysteria2、MTProto、HTTP、SOCKS 等 ｜ A-3 ｜ Features
- 内置订阅服务器，输出 raw / JSON / Clash，按客户端 User-Agent 自动选择 ｜ A-3 ｜ Features ｜ quote: "auto-selected from the client's User-Agent"
- 按客户端管流量配额、到期时间、IP 限制、HWID 设备数限制、一键分享链接/二维码/订阅 ｜ A-3 ｜ Features
- 存储默认 SQLite（`/etc/x-ui/x-ui.db`），可选 PostgreSQL ｜ A-3 ｜ Database Options
- 安装命令 `bash <(curl -Ls .../install.sh)`，安装时**随机生成用户名、密码与访问路径** ｜ A-3 ｜ Quick Start ｜ quote: "a random username, password, and access path"
- ⚠ 项目自述"仅供个人使用，请勿用于非法用途或生产环境" ｜ A-3 ｜ Important ｜ quote: "intended for personal use only"
- 仓库星标 46.8k / fork 11.8k（2026-09-23 观测） ｜ A-3 ｜ Stars

**安装细则（B-1）**
- 一键安装命令 `bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)` ｜ B-1 ｜ Install in one-line
- 一键安装器生成随机用户名、随机密码、随机 web base path ｜ B-1 ｜ 同上
- 安装后访问 `http://<your-ip>:<your-port>/<your-path>`，运行 `x-ui` 可重开管理菜单 ｜ B-1 ｜ 同上
- Docker Compose 用镜像 `ghcr.io/mhsanaei/3x-ui:latest`，**默认仅发布面板端口 2053** ｜ B-1 ｜ Using Docker Compose ｜ quote: "2053:2053"
- ⚠ **Docker 部署默认凭据为 admin / admin**，登录后须立即在 Panel Settings > Authentication 改密 ｜ B-1 ｜ 同上 ｜ quote: "Password: `admin`"
- ⚠ Compose 的 ports 块**只发布面板端口 2053，入站代理端口不会自动暴露** ｜ B-1 ｜ 同上 ｜ quote: "are **not** exposed automatically"
- 手动安装按 `uname -m` 分架构：amd64/arm64/armv7/armv6/armv5/s390x ｜ B-1 ｜ Manual installation
- 服务文件按 OS 分支：ubuntu/debian/armbian、arch/manjaro/parch、其余走 rhel；**Alpine 用 OpenRC 须改用一键脚本** ｜ B-1 ｜ 同上 ｜ quote: "Alpine Linux uses OpenRC"

### 4.4 机场 vs 自建（本篇唯一的量化对照）

- 机场 = 订阅制翻墙代理的地下市场形态 ｜ A-2 ｜ Abstract ｜ quote: "subscription-based ... proxies"
- 1667 名受访者中**超过一半使用机场**，是受访者中最主流的现成工具 ｜ A-2 ｜ Abstract ｜ quote: "over half of our 1,667~survey respondents"
- 用户选择理由：易用性、性能、可访问 ChatGPT/Netflix 等地区受限服务 ｜ A-2 ｜ Abstract ｜ quote: "ease of use, performance"
- 全网扫描 + Telegram 公告频道抓取，识别出 **3431 个活跃机场** ｜ A-2 ｜ Abstract ｜ quote: "3,431 active airports"
- 这些机场建立在**少数几个开源工具包**之上（摘要未点名） ｜ A-2 ｜ Abstract ｜ quote: "a handful of open-source toolkits"
- 订阅 35 个机场实测：性能**常超过直连**，原因是独特的多跳架构 ｜ A-2 ｜ Abstract ｜ quote: "we subscribe to 35 airports"
- 机场接受支付宝等商业支付渠道，并**频繁遭遇政府下架** ｜ A-2 ｜ Abstract ｜ quote: "payment through commercial services like Alipay"
- 机场会自行实施各自的审查策略，客户端难以配置到最优 ｜ A-2 ｜ Abstract ｜ quote: "their own distinct censorship policies"
- v1 提交 2026-06-16，DOI 10.48550/arXiv.2606.18427 ｜ A-2 ｜ Submission history

> ⚠ 写作纪律：A-2 是**摘要页**，本地无正文。只能引用摘要中出现的数字与结论，**不得延伸推断**多跳架构细节、机场规模分布或协议占比。

### 4.5 VPS 选购

- RackNerd 机房含洛杉矶、圣何塞、西雅图、达拉斯、亚特兰大、芝加哥、纽约、Ashburn、阿姆斯特丹、法国、都柏林、多伦多 ｜ B-2 ｜ opening paragraph
- RackNerd 入门档（2026-09-23 观测）：512MB **$26.99/年**；1GB $17.99/月；2GB $20.59/月 ｜ B-2 ｜ KVM VPS Plans
- RackNerd 全系含 RAID-10 SSD、1Gbps、1 个免费 IPv4、即时开通 ｜ B-2 ｜ 同上
- RackNerd 控制面板可 Start/Stop/Re-Install/Console/Reset ｜ B-2 ｜ Intuitive Control Panel
- RackNerd 洛杉矶与法国机房可申请最多 100 个免费 IPv6 ｜ B-2 ｜ FAQ
- ⚠ **B-2 同表内计费周期不一致**（512MB 标 `/year`，其余档标 `/month`），引用时**必须连周期一起写**
- CloudCone SSD VPS 1（2026-09-23 观测）：$2.33/月、**年付 $28**，2 vCPU / 1GB / 30GB SSD / 4TB 月流量 ｜ B-6 ｜ SSD VPS 1
- CloudCone SSD VPS 2：$3.83/月、年付 $46，4 vCPU / 2GB / 60GB / 7TB ｜ B-6 ｜ SSD VPS 2
- CloudCone 全档共用：RAID-10 SSD、1Gbps、1×IPv4 + 3×IPv6、KVM、CPU 可创建前升级 ｜ B-6 ｜ 同上
- CloudCone 数据中心在美国洛杉矶；DDoS 防护由 Voxility 提供且免费 ｜ B-6 ｜ Data Center / DDoS
- KiwiVM 是搬瓦工官方自研控制面板，支持 start/stop、OS reload、Emergency console、rDNS、机房迁移、快照、用量统计、API ｜ B-3 ｜ About our Self-Managed KVM VPS
- 搬瓦工可选 OS：AlmaLinux、RockyLinux、CentOS、Debian、Ubuntu、CentOS Stream、Fedora ｜ B-3 ｜ 同上
- ⚠ **搬瓦工的价格与套餐不可得**（JS 门控），正文不得编造

### 4.6 SSH 登录

- FinalShell 官网标注版本 **4.6.3**，更新日期 2025.5.21 ｜ B-4 ｜ title ｜ quote: "版本4.6.3"
- 支持 Windows / macOS / Linux ｜ B-4 ｜ 主要特性
- Windows X64 下载：`https://dl.hostbuf.com/finalshell3/finalshell_windows_x64.exe` ｜ B-4 ｜ 正文下载地址
- macOS Arm(m1/m2/m3) 为 `finalshell_macos_arm64.pkg`，X64 为 `finalshell_macos_x64.pkg` ｜ B-4 ｜ 同上
- Linux 为 .deb：x64 / arm64 / LoongArch64 龙芯 ｜ B-4 ｜ 同上
- 更新日志地址 `https://www.hostbuf.com/t/989.html` ｜ B-4 ｜ 同上
- 特色：云端同步、海外服务器远程桌面加速、ssh 加速、本地化命令输入框（补全/历史/自定义参数） ｜ B-4 ｜ 正文特色功能段
- ⚠ **FinalShell 无官方使用手册**，仅下载与更新日志。连接步骤只能引第三方教程并降层标注，或改写为通用 SSH 概念

### 4.7 带域名与 CDN 前置

- Proxied（橙云）让 HTTP/HTTPS 经 Cloudflare；DNS-only（灰云）直接返回源站真实 IP ｜ C-1 ｜ intro ｜ quote: "responds with your server's actual IP address"
- **只有 A、AAAA、CNAME 可被代理**；MX、TXT 等永远 DNS-only ｜ C-1 ｜ intro ｜ quote: "always DNS-only"
- 代理记录 TTL 默认且固定 Auto（300 秒），不可编辑 ｜ C-1 ｜ Predefined TTL ｜ quote: "set to 300 seconds"
- 同一 name 上多条 A/AAAA 且至少一条被代理时，该 name 全部按代理处理 ｜ C-1 ｜ Mix proxied and unproxied
- 代理 CNAME 默认做 flattening，返回 Cloudflare anycast IP ｜ C-1 ｜ CNAME records
- DNS-only **会把源站 IP 暴露给任何查询者**，失去针对性攻击防护 ｜ C-1 ｜ Example ｜ quote: "exposes your origin IP address"
- 源站未在 Proxy Read Timeout 内响应则返回 524 ｜ C-1 ｜ Connection timeouts
- 只有承载 HTTP/HTTPS 的 A/AAAA/CNAME 可代理 ｜ C-2 ｜ Proxy eligibility ｜ quote: "serve HTTP or HTTPS traffic"
- ⚠ 代理**非标准端口的 HTTP/HTTPS**，或代理 TCP/UDP 应用，需用 **Cloudflare Spectrum** ｜ C-2 ｜ Ports and protocols ｜ quote: "Cloudflare Spectrum"
- ⚠ **新域名 pending 状态最长 24 小时，期间所有记录（含设为代理的）实际按 DNS-only 生效并返回源站 IP** ｜ C-2 ｜ Pending domains ｜ quote: "up to 24 hours"
- ⚠ 官方建议：**zone 激活后在主机商处轮换源站 IP**，防止上线期间源站 IP 泄漏 ｜ C-2 ｜ Pending domains ｜ quote: "rolling your origin IP addresses"
- 用 Cloudflare 作 secondary DNS 且 Pre-signed DNSSEC 时，代理记录被当作 DNS-only ｜ C-2 ｜ Pre-signed DNSSEC
- NTLM/Kerberos 等 Windows 集成认证与代理记录不兼容 ｜ C-2 ｜ Windows authentication

### 4.8 节点被封与换 IP

- DigitalOcean **重建（rebuild）保留 IP**；销毁则把 IP 释放回地址池，**几乎不可能拿回同一 IP** ｜ C-5 ｜ 场景 1 ｜ quote: "the IP address is retained"
- 重建会用所选镜像抹掉磁盘并替换，镜像须与原实例同 OS 家族 ｜ C-5 ｜ intro ｜ quote: "wipes the Droplet's disk"
- 重建**不可逆**，无备份/快照则数据无法找回 ｜ C-5 ｜ intro
- 重建后主机密钥改变，本地 `known_hosts` 报 REMOTE HOST IDENTIFICATION HAS CHANGED；修复 `ssh-keygen -f "/root/.ssh/known_hosts" -R <ip>` ｜ C-5 ｜ Control Panel 流程
- Vultr：**快照不保留 IP**，恢复快照会分配新 IP，除非 attach a Reserved IP ｜ C-8 ｜ 首段 ｜ quote: "snapshots do not retain the IP address"
- Vultr Reserved IP 可在同一 region 的实例间重新分配，适合 rebuild/migration 时保持 IP 连续性 ｜ C-8 ｜ 首段
- Vultr 部署时网络由 cloud-init 自动配置；**部署后**新增/移除 VPC、新增或更改公网 IP 须手工配置 ｜ C-7 ｜ Configure Linux Servers
- Vultr：设了静态 IP 后从快照恢复会**无法联网**，须经 web console 改回 DHCP ｜ C-7 ｜ Restoring a Backup
- Vultr 推荐 DNS resolver：IPv4 `108.61.10.10`、IPv6 `2001:19f0:300:1704::6` ｜ C-7 ｜ Configure IPv4/IPv6
- ⚠ **无任何官方文档说明"如何判定本机 IP 已被封"** → 正文只能给经验性判断路径，且必须标注为经验而非官方标准（见 §6）

### 4.9 安全加固

- SSH `Port` 默认 22，可多次出现 ｜ C-4 ｜ KEYWORDS Port ｜ quote: "The default is 22"
- `PasswordAuthentication` 默认 **yes** ｜ C-4 ｜ KEYWORDS ｜ quote: "The default is `yes`"
- `PermitRootLogin` 取值必须是 yes / prohibit-password / forced-commands-only / no，默认 **prohibit-password** ｜ C-4 ｜ KEYWORDS ｜ quote: "prohibit-password"
- `prohibit-password` 时对 root 关闭密码与 keyboard-interactive 认证（`without-password` 为废弃别名） ｜ C-4 ｜ KEYWORDS
- `PermitEmptyPasswords` 默认 no ｜ C-4 ｜ KEYWORDS ｜ quote: "The default is `no`"
- `MaxAuthTries` 默认 6，达到一半即开始记录额外失败 ｜ C-4 ｜ KEYWORDS
- `LoginGraceTime` 默认 120 秒，0 表示无限制 ｜ C-4 ｜ KEYWORDS
- ⚠ 以上 C-4 条目的**参数归属为推断**（见 §3.4），引用默认数值前须回源人工确认
- fail2ban：优先在 `*.local` 覆盖 `*.conf`，`.local` 中只写要改的项 ｜ C-3 ｜ CONFIGURATION FILES FORMAT
- fail2ban 解析顺序 `jail.conf` → `jail.d/*.conf` → `jail.local` → `jail.d/*.local`，后者覆盖前者 ｜ C-3 ｜ 同上 ｜ quote: "take precedence"
- `bantime` = 封禁时长；`findtime` = 统计失败次数的时间窗口；`maxretry` = 最近 findtime 秒内需达到的失败阈值 ｜ C-3 ｜ jail.conf [DEFAULT]
- `findtime`/`bantime` 可写整数秒或缩写格式（600 等价 10m），可用 `fail2ban-client --str2sec` 验证 ｜ C-3 ｜ TIME ABBREVIATION FORMAT
- `ignoreself` 默认 true；`ignoreip` 列出永不封禁的 IP/CIDR ｜ C-3 ｜ jail.conf [DEFAULT]
- `actionban` 在达到 maxretry 且落在最近 findtime 内时封禁，`actionunban` 在 bantime 后解封 ｜ C-3 ｜ ACTION CONFIGURATION FILES
- ⚠ C-3 **未给出各参数的发行版默认数值**（bantime/findtime/maxretry 的具体秒数需另找默认配置文件）
- 面板侧最小加固（改默认口令、自定义面板路径、2FA）在 A-3 / B-1 中属产品配置说明，**无独立官方安全文档**

---

## 5. 矛盾与冲突

| # | 冲突 | 处置 |
|---|---|---|
| 1 | **换 IP 结论按厂商分化**：C-5（DigitalOcean 重建**保留** IP）vs C-8（Vultr 快照恢复**分配新** IP，需 Reserved IP 才能保持） | **不是矛盾，是两家厂商语义不同**（重建 ≠ 快照恢复）。正文必须分厂商分操作写，禁止合并成"重建会换 IP"这类通论。C-7 通篇未涉及换 IP，不可用于此结论 |
| 2 | A-3-c8（"仅供个人使用、勿用于生产"）vs A-3 功能清单（多节点、多用户、配额、订阅服务） | 真实张力，正文可如实并列：项目自述定位与功能面向不一致 |
| 3 | A-2 称机场建于"少数几个开源工具包"，摘要未点名；A-3 是面板而非"工具包" | **不可建立 A-2 ↔ A-3 的对应关系**。正文不得写成"机场普遍用 3x-ui 搭建" |
| 4 | B-1-c2（一键安装随机凭据）vs B-1-c5（Docker 默认 admin/admin） | 非矛盾但**极易误用**。正文必须分别写明：一键脚本 = 随机凭据；Docker = admin/admin **且必须立即改** |
| 5 | C-1（A/AAAA/CNAME 可代理）vs C-2（只有承载 HTTP/HTTPS 的这三类才可代理） | C-2 更严格，非冲突，表述时用 C-2 口径 |

---

## 6. 覆盖缺口与开放问题（写作时必须降级表述）

| 缺口 | 正文处置 |
|---|---|
| 「代理节点」「订阅链接」**无官方定义来源** | 标为"行业通用说法"，不得写成官方口径 |
| 「如何判定 IP 被封」**无官方文档** | 只能写经验性判断路径，显式标注"非官方标准" |
| 面板层**无独立官方安全文档** | 加固建议只能引产品配置页 + 通用 SSH/fail2ban 官方文档 |
| FinalShell **无官方使用手册** | 连接步骤改写为通用 SSH 概念，或引第三方并标注层级 |
| 3x-ui **无官方中文零基础教程** | 中文表述由本项目撰写，不假托官方 |
| C-3 **未给 fail2ban 默认数值** | 不写具体默认秒数，只写参数语义 |
| B-5 作者配套文档**不可得** | 不得引用其内容 |
| 搬瓦工**套餐价格不可得** | 不写搬瓦工价格 |
| A-2 仅有摘要 | 只引摘要数字，不延伸 |

---

## 7. 下游交接

### 给 `outline-generator`（P3）

- 建议结构：**概念铺垫（VPS / 协议 / 面板 / 机场 vs 自建）→ 落地主线（选购 → 登录 → 装面板 → 建节点 → 带域名 → 使用 → 被墙处置）→ 安全事项**
- 素材分配：概念用 §4.1/4.2/4.3/4.4；落地用 §4.5~4.8；安全用 §4.9
- **与既有笔记 `自建代理节点/自建代理节点搭建实战.md` 的去重边界**（用户已确认 A 方案）：
  内核直配（手写 Xray JSON、REALITY 原理、nftables/suricata 深度加固）**只做指引与链接，不重复展开**

### 给 `chapter-writer`（P4）

派发提示中**不要转述本文件的措辞**。只传：章节范围 + 本文件 §4 对应的 claim ID 与 anchor + `sources/` 路径。
写作时逐条回 `sources/{ID}.md` 核对；凡写"官方说明 / 官方口径 / 原文"处，必须能在对应文件中找到原句。
凡本节 §6 列出的缺口，按表中"正文处置"列降级表述。
