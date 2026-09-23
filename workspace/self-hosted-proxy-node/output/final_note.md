# 自建代理节点：概念入门到上手实战

## 目录

- 第一章：分层模型——代理协议之外的传输三件事
- 第二章：REALITY 原理——不是新协议，是 TLS 的变体
- 第三章：落地前的 VPS 硬化基线
- 第四章：监控、文件完整性与被入侵后的处置
- 第五章：服务端配置——VLESS + XTLS Vision + REALITY
- 第六章：客户端配置——结构对称与字段配对
- 第七章：连通校验与字段对齐排错

---

## 第一章：分层模型——代理协议之外的传输三件事

要让 VPS 上的节点被人连上，第一步不是选 VLESS 还是 Trojan，而是决定「用户怎么连进来」。VLESS、Trojan 管的是代理协议本身；真正决定数据包长什么样、走哪条路的，是每个入站/出站里那个叫 `streamSettings` 的对象。它有个常被忽略的性质：一部分设置必须两端共同遵守——服务端选了 WebSocket，客户端也得选 WebSocket。本章把 `streamSettings` 拆成三层，讲清各层管什么、哪些组合合法，为第 5、6 章照抄服务端与客户端配置打地基。

## 1.1 为什么两端必须对齐

`streamSettings` 配置的是「代理协议之外的数据传输部分，如承载方式、安全机制及附加行为」[^c1-1]。官方把它分成三类，分属不同层次，在一定范围内可以相互组合。

重点在于，其中一部分配置会直接影响与远端建立通信的方式。对这类需要协商的配置，官方明确要求两端兼容，原话是：

> 一端使用 WebSocket，另一端也必须使用 WebSocket，否则无法建立通信。

后面必须逐字段配对，原因就在这里：服务端与客户端的 `streamSettings` 不是各写各的，而是同一份约定的两种视角。此外 `streamSettings` 是 `InboundObject`/`OutboundObject` 的子项，每个入站、出站都能各配一套，所以一台服务端能给不同入站挂不同组合。

> [!tip] 大白话
> 把两端协商想成打电话前对暗号：你开口说「讲中文」，对面也必须讲中文；一边改说粤语，这通电话就接不上。

## 1.2 承载方式 method

`method` 决定数据流的承载形式，取值域是 `raw | xhttp | mkcp | grpc | websocket | httpupgrade | hysteria`，默认 `raw`[^c1-1]。

每种方式都有专属的 Settings 字段——`rawSettings`、`xhttpSettings`、`kcpSettings`、`grpcSettings`、`wsSettings`、`httpupgradeSettings`、`hysteriaSettings`。注意 `kcpSettings` 对应的是 `mkcp`。这些字段只在对应 `method` 下生效，方法不匹配时写了也被忽略。

下面把完整的 `streamSettings` 骨架摆出来，三层字段都在，默认值标在行内注释里：

```jsonc
{
  // outbound 示例，同样可用于 inbound
  "outbounds": [
    {
      // ...
      "streamSettings": {
        // 传输方式层：默认 raw
        "method": "raw",           // raw|xhttp|mkcp|grpc|websocket|httpupgrade|hysteria
        "rawSettings": {},         // 仅 method=raw 时有效
        "xhttpSettings": {},       // 仅 method=xhttp 时有效
        "kcpSettings": {},         // 仅 method=mkcp 时有效
        "grpcSettings": {},        // 仅 method=grpc 时有效
        "wsSettings": {},          // 仅 method=websocket 时有效
        "httpupgradeSettings": {}, // 仅 method=httpupgrade 时有效
        "hysteriaSettings": {},    // 仅 method=hysteria 时有效
        // 传输安全层：默认 none
        "security": "none",        // none|reality|tls
        "realitySettings": {},     // 仅 security=reality 时有效
        "tlsSettings": {},         // 仅 security=tls 时有效
        // 附加配置层
        "finalmask": {},
        "sockopt": {}
      }
    }
  ]
}
```

## 1.3 安全层 security

`security` 指定传输过程中使用的安全机制，取值 `none | reality | tls`，默认 `none`[^c1-1]：`none` 表示不启用（默认值），`reality` 表示使用 REALITY，`tls` 表示使用 TLS。

TLS 由 Golang 提供，通常协商结果为 TLS 1.3，不支持 DTLS[^c1-1]。它的兼容性最好：官方说明 `tlsSettings` 支持与 RAW、XHTTP、mKCP、gRPC、WebSocket、HTTPUpgrade、Hysteria 全部七种承载方式组合。

REALITY 不是新协议，而是「对 TLS 的一种修改，通过借用目标站点的 TLS 外观与握手特征来完成伪装」[^c1-1]。它的组合面窄得多，只支持与 RAW、XHTTP、gRPC 三种承载方式组合——这是第 2 章的主题。

> [!tip] 大白话
> `method` 是「走哪条路」，`security` 是「路上要不要罩一层看不出内容的信封」。TLS/REALITY 就是信封，只不过 REALITY 的信封是照着某个正经网站的信封仿制的。

## 1.4 组合硬约束

方法层和安全层不能随便搭。据 S-1 官方速查表归纳，`streamSettings.method + streamSettings.security` 的合法组合如下[^c1-1]：

| `method` ↓ / `security` → | `none` | `tls` | `reality` |
| --- | --- | --- | --- |
| `raw` | 支持 | 支持 | 支持 |
| `xhttp` | 支持 | 支持 | 支持 |
| `grpc` | 支持 | 支持 | 支持 |
| `websocket` | 支持 | 支持 | 不支持 |
| `httpupgrade` | 支持 | 支持 | 不支持 |
| `mkcp` | 支持 | 支持 | 不支持 |
| `hysteria` | 不支持 | 必须 | 不支持 |

读表要点：`hysteria` 承载下 `security` 必须是 `tls`，`none`、`reality` 都不支持；`raw` / `xhttp` / `grpc` 在 `none` / `tls` / `reality` 下都支持，是服务端最稳的组合；其余承载（`websocket` / `httpupgrade` / `mkcp`）能与 `none`、`tls` 搭配，但都不能配 `reality`。

还有一条针对协议 + 安全的约束必须记住：当 `streamSettings.security` 为 `none` 时，VLESS（未启用 Encryption）和 Trojan 仅允许连接私网地址[^c1-1]。VLESS 的 Encryption 是可选的、默认关闭（`encryption: "none"`）；启用后即便 `security` 为 `none` 也能连公网，但它给不了 TLS/REALITY 那种正常 HTTPS 的外观。换言之，公网节点上几乎没有理由用 `none`。

> [!tip] 大白话
> 想成点餐的组合限制：Hysteria 这道菜只配 TLS 这一种蘸料；`reality` 蘸料只给 raw/xhttp/grpc 三样主食；而「不加密」（none）这档只卖堂食（私网），不做外带（公网）。

## 1.5 附加配置与直接出站

第三层是附加配置，只有两个字段：`finalmask`（对流量的最终伪装）与 `sockopt`（底层网络行为）[^c1-1]。

与承载方式、安全层不同，这一层不参与两端协商——**推断**：官方速查表只覆盖前两层，并未给出 `finalmask` / `sockopt` 的组合规则，因此「不参与协商、属本地行为控制」是据文档结构归纳（confidence: medium），不是官方原话。

一个具体例子能看出这层的定位：Freedom 这类直接出站，对端是任意普通公网目标（如某个网站），此时传输配置「不需要（也基本不能）与另一端协商」，而是用于控制本地发出连接时的行为，「此时只有 `sockopt` 可用」[^c1-1]。所以如果在服务端 `outbounds` 的 freedom 出站里看到 `realitySettings`、`finalmask` 之类的东西，就是放错了层。

> [!tip] 大白话
> 前两层像两个人通话前商量的规则（必须双方一致）；附加配置像你握话筒的姿势、坐的凳子——只影响你自己这一端，不用对方同意，也不能靠它俩接通电话。

## 小结

- `streamSettings` 只管代理协议之外的传输，分承载方式、安全机制、附加行为三层。
- 需要协商的部分必须两端兼容；这是服务端/客户端配置必须逐字段配对的根据。
- `method` 默认 `raw`，七种取值各有专属 Settings，只在对应 `method` 下生效。
- `security` 默认 `none`；TLS 兼容全部七种承载，REALITY 只配 RAW/XHTTP/gRPC，hysteria 必须 tls。
- `security=none` 时 VLESS/Trojan 仅限私网；`finalmask` / `sockopt` 不参与协商，freedom 直接出站只有 `sockopt`。

下一章进入 REALITY 内部：它凭什么能借用某个网站的 TLS 外观，鉴权失败时又为什么能把连接原样转给 `target`。

[^c1-1]: 传输配置 - Xray-core 官方文档，https://xtls.github.io/config/transport.html

---

## 第二章：REALITY 原理——不是新协议，是 TLS 的变体

第一章把 `streamSettings` 分成承载、安全、附加三层，`security` 取值为 `none / tls / reality`。本章说明 `reality` 是什么、为什么能替代 `tls`，以及它的回落语义为何是伪装成立的关键。

## 2.1 设计意图与官方收益

`tls` 的痛点是服务器必须出示自己的证书：自签证书无可信 CA 背书，主动探测一眼就认出「这是代理入口」。REALITY 不自己当网站，而是借一个真网站的外观：

> REALITY 是对 TLS 的一种修改，通过借用目标站点的 TLS 外观与握手特征来完成伪装。[^c2-1]

关键是**修改**，不是新协议：服务端是 Go 1.19.5 标准库 `tls` 包的 fork，客户端参考实现在 Xray-core 的 `transport/internet/reality/reality.go`。[^c2-2] 官方对开发者说：

> REALITY 只是修改了 TLS，客户端的实现只需要轻度修改完全随机的 session id 和自定义证书验证即可。[^c2-1]

替代 TLS 后的官方收益：

> By replacing TLS with REALITY, **you can eliminate server-side TLS fingerprint characteristics**, maintain forward secrecy, **and render certificate chain attacks ineffective**.[^c2-2]

即消除服务端 TLS 指纹、保持前向保密、使证书链攻击失效；并可「指向另一个网站」而无需买域名或配 TLS 服务器，全程呈现指定 SNI。[^c2-2]

> [!tip] 大白话
> 把 REALITY 想成「借壳」：不自己挂招牌，而是借邻居的门面谈生意，外人看到的全是邻居的样子。所以……你不必真拥有那个网站，只需挑个好邻居。

## 2.2 目标站要求

**最低要求**（据官方文档归纳，要的是「真站、稳站、和你像在同一个地方」）：[^c2-2]

- 境外网站；
- 支持 TLSv1.3 与 H2；
- 域名不发生重定向（主域重定向到 www 不影响）。

**加分项**：IP 邻近（延迟更低、特征更相似）；Server Hello 后握手报文已加密（如 `dl.google.com`）；支持 OCSP Stapling。[^c2-2]

## 2.3 鉴权与回落语义

最反直觉也最关键：连上 443 却未通过鉴权（非合法 REALITY 请求）的流量，Xray **不拒绝**，而是**直接转发**到目标站：

> 为了伪装的效果考虑，Xray 对于鉴权失败（非合法 REALITY 请求）的流量，会直接转发至 `target`。[^c2-1]

字段上，该目标站官方叫 `target`，**旧称 `dest`**，两者互为 alias。[^c2-1] 这正是伪装成立的原因：扫描器看到的应是「有正常网站在应答」；若撞上「直接拒连」的端口，本身就是「这里有代理」的铁证。

代价与缓解（**推断，confidence: medium**）：若 `target` 恰是 Cloudflare 这类 CDN 背后的站点，你的服务器就相当于替它做端口转发，可能被扫后被人偷跑流量。[^c2-1] 官方缓解方向：前置 Nginx 按 SNI 过滤，或用 `limitFallbackUpload` / `limitFallbackDownload` 限速。[^c2-1] 但**回落限速本身是一种特征**：

> 回落限速是一种特征，不建议启用，如果您是面板/一键脚本开发者，务必让这些参数随机化。[^c2-1]

故官方建议优先「偷同 ASN 的证书」（大概率用不到限速），不得已借免费 CDN 证书时才考虑限速。[^c2-1]

> [!tip] 大白话
> 把回落想成「前台代接电话」：打错的电话不挂断（太可疑），而是转给真正的公司。所以……越像普通网站越好；但转接速度掐得很怪又是新破绽。

## 2.4 客户端证书三分支与 spider 模式

鉴权通过时客户端收到**临时可信证书**（由临时认证密钥签发，服务端确认对方合法后自行生成）。[^c2-2] 三种情况会让客户端拿到**目标站真实证书**：[^c2-2]

- 服务端拒绝该 Client Hello 并把流量转给目标站（即 2.3 回落）；
- 客户端的 Client Hello 被中间人转发到目标站；
- 发生中间人攻击，可能由目标站协助，或属证书链攻击。

客户端能区分三类证书并决定下一步：[^c2-2]

| 客户端收到的证书 | 含义 | 客户端行为 |
| --- | --- | --- |
| 临时可信证书 | 由服务端临时认证密钥签发，鉴权通过 | 连接正常可用 |
| 真实（目标站）证书 | 服务端拒绝并回落，或中间人转发 / 证书链攻击 | 进入 spider 模式 |
| 无效证书 | 无法验证 | 触发 TLS alert，终止连接 |

据官方文档归纳，客户端靠 `password`（旧称 `publicKey`）校验临时证书签名；真实证书非该密钥签发故判为「非本服务端」，转入 spider 模式并按 `spiderX` 访问目标站。[^c2-1][^c2-2]

> [!tip] 大白话
> 三种证书像**验钞**：临时可信证书是你自印、自己人才认的标记；真实证书是「钱是真的，但不是我家发的」；无效证书是假钞。所以……拿到真钞就装作普通顾客继续逛（spider 模式），假钞才摁铃。

## 2.5 适用边界与路线图

REALITY 是传输安全层，理论上能与别的协议组合，但官方明确不推荐：

> REALITY can also be used in conjunction with proxy protocols other than XTLS, but it is **not recommended** as they exhibit clear **TLS-in-TLS** characteristics that have already been targeted.[^c2-2]

即非 XTLS 协议配 REALITY 会呈现明显的 **TLS-in-TLS**（TLS 套 TLS）特征，且这类特征早已被针对。[^c2-2] 据官方文档归纳，外层 REALITY 借的是目标站一层 TLS 外观，内层协议若又自带一层 TLS，两层叠起来反而不像普通网站流量。这与第一章「`security = none` 时 VLESS/Trojan 仅限私网」合起来，正好解释当前主线为何是 VLESS + XTLS Vision + REALITY。

路线图：REALITY 下一主要目标是 **prebuilt mode**（预先收集目标网站特征），XTLS 下一主要目标是 **0-RTT**。[^c2-2]

## 小结

- REALITY 不是新协议，而是 TLS 的一种修改：服务端为 Go 1.19.5 `tls` 包的 fork，借目标站的 TLS 外观与握手特征伪装。[^c2-1][^c2-2]
- 官方收益：消除服务端 TLS 指纹、保持前向保密、使证书链攻击失效，无需买域名或配 TLS 服务器即可全程呈现指定 SNI。[^c2-2]
- 目标站最低要求为境外、支持 TLSv1.3 与 H2、不重定向；加分项含 IP 邻近、握手报文已加密、OCSP Stapling。[^c2-2]
- 鉴权失败时流量被转发至 `target`（旧称 `dest`）而非拒绝；被 CDN 偷跑流量的代价与缓解为推断（confidence: medium），且回落限速本身是特征、官方不建议启用。[^c2-1]
- 客户端按「临时可信证书 / 真实证书 / 无效证书」分别进入正常连接、spider 模式、终止连接；非 XTLS 协议配 REALITY 呈现 TLS-in-TLS 特征，不推荐。[^c2-1][^c2-2]

下一章（第三章：落地前的 VPS 硬化基线）从原理转向动手：把 443 暴露出去前，先关掉该关的服务、配好防火墙。

[^c2-1]: REALITY 官方配置文档（Xray-core docs），https://xtls.github.io/config/transports/reality.html
[^c2-2]: Xray-examples REALITY 设计说明（英文），https://github.com/XTLS/Xray-examples

---

## 第三章：落地前的 VPS 硬化基线

本章回答一个问题：在第 5 章把服务端口对外暴露之前，这台 VPS 应该先处于什么状态。正确顺序是「先缩小暴露面，再放服务」——把硬化当作上线前的基线，而不是被扫到之后的补丁。

## 3.1 安全策略与风险模型

先定策略，再挑工具。Debian 手册把「风险」定义为三个问题的答案：要保护什么、要防止什么发生、谁会尝试使其发生；三者答清，策略才有落点[^c3-S10]。手册还否定「装个工具就安全」的错觉：「Security is a process, not a product」[^c3-S10]。

对单台 VPS 可归纳出三条要点。其一，**短边界优于长边界**：边界短而明确比漫长曲折的边界更好防守，敏感服务应集中在少量机器、只经最少检查点访问（据 S-10 归纳）[^c3-S10]。其二，**优先停用不需要的服务**：与其用包过滤阻止对某服务的访问，不如让服务根本不监听不该开放的接口，或直接停用、卸载不需要的服务[^c3-S10a]。其三，**包过滤只是补充而非唯一防线**：防火墙只对确实经过它的数据包有效[^c3-S10a]。

> [!tip] 大白话
> 把 VPS 想成仓库：与其在门口摆安检机（包过滤），不如先把不需要的门砌死（停用服务）。

## 3.2 防火墙 nftables

包过滤是「最少检查点」的执行者。Debian 自 Buster 起默认使用 nftables 框架，旧 `iptables` 命令已改为走 nftables 内核 API[^c3-S10a]。

与 iptables 不同，**nftables 没有默认表**，表的数量与内容都由用户自建；每张表必须且只能属于 `ip`、`ip6`、`inet`、`arp`、`bridge` 五个 family 之一，未指定时默认 `ip`[^c3-S10a]。链分两类：**base chain** 注册进 Netfilter hook，是数据包进入网络栈的入口，能看到流量；**regular chain** 不挂 hook，只能作为 `jump` 目标组织规则[^c3-S10a]。规则由「匹配表达式 + verdict」组成，verdict 取值有 `accept`、`drop`、`queue`、`continue`、`return`、`jump chain`、`goto chain`[^c3-S10a]。

持久化与开机装载：`nft` 的改动不会自动持久化，规则存于 `/etc/nftables.conf`，可用 `nft list ruleset > /etc/nftables.conf` 保存，开机装载需 `systemctl enable nftables`[^c3-S10a]。迁移路径：单条命令用 `iptables-translate` / `ip6tables-translate`，整份规则集先用 `iptables-save` 导出、再经 `iptables-restore-translate` 转换；`iptables-nft` 一类命令只作向后兼容[^c3-S10a]。

下面的最小规则集是我据 S-10a 语法自行编写的（**推断**）；S-10a 只给语法与装载方式，未提供面向 VPS 的现成规则集[^c3-S10a]。

```nft
# /etc/nftables.conf —— 推断：非手册原文，按最小开放原则编写
table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;   # 默认拒绝
        ct state established,related accept   # 放行已建立连接的回包
        iif "lo" accept                        # 放行回环
        tcp dport { 22, 443 } accept           # 只开 SSH 与节点端口，按需增删
        icmp type echo-request accept          # 允许 ping
    }
    chain forward { type filter hook forward priority filter; policy drop; }
    chain output  { type filter hook output  priority filter; policy accept; }
}
```

> [!tip] 大白话
> 把 nftables 想成门禁账簿：表是账本，base chain 是站门口的门、regular chain 只是备注页，verdict 是放行 / 丢弃 / 转交。规则不写回 `/etc/nftables.conf`，重启即失效。

## 3.3 fail2ban

**定位与机制**。暴力破解的缓解思路是限制同一来源的登录尝试次数、临时封禁该 IP——这正是 Fail2Ban 的定位，它能监控任何把登录尝试写进日志的服务[^c3-S10b]。它扫描日志（如 `/var/log/auth.log`），对失败登录过多的 IP 更新防火墙规则、拒绝其新连接；开箱支持 sshd、Apache 等日志，自 v0.10 起支持 IPv6[^c3-S11]。

**能力边界**。它只能降低失败认证的速率，无法消除弱认证本身的风险（官方建议改用双因素或公私钥认证）[^c3-S11]；也无法应对分布式暴力破解（大量机器分散尝试）[^c3-S10b]。

**配置与覆盖约定**。四类配置文件都在 `/etc/fail2ban/`：`fail2ban.conf`（全局）、`filter.d/*.conf`（识别认证失败）、`action.d/*.conf`（封禁/解封命令）、`jail.conf`（filter 与 action 的组合即 jail）[^c3-S10b]。约定是**不要直接修改 `jail.conf`**，启用或配置 jail 要写进 `/etc/fail2ban/jail.d/defaults-debian.conf` 或同目录文件，以免升级被覆盖[^c3-S10b]。以 sshd jail 为例，手册默认值是 `bantime = 10m`、`findtime = 10m`、`maxretry = 5`：10 分钟内 5 次失败，封来源 IP 10 分钟[^c3-S10b]。

```ini
# /etc/fail2ban/jail.d/defaults-debian.conf —— 推断：覆盖写法示意，取值取自 S-10b
[sshd]
bantime  = 10m
findtime = 10m
maxretry = 5
```

> [!warning] 两处口径不要混用
> S-11 的 README 面向**源码安装**，讲的是复制 `init.d` 脚本、`update-rc.d` 那套步骤，且未给出任何默认 jail 数值[^c3-S11]。Debian 用 apt 包安装时，默认值与配置目录以 S-10b 为准[^c3-S10b]。两处不能混用。

## 3.4 拥塞控制 sysctl

本节只讲键名与语义，不涉及具体算法的收益。五个键都属于 `net.ipv4.tcp_*`：

| 键名 | 类型 | 语义 |
| --- | --- | --- |
| `tcp_congestion_control` | STRING | 为新连接选择拥塞控制算法；`reno` 始终可用，其他取决于内核配置；默认由内核配置阶段决定；被动连接继承监听套接字的选择[^c3-S12] |
| `tcp_available_congestion_control` | STRING（只读） | 显示已注册的可用算法；更多算法可能以模块形式存在但尚未加载[^c3-S12] |
| `tcp_allowed_congestion_control` | STRING | 显示/设置非特权进程可用的选项，是上者的子集[^c3-S12] |
| `tcp_ecn` | INTEGER | 仅当两端都表示支持时使用 ECN；让支持的路由器在丢包前发出拥塞信号；协商选出双方都支持的最高反馈变体[^c3-S12] |
| `tcp_slow_start_after_idle` | BOOLEAN | 启用时按 RFC2861 行为，空闲期（以当前 RTO 界定）后使拥塞窗口超时；关闭则空闲后不重置窗口[^c3-S12] |

切换算法的前提（**推断**）：目标算法须出现在 `tcp_available_congestion_control` 中（模块已加载）；若由非特权进程选择，还须落在 `tcp_allowed_congestion_control` 白名单内[^c3-S12]。

```ini
# /etc/sysctl.d/90-net.conf —— 推断：写入方式示意，键名与语义见上表
net.ipv4.tcp_congestion_control = <已注册的算法名>
net.ipv4.tcp_slow_start_after_idle = 0
```

> [!warning]
> 这份内核文档全文未点名 BBR，因此本节只给参数名与语义，**不做任何吞吐或延迟收益断言**[^c3-S12]。

## 小结

- 硬化先定策略：把风险模型三问答清，记住「Security is a process, not a product」[^c3-S10]。
- 最有效的一步是缩小边界：停用不需要的服务，包过滤只作补充[^c3-S10a]。
- nftables 无默认表，规则靠 `/etc/nftables.conf` + `systemctl enable nftables` 持久化，旧命令走 `iptables-translate` 迁移[^c3-S10a]。
- fail2ban 只缓解暴力破解、不消除弱认证风险；改配置写进 `jail.d/`，默认 `10m/10m/5`[^c3-S10b][^c3-S11]。
- 拥塞控制只认键名与语义；内核文档未点名 BBR，不做性能断言[^c3-S12]。

日志监控（logcheck）、文件完整性与被入侵后的处置属于「长期在线后要看的东西」，另见第 4 章。

[^c3-S10]: Debian 管理员手册，第 14 章《Security》（含 14.1 定义安全策略）。https://debian-handbook.info/browse/stable/security.html
[^c3-S10a]: 同上，14.2《Firewall or Packet Filtering》。https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html
[^c3-S10b]: 同上，14.3《Supervision: Prevention, Detection, Deterrence》。https://debian-handbook.info/browse/stable/sect.supervision.html
[^c3-S11]: fail2ban 官方仓库 README。https://github.com/fail2ban/fail2ban
[^c3-S12]: Linux Kernel Documentation — IP Sysctl。https://docs.kernel.org/networking/ip-sysctl.html

---

## 第四章：监控、文件完整性与被入侵后的处置

第 3 章收窄了暴露面，但节点长期在线：你需要在攻击者试探时就察觉，并在真被进来后知道先做什么。本章与第 3 章互不依赖（防火墙、fail2ban、sysctl 见第 3 章）。

## 4.1 日志监控 logcheck

日志没人读等于没写。`logcheck` 默认**每小时**检查一次日志，把不寻常的消息邮件给管理员；清单在 `/etc/logcheck/logcheck.logfiles`。[^c4-s10b]

```bash
cat /etc/logcheck/logcheck.logfiles
```

模式有三种：`paranoid`（极啰嗦）、`server`（**默认，官方推荐多数服务器**）、`workstation`（最简）。规则按作用分目录：`/etc/logcheck/cracking.d/` 判定入侵尝试、`cracking.ignore.d/` 取消该判定；`/etc/logcheck/violations.d/` 归类安全告警、`violations.ignore.d/` 取消该归类；其余按"系统事件"处理，且被判定的消息只能由对应 `.ignore.d/` 规则忽略。[^c4-s10b]

> [!tip] 大白话
> 像每小时巡一圈的值班员：只把"看着不对"的记录丢进你邮箱；`server` 即普通办公楼的巡逻强度。

## 4.2 文件完整性与包校验

系统装好后（除安全更新）多数文件本不该变化，异常变化值得追查。AIDE 拿一份"合法系统镜像"逐项比对：镜像存为数据库 `/var/lib/aide/aide.db`，由 `aideinit` 初始化，之后**每天**由 `/etc/cron.daily/aide` 校验，变化写入 `/var/log/aide/*.log` 并邮件通知。[^c4-s10b]

```bash
sudo aideinit     # 初始化基线库 → /var/lib/aide/aide.db
sudo dpkg -V      # 校验已安装包的文件是否被改动
```

`dpkg -V` 能找出被改动的包文件，但**局限是决定性的**：校验和取自本机 dpkg 数据库（`/var/lib/dpkg/info/*.md5sums`），原文 "a thorough attacker will therefore update these files"——拿到 root 的攻击者会把校验和一并改掉，故输出**不能当可信证据**。AIDE 同理：库在本地，root 可替换它掩盖痕迹（缓解办法是把参考数据放到只读介质）。[^c4-s10b] 即：**这类"本机自证"手段都可被 root 攻击者同步篡改。**

> [!tip] 大白话
> 像给全屋家具拍照存档、每日比对；但相册也在屋里，小偷能顺手换掉照片——它是"提示灯"，不是"判决书"。

## 4.3 网络层检测 suricata

前两项是本机视角，`suricata` 看网络：它是 NIDS，监听网络以发现渗透企图与敌意行为（含 DoS），事件落在 `/var/log/suricata`。[^c4-s10b]

配置是 `/etc/suricata/suricata.yaml`。**最小配置**要设 `HOME_NET`（本网地址范围，即全部潜在攻击目标）与监控 `interface`；建议设 `LISTENMODE=pcap`，因为默认的 `nfqueue` 还需在 netfilter 上配 `NFQUEUE` 转发才能用。[^c4-s10b] **固有局限**：有效性受限于网卡实际看到的流量——**它像门口的摄像头，只看得见镜头对着的那条通道**：接普通交换机只能看到针对本机的攻击，故应接镜像端口。[^c4-s10b] 单机 VPS 是否值得上它需自行取舍（据官方文档归纳）。

## 4.4 被入侵后的处置顺序

官方**没有**统一响应清单；下列顺序据 14.7 各小节归纳（推断），实操并不严格串行。[^c4-s10][^c4-s10c]

1. **发现线索**：入侵常在影响服务后才暴露（变慢、连不上），典型线索是不该存在的进程。

```bash
ls -al /proc/3719/exe
# → /proc/3719/exe -> /var/tmp/.bash_httpd/psybnc  （以 www-data 身份运行，可断定被入侵）
```

2. **断网**：攻击者需网络才能达成目标（窃数据、当跳板等）。物理可达就直接拔线；**异地托管则先采集重要信息，再尽量关停服务**（通常除 `sshd` 外全停），且无法排除攻击者有同等 SSH 权限。[^c4-s10c]
3. **保全证据**：至少硬盘内容、运行进程列表、开放连接列表。检查限于最小命令集（`netstat -tupan`、`ps auxf`、`ls -alR /proc/[0-9]*`）并逐条记录——原文："Every command is potentially subverted and can erase pieces of evidence."。避免"热分析"：被替换的 `ps`、`ls` 甚至内核都可能被篡改。[^c4-s10c]
4. **重装**：未经完整重装不应重新上线；若攻击者已取得管理员权限，几乎只有重装能清掉一切（尤其后门），并须打齐更新。不要用晚于被入侵时间点的备份，理想情况只恢复数据、软件从安装介质重装。[^c4-s10c]
5. **取证分析**：服务恢复后再细看磁盘镜像，目标是定位攻击入口。挂载须带 `ro,nodev,noexec,noatime`，以免改动内容或误运行被篡改的程序；入手点：`.bash_history`、近期增改访问的文件、`strings` 提取的文本串、`/var/log` 的时间线。[^c4-s10c]

> [!warning] 别按小节号机械排序
> 成像、重装、分析三者**交叠**：官方小节里"重装"（14.7.4）反而排在"取证分析"（14.7.5）前，次序本身交叉。更贴近实操的是：**先成像保全，再重装恢复服务，分析可在成像后并行**——成像与重装不依赖分析；分析结果又反过来决定重装堵哪个入口。[^c4-s10c]

> [!tip] 大白话
> 像着火后：先拍照留证（成像），同时修楼恢复营业（重装），事后才研究起火原因（分析）；三者本可并行。

## 小结

- `logcheck` 默认每小时巡检日志并邮件上报；`server` 是默认且推荐多数服务器的模式，规则分 `cracking.d/` 与 `violations.d/`。
- AIDE 以 `/var/lib/aide/aide.db` 每日校验（`aideinit` + `/etc/cron.daily/aide`）；`dpkg -V` 可查包文件改动，但校验和取自本机、可被同步更新，**均不能当可信证据**。
- `suricata` 最小配置为 `HOME_NET` + 监控 `interface`，建议 `LISTENMODE=pcap`；有效性受限于网卡实见流量。
- 处置顺序：**发现线索 → 断网 → 保全证据 → 重装 → 取证分析**（据官方文档归纳）；三者交叠，不应机械串行。

下一章进入服务端配置：用 VLESS + XTLS Vision + REALITY 写出可照抄的 `config.json`，把前两章的概念落到具体字段上。

[^c4-s10]: The Debian Administrator's Handbook, Chapter 14 Security（14.1 Defining a Security Policy，并作为 14.7 各小节顺序的总纲）— https://debian-handbook.info/browse/stable/security.html
[^c4-s10b]: The Debian Administrator's Handbook, 14.3 Supervision: Prevention, Detection, Deterrence — https://debian-handbook.info/browse/stable/sect.supervision.html
[^c4-s10c]: The Debian Administrator's Handbook, 14.7 Dealing with a Compromised Machine — https://debian-handbook.info/browse/stable/sect.dealing-with-compromised-machine.html

---

## 第五章：服务端配置——VLESS + XTLS Vision + REALITY

这一章把第一章的分层模型与第二章的 REALITY 原理，落成一份能直接照抄的 `config.json`。服务端配置是整条链路的锚点：客户端几乎所有字段都要与这里对齐，所以先把服务端写死、写对，后续第六章的配对才有基准。本章只写服务端。

## 5.1 服务端骨架

一份可用的服务端配置只有两件东西：一个入站（接收客户端）和一个出站（把解密后的流量直送公网）。先看完整文件，再逐段拆解——除两个需你自己生成的占位值外，其余字段可直接照抄[^c5-S6a]：

```jsonc
// /usr/local/etc/xray/config.json
{
  "inbounds": [
    {
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "REPLACE-WITH-OUTPUT-OF-xray-uuid",       // ./xray uuid 生成
            "flow": "xtls-rprx-vision"                       // 指定后客户端必须启用 XTLS
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "method": "raw",                                     // 官方字段表写法；官方示例仍用旧名 "network": "tcp"
        "security": "reality",
        "realitySettings": {
          "target": "example.com:443",                       // 必填，旧称 dest
          "serverNames": ["example.com", "www.example.com"],
          "privateKey": "REPLACE-WITH-OUTPUT-OF-xray-x25519", // ./xray x25519 生成
          "shortIds": ["", "0123456789abcdef"]
        }
      },
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls", "quic"],
        "routeOnly": true
      }
    }
  ],
  "outbounds": [
    { "protocol": "freedom", "tag": "direct" }
  ]
}
```

骨架里的关键字段，逐项对齐：

| 位置 | 值 | 为什么 |
| --- | --- | --- |
| `inbounds[0].port` | `443` | 借用 HTTPS 端口；官方示例只写 `port`，不含 `listen` |
| `inbounds[0].protocol` | `"vless"` | 与 REALITY 搭配的主线协议 |
| `streamSettings.method` | `"raw"` | 传输方式 RAW；官方示例改用旧名 `network: "tcp"`（**推断**：两者指同一设置，官方字段表只列 `method`）；REALITY 仅支持 RAW/XHTTP/gRPC |
| `streamSettings.security` | `"reality"` | 启用 REALITY 作为传输安全层 |
| `settings.decryption` | `"none"` | VLESS 服务端的固定占位值 |
| `settings.clients[0].id` | UUID | 用 `./xray uuid` 生成，客户端 `id` 必须与之相同 |

`clients[0].flow` 取 `"xtls-rprx-vision"`。按官方示例注释，它「if specified, clients must enable XTLS」——一旦指定，客户端侧也必须启用 XTLS。[^c5-S6c]

> [!tip] 大白话
> 把入站想成一栋写字楼的收发室：`port 443` 是它的门牌，`protocol vless` 是它收包裹的格式，`security reality` 是门口那套「看起来像普通 HTTPS 大楼」的装修。`id` 则是员工工牌——只有工牌对得上的包裹才被受理。

## 5.2 REALITY 服务端四参数

`realitySettings` 在服务端有四个必填字段，缺一不可。字段表以官方仓库原文为准[^c5-S2]：

| 字段 | 必填 | 语义与取值 |
| --- | --- | --- |
| `target` | 是 | 要借用外观的目标站，格式同 VLESS `fallbacks` 的 `dest`；**旧称 `dest`，两字段互为 alias** |
| `serverNames` | 是 | 允许客户端使用的 `serverName` 列表；「不支持 `*` 通配符」 |
| `privateKey` | 是 | 「执行 `./xray x25519` 生成」；其对应公钥即客户端 `password` |
| `shortIds` | 是 | 客户端可用的 `shortId` 列表，「可用于区分不同的客户端」；含空值则客户端 `shortId` 可为空 |

几点容易踩的细节：

- **`target` 也是客户端/服务端的判定开关**。官方原文：「核心按照这个字段是否存在区分是当前是客户端还是服务端配置，不要在客户端填写，否则会造成识别异常。」[^c5-S2]
- **`serverNames` 一般与 `target` 一致**，或取目标站证书的 SAN；列表可包含空值 `""`，代表接受没有 SNI 的连接。
- **`shortIds` 有格式硬约束**：取值只能 `0`–`f`，「长度为 8 个字节，即 16 个 0~f 的数字字母，可以小于 16 个，核心将会自动在后面补 0，但位数必须是**偶数**」。因此 `aa1234` 会被自动补成 `aa12340000000000`，而 `aaa1234`（奇数位）会直接报错。[^c5-S2]

> [!tip] 大白话
> 把 REALITY 想成「借邻居家的门面」：`target` 是你借的那家店（访客看到的招牌就是它），`serverNames` 是「允许挂这块招牌的域名清单」，`privateKey` 是你和熟客之间的暗号（熟客按暗号进门，外人被引到邻居店里正常逛），`shortIds` 则是发给不同熟客的短号，用来区分谁是谁。

## 5.3 路由与嗅探

`sniffing` 块负责「看一眼流量本来要去哪」，`outbounds` 则只有一条直出。两者配合决定流量怎么走：

| 字段 | 值 | 作用 |
| --- | --- | --- |
| `sniffing.enabled` | `true` | 开启流量嗅探 |
| `sniffing.destOverride` | `["http","tls","quic"]` | 从 HTTP / TLS / QUIC 报文里读出真实目标域名 |
| `sniffing.routeOnly` | `true` | **只用嗅探结果做路由，不改写目标地址** |
| `outbounds[0].protocol` | `"freedom"` | 直接出站，连接目标 |
| `outbounds[0].tag` | `"direct"` | 出站标识 |

`routeOnly: true` 是这里的关键：**推断**（官方示例给出了该配置，但未解释其语义），没有它，嗅探出的域名会被写回连接的目标地址；置为 `true` 后，嗅探结果只用于路由判断，实际仍按原地址发起连接。官方示例固定使用 `routeOnly: true`。[^c5-S6a]

`outbounds` 只有一条 `freedom` 出站（`tag: "direct"`）。回落不需要额外的出站规则：官方说明对鉴权失败的流量「会**直接转发**至 target」，回落由 `target` 承担 [^c5-S2]；**推断**——这份骨架不需要为回落另写一条出站，是据官方示例的结构归纳，官方未明说这一点。[^c5-S6a]

> [!tip] 大白话
> 嗅探像前台「拆开信封看一眼收件地址」；`routeOnly: true` 表示只看不动信封——知道寄给谁就行，别去改快递单上的地址。

## 5.4 进阶字段

下面这些字段官方示例未出现，属选填，按需再加。它们同样出自官方仓库字段表[^c5-S2]，也是抓取版文档漏掉、必须回仓库原文核对的一批：

| 字段 | 侧 | 必填 | 语义 |
| --- | --- | --- | --- |
| `show` | 服务端 | 选填 | 「值为 `true` 时，输出调试信息」 |
| `xver` | 服务端 | 选填 | 格式同 VLESS `fallbacks` 的 `xver` |
| `minClientVer` / `maxClientVer` | 服务端 | 选填 | 允许的客户端 Xray 最低 / 最高版本，格式 `x.y.z` |
| `maxTimeDiff` | 服务端 | 选填 | 「允许的最大时间差，单位为毫秒」 |
| `mldsa65Seed` | 服务端 | 选填 | 为发给客户端的证书附加后量子签名所用的私钥，算法 ML-DSA-65；用 `xray mldsa65` 生成 |
| `mldsa65Verify` | 客户端 | 选填 | 客户端侧对应 `mldsa65Seed` 的验证公钥，属第六章范围 |

`mldsa65Seed` 有两处硬条件值得留意：启用后「target 所返回的证书长度**必须**大于 3500」，否则临时证书变大反而形成特征；且为取得完整的后量子安全，`target` 也需支持后量子密钥交换 X25519MLKEM768。两者都可用 `xray tls ping example.com` 查看。[^c5-S2]

## 5.5 新旧命名与字段表口径

同一组字段在官方来源里有新旧两个名字，这是老教程对不上的最常见原因：

| 服务端字段（现名） | 旧称 | 说明 |
| --- | --- | --- |
| `target` | `dest` | 「旧称 dest, 当前版本两个字段互为 alias」 |

差异来自文档版本：Xray-examples 官方示例（S-6a）仍写 `dest`，而 xtls 官网 REALITY 文档（S-2）已改用 `target`。[^c5-S6a][^c5-S2] 两处都在 tier-1 官方来源里，**不是错误，是改名过渡**。

因此本章的**字段表一律以官方仓库原文（`DOCSRC_reality.md`）为准**，不抄抓取版。爬取 `reality.html` 得到的副本里 `RealityObject` 代码块被截断，漏掉了 `show`、`mldsa65Seed`、`minClientVer`/`maxClientVer`/`maxTimeDiff` 等字段；核对仓库原文后字段才完整。[^c5-S2]

上面 5.1 的配置为与最新文档保持一致，服务端统一用现名 `target`；由于二者互为 alias，写 `dest` 同样有效。

## 小结

- 服务端配置 = 一个 VLESS 入站 + 一条 `freedom` 直出；`port 443`、`protocol vless`、`network tcp`、`security reality`、`decryption "none"` 是骨架定式。
- `clients[0].id` 用 `./xray uuid` 生成，`flow: "xtls-rprx-vision"` 一旦指定，客户端必须启用 XTLS。
- REALITY 服务端四参数必填：`target`（旧称 `dest`）、`serverNames`（不支持 `*`）、`privateKey`（`./xray x25519`）、`shortIds`；`shortIds` 位数必须是 2 的倍数、最大 16。
- `sniffing.destOverride: [http,tls,quic]` 配 `routeOnly: true`，只嗅探不改地址；回落由 `target` 承担，无需额外出站。
- 进阶字段（`show`、`xver`、`minClientVer`/`maxClientVer`/`maxTimeDiff`、`mldsa65Seed`/`mldsa65Verify`）以仓库原文为准，抓取版有缺漏。

下一章写客户端：它要与本章的服务端结构对称，并把 `id`、`shortId`、`serverName` 等字段逐一配对。

[^c5-S2]: REALITY 官方配置文档（Xray-core 仓库原文），https://xtls.github.io/config/transports/reality.html
[^c5-S6a]: Xray-examples 服务端配置示例 VLESS-TCP-XTLS-Vision-REALITY，https://github.com/XTLS/Xray-examples
[^c5-S6c]: Xray-examples REALITY 设计说明（英文），https://github.com/XTLS/Xray-examples

---

## 第六章：客户端配置——结构对称与字段配对

服务端配好之后（见第五章），客户端只需回答两个问题：本机程序把流量交给谁，以及这份流量凭什么让服务端认出是自己人。Xray 客户端与服务端共用同一套配置结构，因此这两个问题最终都落在字段级：传输层结构必须对称，鉴权字段必须与第五章生成的那组值一一配对。本章先给骨架，再给对齐关系，最后列出地雷，产出一份可直接照抄的客户端 `config.json`。

## 6.1 客户端骨架

客户端配置里真正起作用的只有两个顶层数组：`inbounds` 负责「接住」本机程序发出的流量，`outbounds` 负责把它转交给服务端。入站是一条本地 SOCKS 代理，官方客户端示例把它固定成回环地址上的一个端口。

```json
{
  "inbounds": [
    {
      "listen": "127.0.0.1",
      "port": 10808,
      "protocol": "socks",
      "settings": { "udp": true }
    }
  ]
}
```

`listen: "127.0.0.1"` 表示只监听回环地址，局域网内其他机器访问不到这个代理口；`port: 10808` 是之后本地程序要填的代理端口；`settings.udp: true` 让这条 SOCKS 同时转发 UDP，否则只有 TCP 会走代理。这三项与官方客户端示例一致 [^c6-S6b]。

> [!tip] 大白话
> 入站像家里的一扇内门：`127.0.0.1:10808` 只开给本机，邻居（同一局域网的别的机器）进不来；`udp: true` 相当于告诉这扇门「既过人、也过小车」，别只放行行人（TCP）把 UDP 流量挡在门外。

## 6.2 出站与传输层对齐

出站分两半：`settings` 说明「连谁、用什么身份、开哪种流控」，`streamSettings` 负责让传输层与服务端对齐。

```json
{
  "outbounds": [
    {
      "protocol": "vless",
      "settings": {
        "address": "your.server.example",
        "port": 443,
        "id": "",                      // 必须与服务端 clients[0].id 一致
        "encryption": "none",
        "flow": "xtls-rprx-vision"
      },
      "streamSettings": {
        "method": "raw",
        "security": "reality"
      },
      "tag": "proxy"
    }
  ]
}
```

| 字段 | 填什么 | 与服务端的关系 |
| --- | --- | --- |
| `address` | 服务端域名或 IP | 指向第五章那台服务端所在主机 |
| `port` | `443` | 与服务端 `inbounds[0].port` 相同 |
| `id` | UUID 字符串 | 必须等于服务端 `clients[0].id` |
| `encryption` | `"none"` | VLESS 的固定占位值，两侧一致 |
| `flow` | `"xtls-rprx-vision"` | 服务端指定 flow 后客户端必须启用 XTLS |
| `tag` | `"proxy"` | 仅本地标签，供路由引用，不参与协商 |

`id` 在官方示例中的注释是「Needs to match server side」，即必须与服务端 `clients[0].id` 一致 [^c6-S6b]。`streamSettings` 的 `method`/`security` 与服务端结构对称——传输层协商已在第一章说明，此处只需记住一端改动另一端必须跟随 [^c6-S2]。注意官方示例这里写的是旧名 `network: "tcp"`，而官方字段表只列 `method: "raw"`；**推断**：两者指同一设置，本笔记统一采用字段表口径 [^c6-S2][^c6-S6b]。

> [!tip] 大白话
> 这两份配置像同一张表的两栏：`id` 是双方共用的工牌号，`port`/`method`/`security` 是同一扇门和同一款锁芯。客户端要做的是如实写下「我是谁、去哪」，而不是擅自更换锁芯型号。

## 6.3 客户端 REALITY 字段

`security: "reality"` 打开后，真正决定能否通过鉴权的是 `realitySettings` 里的五个字段。它们的语义与约束以下表为准（取自官方文档仓库原文）[^c6-S2]：

| 字段 | 要求 | 语义 | 对应服务端字段 |
| --- | --- | --- | --- |
| `password` | 必填 | 服务端私钥对应的公钥，用 `./xray x25519 -i "服务器私钥"` 生成；旧称 `publicKey` | `privateKey` |
| `serverName` | 取 `serverNames` 之一 | 客户端声称访问的 SNI；设为任意 IP 可发送无 SNI 的 Client Hello（需服务端 `serverNames` 含空值） | `serverNames` |
| `shortId` | 服务端 `shortIds` 之一 | 用于区分不同客户端；取值 `0`~`f`，长度须为 2 的倍数、最大 16 | `shortIds` |
| `fingerprint` | 必填 | 用 uTLS 模拟的客户端 TLS 指纹，如 `chrome` | 无（仅客户端） |
| `spiderX` | 选填 | 爬虫初始路径与参数，建议每个客户端不同 | 无（仅客户端） |

关于命名要单独提醒一句：官方文档已把客户端这一项从 `publicKey` 改名为 `password`，理由是「旧称 publicKey, 为防止误解更名(这个东西地位上确实是 x25519 公钥但是在 REALITY 的设计中是客户端持有，不能公开)」[^c6-S2]；而官方客户端示例文件仍写作 `publicKey` [^c6-S6b]。本章字段表采用文档口径的 `password`，新旧命名对不上时放到第七章处理。

> [!tip] 大白话
> 这五个字段像进门要出示的五件东西：`password` 是配对钥匙（必须配得上服务端那把私钥），`serverName` 是你报的门牌号，`shortId` 是分机号，`fingerprint` 是你的口音（伪装成 Chrome），`spiderX` 是进门后先走的那条路线。任何一件与服务端登记的不符，就会被当成陌生人转发回真站。

## 6.4 配对关系与地雷

配对关系一次看完（左列客户端、右列服务端）：

| 客户端字段 | 必须匹配的服务端字段 | 匹配方式 |
| --- | --- | --- |
| `settings.id` | `clients[0].id` | 完全相同 |
| `realitySettings.password` | `realitySettings.privateKey` | 公钥/私钥配对 |
| `realitySettings.serverName` | `realitySettings.serverNames` | 属于该列表 |
| `realitySettings.shortId` | `realitySettings.shortIds` | 属于该列表 |
| `settings.flow` | `clients[0].flow` | 服务端指定后客户端必须启用 XTLS |

下面是四个最容易踩的地雷。

1. **`shortId` 的长度规则**。「长度为 8 个字节，即 16 个 0~f 的数字字母，可以小于16个，核心将会自动在后面补0, 但位数必须是**偶数** (因为一个字节有2位16进制数)」[^c6-S2]。也就是说 `aa1234` 会被自动补成 `aa12340000000000`，而 `aaa1234`（7 位，奇数）会直接报错；上限 16 位 [^c6-S6c]。
2. **`fingerprint` 不得填 `unsafe`**。文档明确「此处不支持使用 `unsafe` 禁用 utls, 因为 REALITY 协议实现使用了该库以操作底层 TLS 参数。」[^c6-S2]。
3. **客户端绝不能填 `target`**。「核心按照这个字段是否存在区分是当前是客户端还是服务端配置，不要在客户端填写，否则会造成识别异常。」[^c6-S2]
4. **服务端指定了 `flow`，客户端必须启用 XTLS**。服务端示例中 `flow: "xtls-rprx-vision"` 本为可选，但「Optional, if specified, clients must enable XTLS」，所以客户端也要写上同值的 `flow` [^c6-S6c]。

把以上各段拼起来，就是一份可直接照抄的完整客户端配置：

```json
{
  "log": { "loglevel": "warning" },
  "inbounds": [
    {
      "listen": "127.0.0.1",
      "port": 10808,
      "protocol": "socks",
      "settings": { "udp": true }
    }
  ],
  "outbounds": [
    {
      "protocol": "vless",
      "settings": {
        "address": "your.server.example",    // 服务端域名或 IP
        "port": 443,                          // 与服务端 inbounds[0].port 相同
        "id": "粘贴服务端 clients[0].id",      // 必须一致
        "encryption": "none",
        "flow": "xtls-rprx-vision"            // 与服务端 clients[0].flow 一致
      },
      "streamSettings": {
        "method": "raw",
        "security": "reality",
        "realitySettings": {
          "fingerprint": "chrome",            // 必填，不可用 unsafe
          "serverName": "example.com",        // 属于服务端 serverNames
          "password": "粘贴服务端公钥",         // 由 privateKey 推出；旧称 publicKey
          "shortId": "0123456789abcdef",      // 属于服务端 shortIds，偶数长度且不超过 16
          "spiderX": "/"                      // 建议每个客户端不同
        }
      },
      "tag": "proxy"
    }
  ]
}
```

去掉注释后即可直接使用。其中有五处必须按服务端实际值替换：`address`、`id`、`password`、`serverName`、`shortId`。

## 小结

- 客户端 = 一条本地 SOCKS 入站（`127.0.0.1:10808`，`settings.udp: true`）+ 一条 VLESS 出站。
- 出站的 `method`/`security` 与服务端结构对称，`id` 必须等于服务端 `clients[0].id`。
- REALITY 客户端五字段：`password`（旧称 `publicKey`）、`serverName`、`shortId`、`fingerprint`、`spiderX`。
- 四条地雷：`shortId` 须为偶数长度且不超过 16；`fingerprint` 不可用 `unsafe`；客户端不填 `target`；服务端给了 `flow` 客户端必须启用 XTLS。
- 配对清单：`id`、`password` ↔ `privateKey`、`serverName` ∈ `serverNames`、`shortId` ∈ `shortIds`、`flow` 一致。

下一章给出把这些配置真正跑通的验证路径：从本地 SOCKS 自检、字段配对检查清单，到连不上时如何顺着失败信号定位到具体字段。

[^c6-S2]: REALITY 官方配置文档，https://xtls.github.io/config/transports/reality.html （本地权威原文：`sources/DOCSRC_reality.md`）
[^c6-S6b]: Xray-examples 客户端配置（VLESS-TCP-XTLS-Vision-REALITY），https://github.com/XTLS/Xray-examples
[^c6-S6c]: Xray-examples REALITY 设计说明（英文），https://github.com/XTLS/Xray-examples

---

## 第七章：连通校验与字段对齐排错

服务端与客户端配置写完后，别急着对外运行——先确认链路真能通。REALITY 鉴权是隐式的：字段只要有一处对不上，你通常收不到「某某字段错误」，而是超时、握手失败或断开。本章给出一条自检路径和一张配对清单。

> [!warning] 本章是归纳，不是官方步骤
> 官方文档只逐字段描述配置项[^c7-s2]，设计说明只解释客户端证书分支语义[^c7-s6c]，**没有端到端连通校验教程**。故 7.1–7.4 的校验方法与排错树系据字段约束归纳（推断），非官方口径；凡属归纳处均在句中标注。

## 7.1 本地 SOCKS 自检

从本地开始，因为客户端最靠近你的一段是它的本地入站：官方示例把它定义为监听 `127.0.0.1:10808` 的 SOCKS 并打开 `udp`[^c7-s6b]，任何支持 SOCKS5 的本机程序都能经它出网。

自检步骤（推断）：① 用客户端内核加载 `config.json`，确认进程未因语法错误退出；② 把日志级别临时设为 `debug`（客户端示例首行即 `"log": {"loglevel": "debug"}`[^c7-s6b]），失败时能看到握手细节；③ 经本地 SOCKS 端口发请求观察返回。

```bash
# 经客户端本地入站发请求；--socks5-hostname 让域名在代理侧解析
curl --socks5-hostname 127.0.0.1:10808 -I https://example.com
```

返回被访问站点正常的响应头即说明链路成立。若 curl 连不上 `127.0.0.1:10808`，是内核没起或入站 `listen`/`port` 对不上；若 SOCKS 能连但请求超时或重置，故障就在客户端出站到服务端之间（推断），转入 7.2、7.4。

## 7.2 字段配对检查清单

两端有五处**必须成对**，缺一处鉴权就过不了（原文见[^c7-s2][^c7-s6b]）：

| # | 服务端字段 | 客户端字段 | 配对要求 |
| --- | --- | --- | --- |
| 1 | `clients[0].id` | `id` | 同一个 UUID（示例注释：Needs to match server side） |
| 2 | `privateKey` | `password` | 一对 X25519 公私钥 |
| 3 | `serverNames` | `serverName` | 客户端值 ∈ 服务端列表 |
| 4 | `shortIds` | `shortId` | 客户端值 ∈ 服务端列表 |
| 5 | `clients[0].flow` | `flow` | 两端取值一致（示例均为 `xtls-rprx-vision`） |

- 第 2 项：服务端 `privateKey` 用 `./xray x25519` 生成；客户端 `password`（旧称 `publicKey`）是「服务端私钥对应的公钥」，用 `./xray x25519 -i "服务器私钥"` 反推[^c7-s2]——同一对密钥的两半。
- 第 3、5 项：`serverNames`「不支持 `*` 通配符」[^c7-s2]，客户端 `serverName` 只能从列表里挑；`flow` 服务端选填，但「if specified, clients must enable XTLS」[^c7-s6c]，服务端写了就须在客户端配同一值。

> [!warning] 只能记死的一条
> 两端**共用同一个 `realitySettings` 块名**，但可填字段不同：`target` 是服务端字段，「不要在客户端填写，否则会造成识别异常」[^c7-s2]——客户端绝不能出现 `target`。

> [!tip] 大白话
> 五处配对像「对号入座」：`id` 是工牌号，`password` ↔ `privateKey` 是一把锁与唯一能开它的钥匙，`serverName`/`shortId` 必须在服务端「白名单」上；任一项填了名单外的值，门卫都不放行。

## 7.3 新旧命名对不上

照官方客户端示例抄会看到 `dest` 和 `publicKey`，翻官方字段表却是 `target` 和 `password`。**这不是版本错误，而是别名过渡**，两套名字都在 tier-1 官方源里[^c7-res]：

| 含义 | 旧名（示例 S-6a/S-6b） | 新名（字段表 S-2） | 关系 |
| --- | --- | --- | --- |
| 服务端伪装目标站 | `dest` | `target` | 互为 alias[^c7-s2] |
| 客户端持有的公钥 | `publicKey` | `password` | 旧称 `publicKey`，为「防止误解更名」[^c7-s2] |

服务端示例注释用 `dest`[^c7-s6a]、字段表用 `target`「旧称 dest」；客户端示例注释用 `publicKey`、字段表用 `password`「旧称 publicKey」（均见[^c7-s2][^c7-s6b]）。二者都指同一字段，**按含义配对，别当成两项**；查字段表一律以权威版为准[^c7-res]。

> [!tip] 大白话
> 像一个人改了名：示例还叫旧名，新文档改叫新名，**还是同一个人**；服务端见过「张三」、客户端又见「张小明」，别当两人各配一遍。

## 7.4 失败信号解读

配对对了，仍有几个「看着通了、其实没通」的信号：

- **`shortId` 位数**：取值为 0–f、最多 16 位，核心会自动在末尾补 0，「但位数必须是**偶数**」[^c7-s2]。故不足 16 位的偶数位自动补 0（`aa1234` → `aa12340000000000`），**奇数位直接报错**（`aaa1234` 报错）。
- **`serverName` 不匹配**：客户端 `serverName` 须为「服务端 `serverNames` 之一」[^c7-s2]。填了列表外的名字，鉴权过不了；按回落语义，非合法 REALITY 请求会被**直接转发至 `target`**[^c7-s2]（推断：客户端因而拿不到临时可信证书，落到 spider 模式）。
- **进入 spider 模式**：客户端正常应收到「temporary trusted certificate（临时可信证书）」；收到目标网站**真实证书**时，「the client enters spider mode」[^c7-s6c]。官方列三种会拿到真实证书的情形：服务端拒绝 Client Hello 并转往目标站、Client Hello 被中间人转发到目标站、发生证书链攻击[^c7-s6c]。**推断**：进入 spider 模式即你在和目标站而非自己的节点对话，常见诱因正是 `serverName` 不在白名单。

> [!tip] 大白话
> 正常握手该拿到一张「我方临时发的通行证」；spider 模式下拿到的是**对方公司的真名片**——说明请求被转到了伪装用的目标站，先回 7.2 核 `serverName`。

## 小结

- 官方**没有**端到端连通校验教程；本章方法系归纳（推断），全章适用。
- 五处硬配对：`id` 两端一致、`password` ↔ `privateKey` 同一对 X25519 密钥、`serverName ∈ serverNames`、`shortId ∈ shortIds`、`flow` 两端一致；`target`/`dest`、`password`/`publicKey` 是别名过渡，按**含义**配对。
- 三个失败信号：`shortId` 奇数位报错（偶数位不足 16 位自动补 0）、`serverName` 不在白名单致鉴权失败并被转发至 `target`、收到真实证书即进入 spider 模式。

[^c7-s2]: S-2 REALITY 官方配置文档. https://xtls.github.io/config/transports/reality.html
[^c7-s6a]: S-6a Xray-examples 服务端配置（VLESS-TCP-XTLS-Vision-REALITY）. https://github.com/XTLS/Xray-examples
[^c7-s6b]: S-6b Xray-examples 客户端配置（同上目录）. https://github.com/XTLS/Xray-examples
[^c7-s6c]: S-6c Xray-examples REALITY 设计说明（英文）. https://github.com/XTLS/Xray-examples
[^c7-res]: 02_deep_research.md 第五节「矛盾、别名与注意点」.
