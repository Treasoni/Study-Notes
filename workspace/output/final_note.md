---
title: 使用 Docker Compose 部署 Misskey：从零跑通到长期维护
tags:
  - docker
  - docker-compose
  - misskey
  - self-hosting
  - nas
created: 2026-09-15
updated: 2026-09-15
status: 已完成
source_project: misskey-docker-compose-deploy
---

# 使用 Docker Compose 部署 Misskey：从零跑通到长期维护

## 导读

这篇笔记是一条可照做的主线：从克隆 Misskey 源码、落位三份配置文件（`compose.yml`、`.config/default.yml`、`.config/docker.env`），到构建、初始化、启动，再到版本升级与长期维护。它写给已经会基本 Docker / Docker Compose 用法、准备在 NAS 或自建服务器（x86_64）上把 Misskey 真正跑起来的人。全篇以「先把最小闭环跑通」为界：反向代理与 TLS 配置、全文检索 provider 的对比、PGroonga 安装、对象存储、邮件发送都不在范围内；这些内容仅在必要处一句话带过，不展开步骤。

## 标注约定

全篇用三种标记区分内容成色：【官方】＝官方文档或官方仓库一手文件直接陈述；【推断】＝本文档推断、没有官方来源；【过时】＝已失效信息，只能按历史口径阅读。

## 目录

1. [第一章 部署前置：克隆源码与三份产物的落位](#第一章-部署前置克隆源码与三份产物的落位)
2. [第二章：`compose.yml`——服务栈、依赖顺序、网络与挂载](#第二章composeyml服务栈依赖顺序网络与挂载)
3. [第三章：`.config/default.yml`——应用配置必改字段与不可变项](#第三章configdefaultyml应用配置必改字段与不可变项)
4. [第四章：`.config/docker.env`——数据库口令与变量注入](#第四章configdockerenv数据库口令与变量注入)
5. [第五章：构建 → 初始化 → 启动——跑通链路](#第五章构建--初始化--启动跑通链路)
6. [第六章：升级流程与 NAS 遗留约束](#第六章升级流程与-nas-遗留约束)

> 全篇引用统一汇总于文末 [参考来源](#参考来源)。六章为顺序结构：第一章落位产物、第二章读编排文件、第三章读应用配置、第四章读数据库口令、第五与第六章执行并维护，建议按序阅读。

---

## 相关笔记

本篇只讲 Misskey 特有的部署约束，Docker / Compose 的通用能力不重复讲。以下 vault 内笔记与本篇互补：

| 笔记 | 与本篇的关系 |
| --- | --- |
| [[Docker与DockerCompose命令速查]] | 命令语法速查；本篇假定你已掌握，不解释通用用法 |
| [[Linux-Docker与DockerCompose安装指南-国内网络版]] | 第一章「前置条件」的展开：Linux 侧 Docker + Compose 安装 |
| [[Docker网络结构详解]] | 第二章 2.4 网络与端口的通用背景 |
| [[docker里的GID和UID]] | 第二章 2.8 卷权限的通用排查方法，衔接本篇的 UID/GID 遗留问题 |
| [[docker容器如何更新]] | 第六章升级流程的通用做法（镜像加速、版本锁定） |
| [[Docker MOC]] | Docker 主题索引 |

---

## 第一章 部署前置：克隆源码与三份产物的落位

Misskey 的 Docker 部署有个和其他自建服务很不一样的地方：它不提供一个「拉个镜像、起个容器」就完事的路径，而是要求你克隆整个源码仓库，把三份示例文件复制成生效文件，然后自己构建镜像。麻烦的是这三份示例文件名字长得极其相似——`compose_example.yml`、`docker_example.yml`、`docker_example.env`——几乎每个人第一次配置时都会把它们弄混。

本章只做一件事：把源码克隆下来，让三份产物各就各位，并弄清楚它们各自到底在管什么。这一步本身不产生任何技术难点，但它是后面五章的地基——分不清这三个文件，第三章、第四章的字段改在哪里就无从谈起。

> 本章标注约定：`【官方】`＝官方文档或官方仓库一手文件直接陈述；`【推断】`＝本文档推断、无官方来源；`【过时】`＝已失效信息，按历史口径呈现。本章内容全部来自官方一手来源，没有需要标注为推断或过时的条目。

---

### 1.1 前置条件只有一条 【官方】

Misskey Hub 的 Docker 部署指南[^c1-1]里，前置条件只有一行（顺带一提，英文页面上这个小标题原文写的就是日文「前提条件」，官方页面自己没翻译干净）：

> Make sure Docker and Docker Compose are installed on your system.

也就是说，唯一的要求是「你的系统上装好了 Docker 和 Docker Compose」。官方**没有**给出最低版本号要求。这一点的实际影响是：官方不背书也不排除任何具体版本，遇到版本相关问题时你无法拿「官方要求 X 版本」来佐证，只能自己判断。

| 项 | 官方口径 |
| --- | --- |
| 需要装什么 | Docker 与 Docker Compose |
| 最低版本 | 未给出，只说「已安装」 |

> [!tip] 大白话
> 把这条前置条件想成请人上门装修时说的「你家里得有电有水管」。官方只确认「有」，没规定必须是几平方的电线、多粗的水管。所以别指望在这份文档里找到「Compose 必须 ≥ 2.x」这类硬指标——它没写。

---

### 1.2 第一步：克隆源码 【官方】

官方给出的克隆命令是三步，注意 `sudo` 之外的每一处细节都要照抄：`-b master` 指定分支，克隆完还额外做了一次 `git checkout master`。

```bash
# 在部署机上执行（先 cd 到你希望存放源码的目录）
git clone -b master https://github.com/misskey-dev/misskey.git
cd misskey
git checkout master
```

三个命令里，`git clone -b master ...` 已经指定了 master 分支，紧接着的 `git checkout master` 从字面上看像是重复动作——但这是官方原文，两句都保留，不要自行「优化」。另外注意 `cd misskey`：克隆会在当前目录下创建名为 `misskey` 的子目录，后续所有操作都在这个目录**内部**进行。

> [!tip] 大白话
> 把 `git clone -b master` 想成去仓库取货时先报一句「我要 master 那条货架上的」。后面那句 `git checkout master` 相当于走到货架前又确认了一遍「对，就是这条」。多确认一次没有坏处，删掉反而偏离了官方原文。

---

### 1.3 第二步：三连拷贝 【官方】

这是本章最关键的一步，也是最容易抄错的一步。官方原文说明是「以下命令会把各种配置文件从示例位置拷贝到它们实际的配置位置」，紧接着给出三条 `cp`：

```bash
# 在上一步创建的 misskey/ 仓库根目录内执行
cp .config/docker_example.yml .config/default.yml
cp .config/docker_example.env .config/docker.env
cp ./compose_example.yml ./compose.yml
```

三行分别完成了三件互相独立的事，行与行之间**没有依赖顺序**，但每一行的「来源」和「目标」都不同——这正是混淆的来源。执行完之后，仓库里会同时存在「示例文件」和「生效文件」；官方没有要求你删除示例文件，所以两种情况并存是正常状态。

#### 执行前后：目录里多了什么

下面把这一步前后与本章相关的目录条目并排列出（`...` 表示仓库中与本章无关的其他内容）：

**执行前**——只有一份份 `*_example` 样板：

```text
misskey/                          # git clone 得到的仓库根目录
├── compose_example.yml           # 编排示例（尚未生效）
├── ...
└── .config/
    ├── docker_example.yml        # 应用配置示例（尚未生效）
    ├── docker_example.env        # 数据库口令示例（尚未生效）
    └── ...
```

**执行后**——三个不带 `_example` 的「生效文件」出现，与样板并存：

```text
misskey/
├── compose_example.yml           # 保留，不动
├── compose.yml                   # ← 从 compose_example.yml 拷来（生效）
├── ...
└── .config/
    ├── docker_example.yml        # 保留，不动
    ├── docker_example.env        # 保留，不动
    ├── default.yml               # ← 从 docker_example.yml 拷来（生效）
    ├── docker.env                # ← 从 docker_example.env 拷来（生效）
    └── ...
```

一眼能看出规律：`_example` 全部留在原地，真正被 Docker 和 Misskey 读取的是拷贝出来的那三个**不带 `_example`** 的文件。后续第三、四章要改的字段，全都在右边的三个文件里，改左边的示例文件毫无作用。

> [!tip] 大白话
> 把 `*_example` 文件想成楼盘售楼处的样板间，`cp` 就是照着样板间在你自己那套房子里真砌了一堵墙。你去样板间里刷漆，自家房子不会变——所以改配置永远改拷贝出来的那一份，别改 `_example`。

---

### 1.4 三份产物辨析：它们到底各管什么 【官方】

三份示例文件的命名高度相似，这是读者最容易翻车的地方。先把命名陷阱点破：

- `compose_example.yml`（根目录）与 `.config/docker_example.yml`（`.config` 目录下）后缀相同、都带 `example`，只有前缀一个叫 `compose`、一个叫 `docker`；
- `.config/docker_example.yml` 与 `.config/docker_example.env` 同在 `.config` 目录、前缀完全相同，差别**只有最后的扩展名** `.yml` 与 `.env`。

只差一两个字符，控制的却是完全不同的东西。下表是本章的核心产出——「源文件 → 目标文件 → 谁读它 → 它实际控制什么」四列对照：

| 拷来的源文件 | 目标文件（生效） | 谁读它 | 它实际控制什么 |
| --- | --- | --- | --- |
| `./compose_example.yml` | `./compose.yml` | `docker compose` 命令本身 | **编排**：起哪几个容器、用哪个镜像、谁等谁、连哪个网络、映射哪个端口、挂哪些目录 |
| `.config/docker_example.yml` | `.config/default.yml` | Misskey 应用进程 | **应用配置**：实例 URL、数据库连接、Redis 连接、ID 生成方式等 |
| `.config/docker_example.env` | `.config/docker.env` | `db` 服务（经 `env_file` 加载） | **数据库口令**：`POSTGRES_PASSWORD` / `POSTGRES_USER` / `POSTGRES_DB` 及拼出的 `DATABASE_URL`[^c1-3] |

两个「谁读它」的细节值得记住，它们是后面章节的解释基础：

1. `.config/default.yml` 之所以能被 Misskey 读到，是因为编排文件把 `.config` 目录整个以**只读**方式挂进了 `web` 容器（`./.config:/misskey/.config:ro`）[^c1-2]。所以应用配置**必须**放在 compose 文件旁边的 `.config/` 目录里，换个位置就不生效了。
2. `.config/docker.env` 是被编排文件里 `db` 服务的 `env_file` 指令加载的[^c1-2]，也就是说这份文件是给数据库容器用的。

> [!tip] 大白话
> 把整套部署想成开一家餐厅：`compose.yml` 是**厨房排班表**——开几个灶、谁先备菜谁后开火（服务与依赖顺序）；`.config/default.yml` 是**店规和门牌**——店名叫什么、地址挂在哪（实例 URL 等应用配置）；`.config/docker.env` 是**保险柜密码条**——只交给后厨管库房的人（`db` 容器）。
> 三张纸都放在桌上、名字都带 `docker` 或 `example`，但一张给调度、一张给店长、一张给库管。认错纸，活儿就派错人。

---

### 1.5 接下来该改哪一份 【官方】

官方对三份文件的编辑要求措辞不同，原文是这样的：

> Please edit `default.yml` and `docker.env` file as per the description. Also edit `compose.yml` as needed. (If you want to change the port etc.)

| 文件 | 官方原话 | 官方给出的改动示例 |
| --- | --- | --- |
| `.config/default.yml` | edit … **as per the description**（按文件里的说明改） | 未举例，由文件内注释说明 |
| `.config/docker.env` | edit … **as per the description**（按文件里的说明改） | 未举例，由文件内注释说明 |
| `compose.yml` | edit … **as needed**（按需改） | 「If you want to change the port etc.」，即例如改端口 |

具体的字段级操作分别在后面章节展开：`default.yml` 见第三章，`docker.env` 见第四章，`compose.yml` 见第二章。本章只需要建立一个观念——**「按文件内注释改」是官方的默认工作方式**，`default.yml` 和 `docker.env` 这两个文件里的大量注释本身就是说明书。

> [!tip] 大白话
> 把这两个配置文件想成一份「填空式表格」：每一项旁边都印着灰色小字说明该填什么，你只需要把孩子填进去。官方说「按说明改」，意思就是别凭感觉删注释、别自作主张改结构——留着那些说明文字，它是你以后回看时的唯一线索。

---

### 1.6 一个必须知道的文档缺陷：页面目录不可信 【官方】

打开这份指南时，页面顶部的目录（Table of Contents）看起来很正常，但它**漏掉了四个正文章节**。下面是页内目录实际列出的条目，与正文实际存在的章节对照：

| 页内目录实际列出 | 正文实际存在的章节 |
| --- | --- |
| Clone the Repository | Clone the Repository |
| How to execute CLI commands? | Configuration |
| （未列出） | Build & Initialize |
| （未列出） | Startup |
| （未列出） | Updating Misskey |
| How to execute CLI commands? | How to execute CLI commands? |

四个被漏掉的正是从「配置」到「升级」的完整主干。若你按页面目录当作步骤索引来读，会直接跳过本文档第三到六章要讲的全部内容。**结论：不要用这份文档的页内目录当导航，直接按正文章节顺序读。**

（顺带记一笔：官方页面正文里还有一处更严重的缺陷——更新流程最后一行两条命令粘连成了一条不可执行的命令。那属于第六章的范围，本章不展开，但提前告诉你「这份文档不能无脑照抄」，读的时候保持警觉。）

---

### 小结

- **前置条件只有一条**：装好 Docker 与 Docker Compose，官方未给最低版本号。
- **克隆用官方原文**：`git clone -b master https://github.com/misskey-dev/misskey.git`，随后 `cd misskey` 与 `git checkout master` 都保留，不自行优化。
- **三连拷贝是三件独立的事**：`compose_example.yml` → `compose.yml`、`.config/docker_example.yml` → `.config/default.yml`、`.config/docker_example.env` → `.config/docker.env`。
- **三者职责完全不同**：根目录的 `compose.yml` 管编排，`.config/default.yml` 管应用配置（靠 `.config` 只读挂载被读到），`.config/docker.env` 管数据库口令（由 `db` 服务经 `env_file` 读取）。
- **只改生效文件，不改 `_example`**：官方对 `default.yml` / `docker.env` 的要求是「按文件内说明改」，对 `compose.yml` 是「按需改（如端口）」。
- **文档缺陷**：页内目录遗漏 Configuration、Build & Initialize、Startup、Updating 四节，不可当作步骤索引。

### 下一章预告

产物已就位，下一章打开 `compose.yml`，逐段拆解这份编排文件：为什么 `web` 不是从镜像仓库拉取而是本地构建、`web` 如何等到数据库和 Redis 双双健康才启动、只有哪些端口真正对外、以及三处绑定挂载各自把宿主目录映射到了哪里——其中数据库那一处的目标路径有一个很容易写错的细节。

---

## 第二章：`compose.yml`——服务栈、依赖顺序、网络与挂载

上一章把三份产物摆到了位，但你还没看过其中任何一份的内容。本章只做一件事：把 `compose.yml` 从头到尾读一遍。它决定了这台机器上到底要跑哪几个容器、谁必须等谁、谁能对外开端口、以及数据最终落在宿主机的哪个目录——这四处全是后续配置与启动的落脚点，读错一处，第三章到第五章的努力都会打空。

> 本章读的是文件，不是操作。你不需要在本章执行任何命令；构建、初始化、启动是第五章的事。

---

### 2.1 先睹为快：整份文件长什么样

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

### 2.2 三个启用的服务

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

### 2.3 启动顺序：`web` 等 `db` 和 `redis` 双双体检合格

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

### 2.4 端口与网络：只有 `web` 对外开窗

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

### 2.5 三处绑定挂载（以及那个最容易写错的路径）

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

#### 最容易写错的一处：`/var/lib/postgresql` 不是 `/var/lib/postgresql/data`

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

### 2.6 `restart: always` 出现在全部三个服务上

【官方】`web`、`redis`、`db` 三个服务的定义里都有 `restart: always`【官方】[^c2-1]。含义是容器因任何原因退出（包括宿主机重启）都会被自动拉起。对自建实例而言这是必要的兜底：NAS 断电重来后不需要你手工 `up`，栈会自行恢复。

但要注意「自动拉起」不等于「启动顺序被保证」：`restart` 只负责各自复活，顺序仍需靠 2.3 的 `depends_on`。重启过程中若 `web` 比 `db` 先起来，`web` 会在启动时短暂连不上数据库，待 `db` 就绪后恢复正常。

---

### 2.7 只以注释存在的服务：不要以为它们在栈里

文件下半部分有一大段以 `#` 开头的服务定义，涉及三个名字：`mcaptcha`（`mcaptcha/mcaptcha:latest`）、`mcaptcha_redis`（`mcaptcha/cache:latest`）、`meilisearch`（`getmeili/meilisearch:v1.3.4`）【官方】[^c2-1]。

【官方】关键点：**它们全部被注释，默认不启用**，不属于当前服务栈【官方】[^c2-1]。只是顺手扫一眼文件的人，容易误以为这些名字也是要跑的服务——尤其在 `web.links` 里还留了两行注释形式的 `# - mcaptcha`、`# - meilisearch`，视觉上更像是「栈的一部分」。判断某服务是否启用，唯一可靠依据是它的定义是否被 `#` 注释掉。

本轮不展开这三个注释服务的配置（验证码是可选的反滥用组件，`meilisearch` 是备选全文检索方案，默认配置用的是 `sqlLike`）。你现在只需要记住：**它们没有在跑**。

> [!tip] 大白话
> 把注释块想成**样板间**：售楼处里摆着几套精装修的样板，看着像在卖，其实没有一户真的交付。文件里 `mcaptcha`、`meilisearch` 就是这种样板间——写在纸上、没接线。别把它们当成你机器上正在运行的东西。

---

### 2.8 卷权限：v13 的历史故障与仍未确认的现状

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

> 相关：容器 UID/GID 与宿主机文件权限的通用排查思路见 [[docker里的GID和UID]]；本节只记录 Misskey 这边的具体历史。

---

### 小结

- `compose.yml` 只启用三个服务：`web`（`build: .` 本地构建）、`redis:7-alpine`、`db: postgres:18-alpine`；`web` 不从镜像仓库拉取，所以部署机上必须保留完整源码树。
- 启动顺序由 `depends_on` + `condition: service_healthy` 保证：`web` 等 `db` 与 `redis` 双双健康才起；两个健康检查都是 `interval: 5s`、`retries: 20`，且**都未设 `timeout` 与 `start_period`**。
- 只有 `web` 发布宿主端口 `"3000:3000"`；`redis`、`db` 不开端口，仅在 `internal_network` 内可达。`web` 同时加入内、外两个网络。
- 三处绑定挂载：`./db → /var/lib/postgresql`（**不是 `…/data`**，全文件最易错处）、`./redis → /data`、`./files → /misskey/files`；另有 `./.config → /misskey/.config:ro` 只读挂入 `web`。三个服务均设 `restart: always`。
- `mcaptcha`、`mcaptcha_redis`、`meilisearch` 只以注释存在，默认不启用；卷权限方面，v13 曾出现 UID/GID `991` 导致的 EACCES 与 500，`chown` 无效、issue 当日关闭无修复记录，当前版本的实际 UID/GID 无来源可确认【推断】。

### 下一章预告

编排文件已经读通：容器怎么起、谁等谁、数据落哪，都清楚了。但 `web` 容器里跑起来之后要连哪个域名、用哪个数据库用户、端口对不对得上，这些不在 `compose.yml` 里，而在通过只读挂载送进去的那份应用配置里。下一章就打开 `.config/default.yml`，逐个过一遍**必须改**的字段、哪些可留默认，以及那几个「启动后改了就出事」的不可变项。
---

## 第三章：`.config/default.yml`——应用配置必改字段与不可变项

> 标注约定：`【官方】`＝官方文档或官方仓库一手文件直接陈述；`【推断】`＝本文档推断、无官方来源；`【过时】`＝已失效信息，按历史口径呈现。

上一章读的是 `compose.yml`，它只回答「跑哪些容器、它们怎么连」。这一章要处理的 `.config/default.yml` 回答的是另一个问题：**Misskey 这个应用自己怎么工作**——对外叫什么名字、连的数据库在哪、缓存用哪个实例、帖子 ID 怎么生成。

为什么这份文件值得单独用一章、而且比编排文件更危险？因为三份产物里只有它含有**一旦实例启动就基本不能再改**的字段，其中 `url` 一个字符写错，代价可能是把整个联邦关系网打碎。所以这一章的重点不是「把每一行都讲一遍」，而是**先把不可变的字段定死，再看哪些字段需要改、哪些保持注释即可**。

---

### 3.1 先睹为快：这份文件长什么样

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

### 3.2 `url`：全篇风险最高的一个字段

这是整章的重心，也是整份笔记里最不能出错的一行。因为它有两个叠加属性：**必须改**（默认是占位符）＋ **改完就基本不能反悔**。

#### 官方原文

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

#### 要改成什么

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

#### 为什么「启动后不可改」——四处独立信号

这不是某一个页面的口头提醒，而是四个互相独立的位置在说同一件事，官方把风险级别定得很高：

| # | 位置 | 原文 | 标注 |
| --- | --- | --- | --- |
| 1 | 配置文件本身 | `ONCE YOU HAVE STARTED THE INSTANCE, DO NOT CHANGE THE URL SETTINGS AFTER THAT!` | 【官方】[^c3-1] |
| 2 | Docker 部署指南页首 Danger 提示 | `Do not recreate the database with the domain/hostname of the server once you have started using it!` | 【官方】[^c3-2] |
| 3 | Ubuntu 安装指南页首 Danger 提示 | `Do not recreate the database for a domain/hostname that is already in use on a running server!` | 【官方】[^c3-4] |
| 4 | Ubuntu 安装指南正文 | `Never change the domain name or hostname of a server once it has been put into use!` | 【官方】[^c3-4] |

第 2、3 条是同一件事的两种表述，必须原样理解：**它禁止的是「用一个已在运行的服务器曾经用过的域名/主机名去重建数据库」**。换个说法——"这个域名我之前用过，现在想拿它重装一台新库" 这条路是被明确堵死的。它同时说明了为什么 `url` 属于「启动前必须定死」的字段。

反方向并没有被禁止：**全新域名 + 全新数据库**是正常的首次部署，不存在「用过」的包袱。

#### 写错的症状：无法注册

如果 `url` 填得不对，会怎样？【官方】排错页在 `Cannot Sign Up`（无法注册）条目下给了它一个具名原因[^c3-3]：

> It seems like it cannot connect to the API. Check if the `url:` at the beginning of `default.yml` is set correctly. Check the Node.js version and installation settings again carefully.

也就是说，客户端**连不上 API**，对外表现就是「注册不了」。这条信息很有用：当你的实例界面能打开、却卡在注册时，第一反应应该去回看 `default.yml` 开头的 `url`，而不是去猜数据库口令。

#### 启动后改动会怎样：社区给出的答案

配置文件说「不要改」，但没说「改了会怎样」。这个答案在官方仓库的一条问答讨论里，由维护者给出【官方】[^c3-5]：

> **I would highly recommend _not_ changing your URL. Due to how the Fediverse/ActivityPub works, changing your URL will most likely result in entirely broken federation.**

（强烈建议不要改 URL。由于 Fediverse/ActivityPub 的运作方式，改 URL **极有可能导致联邦完全损坏**。）

同一讨论里，有人追问「那你自己不是改过吗，怎么做到的」，维护者的回答同样值得原样保留，因为它恰好说明了「极少数成功案例」的真实成色【官方】[^c3-5]：

> 1. I changed it with my servers running **Firefish, not Misskey**
> 2. The whole process involved multiple custom scripts talking both to the server API and the database directly and was overall **extremely janky**. I wouldn't recommend that anyone try and recreate what I did tbh.

拆开看这两条：唯一被提到的成功案例**不在 Misskey 上**（那是另一个联邦软件 Firefish）；做法是一堆自定义脚本同时操作服务端 API 和数据库，作者自己评价为 extremely janky（极其粗糙），并且**明确不建议任何人效仿**。所以对 Misskey 用户来说，结论是：**没有可复制的正当路径**。

#### 【推断】文档没写、但你该意识到的后果

【官方】只说了「注册不了」和「联邦完全损坏」两个症状。**为什么会损坏**、损坏到什么粒度，官方没有展开。下面这条是本文档的推断，请与上面的官方结论分开看：

【推断】`url` 会被用来构造这个实例对外广播的身份标识（比如帖子和用户的 URI）。一旦这个值变了，**远端服务器数据库里记住的仍然是旧域名**——那些指向你实例的引用不会自动跟着改，于是形成「新旧地址并存、互相指不到对方」的错位状态。这解释了为什么官方宁愿让你「启动前定死」也不提供迁移方案：问题不在改这一行本身，而在于这个值早已被复制到了你控制不到的地方。

这是一条**推断**，没有官方原文支撑；它只用于帮你理解「为什么官方态度这么强硬」，不作为操作依据。

#### 还有两条路：环境变量与开发环境

【官方】配置文件里留了一句：`# You can set url from an environment variable instead.`——**`url` 也可以改用环境变量提供**。但要注意：**示例文件里并没有写出这个环境变量的名字**【官方】[^c3-1]。所以除非你去别处查到确切变量名，否则照示例直接改这一行是最稳的做法。

另一条是给开发环境的口径【官方】[^c3-4]：

> For a development environment, specify the URL as `url: http://localhost:3000`

这是**开发环境**的写法，来源是 Ubuntu 安装指南的 Tips，不要把它当成生产/内网部署的推荐值。你的目标场景（NAS、可能只有内网）属于官方**完全没有覆盖**的空白区——那部分设计属于本篇的推断范畴，会在后续章节单独讨论，本章只管把「`url` 是什么、为什么不能反悔」讲透。

---

### 3.3 第二个启动后不可改的字段：`id`

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

### 3.4 数据库连接：`db.*`

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

### 3.5 Redis：默认一个实例扛下所有角色

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

### 3.6 全文检索：`fulltextSearch.provider` 的出厂值

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

#### 一处文档缺陷：串位的注释

在 `fulltextSearch:` 块的第一行，有一句注释：

```yaml
fulltextSearch:
  # You can select the ID generation method.
```

这句话属于**从 `id` 块复制粘贴时留下的错位注释**——它和全文检索毫无关系（`id` 块里也有一句一字不差的 `# You can select the ID generation method.`）。读到它直接忽略即可，**不要因为这句话去找什么「ID generation」设置**【官方】[^c3-1]。

---

### 3.7 端口与代理绕行：`port` / `proxyBypassHosts`

这两个字段分散在文件的不同区段，但共同点是：**默认值即可，通常不需要改**。

#### `port`

```yaml
# .config/default.yml
# The port that your Misskey server should listen on.
port: 3000
```

【官方】`port: 3000` 表示 Misskey 应用在**容器内部**监听 3000。它与上一章 compose 里 `web` 发布的端口映射 `"3000:3000"` 相对应——宿主机的 3000 转发到容器的 3000【官方】[^c3-1]。所以：

- 如果你**不改** compose 的端口映射，这里就保持 `3000`；
- 只有当你在 compose 里换了宿主机端口（比如改成 `"8080:3000"`），才需要关心这个数字的对应关系。

同一区段的注释还画了一张图，说明 Misskey 需要反向代理来支持 HTTPS：用户 → 代理（443）→ Misskey（3000）。这里只是背景——**反代与 TLS 不是本章要解决的问题**，你只需要知道文件里这段注释是在解释「为什么 `url` 用 https、而 `port` 只是内部的 3000」【官方】[^c3-1]。

#### `proxyBypassHosts`

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

### 3.8 一大片「只以注释存在」的字段

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

### 3.9 YAML 正确性：一个缩进就能让 Misskey 停摆

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

### 本章小结

- **`url` 是本章的重心，也是整篇笔记风险最高的一个字段。** 它默认是占位符 `https://example.tld/`，必须改成「用户浏览器地址栏里应该看到的地址」；写错会导致**无法注册**（客户端连不上 API），而**启动后改动极可能导致联邦完全损坏**——唯一的成功案例发生在 Firefish（非 Misskey）上，靠多个自定义脚本操作 API 与数据库，作者自评极其粗糙、不建议效仿。配套的官方禁令是：**不要用已投入使用的服务器域名/主机名去重建数据库**。
- **还有一个同款不可变字段 `id`。** 出厂值 `id: 'aidx'`，备选 `aid`/`aidx`/`meid`/`ulid`/`objectid`，带一字不差的「启动后不可更改」警告；文件自述通常不需要改，保持默认即可。
- **需要动手改的其实很少。** `db.host: db`、`db.port: 5432`、`redis.host: redis`、`redis.port: 6379` 都必须与 compose 的服务名/端口对应（改一处要同步另一处）；`db.user`/`db.pass` 是占位值且必须与 `.config/docker.env` 一致——口令那一半留到下一章。
- **大量字段「只以注释存在」＝取默认值、当前不生效**（`disableCache`、`extra.ssl`、四个 Redis 角色块、`disableHsts`、`clusterLimit`、`threadPoolSize`、各投递并发与重试、`proxy`、`maxFileSize`、`logging`、`sentry*` 等）；不取消注释就不参与运行，**默认值就是给你用的**。
- **两个「无需改动」的出厂设置**：`fulltextSearch.provider: sqlLike` 是默认值、只依赖 PostgreSQL 标准能力、**不需要任何扩展**；`proxyBypassHosts` 是生效的非注释列表（`api.deepl.com`、`api-free.deepl.com`、`www.recaptcha.net`、`hcaptcha.com`、`challenges.cloudflare.com`）。另外，YAML **行首缩进写错会让 Misskey 不工作**，`fulltextSearch` 块首那句串位注释是文档缺陷、可直接忽略。

### 下一章预告

到这里，应用配置已经定死：实例叫什么、连哪个数据库、缓存怎么用、帖子 ID 怎么生成，全部有了答案。但还有一块拼图没接上——`db.user`/`db.pass` 这两个占位值**必须和另一份文件保持一致**，而那份文件还管着数据库容器的启动口令。下一章就进入 `.config/docker.env`，把「口令」这一环补齐，并说清一个反直觉的事实：改了这份文件，并不是所有地方都会跟着变。
---

## 第四章：`.config/docker.env`——数据库口令与变量注入

前两章分别处理了「起哪些容器」（`compose.yml`）和「Misskey 自己怎么跑」（`default.yml`）。还差一环：数据库容器的账号密码从哪来。答案就是这个只有 11 行的 `.config/docker.env`。它一分钟能读完，却埋着全篇唯一一个「不改就一定出事」的安全陷阱，所以单独成章。

---

### 4.1 先看全文

它是从 `.config/docker_example.env` 拷来的，全文如下（`【官方】`：与仓库示例逐字一致，`master` 与 `develop` 分支相同[^c4-1]）：

```env
# .config/docker.env
# misskey settings
# MISSKEY_URL=https://example.tld/

# db settings
POSTGRES_PASSWORD=example-misskey-pass
# DATABASE_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_USER=example-misskey-user
# DATABASE_USER=${POSTGRES_USER}
POSTGRES_DB=misskey
# DATABASE_DB=${POSTGRES_DB}
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

逐行拆开，只有 4 行真正生效，其余全被 `#` 注释掉 `【官方】`：

| 变量 | 值 | 状态 | 作用 |
| --- | --- | --- | --- |
| `MISSKEY_URL` | `https://example.tld/` | 注释 | 未说明用途（见 4.4） |
| `POSTGRES_PASSWORD` | `example-misskey-pass` | **生效** | 数据库口令——**必须改** |
| `DATABASE_PASSWORD` | `${POSTGRES_PASSWORD}` | 注释 | 备选写法（见 4.3） |
| `POSTGRES_USER` | `example-misskey-user` | **生效** | 数据库用户名 |
| `DATABASE_USER` | `${POSTGRES_USER}` | 注释 | 备选写法 |
| `POSTGRES_DB` | `misskey` | **生效** | 数据库名 |
| `DATABASE_DB` | `${POSTGRES_DB}` | 注释 | 备选写法 |
| `DATABASE_URL` | `postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}` | **生效** | 拼出来的连接串 |

所以这个文件的职责只有一件事：**给数据库容器一组账号、口令、库名，再顺手拼一个连接串。**

> [!tip] 大白话
> 把它想成「出租屋的水电开户单」——户名（`POSTGRES_USER`）、门锁密码（`POSTGRES_PASSWORD`）、房号（`POSTGRES_DB`），最后一行 `DATABASE_URL` 是把这三项抄成一句「门牌+钥匙」的完整地址。它不决定 Misskey 长什么样，只决定**数据库这扇门怎么开**——这也正是下一节那个陷阱危险的原因：门锁密码印在公开说明书上。

---

### 4.2 最大的坑：占位口令是一把真的能用的钥匙

这是本章最重要的一点 `【官方】`：`POSTGRES_PASSWORD=example-misskey-pass` 里的 `example-misskey-pass` **不是空占位符，也不是格式非法的假值**，而是一个语法完全合法、容器启动后立刻被采纳为真实口令的字符串[^c4-1]。也就是说：

- `cp` 完示例直接 `docker compose up`，数据库**会正常跑起来**，不会有任何报错提示你「密码没改」；
- 与此同时，你的实例口令就是 `example-misskey-pass`——一个写在 GitHub 公开仓库里、谁都能 `curl` 到的字符串。

【官方】把它列为必改清单的首要项[^c4-2]。危险恰恰在于它「不报错」：空口令会失败，非法格式可能被拒，而一个可用的弱口令会安静地跑下去。

改动时要连带处理一致性 `【官方】`：`default.yml` 的 `db.user` / `db.pass` 示例值同样是 `example-misskey-user` / `example-misskey-pass`，与这里必须对得上[^c4-3]。两处填的不是两个密码，而是**同一把钥匙的两份副本**，只改一边就连不上库。

> [!warning] 易错点
> 改口令要同时改两处：`.config/docker.env` 的 `POSTGRES_PASSWORD`（数据库容器用）与 `.config/default.yml` 的 `db.pass`（Misskey 应用用）。注意 `default.yml` 有一行注释说 `user` / `pass` **也可由环境变量提供**，但示例没写出变量名，所以默认仍按「写死在 YAML 里」理解。

---

### 4.3 `DATABASE_URL` 是拼出来的；另有三行注释备选

最后一行值得单独看：

```env
# .config/docker.env
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

`${...}` 是**变量插值**：加载方先把大括号里的名字替换成上面几行的值，再得到最终字符串。代入示例默认值，它展开成 `【官方】`：

```text
postgres://example-misskey-user:example-misskey-pass@db:5432/misskey
          └── POSTGRES_USER ──┘ └─ POSTGRES_PASSWORD ─┘ │    └ POSTGRES_DB
                                                         └── 主机名 db，端口 5432
```

两个可直接落地的结论：主机名 `db` / 端口 `5432` 必须与 `compose.yml` 的服务名、`default.yml` 的 `db.host` 一致；改口令只需动 `POSTGRES_PASSWORD` 一处，`DATABASE_URL` 展开后自动跟着变，反之若把连接串写成明文，就等于把口令抄了第二份，日后必然遗忘同步。

【推断】文件把连接串交给 `${VAR}` 插值而非写死字面量，意味着加载它的程序（Compose / dotenv 类实现）必须支持变量展开；若某环境不展开 `${}`，这行拿到的就是带花括号的原始字符串。文件本身没说展开由谁负责。

紧跟每个 `POSTGRES_*` 之后各有一行「镜像」写法，全部被注释 `【官方】`：`DATABASE_PASSWORD=${POSTGRES_PASSWORD}`、`DATABASE_USER=${POSTGRES_USER}`、`DATABASE_DB=${POSTGRES_DB}`。这说明 Misskey 也接受**把连接信息分项给**，由程序自己组装。三行都用 `${...}` 回指上面的 `POSTGRES_*`，可见作者本意不是让你另填一份值，而是换个变量名走另一条读取路径。至于两者同时存在时谁优先、哪种写法在哪些版本生效，示例没说，本笔记不猜 `【官方】`。

---

### 4.4 `MISSKEY_URL`：存在，但文件没说它是干什么的

第一行 `# MISSKEY_URL=https://example.tld/` 被注释，所以默认不生效 `【官方】`。它是文件里唯一的 `MISSKEY_*` 变量，位于 `# misskey settings` 注释组下，值是 `https://example.tld/`——与 `default.yml` 里 `url` 的占位值一模一样。

本笔记对此**不作断言**。若要给方向性判断，那只能是：【推断】它很可能与 `default.yml` 的 `url` 对应，用于从环境变量提供实例地址；但文件既把它注明为可选（已注释），又没给任何说明，因此不影响照抄示例跑通流程。

---

### 4.5 谁在真正读这个文件——「改了全局生效」是错的

这是本章第二个必须记住的点。回到 `compose.yml`，看两个服务的差别 `【官方】`[^c4-4]：

```yaml
# compose.yml（节选）
services:
  web:
    build: .
    # env_file:              ← 整行被注释掉
    #   - .config/docker.env
    volumes:
      - ./.config:/misskey/.config:ro   # 实际配置从只读挂载进容器

  db:
    image: postgres:18-alpine
    env_file:
      - .config/docker.env               # ← 这一行是生效的
```

| 服务 | 是否读 `docker.env` | 实际配置来源 |
| --- | --- | --- |
| `db` | **读**（`env_file` 生效） | `.config/docker.env` |
| `web` | **不读**（`env_file` 被注释） | `.config/` 只读挂载 → 即 `default.yml` |

由此得到两个必须记住的推论：

1. **改 `docker.env` 不会全局重配 Misskey。** 它只喂给 `db` 容器；`web`（Misskey 本体进程）拿配置的通道是 `.config` 只读挂载，读的是 `default.yml`。所以「我改了 `docker.env`，Misskey 就该用新口令」是**错误预期**：应用侧口令在 `default.yml` 的 `db.pass`，两个文件各管一半。
2. **这个文件是隐式必需的。** 因为 `db` 的 `env_file` 确实生效，`.config/docker.env` 一旦不存在，`db` 启动就失败——不像 `web` 有「不读也行」的余地。第一章「三连拷贝」不能漏掉任何一份，这里给出了其中一份的硬理由。

> [!tip] 大白话
> 把 `env_file` 想成「这张卡能刷开哪个房间的门」：`db` 那行没被注释，是「能刷开数据库房间」；`web` 那行加了 `#`，等于「刷不开 Misskey 房间的门」，而 Misskey 房间的钥匙挂在另一面墙（`.config/default.yml`）上。所以指望「改一次 `docker.env`，全楼换锁」不成立。

---

### 小结

- 职责单一：给 `db` 容器提供 `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB`，并拼出 `DATABASE_URL` `【官方】`。
- **首要必改项**：`POSTGRES_PASSWORD=example-misskey-pass` 是可直接生效的占位口令，照抄不改会得到一个口令公开可知的实例 `【官方】`。
- `POSTGRES_USER` 默认 `example-misskey-user`、`POSTGRES_DB` 默认 `misskey`；同名的 `DATABASE_*` 三行是注释备选写法，说明 Misskey 也能分项读取连接信息 `【官方】`。
- `DATABASE_URL` 由 `${VAR}` 插值拼出，改 `POSTGRES_*` 会自动同步；主机名 `db` / 端口 `5432` 必须与 `compose.yml`、`default.yml` 一致 `【官方】`。
- `MISSKEY_URL` 存在但被注释、未说明用途；**改 `docker.env` 不等于重配 Misskey**——`web` 的 `env_file` 被注释，应用配置走 `.config` 只读挂载，而 `db` 的 `env_file` 生效使本文件成为隐式必需文件 `【官方】`。

---

三份产物到这里全部处理完：编排、应用配置、数据库口令。下一章进入执行环节——按官方三步走 `build` → `run --rm web pnpm run init` → `up -d`，并在上机前对照内存地板与 CPU 指令集门槛做一次自查。

---

## 第五章：构建 → 初始化 → 启动——跑通链路

前面几章我们把 `compose.yml`、`.config/default.yml`、`.config/docker.env` 都改完了，但屏幕上还没有任何东西在跑——配置再正确，也只是三份躺在磁盘上的文本。这一章就是兑现前面所有准备的地方：按顺序跑三条命令，让 Misskey 真正起来。但它不是「照着敲三条命令」那么简单——在你按下回车之前，有两个硬件门槛会直接决定这次部署是「跑通」还是「根本跑不起来」，其中一个是从 2026.7.0 才开始生效的硬性要求，老旧 NAS 上很可能属于「还没开始就已经结束」。

---

### 开始之前：先自查两个硬件门槛

这两个检查必须在跑命令之前完成。它们不看你配置得对不对，只看你机器行不行。

#### 门槛一：CPU 指令集 SSE4.2（2026.7.0 起的 go / no-go）【官方】

这是本轮升级里最容易被忽略、代价却最大的变化。2026.7.0 的发布说明在开头就单独列出了它：

> バックエンドで画像処理に用いているライブラリ sharp のシステム要件の変更により、**SSE4.2 命令セットをサポートしていない x86_64 CPU では Misskey が正しく動作しなくなります**。仮想マシンに Misskey をデプロイしている場合や、古いハードウェアをお使いの場合は、アップデート前にお使いの環境をご確認ください。なお、**ARM64 など x86_64 ではない環境においてはこの変更による影響はありません**。[^c5-4]

拆开看，这条约束的边界非常清楚：

| 维度 | 内容 |
| --- | --- |
| 从哪个版本开始 | **2026.7.0** 起生效 |
| 成因 | 后端图像处理库 **sharp** 的系统要求变更 |
| 影响谁 | **不支持 SSE4.2 的 x86_64 CPU** |
| 不影响谁 | **ARM64 等所有非 x86_64 环境** |
| 对老旧 NAS 意味着什么 | 用老旧 Celeron / Atom 这类低端 x86_64 芯片的 NAS、以及在旧 PC 上跑的虚拟机，可能**无法正确运行 Misskey** |

请注意这里的措辞是「无法**正确**运行」，不是「跑不起来会报错」——这类指令集缺失往往表现为运行期异常，而不是构建期就拦住你。所以别指望「能构建成功」就等于「没问题」：构建通过只说明镜像造出来了，跑起来还需要 CPU 本身支持 SSE4.2。对你手上的 NAS，正确做法是去买之前先查这颗 CPU 的规格说明里有没有 SSE4.2，而不是先部署再排查。

> [!tip] 大白话
> 把 SSE4.2 想成新家电要求的插座规格：说明书上写着「必须要三孔带地线」，你家墙上老式两孔插排插上去，未必当场冒烟，但电器就是不能正常转。所以选购 NAS 或按下部署键之前，先确认这台机器的「插座」合不合规。

#### 门槛二：内存——两个口径，千万别记混【官方】

内存这块最容易出错的地方，是把不同作用范围的两个数字揉成一个。官方给出的其实是**两把不同尺子**：

| 数字 | 口径（作用范围） | 性质 | 来源 |
| --- | --- | --- | --- |
| **至少 2GB** | **构建 Misskey + 执行数据库迁移（含初始化）** | 硬地板，低于此构建会失败 | 手动安装指南[^c5-2] / 排错页[^c5-3] |
| **推荐约 4GB** | **运行整体** | 推荐值 | 手动安装指南[^c5-2] |
| ~~约 1.5GB~~ | ~~构建~~ | **【过时】** 历史口径，已失效 | 手动安装指南[^c5-2] |

三个数字的原文口径分别是：

- 2GB【官方】：「Building Misskey and running database migrations (including initialization) require at least 2GB of RAM.」——这是**构建 + 迁移**的硬地板，它管的是「能不能造出来」。[^c5-2]
- 4GB【官方】：「It is recommended to have around 4 GB of memory.」——这是面向**整机运行**的推荐值，它管的是「跑起来顺不顺」。[^c5-2]
- 1.5GB【过时】：「Previously, it was explained that the build could be completed with approximately 1.5 GB of memory due to the introduction of Vite. However, the frontend build requirements have recently become more demanding again.」——曾经成立，因前端构建需求回升而失效，只作历史说明。[^c5-2]

排错页独立给了一句同口径的表述：「Empirically, Misskey requires at least 2GB of memory to build.」[^c5-3]

> [!warning] 一个必须点破的错觉
> 「2GB」和「4GB」**不是同一个指标的两个版本**，不能理解成「官方说 4GB 就够，2GB 是旧的」。它们量的是两件事：一个是「构建时别被 OOM 杀掉」的地板，一个是「实例长期运行」的推荐配置。本章后面提到的任何内存数字，都请回到这张表对照它的作用范围。

内存不够时，官方给出两条缓解路径【官方】[^c5-2]：

1. **给服务器加 swap 空间**；
2. **在本机（你的 PC）构建，再通过 SFTP 把构建好的目录传到服务器**。

排错页给出的是同一思路的另一半：也可以「扩大服务器规格，或者在自己的 PC 上构建后再部署上去」[^c5-3]。

> [!tip] 大白话
> 把这两个数字想成装修：2GB 是「楼板最低承重」——低于它，材料一上楼就塌（构建失败）；4GB 是「住进来之后的活动面积」——住人、走线、摆家具都得算进去。拿承重标准去衡量居住面积，或者反过来，都会得出错误结论。

#### 附：支持架构，以及一个「什么都查不到」的事实【官方】

支持架构为 **amd64 与 arm64**，官方同时描述「较新的 CPU 足以以极少资源运行本系统」[^c5-2]。这句话要和上面的 SSE4.2 门槛一起读：官方说「较新的 CPU 够用」，而 2026.7.0 之后「够用」的前置条件里加上了 x86_64 必须支持 SSE4.2。

还有一个反直觉的事实值得单独说：**容器版部署指南与 env 示例里，没有任何内存 / CPU / 磁盘数字**【官方】。上面 2GB / 4GB / 1.5GB 全部只出自「手动安装」路径（手动 Ubuntu 指南与排错页），容器指南只在资源索引里指向一篇单独的 Scaling 文章[^c5-1][^c5-2][^c5-9]。也就是说，如果你只看容器指南，是永远看不到内存门槛的——这正是它最危险的盲区。

---

### 三条命令，按顺序跑

先把完整链路一次性摆出来，再逐条解释。这三条命令都出自容器指南，`sudo` 前缀是官方原文，**原样保留、不要省略、不要重排**【官方】[^c5-1]：

```bash
# 执行位置：misskey 仓库根目录（clone 出来的那个目录）
sudo docker compose build                          # 第一步：本地构建 web 镜像
sudo docker compose run --rm web pnpm run init     # 第二步：执行数据库初始化
sudo docker compose up -d                          # 第三步：后台启动整个服务栈
```

指南在这一节的原话是：「The next set of commands will build Misskey image and perform database initialization. **This will take some time.**」——官方明确提醒这会花不少时间，别以为卡住了。[^c5-1]

注意：**第一步和第二步是两条独立命令，必须按顺序分别执行**，不存在「一条命令顺手把初始化也做了」的方式，也不存在一个叫 `init` 的独立服务【官方】[^c5-1]。

> [!tip] 大白话
> 把 `docker compose build` 想成「在自家厨房把所有食材先处理备齐」：切配、腌制、预热，一步都不能少，且最耗时间。后面的启动只是「菜备好了，开火下锅」。跳过备料直接下锅，端上来的是一盘夹生菜。

#### 第一步：构建 `sudo docker compose build`【官方】

这条命令对应第二章讲过的 `web: build: .`——Misskey 的 web 镜像**不是从镜像仓库拉下来的**，而是用仓库根目录的 Dockerfile 在本机现场构建的[^c5-5]。所以：

- 目标机器上**必须保留完整的源码树**，不能只留几个配置文件；
- 构建过程本身就是内存最吃紧的时刻，也就是上面那张表里 **2GB 硬地板**真正发挥作用的地方——内存不足是服务端构建失败的具名原因[^c5-2]；
- 官方没有为这一步提供任何预构建镜像方案，NAS 上「现场构建」几乎是必经之路。

这一步官方没有给出样例输出。判断成功的通用信号是命令正常退出、没有构建错误（而不是被 OOM 中途杀掉）。如果你在 NAS 上跑到一半失败，先回到内存门槛那一节——多数情况是内存问题，而不是配置问题。

#### 第二步：初始化 `sudo docker compose run --rm web pnpm run init`【官方】

这条命令做的，就是发布说明里所说的「database migrations (including initialization)」——**数据库迁移与初始化**[^c5-2]。

关于它的形态，有三个要点必须记住：

1. **它跑在一个一次性的 `web` 容器里**，不是某个常驻的 init 服务[^c5-1]。
2. **`--rm` 是关键**：它表示容器退出后立即删除。初始化是一次性的活，干完就散，不需要留下这个容器占着磁盘或干扰后续 `up`。
3. 它复用 `web` 这个服务定义，所以它和第三步启动的**是同一套配置、同一个镜像**——第二、三步之间不需要重新构建。

> [!tip] 大白话
> 把 `--rm` 想成请了一次性的临时工：他拿着临时工牌进场，把「初始化数据库」这件事干完，出门时工牌当场回收、人也不留在名册上。如果不要 `--rm`，这个干完活的临时工会一直挂在你的容器列表里，成了没人管的僵尸记录。

#### 第三步：启动 `sudo docker compose up -d`【官方】

`-d` 表示 detached，**后台运行**：命令会返回，容器继续在后台跑[^c5-1][^c5-5]。这一步没有新东西要你配置——它启动的就是第二章读过的服务栈：`web`、`redis`、`db`，并按 `depends_on` + `condition: service_healthy` 的规则等 `db` 与 `redis` 双双健康后才拉起 `web`[^c5-5]。你不需要手工先起数据库，顺序由编排文件替你保证了。

> [!tip] 大白话
> `-d` 就像按下空调遥控器的开机键：灯亮、机器开始工作，但你不必站在出风口前一直守着。命令一返回，你的终端就能干别的了。

---

### 跑起来之后：NAS 上会「慢」在哪【推断】

链路如果一切正常，到这一步你已经有一个在跑的实例了。但在 NAS 这类磁盘 I/O 较慢的环境上，有两个可以预期的现象，需要提前有心理准备。

**首次 `docker compose up -d` 的等待会明显更久。** 原因不是 Misskey 变慢了，而是两个健康检查各自的参数：`redis` 用 `redis-cli ping`、`db` 用 `pg_isready`，两者都只设了 `interval: 5s` 与 `retries: 20`，**都没有设置 `timeout` 与 `start_period`**[^c5-5]。健康检查要反复探测、在慢速存储上每次探测本身也慢，于是「等健康」这一段的累积时间被拉长。这一条属于**本文的推断**——容器指南与示例文件都没有讨论 NAS 场景，是从「健康检查缺 `timeout`/`start_period`」这个已核实的事实，加上慢速存储这个前提推出的，不是官方陈述。

应对方式很简单：**首次启动多等一会儿，不要看到进度慢就急着反复重启**。反复重启只会让数据库与 Redis 反复经历冷启动，把慢变成更慢。

> [!warning] 与内存门槛的关系
> 这里说的「慢」是 I/O 慢，不是内存不够。别把「启动等很久」误判成「内存不够」从而去加 swap——两者是不同的症状：内存不足通常表现为**构建阶段**被 OOM 杀掉（对应那张表里的 2GB 地板），而不是启动阶段单纯地慢。

---

### 资源相关设置：都在注释里，别去正文找【官方】

如果你翻回第三章看 `.config/default.yml`，会发现唯一与资源相关的可调项是 `clusterLimit`（worker 进程数）与 `threadPoolSize`（每个 worker 的 CPU 密集任务线程数）——两者**都是注释状态、不取消注释即不生效、默认值均为 `1`**[^c5-8]。也就是说，当前配置模型里没有一个「内存上限」之类的开关：内存能不能满足，靠的是你选机器，而不是改 YAML。

> [!tip] 大白话
> 把 `.config/default.yml` 里那些资源相关的行想成「装修图册里的可选方案页」：印在册子上不等于砌进墙里，不把注释符号去掉，它们就永远只是纸面上的建议。想靠改这个文件「加大内存」，方向就错了。

---

### 顺手记住：临时跑一条后端命令

跑通之后，你迟早会需要单独执行一条后端命令（比如查状态、跑维护脚本）。官方给的统一套路是复用同一个「一次性容器」模式【官方】[^c5-1]：

```bash
# 执行位置：misskey 仓库根目录
sudo docker compose run --rm web node packages/backend/built/tools/foo bar
```

把结尾的 `packages/backend/built/tools/foo bar` 换成你真正要执行的那个脚本及其参数即可。模式和你刚跑过的初始化完全一样：`run --rm` + 一次性的 `web` 容器。记住这个形状，后面遇到需要「进 Misskey 内部跑一条命令」的场景，直接套用。

> [!tip] 大白话
> 把这条命令想成「给工厂里临时派一张工单」：不用把整条产线停掉，只叫一名临时工进来，单独把 `foo bar` 这活干完就走。你不需要改动正在运行的服务，也不需要在容器列表里留下痕迹。

---

### 小结

- **上机前先过两道硬件关卡**：CPU 侧是 2026.7.0 起的 SSE4.2 硬门槛（只影响 x86_64，不影响 ARM64）；内存侧要分清 **2GB 是「构建+迁移」的硬地板**、**约 4GB 是「运行整体」的推荐值**，两者不可合并，`1.5GB` 已是【过时】口径。
- **三条命令按顺序跑**：`sudo docker compose build` → `sudo docker compose run --rm web pnpm run init` → `sudo docker compose up -d`；`sudo` 与全部参数为官方原文，逐字保留。构建会明显耗时。
- **初始化是一次性容器，不是独立服务**：`--rm` 让它在干完活后自动消失；第一步与第二步是两条**独立且有序**的命令。
- **`up -d` 是后台启动**，依赖顺序由编排文件内的健康检查保证，你不需要手工先起数据库。
- **NAS 慢不是错的信号**：健康检查缺 `timeout`/`start_period`，慢速存储上首次启动会更久（【推断】）；这与「内存不足导致构建失败」是两回事。

### 下一章预告

现在你有一个能访问、能注册、能发帖的实例了，但「跑起来」只是起点——Misskey 会持续发布新版本，其中还包括明确要求尽快升级的安全版本。下一章我们进入长期维护视角：完整的升级流程（以及官方文档里那条**粘连到不能照抄**的命令要怎么拆开）、镜像标签策略，以及 NAS 上那些仍然悬而未决的遗留约束。
---

## 第六章：升级流程与 NAS 遗留约束

前五章把实例跑起来了：产物落位、编排文件、应用配置、数据库口令、构建初始化启动。但一个自建实例真正的寿命是从第二次升级开始的——Misskey 迭代很快，近期连续几个版本都带着会改变运行环境的破坏性变更。这一章解决两个问题：**照着官方流程安全地升级一次**，以及**在 NAS 这种非标准环境上，哪些结论有官方依据、哪些只是本文推断、哪些已经过时**。读完它，你应该能独立判断「这次升级我能不能直接上」。

> [!warning] 升级前的第一动作不是敲命令
> 官方在更新章节明确要求：**升级前务必先查阅 release notes / `CHANGELOG.md`，提前确认本次变更内容以及是否需要额外步骤（通常不需要）**。【官方】[^c6-1] 这句话不是客套——后文 6.4 列出的破坏性变更，全部只能从发布说明里读到，升级流程本身不会提示你。

---

### 6.1 官方升级流程，逐条拆解

官方容器版指南给出的更新流程是一条直线，按顺序执行即可。先把完整产物放出来，再逐条解释为什么这么写。

```bash
# 在 Misskey 仓库根目录执行（来源：S01「Updating Misskey」）
git stash
git checkout master
git pull
git submodule update --init
git stash pop
sudo docker compose build
# 原文此处两条命令粘连，已拆分为两步，见 6.1.1
sudo docker compose stop
sudo docker compose up -d
```

| 步骤 | 命令 | 作用 |
| --- | --- | --- |
| 1 | `git stash` | 把本地对源码树的改动（含你改过的配置）暂存起来 |
| 2 | `git checkout master` | 切到官方主干分支 |
| 3 | `git pull` | 拉取最新代码 |
| 4 | `git submodule update --init` | 同步子模块 |
| 5 | `git stash pop` | 把暂存的本地改动重新盖回来 |
| 6 | `sudo docker compose build` | 用新代码重新本地构建镜像 |
| 7 | `sudo docker compose stop` | 停服（原文粘连行的前半段） |
| 8 | `sudo docker compose up -d` | 启动（原文粘连行的后半段） |

**为什么先 stash 再 pop**：这份流程刻意把本地改动藏起来、拉完代码再放回来，目的就是**保留你对配置文件的修改**。【官方】[^c6-2] 如果你改的是 `.config/default.yml`、`.config/docker.env` 这类被 git 跟踪的文件，这一步保证它们不会被 `git pull` 冲掉。

> [!tip] 大白话
> 把 `git stash` / `git stash pop` 想成「升级前先把自己桌上的私人物品收进抽屉，等装修队换完地板再摆回原位」——不这么做，装修队（`git pull`）会把你桌上的东西当垃圾清走。所以这两步是成对的，缺了 `pop`，你的配置改动就失踪了。

#### 6.1.1 文档缺陷：末行两条命令粘连

上面的拆解里第 7、8 步并不是官方原文的分行，而是**本文对一处上游文档缺陷的修正**。S01 更新流程的最后一行把两条命令粘在了一起，中间没有任何分隔符：

```text
# 来源：S01「Updating Misskey」原文末行（缺陷：两条命令粘连、无分隔符，照抄不可执行）
sudo docker compose stop sudo docker compose up -d
```

这行**不能照抄执行**——shell 会把 `stop` 后面的整串当成参数，而不是第二条命令。它实际想表达的是「停服」和「启动」两步。官方页面在这里丢失了一个换行，本文按两步呈现。【官方（缺陷）】[^c6-3]

> [!tip] 大白话
> 这就像说明书把「关电源」和「按启动键」两个按钮的图印嵌在一起，看起来像一个按钮。你要做的是把它们当两个动作分开执行，而不是去按那个不存在的合并按钮。

#### 6.1.2 升级路径里没有什么

比「有什么」更重要的是「没有什么」，因为这直接决定你升级时**不需要**多做什么：

- 升级流程**没有**重复 `pnpm run init`。初始化只在首次部署时做过一次。【官方】[^c6-4]
- 除了一句「通常不需要额外步骤」，官方**没有给出任何显式的数据库迁移命令**。【官方】[^c6-5]

换句话说，照着上面 8 步走完，迁移是构建与启动过程内部完成的，不需要你手工触发。这也再次说明**为什么升级前必须读发布说明**：一旦某个版本真的需要额外步骤，官方只会写在 `CHANGELOG.md` 里，流程本身不会提醒。

**耗时预期**：升级耗时取决于**本次更新内容**与**数据库规模**。【官方】[^c6-6] 在 NAS 上，磁盘 I/O 偏慢会把这段时间进一步拉长。

> 相关：容器更新的通用做法（含镜像加速与版本锁定）见 [[docker容器如何更新]]；本节只讲 Misskey 自己的升级路径。

---

### 6.2 镜像标签策略：哪些固定、哪些浮动

升级时另一个绕不开的问题是「镜像从哪里来、版本锁没锁」。把编排文件里的实际写法摊开看最清楚。

| 服务 | 镜像写法 | 标签是否固定 |
| --- | --- | --- |
| `web` | `build: .`（本地构建） | 不适用——无镜像标签 |
| `redis` | `redis:7-alpine` | 固定主版本 |
| `db` | `postgres:18-alpine` | 固定主版本 |
| `mcaptcha`（注释，未启用） | `mcaptcha/mcaptcha:latest` | 浮动 |
| `mcaptcha_redis`（注释，未启用） | `mcaptcha/cache:latest` | 浮动 |
| `meilisearch`（注释，未启用） | `getmeili/meilisearch:v1.3.4` | 固定 |

数据来源：S07 编排示例。【官方】[^c6-7]

这里最关键的一点是 **`web` 应用镜像不是从 registry 拉取的，而是用仓库根目录的 Dockerfile 本地构建**（`build: .`）。【官方】[^c6-8] 因此：

- **不存在一个「官方发布的、带版本号的应用镜像」供你固定**。你升级应用的方式是 `git pull` 换代码、再 `docker compose build` 重建，而不是改一个 tag。
- 真正会被「拉取」的只有数据库和 Redis 两个基础镜像，它们的标签是固定的。
- 官方**没有给出** registry 预构建镜像或版本固定策略。【官方】[^c6-9]

补充一个容易漏掉的相邻事实：官方资源索引里确实存在一篇 **「How to push to Docker Hub using GitHub Actions」**，指向仓库内的 `/.github/workflows/docker.yml` 示例。【官方】[^c6-10] 但那是给你**自己推送镜像**用的示例，不是官方替你发布了一个可拉取的发行镜像——别把它误读成「有官方镜像可以 pin」。

> [!tip] 大白话
> 把 `web` 想成「自家厨房现做的菜」，`redis`/`db` 想成「超市买的固定品牌调料」。升级时你换的是自家厨房的菜谱（`git pull` 新代码）然后重做，而不是去货架上换一包「Misskey 2026.9.0 预包装版」——因为市面上根本没有这包预包装版。而浮动的 `latest` 标签则像「让厨师自由发挥」，每次可能给你不同的东西，所以那两项目前只是注释、并未启用。

---

### 6.3 升级前必须自查的破坏性变更

这一节是本篇最该反复看的部分。以下变更多半来自 **2026.7.0**，其中包含硬件门槛、运行环境版本和配置书写方式三类「不看就会踩」的改动。

| 版本 | 变更 | 对升级的实际影响 |
| --- | --- | --- |
| 2026.7.0 | Docker 镜像基础环境升级：Node.js → `26.4.0`，Debian → trixie (v13) | 镜像底层整体重建，glibc / Debian 大版本同时跃迁 |
| 2026.7.0 | 最低 Node.js 版本提高到 **22.22.2 / 24.17.0 / 26.4.0** | 非容器运行或自建镜像者需先升 Node；v22 仍可用但计划未来移除 |
| 2026.7.0 | x86_64 必须支持 **SSE4.2** 指令集 | VM 与老旧硬件升级前须自查；**不影响 ARM64** |
| 2026.7.0 | 敏感媒体判定改为调用外部服务 `sensitive-detector` | 依赖此功能的实例需自建服务，否则功能静默失效 |
| 2026.7.0 | YAML 解析器更严格，旧写法可能启动报语法错误 | 升级前须检查 `.config/default.yml` |
| 2026.7.0 | 移除 2025.4.0 及更早版本的客户端设置迁移 | 跨版本跳跃者需先经过一次 2026.5.1 |
| 2026.9.0 | 安全版本，含 7 个 GHSA 公告 | 官方要求尽快升级；未见重述 2026.7.0 的要求变更 |

数据来源：S10b（2026.7.0）、S10a（2026.9.0）。【官方】[^c6-11] 下面逐条展开。

#### 6.3.1 运行环境基线跃迁（2026.7.0）

2026.7.0 把 Docker 镜像的 Node.js 升到 **26.4.0**、Debian 升到 **trixie (v13)**。【官方】[^c6-12] 同时把最低 Node.js 版本提高到 **22.22.2 / 24.17.0 / 26.4.0**：v24 与 v26 受支持，v22 仍能运行但**计划在未来版本移除支持**。【官方】[^c6-13]

对容器部署的你来说，这一条大多由镜像替你消化；但如果你曾经把 Misskey 装到裸机、或自己维护镜像，就必须先确认运行时的 Node 版本已达标。

#### 6.3.2 CPU 指令集门槛（2026.7.0）

这是第五章讲过的硬件门槛，在这里换一个视角看：它是一条**「升级前必须确认」的版本级变更**。2026.7.0 起，**不支持 SSE4.2 指令集的 x86_64 CPU 将无法正确运行 Misskey**，成因是后端图像处理库 **sharp** 的系统要求变更；影响虚拟机与老旧硬件，**ARM64 等非 x86_64 环境不受影响**。【官方】[^c6-14]

对 NAS 用户尤其重要：老旧 Celeron / Atom 类 CPU 可能不满足，升级前应先在目标机上确认指令集。

#### 6.3.3 敏感媒体检测外置（2026.7.0）

NSFW 判定从「本体内置 `nsfwjs` 推理」改为「对外部服务 `sensitive-detector` 的 HTTP 调用」。【官方】[^c6-15] 具体分工是：**图像的归一化、视频抽帧、阈值判定与聚合仍由 Misskey 本体完成**，只把「已归一化图像的推理」这一步委托给外部服务。【官方】[^c6-16]

关键后果：依赖敏感检测的实例需要**自行部署 `sensitive-detector`**，并在控制台「モデレーション > センシティブなメディアの検出」里填连接地址；**若连接地址未配置，则完全不进行判定，一切按非敏感处理**。【官方】[^c6-17]

> [!warning] 静默失效，不会报错
> 「未配置即不检测」意味着升级后你的实例不会崩、不会报错，只是**敏感媒体不会再被自动标记**。这是一个容易在升级后被忽略的功能缺口，升级后务必到控制台确认该地址是否已填。

#### 6.3.4 配置解析更严格（2026.7.0）

YAML 解析器升级后校验更严格，**启动时读取 config 可能因语法错误而失败**。【官方】[^c6-18] 发布说明点名的例子是 `allowPrivateNetworks`：如果你沿用 2026.6.0 及更早的 `example.yml` 写法，就需要**把数组的闭括号缩进提高，或改写为 list 形式**。【官方】[^c6-19] 换言之，第三章那份「YAML 行首缩进写错会直接导致 Misskey 无法工作」的警告，在 2026.7.0 之后被解析器本身强化了。

#### 6.3.5 客户端设置迁移（2026.7.0）

2026.7.0 **移除了从 2025.4.0 及更早版本迁移客户端设置的能力**：若你想从 2025.4.0 直接跳到 2026.6.0 以上，设置**不会**被迁移；想迁移必须**先经过一次 2026.5.1**。【官方】[^c6-20] 这条只影响「跨了很大版本跨度」的实例，长期跟着升级的用户不会遇到。

#### 6.3.6 最新版本：2026.9.0 是安全版本

2026.9.0 是一个**安全版本，包含 7 个 GHSA 公告**，上游以醒目提示要求尽快升级到该版本或最新版。【官方】[^c6-21] 需要留意的是：**它没有重述或修订 2026.7.0 的那批要求变更**——也就是说，2026.7.0 的 SSE4.2、Node 最低版本、sensitive-detector 等要求，在 2026.9.0 的发布说明里既没被重申，也没被取消。【官方】[^c6-22]

---

### 6.4 【推断】三则：有本文结论、无官方来源

从第一章到这一章，大部分结论都指向官方一手来源。但有三处是**本文档的推断，没有任何官方出处**。把它们集中在这里，方便你给它们的可信度降一档看待。

| # | 推断内容 | 为什么是推断 |
| --- | --- | --- |
| 推断 1 | **仅内网 / 无公网域名方案** | 官方文档完全没有覆盖该场景；反代文档只给「公网域名 + Let's Encrypt」的配置 |
| 推断 2 | **NAS 分步指引** | 未找到 NAS 专属一手实操记录，只有聚合类二手教程，本期不再依赖 |
| 推断 3 | **需要 `docker compose` v2** | 官方只要求「已安装」；是从示例用到的特性反推出来的 |

**推断 1 —— 仅内网 / 无公网域名方案**。官方文档**完全没有**覆盖无公网域名的场景，反向代理文档只给出公网域名 + Let's Encrypt 的配置。【推断】本文中凡是涉及「仅内网使用」的建议，都是需要你自行设计的空白区，不是官方指引。

**推断 2 —— NAS 分步指引**。本期未找到 NAS 专属的一手实操记录，只有聚合类二手教程。因此本篇不依赖任何「NAS 专属步骤」，相关步骤一律按通用路径改写并标注为推断。【推断】

**推断 3 —— `docker compose` 版本**。官方只要求「Docker 与 Docker Compose 已安装」，未给最低版本。【官方】[^c6-23] 但示例编排文件使用了 `depends_on.condition: service_healthy` 与顶层 `networks` 这类特性，**实际上需要 Compose v2**。这是从示例用到的能力反推出的要求，官方并未明说。【推断】

> [!tip] 大白话
> 把三类标记想成食品保质期的三种标注法：【官方】是「厂家印刷的成分表」，【推断】是「本店厨师的口味建议」，【过时】是「上一版包装上的旧配方」。买东西先看厂家成分表，口味建议可以参考但可能不合你胃口，旧配方则只能当历史看——别照着旧配方做菜。学会扫一眼标记，就不会把「厨师建议」当成「厂家承诺」。

---

### 6.5 【过时】两则：只能按历史口径读

以下两条信息在官方页面上仍然存在，但**已经过时**，本章按历史信息呈现，正文不得据此操作。

#### 6.5.1 安装指南里的 Node.js 版本 pin

S06（Ubuntu 手动安装指南）的安装命令把 Node 源 pin 在 **`NODE_MAJOR=20`**：

```bash
# S06 安装命令中的 Node 源（已过时，勿据此操作）
NODE_MAJOR=20; echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list;
```

但**同一页面**的验证文字却说：如果输出类似 **`v22.x.x`** 则安装成功。【过时】[^c6-24] 同一页面对 Node 版本自相矛盾，说明该段落已滞后。**处理原则：以发布说明为准**——即 6.3.1 给出的最低版本 **22.22.2 / 24.17.0 / 26.4.0**。【过时】

#### 6.5.2 Redis 密码条目

排错页（S04）声称：**11.20.2 之前的版本无法解析 Redis 密码**，因此 Redis 必须不设密码、并把 `default.yml` 里 `redis:` 下的 `pass:` 行注释掉。【过时】[^c6-25] 该页面自身标注为「2018-10-07 撰写、2021-12-20 最后更新」，这条指引只对 11.20.2 之前的老版本成立，**已不适用于当前版本线**。【官方（页面日期）】

> [!warning] 不要把旧条目当现行最佳实践
> 你若在网上看到「Misskey 的 Redis 必须无密码」这类说法，源头多半就是这条 2021 年的旧条目。它描述的是 11.20.2 之前的限制，不是当前版本的配置建议。遇到历史信息与发布说明打架，**发布说明优先**。

---

### 6.6 相邻官方事实

以下几条有官方依据、值得知道，但都不构成需要你执行的配置步骤，各一句话带过：

- **反向代理**：官方建议用 **nginx** 作反向代理，并把 Misskey 运行在不直接暴露到公网的状态下。【官方】[^c6-26]
- **CDN**：对外发布时，官方**强烈建议使用 Cloudflare 等 CDN**。【官方】[^c6-27]
- **家用服务器的端口**：若在家用服务器上托管，需确认路由器允许 **80 与 443** 入站连接。【官方】[^c6-28]
- **FFmpeg 与 ImageMagick**：**FFmpeg 用于处理视频与音频、是需要的**；而 **ImageMagick 明确不需要**。【官方】[^c6-29]
- **AGPL-3.0 披露义务**：Misskey 采用 AGPL-3.0，**fork 或修改其源码会触发修改披露义务**。【官方】[^c6-30]

> 本文按用户决定**不展开**反向代理配置步骤、TLS 设置、全文检索 provider 对比、PGroonga 安装、对象存储与邮件配置。

---

### 6.7 遗留问题：尚未确定的事

以下是本篇**无法给出结论**的开放项，写作时一律按「未确定」标注，不得当作已知事实：

1. **当前版本容器的实际 UID/GID 未知**——唯一可查的数字是 v13 时代的 `991:991`，当前版本没有任何来源给出具体值，也不存在 `PUID`/`PGID` 式变量。【开放】
2. **v13 的卷权限缺陷是否已在后续版本修复、以何种方式修复，无可查来源**——当初的 issue 当日即关闭，未记录修复提交或版本。【开放】
3. **2GB 构建内存地板是否仍适用于 2026.7.0 之后的版本**未知——该数字出自更早的两处来源，都早于近期的 Node / Debian 大版本跃迁。【开放】
4. **2026.9.0 是否调整了 2026.7.0 的 SSE4.2 / Node 最低版本 / sensitive-detector 要求**，发布说明未重述，无从判断。【开放】
5. **不存在官方的「仅内网」指引**——无公网域名的部署方案没有一手来源可依。【开放】

---

### 小结

- 官方升级流程是 **`git stash` → `git checkout master` → `git pull` → `git submodule update --init` → `git stash pop` → `sudo docker compose build` → 停服 → 启动**；刻意 stash/pop 是为了保留本地配置改动。【官方】
- 升级路径**不重复初始化**、**没有显式迁移命令**，官方只提示「通常不需要额外步骤」；但**升级前必须先读 release notes / `CHANGELOG.md`**，耗时取决于更新内容与数据库规模。【官方】
- 上游更新流程末行两条命令**粘连成一行、照抄不可执行**，须拆为「停服」「启动」两步。【官方（缺陷）】
- 应用镜像是**本地构建**（`build: .`），不存在可供固定的官方发行镜像；`redis`/`postgres`/`meilisearch` 标签固定，注释中的 `mcaptcha` 浮动。【官方】
- 近期破坏性变更集中在 **2026.7.0**（基础镜像跃迁、Node 最低版本、SSE4.2、sensitive-detector 外置、YAML 解析更严格、客户端设置迁移）；**2026.9.0 是含 7 个 GHSA 的安全版本**，且未重述上一版的要求。【官方】
- 三类内容必须分清：【官方】有出处，【推断】三则无官方来源，【过时】两则（Node pin、Redis 密码条目）只能按历史读。【官方 / 推断 / 过时】

#### 结语：留两条线盯住

走到这里，你已经能把实例从零部署起来、也知道怎么安全地升级和维护它。但有两件事本篇给不出确定答案，建议你后续自行跟踪：

1. **`sensitive-detector` 的部署方式与资源占用**——本期只确认了「未配置则不检测」，它自己怎么部署、要吃多少资源，尚无一手资料。
2. **当前版本容器的实际 UID/GID，以及 v13 卷权限缺陷是否已在下游修复**——这直接决定 NAS 上 `./files`、`./db`、`./redis` 三个挂载目录应归谁所有。

盯住这两条，你的自建实例就能从「跑起来」稳稳走到「长期跑下去」。

---

## 参考来源

> 说明：六章正文的脚注定义统一汇总于此，按章节分组；正文中的 `[^cN-x]` 可到对应章节组检索。脚注 ID 带有章节前缀（`c1-` … `c6-`），跨章不会冲突。
>
> 下列定义中若出现 `S01`、`S10b` 这类简写代号，对应关系见下表：

| 代号 | 来源 |
| --- | --- |
| S01 | [Building Misskey using Docker Compose — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/) |
| S02 | [Installation resources 索引 — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/resources/) |
| S03 | [Nginx configuration — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/resources/nginx/) |
| S04 | [Troubleshooting Manual Installation — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/) |
| S05 | [Note search — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/features/search/) |
| S06 | [Detailed guide to installing Misskey on Ubuntu — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/) |
| S07 | [compose_example.yml — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml) |
| S08 | [.config/docker_example.yml — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml) |
| S09 | [.config/docker_example.env — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.env) |
| S10a | [Release 2026.9.0 — misskey-dev/misskey](https://github.com/misskey-dev/misskey/releases/tag/2026.9.0) |
| S10b | [Release 2026.7.0 — misskey-dev/misskey](https://github.com/misskey-dev/misskey/releases/tag/2026.7.0) |
| S11 | [Issue #9613 — misskey-dev/misskey](https://github.com/misskey-dev/misskey/issues/9613) |
| S12 | [Discussion #9254 Changing Instance Domain — misskey-dev/misskey](https://github.com/misskey-dev/misskey/discussions/9254) |

### 第一章来源

[^c1-1]: [Building Misskey using Docker Compose — Misskey Hub](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/)
[^c1-2]: [compose_example.yml — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml)
[^c1-3]: [.config/docker_example.env — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.env)

### 第二章来源

[^c2-1]: [compose_example.yml — misskey-dev/misskey](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml)
[^c2-2]: [Issue #9613 容器内已上传文件无法访问 — misskey-dev/misskey](https://github.com/misskey-dev/misskey/issues/9613)（2023-01-16 开、同日关闭）

### 第三章来源

[^c3-1]: [.config/docker_example.yml（Misskey 官方仓库示例配置文件）](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml)
[^c3-2]: [Building Misskey using Docker Compose（Misskey Hub 官方容器部署指南）](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/)
[^c3-3]: [Troubleshooting Manual Installation（Misskey Hub 官方排错页）](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/)
[^c3-4]: [Detailed guide to installing Misskey on Ubuntu（Misskey Hub 官方 Ubuntu 安装指南）](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/)
[^c3-5]: [Discussion #9254 Changing Instance Domain（Misskey 官方仓库讨论）](https://github.com/misskey-dev/misskey/discussions/9254)

### 第四章来源

[^c4-1]: Misskey 仓库示例文件 [.config/docker_example.env](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.env)。
[^c4-2]: 官方指南要求「编辑 `default.yml` 和 `docker.env`（as per the description）」：[Building Misskey using Docker Compose](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/)；`POSTGRES_PASSWORD` 即该文件中需替换的占位口令，见 S09。
[^c4-3]: Misskey 仓库示例文件 [.config/docker_example.yml](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml) 的 `db.user` / `db.pass`。
[^c4-4]: Misskey 仓库示例文件 [compose_example.yml](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml)。

### 第五章来源

[^c5-1]: [Building Misskey using Docker Compose](https://misskey-hub.net/en/docs/for-admin/install/guides/docker/)（缓存：`sources/S01_docker-guide.md`）
[^c5-2]: [Detailed guide to installing Misskey on Ubuntu](https://misskey-hub.net/en/docs/for-admin/install/guides/ubuntu-manual/)（缓存：`sources/S06_ubuntu-manual.md`）
[^c5-3]: [Troubleshooting Manual Installation](https://misskey-hub.net/en/docs/for-admin/install/resources/troubleshooting/)（页面标注 2018-10-07 撰写、2021-12-20 最后更新；缓存：`sources/S04_troubleshooting.md`）
[^c5-4]: [Release 2026.7.0](https://github.com/misskey-dev/misskey/releases/tag/2026.7.0)（缓存：`sources/S10b_release_2026.7.0.md`）
[^c5-5]: [compose_example.yml](https://github.com/misskey-dev/misskey/blob/master/compose_example.yml)（缓存：`sources/S07_compose_example.yml.md`）
[^c5-8]: [.config/docker_example.yml](https://github.com/misskey-dev/misskey/blob/master/.config/docker_example.yml)（缓存：`sources/S08_docker_example.yml.md`）
[^c5-9]: [Installation resources 索引](https://misskey-hub.net/en/docs/for-admin/install/resources/)（其中指向单独的 Scaling Misskey 文章；缓存：`sources/S02_install-resources.md`）

### 第六章来源

[^c6-1]: S01「Updating Misskey」：When updating, be sure to check the release notes and review any changes and whether additional steps are required (usually none) in advance.
[^c6-2]: S01「Updating Misskey」：流程含 `git stash` 与 `git stash pop`，用于保留本地配置改动。
[^c6-3]: S01「Updating Misskey」原文末行印作 `sudo docker compose stop sudo docker compose up -d`，两条命令粘连、无分隔符。
[^c6-4]: S01 更新流程中未出现 `pnpm run init`，初始化仅见于「Build & Initialize」一节。
[^c6-5]: S01 更新章节除「usually none」外，未给出任何显式数据库迁移命令。
[^c6-6]: S01「Updating Misskey」：It may take time depending on the update content and the size of the database.
[^c6-7]: S07 `compose_example.yml` 中 `redis:7-alpine`、`postgres:18-alpine`、`getmeili/meilisearch:v1.3.4`、`mcaptcha/mcaptcha:latest`、`mcaptcha/cache:latest`。
[^c6-8]: S07 `web` 服务使用 `build: .` 本地构建，非 registry 拉取。
[^c6-9]: S01 仅提供 `build: .` 本地构建路径，未给出 registry 预构建镜像与版本固定策略。
[^c6-10]: S02「How to push to Docker Hub using GitHub Actions」：示例见原仓库 `/.github/workflows/docker.yml`。
[^c6-11]: S10b（2026.7.0）、S10a（2026.9.0）发布说明。
[^c6-12]: S10b：Docker Image の Node.js を 26.4.0 に、Debian を trixie (v13) に更新。
[^c6-13]: S10b：最低動作バージョンを 22.22.2 / 24.17.0 / 26.4.0 に引き上げ；v22 は今後サポート終了予定。
[^c6-14]: S10b：SSE4.2 命令セットをサポートしていない x86_64 CPU では Misskey が正しく動作しなくなります；ARM64 など x86_64 ではない環境では影響なし。
[^c6-15]: S10b：センシティブメディアの判定が外部サービス sensitive-detector への HTTP 呼び出し方式に変更。
[^c6-16]: S10b：画像の正規化・動画フレームの抽出・しきい値判定・集約は引き続き本体側で実施。
[^c6-17]: S10b：接続先が未設定の場合、センシティブ判定は行われません (すべて非センシティブ扱い)。
[^c6-18]: S10b：YAML パーサーをアップデートし、より厳格なチェックが行われるように；起動時に config の読み取りで構文エラーが発生する可能性。
[^c6-19]: S10b：例えば `allowPrivateNetworks` を 2026.6.0 までの `example.yml` の構文を元に記述している場合は、配列の閉じ括弧のインデントを上げるか、リスト表示に書き換える必要があります。
[^c6-20]: S10b：2025.4.0 以前の設定情報の移行処理が削除；2025.4.0 から直接 2026.6.0 以上にアップデートする場合は設定が移行されません…移行したい場合は一度 2026.5.1 を経由してください。
[^c6-21]: S10a：今回のアップデートでは重大な脆弱性を修正しています。可及的速やかにアップデートしてください；含 7 个 GHSA 公告（GHSA-rrm8-pwmf-gxm3、GHSA-5c3q-jmv3-r6fx、GHSA-vwfw-pgg7-5hg6、GHSA-xc6c-m4f7-jcc9、GHSA-jx9q-24fh-4fxw、GHSA-h3mq-w9gq-6mwm、GHSA-g3ph-65m3-x625）。
[^c6-22]: S10a 全文未见对 2026.7.0 SSE4.2 / Node / sensitive-detector 要求的重述或修订。
[^c6-23]: S01 前提条件：Make sure Docker and Docker Compose are installed on your system（未给最低版本）。
[^c6-24]: S06 安装命令 `NODE_MAJOR=20`，同页验证文字称输出类似 `v22.x.x` 则安装成功——页面内部矛盾。
[^c6-25]: S04「Cannot connect to redis」：Misskey versions prior to 11.20.2 cannot resolve redis passwords（页面标注 2018-10-07 撰写、2021-12-20 最后更新）。
[^c6-26]: S02「Nginx configuration」：We recommend using nginx as a reverse proxy and operating the Misskey server without exposing it directly to the Internet.
[^c6-27]: S02「CDN Configuration」：We strongly recommend using a CDN such as Cloudflare when publishing your Misskey server.
[^c6-28]: S06「Check Router Settings」：If you are hosting on a home server, make sure your router allows inbound connections on ports 80 and 443.
[^c6-29]: S06「FFmpeg」：FFmpeg is used for processing video and audio；S04「ImageMagick related」：ImageMagick is not required!
[^c6-30]: S02「Notes on Forking and Customizing Misskey」：The GNU Affero General Public License v3.0 (AGPL-3.0), adopted by Misskey, mandates the disclosure of any modifications made to the Misskey source code.
