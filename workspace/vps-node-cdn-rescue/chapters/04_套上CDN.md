# 第 4 章 把节点套上 CDN（TLS / 端口 / WS）

域名侧通了，只解决了一半：请求能到 Cloudflare。另一半是 **Cloudflare 能不能顺利把请求交回你的源站**——这一步由端口、TLS 模式、传输方式三个条件共同决定，任何一个不满足，你看到的都是报错而不是连通。本章只讲 Cloudflare 侧与 Xray 侧的这些条件，**不含安装面板与搭建节点**（面板侧只给一句话指路，见 4.4）。

## 4.1 端口：哪些能代理，哪些代理了也不能缓存

Cloudflare 默认代理的 HTTP / HTTPS 端口共 **13 个**（来源：B-3 | `## Network ports compatible with Cloudflare's proxy`）：

| 类别 | 端口 |
|---|---|
| HTTP | 80, 8080, 8880, 2052, 2082, 2086, 2095 |
| HTTPS | 443, 2053, 2083, 2087, 2096, 8443 |

其中 **10 个可代理但缓存被禁用**（来源：B-3 | `Ports supported by Cloudflare, but with caching disabled`）：

| 可代理但禁用缓存的端口 |
|---|
| 2052, 2053, 2082, 2083, 2086, 2087, 2095, 2096, 8880, 8443 |

> [!warning] 「只有 80/443 走缓存」是**排除推论**，不是官方口径
> 官方文档**只列了这 10 个禁用缓存的端口**，并未正面说明其余端口是否走缓存。「13 个里 10 个禁用缓存 → 只有 80/443 走缓存」是由排除法得出的**推论**，此处明确标记为本笔记推论（来源：B-3 | 同上；02_deep_research.md | §三-3）。

想在列表之外用端口，官方只给两条路：**改成灰云**（绕过 Cloudflare 直连源站）或用 **Spectrum**（支持全部端口，但全端口 Spectrum 仅企业版）（来源：B-3 | `## How to enable Cloudflare's proxy for additional ports`）。把这两条官方事实拼起来即得一个**合成结论**：**免费版若要代理列表外的端口，唯一选择是放弃代理**——灰云等于方案自我取消，Spectrum 又要企业版（来源：同上；02_deep_research.md | §三-4）。

另两条限定：**中国方向**只有 80 与 443 兼容启用了 China Network 的域名（来源：B-3 | `Ports 80 and 443 are the only ports...`）；而列表外的端口常被扫描器报「开放」，那是 Cloudflare anycast 网络为其他客户在这些端口上服务的副作用，**不是你的服务暴露**（来源：B-3 | `Due to the nature of Cloudflare's anycast network...`）。

## 4.2 TLS 模式：两段连接，五种选择

**它是什么**：SSL/TLS 加密模式同时决定**两段连接**——访客 ↔ Cloudflare（第一段）与 Cloudflare ↔ 源站（第二段）（来源：B-4 | 首段）。

**具体产物**：可选模式共五种，差别就在「第二段怎么连、验不验证书」（来源：B-4 | `### Custom SSL/TLS`）：

| 模式 | 访客 ↔ CF | CF ↔ 源站 | 源站证书要求 | 典型场景 |
|---|---|---|---|---|
| Off | 明文 | 明文 | 无 | 不需要加密 |
| Flexible | HTTPS | **明文 HTTP** | 无 | 源站不支持 TLS |
| Full | 跟随访客协议 | HTTPS，**不验证**证书 | 可自签或无效 | 源站用自签证书 |
| Full (strict) | 跟随访客协议 | HTTPS，**验证**证书 | 有效、受信、CN/SAN 匹配 | 官方最推荐 |
| Strict (SSL-Only Origin Pull) | 任意 | 一律 HTTPS 且验证 | 同上 | 恒加密到源站 |

**带具体值的例子**：选 **Full**，源站只要「443 上能讲 HTTPS」即可，证书哪怕是自签也放行；选 **Full (strict)**，源站证书必须**同时**满足三条——**未过期**、由**公开受信 CA**（如 Let's Encrypt）或 Cloudflare Origin CA 签发、且 **CN 或 SAN 匹配被请求的主机名**；不满足就会撞上 **526**（来源：B-8 | `## Use when`、`### Prerequisites`）。所以一句话：**能不能用自签证书，就是 Full 与 Full (strict) 的分水岭**。

> [!tip] 大白话
> 把两段连接想成两段路、两个关卡：访客到 Cloudflare 是第一段，Cloudflare 到你的服务器是第二段。**Flexible 是「第一段锁门、第二段敞着」**；**Full 是「两段都加密，但保安不核对对方身份」**；**Full (strict) 才要求源站出示一张拿得出手的证件**（受信 CA 签发、没过期、名字对得上）——证件不合格，保安把人拦在门外，你看到的是 526。

顺带一句：默认是**自动模式（Automatic SSL/TLS）**，它会用探测器评估站点并逐档升级；不想要就切到 Custom SSL/TLS 手动选（来源：B-4 | `### Automatic SSL/TLS (default)`）。而 Flexible 虽常见于源站不支持 TLS 的情形，官方仍建议尽可能把源站配置升级上去（来源：B-4 | `### Custom SSL/TLS`）。

## 4.3 WebSocket：Cloudflare 侧开箱可用

Cloudflare **支持代理的 WebSocket 连接，无需额外配置**；开关在 dashboard 的 **Network** 页，**所有套餐可用**（来源：D-1 | 首段、`## Enable WebSockets`、`## Availability`）。

要留意三个「会断」的时机（来源：D-1 | `### Technical note`、`### Best practices`、`### Idle timeout`）：**空闲超时**——两个方向都没有数据达到一定时长即被关闭，官方建议客户端实现 **heartbeat（ping/pong）** 保活；**发布新代码**——Cloudflare 给全球网络发布新代码时可能重启服务器，**会中止 WebSocket 连接**；官方最佳实践是「实现 keepalive」并「检查、移除或延长源站 / 客户端侧的超时设置」。

Xray 侧的 `wsSettings` 字段（按官方字段名列出，**非完整可用配置**，来源：C-1 | `WebSocketObject`）：

```jsonc
// wsSettings：字段名与官方一致，此处只列字段与含义
{
  "acceptProxyProtocol": false,   // 仅 inbound：是否接收 PROXY protocol；不了解请忽略
  "path": "/",                    // HTTP 路径；带 ?ed=2560 启用 Early Data 降延迟（推荐 2560，最大 8192）
  "host": "xray.com",             // 请求发送的 host；服务端指定后即校验客户端 host（优先级 host > headers > address）
  "headers": { "key": "value" },  // 仅客户端：自定义 HTTP 头，键值对
  "heartbeatPeriod": 10           // 间隔发 Ping 保活；0 或不填则不发送
}
```

官方还有一条与「源地址」有关的提示：WebSocket 会识别 HTTP 请求的 `X-Forwarded-For` 头来覆写流量的源地址，**优先级高于 PROXY protocol**（来源：C-1 | 页首 TIP 块）。

> [!warning] 官方对 WebSocket 的立场是「建议迁移」，不是「推荐方案」
> Xray 官方 WebSocket 页首的 DANGER 块明确**建议换用 XHTTP**，理由是 WebSocket 存在「ALPN 是 http/1.1」等显著流量特征（来源：C-1 | 页首 DANGER 块）。因此本文把 WebSocket 写成**当前可用的传输方式**，而不是「官方推荐方案」。

## 4.4 落在源站上的一句话指路（不展开）

配置动作只剩一句：

> 在面板中把入站传输设为 **WebSocket**，Host / Path 填 **你的 CDN 域名与路径**；具体字段位置与截图见面板流 `[[07 搭建节点（带域名与 Cloudflare）]]`（总览见 `[[00 VPS 自建节点零基础全流程]]`）。

**必须标明这是推导**：面板表单字段与 Xray 字段的对应关系**没有官方文档**，是由 Xray 官方字段定义 + 面板表单结构推导而来（对照 C-1 的 `wsSettings` 字段即可看出对应）。本章**不**给字段填写表、不升级成操作小节，也不复述建节点流程。

## 4.5 443 复用两条路

同一台源站、同一个 443，要同时服务「真网站」和「代理入口」，有两条路：

- **Xray 内置 fallback 分流**：用 `fallbacks` 按 path / alpn 把非代理流量转给本机 web 服务；官方称其「没有多余处理、纯粹转发流量，**理论性能比 Nginx 更强**」（来源：C-7 | `> path`）。
- **Nginx / Caddy 反代分流**：由反代按路由把 WebSocket 流量转给节点入站，其余给网站；3x-ui wiki 给了 Nginx 与 Caddy 两套配置（来源：C-2 | `## Reverse Proxy`）。

fallback 被官方称作 Xray「最强大功能之一」，**可有效防止主动探测，并让常用端口多服务共享**；目前可在使用 VLESS 或 trojan 协议时通过 `fallbacks` 启用（来源：C-7 | 页首引言）。匹配时取**最精确的子元素**，与子元素排列顺序无关；若若干子元素的 alpn 与 path 都相同，则以最后一个为准（来源：C-7 | `## 补充说明`）。

fallback 的适用前提与关键字段（来源：C-7 | `## fallbacks 配置`、`### FallbackObject`）：**只能用于 TCP + TLS 传输组合**，有子元素时 Inbound TLS 需设 `"alpn":["http/1.1"]`；`name` 匹配 TLS SNI，`alpn` 匹配协商出的 ALPN，`path` 匹配首包 HTTP PATH（不支持 h2c）；`dest` 必填，决定 TLS 解密后 TCP 流量的去向；`xver` 用于发送 PROXY protocol（填 1 或 2）。

> [!warning] 照抄旧模板的版本坑
> `dest` 只填 port（形如 `80`）时通常指向本机明文 HTTP 服务。官方注明：**v25.7.26 之后**，只含 port 的 `dest` 指向 **localhost**，而在此之前指向 `127.0.0.1`——改动后实际目标很可能是 `::1`，于是「监听 `::1` 却只允许 `127` 进入」或额外上 PROXY protocol 的旧 webserver 会表现不同（来源：C-7 | `> dest` 项下的版本注）。**早于该版本的教程与模板都需重新核对**。

## 4.6 源站证书怎么来

要挂在 Cloudflare 代理后并停在 Full (strict)，源站得有能过验证的证书。3x-ui 面板提供了这条路：**用 Cloudflare API 做 DNS 验证**申请证书，因而也适用于**泛域名**与**在 Cloudflare 代理后的服务器**；前置条件是你的域名**已由 Cloudflare 管理**（NS 指向 Cloudflare），并准备一枚 **API Token**（推荐，权限 `Zone:DNS:Edit`）或注册邮箱 + **Global API Key**（来源：C-2 | `### Cloudflare`）。本章只写到「能申请」为止，面板内操作步骤不在此展开。

> [!note] 别把这节当成「套 CDN 的官方教程」
> C-2 里标题为 **Cloudflare** 的那节，讲的只是**用 DNS 验证给源站申请证书**，与「把节点挂在 Cloudflare 代理后」是两回事；它的反代章节也只给 Nginx / Caddy，**完全不涉及 Cloudflare**（来源：C-2 | `## Getting SSL`、`## Reverse Proxy`）。

> [!tip] 大白话
> 把这一章想成「对方肯不肯把货交回给你」的三道门：**端口**是「门牌号在不在允许清单里」，**TLS 模式**是「你出不出示一张合格证件」，**WebSocket** 是「走哪条通道、通道能撑多久」。三道门都过，请求才真正走到你的节点上。

### 本章小结

- Cloudflare 默认代理 13 个 HTTP/HTTPS 端口，其中 10 个可代理但**缓存被禁用**；「只有 80/443 走缓存」是**排除推论**，官方只列了禁用缓存的 10 个（来源：B-3 | `## Network ports compatible with Cloudflare's proxy`、`Ports supported by Cloudflare, but with caching disabled`；02_deep_research.md | §三-3）。
- 免费版要代理列表外端口只有放弃代理一条路——这是「官方只给灰云与 Spectrum」加「全端口 Spectrum 仅企业版」的**合成结论**（来源：B-3 | `## How to enable Cloudflare's proxy for additional ports`；02_deep_research.md | §三-4）。
- TLS 模式同时管两段连接；Full 与 Full (strict) 的分水岭是**源站证书能否自签**，后者要求未过期、受信 CA 或 Origin CA 签发、CN/SAN 匹配（来源：B-4 | 首段、`### Custom SSL/TLS`；B-8 | `## Use when`）。
- WebSocket 在 Cloudflare 侧开箱可用、全套餐支持，但 Xray 官方**建议迁移到 XHTTP**，不能写成「官方推荐方案」；空闲超时与网络代码发布都会断连（来源：D-1 | 首段、`### Idle timeout`、`### Technical note`；C-1 | 页首 DANGER 块）。
- 443 复用有 Xray fallback 与 Nginx / Caddy 两条路；`dest` 只填 port 的指向在 **v25.7.26** 后发生变化，旧模板需重新核对（来源：C-7 | `### FallbackObject`、`> dest`）。

### 下一章预告

到这里配置已经走完。但配完不等于通了，也不等于更快——先分清不通的原因，再谈加速值不值。

> 上一篇：[[03_接入Cloudflare]] ｜ 返回索引：[[00 VPS 自建节点零基础全流程]] ｜ 下一篇：[[05_被墙判定与加速取舍]]
