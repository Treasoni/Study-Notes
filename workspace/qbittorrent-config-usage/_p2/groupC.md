## 组 C：使用与排错

### LC-1 · The BitTorrent Protocol Specification (BEP 3)
- 文件: `sources/l3-1_bep3-tracker-protocol.md` ｜ tier: 官方（bittorrent.org 规范） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - BEP 3 定义 BitTorrent 的实体构成：普通 web 服务器、静态 metainfo 文件、tracker、源下载者、终端浏览器与终端下载者。 ｜ `sources/l3-1_bep3-tracker-protocol.md:23`
  - Tracker GET 请求 `info_hash` 是 metainfo 中 info 值 bencode 形式的 20 字节 sha1 哈希，几乎必然需要转义。 ｜ `sources/l3-1_bep3-tracker-protocol.md:81`
  - `peer_id` 是长度 20 的字符串，每个下载者在开始新下载时随机生成自己的 id。 ｜ `sources/l3-1_bep3-tracker-protocol.md:86`
  - `ip` 是可选参数，给出该 peer 所在 IP 或 dns 名，一般用于与 tracker 同机的源。 ｜ `sources/l3-1_bep3-tracker-protocol.md:89`
  - `port` 是 peer 监听的端口号；常见行为是先试 6881，被占用再试 6882、6883……到 6889 后放弃。 ｜ `sources/l3-1_bep3-tracker-protocol.md:92`
  - `uploaded`／`downloaded`／`left` 均以十进制 ascii 编码；`left` 是尚需下载的字节数，不能由 downloaded 与文件长度反推（可能是续传，且可能因校验失败重下）。 ｜ `sources/l3-1_bep3-tracker-protocol.md:95,98,101`
  - `event` 可选取值 `started`／`completed`／`stopped`／`empty`；`started` 在下载首次开始时发，`completed` 在下载完成时发（若开始即完整则不发），`stopped` 在停止下载时发。 ｜ `sources/l3-1_bep3-tracker-protocol.md:104`
  - Tracker 响应是 bencode 字典：失败时有 `failure reason`（人类可读字符串，无需其他键）；成功则必有 `interval`（秒，两次常规重请求间隔）与 `peers`，peers 每项含 `peer id`、`ip`、`port`。 ｜ `sources/l3-1_bep3-tracker-protocol.md:106`
  - 更常见的是 tracker 返回紧凑 peer 列表，见 BEP 23；也常见走 UDP tracker 协议（BEP 15）。 ｜ `sources/l3-1_bep3-tracker-protocol.md:107,109`
  - metainfo 必含 `announce`（tracker URL）与 `info` 字典；`piece length` 几乎总是 2 的幂，最常见 2^18=256 K（3.2 之前默认 2^20=1 M）；`pieces` 长度是 20 的倍数，每 20 字节是该 piece 的 SHA1。 ｜ `sources/l3-1_bep3-tracker-protocol.md:62,65,70,71`
  - peer 协议握手以十进制字符 19 开头、后接字符串 `BitTorrent protocol`；其后 8 字节保留位当前全为 0；数据用 4 字节大端整数。 ｜ `sources/l3-1_bep3-tracker-protocol.md:118,119,120`
  - peer 消息类型字节：0 choke、1 unchoke、2 interested、3 not interested、4 have、5 bitfield、6 request、7 piece、8 cancel。 ｜ `sources/l3-1_bep3-tracker-protocol.md:127`
  - `request` 含 index/begin/length，长度通常为 2 的幂；当前所有实现用 2^14（16 kiB），并会关闭请求量超过该值的连接。 ｜ `sources/l3-1_bep3-tracker-protocol.md:141`
  - 现役 choke 算法每 10 秒才改变一次 choke 集合，按下载速率 unchoke 4 个最感兴趣的 peer；乐观 unchoke 每 30 秒轮换一次。 ｜ `sources/l3-1_bep3-tracker-protocol.md:148,149`
  - 零长度消息为 keepalive 并被忽略，一般每两分钟发一次。 ｜ `sources/l3-1_bep3-tracker-protocol.md:123`
- 关键实体（端口/路径/阈值等，逐字）: 端口 `6881`→`6882`/`6883`…`6889`；`peer_id` 长度 `20`；`info_hash` = `20 byte sha1`；piece length `2 18 = 256 K` / `2 20 = 1 M`；request 长度 `2^14 (16 kiB)`；choke 变更间隔 `ten seconds`；乐观 unchoke 轮换 `30 seconds`；unchoke 数量 `four peers`；keepalive `once every two minutes`；握手前导 `ninteen (decimal)` + `BitTorrent protocol`

### LC-2 · Things we need to know to help you with 'speed' issues（qBittorrent 官方 wiki）
- 文件: `sources/l3-2_speed-issues.md` ｜ tier: 官方（qBittorrent 官方 wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 该页明确：别在 wiki 里问速度问题，要到官方支持论坛 forum.qbittorrent.org 求助并附上下列信息。 ｜ `sources/l3-2_speed-issues.md:12`
  - 官方要求先关掉所有正在运行的 BitTorrent 客户端，再用 Speedtest.net 实测带宽并回贴截图；ISP 卖给你的带宽数字不作数。 ｜ `sources/l3-2_speed-issues.md:14,16`
  - 必须提供版本与操作系统，且要求先用最新版；官方声明不支持旧版 qBittorrent。 ｜ `sources/l3-2_speed-issues.md:18`
  - 需要自查/上报的设置项包括：连接数（全局与单种）、监听端口、上传槽位（全局与单种）、半开连接值、uTP 开关、uTP 限速、加密开关、IPv6 开关。 ｜ `sources/l3-2_speed-issues.md:20,21,22,23,24,25,26,27`
  - 还需报告 libtorrent 版本（Help -> About -> Libraries）、连接状态图标、状态栏的 DHT 节点数，以及是否用代理或 VPN。 ｜ `sources/l3-2_speed-issues.md:28,29,30,31`
  - 单种问题需给出：任务状态、seed/peer 计数「x(n)」形式（括号内是可能数，括号外是实际数）、tracker 状态信息。 ｜ `sources/l3-2_speed-issues.md:42,43,44`
  - 贴截图时要求隐去任务名/哈希，以及私种 URI 中的 access key；索要受版权内容种子属违规，可能导致警告或封号。 ｜ `sources/l3-2_speed-issues.md:47,48`
- 关键实体（端口/路径/阈值等，逐字）: 论坛 `http://forum.qbittorrent.org`；测速站 `http://www.speedtest.net`；版本查询 `Help -> About -> Libraries`；状态栏项 `DHT node count`；计数格式 `x(n)`
- 注: 该页正文（含 checklist）已成功取回，非 snippet-only。

### LC-3 · Deluge - ArchWiki（发行版社区 wiki）
- 文件: `sources/l3-3_archwiki-deluge.md` ｜ tier: 镜像或发行方（ArchWiki，社区维护） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - Deluge 要求至少开放一个 TCP 和 UDP 端口以接受入站连接用于做种；若提示无法为入站连接打开端口，则需自行放行端口。 ｜ `sources/l3-3_archwiki-deluge.md:69`
  - wiki 示例中放行 `56881` 到 `56889`（TCP 与 UDP 各一条 iptables 规则）。 ｜ `sources/l3-3_archwiki-deluge.md:69`
  - 处在 NAT 路由器/防火墙后的用户必须做端口转发；UPnP 也可用，但因需要预定义端口，无法与系统本地防火墙配合。 ｜ `sources/l3-3_archwiki-deluge.md:77`
  - 当 iptables conntrack 被设为丢弃 INVALID 包时，大量合法 torrent 流量（尤其 DHT 流量）会被误判丢弃；症状是长时间运行后 torrent 不再做种、DHT 开销流量持续偏低（一例中不足 3KiB/s）。 ｜ `sources/l3-3_archwiki-deluge.md:79`
  - 因此 wiki 建议关闭所有 torrent 流量的连接跟踪（NOTRACK）以获得最佳性能，并额外放行 ICMP 类型 3/4/11/12。 ｜ `sources/l3-3_archwiki-deluge.md:79,89,90,91,92`
  - 警告：端口范围写成 `1024:65535` 会破坏所有 DNS 查询。 ｜ `sources/l3-3_archwiki-deluge.md:97`
  - 守护进程默认端口为 58846，多用户同机运行需各自改动；Web UI 默认端口 8112，Web 默认密码为 `deluge`。 ｜ `sources/l3-3_archwiki-deluge.md:27,152,148`
  - 用 libtorrent 时不建议限制入站连接数，因为会限制与同一客户端保持多条连接（即使跨不同种子）的能力。 ｜ `sources/l3-3_archwiki-deluge.md:81`
- 关键实体（端口/路径/阈值等，逐字）: 做种端口示例 `56881:56889`；出站示例 `56890:57200`；守护进程端口 `58846`；Web 端口 `8112`；Web 默认密码 `deluge`；状态文件路径 `/srv/deluge/.config/deluge/state`；配置目录 `$HOME/.config/deluge/`；危险范围 `1024:65535`
- 注: 本文以 Deluge/libtorrent 为例，规则为发行版社区 wiki 描述，非 qBittorrent 官方说明。

### LC-4 · ngosang/trackerslist（公共 Tracker 列表项目）
- 文件: `sources/l3-4_trackerslist-readme.md` ｜ tier: 社区经验（第三方开源项目） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 项目定位是「Updated list of public BitTorrent trackers」，列表每日自动更新（页面标注 Last update 2026/10/07）。 ｜ `sources/l3-4_trackerslist-readme.md:9,12`
  - 提供分档列表：trackers_best 20 条、trackers_all 82 条、trackers_all_udp 51 条、trackers_all_http 19 条、trackers_all_https 12 条、trackers_all_i2p 17 条等。 ｜ `sources/l3-4_trackerslist-readme.md:14,15,16,17,18,20`
  - 另有「同内容但用 IP 代替域名」的版本（如 trackers_best_ip 20 条、trackers_all_ip 58 条），面向有 DNS 问题的用户。 ｜ `sources/l3-4_trackerslist-readme.md:23,24,25`
  - 项目说明：由 bot 自动检查 tracker 并更新列表；同域名或同 IP 的 tracker 会被去重（见 blacklist）；tracker 按 popularity 与 latency 排序（best 到 worst）。 ｜ `sources/l3-4_trackerslist-readme.md:29,30,31`
  - 有严格适用范围：WebSocket（ws/wss，WebTorrent）tracker 仅少数客户端支持；I2P tracker 需 I2P Router 及支持它的客户端（示例列出 qBittorrent、BiglyBT、Tixati、I2PSnark、libtorrent）；Yggdrasil tracker 需 Yggdrasil Network Router。 ｜ `sources/l3-4_trackerslist-readme.md:32,33,34`
  - GitHub API 元数据（2026-10-07 读）：`pushed_at = 2026-10-06T22:09:41Z`、`archived = False`、`stargazers_count = 55288`、`default_branch = master`。 ｜ `sources/l3-4_trackerslist-api.json`（`repos/ngosang/trackerslist` 原始 JSON 快照）
- 关键实体（端口/路径/阈值等，逐字）: 列表条目数 `20`/`82`/`51`/`19`/`12`/`17`/`1`；IP 版 `20`/`58`/`4`；原始链接基础 `https://raw.githubusercontent.com/ngosang/trackerslist/master/`；镜像 `https://ngosang.github.io/trackerslist/` 与 `https://cdn.jsdelivr.net/gh/ngosang/trackerslist@master/`；API: `pushed_at 2026-10-06T22:09:41Z`, `archived False`, `stargazers_count 55288`, `default_branch master`
- 注: 该项目为第三方社区维护，条目数会随每日自动更新变化——引用具体数字时须以目标日快照为准。

### LC-5 · How to Disable DHT, PeX, and LPD（qBittorrent 官方 wiki）
- 文件: `sources/l3-5_disable-dht-pex-lpd.md` ｜ tier: 官方（qBittorrent 官方 wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方关闭步骤：打开选项（菜单栏 Tools->Options），进入 “BitTorrent” 页。 ｜ `sources/l3-5_disable-dht-pex-lpd.md:11`
  - 在该页取消勾选 “Enable DHT [...]”、“Enable Peer Exchange (PeX) [...]”、“Enable Local Peer Discovery [...]” 三项即关闭。 ｜ `sources/l3-5_disable-dht-pex-lpd.md:12`
  - 该页仅说明「怎么关」与 UI 名称，未说明三者定义，也未给出「何时应关」的适用条件；页面由 Chocobo1 于 May 1, 2024 编辑（2 次修订）。 ｜ `sources/l3-5_disable-dht-pex-lpd.md:10,11,12`
- 关键实体（端口/路径/阈值等，逐字）: 菜单路径 `Tools->Options`；选项页 `"BitTorrent"`；三个复选框名 `"Enable DHT [...]"`、`"Enable Peer Exchange (PeX) [...]"`、`"Enable Local Peer Discovery [...]"`
- 注: 「DHT / PeX / LPD 是什么」在本组已取回来源中仅能还原其 UI 全称（Distributed Hash Table / Peer Exchange / Local Peer Discovery），**未获得**权威定义段或「何时该关」的官方说明。

### LC-6 · Private BitTorrent Trackers Face Credit Crunch（TorrentFreak，行业媒体科普）
- 文件: `sources/l3-6_torrentfreak-credit-crunch.md` ｜ tier: 社区经验（行业媒体报道，2009-03-31；**非任何 PT 站的官方规则**） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 文章开篇陈述：从统计上看，私种站全体成员根本不可能都维持接近 1 的上传/下载比；即便 0.4 或更低这种较宽松门槛，对上传带宽有限的新人也很难达到。 ｜ `sources/l3-6_torrentfreak-credit-crunch.md:8`
  - 引述荷兰代尔夫特理工大学 Tribler 团队的研究，称其考察了多个私种站的「比经济（ratio economy）」并与金融危机作类比。 ｜ `sources/l3-6_torrentfreak-credit-crunch.md:9`
  - 研究发现现有 ratio 体系严重偏向少数拥有大量上传能力的用户（常配备 seedbox），这些「富 peer」拿走了不成比例的上传信用，使新/弱 peer 难以维持达标 ratio。 ｜ `sources/l3-6_torrentfreak-credit-crunch.md:10`
  - 研究人员称即便所有人带宽相近，信用短缺仍会发生（credit crunch），并提出了 0.4 等较宽的 ratio 门槛与「seeding bonus」「用总做种时长替代上传/下载比」等替代思路。 ｜ `sources/l3-6_torrentfreak-credit-crunch.md:11,15`
  - 引述 BitTorrent 协议发明者 Bram Cohen 反对分享率：「更好做法是……不要用总上传/下载比，或用也只作参考、不作为封禁依据」。 ｜ `sources/l3-6_torrentfreak-credit-crunch.md:14`
- 关键实体（端口/路径/阈值等，逐字）: 比值 `close to 1`；宽门槛 `0.4 or less`；研究方 `Tribler`（Technical University of Delft）
- 注: 这是一篇 2009 年行业媒体科普/评论，描述的是对私种分享率机制的**一般性观察与学术研究**，不是某站规则；任何具体阈值须以目标站 rules/FAQ 为准。

### LC-7 · Torrent Hit and Run Penalties Explained（社区文章）
- 文件: `sources/l3-7_hit-and-run-penalties.md` ｜ tier: 社区经验（第三方科普文章，**非某站官方规则**） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 文章称 HnR（hit-and-run）检测是私种站主要采用的一种自动机制，用于惩罚下完立即停止做种的用户，罚则从警告、限速下载到永久封号递进。 ｜ `sources/l3-7_hit-and-run-penalties.md:8`
  - 定义：完成下载后在未满足社区最低做种要求前就把任务从客户端移除，即构成一次 HnR。 ｜ `sources/l3-7_hit-and-run-penalties.md:10`
  - 文章称 tracker 通常并行执行两项基准：按时长（常见 24–72 小时）与按 ratio（常见达到 1:1）；任一条满足通常即清除 HnR 风险。 ｜ `sources/l3-7_hit-and-run-penalties.md:11,12,15`
  - 文章称多数站不会一检测到停种就封号，而给出宽限期（常 24–48 小时）；期内恢复做种并补齐时长或流量即自动清除 HnR 标记、无罚。 ｜ `sources/l3-7_hit-and-run-penalties.md:17,18`
  - 罚则递进层次（文章所述）：记录 strike（常采用「三振」模型）→ 扣积分/花大量积分「买断」strike → 下载限制（Leech Ban，禁取新种子/磁链）→ 账号降级 → 永久封号并常加入 IP/邮箱黑名单。 ｜ `sources/l3-7_hit-and-run-penalties.md:21,22,23,24,25`
  - 恢复途径（文章所述）：重新做种补齐要求，或用积分在站内界面手动消除 strike。 ｜ `sources/l3-7_hit-and-run-penalties.md:30,31`
- 关键实体（端口/路径/阈值等，逐字）: 时长基准 `between 24 and 72 hours`；ratio 基准 `1:1 ratio`；宽限期 `between 24 to 48 hours`；strike 模型 `"three-strike"`；术语 `Leech Ban`
- 注: 本篇为通用科普，未指向任何具体站点；文中「常见/通常」均为作者概括，**具体阈值以目标站 rules/FAQ 为准**。

### LC-8 · Private Tracker Minimum Seed Time Requirements（社区文章）
- 文件: `sources/l3-8_minimum-seed-time.md` ｜ tier: 社区经验（第三方科普文章，**非某站官方规则**） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 文章称现代私种站标准最低做种时长通常为 48–72 小时（2–3 天），但确切时长随社区规则、内容类型与平台架构（如 Gazelle 或 UNIT3D）而变。 ｜ `sources/l3-8_minimum-seed-time.md:10`
  - 文中细分：标准种子通常要求 24–72 小时活跃做种；大文件或整季包可能要求 5–14 天（120–336 小时）；高等级/高级用户常获较短要求。 ｜ `sources/l3-8_minimum-seed-time.md:11,12,13`
  - 做种时长通常按累计计算（不必连续一次完成），但须在指定时限内（如完成后 7–14 天内）累计达标。 ｜ `sources/l3-8_minimum-seed-time.md:16`
  - 文章称多数现代平台执行「双条件」规则：要么做满最低时长（例如 72 小时），要么在该种子上传到 1:1（1.0）ratio，满足其一即可从追踪系统清除、免罚。 ｜ `sources/l3-8_minimum-seed-time.md:19,20,21`
  - 文中提到做种可产生 bonus points，可换上传信用、自定义头衔，或消除误判的 HnR 警告。 ｜ `sources/l3-8_minimum-seed-time.md:27`
- 关键实体（端口/路径/阈值等，逐字）: 主区间 `48 to 72 hours (2 to 3 days)`；标准种子 `24 and 72 hours`；大文件 `5 to 14 days (120 to 336 hours)`；时限示例 `within 7 to 14 days of completion`；示例时长 `72 hours`；ratio `1:1 (1.0)`
- 注: 同为通用科普，未指向具体站点；所有「通常/大多数」表述均为作者概括，**具体阈值以目标站 rules/FAQ 为准**。

### 矛盾与缺口
- **DHT/PeX/LPD 的定义与「何时该关」缺一手权威来源**：本组仅 LC-5 给出三者的 UI 全称与关闭步骤，未含定义段或适用条件；LC-3 只提到 DHT 流量会被 conntrack 误丢。三者定义与关闭时机需另行取源（如 qBittorrent 官方选项说明页 / BEP 5）。
- **无速度排错项来自官方 wiki，但「值应该设多少」未给**：LC-2 只列出自查清单（连接数、半开连接、uTP、加密、IPv6、DHT 节点数等），未给出推荐数值；具体取值需结合用户带宽（LC-2 要求先实测）与其他来源。
- **H&R/分享率来源性质须明确标注**：LC-6 为 2009 年行业媒体科普（非规则）、LC-7 与 LC-8 为第三方社区科普文章（非某站官方）。三者中的「24–72 小时」「1:1」「24–48 小时宽限」「三振」等均为概括性说法，**不代表任何具体 PT 站的现行规则；具体阈值以目标站 rules/FAQ 为准**。
- **LC-6 时效性**：TorrentFreak 文章为 2009-03-31，描述的是当时的比经济与学术研究，不宜当作现行私种生态的现状依据。
- **LC-3 宿主非 qBittorrent**：ArchWiki 的 Deluge 页以 Deluge/libtorrent 为对象，端口示例（56881-56889、58846、8112）属 Deluge 而非 qBittorrent；可借鉴其「TCP+UDP 都要开、NAT 需转发、conntrack 误丢」的排错思路，但不可把其端口号当作 qBittorrent 默认值。
- **LC-4 条目数为「每日变动」值**：README 中的 82/51/20 等条目数随每日自动更新变化，引用时须绑定快照日期 2026-10-07。
- **BEP 3 未覆盖 DHT/PeX/LPD 与 UDP tracker 细节**：BEP 3 明确指向 BEP 23（紧凑 peer 列表）与 BEP 15（UDP tracker），本组未取这两份 BEP；若笔记要展开 announce 的紧凑格式或 UDP 流程，需补取来源。
