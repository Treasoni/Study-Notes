# 第六章：升级流程与 NAS 遗留约束

前五章把实例跑起来了：产物落位、编排文件、应用配置、数据库口令、构建初始化启动。但一个自建实例真正的寿命是从第二次升级开始的——Misskey 迭代很快，近期连续几个版本都带着会改变运行环境的破坏性变更。这一章解决两个问题：**照着官方流程安全地升级一次**，以及**在 NAS 这种非标准环境上，哪些结论有官方依据、哪些只是本文推断、哪些已经过时**。读完它，你应该能独立判断「这次升级我能不能直接上」。

> [!warning] 升级前的第一动作不是敲命令
> 官方在更新章节明确要求：**升级前务必先查阅 release notes / `CHANGELOG.md`，提前确认本次变更内容以及是否需要额外步骤（通常不需要）**。【官方】[^c6-1] 这句话不是客套——后文 6.4 列出的破坏性变更，全部只能从发布说明里读到，升级流程本身不会提示你。

---

## 6.1 官方升级流程，逐条拆解

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

### 6.1.1 文档缺陷：末行两条命令粘连

上面的拆解里第 7、8 步并不是官方原文的分行，而是**本文对一处上游文档缺陷的修正**。S01 更新流程的最后一行把两条命令粘在了一起，中间没有任何分隔符：

```text
# 来源：S01「Updating Misskey」原文末行（缺陷：两条命令粘连、无分隔符，照抄不可执行）
sudo docker compose stop sudo docker compose up -d
```

这行**不能照抄执行**——shell 会把 `stop` 后面的整串当成参数，而不是第二条命令。它实际想表达的是「停服」和「启动」两步。官方页面在这里丢失了一个换行，本文按两步呈现。【官方（缺陷）】[^c6-3]

> [!tip] 大白话
> 这就像说明书把「关电源」和「按启动键」两个按钮的图印嵌在一起，看起来像一个按钮。你要做的是把它们当两个动作分开执行，而不是去按那个不存在的合并按钮。

### 6.1.2 升级路径里没有什么

比「有什么」更重要的是「没有什么」，因为这直接决定你升级时**不需要**多做什么：

- 升级流程**没有**重复 `pnpm run init`。初始化只在首次部署时做过一次。【官方】[^c6-4]
- 除了一句「通常不需要额外步骤」，官方**没有给出任何显式的数据库迁移命令**。【官方】[^c6-5]

换句话说，照着上面 8 步走完，迁移是构建与启动过程内部完成的，不需要你手工触发。这也再次说明**为什么升级前必须读发布说明**：一旦某个版本真的需要额外步骤，官方只会写在 `CHANGELOG.md` 里，流程本身不会提醒。

**耗时预期**：升级耗时取决于**本次更新内容**与**数据库规模**。【官方】[^c6-6] 在 NAS 上，磁盘 I/O 偏慢会把这段时间进一步拉长。

---

## 6.2 镜像标签策略：哪些固定、哪些浮动

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

## 6.3 升级前必须自查的破坏性变更

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

### 6.3.1 运行环境基线跃迁（2026.7.0）

2026.7.0 把 Docker 镜像的 Node.js 升到 **26.4.0**、Debian 升到 **trixie (v13)**。【官方】[^c6-12] 同时把最低 Node.js 版本提高到 **22.22.2 / 24.17.0 / 26.4.0**：v24 与 v26 受支持，v22 仍能运行但**计划在未来版本移除支持**。【官方】[^c6-13]

对容器部署的你来说，这一条大多由镜像替你消化；但如果你曾经把 Misskey 装到裸机、或自己维护镜像，就必须先确认运行时的 Node 版本已达标。

### 6.3.2 CPU 指令集门槛（2026.7.0）

这是第五章讲过的硬件门槛，在这里换一个视角看：它是一条**「升级前必须确认」的版本级变更**。2026.7.0 起，**不支持 SSE4.2 指令集的 x86_64 CPU 将无法正确运行 Misskey**，成因是后端图像处理库 **sharp** 的系统要求变更；影响虚拟机与老旧硬件，**ARM64 等非 x86_64 环境不受影响**。【官方】[^c6-14]

对 NAS 用户尤其重要：老旧 Celeron / Atom 类 CPU 可能不满足，升级前应先在目标机上确认指令集。

### 6.3.3 敏感媒体检测外置（2026.7.0）

NSFW 判定从「本体内置 `nsfwjs` 推理」改为「对外部服务 `sensitive-detector` 的 HTTP 调用」。【官方】[^c6-15] 具体分工是：**图像的归一化、视频抽帧、阈值判定与聚合仍由 Misskey 本体完成**，只把「已归一化图像的推理」这一步委托给外部服务。【官方】[^c6-16]

关键后果：依赖敏感检测的实例需要**自行部署 `sensitive-detector`**，并在控制台「モデレーション > センシティブなメディアの検出」里填连接地址；**若连接地址未配置，则完全不进行判定，一切按非敏感处理**。【官方】[^c6-17]

> [!warning] 静默失效，不会报错
> 「未配置即不检测」意味着升级后你的实例不会崩、不会报错，只是**敏感媒体不会再被自动标记**。这是一个容易在升级后被忽略的功能缺口，升级后务必到控制台确认该地址是否已填。

### 6.3.4 配置解析更严格（2026.7.0）

YAML 解析器升级后校验更严格，**启动时读取 config 可能因语法错误而失败**。【官方】[^c6-18] 发布说明点名的例子是 `allowPrivateNetworks`：如果你沿用 2026.6.0 及更早的 `example.yml` 写法，就需要**把数组的闭括号缩进提高，或改写为 list 形式**。【官方】[^c6-19] 换言之，第三章那份「YAML 行首缩进写错会直接导致 Misskey 无法工作」的警告，在 2026.7.0 之后被解析器本身强化了。

### 6.3.5 客户端设置迁移（2026.7.0）

2026.7.0 **移除了从 2025.4.0 及更早版本迁移客户端设置的能力**：若你想从 2025.4.0 直接跳到 2026.6.0 以上，设置**不会**被迁移；想迁移必须**先经过一次 2026.5.1**。【官方】[^c6-20] 这条只影响「跨了很大版本跨度」的实例，长期跟着升级的用户不会遇到。

### 6.3.6 最新版本：2026.9.0 是安全版本

2026.9.0 是一个**安全版本，包含 7 个 GHSA 公告**，上游以醒目提示要求尽快升级到该版本或最新版。【官方】[^c6-21] 需要留意的是：**它没有重述或修订 2026.7.0 的那批要求变更**——也就是说，2026.7.0 的 SSE4.2、Node 最低版本、sensitive-detector 等要求，在 2026.9.0 的发布说明里既没被重申，也没被取消。【官方】[^c6-22]

---

## 6.4 【推断】三则：有本文结论、无官方来源

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

## 6.5 【过时】两则：只能按历史口径读

以下两条信息在官方页面上仍然存在，但**已经过时**，本章按历史信息呈现，正文不得据此操作。

### 6.5.1 安装指南里的 Node.js 版本 pin

S06（Ubuntu 手动安装指南）的安装命令把 Node 源 pin 在 **`NODE_MAJOR=20`**：

```bash
# S06 安装命令中的 Node 源（已过时，勿据此操作）
NODE_MAJOR=20; echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list;
```

但**同一页面**的验证文字却说：如果输出类似 **`v22.x.x`** 则安装成功。【过时】[^c6-24] 同一页面对 Node 版本自相矛盾，说明该段落已滞后。**处理原则：以发布说明为准**——即 6.3.1 给出的最低版本 **22.22.2 / 24.17.0 / 26.4.0**。【过时】

### 6.5.2 Redis 密码条目

排错页（S04）声称：**11.20.2 之前的版本无法解析 Redis 密码**，因此 Redis 必须不设密码、并把 `default.yml` 里 `redis:` 下的 `pass:` 行注释掉。【过时】[^c6-25] 该页面自身标注为「2018-10-07 撰写、2021-12-20 最后更新」，这条指引只对 11.20.2 之前的老版本成立，**已不适用于当前版本线**。【官方（页面日期）】

> [!warning] 不要把旧条目当现行最佳实践
> 你若在网上看到「Misskey 的 Redis 必须无密码」这类说法，源头多半就是这条 2021 年的旧条目。它描述的是 11.20.2 之前的限制，不是当前版本的配置建议。遇到历史信息与发布说明打架，**发布说明优先**。

---

## 6.6 相邻官方事实

以下几条有官方依据、值得知道，但都不构成需要你执行的配置步骤，各一句话带过：

- **反向代理**：官方建议用 **nginx** 作反向代理，并把 Misskey 运行在不直接暴露到公网的状态下。【官方】[^c6-26]
- **CDN**：对外发布时，官方**强烈建议使用 Cloudflare 等 CDN**。【官方】[^c6-27]
- **家用服务器的端口**：若在家用服务器上托管，需确认路由器允许 **80 与 443** 入站连接。【官方】[^c6-28]
- **FFmpeg 与 ImageMagick**：**FFmpeg 用于处理视频与音频、是需要的**；而 **ImageMagick 明确不需要**。【官方】[^c6-29]
- **AGPL-3.0 披露义务**：Misskey 采用 AGPL-3.0，**fork 或修改其源码会触发修改披露义务**。【官方】[^c6-30]

> 本文按用户决定**不展开**反向代理配置步骤、TLS 设置、全文检索 provider 对比、PGroonga 安装、对象存储与邮件配置。

---

## 6.7 遗留问题：尚未确定的事

以下是本篇**无法给出结论**的开放项，写作时一律按「未确定」标注，不得当作已知事实：

1. **当前版本容器的实际 UID/GID 未知**——唯一可查的数字是 v13 时代的 `991:991`，当前版本没有任何来源给出具体值，也不存在 `PUID`/`PGID` 式变量。【开放】
2. **v13 的卷权限缺陷是否已在后续版本修复、以何种方式修复，无可查来源**——当初的 issue 当日即关闭，未记录修复提交或版本。【开放】
3. **2GB 构建内存地板是否仍适用于 2026.7.0 之后的版本**未知——该数字出自更早的两处来源，都早于近期的 Node / Debian 大版本跃迁。【开放】
4. **2026.9.0 是否调整了 2026.7.0 的 SSE4.2 / Node 最低版本 / sensitive-detector 要求**，发布说明未重述，无从判断。【开放】
5. **不存在官方的「仅内网」指引**——无公网域名的部署方案没有一手来源可依。【开放】

---

## 小结

- 官方升级流程是 **`git stash` → `git checkout master` → `git pull` → `git submodule update --init` → `git stash pop` → `sudo docker compose build` → 停服 → 启动**；刻意 stash/pop 是为了保留本地配置改动。【官方】
- 升级路径**不重复初始化**、**没有显式迁移命令**，官方只提示「通常不需要额外步骤」；但**升级前必须先读 release notes / `CHANGELOG.md`**，耗时取决于更新内容与数据库规模。【官方】
- 上游更新流程末行两条命令**粘连成一行、照抄不可执行**，须拆为「停服」「启动」两步。【官方（缺陷）】
- 应用镜像是**本地构建**（`build: .`），不存在可供固定的官方发行镜像；`redis`/`postgres`/`meilisearch` 标签固定，注释中的 `mcaptcha` 浮动。【官方】
- 近期破坏性变更集中在 **2026.7.0**（基础镜像跃迁、Node 最低版本、SSE4.2、sensitive-detector 外置、YAML 解析更严格、客户端设置迁移）；**2026.9.0 是含 7 个 GHSA 的安全版本**，且未重述上一版的要求。【官方】
- 三类内容必须分清：【官方】有出处，【推断】三则无官方来源，【过时】两则（Node pin、Redis 密码条目）只能按历史读。【官方 / 推断 / 过时】

### 结语：留两条线盯住

走到这里，你已经能把实例从零部署起来、也知道怎么安全地升级和维护它。但有两件事本篇给不出确定答案，建议你后续自行跟踪：

1. **`sensitive-detector` 的部署方式与资源占用**——本期只确认了「未配置则不检测」，它自己怎么部署、要吃多少资源，尚无一手资料。
2. **当前版本容器的实际 UID/GID，以及 v13 卷权限缺陷是否已在下游修复**——这直接决定 NAS 上 `./files`、`./db`、`./redis` 三个挂载目录应归谁所有。

盯住这两条，你的自建实例就能从「跑起来」稳稳走到「长期跑下去」。

---

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
