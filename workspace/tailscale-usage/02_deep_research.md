# Tailscale 使用教程 - 深度收集结果 (P2)

> 项目：tailscale-usage
> 收集日期：2026-08-28
> 状态：P2 完成，等待用户确认素材质量后进入 P3 大纲

---

## 1. 范围

用户选择「全部深挖」，覆盖 4 个探索方向：
1. **基础与安装** — 账号体系、登录鉴权、各平台客户端、`tailscale up`
2. **常用功能实战** — MagicDNS、ACL 基础、subnet router、exit node、serve/funnel、Tailscale SSH、节点分享
3. **生态与排错** — vs ZeroTier/frp 选型、打洞失败走 DERP、免费版限制、DERP 排错
4. **进阶用法** — ACL policy（tags/groups/autoApprovers）、Headscale 自建控制面、自建 DERP、容器/K8s

深度：上手（含进阶用法，以「能用、知道怎么配」为度）。用户基础：有了解。

素材规模：**17 篇源**（官方 14 / 深度报告 3），正文缓存于 `.research_cache/`（约 260KB），已按源做 claim-level 抽取。

---

## 2. 源表

| 源 ID | 内容 | 层级 | URL | 缓存文件 |
|-------|------|------|-----|----------|
| S01 | Quickstart 快速入门 | official | https://tailscale.com/docs/how-to/quickstart | 07_tailscale_com.md |
| S02 | CLI 参考（up/down/set/status/ip/ping/netcheck 等） | official | https://tailscale.com/docs/reference/tailscale-cli | 12_tailscale_com.md |
| S03 | MagicDNS | official | https://tailscale.com/docs/features/magicdns | 03_magicdns_tailscale_com.md |
| S04 | Exit nodes | official | https://tailscale.com/docs/features/exit-nodes | 04_tailscale_com.md |
| S05 | Subnet router 配置 | official | https://tailscale.com/docs/features/subnet-routers/how-to/setup | 05_tailscale_com.md |
| S06 | tailscale funnel 命令 | official | https://tailscale.com/docs/reference/tailscale-cli/funnel | 14_tailscale_com.md |
| S07 | Tailnet policy file 语法 | official | https://tailscale.com/docs/reference/syntax/policy-file | 10_tailscale_com.md |
| S08 | Tailscale SSH | official | https://tailscale.com/docs/features/tailscale-ssh | 09_tailscale_com.md |
| S09 | Headscale（自建控制面仓库） | report | https://github.com/juanfont/headscale | 06_github_com.md |
| S10 | 自定义 DERP | official | https://tailscale.com/docs/reference/derp-servers/custom-derp-servers | 08_tailscale_com.md |
| S11 | DERP 路由排错 | official | https://tailscale.com/docs/reference/troubleshooting/network-configuration/derp-routing | 13_tailscale_com.md |
| S12 | 免费套餐与折扣 | official | https://tailscale.com/docs/account/manage-plans/free-plans-discounts | 02_freeplans_tailscale_com.md |
| S13 | UDP 打洞失败检测与中继回退状态机（博客） | report | https://blog.hotdry.top/posts/2026/02/19/tailscale-udp-hole-punching-failure-detection/ | 01_blog_hotdry_top.md |
| S14 | frp vs ZeroTier vs Tailscale vs ngrok 实测对比 | report | https://www.qingyunl.com/news/361.html | 11_www_qingyunl_com.md |
| S15 | ACL 入门 | official | https://tailscale.com/docs/features/access-control/acls | 01_tailscale_com.md |
| S16 | Kubernetes 集成 | official | https://tailscale.com/docs/kubernetes | 02_tailscale_com.md |
| S17 | 节点分享 Sharing | official | https://tailscale.com/docs/features/sharing | 03_tailscale_com.md |

层级分布：official 14 / report 3 / community 0。P1 的 C5 社区排错帖未纳入 P2，其经验已由 S13 博客 + 官方 S11 覆盖。

---

## 3. Claim/Source 映射

### 3.1 基础与安装

- **tailnet 创建两条路径**：网页 Get Started，或先装客户端再到 login.tailscale.com/start 注册；均需 SSO 账号（S01）
- **套餐选择**：自定义域名注册自动进 Enterprise 14 天试用；@gmail.com 等公共邮箱注册进 Personal，免费 6 用户（S01）
- **每台设备自动分配唯一 `100.x.y.z` IP**，跨网络/防火墙稳定（S01）
- **admin console**（console.tailscale.com/admin）集中管理用户、设备、DNS、权限、认证密钥（S01）
- **设备名**：默认取 OS hostname，可在 Machines 页重命名（S01）
- **成员邀请**：自定义域名下同域邮箱免邀请；外部用户用 Users 页 Invite（邮件或链接）（S01）
- **服务器接入推荐**：tag 身份 + auth key，支持 MDM；无头登录用 `--auth-key`（S01, S02）
- **CLI 平台差异**：Linux `tailscale` 已在 $PATH；iOS/Android 无 CLI（S02）
- **`tailscale up` 无 flag 即连接认证**；`down` 断开，重连只需再 `up`（S02）
- **常用子命令**：`status`（5 列：IP/机器名/owner/OS/连接态，含 direct/relay）、`ip`（-4/-6/-1）、`ping`（--until-direct、默认 10 次）、`set`（只改显式项，无默认值）、`netcheck`（诊断物理网络，UDP false 则必走 DERP）、`bugreport`（BUG- 标识符）、`whoami/whois`、`login/logout`、`update`、`wait`（S02）
- **`tailscale set` vs `up`**：up 是「全量设置」，set 只更新显式设置的项，无默认值（S02）
- **免费版 Personal**：单 tailnet 6 免费用户 + node sharing；设备数上限该页未明确（S12）

### 3.2 常用功能实战

- **MagicDNS**：自动注册设备名，`ping monitoring`、`ssh user@monitoring` 即可；所有套餐可用（S03）
  - v1.20+ 无需配置 nameserver；2022-10-20 后新建 tailnet 默认启用（S03）
  - FQDN = 机器名 + tailnet DNS 名，如 `monitoring.yak-bebop.ts.net`；自动加 search domains（S03）
  - macOS `host`/`nslookup` 绕过系统 DNS 不适用；`ping` 可用（S03）
  - 单设备禁用：Linux `set --accept-dns=false`；macOS/Windows 在 GUI 关闭（S03）
  - `*.beta.tailscale.net` 已于 2024-09-13 停用（S03, S17）
- **Subnet router**（S05 + S02）：
  - 步骤：装客户端 → 开 IP forwarding（`/etc/sysctl.d/99-tailscale.conf` 写 `net.ipv4.ip_forward=1`、`net.ipv6.conf.all.forwarding=1`，`sudo sysctl -p` 生效）→ `sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24` → admin console Machines 页审批（Edit route settings 勾选）→ 客户端 `up --accept-routes` 或 `set --accept-routes`
  - `--accept-routes` 默认值有平台差异：Windows/iOS/Android/macOS App Store 与 standalone 版默认接受，其余平台（如 Linux）默认不接受（S02）
  - 审批不通过则不生效；`--snat-subnet-routes`（仅 Linux）默认开 SNAT，子网设备看到流量来自 router（S02）
- **Exit node**（S04 + S02）：
  - 通过默认路由 `0.0.0.0/0`、`::/0` 转发全部公网流量，类似传统 VPN；典型场景不安全 Wi-Fi、访问仅限本国的服务（S04）
  - 发布：客户端 Exit Node → Run as exit node，或 `up --advertise-exit-node`；Admin 审批 Machines 页勾选 Use as exit node；`autoApprovers.exitNode` 可自动批准（S04, S07）
  - 使用：客户端 Exit Nodes 区选出口；`up --exit-node=<ip|name>`；`--exit-node-allow-lan-access` 允许同时访问本地 LAN（默认禁止）（S04, S02）
  - **自定义 ACL 后必须加 `dst: ["autogroup:internet"]` 才可走出口流量**；把 exit node 设备当 dst 只允许连它（如 SSH），不能当网关（S04）
  - 验证：查公网 IP 显示为 exit node 的 IP（S04）；key 过期后 advertised routes fail close，避免流量泄漏（S04）
- **ACL 基础**（S15）：
  - deny-by-default；新建 tailnet 默认策略 allow all；**无 `acls` 段 = allow all，空对象 `{}` = deny all**（S15）
  - 每条规则 `action/src/dst`；方向性——允许 src→dst 不等于反向放行（S15）
  - 规则在设备本地强制执行；编辑入口：admin console / GitOps / API（S15）
  - **免费版可写访问规则但目标只能 Any/IP/CIDR/Autogroup/Group/User/Tag/Hosts/IP sets；指定端口与协议是 Premium/Enterprise 专属**（S15）
- **serve/funnel**（S06）：
  - CLI 自 v1.52 起变更；语法 `tailscale funnel [flags] target`，子命令 `status`/`reset`/`off`（S06）
  - **HTTPS 只允许 443、8443、10000 三端口**；证书自动签发（Let's Encrypt，90 天，`tailscale cert` 需自行续期）（S06, S02）
  - 四种内容模式：HTTP 反代（仅 `http://127.0.0.1` 后端）、文件、目录（绝对路径）、静态文本 `text:"..."`（S06）
  - `--proxy-protocol=1|2` 透传源 IP；`--tls-terminated-tcp=<port>` 转发 TLS 终结后 TCP（适用 Caddy/SSH/RDP）；`--tcp=<port>` 原始 TCP 转发，均限 443/8443/10000（S06）
  - `--bg` 后台持久，重启自动恢复；`off` 时原命令 flag 必须齐全（S06）
  - Funnel 公网暴露，Serve 仅 tailnet 内（S01）
- **Tailscale SSH**（S08）：
  - 接管 Tailscale IP 的 22 端口，不碰 `/etc/ssh/sshd_config` 与 authorized_keys；非 Tailscale 流量不受影响（S08）
  - 启用：`tailscale set --ssh`（每台主机一次）；连接：`ssh device` 或 `ssh user@device`（S08）
  - 需**双重放行**：ACL 允许 src→dst 端口 22 + 存在 ssh 规则（S08）
  - ssh 规则：`action`（accept/check）、`src`、`dst`（只能 tag/`autogroup:self`/单用户，端口固定 22）、`users`（`autogroup:nonroot` 或 `localpart:*@domain`）、`checkPeriod`（1min-168h，默认 12h，可 `always`）、`acceptEnv`（v1.76+，`*`/`?` 通配）（S07, S08）
  - 评估最严格优先：check 先于 accept；撤销用户秒级生效、终止既有连接（S08）
  - 限制：服务端仅 Linux/macOS 开源 tailscaled（v1.24+）；不支持 Synology/QNAP；`tailscaled` 重启终止会话；端口固定 22（S08）
- **节点分享 Sharing**（S17）：
  - beta，v1.4+，所有套餐可用；只分享单台机器，不暴露 tailnet 其他内容；剥离 tags/groups/subnet 信息（S17）
  - 邀请链接单次或可复用（≤1000 次，未用 30 天过期）；接受者可用任意 Tailscale 账号（S17）
  - 被分享机器默认 quarantine：可接受入站，不能主动发起连接（S17）
  - 分享的机器只能用完整域名 `<hostname>.<tailnet>.ts.net` 访问；可用 `autogroup:shared` 写规则限制（S17）
  - 带 tag 的机器不能分享；分享 exit node 需广告+审批+勾选 Allow use as an exit node（S17）

### 3.3 生态与排错

- **四工具实测对比**（S14，裸金属 1Gbps 公网，iperf3）：
  - frp：320Mbps / 12ms / CPU 15%；加密+压缩同开会打爆 CPU，推荐仅加密
  - ZeroTier：566Mbps / 8ms / CPU 8%；默认 MTU 2800 需改 1500；`listpeers` 确认 DIRECT
  - Tailscale：632Mbps / 5ms / CPU 5%（四者最高）；裸金属需 `--accept-routes`；Linux 默认内核态 WireGuard（无内核模块用户态约 -30%）
  - ngrok：71.8Mbps / 20ms+；免费版 ≤10 并发，易 too many connections；只适合 Demo
  - 选型：生产高吞吐 Tailscale/ZeroTier；frp 传统大量端口映射；ngrok 快速调试
- **打洞机制**（S13）：
  - 连接默认从 DERP 起步（交换端点+密钥），直连与回退并行探测选最优；成功即无缝切直连（WireGuard 端到端加密）
  - 官方称典型环境直连成功率 >90%；状态机是**被动检测**而非主动超时，不打洞超时强切，检测到直连立即升级
  - 打洞失败主因：**对称 NAT**（每连接换端口，无法预测）、多层 NAT、严格防火墙（UniFi 默认拦 UDP）
  - 「沉默失败」：UDP 失败无错误响应，靠超时/对端确认判定
  - 缓解：端点独立映射（Endpoint-Independent Mapping）、加大 UDP 会话数、拓扑设计（稳定 UDP 节点/Peer Relay）、关键链路专线或强制 TCP 443
  - 官方未暴露打洞/回退超时参数，不可用户调节（S13）
- **DERP 排错**（S11 + S02）：
  - `tailscale status` 看 relay code（如 `sea`=西雅图）即走 DERP；无 relay 行即直连（direct IP:port）
  - `tailscale ping`：`via DERP(sea) in 242ms` = 中继，`via 1.2.3.4:1234` = 直连；默认最多 10 次（--c 改）；`--until-direct` 默认 true
  - `tailscale netcheck`：UDP false 无法 P2P，回落到加密 TCP 中继；报 Nearest DERP、NAT 映射（UPnP/NAT-PMP/PCP）、HairPinning（S02）
- **免费版限制**（S12）：
  - Personal：单 tailnet **6 免费用户** + node sharing；设备数上限本页未明确
  - GitHub 开源项目（OSI license）可申请 Community 免费版，需 GitHub 认证，不能走 Billing 自助开通
  - 慈善/非营利/教育机构 50% 折扣；Promo 码仅限付费抵扣；套餐管理需 Owner/Admin/Billing admin

### 3.4 进阶用法

- **Policy file 语法**（S07）：
  - HuJSON 书写；顶层分区：`grants`/`acls`/`ssh`/`autoApprovers`/`nodeAttrs`/`postures`/`tagOwners`/`groups`/`hosts`/`ipsets`/`tests`/`sshTests`（S07）
  - **`grants` 是新一代访问控制**（同时管网络层+应用层，deny-by-default）；ACL 无限期支持但不再加新特性，新配置推荐迁移 grants（S07, S15）
  - `groups`：`group:` 前缀，成员写完整邮箱，不能嵌套组，改动自动传播（S07）
  - `tagOwners`：tag 先定义才能用于 ACL；owner 可为邮箱/组/autogroup/tag；`[]` 简写 = `autogroup:admin`（S07）
  - `autoApprovers`：`routes` 与 `exitNode` 两键自动审批；只对首次广播生效，不追溯；设备被他人重认证会停播路由，建议用 tag 规避（S07）
  - 用户引用：`user@example.com`/`user@github`/`user@passkey`；`user:*@domain` 不能用于 gmail 等共享域、不含外部受邀用户（S07）
  - 网络选项：`derpMap` 自定义/禁用默认 DERP；`randomizeClientPort` 用随机端口替代默认静态 UDP 41641（S07）
- **Headscale 自建控制面**（S09）：
  - 开源自托管 Tailscale 控制服务器；Tailscale 除 GUI 客户端与控制服务器外全开源
  - 控制面职责：交换 WireGuard 公钥、分配 IP、用户边界、机器共享、暴露路由；数据面走节点间 WireGuard
  - 设计目标：**窄范围单一 tailnet**，面向个人/小型开源组织
  - 官方不支持也不鼓励反向代理与容器部署；必须按发布版本选对应 GitHub tag；文档分 stable/development 两版
  - README 未含自定义 DERP 接入细节，需查 headscale.net/stable 文档
- **自定义 DERP**（S10）：
  - **alpha 阶段**；DERP 是直连失败且无 Peer Relay 时的回退中继；大多数情况无需自建
  - 硬性要求：**直连公网（不能 NAT/负载均衡）**——DERP 靠源 IP 识别设备，客户端用 HTTP upgrade 建双向通道，云 LB 大多不支持；开放 443（HTTPS/HTTP）+ 3478（STUN）；允许 ICMP
  - 部署：`go install tailscale.com/cmd/derper@latest` → `sudo derper --hostname=example.com`；需域名指向
  - 接入：policy 写 `derpMap`；region ID **900-999** 保留自定义；每 region 一个 server，冗余用多 region
  - 移除默认：region 置 `null` 或 `OmitDefaultRegions: true`；防蹭用 `--verify-clients`（同机跑 tailscaled）；监控用 `cmd/derpprobe`
  - 限制：不支持设备共享/跨 tailnet；不能放防火墙/LB 后；不用于 regional routing
- **Kubernetes 集成**（S16）：
  - 形态：operator / sidecar / proxy / subnet router；用途：Service ingress、tailnet egress、安全访问 kube-apiserver
  - 认证：ephemeral + reusable auth key，放 Secret `TS_AUTHKEY`；无 key 可从容器日志登录 URL 认证
  - v1.16+ 状态存 K8s Secret（需 RBAC）；ephemeral 关机自动移除
  - Sidecar 暴露单 pod 双向连通；userspace sidecar 出站需 SOCKS5/HTTP proxy
  - Subnet router：`TS_ROUTES=10.20.0.0/16,10.42.0.0/15`，admin console 启用 + 客户端 `--accept-routes`
  - **容器默认无 DNS**，MagicDNS 需 `TS_ACCEPT_DNS=true`（S16）

---

## 4. 矛盾点

| # | 冲突 | 处理 |
|---|------|------|
| 1 | **免费版设备数**：P1 曾记「设备不限（旧 100 设备已作废）」；P2 官方免费页缓存只明确「6 用户」，**设备数上限本页未明确** | 笔记写「Personal = 6 免费用户」；设备数标注「以官方 Pricing 页为准」，旧「100 设备」已不出现但新上限待核实 |
| 2 | **默认是否走 DERP**：S14 社区博客称「Tailscale 默认走 DERP、需关候选中继」，与官方 S11/S13「优先直连、DERP 仅回退、超时不可调」冲突 | 以官方为准，社区说法标注为「社区观点」不采用 |
| 3 | **打洞超时/参数**：社区偶传可调，官方明确不可用户调节 | 以官方 S13 为准 |
| 4 | **`--accept-routes` 默认值**：平台间不一致（Windows/iOS/Android/macOS 默认接受，Linux 等不接受） | 笔记单列「平台差异」易错点（S02） |

---

## 5. 实操指引（供写作使用）

- **上手路径**：安装 → `tailscale up` 登录 → `status/ip/ping` → MagicDNS（用名字访问）→ subnet router（访问打印机等）→ exit node（不安全 Wi-Fi 上网）→ ACL 收紧 → Tailscale SSH 免密钥
- **进阶路径**：`tailscale serve/funnel` 暴露服务 → policy tags/groups 多设备管理 → sharing 分享给外部 → Headscale 自建控制面 → 自建 DERP（合规/低延迟）→ K8s operator/sidecar
- **排错流程**：`tailscale status` 看 relay code → `tailscale ping --until-direct` 判别直连/中继 → `tailscale netcheck` 查 NAT/端口映射 → 检查 ACL 与路由审批 → 检查防火墙/UPnP
- **免费版够用边界**：6 用户、无端口级 ACL（需 Premium）、无 checkPeriod 检查模式（SSH 用 accept 即可）、设备数待核实

---

## 6. 未决问题

1. **免费版设备数上限**：官方免费页未明确，需查 Pricing 页或实测（P1 的「设备不限」说法无官方缓存支撑）。
2. **分享节点数量上限**：sharing 文档未给数量限制。
3. **打洞失败的量化缓解数据**：UPnP/固定端口/自建 DERP 的前后对照仅社区零散经验，S13 未含量化；笔记标注为经验值。
4. **Headscale 具体部署步骤**：README 未含 DERP 接入细节，写作时如需深度步骤需查 headscale.net/stable 文档（可作为笔记中的「延伸阅读」链接处理，不阻塞大纲）。

---

## 7. 下游交接

- **推荐大纲结构**（5-6 章）：① 基础安装与登录 ② 常用功能实战（MagicDNS/ACL/subnet router/exit node）③ 端口暴露与 SSH（serve/funnel、Tailscale SSH、分享）④ 生态对比与排错（vs ZeroTier/frp、DERP 排错、免费版限制）⑤ 进阶用法（policy tags/groups、Headscale、自建 DERP、K8s）
- **素材支撑**：每章均有 official 一级源支撑；对比/选型用 S14，排错用 S11/S13，进阶用 S07/S09/S10/S16
- **写作注意**：
  - 免费版口径：6 用户（S12），不要写「100 设备」
  - 命令以 v1.52+ 语法为准（serve/funnel CLI 已变更，S06）
  - 保留「平台差异」标注（--accept-routes、macOS host/nslookup、iOS/Android 无 CLI）
  - 目标 Obsidian：YAML frontmatter、Callout、高价值双链、代码块带语言标识（`.claude/rules/obsidian/note-system.md`）
- **补充缓存**：17 篇源正文在 `workspace/tailscale-usage/.research_cache/`，按需取锚点；不重复抓取。
