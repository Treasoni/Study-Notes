# tcp协议 - 深度素材

- 主题: tcp协议
- 项目标识: tcp-protocol
- 收集时间: 2026-08-12
- 阶段: 2 深度收集（P2）
- 已确认方向: TCP/IP 协议基础（深度: 上手 / 基础: 有了解）
- 素材结构: 概念原理 + 连接管理 + 可靠传输 + 常见坑排查 + 工具链实操 + 进阶路径

---

## 一、TCP 基础概念与报文结构

### 1.1 TCP/IP 分层模型

- TCP/IP 四层模型：链路层 / 网络层 / 传输层 / 应用层。
- 与 OSI 七层对应关系：应用层（应用/表示/会话）、传输层、网络层、链路层（数据链路/物理）。
- 三大寻址概念区别与配合：**IP 地址**（网络层定位主机）、**MAC 地址**（链路层 48 位）、**端口号**（传输层定位进程）。
- 封装与解封装：应用数据逐层加头，接收方逐层剥头。
- TCP 面向连接可靠、UDP 无连接轻量。

### 1.2 TCP 报文头字段

**总体结构**：
- 固定首部 **20 字节**，最大 **60 字节**（含选项，数据偏移 4 位，最大 15×4=60）。
- 校验和计算需在 TCP 报文段前拼接 **12 字节伪首部**。

| 字段 | 位数 | 作用 |
|------|------|------|
| 源端口 | 16 | 标识发送方应用进程 |
| 目的端口 | 16 | 标识接收方应用进程 |
| 序号（Sequence Number） | 32 | 本报文段**第一个数据字节**的字节流序号 |
| 确认号（Ack Number） | 32 | 期望收到的**下一个字节**序号（仅 ACK=1 有效） |
| 数据偏移（首部长度） | 4 | 数据起始处距离，单位 32 位字（4 字节） |
| 保留 | 6 | 置 0 |
| URG / ACK / PSH / RST / SYN / FIN | 各 1 | 控制标志位（共 6 位；现代实现另有 CWR、ECE，共 8 个） |
| 窗口（Window） | 16 | 接收窗口大小（字节），用于流量控制 |
| 校验和（Checksum） | 16 | 校验首部+数据（含 12 字节伪首部） |
| 紧急指针（Urgent Pointer） | 16 | 仅 URG=1 有效 |
| 选项（Options） | 可变（4n） | MSS、SACK、时间戳、窗口扩大因子等 |

**关键数值**：
- 端口范围 0~65535（16 位，知名端口 0~1023）。
- MSS = TCP 报文段长度 − TCP 首部长度 = 数据字段最大长度，与接收窗口无关。
- 数据仅 1 字节时 IP 层开销至少 40 字节，网络利用率不超过 **1/41**。

### 1.3 序号/确认号语义（RFC 793）

- 确认号表示"下一个期待接收的字节序号"（累计确认）。
- SYN 报文在序号空间**占据一个位置**：SYN 占用序号 X，其后第一个数据字节序号为 X+1；FIN 同理占一个序号。
- 第三个握手包（ACK）**不占用序号空间**。

---

## 二、连接管理

### 2.1 三次握手

| 步骤 | 方向 | 标志位 | seq / ack | 语义 |
|------|------|--------|-----------|------|
| 1 | 客户端→服务器 | `SYN=1` | seq=x | 请求建连，声明 ISN(x)，客户端进 SYN-SENT |
| 2 | 服务器→客户端 | `SYN=1, ACK=1` | seq=y, ack=x+1 | 同意建连，发自己的 ISN(y)，确认收到对方 SYN |
| 3 | 客户端→服务器 | `ACK=1` | seq=x+1, ack=y+1 | 确认收到 SYN，双方 ESTABLISHED |

**为什么必须是三次**：
1. 同步双方的初始序列号（ISN）。
2. 确认双方收发能力正常（全双工双向确认）。
3. 防止旧重复 SYN 造成混淆（RFC 793 Figure 9 场景）——只有两次握手时，网络中延迟的旧 SYN 会被误当新连接；三次握手让发送方验证，不合法则回 RST。
4. 支持双方同时发起连接（simultaneous open）。

### 2.2 四次挥手（A 主动关闭为例）

| 步骤 | 方向 | 标志位 | seq / ack | A 状态 | B 状态 |
|------|------|--------|-----------|--------|--------|
| 1 | A→B | `FIN=1, ACK=1` | seq=u | FIN_WAIT_1 | ESTABLISHED |
| 2 | B→A | `ACK=1` | ack=u+1 | FIN_WAIT_2 | CLOSE_WAIT |
| 3 | B→A | `FIN=1, ACK=1` | seq=v | FIN_WAIT_2 | LAST_ACK |
| 4 | A→B | `ACK=1` | ack=v+1 | TIME_WAIT（2MSL） | CLOSED |

**为什么是四次**：TCP 全双工，两方向关闭独立；收到 FIN 的一方只回 ACK，须等本地应用也 close() 后才发自己的 FIN。若双方**同时关闭**可合并为三次（出现 CLOSING 态）。

### 2.3 TCP 状态机（11 个状态）

| 状态 | 含义 | 进入事件 | 离开事件 |
|------|------|----------|----------|
| CLOSED | 无连接初始/终止态 | 收到 RST；TIME_WAIT 超时 | 被动 OPEN→LISTEN；主动 OPEN→SYN-SENT |
| LISTEN | 等待连接请求 | 被动 OPEN | 收到合法 SYN→SYN-RECEIVED |
| SYN-SENT | 已发连接请求 | 主动 OPEN | 收到 SYN+ACK→ESTABLISHED；收到 SYN→SYN-RECEIVED |
| SYN-RECEIVED | 已收已发 SYN | LISTEN/SYN-SENT 收 SYN | 收到 ACK→ESTABLISHED；收到 RST→回 LISTEN/CLOSED |
| ESTABLISHED | 正常数据传输 | 完成三次握手 | 本地 CLOSE→FIN_WAIT_1；收到 FIN→CLOSE_WAIT |
| FIN-WAIT-1 | 已发 FIN | 本地 CLOSE 后发 FIN | 收到 ACK→FIN_WAIT_2；收到 FIN→CLOSING |
| FIN-WAIT-2 | 等对方 FIN | 收到对 FIN 的 ACK | 收到 FIN→TIME_WAIT |
| CLOSE-WAIT | 等本地应用 close() | 收到 FIN 后发 ACK | 本地 CLOSE→LAST_ACK |
| CLOSING | 双方同时关闭 | FIN_WAIT_1 中先收 FIN | 收到 ACK of FIN→TIME_WAIT |
| LAST-ACK | 等对方确认自己的 FIN | CLOSE_WAIT 后发 FIN | 收到 ACK of FIN→CLOSED |
| TIME-WAIT | 确保远端收到 FIN 确认 | FIN_WAIT_2/CLOSING 收 FIN 后发 ACK | 2MSL 超时→CLOSED |

**关键迁移链**：
- 主动方：`ESTABLISHED →(发FIN)→ FIN_WAIT_1 →(收ACK)→ FIN_WAIT_2 →(收FIN,发ACK)→ TIME_WAIT →(2MSL)→ CLOSED`
- 被动方：`ESTABLISHED →(收FIN,发ACK)→ CLOSE_WAIT →(本地close,发FIN)→ LAST_ACK →(收ACK)→ CLOSED`
- 异常：FIN_WAIT_1 先收 FIN→CLOSING；FIN_WAIT_2 收不到 FIN 依赖 `tcp_fin_timeout`。

### 2.4 TIME_WAIT

- 主动关闭方发完最后一个 ACK 后进入，持续 **2MSL**。
- **作用**：
  1. 确保最后一个 ACK 可靠送达（ACK 丢失时对端重发 FIN，本方仍可再回 ACK）。
  2. 排空网络中的旧重复报文，防污染复用四元组的新连接。
  3. 防止四元组复用引发串扰。
- **为什么 2MSL**：数据一个方向 1MSL + ACK 返回 1MSL。
- **关键数值**：RFC 793 规定 MSL=2 分钟，故语义上 TIME_WAIT=4 分钟；**Linux 实际约 60 秒**（`TCP_TIMEWAIT_LEN=60*HZ`，MSL 常取 30~60s）。
- **资源影响**：主要瓶颈是**端口耗尽**（高并发短连接场景）；内存/fd 次之。
- **调优参数**（Linux）：
  | 参数 | 作用 | 注意 |
  |------|------|------|
  | `net.ipv4.tcp_tw_reuse` | 允许 TIME_WAIT 复用为出站连接 | 需配合时间戳；仅主动发起方 |
  | `net.ipv4.tcp_tw_recycle` | 更快回收 | NAT 下有风险，Linux 4.12+ 已移除，勿用 |
  | `net.ipv4.tcp_max_tw_buckets` | TIME_WAIT 数量上限 | 兜底防端口耗尽 |
  | `net.ipv4.tcp_fin_timeout` | FIN_WAIT_2 超时 | 不直接控制 TIME_WAIT |
  | `SO_REUSEADDR` | 服务端重用 TIME_WAIT 的地址/端口 | 服务端重启场景常用 |

### 2.5 半关闭（Half-Close）vs 半开连接（Half-Open）

| 维度 | 半关闭 | 半开连接 |
|------|--------|----------|
| 性质 | 协议正常特性（单向关闭） | 异常故障状态（僵尸连接） |
| 前提 | 双方进程均存活 | 一方崩溃/断电/网络断裂 |
| 对应状态 | FIN_WAIT_1/2、CLOSE_WAIT | 幸存方仍停留 ESTABLISHED |
| 触发 | 应用 `shutdown(fd, SHUT_WR)` 发 FIN | 对端未发 FIN 即消失 |
| 后果 | 正常，另一方向可继续传输 | 资源泄漏，需 Keepalive/超时回收 |

- 半关闭典型应用：HTTP/1.1 客户端发完请求半关闭发送，等服务端回传响应。
- 半开检测：① 发数据触发 RST；② TCP Keepalive（Linux 默认 `tcp_keepalive_time=7200s`、`intvl=75s`、`probes=9`）；③ 应用层心跳。

### 2.6 鲁棒性原则

RFC 793 §2.10："be conservative in what you do, be liberal in what you accept from others."（对自己发送保守，对接收宽容。）

---

## 三、可靠传输机制

### 3.1 可靠传输基础

- 每个字节有唯一序列号；接收方用**累计确认**返回"下一个期望字节序号"：`ACK = 已连续收到的最后字节 + 1`。
- **ARQ（自动重传请求）**：发后启动计时器，RTO 内未收 ACK 则重传最早未确认段；收重复/乱序数据立即回**重复 ACK**。
- 按字节编号，重传时可把数据重新分片成更大的段。
- ACK 生成策略（RFC 5681/1122）：**延迟 ACK**（每 2 个满段至少 1 个 ACK，且 500ms 内必须回）；乱序立即回重复 ACK。

### 3.2 流量控制（滑动窗口）

- 目的：防接收方缓冲区溢出（端到端速率匹配）。
- 接收方在头部**接收窗口 RWND** 通告还能收多少字节；窗口 16 位，最大 65,535 字节。
- 窗口三种操作：打开（收到 ACK 前移）、关闭（左缘右移）、缩小（TCP 允许但不推荐）。
- **零窗口死锁**：RWND=0 时发送方停发，双方互相等待 → 发送方启动**持久计时器（Persist Timer）**周期发**窗口探测包**。
- 与拥塞控制区别：

  | 维度 | 流量控制 | 拥塞控制 |
  |------|----------|----------|
  | 控制对象 | 发送端↔接收端 | 网络节点之间 |
  | 目的 | 防接收端被淹没 | 防网络节点过载 |
  | 依据 | 接收端缓冲区（RWND） | 网络状况（CWND） |

### 3.3 拥塞控制（RFC 5681）

**两个核心变量**：
- `cwnd`：拥塞窗口，发送方对在途未确认数据的自身上限。
- `ssthresh`：慢启动阈值。经典初始值 65,535 字节（TCP/IP详解）；RFC 未规定默认。

**四算法**：慢启动 → 拥塞避免 →（拥塞）→ 快速重传 / 快速恢复。

1. **慢启动**（cwnd < ssthresh）：从 1 个满段开始，每个确认新数据的 ACK：`cwnd += min(N, SMSS)`；每个 RTT cwnd 翻倍（1→2→4→8），指数增长。初始窗口（IW）按 SMSS 分档（RFC 5681 §2）：SMSS>2190→2×SMSS；1095<SMSS≤2190→3×SMSS；SMSS≤1095→4×SMSS。
2. **拥塞避免**（cwnd > ssthresh）：每 RTT 线性增长约 1 满段：`cwnd += SMSS² / cwnd`。
3. **快速重传**：收到 **3 个重复 ACK** 立即重传 SND.UNA 最早未确认段。
4. **快速恢复**（RFC 5681 §3.2）：
   - 第 1、2 个重复 ACK（Limited Transmit，RFC 3042）：可发新数据但 cwnd 不变。
   - 第 3 个重复 ACK：`ssthresh = max(FlightSize/2, 2×SMSS)`；`cwnd = ssthresh + 3×SMSS`。
   - 之后每多一个重复 ACK：`cwnd += SMSS`。
   - 收到确认新数据的 ACK：`cwnd = ssthresh`，回到拥塞避免。

**超时处理**（强拥塞信号，退回慢启动）：
- `ssthresh = max(FlightSize/2, 2×SMSS)`（仅首次重传时设置）；`cwnd = 1 满段（Loss Window）`。
- **FlightSize** = 已发出未确认的数据量（注意不是 cwnd）。
- 空闲重连：超过 1 个 RTO 未收发，恢复前 `cwnd = min(IW, cwnd)`。

### 3.4 超时与重传（RFC 6298）

- **RTT**：报文发出到收到对应 ACK 的往返时间。**RTO**：等待 ACK 的最长期限。
- **RTO 公式**（RFC 6298，α=1/8，β=1/4，K=4）：
  - 首样本 R：`SRTT=R; RTTVAR=R/2; RTO = SRTT + max(G, 4×RTTVAR)`
  - 后续样本 R'：`RTTVAR=(1-β)×RTTVAR+β×|SRTT-R'|; SRTT=(1-α)×SRTT+α×R'; RTO=SRTT+max(G,4×RTTVAR)`
  - 边界：RTO 低于 1s 取整到 1s；无样本初始 RTO=1s（旧 RFC 2988 用 3s）。
  - Jacobson 经典形式：`Err=M-A; A←A+⅛Err; D←D+¼(|Err|-D); RTO=A+4D`。
- **Karn 算法**（重传二义性）：① 被重传段的 ACK 不参与 RTT 测量（除非启用时间戳 RFC 1323）；② 重传期间 RTO 指数退避；③ 新数据正常确认后恢复常规计算。
- **指数退避**：每次超时 `RTO=RTO×2` 至上限 64s；重传间隔序列 1,3,6,12,24,48,64…；连续重传约 9 分钟后放弃并发 RST。

### 3.5 发送窗口

- **发送窗口 = min(cwnd, rwnd)**（RFC 5681 约束：不得发送序号高于 最高已确认 + min(cwnd, rwnd)）。
- rwnd 小→流量控制主导；cwnd 小→拥塞控制主导。
- `ssthresh` 更新用 **FlightSize** 而非 cwnd（因 cwnd 可能超过 rwnd）。

---

## 四、常见坑与排查

### 4.1 大量 CLOSE_WAIT

- **机制**：被动关闭方收到 FIN 回 ACK 后进入 CLOSE_WAIT，等应用 close()。应用不关 socket → 卡在 CLOSE_WAIT。
- **本质**：**几乎必然是代码 bug（漏 close），调内核参数无效**。
- **危害**：fd 与内存泄漏 → `Too many open files` → 新连接无法建立。
- **排查命令**：
  ```bash
  ss -ant | grep -i close-wait | wc -l                      # 统计
  ss -antp | grep -i close-wait                             # 定位进程
  ls -la /proc/$(pidof 进程)/fd | wc -l; ulimit -n           # fd 数对比
  ss -lnt | grep :端口                                       # 全连接队列积压
  ```
- **处理**：代码补齐 close（try-with-resources/finally）；连接池探活；监控 CLOSE_WAIT>100 告警。

### 4.2 大量 TIME_WAIT

- **机制**：主动关闭方四挥后进入 TIME_WAIT（2MSL），高并发短连接下可耗尽端口。
- **危害**：TIME_WAIT 本身危害有限（约 1 万条约 1MB 内存），真正危险的是 CLOSE_WAIT。
- **排查**：`ss -tan state time-wait | wc -l`；`ss -s`。
- **处理（治本 > 内核参数）**：改长连接（HTTP keep-alive、连接池）、`SO_REUSEADDR`；内核参数：
  ```bash
  net.ipv4.tcp_tw_reuse = 1        # 需 tcp_timestamps=1，仅客户端角色
  net.ipv4.tcp_fin_timeout = 30
  net.ipv4.ip_local_port_range = 1024 65000
  net.ipv4.tcp_max_tw_buckets = 5000
  net.ipv4.tcp_timestamps = 1
  ```
- **不要开 `tcp_tw_recycle`**：NAT 下时间戳错乱，Linux 4.12+ 已移除。

### 4.3 SYN 洪水与半连接队列

- **原理**：伪造源 IP 狂发 SYN，半连接队列被占满，正常用户握手失败。
- **两个队列**：半连接队列（syn queue，长度由 listen backlog 与 `tcp_max_syn_backlog` 决定）；全连接队列（accept queue，`ss -lnt` 可观察）。
- **关键参数**（Linux）：

  | 参数 | 默认 | 作用 |
  |------|------|------|
  | `net.ipv4.tcp_max_syn_backlog` | ~1024 | 半连接队列上限 |
  | `net.ipv4.tcp_synack_retries` | 5 | 服务端 SYN+ACK 重传次数 |
  | `net.ipv4.tcp_syn_retries` | 5~6 | 客户端 SYN 重传次数 |
  | `net.ipv4.tcp_syncookies` | 1 | SYN Cookie（=2 强制，=0 关闭） |

- **检测**：`netstat -s | grep "SYNs to LISTEN"`；`dmesg` 出现 `possible SYN flooding... Sending cookies.`
- **防御组合**：`tcp_syncookies=1; tcp_max_syn_backlog=65536; tcp_synack_retries=2; tcp_syn_retries=1` + iptables connlimit/limit。注意双刃剑：backlog 过大耗内存、retries 过低弱网下误伤正常用户。

### 4.4 半开连接检测与 TCP Keepalive

- **Keepalive 默认值"佛系"**（Linux `/proc/sys/net/ipv4/`）：`tcp_keepalive_time=7200s`、`tcp_keepalive_intvl=75s`、`tcp_keepalive_probes=9`；对端崩溃约 2 小时 11 分后才释放。
- **调整**：
  ```bash
  sysctl -w net.ipv4.tcp_keepalive_time=1200
  sysctl -w net.ipv4.tcp_keepalive_intvl=75
  sysctl -w net.ipv4.tcp_keepalive_probes=9
  # 应用级 setsockopt：TCP_KEEPIDLE / TCP_KEEPINTVL / TCP_KEEPCNT
  # macOS：sysctl net.inet.tcp.keepidle / keepintvl / keepcnt
  ```
- 生产更常用**应用层心跳**（Netty IdleStateHandler、Dubbo 心跳）。

---

## 五、工具链实操

### 5.1 tcpdump 抓取三次握手 / 四次挥手

**关键参数**：`-i 网卡`；`-nn` 纯数字；`-S` 绝对序列号；`-c N` 停止；`-w/-r file.pcap`；`-ttt` 时间差。

```bash
sudo tcpdump -i eth0 -nn -S 'host 192.168.1.5 and port 80' -c 10
# 输出校验：包1 seq=x → 包2 ack=x+1；包2 seq=y → 包3 ack=y+1
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & tcp-syn != 0'            # 仅握手包
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-fin|tcp-ack) != 0'  # 仅挥手包
sudo tcpdump -i eth0 -w handshake.pcap 'tcp port 443'              # 存文件
```

**Flags 速查**：`[S]`=SYN，`[S.]`=SYN+ACK，`[.]`=ACK，`[P]`=PSH，`[F.]`=FIN+ACK，`[R]`=RST。
**异常特征**：握手失败=客户端反复 `[S]` 无 `[S.]` 回应；挥手异常=只有 `[F.]`+`[.]` 无对端 FIN（FIN_WAIT_2 滞留）。

### 5.2 Wireshark

- 过滤器：`tcp`、`tcp.flags.syn==1`、`tcp.flags.fin==1`、`ip.addr==IP`、`tcp.port==443`。
- 识别握手：前三个包 `[SYN]→[SYN,ACK]→[ACK]`。
- 相对序号默认从 0 起；编辑→首选项→Protocols→TCP 可关 "Relative sequence numbers" 看真实 ISN。
- 右键→追踪流→TCP 流隔离单条连接。

### 5.3 netstat / ss

```bash
# Linux（ss 更快）
ss -tnpa                          # 所有 TCP 连接含进程
ss -s                             # 汇总统计
ss -tan state time-wait           # 按状态过滤
ss -lnt | grep :80                # 监听端口 + 队列积压
netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'   # 状态计数
# macOS（无 ss）
netstat -an | grep -i time_wait | wc -l
lsof -i :8080 -nP
```
> 注意：Linux `netstat -p` 显示进程；macOS `-p` 是协议过滤。

---

## 六、进阶学习路径与资源

### 学习顺序（基础→深入）
1. 分层模型（OSI vs TCP/IP）
2. TCP 报文头（端口/序号/确认号/标志位/窗口/选项）
3. 连接管理（握手/挥手/状态机，配抓包验证）
4. 可靠传输（seq/ACK/校验和/超时重传/SACK）
5. 流量控制（滑动窗口/窗口缩放/Nagle/延迟 ACK）
6. 拥塞控制（慢启动/拥塞避免/快速恢复/BBR）
7. 工程实践（内核调优、CLOSE_WAIT/TIME_WAIT 排障、心跳设计）
8. 进阶（TCP 多路复用、零拷贝、百万并发、HTTP/2、HTTP/3/QUIC、TLS）

### 关键 RFC
- RFC 793（TCP 规范）、RFC 1122（主机要求）、RFC 1323（时间戳/窗口缩放）
- RFC 2018/2883（SACK）、RFC 5681（拥塞控制）、RFC 6298（RTO 计算）
- RFC 7414（TCP 学习路线图 Roadmap）

### 书籍
- 《TCP/IP 详解 卷1：协议》（Stevens）——精读 17-27 章
- 《计算机网络：自顶向下方法》（Kurose & Ross）
- 《TCP/IP 图解》（竹下隆史等）、《Unix 网络编程 卷1》（Stevens）
- 《Linux 网络编程》（清华大学出版社）、《图解 Linux 网络编程》（2026 新书）

### 课程/社区
- Stanford CS144（动手实现 TCP/IP 协议栈）
- Coursera《TCP/IP and Advanced Topics》、国家高等教育智慧教育平台《计算机网络》
- 小林 coding（图解网络）、酷壳 CoolShell、RFC Editor 官网

### 动手实验
Wireshark + tcpdump 抓包验证、`curl -I` 制造流量、Python/C 写 echo server/client、Packet Tracer/GNS3 模拟拓扑。

---

## 七、关键数值速查

| 项目 | 数值 |
|------|------|
| TCP 首部 | 固定 20 字节（最小），60 字节（最大） |
| 端口范围 | 0~65535（16 位） |
| 序号/确认号 | 各 32 位 |
| 窗口字段 | 16 位，最大 65,535 字节 |
| MSS 效率阈值 | 数据 1 字节时利用率 ≤ 1/41 |
| MSL（RFC 规范） | 2 分钟 |
| TIME_WAIT（RFC 语义） | 2MSL = 4 分钟 |
| TIME_WAIT（Linux 实际） | 约 60 秒（TCP_TIMEWAIT_LEN=60*HZ） |
| ISN 循环周期 | 约 4.55 小时（32 位时钟约每 4μs 递增） |
| RTO 初始值 | 1 秒（无 RTT 样本时） |
| 指数退避上限 | 64 秒 |
| 快速重传触发 | 3 个重复 ACK |
| Keepalive 默认 | 7200s + 9×75s ≈ 7875s 释放 |

---

## 八、来源清单

**官方文档**
- RFC 793: https://www.rfc-editor.org/rfc/rfc793.html
- RFC 9293 (RFC 793bis): https://www.rfc-editor.org/rfc/inline-errata/rfc9293.html
- RFC 5681: https://www.rfc-editor.org/rfc/rfc5681
- RFC 6298: https://www.rfc-editor.org/rfc/rfc6298

**技术博客/社区**
- 腾讯云：TCP/IP 分层模型 (/article/2452493)、TCP 报文段首部格式 (/article/2430879)、三次握手/四次挥手 (/article/2566977)、TIME_WAIT 解析 (/article/2473426)、TIME_WAIT或CLOSE_WAIT原因解决 (/article/2093503)、close_wait 血案 (/article/2383535)、keepalive 特性解析 (/article/2389843)
- 阿里云：OSI/TCP/IP 基础 (/article/871012)、三次握手四次挥手详解 (/article/1572990)、tcpdump 抓包分析 (/article/518559, /article/763984)、timewait 优化 (/article/531366)、内核参数调优 (/article/1482736)、心跳包 (/article/616561)
- Baeldung-CN：流量控制 vs 拥塞控制 (baeldung-cn.com/cs/tcp-flow-control-vs-congestion-control)、TCP Socket 无连接超时
- GitHub：understand-tcp-udp (JerryC8080/understand-tcp-udp)
- CSDN：半打开和半关闭 (weixin_30635053/.../99378838)、半连接全连接队列
- 知乎：Linux TCP 内核参数优化总结；百度云：Wireshark TCP 三次握手解析

**注**：个别阿里云页面为 JS 渲染，静态抓取无法取到正文，已由等价的 RFC 官方标准及其他来源补足；内核参数默认值以 Linux `/proc/sys` 与 man 手册口径为准。
