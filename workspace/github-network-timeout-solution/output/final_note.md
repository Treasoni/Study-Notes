---
title: "GitHub 国内网络连接超时解决方案"
tags:
  - github
  - 网络
  - 代理
  - 镜像
  - GFW
created: 2026-08-29
updated: 2026-08-29
status: 已完成
source_project: github-network-timeout-solution
---

# GitHub 国内网络连接超时解决方案

这是一篇实战向的排障笔记，面向会用 git / 命令行、懂基本网络概念，并遇到过「agent 或工具从大陆网络拉取 GitHub 包超时」的开发者。全文按「现象与诊断 → 根因原理 → 三种解决方案（代理 / 国内镜像 / hosts·gh-proxy）→ Agent 场景落地 → 决策速查表」共七章组织：先学会把超时定位到具体环节，再理解 GFW 的干扰原理，随后逐工具配置代理或国内镜像，最后落到 agent 场景并汇总为一张可随时回查的速查表。

## 目录

1. [第 1 章：现象与诊断 — 先确定超时发生在哪一环](#第-1-章现象与诊断--先确定超时发生在哪一环)
2. [第 2 章：根因 — GFW 如何干扰大陆访问 GitHub](#第-2-章根因-gfw-如何干扰大陆访问-github)
3. [第 3 章：方案一 — 走代理：环境变量与各工具配置](#第-3-章方案一-走代理环境变量与各工具配置)
4. [第 4 章：方案二 — 国内镜像加速](#第-4-章方案二-国内镜像加速)
5. [第 5 章：方案三 — hosts 与 gh-proxy 工具](#第-5-章方案三-hosts-与-gh-proxy-工具)
6. [第 6 章：Agent 场景落地 — 给拉包工具配好网络](#第-6-章agent-场景落地-给拉包工具配好网络)
7. [第 7 章：决策速查表与常见坑](#第-7-章决策速查表与常见坑)

---

# 第 1 章：现象与诊断 — 先确定超时发生在哪一环

本篇笔记按「现象与诊断 → 根因原理 → 代理 → 国内镜像 → hosts/gh-proxy → Agent 场景 → 决策速查」七章组织。本章解决最前置的问题：当 Git 克隆或拉取 GitHub 包超时，到底卡在哪一环？不先把环节定位准，后面用代理、镜像还是改 hosts 都会变成瞎猜。

## 1.1 先排除 GitHub 自身故障

动手排查前，先花 10 秒看一眼 GitHub 官方状态页 [^c1-1]。大陆用户遇到的超时绝大多数是「本地/跨境路径」问题，而不是 GitHub 挂了，但官方故障确实存在：

- Git Operations 最近 90 天可用性为 100%（截至 2026-08-29）。
- 2026-08 出现过两类官方故障：一是 SSH Git 短时降级（仅影响 SSH，约 4 分钟）；二是 codeload/archive 下载错误率约 50% 的全网故障。

判断要点：如果状态页显示全绿而你依然连不上，问题基本出在「本地到跨境」这一段——这正是本书后面所有章节要解决的。

## 1.2 用 git 追踪命令定位卡点

Git 自带一套开箱即用的追踪开关，不需要装任何额外工具，最常用的是这两档：

```bash
# 一般跟踪：看到 git 正在做什么
GIT_TRACE=1 git fetch <仓库地址>

# curl 级完整转储：看到与服务器交换的每一行（等价 curl --trace-ascii）
GIT_TRACE_CURL=1 git fetch <仓库地址>
```

`GIT_TRACE_CURL=1` 会打出完整的 HTTP 层对话，包括 `Connected to github.com port 443`、`SSL connection using TLS1.3`、`> GET /...`、`< HTTP/2 200` 这类行。看它卡在哪一行：

- 一直停在域名解析、连不上端口 → TCP 层问题；
- 停在 `SSL connection` 之后 → TLS 握手或数据传输问题。

默认会对 Cookie、Authorization、Proxy-Authorization 打码，避免日志泄露凭据；确需明文时才用 `GIT_TRACE_REDACT=false` 关闭。其余开关按需选用（均出自 Git 官方手册 [^c1-2]）：

```bash
GIT_TRACE_CURL_NO_DATA=1 git fetch <仓库地址>  # 只看信息行与响应头，不看包体
GIT_TRACE_PACKET=1 git fetch <仓库地址>        # packet 级，排查对象协商/协议问题
GIT_TRACE2=1 git fetch <仓库地址>              # trace2 文本输出（另有 _EVENT/_PERF 变体）
```

注意：旧名 `GIT_CURL_VERBOSE` 已被 `GIT_TRACE_CURL` 取代，看到老教程用旧名，换新的即可。

## 1.3 症状分层：三类典型表现

大陆访问 GitHub 失败，绝大多数逃不出下面三类 [^c1-4]：

| 症状 | 典型成因 | 快速验证 |
|------|---------|---------|
| 浏览器报 `DNS_PROBE_FINISHED_NXDOMAIN`，域名解析不出 | DNS 污染 | `nslookup github.com` 看解析结果 |
| 页面能开，但样式、登录按钮全乱 | SNI 阻断 / CDN 干扰 | 换浏览器、换网络对比 |
| clone/push 卡在 Writing objects 后断开 | 跨境链路丢包 / 限速 | 用 `curl -vI` 看 TCP/TLS 是否完成 |

浏览器和终端都能用的判断手段是 `curl -vI`，它会打印完整的握手过程：

```bash
curl -vI https://github.com
```

重点关注三行：`Trying ...`（开始 TCP 连接）、`Connected to ...`（TCP 成功）、`SSL connection using TLS...`（TLS 完成）。卡在 `Trying` 一直不出现 `Connected`，就是 TCP 握手被丢；能连上但后续卡顿，则是数据传输环节。

> [!tip] 大白话：症状分层像分诊
> 把网络问题想成看病：DNS 污染是「挂号都挂不上」——地址找不到；SNI 阻断是「人到了但门禁按名字拦下」——连接能建却被按域名拦截；跨境丢包是「路太堵，货送一半丢了」。先分清是哪一科，才能开对药方，所以这一章是后面所有方案的前提。

## 1.4 git 低速中止与 postBuffer 误区

很多人遇到「Writing objects 挂起很久然后断开」，第一反应是网络断了。其实更常见的机制是 git 自己「主动放弃」：`http.lowSpeedLimit` 和 `http.lowSpeedTime` 定义了「传输速度低于 X 字节/秒、持续 Y 秒，就判定超时并中止」[^c1-3]。跨境链路被限速时，恰好会触发这个机制。

```bash
# 查看当前值
git config --get http.lowSpeedLimit
git config --get http.lowSpeedTime

# 放宽阈值：允许 1 KB/s 持续 30 秒
git config --global http.lowSpeedLimit 1000
git config --global http.lowSpeedTime 30
```

> [!tip] 大白话：什么是「低速中止」
> 把它想成叫外卖的耐心阈值：「如果外卖员每 30 秒都没往前进一米，我就取消订单。」低速中止就是 git 的耐心阈值——不是网断了，而是 git 发现速度长期低于你的要求，主动放弃了。所以 Writing objects 卡很久才断，先怀疑它，别急着怪网络。

另一个流传很广的「偏方」是调大 `http.postBuffer`（默认 1 MiB）。官方文档明确：调高它对大多数 push 问题无效，只在 HTTP/1.0 或不合规代理面前才有意义，而且白白增加内存占用 [^c1-3]。这条建议在社区里流传甚广 [^c1-5]，但别把它当万能药——遇到 push 卡住，优先走第 3 章的代理方案。

## 本章小结

- 先查 GitHub 官方状态页（www.githubstatus.com）排除 GitHub 自身故障；大陆超时绝大多数是本地/跨境路径问题。
- 用 `GIT_TRACE_CURL=1 git fetch <url>` 看 HTTP 层对话，按卡住的位置区分 TCP / TLS / 传输环节，`GIT_TRACE`、`GIT_TRACE2` 等开关按需补充。
- `curl -vI https://github.com` 是最快的链路体检：`Trying` → `Connected` → `SSL connection` 三步，卡在哪一步就是哪一环。
- 症状分三类：DNS 污染（解析不出域名）、SNI 阻断/CDN 干扰（页面可用但资源缺失）、跨境丢包（握手超时或 Writing objects 中断）。
- Writing objects 挂起后断开，多半是 `http.lowSpeedLimit`/`lowSpeedTime` 低速中止机制触发；调大 `http.postBuffer` 对多数 push 无效，是误区。

下一章将解释这些现象背后的根因——GFW 作为「中间人」究竟用哪些手段干扰大陆访问 GitHub。

---

# 第 2 章：根因 — GFW 如何干扰大陆访问 GitHub

上一章我们学会了用 `GIT_TRACE_CURL=1` 和 `curl -vI` 把超时定位到「DNS 解析 / TCP 连接 / TLS 握手」的具体环节。诊断到此，你自然会问一个更深的问题：GitHub 本身没故障，为什么大陆网络就是能让它超时？这一章讲清根因——GFW 是怎么介入你与 GitHub 之间每一条国际连接的。

## 2.1 GFW 是「中间人」而非简单防火墙

大多数人把防火墙想成一堵墙：不让某些包过去。但 GFW 的工作方式更像一个**中间人**（Man-in-the-Middle，MitM）：它位于每个国际连接必经的路径上，不仅能**被动观察**你流量的去向和内容，还能**主动修改**连接本身[^c2-s4]。这意味着它能对流量做的事，远超「放行 / 丢弃」二选一——可以篡改、可以伪装、可以掐断、也可以限速。

> [!tip] 大白话
> 把 GFW 想成小区门口的门卫。普通防火墙是「不让带管制物品进小区」，而 GFW 是那个**能拆包裹、能看内容、能改地址、还能偷偷把包裹截下来的门卫**。所以「连接超时」背后可能藏着好几种不同的「动手脚」方式，光靠一条命令看不出全貌。

## 2.2 四种干扰机制

根据 TUM 学术综述，GFW 对跨境连接主要用四种手段[^c2-s4]：

**① 子网屏蔽 / 重路由（Subnet Blocking）**
直接对某些 IP 子网做 null-route 或 BGP 劫持，让发往该网段的流量全部黑洞或改道。它的特点是「按 IP 地址范围打击」，所以容易**连带误伤**——同一网段里无辜的网站也会被封掉。

**② DNS 污染（DNS Pollution）**
DNS 负责把 `github.com` 解析成 IP。GFW 在这里有两招：
- 要求**境内 DNS 解析器**对某些域名返回一个假 IP；
- 对你发往**境外解析器**（如 8.8.8.8）的查询，伪装成「官方应答」抢答一个假结果。

你拿到假 IP，连接自然失败或连去别处。历史上 `github.com` 在 2013 年就曾被 DNS 方式阻断，后因社区抗议而解除[^c2-s4]。

> [!tip] 大白话
> DNS 污染就是**篡改你查地址簿的结果**。你要寄信到「GitHub 出版社」，地址簿（DNS 服务器）被人偷偷换成了一条假地址；更狠的是，你打电话去问外面的总台（境外 DNS），总台还没开口，旁边就有人抢着冒充总台报一个错地址。你照着错地址寄，永远寄不到。

**③ 关键词过滤（Keyword Filtering + TCP RST）**
对**明文**流量（HTTP）检查内容里的敏感关键词，一旦命中就回发一个 TCP RST（重置）包，假装「对方主动断开了连接」，从而掐断会话。GFW 对 HTTP 流量有专门的检测逻辑[^c2-s4]。

**④ SNI 过滤（SNI Filtering）**
这是和 GitHub 超时最相关的一条。如今大量网站共用同一个 IP（IP 共享 / 虚拟主机），只看目标 IP 分不清你要访问谁；而 TLS 握手时，客户端会**明文**发送一个 SNI 字段，声明「我要访问的主机名」。GFW 就盯住这个**明文主机名**做过滤，命中即拦。反过来，想用 ESNI（加密 SNI）绕开？GFW 的选择是**直接丢包**——不给你商量的余地[^c2-s4]。

> [!tip] 大白话
> SNI 过滤是**检查包裹上贴的「收件人」标签**。很多网站共用同一个地址（IP），门卫看不出差别；但你在包裹外面贴了一张明信片大小的标签，写着「收件人：GitHub」，门卫一眼看到这张**明文标签**就拦下。所以地址（IP）完全正确，包裹照样到不了。

## 2.3 带宽限速与加密 DNS 的局限

除了上面四种「拦」的手段，GFW 还会对国际连接**普遍节流**——不拦你，但把你的路压得很窄，晚高峰更明显[^c2-s4]。这正好对应上一章说的「跨境链路丢包 / 卡 Writing objects 后断开」：不是连不上，而是太慢，慢到触发 git 的低速中止。

你可能会想：DNS 被污染，那把查询加密不就行了？**DoH / DoT（基于 HTTPS / TLS 的加密 DNS）确实能部分绕过 DNS 污染**，但局限很明显[^c2-s4]：
- GFW 也能**直接阻断加密 DNS** 服务，让你根本连不上解析器；
- 更隐蔽的是，部分**境内 DoH 解析器**返回的结果本身就和污染结果差不多。

所以「换加密 DNS」只能算半招，不能根治。

## 2.4 为什么改了 hosts 拿对 IP 仍会被阻断

把前两节串起来，就能解释一个常见的困惑：**明明用 hosts 把 `github.com` 指向了正确的 IP，走 HTTPS 访问还是超时。**

原因在于 DNS 污染和 SNI 过滤是**相互独立**的两层机制[^c2-s4][^c2-s5]：
- hosts 解决的是「拿到正确 IP」——它绕过了 DNS 解析，也就绕过了 DNS 污染；
- 但接下来建立 TLS 连接时，GFW 在 SNI 层看到的是明文主机名 `github.com`。因为 IP 是共享的、而流量内容是加密的，它能过滤的抓手恰恰就是这个 SNI 字段，hosts 对此毫无影响。

所以一个形象的结论是：**hosts 只治「查错地址」，治不了「看到收件人标签就拦」。** 要让流量真正打通，只能让连接完全绕过 GFW 的视野（走代理），或走 SNI 不在过滤名单内的路径（镜像 / 反代）[^c2-s5]。这也是后三章三种方案各自的原理出发点。

> [!tip] 大白话
> DNS 污染和 SNI 过滤的区别，就是「**改地址簿**」和「**认标签拦件**」的区别。hosts 相当于把地址簿换成了自己手写的小抄，地址（IP）是对的；但门卫在门口拦包裹看的不是地址，而是包裹上的「收件人：GitHub」标签——小抄救不了标签。想让包裹过去，要么让快递走门卫看不到的路（代理），要么换个门卫不认识的收件人标签（镜像 / 反代）。

## 本章小结

- GFW 不是简单防火墙，而是能**观察、篡改、掐断**每个国际连接的中间人（MitM）[^c2-s4]。
- 四种干扰机制：子网屏蔽 / 重路由（按 IP 段打击、易误伤）、DNS 污染（篡改解析结果）、关键词 RST（掐断明文 HTTP）、SNI 过滤（按 TLS 握手明文主机名拦 HTTPS）[^c2-s4]。
- 对国际连接普遍**带宽限速**，是「慢到超时」而非「连不上」的常见原因[^c2-s4]。
- 加密 DNS（DoH/DoT）只能**部分**绕过污染：GFW 可阻断加密 DNS，部分境内 DoH 解析器结果与污染近似[^c2-s4]。
- hosts 拿到正确 IP 仍被阻断，是因为 **SNI 过滤独立于 DNS 存在**：治得了「查错地址」，治不了「看标签拦件」[^c2-s4][^c2-s5]。

---

# 第 3 章：方案一 — 走代理：环境变量与各工具配置

前两章我们把「超时发生在哪一环」和「GFW 为什么能干扰」讲清楚了，这一章进入真正的实操。如果你手上有一台可用的代理客户端（Clash/v2ray 类，本地监听如 `127.0.0.1:7890`），走代理是覆盖面最广、最一劳永逸的方案——但难点在于：**每个工具都要单独配一遍**，而且配错了常常不报错、只是悄悄不走代理。本章按「环境变量通用语义 → git → npm → docker」的顺序，把代理配置讲透，并点出最容易坑人的几处不一致。

---

## 3.1 代理环境变量的通用语义（libcurl 规则）

curl、git、pip、go 这些工具为什么会「共用」同一组代理环境变量？因为它们要么基于 libcurl，要么遵循同一套传统惯例。理解了这组变量的规则，就能解释大多数「我明明设了代理怎么不走」的诡异现象。规则见 [libcurl-env(3) manpage](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html)：

- **按 URL scheme 选变量**：访问一个 `https://` 开头的目标，选用的其实是 `http_proxy`（不是 `https_proxy`）。这里的 scheme 指的是**代理本身的协议**，不是目标协议——用 HTTP 代理同时代理 http 和 https 目标，都靠 `http_proxy`。
- **`http_proxy` 只认小写**：libcurl 会刻意忽略大写的 `HTTP_PROXY`（这是安全设计，防止 CGI 环境注入污染）；而 `https_proxy`、`all_proxy`、`no_proxy` 大写也认。
- **scheme 专属变量覆盖 `ALL_PROXY`**：`http_proxy`/`https_proxy` 的优先级高于 `ALL_PROXY`（后者只是全协议兜底）。
- **`NO_PROXY` 是逗号分隔的直连白名单**：支持 IP 前缀（如 `192.168.`）、域名（`example.com` 及其所有子域都直连）、前导点 `.example.com`（**仅**匹配子域，不含主域）、以及 `*`（全部直连）。

```bash
# 只对当前终端会话生效，关闭即失效；写进 ~/.zshrc / ~/.bashrc 则长期生效
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
# all_proxy 兜底所有协议（可用 socks5）
export all_proxy=socks5://127.0.0.1:7890
# 本地地址一律直连，不要绕代理
export no_proxy=localhost,127.0.0.1,192.168.,.local

# 验证 curl 是否真的走了代理（看输出的 Proxy 头）
curl -vI https://github.com 2>&1 | grep -iE "proxy|via"
```

> [!tip] 大白话：为什么 `http_proxy` 只认小写？
> 把 libcurl 想成一位严格的宿管阿姨：她只认证件上的本名（小写 `http_proxy`）。你换个艺名 `HTTP_PROXY` 去敲门，她以为你是来骗门禁的陌生人，直接不理你——这正是 libcurl 刻意为之的安全设计，防止从外部环境注入伪造代理。所以别再问「为什么我设了 `HTTP_PROXY` 没用」，改回小写就对了。

---

## 3.2 git 代理配置与优先级

git 是你最常遇到超时的场景，配置优先级从高到低如下（详见 [git-config 官方文档](https://git-scm.com/docs/git-config)）：

1. `http.proxy`（git config）—— 优先级**最高**，压过一切环境变量；
2. `http_proxy` / `https_proxy` / `all_proxy` 环境变量 —— 其次；
3. `remote.<name>.proxy` —— 按**单个仓库**覆盖 `http.proxy`，空串表示该仓库禁用代理；
4. `core.gitProxy` —— 只针对 `git://` 协议（GitHub 2022 年已移除 `git://` 支持，对 GitHub 基本过时，仅剩其他仍提供该协议的主机）。

代理值的语法是 `[protocol://][user[:password]@]proxyhost[:port][/path]`——比如带用户名密码可写 `http://user:pass@127.0.0.1:7890`。

```bash
# 全局代理（推荐，对 https 协议的 remote 生效）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 查看 / 取消
git config --global --get http.proxy
git config --global --unset http.proxy

# 仅对某个 remote 单独覆盖：例如公司内网仓库要直连，就设空串
git config remote.origin.proxy ""

# 列出当前仓库所有 remote 相关配置，便于排查
git config --get-regexp '^remote\.'
```

> [!tip] 大白话：`http.proxy` 为什么优先级最高？
> 把环境变量想成公司的「默认门禁制度」，`git config` 里的 `http.proxy` 想成「安保亲自点名放行」。制度写得再宽松，点名放行才是最终决定。这就是「我明明 export 了代理，git 还是不听话」最常见的真相——八成是更高级的 git 配置在头顶压着，用 `git config --get-regexp` 查一遍就知道。

---

## 3.3 npm 代理配置

npm 有一套自己的配置体系（`.npmrc` / `npm config`），优先级是**命令行 > 环境变量 > npmrc**（见 [npm config 官方文档](https://docs.npmjs.com/cli/v10/using-npm/config)）：

```bash
# 三个配置键写入 ~/.npmrc
npm config set proxy http://127.0.0.1:7890
npm config set https-proxy http://127.0.0.1:7890
npm config set noproxy "localhost,127.0.0.1,.local"

# 验证
npm config get proxy
npm config list
```

npm 读取代理的细节值得单独强调，因为和 libcurl 不一致：

- 环境变量 `HTTPS_PROXY`、`https_proxy`、`HTTP_PROXY`、`http_proxy` **都会被 npm 采用**——注意，npm 大小写都认，和上一节 libcurl「只认小写」的行为不同。
- `noproxy` 默认取环境变量 `NO_PROXY` 的值。
- 所有 `npm_config_*` 前缀的环境变量都会被 npm 当作配置参数：例如 `npm_config_proxy=http://127.0.0.1:7890` 等效于 `npm config set proxy ...`，这在你给 agent 注入配置时非常方便。

> [!tip] 大白话：npm 和 libcurl 的大小写口味不一样
> 同一个 `HTTP_PROXY`，libcurl 系工具（git/curl/pip）当它不存在，npm 却照单全收。就像同一件快递，菜鸟驿站只认小写回执，顺丰大小写都认。跨工具排错时，别拿「这套环境变量我设过了」自我安慰——每个工具都有自己的脾气，逐个验证最稳。

---

## 3.4 docker daemon 代理配置

这是全篇最容易踩的坑：**docker daemon 是一个独立常驻进程，不读你的 shell 环境变量**。你在终端 `export https_proxy` 之后再 `docker pull`，daemon 拉镜像时根本看不见。必须把代理写进 daemon 自己的配置里（见 [Docker Daemon proxy configuration](https://docs.docker.com/engine/daemon/proxy/)）。

**方式 A：systemd drop-in**（主流 Linux 发行版，非 rootless 的默认形态）

```bash
# /etc/systemd/system/docker.service.d/http-proxy.conf
# 创建一个 drop-in 片段，追加到 docker.service 的环境配置
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
```

```bash
# 重载 systemd → 重启 docker daemon → 验证 Environment 是否生效
sudo systemctl daemon-reload
sudo systemctl restart docker
sudo systemctl show --property=Environment docker
```

**方式 B：`daemon.json` 的 `"proxies"` 块**（Docker Engine 23.0+，也适用于不以 systemd 启动 daemon 的环境）

```json
// /etc/docker/daemon.json
{
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890",
    "no-proxy": "localhost,127.0.0.1,.local"
  }
}
```

改完同样要 `sudo systemctl restart docker`。注意：`daemon.json` / CLI 的显式代理配置**优先于环境变量**。

两个重要差异（S7）：

- **rootless 模式**不用 `/etc/systemd/system/`，而是用户级 systemd：把 drop-in 放到 `~/.config/systemd/user/docker.service.d/`，并用 `systemctl --user daemon-reload && systemctl --user restart docker`。
- **Docker Desktop 会忽略 `daemon.json` 的代理配置**，必须在设置界面（Settings → Resources → Proxies）里手动填，`docker pull` 才会走代理。

> [!tip] 大白话：docker daemon 像个不看你朋友圈的室友
> 你 shell 里 `export` 的代理，daemon 完全看不见——就像你在自己房间贴了张「出门右转」的纸条，隔壁室友根本不会看。要让他出门走对路，得把纸条贴到他门上，也就是写进 systemd 或 daemon.json。这就是「环境变量明明都对，docker pull 还是超时」最常见的真相。

---

## 3.5 透明代理要求与常见坑

最后把本方案的硬性要求与高频坑汇总一下：

- **代理必须完全透明**：git 文档明确要求代理不得修改、不得缓冲请求包（S3）。Clash/v2ray 这类标准代理没问题；但如果代理软件做了内容改写、压缩或缓冲，会导致 clone/push 数据损坏或校验失败。遇到「走代理后 clone 总是半路断开/校验失败」，优先怀疑代理不透明。
- **`http.postBuffer` 误区**：默认 1 MiB，官方明示调高它对**多数 push 无效**，只对 HTTP/1.0 或不合规代理有效，且白白增加内存占用（S3）。不要听信社区里「push 失败就调大 postBuffer」的万能方子。
- **大小写语义不一致**：libcurl 只认小写 `http_proxy`（S11），npm 大写也认（S12）。跨工具排错时，逐个工具验证，不要凭一套经验套所有工具。
- **优先级速记**：`http.proxy` > 环境变量；scheme 专属变量（`http_proxy`/`https_proxy`）> `ALL_PROXY`；`NO_PROXY` 直连白名单优先于一切代理。
- **验证手段**：配完任何工具的代理，都用 `GIT_TRACE_CURL=1 git fetch` 或 `curl -vI` 确认请求真的经过代理，而不是「配置了就算数」。

---

## 本章小结

- 代理环境变量是各工具的「通用语言」，但 libcurl 系工具只认小写 `http_proxy`；scheme 专属变量优先于 `ALL_PROXY`，`NO_PROXY` 白名单优先于一切代理。
- git 配 `http.proxy` / `https.proxy`，优先级高于环境变量；`remote.<name>.proxy` 可对单仓库覆盖甚至禁用，`core.gitProxy` 只针对 `git://`（对 GitHub 已过时）。
- npm 用 `proxy` / `https-proxy` / `noproxy` 三个配置键，环境变量大小写都认——与 libcurl 不一致，是跨工具排查的经典陷阱。
- docker daemon 不读 shell 环境变量，必须用 systemd drop-in 或 `daemon.json` 的 `"proxies"` 块；rootless 走 `systemctl --user`，Docker Desktop 则忽略 `daemon.json`，要在设置里配。
- 代理必须透明、不得改包；`http.postBuffer` 调高对多数场景无效。

下一章我们换一条不依赖代理的路：国内镜像加速。即使没有代理，npm / pip / go 也能通过镜像源把下载速度拉回正常水平。

---

# 第 4 章：方案二 — 国内镜像加速

上一章介绍的"走代理"需要一台可用代理；但很多人其实没有。本章换一条思路：**不改变网络路径，而是改变包的下载来源**——把 npm、pip、go 默认连接的官方源，替换成国内同步镜像。包本身不变，只是从更近的服务器取。镜像服务器位于境内，下载请求基本不出境，跨境丢包、限速这两个超时主因（呼应第 2 章根因）直接消失。

> [!tip] 大白话
> 把官方源想成"海外原厂仓库"，国内镜像就是"国内分仓"。原厂每批货（软件包）都会同步一份到分仓，你在国内直接从分仓提货，网络链路短了，自然不容易超时。

## 4.1 npm：npmmirror 与 cnpm

npmmirror（前身淘宝 npm）是阿里维护的 npm 官方仓库镜像 [npmmirror](https://npmmirror.com/)。一次性把默认 registry 切过去：

```bash
npm config set registry https://registry.npmmirror.com
```

之后 `npm install` 都会走镜像地址。验证是否生效：

```bash
npm config get registry
# 期望输出：https://registry.npmmirror.com/
```

也可以换用 cnpm 客户端：

```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
```

cnpm 的额外价值是**手动触发同步**：某个包官方刚发新版、镜像还没跟上时，执行：

```bash
cnpm sync <包名>
```

该包会从官方源即时同步到镜像，随后 `npm install` 就能拿到新版。

## 4.2 pip：TUNA 与配置优先级

PyPI 官方源同样慢。清华 TUNA 提供 PyPI 镜像 [TUNA PyPI 帮助](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)。只想单次安装用镜像，加 `-i`：

```bash
pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple <包名>
```

注意路径里 **`/simple` 不能少、必须走 https**——这是简单索引协议规定的固定路径；TUNA 还提供备用域名 `pypi.tuna.tsinghua.edu.cn`，主域名故障时可替换 [TUNA](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)。

想长期生效，写进 pip 配置：

```bash
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

用 `pip config list` 查看当前生效配置，确认 index-url 已指向镜像。

需要同时保留多个镜像（一个挂掉自动换下一个）时，用 `extra-index-url`，在配置文件里手写（Linux/macOS 为 `~/.config/pip/pip.conf`，Windows 为 `%APPDATA%\pip\pip.ini`）：

```ini
[global]
index-url = https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
extra-index-url =
    https://pypi.org/simple
    https://mirrors.aliyun.com/pypi/simple/
```

pip 的配置优先级是：**命令行 > 环境变量 > 配置文件** [pip 官方配置文档](https://pip.pypa.io/en/stable/topics/configuration/)。PDM、Poetry、uv 也都有各自的镜像配置段，思路一致：把 index 指到 TUNA 即可 [TUNA](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)。

## 4.3 go：GOPROXY 与 sumdb

Go 模块下载走 GOPROXY。先确认模块模式开启，再指向七牛的 goproxy.cn [goproxy.cn](https://goproxy.cn/)：

```bash
go env -w GO111MODULE=on
go env -w GOPROXY=https://goproxy.cn,direct
```

`-w` 会把设置**持久化写入 go 的环境配置文件**，重开终端依然生效；用 `go env GOPROXY` 随时核对当前值。`GOPROXY` 逗号后的 `direct` 是兜底表达式：镜像找不到的模块，直接回源官方抓取。goproxy.cn 用七牛 CDN，缓存超 5268 万模块版本、无带宽限制 [goproxy.cn](https://goproxy.cn/)。

校验和数据库（sumdb）**自动走代理**，无需额外配置——go 在下载时通过 GOPROXY 或默认的 `sum.golang.org` 校验模块，goproxy.cn 对 go 工具链透明，直接 `go mod download` 验证即可。

## 4.4 Docker 镜像加速器现状（推断）

Docker 拉镜像同样有"加速器"概念，但**本节为推断、未验证**（截至 2026-08，未在官方源确认实际可用清单）：2024 年后，国内多数公共 registry 加速器（早年流传的阿里、DaoCloud、中科大等通用地址）已下架或收紧，网上旧教程里的地址大概率已失效；阿里云个人专属加速器需登录容器镜像服务控制台，获取**仅绑定个人账号**的加速地址，**没有通用公共地址**。

因此 Docker 场景建议优先走第 3 章的代理方案；若必须用加速器，请以厂商控制台当前给出的地址为准，不要沿用网上流传的旧公共地址。

> [!tip] 大白话
> 早年公共加速器像"随便进的大食堂"，2024 年后陆续关门了；阿里云那个现在是"包间"——要拿你自己的会员卡（登录控制台）才给你开一间，没有通用的门牌号。

## 4.5 常见坑

- **混合源导致依赖锁问题**：npm 生成 `package-lock.json` 时会把 registry 地址写进锁文件的 `resolved` 字段。开发机用镜像装、CI 用官方源装，锁文件里地址不一致，会触发锁校验失败或重新解析依赖树，出现"本地能装、CI 装不上"的诡异现象。解决：团队统一 registry，明确以锁文件为准；pip 的 `requirements.txt`/lock 同理，别混用多源锁定同一组版本。
- **pip 缓存旧包**：pip 会把下载过的包缓存在本地（缓存是为了加速重复安装），但**镜像源更新不会自动失效本地缓存**——镜像已有新版、本地缓存却命中旧版时，`pip install` 仍装旧包，排查半天以为镜像没同步。用 `pip install --no-cache-dir` 跳过缓存，或 `pip cache purge` 清空后再装。

## 本章小结

- 镜像方案的核心是"换源不换网"：把 npm/pip/go 的下载源切到国内镜像，绕开跨境链路超时，适合没有代理的场景。
- npm：`npm config set registry https://registry.npmmirror.com`，配合 cnpm 可即时 `cnpm sync <包名>` 同步新版。
- pip：临时用 `-i`，长期用 `pip config set global.index-url`，多源用 `extra-index-url`；路径 `/simple` 不能少、必须 https；优先级为命令行 > 环境变量 > 配置文件。
- go：`go env -w GO111MODULE=on` + `go env -w GOPROXY=https://goproxy.cn,direct`，sumdb 校验自动代理。
- Docker 公共加速器 2024 后多数下架、阿里云专属需登录控制台——本节为推断、未验证，建议优先代理。

下一章介绍另一类"不改源、不靠代理"的临时手段：hosts 固定 IP 与 gh-proxy 反代前缀，并说明其时效与安全风险。

---

# 第 5 章：方案三 — hosts 与 gh-proxy 工具

前两章讲的代理和镜像，分别需要「一台可用代理」或「可信镜像源」。这一章给出两个零依赖、零成本的临时手段：改 hosts 把 GitHub 域名直接指向较快 IP，以及给 GitHub URL 加反代前缀的 gh-proxy。它们适合应急救急，但各有明确的时效与安全边界——读完这一章，你会知道什么时候能用、什么时候千万别用。

## 5.1 hosts 方案：GitHub520 原理与使用

### 原理：电话簿手动改号码

hosts 是操作系统自带的「域名 → IP」静态映射表，优先级高于 DNS 查询。GitHub520 的思路很简单：当域名解析被污染、或解析出的 IP 跨境链路差时，它提前测好一批「大陆直连速度较好」的 GitHub IP 写进 hosts，让本机跳过污染 DNS 直接连过去。[GitHub520](https://github.com/521xueweihan/GitHub520)（S14）

> [!tip] 大白话
> 把 hosts 想成「电话簿手动改号码」：你按原电话号码（DNS 解析的 IP）拨过去总打不通或很卡，GitHub520 直接给你一本实测通畅的号码簿，把 GitHub 的号码手抄进去，以后拨号就不经过那个爱捣乱的查号台。所以改 hosts 只绕过了「查号」环节，并不能绕过线路本身的阻断。

### 数据源与 hosts 位置

GitHub520 的 hosts 内容托管在非 GitHub 域名上，**不依赖访问 GitHub 本身**：

```
数据源：https://raw.hellogithub.com/hosts
```

三种主流系统的 hosts 位置（S14）：

| 系统 | hosts 文件路径 |
|------|--------------|
| Windows | `C:\Windows\System32\drivers\etc\hosts` |
| Linux | `/etc/hosts` |
| macOS | `/etc/hosts` |

### 刷新 DNS 缓存

改完 hosts 后无需重启系统，但要让新映射立即生效，需刷新 DNS 缓存（S14）。

Windows（以管理员身份运行 cmd / PowerShell）：

```bash
ipconfig /flushdns
```

macOS：

```bash
sudo killall -HUP mDNSResponder
```

### macOS 一键命令与 SwitchHosts 自动更新

GitHub520 官方 README 提供 macOS 一键脚本（S14）。运行前建议先用 `curl` 预览 hosts 内容再执行：

```bash
curl https://raw.hellogithub.com/hosts   # 先预览，确认内容后再执行下方命令
sudo sh -c 'cd /etc; curl -L https://raw.hellogithub.com/hosts -o hosts; killall -HUP mDNSResponder'
```

手动改 hosts 的痛点是「GitHub 的 IP 会变」。GitHub520 推荐用跨平台工具 **SwitchHosts**：把 `https://raw.hellogithub.com/hosts` 配成远程源，客户端每小时自动拉取刷新，省去手工维护成本（S14）。

### 容器内不生效：hosts 改的是宿主，不是容器

GitHub520 改的是**宿主机**的 `/etc/hosts`。Docker 容器有自己独立的 `/etc/hosts`（由 Docker 动态生成，只含 localhost + 容器 hostname + `--add-host` 条目），且容器内 DNS 走 Docker 内嵌解析器 `127.0.0.11`，它把查不到的域名转发给公共 DNS——**两者都不读宿主的 `/etc/hosts`**。

所以宿主机改完 hosts，容器内 `github.com` 依然解析到被污染的 IP，照样超时；即使 `--network host` 共享网络栈，`/etc/hosts` 与 `resolv.conf` 仍是容器自己的（`resolv.conf` 是容器创建时的快照，之后宿主改解析器它也不会跟进）。

容器里要用 hosts 方案，得把映射**注入容器**（一次性；IP 从 `https://raw.hellogithub.com/hosts` 取当前值）：

```bash
docker run --add-host github.com:140.82.112.3 \
           --add-host api.github.com:140.82.112.6 ...
```

```yaml
# docker-compose.yml
services:
  agent:
    extra_hosts:
      - "github.com:140.82.112.3"
      - "api.github.com:140.82.112.6"
```

**代价**：GitHub520 的 IP 会轮换，注入后不会自动更新，IP 变了需重建容器——容器场景更推荐第 3、4、6 章的代理 / 镜像方案。若想让 GitHub520 刷新后容器内**动态生效**，可在宿主跑一个读取 `/etc/hosts` 的 dnsmasq，并给容器 `dns: [宿主 IP]`。

## 5.2 反代前缀：gh-proxy 用法与自部署

### 前缀用法：给 URL 加一段即可

gh-proxy 是反向代理项目：把 GitHub 的克隆/下载 URL 前面加一个代理前缀，流量先到代理服务器，由它替你访问 GitHub 再转回来。[gh-proxy](https://github.com/suiyueqingqian/gh-proxy)（S15）

克隆公开仓库时，把 `https://github.com/user/repo.git` 换成「前缀 + 原 URL」：

```bash
git clone https://gh.api.99988866.xyz/https://github.com/user/repo.git
```

### 公共实例的局限

公共代理实例免费开放，但有两个现实问题（S15）：

- **域名频繁变动**：公共实例域名随时可能更换，写进脚本很快失效；
- **演示站不堪重负**：免费实例被大量用户共用，速度和稳定性没保证。

结论：**偶尔手动用一次可以；大量使用或写进自动化脚本，建议自部署**。

### 自部署选项

gh-proxy 官方提供两个版本（S15）：

1. **CF Worker 版**：把项目里的 `worker.js` 粘到自己的 Cloudflare Workers，无需服务器；CF 免费版每天 10 万次请求，对个人使用通常足够。
2. **Python 版**：基于 Python，可用 Docker 一键部署到自己的服务器/VPS；Docker 镜像与启动命令以项目 README 的 `docker run` 说明为准，按其执行即可。

## 5.3 时效与安全风险

这一节是本章重点，**用前必读**。

**风险清单（S14、S15、[ipdodo](https://www.ipdodo.com/news/16580/) 的 S5）：**

1. **Token 泄露（最高危）**：私有仓库若用 `git clone https://user:TOKEN@gh-proxy...` 的方式，Token 会以明文经过第三方代理服务器传输，等于把仓库钥匙交给陌生人，**有泄露风险——绝对不要用公共 gh-proxy 实例克隆私有仓库**（S15）。
2. **hosts 服务器到期**：GitHub520 的数据服务器将于 **2026-12-31 到期**（续费靠赞助），该数据源可能在到期后停更（S14）。
3. **社区 IP 时效**：hosts 内容是社区实测 IP，可能随 GitHub 变更/更换 CDN 失效；失效时表现为「hosts 里明明写着这个 IP，连接却超时」（S5）。
4. **不适合自动化构建**：在服务器或 CI 里硬编码 hosts 后，IP 动态轮换会让配置几天内失效，维护成本高；gh-proxy 公共前缀同理会因域名变动而失效。**两者都不适合自动化构建**（S5、S15）。
5. **只绕 DNS，不绕线路**：hosts 只解决「解析到好 IP」；若该 IP 线路本身被限速或阻断，依然会超时（回顾第 2 章的 SNI 过滤机制）。
6. **容器内不生效**：hosts 方案只作用于改了 `/etc/hosts` 的那台机器；Docker 容器有独立的 `/etc/hosts` 与 DNS（`127.0.0.11`），宿主改 hosts 不进入容器，`--network host` 也不例外。容器场景要用 `--add-host` / `extra_hosts` 注入，或直接走代理 / 镜像。

> [!tip] 大白话
> 这两个方案本质是「熟人带路」：GitHub520 帮你抄好电话号码，gh-proxy 帮你去柜台代取快递。熟人靠谱时很快，但「代取快递」的中间人只要经手一次你的钥匙（Token），保险柜就再也不安全了——所以私有仓库的钥匙永远别交给代取的人。

## 本章小结

- hosts 方案（GitHub520）把 GitHub 域名手动解析到社区实测的较快 IP，数据源 `https://raw.hellogithub.com/hosts`，不依赖访问 GitHub；改完需刷新 DNS（Win `ipconfig /flushdns` / Mac `sudo killall -HUP mDNSResponder`），可用 SwitchHosts 远程源自动更新。
- gh-proxy 反代前缀把 `https://github.com/...` 换成 `https://gh.api.99988866.xyz/https://github.com/...`，公开仓库偶尔用可以；公共实例域名变动频繁、人多易慢，大量使用建议自部署 CF Worker 或 Python Docker 版。
- 高风险事项：私有仓库 Token 经第三方代理传输会泄露；hosts 服务器 2026-12-31 到期；社区 IP 会随 GitHub 变更失效；两者都不适合写进自动化构建。
- **容器内不生效**：hosts 方案只作用于改了 `/etc/hosts` 的那台机器；Docker 容器有独立 `/etc/hosts` 与 DNS，宿主改 hosts 不进入容器（`--network host` 也不例外），容器里要用 `--add-host` / `extra_hosts` 注入或走代理/镜像。
- 下一章把这些手段放进 agent 场景：如何给拉包工具（含 docker daemon）统一配好网络。

## 更新记录

- **2026-08-29**：补充「容器内不生效」——GitHub520 改的是宿主 `/etc/hosts`，Docker 容器有独立 `/etc/hosts` 与内嵌 DNS，宿主映射不进入容器；给出 `--add-host` / `extra_hosts` 注入与 dnsmasq 动态方案。

---

# 第 6 章：Agent 场景落地 — 给拉包工具配好网络

前几章把 git、npm、docker 等工具的单点代理配置拆开了，本章把它们落到你的真实场景：一个 agent 进程从大陆网络拉取 GitHub 包时连接超时。结论先行——给 agent 配好「环境变量 + git 全局配置」双保险，再单独处理 Docker daemon，就能覆盖绝大多数拉包路径。

## 6.1 环境变量 + git 全局配置的组合

agent 本质上是「一个父进程 + 一串子进程」：它调用的 git、curl、npm、pip 都是它的子进程。Linux/macOS 的子进程会无条件继承父进程的环境变量，所以只要在启动 agent 的 shell（或 agent 的 systemd unit / 运行时配置）里导出代理变量，agent 内部所有工具就会自动读到。

```bash
# 假设本机代理客户端（Clash/v2ray 类）监听 127.0.0.1:7890，按实际端口修改
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export NO_PROXY=localhost,127.0.0.1
```

两个关键细节：

- **`http_proxy` 只认小写**：libcurl 的环境变量语义里，`http_proxy` 必须是小写才生效，其余变量（如 `HTTPS_PROXY`、`ALL_PROXY`）大小写都认（S11）。所以上面统一用全小写是刻意为之。
- **git 有自己的配置层**：git 的 `http.proxy` 配置项优先于所有 `http_proxy`/`https_proxy`/`all_proxy` 环境变量（S3）。也就是说，即便某个子进程没能继承到环境变量，git 仍然会走代理——这就是「双保险」。

```bash
# git 全局配置，同时覆盖 http/https 两种 remote
git config --global http.proxy http://127.0.0.1:7890

# 验证：能打印出代理地址说明已生效
git config --global --get http.proxy
```

> [!tip] 大白话
> 把环境变量想成「公司张贴的全局规定」，git 全局配置想成「单独给 git 发的一张工牌」。规定贴了，有的工具不抬头看；工牌发了，别的工具又不认。两个都做才是真正的双保险——agent 这个「总包」带着一串「分包」，只要有一个机制生效，拉包就不会裸奔。

遇到某次想临时绕过代理时，git 支持用空串禁用（S3）：

```bash
git -c http.proxy= git fetch
```

## 6.2 浏览器能开但 git 超时的排查

「浏览器能打开 GitHub，终端 git clone 却超时」是最高频的困惑。原因很简单：**浏览器默认读系统的代理设置，而 git/curl 只认环境变量或自身配置，不读系统代理**（S5）。所以浏览器「能开」并不代表命令行也走了代理。

排查三步走：

```bash
# 1. 先确认 git 是否已有代理：无输出 = 没配
git config --global --get http.proxy

# 2. 没有就显式补上
git config --global http.proxy http://127.0.0.1:7890
```

3. 再用第 1 章提过的追踪命令确认流量确实经过代理：`GIT_TRACE_CURL=1 git fetch`，输出里出现 `Connected to 127.0.0.1 (127.0.0.1) port 7890` 之类的行即为生效。

## 6.3 Docker build/pull 的代理配置

最容易踩的坑：agent 里 `export http_proxy=...` 之后 `docker pull` 仍然超时。因为 **Docker daemon 是独立的后台进程，不读 shell 的环境变量**（S7）——你在终端导出的变量只影响当前 shell 及它启动的子进程，影响不到 daemon。所以 docker 必须走自己的配置通道。

方式一：systemd drop-in（推荐，可验证）：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo tee /etc/systemd/system/docker.service.d/http-proxy.conf > /dev/null <<'EOF'
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker

# 验证：输出 Environment 三行即生效
systemctl show --property=Environment docker
```

方式二：`daemon.json` 的 `proxies` 块：

```json
{
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890",
    "no-proxy": "localhost,127.0.0.1"
  }
}
```

改完重启 daemon（`sudo systemctl restart docker`）。daemon 的代理配置会传递给它启动的容器，因此 `docker pull` 拉镜像和 `docker build` 拉基础镜像、执行 RUN 阶段的网络请求都覆盖在内。

> [!tip] 大白话
> 把 docker daemon 想成「装修总包公司」，你在终端 export 的变量只是「对现场的临时工喊的话」，总包在后台按自己的图纸（配置文件）干活。要让总包走代理，得改图纸——改 systemd/daemon.json，而不是在工地上喊。

注意：Docker Desktop（macOS/Windows 图形版）会忽略 `daemon.json` 的代理配置，必须在它的设置面板里配（S7）。

## 本章小结

- Agent 的拉包网络由「环境变量 + git 全局配置」双保险覆盖：环境变量靠子进程继承生效，git 的 `http.proxy` 独立兜底。
- `http_proxy` 只认小写（libcurl 语义），`HTTPS_PROXY`/`NO_PROXY` 大小写均可；统一用全小写最省心。
- 浏览器能开但 git 超时 = git 没读系统代理，显式 `git config --global http.proxy` 即可。
- Docker daemon 不读 shell 环境变量，必须用 systemd drop-in 或 `daemon.json` 配置；Docker Desktop 还要走图形设置。
- 所有改动都用 `git config --get` / `systemctl show` 验证，做到可复制、可回溯。

下一章我们把所有方案收拢成一张「决策速查表」：遇到超时先查哪步、有代理和无代理各走哪条路，以及全流程的坑位清单。

---

# 第 7 章：决策速查表与常见坑

前面六章把「诊断 → 根因 → 代理 / 镜像 / hosts·gh-proxy 三类方案 → Agent 场景」讲完了。这一章不引入新原理，只把决策路径压缩成一张可随时回查的速查表：遇到超时先做什么、五类方案怎么选、最常踩的坑有哪些。

## 7.1 五步决策流程

遇到「GitHub 连接超时」，按下面的顺序走，不要在第一步就急着改配置。全程依据见深度素材 5 节：

| 步骤 | 动作 | 关键命令 / 依据 | 判断标准 |
| --- | --- | --- | --- |
| ① 排除 GitHub 自身故障 | 先看官方状态页 | https://www.githubstatus.com/ [S1](https://www.githubstatus.com/) | 官方有故障则等待；否则进入下一步 |
| ② 定位卡点 | git 追踪 + curl 验证 TCP/TLS | `GIT_TRACE_CURL=1 git fetch`；`curl -vI https://github.com` [S2](https://git-scm.com/docs/git) | 看卡在 connect / TLS / transfer 哪一环 |
| ③ 快速分类 | 按症状归入三类 | DNS 报错→污染；浏览器能开 git 超时→未走代理；Writing objects 挂起→跨境丢包 [S5](https://www.ipdodo.com/news/16580/) | 决定走④还是⑤ |
| ④ 有代理走代理 | 环境变量 + 各工具显式配置 | `export http_proxy=...`；`git config --global http.proxy`；npm/docker/go 逐项配 [S3](https://git-scm.com/docs/git-config) [S7](https://docs.docker.com/engine/daemon/proxy/) [S11](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html) [S12](https://docs.npmjs.com/cli/v10/using-npm/config) | 有可用代理时首选，持久且通用 |
| ⑤ 无代理走镜像 + hosts | 包镜像 + gh-proxy 前缀 + hosts 临时改 DNS | `npm config set registry`；pip `index-url`；`go env -w GOPROXY`；hosts 写 GitHub520 [S8](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) [S9](https://pip.pypa.io/en/stable/topics/configuration/) [S10](https://goproxy.cn/) [S13](https://npmmirror.com/) [S14](https://github.com/521xueweihan/GitHub520) [S15](https://github.com/suiyueqingqian/gh-proxy) | 无代理时的兜底与临时手段 |

> [!tip] 大白话
> 把①~③想成「先量体温再开药」：先确认 GitHub 没病（①）、再确认是哪里疼（②③），最后才按症状开药（④⑤）。跳过量体温直接改配置，等于病根没找准就乱抓药。

## 7.2 方案对照速查表

五类方案在「适用场景、持久性、风险、是否适合自动化」四个维度上的对比：

| 方案 | 适用场景 | 持久性 | 主要风险 | 适合自动化构建？ |
| --- | --- | --- | --- | --- |
| 代理 | 已有一台 Clash/v2ray 类客户端；日常拉包 | 持久，一次配置长期生效 | 代理须完全透明不得改包；git/npm 环境变量大小写语义不一致 | 是（首选） |
| npm·pip·go 镜像 | 拉包超时、无代理 | 持久（registry / index-url / GOPROXY 全局生效） | 混合源导致 lock 地址不一致；pip 缓存旧包 | 是（无代理路线首选） |
| Docker 加速器 | 拉取 Docker 镜像 | 需持续维护；2024 后公共加速器多数关停（推断） | 公共地址普遍失效；阿里云个人专属需登录控制台获取 | 仅 registry 地址稳定时 |
| hosts（GitHub520） | 快速应急、临时克隆 | 短：社区 IP 随时失效、服务器 2026-12-31 到期 | IP 共享 + SNI 阻断下改对 IP 仍可能被断；不随 GitHub 变更自动更新 | 否 |
| gh-proxy 反代前缀 | 临时拉仓库、无代理应急 | 短：公共实例域名频繁变动 | 私有仓库 Token 经第三方代理传输有泄露风险 | 否（仅应急） |

一句话记忆：**有代理用代理，无代理用镜像；hosts 与 gh-proxy 只作临时，别进生产自动化。**

> [!tip] 大白话
> 把五类方案想成通勤方式：代理=自己有专车（最稳，长期）；镜像=地铁直达（没车时首选，线路固定）；hosts / gh-proxy=临时拼车（应急可以，天天用不靠谱）。

## 7.3 常见坑清单与未决问题

写配置时最常踩的五个坑：

| 坑 | 典型表现 | 正确做法 |
| --- | --- | --- |
| postBuffer 误区 | 调高 `http.postBuffer` 期望解决 push 断连 | 官方明示对多数 push 无效，仅对 HTTP/1.0 或不合规代理有效且增内存（[S3](https://git-scm.com/docs/git-config) vs [S6](https://stackoverflow.com/questions/15240815/) 社区共识） |
| 环境变量大小写不一致 | 导了大写 `HTTP_PROXY`，git 不认 | libcurl 的 `http_proxy` 只认小写，npm 大写也认——按工具分别处理（[S11](https://manpages.debian.org/experimental/libcurl4-doc/libcurl-env.3.en.html) vs [S12](https://docs.npmjs.com/cli/v10/using-npm/config)） |
| `GIT_CURL_VERBOSE` 旧名 | 用旧环境变量名拿不到追踪输出 | 现代 git 用 `GIT_TRACE_CURL`（[S2](https://git-scm.com/docs/git) 更正） |
| 公共 DNS 被劫持 | 换成 8.8.8.8 仍被污染 | 公共 DNS 可能被 UDP 劫持；DoH 可部分绕过，但部分境内 DoH 解析器也返回污染结果（[S4](https://netintum.de/fileadmin/TUM/NET/NET-2023-06-1.pdf) [S5](https://www.ipdodo.com/news/16580/)） |
| Docker Desktop 忽略 daemon.json | daemon.json 配了代理不生效 | Docker Desktop 需在设置 GUI 里配代理，不走 daemon.json（[S7](https://docs.docker.com/engine/daemon/proxy/)） |

> [!tip] 大白话
> postBuffer 误区就像「把水桶换大，但水龙头那头根本没水」——传输链路断了，调桶的尺寸没用。先诊断链路，再决定调哪里。

**未决问题**（暂未在素材中定论，使用前需自行确认）：
- 用户侧是否已有可用代理及端口——决定走第④步还是第⑤步（[S6](https://stackoverflow.com/questions/15240815/) [S15](https://github.com/suiyueqingqian/gh-proxy) 相关）。
- Docker 公共加速器 2026-08 的实际可用清单（需实测，文中仅推断）。
- pnpm 与 npm 共用 `.npmrc` 的 `proxy` 键是否仍成立（社区惯例，未在官方源验证）。
- `git://` 协议（`core.gitProxy`）在 GitHub 移除 `git://` 支持后是否还有现实意义。

## 本章小结

- 遇到超时先走五步决策：排除 GitHub 故障 → 定位卡点 → 快速分类 → 有代理走代理 → 无代理走镜像 + hosts。
- 五类方案中，代理与镜像适合长期与自动化；hosts 与 gh-proxy 只作临时应急。
- 五个高频坑：postBuffer 误区、环境变量大小写不一致、`GIT_CURL_VERBOSE` 旧名、公共 DNS 被劫持、Docker Desktop 忽略 daemon.json。
- 若干未决问题（代理可用性、Docker 加速器现状、pnpm 共享键、`git://` 意义）留待实操中确认。

---

## 脚注

[^c1-1]: GitHub Status 官方状态页 — https://www.githubstatus.com/
[^c1-2]: Git 官方手册 git(1)，环境变量/跟踪 — https://git-scm.com/docs/git
[^c1-3]: git-config 官方文档 — https://git-scm.com/docs/git-config
[^c1-4]: ipdodo《GitHub 无法访问？2026 开发者终极网络抢救指南》— https://www.ipdodo.com/news/16580/
[^c1-5]: StackOverflow Q15240815 — remote end hung up — https://stackoverflow.com/questions/15240815/
[^c2-s4]: TUM 学术综述《Survey on the Chinese Government's Censorship Mechanisms》(2023-06)，https://netintum.de/fileadmin/TUM/NET/NET-2023-06-1.pdf
[^c2-s5]: ipdodo《GitHub 无法访问？2026 开发者终极网络抢救指南》(2026-03)，https://www.ipdodo.com/news/16580/
