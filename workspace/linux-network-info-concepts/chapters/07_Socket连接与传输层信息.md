# Socket 连接与传输层信息

前六章我们从链路层一路走到网络层，看过了 MAC 地址、IP 地址、路由表和邻居表。现在终于到达传输层——所有网络通信的"最后一公里"交付环节。本章的核心问题是：**操作系统如何管理成千上万的网络连接？怎样快速查看端口监听情况、定位连接异常？**

---

## TCP/UDP 协议概念速览

在动手敲命令之前，先搞清传输层两个主角：TCP 和 UDP。它们共享同一个底层网络（IP），但交付方式完全不同。

### 协议头部结构

```
TCP 头部（最少 20 字节）：
┌─────────────────────────────────────────────────────────────┐
│     源端口 (16 bit)        │      目标端口 (16 bit)         │
├─────────────────────────────────────────────────────────────┤
│                    序列号 Sequence Number (32 bit)           │
├─────────────────────────────────────────────────────────────┤
│                  确认号 Acknowledgment Number (32 bit)       │
├────────┬────────┬─────────┬────────┬───────────┬────────────┤
│ 数据偏移 │ 保留  │ 标志位  │  窗口大小 (16 bit)             │
│ (4 bit) │(3 bit)│ (9 bit) │                                │
├────────┴────────┴─────────┼────────┬───────────────────────┤
│  校验和 (16 bit)          │  紧急指针 (16 bit)              │
├───────────────────────────┴────────────────────────────────┤
│                    选项（可选，0-40 字节）                   │
│                     填充至 32 位对齐                        │
└─────────────────────────────────────────────────────────────┘

UDP 头部（固定 8 字节）：
┌─────────────────────────────────────────────────────────────┐
│     源端口 (16 bit)        │      目标端口 (16 bit)         │
├─────────────────────────────────────────────────────────────┤
│       长度 (16 bit)        │       校验和 (16 bit)          │
└─────────────────────────────────────────────────────────────┘
```

> [!note] TCP vs UDP 核心区别
> - **TCP**：面向连接、可靠、有序——适合网页浏览、文件传输、邮件
> - **UDP**：无连接、尽力交付——适合 DNS 查询、视频流、游戏
> - 直观理解：TCP 像挂号信（有回执、按顺序到达），UDP 像明信片（丢了不补发）

| 特性 | TCP | UDP |
|------|-----|-----|
| 头部大小 | 20-60 字节 | 8 字节（固定） |
| 连接建立 | 三次握手 | 无需握手 |
| 可靠性 | 确认重传 | 无确认 |
| 顺序保证 | 序列号排序 | 不保证顺序 |
| 流量控制 | 滑动窗口 | 无 |
| 拥塞控制 | 有（cwnd/ssthresh） | 无 |
| 适用场景 | HTTP/HTTPS/SSH/FTP | DNS/DHCP/视频流/VPN |

### TCP 标志位

TCP 标志位是理解连接状态的钥匙，`ss` 和 `tcpdump` 的输出中会频繁出现：

| 标志 | 全称 | 含义 |
|------|------|------|
| SYN | Synchronize | 发起连接请求 |
| ACK | Acknowledgment | 确认收到数据 |
| FIN | Finish | 结束发送 |
| RST | Reset | 强制断开 |
| PSH | Push | 立即推送 |
| URG | Urgent | 紧急指针 |

---

## TCP 状态机

TCP 是一个**有状态**的协议。每个连接在其生命周期中会经历多个状态。理解这些状态是阅读 `ss` 输出和排查连接问题的前提。

### 标准 TCP 状态流转

```
          ┌──────────────────────────────────┐
          │              CLOSED              │
          └──────────────────────────────────┘
                      │
                 (主动打开)
                      │
                      ▼
          ┌──────────────────────────────────┐
          │            SYN-SENT              │◄──── 客户端发起连接
          └──────────────────────────────────┘
                      │
              (收到 SYN+ACK)
                      │         ┌───────────────────────┐
                      ▼         │     LISTEN             │◄── 服务端等待连接
          ┌──────────────────┐   └───────────────────────┘
          │   ESTABLISHED    │◄──────── (收到 SYN)
          └──────────────────┘          │
               │         │              │
          (主动关闭)   (被动关闭)       (发起 SYN+ACK)
               │         │              │
               ▼         │              ▼
     ┌─────────────┐     │    ┌───────────────────┐
     │  FIN-WAIT-1 │     │    │   SYN-RECEIVED    │
     └─────────────┘     │    └───────────────────┘
           │             │              │
     (收到 ACK)    (收到 FIN)     (收到 ACK)
           │             │              │
           ▼             ▼              ▼
     ┌─────────────┐ ┌───────────┐ ┌─────────────┐
     │  FIN-WAIT-2 │ │CLOSE-WAIT │ │ ESTABLISHED  │
     └─────────────┘ └───────────┘ └─────────────┘
           │             │
     (收到 FIN)    (发起 FIN)
           │             │
           ▼             ▼
     ┌─────────────┐ ┌───────────┐
     │  TIME-WAIT  │ │ LAST-ACK  │
     └─────────────┘ └───────────┘
           │             │
       (2MSL 后)   (收到 ACK)
           │             │
           ▼             ▼
          ┌──────────────────────────────────┐
          │              CLOSED              │
          └──────────────────────────────────┘
```

### 关键状态解读

| 状态 | 含义 | 排障关注点 |
|------|------|-----------|
| **LISTEN** | 服务端正在监听端口，等待连接 | 正常。可用 `ss -tulnp` 确认服务是否启动 |
| **ESTABLISHED** | 连接已建立，数据在传输 | 正常。数量异常多可能说明有问题 |
| **TIME-WAIT** | 主动关闭方等待（2MSL，约 60s） | 大量 TIME-WAIT 可能耗尽端口资源 |
| **CLOSE-WAIT** | 被动关闭方等待应用调用 `close()` | **应警惕**——说明应用有 bug，未正确关闭 Socket，会导致句柄泄漏 |
| **FIN-WAIT-2** | 主动关闭方已收到对端的 FIN ACK | 大量 FIN-WAIT-2 可能说明对端未正常关闭 |
| **SYN-RECV** | 收到 SYN 但未完成三次握手 | 大量 SYN-RECV 可能是 SYN Flood 攻击 |
| **CLOSING** | 双方同时发起关闭 | 罕见，通常很快消失 |

> [!warning] CLOSE-WAIT 泄漏是最常见的排障场景
> 当服务端发现大量 CLOSE-WAIT 状态的连接（用 `ss -tanp \| grep CLOSE-WAIT`），几乎可以断定是应用程序没有正确关闭 Socket。这不是网络问题，是代码问题。
>
> 类似场景在排障中很常见——`ss` 查出的状态直接告诉你"问题在哪一层"。

### 连接数限制的内核参数

```bash
# 查看最大文件句柄数（直接影响连接上限）
cat /proc/sys/fs/file-max

# 查看临时端口范围（客户端连接用）
cat /proc/sys/net/ipv4/ip_local_port_range
# 典型输出：32768 60999

# TIME-WAIT 复用（高并发场景建议开启）
sysctl net.ipv4.tcp_tw_reuse
# 注意：Linux 4.12+ 已移除 tcp_tw_recycle 参数
```

---

## Socket 与连接五元组

### 什么是 Socket

Socket（套接字）是操作系统提供的一个**抽象接口**，应用通过它进行网络通信。在 Linux 中，一切皆文件——Socket 也是一种文件描述符。

一个 Socket 包含两个要素：**IP 地址 + 端口号**。

```bash
# 查看进程打开的文件描述符（含 Socket）
ls -la /proc/<PID>/fd/ | grep socket
# 输出示例：
# lrwx------ 1 root root 64 Jul 29 10:00 3 -> 'socket:[12345]'

# 查看系统级 Socket inode 信息
cat /proc/net/tcp | head -5
```

### 连接五元组

一个完整的 TCP 连接由**五个元素**唯一标识：

```
(源 IP, 源端口, 目标 IP, 目标端口, 传输层协议)
```

```bash
ss -tanp | head -5
# 输出示例：
# STATE      RECV-Q SEND-Q  LOCAL ADDRESS:PORT     PEER ADDRESS:PORT    PROCESS
# LISTEN     0      128     0.0.0.0:22             0.0.0.0:*            users:(("sshd",pid=1234,fd=3))
# ESTAB      0      0       192.168.1.100:22       10.0.0.5:54321       users:(("sshd",pid=5678,fd=4))
```

每一行就是一个五元组实例。五元组的任何一项不同，就是不同的连接。

> [!tip] 为什么五元组很重要
> - **端口冲突**：同一 IP 上不能有两个服务监听相同端口（五元组中的"目标端口"冲突）
> - **连接数上限**：客户端的五元组中"源端口"受 `ip_local_port_range` 限制，约 28,000 个
> - **NAT 映射**：路由器通过五元组区分内网多个设备共享同一公网 IP 的流量

---

## `ss` 命令详解

`ss` 是 Socket Statistics 的缩写，它通过 **netlink** 直连内核读取 Socket 信息，比传统 `netstat` 快 10-100 倍。以下是它的各类用法。

### 查看监听端口：`ss -tulnp`

这是最常用的 `ss` 命令组合，用于查看当前机器在**监听**哪些端口。

```bash
# -t: TCP  -u: UDP  -l: listening（仅显示监听状态）
# -n: 不解析服务名（显示端口号而不是 http/ssh）  -p: 显示对应的进程
ss -tulnp
```

**输出示例**：
```
Netid  State   Recv-Q  Send-Q  Local Address:Port     Peer Address:Port   Process
tcp    LISTEN  0       128     0.0.0.0:22             0.0.0.0:*           users:(("sshd",pid=1234,fd=3))
tcp    LISTEN  0       128     [::]:22                [::]:*              users:(("sshd",pid=1234,fd=4))
tcp    LISTEN  0       511     0.0.0.0:80             0.0.0.0:*           users:(("nginx",pid=5678,fd=6))
udp    LISTEN  0       0       127.0.0.53:53          0.0.0.0:*           users:(("systemd-resolve",pid=987,fd=12))
```

输出解读：
- **Netid**：协议类型（tcp/udp）
- **State**：仅监听端口有 LISTEN 状态
- **Local Address:Port**：绑定地址和端口
  - `0.0.0.0:80` 表示监听所有 IPv4 接口的 80 端口
  - `127.0.0.53:53` 表示仅监听本机 loopback，外部不可访问
  - `[::]:22` 表示监听所有 IPv6 接口（通常同时覆盖 IPv4）
- **Process**：哪个进程在监听（PID 和进程名）

> [!tip] 端口占用的终极确认
> 当你启动某个服务提示"Address already in use"时，用 `ss -tulnp | grep :<端口号>` 一秒定位是哪个进程占用了端口。

### 查看所有连接：`ss -tanp`

```bash
# -a: all（显示所有状态，不仅仅是 LISTEN）
ss -tanp
```

**输出示例**：
```
STATE      RECV-Q  SEND-Q  LOCAL ADDRESS:PORT     PEER ADDRESS:PORT        Process
LISTEN     0       128     0.0.0.0:22             0.0.0.0:*                users:(("sshd",pid=1234,fd=3))
ESTAB      0       0       192.168.1.100:22       10.0.0.5:54321           users:(("sshd",pid=5678,fd=4))
ESTAB      0       0       192.168.1.100:22       10.0.0.5:54322           users:(("sshd",pid=5679,fd=4))
TIME-WAIT  0       0       192.168.1.100:34567    93.184.216.34:443        -
```

这里可以看到 TCP 状态机中的各种实际状态。注意 TIME-WAIT 状态的行没有 `users:` 信息，因为该连接已经不再关联任何进程（等待 2MSL 超时后自动释放）。

### 连接统计总览：`ss -s`

```bash
ss -s
```

**输出示例**：
```
Total: 298 (kernel 398)
TCP:   18 (estab 4, closed 9, orphaned 0, synrecv 0, timewait 3/0), ports 12

Transport Total     IP        IPv6
*          398       -         -
RAW        1         1         0
UDP        6         5         1
TCP        9         6         3
INET       16        12        4
FRAG       0         0         0
```

关键字段解读：
- **Total**：当前打开的 Socket 总数
- **estab**：已建立连接数（正常通信中）
- **timewait**：TIME-WAIT 状态的连接数
- **orphaned**：孤儿连接（不再关联任何进程，通常是有问题的连接）

> [!tip] 快速判断系统负载
> 如果 `estab` 远低于正常水平但应用报错，或 `timewait` 数量异常增长（超过几万），说明连接回收出了问题。

### TCP 内部参数：`ss -i`

`ss -i` 是排查 TCP 性能问题的利器，它能显示每个 TCP 连接的**内核内部状态参数**。

```bash
# 查看所有 ESTABLISHED 连接的内部参数
ss -t -i state established
```

**输出示例**：
```
ESTAB    0    0    192.168.1.100:22    10.0.0.5:54321
         cubic wscale:7,8 rto:204 rtt:12.5/4.5 ato:40 mss:1460 pmtu:1500
         rcvmss:536 advmss:1448 cwnd:10 ssthresh:7 bytes_sent:12345
         bytes_retrans:0 bytes_acked:12345 segs_out:12 segs_in:10
         send 130.4Mbps lastsnd:2 lastrcv:2 lastack:2 pacing_rate 260.8Mbps
         rcv_space:14600 rcv_ssthresh:64088
```

参数解读（这是排查 TCP 性能问题的核心信息）：

| 参数 | 含义 | 排障用途 |
|------|------|---------|
| **rtt** | 往返延迟（平均/均方差），单位 ms | 判断网络延迟是否正常 |
| **rto** | 超时重传时间，单位 ms | RTO 过大说明丢包严重 |
| **cwnd** | 拥塞窗口，单位段数 | 影响吞吐量的核心参数 |
| **ssthresh** | 慢启动阈值 | 丢包后大幅降低 |
| **mss** | 最大段大小（MTU - 40） | 如果小于 1460 可能有 PMTU 问题 |
| **pmtu** | 路径 MTU | 端到端最大传输单元 |
| **bytes_retrans** | 重传字节数 | **>0 说明有丢包** |
| **send** | 估算发送速率，单位 bps | 实际可用带宽 |
| **pacing_rate** | 内核 pacing 速率 | TCP BBR 等拥塞控制算法控制 |

```bash
# 实时监控某连接的 RTT 变化（结合 watch）
watch -n 1 'ss -t -i state established | grep -A1 "192.168.1.100:22"'
```

> [!warning] bytes_retrans > 0 意味着什么
> 当 `ss -i` 输出中 `bytes_retrans` 不为 0，说明 TCP 层发生了重传。这可能是网络拥塞、链路不稳定，也可能是对端性能瓶颈。如果重传率超过 1%，需要进一步排查。

---

## 状态过滤与端口过滤

`ss` 支持灵活的状态过滤和表达式过滤，远超 `netstat` 的能力。

### 按状态过滤

```bash
# 列出所有处于 TIME-WAIT 状态的连接
ss state time-wait

# 同时匹配多个状态
ss state established state time-wait

# 组合协议 + 状态
ss -t state time-wait           # 仅 TCP 的 TIME-WAIT
ss -u state established         # 仅 UDP 的 "已建立"（UDP 无状态，但实际上有记录）

# 状态取反（排除）
ss -t state all state -time-wait   # 除了 TIME-WAIT 之外的所有 TCP 状态
```

`ss` 支持的内置状态名（在 `tcp` 状态下可用）：

```
established, syn-sent, syn-recv, fin-wait-1, fin-wait-2, time-wait,
closed, close-wait, last-ack, listening, closing
```

另外还有一个便捷缩写：
```bash
ss -t state connected           # 所有非 LISTEN 非 CLOSED 的已连接状态
ss -t state synchronized        # 完成三次握手的连接（不含 SYN-SENT/SYN-RECV）
ss -t state bucket              # TIME-WAIT 和 SYN-RECV（mini socket 优化）
```

### 按端口过滤

```bash
# 方式一：语法糖匹配（ss 原生表达式）
ss sport = :80                   # 源端口是 80
ss dport = :443                  # 目标端口是 443
ss sport = :80 or dport = :80    # 源或目标端口是 80

# 方式二：grep 过滤（更灵活）
ss -tanp | grep ':80 '

# 方式三：端口范围
ss -tanp sport > :1024           # 源端口大于 1024
ss -tanp sport \< :1024          # 源端口小于 1024（需转义 <）

# 端口区间
ss -tanp '( sport >= :8000 and sport <= :8999 )'
```

### 按 IP 过滤

```bash
# 匹配特定 IP
ss -tanp src 192.168.1.100       # 源 IP
ss -tanp dst 10.0.0.5            # 目标 IP

# 匹配子网
ss -tanp src 192.168.1.0/24      # 源子网

# 组合过滤——等价的复杂表达式
ss -tanp '( src 192.168.1.100 and dport = :443 )'
```

### 实用排障组合

```bash
# 场景 1：确认 8080 端口是否被占用
ss -tulnp | grep ':8080'

# 场景 2：查看某 IP 与当前机器的所有连接
ss -tanp dst 10.0.0.5

# 场景 3：查看所有 CLOSE-WAIT（排查连接泄漏）
ss -tanp state close-wait

# 场景 4：查看 MySQL 端口的所有 ESTABLISHED 连接
ss -tanp state established dport = :3306

# 场景 5：查看高延迟连接（需要 shell 脚本辅助）
ss -t -i state established | grep -B1 "rtt:.*/.*>"  # 匹配 RTT 中高延迟
```

---

## Recv-Q / Send-Q 排障

`Recv-Q` 和 `Send-Q` 是 `ss` 输出中的两个关键数值，代表 Socket 缓冲区中的数据积压情况。它们是判断应用处理能力是否跟得上的重要指标。

### 含义

```
ss -tanp | head -3
STATE      RECV-Q  SEND-Q  LOCAL:PORT     PEER:PORT
LISTEN     0       128     0.0.0.0:22     0.0.0.0:*
ESTAB      500     0       192.168.1.100:22  10.0.0.5:54321
```

- **Recv-Q**（接收队列）：
  - **LISTEN 状态下**：已完成三次握手但未被 `accept()` 的连接数（backlog 积压）
  - **ESTABLISHED 状态下**：内核已收到但对端应用尚未读取的数据字节数
- **Send-Q**（发送队列）：
  - **LISTEN 状态下**：backlog 最大值（是配置值，不是积压数）
  - **ESTABLISHED 状态下**：应用已写入但内核尚未发往对端的数据字节数

> [!note] LISTEN 状态的 Send-Q 含义
> 当看到 LISTEN 状态的 Send-Q 不为 0 时，请区分：
> - 对于 LISTEN 状态，Send-Q = `somaxconn`（内核 backlog 上限，默认 4096 或 128），**这是最大值，不是当前积压数**
> - Recv-Q 才是真正的积压连接数

### 排障场景

```bash
# 场景 1：Listen backlog 溢出
# 现象：Recv-Q > 0，说明有连接排队等待 accept()
ss -t state listening

# 如果 Recv-Q 持续增大并接近 Send-Q，说明应用 accept() 速度跟不上
# 解决方案：
# 1. 优化应用（使用线程池、异步 IO）
# 2. 增大 backlog：修改应用配置（如 nginx 的 listen backlog=1024）
# 3. 增大内核限制：sysctl -w net.core.somaxconn=4096

# 场景 2：数据接收延迟
# 现象：Recv-Q 持续增长（ESTABLISHED 状态）
# 说明：应用读取 Socket 数据太慢，内核缓冲区堆积
# 解决方法：优化应用的数据读取逻辑

# 场景 3：数据发送阻塞
# 现象：Send-Q 持续增长
# 说明：对端读取太慢、网络拥塞、或者对端窗口已满
# 解决方法：检查对端应用、检查网络带宽延迟
```

**真实事故案例**：
```
# 某 Web 服务器突然响应变慢
$ ss -tanp | head -10
LISTEN     4095   128   0.0.0.0:80      0.0.0.0:*
ESTAB      0      0     ...             ...
ESTAB      0      0     ...             ...
ESTAB      5000   0     ...             ...

# Recv-Q 在 LISTEN 状态上高达 4095，接近 Send-Q=128？！
# 不对！LISTEN 状态的 Send-Q=128 是 max backlog
# 4095 是积压连接数，远超应用的 accept() 处理能力
```

> [!warning] Recv-Q / Send-Q 解读口诀
> - **LISTEN 状态**：Recv-Q = 当前积压 Send-Q = 最大 backlog
> - **ESTABLISHED 状态**：Recv-Q = 应用还没读 Send-Q = 对端还没收
> - **两边都大**：大概率是网络瓶颈
> - **仅 Recv-Q 大**：应用处理慢
> - **仅 Send-Q 大**：对端处理慢或网络拥堵

---

## `ss` vs `netstat` 性能对比

虽然大部分发行版仍保留 `netstat`，但在生产环境（特别是高并发服务器）上，两者的性能差距非常明显。

### 速度对比

| 测试场景 | `ss` | `netstat` | 倍数 |
|---------|------|-----------|------|
| 10 个连接 | < 0.01s | < 0.02s | ~2x |
| 1,000 个连接 | 0.02s | 0.15s | ~7x |
| 10,000 个连接 | 0.10s | 2.3s | ~23x |
| 100,000 个连接 | 0.45s | 30+s | ~70x |
| 500,000 个连接 | 2.1s | 超时/不可用 | >100x |

> 数据来源：基于常见云服务器测试，不同内核版本略有差异 [SS Network Troubleshooting Guide](https://github.com/ryzendev/Linux-Tips-and-Tricks/wiki/SS-Network-Troubleshooting)

### 为什么 `ss` 更快

关键在于底层数据读取方式的不同：

```
ss 数据流（netlink 直连内核）：
应用 ss → netlink socket → 内核 diag 模块 → Socket 数据
           ↓
      无需上下文切换，直接读取内核内存

netstat 数据流（读取 /proc 文件系统）：
应用 netstat → 读取 /proc/net/tcp → 内核遍历 Socket 表 → 格式化写入文件
                                                              ↓
              netstat 重新解析文本 → 读取下一次 /proc/net/udp → ...
           ↓
      每次读取涉及多次系统调用 + 文本格式化 + 文本解析
```

### 命令互换表

| 查询目标 | `netstat` | `ss` |
|---------|-----------|------|
| 监听端口 | `netstat -tulnp` | `ss -tulnp` |
| 所有连接 | `netstat -tanp` | `ss -tanp` |
| 统计总览 | `netstat -s` | `ss -s` |
| 按状态过滤 | 需 grep | `ss state established` |
| 按端口过滤 | 需 grep | `ss dport = :80` |
| TCP 内部参数 | 不支持 | `ss -t -i` |
| 进程信息 | `-p` 参数 | `-p` 参数 |

> [!warning] 生产环境建议
> 在有大量连接（>5000）的服务器上，**永远不要用 `netstat`**。`ss` 不仅快 10-100 倍，而且输出格式更一致、更易于脚本解析。当你 SSH 到一台高负载服务器时，`netstat` 可能会花费几十秒甚至几分钟，而 `ss` 几乎瞬间返回结果。
>
> 注意：在容器环境中（如 Docker），`netstat` 可能依赖的 `/proc` 文件系统被部分隔离，导致输出不完整或错误。`ss` 通过 netlink 接口不受此影响，在容器内的行为与宿主机一致。

---

## 本章小结

- **TCP 是有状态的协议**，理解状态机（特别是 LISTEN、ESTABLISHED、TIME-WAIT、CLOSE-WAIT）是排查连接问题的基本功
- **连接五元组**是本层核心概念，任何一项不同就是不同连接，理解五元组才能理解端口冲突、连接数上限、NAT 映射等问题
- **`ss -tulnp`** 是最常用的端口监听查询命令，`ss -tanp` 查看所有连接状态
- **`ss -i`** 可以查看 TCP 内部参数（RTT、cwnd、重传字节数等），是排查 TCP 性能问题的利器
- **Recv-Q / Send-Q** 是 Socket 缓冲区的积压指标：LISTEN 状态看 backlog 溢出，ESTABLISHED 状态看应用处理速度
- **`ss` 比 `netstat` 快 10-100 倍**，在高并发环境下务必使用 `ss`

### 下章预告

下一章我们将 Wi-Fi 上空——**无线网络信息**。你会学到如何用 `iw` 和 `nmcli` 查看无线连接状态、信号强度和扫描附近的 AP，以及新旧无线工具的区别。

---

*章节编号：07 | 计划篇幅：中 | 实际篇幅：含多个代码示例和概念图示*
