# 第二章 部署（以 Docker Compose 为主）

上一章交代了它是什么、能做什么；这一章解决「让它真正跑起来」。部署是整个流程里最容易"手一抖就白忙"的一环：卷挂载写错，程序照样启动，但你打开界面看到的是一片空曲库；`/app/data` 忘了挂，容器重启一次，配置和激活状态全丢。所以本章不直接甩一份 compose 让你抄，而是先把容器里那几条**固定路径**讲透，再动手。本章以通用 Docker Compose 为主线，NAS 的平台差异收在 2.6。

## 2.1 部署前必须知道的容器路径与挂载概念

### 一句话定位：什么是「目录挂载」

官方名词解释里把绑定挂载（Bind Mounts）定义为容器与宿主机之间共享文件或目录的方式，原文是：「绑定挂载（Bind Mounts）是 Docker 容器与宿主机之间共享文件或目录的一种方式。它允许你将宿主机上的任意路径直接映射到容器内的指定路径。」[^c2-d5]

拆开看，一次挂载要写两个路径[^c2-d5]：

- **宿主机地址（Host Path）**：你的 NAS 或服务器上的真实目录，你想让容器用到的那份数据所在的地方。这个由你决定。
- **容器内地址（Container Path）**：数据在容器内部"出现"的位置。官方补了一句关键的话：「容器内的地址一般是开发者定义的路径位置，不可修改了。」[^c2-d5]

### 具体产物：这个项目定义了三个容器内路径

对 Music Tag Web 来说，右边那一列（容器内路径）是作者定死的，你只能换左边：

```text
宿主机（你的 NAS / 服务器）                容器内部（music-tag-web）
/你的音乐目录        ──── 挂载 ────►      /app/media      # 曲库
/你的配置目录        ──── 挂载 ────►      /app/data       # 配置与数据库
/你的下载目录        ──── 挂载 ────►      /app/download   # 后台刮削监控目录
```

三个路径各自的用途，官方 Compose 部署页给的说明是：`/path/to/your/music` 换成「你的 NAS 上音乐文件夹的绝对路径」，`/path/to/your/config` 换成「你新建的一个目录路径，用于存放应用程序的配置文件」，而 `/path/to/your/download` 换成「你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录」[^c2-d4]。

### 带具体值的可代入例子

假设你的曲库在 `/volume1/music`，想给容器配置单独建一个 `/volume1/docker/mtw`，下载目录是 `/volume1/downloads`，那么三条挂载就写成：

```text
/volume1/music      : /app/media
/volume1/docker/mtw : /app/data
/volume1/downloads  : /app/download
```

反过来说：如果你把宿主机路径写成 `/volume1/music`，却在容器里期待 `/app/media` 指向别处，那是做不到的——右边不可改。

### 对照表：左右两边谁说了算

| 位置 | 写法示例 | 谁决定 | 能否改 | 改错的后果 |
| --- | --- | --- | --- | --- |
| 宿主机路径（冒号左边） | `/volume1/music` | 你 | 随便改，指向你自己的目录即可 | 指到空目录 → 界面里曲库为空 |
| 容器内路径（冒号右边） | `/app/media` | 项目作者 | **不可改** | 改成别的 → 程序找不到数据，等于没挂 |
| 宿主机端口（`-p` 左边） | `8002` | 你 | 可改，冲突时换一个 | 记错端口 → 浏览器打不开 |
| 容器内端口（`-p` 右边） | `8002` | 项目作者 | **不可改**（V2 为 8002） | 改成 8001 → 连不上服务 |

> [!tip] 大白话
> 把容器想成一套**已经装修好的出租屋**：屋里的三个柜子——`/app/media`（放唱片）、`/app/data`（放钥匙和账本）、`/app/download`（收快递的暂存区）——位置是房东装死的，你不能挪。你能做的是在屋外挑三个真实房间，用一根管子接过去，让屋里那个柜子"通"到你指定的房间。管子接错房间，柜子本身还在，只是永远是空的。

> [!tip] 实践建议：先建目录，再写 compose
> 动手前先在宿主机上把目录准备好：曲库目录（已有就跳过）和配置目录（新建一个）。配置目录建议放在专门留给 Docker 的位置，例如 `/volume1/docker/mtw`，将来整体备份、迁移都只动这一个文件夹。之所以强调"先建"，是因为 Docker 遇到不存在的宿主机路径时通常不会报错——它会替你建一个空目录，于是你得到一个"挂上了、但是空的"曲库，比直接报错更难排查。

> [!note] 核心概念：容器与宿主机的边界
> 容器有自己独立的文件系统，默认**看不见**宿主机上的任何目录。挂载就是在这道边界上凿一个洞：左边是边界外的真实目录，右边是边界内的固定挂载点。所以"容器里能不能看到我的音乐"，完全取决于你有没有挂、挂对没挂对，而不是取决于文件是否存在于你的机器上。

> [!warning] 易错点
> 挂载路径的冒号左右**不能写反**。`-v /app/media:/volume1/music` 这种写法不会报错，但你会得到一个空的曲库，而且极难一眼看出问题。

## 2.2 镜像与 tag 选择

官方快速开始页给出的镜像名是 `xhongc/music_tag_web:latest`，并说明：「latest 为最新版本号，你也可以指定版本，例如：2.1.7, ...」[^c2-d2]。

> [!warning] 不要把 2.1.7 当成当前版本号
> 官方页面里的 `2.1.7` 只是"指定版本"这一写法的举例，页面**没有**声明它是当前版本、也没有声明它是版本要求[^c2-d2]。本笔记不对当前最新版本号做任何断言（该信息 `未取到`）。想知道有哪些 tag，官方给的做法是去 Docker Hub 的 tags 页面查看[^c2-d2]。

拉不动镜像时的国内替代方案，官方给的是一句话替换：

```bash
# 原镜像
xhongc/music_tag_web:latest

# 网络受限时替换为阿里云镜像
registry.cn-hangzhou.aliyuncs.com/xhongc/music_tag_web:latest
```

原页面的说法是：「如果因为**网络问题，无法拉取镜像**，可以使用阿里云的 music tag web 镜像」，并把下文所有 `xhongc/music_tag_web:latest` 替换成上面那个阿里云名称[^c2-d2]。

架构方面，快速开始页写明：「V2 版本支持 arm64、amd64 和 armv7 架构的 Docker 部署」[^c2-d2]。也就是说 x86 服务器、ARM 小主机和部分 ARMv7 设备都在官方支持范围内。

> [!warning] 镜像仓库名有两个版本，以 `xhongc` 为准
> 官方文档里出现过 `xhong/music_tag_web`（少一个 `c`）的写法，与快速开始页的 `xhongc/music_tag_web` 冲突[^c2-d2]。**本笔记统一以 `xhongc/music_tag_web` 为准**。如果你在别处（例如升级相关页面）照抄了 `xhong/music_tag_web`，会直接拉不到镜像——这是官方文档自身的笔误，不是你的操作问题。

> [!tip] 大白话
> `latest` 相当于"自动帮你拿最新那一版"，方便但每次更新都是未知版本；写成具体版本号（如 `:2.1.7`）相当于把商品型号钉死，升级要自己动手，但可复现。官方两句话都给了，但**没有**建议你选哪种[^c2-d2]，所以这是你自己的取舍，不是官方口径。

**本节的已知空白**：`latest` 与固定版本之间官方是否有偏好，`未取到`；当前最新版本号，`未取到`；Docker Hub 上 tag 的完整列表与最后推送时间，本轮收集时 `未取到`（本机访问 Docker Hub 超时）。

## 2.3 Compose 部署（三卷、端口映射、重启策略）

### 官方原始 compose

Docker Compose 部署页给出的完整配置如下（逐字照录）[^c2-d4]：

```yaml
version: '3'

services:
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      - /path/to/your/music:/app/media
      - /path/to/your/config:/app/data
      - /path/to/your/download:/app/download
    restart: always
```

把三处 `/path/to/your/...` 换成你自己的路径即可运行。这就是官方推荐的部署形态：**三个卷**。

### 逐行拆解

- `ports: - "8002:8002"`：冒号左边是宿主机端口，右边是容器内端口。
- `volumes` 三行：分别对应 2.1 讲过的 `/app/media`、`/app/data`、`/app/download`。
- `restart: always`：容器退出后自动拉起（下一段会说明这里我们改用 `unless-stopped`）。

> [!note] 核心概念：端口映射
> 容器是一个隔离的网络环境，容器内部监听 8002，宿主机上的 8002 默认并不会自动转发给它。`-p 8002:8002`（compose 里就是 `ports` 那一行）就是做这件事：**把宿主机的 8002 接到容器的 8002**。和挂载一样，右边（容器内）是项目定死的，左边（宿主机）由你决定。

> [!tip] 大白话
> 端口映射像**公司总机转分机**：外面的人只知道公司总机号（宿主机端口），打进来之后总机帮你转到某个分机上（容器端口）。分机号是内部分配的、不能自己乱改（8002 就是 8002）；总机号对外公示，冲突了可以换一个。所以"我改端口"永远只改左边。

### 三个卷：为什么推荐照单全收

| 卷 | 挂载点 | 装什么 | 不挂会怎样 |
| --- | --- | --- | --- |
| 第一 | `/app/media` | 你的音乐库 | 界面里看不到任何歌曲 |
| 第二 | `/app/data` | 配置与数据库（含 V2 激活信息） | 重建容器后配置、激活状态丢失 |
| 第三 | `/app/download` | 后台刮削的监控目录 | 官方 Compose 页给出的第三个卷，用于「后台刮削监控目录」[^c2-d4] |

第三卷按官方说明是「你新下载音乐的目录，不与媒体库重复和重合，用于后台刮削监控目录」[^c2-d4]。

> [!warning] 关于第三卷的口径，请照官方，不要照本笔记
> 官方 `docker run` 示例只挂了两个卷（不含 `/app/download`），Compose 示例挂了三个，官方**没有说明两者等价或如何取舍**[^c2-d3][^c2-d4]。
> 本笔记的推荐是：**以 Compose 的三卷为准**。至于"不用后台刮削就可以省掉第三卷"，这是**本笔记的推断**，不是官方说法；`/app/download` 是否必需、缺失时后台刮削是否仍可用，本轮收集中 `未取到`。稳妥做法是三个都挂上。

### 重启策略：三种写法，统一用 `unless-stopped`

同一个项目里出现过三种重启写法[^c2-d3][^c2-d4][^c2-d7]：

| 出处 | 写法 | 含义 |
| --- | --- | --- |
| V2 Docker 部署页 | `--restart=unless-stopped` | 崩溃或重启后自动拉起；但**你手动停止过**的容器不会自动再起 |
| V2 Compose 页 | `restart: always` | 无论什么原因退出都自动拉起，包括你手动停掉的 |
| V1 快速开始页 | `--restart=always` | 同 `always` |

**本笔记统一采用 `unless-stopped`**：它既有"挂了自动拉起"的可靠性，又尊重你手动停容器的意图——你想停它做维护时，它不会立刻自己爬起来。

> [!warning] 两个 compose 层面的常见坑
> - **宿主机目录先建好**：路径不存在时 Docker 常会自己造一个空目录，表现为"挂上了但里面什么都没有"。
> - **端口冲突**：宿主机 8002 已被别的服务占用时，`docker compose up -d` 会直接失败。把 `ports` 左边改成别的端口即可，例如 `"18002:8002"`——右边 8002 保持不动，因为那是容器内的固定值。改完记得访问地址也跟着换成新端口。

### 改好的可运行版本

把路径和重启策略换成我们推荐的形式：

```yaml
version: '3'

services:
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"           # 宿主机:容器内；右边 8002 不可改，左边冲突时可换
    volumes:
      - /volume1/music:/app/media           # 曲库，右边不可改
      - /volume1/docker/mtw:/app/data       # 配置与数据库，右边不可改
      - /volume1/downloads:/app/download    # 后台刮削监控目录，不与曲库重合
    restart: unless-stopped
```

保存为 `docker-compose.yml`，在它所在目录执行：

```bash
docker compose up -d      # 后台启动；首次会自动拉镜像
docker compose logs -f    # 观察启动日志，Ctrl+C 退出查看
```

> [!tip] 实践建议
> 这份 compose 是"最小可用"版本。如果你后续想启用容器内一键自动更新等进阶能力，它们对挂载有额外要求。相关做法集中在附录 B，本处不展开——先把最小可用版跑通，再回附录按需加。

## 2.4 `docker run` 对照写法

不想用 compose 也能跑。官方 Docker 部署页给的是一条 `docker run`（原文为一行，下面为提高可读性折行）[^c2-d3]：

```bash
docker run -d \
  -p 8002:8002 \
  -v /path/to/your/music:/app/media \
  -v /path/to/your/config:/app/data \
  --name=music-tag-web \
  --restart=unless-stopped \
  xhongc/music_tag_web:latest
```

官方对参数的说明是：把 `/path/to/your/music` 换成「你的 NAS 上音乐文件夹的绝对路径」，把 `/path/to/your/config` 换成「你新建的一个目录路径，用于存放应用程序的配置文件」[^c2-d3]。绿联部署页给的命令与此一致，只是前面多了 SSH 登录步骤[^c2-n3]。

### 与 Compose 的差异（这是本章必须盯住的一处）

| 对比项 | Compose（2.3） | `docker run`（官方 D3 示例） |
| --- | --- | --- |
| 卷的数量 | **3 个**（含 `/app/download`） | **2 个**（不含 `/app/download`） |
| 重启策略 | `restart: always` | `--restart=unless-stopped` |
| 容器名 | `container_name: music-tag-web` | `--name=music-tag-web` |
| 端口 | `"8002:8002"` | `-p 8002:8002` |

> [!warning] 用 `docker run` 起步的人，最容易漏掉第三个卷
> 官方 `docker run` 示例只有两个 `-v`，而 Compose 示例有三个，官方未说明二者等价或如何取舍[^c2-d3][^c2-d4]。如果你打算使用后台刮削，按 2.3 的说明补上第三个 `-v`：
> `-v /volume1/downloads:/app/download`。

### V1 的写法（供对照，别照抄到 V2）

V1 快速开始页的四步如下[^c2-d7]：

```bash
# 1. 拉镜像
docker pull xhongc/music_tag_web:latest

# 2. docker run 启动（注意端口是 8001）
docker run -d -p 8001:8001 -v /path/to/your/music:/app/media -v /path/to/your/config:/app/data --restart=always xhongc/music_tag_web:latest
```

V1 还给了 Portainer stacks 的等价写法（原文以单行呈现，此处按 YAML 排版）[^c2-d7]：

```yaml
version: '3'
services:
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8001:8001"
    volumes:
      - /path/to/your/music:/app/media:rw
      - /path/to/your/config:/app/data
    command: /start
    restart: always
```

对照可见两处关键差别：V1 端口是 **8001**，且多一行 `command: /start`。快速开始页把这一点写得很直白——V2「容器内的端口是 8002，和不需要 command /start 命令」[^c2-d2]。**如果你复制的是 V1 的片段却期望跑 V2，端口和启动命令都会对不上。**

> [!warning] 注意 `:rw` 后缀
> V1 的 Portainer 示例中 `/app/media` 写了 `:rw` 后缀（读写），而 V2 Compose 示例的三个卷都没写[^c2-d7][^c2-d4]。不写后缀默认就是读写，所以这不是必须项，但看到别人配置里多一个 `:rw` 不必惊讶。

## 2.5 访问地址、默认凭据与后台入口

### 访问地址

V2 安装完成后，官方 Docker 部署页的原文是：「在网页浏览器中输入 `http://127.0.0.1:8002` 或者绿联设备的实际 IP 地址加上端口 8002」[^c2-d3]。

从别的机器访问时，把 `127.0.0.1` 换成部署机器的实际 IP。绿联页给的写法是「输入绿联设备的IP地址后跟端口号8002（例如 `http://greenlink_ip:8002`）」，并把 `greenlink_ip` 换成实际地址[^c2-n3]。

> [!warning] V2 手册提到"绿联设备"疑似串页
> V2 的通用 Docker 部署页里出现了"绿联设备"字样，而该站另有独立的绿联部署页[^c2-d3]。**本笔记推断**这是从绿联页复制过来的残留表述，不影响你按 IP:8002 访问这件事。[推断]

### 默认凭据与后台入口

官方 Docker 部署页写明：「登录后，默认账号密码为 `admin/admin`。」[^c2-d3] 首次登录后应立即修改默认密码。

后台入口 `[/admin]` 的写法：

| 版本 | 官方给出的地址 | 来源 |
| --- | --- | --- |
| V1 | `127.0.0.1:8001/admin` | V1 快速开始页原文「访问在 `127.0.0.1:8001/admin` 默认账号密码 *admin/admin*」[^c2-d7] |
| V2 | 只给了 `http://127.0.0.1:8002`，**未说明是否仍需 `/admin` 后缀** | V2 Docker 部署页[^c2-d3] |

> [!warning] 访问路径写法不一致
> V1 手册明确带 `/admin`，V2 手册只给根地址、未说明后缀[^c2-d3][^c2-d7]。**本笔记的建议写法**是：先访问 `http://<你的IP>:8002`，后台入口为 `/admin`，即 `http://<你的IP>:8002/admin`。请注意 V2 手册**未明确**这一点，实际以界面为准。

### 三个容易踩的细节

1. **反向代理报 csrf 错误**：官方原文「如果你反向代理页面进去报错 csrf 错误，请用局域网地址进入。」[^c2-d3] 也就是说，先用内网地址把初始化做完。
2. **Subsonic 密码**：官方说「如果需要修改 Subsonic 的默认账号密码，也请在登录后进行操作」，并提醒修改后可能需要重新登录、页面没刷出来就刷新[^c2-d3]。凭据位置与客户端清单属播放侧内容，见附录 A。
3. **V2 必须激活**：官方第 6 步是「登录后，点击 V1 标签，按照提示输入 V2 激活码以完成激活。」[^c2-d3] 这一步是 V2 的强制门槛，登录后的完整流程（改密、激活码获取、6 次上限）见第三章。

### 部署完成后的自检清单

按下面五项逐条核对，任何一条不过，都不要急着往下走：

1. **容器在跑**：终端里 `docker ps` 能看到 `music-tag-web`，状态是 Up。
2. **端口能通**：浏览器打开 `http://<你的IP>:8002`，看到登录页而不是"无法访问"。
3. **曲库挂上了**：登录后界面里能看到你的音乐内容，而不是一片空白。空的基本只有一个原因——`/app/media` 那行左边指错了目录。
4. **配置挂上了**：确认 `/app/data` 对应的宿主机目录里已经生成了文件（数据库与配置文件）。这一步是防"重建容器后配置、激活全丢"的关键。
5. **第三个卷在位**：若你打算使用后台刮削，确认 `/app/download` 也挂了，并且它和曲库目录不重合。

后三项都可以用一条命令查实际挂载：

```bash
docker ps                                                      # 容器是否在跑，端口映射对不对
docker inspect music-tag-web --format "{{json .Mounts}}"       # 实际挂了哪几个卷、左边对应哪
```

**本节已知空白**：官方部署页**没有出现任何环境变量清单**（如 PUID/PGID/TZ 之类），fnOS 页全部截图里也没有环境变量输入区与网络模式字段[^c2-d3][^c2-o1]——本节因此不列任何环境变量示例（`未取到`）。

## 2.6 NAS 差异小节

通用的 Compose 写法在所有支持 Docker 的 NAS 上都成立，差别只在"从哪里点进去"。本节以飞牛 fnOS 为主——它的官方部署页整页几乎没有文字，步骤全部承载在 11 张截图里。

### 飞牛 fnOS（以截图为准）

fnOS 部署页正文只有一句版本标注与几行文字：`fnos版本：0.8.24`、`进入docker界面搜索 xhongc/music_tag_web 点击下载`、`选择对应版本：latest`、`等待下载完成`，然后写明「两种方式可以部署，二选一」，即「第一种：容器部署」与「第二种：Compose部署」[^c2-n4]。

> [!warning] 该页的版本号含义未确认
> `fnos版本：0.8.24` 是页面原文，但页面**没有说明**这个数字指 fnOS 系统版本还是别的什么。**本笔记推断**它是作者测试时所用的 fnOS 系统版本[^c2-n4]。[推断]

**路线一：容器部署（界面表单）**[^c2-o1]

1. 左侧进 **Docker 应用**（不是应用商店，该页全程没有出现应用商店），在「镜像仓库」页搜索 `xhongc/music_tag_web`。搜索结果有 3 条，官方那条是第一条 `xhongc/music_tag_web`（下载量 `100K+`、收藏 `35`、带描述行 `Music Tag 音乐标签web版`），另外两条是同名个人镜像（`w497273/...`、`0x152a/...`）。页面没有文字提示该选哪条。[截图读取]
2. 点下载后弹「选择标签」，字段 `镜像标签` 填 `latest`。[截图读取]
3. 下载完成后进「创建容器」第 1 步：`选择镜像*` = `xhongc/music_tag_web:latest`，`容器名称*` = `music_tag_web`（**下划线**）；「资源限制」不勾，「开机自动开启」不勾。[截图读取]
4. 第 2 步「高级设置」：`端口设置` 一行填 本地端口 `8002` → 容器端口 `8002`，协议 `TCP`；`存储位置` 填两条 —— 本地 `/vol1/1000/music` → 装载 `/app/media`（读写），本地 `/vol1/1000/mtw_config` → 装载 `/app/data`（读写）。[截图读取]
5. 第 3 步「确认信息」：核对后勾选「创建后启动容器」，点「创建」。[截图读取]

**路线二：Compose 部署**[^c2-o1]

1. 左侧 `Compose` → 项目管理 → `+ 新增项目`。
2. 「创建项目」弹窗里选来源 `创建docker-compose.yml`，路径填 `vol1/1000/mtw_config`，勾「创建项目后立即启动」。
3. 内嵌编辑器里粘贴下面这段 YAML（**逐字照录自截图，此 YAML 不在页面正文里**）[^c2-o1]：

```yaml
version: '3'

services:
  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      - /vol1/1000/music:/app/media:rw
      - /vol1/1000/mtw_config:/app/data
    restart: unless-stopped
```

部署完成后，页面正文的说明是「成功部署访问8002端口，默认账号密码 都为 admin，左上角V1标签点击激活V2版本」[^c2-n4]。

> [!warning] fnOS 截图自身有缺陷，照容器路线走必须自查
> **「高级设置」里配了 2 条卷映射（`/app/media` 与 `/app/data`），但紧接着的「确认信息」汇总页只剩 1 条**——`/app/data` 那一行不见了。这是截图本身的差异，不是阅读误差；对比之下 Compose 路线的 YAML 明确带 2 条卷。[截图读取][^c2-o1]
> 后果是实打实的：V2 的配置与数据库落在 `/app/data`，**这个卷没挂上，重建容器就等于丢配置、丢激活**。所以照容器路线走完第 3 步「确认信息」时，请务必回头确认 `/app/data` 那一条真的在列表里；不在就点「上一步」重加。
> 另外两条路线生成的容器名不同：容器部署是 `music_tag_web`（下划线），Compose 部署是 `music-tag-web`（连字符）[^c2-o1]。后续写命令（例如检查日志）时不要混用。
> 还有一处小的不一致：Compose 的「路径」字段截图里填的是 `vol1/1000/mtw_config`（无前导斜杠），而同一页 YAML 卷里写的是 `/vol1/1000/mtw_config`（有前导斜杠）[^c2-o1]。按 YAML 里的带斜杠写法即可。

> [!tip] 大白话
> 这一步就像**在租房 App 里下单，最后一步的确认清单比前面的勾选项少了一行**。你前面明明勾了"配置柜"，确认页却没列出来——如果不回头核对，你以为都装好了，实际搬进去才发现没有衣柜。fnOS 这份官方截图就处于这个状态。

### 其他 NAS：一张简表

| 平台 | 入口方式 | 关键值 | 来源 |
| --- | --- | --- | --- |
| 群晖 | 容器管理器「注册表」搜索 `music_tag_web`，第一个即本项目镜像 | 容器内端口 8002（第二个值），容器外随意；音乐映射到 `/app/media`、新建目录映射到 `/app/data`，官方两次强调「此路径不可更改」 | N1[^c2-n1] |
| 1Panel | 方式一「应用商店安装（推荐）」；方式二「镜像安装」 | 方式一默认挂载 `./data:/app/media:rw` 与 `./config:/app/data`，自定义媒体库改 compose；方式二镜像 `xhongc/music_tag_web:latest`，容器端口**必须 8002 不能改变**，协议选 TCP | N2[^c2-n2] |
| 绿联 | 终端 SSH 登录 → `sudo -i` → 跑 `docker run` | `-p 8002:8002`，访问 `http://<绿联IP>:8002` | N3[^c2-n3] |
| 极空间 | 拉镜像 → 双击镜像 → 建 Docker 目录 → 加目录映射 → 加端口 | 目录映射 `/app/media`、`/app/data`；端口可选 host（默认约 8002）或自定义 bridge | N5（该页自述转载第三方，按**社区实践**看待）[^c2-n5] |

> [!warning] 极空间页属转载，不与官方步骤混用
> 极空间部署页首行自述作者没有极空间 NAS，教程来自第三方网站 `https://izspace.cn/music/musictag.html`[^c2-n5]。所以上表中极空间那一行的步骤，请当作**社区经验**，不是官方自述步骤。

> [!warning] 威联通：官方手册未见专页
> 本笔记的素材中没有找到任何威联通（QNAP）的官方部署页面。**不得据此推断威联通无法部署或要特殊处理**——这里只如实记录一个空白：官方手册未见威联通专页。威联通用户可参照 2.3 的通用 Compose 思路，在 Container Station 里自行配置。此为**本笔记的推断性建议**，非官方口径。

> [!warning] 激活步骤在各 NAS 页覆盖不一致——这是页面缺失，不是"无需激活"
> 1Panel 页写明「在登录后 点击V1 标签，输入 V2 激活 即可完成激活。」[^c2-n2]；fnOS 页写明「左上角V1标签点击激活V2版本」[^c2-n4]。但群晖页与绿联页**完全没有提到激活步骤**，极空间页也没有[^c2-n1][^c2-n3][^c2-n5]。**本笔记不能据此推断这些平台无需激活**——V2 的激活是登录后处处都要过的门槛（见第三章），这几页只是没写。

**本节的已知空白**：各 NAS 页**均未给出平台系统版本号**（群晖 DSM、1Panel 面板、绿联 UGOS、极空间均无），也均未给出 Music Tag Web 自身的版本号；所有截图里都没有环境变量输入区，也没有网络模式（bridge/host）选择项[^c2-n1][^c2-n2][^c2-n3][^c2-n5][^c2-o1]。这些是文档空白，本笔记不做补齐。

> [!summary] 本章小结
> - **三条挂载，右边不可改**：`/app/media`（曲库）、`/app/data`（配置与数据库）、`/app/download`（后台刮削监控目录）。左边宿主机路径由你决定。
> - **推荐 Compose 三卷配置**；官方 `docker run` 示例只挂两卷、少了 `/app/download`，"不用后台刮削可省"是**本笔记推断**，不是官方说法。
> - **重启策略统一用 `unless-stopped`**：官方三种写法并存，它兼顾自动拉起与"手动停就别再自己爬起"。
> - **端口只改左边**：V2 容器内固定 8002，V1 是 8001 且多一行 `command: /start`。
> - **镜像认准 `xhongc/music_tag_web`**；写成 `xhong/music_tag_web`（少个 c）拉不到镜像。
> - **访问 `http://<IP>:8002`，后台入口为 `/admin`**（V2 手册未明确 `/admin` 后缀）；默认凭据 `admin/admin`，登录后立即改密。
> - **NAS 上以飞牛 fnOS 为主**；其容器路线截图有卷映射缺陷，务必自查 `/app/data` 是否真的挂上。威联通无官方专页。

下一章我们接着登录之后的动作往下走：改掉默认密码、拿到并填入 V2 激活码，以及为什么这串激活码有 6 次上限、跨设备激活会顶掉前一台——做好这几件事，V2 才算真正可用。

## 参考来源

[^c2-d2]: V2 快速开始（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi.md

[^c2-d3]: V2 Docker 部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-bu-shu.md

[^c2-d4]: V2 Docker Compose 部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/docker-compose-bu-shu.md

[^c2-d5]: V2 名词解释（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/ming-ci-jie-shi.md

[^c2-d7]: V1 快速开始（官方文档）— https://xiers-organization.gitbook.io/music-tag-web/kuai-su-kai-shi.md

[^c2-n1]: 群晖部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/qun-hui-bu-shu.md

[^c2-n2]: 1panel 部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/1panel-bu-shu.md

[^c2-n3]: 绿联部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/l-lian-bu-shu.md

[^c2-n4]: 飞牛云 fnOS 部署（官方文档，正文文字部分）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md

[^c2-n5]: 极空间部署（官方文档页面，正文自述教程转载自第三方网站，按社区实践看待）— https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/ji-kong-jian-bu-shu.md

[^c2-o1]: 飞牛云 fnOS 部署 11 张截图（`fnos-01` … `fnos-11`，逐张读取，正文中标注 `[截图读取]`）— 同一页面 https://xiers-organization.gitbook.io/music-tag-web-v2/kuai-su-kai-shi/fei-niu-yun-fnos-bu-shu.md
