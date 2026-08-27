## 基础安装与登录

本章解决三个问题：Tailscale 到底是什么、该用什么账号注册、如何把第一台设备装好并登录。学完你就能把一台设备接进 tailnet，并用最基础的 CLI 确认连接状态。动手前建议先回顾 [[内网穿透带宽性能分析]] 里的 NAT、P2P 与中继概念——本章的术语都建立在它们之上。

### 1.1 认识 Tailscale 与核心概念

Tailscale 是基于 WireGuard 构建的组网工具：它把分散在不同网络（NAT、防火墙背后）的设备组合成一个私有虚拟局域网，也就是 **tailnet**。设备加入后就像在同一个局域网里互访，无需配置端口映射或申请公网 IP[^c1-1]。

理解它工作方式的关键是「控制面 / 数据面」分离模型：

- **控制面（coordination plane）**：Tailscale 的控制服务器负责身份认证、交换各设备的 WireGuard 公钥、分配虚拟 IP。它不承载你的业务流量。
- **数据面（data plane）**：设备之间直接建立 WireGuard 加密隧道传输数据；打洞失败时回退到 DERP 中继转发，但流量始终端到端加密[^c1-1]。

[!tip] 大白话
把控制面想成**电话总机**：总机只帮你登记号码、接通线路，不参与你们通话内容；数据面才是你们直接对话的那条线路。所以 Tailscale 服务器挂掉时，已建立的设备间连接往往还能继续走。

[!note] 核心概念
**tailnet** 就是「你的虚拟内网」。登录进同一个 tailnet 的设备互相视为同一私网成员，新设备加入后自动获得与成员互通的能力。

每台设备加入 tailnet 时会被自动分配一个唯一的 `100.x.y.z` 虚拟 IP。它与设备所在物理网络无关，跨网络、跨防火墙保持稳定，可当作访问这台设备的固定地址[^c1-1]。

[!tip] 大白话
把 `100.x.y.z` 想成小区的**固定门牌号**：住户今天在哪个城市（物理网络）不影响门牌号。访问设备时直接记这个地址就行，不用管它在哪个公网 IP 后面、端口映射有没有配。

### 1.2 账号与套餐选择

注册有两条等价路径[^c1-1]：

1. 打开官网点 **Get Started**，用 SSO 账号（Google、GitHub、Microsoft 等）登录创建 tailnet；
2. 或先安装客户端，运行登录命令后访问 `login.tailscale.com/start` 完成注册。

[!warning] 易错点
套餐口径：用 `@gmail.com` 等**公共邮箱**注册会进入 **Personal 免费版**，单个 tailnet 免费 **6 个用户**；用**自定义域名**邮箱注册会自动进入 **Enterprise 14 天试用**。想长期用免费版就用公共邮箱[^c1-1][^c1-3]。旧「100 设备」的说法已废弃，设备数上限以官方 Pricing 页为准[^c1-3]。

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

**本章小结**

- Tailscale 采用控制面 / 数据面分离：控制服务器只做协调，业务流量走节点间 WireGuard 加密隧道。
- 每台设备自动获得唯一 `100.x.y.z` IP，跨网络稳定，是访问设备的固定地址。
- 公共邮箱注册进 Personal 免费版（6 用户），自定义域名会进 Enterprise 试用。
- Linux 一键脚本 + `sudo tailscale up` 即可完成安装登录；iOS / Android 无 CLI，用官方 App。
- 常用 CLI：`up` / `status` / `ip` / `whoami` / `down` / `logout` / `set`。

下一章进入实战：用 MagicDNS 用名字直接访问设备、配置子网路由访问家里内网、用 Exit Node 在不安全 Wi-Fi 下安全上网。

## 参考来源

[^c1-1]: Tailscale Quickstart — https://tailscale.com/docs/how-to/quickstart
[^c1-2]: Tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c1-3]: Free pricing plans — https://tailscale.com/docs/account/manage-plans/free-plans-discounts
