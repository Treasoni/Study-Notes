## Docker Compose：v1/v2 与核心命令

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
