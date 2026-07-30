# 虚拟网络模式 — 深度研究

> 收集时间：2026-07-29
> 搜索策略：3 subagent 并行搜索 + 定向精读 10+ 篇文章
> 覆盖范围：5 大方向

---

## 目录

1. [通用虚拟网络基础](#1-通用虚拟网络基础)
2. [虚拟机网络模式](#2-虚拟机网络模式)
3. [Docker 容器网络模式](#3-docker-容器网络模式)
4. [Kubernetes 网络模型](#4-kubernetes-网络模型)
5. [虚拟网络技术对比与选型](#5-虚拟网络技术对比与选型)

---

## 1. 通用虚拟网络基础

### 1.1 VLAN

- **层次**: 数据链路层（L2）
- **原理**: IEEE 802.1Q 标准，在以太网帧头插入 4 字节 VLAN Tag，其中包含 12 位 VLAN ID
- **规模**: 最多 4094 个网络（ID 1-4094）
- **局限**: ID 数量不足；依赖物理拓扑，无法跨越三层边界
- **配置**: 交换机端口设置 `port link-type` + `port default vlan`

### 1.2 VLANIF（三层逻辑接口）

- **层次**: 网络层（L3）
- **功能**: 为 VLAN 提供网关能力，实现跨 VLAN 路由
- **配置**: `interface Vlanif [ID]` + 配置 IP
- **局限**: 受底层 VLAN 4094 上限约束

### 1.3 VXLAN

- **层次**: L2 over L4 UDP（Overlay）
- **原理**: MAC-in-UDP 封装，原始以太网帧作为内层载荷，依次添加 VXLAN 头（8 字节含 24 位 VNI）、UDP 头（目的端口 4789）、外层 IP/MAC 头
- **规模**: 24 位 VNI → 约 1600 万（2^24）独立虚拟网络
- **关键组件**: VTEP（隧道端点，封装/解封装）、VNI（网络标识）、BD（广播域，VNI 1:1 映射）、NVE（网络虚拟化边缘实体）
- **转发模式**:
  - **同子网**: MAC 表直接 VTEP 间封装转发（桥接行为）
  - **不同子网**: 经三层网关 BDIF → 解封装 → 路由 → 重写 MAC → 再封装
- **MAC 学习**: 本地学习（MAC+VNI+入接口）和远端学习（MAC+VNI+远端 VTEP IP）
- **VTEP 部署**: 软件模式（vSwitch，灵活但 CPU 受限）、硬件模式（ASIC，高性能）、混合模式

### 1.4 Overlay / Underlay

- **Underlay**: 底层物理 IP 网络（三层），承载基础传输
- **Overlay**: 在 Underlay 之上构建的逻辑网络（如 VXLAN），与物理拓扑解耦
- **关系**: Underlay 提供连通性，Overlay 提供逻辑隔离。拓扑变化互不影响

### 1.5 SDN

- **定义**: 转发与控制分离 + 集中控制 + 可编程
- **三层架构**:
  1. **基础设施层（数据平面）**: 转发设备仅负责按流表规则转发
  2. **控制层（控制平面）**: SDN 控制器全局视图，南向接口（OpenFlow）下发流表
  3. **应用层**: 网络应用通过北向接口（REST API）调用网络能力
- **OpenFlow**: 最早标准化的南向接口协议，流表匹配/动作机制
- **Google B4 实践**: 网络利用率从 30-40% 提升至 95%

### 1.6 Linux 网络命名空间

- **定义**: 每个 namespace 拥有独立网络栈（网卡、路由表、防火墙、端口号）
- **veth pair**: 虚拟以太网设备对，一端数据入另一端出，用于连接不同 namespace
- **与 bridge 结合**: 实际容器网络中，多个 namespace 的 veth 一端挂到 Linux bridge，由 bridge 充当虚拟交换机
- **基本命令**:
  ```bash
  ip netns add net0                    # 创建 namespace
  ip link add veth0 type veth peer name veth1  # 创建 veth pair
  ip link set veth1 netns net0         # 将一端移入 namespace
  ip netns exec net0 ip addr add 10.1.1.1/24 dev veth1
  ```

### 1.7 精读笔记

#### 资料 1: VLAN/VLANIF/VXLAN 核心对比
- **URL**: https://cloud.tencent.com.cn/developer/article/2512624
- **核心观点**: VLAN 4094 vs VXLAN 1600 万的标识空间差异是本质区别；VLANIF 和 BDIF 功能类似（三层网关）但底层标识机制不同
- **关键数据**: VLAN ID 12 位 → 4094；VNI 24 位 → 1600 万；VXLAN UDP 端口 4789

#### 资料 2: SDN 全面解读
- **URL**: https://www.edu.cn/sdn_12536/20130724/t20130724_992256.shtml
- **核心观点**: SDN 本质是转发与控制分离；Google B4 展现 SDN 实战价值（利用率 95%）；OpenFlow 定义控制器与交换机间的通信标准
- **关键数据**: Google 2010 年启动，2012 年完成部署；网络利用率提升至 95%

#### 资料 3: VXLAN 报文转发过程
- **URL**: https://developer.aliyun.com/article/1588407
- **核心观点**: 同子网转发是桥接（L2），不同子网转发是路由（L3），两者在 VXLAN 中处理完全不同；头端复制列表是广播性能瓶颈

#### 资料 4: Linux 网络命名空间
- **URL**: https://bbs.huaweicloud.com/blogs/148734 + https://cloud.tencent.com.cn/developer/article/2486110
- **核心观点**: namespace 拥有完整独立 Linux 网络协议栈；报文方向取决于视角（Host vs namespace）；veth pair 一端入另一端出

---

## 2. 虚拟机网络模式

### 2.1 VMware 三种网络模式

#### 桥接模式（Bridged）
- **虚拟交换机**: VMnet0
- **原理**: 虚拟机直接连接到宿主机所在局域网，拥有独立 IP（与宿主机同网段）
- **优点**: 外部可直接访问；性能损耗极低（< 5%）
- **缺点**: 受公共 WiFi 路由器策略限制；直接暴露于网络；IP 可能冲突
- **适用场景**: 需要对外提供服务的服务器、网络仿真实验

#### NAT 模式
- **虚拟交换机**: VMnet8
- **原理**: 宿主机内部创建私有虚拟网络，内置 DHCP 分配私有 IP，NAT 设备代理对外通信
- **优点**: 开箱即用，无需配置；隔离性好；适应各种 WiFi 环境
- **缺点**: 外部默认无法访问；需手动端口转发
- **适用场景**: 日常上网、开发测试（推荐创建虚拟机的默认模式）

#### 仅主机模式（Host-Only）
- **虚拟交换机**: VMnet1
- **原理**: 完全包含在主机内部的虚拟网络，虚拟机只能与宿主机及同网络其他 VM 通信
- **优点**: 完全隔离，安全性极高
- **缺点**: 无法访问互联网
- **适用场景**: 安全研究、恶意软件测试、封闭开发环境

### 2.2 KVM 网络模式

| 模式 | 组件 | 特点 |
|------|------|------|
| **Masquerade（NAT）** | virbr0 + dnsmasq + iptables SNAT | 默认模式，IP 段 192.168.122.0/24，性能损耗 ~15% |
| **Bridge 模式** | br0 网桥（手动创建） | 物理网卡进混杂模式，MAC 透传，性能损耗 < 5% |
| **路由模式（Routed）** | 虚拟交换机 L3 路由 | 独立子网，不做 NAT，需外部配置路由表 |
| **隔离模式（Isolated）** | 私有虚拟网络 | VM 之间及与宿主机可通信，无外网出口 |

### 2.3 三模式对比

| 维度 | 桥接 | NAT | 仅主机 |
|------|------|-----|--------|
| 虚拟交换机 | VMnet0 | VMnet8 | VMnet1 |
| 外网访问 | 直接 | 通过主机 NAT | 不可用 |
| 外部主动访问 | 可直达 | 需端口转发 | 不可达 |
| 性能损耗 | < 5% | ~15% | 无 |
| 配置复杂度 | 较高 | 低（默认） | 低 |
| WiFi 推荐度 | 低 | 极高 | 不适用 |

### 2.4 Docker + VM 混合部署

- **问题**: Docker bridge + KVM NAT 叠加引入多层 NAT，性能损耗叠加
- **推荐方案**: macvlan/ipvlan — 容器获得独立 MAC 地址，与 VM 同网段通信，性能近乎原生
- **macvlan 局限**: 容器不能直接与宿主机通信；仅支持 Linux；云平台屏蔽
- **最佳实践**: 网络层用 macvlan/ipvlan；对外服务通过集中反向代理；结合 iptables 做跨边界访问控制

---

## 3. Docker 容器网络模式

### 3.1 模式详解

#### Bridge 模式（默认）
- **组件**: docker0 网桥 + veth pair + iptables NAT
- **IP 分配**: 172.17.0.0/16 私有子网
- **端口映射**: iptables DNAT 规则（`-p host_port:container_port`）
- **通信流程**: 外部 → PREROUTING → DOCKER 链(DNAT) → FORWARD → docker0 → veth → 容器
- **conntrack**: 连接跟踪记录五元组映射，高并发可能 `conntrack table full`
- **局限**: 跨主机需端口映射；默认 bridge 不支持容器名 DNS 解析

#### 自定义 Bridge 网络
- **优势**: 内置自动 DNS 解析（127.0.0.11）；支持运行时动态连接/断开
- **推荐**: 生产环境使用自定义 bridge 而非默认 docker0

#### Host 模式
- **原理**: 容器共享宿主机网络命名空间，使用宿主机 IP 和端口
- **性能**: 最高（95%+ 物理网卡性能），延迟约 0.02ms
- **局限**: 无网络隔离；仅 Linux；端口冲突需应用自行协调

#### Overlay 模式
- **原理**: VXLAN 隧道跨主机通信，需 Docker Swarm
- **性能**: 每跳 +1.1ms 延迟；损耗 5-15%（大包场景达 60%）；软件封装 ~5% CPU
- **MTU**: 需调整为 1450（VXLAN 50 字节开销）
- **加密**: 启用加密额外降低 20-30% TCP 吞吐

#### Macvlan 模式
- **原理**: 每个容器分配独立 MAC 地址，直连物理网络
- **性能**: 延迟约 0.03ms，吞吐量达 9.8 Gbps
- **局限**: 仅 Linux；容器与宿主机无法直接通信；云平台屏蔽；ESXi 限制 MAC 数量
- **工作模式**: bridge（默认互通）/ VEPA / private / passthru

#### IPvlan 模式
- **原理**: 所有容器共享父接口 MAC 地址，内核要求 4.2+
- **模式**: L2（桥接）和 L3（路由隔离）
- **优势**: MAC 地址表压力低；虚拟化平台兼容性好

#### None 模式
- **用途**: 完全自定义网络，后接 `docker network connect` 按需接入

#### Container 模式
- **原理**: 共享另一个容器的网络命名空间，通过 `localhost` 通信
- **类比**: 同 Kubernetes Pod 中多容器共享网络的设计
- **适用**: Sidecar 架构、网络调试容器

### 3.2 性能对比

| 模式 | 延迟 | 吞吐量 | CPU 开销 | 跨主机 |
|------|------|--------|---------|--------|
| Host | ~0.02ms | 95%+ 物理网卡 | ~0% | 直接物理 IP |
| Macvlan | ~0.03ms | ~9.8 Gbps | ~5% | 依赖物理路由 |
| Bridge | ~0.05ms | 中等（iptables 瓶颈） | 中 | 需端口映射 |
| Overlay | ~1.2ms | 损耗 5-15%（大包达 60%） | ~5-33% | 原生支持 |

### 3.3 精读笔记

#### 资料 1: Docker 各网络模式介绍
- **URL**: https://cloud.tencent.com.cn/developer/article/1444666
- **核心观点**: 5 种网络模式覆盖大部分场景；Container 模式原理同 K8s Pod
- **未覆盖**: Macvlan/IPvlan、自定义 Bridge、性能数据

#### 资料 2: Docker 网络配置 Bridge 到 Overlay
- **URL**: https://developer.aliyun.com/article/1501655
- **核心观点**: 入门级概述；Overlay 需 Swarm；Macvlan 适用于容器对外服务

#### 资料 3: Docker Bridge NAT 端口映射原理
- **URL**: https://github.com/ICKelin/article/blob/master/系列文章/docker/docker网络之端口映射.md
- **核心观点**: iptables DNAT/MASQUERADE 完整流程；conntrack 连接跟踪机制；DOCKER-USER 链用于自定义规则
- **关键规则**:
  ```bash
  iptables -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
  iptables -t nat -A DOCKER ! -i docker0 -p tcp --dport 9097 -j DNAT --to 172.17.0.2:80
  ```

---

## 4. Kubernetes 网络模型

### 4.1 CNI 架构

- **定义**: CNCF 项目，定义容器运行时与网络插件间的契约
- **命令接口**: `ADD`（创建网络接口时调用）、`DEL`（删除时调用）
- **工作流程**: 容器运行时 → 分配 network namespace → 传递 JSON 配置 → CNI 插件创建 veth pair → IPAM 分配 IP → 配置路由
- **范围**: CNI 只处理 L2/L3，L4 端口映射由容器运行时负责
- **NetworkPolicy**: K8s 定义资源对象，实际由 Policy Controller（如 Calico）实现

### 4.2 K8s 网络模型

- **"单 Pod 单 IP"**: 所有 Pod 可在无 NAT 情况下直接通信
- **主机内组网**: veth pair + Linux bridge（cni0）
- **Overlay vs Underlay**:
  - **Overlay**: 无基础设施要求，有封装开销（VXLAN 50 字节 / IPIP 20 字节）
  - **Underlay**: 高性能无封装，需 BGP 等网络基础设施支持

### 4.3 Flannel（VXLAN 模式）

- **架构**: 每个节点运行 flanneld 守护进程，从 etcd/K8s API 获取子网分配
- **关键设备**: flannel.1（VTEP）、cni0（网桥）、veth pair
- **跨节点通信流程**:
  1. Pod → veth pair → cni0 网桥
  2. 路由表 → flannel.1（VTEP）
  3. ARP 表获取目标 VTEP MAC（PERMANENT 条目）
  4. VXLAN 封装（VNI=1，UDP 8472）
  5. FDB 表查找 VTEP MAC 对应宿主机 IP
  6. 物理网络传输 → 目标节点解封装 → flannel.1 → cni0 → 目标 Pod
- **三张核心表**: 路由表（转发决策）、ARP 表（VTEP MAC）、FDB 表（MAC→宿主机 IP）
- **MTU**: 需调整为 1450

### 4.4 Calico

- **架构**: Felix（iptables+路由） + BIRD（BGP 路由广播）
- **网络模型**: 纯三层（L3），将每个节点视为路由器
- **Pod IP**: `/32` 掩码，点对点设计
- **虚拟网关**: `169.254.1.1` 链路本地地址，所有 Pod 通用
- **模式**: BGP 直连（无封装，需网络支持）、IPIP（20 字节头）、VXLAN
- **优势**: 原生支持 NetworkPolicy；无封装性能好；大规模集群首选

### 4.5 Cilium（eBPF）

- **原理**: eBPF 程序挂载到内核网络钩子，直接在内核处理包
- **优势**: 绕过 iptables/kube-proxy；TCP 吞吐量提升 40%；尾部延迟降至 1/5
- **功能**: 可完全替换 kube-proxy；支持 L7 协议感知（HTTP/gRPC/Kafka）
- **Hubble**: 基于 eBPF 的可观测性组件，流量监控和服务拓扑可视化
- **前提**: Linux 内核 >= 4.19.57

### 4.6 CNI 插件对比

| 插件 | 网络模型 | 封装 | NetworkPolicy | 性能 | 适用场景 |
|------|---------|------|-------------|------|---------|
| **Flannel** | Overlay | VXLAN（50 字节） | 不支持 | 中等 | 小规模集群、快速部署 |
| **Calico** | Underlay/Overlay | BGP/IPIP/VXLAN | 支持 | 高 | 大规模集群、需策略场景 |
| **Cilium** | eBPF | IPIP/直连 | 支持（L3-L7） | 极高 | 高性能、可观测性需求 |
| **Weave** | Overlay | UDP/VXLAN | 支持 | 中等 | 小到中型集群 |

### 4.7 Flannel vs Calico 性能实测

| 指标 | Flannel | Calico |
|------|---------|--------|
| 平均延迟 | 2.8 ms | **1.6 ms** |
| 吞吐量 | 8.4 Gbps | **9.2 Gbps** |
| 抖动 | 0.5 ms | **0.3 ms** |
| CPU 使用率 | **22%** | 25% |

---

## 5. 虚拟网络技术对比与选型

### 5.1 性能总排序

```
Host > Macvlan/Ipvlan > Underlay CNI (Calico BGP) > Bridge > Overlay CNI (Flannel VXLAN)
```

### 5.2 Overlay 性能损耗分解

| 损耗来源 | 开销 |
|---------|------|
| VXLAN 封装/解封装 | ~5% CPU |
| 安全策略/防火墙 | ~20% |
| 流量镜像 | ~5% |
| veth 数据复制 | ~3% |
| **最大总开销** | **~33%** |

### 5.3 MTU 规划

| 场景 | 推荐 MTU |
|------|---------|
| 标准以太网 | 1500 |
| VXLAN Overlay | 1450（1500 - 50 字节封装） |
| IPIP Overlay | 1480（1500 - 20 字节封装） |
| Jumbo Frames + VXLAN | 8950（9000 - 50） |

### 5.4 选型决策矩阵

| 场景 | 推荐方案 | 关键考量 |
|------|---------|---------|
| Docker 单机 | 自定义 Bridge | 内置 DNS 解析、独立隔离 |
| Docker 跨主机 | Overlay（VXLAN）+ Swarm | 跨主机通信、零改现网 |
| Docker 高性能 | Macvlan / Host | 低延迟、高吞吐 |
| K8s 生产集群 | Calico（BGP/VXLAN）+ NetworkPolicy | 细粒度控制、成熟生态 |
| K8s 快速验证 | Flannel（VXLAN） | 部署最简单 |
| VM 日常使用 | NAT 模式 | 默认可用、WiFi 友好 |
| VM 对外服务 | 桥接模式 | 独立 IP、外部可直达 |
| VM 安全测试 | 仅主机模式 | 完全隔离 |
| Docker + VM 混合 | Macvlan/Ipvlan | 同网段高性能、避免多层 NAT |

### 5.5 核心变量关系

```
隔离性  ↑  仅主机(None) > Overlay > Bridge(NAT) > Macvlan > Host
性能    ↑  Host > Macvlan > Bridge > Overlay
灵活性  ↑  Overlay > Bridge > Macvlan > Host
部署难度 ↑  Overlay > Macvlan > Bridge > Host
```

---

## 参考来源

1. [VLAN/VLANIF/VXLAN 七个维度对比 - 腾讯云](https://cloud.tencent.com.cn/developer/article/2512624)
2. [SDN 全面解读 - 中国教育和科研计算机网](https://www.edu.cn/sdn_12536/20130724/t20130724_992256.shtml)
3. [VXLAN 报文转发原理 - 阿里云](https://developer.aliyun.com/article/1588407)
4. [Linux 网络命名空间初认识 - 华为云](https://bbs.huaweicloud.com/blogs/148734)
5. [Linux network namespace 初认识 - 腾讯云](https://cloud.tencent.com.cn/developer/article/2486110)
6. [VMware 三种网络模式原理 - 阿里云](https://developer.aliyun.com/article/1681598)
7. [Docker 网络模式与容器间通信深度解析 - 百度云](https://cloud.baidu.com/article/3381358)
8. [Docker 各网络模式介绍 - 腾讯云](https://cloud.tencent.com.cn/developer/article/1444666)
9. [Docker 端口映射原理分析 - GitHub](https://github.com/ICKelin/article/blob/master/系列文章/docker/docker网络之端口映射.md)
10. [Kubernetes CNI 网络模型 - 阿里云](https://developer.aliyun.com/article/1481169)
11. [Flannel vs Calico CNI 之战 - 腾讯云](https://cloud.tencent.com.cn/developer/article/2499890)
12. [Flannel VXLAN 数据报文转发 - 阿里云](https://developer.aliyun.com/article/1595095)
13. [容器化部署网络配置优化 - 百度云](https://cloud.baidu.com/article/5636825)
14. [容器网络 vs 虚拟化网络对比](https://www.cloudnative-tech.com/p/7726/)
