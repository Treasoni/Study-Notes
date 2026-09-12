# 第 7 章 排错：按顺序查，别猜

第 6 章你跑过六步验收，如果没过，这一章给你用。排错最怕的不是问题难，而是上来就回头改 SNAT、或去 HAOS 上跑 `sysctl`。正确做法是按固定顺序逐项排除，先定位到具体一环，再动手。

## 7.1 路由根本没出现在客户端的路由表里

最典型的失败：客户端上 `ip route` 或 `netstat -rn` 里压根看不到 `192.168.1.0/24`。先不要怀疑 HAOS，按官方 [Route injection 文档](https://tailscale.com/docs/reference/route-injection) 的 Troubleshooting 顺序查：

```bash
# 1. 在子路由节点上确认它确实在 advertise
tailscale status --json

# 2. 去管理端确认这条路由已被 approve
#    Machines → 找到 homeassistant → Edit route settings → Subnet routes 勾选

# 3. Linux 客户端：确认自己接受了路由（其他平台默认接受）
tailscale debug prefs          # 看 RouteAll 是不是 true
tailscale set --accept-routes  # 若为 false，用这条打开

# 4. 客户端：看是否有更具体的本地路由抢了优先级
ip route        # Linux
netstat -rn     # macOS
```

这正是第 5 章四个注入条件里的前三条：advertise、approve、accept。官方还提醒：客户端不会主动 ping 路由器来发现路由。

> [!tip] 大白话
> 路由像快递地址库：节点报备「我能送到 192.168.1.0/24」，管理端 approve 是总部盖章，客户端 accept 是收件点同意接收。缺一步地址库就是空的。

## 7.2 路由在、隧道也通，但目标不通

路由已出现在客户端，`tailscale ping` 到 HAOS 的 tailnet IP 也通，但访问 `192.168.1.50` 就是不行。这时包进了隧道却被丢了，官方给的三步：

```bash
# 1. 看生效的包过滤规则（ACL / grants），检查 PacketFilter 段
tailscale debug netmap
```

2. 确认目标从子路由节点本机可达——在 HA 终端 ping 一下目标，先排除目标自己掉线。
3. 检查子路由节点或目标设备上的防火墙。

这里要把两件事分开：**路由控制哪些包进隧道，访问控制决定哪些包被放行**。官方原文：`Grants control packet filtering, while routes are injected based on what subnet routers advertise and what the control plane approves.`

> [!tip] 大白话
> 路由是「这条路通不通到家」，ACL 是「门口保安放不放你进」。路修好不等于能进门。

## 7.3 路由和 ACL 是两套东西

第 5.1 节的这个误解到排错阶段就成了判断依据。官方两个反直觉例子：

- 子路由广告了 `10.0.0.0/8` 但没有 grant 覆盖：客户端**会**拿到路由，流量进隧道后被包过滤丢掉。原文：`If a router advertises 10.0.0.0/8 but no grant covers it, clients receive the route but traffic is dropped by the packet filter.`
- 反过来，允许 `192.168.0.0/16` 的 grant **不会**额外注入任何路由：`A grant allowing 10.0.0.0/8 does not cause additional routes to be injected.`

一句话：`You can have a route without ACL access (packets enter the tunnel but are dropped by the filter), or ACL access without a route (packets never enter the tunnel).` 两条都得有。这一节是「避免在错误的地方改配置」——路由没出现回 7.1 查 advertise / approve / accept，路由出现但走不通再来查 ACL。

## 7.4 HAOS 特有的坑

### 7.4.1 key 过期导致 fail-close

连接器（connector，子路由、exit node、app connector 都算）的 key 过期后，它的路由在**其他设备上仍然保留，但变得不可达**。官方 [Subnet routers 文档](https://tailscale.com/docs/features/subnet-routers) 把这条行为叫 "fail close"：`When a connector's ... key expires, the connector's advertised routes remain configured on other devices but become unreachable (known as "fail close" policy). Tailscale keeps these routes in place intentionally because removing them could leak traffic to untrusted networks.`

这是官方**有意为之**，不是 bug——路由故意不撤，免得流量泄漏到不可信的网络（fail-close，像消防通道被反锁：门还挂在那儿却推不开）。定位动作很简单：把「最近有没有到期或重新认证」当成固定检查项。预防办法见第 2 章和第 4.3 节——关闭该节点的 key 过期，或配置高可用。

### 7.4.2 排错前先关掉日志压制

`log_suppression` 默认开启，作用是「在 200 行之后开始压掉插件日志」。官方原话：`Turn it off only in case you are troubleshooting, because Tailscale is quite chatty.` 日志很啰嗦，平时压掉是好事；但排错时线索恰藏在被压掉的部分里，所以先关掉它：

```yaml
log_suppression: false
```

改完记得重启插件（这和第 4.2 节的总原则一致）。

### 7.4.3 `sysctl` 报 `Read-only file system`（警告① 的报错现场）

如果你照 Linux 子路由教程走了第 2 步，会看到：

```text
[core-ssh ~]$ sysctl -p /etc/sysctl.d/99-tailscale.conf
sysctl: error setting key 'net.ipv4.ip_forward': Read-only file system
sysctl: error setting key 'net.ipv6.conf.all.forwarding': Read-only file system
```

这不是配置错误，是路径错误——你根本不该在 HAOS 上做这一步。维护者回复只有一句：`Please read the docs, it says "follow steps from step 3", because what you want to configure, is already set.` 你想配的 IP forwarding，插件已经代做了。官方 DOCS.md 也写明插件已替你处理 "IP address forwarding" 和 "Clamp the MSS to the MTU"（见第 4.2.1 节）。

> [!warning]
> 看到 `Read-only file system` 就去搜 remount、想把根文件系统挂成可写，是野路子。这一步在 HAOS 上本就不该存在，绕过去只会破坏受管系统完整性。

### 7.4.4 DNS loop 会让 `hassio_dns` 崩溃

这一节接第 3.4 节那条 `ha dns options --servers dns://100.100.100.100` 命令。它默认是好的，但有一个已知的严重后果：MagicDNS 解析不了某个名字时，**不返回 REFUSED、SERVFAIL 或 NXDOMAIN**，而是回头去问系统原本的 DNS。HA 上那个「原本的 DNS」就是 `hassio_dns`——你又把 `100.100.100.100` 配成它的第一顺位，于是形成 loop，`hassio_dns` 崩溃，连带 supervisor、nginx 出问题。维护者贴出的 coredns 日志原文：

```text
[FATAL] plugin/loop: Loop (172.30.32.1:51675 -> :53) detected for zone ".", see https://coredns.io/plugins/loop#troubleshooting. Query: "HINFO 3773484566690024990.644798792321423444."
[01:09:56] WARNING: Halt DNS plug-in with exit code 1
```

`accept_dns: false` **不是**解法。维护者明确说它会把控制台下发的全局 nameserver 一起废掉：`permanent accept_dns=false disables the DNS config's magical modification, but also disables accepting configured global nameservers by 100.100.100.100 from TS admin page, they won't be called, it would break things.`

维护者一开始的结论是「干脆全局关掉 MagicDNS」，但**第二天自己推翻了**，因为会连带影响普通客户端：`disabling MagicDNS is fine for HA (or other "linux" servers with manual net configs), but bad for general (even DHCP based) win/linux clients -> better figure out how MagicDNS interferes with hassio_dns than to disable it completely`。关掉后 Ubuntu / Win11 连完整域名的解析都会失效。

最后一条安抚性结论：插件停止时，HA 里的 `100.100.100.100` 会被**跳过**，不会导致 DNS 全挂，维护者对此回答 `Yes, will skip it. Tested.` 排查动作：先 `ha dns info` 确认 `servers: []`；要清空列表按官方文档用 `ha dns reset` 加 `ha dns restart`，两条都要执行。

## 7.5 四种常见误判，以及一个不要当步骤的「怪招」

**误判一：把 exit node 当子路由用。** 子路由只暴露指定网段、不影响上网流量走向，exit node 接管设备全部出站流量，像消费级 VPN。插件里它们是两个独立选项（`advertise_routes` 与 `advertise_exit_node`），在控制台的 Edit route settings 下分开授权。别用 exit node 实现「访问家里局域网」。

**误判二：把 HAOS 主机本地优先当故障。** 回到第 6.2.1 节。官方原文：`In case your local subnets collide with subnet routes within your tailnet, your local network access has priority, and these addresses won't be routed toward your tailnet.` 这是防止 HA 失联的设计，收益对象是远程 tailnet 设备，不是 HA 主机自己。

**误判三：局域网内的 Linux 节点自己掉线。** 症状是 **tailnet IP 通、LAN IP 不通、从局域网内 ping 100% 丢包**。这不是 HAOS 的问题，是那个节点接受子路由后，回包被抢走改走 `tailscale0`（第 4.5 节的非对称路由）。在那台节点上查：

```bash
ip rule show
ip route show table 52
ip route get <目标> from <源>
```

判定标准：`ip route get` 对局域网目标返回 `tailscale0` 而非 `eth0` / `wlan0` 就命中了。关于「HAOS 自带更高优先级的本地路由保护规则」，来源只有一篇非官方个人博客、未获官方印证，如实标注待核实。

> [!tip] 大白话
> 非对称路由好比寄信：去信走家门口的路（LAN），回信却被导航带上另一条高速（tailscale0）。两边都「通」，但收信人等不到回信，看上去就是丢包。

**误判四：让上游路由器参与转发时，回包丢失。** 出向（LAN → tailnet）能通，回包丢。维护者亲述过这个坑：`when I used the router to route toward my TS subnet router, while outgoing (LAN->tailnet) connections worked fine, I lost the returning/reply packets from the LAN back to the tailnet (different path for the returning packets, they go through the router, while the original packages from the tailnet was sent by the TS subnet router directly to the non-TS device), but this was a firewall issue`。所以多半是路由器/防火墙配置，不是 HAOS 的锅。

最后两个收尾要点。其一，「能 ping 通但网页卡死」多半是上游丢弃 UDP：先查 `41641/udp` 与端口转发，官方说明它是 `UDP port to listen on for WireGuard and peer-to-peer traffic.`，并建议用 `tailscale ping <hostname-or-ip>` 测直连。仍不行才考虑兜底：

```yaml
always_use_derp: true
```

官方口径要保留：`Basically you will never want to enable this option.` 其二，网上流传的「先启用再关闭 `userspace_networking` 才生效」标为**社区个案**——对应 issue 官方已 `closed as not planned`，只作现象记录，不作操作步骤。

## 本章小结

- 路由没出现，按 advertise → approve → accept → 本地路由优先级 顺序查，先别怀疑 HAOS。
- 路由在但流量不通，查 ACL / grants（`tailscale debug netmap` 的 `PacketFilter`）、目标可达性、防火墙；路由和 ACL 两套机制缺一不可。
- HAOS 特有坑：key 过期会 fail-close；排错先关 `log_suppression`；`Read-only file system` 是路径错误；DNS loop 别用 `accept_dns: false` 或关 MagicDNS 去解。
- 四种误判里只有「上游路由器参与转发导致回包丢失」可能真涉及路由器配置。

下一章收尾：讲清范围边界、未核验声明，以及什么时候才真正需要 site-to-site。
