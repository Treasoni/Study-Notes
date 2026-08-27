## 常用功能实战：MagicDNS、ACL、子网路由与 Exit Node

上一章我们把设备装好客户端、登录进 tailnet，每台设备都拿到了固定的 `100.x.y.z` 内网地址。但裸 IP 不好记，默认的"全放行"策略在设备变多时也不安全。这一章把四个日常最高频的能力一次讲透：用名字访问设备（MagicDNS）、控制谁到谁的访问（ACL）、把整个局域网带进 tailnet（子网路由）、借一台设备的公网出口上网（Exit Node）。掌握这四件事，你就能解决远程访问 80% 的日常场景；对 NAT、P2P 打洞这些底层机制还有疑问的话，可以随时翻一下 [[内网穿透带宽性能分析]]。

### 2.1 MagicDNS：用名字访问设备

Tailscale 会给每台设备自动注册一个"内网域名"，这就是 MagicDNS。默认启用，不需要任何配置——新创建的 tailnet 在 2022-10-20 之后默认开启，客户端 v1.20+ 也无需手动配置 nameserver[^c2-1]。开启后你可以直接用机器名访问：

```bash
$ ping monitoring                # 不需要记 100.101.102.103
PING monitoring (100.101.102.103): 56 data bytes

$ ssh user@monitoring            # 同样适用
```

MagicDNS 的完整域名（FQDN）由**机器名 + tailnet DNS 名**组成，例如 `monitoring.yak-bebop.ts.net`；tailnet 会自动给设备追加 search domain，所以短名字 `monitoring` 就能解析[^c2-1]。

> [!tip] 大白话：MagicDNS 就是 tailnet 内部的"通讯录"
> 把 MagicDNS 想成小区物业自动维护的通讯录：每台设备入网时自动登记"姓名→房号（100.x）"的对应关系，还帮你把门牌号后缀补全。所以你不必背 100.101.102.103 这种门牌号，喊一声 `monitoring` 就能找到对方。

如果你在某台设备上不想用 MagicDNS（比如它本身要跑自己的 DNS），可以只在这台设备上关掉：

```bash
sudo tailscale set --accept-dns=false     # 关闭后只影响本机
sudo tailscale set --accept-dns=true      # 重新开启
```

macOS / Windows 没有对应 CLI 开关，需要在客户端 GUI 的 DNS 设置里关闭[^c2-1]。

> [!warning] macOS 易错点：`host` / `nslookup` 不适用
> macOS 上 `host monitoring` 和 `nslookup monitoring` 会绕过系统 DNS 直查公网 DNS，解析不出 tailnet 内部名字；但 `ping`、`ssh` 走系统解析，所以能用。判断 MagicDNS 是否生效，请用 `ping` 或 `dscacheutil -q host -a name monitoring`，别被 `host`/`nslookup` 的结果误导[^c2-1]。

另外提醒：早期教程里的 `*.beta.tailscale.net` 域名后缀已于 2024-09-13 停用，现在统一是 `*.ts.net`，照旧教程排错时别被带偏[^c2-1]。

### 2.2 ACL 基础：从默认放行到收紧

ACL（Access Control List）决定 tailnet 里**谁（src）能访问谁（dst）**。Tailscale 的安全原则是 deny-by-default，但**新建的 tailnet 默认策略却是全放行**，所以别以为"能用 = 已经安全"[^c2-2]。

> [!tip] 大白话：ACL 就是一张授权清单
> 把 ACL 想成大楼门禁的授权表：每行写"某人 → 能进某房间"。默认情况下这栋楼不设防（allow all）；你在清单里写了任何一条规则后，没写到的组合就默认进不去。所以加规则 = 开始"上锁"。

关键心法（三个坑一次记牢）：

- **无 `acls` 段 = allow all，空对象 `{}` = deny all**。如果你在 Admin Console 里打开 Access Controls，看见的是一个 `{}` 空对象——这是 deny all，不是默认放行！新建 tailnet 的默认放行来自"存在一条隐式的全放行规则"，一旦你保存了自己的 `acls` 段，就按你写的来[^c2-2]。
- **规则有方向性**：允许 `laptop → server` 不等于 `server → laptop` 也能通，反向访问要单独再写一条[^c2-2]。
- **免费版不能写端口级规则**：目标只能写 Any（`*`）、IP、CIDR、Autogroup、Group、User、Tag、Hosts、IP sets；`dst` 里带 `:端口` / `:协议` 属于 Premium/Enterprise 专属功能[^c2-2]。

全放行（等价于新建 tailnet 的默认行为）：

```json
{
  "acls": [
    { "action": "accept", "src": ["*"], "dst": ["*:*"] }
  ]
}
```

收紧——只允许 `alice@example.com` 访问 `monitoring`，其余全部拒绝：

```json
{
  "acls": [
    { "action": "accept", "src": ["alice@example.com"], "dst": ["monitoring"] }
  ]
}
```

> [!warning] 免费版易错点：`dst` 别写端口段
> 免费版写规则时，`dst` 写成 `"monitoring"`、`"100.101.102.103"` 或 `"*"` 即可，等价于放行该目标的全部端口；`":22"`、`":tcp"` 这类端口/协议写法是 Premium/Enterprise 才支持。你在免费版里写了端口段，规则要么不生效要么报错，先用无端口写法。

ACL 由 tailnet 内每台设备本地强制执行（不依赖中心代理），编辑入口在 Admin Console，也可走 GitOps / API[^c2-2]。规则配错最常见的症状是：`tailscale ping` 能通、但访问具体服务超时——先查 ACL 是不是把端口写死了。

### 2.3 子网路由 Subnet Router

场景：家里一台 Raspberry Pi 连着打印机、路由器管理页，你在公司想直接访问它们。它们装不了 Tailscale？没问题——让 Pi 当**子网路由器（subnet router）**，把整个局域网"代理"进 tailnet。核心三步 + 两步收尾[^c2-3]：

**第一步，在路由设备上开启 IP 转发。** 因为流量要在一个网卡（Tailscale 虚拟网卡）和另一个网卡（局域网口）之间转发：

```bash
# /etc/sysctl.d/99-tailscale.conf
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

```bash
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
```

**第二步，广播你要代理的网段**（把示例网段换成你家路由器实际的局域网网段，如 `192.168.1.0/24`）：

```bash
sudo tailscale set --advertise-routes=192.0.2.0/24,198.51.100.0/24
```

**第三步，去 Admin Console 审批**：Machines 页 → 点对应设备 → Edit route settings → 勾选要批准的 route → Save。**审批不通过，路由就不生效**，这是配完"看起来对但访问不了"的高频原因[^c2-3]。

**第四步，在客户端接受路由**：

```bash
sudo tailscale set --accept-routes
```

> [!warning] 平台差异：`--accept-routes` 默认值不一致
> Windows、iOS、Android、macOS（App Store 与 standalone 版）默认就接受子网路由；**但 Linux 等其余平台默认不接受**。所以在 Linux 客户端上，`--accept-routes` 这一步不能省——多数"我明明审批了为什么访问不了子网"的问题就出在这[^c2-5]。

**关于 SNAT**：`--snat-subnet-routes` 是仅 Linux 可用的 flag，默认开启。开启后，子网里的普通设备看到的连接来源是路由器的 Tailscale IP（`100.x`），而不是你设备的 IP；好处是子网内设备零配置就能回包，代价是丢了真实来源 IP。只有需要保留源 IP 的场景才关掉它[^c2-5]。

### 2.4 Exit Node

Exit Node 是"整台设备当网关"：它把你的默认路由（`0.0.0.0/0` 和 `::/0`）接过来，**所有公网流量先加密到这台设备，再由它的公网 IP 发出去**，效果类似传统 VPN[^c2-4]。典型场景：公共 Wi-Fi 防窃听、访问只对特定国家/地区开放的服务、隐藏自己设备的公网 IP。

> [!tip] 大白话：Exit Node 就是替你出门办事的门卫
> 你的所有"出门"请求（访问公网）不再自己直接出去，而是先加密送到门卫（exit node），由门卫用他自己的门禁卡（公网 IP）替你出去。所以别人看到的是门卫的地址，不是你的；在公共 Wi-Fi 这种"坏小区"里特别安全。

**发布（在当出口的设备上）**：

```bash
sudo tailscale up --advertise-exit-node
```

GUI 客户端则在 Settings → Exit Node 里勾选 Run as exit node[^c2-4]。

**审批**：Admin Console → Machines 页 → 勾选该设备 Use as exit node。想省去手动审批，可以在 policy file 里加 `autoApprovers.exitNode` 自动批准指定用户发布的出口[^c2-4][^c2-6]：

```json
{
  "autoApprovers": {
    "exitNode": ["user@example.com"]
  }
}
```

**使用（在任意客户端上）**：

```bash
sudo tailscale set --exit-node=<ip或机器名> --exit-node-allow-lan-access
```

- `--exit-node=<ip|name>`：指定出口，可以是 `100.x` IP 或机器名[^c2-5]。
- `--exit-node-allow-lan-access`：默认**禁止**在走出口的同时访问本地 LAN。开了 exit node 后发现打不开自家打印机/路由器管理页，就是这个 flag 没加[^c2-5]。

**验证**：走出口后查公网 IP，应显示为出口设备的公网 IP：

```bash
$ curl ifconfig.me
203.0.113.9
```

> [!warning] Exit Node 与 ACL 的两个坑
> 1. **自定义 ACL 后必须放行 `autogroup:internet`**：一旦你写过自己的 `acls`，客户端就无法把 exit node 当网关转发公网流量，除非显式加一条规则：
>    ```json
>    { "action": "accept", "src": ["alice@example.com"], "dst": ["autogroup:internet"] }
>    ```
> 2. **把 exit node 设备写进 `dst` 只表示"能连到它"，不表示"能把它当网关"**。例如 `dst: ["100.66.5.2"]` 只是允许你 SSH 到那台设备；要走它的公网出口，必须用上面 `autogroup:internet` 那条[^c2-4]。

最后一条安全兜底：作为出口的那台设备 key 过期时，tailnet 会 fail close——宁可断流也不会把流量悄悄改走其他路径，避免流量泄漏。这也是 exit node 比随手搭的代理更可信的原因[^c2-4]。

### 本章小结

- MagicDNS 让 tailnet 内直接用机器名访问，FQDN = 机器名 + tailnet DNS 名；Linux 用 `set --accept-dns` 控制开关，macOS 上 `host`/`nslookup` 不适用但 `ping` 可以。
- ACL 默认全放行：无 `acls` 段 = allow all，空对象 `{}` = deny all；规则严格有方向性；免费版不能写端口级规则。
- 子网路由 = 三步走（开 IP forwarding → `set --advertise-routes` → 审批）+ 客户端 `set --accept-routes`；`--accept-routes` 在 Linux 上默认关闭，最容易漏。
- Exit Node 通过 `0.0.0.0/0`、`::/0` 转发全部公网流量；自定义 ACL 后必须放行 `autogroup:internet`，把出口当 `dst` 并不等于能当网关。

下一章我们把方向反过来：用 `tailscale serve` 把本机端口暴露给 tailnet、用 `tailscale funnel` 暴露到公网并自动签发 HTTPS 证书，再加免密钥的 Tailscale SSH 与单机分享——远程访问的"输入"和"输出"就都齐了。

## 参考来源

[^c2-1]: MagicDNS — https://tailscale.com/docs/features/magicdns
[^c2-2]: ACLs 入门 — https://tailscale.com/docs/features/access-control/acls
[^c2-3]: Configure a subnet router — https://tailscale.com/docs/features/subnet-routers/how-to/setup
[^c2-4]: Exit nodes — https://tailscale.com/docs/features/exit-nodes
[^c2-5]: Tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c2-6]: Tailnet policy file — https://tailscale.com/docs/reference/syntax/policy-file
