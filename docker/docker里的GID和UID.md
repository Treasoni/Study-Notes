---
title: Docker 里的 UID / GID
tags:
  - docker
  - 权限
  - UID
  - GID
created: 2026-07-28
updated: 2026-09-14
status: 已完成
source_project: study-notes
---

> [!info] 相关文档
> - [[Docker MOC]] - Docker 知识索引
> - [[Docker容器服务访问宿主机文件]] - 深挖：挂载选型、权限对齐与安全边界完整实战
> - [[OpenList网盘挂载-05-Docker映射]] - 「容器以什么身份访问挂载文件」的完整实例
> - [[docker容器搭建错误的知识讲解]] - 配置修改后的行为
> - [[docker容器如何更新]] - 容器更新指南

# Docker 里的 UID / GID

> [!summary] 本笔记解决什么问题
> 容器跑起来了，但它生成的文件宿主机删不掉、改不动，日志里一堆 `Permission denied`。根因只有一个：**容器进程的 UID 和宿主目录的属主对不上**。本笔记按「是什么 → 为什么出错 → 三种解法 → 怎么验证 → 常见坑」的顺序把这件事讲透，读完能独立修好绝大多数容器权限问题。
>
> 想继续深挖挂载选型、安全边界（只读卷、SELinux、docker.sock），看 [[Docker容器服务访问宿主机文件]]。

## 目录

1. [[#第 1 章：UID / GID 是什么|第 1 章：UID / GID 是什么]]
2. [[#第 2 章：为什么会 Permission denied|第 2 章：为什么会 Permission denied]]
3. [[#第 3 章：三种解法|第 3 章：三种解法]]
4. [[#第 4 章：验证与排查三步|第 4 章：验证与排查三步]]
5. [[#第 5 章：常见坑|第 5 章：常见坑]]
6. [[#第 6 章：实战场景：媒体 / 下载类容器|第 6 章：实战场景：媒体 / 下载类容器]]

---

## 第 1 章：UID / GID 是什么

先纠正一个常见混淆：容器里跟**权限**有关的是 UID / GID，**不是 PID**。

| 缩写      | 全称         | 中文     | 跟权限的关系               |
| ------- | ---------- | ------ | -------------------- |
| **UID** | User ID    | 用户 ID  | 决定「这个进程算谁」           |
| **GID** | Group ID   | 用户组 ID | 决定「这个进程属于哪个组」        |
| PID     | Process ID | 进程 ID  | 无关，只是运行中进程的编号，每次重启都变 |

关键背景：**Linux 文件系统里存的不是用户名，是数字。**

`/etc/passwd` 里的 `zhq` 只是给数字 `1000` 贴的一个标签。文件属性上真正记录的是 `1000:1000`，用户名只是 `ls -l` 帮你翻译出来的展示层。所以「名字对不对」不重要，**数字对不对才重要**——这也是后面一切权限问题的总根源。

### 怎么查自己的 UID / GID

```bash
id                # 一次看全：uid / gid / 所属组
id -u             # 只输出 UID 数字，如 1000
id -g             # 只输出 GID 数字，如 1000
id zhq            # 看指定用户（把 zhq 换成你的用户名）
```

输出示例：

```text
uid=1000(zhq) gid=1000(zhq) groups=1000(zhq),27(sudo),100(users)
```

这三行数字就是后面配置 `PUID` / `PGID` / `user:` 时要填的值。

> [!tip] 大白话
> 把 UID 想成**数字工号**。宿主机这个「文件柜管理员」只认工号，不认工牌上的名字。改名没用，得让工号对上。

---

## 第 2 章：为什么会 Permission denied

### 根因：Docker 不做 UID 映射

这是最反直觉的一点：

> **容器里的 UID 1000，就是宿主机的 UID 1000。Docker 不会帮你把容器里的用户「翻译」成宿主机的某个用户。**

不是「容器内 root 自动等于宿主机管理员」，而是**同一个数字在两边通用**。容器进程拿着工号 33，宿主机目录的锁上写的是工号 1000，门就是打不开——哪怕容器里那个用户叫 `www-data`。

而多数容器**默认以 root（UID = 0）运行**（除非 Dockerfile 里写了 `USER`）。于是：

```bash
docker run -v /data/downloads:/downloads some-image
```

容器里是 root 在写文件，宿主机上看到的就是：

```text
-rw-r--r-- 1 root root 1234567 Sep 14 00:00 xxx.mkv
```

然后你用自己的账号删：

```bash
rm xxx.mkv
# rm: cannot remove 'xxx.mkv': Permission denied
```

### 为什么「能读不能删」

`-rw-r--r--` 就是权限 `644`，拆开看：

| 段 | 值 | 含义 |
| --- | --- | --- |
| `-` | — | 普通文件（`d` 才是目录） |
| `rw-` | 6 | **属主 root**：可读可写 |
| `r--` | 4 | **属组 root**：只读 |
| `r--` | 4 | **其他人**：只读 |

你既不是 root 也不在 root 组，落在「其他人」这一档——所以**能读，不能改**。

至于**删不掉**，还有一层：删除文件要求你对该文件**所在目录**有写权限（`w`）。目录属主是 root、权限通常是 `755`，你同样落在「其他人 = `r-x`」，没有 `w`，所以删不了。

> [!tip] 大白话
> 文件柜管理员只认工号。容器拿着工号 0，柜子锁上写的是工号 1000 —— 你（工号 1000）也开不了那把锁。而且连「把柜子里的东西扔了」都不行，因为那是**柜子**的门禁，不是格子里的门禁。

---

## 第 3 章：三种解法

三条路的区别是「**谁让步**」：

| 方案                        | 一句话           | 改的是谁         | 适用范围        | 可靠度         |
| ------------------------- | ------------- | ------------ | ----------- | ----------- |
| **A. `chown`**            | 让宿主目录去迁就容器    | 宿主目录属主       | 所有镜像        | ★★★ 最通用     |
| **B. `user:` / `--user`** | 让容器换个人来跑      | 容器进程 UID:GID | 镜像需支持任意用户启动 | ★★          |
| **C. `PUID` / `PGID`**    | 报个工号给镜像，让它自己换 | 镜像入口脚本       | **只有支持的镜像** | ★★ 选错镜像完全无效 |

### 3.1 方案 A：`chown` 改宿主目录属主（最通用）

先查容器实际用哪个 UID 跑：

```bash
docker exec <容器名> id
# 输出示例：uid=999(postgres) gid=999(postgres) groups=999(postgres)
```

再把宿主目录的属主改成同一个数字：

```bash
# 把宿主目录属主改成容器用户的 UID:GID（示例：1000）
sudo chown -R 1000:1000 /data/downloads
```

优点是任何镜像都管用；缺点是每次换镜像、换 UID 都得重新对一次。

### 3.2 方案 B：Compose 的 `user:` / `docker run --user`

这是 **Docker 原生**的能力，由容器运行时执行，对所有镜像都「生效」：

```yaml
services:
  app:
    image: some-image
    user: "1000:1000"        # 覆盖容器进程的 UID:GID
    volumes:
      - /data/downloads:/downloads
```

等价命令行：

```bash
docker run --user 1000:1000 -v /data/downloads:/downloads some-image
```

> [!warning] 注意：不是所有镜像都能换用户启动
> 有些镜像在初始化阶段**必须以 root 运行**（要改配置、装依赖、绑特权端口、设文件属主），一旦换成普通用户就会直接起不来或初始化失败。如果加了 `user:` 之后容器启动报错，退回去用方案 A。

### 3.3 方案 C：`PUID` / `PGID`——只对支持的镜像有效

这是最常被误解的一条，单独讲清楚。

```yaml
services:
  app:
    image: lscr.io/linuxserver/qbittorrent:latest
    environment:
      - PUID=1000
      - PGID=1000
    volumes:
      - /data/downloads:/downloads
```

> [!warning] 关键澄清：PUID / PGID 不是 Docker 的功能
> Docker 本身**不认识** `PUID` / `PGID`——它们只是两个普通的自定义环境变量，由**镜像自己的启动脚本**读取。以 linuxserver 系镜像为例：其 entrypoint（s6 `init-adduser`）启动时读这两个值，把镜像内部的固定用户 `abc` 改成你指定的数字，并顺手 `chown` 相关目录。
>
> 由此推出三条硬约束：
> 1. 只有**明确支持**的镜像写了才有用——linuxserver 系、hotio 系，以及基于它们 baseimage 构建的镜像；
> 2. 官方镜像（Postgres、Nextcloud、nginx 等）写 `PUID` **完全不生效**，它们只认方案 A / B；
> 3. linuxserver 官方明确说明其镜像**与 `--user` 不兼容**，所以方案 B 和方案 C 不要混用。
>
> 依据：linuxserver 官方文档《Understanding PUID and PGID》（2026-09 查阅）。

### 3.4 怎么选

1. 先翻**镜像文档**：出现 `PUID` / `PGID` 字样 → 方案 C（照抄官方示例即可）。
2. 文档没提 → 优先方案 A（`chown`），必要时用方案 B 微调。
3. 通用心法：**谁写文件谁就是属主**。与其追着容器改，不如让宿主目录去迁就它。

> [!tip] 大白话：三张工牌
> - **方案 A** = 把柜子的锁拆了重装，换成对方的工号（改环境，不改人）。
> - **方案 B** = 让容器换个工牌进厂，但有的工厂规定「进场必须用老板工牌」，那就换不了。
> - **方案 C** = linuxserver 家的特殊门禁卡：你在门口报个号（`PUID` / `PGID`），保安（entrypoint）自动把对应工牌挂你脖子上。
> 注意方案 C 的保安只在 linuxserver / hotio 这几栋楼上班——跑到别的楼报号，没人理你。

---

## 第 4 章：验证与排查三步

遇到 `Permission denied`，按顺序走这三步，别瞎试：

```bash
# ① 容器里进程实际以什么用户跑
docker exec <容器名> id

# ② 镜像默认的 User（来自 Dockerfile 的 USER 指令；没设置就是 root）
docker inspect <镜像名> --format '{{.Config.User}}'

# ③ 宿主挂载目录当前的数字属主（-n 是关键：直接看数字，不翻译成名字）
ls -ln /宿主机/挂载目录
```

判读方法：

| 步骤 | 它在回答什么问题 | 期望结果 |
| --- | --- | --- |
| ① | 容器「拿的是几号工牌」 | 得到容器进程的 UID，如 `999` |
| ② | 这面墙「出厂默认给谁发工牌」 | 空 = root；或 `www-data` 之类 |
| ③ | 文件柜的锁上「写的是几号」 | 得到宿主目录属主的数字 |

**三步对到同一个数字，权限问题就消失了。**

修完之后验证一次：

```bash
# 让容器在挂载点写一个测试文件
docker exec <容器名> touch /挂载点/.perm-test
# 回宿主机看属主是不是你要的 UID（不是 root 就对了）
ls -ln /宿主机/挂载目录/.perm-test
rm /宿主机/挂载目录/.perm-test
```

> [!tip] 大白话
> ① 问「我拿的是几号工牌」，② 问「这面墙出厂时默认给谁发工牌」，③ 看「柜子锁上是几号」。三个数字对齐，门自然就开了。

---

## 第 5 章：常见坑

| 坑 | 现象 | 正确做法 |
| --- | --- | --- |
| `PUID=0` / `PGID=0` | 等于没设置，而且更糟——等于明确告诉镜像「用 root 跑」 | 填 `id -u` / `id -g` 的真实值 |
| 改了 PUID，旧文件属主没变 | 启动脚本只 `chown` 它自己管的几个目录，存量文件不一定覆盖 | 手动清一次：`sudo chown -R 1000:1000 /data/...` |
| 把 PUID 当命令行参数 | `docker run --puid 1000 ...` 报 `unknown flag` | 它是环境变量，写成 `-e PUID=1000` |
| PUID 填了非数字 | 启动脚本报错，严重时值被拼进 shell 当命令执行（环境变量注入） | 只填纯数字，不要带引号、空格、`$(...)` |
| rootless 模式下按 rootful 算 | 按 1000 配的 PUID，写出来的文件属主变成 `100999` 之类的怪数字 | rootless 下容器 root 映射到宿主你的 UID，PUID 要按**重映射后**的数字算 |
| 命名卷换了镜像 | 新镜像 UID 不同，旧卷里文件还是旧属主 | `docker volume rm` 重建，或进容器手动 `chown` |
| Docker Desktop 挂 Windows 盘 | 改 `PUID` 看不出效果，属主始终是同一个 | 数据放 WSL2 原生路径（`~/...`），别放 `/mnt/c/...` |

### 关于最后一条（Windows / macOS 用户必看）

Docker Desktop 的 bind mount 要穿过一层 VM 和文件共享层。当你挂的是 **Windows 盘符**（`/mnt/c/...`）时，底层走 9P 协议：

- 9P **不保存也不遵守** Linux 的 UID / GID 与 `chmod` 位，`/mnt/c` 上的文件默认会呈现为 `root:root` 或挂载时指定的那个 uid；
- 也就是说，在 `/mnt/c` 上 `chown` / `chmod` **默认无效**（默认没开 `metadata`），重启 WSL 还会复位；
- 想让属主真正生效，得在 `/etc/wsl.conf` 里给 automount 加 `metadata`（可配合 `uid=` / `gid=`），然后 `wsl --shutdown` 重启 WSL。注意**不要**去改 Docker Desktop 自己那两个 WSL 发行版的配置。

最省事的做法是绕开这一层：把项目和数据放在 **WSL2 内部的 Linux 路径**（如 `~/docker/data`），那里是真正的 ext4，UID / GID 语义完整，性能和权限都正常。

---

## 第 6 章：实战场景：媒体 / 下载类容器

这类容器是「权限问题」的重灾区：

- qBittorrent / Transmission（下载器）
- Sonarr / Radarr（自动整理）
- Jellyfin / Emby（媒体服务器）
- 各类 NASTools

**90% 都要求你设置 `PUID` / `PGID`**，原因在于它们的完整工作流每一步都要**跨目录改写文件**：

1. 下载器把文件写进 `/downloads`；
2. 整理工具把它**重命名 / 硬链接 / 移动**到 `/media`；
3. 媒体服务器扫描 `/media` 并**写回元数据**（刮削的封面、nfo）。

只要中间有一环的属主对不上，就会连锁失败：

- 刮削失败（写不进元数据）
- 重命名失败
- 自动整理失败
- 日志里刷屏 `Permission denied`

> [!tip] 大白话
> 下载器是「厨房」，整理工具是「传菜员」，媒体库是「餐桌」。三个岗位必须能互相递盘子——只要有一个人拿的工牌刷不开下一道门，菜就卡在传送带上了。

---

## 相关笔记

- [[Docker容器服务访问宿主机文件]] - 挂载选型、权限对齐与安全边界完整实战
- [[OpenList网盘挂载-05-Docker映射]] - 容器以什么身份访问挂载文件
- [[Docker与DockerCompose命令速查]] - `docker run` / `docker compose` 常用命令
- [[docker容器搭建错误的知识讲解]] - 改了 compose 之后 Docker 会做什么
- [[linux的文件权限]] - Linux 权限位基础（rwx、属主 / 属组 / 其他人）
- [[Docker MOC]] - Docker 学习笔记目录

---

## 更新记录

- **2026-09-14**：重写为完整入门指南。修好第 1 章损坏的渲染行（`**Docker 里常见的是 UID / GID>` 未闭合 bold）；补 frontmatter（`title` / `created` / `updated` / `status` / `source_project`）；新增「三招解法对照表」「验证与排查三步」「常见坑表」三章；**修正关键事实错误**——原文把 `PUID` / `PGID` 当作通用做法，实为镜像 entrypoint 读取的自定义环境变量，仅 linuxserver / hotio 系有效；代码块中命令输出的语言标识由 bash 修正为 text；补 4 处 `[!tip] 大白话` 与双链。
  - 起因：2026-08-04 那轮批量更新只补了 frontmatter，且产物落在 `workspace/update-docker/updates/gid-uid/updated_note.md`，未回写 vault 笔记。
- **2026-08-04**：仅补齐 YAML frontmatter，正文未改动。
