---
title: "第二章：网络隔离基础 — VLAN 与 VLANIF"
created: 2026-07-29
updated: 2026-07-29
tags:
  - virtual-networking
  - networking
  - learning-note
status: completed
source_project: virtual-networking
---

# 第二章：网络隔离基础 — VLAN 与 VLANIF

> [!note]
> 笔记类型：概念笔记 | 篇幅：中 | 代码示例：有（交换机 VLAN 配置命令）

## 本章要回答的问题

在同一台交换机上，如何让财务部和开发部的网络流量互不可见？当两个部门需要通信时，又如何在不改变物理布线的前提下打通？[[VLAN]]（Virtual Local Area Network）用 4 个字节解决了第一个问题，VLANIF 用一条命令解决了第二个问题。本章从 802.1Q 标准开始，逐步深入到端口配置和三层网关，最终通过一个完整的组网案例串联所有知识点。

---

## 2.1 问题场景：没有 VLAN 的世界

想象一个只有集线器和交换机的传统二层网络。当财务部的 PC-A 发送一个广播帧（如 ARP 请求）时，这个广播帧会扩散到交换机的所有端口。开发部的 PC-B 也会收到这个它根本不关心的广播，浪费 CPU 资源。更严重的是，PC-B 只要把网卡设为混杂模式，就能抓取财务部的所有流量——**完全没有隔离**。

```
   [PC-A] 财务部           [PC-B] 开发部
      |                       |
      +----+----[Switch]----+
           |           |
        [Server1]   [Server2]
```

**广播帧从 PC-A 发出，PC-B 和所有服务器都会收到。**

解决这个问题的传统办法是：物理隔离——用两台独立的交换机，财务部用一台，开发部用一台。但这意味着：
- 成本翻倍（每多一个部门就多一台交换机）
- 灵活性为零（人员跨部门调动时需要物理插拔网线）
- 无法扩展（一个交换机端口用完了只能用另一台）

VLAN 的目标是：**在一台物理交换机上实现多个逻辑交换机的效果**。

---

## 2.2 802.1Q 标准与 VLAN Tag 机制

### 核心原理：在以太网帧中"夹带"一个标签

IEEE 802.1Q 标准的做法非常巧妙——它对标准的以太网帧做了最小的侵入性修改：在源 MAC 地址和 EtherType 字段之间插入一个 **4 字节的 VLAN Tag**。

```
标准以太网帧（无 VLAN）：
┌─────────┬──────────┬──────────┬──────────┐
│ 目的MAC  │ 源MAC    │ 类型/长度 │  载荷    │
│ (6字节)  │ (6字节)  │ (2字节)  │ (46-1500)│
└─────────┴──────────┴──────────┴──────────┘

802.1Q 帧（带 VLAN Tag）：
┌─────────┬──────────┬────────┬──────────┬──────────┐
│ 目的MAC  │ 源MAC    │ TPID   │  TCI     │ 类型/长度 │  载荷    │
│ (6字节)  │ (6字节)  │ (2字节)│ (2字节)   │ (2字节)  │ (46-1500)│
└─────────┴──────────┴────────┴──────────┴──────────┘
                         ↑
                  这 4 字节就是 VLAN Tag
```

这 4 字节的 VLAN Tag 又分为两部分：

| 字段 | 长度 | 值 | 含义 |
|------|------|----|------|
| **TPID** (Tag Protocol Identifier) | 16 位 | `0x8100` | 标记这个帧是 802.1Q 帧 |
| **TCI** (Tag Control Information) | 16 位 | 见下方拆解 | 包含优先级、CFI 和 VLAN ID |

其中 TCI 进一步拆解：

```
TCI (16 bits)：
┌────┬────┬──────────────┐
│PCP │ DEI│   VLAN ID    │
│3bit│ 1bit│   12 bit     │
└────┴────┴──────────────┘
```

- **PCP** (Priority Code Point)：3 位，802.1p 优先级，共 8 级（0-7）
- **DEI** (Drop Eligible Indicator)：1 位，拥塞时可丢弃标记
- **VLAN ID**：12 位，取值范围 0-4095，其中 0 和 4095 保留

### 关键数字：为什么是 4094 个 VLAN？

12 位二进制最大值是 \(2^{12} = 4096\)。但标准规定：
- **VLAN 0**：用于优先级标记，不标识具体 VLAN
- **VLAN 4095**：保留未使用

因此可用范围为 **1-4094**，共 4094 个 VLAN。

> [!note]
> **技术上：** 这 4094 的限制在 1998 年足以满足绝大多数企业网络的需求。但在公有云和多租户数据中心场景下，4094 就远远不够了——这直接催生了 [[VXLAN]] 的 24 位 VNI（约 1600 万）。我们将在第 3 章详细讨论。
>
> **实践中：** 即使在一个中型企业中，4094 个 VLAN 也很少真正用完。真正的瓶颈不在数量，在于 VLAN 依赖物理拓扑——不同交换机上的同一个 VLAN 需要 Trunk 链路打通，跨数据中心时更需要复杂的配置管理。

---

## 2.3 端口类型：Access 与 Trunk

交换机上的每个端口需要配置一种角色，决定它对 VLAN Tag 的处理方式。

### Access 端口

- **用途**：连接终端设备（PC、服务器、打印机）
- **行为**：收到数据帧时，打上该端口的 PVID（Port VLAN ID）；发出数据帧时，剥离 Tag
- **特点**：终端设备完全不知道 VLAN 的存在，它看到的仍然是一个标准的无 Tag 以太网帧

```
终端 PC (无 Tag) ──── Access 端口 (PVID=10) ──── 交换机内部 (带 Tag=10)
```

### Trunk 端口

- **用途**：连接交换机与交换机、或交换机与路由器
- **行为**：允许一个或多个 VLAN 的带 Tag 帧通过；默认情况下不发送 VLAN 1（管理 VLAN）
- **特点**：帧在 Trunk 链路上始终携带 VLAN Tag，接收端交换机根据 Tag 将帧分发到正确的 VLAN

```
交换机 A (Tag=10,20) ──── Trunk 端口 ──── 交换机 B (Tag=10,20)
```

### 配置命令（以华为交换机为例）

```bash
# 进入系统视图
system-view

# === 配置 Access 端口 ===
interface GigabitEthernet0/0/1
  port link-type access          # 设置端口类型为 Access
  port default vlan 10           # 指定该端口属于 VLAN 10
  quit

# === 配置 Trunk 端口 ===
interface GigabitEthernet0/0/24
  port link-type trunk           # 设置端口类型为 Trunk
  port trunk allow-pass vlan 10 20 30   # 允许 VLAN 10、20、30 通过
  quit
```

```bash
# 以 Cisco 交换机为例（语法不同，逻辑相同）
configure terminal
interface GigabitEthernet0/1
  switchport mode access
  switchport access vlan 10
  exit

interface GigabitEthernet0/24
  switchport mode trunk
  switchport trunk allowed vlan 10,20,30
  exit
```

> [!warning]
> **注意**：华为和 Cisco 的配置语法有差异，但逻辑完全一致——Access 端口只属于一个 VLAN，Trunk 端口透传多个 VLAN 的 Tag 帧。

### 一个小实验：验证你的理解

假设有两台交换机通过 Trunk 连接，PC-A 在 VLAN 10 中，PC-B 在 VLAN 20 中：

```
PC-A (VLAN 10) ── [Switch1] ──Trunk── [Switch2] ── PC-B (VLAN 20)
```

**问**：PC-A 发送一个广播帧，PC-B 会收到吗？

**答**：不会。Switch1 在 Access 端口收到 PC-A 的无 Tag 帧后，打上 VLAN 10 的 Tag。Switch1 内部将帧复制到所有属于 VLAN 10 的端口——Trunk 端口允许 VLAN 10 通过，因此帧带着 Tag=10 通过 Trunk 到达 Switch2。Switch2 发现 Tag=10，只将帧转发给 VLAN 10 的端口，而 PC-B 在 VLAN 20，所以不会收到。这就是 VLAN 隔离的本质。

---

## 2.4 VLANIF：打通 VLAN 之间的通信

VLAN 实现了隔离，但隔离不是最终目的——大多数场景下，不同 VLAN 仍然需要通信（财务部需要访问开发部的服务器）。传统办法是在 VLAN 间连接一台路由器，每个 VLAN 占用一个路由器端口。

```
[路由器]
  |     |     |
 VLAN10 VLAN20 VLAN30
  |     |     |
 [交换机]
```

这种方案的缺点很明显：有多少个 VLAN 就需要多少个路由器端口和线缆。

### VLANIF：三层逻辑接口

VLANIF 是交换机内部的一个 **三层逻辑接口**。它本质上是一个虚拟的"路由器端口"，绑定到某个 VLAN，为该 VLAN 内的主机提供网关功能。

```
┌──────────────────────────────────┐
│            交换机                 │
│                                  │
│  ┌─────────┐    ┌───────────┐    │
│  │  VLAN 10 │    │ VLANIF 10 │    │
│  │  (二层)  │◄──►│ 10.0.1.1  │    │
│  └─────────┘    └───────────┘    │
│                                  │
│  ┌─────────┐    ┌───────────┐    │
│  │  VLAN 20 │    │ VLANIF 20 │    │
│  │  (二层)  │◄──►│ 10.0.2.1  │    │
│  └─────────┘    └───────────┘    │
│                                  │
│       ┌──────────────────┐       │
│       │  三层转发引擎      │       │
│       │  (路由查表)       │       │
│       └──────────────────┘       │
└──────────────────────────────────┘
```

**工作原理**：
1. PC-A（VLAN 10, IP 10.0.1.2）发送数据给 PC-B（VLAN 20, IP 10.0.2.2）
2. PC-A 发现目标 IP 不在同一子网，将数据帧发往默认网关 10.0.1.1（即 VLANIF 10）
3. 交换机在 VLANIF 10 收到数据包，进行三层路由查表
4. 路由表指示目标网络 10.0.2.0/24 通过 VLANIF 20 可达
5. 交换机重写源/目的 MAC 地址，通过 VLANIF 20 将帧发出
6. VLAN 20 的 Access 端口收到帧，剥离 Tag，送达 PC-B

### 配置命令

```bash
# 创建 VLAN
vlan batch 10 20

# 创建 VLANIF 并配置 IP（作为网关）
interface Vlanif10
  ip address 10.0.1.1 255.255.255.0
  quit

interface Vlanif20
  ip address 10.0.2.1 255.255.255.0
  quit
```

配置完成后，VLAN 10 和 VLAN 20 之间自动具备三层路由能力。不需要额外的路由器硬件。

---

## 2.5 完整配置示例：企业部门组网

### 网络拓扑

```
                         [核心交换机]
                         VLANIF 10: 192.168.10.1/24
                         VLANIF 20: 192.168.20.1/24
                         VLANIF 30: 192.168.30.1/24
                        /       |        \
                   [Trunk]   [Trunk]    [Trunk]
                     /         |          \
           [接入交换机1]  [接入交换机2]  [接入交换机3]
            VLAN 10       VLAN 20       VLAN 30
           (财务部)      (开发部)      (服务器区)

PC-A: 192.168.10.2/24  网关 192.168.10.1
PC-B: 192.168.20.2/24  网关 192.168.20.1
Srv:  192.168.30.2/24  网关 192.168.30.1
```

### 配置步骤

**步骤 1：核心交换机配置 VLAN 和 VLANIF**

```bash
system-view
sysname Core-Switch

# 创建 VLAN
vlan batch 10 20 30

# 配置 Trunk 端口（连接接入交换机）
interface GigabitEthernet0/0/1
  port link-type trunk
  port trunk allow-pass vlan 10
  quit

interface GigabitEthernet0/0/2
  port link-type trunk
  port trunk allow-pass vlan 20
  quit

interface GigabitEthernet0/0/3
  port link-type trunk
  port trunk allow-pass vlan 30
  quit

# 配置 VLANIF（三层网关）
interface Vlanif10
  ip address 192.168.10.1 255.255.255.0
  quit

interface Vlanif20
  ip address 192.168.20.1 255.255.255.0
  quit

interface Vlanif30
  ip address 192.168.30.1 255.255.255.0
  quit
```

**步骤 2：接入交换机 1（财务部）配置**

```bash
system-view
sysname Access-Switch1

# 创建 VLAN
vlan batch 10

# 上联端口（连核心交换机）配置为 Trunk
interface GigabitEthernet0/0/24
  port link-type trunk
  port trunk allow-pass vlan 10
  quit

# 下联端口（连 PC）配置为 Access
interface GigabitEthernet0/0/1
  port link-type access
  port default vlan 10
  quit

# 其他 PC 端口类似... 不再一一列出
```

**步骤 3：验证配置**

```bash
# 查看 VLAN 信息
display vlan
# 输出示例：
# -------------------------------------------------------------------------------
# VID  Type    Ports
# -------------------------------------------------------------------------------
# 1    common  GE0/0/1(D)  GE0/0/2(D)  ...
# 10   common  GE0/0/1(U)  GE0/0/24(U)  ...
# 20   common  GE0/0/2(U)  GE0/0/24(U)  ...
# 30   common  GE0/0/3(U)  GE0/0/24(U)  ...

# 查看 VLANIF 接口状态
display ip interface brief Vlanif10
# 输出示例：
# *down: administratively down
# Interface                 IP Address/Mask      Physical   Protocol
# Vlanif10                  192.168.10.1/24      up         up

# 测试 VLAN 间连通性
ping 192.168.20.2
# 输出示例（应从核心交换机 ping 通 PC-B）：
# PING 192.168.20.2: 56 data bytes
# 64 bytes from 192.168.20.2: icmp_seq=0 ttl=128 time=1 ms
# 64 bytes from 192.168.20.2: icmp_seq=1 ttl=128 time=1 ms
```

### 测试结果预期

| 测试场景 | 期望结果 | 原理 |
|---------|---------|------|
| PC-A ping PC-B (跨 VLAN) | 成功 | VLANIF 提供三层路由 |
| PC-A 广播 | 仅 VLAN 10 内设备收到 | VLAN 隔离广播域 |
| PC-B 抓包（混杂模式） | 抓不到 VLAN 10 的流量 | VLAN Tag 隔离数据帧 |

---

## 2.6 VLAN 的局限

VLAN 是虚拟网络的伟大起点，但它有几个根本性局限。理解这些局限，也就理解了为什么需要 [[VXLAN]] 和 [[Overlay网络]]。

| 局限 | 说明 | 后续方案 |
|------|------|---------|
| **4094 上限** | 12 位 VLAN ID 只有 4094 个可用 | [[VXLAN]] 的 24 位 VNI（1600 万） |
| **依赖物理拓扑** | VLAN 是二层技术，跨三层边界需要额外配置 | VXLAN Overlay 隧道跨越三层网络 |
| **STP 限制** | 生成树协议阻塞冗余链路，降低带宽利用率 | ECMP 多路径负载均衡 |
| **广播域仍然存在** | 每个 VLAN 是一个广播域，大量 ARP 请求在 VLAN 内泛滥 | ARP 抑制、头端复制优化 |
| **配置分散** | 每台交换机都需要单独配置 VLAN 和端口 | [[SDN]] 集中控制器下发配置 |

---

## 本章总结

- **802.1Q** 通过在以太网帧中插入 4 字节 VLAN Tag 实现 VLAN 标识，其中 12 位 VLAN ID 支持 4094 个逻辑网络
- **Access 端口**连接终端设备，自动打 Tag 和剥 Tag；**Trunk 端口**连接交换机，透传多个 VLAN 的 Tag 帧
- **VLAN** 实现了二层广播域隔离——不同 VLAN 的帧互不可见
- **VLANIF** 是三层逻辑接口，为 VLAN 提供网关和路由能力，使跨 VLAN 通信不需要额外路由器硬件
- VLAN 的 4094 上限和二层依赖是主要瓶颈，为 VXLAN 等 Overlay 技术铺平了道路

## 下一章预告

VLAN 用 4 字节实现了 4094 个网络。下一章我们将看到 [[VXLAN]] 如何用 MAC-in-UDP 封装技术，将虚拟网络的数量扩展到 1600 万，并让虚拟网络彻底脱离物理拓扑的限制。你将理解 Overlay/Underlay 的分层架构，以及 VTEP、VNI、BD 等关键组件的作用。
