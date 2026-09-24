# 第 4 章 多出口与故障转移：mwan3 的四层模型

前三章都默认出口只有一个：第 1、2 章讨论包在转发路径上被谁接管、会不会被硬件加速绕过，第 3 章讨论客户端的网关由谁下发。这一章把「出口」本身变成变量——一台主机或一个局域网要按策略走不同出口，并在某个出口故障时自动切换，OpenWrt 用 mwan3 表达这件事。要回答四个问题：它的四层模型如何互相引用、健康探测的默认语义埋了什么坑、它到底能不能叠加带宽，以及在旁路由场景里它管到哪一步为止。

## 4.1 四层模型与引用约束

mwan3 官方文档开篇先划版本：**"This is documentation for the iptables version of mwan3"**，并在页内指向一份独立的 nftables 文档页[^c4-s6]——这一点 4.4 节展开。官方把配置关系组织成四层：**interface → member → policy → rule**[^c4-s6]。

引用链是**单向且逐级**的，两条约束必须记住：

- 「For a network interface to be used in mwan3, it must be defined as a member, which can then be used in policies.」——接口本身不能直接用，必须先包成 member，member 才能进 policy[^c4-s6]。
- 「Members can't be used for rules directly.」——rule 只能引用 policy，**不能直接引用 member**[^c4-s6]。

```uci
# /etc/config/mwan3 —— 四层引用链结构示意
# 本片段只画「谁引用谁」的骨架，字段名按官方四层模型，取值以本机配置为准
config interface 'wan1'          # 第 1 层：物理出口
	option enabled '1'

config member 'wan1_m1_w1'       # 第 2 层：接口 + 度量 + 权重
	option interface 'wan1'
	option metric '1'
	option weight '1'

config policy 'balanced'         # 第 3 层：策略（引用 member）
	list use_member 'wan1_m1_w1'
	option last_resort 'default'

config rule 'default_rule'       # 第 4 层：规则（引用 policy，不能直接引用 member）
	option dest_ip '0.0.0.0/0'
	option use_policy 'balanced'
```

> [!tip] 大白话
> 把四层想成点菜：接口是食材，member 是把食材配好的一盘菜，policy 是套餐组合，rule 是「谁点什么」。官方那句 `Members can't be used for rules directly.` 的意思就是——客人只能点套餐（policy），不能直接点后厨的备料（member）。

## 4.2 metric / weight 与健康探测的语义

member 的**排序与均衡**由 metric 决定，官方三句讲全了[^c4-s6]：

| 官方原文 | 语义 |
|---------|------|
| "Members within one policy with a lower metric have precedence over higher metric members." | metric 小的**优先**——这正是主/备与故障转移的表达方式 |
| "Members with the same metric will load-balance." | metric **相同**才进入负载均衡 |
| "Load-balanced member interfaces distribute more traffic out those with higher weights." | weight 大者分到**更多流量**（仅在同 metric 均衡时生效） |

所以同一份配置里，「故障转移」与「负载均衡」不是两个开关，而是**metric 是否相同**这一件事的两种结果。

健康探测另有一处**最容易踩的默认语义**：

- 字段是 `track_ip`，官方释义「The host(s) to test if interface is still alive. **If this value is missing the interface is always considered up.**」[^c4-s6]——不配 `track_ip`，接口**永远被视为 up**，故障转移根本不会触发。
- 一旦接口真的 down：官方原文「When an interface goes down, mwan3 deletes all the rules and routes to that interface.」[^c4-s6]

```uci
# /etc/config/mwan3 —— 为出口配置健康探测
config interface 'wan1'
	option enabled '1'
	list track_ip '1.1.1.1'      # 探测目标；缺省则此接口永远视为 up，故障转移不生效
	list track_ip '8.8.8.8'
```

> [!tip] 大白话
> metric 是排队顺位，weight 是端菜比例，`track_ip` 是点名签到。不签到（不配 `track_ip`）就等于默认全员到齐——你想要的「有人倒下就换人」，永远不会发生。

## 4.3 带宽叠加的边界

官方对「多出口能不能叠加带宽」有明确原句，**主语是 load-balancing**：

> "Linux outgoing network traffic load-balancing is performed on a per-IP connection basis -- **it is not channel-bonding, where a single connection (e.g. a single download) will use multiple WAN connections simultaneously**."[^c4-s6]

（该句已逐字核实，中段过渡符为双减号 `--`。）受益边界官方也给了原文：「load-balancing will help speed multiple separate downloads or traffic generated from a group of source PCs」，但「it will not speed up a single download from one PC」，除非「the download is spread across multiple IP streams such as by using a download manager」[^c4-s6]。

一处**必须点名的措辞陷阱**：把这条结论写成「**策略路由不等于带宽叠加**」，**这是推断，不是官方口径**——D1-2 的主语是 **load-balancing**，官方全文**没有出现「策略路由」字样**，不能让「策略路由」这个词借用官方署名。

> [!tip] 大白话
> 想成多开几条收银台：一群顾客各自排队（多条连接）确实结账更快，但一个顾客手上只有一件货（单条连接），还是只能走一条队。除非他像代购一样把手里的货分成好几单（多 IP 流 / 下载管理器），才吃得到多条队的好处。

## 4.4 版本选型：iptables 版与 nftables 之别

官方 iptables 版页面自认「mwan3 has not been updated to natively support nftables yet」，并在版本支持表里给出两行判断[^c4-s6]：

| 版本 | 已逐字核实的引文 |
|------|----------------|
| 24.10 | "Unlikely to function properly due to still being iptables based. The unofficial port also is not supported on 24.10" |
| 25.12 | 该行**只核实了两个片段**："It is no longer recommended to use the official mwan3 package at this time" 与 "which is no longer the firewall backend of OpenWrt." |

25.12 行的**完整整句未经逐字核实**，本笔记**只分别引用这两个已核实片段，不拼接成一句完整引文**。

**nftables 版是社区移植，不是官方维护。** 官方托管页自述了四点[^c4-s6a]：

| 它自述什么 | 官方原文 | 说人话 |
|-----------|---------|--------|
| 页面标题 | 「mwan3 (nftables unofficial)」 | 标题里就带 unofficial（非官方） |
| 谁维护官方版 | 「The official mwan3 is the original iptables version maintained by feckert」 | 官方 mwan3 就是原始的 iptables 版，维护者是 feckert |
| 谁移植的 | 「Community member dl12345 has ported the original mwan3 codebase to be compatible with nftables」 | 由社区成员 dl12345 把原代码移植到 nftables |
| 新名字 | 「the nftables version is referred to as mwan3-nft.」 | nftables 版称作 mwan3-nft |

它的可用性边界也由官方托管页逐条写明[^c4-s6a]：

| 边界 | 官方原文 | 说人话 |
|------|---------|--------|
| 支持的版本 | 「The nftables version of mwan3 is only supported on OpenWrt 25.12 or newer releases.」 | 只支持 OpenWrt 25.12 及更新版本 |
| 包管理 | 「opkg packages do not exist for the nftables version.」 | 没有 opkg 包 |
| 官方软件源 | 「This version is currently not available in official OpenWrt package feeds」 | 当前不在官方 feed 里 |
| 那要怎么装 | 「…but can be installed with apk manually.」 | 只能手动用 apk 装（此句为页面同义句片段） |
| LuCI 界面 | 「The LuCI package is arch independent.」 | LuCI 界面是独立包（架构无关），可选装 |

**安装方式就按页面实况写**：不在官方 feed，需从 GitHub 手动取 apk，且因包未签名须加 `--allow-untrusted`，否则 apk 会拒绝安装。**页面并未陈述「需 nftables + firewall4」这一依赖，不要替它补上。**

```bash
# nftables 版不在官方 feed，opkg 包不存在；需从 GitHub 手动取 apk
# 包未签名，必须加 --allow-untrusted，否则 apk 会拒绝安装
apk add --allow-untrusted ./mwan3-nft-*.apk

# LuCI 界面是独立包（arch independent），可选装
apk add --allow-untrusted ./luci-app-mwan3-*.apk
```

（具体文件名与版本号以该项目 GitHub 发布页为准，此处不写死。）升级与迁移行为：官方说明「apk will perform an upgrade if the older mwan3 iptables version is installed」，并有「a one-time run migration that is automatically triggered on post-install」[^c4-s6a]。配置**仍是 UCI `/etc/config/mwan3`**，sections 为 `globals` / `interface` / `member` / `policy` / `rule` / `ipset`；差异在于「All iptables/ipset usage with nftables equivalents」、新增按源 MAC 建规则、`mwan3rtmon` 改为 ucode[^c4-s6a]。

**三组悬而未决（X7 / X8 / X9，并列呈现，本笔记不替你裁决）：**

- **X7 定性不一致**：iptables 版文档（S6）以**姊妹文档**的口吻链接 nftables 版；而 nftables 版自述（S6a）是**社区移植、不在官方 feed**[^c4-s6][^c4-s6a]。
- **X8「语法不通用」只部分获证**：支持「不通用」的证据在**后端**——S6「has not been updated to natively support nftables yet」、S6a 后端全换 nftables；但 S6a 同页又说「The overall IP rule/route management is largely unchanged.」，且「This documentation has been cloned from the original iptables version」[^c4-s6][^c4-s6a]。→ 证据**只支持「后端不通用」，不支持「整个 UCI 语法完全不同」**。
- **X9 25.12 选型结论悬空**：S6 称 25.12「It is no longer recommended to use the official mwan3 package at this time」；而唯一的 nft 版**仅支持 25.12+**，却「is currently not available in official OpenWrt package feeds」[^c4-s6][^c4-s6a]。两侧都指向同一个尴尬区间，**本篇不给单一推荐**。

> [!tip] 大白话
> 想成「正版停产、民间改装件只适配新款机型、但还没上架官方商店」：官方版在新系统上不再被推荐，非官方版只支持新系统却要自己 sideload。所以没有「闭眼选一个」的答案——这正是三组分歧只能并列的原因。

## 4.5 与旁路由场景的交集边界

**这一节是推断，标 [推断]。** mwan3 的官方文档（S6/S6a）**不涉及单臂旁路由与非对称上下行**：它默认路由器本身就是多出口的持有者（各 WAN 直连本机）。因此 D1 的机制与第 5 章的排错小节之间，**缺少可引用的官方桥接材料，只能靠推断连接**。

能确定的是机制发生在哪一层：4.1 的四层引用链与 4.2 的「接口 down 则删除到该接口的全部规则与路由」，都是在**本机路由表与规则**层面起作用[^c4-s6]。而单臂旁路由的场景是客户端流量经旁路由转发、且上下行可能走不同路径——这与 mwan3 假设的多出口直连拓扑**不是同一件事**。这层连接本身**缺少官方桥接材料**，本笔记**不用社区材料补白**，也不因此压缩或改窄 D1 的定位：它是「本机多出口」的正确答案，只是「旁路由该不该用它、怎么用」超出了官方文档能背书的范围。

> [!tip] 大白话
> mwan3 像「给本机装的多路配电箱」：它管的是「这台机器自己有多个出口怎么分流」。旁路由是「替邻居转电的中间站」，两者接口不同。官方只写了前者的说明书，所以「旁路由上怎么接这台配电箱」，本章只能推断到这一步、坦白停在这里。

## 小结

- mwan3 是**四层引用链** interface → member → policy → **rule**；member 不能直接被 rule 引用（`Members can't be used for rules directly.`）[^c4-s6]。
- metric 决定主/备与均衡（**相同 metric 才负载均衡**），weight 只在同 metric 均衡时决定分流比例；**不配 `track_ip` 则接口永远视为 up**，故障转移不生效；接口 down 时 mwan3 会删除到它的全部规则与路由[^c4-s6]。
- 官方原文明确 load-balancing「is not channel-bonding」，单个连接不跨多条 WAN；受益边界是「多路独立下载 / 多台源 PC」，单个下载不受益，除非走多 IP 流[^c4-s6]。**把这条写成「策略路由≠带宽叠加」是推断**（官方全文无「策略路由」字样）。
- 版本选型呈**悬空**：24.10 不适用（已核实整句）；iptables 版自认未原生支持 nftables；nft 版仅支持 25.12+ 且不在官方 feed。**X7/X8/X9 并列，不给单一推荐**；引用 nft 版须写 wiki 的 `mwan3-nft` 页并标注 unofficial[^c4-s6][^c4-s6a]。
- **4.5 是推断**：S6/S6a 不涉及单臂旁路由与非对称上下行，D1 与排错小节之间缺少官方桥接材料，本章不补白[^c4-s6]。

多出口与高可用不在既有笔记范围内；如需**系统级选型背景**，见既有笔记 [[软路由教程/主流软路由系统对比与选择指南]]。**D2 浮动网关高可用（VRRP/Keepalived）与 D3 可观测性与性能边界（nlbwmon）本笔记不展开。**

下一章把前四章的机制收束成一套可复现的排错方法：当现象是「有时能通、有时不通」时，如何用单变量方法把问题锁到具体一层，并用有官方锚点的命令验证。

[^c4-s6]: OpenWrt Wiki《mwan3（iptables 版）》，https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3
[^c4-s6a]: OpenWrt Wiki《mwan3 (nftables unofficial)》（标注 unofficial），https://openwrt.org/docs/guide-user/network/wan/multiwan/mwan3-nft
