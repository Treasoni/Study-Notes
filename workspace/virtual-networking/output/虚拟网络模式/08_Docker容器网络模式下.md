---
title: "第八章：Docker 容器网络模式（下）— 跨主机与高性能模式"
created: 2026-07-29
updated: 2026-07-29
tags:
  - virtual-networking
  - networking
  - learning-note
status: completed
source_project: virtual-networking
---

# 第8章：Docker 容器网络模式（下）— 跨主机与高性能模式

## 8.1 引言：单机模式的边界

上一章我们学习了 [[Bridge模式|Bridge]]、Host、Container、None 四种单机模式。它们的共同局限：**只能在一台宿主机上工作**。

想象这样一个场景：你有三台服务器，每台运行了 N 个容器。要让 A 服务器的容器访问 B 服务器的容器，Bridge 模式下只能通过 `宿主机IP:端口映射` 的方式——这要求你手动管理每台宿主机的端口分配，还要处理端口冲突、服务发现等问题。当容器数量超过几十个时，这种方式就不可维护了。

本章介绍的三种模式从不同角度解决了这个问题：

| 模式 | 解决什么问题 | 本质方案 |
|------|-----------|---------|
| **[[Overlay网络|Overlay]]** | 跨主机通信，零修改现网 | [[VXLAN]] 隧道封装 |
| **[[Macvlan]]** | 高性能直连物理网络 | 容器获得独立 MAC 地址 |
| **[[Ipvlan]]** | 兼容性更好的高性能方案 | 容器共享 MAC，内核路由 |

## 8.2 Overlay 模式：VXLAN 隧道跨主机通信

### 8.2.1 为什么需要 Overlay？

设想你有一台物理服务器，IP 是 `192.168.1.10`，上面跑着容器 A（`10.0.1.2`）。第二台物理服务器 IP 是 `192.168.1.20`，上面跑着容器 B（`10.0.2.2`）。问题来了：

**容器 A 怎么知道 10.0.2.2 在另一台机器上？**

两种思路：

1. **打通物理网络**：在物理交换机上配置路由，告诉它 10.0.x.x 的下一跳。但这需要网络工程师介入，周期长、不灵活。
2. **Overlay 隧道**：把容器的数据包封装起来，底层通过宿主机的物理 IP 传递。物理网络不需要知道上层网络的存在。

Docker [[Overlay网络|Overlay]] 模式选择的就是方案 2。

### 8.2.2 VXLAN 封装原理

我们在第三章详细学习过 [[VXLAN]]。Docker Overlay 模式就是 VXLAN 的一个实际应用：

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ 外层 MAC头   │ 外层 IP头    │ UDP头        │ VXLAN头      │
│ (14 字节)    │ (20 字节)    │ (8 字节)     │ (8 字节)     │
│              │ 目的端口:4789 │ dport:4789   │ VNI: 24bit  │
│              │              │              │              │
├──────────────┴──────────────┴──────────────┴──────────────┤
│                     原始以太网帧 (内层)                     │
│             包含容器 MAC + 容器 IP + 载荷                   │
└───────────────────────────────────────────────────────────┘

← 总开销：50 字节（20 IP + 8 UDP + 8 VXLAN + 14 内层 MAC）→
```

整个过程可以概括为三步：

```
[容器A] 发送数据包 → Docker 识别目标不在本地
    → VXLAN 封装（原始包 + 50 字节头）
    → 经过宿主机的物理网卡发送到目标宿主机
    → 目标宿主机解封装 → 送到容器B
```

### 8.2.3 部署前提：Docker Swarm

Overlay 模式**不能直接使用**，需要先初始化 [[Docker Swarm]]：

```bash
# 1. 在管理节点初始化 Swarm
docker swarm init --advertise-addr 192.168.1.10

# 2. 获取加入 Token（在管理节点上执行）
docker swarm join-token worker

# 3. 在工作节点加入 Swarm
docker swarm join --token SWMTKN-1-xxxx 192.168.1.10:2377

# 4. 创建 Overlay 网络
docker network create --driver overlay \
  --subnet 10.0.100.0/24 \
  --gateway 10.0.100.1 \
  my-overlay-net
```

为什么需要 Swarm？因为 Overlay 网络需要**分布式控制平面**来协调各节点的 VXLAN 配置——谁在哪个子网、VTEP 地址是什么、VNI 怎么分配。Swarm 的集群管理功能提供了这些元数据同步机制。

### 8.2.4 MTU 调整：一个不能忽视的细节

VXLAN 封装增加了 50 字节开销。如果物理网络的 MTU 是 **1500**，VXLAN 封装后总大小变成 **1550** 字节，超过了物理链路 MTU：

```bash
# 没有调整 MTU 的后果
docker run --network my-overlay-net alpine ping -M do -s 1472 google.com

# -M do: 禁止分片，-s 1472: ICMP 载荷大小
# 如果物理链路 MTU=1500，VXLAN 封装后变成 1522 字节，超过限制
# 结果：ping 失败（Fragmentation required）
```

正确的做法是调整容器网络的 MTU 为 **1450**：

```bash
# 创建 Overlay 网络时指定 MTU
docker network create --driver overlay \
  --opt mtu=1450 \
  --subnet 10.0.100.0/24 \
  my-overlay-net
```

1450 的计算方式：1500（标准以太网） - 50（VXLAN 封装开销） = 1450。

> [!note]
> 如果底层网络支持 Jumbo Frame（MTU 9000），VXLAN 网络的 MTU 可设为 8950，在跨主机大数据传输场景下有显著性能提升。

### 8.2.5 性能损耗评估

Overlay 模式的性能损耗来自三个层面：

| 损耗来源 | 具体原因 | 典型开销 |
|---------|---------|---------|
| **封装/解封装** | VXLAN 头部的添加和移除，由 CPU 完成（软件 VTEP） | ~5% CPU |
| **额外的网络跳数** | 数据包多经过一段 VXLAN 隧道 | 每跳 +1.1ms 延迟 |
| **吞吐量下降** | 封装开销 + 分片风险 + 额外处理 | 5-15%（小包）；大包场景高达 60% |
| **加密额外开销** | 启用 IPSec 加密时的额外负载 | TCP 吞吐额外降低 20-30% |

一个经验性的性能数据对比：

```
Host 模式:  ~0.02ms 延迟, 95%+ 吞吐
Bridge 模式: ~0.05ms 延迟, 80-90% 吞吐
Overlay 模式: ~1.2ms 延迟, 85-95% 吞吐（小包）/ 40-95% 吞吐（大包）
```

### 8.2.6 Overlay 模式的最佳实践

```bash
# 1. 生产环境使用自定义 Overlay 网络，而非默认 overlay
#    自定义网络允许你精确控制子网、MTU 和 IPAM

# 2. 设置合理的 MTU 值
docker network create --driver overlay \
  --opt mtu=1450 \
  --subnet 10.0.100.0/22 \
  my-overlay

# 3. 通过 attachable 选项让独立容器也能接入
docker network create --driver overlay \
  --attachable \
  my-overlay

# 4. 加密敏感流量（如果有跨安全域通信需求）
docker network create --driver overlay \
  --opt encrypted \
  secure-overlay
```

> [!warning] 加密选项说明
> 加密选项 `--opt encrypted` 在控制平面和数据平面都启用 IPSec 加密。启用后 VXLAN 数据包自动加密，但性能会额外下降 20-30%。仅在跨不可信网络时启用。

## 8.3 Macvlan 模式：容器直连物理网络

### 8.3.1 原理：给容器一张「独立网卡」

[[Macvlan]] 模式的核心思想：**给每个容器分配一个独立的 MAC 地址**，让它像一台真实的物理机一样挂在二层网络上。

```
宿主机（192.168.1.100, MAC: aa:bb:cc:dd:ee:01）
    │
    ├── 容器 A (192.168.1.101, MAC: ee:ff:00:11:22:33)
    ├── 容器 B (192.168.1.102, MAC: ee:ff:00:11:22:34)
    └── 容器 C (192.168.1.103, MAC: ee:ff:00:11:22:35)

宿主机网卡（eth0）进入混杂模式（promiscuous mode）
    │
    ▼
物理交换机 ← 看到 4 个 MAC 地址（宿主机 + 3 个容器）
```

在物理交换机看来，这 4 个 MAC 地址都连接在同一个端口上。交换机不需要知道 [[Docker]] 的存在，它以为有 4 台独立的设备接入网络。

### 8.3.2 创建 Macvlan 网络

```bash
# 假设物理网卡 eth0 连接在 192.168.1.0/24 网段，网关 192.168.1.1
docker network create --driver macvlan \
  --subnet 192.168.1.0/24 \
  --gateway 192.168.1.1 \
  -o parent=eth0 \
  my-macvlan-net

# 启动容器，直接获取同网段 IP
docker run -d --name macvlan-nginx \
  --network my-macvlan-net \
  --ip 192.168.1.200 \
  nginx:alpine

# 验证：无需端口映射，外部可直接访问 192.168.1.200:80
curl http://192.168.1.200:80
```

Macvlan 模式**不需要端口映射**。容器的 IP 直接暴露在物理网络中，外部可以像访问一台普通服务器一样访问容器。

### 8.3.3 Macvlan 的四种工作模式

| 模式 | 说明 | 容器间通信 | 适用场景 |
|------|------|-----------|---------|
| **Bridge**（默认） | 容器通过宿主机内部虚拟网桥互通 | 支持 | 多数场景 |
| **VEPA** | 流量必须经过外部交换机再回来 | 需要外部交换机 hairpin 模式 | 合规审计场景 |
| **Private** | 容器间禁止通信 | 不互通 | 安全隔离强需求 |
| **Passthru** | 物理网卡直通到单个容器 | 单个容器独占 | 极致性能 |

```bash
# 创建 VEPA 模式
docker network create --driver macvlan \
  -o parent=eth0 -o macvlan_mode=vepa \
  --subnet 192.168.1.0/24 \
  my-vepa-net

# 创建 Private 模式（容器间完全隔离）
docker network create --driver macvlan \
  -o parent=eth0 -o macvlan_mode=private \
  --subnet 192.168.1.0/24 \
  my-private-net
```

### 8.3.4 性能优势

Macvlan 模式在性能上非常接近 Host 模式：

| 维度 | Macvlan 数据 |
|------|-------------|
| 延迟 | ~0.03ms（仅比 Host 多 0.01ms） |
| 吞吐量 | ~9.8 Gbps（几乎占满万兆网卡） |
| CPU 开销 | ~5%（仅用于 MAC 地址处理，无 NAT） |

Macvlan 绕过了 docker0 网桥和 iptables NAT，数据路径更短：

```
Macvlan 路径: 容器 → 直接通过物理网卡发送（MAC 地址替换）
Bridge 路径:  容器 → veth → docker0 → iptables NAT → 物理网卡
```

### 8.3.5 限制与注意事项

#### Linux 独占
Macvlan 是 Linux 内核特性，macOS 和 Windows 上不可用（Docker Desktop 不支持）。

#### 容器无法与宿主机通信（最令人困惑的陷阱）

```bash
# 容器（192.168.1.200）尝试访问宿主机（192.168.1.100）
docker exec macvlan-nginx ping 192.168.1.100
# 失败！没有响应

# 宿主机尝试访问容器
ping 192.168.1.200
# 失败！
```

**原因**：Linux 内核拒绝接收来自自身子接口的 MAC 地址的包。宿主机 eth0 和容器共享同一个物理网卡，但从主机视角看，容器 MAC 属于"子接口"范畴，内核的 MAC 地址过滤逻辑直接丢弃了来自这些子接口指向宿主机自己的包。

**解决方案**：让容器通过宿主机上的另一个子接口（如 `eth0.100`）与宿主机通信，或通过 `--aux-address` 预留一个地址给宿主机。

#### 云平台不可用

```bash
# AWS EC2、阿里云 ECS 等需要端口映射
# 云厂商 MAC 地址过滤机制会丢弃非注册 MAC 的数据包
# 在这些环境中 Macvlan 基本不可用
```

**原因**：云平台的虚拟交换机（如 AWS 的 VPC 路由器）有自己的 MAC 地址学习机制，不允许虚拟机使用未经 VPC 管理的 MAC 地址发送数据包。容器产生的 MAC 地址不在云平台的许可范围内，数据包会被直接丢弃。

#### ESXi MAC 地址数量限制

在 vSphere 环境下，每个虚拟交换机的端口（即每台虚拟机的虚拟网卡）默认限制最多允许的 MAC 地址数量。超过限制后数据包会被丢弃。

**解决方案**：在 ESXi 中设置 `vlan.maccount` 参数，或使用 [[Ipvlan]] 模式替代。

## 8.4 IPvlan 模式：共享 MAC 的高性能方案

### 8.4.1 原理：所有容器共享父接口的 MAC

[[Ipvlan]] 与 Macvlan 的最大区别：**所有容器共享父接口的 MAC 地址**，但各有独立的 IP 地址。

```
宿主机（192.168.1.100, MAC: aa:bb:cc:dd:ee:01）
    │
    ├── 容器 A (192.168.1.101, MAC: aa:bb:cc:dd:ee:01) ← 相同 MAC
    ├── 容器 B (192.168.1.102, MAC: aa:bb:cc:dd:ee:01) ← 相同 MAC
    └── 容器 C (192.168.1.103, MAC: aa:bb:cc:dd:ee:01) ← 相同 MAC

在物理交换机看来：只有 1 个 MAC 地址（宿主机的 MAC）
通过 IP 地址区分不同容器
```

这解决了 Macvlan 的几个核心痛点：

1. **MAC 地址表压力**：交换机 MAC 地址表只需要维护宿主机的 1 个条目，而不是几十个
2. **虚拟化平台兼容性**：大多数云平台和虚拟化环境不限制单个 MAC 地址的 IP 数量
3. **ESXi 限制**：不再受 ESXi MAC 数量限制的影响

### 8.4.2 IPvlan 的两种工作模式

#### L2 模式：类似 Macvlan Bridge

```bash
# 创建 IPvlan L2 网络
docker network create --driver ipvlan \
  --subnet 192.168.1.0/24 \
  --gateway 192.168.1.1 \
  -o parent=eth0 \
  -o ipvlan_mode=l2 \
  my-ipvlan-l2
```

L2 模式下，IPvlan 的行为与 Macvlan Bridge 类似——容器可以直接与同网段设备通信，数据包在二层转发。区别在于共享 MAC。

#### L3 模式：内置三层路由隔离

```bash
# 创建 IPvlan L3 网络
docker network create --driver ipvlan \
  --subnet 10.10.1.0/24 \
  --subnet 10.10.2.0/24 \
  -o parent=eth0 \
  -o ipvlan_mode=l3 \
  my-ipvlan-l3
```

L3 模式更值得关注——它实现了**容器级别的三层路由隔离**：

```
10.10.1.0/24 的容器群
    │  不能直接互通（需要经过宿主机路由）
10.10.2.0/24 的容器群
```

L3 模式下，不同子网的容器不能直接二层通信（没有 MAC 寻址），必须经过宿主机内核在 IP 层路由。这意味着：

- **天然隔离**：不同子网间的流量必须经过宿主机内核
- **可控访问**：可以通过 iptables 精确控制跨子网流量
- **无需 VLAN**：在同一个物理网络上实现了多租户隔离

### 8.4.3 内核版本要求

```bash
# 检查内核版本
uname -r

# IPvlan 需要 Linux 内核 >= 4.2
# 推荐内核 >= 4.11（修复了大量 IPvlan 相关 bug）
```

## 8.5 六种模式全面对比

### 8.5.1 性能对比总表

| 模式 | 延迟 | 吞吐量 | CPU 开销 | 跨主机支持 | 端口映射 |
|------|------|--------|---------|-----------|---------|
| **Host** | ~0.02ms | 95%+ 物理网卡 | ~0% | 需要物理 IP | 不需要 |
| **Macvlan** | ~0.03ms | ~9.8 Gbps | ~5% | 依赖物理路由 | 不需要 |
| **Ipvlan** | ~0.03ms | ~9.5 Gbps | ~3% | L3 模式原生支持 | 不需要 |
| **Bridge（自定义）** | ~0.05ms | 中（iptables 瓶颈） | 中 | 需端口映射 | 需要 |
| **Bridge（默认）** | ~0.08ms | 中 | 中 | 需端口映射 | 需要 |
| **Overlay** | ~1.2ms | 损耗 5-15%（大包可达 60%） | 5-33% | 原生支持 | 不需要 |

### 8.5.2 功能对比表

| 特性 | Host | Macvlan | Ipvlan | Bridge | Overlay | None |
|------|------|---------|--------|--------|---------|------|
| 网络隔离 | 无 | 有 | 有（L3 更强） | 有 | 有 | 完全 |
| 内置 DNS | 无 | 无 | 无 | 自定义有 | 有 | 无 |
| 容器↔宿主机通信 | - | 不支持 | 支持 | 支持 | 支持 | 手动 |
| 云平台可用 | 有限 | 不可用 | 可用（L3） | 可用 | 可用 | 可用 |
| 动态连接/断开 | - | 有限 | 有限 | 自定义支持 | 支持 | 支持 |
| 加密通信 | 应用层 | 应用层 | 应用层 | 应用层 | 内置可选 | 应用层 |

### 8.5.3 隔离性/性能/灵活性三角

```
                    隔离性强
                    ↑
        Overlay ────┼──── None
                   /|\
                  / | \
                 /  |  \
          Bridge    |    IPvlan L3
                 \  |  /
                  \ | /
                   \|/
         Macvlan ──┼── Host
                    |
                    ↓
                  性能强

灵活性: Overlay > Bridge > None > IPvlan > Macvlan > Host
部署难度: Overlay > Macvlan > IPvlan > Bridge > Host
```

## 8.6 选型建议

### 8.6.1 按场景推荐

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| **单机开发测试** | 默认 Bridge | 即开即用，无需额外配置 |
| **单机生产环境** | 自定义 Bridge | 内置 DNS + 网络隔离 |
| **跨主机通用方案** | Overlay | 零修改现网，原生跨主机 |
| **极致性能（单机）** | Host | 延迟最低，吞吐最高 |
| **极致性能（跨主机）** | Macvlan | 接近物理网卡性能 |
| **虚拟化平台兼容** | IPvlan L2 | 共享 MAC，平台兼容性好 |
| **多租户隔离** | IPvlan L3 | 子网级别路由隔离 |
| **Sidecar 架构** | Container | 共享网络命名空间 |
| **完全自定义** | None | 手动构建网络栈 |

### 8.6.2 决策流程图

```
开始选型
    │
    ├── 需要跨主机通信吗？
    │   ├── 是 → 物理网络能改吗？
    │   │   ├── 能 → Macvlan（高性能）或 IPvlan L3（兼容性）
    │   │   └── 不能 → Overlay（VXLAN 隧道）
    │   │
    │   └── 否 → 需要极致性能？
    │       ├── 是 → Host 模式（零损耗）
    │       └── 否 → 自定义 Bridge（生产推荐）
    │
    └── 特殊情况？
        ├── Sidecar 模式 → Container
        ├── 完全自定义 → None
        ├── 云平台部署 → Overlay 或 Bridge（避免 Macvlan）
        └── ESXi 环境 → IPvlan（避免 Macvlan MAC 限制）
```

### 8.6.3 避坑清单

1. **不要在生产环境使用默认 docker0**：缺少 DNS 解析，容器重启后 IP 变化会导致服务中断
2. **不要在云平台用 Macvlan**：云厂商的 MAC 地址过滤会丢弃 Macvlan 容器发出的数据包
3. **使用 Overlay 时务必调整 MTU**：VXLAN 50 字节开销，不调整 MTU 会导致大包通信失败
4. **不要在 macOS/Windows 上依赖 Host 模式**：Docker Desktop 的虚拟机实现导致 Host 模式行为不完全一致
5. **Macvlan 容器不能和宿主机直接通信**：这不是 bug，是 Linux 内核的设计选择
6. **Overlay 加密选项要按需启用**：加密对 TCP 吞吐的额外损耗达 20-30%，仅在跨不可信网络时使用
7. **IPvlan L3 模式需要手动配置路由**：不同子网间的流量默认不通，需要宿主机上的路由规则

## 8.7 本章总结

- **[[Overlay网络|Overlay]] 模式**通过 [[VXLAN]] 隧道实现跨主机容器通信，需要 [[Docker Swarm]] 集群支持。数据包每跳增加约 1.1ms 延迟，吞吐损耗 5-15%（大包场景可达 60%），使用时必须调整 MTU 为 1450。
- **[[Macvlan]] 模式**给每个容器分配独立 MAC 地址，容器直连物理网络，延迟仅 0.03ms、吞吐近 10 Gbps。主要限制：Linux 独占、容器不能与宿主机直接通信、云平台不可用、ESXi 有 MAC 数量限制。
- **[[Ipvlan]] 模式**让所有容器共享父接口的 MAC 地址，解决了 Macvlan 的 MAC 数量限制问题。L2 模式类似 Macvlan Bridge，L3 模式提供子网级别的路由隔离。
- **性能排序**：Host > Macvlan > IPvlan > Bridge（自定义）> Bridge（默认）> Overlay。选型时需要在性能、隔离性、灵活性之间做权衡。
- **选型核心原则**：跨主机首选 Overlay（通用）或 Macvlan（高性能）；单机生产用自定义 Bridge；极致性能用 Host；需要平台兼容用 IPvlan。

### 内容预告

至此，Docker 的六种网络模式我们已经全部掌握。下一章将进入容器编排的世界——[[Kubernetes]] 网络模型与 CNI 插件。你会发现，K8s 的核心网络方案（如 [[Flannel]]、[[Calico]]、[[Cilium]]）的底层原理，正是我们这两章学过的技术的延伸和组合。
