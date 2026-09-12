# 第 4 章 子路由：把 HAOS 变成 tailnet 的网关

前面几章你已经能让远程设备访问 HA 自己。可家里真正要用的往往是打印机、摄像头、路由器管理页——它们装不了 Tailscale。这一章让 HAOS 当网关，把整个 `192.168.1.0/24` 借给 tailnet 用，网段里的设备一个字节都不用改。

## 4.1 子路由在做什么：一句话和一条边界

子路由的官方定义是：让 tailnet 覆盖那些「不能或无法运行 Tailscale 客户端」的设备：

> "Subnet routers let you extend your Tailscale network (known as a tailnet) to include devices that don't or can't run the Tailscale client."

网关由 HAOS 扮演：你告诉它「`192.168.1.0/24` 归我管」。远程设备要访问 `192.168.1.50`，包先走隧道到 HAOS，再由它用普通 LAN 的方式转给打印机；打印机全程不知道 Tailscale 存在。

还一条容易混的边界：子路由**只暴露指定网段**；exit node 接管的是 **tailnet 设备访问公网的全部出站流量**，官方比作「VPN 服务器」。别顺手打开 `advertise_exit_node`。

> [!tip] 大白话
> 把子路由想成小区门口的快递代收点：快递员（远程设备）只认识代收点（HAOS），不认识你家打印机；代收点负责把包裹送上楼。打印机不用认识快递员，这就是「不用装任何东西」。

## 4.2 本文推荐配置与逐项解释

按下面五项写。**其余选项保持默认，不要一起抄进来**——[插件官方 DOCS.md](https://raw.githubusercontent.com/hassio-addons/app-tailscale/refs/heads/main/tailscale/DOCS.md) 提醒那段示例「不是默认值，别照抄，自己写一份」，你真正要动的只有 `advertise_routes`。

```yaml
accept_dns: true
accept_routes: false
advertise_routes:
  - 192.168.1.0/24
snat_subnet_routes: true      # 默认值，保持不动 —— 本场景的核心
userspace_networking: false   # 默认值，保持不动
```

**`advertise_routes`**：这是**列表**选项，本场景写 `192.168.1.0/24`。2022 年的 [issue #96](https://github.com/hassio-addons/app-tailscale/issues/96) 曾抱怨「插件只能广告一个网段」——那是历史限制，现在的 `advertise_routes` 本身就是列表，当时的诉求已被满足。

**`accept_routes: false`**：两层理由。一是 HAOS 自己不需要别人的网段；更关键的是，它正是防止本机被 peer 广播的子路由劫持的标准手段。官方定义是「接受 tailnet 里其他节点广告的子网路由」，所以准确含义是**本机不用其他 peer 的子路由做出站路由决策**，**不**等于「别人访问不到本机」——远程设备照样能通过这台网关进 LAN。这个区别在 4.5 节会变成一条具体的坑。

其余三项也都默认不动：

- **`accept_dns: true`**：接受控制台下发的 DNS 设置，与第 3 章配合。
- **`snat_subnet_routes: true`**：本章核心，官方描述是「让子网设备看到来自子网路由器的流量，从而简化路由配置」。
- **`userspace_networking: false`**：关闭才有 `tailscale0` 接口。

三项都别动，改完配置记得重启插件。

> [!tip] 大白话
> `accept_routes: false` 就像「本机只认自己的地图，不看别人发来的地图」——它管的是**你出门怎么走**，不是「别人能不能来你家」。很多人把这两件事搞混，才以为关掉它会把远程访问一起关掉。

### 4.2.1 警告①：不要照抄 Linux 子路由教程的第 2 步

[官方 Subnet routers 文档](https://tailscale.com/docs/features/subnet-routers)配 Linux 子路由的第二步是开 IP 转发，给的是这三行：

```bash
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

**这一步假定你有完整可写的 Linux 主机**：能改内核参数、能写 `/etc/sysctl.d/`。HAOS 根文件系统只读，照抄会原样撞到这段报错：

```text
[core-ssh ~]$ sysctl -p /etc/sysctl.d/99-tailscale.conf
sysctl: error setting key 'net.ipv4.ip_forward': Read-only file system
sysctl: error setting key 'net.ipv6.conf.all.forwarding': Read-only file system
```

这不是你配错了，是路径错了。维护者 lmagyar 对[这条报错](https://github.com/hassio-addons/app-tailscale/issues/415)的回复原话是：

> "Please read the docs, it says \"follow steps from step 3\", because what you want to configure, is already set."

插件已经替你做了「IP address forwarding」和「Clamp the MSS to the MTU」，从第 3 步往下做就行。别为绕过只读琢磨 remount（排查见第 7 章）。

### 4.2.2 警告②：不要关 `snat_subnet_routes`

反面示例，**本场景不要执行**：

```bash
tailscale up --snat-subnet-routes=false
```

官方把它定位成只在「进阶 Site-to-site networking（跨多个网络）」时才用：

> "Only disable this option if you fully understand the implications. Keep it enabled if preserving the real source IP address is not critical for your use case."

关掉后源地址会保留成原始设备地址，而 LAN 设备根本不认识 `100.64.0.0/10`，不知道回包该送哪里。官方要求补一条回程路由，把去往该段的流量交给子路由器的 LAN IP，落点只有**设备自身的操作系统 / 你的 VPC 设置 / 你的 DHCP 服务器**三处，且这个 flag「只在 Linux 子路由器上生效」。HAOS 只读，这些你几乎都动不了。

维护者的回复原话是：

> "With `snat_subnet_routes: true` it just works."

事实这样并列，你自己看因果：一边官方说关 SNAT 是进阶 site-to-site 的开关、关之前要「完全理解后果」；另一边失败复现（[#430](https://github.com/hassio-addons/app-tailscale/issues/430)、[#415](https://github.com/hassio-addons/app-tailscale/issues/415)）反复出现在 `snat_subnet_routes: false` 的配置里——#430 就是 `snat_subnet_routes: false` + `accept_routes: true`，结果 tailnet 内的 `100.123.82.54` 通、同网段的 `192.168.1.102` 不通。

> [!tip] 大白话
> SNAT 就像代收点统一换成自己的地址：寄件人（LAN 设备）只认识代收点，回执自然寄回代收点，再由它转给你。关掉 SNAT 等于要求寄件人记住一个从没见过的地址，你得挨家挨户（每台设备、路由器、DHCP）贴说明。家用单点需求，没理由自找麻烦。

## 4.3 在管理控制台授权这条路由

配置写对只是一半。路由不会自动生效，**必须在管理控制台手动批准**，否则永远不会下发到客户端：

1. 打开控制台 **Machines** 页。
2. 找到 **Subnets** 标记，或用 `property:subnet` 过滤器列出所有广告子路由的设备。
3. 选中带 `subnet` 属性的设备，展开 **Subnets** 段。
4. 点 **Edit**，打开 **Edit route settings**。
5. 在 **Subnet routes** 下勾选 `192.168.1.0/24`，**Save**。

顺手复核 key 过期：官方建议给服务器**关闭 key 过期**，省得反复重新认证（第 2 章做过）。

没授权的后果很具体：不是报错，而是**配了没生效**——路由只存在于 HAOS 上，客户端什么都没有。这是第 7 章排错清单的**第 1 顺位**。

## 4.4 「HAOS 做不了子路由」这个说法从哪来

搜索时你一定会撞到矛盾：社区一大堆「HAOS 做不了子路由」的经验帖，官方文档却说默认配置就行。两边都有依据，关键是**它们讲的不是同一件事**。

反方依据有两类。一类是**容器网络路径层面**的质疑：Supervisor 的 `eth0` 默认路由会把回包送回本地路由器，容器里没有通往 `tailscale0` 的出站路由，去程进不去。另一类是**照抄 Linux 教程失败后放弃**——跑 `sysctl` 撞上只读文件系统，失败复现里反复出现 `snat_subnet_routes: false`。

正方不是一句「官方说可以」。维护者 lmagyar 在 [issue #415](https://github.com/hassio-addons/app-tailscale/issues/415) 的实测原话：

> "OK, I've tested meticuously the site-to-site networking (for another reason), and in short, it works flawlessly, no need for any extra iptables rule."
>
> "Test was done with rPIs running HASS OS."
>
> "And tested on a VirtualBox VM running HA-OS: exact same results as with rPI+HA OS: it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config."
>
> "So I think this is not a HASS OS or add-on issue, but a local net/VM config issue."

注意三点：他测的是**两种 HAOS 部署形态**（树莓派实机 + VirtualBox 虚拟机）；测的是**双向 site-to-site**，比「远程单向访问 LAN」**更难**；结论是「能工作」。

而**反方讲「去程进不去 `tailscale0`」，维护者讲「整体链路能通」**——前者质疑容器网络路径的某个环节，后者描述端到端效果；路径层面的疑问不必然导致链路不通。

界面差异也可能出现：不同版本下 Web UI 显示的值与文档不一致。别猜版本号，以装完那一刻配置页的实际值为准，第 5 章给校验命令。

最后是**引用纪律**：本篇不引用任何未核验来源、也不转述其内容。网上流传的「HAOS 同网段不能跨段转发」求助帖，经核实并不含这个结论，因此不作为证据出现。

## 4.5 同网段专属警告：别把同一个 LAN 上的其他 Linux 节点搞成非对称路由

这一节专门给同网段场景：你 advertise 的 `192.168.1.0/24`**正是 HAOS 自己所在的网段**。

先照实描述现象，不做机制断言：某台设备用 tailnet IP 能访问，用普通 LAN IP 却访问不了，从局域网内 `ping` 它 100% 丢包。机制是——**入包走 LAN，回包被 Tailscale 的路由表抢走、改走 `tailscale0`**，一去一回路径不同，即非对称路由。

还有一个说法需要**诚实标注**：「HAOS 自带一条更高优先级的本地路由保护规则」，让本地目标先走主路由表。此说法目前**只有一个[非官方个人博客来源](https://docs.dev-eric.work/archive/home-lab/tailscale-subnet-router-asymmetric-routing)**，未获官方印证——你可以理解为「HAOS 侧通常有保护」，但**不要当成官方结论**。

自查手段是三条单行命令：

```bash
ip rule show
ip route show table 52
ip route get <目标> from <源>
```

判定标准：`ip route get` 对一个局域网目标返回 `tailscale0` 而不是 `eth0` / `wlan0`，问题就在这台设备上。

本场景的正确做法：你自己的 HAOS 保持 `accept_routes: false`（4.2 已配好），保护够用。**真正要操心的是同一网段的其他 Linux 节点**——它们未必有那层保护，接受这条子路由后可能失去局域网可达性；让上游路由器参与转发也可能出现回程路径问题。

取舍很简单：家用单点需求下，最省事就是「**HAOS 保持 `accept_routes` 关闭 + 不给同一网段的其他 Linux 节点装 Tailscale**」。真要装，再按上面三条命令逐台自查。
