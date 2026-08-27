# 内网穿透带宽性能分析 - 深度收集 (P2)

> 项目：intranet-penetration-bandwidth
> 收集日期：2026-08-27
> 状态：P2 完成，等待用户确认素材质量
> 精读缓存：`workspace/intranet-penetration-bandwidth/.research_cache/`

---

## 1. Scope

围绕用户三个问题组织：(1) 内网穿透带宽性能可以干嘛；(2) ZeroTier/Tailscale 这类方案如何评估带宽；(3) 商业套餐 2/4/8 Mbps 各能做什么（附带实战测速）。

**重要修正**：探测与精读后发现，国内主流固定带宽套餐（花生壳）实际档位为 **2 / 3 / 5 / 7 Mbps**（专业/商业/旗舰/铂金），并存在 3Mbps 的"测试号"；并非用户假设的 2/4/8。笔记需以 2/3/5/7 + 通用 2/4/8 两种口径说明"某个带宽档能干什么"。

---

## 2. Source Table

| ID | 标题 | URL | 层级 | 日期 |
|----|------|-----|------|------|
| S01 | iperf3 官方手册 (ESnet) | https://software.es.net/iperf/invoking.html | 官方 | iperf3 3.21 |
| S02 | Tailscale Peer Relays: fix homelab from across the globe | https://tailscale.com/blog/peer-relays-international-networks | 官方 | 2026-01 |
| S03 | Tailscale NAT traversal pt.3 | https://tailscale.com/blog/nat-traversal-improvements-pt3-looking-ahead | 官方 | 2025-10 |
| S04 | Microsoft RDP Network Guidelines | https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/network-guidance | 官方 | 2024-07 |
| S05 | 花生壳 Oray 套餐页 | https://www.myoray.com/vir_goods/shells.html | 厂商定价 | 2024 |
| S06 | ZeroTier Bandwidth Considerations | https://docs.zerotier.com/faq/bandwidth/ | 官方 | 2025-08 |
| S07 | iPerf3 基准：ZeroTier vs Netmaker vs Tailscale vs 直连 | https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/ | 报告 | 2022-08 |
| G01 | ngrok Pricing | https://ngrok.com/pricing | 厂商定价 | 2026-08 访问 |
| G02 | frp/nps 自建中转瓶颈（多篇汇总） | https://github.com/fatedier/frp/issues/4758 · https://github.com/fatedier/frp/issues/4879 · https://idctop.com/article/508738.html 等 | 报告/社区 | 2026-08 访问 |
| G03 | Zoom 官方带宽用量表 | https://library.zoom.com/.../calculating-bandwidth-usage-for-zoom-meetings-and-phone | 官方 | 2026-08 访问 |
| G04 | Synology KB：4K 外网串流带宽 | https://kb.synology.com/zh-tw/DSM/tutorial/Does_my_Synology_NAS_support_streaming_4k_videos | 官方 | 2026-08 访问 |
| G05 | Tailscale 官方定价 | https://tailscale.com/pricing | 官方 | 2026-08 访问 |
| G06 | ZeroTier 官方定价 | https://www.zerotier.com/pricing/ | 官方 | 2026-08 访问 |
| G07 | 川观新闻：运营商上行限速报道 | https://cbgc.scol.com.cn/news/5907145 | 报告 | 2025-02 |

---

## 3. Claim / Source Map

### 3.1 内网穿透两类架构与带宽含义

- **两类架构决定带宽来源**：
  - **P2P（NAT 打洞）**：节点间直连，流量不经过厂商服务器。带宽上限 = 两端物理链路 + 两端 CPU/加解密能力（S06）。
  - **中转（Relay）**：流量经服务器转发。带宽上限 = 中转服务器带宽/线路 + 限速策略 + 两端物理链路（S02/S03/G02）。
- **直连 vs 中转的量化差距**（RustDesk 实测，P1-A5）：P2P 直连可达 850Mbps，服务器中继受限于家宽上行（典型 30Mbps），打洞失败自动回退中继（P1-A5）。
- **商业套餐用固定 Mbps 标注**：国内厂商（花生壳、frp 商业服务）用"每映射固定带宽 + 映射数 + 并发数"定价（S05、P1-A4）；国外 ngrok 走"流量 GB 计费"（免费 1GB/月，超额 $0.10/GB）（G01）。两种商业模型：**带宽包**（稳定低速、不限流量）vs **流量包**（不限速、按量计费）。
- **上行带宽是常见隐形瓶颈**：家庭宽带下行 100-1000Mbps 但上行常仅 30-50Mbps（S02：作者 ISP 国际线路 30-40Mbps）；国内有运营商将上行限速到 5Mbps 的报道（G07）。内网穿透大量场景消耗的是**本端上行**。

### 3.2 ZeroTier / Tailscale 如何评估带宽

- **直连时"带宽=两端链路"**：ZeroTier 官方——流量不经过其服务器，"速度取决于两端 CPU 与网络加解密收发能力"，且**不限速、不能读加密包内容**（S06）。
- **中继仅作回退**：敌意 NAT/防火墙时包经 root 服务器中继，只增加延迟（物理路径更长），不保证可靠性；性能与订阅等级无关（S06）。
- **Tailscale DERP 是共享 TCP 中继**：本质为 TCP 中继（TLS/443），不为高性能优化；共享资源执行 rate limits 与 fair usage，会**限速吞吐**；丢包时 TCP 重传延迟比纯 UDP 更糟（S03）。
- **实测中继 vs 自建 relay**：跨洋（印度→美国）iPerf3 经共享 DERP 仅 **~2.2 Mbps**，启用自建 peer relay 后 **27-35 Mbps**（12.5x），延迟 452ms→298ms（S02）。
- **用户态 vs 内核态开销**：同一千兆交换链路实测——直连 754 / Netmaker(内核 WireGuard) 852 / ZeroTier 546 / Tailscale 268 Mbps（S07）。Tailscale 低吞吐是 userspace 实现 + 重传所致，**并非中继限速**（S07）。
- **免费版限制**：Tailscale Personal 免费 **6 用户 / 不限设备 / 50 个 tagged resources**（tagged 超额 $1/月/个，目前未强制），任何套餐无带宽/流量上限声明（G05）。ZeroTier 免费 **10 设备 / 1 网络**（老账号 25 设备），付费 Essential $18/月、Scale $179/月，各档无带宽披露（G06）。
- **如何"看"带宽**：不能看套餐页（根本没有），而要看——两端物理链路、`tailscale ping` 是否 `via DERP`（走中继）还是直连、用 iPerf3 实测端到端吞吐（S02/S06/S07）。

### 3.3 商业套餐带宽量化（2/3/5/7 与 2/4/8 口径）

- **花生壳固定带宽档**（S05）：测试号 3Mbps（TCP/HTTP 仅）、专业版 **2Mbps**、商业版 **3Mbps**、旗舰 **5Mbps**、铂金 **7Mbps**（流量不限）。价格与带宽非线性（测试号 3M 反超专业版 2M，差异在集群/并发/协议）。
- **Sakura Frp**：免费隧道限速 10 Mibps/5GiB，VIP 36 Mibps/163GiB（P1-A4）——中转同时限速+限流量。
- **自建 frp/nps 中转**：云服务器带宽是第一瓶颈（1核512MB 可支撑几十隧道）；**1Mbps 远程桌面基本不可用**，文件传输建议 ≥5Mbps，远程桌面/网站穿透建议 ≥10Mbps；低价"1Gbps 端口"常为共享带宽；运营商 QoS/高端口限速常见（frp 仅 500KB/s，改 80/443 后跑满）；协议差异 TCP≈18 / KCP≈68 / QUIC 75Mbps+（G02）。
- **ngrok 流量包模型**：免费 1GB/月，Hobbyist $10 含 5GB，超额 $0.10/GB（G01）——低流量/突发友好，重流量单价累计。

### 3.4 场景带宽需求对照表（用于"2/4/8 能干嘛"）

| 场景 | 推荐带宽 | 来源 | 2Mbps | 4Mbps | 8Mbps |
|------|----------|------|-------|-------|-------|
| 远程桌面 轻量（文字/办公） | 1.5 Mbps | S04 | ✅ 可用 | ✅ 流畅 | ✅ 富余 |
| 远程桌面 中度（日常操作） | 3 Mbps | S04 | ⚠️ 勉强 | ✅ 可用 | ✅ 流畅 |
| 远程桌面 重度（图形/1080p） | 5 Mbps | S04 | ❌ | ⚠️ 勉强 | ✅ 可用 |
| 远程桌面 4K | 15 Mbps | S04 | ❌ | ❌ | ⚠️ 不够 |
| 视频会议 720p | 1.2–2.6 Mbps | G03 | ⚠️ | ✅ | ✅ |
| 视频会议 1080p（1:1） | 3.8 Mbps | G03 | ❌ | ⚠️ | ✅ |
| 视频会议 1080p60 | 12.8 Mbps | G03 | ❌ | ❌ | ⚠️ |
| 网页浏览/API | <1 Mbps | 推断 | ✅ | ✅ | ✅ |
| NAS 文件传输（同步/备份） | ≥5 Mbps（越大越好） | G02 | ❌ 慢 | ⚠️ 慢 | ⚠️ 可用 |
| 媒体串流 1080p | ≥码率×1.5（≈6-15） | G04 | ❌ | ⚠️ | ⚠️ |
| 媒体串流 4K | ≥25 Mbps 上行 | G04 | ❌ | ❌ | ❌ |
| 纯语音通话 | 60–100 kbps | G03 | ✅ | ✅ | ✅ |

> 注：RDP/会议数字以 30fps、丢包 <0.1% 为前提（S04）；远程桌面类场景对延迟同样敏感（RTT ≤20ms 辅助技术），带宽够≠体验好。

### 3.5 实战：iPerf3 测速配方与常见坑

**iPerf3 测速配方**（S01 + S07）：
```bash
# 服务端（隧道内网主机）
iperf3 -s -p 5201
# 上行测速
iperf3 -c <隧道内网IP> -p 5201 -P 4 -t 30 -O 5
# 下行测速（加 -R）
iperf3 -c <隧道内网IP> -p 5201 -R -P 4 -t 30 -O 5
# UDP 丢包/抖动（UDP 必须显式 -b，默认仅 1 Mbit/s）
iperf3 -c <隧道内网IP> -u -b 20M -t 30
```
关键参数（S01）：`-P` 多流（仅 CPU 受限场景提升吞吐）、`-R` 反向下行、`-b` UDP 必须显式、`-O` 跳过 TCP 慢启动、`-t` 建议 ≥30s、默认端口 5201、控制连接与数据流分离。

**判定方法**：与场景表对比——远程桌面看单流（`-P 1`）结果；`tailscale ping` 看是否 `via DERP`（中继）判断走直连还是回退（S02）。

**常见坑汇总**（G02/S07/S03）：
1. 打洞失败回退中继：对称 NAT/CGNAT（运营商大内网）破坏 UDP 打洞 → 自动走 DERP/root → 带宽骤降（S02 印度运营商案例）。
2. 家庭宽带上行限制：千兆下行但上行 30-50Mbps，甚至被限 5M（G07）。
3. 用户态加密开销：Tailscale userspace 直连 268Mbps 低于内核态 852Mbps（S07）。
4. 商业套餐"带宽"≠实际吞吐：共享带宽、QoS、单线程限制都可能拉低（G02）。
5. TCP 中继拥塞：DERP 跨洋 2.2Mbps，丢包时重传惩罚（S02/S03）；frp 需调大 TCP 窗口/缓冲。

---

## 4. Contradictions / Caveats

1. **套餐档位口径**：用户假设 2/4/8 Mbps，花生壳实际 2/3/5/7；"4/8"不是国内主流档位，笔记应说明"档位因厂商而异，评估方法一致"。
2. **ZeroTier"不限速" vs Tailscale DERP"限速"**：两家中继策略不同（ZeroTier root 只加延迟不限速 vs Tailscale DERP 有 fair usage 限速），不是矛盾。
3. **S07 Netmaker 数据重复错标**：原页 netmaker-1 小节与 Tailscale 逐秒数据一致，不可当作独立数据点；Netmaker 真实值 852Mbps。
4. **场景数字前提**：RDP/Zoom 为推荐/峰值估算（30fps、<0.1% 丢包）；Synology 4K=25Mbps 为公网推荐值。
5. **ZeroTier 中继限速量化缺失**：官方无数字，缺社区实测（Tailscale DERP 有 2.2Mbps 实测）。

---

## 5. Practical Guidance（下游可直接引用）

- **先判断架构再谈带宽**：P2P 直连看两端链路与 CPU；走中继看中继服务器与限速。
- **ZeroTier/Tailscale 带宽评估 = 实测**：用 `tailscale ping`（是否 via DERP）+ iPerf3 端到端；不要找套餐带宽数字。
- **商业套餐选档**：2Mbps ≈ 轻量远程桌面/文字办公/网页；4Mbps ≈ 中度远程桌面/720p 会议；8Mbps ≈ 重度远程桌面(1080p)/1080p 会议/轻度文件传输；4K 串流/NAS 大文件传输需要 ≥15-25Mbps 或自建方案。
- **上行带宽是第一瓶颈**：选套餐前先测自家上行（`speedtest`/iPerf3），穿透流量大部分消耗本端上行。
- **打洞失败是最大变数**：运营商 CGNAT/对称 NAT 下 ZeroTier/Tailscale 会回退中继，带宽断崖式下降；可自建 peer relay/DERP/moon 缓解（S02）。

---

## 6. Open Questions（下游可选深挖）

1. ZeroTier root 中继的量化限速数据（官方未给，社区实测少）。
2. 国内各商业穿透厂商（花生壳/贝锐、NATAPP、Sakura）的 2/4/8 档位横向对比表（含流量/并发/协议限制）——需逐个厂商定价页。
3. WireGuard 内核态 vs 用户态对"带宽评估"的普适影响（仅 TechOverflow 单点实测）。

---

## 7. Downstream Handoff（供 outline-generator / chapter-writer）

- **笔记定位**：入门概念 + 实战。用户基础"有了解"，避免过深协议。
- **建议章节骨架**（可再调）：
  1. 内网穿透带宽是什么：P2P vs 中转，带宽从哪来
  2. ZeroTier/Tailscale 带宽怎么看（直连/中继/实测）
  3. 商业套餐 2/4/8（及 2/3/5/7）各能干嘛：场景对照表
  4. 实战：iPerf3 测速 + 按自家场景选型
  5. 常见坑与 FAQ
- **必须包含的实证数字**：RDP 1.5/3/5/15；Zoom 3.8/12.8；4K 串流 ≥25；DERP 2.2 vs peer relay 27-35；ZeroTier 免费 10 设备、Tailscale 6 用户无限设备。
- **缓存文件**：`.research_cache/01-07*.md` 含全文，章节写作时可再查。
