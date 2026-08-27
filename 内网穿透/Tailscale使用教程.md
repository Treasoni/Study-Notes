---
title: Tailscale使用教程
tags:
  - 内网穿透
  - Tailscale
  - WireGuard
  - VPN
  - MagicDNS
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: tailscale-usage
---

# Tailscale 使用教程

这篇笔记是「上手级」的 Tailscale 实战指南：假设你已经了解 NAT、P2P/中继、上行带宽等内网穿透概念（可对照同系列笔记 [[内网穿透带宽性能分析]]），目标是看完就能自己把 Tailscale 用起来。正文按「接入 → 常用功能 → 端口暴露与 SSH → 选型排错 → 进阶」五章推进，每章都有可直接照抄的命令示例与「易错点」提醒。第 1–3 章覆盖日常绝大多数场景，第 4–5 章在需要选型、排错或掌控权时按需查阅。

## 目录

1. [[#基础安装与登录|第一章：基础安装与登录]]
2. [[#常用功能实战：MagicDNS、ACL、子网路由与 Exit Node|第二章：常用功能实战：MagicDNS、ACL、子网路由与 Exit Node]]
3. [[#端口暴露与 SSH：serve、funnel 与 Tailscale SSH|第三章：端口暴露与 SSH：serve、funnel 与 Tailscale SSH]]
4. [[#生态对比与排错|第四章：生态对比与排错]]
5. [[#进阶用法|第五章：进阶用法]]

---

## 基础安装与登录

本章解决三个问题：Tailscale 到底是什么、该用什么账号注册、如何把第一台设备装好并登录。学完你就能把一台设备接进 tailnet，并用最基础的 CLI 确认连接状态。动手前建议先回顾 [[内网穿透带宽性能分析]] 里的 NAT、P2P 与中继概念——本章的术语都建立在它们之上。

### 1.1 认识 Tailscale 与核心概念

Tailscale 是基于 WireGuard 构建的组网工具：它把分散在不同网络（NAT、防火墙背后）的设备组合成一个私有虚拟局域网，也就是 **tailnet**。设备加入后就像在同一个局域网里互访，无需配置端口映射或申请公网 IP[^c1-1]。

理解它工作方式的关键是「控制面 / 数据面」分离模型：

- **控制面（coordination plane）**：Tailscale 的控制服务器负责身份认证、交换各设备的 WireGuard 公钥、分配虚拟 IP。它不承载你的业务流量。
- **数据面（data plane）**：设备之间直接建立 WireGuard 加密隧道传输数据；打洞失败时回退到 DERP 中继转发，但流量始终端到端加密[^c1-1]。

> [!tip] 大白话
> 把控制面想成**电话总机**：总机只帮你登记号码、接通线路，不参与你们通话内容；数据面才是你们直接对话的那条线路。所以 Tailscale 服务器挂掉时，已建立的设备间连接往往还能继续走。

> [!note] 核心概念
> **tailnet** 就是「你的虚拟内网」。登录进同一个 tailnet 的设备互相视为同一私网成员，新设备加入后自动获得与成员互通的能力。

每台设备加入 tailnet 时会被自动分配一个唯一的 `100.x.y.z` 虚拟 IP。它与设备所在物理网络无关，跨网络、跨防火墙保持稳定，可当作访问这台设备的固定地址[^c1-1]。

> [!tip] 大白话
> 把 `100.x.y.z` 想成小区的**固定门牌号**：住户今天在哪个城市（物理网络）不影响门牌号。访问设备时直接记这个地址就行，不用管它在哪个公网 IP 后面、端口映射有没有配。

### 1.2 账号与套餐选择

注册有两条等价路径[^c1-1]：

1. 打开官网点 **Get Started**，用 SSO 账号（Google、GitHub、Microsoft 等）登录创建 tailnet；
2. 或先安装客户端，运行登录命令后访问 `login.tailscale.com/start` 完成注册。

> [!warning] 易错点
> 套餐口径：用 `@gmail.com` 等**公共邮箱**注册会进入 **Personal 免费版**，单个 tailnet 免费 **6 个用户**；用**自定义域名**邮箱注册会自动进入 **Enterprise 14 天试用**。想长期用免费版就用公共邮箱[^c1-1][^c1-3]。旧「100 设备」的说法已废弃，设备数上限以官方 Pricing 页为准[^c1-3]。

注册后，`console.tailscale.com/admin`（admin console）是管理入口：管理设备、用户、DNS、ACL 与认证密钥[^c1-1]。设备名默认取操作系统主机名，可在 Machines 页重命名。

### 1.3 各平台安装与登录

Linux / Windows / macOS 的安装方式：

```bash
# Linux（Debian/Ubuntu 等主流发行版），脚本自动添加软件仓库并安装
curl -fsSL https://tailscale.com/install.sh | sh

# 连接并认证
sudo tailscale up
```

运行 `sudo tailscale up` 会打印一个登录链接，浏览器打开并用账号授权即可；`up` 不带任何 flag 就表示「连接并认证」[^c1-2]。Windows / macOS 从官网或应用商店下载客户端，登录同一账号即可。

**iOS / Android 没有 CLI**，只能使用官方 App 扫码或账号登录，登录后设备自动加入 tailnet[^c1-2]。

服务器、树莓派这类无头设备，推荐用 **auth key** 做无交互认证[^c1-1][^c1-2]：

```bash
sudo tailscale up --auth-key=<你的密钥>
```

在 admin console 中生成一次性 auth key，可配合 tag 给设备打上身份标签，方便后续用 ACL 统一管理。断开连接用 `tailscale down`，重连只需再执行一次 `tailscale up`[^c1-2]。

### 1.4 常用 CLI 一览

Linux 安装后 `tailscale` 已在 `$PATH` 中[^c1-2]。最常用的命令：

| 命令 | 作用 |
|------|------|
| `tailscale up` | 连接并认证（无 flag 即完成登录） |
| `tailscale status` | 查看本机与对端状态，5 列：IP、机器名、owner、OS、连接态（direct/relay） |
| `tailscale ip -4` | 显示本机 IPv4（`-6` 为 IPv6，`-1` 只显示本机自身 IP） |
| `tailscale whoami` | 查看当前节点登录的账号身份 |
| `tailscale down` | 断开连接 |
| `tailscale logout` | 注销登录 |
| `tailscale set --xxx` | 只更新显式指定的配置项 |

典型流程（输出为示意）：

```text
$ tailscale status
100.71.200.1  desktop  you@example.com  linux   -
100.71.200.2  nas      you@example.com  linux   direct 192.168.1.10:41641

$ tailscale ip -4
100.71.200.1

$ tailscale whoami
User: you@example.com
Node: desktop
```

`tailscale set` 与 `up` 的区别：`up` 是全量设置，`set` 只修改显式给出的项、不碰其他配置[^c1-2]。本章先用 `up` 把设备连进来，后续章节会用 `set` 做精细调整。

### 本章小结

- Tailscale 采用控制面 / 数据面分离：控制服务器只做协调，业务流量走节点间 WireGuard 加密隧道。
- 每台设备自动获得唯一 `100.x.y.z` IP，跨网络稳定，是访问设备的固定地址。
- 公共邮箱注册进 Personal 免费版（6 用户），自定义域名会进 Enterprise 试用。
- Linux 一键脚本 + `sudo tailscale up` 即可完成安装登录；iOS / Android 无 CLI，用官方 App。
- 常用 CLI：`up` / `status` / `ip` / `whoami` / `down` / `logout` / `set`。

下一章进入实战：用 MagicDNS 用名字直接访问设备、配置子网路由访问家里内网、用 Exit Node 在不安全 Wi-Fi 下安全上网。

### 参考来源

[^c1-1]: Tailscale Quickstart — https://tailscale.com/docs/how-to/quickstart
[^c1-2]: Tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c1-3]: Free pricing plans — https://tailscale.com/docs/account/manage-plans/free-plans-discounts

---

接入只是第一步。接下来这一章把 tailnet 从「能连通」推向「日常好用」。

## 常用功能实战：MagicDNS、ACL、子网路由与 Exit Node

上一章我们把设备装好客户端、登录进 tailnet，每台设备都拿到了固定的 `100.x.y.z` 内网地址。但裸 IP 不好记，默认的"全放行"策略在设备变多时也不安全。这一章把四个日常最高频的能力一次讲透：用名字访问设备（MagicDNS）、控制谁到谁的访问（ACL）、把整个局域网带进 tailnet（子网路由）、借一台设备的公网出口上网（Exit Node）。掌握这四件事，你就能解决远程访问 80% 的日常场景；对 NAT、P2P 打洞这些底层机制还有疑问的话，可以随时翻一下 [[内网穿透带宽性能分析]]。

### 2.1 MagicDNS：用名字访问设备

Tailscale 会给每台设备自动注册一个"内网域名"，这就是 MagicDNS。默认启用，不需要任何配置——新创建的 tailnet 在 2022-10-20 之后默认开启，客户端 v1.20+ 也无需手动配置 nameserver[^c2-1]。开启后你可以直接用机器名访问：

```bash
$ ping monitoring                # 不需要记 100.101.102.103
PING monitoring (100.101.102.103): 56 data bytes

$ ssh user@monitoring            # 同样适用
```

MagicDNS 的完整域名（FQDN）由**机器名 + tailnet DNS 名**组成，例如 `monitoring.yak-bebop.ts.net`；tailnet 会自动给设备追加 search domain，所以短名字 `monitoring` 就能解析[^c2-1]。

> [!tip] 大白话：MagicDNS 就是 tailnet 内部的"通讯录"
> 把 MagicDNS 想成小区物业自动维护的通讯录：每台设备入网时自动登记"姓名→房号（100.x）"的对应关系，还帮你把门牌号后缀补全。所以你不必背 100.101.102.103 这种门牌号，喊一声 `monitoring` 就能找到对方。

如果你在某台设备上不想用 MagicDNS（比如它本身要跑自己的 DNS），可以只在这台设备上关掉：

```bash
sudo tailscale set --accept-dns=false     # 关闭后只影响本机
sudo tailscale set --accept-dns=true      # 重新开启
```

macOS / Windows 没有对应 CLI 开关，需要在客户端 GUI 的 DNS 设置里关闭[^c2-1]。

> [!warning] macOS 易错点：`host` / `nslookup` 不适用
> macOS 上 `host monitoring` 和 `nslookup monitoring` 会绕过系统 DNS 直查公网 DNS，解析不出 tailnet 内部名字；但 `ping`、`ssh` 走系统解析，所以能用。判断 MagicDNS 是否生效，请用 `ping` 或 `dscacheutil -q host -a name monitoring`，别被 `host`/`nslookup` 的结果误导[^c2-1]。

另外提醒：早期教程里的 `*.beta.tailscale.net` 域名后缀已于 2024-09-13 停用，现在统一是 `*.ts.net`，照旧教程排错时别被带偏[^c2-1]。

### 2.2 ACL 基础：从默认放行到收紧

ACL（Access Control List）决定 tailnet 里**谁（src）能访问谁（dst）**。Tailscale 的安全原则是 deny-by-default，但**新建的 tailnet 默认策略却是全放行**，所以别以为"能用 = 已经安全"[^c2-2]。

> [!tip] 大白话：ACL 就是一张授权清单
> 把 ACL 想成大楼门禁的授权表：每行写"某人 → 能进某房间"。默认情况下这栋楼不设防（allow all）；你在清单里写了任何一条规则后，没写到的组合就默认进不去。所以加规则 = 开始"上锁"。

关键心法（三个坑一次记牢）：

- **无 `acls` 段 = allow all，空对象 `{}` = deny all**。如果你在 Admin Console 里打开 Access Controls，看见的是一个 `{}` 空对象——这是 deny all，不是默认放行！新建 tailnet 的默认放行来自"存在一条隐式的全放行规则"，一旦你保存了自己的 `acls` 段，就按你写的来[^c2-2]。
- **规则有方向性**：允许 `laptop → server` 不等于 `server → laptop` 也能通，反向访问要单独再写一条[^c2-2]。
- **免费版不能写端口级规则**：目标只能写 Any（`*`）、IP、CIDR、Autogroup、Group、User、Tag、Hosts、IP sets；`dst` 里带 `:端口` / `:协议` 属于 Premium/Enterprise 专属功能[^c2-2]。

全放行（等价于新建 tailnet 的默认行为）：

```json
{
  "acls": [
    { "action": "accept", "src": ["*"], "dst": ["*:*"] }
  ]
}
```

收紧——只允许 `alice@example.com` 访问 `monitoring`，其余全部拒绝：

```json
{
  "acls": [
    { "action": "accept", "src": ["alice@example.com"], "dst": ["monitoring"] }
  ]
}
```

> [!warning] 免费版易错点：`dst` 别写端口段
> 免费版写规则时，`dst` 写成 `"monitoring"`、`"100.101.102.103"` 或 `"*"` 即可，等价于放行该目标的全部端口；`":22"`、`":tcp"` 这类端口/协议写法是 Premium/Enterprise 才支持。你在免费版里写了端口段，规则要么不生效要么报错，先用无端口写法。

ACL 由 tailnet 内每台设备本地强制执行（不依赖中心代理），编辑入口在 Admin Console，也可走 GitOps / API[^c2-2]。规则配错最常见的症状是：`tailscale ping` 能通、但访问具体服务超时——先查 ACL 是不是把端口写死了。

### 2.3 子网路由 Subnet Router

场景：家里一台 Raspberry Pi 连着打印机、路由器管理页，你在公司想直接访问它们。它们装不了 Tailscale？没问题——让 Pi 当**子网路由器（subnet router）**，把整个局域网"代理"进 tailnet。核心三步 + 两步收尾[^c2-3]：

**第一步，在路由设备上开启 IP 转发。** 因为流量要在一个网卡（Tailscale 虚拟网卡）和另一个网卡（局域网口）之间转发：

```bash
# /etc/sysctl.d/99-tailscale.conf
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

```bash
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

**第二步，广播你要代理的网段**（把示例网段换成你家路由器实际的局域网网段，如 `192.168.1.0/24`）：

```bash
sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24
```

**第三步，去 Admin Console 审批**：Machines 页 → 点对应设备 → Edit route settings → 勾选要批准的 route → Save。**审批不通过，路由就不生效**，这是配完"看起来对但访问不了"的高频原因[^c2-3]。

**第四步，在客户端接受路由**：

```bash
sudo tailscale set --accept-routes
```

> [!warning] 平台差异：`--accept-routes` 默认值不一致
> Windows、iOS、Android、macOS（App Store 与 standalone 版）默认就接受子网路由；**但 Linux 等其余平台默认不接受**。所以在 Linux 客户端上，`--accept-routes` 这一步不能省——多数"我明明审批了为什么访问不了子网"的问题就出在这[^c2-5]。

**关于 SNAT**：`--snat-subnet-routes` 是仅 Linux 可用的 flag，默认开启。开启后，子网里的普通设备看到的连接来源是路由器的 Tailscale IP（`100.x`），而不是你设备的 IP；好处是子网内设备零配置就能回包，代价是丢了真实来源 IP。只有需要保留源 IP 的场景才关掉它[^c2-5]。

### 2.4 Exit Node

Exit Node 是"整台设备当网关"：它把你的默认路由（`0.0.0.0/0` 和 `::/0`）接过来，**所有公网流量先加密到这台设备，再由它的公网 IP 发出去**，效果类似传统 VPN[^c2-4]。典型场景：公共 Wi-Fi 防窃听、访问只对特定国家/地区开放的服务、隐藏自己设备的公网 IP。

> [!tip] 大白话：Exit Node 就是替你出门办事的门卫
> 你的所有"出门"请求（访问公网）不再自己直接出去，而是先加密送到门卫（exit node），由门卫用他自己的门禁卡（公网 IP）替你出去。所以别人看到的是门卫的地址，不是你的；在公共 Wi-Fi 这种"坏小区"里特别安全。

**发布（在当出口的设备上）**：

```bash
sudo tailscale up --advertise-exit-node
```

GUI 客户端则在 Settings → Exit Node 里勾选 Run as exit node[^c2-4]。

**审批**：Admin Console → Machines 页 → 勾选该设备 Use as exit node。想省去手动审批，可以在 policy file 里加 `autoApprovers.exitNode` 自动批准指定用户发布的出口[^c2-4][^c2-6]：

```json
{
  "autoApprovers": {
    "exitNode": ["user@example.com"]
  }
}
```

**使用（在任意客户端上）**：

```bash
sudo tailscale set --exit-node=<ip或机器名> --exit-node-allow-lan-access
```

- `--exit-node=<ip|name>`：指定出口，可以是 `100.x` IP 或机器名[^c2-5]。
- `--exit-node-allow-lan-access`：默认**禁止**在走出口的同时访问本地 LAN。开了 exit node 后发现打不开自家打印机/路由器管理页，就是这个 flag 没加[^c2-5]。

**验证**：走出口后查公网 IP，应显示为出口设备的公网 IP：

```bash
$ curl ifconfig.me
203.0.113.9
```

> [!warning] Exit Node 与 ACL 的两个坑
> 1. **自定义 ACL 后必须放行 `autogroup:internet`**：一旦你写过自己的 `acls`，客户端就无法把 exit node 当网关转发公网流量，除非显式加一条规则：
>    ```json
>    { "action": "accept", "src": ["alice@example.com"], "dst": ["autogroup:internet"] }
>    ```
> 2. **把 exit node 设备写进 `dst` 只表示"能连到它"，不表示"能把它当网关"**。例如 `dst: ["100.66.5.2"]` 只是允许你 SSH 到那台设备；要走它的公网出口，必须用上面 `autogroup:internet` 那条[^c2-4]。

最后一条安全兜底：作为出口的那台设备 key 过期时，tailnet 会 fail close——宁可断流也不会把流量悄悄改走其他路径，避免流量泄漏。这也是 exit node 比随手搭的代理更可信的原因[^c2-4]。

### 本章小结

- MagicDNS 让 tailnet 内直接用机器名访问，FQDN = 机器名 + tailnet DNS 名；Linux 用 `set --accept-dns` 控制开关，macOS 上 `host`/`nslookup` 不适用但 `ping` 可以。
- ACL 默认全放行：无 `acls` 段 = allow all，空对象 `{}` = deny all；规则严格有方向性；免费版不能写端口级规则。
- 子网路由 = 三步走（开 IP forwarding → `set --advertise-routes` → 审批）+ 客户端 `set --accept-routes`；`--accept-routes` 在 Linux 上默认关闭，最容易漏。
- Exit Node 通过 `0.0.0.0/0`、`::/0` 转发全部公网流量；自定义 ACL 后必须放行 `autogroup:internet`，把出口当 `dst` 并不等于能当网关。

下一章我们把方向反过来：用 `tailscale serve` 把本机端口暴露给 tailnet、用 `tailscale funnel` 暴露到公网并自动签发 HTTPS 证书，再加免密钥的 Tailscale SSH 与单机分享——远程访问的"输入"和"输出"就都齐了。

### 参考来源

[^c2-1]: MagicDNS — https://tailscale.com/docs/features/magicdns
[^c2-2]: ACLs 入门 — https://tailscale.com/docs/features/access-control/acls
[^c2-3]: Configure a subnet router — https://tailscale.com/docs/features/subnet-routers/how-to/setup
[^c2-4]: Exit nodes — https://tailscale.com/docs/features/exit-nodes
[^c2-5]: Tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c2-6]: Tailnet policy file — https://tailscale.com/docs/reference/syntax/policy-file

---

设备互访解决之后，轮到「服务暴露」这一侧。

## 端口暴露与 SSH：serve、funnel 与 Tailscale SSH

前两章解决的是「设备之间互访」：登录、用名字 ping、走子网路由访问内网设备、用 exit node 上网。但还有一类高频需求没解决——**我跑了一个 Web 服务，怎么把它安全地暴露出去**？这一章讲 Tailscale 的端口暴露三板斧：`serve`（只给 tailnet 内成员访问）、`funnel`（对公网开放）、HTTPS 证书自动签发，再顺手把免密钥的 Tailscale SSH 和「把单台机器分享给外部用户」的 Sharing 一起讲掉。全程不用碰路由器、不用手动配证书，命令基本就是一条 `tailscale xxx`。

> 端口暴露本质上是在内网和外部之间「开一个门」，这扇门的带宽上限取决于出口上行，相关结论可以参考 [[内网穿透带宽性能分析]]。

### 3.1 Tailscale Serve：tailnet 内端口暴露

`tailscale serve` 把本机某个端口上的服务挂到你的 tailnet 域名下，只允许 tailnet 内成员通过 HTTPS 访问。典型场景：家里的 NAS 面板、开发环境的前端页面、内网监控面板——只给自己人看，不打算让公网碰。

> [!tip] 大白话：把 serve 想成在办公楼里给自家服务开了一个「前台窗口」。访客（tailnet 成员）要刷工牌才能进楼，窗口背后的服务还待在原来的工位上（本地 3000 端口），只是多了一个体面的正门。所以：serve 只对本楼（tailnet）开放，楼外的人看不见它。

v1.52 起 serve 的 CLI 改成新语法 `tailscale serve [flags] target`，下面直接上手。假设你已经在本地跑了一个服务：

```bash
# 目标设备（服务所在机器）终端
# 第一步：先启动一个本地服务，比如 Python 静态服务器
# --bind 127.0.0.1 保证它只监听本机，不直接暴露到局域网
python3 -m http.server 3000 --bind 127.0.0.1

# 第二步：新开一个终端，把它挂到 tailnet 上
# --bg 表示后台持久运行，tailscaled 重启后会自动恢复，不用再敲一次
tailscale serve --bg 3000
```

执行后没有报错就说明已生效。用子命令管理：

```bash
tailscale serve status    # 查看这台设备当前暴露了哪些内容
tailscale serve reset     # 清空这台设备所有 serve 配置
tailscale serve off       # 关闭 serve
```

`status` 的输出长这样，`tailnet only` 表示只有内网成员能访问：

```text
http://monitoring.yak-bebop.ts.net (tailnet only)
|-- http://127.0.0.1:3000
```

几个必须知道的限制：

- **HTTPS 端口只有 443、8443、10000 三个**，不能随便指定，默认走 443。
- 证书由 Let's Encrypt 自动签发（90 天有效），serve/funnel 托管时不需要你管续期；如果要手动签发证书（比如部署到别处），用 `tailscale cert <hostname>.<tailnet>.ts.net`，此时 90 天后需自行续期。[^c3-1][^c3-2]
- 除了 HTTP 反代，serve 还支持三种内容模式：**文件**、**目录**（写绝对路径）、**静态文本**（直接返回 `text:"..."`）。最常用的是 HTTP 反代，后端地址只能是 `http://127.0.0.1`，不会转发到局域网里的其它主机。[^c3-2]

> [!warning] 易错点：`tailscale serve off` 关闭时，**启动时用过的 flag 必须原样补全**，缺了会报错。比如你用 `tailscale serve --bg 3000` 启动，关的时候要写 `tailscale serve --bg off`，不能只敲 `tailscale serve off`。[^c3-2]

### 3.2 Tailscale Funnel：公网暴露

如果说 serve 是「楼内前台」，`funnel` 就是直接在临街开的铺面——**任何人都能访问**，不需要在你的 tailnet 里。两者的关系一句话：Serve 只给 tailnet 内，Funnel 给全世界。

```bash
# 目标设备终端
# 把 3000 端口直接暴露到公网（同样支持 --bg 后台持久）
tailscale funnel --bg 3000
```

```text
https://monitoring.yak-bebop.ts.net (Funnel)
|-- http://127.0.0.1:3000
```

Funnel 和 Serve 共用同一套 HTTPS 端口限制（443/8443/10000）和证书自动签发机制，区别只在「谁能访问」——`status` 输出里会明确标出 Funnel。想要「只有 tailnet 内能访问」用 serve，想要「公网也能打开」用 funnel，选错的话暴露范围会差一个数量级。[^c3-1]

需要透传真实客户端 IP 或处理非 HTTP 流量时，serve/funnel 都支持几个高级 flag：

```bash
# 让后端拿到真实客户端 IP（PROXY protocol v1 或 v2）
tailscale serve --bg --proxy-protocol=1 3000

# 后端自己处理 TLS（比如 Caddy 反代、SSH、RDP 这类场景），
# Tailscale 不做 TLS 卸载，只把原始 TCP 流转发到后端的 443 端口
tailscale funnel --bg --tls-terminated-tcp=443 443

# 原始 TCP 转发（同样只限 443/8443/10000 三个端口）
tailscale funnel --bg --tcp=10000 10000
```

> [!warning] 安全边界：Funnel 是**公网暴露**，等于把服务直接挂到互联网上。它只负责开「入口」，不帮你做鉴权——登录、限流、防扫描都得靠服务自己。开 Funnel 前先想清楚：这个服务真的需要全世界访问吗？多数场景其实 serve 就够了；如果只是临时给某人看，用 3.4 的 Sharing 更安全。

### 3.3 Tailscale SSH：免密钥 SSH

传统 SSH 要管理公钥、往每台机器写 `authorized_keys`。Tailscale SSH 直接**接管 Tailscale IP 上的 22 端口**，由 Tailscale 控制面统一认证身份，不碰你本机的 `/etc/ssh/sshd_config` 和 `authorized_keys`；局域网或公网来的普通 SSH 流量走原路径，不受影响。[^c3-3]

> [!tip] 大白话：把 Tailscale SSH 想成「把钥匙交给物业管家」。以前你要自己配门锁、给每个人配钥匙（authorized_keys、私钥），现在管家（Tailscale 控制面）统一刷卡认证——只要对方在 tailnet 里、ACL 允许，直接 `ssh user@device` 就进去了，不用再交换公钥。

启用分两步：

```bash
# 被登录的那台机器上执行
# 第一步：开启 Tailscale SSH（每台主机只需一次）
tailscale set --ssh

# 第二步：从另一台 tailnet 内设备连接，直接写 MagicDNS 机器名
ssh user@device
# 或写完整 FQDN
ssh user@device.yak-bebop.ts.net
```

> [!warning] 易错点——双重放行：光执行 `tailscale set --ssh` 还不够，要连得上必须同时满足两件事：① ACL 里有一条规则允许 src→dst 的**端口 22** 流量；② policy 里存在一条 **ssh 规则**。两者缺一不可。新建 tailnet 的默认 allow-all 恰好同时满足，所以一般感觉不到；但只要你收紧过 ACL，就会遇到「set --ssh 开了还是连不上」的诡异情况。[^c3-3][^c3-4]

ssh 规则写在 policy 文件顶层的 `ssh` 段。先看一个完整例子（先睹为快），再逐字段拆：

```json
// policy.hujson（tailnet policy 文件的 ssh 段）
{
  "ssh": [
    {
      "action": "accept",
      "src":    ["autogroup:member"],
      "dst":    ["tag:server"],
      "users":  ["autogroup:nonroot"]
    }
  ]
}
```

- `action`：`accept`（直接放行）或 `check`（二次确认模式）。
- `src`：发起方，可以是用户、组、tag 或 autogroup。
- `dst`：目标机器，**只能写 tag、`autogroup:self` 或单个用户，端口固定为 22，不能改**。
- `users`：目标机器上允许登录的系统用户，常用 `autogroup:nonroot`（所有非 root 用户），也可以写 `localpart:*@domain`。[^c3-4]

如果希望登录前做二次确认，用 `check` 模式，加 `checkPeriod` 控制确认频率：

```json
// policy.hujson（check 模式示例）
{
  "ssh": [
    {
      "action": "check",
      "src":    ["autogroup:member"],
      "dst":    ["tag:server"],
      "users":  ["autogroup:nonroot"],
      "checkPeriod": "2h"
    }
  ]
}
```

- `checkPeriod` 范围 1min–168h（1 分钟到 7 天），默认 12h，设为 `always` 则每次连接都要重新确认。[^c3-4]
- 多条规则同时命中时**最严格的优先**：`check` 先于 `accept` 生效；撤销某个用户后**秒级生效**，会直接终止其已建立的连接。[^c3-3]
- 注意 `check`（二次确认）模式属付费功能，免费版直接用 `accept` 即可。

限制也要知道：Tailscale SSH 服务端只支持 **Linux / macOS** 的开源 tailscaled（v1.24+），Synology、QNAP 等 NAS 不支持；端口固定 22；`tailscaled` 重启会终止现有 SSH 会话。[^c3-3]

### 3.4 节点分享 Sharing

Sharing 解决另一个问题：**把一台机器临时分享给 tailnet 之外的人**，比如让外部顾问 SSH 到一台服务器。它只分享这一台机器，不暴露你 tailnet 的任何其它内容；分享时会剥离这台机器的 tags、groups、subnet router 等身份信息，对方看到的只是一台「孤立的机器」。[^c3-5]

操作在 admin console 的 Machines 页完成：找到目标机器 → 分享（Share）→ 生成邀请链接发给对方。链接分两种：[^c3-5]

- **单次链接**：一个人用一次就失效；
- **可复用链接**：最多可用 1000 次，且 30 天未被使用会过期。

对方收到链接后，用**任意 Tailscale 账号**登录接受即可，不需要加入你的 tailnet。

几个必须记住的规则：

- 被分享的机器默认 **quarantine（隔离）**：对方可以连进来（入站），但**不能以它为跳板主动发起连接**（出站），避免「分享一台机器 = 给你内网开了个口子」。[^c3-5]
- 对方访问这台机器时**只能用完整域名 `<hostname>.<tailnet>.ts.net`**，不能用短机器名。[^c3-5]
- **带 tag 的机器不能分享**。如果这台机器打了 tag，得先去掉 tag 才能分享。[^c3-5]
- 分享 exit node 需要额外广告路由 + 审批 + 勾选 "Allow use as an exit node"。[^c3-5]
- 这是 beta 功能（v1.4+），所有套餐可用。

如果你想统一限制「被分享进来的外部用户」能访问什么，在 ACL 里用 `autogroup:shared` 指向这群人：

```json
// policy.hujson（ACL 示例）
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:shared"],
      "dst": ["<hostname>.<tailnet>.ts.net"]
    }
  ]
}
```

这样就把外部用户的访问范围收在可控的几台机器内，而不是默认放行。[^c3-5]

### 本章小结

- `serve` 把本地服务只暴露给 tailnet 内成员，`funnel` 对公网开放，两者共用 HTTPS 三端口（443/8443/10000）和 Let's Encrypt 自动签发证书。
- v1.52+ 语法是 `tailscale serve/funnel [flags] target`，管理用 `status` / `reset` / `off`；`--bg` 后台持久，`off` 时 flag 必须补全。
- 高级转发：`--proxy-protocol=1|2` 透传源 IP，`--tls-terminated-tcp=<port>` 适合 Caddy/SSH/RDP，`--tcp=<port>` 做原始 TCP 转发。
- Tailscale SSH 免密钥登录要记住「双重放行」：ACL 端口 22 + ssh 规则缺一不可；ssh 规则 `dst` 只能写 tag/`autogroup:self`/单用户，端口固定 22，`checkPeriod` 默认 12h。
- Sharing 只分享单台机器，对方只能以完整域名访问且默认 quarantine；带 tag 的机器不能分享。

下一章我们从「怎么配」切换到「怎么选、怎么修」：frp / ZeroTier / ngrok 与 Tailscale 的实测对比，以及打洞失败走 DERP 时，如何用 `status` / `ping` / `netcheck` 一步步定位问题。

### 参考来源

[^c3-1]: Tailscale Funnel 命令参考 — https://tailscale.com/docs/reference/tailscale-cli/funnel
[^c3-2]: Tailscale CLI 参考 — https://tailscale.com/docs/reference/tailscale-cli
[^c3-3]: Tailscale SSH — https://tailscale.com/docs/features/tailscale-ssh
[^c3-4]: Tailnet policy file 语法 — https://tailscale.com/docs/reference/syntax/policy-file
[^c3-5]: 节点分享 Sharing — https://tailscale.com/docs/features/sharing

---

配通之后，还需要会选、会修。

## 生态对比与排错

功能都配通了，接下来三个问题绕不开：Tailscale 跟 frp、ZeroTier、ngrok 比到底快多少？直连打洞失败时会怎样？出了问题怎么定位？本章先给出一组实测数据回答「怎么选」，再讲清打洞与 DERP 回退的机制，接着给一套可直接照做的排错流程，最后盘点免费版限制。

### 4.1 四工具实测对比与选型

以下数据来自**单一测试环境**（裸金属 1Gbps 公网、iperf3 测速）的实测[^c4-1]，仅作选型参考：

| 工具 | 实测带宽 | 延迟 | CPU 占用 | 关键限制与备注 |
|---|---|---|---|---|
| frp | 320 Mbps | 12ms | 15% | 加密+压缩同开会打爆 CPU，建议仅加密 |
| ZeroTier | 566 Mbps | 8ms | 8% | 默认 MTU 2800 需改 1500 |
| Tailscale | 632 Mbps | 5ms | 5% | 裸金属需 `--accept-routes` |
| ngrok | 71.8 Mbps | 20ms+ | — | 免费版 ≤10 并发，易触发 too many connections |

> [!warning] 单一测试环境，结论只作选型参考
> 这是同一台裸金属服务器、同一网络的单次实测[^c4-1]，数值会随网络、设备与版本变化。真正选型时，最好在自己的链路上用同样的方法各跑一遍。

几点值得注意：frp 在加密与压缩同时开启时 CPU 飙到 15%，实测建议**只开加密**；ZeroTier 默认 MTU 2800 在多数公网链路会被分片拖慢，要改成 1500（改完用 `zerotier-cli listpeers` 确认 `DIRECT`）；Tailscale 是四者中**综合表现最高**的——632Mbps 带宽、5ms 延迟，CPU 占用反而最低（5%），Linux 上默认走内核态 WireGuard，若内核模块不可用而退回用户态实现，性能约降 30%[^c4-1]。带宽与吞吐的影响因素可参考 [[内网穿透带宽性能分析]]。

选型建议[^c4-1]：

- **生产高吞吐** → Tailscale 或 ZeroTier，两者 P2P 直连，吞吐远高于中继方案；
- **传统大量端口映射** → frp，思路直观、控制力强；
- **快速调试/临时暴露** → ngrok，零配置开箱即用，但免费版并发与带宽都受限。

想自己复测，iperf3 命令参考（对端为 tailnet 内设备）：

```bash
# 对端（服务器）启动服务端
iperf3 -s

# 本机发起测速，-t 指定时长
iperf3 -c 100.x.y.z -t 30
```

### 4.2 打洞机制与 DERP 回退

Tailscale 并不保证一上来就是直连。连接建立时，节点**默认从 DERP 中继起步**——先用它交换对端端点与 WireGuard 公钥，同时并行探测直连路径，两条路径选最优；一旦打洞成功，就**无缝切换为直连**，后续流量走端到端加密的 WireGuard，中继不再参与[^c4-2]。

> [!note] 直连优先，DERP 仅回退
> 官方口径是「优先直连、DERP 仅回退」[^c4-2]。看到 `relay "sea"` 不代表系统「偏爱」中继，只是此刻直连还没成功或已失败。典型环境下官方称直连成功率超过 90%[^c4-2]。

> [!tip] 大白话：直连 vs 中继
> 把直连打洞想成「两户人家窗户对窗户，喊话直达」；DERP 中继想成「楼道里站个传话人」。能直达就直达，传话人只在喊不通时兜底——所以看到 `relay "sea"` 不是故障，只是暂时没人能直达而已。

这里有个易误解点：打洞与回退的状态机是**被动检测**，不是「等一个超时就强制切换」[^c4-2]。系统持续观察路径质量，检测到更优的直连就立即升级，不会主动打断当前连接。官方**没有暴露任何「打洞/回退超时」参数，不可用户调节**；社区偶有「可调超时」的说法，以官方口径为准，不采用[^c4-2]。

打洞失败主要有三类原因[^c4-2]：

- **对称 NAT**：每次连接都换出站端口，无法预测，最难穿透；
- **多层 NAT**：家庭路由器叠加运营商 NAT，端点映射层层嵌套；
- **严格防火墙**：如 UniFi 默认拦截 UDP，直接断掉打洞通道。

> [!warning] UDP 失败是「沉默」的
> UDP 打洞失败**不会有任何错误报文返回**，系统只能靠超时或对端确认来判定失败[^c4-2]。排查时别干等报错——走了中继不代表故障，可能只是打不通直连。

缓解思路：尽量用支持端点独立映射（Endpoint-Independent Mapping）的路由器、加大 UDP 会话数上限、在拓扑中保留一个稳定 UDP 节点或 Peer Relay，关键链路直接走专线或强制 TCP 443[^c4-2]。

### 4.3 排错流程

遇到「设备在线却连不上 / 访问很慢」，按下面四步定位[^c4-3][^c4-4]。

**第一步：`tailscale status` 看走没走中继**

```bash
tailscale status
```

设备状态列若出现 `relay "sea"`，说明流量正经过 DERP（`sea` 是西雅图中继的代码）；没有 relay 行、状态列为 direct 的才是直连[^c4-3]。

```text
# 示意：第 5 列 relay "sea" = 走中继；"-" = 直连
100.101.102.103  device-a   user@   linux    -
100.101.102.104  device-b   user@   windows  relay "sea"
```

**第二步：`tailscale ping` 判别直连还是中继**

```bash
tailscale ping --until-direct device-b   # 直连成功后立即停止（默认 true）
tailscale ping --c=5 device-b            # 只探测 5 次（默认最多 10 次）
```

输出 `via DERP(sea) in 242ms` = 中继；`via 1.2.3.4:1234 in 8ms` = 已打通直连[^c4-3]。

**第三步：`tailscale netcheck` 检查底层网络**

```bash
tailscale netcheck
```

重点看 UDP 一栏：若为 `false`，说明当前网络**无法 P2P 打洞**，流量只能回落加密 TCP 中继；同时该命令会报告最近的 DERP、NAT 映射方式（UPnP / NAT-PMP / PCP）与 HairPinning 支持情况[^c4-4]。

**第四步：对照常见坑检查**

- **ACL 误配**：规则只允许 A→B，反向未放行；
- **子网路由未审批**：`--advertise-routes` 广播了，但 admin console 没勾选审批；
- **exit node 流量路径**：自定义 ACL 后忘记加 `dst: ["autogroup:internet"]`；
- **key 过期**：认证密钥过期后 advertised routes 会 fail close，宁可断流量也不泄漏[^c4-3]。

仍定位不了，用 `tailscale bugreport` 生成一份带 `BUG-` 标识符的诊断包，发给官方或社区[^c4-4]。

### 4.4 免费版限制盘点

免费版 Personal 的关键边界[^c4-5]：

- **单 tailnet 最多 6 个免费用户**，支持节点分享（node sharing）；
- 设备数上限官方免费页未写死，**以 Pricing 页为准**——旧「100 设备」的说法已废弃，不要信。

付费专属能力（免费版用替代方案即可）[^c4-5]：

- **端口级 ACL**：免费版 ACL 目标只能写 Any / IP / CIDR / Group / User / Tag 等粒度，指定端口与协议是 Premium/Enterprise 专属；
- **ssh 检查模式（checkPeriod）**：免费版 SSH 规则用 `accept` 放行即可，周期性校验是付费功能。

> [!tip] 免费版够用判断
> 个人 6 用户以内、不需要按端口精细授权、SSH 不需要「每次检查」——免费版基本够用，不必急着升级。

另有两条折扣/免费路径[^c4-5]：符合 OSI 协议的开源项目可申请 **Community 免费版**（需 GitHub 认证，不能走 Billing 自助开通）；慈善、非营利与教育机构可享 **50% 折扣**。

### 本章小结

- 四工具实测（单一环境）：Tailscale 综合表现最高（带宽最大、CPU 最低）；frp 适合大量端口映射、ngrok 适合快速调试。
- Tailscale 连接默认从 DERP 起步，并行探测直连，成功即无缝切换；状态机是被动检测，超时参数不可调。
- 打洞失败主因是对称 NAT、多层 NAT 与严格防火墙；UDP 失败「沉默」，只能靠超时判定。
- 排错四步：`status` 看 relay code → `ping` 判别直连/中继 → `netcheck` 查 UDP/NAT → 核对 ACL、路由审批、exit node、key 过期。
- 免费版：单 tailnet 6 用户 + 分享；端口级 ACL 与 ssh checkPeriod 是付费功能。

下一章进入进阶用法：policy 的 tags/groups、Headscale 自建控制面、自建 DERP 与容器/K8s 集成——当免费版或官方中继满足不了你时，这些就是解药。

### 参考来源

[^c4-1]: 裸金属内网穿透对决：frp vs ZeroTier vs Tailscale vs ngrok — https://www.qingyunl.com/news/361.html
[^c4-2]: Tailscale UDP 打洞失败检测与中继回退状态机 — https://blog.hotdry.top/posts/2026/02/19/tailscale-udp-hole-punching-failure-detection/
[^c4-3]: Tailscale Docs：Troubleshoot DERP traffic routing — https://tailscale.com/docs/reference/troubleshooting/network-configuration/derp-routing
[^c4-4]: Tailscale Docs：tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c4-5]: Tailscale Docs：Free pricing plans — https://tailscale.com/docs/account/manage-plans/free-plans-discounts

---

当免费版或官方中继满足不了需求时，最后一步是把控制权握回自己手里。

## 进阶用法

前四章我们一直在把 Tailscale 当「开箱即用的内网穿透」工具：装上、登录、用名字访问，剩下的交给官方云。这一章回答一个更实际的问题——**当默认策略不够用，或者你想把控制权握在自己手里时，应该怎么配**。你会学到 Policy 文件的高级写法（tags / groups / 自动审批 / 自定义 DERP），以及 Headscale 自建控制面、自建 DERP、Docker 与 Kubernetes 容器集成的「能用级」配置。

### 5.1 Tailnet Policy 进阶

Policy 文件用 HuJSON（带注释的 JSON）书写。顶层除了你熟悉的 `acls`、`ssh` 分区，还有 `grants`、`groups`、`tagOwners`、`autoApprovers`、`derpMap` 等[^c5-1]。

**新一代访问控制：`grants`**
`grants` 是新一代访问控制，同时管网络层与应用层，默认 deny-by-default。官方会**无限期支持** `acls`，但不再给它加新特性，新配置推荐迁移到 `grants`。上手阶段知道「grants 是 ACL 的演进方向」即可，不必立刻重写现有规则。

**`groups`：用户分组**
带 `group:` 前缀的组，成员写完整邮箱，**不能嵌套**（组里不能再引用另一个组）；改动会自动传播到引用它的规则。适合把「运维」「开发」这类人员分组复用，避免在每条规则里重复列邮箱。

**`tagOwners`：设备身份标签**
tag 必须先定义在 `tagOwners` 里，才能被 ACL 引用——这跟第一章「服务器推荐用 tag 身份 + auth key 接入」呼应。owner 可以是邮箱、组、autogroup 或另一个 tag；写成 `[]` 简写等于 `autogroup:admin`，表示只有管理员能发这个 tag[^c5-1]。

> [!tip] 大白话：把 `tag:server` 想成发给服务器的**临时工牌**。工牌要先在 `tagOwners` 里登记「谁有权发」，设备戴上它才拥有对应身份。所以 ACL 里写 `tag:server` 之前，必须先定义好 `tagOwners`，否则 tag 不存在、规则无法引用。

**`autoApprovers`：路由自动审批**
第二章我们手动在 admin console 审批 subnet router 和 exit node；`autoApprovers` 可以把审批写进策略文件，`routes` 键管子网路由、`exitNode` 键管出口节点，并指定哪些人/组/tag 能被自动批准。

> [!warning] 易错点：`autoApprovers` 只对**首次广播**的路由生效，不追溯。设备如果后来被他人重新认证，会停止广播路由，已批准规则不会自动恢复。规避办法是给这类设备打 tag，让审批跟随 tag 而不是单个设备。

**网络选项：`derpMap` 与 `randomizeClientPort`**
`derpMap` 用于自定义或禁用默认 DERP（5.3 会用它接入自建中继）；`randomizeClientPort: true` 让客户端改用随机 UDP 端口，替代默认固定的 41641，可规避部分防火墙对固定端口的封禁[^c5-1]。

```jsonc
// policy.hujson —— 组合演示 groups / tagOwners / autoApprovers / derpMap / randomizeClientPort
{
  "groups": {
    "group:ops": ["alice@example.com", "bob@example.com"]
  },
  "tagOwners": {
    "tag:server": ["group:ops"],
    "tag:nas": []
  },
  "autoApprovers": {
    "routes": {
      "192.0.2.0/24": ["tag:server"],
      "198.51.100.0/24": ["tag:server"]
    },
    "exitNode": ["group:ops"]
  },
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "mydc",
        "RegionName": "My Data Center",
        "Nodes": [
          { "Name": "mydc1", "RegionID": 900, "HostName": "derp.example.com" }
        ]
      }
    }
  },
  "randomizeClientPort": true
}
```

### 5.2 Headscale：自建控制面

Tailscale 除各 GUI 客户端和控制服务器外基本全开源。**Headscale 就是那个「控制服务器」的自托管替代品**[^c5-2]。

**它做什么、不做什么**
控制面只负责四件事：交换 WireGuard 公钥、分配 `100.x.y.z` IP、维护用户边界、暴露路由；**数据面仍走节点间的 WireGuard**——即使换成 Headscale，设备之间的流量依然是端到端加密的 P2P，不经过控制面。Headscale 的设计目标是**窄范围的单一 tailnet**，面向个人或小型开源组织[^c5-2]。

> [!tip] 大白话：把控制面想成酒店前台：它只负责登记住客（交换公钥）、分配房号（IP）、确认身份（用户边界）；住客之间的行李搬运仍是点对点完成的。所以 Headscale 只替换「前台」，不介入也不影响你的实际数据流量。

**部署注意**
官方不支持也不鼓励把 Headscale 放在反向代理后面，或用容器部署；文档分 stable / development 两版，**必须按发布版本选对应的 GitHub tag**，不要直接拉 master。具体部署细节以 headscale.net/stable 为准——README 不含自定义 DERP 的接入细节[^c5-2]。

```bash
# 创建用户（对应 tailnet 里的身份边界）
headscale users create myuser
# 注册节点：把客户端登录时生成的 node key 绑定到该用户
headscale nodes register --user myuser --key nodekey:xxxxx
```

### 5.3 自建 DERP

DERP 是直连失败且没有 Peer Relay 时的**回退中继**（第四章已讲它如何兜底）。注意：**DERP 目前是 alpha 阶段**，大多数情况用官方默认就够，自建只为合规或降低延迟[^c5-3]。

> [!tip] 大白话：把 DERP 想成小区门口的中转驿站：两家直连不上时，包裹先经驿站中转，但驿站不拆看内容（中继流量仍端到端加密）。所以只有打洞失败才用得上它，多数场景无需自建。带宽与性能影响可参考 [[内网穿透带宽性能分析]]。

**硬性要求**
DERP 靠**源 IP**识别设备，客户端用 HTTP upgrade 建双向通道，所以它必须**直连公网**——不能放在 NAT 或负载均衡后面；需要开放 443（HTTPS/HTTP）与 3478（STUN），并允许 ICMP[^c5-3]。

> [!warning] 易错点：DERP 不能放 NAT / 负载均衡后面。云厂商的 LB 大多不支持 HTTP upgrade 的双向通道，源 IP 也会被改写，导致客户端认不出彼此。硬性要求是 443 + 3478 放通、允许 ICMP。

**部署与接入**

```bash
# 编译安装 derper（需要 Go 环境）
go install tailscale.com/cmd/derper@latest
# 启动：域名要指向这台公网服务器
sudo derper --hostname=example.com
```

在 policy 的 `derpMap` 里声明自己的 region。**region ID 900–999 保留给自定义**；每个 region 放一个 server，想要冗余就配多个 region[^c5-3]。

```jsonc
{
  "derpMap": {
    "OmitDefaultRegions": true,
    "Regions": {
      "900": {
        "RegionID": 900,
        "RegionCode": "mydc",
        "RegionName": "My Data Center",
        "Nodes": [
          { "Name": "mydc1", "RegionID": 900, "HostName": "derp.example.com" }
        ]
      }
    }
  }
}
```

**防蹭与监控**
自建 DERP 默认对所有人开放，可能被当成免费中继。加 `--verify-clients` 可要求客户端在本机跑 tailscaled 校验身份；同仓库还提供 `cmd/derpprobe`，可周期性探测 DERP 的可用性[^c5-3]。

```bash
# 防蹭：只服务本机 tailscaled 认证过的客户端
sudo derper --hostname=example.com --verify-clients
```

### 5.4 Docker 与 Kubernetes 集成

Tailscale 官方支持在容器和 K8s 里运行，形态分四种：**operator / sidecar / proxy / subnet router**，用途覆盖 Service 入口（ingress）、tailnet 出站（egress）、安全访问 kube-apiserver[^c5-4]。Docker 是上手成本最低的一类：官方镜像 `tailscale/tailscale`（GitHub Container Registry 对应 `ghcr.io/tailscale/tailscale`）把 `tailscaled` 与启动脚本 containerboot 打包在一起，用环境变量驱动[^c5-6]。

#### 5.4.1 单机部署：`docker run`

先到 admin console → **Keys** → Generate auth key 生成一次性密钥，然后启动：

```bash
docker pull tailscale/tailscale:latest

docker run -d \
  --name tailscale \
  --hostname tailscale-nginx \
  -e TS_AUTHKEY=<tskey-YOUR-AUTH-KEY> \
  -e TS_STATE_DIR=/var/lib/tailscale \
  -v ./tailscale-state:/var/lib/tailscale \
  --cap-add=net_admin \
  --cap-add=net_raw \
  --restart unless-stopped \
  tailscale/tailscale:latest
```

启动后在 admin console 的 Machines 页看到 `tailscale-nginx`，说明节点已加入 tailnet。常用环境变量速查[^c5-6][^c5-7]：

| 变量 | 作用 | 等价 CLI |
|------|------|----------|
| `TS_AUTHKEY` | 认证密钥，容器自动登录 | `tailscale login --auth-key=` |
| `TS_STATE_DIR` | 状态目录，必须持久化 | `tailscaled --statedir=` |
| `TS_USERSPACE` | user-space 网络开关（默认 true） | `tailscaled --tun=userspace-networking` |
| `TS_HOSTNAME` | 自定义 tailnet 主机名 | `tailscale set --hostname=` |
| `TS_ROUTES` | 广播子网路由 | `tailscale set --advertise-routes=` |
| `TS_ACCEPT_DNS` | 接受 MagicDNS 配置（默认不接收） | `tailscale up --accept-dns` |
| `TS_EXTRA_ARGS` | 附加 `tailscale up` 参数 | 如 `--advertise-exit-node --ssh` |
| `TS_TAILSCALED_EXTRA_ARGS` | 附加 `tailscaled` 参数 | 如 `--verbose=2` |

> [!warning] 易错点：状态目录必须持久化
> 容器默认把状态放在临时目录，**不挂载 volume 的话，每次重启都会注册成新节点**，admin console 里会堆满重复设备。`-v ./tailscale-state:/var/lib/tailscale` 就是为了保住节点身份（私钥），这条不能省。

**user-space 与内核态**：镜像默认 `TS_USERSPACE=true`（user-space networking），不需要 `/dev/net/tun`，适合「只让这台容器自己入网」；但性能略低，且共享命名空间的其它容器无法透明访问 tailnet。要用内核态 WireGuard（sidecar 模式必需），设 `TS_USERSPACE=false` 并挂载 TUN 设备：

```bash
docker run -d \
  --name tailscale \
  --hostname my-node \
  -e TS_AUTHKEY=<tskey-YOUR-AUTH-KEY> \
  -e TS_STATE_DIR=/var/lib/tailscale \
  -e TS_USERSPACE=false \
  -v ./tailscale-state:/var/lib/tailscale \
  -v /dev/net/tun:/dev/net/tun \
  --cap-add=net_admin \
  --cap-add=net_raw \
  --restart unless-stopped \
  tailscale/tailscale:latest
```

#### 5.4.2 Sidecar 模式：把应用容器接进 tailnet

最常见的需求是「我有个容器服务（nginx、Grafana、Home Assistant…），只想让 tailnet 内的人访问」。做法是让应用容器共享 Tailscale 容器的网络命名空间，应用本身不用改任何代码：

```yaml
# docker-compose.yml
services:
  tailscale:
    image: tailscale/tailscale:latest
    hostname: my-app          # MagicDNS 里显示的名字
    environment:
      - TS_AUTHKEY=${TS_AUTHKEY}
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_USERSPACE=false    # sidecar 模式必须内核态
    volumes:
      - ts-state:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - NET_ADMIN
      - NET_RAW
    restart: unless-stopped

  nginx:
    image: nginx:latest
    network_mode: service:tailscale   # 共享 tailscale 容器的网络栈
    depends_on:
      - tailscale

volumes:
  ts-state:
```

`network_mode: service:tailscale` 让 nginx 与 tailscale 共用同一套网络栈：nginx 监听 `80`，就直接出现在 Tailscale 容器的 `100.x` IP 与 MagicDNS 主机名上，tailnet 成员用 `http://my-app` 就能访问。数据路径：加密包 → tailscaled 解密 → `tailscale0` 虚拟网卡 → 共享命名空间内的 nginx[^c5-6]。

> [!warning] 易错点：容器默认没有 DNS
> 容器不继承宿主机 DNS 配置，**MagicDNS 在容器里默认不生效**。要用机器名访问其它设备，必须显式设 `TS_ACCEPT_DNS=true`，否则只能写 `100.x` IP（K8s 里同理，见 5.4.4）。

#### 5.4.3 容器作子网路由 / Exit Node

思路与第二章完全一致，只是把 CLI flag 换成环境变量：

```bash
# 子网路由：广播本机可达的网段（用 host 网络）
docker run -d \
  --name ts-subnet-router \
  --network=host \
  --cap-add=net_admin \
  -e TS_AUTHKEY=<tskey-YOUR-AUTH-KEY> \
  -e TS_ROUTES=192.168.1.0/24,192.168.2.0/24 \
  -e TS_EXTRA_ARGS=--accept-routes \
  tailscale/tailscale:latest

# Exit node：整台设备当公网出口
docker run -d \
  --name ts-exit-node \
  --network=host \
  --cap-add=net_admin \
  -e TS_AUTHKEY=<tskey-YOUR-AUTH-KEY> \
  -e TS_EXTRA_ARGS=--advertise-exit-node \
  tailscale/tailscale:latest
```

广播后照例要去 admin console **审批路由**，客户端再 `tailscale set --accept-routes`（子网）或用 `--exit-node=<设备名>`（出口）使用[^c5-6][^c5-7]。

#### 5.4.4 Kubernetes 部署

容器认证方式与 Docker 相同：用 auth key——一次性（ephemeral）或可复用（reusable）——存到 K8s Secret `TS_AUTHKEY`；如果没配 key，也能从容器日志里拿到登录 URL 完成认证。ephemeral 节点关机后自动从 tailnet 移除[^c5-4]。

K8s 下的 subnet router 与 5.4.3 一致，只是把路由声明放进 `TS_ROUTES`，例如 `TS_ROUTES=10.20.0.0/16,10.42.0.0/15`，然后在 admin console 启用、客户端 `--accept-routes`[^c5-4][^c5-5]。

```yaml
# K8s 部署 tailscale 时注入的环境变量（以 sidecar / subnet router 为例）
env:
  - name: TS_AUTHKEY
    valueFrom:
      secretKeyRef:
        name: tailscale-auth
        key: TS_AUTHKEY
  - name: TS_ROUTES
    value: "10.20.0.0/16,10.42.0.0/15"
  - name: TS_ACCEPT_DNS
    value: "true"
```

> [!warning] 易错点：容器默认没有 DNS 解析（不继承宿主机配置），所以 MagicDNS 在容器里默认不生效。需要 MagicDNS 时，必须显式设 `TS_ACCEPT_DNS=true`，否则只能用 IP 访问其他设备。

### 本章小结

- `grants` 是新一代访问控制（deny-by-default），`acls` 无限期支持但推荐新配置迁移；`groups` 不能嵌套，tag 必须先定义在 `tagOwners` 才能被 ACL 引用。
- `autoApprovers` 只对首次广播的路由生效，重认证会停播；`randomizeClientPort` 用随机端口替代固定 UDP 41641。
- Headscale 自托管控制面只替换「前台」，数据面仍走节点间 WireGuard；不鼓励反代/容器部署，必须按发布版本选 GitHub tag。
- 自建 DERP 处于 alpha，必须直连公网（不能 NAT/LB）、开放 443+3478；region ID 900–999 留给自定义，`--verify-clients` 防蹭、`cmd/derpprobe` 监控。
- Docker 单机部署用官方镜像 `tailscale/tailscale` + `TS_*` 环境变量；**状态目录必须挂 volume 持久化**，否则每次重启都是新节点。Sidecar 用 `network_mode: service:tailscale` 共享网络栈（需 `TS_USERSPACE=false`），容器作 subnet router / exit node 用 `TS_ROUTES` / `TS_EXTRA_ARGS`。容器默认无 DNS，MagicDNS 需 `TS_ACCEPT_DNS=true`。

到这里，五章正文全部完成。下一步会把全部分章节拼成一篇完整的《Tailscale 使用教程》，统一标题层级、检查引用，并做 Obsidian 美化发布。

### 参考来源

[^c5-1]: Tailnet policy file 语法 — https://tailscale.com/docs/reference/syntax/policy-file
[^c5-2]: Headscale GitHub 仓库 — https://github.com/juanfont/headscale
[^c5-3]: 自定义 DERP 服务器 — https://tailscale.com/docs/reference/derp-servers/custom-derp-servers
[^c5-4]: Tailscale on Kubernetes — https://tailscale.com/docs/kubernetes
[^c5-5]: Tailscale CLI 参考 — https://tailscale.com/docs/reference/tailscale-cli
[^c5-6]: Tailscale Docs：在 Docker 中连接容器（standalone） — https://tailscale.com/docs/features/containers/docker/how-to/connect-docker-standalone
[^c5-7]: Tailscale Docs：Docker 配置参数（环境变量） — https://tailscale.com/docs/features/containers/docker/docker-params

---

## 结语

到这里，五章内容就走完了：从把第一台设备接入 tailnet，到用名字访问、ACL 收紧权限，再到 serve/funnel 暴露服务、Tailscale SSH 免密登录，最后落到选型排错与进阶能力。整个学习路径可以概括为「先会用，再会修，最后把控制权握在自己手里」。如果只是想上手，前两章就能覆盖大部分日常场景；第四、五章可以在遇到性能、合规或扩容需求时回来精读。下一步，不妨挑一台设备把全文的命令从头到尾跑一遍，再回到 [[内网穿透带宽性能分析]] 对照理解带宽与打洞原理。

---

## 更新记录

- 2026-08-28：补充 5.4 节 Docker 部署内容（standalone `docker run`、Compose Sidecar、容器作 subnet router / exit node），节标题改为「Docker 与 Kubernetes 集成」，并新增 `TS_*` 环境变量速查表与官方文档来源。
