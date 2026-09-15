## 学习笔记大纲：《使用 Docker Compose 部署 Misskey》

> 笔记类型：实战笔记（按「文件 / 产物」组织，顶级章节对应一个具体产物或一段操作规程）
> 预计总篇幅：约 20–28 页
> 章节数：6
> 素材标注约定：`【官方】`＝官方文档或官方仓库一手文件直接陈述；`【推断】`＝本文档推断、无官方来源；`【过时】`＝已失效信息，须按历史口径呈现。

---

### 第一章：部署前置——克隆源码与三份产物的落位

- **篇幅**：短
- **覆盖要点**：
  - 唯一前置条件是已安装 Docker 与 Docker Compose，官方未给最低版本要求 【官方】
  - 克隆命令 `git clone -b master …`，并在克隆目录内 `git checkout master` 【官方】
  - 三连拷贝：`compose_example.yml` → `compose.yml`、`.config/docker_example.yml` → `.config/default.yml`、`.config/docker_example.env` → `.config/docker.env` 【官方】
  - 三份产物职责辨析：根目录文件是编排、`.config` 下 yml 是应用配置、`.config` 下 env 是数据库口令；三者名字相近但用途完全不同 【官方】
  - 编辑方式：按文件内注释改 `default.yml` 与 `docker.env`，「按需」改 `compose.yml`（例如端口） 【官方】
  - 命令均带 `sudo` 前缀，属官方原文，保留 【官方】
  - 文档缺陷提醒：该页 ToC 只列两节，遗漏 Configuration / Build & Initialize / Startup / Updating 四节，不可当作步骤索引 【官方】
- **素材引用**：A1, A2, A3, A4, A8, S01, S07, S09
- **代码示例**：有

### 第二章：`compose.yml`——服务栈、依赖顺序、网络与挂载

- **篇幅**：长
- **覆盖要点**：
  - 三个启用服务与镜像：`web`（`build: .` 本地构建）、`redis:7-alpine`、`db: postgres:18-alpine` 【官方】
  - `web` 不从 registry 拉镜像，而是用仓库根目录 Dockerfile 本地构建，NAS 上因此必须保留完整源码树 【官方】
  - 依赖顺序：`depends_on` + `condition: service_healthy`，`web` 等 `db` 与 `redis` 双双健康才启动 【官方】
  - 两个健康检查：`redis-cli ping` 与 `pg_isready`，均 `interval: 5s`、`retries: 20`；未设 `timeout` 与 `start_period` 【官方】
  - 端口：只有 `web` 发布 `"3000:3000"`，`redis`(6379) 与 `db`(5432) 不发布，仅容器网络内可达 【官方】
  - 网络：`internal_network`（`internal: true`）与 `external_network`；`web` 双网络，`redis`/`db` 仅 internal；`web` 另声明 `links` 【官方】
  - 绑定挂载三处：`./db` → `/var/lib/postgresql`（注意不是 `…/data`）、`./redis` → `/data`、`./files` → `/misskey/files` 【官方】
  - `.config` 以只读方式挂载进 `web`，所以应用配置必须放在 compose 文件旁的 `.config/` 【官方】
  - 卷权限就近说明：三个绑定挂载目录需可写；v13 曾出现容器内 UID/GID `991` 导致的 `EACCES`，对客户端表现为 HTTP 500，且同时影响已有文件访问与新上传，报告者 `chown -hR 991:991` 后仍不可访问，issue 当日关闭未记录修复 【官方】
  - 当前版本容器的实际 UID/GID 无来源可确认，也不存在 `PUID`/`PGID` 类变量（遗留项，不得断言已修复） 【官方】
  - 三个服务均 `restart: always` 【官方】
  - 仅以注释存在的 `mcaptcha`、`mcaptcha_redis`、`meilisearch` 不启用（本轮不展开其配置） 【官方】
- **素材引用**：A10–A28, C25–C30, S07, S11
- **代码示例**：有

### 第三章：`.config/default.yml`——应用配置必改字段与不可变项

- **篇幅**：长
- **覆盖要点**：
  - `url` 必须改成用户最终看到、可访问的地址，示例值仅为占位符 `https://example.tld/` 【官方】
  - `url` 所在配置块带明确警告：实例启动后不得更改 【官方】
  - 配套 Danger 提示：不得用该服务器域名/主机名重新创建数据库 【官方】
  - `url` 配置错误是「无法注册」的具名原因；社区结论是启动后改动「极可能导致联邦完全损坏」，唯一成功案例不在 Misskey 上且被作者自评为不建议效仿 【官方】
  - `url` 也可由环境变量提供，但示例未写出变量名 【官方】
  - `db.host: db` / `db.port: 5432` 与 compose 服务名一一对应，改一处必须同步另一处 【官方】
  - `db.db` / `db.user` / `db.pass` 为占位值，且须与 `docker.env` 保持一致 【官方】
  - `db.disableCache`（默认 `true`）与 `db.extra.ssl`（默认关）仅以注释示例出现 【官方】
  - `dbReplications` 显式 `false`，`dbSlaves` 副本列表仅为注释模板 【官方】
  - Redis 只启用基础块（`host`/`port`），`family`/`pass`/`prefix`/`db` 及四个角色专用块全部注释——默认单个 Redis 实例承担所有角色 【官方】
  - `fulltextSearch.provider` 显式设为 `sqlLike`，这是默认值，使用 PostgreSQL 标准能力、不需要任何扩展（不做 provider 对比） 【官方】
  - `id` 显式 `'aidx'`，备选有 `aid`/`meid`/`ulid`/`objectid`，并带同样的启动后不可更改警告 【官方】
  - `port: 3000` 与 compose 发布的端口对应 【官方】
  - `proxyBypassHosts` 是生效的非注释列表（DeepL、reCAPTCHA、hCaptcha、Cloudflare challenge 域名） 【官方】
  - 大量仅注释示例字段（`disableHsts`、`clusterLimit`、`threadPoolSize`、各投递并发、日志块、Sentry 块、`maxFileSize` 等）：不取消注释即不生效，取值即默认 【官方】
  - YAML 注意点：`#` 之后为注释，行首缩进写错会直接导致 Misskey 无法工作 【官方】
  - 文档缺陷提醒：`fulltextSearch` 块里有一句从 `id` 块复制粘贴残留的错位注释，可忽略 【官方】
- **素材引用**：A29, A31–A43, A49, A50, A51, A52, A53, A54, A55, S04, S05, S06, S08, S12
- **代码示例**：有

### 第四章：`.config/docker.env`——数据库口令与变量注入

- **篇幅**：短
- **覆盖要点**：
  - `POSTGRES_PASSWORD` 在示例中是**可直接生效的占位口令**，照抄不改会得到口令公开可知的实例（安全陷阱） 【官方】
  - `POSTGRES_USER` 默认 `example-misskey-user`，`POSTGRES_DB` 默认 `misskey` 【官方】
  - `DATABASE_URL` 由三个 `POSTGRES_*` 经 `${VAR}` 插值拼出：`postgres://…@db:5432/…` 【官方】
  - 另有三行注释备选 `DATABASE_PASSWORD` / `DATABASE_USER` / `DATABASE_DB`，说明 Misskey 也能分项读取而非只认单一 URL 【官方】
  - `MISSKEY_URL` 存在但被注释，示例未解释用途 【官方】
  - `web` 服务的 `env_file` 行默认被注释，实际配置走 `.config` 只读挂载；因此「改了 `docker.env` 就全局生效」是错误预期 【官方】
  - `.config/docker.env` 是隐式必需文件：`db` 的 `env_file` 确实生效，文件缺失会直接影响 `db` 启动 【官方】
- **素材引用**：A13, A44–A48, S07, S09
- **代码示例**：有

### 第五章：构建 → 初始化 → 启动——跑通链路

- **篇幅**：中
- **覆盖要点**：
  - 第一步构建：`sudo docker compose build` 【官方】
  - 内存门槛（地板）：构建 Misskey 并执行数据库迁移（含初始化）**至少需要 2GB RAM**；内存不足是服务端构建失败的具名原因，缓解手段为加 swap，或在本机构建后经 SFTP 传构建产物 【官方】
  - 内存门槛（推荐）：**推荐约 4GB**，面向运行整体。与 2GB 是两个不同口径，必须并列呈现、不得合并为一个数字 【官方】
  - 历史口径：曾有过「约 1.5GB 即可完成构建」的说法，因前端构建需求回升而失效，仅作历史说明 【官方】
  - CPU 硬门槛：2026.7.0 起，不支持 SSE4.2 的 x86_64 CPU 将无法正确运行 Misskey（成因是图像处理库 sharp 的系统要求变更），影响虚拟机与老旧硬件，**不影响 ARM64** 【官方】
  - 支持架构为 amd64 与 arm64 【官方】
  - 注意：容器版指南与 env 示例均未给出任何内存/CPU/磁盘数字 【官方】
  - 第二步初始化：`sudo docker compose run --rm web pnpm run init`，在一次性 `web` 容器中执行，不是独立 init 服务 【官方】
  - 第三步启动：`sudo docker compose up -d` 【官方】
  - NAS 落地提示：磁盘 I/O 慢会让首次 `up` 的等待明显更久，且健康检查未设 `timeout`/`start_period`，慢速存储上可能被提前判定失败 【推断】
  - 临时后端 CLI 复用同一模式：`sudo docker compose run --rm web node packages/backend/built/tools/foo bar` 【官方】
- **素材引用**：A5, A6, A7, A9, C10, C18, C19, C20, C21, C22, C23, S01, S06, S10b
- **代码示例**：有

### 第六章：升级流程与 NAS 遗留约束

- **篇幅**：中
- **覆盖要点**：
  - 升级六步：`git stash` → `git checkout master` → `git pull` → `git submodule update --init` → `git stash pop` → `sudo docker compose build` → 重启；刻意 stash/pop 是为了保留本地配置改动 【官方】
  - 升级路径**没有**重复 `pnpm run init`，也没有显式迁移命令；官方只提示「通常不需要额外步骤」 【官方】
  - 升级前务必查 release notes / `CHANGELOG.md`，确认是否需要额外步骤；耗时取决于更新内容与数据库规模 【官方】
  - 文档缺陷：S01 更新流程末行两条命令粘连成 `sudo docker compose stop sudo docker compose up -d`，照抄不可执行，须拆为「停服」「启动」两步并加注 【官方】
  - 镜像标签策略：`redis`/`postgres`/注释中的 `meilisearch` 固定版本，注释中的 `mcaptcha` 浮动；官方只提供本地构建路径，未给 registry 预构建镜像与版本固定策略 【官方】
  - 2026.9.0 是安全版本（含 7 个 GHSA 公告），官方要求尽快升级 【官方】
  - 2026.7.0 的 YAML 解析校验更严格，`allowPrivateNetworks` 等写法可能在启动时报语法错误，需调整缩进或改写为 list 形式 【官方】
  - 2026.7.0 移除了从 2025.4.0 及更早版本迁移客户端设置的能力，如需迁移必须先经过一次 2026.5.1 【官方】
  - 2026.7.0 起 NSFW 判定改为对外部服务 `sensitive-detector` 的 HTTP 调用，未配置则不做任何判定、一切按非敏感处理 【官方】
  - 【过时】Node.js 版本 pin：S06 安装命令 pin `NODE_MAJOR=20`，与同页验证文字自相矛盾；正文不得引用该版本号，以发布说明（最低 22.22.2 / 24.17.0 / 26.4.0，v22 计划移除）为准 【过时】
  - 【过时】Redis 密码条目：排错页称 11.20.2 之前版本无法解析 Redis 密码、故必须无密码且注释 `redis.pass`；该页标注 2018 年撰写、2021 年最后更新，仅作历史说明 【过时】
  - 【推断】仅内网 / 无公网域名方案：官方文档完全未覆盖该场景（反代文档只给公网域名 + Let's Encrypt 的配置），此部分为本文档推断，需自行设计并显式标注 【推断】
  - 【推断】NAS 分步指引：未找到 NAS 专属一手实操记录，只有聚合类二手教程，本期不再依赖；相关步骤按通用路径改写并标注 【推断】
  - 【推断】`docker compose` 版本：官方只要求「已安装」；示例使用 `depends_on.condition: service_healthy` 与顶层 `networks`，实际需要 Compose v2 【推断】
  - 遗留项（不得当作已知事实）：v13 卷权限问题是否已修复、当前容器 UID/GID 未知；2GB 构建地板是否仍适用于 2026.7.0 之后未知；2026.9.0 是否调整 2026.7.0 的 SSE4.2 / Node / sensitive-detector 要求未见重述 【官方】
  - 相邻事实一句话带过（不做配置步骤）：官方建议用 nginx 反代、不要把 Misskey 直接暴露公网，并强烈建议对外发布时使用 Cloudflare 等 CDN；家用服务器场景需路由器放行 80/443；FFmpeg 用于音视频处理而 ImageMagick 明确不需要；fork 或修改源码会触发 AGPL-3.0 披露义务 【官方】
- **素材引用**：C1–C17, C31, C32, C38, C39, C42, S01, S02, S06, S10a, S10b
- **代码示例**：有

---

## 学习路径说明

### 前置要求
- 已掌握 Docker / Docker Compose 基本用法（本 vault 内已有 `docker-compose-commands`、`docker-compose-linux-install`、`docker-compose部署` 等笔记，本篇不重复通用 compose 语法）。
- 部署机器已装 Docker 与 Docker Compose v2（官方只说「已安装」，未给最低版本）。
- 目标为 NAS / 自建服务器（如 fnOS、群晖）、x86_64；ARM64 亦可，但需注意 CPU 指令集差异。
- 具备在目标机器上编辑 YAML 与 `.env` 文本文件、查看容器日志的能力。

### 学完能做什么
- 依序完成克隆 → 三连拷贝 → 配置 → 构建 → 初始化 → 启动，让实例可访问、可注册、可发帖。
- 准确说出三份产物（`compose.yml`、`.config/default.yml`、`.config/docker.env`）各自负责什么，不再把它们混淆。
- 改对全部必改字段：`url`、`db.user`/`db.pass`、`POSTGRES_PASSWORD` 与一致性问题、按需改端口。
- 解释为什么 `url` 与 `id` 启动后不可更改，以及写错会带来什么后果。
- 判断自己硬件是否达标：SSE4.2 指令集、构建+迁移 2GB 地板、推荐 4GB。
- 按官方流程完成一次版本升级，并知道升级前要查 release notes、末行粘连命令不能照抄。
- 区分哪些结论有官方依据、哪些是本篇推断、哪些是已过时的历史信息。

### 建议学习顺序
1. 第一章（5–10 分钟）：先把产物落位，建立「三个文件各司其职」的心智模型。
2. 第二章（20–30 分钟）：读编排文件，理解服务栈、依赖顺序、网络与挂载，尤其是卷权限。
3. 第三章（30–40 分钟）：逐字段过应用配置，先把 `url` 定死。
4. 第四章（10 分钟）：处理数据库口令，确认两个文件的一致性。
5. 第五章（20 分钟）：执行构建、初始化、启动；上机前先对照内存地板与 SSE4.2 门槛自查。
6. 第六章（20 分钟）：跑通后再读升级流程与 NAS 遗留约束，作为长期维护参考。
7. 建议按章节顺序上机验证：前四章改配置、第五章跑起来、第六章留作运维手册。

> 缺口提示：`sensitive-detector` 的部署方式与资源占用本期未收集，仅知「未配置则不检测」；若后续需要敏感媒体自动判定，需补充研究。
