# 使用 Docker Compose 部署 Misskey - P2 深度素材

- **项目标识**: `misskey-docker-compose-deploy`
- **阶段**: P2（深度收集）
- **检索日期**: 2026-09-15
- **范围**: A（最小可运行闭环）+ C（NAS 落地与运维）
- **正文缓存**: `workspace/misskey-docker-compose-deploy/sources/`

---

## 一、范围与边界

**纳入**：容器化部署的完整链路、compose 服务栈逐项、应用配置必改字段、密钥注入方式、升级流程、镜像与标签策略、近期破坏性变更、硬件门槛、卷权限。

**排除（用户 2026-09-15 决策）**：

| 排除项 | 处理 |
| --- | --- |
| 反向代理与 TLS（B） | 不进正文。仅在解释 `url` 不可变、以及配置示例里的代理注释时作为一句话背景。 |
| 全文检索三种 provider 对比（D） | 不进正文。仅在解释必改字段时说明默认值是 `sqlLike` 且不需要扩展。 |
| 对象存储 | 移除。官方文档与示例文件均无指引。 |
| 邮件发送 | 移除。同上，示例中仅有注释占位。 |

---

## 二、来源表

| ID | 来源 | 层级 | 日期 | 缓存文件 |
| --- | --- | --- | --- | --- |
| S01 | [Building Misskey using Docker Compose](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/) | official | unknown | `S01_docker-guide.md` |
| S02 | [安装资源索引](https://misskey-hub.net/en/docs/for-admin/install/resources/) | official | unknown | `S02_install-resources.md` |
| S04 | [Troubleshooting（手动安装排错）](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/) | official | **页面标注：2018-10-07 撰写，2021-12-20 最后更新** | `S04_troubleshooting.md` |
| S05 | [ノート検索 / Note search](https://misskey-hub.net/en/docs/for-admin/features/search/) | official | unknown | `S05_note-search.md`（正文为日文） |
| S06 | [Detailed guide to installing Misskey on Ubuntu](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/) | official | unknown | `S06_ubuntu-manual.md` |
| S07 | [compose_example.yml](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml) | primary | 2025-12-14（最近改动该路径的提交） | `S07_compose_example.yml.md` |
| S08 | [.config/docker_example.yml](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml) | primary | unknown | `S08_docker_example.yml.md` |
| S09 | [.config/docker_example.env](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.env) | primary | unknown | `S09_docker_example.env.md` |
| S10a | [Release 2026.9.0](https://github.com/misskey-dev/misskey/releases/tag/2026.9.0) | official | 2026-09-06 | `S10a_release_2026.9.0.md` |
| S10b | [Release 2026.7.0](https://github.com/misskey-dev/misskey/releases/tag/2026.7.0) | official | 2026-07-31 | `S10b_release_2026.7.0.md` |
| S11 | [Issue #9613 容器内已上传文件无法访问](https://github.com/misskey-dev/misskey/issues/9613) | primary | 2023-01-16 开、当日关闭 | `S11_issue_9613.md` |
| S12 | [Discussion #9254 Changing Instance Domain](https://github.com/misskey-dev/misskey/discussions/9254) | primary | 2022-12-03 开，2023-11-12 有跟进 | `S12_discussion_9254.md` |

**层级分布**：official 6 / primary 6 / implementation-report 0 / community 0。

**已验证的复核项（2026-09-15，本次 P2 亲自执行）**：

- S07、S08、S09 三份示例文件在 `master` 与 `develop` 分支**逐字节一致**，故不存在「文档让你 checkout master、示例却来自 develop」的版本错配问题（`diff` 验证，三份均 identical）。
- 全部来源中的内存数字穷举后仅有三处：`2GB`（S04 L141、S06 L556）、`1.5 GB`（S06 L161）、`4 GB`（S06 L160）。P1 探测记录里出现的「3GB」**无法复现**，已弃用，不进正文。

---

## 三、主张-来源映射

### 3.1 部署链路（A）

| # | 主张 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| A1 | 唯一前置条件是已安装 Docker 与 Docker Compose，官方未给最低版本要求 | S01 | 前提条件 |
| A2 | 克隆命令为 `git clone -b master https://github.com/misskey-dev/misskey.git`，并在克隆内 `git checkout master` | S01 | Clone the Repository |
| A3 | 配置是三连拷贝：`.config/docker_example.yml`→`.config/default.yml`、`.config/docker_example.env`→`.config/docker.env`、`./compose_example.yml`→`./compose.yml` | S01 | Configuration |
| A4 | 指南要求按文件内注释自行编辑 `default.yml` 与 `docker.env`，并「按需」编辑 `compose.yml`（例如改端口） | S01 | Configuration |
| A5 | 构建与初始化是两条独立命令：`sudo docker compose build`，再 `sudo docker compose run --rm web pnpm run init` | S01 | Build & Initialize |
| A6 | 初始化在一个一次性的 `web` 容器里执行（`--rm`），不是独立的 init 服务 | S01 | Build & Initialize |
| A7 | 启动命令是 `sudo docker compose up -d` | S01 | Startup |
| A8 | 指南中所有命令都带 `sudo` 前缀 | S01 | 多处 |
| A9 | 临时后端 CLI 命令复用同一模式：`sudo docker compose run --rm web node packages/backend/built/tools/foo bar` | S01 | How to execute CLI commands? |

### 3.2 服务栈与依赖顺序（A / C）

| # | 主张 | 来源 |
| --- | --- | --- |
| A10 | 编排示例启用三个服务：`web`（`build: .` 本地构建）、`redis`（`redis:7-alpine`）、`db`（`postgres:18-alpine`） | S07 |
| A11 | `web` **不是**从 registry 拉取镜像，而是用仓库根目录的 Dockerfile 本地构建，因此部署机器上必须有完整源码树 | S07 |
| A12 | `web` 以只读方式挂载 `./.config:/misskey/.config:ro`，所以应用配置必须放在 compose 文件旁的 `.config/` 目录 | S07 |
| A13 | `db` 服务启用了 `env_file: .config/docker.env`；`web` 服务的 `env_file` 行**默认被注释掉** | S07 |
| A14 | `web` 通过 `depends_on` + `condition: service_healthy` 等待 `db` 与 `redis` 双双健康后才启动 | S07 |
| A15 | `redis` 健康检查为 `redis-cli ping`，`interval: 5s`、`retries: 20` | S07 |
| A16 | `db` 健康检查为 `pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB`，`interval: 5s`、`retries: 20` | S07 |
| A17 | 两个健康检查都只设了 `test`/`interval`/`retries`，**未设** `timeout` 与 `start_period` | S07 |
| A18 | 只有 `web` 发布宿主端口 `"3000:3000"`；`redis`(6379) 与 `db`(5432) 不发布端口，仅容器网络内可达 | S07 |
| A19 | 声明两个网络：`internal_network`（`internal: true`）与 `external_network`（无配置） | S07 |
| A20 | `web` 同时加入两个网络；`redis` 与 `db` 只加入 `internal_network` | S07 |
| A21 | `web` 声明 `links` 指向 `db` 与 `redis` | S07 |
| A22 | `db` 数据落 `./db` 挂到 `/var/lib/postgresql`（注意**不是** `/var/lib/postgresql/data`） | S07 |
| A23 | `redis` 数据落 `./redis` 挂到 `/data` | S07 |
| A24 | `web` 的持久化目录是 `./files` 挂到 `/misskey/files` | S07 |
| A25 | 三个服务均设 `restart: always` | S07 |
| A26 | 另有三个服务仅以注释形式存在：`mcaptcha`(`mcaptcha/mcaptcha:latest`)、`mcaptcha_redis`(`mcaptcha/cache:latest`)、`meilisearch`(`getmeili/meilisearch:v1.3.4`) | S07 |
| A27 | 注释中的 `meilisearch` 只加入 `internal_network`，密钥来自 `.config/meilisearch.env`，设 `MEILI_NO_ANALYTICS=true`、`MEILI_ENV=production`，数据落 `./meili_data:/meili_data`，无端口无健康检查 | S07 |
| A28 | 注释中的 `mcaptcha` 是唯一放在 `external_network` 上并带别名 `localhost` 的服务，暴露 7493，依赖健康的 `db` 与 `mcaptcha_redis` | S07 |
| A29 | 应用配置的 host 值与 compose 服务名一一对应：`db.host: db`、`redis.host: redis`，端口 `5432`/`6379`；改一处的服务名必须同步改另一处 | S07 + S08 |
| A30 | 应用配置 `port: 3000` 与 compose 发布的 `"3000:3000"` 对应 | S07 + S08 |

### 3.3 配置字段（A）

| # | 主张 | 来源 |
| --- | --- | --- |
| A31 | `url` 必须改成用户最终看到、可访问的地址，示例值是占位符 `https://example.tld/` | S08 |
| A32 | `url` 也可以改用环境变量提供，但示例未写出该变量名 | S08 |
| A33 | `db.db` 示例默认 `misskey`；`db.user` / `db.pass` 是占位值 `example-misskey-user` / `example-misskey-pass`，可用环境变量覆盖 | S08 |
| A34 | `db.disableCache`（默认 `true`）与 `db.extra.ssl` 仅以注释示例出现，即默认开启缓存、关闭 SSL | S08 |
| A35 | `dbReplications` 显式为 `false`；`dbSlaves` 副本列表仅以注释模板存在 | S08 |
| A36 | Redis 只启用基础块（`host: redis`、`port: 6379`），`family`/`pass`/`prefix`/`db` 及四个角色专用块（`redisForPubsub`、`redisForJobQueue`、`redisForTimelines`、`redisForReactions`）**全部注释掉**——默认一个 Redis 实例承担所有角色 | S08 |
| A37 | `fulltextSearch.provider` 显式设为 `sqlLike`，文件自述这是默认值；该值使用 PostgreSQL 标准能力，**不需要任何扩展** | S08 + S05 |
| A38 | `id` 显式设为 `'aidx'`；备选有 `aid`(短、毫秒精度)、`meid`、`ulid`、`objectid`(向后兼容保留) | S08 |
| A39 | `port` 设为 `3000` | S08 |
| A40 | `proxyBypassHosts` 是生效的非注释列表，内容为 `api.deepl.com`、`api-free.deepl.com`、`www.recaptcha.net`、`hcaptcha.com`、`challenges.cloudflare.com` | S08 |
| A41 | 以下字段均为注释示例、取默认值，不取消注释即不生效：`disableHsts: true`、`clusterLimit: 1`、`threadPoolSize: 1`、`deliverJobConcurrency: 128`、`inboxJobConcurrency: 16`、`deliverJobPerSec: 128`、`inboxJobPerSec: 32`、`deliverJobMaxAttempts: 12`、`inboxJobMaxAttempts: 8`、`outgoingAddressFamily: ipv4`、`maxFileSize: 262144000`、`allowedPrivateNetworks`（默认 undefined） | S08 |
| A42 | `logging` 块为注释示例，记录默认 `format: pretty`、生产环境 `level: info`（否则 `debug`）、`sql.enableQueryParamLogging: false`、`sql.disableQueryTruncation: false`、请求/响应体日志默认关闭且 `bodies.maxBytes: 16384`（注释写「默认 16 KiB，最大 128 KiB」） | S08 |
| A43 | `sentryForBackend` / `sentryForFrontend` 均为注释示例，DSN 占位 `https://examplePublicKey@o0.ingest.sentry.io/0` | S08 |
| A44 | 示例文件中 `POSTGRES_PASSWORD` 携带**可直接生效的占位值** `example-misskey-pass`，照抄不改会得到一个数据库口令公开可知的实例 | S09 |
| A45 | `POSTGRES_USER` 默认 `example-misskey-user`，`POSTGRES_DB` 默认 `misskey` | S09 |
| A46 | `DATABASE_URL` 由三个 `POSTGRES_*` 值经 `${VAR}` 插值拼出：`postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}`，因此依赖加载它的程序支持变量展开 | S09 |
| A47 | 文件另有三行注释备选 `DATABASE_PASSWORD` / `DATABASE_USER` / `DATABASE_DB`，各回指对应的 `POSTGRES_*` 值，说明 Misskey 也能分项读取而非只认单一 URL | S09 |
| A48 | `MISSKEY_URL` 存在但被注释，示例值 `https://example.tld/`，文件中未解释其用途 | S09 |
| A49 | 配置文件是 YAML，`#` 之后为注释，且**行首空格数写错会导致 Misskey 无法工作** | S04 + S06 |

### 3.4 不可变字段（A / C，高风险）

| # | 主张 | 来源 |
| --- | --- | --- |
| A50 | `url` 所在的配置块带明确警告：**实例启动后不得更改** | S08（`# ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE`） |
| A51 | `id` 生成方式带同样的启动后不可更改警告 | S08 |
| A52 | 指南在页面标题下以 Danger 提示：**一旦开始使用，不要用该服务器的域名/主机名重新创建数据库** | S01 |
| A53 | `url` 配置错误是「无法注册」的一条具名原因——客户端连不上 API | S04 |
| A54 | 安装指南把域名/主机名同样列为启用后不可更改，并在 Danger 提示中重申不得为已投入使用的域名重建数据库 | S06 |
| A55 | 社区维护者答复：实例 URL 启动后基本不可更改，改动「极可能导致联邦完全损坏」；唯一成功案例是在 Firefish（非 Misskey）上用多个自定义脚本同时操作 API 与数据库，作者自评极其粗糙、不建议效仿 | S12 |

### 3.5 升级与运维（C）

| # | 主张 | 来源 |
| --- | --- | --- |
| C1 | 容器版更新流程：`git stash` → `git checkout master` → `git pull` → `git submodule update --init` → `git stash pop` → `sudo docker compose build` → 重启 | S01 |
| C2 | 该流程刻意 stash 本地改动再 pop 回来，以保留本地配置修改 | S01 |
| C3 | 指南在更新处警告：更新前务必查阅 release notes / `CHANGELOG.md`，提前确认是否需要额外步骤（通常不需要） | S01 |
| C4 | 更新耗时取决于更新内容与数据库规模 | S01 |
| C5 | 更新路径中**没有**重复 `pnpm run init`，且除「通常不需要额外步骤」外没有任何关于迁移的说明，未给出显式迁移命令 | S01 |
| C6 | 镜像标签策略：`redis:7-alpine`、`postgres:18-alpine` 固定，注释里的 `getmeili/meilisearch:v1.3.4` 固定；注释里的 `mcaptcha/mcaptcha:latest`、`mcaptcha/cache:latest` 浮动 | S07 |
| C7 | 官方只提供本地构建路径，未给出 registry 预构建镜像与版本固定策略；仓库内另存有一个推送到 Docker Hub 的 GitHub Actions 示例 `/.github/workflows/docker.yml` | S01 + S02 |
| C8 | 2026.7.0 把 Docker 镜像的 Node.js 升到 26.4.0、Debian 升到 trixie (v13) | S10b |
| C9 | 2026.7.0 把最低 Node.js 版本提高到 **22.22.2 / 24.17.0 / 26.4.0**；v24 与 v26 受支持，v22 仍可用但计划在未来版本移除支持 | S10b |
| C10 | 2026.7.0 起，**不支持 SSE4.2 指令集的 x86_64 CPU 将无法正确运行 Misskey**，成因是图像处理库 sharp 的系统要求变更；影响虚拟机与老旧硬件，**不影响 ARM64 等非 x86_64 环境** | S10b |
| C11 | 2026.7.0 起，NSFW/敏感媒体判定改为对外部服务 `sensitive-detector` 的 HTTP 调用；主进程仍自行完成图像归一化、视频抽帧、阈值判定与聚合 | S10b |
| C12 | 因此 `nsfwjs` / `@tensorflow/tfjs` / `@tensorflow/tfjs-node` 与内置模型被移出 Misskey 包，原生 ML 栈的安装要求得以放宽 | S10b |
| C13 | 依赖敏感媒体检测的实例需自行部署 `sensitive-detector` 并在控制台「モデレーション > センシティブなメディアの検出」填连接地址；**未填则不进行任何判定，一切按非敏感处理** | S10b |
| C14 | 2026.7.0 的 YAML 解析器校验更严格，`example.yml` 里原本合法的写法可能在启动时报语法错误；被点名的例子是 `allowPrivateNetworks`，需把数组闭合括号缩进提高或改写为 list 形式 | S10b |
| C15 | 2026.7.0 移除了从 2025.4.0 及更早版本迁移客户端设置的能力；若想迁移，必须**先经过一次 2026.5.1** | S10b |
| C16 | 2026.9.0 是安全版本，含 7 个 GHSA 公告，上游明确要求尽快升级到该版本或最新版 | S10a |
| C17 | 2026.9.0 **未重述或修订** 2026.7.0 的上述要求变更 | S10a（推断：全文未见相关条目） |

### 3.6 硬件与资源（C）

| # | 主张 | 来源 |
| --- | --- | --- |
| C18 | 构建 Misskey 并执行数据库迁移（含初始化）**至少需要 2GB RAM**；内存不足是服务端构建失败的具名原因，缓解手段为加 swap，或在本机构建后经 SFTP 传构建产物 | S06 |
| C19 | 排错页独立表述：经验上构建 Misskey 至少需要 2GB 内存 | S04 |
| C20 | **推荐约 4 GB 内存** | S06 |
| C21 | 曾有过「因引入 Vite，约 1.5 GB 内存即可完成构建」的说法，但前端构建需求后来再次变高 | S06 |
| C22 | 支持的架构为 **amd64 与 arm64**；「较新的 CPU」被描述为足以以极少资源运行 | S06 |
| C23 | 容器版指南（S01）与 env 示例（S09）**均未给出任何内存/CPU/磁盘数字**，只有 S02 指向单独的 Scaling 文章 | S01 + S02 + S09 |
| C24 | 应用配置中唯一与资源相关的可调项是 `clusterLimit`（worker 进程数）与 `threadPoolSize`（每 worker 的 CPU 密集任务线程数），两者均注释、默认 `1` | S08 |

### 3.7 卷权限与故障（C）

| # | 主张 | 来源 |
| --- | --- | --- |
| C25 | v13 时代的容器内 `/misskey/files/` 文件属主为数字 UID/GID **991** | S11 |
| C26 | 当时的报错是容器内对具体文件路径的权限拒绝，`Error: EACCES: permission denied, open '/misskey/files/...'`，对客户端表现为 HTTP 500 | S11 |
| C27 | 该问题**同时影响已有文件的访问与新的上传**，不限于历史文件 | S11 |
| C28 | 报告者执行 `sudo chown -hR 991:991 ./files` 后仍无法恢复访问 | S11 |
| C29 | 该 issue 在开启当日即被关闭，正文中**未记录修复提交、修复版本或绕过方法** | S11 |
| C30 | 无任何来源给出当前版本容器的具体 UID/GID，也不存在 `PUID`/`PGID` 式配置变量；唯一数字是 v13 的 `991:991` | S11（综合性推断） |

### 3.8 其他运维要点（C，附带）

| # | 主张 | 来源 |
| --- | --- | --- |
| C31 | 官方建议用 nginx 作反向代理、不要把 Misskey 直接暴露到公网；S01 全文**未提反代与 TLS** | S02 + S01 |
| C32 | 官方强烈建议对外发布时使用 Cloudflare 等 CDN | S02 |
| C33 | 反代若阻断 WebSocket，客户端会一直显示「Reconnecting」、时间线不再实时更新 | S04 |
| C34 | Cloudflare 的 Rocket Loader 或 Auto Minify 开启会导致页面加载永远不结束 | S04 |
| C35 | 生产环境必须设 `NODE_ENV=production`，否则服务端顶部显示红色「This is a development build」 | S04 |
| C36 | PostgreSQL 建议 v13 及以上；Redis 为缓存与内部通信（含联邦相关处理）的必需组件，配置为 `host` + `port 6379` | S04 + S06 |
| C37 | Misskey 11.20.2 之前的版本无法解析 Redis 密码，故 Redis 必须无密码且 `redis:` 下的 `pass:` 需注释掉 | S04 |
| C38 | FFmpeg 用于处理视频与音频；ImageMagick **明确不需要** | S06 + S04 |
| C39 | 家用服务器场景下，除 DNS 记录正确外，路由器还需放行 80 与 443 的入站连接 | S06 |
| C40 | 开发环境可用 `url: http://localhost:3000` 替代公网域名 | S06 |
| C41 | 对象存储故障的一条具名原因是对象权限过严，需保证「文件（对象）可被任何人获取」 | S04 |
| C42 | fork 或修改 Misskey 源码会触发 AGPL-3.0 的修改披露义务 | S02 |

**边界说明（与本期决策相关但有价值，留档备查）**：

- S05 记载：选用 PGroonga 时需把 `postgres:18-alpine` 换成 `groonga/pgroonga:latest-alpine-18-slim`，并手工 `CREATE EXTENSION pgroonga;` 与建索引，且**迁移不会自动创建**；启用前需备份数据库并停止 Misskey；建索引耗时较长。另：Meilisearch 无法检索关注者限定帖；Misskey 的笔记搜索**默认为关闭**，需在角色中开启「ノート検索の利用」。以上属 D 范围，本期不展开。
- S06 记载：`proxySmtp` 与 `mediaProxy` 在示例中仅为注释占位。邮件与对象存储官方无指导，本期已移除。

---

## 四、口径冲突与文档缺陷

### 4.1 冲突 1：Node.js 版本（需以发布说明为准）

| 来源 | 说法 |
| --- | --- |
| S06 | 安装命令 pin `NODE_MAJOR=20`，但同页验证文字却说「如果输出类似 v22.x.x 则安装成功」——**页面内部自相矛盾** |
| S10b | 最低运行版本提高到 `22.22.2 / 24.17.0 / 26.4.0` |

**处理**：S06 的 Node 相关内容已过时，正文不得引用其版本号。以 S10b 为准。

### 4.2 并非冲突：内存的三个数字口径不同

| 数字 | 口径 | 来源 |
| --- | --- | --- |
| 2GB | **构建 + 迁移**的硬地板 | S04、S06 |
| 1.5 GB | 历史上曾成立、现已失效 | S06 |
| 4 GB | **推荐**（面向运行整体） | S06 |

**处理**：三者 scope 不同，不得合并为单一数字，也不得表述为「官方要求 X GB」。正文按「构建地板 2GB / 推荐 4GB」并列呈现。

### 4.3 已弃用的 P1 说法

P1 探测记录提到「安装脚本总可用内存至少 3GB」。本次 P2 对全部缓存来源做了穷举检索，**该数字无法复现**，判定为不可靠，不进正文。

### 4.4 文档缺陷（影响读者照抄）

| 缺陷 | 来源 | 说明 |
| --- | --- | --- |
| 更新流程末行拼接错误 | S01 | 页面印成 `sudo docker compose stop sudo docker compose up -d`，两条命令粘连、无分隔符，**照抄不可执行**，实为停服与启动两步 |
| 页面目录不完整 | S01 | 页内 ToC 只列 "Clone the Repository" 与 "How to execute CLI commands?"，遗漏 Configuration、Build & Initialize、Startup、Updating 四节，不可当作步骤索引 |
| 注释串位 | S08 | `fulltextSearch` 块里带着一句「You can select the ID generation method.」，属于从 `id` 块复制粘贴留下的错位注释，与上下文无关 |
| 排错页严重过时 | S04 | 页面标注 2018-10-07 撰写、2021-12-20 最后更新；其中 Redis 密码条目针对 11.20.2 之前的版本，已不适用于当前版本线 |
| 安装指南部分过时 | S06 | Node 版本 pin 与验证文字矛盾（见 4.1），构建内存说明也以「历史上曾」的口径表述 |

### 4.5 安全与配置陷阱

| 项 | 说明 | 来源 |
| --- | --- | --- |
| 占位口令可直接生效 | `POSTGRES_PASSWORD=example-misskey-pass` 在示例中是**有效值**而非空占位，照抄不改会产生口令公开可知的数据库 | S09 |
| `web` 默认不读 env 文件 | `web` 服务的 `env_file` 行默认注释，实际配置走 `.config` 只读挂载；`db` 则确实读 `docker.env`。因此「改了 `docker.env` 就全局生效」是错误预期 | S07 |
| `.config/docker.env` 是隐式必需 | 因为 `db.env_file` 生效，该文件缺失会直接影响 `db` 启动 | S07 |
| 三份示例的职责易混淆 | 根目录 `compose_example.yml` 是编排；`.config/docker_example.yml` 是应用配置；`.config/docker_example.env` 是数据库口令。三者名字相近但用途完全不同 | S01 + S07 + S09 |

---

## 五、实践指引（供写作阶段直接取材）

### 5.1 必改清单（照抄示例后必须改，否则有风险或跑不起来）

1. `.config/docker.env` 里的 `POSTGRES_PASSWORD`（占位值可直接生效）。
2. `.config/default.yml` 里的 `url`（占位 `https://example.tld/`，且**启动后不可更改**）。
3. `.config/default.yml` 里的 `db.user` / `db.pass`（占位值与 `docker.env` 需一致）。
4. 按需改 `compose.yml` 的端口映射（`"3000:3000"`）。

### 5.2 依赖顺序（NAS 上尤其重要）

示例已内置依赖顺序：`web` 等 `db` 与 `redis` 双双 `service_healthy` 才启动，两个健康检查各 `interval: 5s`、`retries: 20`。因此**不需要**手工先起数据库；但这也意味着 NAS 上磁盘 I/O 慢时，首次 `up` 的等待时间会更长。两个健康检查都未设 `timeout` 与 `start_period`，慢速存储上可能提前判定失败。

### 5.3 NAS / 自建服务器上的实际约束（本文档推断部分，需标注）

- **构建 vs 预构建**：官方只给 `build: .` 本地构建路径，而构建需要完整源码树与至少 2GB 可用内存。NAS 上直接构建是内存风险的主要来源。官方未提供预构建镜像方案；仓库内仅有推送到 Docker Hub 的 GitHub Actions 示例。
- **CPU 指令集硬门槛**：2026.7.0 起 x86_64 必须支持 SSE4.2。老旧 NAS 的 Celeron/Atom 可能不满足，需在采购/选型前确认。ARM64 不受此限。
- **卷权限**：`./files`、`./db`、`./redis` 三个绑定挂载目录需可写；v13 曾出现 UID/GID 991 导致的 EACCES 与 HTTP 500，当前版本实际 UID/GID 无来源可确认。
- **仅内网使用**：官方文档**完全没有**覆盖无公网域名的场景（反代文档只给公网域名 + Let's Encrypt 的配置）。此部分为本文档推断，必须显式标注。
- **`docker compose` 版本**：官方只要求「已安装」，未给最低版本。示例使用 `depends_on.condition: service_healthy` 与顶层 `networks`，需要 Compose v2。

---

## 六、遗留问题（写作阶段不得当作已知事实）

1. **当前版本容器的实际 UID/GID 未知**，也没有 `PUID`/`PGID` 类变量；C25–C30 全部限于 v13。
2. **v13 的卷权限问题是否已修复、以何种方式修复，无可查来源**；issue 当日关闭且未记录修复。
3. **2GB 构建地板是否仍适用于 2026.7.0 之后的版本**未知——该数字出自 S04（2021）与 S06，两地都早于近期的 Node/Debian 大版本跃迁。
4. **2026.9.0 是否调整了 2026.7.0 的 SSE4.2 / Node 最低版本 / sensitive-detector 要求**，发布说明未重述，无从判断。
5. **NAS 专属一手实操记录未找到**，只有聚合类二手教程，本期已不再依赖。
6. **仅内网部署方案无官方依据**，属需要自行设计的空白区。
7. **`sensitive-detector` 的部署方式**（是否也走 compose、资源占用）本期未收集；只知未配置则不检测。
8. **文档语言版本差异未比对**：日文、简体中文、繁体中文版文档均存在，正文内容差异未逐字核对。

---

## 七、下游交接

**给 outline-generator**：

- 结构应围绕「A 的可执行链路 + C 的落地约束」组织，不要把 A 与 C 拆成互不相干的两半——NAS 的约束应当在跑通步骤的对应位置就近出现（例如讲构建时就带出内存地板与 SSE4.2，讲挂载时就带出卷权限）。
- 素材锚点按上表 `A1–A55`、`C1–C42` 编号引用，写作阶段回源时按编号定位。
- 必须在正文中显式区分三类内容：**官方明示**（S01–S12 直接陈述）、**本文档推断**（第五节 5.3 与仅内网方案）、**已过时信息**（S04 的 Redis 密码条目、S06 的 Node 版本）。
- 内存数字按「构建地板 2GB / 推荐 4GB」两个口径并列，禁止合并。
- 不得引用 S04 的 Redis 密码指引与 Node 版本 pin；不得使用 P1 记录的「3GB」。
- 全文只依赖官方一手来源即可成立，无需引入社区二级来源。

**给 chapter-writer**：

- 引用来源时用 S-ID + 锚点，不要复述本文件的措辞——本文件是提炼，不是原文；凡需要逐字精确的（命令、字段名、数字、目录路径）必须回源到 `sources/` 下对应缓存文件核对。
- 命令块中的 `sudo` 前缀是官方原文，保留。
- S01 更新流程末行的粘连命令**不要照抄**，按「停服」「启动」两步写并加注说明。
