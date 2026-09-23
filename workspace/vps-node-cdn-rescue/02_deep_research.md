# 02 深度收集结果 - VPS 被墙节点 CDN 拯救实战（Cloudflare CDN 回源）

- **运行标识**: vps-node-cdn-rescue
- **阶段**: P2（深度收集）
- **抓取日期**: 2026-09-24
- **素材总量**: **23 篇**（P1 计划的 21 篇 + P2 缺口补抓 2 篇）
- **层级配比**: `official` 17 篇 / `primary-research` 4 篇 / `community` **0 篇**
- **派发记录**: 3 个深度阅读子代理（概念组 6 篇 / Cloudflare 配置组 8 篇 / 实操排错组 7 篇），符合「≤3 delegates 且禁止一源一代理」
- **正文缓存位置**: `sources/{ID}.md`（下游阶段只传路径与锚点，不粘贴正文）

## 取材基调（用户 P0 / P1 确认）

1. **概念 + 实战混合**，非纯实操手册。
2. **域名前置（免费域名获取 / 托管解析）只做指路**，链到同系列两期视频，不展开。
3. **纳入 Cloudflare 免费版端口表与限制清单**（用户点名）。
4. **不复述「安装面板 / 搭建节点」** —— 那两段是上一期视频的重演，正文只做指路并链回面板流笔记。
5. **纳入两篇 USENIX 一手论文**，在「CDN 为什么能救被墙」一节各用一两句给结论并标注引用，其余不展开。

---

## 一、来源表

> tier 口径：`official` = 厂商官方文档/官方 wiki；`primary-research` = 同行评议论文或测量机构一手材料。
> 全部条目均经父流程 curl 复核；`sources/` 下为实际落盘文件。

| ID | 标题 | URL | Tier | 抓取 | 落盘大小 |
|---|---|---|---|---|---|
| A-1 | What is a CDN? — Cloudflare Learning Center | https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ | official | ✅ | 10.7 KB |
| A-2 | CDN Reference Architecture — Cloudflare Docs | https://developers.cloudflare.com/reference-architecture/architectures/cdn/ | official | ✅ | 31.1 KB |
| A-3 | How CloudFront delivers content — AWS | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html | official | ✅ | 11.4 KB |
| A-4 | CDN — MDN Web Docs Glossary | https://developer.mozilla.org/en-US/docs/Glossary/CDN | official | ✅ | 3.9 KB |
| A-5 | Domain Shadowing（USENIX Security 2021）摘要页 | https://www.usenix.org/conference/usenixsecurity21/presentation/wei | primary-research | ✅（仅摘要） | 2.4 KB |
| A-6 | How the GFW Detects and Blocks Fully Encrypted Traffic（USENIX Security 2023） | https://gfw.report/publications/usenixsecurity23/en/ | primary-research | ✅ | 104.3 KB |
| B-1 | Proxy status · Cloudflare DNS docs | https://developers.cloudflare.com/dns/proxy-status/ | official | ✅ | 9.9 KB |
| B-2 | Proxying limitations · Cloudflare DNS docs | https://developers.cloudflare.com/dns/proxy-status/limitations/ | official | ✅ | 5.0 KB |
| B-3 | Network ports · Cloudflare Fundamentals docs | https://developers.cloudflare.com/fundamentals/reference/network-ports/ | official | ✅ | 4.2 KB |
| B-4 | Encryption modes · Cloudflare SSL/TLS docs | https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/ | official | ✅ | 9.1 KB |
| B-5 | DNS setups · Cloudflare DNS docs | https://developers.cloudflare.com/dns/zone-setups/ | official | ✅ | 4.6 KB |
| B-6 | Primary setup (Full) · Cloudflare DNS docs | https://developers.cloudflare.com/dns/zone-setups/full-setup/ | official | ✅（偏短） | 1.6 KB |
| B-7 | CNAME setup (Partial) · Cloudflare DNS docs | https://developers.cloudflare.com/dns/zone-setups/partial-setup/ | official | ✅ | 4.1 KB |
| B-8 | Full (strict) · Cloudflare SSL/TLS docs | https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/ | official | ✅ | 3.3 KB |
| B-9 | Cloudflare Free 套餐页（营销页，**未抓取**） | https://www.cloudflare.com/plans/free/ | official（营销） | ⏭️ 跳过 | — |
| C-1 | WebSocket（Xray 传输配置官方文档） | https://xtls.github.io/config/transports/websocket.html | official | ✅ | 3.7 KB |
| C-2 | Configuration（3x-ui 官方 wiki） | https://github.com/MHSanaei/3x-ui/wiki/Configuration | official | ✅ | 15.1 KB |
| C-3 | Error 525 · Cloudflare 官方排错 | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-525/ | official | ✅ | 3.2 KB |
| C-4 | Error 413 · Cloudflare 官方排错 | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-413/ | official | ✅ | 2.6 KB |
| C-5 | Glossary（OONI 阻断类型定义） | https://ooni.org/support/glossary/ | primary-research | ✅ | 40.9 KB |
| C-6 | Error 526 · Cloudflare 官方排错 | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-526/ | official | ✅ | 6.3 KB |
| C-7 | Fallback 回落（Xray 官方文档） | https://xtls.github.io/config/features/fallback.html | official | ✅ | 5.9 KB |
| **D-1** | **WebSockets · Cloudflare Network settings docs**（P2 缺口补抓） | https://developers.cloudflare.com/network/websockets/ | official | ✅ | 5.4 KB |
| **D-2** | **Domain Shadowing 全文 PDF**（P2 缺口补抓） | https://www.usenix.org/system/files/sec21-wei.pdf | primary-research | ✅（pdftotext） | 82.5 KB |

**B-9 跳过说明**：营销页，`official` 层级最低且无单页权威额度表；Free 限额结论改由 D-1 的「全套餐支持」与各产品文档的 plan availability 段落支撑，避免引用营销口径。

---

## 二、Claim / Source 映射（按预期章节组织）

### 2.1 CDN 是什么

| 结论 | 来源 | 锚点 |
|---|---|---|
| CDN 是地理分布的一组服务器，把内容缓存在更靠近终端用户的位置来加速分发 | A-1 | 首段 / `## What is a CDN?` |
| **CDN 不托管内容、不能替代虚拟主机**；它只在网络边缘缓存内容 | A-1 | `## Is a CDN the same as a web host?`（含原文引句） |
| CDN 把服务器放在不同网络之间的交换点（IXP），以降低时延与传输成本 | A-1 | `## How does a CDN work?` |
| 降延迟的四类机制：缩短物理距离、负载均衡与 SSD 等软硬件优化、压缩与 minify、TLS 连接复用与 TLS false start | A-1 | `## Latency` |
| Anycast 路由在某数据中心整体故障时把流量转到其他可用节点 | A-1 / A-2 | A-1 `## Reliability and redundancy`；A-2 `### Routing requests to CDN nodes — Anycast routing` |
| 请求到 CDN 节点有两条路径：**DNS unicast 路由**与 **anycast 路由** | A-2 | `### Routing requests to CDN nodes` |
| DNS unicast 按**客户端 DNS 解析器**（而非客户端 IP）判断就近节点，且受 DNS TTL 约束，故障切换不优雅 | A-2 | 同上 → `DNS unicast routing` |
| Anycast 让多节点宣告同一 IP，客户端重定向交给 BGP，流量送到最近且有容量的数据中心 | A-2 | 同上 → `Anycast routing` |
| 有 CDN 时，源站只在**未命中或内容不可缓存（动态内容）**时被联系 | A-2 | `### Impacts` |
| CDN 以**反向代理**身份位于源站之前，因此能提供 DDoS 缓解等安全能力 | A-2 | `### Impacts — Improved website security` / `## Cloudflare CDN architecture and design` |
| 缓存是在临时位置存放文件副本，使用户无需每次回源 | A-1 | `## FAQs — How does caching work within a CDN?` |
| 每次源站响应都消耗一次带宽；CDN 用缓存承接大部分请求，从而降低回源与主机成本 | A-1 | `## Bandwidth expense` |
| 无缓存命中时请求被转发到源站；回源响应在收到第一个字节时即开始向用户转发，同时写入缓存 | A-3 | `## How CloudFront delivers content to your users` 步骤 2–3.3 |
| 回源链路可分层：POP 未命中 → regional edge cache → 源站；回源后对象同时写入两层，同区域 POP 共享缓存 | A-3 | `###### How regional caches work` |
| 代理类 HTTP 方法（PUT/POST/PATCH/OPTIONS/DELETE）与运行时判定为动态的请求**不经** regional edge cache，直接回源 | A-3 | `###### Note`（第二、三条） |
| 使用第三方 CDN 的代价：对第三方的额外依赖、额外攻击面、可能反而降低性能（跨源不共享缓存） | A-4 | `There are also downsides to using CDNs` |
| CDN 在某地区被封锁或被永久关停，站点就会故障 | A-4 | `There are also downsides to using CDNs`（第一条） |
| Cloudflare 以 SaaS 模式提供 CDN，客户无需管理基础设施或软件 | A-2 | `## Introducing the Cloudflare CDN` |

> **厂商自述数据（引用须标明"Cloudflare 自称"）**：全球 anycast 网络覆盖数百城市、50 ms 内触达 95% 互联网人口、网络容量 >405 Tbps（A-2 `## Cloudflare CDN architecture and design`）；Argo Smart Routing 平均带来 30% web 资源性能提升（A-2 `### Argo Smart Routing`）。文件内**无第三方核验**。

### 2.2 CDN 为什么能救被墙节点（原理与边界）

| 结论 | 来源 | 锚点 |
|---|---|---|
| 代理记录的 DNS 查询返回 **Cloudflare anycast IP，而非源站真实 IP** | B-1 | `Proxied records` |
| 灰云（DNS-only）记录**返回源站真实 IP**，暴露源站地址 | B-1 | `Proxied records` / `DNS-only records` |
| Cloudflare 是反向代理：所有请求先穿越 Cloudflare 网络才到达源站 | A-2 | `## Cloudflare CDN architecture and design` |
| Domain fronting 的抗封锁来自「附带损害」：要禁掉它，审查方必须封掉用户访问**整个 CDN**，导致该 CDN 上所有域名不可达 | D-2 | §2.3 The Rise and Fall of Domain Fronting（含原文引句） |
| 若只封被禁域名，**任一允许的域名都能当日落域名**，使同 CDN 上其他所有域名可用 | D-2 | §6.1.3（含原文引句） |
| Domain shadowing 更难封：要封掉一个域名，审查方必须封掉**所有允许 domain shadowing 的 CDN**，附带损害远大于 domain fronting | D-2 | §6.1.3 Blocking a CDN |
| Domain shadowing 使连接 URL、TLS SNI、HTTP(S) Host 头**全部看起来属于被允许的那个域名** | A-5 | Abstract |
| 即使审查方封掉某一个 CDN，也**不能禁用 domain shadowing**，因为用户可以换到其他仍允许该手法的 CDN | D-2 | §6.1.3（末段） |
| GFW 自 2021-11 起对"全加密流量"实施**纯被动实时检测与封锁**（观察窗口至 2023-02） | A-6 | Abstract；§1 |
| GFW 不正面定义"全加密流量"，而是用**五条粗粒度豁免规则**放过"不像全加密"的流量，其余一律封锁 | A-6 | §4 / Algorithm 1 |
| 豁免规则逐条：① popcount 比率 ≤3.4 或 ≥4.6；② 前 6 字节（或更多）落在 `[0x20,0x7e]`；③ >50% 字节落在 `[0x20,0x7e]`；④ >20 个连续字节落在 `[0x20,0x7e]`；⑤ 匹配 TLS 或 HTTP 协议指纹 | A-6 | §4 Algorithm 1（推断所得） |
| TLS 豁免依赖首 3 字节匹配 `[\x16-\x17]\x03[\x00-\x09]`；HTTP 豁免依赖方法名 + 空格（大小写不敏感，拼错则不豁免） | A-6 | §4.3 |
| 中文（UTF-8 与 GBK）字符**不享受任何豁免** | A-6 | §4.2 |
| 触发后**仅"客户端→服务器"方向的包被丢弃**，服务器发往客户端的包不受影响 | A-6 | §4.4 |
| 该机制**仅作用于 TCP**；UDP 不触发。作者判断为"临时性"，审查方随时可扩展 | A-6 | §4.4 |
| 封锁可发生在 **1–65535 全部端口**，换非标准端口**不能**规避 | A-6 | §4.4 |
| 触发后同一 3 元组被**残余封锁 120 或 180 秒**，且计时器不因后续发包重置 | A-6 | §4.4 |
| 必须完成完整 TCP 握手才可能触发；只检查"客户端→服务器"首个数据包，**不做多包流重组** | A-6 | §4.5 |
| 封锁是**概率性**的，单连接封锁概率约 **26.3%** | A-6 | §6.3 |
| 受影响的 AS **都是向个人出售 VPS 的供应商**（Alibaba US、Constant、Amazon/DO/Linode 部分前缀）；**Akamai、Cloudflare 这类大型 CDN AS 不在受影响之列** | A-6 | §6.2 Figure 4 说明段 |
| 客户端侧规避手法（可定制 IV 前缀、改写 popcount、走 UDP/QUIC、Base64、20+ 连续可打印字符）截至 2023-02 在中国仍有效 | A-6 | §8.1、§8.2、§A |

> ⚠ **A-6 的引用纪律（必须遵守）**：§6.2 那条"CDN AS 不在受影响之列"的语境**严格限于"全加密流量被动检测"这一单一机制**。它**不能**推出「CDN 对其它封锁手段免疫」，也**不能**推出「CDN 是当局的有意豁免」。所有数字（26.3%、98%、0.6%）均来自 2022-05 的 10% IPv4 扫描、仅 port 80，且 0.6% 是**模拟值而非真实误伤率**。任何 2026 年现状陈述都不能由本文支撑，写作时须带时间限定。

### 2.3 获取与接入 Cloudflare

| 结论 | 来源 | 锚点 |
|---|---|---|
| 代理状态决定该记录的 HTTP/HTTPS 流量走 Cloudflare 还是直连源站；Proxied = 橙云，DNS-only = 灰云 | B-1 | `Benefits` |
| **只有用于 IP 地址解析的 A、AAAA、CNAME 可被代理**；MX、TXT 等永远是 DNS-only | B-1 | `Proxied records`（含原文引句） |
| **收窄口径**：只有承载 HTTP 或 HTTPS 流量的 A/AAAA/CNAME 可被代理 | B-2 | `Proxy eligibility` |
| 同名下多条 A/AAAA 中只要有一条被代理，该名下所有 A/AAAA 都按代理处理 | B-1 | `Mix proxied and unproxied` |
| CNAME 链上任一主机名被代理，整条请求都按代理处理；被代理的 CNAME 默认做 CNAME flattening | B-1 | `CNAME records` |
| 代理记录 **TTL 固定为 Auto（300 秒）**，不可编辑 | B-1 | `Predefined time to live` |
| **DNS setup 四种**：Primary (Full)、CNAME (Partial)、Zone transfers、Subdomain setup | B-5 | `DNS setups` |
| **Free / Pro 套餐下，primary setup (full) 是唯一可用的方案** | B-5 / B-6 | B-5 `Common use cases and availability`（含原文引句）；B-6 `Availability` 表 |
| CNAME setup (Partial) 需要 **Business 或 Enterprise**；zone transfers 与 subdomain setup 仅 Enterprise | B-5 | `Common use cases and availability` |
| Partial 方案下被代理主机名必须 CNAME 指向 `{your-hostname}.cdn.cloudflare.net` | B-7 | `How to` |
| 因 CNAME 不允许置于 apex（RFC 1912），partial 方案要代理 apex 需权威 DNS 支持 CNAME Flattening；否则改用重定向到已代理子域或 static IP / BYOIP | B-7 | `CNAME flattening`（含原文引句） |
| 针对 DNS 基础设施的 DDoS 防护**只在 primary setup (full)** 上提供 | B-7 | `DDoS protection` |
| **新添加域名在验证所有权前处于 pending，最长可能需 24 小时** | B-2 | `Pending domains` |
| **pending 期间所有记录（即使已设为代理）实际都是 DNS-only，请求会返回源站 IP** | B-2 | `Pending domains`（含原文引句） |
| 官方建议 **zone 激活后轮换源站 IP**，避免接入期间源站 IP 泄露 | B-2 | `Pending domains` |
| zone 可能状态：Initializing、Pending、Active、Moved、Deleted、Purged | B-5 | `Zone status` |
| B-6 只给 primary setup 的定义与可用性表，**不含 NS 接入操作细则**（指向未抓取的 `Set up a primary zone` 子页） | B-6 | 正文首段 / `Availability` |

### 2.4 端口与协议限制（用户点名要的完整清单）

| 结论 | 来源 | 锚点 |
|---|---|---|
| 默认情况下 Cloudflare 只代理**下列 13 个** HTTP/HTTPS 端口 | B-3 | `Network ports compatible with Cloudflare's proxy` |

**完整端口清单（逐项，B-3）**

| 端口 | 归类 | 是否在「缓存禁用」清单 | 备注 |
|---|---|---|---|
| 80 | HTTP ports supported by Cloudflare | 否 | 中国数据中心 + China Network 域名**仅** 80/443 可用 |
| 8080 | HTTP ports supported by Cloudflare | 否 | — |
| 8880 | HTTP ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2052 | HTTP ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2082 | HTTP ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2086 | HTTP ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2095 | HTTP ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 443 | HTTPS ports supported by Cloudflare | 否 | 中国数据中心 + China Network 域名**仅** 80/443 可用 |
| 2053 | HTTPS ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2083 | HTTPS ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2087 | HTTPS ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 2096 | HTTPS ports supported by Cloudflare | **是** | 可代理但不缓存 |
| 8443 | HTTPS ports supported by Cloudflare | **是** | 可代理但不缓存 |

| 结论 | 来源 | 锚点 |
|---|---|---|
| 缓存禁用清单共 **10 个**端口：2052、2053、2082、2083、2086、2087、2095、2096、8880、8443 | B-3 | 同页清单 |
| ⚠ 文档**只列「禁用缓存」清单**，**未明文写 80/443 已启用缓存** → 「仅 80/443 走缓存」属**排除推论**，引用时须标注 | B-3 | 同上 |
| 为额外端口开代理只有两条路：① 把子域改为**灰云直连源站**；② 为该主机名配置 **Spectrum** 应用 | B-3 | `How to enable Cloudflare's proxy for additional ports` |
| Spectrum 支持所有端口，但**全端口 Spectrum 仅 Enterprise 可用** | B-3 | 同锚点（含原文引句） |
| 付费套餐可用 WAF 规则封堵非 80/443 端口流量：旧版托管规则 ID `100015`；新版属 Cloudflare Managed Ruleset（规则 ID `...664ed6fe`，**默认禁用**） | B-3 | `How to block traffic on additional ports` |
| 仅 80 和 443 兼容「中国数据中心内、启用 China Network 的域名」的 HTTP/HTTPS 流量 | B-3 | 清单备注 |
| 因 anycast 特性，非 80/443 端口对其他客户开放；Netcat 与扫描器在特定条件下会报这些非标准端口为"开放"——**这是 anycast 共享的副作用，不是你的服务暴露** | B-3 | `Related resources` |
| 要在非标准端口代理 HTTP/HTTPS，或代理 TCP/UDP 应用，需使用 Cloudflare Spectrum | B-2 | `Ports and protocols` |
| 代理请求有按套餐分级的请求/响应体积上限，代理状态下无法绕过；默认 Proxy Read Timeout 超时返回 **524**，仅 Enterprise 可调高 | B-1 | `Request and response size limits` / `Connection timeouts` |
| 不可代理目标黑名单（精确匹配）：`dkim2.mcsv.net`、`dkim3.mcsv.net`、`zmverify.zoho.com`、`dkim.infusionmail.com`；`dkim.amazonses.com`（含子域）；子域级：`onmicrosoft.com`、`dkim.intercom.io`、`acm-validations.aws` | B-2 | `Non-proxiable targets` |
| Microsoft IWA / NTLM / Kerberos 因违反 HTTP/1.1 规范**不兼容代理记录**；NTLM 在 TCP 层认证，Cloudflare 不保证连续请求复用同一 TCP 连接 → 可能反复弹窗或认证循环 | B-2 | `Windows authentication` |
| 二级 DNS + Pre-signed DNSSEC 场景下，Cloudflare 会把记录当作 DNS-only 处理 | B-2 | `Pre-signed DNSSEC` |
| **Cloudflare 支持代理 WebSocket 连接，无需额外配置** | D-1 | 首句 |
| WebSocket 开关在 Dashboard 的 **Network** 页；API 用 `PATCH`，setting 名 `websockets`，value `"on"` | D-1 | `Enable WebSockets` |
| **WebSocket 在所有 Cloudflare 套餐均支持** | D-1 | `Availability` |
| **Argo 与 WebSocket 不兼容** | D-1 | `Compatibility notes`（表格 Notes 列） |
| 已建立的 WS 连接**不再被 WAF 检查**；但初始 HTTP 101 请求与其他请求一样受 WAF 托管规则/自定义规则/速率限制约束 | D-1 | `Compatibility notes` |
| WS 连接在**两个方向都无数据传输**时会被 Cloudflare 关闭；企业可联系客户团队改空闲超时；官方建议实现**客户端心跳（ping/pong）** | D-1 | `Idle timeout` |
| Cloudflare 向全球网络发布新代码时**可能重启服务器，从而终止 WS 连接** | D-1 | `Technical note` |
| Cloudflare 只把 WS 的**初始升级请求**计为一个 HTTP 请求；带宽按 **Cloudflare → 客户端**方向计量 | D-1 | `Requests and Bandwidth measurement` |
| WS 排错可用 `wscat` 在单 URL 上复现；`EdgeStartTimestamp` / `EdgeStopTimestamp` 表示 WS 连接时长（非初始 HTTP 连接） | D-1 | `Troubleshooting` |

> ⚠ **D-1 的表格残缺**：`Compatibility notes` 表的**产品名列在抓取结果中丢失**，只有 Notes 列存活。因此「Argo 不兼容」与「WAF 规则适用」两条的归属产品无法从本文件确认，引用时须回源核对或改写为不依赖产品名的表述。

### 2.5 套上 CDN：TLS 模式与回源证书

| 结论 | 来源 | 锚点 |
|---|---|---|
| 加密模式同时控制两段连接：**访客↔Cloudflare** 与 **Cloudflare↔源站** | B-4 | `Available encryption modes` |
| Cloudflare **强烈建议**使用 Full 或 Full (strict)，以防到源站的恶意连接 | B-4 | 同锚点 |
| 模式分两大类：**Automatic SSL/TLS（默认）**与 **Custom SSL/TLS（手动）** | B-4 | 同锚点 |
| 存在**自动升级**机制：从 1% 流量起爬坡，无问题按 10% 递增至 100%；源站连通性失败则中止并回滚 | B-4 | `Automatic SSL/TLS (default)` → `Additional details` |
| 退出自动模式：单 zone 用 `PATCH /zones/$ZONE_ID/settings/ssl_automatic_mode`，body `{"value":"custom"}` | B-4 | `Opt out single zone` |
| API 改模式用 `PATCH`，setting 名 `ssl`，value ∈ `off` / `flexible` / `full` / `strict` / `origin_pull` | B-4 | `Update your encryption mode` |

**Custom SSL/TLS 五种模式对照（逐项完整，B-4）**

| 模式 | 访客↔Cloudflare | Cloudflare↔源站 | 源站证书要求 | 文档说明的适用场景 |
|---|---|---|---|---|
| Off (no encryption) | 不加密 | 不加密 | 无 | 全程明文 HTTP |
| Flexible | 可经 HTTPS 加密 | **不加密** | 无 | 源站不支持 TLS 时常用；官方仍建议尽量升级源站 |
| Full | 跟随访客协议 | 访客 HTTP 则 HTTP；访客 HTTPS 则 HTTPS，**但不校验**源站证书 | 不校验 | 源站用自签名或无效证书时常用 |
| Full (strict) | 加密 | 加密**且校验**源站证书 | 由公共 CA（如 Let's Encrypt）或 Cloudflare Origin CA 签发 | 同 Full 但增加校验 |
| Strict (SSL-Only Origin Pull) | 任意 | **始终 HTTPS 且校验证书**，与访客协议无关 | 需可校验 | Enterprise 方向 |

| 结论 | 来源 | 锚点 |
|---|---|---|
| Full (strict) 做 Full 模式的一切，并对源站证书施加更严格要求；官方称应尽量选它，**除非你是 Enterprise 客户**（此时对应 SSL-Only Origin Pull） | B-8 | 正文首段 / `Use when` |
| 源站证书必须**未过期**：`notBeforeDate < now() < notAfterDate` | B-8 | `Prerequisites`（含原文引句） |
| 源站证书必须由**公共受信任 CA 或 Cloudflare Origin CA** 签发 | B-8 | `Prerequisites` |
| 源站证书的 **CN 或 SAN 必须匹配被请求/目标主机名** | B-8 | `Prerequisites` |
| 启用前要求源站在 **443** 接受 HTTPS 并出示合规证书，否则访客可能遇到 **526** | B-8 | `Process` |
| 视源站配置，可能还需调整设置以避免 Mixed Content 错误或重定向循环 | B-8 | `Limitations` |
| 3x-ui **内置 Cloudflare SSL 证书申请使用 DNS 验证**，因此对通配符证书和**置于 Cloudflare 代理后的服务器**同样可用 | C-2 | `Getting SSL → Cloudflare`（含原文引句） |
| 该功能需要 Cloudflare API Token（作用域 `Zone:DNS:Edit`）或注册邮箱 + Global API Key；**域名必须由 Cloudflare 管理（NS 指向 Cloudflare）** | C-2 | 同上需求列表 |
| 操作路径：执行 `x-ui` → 选 `Cloudflare SSL Certificate` → 先问用 Token（`t`，默认）还是 Global Key（`g`）→ 再输入域名 | C-2 | 同锚点 |
| 创建受限 Token 的官方路径：API Tokens 页 → Create Token → `Edit zone DNS` 模板 → 限定到本 zone | C-2 | `How to create a scoped API Token` |
| 面板设置里的 URL 必须以 `/` 结尾 | C-2 | `Reverse Proxy → Nginx → Note` |
| 订阅默认端口 `2096`；`/sub` 的 location 需增设 `X-Forwarded-Host` 与 `X-Forwarded-Port`，且 `/sub` 面板设置里的 "URI Path" 必须与其一致 | C-2 | `Reverse Proxy → Nginx → For the subscriptions` |
| Nginx 反代面板需 `proxy_http_version 1.1` 与 `Upgrade`/`Connection "upgrade"` 头，并透传 `X-Forwarded-For`、`X-Forwarded-Proto`、`Host`、`X-Real-IP`、`Range`、`If-Range` | C-2 | `Reverse Proxy → Nginx` |
| 官方 Caddy 配置**仅在 inbound 传输设为 "WebSocket" 时可用**，且要求强制 TLS 1.3（`protocols tls1.3`） | C-2 | `Reverse Proxy → Caddy`（含原文引句） |
| Caddy 的 `/api/v1*` 路由用 `Connection *Upgrade*` + `Upgrade websocket` 头匹配，命中反代到 inbound 端口，未命中返回 403 | C-2 | 同锚点 |
| 环境变量 `XUI_SKIP_HSTS` 默认 `false`；置真可跳过发送 `Strict-Transport-Security` 头，用于在反代处终止 TLS 的场景 | C-2 | `Available environment variables` |
| 面板内置 Swagger UI，OpenAPI 3 规范位于 `<面板地址>/panel/api/openapi.json` | C-2 | `API Documentation` |

### 2.6 Xray 侧的传输与回落

| 结论 | 来源 | 锚点 |
|---|---|---|
| ⚠ **官方把 WebSocket 定性为特征明显、建议迁移的传输**：页首 DANGER 块推荐换用 XHTTP，以避免「ALPN 是 http/1.1」等显著流量特征 | C-1 | 页首 DANGER 块（含原文引句） |
| 客户端 `path` 含 `ed` 参数（如 `/mypath?ed=2560`）即启用 **Early Data** | C-1 | `path`: string |
| Early Data 在升级握手同时用 `Sec-WebSocket-Protocol` 头承载首包数据，**该头值即首包长度阈值** | C-1 | 同锚点 |
| `ed` 推荐值 **2560**，最大 **8192**；首包长度超过阈值则不启用；过大可能引发兼容问题，遇问题可调低 | C-1 | 同锚点 |
| `path` 默认 `"/"`；`host` 默认空（服务端为空时不校验客户端 host，指定后校验一致性） | C-1 | `path` / `host` |
| 客户端发送 host 的优先级为 `host` > `headers` > `address` | C-1 | `host`: string |
| `headers` **仅客户端可用**，为自定义 HTTP 头键值对 | C-1 | `headers` |
| `acceptProxyProtocol` **仅用于 inbound**；为 true 时请求方须先发 PROXY protocol v1/v2，否则连接被关闭 | C-1 | `acceptProxyProtocol` |
| `heartbeatPeriod` 指定间隔发送 Ping 保活；不指定或为 0 时不发送（**当前默认行为**） | C-1 | `heartbeatPeriod` |
| WebSocket 会识别 `X-Forwarded-For` 头覆写流量源地址，**优先级高于 PROXY protocol** | C-1 | 页首 TIP 块 |
| WebSocket 连接可被其它 HTTP 服务器（如 Nginx）分流，也可被 VLESS fallbacks path 分流 | C-1 | 页首正文 |
| Fallback 用于**防主动探测**，并可让常用端口多服务共享，核心是「首包回落机制」 | C-7 | 页首引言 |
| fallbacks **仅在使用 VLESS 或 trojan 协议时可用**，且**只能用于 TCP+TLS 传输组合** | C-7 | 页首引言 / `FallbackObject` |
| 该项有子元素时，Inbound TLS 需设置 `"alpn":["http/1.1"]` | C-7 | `FallbackObject` |
| VLESS 会把「TLS 解密后首包长度 < 18」或「协议版本无效」或「身份认证失败」的流量转发到 `dest` 指定地址 | C-7 | `FallbackObject` |
| 非 TCP+TLS 的传输组合**必须删掉 `fallbacks` 项**；此时 VLESS 会等读够所需长度，协议版本无效或认证失败时直接断开 | C-7 | 同锚点 |
| `name` 匹配 TLS SNI（空为任意，默认 `""`）；`alpn` 匹配协商结果（空为任意，匹配成功日志输出 `realAlpn =`） | C-7 | `name` / `alpn` |
| fallbacks 的 alpn 含 `"h2"` 时，Inbound TLS 需设置 `"alpn":["h2","http/1.1"]` | C-7 | `alpn` |
| **Fallback 内的 `alpn` 匹配的是实际协商出的 ALPN，而 Inbound TLS 的 `alpn` 是握手可选列表，两者含义不同** | C-7 | TIP 块 |
| `path` 匹配首包 HTTP PATH，非空须以 `/` 开头，**不支持 h2c**；匹配是"智能"的，读取不超过 55 字节，不做完整 HTTP 解析，成功输出 `realPath =` | C-7 | `path`: string |
| path 回落用途是分流其它 inbound 的 WS 流量或 HTTP 伪装流量；官方称此方式**理论性能比 Nginx 更强** | C-7 | 同锚点 |
| fallbacks 所在入站本身必须是 TCP+TLS（为分流到其它 WS 入站），**被分流的入站无需配置 TLS** | C-7 | `path` → 注意 |
| `dest` **必填**，缺省无法启动；支持 TCP 地址与 Unix domain socket；填域名时直接发起 TCP 连接而**不走内置 DNS** | C-7 | `dest` |
| ⚠ **版本断裂**：v25.7.26 之后只填 port 的 dest 才指向 localhost，此前都是 127.0.0.1；改动后实际目标很可能是 `::1` | C-7 | `dest` → 注 |
| 因上述变更，**照抄网上模板**的 webserver 可能监听 `::1` 却只允许 127 进入或强制 proxy protocol，导致行为不同 | C-7 | 同锚点 |
| `xver` 用于发送 PROXY protocol 传递真实来源 IP 与端口，填 1 或 2，默认 0；官方建议填 1；1 与 2 功能相同只是结构不同 | C-7 | `xver`: number |
| 配置 Nginx 接收 PROXY protocol 时，除 `proxy_protocol` 外还需设置 `set_real_ip_from`，否则可能出问题 | C-7 | WARNING 块 |
| 匹配命中「最精确」的子元素，与排列顺序无关；若多个子元素 alpn 与 path 均相同，则以**最后一个**为准 | C-7 | 补充说明 |
| 回落分流均是**解密后 TCP 层的转发**，而非 HTTP 层，只在必要时检查首包 PATH | C-7 | 补充说明 |

### 2.7 故障排错

| 结论 | 来源 | 锚点 |
|---|---|---|
| **525 = Cloudflare 与源站之间的 SSL 握手失败** | C-3 | `Error 525: SSL handshake failed` |
| 525 成立需**同时**满足：握手失败 + SSL/TLS Overview 中设为 **Full 或 Full (Strict)** | C-3 | `Common causes` |
| 525 的源站侧常见成因（并列，官方**未给排查顺序**）：未安装有效证书、443（或自定义安全端口）未开放、不支持 SNI、双方 cipher suites 不匹配 | C-3 | `Resolution` |
| 可用 Origin Analytics 的 Origin status codes 图查看 `originResponseStatus` 为 `0` 的时段，作为 TLS 协商失败的指示 | C-3 | `Diagnose with Origin Analytics` |
| **526 = Cloudflare 无法验证源站 SSL 证书** | C-6 | `Error 526: invalid SSL certificate` |
| 526 成立需**同时**满足：无法校验源站证书 + SSL/TLS Overview 中设为 **Full SSL (Strict)** | C-6 | `Common causes` |
| 526 的快速绕行（官方称 workaround 而非修复）：把 SSL 从 Full (strict) 改为 Full | C-6 | `Common causes` → `Resolution` |
| 526 的两条修复路径：把自签名证书加入 Custom Origin Trust Store，或在源站使用 Cloudflare Origin CA 证书 | C-6 | 同锚点 |
| 526 的源站证书核对清单（**并列 7 项，无优先级**）：未过期、未吊销、由 CA 签发（非自签名）、请求域名在 CN 或 SAN 中、证书链完整（需一并提供中间 CA）、源站接受 443 连接等 | C-6 | `Resolution` |
| 建议临时 pause Cloudflare 后，用外部 SSL checker 对该源站证书做独立验证 | C-6 | `Resolution` 末项 |
| **413 = Payload Too Large**，因客户端发送的负载超出服务器可接受上限 | C-4 | `413 Payload Too Large` |
| 最大上传体积按套餐：**Free 100 MB、Pro 100 MB、Business 200 MB、Enterprise 最高 5 GB** | C-4 | `Cloudflare-specific information` 套餐表 |
| 用户可在 zone 的 **Network** 页调整 **Maximum Upload Size**；Enterprise 可自助设到 5 GB 以内 | C-4 | 同锚点 |
| 官方给出的三条绕行：**把请求拆成更小的块、把 DNS 记录改为 DNS-only、升级套餐** | C-4 | 同锚点（含原文引句） |
| ⚠ 其中"改为 DNS-only"**等价于放弃 CDN 代理**，对以 CDN 前置为存在理由的节点而言等于取消方案本身 | C-4 + 本文件推论 | 跨源限定，见 §三-3 |

### 2.8 被墙判定：可用的分类学

| 结论 | 来源 | 锚点 |
|---|---|---|
| OONI 把网络干扰分为三类可测量形态：**TCP/IP blocking、DNS tampering、HTTP blocking** | C-5 | 三个词条 |
| **TCP/IP blocking**：阻止客户端与目标建立 TCP 连接——使目标 IP 不可达，或**主动注入 TCP RST 包**重置该 `IP:Port` 连接 | C-5 | `TCP/IP blocking`（含原文引句） |
| **DNS tampering** 是 DNS hijacking 与 DNS spoofing 的总称；表现为 DNS 查询返回错误 IP | C-5 | `DNS tampering` |
| **DNS hijacking**（= DNS poisoning）：被查询的 resolver 不诚实，主动返回错误应答 | C-5 | `DNS hijacking` |
| **DNS spoofing**（= DNS injection）：DNS 查询在链路上被拦截并注入伪造应答 | C-5 | `DNS spoofing` |
| OONI 对二者边界的定义：**hijacking 的伪造发生在被查询的 resolver，spoofing 的伪造发生在查询被拦截的链路上** | C-5 | `DNS spoofing` |
| **HTTP blocking**：HTTP 层干扰总称，两类实现——投放 block page；HTTP failure（被透明代理拦截、连接被重置、明文连接被劫持重定向） | C-5 | `HTTP blocking` |
| block page 是唯一会明确告知用户审查存在的形式；OONI 的启发式规则下，**检测到 block page 即自动确认审查存在** | C-5 | `Block page`（含原文引句） |
| TCP/IP blocking 的判定基于**与未审查网络的对照**：结果不匹配即标记为 anomaly（官方措辞为 "potential"，非确定） | C-5 | `Network anomaly` |
| **anomaly ≠ 审查**；false positive 成因有四：瞬时网络故障、源站自身不可靠、DNS resolver 按地理就近返回不同 IP、网站按访问国家返回不同内容 | C-5 | `False positive` |
| internet blackout 指某国家/地区互联网被完全切断；**测量断网目前不在 OONI 能力范围内** | C-5 | `Internet blackout`（含原文引句） |
| domain fronting 是按 SNI 与内部目标分离的方式借用大云厂商域名前置流量，依赖审查方不愿造成"附带损害" | C-5 | `Domain fronting` |
| HTTP 451 被 OONI 标注为实现互联网审查所用的状态码 | C-5 | `HTTP status codes` |
| vantage point = 「网络 + 国家」的唯一组合 | C-5 | `Vantage point` |

> ⚠ **C-5 的使用边界**：OONI 的三分法面向**网站审查检测**，**不是代理节点判定手册**。它不含「节点被识别并封禁」这一类，也没有给出可用于自建节点的判定命令与阈值。引用时必须写明这是分类依据，不是操作步骤。

---

## 三、矛盾与限定（写作时必须保留的措辞）

1. **代理资格口径收窄**：B-1 说「A/AAAA/CNAME 可被代理」，B-2 收窄为「只有**承载 HTTP/HTTPS 流量**的 A/AAAA/CNAME 可被代理」。两者不直接冲突，但 **B-2 是更严格的门槛，写作以 B-2 为准并注明**。
2. **"CNAME flattening" 一词两义**：B-1 指 **Cloudflare 侧**对被代理 CNAME 的默认展平；B-7 指**外部权威 DNS 提供商**必须支持的展平能力。读者极易混淆，必须分开表述。
3. **端口缓存结论是推论**：B-3 **只列「禁用缓存」清单（10 个）**，未明文写 80/443 启用缓存。「仅 80/443 走缓存」**属排除推论**，不得写成官方口径。
4. **免费版没有"额外端口"出路**：B-3 只给灰云与 Spectrum 两条路，而全端口 Spectrum 限 Enterprise。即**免费版想代理非 13 端口之一，唯一选择是放弃代理**——这条结论是两条官方事实的合成，写作时须标明。
5. **525 与 526 的判定条件不重叠**：525 需 Full **或** Full (Strict)；526 **仅**需 Full (Strict)。二者是互斥成因，**不是同一故障的两个阶段**。文档未说明同一请求是否可能先失败于 526 再显示为 525。
6. **官方不给排错顺序**：C-3 与 C-6 都只给**并列**成因列表（C-6 明标 7 项并列），**没有**先查证书 / 再查端口 / 再查 cipher 的官方次序。任何"官方推荐顺序"的说法都是编的。
7. **C-4 的范围措辞自相矛盾**：正文说 "The upload limit for the Cloudflare API depends on your plan"，但表格列名是 "Max upload size"，下文又说可在 zone 的 Network 页调整全局 Maximum Upload Size。**同一页内「API 上传限制」与「zone 全局上传限制」未做区分**。Free = 100 MB 这条数字的适用对象（API 还是 zone 全部入站请求）本页无法判定。
8. **C-1 的官方立场是"建议迁走 WS"**：DANGER 块明写推荐换用 XHTTP，理由是 ALPN 特征明显。而 C-2 的 Caddy 章节仍以 WebSocket inbound 为前提给配置——两者不是矛盾，但 **C-1 的迁移建议未被 C-2 跟进**，写作时不应把 WS 写成"官方推荐方案"。
9. **C-7 的 dest 语义有版本断裂**：v25.7.26 前后「只填 port」的目标从 127.0.0.1 变为 localhost（很可能是 `::1`）。**早于该版本的任何教程/模板都需按此重新核对**。
10. **C-2 的"Cloudflare"两处语境完全不同**：C-2 的 Cloudflare 章节只讲**用 DNS 验证申请源站证书**，**不是**讲"把节点挂在 Cloudflare 代理后"；其反代章节只给 Nginx/Caddy，完全不提 Cloudflare。**把它当作"面板套 CDN 的官方教程"是误读**。
11. **C-5 无「被墙」这一术语**：OONI 三分法是审查测量分类，**不含**"节点被识别并封禁"类别，且每条判定均用 potential / anomaly 措辞，唯一"自动确认"的情形是检测到 block page。
12. **A-6 的 CDN 结论语境极窄**：§6.2「CDN AS 不在受影响之列」严格限于**全加密流量被动检测**这一机制，不能推出「CDN 对其它封锁手段免疫」，也不能推出「CDN 是有意豁免」。
13. **A-5 摘要 vs 全文**：A-5 摘要页不含方法细节；D-2 全文已补抓并核对，「附带损害」论证出自 **D-2 §2.3 / §6.1.3**，引用时应指向全文锚点而非摘要。
14. **厂商自述数据无第三方核验**：A-2 的 405 Tbps、95%/50 ms、Argo 提速 30% 均为 Cloudflare 自称。
15. **两处抓取结构损坏**：A-2 `#### Tiered Cache topologies` 表列对齐错乱；D-1 `Compatibility notes` 表产品名列丢失。**引用这两处前必须回源核对**。

---

## 四、可写 / 不可写清单（P3 大纲与 P4 写作的硬约束）

### ✅ 可以写（有 official / primary-research 锚点）

- CDN 的定义、缓存与回源链路、anycast 与就近接入、CDN 的反向代理位置。
- Cloudflare 接入：代理状态、可代理记录类型、pending 期风险与轮换源站 IP 建议、NS 接入 vs CNAME 接入的套餐门槛。
- **完整端口清单与缓存禁用清单**、额外端口的两条路与其套餐限制、非标端口被扫描器报"开放"的官方解释。
- TLS 五种模式对照、Full (strict) 的源站证书四条硬要求、525 / 526 / 413 / 524 的官方成因与绕行。
- WebSocket 在 Cloudflare 侧的支持状态、开关、套餐范围、空闲超时与心跳建议、发布新代码会断连。
- Xray WS 传输字段（path/host/headers/ed/acceptProxyProtocol/heartbeatPeriod）与 fallback 机制，含 v25.7.26 的 dest 版本断裂。
- 3x-ui 侧：用 DNS 验证申请 Cloudflare 证书、Nginx/Caddy 反代面板、订阅路径与 `XUI_SKIP_HSTS`。
- 阻断分类学（OONI 三分法）与"anomaly ≠ 审查"的 false positive 四种成因。
- 「CDN 抗封锁靠附带损害」的原理与其失效边界（D-2 全文锚点）。

### ⛔ 不能写 / 必须降层标注

| 不能写成 | 实际只能写成 | 依据 |
|---|---|---|
| 「官方判定节点是否被墙的方法」 | 只能写"业内常用的判定思路"，并说明 Cloudflare / Xray / 3x-ui 官方均无此内容 | 缺口 1 |
| 「套 CDN 后速度实测下降 N%」 | 只能定性说"回源链路更长"，或标注为社区测量 | 缺口 2 |
| 「官方推荐先查 A 再查 B 再查 C」 | 只能给并列成因清单，由本笔记组织为排查建议 | §三-6 |
| 「面板里这样填就能套 CDN」（当成官方步骤） | 只能写"依据 Xray 官方字段定义 + 面板表单字段对应关系推导"，并标注为推动 | 缺口 2（组 C） |
| 「CDN 对封锁免疫」 | 只能写 §6.2 的原语境：该机制下大型 CDN AS 未受影响，且带 2021-11~2023-02 时间限定 | §三-12 |
| 「仅 80/443 走缓存（官方）」 | 写"文档只列了 10 个禁用缓存的端口" | §三-3 |
| 「视频里说……」（口播） | 一律写「据视频章节推断」 | 视频无字幕 |

### 三处必须回源核对后再引用的表格

1. A-2 `#### Tiered Cache topologies`（列错位）
2. D-1 `Compatibility notes`（产品名丢失）
3. B-5 `Subdomain setup` 父子 zone 可用性表（表体行缺列）

---

## 五、实践指引（可直接进入大纲的可操作结论）

> 以下每条均有上方 claim 映射支撑；标注「推论」处须在正文中保留措辞。

1. **免费版要套 CDN，必须走 NS 全量接入**：Free / Pro 只能 primary (full)，CNAME (partial) 要 Business 起。→ B-5 / B-6 / B-7
2. **接入期间有源站 IP 泄露窗口**：pending 状态下所有记录实际 DNS-only、会返回源站真实 IP，官方建议**激活后轮换源站 IP**。→ B-2
3. **端口要选 13 个之一，且优先 443**：非标端口在免费版无代理出路（灰云 = 放弃 CDN，Spectrum 全端口 = Enterprise）。中国方向还要注意 China Network 域名仅 80/443。→ B-3
4. **TLS 模式选 Full (strict) 的前提是源站有合规证书**；没证书先用 Full 但会明文回源；3x-ui 可直接用 `x-ui` 菜单申请 Cloudflare Origin CA 证书（DNS 验证）。→ B-4 / B-8 / C-2
5. **WebSocket 在 Cloudflare 侧开箱可用，但要主动加心跳**：官方明说双向无数据会被断开，且发布新代码会重启服务器断连。→ D-1（与 C-1 的 `heartbeatPeriod` 呼应）
6. **先验证 443 回源通不通，再看应用层**：525 = 握手失败，526 = 证书验不过；526 的 7 项核对清单可直接做成表。→ C-3 / C-6
7. **大文件上行会撞 413**（Free 100 MB），官方绕行之一"改 DNS-only"对套 CDN 场景等于自毁。→ C-4
8. **判断"是不是被墙了"只能靠分类排除**：用 OONI 三类（TCP/IP blocking / DNS tampering / HTTP blocking）做区分，并记住 anomaly ≠ 审查、有四种 false positive。→ C-5（须标注为分类依据而非官方判定流程）
9. **Xray 侧 443 复用有两条路**：Xray 内置 fallback 分流（官方称理论性能更强）或 Nginx/Caddy 反代分流；C-2 的 Caddy 模板仅适用于 WS inbound。→ C-7 / C-1 / C-2
10. **照抄旧模板有坑**：v25.7.26 后 `dest` 只填 port 会指向 localhost（很可能 `::1`），旧模板的 webserver 可能监听 `127.0.0.1` 而不匹配。→ C-7

---

## 六、开放问题（进入 P3 前需明确的）

1. **「被墙判定」这一节写到什么程度？** 没有官方来源可依。建议：写成"分类排除 + 三步自检"的经验小节，明确标注为经验方法，并链到 OONI 的 false positive 说明。需用户在 P3 确认篇幅。
2. **面板侧（3x-ui）套 CDN 的具体字段填法无官方来源**：可作为"依据 Xray 官方字段 + 面板表单结构推导"的操作小节，但必须标注为推动。或者按 P0 已定的"不复述面板操作"原则，只写"在面板中把入站传输设为 WebSocket，Host/Path 填 CDN 域名与路径"这一句并链回面板流笔记。**需用户拍板。**
3. **作者配套 Notion 文档未抓取**（SPA，且与上一期共用同一链接）。是否需要为本篇补抓一次 JS 渲染版本？若不抓，视频步骤的书面来源就只有上一期那份文档。
4. **免费域名获取 / 托管解析**：按 P0 已定只做指路（链到同系列两期视频）。本篇不展开，但需要在正文给出一句"没有域名先去这里"。
5. **两张残缺表是否回源核对**（A-2 Tiered Cache、D-1 兼容性）：两张表都非本篇主线（Tiered Cache 属进阶缓存、兼容性表只影响两条边注），**建议不回源，直接在正文回避这两处引用**。

---

## 七、下游交接说明（P3 / P4 必读）

### 给 outline-generator

- 素材路径：`workspace/vps-node-cdn-rescue/sources/{ID}.md`（23 篇）。
- 建议主线（对齐视频章节 + P0 确认）：**① CDN 是什么 → ② 为什么能救被墙（原理与边界）→ ③ 接入 Cloudflare 与域名解析 → ④ 把节点套上 CDN（TLS/端口/WS）→ ⑤ 被墙判定与加速取舍 → ⑥ 排错速查**。
- 第四章「把节点套上 CDN」**不含**"安装面板 / 搭建节点"（P0 已定不复述），只写与 CDN 相关的配置（TLS 模式、端口选择、WS 开关、回源验证）。
- 与既有笔记的互链：`自建代理节点搭建实战.md`、面板流笔记（运行中）、`自建代理节点 MOC.md`。

### 给 chapter-writer

- **禁止转述本文件的结论当原文**：本文件是 claim 摘要，写作时必须回 `sources/{ID}.md` 的原锚点核对。
- 引用粒度：每条事实性结论挂 `[^{ID}-{锚点}]` 形式的来源标注；「推论」处必须显式写「推论」。
- 视频口播不可得：凡视频结论一律写「据视频章节推断」，**不得**写成视频原话。
- 保留措辞清单：§三 的 15 条矛盾与限定中，第 1、3、4、5、6、8、10、12 条**必须在正文体现**。
- 不可写清单：§四 的 ⛔ 表逐条遵守。
- 用户偏好：核心概念加 `[!tip] 大白话` 通俗解释 + 打比方类比；按「它是什么 → 具体产物长什么样 → 带具体值的可代入例子 → 对比表 → 大白话类比」的顺序落地。

### 尚未解决

- §六 的第 2 条（面板字段写到什么程度）需要在 P3 前拿到用户决定；其余开放问题都可在 P3 大纲里以"占位或指路"方式落地。
