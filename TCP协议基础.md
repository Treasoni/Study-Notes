---
title: "TCP 协议基础：从心智模型到动手排查"
tags: [tcp, 网络协议, 传输层, 计算机网络]
created: 2026-08-12
updated: 2026-08-12
status: completed
source_project: tcp-protocol
---

# TCP 协议基础：从心智模型到动手排查

> [!summary] 笔记简介
> 从分层模型出发，建立 TCP 的心智模型；逐步深入报文头、连接管理、可靠传输三大核心，再用工具链实操与高频问题排查落地，最后沉淀速查表与进阶路线。适合有基础了解、想"上手"的读者。

## 目录

- **第一章** 站在协议栈看 TCP——分层模型与寻址
- **第二章** 读懂 TCP 报文头
- **第三章** 连接管理——三次握手、四次挥手与状态机
- **第四章** 可靠传输——确认、窗口与拥塞控制
- **第五章** 工具链实操——抓包与连接状态观察
- **第六章** 高频连接异常排查
- **第七章** 关键数值速查与进阶路线

---
## 第一章：站在协议栈看 TCP——分层模型与寻址

> [!note] 本章目标
> 建立 TCP/IP 分层的心智模型，说清 TCP 在协议栈中的位置、它靠什么机制被"送达"正确的应用，以及它和 UDP 的本质区别。

### 四层模型与 OSI 对应

TCP/IP 是事实上的互联网协议族，通常描述为**四层模型**：

| 层级 | 职责 | 代表协议 |
|------|------|----------|
| 应用层 | 面向用户的应用协议 | HTTP、DNS、FTP、SSH |
| 传输层 | 进程到进程的通信、可靠/不可靠 | **TCP**、UDP |
| 网络层 | 主机到主机的寻址与路由 | IP、ICMP |
| 链路层 | 同一物理链路内的帧传输 | 以太网、ARP |

它和教科书上的 OSI 七层模型并非一一对应，而是把 OSI 的高三层合并为"应用层"、把低两层合并为"链路层"：

```
OSI 七层                TCP/IP 四层
应用层 ─┐
表示层 ─┤ →  应用层
会话层 ─┘
传输层      →  传输层   ← TCP 在这里
网络层      →  网络层
数据链路层 ─┐
物理层   ──┘ →  链路层
```

> [!tip] 为什么先看分层？
> 所有网络排障的第一步都是"先定位问题出在哪一层"。建立了分层地图，你才知道抓包该看 TCP 字段、看 IP 地址还是看链路帧。

### 三大寻址：IP、MAC、端口

一次通信要成功，需要三层寻址协同工作：

| 寻址 | 所在层 | 定位对象 | 典型形态 |
|------|--------|----------|----------|
| IP 地址 | 网络层 | 哪台**主机** | 32 位点分十进制，如 192.168.1.5 |
| MAC 地址 | 链路层 | 哪块**网卡** | 48 位，如 00:1a:2b:3c:4d:5e |
| 端口号 | 传输层 | 主机上哪个**进程** | 0~65535，知名端口 0~1023 |

- **IP 地址**解决"数据包去哪台机器"。
- **端口号**解决"到机器后交给哪个进程"——这正是 TCP 所在传输层的核心价值。
- **MAC 地址**解决"下一跳的物理网卡是谁"，在局域网内逐跳转发。

三者配合的关系：IP 负责跨网络路由，MAC 负责本地链路转发，端口负责最终的应用分发。

### 封装与解封装

发送方从上层往下逐层**封装**（加头），接收方从下往上逐层**解封装**（剥头）：

```
应用数据
  ↓ 应用层加工
[应用数据]
  ↓ TCP 加传输头（源/目的端口、序号、校验和...）
[TCP 头 | 应用数据]
  ↓ IP 加网络头（源/目的 IP）
[IP 头 | TCP 头 | 应用数据]
  ↓ 链路层加帧头/帧尾
[帧头 | IP 头 | TCP 头 | 应用数据 | 帧尾]
```

对 TCP 而言，它看到的是"应用字节流"，而它自己则作为载荷被 IP 封装。

### TCP vs UDP

同属传输层，两者哲学截然不同：

| 维度 | TCP | UDP |
|------|-----|-----|
| 连接 | 面向连接（需三次握手） | 无连接 |
| 可靠性 | 可靠（确认、重传） | 尽力而为（可能丢包） |
| 数据边界 | 字节流 | 报文（保留边界） |
| 典型场景 | HTTP、SSH、文件传输 | DNS、音视频、游戏 |

> [!summary] 本章小结
> - TCP/IP 四层模型把 OSI 七层压缩为应用/传输/网络/链路四层，TCP 位于**传输层**。
> - 通信需要三层寻址协同：**IP 定位主机、MAC 定位网卡、端口定位进程**。
> - 数据发送经过逐层封装、接收经过逐层解封装。
> - TCP 是**面向连接、可靠、字节流**的协议，与 UDP 形成鲜明对比。
> - 掌握分层心智模型后，下一步是读懂 TCP 自己的"信封"——报文头。
## 第二章：读懂 TCP 报文头

> [!note] 本章目标
> 能对着一次真实抓包，逐字段读懂 TCP 首部。这一章是为第 3、5 章的握手观察打基础。

### 首部总体结构

TCP 首部**固定 20 字节**，通过"数据偏移"字段可扩展到最大 **60 字节**（选项最多 40 字节）：

- 数据偏移（4 位）以 32 位字为单位：`数据偏移 × 4 = 首部字节数`，最大 `15 × 4 = 60`。
- 校验和计算时，TCP 报文段前会拼接一个 **12 字节的伪首部**（含源/目的 IP、协议号、TCP 长度），用于交叉校验 IP 层信息。

### 核心字段逐项

| 字段 | 位数 | 作用 |
|------|------|------|
| 源端口 | 16 | 发送方进程 |
| 目的端口 | 16 | 接收方进程 |
| 序号（Seq） | 32 | 本报文段**第一个数据字节**的序号 |
| 确认号（Ack） | 32 | 期望收到的**下一个字节**序号（仅 ACK=1 时有效） |
| 数据偏移 | 4 | 首部长度（单位 4 字节） |
| 保留 | 6 | 置 0 |
| URG / ACK / PSH / RST / SYN / FIN | 各 1 | 六个控制标志位 |
| 窗口（Window） | 16 | 接收窗口大小，用于流量控制 |
| 校验和 | 16 | 首部+数据（含伪首部）的校验 |
| 紧急指针 | 16 | 仅 URG=1 时有效 |
| 选项 | 可变 | MSS、SACK、时间戳、窗口扩大因子 |

> [!note] 六个标志位的含义
> - **SYN**：连接请求/接受（握手）。
> - **ACK**：确认号有效。
> - **FIN**：发送端数据已发完，请求释放连接。
> - **RST**：连接出错，强制复位。
> - **PSH**：接收方尽快交付应用层。
> - **URG**：紧急指针有效。
>
> 现代实现另有 **CWR**、**ECE**（显式拥塞通知 ECN）两个标志位，共 8 个控制位。

### 选项字段

首部的"可扩展空间"用于协商连接参数：

- **MSS**（最大报文段长度）：数据字段最大长度，握手时协商。
- **SACK**（选择性确认）：允许只重传丢失的片段，而非全部重传。
- **时间戳**：精确测 RTT、防序号回绕混淆，也是 `tcp_tw_reuse` 生效的前提。
- **窗口扩大因子**：把 16 位窗口放大，突破 65,535 字节上限。

### 序号与确认号语义

理解 TCP 可靠性的钥匙在于**按字节编号**：

- 每个数据字节都有唯一序号；`Seq` 表示本段**第一个数据字节**的序号。
- `Ack` 表示"**下一个期待接收的字节序号**"（累计确认）。
- **SYN 与 FIN 各占一个序号位置**：SYN 占用序号 X，其后第一个数据字节为 X+1；FIN 同理。
- 纯 ACK（无数据）**不消耗序号空间**。

> [!tip] 验证方法
> 抓包时校验：握手第 2 包的 `Ack = 第 1 包 Seq + 1`；第 3 包的 `Ack = 第 2 包 Seq + 1`。这正是"SYN 占一个序号"的直接证据。

> [!summary] 本章小结
> - TCP 首部固定 **20 字节**，可扩展至 60 字节；六个核心标志位控制连接与数据语义。
> - 序号/确认号按**字节**编号，累计确认，SYN/FIN 各占一个序号。
> - 选项字段（MSS、SACK、时间戳、窗口扩大）在握手时协商连接参数。
> - 读懂报文头后，就可以看懂第 3 章里握手/挥手的每一个包。
## 第三章：连接管理——三次握手、四次挥手与状态机

> [!note] 本章目标
> 掌握 TCP 连接从建立到释放的完整报文序列、背后的设计原因，以及贯穿始终的 11 个状态机。这是全篇最核心的一章。

### 三次握手：建立连接

| 步骤 | 方向 | 标志位 | Seq / Ack | 语义 |
|------|------|--------|-----------|------|
| 1 | 客户端 → 服务器 | `SYN=1` | seq=x | 请求建连，声明自己的 ISN=x |
| 2 | 服务器 → 客户端 | `SYN=1, ACK=1` | seq=y, ack=x+1 | 同意建连，发自己的 ISN=y，确认收到对方的 SYN |
| 3 | 客户端 → 服务器 | `ACK=1` | seq=x+1, ack=y+1 | 确认收到服务器 SYN，双方进入 ESTABLISHED |

**为什么必须是三次？**

1. **同步初始序列号（ISN）**：双方必须就各自的起始序号达成一致，后续字节流才能可靠编号。
2. **确认双方收发能力**：全双工通信需要双向确认。
3. **防止旧重复 SYN 造成混淆**：若只有两次握手，网络中延迟的旧 SYN 会被误当成新连接。三次握手让发送方验证——发现回应不合法就回 RST，拒绝建立错误的连接。
4. 额外能力：支持双方**同时发起连接**（simultaneous open）。

> [!tip] 一个记忆锚点
> 第三次握手其实"不需要携带数据"，它的存在纯粹是为了**让服务器确认"客户端收到了我的 SYN+ACK"**。少了这一步，服务器无法确定这个连接是否真的可用。

### 四次挥手：释放连接

以 A 主动关闭为例：

| 步骤 | 方向 | 标志位 | A 状态 | B 状态 |
|------|------|--------|--------|--------|
| 1 | A → B | `FIN=1, ACK=1` | FIN_WAIT_1 | ESTABLISHED |
| 2 | B → A | `ACK=1` | FIN_WAIT_2 | CLOSE_WAIT |
| 3 | B → A | `FIN=1, ACK=1` | FIN_WAIT_2 | LAST_ACK |
| 4 | A → B | `ACK=1` | TIME_WAIT（2MSL） | CLOSED |

**为什么是四次？**

TCP 是**全双工**协议，两个方向的关闭互相独立。收到 FIN 的一方**只回 ACK**，但不会立刻发自己的 FIN——它必须等本地应用也调用 `close()` 之后才能发 FIN。因此需要"两对 FIN/ACK"，共 4 个包。

> [!note] 特殊情况
> 若双方**同时关闭**（simultaneous close），可合并为三次，中间会出现 **CLOSING** 状态。

### 状态机与迁移链

TCP 的 11 个状态如下：

| 状态 | 含义 |
|------|------|
| CLOSED | 无连接的初始/终止态 |
| LISTEN | 等待连接请求（服务端） |
| SYN-SENT | 已发连接请求（客户端） |
| SYN-RECEIVED | 已收已发 SYN，等待确认 |
| ESTABLISHED | 正常数据传输 |
| FIN-WAIT-1 / FIN-WAIT-2 | 主动关闭方，等待对端 FIN |
| CLOSE-WAIT | 被动关闭方，等本地应用 close() |
| CLOSING | 双方同时关闭 |
| LAST-ACK | 已发自己的 FIN，等确认 |
| TIME-WAIT | 等待 2MSL 确保远端收到确认 |

**两条关键迁移链：**

```
主动方：ESTABLISHED →(发FIN)→ FIN_WAIT_1 →(收ACK)→ FIN_WAIT_2 →(收FIN,发ACK)→ TIME_WAIT →(2MSL)→ CLOSED
被动方：ESTABLISHED →(收FIN,发ACK)→ CLOSE_WAIT →(本地close,发FIN)→ LAST_ACK →(收ACK)→ CLOSED
```

**TIME_WAIT 初识**：主动关闭方发完最后一个 ACK 后进入 TIME_WAIT，持续 **2MSL**（RFC 规范 4 分钟，Linux 实际约 60 秒）。两个作用：
1. 若最后一个 ACK 丢失，对端会重发 FIN，本方仍在 TIME_WAIT 可再回 ACK。
2. 让旧连接的迟到报文在网络中自然消亡，防止污染复用同一四元组的新连接。

### 半关闭 vs 半开连接

这两个概念极易混淆，务必区分：

| 维度 | 半关闭（Half-Close） | 半开连接（Half-Open） |
|------|----------------------|----------------------|
| 性质 | 协议**正常**特性（单向关闭） | **异常**故障状态（僵尸连接） |
| 前提 | 双方进程均存活 | 一方崩溃/断电/网络断裂 |
| 对应状态 | FIN_WAIT_1/2、CLOSE_WAIT | 幸存方仍停留 ESTABLISHED |
| 触发 | 应用 `shutdown(SHUT_WR)` 发 FIN | 对端未发 FIN 即消失 |
| 后果 | 正常，另一方向可继续传输 | 资源泄漏，需 Keepalive 回收 |

> [!example] 半关闭的典型应用
> HTTP/1.1 中，客户端发完请求后可以半关闭**发送**方向，服务器仍可通过同一连接回传完整响应体，全部发完后再发自己的 FIN。

### 动手验证：curl + tcpdump

在本地用最简单的方式观察一次完整握手：

```bash
# 终端 A：抓包（Linux 用 eth0，macOS 用 en0）
sudo tcpdump -i en0 -nn -S 'tcp port 8080' -c 10

# 终端 B：发起一个本地连接
python3 -m http.server 8080 &
curl -I http://127.0.0.1:8080/
```

预期输出三条核心记录：

```
... Flags [S],   seq 123456789, win 64240, length 0   ← SYN
... Flags [S.],  seq 987654321, ack 123456790, win 64240, length 0   ← SYN+ACK
... Flags [.],   ack 987654322, win 64240, length 0   ← ACK
```

校验：`包2.ack = 包1.seq + 1`，`包3.ack = 包2.seq + 1`——正是第 2 章讲的"SYN 占一个序号"。

> [!summary] 本章小结
> - 三次握手同步 ISN 并确认双向能力，**三次而非两次**是为了防止旧 SYN 混淆。
> - 四次挥手源于全双工下每方向需独立关闭。
> - 11 个状态机贯穿连接一生；TIME_WAIT 是主动关闭方的"安全等待区"。
> - **半关闭是正常特性、半开是故障**，二者状态与后果完全不同。
> - 用 curl + tcpdump 可以亲手验证整个握手过程。
## 第四章：可靠传输——确认、窗口与拥塞控制

> [!note] 本章目标
> 理解 TCP 如何用"确认 + 重传"实现可靠，又如何用两套窗口（流量控制、拥塞控制）实现高效——这是 TCP 最精妙的部分。

### 累计确认与 ACK 策略

TCP 面向**字节流**，可靠性建立在字节序号之上：

- 接收方用**累计确认**返回"下一个期望的字节序号"：`Ack = 已连续收到的最后字节 + 1`。
- **ARQ（自动重传请求）**：发送方发出数据后启动计时器，若在 RTO 内未收到 ACK，就重传最早未确认的报文段。
- 接收方收到**乱序**数据时立即回**重复 ACK**，催促发送方补发。

> [!note] 为什么按字节编号而不是按报文编号？
> 按字节编号让 TCP 在重传时可以把数据**重新分片**成更大的段再发，也使得累计确认天然简洁——一个 Ack 就能确认前面所有字节。

**ACK 生成策略**（RFC 5681/1122）：
- **延迟 ACK**：每 2 个满段至少回 1 个 ACK，且收到第一个未确认报文后 500ms 内必须回。
- 乱序报文**立即回重复 ACK**；每收一个段最多回一个 ACK。

### 流量控制：滑动窗口

**目的**：防止发送端太快、淹没接收端缓冲区（端到端速率匹配）。

- 接收方在 TCP 头部**接收窗口 RWND** 里通告自己还能收多少字节；窗口字段 16 位，最大 65,535 字节。
- 发送方维护一个发送窗口，**已发送未确认的数据必须落在窗口内**。窗口三种操作：
  1. **打开**：收到 ACK，已确认部分滑出，可继续发新数据。
  2. **关闭**：已确认数据不再保留，左缘右移。
  3. **缩小**：接收方减小 RWND（允许但不推荐）。

**零窗口死锁与持久计时器**：若接收方缓冲区满，通告 `RWND=0`，发送方必须停发，双方可能互相等待。解决方式：发送方启动**持久计时器（Persist Timer）**，周期发送**窗口探测包**，直到收到非零 RWND。

### 拥塞控制：四算法

**目的**：防止发送太快压垮网络节点。核心是两个变量：

- **cwnd**（拥塞窗口）：发送方对在途未确认数据的自身上限。
- **ssthresh**（慢启动阈值）：决定走慢启动还是拥塞避免。

| 算法 | 触发条件 | 行为 |
|------|----------|------|
| 慢启动 | cwnd < ssthresh | 每个 RTT cwnd 翻倍（1→2→4→8），指数探测带宽 |
| 拥塞避免 | cwnd > ssthresh | 每 RTT 线性 +1 满段，缓慢增长 |
| 快速重传 | 收到 **3 个重复 ACK** | 不等超时，立即重传最早未确认段 |
| 快速恢复 | 快速重传后 | 窗口减半再逐步恢复 |

**关键公式**（RFC 5681）：
- 慢启动：`cwnd += min(N, SMSS)`（每个确认新数据的 ACK）。
- 拥塞避免：`cwnd += SMSS² / cwnd`（每 ACK）。
- 快速恢复第 3 个重复 ACK：`ssthresh = max(FlightSize/2, 2×SMSS)`；`cwnd = ssthresh + 3×SMSS`。
- **超时**（强拥塞信号）：`ssthresh = max(FlightSize/2, 2×SMSS)`；`cwnd = 1`（退回慢启动）。

> [!warning] FlightSize 不是 cwnd
> FlightSize 是**实际在途未确认的数据量**，cwnd 可能大于接收窗口 rwnd。计算 ssthresh 用的是 FlightSize。

### 超时与重传：RTO、Karn 与指数退避

- **RTT**：报文发出到收到对应 ACK 的往返时间。
- **RTO**：等待 ACK 的最长期限。过大会降吞吐，过小会误判丢包引发无谓重传。

**RTO 动态估算**（RFC 6298，α=1/8、β=1/4、K=4）：

```
首样本 R：SRTT = R；RTTVAR = R/2；RTO = SRTT + max(G, 4×RTTVAR)
后续样本 R'：RTTVAR = (1-β)×RTTVAR + β×|SRTT - R'|
             SRTT   = (1-α)×SRTT + α×R'
             RTO    = SRTT + max(G, 4×RTTVAR)
```

边界：RTO 低于 1 秒向上取整到 1 秒；无 RTT 样本时初始 RTO = 1 秒。

**Karn 算法**解决"重传二义性"——报文超时重传后，收到的 ACK 无法判断是针对首次发送还是重传的：
1. 被重传段的 ACK **不参与 RTT 测量**（除非启用时间戳选项）。
2. 重传期间 RTO 直接**指数退避**：`RTO = RTO × 2`，直到上限 64 秒。
3. 新数据被正常确认后恢复常规计算。

典型退避序列：1, 3, 6, 12, 24, 48, 64 秒……连续重传约 9 分钟后放弃并发 RST。

### 发送窗口：两套窗口的合力

```
发送窗口 = min(cwnd, rwnd)
```

- **rwnd** 防止淹没接收方（流量控制）。
- **cwnd** 防止压垮网络（拥塞控制）。
- 哪个小，就以哪个为实际发送上限：接收方处理慢→rwnd 主导；网络拥塞→cwnd 主导。

### 最小演示：Python Socket

用 Python 直观感受"连接建立 + 字节流收发"：

```python
# server.py
import socket
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 9000))
srv.listen(5)
conn, addr = srv.accept()          # 三次握手在这里完成
data = conn.recv(1024)             # 读取字节流
print("收到:", data.decode())
conn.sendall(b"hello client")      # 回传
conn.close()
```

```python
# client.py
import socket
cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cli.connect(("127.0.0.1", 9000))   # 三次握手在这里完成
cli.sendall(b"hello server")
print("收到:", cli.recv(1024).decode())
cli.close()
```

> [!tip] 配合第 5 章观察
> 运行这两个程序时，用 `tcpdump` 或 Wireshark 抓 127.0.0.1 的 9000 端口，就能看到 `connect()` 触发三次握手、`close()` 触发四次挥手。

> [!summary] 本章小结
> - 可靠性来自**累计确认 + ARQ 重传**，按字节编号让一切变简洁。
> - 流量控制用 **rwnd** 保护接收方；拥塞控制用 **cwnd** 保护网络；实际发送上限是两者的较小值。
> - 拥塞控制四算法（慢启动/拥塞避免/快速重传/快速恢复）是 TCP 高效传输的引擎。
> - RTO 动态估算 + Karn 算法 + 指数退避，共同构成超时重传机制。
## 第五章：工具链实操——抓包与连接状态观察

> [!note] 本章目标
> 用 tcpdump / Wireshark / ss 亲手观察真实连接。工具熟练后，第 6 章的排查才有着力点。

### tcpdump：抓取三次握手 / 四次挥手

**环境**：Linux / macOS 均可用，通常需 `sudo`；macOS 网卡常为 `en0`，Linux 为 `eth0`。

**关键参数**：

| 参数 | 作用 |
|------|------|
| `-i 网卡` | 指定网卡 |
| `-nn` | 纯数字，不做域名/端口反解（抓包必加） |
| `-S` | 显示绝对序列号（默认显示相对 seq） |
| `-c N` | 抓 N 个包后停止 |
| `-w file.pcap` / `-r file.pcap` | 写文件 / 读文件 |
| `-ttt` | 显示与上一条的时间差 |

**抓取三次握手**：

```bash
sudo tcpdump -i eth0 -nn -S 'host 192.168.1.5 and port 80' -c 10
# 典型输出：
# ... 192.168.1.5.54231 > 203.0.113.1.80: Flags [S],  seq 123456789, ...   ← SYN
# ... 203.0.113.1.80  > 192.168.1.5.54231: Flags [S.], seq 987654321, ack 123456790, ...   ← SYN+ACK
# ... 192.168.1.5.54231 > 203.0.113.1.80: Flags [.],  ack 987654322, ...   ← ACK
```

校验：`包2.ack = 包1.seq + 1`、`包3.ack = 包2.seq + 1`。

**只抓特定标志位**：

```bash
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & tcp-syn != 0'            # 仅握手包
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-fin|tcp-ack) != 0'  # 仅挥手包
sudo tcpdump -i eth0 -w handshake.pcap 'tcp port 443'              # 存文件
```

**Flags 速查**：`[S]`=SYN，`[S.]`=SYN+ACK，`[.]`=ACK，`[P]`=PSH，`[F.]`=FIN+ACK，`[R]`=RST。

**异常特征**：
- 握手失败：客户端反复重发 `[S]`，始终没有 `[S.]` 回应。
- 挥手异常：只有 `[F.]` + `[.]`，迟迟没有对端 FIN（对应 FIN_WAIT_2 滞留）。

### Wireshark：过滤与追踪流

1. 选网卡开始抓包 → 触发流量（`curl -I https://example.com` 或浏览器访问）→ 停止。
2. **过滤器**：
   - `tcp`：只看 TCP。
   - `tcp.flags.syn==1`：过滤握手包。
   - `tcp.flags.fin==1`：过滤挥手包。
   - `ip.addr==1.2.3.4` / `tcp.port==443`：按地址/端口过滤。
3. **识别握手**：最前面三个包依次为 `[SYN] → [SYN,ACK] → [ACK]`。
4. **看真实序号**：Wireshark 默认显示相对 Seq（从 0 起），在 编辑→首选项→Protocols→TCP 关闭 "Relative sequence numbers" 即可看到真实 ISN。
5. **追踪单条连接**：右键任一本端报文 → 追踪流 → TCP 流，隔离出整条连接全部报文。

### ss / netstat：连接状态与队列统计

**环境差异**：`ss` 仅在 Linux；macOS 用 `netstat -an` 与 `lsof -i`。注意 Linux 的 `netstat -p` 显示进程，macOS 的 `-p` 是协议过滤。

```bash
# Linux —— ss 更快，大数据量推荐
ss -tnpa                       # 所有 TCP 连接，含进程
ss -s                          # 汇总统计（estab/synrecv/timewait…）
ss -tan state time-wait        # 按状态过滤
ss -lnt | grep :80             # 监听端口，看 Recv-Q/Send-Q 队列积压

# Linux —— netstat 兼容性更好
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'   # 按状态计数
netstat -s | grep -i "SYNs to LISTEN"    # 协议栈计数

# macOS
netstat -an | grep -i time_wait | wc -l
lsof -i :8080 -nP               # 查看占用某端口的进程
```

> [!tip] 队列积压怎么看
> `ss -lnt` 中 LISTEN 状态的 **Recv-Q** = 等待 `accept()` 的连接数（全连接队列积压），**Send-Q** = 队列容量上限。Recv-Q 持续接近 Send-Q 说明应用 accept 跟不上。

> [!summary] 本章小结
> - tcpdump 用 `-nn -S` 抓包，凭 `[S]/[S.]/[.]/[F.]` 判断握手/挥手与异常。
> - Wireshark 用过滤器、追踪流、相对序号开关快速定位单条连接。
> - `ss` 比 `netstat` 更快、支持按状态过滤；跨平台要留意参数差异。
> - 队列积压（Recv-Q vs Send-Q）是观察服务端处理能力的窗口。
## 第六章：高频连接异常排查

> [!note] 本章目标
> 能独立诊断四个最高频的 TCP 连接问题：CLOSE_WAIT、TIME_WAIT、SYN 洪水、半开连接。

### 大量 CLOSE_WAIT：几乎都是代码 bug

**机制**：CLOSE_WAIT 出现在**被动关闭方**。收到对端 FIN 并回 ACK 后进入该状态，等应用调用 `close()`。若应用迟迟不关，连接就卡死在 CLOSE_WAIT。

> [!warning] 核心判断
> **大量 CLOSE_WAIT ≈ 应用没关 socket，是代码 bug，调内核参数无效。**

**危害**：连接不释放 fd 与内存，积压多会触发 `Too many open files`，新连接无法建立（MySQL/Tomcat 假死）。

**排查命令**：

```bash
ss -ant | grep -i close-wait | wc -l       # 统计（正常 <10，>100 基本判定泄漏）
ss -antp | grep -i close-wait              # 定位持有 CLOSE_WAIT 的进程
ulimit -n                                  # 进程 fd 上限
ss -lnt | grep :端口                        # 全连接队列是否积压
```

**根因与处理**：
- 代码漏 `close()`：异常分支/return 前没关连接。Java 用 try-with-resources，DB 操作放 `finally { close }`。
- 连接池 bug：连接归还未关、以"对端 IP+端口"做 key 导致服务下线后连接永不释放；应加探活。
- 响应慢/超时过小：客户端 timeout 断开，服务端线程阻塞无法 close。
- 临时缓解（只治标）：重启进程、调大 nofile 上限。**治本必须改代码**。

### 大量 TIME_WAIT：端口耗尽与治本

**机制**：TIME_WAIT 出现在**主动关闭方**，持续 2MSL（Linux 约 60 秒）。高并发短连接下大量连接堆积，可能耗尽本地端口。

> [!note] 风险分级
> TIME_WAIT 多本身危害有限（约 1 万条约 1MB 内存），**真正危险的是 CLOSE_WAIT**。TIME_WAIT 的问题是端口被"冻结"，报 `address already in use`。

**排查**：`ss -tan state time-wait | wc -l`；`ss -s`。

**处理（治本 > 内核参数）**：
- 治本：改长连接（HTTP keep-alive、连接池）；代码用 `SO_REUSEADDR`。
- 内核参数（写入 `/etc/sysctl.conf` 后 `sysctl -p`）：

```bash
net.ipv4.tcp_tw_reuse = 1        # 复用 TIME_WAIT 为出站连接（需 tcp_timestamps=1）
net.ipv4.tcp_fin_timeout = 30    # 调小 FIN-WAIT-2
net.ipv4.ip_local_port_range = 1024 65000
net.ipv4.tcp_max_tw_buckets = 5000
net.ipv4.tcp_timestamps = 1
```

> [!warning] 不要开 `tcp_tw_recycle`
> 它通过时间戳加速回收，在 **NAT 环境下会造成"时间戳错乱"、部分用户连不上**，且内核 4.12+ 已移除该参数。

### SYN 洪水：半连接队列与防御

**原理**：攻击者伪造源 IP 狂发 SYN，服务端为每个半连接分配资源并回 SYN+ACK，但 ACK 永远不来，半连接队列被占满，正常用户握手失败。

**两个队列**：
- **半连接队列**（syn queue）：收到 SYN 未完成握手，长度由 `listen()` backlog 与 `tcp_max_syn_backlog` 共同决定。
- **全连接队列**（accept queue）：握手完成等待 `accept()`，`ss -lnt` 的 Recv-Q/Send-Q 可观察。

**关键参数**（Linux）：

| 参数 | 默认 | 作用 |
|------|------|------|
| `net.ipv4.tcp_max_syn_backlog` | ~1024 | 半连接队列上限 |
| `net.ipv4.tcp_synack_retries` | 5 | 服务端 SYN+ACK 重传次数 |
| `net.ipv4.tcp_syn_retries` | 5~6 | 客户端 SYN 重传次数 |
| `net.ipv4.tcp_syncookies` | 1 | SYN Cookie（=2 强制，=0 关闭） |

**检测**：`netstat -s | grep "SYNs to LISTEN"`；`ss -tan state syn-recv`；`dmesg` 出现 `possible SYN flooding... Sending cookies.`

**防御组合**：

```bash
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 65536
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 1
```

辅助：iptables `connlimit` 限制单 IP 并发半连接、`limit` 限制 SYN 速率。注意双刃剑：backlog 过大耗内存，retries 调太低在弱网下会误伤正常用户。

### 半开连接与 Keepalive

**半开连接**：一端崩溃/断电，对端不知情，仍停留 ESTABLISHED。发数据会触发 RST；检测依赖保活机制。

**TCP Keepalive 默认值"佛系"**（Linux `/proc/sys/net/ipv4/`）：

| 参数 | 默认 | 含义 |
|------|------|------|
| `tcp_keepalive_time` | 7200s | 空闲多久开始第一个探测包 |
| `tcp_keepalive_intvl` | 75s | 探测无响应后重发间隔 |
| `tcp_keepalive_probes` | 9 | 连续无响应次数上限 |

按默认值，对端崩溃后约 **7200 + 9×75 ≈ 7875s（约 2 小时 11 分）** 才释放连接。

**调整**：

```bash
sysctl -w net.ipv4.tcp_keepalive_time=1200
sysctl -w net.ipv4.tcp_keepalive_intvl=75
sysctl -w net.ipv4.tcp_keepalive_probes=9
# 应用级 setsockopt：TCP_KEEPIDLE / TCP_KEEPINTVL / TCP_KEEPCNT
# macOS：sysctl net.inet.tcp.keepidle / keepintvl / keepcnt
```

> [!tip] 生产首选应用层心跳
> 内核 Keepalive 不可控且发现慢，生产更常用**应用层心跳**（Netty `IdleStateHandler`、Dubbo 心跳），可控性更强、发现更快。

> [!summary] 本章小结
> - **CLOSE_WAIT 多 = 代码漏 close**，调内核参数无效，必须治本。
> - **TIME_WAIT 多 = 端口冻结**，先改长连接，再用 `tcp_tw_reuse` 等参数辅助，禁用 `tcp_tw_recycle`。
> - **SYN 洪水**靠 SYN Cookie + 调队列/重传参数 + 防火墙限速防御。
> - **半开连接**靠 Keepalive 或应用层心跳回收，默认 Keepalive 参数对生产太"佛系"。
## 第七章：关键数值速查与进阶路线

> [!note] 本章目标
> 沉淀一份随用随查的速查表，并给出从"基础"走向"深入"的清晰路径。

### 关键数值速查表

| 项目 | 数值 |
|------|------|
| TCP 首部 | 固定 20 字节（最小），60 字节（最大，含选项） |
| 端口范围 | 0~65535（16 位，知名端口 0~1023） |
| 序号 / 确认号 | 各 32 位 |
| 窗口字段 | 16 位，最大 65,535 字节 |
| MSS 效率阈值 | 数据仅 1 字节时利用率 ≤ 1/41 |
| MSL（RFC 793 规范值） | 2 分钟 |
| TIME_WAIT（RFC 语义） | 2MSL = 4 分钟 |
| TIME_WAIT（Linux 实际） | 约 60 秒（`TCP_TIMEWAIT_LEN=60*HZ`） |
| ISN 循环周期 | 约 4.55 小时（32 位时钟约每 4μs 递增） |
| RTO 初始值 | 1 秒（无 RTT 样本时） |
| 指数退避上限 | 64 秒 |
| 快速重传触发 | 3 个重复 ACK |
| Keepalive 默认（Linux） | 7200s + 9×75s ≈ 7875s 释放 |
| 拥塞窗口初始 | 1~10 MSS（按 SMSS 分档） |

### 核心 RFC 与书单

**关键 RFC**：
- RFC 793 — TCP 协议规范（连接管理、状态机）
- RFC 9293 — RFC 793bis，现行权威修订版（报文结构）
- RFC 1122 — 主机要求
- RFC 1323 — 时间戳、窗口缩放
- RFC 5681 — 拥塞控制
- RFC 6298 — RTO 计算
- RFC 7414 — TCP 学习路线图（Roadmap）

**推荐书籍**：
- 《TCP/IP 详解 卷1：协议》（Stevens）—— 精读第 17-27 章
- 《计算机网络：自顶向下方法》（Kurose & Ross）—— 建立整体观
- 《TCP/IP 图解》（竹下隆史等）—— 入门图文
- 《Unix 网络编程 卷1：套接字联网 API》（Stevens）—— socket 编程权威
- 《Linux 网络编程》（清华大学出版社）—— 用户层到内核层

### 进阶路线与动手实验

**8 步进阶路线**：

1. 分层模型（OSI vs TCP/IP）
2. TCP 报文头（端口/序号/确认号/标志位/窗口/选项）
3. 连接管理（握手/挥手/状态机，配抓包验证）
4. 可靠传输（seq/ACK/校验和/超时重传/SACK）
5. 流量控制（滑动窗口/窗口缩放/Nagle/延迟 ACK）
6. 拥塞控制（慢启动/拥塞避免/快速恢复/BBR）
7. 工程实践（内核调优、CLOSE_WAIT/TIME_WAIT 排障、心跳设计）
8. 进阶主题（TCP 多路复用、零拷贝、百万并发、HTTP/2、HTTP/3/QUIC、TLS）

**动手实验建议**：
- 用 tcpdump/Wireshark 抓包验证三次握手、四次挥手。
- 用 `curl -I` 制造流量，配合 `ss` 观察连接状态变化。
- 写 Python echo server/client（见第 4 章），理解 `connect()`/`close()` 背后的报文。
- 进阶挑战：Stanford CS144 动手实现一个 TCP/IP 协议栈。

**优质资源**：
- 小林 coding（图解网络）、酷壳 CoolShell、RFC Editor 官网
- Coursera《TCP/IP and Advanced Topics》、国家高等教育智慧教育平台《计算机网络》
- B 站 湖科大教书匠 / 韩立刚 TCP/IP 系列

> [!summary] 本章小结
> - 速查表覆盖首部、端口、TIME_WAIT、RTO、Keepalive 等关键数值，随用随查。
> - 权威依据以 RFC 793/9293/5681/6298 为核心，书籍首选《TCP/IP 详解》。
> - 进阶遵循"分层→报文→连接→可靠→流量→拥塞→工程→进阶"的 8 步路线，每个阶段都配动手实验。
> - 学完本笔记，你就为 HTTP/2、TLS、QUIC 等上层协议打下了扎实基础。
