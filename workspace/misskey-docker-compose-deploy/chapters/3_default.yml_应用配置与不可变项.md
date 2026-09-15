# 第三章：`.config/default.yml`——应用配置必改字段与不可变项

> 标注约定：`【官方】`＝官方文档或官方仓库一手文件直接陈述；`【推断】`＝本文档推断、无官方来源；`【过时】`＝已失效信息，按历史口径呈现。

上一章读的是 `compose.yml`，它只回答「跑哪些容器、它们怎么连」。这一章要处理的 `.config/default.yml` 回答的是另一个问题：**Misskey 这个应用自己怎么工作**——对外叫什么名字、连的数据库在哪、缓存用哪个实例、帖子 ID 怎么生成。

为什么这份文件值得单独用一章、而且比编排文件更危险？因为三份产物里只有它含有**一旦实例启动就基本不能再改**的字段，其中 `url` 一个字符写错，代价可能是把整个联邦关系网打碎。所以这一章的重点不是「把每一行都讲一遍」，而是**先把不可变的字段定死，再看哪些字段需要改、哪些保持注释即可**。

---

## 3.1 先睹为快：这份文件长什么样

这份文件不是你手写的，而是第一步「三连拷贝」里从官方示例复制过来的【官方】[^c3-2]：

```bash
# 在克隆目录内执行
cp .config/docker_example.yml .config/default.yml
```

复制之后，官方给的编辑指引是一句话：**「请按文件里的说明（as per the description）编辑 `default.yml`」**【官方】[^c3-2]。原文是：

> Please edit `default.yml` and `docker.env` file as per the description. Also edit `compose.yml` as needed. (If you want to change the port etc.)

这句话是本章的阅读方法：**这份配置文件自带的注释，就是官方给你写的说明书**。它给每个字段都标了用途、取值和警告，你不需要另找一份文档对照。所以在逐段拆解之前，先完整看一遍原文，建立「哪里有什么」的地图【官方】[^c3-1]。

下面是 `.config/default.yml` 的完整内容（由 `.config/docker_example.yml` 拷贝而来，逐字保留）：

```yaml
# .config/default.yml
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Misskey configuration
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#   ┌─────┐
#───┘ URL └─────────────────────────────────────────────────────

# Final accessible URL seen by a user.
# You can set url from an environment variable instead.
url: https://example.tld/

# ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE
# URL SETTINGS AFTER THAT!

#   ┌───────────────────────┐
#───┘ Port and TLS settings └───────────────────────────────────

#
# Misskey requires a reverse proxy to support HTTPS connections.
#
#                 +----- https://example.tld/ ------------+
#   +------+      |+-------------+      +----------------+|
#   | User | ---> || Proxy (443) | ---> | Misskey (3000) ||
#   +------+      |+-------------+      +----------------+|
#                 +---------------------------------------+
#
#   You need to set up a reverse proxy. (e.g. nginx)
#   An encrypted connection with HTTPS is highly recommended
#   because tokens may be transferred in GET requests.

# The port that your Misskey server should listen on.
port: 3000

#   ┌──────────────────────────┐
#───┘ PostgreSQL configuration └────────────────────────────────

db:
  host: db
  port: 5432

  # Database name
  # You can set db from an environment variable instead.
  db: misskey

  # Auth
  # You can set user and pass from environment variables instead.
  user: example-misskey-user
  pass: example-misskey-pass

  # Whether disable Caching queries
  #disableCache: true

  # Extra Connection options
  #extra:
  #  ssl: true

dbReplications: false

# You can configure any number of replicas here
#dbSlaves:
#  -
#    host:
#    port:
#    db:
#    user:
#    pass:
#  -
#    host:
#    port:
#    db:
#    user:
#    pass:

#   ┌─────────────────────┐
#───┘ Redis configuration └─────────────────────────────────────

redis:
  host: redis
  port: 6379
  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
  #pass: example-pass
  #prefix: example-prefix
  #db: 1

#redisForPubsub:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForJobQueue:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForTimelines:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForReactions:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#   ┌───────────────────────────────┐
#───┘ Fulltext search configuration └─────────────────────────────

# These are the setting items for the full-text search provider.
fulltextSearch:
  # You can select the ID generation method.
  # - sqlLike (default)
  #   Use SQL-like search.
  #   This is a standard feature of PostgreSQL, so no special extensions are required.
  # - sqlPgroonga
  #   Use pgroonga.
  #   You need to install pgroonga and configure it as a PostgreSQL extension.
  #   In addition to the above, you need to create a pgroonga index on the text column of the note table.
  #   see: https://pgroonga.github.io/tutorial/
  # - meilisearch
  #   Use Meilisearch.
  #   You need to install Meilisearch and configure.
  provider: sqlLike

# For Meilisearch settings.
# If you select "meilisearch" for "fulltextSearch.provider", it must be set.
# You can set scope to local (default value) or global
# (include notes from remote).

#meilisearch:
#  host: meilisearch
#  port: 7700
#  apiKey: ''
#  ssl: true
#  index: ''
#  scope: local

#   ┌───────────────┐
#───┘ ID generation └───────────────────────────────────────────

# You can select the ID generation method.
# You don't usually need to change this setting, but you can
# change it according to your preferences.

# Available methods:
# aid ... Short, Millisecond accuracy
# aidx ... Millisecond accuracy
# meid ... Similar to ObjectID, Millisecond accuracy
# ulid ... Millisecond accuracy
# objectid ... This is left for backward compatibility

# ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE
# ID SETTINGS AFTER THAT!

id: 'aidx'

#   ┌────────────────┐
#───┘ Error tracking └──────────────────────────────────────────

# Sentry is available for error tracking.
# See the Sentry documentation for more details on options.

#sentryForBackend:
#  enableNodeProfiling: true
#  # Specify Sentry integration names to disable individual auto-instrumentation.
#  # The names are integration .name values, not factory function names.
#  # To check enabled names, set `options.debug: true` and see
#  # "Integration installed: <name>" in the Sentry logs.
#  #
#  # As of 2026-07-07 / @sentry/node 10.62.0, useful names for Misskey include:
#  #   Postgres  ... DB queries (when pg is externalized)
#  #   Redis     ... ioredis commands
#  #   Fastify   ... inbound HTTP routes
#  #   Http      ... inbound/outbound HTTP; disabling this can also affect request isolation
#  #   NodeFetch ... fetch/undici requests
#  disabledIntegrations: ['Postgres']
#  options:
#    dsn: 'https://examplePublicKey@o0.ingest.sentry.io/0'
#    # By default, Misskey prevents Sentry trace headers (`sentry-trace` and
#    # `baggage`) from being sent to remote ActivityPub/Webhook/etc. hosts.
#    # To intentionally propagate distributed traces to trusted internal services,
#    # list only those internal URL patterns here.
#    # Avoid broad patterns that match remote servers unless you intentionally
#    # want to restore Sentry's legacy behavior of propagating traces to all
#    # outbound HTTP requests.
#    #tracePropagationTargets: []
#    # Internal allowlist example:
#    #tracePropagationTargets:
#    #  - 'internal-service.example'

#sentryForFrontend:
#  vueIntegration:
#    tracingOptions:
#      trackComponents: true
#  browserTracingIntegration:
#  replayIntegration:
#  options:
#    dsn: 'https://examplePublicKey@o0.ingest.sentry.io/0'

#   ┌─────────────────────┐
#───┘ Other configuration └─────────────────────────────────────

# Whether disable HSTS
#disableHsts: true

# Number of worker processes
#clusterLimit: 1

# Number of threads of extra thread pool for CPU-intensive tasks (per worker)
#threadPoolSize: 1

# Job concurrency per worker
# deliverJobConcurrency: 128
# inboxJobConcurrency: 16

# Job rate limiter
# deliverJobPerSec: 128
# inboxJobPerSec: 32

# Job attempts
# deliverJobMaxAttempts: 12
# inboxJobMaxAttempts: 8

# IP address family used for outgoing request (ipv4, ipv6 or dual)
#outgoingAddressFamily: ipv4

# Proxy for HTTP/HTTPS
#proxy: http://127.0.0.1:3128

proxyBypassHosts:
  - api.deepl.com
  - api-free.deepl.com
  - www.recaptcha.net
  - hcaptcha.com
  - challenges.cloudflare.com

# Proxy for SMTP/SMTPS
#proxySmtp: http://127.0.0.1:3128   # use HTTP/1.1 CONNECT
#proxySmtp: socks4://127.0.0.1:1080 # use SOCKS4
#proxySmtp: socks5://127.0.0.1:1080 # use SOCKS5

# Media Proxy
#mediaProxy: https://example.com/proxy

# For security reasons, uploading attachments from the intranet is prohibited,
# but exceptions can be made from the following settings. Default value is "undefined".
# Read changelog to learn more (Improvements of 12.90.0 (2021/09/04)).
#allowedPrivateNetworks:
#  - '127.0.0.1/32'

# Upload or download file size limits (bytes)
#maxFileSize: 262144000

# Log settings
# logging:
#   # Log output format. "json" outputs one-line JSON; defaults to "pretty".
#   format: pretty
#   # Minimum level for all loggers. Defaults to info in production and debug otherwise.
#   level: info
#   # The longest matching logger domain takes precedence over the global level.
#   domains:
#     core.boot: info
#     queue: error
#     queue.deliver: debug
#     db.sql: off
#   # HTTP status classes to record in the access log. No output when unspecified.
#   access:
#     statusClasses:
#       - '2xx'
#       - '3xx'
#       - '4xx'
#       - '5xx'
#     # Enable body logging explicitly only during development.
#     bodies:
#       request: false
#       response: false
#       # 16 KiB by default, up to 128 KiB.
#       maxBytes: 16384
#   sql:
#     # Outputs query parameters during SQL execution to the log.
#     # default: false
#     enableQueryParamLogging: false
#     # Disable query truncation. If set to true, the full text of the query will be output to the log.
#     # default: false
#     disableQueryTruncation: false
```

这份文件被以**只读**方式挂载进 `web` 容器（上一章的 `./.config:/misskey/.config:ro`），所以你只能在宿主机上改它、再重启容器生效，容器内改不了【官方】[^c3-1]。

先看结构地图：文件按区段组织，**每一段开头都有一条用 `#` 画的横幅**（`URL`、`PostgreSQL configuration`、`Redis configuration`……），这就是它的目录。按风险从高到低，逐段拆。

---

## 3.2 `url`：全篇风险最高的一个字段

这是整章的重心，也是整份笔记里最不能出错的一行。因为它有两个叠加属性：**必须改**（默认是占位符）＋ **改完就基本不能反悔**。

### 官方原文

```yaml
# .config/default.yml
#   ┌─────┐
#───┘ URL └─────────────────────────────────────────────────────

# Final accessible URL seen by a user.
# You can set url from an environment variable instead.
url: https://example.tld/

# ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE
# URL SETTINGS AFTER THAT!
```

注意三层信息【官方】[^c3-1]：

1. 注释 `# Final accessible URL seen by a user.` —— 它的定义是「**用户最终在浏览器里看到的、可访问的地址**」；
2. `url: https://example.tld/` —— `example.tld` 是占位符，**不是能直接用的值**；
3. 紧跟的警告 —— `ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE URL SETTINGS AFTER THAT!`（实例一旦启动，就不要改 URL 设置）。

### 要改成什么

【官方】排错页把这条讲得最直白[^c3-3]：

> **In `url` , write the URL that is **(or you want to be)** displayed in the address bar when accessing the server via a browser.**

也就是「**你访问这个服务器时，浏览器地址栏里出现的（或你希望出现的）那个地址**」——不是容器端口，不是内网 IP，不是 `localhost`，而是**用户真正敲进浏览器、最终生效的那一串**。

| `url` 取值 | 含义 | 是否正确 |
| --- | --- | --- |
| `https://example.tld/` | 官方占位符，示例用 | 永远不正确，必须替换 |
| `https://你的域名/`（示意） | 用户浏览器地址栏应该看到的地址 | 对外提供服务时的正确形态 |
| `http://localhost:3000` | 本机开发自测 | 仅开发环境口径（见本章末尾）【官方】[^c3-4] |

> [!tip] 大白话
> 把 `url` 想成这个实例的**门牌号＋身份证号**：它不只是「网站地址」，还是这个实例在联邦网络里对外的身份。你在装修阶段（还没上线）换门牌号不要紧；一旦挂着这个门牌号开门营业、把名片发给了全网各个服务器，再换就会让所有人手里的旧名片作废。
> 所以：**先把 `url` 想清楚、写死，再启动实例。**

### 为什么「启动后不可改」——四处独立信号

这不是某一个页面的口头提醒，而是四个互相独立的位置在说同一件事，官方把风险级别定得很高：

| # | 位置 | 原文 | 标注 |
| --- | --- | --- | --- |
| 1 | 配置文件本身 | `ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE URL SETTINGS AFTER THAT!` | 【官方】[^c3-1] |
| 2 | Docker 部署指南页首 Danger 提示 | `Do not recreate the database with the domain/hostname of the server once you have started using it!` | 【官方】[^c3-2] |
| 3 | Ubuntu 安装指南页首 Danger 提示 | `Do not recreate the database for a domain/hostname that is already in use on a running server!` | 【官方】[^c3-4] |
| 4 | Ubuntu 安装指南正文 | `Never change the domain name or hostname of a server once it has been put into use!` | 【官方】[^c3-4] |

第 2、3 条是同一件事的两种表述，必须原样理解：**它禁止的是「用一个已在运行的服务器曾经用过的域名/主机名去重建数据库」**。换个说法——"这个域名我之前用过，现在想拿它重装一台新库" 这条路是被明确堵死的。它同时说明了为什么 `url` 属于「启动前必须定死」的字段。

反方向并没有被禁止：**全新域名 + 全新数据库**是正常的首次部署，不存在「用过」的包袱。

### 写错的症状：无法注册

如果 `url` 填得不对，会怎样？【官方】排错页在 `Cannot Sign Up`（无法注册）条目下给了它一个具名原因[^c3-3]：

> It seems like it cannot connect to the API. Check if the `url:` at the beginning of `default.yml` is set correctly. Check the Node.js version and installation settings again carefully.

也就是说，客户端**连不上 API**，对外表现就是「注册不了」。这条信息很有用：当你的实例界面能打开、却卡在注册时，第一反应应该去回看 `default.yml` 开头的 `url`，而不是去猜数据库口令。

### 启动后改动会怎样：社区给出的答案

配置文件说「不要改」，但没说「改了会怎样」。这个答案在官方仓库的一条问答讨论里，由维护者给出【官方】[^c3-5]：

> **I would highly recommend _not_ changing your URL. Due to how the Fediverse/ActivityPub works, changing your URL will most likely result in entirely broken federation.**

（强烈建议不要改 URL。由于 Fediverse/ActivityPub 的运作方式，改 URL **极有可能导致联邦完全损坏**。）

同一讨论里，有人追问「那你自己不是改过吗，怎么做到的」，维护者的回答同样值得原样保留，因为它恰好说明了「极少数成功案例」的真实成色【官方】[^c3-5]：

> 1. I changed it with my servers running **Firefish, not Misskey**
> 2. The whole process involved multiple custom scripts talking both to the server API and the database directly and was overall **extremely janky**. I wouldn't recommend that anyone try and recreate what I did tbh.

拆开看这两条：唯一被提到的成功案例**不在 Misskey 上**（那是另一个联邦软件 Firefish）；做法是一堆自定义脚本同时操作服务端 API 和数据库，作者自己评价为 extremely janky（极其粗糙），并且**明确不建议任何人效仿**。所以对 Misskey 用户来说，结论是：**没有可复制的正当路径**。

### 【推断】文档没写、但你该意识到的后果

【官方】只说了「注册不了」和「联邦完全损坏」两个症状。**为什么会损坏**、损坏到什么粒度，官方没有展开。下面这条是本文档的推断，请与上面的官方结论分开看：

【推断】`url` 会被用来构造这个实例对外广播的身份标识（比如帖子和用户的 URI）。一旦这个值变了，**远端服务器数据库里记住的仍然是旧域名**——那些指向你实例的引用不会自动跟着改，于是形成「新旧地址并存、互相指不到对方」的错位状态。这解释了为什么官方宁愿让你「启动前定死」也不提供迁移方案：问题不在改这一行本身，而在于这个值早已被复制到了你控制不到的地方。

这是一条**推断**，没有官方原文支撑；它只用于帮你理解「为什么官方态度这么强硬」，不作为操作依据。

### 还有两条路：环境变量与开发环境

【官方】配置文件里留了一句：`# You can set url from an environment variable instead.`——**`url` 也可以改用环境变量提供**。但要注意：**示例文件里并没有写出这个环境变量的名字**【官方】[^c3-1]。所以除非你去别处查到确切变量名，否则照示例直接改这一行是最稳的做法。

另一条是给开发环境的口径【官方】[^c3-4]：

> For a development environment, specify the URL as `url: http://localhost:3000`

这是**开发环境**的写法，来源是 Ubuntu 安装指南的 Tips，不要把它当成生产/内网部署的推荐值。你的目标场景（NAS、可能只有内网）属于官方**完全没有覆盖**的空白区——那部分设计属于本篇的推断范畴，会在后续章节单独讨论，本章只管把「`url` 是什么、为什么不能反悔」讲透。

---

## 3.3 第二个启动后不可改的字段：`id`

除了 `url`，还有一处带**一字不差的同款警告**——帖子 ID 的生成方式【官方】[^c3-1]：

```yaml
# .config/default.yml
#   ┌───────────────┐
#───┘ ID generation └───────────────────────────────────────────

# You can select the ID generation method.
# You don't usually need to change this setting, but you can
# change it according to your preferences.

# Available methods:
# aid ... Short, Millisecond accuracy
# aidx ... Millisecond accuracy
# meid ... Similar to ObjectID, Millisecond accuracy
# ulid ... Millisecond accuracy
# objectid ... This is left for backward compatibility

# ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE
# ID SETTINGS AFTER THAT!

id: 'aidx'
```

关键点【官方】[^c3-1]：

- 示例**出厂就给了一个生效值**：`id: 'aidx'`（注意带单引号）；
- 警告与 `url` 完全同款，只是把 `URL SETTINGS` 换成 `ID SETTINGS`：**实例启动后不要再改**；
- 文件自己也承认「你通常不需要改这个设置」（`You don't usually need to change this setting`）。

备选值及官方对它们的描述，逐字列在这里：

| 取值 | 官方描述 | 中文理解 |
| --- | --- | --- |
| `aid` | Short, Millisecond accuracy | 短、毫秒精度 |
| `aidx` | Millisecond accuracy | 毫秒精度（**示例出厂值**） |
| `meid` | Similar to ObjectID, Millisecond accuracy | 类似 ObjectID、毫秒精度 |
| `ulid` | Millisecond accuracy | 毫秒精度 |
| `objectid` | This is left for backward compatibility | 仅为向后兼容保留 |

【官方】既然示例已经显式给了 `aidx`，而且文件说「通常不用改」，**保持默认即可**——你要做的是知道它存在、且和 `url` 一样属于启动前定死的字段。

---

## 3.4 数据库连接：`db.*`

这一段要处理「Misskey 去哪里找数据库」。先把原文摆出来【官方】[^c3-1]：

```yaml
# .config/default.yml
db:
  host: db
  port: 5432

  # Database name
  # You can set db from an environment variable instead.
  db: misskey

  # Auth
  # You can set user and pass from environment variables instead.
  user: example-misskey-user
  pass: example-misskey-pass

  # Whether disable Caching queries
  #disableCache: true

  # Extra Connection options
  #extra:
  #  ssl: true

dbReplications: false

# You can configure any number of replicas here
#dbSlaves:
#  -
#    host:
#    port:
#    db:
#    user:
#    pass:
#  -
#    host:
#    port:
#    db:
#    user:
#    pass:
```

按「性质」把每个字段分类，这是本段最重要的一张表：

| 字段 | 示例值 | 性质 | 说明 |
| --- | --- | --- | --- |
| `db.host` | `db` | **生效** | 必须与 compose 的服务名对应【官方】 |
| `db.port` | `5432` | **生效** | PostgreSQL 端口，与服务定义对应【官方】 |
| `db.db` | `misskey` | **生效** | 数据库名；示例取值即默认 |
| `db.user` | `example-misskey-user` | **生效·占位** | 占位值，需与 `docker.env` 一致【官方】 |
| `db.pass` | `example-misskey-pass` | **生效·占位** | 占位值，需与 `docker.env` 一致【官方】 |
| `db.disableCache` | `true` | **注释** | 仅示例，取消注释才生效【官方】 |
| `db.extra.ssl` | `true` | **注释** | 仅示例，取消注释才生效【官方】 |
| `dbReplications` | `false` | **生效** | 显式关闭【官方】 |
| `dbSlaves` | — | **注释** | 副本列表模板，未启用【官方】 |

两个必须记住的关联【官方】[^c3-1]：

1. **`host` 值与 compose 服务名一一对应。** `db.host: db` 里的这个 `db`，正是 `compose.yml` 里那个数据库服务的名字；`redis.host: redis` 同理。**改一处的服务名，另一处必须同步改**，否则应用会找不到数据库。
2. **`user` / `pass` 是占位值，且必须与 `.config/docker.env` 保持一致。** 两份文件是两套配置入口，但指向同一个数据库账户；对不上就连不上。口令那一半在下一章（`.config/docker.env`）处理，这里只需要知道「它俩必须一致」。

`db.db: misskey` 这一行的注释还提示：数据库名同样可以用环境变量提供（`# You can set db from an environment variable instead.`）【官方】。

> [!tip] 大白话
> 把 compose 里的服务名想成**同一栋楼里的房间号**：容器之间不靠 IP，靠「你叫什么名字」互相找到对方。`db.host: db` 的意思是「数据库住在一个叫 `db` 的房间」。
> 所以只要你给 compose 里的数据库服务改了名（比如从 `db` 改成 `postgres`），就得回来把这里的 `db` 一起改——**两边名字对不上，Misskey 就找不到数据库，启动后直接连不上。**

---

## 3.5 Redis：默认一个实例扛下所有角色

Redis 段是这份文件里「注释密度」最高的地方之一，先把原文摆出来【官方】[^c3-1]：

```yaml
# .config/default.yml
redis:
  host: redis
  port: 6379
  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
  #pass: example-pass
  #prefix: example-prefix
  #db: 1

#redisForPubsub:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForJobQueue:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForTimelines:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1

#redisForReactions:
#  host: redis
#  port: 6379
#  #family: 0  # 0=Both, 4=IPv4, 6=IPv6
#  #pass: example-pass
#  #prefix: example-prefix
#  #db: 1
```

拆开看，这一段实际上分成**六个块**，但只有**第一个块的主体是生效的**【官方】[^c3-1]：

| 块 | 状态 | 生效内容 |
| --- | --- | --- |
| `redis:` | 主体**生效** | 只有 `host: redis` 与 `port: 6379` |
| `redis:` 内部的 `family`/`pass`/`prefix`/`db` | 全部**注释** | 不生效 |
| `redisForPubsub:` | **整块注释** | 不生效 |
| `redisForJobQueue:` | **整块注释** | 不生效 |
| `redisForTimelines:` | **整块注释** | 不生效 |
| `redisForReactions:` | **整块注释** | 不生效 |

结论很直接：**示例的出厂状态是「一个 Redis 实例承担全部角色」**【官方】[^c3-1]。后四个角色专用块（发布订阅 / 任务队列 / 时间线 / 表情回应）是**给你将来做分流用的模板**——只有当你确实要用多个 Redis 实例分别扛不同职责时，才去取消注释并逐个填。默认用法下，你不需要碰它们。

和数据库一样，`host: redis` 里的 `redis` 就是 compose 里那个 Redis 服务的名字，两者对应【官方】。

> [!tip] 大白话
> 把基础 `redis:` 块想成「一个大通间」，把那四个角色专用块想成「可以分租出去的隔间」。示例默认只开了大通间——**所有活儿由一个 Redis 干**。
> 你现在不需要划分隔间；只有当实例变大、想让不同工作负载互不干扰时，才有必要把隔间（那几个注释块）打开。

---

## 3.6 全文检索：`fulltextSearch.provider` 的出厂值

原文【官方】[^c3-1]：

```yaml
# .config/default.yml
#   ┌───────────────────────────────┐
#───┘ Fulltext search configuration └─────────────────────────────

# These are the setting items for the full-text search provider.
fulltextSearch:
  # You can select the ID generation method.
  # - sqlLike (default)
  #   Use SQL-like search.
  #   This is a standard feature of PostgreSQL, so no special extensions are required.
  # - sqlPgroonga
  #   Use pgroonga.
  #   You need to install pgroonga and configure it as a PostgreSQL extension.
  #   In addition to the above, you need to create a pgroonga index on the text column of the note table.
  #   see: https://pgroonga.github.io/tutorial/
  # - meilisearch
  #   Use Meilisearch.
  #   You need to install Meilisearch and configure.
  provider: sqlLike
```

只讲结论，不展开对比【官方】[^c3-1]：

- 出厂值就是 `provider: sqlLike`；
- 文件自述 `sqlLike` 是 **default（默认值）**；
- 注释明确说它是 **`This is a standard feature of PostgreSQL, so no special extensions are required.`**——使用 PostgreSQL 的**标准能力，不需要安装任何扩展**。

也就是说：**你什么都不用做，这个默认值就能用**。同一段注释里还并列点了另外两个可选项的名字（`sqlPgroonga`、`meilisearch`）；本章不比较这三者、也不给 PGroonga 的安装步骤——只保留一句：**改它们意味着引入额外组件，不属于「跑通最小闭环」的必要动作**。

紧接着还有一段注释掉的 `#meilisearch:` 连接设置块（`host: meilisearch`、`port: 7700`、`apiKey: ''`、`ssl: true`、`index: ''`、`scope: local`）。它是上方注释所说的「只有当你把 `provider` 选成 `meilisearch` 时才需要设置」的那部分，默认**整块注释、不生效**【官方】[^c3-1]。

### 一处文档缺陷：串位的注释

在 `fulltextSearch:` 块的第一行，有一句注释：

```yaml
fulltextSearch:
  # You can select the ID generation method.
```

这句话属于**从 `id` 块复制粘贴时留下的错位注释**——它和全文检索毫无关系（`id` 块里也有一句一字不差的 `# You can select the ID generation method.`）。读到它直接忽略即可，**不要因为这句话去找什么「ID generation」设置**【官方】[^c3-1]。

---

## 3.7 端口与代理绕行：`port` / `proxyBypassHosts`

这两个字段分散在文件的不同区段，但共同点是：**默认值即可，通常不需要改**。

### `port`

```yaml
# .config/default.yml
# The port that your Misskey server should listen on.
port: 3000
```

【官方】`port: 3000` 表示 Misskey 应用在**容器内部**监听 3000。它与上一章 compose 里 `web` 发布的端口映射 `"3000:3000"` 相对应——宿主机的 3000 转发到容器的 3000【官方】[^c3-1]。所以：

- 如果你**不改** compose 的端口映射，这里就保持 `3000`；
- 只有当你在 compose 里换了宿主机端口（比如改成 `"8080:3000"`），才需要关心这个数字的对应关系。

同一区段的注释还画了一张图，说明 Misskey 需要反向代理来支持 HTTPS：用户 → 代理（443）→ Misskey（3000）。这里只是背景——**反代与 TLS 不是本章要解决的问题**，你只需要知道文件里这段注释是在解释「为什么 `url` 用 https、而 `port` 只是内部的 3000」【官方】[^c3-1]。

### `proxyBypassHosts`

这是文件里**少数「生效、但通常无需修改」的区块**——它是一个**非注释的、真实生效的列表**【官方】[^c3-1]：

```yaml
# .config/default.yml
proxyBypassHosts:
  - api.deepl.com
  - api-free.deepl.com
  - www.recaptcha.net
  - hcaptcha.com
  - challenges.cloudflare.com
```

逐条列出（共五项）【官方】[^c3-1]：

| 列表项 | 从域名可直观判断的用途 |
| --- | --- |
| `api.deepl.com` | DeepL 翻译 API |
| `api-free.deepl.com` | DeepL 免费版翻译 API |
| `www.recaptcha.net` | reCAPTCHA 验证 |
| `hcaptcha.com` | hCaptcha 验证 |
| `challenges.cloudflare.com` | Cloudflare 挑战（challenge） |

一眼能看出这是「即使你配了 HTTP 代理，也要绕开、不要走代理」的例外名单（`proxyBypassHosts` 字面意思即「代理绕行主机」）——都是第三方服务的域名，**保持默认即可**。

---

## 3.8 一大片「只以注释存在」的字段

从 `# Other configuration` 区段开始，文件里出现了大量**只有注释、没有生效值**的字段。理解这一段的**模式**比记住每个字段更重要：

> **在这个文件里，被 `#` 注释掉 = 该字段取默认值 + 当前不生效。** 只有把行首的 `#` 去掉（取消注释）并重新加载，它才会起作用【官方】[^c3-1]。

这个模式是通用的：前面 `db.disableCache`、`db.extra.ssl`、Redis 的四个角色块、`#meilisearch:` 块，全部遵循同一条规则——**你不动它，它就不参与运行**。

下面按区段把这一大片字段紧凑列出，方便你扫描。**全部为注释示例、默认不生效**【官方】[^c3-1]：

| 字段 | 注释里的示例值 | 作用（按文件自述） |
| --- | --- | --- |
| `disableHsts` | `true` | 是否禁用 HSTS |
| `clusterLimit` | `1` | worker 进程数 |
| `threadPoolSize` | `1` | 每个 worker 的 CPU 密集任务线程数 |
| `deliverJobConcurrency` | `128` | 每个 worker 的投递任务并发 |
| `inboxJobConcurrency` | `16` | 每个 worker 的收件任务并发 |
| `deliverJobPerSec` | `128` | 投递速率限制 |
| `inboxJobPerSec` | `32` | 收件速率限制 |
| `deliverJobMaxAttempts` | `12` | 投递最大尝试次数 |
| `inboxJobMaxAttempts` | `8` | 收件最大尝试次数 |
| `outgoingAddressFamily` | `ipv4` | 出站请求用的 IP 协议族（`ipv4` / `ipv6` / `dual`） |
| `proxy` | `http://127.0.0.1:3128` | HTTP/HTTPS 代理 |
| `proxySmtp` | `http://127.0.0.1:3128`（另有 `socks4://…`、`socks5://…` 两行备选） | SMTP/SMTPS 代理 |
| `mediaProxy` | `https://example.com/proxy` | 媒体代理 |
| `allowedPrivateNetworks` | `- '127.0.0.1/32'` | 内网上传白名单；文件注明默认值是 `"undefined"` |
| `maxFileSize` | `262144000` | 上传/下载文件大小上限（字节） |
| `logging` | 见下方 | 日志设置块 |
| `sentryForBackend` / `sentryForFrontend` | 见下方 | 错误追踪块 |

其中两个块内容较多，单独说明：

**`logging` 块**（整块注释，取值即示例所写的默认口径）【官方】[^c3-1]：

- `format: pretty` —— 日志输出格式，文件注明「`json` 输出单行 JSON；默认 `pretty`」；
- `level: info` —— 全局最低日志级别，文件注明「生产环境默认 `info`，否则 `debug`」；
- `domains:` —— 按域覆盖级别的例子（`core.boot: info`、`queue: error`、`queue.deliver: debug`、`db.sql: off`），注释说明「匹配最长的日志域优先于全局级别」；
- `access.statusClasses:` —— 访问日志记录的 HTTP 状态类（`'2xx'`、`'3xx'`、`'4xx'`、`'5xx'`），注释说明「未指定则不输出」；
- `access.bodies:` —— `request: false`、`response: false`，附 `maxBytes: 16384`，注释写明「默认 16 KiB，最大 128 KiB」；
- `sql.enableQueryParamLogging: false`（默认 `false`）、`sql.disableQueryTruncation: false`（默认 `false`）。

**`sentryForBackend` / `sentryForFrontend` 块**（整块注释）【官方】[^c3-1]：DSN 占位值均为 `https://examplePublicKey@o0.ingest.sentry.io/0`，属于「接入 Sentry 错误追踪」时才需要的内容，默认完全不参与运行。

另外，`db` 与 `redis` 两段里也各有一小撮注释字段，前文已列出：`db.disableCache`、`db.extra.ssl`、`dbSlaves`，以及 Redis 的 `family`/`pass`/`prefix`/`db` 与四个角色块——它们遵循**同一条注释规则**，此处不再重复。

> [!tip] 大白话
> 把这一大片注释字段想成**出厂设置贴纸上被盖住的那几行**：产品已经按默认参数跑着了，贴纸只是告诉你「如果你想把某项调成别的值，标的是这样」。**没撕开贴纸（去掉 `#`），它就一直是默认值**。
> 所以看到它们**不要慌、不要逐条取消注释**——默认值就是给你用的。

---

## 3.9 YAML 正确性：一个缩进就能让 Misskey 停摆

这是整份文件里**最廉价、也最容易踩**的坑：语法正确性。

三条官方原文【官方】：

1. 关于注释：`In YAML format, everything from `#` to the end of the line is treated as a comment.`（YAML 里，从 `#` 到行尾都算注释）[^c3-3]；
2. 关于缩进（排错页）：`There might be a syntax error in default.yml. Are there any extra spaces at the beginning of a line?`（可能是 `default.yml` 的语法错误——**行首是不是多了空格？**）[^c3-3]；
3. 关于后果（Ubuntu 指南）：`This configuration file is written in YAML format, so be particularly careful with the number of spaces at the beginning of each line; if incorrect, Misskey will not work.`（**行首空格数写错，Misskey 就不会工作**）[^c3-4]。

把这三条合起来：**YAML 用缩进表达层级；行首空格数错一格，整个文件的层级结构就变了，Misskey 直接不工作。** 编辑时务必用等宽编辑器、确认没有混入 Tab、并且别把某个字段的行首缩进多敲一格。

> [!tip] 大白话
> 把 YAML 的缩进想成**楼层号**：`db:` 是 1 楼，它下面缩进两格的 `host`、`port` 是 2 楼——「住在 1 楼的这间房子里」。你如果把某个 2 楼字段多缩了一格，它就被算到别的「房子」底下去了。
> 所以 YAML 里**缩进就是语法**，不是排版美化；多一个空格，Misskey 就读不懂这份文件，于是干脆不工作。

最后再把两条与「编辑方式」相关的提醒收在这里：

- **这份文件的注释就是官方说明书。** 官方让你「按文件里的说明编辑」（`as per the description`）【官方】[^c3-2]，文件里每个字段都自带用途与警告（本章已逐段验证过）。这正是第一章提到的工作方法：**遇到不确定的字段，先读它上面的注释，而不是去别处搜**。
- **本章开头展示的那段「串位注释」是文档缺陷，不是你要处理的配置。** `fulltextSearch:` 块首那句 `# You can select the ID generation method.` 是从 `id` 块复制粘贴的残留，忽略即可【官方】[^c3-1]。

---

## 本章小结

- **`url` 是本章的重心，也是整篇笔记风险最高的一个字段。** 它默认是占位符 `https://example.tld/`，必须改成「用户浏览器地址栏里应该看到的地址」；写错会导致**无法注册**（客户端连不上 API），而**启动后改动极可能导致联邦完全损坏**——唯一的成功案例发生在 Firefish（非 Misskey）上，靠多个自定义脚本操作 API 与数据库，作者自评极其粗糙、不建议效仿。配套的官方禁令是：**不要用已投入使用的服务器域名/主机名去重建数据库**。
- **还有一个同款不可变字段 `id`。** 出厂值 `id: 'aidx'`，备选 `aid`/`aidx`/`meid`/`ulid`/`objectid`，带一字不差的「启动后不可更改」警告；文件自述通常不需要改，保持默认即可。
- **需要动手改的其实很少。** `db.host: db`、`db.port: 5432`、`redis.host: redis`、`redis.port: 6379` 都必须与 compose 的服务名/端口对应（改一处要同步另一处）；`db.user`/`db.pass` 是占位值且必须与 `.config/docker.env` 一致——口令那一半留到下一章。
- **大量字段「只以注释存在」＝取默认值、当前不生效**（`disableCache`、`extra.ssl`、四个 Redis 角色块、`disableHsts`、`clusterLimit`、`threadPoolSize`、各投递并发与重试、`proxy`、`maxFileSize`、`logging`、`sentry*` 等）；不取消注释就不参与运行，**默认值就是给你用的**。
- **两个「无需改动」的出厂设置**：`fulltextSearch.provider: sqlLike` 是默认值、只依赖 PostgreSQL 标准能力、**不需要任何扩展**；`proxyBypassHosts` 是生效的非注释列表（`api.deepl.com`、`api-free.deepl.com`、`www.recaptcha.net`、`hcaptcha.com`、`challenges.cloudflare.com`）。另外，YAML **行首缩进写错会让 Misskey 不工作**，`fulltextSearch` 块首那句串位注释是文档缺陷、可直接忽略。

## 下一章预告

到这里，应用配置已经定死：实例叫什么、连哪个数据库、缓存怎么用、帖子 ID 怎么生成，全部有了答案。但还有一块拼图没接上——`db.user`/`db.pass` 这两个占位值**必须和另一份文件保持一致**，而那份文件还管着数据库容器的启动口令。下一章就进入 `.config/docker.env`，把「口令」这一环补齐，并说清一个反直觉的事实：改了这份文件，并不是所有地方都会跟着变。

---

[^c3-1]: [.config/docker_example.yml（Misskey 官方仓库示例配置文件）](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml)
[^c3-2]: [Building Misskey using Docker Compose（Misskey Hub 官方容器部署指南）](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/)
[^c3-3]: [Troubleshooting Manual Installation（Misskey Hub 官方排错页）](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/)
[^c3-4]: [Detailed guide to installing Misskey on Ubuntu（Misskey Hub 官方 Ubuntu 安装指南）](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/)
[^c3-5]: [Discussion #9254 Changing Instance Domain（Misskey 官方仓库讨论）](https://github.com/misskey-dev/misskey/discussions/9254)
