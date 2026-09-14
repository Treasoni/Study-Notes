# 附录 B 进阶配置（可跳读）

> [!note] 这是可选阅读
> 按第二章的三卷 Compose 跑起来、需求只在"刮削 + 改标签 + 整理"的话，本附录**现在不用看**。它收五类进阶动作：切 MySQL、接外置 Redis、改服务端口、容器自动更新与三种升级方式、多目录独立挂载，末尾附升级前检查清单。

## B.1 切换到 MySQL（解决 `sqlite database is locked`）

MySQL 页开篇原文：「本项目默认采用Sqlite数据库，sqlite 在并发写入时容易出现sqlite database is locked，因此支持提供替换成为 msyql 数据库」（末词 "msyql" 为原文拼写）[^cB-n6]。该页每个 `MYSQL_*` 变量都注明「（没有可以不填，默认使用 sqlite）」——MySQL 是**替换项**，不是必需项[^cB-n6]。

> [!tip] 大白话
> Sqlite 像**一本只有一支笔的账本**：同一时刻只能一个人写，第二个来写就得等，等不到就报 "database is locked"；MySQL 像**银行柜台**，多人各写各的。只有多个任务会同时写（后台刮削与手动编辑撞车）时，换它才划算。

### 方法一（推荐）：一个 yaml 起两个容器

原文：「在一个 yaml 文件中部署 MySQL 和 Music Tag Web 两个容器。」[^cB-n6] 这份可直接跑，替换三处（密码、音乐目录、配置目录）即可。

```yaml
version: '3'

services:
  db:
    image: mysql:latest
    container_name: mysql
    restart: always
    command:
      --character-set-server=utf8mb4
      --collation-server=utf8mb4_unicode_ci
    environment:
      MYSQL_ROOT_PASSWORD: your_root_password  # ← 改成你自己的强密码
      MYSQL_DATABASE: music_tag  # 数据库名称，无需修改
    volumes:
      - ./mysql-data:/var/lib/mysql

  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"  # 主机端口:容器端口
    volumes:
      - /path/to/your/music:/app/media  # ← 改成你的音乐文件目录
      - /path/to/your/config:/app/data  # ← 改成你的配置文件目录
    environment:
      - MYSQL_HOST=db  # 数据库主机名，使用服务名, 不需要修改
      - MYSQL_PASSWORD=your_root_password  # 与上面的 MySQL 密码一致
      - MYSQL_DB_NAME=music_tag  # 数据库名称，无需修改
      - MYSQL_USER=root
      - MYSQL_PORT=3306
      - WORKER_NUM=8  # 后台任务线程数
    restart: always
    depends_on:
      - db
```

启动用 `docker-compose up -d`，验证是「打开浏览器，访问 `http://你的服务器IP:8002`」[^cB-n6]。注意 `MYSQL_HOST=db` 填的是 **MySQL 的服务名**而非 IP；原文另提示「首次部署时，建议**不额外修改任何默认配置**」[^cB-n6]。

### 方法二：分开部署

原文写的是「分开部署 mysql 和 music tag web 容器」[^cB-n6]。先单独起 MySQL：

```bash
docker run -p 3306:3306 --name mysql \
  -v /your/mysql/data:/var/lib/mysql \
  --restart=always \
  -e MYSQL_ROOT_PASSWORD=your_root_password \
  -e MYSQL_DATABASE=music_tag \
  -d mysql:latest
```

再停掉原有容器、加上 `MYSQL_*` 变量重启它；原文补了一句「/app/media 和/app/data 文件目录不需要删除。」[^cB-n6] 页内变量说明为：`MYSQL_HOST` 填 mysql 的局域网 IP，`MYSQL_PASSWORD` 填上文配置的那个密码，`MYSQL_DB_NAME` 填数据库名，`MYSQL_USER` 默认为 root，`MYSQL_PORT` 默认端口为 3306[^cB-n6]。

> [!warning] 同一变量在页内有两种叫法
> `MYSQL_DB_NAME` 在方法一注释里叫「数据库名称，无需修改」，方法二注释里却叫「数据表名称（没有可以不填，默认使用 sqlite）」[^cB-n6]，二者并不等价。按它与 `MYSQL_DATABASE: music_tag` 的对应关系，理解成**数据库名**、值保持 `music_tag`。

### 配完打不开？官方 5 条自查

原页「配置完成后打不开 music tag web？」给出 5 条[^cB-n6]：MySQL 端口是否暴露；music tag web 是否能访问到 mysql；原先已有 mysql 时是否建了 `music_tag` 数据库；配置是否拼写错误；mysql 版本太新可用 `mysql:5.7`。原页称其「基本能解决 90% 的问题了」。

> [!note] 本节空白
> 从 Sqlite 切到 MySQL 时**原有数据是否迁移、怎么迁移，N6 全页未说明**（`未取到`）。动手前请把 `/app/data` 整体备份一份；本笔记不做推断。

## B.2 接外置 Redis

外置 Redis 页首段：「容器本身就会启动一个 redis，如果你不需要**外置**的 redis，可以不进行此项的配置。」[^cB-n7] 即**不配置是默认状态**，只有服务器上已有 Redis 想复用时才需要往下看。

> [!tip] 大白话
> Redis 像**前台那块便签板**：常用信息抄在板上，取用快，断电就没了，真正的账本在数据库里。容器自带一块够用；你已有自己的板子，就让容器指向它。

**方法一（复用已有 Redis）**：原文要求在环境变量添加 `REDIS_HOST`，其默认端口为 6379；要改用其他端口时需同时设置 `REDIS_PORT`。`REDIS_HOST` 可以是局域网 IP，也可以是容器网络里的连接地址；若 Redis 设了密码，还需配置 `REDIS_PASSWORD`[^cB-n7]。

**方法二（一起写进 compose）**：原文是「在一个yaml 文件中一起部署 redis 和 music tag web」[^cB-n7]：

```yaml
version: '3'

services:
  redis:
    image: redis:latest
    container_name: redis
    restart: always
    ports:
      - "6379:6379"  # 主机端口:容器端口
    command: redis-server --requirepass yourpassword  # 设置密码

  music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8002:8002"
    volumes:
      - /path/to/your/music:/app/media  # ← 改成你的音乐文件目录
      - /path/to/your/config:/app/data  # ← 改成你的配置文件目录
    environment:
      - REDIS_HOST=redis  # 使用服务名, 不需要修改
      - REDIS_PASSWORD=yourpassword  # 与上面的 redis 密码一致
      - REDIS_PORT=6379
    restart: always
    depends_on:
      - redis
```

`REDIS_HOST=redis` 同样是**服务名**；密码在 Redis 侧由 `command: redis-server --requirepass yourpassword` 设定，再用 `REDIS_PASSWORD` 传给 Music Tag Web，两处必须一致[^cB-n7]。

> [!warning] `REDIS_PORT` 的默认值，文档给了两个
> 自定义端口页（N8）表格中 `REDIS_PORT` 既写默认「6379」，又备注「选填，v2.6.0 及以上版本默认 6380」[^cB-n8]；外置 Redis 页（N7）正文则写「其默认端口为 6379」[^cB-n7]。两说并存，**取哪个取决于版本是否为 v2.6.0 及以上**，本笔记无法确认你手上镜像的实际默认值。稳妥做法：显式写出 `REDIS_PORT`。

> [!note] 本节空白
> 切换到外置 Redis 之后，原有缓存/数据是否重建、有无副作用，N7 全页未说明（`未取到`）。

## B.3 自定义服务端口（host / bridge 两种改法）

自定义端口页首句：「如果你使用网络模式host，出现端口冲突，可以进行自定义端口号」[^cB-n8]——host 模式下容器直接占用宿主机 8001 / 8002 / 9001，被占了就起不来。

「二、核心环境变量说明（容器内端口）」的表[^cB-n8]：

| 环境变量 | 作用说明 | 默认值 | 特殊说明 |
| --- | --- | --- | --- |
| `GUNICORN_PORT` | 后端服务端口 | 8001 | 选填 |
| `NGINX_PORT` | Nginx 代理后的后端服务端口 | 8002 | 选填 |
| `SUPERVISOR_PORT` | Supervisor 进程管理端口 | 9001 | 选填 |
| `REDIS_PORT` | Redis 服务端口 | 6379 | 选填，v2.6.0 及以上版本默认 6380 |

原文说明这些变量修改后「仅影响容器内部，不直接映射到主机」[^cB-n8]。

**host 模式（原文标为"推荐修改方式"）**：「直接在 `environment` 中添加需自定义的端口变量，无需修改 `ports` 配置。」[^cB-n8]

**bridge 模式（原文标为"特殊情况修改"）**：「一般无需修改容器内端口，仅需在 `ports` 中映射主机端口即可」；若确要改容器内端口，两个条件必须同时满足——改 `environment` 里对应变量（如 `GUNICORN_PORT`），并在 `ports` 中同步映射新的容器内端口（如 `"8006:8006"`）[^cB-n8]。**少改任意一处都接不上。**

> [!tip] 大白话
> 端口像**门牌号**。host 模式是"你家门牌直接挂在街上"，号被占了就得换；bridge 模式是"你家在小区里，大门另有对外门牌"——外面换号不影响屋里，**屋里换号则内外两块牌子必须同时换**，否则快递（请求）送不到门口。

原页「四、完整配置示例」把主机与容器内端口改成 8006、另设 `GUNICORN_PORT=8003`，并注明 `ports` 的容器内端口要「与NGINX_PORT保持一致」[^cB-n8]：

```yaml
music-tag:
    image: xhongc/music_tag_web:latest
    container_name: music-tag-web
    ports:
      - "8006:8006"  # 主机端口:容器内端口（与NGINX_PORT保持一致）
    volumes:
      - /path/to/your/music:/app/media
      - ./config:/app/data
    environment:
      - WORKER_NUM=8
      - GUNICORN_PORT=8003  # 自定义后端服务端口
      - NGINX_PORT=8006  # 与 ports 映射的容器内端口一致
      - SUPERVISOR_PORT=9001  # 保持默认或按需修改
    restart: always
    depends_on:
      - db  # 依赖MySQL服务，确保先启动数据库
```

该示例原文没有顶层 `version:` / `services:` 包裹，服务名直接写 `music-tag`，并带 `depends_on: db`——它本是 MySQL 方案的一部分，单独抄用需补回外层结构并删掉 `depends_on`。

> [!note] 本节空白
> 三个端口变量**是否必须保持特定关系，N8 未说明**（`未取到`）；能确认的只有示例做法：`NGINX_PORT` 与 `ports` 里的容器内端口取同一值。

## B.4 自动更新、定时更新与三种升级方式

### B.4.1 一键更新与 Docker Socket 前提

自动更新页声明其可自动完成：「下载最新版本的程序 / 停止旧版本容器 / 启动新版本容器 / 清理旧版本镜像，释放磁盘空间 / 保留你的所有数据和配置」[^cB-n9]。入口是登录后左侧菜单「系统设置」→「系统信息」，在「系统版本」区域点「检查更新」，再「确认容器名称（通常默认为 `music-tag-web`）」[^cB-n9]。

前提原文加重语气：「**如果你想使用自动更新功能，在首次部署时必须挂载 Docker Socket。**」[^cB-n9] 对应一行挂载：

```yaml
      - /var/run/docker.sock:/var/run/docker.sock
```

未挂载时原页列出的表现有「Docker客户端初始化失败」「无法连接到 Docker daemon」「更新按钮点击后没有反应」[^cB-n9]。检查是否挂上，原文给两法[^cB-n9]：

```bash
# 方法 1：看容器配置里的挂载项
docker inspect music-tag-web | grep docker.sock
# 期望看到："Source": "/var/run/docker.sock", "Destination": "/var/run/docker.sock"

# 方法 2：进容器里看 socket 文件是否存在
docker exec -it music-tag-web bash
ls -l /var/run/docker.sock
# 期望看到：srw-rw---- 1 root docker 0 Dec  2 10:00 /var/run/docker.sock
```

> [!tip] 大白话
> Docker Socket 像**整栋楼的总电闸钥匙**。容器本只能用自己屋里的插座；挂上 socket 等于把总闸钥匙交给它，它才能开关别的容器、拉删镜像——自动更新靠的正是这个"越权"。代价是：能进容器的人就握有宿主机 Docker 的控制权。

### B.4.2 定时更新：两种 Watchtower 用法

方法 1，系统 crontab（示例为每天凌晨 3 点跑一次）[^cB-n9]：

```bash
crontab -e
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music-tag-web
```

方法 2，常驻 Watchtower（`--interval 86400` 表示每 24 小时检查一次，`--cleanup` 表示自动清理旧镜像）[^cB-n9]：

```bash
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \
  --interval 86400 \
  music-tag-web
```

两条命令末尾的 `music-tag-web` 都是**要监控的容器名**；网络受限时，官方给的替代镜像是 `registry.cn-hangzhou.aliyuncs.com/xhongc/watchtower:latest`[^cB-n9]。

> [!warning] 容器名对不上，Watchtower 就白跑
> 更新页与 `docker run` 场景用 `music-tag-web`[^cB-n9]，升级页的 Watchtower 示例末尾却写 `music_tag_web`（下划线）[^cB-f4]。**命令末尾必须换成你机器上真实的容器名**，用 `docker ps` 的 `NAMES` 列确认[^cB-n9]。名字写错时它不报错、也不更新，最难发现。

### B.4.3 三种升级方式（含 `down -v` 警告）

升级页开头写「提供3种方式进行更新」：docker pull、Docker Compose、watchtower[^cB-f4]。

**方式一 `docker pull` 后重建**：先拉新镜像，再「停止正在运行的旧版容器，并将其删除」，最后「使用快速开始中的命令用新镜像重新部署」[^cB-f4]：

```bash
docker stop my-music-tag-web   # ← 换成你的容器名
docker rm my-music-tag-web
```

**方式二 Docker Compose**：原文说 Compose「可以自动处理容器的停止、删除和重新创建」，步骤为「拉取新镜像：`docker-compose pull`」+「更新并重启服务：`docker-compose up -d`」[^cB-f4]。

> [!warning] `docker-compose down -v` 会连卷一起删
> 原页区分了两条命令：`docker-compose down` 只清理「容器、网络但不包括卷（数据持久化存储）」；「若要连同卷一起删除，请添加 -v 选项：`docker-compose down -v`」。紧接的提醒是「确保所有重要数据都已正确挂载到持久化存储上，防止数据丢失。」[^cB-f4] 除非你确定数据都挂在宿主机目录且另有备份，**不要用 `-v`**：卷一删，`/app/data` 里的配置、数据库与激活信息一并没了。

**方式三 watchtower 一次性更新**：「`docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower --cleanup --run-once music_tag_web`」，末尾换成你自己的容器名[^cB-f4]。

> [!warning] 升级示例里的镜像名少了个 `c`
> 升级页示例写 `docker pull xhong/music_tag_web:2.0.1`[^cB-f4]，正确的仓库名是 `xhongc/music_tag_web`[^cB-n6][^cB-n7][^cB-n9]。照抄升级页会**拉不到镜像**。页面里的 `2.0.1` 只是「假设我们想要更新到版本 2.0.1」的举例[^cB-f4]；**当前最新版本号本笔记无法确认**（`未取到`，官方站内也没有 changelog 页）。

### B.4.4 服务名不一致：抄哪份 yaml 就按哪份的服务名

| 出处 | 服务名 | `container_name` |
| --- | --- | --- |
| MySQL 页 方法一 / 方法二 | `music-tag` | `music-tag-web` |
| 外置 Redis 页 方法二 | `music-tag` | `music-tag-web` |
| 自定义端口页 示例 | `music-tag` | `music-tag-web` |
| 自动更新页 首段 yaml | `music-tag-web` | `music-tag-web` |
| 自动更新页「确保数据持久化」片段 | `web` | （未写） |

**服务名在官方各页之间不统一，同一页内也会变**[^cB-n6][^cB-n7][^cB-n8][^cB-n9]。`depends_on` 与 `docker-compose up <name>` 里的名字，必须和自己 yaml 的服务名逐字一致。

### B.4.5 更新耗时与中断

原页「更新需要多长时间？」写「**通常 1-5 分钟**」，并提示「更新期间服务会短暂中断，建议在低峰时段进行」[^cB-n9]；但同页「步骤 2：执行更新」写的是「等待更新完成（通常需要 1-3 分钟）」[^cB-n9]。

> [!note] 两个数字并列，不合并
> 同一页给出「1-3 分钟」与「1-5 分钟」两种耗时，官方未说明适用条件差异，本笔记**并列保留两个说法**。原页另提到新版本镜像「通常在 500MB-1GB」[^cB-n9]。

## B.5 多目录独立挂载

原页定位：「将多个音乐库目录添加到容器中，实现灵活管理且避免路径冲突」，适合音乐分散在多个文件夹的用户[^cB-f6]。做法是在 `docker-compose.yml` 的 `volumes` 段按分类逐行添加[^cB-f6]：

```yaml
volumes:
  # 流行音乐库
  - /path/to/your/pop_music:/app/media/Pop
  # 摇滚音乐库
  - /path/to/your/rock_music:/app/media/Rock
  # 古典音乐库
  - /path/to/your/classical_music:/app/media/Classical
  # - /path/to/another_music:/music/AnotherCategory
```

原页解释：左侧「是你本地计算机上的实际音乐文件夹路径」，右侧「是容器内的路径，按音乐类别进行分类」[^cB-f6]；改完执行 `docker-compose down` 再 `docker-compose up -d` 生效[^cB-f6]。

> [!tip] 大白话
> 默认是把整个曲库**一个书架**搬进容器；音乐本就按类型散在几处时，硬合成一个目录既费事又易乱。多目录挂载相当于**在容器里摆几个贴着标签的格子**，每个宿主机文件夹各接一格，将来想挪哪个只动哪一根线。

> [!warning] 同一页的容器内路径有两版，对不上
> 配置段的映射写 `/app/media/Pop`，同页「容器内访问」一节却列出「`/music/Pop`：对应本地流行音乐库」[^cB-f6]，两组路径互斥。**本笔记按配置段（`/app/media/<分类>`）理解**——它可执行，也与第二章"`/app/media` 是曲库根目录"一致；原文两版并存，此处如实标注。

原页四条注意事项中，最关键的两条是[^cB-f6]：1）「确保挂载路径的正确性，错误的路径会导致容器无法访问音乐文件」；2）「新增或移除音乐库后，需要重启容器才能生效」。

## B.6 升级前检查清单

> [!warning] 本节依据社区反馈，不是官方口径
> 以下现象来自项目 issue **#546**（用户报告 + 作者回复），属**社区层级**；清单本身是本笔记的建议。官方自动更新页的声明是「保留你的所有数据和配置」[^cB-n9]，与 #546 的现象并不一致，两者一并列出，不替任何一方下结论。

**社区现象（#546）**：用户报告「就是升级了2.66版本，没有做任何命令改变。升级完成再打开音乐收藏图片全部不显示，专辑艺术家都无法显示」；作者先追问附件目录是否被删，用户答复只删了旧镜像、拉了新镜像，设置都在，唯独艺术家与专辑封面丢失，且确认 attachment 目录里的图片实际仍在。到本笔记可复核到的公开评论为止**未见根因结论**[^cB-f14]。

**升级前检查清单（本笔记建议，非官方口径）**：

1. **先备份 `/app/data`**：整目录打包到容器外另存一份。
2. **确认卷映射未变**：核对 `/app/media`、`/app/data`、`/app/download` 三条挂载仍在、左侧值未改。
3. **升级后立刻验证封面**：#546 的现象正是升级后才暴露。
4. **保留旧镜像**：自动更新会「清理旧版本镜像」[^cB-n9]，留一份旧 tag 便于回退。
5. **避开低峰时段**：更新期间服务会短暂中断[^cB-n9]。

> [!note] 本附录的已知空白
> 下列四项本次复核未找到官方说明，本笔记不作陈述：**Sqlite→MySQL 的数据迁移方式**、**切换外置 Redis 后原有缓存/数据的处理**、**当前最新版本号**、**`GUNICORN_PORT` / `NGINX_PORT` / `SUPERVISOR_PORT` 三者是否必须保持特定关系**——均为 `未取到`。

> [!summary] 本附录小结
> - **MySQL 与 Redis 都是替换项**：默认 Sqlite、容器自带 redis；`MYSQL_HOST` 填服务名，`REDIS_PORT` 默认值有 6379 与「v2.6.0 及以上 6380」两说。
> - **改端口分网络模式**：host 只改 `environment`；bridge 改容器内端口必须 `environment` 与 `ports` 同时改。
> - **自动更新的前提是挂上 `docker.sock`**，容器名用 `docker ps` 核对。
> - **升级三法**：`docker pull` 重建、`docker-compose pull` + `up -d`、watchtower；`docker-compose down -v` 会连卷删除。
> - **升级前先备份 `/app/data`**——本笔记建议，依据社区 #546。

若只想稳定使用，B.1、B.2、B.3 大多可以不动；真正值得现在就做的一条是 B.6 的第 1 项。遇到具体故障，再翻附录 C 的排错 FAQ。

## 参考来源

[^cB-n6]: Mysql 部署（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/mysql-bu-shu.md

[^cB-n7]: 外置Redis服务（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/wai-zhi-redis-fu-wu.md

[^cB-n8]: 自定义服务端口（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/zi-ding-yi-fu-wu-duan-kou.md

[^cB-n9]: 容器自动更新（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jin-jie-pei-zhi/rong-qi-zi-dong-geng-xin.md

[^cB-f4]: 怎么更新/升级 版本呢？（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/zen-me-geng-xin-sheng-ji-ban-ben-ne.md

[^cB-f6]: 多目录独立挂载的方式（官方文档）— https://xiers-organization.gitbook.io/music-tag-web-v2/jiao-cheng-wen-zhang/duo-mu-lu-du-li-gua-zai-de-fang-shi.md

[^cB-f14]: 社区 issue #546「【Bug问题】: 更新升级容器以后，专辑封面和艺术家封面全部打不开」（用户报告 + 作者 xhongc 回复，社区层级）— https://github.com/xhongc/music-tag-web/issues/546
