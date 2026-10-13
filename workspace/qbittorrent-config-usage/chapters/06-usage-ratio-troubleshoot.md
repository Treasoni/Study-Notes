## 第 6 章 用起来（下）：分享率、H&R 与「没速度」排查

前两章已经会加种、会找同伴了。这一章收尾两件私种用户最挂心的事：**分享率 / H&R**（做完种子要「还债」），以及下载**没速度**时怎么按官方顺序自查。一句话看懂：分享率 / H&R 是**私种通用的机制**，不是某一站的规则；没速度时**别乱调参数**，按官方那张清单逐项报。

### 6.1 结论先行

| 问题 | 一句话 |
| --- | --- |
| 分享率为什么难维持 | 往往不是你的错：资源天生向「带宽大的少数人」倾斜（6.2，F9） |
| H&R 是什么 | 「下完就跑」——没还够债就撤种（6.3） |
| 没速度怎么办 | 按官方清单实测 + 逐项报，而不是抄「万能参数」（6.4，G1） |

> [!warning] 先说边界
> 本章讲的是**通用机制**，不是任何具体站的规则，也不给出任何站的达标线。**具体阈值一律以你目标站的 rules / FAQ 为准。**

### 6.2 分享率为什么「难」：credit crunch（F9）

把分享率想成**一个水池**：你下载是「舀走水」，上传是「倒回水」，分享率就是「倒回 ÷ 舀走」。直觉上人人努力就能维持在 1 附近——但研究结论恰恰相反：

| 官方原文 | 说人话 |
| --- | --- |
| 「Statistically, it is simply impossible for all members of a private BitTorrent tracker to maintain an upload/download ratio close to 1.」[^c6-lc6-8] | 从统计上讲，一个私种的所有成员**不可能**都维持在接近 1 的分享率。 |

而且，就连更宽松的比例（例如 0.4 或更低）对新用户也可能难以维持[^c6-lc6-8]。

原因在结构，不在个人：荷兰代尔夫特理工大学的 Tribler 团队专门研究过私种的「比率经济」[^c6-lc6-9]，发现少数「带宽大的 peers」（常配有 seedbox）会拿走不成比例的上传「额度」，新用户 / 弱用户就更难达标[^c6-lc6-10]。研究者把这种现象称作 **credit crunch**（信用紧缩）[^c6-lc6-11]。

连 BitTorrent 协议的作者 Bram Cohen 也质疑唯分享率论：

| 官方原文 | 说人话 |
| --- | --- |
| 「A better approach would be to not count it against people when they download from heavily overseeded torrents.」[^c6-lc6-14] | 更好的做法是：当用户从「种子极多」的资源下载时，**不要把这算成他的负担**。 |

这也解释了为什么不少社区改用别的口径（如「做种奖励」或「总做种时长」）[^c6-lc6-15]。

> [!tip] 大白话
> 分享率像**班级平均分**：全班不可能人人考第一。资源天生向「带宽大的少数人」倾斜，所以「比例难看」常常不是你不努力，而是结构如此。

### 6.3 H&R 与最低做种时长：通用机制（F9）

**H&R（hit-and-run）**＝「下完就跑」：下完立刻撤种、不再做种[^c6-lc7-8]。私种靠它维持资源存活。判定通常看**两个基准**，满足任一即可清除[^c6-lc7-10]：

| 基准 | 通用口径（以目标站为准） |
| --- | --- |
| 时长基准 | 连续或累计做种一段时间，**常见区间为 24–72 小时**[^c6-lc7-11] |
| 比例基准 | 上传量达到下载量的一定比例，**通常为 1:1**[^c6-lc7-12] |

来源的说法是「满足任一条件，通常就清掉 H&R 风险」[^c6-lc7-15]。

> [!tip] 大白话
> H&R 像**借了书不还**：下载是「借」，做种是「还」。只要你还够时间，或者还够「与借出等量」（1:1），就算清账——满足其一即可。

**会先给缓冲**：多数站不会一发现撤种就封号，而是先给一个**宽限期（常见 24–48 小时）**并发通知[^c6-lc7-17]；在窗口内重新做种、补齐时数或上传量，标记会自动清除、不受罚[^c6-lc7-18]。

**累犯才逐级加重**：宽限期过了仍未解决，处罚会升级——记 strike（常见「三振」模式）[^c6-lc7-21] → 扣积分 / 花积分赎[^c6-lc7-22] → 禁下载（leech ban）[^c6-lc7-23] → 降级[^c6-lc7-24] → 永久封号[^c6-lc7-25]。

**怎么补救**：把文件重新挂上做种（re-seed）[^c6-lc7-30]，或用手里的积分抵消这次 strike[^c6-lc7-31]。

**最低做种时长**是 H&R 背后的那条线：多数现代私种的「标准最低做种时长」常写成 48–72 小时（2–3 天）[^c6-lc8-10]；普通种子常见 24–72 小时[^c6-lc8-11]，大文件 / 整季包可能要到 5–14 天[^c6-lc8-12]。这条线通常**可累计**：

| 官方原文 | 说人话 |
| --- | --- |
| 「This time is typically cumulative, meaning a user does not need to seed continuously in one uninterrupted session, but the total active seeding hours must meet the requirement within a specified timeframe (such as within 7 to 14 days of completion).」[^c6-lc8-16] | 这个时长通常可**累计**——不必一次不间断做种，只要在规定时间窗（如完成后 7–14 天内）把有效做种时数累够即可。 |

它同样遵循「时长或比例满足其一」的双条件[^c6-lc8-19]（做满时长[^c6-lc8-20]，或达到 1:1[^c6-lc8-21]）；超出最低时长仍继续做种，还能攒积分[^c6-lc8-27]。此外，用户等级越高，要求的时长往往越短[^c6-lc8-13]。

> [!warning] 数字只是「常见区间」
> 上面所有数字都是来源里的「常见 / 通常」区间，**不是硬性标准**；**你目标站的实际要求以它的 rules / FAQ 为准**。

### 6.4 没速度怎么办：按官方清单自查（G1）

下载没速度时，最容易犯的错是**照抄网上的「万能参数」**。qB 官方的态度正好相反：**先实测，再逐项报**。

**第一步：测出你的真实带宽**

| 官方原文 | 说人话 |
| --- | --- |
| 「What your ISP has sold you is irrelevant, to calculate a starting place for settings requires a real time check of bandwidth/speed capability.」[^c6-lc2-14] | 你的 ISP 卖给你多少带宽无关紧要；要算出设置的起点，必须实时测一次带宽 / 速度能力。 |

怎么测：**关掉所有正在跑的 BT 客户端**，用浏览器打开 Speedtest.net 跑一轮，并截图[^c6-lc2-16]。

**第二步：确认版本够新**

> [!warning] 先升级，再提问
> 官方明确要求：提问前先确认自己用的是**该 OS 的最新版**（旧版不在支持范围内）[^c6-lc2-18]。

**第三步：准备好「线索清单」**——官方要你提供的设置信息包括[^c6-lc2-20]：

| 官方原文 | 中译 |
| --- | --- |
| `Connections: Global maximum and per torrent`[^c6-lc2-20] | 连接数：全局最大值与每任务最大值 |
| `Listening port`[^c6-lc2-21] | 监听端口 |
| `Upload slots: Global maximum and per torrent`[^c6-lc2-22] | 上传槽位：全局最大值与每任务最大值 |
| `Half-open connection value`[^c6-lc2-23] | 半开连接数 |
| `Is uTP on or off?` / `Rate limiting uTP?`[^c6-lc2-24] | uTP 开关 / 是否限速 uTP（两问） |
| `Encryption on or off?`[^c6-lc2-26] / `IPv6 on or off?`[^c6-lc2-27] | 加密、IPv6 开关 |
| `libtorrent version`[^c6-lc2-28] / `Connection status?`[^c6-lc2-29] / `DHT node count`[^c6-lc2-30] | libtorrent 版本、连接状态、DHT 节点数 |
| `Are you using a proxy or a VPN?`[^c6-lc2-31] | 是否使用了代理 / VPN |

若某个**具体任务**有问题，还要另外报它的状态、seed / peer 计数、tracker 状态[^c6-lc2-42][^c6-lc2-43][^c6-lc2-44]。

**第四步：上传截图前先打码**

> [!warning] 隐私红线
> 截图前请**隐藏任务名列 / 打码**名与哈希，并抹掉私种 URI 里的 `access key`[^c6-lc2-47]；官方还明确**不要**贴非开源 / 非公有领域资源的 `.torrent` URI 或磁力链接[^c6-lc2-48]。

**如果症状是「完全连不上、没人来连」**

那多半是**端口没通**。以同类客户端的 ArchWiki 说法：BT 至少要有一个 TCP 和一个 UDP 端口对外开放，才能接受入站连接[^c6-lc3-69]；在 NAT / 防火墙后还需要把对应端口**转发**进去（UPnP 也可用，但它与「本机防火墙需要固定端口」的机制相冲突）[^c6-lc3-77]。另外，Linux 上若用 iptables 的 conntrack，有时会把大量**合法的 DHT 流量**当成 INVALID 丢掉，症状是「做种尤其是开着 DHT 时不出量」[^c6-lc3-79]。

> [!warning] 这条来自 Deluge，不是 qB（F10）
> 上面端口 / NAT / conntrack 三条**出自 Deluge 的 ArchWiki**，**不是 qBittorrent 的一手来源**，只作通用原理参考。端口号本身以你的配置为准：qB 官方 Docker 镜像的 torrenting 端口默认是 `6881`[^c6-la1-60]；linuxserver 镜像的端口映射示例里，`8080` 用于 WebUI[^c6-la2-91]。

> [!tip] 大白话
> 报「线索」像**去医院看病**：医生要先看你的化验单（实测带宽）和病史（版本、设置），才敢开方；你只喊一句「我头晕」，谁也帮不了你。

### 收束：你现在会了什么

- **装**：官方镜像与 linuxserver 镜像两条路，容器与目录都能跑起来。
- **配**：端口、下载路径、硬链接口径，再往下是分类 / 标签 / 限速 / 代理 / **完成回调**。
- **用**：加种、Tracker、DHT/PeX/LPD；分享率 / H&R 通用机制；没速度时按官方清单自查。
- 一条贯穿全册的纪律：**参数与阈值以官方文档或你自己的实测为准**，不抄「万能值」，也不拿某站的规则当通用标准。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文**成句**引文，逐字原文与中译对照如下（字段 / 键名类英文按规范保留原文，已在正文就地给中译，不重复入表）。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Statistically, it is simply impossible for all members of a private BitTorrent tracker to maintain an upload/download ratio close to 1.` | 从统计上讲，一个私种的所有成员不可能都维持在接近 1 的分享率。 | `LC-6 · sources/l3-6_torrentfreak-credit-crunch.md:8` |
| 2 | `A better approach would be to not count it against people when they download from heavily overseeded torrents.` | 更好的做法是：当用户从「种子极多」的资源下载时，不要把这算成他的负担。 | `LC-6 · sources/l3-6_torrentfreak-credit-crunch.md:14` |
| 3 | `Seeding the completed download continuously or cumulatively for a set duration (commonly between 24 and 72 hours).` | 连续或累计地做种一段设定时长（常见为 24 至 72 小时）。 | `LC-7 · sources/l3-7_hit-and-run-penalties.md:11` |
| 4 | `Uploading a specific amount of data relative to what was downloaded, typically reaching a 1:1 ratio.` | 上传相对于已下载的一定数据量，通常要达到 1:1 的比例。 | `LC-7 · sources/l3-7_hit-and-run-penalties.md:12` |
| 5 | `Fulfilling either condition usually clears the torrent of any HnR risk.` | 满足其中任一条件，通常就能清除该种子的 H&R 风险。 | `LC-7 · sources/l3-7_hit-and-run-penalties.md:15` |
| 6 | `This time is typically cumulative, meaning a user does not need to seed continuously in one uninterrupted session, but the total active seeding hours must meet the requirement within a specified timeframe (such as within 7 to 14 days of completion).` | 这个时长通常可累计——不必一次不间断做种，只要在规定时间窗（如完成后 7 至 14 天内）把有效做种时数累够即可。 | `LC-8 · sources/l3-8_minimum-seed-time.md:16` |
| 7 | `What your ISP has sold you is irrelevant, to calculate a starting place for settings requires a real time check of bandwidth/speed capability.` | 你的 ISP 卖给你多少带宽无关紧要；要算出设置的起点，必须实时测一次带宽 / 速度能力。 | `LC-2 · sources/l3-2_speed-issues.md:14` |
| 8 | `Turn off any and all BitTorrent clients that are running, open Speedtest.net in a browser, run the test(s), then provide a screen shot of the results in your post.` | 关掉所有正在运行的 BT 客户端，用浏览器打开 Speedtest.net 跑测试，然后把你帖子里附上结果截图。 | `LC-2 · sources/l3-2_speed-issues.md:16` |
| 9 | `Also before asking, please ensure that you are using the latest release for your OS.` | 另外在提问之前，请先确认你用的是该操作系统的最新版。 | `LC-2 · sources/l3-2_speed-issues.md:18` |

## 脚注

[^c6-lc6-8]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:8`（不可能所有成员都维持接近 1 的分享率）。
[^c6-lc6-9]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:9`（代尔夫特理工 Tribler 团队研究比率经济）。
[^c6-lc6-10]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:10`（比率体系向少数大带宽 peers 倾斜）。
[^c6-lc6-11]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:11`（`credit crunch` 一词）。
[^c6-lc6-14]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:14`（Bram Cohen 反对唯分享率论）。
[^c6-lc6-15]: LC-6 · `sources/l3-6_torrentfreak-credit-crunch.md:15`（做种奖励 / 总做种时长等替代口径）。
[^c6-lc7-8]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:8`（H&R 的定义）。
[^c6-lc7-10]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:10`（两个判定基准）。
[^c6-lc7-11]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:11`（时长基准）。
[^c6-lc7-12]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:12`（比例基准）。
[^c6-lc7-15]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:15`（满足其一即清除）。
[^c6-lc7-17]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:17`（宽限期常见 24–48 小时）。
[^c6-lc7-18]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:18`（窗口内补齐则标记自动清除）。
[^c6-lc7-21]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:21`（记 strike，「三振」模式）。
[^c6-lc7-22]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:22`（扣积分 / 花积分赎回）。
[^c6-lc7-23]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:23`（禁下载 `leech ban`）。
[^c6-lc7-24]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:24`（账户降级）。
[^c6-lc7-25]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:25`（永久封号）。
[^c6-lc7-30]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:30`（重新做种 re-seeding）。
[^c6-lc7-31]: LC-7 · `sources/l3-7_hit-and-run-penalties.md:31`（用积分抵消 strike）。
[^c6-lc8-10]: LC-8 · `sources/l3-8_minimum-seed-time.md:10`（标准最低做种时长常见 48–72 小时）。
[^c6-lc8-11]: LC-8 · `sources/l3-8_minimum-seed-time.md:11`（普通种子 24–72 小时）。
[^c6-lc8-12]: LC-8 · `sources/l3-8_minimum-seed-time.md:12`（大文件 / 整季包 5–14 天）。
[^c6-lc8-13]: LC-8 · `sources/l3-8_minimum-seed-time.md:13`（用户等级越高要求越短）。
[^c6-lc8-16]: LC-8 · `sources/l3-8_minimum-seed-time.md:16`（时长可累计，须在规定窗口内）。
[^c6-lc8-19]: LC-8 · `sources/l3-8_minimum-seed-time.md:19`（双条件规则）。
[^c6-lc8-20]: LC-8 · `sources/l3-8_minimum-seed-time.md:20`（做满最低时长）。
[^c6-lc8-21]: LC-8 · `sources/l3-8_minimum-seed-time.md:21`（达 1:1 比例）。
[^c6-lc8-27]: LC-8 · `sources/l3-8_minimum-seed-time.md:27`（持续做种可攒积分）。
[^c6-lc2-14]: LC-2 · `sources/l3-2_speed-issues.md:14`（先实时测带宽，再定设置起点）。
[^c6-lc2-16]: LC-2 · `sources/l3-2_speed-issues.md:16`（关掉客户端、用 Speedtest.net 测速并截图）。
[^c6-lc2-18]: LC-2 · `sources/l3-2_speed-issues.md:18`（提问前确认用该 OS 最新版）。
[^c6-lc2-20]: LC-2 · `sources/l3-2_speed-issues.md:20`（线索清单首项：连接数全局 / 每任务）。
[^c6-lc2-21]: LC-2 · `sources/l3-2_speed-issues.md:21`（监听端口）。
[^c6-lc2-22]: LC-2 · `sources/l3-2_speed-issues.md:22`（上传槽位全局 / 每任务）。
[^c6-lc2-23]: LC-2 · `sources/l3-2_speed-issues.md:23`（半开连接数）。
[^c6-lc2-24]: LC-2 · `sources/l3-2_speed-issues.md:24-25`（uTP 两问：开关与是否限速）。
[^c6-lc2-26]: LC-2 · `sources/l3-2_speed-issues.md:26`（加密开关）。
[^c6-lc2-27]: LC-2 · `sources/l3-2_speed-issues.md:27`（IPv6 开关）。
[^c6-lc2-28]: LC-2 · `sources/l3-2_speed-issues.md:28`（libtorrent 版本）。
[^c6-lc2-29]: LC-2 · `sources/l3-2_speed-issues.md:29`（连接状态）。
[^c6-lc2-30]: LC-2 · `sources/l3-2_speed-issues.md:30`（DHT 节点数）。
[^c6-lc2-31]: LC-2 · `sources/l3-2_speed-issues.md:31`（是否使用代理 / VPN）。
[^c6-lc2-42]: LC-2 · `sources/l3-2_speed-issues.md:42`（具体任务需报其状态）。
[^c6-lc2-43]: LC-2 · `sources/l3-2_speed-issues.md:43`（seed / peer 计数）。
[^c6-lc2-44]: LC-2 · `sources/l3-2_speed-issues.md:44`（tracker 状态信息）。
[^c6-lc2-47]: LC-2 · `sources/l3-2_speed-issues.md:47`（截图前隐藏任务名 / 哈希 / `access key`）。
[^c6-lc2-48]: LC-2 · `sources/l3-2_speed-issues.md:48`（不贴非开源资源的 .torrent / 磁力链接）。
[^c6-lc3-69]: LC-3 · `sources/l3-3_archwiki-deluge.md:69`（BT 需至少一个 TCP 与一个 UDP 端口对外开放）。
[^c6-lc3-77]: LC-3 · `sources/l3-3_archwiki-deluge.md:77`（NAT / 防火墙后需转发端口；UPnP 与本机防火墙冲突）。
[^c6-lc3-79]: LC-3 · `sources/l3-3_archwiki-deluge.md:79`（conntrack 可能把合法 DHT 流量当 INVALID 丢弃）。
[^c6-la1-60]: LA-1 · `sources/l1-1_official-docker-readme.md:60`（官方镜像 torrenting 端口默认 `6881`）。
[^c6-la2-91]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:91`（linuxserver 镜像端口映射示例：`8080` 对应 WebUI）。
