---
title: "第九章：Kubernetes 网络模型与 CNI 插件"
created: 2026-07-29
updated: 2026-07-29
tags:
  - virtual-networking
  - networking
  - learning-note
status: completed
source_project: virtual-networking
---

# 第九章：Kubernetes 网络模型与 CNI 插件

## 本章要解决什么问题

前两章我们深入了 [[Docker]] 的六种网络模式，但 Docker 解决的是单容器的网络接入问题。当我们进入 [[Kubernetes]] 的世界，面对的是成百上千个 Pod 在集群中动态调度、随时漂移的场景。一个 Pod 从节点 A 迁移到节点 B，它的 IP 会变吗？不同节点上的 Pod 如何无需端口映射就能直接通信？谁负责为每个新创建的 Pod 插上网线？

这些问题都指向同一个基础设施层——**Kubernetes 网络模型**和它的实现者 [[CNI|CNI 插件]]。本章将深入 CNI 的架构契约，剖析三个主流插件（[[Flannel]]、[[Calico]]、[[Cilium]]）的工作原理，让你理解 K8s 网络"从 Pod 创建到跨节点通信"的完整链路。

---

## 9.1 容器网络接口（CNI）：为 Pod 插上网线的标准契约

### 9.1.1 为什么需要 CNI

在 Docker 的世界里，网络模式是内建的——Docker 自己创建 bridge、管理 iptables、分配 IP。但 Kubernetes 的设计哲学是"可插拔"：网络实现不应该绑死在容器运行时里，而应该让第三方插件各展所长。

这就是 [[CNI]]（Container Network Interface）的诞生背景。它是一个 CNCF 项目，定义了一套**容器运行时与网络插件之间的标准接口契约**。

### 9.1.2 CNI 的运作模型

CNI 的模型非常精简，核心只有两个操作：

| 操作 | 触发时机 | 插件的职责 |
|------|---------|-----------|
| `ADD` | 容器（Pod）创建时 | 创建网络接口、分配 IP、配置路由 |
| `DEL` | 容器（Pod）删除时 | 清理网络接口、释放 IP、清理路由 |

**完整的工作流程（从 Pod 创建到网络就绪）：**

```
1. kubelet 收到创建 Pod 的请求
2. kubelet 调用 CRI（容器运行时接口）创建 pause 容器
3. 容器运行时创建独立的 network namespace
4. 容器运行时根据配置读取 CNI JSON 配置
5. 调用 CNI 插件的二进制文件，传入 network namespace 路径和配置
6. CNI 插件：
   a. 创建 veth pair，一端放入 namespace，另一端挂到主机网桥
   b. 调用 IPAM 插件分配 IP 地址
   c. 配置路由规则
7. 返回结果给容器运行时，Pod 网络就绪
```

这里有一个关键的设计细节需要特别注意：**CNI 只负责 L2（数据链路层）和 L3（网络层）**。L4 的端口映射（如 `kube-proxy` 的 Service）是容器运行时或 Kubernetes 组件自己的职责，不在 CNI 的范围内。

> [!note]
> **CNI 契约的简洁性**：整个规范只有一个 JSON 配置文件和几个二进制插件。这种"少即是多"的设计让它获得了广泛的生态支持。

---

## 9.2 K8s 网络模型：单 Pod 单 IP

Kubernetes 对网络提出了三个基本要求，这是所有 CNI 插件都必须满足的：

1. **所有 Pod 可以不经过 NAT 直接通信**（无论是否在同一个节点）
2. **所有节点可以不经过 NAT 直接与所有 Pod 通信**
3. **Pod 看到的自身 IP 与其他 Pod 看到的该 Pod IP 一致**

这三条规则合在一起，就是著名的 **"单 Pod 单 IP"** 模型。每个 Pod 拥有一个集群内唯一的、可路由的 IP 地址，没有了 Docker [[Bridge模式|bridge]] 模式中端口映射的烦恼。

### 9.2.1 主机内组网：veth pair + bridge

在同一个节点上，多个 Pod 之间的通信非常直接——和 Docker bridge 模式的原理完全一致：

```
Pod A (10.244.1.2)
    └─ veth0@if1 (eth0 in Pod)
         │
    cni0 (Linux bridge, 10.244.1.1/24)
         │
    └─ veth1@if2 (eth0 in Pod)
Pod B (10.244.1.3)
```

- 每个 Pod 拥有一对 veth pair，一端在 Pod 的 network namespace 内（eth0），另一端挂到节点上的 Linux bridge `cni0`
- `cni0` 是每个节点上的核心网桥，负责本节点内 Pod 的二层互通
- 跨节点的通信，就需要 CNI 插件来解决了

---

## 9.3 Flannel：最简单的 Overlay 方案

[[Flannel]] 由 CoreOS 开发，是 K8s 生态中最简单的 CNI 插件。它的核心思路是：**每个节点分配一个独立的子网，跨节点通信通过 [[VXLAN]] 隧道封装**。

### 9.3.1 架构概览

每个节点上运行一个 `flanneld` 守护进程，它的职责是：

1. 从集群存储（[[etcd]] 或 K8s API）中为自己分配一个子网（如 `10.244.1.0/24`）
2. 监听其他节点的子网分配信息
3. 维护本节点上的路由表、ARP 表、FDB 表

### 9.3.2 部署 Flannel

```bash
# 最简单的部署方式
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml

# 验证部署状态
kubectl -n kube-flannel get pods
# 输出示例：
# NAME                    READY   STATUS    RESTARTS   AGE
# kube-flannel-ds-abc12   1/1     Running   0          2m
# kube-flannel-ds-def34   1/1     Running   0          2m

# 查看 flanneld 分配的节点子网
kubectl get nodes -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.podCIDR}{"\n"}{end}'
# 输出示例：
# node-1    10.244.1.0/24
# node-2    10.244.2.0/24
```

Flannel 以 DaemonSet 方式运行，每个节点一个 Pod。部署完成后，每个节点上的网络设备拓扑如下：

```
节点上的网络设备（以 node-1 为例）：

物理网卡 eth0 (192.168.1.10)
    │
flannel.1 (VTEP, VXLAN 隧道端点)
    │    MAC: 8a:4b:5c:6d:7e:8f
    │    IP:  10.244.1.0 (实际不通信，仅作为 VTEP 标识)
    │
cni0 (Linux bridge, 10.244.1.1/24)
    │
    ├── vethXXX (Pod A, 10.244.1.2)
    ├── vethYYY (Pod B, 10.244.1.3)
    └── ...
```

### 9.3.3 跨节点通信 —— VXLAN 三表协作

这是 Flannel 最核心、也最值得深入理解的部分。假设 Pod A（node-1, 10.244.1.2）想访问 Pod B（node-2, 10.244.2.3），完整的通信链路如下：

#### 第一步：Pod -> cni0 bridge

Pod A 的数据包从 eth0 发出，目标 IP 是 10.244.2.3。由于目标 IP 不在本节点子网（10.244.1.0/24）内，数据包从 veth 进入 cni0 网桥后，网桥发现目标 MAC 不在本网桥的 MAC 表中，于是送上主机的网络栈进行路由决策。

#### 第二步：路由表 -> flannel.1

关键就在主机路由表：

```bash
# 在 node-1 上查看路由表
ip route show | grep flannel
# 输出：
# 10.244.1.0/24 dev cni0 proto kernel scope link src 10.244.1.0
# 10.244.2.0/24 via 10.244.2.0 dev flannel.1 onlink
# 10.244.3.0/24 via 10.244.3.0 dev flannel.1 onlink
```

解读这条路由：
- 10.244.2.0/24 这个子网对应的下一跳是 10.244.2.0（这是目标 VTEP 的标识 IP）
- 出接口是 flannel.1（VXLAN 隧道端点）
- `onlink` 标志：允许将路由指向 flannel.1，而不要求目标 IP 在同一链路上

> [!note]
> **路由表回答的是"往哪个方向走"**。现在数据包被导向了 flannel.1 这个 VTEP 设备。

#### 第三步：ARP 表 -> 目标 VTEP MAC

既然数据包要进入 flannel.1，内核需要知道目标 VTEP 的 MAC 地址。这就需要 ARP 表：

```bash
# 在 node-1 上查看 ARP 表中 flannel 相关的条目
ip neigh show dev flannel.1
# 输出：
# 10.244.2.0 lladdr a6:7b:8c:9d:0e:1f PERMANENT
# 10.244.3.0 lladdr b2:3c:4d:5e:6f:70 PERMANENT
```

注意两点：
- 这里的 ARP 条目问的是 **VTEP 的 MAC 地址**（即 flannel.1 设备在 node-2 上的 MAC），**不是 Pod 的 MAC 地址**
- 所有条目都是 `PERMANENT`（永久条目），由 flanneld 静态写入，不通过 ARP 广播学习

> [!note]
> **ARP 表回答的是"目标 VTEP 的 MAC 是什么"**。现在数据包将被封装上内层以太网头，目的 MAC 为 `a6:7b:8c:9d:0e:1f`。

#### 第四步：VXLAN 封装

此时内核进入 VXLAN 封装流程。原始数据包成为内层载荷，外面按顺序添加：

| 协议层 | 内容 | 大小 |
|--------|------|------|
| 内层以太网头 | 源/目标 Pod MAC | 14 字节 |
| 内层 IP 头 | 10.244.1.2 -> 10.244.2.3 | 20 字节 |
| 内层载荷 | TCP/UDP 数据 | 可变 |
| **VXLAN 头** | VNI=1, Flags | **8 字节** |
| **外层 UDP 头** | 源端口(哈希) -> 8472 | **8 字节** |
| **外层 IP 头** | 192.168.1.10 -> ? | **20 字节** |
| **外层以太网头** | 源 MAC -> ? | **14 字节** |

但这里还有一个问题：外层 UDP 和 IP 头的目标 IP 是什么？VXLAN 封装知道目标 VTEP 的 MAC（从 ARP 表得到），但还不知道目标 VTEP 所在的宿主机 IP。这就需要第三张表。

#### 第五步：FDB 表 -> 宿主机 IP

FDB（Forwarding Database）表是二层交换机的转发表，在这里记录的是 **"VTEP MAC 地址 -> 宿主机 IP 地址"** 的映射：

```bash
# 在 node-1 上查看 FDB 表中 flannel 相关的条目
bridge fdb show dev flannel.1
# 输出：
# a6:7b:8c:9d:0e:1f dst 192.168.2.20 self permanent
# b2:3c:4d:5e:6f:70 dst 192.168.3.30 self permanent
```

解读：MAC 地址为 `a6:7b:8c:9d:0e:1f` 的 VTEP 位于 IP 为 `192.168.2.20` 的宿主机（即 node-2）上。

> [!note]
> **FDB 表回答的是"这个 VTEP MAC 对应的物理宿主机 IP 是什么"**。现在外层 UDP/IP/以太网头都有了完整的目标地址。

#### 第六步：物理网络传输与解封装

封装完成的 VXLAN 包（UDP 目标端口 8472）通过物理网卡 eth0 发出，经过物理网络到达 node-2。

node-2 的内核收到 UDP 8472 端口的包后：
1. 识别出这是 VXLAN 包
2. 解封装，剥离外层头，取出内层原始数据包
3. 将内层数据包交给 flannel.1（VTEP）
4. flannel.1 根据目标 MAC 确认目标 Pod 在本节点
5. 数据包进入 cni0 网桥
6. cni0 通过 MAC 表找到对应的 veth 端口
7. 数据包到达 Pod B（10.244.2.3）

**整个链路的流程图：**

```
Pod A (10.244.1.2)
    │ 目标: 10.244.2.3
    ▼
veth pair
    │
    ▼
cni0 bridge ──路由表──▶ flannel.1 (VTEP)
                              │
                    ┌─────────┼─────────┐
                    │         │         │
                  路由表    ARP表    FDB表
                  决定方向  VTEP MAC  →宿主机IP
                    │         │         │
                    └─────────┼─────────┘
                              │
                              ▼
                    VXLAN 封装 (VNI=1, UDP 8472)
                              │
                              ▼
                    eth0 物理网卡 → 物理网络
                              │
                              ▼
                    node-2 解封装
                              │
                              ▼
                    flannel.1 → cni0 → veth → Pod B
```

> [!summary] 三表协作的核心思想
> 路由表解决"去哪"，ARP 表解决"VTEP 长什么样"，FDB 表解决"VTEP 在哪里"。三者缺一不可。

#### MTU 注意事项

VXLAN 封装会增加 50 字节的开销，因此 Flannel 要求物理网络的 MTU 设置为 **1450**（标准以太网 1500 - 50）。如果不调整，会导致 TCP 分段和性能下降。具体配置方法见第十章。

---

## 9.4 Calico：纯三层的高性能方案

Flannel 的 [[Overlay网络|Overlay]] 方案简单易用，但封装和解封装带来了性能损失。[[Calico]] 走的是另一条路——**纯三层（L3）网络模型**，将每个节点当作一台路由器，Pod IP 直接在物理网络上路由。

### 9.4.1 架构组件

Calico 由三个核心组件构成：

| 组件 | 职责 |
|------|------|
| **Felix** | 运行在每个节点上的守护进程，负责配置 iptables 规则和路由表 |
| **BIRD** | BGP 路由协议实现，负责在节点之间广播路由信息 |
| **Calico API Server** | 管理 NetworkPolicy 等资源对象（可选） |

### 9.4.2 部署 Calico

```bash
# 使用 Operator 部署 Calico（推荐方式）
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27/manifests/tigera-operator.yaml

# 创建 Calico 自定义资源
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.27/manifests/custom-resources.yaml

# 验证部署状态
kubectl get pods -n calico-system
# 输出示例：
# NAME                                       READY   STATUS
# calico-node-abc12                          1/1     Running
# calico-node-def34                          1/1     Running
# calico-kube-controllers-5d6c7f8b9b-xyz12   1/1     Running

# 查看 Calico 管理的网络接口
ip link show | grep cali
# 输出示例：
# cali12345: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
# cali67890: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
```

### 9.4.3 Calico 的网络模型

Flannel 使用 cni0 这种 Linux bridge 进行二层交换，Calico 不同——**它不使用 bridge**。每个 Pod 通过 veth pair 直连到宿主机，每个 Pod 的 IP 以 `/32` 掩码作为独立路由条目，宿主机上的 Felix 负责维护这些路由。

```
节点上的网络设备（Calico 模式）：

节点 node-1 (192.168.1.10)
    │
    ├── eth0 (物理网卡)
    │
    ├── caliXXXXX ─── veth ─── Pod A (10.244.1.2/32)
    │
    └── caliYYYYY ─── veth ─── Pod B (10.244.1.3/32)
```

### 9.4.4 Calico 路由表 vs Flannel 路由表

```bash
# Calico 节点路由表（关键部分）
ip route show proto bird
# 输出：
# 10.244.1.2 dev caliXXXXX scope link          # 本节点 Pod A
# 10.244.1.3 dev caliYYYYY scope link          # 本节点 Pod B
# 10.244.2.3 via 192.168.2.20 dev eth0 proto bird # 跨节点 Pod，直接走物理网卡
# 10.244.3.5 via 192.168.3.30 dev eth0 proto bird # 跨节点 Pod，直接走物理网卡
```

对比 Flannel：

```bash
# Flannel 节点路由表（关键部分）
# 10.244.2.0/24 via 10.244.2.0 dev flannel.1 onlink  # 走 VTEP 隧道
# 10.244.3.0/24 via 10.244.3.0 dev flannel.1 onlink  # 走 VTEP 隧道
```

关键区别：

| 维度 | Flannel | Calico |
|------|---------|--------|
| 跨节点路径 | 走 flannel.1（VTEP），需要 VXLAN 封装 | 走 eth0（物理网卡），直接路由 |
| 路由粒度 | 子网级（/24），以节点为单位聚合 | Pod 级（/32），每个 Pod 独立路由 |
| 路由维护 | flanneld 静态写入 | BIRD 通过 BGP 动态广播 |
| 封装开销 | VXLAN 50 字节 | 0（纯 BGP 模式） |

### 9.4.5 虚拟网关 169.254.1.1

Calico 还有一个巧妙的设计：所有 Pod 的默认网关统一设置为 `169.254.1.1`。这个地址是链路本地地址（Link-Local Address），意味着它只在当前链路有效，不需要路由。

```bash
# 进入 Pod 查看路由
kubectl exec -it <pod-name> -- ip route
# 输出：
# default via 169.254.1.1 dev eth0
# 10.244.1.2 dev eth0 scope link
```

`169.254.1.1` 并不对应任何真实设备，它的作用是让 Pod 内发出的数据包通过 veth pair 进入宿主机，由 Felix 配置的 iptables 规则和路由表决定下一步走向。

### 9.4.6 Calico 的三种运行模式

| 模式 | 封装 | 场景 | 优点 | 缺点 |
|------|------|------|------|------|
| **BGP** | 无 | Underlay 网络，物理路由器支持 BGP | 性能最高 | 需要网络基础设施支持 |
| **IPIP** | 20 字节 | Overlay 模式，无 BGP 要求 | 兼容性好 | 少量封装开销 |
| **VXLAN** | 50 字节 | Overlay 模式，大集群 | 标准 Overlay | 封装开销大 |

BGP 模式是 Calico 的"完全体"——不封装、不隧道、纯三层路由。但它的前提条件是底层网络设备（物理路由器或云平台）支持 BGP 协议，否则就用不了。IPIP 和 VXLAN 模式是不依赖底层网络的备选方案。

### 9.4.7 NetworkPolicy：Calico 的杀手级能力

Flannel 有一个重要短板：**不支持 [[NetworkPolicy]]**。Calico 原生支持 K8s 的 NetworkPolicy 资源，还能扩展更丰富的策略规则。

```yaml
# 一个 NetworkPolicy 示例
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-allow
spec:
  podSelector:
    matchLabels:
      app: api-server
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: web-frontend
    ports:
    - protocol: TCP
      port: 8080
```

这个策略的意思是：只有标签为 `app=web-frontend` 的 Pod 可以访问标签为 `app=api-server` 的 Pod 的 8080 端口。Felix 会将这个策略翻译为宿主机上的 iptables 规则，在 Pod 流量进出的必经之路上进行过滤。

---

## 9.5 Cilium：eBPF 驱动的下一代网络

如果说 Flannel 是"够用就好"，Calico 是"成熟稳定"，那么 [[Cilium]] 代表的是"面向未来"。它建立在 Linux 内核的 [[eBPF]] 技术之上。

### 9.5.1 eBPF 的革命性意义

要理解 Cilium，先要理解 eBPF 做了什么。

传统上，内核的网络处理路径是固定的：数据包经过网卡 -> 内核协议栈 -> iptables -> socket。如果你想干预这个过程，要么修改内核代码（极难），要么通过 iptables/netfilter 这种"钩子"（但性能差）。

**eBPF 改变了这一切**——它允许你在内核网络路径的任意点插入一小段用户编写的程序，这些程序在内核中运行，既安全又高效。

```
传统路径：
    网卡 → 内核协议栈 → iptables(线性匹配) → socket
                                         ↑
                                   每一条规则都检查
                                   规则越多越慢

eBPF 路径：
    网卡 → eBPF 程序(哈希查找) → socket
                         ↑
                    O(1) 查找
                    无视规则数量
```

> [!tip] 一句话理解 eBPF
> 相当于给内核装上了"插件系统"，让你能在不修改内核的情况下，以内核级别的性能处理网络包。

### 9.5.2 Cilium 的优势

基于 eBPF，Cilium 实现了几项关键突破：

**绕过 kube-proxy**：
K8s 的 Service 通常由 kube-proxy 通过 iptables 实现。当集群中有成千上万个 Service 时，iptables 规则呈线性增长，每次数据包匹配都要遍历所有规则。Cilium 使用 eBPF 的哈希映射替代 iptables 链，实现 O(1) 的查找性能。

**TCP 吞吐量提升 40%**：
在网络密集型应用（如数据传输、流媒体）中，Cilium 的 eBPF 路径比 iptables 路径快得多。

**尾部延迟降至 1/5**：
在微服务调用链中，长尾延迟（P99）是关键指标。Cilium 通过减少网络路径上的 hops 和避免 iptables 的遍历开销，将尾部延迟大幅降低。

**L7 协议感知**：
传统 CNI 插件只看到 L3（IP）和 L4（端口）。Cilium 能识别 HTTP、gRPC、Kafka 等应用层协议，可以实现像"允许 GET 请求但拒绝 DELETE 请求"这样的精细化策略。

```bash
# L7 感知的 NetworkPolicy 示例（Cilium CRD）
apiVersion: "cilium.io/v2"
kind: CiliumNetworkPolicy
metadata:
  name: "http-allow"
spec:
  endpointSelector:
    matchLabels:
      app: api-server
  ingress:
  - toPorts:
    - ports:
      - port: "8080"
        protocol: TCP
      rules:
        http:
        - method: "GET"
          path: "/api/v1/.*"
```

### 9.5.3 Hubble：eBPF 原生的可观测性

Cilium 还附带了一个可观测性组件 Hubble，它利用 eBPF 在内核层面捕获网络流量，提供细粒度的监控能力：

```bash
# 查看集群中的网络流量
hubble observe --namespace default
# 输出示例：
# Jan 01 12:00:00.000  pod/frontend:54321 -> pod/backend:8080  http-request GET /api/v1/users
# Jan 01 12:00:00.001  pod/backend:8080 -> pod/frontend:54321  http-response 200 2.3ms
```

传统方式（如 Prometheus + 指标采集）只能看到聚合数据，Hubble 能看到**每条请求的完整路径**，极大简化了微服务排障。

### 9.5.4 部署前提

Cilium 对内核版本有要求：

```
Linux 内核 >= 4.19.57（推荐 5.10+）
```

如果你的节点使用较老的内核（如 CentOS 7 默认的 3.10），就无法运行 Cilium。这是它在生产环境推广中的最大障碍。

---

## 9.6 CNI 插件选型对比

### 9.6.1 四款主流插件全景

| 维度 | Flannel | Calico | Cilium | Weave |
|------|---------|--------|--------|-------|
| **网络模型** | Overlay (VXLAN) | Underlay/Overlay | eBPF | Overlay |
| **封装** | VXLAN (50B) | BGP/IPIP/VXLAN | IPIP/直连 | UDP/VXLAN |
| **NetworkPolicy** | 不支持 | 支持 (L3-L4) | 支持 (L3-L7) | 支持 |
| **性能** | 中等 | 高 | 极高 | 中等 |
| **部署难度** | 极简 | 中等 | 中等 | 简单 |
| **内核要求** | 无特殊 | 无特殊 | >= 4.19.57 | 无特殊 |
| **适用场景** | 小规模、快速验证 | 大规模、需策略控制 | 高性能、可观测性 | 中小规模 |

### 9.6.2 Flannel vs Calico 性能实测

| 指标 | Flannel（VXLAN） | Calico（BGP） |
|------|------------------|---------------|
| 平均延迟 | 2.8 ms | **1.6 ms** |
| 吞吐量 | 8.4 Gbps | **9.2 Gbps** |
| 抖动（Jitter） | 0.5 ms | **0.3 ms** |
| CPU 使用率 | **22%** | 25% |

从数据可以看到：
- Calico 在延迟和吞吐上明显优于 Flannel（约 40% 的延迟降低，10% 的吞吐提升）
- Calico 的 CPU 使用率略高（多了 BGP 协议维护的开销）
- 如果集群规模较大（超过 50 节点），强烈建议使用 Calico

### 9.6.3 选型建议

```
场景                            推荐方案
─────────────────────────────────────────────────
个人学习/实验环境                Flannel（部署最简单）
生产集群（< 50 节点，无策略需求）  Flannel VXLAN
生产集群（> 50 节点）             Calico BGP（底层支持）或 VXLAN
生产集群（需网络隔离策略）        Calico
高吞吐/低延迟要求                Calico BGP 或 Cilium
需 L7 策略/可观测性              Cilium + Hubble
老内核（< 4.19）                 Flannel 或 Calico（不能用 Cilium）
```

---

## 本章总结

- **[[CNI]] 是 K8s 网络的核心接口**，定义了 ADD/DEL 两个基本操作，容器运行时通过它调用网络插件为 Pod 创建网络。
- **K8s 网络模型要求"单 Pod 单 IP"**，所有 Pod 和节点之间可以直接通信，无需 NAT。
- **[[Flannel]] 用 [[VXLAN]] 隧道实现 [[Overlay网络|Overlay]] 网络**，核心是路由表（决定方向）、ARP 表（VTEP MAC）、FDB 表（宿主机 IP）三表协作。
- **[[Calico]] 采用纯三层模型**，将节点视为路由器，通过 BGP 广播 Pod 路由，无需封装，支持 [[NetworkPolicy]]。
- **[[Cilium]] 基于 [[eBPF]] 技术**，绕过 iptables/kube-proxy，提供更高性能和 L7 感知能力，但需要较新的内核。
- **选型的核心权衡**：Flannel 最简单，Calico 最平衡，Cilium 最前沿。

## 下一章预告

从 [[VLAN]] 到 [[VXLAN]]，从 Docker bridge 到 Calico BGP——我们已经走过了整个虚拟网络技术栈。第十章将把所有技术拉到一个全景画布上进行对比，给出精确到每一个场景的选型决策矩阵，并用一份实战指南收束全文。

---

**参考来源**：
- [[Kubernetes]] CNI 网络模型 - 阿里云（素材 #10）
- Flannel vs Calico CNI 之战 - 腾讯云（素材 #11）
- Flannel VXLAN 数据报文转发 - 阿里云（素材 #12）
- 容器化部署网络配置优化 - 百度云（素材 #13）
- 容器网络 vs 虚拟化网络对比（素材 #14）
