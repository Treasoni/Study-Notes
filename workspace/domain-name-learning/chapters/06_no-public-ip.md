# 第6章 没有公网 IP 也能用域名——Cloudflare Tunnel / frp+Caddy / Tailscale Funnel

到第 5 章为止，我们默认的路径都是「你有公网 IP，DNS 解析到你家或服务器，Caddy/Nginx 在 80/443 接客」。但真实世界经常不满足这个前提：家用宽带往往在运营商 NAT 后面，并没有一个独享的公网 IPv4；公司、校园或某些小区宽带还会封掉入站端口。本章要解决的问题是：**没有公网 IP（或不便开入站端口）时，怎么让一个域名访问到你内网的服务？**

答案不是把公网 IP「变出来」，而是换一个思路——**让内网的一台设备主动「出站」，去连接一个公网可达的中间方**。访客永远只访问这个中间方，中间方再通过那条已经建立的出站通道，把请求送进你的内网。本章对比三种最常见的落地方式：Cloudflare Tunnel、frp + Caddy、Tailscale Funnel，并给出可复制的接入配置。

## 6.1 场景与三方案概览

先判断你是否需要本章。出现下面任一情况，就属于「没有公网 IP」的赛道：

- **无公网 IP**：你的宽带处于 CGNAT / 运营商大内网，路由器 WAN 口拿到的是运营商私网地址，端口映射无从谈起；
- **有 IP 但不便开入站**：有公网 IP，但 80/443 被运营商封锁，或你出于安全考虑不想给内网服务开任何入站端口。

三条方案的共同骨架是「出站隧道」，区别只在于**谁在公网替你接客、要不要你自己的域名、要不要一台自建 VPS**。先看总览表：

| 对比维度 | Cloudflare Tunnel | frp + Caddy | Tailscale Funnel |
| --- | --- | --- | --- |
| 谁在公网接客 | Cloudflare 边缘节点 | 你自己的 VPS（frps + Caddy） | Tailscale 基础设施 |
| 需要自有域名？ | **是**，且须把域名托管到 Cloudflare | **是**（一个主域 + 子域/泛解析） | **否**，只能用分配的 `ts.net` 域名 |
| 需要自建 VPS？ | 否 | **是** | 否 |
| 入站端口要求 | 零入站（cloudflared 只出站） | VPS 需开 443 与 frp 控制/数据端口 | 仅 443/8443/10000，由 Funnel 托管 |
| TLS 证书归谁管 | Cloudflare 边缘托管 | Caddy 自动签发（HTTP-01 / DNS-01） | tailnet HTTPS 自动签发 `.ts.net` 证书 |
| 大陆访问与合规差异 | 流量走 CF 全球边缘，大陆访问延迟/稳定性波动明显（经验）；合规看源站物理位置，套隧道≠免备案 | 取决于 VPS 机房位置；香港/海外免备案但大陆访问有波动，大陆机房则需备案 | 经 Tailscale 中继，大陆可用性不保证、域名也不受你控制（经验） |
| 一句话适用 | 有域名、愿托管 CF、想零入站 + CDN/WAF | 有 VPS、想自持 DNS 与控制面、长期多子域 | 临时演示 / 内部工具 / 还没买域名 |

上表「大陆访问与合规差异」一栏属于**社区经验与政策解读**，不是各厂商的功能承诺[^c6-6][^c6-7]。后面 6.5 会专门提醒：**把「工具的功能承诺」和「大陆访问/合规现实」分开评估**，别因为用了某个隧道就误以为「免备案」或「大陆快」。

## 6.2 Cloudflare Tunnel

这一节的目标很单一：**把内网服务映射成一个公网 HTTPS 主机名，但内网机器一个入站端口都不开**。

**原理与前提。** Cloudflare Tunnel 的核心是一个叫 `cloudflared` 的小进程，装在你的内网机器上。它**主动出站**连接到 Cloudflare 边缘并维持一条加密长连接；你在 Cloudflare 侧把某个公网主机名（如 `app.example.com`）「路由」到这条隧道上。访客请求先落到 Cloudflare 边缘，边缘把请求交给隧道，`cloudflared` 再转给你内网的 HTTP/TCP/SSH 服务[^c6-1]。

关键点：

- **不需要公网 IP，也不需要任何入站端口**——`cloudflared` 只会主动往外连[^c6-1]；
- **前提是域名托管在 Cloudflare**——「公网主机名 → 隧道」的映射挂在 CF 的 DNS / Zero Trust 上，第 4 章讲的「把 NS 切到 Cloudflare」在这里就是前置步骤[^c6-1]；
- 因为公网流量必经 CF 边缘，**CDN / WAF / DDoS 防护会随 Tunnel 一起生效**[^c6-1]；
- 支持映射的不止 HTTP，TCP / SSH 也在能力范围内，本章示例用 HTTP 讲通主线[^c6-1]。

> [!tip] 大白话：出站隧道
> 把 `cloudflared` 想成一位「住你家、每天主动出门到全球网点报到」的管家。访客不需要知道你家门牌号（公网 IP），只要去网点（CF 边缘）说「我要找 app.example.com」，网点就喊管家从后门把人领进来。你家甚至可以没有门牌号（无公网 IP），只要管家能出门（能出站联网）就行。
> 所以 Tunnel 的实质收益是：**内网设备对公网零入站可达**，攻击面被收窄到你主动选择暴露的那几个公网主机名上。

**最小接入配置。** 下面是官方 quickstart 的最小操作序列。命令以 `cloudflared tunnel --help` 与你安装版本为准，这里按 C2 描述的行为模型组织，不逐条复刻官方原文。

先做一次性授权并创建隧道：

```bash
# 1) 授权：会打开浏览器，让你选择 Cloudflare 账号与域名
cloudflared tunnel login

# 2) 创建一条命名隧道（成功后打印隧道 ID，并在 ~/.cloudflared/ 下生成凭据文件）
cloudflared tunnel create my-home
```

接着是核心的配置文件。**先睹为快**：

```yaml
# /etc/cloudflared/config.yml
tunnel: my-home                      # 与上一步创建的隧道名一致
credentials-file: /root/.cloudflared/<隧道ID>.json   # create 时生成的凭据文件

ingress:
  - hostname: app.example.com        # 公网主机名（前提：example.com 已托管在 CF）
    service: http://localhost:3000   # 映射到你内网的 HTTP 服务
  - service: http_status:404         # 兜底规则：没匹配到的主机名统一返回 404
```

逐段拆讲：

- `tunnel` + `credentials-file`：告诉 `cloudflared` 用哪条命名隧道、用哪个凭据文件去连接 CF 边缘。凭据文件是 `cloudflared tunnel create` 时自动生成的。
- `ingress` 是**从上到下逐条匹配**的路由表：请求的 Host 命中 `app.example.com`，就转发到 `http://localhost:3000`（你内网那个真实服务）。
- 最后一条 `service: http_status:404` 是**兜底表达式**——任何没匹配到 `hostname` 的请求都回 404，避免隧道被当开放代理乱用。

最后把公网主机名指到隧道并启动：

```bash
# 3) 把 app.example.com 路由到这条隧道（自动在 CF DNS 生成对应记录）
cloudflared tunnel route dns my-home app.example.com

# 4) 前台启动（生产环境建议用 systemd / Docker 守护）
cloudflared tunnel run my-home
```

完成这四步后，浏览器访问 `https://app.example.com` 应该能看到内网服务。以后要加服务，只需在 `ingress` 里增加一条 `hostname → service` 映射并重启 `cloudflared`。证书、跳转、WAF 这些都在 CF 边缘处理，内网侧不用管 PEM、不用开 443。

> [!tip] 大白话：为什么「域名托管在 CF」是硬前提
> 「公网主机名 → 隧道」这张对应表存在 Cloudflare 的 DNS 里，就像访客名单存在网点前台。如果域名解析不在 CF，CF 就不知道 `app.example.com` 该交给哪条隧道。
> 所以这条路的前提是第 4 章那个动作：把域名的 NS 切到 Cloudflare。

## 6.3 frp + Caddy TLS 终止（自建 VPS 组合）

Cloudflare Tunnel 的代价是「域名要托管到 CF」。如果你已经有一台 VPS，想把 DNS、证书、服务控制面都留在自己手里，frp + Caddy 是自建派的主流选择。分工是：

- **frp** 负责「内网拨号到 VPS」的隧道：内网机器跑 `frpc` 主动出站连上 VPS 的 `frps`，并声明「我负责哪个域名」；
- **Caddy** 负责 VPS 上的 **TLS 终止与反向代理**：对公网持有证书，收到 HTTPS 后解密，再以明文 HTTP 转发给 frps 的虚拟主机端口。

为什么非要 Caddy 这一层？因为 **frp 的虚拟主机入口工作在明文 HTTP 层，不做 TLS 终止**——它只按 Host 头把请求路由给对应的 `frpc`[^c6-3]。下面这张拓扑图把完整链路画出来：

```text
公网访客
   │  https://app.edge.example.com
   ▼
┌─────────────────────────── VPS（有公网 IP）───────────────────────────┐
│  Caddy :443（TLS 终止，自动持有证书）                                  │
│     │  reverse_proxy 127.0.0.1:8080                                    │
│     ▼                                                                  │
│  frps  vhostHTTPPort :8080（按 Host 头路由，明文 HTTP）                │
└───────────────────────────┬──────────────────────────────────────────┘
                            │  frpc 主动建立的出站长连接
┌───────────────────────────▼──────────────────────────────────────────┐
│  内网机器（无公网 IP）：frpc ──▶ 本地 HTTP 服务 :3000                    │
└──────────────────────────────────────────────────────────────────────┘
```

**frps 端配置。** 在 VPS 上跑 frp 服务端。**先睹为快**：

```toml
# /etc/frp/frps.toml
bindPort = 7000        # frpc 拨号上来的控制端口（VPS 安全组需放行）
vhostHTTPPort = 8080   # 关键：虚拟主机 HTTP 入口，按 Host 头路由到对应 frpc
```

逐段拆讲：

- `bindPort`：`frpc` 主动连上来的控制端口，也是两者维持长连接的端口；
- `vhostHTTPPort`：**本章的关键参数**——frp 在这里开一个「虚拟主机」HTTP 入口，所有走这个端口的请求按 Host 头分发给不同的 `frpc`。一个端口就能服务多个域名的内网服务[^c6-3]。

**frpc 端配置。** 在内网机器上跑 frp 客户端。**先睹为快**：

```toml
# frpc.toml
serverAddr = "vps.example.com"   # frps 所在 VPS 的地址（IP 或域名）
serverPort = 7000                # 与 frps 的 bindPort 对应

[[proxies]]
name = "myapp"
type = "http"                    # http 虚拟主机类型：frps 按 Host 头路由到这条代理
localIP = "127.0.0.1"
localPort = 3000                 # 你内网真实的 HTTP 服务
customDomains = ["app.edge.example.com"]  # 访客带这个 Host 访问 vhostHTTPPort 时，路由到这里
```

逐段拆讲：

- `serverAddr` / `serverPort`：告诉 `frpc` 去哪里拨号（你的 VPS）；
- `type = "http"` + `customDomains`：声明这是一条 **HTTP 虚拟主机代理**，并把自己认领的域名报给 frps。frps 在 `vhostHTTPPort` 收到某个 Host 的请求时，就查这张表找到你这条隧道，转发回 `localIP:localPort`[^c6-3]；
- 一条 `frpc.toml` 里可以写多个 `[[proxies]]`，每个认领不同子域——这就是「一个 8080 端口按 Host 路由多个内网服务」的由来。

此时两个进程起来后，访问 `http://VPS:8080` 并带 `Host: app.edge.example.com` 已经能打通内网。但公网用户要的是 HTTPS，所以还差 Caddy。

> [!tip] 大白话：vhostHTTPPort 像公寓前台
> frps 的 `vhostHTTPPort` 就像一栋只有一个大门的公寓前台。访客进门喊一句「我找 myapp」（Host 头），前台看一眼名单（customDomains）就把他领到对应房间（某条 frpc 隧道）。所以**一个端口能同时服务很多个不同域名的内网服务**，前提是每个 frpc 都声明自己认领哪个域名。

**Caddy 端：TLS 终止与反代。** 单服务最小版完整文件先睹为快：

```caddyfile
# /etc/caddy/Caddyfile
app.edge.example.com {
    reverse_proxy 127.0.0.1:8080   # 反代到 frps 的 vhostHTTPPort
}
```

逐段拆讲：

- 这一步的前提是 DNS 里 `app.edge.example.com` 指向 VPS 的公网 IP，且 VPS 的 80/443 公网可达——这正是第 5 章 5.3 讲的 Caddy 自动 HTTPS 触发条件：A 记录指向本机 + 端口可达 + 配置里写了域名[^c6-5]；
- Caddy 会自动用 ACME 为 `app.edge.example.com` 签证书并续期，默认 80→443 跳转[^c6-5]；
- `reverse_proxy 127.0.0.1:8080` 把解密后的明文 HTTP 交给本机 frps 的 `vhostHTTPPort`；frps 再按 Host 头把请求送进隧道。**注意 8080 只需要在本机可达，不必对公网开放**。

> [!warning] frp 不做 TLS 终止
> frp 的虚拟主机入口工作在**明文 HTTP 层**：它按 Host 头转发，但**不会**把你的 `http://` 源站自动升级成公网可用的 `https://`。想让对外是 HTTPS，有三条路，别指望 frps 自己完成：
> 1. **本地服务本身就是 HTTPS**——frp 原样转发（frp 的 https 代理要求源站已经是 HTTPS，frps 不帮你终结 TLS）[^c6-3]；
> 2. **frpc 侧挂 `https2http` 类插件**，让 frp 链路内部做「外部 HTTPS → 内部 HTTP」转换[^c6-3]；
> 3. **在 VPS 前置 Caddy/Nginx 终结 TLS**（本小节做法）：Caddy 对外持证书，frps 只保留 `vhostHTTPPort` 走明文 HTTP。
>
> 直接把 `vhostHTTPPort` 裸奔给公网 = 访客只能拿到明文 HTTP，没有证书、没有域名体验。

> [!tip] 大白话：TLS 终止的分工
> 把 Caddy 想成大厦门口的**安检门卫**，frps 是里面的**前台**。门卫负责「验明正身、拆开加密包裹」（TLS 终止），前台只管按收件人名字把包裹送到对应房间。frp 这个前台**不会拆包裹**——如果你直接让它收 HTTPS 包裹，它只认「包裹本来就是拆好的」（源站已是 HTTPS），否则就要在源站侧加个能拆包裹的插件（https2http）。

**多子域升级：通配证书 + DNS-01。** 上面的单服务写法每加一个子域就要在 Caddyfile 加一段。要服务一堆子域（`app.edge`、`blog.edge`、`api.edge`……），更省事的是让 Caddy 持一张 `*.edge.example.com` 通配证书[^c6-4]。完整文件先睹为快：

```caddyfile
# /etc/caddy/Caddyfile —— 通配升级版
*.edge.example.com {
    tls {
        dns <你的DNS商的插件> <凭据>   # 占位：具体写法见对应 caddy-dns 插件文档
    }
    reverse_proxy 127.0.0.1:8080
}
```

拆讲与提醒：

- **Let's Encrypt 的通配证书强制走 DNS-01**，Caddy 需要你 DNS 商的凭据去写一条 TXT 记录，而不是开放 80 端口验证[^c6-5]；
- Caddy 2.10+ 拿到通配证书后，会自动用它服务配置里的所有子域[^c6-5]；
- 这样 frpc 那边新增一条 `customDomains` 子域时，Caddy 配置不用动——前提是新增子域（或泛解析）也指向 VPS；
- **测试/反复签发务必先切 LE staging**，否则可能被限流封禁最长一周（衔接第 5 章 5.4 的提醒）[^c6-5]。

## 6.4 Tailscale Funnel

如果你**连域名都还没买**，或者只想给同事/自己快速看一个效果，Funnel 是三条路里最短的。它建立在 Tailscale 的 tailnet 之上：你的机器加入 tailnet 后，一行 `tailscale funnel 3000` 就把本机的 3000 端口暴露成一个**公网 HTTPS URL**，形如 `https://<主机名>.<你的tailnet>.ts.net`[^c6-2]。

```bash
# 1) 安装并登录，让设备加入你的 tailnet
tailscale up

# 2) 前置：到 admin 控制台打开 MagicDNS 与 HTTPS Certificates
#    （公网 URL 需要可解析的 ts.net 名字 + 一张 .ts.net 证书）
#    https://login.tailscale.com/admin/dns

# 3) 一行暴露：把本机 3000 端口的服务放上公网（确保该端口确有服务在监听）
tailscale funnel 3000
# 输出形如：https://<主机名>.<tailnet>.ts.net  （C3）

# 4) 查看当前 funnel 状态 / 关闭
tailscale funnel
tailscale funnel off
```

前置条件与边界（来自官方文档）：**MagicDNS + tailnet HTTPS 要先行开启**，Funnel 才能拿到 `ts.net` 的名字和证书[^c6-2]。

> [!tip] 大白话：Funnel 发的是「临时工牌」
> 把 Funnel 想成公司前台发的临时工牌：好用、五分钟就办好，但**工牌上印的是公司的地址（ts.net），不是你自己设计的门牌**。演示完、访客散了，工牌一收就恢复原状。
> 所以 Funnel 适合「临时给个公网入口看看效果」，不适合需要把服务长期挂在自己域名下的正式项目。

Funnel 的硬边界（务必记牢）：

- **只能绑 `ts.net` 域，不能绑自有域名**——证书是 tailnet 自动签的 `.ts.net` 证书，浏览器信任的是这个 ts.net 名字，换不成你自己的域名[^c6-2]；
- **只有 443 / 8443 / 10000 三个端口可以被 Funnel**，不是任意端口都能开[^c6-2]；
- **带宽受限**——官方只表述为受限，未公开具体数值（本批研究的开放问题，不臆造额度），只适合演示与低流量场景[^c6-2]；
- 证书/域名都由 Tailscale 托管，访问质量取决于 Tailscale 基础设施与你所在网络的连通情况（经验）。

> [!note] 和第 5 章的一个交叉点
> Caddy 对 `.ts.net` 这类域名不会走 ACME 自动签证书，而是在握手时向本机 Tailscale 取证书[^c6-5]。所以别试图在 Funnel 前面再叠一层 Caddy 来「换掉」ts.net 域名——Funnel 的域名绑定是它自己定的，不是靠反代能改的。

## 6.5 选型与边界提醒

**怎么选。** 按三步决策，不用纠结：

1. **没有域名、只想临时开个公网 URL**（给同事看 demo、自己在外网访问家里工具）→ **Tailscale Funnel**；
2. **有域名，愿意把解析托管到 Cloudflare**，想要零入站 + 自带 CDN/WAF，不想养 VPS → **Cloudflare Tunnel**；
3. **有域名也有 VPS**，想把 DNS、证书、服务控制面都留在自己手里、长期跑多个子域 → **frp + Caddy**。

**三条边界提醒。**

- **把「功能承诺」和「大陆现实」分开看。** Cloudflare Tunnel 官方承诺的是「出站-only 接入、无需公网 IP/入站端口、CDN/WAF/DDoS 自动生效」[^c6-1]；但这不等于「大陆访问快」，也不等于「免备案」。大陆访问质量是社区经验层面的事[^c6-6]，合规判定看的是**源站物理位置**，套隧道/套 CF 都改变不了这个判定——完整合规速查放第 7 章。**别因为用了 Tunnel 就默认「大陆快 + 免备案」。**
- **frp 组合里，证书职责在 Caddy，不在 frps。** frps 只做明文 HTTP 的按 Host 路由；对外 HTTPS 由 Caddy 终结，或源站自已是 HTTPS，或用 `https2http` 插件[^c6-3][^c6-4]。测试证书签发先走 LE staging，防封禁[^c6-5]。
- **Funnel 的域名、端口、带宽三个硬边界**决定了它只能是轻量/临时方案：不能绑自有域名、只有 443/8443/10000、带宽受限且官方未公开额度[^c6-2]。

最后一条通用提醒：三条隧道本质上都是**把内网服务反向暴露到公网**，暴露面仍然在你映射出去的那个服务上。别因为「用了隧道」就觉得内网是安全的——内网服务该有的认证、补丁、最小暴露一样都别省；只映射你确实要给别人用的端口和服务。

## 本章小结与下一章预告

- 没有公网 IP 的通用思路是**出站隧道**：内网设备主动连一个公网可达的中间方，访客只访问中间方；
- **Cloudflare Tunnel**：`cloudflared` 出站-only 连 CF 边缘，零入站端口，域名须托管在 CF，CDN/WAF/DDoS 自动生效[^c6-1]；
- **frp + Caddy**：frps 用 `vhostHTTPPort` 按 Host 头路由多个子域，Caddy 在前面做 TLS 终止；frp 本身不做 TLS 终止，暴露本地 HTTP 需要 Caddy 前置或 `https2http` 插件[^c6-3][^c6-4]；
- **Tailscale Funnel**：一行命令得到公网 HTTPS URL，但只能绑 `ts.net`、只有 443/8443/10000、带宽受限[^c6-2]；
- 选型看三个变量：**要不要自有域名、要不要自建 VPS、能否接受大陆访问/合规现实**。

下一章把整本笔记收束成一条 0→1 上线路径，并把本章反复出现的「合规」问题一次讲透：源站到底放哪、什么情况必须备案、「域名被墙」和「IP 被封」怎么区分、上线前按什么清单自查。

[^c6-1]: Cloudflare Tunnel 官方文档（C2）：https://developers.cloudflare.com/tunnel/
[^c6-2]: Tailscale Funnel 官方文档（C3）：https://tailscale.com/docs/features/tailscale-funnel
[^c6-3]: frp 官方示例·自定义域名访问内网 Web（C4）：https://gofrp.org/zh-cn/docs/examples/vhost-http/
[^c6-4]: 边缘设备上云：Frp+CF+Caddy 工程博客（C9）：https://blog.soulter.top/posts/edge-server-tunnel.html
[^c6-5]: Caddy Automatic HTTPS 官方文档（C1）：https://caddyserver.com/docs/automatic-https
[^c6-6]: V2EX 社区经验帖（C11）：https://global.v2ex.co/t/1208376 （大陆访问/合规体验，经验参考，非官方承诺）
[^c6-7]: LINUX DO 社区经验帖（C12）：https://linux.do/t/topic/471983/6 （「被墙的是域名还是服务器 IP」，经验参考，非官方承诺）
