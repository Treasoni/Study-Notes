---
title: "Linux 网络信息获取与概念 - 导航索引"
tags: [linux, network, index, moc]
created: 2026-07-29
updated: 2026-07-29
status: index
---

# Linux 网络信息获取与概念

> 从概念到命令，系统掌握 Linux 网络信息查询

**笔记类型**：实战笔记（概念解释 + 查询命令 + 实战示例）
**总章节**：10 篇
**建议学习时间**：带实操约 8–12 小时

---

## 章节列表

| # | 章 | 文件 | 说明 | 行数 |
|---|-----|------|------|------|
| 1 | 概览与工具链 | [[01_网络信息查询概览与工具链]] | 分层模型、iproute2 vs net-tools、查询速查表、通用排查思路 | 短 |
| 2 | 网络接口与链路层 | [[02_网络接口与链路层信息]] | MAC 地址、MTU、`ip link`、`ethtool`、JSON 输出 | 中 |
| 3 | IP 地址与子网 | [[03_IP地址与子网信息]] | IPv4 结构、CIDR、特殊地址、`ip addr`、`ip -j` + jq | 中 |
| 4 | 路由表 | [[04_路由表信息]] | 直连/静态/动态路由、最长前缀匹配、`ip route`、策略路由 | 中 |
| 5 | DNS 解析与域名 | [[05_DNS解析与域名信息]] | 解析流程、记录类型、配置文件体系、systemd-resolved、`dig` | 长 |
| 6 | ARP 与邻居发现 | [[06_ARP与邻居发现]] | ARP 协议、邻居状态机、`ip neigh`、NDP、表溢出排障 | 短 |
| 7 | Socket 连接与传输层 | [[07_Socket连接与传输层信息]] | TCP/UDP 协议、TCP 状态机、`ss` 命令、Recv-Q/Send-Q | 中 |
| 8 | 无线网络 | [[08_无线网络信息]] | `iw`、`nmcli`、信号质量 dBm、AP 扫描 | 短 |
| 9 | 网络监控与统计 | [[09_网络监控与统计]] | `iftop`、`nload`、`nethogs`、`bmon`、`ethtool -S`、`vnstat` | 中 |
| 10 | 抓包与协议分析 | [[10_抓包与协议分析基础]] | `tcpdump`、BPF 过滤表达式、报文解读、抓包存储 | 中 |

---

## 建议学习路径

### 按顺序阅读（推荐）
1. **第一章必读** — 建立分层模型和工具家族的全局认知
2. **第二至七章按序阅读** — 从 L2 到 L7 层层递进：
   - 链路层 → IP/子网 → 路由 → DNS → ARP/邻居 → 传输层/Socket
3. **第八章（无线）** — 如有无线网卡则学，否则可跳过
4. **第九章（监控）与第十章（抓包）** — 独立进阶技能，可在前面七章之后任意顺序学习

### 按排查场景跳读
| 遇到的问题 | 直接查阅章节 |
|-----------|-------------|
| 网卡不亮/连不上 | 第二章（`ip link` / `ethtool`） |
| 上不了网（IP 配置） | 第三章（`ip addr`） |
| 上不了网（路由问题） | 第四章（`ip route` / `ip route get`） |
| 域名解析失败 | 第五章（`dig` / `resolvectl`） |
| 端口被占用/连接异常 | 第七章（`ss`） |
| 内网机器不通 | 第六章（`ip neigh`） |
| WiFi 信号差 | 第八章（`iw` / `nmcli`） |
| 带宽跑满/谁在偷流量 | 第九章（`iftop` / `nethogs`） |
| 想抓包看协议细节 | 第十章（`tcpdump`） |

---

## 学习目标自检

学完本笔记后，你应该能：

- [ ] 熟练使用 `iproute2` 全家桶（`ip link`、`ip addr`、`ip route`、`ip neigh`）查询一切网络信息
- [ ] 理解 IP 子网划分、路由选择、DNS 解析、ARP 发现等核心概念
- [ ] 用 `ss` 替代 `netstat`，快速定位端口占用和连接异常
- [ ] 用 `dig` 和 `resolvectl` 排查域名解析故障（包括 systemd-resolved 相关痛点）
- [ ] 用 `iw` 和 `nmcli` 管理无线网络连接信息
- [ ] 用 `iftop`、`nload`、`nethogs` 监控实时带宽和进程级流量
- [ ] 用 `tcpdump` 抓包并分析基本的网络协议交互
- [ ] 理解并避开 Linux 网络查询中的常见坑（resolv.conf 被覆盖、ARP 表溢出、ICMP 限速假阳性等）

---

## 各章节 YAML Frontmatter 模板

拆分单篇笔记时，每章添加：

```yaml
---
title: "第N章：章节标题"
tags: [linux, network]
created: 2026-07-29
updated: 2026-07-29
status: complete
source_project: linux-network-info-concepts
---
```

---

*本索引页自动生成，属于 `linux-network-info-concepts` 项目的一部分。*
