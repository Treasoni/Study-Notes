## 第 2 章：动手：用 Docker 把 SearXNG 跑起来

### 2.1 先选一条路

这一章把第 1 章讲的「实例」真正立起来：用 Docker 在本机起一个 SearXNG，浏览器打开就能搜。有两条**等价**路径，随便选一条都能跑通：

| 路径 | 它是什么 | 适合谁 |
| --- | --- | --- |
| ① Hermes 单服务配方 | 一个 `searxng` 容器直接跑，配置挂到 `./searxng` | 只想尽快接上 Hermes 的人（最省事） |
| ② SearXNG 官方编排 | 双服务 `core` + `valkey`，配置挂到 `./core-config/` | 想贴近上游现状、以后好跟官方升级的人 |

> [!tip] 只想最快跑通？
> 直接照抄 2.3 的路径①，跳过 2.4 的路径②。两条路径出来的服务**一样**，只是容器数量与挂载目录名不同。

两条路出来的服务一模一样，差别只在「谁维护这套编排」：路径① 是 Hermes 官方文档给的单服务配方，图的是十几秒跑通、目录结构最简单；路径② 是 SearXNG **上游自己的** compose 模板，图的是跟官方保持一致、日后升级省心——代价是多带一个缓存服务、挂载目录名也不同。只想接上 Hermes，就抄路径①；想以后跟着上游升级，再抄路径②。

### 2.2 概念：容器第一次启动时发生了什么

先讲一个能省你半小时的机制。第一次 `docker compose up -d` 时，容器里的 `entrypoint.sh` 会检查 `/etc/searxng/settings.yml` 在不在；**不在，就顺手从镜像自带的模板 `settings.template.yml` 复制一份出来，并把模板里写死的占位密钥 `ultrasecretkey` 随机化**。[^c2-c]

所以：**不要从零手写 `settings.yml`**。正确姿势是让容器先生成一份，再在宿主上直接改——第 3 章开 JSON 就是干这件事。

实体落点：容器里的两个关键路径，分别对应宿主上的什么——

| 容器内路径 | 装什么 | 路径① 挂到宿主 | 路径② 挂到宿主 |
| --- | --- | --- | --- |
| `/etc/searxng/` | 配置文件（`settings.yml` 等） | `./searxng` | `./core-config/` |
| `/var/cache/searxng/` | 持久数据（`faviconcache.db` 等） | Docker 卷 `core-data` | Docker 卷 `core-data` |

官方原话也把这两个卷点名了：`/etc/searxng` 是 `Configuration files (settings.yml, etc.)`，`/var/cache/searxng` 是 `Persistent data (faviconcache.db, etc.)`。[^c2-d]

顺带钉一个容易想当然的点：**并不是随便设一个环境变量就能改任意配置**。官方容器只认下面三族变量，别把不相干的变量名往里塞：[^c2-i]

| 变量族 | 管什么 | 本项目会用到的例子 |
| --- | --- | --- |
| `$SEARXNG_*` | `server:` / `general:` 下的同名配置项 | `SEARXNG_BASE_URL`、`SEARXNG_PORT` |
| `$GRANIAN_*` | Granian 这个应用服务器本身的选项 | 监听端口等 |
| `$FORCE_OWNERSHIP` | 把挂载进来的卷和文件属主统一改成 `searxng:searxng`（默认就开着） | 一般不用动 |

> [!tip] 大白话
> 把容器想成**一间出租屋**：房东（镜像）入住前已经放好一份配置模板，你进屋第一件事不是从白纸写起，而是把这份模板改两处、重启生效——而这份模板因为挂载，本来就摆在你宿主上。

### 2.3 路径① 照抄：Hermes 单服务

**第一步，建工作目录**（把 `docker-compose.yml` 和配置都放在 `~/searxng` 下）：

```bash
mkdir -p ~/searxng/searxng
cd ~/searxng
```

**第二步，写 `docker-compose.yml`**（来源：Hermes 官方推荐配方）：[^c2-a]

```yaml
# ~/searxng/docker-compose.yml
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8888:8080"                       # 宿主 8888 → 容器 8080
    volumes:
      - ./searxng:/etc/searxng:rw         # 配置目录
    environment:
      - SEARXNG_BASE_URL=http://localhost:8888/
    restart: unless-stopped
```

这里 `SEARXNG_BASE_URL` 按官方支持项来用：它**是官方支持的覆盖项**（由 `settings.yml` 的 `base_url` 被其覆盖），但**官方 compose 未启用它**，这里是**本配方显式设置**的。[^c2-p]

**第三步，启动**：

```bash
docker compose up -d
```

起来后浏览器打开 `http://localhost:8888`，看到搜索框即成功。如果没起来，先 `docker compose ps` 看容器状态、再 `docker compose logs -f` 看日志——这两条命令是排错的第一落点。

> [!warning] 拉镜像被限流？
> Docker Hub 现在对**未认证的匿名拉取**有速率限制。如果你恰好被卡在拉取这一步，把镜像从 `searxng/searxng` 换成官方提供的 GHCR 镜像 `ghcr.io/searxng/searxng` 即可。[^c2-k]

### 2.4 路径② 官方编排，及与路径① 的 4 处差异

官方文档推荐用 compose 模板部署。[^c2-b] 四步走：

```bash
# 1) 建配置目录  2) 拉取官方 compose 模板与 .env 样例
mkdir -p ./searxng/core-config/
cd ./searxng/
curl -fsSL -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml
curl -fsSL -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
# 3) 复制出 .env   4) 启动
cp -i .env.example .env
docker compose up -d
```

注意这套编排和路径① **不是一回事**，差在 4 处（照抄错一处就会找不到目录）：

1. **双服务**：官方 compose 里除了 `core`，还有一个 `valkey` 缓存服务（`docker.io/valkey/valkey:9-alpine`）。[^c2-e]
2. **挂载点不同**：官方挂 `./core-config/:/etc/searxng/:Z`[^c2-f]，**不是**路径① 的 `./searxng`。
3. **端口默认 8080**：官方 compose 的宿主与容器端口都默认 8080；想要 8888 就设 `SEARXNG_PORT=8888`（或另做端口映射）。[^c2-g]
4. **`.env` 三项默认全是注释**（`#SEARXNG_VERSION` / `#SEARXNG_HOST` / `#SEARXNG_PORT`），也就是直接用镜像默认值。[^c2-h]

这里补两处容易含糊的细节。其一，官方约定用 `SEARXNG_PORT` 而不是直接改容器监听端口，是因为**容器入口脚本只认这一个变量**：它把纯数字的 `SEARXNG_PORT` 转成 Granian 真正读取的 `GRANIAN_PORT`；设成空值或非数字会被直接忽略，端口不会变。[^c2-j] 其二，挂载点结尾的 `:Z` 是 SELinux 环境下的重新打标，配合默认开启的 `$FORCE_OWNERSHIP`，保证容器有权限读写挂进去的配置目录。[^c2-i]

官方 compose 的关键片段长这样：[^c2-b]

```yaml
# container/docker-compose.yml（官方，节选）
services:
  core:
    image: docker.io/searxng/searxng:${SEARXNG_VERSION:-latest}
    ports:
      - ${SEARXNG_HOST:+${SEARXNG_HOST}:}${SEARXNG_PORT:-8080}:${SEARXNG_PORT:-8080}
    volumes:
      - ./core-config/:/etc/searxng/:Z
  valkey:
    image: docker.io/valkey/valkey:9-alpine
```

启动后用 `docker compose ps` 点个数——应当看到两个服务，其中 `core` 的端口映射是 `0.0.0.0:8080->8080/tcp`：

```bash
docker compose ps
# 输出示例（截取）：
# NAME             ...   PORTS
# searxng-core     ...   0.0.0.0:8080->8080/tcp
# searxng-valkey   ...   6379/tcp
```

> [!warning] 一个常见混淆
> 路径② 的 `settings.yml` 生成在 `./searxng/core-config/settings.yml`，而路径① 生成在 `~/searxng/searxng/settings.yml`。这两个位置都在**宿主**上（配置目录已经挂进容器），所以第 3 章改 JSON 直接编辑对应文件即可，不用先把它从容器里复制出来。

### 2.5 端口口径（对比表，全篇冻结）

端口是这篇笔记最容易翻车的地方，第一次就把它钉死，后面第 3、4、5 章原样复用：

| 场景 | 宿主端口 | 容器内端口 | 来源 |
| --- | --- | --- | --- |
| 官方 compose 默认 | 8080 | 8080 | L2-2 · `l2-2_container-docker-compose.yml:12` |
| 官方手动 `docker run` 示例 | 8888 | 8080 | L2-1 · `l2-1_installation-docker.html:585` |
| **裸机**（非容器）出厂 settings | 8888 | ——（裸机直接监听 8888） | L2-10 · `l2-10_searx-settings-default.yml:90` |
| Hermes 配方（路径①） | 8888 | 8080 | L3-1 · `l3-1_web-search.md:169` |

**一句话钉死：容器内一律 8080；8888 要么是宿主映射端口、要么是裸机出厂默认**；`SEARXNG_URL` 必须与宿主端口一致（本句在第 4、5 章原样复用，不改写）。

### 2.6 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `This is the recommended way to deploy SearXNG in a containerized environment.` | 这是在容器化环境里部署 SearXNG 的推荐方式。 | L2-1 · sources/l2-1_installation-docker.html:492 |
| 2 | `DockerHub now applies rate limits to unauthenticated image pulls. If you are affected by this, you can use the GHCR mirror instead.` | DockerHub 现在对未认证的镜像拉取施加速率限制；如果你受影响，可以改用 GHCR 镜像。 | L2-1 · sources/l2-1_installation-docker.html:480-481 |
| 3 | `This will start SearXNG in the background, accessible at http://localhost:8888` | 这会在后台启动 SearXNG，可通过 http://localhost:8888 访问。 | L2-1 · sources/l2-1_installation-docker.html:591 |
| 4 | `Two volumes are exposed that should be mounted to preserve its contents:` | 它暴露了两个应当挂载出来以保留其内容的卷。 | L2-1 · sources/l2-1_installation-docker.html:618 |
| 5 | `Remember to review the new templates for any changes that may affect your deployment, and update the .env file accordingly.` | 记得审阅新模板中对部署可能有影响的变更，并相应更新 .env 文件。 | L2-1 · sources/l2-1_installation-docker.html:534-535 |

[^c2-a]: Hermes Docs · Web Search · Option A — Self-host with Docker（`l3-1_web-search.md:149-181`）
[^c2-b]: SearXNG Docs · Installation with Docker · Compose instancing（`l2-1_installation-docker.html:490-528`；官方 compose `l2-2_container-docker-compose.yml`）
[^c2-c]: SearXNG 上游 `container/entrypoint.sh:80-93`（首启从 `settings.template.yml` 生成 `settings.yml` 并随机化密钥）
[^c2-d]: SearXNG Docs · Installation with Docker · Volumes（`l2-1_installation-docker.html:618-621`）
[^c2-e]: 官方 compose · `valkey` 服务（`l2-2_container-docker-compose.yml:18-24`）
[^c2-f]: 官方 compose · 配置挂载（`l2-2_container-docker-compose.yml:15`）
[^c2-g]: 官方 compose 端口默认（`l2-2_container-docker-compose.yml:12`）；`.env` 示例 `SEARXNG_PORT`（`l2-8_env.example:15`）
[^c2-h]: `container/.env.example` 三项默认全注释（`l2-8_env.example:9,12,15`）
[^c2-i]: SearXNG Docs · Installation with Docker · Environment variables（`l2-1_installation-docker.html:624-633`）
[^c2-j]: SearXNG 上游 `container/entrypoint.sh:114-124`（仅把纯数字的 `SEARXNG_PORT` 转成 `GRANIAN_PORT`）
[^c2-k]: SearXNG Docs · Installation with Docker · Docker Hub 限流与 GHCR 镜像（`l2-1_installation-docker.html:476-487`）
[^c2-p]: 出厂 `settings.yml` 注释说明 `base_url` 会被环境变量 `${SEARXNG_BASE_URL}` 覆盖（`l2-10_searx-settings-default.yml:92-93`）；Hermes 配方显式设置（`l3-1_web-search.md:173`）
