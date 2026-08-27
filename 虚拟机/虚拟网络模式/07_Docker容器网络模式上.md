---
title: "第七章：Docker 容器网络模式（上）— 单机模式"
created: 2026-07-29
updated: 2026-07-29
tags:
  - virtual-networking
  - networking
  - learning-note
status: completed
source_project: virtual-networking
---

# 第7章：Docker 容器网络模式（上）— 单机模式

## 7.1 引言：为什么 Docker 网络需要多种模式？

上一章我们学习了虚拟机网络模式：桥接、[[NAT]]、仅主机。[[Docker]] 容器的网络需求与虚拟机类似——需要隔离、需要互通、需要对外暴露服务——但容器的本质差异（**进程级隔离而非完整操作系统**）决定了它的网络方案有独特的设计。

Docker 提供了六种网络模式，本章我们先介绍其中四种单机模式，下一章再介绍跨主机和高性能模式：

| 模式             | 一句话定位                 | 适用场景                        |             |
| -------------- | --------------------- | --------------------------- | ----------- |
| **[[Bridge模式   | Bridge]]**（默认）        | 通过虚拟网桥 + iptables 实现隔离和端口映射 | 单机开发测试、默认选择 |
| **自定义 Bridge** | 增强版 Bridge，带内置 DNS 解析 | 生产环境单机部署                    |             |
| **Host**       | 容器共享宿主机网络栈，零损耗但无隔离    | 高性能场景、网络监控工具                |             |
| **Container**  | 两个容器共享同一个网络命名空间       | Sidecar 代理、网络调试             |             |
| **None**       | 空网络，完全自定义             | 离线计算、自定义网络方案                |             |

## 7.2 Bridge 模式：Docker 的默认选择

### 7.2.1 从「网络命名空间 + veth」到 Bridge 模式

在第五章我们亲手搭建过这样的场景：用 `ip netns` 创建隔离的网络命名空间，用 `veth pair` 连接两个空间，再挂到 `br0` 网桥上。Docker [[Bridge模式|Bridge]] 模式的本质，就是这个方案的自动化版本。

想象一下：你运行 `docker run nginx`，Docker 在后台替你完成了以下操作：

1. 为容器创建一个独立的网络命名空间
2. 创建一对 `veth` 虚拟网卡
3. 一端（`vethxxx`）挂到名为 `docker0` 的 Linux 网桥上
4. 另一端（`eth0`）放进容器的网络命名空间，分配 IP 地址 172.17.0.2
5. 配置 iptables NAT 规则，让容器能访问外网

让我们实际验证一下。启动一个 Nginx 容器并观察网络结构：

```bash
# 启动一个 Nginx 容器
docker run -d --name web-demo -p 9097:80 nginx:alpine

# 查看宿主机上的网桥
brctl show docker0

# 预期输出：
# bridge name     bridge id               STP enabled     interfaces
# docker0         8000.0242a1b2c3d4       no              veth3a2b1c
```

> [!tip]
> 如果系统没有 `brctl`，可以通过 `ip link show type bridge` 或 `bridge link` 查看。

重点关注这里的 `interfaces` 列——`veth3a2b1c` 就是 veth pair 在宿主机的一端。它的另一端在容器内部，命名为 `eth0`。

进入容器内部验证：

```bash
docker exec web-demo ip addr show eth0

# 预期输出：
# 5: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 ...
#     link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff
#     inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
```

看到 `172.17.0.2/16` 了？这就是 Docker 的默认私有子网。为什么是 `172.17.0.0/16`？这是一个历史选择，Docker 从 `172.17.0.0` 开始用 `16` 位掩码（`/16`），最多可容纳 65534 个容器地址。

### 7.2.2 网络拓扑全景图

```
                        宿主机
    ┌─────────────────────────────────────────────────┐
    │                                                 │
    │  容器 A                    容器 B                │
    │  172.17.0.2                172.17.0.3            │
    │  ┌──────┐                  ┌──────┐              │
    │  │ eth0 │                  │ eth0 │              │
    │  └──┬───┘                  └──┬───┘              │
    │     │                         │                   │
    │  veth3a                    veth9b                 │
    │     │                         │                   │
    │     └──────────┬──────────────┘                   │
    │                │                                  │
    │          ┌─────┴─────┐                            │
    │          │  docker0  │  ← Linux Bridge (172.17.0.1)│
    │          └─────┬─────┘                            │
    │                │                                  │
    │          ┌─────┴─────┐                            │
    │          │   eth0    │  ← 宿主机物理网卡          │
    │          └─────┬─────┘                            │
    │                │                                  │
    │         iptables NAT (MASQUERADE + DNAT)           │
    └────────────────┼──────────────────────────────────┘
                     │
                  Internet/网络
```

这张图的关键信息：

- **docker0 不是路由器，而是网桥（二层交换机）**。同一台宿主机上的容器通过 docker0 可以直接二层通信，不需要经过三层路由。
- **docker0 的 IP（172.17.0.1）是容器的默认网关**。容器访问外部网络时，数据包先到 docker0，由宿主机内核替容器的 IP 做路由和 NAT。
- **veth pair 是虚拟网线**。两端分别插入容器和 docker0，数据在一端输入，从另一端原样输出。

### 7.2.3 容器访问外网的通信流程

技术上说，Docker 的默认 [[Bridge模式|Bridge]] 模式对外通信依赖 **iptables MASQUERADE（源地址伪装）** 。让我们剖析一次完整的对外访问：

**场景**：容器（172.17.0.2）向百度（183.232.231.174:80）发起 HTTP 请求。

**步骤 1：容器发出数据包**

```
源 IP: 172.17.0.2:34567  →  目的 IP: 183.232.231.174:80
```

容器根据路由表（默认网关 172.17.0.1），将数据包从 `eth0` 发出，通过 veth pair 到达 docker0 网桥。

**步骤 2：宿主机路由决策**

数据包到达 docker0 后，宿主机内核查看路由表：

```bash
ip route show | grep 172.17

# 输出：
# 172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
```

目的地址 `183.232.231.174` 不在 `172.17.0.0/16` 范围内，所以要查默认路由。数据包被转发到宿主机主网卡（eth0）的出口。

**步骤 3：MASQUERADE 改写源地址**

数据包即将离开宿主机 eth0 前，触及关键的 iptables 规则：

```bash
iptables -t nat -A POSTROUTING -s 172.17.0.0/16 ! -o docker0 -j MASQUERADE
```

这条规则的含义："源地址在 172.17.0.0/16 内，并且**出口不是 docker0** 的数据包，做源地址伪装"。

MASQUERADE 会把数据包的源 IP 从私有地址 `172.17.0.2` 替换为宿主机的公网 IP（假设是 `192.168.1.100`）。为什么叫"伪装"？因为百度看到的请求来源是宿主机的 IP，而不是容器真正的私有 IP。

```
改写前: 172.17.0.2:34567  →  183.232.231.174:80
改写后: 192.168.1.100:23456  →  183.232.231.174:80
```

**步骤 4：响应包返回**

百度响应数据包到达宿主机：

```
源 IP: 183.232.231.174:80  →  目的 IP: 192.168.1.100:23456
```

宿主机需要找到这个数据包应该发给谁。这就是 **conntrack（连接跟踪）** 出场的地方——下面单独讨论。

### 7.2.4 外部访问容器：端口映射的 DNAT 流程

上面是容器主动访问外网。反过来，外部如何访问容器里的服务？比如你访问 `http://宿主机IP:9097`，如何到达 `172.17.0.2:80`？

这就是 `-p 9097:80` 参数的作用。Docker 在 iptables 中插入了一条 DNAT 规则：

```bash
iptables -t nat -A DOCKER ! -i docker0 -p tcp --dport 9097 -j DNAT --to 172.17.0.2:80
```

这条规则的含义："从**非 docker0 接口**进入的 TCP 数据包，如果目的端口是 9097，把目的地址改写为 172.17.0.2:80"。

完整的入站通信路径如下：

```
外部客户端 (192.168.1.50:50000)
    │
    ▼ 访问宿主机公网 IP:9097
PREROUTING 链 (raw/表 → mangle/表 → nat/表)
    │
    ▼ nat/PREROUTING → nat/DOCKER 链匹配
DNAT 改写: 目的地址从 192.168.1.100:9097 → 172.17.0.2:80
    │
    ▼
路由决策：目的 172.17.0.2 → 走 docker0 出口
    │
    ▼
FORWARD 链（filter 表），检查转发是否允许
    │
    ▼
POSTROUTING 链 (无需 SNAT，因为目标在 docker0 网段内)
    │
    ▼
docker0 网桥 → veth pair → 容器 eth0 → Nginx 进程
```

关键洞察：**到宿主机 9097 端口的入站包，经历了目的地改写（DNAT），但源地址仍然是外部客户端的真实 IP**（前提是外部客户端和宿主机在同一网段）。如果客户端在更远的互联网上，源地址可能会经历额外的 NAT。

用 iptables 验证当前的 DNAT 规则：

```bash
iptables -t nat -vnL DOCKER

# 输出示例：
# Chain DOCKER (2 references)
#  pkts bytes target     prot opt in     out     source    destination
#     5   320 DNAT       tcp  --  !docker0 *       0.0.0.0/0 0.0.0.0/0  tcp dpt:9097 to:172.17.0.2:80
```

`pkts` 列显示已有 5 个数据包命中了这条 DNAT 规则，说明端口映射在正常工作。

### 7.2.5 conntrack：连接跟踪机制

#### 为什么需要 conntrack？

回想上一节的场景：Nginx 响应包回到宿主机时，目的 IP 是 `192.168.1.100`（宿主机的 IP），而不是容器 IP。宿主机怎么知道这个响应应该转发给 `172.17.0.2:80` 而不是别的容器？

答案在于 **conntrack（Connection Tracking）**。它在 NAT 改写的那一刻就记住了这条连接的信息。

#### 五元组记录

当 DNAT 规则改写第一个 SYN 包时，conntrack 在内存中创建一条记录，保存 **五元组** 的映射关系：

```
原始方向:  192.168.1.50:50000 → 192.168.1.100:9097  (TCP SYN)
改写后:    192.168.1.50:50000 → 172.17.0.2:80       (TCP SYN)
```

conntrack 将这两个方向的五元组都记录下来：

```bash
# 查看当前连接跟踪表
conntrack -L | grep 172.17.0.2

# 输出示例：
# tcp      6 117 TIME_WAIT src=192.168.1.50 dst=192.168.1.100 sport=50000 dport=9097 \
#   [NAT] src=172.17.0.2 dst=192.168.1.50 sport=80 dport=50000
#   [ASSURED] mark=0 use=1
```

注意这条记录包含了两组五元组：
- **原始方向（Original）**：外部客户端看到的
- **回复方向（Reply）**：NAT 改写后的实际路径

当响应包返回时，conntrack 查找到匹配的回复方向记录，自动做 **反向 NAT**，将目的地址从 `192.168.1.100:9097` 改回 `172.17.0.2:80`。这个过程对外部客户端完全透明。

#### 高并发问题：conntrack table full

conntrack 表的容量是有限的。默认值因系统而异：

```bash
# 查看当前 conntrack 最大值
sysctl net.netfilter.nf_conntrack_max

# 查看当前 conntrack 使用量
sysctl net.netfilter.nf_conntrack_count
```

一个典型的 4GB 内存机器，默认 `nf_conntrack_max` 大约为 65536 或 262144。当短时间内产生大量连接（例如高并发 API 网关），conntrack 表可能被填满，导致以下错误：

```
dmesg | tail

# 输出：
# nf_conntrack: nf_conntrack: table full, dropping packet
```

**后果**：新连接无法建立，服务部分不可用。这是生产环境中最常见的问题之一。

**解决方案**：

```bash
# 方案一：增大 conntrack 最大值（临时生效）
sysctl -w net.netfilter.nf_conntrack_max=1048576

# 方案二：缩短超时时间，加速条目回收
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established=600

# 方案三：持久化配置
echo "net.netfilter.nf_conntrack_max = 1048576" >> /etc/sysctl.conf
echo "net.netfilter.nf_conntrack_tcp_timeout_established = 600" >> /etc/sysctl.conf
sysctl -p
```

> [!tip] 经验法则
> 每个并发连接消耗约 300 字节内核内存。计算需要的最大并发量，再乘以 1.5 的余量来设置 `nf_conntrack_max`。

### 7.2.6 默认 Bridge 模式的局限

默认 [[Bridge模式|Bridge]] 模式虽然即开即用，但有两个重要局限：

**局限一：容器间只能通过 IP 通信**

默认 docker0 网桥**不提供 DNS 解析**。容器 A（172.17.0.2）要访问容器 B（172.17.0.3），不能用容器名 `ping containerB`，只能用 IP：

```bash
docker exec containerA ping 172.17.0.3    # 可以
docker exec containerA ping containerB    # 不可以（默认 bridge）
```

这在容器重启后就会变成问题——IP 可能变化，写死的 IP 会失效。

**局限二：容器只能通过 `--link` 实现单向发现**

传统上使用 `--link` 标志可以添加 /etc/hosts 条目，但这种方法已经过时：

```bash
docker run -d --name web --link db:db my-web-app
```

但 `--link` 本质是修改 `/etc/hosts` 文件，而不是真正的 DNS 解析。在 Docker Compose 和自定义 Bridge 面前，这种方法已被淘汰。

## 7.3 自定义 Bridge 网络：生产环境的正确选择

针对默认 Bridge 的局限，Docker 提供了 **自定义 Bridge 网络**。

### 7.3.1 创建自定义 Bridge 网络

```bash
# 创建一个自定义 bridge 网络
docker network create --driver bridge \
  --subnet 10.10.0.0/16 \
  --gateway 10.10.0.1 \
  my-net
```

这个命令做了什么？与默认 bridge 的差异：

| 特性 | 默认 docker0 | 自定义 Bridge |
|------|-------------|--------------|
| DNS 解析 | 不支持容器名解析 | **内置 DNS 解析（127.0.0.11）** |
| 网络隔离 | 所有容器都在 docker0 上互通 | 每个自定义 bridge 独立隔离 |
| 运行时连接 | 启动时通过 `--network` 指定 | 支持动态 `connect`/`disconnect` |
| IP 分配 | 自动从 172.17.0.0/16 分配 | 可自定义子网 |
| 生产推荐度 | 低 | **高** |

### 7.3.2 内置 DNS 解析：127.0.0.11

Docker 内置了一个轻量级 DNS 解析器，监听 **127.0.0.11:53**。当容器使用自定义 Bridge 网络时：

1. Docker 自动将容器的 `/etc/resolv.conf` 中的 nameserver 设置为 `127.0.0.11`
2. 容器间通过容器名互相解析，DNS 服务器自动返回容器 IP
3. 如果查询的域名不在 Docker 网络内，转发给宿主机的 DNS 配置

验证方式：

```bash
# 创建并启动两个容器在同一个自定义网络上
docker run -d --name app1 --network my-net alpine sleep 3600
docker run -d --name app2 --network my-net alpine sleep 3600

# 在 app1 中通过容器名访问 app2
docker exec app1 ping app2

# 预期输出：
# PING app2 (10.10.0.3): 56 data bytes
# 64 bytes from 10.10.0.3: seq=0 ttl=64 time=0.123 ms
```

这就是生产环境更推荐自定义 Bridge 的原因——**容器名不再是摆设，而是可用的服务发现机制**。

### 7.3.3 运行时动态连接/断开

自定义 Bridge 支持运行时修改网络连接，默认 docker0 不支持：

```bash
# 将运行中的容器连接到额外网络
docker network connect my-net app1

# 断开连接
docker network disconnect my-net app1

# 查看容器的网络连接
docker inspect app1 --format '{{json .NetworkSettings.Networks}}'
```

这种灵活性在**蓝绿部署**或**流量切换**场景中非常有用——你可以在不重启容器的情况下，将其从一个网络切换到另一个网络。

## 7.4 Host 模式：零网络损耗

### 7.4.1 原理

Host 模式是最简单的——**容器直接共享宿主机的网络命名空间**。不创建独立的网络栈，不分配私有 IP，不做端口映射。

启动命令：

```bash
docker run --network host -d nginx:alpine
```

### 7.4.2 与非 Host 模式的差异

在 Host 模式下：

- 容器内的 `eth0` 不存在了
- `ip addr` 看到的就是宿主机的网卡
- Nginx 直接监听在宿主机 `80` 端口（无需 `-p` 映射）
- 容器间的端口冲突需要应用自行协调

```bash
# 验证：宿主机和容器看到相同的网络信息
docker exec host-nginx ip addr show eth0
# 和宿主机上执行 ip addr show eth0 输出完全一致
```

### 7.4.3 性能优势

Host 模式的性能优势来自**零网络开销**：

| 维度 | Bridge 模式 | Host 模式 |
|------|-----------|----------|
| 数据路径 | 容器 → veth → docker0 → iptables → 物理网卡 | 容器 → 直接使用物理网卡 |
| 额外延迟 | ~0.05ms（iptables + veth 复制） | **~0.02ms**（几乎为 0） |
| 吞吐量 | 80-90% 物理网卡性能 | **95%+ 物理网卡性能** |
| CPU 开销 | 中（iptables 连接跟踪 + NAT） | **接近 0%** |

性能差异在最坏情况下可达 30% 以上，在**高吞吐网络应用**（如代理、网关、日志采集器）中尤为明显。

### 7.4.4 典型使用场景

```bash
# 1. 网络监控工具（需要看到宿主机所有网络接口）
docker run --network host -d nicolaka/netshoot

# 2. 高性能代理
docker run --network host -d nginx:alpine
# Nginx 直接监听 80/443，零网络损耗

# 3. 需要操作宿主机网络配置的工具
docker run --network host --privileged -d weavenet/weave
```

> [!warning] 注意
> Host 模式**仅支持 Linux**。在 macOS 和 Windows 上，[[Docker]] 通过虚拟机运行，`--network host` 的实际行为与 Linux 不同。

## 7.5 Container 模式：共享网络命名空间

### 7.5.1 原理

Container 模式（也叫 **Sidecar 模式**）让一个容器共享另一个容器的网络命名空间。两者通过 `localhost` 互相通信。

```
┌─────────────────────────────────────┐
│        容器 A 的网络命名空间          │
│                                     │
│  ┌─────────────┐  ┌─────────────┐   │
│  │   主容器    │  │  Sidecar    │   │
│  │  (nginx)   │  │ (fluentd)   │   │
│  │  172.17.0.2│  │  127.0.0.1  │   │
│  └──────┬─────┘  └──────┬──────┘   │
│         │               │          │
│         └───────┬───────┘          │
│                 │ localhost         │
│             ┌───┴───┐              │
│             │  eth0 │              │
│             └───────┘              │
└─────────────────────────────────────┘
                 │
                 ▼
              docker0
```

关键点：

- **只有一个 eth0**，两个容器共享
- Sidecar 容器通过 `127.0.0.1` 访问主容器的服务
- 两者共享 IP、端口空间、路由表

### 7.5.2 实战：Nginx + Fluentd 日志采集

```bash
# 步骤1：启动主容器（Nginx）
docker run -d --name web-server nginx:alpine

# 步骤2：查看主容器的 IP
docker inspect web-server --format '{{.NetworkSettings.IPAddress}}'
# 输出：172.17.0.2

# 步骤3：启动 Sidecar 容器，共享主容器的网络命名空间
docker run -d --name log-collector \
  --network container:web-server \
  fluentd
```

在 `log-collector` 中，可以通过 `localhost:80` 访问 Nginx：

```bash
docker exec log-collector curl http://localhost:80
# 成功返回 Nginx 欢迎页
```

### 7.5.3 与 Kubernetes Pod 设计的关系

Container 模式的设计理念直接影响 [[Kubernetes]] 的 **Pod 模型**。在 K8s 中，一个 Pod 包含多个容器，所有容器共享同一个网络命名空间：

```
Kubernetes Pod
┌─────────────────────────────────────┐
│        共享网络命名空间               │
│                                     │
│  ┌─────────┐  ┌─────────┐          │
│  │  App    │  │ Sidecar │          │
│  │ (Java)  │  │ (Envoy) │          │
│  │         │  │         │          │
│  └────┬────┘  └────┬────┘          │
│       │ localhost  │               │
│       └──────┬─────┘               │
│          ┌───┴───┐                  │
│          │ eth0  │                  │
│          └───────┘                  │
└─────────────────────────────────────┘
```

**Docker Container 模式就是 K8s Pod 网络模型的前身**。理解了这个模式，你就理解了为什么 K8s Pod 中的多个容器可以通过 `localhost` 互相通信。

### 7.5.4 使用注意事项

```bash
# 错误：试图释放 sidecar 容器的端口
docker run -d --name sidecar --network container:web -p 9090:9090 my-sidecar
# 报错：Cannot publish ports when using container network mode

# 正确：端口映射只在主容器上设置
docker run -d --name web -p 9097:80 nginx:alpine
docker run -d --name sidecar --network container:web my-sidecar
```

**关键规则**：端口映射（`-p`）只能在主容器上配置，Sidecar 共享主容器的所有端口。

## 7.6 None 模式：完全自定义

### 7.6.1 原理

None 模式给容器一个**空的网络命名空间**——没有网卡、没有 IP、没有路由。容器内只有一个 `lo` 回环接口：

```bash
docker run --network none -d alpine sleep 3600

# 在容器中查看网络
docker exec none-test ip addr
# 输出：只有 lo（127.0.0.1），没有 eth0
```

### 7.6.2 使用场景

None 模式适用于以下场景：

1. **离线计算任务**：纯 CPU/GPU 计算任务，不需要任何网络
2. **完全自定义网络**：用户自己通过 `docker network connect` 按需接入网络

```bash
# 创建 none 模式容器后，再动态接入自定义网络
docker run -d --name compute --network none alpine sleep 3600

# 处理完离线数据后，接入网络上报结果
docker network connect my-net compute
docker exec compute curl http://my-api-server/report
```

## 7.7 本章总结

- **[[Bridge模式|Bridge]] 模式**是 Docker 的默认网络模式，通过 docker0 网桥 + veth pair + iptables NAT 实现容器网络隔离和对外通信。数据包出宿主机时经过 MASQUERADE（源地址伪装），入宿主机时经过 DNAT（目的地址改写）。
- **conntrack（连接跟踪）** 记录 NAT 转换的五元组映射关系，确保响应包能被正确还原。高并发场景下需要监控 `nf_conntrack_max`，避免出现 `table full` 丢包问题。
- **自定义 Bridge 网络**比默认 docker0 更强大：内置 `127.0.0.11` DNS 解析支持容器名寻址，支持运行时动态连接/断开，适合生产环境。
- **Host 模式**让容器共享宿主机的网络命名空间，零网络开销（延迟 ~0.02ms，吞吐 95%+），适用于高性能代理和网络工具，但牺牲了端口隔离。
- **Container 模式**（Sidecar 模式）让两个容器共享同一个网络命名空间，通过 `localhost` 通信。这是 [[Kubernetes]] Pod 网络模型的前身。
- **None 模式**提供完全空的网络命名空间，适用于离线计算和完全自定义网络方案。

### 下一章预告

本章所有模式都局限于**单台主机**。跨主机容器如何通信？下一章介绍的 [[Overlay网络|Overlay]] 模式通过 [[VXLAN]] 隧道解决这个问题，同时 [[Macvlan]] 和 [[Ipvlan]] 模式提供了近乎物理网卡性能的高性能方案。
