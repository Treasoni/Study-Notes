## 第 2 章 装起来：镜像三选一、卷映射与首次登录

上一章认清了 qBittorrent 的位置，这一章把它装起来。在 fnOS + Docker 上，装 qBittorrent 只有三件事：**选一个镜像、把两个目录映射进去、拿到首次登录口令**。看着简单，每件都有坑——镜像选错会让环境变量静默失效，目录写成相对路径会直接报错，口令取法还取决于版本号。本章把三件事逐个讲清，最后给两版可照抄的 `docker-compose.yml`。

### 2.1 结论先行：装起来只需三件事

先把三件事和各自的坑摆出来：

| 要做的事 | 怎么做 | 常见坑 |
| --- | --- | --- |
| 选镜像 | 官方 / LinuxServer / 增强版社区镜像 三选一 | 换镜像后环境变量名不一样（2.2） |
| 映两个目录 | 给容器开两扇「门」，通向你的硬盘：`/config` 与 `/downloads` | 写相对路径会直接起不来（2.3） |
| 拿首登口令 | 看版本：≥ `4.6.1` 去容器日志抄临时口令 | 只记住一种取法（2.4） |

> [!tip] 大白话
> 把容器想成**一台租来的、没有硬盘的电脑**：它一重建就把东西忘光，所以得把你自己硬盘上的两个文件夹「租」给它——一个放配置（`/config`），一个放下载的文件（`/downloads`）。这个「租房」动作就是**卷映射**，门必须开在你硬盘上的一个真实路径，不能是容器里的一条相对路径。

### 2.2 三选一：三个镜像，差在环境变量前缀

| | 官方镜像 | LinuxServer 镜像 | 增强版社区镜像 |
| --- | --- | --- | --- |
| 镜像坐标 | `qbittorrentofficial/qbittorrent-nox`[^c2-la1-3] | `lscr.io/linuxserver/qbittorrent`[^c2-la2-11] | 无官方 Docker 镜像（见下） |
| WebUI 端口变量 | `QBT_WEBUI_PORT`[^c2-la1-61] | `WEBUI_PORT`[^c2-la2-100] | 视第三方镜像而定 |
| BT 端口变量 | `QBT_TORRENTING_PORT`[^c2-la1-58] | `TORRENTING_PORT`[^c2-la2-101] | 视第三方镜像而定 |
| 默认端口 | 8080 / 6881[^c2-la1-63][^c2-la1-60] | 8080 / 6881[^c2-la2-91] | 视第三方镜像而定 |
| 首登口令 | 有版本分界（2.4）[^c2-la1-144] | 临时口令打到容器日志[^c2-la2-24] | 视第三方镜像而定 |

**这里最关键的一行是「环境变量名」**：官方镜像用带前缀的 `QBT_*`，LinuxServer 用不带前缀的 `WEBUI_PORT` / `TORRENTING_PORT`——**两套名字互不识别**[^c2-la1-58][^c2-la2-101]。你从网上抄一份别人的 compose 贴到自己的镜像上，名字对不上就会被**静默忽略**：容器照常启动，端口却还是默认值，你怎么改都不生效。这是新手最常见的坑。

至于「增强版」：它**没有官方 Docker 镜像**，本册不给它的容器坐标——其 README 的 Repository 一节只列 AppImage / AUR / Debian / openSUSE / Ubuntu / macOS / Windows 原生包[^c2-la3-37]。要容器化只能另找社区维护的第三方镜像，多一层不可控。**本册主线用官方镜像**，需要别的口味时再自行评估。

一句话选法：跟着本册主线就选官方镜像；如果你这一套别的容器都已经在用 LinuxServer 生态，那就选 LinuxServer 版，两者功能等价，差别只在环境变量名。无论选谁，**记牢你选的那套变量名**，别混用。

顺带统一写法：镜像名和文档里一律是 `qBittorrent`（`q` 小写、`B` 大写），这是官方规范写法[^c2-la1-1]；网上 `Qbittorrent`、`QBittorrent` 等写法都非规范。

### 2.3 卷映射：两个根目录，`/config` 与 `/downloads`

卷映射就是把你硬盘上的两个目录「接」进容器，容器里用固定的内部路径去访问：

| 容器内路径 | 装什么 | 你该给它配什么 |
| --- | --- | --- |
| `/config` | qBittorrent 的全部配置（含 `qBittorrent.conf`、种子状态）[^c2-la2-105] | 一个专属于它的空目录 |
| `/downloads` | 下载下来的文件[^c2-la2-106] | 你的下载目录（要和 MoviePilot 看到的一致，第 3 章） |

**两条硬规则**。第一条，卷必须写**宿主机上的绝对路径**，官方有明确原话：

| 它管什么 | 官方原文 | 说人话 |
| --- | --- | --- |
| 卷路径怎么写 | 「Using a relative path will not work.」[^c2-la1-67] | 卷必须写宿主机上的绝对路径；写相对路径，容器直接起不来。 |

第二条，`/config` 单独给一个干净目录，别和别的程序共用，否则配置文件会互相覆盖。一句话记法：**`/config` 一人一个抽屉，`/downloads` 大家一起用**（它要和 MoviePilot 的下载目录是同一个，第 3 章展开）。

> [!tip] 大白话
> 把 `/config` 想成 qBittorrent 的**记事本**，`/downloads` 想成它的**收件箱**。记事本要放在只属于它的抽屉里（否则和别人的笔记混在一起），收件箱则要和 MoviePilot 的收件箱**是同一个**（否则 MoviePilot 收不到快递，第 3 章细说）。

### 2.4 WebUI 首次登录：口令随版本变（F1）

装好后，浏览器打开 `http://<你的设备地址>:<WebUI 端口>`（默认 8080）[^c2-la1-142]。登录口令**取决于版本**，两种情形都要记清，别只会一种：

| 版本 | 首登怎么拿口令 | 出处 |
| --- | --- | --- |
| ≥ `4.6.1`（新） | 启动时**生成一个临时口令打印到容器日志**，用 `docker logs` 抄出来 | 官方镜像 README[^c2-la1-144] |
| < `4.6.1`（旧） | 用**默认口令**，无需去日志里找 | 官方镜像 README[^c2-la1-152] |

官方对「新版本」这一幕有原话，资格够硬，单独摆出来：

| 官方原文 | 说人话 |
| --- | --- |
| 「For newer qBittorrent versions (≥ 4.6.1), qBittorrent will generate a temporary password and print it to the console (via stdout).」[^c2-la1-144] | 较新的版本启动时会生成一个**临时口令**，并打印到控制台（标准输出）——这就是你要抄下来的那串。 |

没有附着控制台，就用这条命令看日志[^c2-la1-149]：`docker logs qbittorrent-nox`。LinuxServer 镜像同理，它的临时口令也会打到容器日志里[^c2-la2-24]。

而**旧版本（< `4.6.1`）**没有这个机制，直接用默认账号口令登录就行，不必去日志里翻[^c2-la1-152]。所以「口令到底去哪拿」这件事，先看清你装的是哪个版本——这就是 `4.6.1` 这个分界的由来。

登录后**立刻改密码**[^c2-la1-154]：WebUI 里 `Tools` 菜单 → `Options...` → `WebUI` 标签页 → `Authentication`。不改的话，很多镜像**每次启动都会重新生成一个临时口令**，你下次又登不进去[^c2-la2-25]。

### 2.5 动手实践（新手可跳过）

> [!tip] 新手可跳过
> 这一节是可直接照抄的配制。不打算自己写 compose 的读者可以跳过，直接照搬下面的文件、改掉路径即可。

**官方镜像版**（环境变量用 `QBT_*`[^c2-la1-58][^c2-la1-61]）：

```yaml
# docker-compose.yml（官方镜像版）
services:
  qbittorrent:
    image: qbittorrentofficial/qbittorrent-nox:latest   # 也可换 GitHub 镜像 ghcr.io/qbittorrent/docker-qbittorrent-nox:latest
    container_name: qbittorrent-nox
    environment:
      - QBT_LEGAL_NOTICE=confirm        # 只有你已阅读其法律声明才填 confirm
      - QBT_TORRENTING_PORT=6881        # BT 端口，默认 6881
      - QBT_WEBUI_PORT=8080             # WebUI 端口，默认 8080
      - PUID=1000                       # 运行身份，默认 1000
      - PGID=1000
      - TZ=Asia/Shanghai
    volumes:
      - /vol1/1000/docker/qbittorrent/config:/config      # 绝对路径，不能用相对路径
      - /vol1/1000/media/downloads:/downloads
    ports:
      - 8080:8080
      - 6881:6881                       # BT，tcp
      - 6881:6881/udp                   # BT，udp（两个都要）
    read_only: false                    # 用了 PUID/PGID 就必须关掉只读
    stop_grace_period: 30m              # 官方要求：默认 10s 太短，会损坏文件
    restart: unless-stopped
```

**LinuxServer 镜像版**（环境变量**不带** `QBT_` 前缀[^c2-la2-100][^c2-la2-101]）：

```yaml
# docker-compose.yml（LinuxServer 镜像版）
services:
  qbittorrent:
    image: lscr.io/linuxserver/qbittorrent:latest
    container_name: qbittorrent
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - WEBUI_PORT=8080                 # 注意：不带 QBT_ 前缀
      - TORRENTING_PORT=6881            # 注意：不带 QBT_ 前缀
    volumes:
      - /vol1/1000/docker/qbittorrent/config:/config
      - /vol1/1000/media/downloads:/downloads
    ports:
      - 8080:8080
      - 6881:6881
      - 6881:6881/udp
    stop_grace_period: 10s
    restart: unless-stopped
```

几个必须照做的小点：

- **路径改成你自己的**：`/vol1/1000/...` 是 fnOS 常见的卷布局示意，按你机器上的实际路径替换[^c2-la1-67]。
- **官方镜像的 `stop_grace_period` 不能省**：官方镜像警告默认只有 10 秒，太短会打断关闭流程、损坏文件，要求改成 30 分钟（官方版 compose 已写 `stop_grace_period: 30m`）[^c2-la1-118]；上面的 **LinuxServer 版**沿用其文档示例的 `10s`[^c2-la2-60]，两者各随镜像口径，别混用。
- **用了 `PUID`/`PGID` 就要关只读**：官方镜像默认以只读文件系统运行，而 `PUID`/`PGID` 与只读不兼容，必须写 `read_only: false`[^c2-la1-123]。
- **想省掉端口映射也有别的写法**：社区配方里出现过 `network_mode: host`，让容器直接用宿主机网络[^c2-la5-32]；代价是它会把服务直接暴露在宿主网络上、并和其它占端口的程序冲突，本册不默认采用。
- **改端口要「两侧同改」**：只改环境变量、不改 `ports:` 映射，或反过来，都会不生效——这正是第 3 章要讲透的一件事。

取首登口令（≥ `4.6.1`）[^c2-la1-149]：

```shell
docker logs qbittorrent-nox
```

> [!warning] 可选：改 conf 去掉 https 跳转（社区经验）
> 有人会先停容器、再编辑 `qBittorrent.conf`，在 `[Preferences]` 里加 `WebUI\HostHeaderValidation=false` 与 `WebUI\CSRFProtection=false`，以绕开某些浏览器强制 https 的问题[^c2-la4-35]。这是**社区经验**（非官方口径）；它同时**降低了安全性**（关掉了跨站请求防护），请只在你清楚后果时使用，并记得**先停容器再改**，否则配置会被重置[^c2-la4-42]。

一个小提醒：上面的镜像名、端口、卷路径都回官方镜像 README 与 LinuxServer 文档核对过；网上社区配方（含 fnOS 论坛）只作交叉参考，不作为精确口径——曾见过配方里 `PUID`/`PGID` 给成 `0`（以 root 运行），本册不放这种值[^c2-la5-20]。

### 本章小结

- 装起来只需三件事：**选镜像 → 映两个目录（`/config`、`/downloads`）→ 拿首登口令**。
- 三个镜像的功能等价，最容易踩的差别是**环境变量前缀**：官方用 `QBT_*`，LinuxServer 用不带前缀的名字，两套互不识别，抄错会被静默忽略（F2）。
- 卷必须写**宿主机上的绝对路径**；`/config` 要独占一个干净目录，`/downloads` 要和 MoviePilot 看到的**是同一个**。
- 首登口令**随版本变**：`≥ 4.6.1` 去容器日志抄临时口令，`< 4.6.1` 用默认口令；进去后**立刻改密码**（F1）。
- 官方镜像两个必改项：`stop_grace_period: 30m`（默认 10 秒太短，会损坏文件）、用了 `PUID`/`PGID` 就要 `read_only: false`。

### 下一章预告

容器起来了，但「装好」不等于「配好」。第 3 章讲**配好**的两件核心事：**BT 端口要映射、改端口必须「两侧同改」**，以及下载目录与硬链接口径——为什么下载目录必须和媒体端**映射同一个宿主目录**，否则硬链接会失效。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `Using a relative path will not work.` | 用相对路径不行。 | `LA-1 · sources/l1-1_official-docker-readme.md:69` |
| 2 | `For newer qBittorrent versions (≥ 4.6.1), qBittorrent will generate a temporary password and print it to the console (via stdout).` | 对于较新的 qBittorrent 版本（≥ 4.6.1），qBittorrent 会生成一个临时口令并打印到控制台（标准输出）。 | `LA-1 · sources/l1-1_official-docker-readme.md:144` |
| 3 | `You must then change username/password in the web UI section of settings.` | 随后你必须在设置的 Web UI 一栏里修改用户名/口令。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:25` |

## 脚注

[^c2-la1-1]: LA-1 · `sources/l1-1_official-docker-readme.md:1`。
[^c2-la1-3]: LA-1 · `sources/l1-1_official-docker-readme.md:3`（官方镜像仓库坐标）。
[^c2-la1-58]: LA-1 · `sources/l1-1_official-docker-readme.md:58-60`（`QBT_TORRENTING_PORT`，未设时默认 `6881`）。
[^c2-la1-60]: LA-1 · `sources/l1-1_official-docker-readme.md:60`。
[^c2-la1-61]: LA-1 · `sources/l1-1_official-docker-readme.md:61-63`（`QBT_WEBUI_PORT`，未设时默认 `8080`）。
[^c2-la1-63]: LA-1 · `sources/l1-1_official-docker-readme.md:63`。
[^c2-la1-67]: LA-1 · `sources/l1-1_official-docker-readme.md:67-72`（`/config` 与 `/downloads` 卷说明）。
[^c2-la1-118]: LA-1 · `sources/l1-1_official-docker-readme.md:115-118`（`stop_grace_period: 30m`）。
[^c2-la1-123]: LA-1 · `sources/l1-1_official-docker-readme.md:121-125`（`PUID`/`PGID` 默认 `1000`，与只读不兼容）。
[^c2-la1-142]: LA-1 · `sources/l1-1_official-docker-readme.md:142`。
[^c2-la1-144]: LA-1 · `sources/l1-1_official-docker-readme.md:144-145`。
[^c2-la1-149]: LA-1 · `sources/l1-1_official-docker-readme.md:146-150`。
[^c2-la1-152]: LA-1 · `sources/l1-1_official-docker-readme.md:152`。
[^c2-la1-154]: LA-1 · `sources/l1-1_official-docker-readme.md:154-156`（登录后改密码的路径）。
[^c2-la2-11]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:11`。
[^c2-la2-24]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:24`。
[^c2-la2-25]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:25`。
[^c2-la2-60]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:60`（LinuxServer 的 compose 示例 `stop_grace_period:"10s"`，标注 `#optional`）。
[^c2-la2-91]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:91-93`（端口表：`8080:8080` / `6881:6881` / `6881:6881/udp`）。
[^c2-la2-100]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:100`。
[^c2-la2-101]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:101`。
[^c2-la2-105]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:105`（`/config` 卷）。
[^c2-la2-106]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:106`（`/downloads` 卷）。
[^c2-la3-37]: LA-3 · `sources/l1-3_enhanced-fork-readme.md:37-82`（Repository 节）。
[^c2-la4-35]: LA-4 · `sources/l1-4_fnOS-community-1.md:35-36`（社区经验，非官方口径）。
[^c2-la4-42]: LA-4 · `sources/l1-4_fnOS-community-1.md:42`。
[^c2-la5-20]: LA-5 · `sources/l1-5_fnOS-community-2.md:20`（社区 compose 示例，仅作交叉参考）。
[^c2-la5-32]: LA-5 · `sources/l1-5_fnOS-community-2.md:24,32`（社区 compose 出现 `network_mode: host`；第 24 行「或者使用host模式」，仅作交叉参考）。
