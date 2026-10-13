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
