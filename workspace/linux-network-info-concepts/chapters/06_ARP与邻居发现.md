# ARP 与邻居发现

## 从一个问题开始

两台机器在同一个二层网络（比如连在同一个交换机上），A 要发一个 IP 包给 B。A 知道 B 的 IP 地址（`192.168.1.5`），但以太网帧的目标地址需要的是 **MAC 地址**，而不是 IP 地址。A 怎么知道 B 的 MAC 是什么？

这个"IP 到 MAC"的映射就是本章要解决的核心问题。映射表由 **ARP 协议**（IPv4）或 **NDP**（IPv6）维护，而 `ip neigh` 就是我们查看和操作这张表的命令。

> [!note] 前置知识
> 读本章前，你应该了解 MAC 地址（6 字节的网卡硬件地址）和 IP 地址的基本区别。如果你对 MAC 地址不太熟悉，建议先读第二章"网络接口与链路层信息"。

---

## ARP 协议核心概念

### 广播请求，单播回复

ARP（Address Resolution Protocol，地址解析协议）的工作原理非常简单，只有两个步骤：

```
主机 A (192.168.1.2, MAC: aa:aa:aa:aa:aa:aa)
想找 B (192.168.1.5) 的 MAC

Step 1: 广播  ──→ 交换机 ──→ 所有同网段设备
          "谁是 192.168.1.5？请告诉 aa:aa:aa:aa:aa:aa"
          ┌───────────────┐
          │ 目标 MAC: FF:FF:FF:FF:FF:FF  ← 广播地址
          │ 源 MAC:    aa:aa:aa:aa:aa:aa  ← A 自己的 MAC
          │ 请求:      192.168.1.5 的 MAC 是谁？
          └───────────────┘

Step 2: 单播  ←── 只有 B 回复
          "192.168.1.5 是我，我的 MAC 是 bb:bb:bb:bb:bb:bb"
          ┌───────────────┐
          │ 目标 MAC: aa:aa:aa:aa:aa:aa  ← 单播直接发给 A
          │ 源 MAC:    bb:bb:bb:bb:bb:bb  ← B 响应
          │ 回复:      192.168.1.5 → bb:bb:bb:bb:bb:bb
          └───────────────┘
```

关键特征：

| 特征 | 说明 |
|------|------|
| **广播请求** | 目标 MAC 填 `FF:FF:FF:FF:FF:FF`，同一广播域内所有设备都会收到 |
| **单播回复** | 只有目标 IP 对应的设备回复，回复是单播（直接发给请求者） |
| **缓存** | 解析结果存入内核的 ARP 缓存（邻居表），后续不再广播 |
| **超时** | 条目有生存时间（通常几十秒到几分钟），超时后重新探测 |
| **协议标识** | 以太网帧中 EtherType = `0x0806` 表示 ARP |

> [!tip] 抓包验证
> 可以用 `tcpdump -i eth0 arp` 抓到 ARP 请求和回复包。你会看到广播请求的 MAC 目标地址全是 `ff:ff:ff:ff:ff:ff`，而回复是单播。

### ARP 只在同一广播域内工作

这是 **非常关键** 的一点：ARP 不能跨路由器工作。如果目标 IP 不在同一子网，主机会把包发给默认网关，然后用 ARP 解析 **网关的 MAC**，而非目标 IP 的 MAC。

```
# 本机 IP: 192.168.1.2/24
# 默认网关: 192.168.1.1
# 目标: 8.8.8.8（不在同一子网）

# 本机判断：8.8.8.8 不在 192.168.1.0/24 内
# 行为：ARP 查询的是 192.168.1.1（网关）的 MAC，不是 8.8.8.8 的
```

---

## 邻居状态机详解

ARP 缓存中的每个条目都有一个**状态**，标志着该映射的"信任程度"。理解这些状态是排障的基础。

```
                    ┌──────────┐
                    │  PERMANENT │  ← 静态配置，永不超时
                    └─────┬────┘
                          │
    ┌───────────┐    ┌───▼────┐
    │  FAILED   │◄───│ 刚添加  │
    └───────────┘    └───┬────┘
                         │ 解析成功
                    ┌────▼─────┐
                    │ REACHABLE │  ← 最近确认过可达
                    └────┬─────┘
                         │ 超时（约 30s）
                    ┌────▼────┐
                    │  STALE  │  ← 可能还可用，但未验证
                    └────┬────┘
                         │ 要发包给这个邻居
                    ┌────▼────┐
                    │  DELAY  │  ← 延迟验证期（约 5s）
                    └────┬────┘
                         │ 仍然没确认
                    ┌────▼────┐
                    │  PROBE  │  ← 发单播探测（最多 3 次）
                    └────┬────┘
                    成功／│ 失败
                 ┌───────┴────────┐
                 ▼                ▼
            ┌──────────┐   ┌──────────┐
            │REACHABLE │   │  FAILED  │
            └──────────┘   └──────────┘
```

### 状态详解

| 状态 | 含义 | 典型触发条件 |
|------|------|-------------|
| **REACHABLE** | 最近确认过可达，映射有效 | 刚完成 ARP 解析 / 收到对端回复 |
| **STALE** | 条目超时，可能仍可用但未验证 | REACHABLE 超时（默认约 30-45 秒） |
| **DELAY** | 需要发数据了，但先等一小会儿 | STALE 状态下有流量要发给这个 IP |
| **PROBE** | 正在发单播探测确认 | DELAY 超时（约 5 秒）后仍未收到确认 |
| **FAILED** | 不可达 | PROBE 重试失败 |
| **PERMANENT** | 静态条目，永不超时 | 通过 `ip neigh add ... nud permanent` 添加 |

> [!warning] STALE 不是"坏"的状态
> STALE 只表示"有一段时间没确认了"。如果映射实际上仍是正确的，从 STALE 发数据包时走 DELAY → PROBE 流程，成功后会回到 REACHABLE，用户基本无感知。

### 超时参数调优

```bash
# 查看 ARP 相关超时参数
sysctl net.ipv4.neigh.default.gc_stale_time
# 默认值: 60 秒
# 含义: 从 REACHABLE 变为 STALE 的时间

sysctl net.ipv4.neigh.default.base_reachable_time
# 默认值: 30 秒
# 含义: REACHABLE 状态的基础超时时间

sysctl net.ipv4.neigh.default.retrans_time_ms
# 默认值: 1000 毫秒
# 含义: PROBE 状态的重试间隔
```

---

## `ip neigh show` 输出解读

`ip neigh` 是 iproute2 中管理邻居表的命令，替代旧的 `arp -a`。

### 基本用法

```bash
# 查看所有邻居条目
ip neigh show

# 输出示例
192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
192.168.1.5 dev eth0 lladdr 11:22:33:44:55:66 STALE
192.168.1.10 dev eth0 FAILED
fe80::1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
172.17.0.2 dev docker0 lladdr 02:42:ac:11:00:02 REACHABLE
```

### 输出字段解读

```
192.168.1.1        dev eth0        lladdr aa:bb:cc:dd:ee:ff      REACHABLE
└──── 邻居 IP      └── 所属网卡    └── 对端 MAC 地址             └── 状态
   (可含 IPv6)        (多个网卡时        (lladdr = link layer
                      区分接口)          address)
```

### 常用过滤

```bash
# 只看某个接口的邻居
ip neigh show dev eth0

# 只看 IPv6 邻居（NDP 条目）
ip neigh show dev eth0 | grep "inet6"   # 或
ip -6 neigh show

# 只查看 REACHABLE 状态的
ip neigh show | grep REACHABLE

# 只查看 FAILED 的（可能有问题的）
ip neigh show | grep FAILED

# JSON 输出（适合脚本解析）
ip -j neigh show
```

### 与旧命令对比

```bash
# 旧命令（net-tools）
arp -a            # 查看 ARP 表
arp -d 192.168.1.5  # 删除条目

# 新命令（iproute2）
ip neigh show     # 查看邻居表
ip neigh delete 192.168.1.5 dev eth0  # 删除条目
```

> [!note] `ip neigh` vs `arp`
> `ip neigh` 是内核 netlink 接口的直接封装，支持 **IPv4（ARP）和 IPv6（NDP）** 统一输出，而旧 `arp` 命令只支持 IPv4。在现代发行版上，始终使用 `ip neigh`。

---

## `ip neigh flush` 清除邻居表

当你怀疑邻居表中有过期或错误的条目时，清空后让内核重新解析是一种常用的排障手段。

### 清空所有条目

```bash
# 清空所有邻居条目
ip neigh flush all

# 输出示例
192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE removed
192.168.1.5 dev eth0 lladdr 11:22:33:44:55:66 STALE removed
192.168.1.10 dev eth0 FAILED removed
```

### 按条件过滤清除

```bash
# 只清空某个接口的
ip neigh flush dev eth0

# 只清空 NUD_FAILED 状态的
ip neigh flush nud failed

# 只清空指定 IP
ip neigh flush 192.168.1.5 to 192.168.1.5

# 组合条件
ip neigh flush dev eth0 nud stale
```

### flush 的典型使用场景

| 场景 | 操作 | 说明 |
|------|------|------|
| 网关 MAC 变更 | `ip neigh flush dev eth0` | 网关更换硬件后旧映射失效 |
| VM/容器迁移 | `ip neigh flush dev br0` | 迁移后 IP 未变但 MAC 变了 |
| 频繁出现 FAILED | `ip neigh flush nud failed` | 清理不可达条目避免表满 |
| 怀疑 ARP 缓存问题 | `ip neigh flush all` | 让所有条目重新解析 |

> [!tip] flush 后验证
> 清空后运行 `ping 192.168.1.1` 触发 ARP 重新解析，然后 `ip neigh show` 确认新条目是 REACHABLE。

### 静态添加条目

```bash
# 添加一个 PERMANENT（永不超时）的静态条目
ip neigh add 192.168.1.100 lladdr de:ad:be:ef:00:01 nud permanent dev eth0

# 添加一个 REACHABLE 条目（也会超时）
ip neigh add 192.168.1.200 lladdr de:ad:be:ef:00:02 nud reachable dev eth0

# 删除静态条目
ip neigh delete 192.168.1.100 dev eth0
```

> [!warning] 谨慎使用 PERMANENT
> 静态 MAC 绑定只在极少数场景下需要（如特定安全要求）。一旦对端硬件更换，你会收到 **IP 通但实际不通** 的诡异故障。多数场景下让内核自动管理即可。

---

## IPv6 NDP 取代 ARP

IPv6 中没有 ARP 协议，它的角色由 **NDP（Neighbor Discovery Protocol，邻居发现协议）** 替代。

### 核心差异

| 对比维度 | ARP（IPv4） | NDP（IPv6） |
|---------|-----------|-------------|
| **协议基础** | 独立的 ARP 协议（EtherType=0x0806） | 基于 ICMPv6（Type 135/136） |
| **传输方式** | 广播 (L2 broadcast) | 多播 (L2 multicast，不发到无关节点) |
| **安全性** | 无内置保护，易被 ARP 欺骗 | 支持 SEND（Secure Neighbor Discovery） |
| **地址解析** | ARP 请求/回复 | 邻居请求 NS / 邻居公告 NA |
| **其他功能** | 仅地址解析 | 还包括路由器发现、无状态地址自动配置(SLAAC)、重复地址检测(DAD) |
| **内核接口** | `ip neigh` 统一管理 | 同一张邻居表，`ip neigh` 同样适用 |

### NDP 的核心消息

```
NDP 邻居请求 (Neighbor Solicitation, ICMPv6 Type 135)
  ──→ 多播到目标节点的被请求节点多播地址
  ──→ "谁是 fe80::1234?"

NDP 邻居公告 (Neighbor Advertisement, ICMPv6 Type 136)
  ←── 单播回复
  ←── "fe80::1234 是我，我的 MAC 是 aa:bb:cc:dd:ee:ff"
```

```bash
# 查看 IPv6 邻居条目（和 IPv4 用同一个命令）
ip -6 neigh show

# 输出示例
fe80::1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
fe80::1234 dev eth0 lladdr 11:22:33:44:55:66 STALE
```

> [!note] 邻居表统一管理
> 在 Linux 内核层面，ARP（IPv4）和 NDP（IPv6）的解析结果存在 **同一张邻居表** 中。`ip neigh show` 不区分协议，IPv4 和 IPv6 条目并排输出。用 `ip -4 neigh show` 只看 IPv4，`ip -6 neigh show` 只看 IPv6。

---

## ARP 表溢出与 `gc_thresh` 排障

### 问题现象

在较大规模的二层网络（如 Kubernetes 集群节点数较多、DHCP 子网很大）或频繁建立/断开连接的场景下，ARP 表可能会占满。占满后的典型症状：

- 内核日志出现 `neighbour: arp_cache: neighbor table overflow!`
- 新的 AP R解析失败，导致 `ping` 通但对端连接异常
- `dmesg | tail` 能看到相关警告

### 三个关键参数

内核用三个参数控制 ARP 表的垃圾回收（GC）：

```bash
sysctl net.ipv4.neigh.default.gc_thresh1   # 软下限（默认 128）
sysctl net.ipv4.neigh.default.gc_thresh2   # 软上限（默认 512）
sysctl net.ipv4.neigh.default.gc_thresh3   # 硬上限（默认 1024）
```

| 参数 | 作用 | 行为 |
|------|------|------|
| `gc_thresh1` | 最小保留数 | 条目少于这个数时，GC 不会主动回收 |
| `gc_thresh2` | 软上限 | 超过这个数时，GC 开始尝试回收 **STALE** 条目 |
| `gc_thresh3` | 硬上限 | 超过这个数时，直接拒绝新条目（开始丢包） |

### 排查步骤

```bash
# 1. 查看当前邻居表大小
ip neigh show | wc -l

# 2. 查看当前 GC 参数
sysctl net.ipv4.neigh.default.gc_thresh1
sysctl net.ipv4.neigh.default.gc_thresh2
sysctl net.ipv4.neigh.default.gc_thresh3

# 3. 检查内核日志是否有溢出警告
dmesg | grep -i "neighbor table overflow"

# 4. 看 FAILED 条目是否过多
ip neigh show | grep FAILED | wc -l
```

### 定位原因

ARP 表溢出通常有以下原因：

1. **子网过大**（如 `/16` 甚至 `/8` 的子网），ARP 条目远多于 `gc_thresh3`
2. **外部扫描**，IP 扫描工具发出大量请求，产生大量 FAILED 条目
3. **容器/VM 频繁创建销毁**，IP 不断变化，旧的 STALE/FALED 条目堆积
4. **网络设备故障**，某些 IP 反复可达/不可达，导致状态频繁切换

### 临时修复

```bash
# 调大 gc_thresh（临时生效，重启后恢复）
sysctl -w net.ipv4.neigh.default.gc_thresh1=512
sysctl -w net.ipv4.neigh.default.gc_thresh2=2048
sysctl -w net.ipv4.neigh.default.gc_thresh3=4096

# 清空 FAILED 条目释放空间
ip neigh flush nud failed
```

### 持久化配置

```bash
# 写入 /etc/sysctl.conf 或 /etc/sysctl.d/99-arp.conf
cat >> /etc/sysctl.d/99-arp.conf << 'EOF'
# ARP 表 GC 参数调优（适用于大二层网络）
net.ipv4.neigh.default.gc_thresh1 = 512
net.ipv4.neigh.default.gc_thresh2 = 2048
net.ipv4.neigh.default.gc_thresh3 = 4096
EOF

# 立即生效
sysctl -p /etc/sysctl.d/99-arp.conf
```

> [!warning] gc_thresh3 不是越多越好
> 每个邻居条目约占用 256 字节内核内存。设置过大（如十几万）会消耗大量内核内存。根据实际需要设置，Kubernetes 集群建议设为节点数的 2-3 倍。

---

## 本章小结

- **ARP 协议** 通过广播请求 / 单播回复，将 IP 地址解析为 MAC 地址，**只在同一广播域内工作**
- **邻居状态机** 是理解 ARP 缓存行为的关键：REACHABLE（最近确认）→ STALE（超时）→ DELAY（等待）→ PROBE（探测）→ FAILED（失败），PERMANENT 是静态绑定
- `ip neigh show` 是查看邻居表的标准命令，支持 `-j` JSON 输出和按接口/状态过滤，**统一管理 IPv4（ARP）和 IPv6（NDP）**
- `ip neigh flush` 清空邻居表是常见排障手段，可配合过滤条件定向清除
- **IPv6 用 NDP 替代 ARP**，基于 ICMPv6 多播，更高效安全，但内核使用同一张邻居表管理
- **ARP 表溢出** 由 `gc_thresh1/2/3` 控制，超过硬上限会导致内核丢包，可根据子网规模适当调大
- 排查 ARP 问题的基本思路：`ip neigh show | wc -l` → `dmesg | grep "neighbor table overflow"` → 定位原因 → `ip neigh flush nud failed` → 调整 `gc_thresh`

### 下章预告

下一章我们将从数据链路层（L2）跃升到传输层（L4），学习 **Socket 连接与传输层信息**。你会看到如何用 `ss` 替代 `netstat` 查看 TCP/UDP 连接状态、解读 Recv-Q/Send-Q 的含义，以及如何通过 TCP 状态机诊断连接问题。

---

*章节编号：06 | 计划篇幅：短 | 代码示例：有*
