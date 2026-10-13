## 第 4 章 配好（下）：分类、限速、代理与完成回调

上一章把端口和路径立好，容器和目录都通了。这一章让下载「**自动收尾**」——不必你守在电脑前看完再手动整理。要做到这点，配好四件东西即可：**分类与标签**（给种子贴标记）、**队列与限速**（别把带宽占满）、**代理**（需要时才用）、以及最关键的**完成回调**（下完自动通知整理端）。

### 4.1 结论先行：让下载「自动收尾」

先把要配的东西和它们所在的标签页列清：

| 要配的 | 在哪个标签页 | 作用 |
| --- | --- | --- |
| 分类与标签 | `Downloads` 与主界面分类栏 | 给种子贴标记，整理端按类入库（4.2） |
| 队列 | `BitTorrent` → `Torrent Queuing`[^c4-lb1-115][^c4-lb1-123] | 控制同时下载 / 上传的任务数（4.3） |
| 限速 | `Speed` → `Global Rate Limits`[^c4-lb1-110][^c4-lb1-111] | 给上下行带宽封顶（4.3） |
| 代理 | `Connection` → `Proxy server`[^c4-lb1-91][^c4-lb1-105] | 需要走代理时才填（4.4） |
| 完成回调 | `Downloads` → `Run an external program on torrent completion`[^c4-lb1-89] | 下完自动执行命令，通知 MoviePilot 整理（4.5） |

先记一条：这些设置项都**在同一张官方合并页里、按标签页分组**，不存在「分类页」「限速页」各自独立的官方页（F5）[^c4-lb1-11]。

> [!tip] 大白话
> 把「完成回调」想成**快递到了自动按门铃**：MoviePilot 不必一直盯着快递柜，铃一响它就来取件整理。分类 / 标签则是**给包裹贴的标签纸**——贴得好，取件人一眼就分得出该放哪个货架。

### 4.2 分类与标签：为「自动整理」铺路

两个词先分清：

| 名词 | 官方说法 | 一句话解释 |
| --- | --- | --- |
| 分类 | 「%L: Category」[^c4-lb6-35] | 一个种子归属的大类（如 Movie / TV） |
| 标签 | 「%G: Tags (separated by comma)」[^c4-lb6-36] | 可以给一个种子挂多个，逗号分隔 |

它们为什么重要？因为**整理端可以「只整理带某个标签的下载」**：MoviePilot 的「下载器种子标签」设定就是这样——设了标签后，只有带对应标签的任务才会被自动整理[^c4-lb3-91]。所以给 qB 里由 MoviePilot 下发的种子统一打一个标签，能避免它去动你手动加进来的杂项。

> [!tip] 大白话
> 分类像**一个大抽屉**，标签像**抽屉里的便利贴**：一个种子只能进一个抽屉（分类），却可以贴多张便利贴（标签）。整理端说的「只看贴了某张便利贴的」，就是靠标签来筛。

（相邻选项：走 MoviePilot「目录监控」整理时，官方要求打开下载器的「为不完整文件添加扩展名」，否则文件可能没下完就被搬走[^c4-lb3-94]。）

### 4.3 队列与限速：只搬官方自查清单，不给万能值

**队列**在 `BitTorrent` 标签页的 `Torrent Queuing` 一节[^c4-lb1-115][^c4-lb1-123]，控制同时下载 / 上传的任务数。**限速**在 `Speed` 标签页的 `Global Rate Limits` 一节[^c4-lb1-110][^c4-lb1-111]，给全局上下行封顶。

这里要克制：**「该限多少、连接数设多大」没有万能值**。官方的做法是**先实测、后设值**：

| 官方原文 | 说人话 |
| --- | --- |
| 「What your ISP has sold you is irrelevant, to calculate a starting place for settings requires a real time check of bandwidth/speed capability.」[^c4-lc2-14] | 你的 ISP 卖给你多少带宽无关紧要；要算出设置的起点，必须实时测一次带宽 / 速度能力。 |

官方给出的是一张**自查清单**，而不是一套推荐数字[^c4-lc2-20]：

| 自查项 | 说明 |
| --- | --- |
| 连接数（全局 / 每任务） | 官方要你先报这两项[^c4-lc2-20] |
| 监听端口 | 就是第 3 章的 BT 端口[^c4-lc2-21] |
| 上传槽位（全局 / 每任务） | 官方要你先报这两项[^c4-lc2-22] |
| 半开连接数 | 官方要你先报[^c4-lc2-23] |
| uTP 开关 / 是否限速 uTP | 官方要你先报[^c4-lc2-24]（两问） |
| 加密、IPv6 开关 | 官方要你先报[^c4-lc2-26][^c4-lc2-27] |
| 是否用了代理 / VPN | 官方要你先报[^c4-lc2-31] |

一句话：遇到速度问题，**先测速、再逐项报**，别照抄「万能参数」。

> [!tip] 大白话
> 限速像**给水管装阀门**：开多大要看你家水压（实测带宽），别人家的开度抄不来。官方那张清单问的是「阀门、管子、接头各是什么规格」，从不给你一个「拧到 3.5 圈」的万能答案。

### 4.4 代理：接入点在这里，字段来源薄弱（标注）

代理的入口在 `Connection` → `Proxy server` 一节[^c4-lb1-91][^c4-lb1-105]：官方说明它用于「下载种子时使用代理服务器」[^c4-lb1-106]。

> [!warning] 本册不给代理的具体字段
> 代理涉及一串字段（类型、主机、端口、认证等），本册**没有 qBittorrent 一手来源**逐字给出取值。这里只给「接入点在哪」，**字段一律以官方选项页为准**。

### 4.5 完成回调：以源码占位符为准（F6/F7），与 MoviePilot 对接

这一节是整章的落点。**完成回调**＝让 qBittorrent 在种子「添加时」或「完成时」自动执行一条命令[^c4-lb1-90]：

| 官方原文 | 说人话 |
| --- | --- |
| 「You can run external programs on torrent completions.」[^c4-lb2-12] | 你可以在种子**下载完成**时运行外部程序。 |
| 「This allows you to run a program on finishing certain types of torrents in a certain location.」[^c4-lb1-90] | 它让你在「某些类型、某个位置」的种子**完成时**运行一个程序。 |

**先讲一个坑（F7）**：官网 wiki 与源码不同步。官网 wiki 只描述了「完成时运行」一个入口；而 **master 源码的界面早已拆成两个**——`Run on torrent added:` 和 `Run on torrent finished:`[^c4-lb6-221][^c4-lb6-239]。**以源码为准**：版本够新时，你会看到两个开关，而不是一个。

**再讲占位符（F6）**：命令里可以用占位符引用种子的信息。**占位符以源码为准**——官方两个 wiki 页面都不列它们，定义在源码里，共 13 个、**大小写敏感**[^c4-lb6-33]。常用几个：

| 占位符 | 含义 | 出处 |
| --- | --- | --- |
| `%N` | 种子名称 | LB-6[^c4-lb6-34] |
| `%L` | 分类 | LB-6[^c4-lb6-35] |
| `%G` | 标签（逗号分隔） | LB-6[^c4-lb6-36] |
| `%F` | 内容路径 | LB-6[^c4-lb6-37] |
| `%D` | 保存路径 | LB-6[^c4-lb6-39] |
| `%Z` | 种子大小（字节） | LB-6[^c4-lb6-41] |

> [!warning] 用小写会静默失效
> 占位符**大小写敏感**：`%n` 不是 `%N`。写错不会报错，只会原样输出或替换失败——所以照抄时连大小写一起抄。

**触发点**也有两个：`torrentAdded`（添加时）与 `torrentFinished`（完成时）[^c4-lb6-124][^c4-lb6-133]。MoviePilot 的用法就是填在**完成回调**里，下完立即通知它整理入库[^c4-lb3-15]。

**回调地址填什么（G4）**：本册**没有一手来源**规定容器里该填宿主地址还是容器名，所以给你两种情形的判断方法，不写死：

| 情形 | 填什么 |
| --- | --- |
| qB 与 MoviePilot 在**同一个 compose 网络** | 用 MoviePilot 的**服务名**当主机名 |
| 两者**不在同一网络**（或其中一个是独立部署） | 填一台**双方都能访问**的宿主机地址 |

`localhost` / `127.0.0.1` 在容器里通常**指的是容器自己**，多数情况下填不通。

> [!tip] 大白话
> 回调地址像**给门铃接线**：两个人在同一栋楼（同一 compose 网络），喊门牌号（服务名）就行；分在两栋楼，就得写一个双方都找得到的**街道地址**（宿主 IP），而不是各自屋里的「我这间房」（`localhost`）。

### 4.6 动手实践（新手可跳过）

> [!tip] 新手可跳过
> 这一节是可以直接照填的内容；不打算配回调的读者可跳过。

**① 填进「完成回调」的命令**（地址、端口、token 按实际调整）[^c4-lb3-15]：

```shell
curl "http://<MoviePilot地址>:3000/api/v1/transfer/now?token=moviepilot"
```

**② 用占位符引用种子信息**：写成命令参数时，**用引号把占位符包起来**，否则遇空格会被截断[^c4-lb6-47]。例如把种子名传给脚本：

```shell
/scripts/on-finish.sh "%N"
```

**③ 对应的配置键**（写在 `qBittorrent.conf` 里时）：完成回调的开关键是 `AutoRun/enabled`、命令键是 `AutoRun/program`[^c4-lb6-171][^c4-lb6-184]；「添加时」的开关是 `AutoRun/OnTorrentAdded/Enabled`、命令是 `AutoRun/OnTorrentAdded/Program`[^c4-lb6-145][^c4-lb6-158]。两个开关的**默认值都是 `false`**（默认不开）[^c4-lb6-171][^c4-lb6-145]。

```ini
# qBittorrent.conf（片段）
[AutoRun]
enabled=true
program=curl "http://<MoviePilot地址>:3000/api/v1/transfer/now?token=moviepilot"
```

**④ 若回调是一个脚本**：别忘了给它执行权限[^c4-lb2-14]：

```shell
chmod 755 /path/to/script
```

> [!warning] 别把种子名直接拼进 shell
> qBittorrent 默认**不给外部程序注入 shell 环境**，正是为了防止「用种子名做命令注入」——源码注释里写得很清楚[^c4-lb6-54]。所以别写 `sh -c "... %N ..."` 这类把不可信字符串直接拼进 shell 的命令；要处理种子名，交给脚本的参数去接。

### 本章小结

- 「自动收尾」＝配好分类与标签、队列与限速、代理、**完成回调**四件事；设置项都在同一张官方合并页里、按标签页分组（F5）。
- 分类是**一个大抽屉**，标签是**抽屉里的便利贴**；MoviePilot 可「只整理带某标签的下载」[^c4-lb3-91]。
- 限速 / 连接数**没有万能值**：官方让你先实测、再按自查清单逐项报[^c4-lc2-14]。
- 代理只给「接入点」，字段以你自己的官方选项页为准（来源薄弱，已标注）。
- 完成回调占位符**以源码为准**（13 个、大小写敏感，F6）；触发点 `torrentAdded` / `torrentFinished`；wiki 与源码不同步，**以源码为准**（F7）。
- 回调地址填宿主还是容器名没有一手来源（G4）：同网络用服务名，跨网络用双方可达的宿主地址。

### 下一章预告

下载能自动收尾了，接下来是「怎么找资源」。第 5 章讲加种、Tracker 与公共 Tracker 列表，以及 DHT / PeX / LPD 这三个「绕过 Tracker 找同伴」的开关——以及为什么私种场景常常要关掉它们。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `You can run external programs on torrent completions.` | 你可以在种子下载完成时运行外部程序。 | `LB-2 · sources/l2-2_external-programs.md:12` |
| 2 | `This allows you to run a program on finishing certain types of torrents in a certain location.` | 它让你在「某些类型、某个位置」的种子完成时运行一个程序。 | `LB-1 · sources/l2-1_options-explained.md:90` |
| 3 | `Supported parameters (case sensitive):` | 支持的参数（大小写敏感）： | `LB-6 · sources/l2-6_placeholder-source.md:33` |
| 4 | `%L: Category` | %L：分类 | `LB-6 · sources/l2-6_placeholder-source.md:35` |
| 5 | `%G: Tags (separated by comma)` | %G：标签（以逗号分隔） | `LB-6 · sources/l2-6_placeholder-source.md:36` |
| 6 | `Run on torrent added:` | 添加种子时运行： | `LB-6 · sources/l2-6_placeholder-source.md:221` |
| 7 | `Run on torrent finished:` | 种子完成时运行： | `LB-6 · sources/l2-6_placeholder-source.md:239` |

## 脚注

[^c4-lb1-11]: LB-1 · `sources/l2-1_options-explained.md:11`（设置按标签页分组，官方只有一张合并说明页）。
[^c4-lb1-89]: LB-1 · `sources/l2-1_options-explained.md:89`（`Downloads` → `Run an external program on torrent completion` 小节标题）。
[^c4-lb1-90]: LB-1 · `sources/l2-1_options-explained.md:90`（该小节说明句）。
[^c4-lb1-91]: LB-1 · `sources/l2-1_options-explained.md:91`（`Connection` 标签页标题）。
[^c4-lb1-105]: LB-1 · `sources/l2-1_options-explained.md:105`（`Proxy server` 小节标题）。
[^c4-lb1-106]: LB-1 · `sources/l2-1_options-explained.md:106`（代理用于「下载种子时使用代理服务器」）。
[^c4-lb1-110]: LB-1 · `sources/l2-1_options-explained.md:110`（`Speed` 标签页标题）。
[^c4-lb1-111]: LB-1 · `sources/l2-1_options-explained.md:111`（`Global Rate Limits` 小节）。
[^c4-lb1-115]: LB-1 · `sources/l2-1_options-explained.md:115`（`BitTorrent` 标签页标题）。
[^c4-lb1-123]: LB-1 · `sources/l2-1_options-explained.md:123`（`Torrent Queuing` 小节）。
[^c4-lb2-12]: LB-2 · `sources/l2-2_external-programs.md:12`（可在种子完成时运行外部程序；设置位于 `Options` > `Downloads`）。
[^c4-lb2-14]: LB-2 · `sources/l2-2_external-programs.md:14`（脚本需 `chmod 755 /path/to/script`）。
[^c4-lb3-15]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:15`（MoviePilot 给的完成回调 `curl ".../api/v1/transfer/now?token=..."`）。
[^c4-lb3-91]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:91`（设定「下载器种子标签」后只整理带对应标签的任务）。
[^c4-lb3-94]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:94`（目录监控需打开下载器的「为不完整文件添加扩展名」选项）。
[^c4-lb6-33]: LB-6 · `sources/l2-6_placeholder-source.md:33`（界面显示的「支持的参数（大小写敏感）」一行）。
[^c4-lb6-34]: LB-6 · `sources/l2-6_placeholder-source.md:34`（`%N: Torrent name`）。
[^c4-lb6-35]: LB-6 · `sources/l2-6_placeholder-source.md:35`（`%L: Category`）。
[^c4-lb6-36]: LB-6 · `sources/l2-6_placeholder-source.md:36`（`%G: Tags (separated by comma)`）。
[^c4-lb6-37]: LB-6 · `sources/l2-6_placeholder-source.md:37`（`%F: Content path`）。
[^c4-lb6-39]: LB-6 · `sources/l2-6_placeholder-source.md:39`（`%D: Save path`）。
[^c4-lb6-41]: LB-6 · `sources/l2-6_placeholder-source.md:41`（`%Z: Torrent size (bytes)`）。
[^c4-lb6-47]: LB-6 · `sources/l2-6_placeholder-source.md:47`（用引号包裹参数以免被空白截断）。
[^c4-lb6-54]: LB-6 · `sources/l2-6_placeholder-source.md:54`（默认不给 shell 环境，防命令注入）。
[^c4-lb6-124]: LB-6 · `sources/l2-6_placeholder-source.md:124`（触发点 `Application::torrentAdded`）。
[^c4-lb6-133]: LB-6 · `sources/l2-6_placeholder-source.md:133`（触发点 `Application::torrentFinished`）。
[^c4-lb6-145]: LB-6 · `sources/l2-6_placeholder-source.md:145-147`（`AutoRun/OnTorrentAdded/Enabled`，默认 `false`）。
[^c4-lb6-158]: LB-6 · `sources/l2-6_placeholder-source.md:158`（`AutoRun/OnTorrentAdded/Program`）。
[^c4-lb6-171]: LB-6 · `sources/l2-6_placeholder-source.md:171`（`AutoRun/enabled`，默认 `false`）。
[^c4-lb6-184]: LB-6 · `sources/l2-6_placeholder-source.md:184`（`AutoRun/program`）。
[^c4-lb6-221]: LB-6 · `sources/l2-6_placeholder-source.md:221`（UI 标题 `Run on torrent added:`）。
[^c4-lb6-239]: LB-6 · `sources/l2-6_placeholder-source.md:239`（UI 标题 `Run on torrent finished:`）。
[^c4-lc2-14]: LC-2 · `sources/l3-2_speed-issues.md:14`（先实时测带宽，再定设置起点）。
[^c4-lc2-20]: LC-2 · `sources/l3-2_speed-issues.md:20`（自查项：连接数全局 / 每任务）。
[^c4-lc2-21]: LC-2 · `sources/l3-2_speed-issues.md:21`（自查项：监听端口）。
[^c4-lc2-22]: LC-2 · `sources/l3-2_speed-issues.md:22`（自查项：上传槽位全局 / 每任务）。
[^c4-lc2-23]: LC-2 · `sources/l3-2_speed-issues.md:23`（自查项：半开连接数）。
[^c4-lc2-24]: LC-2 · `sources/l3-2_speed-issues.md:24-25`（自查项两问：`Is uTP on or off?` 与 `Rate limiting uTP?`）。
[^c4-lc2-26]: LC-2 · `sources/l3-2_speed-issues.md:26`（自查项：加密开关）。
[^c4-lc2-27]: LC-2 · `sources/l3-2_speed-issues.md:27`（自查项：IPv6 开关）。
[^c4-lc2-31]: LC-2 · `sources/l3-2_speed-issues.md:31`（自查项：是否使用代理 / VPN）。
