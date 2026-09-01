---
title: Gateway 常驻与 Compose 编排
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
created: 2026-08-28
updated: 2026-08-29
status: 完成
source_project: hermes-docker-deploy
---

> [[01-镜像数据卷与首次setup|⬅ 上一章]] · [[README|📖 返回目录]] · [[03-微信个人号iLink接入|下一章 ➡]]

# Gateway 常驻与 Compose 编排

第 1 章我们跑通了首次 setup，`~/.hermes/.env` 已落盘。但 setup 容器是一次性的，退出即销毁——Hermes 还没有真正"开始上班"。本章解决核心问题：**怎么让 Hermes 以 gateway 模式常驻后台，开机自启、崩溃自愈，并用一份 docker-compose.yaml 把 API Server、Dashboard、资源限制一次编排到位**。读完你会拿到两个可直接照抄的产物：一条 `docker run` 常驻命令（产物 C）和一份完整的 `docker-compose.yaml`（产物 D），并理解背后的权限模型、升级流程与三个高频坑。



## 2.1 产物 C：gateway 常驻一条命令

### 先睹为快

```bash
# 前置：~/.hermes/.env 已由第 1 章 setup 生成
docker run -d \
  --name hermes \
  --restart unless-stopped \
  -v ~/.hermes:/opt/data \
  -p 8642:8642 \
  nousresearch/hermes-agent:latest \
  gateway run
```

### 逐参数拆讲

| 参数 | 含义 | 为什么需要 |
|------|------|-----------|
| `-d` | detached，后台运行 | 命令立即返回，容器在后台常驻 |
| `--name hermes` | 给容器命名 | 之后 `docker logs hermes`、`docker stop hermes` 直接按名字操作 |
| `--restart unless-stopped` | 重启策略 | 开机自动拉起；进程崩溃自动重启；只有你手动 `docker stop` 才不再拉起 |
| `-v ~/.hermes:/opt/data` | 挂载数据卷 | 宿主机目录 ↔ 容器内 `/opt/data`，状态只存这里（档案柜比方见第 1 章） |
| `-p 8642:8642` | 端口映射 | 把容器 8642（API Server）暴露到宿主机 |
| `nousresearch/hermes-agent:latest` | 官方镜像 | 日常用 `:latest`，生产建议 pin 日期式 tag（见下方版本说明） |
| `gateway run` | 启动子命令 | 以 gateway 模式常驻，替代一次性 setup |

[!tip] 大白话：`--restart unless-stopped`
把容器想成小区夜班保安——你不用天天盯。设备重启了，物业（Docker）会自动把保安再派上岗；保安晕倒了，物业也会换人顶上。只有你主动打辞职报告（`docker stop`），物业才不再管。所以除非你手动停，Hermes 永远在岗。

### 纯聊天平台可以省掉 `-p 8642:8642`

`-p 8642:8642` 的作用是让别人能主动连进 Hermes 的 API Server。但本册要接入的三个国内平台——微信 iLink（长轮询）、飞书（WebSocket）、QQ（WebSocket）——**全部是 Hermes 主动向外发起连接**，没有公网入站请求。如果只跑聊天平台，这行可以删掉，少暴露一个端口就少一个攻击面（第 10 章安全基线还会强调）。

只有两种情况才必须留端口：

- 想用 9119 Dashboard（另需 `HERMES_DASHBOARD=1` + `-p 9119:9119`）；
- 想让外部程序/非官方桥调 Hermes 的 8642 API Server（此时还要配 `API_SERVER_ENABLED` + `API_SERVER_KEY`，见第 10 章）。

### 验证常驻成功

```bash
docker ps            # STATUS 应为 Up；PORTS 显示 0.0.0.0:8642->8642/tcp
docker logs -f hermes   # 观察 gateway 启动日志
```

预期输出（节选）：

```text
CONTAINER ID   IMAGE                                STATUS         PORTS
1f4c7a9b2e5d   nousresearch/hermes-agent:latest     Up 5 minutes   0.0.0.0:8642->8642/tcp
```

日志里应能看到 gateway 开始轮询各平台/等待连接。如果一启动就退出，多半是 `.env` 缺关键键或权限问题——先看 2.4 和 2.6。

[!note] 版本说明
官方目前用**日期式 tag**（如 `v2026.8.27`，pyproject 版本 0.20.6），没有 `RELEASE_v0.6.0.md` 这类文件。日常用 `:latest` 最省心；生产建议 pin 到某个日期 tag（`nousresearch/hermes-agent:v2026.8.27`），升级时再显式切换（见 2.5）。（F2）

## 2.2 产物 D：docker-compose.yaml 完整示例

`docker run` 一条命令能跑，但参数一多就容易忘、容易错。Compose 把"用什么镜像、映射哪些端口、挂哪个卷、设哪些环境变量、限多少资源"写成一份声明式清单，`docker compose up -d` 一键拉起，团队可复现、自己可追踪。

### 先睹为快

```yaml
services:
  hermes:
    image: nousresearch/hermes-agent:latest
    container_name: hermes
    restart: unless-stopped
    command: gateway run
    ports:
      - "8642:8642"   # gateway API
      - "9119:9119"   # dashboard（仅在 HERMES_DASHBOARD=1 时生效）
    volumes:
      - ~/.hermes:/opt/data
    environment:
      - HERMES_DASHBOARD=1
      # 取消注释以直接转发特定环境变量而非使用 .env 文件：
      # - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      # - OPENAI_API_KEY=${OPENAI_API_KEY}
      # - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2.0"
```

[!tip] 大白话：Compose 是什么
把 docker run 的一长串参数想成"开工前给员工口头交代"。口头交代容易漏，第二天换个人就全忘了。Compose 相当于**开业前写好的岗位说明书**——每个服务负责什么、在哪个工位（端口）、动哪个档案柜（数据卷）、领多少预算（资源），白纸黑字。以后 `docker compose up -d` 一个命令按说明书全部照做。

## 2.3 docker-compose.yaml 逐段拆讲

### services：一张岗位表

顶层 `services:` 下列出的每个名字（这里只有 `hermes`）对应一个容器。将来要加别的服务（比如第 8 章的 NapCat），就平行再开一段。Compose 会按这份清单依次创建并管理它们（D1 §Compose）。

### ports：对外门牌

```yaml
    ports:
      - "8642:8642"   # 宿主机端口 : 容器端口
      - "9119:9119"
```

语法是 `宿主机端口:容器端口`。把容器想成一间没门牌号的房间——容器内部的 8642 端口只有 Docker 自己知道；`ports` 相当于在宿主机前台登记一块门牌，外部才能访问。

- **8642**：Hermes API Server，接收外部 REST 请求。
- **9119**：Hermes Dashboard，配合 `HERMES_DASHBOARD=1` 使用，浏览器打开 `http://localhost:9119` 查看仪表盘（具体页面路径需实测）。

> 纯聊天平台可把 `ports` 整段删掉（同 2.1 的"可省 -p"）。这是最省心的最小配置。

### volumes：档案柜（唯一状态源）

```yaml
    volumes:
      - ~/.hermes:/opt/data
```

宿主机 `~/.hermes/` 挂到容器内 `/opt/data`。`.env`、`config.yaml`、`sessions`、`memories`、`logs` 全在这里。**容器随便删，档案柜不动**——这是升级、迁移的底气（D1 §持久化卷）。注意：Compose 里 `~` 通常能识别，但写死 `/home/你的用户名/.hermes` 最保险，避免某些环境下 `~` 展开异常。

[!tip] 大白话：为什么容器可以随便删
容器是**临时工**，干完活就换人，什么都不带走；`~/.hermes` 是**公司档案柜**，聊天记录、记忆、配置全锁在里面。辞退临时工（删容器）不影响档案柜，换个新临时工（新容器）照样上班。

### environment：开关与密钥

```yaml
    environment:
      - HERMES_DASHBOARD=1
```

这里详细的启用dashboard的笔记在[11-Dashboard认证配置实战](11-Dashboard认证配置实战.md)。
`HERMES_DASHBOARD=1` 打开 9119 仪表盘。这里也是以后放平台密钥的地方——微信的 `WEIXIN_TOKEN`、飞书的 `FEISHU_APP_SECRET`、QQ 的 `QQ_CLIENT_SECRET` 都会追加进来（第 3/5/7 章）。密钥明文写在 yaml 里，等于写进代码仓库——建议至少用 `.env` 文件 + `env_file:` 引用（第 10 章安全基线细讲）。

### 资源限制：给容器"上预算"

```yaml
    mem_limit: 4g     # 最多吃 4G 内存
    cpus: 2.0         # 最多用 2 核 CPU
    shm_size: 1g      # /dev/shm 共享内存 1G
```

Hermes 要跑 Python 解释器、Node、可选 Playwright 浏览器，属于"胃口不小"的服务。`mem_limit` 是**硬上限**：容器内存超限会被内核 OOM Kill（`docker logs` 里出现 `Killed`）。要真用满 4G，宿主需有 ≥4G 物理内存或配置 swap。`cpus` 限制 CPU 争抢，避免拖垮同宿主其他容器。`shm_size` 对应 2.6 的坑 3——浏览器工具依赖 `/dev/shm`，默认 64M 根本不够（D1 §故障排查）。

### 启动/停止/看日志

```bash
cd ~/hermes-stack
docker compose up -d          # 按清单创建并后台启动
docker compose ps             # 看各服务状态
docker compose logs -f hermes # 跟踪 hermes 日志
docker compose down           # 停止并删除容器（数据卷 ~/.hermes 保留）
```

## 2.4 权限模型：为什么容器里"不能随便动 /opt/hermes"

部署 Hermes 最容易被权限问题绊倒。先理解镜像的权限设计，再动手（D1 §权限模型）。

**启动链路**（英文版文档口径，以 `entrypoint-dispatch.sh` 为准）：

```text
docker run（root）
  └─ entrypoint-dispatch.sh  /  s6-overlay（PID 1，root 身份）
       ├─ ① root 先把数据卷 chown 给 hermes 用户（UID 10000）
       └─ ② s6-setuidgid 降权 → 以 UID 10000 运行 gateway
```

要点拆开说：

1. **root 只做"开门"一件事**：容器以 root 启动，但 root 不会亲自跑 gateway，而是先把 `~/.hermes` 数据卷的所有权 `chown` 给内置的 `hermes` 用户（UID 10000）。
2. **`s6-setuidgid` 降权**：随后用 `s6-setuidgid` 把进程身份降到 UID 10000，gateway 全程以低权限运行。降权 = 即使容器被攻破，攻击者拿到的也只是普通用户权限，不是 root。
3. **`/opt/hermes` 是只读安装树**：镜像里的代码装在 `/opt/hermes`，对 UID 10000 只读。这是"安装树锁"——升级就是换整棵新树，不在旧树里打补丁。

所以常见的 `PermissionError /opt/hermes/.env` 的准确机理是：**旧镜像把 `/opt/hermes` 锁成 0700（只有 root 可写），而 gateway 已经降权到 UID 10000，去写 `/opt/hermes/.env` 时被拒**。不是 `.env` 本身的权限问题，是"降权员工写经理的保险柜"。

修复三板斧（按推荐顺序）：

```bash
# 方式 A：把数据卷权限放给降权用户（最推荐，一步到位）
chmod -R 755 ~/.hermes

# 方式 B：用 HERMES_UID/GID 把降权 UID 改到宿主机用户（避免和宿主机权限打架）
docker run -d --name hermes \
  -e HERMES_UID=$(id -u) -e HERMES_GID=$(id -g) \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent:latest gateway run

# 方式 C（仅针对 2026-08 之前的旧镜像）：手动把安装树改 0755
docker exec -u root hermes chmod 0755 /opt/hermes
```

> 不要用 `chmod 777`——那是把保险柜门拆了。`755` 已足够让 UID 10000 读写数据卷。升级到新镜像后方式 C 通常不再需要（D1 §故障排查）。

**root 跑 gateway 默认被拒**：镜像的安全设计是"别用 root 跑服务"。如果你显式要求以 root 身份跑 gateway（比如某些调试场景），容器会拒绝启动，必须加环境变量 `HERMES_ALLOW_ROOT_GATEWAY=1` 才放行。生产环境不要开这个开关——它等于撤销了整套降权设计（D1 §权限模型）。

[!tip] 大白话：s6-setuidgid 降权
把镜像想成一家严格的公司：进门时你是总经理（root），但总经理只在门口刷个卡，把门禁交给**挂临时工牌的员工（UID 10000）**去干活。临时工牌只能进出自己工位（数据卷），进不了总经理办公室（`/opt/hermes` 安装树）。这样就算混进坏人，他也只是临时工权限，砸不了场子。`HERMES_ALLOW_ROOT_GATEWAY=1` 相当于"总经理非要亲自干活"的特批条，非必要别开。

**ENTRYPOINT 口径勘误**：官方中文文档写的是 s6 `/init` 作 PID 1，英文文档写的是 `entrypoint-dispatch.sh`（面向 Fly.io / K8s 直跑 stage2 的部署）。两者对常规 Compose 使用没有影响——都会先 chown 卷再降权；区别只影响需要直跑 stage2 的高级托管场景。**以英文版 `entrypoint-dispatch.sh` 为准**（素材矛盾点 5）。

## 2.5 升级与重建：档案柜不动，换人上班

Hermes 迭代快，升级是家常便饭。升级三原则：**先备份 → 拉新镜像 → 重建容器，数据卷不动**（D1 §升级）。

### 完整升级流程

```bash
# ① 时间戳备份（先写备份再动，永远有效）
ts=$(date +%Y%m%d%H%M%S)
tar czf ~/.hermes-backup-$ts.tar.gz -C "$HOME" .hermes

# ② 拉新镜像（:latest 会拉到最新；pin 了日期 tag 就拉那个 tag）
docker pull nousresearch/hermes-agent:latest

# ③ 重建容器，数据卷 ~/.hermes 不动
cd ~/hermes-stack
docker compose up -d --force-recreate
```

用 `docker run` 管理的话，重建两步：

```bash
docker stop hermes && docker rm hermes
docker run -d --name hermes --restart unless-stopped \
  -v ~/.hermes:/opt/data -p 8642:8642 \
  nousresearch/hermes-agent:latest gateway run
```

### 为什么这样安全

- **数据卷不动**：`~/.hermes` 是唯一状态源，新容器挂同一个目录，聊天记录、记忆、平台凭证全在。
- **`--force-recreate`**：即使 compose 配置没变，也强制用新镜像重建容器。不加它，Compose 可能认为"配置没变"而跳过重建。
- **时间戳备份**：升级后发现新版有 bug，随时可以回滚：

```bash
# 回滚：拉回旧 tag，重建
docker pull nousresearch/hermes-agent:v2026.8.27   # 换成你上次用的 tag
cd ~/hermes-stack && docker compose up -d --force-recreate
```

备份文件建议至少留一份跨版本（`~/.hermes-backup-*.tar.gz`），确认新版本跑稳一周再清理。

## 2.6 常见坑

### 坑 1：`docker exec hermes hermes logs` 报 PATH 找不到

这是镜像没有把 `hermes` 可执行文件放到标准 PATH 导致的（W4）。你以为"进容器跑个 CLI 很自然"，但 `docker exec` 起的是一个干净 shell，既没有镜像入口的环境变量，也可能没有可执行文件。**别在 exec 里找二进制，改用一次性容器跑 CLI**：

```bash
# 错误示范：exec 找不到 hermes
docker exec -it hermes hermes gateway setup   # 可能报 command not found / PATH 错误

# 正确姿势：一次性容器 + 同一个数据卷
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent:latest \
  gateway setup        # 或 logs、skills 等任意 CLI 子命令
```

`--rm` 用完即删，`-v` 挂同一个数据卷，跑完写进 `~/.hermes`，常驻容器立即生效。**需要看运行时日志请用 `docker logs`，需要跑 CLI 请用一次性容器**，各司其职。

### 坑 2：两个 gateway 共享数据目录 → 排他锁冲突

一个数据目录只能有一个 gateway 实例。Hermes 会对数据目录加**排他锁**，第二个 gateway 抢不到锁会报错或行为异常。常见触发场景：

- 手动 `docker run` 起了一个，又 `docker compose up -d` 起了第二个，两个容器挂同一个 `~/.hermes`；
- 想"多开平台"而复制配置、共用卷。

正确做法（D1 §故障排查 + 第 9 章约束）：**一个数据卷 = 一个 gateway = 一个容器**。要接多个平台，把平台配置写进**同一个** gateway 的 `.env`（第 3-8 章就是这么做的），不要各起一个。

```bash
# 排查：本机是否已有容器占用同一个卷
docker ps --filter name=hermes
docker inspect hermes --format '{{.Mounts}}'   # 确认挂载路径
```

### 坑 3：浏览器工具白屏/崩溃 → `--shm-size=1g`

Hermes 内置 Playwright + Chromium（浏览器自动化工具）。容器默认 `/dev/shm` 只有 64M，Chromium 渲染一多就崩溃（D1 §故障排查）。现象：浏览器工具调用失败、日志里出现 `DevTools` 相关报错、`SIGBUS` 等。

修复——给容器加共享内存配额：

```bash
# docker run 方式
docker run -d ... --shm-size=1g nousresearch/hermes-agent:latest gateway run

# compose 方式（见 2.2 的 shm_size 字段）
docker compose up -d --force-recreate   # 让 shm_size 生效
```

## 2.7 初始化清单：Compose 就绪后如何初始化与配置

`docker-compose.yaml` 只是「常驻启动」的说明书，它**不会替你初始化**——`.env` 与 `config.yaml` 必须先就绪，gateway 才有东西可读。本节把 Compose 就绪后的初始化收敛成四步清单：前三步用一次性容器完成，第四步才轮到 compose 常驻。第 1 章已跑过 setup 的，可压缩成两步（③+④）。

### 先睹为快：四步命令

```bash
# ① 首次 setup（产出 ~/.hermes/.env，仅新机器/新目录需要）
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup

# ② 配置模型 provider（可选：新增 provider / 改默认模型）
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent model

# ③ 验证配置齐全
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent doctor

# ④ compose 常驻启动
cd ~/hermes-stack
docker compose up -d
docker compose ps
docker compose logs -f hermes
```

### 逐段拆讲

| 步骤 | 干什么 | 关键点 |
|------|--------|--------|
| ① setup | 交互式向导产出 `~/.hermes/.env` | `-it` **必须**；向导依次问 provider → API Key → 是否启用平台；第 1 章跑过可跳过 |
| ② model | 会话外配置模型 provider | 也可手工改 `config.yaml` + `.env`，key 只进 `.env`（详见 [[03-模型 Provider 配置\|模型 Provider 配置]]） |
| ③ doctor | 诊断配置与密钥是否齐全 | 缺 key / provider 拼错都会暴露；`doctor` 过了再启动，避免一启动就退出 |
| ④ compose up | 按 2.2 清单常驻启动 gateway | 日志出现 gateway 开始轮询各平台 / 等待连接即成功 |

[!note] 初始化前先处理权限
权限问题（2.4）要在初始化**之前**解决，否则 setup 第一步就撞 `PermissionError /opt/hermes/.env`。推荐 `chmod -R 755 ~/.hermes`，或在 compose 里配 `HERMES_UID` / `HERMES_GID` 对齐宿主 UID。

[!warning] 三条红线（对应 2.6 三大坑）
1. CLI 一律用一次性容器，不要 `docker exec hermes hermes ...`；
2. 一个数据卷只能一个 gateway，别让手动 `docker run` 与 `docker compose up` 抢同一个 `~/.hermes`；
3. 接平台时逐个在 `.env` 取消注释填 key、不重建容器，平台变量见第 3~8 章。

## 小结

- **产物 C**：`docker run -d --restart unless-stopped -v ~/.hermes:/opt/data -p 8642:8642 ... gateway run` 让 Hermes 常驻后台；纯聊天平台可删 `-p 8642:8642`。
- **产物 D**：`docker-compose.yaml` 一份文件管住镜像、端口（8642 API + 9119 Dashboard）、数据卷、`HERMES_DASHBOARD=1` 与资源限制（memory 4G / cpus 2.0 / shm 1G）。
- **权限模型**：root 只做 chown 开门，`s6-setuidgid` 降权 UID 10000 干活；`/opt/hermes` 只读；`PermissionError /opt/hermes/.env` = 降权员工写 0700 安装树；`HERMES_ALLOW_ROOT_GATEWAY=1` 非必要不开。
- **升级**：时间戳备份 → pull 新镜像 → `--force-recreate` 重建，数据卷不动，可随时回滚。
- **三大坑**：CLI 用一次性容器（不要 `docker exec`）、一个数据卷只能一个 gateway（排他锁）、浏览器工具要 `--shm-size=1g`。

Hermes 现在已经"常驻上班"了，但它还孤零零的——没有连接任何消息平台。下一章开始接入第一个国内平台：**微信个人号 iLink 扫码直连**，看看 gateway setup 怎么扫码建号、长轮询如何做到免公网收发消息，以及"不能进普通群"的能力边界。
