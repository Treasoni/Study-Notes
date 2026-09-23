# 旁路由进阶使用 - 阶段 2 深度研究素材

> 工作流：learning-note-flow ｜ 运行：bypass-router-advanced
> 阶段：P2 深度收集 ｜ 检索日：2026-09-23
> 上游：`00_intent.md`（精通型）｜ `01_explore_result.md`（P1 方向与来源核对）
> 本轮范围：用户 P1 确认的 **A2 三种接管模式、A4 硬件加速失效、B2+B1 网关与 DHCP 下发体系、D1 多出口与故障转移**，加**排错方法论独立小节**

## 一、范围与取回方式

### 已排除（不在本轮）

A1（已有笔记覆盖）、A3、B3 DNS 分层、B4 分流规则、B5 IPv6、D2 浮动网关、D3 可观测性。笔记中如需引用，改为交叉链接既有笔记，不重复展开。

### 取回方式告警（影响可复现性，下游引用前必读）

| 现象 | 影响 | 处置 |
|------|------|------|
| `openwrt.org` 对自动化抓取返回 **Anubis 反爬挑战页**（HTTP 200，约 4–4.3KB，标题 `Testing to determine if you are a bot!`） | S4/S5/S5a/S6/S6a 及 G1 的 OpenWrt 官方引文**未能落盘**，均由 WebFetch 渲染提取 | 引号内引文为提取所得短引，**定稿前需人工复核**：S4 的 "not channel-bonding" 句、S5 的 `"3,192.168.1.1 6,192.168.1.1"` 句、G1 的 `masq_allow_invalid` 句 |
| `crawl.sh` 按**域名**命名输出文件，同域名多 URL 互相覆盖 | 曾发生 mankier 首发被覆盖 | 后续批量抓取统一使用独立子目录（本轮 G1/G2/G3 已改用 `cache/g1-luci/`、`cache/g2-kernel/` 等） |
| 社区教程站（S9）无署名、无发布日期，仅"最后查看"日期，页面含推广位 | 不可作为配置语义依据 | 仅用作入门流程与排查方法论，任何配置结论不得冒用官方口径 |
| DeepWiki 等 AI 聚合页含 `TPROXY High / TUN Medium` 类对比表 | 来源可信度不足 | **已排除**，未写入任何 claim |

## 二、来源表

### Tier 1 官方 / 一手

| ID | 来源 | 发布者 | 日期 | 落盘 | 用于 |
|----|------|--------|------|------|------|
| S1 | `xtls.github.io/document/level-2/transparent_proxy/transparent_proxy.html` | Project X (XTLS) | 未标注 | ✅ `cache/01_xtls_github_io.md` | A2 |
| S3 | `wiki.metacubex.one/config/inbound/` | mihomo 官方 | 未标注 | ✅ `cache/s3_inbound.md` | A2 |
| S3a | `.../config/inbound/listeners/tproxy/` | mihomo 官方 | 未标注 | ✅ `cache/s3a_tproxy.md` | A2 |
| S3b | `.../config/inbound/listeners/tun/` | mihomo 官方 | 未标注 | ✅ `cache/s3b_tun.md` | A2 |
| S3c | `.../config/inbound/tun/` | mihomo 官方 | 未标注 | ✅ | A2 |
| S4 | `openwrt.org/docs/guide-user/perf_and_log/flow_offloading` | OpenWrt Wiki（phinn） | 2026/08/17 | ⚠️ 未落盘 | A4 |
| S4b | `openwrt.org/docs/guide-user/firewall/firewall_configuration` | OpenWrt Wiki | 未标注 | ⚠️ 未落盘 | A4、排错 |
| S5 | `openwrt.org/docs/guide-user/base-system/dhcp` | OpenWrt Wiki | 未标注 | ⚠️ 未落盘 | B1+B2 |
| S5a | `.../base-system/dhcp_configuration` | OpenWrt Wiki | 未标注 | ⚠️ 未落盘 | B1+B2 |
| S6 | `openwrt.org/docs/guide-user/network/wan/multiwan/mwan3` | OpenWrt Wiki（jamesmacwhite） | 2026/07/25 | ⚠️ 未落盘 | D1 |
| S6a | `.../multiwan/mwan3-nft` | OpenWrt Wiki 托管，社区移植 | 2026/08/31 | ⚠️ 未落盘 | D1 |
| S2 | `doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html` | iStoreOS 官方文档 | 未标注 | ✅ `cache/03_doc_istoreos_com.md` | B1+B2 |
| S7 | `github.com/istoreos/istoreos/issues/2066` | istoreos 官方仓库 | 2025-01-17 起，末帖 2025-10-08 | ✅ `cache/02_github_com.md` | B1+B2 |
| SG1-02 | `raw.githubusercontent.com/openwrt/luci/master/.../luci-app-firewall/htdocs/luci-static/resources/view/firewall/zones.js` | OpenWrt LuCI 上游源码 | master | ✅ `cache/g1-luci/` | 排错 |
| SG2-01 | `kernel.org/doc/html/latest/networking/nf_flowtable.html` | kernel.org | 内核 7.3.0-rc4 | ✅ `cache/g2-kernel/` | A4 |
| SG2-02 | `wiki.nftables.org/.../Flowtables` | nftables 官方 wiki | — | ✅ `cache/01_wiki_nftables_org.md` | A4 |
| SG2-03 | `wiki.nftables.org/.../Configuring_chains` | nftables 官方 wiki | — | ✅ `cache/g2-chains/` | A4 |
| SG2-04 | `netfilter.org/documentation/HOWTO/netfilter-hacking-HOWTO-3.html` | netfilter.org | 2.4 时代 | ✅ | 排错（**仅用于 NFQUEUE 语义，不可用于 hook 顺序**） |
| SG3-01 | `tcpdump.org/manpages/tcpdump.1.html` | tcpdump.org | 未标注 | ✅ `cache/g3-tcpdump/` | 排错 |
| SG3-02 | `conntrack-tools.netfilter.org/manual.html` | netfilter.org | — | ✅ | 排错 |
| SG3-03 | `mankier.com/8/iptables` | 上游 man page 镜像 | 未标注 | ✅ `cache/g3-iptables/` | 排错 |

### Tier 3 社区操作经验（仅作标注后的经验引用）

| ID | 来源 | 日期 | 落盘 | 用于 |
|----|------|------|------|------|
| S8 | `wusiyu.me/openwrt-bypass-gateway-tcp-not-work/` | 2023-08-06 | ✅ `cache/01_wusiyu_me.md` | 排错 |
| S9 | `chonglangbiji.com/guide/openwrt-bypass-router-gateway-dns-transparent-proxy-2026/` | 无署名，"最后查看"2026-05-21 | ✅ `cache/01_www_chonglangbiji_com.md` | B1+B2、排错 |
| S12 | `blog.hellowood.dev/posts/openwrt-tag-specific-device-bypass-gateway-dns/` | 2025-08-10 / 更新 2026-03-22 | ✅ `cache/01_blog_hellowood_dev.md` | B1 |
| C1 | `blog.openyq.top/posts/23739/` | 未标注 | ✅ | A2（社区口径） |
| C2 | `aiya.de5.net/t/topic/192/2` | 未标注 | ✅ | A2（社区口径） |
| C3 | `global.v2ex.co/t/1086272` | 未标注 | ✅ | A2（社区口径） |
| C4 | `www.ha0wen.top/archives/2567` | 2025（站内） | ✅ | A2（社区口径） |

## 三、Claim / Source 映射（按笔记方向组织）

引用约定：`"……"` 内为来源原文逐字引用；标 **[推断]** 的条目无官方锚点，不得写成官方口径；标 **[未证]** 的条目在已抓取页面中查找失败。

### A2｜透明代理三种接管模式

| # | Claim | 来源 · 锚点 |
|---|-------|------------|
| A2-1 | 透明代理的定义："透明代理简单地说就是不让被代理的设备感觉到自己被代理了。"被代理设备上无需运行任何代理软件 | S1 ·「什么是透明代理」 |
| A2-2 | 局域网设备上网方向为 `PREROUTING → FORWARD → POSTROUTING`；"通过使用 iptables 操控PREROUTING链 和OUTPUT链的流量走向，转发到 Xray，就可以代理局域网设备和网关本机。" | S1 ·「iptables 实现透明代理原理」 |
| A2-3 | iptables 方案"由于其比 tun2socks 更高效率以及适合在路由器中配置而广泛使用。"**注意比较对象是 tun2socks，不能等同于 mihomo TUN** | S1 ·「iptables/nftables」 |
| A2-4 | **回程也走 PREROUTING**，是理解非对称路径的直接锚点："虽然网关访问公网 IP 不需要经过PREROUTING链，但被访问的服务器向网关返回信息时要经过PREROUTING链，且这部分被转发到 Xray 了" | S1 ·「相当于做到第一阶段」 |
| A2-5 | TProxy 需要策略路由才能接管本机出向流量："iptables-tproxy 不支持对OUTPUT链操作，但是我们可以通过配置策略路由，把OUTPUT链中相应的包重新路由到PREROUTING链上。"具体为 `ip rule add fwmark 1 table 100` 与 `ip route add local 0.0.0.0/0 dev lo table 100` | S1 ·「第三阶段」 |
| A2-6 | 官方明确判定 redirect 过时：所推荐教程中一篇"是基于 iptables-redirect 模式，已经过时了，不建议使用" | S1 ·「iptables/nftables」 |
| A2-7 | mihomo 官方把透明代理与系统接管归为一类，含 Redirect / TProxy / TUN 三种 listener；顶层 `port`/`socks-port`/`mixed-port`/`redir-port`/`tproxy-port` 适合只需一组固定代理端口 | S3 · Listener 类型表、开篇 |
| A2-8 | 官方对两种 TUN 入口的分工："顶层 `tun` 配置用于接管系统流量，适合需要自动路由、DNS 劫持或按应用分流的场景。"；"Listener 中的 TUN 面向高级使用场景。普通用户应优先使用顶层 TUN 配置。" | S3 · 开篇、Note；S3b · 首行注意 |
| A2-9 | TUN 的 stack 建议："如无使用问题，建议使用 `mixed`栈，默认 `gvisor`" | S3c · stack |
| A2-10 | `auto-redirect`："仅支持 Linux，自动配置 iptables/nftables 以重定向 TCP 连接，需要`auto-route`已启用"；`gso`"启用通用分段卸载，仅支持 Linux" | S3c · auto-route/auto-redirect、gso |

**A2 的两个结构性缺口（必须在笔记中如实呈现，不得用二手补白）**

1. **官方两条线未打通**：mihomo 官方 TProxy 页（S3a）**全文仅一行字段说明**（"是否监听 UDP"），完全不给 iptables/nftables 规则、fwmark 与策略路由前提；而这些前提只存在于 S1。S1 又把"主路由、单臂路由与旁路由"和"避免已有连接的包二次通过 TPROXY"明确标为 **"待补充..."**。→ 笔记应点明：**接管规则层在一手文档中是缺位的**，社区实践填补了它，这正是旁路由内容难以找到权威单一来源的根因。
2. **无一手定量性能数据**：无任何官方或可信实测给出 TUN vs TProxy 的吞吐与 CPU 占用对比。

### A4｜硬件加速为何让代理失效

| # | Claim | 来源 · 锚点 |
|---|-------|------------|
| A4-1 | flow offloading 的定义："bypasses the CPU-intensive Netfilter stack (firewall processing) for established traffic flows"，并"significantly increases network throughput" | S4 · 页面导言 |
| A4-2 | 软件卸载 SFO："typically increases bandwidth by 2-3x over firewall filtering each packet"；"Since SFO is a software feature it is widely supported on all CPUs" | S4 · SFO |
| A4-3 | 硬件卸载 HFO："requires specialized SoC hardware to bypass QoS traffic controls at high priority"；"handles a limited number of concurrent connections (64 queues is typical)"；"also incompatible with QoS features such as SQM" | S4 · HFO |
| A4-4 | 适用范围限定："applies to forwarded connections"，"including those to containers like LXC or podman, but not locally running web-server" | S4 · 适用范围 |
| A4-5 | 开关项：`flow_offloading`（默认 0）"Enable software flow offloading for connections. (decrease cpu load / increase routing throughput)"；`flow_offloading_hw`（默认 0）"Enable hardware flow offloading for connections. (depends on flow_offloading and hw capability)" | S4b · defaults 表 |
| **A4-6** | **机制层证实**：内核官方原文："A packet that finds a matching entry in the flowtable (ie. flowtable hit) is transmitted to the output netdevice via `neigh_xmit()`, hence, packets bypass the classic IP forwarding path (the visible effect is that you do not see these packets from any of the Netfilter hooks coming after ingress)." | SG2-01 · Overview |
| A4-7 | flowtable 挂载位置："Flowtables reside in the ingress hook that is located before the prerouting hook."；ingress"sees packets immediately after they are passed up from the NIC driver, before even prerouting." | SG2-02、SG2-03 |
| A4-8 | NFQUEUE 的机制基础：hook 返回值 "NF_QUEUE: queue the packet (usually for userspace handling)." → 排队必须发生在某个被遍历的 hook 内 | SG2-04 · §3.1 |
| **A4-9** | **[推断]** 由 A4-6～A4-8 推出："启用 flow offloading 后，依赖 NFQUEUE 的透明代理会拦不到已建立连接的后续包。"**机制前提已被官方原文证实，但内核与 OpenWrt 官方均未提及 NFQUEUE 或透明代理**，故此结论本身须标为推断，不得写成官方口径 | 组合推断 |

> **A4 必须纠正的一处官方边界**：S4 官方**全文未出现 NFQUEUE**（关键词核对：netfilter 出现、flowtable 出现、nftables 未出现、NFQUEUE 未出现）。因此「卸载后绕过 NFQUEUE」不能当官方说法引用。

### B2+B1｜网关与 DHCP 下发体系

| # | Claim | 来源 · 锚点 |
|---|-------|------------|
| B1-1 | 官方选项名的书写规则："The ID dhcp_option here must be with written with an underscore."；"OpenWrt will translate this to --dhcp-option, with a hyphen, as ultimately used by dnsmasq." | S5 · dhcp_option 条目 |
| B1-2 | **3=网关、6=DNS 的官方原文示例**：`"3,192.168.1.1 6,192.168.1.1" to give out gateway and DNS server addresses`（多个 option 用空格分隔） | S5 · 选项号示例段 |
| B1-3 | 强制下发的区别："Exactly the same as dhcp_option (note the underscores), but it will be translated to --dhcp-option-force"，"meaning that the DHCP option will be sent regardless on whether the client requested it."，"dhcp_option_force available since 18.06" | S5 · dhcp_option_force 条目 |
| B1-4 | tag 机制官方表述："you can use the dhcp_option list to add DHCP options to be sent to hosts with this tag (or networkid)."；"tag classifying sections have one configuration option: values of DHCP options to assign to this tag." | S5 · tag 条目 |
| B1-5 | tag 的官方写法：`uci set dhcp.tag1="tag"` + `dhcp.tag1.dhcp_option="6,8.8.8.8,8.8.4.4"`，host 侧 `dhcp.@host[-1].tag="tag1"` | S5a · tag classifier 段 |
| B1-6 | 用 MAC classifier 压掉默认网关的官方写法：`dhcp.mac1.dhcp_option="3"` 表示 "Disable default gateway"，再配 `"6,192.168.1.3"` 自定义 DNS | S5a · MAC classifier 段 |
| B1-7 | **社区实现与官方语义交叉印证**：tag 的实测渲染结果为 `dhcp-option=tag:proxynode,3,10.0.0.2` 与 `dhcp-option=tag:proxynode,6,10.0.0.2,1.1.1.1`；作者解释"3 是网关地址，6 是 DNS 地址，多个 DNS 地址用逗号分隔；不同的 dhcp_option 使用空格分隔" | S12 ·「tag 单独配置网关地址和 DNS」「检查配置」 |
| B1-8 | tag 下发的前提（社区）：需要"先给设备分配静态 IP 并添加 tag"，即 tag 下发依赖主机条目 | S12 ·「给设备分配添加 Tag」 |
| B1-9 | LuCI 局限（社区）："页面没有直接配置 tag 的网关和 DNS 的选项，需要通过命令行来配置" | S12 ·「tag 单独配置网关地址和 DNS」 |
| B1-10 | 客户端侧实测结果：`route -n` 默认网关变为 10.0.0.2，`resolvectl status eth0` 显示 "DNS Servers: 10.0.0.2 1.1.1.1"，且"其他没有配置 tag 的设备依然使用主路由的网关和 DNS 地址" | S12 ·「检查配置」 |
| B2-1 | iStoreOS 官方并列 **5 种**方案：手动静态 IP、旁路由 DHCP、（华硕）浮动网关、（iStoreOS）浮动网关、（iStoreOS 分身）浮动网关 | S2 ·「主旁方案」表 |
| B2-2 | 官方手动静态 IP 方案："主路由：任何路由器，默认开启DHCP，不需要其他任何设置"；旁路由"关闭DHCP"；设备侧手动指定网关/DNS 为旁路由 IP。→ **此方案完全不改主路由任何设置** | S2 ·「手动静态IP方案」 |
| B2-3 | 官方旁路由 DHCP 方案："主路由：任何路由器，默认关闭DHCP，网关设为旁路由IP"；旁路由"开启DHCP，全面接管局域网" | S2 ·「旁路由DHCP方案」 |
| B2-4 | 官方浮动网关方案按设备分配网关靠主路由的"局域网设备管理"，而非互相设网关 | S2 ·「(iStoreOS)浮动网关方案」 |
| B2-5 | 官方**(华硕)浮动网关方案有固件硬依赖**：要求主路由刷 ASUSGO 梅林改版固件"102.4及以上版本" | S2 |
| B2-6 | **iStoreOS 已知缺陷（官方仓库实测报告）**：官方原文"istoreos利用自带的设置向导设置为旁路由时，不会自动关闭DHCP，需要手动勾选忽略此接口。" | S7 · Issue body 第 1 点 |
| B2-7 | 官方原文"即便你手动在DHCP勾选忽略此接口，但是当电脑网卡设置成自动获取IP后，IP是不会获取了，但网关会获取成istoreOS旁路由的IP。"；复测补充"发现有的电脑会获取到网关，有的不会。" | S7 · Issue body 第 2 点、2025-01-18 回帖 |
| B2-8 | 维护者把故障域判给**实际下发租约的 DHCP 服务**："如果istoreos的dhcp服务都关了，那你的电脑获取不到网关跟istoreos有什么关系？应该要去检查dhcp服务啊。" | S7 · jjm2473（Contributor）2025-01-19 回帖 |
| B2-9 | 官方操作顺序（社区总结，与本项目 P0 顺序一致）："先固定旁路由 LAN IP，关闭旁路由 DHCP；再在主路由 DHCP 中下发网关和 DNS；确认普通上网正常后，最后开启透明代理插件。" | S9 · 导语 |
| B2-10 | 单 DHCP 权威原则（社区）："网络里同时出现两个 DHCP 服务时，客户端可能拿到随机网关，表现为有时能上网、有时不行。" | S9 ·「第 2 步」+ 常见问题 |
| B2-11 | 三个下发层次与各自代价（社区）：网关指向旁路由（注意"旁路由故障会影响测试设备上网"）／只改 DNS（"不是所有流量都会进旁路由"）／手动单设备；建议"先只改一台电脑或手机，确认没有问题后，再通过主路由 DHCP 下发给更多设备" | S9 ·「第 3 步」 |

### D1｜多出口与故障转移（mwan3）

| # | Claim | 来源 · 锚点 |
|---|-------|------------|
| D1-1 | 本页为 iptables 版文档："This is documentation for the iptables version of mwan3"，页内指向独立 nftables 文档页 | S6 · 顶部声明段 |
| D1-2 | **官方原文支撑"带宽不叠加"**：`"Linux outgoing network traffic load-balancing is performed on a per-IP connection basis."` 与 `"it is not channel-bonding, where a single connection (e.g. a single download) will use multiple WAN connections."` | S6 · Load balancing 段 |
| D1-3 | 受益边界（官方）：`"load-balancing will help speed multiple separate downloads or traffic generated from a group of source PCs"`，但 `"it will not speed up a single download from one PC"`，除非 `"the download is spread across multiple IP streams such as by using a download manager"` | S6 |
| D1-4 | 四层模型与引用约束（官方）：interface → member → policy → rule；`"For a network interface to be used in mwan3, it must be defined as a member, which can then be used in policies."`；`"Members can't be used for rules directly."` | S6 · Members/Policies/Rules 段 |
| D1-5 | metric 与 weight 语义（官方）：`"Members within one policy with a lower metric have precedence over higher metric members."`；`"Members with the same metric will load-balance."`；`"Load-balanced member interfaces distribute more traffic out those with higher weights."` | S6 |
| D1-6 | 健康探测与失效（官方）：track_ip `"The host(s) to test if interface is still alive. If this value is missing the interface is always considered up."`；`"When an interface goes down, mwan3 deletes all the rules and routes to that interface."` | S6 · Tracking 段 |
| D1-7 | 版本支持口径（官方）：`"mwan3 has not been updated to natively support nftables yet"`；25.12 行 `"It is no longer recommended to use the official mwan3 package at this time, given it is based on iptables"`；24.10 行 `"Unlikely to function properly due to still being iptables based."` | S6 · 版本支持表 |
| D1-8 | nft 版的定位：页面标题 `"mwan3 (nftables unofficial)"`；`"The official mwan3 is the original iptables version maintained by feckert"`；`"Community member dl12345 has ported the original mwan3 codebase to be compatible with nftables"`；`"the nftables version is referred to as mwan3-nft."` | S6a · 版本定位段 |
| D1-9 | nft 版的可用性边界（官方托管页自述）：`"The nftables version of mwan3 is only supported on OpenWrt 25.12 or newer releases."`；`"opkg packages do not exist for the nftables version."`；`"is currently not available in official OpenWrt package feeds"`；需 nftables + firewall4，用 apk 安装 | S6a · Installation 段 |
| D1-10 | 迁移行为：`"apk will perform an upgrade if the older mwan3 iptables version is installed"`，并有 `"a one-time run migration that is automatically triggered on post-install"` | S6a · Migration 段 |
| D1-11 | 配置仍为 UCI `/etc/config/mwan3`，sections 含 `config globals/interface/member/policy/rule/ipset`；差异在 `"All iptables/ipset usage with nftables equivalents"`、新增按源 MAC 建规则、mwan3rtmon 改为 ucode | S6a · Configuration / Changes vs iptables 段 |

### 排错方法论与工具链（贯穿小节）

| # | Claim | 来源 · 锚点 |
|---|-------|------------|
| T-1 | 核心方法论（社区，与本项目流程一致）："不要把订阅、DNS、规则分流和系统代理混在一起排查。先固定变量，只看一层。"判定方式示例为"先测 IP，再测域名" | S9 ·「旁路由常见故障速查」 |
| T-2 | 非对称路径下的现象序列（社区，**作者仅文字描述、未给抓包命令**）：客户端发 SYN → 收 SYN+ACK → 发 ACK → 发 payload →（无回应 ACK）→ 重复收 SYN+ACK → 重传 payload 仍无 ACK | S8 · 抓包序列列表 |
| T-3 | 现象机制（社区归因）："由于服务器回应的SYN + ACK没有经过OpenWrt，使得OpenWrt没有正确追踪TCP连接"，进而"OpenWrt认为客户端后续的数据包是'无效数据包'，并丢弃" | S8 · 机制解读段 |
| T-4 | **社区处置路径一**："在OpenWrt中解决的方法也很简单，首先在'防火墙'页面中关闭'丢弃无效数据包'" | S8 · 修复步骤 1 |
| T-5 | **社区处置路径二**："若OpenWrt通过独立线路（在防火墙的WAN Zone）连接主路由，则在一些特定情况下（比如因为一些组网需求，对一些内网网段开启了masquerade），还要打开WAN Zone – 编辑 – 连接追踪设置 – 允许'无效'流量" | S8 · 修复步骤 2 |
| T-6 | **对应官方条目（缺口 G1 已填）**：T-4 对应全局 `drop_invalid`（boolean，文档默认值 `0`），官方原文 "Drop invalid packets (e.g. not matching any active connection)."；LuCI 界面名 `_('Drop invalid packets')` | SG1-01 · Defaults 表；SG1-02 · defaults 区 |
| T-7 | **T-5 对应的官方条目是 zone 级 `masq_allow_invalid`**（boolean，文档默认值 `0`），官方原文 `"Do not add DROP INVALID rules, if masquerading is used."`，续句 `"The DROP rules are supposed to prevent NAT leakage"`；LuCI 中位于 zone 弹窗的 **conntrack 页签**，界面名 `_('Allow "invalid" traffic')`，说明原文 `"Do not install extra rules to reject forwarded traffic with conntrack state invalid. This may be required for complex asymmetric route setups."` | SG1-01 · Zones 表；SG1-02 · conntrack 页签 |
| T-8 | **纠正**：OpenWrt 官方只存在上述**两个** invalid 相关条目；「zone 级允许无效流量」不是独立的 conntrack 选项，S8 的口头路径对应的就是 `masq_allow_invalid` | SG1-01 · Zones 节正文（反证） |
| T-9 | 抓包工具：双向抓包须分别指定接口，`-i`/`--interface` 官方用途为 "Listen, report the list of link-layer types, … on interface." → **不能用单一接口推断全链路** | SG3-01 · `-i` 条 |
| T-10 | 握手判定依据（官方）：_Tcpflags_ 为 "some combination of S (SYN), F (FIN), P (PSH), R (RST), U (URG), W (CWR), E (ECE), e (AE) or `.` (ACK)"；官方握手序列原文："1) Caller sends SYN　2) Recipient responds with SYN, ACK　3) Caller sends ACK" → 据此定位 T-2 中缺失的一步 | SG3-01 · OUTPUT FORMAT、Particular TCP Flag Combinations |
| T-11 | 官方示例命令（打印每个 TCP 会话的起止包）：`tcpdump -n 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0'` | SG3-01 · EXAMPLES |
| T-12 | 连接跟踪查看（官方）："You can list the existing flows using the conntrack utility via command:" 后接 `# conntrack -L`；过滤示例 `# conntrack -L -p tcp --dport 993`，"You can filter out the listing without using grep" | SG3-02 · Chapter 5 |
| T-13 | **判定连接是否已被 flowtable 卸载（官方，A4 的直接诊断手段）**："You can identify offloaded flows through the [OFFLOAD] tag when listing your connection tracking table."示例输出含 `... [OFFLOAD] mark=0 use=2`；另一处官方原文："you will observe that the counter rule in the example above does not get updated for the packets that are being forwarded through the forwarding bypass." | SG2-01 · Counters |
| T-14 | conntrack 工具文档自身把 INVALID 与丢弃规则集关联："You have a stateful rule-set that drops traffic in INVALID state." —— 与 T-6/T-7 互相印证 | SG3-02 · Chapter 5 末尾 |
| T-15 | NAT 规则查看（官方）：`iptables -L` 的 `-L` 条原文 "List all rules in the selected chain. If no chain is selected, all chains are listed. Like every other iptables command, it applies to the specified table (filter is the default), so NAT rules get listed by" 后接示例 `iptables -t nat -n -L` | SG3-03 · `-L` 条 |

## 四、矛盾与张力（**必须并列标注，不得裁决或静默合并**）

| # | 分歧 | 一方锚点 | 另一方锚点 |
|---|------|---------|-----------|
| X1 | **TUN vs TProxy 性能优劣方向相反** | C3："tun 性能比 tproxy 差，尽量用 tproxy 吧。" | C4："udp的tun效率高。"／"tproxy在高压环境表现并不好。"／"tproxy不建议常用。" |
| X2 | **模式推荐相反** | C1："TProxy 是最佳选择…优先使用" | C4："肯定是全部tun。tun和docker的兼容性非常好" |
| X3 | **同一帖内部按协议分层结论不同** | C3："tun 性能比 tproxy 差" | C3 同帖："tcp 用 redirect ，udp 用 tun 是最快的" |
| X4 | **社区「主路由与旁路由 LAN 网关互设＝互指」无来源支持，且与本批所有锚点方向相反** | 社区常见说法（本批未取得支持锚点） | S2：手动静态 IP 方案"主路由：任何路由器，默认开启DHCP，不需要其他任何设置"；S9 拓扑表主路由建议"保持不变"，仅旁路由侧单向指向；S7 维护者把故障域指向 DHCP 服务本身。→ **结论**：真正的问题是**下发点在哪**，不是两边 LAN 网关互设 |
| X5 | **默认关哪一侧 DHCP，官方并列而非单一口径** | S2 旁路由 DHCP 方案：主路由"默认关闭DHCP，网关设为旁路由IP" | S9 与 S2 手动静态 IP 方案：关旁路由 DHCP、由主路由统一分配 |
| X6 | **S7 内部对"网关来自谁"归因不一致，线程未收束** | 用户：忽略 DHCP 后仍"网关会获取成istoreOS旁路由的IP" | 维护者："如果istoreos的dhcp服务都关了，那你的电脑获取不到网关跟istoreos有什么关系？" |
| X7 | **mwan3 nft 版的定性不一致** | S6 以姊妹文档口吻链接 nftables 版 | S6a 自述 `"mwan3 (nftables unofficial)"`、社区移植、不在官方 feed |
| X8 | **「配置语法不通用」只部分获证** | 支持：S6 `"mwan3 has not been updated to natively support nftables yet"`；S6a 后端全换 nftables、新增 `config ipset` | 反对：S6a 同页 `"The overall IP rule/route management is largely unchanged."`、`"This documentation has been cloned from the original iptables version"`。→ 证据支持**后端不通用**，不支持**整个 UCI 语法完全不同** |
| X9 | **25.12 选型结论悬空** | S6：25.12 `"It is no longer recommended to use the official mwan3 package at this time"` | S6a：nft 版仅支持 25.12+，但 `"is currently not available in official OpenWrt package feeds"` |
| X10 | **HFO 与 QoS 冲突的表述范围** | S4 官方仅对 **HFO** 说 `"also incompatible with QoS features such as SQM"` | 社区二手摘要称**软件卸载同样与 SQM/QoS 冲突** —— 本批已抓取页面中**未取得逐字锚点**，标 **[未证]**，不作为已确认矛盾 |

## 五、可直接写入笔记的处置建议

1. **A2 章**：用 S1 的 PREROUTING/OUTPUT 与 TProxy 策略路由命令讲清数据路径，用 S3 三条 listener 讲 mihomo 侧的对应关系，然后**显式声明官方缺口**（S3a 只有一行、S1 把旁路由标为"待补充"）——这个缺口本身就是笔记的独家价值。
2. **A4 章**：用 A4-1～A4-4 讲官方对 flow offloading 的定义与代价，用 A4-6～A4-8 讲机制层证据（"bypasses … any of the Netfilter hooks coming after ingress"），再给出 A4-9 的推断并**明确标注为推断**。不要写"官方说会绕过 NFQUEUE"。
3. **A4 的可验证判据**（本笔记最有实操价值的一点）：`conntrack -L` 输出中带 `[OFFLOAD]` 标签的连接即已被卸载（T-13）；配合"计数器不再增长"做交叉验证。
4. **B1 章**：B1-1～B1-6 全部可用官方原文，tag 写法用 S5a 官方段 + S12 实测渲染结果交叉印证。注意区分 `dhcp_option_force`（S5 有正式条目，since 18.06）与 S5a 的 `dhcp.lan.force="1"`（跳过竞争 DHCP 检查，**语义完全不同**）。
5. **B2 章**：以 S2 的 5 种官方方案为骨架（而不是社区常说的"三档"），把 S7 的真实缺陷作为官方方案的已知反例；X4 单独用一句话点明"互指"说法缺乏来源支持，并给出真正的判据是**下发点**。
6. **D1 章**：D1-2 的"not channel-bonding"**有官方原文支撑**，可以直接写"官方明确说这不等于链路绑定"；但把它表述为"策略路由不等于带宽叠加"属于 [推断]（原文主语是 load-balancing，全文无"策略路由"字样）。版本选型按 X9 呈现为悬空结论，不要给出单一推荐。
7. **排错小节**：以 T-1 的方法论开篇，用 T-10/T-11/T-12/T-15 给出**有官方锚点的命令**，用 T-6/T-7 把 T-4/T-5 的社区口头路径转成官方条目名，用 T-13 收尾。**T-3 的 conntrack 归因必须保留 S8 作者自述**："具体conntrack的工作方式和该问题的出现条件，有待进一步验证"——不得升级为确定结论。

## 六、未填补 / 待复核

### 未填补

1. **`dhcp_option_force` 在旁路由场景的实测行为**：S5 只有定义，无任何来源给出"客户端未请求 option 6 时强制下发 DNS"在代理客户端的实测结果。
2. **tag 段与 force 的组合语义无文档锚点**：仅由 dnsmasq.init 源码支撑（tag 段读布尔 `force`，而 `dhcp_option_force` 列表走 pool 路径）→ 标 [推断]。
3. **DHCP 租约续期与旁路由宕机后的故障切换行为**无来源覆盖。
4. **双栈网关竞争**（RA + DHCPv6 + DHCPv4 并发下发）无来源覆盖。
5. **mwan3 与旁路由场景无交集**：S6/S6a 不涉及单臂旁路由与非对称上下行；S9 明确排除"多出口负载"。→ D1 与排错小节之间**缺少可引用的官方桥接材料**，只能靠 [推断] 连接。
6. **IPv6 DNS 是否可用 dhcp_option 下发**：S5 的 odhcpd 条目只说 "Only IPv6 addresses are accepted. To configure IPv4 DNS servers, use dhcp_option."，**未见"IPv6 DNS 不能用 dhcp_option"的官方明确表述** → 该说法标 [未证]。本轮不做 IPv6，仅记录。
7. **无一手定量性能数据**（TUN vs TProxy 吞吐/CPU）。

### 待人工复核（因 Anubis 拦截，引文经渲染提取）

- S4 的 `"not channel-bonding"` 与 SFO/HFO 三条引文
- S5 的 `"3,192.168.1.1 6,192.168.1.1"` 与 `dhcp_option_force` 条目
- S6 的 `"not channel-bonding"` 句与版本支持表
- SG1-01 的 `masq_allow_invalid` 原文

### 已被推翻、不得写入的引用

| 原引用 | 问题 |
|--------|------|
| `openwrt.org/docs/guide-user/base-system/dnsmasq` | 页面不存在（官方 wiki 空页）→ 已改用 S5/S5a |
| `github.com/dl12345/mwan3` 当 mwan3 官方 README | 该仓库是 nftables 移植分支。**补充精确化**：S6a 官方托管页确实署名 `"Community member dl12345 has ported the original mwan3 codebase"`，即该仓库是官方页承认的移植来源，但**权威文档面是 wiki 的 `mwan3-nft` 页**，引用须写 wiki 页并标注 unofficial |
| DeepWiki `qichiyuhub/rule`、`nikkinikki-org` 的 `TPROXY High / TUN Medium` 对比表 | AI 聚合页，来源可信度不足，不作为锚点 |

## 七、下游交接（给 outline-generator / chapter-writer）

**素材规模**：Tier 1 官方/一手 21 条 + Tier 3 社区 7 条；claim 记录 66 条；已确证矛盾 10 组；未填补缺口 7 项。

**建议章节骨架**（3 级以内，与 P1 方向一致）：

```
第 1 章 三种接管模式：REDIRECT / TProxy / TUN 的数据路径   ← A2（含官方缺口声明）
第 2 章 硬件加速：为什么代理会静默失效                      ← A4（含 [OFFLOAD] 可验证判据）
第 3 章 网关与 DHCP 下发体系                                ← B2+B1（S2 五方案骨架 + S7 真实缺陷）
第 4 章 多出口与故障转移：mwan3 的四层模型                  ← D1（版本选型按悬空结论呈现）
第 5 章 排错：单变量方法论与工具链                          ← T 组（命令均有官方锚点）
```

**写作硬约束**（下游不得违反）：

1. 凡标 **[推断]** 的内容，正文必须显式标注"这是推断"；凡标 **[未证]** 的必须说"未找到来源支持"。
2. 标 X1～X10 的矛盾**必须并列呈现双方锚点**。特别是 X1/X2/X3：不得给出"TUN 更好"或"TProxy 更好"的单一结论。
3. 「旁路由没有权威单一文档」是本笔记的核心论点之一，须在第一段就立起来，并用 A2 的官方缺口（S3a 仅一行、S1 标"待补充"）作为证据。
4. 不得引用第六节"已被推翻"表中的任何来源。
5. 社区来源（S8/S9/S12/C1–C4）引用时须标注为社区经验；S9 无署名与发布日期，不得作为配置语义依据。
6. 引用 S8 的 conntrack 归因时，必须一并给出作者自述的"有待进一步验证"。
