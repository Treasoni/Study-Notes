# 学习笔记大纲：《Tailscale 使用教程》

> 笔记类型：实战笔记
> 学习深度：上手（含进阶用法，以「能用、知道怎么配」为度）
> 用户基础：有了解（已掌握 NAT、P2P/中继、上行带宽等内网穿透概念）
> 预计总篇幅：约 10,000 字（目标 8,000–12,000）
> 章节数：5

---

## 第一章：基础安装与登录

- **篇幅**：约 1,200 字（短）
- **覆盖要点**：Tailscale 是什么（控制面/数据面模型）、tailnet 与账号体系、免费版口径（Personal 6 用户）、各平台客户端安装、`tailscale up` 登录认证、常用 CLI 一览、平台差异（iOS/Android 无 CLI）
- **素材引用**：S01, S02, S12
- **代码示例**：Linux 安装脚本（`curl -fsSL https://tailscale.com/install.sh | sh`）、`sudo tailscale up`、`tailscale down`、`tailscale status`、`tailscale ip -4/-6/-1`、`tailscale up --auth-key=<key>`、`tailscale whoami`

### 1.1 认识 Tailscale 与核心概念
- 控制面/数据面模型，WireGuard 协议一句话定位（端到端加密）
- tailnet 概念；每台设备自动分配唯一 `100.x.y.z` IP，跨网络/防火墙稳定

### 1.2 账号与套餐选择
- 注册两条路径：网页 Get Started，或先装客户端再到 login.tailscale.com/start
- 套餐口径：@gmail.com 等公共邮箱注册进 Personal，免费 **6 用户**；自定义域名自动进 Enterprise 14 天试用
- 设备数上限：以官方 Pricing 页为准（旧「100 设备」说法已废弃，不写入笔记）

### 1.3 各平台安装与登录
- Linux / Windows / macOS 安装与登录；iOS / Android 无 CLI，使用 App 扫码/登录（平台差异）
- 无头/服务器接入推荐：tag 身份 + auth key（`--auth-key`）

### 1.4 常用 CLI 一览
- `status` / `ip` / `down` / `set` / `whoami` / `logout`；`up` 无 flag 即连接认证

---

## 第二章：常用功能实战：MagicDNS、ACL、子网路由与 Exit Node

- **篇幅**：约 2,600 字（长）
- **覆盖要点**：MagicDNS 用名字访问设备、ACL 基础与默认策略、子网路由（subnet router）配置与审批、Exit Node 发布与使用、平台差异易错点（`--accept-routes` 默认值、macOS host/nslookup）
- **素材引用**：S03, S15, S05, S04, S02, S07
- **代码示例**：`tailscale set --accept-dns=false`、sysctl IP forwarding 配置（`/etc/sysctl.d/99-tailscale.conf`）、`sudo tailscale set --advertise-routes=...`、客户端 `--accept-routes`、`tailscale up --advertise-exit-node`、`tailscale up --exit-node=<ip|name> --exit-node-allow-lan-access`、ACL HuJSON 示例（allow-all / 收紧 / `autogroup:internet`）、policy 中 `autoApprovers.exitNode`

### 2.1 MagicDNS：用名字访问设备
- 默认启用；`ping monitoring`、`ssh user@monitoring` 直接用机器名
- FQDN = 机器名 + tailnet DNS 名（如 `monitoring.yak-bebop.ts.net`）
- 易错点：macOS `host`/`nslookup` 绕过系统 DNS 不适用，`ping` 可用
- 单设备禁用：Linux `set --accept-dns=false`；macOS/Windows 在 GUI 关闭

### 2.2 ACL 基础：从默认放行到收紧
- deny-by-default；新建 tailnet 默认 allow all；**无 `acls` 段 = allow all，空对象 `{}` = deny all**
- 每条规则 `action/src/dst`，方向性（允许 src→dst 不等于反向放行）
- 免费版可写范围：目标只能 Any/IP/CIDR/Autogroup/Group/User/Tag/Hosts/IP sets；指定端口与协议是 Premium/Enterprise 专属（易错点）

### 2.3 子网路由 Subnet Router
- 三步走：装客户端 → 开 IP forwarding（sysctl）→ `set --advertise-routes` → admin console 审批（Edit route settings 勾选）→ 客户端 `--accept-routes`
- 易错点：`--accept-routes` 默认值平台差异（Windows/iOS/Android/macOS 默认接受，Linux 等默认不接受）
- `--snat-subnet-routes`（仅 Linux）默认开 SNAT 说明

### 2.4 Exit Node
- 原理：通过默认路由 `0.0.0.0/0`、`::/0` 转发全部公网流量（典型场景：不安全 Wi-Fi、访问仅限本国的服务）
- 发布 + admin 审批 + `autoApprovers.exitNode` 自动批准
- 使用：`--exit-node=<ip|name>`、`--exit-node-allow-lan-access`（默认禁止访问本地 LAN）
- 易错点：自定义 ACL 后必须加 `dst: ["autogroup:internet"]` 才可走出口流量；把 exit node 当 dst 只允许连它，不能当网关

---

## 第三章：端口暴露与 SSH：serve、funnel 与 Tailscale SSH

- **篇幅**：约 2,200 字（中长）
- **覆盖要点**：`tailscale serve`（tailnet 内反代）、`tailscale funnel`（公网暴露）、HTTPS 证书自动签发、Tailscale SSH 免密钥、节点分享（Sharing）
- **素材引用**：S06, S02, S08, S07, S17
- **代码示例**：`tailscale serve --bg 3000`、`tailscale serve status/reset/off`、`tailscale funnel --bg 3000`、`--proxy-protocol=1|2`、`--tls-terminated-tcp=<port>`、`--tcp=<port>`、`tailscale cert <hostname>.<tailnet>.ts.net`、`tailscale set --ssh`、`ssh user@device`、SSH rule JSON（`action`/`src`/`dst`/`users`/`checkPeriod`）、分享链接与 `autogroup:shared` 规则

### 3.1 Tailscale Serve：tailnet 内端口暴露
- v1.52+ 新语法 `tailscale serve [flags] target`；子命令 `status`/`reset`/`off`
- 四种内容模式：HTTP 反代（仅 `http://127.0.0.1` 后端）、文件、目录（绝对路径）、静态文本 `text:"..."`
- HTTPS 仅限 443/8443/10000 三端口；证书自动签发（Let's Encrypt，90 天，`tailscale cert` 需自行续期）
- `--bg` 后台持久，重启自动恢复；`off` 时原命令 flag 必须齐全（易错点）

### 3.2 Tailscale Funnel：公网暴露
- Funnel 公网、Serve 仅 tailnet 内（对比）
- 暴露命令与 flags；`--tls-terminated-tcp` 适用 Caddy/SSH/RDP
- 公网暴露的安全边界提醒（易错点）

### 3.3 Tailscale SSH：免密钥 SSH
- 接管 Tailscale IP 的 22 端口，不碰 `/etc/ssh/sshd_config` 与 authorized_keys；非 Tailscale 流量不受影响
- 启用：`tailscale set --ssh`（每台主机一次）；连接：`ssh device` 或 `ssh user@device`
- **双重放行**：ACL 允许 src→dst 端口 22 + 存在 ssh 规则（易错点）
- ssh 规则语法：`action`（accept/check）、`dst`（只能 tag/`autogroup:self`/单用户，端口固定 22）、`users`（`autogroup:nonroot` 等）、`checkPeriod`（1min–168h，默认 12h，可 `always`）
- 限制：服务端仅 Linux/macOS 开源 tailscaled（v1.24+）；不支持 Synology/QNAP；端口固定 22

### 3.4 节点分享 Sharing
- 只分享单台机器，不暴露 tailnet 其他内容；剥离 tags/groups/subnet 信息
- 邀请链接单次或可复用（≤1000 次，未用 30 天过期）；接受者可用任意 Tailscale 账号
- 被分享机器默认 quarantine：可接受入站，不能主动发起连接；用 `autogroup:shared` 写规则
- 带 tag 的机器不能分享（易错点）

---

## 第四章：生态对比与排错

- **篇幅**：约 1,800 字（中）
- **覆盖要点**：frp / ZeroTier / Tailscale / ngrok 实测对比与选型、打洞机制与 DERP 回退、排错流程（status/ping/netcheck 判别直连 vs 中继）、免费版限制盘点
- **素材引用**：S14, S13, S11, S02, S12
- **代码示例**：`tailscale status`（读 relay code）、`tailscale ping --until-direct` / `--c=<n>`、`tailscale netcheck`、`tailscale bugreport`、iperf3 测速命令参考

### 4.1 四工具实测对比与选型
- 数据（裸金属 1Gbps 公网，iperf3）：frp 320Mbps / ZeroTier 566Mbps / Tailscale 632Mbps / ngrok 71.8Mbps（简表）
- Tailscale 表现最好（632Mbps / 5ms / CPU 5%）；frp 加密+压缩同开会打爆 CPU；ZeroTier 默认 MTU 需改 1500；ngrok 免费版 ≤10 并发
- 选型建议：生产高吞吐 Tailscale/ZeroTier；frp 传统大量端口映射；ngrok 快速调试

### 4.2 打洞机制与 DERP 回退
- 连接默认从 DERP 起步，直连与回退并行探测选最优，成功无缝切直连
- 官方口径：典型环境直连成功率 >90%；状态机是**被动检测**，无超时强切，官方不可调参数（社区「可调超时」观点不采用）
- 打洞失败主因：对称 NAT、多层 NAT、严格防火墙（UniFi 默认拦 UDP）；「沉默失败」原理

### 4.3 排错流程
- `tailscale status` 看 relay code（如 `sea`=西雅图）即走 DERP；无 relay 行即直连
- `tailscale ping`：`via DERP(sea)` = 中继，`via 1.2.3.4:1234` = 直连
- `tailscale netcheck`：UDP false 无法 P2P，回落加密 TCP 中继
- 常见坑：ACL 误配、子网路由未审批、exit node 流量路径、key 过期后 advertised routes fail close

### 4.4 免费版限制盘点
- Personal：单 tailnet **6 免费用户** + node sharing；设备数以 Pricing 页为准
- 端口级 ACL、ssh checkPeriod 检查模式等属付费功能（免费版用 accept 即可）
- Community（开源项目）/慈善/教育折扣路径简介

---

## 第五章：进阶用法

- **篇幅**：约 2,200 字（长）
- **覆盖要点**：Tailnet Policy 进阶（tags/groups/autoApprovers/derpMap）、Headscale 自建控制面、自建 DERP、容器与 Kubernetes 集成
- **素材引用**：S07, S09, S10, S16, S02
- **代码示例**：HuJSON policy（`groups`/`tagOwners`/`autoApprovers`/`derpMap`/`randomizeClientPort`）、`go install tailscale.com/cmd/derper@latest`、`sudo derper --hostname=example.com`、derpMap region 900–999 配置、`--verify-clients`、`cmd/derpprobe`、K8s env（`TS_AUTHKEY`/`TS_ROUTES`/`TS_ACCEPT_DNS=true`）、Headscale 命令参考（`headscale users create`、`headscale nodes register`）

### 5.1 Tailnet Policy 进阶
- `grants` 新一代访问控制（同时管网络层+应用层，deny-by-default）简介；ACL 无限期支持但推荐新配置迁移 grants
- `groups`：`group:` 前缀，成员写完整邮箱，不能嵌套
- `tagOwners`：tag 先定义才能用于 ACL；`[]` 简写 = `autogroup:admin`
- `autoApprovers`：`routes` 与 `exitNode` 两键自动审批；只对首次广播生效，建议用 tag 规避重认证停播
- 网络选项：`derpMap` 自定义/禁用默认 DERP；`randomizeClientPort` 随机端口替代默认 UDP 41641

### 5.2 Headscale：自建控制面
- 开源自托管 Tailscale 控制服务器；职责（交换 WireGuard 公钥、分配 IP、用户边界）；数据面仍走节点间 WireGuard
- 适用边界：窄范围单一 tailnet，面向个人/小型开源组织
- 官方不支持也不鼓励反向代理与容器部署；必须按发布版本选对应 GitHub tag
- 部署命令参考 + 延伸阅读链接（headscale.net/stable，README 未含 DERP 接入细节）

### 5.3 自建 DERP
- alpha 阶段；DERP 是直连失败且无 Peer Relay 时的回退中继；大多数情况无需自建
- 硬性要求：直连公网（不能 NAT/负载均衡）、开放 443（HTTPS/HTTP）+ 3478（STUN）、允许 ICMP
- 部署：`go install tailscale.com/cmd/derper@latest` → `sudo derper --hostname=example.com`
- 接入：policy 写 `derpMap`；region ID **900–999** 保留自定义；每 region 一个 server，冗余用多 region
- 移除默认：region 置 `null` 或 `OmitDefaultRegions: true`；防蹭用 `--verify-clients`（同机跑 tailscaled）；监控用 `cmd/derpprobe`

### 5.4 容器与 Kubernetes
- 四种形态：operator / sidecar / proxy / subnet router；用途：Service ingress、tailnet egress、安全访问 kube-apiserver
- 认证：ephemeral + reusable auth key，放 Secret `TS_AUTHKEY`；无 key 可从容器日志登录 URL 认证
- Subnet router：`TS_ROUTES=10.20.0.0/16,10.42.0.0/15`，admin console 启用 + 客户端 `--accept-routes`
- 易错点：容器默认无 DNS，MagicDNS 需 `TS_ACCEPT_DNS=true`

---

## 学习路径说明

### 前置要求
- 了解 NAT、P2P/中继、上行带宽等内网穿透概念（参考《内网穿透带宽性能分析》）
- 至少一台可安装 Tailscale 的设备（个人电脑/服务器/手机）
- 一个可注册的邮箱账号（建议用公共邮箱注册进 Personal 免费版）

### 学完能做什么
- 在个人设备间组建加密内网，用名字直接访问各设备（MagicDNS）
- 远程访问家里内网设备（subnet router）、在不安全 Wi-Fi 下安全上网（exit node）
- 用 `tailscale serve` / `funnel` 暴露本地服务（tailnet 内 / 公网）并自动签发 HTTPS 证书
- 免密钥 SSH 登录（Tailscale SSH）、把单台设备分享给外部用户（Sharing）
- 遇到打洞失败/走中继能自诊断（status/ping/netcheck），判断是否该调网络或自建 DERP
- 知道进阶能力（policy tags/groups、Headscale、自建 DERP、K8s 集成）的适用场景与基本配置方法

### 建议学习顺序
- 第一章（基础安装与登录）→ 第二章（常用功能实战）→ 第三章（端口暴露与 SSH）→ 第四章（生态对比与排错）→ 第五章（进阶用法）
- 每章实操建议用时：1h / 2h / 1.5h / 1h / 2h（含动手验证）；可先学 1–3 章上手，4–5 章按需选读
