# 01 探测式收集结果 - 自建代理节点

## 元信息

- **运行标识**: self-hosted-proxy-node
- **工作流 / 阶段**: learning-note-flow / P1 探测式收集
- **检索透镜数**: 3（概念与原理层 / 服务端方案与搭建 / VPS 准备与运维硬化）
- **检索日期**: 2026-09-23
- **原始候选**: 15 条 → **去重后 14 条**
- **去重说明**: `https://xtls.github.io/config/transports/reality.html` 同时命中 `L1-2`（原理）与 `L2-1`（配置字段），合并为 `S-2`，在两个用途下复用。
- **信源分级**: tier-1 = 官方文档 / 官方仓库 / 规范原文；tier-2 = 有署名实现报告 / 权威技术博客；tier-3 = 社区讨论（仅作运维经验）

## 去重后信源表

| ID | 标题 | 信源 | tier | 分 | 一句话相关性 |
| --- | --- | --- | --- | --- | --- |
| S-1 | Xray 传输配置：传输方式 / 传输安全 / 附加配置 | https://xtls.github.io/config/transport.html | tier-1 | 5 | 官方把 raw/xhttp/grpc 等传输方式与 none/tls/reality 安全层分开说明并给出兼容表，是讲清「协议层 vs 传输层」的一手入口 |
| S-2 | REALITY 官方配置文档 | https://xtls.github.io/config/transports/reality.html | tier-1 | 5 | 官方定义 REALITY 为对 TLS 的改动式伪装（借目标站握手外观、消除服务端指纹、鉴权失败回落 target），并列服务端/客户端字段 |
| S-3 | RFC 8446: TLS 1.3 | https://www.rfc-editor.org/rfc/rfc8446.txt | tier-1 | 4 | TLS 1.3 规范原文，给「REALITY 只改 TLS」定位到具体握手环节的权威底稿 |
| S-4 | refraction-networking/utls | https://github.com/refraction-networking/utls | tier-1 | 4 | ClientHello 层指纹模拟能力的官方实现说明，含自身局限，是理解伪装与指纹机制的核心来源 |
| S-5 | sing-box：General（Profile / Remote 远程配置） | https://sing-box.sagernet.org/clients/general/ | tier-1 | 4 | 官方定义 Profile 的 Local/Remote 形态与远程订阅更新周期，是订阅机制在客户端侧的规范表述 |
| S-6 | XTLS/Xray-examples 官方配置示例仓库 | https://github.com/XTLS/Xray-examples | tier-1 | 5 | 官方完整配置示例集（含 VLESS-XTLS-uTLS-REALITY 服务端与客户端），可对照套用，最贴合上手实战 |
| S-7 | sing-box：Hysteria2 入站配置 | https://sing-box.sagernet.org/configuration/inbound/hysteria2/ | tier-1 | 5 | 官方 Hysteria2 inbound 参考页，覆盖 up/down_mbps、obfs、tls、masquerade、bbr_profile 等 QUIC 专属字段 |
| S-8 | 3X-UI（MHSanaei/3x-ui）官方仓库与 Wiki | https://github.com/MHSanaei/3x-ui | tier-1 | 5 | Xray 面板官方仓库，含安装脚本、版本固定、Docker 与数据库选项，面板化快速上手的主流路径 |
| S-9 | Remnawave 官方文档：Panel 安装 | https://docs.rw/install/remnawave-panel/ | tier-1 | 4 | 面板与 Node 分离的 Docker Compose 部署流程，代表较新的节点管理架构 |
| S-10 | The Debian Administrator's Handbook — Ch.14 Security | https://debian-handbook.info/browse/stable/security.html | tier-1 | 5 | Debian 官方手册安全章，覆盖安全策略、nftables、日志与活动监控、入侵后处置，是硬化的概念与流程总纲 |
| S-11 | fail2ban 官方仓库（README + manpage + wiki） | https://github.com/fail2ban/fail2ban | tier-1 | 4 | 登录爆破防护的权威配置依据，附 jail.conf(5) 与 wiki |
| S-12 | Linux Kernel Documentation — IP Sysctl | https://docs.kernel.org/networking/ip-sysctl.html | tier-1 | 4 | 内核官方 sysctl 文档，权威描述 tcp_congestion_control，是启用 BBR 时写参数的规范依据 |
| S-13 | Restic 官方文档 | https://restic.readthedocs.io/en/stable/ | tier-1 | 4 | 仓库初始化、加密、备份恢复、forget/prune 保留策略，适合备份迁移方案参考 |
| S-14 | Spamhaus Reputation Checker 排障说明 | https://www.spamhaus.org/resource-hub/ip-and-domain-reputation-checker/spamhaus-reputation-checker-troubleshoot-your-listing/ | tier-1 | 3 | 官方 IP/域名信誉查询与 CSS 判定点（PTR、HELO、FCrDNS），判 IP 是否被打脏的权威入口，但偏邮件信誉视角 |

## 可达但未列入的备选（已实测可访问）

| 来源 | URL | 说明 |
| --- | --- | --- |
| sing-box TUIC v5 入站 | https://sing-box.sagernet.org/configuration/inbound/tuic/ | 受 5 条上限未列入；若方向含 TUIC 需补 |
| Marzban 官方安装文档 | https://gozargah.github.io/marzban/en/docs/installation | 主仓 2026-06 后趋于停滞；`Marzban-node` 已被维护者明示不再支持并指向 `M03ED/gozargah-node` |
| Hiddify Manager | https://hiddify.com/manager/ | 文档托管在教程页而非仓库内，步骤粒度弱于其他官方文档 |
| Debian Wiki — PeriodicUpdates | Debian Wiki（unattended-upgrades） | 自动安全更新的官方 Wiki 依据 |
| OneUptime BBR 实战指南 | tier-2 | 含 sysctl 命令的实操向参考 |
| Prometheus node_exporter | 官方仓库 | 监控方向可补 |

## 覆盖缺口（阶段 2 需降级标注或补齐）

1. **订阅与分享链接格式无 tier-1 规范原文**。`vless://` 参数集、`vmess://`、base64 订阅列表只有客户端与第三方工具文档。阶段 2 若涉及，须**明确标注为 tier-2/3 且非规范**。
2. **入站/出站与「客户端/服务端同格式」缺单一权威页面**，分散在 `S-1`、inbound、outbound 与 sing-box 配置页之间，需自行汇总（汇总结论须标为 inference）。
3. **协议横向对比（VLESS / VMess / Trojan / Shadowsocks）无官方对照文档**，只能从各协议页分别汇总。
4. **检测侧指纹（JA3/JA4）只有厂商安全博客**，本轮未收录为候选，属可补的 tier-2 缺口。
5. **面板侧无端到端「首个入站」分步官方教程**，必须结合 `S-2` / `S-6` / `S-7` 的内核字段文档补齐。
6. **「脏 IP」判定无 tier-1 规范原文**，依赖商业信誉服务与黑名单运营方工具页（`S-14` 为邮件信誉视角）。此项若写入笔记须标为经验性判断。
7. **BBR 在内核文档中无独立页面**，只能经 `S-12` 与源码 `net/ipv4/tcp_bbr.c` 间接确认；BBRv2/v3 未进主线。
8. **Debian 官方 Securing Debian Manual 入口已失效**（`debian.org/doc/manuals/securing-debian-manual` 返回 404），退回到 harden-doc 包与 Debian Wiki。
9. **Debian 12 / Ubuntu 22.04 硬化缺单页官方 checklist**，「公钥登录 + 禁 root + 防火墙 + fail2ban + 自动安全更新」需从多页拼合。

## 方向菜单

| 方向 | 一句话 | 阶段 2 核心源 | 适合 |
| --- | --- | --- | --- |
| **A. 面板优先上手** | 先用 `S-8` 3X-UI 跑通 VLESS+REALITY，再回补概念 | S-8, S-2, S-6 | 想尽快拿到能用的节点，概念后置 |
| **B. 内核直配（概念与字段对齐）** | 用 Xray-core 原生配置逐字段理解 REALITY，概念与实战一一对应 | S-1, S-2, S-3, S-6 | 与「先讲概念再实战」的目标最贴合 |
| **C. 双栈实战（TCP 主线 + QUIC 备用）** | B 路线再加 sing-box + Hysteria2 作为备用线路，覆盖协议冗余 | S-1, S-2, S-6, S-7, 可补 TUIC | 想要真实可用的抗单点方案 |
| **D. 硬化与运维优先** | 把 VPS 硬化与备份作为第一章实战，再搭节点 | S-10, S-11, S-12, S-13, S-14 | 更看重长期稳定与安全 |

> 四个方向共享同一套概念铺垫需求（S-1 / S-2 / S-3），差别在实战主线与深度收集重心。

## 阶段 2 预估范围

- **深度精读**: 3-5 个核心源（随方向而定），目标产出 `02_deep_research.md`
- **需要补齐的缺口**: 订阅格式（降级标注）、协议横向对比（自行汇总）、面板首入站步骤（跨源拼合）
- **预计新增检索**: 若选 C 方向，需补 sing-box TUIC 页；若选 D 方向，需补 Debian Wiki 与 OneUptime 两条
- **时效提醒**: `S-8` / `S-9` 迭代频繁；Marzban 生态已变动，若笔记涉及多节点方案须按当前状态描述，不得沿用旧教程

## 待用户决策

- [ ] 从方向 A / B / C / D 中选择一个（可组合，例如 B + D）
- [ ] 确认信源质量与缺口标注方式是否接受
