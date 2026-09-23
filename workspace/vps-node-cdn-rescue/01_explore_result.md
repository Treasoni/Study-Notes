# 01 探测式收集结果 - VPS 被墙节点 CDN 拯救实战（Cloudflare CDN 回源）

- **运行标识**: vps-node-cdn-rescue
- **阶段**: P1（探测式收集）
- **检索日期**: 2026-09-24（子代理探测 + 父流程 21 条 URL 全量复核）
- **派发记录**: 3 个透镜 × 1 个子代理（并发 3，符合「≤3 delegates / ≤4 同类并发」约束）
- **数据来源**: 视频章节骨架（见 `00_intent.md`）+ 官方文档探测
- **视频转录状态**: ⚠ 无字幕（本次两次独立核验：watch 页无 `captionTracks`；`yt-dlp --list-subs` 返回 has no subtitles / no automatic captions）→ **本阶段未产生任何"视频原话"类记录**，视频结论一律标注「据视频章节推断」

---

## 一、透镜与探测结果

### 透镜 A：概念层 —— CDN 是什么、为什么能救被墙节点
Subagent A（17 tool calls）。核心产出：Cloudflare 官方概念页与参考架构、AWS CloudFront 官方机制页、MDN 中立术语定义、两篇 USENIX 一手论文（CDN 抗封锁、全加密流量检测）。

### 透镜 B：接入与配置层 —— Cloudflare 官方文档
Subagent B（18 tool calls）。核心产出：代理状态与限制、**网络端口参考页**、SSL/TLS 加密模式、DNS 接入方式总览（NS 接入 / CNAME 接入 / 子域接入）。

### 透镜 C：实战与被墙层 —— 套 CDN 的配置出处与被墙判定
Subagent C（19 tool calls）。核心产出：Xray 官方 WebSocket 与回落配置页、3x-ui 官方 wiki 的 Cloudflare 章节、Cloudflare 525/526/413 官方排错页、OONI 阻断类型定义。

---

## 二、来源表（已按 canonical URL 去重）

> tier 口径：`official` = 项目官方文档/厂商官方页/官方仓库；`primary-research` = 同行评议或测量机构一手研究；
> `community` = 第三方教程/经验帖，仅可作操作性经验并须标注层级。

### 概念层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| A-1 | What is a CDN? — Cloudflare Learning Center | https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ | official | 厂商官方概念页，定义 CDN 为地理分布式服务器群，解释边缘缓存、就近接入、反向代理、负载均衡与 anycast 机制，并给出加速、降带宽、冗余、安全四类收益，是概念层最直接的总览入口。 | 无标识 | 5 |
| A-2 | CDN Reference Architecture — Cloudflare Docs | https://developers.cloudflare.com/reference-architecture/architectures/cdn/ | official | 官方参考架构文档，成体系讲清边缘节点、缓存命中/未命中、回源（origin server）、anycast 与源站 IP 相关的部署取舍，比营销页更适合作「工作原理」章节的技术底稿。 | 2026-04-16 | 5 |
| A-3 | How CloudFront delivers content — AWS CloudFront Developer Guide | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html | official | 另一家厂商的官方机制说明，用请求生命周期串起 DNS 就近路由、边缘 POP 缓存命中/未命中、区域边缘分层缓存与回源取回并写回缓存，是「缓存 + 回源」链路最清晰的对照描述。 | 无标识 | 5 |
| A-4 | CDN — MDN Web Docs Glossary | https://developer.mozilla.org/en-US/docs/Glossary/CDN | official | 简短中立的第三方（非厂商）术语定义，另点出使用第三方 CDN 的三类代价（依赖第三方、额外攻击面、跨源不共享缓存），并明确提到「CDN 在某区域被屏蔽」这一依赖风险边界。 | 2025-07-11 | 4 |
| A-5 | Domain Shadowing: Leveraging CDNs for Robust Blocking-Resistant Communications（USENIX Security 2021） | https://www.usenix.org/conference/usenixsecurity21/presentation/wei | primary-research | 一手学术论文，论述利用 CDN「任意回源域名」特性规避封锁，并说明审查方要阻断就必须封整个 CDN 域名/IP，是理解「CDN 抗封锁边界」与域名封锁 vs IP 封锁取舍的权威依据。 | 2021-08 | 4 |
| A-6 | GFW Report — 全加密流量检测研究（USENIX Security 2023，补录） | https://gfw.report/publications/usenixsecurity23/en/ | primary-research | 测量机构的一手研究，用于支撑「为什么节点流量会被识别」这一层判断；面向流量检测而非操作手册，只能作原理侧引用。 | 2023 | 3 |

### 接入与配置层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| B-1 | Proxy status · Cloudflare DNS docs | https://developers.cloudflare.com/dns/proxy-status/ | official | 官方概念页，说明代理状态（橙云 Proxied 与灰云 DNS only）的区别、可代理的记录类型、TTL 行为与混合记录处理，是判断域名是否走 Cloudflare 代理的第一入口。 | 2026-04-21 | 5 |
| B-2 | Proxying limitations · Cloudflare DNS docs | https://developers.cloudflare.com/dns/proxy-status/limitations/ | official | 官方限制专页，集中列出代理记录的限制与例外（未激活域名的表现、不可代理的目标、非 HTTP 端口与非标准协议不可转发等），是「套了 CDN 反而不通」的首要排查依据。 | 2026-04-21 | 5 |
| B-3 | Network ports · Cloudflare Fundamentals docs | https://developers.cloudflare.com/fundamentals/reference/network-ports/ | official | 官方参考页，列明 Cloudflare 代理默认可用的 HTTP/HTTPS 端口清单、禁用缓存的端口，以及如何为额外端口启用代理——直接支撑用户点名要的「免费版端口表」。 | 2026-04-20 | 5 |
| B-4 | Encryption modes · Cloudflare SSL/TLS docs | https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/ | official | SSL/TLS 官方页，逐项说明 Flexible、Full、Full (strict) 加密模式的含义、对源站证书的要求与适用场景，给出源站证书要求的权威口径。 | 2026-04-16 | 5 |
| B-5 | DNS setups · Cloudflare DNS docs | https://developers.cloudflare.com/dns/zone-setups/ | official | DNS 接入方式官方总览页，对比 primary（NS 全量接入）、CNAME/Partial、subdomain 等接入路径，是区分 NS 接入与 CNAME 接入的最权威汇总入口。 | 2026-08-25 | 4 |
| B-6 | Full setup（NS 接入）· Cloudflare DNS docs（补录） | https://developers.cloudflare.com/dns/zone-setups/full-setup/ | official | NS 全量接入的分步官方说明（改 NS → 等待激活 → 验证），对应视频 3:30「解析域名」的实际动作。 | 常青页 | 4 |
| B-7 | Partial (CNAME) setup · Cloudflare DNS docs（补录） | https://developers.cloudflare.com/dns/zone-setups/partial-setup/ | official | CNAME 接入的官方说明与适用条件，用于对照「不改 NS 也能套 CDN」的路径与其限制。 | 常青页 | 4 |
| B-8 | Full (strict) 模式细则 · Cloudflare SSL/TLS docs（补录） | https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/ | official | Full (strict) 对源站证书的具体要求（有效、未过期、域名匹配、受信任或 CF 源站证书），是回源 526 类问题的权威对照页。 | 常青页 | 4 |
| B-9 | Cloudflare Free 套餐页（补录） | https://www.cloudflare.com/plans/free/ | official | **营销页**（非开发文档），Free 套餐功能与限额的对外口径；具体额度仍需逐产品文档核对，不可当作单页权威限额表。 | 常青页 | 3 |

### 实战与被墙层

| ID | 标题 | URL | Tier | 相关性 | 日期 | 分 |
|---|---|---|---|---|---|---|
| C-1 | WebSocket（Xray 传输配置官方文档） | https://xtls.github.io/config/transports/websocket.html | official | Xray 官方对 wsSettings 的权威定义，含 path、host、acceptProxyProtocol 与 `?ed=2560` Early Data 降延迟参数，是「节点如何走 WS 套 CDN」的配置出处。 | 无标识 | 5 |
| C-2 | Configuration（3x-ui 官方 wiki） | https://github.com/MHSanaei/3x-ui/wiki/Configuration | official | 面板官方 wiki 中单列 Cloudflare 章节，给出 CDN 场景下的入站参数（域名/Host/Path/TLS/SNI）与面板侧设置要点，是与本项目面板流主线对齐的官方操作性说明。 | 无标识 | 4 |
| C-3 | Error 525 · Cloudflare 官方排错 | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-525/ | official | 官方定义 525 为 CF 与源站握手失败，列出证书缺失、443 未放行、SNI、加密套件四类成因与排查路径，对应套 CDN 后最常见的回源故障。 | 2026-06-16 | 4 |
| C-4 | Error 413 · Cloudflare 官方排错 | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-413/ | official | 官方按套餐列出最大上传体积（Free/Pro 100MB、Business 200MB、Enterprise 至 5GB）及超限绕行方式，是免费版 100MB 上传限制的权威出处。 | 2026-09-03 | 4 |
| C-5 | Glossary（OONI 术语表：DNS tampering / TCP-IP blocking / HTTP blocking） | https://ooni.org/support/glossary/ | primary-research | 测量机构对阻断类型的官方定义，可作「域名被 DNS 污染 / IP 或端口层阻断 / 应用层阻断」三分法的可引用分类依据，但面向网站审查而非代理节点。 | 2023-07-03 | 4 |
| C-6 | Error 526 · Cloudflare 官方排错（补录） | https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-526/ | official | 526 为「源站证书无效」，与 B-8 的 Full (strict) 要求成对，构成回源证书类故障的完整对照。 | 常青页 | 4 |
| C-7 | Fallback（Xray 官方回落配置，补录） | https://xtls.github.io/config/features/fallback.html | official | 官方回落机制说明，用于解释 WS+TLS 场景下 443 端口如何被复用与分流，是「套 CDN 后为什么还要回落」的原理出处。 | 常青页 | 4 |

### 去重说明

- B-1 `proxy-status` 与 B-2 `proxy-status/limitations` 为同一官方站的两个独立页，前者定义、后者给限制与风险，均保留。
- B-5 `zone-setups`（总览）与 B-6/B-7（分项）为同一官方站的总分关系，语义互补，保留。
- B-4 `ssl-modes`（总览）与 B-8 `ssl-modes/full-strict` 同上。
- C-3（525）与 C-6（526）为同级独立排错页，故障对象不同，不视为重复。
- B-9 明确标注为**营销页**，与 B-3（开发文档端口表）层级不同，引用限额结论时以 B-3 与各产品文档为准。
- **本表 20 条候选全部经父流程 curl 独立复核**；其中 B-3 与 B-7 首次返回 `000`（瞬时失败），重试 3 次均 200，已收录。
- 无需人工补录的低分层来源：本阶段**未收录任何 community 层来源**（子代理按「宁缺勿滥」处理），因此 P2 若需要社区踩坑经验，须新增一次带标注的检索。

---

## 三、覆盖缺口（P2 需正面处理）

1. **「节点被墙」的判定没有 official / primary 来源** —— Xray、3x-ui、Cloudflare 官方文档均无此内容；OONI（C-5）面向网站审查的阻断分类，**不能直接当节点判定手册**。P2 只能写「社区操作性经验」，不得伪装成官方判定标准。（与进行中的 `vps-node-panel-tutorial` 缺口 2 同源。）
2. **「套 CDN 比直连慢」无官方一手量化** —— Cloudflare 官方只讲加速（Argo 等），代价侧只有社区实测。P2 若写延迟结论，必须标注为社区测量，或改为定性表述。
3. **Free 套餐限额无开发文档级单页** —— 仅有营销页（B-9）+ 各产品的 plan availability 段落，无单一权威限额表；额度须逐产品核对后拼装，不可概括成一句。
4. **「CDN 隐藏源站真实 IP」缺独立官方术语页** —— Cloudflare 的 origin-server / edge-server 术语页本次返回 403，只能由 A-1/A-2 的反向代理与源站描述间接支撑。
5. **「域名污染 vs IP 封锁」缺权威边界条件** —— 无官方或一手研究直接对比两者在 CDN 场景下的失效条件，只能靠 A-5 的封锁代价论证与 A-4 的「区域屏蔽」提示间接覆盖。
6. **作者配套 Notion 文档为 SPA，需 JS 渲染** —— 且原文无更新日期，不能作为「最新步骤」的唯一依据。
7. **Xray 侧「WS + Cloudflare 回源」无端到端官方教程** —— C-1/C-7 是配置字段定义，C-2 是面板侧要点，完整链路仍须父流程按官方字段拼装，不能引用某一篇「官方完整教程」（不存在）。

---

## 四、P2 建议核心来源与预算

**核心必抓（用户点名的两类优先）**：
- 端口与限制：**B-3**（端口表）、**B-2**（代理限制）、**B-4**（TLS 模式）
- 概念底稿：**A-1** + **A-2**（CDN 是什么 / 工作原理）
- 实操出处：**C-1**（WS 配置）、**C-2**（3x-ui Cloudflare 章节）
- 抗封锁边界：**A-5**（USENIX 2021，CDN 抗封锁）

**缺口补抓（按需）**：B-1、B-5、B-6、B-7、B-8、B-9、C-3、C-4、C-6、C-7、A-3、A-4、A-6

**预算估计**：
- 抓取篇数：核心 8 篇 + 缺口约 4–6 篇 ≈ **12–14 篇**
- 派发：**≤3 个深度阅读子代理**（按来源组分批：概念与抗封锁组 / Cloudflare 配置组 / 实操与排错组），禁止一源一代理
- `02_deep_research.md` 预期体量：**约 18–24 KB**，含来源表、claim/source 映射、矛盾点、开放问题、下游交接说明
- 环境：crawl4ai 环境需先复探（`crawl.sh --help`）；**B-9 与作者 Notion 页若抓取，必须用默认 JS 渲染模式**

---

## 五、方向确认菜单（P1 → P2 用户关卡）

学习方向已由视频章节结构 + P0 确认锁定（概念+实战混合、域名前置只做指路、纳入免费版端口表与限制清单）。
此处确认的只是 **P2 的取材侧重**：

```
[1] 全流程均衡取材（推荐）
    CDN 概念与原理 ~30% + Cloudflare 接入与配置 ~45% + 被墙判定与加速取舍 ~25%
    对应视频 8 个章节，其中 4:52「安装面板」/6:26「搭建节点」按 P0 确认不复述，只做指路

[2] 概念讲透
    加重 CDN 原理与抗封锁边界（A-5、A-6），配置只留最小可跑通路径
    适合你想先搞懂「为什么套 CDN 能救被墙」再动手

[3] 工具手册向
    概念压缩成一节，重心全在 Cloudflare 配置 + 排错（端口 / TLS 模式 / 525 / 526 / 413 / NS 未生效）
    适合当操作速查表用
```

**另需你确认一项**：本透镜抓到两篇 USENIX 一手论文（A-5 CDN 抗封锁、A-6 全加密流量检测）。
放进一篇实操笔记里会让行文偏学术，但它们是本主题**唯一能支撑「抗封锁边界」的高可信来源**（缺口 5 就卡在这）。

- **纳入（推荐）**：在「CDN 为什么能救被墙」一节用一两句给出结论并标注引用，其余不展开
- **不纳入**：该节只保留官方机制描述，放弃「边界条件」的论证

直接回「1 + 纳入」或「按推荐」即可，我据此进 P2。若选 [2] 或 [3] 请一并说明。
