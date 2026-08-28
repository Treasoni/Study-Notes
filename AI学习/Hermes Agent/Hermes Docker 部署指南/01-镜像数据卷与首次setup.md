---
title: 镜像、数据卷与首次 setup
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
---

> [[README|📖 返回目录]]

# 镜像、数据卷与首次 setup

> 本章回答两个问题：**用哪个镜像跑 Hermes**、**Hermes 的状态存在哪里**。跑通本章，你就拥有一个「重启机器也不丢」的 Hermes 数据目录——这是后续所有平台接入的地基。

## 1.1 认识官方镜像 `nousresearch/hermes-agent`

Hermes 官方在 Docker Hub 发布镜像，名称固定为 `nousresearch/hermes-agent`，直接 `docker pull` 或 `docker run` 即可获取 [D1 §快速开始](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)。

### tag 策略：`:latest` 还是日期式 tag？

- 官方文档示例一律写 `nousresearch/hermes-agent`，隐含 `:latest`，跟随最新版。
- 仓库源码用**日期式 tag** 发版，例如 `v2026.8.27`；当前 pyproject 版本为 0.20.6。官方**没有** `RELEASE_v0.6.0.md` 这类文件，网上若看到「v0.6.0」「v0.9.0」等版本号，多为旧资料或 PR 合并窗口的临时表述 [F2](https://github.com/NousResearch/hermes-agent)。

> [!tip] 大白话：镜像 tag
> 把 `:latest` 想成「App Store 里的『最新版』」，今天和昨天装的可能不是同一个东西；把 `v2026.8.27` 想成「某个日期的发布快照」，钉死不变。所以**日常调试用 latest 图省事，正式部署用日期式 tag 图可复现**——哪天踩了坑，你能确定自己跑的是哪一版。

> [!warning] tag pin 策略需实测
> 官方没有给出「必须 pin 某个 tag」的硬性规定，日期式 tag 是否长期保留属需实测项。保守做法：Compose / README 里写死一个日期式 tag，升级时显式修改，不默默跟着 latest 漂移。

### 镜像内置环境

镜像基于 `debian:13.4`，开箱内置一整套运行环境，**你在宿主机不需要装任何 Python / Node** [D1 §Dockerfile](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)：

| 组件 | 版本/用途 |
|------|-----------|
| Python | 3.13 + uv（Hermes 主运行时，uv 管依赖） |
| Node.js | 26 + npm（部分工具 / 技能需要） |
| Playwright | 预装 Chromium，浏览器工具直接用 |
| docker-cli | 可选挂载 `/var/run/docker.sock` 驱动宿主机 Docker |
| openssh-client | SSH 相关技能 |
| s6-overlay | v3，作为 PID1 进程管理器，负责启动 / 守护 gateway |

两个值得记住的点：**浏览器工具**要求容器有足够共享内存（第 2 章会用到 `--shm-size=1g`）；**docker-cli 存在但不自动连宿主**，需要你显式挂载 socket，属高级用法。

## 1.2 大白话：数据卷持久化

> [!tip] 大白话：容器是临时工，`~/.hermes` 是档案柜
> 把容器想成**临时工**：他干活利索，但你一「开除」他（删容器），他手里的东西全跟着没了。`~/.hermes` 是公司的**档案柜**：临时工每做完一件事都把成果归档进柜子，换多少茬临时工，档案永远在。`-v ~/.hermes:/opt/data` 就是「把档案柜搬到临时工工位上」的指令。

技术上的准确表述：容器内的文件系统是**可丢弃的**，`docker rm` 或重建容器会全部清空；而挂载卷（bind mount）把宿主机目录 `~/.hermes/` 映射到容器内 `/opt/data`，这个目录是 Hermes **唯一的状态源**。`.env`、`config.yaml`、记忆、会话全部落在里面，删容器、换镜像都不动它 [D1 §持久化卷](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)。

由此得到一条贯穿全册的铁律：

> [!note] 铁律
> **Hermes 的所有状态都在 `~/.hermes/`。** 升级、回滚、备份、迁移，操作的只有这个目录；容器本身随时可以推倒重建。

## 1.3 产物 A：数据卷目录树 `~/.hermes/`

先睹为快——setup 之后你的 `~/.hermes/` 会长成这样（注释标注了每个条目的用途）：

```text
# ~/.hermes/ —— 数据卷根目录（宿主机一侧）
~/.hermes/
├── .env          # 环境变量 + 全部密钥（token/secret 明文，最高敏感）
├── config.yaml   # 主配置：模型 provider、平台开关、技能参数
├── SOUL.md       # 人设/人格文件（角色设定、说话风格）
├── sessions/     # 会话历史（每个对话的上下文快照）
├── memories/     # 长期记忆（跨会话保留的事实/偏好）
├── skills/       # 技能目录（自定义技能放这里）
├── cron/         # 定时任务定义
├── hooks/        # 钩子脚本（生命周期事件触发）
├── logs/         # 运行日志（gateways/<profile>/current 由 gateway 滚动）
├── skins/        # 皮肤/主题（界面风格）
└── home/         # 容器内 /home/hermes 的落盘（凭据缓存、临时文件）
```

对照大纲要点拆几个关键条目：

- `.env` 与 `config.yaml` 是**两个不同层级的配置**：`.env` 放密钥和环境级变量，`config.yaml` 放结构化配置（模型、平台、技能参数）。
- `sessions/` 与 `memories/` 的区别：**会话**是一次性对话的现场，**记忆**是沉淀下来的长期事实。两者都在数据卷里，所以重启 Hermes 不会「失忆」。
- `logs/` 在第 9 章展开：gateway 日志以 `gateways/<profile>/current` 的形式滚动落盘，`docker logs` 与文件日志可互相印证。

## 1.4 产物 B：首次 setup 向导

### setup 命令

新建数据目录并启动首次配置向导 [D1 §快速开始](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)：

```bash
# ① 先建宿主数据目录
mkdir -p ~/.hermes

# ② 以交互式 TTY 跑 setup，向导会写入 ~/.hermes/.env
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup
```

拆讲四个要素：

- `-it`：**必须的**。setup 是交互式向导，没有 TTY 就无法回答提问（无 TTY 环境下扫码类步骤的替代方案官方未明确，属需实测项）。
- `--rm`：容器用完即删、不残留；因为状态都写进了 `~/.hermes`，容器本身不需要保留。
- `-v ~/.hermes:/opt/data`：把档案柜挂进临时工工位，setup 写出的 `.env` 直接落盘到宿主机。
- `setup`：镜像入口的子命令。向导依次问：默认模型 provider → API Key → 是否启用消息平台等。

### 产物：`~/.hermes/.env`

向导跑完后，`~/.hermes/.env` 内容形如（省略号处为你在向导中填入的值；未选的平台可能不出现，后续章节需要的变量照格式自行补充即可）：

```ini
# ~/.hermes/.env —— setup 向导生成（日期以实际为准）
# 警示：本文件明文保存全部密钥，属数据卷内最高敏感文件；
# 不要提交 git、不要截图外发，备份前先加密。

# ---------- 模型 Provider ----------
# 至少一个 provider；变量名随你选的 provider 不同
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
# ANTHROPIC_API_KEY=

# ---------- 消息平台（第 3~8 章逐个启用）----------
# WEIXIN_ACCOUNT_ID=
# WEIXIN_TOKEN=
# WECOM_BOT_ID=
# WECOM_SECRET=
# FEISHU_APP_ID=
# FEISHU_APP_SECRET=
# QQ_APP_ID=
# QQ_CLIENT_SECRET=

# ---------- API Server（第 10 章启用）----------
# API_SERVER_ENABLED=true
# API_SERVER_HOST=127.0.0.1
# API_SERVER_KEY=
```

逐段拆讲关键键：

- **模型 provider 区**：这是 setup 的核心产出。Hermes 不绑死某家模型，`OPENAI_API_KEY` / `ANTHROPIC_API_KEY` 等按你选的 provider 落盘，变量名以该 provider 官方名为准。
- **消息平台区**：setup 里没启用就保持注释。本册第 3~8 章每接入一个平台，就取消注释对应几行并填值——这是全册的「逐步点亮」主线。
- **API Server 区**：默认关闭。第 10 章讲安全三件套（`API_SERVER_ENABLED` + `API_SERVER_HOST` + `API_SERVER_KEY`）时才打开。

> [!tip] 大白话：`.env` 是保险箱
> `.env` 就是 Hermes 的**保险箱**：所有门禁卡（token/secret）都锁在里面。档案柜（`~/.hermes`）本身不设防，所以保险箱的钥匙（文件权限、git 隔离）得自己看好——第 10 章专门讲安全。

## 1.5 常见坑：`PermissionError /opt/hermes/.env`

首次 `docker run` setup 时，最容易撞上这个报错：

```
PermissionError: [Errno 13] Permission denied: '/opt/hermes/.env'
```

### 准确机理（两层叠加）

1. **安装树锁权限**：镜像把 Hermes 装在容器内 `/opt/hermes`，是**只读安装树**；2026-08 之前的旧镜像把 `/opt/hermes` 锁成了 `0700`（仅 root 可进）[D1 §故障排查](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)。
2. **UID 10000 降权**：容器启动后从 root 降权到 `hermes` 用户（UID 10000）运行，而宿主机挂进来的 `~/.hermes` 属主是你宿主 UID（通常 1000）——两者对不上，hermes 想写 `.env` 就被拒。

一句话：**进程权限（10000）写不进「只读的安装树」或「属主不匹配的宿主目录」。**

> [!warning] 易错点
> 不要靠 `docker exec -u root` 绕权限乱改容器内部文件——容器一删就没了。**持久化的修复必须落在 `~/.hermes/` 这一层。**

### 修复：三选一

```bash
# 方案 A（最省事）：让宿主目录对所有容器用户可读写
chmod -R 755 ~/.hermes

# 方案 B（最规范）：让容器内 hermes 的 UID 与你宿主 UID 一致
docker run -it --rm \
  -e HERMES_UID="$(id -u)" -e HERMES_GID="$(id -g)" \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent setup

# 方案 C（仅 2026-08 前的旧镜像）：解 /opt/hermes 安装树的 0700 锁
# 注意：docker exec 针对的是你实际起名的运行中容器
docker exec -u root hermes chmod 0755 /opt/hermes
```

方案 B 是长期最稳的：`HERMES_UID/GID`（文档中也写作 `PUID/PGID`）让容器以你的 UID 运行，读写 `~/.hermes` 天然无冲突；第 2 章的 Compose 会把这两个变量正式写进配置 [D1 §故障排查](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker)。

## 本章小结

- 官方镜像 `nousresearch/hermes-agent`：日常用 `:latest` 图省事，正式部署建议 pin 日期式 tag（如 `v2026.8.27`）求可复现；镜像内置 Python 3.13+uv / Node 26 / Playwright / docker-cli / s6-overlay，宿主机零依赖。
- 数据卷是 Hermes 唯一状态源：容器是临时工、`~/.hermes` 是档案柜，升级、回滚、迁移都只动这个目录。
- 目录树里 `.env`（密钥）与 `config.yaml`（结构配置）是两层不同配置；`sessions/` 与 `memories/` 分记会话现场与长期记忆。
- 首次 setup = `mkdir -p ~/.hermes && docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup`，产出 `.env`。
- `PermissionError /opt/hermes/.env` 的机理是「0700 安装树锁 + UID 10000 降权」双叠加，推荐用 `HERMES_UID/GID` 对齐宿主 UID 解决。

## 下一章预告

数据目录就绪后，下一步是把 Hermes 从「一次性 setup」升级成**常驻服务**：第 2 章用 `gateway run` + `docker-compose.yaml` 把 Hermes 跑成开机自启的守护进程，并讲透「root 先 chown → s6-setuidgid 降权」的权限模型——那是理解 Docker 化 Hermes 的最后一根主线。
