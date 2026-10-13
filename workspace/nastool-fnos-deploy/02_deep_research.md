# P2 深度素材 — 飞牛 fnOS 上搭建 nastool 家庭影院（MoviePilot V3 + 备选路）

> ⚠️ **本文件是中间产物**：引文与数值请回 `sources/` 按「文件:行」核对，不要直接当权威。
> 生成日期：2026-10-06 ｜ 阶段：P2 ｜ 上游：`00_intent.md`、`01_explore_result.md`
> 下游交接：`outline-generator`、`chapter-writer`（只取来源 ID / 路径 / 锚点，不要复述本文件的转述句为引文）

---

## 一、范围

按用户在 P1 关卡确认的 **A+C 双路**收集：

- **主路 A**：MoviePilot **V3** 在 fnOS 上的部署、认证、生态对接与避坑（一手来源 = 官方 Wiki + 官方仓库文档）。
- **备选路 C**：不依赖 PT 认证的网盘流媒体路线（小雅 / OpenList 等）——**本路无须新收集**，库内既有笔记已完整覆盖，见 §六。

本轮**未**收集：Windows / 群晖套件 / 本地 CLI 安装方式（`wiki/install.txt:466-600`，与本主题无关）；音乐链路细节（V3 新增，非家庭影院主线）。

---

## 二、来源表

| ID | tier | 来源 | 地址 | 取回日期 | evidence_form |
| --- | --- | --- | --- | --- | --- |
| W-BASIC | A | MoviePilot Wiki · 基础（用户认证 / 初始密码） | `https://wiki.movie-pilot.org/basic` | 2026-10-06 | fetched → `sources/wiki/basic.{html,txt}` |
| W-INSTALL | A | MoviePilot Wiki · 安装指引（V3 全量 Compose / 反代） | `https://wiki.movie-pilot.org/install` | 2026-10-06 | fetched → `sources/wiki/install.txt` |
| W-CONF | A | MoviePilot Wiki · 配置参考（环境变量） | `https://wiki.movie-pilot.org/configuration` | 2026-10-06 | fetched → `sources/wiki/configuration.txt` |
| W-READY | A | MoviePilot Wiki · 环境准备（网络 / 站点 / 配套软件） | `https://wiki.movie-pilot.org/ready` | 2026-10-06 | fetched → `sources/wiki/ready.txt` |
| W-SITE | A | MoviePilot Wiki · 站点 | `https://wiki.movie-pilot.org/site` | 2026-10-06 | fetched → `sources/wiki/site.txt` |
| W-REORG | A | MoviePilot Wiki · 文件整理 | `https://wiki.movie-pilot.org/reorganize` | 2026-10-06 | fetched → `sources/wiki/reorganize.txt` |
| W-TROUBLE | A | MoviePilot Wiki · 故障排除 | `https://wiki.movie-pilot.org/troubleshooting` | 2026-10-06 | fetched → `sources/wiki/troubleshooting.txt` |
| W-DL | A | MoviePilot Wiki · 下载目录 | `https://wiki.movie-pilot.org/download` | 2026-10-06 | fetched → `sources/wiki/download.txt` |
| G-README | A | MoviePilot 仓库 README（v3 分支） | `raw.githubusercontent.com/jxxghp/MoviePilot/v3/README.md` | 2026-10-06 | fetched → `sources/gh/MoviePilot_v3_README.md` |
| G-V2V3 | A | V2→V3 变化总览（仓库内） | `.../v3/docs/v2-to-v3-overview.md` | 2026-10-06 | fetched → `sources/gh/v2-to-v3-overview.md` |
| G-ARCH | A | NAStool/nas-tools 归档存证 | `https://github.com/NAStool/nas-tools` | 2026-10-06 | fetched → `sources/gh/nastool_repo_page.html` |
| X-404 | A | jxxghp/nas-tools HTTP 404 存证 | `https://github.com/jxxghp/nas-tools` | 2026-10-06 | fetched → `sources/gh/nas-tools_github_page_status.txt` |
| C-FNNAS | B | 飞牛官方论坛 MoviePilot 贴（tid=605/1165） | `club.fnnas.com/...tid=605` | 2026-10-06 | **抓取失败**（反爬，仅 417 字符壳）→ snippet-only |
| C-BLOG | B | 视频简介指向的配置站 | `blog.010322.xyz` | 2026-10-06 | **不可达**（HTTP 000）→ snippet-only |

> `snippet-only` 行（C-FNNAS、C-BLOG）**不得当证据**；P3/P4 若要用，须先补抓。

---

## 三、Claim → Source 映射

### A1 选型现状（主线为何是 MoviePilot V3）

| # | 论断 | 出处 |
| --- | --- | --- |
| 1 | 原版 nastool 仓库已归档、只读：`This repository was archived by the owner on May 16, 2023. It is now read-only.` | `G-ARCH` 仓库页横幅 |
| 2 | 旧地址 `jxxghp/nas-tools` 已 404（不存在） | `X-404` |
| 3 | MoviePilot 自述：`基于 NAStool 部分代码重新设计，聚焦自动化核心需求，减少问题同时更易于扩展和维护。` | `G-README:15` |
| 4 | `推荐优先使用 Docker 部署。V3 使用独立镜像 \`jxxghp/moviepilot-v3\`，V2 和旧版镜像保持原命名。` | `G-README:30` |
| 5 | V3 标准镜像是普通用户默认选择 | `G-V2V3:465`、`G-V2V3:462`（`jxxghp/moviepilot-v3:latest`） |
| 6 | V3 兼容 V2 的配置与数据库，保留原 `/config` 映射即可，但**不能只靠重启 V2 容器跨主版本升级** | `W-INSTALL:20-25`、`G-V2V3:467` |

### A2 认证门槛（本主题的**关键约束**）

| # | 论断 | 出处 |
| --- | --- | --- |
| 7 | MoviePilot 引入 PT 用户认证：`，MoviePilot引入了PT用户认证机制，你需要有认证站点范围内的账号才能使用软件的资源搜索、订阅及下载功能，出此下策与利益无关，属NAStool一路走来，吸取失败经验的无奈之举。` | `W-BASIC:55` |
| 8 | **功能二分**：`MoviePilot包括两大部分功能：文件整理刮削、资源订阅下载，其中资源订阅下载功能需要有可用的PT站点，同时这些站点中需要有一个可用于认证` | `W-READY:71-83` |
| 9 | 未认证则站点不可用：`如果你没有通过用户认证，私有站点和公开站点都无法维护到系统中，已维护的站点实际也无法使用。` | `W-SITE:4` |
| 10 | `❗AUTH_SITE：认证站点（认证通过后才能使用站点相关功能），支持配置多个认证站点，使用 , 分隔，如：iyuu,hhclub，会依次执行认证操作，直到有一个站点认证成功。` | `W-CONF:29-35` |
| 11 | 三种认证方式：初始化向导（V1/V2）/ 头像菜单「用户认证」（v2.0.7+ 支持 UI）/ 环境变量 `AUTH_SITE` | `W-BASIC:56-63`、`W-CONF:36` |

> **推论（非引文，须显式标注）**：由 #8 可推出「**没有 PT 账号时，MoviePilot 的「文件整理刮削」仍可用，只有「资源订阅下载」不可用**」。这是把 A 路与 C 路接起来的关键，但它是**推断**，成品中必须写明依据（#8 的功能二分），不得写成官方原话。

### A3 V3 部署（可照抄骨架）

| # | 论断 | 出处 |
| --- | --- | --- |
| 12 | V3 全新启动不预置管理员/密码/API Key：`V3 全新启动不会预置管理员用户、密码或 API Key，首次访问 Web 地址时会进入初始化页面，填写管理员用户名、密码（需确认两次）并生成 API Key 后保存，再跳转到登录页面。` | `W-INSTALL:40` |
| 13 | V3 模板中**不需要**填 `SUPERUSER` / `SUPERUSER_PASSWORD` / `API_TOKEN` | `W-INSTALL:238-243`、`W-INSTALL:456-464` |
| 14 | 「小白版」只需改 3 个宿主机目录：`/media`、`/moviepilot-v3/config`、`/moviepilot-v3/core` | `W-INSTALL:200-204` |
| 15 | 启动与更新：`docker compose up -d`；更新 `docker compose pull && docker compose up --force-recreate -d` | `W-INSTALL:232-245` |
| 16 | 访问 `http://宿主机IP:3000`；端口改了则访问地址同步改 | `W-INSTALL:214` |
| 17 | `/media` 硬链接约束：`如果你计划使用 硬链接 来整理文件，那么 文件下载目录 和整理后的 媒体库目录 只能映射一个根目录不能分开映射，否则将会导致跨盘无法硬链接。` | `W-INSTALL:440` |
| 18 | 三种跨盘不可硬链接的情形（不同磁盘 / 同盘不同分区 / 分别映射成两个路径） | `W-INSTALL:441-444` |
| 19 | V3 优雅停止：建议预留 `120` 秒（`--stop-timeout 120` / `stop_grace_period: 120s`） | `W-INSTALL:41-43`、`W-INSTALL:230` |
| 20 | V3 内置 supervisor 托管 Nginx + 后端，Web 内建重启不需要映射 `/var/run/docker.sock` | `W-INSTALL:44-48` |
| 21 | 基础环境变量：`NGINX_PORT=3000`、`PORT=3001`、`PUID`、`PGID`、`UMASK`、`TZ` | `W-INSTALL:222-228`、`W-CONF:248-266` |
| 22 | 反向代理需加 `proxy_set_header` 等（否则部分功能不可用），SSL 需开 `http2` | `W-INSTALL:612-631` |

> **端口提醒（存疑，snippet-only，勿当结论）**：社区帖称飞牛应用中心的浏览器会占用 `3000`，且改 MoviePilot 端口可能导致安装失败。**一手未证实**，成品若要写须标「社区经验，待实机验证」。

### A4 生态对接

| # | 论断 | 出处 |
| --- | --- | --- |
| 23 | 下载器版本要求：Qbittorrent `>= 4.3.9`、Transmission `>= 3.0` | `W-READY:96-103` |
| 24 | 媒体服务器版本建议：Emby `>= 4.8.0.45`、Jellyfin `latest`、Plex 无特定要求 | `W-READY:104-114` |
| 25 | CookieCloud：MP 已内置服务端；浏览器插件必装，用于同步站点 Cookie | `W-READY:115-124` |
| 26 | MP 是「一环」：需下载器下载、媒体服务器展示，并通过媒体服务器 Api 查库存控重复下载 | `W-READY:85-94` |
| 27 | 整理模式：硬链接 / 软链接 / 复制 / 移动 / Rclone 复制 / Rclone 移动，各自代价 | `W-REORG:174-198` |
| 28 | 覆盖方式：从不覆盖 / 按大小覆盖 / 总是覆盖 / 仅保留最新版本 | `W-REORG:200-214` |
| 29 | 站点项：地址 / 优先级 / RSS / 超时 / Cookie / Authorization / API Key / UA / 流控 / 代理 / 浏览器仿真 | `W-SITE:311-368` |
| 30 | 下载目录必须映射进容器且与下载器目录一致，否则文件落进容器内 | `W-DL:3-9` |
| 31 | QB 完成时回调可省去轮询：`curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot"` | `W-REORG:168-172` |

### A5 避坑

| # | 症状 | 原因 / 处理 | 出处 |
| --- | --- | --- | --- |
| 32 | 硬链接转移报 `-1` | 下载目录与媒体库目录跨盘/跨存储空间/分别映射 | `W-TROUBLE:3-13` |
| 33 | 目录监控不自动整理（日志有 `inotify` 报错） | 宿主机调大 inotify 参数并重启 | `W-READY:60-68`、`W-TROUBLE:23-29` |
| 34 | 网盘 / SMB / NFS 不支持事件触发的实时监控 | 打开目录监控「兼容模式」（性能较低），或改用下载器监控 | `W-TROUBLE:30-43` |
| 35 | 启动时重复下载浏览器内核 | 检查是否映射 `/moviepilot-v3/core:/moviepilot/.cloakbrowser` | `W-TROUBLE:48-51` |
| 36 | `No module named 'app.helper.sites'` | 自动更新被打断；重置/重建容器，并配 `PROXY_HOST` | `W-TROUBLE:15-21` |
| 37 | 网络前提：需顺畅访问 TheMovieDb Api 与 GitHub | 否则元数据匹配与升级/插件会失败 | `W-READY:3-36` |
| 38 | 建议装 portainer 简化容器配置编辑 | — | `W-READY:125-129` |

---

## 四、矛盾与冲突（已在写出口核对）

1. **社区「V2 式」Compose 与 V3 不兼容。** `01_explore_result.md` 候选 7（腾讯云教程）及大量视频/帖子的 Compose 仍写 `SUPERUSER_PASSWORD` / `API_TOKEN` / `AUTH_SITE` 环境变量——那是 **V2** 口径。V3 改为首次网页初始化（#12、#13）。**写 V3 教程时照抄会误导。**
2. **「没有 PT 能不能用」口径不一。** 社区有「MP 支持 BT 下载」的说法（snippet-only）；官方口径是 #7/#8——**资源订阅下载必须有可用的 PT 站点**。**以官方为准**，并把 #8 的「整理刮削不需要 PT」作为无 PT 用户的出路。
3. **「V2 已停止支持（2026-08-31）」未获官方证实。** 来自 Doker Hub 页 snippet，官方文档未见。**不写进成品**，或标注为未证实。
4. **`W-BASIC:54` 存疑**：`为了控制用户数量避免大规范泛滥使用`，HTML 原文（`<strong>` 内）亦如此，疑为站点笔误（疑为「大规模」）。**该半句不要引用**，只引 #7 的后半段。

---

## 五、实践指引（供大纲与写作）

- **主线骨架**：选型（为何 V3）→ 准备（网络 / 目录 / 配套软件）→ 部署（小白版 Compose）→ 首次初始化 → 认证 → 下载器 / 媒体服务器 / 站点 → 整理模式 → 外网访问 → 避坑。
- **必须前置讲清的门槛**：没有 PT 站点账号 → 只能做「文件整理刮削」，不能搜片/订阅/下载（#8）。这条不前置，读者会在认证那步才发现。
- **目录规划是易错点**：硬链接要求下载目录与媒体库在同一根目录下（#17、#18），与库内既有 `[[流媒体与影音/小雅 fnOS 单容器部署/03 动手前准备]]` 的目录规划口径可对齐。
- **fnOS 特有**：Community 层尚无一手来源，涉及 fnOS 实机细节（端口占用、路径命名 `/vol1/1000/...`）时按「社区经验 + 待验证」处理。

---

## 六、C 路（不依赖 PT）：库内既有笔记已覆盖

C 路**不新收集**，直接复用 vault 既有笔记，成品以双链引用：

| 库内笔记 | 覆盖内容 |
| --- | --- |
| `[[流媒体与影音/小雅 fnOS 单容器部署/小雅 fnOS 单容器部署（总览）]]` | fnOS 上单容器部署小雅（AList 资源层）、选型、避坑、运维（全 7 章） |
| `[[流媒体与影音/Strm流文件与302播放详解]]` | STRM 指针文件与 302 直链原理 |
| `[[流媒体与影音/网盘影视播放与本地存储的取舍]]` | 网盘播放 / 302 / 本地下载三路线选型 |
| `[[流媒体与影音/硬件解码vs软件解码]]` | 解码方式选型 |

**A 与 C 的接口**：MoviePilot V3 的「文件整理刮削」可与网盘流媒体路线共存——即用 C 路解决「片子从哪来」，用 A 路的整理/刮削能力管本地已下载的片。此接口是**推断**（见 §三 A2 推论），成品须标明依据。

---

## 七、开放问题（不得在成品中拍脑袋）

1. fnOS 上 `3000` 端口是否真被应用中心浏览器占用、改端口是否真会失败——**一手未证实**。
2. 视频 `BV1egF7eFERT` 正文与 `blog.010322.xyz` 配置内容——**均未取得**（站点不可达）。成品若提「视频里的做法」，只能引其标题/简介（`01_explore_result.md` 候选 8）。
3. 飞牛官方论坛实机贴（tid=605/1165）抓取被反爬拦截——**未取到**。
4. V2 是否已正式停止支持——**未证实**。

---

## 八、下游交接

- **给 `outline-generator`**：按 §五 的骨架出章；务必把「无 PT 只能整理刮削」写成独立小节或独立 Callout。
- **给 `chapter-writer`**：引文只从 §三 引文行取，并按「文件:行」回 `sources/` 复核；`snippet-only` 与 §七 的开放问题**不得**写成确定结论；§三 A2 的**推断**必须显式标注为推断。
- **给 `note-beautifier`**：C 路以双链指向库内既有笔记，不要复制其正文；MOC 更新走 `[[流媒体与影音 MOC]]`。

### 自检记录

- 引文逐字核对：**英文整句 2 处**（归档横幅句、README 镜像句），校验器 V 全绿（原始来源命中 2 / 仅中间产物命中 0 / 未命中 0）；**中文引文 12 处**为人工逐字比对（校验器只覆盖整句英文引文），行号已回 `sources/` 打点收紧（#8→`ready.txt:71-83`、#14→`install.txt:200-204`、#16→`install.txt:214`、#17→`install.txt:440`）。
- 数值重新计数：端口/版本号/超时秒数（`3000`、`3001`、`120`、`4.3.9`、`3.0`、`4.8.0.45`）均回原文核对。
- 命令：
  `python .claude/scripts/note-citation-check.py ./workspace/nastool-fnos-deploy --mode verbatim --file 02_deep_research.md`
  输出：`英文整句引文 2 处；原始来源命中 2 / 仅自己中间产物命中 0 / 未命中 0` ✅。

> 校验器缺陷已修：原实现只按 `chapters/*.md` 判空，导致文档化的 P2 命令（只给 `--file`）提前退出、V 根本没跑。已在 canonical `.codex/scripts/note-citation-check.py` 把空判改为「body_files 或 extra_files 至少有一个」，同步后 `.claude/` 一致。
