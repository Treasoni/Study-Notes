# 第五章：Linux 网络虚拟化基石 — 网络命名空间与 veth

> **笔记类型**：概念笔记 | **阅读时间**：30 分钟
> **前置要求**：理解 VLAN 概念（第二章）、基本的 Linux 命令行操作

## 开篇

前四章我们一直在讨论**物理网络设备层面**的虚拟化 — VLAN 在交换机上切分广播域，VXLAN 在物理 IP 网络上叠加虚拟二层网络，SDN 让转发设备与控制逻辑解耦。但所有这些技术最终要落地到**主机内部**。一台物理服务器上跑着多个虚拟机或容器，它们如何共享同一块物理网卡？如何实现彼此隔离？如何在需要时互相通信？

答案是 Linux 内核内置的两个关键机制：**网络命名空间（network namespace）** 和 **veth pair（虚拟以太网对）**。它们是所有容器网络方案（Docker、Kubernetes、LXC）的底层基石。理解它们，就等于拿到了理解全部虚拟网络的钥匙。

---

## 1. 网络命名空间：制造"独立网络栈"的魔法

### 1.1 想象一个"网络沙盒"

想象你有一台物理服务器，上面插着一块网卡，配着 IP `192.168.1.100`。这台服务器的 `/etc/hosts` 里写了一些域名解析规则，iptables 里有几条防火墙规则，路由表知道自己该走哪个网关。

现在，你想在这台服务器上跑两个 Web 应用，每个应用都需要独立的网络环境：

- 应用 A 需要使用 `192.168.1.101`，监听端口 `80`，有自己的防火墙规则
- 应用 B 需要使用 `10.0.0.2`，监听端口 `8080`，另一个防火墙规则

直接跑的话，它们会互相冲突。怎么办？

**网络命名空间**就是用来解决这个问题的。它把 Linux 内核的网络协议栈**复制**出一份独立的副本，每个命名空间拥有完整的独立网络栈。

### 1.2 命名空间里有什么？

当你创建一个新的网络命名空间时，它获得了一整套"空白的"网络基础设施：

```
┌──────────────────────────────────────────────┐
│              网络命名空间 net0                │
│                                              │
│  ┌──────────┐  ┌────────┐  ┌──────────────┐ │
│  │   网卡    │  │ 路由表 │  │ iptables规则  │ │
│  │ (空的)    │  │ (空的) │  │  (空的)       │ │
│  └──────────┘  └────────┘  └──────────────┘ │
│                                              │
│  ┌──────────┐  ┌────────┐  ┌──────────────┐ │
│  │   socket  │  │ ARP表  │  │  连接跟踪表   │ │
│  │  (空的)   │  │ (空的) │  │  (空的)       │ │
│  └──────────┘  └────────┘  └──────────────┘ │
│                                              │
│  ┌──────────┐  ┌─────────────────────────┐   │
│  │ /proc/net │  │ /sys/class/net          │   │
│  └──────────┘  └─────────────────────────┘   │
└──────────────────────────────────────────────┘
```

具体来说，每个网络命名空间包含以下独立资源：

| 资源类别 | 具体内容 | 说明 |
|---------|---------|------|
| 网络接口 | 网卡、lo 回环接口 | 创建时只有 lo 接口（默认 down 状态） |
| IPv4/IPv6 协议栈 | IP 地址、IP 层参数 | `/proc/sys/net/ipv4/*` 完全独立 |
| 路由表 | FIB（转发信息库） | 完全独立，`ip route` 互不影响 |
| 邻居表 | ARP 表、NDP 表 | 独立 MAC 地址解析 |
| Netfilter | iptables 规则链 | 包含所有表（filter/nat/mangle/raw） |
| 连接跟踪 | conntrack 表 | 独立跟踪连接状态 |
| Socket | 端口号空间 | 不同命名空间可用相同端口无冲突 |
| /proc/net | 进程网络信息 | 不同命名空间看到不同内容 |

**关键洞察**：端口号是命名空间隔离的。命名空间 A 里的 `:80` 和命名空间 B 里的 `:80` 互不冲突 — 它们是完全不同的端口空间。

### 1.3 默认命名空间（Root Namespace）

系统启动时，默认有一个网络命名空间，称为 **root network namespace**。你平常操作的 Linux 网络环境，就是这个默认命名空间。

Docker 或 LXC 启动容器时，会为容器创建新的网络命名空间，并把这个新命名空间"移入"容器进程。这样一来，容器里的进程看到的网络环境就和宿主机完全隔离。

> **技术上**：每个 Linux 进程都有一个 `/proc/$PID/ns/net` 符号链接指向其网络命名空间。进程创建（`clone()`）时指定 `CLONE_NEWNET` 标志，就会进入新命名空间。

---

## 2. 实操：使用 ip netns 管理命名空间

Linux 提供了 `ip netns` 命令来管理网络命名空间。让我们动手操作。

### 2.1 创建和查看命名空间

```bash
# 创建两个命名空间
sudo ip netns add ns_red
sudo ip netns add ns_blue

# 列出所有命名空间
sudo ip netns list
```

输出示例：
```
ns_blue
ns_red
```

每个命名空间默认只有一个回环接口（`lo`），而且是 down 状态的：

```bash
# 查看 ns_red 中的网络接口
sudo ip netns exec ns_red ip link list
```

输出示例：
```
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

注意 `state DOWN` — 这个 lo 接口还不能用。

```bash
# 启用 ns_red 中的 lo
sudo ip netns exec ns_red ip link set lo up

# 现在 lo 是 UP 了
sudo ip netns exec ns_red ip link list
```

输出示例：
```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noop state UNKNOWN ...
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

> **`ip netns exec` 是什么？** 它让后续命令在指定命名空间的网络栈中执行。可以理解为"钻进那个网络沙盒里执行命令"。

### 2.2 命名空间之间是彻底隔离的

```bash
# 在 root 命名空间查看路由表
ip route show | head -5

# 在 ns_red 中查看路由表 — 空的！
sudo ip netns exec ns_red ip route show
```

输出示例：
```
# root 命名空间有路由表条目（具体取决于网络配置）
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100

# ns_red — 空的，什么都没有
```

这意味着命名空间内的进程无法访问外部网络，除非我们手动给它"接上网线"。

---

## 3. veth pair：虚拟网线

### 3.1 概念

网络命名空间创建了一个独立的网络环境，但它是一个"孤岛" — 里面的进程无法和外界通信。我们需要一种方式，把命名空间"接入网络"。

这就是 **veth pair（虚拟以太网对）** 的用武之地。

**想象一根虚拟网线**，两端各连着一个虚拟网卡。数据从一端进入，就从另一端出来。这就是 veth pair。

```
┌─────────────┐                    ┌─────────────┐
│  命名空间A  │                    │  命名空间B  │
│             │                    │             │
│  ┌───────┐  │    veth0 ---- veth1   ┌───────┐  │
│  │ veth0 │──┼───────────────────────│ veth1 │  │
│  └───────┘  │                    └───────┘  │
│             │                    │             │
└─────────────┘                    └─────────────┘
```

**关键理解**：
- veth pair 是成对出现的，永远是一端进、另一端出
- 它像一根"网线"，两端的网卡就是水晶头
- 你可以把一端留在 root 命名空间，另一端移入新命名空间 — 这就实现了命名空间和宿主机之间的网络连通

### 3.2 创建并配通 veth pair

下面是最基本的操作 — 创建一个 veth pair，将一端放入命名空间，配 IP、启用，验证连通性。

```bash
# 步骤 1：创建 veth pair
# 创建一对虚拟网卡，一端叫 veth0，另一端叫 veth1
sudo ip link add veth0 type veth peer name veth1

# 步骤 2：查看宿主机的网卡列表，此时两个 veth 都在 root 命名空间
ip link show | grep veth
```

输出示例：
```
5: veth1@veth0: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 ...
6: veth0@veth1: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 ...
```

两个 veth 接口目前都在 root 命名空间。现在把 `veth1` 移入 `ns_red`：

```bash
# 步骤 3：将 veth1 移入 ns_red 命名空间
sudo ip link set veth1 netns ns_red

# 再次查看宿主机的网卡 — veth1 消失了！
ip link show | grep veth
```

输出示例：
```
6: veth0@if5: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 ...
```

`veth1` 已经不在这台宿主机的 root 命名空间里了 — 它属于 `ns_red` 了。

```bash
# 步骤 4：在 ns_red 中查看，veth1 在里面
sudo ip netns exec ns_red ip link show | grep veth
```

输出示例：
```
5: veth1@if6: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 ...
```

现在为两端配置 IP 地址，并启用它们：

```bash
# 步骤 5：配置 IP
sudo ip addr add 10.10.10.1/24 dev veth0           # root 命名空间的 veth0
sudo ip netns exec ns_red ip addr add 10.10.10.2/24 dev veth1  # ns_red 中的 veth1

# 步骤 6：启用接口
sudo ip link set veth0 up
sudo ip netns exec ns_red ip link set veth1 up

# 步骤 7：测试连通性 — 从 root 命名空间 ping ns_red
ping -c 3 10.10.10.2
```

输出示例：
```
PING 10.10.10.2 (10.10.10.2) 56(84) bytes of data.
64 bytes from 10.10.10.2: icmp_seq=1 ttl=64 time=0.087 ms
64 bytes from 10.10.10.2: icmp_seq=2 ttl=64 time=0.052 ms
64 bytes from 10.10.10.2: icmp_seq=3 ttl=64 time=0.052 ms

--- 10.10.10.2 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2089ms
rtt min/avg/max/mdev = 0.052/0.063/0.087/0.016 ms
```

延时只有 0.05-0.09 毫秒 — 和物理网络完全不在一个量级。这是纯内核内的数据传输，没有物理线缆的延迟。

```
┌─────────────────────┐      ┌──────────────────┐
│  root namespace     │      │  ns_red           │
│                     │      │                   │
│  ┌──────┐           │      │           ┌──────┐│
│  │ veth0│───────────┼──────┼───────────│veth1 ││
│  │      │10.10.10.1 │      │10.10.10.2 │      ││
│  └──────┘           │      │           └──────┘│
└─────────────────────┘      └──────────────────┘
```

> **`@ifN` 是什么意思？** `veth1@if6` 中的 `@if6` 表示对端接口在内核中的索引号。这是 veth pair 特有的显示方式，帮助你知道这根"网线"的另一端连到了哪个接口。

### 3.3 veth pair 转发原理

当 `ns_red` 中的进程想要访问 `10.10.10.1` 时：

1. 进程通过 socket 发送数据包到 `ns_red` 协议栈
2. 路由表查找目标 `10.10.10.1`，发现是同网段直连
3. 从 `veth1` 接口发出
4. **内核直接将数据包"传递"到对端 `veth0`** — 本质是一个内核函数调用，内存中的 sk_buff 结构体被传递给对端
5. root 命名空间的协议栈收到来自 `veth0` 的数据包
6. 目标 IP 匹配到 `veth0` 的地址 `10.10.10.1`，数据送达

整个过程没有经过任何物理硬件，全在内核内部完成。

---

## 4. namespace + bridge：构建虚拟网络

单个 veth pair 连接两个命名空间还行，但如果有 5 个、10 个命名空间需要互相通信呢？两两连接显然不现实。

这就是 **Linux bridge（网桥）** 登场的时候。它扮演虚拟交换机的角色，所有命名空间的 veth 一端都插到 bridge 上。

### 4.1 组网拓扑

```
┌─────────────────────────────────────────────────┐
│                 root namespace                    │
│                                                   │
│  ┌──────┐                                        │
│  │ eth0 │ (物理网卡，连接外部网络)                 │
│  └──┬───┘                                        │
│     │                                            │
│  ┌──▼──────────┐                                 │
│  │   br0       │ (Linux bridge, 虚拟交换机)       │
│  │ 10.0.0.1/24│                                 │
│  └──┬──┬──┬───┘                                 │
│     │  │  │                                      │
│  ┌──┘  │  └──┐                                   │
│  │     │     │                                   │
│  ▼     ▼     ▼                                   │
│ veth0 veth2 veth4    (root 命名空间端)            │
│  │     │     │                                   │
│  │     │     │                                   │
│  ▼     ▼     ▼                                   │
│ veth1 veth3 veth5    (移入各命名空间)             │
│  │     │     │                                   │
│ ┌┘     │     └┐                                  │
│ │      │      │                                  │
│ ▼      ▼      ▼                                  │
│ns_red ns_blue ns_green                            │
│10.0.0.2 10.0.0.3 10.0.0.4                       │
└─────────────────────────────────────────────────┘
```

### 4.2 完整配置步骤

```bash
#!/bin/bash
# 完整组网脚本：3 个命名空间通过 bridge 互通

# === 1. 清理旧环境（如果之前跑过） ===
sudo ip netns del ns_red 2>/dev/null
sudo ip netns del ns_blue 2>/dev/null
sudo ip netns del ns_green 2>/dev/null
sudo ip link del br0 2>/dev/null

# === 2. 创建命名空间 ===
sudo ip netns add ns_red
sudo ip netns add ns_blue
sudo ip netns add ns_green

# === 3. 创建 veth pairs ===
# 命名空间 红色
sudo ip link add veth_red type veth peer name veth_red_b
# 命名空间 蓝色
sudo ip link add veth_blue type veth peer name veth_blue_b
# 命名空间 绿色
sudo ip link add veth_green type veth peer name veth_green_b

# 注：_b 后缀端将挂到 bridge 上，另一端放入命名空间

# === 4. 将 veth 一端移入命名空间 ===
sudo ip link set veth_red netns ns_red
sudo ip link set veth_blue netns ns_blue
sudo ip link set veth_green netns ns_green

# === 5. 创建 bridge ===
sudo ip link add name br0 type bridge
sudo ip link set br0 up

# === 6. 将 veth 的另一端（_b 端）挂到 bridge 上 ===
sudo ip link set veth_red_b master br0
sudo ip link set veth_red_b up

sudo ip link set veth_blue_b master br0
sudo ip link set veth_blue_b up

sudo ip link set veth_green_b master br0
sudo ip link set veth_green_b up

# === 7. 配置命名空间内的 IP、启用 lo 和 veth ===
sudo ip netns exec ns_red ip link set lo up
sudo ip netns exec ns_red ip link set veth_red up
sudo ip netns exec ns_red ip addr add 10.0.0.2/24 dev veth_red

sudo ip netns exec ns_blue ip link set lo up
sudo ip netns exec ns_blue ip link set veth_blue up
sudo ip netns exec ns_blue ip addr add 10.0.0.3/24 dev veth_blue

sudo ip netns exec ns_green ip link set lo up
sudo ip netns exec ns_green ip link set veth_green up
sudo ip netns exec ns_green ip addr add 10.0.0.4/24 dev veth_green

# === 8. 给 bridge 配置 IP（作为各命名空间的网关） ===
sudo ip addr add 10.0.0.1/24 dev br0

# === 9. 验证 ===
echo ""
echo "===== 从 ns_red ping ns_blue ====="
sudo ip netns exec ns_red ping -c 2 10.0.0.3

echo ""
echo "===== 从 ns_blue ping ns_green ====="
sudo ip netns exec ns_blue ping -c 2 10.0.0.4

echo ""
echo "===== 从 ns_green ping host (br0) ====="
sudo ip netns exec ns_green ping -c 2 10.0.0.1
```

### 4.3 验证结果

```bash
# 从 ns_red ping ns_blue
PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=0.112 ms
64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.087 ms

# 查看 bridge 的 MAC 地址表 — 相当于物理交换机的 CAM 表
bridge fdb show dev br0
```

输出示例：
```
2e:3a:4b:5c:6d:7e master br0
ab:cd:ef:12:34:56 master br0
...
```

这里的 `bridge fdb` 命令显示的正是 Linux bridge 学到的 MAC 地址表 — 和物理交换机用 `show mac-address-table` 看到的东西完全一样。

### 4.4 关键理解：bridge 就是一台软件交换机

Linux bridge 的行为和物理二层交换机完全一致：

| 功能 | 物理交换机 | Linux bridge |
|------|-----------|-------------|
| MAC 地址学习 | 硬件 ASIC 学习 | 内核学习（通过 `bridge fdb` 查看） |
| 转发决策 | 查 MAC 地址表 | 查 FDB 表 |
| 广播/未知单播 | 泛洪到所有端口（除入端口） | 内核泛洪到所有 bridge 端口 |
| STP 生成树 | 硬件支持 | 内核支持（`bridge stp` 可开启） |
| VLAN 过滤 | IEEE 802.1Q | 支持（`bridge vlan` 可配置） |

**唯一的区别**：物理交换机转发靠专用 ASIC 芯片，Linux bridge 转发靠内核 CPU。但在小规模场景下，Linux bridge 的性能完全足够。

---

## 5. 与容器网络的关系

### 5.1 Docker 的默认 network 模式其实就是你刚搭的

值得反复强调的一点：你上一节用手动命令搭出来的"bridge + 多个命名空间 + veth pair"网络，**本质上就是 Docker 默认的 bridge 网络的工作方式**。

Docker 替你做了这些事：

```bash
# Docker 创建一个名为 docker0 的 bridge
# 为每个容器创建一个网络命名空间
# 为每个容器创建一对 veth
# 一端挂到 docker0，另一端放入容器的命名空间
# 通过 DHCP-like 机制分配 IP（通常 172.17.0.0/16 子网）
```

对比：

| 组件 | 手动配置 | Docker 自动配置 |
|------|---------|----------------|
| Bridge | `br0` | `docker0`（或自定义 bridge） |
| 命名空间 | `ns_red`、`ns_blue` | 每个容器一个隐藏的命名空间 |
| veth pair | `veth_red/veth_red_b` | `vethXXX`（Docker 自动取名） |
| IP | 手动 `ip addr add` | Docker 自动从子网分配 |
| 默认网关 | bridge 的 IP | bridge 的 IP |
| 外部访问 | 需要额外配置 NAT | 自动添加 iptables MASQUERADE |

### 5.2 一句话说清

> **容器实际上就是一个"轻量级网络命名空间 + veth pair + 约束进程"的组合。**

当你运行 `docker run` 时，Docker 做的事情和你手动打那些 `ip netns` / `ip link` 命令完全一样，只不过自动化了，并加上了 cgroups 资源限制和文件系统隔离。

### 5.3 Docker Host 模式

现在再回头看 Docker 的 host 模式就很好理解了：

```bash
docker run --net=host nginx
```

这个命令的本质是：不让 Docker 创建新的网络命名空间，容器进程直接使用 root 命名空间的网络栈。这相当于你在宿主机上直接启动 nginx，性能当然最好，但也完全失去了网络隔离性。

---

## 6. 扩展：命名空间间的三层互通

上面的例子是二层互通 — 所有命名空间在同一个子网 `10.0.0.0/24` 内，全靠 bridge 转发。如果你想实现**跨子网通信**（即让 `ns_red` 在 `10.0.0.0/24`，`ns_blue` 在 `10.0.1.0/24`），就需要**路由 + 命名空间充当网关**了。

思路：再创建一个命名空间充当"路由器"，它分别连接两个子网的 bridge，并启用 IP 转发。

```bash
# 创建一个路由器命名空间
sudo ip netns add router

# 创建两组 veth pair
# 第一组连接左侧子网 (10.0.0.0/24)
sudo ip link add veth_left type veth peer name veth_left_b
sudo ip link set veth_left netns router
sudo ip link set veth_left_b master br_left   # br_left 是左侧 bridge

# 第二组连接右侧子网 (10.0.1.0/24)
sudo ip link add veth_right type veth peer name veth_right_b
sudo ip link set veth_right netns router
sudo ip link set veth_right_b master br_right  # br_right 是右侧 bridge

# 在 router 命名空间中配置两侧 IP 并启用 IP 转发
sudo ip netns exec router ip addr add 10.0.0.254/24 dev veth_left
sudo ip netns exec router ip addr add 10.0.1.254/24 dev veth_right
sudo ip netns exec router sysctl -w net.ipv4.ip_forward=1

# 在左侧命名空间中设置默认网关指向 router
sudo ip netns exec ns_red ip route add default via 10.0.0.254

# 在右侧命名空间中设置默认网关指向 router
sudo ip netns exec ns_blue ip route add default via 10.0.1.254

# 现在 ns_red 可以 ping 通 ns_blue
sudo ip netns exec ns_red ping -c 2 10.0.1.2
```

```
 ┌─────────────┐        ┌──────────────┐        ┌─────────────┐
 │ 左侧子网     │        │ router 命名空间│        │ 右侧子网     │
 │ 10.0.0.0/24 │        │              │        │ 10.0.1.0/24 │
 │             │        │ 10.0.0.254   │        │             │
 │ ns_red      │        │ 10.0.1.254   │        │ ns_blue     │
 │ 10.0.0.2 ───┼────────┼── veth_left  ┼────────┼─── 10.0.1.2 │
 └─────────────┘        └──────────────┘        └─────────────┘
```

这就是容器网络 CNI 插件（如 Flannel、Calico）的原始形态 — 它们只不过把这个"路由器命名空间"换成了更高效的方式（如 VTEP 设备或 BGP 路由）。

---

## 7. 常见陷阱

### 陷阱 1：忘记启用 IP 转发

命名空间之间跨子网 ping 不通时，首要检查：

```bash
# 在用作网关的命名空间中检查
sudo ip netns exec router sysctl net.ipv4.ip_forward
# 期望输出：net.ipv4.ip_forward = 1
```

### 陷阱 2：bridge 上 STP 阻塞端口

如果 bridge 上有多个端口且拓扑存在环路，STP 会阻塞端口。Linux bridge 默认 STP 是关闭的，但如果开启了却未收敛，会导致丢包：

```bash
# 查看 bridge 的 STP 状态
bridge link show
# 如果不需要，关闭 STP
sudo ip link set br0 type bridge stp_state 0
```

### 陷阱 3：命名空间无法访问外网

命名空间默认只有 veth pair 通向 host，没有通往物理网络的路径。如果命名空间需要访问互联网，需要：

1. 在 root 命名空间开启 IP 转发
2. 添加 iptables MASQUERADE 规则

```bash
# 宿主机上开启转发
sudo sysctl -w net.ipv4.ip_forward=1

# 添加 NAT 规则（假设命名空间网段 10.0.0.0/24，物理网卡 eth0）
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE
```

### 陷阱 4：忘记清理导致资源泄漏

每创建一个网络命名空间，内核都会占用一些资源。忘记清理的命名空间会累积：

```bash
# 如果 br0 已被某个命名空间的 veth 占用，先删 veth 再删 br0
sudo ip link delete veth_red_b     # 删除一端，对端自动被清理
sudo ip link delete br0            # 等所有 veth 移除后才能删除 bridge
sudo ip netns del ns_red           # 删除命名空间
```

---

## 本章小结

- **网络命名空间**是 Linux 内核提供的网络栈隔离机制，每个命名空间拥有完全独立的网卡、路由表、iptables 规则、端口号和 socket。不同命名空间内的进程使用相同的端口号不会冲突。
- **veth pair** 是一根虚拟网线，数据从一端进入就从另一端出来。它用来将不同的网络命名空间"连接"起来，或者将命名空间"接入"宿主机的网络栈。
- **Linux bridge + veth pair + 多个命名空间**的组合构成了容器网络的基石。一台 Docker 主机上的 `docker0` bridge + veth pair 组网方式，本质上和你手动 `ip link` 搭建的网络完全一致。
- **跨命名空间的路由**需要借助额外的"路由器"命名空间，并启用 IP 转发功能，这也是 CNI 插件实现跨节点通信的底层思路。
- 操作网络命名空间的核心命令是：`ip netns add`（创建）、`ip netns exec`（进入执行）、`ip link set ... netns`（移动接口）。

## 下一章预览

理解了主机内部的网络虚拟化基石后，我们来看看更传统的场景 — **虚拟机网络模式**。VMware 和 KVM 各提供了哪些网络模式？桥接、NAT、仅主机之间如何选型？当 Docker 和 VM 混合部署时，如何避免"两层 NAT"带来的性能灾难？下一章我们来逐一拆解。
