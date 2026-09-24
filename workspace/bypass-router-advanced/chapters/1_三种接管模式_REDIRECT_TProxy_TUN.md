# 第 1 章 三种接管模式：REDIRECT / TProxy / TUN 的数据路径

在动手调任何一条 iptables 规则之前，先接受一个事实：**「旁路由」这一层不存在权威单一文档**。OpenWrt、mihomo、MosDNS 的官方文档只覆盖到组件层，而「旁路由究竟该怎么接管流量」的实践写法主要来自社区事实标准——本章 1.3 会给出两个可直接核验的官方缺口作为证据。这一章要回答的问题是：透明代理到底在数据路径的哪一点接管流量，REDIRECT / TProxy / TUN 三种模式各自付出什么代价，以及为什么社区对选型的口径收束不了。

## 1.1 透明代理的接管点与回程路径

透明代理的定义来自 Project X（XTLS）官方文档：「透明代理简单地说就是不让被代理的设备感觉到自己被代理了。」[^c1-s1] 被代理设备上无需运行任何代理软件，所有接管动作都发生在网关这一跳——也就是你要配置的旁路由。

局域网设备上网时，数据包的走向是固定的三段链：

```text
局域网设备：客户端   ──► [PREROUTING] ──► 路由决策 ──► [FORWARD] ──► [POSTROUTING] ──► 公网
网关本机：  本机进程 ──► [OUTPUT]（不经过 PREROUTING） ──► [POSTROUTING] ──► 公网
```

官方文档把这层操作讲得很直接：「通过使用 iptables 操控PREROUTING链 和OUTPUT链的流量走向，转发到 Xray，就可以代理局域网设备和网关本机。」[^c1-s1] 注意这里点了两条链：局域网设备的转发流量走 PREROUTING，网关本机自己发出的流量走 OUTPUT。

真正容易被忽略的是**回程也走 PREROUTING**。官方原文：「虽然网关访问公网 IP 不需要经过PREROUTING链，但被访问的服务器向网关返回信息时要经过PREROUTING链，且这部分被转发到 Xray 了」[^c1-s1]。这段话是理解非对称路径的直接锚点：同一台设备的去程与回程可能经过不同的链，第 5 章的排错会用到它。回程不对称与 MASQUERADE 的必要性属于基础原理，本笔记不重复展开，参见既有笔记 [[软路由教程/旁路由原理详解]]。

> [!tip] 大白话
> 把 PREROUTING 想成路由器的入口闸机：凡是「从网线进来」的包——无论是局域网机器要往外发的，还是公网服务器回应的——都得先刷这道闸。所以代理只要守在这道闸上，就能同时截住「去」和「回」两个方向；而路由器本机自己发的包不走入口闸，走的是 OUTPUT 这条专用通道。所以下面 TProxy 才需要额外用策略路由绕一圈。

## 1.2 三条路径的机制差异：REDIRECT / TProxy / TUN

mihomo 官方把「透明代理与系统接管」归为一类，其中包含 Redirect / TProxy / TUN 三种 listener[^c1-s3]。

**REDIRECT**：XTLS 官方已判定它过时——官方推荐的教程中有一篇被直接标注为「是基于 iptables-redirect 模式，已经过时了，不建议使用」[^c1-s1]。它的机制本身在 netfilter 官方 iptables-extensions man page 里写得很清楚[^c1-sa2-01]，逐条拆开是这样：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| 在哪生效 | 「This target is only valid in the nat table, in the PREROUTING and OUTPUT chains, and user-defined chains which are only called from those chains.」 | 只认 `nat` 表，只认 PREROUTING / OUTPUT 两条链（以及从这两条链调用的自定义链）；写在别的表或别的链上不生效 |
| 怎么改包 | 「It redirects the packet to the machine itself by changing the destination IP to the primary address of the incoming interface」 | 把目的 IP 改写成「入接口的主地址」，于是包被交回本机自己 |
| 本机发出的包 | 「locally-generated packets are mapped to the localhost address, 127.0.0.1 for IPv4 and ::1 for IPv6」 | 本机自己产生的包映射到回环地址（IPv4 是 127.0.0.1，IPv6 是 ::1） |
| 改目的端口 | 「This specifies a destination port or range of ports to use: without this, the destination port is never altered.」 | `--to-ports` 用来指定改成哪个端口；不写它，目的端口原样不动 |
| 端口随机化 | 「If option --random is used then port mapping will be randomized (kernel >= 2.6.22).」 | 加 `--random` 让端口映射随机（内核 ≥ 2.6.22） |
| IPv6 | 「IPv6 support available starting Linux kernels >= 3.7.」 | IPv6 支持从内核 3.7 起 |

一句话概括：**REDIRECT 做的事就是「把本该发给别人的包，在 nat 表里改成发给我自己」**——透明代理在本机监听对应端口，接住的就是这批被改回本机的流量。

> [!warning] 一个常被读错的地方：那句「只对 tcp/udp/dccp/sctp 有效」管的是 `--to-ports`，不是 REDIRECT 本身
> man page 里「This is only valid if the rule also specifies one of the following protocols: tcp, udp, dccp or sctp.」这句话，**排在 `--to-ports` 选项的说明之下**（MASQUERADE 的 `--to-ports` 也一样），**不是 REDIRECT target 的协议限制**——man page 没有对 target 本身规定协议范围。
> 说人话：**只有当你打算改写目的端口时，规则才必须同时限定 tcp / udp / dccp / sctp 之一。** 读成「REDIRECT 只能处理 TCP」，就是把选项的约束张冠李戴到了整个 target 上。

顺着这个层次，就能看清一条流传很广、但站不住的说法：社区常说「redir 模式只支持 TCP，UDP 必须用 TProxy」——本批素材**未找到来源支持**，标 **[未证]**。原因正是层次错位：官方 man page 界定的是 **target 层**的行为，而「redir 模式的协议范围」属于**配置方案层**，官方在这一层没有给过定义。所以两种写法都不能写：既不能说「官方说 REDIRECT 支持 UDP」，也不能说「官方说 REDIRECT 只支持 TCP」。

**TProxy**：官方原文指出「iptables-tproxy 不支持对OUTPUT链操作，但是我们可以通过配置策略路由，把OUTPUT链中相应的包重新路由到PREROUTING链上。」[^c1-s1] 这就是 TProxy 需要策略路由的前提——它必须把本机出向的包「骗」回 PREROUTING，才能一起接管：

```bash
# 把带 fwmark 1 的包交给自定义路由表 100
ip rule add fwmark 1 table 100
# 让该表把所有目标地址都当作本机地址（local）、从 lo 交付，重新进入 PREROUTING
ip route add local 0.0.0.0/0 dev lo table 100
```

> [!tip] 大白话
> 把这三条路径想成在同一栋楼里装三种「截流闸」：REDIRECT 是已经贴了作废通知的老闸（官方明确不建议再用）；TProxy 是守在入口闸、靠给包打标记（fwmark）来分流的闸；TUN 则是自己在楼里新拉一条虚拟专线（虚拟网卡），把系统流量整条引过去。所以三者的差别不在「能不能代理」，而在「从哪一点、用什么手段把流量抠出来」。

官方文档同时留下一句常被误读的话：iptables 方案「由于其比 tun2socks 更高效率以及适合在路由器中配置而广泛使用。」[^c1-s1] **这里必须澄清：这句话的比较对象是 tun2socks，不能据此写成「iptables 方案比 mihomo TUN 效率更高」。**

**TUN**：官方把 TUN 分为两个入口，并给出明确分工——「顶层 `tun` 配置用于接管系统流量，适合需要自动路由、DNS 劫持或按应用分流的场景。」而「Listener 中的 TUN 面向高级使用场景。普通用户应优先使用顶层 TUN 配置。」[^c1-s3][^c1-s3b] 栈的选择上，官方建议「如无使用问题，建议使用 `mixed`栈，默认 `gvisor`」[^c1-s3c]。此外 `auto-redirect` 条目写明它「仅支持 Linux，自动配置 iptables/nftables 以重定向 TCP 连接，需要`auto-route`已启用」，`gso` 则「启用通用分段卸载，仅支持 Linux」[^c1-s3c]。

## 1.3 官方文档的结构性缺口

需要先厘清：官方并非全无定义——上一节引用的 SA2-01 已把 REDIRECT target 的语义写清。缺位的是上面那一层：把 target、fwmark、策略路由与代理侧 listener 接成一条可用链路所需的**配置规则层**。两个缺口都可核验：

1. **mihomo 官方 TProxy 页全文只有一行字段说明**（内容仅为「是否监听 UDP」），完全不给 iptables/nftables 规则、fwmark 与策略路由前提——而这些前提只存在于 XTLS 的透明代理文档[^c1-s3a][^c1-s1]。
2. **XTLS 官方把「主路由、单臂路由与旁路由」以及「避免已有连接的包二次通过 TPROXY」明确标为「待补充...」**[^c1-s1]。

结论是事实陈述而非推断：**透明代理接管的配置规则层**在一手文档中是缺位的，社区实践填补了它。这正是开篇「旁路由不存在权威单一文档」的直接证据，也是其根因。

> [!tip] 大白话
> 把官方文档想成产品说明书：零件列得很全（有哪几种 listener、字段什么意思），却没写「这些零件怎么接线才能装到旁路由」。所以能跑的旁路由配置，多是社区拼出来、互相抄的。

## 1.4 选型：社区口径为什么不收束

既然权威写法缺位，选型就只能依赖社区经验——而社区口径是矛盾的。下面三组分歧必须并列呈现双方锚点，**本笔记不给「TUN 更好」或「TProxy 更好」的单一结论**。

**X1：TUN 与 TProxy 的性能方向相反。** 一方（社区经验，C3）称「tun 性能比 tproxy 差，尽量用 tproxy 吧。」[V2EX 讨论帖](https://global.v2ex.co/t/1086272)；另一方（社区经验，C4）则称「udp的tun效率高。」「tproxy在高压环境表现并不好。」「tproxy不建议常用。」[ha0wen 博客](https://www.ha0wen.top/archives/2567)。

**X2：模式推荐相反。** 一方（社区经验，C1）主张「TProxy 是最佳选择…优先使用」[openyq 博客](https://blog.openyq.top/posts/23739/)；另一方（社区经验，C4）则主张「肯定是全部tun。tun和docker的兼容性非常好」[ha0wen 博客](https://www.ha0wen.top/archives/2567)。

**X3：同一帖内部按协议分层，结论都不同。** C3 先说「tun 性能比 tproxy 差」，同帖又说「tcp 用 redirect ，udp 用 tun 是最快的」[V2EX 讨论帖](https://global.v2ex.co/t/1086272)。

这组分歧之所以收束不了，还有一个更硬的原因：本轮检索中该项**未找到来源支持**——没有任何官方或可信一手实测给出 TUN 与 TProxy 的吞吐或 CPU 占用对比数据（**[未证]**）。也就是说，根本不存在一个可以用来终结讨论的数字锚点，读者只能按自己的场景（UDP 占比、是否跑 Docker、CPU 强弱）自行权衡。

> [!tip] 大白话
> 把社区选型讨论想成「同一道菜、不同厨师给的配方」：有人说火大点好、有人说小火稳，谁都没给称过重的数据。所以当你看到某篇教程斩钉截铁地推荐某一种模式时，先问一句「它有实测数字吗」——按本章的检索结果，大概率没有。

## 小结

- 透明代理的接管点是网关这一跳；局域网设备去程走 PREROUTING → FORWARD → POSTROUTING，**回程同样要过 PREROUTING**，这是非对称路径的根源。
- REDIRECT 官方已判定过时；TProxy 依赖策略路由把本机出向流量绕回 PREROUTING；TUN 官方分顶层与 listener 两个入口，并建议 `mixed` 栈。
- 「iptables 方案更高效」的比较对象是 tun2socks，不能等同于「比 mihomo TUN 更快」。
- 官方文档在接管规则层是缺位的（TProxy 页仅一行、XTLS 页标「待补充」），这正是「旁路由没有权威单一文档」的证据。
- X1/X2/X3 三组分歧双方锚点并列，且无一手定量性能数据，选型不存在标准答案。

下一章转向一个会让上面这套模型「静默失效」的机制：硬件加速（flow offloading）在数据路径的哪一点跳过了 Netfilter，从而让依赖 NFQUEUE 的透明代理拦不到已建立连接的后续包——并给出一个可现场验证的判据。

[^c1-s1]: Project X (XTLS) 官方文档《透明代理》，https://xtls.github.io/document/level-2/transparent_proxy/transparent_proxy.html
[^c1-s3]: mihomo 官方文档《Inbound》，https://wiki.metacubex.one/config/inbound/
[^c1-s3a]: mihomo 官方文档《TProxy listener》，https://wiki.metacubex.one/config/inbound/listeners/tproxy/
[^c1-s3b]: mihomo 官方文档《TUN listener》，https://wiki.metacubex.one/config/inbound/listeners/tun/
[^c1-s3c]: mihomo 官方文档《TUN 配置》，https://wiki.metacubex.one/config/inbound/tun/
[^c1-sa2-01]: netfilter 项目官方站点 iptables-extensions man page，https://ipset.netfilter.org/iptables-extensions.man.html
