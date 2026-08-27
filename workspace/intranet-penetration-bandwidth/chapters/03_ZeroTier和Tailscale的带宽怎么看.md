# 第三章：ZeroTier / Tailscale 的带宽怎么看——直连、中继与实测

上一章讲的"买套餐"方案，套餐页会白纸黑字写 2Mbps、5Mbps。但打开 ZeroTier 或 Tailscale 的定价页，你会发现找不到任何带宽数字——不是厂商漏写，而是这类方案的带宽逻辑完全不同。这一章回答：为什么这类方案没有套餐带宽、直连与中继的带宽来源差异在哪、用户态与内核态实现会造成多大实测差距，以及怎么"看"自家带宽。

## 3.1 为什么这类方案没有套餐带宽数字

ZeroTier 官方 FAQ 说得很直接：**直连时流量不经过 ZeroTier 服务器**，传输速度取决于两端设备的 CPU 与网络加解密收发能力；厂商不限速，也读不了加密包内容[^c3-S06]。

订阅限制落在"设备数 / 用户数"而不是带宽：

- Tailscale Personal 免费 **6 用户 / 不限设备**[^c3-G05]；
- ZeroTier 免费 **10 设备 / 1 网络**（老账号 25 设备）[^c3-G06]。

付费档买的是更多设备、更多网络、集中策略与团队管理，**不卖"更高带宽"**。ZeroTier 还特别强调：中继场景的性能与订阅等级无关[^c3-S06]。

所以结论是：这类方案的带宽不是套餐参数，而是**实测结果**——套餐页根本没有数字可看。

> [!tip] 大白话
> 把 ZeroTier/Tailscale 想成**给你和远方的朋友之间修一条专属小路**——小路多宽，取决于你们各自家门口的路（两端带宽）和搬东西的手速（CPU 加解密）；修路的人（厂商）不替你们限速，也看不到你们搬了什么。所以套餐页只能写"最多几个设备入网"，写不出"能跑多快"。

## 3.2 直连与中继：带宽来源完全不同

没有套餐带宽数字，不代表没有限制——限制藏在**走直连还是走中继**上。

**直连（[[P2P]]）**：两端直接通信，带宽上限 = 两端物理链路 + 两端 CPU/加密能力（第一章已讲过）。**中继**：打洞失败时流量经过厂商中继服务器，带宽上限变成"中继服务器 + 限速策略 + 两端链路"。

两类工具的官方说法就有差异：

- Tailscale 的 [[DERP]] 是**共享 TCP 中继**（走 TLS/443），官方明确"不为高性能优化"，会对吞吐执行速率限制与 fair usage（公平使用）限速；并且因为它是 TCP，丢包时重传带来的延迟惩罚比纯 UDP 更糟[^c3-S03]。
- ZeroTier 的 root 中继策略不同：官方声明只增加延迟、不主动限速；但没有量化限速数据，实际体验仍需实测[^c3-S06]。

跨洋实测最能说明差距。Tailscale 官方博客记录了一次印度→美国的实测：经共享 DERP 中继，iPerf3 只有约 **2.2Mbps**；启用自建 peer relay 后提升到 **27-35Mbps**（约 12.5 倍），延迟也从 452ms 降到 298ms[^c3-S02]。

> [!warning] 注意
> 中继本质是"打洞失败后的回退路径"，而且是共享资源。对称 NAT 或运营商 [[CGNAT]]（大内网）环境下，UDP 打洞常会失败，流量自动回退到 DERP/root 中继——这就是很多人"带宽突然断崖"的根本原因（第 5 章会展开）。

> [!tip] 大白话
> 直连像**飞机直飞**，中继像**先飞到中转机场再转机**。中转机场吞吐有限、时刻要和所有人共享，遇上天气（丢包）还得排队重飞。所以"有没有经过中转"比"套餐写了多少 Mbps"重要得多。

## 3.3 用户态 vs 内核态：实测吞吐差距

即使同为"直连"，不同实现的实测吞吐也能差出好几倍。一个典型的同链路基准测试（同一台千兆交换机直连两台机器）[^c3-S07]：

| 方案 | 实测吞吐 | 说明 |
|------|----------|------|
| 裸直连（无隧道） | 754 Mbps | 基线 |
| Netmaker（内核态 WireGuard） | 852 Mbps | 内核态加密 |
| ZeroTier | 546 Mbps | 用户态加密 |
| Tailscale | 268 Mbps | 用户态加密 + 重传 |

Tailscale 最低，**并不是因为中继限速**（测试都在同一条链路直连），而是它的实现偏重用户态加密（userspace），加解密在应用程序进程里完成，并伴随重传开销；Netmaker 走内核态 WireGuard，加密在操作系统内核里完成，开销更小[^c3-S07]。

> [!tip] 大白话
> 把加密想成**安检**。内核态像**流水线自动安检**——行李在传送带上边过边检，几乎不停顿；用户态像**每件行李都搬到人工安检台检查**——更灵活，但每件都要折腾一下。隧道数据量越大，"人工安检"的时间占比越明显，实测吞吐就越低。

> [!note] 这说明什么
> 对带宽评估而言：直连时你该看的不是厂商套餐，而是**两端设备的 CPU 和网络实现**。老旧的 NAS、树莓派跑用户态实现，实测吞吐可能远低于桌面机。

## 3.4 怎么"看"自家带宽

三步走，全部靠实测而不是看套餐页。

**第一步：判断走直连还是中继。** Tailscale 用 `tailscale ping`：

```bash
# 用节点名或 Tailscale 内网 IP ping 另一台设备
tailscale ping nas

# 走中继时，输出会带 via DERP：
pong from nas (100.101.102.103) via DERP(ord) in 80ms

# 直连时，输出直接显示对端 IP:端口，没有 DERP：
pong from nas (100.101.102.103) via 203.0.113.9:41641 in 12ms
```

看到 `via DERP(...)` 就是走了中继；显示对端 `IP:端口` 就是直连[^c3-S02]。ZeroTier 没有完全等价的单条命令，但可以用 `zerotier-cli peers` 查看对端路径是否经由 relay（root）中继[^c3-S06]。

**第二步：实测端到端吞吐。** 用 iPerf3 在隧道两端测，不要只用 Speedtest 测本机公网——那测不到隧道自身。完整的四组命令配方放在第四章。

**第三步：把实测结果对照场景需求。** 拿到的数字（比如"直连 500Mbps"或"中继 3Mbps"）去对照第二章的场景需求表，就知道够不够用、差多少。

> [!warning] 别忘了上行
> 隧道里"对外提供服务的那台设备"在大量消耗**它自己的上行**。判断直连吞吐前，先确认两端（尤其是服务端）的上行带宽——家宽上行常只有 30-50Mbps，隧道再快也会被它卡住[^c3-S02]。

## 本章小结

- ZeroTier/Tailscale 没有套餐带宽数字：带宽由两端链路 + CPU/加解密决定，付费档只限设备数/用户数、不限带宽；带宽评估 = 实测。
- 直连与中继的带宽来源完全不同：DERP 是共享 TCP 中继、有 fair usage 限速；跨洋实测共享 DERP ~2.2Mbps，自建 peer relay 后 27-35Mbps。
- 同样的链路，实现方式也影响吞吐：实测裸直连 754 / Netmaker 852 / ZeroTier 546 / Tailscale 268 Mbps；Tailscale 低来自用户态加密 + 重传，不是中继限速。
- "看"带宽三步：`tailscale ping` 判断是否 `via DERP`（直连/中继）→ iPerf3 端到端实测 → 对照场景需求表。

下一章进入动手环节：用 iPerf3 完整测一遍自家隧道，把"直连还是中继""上行有没有被卡"都量化出来，并据此做选型决策。

---

[^c3-S06]: ZeroTier 官方文档 — [Bandwidth Considerations](https://docs.zerotier.com/faq/bandwidth/)
[^c3-S03]: Tailscale 官方博客 — [Improving NAT traversal, pt. 3](https://tailscale.com/blog/nat-traversal-improvements-pt3-looking-ahead)
[^c3-S02]: Tailscale 官方博客 — [Using Tailscale's Peer Relays to fix a homelab connection from across the globe](https://tailscale.com/blog/peer-relays-international-networks)
[^c3-S07]: TechOverflow — [iPerf3 基准：ZeroTier vs Netmaker vs Tailscale vs 直连](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/)
[^c3-G05]: Tailscale 官方定价 — https://tailscale.com/pricing
[^c3-G06]: ZeroTier 官方定价 — https://www.zerotier.com/pricing/
