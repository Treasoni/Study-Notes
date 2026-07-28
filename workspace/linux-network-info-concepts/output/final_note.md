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
2. [第二章：网络接口与链路层信息](#第二章网络接口与链路层信息)
3. [第三章：IP 地址与子网信息](#第三章ip-地址与子网信息)
4. [第四章：路由表信息](#第四章路由表信息)
5. [第五章：DNS 解析与域名信息](#第五章dns-解析与域名信息)
6. [第六章：ARP 与邻居发现](#第六章arp-与邻居发现)
7. [第七章：Socket 连接与传输层信息](#第七章socket-连接与传输层信息)
8. [第八章：无线网络信息](#第八章无线网络信息)
9. [第九章：网络监控与统计](#第九章网络监控与统计)
10. [第十章：抓包与协议分析基础](#第十章抓包与协议分析基础)

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

#### 按场景查找

| 想查什么 | 优先使用命令 | 所属层次 |
|---------|------------|---------|
| 网卡是否在线、MAC 地址、MTU | `ip link show` | L2 |
| 网卡速率、驱动、硬件信息 | `ethtool eth0` | L1/L2 |
| IP 地址、子网掩码、scope | `ip addr show` | L3 |
| 默认网关、路由表 | `ip route show` | L3 |
| DNS 解析结果 | `dig baidu.com` | L7 |
| 系统 DNS 配置 | `resolvectl status` | L7 |
| 目标 IP 对应哪个 MAC | `ip neigh show` | L2 |
| 哪些端口在监听 | `ss -tulnp` | L4 |
| TCP 连接状态统计 | `ss -tanp` | L4 |
| 连通性测试 | `ping -c 5 <IP>` | L3/L4 |
| 路由追踪 | `mtr baidu.com` | L3 |
| WiFi 信号强度和 SSID | `iw dev wlan0 link` | L1/L2 |
| 实时带宽 | `iftop -i eth0` | L2-L4 |
| 网卡 CRC 错误统计 | `ethtool -S eth0` | L2 |
| 抓包分析 | `tcpdump -i eth0` | L2-L7 |

> [!tip] 快速记忆口诀
> **"链路看 `link`，地址看 `addr`，路由看 `route`，邻居看 `neigh`"**——`ip` 工具的四个主命令覆盖了 80% 的日常查询需求。

---

### 信息查询通用思路

#### 三步排查法

```
1. 确认状态（正常吗？）
2. 读取配置（设了什么？）
3. 验证连通（实际通不通？）
```

#### 信息查询通用方法论

1. **从全局到局部**：先用简洁模式（`-br`）获取概览，再深入特定接口或条目
2. **从底层到上层**：先确认物理/链路层正常，再查网络层、传输层、应用层
3. **交叉验证**：多个工具验证同一个信息
4. **善用 JSON 输出**：`ip -j` + `jq` 适合脚本化批量查询

#### 常见误区

| 误区 | 正确做法 |
|------|---------|
| 装了网卡驱动就一定能看到 `ip link up` | 检查物理连接、协商速率、`ethtool eth0` 确认 Link detected: yes |
| `ifconfig` 看不到 IP 就是没 IP | 用 `ip addr show` 确认 |
| ping 不通就是网络断了 | 先确认是否 ICMP 被防火墙拦截 |
| `netstat` 很慢就是机器有问题 | `netstat` 读 `/proc` 本身慢，改用 `ss` |

---

### 本章小结

- Linux 网络信息是内核网络栈各层的状态数据，通过特定命令读取
- **分层模型是排查的根本框架**
- **iproute2 是现代 Linux 网络查询的标准工具家族**
- 通用排查思路=**确认状态→读取配置→验证连通**

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

MAC 地址（Media Access Control Address）是网卡出厂时烧录的 48 位标识符，通常表示为 12 位十六进制数：`aa:bb:cc:dd:ee:ff`。

| 属性 | 说明 |
|------|------|
| 长度 | 6 字节（48 位） |
| 表示法 | 12 位十六进制，通常用冒号分隔 |
| 范围 | 全球唯一（理论上），前 3 字节是 OUI（厂商代码） |
| 作用域 | **同一广播域内有效**——跨路由设备无法通过 MAC 寻址 |
| 可修改 | 支持软件覆盖 |

> [!note] MAC 地址 vs IP 地址
> MAC 地址是"原地物理身份"，IP 地址是"逻辑位置"。类比：MAC 是身份证号（出生就有，基本不变），IP 是住址（搬家就变）。

#### 1.2 以太网帧结构：L2 的数据单元

```
  ┌─────────────────────────────────────────────────────────┐
  │ 目的MAC  │  源MAC   │  Type/Len │  Payload  │   FCS    │
  │ (6 字节)  │ (6 字节)  │ (2 字节)  │ (46-1500B)│ (4 字节) │
  └─────────────────────────────────────────────────────────┘
```

#### 1.3 MTU：一个以太网帧能装多少数据

**MTU（Maximum Transmission Unit）** 是网络接口所能传输的最大数据包大小（字节）。标准以太网 MTU = **1500 字节**。

```
MTU 1500 = 以太网头(14) + IP 头(20) + TCP 头(20) + 数据(1446)
                                           ↓
                                    TCP MSS = 1460
```

> [!warning] VPN 和隧道场景下的 MTU 陷阱
> 当你使用 VPN（OpenVPN、WireGuard 等）时，额外的封装头部会减少有效 MTU。
> 一个常见的排查步骤：`ping -M do -s 1472 baidu.com` 如果失败，说明路径上可能有 MTU 问题。

---

### 2. `ip link`：查看网卡状态

```bash
ip link show
```

输出示例：

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 ... state UNKNOWN ...
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ... state UP ...
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 ... state DOWN ...
```

**关键字段**：

| 字段 | 含义 | 常见值 |
|------|------|--------|
| `state` | 接口运行状态 | `UP`/`DOWN`/`UNKNOWN` |
| `mtu` | 最大传输单元 | `1500`（以太网） |
| `LOWER_UP` | 物理层已连接 | 有则表示物理层就绪 |
| `NO-CARRIER` | 物理层未连接 | 没有物理信号 |
| `link/ether` | MAC 地址 | `52:54:00:12:34:56` |

> [!note] `UP` 不等于 `LOWER_UP`
> - `state UP` = 软件层面启动了接口
> - `LOWER_UP` = 物理连接正常
> - `NO-CARRIER` = 物理层断开
> **如果看到 `state UP` 但 `NO-CARRIER`，说明软件配置正确，但物理连接有问题。**

#### 简洁模式（`-br`）

```bash
ip -br link show
# lo               UNKNOWN   00:00:00:00:00:00
# eth0             UP        52:54:00:12:34:56
# docker0          DOWN      02:42:ac:11:00:01
```

---

### 3. `ip -s link`：收发统计信息

```bash
ip -s link show eth0
```

RX 列：`bytes`、`packets`、`errors`、`dropped`、`missed`、`mcast`
TX 列：`bytes`、`packets`、`errors`、`dropped`、`carrier`、`collsns`

> [!tip] `dropped` 不等于 `errors`
> `errors` 是硬件/物理层面的错误，`dropped` 是内核主动丢弃（缓冲区满）。

---

### 4. `ip -j` JSON 输出

```bash
ip -j link show eth0
```

JSON 输出优势：字段命名规范、结构稳定、不依赖文本行顺序。

配合 `jq` 实战：
```bash
ip -j link show | jq '.[] | {name: .ifname, state: .operstate, mac: .address}'
ip -j link show | jq -r '.[] | select(.operstate == "UP") | .ifname'
ip -j -s link show eth0 | jq '.[0].stats64.tx.dropped / .[0].stats64.tx.packets * 100'
```

---

### 5. `ethtool`：网卡硬件信息与驱动查询

```bash
ethtool eth0          # 基本参数（Speed、Duplex、Link detected）
ethtool -i eth0       # 驱动信息
ethtool -S eth0       # 硬件级统计（CRC 错误、FIFO 溢出）
ethtool -g eth0       # ring buffer 大小
```

> [!warning] 速率不匹配的后果
> 遇到"通了但很慢"时，先检查协商速率：`ethtool eth0 | grep Speed`

---

### 6. 常见链路层问题排查

#### 网卡 DOWN 且 LOWER_UP 不存在

```bash
ethtool eth0 | grep "Link detected"
sudo ip link set dev eth0 up
```

#### MTU 不匹配

```bash
ping -M do -s 1472 192.168.1.1    # 测试路径 MTU
```

#### 网卡丢包排查流程

```
检查 ip -s link 中 dropped > 0
→ 检查 ethtool -g ring buffer 当前值
→ 检查 ethtool -S 中 rx_missed_errors 是否增长
→ 检查 /proc/net/softnet_stat
→ 检查系统内存压力
```

---

### 本章小结

- **MAC 地址是网卡的链路层标识**（48 位），在同一广播域内有效
- **MTU 决定单帧最大数据量**（以太网默认为 1500）
- **`ip link show` 是最核心的链路层查询命令**：`-br` 简洁模式、`-s` 收发统计
- **`ip -j link show` JSON 输出 + `jq` 解析**适合监控脚本
- **`ethtool` 提供硬件级视角**：协商速率、驱动版本、CRC 错误

#### 下章预告

链路层搞定后，下一章将往上走一层——**IP 地址与子网信息**。

---

---

## 第三章：IP 地址与子网信息

如果说 MAC 地址是网卡的"身份证"，那 IP 地址就是它在网络中的"门牌号"。没有 IP，数据包就不知道该往哪送。

---

### IP 地址核心概念

IPv4 地址由 32 个比特组成，分为**网络位**和**主机位**：

```
点分十进制：  192  .  168  .   1   .  100
二进制：      11000000  10101000  00000001  01100100
              ├─────── 网络位 ────────┤── 主机位 ─┤
```

> [!note] 关键认知
> 判断两个 IP 是否在同一网络，不是看它们数字上是否接近，而是看它们的网络位是否相同。

---

### 子网掩码与 CIDR

子网掩码高位连续为 1 表示网络位，低位为 0 表示主机位。

CIDR 表示法直接在 IP 后面加 `/` 和网络位数：

| CIDR | 子网掩码 | 可用主机数 |
|------|---------|-----------|
| `/8` | `255.0.0.0` | 16,777,214 |
| `/16` | `255.255.0.0` | 65,534 |
| `/24` | `255.255.255.0` | 254 |
| `/30` | `255.255.255.252` | 2 |
| `/32` | `255.255.255.255` | 1 |

---

### 特殊 IP 地址

- **Loopback**：`127.0.0.0/8`，发往本机的数据包不会离开本机
- **Link-Local**：`169.254.0.0/16`，DHCP 分配失败时的备用地址
- **私有地址**：`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`

> [!warning] 出现 `169.254.x.x` 通常意味着 DHCP 故障——这是排查时的红色警报。

---

### `ip addr` 命令详解

```bash
ip addr show eth0
```

输出逐字段解读：
- `inet 192.168.1.100/24` — IP + CIDR
- `scope global` — 作用域（global/link/host）
- `dynamic` — 动态地址（DHCP 获取）

#### Scope（作用域）

| Scope | 含义 | 常见地址 |
|-------|------|---------|
| `global` | 全局可用 | `192.168.1.100/24` |
| `link` | 仅限同一链路 | `169.254.x.x/16` |
| `host` | 仅限本机 | `127.0.0.1/8` |

#### 简洁模式（`-br`）

```bash
ip -br addr show
# lo      UNKNOWN   127.0.0.1/8
# eth0    UP        192.168.1.100/24
```

#### JSON 模式（`-j`）

```bash
ip -j addr show eth0 | jq -r '.[0].addr_info[] | select(.family == "inet") | .local'
```

---

### 常见坑

1. **多个 IP 的优先级**：源地址选择由路由表的最长前缀匹配决定
2. **Secondary 地址**：不会用作对外连接的源地址，primary 被删除后自动晋升
3. **`ifconfig` vs `ip addr`**：`ifconfig` 可能不显示某些地址
4. **`scope host` 的地址** ping 不通其他机器

---

### 本章小结

- **IPv4 地址 = 32 位二进制，分为网络位 + 主机位**
- **CIDR 表示法**（如 `/24`）是子网掩码的简写
- **特殊地址**：`127.0.0.0/8`、`169.254.0.0/16`、私有地址
- **`ip -br addr show` + `ip -j addr show`** 覆盖人类阅读和脚本解析两大场景

#### 下章预告

IP 配好了，数据包怎么知道下一步往哪里送？这就是**路由表**的工作。

---

---

## 第四章：路由表信息

### 引子：数据包出了本机，下一步去哪？

上一章我们学会了查看 IP 地址，知道了本机在哪个网段。但数据包要发送到另一个网络（比如访问 `8.8.8.8`），它出了本机网卡之后该往哪走？答案是 **路由表**。

> 一句话定义：路由表是内核中用于决定"数据包下一步去哪"的规则集合。

> [!note] 为什么需要路由表？
> 一台 Linux 机器可能有多个网卡（eth0、eth1、wlan0），连接着不同的网络。当数据包从本机发出时，内核必须决定：扔给 eth0 还是 eth1？交给哪个下一跳？路由表就是做这个决策的。

---

### 路由表核心概念

每条路由条目有三个要素：**目的网络**、**下一跳**、**出接口**。

三种路由来源：
1. **直连路由**（`proto kernel`）：配置 IP 时内核自动添加
2. **静态路由**（`proto static`）：手动添加
3. **动态路由**：路由协议学习

**默认路由**是路由表的"兜底"规则：`default via 192.168.1.1 dev eth0`

---

### 最长前缀匹配规则

前缀越长（掩码越精确），优先级越高。metric 是第二优先级。

```
10.0.0.0/8      via 10.0.0.1
10.0.1.0/24     via 10.0.1.1
0.0.0.0/0       via 192.168.1.1

目标 10.0.1.5 → 匹配 /8、/24、/0 → 最长前缀 /24 → 走 10.0.1.1
目标 8.8.8.8  → 只匹配 /0       → 走默认路由
```

---

### `ip route show` 详解

```bash
ip route show
# default via 192.168.1.1 dev eth0 proto dhcp metric 100
# 10.0.0.0/24 dev eth1 proto kernel scope link src 10.0.0.1 metric 101
# 192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100 metric 100
```

字段：`via`（下一跳）、`dev`（出接口）、`proto`（来源）、`scope`（作用域）、`metric`（度量）

---

### `ip route get`：模拟路由决策

这是排查路由问题时**最实用的命令**。不发送任何数据包，直接告诉路由决策结果。

```bash
ip route get 8.8.8.8
# 8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.100 uid 1000
```

---

### 策略路由：`ip rule` 与多路由表

Linux 支持多张路由表：`local`（255）、`main`（254）、`default`（253）和自定义表。

```bash
ip rule show
# 0:      from all lookup local
# 32766:  from all lookup main
# 32767:  from all lookup default
```

---

### 路由排查思路

**场景 1：默认网关丢了** → `ping` 报 `Network is unreachable` → `ip route show default`

**场景 2：多网卡路由冲突** → 两个 DHCP 默认路由互相覆盖 → 调整 metric 或使用策略路由

**场景 3：路由配了但没生效** → 用 `ip route get` 模拟决策定位问题

---

### 本章小结

- **最长前缀匹配**是路由选择的第一标准
- **`ip route show`** 查看路由表，**`ip route get`** 模拟路由决策
- **策略路由**允许基于源 IP 等多维度选择路由表
- 黄金组合：`ip route show default` + `ip route get <target>` + `ping <gateway>`

#### 下章预告

路由表告诉数据包"往哪走"，但大多数时候我们访问的目标是域名而非 IP 地址。下一章将深入 **DNS 解析与域名信息**。

---

---

## 第五章：DNS 解析与域名信息

当你输入 `baidu.com` 并按下回车，浏览器需要找到这个域名对应的 IP 地址才能建立连接。这个从"域名"到"IP"的转换过程，就是 **DNS 解析（Domain Name System resolution）**。它是互联网通信的第一步——如果这一步失败，你连不上任何网站，而 `ping` 和 `ip addr` 看到的网络配置可能完全正常。

本章是全书最长的一章，因为 DNS 是实际排障中**最常出问题**的环节。

---

### DNS 解析完整流程：从浏览器到 DNS 服务器

> [!note] 一句话理解 DNS
> DNS 本质上是一个**分布式的键值数据库**——键是域名（如 `www.example.com`），值是 IP 地址（如 `93.184.216.34`）。

1. **浏览器缓存检查**——不发送任何网络请求
2. **操作系统缓存检查**——`resolvectl statistics` 查看命中情况
3. **读取 `/etc/hosts`**——静态域名→IP 映射表
4. **查询 DNS 解析器**——通常是 systemd-resolved 的 stub（`127.0.0.53`）
5. **递归查询到权威 DNS**——根→TLD→权威服务器
6. **浏览器发起 HTTP 连接**

```
完整链路：浏览器缓存 → OS 缓存 → /etc/hosts → DNS 解析器 → 根 → TLD → 权威
```

---

### DNS 记录类型详解

| 类型 | 作用 | 查询命令 |
|------|------|---------|
| **A** | 域名 → IPv4 | `dig example.com A` |
| **AAAA** | 域名 → IPv6 | `dig example.com AAAA` |
| **CNAME** | 域名别名 | `dig www.example.com CNAME` |
| **MX** | 邮件服务器 | `dig example.com MX` |
| **NS** | 权威 DNS 服务器 | `dig example.com NS` |
| **TXT** | 任意文本 | `dig example.com TXT` |
| **SOA** | 区域权威信息 | `dig example.com SOA` |

> [!tip] SOA 的 serial 字段是"DNS 排障神器"
> 当你的 DNS 修改没有生效时，`dig example.com SOA` 查看 serial 号，确认区域文件是否更新。

---

### Linux DNS 配置文件体系

```
/etc/nsswitch.conf → 控制"以什么顺序查"
/etc/hosts → 静态映射（优先级高）
/etc/resolv.conf → 指定 DNS 服务器（优先级低）
```

#### 第一环：`/etc/nsswitch.conf`

```bash
$ grep hosts /etc/nsswitch.conf
hosts:          files dns   # 先查 /etc/hosts，没找到再查 DNS
```

> [!warning] `getent hosts` vs `dig` 的区别
> - `getent hosts`：走 NSS 链路，**完全模拟应用行为**
> - `dig`：直接向 DNS 服务器发送请求，**跳过 NSS 和 `/etc/hosts`**

#### 第二环：`/etc/hosts`

```bash
127.0.0.1       localhost
127.0.1.1       pop-os
192.168.1.10    nas.home
```

#### 第三环：`/etc/resolv.conf`

> [!warning] 最常见的 DNS 踩坑点：手动编辑 `/etc/resolv.conf`
> 在 Ubuntu 16.04+ 上，`/etc/resolv.conf` 是一个符号链接指向 systemd-resolved 管理的文件。**手动编辑这个文件会被 systemd-resolved 定期覆盖**。

---

### systemd-resolved 与 resolvectl

systemd-resolved 在 `127.0.0.53` 上启动一个本地 DNS 代理：

1. **缓存 DNS 查询结果**
2. **管理 `/etc/hosts`**
3. **DNSSEC 验证**（可选）
4. **每接口 DNS 配置**

#### resolvectl 命令详解

```bash
resolvectl status                        # 查看当前 DNS 配置
resolvectl query baidu.com               # DNS 查询
resolvectl statistics                    # 缓存命中情况
resolvectl flush-caches                  # 清空 DNS 缓存（最常用排障操作）
resolvectl dns enp0s3 8.8.8.8            # 设置接口 DNS
```

> [!note] `resolvectl query` vs `dig`
> - `resolvectl query` 走 systemd-resolved 的完整链路（含缓存和 `/etc/hosts`）
> - `dig` 直接向指定 DNS 服务器发查询，绕过 systemd-resolved
> - 排障时两者的差异本身就是信息

---

### `dig` 命令详解

`dig`（Domain Information Groper）是 DNS 查询的**首选工具**。

#### 基本查询

```bash
dig baidu.com
```

输出关键字段：`status`（NOERROR/NXDOMAIN）、`ANSWER SECTION`（返回结果）、`SERVER`（哪个 DNS 服务器返回的）、`Query time`

#### +short：简化输出

```bash
dig baidu.com +short
# 39.156.66.10
# 110.242.68.66
```

#### @server：指定 DNS 服务器

```bash
dig @8.8.8.8 baidu.com +short    # Google DNS
dig @1.1.1.1 baidu.com +short    # Cloudflare DNS
dig @114.114.114.114 baidu.com +short  # 国内 DNS
```

#### +trace：追踪完整委派链

```bash
dig baidu.com +trace
```

从根服务器一步步追踪到权威服务器，精准定位 DNS 故障环节。

#### -x：反向查询（IP 到域名）

```bash
dig -x 8.8.8.8 +short
# dns.google.
```

#### dig 常用选项速查

| 选项 | 作用 |
|------|------|
| `+short` | 简化输出 |
| `+trace` | 追踪递归查询 |
| `+noall +answer` | 只显示答案段 |
| `@server` | 指定 DNS 服务器 |
| `-x IP` | 反向查询 |
| `+time=5` | 设置超时秒数 |

---

### nslookup 与 host 快速查询

| 工具 | 输出详细度 | `+trace` | 推荐场景 |
|------|-----------|----------|---------|
| `dig` | 最详细 | 支持 | 深度排障、脚本 |
| `nslookup` | 中等 | 不支持 | 日常快速查询 |
| `host` | 最精简 | 不支持 | 脚本、简单验证 |

---

### 常见 DNS 排查场景

**场景一："网站打不开，是不是 DNS 的问题？"**

```bash
dig www.baidu.com +short           # 确认域名能不能解析
dig @8.8.8.8 www.baidu.com +short  # 对比不同 DNS 服务器
getent hosts www.baidu.com         # 检查系统解析链路
```

**场景二："改了 DNS 记录，但本机还是旧 IP"**

```bash
resolvectl flush-caches   # 清空缓存
dig www.example.com +short  # 确认是否拿到新 IP
```

**场景三："域名解析到了错误的 IP（可能被劫持）"**

对比不同 DNS 服务器返回结果，使用 `+trace` 确认权威服务器返回的正确值。

---

### 本章小结

- **DNS 解析流程**从浏览器缓存开始，经过 OS 缓存、`/etc/hosts`、本地解析器，最终通过递归查询到达权威 DNS 服务器
- **配置文件链路**：`nsswitch.conf` → `/etc/hosts` → `/etc/resolv.conf`
- **systemd-resolved** 在 `127.0.0.53` 启动 stub 解析器，`resolvectl flush-caches` 是最常用的排障操作
- **`dig`** 是 DNS 排障的首选工具——`+short`、`+trace`、`@server`、`-x`
- **排障三步走**：`dig` 测 DNS 服务器本身 → `getent hosts` 测系统链路 → 对比不同 DNS 服务器判断是否被劫持

#### 下章预告

下一章我们回到链路层，深入 **ARP 协议与邻居发现**。

---

---

## 第六章：ARP 与邻居发现

### 从一个问题开始

两台机器在同一个二层网络，A 要发一个 IP 包给 B。A 知道 B 的 IP 地址（`192.168.1.5`），但以太网帧的目标地址需要的是 **MAC 地址**，而不是 IP 地址。A 怎么知道 B 的 MAC 是什么？

这个"IP 到 MAC"的映射就是本章要解决的核心问题。映射表由 **ARP 协议**（IPv4）或 **NDP**（IPv6）维护，而 `ip neigh` 就是我们查看和操作这张表的命令。

---

### ARP 协议核心概念

**广播请求，单播回复**：

```
Step 1: A 广播 ──→ "谁是 192.168.1.5？请告诉 aa:aa:aa:aa:aa:aa"
Step 2: B 单播 ←── "192.168.1.5 是我，我的 MAC 是 bb:bb:bb:bb:bb:bb"
```

> [!tip] 抓包验证
> 用 `tcpdump -i eth0 arp` 可以抓到 ARP 请求和回复包。

**非常关键**：ARP 不能跨路由器工作。如果目标 IP 不在同一子网，主机会用 ARP 解析**网关的 MAC**，而非目标 IP 的 MAC。

---

### 邻居状态机详解

ARP 缓存中的每个条目都有一个**状态**：

```
REACHABLE → STALE → DELAY → PROBE → FAILED
PERMANENT（静态绑定，永不超时）
```

| 状态 | 含义 |
|------|------|
| **REACHABLE** | 最近确认过可达 |
| **STALE** | 条目超时，可能仍可用但未验证 |
| **DELAY** | 需要发数据了，但先等一小会儿 |
| **PROBE** | 正在发单播探测确认 |
| **FAILED** | 不可达 |
| **PERMANENT** | 静态条目，永不超时 |

> [!warning] STALE 不是"坏"的状态
> STALE 只表示"有一段时间没确认了"。从 STALE 发数据包时会自动重验证，用户基本无感知。

---

### `ip neigh show` 输出解读

```bash
ip neigh show
# 192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
# 192.168.1.5 dev eth0 lladdr 11:22:33:44:55:66 STALE
# 192.168.1.10 dev eth0 FAILED
```

字段：`邻居 IP` `dev`（所属网卡）`lladdr`（对端 MAC）`状态`

常用过滤：
```bash
ip neigh show dev eth0          # 只看某个接口
ip -6 neigh show                # 只看 IPv6
ip neigh show | grep FAILED     # 只看有问题的
ip -j neigh show                # JSON 输出
```

---

### `ip neigh flush` 清除邻居表

```bash
ip neigh flush all              # 清空所有
ip neigh flush dev eth0         # 清空某个接口
ip neigh flush nud failed       # 只清空 FAILED 状态
```

典型使用场景：网关 MAC 变更、VM/容器迁移、频繁出现 FAILED、怀疑 ARP 缓存问题。

---

### IPv6 NDP 取代 ARP

IPv6 中没有 ARP 协议，由 **NDP（Neighbor Discovery Protocol）** 替代。

| 对比维度 | ARP（IPv4） | NDP（IPv6） |
|---------|-----------|-------------|
| 协议基础 | 独立 ARP 协议 | 基于 ICMPv6 |
| 传输方式 | 广播 | 多播 |
| 安全性 | 无内置保护 | 支持 SEND |
| 功能 | 仅地址解析 | 还包括路由器发现、SLAAC、DAD |

> [!note] 邻居表统一管理
> 在 Linux 内核层面，ARP（IPv4）和 NDP（IPv6）的解析结果存在**同一张邻居表**中。`ip neigh show` 不区分协议。

---

### ARP 表溢出与 `gc_thresh` 排障

在大二层网络中，ARP 表可能占满，症状：`neighbour: arp_cache: neighbor table overflow!`

三个关键内核参数：
```bash
sysctl net.ipv4.neigh.default.gc_thresh1   # 软下限（默认 128）
sysctl net.ipv4.neigh.default.gc_thresh2   # 软上限（默认 512）
sysctl net.ipv4.neigh.default.gc_thresh3   # 硬上限（默认 1024）
```

排查与修复：
```bash
ip neigh show | wc -l           # 查看当前大小
dmesg | grep -i "neighbor table overflow"  # 检查内核日志
ip neigh flush nud failed       # 清空 FAILED 条目
# 调大 gc_thresh：
sysctl -w net.ipv4.neigh.default.gc_thresh3=4096
```

---

### 本章小结

- **ARP 协议**通过广播请求/单播回复将 IP 解析为 MAC，**只在同一广播域内工作**
- **邻居状态机**：REACHABLE → STALE → DELAY → PROBE → FAILED
- **`ip neigh show`** 统一管理 IPv4（ARP）和 IPv6（NDP）
- **ARP 表溢出**由 `gc_thresh1/2/3` 控制，超过硬上限会导致内核丢包

#### 下章预告

下一章我们将从数据链路层（L2）跃升到传输层（L4），学习 **Socket 连接与传输层信息**。

---

---

## 第七章：Socket 连接与传输层信息

前六章我们从链路层一路走到网络层，看过了 MAC 地址、IP 地址、路由表和邻居表。现在终于到达传输层——所有网络通信的"最后一公里"交付环节。本章的核心问题是：**操作系统如何管理成千上万的网络连接？怎样快速查看端口监听情况、定位连接异常？**

---

### TCP/UDP 协议概念速览

| 特性 | TCP | UDP |
|------|-----|-----|
| 头部大小 | 20-60 字节 | 8 字节（固定） |
| 连接建立 | 三次握手 | 无需握手 |
| 可靠性 | 确认重传 | 无确认 |
| 顺序保证 | 序列号排序 | 不保证顺序 |
| 流量控制 | 滑动窗口 | 无 |
| 适用场景 | HTTP/HTTPS/SSH/FTP | DNS/DHCP/视频流/VPN |

---

### TCP 状态机

TCP 是一个**有状态**的协议。理解这些状态是阅读 `ss` 输出和排查连接问题的前提。

| 状态 | 含义 | 排障关注点 |
|------|------|-----------|
| **LISTEN** | 服务端正在监听端口 | 正常。确认服务是否启动 |
| **ESTABLISHED** | 连接已建立 | 数量异常多可能有问题 |
| **TIME-WAIT** | 主动关闭方等待（约 60s） | 大量堆积可能耗尽端口资源 |
| **CLOSE-WAIT** | 被动关闭方等待应用调用 close() | **应警惕**——说明应用有 bug |
| **SYN-RECV** | 收到 SYN 但未完成三次握手 | 大量 SYN-RECV 可能是 SYN Flood |

> [!warning] CLOSE-WAIT 泄漏是最常见的排障场景
> `ss -tanp | grep CLOSE-WAIT` 确认有未正确关闭的 Socket。这不是网络问题，是代码问题。

---

### Socket 与连接五元组

一个完整的 TCP 连接由**五个元素**唯一标识：
```
(源 IP, 源端口, 目标 IP, 目标端口, 传输层协议)
```

```bash
ss -tanp | head -5
# STATE      RECV-Q SEND-Q  LOCAL ADDRESS:PORT     PEER ADDRESS:PORT
# LISTEN     0      128     0.0.0.0:22             0.0.0.0:*
# ESTAB      0      0       192.168.1.100:22       10.0.0.5:54321
```

---

### `ss` 命令详解

`ss`（Socket Statistics）通过 **netlink** 直连内核读取 Socket 信息，比传统 `netstat` 快 10-100 倍。

#### 查看监听端口：`ss -tulnp`

```bash
ss -tulnp
# -t: TCP  -u: UDP  -l: listening  -n: 不解析服务名  -p: 显示进程
```

#### 查看所有连接：`ss -tanp`

```bash
ss -tanp
# STATE      RECV-Q  SEND-Q  LOCAL:PORT         PEER:PORT
# LISTEN     0       128     0.0.0.0:22         0.0.0.0:*
# ESTAB      0       0       192.168.1.100:22   10.0.0.5:54321
# TIME-WAIT  0       0       192.168.1.100:34567 93.184.216.34:443
```

#### 连接统计总览：`ss -s`

```bash
ss -s
# Total: 298 (kernel 398)
# TCP:   18 (estab 4, closed 9, orphaned 0, synrecv 0, timewait 3/0), ports 12
```

#### TCP 内部参数：`ss -i`

```bash
ss -t -i state established
# rtt:12.5/4.5  rto:204  cwnd:10  ssthresh:7  mss:1460
# bytes_retrans:0  send:130.4Mbps  pacing_rate:260.8Mbps
```

| 参数 | 含义 | 排障用途 |
|------|------|---------|
| **rtt** | 往返延迟 | 判断网络延迟是否正常 |
| **rto** | 超时重传时间 | RTO 过大说明丢包严重 |
| **cwnd** | 拥塞窗口 | 影响吞吐量的核心参数 |
| **bytes_retrans** | 重传字节数 | **>0 说明有丢包** |

---

### 状态过滤与端口过滤

```bash
ss state time-wait                     # 列出所有 TIME-WAIT
ss -t state established                # 仅 TCP 的 ESTABLISHED
ss sport = :80                         # 源端口是 80
ss dport = :443                        # 目标端口是 443
ss -tanp dst 10.0.0.5                  # 匹配特定 IP
ss -tanp state close-wait              # 排查连接泄漏
ss -tulnp | grep ':8080'               # 确认端口是否被占用
```

---

### Recv-Q / Send-Q 排障

| 状态 | Recv-Q | Send-Q |
|------|--------|--------|
| **LISTEN** | 当前积压连接数 | 最大 backlog 值 |
| **ESTABLISHED** | 应用还没读的数据 | 对端还没收的数据 |

> [!warning] Recv-Q / Send-Q 解读口诀
> - 两边都大：网络瓶颈
> - 仅 Recv-Q 大：应用处理慢
> - 仅 Send-Q 大：对端处理慢或网络拥堵

---

### `ss` vs `netstat` 性能对比

| 测试场景 | `ss` | `netstat` |
|---------|------|-----------|
| 10,000 个连接 | 0.10s | 2.3s |
| 100,000 个连接 | 0.45s | 30+s |

> [!warning] 生产环境建议
> 在有大量连接（>5000）的服务器上，**永远不要用 `netstat`**。`ss` 不仅快 10-100 倍，而且输出格式更一致。

---

### 本章小结

- **TCP 是有状态的协议**，理解状态机是排查连接问题的基本功
- **连接五元组**是本层核心概念
- **`ss -tulnp`** 查看监听端口，**`ss -tanp`** 查看所有连接
- **`ss -i`** 查看 TCP 内部参数（RTT、cwnd、重传字节数）
- **Recv-Q / Send-Q** 是 Socket 缓冲区的积压指标
- **`ss` 比 `netstat` 快 10-100 倍**

#### 下章预告

下一章我们将 Wi-Fi 上空——**无线网络信息**。

---

---

## 第八章：无线网络信息

### 从有线到无线：多了什么

有线网络的信息查询核心在接口、IP、路由——这些概念在无线环境下依然存在，但无线多了两个关键维度：**信号质量**和 **AP 关联状态**。

---

### iw vs iwconfig：新旧工具链

| 对比维度 | `iw`（现代） | `iwconfig`（旧版） |
|---------|-------------|-------------------|
| 内核接口 | nl80211（netlink） | Wireless Extensions（ioctl） |
| 维护状态 | 活跃维护 | 2009 年后基本停滞 |
| 输出格式 | 结构化，可脚本解析 | 纯文本 |

---

### `iw dev`：查看无线网卡

```bash
sudo iw dev
# phy#0
#     Interface wlan0
#         addr  a4:5e:60:xx:xx:xx
#         type managed
#         channel 6 (2437 MHz), width: 20 MHz
```

---

### `iw dev wlan0 link`：查看当前连接状态

这是无线排查最常用的命令——**不需要扫描，只输出当前关联的 AP 信息**。

```bash
iw dev wlan0 link
# Connected to 12:34:56:78:9a:bc
#     SSID: MyHomeWiFi
#     freq: 5180
#     signal: -45 dBm
#     tx bitrate: 200.0 MBit/s MCS 5
```

| 指标 | 含义 |
|------|------|
| `signal` | 信号强度 dBm，**绝对值越小越强** |
| `tx bitrate` | 物理层速率，实际吞吐量约为 50%-70% |

---

### `iw dev wlan0 scan`：扫描 AP

```bash
sudo iw dev wlan0 scan | grep -E 'SSID|signal|freq|WPA|RSN'
```

需要 root 权限，扫描期间当前连接会短暂中断。

---

### `nmcli device wifi`：用 NetworkManager 管理无线

```bash
nmcli device wifi list                    # 扫描并列出 WiFi（不需要 root）
nmcli device wifi connect "SSID" password "pwd"  # 连接 WiFi
nmcli device wifi rescan                  # 强制重新扫描
nmcli device disconnect wlan0             # 断开连接
```

> [!tip] `nmcli` vs `iw` 选择建议
> - 快速查看可用网络：`nmcli device wifi list`
> - 深度排查信号质量：`iw dev wlan0 link`
> - 底层扫描数据：`iw dev wlan0 scan`

---

### 无线信号质量指标解读

**dBm 参考表**：

| dBm 范围 | 质量评级 |
|---------|---------|
| -30 ~ -50 | 极好 |
| -50 ~ -60 | 良好 |
| -60 ~ -70 | 一般 |
| -70 ~ -80 | 较差 |
| < -90 | 不可用 |

> [!warning] dBm 是负数，绝对值越小信号越强
> -45 dBm 比 -75 dBm 信号好。

**实际 TCP 吞吐量 ≈ PHY 速率 × 0.5 ~ 0.7**

---

### 本章小结

- **`iw` 是现代 Linux 无线查询标准工具**
- **`iw dev wlan0 link`** 查看当前连接状态（SSID、信号强度 dBm、TX/RX 速率）
- **`nmcli device wifi`** 提供更高级的无线管理
- **dBm 越小越强**，-50 算优，-75 算差

#### 下章预告

下一章从无线切换到**网络监控与统计**。

---

---

## 第九章：网络监控与统计

### 从"通不通"到"用多少"

前面章节关注的都是"网络能不能用"——IP 配了吗？路由通了吗？DNS 解析对吗？但实际运维中还有一个无法回避的问题：**网络到底用了多少？**

这些工具回答的不是"通不通"，而是"用多少""谁在用""稳不稳"。

---

### 网络监控四维分类

| 维度 | 分类 | 代表工具 |
|------|------|---------|
| 时间维度 | 实时 | `iftop`、`nload`、`bmon`、`nethogs` |
| | 历史 | `vnstat` |
| 粒度维度 | 接口级 | `nload`、`bmon`、`/proc/net/dev` |
| | 连接级 | `iftop` |
| | 进程级 | `nethogs` |
| 统计维度 | 流量 | `iftop`、`nload`、`vnstat` |
| | 错误 | `ethtool -S`、`ip -s link` |

---

### iftop：按连接查看实时带宽

```bash
iftop -i eth0 -n           # 监听 eth0，不反解 DNS
iftop -i eth0 -n -P        # 同时显示端口号
iftop -i eth0 -n -f "port 443"  # 只看特定端口
```

交互快捷键：`n` 切换 DNS，`p` 切换端口，`1/2/3` 切换排序列，`q` 退出。

---

### nload：简洁流量总览

```bash
nload -u M eth0            # 以 MB/s 监控 eth0
```

> [!warning] 单位陷阱
> `nload` 默认以 bit/s 显示，**习惯性加 `-u M` 参数**切换为 MB/s。

---

### nethogs：按进程归因流量

```bash
sudo nethogs eth0          # 监控 eth0
sudo nethogs any           # 监控所有接口
```

显示 PID、用户、程序路径、发送和接收速率。交互快捷键：`m` 切换单位，`s` 按发送排序，`r` 按接收排序。

> [!tip] 发现偷跑流量的程序
> 当带宽异常时，`nethogs` 直接显示哪个进程（PID）在消耗带宽。

---

### bmon：ASCII 图表 + 详细统计

```bash
bmon -p eth0               # 监控指定接口
```

上面板是 ASCII 折线图（流量变化趋势），下面板是详细数值统计（Rx/Tx 的 Bytes、Packets、Errors、Dropped）。

---

### ethtool -S：网卡硬件级统计

```bash
sudo ethtool -S eth0 | grep -E "(error|drop|miss|crc|collision)"
```

| 指标 | 正常值 | 异常含义 |
|------|--------|---------|
| `rx_crc_errors` | 持续为 0 | 网线/网卡硬件问题 |
| `rx_missed_errors` | 接近 0 | 硬件缓冲不足 |
| `tx_carrier_errors` | 接近 0 | 网线松动 |

---

### vnstat：历史流量统计

```bash
vnstat -i eth0             # 默认统计（当日、当月、全部）
vnstat -i eth0 -m          # 查看本月统计
vnstat -i eth0 -d          # 查看今日统计
vnstat -l -i eth0          # 实时模式
```

> [!tip] 建立"正常值"基线
> 持续运行 `vnstat` 一周后，你就知道这台机器的日常流量基线。当某天流量突然翻倍时，你立刻就能感知到异常。

---

### `/proc/net/dev`：底层数据源

所有监控工具的根基是同一个文件：`/proc/net/dev`。

```bash
cat /proc/net/dev
# Inter-|   Receive  ...  |  Transmit ...
#  eth0: 987654321 654321 0 2 ...
```

所谓"实时带宽"就是两次读取的差值除以时间间隔。

---

### 各工具适用场景对比

| 场景 | 推荐工具 |
|------|---------|
| 快速看一眼当前总带宽 | `nload -u M eth0` |
| 哪个连接最占带宽 | `iftop -i eth0 -n -P` |
| 哪个程序在偷跑流量 | `sudo nethogs eth0` |
| 看流量变化趋势 | `bmon -p eth0` |
| 检查网卡硬件问题 | `sudo ethtool -S eth0` |
| 月度流量报告 | `vnstat -i eth0 -m` |
| 编写自定义监控脚本 | `cat /proc/net/dev` |

---

### 本章小结

- 网络监控按**时间维度**分实时和历史，按**粒度**分接口级、连接级、进程级
- **`iftop`** 按连接展示实时带宽
- **`nload`** 最简洁的接口级总带宽视图，务必加 `-u M`
- **`nethogs`** 唯一能按 PID 归因的工具
- **`ethtool -S`** 网卡硬件级统计
- **`vnstat`** 记录历史流量，适合建立流量基线
- **`/proc/net/dev`** 是底层数据源

#### 下章预告

下一章进入抓包分析的世界——**`tcpdump`**。

---

---

## 第十章：抓包与协议分析基础

前面九章我们一直在用各种命令"读"网络信息——读路由表、读连接状态、读 DNS 记录。但有一个更本质的方式：**直接看网线上跑的数据包**。这就是抓包（packet capture）。

比起读统计数据，看原始报文能让你看到更底层的东西——某次连接到底有没有握手成功？哪个包丢了？重传了几次？对方回了什么标志位？这些在 `ss` 或 `ping` 的输出里看不到，但在 `tcpdump` 的输出里一清二楚。

---

### 1. tcpdump 基础用法

#### 安装确认

```bash
sudo apt install tcpdump -y    # Debian/Ubuntu
sudo pacman -S tcpdump         # Arch Linux
```

#### 选择接口：`-i`

```bash
sudo tcpdump -i eth0           # 监听特定接口
sudo tcpdump -i any            # 监听所有接口
sudo tcpdump -i lo             # 监听回环接口
```

#### 抓取数量：`-c`

```bash
sudo tcpdump -i eth0 -c 5     # 抓 5 个包后退出
```

#### 关闭域名解析：`-n` 和 `-nn`

```bash
sudo tcpdump -i eth0 -c 5 -nn  # 不反解 IP 和端口
```

> [!note] 实战习惯
> 大部分排查场景**始终加 `-nn`**。

#### 最常用的组合

```bash
sudo tcpdump -i any -c 100 -nn   # 轻量诊断
sudo tcpdump -i eth0 -c 50 -nn -v  # 看得更细
sudo tcpdump -i eth0 -nn          # 永不停机
```

---

### 2. BPF 过滤表达式

BPF（Berkeley Packet Filter）是 tcpdump 的过滤语言。

**按 IP 过滤**：
```bash
'tcp and (port 80 or port 443) and not host 192.168.1.1'
```

**按端口过滤**：
```bash
sudo tcpdump -i eth0 -nn port 80
sudo tcpdump -i eth0 -nn src port 80
sudo tcpdump -i eth0 -nn dst port 80
```

**按协议过滤**：
```bash
sudo tcpdump -i eth0 -nn tcp
sudo tcpdump -i eth0 -nn udp
sudo tcpdump -i eth0 -nn icmp
sudo tcpdump -i eth0 -nn arp
```

**复合条件**：
```bash
sudo tcpdump -i eth0 -nn 'tcp and (port 80 or port 443) and not host 192.168.1.1'
```

> [!warning] 表达式组织顺序
> BPF 引擎优先级：`not` > `and` > `or`。复杂表达式建议用括号明确分组。

---

### 3. 抓包存储与读取

```bash
# 写入文件
sudo tcpdump -i eth0 -c 10000 -nn -w capture.pcap

# 读取文件
tcpdump -r capture.pcap -nn
tcpdump -r capture.pcap -nn tcp
tcpdump -r capture.pcap -nn host 192.168.1.1

# 文件轮转（每 100MB 切一个文件，最多保留 20 个）
sudo tcpdump -i eth0 -nn -C 100 -W 20 -w trace.pcap
```

**典型工作流**：服务器上 `-w` 写文件 → 传文件到本地 → `-r` 读取分析。

---

### 4. 报文输出逐字段解读

```
12:34:56.789012 IP 192.168.1.100.54321 > 93.184.216.34.80: Flags [S], seq 12345, ack 0, win 65535, options [mss 1460], length 0
```

| 字段 | 示例值 | 含义 |
|------|--------|------|
| 时间戳 | `12:34:56.789012` | 精确到微秒 |
| 协议 | `IP` | 网络层协议 |
| 源 | `192.168.1.100.54321` | 源 IP.源端口 |
| 目标 | `93.184.216.34.80` | 目标 IP.目标端口 |
| Flags | `[S]` | TCP 标志位 |
| seq | `12345` | 序列号 |
| ack | `0` | 确认号 |
| win | `65535` | 窗口大小 |

**标志位详解**：

| 缩写 | 含义 | 场景 |
|------|------|------|
| `S` | SYN | 三次握手第一个包 |
| `.` | ACK | 几乎所有包都带 |
| `F` | FIN | 四次挥手 |
| `P` | PSH | 立即推送 |
| `R` | RST | 重置连接 |
| `[S.]` | SYN-ACK | 三次握手第二个包 |

**三次握手的完整报文**：

```
12:34:56.000001 IP A.50001 > B.80: Flags [S], seq 1000          ← SYN
12:34:56.000120 IP B.80 > A.50001: Flags [S.], seq 2000, ack 1001  ← SYN-ACK
12:34:56.000150 IP A.50001 > B.80: Flags [.], ack 2001            ← ACK
```

---

### 5. 实用过滤场景

**只看 TCP 三次握手**：
```bash
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & tcp-syn != 0 and tcp[tcpflags] & tcp-ack == 0'
```

**只抓 DNS 查询**：
```bash
sudo tcpdump -i eth0 -nn udp port 53
```

**抓特定对话**：
```bash
sudo tcpdump -i eth0 -nn host 192.168.1.100 and host 10.0.0.5 and tcp port 80
```

**排除自己的 SSH 流量**：
```bash
sudo tcpdump -i eth0 -nn not port 22
```

---

### 6. 权限说明

tcpdump 需要 root 或 capabilities：

```bash
# 方案一：sudo（最简单，推荐临时使用）
sudo tcpdump -i eth0 -nn

# 方案二：设置 CAP_NET_RAW 能力
sudo setcap cap_net_raw,cap_net_admin+eip $(which tcpdump)

# 方案三：加入 wireshark 组
sudo usermod -a -G wireshark $USER
```

> [!warning] capabilities 的安全风险
> 生产环境建议仅在诊断期间临时开放，用完后移除：`sudo setcap -r $(which tcpdump)`

---

### 7. 与其他工具的配合

**tcpdump + Wireshark**：服务器上 `tcpdump -w` 抓包，本地用 Wireshark 图形化分析。

**tcpdump + tshark**：Wireshark 的命令行版本，适合复杂分析：
```bash
tshark -r capture.pcap -T fields -e ip.src -e tcp.srcport -e http.request.uri
```

**tcpdump + ngrep**：按包内容匹配：
```bash
sudo ngrep -d eth0 -q 'GET /api' port 80
```

---

### 本章小结

- **tcpdump 是命令行抓包的工业标准**
- **基础三参数必记**：`-i` 指定接口、`-c` 限制数量、`-nn` 禁用域名解析
- **BPF 过滤表达式**是精准定位流量的关键
- **抓包三段式**：本地 `-w` 写文件 → 传文件 → `-r` 读取分析
- **报文输出解读是基本功**：重点看 Flags、seq、ack
- **权限**：需要 root 或 `CAP_NET_RAW` + `CAP_NET_ADMIN`
- **联合使用**：tcpdump + Wireshark 覆盖从采集到分析的完整链路

### 下一步学什么

至此，整个《Linux 网络信息获取与概念》的十章节内容已全部完成。从第一章的全局框架到本章的原始报文分析，你走通了从"看配置"到"看线缆"的全路径。建议回到第一章的速查表，对照你实际遇到过的网络问题做一次交叉复习——命令只有融入真实排查场景才真正内化。

---

---

## 结语

至此，整本《Linux 网络信息获取与概念》的十章内容全部完成。

我们从最底层的**网络接口与链路层**出发（MAC 地址、MTU、`ip link`、`ethtool`），向上经过 **IP 地址与子网**（CIDR、`ip addr`、特殊地址），进入**路由表**（最长前缀匹配、`ip route get`、策略路由），再到 **DNS 解析**（`dig`、`resolvectl`、systemd-resolved 体系），回到 **ARP 与邻居发现**（IP→MAC 映射、邻居状态机），升入传输层 **Socket 连接**（TCP 状态机、`ss` 命令、Recv-Q/Send-Q），途径 **无线网络**（`iw`、`nmcli`、信号质量），横跨**网络监控与统计**（`iftop`、`nload`、`nethogs`、`vnstat`），最终以 **tcpdump 抓包分析** 收尾——走通了一条从"看配置"到"看线缆"的完整学习路径。

### 核心收获

1. **分层思维是排查的根本框架**——问题出在哪一层，就用哪一层的工具查。链路层查 `ip link`，网络层查 `ip addr` / `ip route`，传输层查 `ss`，应用层查 `dig`。
2. **`iproute2` 是现代标准**——`ip`、`ss`、`bridge` 三位一体替代了 `ifconfig`、`netstat`、`arp`、`route` 四个旧工具。`ip -j` JSON 输出让脚本化运维更可靠。
3. **缓存是排障的第一道关卡**——DNS 缓存（`resolvectl flush-caches`）、ARP 缓存（`ip neigh flush`）、浏览器缓存——排查前先清缓存，排除"幽灵问题"。
4. **状态机思维**——TCP 状态机（LISTEN/ESTABLISHED/TIME-WAIT/CLOSE-WAIT）、邻居状态机（REACHABLE/STALE/FAILED）本质上都是"有限状态自动机"，理解它们才能准确解读工具输出。
5. **从统计到真相**——`ss` 告诉你连接状态，`iftop` 告诉你带宽用量，但 `tcpdump` 告诉你真正的报文交换过程。三者结合构成完整的排查链。

### 推荐后续学习方向

- **深入 iptables/nftables**：理解防火墙规则如何影响网络信息查询（比如 ICMP 被过滤导致 ping 假阳性）
- **网络性能调优**：`ss -i` 中看到的 cwnd、RTT、BBR 拥塞控制算法等参数的深入理解和调优
- **容器网络**：Docker bridge、CNI、Overlay 网络（VXLAN/Geneve）对网络信息查询的影响
- **Wireshark 深度分析**：用 `tcpdump` 抓包后用 Wireshark 做 TCP 流追踪、HTTP 请求分析、TLS 握手分析

> **记住**：网络排查的核心不是背命令，而是建立"分层 → 定位 → 工具 → 验证"的问题解决回路。命令只是工具，思维才是武器。
