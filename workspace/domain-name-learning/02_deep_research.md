# 域名相关的学习 - 深度研究素材（P2）

- **运行**: domain-name-learning（learning-note-flow）
- **日期**: 2026-09-04
- **阶段**: P2 深度收集
- **方向**: D 三线并进（原理 → 注册解析 → 实战接入）
- **读取缓存**: `workspace/domain-name-learning/.cache-{a,b,c}/`（源正文缓存，下游无需重抓）

## 1. 范围

为「域名相关的学习」（入门了解 → 上手可用，概念 + 实战混合）收集的素材。覆盖三层：
1. **原理层**：DNS 解析链路、域名层级、记录类型、TTL/缓存/DNS 传播、IDN/中文域名。
2. **管理合规层**：注册/选购、实名、国内 ICP 备案、解析托管与 NS 委派、转移、域名安全。
3. **实战层**：域名接自建服务——Caddy/Nginx+certbot HTTPS、Cloudflare Tunnel、Tailscale Funnel、frp，以及大陆可用性与合规现实。

素材以官方文档与厂商一手文档为主（约 78%），注册商资讯与社区经验仅作价格量级/运维经验参考。

## 2. 源清单

| id | 标题 | url | tier | date |
|----|------|-----|------|------|
| A1 | DNS records（Cloudflare Learning） | https://www.cloudflare.com/learning/dns/dns-records/ | 官方教程 | 抓取 2026-09-04 |
| A2 | What is DNS?（Cloudflare Learning） | https://www.cloudflare.com/learning/dns/what-is-dns/ | 官方教程 | 抓取 2026-09-04 |
| A3 | Enabling IDNs（ICANN Blog） | https://www.icann.org/en/blogs/details/hello-world-enabling-internationalized-domain-names-idns-16-6-2021-en | 官方/一手 | 2021-06 |
| A4 | DNS 基本概念（阿里云云解析） | https://help.aliyun.com/zh/dns/basic-concepts-dns2-0 | 厂商文档 | 抓取 2026-09-04 |
| A5 | 什么是 DNS 传播？（IBM Think） | https://www.ibm.com/cn-zh/think/topics/dns-propagation | 厂商文档 | 抓取 2026-09-04 |
| A6 | DNS 排障工具 dig/nslookup/host（Red Hat） | https://www.redhat.com/en/blog/DNS-name-resolution-troubleshooting-tools | 官方 | 2026 可访问 |
| B1 | ICP备案·域名核验要求（阿里云） | https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/prepare-and-check-the-domain-name | 官方文档 | 抓取 2026-09-04 |
| B2 | 什么是 ICP 备案（阿里云） | https://help.aliyun.com/zh/icp-filing/basic-icp-service/product-overview/what-is-an-icp-filing | 官方文档 | 抓取 2026-09-04 |
| B3 | 域名实名认证（腾讯云） | https://cloud.tencent.cn/document/product/242/6707 | 官方文档 | 2026-08 |
| B4 | 添加子域名解析 / NS 委派（DNSPod） | https://cloud.tencent.cn/document/product/302/105665 | 官方文档 | 2025-12 |
| B5 | Transfer your domain to Cloudflare | https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/ | 官方文档 | 2026-04 |
| B6 | DNSSEC（Cloudflare DNS Docs） | https://developers.cloudflare.com/dns/dnssec/ | 官方文档 | 2026-06 |
| B7 | 域名注册多少钱·2026（新网资讯） | https://www.xinnet.com/knowledge/2142353461.html | 注册商资讯 | 2026-06 |
| B8 | 域名一年多少钱？后缀对比（聚名） | https://www.jm.cn/zx/30459.html | 注册商资讯 | 2026-07 |
| B9 | 域名安全最佳实践（阿里云） | https://help.aliyun.com/zh/dws/user-guide/domain-name-security1 | 官方文档 | 抓取 2026-09-04 |
| C1 | Caddy Automatic HTTPS | https://caddyserver.com/docs/automatic-https | 官方文档 | 抓取 2026-09-04 |
| C2 | Cloudflare Tunnel Docs | https://developers.cloudflare.com/tunnel/ | 官方文档 | 2026-05 |
| C3 | Tailscale Funnel | https://tailscale.com/docs/features/tailscale-funnel | 官方文档 | 2026-01 |
| C4 | frp 自定义域名访问内网 Web（中文示例） | https://gofrp.org/zh-cn/docs/examples/vhost-http/ | 官方文档 | 2026-03 |
| C5 | Certbot 文档（导航） | https://eff-certbot.readthedocs.io/ | 官方文档 | Certbot 5.8 |
| C6 | Certbot User Guide | https://eff-certbot.readthedocs.io/en/stable/using.html | 官方文档 | 同 C5 |
| C7 | certbot.eff.org 指令页 | https://certbot.eff.org/instructions | 官方 | 2026-09 |
| C8 | 搭建网站·ECS 指南（阿里云，0→1） | https://help.aliyun.com/zh/ecs/user-guide/build-a-website/ | 官方文档 | 抓取 2026-09-04 |
| C9 | 边缘设备上云：Frp+CF+Caddy（工程博客） | https://blog.soulter.top/posts/edge-server-tunnel.html | 实操博客 | 抓取 2026-09-04 |
| C10 | Cloudflare 能绕过 ICP 备案吗？（穿云） | https://www.cloudbypass.com/tutorial/9942.html | 实操解读 | 抓取 2026-09-04 |
| C11 | V2EX：域名国内能否访问（社区经验） | https://global.v2ex.co/t/1208376 | 社区经验 | 抓取 2026-09-04 |
| C12 | LINUX DO：被墙的是域名还是服务器 IP | https://linux.do/t/topic/471983/6 | 社区经验 | 抓取 2026-09-04 |

Tier 分布：官方/一手文档 17 条，注册商资讯 2 条，实操博客/社区 4 条。价格类（B7/B8）与社区经验（C11/C12）按"量级/经验参考"引用，不当作事实断言。

## 3. 主题化要点（claim/source map）

### 3.1 原理：DNS 是什么与解析链

- DNS = 域名↔IP 的分布式数据库（电话簿），协议走 UDP/TCP 53；分类：公网/内网、权威/递归 [A2][A4]
- 一次完全未缓存解析涉及 4 类服务器：递归解析器 → 根 → TLD → 权威，典型 8 步；有缓存即跳步 [A2]
- 递归解析器在查询链起点代查并缓存；权威服务器在末端持有记录、是最终事实源 [A2][A4]
- 域名层级：点分标号序列，`.com`=TLD，`aliyun.com`=二级/主域名，`www.aliyun.com`=三级/子域 [A4][A3]
- 上层服务器只存"下一级服务器地址"，逐级下查；最高层是根 [A4]
- 查子域时权威之后还可能多一级存该子域 CNAME 的服务器 [A2]

### 3.2 原理：递归/缓存/TTL/DNS 传播

- 查询类型：递归=代查到底；迭代=只给"下一步问谁"；非递归=命中缓存/权威直接答 [A2]
- 浏览器/OS/ISP 递归器逐级缓存；Chrome 可 chrome://net-internals/#dns 查浏览器缓存 [A2]
- 所有记录带 TTL = 该记录在缓存中保留/刷新间隔；TTL 越小改动生效越快、查询频率越高 [A1][A4]
- DNS 传播 ≠ 全球同步，而是各级缓存按 TTL 过期；生效速度受 TTL、ISP 缓存（偶有忽略 TTL）、根/TLD 更新影响；通常数小时到数天 [A5]
- "秒级生效"多见于商业宣传（如 IBM 自家 NS1），须标注商业立场（推断）[A5]

### 3.3 原理：记录类型与常见坑

- A=IPv4；AAAA=IPv6；CNAME=别名转发（不提供 IP）；MX=邮件；TXT=文本（SPF/所有权验证）；NS=该域域名服务器；SOA=域管理；SRV=服务+端口；PTR=反向查询 [A1][A4]
- 主机记录 `@`=主域本身，`*`=泛解析；别用泛解析兜底 [A4]
- **CNAME 不能用于根域/apex**（不能与其它记录共存）；根域要 CNAME 效果用服务商 ALIAS/ANAME [A1][A4]
- CAA 声明允许哪些 CA 为该域发证书，可被子域继承 [A1]
- DNSSEC 用数字签名防欺骗与缓存污染 [A4][B6]
- DoH/DoT（RFC 8484/7858）加密 DNS 请求 [A4]
- TXT 单条记录 255 字节、可拼接；"512 字符"是阿里云产品录入上限（语境差异）[A4]

### 3.4 原理：IDN / 中文域名

- DNS 底层 ASCII；IDN 让本地文字进域名，浏览器/工具自动转 Punycode（A-label `xn--`）[A3]
- 2021 数据：37 语言 23 文字、154 个 IDN TLD 入根；IDN 注册约 830 万个，77% 在 ccTLD 下 [A3]
- 现实障碍是"通用接受 UA"：软件/邮箱须能处理非 ASCII 域名与邮箱 [A3]
- Punycode 编码细节与同形攻击风险本批未充分展开 → 见开放问题 [A3]

### 3.5 原理：排障工具（缺口补齐）

- 查记录：`dig example.com`（默认 A）、`dig example.com MX`、答案只看 `+short` [A6]
- RCODE：NOERROR 正常 / NXDOMAIN 不存在 / SERVFAIL 上游或权威故障 / REFUSED 拒绝递归 [A6]
- 改了解析仍旧：`dig @1.1.1.1 example.com` 与默认对比——公共递归器新而本地旧=本地缓存未过期；两边旧=真没生效 [A6]
- `dig +trace` 看根→TLD→权威整条委托链；`dig @权威 example.com` 绕过缓存看"最终事实" [A6]
- Windows 用 `nslookup -type=MX example.com` / `nslookup example.com 8.8.8.8` [A6]

### 3.6 管理合规：ICP 备案（大陆强约束）

- 解析至**中国大陆服务器**的网站/App 必须备案（非经营性备案制，经营性须 ICP 证）；域名放境外服务器无需备案 [B2][B1]
- 未备案直接解析到大陆服务器，接入商监测会阻断访问；换接入商须"接入备案" [B2]
- 备案只备主域名，其下子域名免额外备案；阿里云代备案不支持 IP 备案 [B2][B1]
- 域名核验要求：后缀须在工信部批复列表（.org 等未批复→大陆备案不可用）；注册商须为批复机构；实名四要素与备案主体一致；到期须 >45 天 [B1]
- 阿里云国际站注册的域名须转入中国内地注册商并实名后才可备案 [B1]
- 实名失败将处于 Serverhold（暂停解析）；通过后约 48h 恢复 [B3]

### 3.7 管理合规：实名、子域委派、转移（国内外对照）

- 实名：个人=身份证彩色件；企业=营业执照；企业联系人须填个人（建议法人）；审核 1~3 工作日 [B3]
- 注册商与解析商可分离：域名留在 A，DNS 交 B（DNSPod/阿里云）；子域可加 **NS 记录独立委派**到另一解析商，用 TXT 记录做归属校验 [B4]
- 子域解析优先于主域同名记录；子域名不支持 URL 转发 [B4]
- 转移规则（ICANN）：注册满 60 天且 60 天内未转出；近 60 天改注册人信息触发 60 天锁；转出须解锁（clientTransferProhibited）+ 授权码（EPP），码有效期短 [B5]
- gTLD（.com/.net/.org）转移通常顺延 1 年；Cloudflare Registrar 按成本价无加价 [B5]
- 已开 DNSSEC 时改 NS 前须先关并等 TTL 过期（约 24–48h）[B5][B6]

### 3.8 管理合规：域名安全（缺口补齐）

- 安全分层：账户 MFA → 注册商禁止转移锁/禁止更新锁 → 注册局安全锁（serverDelete/Transfer/UpdateProhibited）→ DNSSEC [B9]
- 个人基线：MFA + 禁止转移锁；核心域加注册局锁 + DNSSEC [B9]
- DNSSEC 启用=解析商签名生成 DS → 到注册商加 DS；Cloudflare 首选算法 13（ECDSA P-256/SHA-256）[B6]
- 社区提示：2FA 只保护登录，转移流程未必二次验证（TrustName 事件，未抓官方原文，需复核）[B8→见注]

### 3.9 价格与选购（大陆视角，量级参考）

- 聚名 2026-07 报价（首年→续费，¥）：.com 85→95、.cn 38→42、.net 99→109、.xyz 15→98、.top 28→68、.shop 18→118、.icu 22→98 [B8]
- 新网口径：.cn 首年 ¥28–55；.com 首年 ¥68–129 多数次年 ¥139+；.xyz/.site 首年 ¥19–39 [B7]
- 结论：**首年低价后缀续费常大涨**；长期品牌选 .com/.cn/.net，开自动续费；下单前同平台对比"首年+续费"两列 [B8][B7]

### 3.10 实战：Caddy 自动 HTTPS

- Caddy 默认对所有站点开 HTTPS：公网域名用 LE/ZeroSSL（ACME），内网/本地名用自建本地 CA；自动续期并默认 80→443 跳转 [C1]
- 触发自动 HTTPS 条件：A/AAAA 指向本机 + 80/443 公网可达 + 配置含域名 [C1]
- HTTP-01(80)/TLS-ALPN(443) 需对应端口公网可达；DNS-01 需 DNS 商凭据写 TXT，无需开端口，是通配符证书唯一途径 [C1]
- 通配证书 LE 强制 DNS-01；Caddy 2.10+ 自动用通配证书服务子域 [C1]
- 测试/反复续期务必切 LE staging，否则限流封禁最长一周 [C1]
- 本地 localhost/IP 由本地 CA 签；`.ts.net` 域名 Caddy 不托管，握手时向本机 Tailscale 取证书 [C1]
- 最小反代：Caddyfile `example.com { reverse_proxy 127.0.0.1:端口 }` [C1→推断应用]

### 3.11 实战：Nginx + Certbot

- certbot 分 authenticator（证明控域）与 installer（改 Web 配置）；`certbot --nginx` 自动签发并装入 Nginx，可 rollback [C6]
- `certonly --webroot -w <根> -d 域` 免停机 http-01；`--standalone` 需独占 80 [C6]
- dns 插件（certbot-dns-*）是通配证书唯一途径；`--manual` 默认不自动续期 [C6]
- `certbot renew` 只续临期证书（阈值=剩余寿命 <1/3，寿命≤10 天则 <1/2）；判断"真续期"用 `--deploy-hook` 重载服务 [C6]
- 证书在 `/etc/letsencrypt/live/<cert>/`（fullchain.pem + privkey.pem）；目录默认 0700 [C6]

### 3.12 实战：无公网 IP 方案

- **Cloudflare Tunnel**：cloudflared 出站-only 连 CF 边缘，无需公网 IP/入站端口；CDN/WAF/DDoS 自动生效；公网主机名映射本地服务（HTTP/TCP/SSH）；依赖域名托管在 CF [C2]
- **Tailscale Funnel**：`tailscale funnel 3000` 得公网 HTTPS URL `https://<主机>.<tailnet>.ts.net`；仅能绑 ts.net 域、不能绑自有域名；仅 443/8443/10000；带宽受限；MagicDNS + tailnet HTTPS 前置 [C3]
- **frp**：frps 开 `vhostHTTPPort`，frpc 配 `type="http"` + `customDomains`；一个端口按 Host 路由多个子域；frp 的 https 代理要求本地服务本身是 HTTPS（frps 不做 TLS 终止），暴露本地 HTTP 需 https2http 插件 [C4]
- 常用组合：frp 出公网 + Caddy 在 VPS 前做 TLS 终止（`*.edge.你的域名` → Caddy DNS-01 通配证书 → reverse_proxy 到 vhostHTTPPort）[C9]

### 3.13 大陆可用性与合规现实

- **备案看源站服务器物理位置**，不是域名注册地/前端 CDN；"套 CF 免备案"是误区——大陆源站套 CF 仍触碰政策红线 [C10]
- 大陆源站要快 = 大陆服务器 + 备案 + 国内 CDN/CF 中国版（京东云）；免备案+海外快 = 海外/香港服务器 + CF 全球版，代价是大陆延迟 [C10][C11]
- "域名被墙（DNS 污染/封锁）" 与 "服务器 IP 被封" 是两种阻断，处理方式不同 [C12]
- 社区经验：备案≠可访问保障；海外域名国内可解析但 QoS 波动 [C11][C12]

## 4. 冲突与张力（写作时需并列说明）

| 现象 | 说明 | 处理 |
|------|------|------|
| "先查根" vs "缓存可跳步" | A2 未缓存 8 步 vs 缓存命中跳步 | 同一机制两状态，画流程图时并列为"未缓存/已缓存"两条路径 |
| TXT "512 字符" vs 协议 255 字节 | 产品录入上限 vs 协议事实 | 注明语境差异 |
| "传播秒级" vs "数小时到数天" | 商业宣传 vs 通用规律 | 标注商业立场，给通用经验值 |
| Tunnel "零攻击面/免费高可用" vs 大陆访问慢/合规 | 功能承诺 vs 大陆合规/性能现实 | 分开章节讲，避免误读 |
| 价格口径差异（.com 首年 68–129 vs 85） | 不同平台活动/时间点 | 只作量级参考，强调"同平台首年+续费同看" |

## 5. 实战要点汇总（写作可复用清单）

1. 先辨场景：**源站放哪**决定要不要备案（大陆服务器必须备案，境外免备案）。
2. 长期项目域名选 .com/.cn/.net；首年低价后缀看续费；注册即开自动续费。
3. 大陆建站顺序：批复注册商 → 实名模板先行 → 备案（主域到期>45天、实名四要素一致）→ 解析。
4. 域名与解析分离是常态；子域可 NS 独立委派。
5. 解析生效排查三步：`dig @1.1.1.1` 对比默认、`dig +trace`、`dig @权威`；别忘本地/浏览器缓存。
6. CNAME 不要放根域；上线前把 TTL 调低（如 60s）。
7. 有公网 IP + 自有域名：Caddy 反代最省心；已有 Nginx 用 `certbot --nginx`。
8. 无公网 IP：Cloudflare Tunnel（要自有域名、托管到 CF）或 frp+Caddy（自建 VPS）；临时演示 Tailscale Funnel（ts.net）。
9. 域名安全基线：MFA + 禁止转移锁；DNSSEC 换 NS 前先关。
10. 测试 HTTPS/续期逻辑先切 LE staging。

## 6. 开放问题

1. Punycode 编码与同形攻击细节需补一篇技术源（A3 只给背景与数据）。
2. ICANN/注册局/注册商三方在域名生命周期分工（WHOIS/续费/赎回）本批展开不足。
3. .dev 等 Google 运营后缀在大陆注册/备案可行性与报价未确证（推断支持有限）。
4. 大陆注册局对 DNSSEC（尤其 .cn、算法 13）支持范围未核实，需确认"开 DNSSEC 是否影响大陆解析/备案"。
5. Cloudflare Tunnel 免费套餐并发/带宽额度、Tailscale Funnel 具体限速值官方未披露。
6. 各省管局对">45 天""后缀批复"的差异化执行缺省级细则。
7. 2026 年 LE 证书有效期/续期策略（90 天短期证书是否仍演进）未在官方页说明。

## 7. 下游交接（P3 大纲种子）

- 建议按「场景 → 概念 → 选择 → 操作」组织，分三大块：
  1. **原理**：域名是什么 / DNS 解析链（4 类服务器、8 步、缓存） / 记录类型与 CNAME/apex 坑 / TTL 与传播 / IDN 简介
  2. **买到手并管理**：后缀与注册商选择 / 实名与 ICP 备案（大陆） / 解析托管与 NS 委派 / 转移与域名安全（MFA/锁/DNSSEC）
  3. **把域名用起来**：解析到服务器 + Caddy HTTPS / Nginx+certbot / 无公网 IP：Cloudflare Tunnel、frp+Caddy、Tailscale Funnel / 大陆合规速查
- 关键素材引用：原理章用 A1/A2/A4/A5；管理章用 B1/B2/B3/B4/B5/B6/B9；实战章用 C1/C2/C3/C4/C6；价格仅作附注（B7/B8）；合规用 C10/C11/C12。
- 动手部分可基于读者已有 Docker/反代基础，给出可直接复制的 Caddyfile、frpc/frps.toml、certbot 命令片段。
