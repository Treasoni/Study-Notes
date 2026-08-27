---
title: Docker与DockerCompose命令速查
tags: [docker, docker-compose, 命令速查, cheat-sheet, 入门]
created: 2026-08-08
updated: 2026-08-08
status: published
source_project: docker-compose-commands
---

# Docker 与 Docker Compose 命令的使用

> [!info] 相关目录
> 本笔记属于 [[Docker MOC]]。这是一份「Docker 与 Docker Compose 命令」的入门速查笔记：从「镜像 vs 容器」的心智模型讲起，接着是 Docker CLI 命令速查（镜像 / 容器 / 网络 / 卷 / 系统清理），再到 Docker Compose 编排与 compose.yaml 配置语法，最后附高频坑与排错速查表。零基础可通读一遍建立心智模型，之后当作随身速查手册随查随用。

---

## 目录

1. [第 1 章：初识 Docker：镜像与容器](#第-1-章初识-docker镜像与容器)
   - [镜像：一份可复用的「菜谱」](#镜像一份可复用的菜谱)
   - [容器：照着菜谱做出来的一盘菜](#容器照着菜谱做出来的一盘菜)
   - [日常流程：从拿菜谱到收桌子](#日常流程从拿菜谱到收桌子)
   - [改动要写进菜谱，而不是改那盘菜](#改动要写进菜谱而不是改那盘菜)
   - [这本笔记怎么用](#这本笔记怎么用)
2. [第 2 章：Docker 命令速查：镜像与容器管理](#第-2-章docker-命令速查镜像与容器管理)
   - [镜像命令速查：管好你的「菜谱」](#镜像命令速查管好你的菜谱)
   - [`docker run`：开容器总入口](#docker-run开容器总入口)
   - [容器生命周期命令：从开火到倒掉](#容器生命周期命令从开火到倒掉)
   - [易混点：两对命令单独拎出来](#易混点两对命令单独拎出来)
3. [第 3 章：Docker 命令速查：网络、卷与系统管理](#第-3-章docker-命令速查网络卷与系统管理)
   - [3.1 网络命令组：让容器互相找到对方](#31-网络命令组让容器互相找到对方)
   - [3.2 数据卷命令组：让数据不随容器消失](#32-数据卷命令组让数据不随容器消失)
   - [3.3 系统命令组：看家底与安全清理](#33-系统命令组看家底与安全清理)
4. [第 4 章：Docker Compose：v1/v2 与核心命令](#第-4-章docker-composev1v2-与核心命令)
   - [Compose 解决什么问题：从「一串 docker run」到「一个项目」](#compose-解决什么问题从一串-docker-run到一个项目)
   - [先分清两个 compose：v1 vs v2](#先分清两个-composev1-vs-v2)
   - [compose 核心命令速查表](#compose-核心命令速查表)
   - [最小示例：一个项目一键起停](#最小示例一个项目一键起停)
5. [第 5 章：compose.yaml 配置语法与常用工作流](#第-5-章composeyaml-配置语法与常用工作流)
   - [顶层结构：name / services / networks / volumes](#顶层结构name--services--networks--volumes)
   - [service 常用键详解](#service-常用键详解)
   - [关键语法点](#关键语法点)
   - [完整最小示例：nginx + postgres](#完整最小示例nginx--postgres)
   - [常用工作流命令序列](#常用工作流命令序列)
6. [第 6 章：常见坑与排错](#第-6-章常见坑与排错)
   - [6.1 容器启动即退出（最常见）](#61-容器启动即退出最常见)
   - [6.2 权限问题：Permission denied](#62-权限问题permission-denied)
   - [6.3 清理最佳实践](#63-清理最佳实践)
   - [6.4 Windows 挂载路径问题](#64-windows-挂载路径问题)
   - [6.5 其他高频坑](#65-其他高频坑)
   - [6.6 一页速查小结](#66-一页速查小结)

---

## 第 1 章：初识 Docker：镜像与容器

你有没有过这样的经历：照着网上教程部署软件，第一步就是 `docker pull`、`docker run`，但到底在拉什么、跑什么，心里没底。这一章先把 Docker 最核心的两个概念——**镜像**和**容器**——讲明白。只要这对关系清楚了，后面所有命令都只是围绕它俩打转。

### 镜像：一份可复用的「菜谱」

> [!tip] 大白话
> 把**镜像**想成一本菜谱：它是一份只读、可反复复用的「设计蓝图」，里面写好了代码、运行时、系统库和配置。菜谱本身不能吃，镜像本身也不能运行——它只是「怎么做」的完整说明。

一份镜像就是一个完整打包的「应用快照」：你想要的软件、它依赖的环境、默认配置，全都在里面。好处是**可复用**——同一个镜像可以随时拿出来，开出任意多个实例，彼此互不干扰。镜像和容器的关系，是 Docker 官方文档反复强调的第一课 [Docker Docs](https://docs.docker.com/get-started/)。

### 容器：照着菜谱做出来的一盘菜

> [!tip] 大白话
> 把**容器**想成照着菜谱现做出来的一盘菜：它是一个可运行、可修改、用完可扔的实例。同一份菜谱能做出一盘又一盘，同一份镜像也能同时开出很多容器，互不影响。

`docker run` 就是「做菜上桌」的动作：它拿一份镜像当菜谱，在机器上开出一个运行中的容器。你往容器里加了盐、改了口味，只影响这一盘；菜谱（镜像）原封不动。

### 日常流程：从拿菜谱到收桌子

Docker 最常用的几条命令，正好对应厨房里的一套动作 [Docker CLI 参考](https://docs.docker.com/reference/)：

| 命令 | 厨房动作 |
|------|---------|
| `docker pull` | 拿菜谱：从仓库把镜像下载到本地 |
| `docker run` | 做菜上桌：照镜像开出一个容器 |
| `docker ps` | 看看桌上摆了几盘：列出运行中的容器 |
| `docker stop` / `docker rm` | 收走 / 倒掉：停止并删除容器 |

> [!tip] 大白话
> 把容器想成一次性餐具：用完就扔，成本很低，不必心疼。**容器天生是「一次性」的**，这正是它的设计意图——随时开、随时扔。

### 改动要写进菜谱，而不是改那盘菜

新手最容易踩的坑：进到容器里手动改了一堆配置，重启容器后发现全没了。原因很简单——你改的是「那一盘菜」，菜谱（镜像）根本没变。想要长期保留改动，正确做法是：

1. 把改动写进 `Dockerfile`（相当于给菜谱加新步骤）；
2. 用 `docker build` 重新构建出一份新镜像；
3. 再用新镜像开容器。

这样每次开出来的容器，都是一模一样的「标准口味」，而不是靠手工补救的「这盘特有」。

### 这本笔记怎么用

这一系列笔记分两块：**先懂、再查**。第 1 章就是「先懂」的部分，帮你在脑子里搭好「镜像 vs 容器」这个心智模型；从第 2 章开始是「再查」的部分——每条命令都配了速查表和一句话解释，用到时随手翻对应章节即可，不必一次背完。

### 本章小结

- 镜像 = 只读的模板 / 菜谱，本身不能运行；容器 = 照镜像开出的运行实例 / 一盘菜。
- 同一份镜像可以同时开无数个容器，互不干扰。
- 核心命令流：`pull`（拿菜谱）→ `run`（上桌）→ `ps`（查看）→ `stop`/`rm`（收走）。
- 容器用完可扔；长期改动写进 `Dockerfile` 重新 `build`，而不是手工改容器。
- 本笔记「先懂再查」：本章建立心智模型，后续章节当速查表。

### 下一章预告

概念清楚了，接下来该动手了。第 2 章进入 Docker 命令速查，从「拉取、查看、构建镜像」开始，再到 `docker run` 的完整用法——你会发现，所有命令都在这一章的厨房比喻里各就各位。

---

## 第 2 章：Docker 命令速查：镜像与容器管理

上一章我们搭好了心智模型：**镜像是菜谱，容器是照着菜谱做出来的那盘菜**。这一章开始动手——把最常用的镜像命令和容器命令挨个过一遍。你不需要背，用的时候翻回来对照即可；每条命令都能在厨房比喻里找到自己的位置。

### 镜像命令速查：管好你的「菜谱」

镜像命令管的是"菜谱本身"：拿、看、扔、造、起名、寄出去。

| 命令 | 做什么 | 厨房里的动作 |
|------|-------|-------------|
| `docker pull NAME[:TAG]` | 从仓库拉取镜像到本地 | 拿菜谱回家 |
| `docker images` | 列出本地已有的镜像 | 翻翻家里存了哪些菜谱 |
| `docker rmi IMAGE` | 删除本地镜像 | 扔掉一本菜谱 |
| `docker build -t NAME .` | 用当前目录的 Dockerfile 构建镜像 | 照着新步骤写出一本新菜谱 |
| `docker tag 源 目标` | 给镜像加标签 / 别名 | 给同一道菜再多起一个菜名 |
| `docker push NAME[:TAG]` | 推送到远程仓库 | 把菜谱寄回公共厨房 |

其中 `TAG` 是版本号，不写默认 `latest`，例如 `docker pull ubuntu:22.04` 和 `docker pull ubuntu` 拿到的版本不同 [Docker CLI 参考](https://docs.docker.com/reference/)。

> [!tip] 大白话
> `rmi` 是删**镜像**（菜谱），`rm` 是删**容器**（那盘菜）——俩兄弟别搞混，下一节会见到 `rm`。`tag` 不复制内容，只给同一个镜像多贴一个名字，像"番茄炒蛋"和"西红柿炒鸡蛋"其实是同一盘。`push` 前要先 `docker login` 登录仓库，相当于在公共厨房报个名，人家才允许你寄菜谱；自己写的菜谱不 push，别人 `pull` 不到。

### `docker run`：开容器总入口

语法：`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`。八个最常用的 flag 记熟，日常 90% 的场景就够了：

| Flag | 含义 | 示例 |
|------|------|------|
| `-d` | 后台运行（detached），不霸占终端 | `-d` |
| `-p 宿主:容器` | 端口映射，让外面能访问容器内服务 | `-p 8080:80` |
| `-v 宿主:容器` | 挂载目录 / 卷，两边目录互通 | `-v $(pwd):/app` |
| `-e KEY=VALUE` | 设置环境变量 | `-e TZ=Asia/Shanghai` |
| `--rm` | 容器退出时自动删除（适合临时任务） | `--rm` |
| `--name 名字` | 给容器起名，之后用名字引用 | `--name web` |
| `--restart 策略` | 崩溃后自动重启，策略有 `no` / `on-failure` / `always` / `unless-stopped` | `--restart=always` |
| `-it` | 交互式终端（进容器里敲命令） | `-it` |

> [!tip] 大白话
> `-p 8080:80` 像给容器这间房的外墙开一扇门：宿主机 8080 号门，直通容器里的 80 号房间，读作"宿主机 8080 → 容器 80"。容器默认是封闭的（网络隔离），外面的浏览器根本够不到它，必须显式开这扇门才能访问。
> `--restart=always` 像给这道菜装了个"自动回锅"开关：容器意外崩溃或机器重启后，Docker 会自动把它重新拉起来，不用你手动 `start`。

#### 综合示例：一行命令跑起 nginx

```bash
docker run -d -p 8080:80 --name web --restart=always nginx
```

逐个拆开看：

- `-d`：后台运行，终端不被霸占；
- `-p 8080:80`：访问 `http://localhost:8080` 就能到达容器内 nginx 的 80 端口；
- `--name web`：容器起名 `web`，后面 `docker stop web` 直接叫名字；
- `--restart=always`：nginx 崩溃自动重启；
- `nginx`：用官方 nginx 镜像。若本地没有，`run` 会自动先 `pull` 再运行。

### 容器生命周期命令：从开火到倒掉

镜像命令管菜谱，容器命令管那盘菜。一条生命周期走完：**开 → 看 → 停 → 再开 → 扔**。

| 命令                                      | 做什么                 | 厨房比喻          |
| --------------------------------------- | ------------------- | ------------- |
| `docker ps`                             | 列出运行中的容器            | 看桌上现在摆了几盘     |
| `docker ps -a`                          | 列出所有容器（含已停止）        | 连收走的盘子一起看     |
| `docker start CONTAINER`                | 启动一个已存在的容器          | 把收走的菜重新端上桌    |
| `docker stop CONTAINER`                 | 优雅停止容器              | 收盘子，给几秒收拾时间   |
| `docker restart CONTAINER`              | 重启容器                | 撤下去重新端上来      |
| `docker rm [-f] [-v] CONTAINER`         | 删除容器                | 倒掉这盘菜，盘子也扔    |
| `docker exec [-it] CONTAINER CMD`       | 在运行中的容器里执行命令        | 到后厨那盘菜旁边加调料   |
| `docker logs [-f] [--tail N] CONTAINER` | 查看容器日志              | 看这盘菜出锅后的流水账   |
| `docker inspect CONTAINER\|IMAGE`       | 查看底层详情（IP、挂载、环境变量）  | 翻后厨台账，查完整记录   |
| `docker cp 容器:路径 宿主路径`                  | 与容器双向复制文件           | 从菜盘夹走 / 放进配料  |
| `docker stats`                          | 实时看 CPU / 内存 / 网络占用 | 盯后厨火力、用水用电    |
| `docker top CONTAINER`                  | 看容器内进程              | 看这道菜正在被哪些工序处理 |

> [!tip] 大白话
> `logs -f` 是"跟随"日志——像盯着锅盖，新冒出的蒸汽（日志）实时刷出来；加 `--tail 100` 表示只从最后 100 行开始看，避免刷屏。排错时它的出场率最高。

### 易混点：两对命令单独拎出来

新手最容易把这两对搞混，单独标注。

> [!warning] 易混点 1：`exec -it` 进容器 vs `cp` 拷文件
> `docker exec -it web sh` 是**钻进运行中的容器里敲命令**——像到那盘菜旁边加调料，改的是容器内环境；
> `docker cp web:/etc/nginx/nginx.conf ./` 是把容器里的文件**拷到宿主机**（反过来 `docker cp ./x web:/path` 把宿主文件拷进容器）——像夹走或放进配料。
> 记法：`exec` 进去**干活**，`cp` 在两头**搬运文件**，`cp` 不进入容器。

> [!warning] 易混点 2：`ps` 只看运行中，`ps -a` 才看全部
> `docker ps` 默认**只列出运行中的容器**，已停止的会被藏起来。排错第一步通常就是 `docker ps -a`——否则一个"一启动就退出的容器"你根本看不见。想连停掉的容器一起看，加 `-a`（all）。

### 本章小结

- 镜像命令 = 菜谱管理：`pull` 拿、`images` 看、`rmi` 扔、`build -t` 造、`tag` 起别名、`push` 寄仓库。
- `docker run` 是开容器总入口，核心 flag：`-d` 后台、`-p` 端口映射、`-v` 挂载、`-e` 环境变量、`--name` 命名、`--rm` 退出即删、`--restart` 自动重启、`-it` 交互终端。
- 容器生命周期一条龙：`ps` 看 → `start/stop/restart` 控制 → `rm` 删除，配 `exec` / `logs` / `inspect` / `cp` / `stats` / `top` 日常运维。
- 易混点：`exec -it` 进容器干活，`cp` 双向搬文件；`ps` 只看运行中，`ps -a` 才含已停止。
- 每条命令都能对上第 1 章的厨房比喻，用到的场景随手翻回本表即可。

### 下一章预告

镜像和容器这两类最常用的命令已就位。但容器的价值不止"跑一个进程"——多个容器之间怎么联网、数据怎么持久化（卷）、磁盘满了怎么安全清理，是第 3 章「网络、卷与系统管理」要解决的。那些命令同样是随查随用的速查表。

---

## 第 3 章：Docker 命令速查：网络、卷与系统管理

上一章我们把镜像和容器的命令玩熟了，但一个真实应用还有两个「看不见的邻居」：容器之间要互相通信（网络），数据要跨重启存活（数据卷）。这一章把这两组命令讲完，再教你安全地做系统清理——这可能是整个 Docker 里最需要「手别抖」的操作。

### 3.1 网络命令组：让容器互相找到对方

默认情况下，多个容器会加入同一个名为 `bridge` 的默认网络，可以通过容器名互相访问。需要隔离、自定义网段时，再自己建网络。

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker network ls` | 列出所有网络 | `docker network ls` |
| `docker network create [-d 驱动] NAME` | 新建网络（`-d bridge` 是默认驱动） | `docker network create mynet` |
| `docker network inspect NAME` | 查看网络详情（网段、已连接容器 IP） | `docker network inspect mynet` |
| `docker network connect 网络 容器` | 把运行中的容器接入网络 | `docker network connect mynet web` |
| `docker network disconnect 网络 容器` | 把容器移出网络 | `docker network disconnect mynet web` |
| `docker network rm NAME` | 删除网络（须先断开所有容器） | `docker network rm mynet` |

> [!tip] 大白话
> 把网络想成**楼里的内线电话**：容器一搬进这栋楼（网络），就有了一个内部号码（IP），通过容器名就能拨通彼此；`connect`/`disconnect` 就是给某个房间「接通/掐掉内线」。所以——多个容器要协作，就放进同一个网络，互相用名字访问，而不是写死 IP。

### 3.2 数据卷命令组：让数据不随容器消失

容器是「用完可扔」的，但数据库、上传文件这些数据必须活下来。数据卷（volume）就是 Docker 管理的一块独立存储，删容器不影响它。

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker volume ls` | 列出所有卷 | `docker volume ls` |
| `docker volume create NAME` | 新建命名卷 | `docker volume create mydata` |
| `docker volume inspect NAME` | 查看卷详情（挂载点、驱动） | `docker volume inspect mydata` |
| `docker volume rm NAME` | 删除指定卷 | `docker volume rm mydata` |
| `docker volume prune [-a] [-f]` | 清理未使用的卷（`-a` 也删未被引用但仍在用的，需谨慎） | `docker volume prune -f` |

挂载数据有两种常见方式，第 2 章的 `-v` 参数两者都支持：

- **命名卷**：`-v mydata:/data`，存放位置由 Docker 管理，路径可移植，适合数据库等需要长期保存的数据。
- **绑定挂载**：`-v $(pwd):/data`，直接指向宿主机某个目录，适合开发时改代码即时生效；但权限按数字 UID/GID 匹配，容易踩坑（见 [[docker里的GID和UID]]）。

> [!tip] 大白话
> 把数据卷想成**租客房间里的冰箱**：容器是租客，退了房（删除容器）冰箱和里面的东西还在；只有你主动把冰箱拖走（`volume rm` / `prune`），数据才真没了。所以——想留数据，就挂卷；删容器时别顺手把卷也删了。

### 3.3 系统命令组：看家底与安全清理

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker info` | 系统级信息（容器/镜像数量、存储驱动） | `docker info` |
| `docker version` | 分别显示 Client 与 Server/Engine 版本 | `docker version` |
| `docker system df` | 磁盘占用统计（镜像/容器/卷/构建缓存） | `docker system df` |
| `docker system prune [-a] [-f] [--volumes]` | 清理闲置资源（见下表） | `docker system prune -a` |
| `docker login [仓库]` | 登录镜像仓库（建议 `--password-stdin` 安全读密码，避免明文入历史） | `docker login` |

`system prune` 的 Flag 逐层「加码」，破坏性也随之加大：

| Flag | 含义 | 风险 |
|------|------|------|
| （无 Flag） | 删已停容器 + 未用网络 + 悬空镜像 + 未用构建缓存 | 低 |
| `-a` | 连**未被任何容器使用**的镜像一起删 | 中：之后拉镜像要重新下载 |
| `-f` | 跳过确认提示（否则会先问一句） | 低 |
| `--volumes` | 额外清理未使用的卷 | **高：可能销毁数据** |

> [!warning] 卷默认不自动删除
> `docker system prune` 默认**不会**碰数据卷。官方理由是：*"Volumes are never removed automatically, because to do so could destroy data."*（卷永不自动删除，因为那可能摧毁数据）。所以只有当你**明确**加 `--volumes` 时才会删卷——在跑这条命令前，务必确认卷里的数据不再需要，或已备份。

安全清理的推荐顺序：先 `docker system df` 预览占了多大空间 → 日常用 `docker system prune -a --filter "until=24h"` 只清 24 小时前的闲置镜像 → 需要时按类型单独清理（`docker container prune`、`docker image prune -a`、`docker network prune`、`docker buildx prune`）。

> [!warning] 别手滑
> `docker system prune -a --volumes` 会一口气删掉所有未使用镜像和未使用卷。心情不好想「大扫除」时可以这么干，但请先背出你哪几个卷里有数据库——**一旦删了，没有任何回收站**。

### 本章小结

- 网络是容器间互相发现的通道：`network create` + `connect`，容器用名字互访。
- 数据卷是独立于容器的存储：删容器不删卷，只有 `volume rm` / `prune` 才真正清数据。
- 挂载分两种：命名卷（Docker 管位置，适合持久数据）与绑定挂载（直接指宿主机目录，注意 UID/GID）。
- 清理前先 `system df` 看家底；`prune` 默认不删卷，加 `--volumes` 才是高风险的真正清空。
- `--password-stdin` 登录仓库，避免密码留在命令历史里。

### 下一章预告

单个容器的「生老病死」和「周边配套」你已经全会了。但真实项目往往是十几个容器一起跑——逐个 `docker run` 会把人逼疯。下一章进入 Docker Compose，看怎么把这一整套命令写进一个文件、一条命令全部拉起。

---

## 第 4 章：Docker Compose：v1/v2 与核心命令

前几章讲的都是**单容器**命令：`docker run` 开一个容器、`docker ps` 看一个容器。可真实应用往往是一「堆」容器：前端一个、后端一个、数据库一个。如果每个都要手动敲 `docker run`，还要记住端口映射、数据卷、环境变量、容器之间的网络连通，用不了几个服务就会疯掉。这一章介绍 **Docker Compose**——把「一串 `docker run`」统一写进一个文件，用一条命令编排成一个项目。

### Compose 解决什么问题：从「一串 docker run」到「一个项目」

假设一个最简单的 Web 应用有三部分：数据库（db）、后端（backend）、前端（frontend）。不用 Compose 的话，你要手动执行：

```bash
docker run -d --name db -p 5432:5432 -v db-data:/var/lib/postgresql/data -e POSTGRES_USER=example postgres
docker run -d --name backend -p 8080:8080 -e DB_HOST=db myapp/backend
docker run -d --name frontend -p 80:80 myapp/frontend
```

每一条都要精确记参数，容器之间还得互相连通。服务一多，这套手写流程根本没法维护。

> [!tip] 大白话
> 把 Compose 想成一张「项目清单」：以前你要亲手一条条执行 `docker run`，现在把这些命令统一写进一个 `compose.yaml` 文件，然后 `docker compose up -d` 一条命令，整个项目（前端 + 后端 + 数据库）就全部按清单启动、连网、挂卷。就像点外卖，不用挨个窗口买，一张单子全搞定。

技术上，Compose 读取 `compose.yaml`，把里面声明的每个 service 翻译成容器的创建、网络、卷操作，并自动处理服务间的网络连通和依赖顺序 [Compose 应用模型](https://docs.docker.com/compose/compose-application-model/)。实践上，`up -d` 一条命令等于之前的 N 条 `docker run`，`down` 又能一键拆除整个项目。

### 先分清两个 compose：v1 vs v2

网上教程里你可能见过两种写法：`docker-compose`（带连字符）和 `docker compose`（带空格）。这俩**不是同一个东西**，必须分清 [v1→v2 迁移文档](https://docs.docker.com/compose/migrate/)：

| | v1 | v2 |
|---|---|---|
| 命令 | `docker-compose`（连字符） | `docker compose`（空格） |
| 实现 | 独立 Python 工具 | Go 编写的 Docker CLI 插件 |
| 状态 | 已弃用、停止维护 | 现行标准，随 Docker Desktop / Engine 安装 |
| 配置文件 | `docker-compose.yml` | 无需修改，直接通用 |

**迁移方法**：把连字符换成空格即可，绝大多数命令 drop-in 兼容：

```bash
docker-compose up -d    →    docker compose up -d
```

但有两个行为差异，迁移时容易撞上：

- **容器命名**：v2 用连字符 `example-frontend-1`，v1 用下划线 `example_frontend_1`。
- **scale**：v2 移除了 `docker compose scale`，改用 `up --scale`。

> [!tip] 大白话
> 把 v1/v2 想成同一款软件的新旧两代：v1 是独立的小工具（已停更），v2 是直接长进 Docker 身体里的插件。日常只要记住用 v2 的 `docker compose`（空格）；看到教程里旧版的 `docker-compose`（连字符），把它换成空格就行，配置文件不用改。

### compose 核心命令速查表

在项目目录（放 `compose.yaml` 的地方）执行 [Compose CLI 参考](https://docs.docker.com/reference/cli/docker/compose/)：

| 命令 | 用途 |
|------|------|
| `docker compose up [-d] [--build]` | 构建、创建、启动全部服务；`-d` 后台；`--build` 启动前构建 |
| `docker compose down [-v]` | 停止并删除容器与默认网络；默认保留命名卷，`-v` 连卷一起删 |
| `docker compose ps` | 列出各服务容器与状态 |
| `docker compose logs [-f] [-n N]` | 查看全部服务日志；`-f` 跟随滚动，`-n` 只看末尾 N 行 |
| `docker compose exec SERVICE CMD` | 在**运行中**容器执行命令，如 `exec frontend sh` |
| `docker compose build [--no-cache]` | 构建 / 重建镜像 |
| `docker compose pull / push` | 拉取 / 推送各服务镜像 |
| `docker compose config [-q]` | 合并并渲染最终配置；`-q` 仅校验不输出 |
| `docker compose run SERVICE CMD` | 按服务定义**新建一次性容器**执行命令（区别于 `exec`） |
| `docker compose restart / stop / start` | 重启 / 停止（保留容器）/ 启动 |
| `docker compose stats / top / images` | 资源占用 / 容器内进程 / 已用镜像 |

**关键 Flag 单独强调**：

- `up -d`：后台运行（detached）。不加 `-d` 会占住当前终端，Ctrl+C 就停。
- `up --build`：启动前先重新构建镜像。改完代码不想手动 `build` 时用。
- `down -v`：破坏性操作，删容器、网络，**连命名卷一起删**，数据永久丢失。
- `config -q`：静默校验配置文件。YAML 写错时，它是最快的排错工具。

> [!warning] 破坏性操作
> `docker compose down -v` 里的 `-v` 会删除命名卷（命名卷 = 持久化数据仓库）。容器删了可以重建，**卷删了数据就没了**。日常清理用 `docker compose down`（保留卷）即可，只有确认数据不要了才加 `-v`。

### 最小示例：一个项目一键起停

写一个最简 `compose.yaml`：

```yaml
services:
  web:
    image: nginx:1.27
    ports:
      - "8080:80"
```

在同一个目录下执行：

```bash
docker compose up -d      # 拉取 nginx 并后台启动，容器自动命名 <项目名>-web-1
docker compose ps         # 看到 web 服务在运行
docker compose logs -f    # 跟随日志，Ctrl+C 退出
docker compose down       # 停止并删除容器、网络，保留数据卷
```

> [!tip] 大白话
> 把 compose 里的服务名想成「项目成员的称呼」：写 `web` 就是给前端组件起名，启动后容器会自动变成「项目名-web-1」。之后你不用记容器 ID，直接用服务名 `web` 就能进容器、看日志——这就是「编排」带来的便利。

### 本章小结

- Compose = 把一串 `docker run` 统一写进一个文件，用一条命令编排成项目。
- `docker compose`（v2，空格）是现行标准；`docker-compose`（v1，连字符）已弃用，连字符改空格即可迁移。
- v2 容器名用连字符（`example-frontend-1`）、v1 用下划线；v2 移除了 `compose scale`。
- 核心命令围绕 `up` / `down` 转：`up -d` 后台起、`down` 拆除（保留卷）、`down -v` 破坏性删卷。
- `config -q` 是配置校验神器，YAML 写错时快速定位。

### 下一章预告

命令会用了，下一步就是读懂并写出 `compose.yaml`。第 5 章深入配置语法：`services` 里每个键（`image` / `build` / `ports` / `environment` / `volumes` / `depends_on`…）是什么意思、命名卷为什么必须顶层声明、`$VAR` 插值怎么转义。啃下语法，你就能从「会用命令」升级到「自己编排一套多服务应用」。

---

## 第 5 章：compose.yaml 配置语法与常用工作流

上一章我们学会了 `docker compose` 这条命令怎么用：`up`、`down`、`logs`、`exec`……但命令只是"按钮"，真正决定一个 Compose 项目长什么样的，是那个叫 `compose.yaml` 的配置文件。本章就来啃这份配置文件的语法：顶层结构、service 常用键、几个绕不开的变量语法，最后给一个 nginx + postgres 的完整最小示例，并串起一套日常开发最常用的工作流命令序列。学完本章，你就能读懂别人的 `compose.yaml`，也能从零写出一份自己的。

### 顶层结构：name / services / networks / volumes

一份 `compose.yaml` 最外面（顶层）有四个关键字段，其中只有一个必填：

```yaml
name: myapp                 # 项目名（可选，v2 支持）
services:                   # 必填：定义"有哪些服务"
  web: ...
  db:  ...
networks:                   # 可选：自定义网络
  front-tier: {}
volumes:                    # 可选：命名卷声明
  db-data:
```

- `name`：给这个项目起名。不写的话，Compose 默认用**目录名**当项目名。项目名会进入容器名、默认网络名里，所以改名会影响后面 `down` 时能不能找到这些资源。
- `services`：**唯一必填**的顶层块，里面每个 key 是一个服务（就是一个容器的配置模板）。
- `networks`：声明要用到的自定义网络。不写也能用，Compose 会创建一个默认网络把同项目所有服务连通。
- `volumes`：声明**命名卷**。数据卷和网络一样，顶层先"开个户"，服务里才能引用。

> [!tip] 大白话
> **项目 / 服务 / 命名卷**：把项目想成**整套应用**（默认用目录名命名，比如 `myapp`）；服务就是**应用里的一个个组件**——`web`（网页）、`db`（数据库），每个组件对应一个容器，容器自动命名为 `项目名-服务名-序号`（如 `myapp-web-1`）；命名卷则是**跨容器重启的持久化仓库**——容器销毁了、数据还在仓库里，下次启动还能接着用。就像一家店：店名是项目，前台和后厨是服务，仓库里的存货是命名卷，店员走了仓库不会跟着消失。

### service 常用键详解

service 下的键决定这个容器"怎么启动"。我们按用途分组看（[语法参考：Compose 官方文件](https://docs.docker.com/reference/compose-file/)）：

**镜像与构建**

```yaml
services:
  web:
    image: nginx:1.27       # 用现成镜像
  api:
    build: ./backend        # 用本地 Dockerfile 构建
    image: my-backend:1.0   # 构建完打上这个标签
```

- `image`：直接拉取或指定使用的镜像。
- `build`：本地构建路径（`./backend` 表示该目录下的 Dockerfile）。`build` 和 `image` 可以同时写——构建完成后再用 `image` 打标签。

**启动命令**

```yaml
services:
  web:
    command: ["nginx", "-g", "daemon off;"]   # 覆盖镜像的 CMD
    entrypoint: /entry.sh                      # 覆盖镜像的 ENTRYPOINT
```

- `command`：覆盖镜像里的 CMD，指定容器启动后跑什么命令。
- `entrypoint`：覆盖镜像里的 ENTRYPOINT。记住一句话：ENTRYPOINT 是"入口脚本"，`command` 是"传给它的参数"，command 覆盖不会动 entrypoint。

**端口与暴露**

```yaml
services:
  web:
    ports:
      - "8080:80"           # 宿主机8080 → 容器80，字符串形式
    expose:
      - "3000"              # 仅项目内其他服务可访问，不映射到宿主机
```

- `ports`：把容器端口**映射到宿主机**，格式 `"宿主机端口:容器端口"`。别人访问你机器的 8080 就能进到容器里的 80。
- `expose`：只声明容器开了某个端口，供**同网络其他服务**访问，宿主机访问不到。常用于 `web` 对 `api` 说"我只开放 3000 给你"。

**环境变量**

```yaml
services:
  db:
    environment:                    # 直接写变量
      POSTGRES_USER: example
      ENABLE_FEATURE: "true"        # 布尔值必须加引号，否则被 YAML 解析成布尔
    env_file:                       # 从文件读变量
      - ./.env.backend
```

- `environment`：直接指定环境变量。注意 `true`/`false`/数字要加引号，否则 YAML 会把它当成布尔或数字而不是字符串。
- `env_file`：从一个文件批量读入环境变量。**优先级：`environment` 里的值会覆盖 `env_file` 里的同名值**。

**数据卷**

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data   # 命名卷：须在顶层 volumes 声明
      - ./config:/etc/app:ro               # 绑定挂载：宿主路径:容器路径[:ro]
```

- 命名卷：把数据持久化到 Compose 管理的卷里，容器删了数据还在，**必须在顶层 `volumes:` 声明后才能在 service 里引用**。
- 绑定挂载：直接把宿主机的某个目录（如 `./config`）挂进容器，`./` 是相对 `compose.yaml` 所在目录的相对路径；`:ro` 表示只读。

**服务依赖与健康检查**

```yaml
services:
  web:
    depends_on:
      db:
        condition: service_healthy   # 等 db 健康了才启动 web
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      retries: 3
```

- `depends_on`：控制启动顺序。简单写法 `depends_on: [db]` 只保证"db 先启动"，不保证 db 已就绪；长语法 `condition: service_healthy` 则等 db 通过健康检查才启动。
- `healthcheck`：给容器定义健康检查。`test` 是检查命令，`interval` 是间隔，`retries` 是失败几次算不健康。

**重启策略与网络**

```yaml
services:
  web:
    restart: unless-stopped   # no | always | on-failure | unless-stopped
    networks:
      - front-tier
```

- `restart`：容器退出后是否自动重启。`unless-stopped` 最常用——除非你手动 stop，否则挂了自动拉起。
- `networks`：把服务挂到哪个自定义网络；不写则进默认网络。

### 关键语法点

几个容易踩坑、但看懂一次就再也忘不掉的语法规则：

**命名卷必须顶层声明**。service 里的 `volumes:` 只是"引用"，顶层 `volumes:` 才是"开户"。漏了顶层声明，`docker compose up` 会直接报错说卷未定义。

**环境变量插值与转义**。`compose.yaml` 的值里 `$VAR` 或 `${VAR}` 会被 Compose 用宿主环境变量替换（常用于端口、镜像 tag 这类"部署时才知道"的值）。想输出**字面**的 `$`，必须写成 `$$`。支持两种便捷写法：

```yaml
services:
  web:
    image: nginx:${NGINX_TAG:-1.27}     # 没设 NGINX_TAG 就用 1.27
    ports:
      - "${HOST_PORT:?请先设置 HOST_PORT}:80"   # 没设就报错并中断
```

- `${VAR:-default}`：变量为空或未设时，用 `default` 兜底。
- `${VAR:?error message}`：变量必须存在，否则启动时报错退出——适合防呆。

**`.env` 自动加载与优先级**。Compose 会自动读取 `compose.yaml` 旁边的 `.env` 文件，把里面的变量用于上面的插值。注意：**`.env` 只用于配置插值，不会自动注入容器**（容器里的变量要靠 `environment` / `env_file`）。变量覆盖优先级从高到低：

```
Shell 里的环境变量 > --env-file 指定的文件 > 项目旁的 .env
```

**默认文件名与 `-f`**。默认找 `compose.yaml`（`docker-compose.yaml` 也认）。想用别的文件名或合并多个文件，用 `-f`，且可多次指定：

```bash
docker compose -f prod.compose.yaml up -d
docker compose -f base.yaml -f override.yaml up -d   # 后者覆盖前者同名键
```

> [!tip] 大白话
> **`$$` 转义**：把 `$` 想成**钥匙串上的特殊挂扣**——Compose 看到 `$` 就会去口袋里翻"变量钱包"。想让系统真的打出一个 `$` 符号（比如给容器传 `$HOME` 这种字符串），就得把它"锁"成 `$$`：两个挂扣叠一起，Compose 就知道"这不是变量，你直接打印吧"。所以：想取变量用 `$VAR`，想打字面 `$` 用 `$$`。

### 完整最小示例：nginx + postgres

把上面所有知识点串起来，写一个双服务的最小项目：`web`（nginx 网页）+ `db`（postgres 数据库），数据库数据用命名卷持久化，`web` 等 `db` 健康后才启动。

```yaml
name: myapp
services:
  web:
    image: nginx:1.27
    ports:
      - "8080:80"                     # 浏览器访问 localhost:8080
    depends_on:
      db:
        condition: service_healthy    # db 健康了才启动 web
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: myapp
    volumes:
      - db-data:/var/lib/postgresql/data   # 数据存到命名卷
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U example"]
      interval: 10s
      retries: 5
    restart: unless-stopped

volumes:
  db-data:          # 命名卷顶层声明，缺了这里 up 会报错
```

保存为 `compose.yaml` 后，在**同一目录**执行首次部署：

```bash
docker compose up -d
# 输出类似：
#  [+] Running 4/4
#  ✔ Network myapp_default    Created
#  ✔ Volume myapp_db-data     Created
#  ✔ Container myapp-db-1     Started
#  ✔ Container myapp-web-1    Started
```

可以看到 Compose 自动做了三件事：建了项目专属网络、创建了命名卷、按依赖顺序启动了两个容器（容器名都是 `项目-服务-序号`）。打开 `http://localhost:8080` 就能看到 nginx 欢迎页。

> [!tip] 大白话
> **depends_on + healthcheck 的配合**：`depends_on` 像"等同事到岗"的先后顺序，但"到岗"不等于"能干活"——数据库容器起来了，可能还在初始化。`healthcheck` 就是给 db 装了个**对讲机**，web 一直听它喊"我准备好了"才开工。这样就不会出现网页先启动、一访问数据库就报"连不上"的尴尬。

### 常用工作流命令序列

配置写好了，日常就是这一套"启动 → 更新 → 看日志 → 进容器 → 清理 → 校验"的循环：

```bash
# 1. 首次部署（拉镜像 + 建网络/卷 + 后台启动）
docker compose up -d

# 2. 更新镜像（重新拉取最新镜像，只重建镜像有变的服务）
docker compose pull && docker compose up -d

# 3. 跟随日志（Ctrl+C 退出跟随）
docker compose logs -f

# 4. 进运行中的容器调试
docker compose exec web sh

# 5. 优雅清理（停止并删除容器/默认网络，保留数据卷）
docker compose down

# 6. 校验配置（展开变量、短语法，并打印最终合并结果）
docker compose config
```

两条易混的清理命令，务必分清：

- `docker compose down`：停止容器、删掉容器和默认网络，**保留命名卷**——数据还在，下次 `up` 直接恢复。
- `docker compose down -v`：在 `down` 基础上**额外删除命名卷**，数据库数据一并消失。

> [!warning] 易错点
> **`down -v` 是破坏性操作**。命名卷默认不自动删是官方设计——因为里面存的是真实数据。养成习惯：不确定卷里有没有重要数据，就只用 `down`，把 `-v` 留给"确定要推倒重来"的场景。

`docker compose config -q` 是校验的静默版：不打印内容，语法有问题才报错，适合写进脚本做 CI 检查；`docker compose config` 完整版会把 `${VAR}` 展开后的最终配置打印出来，是排查"变量为什么没生效"的利器。

### 本章小结

- `compose.yaml` 顶层只有 `services` 是必填，`name` / `networks` / `volumes` 按需声明；项目名默认取目录名。
- service 常用键可以分五组记：镜像/构建（`image`、`build`）、启动命令（`command`、`entrypoint`）、网络（`ports`、`expose`、`networks`）、配置（`environment`、`env_file`、`volumes`）、运维（`depends_on`、`healthcheck`、`restart`）。
- 三个必须背的语法规则：命名卷要顶层"开户"；`$VAR` 做插值、`$$` 打字面 `$`、`${VAR:-default}` 兜底、`${VAR:?err}` 防呆；`.env` 只用于插值不注入容器，优先级 Shell > `--env-file` > `.env`。
- 一份 nginx + postgres 的最小 `compose.yaml` 配 `docker compose up -d`，就能一键跑起整套双服务应用。
- 日常工作流六连：`up -d`（部署）→ `pull && up -d`（更新）→ `logs -f`（看日志）→ `exec`（进容器）→ `down`（清理保数据）→ `config`（校验）。
- `down` 保留数据卷，`down -v` 才删卷——后者是破坏性操作，慎用。

### 下一章预告

配置语法已经打通，下一步自然要面对"写完的配置真的能跑起来吗"——第 6 章我们进入最常见的高频坑与排错：容器启动即退出、权限问题、端口冲突、Windows 挂载路径，每一条都配对应的排查命令和退出码定性表，让你遇到问题能自己定位。

---

## 第 6 章：常见坑与排错

前几章我们学会了 Docker 的镜像、容器、网络、卷命令，也学会了用 Compose 一键编排整套应用。但真正上手时你会发现：命令敲对了，容器却一启动就退出；日志里全是 `Permission denied`；Compose 一跑就报路径错误。本章把这些「翻车现场」按「症状 → 排查 → 解决」整理成三张速查表，遇到问题时直接按图索骥。不必一次背完，**用到再查**是本章的正确打开方式。

### 6.1 容器启动即退出（最常见）

> 症状：`docker ps` 里看不到容器，加 `-a` 才看到它 `Exited (1) 2 seconds ago`。

**先别急着翻日志**，第一步是看退出码。退出码是容器给你留的「遗言」，一张表就能给情况定性：

| 退出码 | 含义 | 典型原因 |
|--------|------|---------|
| 0 | 前台进程正常跑完就退出 | 应用自己后台化了（daemonize），PID 1 一结束容器就停 |
| 1 | 应用启动崩溃 | 配置错误、缺环境变量/密钥、依赖未就绪 |
| 126 | 文件存在但不可执行 | 权限拒绝（没有执行位） |
| 127 | 命令未找到 | 二进制缺失或路径写错 |
| 137 (128+9) | 进程被 SIGKILL 强杀 | 内核 OOM killer 杀掉（超内存限制） |

记忆规则很简单：**退出码 = 128 + 信号编号**。信号 9 是 SIGKILL（强杀），所以 137 = 128 + 9；信号 15 是 SIGTERM（优雅终止），对应 143。

> [!tip] 大白话
> 把退出码想成**集装箱上的故障灯**。绿灯（0）= 活儿干完自己熄火；黄灯（1）= 机器一开就熄火，多半是配置问题；红灯（137）= 被管理员强断电，Docker 里往往是「内存爆了被系统当机立断杀掉」。所以看到数字别慌，先查它是哪盏灯。

**按顺序排查（四条命令）**：

```bash
# 1. 确认状态：看退出码和运行时长
docker ps -a --filter name=<容器> --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"

# 2. 看具体退出码和是否 OOM
docker inspect --format '{{.State.ExitCode}}' <容器>
docker inspect --format '{{.State.OOMKilled}}' <容器>   # 137 且为 true = 内存被内核杀

# 3. 看它当初是用什么命令启动的（CMD / ENTRYPOINT 对不对）
docker inspect --format 'Cmd={{.Config.Cmd}} Entrypoint={{.Config.Entrypoint}}' <容器>

# 4. 看应用自己的报错
docker logs --tail 100 <容器>
```

如果日志也看不出所以然，最后一步是**覆盖入口、交互式复现**——相当于进到容器里手工把启动命令敲一遍：

```bash
docker run --rm -it --entrypoint sh <镜像>
# 进入容器后手动执行它的启动命令，就能看到真实的报错堆栈
```

**对症下药**：

- **exit 0（自己后台化）**：把进程拉到前台。Nginx 用 `nginx -g "daemon off;"`，Apache 用 `apachectl -D FOREGROUND`。
- **exit 137（OOM）**：提高 `--memory` 内存限制，或降低应用占用；JVM 应用把 `-Xmx` 设为容器上限的约 75%，留出余量。
- **exit 1（启动崩溃）**：用 `--entrypoint sh` 复现启动序列，逐个核对环境变量、密钥挂载、依赖服务是否就绪。

**预防**：在 Dockerfile 里用 **exec 数组形式**写 CMD/ENTRYPOINT（`CMD ["nginx","-g","daemon off;"]`），让应用直接作为 PID 1 运行、正确接收 SIGTERM 优雅退出；shell 形式（`CMD nginx -g "daemon off;"`）会包成 `/bin/sh -c`，信号转发多一层，容易超时被强杀。[Netdata 容器退出排查](https://www.netdata.cloud/guides/docker/docker-container-exits-immediately/)

### 6.2 权限问题：Permission denied

> 症状：容器里的应用写宿主绑定挂载目录时报 `Permission denied`，改了文件权限也没用。

**原因**：绑定挂载按**数字 UID/GID** 匹配，不按用户名。Docker 自动创建的挂载目录属主通常是 `root:root`（755），而容器里的应用若以非 root 用户运行，写进去自然被拒。

> [!tip] 大白话
> 把 UID/GID 想成**员工的工号**。宿主机只认工号不认名字：容器里的应用工号是 1000，想写一个「只允许工号 0（root）进」的文件夹，当然被拒。所以别在容器里改名改权限，要让**工号对上号**。

**四种解法，按场景选一种**：

```bash
# 方案一：运行时指定 UID/GID（docker run 场景）
docker run -u $(id -u):$(id -g) -v $(pwd)/data:/app/data myapp
```

```yaml
# 方案二：Compose 场景，用 user: 键，配合 .env 传值
services:
  app:
    image: myapp
    user: "${UID}:${GID}"
    volumes:
      - ./data:/app/data
# .env 文件里写上：
# UID=1000
# GID=1000
```

```bash
# 方案三：在宿主机上把目录属主改成容器内用户的数字 ID
sudo chown -R 1000:1000 ./data
```

```yaml
# 方案四：LinuxServer.io 系列镜像的约定——PUID / PGID 环境变量，容器内部自动 chown
services:
  app:
    image: lscr.io/linuxserver/readarr
    environment:
      - PUID=1000
      - PGID=1000
```

> [!warning] 高危提示
> 用 `chown -R` 改属主前务必确认目录是「专用的数据目录」；不要对整个项目根目录或系统目录乱改。`PUID`/`PGID` 方案只对 LinuxServer.io 系列镜像生效，普通镜像不一定支持。

更深一层的 UID/GID 映射原理（rootless 模式、`--userns` 等）可以看官方文档 [UID/GID 映射](https://docs.docker.com/engine/security/rootless/uid-gid-mapping/)；如果你已经见过这个概念，可以链接到 [[docker里的GID和UID]] 一起复习。

### 6.3 清理最佳实践

磁盘越来越满？清理要**先预览、再动手、分类型**，别一上来就 `prune` 全家桶。

```bash
# 第一步：先看谁占了多少
docker system df

# 第二步：日常清理——只删 24 小时前的未用镜像（-a 连未使用镜像一起删）
docker system prune -a --filter "until=24h"

# 第三步：按类型精准清理（各删各的）
docker container prune      # 只删已停止的容器
docker image prune -a       # 只删未使用的镜像
docker network prune        # 只删未使用的网络
docker buildx prune         # 只删构建缓存
```

> [!warning] 高危提示
> 卷（volume）**默认不会被自动删除**。官方原话是 "Volumes are never removed automatically, because to do so could destroy data."（绝不自动删卷，因为那可能毁掉数据）。`system prune` 默认不带 `--volumes`；如果你主动加 `--volumes`，等于把数据库数据一起清掉，**删前务必确认这些卷不再需要**。写笔记时也提醒一句：`down -v` 同理，是破坏性操作。

### 6.4 Windows 挂载路径问题

> 症状：Windows 上跑 compose 报 `Invalid volume specification: 'C:\Users\...:/app:rw'`。

**原因**：Compose 把 Windows 路径 `C:\...` 转换后发给 Linux daemon，daemon 解析不了，直接报格式无效。这个在 Docker Desktop 上很少见，多见于 WSL/远程引擎场景。[StackOverflow 讨论](https://stackoverflow.com/questions/79373371/)

**处理**：如果你确实在跑 Windows 容器，设环境变量关掉转换：

```bash
# PowerShell
$env:COMPOSE_CONVERT_WINDOWS_PATHS = "0"
# bash
export COMPOSE_CONVERT_WINDOWS_PATHS=0
```

**v2.35.0+ 的新坑**：Compose 从 v2.35.0 起，bind 源路径不存在时**直接报错** `bind source path does not exist`，不再自动建目录。短语法（`./data:/app/data`）默认隐含 `create_host_path: true` 所以不受影响；但长语法需要显式声明：

```yaml
services:
  app:
    volumes:
      - type: bind
        source: ./data
        target: /app/data
        create_host_path: true   # v2.35+ 显式允许自动创建
```

> [!tip] 大白话
> 把挂载想成**装修前先打通两间房**。新版 Compose 学乖了：你说「把这两间房打通」，它先确认墙对面确实存在，不存在就拒单，而不是像以前那样自己默默拆墙（自动建目录）。所以 Windows 上遇到挂载报错，先检查源目录到底存不存在。

### 6.5 其他高频坑

#### 端口冲突：`port is already allocated`

**症状**：`docker run -p 8080:80` 或 `compose up` 报端口已被占用。

**排查**：先看是哪个容器占的，再看是不是宿主进程占的：

```bash
docker compose ps          # 项目内谁在占这个端口
ss -ltnp | grep :8080      # Linux：宿主进程
netstat -ano | findstr :8080   # Windows
```

找到之后：把容器 `down` 掉、杀掉宿主进程、或者改映射端口。想深入理解容器端口映射与网络模型，可以链接到 [[Docker网络结构详解]] 复习。

#### YAML 校验：`$` 转义与 `version:` 键

**症状**：compose 配置里写了个环境变量 `$VAR`，结果启动后值不见了或报解析错误。

**原因**：Compose 会对 YAML 值里的 `$VAR`/`${VAR}` 做插值，想表达字面 `$` 必须写成 `$$`。另外新版 Compose **已移除 `version:` 键**（弃用），配置里还留着会报警告。

```bash
docker compose config --quiet   # 静默校验：没输出 = 通过，有输出 = 错误
```

```yaml
# 错：想把字面 "$" 传给容器
environment:
  PASSWORD: "$abc123"
# 对：用 $$ 转义
environment:
  PASSWORD: "$$abc123"
```

#### 更新不生效：镜像改了但容器还是旧行为

**症状**：改了 compose.yaml 或重建了镜像，`up` 之后容器行为没变。

**原因**：`up` 会复用已有容器；配置变了、镜像 tag 没变时，它不会自动重建。

**解决**：先 `down` 再 `up`（彻底重建），或直接强制重建：

```bash
docker compose down && docker compose up -d     # 先清理再起
docker compose up -d --force-recreate           # 或强制重建容器
```

### 6.6 一页速查小结

#### 退出码速查表

| 退出码 | 含义 | 第一反应 |
|--------|------|---------|
| 0 | 正常跑完退出 | 进程后台化了，改成前台运行 |
| 1 | 启动崩溃 | 查 `logs`，核对配置/环境变量 |
| 126 | 存在但不可执行 | 查执行权限 |
| 127 | 命令未找到 | 查路径/二进制是否装对 |
| 137 | 被 SIGKILL 强杀 | 查 OOM，加内存或降占用 |

记忆：**退出码 = 128 + 信号编号**。

#### 最常用命令一句话回顾

```bash
docker ps -a                                   # 所有容器（含已停止）
docker logs --tail 100 <容器>                   # 看报错
docker inspect --format '{{.State.ExitCode}}' <容器>   # 看退出码
docker run --rm -it --entrypoint sh <镜像>      # 进容器手动复现
docker system df                                # 清理前先看占用
docker system prune -a --filter "until=24h"     # 日常安全清理
docker compose config --quiet                   # 校验配置
docker compose up -d --force-recreate           # 强制重建生效
docker compose down                             # 停并删容器（保留数据卷）
```

### 本章小结

- **启动即退出**：先看退出码定性（0 后台化 / 1 崩溃 / 126 不可执行 / 127 找不到 / 137 OOM），再按 `ps -a` → `inspect` → `logs` → `--entrypoint sh` 顺序排查。
- **权限问题**：绑定挂载按数字 UID/GID 匹配；`-u`、`user:`、`chown`、`PUID/PGID` 四选一让「工号对上号」。
- **清理三连**：`system df` 预览 → `prune -a --filter "until=24h"` → 单类型 `prune`；卷默认不自动删，加 `--volumes` 是破坏性操作。
- **Windows 路径**：`Invalid volume specification` 用 `COMPOSE_CONVERT_WINDOWS_PATHS=0` 处理；v2.35+ 源路径不存在会直接报错。
- **其他高频坑**：端口冲突用 `ss`/`netstat` 定位、`$` 写 `$$`、去掉 `version:` 键、更新不生效就 `down` 再 `up`。

到这里，六章全部写完——从「镜像 vs 容器」的心智模型，到命令速查、Compose 编排、配置语法，再到本章的排错手册。建议把这篇笔记当作**随身速查表**：平时不用背，等遇到「启动即退出」或「Permission denied」，翻到对应小节对号入座即可。祝你的容器从此不再说退就退。

---

## 参考资源

- [Docker 官方文档 - Get Started](https://docs.docker.com/get-started/)：镜像与容器核心概念入门。
- [Docker CLI 参考](https://docs.docker.com/reference/)：所有 `docker` 命令的完整参考。
- [Docker Compose 应用模型](https://docs.docker.com/compose/compose-application-model/)：Compose 如何描述并编排多服务应用。
- [v1 → v2 迁移文档](https://docs.docker.com/compose/migrate/)：`docker-compose` 到 `docker compose` 的迁移说明与行为差异。
- [Docker Compose CLI 参考](https://docs.docker.com/reference/cli/docker/compose/)：所有 `docker compose` 命令的完整参考。
- [Compose 文件语法参考](https://docs.docker.com/reference/compose-file/)：`compose.yaml` 各字段详解。
- [Netdata - Docker 容器启动即退出排查](https://www.netdata.cloud/guides/docker/docker-container-exits-immediately/)：退出码排错实战指南。
- [Docker 官方 - UID/GID 映射](https://docs.docker.com/engine/security/rootless/uid-gid-mapping/)：rootless 模式下 UID/GID 映射原理。
