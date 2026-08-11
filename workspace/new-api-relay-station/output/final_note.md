---
title: 搭建并学会使用 AI API 中转站（new-api）
tags: [AI, 中转站, new-api, Docker, 实战笔记]
created: 2026-08-12
updated: 2026-08-12
status: draft
source_project: new-api-relay-station
---

# 搭建并学会使用 AI API 中转站（new-api）

## 笔记总览

> [!abstract] 笔记简介
> 这是一份面向**零基础读者**的实战笔记，目标是从零搭建并学会使用 AI API 中转站（new-api）。笔记主线是「概念 → 部署 → 初始化与安全 → 渠道配置 → 令牌与客户端接入 → 避坑运维 → 总结与进阶」，全程手把手、可照做。

- **目标读者**：零基础（未搭过 Web 服务、未用过 Docker，从环境准备讲起）
- **学完能做什么**：
  - 独立从零部署一个可用的 new-api 中转站（单容器自用或 Compose 生产版）
  - 完成初始化、安全加固，并配置 HTTPS 反向代理
  - 正确配置多个上游渠道、多 Key 池与自动禁用兜底
  - 创建并管理令牌（额度、模型白名单、分组、IP 白名单）
  - 把中转站接入 NextChat / Cherry Studio / ChatBox / LobeChat / Claude Code 等客户端
  - 独立排查「无可用渠道」「额度不足」「模型不匹配」等高频问题，并完成备份与升级
- **前置要求**：一台 64 位 Linux 服务器（内存 1 GB+，磁盘 10 GB+）、一个上游 AI 服务商的 API Key；Docker、Linux 命令都会在笔记内手把手讲解

## 目录

1. [第一章：认识中转站与 new-api](#第一章认识中转站与-new-api)
2. [第二章：环境准备与 Docker 部署](#第二章环境准备与-docker-部署)
3. [第三章：首次初始化与安全加固](#第三章首次初始化与安全加固)
4. [第四章：渠道配置](#第四章渠道配置)
5. [第五章：令牌管理与客户端接入](#第五章令牌管理与客户端接入)
6. [第六章：常见坑与运维](#第六章常见坑与运维)
7. [第七章：总结与进阶](#第七章总结与进阶)

---

## 第一章：认识中转站与 new-api

> 本章回答一个最基础的问题：**AI API 中转站到底是什么，为什么我需要它？** 我们先用生活化的方式讲清「中转站」这个角色，再介绍本笔记的主角 new-api，最后把后面六章要做的所有事提前看一遍，让你对整条学习路径心里有数。本章零基础可读，不需要任何前置知识。

### 1.1 什么是 AI API 中转站

先放下技术名词，用一个生活场景来想。

> [!tip] 大白话：中转站像「快递驿站」
> 把各家 AI 模型厂商想成不同的快递公司，你买的包裹（AI 能力）被它们分别送到各家网点。中转站就是小区门口的快递驿站——**各家快递统一送到驿站，你只需要去一个地方取件**。所以对你来说，不管包裹原本是哪家快递送的，取件地址永远只有一个。

技术上的定义也完全对应这句话：**中转站是一个「聚合多上游模型、统一对外提供 OpenAI 兼容 API」的网关服务**[new-api 官方仓库](https://github.com/QuantumNous/new-api)。它把 DeepSeek、OpenAI、Kimi 等多家服务商聚合到一处，对外只暴露一套统一接口。

那它解决了什么实际问题？想想如果没有中转站，你要在多个 AI 客户端之间切换多个模型时，得面对这些麻烦：

- 每个服务商的 Key、接口地址各不相同，要记好几套配置；
- 各家计费规则、额度管理分散，查账要到处登录；
- 某个上游模型想换成另一家时，要改一堆客户端配置。

中转站把这些统一收口：**客户端只认一个地址、一个 Key，上游换了哪家供应商对你完全透明**。这正是「中转」二字的含义——它挡在你和各家 AI 厂商之间，帮你把复杂度吃掉。

### 1.2 new-api 是什么：与 one-api 的关系

new-api 就是一个开源的、社区活跃维护的中转站项目，代码托管在 GitHub 的 `QuantumNous/new-api` 仓库，配套有官方文档站 docs.newapi.pro[官方文档站](https://docs.newapi.pro/)。它能做的正是 1.1 描述的事：多渠道聚合、统一鉴权、额度管理与日志分发。

你可能听说过它有个「前辈」叫 one-api。两者关系可以用一句话概括：**new-api 是社区在 one-api 基础上延续和发展的活跃分支，界面与用法高度接近，但更新节奏更快、周边生态更完整**。对零基础的你来说，不需要先去学 one-api——直接学 new-api 即可，后面所有操作都只围绕 new-api 这一个项目展开。

### 1.3 核心概念速览：渠道、令牌、模型映射、分组、额度、限流

后面每一章都会反复用到下面六个词。先混个脸熟，不必现在全懂，遇到时再回来查这张表即可。

| 术语 | 一句话解释 |
|------|-----------|
| 渠道（Channel） | 对接一个上游服务商的最小配置单元，封装了上游的 Key、接口地址、可服务模型、分组等 |
| 令牌（Token） | 分发给客户端使用的认证凭证，格式 `sk-{base_key}`，采用 OpenAI 兼容鉴权 |
| 模型映射（ModelMapping） | 把「入站模型名」改写成「上游实际模型名」的映射规则 |
| 分组（Group） | 用户 / 令牌 / 渠道共有的路由隔离维度，默认是 `default` |
| 额度（Quota） | 计费点数，1 美元 = 500,000 配额点数；账户余额是扣费来源，令牌额度是子限制 |
| 限流（Rate Limit） | 控制单位时间内的调用频率，避免把上游接口打到 429 限流 |

下面挑最关键的几个，用大白话再讲一遍。

> [!tip] 大白话：渠道像「超市的供应商」
> 每个渠道就是一家供货商——从哪家进货、进的是什么货（哪些模型）、进价多少都由它决定。**所以「这个模型能不能用」先看有没有渠道在供这个货**，渠道没配，客户端就会报「无可用渠道」。

> [!tip] 大白话：令牌像「临时工牌」
> 令牌就是一张临时工牌，客户端出示它才能刷开 AI 服务的大门；工牌上还写着你能进哪几个房间（模型白名单）、最多能花多少钱（令牌额度）。**所以中转站认牌不认人，Key 丢了等于工牌丢了，要立刻作废重发**。

> [!tip] 大白话：额度像「话费余额」
> 账户余额是你的总话费，令牌额度是这张卡当月的消费封顶，两个都要有才能正常打电话。**所以提示「额度不足」时，先查令牌额度，再查账户余额**，两个位置都看一遍才不漏判。

> [!tip] 大白话：分组像「公司门禁」
> 公司分了很多部门，门禁卡只能进自己部门那层楼。**令牌在哪个组，就只能用哪个组绑定的渠道**；组对不上，同样会「无可用渠道」。

### 1.4 从零到一的全流程预览

学完这套笔记，你能独立完成这样一条链路：部署 → 初始化 → 配置渠道 → 创建令牌 → 接入客户端 → 日常运维。下表把后面六章要解决的问题提前列出来，也是本笔记的路线图。

| 后续章节 | 这一步解决什么 | 对应章节 |
|----------|----------------|----------|
| 第 2 章 | 准备一台 64 位 Linux 服务器，装好 Docker，把中转站跑起来 | 环境准备与 Docker 部署 |
| 第 3 章 | 首次访问初始化向导，创建管理员账号、选择使用模式，并做安全加固 | 首次初始化与安全加固 |
| 第 4 章 | 添加第一个上游渠道，让中转站真正「有货可发」 | 渠道配置 |
| 第 5 章 | 创建令牌，把中转站接入你的 AI 客户端，开始日常使用 | 令牌管理与客户端接入 |
| 第 6 章 | 处理高频报错、数据备份、版本升级等日常运维 | 常见坑与运维 |
| 第 7 章 | 回顾完整流程，给出进阶方向与权威资料清单 | 总结与进阶 |

动手之前先确认基础条件：需要一台 **64 位 Linux 服务器**（Ubuntu / CentOS / Debian 均可，自用场景内存 1 GB 起、磁盘建议 10 GB 以上），并安装 **Docker 与 Docker Compose**——这些都会在第 2 章手把手讲解，零基础不需要提前准备[官方部署：Docker 文档](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-compose-installation)。

### 本章小结

- **中转站**是把多家 AI 上游聚合起来、对外只暴露一套 OpenAI 兼容接口的网关，帮你省去多套 Key 和地址的管理成本。
- **new-api** 是社区活跃维护的开源中转站项目，延续自 one-api，你只需直接学习它即可。
- 六个核心概念——**渠道、令牌、模型映射、分组、额度、限流**——是后面所有章节的通用词汇，理解它们的角色比死记定义更重要。
- 完整学习路径是「**部署 → 初始化 → 渠道 → 令牌 → 接入 → 运维**」六步，对应第 2 到第 7 章。

下一章我们开始动手：准备环境并安装 Docker，用最简单的方式把 new-api 在服务器上跑起来。

---

## 第二章：环境准备与 Docker 部署

> 第一章我们把「中转站是什么」讲清楚了，这一章开始动手：准备一台 64 位 Linux 服务器、装好 Docker，用两种方式把 new-api 跑起来——先讲单容器快速部署（个人自用够用），再讲 Docker Compose 完整版（生产推荐），最后教你怎么验证部署成功。全程零基础可跟做，每个命令都可以直接复制。

### 2.1 前置要求与部署方式选型

动手之前，先确认服务器满足下面三条底线[new-api 官方部署文档](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-compose-installation)：

| 项目 | 最低要求 | 说明 |
|------|----------|------|
| 操作系统 | **64 位 Linux**（Ubuntu / CentOS / Debian 均可） | **不支持 32 位**，装之前先确认系统架构 |
| 内存 | 单容器约 1 GB；完整版建议 2 GB+ | 数据库换 PostgreSQL/Redis 后吃内存更多 |
| 磁盘 | 建议 10 GB+ | 镜像 + `/data` 数据 + 日志都会占空间 |

先花一分钟自查服务器是否满足条件，把下面三条命令各执行一遍：

```bash
uname -m     # 输出 x86_64 或 aarch64 就是 64 位；输出 i386/i686 就不行
free -h      # 看内存大小（Mem 那一行），自用 1G+，完整版 2G+
df -h /      # 看磁盘剩余空间，建议 10G+
```

如果你手里只有 Windows 或 Mac 电脑，也别急：去阿里云 / 腾讯云等平台买一台按量付费的轻量云服务器（选 Ubuntu 系统即可），或者在本机用虚拟机装一个 Ubuntu——本笔记的操作在云服务器上完全一致，教程里的 IP 换成你服务器的公网 IP 就行。

> [!tip] 大白话：Docker 像「集装箱」
> 把 Docker 想成码头上的集装箱——每个软件被打包成一个标准尺寸的箱子（镜像），里面有它运行需要的所有零件；`docker run` 就是开箱启动一个运行中的实例（容器）。**所以同一份镜像能开出无数个互不影响的容器，装软件不再需要自己逐个配依赖**，这也是中转站部署如此简单的原因。

部署方式怎么选？new-api 官方提供两条路线[官方 Docker 单容器文档](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-installation)：

- **单容器（SQLite）**：只有 new-api 一个容器，数据库用自带的 SQLite 文件。适合**个人自用**，简单、省资源。
- **Docker Compose 完整版（PostgreSQL + Redis）**：把 new-api、数据库、缓存三个容器一起编排。适合**生产 / 对外服务**，性能和稳定性更好，官方更推荐。

一句话决策：**自己用选单容器，要对外提供服务选 Compose 完整版**。下面两种都会讲，你可以先按单容器跑通，再升级到完整版。

### 2.2 安装 Docker 与 Docker Compose

以 Ubuntu 为例，官方提供了一键安装脚本[官方 Docker 安装脚本](https://get.docker.com)，把下面三行依次执行：

> 如果你在国内网络环境下安装 Docker 遇到困难，可参考 [[docker/Linux-Docker与DockerCompose安装指南-国内网络版]]。

```bash
# 1. 用官方脚本安装 Docker 和 Docker Compose（会自动装最新版）
curl -fsSL https://get.docker.com | sudo sh

# 2. 设置 Docker 开机自启，并立即启动
sudo systemctl enable --now docker

# 3. 验证安装成功：两条命令都应有版本号输出
docker --version && docker compose version
```

能看到类似 `Docker version 27.x.x` 和 `Docker Compose version v2.x.x` 的输出，就说明装好了。

> [!warning] 易错点：`docker-compose`（横杠）和 `docker compose`（空格）是两代人
> 老教程里到处是 `docker-compose up`，那是旧版命令；新版把 compose 合并进了 Docker，命令变成 `docker compose up`（中间是空格）。**照抄旧教程报 `docker: 'compose' is not found`，就说明缺 compose 插件**，执行 `sudo apt install docker-compose-plugin` 补上即可。本笔记统一用新命令。

### 2.3 单容器快速部署（自用 SQLite）

在服务器上新建一个专门放数据的目录，然后执行下面这条命令：

```bash
# 建议先建个工作目录再执行，这样 ./data 会落在里面
mkdir -p ~/new-api && cd ~/new-api

docker run --name new-api -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v ./data:/data \
  calciumion/new-api:latest
```

逐段看这条命令在做什么：

| 参数 | 含义 |
|------|------|
| `--name new-api` | 给容器起名，后续管理用 |
| `-d` | 后台运行（detached） |
| `--restart always` | 服务器重启 / 容器崩溃后自动拉起 |
| `-p 3000:3000` | 端口映射：见下方易错点 |
| `-e TZ=Asia/Shanghai` | 设置时区为上海 |
| `-v ./data:/data` | 数据卷挂载：见下方易错点 |
| `calciumion/new-api:latest` | 官方镜像名和版本标签 |

第一次运行会自动从镜像仓库拉取镜像，根据网速可能要等一两分钟，属正常现象。启动完成后用下面这条命令确认容器在跑：

```bash
docker ps     # 能看到名为 new-api 的容器、STATUS 为 Up，就是成功了
```

启动后浏览器访问 `http://服务器IP:3000`，能看到 new-api 页面就成功了（具体初始化操作在第 3 章）。

> [!warning] 易错点：`-v ./data:/data` 必须挂载
> 容器本身是一次性的，**不挂载数据卷，容器一删数据就全没了**。把 `./data:/data` 想成一个外接硬盘：左边是服务器上的真实目录（`./data`），右边是容器内部放数据的位置（`/data`）。升级、重建容器时必须带上这条挂载，数据才保得住[官方 FAQ](https://docs.newapi.pro/zh/docs/support/faq)。

> [!warning] 易错点：端口映射「左宿主、右容器」
> `-p 3000:3000` 的**左边**是宿主机（服务器对外）的端口，**右边**是容器内部固定的端口。改对外端口只动左边，例如 `-p 3480:3000` 就是访问 `http://IP:3480`；右边的 `3000` 是 new-api 自己的端口，一般不要动。

### 2.4 Docker Compose 完整版（生产推荐）

Compose 的用法是：把多个容器要用的「菜谱」写进一个 `docker-compose.yml` 文件，然后一条命令全部启动。先创建文件：

```bash
mkdir -p ~/new-api && cd ~/new-api
# 用编辑器创建 docker-compose.yml，内容如下
```

> [!tip] 大白话：docker-compose.yml 像「点菜单」
> 单容器像一个菜，Compose 像一张点菜单——上面写清楚要哪几个菜（new-api、Postgres、Redis）、各用什么锅（镜像）、摆在哪个桌（端口）、调料怎么放（环境变量）。**服务员照着菜单一次全部端上来，而不是你一个个去催**，这就是 `docker compose up -d` 做的事。

完整配置如下（直接复制即可，记得把 `SESSION_SECRET` 换成你自己的随机串）[官方 compose 配置详解](https://docs.newapi.pro/zh/docs/installation/config-maintenance/docker-compose-yml)：

```yaml
version: '3.4'                    # 新版 Compose 可省略此行，留着兼容老版本

services:
  new-api:
    image: calciumion/new-api:latest
    container_name: new-api
    restart: always
    command: --log-dir /app/logs  # 日志写到独立目录
    ports:
      - '3000:3000'               # 左宿主机端口 : 右容器端口
    volumes:
      - ./data:/data              # 数据卷，必须保留
      - ./logs:/app/logs          # 日志目录也挂出来方便查看
    environment:
      - SQL_DSN=postgresql://root:123456@postgres:5432/new-api   # 数据库连接串
      - REDIS_CONN_STRING=redis://redis                           # Redis 连接串
      - TZ=Asia/Shanghai
      - ERROR_LOG_ENABLED=true
      - BATCH_UPDATE_ENABLED=true
      - SESSION_SECRET=你的随机串                                  # 换成 openssl rand -hex 16 生成的串
    depends_on:                   # 先启动依赖，再启动 new-api
      - redis
      - postgres
    healthcheck:                  # 定时探活，页面显示 healthy
      test: ["CMD-SHELL", "wget -q -O - http://localhost:3000/api/status | grep -o '\"success\":\\s*true' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:latest
    container_name: redis
    restart: always

  postgres:
    image: postgres:15
    container_name: postgres
    restart: always
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123456   # 生产环境请改成强密码
      POSTGRES_DB: new-api
    volumes:
      - pg_data:/var/lib/postgresql/data   # 数据库数据用命名卷持久化

volumes:
  pg_data:                        # 声明命名卷
```

在 `docker-compose.yml` 所在目录执行：

```bash
docker compose up -d
```

它会自动拉取三个镜像并后台启动。同样访问 `http://服务器IP:3000` 即可。

> [!note] 三个容器分别干嘛？
> `postgres` 是数据库，负责存渠道、令牌、额度等业务数据；`redis` 是缓存，用于额度预扣、限流等高频操作；`new-api` 是主程序，所有请求都先进它。把它们拆开部署，正是「完整版」比单容器更稳的原因。

### 2.5 常用管理命令与部署验证

启动之后，最常用的几条管理命令如下（都要在 `docker-compose.yml` 所在目录执行）[官方 compose 部署文档](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-compose-installation)；更完整的命令速查可看 [[docker/Docker与DockerCompose命令速查]]：

```bash
docker compose ps                # 查看所有服务状态（UP / healthy）
docker compose logs -f           # 跟踪所有服务日志（Ctrl+C 退出）
docker compose logs --tail=100 new-api   # 只看 new-api 最近 100 行日志
docker compose restart           # 修改配置后重启服务（不删数据）
docker compose down              # 停止服务，但保留数据卷
docker compose down -v           # ⚠️ 慎用：连数据卷一起删除，数据不可恢复
```

单容器模式的对应命令：`docker ps` 看状态、`docker logs -f new-api` 看日志、`docker stop new-api` 停止、`docker rm new-api` 删除容器。

最后做一次部署验证。用 `curl` 请求健康检查接口，期望返回 `"success": true`[官方验证方法](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-compose-installation)：

```bash
curl -s http://localhost:3000/api/status
# 期望输出类似：{"success":true,"message":"","data":...}
```

同时用 `docker compose ps` 确认 `new-api` 状态为 `Up` 且健康：

```bash
docker compose ps
# 期望输出：new-api 容器状态 Up (healthy)，redis / postgres 也为 Up
```

两步都通过，说明中转站已经稳定运行，可以进入第 3 章的初始化了。

> [!warning] 易错点：`docker compose down -v` 千万别随手敲
> `down` 是「收摊」，`-v` 是「把货也一起扔掉」——它会把数据库数据卷一并删掉，**删了无法找回**。日常停止服务只敲 `docker compose down`，只有在确定要清空重来时才带 `-v`。

### 本章小结

- 前置三底线：**64 位 Linux、内存 1 GB+（完整版 2 GB+）、磁盘 10 GB+**；选型上**自用选单容器 SQLite，对外选 Compose 完整版**。
- Docker 安装用官方一行脚本：`curl -fsSL https://get.docker.com | sudo sh`，之后用 `docker --version && docker compose version` 验证。
- 单容器命令的**两个必记点**：`-v ./data:/data` 必须挂载（否则丢数据）；端口映射**左宿主机、右容器**。
- Compose 完整版把 new-api + PostgreSQL + Redis 三个容器一起编排，`docker compose up -d` 一键启动，生产更稳。
- 验证部署：`docker compose ps` 看健康状态，`curl -s http://localhost:3000/api/status` 应返回 `"success": true`。
- 日常管理就记四条：`ps` 看状态、`logs -f` 看日志、`down` 停止、**`down -v` 慎用**。

下一章，我们打开浏览器完成第一次初始化：创建管理员账号、选择使用模式，并顺手做一遍安全加固——这些做完，你的中转站才算真正「上线」。

---

## 第三章：首次初始化与安全加固

> 上一章我们完成了 Docker 部署，但此刻的 new-api 还只是一间「毛坯房」——没有管理员、大门敞开、没有门锁。本章带你完成第一次初始化：创建管理员账号、选对使用模式，确认部署确实没问题；然后照着安全加固清单把门锁好；最后用 Nginx 或 Caddy 挂上 HTTPS，让中转站以安全、加密的方式对外提供访问。零基础可读，全程跟着点即可。

### 3.1 初始化向导：管理员账号与使用模式

在服务器启动 new-api 后，浏览器访问 `http://服务器IP:3000`，会自动跳转到初始化页。第一步是**设置管理员账号 + 密码**——这个账号就是你日后登录管理后台的最高权限账户。

> [!warning] 易错点：官方没有内置默认账号
> 网上常流传「root / 123456」能直接登录，但**因版本而异，不要指望它**。首次访问必须自己创建管理员账号，否则无法进入系统。

第二步是**选择使用模式**，这一步直接决定后面要不要给模型定价[官方部署：Docker Compose 文档](https://docs.newapi.pro/en/docs/installation/deployment-methods/docker-compose-installation)：

- **自用模式**：个人自己用，**不需要给模型定价**，适合大多数自建场景，推荐。
- **对外服务模式**（默认）：需要**为每个模型设置价格**，否则模型不可用——这是最常见的翻车点。
- **演示站点模式**：用来熟悉操作、体验界面，不承担真实流量。

> [!tip] 大白话：对外服务模式像「开店必须贴价签」
> 把中转站想成一家小卖部。自用模式是自家冰箱——拿东西不用付钱；对外服务模式是开门营业——**每件商品必须有价签**，没标价的商品系统不让你卖。所以选了对外服务模式却忘了配价格，客户端就会报「模型不可用」。

### 3.2 验证部署是否成功

初始化完成并登录后，先确认服务确实正常，再往下做安全加固。验证三件套：

```bash
curl -s http://localhost:3000/api/status
# 期望返回内容包含 "success": true

docker compose ps
# Compose 部署：new-api 状态应为 healthy（或 running）
# 单容器部署改用：docker ps | grep new-api
```

再用日志看一眼有没有异常报错：

```bash
docker compose logs --tail=50 new-api
```

看到日志里没有红色 ERROR、`/api/status` 返回成功，就说明部署没问题，可以进入安全加固。

### 3.3 安全加固清单（零基础版）

部署完不等于安全，new-api 默认是「能跑但没设防」的状态。按下面四步把门锁好[官方 compose 配置详解](https://docs.newapi.pro/zh/docs/installation/config-maintenance/docker-compose-yml)：

1. **立即改管理员密码 + 改用户名**：默认的 root / admin 极易被脚本爆破，登录后第一件事就改。
2. **关闭开放注册**：系统设置 → 允许注册 = 关闭，防止陌生人注册你的中转站白嫖额度。
3. **设置固定的 `SESSION_SECRET`**：见下方。
4. **不要直接把 3000 端口暴露到公网**：用下一节的 Nginx / Caddy 反代加 HTTPS。

设置 `SESSION_SECRET` 分两步。先生成一个足够随机的串：

```bash
openssl rand -hex 16
# 输出类似：a1b2c3d4e5f6789012345678abcdef01
```

再把这个随机串写进 compose 文件的环境变量：

```yaml
environment:
  - SESSION_SECRET=你的随机串
```

> [!warning] 易错点：不设 SESSION_SECRET，每次重启全员掉登录
> 不固定它，容器每次重启都会生成一个新密钥，等于把所有人的登录凭证全部作废，已登录用户全部被迫重新登录一次。

> [!tip] 大白话：SESSION_SECRET 像「公司印章」
> 它用来给登录凭证盖章。固定成随机值，等于把印章固定下来；不固定，每次重启就换一枚新章——**旧章盖过的凭证全部失效，全员只能重新登录**。

### 3.4 用 Nginx / Caddy 挂上 HTTPS

直接让用户访问 `http://IP:3000` 既没有加密，也容易暴露管理后台。用 Nginx 反向代理最常见，注意其中「关缓冲」那几行不能省：

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;
    ssl_certificate     /etc/nginx/ssl/api.example.com.pem;
    ssl_certificate_key /etc/nginx/ssl/api.example.com.key;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;

        proxy_connect_timeout 600s;
        proxy_read_timeout    600s;
        proxy_send_timeout    600s;
        client_max_body_size  64m;
    }
}
```

> [!warning] 易错点：反代一定要关缓冲（SSE 流式）
> `proxy_buffering off` 不能省。AI 对话是 SSE 流式输出，开着缓冲会攒满一整段才吐给客户端，表现就是「半天不出字，一出出一整屏」。

如果不想折腾证书，Caddy 会自动申请并续期 HTTPS 证书，一行配置就够[new-api 官方仓库](https://github.com/QuantumNous/new-api)：

```caddyfile
api.example.com {
    reverse_proxy 127.0.0.1:3000
}
```

### 本章小结

- 首次访问 `http://IP:3000` 会进入**初始化向导**：创建管理员账号 + 选择使用模式。
- **对外服务模式必须给模型定价否则不可用**；个人自用直接选「自用模式」，省掉定价的坑。
- 验证部署三件套：`/api/status` 返回 success、`docker compose ps` 健康、`docker compose logs` 无 ERROR。
- 安全加固四步：改密改用户名、关闭开放注册、固定 `SESSION_SECRET`、用反代别裸奔。
- HTTPS 反代**必须关缓冲**，否则 SSE 流式输出会卡成「憋大招」。

下一章进入中转站的核心操作：配置第一个上游渠道，让 new-api 真正「有货可发」——这一步做完，客户端才第一次能调通模型。

---

## 第四章：渠道配置

> 本章回答：**中转站已经跑起来了，怎么让它真正「有货可发」？** 答案是配置渠道。我们先把渠道的每个字段用大白话讲清楚，再带你添加第一个渠道（OpenAI 和 DeepSeek 两个示例），接着讲多 Key 池与负载均衡、排查「无可用渠道」的三大根因，最后教你测试渠道。读完这章，你的中转站就有了第一个真正能用的上游。

### 4.1 渠道是什么：字段逐个讲

第一章里我们把渠道比作「超市的供应商」。new-api 里，渠道（Channel）就是**对接一个上游服务商的最小配置单元**，它把「从哪家进货、进什么货、按什么规则发货」封装成一张配置卡片[官方渠道管理](https://docs.newapi.pro/zh/docs/guide/feature-guide/admin/channel)。下面这张表是添加渠道时最常见的 10 个字段，我标出了每个字段最常踩的坑。

| 字段 | 作用 | 易错点 |
|------|------|--------|
| Type | 选上游服务商的通信协议，决定中转站怎么跟对方「说话」 | **没有专属选项时选 OpenAI**；选错类型无法通信 |
| Name | 给渠道起个名字，方便你自己识别 | 建议写成「厂商-用途」，如 `OpenAI-主` |
| Key | 上游发给你的 API Key，向上游证明身份 | 格式因服务商而异；支持放多个 Key（见 4.3） |
| BaseURL | 上游接口地址，覆盖内置默认值 | **不要带结尾 `/v1` 或 `/`** |
| Models | 这个渠道能服务哪些模型（多选） | **漏勾 = 该模型「无可用渠道」** |
| Group | 这个渠道给哪个用户组用，默认 `default` | **与令牌/用户组对不上会「无可用渠道」** |
| Priority | 优先级，数字越大越先被选中 | 高优渠道失败会自动降级到低优 |
| Weight | 同优先级下的加权随机权重 | 权重为 0 也可能被选中，不是 0 就完全不用 |
| ModelMapping | 把「入站模型名」改写为「上游模型名」（JSON） | 是单向改写，**不会让模型凭空「存在」** |
| AutoBan | 连续出错时自动禁用渠道（状态 3） | 建议开启，作为失败兜底 |

字段太多记不住？先抓最要命的两个。

> [!tip] 大白话：Type 像「说哪种方言」
> 不同厂商说话的「方言」不一样——OpenAI 兼容协议、Anthropic 协议、各家私有协议各不相同。Type 就是让中转站挑一种方言去跟上游对话。**所以没找到专属选项时，选 OpenAI 最稳**，因为绝大多数服务商都兼容 OpenAI 的说话方式。

> [!tip] 大白话：BaseURL 像「收货地址」
> BaseURL 是告诉中转站去哪个「仓库」取货的地址。很多服务的默认地址已经写好了 `/v1`，**你再补一个 `/v1`，等于把门牌写成「/v1/v1」**，就会敲错门、拿到一页网页而不是数据。

### 4.2 添加第一个渠道：OpenAI 与 DeepSeek 示例

操作步骤只有五步：登录后台 → 顶部菜单「渠道」→「添加渠道」→ 按下面示例填写 → 点「提交」，回列表点「测试」验证。

下面的配置示例可以直接照抄，把 Key 换成你自己的即可（文本形式，面板里逐项对应填入）：

```text
# 示例一：OpenAI 官方渠道
Type:       OpenAI
Name:       OpenAI-主
Key:        sk-你的OpenAI密钥
BaseURL:    留空（官方地址已内置，不用填）
Models:     gpt-4o, gpt-4o-mini
Group:      default
Priority:   10
Weight:     100
AutoBan:    开启
```

```text
# 示例二：DeepSeek 渠道
Type:       DeepSeek          # 面板里有 DeepSeek 就选它；没有就选 OpenAI
Name:       DeepSeek-主
Key:        sk-你的DeepSeek密钥
BaseURL:    https://api.deepseek.com   # 注意：结尾不要写成 /v1
Models:     deepseek-chat, deepseek-reasoner
Group:      default
Priority:   10
Weight:     100
AutoBan:    开启
```

两点提醒：

- **Models 一定要勾**。面板里通常是一个可勾选的模型列表，很多人填完 Key 就提交，结果模型一个都没勾——这是「无可用渠道」的头号来源。
- **BaseURL 只对非常规服务商才必须填**。OpenAI、DeepSeek 这类标准服务商官方地址已内置，留空即可；要填时务必核对结尾，不带 `/v1`。

### 4.3 多 Key 池与负载均衡

一个渠道可以放**多个上游 Key**，new-api 会在这些 Key 之间轮询分发，单个 Key 失败自动跳过，恢复后自动重新启用。填入方式两种，任选其一[官方渠道管理](https://docs.newapi.pro/zh/docs/guide/feature-guide/admin/channel)：

```text
# 方式一：换行分隔，一个 Key 一行
sk-key-1111
sk-key-2222
sk-key-3333

# 方式二：JSON 数组
["sk-key-1111", "sk-key-2222", "sk-key-3333"]
```

> [!tip] 大白话：多 Key 池像「多部电梯」
> 一个 Key 只有一部电梯，人多就挤、坏了就全楼瘫痪。多 Key 池就是多装几部电梯，中转站轮流调度、**一部电梯坏了（Key 失效）不影响其他电梯继续跑**。

### 4.4 「无可用渠道」三大根因

报「无可用渠道」或 `model_not_found`，九成是下面三类原因之一，按表逐个排查：

| 根因 | 排查点 | 解决办法 |
|------|--------|----------|
| 1. 模型列表没对上 | 请求的模型名在不在渠道 Models 里？ | 补勾模型，**模型名必须与请求完全一致** |
| 2. 分组没对上 | 令牌/用户所在组，在不在渠道 Group 列表里？ | 让两边分组一致，或把令牌组设 `auto` |
| 3. 渠道被禁用 | 渠道状态是不是 2（手动禁用）或 3（自动禁用）？ | 去渠道列表启用，或先处理自动禁用原因 |

其中第 2 条有个省心技巧：**把令牌的组设为 `auto`**，new-api 会自动遍历该用户所有授权组去找可用渠道，不用你手动对齐分组[官方令牌管理](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)。

> [!tip] 大白话：auto 组像「万能门禁卡」
> 普通门禁卡只能进一个部门，`auto` 是一张万能卡——能刷开你名下所有授权部门的门。**所以拿不准该走哪个组时，用 auto 最省心**；代价是可用渠道范围会扩大，对外服务时要权衡。

### 4.5 测试渠道与常见报错

渠道列表每一行都有「测试」按钮（单测），列表页顶部有「测试所有渠道」（批测）。测试的本质是拿当前渠道向上游发一个最小请求，返回成功就说明这条链路通了。

高频报错 `invalid character '<'` 的含义：**上游返回的是 HTML 网页，而不是 JSON 数据**。常见原因是 BaseURL 指错（比如多带了 `/v1`），或上游被 CDN / 反向代理拦截返回了错误页面。排查顺序：先核对 BaseURL，再换个出口 IP 重测。

> [!tip] 大白话：invalid character '<' 像「敲门敲到保安亭」
> 你以为在敲仓库大门，结果敲到了保安亭，保安递给你一张纸条（HTML 网页），而不是你要的货（JSON 数据）。**所以看到以 `<` 开头的报错，先怀疑地址敲错了**。

### 本章小结

- 渠道是「进货」的最小单元，10 个字段决定从哪进、进什么、怎么发；**先记牢 Type、Key、BaseURL、Models、Group 这五个**。
- 添加渠道的关键动作：**选对 Type（无专属就选 OpenAI）、BaseURL 别带 /v1、Models 一定要勾**。
- 多 Key 池用「换行」或「JSON 数组」填入，Key 失败自动跳过，显著提升可用性。
- 「无可用渠道」三大根因：**模型没勾、分组对不上、渠道被禁用**；拿不准分组就用 `auto`。
- 测试渠道是最后一道防线，`invalid character '<'` = 上游回了网页而不是 JSON，先查 BaseURL。

下一章我们创建令牌，把中转站接入你自己的 AI 客户端，真正开始日常使用。

---

## 第五章：令牌管理与客户端接入

> 本章解决的是整条链路里的「最后一公里」：**如何把中转站里已经配好的模型能力，变成你自己客户端里真正能用的对话**。我们先讲透令牌这个概念（格式、状态、额度），再手把手创建第一个令牌，接着把额度计算规则一次讲清，最后接入主流客户端并跑通连接测试。学完这章，你就能在 NextChat、Cherry Studio 等客户端里调用自己的模型了。

### 5.1 令牌：格式、状态与额度

第四章我们把上游渠道配好了，相当于中转站「有货可发」。但货发给谁？怎么证明「你」有权限拿？答案就是令牌（Token）。

> [!tip] 大白话：令牌像「临时工牌」
> 第一章里我们把令牌比作临时工牌：客户端出示它，中转站才认你。工牌上写着你最多能花多少钱（令牌额度）、能进哪几个房间（模型白名单）。**中转站认牌不认人，工牌号只在办卡那一刻完整显示一次**。

令牌的格式是 `sk-{base_key}[-{channel_id}]`[new-api 官方令牌管理](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)：
- `sk-` 开头，后面跟一长串随机字符（base_key）；
- 末尾可选的 `-{channel_id}` 是强制走某个指定渠道的标记，**只有管理员能用**，普通令牌没有这段。

令牌有四种状态：

| 状态 | 数值 | 含义 |
|------|------|------|
| 启用 | 1 | 正常可用 |
| 禁用 | 2 | 被手动停用 |
| 过期 | 3 | 超过了设置的过期时间 |
| 耗尽 | 4 | 令牌额度用完，自动停止 |

这里有个最容易混淆的点：**令牌额度 ≠ 账户余额**。账户余额是整个站的扣费来源，令牌额度是「这张卡最多能花多少」的子限制。就算账户里很有钱，只要令牌额度耗尽（状态 4），请求一样会报「额度不足」。

> [!warning] 易错点：Key 只在创建弹窗显示一次
> 创建令牌成功后会弹出一个窗口完整显示 `sk-...`，**一旦关闭就再也看不到了**。务必当场复制到安全的地方（密码管理器或本地文件），否则只能重新建一个。Key 泄漏了也不怕，直接禁用重建即可。

### 5.2 创建令牌：字段讲解与最佳实践

操作路径：管理后台 → 令牌 → 添加令牌。核心字段如下[new-api 官方令牌管理](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)：

| 字段 | 含义 | 零基础建议 |
|------|------|-----------|
| 名称 | 用途标注，≤50 字符 | 按客户端命名，如 `nextchat-token` |
| 过期时间 | 令牌有效期 | 留空或 -1 = 永不过期 |
| 剩余配额 | 令牌最大消耗上限 | 自用先设小额度，如 50,000 |
| 无限配额 | 跳过令牌额度检查 | 自用可开，但仍受账户余额约束 |
| 模型限制 | 模型白名单 | 只勾常用模型，减少误用 |
| IP 白名单 | 限定来源 IP/CIDR | 自用可留空 |
| 分组 | 该令牌走的渠道分组 | 默认 `default` |

最佳实践三句话：**一个客户端一个令牌**（哪个 Key 泄漏了只影响一台）；**令牌上尽量勾模型白名单**（防止被调走贵的模型）；**额度先小后大**（确认够用再放开）。

### 5.3 额度是怎么算的

new-api 的计费单位是「配额点数」，**1 美元 = 500,000 配额点数**[官方倍率设置](https://docs.newapi.pro/zh/docs/guide/console/settings/rate-settings)。每次调用的消耗按这个公式算：

```
配额消耗 = (输入 token 数 + 输出 token 数 × 补全倍率) × 模型倍率 × 分组倍率
```

- **补全倍率**：通常输出比输入更贵，如 gpt-4o 补全倍率 = 4、gpt-3.5-turbo = 2；
- **模型倍率**：如 gpt-4o = 1.25、gpt-4o-mini = 0.075；
- **分组倍率**：默认组为 1，可在系统设置里调。

举一个完整例子：用 gpt-4o 请求，输入 1,000 token、输出 500 token。

```
输出按补全倍率放大：500 × 4 = 2,000
(1,000 + 2,000) × 模型倍率 1.25 = 3,750 配额
3,750 ÷ 500,000 ≈ 0.0075 美元
```

一次普通对话只花不到一分钱。自用模式且未配置倍率时，会走默认值，不必给每个模型手动定价。

### 5.4 接入第三方客户端

所有 OpenAI 兼容客户端接入中转站，都只要配三个东西：**Base URL（中转站地址）、API Key（刚才的 `sk-...`）、模型名**。这就是「通用三要素」。

> [!tip] 大白话：三要素像「快递收货地址」
> Base URL 是驿站地址，API Key 是你的取件码，模型名是你想取哪家快递的包裹。三个填对了，快递就能正常送到你手里。

主流客户端配置对照表[官方 Cherry Studio 接入](https://docs.newapi.pro/zh/docs/apps/cherry-studio)：

| 客户端 | Base URL | API Key | 模型名 |
|--------|----------|---------|--------|
| NextChat | 站点地址（或环境变量 BASE_URL） | `sk-...` | 自定义模型写 `+模型名@OpenAI` |
| Cherry Studio | 站点地址（内置 NewAPI 类型） | `sk-...` | 手动添加模型 ID |
| ChatBox | `https://站点/v1` | `sk-...`（**不要加 Bearer**） | 手动填模型 ID |
| LobeChat | `https://站点/v1` | `sk-...` | 手动添加模型 ID |
| Claude Code | `ANTHROPIC_BASE_URL=https://站点` | `ANTHROPIC_API_KEY=sk-...` | `/model` 里选择 |

以 NextChat 的 Docker 部署为例，Base URL 与 API Key 通过环境变量传入：

```bash
docker run -d -p 3000:3000 \
  -e BASE_URL=http://你的站点 \      # 你的中转站地址
  -e OPENAI_API_KEY=sk-xxxx \        # 刚复制的令牌
  -e CODE=你的访问密码 \
  yidadao/chatgpt-next-web
```

Claude Code 则是设置两个环境变量：

```bash
export ANTHROPIC_BASE_URL=https://你的站点
export ANTHROPIC_API_KEY=sk-xxxx
```

### 5.5 连接测试与 Claude 模型坑

无论用哪个客户端，都建议先用 curl 验证中转站和令牌是否连通（推荐先做）[官方 FAQ](https://docs.newapi.pro/zh/docs/support/faq)：

```bash
curl -sS https://你的站点/v1/models -H "Authorization: Bearer sk-xxxx"
```

期望返回一个 JSON 列表，里面是你在渠道里配好的模型：

```json
{"object":"list","data":[{"id":"gpt-4o","object":"model"},{"id":"deepseek-chat","object":"model"}]}
```

如果返回的模型列表正常，说明「令牌 + 渠道 + 模型名」整条链路是通的，问题只剩客户端配置。

最后一个高频坑，专门讲 Claude 模型：NextChat 看到模型名以 `claude-` 开头，会默认走 **Anthropic 原生协议**（用 `x-api-key` 头鉴权），而 new-api 只认 OpenAI 兼容的 `Authorization: Bearer`，于是报错。

> [!warning] 易错点：NextChat 里的 Claude 模型要加 `@OpenAI` 后缀
> 在 NextChat 自定义模型里写 `claude-3-5-sonnet-20241022` 会走错协议。要写成 **`+claude-3-5-sonnet-20241022@OpenAI`**，并在下拉列表里选择标注了 `(OpenAI)` 的项，强制走 OpenAI 兼容通道，`x-api-key` 报错即消失[linux.do NextChat 接入排障](https://linux.do/t/topic/176116)。

### 本章小结

- 令牌格式 `sk-{base_key}[-{channel_id}]`，**Key 只在创建弹窗显示一次，必须当场复制**。
- 令牌额度 ≠ 账户余额：令牌额度是子限制，耗尽（状态 4）照样报「额度不足」。
- 额度公式：`(输入 + 输出 × 补全倍率) × 模型倍率 × 分组倍率`，1 美元 = 500,000 配额。
- 接入客户端只认「三要素」：Base URL + API Key + 模型名；不同客户端写法略有差别。
- 连接测试先跑 `curl /v1/models`；NextChat 用 Claude 模型要加 `+模型名@OpenAI`。

下一章我们进入日常运维：把高频报错、额度不足排查、数据备份与升级一次讲清，让你用得安心。

---

## 第六章：常见坑与运维

> 本章回答一个很现实的问题：**中转站报错了怎么办？怎么才能不丢数据、安全升级？** 前面五章解决「把中转站跑起来」，这一章解决「让它稳稳跑下去」。我们把高频报错列成速查表，讲清重试与自动禁用两道兜底防线，再手把手教你备份与升级，最后给出日常运维命令。

### 6.1 高频报错速查表

下表覆盖零基础用户最常遇到的五类报错。遇到问题先查表，再按「原因」逐项核对，绝大多数都能当场解决。

| 报错现象 | 常见原因 | 处理步骤 |
|---------|---------|---------|
| 「无可用渠道」/ `model_not_found` | ① 渠道 Models 没勾该模型 ② 令牌/用户组不在渠道 Group ③ 渠道被禁用 | 核对模型名完全一致 → 核对分组 → 检查渠道状态 |
| 有余额仍 `insufficient_quota` | 令牌额度耗尽 / 模型倍率未配 / 预消费估算超限 | 先查令牌剩余额度 → 补配倍率 → 自用开「自用模式」 |
| `invalid character '<'` | 上游返回 HTML 而非 JSON（BaseURL 指错，或被 CDN/反代拦截） | 核对 BaseURL（不带结尾 /v1）→ 换出口 IP 再试 |
| 分组负载饱和 | 上游接口被 429 限流 | 渠道加限速、降权重、加同优渠道、开自动禁用 |
| 倍率或价格未配置 | 模型没配价格，对外模式下不可用 | 补配价格，或自用场景切「自用模式」 |

> [!tip] 大白话：报错排查像「驿站取件失败」
> 把一次请求想成去驿站取快递——「无可用渠道」是**货没到**（渠道没配），「额度不足」是**余额不够付取件费**（令牌额度没了），`invalid character '<'` 是**驿站塞了张白纸当回执**（上游返回的不是 JSON）。先分清「没货」「没钱」「货送错了」三类再对症下药，就不会乱。

注意 `insufficient_quota` 最容易误判：账户明明还有钱，客户端却报额度不足。第一反应应查**令牌剩余额度**而不是账户余额——令牌额度是这张卡的消费封顶，账户余额是总话费[令牌管理官方文档](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)。

### 6.2 重试机制与自动禁用兜底

除了手动排查，new-api 还有两道自动防线：**自动重试**和**自动禁用**。但两道防线都有脾气，用错会踩坑。

#### 6.2.1 重试只认特定状态码

自动重试**只对特定 HTTP 状态码生效**——默认是 429（限流）和一部分 5xx；400、408、504、524 等**不会重试**[GitHub Issue #2659](https://github.com/QuantumNous/new-api/issues/2659)。

> [!tip] 大白话：重试像「快递员多敲一次门」
> 快递员只对「门没开但人应该在家」的情况（429 限流、5xx 服务端错误）多敲两下；对「单子已取消」（400 参数错误）不会傻等。**别指望重试能救「参数错误」**，那得改配置。

#### 6.2.2 exhausted 不重试的坑

最典型的坑：**额度不足（`exhausted` / `insufficient_quota`）不是 429，会被直接透传，不自动重试**。这其实是合理设计——额度不足重试一百次还是不足，只会白烧流量。社区在 [PR #2663](https://github.com/QuantumNous/new-api/pull/2663) 里把「自动重试状态码」做成了可配置项。记住结论就够：**遇到额度不足，去查令牌额度和倍率，别等重试。**

#### 6.2.3 自动禁用关键词兜底

在**系统设置 → 运营设置**里配置关键词，当渠道返回的错误文本包含某个词时，系统自动把该渠道拉黑（状态 3），不再参与路由。官方默认带了一批英文词（`Your credit balance is too low`、`insufficient_quota` 等），你也可以补中文词：

```text
# 系统设置 → 运营设置 → 自动禁用关键词（每行一个）
Your credit balance is too low
insufficient_quota
剩余额度不足
该令牌额度已用尽
```

> [!tip] 大白话：自动禁用像「驿站黑名单」
> 某个供应商连续出错，驿站就把它的货拉黑不再接收，省得每次派件都失败。**黑名单不是永久的**，配合「成功自动启用」，供应商恢复正常后还能重新上岗。

#### 6.2.4 配套推荐组合

四件套搭配效果最好：**① 失败自动禁用**（配合关键词）**② 成功自动启用**（渠道恢复正常后自动恢复）**③ 定期渠道测试**（用渠道列表的「测试所有渠道」批量体检）**④ 渠道优先级分层**（高优渠道挂了自动降级到低优渠道）[官方 FAQ](https://docs.newapi.pro/zh/docs/support/faq)。

### 6.3 数据备份与升级

先记住铁律：**升级前必须先备份；没挂载 `/data` 卷，容器一重建数据就全没了。**

#### 6.3.1 升级前先备份

```bash
# SQLite 版（单容器自用最常见）：整目录拷贝，按日期留档
cp -r ./data ./data.bak.$(date +%F)
```

```bash
# MySQL 版（Compose 完整版）：导出成 SQL 文件
mysqldump -u root -p new-api > new-api.sql
```

`$(date +%F)` 会拼出当天日期（如 `data.bak.2026-08-12`），每次备份不覆盖旧的。备份完确认文件存在再继续。

#### 6.3.2 升级三步走

```bash
# 1. 拉取新镜像
docker compose pull

# 2. 停掉旧容器（数据卷保留，不会删数据）
docker compose down

# 3. 用新镜像重新创建并启动
docker compose up -d
```

单容器部署同理：`docker pull calciumion/new-api:latest` 后，用**和之前一模一样**的挂载参数重建容器（`-v ./data:/data` 必须带上）。容器更新的一般方法可参考 [[docker/docker容器如何更新]]。

#### 6.3.3 升级不丢数据的关键：挂载 volume

> [!warning] 易错点：没挂 `/data` = 容器重建即丢数据
> 容器里的数据默认存在容器内部，容器被删掉重建，里面的一切随之消失。只有把宿主机目录挂载进容器（`-v ./data:/data`），数据才落在宿主机上，重建后继续存在。**「升级后数据全没了」的答案，十有八九是当初没挂载 `/data`**。

> [!tip] 大白话：挂载 volume 像「把贵重物品锁进保险箱」
> 容器像一间临时办公室，东西放桌上，办公室拆了东西就没了；把 `/data` 挂载出去，等于把贵重物品锁进保险箱，办公室拆了重建，保险箱里的东西原封不动。**「保险箱」这个动作必须在第一次部署时就做好**，亡羊补牢来不及。

| 部署方式 | 数据落在哪 | 升级后数据还在吗 |
|---------|-----------|----------------|
| 单容器 + `-v ./data:/data` | 宿主机 `./data` 目录 | ✅ 在 |
| 单容器 + 没挂载 | 容器内部（随容器删除而消失） | ❌ 全丢 |
| Compose + `pg_data` 命名卷 | Docker 管理的数据卷 | ✅ 在 |

### 6.4 日常运维与配套最佳实践

#### 6.4.1 看日志

```bash
docker compose logs -f new-api           # 实时跟踪（Ctrl+C 退出）
docker compose logs --tail=100 new-api   # 只看最近 100 行
docker compose logs -f new-api | grep -iE "error|fail|quota"   # 只过滤报错行
```

`-f` 是跟随，`--tail=100` 是只看末尾 100 行，`grep -iE` 按关键词过滤。日志里出现 `insufficient_quota`、`exhausted` 走额度排查；出现 `no available channel` 走 6.1 的无可用渠道排查。

#### 6.4.2 令牌过期提醒

令牌状态有四种：`1 启用 / 2 禁用 / 3 过期 / 4 耗尽`。客户端 Key 突然不好使，先去令牌列表看状态：

- **状态 3（过期）**：创建时设了过期时间，到期自动失效，重新创建即可。
- **状态 4（耗尽）**：令牌剩余额度用完，充值账户余额并给令牌加额度。
- **状态 2（禁用）**：检查是否误操作。

建议每季度批量检查一次令牌状态，长期不用的禁用掉，降低 Key 泄露面[令牌管理官方文档](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)。

#### 6.4.3 渠道 Key 失效处理

上游服务商的 Key 到期、被删或超额后，渠道开始报错。处理顺序：

1. 点渠道列表的「测试」，看报错是「鉴权失败」还是「网络不通」；
2. 结合日志确认是上游拒绝（改 Key）还是网络/BaseURL 问题（改配置）；
3. 更新 Key 后重新测试；短期搞不定的渠道先**手动禁用**，别占请求名额。

#### 6.4.4 限流配置建议

所有下游请求会汇聚到上游渠道，不加控制的话，一个客户端的高频请求就能把上游打到 429，连累其他用户。建议：给重要渠道配**限速**（如每分钟请求数上限）；用**优先级 + 权重**分层，主渠道高优、备用低优，扛不住自动降级；把上游 429 也纳入自动禁用/降级策略，避免雪崩。

### 本章小结

- 五类高频报错有固定套路：**无可用渠道查「模型/分组/状态」**，额度不足**先查令牌额度再查账户余额**，`invalid character '<'` 查 BaseURL。
- **自动重试只认 429 和部分 5xx**；`exhausted` 额度不足**不重试**，直接透传。
- 自动禁用关键词是兜底，推荐**失败自动禁用 + 成功自动启用 + 定期测试 + 优先级分层**四件套。
- **升级前先备份**（SQLite `cp -r` / MySQL `mysqldump`）；升级用 `docker compose pull && down && up -d`。
- **数据不丢的关键是挂载 `/data` 卷**——没挂载，容器重建即丢。
- 日常运维三件事：**看日志 → 查令牌状态 → 定期测试渠道**。

下一章是最后一章：把从零到一的完整流程从头串一遍，回顾每个环节做了什么，再给出进阶方向与权威资料清单，帮你从「能跑」走向「会用、会查、会优化」。

---

## 第七章：总结与进阶

> 到这里，你已经走完了从零到一的全部路程。这一章我们不学新东西，只做三件事：把前面六章的步骤整理成一张可以照做的 10 步清单，给你指几条继续深入的进阶方向，再把这套笔记引用过的权威资料一次性交到你手里。读完你就可以合上笔记，开始动手了。

### 7.1 从零到一全流程回顾

下面这 10 步就是整套笔记的主线，也是你搭建中转站的「终章 checklist」。照着顺序做，每一步的详细操作都在对应章节里，遇到卡壳翻回去即可。

| # | 步骤 | 对应章节 |
|---|------|---------|
| 1 | 准备 64 位 Linux 服务器（内存 1GB+），安装 Docker 与 Compose | 第 2 章 |
| 2 | 选部署方式：自用选单容器 SQLite，生产/对外选 Compose 完整版 | 第 2 章 |
| 3 | 访问 `http://IP:3000`，初始化向导创建管理员账号，选「自用模式」 | 第 3 章 |
| 4 | 立即改密、改用户名、关闭开放注册、设置固定 SESSION_SECRET | 第 3 章 |
| 5 | 添加第一个渠道：选类型 → 填 Key → 选模型 → 分组 default → 测试 | 第 4 章 |
| 6 | 创建令牌（设额度 / 模型白名单 / 分组），当场复制 `sk-...` | 第 5 章 |
| 7 | `curl /v1/models` 验证连通 | 第 5 章 |
| 8 | 接入客户端（NextChat / Cherry Studio / ChatBox 等），配 Base URL / API Key / 模型名 | 第 5 章 |
| 9 | 若对外服务：Nginx/Caddy + HTTPS 反代，配置自动禁用关键词兜底 | 第 3、6 章 |
| 10 | 日常运维：先备份再升级，`docker compose logs` 看日志 | 第 6 章 |

> [!tip] 大白话：这份清单像「装修验收单」
> 把搭建中转站想成装修一套房，这份 10 步清单就是验收单——水电（部署）、刷墙（渠道）、装锁（令牌）每项都打勾，房子才算能住人。**所以别跳步**，第 5、6 步不完成，客户端永远连不上。

### 7.2 进阶方向

基础能跑起来之后，下面这些方向任选一条深入，每一条都能明显提升体验。

| 进阶方向 | 一句话说明 | 想清楚再动手 |
|---------|-----------|-------------|
| HTTPS 反向代理 | 用 Nginx/Caddy 给中转站套上域名和 HTTPS，把 3000 端口藏到内网 | 自用可先跳过，对外服务必做 |
| 多分组多渠道 | 用分组隔离「自用/亲友/对外」，同模型配多渠道做负载均衡与故障切换 | 渠道变多后，配合 AutoBan 更省心 |
| 计费定价 | 按模型倍率、分组倍率给每个模型定价，把中转站变成可对外收费的服务 | 自用模式可完全不管价格 |
| 监控告警 | 用日志 + 自动禁用关键词 + 定期渠道测试，把故障拦在用户发现之前 | 渠道一多，人肉盯不过来 |
| 多实例部署 | 用 Compose 在多个节点部署，配合数据库读写分离扛更高并发 | 单机自用阶段不需要 |

> [!tip] 大白话：进阶方向像「自住还是开店」
> 前面的搭建是「把房装修好」，进阶方向是决定「自住还是开店」——自住（自用）几乎不用管价格和监控，开店（对外）才要定菜单（计费）、雇保安（监控告警）、开分店（多实例）。**所以先想清楚用途，再决定要不要进阶**。

### 7.3 权威资料清单

这套笔记的所有素材都来自下面这些官方与高可信来源，遇到任何问题优先在这里查，比搜索引擎更可靠。

**官方仓库与文档站**
- new-api 官方仓库 README：[QuantumNous/new-api](https://github.com/QuantumNous/new-api)
- 官方文档站：[docs.newapi.pro](https://docs.newapi.pro/)

**部署与配置文档**
- Docker 单容器部署：[官方部署文档](https://docs.newapi.pro/en/docs/installation/deployment-methods/docker-installation)
- Docker Compose 部署：[官方部署文档](https://docs.newapi.pro/en/docs/installation/deployment-methods/docker-compose-installation)
- compose 配置详解（含 SESSION_SECRET）：[官方配置文档](https://docs.newapi.pro/zh/docs/installation/config-maintenance/docker-compose-yml)

**功能指南与 FAQ**
- 渠道管理：[官方文档](https://docs.newapi.pro/zh/docs/guide/feature-guide/admin/channel)
- 令牌管理：[官方文档](https://docs.newapi.pro/zh/docs/guide/feature-guide/user/token)
- 倍率设置：[官方文档](https://docs.newapi.pro/zh/docs/guide/console/settings/rate-settings)
- 官方 FAQ：[docs.newapi.pro/support/faq](https://docs.newapi.pro/zh/docs/support/faq)
- Cherry Studio 官方接入：[官方文档](https://docs.newapi.pro/zh/docs/apps/cherry-studio)

**进阶源码与社区**
- 源码解析：DeepWiki [Channel Management](https://deepwiki.com/QuantumNous/new-api/3-channel-management) / [API Tokens](https://deepwiki.com/QuantumNous/new-api/6.2-api-tokens)
- GitHub Issue #2659（exhausted 不重试）：[issue](https://github.com/QuantumNous/new-api/issues/2659)
- PR #2663（自动重试状态码可配置）：[PR](https://github.com/QuantumNous/new-api/pull/2663)

> [!tip] 大白话：权威清单像「说明书和售后电话」
> 自己折腾遇到问题，最怕在网上乱搜到过时答案。这份清单就是官方「说明书 + 售后电话」——先查官方文档，再翻 GitHub Issue，多数坑都能原地解决。**所以把这一节收藏起来，比记任何教程都管用**。

### 本章小结

- 用 10 步清单对照检查，你的中转站「从零到一」就算真正落地了。
- 进阶方向按用途取舍：自用几乎零成本，对外服务再补 HTTPS、计费、监控与多实例。
- 权威资料以官方仓库、官方文档站、部署文档和 FAQ 为第一优先级，社区与源码解析作补充。
- 整条学习路径「概念 → 部署 → 初始化 → 渠道 → 令牌 → 接入 → 运维」到此闭环。

到这里，整套笔记就结束了。剩下的路要靠你自己动手踩出来——第一次配好渠道、第一次用上自己的中转站，那种「原来就这么简单」的感觉，就是最好的结业证书。去动手吧！
