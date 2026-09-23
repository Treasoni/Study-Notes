<!-- SOURCE: 00_导读.md | 3031 bytes -->
# 导读：节点被墙之后，还有第二条路

节点不通时，最容易想到的动作是「换 IP」；但如果问题不在 IP，换 IP 只是重来一遍。这篇讲另一条路：把节点藏到 CDN 后面，让封锁方「看得见」的目标不再是你服务器的地址（据视频章节推断）。

本篇是**深水区**笔记：前提是你已有能跑通的节点，回答的不是「怎么装面板、怎么建节点」，而是「CDN 凭什么能救被墙节点、代价与边界在哪」。

> [!note] 关于主来源视频
> 主线取自一期视频的章节骨架。该视频**无字幕**：凡涉及口播的判断一律写「据视频章节推断」，可核验事实以 Cloudflare / Xray / 3x-ui 官方文档与一手论文为准（来源：00_intent.md | 主来源）。

## 0.1 三个场景先分清

「不通」至少是三种处境，解法不同：**IP 被墙**——换 IP 或套 CDN 可能有效；**域名被污染**——解析被投毒，查询到不了 Cloudflare，套 CDN 救不了（见第二章 2.5）；**只是配错了**——域名、代理状态、端口、TLS、WS 任一层填错，靠第六章报错码速查。判别这三类**没有官方方法**（来源：02_deep_research.md | §四-缺口 1）。

## 0.2 本篇不做什么

本篇**不**复述装面板、建节点与域名解析的填法——那三段已在面板流展开。

| 维度 | 面板流 | 本篇 |
|---|---|---|
| 主线 | 买 VPS → SSH → 面板 → 建节点 → 带域名与 Cloudflare → 被墙判定与换 IP | CDN 原理与边界 → Cloudflare 侧约束（DNS/端口/TLS/WS）→ 加速取舍 → 排错速查 |
| 重叠处 | 橙云/灰云、可代理记录类型、pending 窗口、非标端口需 Spectrum、换 IP | 不重复，只做速查表 + 链接 |
| 定位 | 零基础一次跑通 | 已完成搭建、想抗封锁 |

（来源：00_intent.md | 差异化定位表。本次不修改面板流。）

> [!note] 内核直配不在此系列
> 手写 Xray JSON、REALITY 原理、nftables / suricata 加固**属官方文档范畴，本系列未成篇**（依据：`[[99 附录 速查表与内容边界]]` 附录 B）。

## 0.3 阅读路线

只有 10 分钟：读第四、六章。想懂原理：加读第一、二章。出问题才查：直接翻第五、六章。

### 本章小结

- 节点被墙的判定无官方方法，本篇只写分类排除的经验方法（来源：02_deep_research.md | §四-缺口 1）。
- 本篇不复述装面板、建节点与域名解析，只补 CDN 原理、约束与排错；视频结论标注「据视频章节推断」（来源：00_intent.md | 主来源）。
- 与面板流的分工见 0.2 分工表，重叠处只做速查与链接（来源：00_intent.md | 差异化定位表）。

### 下一章预告

在讲怎么救之前，先把 CDN 到底是什么讲清楚——否则「套 CDN」会变成一个凭感觉动手的操作。

<!-- END: 00_导读.md -->

<!-- SOURCE: 01_CDN是什么.md | 10484 bytes -->
# 第 1 章 CDN 是什么

「套 CDN」这个动作在教程里常常只有一句话：把域名挂到 Cloudflare，打开小黄云。但如果不先弄清 CDN 到底是什么，这一步就会变成凭感觉动手——你既不知道它替你挡住了什么，也不知道它会在哪里反过来咬你一口。这一章只解决一个问题：CDN 是「帮你加速的缓存网络」，还是「挡在源站前面的反向代理」？

## 1.1 它是什么

CDN（Content Delivery Network，内容分发网络）是**地理分布的一组服务器**，通过把内容缓存在离用户更近的位置来加速分发；缓存对象是加载网页所需的各类资源——HTML 页面、JavaScript 文件、样式表、图片与视频（来源：A-1 | 首段 / `## What is a CDN?`）。官方称如今多数网页流量都经由 CDN 提供，包括 Facebook、Netflix、Amazon 这类大站（来源：A-1 | `## What is a CDN?`）。

这里有一个最常见的误解要先拆掉：**CDN 不托管内容，也不能替代虚拟主机**。官方原话是，CDN 不 host content、不能取代正经的 web hosting，它做的是在网络边缘（network edge）缓存内容从而提升性能（来源：A-1 | `## Is a CDN the same as a web host?`）。你的源站仍是内容的唯一出处，CDN 只是在它前面多放了一层货架。

它凭什么更快？关键在服务器摆在哪里：CDN 把服务器放在**不同网络之间的交换点（IXP）**上，接上这些高速互联点就能降低高速分发中的成本与传输时延（来源：A-1 | `## How does a CDN work?`）。时延的缩短来自四类机制：缩短用户与资源之间的物理距离、负载均衡与 SSD 等软硬件优化、通过压缩与 minify 减小文件体积、以及连接复用与 TLS false start（来源：A-1 | `## Latency`）。

但对我们这个场景而言，比「加速」更要紧的是它的第二个身份：**Cloudflare 是一个反向代理**——它接收客户端请求，再把请求代理回客户的源站服务器，因此**每个请求都要先穿越 Cloudflare 的网络，才到达客户的网络**（来源：A-2 | `## Cloudflare CDN architecture and design`）。正是这一层位置，让第二章的「隐藏真实 IP」成为可能。

## 1.2 一次请求的完整链路

把抽象名词落成一条可跟踪的路径，CDN 就不难懂了。以 AWS 官方文档描述的 CloudFront 为例，用户请求一个对象时依次发生（来源：A-3 | `## How CloudFront delivers content to your users` 步骤 1–3.3）：

1. 用户请求某个对象（例如一张图片或一个 HTML 文件）；
2. **DNS 把请求路由到最能服务该请求的 POP（边缘节点）**，通常就是时延最近的那个；
3. 边缘节点检查自己的缓存——命中就直接返回给用户；
4. 未命中时，边缘节点比对 distribution 里的规格，把请求转发给你的源站；
5. 源站把对象送回边缘节点；
6. **从源站到达的第一个字节开始**，边缘节点就把对象转发给用户，同时把它写入缓存，供下次请求使用。

```
用户 ──①──> 就近边缘节点(POP) ──③命中──> 直接返回
                    │
                    └─④未命中──> 源站 ──⑤──> POP ──⑥──> 用户
                                     （回源响应边转发边写入缓存）
```

在更完整的实现里，回源路径还会分一层：POP 未命中时，通常先去就近的 **regional edge cache**（区域级缓存，容量比单个 POP 大、位于源站与 POP 之间）；那里也没有，才回源到源站；回源取回的对象会同时写入 regional 与 POP 两层，使**同一区域内的各个 POP 共享这份本地缓存**，避免反复打扰源站（来源：A-3 | `###### How regional caches work`）。

## 1.3 带具体值的例子：一条记录，两种答案

「代理状态」这件事，看一条 DNS 查询的结果最直观。Cloudflare 官方文档给的例子是同一个 `example.com` 下的两条记录（来源：B-1 | `### Example`）：

| Type | Name | Content | Proxy status | TTL |
|---|---|---|---|---|
| A | `blog` | `192.0.2.1` | Proxied | Auto |
| A | `shop` | `192.0.2.2` | DNS only | Auto |

对这两条记录分别查询，你会拿到**性质完全不同**的答案：

- 查 `blog.example.com`（橙云）→ 答的是 **Cloudflare 的 anycast IP**（一组共享 IP，用来把流量导向就近的数据中心），**而不是** `192.0.2.1`；请求因此会进入 Cloudflare 的网络并被代理（来源：B-1 | `### Example`）。
- 查 `shop.example.com`（灰云）→ 答的是**真实源站 IP** `192.0.2.2`。这会把源站 IP 暴露给任何查询者，同时 Cloudflare 也无法对这些请求提供 HTTP/HTTPS 分析（来源：B-1 | `### Example`）。

换算成命令行，你看到的就是这两种输出：

```bash
# 橙云记录：答案是 Cloudflare 的 anycast 地址段，看不到 192.0.2.1
$ dig +short blog.example.com
104.16.x.x
172.67.x.x

# 灰云记录：答案是源站真实 IP，一眼可见
$ dig +short shop.example.com
192.0.2.2
```

> [!warning] 这里就是本篇的存在理由
> 对自建节点而言，橙云与灰云的差别不是「快不快」，而是「你的源站 IP 是否直接写在公开 DNS 答案里」。灰云的节点等于把服务器地址挂在门口。

## 1.4 三张对比表

**① 请求怎么被送到 CDN 节点上**，有两种路由方式，差别不小（来源：A-2 | `### Routing requests to CDN nodes`）：

| 维度 | DNS unicast 路由 | Anycast 路由 |
|---|---|---|
| 就近判断依据 | **客户端的 DNS 解析器**，而非客户端 IP | 由 BGP 把流量送到最近且有容量的数据中心 |
| 多节点关系 | 每个节点用独立单播地址 | 多个节点宣告**同一个 IP** |
| 变更生效 | 受 DNS TTL 约束，需等 TTL 过期 | 由路由层面处理 |
| 故障切换 | 不优雅，通常需要新建会话/应用 | 一个节点故障，请求自动转到就近其他节点 |
| 抗流量尖峰 | 单播把流量直接送到特定节点，尖峰时吃紧 | 流量分散到多个数据中心，抗 DDoS 更强 |

**② 缓存命中与回源**，是谁在接你的流量、钱花在哪里（来源：A-2 | `### Impacts`、A-1 | `## Bandwidth expense`）：

| 情形 | 谁响应 | 源站是否被联系 |
|---|---|---|
| 缓存命中 | 边缘节点用缓存副本直接返回 | 否 |
| 未命中 / 内容不可缓存（动态内容） | 回源取回后由边缘节点返回 | **是**，且每次源站响应都消耗一次带宽 |

**③ 哪些请求会绕过中间层缓存**（来源：A-3 | `###### Note`）：

| 请求类型 | 是否经区域级缓存 |
|---|---|
| 可缓存的 GET 请求（未命中时） | 经 regional edge cache 再到源站 |
| 代理类 HTTP 方法（`PUT`/`POST`/`PATCH`/`OPTIONS`/`DELETE`） | **不经**，直接从 POP 到源站 |
| 运行时判定为动态的请求 | **不经**，直接到源站 |

> [!tip] 大白话
> 把 CDN 想成小区门口的便利店：货其实都从远处的大仓库（源站）来，但常买的东西已经预先放在你楼下（边缘节点缓存）——你下楼两步就拿到，不用每次都跑一趟仓库。所以「CDN 加速」本质上是**把货提前搬到离你近的地方**；而一旦要买的是店里没有的东西（缓存未命中、动态内容），还是得回仓库取，只是取货的路线被就近的店长优化过。而「CDN 挡在源站前面」这件事则相当于：所有快递都先送到便利店，再由便利店转交给你——**别人看到的是便利店的地址，看不到仓库在哪**。

## 1.5 顺带说清代价

CDN 不是白拿的。官方文档明确列出使用 CDN 相对自托管静态资源的几项代价（来源：A-4 | `There are also downsides to using CDNs`）：

- **对第三方服务的额外依赖**：CDN 若宕机、**在某地区被封锁**、或被永久关停，你的网站就会故障；
- **多一层攻击面**：攻击者若能攻破 CDN，就可能向你的用户投送恶意内容；
- **与直觉相反，CDN 也可能降低性能**：与第三方站点建立连接意味着更多轮 DNS 查询与内容协商；且现代浏览器出于隐私原因**不在不同源之间共享同一资源的缓存**，同一份资源仍会被反复下载。

注意第一条与 anycast 的关系：某个数据中心整体出问题时，anycast 路由会把流量转到其他可用数据中心（来源：A-1 | `## Reliability and redundancy`）；但如果整个 CDN 在某地区被封或被关停，就没有「其他可用节点」可转了——那是整站故障。

> [!warning] 厂商自述数据要打折看
> Cloudflare 自称其 anycast 网络覆盖全球**数百个城市**、**50 ms 内触达 95%** 的联网人口、网络容量**超过 405 Tbps**；Argo Smart Routing 平均带来 **30%** 的 web 资源性能提升（来源：A-2 | `## Cloudflare CDN architecture and design`、`### Argo Smart Routing`）。这些数字均为 **Cloudflare 自称**，素材中**无第三方核验**，只当量级参考。

### 本章小结

- CDN 是地理分布的服务器群，通过把内容缓存在离用户更近处来加速分发；它**不托管内容、不能替代虚拟主机**（来源：A-1 | 首段、`## Is a CDN the same as a web host?`）。
- 一次请求的链路是：用户 → 就近 POP → 缓存命中直接返回；未命中则回源，**首字节到达即开始向用户转发并写入缓存**（来源：A-3 | 步骤 2–3.3）。
- 请求到节点有 DNS unicast 与 anycast 两条路；anycast 用「同一 IP、多节点宣告」实现就近与故障切换，DNS unicast 则按**客户端 DNS 解析器**而非客户端 IP 判断就近（来源：A-2 | `### Routing requests to CDN nodes`）。
- 代理（橙云）记录的 DNS 答案是 Cloudflare anycast IP，灰云记录答的是源站真实 IP，后者等于公开暴露源站（来源：B-1 | `### Example`）。
- CDN 的代价包括第三方依赖、额外攻击面，以及跨源不共享缓存时可能反而更慢（来源：A-4 | `There are also downsides to using CDNs`）。

### 下一章预告

如果 CDN 只是缓存和加速，它本该与被墙无关。真正让它能救节点的，是它在网络拓扑里的第二个身份。

<!-- END: 01_CDN是什么.md -->

<!-- SOURCE: 02_为什么能救被墙.md | 11508 bytes -->
# 第 2 章 为什么 CDN 能救被墙节点（原理与边界）

上一章我们把 CDN 讲成了「缓存 + 加速」，但缓存与加速本身与被墙无关——纯缓存的 CDN 不会让节点更难封。真正让它能救节点的，是它在网络拓扑里的第二个身份，以及这个身份背后的三层原理。本章要回答：套上 CDN 后，封锁方「看得见」的是什么？这层保护从哪来，又到哪为止？

## 2.1 第一层原理：换脸

最直接的一层是：**你的源站 IP 不再出现在公开的解析答案里**。记录设为代理后，DNS 查询返回的是 Cloudflare 的 anycast IP，而不是源站真实 IP（来源：B-1 | `## Proxied records`、`### Example`）。请求因此先进入 Cloudflare 网络；Cloudflare 作为反向代理再把它代理回源站——**所有请求都要穿越 Cloudflare 网络才到达客户的网络**（来源：A-2 | `## Cloudflare CDN architecture and design`）。封锁方在这一层看到的，是一个 CDN 地址。

只藏 IP 还不够。USENIX Security 2021 关于 domain shadowing 的论文指出，该手法能让连接的**全部「指示器」——连接 URL、TLS 连接的 SNI、HTTP(S) 请求的 Host 头——看起来都属于那个被允许的域名**（来源：A-5 | Abstract）。换句话说，不只「你连的是谁」被换掉了，「你说你要访问谁」也被换掉了——三者同时呈现为同一个被允许的域名，这是该层原理的完整形态。

## 2.2 第二层原理：附带损害

如果只是换脸，封锁方大可以「顺手把你换上的那张脸也封掉」。它没有这么做，是因为这样做要付代价——代价的名字是**附带损害**（collateral damage）。

domain fronting 依赖一个实现细节：许多 CDN **不检查 SNI 与 Host 头的一致性**，只凭 Host 头转发。于是用户可以连到 CDN 边缘、请求一个被允许的域名（front domain），却把 Host 头设成被封锁的域名（来源：D-2 | §2.3）。要封掉它，审查方**必须封掉该 CDN 上所有域名**——否则只要还剩一个被允许的域名，就能当日落域名，让该 CDN 上其他域名重新可用（来源：D-2 | §2.3）。由于 CDN 极为普遍、许多有价值域名也由 CDN 提供，**彻底封锁一个（大型）CDN 对很多审查方而言并不可行**（来源：D-2 | §2.3）。OONI 术语表把这种「依赖审查方不愿造成大面积误伤」的思路称为 **collateral freedom**（来源：C-5 | `Domain fronting`，仅作术语对照）。

**domain shadowing 更难封**：审查方若认定封锁某个域至关重要，仍可整段封掉承载它的那个 CDN；而 domain shadowing 下，要封锁一个域，审查方**必须封掉所有允许该手法的 CDN**（来源：D-2 | §6.1.3 IP Blocking）。且**封掉某一个 CDN 也不禁用该手法**——用户可以换到其他仍允许它的 CDN（来源：D-2 | §6.3.3）。

这套机制之所以成立，还因为 CDN 很难「把后门关掉」：设置任意后端域是它的合法能力，如同 DNS 的 CNAME 可让一个域名指向任意另一个域名；网站把客服外包给第三方（子域 CNAME 指向 `example.zendesk.com`）正靠这个能力运作（来源：D-2 | §6.2.1）。**附带损害不是审查方的善意，而是 CDN 自身业务决定的成本**。

## 2.3 第三层原理：被动检测下的 CDN AS

前两层讲的是「看不见你」。第三层是另一回事：**即使审查方在检测「全加密流量」，大型 CDN 的地址段也不在受影响之列**。

结论出自 GFW Report 的 USENIX Security 2023 论文：GFW 自 **2021 年 11 月**起部署了一套新机制，**对「全加密流量」做纯被动的实时检测与封锁**，影响 Shadowsocks、VMess、Obfs4 等协议（来源：A-6 | Abstract；§1）。作者**推断**其做法是：不正面定义「全加密流量」，而是先用**至少五条粗粒度豁免规则**放过「不像全加密」的流量，其余一律封锁（来源：A-6 | §4 Algorithm 1）：

| 规则 | 内容（面向客户端发出的首个 TCP 载荷） |
|---|---|
| Ex1 | 置位比特比例 ≤ 3.4 或 ≥ 4.6 |
| Ex2 | 前 6 个（或更多）字节落在 `[0x20,0x7e]`（可打印 ASCII） |
| Ex3 | 超过 50% 的字节落在 `[0x20,0x7e]` |
| Ex4 | 超过 20 个连续字节落在 `[0x20,0x7e]` |
| Ex5 | 匹配 TLS 或 HTTP 的协议指纹 |

其中 TLS 的豁免依赖头 3 字节匹配 `[\x16-\x17]\x03[\x00-\x09]`；HTTP 的豁免依赖「方法名 + 一个空格」，**大小写不敏感，但把方法名拼错就不再豁免**（来源：A-6 | §4.3）。另需注意：中文（UTF-8 与 GBK）字符**不享受任何豁免**（来源：A-6 | §4.2）。

被判定后的处置方式也很具体（来源：A-6 | §4.4、§6.3）：

- **只丢「客户端 → 服务器」方向的包**，反向不受影响；该机制**仅作用于 TCP**，UDP 不触发；
- 封锁可发生在 **1–65535 全部端口**，换非标准端口并不能规避；
- 触发后同一 3 元组（客户端 IP、服务器 IP、服务器端口）被**残余封锁 120 或 180 秒**，计时器不因后续发包而重置；
- 封锁是**概率性**的，单连接被封锁概率约 **26.3%**。

哪些地址段会被检测？论文在 **2022 年 5 月**做过一次 10% IPv4 扫描（**仅 TCP 80**）：5.5 百万 IP 中 **98% 不受影响**；受影响的 AS **都是向个人出售 VPS 的供应商**（Alibaba US、Constant，及 Amazon / Digital Ocean / Linode 的部分前缀），而 **Akamai、Cloudflare 这类大型 CDN 的 AS 不在其中**（来源：A-6 | §6.2 Figure 4 说明段）。

> [!warning] 这条结论的语境极窄，必须连着限定一起读
> 「CDN AS 不在受影响之列」**严格限于「全加密流量被动检测」这一个机制**，且出自 **2022 年 5 月、仅 port 80** 的一次扫描，观察窗口为 **2021-11 ~ 2023-02**。它**不能**推出「CDN 对其它封锁手段免疫」，也**不能**推出「CDN 是当局的有意豁免」。任何 2026 年现状陈述都不由该论文支撑（来源：A-6 | Abstract、§6.2；02_deep_research.md | §三-12）。

## 2.4 三层原理各自拦住了什么

| 原理层 | 它挡住什么 | 它挡不住什么 |
|---|---|---|
| 第一层：换脸（藏源站 IP 与域名指向） | 直连 / 扫描源站 IP 的封锁与暴露 | 域名被污染的路径（解析到不了 CDN） |
| 第二层：附带损害（封一个域要连坐整个 CDN） | 「顺手封掉你的域名」这种低成本做法 | 审查方愿承受附带损害时的整段封锁；CDN 主动废除该特性 |
| 第三层：被动检测豁免（CDN AS 不在受影响之列） | 「全加密流量被动检测」这一种机制下的封禁 | 其它封锁手段；该机制本身的后续扩展（作者判断其属临时性） |

## 2.5 边界清单：CDN 救不了什么

前面三层每一层都有反例；看清它们，才知道什么时候该转向别的手段。

**（一）换脸救不了域名被污染。** 第一层原理的前提是「解析能正常走到 Cloudflare」。若封锁发生在解析这一层——查询被投毒、返回伪造答案——请求**根本到不了 Cloudflare**，源站 IP 藏得多好都没有意义。把你暴露在外的不是 IP，而是那串域名；换脸救不了门牌号被改的问题。

**（二）附带损害不是承诺，是可撤销的商业选择。** 第二层原理成立，靠的是审查方「不愿扩大伤害」与 CDN「不愿关掉合法功能」两件事同时成立。但后者会变：论文记录了 domain fronting 的兴衰——**近两年间许多 CDN（如 Google Cloud CDN、Amazon CloudFront）意识到该手法并开始废止它，手段是强制 SNI 与 Host 头一致**，迫使不少规避系统停服或转向更小、封锁成本更低的 CDN（来源：D-2 | §2.3）。论文亦直言：domain shadowing 一旦被公开，很可能遭遇同样命运——**CDN 提供商可能迫于压力禁用它**（来源：D-2 | §6.2）。这层保护依赖商业与政治权衡，不是技术上不可关闭。

**（三）第三层结论有时间与口径双重限定。** 「CDN AS 不在受影响之列」只在**全加密流量被动检测**这一机制、**2021-11 ~ 2023-02** 观察窗口内成立，依据是 **2022 年 5 月、仅 port 80** 的扫描；作者判断该机制属「临时性」，随时可扩展（来源：A-6 | §4.4、§6.2）。读成「CDN 对封锁免疫」是明确的外推错误。

**（四）CDN 自身被整段封锁时，方案整体失效。** 一旦审查方认为封掉该 CDN 的收益大于代价（CDN 越小代价越低），整段封锁就会发生；届时藏在后面的所有东西一起不通。同样，**CDN 片区故障也会造成整站故障**（来源：A-4 | `There are also downsides to using CDNs`）。

**（五）方案不可用时的退路。** 撞上任一条边界——尤其「域名被污染」这类换脸救不了的情形——下一步不是继续在 CDN 上折腾，而是回到「分层排除 + 换 IP」路径。完整操作已写在面板流 `[[09 节点被墙的判定与换 IP（分厂商分操作）]]`，本篇不重复；只需记住：**CDN 是备选路线，不是唯一路线，也不是在所有被墙形态下都成立。**

> [!tip] 大白话
> 把第二层原理想成「用大商场当收货地址」：想拦你，就得连整个商场一起封——可商场里还有几百家店在营业，封了会把所有人得罪。domain fronting 用的是商场「不看收件人和招牌是否一致」这个漏洞，domain shadowing 用的是「允许你填任意收货方」这项正经业务。
> 边界也在这个比方里：**商场会被施压**（它可以自己改规矩，正如 Google Cloud CDN 们废止了 domain fronting）；**铁了心连商场一起封，你的包裹也被拦**（即「CDN 被整段封锁」）。第三层则只是「商场这个地址段不在这台检测仪的扫描名单里」，**不是「能躲开所有检查」**。

### 本章小结

- 第一层「换脸」：代理记录的 DNS 答案不含源站 IP，且连接 URL、TLS SNI、HTTP(S) Host 对外全呈现为同一被允许域名（来源：B-1 | `## Proxied records`；A-5 | Abstract）。
- 第二层「附带损害」：封一个域要连坐整个 CDN 上所有域名，故审查方顾虑代价；domain shadowing 需连坐**所有**允许该手法的 CDN，更难封（来源：D-2 | §2.3、§6.1.3、§6.3.3）。
- 第三层「被动检测豁免」：GFW 全加密流量被动检测下，**Akamai、Cloudflare 这类大型 CDN AS 不在 2022-05、仅 port 80 扫描的受影响之列**；该结论仅限此机制、观察窗口 2021-11 ~ 2023-02，不能外推为「CDN 免疫」或「有意豁免」（来源：A-6 | §6.2、Abstract、§4.4；02_deep_research.md | §三-12）。
- 边界清单：域名被污染救不了；附带损害是可被厂商撤销的商业选择（domain fronting 已被强制 SNI=Host 关停）；CDN 被整段封锁或片区故障时方案整体失效；退路是面板流第 9 章的分层排除与换 IP（来源：D-2 | §2.3、§6.2；A-4 | `There are also downsides to using CDNs`）。

### 下一章预告

原理成立的前提是：你的域名真的由 Cloudflare 接管。这一步的坑，比想象中多。

<!-- END: 02_为什么能救被墙.md -->

<!-- SOURCE: 03_接入Cloudflare.md | 5970 bytes -->
# 第 3 章 接入 Cloudflare 与域名解析

第二章的原理都压在一个前提上：**你的域名真的由 Cloudflare 接管**。这一步的坑比想象中多。本章不讲填法（见面板流 `[[07 搭建节点（带域名与 Cloudflare）]]`），只补三件事：**套餐门槛、接入期行为、怎么验证生效**。

## 3.1 免费版只有一条路

Cloudflare 有四种 zone 接法，对免费用户开放的只有一种（来源：B-5 | `DNS setups`、`Common use cases and availability`；B-6、B-7 | `Availability`）：

| DNS setup | 门槛 | 解决什么 |
|---|---|---|
| Primary (Full) | **Free 起全套餐** | Cloudflare 作主权威 DNS，记录全托管在此 |
| CNAME (Partial) | **Business 起** | 保留原权威 DNS，只把个别子域交它反代 |
| Zone transfers | **仅 Enterprise** | 与另一家 DNS 并用，记录以 AXFR / IXFR 互传 |
| Subdomain setup | **仅 Enterprise** | 被委派子域的设置独立成另一个 zone |

所以结论很干脆：**改 NS，把整个 zone 交给 Cloudflare**。Cloudflare 自持顶级域（TLD）名称服务器，NS 切过去后解析直接落到它自己，**省去若干中间步骤**（来源：D-2 | §3.2）；另有差别：DNS 基础设施的 DDoS 防护只覆盖 full setup（来源：B-7 | `DDoS protection`）。但**官方在这一步没有 NS 接入的操作细则**，只有 setup 定义与可用性数据，改 NS / 加记录属面板流第 7 章（来源：B-5 | `DNS setups`）。

还有个歧义：**`CNAME flattening` 指两回事**——Cloudflare 侧指被代理 CNAME **默认被展平**、返回 anycast 地址（来源：B-1 | `### CNAME records`）；权威 DNS 侧指「把 apex 的 CNAME 展平」的能力，CNAME (partial) 下**只有支持它才能把 apex 代理到 Cloudflare**（来源：B-7 | `CNAME flattening`）。

## 3.2 速查表：代理状态与记录类型

> **以下已在面板流第 7 章展开，此处仅速查**（详见 `[[07 搭建节点（带域名与 Cloudflare）]]`）。

| 项目 | 结论 | 来源 |
|---|---|---|
| 橙云（Proxied） | DNS 答 anycast IP；HTTP/HTTPS 经 Cloudflare，套用 DDoS 防护、缓存与 WAF 规则 | B-1 \| `### Benefits` |
| 灰云（DNS only） | 答**源站真实 IP**，暴露源站 | B-1 \| `## DNS-only records` |
| 哪些记录能被代理 | **仅承载 HTTP/HTTPS 的 A / AAAA / CNAME**（B-2 严口径；B-1 宽口径并列，**以 B-2 为准**） | B-2 \| `## Proxy eligibility`；B-1 |
| 同名多条 A/AAAA | 一条橙云，**整组按橙云处理** | B-1 \| `### Mix proxied and unproxied` |
| CNAME 链 | 链上任一主机名被代理，请求即被代理 | B-1 \| `### Mix proxied and unproxied` |
| 被代理 CNAME | 默认展平，返回 Cloudflare anycast IP | B-1 \| `### CNAME records` |
| 代理记录 TTL | 固定 **Auto = 300 秒**，不可修改 | B-1 \| `### Predefined time to live` |
| 接入期（pending） | 先按灰云处理、**返回源站 IP**；激活后建议**轮换源站 IP** | B-2 \| `## Pending domains` |

## 3.3 接入期与 zone 状态

zone 添加后先进入 **pending** 验证所有权，**最长约 24 小时**；期间**即使记录已设为橙云，也按灰云处理、返回源站 IP**——这段窗口会暴露源站，故官方建议**激活后轮换源站 IP**（来源：B-2 | `## Pending domains`）。zone 状态（来源：B-5 | `## Zone status`）：

| 状态 | 含义 |
|---|---|
| Initializing / Pending | 初始化 / 待验证所有权 |
| Active | 已激活，可代理 |
| Moved / Deleted / Purged | 已迁出 / 已删除 / 已清除 |

## 3.4 解析是否生效怎么验

验证只看一件事：**同一条记录查出来的答案属于哪一边**（来源：B-1 | `### Example`）：

```bash
# 橙云：答案应落在 Cloudflare 地址段
$ dig +short your-domain.example
104.16.x.x
172.67.x.x

# 灰云：直接返回源站真实 IP
$ dig +short your-domain.example
203.0.113.7
```

答案是 Cloudflare 地址段，说明「解析已到 Cloudflare」，正是第四章要接的那一半；若仍是源站 IP，先看 zone 是否还在 pending。

> [!note] `dig` 与在线 DNS 检查是**通用工具**，非本文素材来源
> 地址段形态出自官方 `### Example`；命令本身**无官方锚点**。

## 3.5 域名前置只做指路

本章默认你**已有域名、能改 NS**；若还没有，本系列「低价域名获取」「托管与解析域名」两期更细。

## 3.6 大白话

> [!tip] 大白话
> 把 DNS 想成「门牌登记处」：**NS 接入 = 把整个登记处交给 Cloudflare 管**，门牌都由它发；**CNAME 接入 = 只在自己门口挂块转接牌**指向它那台机器——但要 Business 起，且登记处得能「把转接牌挂到楼顶（apex）」，多数人用不了。

### 本章小结

- Free / Pro 只有 primary (full)；CNAME (partial) 要 Business 起，zone transfers 与 subdomain setup 仅 Enterprise（来源：B-5 | `Common use cases and availability`；B-6、B-7 | `Availability`）。
- 官方在此只给定义与可用性，**没有 NS 接入的操作细则**；填法见面板流 `[[07 搭建节点（带域名与 Cloudflare）]]`（来源：B-5 | `DNS setups`）。
- 可代理记录采用 B-2 严口径「仅承载 HTTP/HTTPS 的 A/AAAA/CNAME」，B-1 宽口径仅并列参考（来源：B-2 | `## Proxy eligibility`；B-1）。
- 接入期（pending，最长 24h）记录按灰云处理并返回源站 IP（来源：B-2 | `## Pending domains`）。
- `CNAME flattening` 一词两义：Cloudflare 侧默认展平被代理 CNAME；权威 DNS 侧需具该能力才能代理 apex（来源：B-1 | `### CNAME records`；B-7 | `CNAME flattening`）。

### 下一章预告

域名侧通了，只解决了「请求能到 Cloudflare」。还差一半——Cloudflare 能不能顺利把请求交回你的源站。

<!-- END: 03_接入Cloudflare.md -->

<!-- SOURCE: 04_套上CDN.md | 12337 bytes -->
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

<!-- END: 04_套上CDN.md -->

<!-- SOURCE: 05_被墙判定与加速取舍.md | 6833 bytes -->
# 第 5 章 被墙判定与加速取舍

配完 CDN 要分清两件事："不通"坏在哪一层，"套了 CDN"更快还是更慢——两者都没有可直接照搬的官方结论。

## 5.1 分类依据（经验方法；Xray / 3x-ui / Cloudflare 三家官方均无此内容）

口径先写：**节点被墙的判定方法，Cloudflare / Xray / 3x-ui 三家官方文档均无此内容，本节所写是经验方法**（来源：02_deep_research.md | §四 ⛔ 表，缺口 1）。本节给的也不是"判定流程"，而是一套**分类依据**。OONI 把网络干扰分为三类可测量形态（来源：C-5 | 词条总览）：

| 形态 | 定义 | 可观察表现 |
|---|---|---|
| TCP/IP blocking | 阻止客户端与目标建立 TCP 连接——让目标 IP 不可达，或**注入 TCP RST 包**重置该 `IP:Port`（来源：C-5 \| `### TCP/IP blocking`） | 连不上；或刚连上就被重置 |
| DNS tampering | **DNS 劫持与 DNS 欺骗的总称**，表现为查询返回错误 IP（来源：C-5 \| `### DNS tampering`） | 解析出的地址不对 |
| HTTP blocking | HTTP 层干扰总称：投放 block page，或 HTTP failure（被透明代理拦截、连接被重置、明文连接被劫持重定向）（来源：C-5 \| `### HTTP blocking`） | 能连上，却收到"不许访问"页 |

DNS tampering 再分两种，区别在**伪造发生在哪里**：**hijacking** 是**被查询的 resolver 不诚实**，**spoofing** 是**查询在链路上被拦截并注入伪造应答**（来源：C-5 | `### DNS hijacking`、`### DNS spoofing`）。

> [!warning] 这是分类依据，不是判定手册
> OONI 三分法面向**网站审查测量**，**不含**"节点被封"这一类，也没给可用的命令与阈值；措辞是 **potential / anomaly**，只有检测到 block page 才"自动确认"（来源：C-5 | `### Block page`）。它靠**与未审查网络对照**判定（来源：C-5 | `### Network anomaly`），结论绑定测量点（网络 + 国家，来源：C-5 | `### Vantage point`）；整片断网时 OONI 自认**超出其能力范围**（来源：C-5 | `### Internet blackout`）。

## 5.2 分层排除已见面板流第 9 章

用 `ping` / `nc` / `traceroute` 分层排除的**完整路径**已见面板流第 9 章，本篇不重复：`[[09 节点被墙的判定与换 IP（分厂商分操作）]]`。

## 5.3 anomaly ≠ 审查：四种 false positive

看到"异常"不等于被审查。OONI 列出四类 false positive 成因（下四行均来源：C-5 | `### False positive`）：

| 成因 | 一句话解释 |
|---|---|
| 瞬时网络故障 | 网络不稳本身会让 TCP 掉线，看起来像 TCP/IP 干扰 |
| 源站自身不可靠 | 源站服务器出问题同样让测试失败，尽管没被干扰 |
| resolver 按地理就近返回 | resolver 返回离你**地理最近**的 IP，与对照点不同，被误判为 DNS tampering |
| 网站按国家返回不同内容 | 网站按访问者所在国给不同内容，被误判为 HTTP 干扰 |

前两类尤其重要：**源站挂了**与**你被墙了**，客户端看来都是"连不上"。OONI 说明见 <https://ooni.org/support/glossary/#false-positive>。

## 5.4 一个易被误读的现象：端口"开放"

非 80/443 端口自查时，Netcat 与安全扫描器可能把某些非标准端口报成"开放"。官方解释：源于 **anycast 网络特性**，这些端口对其他客户的流量也开放，**是 anycast 共享的副作用，不是你的服务暴露**（来源：B-3 | `## How to block traffic on additional ports` 末段）。

## 5.5 加速取舍（只做定性）

CDN 不是"必然更快"，以下机制各有官方锚点，但**本篇不给任何百分比**（来源：02_deep_research.md | §四 ⛔ 表，缺口 2）。

| 更快 | 机制 | 更慢 | 机制 |
|---|---|---|---|
| 物理距离缩短 | 连到地理更近的数据中心（来源：A-1 \| `## Latency`） | 回源链路更长 | 未命中时走 POP → regional edge cache → 源站，多一跳（来源：A-3 \| `###### How regional caches work`） |
| 连接复用与 TLS false start | 降低握手开销（来源：A-1 \| `## Latency`） | 请求不经缓存 | 代理类方法（PUT/POST/PATCH/OPTIONS/DELETE）与动态请求**直接回源**（来源：A-3 \| `###### Note`） |
| 命中缓存 | 边缘节点直接返回，不回源（来源：A-3 \| `## How CloudFront delivers content to your users` 步骤 3） | 跨源不共享缓存 | 浏览器出于隐私不在跨源间共享缓存，同一资源可能重复下载（来源：A-4 \| `There are also downsides to using CDNs`） |
| 就近接入 | DNS 路由到"最能服务该请求"的 POP（来源：A-3 \| 同节步骤 2） | 就近判断依据错位 | DNS unicast 路由按**客户端 DNS 解析器**（非客户端 IP）判断，你与解析器分散时命中的节点未必近（来源：A-2 \| `### Routing requests to CDN nodes → DNS unicast routing`） |

另两处边界：源站只在未命中或内容不可缓存时才被联系（来源：A-2 | `### Impacts`）；Cloudflare 计量 WebSocket 时**只把初始升级请求算作一个 HTTP 请求**、带宽按 **Cloudflare → 客户端**方向计（来源：D-1 | `## Requests and Bandwidth measurement`）——两项计量口径并不等同（**推论**）。

## 5.6 大白话

> [!tip] 大白话
> 这章干一件事：**先分清"是路断了，还是门牌号被改了，还是你把地址写错了"**。TCP/IP blocking 是"路断了"；DNS tampering 是"门牌号被改了"；false positive 的四类里，藏着的正是"地址本来就抄错"。分清这三类，才知道该查链路、查解析，还是先怀疑自己。

### 本章小结

- 节点被墙判定**无官方方法**；OONI 三分法只作分类依据，面向网站审查测量、不含"节点被封"类别，措辞为 potential / anomaly（来源：C-5 | `### TCP/IP blocking`、`### Network anomaly`；02_deep_research.md | §三-11）。
- 三类形态的界线在"伪造发生在哪里"：hijacking 在 resolver、spoofing 在链路（来源：C-5 | `### DNS hijacking`、`### DNS spoofing`）。
- anomaly ≠ 审查；四类 false positive 中，瞬时网络故障与源站自身不可靠最容易被误当成"被墙"（来源：C-5 | `### False positive`）。
- 加速只能定性：物理距离、连接复用、命中缓存、就近接入为增益；回源更长、不经缓存、跨源不共享缓存、就近按解析器判断为退化（来源：A-1 | `## Latency`；A-3 | `###### How regional caches work`；A-4 | `There are also downsides to using CDNs`）。

### 下一章预告

分类排除能告诉你"大概坏在哪一层"；具体是哪一个错，还要看 Cloudflare 的报错码。

<!-- END: 05_被墙判定与加速取舍.md -->

<!-- SOURCE: 06_排错速查.md | 8048 bytes -->
# 第 6 章 排错速查

报错码对上了，接下来按什么顺序查？这一章把 Cloudflare 侧最常见的几个报错整理成速查表，再把每个码的并列成因摊开。先说清一件事：**官方不给排查顺序**，本章的"次序"是本笔记组织的建议。

## 6.1 先立前提：没有官方排查顺序

Cloudflare 官方对 525、526 都只给**并列**成因列表（526 明标为并列的证书核对项），**没有**"先查证书、再查端口、再查 cipher"这种官方次序（来源：C-3 | `### Resolution`；C-6 | `#### Resolution`；02_deep_research.md | §三-6）。因此**本章"建议排查次序"列是本笔记为方便动手而排，不是官方口径**。

## 6.2 525：Cloudflare 到源站的 SSL 握手失败

525 表示 Cloudflare 与源站之间的 **SSL 握手失败**（来源：C-3 | `### Error 525: SSL handshake failed`）。它成立需**同时**满足两条：握手失败 + 在 SSL/TLS 的 Overview 里设为 **Full 或 Full (Strict)**（来源：C-3 | `### Common causes`）。源站侧的并列成因有四个：未安装有效证书、443（或自定义安全端口）未开放、不支持 SNI、双方 cipher suites 不匹配（来源：C-3 | `### Resolution`）。

可用 **Origin Analytics** 的 **Origin status codes** 图看 `originResponseStatus` 为 `0` 的时段——表示未从源站收到 HTTP 响应，可指示 TLS 协商失败；再按时间戳对照源站 SSL 日志（来源：C-3 | `### Diagnose with Origin Analytics`）。

## 6.3 526：源站证书验不过

526 表示 Cloudflare **无法验证源站 SSL 证书**（来源：C-6 | `### Error 526: invalid SSL certificate`）。成立需**同时**满足：无法校验源站证书 + 设为 **Full SSL (Strict)**（来源：C-6 | `### Common causes`）。核对项为**并列 7 项**，无优先级：

| # | 核对项 |
|---|---|
| 1 | 证书未过期 |
| 2 | 证书未被吊销 |
| 3 | 由 CA 签发（非自签名） |
| 4 | 请求 / 目标域名在证书的 **Common Name 或 SAN** 中 |
| 5 | 证书链完整——源站须一并提供叶子证书与所需中间 CA 证书 |
| 6 | 源站接受 443 端口的连接 |
| 7 | 临时 pause Cloudflare 后，用外部 SSL checker 独立验证 |

（7 项均来源：C-6 | `#### Resolution`。）

官方**绕行**（原文称 workaround）是把 SSL 从 Full (strict) 改回 **Full**；两条**修复**路径：把自签名证书加入 **Custom Origin Trust Store**，或源站改用 **Cloudflare Origin CA 证书**（来源：C-6 | `#### Resolution`）。

## 6.4 525 与 526 是互斥成因，不是同一故障的两个阶段

> [!warning] 别把 525、526 当成先后两步
> 两码成立条件**不重叠**：**525 需 Full 或 Full (Strict)**，**526 仅需 Full (Strict)**；二者是**互斥成因**，不是同一故障的两个阶段，文档也**未说明**同一请求是否会先失败于 526 再显示为 525（来源：C-3 | `### Common causes`；C-6 | `### Common causes`；02_deep_research.md | §三-5）。

## 6.5 413：请求体积超限

413 表示客户端发送的负载超出服务器可接受上限（来源：C-4 | `## 413 Payload Too Large`）。Cloudflare 侧的**分套餐上传上限**如下：

| 套餐 | Free | Pro | Business | Enterprise |
|---|---|---|---|---|
| Max upload size | 100 MB | 100 MB | 200 MB | 最高 5 GB |

（来源：C-4 | `### Cloudflare-specific information`。）可在 zone 的 **Network** 页调 **Maximum Upload Size**；Enterprise 可自助设到 5 GB 以内，超过需联系账户团队（来源：C-4 | 同锚点）。官方给的三条绕行：**把请求拆成更小的块**、**把 DNS 记录改为 DNS-only**、**升级套餐**（来源：C-4 | 同锚点）。

> [!warning] 对套 CDN 的节点，"改灰云"等于取消方案
> 第二条绕行对你几乎不可用：把记录改回 DNS-only，就等于放弃 CDN 代理、直接暴露源站 IP，对以 CDN 前置为存在理由的节点而言即**取消方案本身**（来源：C-4 | 同锚点；02_deep_research.md | §三-4）。另外官方同页内对"API 上传"与"zone 全局上传"未作区分，Free = 100 MB 的适用对象在本页无法判定（来源：02_deep_research.md | §三-7）。

## 6.6 524 与请求响应体积 / 超时

Cloudflare 对 Cloudflare→源站设有默认 **Proxy Read Timeout**；源站未在时限内返回 HTTP 响应就返回 **524**，仅 Enterprise 可调高（来源：B-1 | `### Connection timeouts`）。被代理请求还受**按套餐分级**的请求/响应体积上限约束，且代理状态下无法绕过（来源：B-1 | `### Request and response size limits`）。

## 6.7 WebSocket 连接类问题

- 用 **`wscat`** 等客户端工具在**单个 URL** 上复现，便于收窄范围（来源：D-1 | `### Troubleshooting`）。
- 请求日志里的 **`EdgeStartTimestamp` / `EdgeStopTimestamp`** 表示 **WebSocket 连接的时长**（**不是**初始 HTTP 连接的时长）（来源：D-1 | `### Troubleshooting`）。
- **空闲超时**：双向都无数据传输时 Cloudflare 会关闭连接；Enterprise 可定制超时，通用做法是实现**客户端心跳（ping/pong）**（来源：D-1 | `### Idle timeout`）。
- Cloudflare 发布新代码时**可能重启服务器、终止 WS 连接**（来源：D-1 | `### Technical note`）。

## 6.8 一张速查表

| 症状 | 官方并列成因 | 依据锚点 | 本笔记建议的排查次序（非官方） |
|---|---|---|---|
| 525 | 证书无效 / 443 未开 / 无 SNI / cipher 不匹配 | C-3 `### Resolution` | 先确认模式是否 Full 或 Full (Strict)，再查源站证书，最后核对 cipher |
| 526 | 证书 7 项核对 | C-6 `#### Resolution` | 先逐条过 7 项，再用外部 SSL checker 验证 |
| 413 | 请求体积超上限 | C-4 `### Cloudflare-specific information` | 先看体积是否撞套餐上限，再决定拆块或升级 |
| 524 | 源站超时未响应 | B-1 `### Connection timeouts` | 先查源站是否卡死，再看是否需要调超时 |
| WS 断连 | 空闲超时 / 网络代码发布重启 | D-1 `### Idle timeout`、`### Technical note` | 先加客户端心跳，再排除发布窗口 |

（"次序"列是本笔记的**经验建议**；成因列均来自对应来源。端口是否在可代理清单内，回查第四章 4.1（来源：B-3 | `## Network ports compatible with Cloudflare's proxy`）。）

## 6.9 收尾：全查完还是不通怎么办

若按上表查完仍不通，回到第五章做**分类排除**，它至少能告诉你"大概坏在哪一层"。若归因指向"CDN 方案在当前环境不适用"（如解析到不了 Cloudflare、CDN 被整段封锁），就该考虑退路，而非在报错码里打转（来源：02_deep_research.md | §五 实践指引 8）。

### 本章小结

- 官方对 525 / 526 只给**并列**成因，无排查顺序；本章速查表"次序"列是笔记建议（来源：C-3 | `### Resolution`；C-6 | `#### Resolution`；02_deep_research.md | §三-6）。
- **525** = Cloudflare↔源站握手失败，需 Full 或 Full (Strict)；可用 Origin Analytics 的 `originResponseStatus = 0` 辅助定位（来源：C-3 | `### Common causes`、`### Diagnose with Origin Analytics`）。
- **526** = 源站证书验不过，仅需 Full (Strict)；7 项核对并列，绕行是改 Full，修复是 Custom Origin Trust Store 或 Origin CA（来源：C-6 | `### Common causes`、`#### Resolution`）。
- 525 与 526 是**互斥成因**、不是同一故障的两个阶段（来源：02_deep_research.md | §三-5）。
- **413** 上限按套餐：Free/Pro 100 MB、Business 200 MB、Enterprise 最高 5 GB；三条绕行里"改 DNS-only"对套 CDN 节点等于自毁（来源：C-4 | `### Cloudflare-specific information`）。

### 收束

请记住最要紧的边界——**CDN 救不了被污染的域名，也挡不住整段封锁；它给你的是"换一张脸"与"多一条退路"，而非一劳永逸的免疫**。

<!-- END: 06_排错速查.md -->
