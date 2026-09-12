# 第 6 章 验收：你自己跑一遍六步

前五章你都在配置，这一章只做一件事：证明它到底通没通。结论得你自己跑出来，本篇给的是可执行路径，不是成功率保证。

## 6.1 把测试环境摆对

两个变量先固定住，否则第 5 步失败时分不清是谁的问题。

- 测试端必须是真正在家庭网络之外的 tailnet 客户端。最省事的做法是把手机关掉 Wi-Fi、走蜂窝，它就不可能悄悄从家里局域网绕过去。
- 目标设备要选一台明确没装 Tailscale、平时能从家里电脑 ping 通的设备。打印机、摄像头、路由器管理页面都行——官方把「让远程用户访问打印机、摄像头这类装不了客户端的设备」列为子路由的典型用途。
- 先把目标 IP 记下来，后面每一步都用同一个 IP。官方博客举的例子是：HA 在家里网络的 `192.168.1.50`、对外提供 `192.168.1.0/24` 路由，然后就能访问家里所有设备。

> [!tip] 大白话
> 子路由像给家里开了个「代收点」：远程客户端不用认识打印机，把包交给 HAOS 就行。

## 6.2 六步验收清单，按顺序执行

每步都给出判读标准。失败就停在那一环，别跳步。

**第 1 步 确认已在 advertise。** 在 HAOS 终端跑 `tailscale status --json`——官方排错第一条就是「Verify the subnet router is advertising the routes in the admin console or with `tailscale status --json` on the router.」。再记下它的 tailnet IP，第 4 步要用：

```bash
tailscale ip -4
```

**第 2 步 确认管理端已 approve。** 路径见第 4.3 节；没勾 `192.168.1.0/24`，路由不会下发给任何客户端。顺手复核这个节点没开 key 过期：官方说明连接器 key 过期后，路由在其他设备上仍然保留但不可达，是有意的 fail-close 行为，不是路由丢了。

**第 3 步 确认客户端已 accept routes。** Linux 客户端跑：

```bash
tailscale debug prefs
```

看 `RouteAll` 是否为 `true`，为 `false` 就 `tailscale set --accept-routes`。Windows / macOS / Android / iOS / tvOS 默认接受，Linux 默认不接受。

**第 4 步 先证明隧道本身通。** 从客户端 ping HAOS 的 tailnet IP（第 1 步记下的那个）：

```bash
tailscale ping <hostname-or-ip>
```

**第 5 步 最终验收。** 从客户端 ping 局域网目标 IP，换成你 6.1 记下的那个地址：

```bash
ping 192.168.1.50
```

这条通了，子路由才算成。

**第 6 步 反向确认。** 回到 HAOS 上，确认它自己能不能访问那台目标设备。能，问题就被限定在「客户端 → 隧道 → 转发」这条链路上，而不是目标设备本身下线了——官方排错第二条是「Confirm the destination is reachable from the subnet router itself.」。

#### 6.2.1 警告③：HAOS 主机自己不走隧道，是设计不是故障

你几乎一定会在 HA 终端里发现：访问 `192.168.1.x` 并不经过隧道，看起来像路由没生效。官方原文是：

> "In case your local subnets collide with subnet routes within your tailnet, your local network access has priority, and these addresses won't be routed toward your tailnet. This will prevent your Home Assistant instance from losing network connection. This also means that using the same subnet on multiple nodes for load balancing and failover is impossible with the current app behavior."

推论很清楚：子路由的收益对象是**远程 tailnet 设备**，不是 HA 主机自己；代价是无法用同网段做负载均衡与故障转移。别把这条现象当故障。

## 6.3 把结果记下来

把每一步的结论写进一张表，失败时你会立刻知道停在哪：

| 节点名 | 是否 advertise | 是否 approve | 客户端平台 | 是否 accept | 隧道是否通 | 局域网 IP 是否通 | 失败时停在第几步 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

> [!warning] 诚实声明
> 本篇结论由官方文档，加上维护者在**两种 HAOS 部署形态**（树莓派实机 + VirtualBox 虚拟机）上的实测背书。但他测的是**双向 site-to-site**，不是你这套同网段单向场景，原话是 "it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config."。请以你自己的实测为准，不要期待「必定成功」。

验收不通过就直接进第 7 章，按顺序查，不要回头乱改 SNAT。
