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

配置语法已经打通，下一步自然要面对"写完的配置真的能跑起来吗"——第 6 章我们进入最常见的高频坑与排错：容器启动即退出、权限问题、端口冲突、Windows 挂载路径，每一条都配对应的排查命令和退出码定性表，让你遇到问题能自己定位。
