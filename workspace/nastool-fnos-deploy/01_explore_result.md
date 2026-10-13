# P1 探测结果 — nastool 家庭影院（fiNOS）

> ⚠️ 本文件是**中间产物**：其中的引文与数值请回 `sources/` 按行号核对，不要直接当权威。
> 生成日期：2026-10-06 ｜ 生成阶段：P1（探测式收集）
> 本轮范围：按用户指示**只跑方向 1（现状与选型）**，用于锚定「最新方案是什么」；方向 2/3 未派发。

---

## 一、结论：现在的「最新方案」是 MoviePilot V3

一句话：**你给的视频里的原版 nastool 已经走到头了；同一作者（jxxghp）重做的 MoviePilot 才是现在的主线，且已进入 V3。**

| 项 | 结论 | 依据 |
| --- | --- | --- |
| 原版 nastool（NAStool/nas-tools） | **已归档、只读**，归档日期 **2023-05-16** | 仓库页横幅（`sources/gh/nastool_repo_page.html`） |
| 旧地址 `jxxghp/nas-tools` | **404**（已不存在） | 存证 `sources/gh/nas-tools_github_page_status.txt` |
| 当前主线 | **MoviePilot**，官方自述「基于 NAStool 部分代码重新设计」 | `sources/gh/MoviePilot_v3_README.md:15` |
| 当前版本线 | **V3**，独立镜像 `jxxghp/moviepilot-v3:latest`；V2 是上一代 | `sources/gh/MoviePilot_v3_README.md:30`、`sources/gh/v2-to-v3-overview.md:462` |
| 部署方式 | 官方推荐 Docker；Compose 示例与升级以官方 Wiki 为准 | `sources/gh/MoviePilot_v3_README.md:30` |

### ⚠️ 必须先告诉你的一个硬门槛：MoviePilot 需要「PT 站点认证」

这不是可选项。官方 Wiki 的原话是：

> 「MoviePilot引入了PT用户认证机制，你需要有认证站点范围内的账号才能使用软件的资源搜索、订阅及下载功能」（`sources/wiki/basic.txt:55`）

配套的必填项是环境变量 `AUTH_SITE`：

> 「❗AUTH_SITE：认证站点（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用 `,` 分隔，如：`iyuu,hhclub`，会依次执行认证操作，直到有一个站点认证成功。」（`sources/wiki/configuration.txt:29-35`）

**这意味着：** 如果你手上**没有**任何在支持列表里的站点账号（IYUU、HHClub 等），MoviePilot V3 装得起来，但**搜片、订阅、下载这些核心功能用不了**。这会直接改变笔记该写什么，所以在本轮就摆到桌面上。

### 另一处必须纠正的旧认知：V3 的初始化方式变了

网上大量流传的「V2 式」compose 示例（把 `SUPERUSER_PASSWORD` / `API_TOKEN` 写进环境变量）**在 V3 已不适用**：

> 「V3 全新安装不会在启动阶段初始化管理员用户名或密码，也不会把初始密码打印到日志。首次访问 Web 地址时，系统会自动进入初始化页面」（`sources/wiki/basic.txt:4`）

所以凡是照抄旧教程 V3 部署的，都会在「找初始密码」这一步卡住。

---

## 二、候选来源（方向 1）

`evidence_form`：`fetched` = 已取回正文；`snippet-only` = 仅搜索结果文本，**P2 需先抓取才可当证据**。

### 已抓取（fetched）

| # | tier | 来源 | URL | 日期 | 分 | evidence_form | 相关性（一句话） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A | MoviePilot 仓库 README（v3 分支） | `raw.githubusercontent.com/jxxghp/MoviePilot/v3/README.md` | 随 v3 分支 | 5/5 | fetched | 官方定位、V3 镜像名、部署入口 |
| 2 | A | MoviePilot 官方 Wiki · 基础篇 | `https://wiki.movie-pilot.org/basic` | 抓取 2026-10-06 | 5/5 | fetched | **PT 认证门槛**、V3 初始化流程、API_TOKEN |
| 3 | A | MoviePilot 官方 Wiki · 配置参考 | `https://wiki.movie-pilot.org/configuration` | 抓取 2026-10-06 | 5/5 | fetched | `AUTH_SITE`/`PUID`/`PGID`/`PORT`/`NGINX_PORT` 等环境变量官方定义 |
| 4 | A | MoviePilot V2→V3 变化总览（仓库内文档） | `raw.githubusercontent.com/jxxghp/MoviePilot/v3/docs/v2-to-v3-overview.md` | 同步至 2026-09-03 | 4/5 | fetched | V2/V3 差异、升级步骤、回退边界 |
| 5 | A | NAStool/nas-tools 仓库页 | `https://github.com/NAStool/nas-tools` | 归档 2023-05-16 | 4/5 | fetched | 原版已归档的存证 |

### 待抓取（snippet-only，P2 才可用）

| # | tier | 来源 | URL | 分 | evidence_form | 相关性 |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | B | 飞牛私有云官方论坛 · Docker 安装 moviepilot | `club.fnnas.com/forum.php?mod=viewthread&tid=605`、`tid=1165` | 4/5 | snippet-only | fnOS 实机部署贴，含端口冲突等实操细节 |
| 7 | B | 腾讯云社区《飞牛 fnos 使用 docker 部署 MoviePilot V2 自动化影视管理平台教程》 | `cloud.tencent.com.cn/developer/article/2478163` | 4/5 | snippet-only | 「V2 式」compose 全文，**注意其与 V3 差异** |
| 8 | B | 视频来源（本任务的触发视频） | `bilibili.com/video/BV1egF7eFERT/` | 3/5 | snippet-only | 只取到标题与简介，正文未获取 |
| 9 | B | 视频简介指向的配置文件站 | `blog.010322.xyz`（搜 nastool） | 3/5 | snippet-only | 未验证；是否为 V2/V3 口径待查 |
| 10 | C | LINUX DO / NGA / 什么值得买 等选型对比讨论 | 见搜索记录 | 3/5 | snippet-only | 社区口碑：MP ≈ 原版 95% 功能、缺点与门槛 |

### 收集缺口（P2 需补齐）

- **方向 2（部署实操）未跑**：V3 的官方 Compose 示例、目录映射、`PUID/PGID` 在 fnOS 上的实际取值、与飞牛影视/Jellyfin 的对接，均**尚无一手来源**。
- **方向 3（生态与对接）未跑**：下载器、站点索引、硬解、STRM/302 外网播放、避坑清单，**尚无一手来源**。
- `blog.010322.xyz` 与视频正文未取；不确定其口径是原版 nastool 还是 MoviePilot。
- V2 是否已正式停止支持：搜索页称 2026-08-31，但**官方文档未见该表述**，暂列为待核（不要写进成品）。

---

## 三、一手引文存证（供下游按行号回核）

| # | 逐字原文 | 出处（文件:行） |
| --- | --- | --- |
| 1 | `基于 NAStool 部分代码重新设计，聚焦自动化核心需求，减少问题同时更易于扩展和维护。` | `sources/gh/MoviePilot_v3_README.md:15` |
| 2 | `推荐优先使用 Docker 部署。V3 使用独立镜像 \`jxxghp/moviepilot-v3\`，V2 和旧版镜像保持原命名。` | `sources/gh/MoviePilot_v3_README.md:30` |
| 3 | `，MoviePilot引入了PT用户认证机制，你需要有认证站点范围内的账号才能使用软件的资源搜索、订阅及下载功能，出此下策与利益无关，属NAStool一路走来，吸取失败经验的无奈之举。` | `sources/wiki/basic.txt:55` |
| 4 | `V3 全新安装不会在启动阶段初始化管理员用户名或密码，也不会把初始密码打印到日志。首次访问 Web 地址时，系统会自动进入初始化页面；输入管理员用户名、密码和确认密码并保存后，才会创建管理员账号。` | `sources/wiki/basic.txt:4` |
| 5 | `❗AUTH_SITE：认证站点（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用 , 分隔，如：iyuu,hhclub，会依次执行认证操作，直到有一个站点认证成功。` | `sources/wiki/configuration.txt:29-35` |
| 6 | `This repository was archived by the owner on May 16, 2023. It is now read-only.` | `https://github.com/NAStool/nas-tools`（2026-10-06 抓取） |
| 7 | `jxxghp/moviepilot-v3:latest` | `sources/gh/v2-to-v3-overview.md:462` |
| 8 | `首次安装 \| 依赖环境变量和设置向导初始化 \| 首次打开网页创建管理员和 API Key \| 初始密码不再需要出现在日志或部署文件中` | `sources/gh/v2-to-v3-overview.md:33` |

> **存疑项（宁空不猜）**：`sources/wiki/basic.txt:54` 作 `为了控制用户数量避免大规范泛滥使用`，HTML 原文（`<strong>` 内）亦如此，疑似站点笔误（疑为「大规模」）。**该半句不要引用**，只引用第 3 行引文的后半段。

---

## 四、预计 P2 范围

若按方向 A 走，P2 需覆盖：官方 V3 Compose 全量字段 → fnOS 实机差异（端口 3000 冲突、`core` 挂载路径）→ 下载器/媒体服务器/认证配置 → STRM+302 外网播放链路 → 避坑清单。预计一手来源 6–10 篇，社区来源 5–8 篇。

---

## 五、请你选方向（P1 用户关卡）

**先决问题：你手上有可用于认证的站点账号吗（IYUU / HHClub 等）？** 这直接决定笔记能不能按 MoviePilot V3 主线写。

- **方向 A｜完整链路（推荐）**：MoviePilot V3 部署 → PT 认证 → 下载器/媒体服务器对接 → STRM+302 外网播放 → 避坑。最贴合「家庭影院」四个字。
- **方向 B｜精简**：只写到「能搜、能下、能整理」，不铺 STRM/302 与外网播放。
- **方向 C｜换主线**：如果你**没有 PT 站点账号**，改走不依赖 PT 认证的路线（如小雅 / OpenList 网盘流媒体，或 MediaMaster 这类小白工具），原版 nastool 与 MoviePilot 只作背景。

选定后我再进入 P2 深度收集。
