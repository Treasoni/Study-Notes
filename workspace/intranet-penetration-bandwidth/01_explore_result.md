# 内网穿透带宽性能分析 - 探测式收集结果 (P1)

> 项目：intranet-penetration-bandwidth
> 收集日期：2026-08-27
> 状态：P1 完成，等待用户选择方向

---

## 方向菜单

1. **内网穿透与带宽基础** — NAT 打洞 P2P vs 服务器中转 Relay 的带宽差异；上行/下行带宽；为什么商业套餐用固定 Mbps 标注
2. **ZeroTier / Tailscale 带宽评估机制** — 为什么这类方案不按套餐标带宽；直连 P2P vs DERP/Planet/Moon 中继；如何自行测速评估
3. **商业套餐 2 / 4 / 8 Mbps 量化** — 逐档列出能支撑的场景（远程桌面、NAS、Web、串流、同步）与带宽需求对照表
4. **实战内容** — 安装配置 ZeroTier/Tailscale、iPerf3 测速方法、按自家场景估算带宽、常见坑排错

---

## 候选信源（按镜头分组，已去重）

### 镜头 A：带宽基础与商业套餐量化

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| A1 | Microsoft RDP Network Guidelines | https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/network-guidance | official | 2024-07 | 5 | 微软官方 RDP 带宽标准：轻量 1.5Mbps / 中度 3Mbps / 重度 5Mbps / 高性能 15Mbps，1080p≈5Mbps、4K≈15Mbps，直接量化 2/4/8Mbps 能支撑的远程桌面场景 |
| A2 | 花生壳内网穿透套餐页 | https://www.myoray.com/vir_goods/shells.html | official | 当前定价 | 5 | 国内"固定 Mbps"定价典型：专业版 2M、商业版 3M、旗舰 5M、铂金 7M，流量不限，解释国内套餐为何用 Mbps 标注 |
| A3 | ngrok Pricing | https://ngrok.com/pricing | official | 当前定价 | 4 | 国外云转发走"流量计费(GB)"而非固定 Mbps（free 1GB/月、超额 $0.10/GB），反衬两种商业模型 |
| A4 | Sakura Frp 官方套餐 | https://www.natfrp.com/ | official | 当前定价 | 4 | frp 商业服务代表：免费隧道限速 10 Mibps/5GiB，VIP 36 Mibps/163GiB，量化中转限速+流量双重约束 |
| A5 | RustDesk 直连还是中继：源码到实战 | https://www.cnblogs.com/32bin/p/21641255 | report | n/a | 4 | 实测 P2P 直连可达 850Mbps，中继受服务器/家宽上行限制（典型 30Mbps），打洞失败自动回退中继 |

### 镜头 B：ZeroTier / Tailscale 带宽评估

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| B1 | ZeroTier Bandwidth Considerations | https://docs.zerotier.com/faq/bandwidth/ | official | 2025-08 | 5 | 官方 FAQ：直连时流量不经过其服务器，带宽由 CPU 与两端物理链路决定；中继只增延迟不主动限速，性能与订阅等级无关 |
| B2 | Tailscale NAT traversal pt.3 | https://tailscale.com/blog/nat-traversal-improvements-pt3-looking-ahead | official | 2025-10 | 5 | DERP 为 TCP 中继，握手+缓冲增加延迟，作为共享资源有速率限制/公平使用节流；直连 UDP 不受此限 |
| B3 | ZeroTier Private Root Servers (Planet/Moon) | https://docs.zerotier.com/roots/ | official | 2026-01 | 4 | Planet/Moon 架构：moon 仅用于节点发现与打洞引导，直连建立后数据走 P2P，moon 不决定实际带宽 |
| B4 | iPerf3 基准：ZeroTier vs Netmaker vs Tailscale | https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/ | report | 2022-08 | 4 | 千兆交换直连实测：直连 754 / ZeroTier 546 / Tailscale 268 Mbps，给出可复现测速方法，量化 userspace WireGuard 加密开销 |
| B5 | Tailscale DERP 低上传 Issue #18017 | https://github.com/tailscale/tailscale/issues/18017 | community | 2025-11 | 3 | 真实排障：Windows 客户端经 DERP 上传仅 ~10Mbps，WSL 达 40Mbps，说明回退中继时吞吐受客户端与共享中继双重影响 |

### 镜头 C：实战测速与带宽需求估算

| # | 标题 | URL | 层级 | 日期 | 评分 | 相关性 |
|---|------|-----|------|------|------|--------|
| C1 | Tailscale Peer Relays (homelab) | https://tailscale.com/blog/peer-relays-international-networks | official | 2026-01 | 5 | 官方博客 iPerf3 实测印度→美国：DERP 共享中继仅 ~2.2Mbps，自建 peer relay 27–35Mbps，直观展示回退中继限速与家宽上行现实 |
| C2 | iperf3 官方手册 (ESnet) | https://software.es.net/iperf/invoking.html | official | iperf3 3.21 | 4 | iperf3 命令级权威参考：-P 并行流、-R 反向、-b 限速、-O 预热、-t 时长 |
| C3 | Zoom 带宽用量表 | https://library.zoom.com/admin-corner/network-management/quality-of-service-and-network-best-practices-explainer/calculating-bandwidth-usage-for-zoom-meetings-and-phone | official | n/a | 4 | 官方带宽表：1080p 视频会议上行 3.8Mbps、720p 1.2–2.6Mbps、纯语音 60–80kbps、1080p60 12.8Mbps |
| C4 | 川观新闻：50M 实得 5M 上行限速报道 | https://cbgc.scol.com.cn/news/5907145 | report | 2025-02 | 3 | 国内运营商将千兆/50M 上行限速至 5M 的真实案例，解释家庭宽带上行瓶颈 |
| C5 | Synology 官方 KB：4K 外网串流 | https://kb.synology.com/zh-tw/DSM/tutorial/Does_my_Synology_NAS_support_streaming_4k_videos | official | n/a | 3 | NAS 场景：4K 外网串流需 ≥25Mbps 上行，量化 NAS 媒体串流带宽需求 |

> 注：C1/C2/C3 与 A/B 有交叉引用，A1（RDP）与 C3（Zoom）共同支撑"各场景带宽需求对照表"。

---

## 覆盖缺口

1. **ZeroTier / Tailscale 免费版具体限制**：官方"性能与订阅等级无关"已确认，但免费版设备数（10 台/1 网络）与是否有流量上限缺官方定价页直接引用 → P2 补 Tailscale/ZeroTier 官方 pricing。
2. **国内 2/4/8Mbps 阶梯的直接对照**：花生壳给出 2/3/5/7M 档位，但没有一篇直接写"2Mbps 到底能干嘛"的权威表 → 需用 RDP/串流/会议带宽表自行合成对照表。
3. **ZeroTier root 中继的量化限速实测**：Tailscale DERP 有 #18017 实测，ZeroTier 中继缺量化数据 → P2 视需要补社区实测。
4. **frp/nps 自建中转的带宽瓶颈**：商业 frp 已覆盖，自建 frp 在云服务器上跑的带宽瓶颈需补一两个实践来源。

---

## P2 范围估算

- **核心深读**：约 8 篇（official 为主：RDP、ZeroTier FAQ、Tailscale pt.3、Peer Relays、iperf3 手册、花生壳/ngrok/Sakura 定价）
- **补充来源**：3–5 篇（免费版定价、frp 自建实践、ZeroTier 中继实测，视方向选择）
- **产出**：
  - 带宽需求对照表（远程桌面 / NAS / Web / 串流 / 会议 / 同步）
  - P2P vs 中转带宽原理说明（含直连/回退中继机制）
  - 商业套餐 2/4/8Mbps 场景量化表
  - iPerf3 实测方法 + ZeroTier/Tailscale 安装配置要点
- **预计规模**：P2 素材约 3–5k 字结构笔记，支撑一篇入门概念+实战的 Obsidian 笔记

---

## 下一步

等待用户选择学习方向（1–4，可多选），然后进入 **P2 深度收集**。
