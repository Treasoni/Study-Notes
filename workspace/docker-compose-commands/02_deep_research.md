# Docker 与 Docker Compose 命令的使用 - 深度收集素材

收集时间: 2026-08-08
阶段: P2 深度收集
信源: 以 Docker 官方文档为准，技术博客/社区补充
素材质量: 官方文档 6 篇 / 技术博客 4 篇 / 社区 3 篇，已交叉核验

---

## 第一部分：Docker CLI 命令速查

### 1.1 核心概念（大白话素材）

> [!tip] 大白话
> **镜像 = 模板 / 菜谱**：一份只读、可反复复用的"设计蓝图"，包含代码、运行时、系统库和配置；本身不能运行。
> **容器 = 实例 / 一盘菜**：照镜像"现做"出来的一个可运行、可修改、用完可扔的运行实例；同一份镜像可以同时开出很多容器。

日常流程比喻：`docker pull`（拿菜谱）→ `docker run`（照菜谱做菜并端上桌）→ `docker ps`（看看桌上摆了几盘）→ `docker stop/rm`（收走/倒掉）。要长期保留新改动，应写进 Dockerfile 重新 `docker build`，而不是手工改容器。

### 1.2 镜像管理

| 命令 | 用途 | 常用示例 |
|------|------|---------|
| `docker pull NAME[:TAG]` | 从仓库（默认 Docker Hub）拉取镜像 | `docker pull nginx`、`docker pull ubuntu:22.04` |
| `docker images` | 列出本地已有镜像 | `docker images` |
| `docker rmi IMAGE` | 删除镜像（`-f` 强制删被运行容器使用的） | `docker rmi nginx`、`docker rmi -f <id>` |
| `docker build -t NAME .` | 用 Dockerfile 构建镜像 | `docker build -t myapp:latest .` |
| `docker tag 源 目标` | 给镜像打标签/别名（指向同一镜像，不复制） | `docker tag myapp:latest myreg/myapp:v1.0` |
| `docker push NAME[:TAG]` | 推送到仓库（需先 `docker login`） | `docker push username/myapp:latest` |

### 1.3 容器管理

**核心命令 `docker run`**，语法：`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

| Flag | 含义 | 示例 |
|------|------|------|
| `-d` | 后台运行（detached） | `-d` |
| `-p 宿主:容器` | 端口映射 | `-p 8080:80` |
| `-v 宿主:容器` | 挂载目录/卷 | `-v $(pwd):/app` |
| `-e KEY=VALUE` | 设置环境变量 | `-e TZ=Asia/Shanghai` |
| `--rm` | 容器退出时自动删除（适合临时运行） | `--rm` |
| `--name 名字` | 给容器命名 | `--name web` |
| `--restart 策略` | 重启策略：`no`/`on-failure[:次数]`/`always`/`unless-stopped` | `--restart=always` |
| `-it` | 交互式终端（-i 保持 stdin，-t 分配伪终端） | `-it` |

综合示例：`docker run -d -p 8080:80 --name web --restart=always nginx`

**其他容器命令**：

| 命令 | 用途 | 示例 |
|------|------|------|
| `docker ps [-a]` | 列容器（默认运行中，`-a` 含已停止） | `docker ps -a` |
| `docker start/stop/restart CONTAINER` | 启动/停止/重启 | `docker stop web` |
| `docker rm [-f] [-v] CONTAINER` | 删除容器（`-f` 强删运行中，`-v` 删匿名卷） | `docker rm -f web` |
| `docker exec [-it] CONTAINER CMD` | 在运行中容器执行命令 | `docker exec -it mynginx sh` |
| `docker logs [-f] [--tail N] CONTAINER` | 查看日志 | `docker logs -f --tail 100 app` |
| `docker inspect CONTAINER\|IMAGE` | 查看底层详情（IP、挂载、环境变量、配置） | `docker inspect web` |
| `docker cp 容器:路径 宿主路径` | 与容器双向复制文件 | `docker cp mynginx:/etc/nginx/nginx.conf ./` |
| `docker stats` | 实时查看 CPU/内存/网络/磁盘占用 | `docker stats` |
| `docker top CONTAINER` | 查看容器内进程（类似宿主 ps） | `docker top mynginx` |

### 1.4 网络与卷

| 命令 | 用途 |
|------|------|
| `docker network ls / create / inspect / connect / disconnect / rm` | 网络管理（`-d bridge` 默认驱动） |
| `docker volume ls / create / inspect / rm / prune` | 数据卷管理（`volume prune -a -f` 清理未使用卷） |

### 1.5 系统管理

| 命令 | 用途 |
|------|------|
| `docker info` | 系统级信息（容器/镜像数量、存储驱动） |
| `docker version` | Client 与 Server/Engine 版本 |
| `docker system df` | 磁盘占用统计（镜像/容器/卷/构建缓存） |
| `docker system prune [-a] [-f] [--volumes]` | 清理：默认删已停容器+未用网络+悬空镜像+未用构建缓存；`-a` 连未用镜像；`--volumes` 额外清理卷（高风险） |
| `docker login/logout` | 登录/退出镜像仓库（`--password-stdin` 安全读密码） |

---

## 第二部分：Docker Compose 命令与配置

### 2.1 v1 vs v2（必须先讲清）

| | v1 | v2 |
|---|---|---|
| 命令 | `docker-compose`（连字符） | `docker compose`（空格） |
| 实现 | 独立 Python 工具 | Go 编写的 Docker CLI 插件 |
| 状态 | 已弃用、停止维护，官方不推荐 | 现行标准，随 Docker Desktop/Engine 安装（Linux 装 `docker-compose-plugin`） |
| 文件 | `docker-compose.yml` | 无需修改，直接通用 |

- **迁移**：把连字符换成空格即可，绝大多数命令 drop-in 兼容：`docker-compose up` → `docker compose up`
- **行为差异**：v2 容器名用连字符 `-`（`example-frontend-1`），v1 用下划线 `_`；v2 不支持 `compose scale`（改用 `up --scale`）

### 2.2 compose 核心命令

| 命令 | 用途 |
|------|------|
| `docker compose up [-d] [--build] [--force-recreate]` | 构建、创建、启动；`-d` 后台；`--build` 启动前构建；`--force-recreate` 强制重建 |
| `docker compose down [-v]` | 停止并删除容器、默认网络；**默认保留命名卷**；`-v` 删除命名卷（破坏性） |
| `docker compose ps` | 列出容器与状态 |
| `docker compose logs [-f] [-n N]` | 查看日志；`-f` 跟随；`-n` 只看末尾 N 行 |
| `docker compose exec SERVICE CMD` | 在**运行中**容器执行命令（默认分配 TTY，`-T` 关闭） |
| `docker compose build [--no-cache]` | 构建/重建镜像 |
| `docker compose pull / push` | 拉取 / 推送服务镜像 |
| `docker compose config [-q]` | 合并 `-f` 文件、解析变量、展开短语法并渲染；`-q` 仅校验不输出 |
| `docker compose run SERVICE CMD` | 按服务定义**新建一次性容器**执行命令（区别于 exec） |
| `docker compose restart / stop / start` | 重启 / 停止（保留容器）/ 启动 |
| `docker compose stats / top / images` | 资源占用 / 容器内进程 / 已用镜像 |

### 2.3 compose.yaml 语法

顶层三大块 + `name`：

```yaml
name: myapp
services:
  web:  ...
networks:
  front-tier: {}
volumes:
  db-data:
```

service 常用键：

```yaml
services:
  web:
    image: nginx:1.27          # 镜像
    build: ./backend           # 或 build: {context: ./backend, target: builder}
    container_name: web        # 固定名；设置了就不能 scale 超过 1
    command: ["nginx", "-g", "daemon off;"]   # 覆盖镜像 CMD
    entrypoint: /entry.sh      # 覆盖镜像 ENTRYPOINT
    ports:
      - "8080:80"              # "host:container"，字符串形式
    expose:
      - "3000"                 # 仅容器间可访问，不映射到宿主机
    environment:               # mapping 形式
      POSTGRES_USER: example
      ENABLE_FEATURE: "true"   # 布尔值必须加引号，否则 YAML 解析成布尔
    env_file:
      - ./.env.backend         # environment 优先级高于 env_file
    volumes:
      - db-data:/var/lib/postgresql/data   # 命名卷（须顶层 volumes 声明）
      - ./config:/etc/app:ro              # 绑定挂载 host 路径 :container[:ro]
    depends_on:
      db:
        condition: service_healthy        # 长语法；或简单列表 ["db"]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
    restart: unless-stopped     # no | always | on-failure | unless-stopped
    networks:
      - front-tier
```

**关键语法点**：
- 命名卷必须顶层声明：`volumes: {db-data: {}}`，服务里引用
- 环境变量插值：YAML **值**中 `$VAR`/`${VAR}` 都会插值；字面 `$` 用 `$$` 转义；支持 `${VAR:-default}`、`${VAR:?error}`
- `.env` 自动加载（compose.yaml 旁），仅用于插值不默认注入容器；优先级 Shell 环境 > `--env-file` > `.env`
- `name:` 顶层项目名（Compose v2）；未设时按 `-p` > `COMPOSE_PROJECT_NAME` > `name:` > 目录名
- 默认文件名 `compose.yaml`（`docker-compose.yaml` 也认）；`-f` 可多次指定

### 2.4 常用工作流

```bash
docker compose up -d                 # 首次部署：拉镜像 + 建网络/卷 + 后台启动
docker compose pull && docker compose up -d   # 更新镜像（只重建镜像有变的服务）
docker compose logs -f               # 跟随日志
docker compose exec <service> sh     # 进容器
docker compose down                  # 停止并删容器/网络，保留数据卷
docker compose down -v               # 同上 + 删命名卷 → 数据丢失（破坏性）
docker compose config                # 校验并查看展开后的最终配置
```

> [!tip] 大白话
> **Compose 是什么**：把多个容器的启动参数（镜像、端口、环境变量、数据卷、网络）统一写进一个 `compose.yaml`，`docker compose up -d` 一条命令全部启动；等价于把一串 `docker run` 命令编排成一个项目。
> **project/service/volume 比喻**：项目 = 一整套应用（默认以目录名命名）；服务 = 应用里的一个组件（web、db），容器自动命名 `项目-服务-序号`（`example-frontend-1`）；命名卷 = 跨重启共享的持久化数据仓库，销毁容器后数据仍在。

---

## 第三部分：常见坑与排错

### 3.1 容器启动即退出（最常见）

**症状（先看退出码定性）**：

| 退出码 | 含义 | 典型原因 |
|--------|------|---------|
| 0 | 前台进程正常跑完就退出 | 应用自身后台化（daemonize），PID 1 结束容器即停 |
| 1 | 应用启动崩溃 | 配置错误、缺环境变量/密钥、依赖未就绪 |
| 126 | 文件存在但不可执行 | 权限拒绝 |
| 127 | 命令未找到 | 二进制缺失或路径错误 |
| 137 (128+9) | SIGKILL | 内核 OOM killer 杀掉（超内存限制） |

记忆规则：**退出码 = 128 + 信号编号**

**排查步骤（按顺序）**：
```bash
docker ps -a --filter name=<容器> --format "table {{.Names}}\t{{.Status}}\t{{.RunningFor}}"
docker inspect --format '{{.State.ExitCode}}' <容器>
docker inspect --format '{{.State.OOMKilled}}' <容器>   # 137 且 true = OOM
docker inspect --format 'Cmd={{.Config.Cmd}} Entrypoint={{.Config.Entrypoint}}' <容器>
docker logs --tail 100 <容器>
docker run --rm -it --entrypoint sh <镜像>              # 覆盖入口，交互式手动复现
sudo dmesg | grep -i "oom"                              # 内核确认 OOM
```

**解决**：
- daemonize（exit 0）：强制前台，`nginx -g "daemon off;"`、`apachectl -D FOREGROUND`
- OOM（137）：提高内存限制或降占用；JVM `-Xmx` 设为容器上限约 75%
- 崩溃（1）：`--entrypoint sh` 复现启动序列，核对环境变量、密钥挂载、网络依赖

**预防**：ENTRYPOINT/CMD 用 **exec 数组形式**（`CMD ["nginx","-g","daemon off;"]`），让应用直接作为 PID 1，正确接收 SIGTERM 优雅退出；shell form 会包成 `/bin/sh -c`，信号转发有中间层。

### 3.2 权限问题（UID/GID）

- **症状**：非 root 容器写宿主绑定挂载目录报 `Permission denied`
- **原因**：绑定挂载按**数字 UID/GID** 匹配，不按用户名；Docker 自动创建挂载目录时属主为 root:root 755
- **解决**：
  - `docker run -u $(id -u):$(id -g)`
  - compose 用 `user: "${UID}:${GID}"`（`.env` 配 `UID=1000`、`GID=1000`）
  - 宿主机 `chown -R 1000:1000 ./data`
  - LinuxServer.io 约定：`PUID`/`PGID` 环境变量，容器内部自动 chown

### 3.3 清理最佳实践

- **预览**：`docker system df`
- **日常清理**：`docker system prune -a --filter "until=24h"`
- **卷默认不删**：官方理由"Volumes are never removed automatically, because to do so could destroy data."，加 `--volumes` 前务必确认
- **单类型**：`docker container prune`、`docker image prune [-a]`、`docker network prune`、`docker buildx prune`

### 3.4 Windows 挂载路径问题

- **症状**：Windows 上 compose up 报 `Invalid volume specification: 'C:\Users\...:/app:rw'`
- **原因**：Compose 把 Windows 路径转换后发给 Linux daemon 解析不了
- **解决**：目标 Windows 容器时设 `COMPOSE_CONVERT_WINDOWS_PATHS=0`
- **v2.35.0+ 新坑**：bind 源路径不存在直接报 `bind source path does not exist`；短语法（`./data:/app/data`）默认隐含 `create_host_path: true`，长语法需显式设 `create_host_path: true`

### 3.5 其他高频坑

- **端口冲突** `port is already allocated`：`docker compose ps` 看谁在占，或 `ss -ltnp` / `netstat -ano | findstr :端口` 查宿主进程
- **YAML 校验**：`docker compose config --quiet` 静默校验；`$` 要写成 `$$` 转义；新版移除 `version:` 键（已弃用）
- **更新后不生效**：先 `docker compose down` 再 `up`，或 `docker compose up --force-recreate` 强制重建

---

## 参考信源

**官方文档**：
- Docker CLI 参考: https://docs.docker.com/reference/
- 官方速查 PDF: https://docs.docker.com/get-started/docker_cheatsheet.pdf
- Compose CLI 参考: https://docs.docker.com/reference/cli/docker/compose/
- compose.yaml 语法: https://docs.docker.com/reference/compose-file/
- Compose 应用模型: https://docs.docker.com/compose/compose-application-model/
- Prune 清理: https://docs.docker.com/engine/manage-resources/pruning/
- UID/GID 映射: https://docs.docker.com/engine/security/rootless/uid-gid-mapping/
- v1→v2 迁移: https://docs.docker.com/compose/migrate/

**技术博客 / 社区**：
- Netdata 启动即退出排查: https://www.netdata.cloud/guides/docker/docker-container-exits-immediately/
- LinuxServer.io Compose 指南: https://docs.linuxserver.io/general/docker-compose/
- dev.to 命令速查: https://dev.to/benriemer/... / https://dev.to/primghostdev/...
- SO Windows 挂载路径: https://stackoverflow.com/questions/79373371/
- GitHub docker/compose #12735（v2.35 bind 路径回归）: https://github.com/docker/compose/issues/12735
