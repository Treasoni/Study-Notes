# 第二章：REALITY 原理——不是新协议，是 TLS 的变体

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
