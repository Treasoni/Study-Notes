---
title: HAOS Tailscale 内网穿透与子路由实战
tags:
  - 内网穿透
  - Tailscale
  - HAOS
  - HomeAssistant
  - 子网路由
created: 2026-09-12
updated: 2026-09-13
status: 完成
source_project: haos-tailscale-subnet-router
---

# 用 HAOS 上的 Tailscale 插件打通内网穿透与子路由（同网段 192.168.1.0/24 实战）

## 目录

1. [第 1 章 结论前置：同网段到底要不要开 SNAT](#第-1-章-结论前置同网段到底要不要开-snat)
   - [1.1 这篇笔记解决什么、不解决什么](#11-这篇笔记解决什么不解决什么)
   - [1.2 结论：能做，而且保持 `snat_subnet_routes: true` 不动](#12-结论能做而且保持-snat_subnet_routes-true-不动)
   - [1.3 四条「别照抄」警告，以及它们在后文的落点](#13-四条别照抄警告以及它们在后文的落点)
   - [1.4 为什么你必须以自己配置页的实际默认值为准](#14-为什么你必须以自己配置页的实际默认值为准)
2. [第 2 章 装插件并完成登录授权](#第-2-章-装插件并完成登录授权)
   - [2.1 开工前的准备](#21-开工前的准备)
   - [2.2 在 HA 应用商店里安装](#22-在-ha-应用商店里安装)
   - [2.3 启动并完成登录授权](#23-启动并完成登录授权)
   - [2.4 确认上线，以及一个会浪费你半天的坑](#24-确认上线以及一个会浪费你半天的坑)
3. [第 3 章 内网穿透：不开口、不做反代就远程访问](#第-3-章-内网穿透不开口不做反代就远程访问)
   - [3.1 最小可用路径：先能用](#31-最小可用路径先能用)
   - [3.2 更好的路径：Serve 给一个域名和证书](#32-更好的路径serve-给一个域名和证书)
   - [3.3 Funnel 与 `services`：先别急着开](#33-funnel-与-services先别急着开)
   - [3.4 出方向才需要：让 HA 用 tailnet 名字访问别的设备](#34-出方向才需要让-ha-用-tailnet-名字访问别的设备)
   - [3.5 直连还是中继：要不要开 `always_use_derp`](#35-直连还是中继要不要开-always_use_derp)
4. [第 4 章 子路由：把 HAOS 变成 tailnet 的网关](#第-4-章-子路由把-haos-变成-tailnet-的网关)
   - [4.1 子路由在做什么：一句话和一条边界](#41-子路由在做什么一句话和一条边界)
   - [4.2 本文推荐配置与逐项解释](#42-本文推荐配置与逐项解释)
   - [4.3 在管理控制台授权这条路由](#43-在管理控制台授权这条路由)
   - [4.4 「HAOS 做不了子路由」这个说法从哪来](#44-haos-做不了子路由这个说法从哪来)
   - [4.5 同网段专属警告：别把同一个 LAN 上的其他 Linux 节点搞成非对称路由](#45-同网段专属警告别把同一个-lan-上的其他-linux-节点搞成非对称路由)
5. [第 5 章 在远程客户端上接收路由](#第-5-章-在远程客户端上接收路由)
   - [5.1 路由注入的四个条件](#51-路由注入的四个条件)
   - [5.2 各平台默认值不一样，Linux 最容易踩](#52-各平台默认值不一样linux-最容易踩)
   - [5.3 客户端上怎么打开，以及那条校验命令](#53-客户端上怎么打开以及那条校验命令)
6. [第 6 章 验收：你自己跑一遍六步](#第-6-章-验收你自己跑一遍六步)
   - [6.1 把测试环境摆对](#61-把测试环境摆对)
   - [6.2 六步验收清单，按顺序执行](#62-六步验收清单按顺序执行)
   - [6.3 把结果记下来](#63-把结果记下来)
7. [第 7 章 排错：按顺序查，别猜](#第-7-章-排错按顺序查别猜)
   - [7.1 路由根本没出现在客户端的路由表里](#71-路由根本没出现在客户端的路由表里)
   - [7.2 路由在、隧道也通，但目标不通](#72-路由在隧道也通但目标不通)
   - [7.3 路由和 ACL 是两套东西](#73-路由和-acl-是两套东西)
   - [7.4 HAOS 特有的坑](#74-haos-特有的坑)
   - [7.5 四种常见误判，以及一个不要当步骤的「怪招」](#75-四种常见误判以及一个不要当步骤的怪招)
8. [第 8 章 边界、未核验声明与下一步](#第-8-章-边界未核验声明与下一步)
   - [8.1 什么时候才需要关 SNAT](#81-什么时候才需要关-snat)
   - [8.2 本篇的边界与未核验声明](#82-本篇的边界与未核验声明)
   - [8.3 下一步](#83-下一步)

## 第 1 章 结论前置：同网段到底要不要开 SNAT

网上说「HAOS 做不了子路由」的帖子很多，而你的场景最容易掉进这个争议：HAOS 主机和要访问的设备同在 `192.168.1.0/24`。本章先给结论——能做，且不需要关任何开关——再讲清为什么，以及哪些网上的「标准步骤」别照抄。

### 1.1 这篇笔记解决什么、不解决什么

先对齐场景，本篇默认：家用单层路由，网段 `192.168.1.0/24`、没划 VLAN；HAOS 主机与要远程访问的打印机、摄像头、路由器管理页同网段；远程端是别处的手机或笔记本。

三个目标：外网打开 HA 界面；用 tailnet 域名加 HTTPS 访问；让远程设备访问家里装不了 Tailscale 的设备。官方原话背书：

> 「So if your Home Assistant box is on your home network at `192.168.1.50`, and you set it to offer routes at `192.168.1.0/24`, you could then access all the devices on your home network, whether they run Tailscale or not.」（见 [Tailscale 官方博客](https://tailscale.com/blog/remotely-access-home-assistant)）

不覆盖的：exit node、Taildrop、Taildrive、多站点组网均不展开；与既有 fnos 笔记的对照只放第 8 章一句话带过。

### 1.2 结论：能做，而且保持 `snat_subnet_routes: true` 不动

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

### 1.3 四条「别照抄」警告，以及它们在后文的落点

这四条是本篇最值钱的部分：

> [!warning] 四条别照抄
> **① 别去 HAOS 上跑 `sysctl` 开 IP 转发。** 根文件系统只读，Linux 教程那条 `sysctl -p /etc/sysctl.d/99-tailscale.conf` 会直接报 `Read-only file system`；插件已代做 IP forwarding 和 MSS 钳制。展开见 4.2.1，报错现场在 7.4.3。
> **② 别把 `snat_subnet_routes` 改成 `false`。** 除非你确定要做 site-to-site 并已准备好补 `100.64.0.0/10` 的回程路由。展开见 4.2.2，代价清单在 8.1。
> **③ 别把「HAOS 主机自己访问 `192.168.1.x` 不走隧道」当成故障。** 这是官方有意设计的本地优先保护，防止 HA 自己失联。展开见 6.2.1，现象与自查在 7.5。
> **④（同网段专属）别忽视同一 LAN 上其他装了 Tailscale 的 Linux 节点。** 你 advertise 的 `192.168.1.0/24` 正是 HAOS 自己所在网段，那些节点可能因此变成非对称路由、失去局域网可达性。展开见 4.5，现象与自查在 7.5。

第 ④ 条补来源说明：「HAOS 自带更高优先级本地路由保护规则」这一机制**只有一个非官方个人博客来源**，未获官方印证，本篇只当现象描述；要操心的是同网段上**其他** Linux 节点有没有这层保护。（见 [个人博客原文](https://docs.dev-eric.work/archive/home-lab/tailscale-subnet-router-asymmetric-routing)）

### 1.4 为什么你必须以自己配置页的实际默认值为准

`userspace_networking` 的默认值**发生过翻转**：2023 年维护者说「Current last released official add-on runs with userspace networking enabled, no tailscale0.」（见 [Issue #216 评论](https://github.com/hassio-addons/app-tailscale/issues/216)），而当前官方文档写「This option is disabled by default.」——默认值已从开启变成关闭。

影响不小：2023–2024 年的教程与论坛帖大量基于旧默认值，是本主题最大的误导来源，照着做很可能第一步就对不上界面。别背版本号，**以你装完那一刻配置页的实际值为准**，再用一条校验命令确认生效（方法在第 5 章 5.3）。

> [!tip] 大白话
> 像拿着三年前的菜单点菜——不是菜单错了，是你手里那份过时了。以眼前这份为准。

> [!summary] 本章小结
> - 同网段单点需求：能做，`snat_subnet_routes: true` 与 `userspace_networking: false` 都别动。
> - SNAT 是「零额外配置」的原因；别说成「关了必不通」——实测开关都能工作，差别只在补不补回程路由。
> - 四条「别照抄」：别跑 `sysctl`、别关 SNAT、别把本地优先当故障、别忽视同网段其他 Tailscale 节点。
> - 默认值以你配置页的实际值为准，用 5.3 的命令校验。

下一章：装插件、完成登录授权，让控制台的 Machines 列表里出现 `homeassistant`。

结论已经给出：同网段场景保持默认配置即可。接下来先把插件装好、完成授权，让这台 Home Assistant 出现在你的 tailnet 里。

## 第 2 章 装插件并完成登录授权

这一章只做一件事：把 Tailscale 插件装进 HAOS，让你的 Home Assistant 出现在自己的 tailnet 里。全程在 HA 界面和 Tailscale 控制台点鼠标，不碰配置文件。装完它，第 3 章的远程访问才有前提。

### 2.1 开工前的准备

先注册 Tailscale 账号。官方文档写明它对个人与爱好项目免费，单用户账号最多 100 台客户端/设备，用 Google / Microsoft / GitHub 账号在 `tailscale.com/start` 注册即可 [^c2-1]。注册完你就有了一个 tailnet。

第二件事：装完记得去关掉这台设备的 key 过期。官方建议关闭它，避免和 Home Assistant 失联 [^c2-2]。等设备出现在控制台后就去关。不做的话，key 一到期设备会失联、路由随之失效，fail-close 现场见第 7 章 7.4.1 节。

第三件事：顺手把 tailnet 名改好。默认名字长这样 `tail6e5bf.ts.net`，难记也难打；在控制台点 DNS → Rename tailnet，重摇到顺眼为止，同时确认 MagicDNS 与 HTTPS Certificates 已开启 [^c2-3]。第 3 章的 Serve 要用到这个域名和证书。

> [!tip] 大白话
> 把 tailnet 想成你自己的小区：只有被你拉进来的设备才能进院子串门，外面看不到院里的门牌。「登录授权」就是给 Home Assistant 发一张门禁卡；关掉 key 过期，是让这张卡不要到期作废。

### 2.2 在 HA 应用商店里安装

在 HA 里点左下角 Settings → Apps（旧版本叫 Add-ons，HA 2026.8 起更名），再点右下角 Install app，搜索 Tailscale，选中后点 Install [^c2-4]。

这里必须确认你装的是哪一个——这个主题的教程互相矛盾，多半是因为存在两套插件。本笔记操作的是插件 ID `a0d7b954_tailscale`，来自仓库 `hassio-addons/repository`，维护者是 Home Assistant 核心开发者 Franck Nijhof（frenck）[^c2-1]。它的文档自称 Home Assistant Community App: Tailscale。

> [!warning] 别装错，也别照抄
> 另有一套 `hass-tailscale/hass-addons`（要你填 `auth_key` 的那套）已经废弃。这里只作背景说明，**不构成操作指引、你不需要照它做**：认识它长什么样就够了，看到 `auth_key` 字样的教程直接跳过。

### 2.3 启动并完成登录授权

回到 Apps 菜单，点 Tailscale → Info → Start [^c2-4]。官方步骤是先 Start、再看日志确认没报错，然后才授权 [^c2-1]。接着点 Open Web UI 完成登录授权，把 Home Assistant 挂到你的 tailnet 上；这一步会弹出登录页，需要允许弹窗并确认接入 [^c2-4]。

> [!warning] 不是所有浏览器都能完成这一步
> 官方原文：Some browsers don't work with this step. It is recommended to complete this step on a desktop or laptop computer using the Chrome browser.
> 照做就是：找一台桌面或笔记本，用 Chrome。在手机浏览器上卡住，不是你的问题。

顺手可以打开 Watchdog、Auto update；Show in sidebar 可选，官方说它没那么必要 [^c2-4]。

### 2.4 确认上线，以及一个会浪费你半天的坑

回到控制台 Machines 页，应该能看到一台名为 `homeassistant` 的设备，旁边绿点表示已连接 [^c2-4]。看到绿点，这一章就过关。

那个坑在这里。插件后台 Web UI 里也能看到一部分配置项，但官方文档明确写着：这些选项在 Web UI 里是只读的，你改不动，因为所有在 Web UI 上做的改动都会在插件重启后丢失 [^c2-1]。所以**要改配置，只能改插件自己的 YAML**。记住这一点——它直接决定了第 4 章的配置方式，别指望在后台界面上把 `advertise_routes` 点出来。
![](assets/HAOS%20Tailscale%20内网穿透与子路由实战/截屏2026-09-13%2012.41.47.png)

> [!warning] 界面上显示的值，不等于实际生效的值
> 还有一类已知现象：有人在插件界面看到的值和实际生效的行为对不上。这不是错觉——插件的部分默认值在历史上发生过翻转，网上 2023–2024 年的教程大量基于旧默认值，与当前文档写的不一致 [^c2-1]。所以别背版本号、别信旧教程：以你装完那一刻配置页显示的值，加上第 5.3 节那条校验命令来判断。

> [!summary] 本章小结
> - 三件准备：注册 Tailscale 账号、装完关掉该节点 key 过期（见 7.4.1）、把 tailnet 改成好记的名字（第 3 章 Serve 要用）。
> - 认准插件：ID `a0d7b954_tailscale`、仓库 `hassio-addons/repository`、维护者 frenck；`hass-tailscale/hass-addons` 已废弃，别照它做。
> - 顺序是 Install → Start → Open Web UI 授权；授权用桌面 Chrome。
> - 后台 Web UI 的配置项只读、重启即丢，改配置只能改插件 YAML。
> - 控制台 Machines 里出现 `homeassistant` 加绿点，才算授权成功。

下一章不再碰安装界面：直接用刚挂上 tailnet 的这台 HAOS，从外网打开 Home Assistant。

到这里，HA 已经出现在 tailnet 里。下一步就是用这条隧道，从外网打开家里的 Home Assistant。

[^c2-1]: [hassio-addons/app-tailscale DOCS.md](https://github.com/hassio-addons/app-tailscale)（本地缓存 `sources/08_raw_githubusercontent_com.md`）
[^c2-2]: 同 [^c2-1]，`## Configuration` 首段
[^c2-3]: [Remotely access Home Assistant via Tailscale for free](https://tailscale.com/blog/remotely-access-home-assistant)（本地缓存 `sources/11_tailscale_com.md`）
[^c2-4]: 同 [^c2-3]

## 第 3 章 内网穿透：不开口、不做反代就远程访问

外网要打开家里的 HA，传统做法是端口转发或反向代理，代价都是要在路由器上开口子。这一章走另一条路：HA 已经是 tailnet 上的设备，顺着 Tailscale 自己的能力把它露出来就够了——不开端口、不做反代。先用 tailnet IP 拿到「能用」，再用 Serve 拿到「好用的域名 + HTTPS」。

### 3.1 最小可用路径：先能用

授权完成之后，你其实已经能远程访问了：在任意一台连着 tailnet 的设备上，用 HA 的 tailnet IP 加端口访问即可。这是 Tailscale 的默认能力，不是你额外配出来的，官方博客的原话是「without opening ports or setting up proxies」[^c3-blog]。

> [!tip] 大白话
> 把 tailnet 想成一间公司内网：tailnet IP 就是分机号，只要双方都在这个内网里，拨号就通。你要做的不是去电信局申请外线（端口转发），而是确认自己已经在网内。

先别急着做 Serve。用一台真正不在家里的设备（手机关 Wi-Fi 走蜂窝最省事）访问一次，确认这条最朴素的路能走通。它是基线：后面的故障都能被它切成「隧道不通」还是「只有域名层不通」。

#### 3.1.1可能失败的原因
**1. 客户端代理软件（Clash / VPN）拦截了 Tailscale 私网 IP（最主要原因）**

- **分析**：从第一张截图中可以看到浏览器右上角启用了代理软件（紫色火焰图标）。当开启「系统代理」时，浏览器访问 `100.119.21.57:8123` 的流量会被优先接管送入本地代理端口。
- 由于 `100.64.0.0/10` 是 Tailscale 专用的 CGNAT 私有保留网段，代理软件如果未将该网段设为直连（DIRECT），就会将其转给远端海外代理节点；远端节点根本无法寻址你的私人 Tailnet，连接失败后便由本地代理向 Chrome 返回了 **HTTP 502 Bad Gateway**。
- **排查操作**：
    1. 临时关闭或彻底退出电脑上的代理软件（关闭系统代理）。
    2. 如果需要长期与代理共存，在代理软件的「绕过系统代理」列表（Bypass / 直连规则）中加入 Tailscale 网段

- **验证方法**：关闭代理后重新刷新 `[http://100.119.21.57:8123](http://100.119.21.57:8123)`，能够正常出现 HA 登录界面即说明解决。

### 3.2 更好的路径：Serve 给一个域名和证书

直接用 IP 加端口能访问，但浏览器会提示不安全（它不知道 tailnet 内部的连接是端到端加密的），URL 也难记。Serve 能给 HA 一个带有效证书的 tailnet 域名，一次解决这两件事。

它有两处前置。

HA 侧：关闭 SSL/TLS，让 HA 以 HTTP 提供服务——Settings → System → Network → HTTP server → SSL/TLS。然后在“反向代理“同一区块展开 Reverse proxy：启用 `Trust X-Forwarded-For`，把 `127.0.0.1` 加进 `Trusted proxies`，保存（保存会重启 HA 界面）。


Tailscale 控制台的 DNS 页：改一个顺眼的 tailnet 名（这里的Tailnet DNS name），
![](assets/HAOS%20Tailscale%20内网穿透与子路由实战/截屏2026-09-13%2013.08.49.png)
确认 MagicDNS 已启用（在Network->DNS中），并在 HTTPS Certificates 一节 Enable HTTPS。
![](assets/HAOS%20Tailscale%20内网穿透与子路由实战/截屏2026-09-13%2013.08.03.png)

> [!tip] 大白话
> Serve 像在 HA 门口盖了间门卫室：手机先找到门卫室（域名 + 证书），再由它领你进 HA。门卫室设在本机门口，所以 HA 眼里访客永远从「本机」来——这正是 3.2.1 要讲的。

对应的插件配置项是这两行：

```yaml
share_homeassistant: disabled   # 默认值；启用 Serve 时按配置页下拉框改
share_on_port: 443
```

`share_on_port` 只能填 443、8443、10000 三个端口之一，默认就是 443。首次设置后，域名可能要最多 10 分钟才会生效，别刚点完就下结论。

还有两条容易踩：不要再把原来那个端口号拼进 URL；如果浏览器行为古怪或报奇怪的错，先清掉该站点的 cookie 和缓存、重启浏览器。

#### 3.2.1 为什么 `Trusted proxies` 填 `127.0.0.1` 而不是 `100.64.0.0/10`

因为 HA 看到的连接不是从你的 tailnet IP 直接来的，而是从本机的 Serve 代理转过来的，所以可信代理要写回环地址。插件官方文档和 Tailscale 官方博客在这里口径一致，都写 `127.0.0.1`[^c3-docs][^c3-blog]。

> [!warning] 别填 100.64.0.0/10
> 这是新手最容易填错的地方。不要因为「访问来自 tailnet」就填 `100.64.0.0/10`——那样 HA 不认这个代理，Serve 转发过来的请求照样被挡。

### 3.3 Funnel 与 `services`：先别急着开

Funnel 和 Serve 长得像，方向却相反：它会把 HA 暴露到公网，连不装 Tailscale 客户端的设备也能访问。这跟本章「不开口」的初衷正相反，官方博客的说法是「You almost certainly do not want Funnel」[^c3-blog]。普通远程访问用 Serve 就够，不要顺手把 Funnel 打开。

`services` 选项解决另一个需求：用同一个域名把插件商店里的其他服务也露出来（文档举的例子是 audiobookshelf）。它有两条硬约束——只支持 Serve、不支持 Funnel；节点还必须先打上 tag 才能用。

### 3.4 出方向才需要：让 HA 用 tailnet 名字访问别的设备

> [!info] 先分清方向：这一节不是给「访问 HA」用的
> 本节解决的是 **HA → 别的 tailnet 设备**，也就是**出方向**。如果你只想要 tailnet 上的手机、笔记本能打开 HA，那 3.1–3.3 已经做完了，**本节整节都不用做**——包括下面那条 `ha dns options`。

#### 3.4.1 那什么时候才真需要它

只有当 HA 自己要以名字主动连出去时，比如：
- HA 里的集成要连 `nas.tail1234.ts.net` 上的服务；
- 你在 HA 终端 / SSH 插件里 `ping`、`curl` 别的 tailnet 设备；
- 要把 HA 当子路由/站点到站点网关用，双向互通。

为什么入方向不需要它：名字是**发起方**解析的。手机访问 HA，解析发生在手机上，是手机自己的 Tailscale 客户端把 `ha.tail1234.ts.net` 变成 tailnet IP；HA 这侧不需要任何 DNS 配置，它只要「能被路由到」就行。插件文档把这个单向场景写得很直白——开着 `userspace_networking` 时「you get one-way access from tailnet clients to your Home Assistant instance」，也就是说「别人 → HA」这个方向本身就不依赖本节任何东西 [^c3-docs]。

反过来，HA 自己要以名字主动连出去时，解析发生在 HA 内部、走的是 `hassio_dns`，而它默认不认 tailnet 名字，才需要手工把 Tailscale 的 DNS 接上。

> [!warning] 别把三件事混成一件
> 这三个东西常被读成「同一个 MagicDNS」，实际各管一段：
>
> | 配置 | 在哪配 | 管什么 | 本节要不要 |
> | --- | --- | --- | --- |
> | MagicDNS / HTTPS Certificates 开关 | Tailscale 控制台 DNS 页 | 全 tailnet 的名字与证书，**入方向和出方向都受益** | 3.2 做 Serve 时已开；本节不靠它 |
> | `ha dns options --servers dns://100.100.100.100` | HA 命令行 | 改 `hassio_dns` 的上游，**只影响 HA 自己往外解析** | 只有出方向需要，即本节内容 |
> | `userspace_networking` | 插件配置页 | 有没有 `tailscale0`；决定 HA 是单向还是双向参与者 | 保持默认 `false` 不动 |
>
> 一句话：**控制台那个开关 ≠ 需要跑这条命令。**

想让 HA 用 tailnet 名字访问别的设备，前提是 `userspace_networking` 处于关闭状态：只有关闭时，Tailscale 才会提供 `100.100.100.100` 这个 DNS（文档原文：When the `userspace_networking` option is disabled, Tailscale provides a DNS (at `100.100.100.100` and `fd7a:115c:a1e0::53`)）[^c3-docs]。

接法有个反直觉点：不要在 HA 的 Network 页把 Tailscale DNS 设成 DNS 服务器，改用命令行：

```bash
ha dns options --servers dns://100.100.100.100
```

这条命令是持久化的，执行一次就够，重启也不会丢。要清空得用两条：

```bash
ha dns reset
ha dns restart
```

代价是必须用完整域名（FQDN）：`ping device.tail1234.ts.net` 可以，`ping device` 不行。

> [!tip] 大白话
> 完整域名像「省 + 市 + 街道」的地址，解析器只认全称。你只写一个「小明」，它是找不到人的。

另外把 `accept_dns: false` 的含义记准：它表示「不接受控制台下发的全局 nameserver」，不是本地关掉 MagicDNS，也不是本地关掉 Tailscale DNS[^c3-dns]。

> [!warning] 这条命令有个已知后果
> 上面那条 `ha dns options` 有一个已知的严重后果，现象、成因与修法在第 7 章 7.4.4 节。照做之前先读那一节，别等 DNS 挂了再回头找。

什么时候才真的需要它？只有当 **HA 自己要以名字主动连出去**，比如：

- HA 里的集成要连 `nas.tail1234.ts.net` 上的服务；
- 你在 HA 的终端或 SSH 插件里 `ping`、`curl` 别的 tailnet 设备；
- 要把 HA 当双向网关用（对应第 8.1 节的 site-to-site 场景）。

本文第 1.1 节列的三个目标都不属于上面任何一条，所以**照本文走完全程都不会用到这一节**。前面 3.1 说过，能直接用 tailnet IP 连的场合（`100.x.y.z`）就不必换成名字——为一个用不上的方向去担 7.4.4 那个 DNS loop 的风险，不划算。

### 3.5 直连还是中继：要不要开 `always_use_derp`

`always_use_derp` 会强制所有 peer 通信走 DERP 中继、禁用 UDP：

```yaml
always_use_derp: false   # 默认值，保持不动
```

默认不要开。官方文档写得很直接：「Basically you will never want to enable this option.」[^c3-docs]只有当你反复遇到那种特征——能 ping 通设备，但网页或 App 卡死、要刷新页面或强杀 App 才恢复——才把它当兜底考虑，因为根因可能是你的 ISP 在某些条件下错误地丢弃 UDP 包。

P2P 到底有没有打通，别靠感觉判断，交给第 7 章的 `tailscale ping` 和 `41641/udp` 检查。

> [!summary] 本章小结
> - 授权完成后，用 tailnet IP + 端口访问 HA 就能用，不开端口、不做反代。
> - Serve 给的是带证书的 tailnet 域名；前置是 HA 关 SSL/TLS、Reverse proxy 里启用 `Trust X-Forwarded-For` 并把 `127.0.0.1` 加进 `Trusted proxies`，以及控制台 DNS 页改名 + 开 MagicDNS + Enable HTTPS。
> - `share_on_port` 只能 443 / 8443 / 10000，默认 443；域名生效可能最多 10 分钟。
> - Funnel 会把 HA 推到公网，普通需求不要开；`services` 只支持 Serve，节点必须先打 tag。
> - 3.4 那条 `ha dns options` 是**出方向**（HA → 别的设备）才需要的：只做「tailnet 设备 → HA」的入方向不用碰它。命令持久化、只需一次，代价是必须用 FQDN。
> - `always_use_derp` 默认别开。

下一章把视角从「访问 HA 自己」扩到「访问 HA 所在的整个局域网」——配置子路由，把 HAOS 变成 tailnet 的网关。

访问 HA 自己已经解决。接下来把视角从「一台设备」扩大到「整个局域网」——给 tailnet 借出 `192.168.1.0/24`。

[^c3-docs]: hassio-addons/app-tailscale DOCS.md（插件官方文档）— https://raw.githubusercontent.com/hassio-addons/app-tailscale/refs/heads/main/tailscale/DOCS.md
[^c3-blog]: Tailscale 官方博客《Remotely access Home Assistant via Tailscale for free》— https://tailscale.com/blog/remotely-access-home-assistant
[^c3-dns]: hassio-addons/app-tailscale Discussion #449（DNS / MagicDNS 与 hassio_dns）— https://github.com/hassio-addons/app-tailscale/discussions/449

## 第 4 章 子路由：把 HAOS 变成 tailnet 的网关

前面几章你已经能让远程设备访问 HA 自己。可家里真正要用的往往是打印机、摄像头、路由器管理页——它们装不了 Tailscale。这一章让 HAOS 当网关，把整个 `192.168.1.0/24` 借给 tailnet 用，网段里的设备一个字节都不用改。

### 4.1 子路由在做什么：一句话和一条边界

子路由的官方定义是：让 tailnet 覆盖那些「不能或无法运行 Tailscale 客户端」的设备：

> "Subnet routers let you extend your Tailscale network (known as a tailnet) to include devices that don't or can't run the Tailscale client."

网关由 HAOS 扮演：你告诉它「`192.168.1.0/24` 归我管」。远程设备要访问 `192.168.1.50`，包先走隧道到 HAOS，再由它用普通 LAN 的方式转给打印机；打印机全程不知道 Tailscale 存在。

还一条容易混的边界：子路由**只暴露指定网段**；exit node 接管的是 **tailnet 设备访问公网的全部出站流量**，官方比作「VPN 服务器」。别顺手打开 `advertise_exit_node`。

> [!tip] 大白话
> 把子路由想成小区门口的快递代收点：快递员（远程设备）只认识代收点（HAOS），不认识你家打印机；代收点负责把包裹送上楼。打印机不用认识快递员，这就是「不用装任何东西」。

### 4.2 本文推荐配置与逐项解释

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

#### 4.2.1 警告①：不要照抄 Linux 子路由教程的第 2 步

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

#### 4.2.2 警告②：不要关 `snat_subnet_routes`

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

### 4.3 在管理控制台授权这条路由

配置写对只是一半。路由不会自动生效，**必须在管理控制台手动批准**，否则永远不会下发到客户端：

1. 打开控制台 **Machines** 页。
2. 找到 **Subnets** 标记，或用 `property:subnet` 过滤器列出所有广告子路由的设备。
3. 选中带 `subnet` 属性的设备，展开 **Subnets** 段。
4. 点 **Edit**，打开 **Edit route settings**。
5. 在 **Subnet routes** 下勾选 `192.168.1.0/24`，**Save**。

顺手复核 key 过期：官方建议给服务器**关闭 key 过期**，省得反复重新认证（第 2 章做过）。

没授权的后果很具体：不是报错，而是**配了没生效**——路由只存在于 HAOS 上，客户端什么都没有。这是第 7 章排错清单的**第 1 顺位**。

### 4.4 「HAOS 做不了子路由」这个说法从哪来

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

### 4.5 同网段专属警告：别把同一个 LAN 上的其他 Linux 节点搞成非对称路由

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

HAOS 侧的配置与管理端授权都已就位。但路由要到远程客户端真正生效，客户端这端还得点头。

## 第 5 章 在远程客户端上接收路由

第 4 章你在 HAOS 侧 advertise 了 `192.168.1.0/24`、又在管理端勾了授权，但路由要真正进入你手机或笔记本的路由表，客户端这端也得点头。本章三件事：四个条件、Linux 例外、一条自证命令。

### 5.1 路由注入的四个条件

官方文档把「路由什么时候被注入客户端路由表」写得很清楚，必须同时满足四条：

1. **子路由节点 advertise**：节点用 `--advertise-routes` 声明它能到哪些网段，对应第 4 章的 `advertise_routes`。
2. **管理员 approve**：在管理控制台授权，或用 tailnet policy file 里的 `autoApprovers`。
3. **控制面分发**：授权通过后，控制面才把这条路由放进下发给客户端的 network map。
4. **客户端 accept**：客户端必须开启接受子路由。

四条是「与」的关系，缺哪一条，现象都是同一句「配了没生效」。顺带一条：客户端不会 ping 路由器来发现路由，路由是 advertise + approve 后从 network map 收到的。

> [!tip] 大白话
> 把路由想成新开一条公交线：① 车队申报要开，② 交管局（管理端）批，③ 印到站牌（network map）发到各站，④ 乘客（客户端）还得愿意上车。缺一步，你都会觉得「这线路配了等于没有」。

> [!warning] ACL / grants 不会注入路由
> 官方点名的常见误解：grants 和 ACLs **不**控制路由注入，它们只管包过滤。于是两种半吊子状态都不通——**有路由没 ACL**：包进了隧道被过滤器丢掉；**有 ACL 没路由**：包根本没进隧道。两者都要有才端到端通。第 7.3 节会再展开，这里先记住「路由和 ACL 是两套东西」。

### 5.2 各平台默认值不一样，Linux 最容易踩

第 4 条「客户端 accept」的默认值，各平台并不一致：

- Windows、macOS、Android、iOS、tvOS **默认接受**子路由；
- **Linux 默认不接受**，要显式执行 `tailscale set --accept-routes`。

> [!tip] 大白话
> 同一份快递，手机和 Mac 默认放前台，Linux 默认放驿站——不特别交代一声，它不会送上来。

这就解释了一个高频困惑：同一套 HAOS 配置，**手机一配就通、Linux 服务器死活不通**。先别怀疑 HAOS，多半是踩到了 Linux 的默认值。

### 5.3 客户端上怎么打开，以及那条校验命令

图形界面里对应的开关叫 **Use Tailscale subnets**，取消勾选就是「忽略 advertise 过来的路由」，即不接受。命令行等价操作：

```bash
# 接受子路由（Linux 默认关闭，需显式打开）
tailscale set --accept-routes

# 反过来：不接受
tailscale set --accept-routes=false
```

想确认是否生效，用官方校验命令：

```bash
# 看 RouteAll 是否为 true
tailscale debug prefs
```

为 `true` 说明这台客户端确实在接受子路由；为 `false` 就照第一条命令打开。

> [!tip] 大白话
> 第 1 章 1.4 节提醒过你：别背版本号、别信二手教程，要「以你配置页此刻的实际值为准」。`tailscale debug prefs` 的 `RouteAll` 就是这句话的兑现方式——界面显示和文档都不算数，这台机器实际生效的值才算；第 2.4 节说的界面与实际不一致，也靠它判定。

> [!summary] 本章小结
> - 路由注入四条缺一不可：advertise、approve、控制面下发、客户端 accept。
> - ACL / grants 不注入路由，只管包过滤；有路由没 ACL、有 ACL 没路由，两种都不通。
> - 默认值分平台：Windows / macOS / Android / iOS / tvOS 默认接受，Linux 默认不接受。
> - 图形界面看 `Use Tailscale subnets`，命令行用 `tailscale set --accept-routes`（关闭加 `=false`），校验看 `tailscale debug prefs` 的 `RouteAll`。

配置齐了不等于通了。第 6 章把前面环节串成一份六步验收清单，你亲自跑一遍并记下结果。

路由注入的四个条件、Linux 的例外和那条校验命令都讲完了。配置齐了不等于通了，下一步是你亲自跑一遍验收。

## 第 6 章 验收：你自己跑一遍六步

前五章你都在配置，这一章只做一件事：证明它到底通没通。结论得你自己跑出来，本篇给的是可执行路径，不是成功率保证。

### 6.1 把测试环境摆对

两个变量先固定住，否则第 5 步失败时分不清是谁的问题。

- 测试端必须是真正在家庭网络之外的 tailnet 客户端。最省事的做法是把手机关掉 Wi-Fi、走蜂窝，它就不可能悄悄从家里局域网绕过去。
- 目标设备要选一台明确没装 Tailscale、平时能从家里电脑 ping 通的设备。打印机、摄像头、路由器管理页面都行——官方把「让远程用户访问打印机、摄像头这类装不了客户端的设备」列为子路由的典型用途。
- 先把目标 IP 记下来，后面每一步都用同一个 IP。官方博客举的例子是：HA 在家里网络的 `192.168.1.50`、对外提供 `192.168.1.0/24` 路由，然后就能访问家里所有设备。

> [!tip] 大白话
> 子路由像给家里开了个「代收点」：远程客户端不用认识打印机，把包交给 HAOS 就行。

### 6.2 六步验收清单，按顺序执行

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

### 6.3 把结果记下来

把每一步的结论写进一张表，失败时你会立刻知道停在哪：

| 节点名 | 是否 advertise | 是否 approve | 客户端平台 | 是否 accept | 隧道是否通 | 局域网 IP 是否通 | 失败时停在第几步 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

> [!warning] 诚实声明
> 本篇结论由官方文档，加上维护者在**两种 HAOS 部署形态**（树莓派实机 + VirtualBox 虚拟机）上的实测背书。但他测的是**双向 site-to-site**，不是你这套同网段单向场景，原话是 "it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config."。请以你自己的实测为准，不要期待「必定成功」。

验收不通过就直接进第 7 章，按顺序查，不要回头乱改 SNAT。

六步跑完，通过就可以收工；没通过就进下一章。排错的关键是按固定顺序逐项排除，先定位到具体一环再动手。

## 第 7 章 排错：按顺序查，别猜

第 6 章你跑过六步验收，如果没过，这一章给你用。排错最怕的不是问题难，而是上来就回头改 SNAT、或去 HAOS 上跑 `sysctl`。正确做法是按固定顺序逐项排除，先定位到具体一环，再动手。

### 7.1 路由根本没出现在客户端的路由表里

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

### 7.2 路由在、隧道也通，但目标不通

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

### 7.3 路由和 ACL 是两套东西

第 5.1 节的这个误解到排错阶段就成了判断依据。官方两个反直觉例子：

- 子路由广告了 `10.0.0.0/8` 但没有 grant 覆盖：客户端**会**拿到路由，流量进隧道后被包过滤丢掉。原文：`If a router advertises 10.0.0.0/8 but no grant covers it, clients receive the route but traffic is dropped by the packet filter.`
- 反过来，允许 `10.0.0.0/8` 的 grant **不会**额外注入任何路由：`A grant allowing 10.0.0.0/8 does not cause additional routes to be injected.`

一句话：`You can have a route without ACL access (packets enter the tunnel but are dropped by the filter), or ACL access without a route (packets never enter the tunnel).` 两条都得有。这一节是「避免在错误的地方改配置」——路由没出现回 7.1 查 advertise / approve / accept，路由出现但走不通再来查 ACL。

### 7.4 HAOS 特有的坑

#### 7.4.1 key 过期导致 fail-close

连接器（connector，子路由、exit node、app connector 都算）的 key 过期后，它的路由在**其他设备上仍然保留，但变得不可达**。官方 [Subnet routers 文档](https://tailscale.com/docs/features/subnet-routers) 把这条行为叫 "fail close"：`When a connector's ... key expires, the connector's advertised routes remain configured on other devices but become unreachable (known as "fail close" policy). Tailscale keeps these routes in place intentionally because removing them could leak traffic to untrusted networks.`

这是官方**有意为之**，不是 bug——路由故意不撤，免得流量泄漏到不可信的网络（fail-close，像消防通道被反锁：门还挂在那儿却推不开）。定位动作很简单：把「最近有没有到期或重新认证」当成固定检查项。预防办法见第 2 章和第 4.3 节——关闭该节点的 key 过期，或配置高可用。

#### 7.4.2 排错前先关掉日志压制

`log_suppression` 默认开启，作用是「在 200 行之后开始压掉插件日志」。官方原话：`Turn it off only in case you are troubleshooting, because Tailscale is quite chatty.` 日志很啰嗦，平时压掉是好事；但排错时线索恰藏在被压掉的部分里，所以先关掉它：

```yaml
log_suppression: false
```

改完记得重启插件（这和第 4.2 节的总原则一致）。

#### 7.4.3 `sysctl` 报 `Read-only file system`（警告① 的报错现场）

如果你照 Linux 子路由教程走了第 2 步，会看到：

```text
[core-ssh ~]$ sysctl -p /etc/sysctl.d/99-tailscale.conf
sysctl: error setting key 'net.ipv4.ip_forward': Read-only file system
sysctl: error setting key 'net.ipv6.conf.all.forwarding': Read-only file system
```

这不是配置错误，是路径错误——你根本不该在 HAOS 上做这一步。维护者回复只有一句：`Please read the docs, it says "follow steps from step 3", because what you want to configure, is already set.` 你想配的 IP forwarding，插件已经代做了。官方 DOCS.md 也写明插件已替你处理 "IP address forwarding" 和 "Clamp the MSS to the MTU"（见第 4.2.1 节）。

> [!warning] 别去 remount 根文件系统
> 看到 `Read-only file system` 就去搜 remount、想把根文件系统挂成可写，是野路子。这一步在 HAOS 上本就不该存在，绕过去只会破坏受管系统完整性。

#### 7.4.4 DNS loop 会让 `hassio_dns` 崩溃

这一节接第 3.4 节那条 `ha dns options --servers dns://100.100.100.100` 命令。它默认是好的，但有一个已知的严重后果：MagicDNS 解析不了某个名字时，**不返回 REFUSED、SERVFAIL 或 NXDOMAIN**，而是回头去问系统原本的 DNS。HA 上那个「原本的 DNS」就是 `hassio_dns`——你又把 `100.100.100.100` 配成它的第一顺位，于是形成 loop，`hassio_dns` 崩溃，连带 supervisor、nginx 出问题。维护者贴出的 coredns 日志原文：

```text
[FATAL] plugin/loop: Loop (172.30.32.1:51675 -> :53) detected for zone ".", see https://coredns.io/plugins/loop#troubleshooting. Query: "HINFO 3773484566690024990.644798792321423444."
[01:09:56] WARNING: Halt DNS plug-in with exit code 1
```

`accept_dns: false` **不是**解法。维护者明确说它会把控制台下发的全局 nameserver 一起废掉：`permanent accept_dns=false disables the DNS config's magical modification, but also disables accepting configured global nameservers by 100.100.100.100 from TS admin page, they won't be called, it would break things.`

维护者一开始的结论是「干脆全局关掉 MagicDNS」，但**第二天自己推翻了**，因为会连带影响普通客户端：`disabling MagicDNS is fine for HA (or other "linux" servers with manual net configs), but bad for general (even DHCP based) win/linux clients -> better figure out how MagicDNS interferes with hassio_dns than to disable it completely`。关掉后 Ubuntu / Win11 连完整域名的解析都会失效。

最后一条安抚性结论：插件停止时，HA 里的 `100.100.100.100` 会被**跳过**，不会导致 DNS 全挂，维护者对此回答 `Yes, will skip it. Tested.` 排查动作：先 `ha dns info` 确认 `servers: []`；要清空列表按官方文档用 `ha dns reset` 加 `ha dns restart`，两条都要执行；`ha` 命令的完整速查见 [[Home Assistant ha 命令使用]]。

### 7.5 四种常见误判，以及一个不要当步骤的「怪招」

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

> [!summary] 本章小结
> - 路由没出现，按 advertise → approve → accept → 本地路由优先级 顺序查，先别怀疑 HAOS。
> - 路由在但流量不通，查 ACL / grants（`tailscale debug netmap` 的 `PacketFilter`）、目标可达性、防火墙；路由和 ACL 两套机制缺一不可。
> - HAOS 特有坑：key 过期会 fail-close；排错先关 `log_suppression`；`Read-only file system` 是路径错误；DNS loop 别用 `accept_dns: false` 或关 MagicDNS 去解。
> - 四种误判里只有「上游路由器参与转发导致回包丢失」可能真涉及路由器配置。

下一章收尾：讲清范围边界、未核验声明，以及什么时候才真正需要 site-to-site。

排错清单按固定顺序逐项排除即可。最后一步是把范围边界和未核验声明交代清楚。

## 第 8 章 边界、未核验声明与下一步

到这里，你已经能自己配好，也能自己验收。但有些结论比另一些更硬，有些需求从来不在本篇范围内。这一章把边界画清楚，免得你把「这个场景能用」误读成「什么都能用」。

### 8.1 什么时候才需要关 SNAT

只有同时满足三个门槛，才谈得上 site-to-site：需要**双向**（LAN 里的设备也要能主动访问 tailnet）、需要**跨多个网段**、并且**两端都要能主动发起**连接。官方把关 SNAT 写成进阶 Site-to-site networking 的开关，对应的是「traverse multiple networks」这类场景，它不是「更彻底」的选项。

关掉它的代价清单：关 `snat_subnet_routes`、确保不走 userspace 网络、再在设备自身的操作系统、你的 VPC 设置或你的 DHCP 服务器上补一条 `100.64.0.0/10` 的回程路由，指向子路由器的 LAN IP。对家用单点需求，这是明确的过度工程。

> [!warning] 本文场景不要执行
> 下面只是让你看清代价，不是步骤。真关了 SNAT，你还得自己补第二条那样的回程路由，而 HAOS 只读，这一步很难照做。

```bash
# 本文场景不要执行：关掉 SNAT 后，回程路由必须由你补齐
tailscale up --snat-subnet-routes=false
# 所需回程路由条目：目标 100.64.0.0/10 → 下一跳为子路由器的 LAN IP
100.64.0.0/10 via <子路由器 LAN IP>
```

### 8.2 本篇的边界与未核验声明

不在本篇范围的能力：exit node、Taildrop、Taildrive，以及多站点的横向对比——它们要么是另一个功能，要么需要另写一篇。

口径分歧方面，对「HAOS 同网段转发能力」确实存在社区与官方不一致的说法。本篇只陈述已核实的反方依据（容器网络路径层面的质疑）与维护者本人的实测，不引用未核验来源，也不转述其内容。

结论强度方面，本篇给的是「官方文档 + 维护者在树莓派实机与 VirtualBox 虚拟机两种 HAOS 部署上的实测」共同支撑的可执行路径。请记住分寸：维护者测的是**双向 site-to-site**，比你的同网段单向场景更难；这也不等于你这套配置必定成功。验收请以第 6 章你自己跑出来的结果为准。

最后一层是单一来源声明：第 4.5 节提到的「HAOS 自带本地路由保护规则」，目前只有一篇个人博客一个来源，未获官方印证，是否采信请按需自行核实。

### 8.3 下一步

同主题还有两篇可作不同部署形态的参照：[[Tailscale使用教程]]（通用使用）与 [[Tailscale子网路由器部署教程]]（fnOS + Docker 部署），本篇只给链接，不展开。若想继续延伸，可以把远程客户端也纳入 tailnet，并用 Serve 给 HA 之外的服务暴露域名和证书（见第 3.3 节）。

## 更新记录

### 2026-09-13 · 澄清 3.4 节的方向性

- **问题**：原标题「3.4 用 tailnet 名字访问」紧接在 3.2/3.3 的 Serve 之后，容易被读成「用名字访问 HA」，从而误以为远程访问 HA 也必须执行 `ha dns options --servers dns://100.100.100.100`。
- **修改**：标题改为「出方向才需要：让 HA 用 tailnet 名字访问别的设备」；开头新增 `[!info]` 方向说明；新增「别把三件事混成一件」对照表（控制台 MagicDNS 开关 / `ha dns options` / `userspace_networking`）；在 7.4.4 的 warning 之后补「什么时候才真的需要它」场景清单；本章小结拆成两条并补方向限定；同步更新目录锚点。
- **结论**：只做「tailnet 设备 → HA」的入方向，**整节 3.4 都不用做**，`userspace_networking` 也保持默认 `false` 不动。名字由发起方解析，HA 侧不需要 DNS 配置。
- **依据**：插件官方文档 DOCS.md 的 `userspace_networking` 与 `DNS` 两节——前者写明开启时得到「one-way access from tailnet clients to your Home Assistant instance」，后者写明「to be able to address **other clients on your tailnet**」才需要 `100.100.100.100`。措辞主语均指向本机去寻址别人，与前文结论一致。
- **未改动**：命令、清空步骤、FQDN 代价、`accept_dns: false` 释义、指向 7.4.4 的风险提示，均保持原样。
