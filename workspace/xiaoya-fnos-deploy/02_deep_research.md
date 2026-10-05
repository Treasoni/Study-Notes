# 02 深度素材（P2）— fnOS 部署纯净版小雅（单容器）

> **本文件是中间产物**：引文与数值请回 `sources/` 按行号核对。逐字引文只收在「四、逐字引文对照」，其余为带锚点的概述。
>
> 引文校验记录：逐字引文 **17 处**，已用脚本按行号做**子串精确比对**（中文为逐字比对，非脚本代劳）；数值 **若干处**按来源逐行重数。`note-citation-check.py --mode verbatim` 结果见文末「校验」。

- 运行：`xiaoya-fnos-deploy` ｜ 阶段：P2 深度收集 ｜ 用户选定方向：**方向 1 + A（加「单容器 vs 全家桶」对比节）**
- 抓取工具：`crawl4ai`（`.claude/skills/research-collector/scripts/crawl.sh`）；`curl`/`WebFetch` 本环境不可用。

---

## 一、范围与方法

- **回答两问**：① 不想用 Emby，能否用飞牛影视替代；② 单容器怎么部署。附带 **单容器 vs Emby 全家桶** 对比。
- **来源分层**：official（官方仓库/镜像页/项目官方文档）> reputable（维护者站点/技术笔记站）> community（论坛帖/个人博客）。
- **两条未获取来源**：知乎 `p/2063793058689421981`（crawler 被拦）与官方 Notion 配置指南（SPA，仅取到「浏览器不受支持」壳页）——**均未作为证据**，列入「七、未决问题」。

---

## 二、来源表

| ID | 标题 | 类型 | tier | evidence | 快照（repo 相对） |
|---|---|---|---|---|---|
| S1 | xiaoyaliu/alist Docker Hub 官方镜像页 | 镜像页 | official | fetched | `sources/01_hub_docker_com.md` |
| S2 | xiaoyaDev/xiaoya-alist README（main.sh / 兼容性表） | 官方仓库 | official | fetched | `sources/01_raw_githubusercontent_com.md` |
| S3 | 飞牛论坛《小雅Alist部署教程【解决应用中心版本无数据】》tid=9690 | 论坛帖 | community | fetched | `sources/forum/tid-9690.md` |
| S4 | 飞牛论坛《我把 xiaoyaemby 刮削好的 strm 放到飞牛影音》tid=73955 | 论坛帖 | community | fetched | `sources/forum/tid-73955.md` |
| S5 | SmartStrm 官方部署文档 | 项目官方文档 | official | fetched | `sources/01_smartstrm_github_io.md` |
| S6 | xiaoyaDev/xiaoyahelper（xiaoyakeeper 来源） | 官方仓库 | official | fetched | `sources/01_github_com.md` |
| S7 | AkimioJR/MediaWarp README | 官方仓库 | official | fetched | `sources/lens-b/mediawarp/01_github_com.md` |
| S8 | jimboo7339/fntv-proxy README | 官方仓库 | official | fetched | `sources/lens-b/fntvproxy/01_github_com.md` |
| S9 | 飞牛论坛《飞牛影视 strm 实战教程》tid=57134 | 论坛帖 | community | fetched | `sources/p2/tid-57134.md` |
| S10 | 飞牛论坛《飞牛影视+Alist小雅刮削后无影视文件》tid=40446 | 论坛帖 | community | fetched | `sources/p2/tid-40446.md` |
| S11 | 飞牛论坛《小雅安装后飞牛影视扫描会转存到个人阿里网盘》tid=6046 | 论坛帖 | community | fetched | `sources/p2/tid-6046.md` |
| S13 | monlor《小雅影视库一键部署项目》 | 维护者博客 | reputable | fetched | `sources/p2/monlor-144.md` |
| S14 | newzone.top《小雅 Alist：阿里云盘影视资源合集》 | 技术笔记站 | reputable | fetched | `sources/p2/newzone-xiaoya.md` |
| S12 | 知乎《用飞牛影视连接小雅，可行吗？》 | 个人文章 | community | **未获取** | — |
| S15 | 官方 Notion 配置指南 | 官方文档 | official | **未获取** | — |

tier 分布：official 6 ｜ reputable 2 ｜ community 6 ｜ 未获取 2。

---

## 三、事实与来源映射（claim / source map）

> 每条给出 `来源:行号`；概述句非逐字，逐字引文见第四节。

### F1 小雅是什么 / 单容器定位

- 小雅是**资源层**（AList 聚合网盘资源 + 内嵌小雅资源库），播放/海报墙由前端承担（S1、S13:88-91）。
- 官方脚本把 **「安装 小雅Alist」** 与 **「安装 Emby全家桶（一键）」** 列为**不同菜单项**，即「只装 Alist」是官方承认的独立装法（S2:75-76）。
- **「纯净版」不是官方术语**：S1/S2 均无该词；本笔记须把它写清为「社区叫法 ≈ 只装 AList、不装 Emby」。

### F2 单容器部署事实

- **官方镜像** `xiaoyaliu/alist`；官方页给出**一键安装/更新脚本**与 WebDAV 账号（S1:7,16,18）。
- **官方端口 5678**（S1:17）；**WebDAV 账号 `guest` / `guest_Api789`**（S1:18），与论坛帖一致（S3:72）。
- **另一种常用路线（monlor）**：镜像 `ghcr.io/monlor/xiaoya-alist`（S3:36、S13:167），用**环境变量**注入凭据，明确「无需映射文件」（S13:21）；三件套 `ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID`（S13:160-162、S3:45-47）。
- **两套并存配置机制**：① 环境变量（monlor 路线）；② `/data` 或 `/etc/xiaoya` 下**凭据文件**（仅社区回帖为证，见七、待核实）。
- **fnOS 论坛实操 compose**：镜像 `ghcr.io/monlor/xiaoya-alist:latest`，端口 `5677:5678` / `5345:2345` / `5346:2346`（S3:36,40-42）。

### F3 单容器 vs 全家桶（对比节素材）

- 组成：单容器 = 仅 AList（在线播放 + WebDAV）；全家桶 = AList + Emby（+ 可选 Jellyfin）+ Metadata 元数据服务（S13:14,88-91）。
- **推荐配置表**（S13:74-80，维护者推荐、非官方硬性）：

  | 方案 | CPU | 内存 | 硬盘 | 行号 |
  |---|---|---|---|---|
  | 仅部署 Alist | 1 核 | 512M | 512M | S13:78 |
  | Alist + Emby | 2 核 | 4G | 150G | S13:77 |
  | Alist + Emby + Jellyfin | 2 核 | 4G | 200G | S13:79 |
  | Alist + Jellyfin | 2 核 | 4G | 150G | S13:80 |

- **官方 Jellyfin 路线已弃维护**（S2:180），全家桶里「+Jellyfin」不建议走官方脚本。
- fnOS 在官方**兼容性表**内，`all_in_one.sh` / `emby_config_editor.sh` / `xiaoya_notify.sh` 三项均 ✅（S2:277）。

### F4 飞牛影视 vs Emby 作前端

- **不必须 Emby**：没有来源断言「必须 Emby」；S4 发帖者本人就是「全家桶除了 emby」（S4:32）。
- **飞牛影视可作前端**的官方旁证：MediaWarp 自述为「前置于 EmbyServer/Jellyfin/**飞牛影视** 的反向代理服务器」（S7:51）；fntv-proxy 基于飞牛影视 **0.9.3**（S8:45）。
- **播放链路**：STRM 只存 URL 指针，302 直链使流量不过媒体服务器（S7:53）；飞牛侧需把播放地址指向代理端口 **:28005**（S8:71）。
- **外网/蜂窝网坑**：飞牛原生 `/stream` 响应里的直链仍是内网地址（`xiaoya.host:5678`），手机蜂窝网解析不了（S4:42）。
- **UA 绑定坑**：同一条 115 CDN 临时链接，`trim_player` UA 返回 206、换成 `Mozilla/5.0` 返回 403（S4:39-40）。
- **直接扫描小雅的风控坑**：见 F5。

### F5 fnOS 落地与运维

- **应用中心版小雅不可用**（社区唯一来源）：S3:32 楼主称飞牛应用中心自带的小雅AList「实测无法正常获取到视频数据」。**注意**：仅此一帖，非官方公告；且「是否已下架/停更」无官方来源。
- **STRM 生成**：SmartStrm 官方文档给 fnOS 应用中心装法（数据目录 `应用文件/SmartStrm`，应用版**滞后 1~2 个版本**，S5:79,82）与 Compose（镜像 `cp0204/smartstrm:latest`、`:8024`、`network_mode: host`，S5:20-23,31-33）。
- **风控与转存**：飞牛影视直接扫描小雅会触发**转存到个人网盘**、容量不足导致扫描卡住、库为空（S10:33, S11:33,71）；规避法是**只挂小雅下已生成的 strm 子目录**、或刮削后删本地临时文件（S10:33,121,161）。原帖用「基本上半分钟就需要几个T的存储」描述量级（S10:33，**模糊表述，不可当精确值**）。
- **清理转存缓存**：`xiaoyakeeper`，镜像 `ddsderek/xiaoyakeeper`（S6:91）；模式 0/1/3/4/5 有效、模式 2 已废弃（S6:33-55）。

---

## 四、逐字引文对照（原文 / 出处）

> 全部 17 处已按行号做子串精确比对。出处「行号」为该句子在快照文件中的行号。

| 原文（逐字） | 出处 |
|---|---|
| `安装 小雅Alist -> 1 1` | S2:75 |
| `安装 Emby全家桶（一键） -> 2 1` | S2:76 |
| `注意：目前官方 Jellyfin 安装方案已经长久未维护！` | S2:180 |
| `\| fnOS (飞牛私有云) \| ✅ \| ✅ \| ✅ \|` | S2:277 |
| `\| **仅部署 Alist**  \| 1核  \| 512M  \| 512M  \|` | S13:78 |
| `\| **Alist + Emby**  \| 2核  \| 4G  \| 150G  \|` | S13:77 |
| `通过环境变量配置阿里云盘token，无需映射文件` | S13:21 |
| `端口：5678 访问： http://xxxxx:5678/` | S1:17 |
| `webdav 账号密码 用户: guest 密码: guest_Api789` | S1:18 |
| `飞牛NAS应用中心自带的小雅Alist实测无法正常获取到视频数据` | S3:32 |
| `webdav的配置的用户名和密码是guest/guest_Api789` | S3:72 |
| `手机在蜂窝网络上无法使用 NAS 内部域名` | S4:42 |
| `前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器` | S7:51 |
| `0.9.3` | S8:45 |
| `基本上半分钟就需要几个T的存储` | S10:33 |
| `不建议挂载小雅的全部文件夹` | S10:33 |
| `滞后 1~2 个版本` | S5:82 |

---

## 五、矛盾与冲突（不合并，写作时并列）

1. **应用中心版**：S5/S9 说 SmartStrm「已上架 fnOS、可直接装」（S5:77, S9:32）；S10 说「所有软件都不要从飞牛官方应用商店安装」（S10:56）。→ 属**不同对象**（维护中的第三方工具 vs 停更项目），不可类推。
2. **镜像容器内端口**：S1:17 给 `5678`，S14:23 映射到容器 `80`——同一「官方镜像」两种内端口说法，未解决。
3. **WebDAV 默认用户**：S3:55（yml 注释）写「默认用户为 dav」，S3:72/S1:18 写 `guest`。同一文件内自相矛盾（注释来自 monlor 仓库，楼主答案是实测）。
4. **STRM 是否消除风控**：S9:32 开篇称「终于不用再为刮削频繁触发风控」，S9:263 又有用户回报 strm 播放仍报「触发网盘风控」。
5. **MediaWarp 对飞牛影视的成熟度**：正文把飞牛影视列为可代理对象（S7:51），但 TODO 仍列「适配 飞牛影视」（S7:86）。
6. **节点小宝域名**：S9:32 以节点小宝专属域名为核心方案，S9:244 有用户回报新版「没法生成了」。

---

## 六、实操指引（给大纲 / 写作的可执行结论）

1. **首选路线（对齐用户）**：**单容器（仅 AList）+ 飞牛影视作前端**。理由：已有飞牛影视、不想装 Emby；单容器资源门槛低一个量级（S13:77-78）。
2. **镜像二选一**：官方 `xiaoyaliu/alist`（WebDAV + 一键脚本，S1）或 `ghcr.io/monlor/xiaoya-alist`（环境变量注入，S3/S13）。**推荐写清两条路线的差异**，让读者按凭据管理习惯选。
3. **飞牛影视接入**：先解决 STRM/302（SmartStrm 生成 strm，S5/S9），再用 **MediaWarp（FNTV 类型）或 fntv-proxy（飞牛 `:28005`）** 修 302 与外网可达（S7:51, S8:71）——**不要**把整个小雅 Alist 直接丢给飞牛影视扫描（S10:33, S11:33）。
4. **必须写进「坑」**：内网地址导致蜂窝网播不动（S4:42）、CDN 链接绑 UA（S4:39-40）、转存风控与缓存清理（S10/S11/S6）。
5. **应用中心版**：作为「在 fnOS 上装错地方会怎样」的避坑提示（S3:32），并注明仅社区经验。

---

## 七、未决问题 / 待核实（不得写成结论）

1. **「纯净版」无官方定义**——社区俗称，须在正文说明。
2. **`/data` 凭据文件的确切文件名与机制**：~~未在任何已抓官方来源出现；仅社区回帖为证~~ → **已由 P4 回补更新（见文末「补记」）：文件名三件套已坐实，目录随路线**。
3. **`ghcr.io` 无「官方」小雅镜像**——社区指的是 monlor 的 `ghcr.io/monlor/xiaoya-alist`。
4. **`xiaoya.host` 是否官方域**：未证，仅社区链路描述。
5. **飞牛影视支持 STRM 的起始版本**：来源冲突，未定。
6. **应用中心版小雅是否已下架/停更**：无官方公告。
7. **「半分钟几个 T」**：原帖确有该表述（S10:33），但为**模糊定性**，无精确值，写笔记时按「原帖称」引用。
8. **未获取**：S12（知乎，crawler 被拦）、S15（官方 Notion 配置指南，SPA）——Notion 可能含官方完整参数表，若要补，P3 前需换抓取方式。
9. **MediaWarp 与 fntv-proxy 能否共存 / 版本矩阵**：无来源。

---

## 八、下游交接

- **素材就绪度**：两问都有 official/reputable + community 双层支撑；F2/F3/F4 可直接进大纲。
- **写作纪律**：中文逐字引文一律回 `sources/` 按行号核对；`snippet-only` 已全部清零（S9-S11 已抓全文）。
- **下游写作须带上的口径**（跨章不致漂移）：镜像名 `xiaoyaliu/alist` 与 `ghcr.io/monlor/xiaoya-alist` 不可混写；端口 `5678` 与宿主映射（`5677`/`6789`/`15678`）分开写；WebDAV 一律 `guest/guest_Api789`（并注明 S3 注释里的 `dav` 为冲突）。

---

## 校验

- 中文/英文逐字引文 **17 处**已完成按行号子串精确比对（见第四节）。
- 数值：推荐配置表 4 行、端口清单、模式编号 0/1/3/4/5 均逐行重数。
- `note-citation-check.py --mode verbatim --file 02_deep_research.md`：见本轮运行输出。

---

## 补记（P4 回补，2026-10-06）

> 目的：第 3 章写作时发现「凭据文件侧」证据不足（原未决 #2），经用户同意回补抓取。**新增来源不改变 P2 结论，仅补齐一处证据缺口。**

**新增来源**

| ID | 标题 | tier | 快照（repo 相对） |
|---|---|---|---|
| S16 | 博客园 z-addone《安装小雅Alist》(2025-04-13) | community | `sources/p3/z-addone/01_www_cnblogs_com.md` |
| S17 | 博客园 gnz48《群晖 docker 部署小雅全家桶》 | community | `sources/p3/gnz48/01_www_cnblogs_com.md` |
| S18 | GitHub API：`xiaoyaDev/xiaoya-alist` 仓库文件清单 | official | `sources/p3/github-api/listing.json.md` |
| S19 | monlor/docker-xiaoya `env` 模板 | project-official | `sources/p3/monlor-env/01_raw_githubusercontent_com.md` |

**补齐的证据（逐字，含行号）**
- 凭据文件三件套：`mytoken.txt`（S16:23、S17:25）、`myopentoken.txt`（S16:24、S17:25）、`temp_transfer_folder_id.txt`（S16:25、S17:32）。官方侧仅 `mytoken.txt` 可证（S6:65，`/etc/xiaoya/mytoken.txt`）；另两份为**社区教程**支撑（tier=community）。
- 放置位置社区说法：`_data_` 目录（S16:28）、`docker/xiaoya`（S17:32）。
- **WebDAV 用户名冲突有解**：monlor `env` 注释逐字「webdav用户名为dav，设置密码。默认用户密码：guest/guest_Api789」（S19:32）→ `dav` 属 monlor 路线、`guest/guest_Api789` 为默认账号；原「矛盾 #3」应改写为「两路线取值不同」。
- S18 佐证 S2 兼容表脚本名确实存在于官方仓库（`all_in_one.sh` / `main.sh` / `emby_config_editor.sh` / `xiaoya_notify.sh`）。

**对未决清单的更新**
- 未决 #2（`/data` 凭据文件机制）：文件名已坐实，**降级为「文件名已证、目录随路线」**。
- 矛盾 #3（WebDAV dav vs guest）：**改写为路线差异**，不再是来源冲突。

**口径变更（下游须同步）**
- 第 3 章已按此回补：新增文件侧三件套表、WebDAV「两条路线」说明，更新小结与「引文对照」表（新增 #17–#20）。
