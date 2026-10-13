## 第 5 章 用起来（上）：加种、Tracker、DHT/PeX/LPD 与 RSS

前四章把 qBittorrent 装好、配好、能自动收尾了。这一章开始「用起来」：把资源**加进来**，再解决 BT 下载的两件事——**找到别人**、**被别人找到**。一句话看懂：加种靠 `.torrent` 文件或磁力链接，找人靠 Tracker（以及 DHT / PeX / LPD 这几种补充方式），而被找到靠一个对外的端口。

### 5.1 结论先行：加进来 → 找到人 → 被找到

| 环节 | 靠什么 | 一句话 |
| --- | --- | --- |
| 加进来 | `.torrent` 文件 / 磁力链接 | 拿到资源的「身份证」（5.2） |
| 找到人 | Tracker，以及 DHT / PeX / LPD | 几种「找同伴」的方式（5.3、5.4） |
| 被找到 | 对外的 BT 端口 | 别人才连得上你（第 3 章已配） |

> [!tip] 大白话
> 把 Tracker 想成**贴在墙上的公告栏**：你把自己的信息贴上去，也从上面读到别人的信息。DHT / PeX / LPD 则是公告栏之外的几种「打听消息」的路子。它们的准确含义以官方术语为准（见 5.4）。

### 5.2 加种：磁力链接 / torrent 文件，与「添加时」触发

加种有两种来源：`.torrent` 文件和磁力链接。先把几个绕不开的名词扫清：

| 名词 | 一句话 | 出处 |
| --- | --- | --- |
| `.torrent` 文件 | 装着种子元数据（metainfo）的文件 | LC-1[^c5-lc1-83] |
| `info_hash` | metainfo 中 info 值的 20 字节 sha1 哈希，等于该种子的「身份证」 | LC-1[^c5-lc1-83] |
| 磁力链接 | 只带这串 `info_hash`，省掉「先下 `.torrent` 再开始」的链接 | — |

qB 可以被设为打开 `.torrent` 文件 / 点击磁力链接时的默认应用[^c5-lb1-52][^c5-lb1-53]；添加时还能一并设定保存位置、标签、以及要下载哪些文件[^c5-lb1-61]。

加种时还能顺手触发一件事：qB 有一个触发点叫 `torrentAdded`（**添加时**）[^c5-lb6-124]，对应配置键 `AutoRun/OnTorrentAdded/Enabled`，**默认关闭**[^c5-lb6-145]。它和上一章的「完成时」回调是一对——一个管「刚加进来」，一个管「下完了」。

### 5.3 Tracker：公告地址与公共列表（F11）

**Tracker 是公告服务器**：你的客户端向它报到，它回给你一串同伴地址。官方对它的响应格式有明确说法：

| 官方原文 | 说人话 |
| --- | --- |
| 「Tracker responses are bencoded dictionaries.」[^c5-lc1-106] | Tracker 的响应是 bencode 编码的字典。 |

报到时会带上什么？官方 BEP3 列出的 tracker 请求的键里有 `info_hash`（种子身份证）、`peer_id`（本机在这次下载里的随机 id）、`uploaded` / `downloaded` / `left`（已上传 / 已下载 / 还差多少）等[^c5-lc1-79]；此外还带一个 `event`，取值有 `started`、`completed`、`stopped`——分别对应「刚开始下」「下完了」「停止下载」[^c5-lc1-104]。

> [!tip] 大白话
> Tracker 就像**班级点名**：你报「我是谁（`info_hash` / `peer_id`）、我下了多少、还差多少」，它就回给你「还有这些同学也在下同一份资料（peers）」。`started` / `completed` / `stopped` 就是「我来了 / 我做完了 / 我走了」。

对普通用户来说，更实用的是**公共 Tracker 列表**。本册取一个公开维护的清单为例：`ngosang/trackerslist`，自述为「公共 `BitTorrent tracker` 的更新列表」[^c5-lc4-9]，由机器人每天检查并更新[^c5-lc4-29]，且会自动去掉同域名或同 IP 的重复项[^c5-lc4-30]。它另外提供「用 IP 代替域名」的版本，供遇到 DNS 问题时使用[^c5-lc4-23]；列表条目按流行度和延迟从好到差排序[^c5-lc4-31]。

> [!warning] 列表条目数是变动值（F11）
> 这份列表**每天更新**，条目数会变。快照日（2026-10-07）的 README 里，`trackers_all` 标注为 82 条[^c5-lc4-15]——但这**不是**一个固定常量，引用时务必绑定日期，别把它当成「永远是 82」。

添加公共 Tracker 时用它的原始链接（新手可跳过）[^c5-lc4-15]：

```text
https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt
```

### 5.4 DHT / PeX / LPD：官方一句话描述，与「为什么私种要关」（G2）

除了 Tracker，qB 还有三个「额外找同伴」的开关。官方选项页对每个都给了**一句**说明[^c5-lb1-117]：

| 开关（界面名） | 官方那一句的中译 |
| --- | --- |
| `Enable DHT (decentralized network) to find more peers` | DHT 是一种让种子的下载与上传**不依赖 tracker** 的方案 |
| `Enable Peer Exchange (PeX) to find more peers` | 另一种「**降低对 tracker 依赖**」的替代方式 |
| `Enable Local Peer Discovery to find more peers` | BitTorrent 协议的扩展，用于通过**局域网**通信 |

**怎么关**：打开选项（菜单栏 `Tools` → `Options`），进入 `BitTorrent` 页，把上面三项**取消勾选**即可[^c5-lc5-11][^c5-lc5-12]。

> [!warning] 本册只搬官方那一句（G2）
> 官方对这三项各只给了**一句话**（上表就是全部），并没有展开原理。更细的「机制 / 内部原理」本册不补——**一律以官方术语为准**。

**为什么私种场景常要关**：官方那句话已经点明用处——这三项都是**在 Tracker 之外**再想办法找同伴（不依赖 Tracker）。而私种只在 Tracker 内部运作，通常要求不要把资源扩散到清单外。所以私种场景的常见做法，是把这三项关掉。

> [!warning] 这是通行要求，不是某站规则
> 「私种关 DHT / PeX / LPD」是**私种社区的通行做法，不是 qBittorrent 的官方规定，也不是某个站的官方规则**。具体是否要关、怎么关，**以你目标站的 rules / FAQ 为准**。

### 5.5 RSS：官方选项页未覆盖，来源薄弱（G7）

qBittorrent 有 RSS 功能，但**本册没有可依的官方一手说明**：官方那张按标签页分组的选项说明页，其目录里**没有 RSS 标签页**[^c5-lb1-14]（F5）。因此本册对 RSS **点到为止**，不展开细节——若你需要 RSS 自动下载，请先在你的界面里找到它的功能入口，再参照你所用版本的官方文档。

### 本章小结

- 加种、找人、被找到三步；`.torrent` 文件带 metainfo，磁力链接只带 `info_hash`[^c5-lc1-83]。
- Tracker 是公告服务器，响应是 bencoded 字典[^c5-lc1-106]；公共列表由机器人每日更新[^c5-lc4-29]，**条目数是变动值**（F11），引用要绑日期。
- 「添加时」有独立触发点 `torrentAdded` 与配置键 `AutoRun/OnTorrentAdded/Enabled`（默认关）[^c5-lb6-124][^c5-lb6-145]。
- DHT / PeX / LPD 是三个可关的开关[^c5-lc5-12]；定义以官方术语为准（G2），私种常见要求关掉，具体以目标站 rules / FAQ 为准。
- RSS 官方选项页未覆盖，来源薄弱（G7），本册不展开。

### 下一章预告

加种与联网讲清了，第 6 章收尾：私种最在意的**分享率 / H&R**（属通用机制，非某站规则），以及下载「没速度」时，按官方清单逐项自查的顺序。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Tracker responses are bencoded dictionaries.` | Tracker 的响应是 bencode 编码的字典。 | `LC-1 · sources/l3-1_bep3-tracker-protocol.md:106` |
| 2 | `Updated list of public BitTorrent trackers.` | 公共 BitTorrent tracker 的更新列表。 | `LC-4 · sources/l3-4_trackerslist-readme.md:9` |
| 3 | `A bot automatically checks the trackers and updates the lists.` | 一个机器人会自动检查这些 tracker 并更新列表。 | `LC-4 · sources/l3-4_trackerslist-readme.md:29` |
| 4 | `Trackers with the same domain or pointing to the same IP address are removed.` | 同域名或指向同一 IP 地址的 tracker 会被移除。 | `LC-4 · sources/l3-4_trackerslist-readme.md:30` |
| 5 | `DHT is a solution to make torrent downloading and uploading a tracker independent operation.` | DHT 是一种让种子的下载与上传不依赖 tracker 的方案。 | `LB-1 · sources/l2-1_options-explained.md:117` |
| 6 | `another alternative to enable lesser dependency on trackers.` | 另一种「降低对 tracker 依赖」的替代方式。 | `LB-1 · sources/l2-1_options-explained.md:118` |
| 7 | `an extension to the BitTorrent protocol to enable communication via LAN.` | BitTorrent 协议的扩展，用于通过局域网通信。 | `LB-1 · sources/l2-1_options-explained.md:119` |

## 脚注

[^c5-lc1-83]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:83`（`info_hash` 为 metainfo 中 info 值的 20 字节 sha1 哈希）。
[^c5-lc1-79]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:79-102`（tracker 请求的键：`info_hash`、`peer_id`、`uploaded`、`downloaded`、`left` 等）。
[^c5-lc1-104]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:104`（`event` 取值 `started` / `completed` / `stopped`）。
[^c5-lc1-106]: LC-1 · `sources/l3-1_bep3-tracker-protocol.md:106`（Tracker 响应为 bencoded 字典）。
[^c5-lb1-52]: LB-1 · `sources/l2-1_options-explained.md:52`（可把 qB 设为打开 `.torrent` 文件的默认应用）。
[^c5-lb1-53]: LB-1 · `sources/l2-1_options-explained.md:53`（可把 qB 设为点击磁力链接时打开的默认应用）。
[^c5-lb1-61]: LB-1 · `sources/l2-1_options-explained.md:61`（添加时可设保存位置、标签、要下载的内容等选项）。
[^c5-lc4-9]: LC-4 · `sources/l3-4_trackerslist-readme.md:9`（列表自述）。
[^c5-lc4-15]: LC-4 · `sources/l3-4_trackerslist-readme.md:15`（`trackers_all` 一行：快照日标注 82 条，并给出 `trackers_all.txt` 的原始链接）。
[^c5-lb1-117]: LB-1 · `sources/l2-1_options-explained.md:117-119`（三项开关的界面名与官方一句话描述）。
[^c5-lc4-29]: LC-4 · `sources/l3-4_trackerslist-readme.md:29`（机器人每日检查更新）。
[^c5-lc4-30]: LC-4 · `sources/l3-4_trackerslist-readme.md:30`（同域名 / 同 IP 会被移除）。
[^c5-lc4-23]: LC-4 · `sources/l3-4_trackerslist-readme.md:23`（提供「IP 代替域名」的列表，供 DNS 问题使用）。
[^c5-lc4-31]: LC-4 · `sources/l3-4_trackerslist-readme.md:31`（条目按流行度与延迟排序）。
[^c5-lc5-11]: LC-5 · `sources/l3-5_disable-dht-pex-lpd.md:11`（打开 `Tools` → `Options`，进 `BitTorrent` 页）。
[^c5-lc5-12]: LC-5 · `sources/l3-5_disable-dht-pex-lpd.md:12`（取消勾选三项的界面全称）。
[^c5-lb1-14]: LB-1 · `sources/l2-1_options-explained.md:14-31`（选项页目录，无 RSS 标签页）。
[^c5-lb6-124]: LB-6 · `sources/l2-6_placeholder-source.md:124`（触发点 `Application::torrentAdded`）。
[^c5-lb6-145]: LB-6 · `sources/l2-6_placeholder-source.md:145-147`（`AutoRun/OnTorrentAdded/Enabled`，默认 `false`）。
