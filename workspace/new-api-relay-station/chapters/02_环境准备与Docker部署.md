# 第二章：环境准备与 Docker 部署

> 第一章我们把「中转站是什么」讲清楚了，这一章开始动手：准备一台 64 位 Linux 服务器、装好 Docker，用两种方式把 new-api 跑起来——先讲单容器快速部署（个人自用够用），再讲 Docker Compose 完整版（生产推荐），最后教你怎么验证部署成功。全程零基础可跟做，每个命令都可以直接复制。

## 2.1 前置要求与部署方式选型

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

## 2.2 安装 Docker 与 Docker Compose

以 Ubuntu 为例，官方提供了一键安装脚本[官方 Docker 安装脚本](https://get.docker.com)，把下面三行依次执行：

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

## 2.3 单容器快速部署（自用 SQLite）

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

## 2.4 Docker Compose 完整版（生产推荐）

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

## 2.5 常用管理命令与部署验证

启动之后，最常用的几条管理命令如下（都要在 `docker-compose.yml` 所在目录执行）[官方 compose 部署文档](https://docs.newapi.pro/zh/docs/installation/deployment-methods/docker-compose-installation)：

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

## 本章小结

- 前置三底线：**64 位 Linux、内存 1 GB+（完整版 2 GB+）、磁盘 10 GB+**；选型上**自用选单容器 SQLite，对外选 Compose 完整版**。
- Docker 安装用官方一行脚本：`curl -fsSL https://get.docker.com | sudo sh`，之后用 `docker --version && docker compose version` 验证。
- 单容器命令的**两个必记点**：`-v ./data:/data` 必须挂载（否则丢数据）；端口映射**左宿主机、右容器**。
- Compose 完整版把 new-api + PostgreSQL + Redis 三个容器一起编排，`docker compose up -d` 一键启动，生产更稳。
- 验证部署：`docker compose ps` 看健康状态，`curl -s http://localhost:3000/api/status` 应返回 `"success": true`。
- 日常管理就记四条：`ps` 看状态、`logs -f` 看日志、`down` 停止、**`down -v` 慎用**。

下一章，我们打开浏览器完成第一次初始化：创建管理员账号、选择使用模式，并顺手做一遍安全加固——这些做完，你的中转站才算真正「上线」。
