# 第二章：`compose.yml`——服务栈、依赖顺序、网络与挂载

上一章把三份产物摆到了位，但你还没看过其中任何一份的内容。本章只做一件事：把 `compose.yml` 从头到尾读一遍。它决定了这台机器上到底要跑哪几个容器、谁必须等谁、谁能对外开端口、以及数据最终落在宿主机的哪个目录——这四处全是后续配置与启动的落脚点，读错一处，第三章到第五章的努力都会打空。

> 本章读的是文件，不是操作。你不需要在本章执行任何命令；构建、初始化、启动是第五章的事。

---

## 2.1 先睹为快：整份文件长什么样

先把整份文件完整过一遍，建立轮廓，再逐段拆讲。下面是官方仓库 `compose_example.yml` 的全文（你上一章已把它拷成 `compose.yml`）【官方】[^c2-1]：

```yaml
# compose_example.yml（仓库根目录；拷成 compose.yml 后内容不变）
services:
  web:
    build: .
    restart: always
    links:
      - db
      - redis
#     - mcaptcha
#     - meilisearch
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "3000:3000"
    networks:
      - internal_network
      - external_network
    # env_file:
    #   - .config/docker.env
    volumes:
      - ./files:/misskey/files
      - ./.config:/misskey/.config:ro

  redis:
    restart: always
    image: redis:7-alpine
    networks:
      - internal_network
    volumes:
      - ./redis:/data
    healthcheck:
      test: "redis-cli ping"
      interval: 5s
      retries: 20

  db:
    restart: always
    image: postgres:18-alpine
    networks:
      - internal_network
    env_file:
      - .config/docker.env
    volumes:
      - ./db:/var/lib/postgresql
    healthcheck:
      test: "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"
      interval: 5s
      retries: 20

#  mcaptcha:
#    restart: always
#    image: mcaptcha/mcaptcha:latest
#    networks:
#      internal_network:
#      external_network:
#        aliases:
#          - localhost
#    ports:
#      - 7493:7493
#    env_file:
#      - .config/docker.env
#    environment:
#      PORT: 7493
#      MCAPTCHA_redis_URL: "redis://mcaptcha_redis/"
#    depends_on:
#      db:
#        condition: service_healthy
#      mcaptcha_redis:
#        condition: service_healthy
#
#  mcaptcha_redis:
#    image: mcaptcha/cache:latest
#    networks:
#      - internal_network
#    healthcheck:
#      test: "redis-cli ping"
#      interval: 5s
#      retries: 20

#  meilisearch:
#    restart: always
#    image: getmeili/meilisearch:v1.3.4
#    environment:
#      - MEILI_NO_ANALYTICS=true
#      - MEILI_ENV=production
#    env_file:
#      - .config/meilisearch.env
#    networks:
#      - internal_network
#    volumes:
#      - ./meili_data:/meili_data

networks:
  internal_network:
    internal: true
  external_network:
```

轮廓上，这份文件只有三块：`services`（要跑的容器）、`networks`（容器间怎么连通）、以及一大段被 `#` 注释掉的尾部。下面按块拆开。

---

## 2.2 三个启用的服务

真正启用的服务只有三个，其余都在注释里（见 2.7）：

| 服务名 | 来源 | 角色 |
| --- | --- | --- |
| `web` | `build: .`（本地构建，无 `image:`） | Misskey 本体（后端 + 前端） |
| `redis` | `image: redis:7-alpine` | 缓存与实例内部通信 |
| `db` | `image: postgres:18-alpine` | 主数据库 |

【官方】`web` 这一条最需要留意：它**没有** `image:` 字段，用的是 `build: .`。意思是「拿当前目录（也就是仓库根目录）的 Dockerfile 现场构建」，而不是从任何镜像仓库拉一个现成镜像【官方】[^c2-1]。

对 NAS / 自建服务器来说，这一行直接改写了部署要求：**宿主机上必须保留一份完整的源码树**。你不能像跑 Nginx 那样只丢一个 `compose.yml` 到机器上就完事——没有 `packages/`、`Dockerfile` 这些源码文件，`build: .` 无从下手。上一章强调「先 `git clone` 再拷贝」，原因就在这里。

> [!tip] 大白话
> 把 `build: .` 想成**现场装修**，而不是买成品房拎包入住：`image: redis:7-alpine` 是「去建材市场拉一套成品」，`build: .` 是「拿着图纸在你家院子里现盖」。所以院子里（仓库根目录）的图纸和材料一份都不能少——源码树不在，装修队就开不了工。

（顺带一提，`db` 用的是原版 `postgres:18-alpine`，**不是** PGroonga 镜像。这与第三章要讲的 `fulltextSearch.provider: sqlLike` 是配套的：默认配置走 PostgreSQL 标准能力，不需要全文检索扩展。）

---

## 2.3 启动顺序：`web` 等 `db` 和 `redis` 双双体检合格

`web` 的 `depends_on` 段落明确写了两个依赖，且都带 `condition: service_healthy`：

```yaml
# compose.yml · web 服务片段（节选）
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
```

【官方】含义是：`web` 必须等到 `db` 与 `redis` **都**通过各自的健康检查，才会被启动【官方】[^c2-1]。两个健康检查定义在各自服务里：

```yaml
# compose.yml · redis 与 db 的健康检查（节选，逐字保留）
  redis:
    healthcheck:
      test: "redis-cli ping"
      interval: 5s
      retries: 20

  db:
    healthcheck:
      test: "pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB"
      interval: 5s
      retries: 20
```

逐项核对：

| 项 | `redis` | `db` |
| --- | --- | --- |
| `test` | `redis-cli ping` | `pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB` |
| `interval` | `5s` | `5s` |
| `retries` | `20` | `20` |
| `timeout` | 未设置 | 未设置 |
| `start_period` | 未设置 | 未设置 |

【官方】三条要点：

1. 两个检查的 `interval` 与 `retries` 完全相同，都是「每 5 秒探一次，最多 20 次」。
2. 两个检查都**只**设了 `test` / `interval` / `retries`，**没有** `timeout`，也**没有** `start_period`【官方】[^c2-1]。
3. `db` 的 `test` 里那两个 `$$` 是 Compose 的转义写法：`$$` 在 compose 解析阶段会被还原成一个字面 `$` 传进容器，容器里的 shell 再把它展开成实际的用户名与库名（值来自 `db` 的 `env_file`，第四章细说）。所以这里**不能**手滑「修正」成单个 `$`，否则含义会变。

第 2 点在本机跑时无关痛痒，在 NAS 上是实打实的隐患：没有 `timeout` 意味着探测命令若卡住会一直挂着，没有 `start_period` 意味着容器刚起来那几秒的失败也会计入 `retries`。磁盘 I/O 慢的机器上，数据库首次初始化本身就要写不少文件，健康检查可能在数据库还没站稳时就被判失败【推断】（这一后果官方未陈述，是由「未设 `timeout`/`start_period`」这一官方事实推出的）。

> [!tip] 大白话
> 把 `condition: service_healthy` 想成**员工上岗前的体检**：`db` 和 `redis` 是两名员工，`web` 是前台——前台不许比同事先到岗，必须等这两位都拿到体检合格证明才开门。而「没有 `start_period`」相当于体检不给人热身时间：慢速存储上，员工还在系鞋带就被判不合格。

---

## 2.4 端口与网络：只有 `web` 对外开窗

三个服务的对外暴露面差异极大：

| 服务 | 发布宿主端口 | 内部监听端口 | 加入的网络 |
| --- | --- | --- | --- |
| `web` | `"3000:3000"` | 3000 | `internal_network` + `external_network` |
| `redis` | 无 | 6379 | 仅 `internal_network` |
| `db` | 无 | 5432 | 仅 `internal_network` |

【官方】只有 `web` 通过 `ports: - "3000:3000"` 把容器端口映射到宿主机；`redis` 与 `db` **完全没有** `ports` 段，因此从宿主机或外部网络都访问不到它们，只能在 compose 网络内部被其他服务按服务名访问【官方】[^c2-1]。这正是 `default.yml` 里能直接写 `db.host: db`、`redis.host: redis` 的原因——服务名就是网内主机名（第三章展开）。

两个网络定义在文件底部：

```yaml
# compose.yml · 网络定义（节选）
networks:
  internal_network:
    internal: true
  external_network:
```

- `internal_network` 带 `internal: true`，即「内网」：接入它的服务不直连外部网络。
- `external_network` 没有任何配置项（冒号后为空），是一个普通桥接网络，提供对外连通性。

`web` 同时加入两者：走 `internal_network` 跟 `db`、`redis` 说内网话，走 `external_network` 对外收发（拉取远程内容、联邦通信等）。`redis` 与 `db` 只接 `internal_network`，与外部隔离。【官方】[^c2-1]

`web` 还单独声明了 `links` 指向 `db` 与 `redis`。`links` 是 Compose 早期的连接机制（附带主机名别名与隐式启动顺序）；在当前 Compose v2 里，同一网络内的服务名本身就能互相解析，所以这两个 `links` 条目对连通性而言基本是冗余的历史写法，保留它不影响运行【推断】（`links` 的实际语义官方未在示例中说明，属通用 Compose 知识，此处不另立来源）。

> [!tip] 大白话
> 把端口发布想成**开窗**：`web` 在临街墙上开了一扇 3000 号窗，外面能看见；`db` 和 `redis` 一扇窗都没开，只能靠楼里的内部走廊（`internal_network`）找到它们。所以你别指望从浏览器直连 5432 去连数据库——设计上就没这门。

---

## 2.5 三处绑定挂载（以及那个最容易写错的路径）

三个服务各挂一个宿主目录，把该持久化的数据留在宿主机上，容器重建不丢：

| 宿主路径 | 容器内目标 | 用途 | 备注 |
| --- | --- | --- | --- |
| `./db` | `/var/lib/postgresql` | PostgreSQL 数据目录 | **注意不是 `…/data`**，见下 |
| `./redis` | `/data` | Redis 持久化 | |
| `./files` | `/misskey/files` | 用户上传的文件 | 权限敏感，见 2.8 |
| `./.config`（只读） | `/misskey/.config:ro` | 应用配置 | `:ro` 只读，`web` 专用 |

【官方】四处挂载在文件中的原文分别是 `./files:/misskey/files`、`./redis:/data`、`./db:/var/lib/postgresql`，以及 `web` 上的 `./.config:/misskey/.config:ro`【官方】[^c2-1]。

`.config` 以 `:ro` 只读方式挂进 `web`，这解释了上一章的一条硬约束：**应用配置必须放在 compose 文件同级的 `.config/` 目录里**，换个位置容器就看不到【官方】[^c2-1]。第三章的 `default.yml`、第四章的 `docker.env` 都住在这里的缘由即在此。

用目录树看更直观——克隆后的仓库根目录，加上三个数据目录：

```text
misskey/                      # git clone 出来的仓库根（也是 compose 文件的所在）
├── compose.yml               # 本章的文件
├── Dockerfile                # build: . 要用到它
├── db/                       # ← ./db       → /var/lib/postgresql
├── redis/                    # ← ./redis    → /data
├── files/                    # ← ./files    → /misskey/files
├── .config/
│   ├── default.yml           # ← ./.config 以只读方式整体挂进 /misskey/.config
│   └── docker.env            #     （db 还单独用 env_file 读它）
└── packages/ …               # 源码树：build: . 的原料
```

### 最容易写错的一处：`/var/lib/postgresql` 不是 `/var/lib/postgresql/data`

`db` 的挂载目标是 `/var/lib/postgresql`，**父目录本身**，结尾没有 `data`【官方】[^c2-1]。这一处是本文件里最容易「顺手改错」的地方，因为网上绝大多数第三方 PostgreSQL / Compose 教程教的都是挂到 `/var/lib/postgresql/data`。两者只差一个目录层级，后果却不小：

```yaml
# compose.yml · db 挂载（正确，逐字保留）
    volumes:
      - ./db:/var/lib/postgresql
```

```yaml
# 多数第三方 PostgreSQL 教程的写法 —— 不要照搬到本文件
    volumes:
      - ./db:/var/lib/postgresql/data
```

写错会怎样：容器真正写入的路径（本镜像的 PGDATA 所在层级）落在未被挂载的容器层里，宿主机 `./db` 反而空空如也；容器一旦被 `docker compose down` 或重建，数据就随之消失。所以请把这一段当作**不可自作聪明修正**的原文，原样保留。

> [!tip] 大白话
> 把挂载目标想成**保险箱的钥匙孔**：钥匙（`./db`）必须插进本镜像指定的那个孔（`/var/lib/postgresql`）。第三方教程给的孔位（`…/data`）是另一把锁的位置——孔插错了，东西是存进去了，但存进了你下次会一起扔掉的那个抽屉。

【推断】以上「为什么容易错」的解释（第三方教程普遍使用 `…/data`、postgres:18 镜像的目录层级不同）属本文档分析，官方示例文件本身只给了路径，未加说明。

---

## 2.6 `restart: always` 出现在全部三个服务上

【官方】`web`、`redis`、`db` 三个服务的定义里都有 `restart: always`【官方】[^c2-1]。含义是容器因任何原因退出（包括宿主机重启）都会被自动拉起。对自建实例而言这是必要的兜底：NAS 断电重来后不需要你手工 `up`，栈会自行恢复。

但要注意「自动拉起」不等于「启动顺序被保证」：`restart` 只负责各自复活，顺序仍需靠 2.3 的 `depends_on`。重启过程中若 `web` 比 `db` 先起来，`web` 会在启动时短暂连不上数据库，待 `db` 就绪后恢复正常。

---

## 2.7 只以注释存在的服务：不要以为它们在栈里

文件下半部分有一大段以 `#` 开头的服务定义，涉及三个名字：`mcaptcha`（`mcaptcha/mcaptcha:latest`）、`mcaptcha_redis`（`mcaptcha/cache:latest`）、`meilisearch`（`getmeili/meilisearch:v1.3.4`）【官方】[^c2-1]。

【官方】关键点：**它们全部被注释，默认不启用**，不属于当前服务栈【官方】[^c2-1]。只是顺手扫一眼文件的人，容易误以为这些名字也是要跑的服务——尤其在 `web.links` 里还留了两行注释形式的 `# - mcaptcha`、`# - meilisearch`，视觉上更像是「栈的一部分」。判断某服务是否启用，唯一可靠依据是它的定义是否被 `#` 注释掉。

本轮不展开这三个注释服务的配置（验证码是可选的反滥用组件，`meilisearch` 是备选全文检索方案，默认配置用的是 `sqlLike`）。你现在只需要记住：**它们没有在跑**。

> [!tip] 大白话
> 把注释块想成**样板间**：售楼处里摆着几套精装修的样板，看着像在卖，其实没有一户真的交付。文件里 `mcaptcha`、`meilisearch` 就是这种样板间——写在纸上、没接线。别把它们当成你机器上正在运行的东西。

---

## 2.8 卷权限：v13 的历史故障与仍未确认的现状

三个绑定挂载目录需要在宿主机上可写【推断】（本文档推断，官方 compose 示例未直接陈述）。历史上这里出过一次具体的故障，值得知道，但不必惊恐——它是 2023 年的一次性事件。

【官方】事实来自 Issue #9613（2023-01-16 开、同日关闭）[^c2-2]：

- 现象出现在从 **v13** 升级后的 Docker 实例上：容器内 `/misskey/files/` 下的文件属主是数字 `991`（UID/GID 991）。
- 容器日志报 `Error: EACCES: permission denied, open '/misskey/files/...'`，对客户端表现为 `StatusError: 500 Internal Server Error`。
- **已有文件访问与新文件上传同时失败**，并非只影响历史文件。
- 报告者预期的修复手段是 `sudo chown -hR 991:991 ./files`，但执行后**仍未恢复访问**。
- 该 issue 在开启当日即被关闭，正文中**没有记录任何修复提交、修复版本或绕过方法**。

原文中的文件权限行与报错如下（逐字保留）：

```text
# Issue #9613 报告者贴出的现状
$ sudo ls -al files/ba692cfd-ac26-4042-a293-7340d82c901e
-rw-r--r-- 1 991 991 7550 Oct 26 02:55 files/ba692cfd-ac26-4042-a293-7340d82c901e

Error: EACCES: permission denied, open '/misskey/files/23dbcdab-5583-4ab6-808d-727021cf0aa0'
StatusError: 500 Internal Server Error
```

【推断】把上面的官方事实向下推一步：**没有任何来源能确认当前版本容器的实际 UID/GID**——`991:991` 只是 v13 时代的一个观测值，`PUID`/`PGID` 之类的配置变量在官方文件里也不存在。因此「现在的 Misskey 容器用哪个 UID/GID、当年那个问题是否已修」都是**未知项**，不能当作已知事实使用【推断】[^c2-2]。

对本章而言，可落地的动作只有一条：**留意 `./files`（以及 `./db`、`./redis`）的宿主目录权限**。如果日后日志里出现 `EACCES` + `500`，这条历史记录给了你一个排查方向——但它给的只是一段 2023 年的历史，不是一份可直接照抄的修复方案。

> [!tip] 大白话
> 把容器内 UID/GID 想成**门禁卡的编号**：宿主机上 `./files` 这扇门认某个编号的卡。v13 那次是卡号（991）与门锁对不上，文件就在眼前却打不开——而且把门重新配成 991 号也没用，说明问题比「配错一张卡」更绕。至于今天这把锁认几号，档案里没写。

---

## 小结

- `compose.yml` 只启用三个服务：`web`（`build: .` 本地构建）、`redis:7-alpine`、`db: postgres:18-alpine`；`web` 不从镜像仓库拉取，所以部署机上必须保留完整源码树。
- 启动顺序由 `depends_on` + `condition: service_healthy` 保证：`web` 等 `db` 与 `redis` 双双健康才起；两个健康检查都是 `interval: 5s`、`retries: 20`，且**都未设 `timeout` 与 `start_period`**。
- 只有 `web` 发布宿主端口 `"3000:3000"`；`redis`、`db` 不开端口，仅在 `internal_network` 内可达。`web` 同时加入内、外两个网络。
- 三处绑定挂载：`./db → /var/lib/postgresql`（**不是 `…/data`**，全文件最易错处）、`./redis → /data`、`./files → /misskey/files`；另有 `./.config → /misskey/.config:ro` 只读挂入 `web`。三个服务均设 `restart: always`。
- `mcaptcha`、`mcaptcha_redis`、`meilisearch` 只以注释存在，默认不启用；卷权限方面，v13 曾出现 UID/GID `991` 导致的 EACCES 与 500，`chown` 无效、issue 当日关闭无修复记录，当前版本的实际 UID/GID 无来源可确认【推断】。

## 下一章预告

编排文件已经读通：容器怎么起、谁等谁、数据落哪，都清楚了。但 `web` 容器里跑起来之后要连哪个域名、用哪个数据库用户、端口对不对得上，这些不在 `compose.yml` 里，而在通过只读挂载送进去的那份应用配置里。下一章就打开 `.config/default.yml`，逐个过一遍**必须改**的字段、哪些可留默认，以及那几个「启动后改了就出事」的不可变项。

---

[^c2-1]: [compose_example.yml — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml)
[^c2-2]: [Issue #9613 容器内已上传文件无法访问 — misskey-dev/misskey](https://github.com/misskey-dev/misskey/issues/9613)
