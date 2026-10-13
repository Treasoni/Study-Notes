<!-- SOURCE: 01_searxng-what.md | 8902 bytes -->
## 第 1 章：SearXNG 是什么：一句话看懂 + 隐私模型

### 1.1 一句话看懂

SearXNG 是一个「替你去搜、却不记你是谁」的搜索入口：你问它一句话，它替你同时去一批搜索服务各问一遍，再把结果汇总回来给你。[^c1-a] 而在那些搜索服务眼里，来问的是 SearXNG 这台机器，不是你。

它解决的是一个很具体的问题：你照样能用全网的搜索结果，但「你搜了什么、你是谁」不必交给每一家搜索公司。往下一步说——**自托管 SearXNG，就是把中间那个「替你跑腿的人」，从别人的服务器换成你自己机器上的一个实例**。后面五章要做的，全是在把这个「实例」立起来并接进 Hermes。

### 1.2 元搜索是什么（比喻先于术语）

先把 SearXNG 想成一个**只帮你跑腿、不留姓名的前台**。

你走到前台说「查一下 XXX」。前台自己不回答，而是同时派出一批跑腿的：去 Google 的窗口问一遍、去 Bing 的窗口问一遍、去维基的窗口问一遍……把各自递回来的纸条汇总成一份，再交给你。关键就在最后这一下——那些窗口对面看到的，是「前台派来的跑腿的」，**不是站在前台后面的你**。

所以：你拿到的是「多家结果的合集」（通常比只问一家更全），而搜索公司拿不到你的账号、IP 或浏览器指纹。这就是「元搜索」的全部直觉。

正式说法是 **metasearch engine（元搜索引擎）**：它自己几乎不建索引，而是把别家搜索引擎当数据源，统一提问、再把结果聚合起来。官方给的定位原话是：

> `SearXNG is a free internet metasearch engine … Users are neither tracked nor profiled.`[^c1-a]
> 中译：SearXNG 是一个免费的互联网元搜索引擎……用户既不被追踪，也不被画像。

> [!tip] 大白话
> 把 SearXNG 想成「一个只替你跑腿、不留姓名的前台」：好处是你一次能问到好几家，坏处是结果全要经过它转手——**所以接下来第 2 章才会强调「这台前台得是你自己的」**。

### 1.3 隐私模型：三次「脱敏」

SearXNG 保护隐私的总做法，官方概括成一句：把私人数据从「搜索请求」里**脱敏**，分三种形式来做。[^c1-b] 其中最日常的一条是——它**不把 cookie 发给外部搜索引擎，并且每个请求都换一个随机浏览器指纹**（browser profile）。[^c1-c] 也正因如此，请求是公共实例还是自建实例发的都无所谓，因为两种情况下它都已经匿名化了。[^c1-c]

还有一层容易被忽略：**出口 IP 用的是实例的 IP，不是你家的 IP**；官方也允许把这台实例再挂到代理或 Tor 后面。[^c1-d]

下面把「同一句搜索，各方分别看得见什么」摊开：

| 你的做法 | 搜索服务（Google / Bing 等）看得见 | 实例管理员看得见 |
| --- | --- | --- |
| 直接用普通搜索引擎 | 你的 IP、账号、cookie、查询词，也就是「你本人」 | （没有这个角色） |
| 走公共 SearXNG 实例 | 实例的 IP + 随机浏览器指纹，而不是「你」 | 你的查询词——你得信任这位管理员[^c1-e] |
| 自建 SearXNG 实例 | 实例的 IP + 随机浏览器指纹，而不是「你」 | 你的查询词，但这位管理员就是你自己 |

一句话概括：**三种做法里，搜索服务都只看到「实例」；差别只在中间那位管理员是不是你。**

> [!tip] 大白话
> 「脱敏」就是**寄信前把信封上你的地址撕掉、只留寄信局的地址**。收信人（Google）能收到信、能回信，但不知道其实是你写的；唯一还知道是你的人，是经手这封信的邮局——**所以邮局是谁，很重要**。

### 1.4 自建还是用别人的实例（谁值得信任）

看完上面那张表，取舍点就清楚了：公共实例的问题不在技术，而在**信任**。官方直说，用公共实例就必须信任它的管理员——你无从知道他有没有把你的请求记录、聚合甚至卖给别人。[^c1-e] 而一旦自建，「一切都在你手里：源代码、日志设置和私人数据」，也就不必再去信任任何陌生的管理员。[^c1-f]

补一个常被追问的规模问题：**SearXNG 本体目前支持 261 个搜索引擎，其中 81 个默认启用**。[^c1-g] 这两个数字只描述 SearXNG 本体；Hermes 文档另有一个口径不同的引擎数，留到第 4 章再说，**两者不要合并成一个数**。

它的许可方式是 **AGPL-3.0**：本项目以 GNU Affero 通用公共许可证授权。[^c1-h] 对自托管者来说，这意味着源码可查、可自行审阅。

> [!tip] 大白话
> 用公共实例像**借邻居家的 Wi-Fi 上网**——凑合能用，但流量从谁的路由器过，你并不清楚。自建则是自己拉一条线：麻烦一点，可这台路由器是你的。

### 1.5 名词扫盲表

| 名词 | 一句话解释 |
| --- | --- |
| 元搜索（metasearch） | 自己不建索引，转问别家再汇总结果——「替你跑腿的前台」 |
| 聚合器（aggregator） | 把多家结果合并成一份统一结果的组件 |
| 实例（instance） | 跑起来的一个 SearXNG 服务；公共实例人人可用，自建实例只有你能用 |
| 脱敏 | 把请求里的私人数据（cookie、指纹等）抹掉再转发 |
| AGPL-3.0 | 一种强 copyleft 开源许可：改动过、并对外提供服务的代码也要开源 |
| Tor | 一种匿名网络；SearXNG 可让出口流量经它转发，进一步隐藏来源 |

### 1.6 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `SearXNG is a free internet metasearch engine which aggregates results from up to … search services. Users are neither tracked nor profiled. Additionally, SearXNG can be used over Tor for online anonymity.` | SearXNG 是一个免费的互联网元搜索引擎，聚合来自多达若干家搜索服务的结果；用户既不被追踪，也不被画像；此外它还能经由 Tor 使用，以实现匿名。 | L1-1 · sources/l1-1_searxng-docs-index.rst:9-12 |
| 2 | `Removal of private data from search requests comes in three forms:` | 从搜索请求中移除私人数据，有三种形式。 | L1-2 · sources/l1-2_own-instance.rst:26 |
| 3 | `Removing private data means not sending cookies to external search engines and generating a random browser profile for every request. Thus, it does not matter if a public or private instance handles the request, because it is anonymized in both cases.` | 脱敏意味着不向外部搜索引擎发送 cookie，并为每个请求生成一个随机浏览器指纹；因此请求由公共还是私有实例处理都一样，因为两种情况都已匿名化。 | L1-2 · sources/l1-2_own-instance.rst:33-35 |
| 4 | `The IP address used will be the IP of the instance, but SearXNG can also be configured to use proxy or Tor.` | 使用的 IP 将是实例的 IP，但 SearXNG 也可配置为走代理或 Tor。 | L1-2 · sources/l1-2_own-instance.rst:36-37 |
| 5 | `If someone uses a public instance, they have to trust the administrator of that instance.` | 若有人使用公共实例，就必须信任该实例的管理员。 | L1-2 · sources/l1-2_own-instance.rst:48-49 |
| 6 | `everything is in their control: the source code, logging settings and private data. Unknown instance administrators do not have to be trusted.` | 一切都在他们掌控之中：源代码、日志设置与私人数据；也就不必去信任陌生的实例管理员。 | L1-2 · sources/l1-2_own-instance.rst:60-62 |
| 7 | `SearXNG supports 261 search engines of which 81 are enabled by default.` | SearXNG 支持 261 个搜索引擎，其中 81 个默认启用。 | L1-3 · sources/l1-3_configured_engines.html:449-450 |
| 8 | `This project is licensed under the GNU Affero General Public License (AGPL-3.0).` | 本项目以 GNU Affero 通用公共许可证（AGPL-3.0）授权。 | L1-5 · sources/l1-5_repo-readme.rst:61 |

[^c1-a]: SearXNG Docs · 首页（`docs/index.rst`）— https://docs.searxng.org
[^c1-b]: SearXNG Docs · Why use a private instance? — https://docs.searxng.org/user/own-instance.html
[^c1-c]: 同上（`own-instance.rst:33-35`）
[^c1-d]: 同上（`own-instance.rst:36-37`）
[^c1-e]: 同上（`own-instance.rst:48-49`）
[^c1-f]: 同上（`own-instance.rst:60-62`）
[^c1-g]: SearXNG Docs · Configured Engines — https://docs.searxng.org/user/configured_engines.html
[^c1-h]: 上游 `searxng/searxng` README — https://github.com/searxng/searxng
<!-- END: 01_searxng-what.md -->

<!-- SOURCE: 02_docker-setup.md | 11388 bytes -->
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
<!-- END: 02_docker-setup.md -->

<!-- SOURCE: 03_enable-json.md | 8027 bytes -->
## 第 3 章：开启 JSON API —— Hermes 的硬前提

### 3.1 结论先行：这一步不做，后面全白干

SearXNG 出厂只把结果输出成**网页**（`html`），而 Hermes 只吃 **JSON**。这两边对不上，第 4 章就会接不进去。所以这一章要做的就一件事：把 SearXNG 的 JSON 输出打开——**这一步不做，后面全部白搭**。而且它改的是配置文件——得打开 `settings.yml` 改一行、再重启容器让它生效。

### 3.2 概念：`settings.yml` 从哪来、怎么「只写覆盖」

SearXNG 启动时按固定顺序找它的配置文件 `settings.yml`：先看环境变量 `SEARXNG_SETTINGS_PATH` 指定的**完整路径**，没有就找 `/etc/searxng/settings.yml`；这两个都读不到，才回落到镜像自带的出厂文件。[^c3-a] 这就是为什么我们在第 2 章强调「容器里一定有一份 `/etc/searxng/settings.yml`」——首启时 entrypoint 已经替你生成好了。

关键心智模型是 `use_default_settings: true`：**打开它之后，你自己的 `settings.yml` 只需要写「要覆盖的那几项」，其余全部继承出厂默认**。[^c3-b] 官方安装模板里最简的 `settings.yml` 就短短几行：一个 `use_default_settings: true`，加一个 `server:` 块（`secret_key` 与 `image_proxy`）——注意它**没有** `search.formats`，这正是 JSON 默认关着的原因。[^c3-c]

实体落点：同一份 `settings.yml`，在容器里和宿主的哪个位置——改的时候两处都要对上：

| 位置 | 路径 |
| --- | --- |
| 容器内 | `/etc/searxng/settings.yml` |
| 宿主（路径① Hermes 配方） | `~/searxng/searxng/settings.yml` |
| 宿主（路径② 官方编排） | `./searxng/core-config/settings.yml` |

> [!tip] 大白话
> `use_default_settings: true` 就像**只填变更单**：出厂默认是一整套齐备的家具，你只在这张单子上写「多买一把椅子」，其余不用重抄一遍。所以改 JSON，只要在单子上补一行，不是把整份配置重写。

### 3.3 照抄：改配置 → 重启（本册两条路径都能省掉 `docker cp`）

> [!tip] 先说结论：本册两条路径都不用「取回 / 写回」
> 本册两条路径都把**宿主的一个目录挂到了容器的 `/etc/searxng/`**：路径① 挂的是 `~/searxng/searxng/`，路径② 挂的是 `./searxng/core-config/`。[^c3-j] 所以 `docker compose up -d` 起来之后，容器生成的那份 `settings.yml` **本来就落在你宿主上**——直接拿编辑器打开改就行，不需要先「取回来」。[^c3-k] 下面的 `docker cp` 只在**你没有把 `/etc/searxng` 挂到宿主**时才需要（那种情况下配置只活在容器里，复制出来改才不至于一重启就丢）。官方 Docker 安装文档里，路径② 的配置这步也是让你直接编辑 `core-config/settings.yml`，并没有 `docker cp`。[^c3-l]

**（可选）第一步，把容器里生成的配置取回宿主**——只有容器没把 `/etc/searxng` 挂到宿主时才需要（容器名按你的实际来：路径① 是 `searxng`，路径② 是 `searxng-core`）：[^c3-d]

```bash
docker cp searxng:/etc/searxng/settings.yml ~/searxng/searxng/settings.yml
```

**第二步，在文件里追加这段覆盖块**——`search.formats` 同时保留 `html` 并加上 `json`：[^c3-e]

```yaml
search:
  formats:
    - html
    - json
```

**第三步，文件的完整样子应该类似下面这样**（`use_default_settings: true` + 一个 `server:` 块 + 刚加的 `search:` 块），只要结构对上即可：[^c3-f]

```yaml
# ~/searxng/searxng/settings.yml
use_default_settings: true

server:
  secret_key: "abcdef12345678"
  image_proxy: true

search:
  formats:
    - html
    - json
```

**第四步，让它生效**——两条路径的配置文件已经是同一份，重启容器即可；只有你**真的**在第一步用 `docker cp` 把文件取出来过（未挂载的情况），才需要先写回、再重启：[^c3-g]

```bash
# 仅在未挂载、且前面确实用 docker cp 取出过时才需要这一行：
docker cp ~/searxng/searxng/settings.yml searxng:/etc/searxng/settings.yml
docker restart searxng
```

重启完成后，就能用第 5 章那条 `curl` 自检了。

### 3.4 最容易踩的坑：不开 JSON 就是 403

出厂 `settings.yml` 里 `search.formats` 只有一行 `- html`（上面那行 `# formats: [html, csv, json, rss]` 是**注释**，不生效）。[^c3-h] 结果就是：**不带 `format=json` 的请求会拿到 `403 Forbidden`**，因为那个格式是「未设置」的。[^c3-i]

所以以后一旦在第 4 章看到 `403`，第一反应就是回到 3.3 检查 `search.formats` 里到底有没有 `json`。

> [!warning] 公共实例尤其要注意
> 很多**公共** SearXNG 实例干脆禁用了这些机器可读格式，[^c3-i] 这也是官方建议生产环境自托管的原因之一。

### 3.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `If you want to consume the results as JSON, CSV, or RSS, you need to set the format parameter accordingly.` | 如果你想以 JSON、CSV 或 RSS 消费结果，就需要相应设置 format 参数。 | L2-6 · sources/l2-6_search_api.html:444-445 |
| 2 | `Requesting an unset format will return a 403 Forbidden error. Be aware that many public instances have these formats disabled.` | 请求一个未启用的格式会返回 403 Forbidden 错误；注意许多公共实例已禁用这些格式。 | L2-6 · sources/l2-6_search_api.html:446-448 |
| 3 | `SearXNG ships with JSON output disabled by default. Copy the generated config and enable it:` | SearXNG 出厂默认关闭 JSON 输出；把生成的配置复制出来并启用它。 | L3-1 · sources/l3-1_web-search.md:185 |
| 4 | `If use_default_settings: true is present, the file only contains your overrides. All other settings are inherited from the built-in defaults.` | 如果存在 use_default_settings: true，文件里就只包含你的覆盖项，其余设置都继承内置默认。 | L3-1 · sources/l3-1_web-search.md:193 |
| 5 | `You should see something like 10 results. If you get a 403 Forbidden, JSON format is still disabled — recheck step 4.` | 你应看到类似 10 results 的输出；若得到 403 Forbidden，说明 JSON 格式仍未启用——回去重查第 4 步。 | L3-1 · sources/l3-1_web-search.md:235 |

[^c3-a]: SearXNG Docs · settings.yml location（`l2-3_settings.html:451-457`）
[^c3-b]: SearXNG Docs · use_default_settings（`l2-3_settings.html:460-501`）
[^c3-c]: SearXNG 官方安装模板（`l2-7_settings.template.yml:1-8`，全文件无 `search.formats`）
[^c3-d]: Hermes Docs · Web Search · 第 4 步取回配置（`l3-1_web-search.md:187-189`）
[^c3-e]: Hermes Docs · Web Search · 追加的覆盖块（`l3-1_web-search.md:196-201`）
[^c3-f]: Hermes Docs · Web Search · 最简完整样例（`l3-1_web-search.md:205-219`）
[^c3-g]: Hermes Docs · Web Search · 写回并重启（`l3-1_web-search.md:223-225`）
[^c3-h]: 出厂 `settings.yml` 的 `search.formats` 仅 `- html`（`l2-10_searx-settings-default.yml:83-86`）
[^c3-i]: Search API 未设 format 返回 403，且许多公共实例禁用（`l2-6_search_api.html:444-448`）
[^c3-j]: 两条路径都把宿主目录挂到容器 `/etc/searxng`：路径① `l3-1_web-search.md:170-173`（`./searxng:/etc/searxng:rw`）；路径② `l2-2_container-docker-compose.yml:14-15`（`./core-config/:/etc/searxng/:Z`）
[^c3-k]: 首启会把模板生成进配置目录（`l2-9_entrypoint.sh:80-93`）——该目录正是挂载点，故生成物直接落在宿主
[^c3-l]: SearXNG 官方 Docker 安装文档 · 配置这步直接编辑宿主文件（`l2-1_installation-docker.html:527`）
<!-- END: 03_enable-json.md -->

<!-- SOURCE: 04_hermes-integration.md | 6043 bytes -->
## 第 4 章：接入 Hermes：把搜索后端指向本地实例

### 4.1 一句话看懂：一个环境变量就能接上

上一章开好了 JSON，这一章把 Hermes 的搜索后端指向你本机的实例。好消息是：**Hermes 侧唯一必需的设置就是一个环境变量 `SEARXNG_URL`**，指向你的实例地址即可，**不需要任何 API key**。[^c4-a] 源码里也印证了这一点——SearXNG provider 声明的「唯一必需环境变量」正是 `SEARXNG_URL`。[^c4-b]

### 4.2 概念：Hermes 怎么挑搜索后端

Hermes 选择「用哪个搜索引擎」有一套优先级：显式配置（`web.search_backend`）优先，其次是共享的 `web.backend`，最后才是**根据环境变量自动探测**。[^c4-c] 也就是说，只要你设了 `SEARXNG_URL`，即使不写任何配置，Hermes 也会自动认出 SearXNG。自动探测表节选如下：[^c4-d]

| 环境里有什么 | 自动选哪个后端 |
| --- | --- |
| `SEARXNG_URL` | `searxng` |
| `FIRECRAWL_API_KEY` 或 `FIRECRAWL_API_URL` | `firecrawl` |
| `TAVILY_API_KEY` | `tavily` |
| （什么都没设） | keyless ring：`exa` / `parallel` / `firecrawl` / `keenable` |

这里有个容易混淆的**口径**要单独说清。**Hermes 文档称它聚合 70+ 个搜索引擎**（这是 Hermes 自己的说法）；而 **SearXNG 本体的规模是第 1 章那个口径——261 个已配置、81 个默认启用**。两者**归属不同、不要合并成一个数字**，本文也只在讲 Hermes 定位时才提「70+」。

> [!tip] 大白话
> 「自动探测」就像**插上什么设备、系统自动切到哪个输入源**：你插了 `SEARXNG_URL` 这根线，Hermes 就自动把搜索切到 SearXNG，不用你去设置里挑。

### 4.3 动手：改 `.env` + `config.yaml`（或走 `hermes tools`）

**第一步，把实例地址写进 `~/.hermes/.env`**（端口必须与第 2 章的**宿主端口**一致）：[^c4-e]

```bash
# ~/.hermes/.env
SEARXNG_URL=http://localhost:8888
```

**第二步，在 `~/.hermes/config.yaml` 里把搜索后端指到 `searxng`**（顺带配好提取后端，见 4.4）：[^c4-f]

```yaml
# ~/.hermes/config.yaml
web:
  search_backend: "searxng"
  extract_backend: "firecrawl"   # 或 tavily / perplexity / keenable / exa / parallel
```

**第三步（替代写法），也可以走交互命令**——不用手改文件，直接在命令行里选：[^c4-g]

```bash
hermes tools
# 交互里选：Web Search & Extract → SearXNG
```

三条路等价，任选其一。接完后用第 5 章的 `curl` 自检即可确认通了。

### 4.4 关键分界：SearXNG 只负责「搜」

一定要记住这条边界：**SearXNG 只做搜索，不负责提取网页正文**。官方明确写了它是 search-only，`web_extract` 需要**另一个** provider。[^c4-a2] 源码 docstring 同样注明：它只是聚合上游引擎，**并不会去抓取 URL**。[^c4-h]

所以 `web_search`（搜索）可以由 SearXNG 承担，而 `web_extract`（取正文）要单独配一个 provider——就是 4.3 里那行 `extract_backend: "firecrawl"`。第 5 章会把这个边界讲透。

> [!warning] 别把「搜得到」当成「取得到」
> SearXNG 返回的是标题、链接和**摘要片段**，不是整页正文。[^c4-i] 想拿全文，得靠 `web_extract` 那一路。

### 4.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `SearXNG is a privacy-respecting, open-source metasearch engine that aggregates results from 70+ search engines. No API key required — just point Hermes at a running SearXNG instance.` | SearXNG 是一个尊重隐私的开源元搜索引擎，聚合来自 70+ 个搜索引擎的结果；无需 API key——只要把 Hermes 指向一个正在运行的 SearXNG 实例。（注：此处的「70+」是 Hermes 文档口径） | L3-1 · sources/l3-1_web-search.md:145 |
| 2 | `SearXNG is search-only — web_extract requires a separate extract provider.` | SearXNG 只做搜索——web_extract 需要单独的提取 provider。 | L3-1 · sources/l3-1_web-search.md:147 |
| 3 | `Search-only — SearXNG aggregates upstream engines but does not fetch URLs.` | 仅搜索——SearXNG 聚合上游引擎，但并不抓取 URL。 | L3-5 · sources/l3-5_provider.py:3 |
| 4 | `No API key required when using a public instance. Can also be self-hosted for full control.` | 使用公共实例时无需 API key；也可以自托管以获得完全掌控。 | L3-4 · sources/l3-4_searxng-search-SKILL.md:19 |
| 5 | `No content extraction: SearXNG returns snippets, not full page content. Use web_extract, browser tools, or curl for full articles.` | 不提供正文提取：SearXNG 返回的是摘要片段，而非整页内容；要取全文请用 web_extract、浏览器工具或 curl。 | L3-4 · sources/l3-4_searxng-search-SKILL.md:166 |

[^c4-a]: Hermes Docs · Web Search · SearXNG 定位（`l3-1_web-search.md:145`）
[^c4-a2]: Hermes Docs · Web Search · 「search-only」边界（`l3-1_web-search.md:147`）
[^c4-b]: Hermes 源码 · `plugins/web/.../searxng.py` 的 `KEY_ENV`（`l3-5_provider.py:20-22`）
[^c4-c]: Hermes Docs · Web Search · 后端优先级（`l3-1_web-search.md:426-431`）
[^c4-d]: Hermes Docs · Web Search · 自动探测表（`l3-1_web-search.md:437-449`）
[^c4-e]: Hermes Docs · Web Search · 第 7 步 `SEARXNG_URL`（`l3-1_web-search.md:239-241`）
[^c4-f]: Hermes Docs · Web Search · `search_backend` / `extract_backend`（`l3-1_web-search.md:246-249,275-279`）
[^c4-g]: Hermes Docs · CLI · `hermes tools`（`l3-3_cli-commands.md:99`）；交互入口（`l3-1_web-search.md:251`）
[^c4-h]: Hermes 源码 · `l3-5_provider.py:1-3`
[^c4-i]: SearXNG Search Skill · Limitations（`l3-4_searxng-search-SKILL.md:165-169`）
<!-- END: 04_hermes-integration.md -->

<!-- SOURCE: 05_verify-troubleshoot.md | 7415 bytes -->
## 第 5 章：验证与排错：curl、403 与 extract 边界

### 5.1 一句话看懂：一条 curl 就知道接得对不对

前面三章把实例搭起来、开了 JSON、接上了 Hermes。这一章只解决最后一件事：**怎么确认真的接通了**。答案是——不用猜，一条 `curl` 命令就能给出裁决。它打印出一串结果条数，就说明三层全对了：容器在跑、JSON 开着、地址与端口跟 Hermes 配的一致；如果返回 `403` 或者干脆连不上，下面那张症状表能直接把你送到该回头看的章节。

### 5.2 自检：期望输出长什么样

把下面这条命令整段复制进终端（端口用你在第 2 章用的**宿主端口**，这里以 8888 为例）：[^c5-a]

```bash
curl -s "http://localhost:8888/search?q=test&format=json" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(f'{len(d[\"results\"])} results')"
```

命中时它会打印出一个数字，形如 `10 results`。**这个数字就是「JSON 通了」的铁证**。官方原话说得很直白：你应当看到类似 10 results 的输出；若拿到 `403 Forbidden`，说明 JSON 格式仍未启用，回去重查开 JSON 的那一步。[^c5-a]

为什么这一条命令能一锤定音？因为它恰好踩在前后端唯一的接口面上：SearXNG 的搜索 API 只有两个端点，`/` 和 `/search`，两者都接受 GET 与 POST；而结果格式由请求里的 `format` 参数决定，不指定、或指定了一个没启用的格式，都会被拒。[^c5-b]

> [!tip] 大白话
> 这条 `curl` 就是**给实例打个电话问「在吗？」**，它回你一句「10 results」。回得出话，说明四件事同时成立：电话线（宿主端口）通了、号码（`SEARXNG_URL`）对了、对方开着机（容器在跑）、对方听得懂你的方言（`json` 格式已启用）。

还有三个容易忽略的小坑，一并记住：[^c5-g] 一是**查询词里带空格或特殊字符时要 URL 编码**（命令行里手敲容易忘，脚本里用 `urllib.parse.quote()`）；二是**`SEARXNG_URL` 必须设**，没设的话整个后端都不工作；三是**给请求设超时**（`curl --max-time`，或 Python 侧传 `timeout=`），否则实例不可达时命令会一直挂在那里等。

### 5.3 症状 → 病因 → 处置（对照表）

所有「没接上」的表现，基本能归成下面五类。先看现象，再照「处置」列动手：[^c5-c]

| 症状 | 病因 | 处置 |
| --- | --- | --- |
| `403 Forbidden` | JSON 格式没开 | 回第 3 章，把 `search.formats` 补上 `json` |
| `Connection refused` | 容器没起，或 URL 写错 | 先看容器是否在跑；再核对 `SEARXNG_URL` 与**宿主端口**一致 |
| 空结果（`0 results`） | 该实例挡住了这条查询 | 换个实例，或自建 |
| 响应很慢 | 公共实例过载 | 自建，或换一个更闲的实例 |
| `json` 格式不支持 | SearXNG 版本太旧 | 改用 `format=rss`，或升级 SearXNG |

`403` 这一条要单独强调：它**不是命令写错**，而是第 3 章那一步没做或没生效——回去看 `search.formats` 里到底有没有 `json` 即可；同时留意，很多**公共**实例本就把这些格式关掉了。[^c5-b]

如果连症状都拿不到（命令卡住、容器像没反应），先看日志、必要时进容器里查：[^c5-f]

```bash
# 路径②（官方编排，服务名是 core）
docker compose logs -f core
# 路径①（Hermes 单服务，容器名是 searxng）
docker container logs -f searxng
```

```bash
# 需要进容器内部排查时（以官方编排的 core 为例）
docker compose exec -it --user root core /bin/sh -l
```

### 5.4 边界：`web_extract` 不走 SearXNG

这是全篇最容易被误解、也最该钉死的一条边界：**SearXNG 只负责「搜」，不负责「取正文」**。三处互相独立的来源口径一致——官方文档明写它是 search-only、`web_extract` 需要另外的 extract provider；源码 docstring 也说它只是聚合上游引擎、并不去抓取 URL；Skill 文档同样标注它只回摘要片段、不返回整页正文。[^c5-d]

所以第 4 章那一行 `extract_backend: "firecrawl"` 不是锦上添花，而是「想拿到全文」的必经之路。**搜得到 ≠ 取得到正文**。[^c5-e]

> [!warning] 别把两种能力混为一谈
> SearXNG 返回的只有标题、链接和**摘要片段**；要整页正文，得走另一个 provider（如 `firecrawl`）。
> 这是两条独立链路——接上 SearXNG，并不会顺带把正文提取也解决掉。

### 5.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `You should see something like 10 results. If you get a 403 Forbidden, JSON format is still disabled — recheck step 4.` | 你应当看到类似 10 results 的输出；若得到 403 Forbidden，说明 JSON 格式仍未启用——重查第 4 步。 | L3-1 · sources/l3-1_web-search.md:235 |
| 2 | `SearXNG supports querying via a simple HTTP API. Two endpoints, / and /search, are supported for both GET and POST methods.` | SearXNG 支持通过一个简单的 HTTP API 查询；支持 `/` 与 `/search` 两个端点，均接受 GET 与 POST 方法。 | L2-6 · sources/l2-6_search_api.html:440-441 |
| 3 | `Requesting an unset format will return a 403 Forbidden error. Be aware that many public instances have these formats disabled.` | 请求一个未启用的格式会返回 403 Forbidden 错误；注意许多公共实例已禁用这些格式。 | L2-6 · sources/l2-6_search_api.html:446-448 |
| 4 | `Search-only — SearXNG aggregates upstream engines but does not fetch URLs.` | 仅搜索——SearXNG 只聚合上游引擎，并不抓取 URL。 | L3-5 · sources/l3-5_provider.py:3 |
| 5 | `No content extraction: SearXNG returns snippets, not full page content. Use web_extract, browser tools, or curl for full articles.` | 不提供正文提取：SearXNG 返回的是摘要片段而非整页内容；要取全文请用 web_extract、浏览器工具或 curl。 | L3-4 · sources/l3-4_searxng-search-SKILL.md:166 |
| 6 | `Public instances have rate limits, variable uptime, and may disable JSON format at any time. For production use, self-hosting is strongly recommended.` | 公共实例有限流、可用性波动，且可能随时禁用 JSON 格式；生产环境强烈建议自托管。 | L3-1 · sources/l3-1_web-search.md:265 |

[^c5-a]: Hermes Docs · Web Search · 第 6 步自检（`l3-1_web-search.md:228-235`）
[^c5-b]: Search API · 两端点与未设 format 返回 403（`l2-6_search_api.html:439-448`）
[^c5-c]: SearXNG Search Skill · Troubleshooting 表（`l3-4_searxng-search-SKILL.md:171-179`）
[^c5-d]: 三证：官方 search-only（`l3-1_web-search.md:147`）；源码 docstring（`l3-5_provider.py:1-3`）；Skill Limitations（`l3-4_searxng-search-SKILL.md:163-169`）
[^c5-e]: SearXNG Search Skill · No content extraction（`l3-4_searxng-search-SKILL.md:166`）
[^c5-f]: 看日志 / 进容器排查（`l2-1_installation-docker.html:559,563,601`）
[^c5-g]: SearXNG Search Skill · Pitfalls（`l3-4_searxng-search-SKILL.md:181-184`）
<!-- END: 05_verify-troubleshoot.md -->

<!-- SOURCE: 06_advanced.md | 7223 bytes -->
## 第 6 章：进阶可选：引擎裁剪、端口、升级与公共实例

> [!tip] 新手可跳过
> 这一章是**可选加深**：前五章已经能让你跑通并接上 Hermes。这里只点到「能自洽使用」的程度，不讲生产部署的完整教程。照抄默认值也能用，读这一章是为了让你知道**还能往哪些方向调**。

### 6.1 改端口与暴露方式

端口这件事在第 2.5 节已经钉死，这里原样复述、不改写：

> **一句话钉死：容器内一律 8080；8888 要么是宿主映射端口、要么是裸机出厂默认**；`SEARXNG_URL` 必须与宿主端口一致。

在这一口径之上，裸机出厂 `settings.yml` 里有四个 `server:` 项可以被对应环境变量覆盖，等于给了你四个「不改文件、只改 `.env`」的调节旋钮：[^c6-a]

| 出厂配置项 | 含义 | 被哪个环境变量覆盖 |
| --- | --- | --- |
| `port`（出厂 8888） | 监听端口 | `${SEARXNG_PORT}` |
| `bind_address`（出厂 `"127.0.0.1"`） | 绑定地址 | `${SEARXNG_BIND_ADDRESS}` |
| `base_url`（出厂 `false`） | 对外公开的 URL | `${SEARXNG_BASE_URL}` |
| `limiter`（出厂 `false`） | 限流、拦部分机器人 | `${SEARXNG_LIMITER}` |

其中 `base_url` 的边界要按第 2 章的口径理解：它**是官方支持的覆盖项**（由 `settings.yml` 的 `base_url` 被环境变量覆盖），但**官方 compose 并未启用它**，是 Hermes 配方**显式设置**的。

> [!tip] 大白话
> 这四个旋钮就像**空调面板**：机器内部有一份默认设定（`settings.yml` 里写死的 8888 / 127.0.0.1），但墙上那排按钮（`SEARXNG_*` 环境变量）能直接盖过它——你一般只按按钮，不用拆开机器改焊点。

### 6.2 裁剪引擎

SearXNG 默认启用的引擎很多（本体规模见第 1 章：261 个已配置 / 81 个默认启用）。如果你只想用其中几个、或者想屏蔽某个不喜欢的引擎，可以用两条互补的路子，在 `settings.yml` 里二选一：[^c6-b]

```yaml
# 在 settings.yml 里，两种写法二选一

# 方式 A：从默认引擎里「移除」某个（示例：移除 google）
use_default_settings:
  engines:
    remove:
      - google

# 方式 B：只「保留」指定的几个引擎（示例：只留 google 与 duckduckgo）
use_default_settings:
  engines:
    keep_only:
      - google
      - duckduckgo
```

两条路的取舍其实很简单：

| 你的需求 | 用哪个 | 怎么想 |
| --- | --- | --- |
| 想屏蔽某几个引擎，其余照旧 | `engines.remove` | 黑名单：列出**不要**的 |
| 想只留少数引擎，其余都不要 | `engines.keep_only` | 白名单：列出**只要**的 |

记住一件事：**某个引擎到底能不能用，取决于这台实例的配置**——同一个引擎，在别人的实例上开着、在你的实例上可能被禁用。所以「搜不到某个来源」时，先想想是不是它被你（或实例）裁掉了。[^c6-c]

### 6.3 升级与固定版本

官方编排默认用的是滚动镜像标签 `${SEARXNG_VERSION:-latest}`：不指定版本时，`pull` 到的永远是最新镜像。[^c6-d] 想升级服务，标准三步是「停 → 拉新 → 起」：[^c6-e]

```bash
docker compose down
docker compose pull
docker compose up -d
```

如果你更想要**可复现**的部署（比如怕某天新版本改了行为），就在 `.env` 里钉一个具体版本号，镜像标签里那个文档给过的例子长这样：[^c6-f]

```bash
# ~/searxng/.env（或官方编排目录下的 .env）
SEARXNG_VERSION=2026.3.25-541c6c3cb
```

顺带说清 `valkey`：**官方编排里确实带了一个 `valkey` 缓存服务，但最小可用不需要它**。这里只做事实陈述，不判定它「必需」还是「不必需」——你按官方模板照跑，它就是编排的一部分。

### 6.4 自建 vs 公共实例

前面一直默认你走自建（Option A）。如果你动过「直接蹭一个公共实例」的念头，先看官方给的这一段警示：公共实例有限流、可用性会波动，还可能**随时把 JSON 格式关掉**；因此生产环境强烈建议自托管。[^c6-g]

还有一条更底层的理由：**没有防护的公共实例，其搜索服务更容易被滥用**，结果就是上游服务对这台实例抛出 CAPTCHA、甚至封掉它的 IP，于是所有经它发出的查询都只会返回更少的结果。[^c6-h]

所以真要临时用公共实例，正确姿势是**只挑那些明确开了 JSON 格式的**（官方目录在 searx.space，可按此过滤），并且接受「它随时可能变」这个前提。换句话说，公共实例适合救急，不适合长期依赖。

> [!warning] 别把公共实例当默认方案
> 你没法控制别人的实例：它可能限你的流、可能今天开着 JSON 明天关掉。要稳定，自建才是终点。

### 6.5 引文对照（原文 / 中译 / 出处）

> 「出处」列写 `来源ID · sources/文件名:行`。本章每条引文都查得到具体来源，因此**没有用到 `—`**（`—` 表示「来源不明、宁空不猜」）。本章所引来源快照的取回日期均为 2026-10-07。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `It is possible to remove some engines from the default settings.` | 可以从默认设置里移除一些引擎。 | L2-3 · sources/l2-3_settings.html:502 |
| 2 | `As an alternative, it is possible to specify the engines to keep. In the following example, SearXNG has only two engines:` | 作为一种替代方案，可以指定要保留的引擎；在下面的例子里，SearXNG 只保留两个引擎。 | L2-3 · sources/l2-3_settings.html:517 |
| 3 | `public instances without proper protection are more vulnerable to abuse of the search service, which may cause the external service to enforce CAPTCHAs or to ban the IP address of the instance.` | 缺乏恰当防护的公共实例，其搜索服务更容易被滥用，进而可能招致上游服务对其实施 CAPTCHA 校验、或封禁该实例的 IP 地址。 | L1-2 · sources/l1-2_own-instance.rst:52-55 |
| 4 | `Public instances have rate limits, variable uptime, and may disable JSON format at any time. For production use, self-hosting is strongly recommended.` | 公共实例有限流、可用性波动，且可能随时禁用 JSON 格式；生产环境强烈建议自托管。 | L3-1 · sources/l3-1_web-search.md:265 |

[^c6-a]: 出厂 `settings.yml` 的 `server:` 覆盖项（`l2-10_searx-settings-default.yml:88-97`）
[^c6-b]: SearXNG Docs · settings · `engines.remove` / `engines.keep_only`（`l2-3_settings.html:502-533`）
[^c6-c]: SearXNG Search Skill · Engine coverage（`l3-4_searxng-search-SKILL.md:168`）
[^c6-d]: 官方 compose · 镜像 `${SEARXNG_VERSION:-latest}`（`l2-2_container-docker-compose.yml:9`）
[^c6-e]: SearXNG Docs · Installation with Docker · 升级服务（`l2-1_installation-docker.html:545-549`）
[^c6-f]: `container/.env.example` · 钉版本标签（`l2-8_env.example:8-9`）
[^c6-g]: Hermes Docs · Web Search · 公共实例 caution（`l3-1_web-search.md:255-266`）
[^c6-h]: SearXNG Docs · Own Instance · 公共实例被滥用风险（`l1-2_own-instance.rst:52-55`）
<!-- END: 06_advanced.md -->
