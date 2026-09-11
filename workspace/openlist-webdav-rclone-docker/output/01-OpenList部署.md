# 第 1 章 用 Docker 跑起 OpenList

> 🧭 分册导航 ｜ 目录：[[README]] ｜ 下一册：[[02-网盘聚合]]

这一章只解决一件事：在你的 Linux 宿主机上跑出一个能登录、重启后配置与账号都还在的 OpenList 实例。后面的 WebDAV、rclone 挂载、映射给 Docker 容器，全部建立在这个实例之上——这一步没跑稳，后面每一层都是在流沙上盖楼。

> [!warning] 执行环境先对齐
> 本章命令一律以 **Linux 宿主机 + Docker** 为准。你本机是 Windows + Git Bash，`$(id -u)`、`chown`、`/etc/openlist` 这类写法在 Git Bash 下语义不同甚至不存在，请把命令放到 **远程 Linux 宿主机 / NAS / WSL** 里执行。官方文档亦以 Linux 命令行为例。

本章唯一主干来源是 OpenList 官方文档的 Docker 安装页 [OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)，下文凡加引号的文本均已回源逐字核对。

---

## 1.1 选镜像标签：先分清「稳定/开发」和「预装环境」

镜像名固定是 `openlistteam/openlist`，加不同的标签（tag）得到不同用途的镜像。官方给出两类维度：

**第一维：稳定版 / 开发版**

| 标签 | 含义 | 官方说明要点 |
|---|---|---|
| `latest` | 稳定版 | 等价于最新稳定发布 |
| `v*.*.*` | 稳定版（指定版本号） | 最新 tag 见 Docker Hub 的 tags 页 |
| `beta` | 开发版 | 官方原话：`Dev version` |

**第二维：预装环境后缀**（在任意标签后用 `-` 追加）

| 后缀 | 说明（官方原文） |
|---|---|
| `aio` | 「同时包含下列所有预装环境的镜像」 |
| `ffmpeg` | 「预装 ffmpeg 的镜像，用于本地存储缩略图」 |
| `aria2` | 「预装 aria2 的镜像，用于离线下载」 |

官方给的三个拼接示例是 `openlistteam/openlist:latest-aio`、`openlistteam/openlist:latest-aria2`、`openlistteam/openlist:latest-ffmpeg`。

> [!note] `lite` 不属于上面那张后缀表
> 官方在「稳定版」条目下另提了精简版镜像 `openlistteam/openlist:latest-lite`，理由是「部分容器运行平台不支持大于 100M 的镜像」。它不是「预装环境后缀」，而是**去掉内容的精简镜像**，使用场景是 PaaS 平台报出这个错误时：
> `Pod ephemeral local storage usage exceeds the total limit of containers 100Mi.`

**怎么选（本章建议）**：第一次打通链路只用 `openlistteam/openlist:latest`。缩略图和离线下载都不是这一章的目标，等第 2 章真要用本地存储缩略图时再回来换成 `latest-ffmpeg`。`beta` 不要用在你的正式实例上。

> [!tip] 大白话
> 把镜像标签想成点外卖：`latest` 是标准套餐，`v*.*.*` 是指定某一天的固定菜单，`beta` 是厨师试做的新菜；`-ffmpeg`、`-aria2`、`-aio` 是「加购配菜」——分别给你多带一个转码器、一个下载器，或者两样都带。你这一章只需要标准套餐。

---

## 1.2 端口与数据目录：唯一必须显式映射的东西

官方所有示例都包含这两个映射，它们的含义是：

| 参数 | 含义 |
|---|---|
| `-p 5244:5244` | 把容器内 5244 端口映射到宿主机 5244，网页端与后续 WebDAV 都走这个端口 |
| `-v /etc/openlist:/opt/openlist/data` | 把宿主机 `/etc/openlist` 挂到容器内数据目录 `/opt/openlist/data` |

关于宿主机路径，官方专门给了一条提醒：

> 「请注意：`/etc/openlist` 仅为默认映射的目录，您可以根据需要修改为其他目录。」——[OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)

也就是说 `/etc/openlist` 不是规定动作，你完全可以换成 `/opt/openlist`、`/srv/openlist` 或 NAS 上的某个共享目录。真正**不能改**的是冒号后面的容器内路径 `/opt/openlist/data`。

> [!note] 为什么数据目录必须映射
> OpenList 的用户、密码、配置、已添加的存储，全都写在容器内 `/opt/openlist/data` 下。容器本身是「一次性的壳」：`docker rm` 掉再重新 `docker run` 一个，壳是全新的。只有把这个目录映射到宿主机，重建容器时数据才跟着宿主机目录留下。官方在「Docker CLI」更新步骤的注释里写得很直白：「删除 OpenList 容器（只要不手动删除数据，数据仍然保留）」——反过来说，**没映射数据目录，删容器就等于删数据**。

> [!tip] 大白话
> 把容器当成酒店房间，`/opt/openlist/data` 是房间里的保险箱。不映射，退房时保险箱连钥匙一起被清空；映射到宿主机，等于把保险箱搬到你自己家里——房间换了，箱子还在。

---

## 1.3 本章核心：运行身份的分岔（v4.1.0 边界）

这是本章唯一容易踩坑、也是唯一必须精确记住版本边界的地方。

### 边界原话

官方警告原文（中文版）是：

> 「在 `v4.1.0` 以后的版本中（**不包含 `v4.1.0`**），OpenList 镜像已经移除了 `PUID`、`PGID`，并借鉴于 MariaDB 的构建方式，使用 `useradd` 增加了用户 `openlist`（UID 1001）和组 `openlist`（GID 1001），并使用该用户运行 `openlist server`。」——[OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)

请注意括号里的限定：**新行为适用于「`v4.1.0` 之后」，且明确把 `v4.1.0` 自己排除在外**。官方在安装页把示例拆成两节——「v4.1.0 以后版本」和「v4.1.0 及以前版本」——`v4.1.0` 本身归入**旧写法**那一节，仍用 `PUID`/`PGID`。所以版本边界要记成：

| 镜像版本 | 身份机制 |
|---|---|
| **`v4.1.0` 之后**（不含 `v4.1.0`） | 已移除 `PUID`/`PGID`；镜像内建 `openlist` 用户（UID 1001）/ 组（GID 1001），并以该用户运行 `openlist server`；改用 `user:` / `--user` 指定身份 |
| **`v4.1.0` 及以前** | 使用环境变量 `-e PUID=... -e PGID=...` |

### 为什么这是个「必须由你处理」的问题

镜像换成了固定的 UID 1001，于是容器进程能否读写你映射进去的宿主机目录，就不再是自动成立的。官方紧接着写了这句：

> 「这意味着，您需要手动处理映射的目录的权限问题，确保容器内的 `openlist(1001)` 用户有权限访问映射的目录。」——[OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)

### 三种合法的运行身份写法

官方对「`v4.1.0` 之后」给了两条路线，加上「`v4.1.0` 及以前」的一条，共三种写法。以下 `docker run` 命令在 S01 中抓取完整，可逐字使用。

**写法 A：以「当前用户」运行**（官方 TIP：「如果您希望使用当前用户运行和管理 OpenList 及其配置目录，请使用以下命令」）

```bash
mkdir -p /etc/openlist
docker run --user $(id -u):$(id -g) -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e UMASK=022 --name="openlist" openlistteam/openlist:latest
```

`--user $(id -u):$(id -g)` 把容器进程的身份设成你当前登录用户的 UID/GID，于是宿主机上这个目录本来就归你，权限自然对得上。

**写法 B：以容器内置的 1001 用户运行**（官方 TIP：「如果您希望使用 1001，即容器内置的默认 `openlist` 用户运行和管理 OpenList 及其配置目录」）

```bash
sudo chown -R 1001:1001 /etc/openlist
docker run -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e UMASK=022 --name="openlist" openlistteam/openlist:latest
```

这条路线的关键是**先** `chown -R 1001:1001` 把宿主机目录的属主改成 1001，再启动容器，让内置用户 1001 能读写它。

**写法 C：`v4.1.0` 及以前**——用 `PUID`/`PGID`

```bash
docker run -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e PUID=0 -e PGID=0 -e UMASK=022 --name="openlist" openlistteam/openlist:latest
```

把三条放在一起对比，你要做的判断就一句话：

| | 写法 A | 写法 B | 写法 C |
|---|---|---|---|
| 适用版本 | v4.1.0 之后 | v4.1.0 之后 | v4.1.0 及以前 |
| 身份来源 | 宿主机当前用户（`$(id -u):$(id -g)`） | 镜像内建 `openlist(1001)` | 环境变量 `PUID`/`PGID` |
| 需先做的一步 | 无 | `sudo chown -R 1001:1001 <宿主机目录>` | 无 |
| 官方示例中的取值 | `--user $(id -u):$(id -g)` | 不传 `--user`（默认即 1001） | `-e PUID=0 -e PGID=0` |

> [!warning] 待核实（Q3）：rootful Docker 下 `--user 0:0` 的确切含义
> Compose 写法里官方给的是 `user: '0:0'`，并附英文注释：`Please replace \`0:0\` with the actual user ID and group ID you want to use to run OpenList.`
> 官方文档**只在 rootless 语境下**解释过这个写法：「**rootless** 模式中的 Docker，`--user 0:0` 代表当前用户的 UID 和 GID。」
> 那么 **rootful（普通 root 权限的 Docker Engine）下 `--user 0:0` 到底代表什么**——是字面上的 `uid=0, gid=0`（即 root），还是与镜像内建 `openlist(1001)` 之间有某种优先级关系——**官方文档没有说明**。这条线索在本笔记中标记为 **待核实/未证实**，本章不给结论。实操建议：用写法 A 或写法 B 的显式 UID/GID，避开这个歧义。

> [!tip] 大白话
> 把「运行身份」想成进大楼刷的工牌。`v4.1.0` 之后，大楼换了门禁系统：不再让你在门口用 `PUID=0` 之类的纸条声明身份，而是楼里**固定预置了一张工牌**，编号 1001，名叫 `openlist`。这个进程刷卡进你的文件柜——如果文件柜（宿主机映射目录）的锁只认别人，它就打不开，所以官方要你「自己处理权限」。三种写法就是三条路：借你自己的工牌（A）、把柜锁改成配 1001（B）、或者干脆回到旧门禁系统用纸条声明（C）。至于 rootful 下那张写着 `0:0` 的万能卡到底管不管用，官方没说，我们也不知道——这就是上面那个「待核实」。

---

## 1.4 环境变量：先认识这几个

官方环境变量表（中文版）如下，前两个已在上一节讲过：

| 名称 | 默认值 | 说明 |
|---|---|---|
| `PUID` | （表中未给） | 「运行身份 UID，在 v4.1.0 以后的版本中废弃」 |
| `PGID` | （表中未给） | 「运行身份 GID，在 v4.1.0 以后的版本中废弃」 |
| `UMASK` | `022` | 见官方引用的 umask 说明链接 |
| `UTC` | 默认为 UTC 时区 | 「如果你想指定时区，则可以设置此变量，例如：`Asia/Shanghai`」 |
| `RUN_ARIA2` | 视镜像而定 | 「是否同时运行 ARIA2，当镜像含有 aria2 环境时默认为 `true`，否则为 `false`」 |
| `OPENLIST_ADMIN_PASSWORD` | （表中未给） | 「通过环境变量指定管理员密码」 |

两个实践要点：

1. **`UMASK=022` 建议保留**。官方所有示例都带着它，含义是新建文件的默认权限掩码，改成别的值会影响容器写出的文件在宿主机上的可读性。
2. **想要正点的时间戳就设 `UTC`**。默认是 UTC 时区，想让日志和文件时间是你本地时间，加 `-e UTC=Asia/Shanghai`（官方的增强版 Compose 示例里则用 `TZ=${OPLISTDX_TZ}` 表达同一件事）。

**关于环境变量前缀**，官方写了一条容易忽略的约定：

> 「Docker 镜像中的 OpenList 默认使用 `--no-prefix` 参数运行，因此您无需添加 `OPENLIST_` 前缀。」——[OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)

意思是：OpenList 支持用环境变量传配置，通常这类变量要带 `OPENLIST_` 前缀，但因为镜像默认加了 `--no-prefix`，你直接写变量名即可，不要自作聪明加前缀。官方并给了可查询全部变量名的 Go Packages 链接（`pkg.go.dev` 上的 `internal/conf#Config`）。

> [!tip] 大白话
> `--no-prefix` 相当于门牌号简化：本来快递要写「XX 小区 3 栋 502」，现在物业说「本小区就一栋楼，你直接写 502 就行」。所以变量写 `UMASK` 而不是 `OPENLIST_UMASK`——多写前缀反而找不到地址。

---

## 1.5 首次启动与拿到管理员密码

官方没有在安装命令后直接给出密码，而是让你去**看容器日志**：

```bash
docker logs openlist
```

> 「你将在日志中看到密码。」——[OpenList Docs — 使用 Docker 安装](https://doc.oplist.org/guide/installation/docker)

日志里会有一行形如：

```text
Successfully created the admin user and the initial password is: xYZabHGf
```

这里的 `xYZabHGf` 是官方文档里的示例占位值，**你的实例会生成自己的随机串**，别照抄。官方在「首次运行」小节给出的就是上面这行输出格式。

**密码**即日志里那一串。**用户名**方面，官方这一页未逐字写明登录用户名，只把日志里的这一行称为 `admin user`；实操中按 `admin` 登录（若你的界面提示用户名错误，回到 `docker logs openlist` 核对首启那一行）。拿到后立刻打开浏览器访问 `http://<宿主机IP>:5244` 登录。

**忘记密码或想重设**（官方「非首次运行」小节，两条命令逐字如下）：

```bash
# 重新随机生成密码
docker exec -it openlist ./openlist admin random

# 手动设置密码为 `NEW_PASSWORD`（替换为您要设置的密码）
docker exec -it openlist ./openlist admin set NEW_PASSWORD
```

`docker exec -it openlist ./openlist admin random` 会重新生成一个随机密码并打印出来；`... admin set NEW_PASSWORD` 则把密码改成你指定的值。注意第二条里的 `NEW_PASSWORD` 是占位符，你要替换成真实密码。

> [!tip] 大白话
> 初始密码就像快递箱的取件码——**只出现在开箱那一次的短信里**（首次启动的日志）。之后再想换码，就用 `admin random` 让系统重新摇一个，或用 `admin set` 自己定一个。

---

## 1.6 用 Compose 启动（附：YAML 还原说明）

CLI 命令适合一次性验证；长期运行建议用 Compose。官方 Compose 段分「v4.1.0 以后」和「v4.1.0 及以前」两版，其中「以后」这版带有 `user:` 字段：

> [!warning] 这段 YAML 是**按官方页面结构还原**的
> S01 抓取时，该页 Compose 代码块的 YAML 列表项引导符 `- ` 被剥离、`volumes`/`ports` 行丢失缩进（形如 `'./data:/opt/openlist/data'` 顶格）。**不能逐字照抄抓取结果**。下面的缩进与 `- ` 是按官方页面结构还原的；`image`、`container_name`、`user`、`volumes`、`ports`、`environment`、`restart` 的键名与取值均来自 S01 原文，仅列表符号为还原。
> 另：本段 `./data` 是 Compose 的相对路径，官方在同一个页面里让读者先 `mkdir -p /opt/openlist` 并 `cd /opt/openlist` 再创建 `docker-compose.yml`，因此该路径落在 `/opt/openlist/data`。这与 §1.3 的 `docker run` 示例用 `/etc/openlist` 只是**两个不同示例的宿主机路径选择**，不要混用。

```yaml
# docker-compose.yml — 按官方页面结构还原（列表符号为还原，键名取值来自 S01）
services:
  openlist:
    image: 'openlistteam/openlist:latest'
    container_name: openlist
    user: '0:0' # Please replace `0:0` with the actual user ID and group ID you want to use to run OpenList.
    volumes:
      - './data:/opt/openlist/data'
    ports:
      - '5244:5244'
    environment:
      - UMASK=022
    restart: unless-stopped
```

`v4.1.0` 及以前那版则**没有** `user:` 行，改为在 `environment` 下写 `PUID=0` / `PGID=0`。

启动命令（官方原文，在 `docker-compose.yml` 相同目录下执行）：

```bash
docker compose pull
docker compose up -d
```

> [!warning] `user: '0:0'` 请回头看 Q3
> 这个值就是 §1.3 标为**待核实**的那个 `0:0`。官方注释让你「替换成你实际要使用的用户 ID 和组 ID」。在官方把 rootful 语义讲清楚之前，更稳的做法是把它换成显式的 `<你的UID>:<你的GID>`，或直接采用写法 B（不写 `user:`，改用 `chown -R 1001:1001 ./data`）。

如果你想要官方「增强版 Compose」（那条把 openlist 与 aria2-pro、ariang、qbittorrent、transmission 一起定义的版本），本章不展开：官方默认把下载器那几段**整段注释掉**，属于进阶用法。跑通主线只需上面这一份。

---

## 1.7 升级：三种官方姿势

官方给了三条升级路径，前两条不依赖 Compose：

**方式一：Watchtower 一键更新**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower openlist --cleanup --run-once
```

官方提醒：「如果您的容器名不是 `openlist`，请替换为实际的名称。」

**方式二：Docker CLI 四步**

```bash
# 查看容器（查找 OpenList 容器的 ID）
docker ps -a

# 停止运行中的 OpenList 容器实例，否则无法删除（此时 OpenList 容器的 ID 为 d429749a6e69，每次安装时不同）
docker stop ID

# 删除 OpenList 容器（只要不手动删除数据，数据仍然保留）
docker rm ID

# 拉取 OpenList 的最新镜像
docker pull openlistteam/openlist:latest
```

四步之后需要**按 §1.3 的写法重新 `docker run`** 一次——`docker rm` 已经把容器删掉了。这里的 `ID` 和示例值 `d429749a6e69` 都是占位/示例，你要换成 `docker ps -a` 里查到的真实容器 ID。

**方式三：Compose 三连**

```bash
docker compose pull
docker compose down
docker compose up -d
```

> [!warning] 跨 v4.1.0 升级时要顺手改身份写法
> 如果你从 `v4.1.0` 及以前的镜像升级到 `v4.1.0` 之后，旧命令里的 `-e PUID=0 -e PGID=0` 在新镜像上已**废弃/失效**（官方环境变量表原文：`PUID`/`PGID`「在 v4.1.0 以后的版本中废弃」）。升级时要么补上 `--user`，要么先 `chown -R 1001:1001` 数据目录。官方「更新」章节也为此单独拆了「升级到 v4.1.0 以后版本（不包括 v4.1.0）」和「升级到 v4.1.0 以前的版本（包括 v4.1.0）」两套命令。

> [!tip] 大白话
> 三种升级方式分别是：让保洁阿姨替你换房（Watchtower 一条命令搞定）、自己退房再开一间（CLI 四步，关键是保险箱别退）、或者用管理式公寓的统一流程换房（Compose 三连）。共同点只有一个：**先确认数据目录还挂在宿主机上**，否则换房等于丢行李。

---

## 1.8 章末可跑产出（自检清单）

跑完本章，你应该能通过下面全部检查项：

- [ ] `docker ps` 能看到名为 `openlist` 的容器处于 `Up` 状态。
- [ ] 浏览器打开 `http://<宿主机IP>:5244`，页面正常加载。
- [ ] 用用户名 `admin` + 首次启动日志里的初始密码（或 `admin set` 后设定的密码）**能成功登录**。
- [ ] **重启验证持久化**：执行 `docker restart openlist`，等容器重新 `Up` 后刷新浏览器——账号仍然有效、登录状态与配置仍在。
- [ ] **重建验证持久化（更有说服力）**：`docker stop openlist && docker rm openlist`，再用**完全相同**的 `-v`/`volumes` 映射重新创建容器；登录信息与配置依旧存在。如果这一步数据丢了，说明第 1.2 节的 `-v <宿主机目录>:/opt/openlist/data` 没写对。
- [ ] 宿主机上的映射目录（如 `/etc/openlist` 或 `./data`）里能看到 OpenList 写出的文件。

---

## 本章小结

- 镜像名固定 `openlistteam/openlist`；标签分「稳定（`latest` / `v*.*.*`）/ 开发（`beta`）」，`-aio` / `-ffmpeg` / `-aria2` 是预装环境后缀，`-lite` 是另一回事的精简镜像。
- 必须显式映射的是 `-p 5244:5244` 与容器内 `/opt/openlist/data`；宿主机侧的 `/etc/openlist` 只是官方**默认**目录，可随意改。
- 本章核心是版本边界：**`v4.1.0` 之后（不含 `v4.1.0`）** 已移除 `PUID`/`PGID`，改用内建 `openlist(1001)`，要求你自行处理映射目录权限；`v4.1.0` 本身仍属旧写法。三种身份写法：`--user $(id -u):$(id -g)` / `chown -R 1001:1001` + 内置用户 / `-e PUID=0 -e PGID=0`。
- rootful Docker 下 `--user 0:0` 的确切含义官方未说明，**待核实**，实操请用显式 UID/GID。
- 首次密码看 `docker logs openlist`；重设用 `docker exec -it openlist ./openlist admin random|set`。升级有 Watchtower / CLI 四步 / Compose 三连三条官方路径，跨 v4.1.0 升级要同步改运行身份写法。

## 下一章预告

实例跑起来了，但里面还是空的。下一章我们开始「把网盘聚合进来」：认识 OpenList 的存储模型，把第一个存储挂上去——重点讲清 `Mount Path` 这个字段的三重含义、官方两条硬校验（留空、重名）以及各自的报错原文。

---

> 🧭 分册导航 ｜ 目录：[[README]] ｜ 下一册：[[02-网盘聚合]]
