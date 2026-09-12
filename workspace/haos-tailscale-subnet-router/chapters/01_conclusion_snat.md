# 第 1 章 结论前置：同网段到底要不要开 SNAT

网上说「HAOS 做不了子路由」的帖子很多，而你的场景最容易掉进这个争议：HAOS 主机和要访问的设备同在 `192.168.1.0/24`。本章先给结论——能做，且不需要关任何开关——再讲清为什么，以及哪些网上的「标准步骤」别照抄。

## 1.1 这篇笔记解决什么、不解决什么

先对齐场景，本篇默认：家用单层路由，网段 `192.168.1.0/24`、没划 VLAN；HAOS 主机与要远程访问的打印机、摄像头、路由器管理页同网段；远程端是别处的手机或笔记本。

三个目标：外网打开 HA 界面；用 tailnet 域名加 HTTPS 访问；让远程设备访问家里装不了 Tailscale 的设备。官方原话背书：

> 「So if your Home Assistant box is on your home network at `192.168.1.50`, and you set it to offer routes at `192.168.1.0/24`, you could then access all the devices on your home network, whether they run Tailscale or not.」（见 [Tailscale 官方博客](https://tailscale.com/blog/remotely-access-home-assistant)）

不覆盖的：exit node、Taildrop、Taildrive、多站点组网均不展开；与既有 fnos 笔记的对照只放第 8 章一句话带过。

## 1.2 结论：能做，而且保持 `snat_subnet_routes: true` 不动

你的需求属于官方文档描述的标准可做场景：不必关 SNAT，也不必动 `userspace_networking`，保持默认即可。

为什么前置？网上大量「HAOS 做不了子路由」的经验帖，都出现在 SNAT 被关掉的配置下；不动它，就绕开了整片雷区。

> [!tip] 大白话
> SNAT 像「代收快递时把寄件人写成驿站自己」：家里设备不认识 tailnet 的地址体系，SNAT 帮它们把回信地址换成认识的。它是最省事的默认，不是更高级的开关。

结论落到配置就是下面这份，第 4 章逐项展开，其余选项保持默认、不要一起抄：

```yaml
accept_dns: true              # 默认
accept_routes: false          # 默认
advertise_routes:
  - 192.168.1.0/24
snat_subnet_routes: true      # 默认，本场景的核心
userspace_networking: false   # 默认
```

#### 1.2.1 为什么保持 SNAT 开着是「零额外配置」的那条路

远程客户端要访问 `192.168.1.50`，包经隧道到 HAOS，HAOS 再转给打印机。问题在回程：打印机**不认识 `100.64.0.0/10`**（tailnet 地址段），只会把回包丢给默认网关，然后被丢掉。

SNAT 把源地址改写成子路由器自己的 LAN 地址，打印机看到的请求就成了「局域网里一台认识的机器」，回包顺原路回到 HAOS 再进隧道。官方描述：「allows subnet devices to see the traffic originating from the subnet router, and this simplifies routing configuration.」（见 [插件 DOCS.md](https://raw.githubusercontent.com/hassio-addons/app-tailscale/refs/heads/main/tailscale/DOCS.md)）

> [!warning] 别把它讲成「关了就必定不通」
> 官方明确说，关 SNAT 后**必须**补一条回程路由，把 `100.64.0.0/10` 指向子路由器的 LAN IP，且只能落在设备自身、VPC 或 DHCP 上（见 [官方 Subnet routers 文档](https://tailscale.com/docs/features/subnet-routers)）。维护者在 #415 的实测更直接：「it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config.」（见 [Issue #415 评论](https://github.com/hassio-addons/app-tailscale/issues/415)）
> 即开或关都能用，区别只是关掉后要在多处补回程路由，而 HAOS 只读、很难照做。对零基础读者，「不用补任何东西」就是选它的充分理由；官方也把关 SNAT 定位为进阶 site-to-site 的开关。

## 1.3 四条「别照抄」警告，以及它们在后文的落点

这四条是本篇最值钱的部分：

> [!warning] 四条别照抄
> **① 别去 HAOS 上跑 `sysctl` 开 IP 转发。** 根文件系统只读，Linux 教程那条 `sysctl -p /etc/sysctl.d/99-tailscale.conf` 会直接报 `Read-only file system`；插件已代做 IP forwarding 和 MSS 钳制。展开见 4.2.1，报错现场在 7.4.3。
> **② 别把 `snat_subnet_routes` 改成 `false`。** 除非你确定要做 site-to-site 并已准备好补 `100.64.0.0/10` 的回程路由。展开见 4.2.2，代价清单在 8.1。
> **③ 别把「HAOS 主机自己访问 `192.168.1.x` 不走隧道」当成故障。** 这是官方有意设计的本地优先保护，防止 HA 自己失联。展开见 6.2.1，现象与自查在 7.5。
> **④（同网段专属）别忽视同一 LAN 上其他装了 Tailscale 的 Linux 节点。** 你 advertise 的 `192.168.1.0/24` 正是 HAOS 自己所在网段，那些节点可能因此变成非对称路由、失去局域网可达性。展开见 4.5，现象与自查在 7.5。

第 ④ 条补来源说明：「HAOS 自带更高优先级本地路由保护规则」这一机制**只有一个非官方个人博客来源**，未获官方印证，本篇只当现象描述；要操心的是同网段上**其他** Linux 节点有没有这层保护。（见 [个人博客原文](https://docs.dev-eric.work/archive/home-lab/tailscale-subnet-router-asymmetric-routing)）

## 1.4 为什么你必须以自己配置页的实际默认值为准

`userspace_networking` 的默认值**发生过翻转**：2023 年维护者说「Current last released official add-on runs with userspace networking enabled, no tailscale0.」（见 [Issue #216 评论](https://github.com/hassio-addons/app-tailscale/issues/216)），而当前官方文档写「This option is disabled by default.」——默认值已从开启变成关闭。

影响不小：2023–2024 年的教程与论坛帖大量基于旧默认值，是本主题最大的误导来源，照着做很可能第一步就对不上界面。别背版本号，**以你装完那一刻配置页的实际值为准**，再用一条校验命令确认生效（方法在第 5 章 5.3）。

> [!tip] 大白话
> 像拿着三年前的菜单点菜——不是菜单错了，是你手里那份过时了。以眼前这份为准。

## 本章小结

- 同网段单点需求：能做，`snat_subnet_routes: true` 与 `userspace_networking: false` 都别动。
- SNAT 是「零额外配置」的原因；别说成「关了必不通」——实测开关都能工作，差别只在补不补回程路由。
- 四条「别照抄」：别跑 `sysctl`、别关 SNAT、别把本地优先当故障、别忽视同网段其他 Tailscale 节点。
- 默认值以你配置页的实际值为准，用 5.3 的命令校验。

下一章：装插件、完成登录授权，让控制台的 Machines 列表里出现 `homeassistant`。
