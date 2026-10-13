# 阶段 2 深度研究 — qBittorrent 下载器的配置与使用

> 本文件是**中间产物（handoff artifact），不是权威终点**：引文与数值请回 `sources/` 按行号核对。
> 所有 claim 均已绑 `sources/<文件>:<行号>`；行号在**原始抓取文件**上用 `grep -n` 复核（不基于去标签重排文本）。
>
> 深读日期：2026-10-07 ｜ 运行：`qbittorrent-config-usage` ｜ 方向：**A. 全量主线（约 6 章）**
> 深读组：3 组（A 部署 / B 配置 / C 使用与排错），每组 1 个 delegate（≤3/phase）
> 目标环境：fnOS（飞牛 NAS）+ Docker ｜ 深度：上手 ｜ 基础：有了解

---

## 一、范围

本阶段只服务一件事：**在 fnOS 上用 Docker 把 qBittorrent 装起来、配好、日常用顺，并与上级分册 `nastool 家庭影院 fnOS 部署` 的接口口径对齐**。

- **在范围内**：官方/第三方镜像选型与部署；WebUI 首登与端口；关键设置项（连接 / 下载目录 / 队列与限速 / 代理 / 完成回调）；加种、RSS、Tracker；PT 私种与分享率、H&R 的**通用机制**；连通性与「无速度」排错。
- **不在范围内**：qBittorrent 源码实现细节（唯一例外是回调占位符的一手取证）；**具体 PT 站的规则与阈值**（无一手来源，见第六节缺口）；种子内容的合规问题。

---

## 二、来源总表（24 件快照 / 19 件 claim 来源 + 5 件 API 元数据）

**24** 个快照全部落在 `workspace/qbittorrent-config-usage/sources/`，全部 `fetched`（**本阶段无 `snippet-only`**）。
tier 含义：`官方` = qBittorrent 官方文档/官方仓库/规范原文；`镜像或发行方` = 镜像方或下游项目/发行版文档；`社区经验` = 第三方实操与科普，仅作已标注的运维经验。

下表列出 **19** 件 claim 来源（LA 5 / LB 6 / LC 8）；另有 **5** 件 JSON 为仓库元数据（GitHub API 原始响应），只用于核实 `pushed_at` / `archived`，不承载正文论断，见本节末补充。

| ID | 标题 | 文件（sources/ 内） | tier | evidence_form | 取回日期 |
| --- | --- | --- | --- | --- | --- |
| LA-1 | qBittorrent-nox Docker Image（官方仓库 Readme.md） | `sources/l1-1_official-docker-readme.md` | 官方 | fetched | 2026-10-07 |
| LA-2 | qbittorrent - LinuxServer.io（镜像方文档） | `sources/l1-2_linuxserver-qbittorrent.md` | 镜像或发行方 | fetched | 2026-10-07 |
| LA-3 | qBittorrent Enhanced Edition（增强版上游仓库 README） | `sources/l1-3_enhanced-fork-readme.md` | 官方（增强版上游） | fetched | 2026-10-07 |
| LA-4 | 飞牛 fnOS 上跑 qbittorrent 容器（社区实操，孤岛） | `sources/l1-4_fnOS-community-1.md` | 社区经验 | fetched | 2026-10-07 |
| LA-5 | FNOS 飞牛OS 用 docker-compose 装 qbittorrent（社区实操，KewenBlogs） | `sources/l1-5_fnOS-community-2.md` | 社区经验 | fetched | 2026-10-07 |
| LB-1 | Explanation of Options in qBittorrent（qBittorrent 官方 Wiki） | `sources/l2-1_options-explained.md` | 官方 | fetched | 2026-10-07 |
| LB-2 | External programs How-to（qBittorrent 官方 Wiki） | `sources/l2-2_external-programs.md` | 官方 | fetched | 2026-10-07 |
| LB-3 | MoviePilot Wiki 文件整理 | `sources/l2-3_moviepilot-reorganize.md` | 官方（项目方 Wiki） | fetched | 2026-10-07 |
| LB-4 | MoviePilot Wiki 下载 | `sources/l2-4_moviepilot-download.md` | 官方（项目方 Wiki） | fetched | 2026-10-07 |
| LB-5 | TRaSH-Guides 硬链接与即时移动（Hardlinks and Instant Moves） | `sources/l2-5_trash-hardlinks.md` | 社区经验 | fetched | 2026-10-07 |
| LB-6 | 完成回调占位符的一手取证（qBittorrent 上游源码 master） | `sources/l2-6_placeholder-source.md` | 官方（上游源码 primary） | fetched | 2026-10-07 |
| LC-1 | The BitTorrent Protocol Specification (BEP 3) | `sources/l3-1_bep3-tracker-protocol.md` | 官方（bittorrent.org 规范） | fetched | 2026-10-07 |
| LC-2 | Things we need to know to help you with 'speed' issues（qBittorrent 官方 wiki） | `sources/l3-2_speed-issues.md` | 官方（qBittorrent 官方 wiki） | fetched | 2026-10-07 |
| LC-3 | Deluge - ArchWiki（发行版社区 wiki） | `sources/l3-3_archwiki-deluge.md` | 镜像或发行方（ArchWiki，社区维护） | fetched | 2026-10-07 |
| LC-4 | ngosang/trackerslist（公共 Tracker 列表项目） | `sources/l3-4_trackerslist-readme.md` | 社区经验（第三方开源项目） | fetched | 2026-10-07 |
| LC-5 | How to Disable DHT, PeX, and LPD（qBittorrent 官方 wiki） | `sources/l3-5_disable-dht-pex-lpd.md` | 官方（qBittorrent 官方 wiki） | fetched | 2026-10-07 |
| LC-6 | Private BitTorrent Trackers Face Credit Crunch（TorrentFreak，行业媒体科普） | `sources/l3-6_torrentfreak-credit-crunch.md` | 社区经验（行业媒体报道，2009-03-31；**非任何 PT 站的官方规则**） | fetched | 2026-10-07 |
| LC-7 | Torrent Hit and Run Penalties Explained（社区文章） | `sources/l3-7_hit-and-run-penalties.md` | 社区经验（第三方科普文章，**非某站官方规则**） | fetched | 2026-10-07 |
| LC-8 | Private Tracker Minimum Seed Time Requirements（社区文章） | `sources/l3-8_minimum-seed-time.md` | 社区经验（第三方科普文章，**非某站官方规则**） | fetched | 2026-10-07 |


> 补充（5 件 API 元数据，各与同前缀 claim 来源同源，用于核实 `pushed_at` / `archived`，未单列行）：
> `l1-1b_official-docker-api.json`（↔ LA-1）、`l1-3b_enhanced-fork-api.json`（↔ LA-3；亦为引文 `Unofficial qBittorrent Enhanced, based on qBittorrent` 的一手出处）、`l2-3b_moviepilot-wiki-api.json`（↔ LB-3/LB-4）、`l2-5b_trash-guides-api.json`（↔ LB-5）、`l3-4_trackerslist-api.json`（↔ LC-4）。
> 即 sources/ 共 **24** 件 = 19 claim 来源 + 5 元数据。

---

## 三、Claim / 来源映射（三组原始笔记）

> 以下三节为三个深读组的**原始产出**，逐条 claim 均带 `sources/<文件>:<行号>`。行号基准＝原始抓取文件。

## 组 A：部署

### LA-1 · qBittorrent-nox Docker Image（官方仓库 Readme.md）
- 文件: `sources/l1-1_official-docker-readme.md` ｜ tier: 官方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方镜像发布在 Docker Hub `qbittorrentofficial/qbittorrent-nox`，GitHub 仓库为 `qbittorrent/docker-qbittorrent-nox` ｜ `sources/l1-1_official-docker-readme.md:3`
  - 可用 GHCR 镜像替代 Docker Hub：`ghcr.io/qbittorrent/docker-qbittorrent-nox:${QBT_VERSION}` ｜ `sources/l1-1_official-docker-readme.md:112`
  - 支持架构含 `linux/amd64`、`linux/arm64/v8`（另含 386/armv6/armv7/riscv64）｜ `sources/l1-1_official-docker-readme.md:8`
  - `QBT_WEBUI_PORT` 控制 WebUI 端口，未设置时默认 `8080` ｜ `sources/l1-1_official-docker-readme.md:63`
  - `QBT_TORRENTING_PORT` 控制 BT 流量端口，未设置时默认 `6881` ｜ `sources/l1-1_official-docker-readme.md:60`
  - `QBT_LEGAL_NOTICE` 必须填 `confirm` 才能运行（确认已读法律声明）｜ `sources/l1-1_official-docker-readme.md:53`
  - `QBT_VERSION` 可取 `latest`、指定 tag（示例 `4.4.5-1`）或周构建 `alpha`，另有 libtorrent v2 变体 `lt2` ｜ `sources/l1-1_official-docker-readme.md:56`
  - 卷映射固定两个挂载点：`/config`（配置）与 `/downloads`（下载），且须用宿主机绝对路径，相对路径无效 ｜ `sources/l1-1_official-docker-readme.md:69`
  - 运行示例默认带 `--read-only` 与 `--stop-timeout 1800` ｜ `sources/l1-1_official-docker-readme.md:91`
  - 停机超时默认仅 10 秒太短会损坏文件，必须覆盖为 `--stop-timeout 1800`（Compose 用 `stop_grace_period: 30m`）｜ `sources/l1-1_official-docker-readme.md:118`
  - `PUID`/`PGID` 可改进程 UID/GID，默认均为 `1000`；设了它们就必须去掉 `--read-only`，且 rootless 模式下无效 ｜ `sources/l1-1_official-docker-readme.md:123`
  - `PAGID` 设附加组，`.env` 里改 `PUID`/`PGID` 也要去掉 `--read-only` ｜ `sources/l1-1_official-docker-readme.md:127`
  - `UMASK` 设进程 umask，默认继承自 Alpine Linux ｜ `sources/l1-1_official-docker-readme.md:134`
  - 时区由 `TZ` 控制，默认继承 Alpine，多半是 `UTC` ｜ `sources/l1-1_official-docker-readme.md:119`
  - 登录地址 `http://<your_docker_host_address>:8080` ｜ `sources/l1-1_official-docker-readme.md:142`
  - 首登口令分界版本为 `4.6.1`：≥4.6.1 生成临时密码打印到 console（stdout）；<4.6.1 默认 `admin/adminadmin` ｜ `sources/l1-1_official-docker-readme.md:144`
  - 无 console 时用 `docker logs qbittorrent-nox` 查看密码 ｜ `sources/l1-1_official-docker-readme.md:149`
  - 旧版本（<4.6.1）默认用户名/口令逐字为 `admin/adminadmin` ｜ `sources/l1-1_official-docker-readme.md:152`
  - 仓库根目录含 `.env`、`docker-compose.yml`、`docker-stack.yml`、`entrypoint.sh` 文件 ｜ `sources/l1-1_official-docker-readme.md`（GitHub contents API 列目录）
  - 仓库元数据：`pushed_at` = `2026-09-28T20:00:47Z`，`archived` = `false`，`default_branch` = `main`，stars 432 ｜ GitHub API `repos/qbittorrent/docker-qbittorrent-nox`
  - 注：`Readme.md` 在 `master` 与 `main` 之外的路径均 404；仓库 README 实际文件名首字母大写（`Readme.md`）
- 关键实体（端口/路径/口令/标签等，逐字）: 镜像 `qbittorrentofficial/qbittorrent-nox`；GHCR `ghcr.io/qbittorrent/docker-qbittorrent-nox:${QBT_VERSION}`；WebUI 默认端口 `8080`；BT 端口默认 `6881`；卷 `/config`、`/downloads`；环境变量 `QBT_LEGAL_NOTICE=confirm`、`QBT_VERSION=latest|4.4.5-1|alpha|lt2`、`QBT_WEBUI_PORT`、`QBT_TORRENTING_PORT`、`PUID`、`PGID`、`PAGID`、`UMASK`、`TZ`；默认 UID/GID `1000`/`1000`；停机 `--stop-timeout 1800`；分界版本 `4.6.1`；旧版口令 `admin/adminadmin`；`docker logs qbittorrent-nox`

### LA-2 · qbittorrent - LinuxServer.io（镜像方文档）
- 文件: `sources/l1-2_linuxserver-qbittorrent.md` ｜ tier: 镜像或发行方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 拉取方式：`lscr.io/linuxserver/qbittorrent:latest` 会自动取到匹配当前架构的镜像 ｜ `sources/l1-2_linuxserver-qbittorrent.md:11`
  - 支持架构 `x86-64`（tag `amd64-<version tag>`）与 `arm64`（tag `arm64v8-<version tag>`）｜ `sources/l1-2_linuxserver-qbittorrent.md:15`
  - 版本标签只有两个：`latest`（用 libtorrent v2 的稳定版）与 `libtorrentv1`（用 libtorrent v1 的稳定版）｜ `sources/l1-2_linuxserver-qbittorrent.md:21`
  - WebUI 在 `<your-ip>:8080`，`admin` 用户的临时密码会在容器启动时打印到容器日志 ｜ `sources/l1-2_linuxserver-qbittorrent.md:24`
  - 必须在 WebUI 设置里改用户名/口令，不改则每次容器启动都会重新生成新口令 ｜ `sources/l1-2_linuxserver-qbittorrent.md:25`
  - 改 WebUI 端口要同时改 `-p` 两侧端口并把 `WEBUI_PORT` 设为新端口（否则 CSRF/端口映射出问题）｜ `sources/l1-2_linuxserver-qbittorrent.md:28`
  - 端口示例逐字：改到 8123 需 `-p 8123:8123` 且 `-e WEBUI_PORT=8123` ｜ `sources/l1-2_linuxserver-qbittorrent.md:29`
  - `TORRENTING_PORT` 同理：改到 6887 需 `-p 6887:6887`、`-p 6887:6887/udp` 且 `-e TORRENTING_PORT=6887` ｜ `sources/l1-2_linuxserver-qbittorrent.md:32`
  - 端口映射表：`8080:8080` = WebUI；`6881:6881` = tcp 连接端口；`6881:6881/udp` = udp 连接端口 ｜ `sources/l1-2_linuxserver-qbittorrent.md:91`
  - 环境变量：`PUID=1000`、`PGID=1000`、`TZ=Etc/UTC`、`WEBUI_PORT=8080`、`TORRENTING_PORT=6881` ｜ `sources/l1-2_linuxserver-qbittorrent.md:97`
  - 卷映射：`/config`（存全部相关配置文件）与 `/downloads`（下载文件落盘位置）｜ `sources/l1-2_linuxserver-qbittorrent.md:105`
  - Compose 示例中卷为 `/path/to/qbittorrent/appdata:/config` 与 `/path/to/downloads:/downloads`，端口 `8080:8080`、`6881:6881`、`6881:6881/udp` ｜ `sources/l1-2_linuxserver-qbittorrent.md:55`
  - 杂项参数：`--stop-timeout=`（种子多时需加大以保证干净关闭）、`--read-only=true`、`--user=1000:1000` ｜ `sources/l1-2_linuxserver-qbittorrent.md:110`
  - Compose 默认 `stop_grace_period: "10s"`（标为 optional）｜ `sources/l1-2_linuxserver-qbittorrent.md:80`
  - 支持用 `FILE__` 前缀从文件（Docker secrets）注入环境变量 ｜ `sources/l1-2_linuxserver-qbittorrent.md:60`
  - umask 可用可选参数 `-e UMASK=022` 覆盖；umask 是减权限不是 chmod ｜ `sources/l1-2_linuxserver-qbittorrent.md:70`
  - 宿主卷目录须属主与 `PUID`/`PGID` 一致；本例 `PUID=1000`、`PGID=1000`，用 `id your_user` 查自己的值 ｜ `sources/l1-2_linuxserver-qbittorrent.md:74`
- 关键实体（端口/路径/口令/标签等，逐字）: 镜像 `lscr.io/linuxserver/qbittorrent:latest`；标签 `latest`、`libtorrentv1`；架构 tag `amd64-<version tag>`、`arm64v8-<version tag>`；WebUI `8080`；BT `6881`（tcp）/`6881/udp`；环境变量 `PUID=1000`、`PGID=1000`、`TZ=Etc/UTC`、`WEBUI_PORT=8080`、`TORRENTING_PORT=6881`、`UMASK=022`；卷 `/config`、`/downloads`；`stop_grace_period: "10s"`；示例端口 `8123`、`6887`；`--read-only=true`、`--user=1000:1000`；`FILE__` 前缀；用户名 `admin`

### LA-3 · qBittorrent Enhanced Edition（增强版上游仓库 README）
- 文件: `sources/l1-3_enhanced-fork-readme.md` ｜ tier: 官方（增强版上游） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 增强功能：自动封禁迅雷、QQ、百度、Xfplay、DLBT 及离线下载器 ｜ `sources/l1-3_enhanced-fork-readme.md:6`
  - 可选「自动封禁来自中国的未知 Peer」，默认 `OFF` ｜ `sources/l1-3_enhanced-fork-readme.md:8`
  - 可选「自动更新公共 Tracker 列表」，默认 `OFF` ｜ `sources/l1-3_enhanced-fork-readme.md:10`
  - 可选「自动封禁 BitTorrent 媒体播放器 Peer」，默认 `OFF` ｜ `sources/l1-3_enhanced-fork-readme.md:12`
  - 支持 Peer 白名单/黑名单 ｜ `sources/l1-3_enhanced-fork-readme.md:14`
  - 发行渠道为桌面/原生包：AppImage、Arch AUR（含 nox AUR）、Debian、openSUSE、Ubuntu PPA、macOS Homebrew、Windows（Chocolatey/Scoop），无官方 Docker 镜像说明 ｜ `sources/l1-3_enhanced-fork-readme.md:39`
  - Arch 用户可装 `qbittorrent-enhanced-git`（AUR）或 `qbittorrent-enhanced-nox-git`（nox AUR）｜ `sources/l1-3_enhanced-fork-readme.md:45`
  - macOS 安装命令逐字 `brew install c0re100-qbittorrent` ｜ `sources/l1-3_enhanced-fork-readme.md:66`
  - Windows 安装：`choco install qbittorrent-enhanced`；Scoop 需先 `scoop bucket add dorado https://github.com/chawyehsu/dorado` 再 `scoop install qbittorrent-enhanced` ｜ `sources/l1-3_enhanced-fork-readme.md:74`
  - 增强功能相关 bug 上报地址为 `https://github.com/c0re100/qBittorrent-Enhanced-Edition/issues` ｜ `sources/l1-3_enhanced-fork-readme.md:98`
  - 仓库元数据：`description` = `[Unofficial] qBittorrent Enhanced, based on qBittorrent`，`pushed_at` = `2026-10-03T18:52:14Z`，`archived` = `false`，`default_branch` = `v5_2_x`，stars 26744 ｜ GitHub API `repos/c0re100/qBittorrent-Enhanced-Edition`
  - README 全篇不含任何 Docker 镜像坐标、端口或 WebUI 说明（对容器化部署为空缺）｜ `sources/l1-3_enhanced-fork-readme.md`（全篇 grep 无 docker/image）
- 关键实体（端口/路径/口令/标签等，逐字）: 上游 `c0re100/qBittorrent-Enhanced-Edition`；默认分支 `v5_2_x`；AUR 包 `qbittorrent-enhanced-git`、`qbittorrent-enhanced-nox-git`；`brew install c0re100-qbittorrent`；`choco install qbittorrent-enhanced`；Scoop bucket `dorado`；功能开关默认值均 `OFF`；无 Docker 端口/卷/口令信息

### LA-4 · 飞牛 fnOS 上跑 qbittorrent 容器（社区实操，孤岛）
- 文件: `sources/l1-4_fnOS-community-1.md` ｜ tier: 社区经验 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 教程目标版本为 `qBittorrent v5.2.0` ｜ `sources/l1-4_fnOS-community-1.md:8`
  - 镜像坐标用官方镜像并锁 tag：`qbittorrentofficial/qbittorrent-nox:5.2.0-1` ｜ `sources/l1-4_fnOS-community-1.md:25`
  - 容器名 `qbittorrent-nox`；restart 策略 `unless-stopped` ｜ `sources/l1-4_fnOS-community-1.md:25`
  - 环境变量：`PUID=1000`、`PGID=1001`、`TZ=Asia/Shanghai`、`QBT_TORRENTING_PORT=6881`、`QBT_WEBUI_PORT=8080` ｜ `sources/l1-4_fnOS-community-1.md:25`
  - 卷映射：`/config:/config`（左宿主右容器）与 `/: /downloads`（整盘挂到下载目录）｜ `sources/l1-4_fnOS-community-1.md:25`
  - 端口映射：宿主机 `8089` → 容器 `8080`，另加 `6881:6881` 与 `6881:6881/udp` ｜ `sources/l1-4_fnOS-community-1.md:25`
  - 先启动容器再停止，然后改配置：在 `qbittorrent.conf`（如 `~/.config/qBittorrent/qBittorrent.conf`）的 `[Preferences]` 加两行 ｜ `sources/l1-4_fnOS-community-1.md:32`
  - 需加 `WebUI\HostHeaderValidation=false` 与 `WebUI\CSRFProtection=false` ｜ `sources/l1-4_fnOS-community-1.md:35`
  - 必须停容器再改配置，否则配置会被重置 ｜ `sources/l1-4_fnOS-community-1.md:42`
  - 取首登口令：`sudo docker logs qbittorrent-nox`，日志里找自动生成的密码 ｜ `sources/l1-4_fnOS-community-1.md:46`
  - 访问 `http://192.168.100.231:8089/`，用户名 `admin`、密码为日志打印值（须去掉 https 的 s 走 http）｜ `sources/l1-4_fnOS-community-1.md:52`
  - 进后台后必须改密码，否则每次启动容器会自动生成新密码 ｜ `sources/l1-4_fnOS-community-1.md:53`
  - 注：该页抓取后 compose 段被压成单行（第 25 行），无独立换行，正文其余为代码块目录/复制提示等模板文本；全文仅 54 行 / 2034 字节 ｜ `sources/l1-4_fnOS-community-1.md:25`
- 关键实体（端口/路径/口令/标签等，逐字）: 镜像 `qbittorrentofficial/qbittorrent-nox:5.2.0-1`；容器名 `qbittorrent-nox`；`PUID=1000`、`PGID=1001`、`TZ=Asia/Shanghai`、`QBT_TORRENTING_PORT=6881`、`QBT_WEBUI_PORT=8080`；端口 `8089:8080`、`6881:6881`、`6881:6881/udp`；卷 `/config:/config`、`/:/downloads`；配置键 `WebUI\HostHeaderValidation=false`、`WebUI\CSRFProtection=false`；配置路径 `~/.config/qBittorrent/qBittorrent.conf`；取密码 `sudo docker logs qbittorrent-nox`；访问 `http://192.168.100.231:8089/`；用户名 `admin`

### LA-5 · FNOS 飞牛OS 用 docker-compose 装 qbittorrent（社区实操，KewenBlogs）
- 文件: `sources/l1-5_fnOS-community-2.md` ｜ tier: 社区经验 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 用 LinuxServer 镜像并锁 tag：`linuxserver/qbittorrent:4.6.6`，容器名 `qbittorrent` ｜ `sources/l1-5_fnOS-community-2.md:20`
  - 环境变量：`PUID=0`、`PGID=0`、`TZ=Asia/Shanghai`、`UMASK_SET=022`、`WEBUI_PORT=6700`、`TORRENTING_PORT=6701` ｜ `sources/l1-5_fnOS-community-2.md:20`
  - 端口映射：`6700:6700`（WebUI）、`6701:6701`、`6701:6701/udp` ｜ `sources/l1-5_fnOS-community-2.md:20`
  - 卷映射四条：config、theme、downloads、watch（`/vol1/1000/...` 前缀为飞牛存储路径）｜ `sources/l1-5_fnOS-community-2.md:20`
  - `TORRENTING_PORT` 注释建议取 `20000-65535` 区间值（默认 6881）｜ `sources/l1-5_fnOS-community-2.md:20`
  - 另给 host 网络模式变体，在原 compose 基础上追加 `network_mode: host` 且去掉 `ports` 段 ｜ `sources/l1-5_fnOS-community-2.md:32`
  - 默认账号为 `admin`，密码需到容器运行日志里找 ｜ `sources/l1-5_fnOS-community-2.md:36`
  - 日志成功样例：WebUI 在 `http://localhost:6700`，用户名 `admin`，临时密码 `4X72ucMPJ`，并提示 `You should set your own password in program preferences` ｜ `sources/l1-5_fnOS-community-2.md:44`
  - UI 主题用 VueTorrent v2.14.1，下载后放进 theme 目录，WebUI 里填路径 `/theme/vuetorrent` ｜ `sources/l1-5_fnOS-community-2.md:49`
  - compose 来源标注为飞牛官方论坛帖 `https://club.fnnas.com/forum.php?mod=viewthread&tid=2741&extra=page%3D1` ｜ `sources/l1-5_fnOS-community-2.md:20`
  - 注：两段 compose 在第 20、32 行被压成单行输出；第 16、28、40 行是代码行号占位文本（`123456789101112...`），非配置内容 ｜ `sources/l1-5_fnOS-community-2.md:16`
- 关键实体（端口/路径/口令/标签等，逐字）: 镜像 `linuxserver/qbittorrent:4.6.6`；容器名 `qbittorrent`；`PUID=0`、`PGID=0`、`TZ=Asia/Shanghai`、`UMASK_SET=022`、`WEBUI_PORT=6700`、`TORRENTING_PORT=6701`；端口 `6700:6700`、`6701:6701`、`6701:6701/udp`；卷 `/vol1/1000/docker/qbittorrent/config:/config`、`/vol1/1000/docker/qbittorrent/theme:/theme`、`/vol1/1000/media/qbittorrent/downloads:/downloads`、`/vol1/1000/media/qbittorrent/downloads:/watch`；`network_mode: host`；账号 `admin`；临时密码样例 `4X72ucMPJ`；主题路径 `/theme/vuetorrent`；VueTorrent `v2.14.1`

### 矛盾与缺口
- **WebUI 端口口径不统一**：官方与 LinuxServer 默认都是 8080（LA-1:63、LA-2:46/91），但社区实操把宿主端口改成 8089→容器 8080（LA-4:25）或 6700→6700（LA-5:20）。LA-4 只改宿主侧（`8089:8080`）却仍把 `QBT_WEBUI_PORT` 留 8080，与 LA-2「必须同时改两侧 + 设 WEBUI_PORT」的规则相冲——两种做法不能混用。
- **首登口令分界版本**：官方明确以 `4.6.1` 为界，≥4.6.1 用临时密码、<4.6.1 用 `admin/adminadmin`（LA-1:144、152）。LinuxServer 文档只讲「临时密码」不写旧版默认（LA-2:24），与官方口径一致；LA-5 用 4.6.6 也走临时密码（LA-5:44），与之吻合。缺口：增强版（LA-3）README 完全没有登录/口令说明。
- **PUID/PGID 取值冲突**：官方与 LinuxServer 默认均 `1000:1000`（LA-1:123、LA-2:49-50），而 LA-4 用 `1000:1001`（LA-4:25）、LA-5 直接用 `0:0`（root，LA-5:20）。root 运行与官方/发行方推荐的降权取向相反。
- **环境变量命名口径不同（易混用致失效）**：官方镜像用 `QBT_` 前缀（`QBT_WEBUI_PORT`/`QBT_TORRENTING_PORT`，LA-1:61-63），LinuxServer 用无前缀（`WEBUI_PORT`/`TORRENTING_PORT`，LA-2:46-47）。LA-4 用官方镜像故用 `QBT_`，LA-5 用 LinuxServer 故用无前缀，两套不能互换。
- **停机超时默认差异大**：官方要求覆盖到 `--stop-timeout 1800` / `stop_grace_period: 30m`，否则默认 10 秒会损坏文件（LA-1:118）；LinuxServer 文档示例默认只给 `stop_grace_period: "10s"` 并提示可加大（LA-2:80、110）。社区两篇（LA-4、LA-5）均未设置该超时。
- **卷映射口径不一**：官方/发行方均为 `/config` + `/downloads`（LA-1:99-100、LA-2:105-106）；LA-5 额外映射 `/theme` 与 `/watch`（LA-5:25）；LA-4 把整个 `/` 挂到 `/downloads`（LA-4:25），风险与标准做法差异明显。
- **增强版容器镜像坐标空缺**：LA-3（增强版上游）README 只给 AppImage 与各平台原生包，无任何 Docker 镜像/端口/卷说明。要在 fnOS 上容器化跑增强版，须依赖第三方镜像（本组未覆盖），是本组最大缺口。
- **LA-4 快照质量偏低**：页面正文疑似渲染残缺，compose 段被压成单行、混入代码内容，全文仅 54 行 / 2034 字节；可作为「fnOS 上确实用官方镜像 + 改 conf 关 CSRF/HostHeaderValidation + 从日志取密码」的佐证，但不宜作为端口/卷的精确来源。LA-5 同样存在 compose 压行（第 20、32 行）与代码行号占位文本（第 16、28、40 行）。

## 组 B：配置

### LB-1 · Explanation of Options in qBittorrent（qBittorrent 官方 Wiki）

- 文件: `sources/l2-1_options-explained.md` ｜ tier: 官方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方明确说明选项是**按标签页（tab）分组**组织的，不是单页堆叠；选项入口是 `Alt` + `O` 或 Tools → Options。 ｜ `sources/l2-1_options-explained.md:11`
  - 标签页一级标题依次为 `Behavior`、`Downloads`、`Connection`、`Speed`、`BitTorrent`、`Web UI`、`Advanced`，另有 `Deprecated options` 小节。 ｜ `sources/l2-1_options-explained.md:35,59,91,110,115,127,129,193`
  - 下载位置相关的设置项集中在 `Downloads` 标签页的 `Hard Disk` 小节，第一个就是默认保存位置。 ｜ `sources/l2-1_options-explained.md:66,67`
  - 「保存到哪」不是一个单值，wiki 至少列出四项路径型设置：默认保存位置、未完成种子临时目录、.torrent 备份目录、已完成种子的 .torrent 备份目录。 ｜ `sources/l2-1_options-explained.md:67,70,73,74`
  - 「未完成文件加扩展名」是独立开关，作用是把 `Hello.mp3` 暂存为 `Hello.!qb`，下载完成后再改回原文件名。 ｜ `sources/l2-1_options-explained.md:71`
  - 完成回调在 wiki 里的标题是 `Run an external program on torrent completion`，位于 `Downloads` 标签页下。 ｜ `sources/l2-1_options-explained.md:89`
  - **该小节正文只有一句话**，未列出任何占位符、示例命令或脚本要求：全文即「This allows you to run a program on finishing certain types of torrents in a certain location.」。 ｜ `sources/l2-1_options-explained.md:90`
  - `Advanced` 标签页的 qBittorrent 专有项，wiki 直接指向源码文件 `src/gui/advancedsettings.cpp` 作为一手文档，等于承认 wiki 不是设置项的唯一权威。 ｜ `sources/l2-1_options-explained.md:130`
  - `Advanced` 中唯一与「路径数量」有关的默认值是保存路径历史长度。 ｜ `sources/l2-1_options-explained.md:145`
- 关键实体（端口/路径/默认值等，逐字）: `Save path history length — (default: 8)`；`Append .!qb extension`；`Hello.!qb`；`Alt` + `O`；`Tools` → `Options`；`src/gui/advancedsettings.cpp`；`include/libtorrent/settings_pack.hpp`

### LB-2 · External programs How-to（qBittorrent 官方 Wiki）

- 文件: `sources/l2-2_external-programs.md` ｜ tier: 官方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方 how-to 确认**存在**「完成时运行外部程序」这一能力，并给出设置位置：`Options` > `Downloads`。 ｜ `sources/l2-2_external-programs.md:12`
  - 对 bash 脚本的唯一硬性提示是必须先赋予可执行权限。 ｜ `sources/l2-2_external-programs.md:14`
  - **该页实质内容仅上述两句**，没有占位符说明、没有参数表、没有示例；页面其余部分是 wiki 导航模板。 ｜ `sources/l2-2_external-programs.md:12,14`
  - 因此「qBittorrent 官方 wiki 给出完成回调占位符清单」这一说法在本页**不成立**；占位符只能从源码取证（见 LB-6）。 ｜ `sources/l2-2_external-programs.md:12`
- 关键实体（端口/路径/默认值等，逐字）: `Options` > `Downloads`；`chmod 755 /path/to/script`

### LB-3 · MoviePilot Wiki 文件整理

- 文件: `sources/l2-3_moviepilot-reorganize.md` ｜ tier: 官方（项目方 Wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - MoviePilot 官方给出 qBittorrent 完成回调的**现成填法**：在 QB 设置→「下载完成时运行外部程序」处填入一条 curl，实现下载完成立即整理、不必等轮询。 ｜ `sources/l2-3_moviepilot-reorganize.md:15`
  - 该 curl 指向本机 `localhost:3000` 的 `transfer/now` 接口并带 `token=moviepilot`，文档同时声明地址、端口和 token 需按实际调整，curl 也可换成 wget。 ｜ `sources/l2-3_moviepilot-reorganize.md:15`
  - 整理模式在 `设定 -> 目录 -> 整理模式` 中调整，共六种：硬链接、软链接、复制、移动、Rclone 复制、Rclone 移动。 ｜ `sources/l2-3_moviepilot-reorganize.md:102,104-109`
  - **硬链接的前置条件被明确写为「同一磁盘/存储空间/映射路径」**，并说明可改硬链接后的文件名而不影响原文件做种、但不能改文件内容。 ｜ `sources/l2-3_moviepilot-reorganize.md:104`
  - 软链接的前置条件更严：原文件路径必须与生成软链接时一致，docker 环境下即**映射前后的目录路径需要一致**。 ｜ `sources/l2-3_moviepilot-reorganize.md:105`
  - 覆盖策略是独立设置项（`设定 -> 目录 -> 整理模式`），四档：从不覆盖 / 按大小覆盖 / 总是覆盖 / 仅保留最新版本。 ｜ `sources/l2-3_moviepilot-reorganize.md:112,114,116-119`
  - V2 起内建目录监控，无需第三方插件；下载器监控的自动整理间隔为固定轮询值。 ｜ `sources/l2-3_moviepilot-reorganize.md:81,82`
  - V1 的下载器监控需要手动打开 `下载文件自动整理` 开关，且多下载器时默认只监控第 1 个。 ｜ `sources/l2-3_moviepilot-reorganize.md:88,90`
  - 若使用插件式目录监控（实时）而非内建下载器监控，必须打开 qBittorrent 的「为不完整文件添加扩展名」选项，避免下载未完成就被移走。 ｜ `sources/l2-3_moviepilot-reorganize.md:94`
- 关键实体（端口/路径/默认值等，逐字）: `curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot"`；`localhost:3000`；`token=moviepilot`；`5分钟`；`/moviepilot/.config/rclone`；rclone 网盘配置名 `MP`；`AI_AGENT_ENABLE`

### LB-4 · MoviePilot Wiki 下载

- 文件: `sources/l2-4_moviepilot-download.md` ｜ tier: 官方（项目方 Wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 下载目录在 `设定` 中添加；docker 部署时下载目录对应的**根目录必须映射进容器**，否则文件落在容器内导致容器异常。 ｜ `sources/l2-4_moviepilot-download.md:13`
  - 路径口径的核心一句：**下载目录需要与下载器使用的目录一致**，docker 下通过映射路径对齐。 ｜ `sources/l2-4_moviepilot-download.md:15`
  - 手动下载时无法指定下载目录，目录由系统识别资源后自动判定。 ｜ `sources/l2-4_moviepilot-download.md:21`
  - 音乐整理同样要求「下载器路径与 MoviePilot 的目录映射一致」，且 MoviePilot 不建库、不播放，整理后交给外部媒体服务器扫描。 ｜ `sources/l2-4_moviepilot-download.md:27`
- 关键实体（端口/路径/默认值等，逐字）: `设定 -> 目录`；`AUTO_DOWNLOAD_USER`（V1 变量）

### LB-5 · TRaSH-Guides 硬链接与即时移动（Hardlinks and Instant Moves）

- 文件: `sources/l2-5_trash-hardlinks.md` ｜ tier: 社区经验 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 硬链接的三条硬性限制被单独放进 danger 块：不能对目录建硬链接、不能跨文件系统/分区/卷/挂载点建硬链接、exFAT 等文件系统不支持硬链接。 ｜ `sources/l2-5_trash-hardlinks.md:30`
  - 限制的成因解释：每个文件本身就是一条硬链接（指向文件系统上的数据块），**这就是它们受限于同一文件系统**的原因。 ｜ `sources/l2-5_trash-hardlinks.md:39`
  - 硬链接的三个行为后果：删任一副本不影响其它副本、只有全部副本删除后才回收空间、修改任一副本内容会影响所有副本（如改 mp3 标签会破坏做种）。 ｜ `sources/l2-5_trash-hardlinks.md:43,47,49,51`
  - 「即时移动（Atomic Move）」的定义是真正的移动，而非先复制到媒体目录再删除下载目录文件。 ｜ `sources/l2-5_trash-hardlinks.md:61`
  - 硬链接与即时移动的**双重前置条件**：所有路径必须在同一个文件系统上，并且还要满足权限——各应用必须能互相读写对方的文件。 ｜ `sources/l2-5_trash-hardlinks.md:73`
  - 权限由「应用运行的用户与组」「`UMASK`」「ownership」三者共同决定，并指向 Servarr Docker Guide 详述。 ｜ `sources/l2-5_trash-hardlinks.md:73`
  - 用户/组设定方式取决于镜像：LinuxServer.io 一类用 `PUID`/`PGID` 环境变量，另一类用 Docker 原生 `--user` / `user:`（`uid:gid`）。 ｜ `sources/l2-5_trash-hardlinks.md:75`
  - 给出两套推荐组合：多用户 + 共享组配 `UMASK 002`（目录 775、文件 664）；单用户配 `UMASK 022`（目录 755、文件 644）；并明确警告不要用 `UMASK 000`。 ｜ `sources/l2-5_trash-hardlinks.md:79,80,86`
- 关键实体（端口/路径/默认值等，逐字）: `exFAT`；`PUID`；`PGID`；`--user` / `user:`；`uid:gid`；`UMASK 002`；`UMASK 022`；`UMASK 000`；`775` (`drwxrwxr-x`)；`664` (`-rw-rw-r--`)；`755` (`drwxr-xr-x`)；`644` (`-rw-r--r--`)；`777`；`666`

### LB-6 · 完成回调占位符的一手取证（qBittorrent 上游源码 master）

- 文件: `sources/l2-6_placeholder-source.md` ｜ tier: 官方（上游源码 primary） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 占位符**确实存在**，且实现与展示分处两个文件：UI 说明文本在 `src/gui/optionsdialog.cpp`，实际替换逻辑在 `src/app/application.cpp`。 ｜ `sources/l2-6_placeholder-source.md:33,52`
  - UI 明确标注参数清单区分大小写（`Supported parameters (case sensitive):`），共列出 **13 个**占位符。 ｜ `sources/l2-6_placeholder-source.md:33`
  - 13 个占位符为 `%N` `%L` `%G` `%F` `%R` `%D` `%C` `%Z` `%T` `%I` `%J` `%K` `%M`，每个都有官方一句英文解释（如 `%F: Content path (same as root path for multifile torrent)`、`%D: Save path`）。 ｜ `sources/l2-6_placeholder-source.md:34-46`
  - UI 附一条官方 tip：参数含空白会被截断，需要用引号包裹（例如 `"%N"`）。 ｜ `sources/l2-6_placeholder-source.md:47`
  - 这些文本在运行时由代码 `m_ui->labelAutoRunParam->setText(autoRunStr)` 填入，`.ui` 里对应控件是空标签。 ｜ `sources/l2-6_placeholder-source.md:48,262`
  - 替换实现是 `Application::runExternalProgram(const QString &programTemplate, const BitTorrent::Torrent *torrent)`，逐字符扫描 `%` 后按下一字符分派。 ｜ `sources/l2-6_placeholder-source.md:52`
  - switch 分支与 UI 清单**逐字对应**：`C→filesCount`、`D→savePath`、`F→contentPath`、`G→tags`、`I→infoHash v1`、`J→infoHash v2`、`K→torrent id`、`L→category`、`M→comment`、`N→name`、`R→rootPath`、`T→currentTracker`、`Z→totalSize`。 ｜ `sources/l2-6_placeholder-source.md:74,98`
  - `%I` 与 `%J` 取不到时替换为字面量 `-`（`u"-"_s`）。 ｜ `sources/l2-6_placeholder-source.md:84,87`
  - 扫描方向为从串尾向前，并有一个 `--i` 回退以避免重复替换，官方注释举例的转义写法是 `%%N`。 ｜ `sources/l2-6_placeholder-source.md:115`
  - **执行位置**：源码里有**两个**触发点——`Application::torrentFinished`（完成时）与 `Application::torrentAdded`（添加时），F 组问题里的「完成回调」对应前者。 ｜ `sources/l2-6_placeholder-source.md:133`
  - 完成回调仅在开关打开时才执行，配置键为 `AutoRun/enabled`。 ｜ `sources/l2-6_placeholder-source.md:138,171`
  - 三个相关配置键及其默认值：`AutoRun/enabled` 默认 `false`、`AutoRun/program` 无默认、`AutoRun/ConsoleEnabled` 默认 `false`。 ｜ `sources/l2-6_placeholder-source.md:171,184,198`
  - UI 侧已从单一「完成时运行」扩展为两个可勾选分组：`Run on torrent added:` 与 `Run on torrent finished:`，外层分组标题为 `Run external program`。 ｜ `sources/l2-6_placeholder-source.md:221,239,215`
  - 「添加时」触发点同样受独立开关与独立程序串控制，配置键为 `AutoRun/OnTorrentAdded/Enabled`（默认 `false`）与 `AutoRun/OnTorrentAdded/Program`。 ｜ `sources/l2-6_placeholder-source.md:145,158,129`
  - 源码注释说明默认不给用户 shell 环境，理由是防止通过种子名等参数做命令注入（引用 issue 10925）。 ｜ `sources/l2-6_placeholder-source.md:54,57`

  （`sources/l2-6_placeholder-source.md` 的引用行号是该快照文件的内部行号；每行前缀即为该行在上游原始文件中的行号，例如快照第 33 行前缀为 `731:`，对应 `src/gui/optionsdialog.cpp:731`。）
- 关键实体（端口/路径/默认值等，逐字）: 占位符 `%N` `%L` `%G` `%F` `%R` `%D` `%C` `%Z` `%T` `%I` `%J` `%K` `%M`；转义 `%%N`；配置键 `AutoRun/enabled`、`AutoRun/program`、`AutoRun/ConsoleEnabled`、`AutoRun/OnTorrentAdded/Enabled`、`AutoRun/OnTorrentAdded/Program`；默认值 `false`；上游文件 `src/gui/optionsdialog.cpp`、`src/gui/optionsdialog.ui`、`src/app/application.cpp`、`src/base/preferences.cpp`；分支 `master`；issue `10925`

### 矛盾与缺口

- **官方 wiki 落后于源码**：LB-1（末次编辑 2026-09-03）在 `Downloads` 标签页下只有 `Run an external program on torrent completion` 一个小节且正文一句话（`l2-1_options-explained.md:89,90`）；而 master 源码 UI 已拆成 `Run on torrent added:` 与 `Run on torrent finished:` 两个可勾选分组（`l2-6_placeholder-source.md:239`）。写笔记时应以源码为准，并注明 wiki 未更新。
- **占位符清单在官方 wiki 中不存在**：LB-1 与 LB-2 都不列占位符（`l2-1_options-explained.md:90`、`l2-2_external-programs.md:12`）。本组得到的完整一手清单只有 LB-6 的 13 项；任何二手占位符表若要引用，只能以 `sources/l2-6_placeholder-source.md:34-46` 与 `:74,98` 为唯一比对基准。
- **qBittorrent 自身没有「硬链接」设置项**：LB-1 全篇未出现硬链接相关选项；硬链接是整理侧（MoviePilot 的 `设定 -> 目录 -> 整理模式`，`l2-3_moviepilot-reorganize.md:104`）的行为，qB 只负责下载完成的触发。二者是「触发方 + 执行方」关系，不是同一个配置点。
- **硬链接前置条件的两份口径需合并看**：MoviePilot 侧写作「同一磁盘/存储空间/映射路径」（`l2-3_moviepilot-reorganize.md:104`），TRaSH 侧写作「same file system」并补充权限/UMASK 条件（`l2-5_trash-hardlinks.md:30,73`）。MoviePilot 的口径缺少权限维度，只用 LB-3 会漏掉 UMASK/PUID-PGID 这一整块。
- **完成回调的路径口径无人显式声明**：LB-3/LB-4 要求「下载目录与下载器使用的目录一致」（`l2-4_moviepilot-download.md:15`），但都没有说明回调里 curl 的 `localhost:3000` 在 docker 下应填宿主地址还是容器名。这是一个实际配置缺口，本组来源无法回源回答。
- **LB-4 篇幅极短**（41 行，其中 30 行是 frontmatter 与后续章节），下载目录章节只有 3 句正文，未给出任何默认路径值；「默认下载目录是什么」在本组无官方来源可回源。
- **未取到的来源**：qBittorrent 官方对「保存路径」的默认值（如 Linux 下的默认下载目录）在 LB-1 中未给出具体字符串，只有设置项名称；`Settings` 页面亦未列出。该值需另找来源（如 qB 默认配置或源码 `preferences.cpp`），本组记为缺口。

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

---

## 四、跨组矛盾与需冻结口径

| # | 事项 | 处理口径 | 依据 |
| --- | --- | --- | --- |
| F1 | **首登口令分界版本 = 4.6.1** | ≥4.6.1 启动时生成临时口令、打到容器日志（`docker logs` 取）；<4.6.1 为默认口令。笔记须写清分界，不能只给一种 | LA-1 |
| F2 | **环境变量前缀不通用** | 官方镜像用 `QBT_*`（如 `QBT_WEBUI_PORT`）；LinuxServer 镜像用不带前缀的 `WEBUI_PORT` / `TORRENTING_PORT`。两者互不识别——照抄别家配方会静默失效 | LA-1 / LA-2 |
| F3 | **`qBittorrent` 是规范大小写** | 上级分册写的 `Qbittorrent` 为非规范写法；本册统一官方写法并在首次出现时点明 | P0 意图 + 官方来源 |
| F4 | **「增强版」是社区 fork，不是官方版本** | 独立项目，自述 `[Unofficial]`；其 README 内**没有 Docker 镜像**，容器化只能走社区镜像 | LA-3 + C1 |
| F5 | **设置项按「标签页」组织，但只有一张官方合并页** | 不存在 Connection / Downloads / BitTorrent / Speed / RSS 各自独立的官方页；引用按整页锚点 + 小节名 | LB-1 |
| F6 | **完成回调占位符以源码为准** | 官方两处 wiki 都**不列**占位符；占位符定义在 `src/gui/optionsdialog.cpp`（13 个、大小写敏感），触发点 `torrentFinished` / `torrentAdded`，配置键 `AutoRun/enabled` 默认 `false` | LB-6 |
| F7 | **官网 wiki 与源码不同步** | wiki（2026-09-03）仍写单一「完成时运行」；master 源码 UI 已拆成 `Run on torrent added` + `Run on torrent finished`。**以源码为准** | LB-6 |
| F8 | **qBittorrent 本身没有硬链接设置项** | 硬链接是 MoviePilot / 整理侧行为；前提是「同一文件系统 + 同一映射路径 + 权限」 | LB-1 / LB-5 / LB-3 |
| F9 | **H&R / 分享率只能写成通用机制** | 来源为 2009 行业媒体 + 第三方社区文，**非任何 PT 站官方规则**；笔记必须标注这一性质，并写明「具体阈值以目标站 rules/FAQ 为准」 | LC-6 / LC-7 / LC-8 |
| F10 | **ArchWiki Deluge 页不是 qBittorrent 来源** | 该页宿主是 Deluge，其端口号不得当作 qB 默认值；只借其连通性/连接跟踪（conntrack）原理 | LC-3 |
| F11 | **Tracker 列表条目数是变动值** | 引用须绑定 2026-10-07 快照，不得写成固定数字 | LC-4 |

---

## 五、实操指引要点（可进正文的落地结论）

1. **部署三选一**（须给对比表）：官方镜像 `qbittorrentofficial/qbittorrent-nox`（含 GHCR 同源镜像，标签口径 `QBT_VERSION`）／LinuxServer `lscr.io/linuxserver/qbittorrent`／增强版社区镜像。差异集中在**环境变量前缀**与**标签口径**。
2. **卷映射**：`/config` + `/downloads` 是两家的共同最小集；宿主路径要落到 fnOS 的实际卷（社区实操用 `/vol1/1000/...`）。
3. **下载目录口径**：与上级分册 `nastool 家庭影院 fnOS 部署` 一致——qBittorrent 与媒体管理端必须映射**同一宿主目录**，否则硬链接失效、整理变复制。
4. **完成回调**：位置在 `Options > Downloads`；命令按源码占位符写；上级分册给的 `curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot"` 需按实际地址/端口/token 调整（容器内 `localhost` 指向谁，本阶段**无一手来源**，见缺口 G4）。
5. **无速度自查**：按官方排错页的顺序（连接数、监听端口是否映射、上传槽位、半开连接、uTP、加密、IPv6、libtorrent 版本、DHT 节点数、代理/VPN）逐项排；**BT 端口未映射**是最常见的第一顺位原因。
6. **私种与 DHT**：PT 场景通常要关 DHT/PeX/LPD；官网页给的是关闭步骤，**定义**需另引 BEP 5 或官方选项页（见缺口 G2）。

---

## 六、未解缺口（不得用「大概」填，须显式标注或降级表述）

| ID | 缺口 | 现状 | 处置 |
| --- | --- | --- | --- |
| G1 | **具体 PT 站的分享率/H&R 规则与阈值** | 无一手来源 | 写成通用机制 + 标注「非某站规则」；具体以目标站 rules/FAQ 为准（F9） |
| G2 | **DHT / PeX / LPD 的「是什么」缺一手权威定义页** | 官方页只有 UI 全称与关闭步骤 | P3 前补 BEP 5 / 官方选项页；取不到就在正文标「定义以官方术语为准」 |
| G3 | **fnOS 官方侧口径（飞牛论坛）不可达** | `club.fnnas.com` 有 WAF 反爬 | 暂以社区实操（LA-4 / LA-5）为佐证并标注为社区经验；需要官方口径时用浏览器工具 |
| G4 | **容器内回调地址该填宿主还是容器名** | 无一手来源 | 正文按「需按你的实际网络填」表述，给两种情形的判断方法，不写死 |
| G5 | **qBittorrent 默认下载目录的具体值** | 本阶段无来源 | 不写具体默认值；只写「在哪改」（LB-1 Downloads→Hard Disk） |
| G6 | **LA-4 快照质量偏低**（compose 被压成一行、页面 2034 B） | 只能作佐证 | 不作端口/卷的精确来源；精确口径以 LA-1 / LA-2 为准 |
| G7 | **RSS 订阅官方一手说明** | 官方选项页未把 RSS 作标签页列出 | 若正文写 RSS，须标注来源薄弱或另找一手页 |

---

## 七、下游交接

- 本文件为 P3（大纲）与 P4（逐章写作）的**唯一素材入口**；写作时按 `sources/<文件>:<行号>` 回源，不得转述本文件的概括。
- **P2 自检行**：引文 11 处逐字核对（**校验器 V 全绿**：英文整句 11 处，原始来源命中 11 / 仅自己中间产物命中 0 / 未命中 0）/ 数值·路径 8 组重新计数核对（见下）。
  - 命令：`python3.12 .claude/scripts/note-citation-check.py workspace/qbittorrent-config-usage --mode verbatim --file 02_deep_research.md`
  - 结构自检：`python3 .claude/scripts/check-md-structure.py workspace/qbittorrent-config-usage/02_deep_research.md` → 扫描 1 文件、0 处可疑。
  - 数值·路径回源抽查（`grep -n` 于 `sources/` 原件）：① 首登口令分界 4.6.1（`l1-1:144` / `l1-1:152`）；② 占位符 **13** 个（`l2-6`：optionsdialog.cpp 732–744，逐字含 `%C/%D/%F/%G/%I/%J/%K/%L/%M/%N/%R/%T/%Z`）；③ `AutoRun/enabled` 默认 `false`（`l2-6:171`）；④ 触发点 `torrentAdded`/`torrentFinished`（`l2-6`：application.cpp 721–726、783/792）；⑤ 卷 `/config`+`/downloads`（`l1-1:99-100`）；⑥ `PUID/PGID=1000`（`l1-2:49-50`）；⑦ MoviePilot 回调 `curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot"`（`l2-3:15`，逐字）；⑧ WebUI `8080` 与 `WEBUI_PORT` 两侧同改（`l1-1:63/83/142` × `l1-2:24/28/52/57/73`）。
  - 纪律提醒：校验器 V **只覆盖英文整句引文**，中文引文与全部数值仍为人工逐字比对（上表已做）；写章时每条英文成句引文必须回 `sources/` 再比对一次并在章末「引文对照（原文 / 中译 / 出处）」表留档，`出处` 列宁空不猜写 `—`。
- **来源计数（当场重数）**：`sources/` **24 件**（19 claim 来源 + 5 API 元数据），全部 `fetched`，**无 `snippet-only`**；claim 层级 官方 10 / 镜像或发行方 2 / 社区经验 7。
- **给 writer 的硬约束**：F1–F11 必须逐条落地；G1–G7 不得用「大概」填。
- **与上级分册的接口**：`/downloads` 映射、版本下限（`>= 4.3.9`）、完成回调命令，须与 `流媒体与影音/nastool 家庭影院 fnOS 部署/` 第 3、7 章一致；冲突以一手来源为准并在正文记录差异。
