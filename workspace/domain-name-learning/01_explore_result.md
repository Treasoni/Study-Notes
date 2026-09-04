# 域名相关的学习 - 探测式收集结果（P1）

- **运行**: domain-name-learning（learning-note-flow）
- **日期**: 2026-09-04
- **阶段**: P1 探测式收集 ✅ 已完成（等待方向选择）
- **目标**: 入门了解 → 上手可用；概念 + 实战混合

## 探测镜头

| 镜头 | 内容 | 候选源数 |
|------|------|---------|
| A 原理 | 域名层级、DNS 解析全流程、记录类型、TTL/DNS 传播 | 5 |
| B 注册/备案/管理 | 选购、实名、国内 ICP 备案、注册商/解析商分离、转移 | 5 |
| C 实战接入 | CDN/HTTPS、Caddy/Nginx 反代、Cloudflare Tunnel/DDNS/frp | 5 |

共 15 条候选，按 canonical URL 去重后 0 重复。

## 候选源清单

### 镜头 A：域名与 DNS 原理

1. **什么是 DNS？——DNS 如何工作**（Cloudflare Learning）
   url: https://www.cloudflare.com/learning/dns/what-is-dns/
   tier: official-doc | date: unknown | score: 5
   图解解析全流程：递归/权威服务器、缓存与 TTL 角色，入门首选。
2. **DNS 记录类型详解**（Cloudflare Learning）
   url: https://www.cloudflare.com/learning/dns/dns-records/
   tier: official-doc | date: unknown | score: 5
   逐条说明 A/AAAA/CNAME/MX/TXT/NS/SRV 用途与适用场景。
3. **DNS 基本概念**（阿里云帮助中心）
   url: https://help.aliyun.com/zh/dns/basic-concepts-dns2-0
   tier: official-doc | date: unknown | score: 4
   中文官方文档：根/顶级/二级/子域名结构、递归迭代、TTL 术语。
4. **什么是 DNS 传播？**（IBM）
   url: https://www.ibm.com/cn-zh/think/topics/dns-propagation
   tier: official-doc | date: unknown | score: 4
   中文解读：DNS 传播本质是缓存按 TTL 过期，纠正"全球同步"误区。
5. **Enabling IDNs / 中文域名机制**（ICANN 官方博客）
   url: https://www.icann.org/en/blogs/details/hello-world-enabling-internationalized-domain-names-idns-16-6-2021-en
   tier: primary | date: 2021-06 | score: 4
   IDN/中文域名：U-label 与 A-label、Punycode 编码与同形攻击风险。

### 镜头 B：注册/备案/解析管理

1. **域名准备与检查**（阿里云 ICP 备案帮助）
   url: https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/prepare-and-check-the-domain-name
   tier: official-doc | date: unknown | score: 5
   备案前域名核验：批复后缀白名单、注册商资质、实名主体一致、有效期。
2. **什么是 ICP 备案**（阿里云产品概述）
   url: https://www.alibabacloud.com/help/zh/icp-filing/basic-icp-service/product-overview/what-is-an-icp-filing
   tier: official-doc | date: 2026-05 | score: 5
   大陆服务器备案制度、申请/变更/注销/取消接入流程与管局规则。
3. **域名实名认证**（腾讯云域名注册操作指南）
   url: https://cloud.tencent.cn/document/product/242/6707
   tier: official-doc | date: unknown | score: 5
   个人/企业实名材料、信息模板、Serverhold 暂停解析、转入需重新实名。
4. **添加子域名解析**（腾讯云 DNSPod 云解析 DNS 文档）
   url: https://cloud.tencent.cn/document/product/302/105665
   tier: official-doc | date: 2025-12 | score: 4
   A/CNAME/MX/TXT 与 NS 委派，注册商与解析商可分离的操作演示。
5. **Transfer your domain to Cloudflare**（Cloudflare Registrar）
   url: https://developers.cloudflare.com/registrar/get-started/transfer-domain-to-cloudflare/
   tier: official-doc | date: 2026-04 | score: 4
   海外注册商转移前提、60 天锁、WHOIS 默认隐藏，与国内备案路径对照。

### 镜头 C：实战接入自建服务

1. **Caddy 自动 HTTPS 官方文档**
   url: https://caddyserver.com/docs/automatic-https
   tier: official-doc | date: unknown | score: 5
   一个域名 + server 块即自动签发续期 HTTPS，反代子域到内网 Docker 最省心。
2. **Cloudflare Tunnel 官方文档**
   url: https://developers.cloudflare.com/tunnel/
   tier: official-doc | date: 2026-05 | score: 5
   无公网 IP：cloudflared 出站连接 + 自定义域名自动 HTTPS，免费。
3. **Tailscale Funnel 官方文档**
   url: https://tailscale.com/docs/features/tailscale-funnel
   tier: official-doc | date: unknown | score: 4
   无公网 IP 免证书发布本机服务为 HTTPS 公网链接，适合临时对外联调。
4. **frp 通过自定义域名访问内网 Web 服务**（gofrp 官方示例）
   url: https://gofrp.org/zh-cn/docs/examples/vhost-http/
   tier: official-doc | date: 2026-03 | score: 4
   自建 VPS 中转：vhostHTTPPort + customDomains 按域名反代到内网服务。
5. **Certbot（Let's Encrypt 官方客户端）文档**
   url: https://eff-certbot.readthedocs.io/
   tier: official-doc | date: unknown | score: 4
   Nginx 等 Web 服务器自动签发与续期免费证书的标准做法。

## 方向菜单

- **A. 原理为主**：深入 DNS 机制、域名层级与记录类型（偏概念，为后续打底）
- **B. 注册/备案为主**：选购 + 实名 + 国内 ICP 备案 + 解析托管（大陆建站路径）
- **C. 实战接入为主**：把域名用起来——HTTPS/反代/内网穿透/DDNS（服务上线路径）
- **D. 三线并进（推荐，对应先前方向 E）**：按「原理 → 注册解析 → 实战接入」顺序成篇，入门到上手一体

## 覆盖缺口（P2 需补齐）

1. 缺少国内注册商**价格与后缀选购对比**的实测/官方价格页资料。
2. 缺少 **DNS 排障工具**（dig/nslookup/在线解析查询）的一手教程。
3. 缺少「中国大陆访问：海外域名/海外 DNS + CDN 的可用性与备案关系」讨论。
4. 缺少一篇 **0→1 串联**（一个真实域名从购买到 HTTPS 上线的端到端）综合教程。
5. 域名安全专题（DNSSEC、账户二次验证、转移锁）仅 Cloudflare 源覆盖，可补 1 条。

## P2 范围估算

- 三线并进（D）：从每镜头 5 条中选核心 3–5 条精读，加上缺口补齐约 **12–16 个源**；产出 `02_deep_research.md`。
- 单线聚焦（A/B/C）：核心精读约 **5–8 个源**，其余转作"延伸阅读"清单。
