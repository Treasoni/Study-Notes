## 第 1 章：SearXNG 是什么：一句话看懂 + 隐私模型

### 1.1 一句话看懂

SearXNG 是一个「替你去搜、却不记你是谁」的搜索入口：你问它一句话，它替你同时去一批搜索服务各问一遍，再把结果汇总回来给你。[^c1-a] 而在那些搜索服务眼里，来问的是 SearXNG 这台机器，不是你。

它解决的是一个很具体的问题：你照样能用全网的搜索结果，但「你搜了什么、你是谁」不必交给每一家搜索公司。往下一步说——**自托管 SearXNG，就是把中间那个「替你跑腿的人」，从别人的服务器换成你自己机器上的一个实例**。后面五章要做的，全是在把这个「实例」立起来并接进 Hermes。

### 1.2 元搜索是什么（比喻先于术语）

先把 SearXNG 想成一个**只帮你跑腿、不留姓名的前台**。

你走到前台说「查一下 XXX」。前台自己不回答，而是同时派出一批跑腿的：去 Google 的窗口问一遍、去 Bing 的窗口问一遍、去维基的窗口问一遍……把各自递回来的纸条汇总成一份，再交给你。关键就在最后这一下——那些窗口对面看到的，是「前台派来的跑腿的」，**不是站在前台后面的你**。

所以：你拿到的是「多家结果的合集」（通常比只问一家更全），而搜索公司拿不到你的账号、IP 或浏览器指纹。这就是「元搜索」的全部直觉。

正式说法是 **metasearch engine（元搜索引擎）**：它自己几乎不建索引，而是把别家搜索引擎当数据源，统一提问、再把结果聚合起来。官方给的定位原话是：

> `SearXNG is a free internet metasearch engine … Users are neither tracked nor profiled.`[^c1-a]
> 中译：SearXNG 是一个免费的互联网元搜索引擎……用户既不被追踪，也不被画像。

> [!tip] 大白话
> 把 SearXNG 想成「一个只替你跑腿、不留姓名的前台」：好处是你一次能问到好几家，坏处是结果全要经过它转手——**所以接下来第 2 章才会强调「这台前台得是你自己的」**。

### 1.3 隐私模型：三次「脱敏」

SearXNG 保护隐私的总做法，官方概括成一句：把私人数据从「搜索请求」里**脱敏**，分三种形式来做。[^c1-b] 其中最日常的一条是——它**不把 cookie 发给外部搜索引擎，并且每个请求都换一个随机浏览器指纹**（browser profile）。[^c1-c] 也正因如此，请求是公共实例还是自建实例发的都无所谓，因为两种情况下它都已经匿名化了。[^c1-c]

还有一层容易被忽略：**出口 IP 用的是实例的 IP，不是你家的 IP**；官方也允许把这台实例再挂到代理或 Tor 后面。[^c1-d]

下面把「同一句搜索，各方分别看得见什么」摊开：

| 你的做法 | 搜索服务（Google / Bing 等）看得见 | 实例管理员看得见 |
| --- | --- | --- |
| 直接用普通搜索引擎 | 你的 IP、账号、cookie、查询词，也就是「你本人」 | （没有这个角色） |
| 走公共 SearXNG 实例 | 实例的 IP + 随机浏览器指纹，而不是「你」 | 你的查询词——你得信任这位管理员[^c1-e] |
| 自建 SearXNG 实例 | 实例的 IP + 随机浏览器指纹，而不是「你」 | 你的查询词，但这位管理员就是你自己 |

一句话概括：**三种做法里，搜索服务都只看到「实例」；差别只在中间那位管理员是不是你。**

> [!tip] 大白话
> 「脱敏」就是**寄信前把信封上你的地址撕掉、只留寄信局的地址**。收信人（Google）能收到信、能回信，但不知道其实是你写的；唯一还知道是你的人，是经手这封信的邮局——**所以邮局是谁，很重要**。

### 1.4 自建还是用别人的实例（谁值得信任）

看完上面那张表，取舍点就清楚了：公共实例的问题不在技术，而在**信任**。官方直说，用公共实例就必须信任它的管理员——你无从知道他有没有把你的请求记录、聚合甚至卖给别人。[^c1-e] 而一旦自建，「一切都在你手里：源代码、日志设置和私人数据」，也就不必再去信任任何陌生的管理员。[^c1-f]

补一个常被追问的规模问题：**SearXNG 本体目前支持 261 个搜索引擎，其中 81 个默认启用**。[^c1-g] 这两个数字只描述 SearXNG 本体；Hermes 文档另有一个口径不同的引擎数，留到第 4 章再说，**两者不要合并成一个数**。

它的许可方式是 **AGPL-3.0**：本项目以 GNU Affero 通用公共许可证授权。[^c1-h] 对自托管者来说，这意味着源码可查、可自行审阅。

> [!tip] 大白话
> 用公共实例像**借邻居家的 Wi-Fi 上网**——凑合能用，但流量从谁的路由器过，你并不清楚。自建则是自己拉一条线：麻烦一点，可这台路由器是你的。

### 1.5 名词扫盲表

| 名词 | 一句话解释 |
| --- | --- |
| 元搜索（metasearch） | 自己不建索引，转问别家再汇总结果——「替你跑腿的前台」 |
| 聚合器（aggregator） | 把多家结果合并成一份统一结果的组件 |
| 实例（instance） | 跑起来的一个 SearXNG 服务；公共实例人人可用，自建实例只有你能用 |
| 脱敏 | 把请求里的私人数据（cookie、指纹等）抹掉再转发 |
| AGPL-3.0 | 一种强 copyleft 开源许可：改动过、并对外提供服务的代码也要开源 |
| Tor | 一种匿名网络；SearXNG 可让出口流量经它转发，进一步隐藏来源 |

### 1.6 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `SearXNG is a free internet metasearch engine which aggregates results from up to … search services. Users are neither tracked nor profiled. Additionally, SearXNG can be used over Tor for online anonymity.` | SearXNG 是一个免费的互联网元搜索引擎，聚合来自多达若干家搜索服务的结果；用户既不被追踪，也不被画像；此外它还能经由 Tor 使用，以实现匿名。 | L1-1 · sources/l1-1_searxng-docs-index.rst:9-12 |
| 2 | `Removal of private data from search requests comes in three forms:` | 从搜索请求中移除私人数据，有三种形式。 | L1-2 · sources/l1-2_own-instance.rst:26 |
| 3 | `Removing private data means not sending cookies to external search engines and generating a random browser profile for every request. Thus, it does not matter if a public or private instance handles the request, because it is anonymized in both cases.` | 脱敏意味着不向外部搜索引擎发送 cookie，并为每个请求生成一个随机浏览器指纹；因此请求由公共还是私有实例处理都一样，因为两种情况都已匿名化。 | L1-2 · sources/l1-2_own-instance.rst:33-35 |
| 4 | `The IP address used will be the IP of the instance, but SearXNG can also be configured to use proxy or Tor.` | 使用的 IP 将是实例的 IP，但 SearXNG 也可配置为走代理或 Tor。 | L1-2 · sources/l1-2_own-instance.rst:36-37 |
| 5 | `If someone uses a public instance, they have to trust the administrator of that instance.` | 若有人使用公共实例，就必须信任该实例的管理员。 | L1-2 · sources/l1-2_own-instance.rst:48-49 |
| 6 | `everything is in their control: the source code, logging settings and private data. Unknown instance administrators do not have to be trusted.` | 一切都在他们掌控之中：源代码、日志设置与私人数据；也就不必去信任陌生的实例管理员。 | L1-2 · sources/l1-2_own-instance.rst:60-62 |
| 7 | `SearXNG supports 261 search engines of which 81 are enabled by default.` | SearXNG 支持 261 个搜索引擎，其中 81 个默认启用。 | L1-3 · sources/l1-3_configured_engines.html:449-450 |
| 8 | `This project is licensed under the GNU Affero General Public License (AGPL-3.0).` | 本项目以 GNU Affero 通用公共许可证（AGPL-3.0）授权。 | L1-5 · sources/l1-5_repo-readme.rst:61 |

[^c1-a]: SearXNG Docs · 首页（`docs/index.rst`）— https://docs.searxng.org
[^c1-b]: SearXNG Docs · Why use a private instance? — https://docs.searxng.org/user/own-instance.html
[^c1-c]: 同上（`own-instance.rst:33-35`）
[^c1-d]: 同上（`own-instance.rst:36-37`）
[^c1-e]: 同上（`own-instance.rst:48-49`）
[^c1-f]: 同上（`own-instance.rst:60-62`）
[^c1-g]: SearXNG Docs · Configured Engines — https://docs.searxng.org/user/configured_engines.html
[^c1-h]: 上游 `searxng/searxng` README — https://github.com/searxng/searxng
