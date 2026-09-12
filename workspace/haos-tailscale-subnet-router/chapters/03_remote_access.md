# 第 3 章 内网穿透：不开口、不做反代就远程访问

外网要打开家里的 HA，传统做法是端口转发或反向代理，代价都是要在路由器上开口子。这一章走另一条路：HA 已经是 tailnet 上的设备，顺着 Tailscale 自己的能力把它露出来就够了——不开端口、不做反代。先用 tailnet IP 拿到「能用」，再用 Serve 拿到「好用的域名 + HTTPS」。

## 3.1 最小可用路径：先能用

授权完成之后，你其实已经能远程访问了：在任意一台连着 tailnet 的设备上，用 HA 的 tailnet IP 加端口访问即可。这是 Tailscale 的默认能力，不是你额外配出来的，官方博客的原话是「without opening ports or setting up proxies」[^c3-blog]。

> [!tip] 大白话
> 把 tailnet 想成一间公司内网：tailnet IP 就是分机号，只要双方都在这个内网里，拨号就通。你要做的不是去电信局申请外线（端口转发），而是确认自己已经在网内。

先别急着做 Serve。用一台真正不在家里的设备（手机关 Wi-Fi 走蜂窝最省事）访问一次，确认这条最朴素的路能走通。它是基线：后面的故障都能被它切成「隧道不通」还是「只有域名层不通」。

## 3.2 更好的路径：Serve 给一个域名和证书

直接用 IP 加端口能访问，但浏览器会提示不安全（它不知道 tailnet 内部的连接是端到端加密的），URL 也难记。Serve 能给 HA 一个带有效证书的 tailnet 域名，一次解决这两件事。

它有两处前置。

HA 侧：关闭 SSL/TLS，让 HA 以 HTTP 提供服务——Settings → System → Network → HTTP server → SSL/TLS。然后在同一区块展开 Reverse proxy：启用 `Trust X-Forwarded-For`，把 `127.0.0.1` 加进 `Trusted proxies`，保存（保存会重启 HA 界面）。

Tailscale 控制台的 DNS 页：改一个顺眼的 tailnet 名，确认 MagicDNS 已启用，并在 HTTPS Certificates 一节 Enable HTTPS。

> [!tip] 大白话
> Serve 像在 HA 门口盖了间门卫室：手机先找到门卫室（域名 + 证书），再由它领你进 HA。门卫室设在本机门口，所以 HA 眼里访客永远从「本机」来——这正是 3.2.1 要讲的。

对应的插件配置项是这两行：

```yaml
share_homeassistant: disabled   # 默认值；启用 Serve 时按配置页下拉框改
share_on_port: 443
```

`share_on_port` 只能填 443、8443、10000 三个端口之一，默认就是 443。首次设置后，域名可能要最多 10 分钟才会生效，别刚点完就下结论。

还有两条容易踩：不要再把原来那个端口号拼进 URL；如果浏览器行为古怪或报奇怪的错，先清掉该站点的 cookie 和缓存、重启浏览器。

### 3.2.1 为什么 `Trusted proxies` 填 `127.0.0.1` 而不是 `100.64.0.0/10`

因为 HA 看到的连接不是从你的 tailnet IP 直接来的，而是从本机的 Serve 代理转过来的，所以可信代理要写回环地址。插件官方文档和 Tailscale 官方博客在这里口径一致，都写 `127.0.0.1`[^c3-docs][^c3-blog]。

> [!warning]
> 这是新手最容易填错的地方。不要因为「访问来自 tailnet」就填 `100.64.0.0/10`——那样 HA 不认这个代理，Serve 转发过来的请求照样被挡。

## 3.3 Funnel 与 `services`：先别急着开

Funnel 和 Serve 长得像，方向却相反：它会把 HA 暴露到公网，连不装 Tailscale 客户端的设备也能访问。这跟本章「不开口」的初衷正相反，官方博客的说法是「You almost certainly do not want Funnel」[^c3-blog]。普通远程访问用 Serve 就够，不要顺手把 Funnel 打开。

`services` 选项解决另一个需求：用同一个域名把插件商店里的其他服务也露出来（文档举的例子是 audiobookshelf）。它有两条硬约束——只支持 Serve、不支持 Funnel；节点还必须先打上 tag 才能用。

## 3.4 用 tailnet 名字访问：MagicDNS 怎么接才不炸

想让 HA 用 tailnet 名字访问别的设备，前提是 `userspace_networking` 处于关闭状态：只有关闭时，Tailscale 才会提供 `100.100.100.100` 这个 DNS。

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

> [!warning]
> 上面那条 `ha dns options` 有一个已知的严重后果，现象、成因与修法在第 7 章 7.4.4 节。照做之前先读那一节，别等 DNS 挂了再回头找。

## 3.5 直连还是中继：要不要开 `always_use_derp`

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
> - MagicDNS 靠 `ha dns options` 接，持久化、只需一次，代价是必须用 FQDN；`always_use_derp` 默认别开。

下一章把视角从「访问 HA 自己」扩到「访问 HA 所在的整个局域网」——配置子路由，把 HAOS 变成 tailnet 的网关。

[^c3-docs]: hassio-addons/app-tailscale DOCS.md（插件官方文档）— https://raw.githubusercontent.com/hassio-addons/app-tailscale/refs/heads/main/tailscale/DOCS.md
[^c3-blog]: Tailscale 官方博客《Remotely access Home Assistant via Tailscale for free》— https://tailscale.com/blog/remotely-access-home-assistant
[^c3-dns]: hassio-addons/app-tailscale Discussion #449（DNS / MagicDNS 与 hassio_dns）— https://github.com/hassio-addons/app-tailscale/discussions/449
