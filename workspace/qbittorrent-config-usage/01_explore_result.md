# qBittorrent 下载器的配置与使用 — P1 探测结果（explore）

> 本文件是中间产物：引文与数值请回 `sources/` 按行号核对；未取回正文的候选一律标 `snippet-only`，**不得当证据使用**。
> 生成时间：2026-10-07 ｜ run_id：`qbittorrent-config-usage` ｜ 阶段：P1（探测）
> 目标环境：fnOS（飞牛 NAS）+ Docker ｜ 深度：上手 ｜ 基础：有了解
> 取回日期：本批候选的取回/检索日期均为 **2026-10-07**。

---

## 1. 探测方法

三个独立透镜并行探测，每透镜 4–6 个候选，按 canonical URL 去重：

| 透镜 | 覆盖 |
| --- | --- |
| L1 装起来 | 官方是否提供容器镜像、第三方镜像文档坐标、WebUI 首次登录口径 |
| L2 配好 | 设置项一手文档、下载目录/硬链接口径、完成回调 |
| L3 用起来 | Tracker/DHT/PEX 一手说明、连通性排错、PT 分享率与 H&R 出处 |

去重后 **15 个候选**（L1 5 + L2 5 + L3 6 − 1 重复），另附 **3 条已验证线索**。
重复项：`Explanation of Options in qBittorrent`（L2 #1 与 L3 #2 同一 URL，已合并，取 L2 的评分与日期）。

---

## 2. 候选来源清单

### 2.1 官方（official）

| # | 标题 | URL | 相关性 | 日期 | 证据形态 | 评分 |
| --- | --- | --- | --- | --- | --- | --- |
| O1 | qbittorrent/docker-qbittorrent-nox | `https://github.com/qbittorrent/docker-qbittorrent-nox` | 官方容器镜像仓库，含 WebUI 端口与首登口令说明 | `—`（repo push 2026-09-28） | `fetched` | 5 |
| O2 | Explanation of Options in qBittorrent | `https://github.com/qbittorrent/qBittorrent/wiki/Explanation-of-Options-in-qBittorrent` | 逐项解释设置的官方合并页（唯一设置项一手页） | 2026-09-03 | `fetched` | 5 |
| O3 | How to Run External Programs | `https://github.com/qbittorrent/qBittorrent/wiki/External-programs-How-to` | 指明完成钩子在 Options > Downloads；未列占位符 | 2026-09-03 | `fetched` | 4 |
| O4 | The BitTorrent Protocol Specification (BEP 3) | `https://www.bittorrent.org/beps/bep_0003.html` | Tracker announce 协议规范原文 | `—` | `fetched` | 5 |
| O5 | Things we need to know to help you with "speed" issues | `https://github.com/qbittorrent/qBittorrent/wiki/Things-we-need-to-know-to-help-you-with-%27speed%27-issues` | 官方「无速度」排错自查清单 | `—` | `snippet-only` | 4 |
| O6 | ngosang/trackerslist | `https://github.com/ngosang/trackerslist` | 每日更新的公共 Tracker 列表项目 | 2026-10-06（pushed_at） | `fetched`（API） | 5 |

- O1 仓库状态：`pushed_at: 2026-09-28T20:00:47Z` / `archived: false`。官方镜像同时发 Docker Hub（`qbittorrentofficial/qbittorrent-nox`，README 记为 homepage）与 GHCR；WebUI 在主机 `8080`；标签口径 `QBT_VERSION`（`latest` / 版本号 / `alpha`），另有 `lt2` 变体。
- O5 直连 fetch 被重定向到 wiki 首页，正文未取回 → **`snippet-only`**，P2 选定方向若依赖须先补 fetch。
- O6 仓库状态：`pushed_at: 2026-10-06T22:09:41Z` / `archived: false` / stars ≈ 55288 / GPL-2.0。

### 2.2 镜像或发行方（issuer / distro）

| # | 标题 | URL | 相关性 | 日期 | 证据形态 | 评分 |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | LinuxServer.io qbittorrent 镜像文档 | `https://docs.linuxserver.io/images/docker-qbittorrent/` | LinuxServer 版镜像官方文档，含端口与首登口令 | `—`（变更日志最新条目 05.07.26） | `fetched` | 5 |
| D2 | 文件整理（MoviePilot Wiki · reorganize） | `https://raw.githubusercontent.com/jxxghp/MoviePilot-Wiki/main/reorganize.md` | 硬链接须同盘/同映射路径 | 2026-09-30 | `fetched` | 5 |
| D3 | 下载（MoviePilot Wiki · download） | `https://raw.githubusercontent.com/jxxghp/MoviePilot-Wiki/main/download.md` | 下载目录须与下载器一致及 Docker 路径映射 | 2026-09-26 | `fetched` | 4 |
| D4 | Deluge（Arch Wiki） | `https://wiki.archlinux.org/title/Deluge` | 连通性排错：conntrack 丢弃合法 BT 流量与 NOTRACK | `—` | `snippet-only` | 4 |

- D1：坐标 `lscr.io/linuxserver/qbittorrent:latest`；WebUI 在 `8080`；临时口令在启动时打到容器日志；`WEBUI_PORT` 须同时改两侧端口映射；标签 `latest`（libtorrent v2）/ `libtorrentv1`。
- D2/D3 仓库 `jxxghp/MoviePilot-Wiki`：`pushed_at: 2026-10-07T01:48:59Z` / `archived: false`。
- D4 正文经 Arch Wiki 镜像页搜索摘要读到，canonical 页直连被反爬（Anubis）拦截 → **`snippet-only`**。

### 2.3 社区经验（community，仅作已标注的运维经验）

| # | 标题 | URL | 相关性 | 日期 | 证据形态 | 评分 |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | SuperNG6/Docker-qBittorrent-Enhanced-Edition | `https://github.com/SuperNG6/Docker-qBittorrent-Enhanced-Edition` | 增强版 fork 的第三方容器镜像 | 2026-10-05（pushed_at） | `fetched`（仓库元数据；镜像用法 `snippet-only`） | 4 |
| C2 | 飞牛 qbittorrent 下载器容器化安装与注意事项 2026 | `https://gao4.top/202605041.html/` | fnOS 上跑官方镜像的实操，含首登口令与 CSRF 调整 | 2026-05-04 | `fetched` | 4 |
| C3 | FNOS 飞牛 OS 使用 docker-compose 安装 qbittorrent | `http://blog.liukewen.cn/2024/36TSGY2.html` | fnOS 上用 compose 跑 LinuxServer 镜像的实操 | 2024-12-23 发布 / 2026-09-21 更新 | `fetched` | 3 |
| C4 | Hardlinks and Instant Moves (Atomic-Moves)（TRaSH-Guides） | `https://raw.githubusercontent.com/TRaSH-Guides/Guides/master/docs/File-and-Folder-Structure/Hardlinks-and-Instant-Moves.md` | 硬链接限制清单（不跨文件系统/分区；exFAT 不支持） | 2026-06-22 | `fetched` | 4 |
| C5 | Private BitTorrent Trackers Face Credit Crunch（TorrentFreak） | `https://torrentfreak.com/private-bittorrent-trackers-face-credit-crunch-090331/` | 私种分享率经济为何难以人人维持（科普背景） | 2009-03-31（URL 日期） | `snippet-only` | 4 |

- C1 上游 `c0re100/qBittorrent-Enhanced-Edition`（`pushed_at: 2026-10-03T18:52:14Z` / `archived: false` / 自述 `[Unofficial]`）**只发 release 二进制，不发官方镜像**；社区镜像里维护最勤的是本仓（Docker Hub `superng6/qbittorrentee`）。
- C4 仓库 `TRaSH-Guides/Guides`：`pushed_at: 2026-09-28T02:14:41Z` / `archived: false`。
- C5 是行业媒体科普，**不是**任何具体 Tracker 的规则页。

### 2.4 已验证线索（未计入 15 条候选）

| 线索 | URL | 层级 | 证据形态 |
| --- | --- | --- | --- |
| How to Disable DHT, PeX, and LPD | `https://github.com/qbittorrent/qBittorrent/wiki/How-to-Disable-DHT,-PeX,-and-LPD` | 官方 | `fetched`（末次编辑 2024-05-01） |
| H&R 罚则说明 | `https://salivity.github.io/bittorrent/article/torrent-hit-and-run-penalties-explained` | 社区经验 | `snippet-only` |
| 私有站最短做种时长要求 | `https://salivity.github.io/bittorrent/article/private-tracker-minimum-seed-time-requirements` | 社区经验 | `snippet-only` |

未采纳：`terrent.net`、`makeuseof.com` 及各类 SEO 站（营销站，按来源纪律排除）。

---

## 3. 三问答案（部署侧，L1）

| 问题 | 结论 | 依据 |
| --- | --- | --- |
| 官方到底提不提供容器镜像？ | **提供**，且发 Docker Hub + GHCR 双渠道 | O1（README + GitHub API） |
| 常见第三方镜像文档在哪？ | LinuxServer 官方文档页（D1）；增强版为社区镜像（C1） | D1、C1 |
| WebUI 首次登录的一手说明在哪？ | O1 README（4.6.1 起启动生成临时口令打到 stdout，`docker logs` 取）与 D1 Application Setup（独立一手来源，互为印证） | O1、D1 |

---

## 4. 口径风险（必须在后续阶段显式处理）

1. **首登口令分代**：4.6.1 起启动时生成临时口令写入容器日志；4.6.1 之前为默认口令。笔记须写清分界，不能只给一种。
2. **「增强版」是社区 fork，不是官方版本**：`c0re100/qBittorrent-Enhanced-Edition` 自述 `[Unofficial]`，与官方是两个不同项目。
3. **旧笔记版本口径过时**：既有 `qBittorent/` 4 篇写「稳定版 v5.1.x / 测试版 v5.2.0rc1」，与实测不符（官方最新稳定版 **v5.2.4**，2026-09-28）。不得沿用。
4. **大小写口径**：上级分册表格写 `Qbittorrent`，官方品牌写法为 **`qBittorrent`**。
5. **与上级分册的接口口径**：下载目录映射（`/downloads`）、版本下限（`>= 4.3.9`）、完成回调命令须与 `nastool 家庭影院 fnOS 部署` 一致，冲突时以一手来源为准并记录差异。

---

## 5. 覆盖缺口（coverage gaps）

| 缺口 | 状态 | 影响 |
| --- | --- | --- |
| **PT 分享率 / H&R 无一站式一手规则页可达** | ❌ 无 | 本轮无任何具体 Tracker 的 rules/FAQ 进入结果；C5 为行业媒体科普，只能作通用背景。**建议 P2 以用户的目标站 rules/FAQ 为准**，或明确标为「通用背景，非某站规则」 |
| **完成回调占位符（`%N`/`%F`/`%D`）官方未列** | ⚠️ 薄 | O2 仅一句概述、O3 只是指路桩，两页都没有占位符清单；占位符目前只见于第三方。P2 要么回官方源码取一手，要么标社区经验 |
| **fnOS 官方侧口径（飞牛论坛）不可达** | ❌ 被拦 | `club.fnnas.com` 两帖（部署帖 tid=71666、官方 compose 分享 tid=61383）WAF 反爬，三次 fetch 只拿到验证页 → 只有 `snippet-only`。如需飞牛侧更权威口径，P2 需换浏览器工具（`browsermcp` / `opencli-browser`） |
| **`snippet-only` 待补 fetch（3 条）** | ⚠️ 待办 | O5（speed issues）、D4（Arch Wiki Deluge）、C5（TorrentFreak）；L2 侧另有 C4 的硬链接结论已有 D2 一手印证，不阻塞 |
| **连通性排错的一手性** | ⚠️ 弱 | D4（Arch Wiki）是发行方文档、非 qBittorrent 官方；官方排错内容目前只有 O5 且未取回正文 |
| **RSS 订阅** | ⚠️ 薄 | O2 中 RSS 不作为标签页出现，官方 RSS 一手说明暂无专门页 |

---

## 6. 方向菜单（供用户选择）

| 方案 | 内容 | 预计章数 | 说明 |
| --- | --- | --- | --- |
| **A（推荐）全量主线** | 是什么 → 装起来（Docker/镜像/首登）→ 配好（端口/目录与硬链接/分类/限速/代理/回调）→ 用起来（加种/RSS/Tracker/私种与分享率/排错） | ~6 章 | 与 P0「单篇、上手」一致；覆盖 L1+L2+L3；若超 ~30 KB 再建议拆分册 |
| B 只做「装 + 配」 | 部署 + WebUI 关键设置（不做使用/PT 部分） | ~3–4 章 | 最省事，但上级分册缺的「怎么用」仍留空 |
| C 只做「用起来」 | 加种/RSS/Tracker/PT 分享率与 H&R/排错 | ~3 章 | 前提是读者已能跑起来；与 nastool 分册接口弱相关 |
| D 以「对接 MoviePilot」为轴 | 部署 + 与上级分册的接口口径（`/downloads`、版本下限、回调命令）+ 排错 | ~4 章 | 最贴近用户当前场景，但概念铺垫会压缩 |

**推荐 A**：与 P0 确认的「单篇 · 上手 · 补上上级分册的缺口」最贴合；B/C 会各缺一半，D 会牺牲小白友好度。

---

## 7. 预估 P2 范围

- 方向 A：需引用来源约 **12–15 件**（官方 ≥6、镜像/发行方 ≥3、社区经验 ≤4）。优先补齐 3 条 `snippet-only`（O5、D4、C5）；占位符与 H&R 两项按缺口处理方式决定是否回源码 / 标社区经验。
- 方向 B：约 8–10 件，重心在 O1/O2/D1/C2/C3。
- 方向 C：约 8–10 件，重心在 O4/O6、O3、D4、C5 与线索表。
- 方向 D：约 9–12 件，需额外对齐上级分册的接口口径（`流媒体与影音/nastool 家庭影院 fnOS 部署/` 第 3、7 章）。

---

## 8. 交接说明

- 全部 15 条候选的 URL 均来自实际检索或 fetch；标 `fetched` 者正文已取回，标 `snippet-only` 者**仅供 P2 补抓线索**。
- 本文件不含成句引文与需留档的数值；P2 落 `02_deep_research.md` 时按来源纪律逐条回 `sources/` 核对行号。
- 下一步：等待用户从第 6 节方向菜单选择方向；未选定前不进入 P2。
