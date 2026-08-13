# tcp协议 - 探测式收集结果

- 主题: tcp协议
- 项目标识: tcp-protocol
- 收集时间: 2026-08-12
- 阶段: 1 探测式收集（P1）
- 已确认方向: **TCP/IP 协议基础**（深度: 上手 / 基础: 有了解）
- 搜索方式: 3 个 subagent 并行探测

## 探索方向与素材

### 方向 1: TCP 基础概念与报文结构

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | RFC 9293 (RFC 793bis) — TCP 协议规范官方修订版 | https://www.rfc-editor.org/rfc/inline-errata/rfc9293.html | 5/5 | 官方文档 |
| 2 | 【计算机网络】详解 TCP/IP 分层模型 & 局域网和跨网络通信的原理 | https://cloud.tencent.com.cn/developer/article/2452493 | 5/5 | 技术博客 |
| 3 | 计算机网络：TCP 报文段的首部格式 | https://cloud.tencent.com.cn/developer/article/2430879 | 5/5 | 技术博客 |
| 4 | understand-tcp-udp / chapter2.md（TCP 协议头部分析） | https://github.com/JerryC8080/understand-tcp-udp/blob/master/chapter2.md | 4/5 | 技术博客 |
| 5 | 网络 TCP/IP 基础（OSI 七层网络参考模型、协议及原理） | https://developer.aliyun.com/article/871012 | 4/5 | 技术博客 |

**要点**:
- 报文首部最小 20 字节、最大 60 字节；序号/确认号各 32 位；控制位 8 个（CWR、ECE、URG、ACK、PSH、RST、SYN、FIN）
- TCP/IP 四层模型（链路层/网络层/传输层/应用层），MAC 地址 48 位，端口 0~65535（知名端口 0~1023）
- 校验和计算包含 12 字节伪首部

### 方向 2: 连接管理（握手/挥手/状态机）

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | RFC 793 — Transmission Control Protocol（原始 TCP 规范） | https://www.rfc-editor.org/rfc/rfc793.html | 5/5 | 官方文档 |
| 2 | 网络协议基础：TCP 三次握手 / 四次挥手 | https://cloud.tencent.com.cn/developer/article/2566977 | 5/5 | 技术博客 |
| 3 | 为什么 TCP 需要 TIME_WAIT ? | https://cloud.tencent.cn/developer/article/2473426 | 4/5 | 技术博客 |
| 4 | TCP 三次握手和四次挥手详解（阿里云） | https://developer.aliyun.com/article/1572990 | 4/5 | 技术博客 |
| 5 | TCP 连接的半打开和半关闭 | https://blog.csdn.net/weixin_30635053/article/details/99378838 | 4/5 | 社区讨论 |

**要点**:
- 连接由四元组（源/目的 IP + 源/目的端口）唯一标识；11 个状态（CLOSED 为虚构态）
- 三次握手同步 ISN 并确认双方收发能力；四次挥手因全双工需每方向独立关闭
- TIME_WAIT 持续 2MSL（Linux MSL 约 60s），作用：防旧包误收 + 保证可靠终止
- 半关闭（协议正常特性，shutdown 实现）vs 半开连接（异常状态，靠 keepalive 探测）
- 常见坑: 大量 CLOSE_WAIT 多为服务端未调 close()；TIME_WAIT 资源占用；SYN 洪水

### 方向 3: 可靠传输机制（流量/拥塞/重传）

| # | 标题 | URL | 评分 | 来源 |
|---|------|-----|------|------|
| 1 | RFC 5681: TCP Congestion Control | https://www.rfc-editor.org/rfc/rfc5681 | 5/5 | 官方文档 |
| 2 | TCP 中的流量控制与拥塞控制详解 | https://www.baeldung-cn.com/cs/tcp-flow-control-vs-congestion-control | 5/5 | 技术博客 |
| 3 | TCP/IP详解 卷1 第二十一章 TCP 的超时与重传 | https://cloud.tencent.com.cn/developer/article/1075971 | 4/5 | 技术博客 |
| 4 | TCP 重传、滑动窗口、流量控制、拥塞控制 | https://developer.aliyun.com/article/1498828 | 4/5 | 技术博客 |
| 5 | TCP 流量控制和拥塞控制（面试专题） | https://cloud.tencent.com.cn/developer/article/2411712 | 3/5 | 技术博客 |

**要点**:
- 拥塞控制四大算法: 慢启动、拥塞避免、快速重传、快速恢复；快速重传由 3 个重复 ACK 触发
- 流量控制（RWND 保护接收方）vs 拥塞控制（CWND 保护网络）；发送窗口 = min(cwnd, rwnd)
- 超时重传: RTO = SRTT + max(G, K×RTTVAR)；指数退避上限 64 秒
- 滑动窗口: 打开/关闭/缩小；rwnd=0 启动持续计时器 + 零窗口探测

## 综合分析

**共识点**:
- TCP 可靠、面向连接、字节流三大特性贯穿所有方向
- 连接管理与可靠传输都围绕"确认机制 + 状态迁移"展开
- 官方权威信源: RFC 793（连接管理）、RFC 9293（报文结构）、RFC 5681（拥塞控制）

**素材缺口**:
- 流量控制与 RTO 计算暂无同级别 RFC 网页资源（可补 RFC 2988 / RFC 1122）
- 工具链（tcpdump/Wireshark 抓包、netstat/ss 观察连接状态）素材尚未覆盖，需在阶段 2 深度收集补齐

## 待补充方向（进入 P2 后）

- 实战观察: tcpdump/Wireshark 抓包示例（三次握手、四次挥手报文级观察）
- 工具链: curl、netstat/ss、ping 的排查用法
- 进阶路径: RFC 2988（RTO）、RFC 1122（主机要求）、进阶学习资源
