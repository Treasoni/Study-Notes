## 第 7 章 搭建节点（带域名与 Cloudflare）

第 6 章你已经能用「VPS 的 IP + 端口」连通节点。这一章往前一步：给节点绑域名，再把域名挂到 Cloudflare 的代理（CDN）后面。多这一层是为了不把真实 IP 直接暴露给扫描者；代价是多引入解析与代理状态两层变量。

> [!note] 来源边界
> 「代理状态如何工作」引 Cloudflare 官方 DNS 文档（C-1 / C-2）；而「把节点跑在代理后的域名上」这种做法本身无官方文档背书，属**行业通用做法**（素材 §6）。

### 域名 + CDN 前置多解决了什么

裸 IP 节点最脆弱处是 IP 直接暴露。套上代理后，对外解析出的是 Cloudflare 的 anycast IP，而非你的源站 IP（来源：C-1 | intro）；若记录保持 DNS-only，查询者会直接拿到你的真实源站 IP，「把源站 IP 暴露给任何查询者，从而去掉一层针对性攻击防护」（来源：C-1 | Example）。

两个状态名字先记住：

- **Proxied（橙云）**：HTTP/HTTPS 流量经 Cloudflare 网络；
- **DNS-only（灰云）**：Cloudflare 直接返回你服务器的真实 IP，流量不经它的网络（来源：C-1 | intro）。

### 记录类型与代理状态：能做与不能做

不是所有记录都能开代理。只有**承载 HTTP/HTTPS 的 A、AAAA、CNAME** 可以代理，其他类型（如 MX、TXT）始终是 DNS-only（来源：C-2 | Proxy eligibility、C-1 | intro）。

| 记录类型 | 能否开橙云 | 说明 |
|---|---|---|
| A / AAAA（承载 HTTP/HTTPS） | 可以 | 节点域名基本属这类 |
| CNAME（承载 HTTP/HTTPS） | 可以 | 默认做 flattening，返回 Cloudflare anycast IP（来源：C-1 \| CNAME records） |
| MX / TXT 等 | 不能 | 永远 DNS-only |

另一个易踩的组合规则：同一 name 上若有多条 A/AAAA 且至少一条被代理，Cloudflare 会把该 name 上**全部**记录按代理处理（来源：C-1 | Mix proxied and unproxied）。

验证命令（`<DOMAIN>` 换成你的域名）：

```bash
dig +short <DOMAIN>          # 橙云返回 Cloudflare 的 IP；灰云返回你的源站 IP
curl -I https://<DOMAIN>     # 看 HTTP 响应是否经 Cloudflare 返回
```

> [!tip] 大白话
> 橙云像「前台代收点」：快递都送前台，谁也不知道你家门牌；灰云则是前台把你家地址写给每个人。而只有「送流量」的 A/AAAA/CNAME 能进前台，MX、TXT 这类「寄明信片」的一律不接。

### pending 窗口期：24 小时内代理其实不生效

新域名加入 Cloudflare 后处于 pending（待验证所有权）状态，**最长 24 小时**。这期间**即使你把记录设成代理，实际也按 DNS-only 生效，所有 DNS 请求都返回源站 IP**（来源：C-2 | Pending domains）。

后果有两个：一是刚配好就测试会误判「代理没生效」；二是这个窗口期里源站 IP 已经泄漏。因此官方建议：**zone 激活后，在主机商处轮换源站 IP**（来源：C-2 | Pending domains）。

> [!tip] 大白话
> pending 就像房子过户还没办完：你手里拿着新钥匙（橙云设置），但物业系统里登记的业主还是旧信息（源站 IP），访客照样按旧地址找到你。

> [!warning] 别把 pending 当配置错误
> 若 24 小时后警告仍在，才是需要排查（来源：C-2 | Pending domains）。在此之前反复删改记录没有意义。

### 端口与协议的前置约束

代理并非所有端口都能用。要代理**非标准端口的 HTTP/HTTPS**，或代理 **TCP/UDP 应用**，官方明确要求改用 **Cloudflare Spectrum**（来源：C-2 | Ports and protocols）。选端口时就要把这条当约束：走标准 443/80 才能吃普通代理。另：以 Cloudflare 作 secondary DNS 且启用 Pre-signed DNSSEC 时，代理记录会被当作 DNS-only（来源：C-2 | Pre-signed DNSSEC）。

### 兜底：域名方案不通就退回裸 IP

如果解析、橙色云、证书、客户端任一层卡住，**直接退回第 6 章的裸 IP + 端口节点**。它不隐藏 IP，但路径最短、变量最少。域名方案是优化项，不是前置项。若后续需要内核级配置（手写 Xray JSON、REALITY 原理），那属于内核直配范畴，超出本篇范围。

### 本章小结

- 橙云藏源站 IP，灰云直接暴露源站 IP（来源：C-1 | intro、Example）
- 只有承载 HTTP/HTTPS 的 A/AAAA/CNAME 能代理；同一 name 多记录只要一条代理，全部按代理处理（来源：C-2 | Proxy eligibility、C-1 | Mix proxied and unproxied）
- pending 最长 24 小时，期间代理记录实际按 DNS-only 生效并泄漏源站 IP；官方建议激活后轮换源站 IP（来源：C-2 | Pending domains）
- 非标端口 HTTP/HTTPS 或 TCP/UDP 代理需 Spectrum（来源：C-2 | Ports and protocols）

### 下一章预告

节点连通、域名配好后，下一步是把节点「搬进客户端」：分享链接、二维码、订阅地址三者怎么选，以及连不通时按什么顺序分层排查。第 8 章给出这套自检流程。
