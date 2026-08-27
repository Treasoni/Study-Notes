## 端口暴露与 SSH：serve、funnel 与 Tailscale SSH

前两章解决的是「设备之间互访」：登录、用名字 ping、走子网路由访问内网设备、用 exit node 上网。但还有一类高频需求没解决——**我跑了一个 Web 服务，怎么把它安全地暴露出去**？这一章讲 Tailscale 的端口暴露三板斧：`serve`（只给 tailnet 内成员访问）、`funnel`（对公网开放）、HTTPS 证书自动签发，再顺手把免密钥的 Tailscale SSH 和「把单台机器分享给外部用户」的 Sharing 一起讲掉。全程不用碰路由器、不用手动配证书，命令基本就是一条 `tailscale xxx`。

> 端口暴露本质上是在内网和外部之间「开一个门」，这扇门的带宽上限取决于出口上行，相关结论可以参考 [[内网穿透带宽性能分析]]。

### 3.1 Tailscale Serve：tailnet 内端口暴露

`tailscale serve` 把本机某个端口上的服务挂到你的 tailnet 域名下，只允许 tailnet 内成员通过 HTTPS 访问。典型场景：家里的 NAS 面板、开发环境的前端页面、内网监控面板——只给自己人看，不打算让公网碰。

[!tip] 大白话：把 serve 想成在办公楼里给自家服务开了一个「前台窗口」。访客（tailnet 成员）要刷工牌才能进楼，窗口背后的服务还待在原来的工位上（本地 3000 端口），只是多了一个体面的正门。所以：serve 只对本楼（tailnet）开放，楼外的人看不见它。

v1.52 起 serve 的 CLI 改成新语法 `tailscale serve [flags] target`，下面直接上手。假设你已经在本地跑了一个服务：

```bash
# 目标设备（服务所在机器）终端
# 第一步：先启动一个本地服务，比如 Python 静态服务器
# --bind 127.0.0.1 保证它只监听本机，不直接暴露到局域网
python3 -m http.server 3000 --bind 127.0.0.1

# 第二步：新开一个终端，把它挂到 tailnet 上
# --bg 表示后台持久运行，tailscaled 重启后会自动恢复，不用再敲一次
tailscale serve --bg 3000
```

执行后没有报错就说明已生效。用子命令管理：

```bash
tailscale serve status    # 查看这台设备当前暴露了哪些内容
tailscale serve reset     # 清空这台设备所有 serve 配置
tailscale serve off       # 关闭 serve
```

`status` 的输出长这样，`tailnet only` 表示只有内网成员能访问：

```text
http://monitoring.yak-bebop.ts.net (tailnet only)
|-- http://127.0.0.1:3000
```

几个必须知道的限制：

- **HTTPS 端口只有 443、8443、10000 三个**，不能随便指定，默认走 443。
- 证书由 Let's Encrypt 自动签发（90 天有效），serve/funnel 托管时不需要你管续期；如果要手动签发证书（比如部署到别处），用 `tailscale cert <hostname>.<tailnet>.ts.net`，此时 90 天后需自行续期。[^c3-1][^c3-2]
- 除了 HTTP 反代，serve 还支持三种内容模式：**文件**、**目录**（写绝对路径）、**静态文本**（直接返回 `text:"..."`）。最常用的是 HTTP 反代，后端地址只能是 `http://127.0.0.1`，不会转发到局域网里的其它主机。[^c3-2]

[!warning] 易错点：`tailscale serve off` 关闭时，**启动时用过的 flag 必须原样补全**，缺了会报错。比如你用 `tailscale serve --bg 3000` 启动，关的时候要写 `tailscale serve --bg off`，不能只敲 `tailscale serve off`。[^c3-2]

### 3.2 Tailscale Funnel：公网暴露

如果说 serve 是「楼内前台」，`funnel` 就是直接在临街开的铺面——**任何人都能访问**，不需要在你的 tailnet 里。两者的关系一句话：Serve 只给 tailnet 内，Funnel 给全世界。

```bash
# 目标设备终端
# 把 3000 端口直接暴露到公网（同样支持 --bg 后台持久）
tailscale funnel --bg 3000
```

```text
https://monitoring.yak-bebop.ts.net (Funnel)
|-- http://127.0.0.1:3000
```

Funnel 和 Serve 共用同一套 HTTPS 端口限制（443/8443/10000）和证书自动签发机制，区别只在「谁能访问」——`status` 输出里会明确标出 Funnel。想要「只有 tailnet 内能访问」用 serve，想要「公网也能打开」用 funnel，选错的话暴露范围会差一个数量级。[^c3-1]

需要透传真实客户端 IP 或处理非 HTTP 流量时，serve/funnel 都支持几个高级 flag：

```bash
# 让后端拿到真实客户端 IP（PROXY protocol v1 或 v2）
tailscale serve --bg --proxy-protocol=1 3000

# 后端自己处理 TLS（比如 Caddy 反代、SSH、RDP 这类场景），
# Tailscale 不做 TLS 卸载，只把原始 TCP 流转发到后端的 443 端口
tailscale funnel --bg --tls-terminated-tcp=443 443

# 原始 TCP 转发（同样只限 443/8443/10000 三个端口）
tailscale funnel --bg --tcp=10000 10000
```

[!warning] 安全边界：Funnel 是**公网暴露**，等于把服务直接挂到互联网上。它只负责开「入口」，不帮你做鉴权——登录、限流、防扫描都得靠服务自己。开 Funnel 前先想清楚：这个服务真的需要全世界访问吗？多数场景其实 serve 就够了；如果只是临时给某人看，用 3.4 的 Sharing 更安全。

### 3.3 Tailscale SSH：免密钥 SSH

传统 SSH 要管理公钥、往每台机器写 `authorized_keys`。Tailscale SSH 直接**接管 Tailscale IP 上的 22 端口**，由 Tailscale 控制面统一认证身份，不碰你本机的 `/etc/ssh/sshd_config` 和 `authorized_keys`；局域网或公网来的普通 SSH 流量走原路径，不受影响。[^c3-3]

[!tip] 大白话：把 Tailscale SSH 想成「把钥匙交给物业管家」。以前你要自己配门锁、给每个人配钥匙（authorized_keys、私钥），现在管家（Tailscale 控制面）统一刷卡认证——只要对方在 tailnet 里、ACL 允许，直接 `ssh user@device` 就进去了，不用再交换公钥。

启用分两步：

```bash
# 被登录的那台机器上执行
# 第一步：开启 Tailscale SSH（每台主机只需一次）
tailscale set --ssh

# 第二步：从另一台 tailnet 内设备连接，直接写 MagicDNS 机器名
ssh user@device
# 或写完整 FQDN
ssh user@device.yak-bebop.ts.net
```

[!warning] 易错点——双重放行：光执行 `tailscale set --ssh` 还不够，要连得上必须同时满足两件事：① ACL 里有一条规则允许 src→dst 的**端口 22** 流量；② policy 里存在一条 **ssh 规则**。两者缺一不可。新建 tailnet 的默认 allow-all 恰好同时满足，所以一般感觉不到；但只要你收紧过 ACL，就会遇到「set --ssh 开了还是连不上」的诡异情况。[^c3-3][^c3-4]

ssh 规则写在 policy 文件顶层的 `ssh` 段。先看一个完整例子（先睹为快），再逐字段拆：

```json
// policy.hujson（tailnet policy 文件的 ssh 段）
{
  "ssh": [
    {
      "action": "accept",
      "src":    ["autogroup:member"],
      "dst":    ["tag:server"],
      "users":  ["autogroup:nonroot"]
    }
  ]
}
```

- `action`：`accept`（直接放行）或 `check`（二次确认模式）。
- `src`：发起方，可以是用户、组、tag 或 autogroup。
- `dst`：目标机器，**只能写 tag、`autogroup:self` 或单个用户，端口固定为 22，不能改**。
- `users`：目标机器上允许登录的系统用户，常用 `autogroup:nonroot`（所有非 root 用户），也可以写 `localpart:*@domain`。[^c3-4]

如果希望登录前做二次确认，用 `check` 模式，加 `checkPeriod` 控制确认频率：

```json
// policy.hujson（check 模式示例）
{
  "ssh": [
    {
      "action": "check",
      "src":    ["autogroup:member"],
      "dst":    ["tag:server"],
      "users":  ["autogroup:nonroot"],
      "checkPeriod": "2h"
    }
  ]
}
```

- `checkPeriod` 范围 1min–168h（1 分钟到 7 天），默认 12h，设为 `always` 则每次连接都要重新确认。[^c3-4]
- 多条规则同时命中时**最严格的优先**：`check` 先于 `accept` 生效；撤销某个用户后**秒级生效**，会直接终止其已建立的连接。[^c3-3]
- 注意 `check`（二次确认）模式属付费功能，免费版直接用 `accept` 即可。

限制也要知道：Tailscale SSH 服务端只支持 **Linux / macOS** 的开源 tailscaled（v1.24+），Synology、QNAP 等 NAS 不支持；端口固定 22；`tailscaled` 重启会终止现有 SSH 会话。[^c3-3]

### 3.4 节点分享 Sharing

Sharing 解决另一个问题：**把一台机器临时分享给 tailnet 之外的人**，比如让外部顾问 SSH 到一台服务器。它只分享这一台机器，不暴露你 tailnet 的任何其它内容；分享时会剥离这台机器的 tags、groups、subnet router 等身份信息，对方看到的只是一台「孤立的机器」。[^c3-5]

操作在 admin console 的 Machines 页完成：找到目标机器 → 分享（Share）→ 生成邀请链接发给对方。链接分两种：[^c3-5]

- **单次链接**：一个人用一次就失效；
- **可复用链接**：最多可用 1000 次，且 30 天未被使用会过期。

对方收到链接后，用**任意 Tailscale 账号**登录接受即可，不需要加入你的 tailnet。

几个必须记住的规则：

- 被分享的机器默认 **quarantine（隔离）**：对方可以连进来（入站），但**不能以它为跳板主动发起连接**（出站），避免「分享一台机器 = 给你内网开了个口子」。[^c3-5]
- 对方访问这台机器时**只能用完整域名 `<hostname>.<tailnet>.ts.net`**，不能用短机器名。[^c3-5]
- **带 tag 的机器不能分享**。如果这台机器打了 tag，得先去掉 tag 才能分享。[^c3-5]
- 分享 exit node 需要额外广告路由 + 审批 + 勾选 "Allow use as an exit node"。[^c3-5]
- 这是 beta 功能（v1.4+），所有套餐可用。

如果你想统一限制「被分享进来的外部用户」能访问什么，在 ACL 里用 `autogroup:shared` 指向这群人：

```json
// policy.hujson（ACL 示例）
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:shared"],
      "dst": ["<hostname>.<tailnet>.ts.net"]
    }
  ]
}
```

这样就把外部用户的访问范围收在可控的几台机器内，而不是默认放行。[^c3-5]

### 本章小结

- `serve` 把本地服务只暴露给 tailnet 内成员，`funnel` 对公网开放，两者共用 HTTPS 三端口（443/8443/10000）和 Let's Encrypt 自动签发证书。
- v1.52+ 语法是 `tailscale serve/funnel [flags] target`，管理用 `status` / `reset` / `off`；`--bg` 后台持久，`off` 时 flag 必须补全。
- 高级转发：`--proxy-protocol=1|2` 透传源 IP，`--tls-terminated-tcp=<port>` 适合 Caddy/SSH/RDP，`--tcp=<port>` 做原始 TCP 转发。
- Tailscale SSH 免密钥登录要记住「双重放行」：ACL 端口 22 + ssh 规则缺一不可；ssh 规则 `dst` 只能写 tag/`autogroup:self`/单用户，端口固定 22，`checkPeriod` 默认 12h。
- Sharing 只分享单台机器，对方只能以完整域名访问且默认 quarantine；带 tag 的机器不能分享。

下一章我们从「怎么配」切换到「怎么选、怎么修」：frp / ZeroTier / ngrok 与 Tailscale 的实测对比，以及打洞失败走 DERP 时，如何用 `status` / `ping` / `netcheck` 一步步定位问题。

### 参考来源

[^c3-1]: Tailscale Funnel 命令参考 — https://tailscale.com/docs/reference/tailscale-cli/funnel
[^c3-2]: Tailscale CLI 参考 — https://tailscale.com/docs/reference/tailscale-cli
[^c3-3]: Tailscale SSH — https://tailscale.com/docs/features/tailscale-ssh
[^c3-4]: Tailnet policy file 语法 — https://tailscale.com/docs/reference/syntax/policy-file
[^c3-5]: 节点分享 Sharing — https://tailscale.com/docs/features/sharing
