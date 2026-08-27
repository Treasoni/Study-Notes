# Tailscale 使用教程 - 探测式收集结果 (P1)

> 项目：tailscale-usage
> 收集日期：2026-08-28
> 状态：P1 完成，等待用户选择 P2 深挖方向

---

## 方向菜单

1. **Tailscale 基础与安装** — 官方快速入门、各平台安装、`tailscale up` 登录认证、常用命令（status/ip/ping/set）
2. **常用功能实战** — MagicDNS、ACL 基础、subnet router、exit node、`tailscale serve/funnel`、Tailscale SSH
3. **进阶用法** — serve/funnel 与 HTTPS 证书、ACL policy（tags/groups）、容器与 Kubernetes、Headscale 自建控制面、自建 DERP
4. **生态与排错** — 与 ZeroTier/frp 对比选型、打洞失败走 DERP 的诊断排错、免费版限制、社区经验

---

## 候选信源（按镜头分组，已去重）

### 镜头 A：基础安装与常用功能

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| A1 | Tailscale quickstart（官方快速入门） | https://tailscale.com/docs/how-to/quickstart | official | 持续更新 | 5 | 各平台安装、`tailscale up` 登录、添加设备、MagicDNS 概览，主干入门页 |
| A2 | tailscale up 命令参考 | https://tailscale.com/docs/reference/tailscale-cli/up | official | 持续更新 | 5 | 登录认证流程第一手：浏览器登录 URL、auth-key 无头认证、核心 flag（--advertise-routes/--exit-node/--ssh） |
| A3 | Tailscale CLI 参考 | https://tailscale.com/docs/reference/tailscale-cli | official | 持续更新 | 5 | status/ip/ping/set 等子命令完整语法与 flags，常用功能实操权威来源 |
| A4 | Configure a subnet router | https://tailscale.com/docs/features/subnet-routers/how-to/setup | official | 持续更新 | 4 | subnet router 完整配置：--advertise-routes、admin console 审批、客户端 --accept-routes |
| A5 | Exit nodes / route all traffic | https://tailscale.com/docs/features/exit-nodes | official | 持续更新 | 4 | exit node 发布与使用：IP forwarding、--advertise-exit-node、客户端 --exit-node、autogroup:internet 授权 |

> 补充：MagicDNS（https://tailscale.com/docs/features/magicdns）、ACL 基础（https://tailscale.com/docs/features/access-control/acls）官方页，被 A1/A3 覆盖概览，如需专节深入可在 P2 增取。

### 镜头 B：进阶用法

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| B1 | tailscale funnel 命令参考 | https://tailscale.com/docs/reference/tailscale-cli/funnel | official | 持续更新 | 5 | serve/funnel 暴露本地端口为 HTTPS 的完整 CLI 语法、端口限制、`tailscale cert` 证书 |
| B2 | Tailnet policy file 语法参考 | https://tailscale.com/docs/reference/syntax/policy-file | official | 持续更新 | 5 | ACL 进阶权威：HuJSON policy 全语法（tags、groups、tagOwners、autoApprovers、ssh 等） |
| B3 | Tailscale SSH | https://tailscale.com/docs/features/tailscale-ssh | official | 持续更新 | 4 | Tailscale SSH 启用（tailscale set --ssh）、SSH ACL（accept/check）、session recording |
| B4 | Tailscale on Kubernetes | https://tailscale.com/docs/kubernetes | official | 持续更新 | 4 | Kubernetes operator 安装（Helm/oauth）、sidecar、subnet router/exit node（Connector CRD） |
| B5 | Headscale（自建控制面） | https://github.com/juanfont/headscale | report | 持续更新 | 4 | 自托管 Tailscale 控制平面官方仓库，配套自定义 DERP、ACL、Docker 部署 |

> 补充：自定义 DERP 官方文档（https://tailscale.com/docs/reference/derp-servers/custom-derp-servers）、DERP 原理博客（SitePoint: tailscale-peer-relays-nat-traversal-derp）、Headscale 实操报告（onidel.com Ubuntu/Docker）、derper 镜像（github.com/yangchuansheng/derper）、内核态 vs 用户态路由（tailscale.com/docs/reference/kernel-vs-userspace-routers）。

### 镜头 C：生态与排错

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| C1 | Troubleshoot DERP traffic routing issues | https://tailscale.com/docs/reference/troubleshooting/network-configuration/derp-routing | official | 未标注 | 5 | 官方排错页：`tailscale ping` 判别 via DERP / 直连，netcheck 与防火墙定位 |
| C2 | Free pricing plans and discounts | https://tailscale.com/docs/account/manage-plans/free-plans-discounts | official | 2026-04-08 | 5 | 免费版限制一手资料：Personal 6 用户、设备不限（旧 100 设备限制已作废） |
| C3 | Tailscale UDP 穿透失败检测与中继回退状态机 | https://blog.hotdry.top/posts/2026/02/19/tailscale-udp-hole-punching-failure-detection/ | report | 2026-02-19 | 4 | 深度剖析打洞失败检测与 DERP 回退机制，含「沉默失败」与缓解思路 |
| C4 | 裸金属内网穿透对决：frp vs ZeroTier vs Tailscale vs ngrok | https://www.qingyunl.com/news/361.html | report | 未标注 | 4 | 四工具实测吞吐/延迟对比，生态选型维度素材 |
| C5 | Disable relay mode（社区排错帖） | https://forum.tailscale.com/t/disable-relay-mode-always-try-connecting-directly/1933/4 | community | 未标注 | 3 | 对称/硬 NAT 下打洞失败回落 DERP 的真实经验，UPnP、固定 UDP 41641 缓解 |

> 补充：官方 poor-performance-tailnet 排错页（tailscale.com/docs/reference/troubleshooting/poor-performance-tailnet）、pricing-v4 博客（2026-04）、DEV 社区 WireGuard vs Tailscale 对比、XDA Headscale 实测（xda-developers.com）。

---

## 覆盖缺口

1. **自建生态实操（Headscale/DERP）**：官方/仓库源齐全，但缺一篇**中文完整部署实操**（Headscale + 自建 DERP + Docker）；onidel 英文实操可作备选，P2 视需要补 1 篇中文实践。
2. **Tailscale 进阶的多设备/多用户 ACL 场景**：policy-file 语法覆盖了 tags/groups，但缺「多租户/多用户 + 分享节点（tailnet sharing）」的整合示例。
3. **容器/K8s 的中文上手**：官方 K8s 文档为英文；如需中文速成，需补社区教程。
4. **打洞失败的量化缓解数据**：C3 讲机制，缺「UPnP/固定端口/DERP 自建」前后的实测对照（社区零散，可标注为经验值）。

## P2 范围估算

- **核心深读**：约 8-10 篇（official 为主：quickstart、tailscale up、CLI、subnet router、exit node、serve/funnel、policy-file、Tailscale SSH、K8s、DERP troubleshooting、免费版；含 report 级：Headscale、DERP 回退状态机、四工具对比）
- **补充来源**：3-5 篇（MagicDNS/ACL 基础官方页、自定义 DERP 官方、1 篇中文 Headscale 实操、社区排错）
- **产出**：
  - 安装与登录（含 auth-key 无头认证）
  - 常用命令速查（status/ip/ping/set）
  - 常用功能实操（MagicDNS、ACL 基础、subnet router、exit node、serve/funnel、Tailscale SSH）
  - 进阶用法（ACL policy tags/groups、容器/K8s、Headscale、自建 DERP）
  - 生态对比与排错（vs ZeroTier/frp、打洞失败走 DERP、免费版限制、FAQ）
- **预计规模**：P2 素材约 4-6k 字结构笔记，支撑一篇上手+进阶的实战 Obsidian 笔记

---

## 下一步

等待用户选择 P2 深挖方向（1-4，可多选），然后进入 **P2 深度收集**。
