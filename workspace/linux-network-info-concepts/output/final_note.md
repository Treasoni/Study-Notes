---
title: "Linux 网络信息获取与概念"
subtitle: "从概念到命令，系统掌握 Linux 网络信息查询"
tags: [linux, network, iproute2, dns, tcpdump, ip, ss, dig]
created: 2026-07-29
updated: 2026-07-29
status: complete
source_project: linux-network-info-concepts
---

# Linux 网络信息获取与概念

> 从概念到命令，系统掌握 Linux 网络信息查询

**笔记类型**：实战笔记（概念解释 + 查询命令 + 实战示例）  |  **总章节**：10 章  |  **预计学习时间**：带实操约 8–12 小时

---

## 关于本笔记

这是一本系统性学习 Linux 上网络信息查询命令与概念的实战笔记。从网络接口、IP 地址、路由表、DNS 解析到 Socket 连接、无线网络、监控统计和抓包分析，覆盖 Linux 网络栈的各个层次。

如果你已经知道 `ifconfig` 和 `ping`，但想系统掌握 `ip`、`ss`、`dig`、`tcpdump` 等现代工具的完整用法，并理解背后的网络概念，这本笔记就是为你准备的。

### 前置要求

- 基本的 Linux 命令行操作能力（能运行命令、理解管道和重定向）
- 了解 IP 地址的基本概念（知道 IPv4 是类似 `192.168.1.1` 的数字）
- 能使用包管理器安装软件（`apt install` / `pacman -S`）

### 建议学习顺序

1. **第一章必读**：奠定分层模型和工具家族的全局认知，后续各章都基于此框架
2. **第二至七章建议按序阅读**：从 L2 到 L7 层层递进，每章概念依赖前一章
3. **第八章（无线）**：如果当前设备没有无线网卡，可跳读或仅了解命令结构
4. **第九章（监控）与第十章（抓包）**：属于独立进阶技能，可在前面七章之后任意顺序学习

---

## 目录

1. [第一章：网络信息查询概览与工具链](#第一章网络信息查询概览与工具链)
   - [一句话说清 Linux 网络信息](#一句话说清-linux-网络信息)
   - [分层视角](#分层视角)
   - [工具家族：iproute2 vs net-tools](#工具家族iproute2-vs-net-tools)
   - [查询命令速查表](#查询命令速查表)
   - [信息查询通用思路](#信息查询通用思路)
2. [第二章：网络接口与链路层信息](#第二章网络接口与链路层信息)
   - [链路层概念速览](#链路层概念速览)
   - [`ip link`：查看网卡状态](#ip-link查看网卡状态)
   - [`ip -s link`：收发统计信息](#ip--s-link收发统计信息)
   - [`ip -j` JSON 输出](#ip--j-json-输出)
   - [`ethtool`：网卡硬件信息与驱动查询](#ethtool网卡硬件信息与驱动查询)
   - [常见链路层问题排查](#常见链路层问题排查)
3. [第三章：IP 地址与子网信息](#第三章ip-地址与子网信息)
   - [IP 地址核心概念](#ip-地址核心概念)
   - [子网掩码与 CIDR](#子网掩码与-cidr)
   - [特殊 IP 地址](#特殊-ip-地址)
   - [`ip addr` 命令详解](#ip-addr-命令详解)
   - [`ip -j` + jq 脚本化获取 IP](#ip--j--jq-脚本化获取-ip)
   - [常见坑](#常见坑)
4. [第四章：路由表信息](#第四章路由表信息)
   - [路由表核心概念](#路由表核心概念)
   - [最长前缀匹配规则](#最长前缀匹配规则)
   - [`ip route show` 详解](#ip-route-show-详解)
   - [`ip route get`：模拟路由决策](#ip-route-get模拟路由决策)
   - [策略路由：`ip rule` 与多路由表](#策略路由ip-rule-与多路由表)
   - [路由排查思路](#路由排查思路)
5. [第五章：DNS 解析与域名信息](#第五章dns-解析与域名信息)
   - [DNS 解析完整流程](#dns-解析完整流程)
   - [DNS 记录类型详解](#dns-记录类型详解)
   - [Linux DNS 配置文件体系](#linux-dns-配置文件体系)
   - [systemd-resolved 与 resolvectl](#systemd-resolved-与-resolvctl)
   - [`dig` 命令详解](#dig-命令详解)
   - [`nslookup` 与 `host` 快速查询](#nslookup-与-host-快速查询)
   - [常见 DNS 排查场景](#常见-dns-排查场景)
6. [第六章：ARP 与邻居发现](#第六章arp-与邻居发现)
   - [ARP 协议核心概念](#arp-协议核心概念)
   - [邻居状态机详解](#邻居状态机详解)
   - [`ip neigh show` 输出解读](#ip-neigh-show-输出解读)
   - [`ip neigh flush` 清除邻居表](#ip-neigh-flush-清除邻居表)
   - [IPv6 NDP 取代 ARP](#ipv6-ndp-取代-arp)
   - [ARP 表溢出与 `gc_thresh` 排障](#arp-表溢出与-gc_thresh-排障)
7. [第七章：Socket 连接与传输层信息](#第七章socket-连接与传输层信息)
   - [TCP/UDP 协议概念速览](#tcpudp-协议概念速览)
   - [TCP 状态机](#tcp-状态机)
   - [Socket 与连接五元组](#socket-与连接五元组)
   - [`ss` 命令详解](#ss-命令详解)
   - [状态过滤与端口过滤](#状态过滤与端口过滤)
   - [Recv-Q / Send-Q 排障](#recv-q--send-q-排障)
   - [`ss` vs `netstat` 性能对比](#ss-vs-netstat-性能对比)
8. [第八章：无线网络信息](#第八章无线网络信息)
   - [`iw` vs `iwconfig`](#iw-vs-iwconfig)
   - [`iw dev`：查看无线网卡](#iw-dev查看无线网卡)
   - [`iw dev wlan0 link`：查看当前连接状态](#iw-dev-wlan0-link查看当前连接状态)
   - [`iw dev wlan0 scan`：扫描 AP](#iw-dev-wlan0-scan扫描-ap)
   - [`nmcli device wifi`：用 NetworkManager 管理无线](#nmcli-device-wifi用-networkmanager-管理无线)
   - [无线信号质量指标解读](#无线信号质量指标解读)
9. [第九章：网络监控与统计](#第九章网络监控与统计)
   - [网络监控四维分类](#网络监控四维分类)
   - [`iftop`：按连接查看实时带宽](#iftop按连接查看实时带宽)
   - [`nload`：简洁流量总览](#nload简洁流量总览)
   - [`nethogs`：按进程归因流量](#nethogs按进程归因流量)
   - [`bmon`：ASCII 图表 + 详细统计](#bmonascii-图表--详细统计)
   - [`ethtool -S`：网卡硬件级统计](#ethtool--s网卡硬件级统计)
   - [`vnstat`：历史流量统计](#vnstat历史流量统计)
   - [`/proc/net/dev`：底层数据源](#procnetdev底层数据源)
10. [第十章：抓包与协议分析基础](#第十章抓包与协议分析基础)
    - [tcpdump 基础用法](#tcpdump-基础用法)
    - [BPF 过滤表达式](#bpf-过滤表达式)
    - [抓包存储与读取](#抓包存储与读取)
    - [报文输出逐字段解读](#报文输出逐字段解读)
    - [实用过滤场景](#实用过滤场景)
    - [权限说明](#权限说明)
    - [与其他工具的配合](#与其他工具的配合)

---

## 第一章：网络信息查询概览与工具链

### 一句话说清 Linux 网络信息

当你在一台 Linux 机器上敲下 `ip addr`、`ss -tulnp` 或 `dig baidu.com` 时，你其实在做同一件事：**从操作系统中读取网络栈某个层面的状态数据**。这些数据——IP 地址、路由表、DNS 记录、TCP 连接状态——统称为"网络信息"。

> **一句话定义**：Linux 网络信息就是操作系统内核网络栈在各个层次上暴露出来的状态数据，通过特定的命令或接口读取。

常见误解是"网络信息 = ifconfig 的输出"。实际上，`ifconfig` 只是读取链路层 + 网络层信息的工具之一。要系统掌握网络查询，首先需要理解两个关键框架：

1. **分层模型**——告诉你"信息属于哪一层"
2. **工具家族**——告诉你"用什么工具去读"

---

### 分层视角：一层一层的网络信息

网络通信是分层的。每一层只关心自己的"信息"，并向上层提供抽象服务。了解分层有助于精准定位：出了问题，是 IP 配错了、路由没设好、还是 DNS 解析失败？

#### OSI / TCP-IP 模型映射

```
  OSI 模型          TCP-IP 模型           网络信息举例               查询命令
  ────────────      ────────────          ──────────               ──────────
  应用层 (L7)       │                      Socket 连接、DNS 记录    ss -tunap, dig
  表示层 (L6)       │  应用层
  会话层 (L5)       │

  传输层 (L4)       │  传输层              TCP/UDP 端口、连接状态    ss, netstat
                                          Recv-Q/Send-Q、拥塞窗口

  网络层 (L3)       │  网络层              IP 地址、路由表、ARP 表   ip addr, ip route
                                                                  ip neigh

  数据链路层 (L2)   │  网络接口层          MAC 地址、MTU、网卡状态   ip link, ethtool
                                          CRC 错误、协商速率

  物理层 (L1)       │                     Link 信号、网线连接        ethtool, ip link
```

> [!note] 核心认知
> 每条"网络信息"都属于特定层次。**查错了层**是新手最常犯的错误——比如路由不通却去查 MAC 地址，或者 DNS 解析失败却盯着 IP 配置看。

#### 从问题到查询：分层排查示例

假设你发现 `curl https://example.com` 卡住不动了，应该从底层往上层逐层排查：

| 排查步骤 | 查询命令 | 检查什么 |
|---------|---------|---------|
| 1. 网卡是否正常 | `ip link show` | `state UP` 还是 `DOWN`？ |
| 2. IP 是否配置正确 | `ip addr show` | 是否有合法 IP？子网掩码对不对？ |
| 3. 默认路由是否存在 | `ip route show default` | 网关是否可达？ |
| 4. 网关能否 ping 通 | `ping -c 3 <gateway>` | 延迟是否正常？有无丢包？ |
| 5. DNS 能否解析 | `dig example.com` | 是否返回 IP？超时还是 NXDOMAIN？ |
| 6. 目标端口是否可达 | `ss -tunap` 或 `curl -v` | 连接是否被拒绝？超时？ |

> 这个排查顺序在本笔记后续章节中会反复出现，每一章都会展开对应层的排查细节。

---

### 工具家族：iproute2 vs net-tools

Linux 网络查询工具分属两个家族：一个代表过去，一个代表现在。

#### 全面对比

| 对比维度 | iproute2（现代） | net-tools（传统） |
|---------|-----------------|------------------|
| **代表命令** | `ip`、`ss`、`bridge` | `ifconfig`、`netstat`、`arp`、`route` |
| **内核接口** | netlink socket（高效，事件驱动） | `/proc` 文件系统 + ioctl（轮询，较慢） |
| **性能** | 快（ss 比 netstat 快 10-100 倍） | 慢（大量连接时明显） |
| **输出格式** | 支持 `-j` JSON 输出，可脚本解析 | 纯文本，解析困难 |
| **IPv6 支持** | 原生完整支持 | 部分命令需额外参数 |
| **维护状态** | 内核维护，持续更新 | 多数发行版已标记为弃用 |
| **预装情况** | 几乎全部现代发行版默认预装 | Ubuntu 24.04+ 不再预装，需 `apt install net-tools` |
| **代码规模** | 约 80 个工具组合在 `ip` 二进制中 | 每个命令独立二进制 |

#### 新旧命令等效替换表

| 查询目标 | 旧命令 | 新命令 |
|---------|-------|-------|
| 网卡状态和 MAC | `ifconfig -a` | `ip link show` |
| IP 地址 | `ifconfig eth0` | `ip addr show eth0` |
| 路由表 | `route -n` | `ip route show` |
| ARP 表 | `arp -a` | `ip neigh show` |
| 监听端口 | `netstat -tulnp` | `ss -tulnp` |
| Socket 统计 | `netstat -s` | `ss -s` |
| 多播地址 | `netstat -g` | `ip maddr show` |
| VLAN | `vconfig` | `ip link add link eth0 name eth0.10 type vlan id 10` |

> [!warning] 不要混用新旧工具
> 虽然两者可以共存，但不建议在同一个脚本或排查过程中混用。不一致的输出格式和底层数据源可能引入混淆。**如果你在用一个现代发行版（Ubuntu 22.04+、Debian 12+、Fedora 38+），默认选择 iproute2 即可。**

---

### 查询命令速查表

以下按"想查什么"组织，方便快速定位。每个命令对应的详细用法将在后续章节展开。

#### 按场景查找

| 想查什么 | 优先使用命令 | 所属层次 | 后续章节 |
|---------|------------|---------|---------|
| 网卡是否在线、MAC 地址、MTU | `ip link show` | L2 | 第二章 |
| 网卡速率、驱动、硬件信息 | `ethtool eth0` | L1/L2 | 第二章 |
| IP 地址、子网掩码、scope | `ip addr show` | L3 | 第三章 |
| 默认网关、路由表 | `ip route show` | L3 | 第四章 |
| DNS 解析结果 | `dig baidu.com` | L7 | 第五章 |
| 系统 DNS 配置 | `resolvectl status` | L7 | 第五章 |
| 目标 IP 对应哪个 MAC | `ip neigh show` | L2 | 第六章 |
| 哪些端口在监听 | `ss -tulnp` | L4 | 第七章 |
| TCP 连接状态统计 | `ss -tanp` | L4 | 第七章 |
| 连通性测试 | `ping -c 5 <IP>` | L3/L4 | — |
| 路由追踪 | `mtr baidu.com` | L3 | — |
| WiFi 信号强度和 SSID | `iw dev wlan0 link` | L1/L2 | 第八章 |
| 实时带宽 | `iftop -i eth0` | L2-L4 | 第九章 |
| 网卡 CRC 错误统计 | `ethtool -S eth0` | L2 | 第九章 |
| 抓包分析 | `tcpdump -i eth0` | L2-L7 | 第十章 |

> [!tip] 快速记忆口诀
> **"链路看 `link`，地址看 `addr`，路由看 `route`，邻居看 `neigh`"**——`ip` 工具的四个主命令覆盖了 80% 的日常查询需求。

---

### 信息查询通用思路

工具知道在哪之后，还需要知道"怎么查"。以下是经过大量实践验证的通用思路，适用所有网络信息查询场景。

#### 三步排查法

```
1. 确认状态（正常吗？）
2. 读取配置（设了什么？）
3. 验证连通（实际通不通？）
```

**示例——查 IP 配置**：
```bash
# 第一步：确认状态
ip -br addr show                       # eth0 有 IP 吗？state UP 吗？

# 第二步：读取配置（如有异常）
ip addr show eth0                      # 详细信息：DHCP 还是静态？scope 是 global 还是 link？

# 第三步：验证连通
ping -c 3 $(ip -4 -br addr show eth0 | awk '{print $3}' | cut -d/ -f1)  # 自己 ping 自己
```

#### 信息查询通用方法论

1. **从全局到局部**：先用简洁模式（`-br`）获取概览，再深入特定接口或条目
2. **从底层到上层**：先确认物理/链路层正常，再查网络层、传输层、应用层
3. **交叉验证**：多个工具验证同一个信息——例如 `ip -j addr show` + `curl ifconfig.me` 双重确认公网 IP
4. **善用 JSON 输出**：`ip -j` + `jq` 适合脚本化批量查询，且比解析文本更可靠

#### 常见误区

| 误区 | 正确做法 |
|------|---------|
| 装了网卡驱动就一定能看到 `ip link up` | 检查物理连接、协商速率、`ethtool eth0` 确认 Link detected: yes |
| `ifconfig` 看不到 IP 就是没 IP | 用 `ip addr show` 确认，有些发行版不再通过 `ifconfig` 暴露某些地址 |
| ping 不通就是网络断了 | 先确认是否 ICMP 被防火墙拦截（很多云服务器默认禁 ping） |
| `netstat` 很慢就是机器有问题 | `netstat` 读 `/proc` 本身慢，改用 `ss` |

---

### 本章小结

- Linux 网络信息是内核网络栈各层的状态数据，通过特定命令读取
- **分层模型是排查的根本框架**——查的信息属于哪一层，就用哪一层的工具
- **iproute2 是现代 Linux 网络查询的标准工具家族**，已全面替代 net-tools，推荐全部迁移
- 速查表帮助你按"想查什么→用什么命令"快速定位，是本书的导航索引
- 通用排查思路=**确认状态→读取配置→验证连通**，后续每章都围绕这个框架展开

#### 下章预告

下一章我们从最底层开始——**网络接口与链路层信息**。你会学到如何用 `ip link` 查看 MAC 地址和 MTU，用 `ethtool` 探测网卡硬件信息，以及如何用 `ip -j` JSON 输出配合 `jq` 做自动化解析。

---

---

## 第二章：网络接口与链路层信息

### 从"物理连接"到"数据帧"——链路层到底负责什么

第一章我们建立了分层排查的全局观。现在，从最底层的**数据链路层（L2）**开始动手。当你敲下 `ip link show` 时，看到的不只是"网卡是 UP 还是 DOWN"——你看到的是内核与物理网络设备之间最原始的状态接口：MAC 地址、MTU、收发统计、驱动信息。理解这些信息的含义，是后续排查 IP、路由、连接问题的基础。

链路层解决的问题很朴素：**在同一个物理网络（同一根网线或同一个 WiFi 热点）上，两个设备如何可靠地交换数据？** 它不关心 IP 地址，不关心路由，只关心——从 A 的网卡到 B 的网卡，帧能不能过去。

---

### 1. 链路层概念速览

#### 1.1 MAC 地址：网卡的"硬件身份证"

MAC 地址（Media Access Control Address）是网卡出厂时烧录的 48 位标识符，通常表示为 12 位十六进制数：

```
aa:bb:cc:dd:ee:ff
```

**关键特征**：

| 属性 | 说明 |
|------|------|
| 长度 | 6 字节（48 位） |
| 表示法 | 12 位十六进制，通常用冒号分隔（`aa:bb:cc:dd:ee:ff`） |
| 范围 | 全球唯一（理论上），前 3 字节是 OUI（厂商代码） |
| 作用域 | **同一广播域内有效**——跨路由设备无法通过 MAC 寻址 |
| 可修改 | 支持软件覆盖（`ip link set dev eth0 address aa:bb:cc:dd:ee:ff`） |

> [!note] MAC 地址 vs IP 地址
> MAC 地址是"原地物理身份"，IP 地址是"逻辑位置"。类比：MAC 是身份证号（出生就有，基本不变），IP 是住址（搬家就变）。网络通信中，IP 地址用于跨网络寻址，MAC 地址用于同一链路内的帧交付。

#### 1.2 以太网帧结构：L2 的数据单元

数据在链路层的传输单位是**帧（Frame）**。以太网帧的简化结构如下：

```
  ┌─────────────────────────────────────────────────────────┐
  │ 目的MAC  │  源MAC   │  Type/Len │  Payload  │   FCS    │
  │ (6 字节)  │ (6 字节)  │ (2 字节)  │ (46-1500B)│ (4 字节) │
  └─────────────────────────────────────────────────────────┘
```

- **目的 MAC**：接收方网卡的 MAC 地址
- **源 MAC**：发送方网卡的 MAC 地址
- **Type**：上层协议标识。`0x0800` = IPv4，`0x0806` = ARP，`0x86DD` = IPv6
- **Payload**：上层数据（IP 包等），最小 46 字节，最大 1500 字节
- **FCS**：帧校验序列（CRC），检测传输错误

> [!tip] 为什么 Payload 最小 46 字节？
> 这是以太网协议的碰撞检测机制决定的。如果上层数据不足 46 字节，网卡会自动填充到最小长度。你在 Wireshark 抓包中看到的 `[Padding]` 就是填充字节。

#### 1.3 MTU：一个以太网帧能装多少数据

**MTU（Maximum Transmission Unit）** 是网络接口所能传输的最大数据包大小（字节）。标准以太网 MTU = **1500 字节**。

```
MTU 1500 = 以太网头(14) + IP 头(20) + TCP 头(20) + 数据(1446)
                                           ↓
                                    TCP MSS = 1460
                            (MTU - IP头 - TCP头，不含以太网头)
```

> [!note] MTU 与 MSS 的关系
> - **MTU** 是链路层的限制：一个帧最多能装多少数据（包括 IP 头 + TCP 头）
> - **MSS (Maximum Segment Size)** 是 TCP 层的限制：一个 TCP 段最多能装多少应用数据
> - 标准以太网：MSS = 1500 - 20（IP头）- 20（TCP头）= **1460 字节**
> - UDP 无 MSS 概念，所以 UDP 应用中超过 **1472 字节**（1500 - 20 - 8）的数据需要在 IP 层分片

**MTU 不匹配的影响**：

当链路中某个节点的 MTU 小于发送端设定的 MTU 时，有两种后果：

| 场景 | 结果 |
|------|------|
| IP 分片被允许 | 大包被分片后传输，对端重组（降低性能） |
| IP 分片被禁止（DF=1） | 路由器返回 ICMP `Fragmentation Needed`，连接中断（常见于 VPN/隧道场景） |

```bash
# 测试路径 MTU（从本机到目标的最小 MTU）
ping -M do -s 1472 baidu.com    # -M do = 禁止分片，超过路径 MTU 会失败
# 如果成功，增大 -s 直到开始丢包
ping -M do -s 1500 baidu.com    # 很可能失败：1472 + IP头(20) + ICMP头(8) = 1500
```

> [!warning] VPN 和隧道场景下的 MTU 陷阱
> 当你使用 VPN（OpenVPN、WireGuard 等）时，额外的封装头部（如 IPsec、GRE 头）会减少有效 MTU。标准 MTU 1500 的包加上隧道头后超过链路 MTU，导致：
> 1. 包被分片（性能下降）
> 2. 如果 DF 标志被设置，连接直接中断
> **一个常见的排查步骤是**：`ping -M do -s 1472 baidu.com` 如果失败，说明路径上可能有 MTU 问题。

---

### 2. `ip link`：查看网卡状态

`ip link show` 是查看网络接口链路层信息的首选命令，没有任何替代品。它直接通过 netlink 从内核读取接口状态。

#### 2.1 基本用法

```bash
ip link show
```

输出示例：

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:ac:11:00:01 brd ff:ff:ff:ff:ff:ff
```

**关键字段解读**：

| 字段 | 含义 | 常见值 |
|------|------|--------|
| `state` | 接口运行状态 | `UP`/`DOWN`/`UNKNOWN`（loopback 常见） |
| `mtu` | 最大传输单元 | `1500`（以太网）/ `65536`（loopback） |
| `qdisc` | 排队规则（流量控制） | `pfifo_fast`/`noqueue`/`fq_codel` |
| `LOWER_UP` | 物理层已连接（电缆已插好/信号已建立） | 有则表示物理层就绪 |
| `NO-CARRIER` | 物理层未连接（网线未插/交换机未开机） | 没有物理信号 |
| `link/ether` | MAC 地址 | `52:54:00:12:34:56` |
| `brd` | 广播 MAC 地址 | `ff:ff:ff:ff:ff:ff` |

#### 2.2 状态标志解读

尖括号 `<...>` 中的标志描述了接口的当前状态和能力：

| 标志 | 含义 |
|------|------|
| `UP` | 接口已被启用（`ip link set dev eth0 up`） |
| `LOWER_UP` | 物理层已连接（网线插好且链路层有信号） |
| `BROADCAST` | 接口支持广播（以太网都支持） |
| `MULTICAST` | 接口支持多播（现代网卡都支持） |
| `NO-CARRIER` | 物理层断开（网线没插 / 对端设备关机） |

> [!note] `UP` 不等于 `LOWER_UP`
> 这是新手最常见的混淆点之一：
> - `state UP` = 我调用了 `ip link set dev eth0 up`，软件层面启动了接口
> - `LOWER_UP` = 物理连接正常（网线插好了，交换机在工作）
> - `NO-CARRIER` = 物理层断开（网线松了、交换机没电、对端端口 down）
> **如果看到 `state UP` 但 `NO-CARRIER`，说明软件配置正确，但物理连接有问题。**

#### 2.3 简洁模式（`-br`）

当你有多个接口时，完整模式的信息量太大。用 `-br`（brief）模式快速浏览：

```bash
ip -br link show
```

输出示例：

```
lo               UNKNOWN   00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eth0             UP        52:54:00:12:34:56 <BROADCAST,MULTICAST,UP,LOWER_UP>
docker0          DOWN      02:42:ac:11:00:01 <NO-CARRIER,BROADCAST,MULTICAST,UP>
```

简洁模式只有三列：**接口名、状态、MAC 地址**。一眼扫过就能判断哪些接口在线。

```bash
# 只看 UP 的接口
ip -br link show | grep UP

# 只看 DOWN 的接口
ip -br link show | grep DOWN

# 只看特定接口
ip -br link show eth0
```

> [!tip] 别名和重命名
> 生产环境中网卡名可能是 `enp0s3`、`ens33`、`eno1` 等系统化命名（systemd 的可预测命名规则）。如果你更习惯旧式的 `eth0`，可以用 `ip link` 重命名：
> ```bash
> ip link set dev enp0s3 down
> ip link set dev enp0s3 name eth0
> ip link set dev eth0 up
> ```

#### 2.4 指定接口查看

```bash
# 只看单个接口
ip link show dev eth0

# 只看 loopback
ip link show dev lo

# 只看特定类型（如 veth、bridge）
ip link show type bridge
```

---

### 3. `ip -s link`：收发统计信息

加上 `-s`（statistics）参数后，`ip link` 会显示每个接口的收发统计。这是排查网络丢包和性能问题的一线工具。

```bash
ip -s link show eth0
```

输出示例：

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
    RX:  bytes    packets errors dropped  missed   mcast
         1254789   10234   0      0       0       0
    TX:  bytes    packets errors dropped  carrier collsns
         987654     8765   0      0       0       0
```

**RX（接收）列解读**：

| 列 | 含义 | 正常值 | 异常排查 |
|----|------|--------|---------|
| `bytes` | 收到的字节数 | 持续增长 | — |
| `packets` | 收包数 | 持续增长 | — |
| `errors` | 接收错误（CRC 校验失败、帧对齐错误等） | **0** | >0 检查网线、网卡、交换机端口 |
| `dropped` | 内核丢包（ring buffer 满、内存不足） | **0 或极小** | >0 检查 `ethtool -S` ring buffer 溢出 |
| `missed` | 硬件丢包（网卡缓冲区满，未到达内核） | **0** | >0 表示网卡处理不过来 |

**TX（发送）列解读**：

| 列 | 含义 | 正常值 | 异常排查 |
|----|------|--------|---------|
| `errors` | 发送错误 | **0** | >0 检查网卡驱动、物理连接 |
| `dropped` | 发送丢包（队列满、带宽不足） | **0 或极小** | >0 检查 `qdisc` 溢出 |
| `carrier` | 载波丢失次数 | **0** | >0 物理连接不稳定 |
| `collsns` | 碰撞次数 | 交换机网络应为 **0** | >0 可能工作在半双工模式 |

#### 多次统计查看（变化增量）

```bash
# 第一次查看
ip -s link show eth0

# 间隔几秒后第二次查看，关注增量变化
# 或者交替使用 watch 监控
watch -n 2 'ip -s link show eth0'
```

> [!tip] `dropped` 不等于 `errors`
> `errors` 是硬件/物理层面的错误（坏帧、CRC 错），`dropped` 是内核主动丢弃（缓冲区满）。两者都不是 0 时排查方向不同：
> - `errors` > 0：排查**物理层**（网线、光模块、电磁干扰）
> - `dropped` > 0：排查**内核/驱动层**（增加 ring buffer、优化中断处理）

#### 更多 `-s` 获得更详细的统计

```bash
# 两个 -s：显示更详细的统计
ip -s -s link show eth0
```

---

### 4. `ip -j` JSON 输出：让脚本优雅地解析

`ip` 命令支持 `-j`（JSON）输出，这是它比 `ifconfig` 等旧工具领先的重要特性之一。结构化输出让脚本分析变得可靠且简洁。

#### 4.1 基础 JSON 输出

```bash
ip -j link show eth0
```

输出（经排版）：

```json
[
  {
    "ifindex": 2,
    "ifname": "eth0",
    "flags": ["BROADCAST","MULTICAST","UP","LOWER_UP"],
    "mtu": 1500,
    "qdisc": "pfifo_fast",
    "operstate": "UP",
    "carrier": 1,
    "address": "52:54:00:12:34:56",
    "broadcast": "ff:ff:ff:ff:ff:ff"
  }
]
```

对比文本输出要点解析，JSON 的优势一目了然：

| 需求 | 文本解析 | JSON 解析 |
|------|---------|-----------|
| 获取 MAC 地址 | 正则匹配 `link/ether` + 后续字段 | `.address` |
| 获取状态 | 正则匹配 `state UP` 或 `state DOWN` | `.operstate` |
| 判断是否 UP | 看 flags 中是否有 `UP` | `.flags[]` 包含 `"UP"` |
| 获取 MTU | 正则匹配 `mtu` 后数字 | `.mtu` |

#### 4.2 配合 `jq` 实战

`jq` 是 JSON 命令行解析器，可以做到精确提取和批量处理。

```bash
# 提取所有接口的名称和状态
ip -j link show | jq '.[] | {name: .ifname, state: .operstate, mac: .address}'
```

输出：

```json
{
  "name": "lo",
  "state": "UNKNOWN",
  "mac": "00:00:00:00:00:00"
}
{
  "name": "eth0",
  "state": "UP",
  "mac": "52:54:00:12:34:56"
}
{
  "name": "docker0",
  "state": "DOWN",
  "mac": "02:42:ac:11:00:01"
}
```

```bash
# 只看 UP 状态的接口（过滤）
ip -j link show | jq '.[] | select(.operstate == "UP") | .ifname'
```

输出：

```
"eth0"
"lo"
```

```bash
# 用 raw 输出去除引号，适合脚本赋值
ip -j link show | jq -r '.[] | select(.operstate == "UP") | .ifname'
```

输出：

```
eth0
lo
```

```bash
# 检查是否有接口在 DOWN 状态（告警检查）
if ip -j link show | jq -e '.[] | select(.operstate == "DOWN") | .ifname' > /dev/null; then
    echo "WARNING: 有网卡处在 DOWN 状态"
fi

# 获取 eth0 的 MTU
ip -j link show eth0 | jq -r '.[0].mtu'
# 输出: 1500
```

#### 4.3 带统计信息的 JSON

```bash
ip -j -s link show eth0
```

输出：

```json
[
  {
    "ifname": "eth0",
    "operstate": "UP",
    "address": "52:54:00:12:34:56",
    "stats64": {
      "rx": {
        "bytes": 1254789,
        "packets": 10234,
        "errors": 0,
        "dropped": 0
      },
      "tx": {
        "bytes": 987654,
        "packets": 8765,
        "errors": 0,
        "dropped": 0
      }
    }
  }
]
```

```bash
# 提取发送丢包率
ip -j -s link show eth0 | jq '.[0].stats64.tx.dropped / .[0].stats64.tx.packets * 100'
```

> [!tip] JSON 输出的三大使用场景
> 1. **监控告警脚本**：定期提取 `errors`/`dropped` 字段，超过阈值触发告警
> 2. **网络状态面板**：通过 `jq` 提取结构化数据，渲染到 Web Dashboard 或 Grafana
> 3. **自动化运维**：批量检查多台服务器的网卡状态，汇总统计

---

### 5. `ethtool`：网卡硬件信息与驱动查询

`ip link` 告诉你软件层面的状态，`ethtool` 则给你**硬件层面**的信息：网卡实际协商速率、驱动版本、硬件校验和卸载、ring buffer 大小等。

> [!note] ethtool 工作原理
> `ethtool` 通过 ioctl 系统调用直接与网卡驱动通信，读取或设置硬件参数。因此它能看到 `ip link` 看不到的底层信息。但部分功能需要 root 权限。

#### 5.1 基本参数查看

```bash
ethtool eth0
```

输出示例：

```
Settings for eth0:
    Supported ports: [ TP ]
    Supported link modes:   10baseT/Half 10baseT/Full
                            100baseT/Half 100baseT/Full
                            1000baseT/Full
    Supported pause frame use: No
    Supports auto-negotiation: Yes
    Advertised link modes:  1000baseT/Full
    Advertised pause frame use: No
    Advertised auto-negotiation: Yes
    Speed: 1000Mb/s
    Duplex: Full
    Auto-negotiation: on
    Port: Twisted Pair
    PHYAD: 0
    Transceiver: internal
    Auto-negotiation: on
    MDI-X: off (auto)
    Supports Wake-on: pumbg
    Wake-on: d
    Link detected: yes
```

**核心字段**：

| 字段 | 含义 | 健康值 |
|------|------|--------|
| `Speed` | 当前协商速率 | 应与交换机端口匹配（如 `1000Mb/s`） |
| `Duplex` | 双工模式：`Full` 或 `Half` | 现代网络应为 `Full` |
| `Auto-negotiation` | 自动协商状态 | 建议保持 `on` |
| `Link detected` | 物理链路状态 | `yes` = 正常；`no` = 网线未插/交换机端口 down |
| `Supported link modes` | 网卡支持的速率模式 | 用于确认网卡是否支持高级速率 |

> [!warning] 速率不匹配的后果
> 如果交换机端口强制设为 100Mbps，但网卡协商为 1000Mbps，虽然链路显示 UP 且 Link detected: yes，实际通信会：
> 1. 出现大量 CRC 错误（`ethtool -S eth0` 可看到）
> 2. 吞吐量急剧下降
> 3. 偶发连接超时
> **遇到"通了但很慢"时，先检查协商速率。**

#### 5.2 驱动信息

```bash
ethtool -i eth0
```

输出示例：

```
driver: virtio_net
version: 1.0.0
firmware-version:
expansion-rom-version:
bus-info: 0000:00:03.0
supports-statistics: yes
supports-test: no
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: no
```

| 字段 | 含义 | 使用场景 |
|------|------|---------|
| `driver` | 使用的网卡驱动名 | 排查驱动兼容性问题、确认模块是否加载 |
| `version` | 驱动版本 | 确认是否过旧、是否需要升级 |
| `firmware-version` | 网卡固件版本 | 高级场景（网卡厂商提供） |
| `bus-info` | PCI 总线位置 | 配合 `lspci` 定位物理设备 |

```bash
# 结合 lspci 确认物理网卡型号
lspci -s 0000:00:03.0 -v | grep -i ethernet
```

#### 5.3 网卡统计（硬件级统计）

这是比 `ip -s link` 更底层的统计，直接由网卡固件维护，部分数据 `ip` 命令读不到。

```bash
ethtool -S eth0
```

输出示例：

```
NIC statistics:
     rx_packets: 10234
     tx_packets: 8765
     rx_bytes: 1254789
     tx_bytes: 987654
     rx_broadcast: 234
     tx_broadcast: 189
     rx_multicast: 56
     tx_multicast: 43
     rx_crc_errors: 0          # ← CRC 错误（物理层噪声或网线问题）
     rx_frame_errors: 0        # ← 帧对齐错误
     rx_fifo_errors: 0         # ← FIFO 溢出（网卡处理不过来）
     tx_fifo_errors: 0
     rx_missed_errors: 0       # ← 硬件丢包（缓冲区满）
     tx_aborted_errors: 0
     tx_carrier_errors: 0      # ← 载波错误（物理连接不稳定）
```

不同驱动的统计字段名不统一，但常见的异常字段包括：

| 统计字段关键字 | 含义 | 排查方向 |
|--------------|------|---------|
| `crc_error` / `fcs_error` | CRC 校验错 | 网线质量问题、电磁干扰 |
| `fifo_overflow` / `fifo_error` | FIFO 缓冲区满 | 网卡处理能力不足、中断绑定问题 |
| `missed` | 硬件丢包（未到内核） | ring buffer 太小 (`ethtool -g eth0`) |
| `collision` / `collision_count` | 冲突计数 | 检查是否运行在半双工模式 |

#### 5.4 其他有用子命令

```bash
# 查看 ring buffer 大小（接收/发送队列深度）
ethtool -g eth0

# 查看网卡支持的功能（硬件 offload 能力）
ethtool -k eth0

# 查看网卡连接的交换机端口信息（需要交换机支持 LLDP）
ethtool --show-peer eth0
```

> [!tip] 调整 ring buffer 缓解丢包
> 如果 `ip -s link` 显示 `dropped` 非零，且 `ethtool -S` 看到 `rx_missed_errors`，可以尝试增大 ring buffer：
> ```bash
> ethtool -G eth0 rx 4096 tx 4096
> ```
> 这会让网卡有更大的缓冲区来应对流量突发。注意：增大 ring buffer 会增加内存占用。

---

### 6. 常见链路层问题排查

#### 6.1 网卡 DOWN 且 LOWER_UP 不存在

```bash
ip link show eth0
# 输出: <BROADCAST,MULTICAST> ... state DOWN
```

**排查步骤**：

```bash
# 1. 确认物理连接
ethtool eth0 | grep "Link detected"
# 期望: Link detected: yes

# 2. 如果没有物理连接，检查网线和交换机端口指示灯
# 3. 如果物理连接正常，尝试软件启用
sudo ip link set dev eth0 up

# 4. 再次确认
ip -br link show eth0
```

#### 6.2 MTU 不匹配

症状：大文件传输超时或极慢，小包正常。

```bash
# 检查 MTU
ip link show eth0 | grep mtu

# 测试路径 MTU（禁止分片，发送 1500 字节 ICMP）
ping -M do -s 1472 192.168.1.1
# -M do = 设置 DF 标志（Don't Fragment）
# -s 1472 = ICMP 数据部分，加 IP头(20) + ICMP头(8) = 1500 总大小

# 如果失败，减小 -s 直到成功
ping -M do -s 1400 192.168.1.1
```

**常见 MTU 异常场景**：

| 场景 | 典型 MTU | 原因 |
|------|---------|------|
| 标准以太网 | 1500 | — |
| PPPoE（宽带拨号） | 1492 | PPPoE 头占用 8 字节 |
| VPN（OpenVPN） | 1400-1450 | 加密/封装头额外开销 |
| VXLAN | 1450 | VXLAN 头 50 字节 |
| Jumbo Frame（数据中心） | 9000 | 需要两端交换机同时支持 |

#### 6.3 协商速率异常

```bash
# 确认当前协商速率
ethtool eth0 | grep Speed
# Speed: 100Mb/s   ← 如果是千兆网卡，可能有问题

# 查看网卡和交换机都支持的速率
ethtool eth0 | grep "Supported link modes"
ethtool eth0 | grep "Advertised link modes"
```

如果千兆网卡只协商到 100Mbps：
1. **网线质量**：使用 Cat5e 或 Cat6 线缆
2. **交换机端口**：确认交换机端口支持 1000Mbps
3. **端口模式**：两端都设为 auto-negotiation（不要强制设置一侧而另一侧 auto）

> [!warning] 不要强制设置速率
> ```bash
> # 以下操作可能让网卡"聋掉"——链路状态 UP 但实际不通
> sudo ethtool -s eth0 speed 1000 duplex full autoneg off
> ```
> 强制设置速率仅在两端配置一致时才有效。生产环境中，**始终使用自动协商**。现代驱动在某些情况下可能不支持强制模式，或导致链接协商失败。

#### 6.4 网卡丢包排查流程

```
看到 ip -s link 中 dropped > 0
│
├─ 检查 ethtool -g 的 ring buffer 当前值
│  └─ 如果当前值较小（如 256），尝试增加到 4096
│
├─ 检查 ethtool -S 中 rx_missed_errors 是否增长
│  └─ 是 → 硬件缓冲区溢出，增大 ring buffer 或升级网卡
│
├─ 检查 cat /proc/net/softnet_stat 的第三列
│  └─ > 0 → CPU 软中断处理不过来，考虑 RPS (Receive Packet Steering)
│
└─ 检查系统内存压力
   └─ free -h 确认不是内存不足导致内核无法分配 skb
```

---

### 本章小结

- **MAC 地址是网卡的链路层标识**（48 位），在同一广播域内有效；`ip link show` 以 `link/ether` 字段显示
- **MTU 决定单帧最大数据量**（以太网默认为 1500），通过 `ping -M do -s` 可测试路径 MTU；VPN 和隧道场景中 MTU 是常见坑
- **`ip link show` 是最核心的链路层查询命令**：
  - `-br` 简洁模式快速浏览所有接口状态
  - `-s` 显示收发统计（重点关注 `errors` 和 `dropped`）
  - 状态标志中 `UP` 不等于 `LOWER_UP`，后者才代表物理连接正常
- **`ip -j link show` JSON 输出 + `jq` 解析**：结构化数据比文本解析更可靠、更易维护，适合监控脚本和自动化
- **`ethtool` 提供硬件级视角**：查看协商速率、驱动版本、CRC 错误、ring buffer 大小。`ethtool -S` 的硬件统计比 `ip -s` 更底层
- **常见链路层问题**：网卡 DOWN 排查物理和软件两层、MTU 不匹配用 `ping -M do` 诊断、协商速率异常先检查网线再检查交换机端口

#### 下章预告

链路层搞定后，下一章将往上走一层——**IP 地址与子网信息**。你将学到 IPv4 地址的 32 位结构、子网掩码与 CIDR 表示法的对应关系、特殊地址（loopback / link-local / 私有地址），以及 `ip addr show` 命令的全部用法——包括简洁模式、scope 解读、动态/静态标志、JSON 输出配合 `jq` 的进阶技巧。

---

---

## 第三章：IP 地址与子网信息

如果说 MAC 地址是网卡的"身份证"，那 IP 地址就是它在网络中的"门牌号"。没有 IP，数据包就不知道该往哪送——这个门牌号是怎么编排的，Linux 上又该怎么查，就是本章要回答的问题。

---

### IP 地址核心概念

#### 32 位结构的真相

IPv4 地址由 32 个比特（bit）组成，通常写作点分十进制格式（如 `192.168.1.100`）。但这四个数字并不是平等的——它们被划分为**网络位**和**主机位**两部分：

```
点分十进制：  192  .  168  .   1   .  100
二进制：      11000000  10101000  00000001  01100100
              ├─────────── 网络位 ───────────┤── 主机位 ─┤
```

- **网络位**：标识这个地址属于哪个网络（哪个小区）
- **主机位**：标识在这个网络中是哪台设备（哪栋楼）

> [!note] 关键认知
> 判断两个 IP 是否在同一网络，不是看它们数字上是否接近，而是看它们的网络位是否相同。`192.168.1.100` 和 `192.168.1.200` 如果网络位都是 24 位，它们就在同一网络；`192.168.2.100` 则不在。

#### 网络位 vs 主机位的分界线

分界线由**子网掩码**决定——这个问题下节展开。先记住结论：**没有子网掩码的 IP 地址是没有意义的**。

---

### 子网掩码与 CIDR

#### 子网掩码的本质

子网掩码（Subnet Mask）是一个 32 位数，**高位连续为 1 表示网络位，低位为 0 表示主机位**：

```
子网掩码：  255  .  255  .  255  .   0
二进制：    11111111  11111111  11111111  00000000
            ├────────── 24个1 ──────────┤── 8个0 ─┤
            └── 网络位（24位）──┘   主机位（8位）
```

`255.255.255.0` 告诉系统："前 24 位是网络部分，后 8 位是主机部分"。在这个网络上，最多可以有 `2^8 - 2 = 254` 台设备（全 0 和全 1 保留）。

#### CIDR 表示法

CIDR（Classless Inter-Domain Routing）是子网掩码的简写形式，直接在 IP 后面加 `/` 和网络位数：

| CIDR | 子网掩码 | 可用主机数 | 常见用途 |
|------|---------|-----------|---------|
| `/8` | `255.0.0.0` | 16,777,214 | 大型网络（如 10.0.0.0/8） |
| `/16` | `255.255.0.0` | 65,534 | 中型网络（如 192.168.0.0/16） |
| `/24` | `255.255.255.0` | 254 | 最常见——家庭/小企业局域网 |
| `/25` | `255.255.255.128` | 126 | 子网划分 |
| `/30` | `255.255.255.252` | 2 | 点对点链路（刚好两个地址） |
| `/32` | `255.255.255.255` | 1 | 单个主机（常用在路由规则中） |

> [!tip] 快速计算主机数
> 主机位数 = 32 - 网络位数，可用地址数 = 2^主机位数 - 2（减掉网络地址和广播地址）。
>
> 例如 `/24`：32 - 24 = 8 位主机，2^8 - 2 = 254。

#### 在 Linux 上验证子网掩码

```bash
# 查看 IP 和子网掩码（CIDR 形式）
ip addr show eth0

# 输出示例（只关注 inet 行）：
# inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
#      ^^^^^^^^^^^^^^^^                       ^^^^^^^^^
#      IP/CIDR                                broadcast 地址
```

`/24` 就是子网掩码 `255.255.255.0` 的 CIDR 形式。Linux 上 `ip addr` 的所有输出都默认用 CIDR，不显示点分十进制掩码。

---

### 特殊 IP 地址

不是所有 IP 都用来标识一台具体的设备。以下几类地址有特殊含义。

#### Loopback（回环地址）

```
127.0.0.0/8    整个 127 段都留给本机回环
127.0.0.1      最常用的回环地址（localhost）
```

- 发往 `127.0.0.1` 的数据包**不会离开本机**，内核直接回环到本机接收
- 用于测试本机网络栈是否正常：`ping 127.0.0.1`
- 也用于本地服务绑定（开发时常用 `127.0.0.1` 只允许本机访问）

```bash
# 测试本机网络栈
ping -c 1 127.0.0.1

# 正常输出（说明网络栈工作正常）：
# 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.03 ms
```

#### Link-Local（链路本地地址）

```
169.254.0.0/16    DHCP 分配失败时的备用地址
```

- 当 DHCP 客户端无法获取 IP 时，系统自动分配一个 `169.254.x.x` 地址
- 允许同一链路内的设备在没有 DHCP 服务器的情况下通信
- **出现 `169.254.x.x` 通常意味着 DHCP 故障**——这是排查时的红色警报

```bash
# 如果看到这样的输出，说明 DHCP 有问题
ip -br addr show eth0
# eth0             UP             169.254.12.34/16 ...
```

#### 私有地址范围

私有地址（Private IP）用于局域网内部，**不会在互联网上路由**。NAT 路由器负责将私有地址映射为公网地址。

| RFC 1918 范围 | CIDR | 地址数 | 常见场景 |
|--------------|------|-------|---------|
| `10.0.0.0` - `10.255.255.255` | `10.0.0.0/8` | 16,777,216 | 大型企业内网、Kubernetes 集群 |
| `172.16.0.0` - `172.31.255.255` | `172.16.0.0/12` | 1,048,576 | 中型网络（AWS VPC 默认） |
| `192.168.0.0` - `192.168.255.255` | `192.168.0.0/16` | 65,536 | 家庭/办公室路由器最常见 |

> [!warning] 常见误解
> 私有地址不等于"内网地址"。严格来说，"私有"是地址性质（不在互联网路由），"内网"是网络范围（局域网）。私有地址一定在内网使用，但内网也可以使用公网地址（虽然很少这么干）。

#### 其他特殊地址

| 地址 | 用途 |
|------|------|
| `0.0.0.0/0` | 默认路由，匹配所有地址 |
| `0.0.0.0/8` | 表示"本网络"（通常用于 DHCP 请求时的源地址） |
| `255.255.255.255` | 有限广播地址（只在本链路广播） |
| `224.0.0.0/4` | 组播地址范围 |
| `240.0.0.0/4` | 保留地址（未来使用） |

---

### `ip addr` 命令详解

`ip addr` 是查询 IP 配置的标准命令，属于 `iproute2` 工具集。它的功能等价于旧的 `ifconfig`，但输出更清晰、信息更完整。

#### 基础用法

```bash
# 查看所有接口的 IP 配置
ip addr show

# 查看指定接口
ip addr show eth0

# 只查看 IPv4
ip -4 addr show

# 只查看 IPv6
ip -6 addr show
```

#### 输出逐字段解读

执行 `ip addr show eth0`，典型的输出是这样的：

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
       valid_lft 86342sec preferred_lft 86342sec
    inet6 fe80::5054:ff:fe12:3456/64 scope link
       valid_lft forever preferred_lft forever
```

逐行解读：

**第 1 行 — 接口概要**

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
```

| 字段 | 含义 | 说明 |
|------|------|------|
| `2:` | 接口索引号 | 内核分配的编号（与 `/sys/class/net/` 对应） |
| `eth0` | 接口名称 | 可以在 `/etc/systemd/network/` 或 udev 规则中改名 |
| `BROADCAST` | 支持广播 | 以太网接口通常都有 |
| `MULTICAST` | 支持组播 | 几乎所有接口都有 |
| `UP` | 管理状态 UP | 管理员通过 `ip link set eth0 up/down` 控制 |
| `LOWER_UP` | 物理链路正常 | 网线插着、交换机端口开启了 |
| `mtu 1500` | MTU 值 | 最大传输单元，默认 1500 字节 |
| `state UP` | 接口状态 | UP（正常）或 DOWN（关闭） |

> [!tip] state UP vs LOWER_UP
> `state UP` 表示管理员开启了接口；`LOWER_UP` 表示物理链路正常。如果看到 `state UP` 但没有 `LOWER_UP`，说明网线没插好或对端设备断电了。

**第 2 行 — 链路层信息（L2）**

```
link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
```

| 字段 | 含义 |
|------|------|
| `link/ether` | 链路层类型（以太网） |
| `52:54:00:12:34:56` | MAC 地址 |
| `brd ff:ff:ff:ff:ff:ff` | 广播地址（全 F 是标准以太网广播） |

**第 3-4 行 — 网络层信息（L3），IPv4**

```
inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
   valid_lft 86342sec preferred_lft 86342sec
```

| 字段 | 含义 | 说明 |
|------|------|------|
| `inet` | IPv4 地址标识 | `inet6` 是 IPv6 |
| `192.168.1.100/24` | IP 地址 + CIDR 前缀 | `/24` 即子网掩码 `255.255.255.0` |
| `brd 192.168.1.255` | 广播地址 | 该子网的广播地址（主机位全 1） |
| `scope global` | 作用域 | 见下方 scope 详解 |
| `dynamic` | 地址来源 | `dynamic` = DHCP，没有此标记 = 静态配置 |
| `eth0` | 地址所属接口 | 辅助接口名（主要针对 secondary 地址） |
| `valid_lft` / `preferred_lft` | 地址有效期 | DHCP 获取的地址有租约时间 |

**第 5 行 — IPv6 地址**

```
inet6 fe80::5054:ff:fe12:3456/64 scope link
   valid_lft forever preferred_lft forever
```

`fe80::/10` 是 IPv6 的链路本地地址，相当于 IPv4 的 `169.254.0.0/16` 但功能更正式。

#### Scope（作用域）详解

scope 表示这个地址的**有效范围**。这是理解 IP 配置的一个关键概念：

| Scope | 含义 | 常见地址 | 说明 |
|-------|------|---------|------|
| `global` | 全局可用 | `192.168.1.100/24` | 可以跨网络通信（默认） |
| `link` | 仅限同一链路 | `169.254.x.x/16` | 只能在直连的局域网内通信，不跨路由 |
| `host` | 仅限本机 | `127.0.0.1/8` | 只能在本机内通信，不发送到网络 |
| `site` | 仅限站点内 | IPv6 站点地址 | IPv6 专用，IPv4 基本不用 |

理解 scope 有助于解释一些看似奇怪的现象：

```bash
# 场景：为什么 ping 127.0.0.1 通，但 ssh 127.0.0.1 也可能通？
# 答：127.0.0.1 scope 是 host，数据包不会离开本机。内核直接回环。

# 场景：为什么 169.254.x.x 能通但连不上外网？
# 答：scope 是 link，路由器不会转发这些地址的流量。
```

#### 动态地址 vs 静态地址

```bash
# 动态地址（DHCP 获取）—— 行内有 dynamic 标记
inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0

# 静态地址（手动配置）—— 没有 dynamic 标记
inet 10.0.0.5/24 brd 10.0.0.255 scope global eth0
```

DHCP 获取的地址还有有效期（`valid_lft`），过期后会自动释放。静态配置的地址默认永不过期。

#### 简洁模式（`-br`）

```bash
# 简洁模式——适合快速查看
ip -br addr show

# 输出示例：
# lo               UNKNOWN        127.0.0.1/8
# eth0             UP             192.168.1.100/24 10.0.0.5/24
# wlan0            DOWN
```

三列：接口名称 | 状态 | IP 地址列表（逗号分隔）。一眼就能看出哪个接口有 IP、哪个没有。

#### JSON 模式（`-j`）

```bash
# JSON 输出——适合脚本解析
ip -j addr show eth0
```

输出示例（简化为可读格式）：

```json
[
  {
    "ifindex": 2,
    "ifname": "eth0",
    "flags": ["BROADCAST","MULTICAST","UP","LOWER_UP"],
    "mtu": 1500,
    "qdisc": "fq_codel",
    "operstate": "UP",
    "link_type": "ether",
    "address": "52:54:00:12:34:56",
    "broadcast": "ff:ff:ff:ff:ff:ff",
    "addr_info": [
      {
        "family": "inet",
        "local": "192.168.1.100",
        "prefixlen": 24,
        "broadcast": "192.168.1.255",
        "scope": "global",
        "dynamic": true,
        "label": "eth0",
        "valid_life_time": 86342,
        "preferred_life_time": 86342
      },
      {
        "family": "inet6",
        "local": "fe80::5054:ff:fe12:3456",
        "prefixlen": 64,
        "scope": "link"
      }
    ]
  }
]
```

JSON 输出的优势：
- 字段命名规范，容易理解和记忆
- 布尔值（`dynamic: true`）而不是"有这个关键词存在 / 不存在"
- 数值（`prefixlen: 24`）而不是文本 `/24`
- 结构稳定，不依赖文本行顺序

---

### `ip -j` + jq 脚本化获取 IP

#### 安装 jq

```bash
# Ubuntu/Debian
apt install jq -y

# 验证
jq --version
# jq-1.7.1
```

jq 是处理 JSON 的首选命令行工具。结合 `ip -j`，可以精确、可靠地提取任意网络信息。

#### 常用脚本模式

##### 获取指定接口的 IPv4 地址

```bash
# 获取 eth0 的 IPv4 地址
ip -j addr show eth0 | jq -r '.[0].addr_info[] | select(.family == "inet") | .local'

# 输出：192.168.1.100
```

逐段解析这个 jq 表达式：

| 部分 | 含义 |
|------|------|
| `.[0]` | 取出数组的第一个元素（eth0 的信息） |
| `.addr_info[]` | 遍历地址信息数组 |
| `select(.family == "inet")` | 只选 IPv4 |
| `.local` | 提取 IP 地址 |

##### 获取所有接口的 IP（不含 loopback）

```bash
# 列出所有非 lo 接口的 IPv4 地址
ip -j addr show | jq -r '
  .[] | select(.ifname != "lo") |
  .ifname as $if |
  .addr_info[] | select(.family == "inet") |
  "\($if): \(.local)/\(.prefixlen)"
'

# 输出示例：
# eth0: 192.168.1.100/24
# eth0: 10.0.0.5/24
# docker0: 172.17.0.1/16
```

##### 检查地址是否为 DHCP

```bash
# 列出所有 DHCP 获取的 IPv4 地址
ip -j addr show | jq -r '
  .[] | select(.ifname != "lo") |
  .ifname as $if |
  .addr_info[] | select(.family == "inet" and .dynamic == true) |
  "\($if): \(.local)/\(.prefixlen) (DHCP)"
'

# 输出示例：
# eth0: 192.168.1.100/24 (DHCP)
```

##### 获取默认接口的 IP（自动选择有默认路由的接口）

```bash
# 更实用的方式：从路由表反推默认接口
ip -j route show default | jq -r '.[0].dev' | xargs -I {} ip -j addr show {} | \
  jq -r '.[0].addr_info[] | select(.family == "inet") | .local'

# 输出：192.168.1.100
```

这个模式比固定写 `eth0` 更健壮——如果你的机器叫 `ens33` 或 `enp0s3`，一样能正确拿到 IP。

#### 封装为可复用函数

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
get_ip() {
  local iface="${1:-$(ip -j route show default | jq -r '.[0].dev')}"
  ip -j addr show "$iface" | jq -r '.[0].addr_info[] | select(.family == "inet") | .local'
}

get_ip_all() {
  ip -j addr show | jq -r '
    .[] | select(.ifname != "lo") |
    .ifname as $if |
    .addr_info[] | select(.family == "inet") |
    "\($if): \(.local)/\(.prefixlen)"
  '
}

# 使用：
# get_ip            # 默认接口的 IP
# get_ip eth0       # 指定接口的 IP
# get_ip_all        # 所有接口的 IP
```

---

### 常见坑

#### 坑 1：多个 IP 的优先级

一个接口可以有多个 IP 地址。当本机发起对外连接时，系统如何选择源地址？

```bash
# 假设 eth0 配置了两个 IP
ip addr show eth0
# inet 192.168.1.100/24 scope global eth0
# inet 10.0.0.5/24 scope global eth0
```

规则：**默认选择目标网络内的高优先级 IP**（优先级由路由表的最长前缀匹配决定）。如果目标在 `192.168.1.0/24` 内，源地址选 `192.168.1.100`；如果目标在 `10.0.0.0/24` 内，选 `10.0.0.5`。

```bash
# 看实际选择
ip route get 8.8.8.8
# 8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.100 uid 1000
#                                               ^^^^^^^^^^^^^^ 源地址选了哪个
```

如果对源地址有明确要求，用 `ip route get` 模拟，或者用 `ping -I 10.0.0.5 8.8.8.8` 指定源地址。

#### 坑 2：Secondary 地址

当同网段有两个 IP 时，后面的会被标记为 `secondary`：

```bash
ip addr show eth0
# inet 192.168.1.100/24 scope global eth0       # primary
# inet 192.168.1.200/24 scope global secondary eth0  # secondary
```

Secondary 地址的特殊行为：
- **不会用作对外连接的源地址**（只有 primary 地址被使用）
- **如果 primary 被删除，第一个 secondary 自动晋升**为 primary
- 删除 primary 会导致所有同网段 secondary 被删除

```bash
# 演示 secondary 晋升
# 删除 primary
ip addr del 192.168.1.100/24 dev eth0

# 再次查看——原来的 secondary 变成 primary
ip addr show eth0
# inet 192.168.1.200/24 scope global eth0    # 自动晋升
```

#### 坑 3：`ifconfig` vs `ip addr` 信息不一致

```bash
# ifconfig 可能不显示某些地址
ifconfig eth0       # 可能只显示第一个 IP
ip addr show eth0   # 显示所有 IP
```

`ifconfig` 本质上通过 `ioctl` 读取内核数据，某些场景会漏掉地址。`ip addr` 通过 `netlink` 读取，始终完整。

#### 坑 4：`scope host` 的地址 ping 不通其他机器

```bash
# 像这样的地址只能本机用
inet 127.0.0.1/8 scope host lo
```

如果在某个接口上看到 `scope host` 的非 127 地址，记得这是**只能本机内部通信**的地址，其他机器无法访问。

---

### 本章小结

- **IPv4 地址 = 32 位二进制，分为网络位 + 主机位**，分界线由子网掩码决定
- **CIDR 表示法**（如 `/24`）是子网掩码的简写，`/24` = `255.255.255.0`，可用 254 个地址
- **特殊地址要牢记**：`127.0.0.0/8`（回环）、`169.254.0.0/16`（DHCP 失败）、私有地址三段（10/172.16/192.168）
- **`ip addr show` 输出核心字段**：`inet`（IP/CIDR）、`scope`（作用域）、`dynamic`（DHCP 标记）
- **`ip -br addr show` 简洁模式 + `ip -j addr show` JSON 模式**覆盖人类阅读和脚本解析两大场景
- **`ip -j` + `jq` 可以精确提取 IP 信息**，比解析文本更可靠
- **注意 secondary 地址优先级和 scope 含义**，避免配置误解

#### 下章预告

IP 配好了，数据包怎么知道下一步往哪里送？这就是**路由表**的工作。下一章我们学 `ip route`——查看路由表、理解默认网关、模拟路由决策，并解决"为什么上不了网"这类最常见问题。

---

---

## 第四章：路由表信息

### 引子：数据包出了本机，下一步去哪？

上一章我们学会了查看 IP 地址，知道了本机在哪个网段。但数据包要发送到另一个网络（比如访问 `8.8.8.8`），它出了本机网卡之后该往哪走？答案是 **路由表**。

> 一句话定义：路由表是内核中用于决定"数据包下一步去哪"的规则集合。每一条规则称为一个"路由条目"。

> [!note] 为什么需要路由表？
> 一台 Linux 机器可能有多个网卡（eth0、eth1、wlan0），连接着不同的网络。当数据包从本机发出时，内核必须决定：扔给 eth0 还是 eth1？交给哪个下一跳（gateway）？路由表就是做这个决策的。

---

### 路由表核心概念

#### 路由条目三要素

每条路由条目本质上回答三个问题：

| 要素 | 含义 | 示例 |
|------|------|------|
| **目的网络** | 这个路由匹配哪些目标 | `192.168.1.0/24`、`default`（即 `0.0.0.0/0`） |
| **下一跳** | 数据包交给谁（via） | `via 192.168.1.1` |
| **出接口** | 从哪个网卡出去（dev） | `dev eth0` |

#### 三种路由来源

根据路由是如何产生的，可以分为三类：

**1. 直连路由（Directly Connected）**

当给网卡配置 IP 地址时，内核自动添加对应网段的路由。

```bash
# 给 eth1 配置 10.0.0.1/24 后，内核自动添加：
# 10.0.0.0/24 dev eth1 proto kernel scope link src 10.0.0.1 metric 101
```

特征：`proto kernel` 表示由内核自动管理，`scope link` 表示目标在本链路内（不需要经过网关）。

> [!tip] scope link 的含义
> `scope link` 表示目标 IP 和本机在同一个二层网络（同一个广播域），数据包不需要经过路由器转发，直接通过 ARP 获取对端 MAC 地址后发送。

**2. 静态路由（Static Route）**

由管理员手动添加，用于引导特定网段走向特定下一跳。

```bash
# 手动添加一条到 172.16.0.0/16 网段的路由
ip route add 172.16.0.0/16 via 192.168.1.254 dev eth0
```

特征：`proto static`，系统重启后消失（除非写入配置文件）。

**3. 动态路由（Dynamic Route）**

由路由协议守护进程（如 BGP、OSPF）通过动态交换路由信息自动学习。在企业路由器和复杂网络中常见，日常 Linux 桌面/服务器环境下较少出现。

#### 默认路由

默认路由是路由表的"兜底"规则。当数据包的目标地址不匹配任何更具体的路由时，就走默认路由。

```bash
# 两种写法等价
default via 192.168.1.1 dev eth0
0.0.0.0/0 via 192.168.1.1 dev eth0
```

> `0.0.0.0/0` 的意思：网络位 0 位，主机位 32 位，即"匹配所有地址"。

没有默认路由，就无法访问互联网（除非你的目标恰好在一个直连网段内）。这是最常见的网络故障原因之一。

---

### 最长前缀匹配规则

当有多个路由条目都能匹配同一个目标 IP 时，内核如何选择？

**规则很简单：前缀越长（掩码越精确），优先级越高。**

#### 工作原理

```
路由表：
  10.0.0.0/8      via 10.0.0.1
  10.0.1.0/24     via 10.0.1.1
  0.0.0.0/0       via 192.168.1.1  (默认路由)

目标 10.0.1.5 → 匹配 /8、/24、/0 → 最长前缀是 /24 → 走 10.0.1.1
目标 10.0.2.5 → 匹配 /8、/0     → 最长前缀是 /8  → 走 10.0.0.1
目标 8.8.8.8  → 只匹配 /0       → 走默认路由 192.168.1.1
```

> [!note] 最长前缀匹配 vs 路由度量
> 注意区分：最长前缀匹配（掩码长度）是第一优先级，**路由度量（metric）** 是第二优先级。只有当两条路由的**前缀长度完全相同时**，才会比较 metric，metric 越小越优先。

#### 为什么要这样设计？

这种设计让管理员可以"先粗后细"地规划路由：

- 用大网段（如 `/8`）兜底一个大区域
- 用小网段（如 `/24`）覆盖区域内的特例
- 用 `/32` 覆盖单台主机的特殊策略

---

### `ip route show` 详解

`ip route show` 是查看路由表的命令。它的输出格式虽然一眼看上去复杂，但每个字段都有明确的含义。

#### 基本输出解读

```bash
$ ip route show
default via 192.168.1.1 dev eth0 proto dhcp metric 100
10.0.0.0/24 dev eth1 proto kernel scope link src 10.0.0.1 metric 101
172.16.0.0/16 via 192.168.1.254 dev eth0 proto static metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 metric 100
```

逐行解读：

| 行 | 目的网络 | 下一跳 | 出接口 | 来源 | 作用域 | 源地址 | Metric |
|----|---------|-------|--------|------|--------|-------|--------|
| 1 | `default` | `via 192.168.1.1` | `dev eth0` | `proto dhcp` | 无 | 无 | `metric 100` |
| 2 | `10.0.0.0/24` | 无（直连） | `dev eth1` | `proto kernel` | `scope link` | `src 10.0.0.1` | `metric 101` |
| 3 | `172.16.0.0/16` | `via 192.168.1.254` | `dev eth0` | `proto static` | 无 | 无 | `metric 100` |
| 4 | `192.168.1.0/24` | 无（直连） | `dev eth0` | `proto kernel` | `scope link` | `src 192.168.1.100` | `metric 100` |

**字段详解：**

- **`default` / `0.0.0.0/0`**：目的网络。`default` 是 `0.0.0.0/0` 的简写，匹配所有地址。
- **`via <IP>`**：下一跳网关。数据包要交给这个 IP 地址。只在跨网段时出现。
- **`dev <interface>`**：出接口。数据包从哪个网卡出去。
- **`proto <source>`**：路由来源。`kernel` = 内核自动添加，`dhcp` = DHCP 分配，`static` = 手动添加，`boot` = 启动时加载。
- **`scope <scope>`**：路由作用域。`link` = 直连链路（无网关），`global` = 全局（默认值，不显示）。
- **`src <IP>`**：本机访问该网段时默认使用的源 IP 地址。内核自动从接口 IP 中选择。
- **`metric <value>`**：路由度量。值越小优先级越高，同前缀长度时比较 metric。

#### 常用变体

```bash
# 只看默认路由（最常用）
ip route show default

# 只看某个网卡上的路由
ip route show dev eth0

# 只看某个网段的路由
ip route show 192.168.1.0/24

# JSON 输出（适合脚本解析）
ip -j route show
```

**JSON 输出示例：**

```json
[
  {
    "dst": "default",
    "gateway": "192.168.1.1",
    "dev": "eth0",
    "protocol": "dhcp",
    "metric": 100
  },
  {
    "dst": "192.168.1.0/24",
    "dev": "eth0",
    "protocol": "kernel",
    "scope": "link",
    "prefsrc": "192.168.1.100",
    "metric": 100
  }
]
```

> [!tip] 与旧版 `route -n` 对比
> 旧版 `route -n` 的输出缺少 metric 和 proto 字段，且无法区分路由来源。在排查"为什么这个路由不生效"时，`ip route show` 提供的额外信息经常是关键线索。

---

### `ip route get`：模拟路由决策

这是排查路由问题时**最实用的命令**。它不发送任何数据包，而是模拟内核为某个目标 IP 做路由决策的过程，直接告诉你"如果发这个包，会走哪条路"。

#### 基本用法

```bash
$ ip route get 8.8.8.8
8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.100 uid 1000
```

输出解读：

| 字段 | 含义 |
|------|------|
| `8.8.8.8` | 目标地址 |
| `via 192.168.1.1` | 下一跳网关（匹配了默认路由） |
| `dev eth0` | 从 eth0 出去 |
| `src 192.168.1.100` | 本机使用的源 IP 地址 |
| `uid 1000` | 发起查询的进程 UID（默认显示当前用户） |

#### 实战场景

**场景 1：确认某台内网机器走哪条路由**

```bash
$ ip route get 10.0.1.50
10.0.1.50 via 192.168.1.254 dev eth0 src 192.168.1.100 uid 0
```

返回结果表示 10.0.1.50 走的是静态路由（`via 192.168.1.254` 那条 `172.16.0.0/16`），但这里有蹊跷——`10.0.1.50` 并不在 `172.16.0.0/16` 范围内。那它匹配的是哪条路由？

其实 `10.0.1.50` 也可能匹配了默认路由。关键是要理解：`ip route get` 返回的是**实际匹配的路由条目**，而不是你认为"应该"匹配的。这正是它的价值所在。

**场景 2：指定源 IP 测试**

```bash
$ ip route get 8.8.8.8 from 10.0.0.1
8.8.8.8 from 10.0.0.1 via 10.0.0.254 dev eth1 table 100 uid 0
```

从 `10.0.0.1`（eth1）出发访问 `8.8.8.8` 时，走了 `table 100`（策略路由），出接口是 `eth1`。这说明这台机器配置了多路由表策略。

**场景 3：模拟数据包到达本机时的路由决策**

```bash
$ ip route get 192.168.1.100 from 10.0.0.5 iif eth1
192.168.1.100 from 10.0.0.5 dev eth0 table local src 192.168.1.100 uid 0
    cache
```

`iif eth1` 模拟数据包从 eth1 进入本机，目标地址是 `192.168.1.100`。结果匹配了 `table local`，说明这个包是发给本机的。

#### 与 `ping` 对比

| 场景 | `ping` | `ip route get` |
|------|-------|---------------|
| 能否路由 | 需实际发包 | 模拟决策，不发送任何包 |
| 是否受防火墙影响 | 会被过滤 | 不受影响 |
| 是否能看源 IP 选择 | 需抓包查看 | 直接显示 |
| 风险 | 可能触发 ICMP 限速 | 零风险 |

> [!warning] 重要区分
> `ip route get` 模拟的是**本机发出的数据包**的路由决策。对于"经过本机转发的数据包"（即本机作为路由器），情况更复杂，涉及反向路径过滤（rp_filter）等多重机制。日常排查中，`ip route get` 覆盖了 90% 的场景。

---

### 策略路由：`ip rule` 与多路由表

默认情况下，所有路由条目都在 `main` 表中，内核只根据**目标 IP 地址**做路由决策。但在有些场景下，我们需要更灵活的路由策略：

- 从 eth1 进来的数据包走一条出口，从 eth0 进来的走另一条
- 某些应用通过特定出口上网
- 根据防火墙标记走不同的路由路径

#### 多路由表机制

Linux 支持多张路由表，每张表独立管理自己的路由条目。常用的表有：

```bash
$ cat /etc/iproute2/rt_tables
# reserved values
255     local
254     main
253     default
0       unspec
```

| 表名 | 编号 | 用途 |
|------|------|------|
| `local` | 255 | 本地路由（广播、多播、本机 IP），由内核管理，**不要手动修改** |
| `main` | 254 | 主路由表，日常 `ip route show` 看到的就是这个表 |
| `default` | 253 | 默认路由表，通常为空，保留给后处理 |
| 自定义 | 1–252 | 用户自定义表，用于策略路由 |

```bash
# 查看特定路由表
ip route show table local
ip route show table main      # 等价于 ip route show
ip route show table 100       # 查看自定义表
```

#### `ip rule`：路由策略数据库

策略路由的决策流程是：内核遍历 `ip rule` 中的规则，**从编号最小的规则开始匹配**，匹配就停止，使用该规则指定的路由表做决策。

```bash
$ ip rule show
0:      from all lookup local
32766:  from all lookup main
32767:  from all lookup default
```

默认只有三条规则：

| 优先级 | 规则 | 匹配后使用的路由表 |
|--------|------|-------------------|
| 0 | 所有流量 | `local` 表（本地路由） |
| 32766 | 所有流量 | `main` 表（主路由） |
| 32767 | 所有流量 | `default` 表（兜底） |

所以默认情况下，所有流量先匹配 `local`（检查是否是本机地址），再匹配 `main`（看普通路由），最后落到 `default`（空表）。

#### 实战：多网卡多网关策略

假设一台机器有两个网卡：
- eth0: `192.168.1.100/24`，网关 `192.168.1.1`（办公网络）
- eth1: `10.0.0.1/24`，网关 `10.0.0.254`（生产网络）

需求：从 eth1 发出的流量走生产网络网关 `10.0.0.254`，其余流量正常走办公网络。

**第一步：创建自定义路由表**

```bash
# 在 /etc/iproute2/rt_tables 中定义表名（可选，也可以直接使用编号）
echo "100 production" >> /etc/iproute2/rt_tables
```

**第二步：向自定义表中添加路由**

```bash
# 向 production 表添加默认路由
ip route add default via 10.0.0.254 dev eth1 table production

# 同时添加直连路由（否则找不到下一跳）
ip route add 10.0.0.0/24 dev eth1 scope link table production
```

**第三步：添加策略规则**

```bash
# 从 eth1（10.0.0.1）发出的流量，查 production 表
ip rule add from 10.0.0.1 lookup production priority 5000
```

**验证：**

```bash
# 从 eth0 的 IP 访问外网，应该走 main 表（默认路由 192.168.1.1）
$ ip route get 8.8.8.8 from 192.168.1.100
8.8.8.8 from 192.168.1.100 via 192.168.1.1 dev eth0 uid 0

# 从 eth1 的 IP 访问外网，应该走 production 表（10.0.0.254）
$ ip route get 8.8.8.8 from 10.0.0.1
8.8.8.8 from 10.0.0.1 via 10.0.0.254 dev eth1 table production uid 0
```

> [!note] 策略路由的常见用途
> - **多运营商接入**：电信走电信路由表，联通走联通路由表
> - **VPN 分流**：特定流量走 VPN，其余走直连
> - **容器/虚拟机网络**：不同网段的流量导向不同的虚拟网络
> - **测试环境**：同一台机器模拟多个网络路径

---

### 路由排查思路

#### 场景 1：默认网关丢了

**现象**：`ping 8.8.8.8` 报 `Network is unreachable`

**排查**：

```bash
# 第一步：确认默认路由是否存在
ip route show default

# 如果输出为空，说明默认路由缺失
# 如果是 DHCP，尝试续约
sudo dhclient eth0

# 如果是静态配置，手动添加
sudo ip route add default via 192.168.1.1 dev eth0

# 第二步：验证网关是否可达
ip route get 8.8.8.8        # 现在应该能看到 via 192.168.1.1
ping -c 3 192.168.1.1       # 确认网关能通
```

**根因**：DHCP 租约过期、NetworkManager 配置异常、手动删除了默认路由、物理线路断开导致网关不可达。

#### 场景 2：多网卡路由冲突

**现象**：加了第二个网卡后，外网突然不通了，或 ping 外网延迟极高。

**根因**：两个网卡各自通过 DHCP 获取了不同的默认路由，后获取的覆盖了前一个。

```bash
# 排查：查看默认路由是否出现了多个
$ ip route show default
default via 192.168.1.1 dev eth0 proto dhcp metric 100
default via 10.0.0.254 dev eth1 proto dhcp metric 101
```

两条默认路由，metric 不同。假设原先是 eth0 走办公网络，现在 eth1 DHCP 拿到了一条 metric 101 的默认路由。虽然 eth0（metric 100）仍然优先，但如果 eth0 的网关 `192.168.1.1` 不允许访问某些外网地址，数据包就"有去无回"。

**解决方案**：

```bash
# 方法一：删除不需要的默认路由
sudo ip route del default via 10.0.0.254 dev eth1

# 方法二：调整 metric，确保首选正确的网关
sudo ip route replace default via 192.168.1.1 dev eth0 metric 50

# 方法三：使用策略路由精确控制
```

> [!warning] 多网卡常见陷阱
> 默认路由只能有一个有效的出口。多个默认路由并存（即使 metric 不同）在生产环境中往往意味着"流量走向不符合预期"。

#### 场景 3：路由配了但没生效

**现象**：`ip route show` 能看到路由，但实际访问目标 IP 时还是走了默认路由。

```bash
# 排查：用 ip route get 模拟决策
ip route get 172.16.0.50

# 结果可能显示 via wrong-gateway（走了默认路由而非预期的静态路由）
```

**可能原因**：

| 原因 | 检查方法 | 修复 |
|------|---------|------|
| 前缀写错了 | `ip route show 172.16.0.0/16` 确认精确匹配 | 更正目的网络 |
| Metric 值偏高 | 是否有同前缀的路由且 metric 更小？ | `ip route show` 检查所有匹配的路由 |
| 下一跳不可达 | `ip neigh show` 查看邻居是否 STALE/FAILED | 确认下一跳 MAC 能解析到 |
| 表错了 | 策略路由导致实际查询的不是 main 表 | `ip rule show` + `ip route get` 加 `from` 参数 |
| 源 IP 不符 | 策略路由可能根据源 IP 匹配了不同表 | `ip route get <IP> from <src>` 模拟 |

---

### ip route 其他常用操作

虽然本章聚焦"信息查询"，但掌握以下操作有助于理解路由表的工作方式。

```bash
# 添加路由
sudo ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0

# 删除路由
sudo ip route del 10.0.0.0/8

# 替换路由（不存在则添加，存在则更新）
sudo ip route replace 10.0.0.0/8 via 192.168.1.254 dev eth0

# 刷新路由缓存（极少需要，内核自动维护）
sudo ip route flush cache
```

> [!note] 关于路由缓存
> 早期 Linux 内核（2.2 之前）有独立的路由缓存（route cache），需要用 `ip route flush cache` 手动刷新。现代内核（2.6+）使用 FIB（Forwarding Information Base）三态查找，路由变更立即生效，通常不需要手动刷新缓存。

---

### 本章小结

- **路由表是内核决定"数据包下一步去哪"的规则集合**，每条路由由目的网络、下一跳、出接口三个要素组成
- 路由分三种来源：**直连路由**（内核自动添加）、**静态路由**（手动配置）、**动态路由**（路由协议学习）
- **最长前缀匹配**是路由选择的第一标准——掩码越精确的规则越优先
- **`ip route show`** 查看路由表，**`ip route get`** 是最高效的路由决策模拟工具，不发送任何数据包即可验证路由选择
- **`ip rule` 策略路由**允许基于源 IP、TOS、防火墙标记等多维度选择路由表，打破了"仅根据目标 IP 选路"的限制
- 路由排查的黄金组合：`ip route show default` + `ip route get <target>` + `ping <gateway>`，三步定位 90% 的路由问题

#### 下章预告

路由表告诉数据包"往哪走"，但大多数时候我们访问的目标是域名而非 IP 地址。下一章将深入 **DNS 解析与域名信息**，从 `/etc/resolv.conf` 的配置链路到 `dig` 的高级用法，再到 systemd-resolved 的完整体系，帮你彻底掌握 Linux 上的域名解析机制。

---
