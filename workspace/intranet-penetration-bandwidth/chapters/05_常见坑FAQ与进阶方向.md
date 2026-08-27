# 第五章：常见坑、FAQ 与进阶方向

前面四章把"带宽从哪来、某个档位能干什么、怎么实测"都讲完了。可真到用起来，你会发现跑不动的原因往往不是"套餐不够"，而是藏在架构、运营商和实现细节里的几个坑。这一章把最常见的五个坑、四个高频 FAQ 和三条进阶路线一次讲清，当作以后排错的速查表。

## 5.1 常见坑：为什么"跑不到理论值"

### 坑 1：打洞失败自动回退中继，带宽断崖

[[P2P]] 的[[NAT 打洞]]依赖双方 NAT 行为可预测。遇到[[对称 NAT]]或[[CGNAT]]（运营商大内网）时，UDP 打洞会失败，ZeroTier / Tailscale 自动回退到 DERP/root 中继——带宽立刻从"两端链路"降级为"共享中继"，断崖式下跌。Tailscale 官方跨洋实测就是典型：共享 DERP 仅 **2.2Mbps**，启用自建 peer relay 后提升到 **27-35Mbps**（约 12.5 倍）[^c5-S02]。

> [!warning] 易错点
> 打洞失败通常**不报错，而是静默走中继**。远程桌面突然从"流畅"变"卡成幻灯片"，先查是不是走了 DERP/root，而不是急着换套餐。

> [!tip] 大白话
> 把[[CGNAT]]想成**小区大门统一收发快递**——运营商大内网让每户没有独立门牌（公网 IP），想"敲门直连"（UDP 打洞）找不到门，只能全部送到楼管（中继服务器）转交。所以明明是邻居间的小快递，也要绕一大圈还限速。

### 坑 2：家庭宽带上行被限，穿透流量全堵在上行

穿透流量大量消耗**被穿透端的上行**。家宽下行 100-1000Mbps 很常见，上行却常只有 30-50Mbps[^c5-S02]，国内甚至有运营商把上行限速到 **5Mbps** 的报道[^c5-G07]。

> [!warning] 易错点
> 千兆宽带 ≠ 千兆上行。买套餐前先 `speedtest` 或 iPerf3 测自家[[上行带宽]]，否则 NAS 外网传文件慢得离谱还找不到原因。

### 坑 3：用户态加密开销吃掉吞吐

同一条千兆交换链路上，内核态 WireGuard（Netmaker）能到 **852Mbps**，而用户态实现的 Tailscale 直连只有 **268Mbps**——差异主要来自加密在用户态 vs 内核态的损耗 + 重传，不是中继限速[^c5-S07]。

> [!tip] 大白话
> 把加密想成**打包行李**。内核态像流水线自动打包机（快），用户态像人手打包（稳但慢）。链路再宽，CPU 打包速度跟不上，吞吐照样上不去。

### 坑 4：商业套餐的"带宽"≠实际吞吐

套餐标注的 Mbps 是**上限**，不是保证值。[[共享带宽]]、运营商 [[QoS]]、单线程限制都会把它拉低。frp 社区有个典型例子：自建中转跑起来只有 **500KB/s**，把服务端端口从高端口改到 **80/443** 后直接跑满——是运营商对高端口限速，与套餐无关[^c5-G02]。

> [!example] 示例
> "1Gbps 端口"的便宜云服务器，往往写着共享带宽——一台机器几十人分。测出来只有几十 Mbps，不是配置错，是共享的。

### 坑 5：TCP 中继拥塞，丢包时雪上加霜

Tailscale 的 [[DERP]] 本质是 TCP 中继（TLS/443）。TCP 一旦丢包就要重传，高延迟下重传惩罚比纯 UDP 更糟[^c5-S03]；共享中继还会做 fair usage 限速，跨洋实测只有 **2.2Mbps**[^c5-S02]。自建 frp 中继同理，默认 TCP 窗口偏小，跨网大文件传输需要调大窗口与缓冲[^c5-G02]。

## 5.2 FAQ

**Q：为什么我买的 8Mbps 套餐跑不到 8Mbps？**

按顺序排查四件事：①本端上行是否够（上行被限，套餐再高也白搭）；②是否走了[[中继]]而非直连；③是否撞上共享带宽 / QoS / 单线程限制；④两端设备 CPU 是否扛得住加密。商业套餐的 Mbps 是上限，不是保底。

**Q：ZeroTier 和 Tailscale 谁更快？**

看实测：同一链路 ZeroTier 直连 **546Mbps**、Tailscale **268Mbps**（用户态拖累）[^c5-S07]。但"谁更快"取决于三件事：是否走直连、两端 CPU 性能、网络延迟；走中继时两者都受限（Tailscale DERP 有 fair usage 限速）。结论是**别问谁更快，问自家链路走没走直连**。

**Q：4K 串流 / NAS 大文件要多少带宽？**

4K 媒体串流公网推荐 **≥25Mbps** 上行[^c5-G04]；NAS 大文件传输建议 **≥5Mbps**，越大越好[^c5-G02]。对照第二章场景表，4K 串流是少数几个"商业 8Mbps 套餐也跑不动"的场景，只能靠自建直连或 peer relay。

**Q：打洞失败、带宽骤降怎么办？**

先用 `tailscale ping <节点>` 看是否 `via DERP`，确认走了中继；再考虑三条路：①自建 peer relay / DERP / [[Moon]] 缓解共享中继；②换有公网 IP 的线路（避开 CGNAT）；③改用商业固定带宽方案。打洞失败是最大变数，先诊断再动手[^c5-S02]。

## 5.3 进阶方向

- **自建 Moon / DERP / peer relay**：把共享中继换成自己的节点，实测跨洋从 2.2Mbps 提到 27-35Mbps[^c5-S02]。适合长期跨国使用、对带宽敏感的用户。
- **MTU 调优**：隧道内 [[MTU]] 过大时会被分片拖慢；把 WireGuard / Tailscale 接口的 MTU 调到合适值（如 1280-1420），常能明显改善吞吐[^c5-G02]。
- **frp TCP 窗口/缓冲调优**：自建 frp 中继跨网传输慢时，调大 TCP 窗口、收发缓冲，并避开被运营商 QoS 的高端口；配合多线程传输（iPerf3 的 `-P`）进一步榨干带宽[^c5-G02]。

## 本章小结

- 五个坑里，"打洞失败回退中继"和"家宽上行被限"最隐蔽、影响最大，排查优先级最高。
- 用户态加密、共享带宽 / QoS、TCP 中继拥塞，都会让实际吞吐低于理论值——Mbps 是上限不是保底。
- FAQ 的通用思路：先确认直连/中继，再测本端上行，最后对照场景表判断够不够。
- 进阶方向集中在"把中继换成自己的、把参数调到合适"两件事，投入小、收益明显。

到这里五章闭环：从"带宽从哪来"到"某个数字能干什么"，再到"怎么实测、怎么排错"。下一步把五章组装成一篇完整笔记，或先对照第四章在自家设备上跑一遍 iPerf3——你就能对自己的穿透方案做出靠谱判断了。

---

[^c5-S02]: Tailscale 官方博客 — Using Tailscale's Peer Relays to fix a homelab connection from across the globe, https://tailscale.com/blog/peer-relays-international-networks
[^c5-S03]: Tailscale 官方博客 — Improving NAT traversal, pt. 3, https://tailscale.com/blog/nat-traversal-improvements-pt3-looking-ahead
[^c5-S07]: TechOverflow — iPerf3 基准测试：ZeroTier vs Netmaker vs Tailscale vs 直连, https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/
[^c5-G02]: frp/nps 自建中转瓶颈（多篇社区汇总）, https://github.com/fatedier/frp/issues/4758 · https://github.com/fatedier/frp/issues/4879
[^c5-G04]: Synology KB — Does my Synology NAS support streaming 4K videos, https://kb.synology.com/zh-tw/DSM/tutorial/Does_my_Synology_NAS_support_streaming_4k_videos
[^c5-G07]: 川观新闻 — 运营商上行限速报道, https://cbgc.scol.com.cn/news/5907145
