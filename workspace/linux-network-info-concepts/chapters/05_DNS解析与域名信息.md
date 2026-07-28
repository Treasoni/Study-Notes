# DNS 解析与域名信息

当你输入 `baidu.com` 并按下回车，浏览器需要找到这个域名对应的 IP 地址才能建立连接。这个从"域名"到"IP"的转换过程，就是 **DNS 解析（Domain Name System resolution）**。它是互联网通信的第一步——如果这一步失败，你连不上任何网站，而 `ping` 和 `ip addr` 看到的网络配置可能完全正常。

本章是全书最长的一章，因为 DNS 是实际排障中**最常出问题**的环节，而且 Linux 上的 DNS 体系经历了多次演变，新老配置并存，极其容易踩坑。你将学到：DNS 到底是怎么工作的、Linux 上哪些文件控制 DNS、以及如何用 `dig`/`resolvectl` 等工具精准定位问题。

---

## DNS 解析完整流程：从浏览器到 DNS 服务器

> [!note] 一句话理解 DNS
> DNS 本质上是一个**分布式的键值数据库**——键是域名（如 `www.example.com`），值是 IP 地址（如 `93.184.216.34`）。查询的过程就是沿着这个分布式数据库的链条逐级查找。

下面以在浏览器中输入 `www.example.com` 为例，完整走一遍 DNS 解析的流程。

### 第一步：浏览器缓存检查

浏览器自身维护了一个 DNS 缓存。如果之前查过 `www.example.com` 且缓存未过期，浏览器直接用缓存的 IP，**不发送任何网络请求**。你可以通过 `chrome://net-internals/#dns`（Chrome）或 `about:networking#dns`（Firefox）查看浏览器 DNS 缓存。

### 第二步：操作系统缓存检查

如果浏览器缓存没命中，浏览器会调用操作系统的解析接口。在 Linux 上，操作系统（如 systemd-resolved）也会维护一个 DNS 缓存。用 `resolvectl statistics` 可以看到缓存命中情况。

### 第三步：读取 `/etc/hosts`

如果操作系统缓存也没有，Linux 会检查 `/etc/hosts` 文件。这个文件是**静态的域名→IP 映射表**，优先级通常高于 DNS 查询——这是 `/etc/nsswitch.conf` 中 `hosts: files dns` 的含义（"先查文件，再查 DNS"）。

```bash
# /etc/hosts 示例
127.0.0.1       localhost
127.0.1.1       my-laptop
192.168.1.10    dev-server.internal
# 下面这行可以用来临时屏蔽某个域名（强制指向 127.0.0.1）
127.0.0.1       unwanted-ads.example.com
```

> [!tip] `/etc/hosts` 的实用场景
> - **开发环境**：将 `my-app.local` 指向本机 `127.0.0.1`，方便本地调试
> - **屏蔽域名**：将广告域名指向 `127.0.0.1` / `0.0.0.0`
> - **紧急绕过 DNS 故障**：如果 DNS 服务器挂了，可以在 hosts 里临时写入关键域名

### 第四步：查询 DNS 解析器

如果 `/etc/hosts` 中也没有，Linux 将查询配置的 DNS 解析器。在现代 Ubuntu 系统上，这个解析器通常是 **systemd-resolved** 的 stub resolver（`127.0.0.53`），它充当本地 DNS 代理，负责缓存、转发和 DNSSEC 验证。

### 第五步：递归查询到权威 DNS

解析器从根 DNS 服务器开始，逐级向下查询，最终到达 `www.example.com` 的权威 DNS 服务器。完整的递归过程如下：

```
客户端 → 本地解析器 (127.0.0.53)
       ↓
   递归查询开始
       ↓
   根 DNS 服务器          →  返回 .com 顶级域服务器地址
       ↓
   .com 顶级域服务器      →  返回 example.com 权威服务器地址
       ↓
   example.com 权威服务器  →  返回 www.example.com 的 IP 地址
       ↓
   本地解析器缓存结果，返回给客户端
```

> [!tip] `+trace` 参数可以亲眼看到这个链条
> `dig www.example.com +trace` 会一步步展示从根到权威的完整查询过程，本章后面会详细演示。

### 第六步：浏览器发起 HTTP 连接

拿到 IP 地址后，浏览器终于可以发起 TCP 连接，开始 HTTP 请求。至此，DNS 解析的使命完成。

```
完整链路：
浏览器缓存 → 操作系统缓存 → /etc/hosts → DNS 解析器 → 根 DNS → TLD → 权威 DNS
                                  ↓
                           （到这一步才发网络包）
```

---

## DNS 记录类型详解

DNS 不只是"域名→IP"的简单映射。它是一个丰富的数据库，每条记录称为一个 **资源记录（Resource Record, RR）**，有不同类型。

### 核心记录类型速查

| 记录类型 | 全称 | 作用 | 查询命令 |
|---------|------|------|---------|
| **A** | Address Record | 域名 → IPv4 地址 | `dig example.com A` |
| **AAAA** | IPv6 Address Record | 域名 → IPv6 地址 | `dig example.com AAAA` |
| **CNAME** | Canonical Name | 域名别名（域名 → 另一个域名） | `dig www.example.com CNAME` |
| **MX** | Mail Exchange | 邮件服务器（含优先级） | `dig example.com MX` |
| **NS** | Name Server | 域名的权威 DNS 服务器 | `dig example.com NS` |
| **TXT** | Text Record | 任意文本信息（常用于 SPF/DKIM 验证） | `dig example.com TXT` |
| **SOA** | Start of Authority | 区域的权威信息（刷新间隔、管理员邮箱等） | `dig example.com SOA` |

### A 记录

最基本的记录，将域名映射到一个 IPv4 地址。一个域名可以有多条 A 记录实现**DNS 轮询负载均衡**。

```bash
$ dig baidu.com A +short
39.156.66.10
110.242.68.66

# 两个 IP——百度用了 DNS 轮询，每次解析可能拿到不同 IP
```

### AAAA 记录

与 A 记录功能相同，但返回的是 IPv6 地址。

```bash
$ dig baidu.com AAAA +short
# 如果域名没有 IPv6 地址，这里没有输出
```

### CNAME 记录

将域名指向另一个域名。CNAME 记录本身不返回 IP——客户端需要再查一次目标域名的 A/AAAA 记录。

> [!warning] CNAME 的常见陷阱
> - CNAME 记录不能与其他记录类型共存于同一个域名上
> - 根域名（如 `example.com`）通常不能用 CNAME，因为 NS/SOA 记录会冲突——这就是为什么很多网站把 `www.example.com` 做 CNAME 到 `example.com`，而 `example.com` 本身用 A 记录

```bash
# 很多 CDN 服务用 CNAME 指向加速域名
$ dig www.baidu.com CNAME +short
www.a.shifen.com.

# 客户端需要再查一次 A 记录才能拿到 IP
$ dig www.a.shifen.com A +short
39.156.66.14
110.242.68.3
```

### MX 记录

指定域名的邮件服务器地址。每个 MX 记录带有一个 **优先级（preference）** 字段，数值越小优先级越高。

```bash
$ dig gmail.com MX +short
30 alt3.gmail-smtp-in.l.google.com.
10 alt1.gmail-smtp-in.l.google.com.
40 alt4.gmail-smtp-in.l.google.com.
20 alt2.gmail-smtp-in.l.google.com.
5  gmail-smtp-in.l.google.com.
```

这里 `gmail-smtp-in.l.google.com` 优先级 5（最高），`alt1` 优先级 10（备用），以此类推。发件服务器会先尝试优先级最高的，失败后依次尝试备用。

### NS 记录

指定哪个 DNS 服务器是某个域名的权威服务器。这是 DNS 委派机制的核心。

```bash
$ dig baidu.com NS +short
ns3.baidu.com.
ns7.baidu.com.
dns.baidu.com.
ns4.baidu.com.
ns2.baidu.com.
```

### TXT 记录

存储任意文本信息，被广泛用于域名所有权验证和邮件安全。

```bash
# SPF 记录——声明哪些服务器可以代表该域名发邮件
$ dig gmail.com TXT +short
"v=spf1 redirect=_spf.google.com"
"v=spf1 include:_spf.google.com ~all"
"google-site-verification=..._LpQc"
```

常见用途：
- **SPF**（Sender Policy Framework）：声明合法的发件服务器
- **DKIM**：邮件签名验证公钥
- **DMARC**：邮件验证失败时的处理策略
- **域名所有权验证**：云服务商让你添加 TXT 记录证明你控制该域名

### SOA 记录

区域（zone）的**权威元数据记录**。每个域名有且仅有一个 SOA 记录，包含以下关键字段：

```bash
$ dig baidu.com SOA
...
baidu.com.  7200  IN  SOA  dns.baidu.com.  sa.baidu.com. (
                        2024072201  ; serial（序列号，区域版本标识）
                        300         ; refresh（从服务器刷新间隔，秒）
                        300         ; retry（刷新失败后重试间隔，秒）
                        2592000     ; expire（从服务器数据过期时间，秒）
                        7200        ; minimum（否定缓存 TTL，秒）
)
```

> [!tip] SOA 的 serial 字段是"DNS 排障神器"
> 当你的 DNS 修改没有生效时，用 `dig example.com SOA` 查看 serial 号。如果与你预期的不一致，说明 DNS 服务器上的区域文件没有更新或同步。

### 记录类型查询通用写法

```bash
# 指定记录类型
dig baidu.com A          # A 记录
dig baidu.com AAAA       # AAAA 记录
dig baidu.com MX         # MX 记录
dig baidu.com NS         # NS 记录
dig baidu.com TXT        # TXT 记录
dig baidu.com SOA        # SOA 记录
dig baidu.com CNAME      # CNAME 记录
dig baidu.com ANY        # 所有记录类型（注意：很多 DNS 服务器不支持 ANY 查询）

# +short 简化输出
dig baidu.com MX +short

# +noall +answer 只显示回答部分（比 +short 略详细）
dig baidu.com MX +noall +answer
```

---

## Linux DNS 配置文件体系

Linux 上的 DNS 解析不是"一个文件搞定"的简单事情。**三个文件**构成一条完整的解析链路，理解它们的协作关系是排查 DNS 问题的关键。

### 配置文件链路

```
/etc/nsswitch.conf
    ↓ 控制"以什么顺序查"
/etc/hosts
    ↓ 静态映射（优先级高）
/etc/resolv.conf
    ↓ 指定 DNS 服务器（优先级低）
DNS 服务器（如 8.8.8.8 或 127.0.0.53）
```

### 第一环：`/etc/nsswitch.conf`

**NSS（Name Service Switch）** 是 Linux 系统解析名称（用户、组、主机名等）的统一框架。对于主机名解析，它决定了"先查什么、再查什么"的顺序。

```bash
$ grep hosts /etc/nsswitch.conf
hosts:          files dns
```

常见配置及其含义：

| 配置 | 含义 |
|------|------|
| `hosts: files dns` | 先查 `/etc/hosts`，没找到再查 DNS |
| `hosts: dns files` | 先查 DNS，没找到再查 `/etc/hosts`（极少见） |
| `hosts: files mdns4_minimal [NOTFOUND=return] dns` | Ubuntu 默认配置，先查 hosts，再查 mDNS，最后查 DNS |

> [!note] mDNS 是什么？
> `mdns4_minimal` 是 **Multicast DNS**（零配置网络协议，Avahi 实现）。它允许同一局域网内的设备通过 `.local` 域名互相发现——比如 `my-printer.local` 不需要 DNS 服务器就能解析。`[NOTFOUND=return]` 的意思是：如果 mDNS 明确返回"查不到"（而不是超时），就不再继续查 DNS 了。

测试 NSS 解析链路的命令：

```bash
# 使用 NSS 接口查询，不走 dig/nslookup，完整模拟应用层解析行为
$ getent hosts baidu.com
39.156.66.10     baidu.com
110.242.68.66    baidu.com

# 如果修改了 /etc/hosts，getent 能立刻反映顺序变化
# 而 dig 始终直接查 DNS，不受 nsswitch.conf 影响
```

> [!warning] `getent hosts` vs `dig` 的区别
> - `getent hosts`：走 NSS 链路（`nsswitch.conf` → `/etc/hosts` → DNS），**完全模拟应用行为**
> - `dig`：直接向 DNS 服务器发送请求，**跳过 NSS 和 `/etc/hosts`**
> - 排障时两者都要用：`dig` 测 DNS 服务器本身是否正常，`getent hosts` 测系统解析链路是否正常

### 第二环：`/etc/hosts`

静态主机名映射文件。格式非常简单：

```
IP地址    主机名 [别名...]
```

```bash
$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       pop-os
192.168.1.10    nas.home
::1             localhost ip6-localhost ip6-loopback
```

> [!tip] `/etc/hosts` 的调试技巧
> 如果想临时"屏蔽"某个域名指向其真实 IP，可以在 hosts 中加入：
> ```
> 127.0.0.1  tracking.example.com
> ```
> 这样所有指向 `tracking.example.com` 的请求都会发到本机（被拒绝）。改完后立即生效，不需要重启任何服务。

### 第三环：`/etc/resolv.conf`

传统上这个文件直接指定 DNS 服务器地址。但在现代 Linux 上，**它往往是一个符号链接**，由 systemd-resolved 或 NetworkManager 自动管理。

```bash
$ ls -l /etc/resolv.conf
lrwxrwxrwx 1 root root 39 ... /etc/resolv.conf -> ../run/systemd/resolve/stub-resolv.conf

$ cat /etc/resolv.conf
# 这是 systemd-resolved 管理的文件
nameserver 127.0.0.53
options edns0 trust-ad
search .
```

关键字段：

| 字段 | 含义 | 示例 |
|------|------|------|
| `nameserver` | DNS 服务器地址（最多 3 个） | `nameserver 8.8.8.8` |
| `search` | 搜索域，输入短域名时自动追加 | `search example.com` 让 `ping dev` 自动查询 `dev.example.com` |
| `options` | 解析选项 | `ndots:5` 控制"多少个点才算完整域名"、`timeout:2` 超时秒数 |

> [!warning] 最常见的 DNS 踩坑点：手动编辑 `/etc/resolv.conf`
> 在 Ubuntu 16.04+ 上，`/etc/resolv.conf` 是一个符号链接指向 systemd-resolved 管理的文件。**手动编辑这个文件会被 systemd-resolved 定期覆盖**。
>
> 正确做法：使用 `resolvectl` 或配置 `/etc/systemd/resolved.conf`。

---

## systemd-resolved 与 resolvectl

systemd-resolved 是 systemd 家族的 DNS 解析服务。它在现代 Linux 发行版（Ubuntu 16.04+、Debian 11+、Fedora、Arch Linux）上广泛使用，但它的行为与传统的 DNS 配置方式有很大不同，是 **Linux DNS 排障中最大的"坑"来源**。

### Stub Resolver 架构

```
应用进程（浏览器、curl 等）
    ↓ 查询 127.0.0.53:53
systemd-resolved（stub resolver，监听 127.0.0.53:53）
    ↓
    ├── 缓存命中 → 直接返回
    ├── /etc/hosts → 查静态映射
    └── 转发到上游 DNS → 8.8.8.8 / 114.114.114.114 / ...
```

systemd-resolved 在 `127.0.0.53` 上启动一个本地 DNS 代理，负责：

1. **缓存 DNS 查询结果**（减少重复查询）
2. **管理 `/etc/hosts`**（stub 模式，但也可配置为只读）
3. **DNSSEC 验证**（可选）
4. **每接口 DNS 配置**（不同网络接口可使用不同 DNS 服务器）
5. **mDNS 支持**（通过 `.local` 域名）

### 模式选择

systemd-resolved 有三种运行模式，决定了 `/etc/resolv.conf` 的内容：

| 模式 | resolv.conf 指向 | 特点 |
|------|------------------|------|
| **stub**（默认） | `/run/systemd/resolve/stub-resolv.conf` | `nameserver 127.0.0.53`，所有查询经过 systemd-resolved |
| **direct** | `/run/systemd/resolve/resolv.conf` | 直接填写上游 DNS 服务器地址，绕开 systemd-resolved |
| **static** | 手动管理 `/etc/resolv.conf` | systemd-resolved 不管理 resolv.conf |

### resolvectl 命令详解

`resolvectl` 是 systemd-resolved 的管理命令行工具。

#### 查看当前 DNS 配置

```bash
$ resolvectl status
Global
       Protocols: -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: stub

Link 2 (enp0s3)
    Current Scopes: DNS
         Protocols: +DefaultRoute -LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 192.168.1.1    ← 当前网卡的 DNS 服务器
       DNS Servers: 192.168.1.1    ← 配置的所有 DNS 服务器（DHCP 获取）
        DNS Domain: home            ← DNS 搜索域
```

关键信息解读：

- **Global** 部分：全局设置，协议启用状态、DNSSEC 配置
- **Link N** 部分：每个网络接口独立的 DNS 配置
- **Current DNS Server**：当前正在使用的 DNS 服务器（可能是多个中最快的一个）
- **resolv.conf mode**：当前 `/etc/resolv.conf` 的生成模式

#### DNS 查询（替代 dig 的系统级查询）

```bash
# 通过 systemd-resolved 查询域名
$ resolvectl query baidu.com
baidu.com: 39.156.66.10               -- link: enp0s3
           110.242.68.66              -- link: enp0s3

# 反向查询
$ resolvectl query 8.8.8.8
8.8.8.8: dns.google                   -- link: enp0s3

# 查看特定接口的 DNS 配置
$ resolvectl dns enp0s3
Link 2 (enp0s3): 192.168.1.1

# 查看特定接口的 DNS 搜索域
$ resolvectl domain enp0s3
Link 2 (enp0s3): home
```

> [!note] `resolvectl query` vs `dig`
> - `resolvectl query` 走 systemd-resolved 的完整链路（含缓存和 `/etc/hosts`）
> - `dig` 直接向指定 DNS 服务器发查询，绕过 systemd-resolved
> - 排障时两者的差异本身就是信息：如果 `dig` 正常但 `resolvectl query` 失败，问题在 systemd-resolved 而不是网络

#### DNS 缓存管理

```bash
# 查看缓存统计
$ resolvectl statistics
Cache statistics:
    Current Cache Size: 78          ← 当前缓存条目数
          Cache Hits: 1243          ← 命中次数（越大说明缓存效果越好）
        Cache Misses: 567           ← 未命中次数
DNSSEC verdicts:
              Secure: 0
            Insecure: 0
               Bogus: 0
       Indeterminate: 0

# 刷新 DNS 缓存（排障中最常用的操作之一）
$ resolvectl flush-caches

# 验证缓存已清空
$ resolvectl statistics | grep "Current Cache Size"
Current Cache Size: 0
```

> [!tip] `flush-caches` 的使用时机
> 当你修改了 DNS 记录（如更换了网站 IP），但本机仍然解析到旧 IP 时，先执行 `resolvectl flush-caches` 清除 systemd-resolved 缓存。如果清除后还是旧 IP，说明问题在上级 DNS 的 TTL 缓存。

#### 管理每接口 DNS 配置

这是 systemd-resolved 最强大的特性之一——**每个网络接口可以有独立的 DNS 配置**。

```bash
# 查看每个接口的 DNS 配置
$ resolvectl status

# 手动设置某个接口的 DNS（临时，重启后失效）
$ sudo resolvectl dns enp0s3 8.8.8.8 8.8.4.4

# 设置搜索域
$ sudo resolvectl domain enp0s3 example.com

# 永久配置：写 /etc/systemd/resolved.conf
$ cat /etc/systemd/resolved.conf
[Resolve]
DNS=8.8.8.8 8.8.4.4
Domains=example.com
# FallbackDNS=1.1.1.1   ← 当所有接口指定的 DNS 都不可用时的备用
# DNSSEC=allow-downgrade

$ sudo systemctl restart systemd-resolved
```

---

## dig 命令详解

`dig`（Domain Information Groper）是 DNS 查询的**首选工具**。它灵活、信息丰富、可脚本化。与 `nslookup` 相比，`dig` 更详细、更可控。

### 基本查询

```bash
$ dig baidu.com

; <<>> DiG 9.18.28-0ubuntu0.22.04.1-Ubuntu <<>> baidu.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 46253
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232

;; QUESTION SECTION:
;baidu.com.                     IN      A

;; ANSWER SECTION:
baidu.com.              5       IN      A       39.156.66.10
baidu.com.              5       IN      A       110.242.68.66

;; Query time: 4 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed Jul 29 00:00:00 CST 2026
;; MSG SIZE  rcvd: 70
```

输出解读：

| 字段 | 含义 |
|------|------|
| `status: NOERROR` | 查询成功（`NXDOMAIN` 表示域名不存在） |
| `flags: qr rd ra` | `qr`=查询响应, `rd`=期望递归, `ra`=支持递归 |
| `QUESTION SECTION` | 查的是什么（`baidu.com. IN A` = 查 baidu.com 的 A 记录） |
| `ANSWER SECTION` | 返回的结果 |
| `5 IN A 39.156.66.10` | TTL=5 秒, 记录类=IN(Internet), 类型=A, 值=39.156.66.10 |
| `SERVER: 127.0.0.53#53` | 哪个 DNS 服务器返回的（这里显示 systemd-resolved 的 stub） |
| `Query time: 4 msec` | 查询耗时 |

### +short：简化输出

当只需要 IP 地址列表时，`+short` 去除所有元信息：

```bash
$ dig baidu.com +short
39.156.66.10
110.242.68.66
```

对脚本特别友好：

```bash
# 把解析结果赋值给变量
IP=$(dig baidu.com +short | head -1)
echo $IP
# 输出：39.156.66.10
```

### +noall +answer：精确控制输出

`dig` 的"开关"模式非常灵活，可以精确控制显示哪些段落：

```bash
# 只显示 ANSWER SECTION
dig baidu.com +noall +answer
baidu.com.              5       IN      A       39.156.66.10
baidu.com.              5       IN      A       110.242.68.66

# 只显示统计信息
dig baidu.com +noall +stats
```

常用开关组合：

| 组合 | 用途 |
|------|------|
| `+noall +answer` | 最常用，只显示答案 |
| `+noall +short` | 纯 IP 列表，适合脚本 |
| `+noall +stats` | 只显示查询统计 |
| `+noall +authority +additional` | DNS 排障时查看权威和附加信息 |

### @server：指定 DNS 服务器

默认情况下 `dig` 使用系统配置的 DNS 服务器（`/etc/resolv.conf` 中指定的）。通过 `@` 可以指定任意 DNS 服务器：

```bash
# 使用 Google 公共 DNS
$ dig @8.8.8.8 baidu.com +short
39.156.66.10
110.242.68.66

# 使用 Cloudflare DNS
$ dig @1.1.1.1 baidu.com +short
39.156.66.10
110.242.68.66

# 使用国内 DNS
$ dig @114.114.114.114 baidu.com +short
39.156.66.10
110.242.68.66
```

> [!tip] 为什么要指定 DNS 服务器？
> 比较不同 DNS 服务器的返回结果，可以判断你的 DNS 解析器是否返回了正确或最新的结果。比如修改了域名 DNS 记录后，用 `dig @8.8.8.8` 与 `dig @你的DNS` 对比，可以判断是 DNS 服务器缓存问题还是网络问题。

### +trace：追踪完整委派链

这是 `dig` 最强大的排障功能。它模拟 DNS 解析器的递归查询过程，从根服务器开始一步步追踪：

```bash
$ dig baidu.com +trace
```
输出非常长，但结构清晰：

```
.                       518336  IN      NS      a.root-servers.net.      ← 从根开始
.                       518336  IN      NS      b.root-servers.net.
.                       518336  IN      NS      ...（13 台根服务器）
;; Received 281 bytes from 199.7.83.42#53(l.root-servers.net) in 4 ms

com.                    172800  IN      NS      a.gtld-servers.net.     ← .com 顶级域
com.                    172800  IN      NS      b.gtld-servers.net.
com.                    172800  IN      NS      ...（13 台 TLD 服务器）
;; Received 1093 bytes from 192.5.6.30#53(a.gtld-servers.net) in 26 ms

baidu.com.              172800  IN      NS      ns2.baidu.com.          ← baidu.com 的权威服务器
baidu.com.              172800  IN      NS      ns3.baidu.com.
baidu.com.              172800  IN      NS      ns4.baidu.com.
baidu.com.              172800  IN      NS      ns7.baidu.com.
baidu.com.              172800  IN      NS      dns.baidu.com.
;; Received 364 bytes from 192.42.93.30#53(g.gtld-servers.net) in 148 ms

baidu.com.              5       IN      A       39.156.66.10            ← 最终的答案
baidu.com.              5       IN      A       110.242.68.66
;; Received 70 bytes from 110.242.68.3#53(ns4.baidu.com) in 12 ms
```

> [!warning] `+trace` 的排障价值
> 如果某个域名解析失败，`+trace` 可以精准定位问题出在链条的哪个环节：
> - 根服务器查不到 → 可能是防火墙阻断了 DNS 查询（检查 53 端口 UDP 出站）
> - TLD 服务器查不到 → 可能域名不存在
> - 权威服务器没响应 → 可能是域名 NS 记录配置错误或权威服务器宕机
> - 权威服务器返回了错误的 IP → DNS 劫持

### -x：反向查询（IP 到域名）

```bash
$ dig -x 8.8.8.8 +short
dns.google.

$ dig -x 114.114.114.114 +short
public1.114dns.com.
```

反向查询通过 **PTR 记录**实现。ISP 和云服务商通常会为公网 IP 配置 PTR 记录，但家庭宽带和很多 VPS 默认不配置。

### 指定记录类型

本章前面已演示过，这里汇总成表格：

```bash
dig baidu.com A                  # A 记录
dig baidu.com AAAA               # AAAA 记录
dig baidu.com MX                 # MX 记录
dig baidu.com NS                 # NS 记录
dig baidu.com TXT                # TXT 记录
dig baidu.com SOA                # SOA 记录
dig baidu.com CNAME              # CNAME 记录
```

### 批量查询与脚本应用

```bash
# 批量查询多个域名
for domain in baidu.com google.com github.com; do
    echo "$domain: $(dig +short $domain | head -1)"
done
# 输出：
# baidu.com: 39.156.66.10
# google.com: 142.250.80.46
# github.com: 140.82.121.3

# 监控域名 IP 变化
watch -n 60 'dig +short baidu.com | sort'
```

### dig 常用选项速查

| 选项 | 作用 | 示例 |
|------|------|------|
| `+short` | 简化输出，只显示值 | `dig baidu.com +short` |
| `+trace` | 追踪递归查询链路 | `dig baidu.com +trace` |
| `+noall +answer` | 只显示答案段 | `dig baidu.com +noall +answer` |
| `+noall +short` | 纯值输出，适合脚本 | `dig baidu.com +short` |
| `@server` | 指定 DNS 服务器 | `dig @8.8.8.8 baidu.com` |
| `-x IP` | 反向查询 | `dig -x 8.8.8.8` |
| `+time=5` | 设置超时秒数 | `dig @8.8.8.8 baidu.com +time=5` |
| `+tries=2` | 设置重试次数 | `dig @8.8.8.8 baidu.com +tries=2` |

---

## nslookup 与 host 快速查询

虽然 `dig` 是首选，但 `nslookup` 和 `host` 也有各自的适用场景。

### nslookup

`nslookup` 曾经是 DNS 查询的标配工具，交互式和单命令模式都支持。

**单命令模式**：

```bash
# 基本查询
$ nslookup baidu.com
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   baidu.com
Address: 39.156.66.10
Name:   baidu.com
Address: 110.242.68.66

# 指定记录类型
$ nslookup -type=MX gmail.com
gmail.com       mail exchanger = 30 alt3.gmail-smtp-in.l.google.com.
gmail.com       mail exchanger = 10 alt1.gmail-smtp-in.l.google.com.
...

# 指定 DNS 服务器
$ nslookup baidu.com 8.8.8.8
```

**交互模式**（输入 `nslookup` 直接回车进入）：

```
$ nslookup
> server 8.8.8.8          # 设置 DNS 服务器
Default server: 8.8.8.8
> set type=MX             # 设置查询类型
> gmail.com               # 查询
...
> exit
```

> [!note] `nslookup` vs `dig`
> `nslookup` 的优势是输出更简洁、对人更友好；劣势是信息量少、不支持 `+trace`。日常快速查一下用 `nslookup` 没问题，**深度排障时请用 `dig`**。

### host

`host` 是三者中最简洁的，输出极致精简，适合快速查看：

```bash
$ host baidu.com
baidu.com has address 39.156.66.10
baidu.com has address 110.242.68.66
baidu.com mail is handled by 10 mx.maillb.baidu.com.
baidu.com mail is handled by 20 mx1.baidu.com.
baidu.com mail is handled by 15 mx.n.shifen.com.
baidu.com mail is handled by 20 jpmx.baidu.com.

# 指定记录类型
$ host -t MX gmail.com
gmail.com mail is handled by 30 alt3.gmail-smtp-in.l.google.com.
gmail.com mail is handled by 10 alt1.gmail-smtp-in.l.google.com.
...

# 指定 DNS 服务器
$ host baidu.com 8.8.8.8
```

适用于脚本中快速获取解析结果：

```bash
host baidu.com 2>/dev/null | grep "has address" | awk '{print $NF}'
```

### 三工具对比

| 工具 | 输出详细度 | 交互模式 | `+trace` | 脚本友好 | 推荐使用场景 |
|------|-----------|---------|----------|---------|------------|
| `dig` | 最详细 | 不支持 | 支持 | 很好 | 深度排障、分析、脚本 |
| `nslookup` | 中等 | 支持 | 不支持 | 一般 | 日常快速查询 |
| `host` | 最精简 | 不支持 | 不支持 | 最好 | 脚本、简单验证 |

---

## 常见 DNS 排查场景

前面学完了理论知识和工具，现在来看几个实际排查场景，把知识串起来。

### 场景一："网站打不开，是不是 DNS 的问题？"

```bash
# 第一步：确认域名能不能解析（绕开 systemd-resolved）
dig www.baidu.com +short
# 如果返回 IP → DNS 没问题，问题不在 DNS 解析
# 如果没有返回 → DNS 出问题了，继续排查

# 第二步：确认哪个 DNS 服务器出问题（指定不同 DNS 对比）
dig @8.8.8.8 www.baidu.com +short
dig @114.114.114.114 www.baidu.com +short
# 如果公共 DNS 能解析但系统配置的 DNS 不能 → 你用的 DNS 服务器有问题
# 如果都不能 → 可能是网络不通或域名真的不存在

# 第三步：检查系统解析链路
getent hosts www.baidu.com
# 如果 getent 失败但 dig 成功 → 问题在 NSS 配置或 systemd-resolved
# 如果 getent 成功但 dig 也成功 → 一切正常，问题不在 DNS
```

### 场景二："改了 DNS 记录，但本机还是旧 IP"

```bash
# 第一步：检查 systemd-resolved 缓存
resolvectl statistics
# 看 Cache Hits 和 Cache Misses 的比例

# 第二步：清空缓存
resolvectl flush-caches

# 第三步：确认清空后是否能拿到新 IP
dig www.example.com +short

# 如果还是旧 IP → 上游 DNS 服务器缓存未过期，只能等 TTL
# TTL 由域名所有者设置，在 dig 结果中可以看到：
dig www.example.com +noall +answer
# www.example.com.  300  IN  A  1.2.3.4
#                  ^^^ TTL=300 秒 = 5 分钟
```

### 场景三："域名解析到了错误的 IP（可能被劫持）"

```bash
# 用不同 DNS 服务器对比
echo "Google DNS:"
dig @8.8.8.8 example.com +short

echo "Cloudflare DNS:"
dig @1.1.1.1 example.com +short

echo "系统 DNS:"
dig example.com +short

# 如果系统 DNS 返回的 IP 与其他不一致 → 可能是 DNS 劫持
# 用 +trace 确认权威服务器返回的正确结果
dig @8.8.8.8 example.com +trace | grep "example.com."
```

### 场景四："内网域名（私有域名）解析不了"

```bash
# 检查 /etc/hosts 是否有配置
grep internal-server /etc/hosts

# 检查 systemd-resolved 的搜索域
resolvectl status | grep "DNS Domain"

# 检查 NSS 配置
grep hosts /etc/nsswitch.conf

# 检查是否启用了 mDNS（.local 域名必须用 mDNS）
resolvectl status | grep "mDNS"

# 尝试直接通过权威服务器查询（如果能访问的话）
dig @内网DNS服务器IP internal-server.internal A +short
```

### 场景五："ping 域名能通，但浏览器不行为什么？"

这可能是因为：

1. **浏览器有自己的 DNS 缓存** → 清空浏览器 DNS 缓存（`chrome://net-internals/#dns`）
2. **浏览器使用 HTTPS DNS（DoH）** → 某些浏览器默认启用 DNS over HTTPS，绕过系统 DNS
3. **CNAME 记录解析问题** → 浏览器需要额外解析 CNAME 指向的目标域名

```bash
# 确认域名是否有 CNAME 记录
dig example.com CNAME +noall +answer

# 如果有，手动解析目标域名
dig 目标域名.com A +short

# 检查是否支持 IPv6 但 IPv6 网络有问题
dig example.com AAAA +short
# 如果有 AAAA 记录返回，尝试禁用 IPv6 测试
```

---

## 本章小结

- **DNS 解析流程**从浏览器缓存开始，经过操作系统缓存、`/etc/hosts`、本地解析器，最终通过递归查询到达权威 DNS 服务器
- **DNS 记录类型**中 A/AAAA 是最基本的域名到 IP 映射，CNAME 用于别名，MX 用于邮件路由，NS 用于域名委派，TXT 用于验证和邮件安全，SOA 是区域的权威元数据
- **Linux DNS 配置文件链路**为 `nsswitch.conf` → `/etc/hosts` → `/etc/resolv.conf`。使用 `getent hosts` 测试完整链路，`dig` 测试 DNS 服务器本身
- **systemd-resolved** 在 `127.0.0.53` 启动 stub 解析器，管理缓存、每接口 DNS 和 DNSSEC。`resolvectl` 是管理工具，`flush-caches` 是最常用的排障操作
- **`dig`** 是 DNS 排障的首选工具——`+short` 简化输出、`+trace` 追踪委派链、`@server` 指定 DNS 服务器、`-x` 反向查询。`nslookup` 适合快速查询，`host` 适合脚本
- **DNS 缓存**由 systemd-resolved 管理，用 `resolvectl statistics` 查看命中情况，`resolvectl flush-caches` 清空缓存
- **排障三步走**：`dig` 测 DNS 服务器本身 → `getent hosts` 测系统链路 → 对比不同 DNS 服务器判断是否被劫持

### 下章预告

下一章我们回到链路层，深入 **ARP 协议与邻居发现**。你会学到 IP 地址是如何通过 ARP 协议转换为 MAC 地址的，以及 Linux 上邻居表的状态机（REACHABLE/STALE/FAILED）和 `ip neigh` 命令的完整用法——这是理解"同一局域网内两台机器如何通信"的关键。

---

*章节编号：05 | 计划篇幅：长 | 实际篇幅：实战笔记（概念 + 命令操作）*
