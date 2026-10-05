# 小雅 fnOS 单容器部署（合并件）

> 本文件是 7 章单容器部署笔记的**单文件合并版**，供一次性通读；正式发布为拆分多文件（见同目录各章）。


---

# 第 1 章 开篇定位——小雅是什么，这篇要解决什么问题

## 本章要解决的问题

一句话看懂：**小雅是一套「片子留在网盘、点开就能看」的影视资源库**。它不把电影下载到你本地硬盘，而是把一份持续更新的网盘影视目录聚合成一个可访问的服务，让你直接在线播放，或者像挂载文件夹一样挂进播放器（WebDAV）。围绕它，你最关心的两个问题本篇都会给出明确答案：**选型上，不必须用 Emby**——飞牛自带的「飞牛影视」可以充当播放端；**部署上，单容器（只装资源层、不装 Emby）就能跑通**。

本章不带你动手，只做一件事：把「小雅、AList、Emby、飞牛影视、STRM、302 直链、WebDAV、转存」这几个词分别是谁、彼此什么关系摆清楚，再告诉你这篇后面几章各自负责什么。

## 1.1 小雅是什么：它是「资源层」，不是「播放器」

先把「小雅」这个词落地。它对外给人的东西，是一份别人替你维护好的网盘影视目录。技术笔记站对新手的概括是：

> 「小雅 Alist 是基于阿里云盘的影视聚合方案，维护着一份持续更新的影音资源目录，省去了自己找片、管片的麻烦。」（`sources/p2/newzone-xiaoya.md:10`）

拆开这句看两层意思：**资源在哪**——在阿里云盘上，由维护者持续更新，你不用自己找片；**你怎么拿到**——通过一个叫 AList 的程序把它变成一个能访问的服务。小雅官方镜像的作者自述也印证了这一点：

> 「我把 alist.xiaoya.pro 的内容，内嵌在容器里发布了，并添加了 alist 本身没有的搜索功能。」（`sources/01_hub_docker_com.md:10`）

所以「小雅」不是一个播放器，它更像一个**片源仓库**：它负责「有什么片、片在哪」，至于海报墙怎么排、点了之后怎么播，是另一层的事。这一层由 AList 承担——`Alist: 提供资源在线播放，WebDav服务`（`sources/p2/monlor-144.md:88`）。

> [!tip] 大白话
> 把「资源层」想成**仓库**：仓库里堆满了别人的片子，你去仓库能拿到货（播放链接）。但仓库本身不负责「放映」——它不排片单、不做海报墙、不放电影。所以「小雅」两个字，指的是仓库，不是放映厅。

## 1.2 你的两个问题，先给简答

本篇是从你提出的两个问题长出来的，这里先各给一句结论，细节分别落在第 2 章和第 3–5 章。

**问题一（选型）：不想用 Emby，直接用飞牛影视行不行？**
结论：**行，不必须 Emby**。在我们检索到的所有来源里，**没有任何一处**断言「小雅必须配 Emby」；而且已经有社区实践走的是「全家桶去掉 Emby」——发帖者原话是：「部署 小雅的全家桶 除了emby，用刮削好的 strm文件，完美适配」（`sources/forum/tid-73955.md:32`）。也就是说，飞牛影视当播放端这条路，既有官方工具的旁证，也有真实用户在跑。第 2 章会把「能不能替代」拆成四个维度逐项对比。

**问题二（部署）：单容器方案具体怎么部署？**
结论：**只装资源层（仅 AList）就是单容器**，官方安装脚本把「只装小雅 Alist」和「装 Emby 全家桶」列成了两个不同的菜单项（`sources/01_raw_githubusercontent_com.md:75-76`），说明「只装 Alist」是官方承认的独立装法。具体命令集中在第 4 章，第 3 章先备清单。

## 1.3 先立一个比喻：资源层是仓库，播放层是电视

要理解「为什么可以不用 Emby」，得先把这套系统分成两层。这个分层是理解全篇的钥匙：

| 层 | 谁承担 | 决定什么 | 具体产物 |
| --- | --- | --- | --- |
| **资源层** | 小雅（以 AList 为载体） | 「有什么片」 | 一份持续更新的网盘影视目录 + 在线播放 + WebDAV 挂载 |
| **播放层** | 飞牛影视 / Emby / Jellyfin | 「怎么看」 | 海报墙、元数据刮削、播放器、外网访问入口 |

两层的分工，用官方的组件描述能看得更清楚。AList 那层是「提供资源在线播放，WebDav服务」（`sources/p2/monlor-144.md:88`）；而 Emby 那层是「用家庭影视库的方式，可视化展示 Alist 中的资源」（`sources/p2/monlor-144.md:90`）——一个管资源、一个管展示。

**这个分层解释了你最关心的问题：** 既然「怎么看」是一层，而播放层不是只有 Emby 一家（飞牛影视、Jellyfin 干的是同一类事），那么「不想用 Emby」就是**换一个播放层**，而不是放弃整个方案——仓库照旧，只换电视。

> [!tip] 大白话
> 把资源层想成**仓库**、播放层想成**电视**：仓库决定「有什么片」，电视决定「怎么看」（有没有海报墙、能不能刮削出简介、外网点开卡不卡）。你不想用 Emby，本质是「换台电视」，不是「不要仓库」。仓库和小雅没关系的那部分——片源在网盘上——一点都没变。

这套「资源在网盘、不落本地」的取舍，我在同域笔记 [[流媒体与影音/网盘影视播放与本地存储的取舍]] 里展开过，想先补背景的读者可以先读那篇；本章只需要记住：**小雅解决的是「片源从哪来」，不解决「怎么放」。**

## 1.4 名词扫盲表

后面几章会反复出现下面这些词，第一次见就到这张表里查一眼：

| 名词 | 一句话大白话 | 在本篇里的角色 |
| --- | --- | --- |
| **小雅** | 一套基于阿里云盘的影视聚合方案，维护着持续更新的资源目录 | 本篇的「资源层」主体 |
| **AList** | 一个把多种网盘聚成一个文件列表、并提供网页和 WebDAV 访问的程序 | 小雅的载体，单容器部署的主角 |
| **Emby** | 商业的家庭媒体服务器 / 影视库（海报墙、刮削、播放） | 「播放层」的一种，本篇要对比的对象 |
| **飞牛影视** | fnOS 自带的影视库 / 播放端，角色类似 Emby | 「播放层」的另一种，本篇的替代方案 |
| **STRM** | 一个只存 URL 指针的文本文件，本身不含视频（像「快捷方式」） | 把网盘片源接进播放层的桥 |
| **302 直链** | HTTP 重定向：播放器拿到真实直链后直接去下载，流量**不经过**媒体服务器 | 播放链路的关键一环，决定外网能不能看 |
| **WebDAV** | 一种协议，让播放器/电脑像挂目录一样访问网盘里的文件 | 资源层对外暴露的第二种取用方式 |
| **转存** | 把网盘上的片源临时「复制」一份到你自己的网盘目录，以换取可播放的直链 | 会占用你网盘空间，需定期清理 |

其中 **STRM**（`strm 只是 URL 指针`，`sources/lens-b/fntvproxy/01_github_com.md:266`）和 **302 直链**（`Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器`，`sources/lens-b/mediawarp/01_github_com.md:53`）这两个概念是主线，第 5 章会专门讲。想更早看懂它们的原理，可以先读同域笔记 [[流媒体与影音/Strm流文件与302播放详解]]。

> [!tip] 大白话
> **转存**像「借片」：仓库里的片你直接看会卡，于是先把它「暂借」一份到自己网盘再放，看完要还（清理）——否则自己网盘会被借来的片子塞满。**302 直链**像「转介绍」：播放器问一句「片在哪」，服务器答「在 A 处」，播放器就直接去 A 处拿，**不绕回**服务器中转，所以省带宽、更流畅。

## 1.5 「纯净版」是什么：一处必须澄清的叫法

本篇标题里的「纯净版」，**不是官方术语**。在我们核对过的官方来源（官方镜像页、官方脚本仓库）里，**都没有出现过「纯净版」这个词**。它在社区里约定俗成地指「只装小雅 Alist、不装 Emby 全家桶」的那套轻量装法，官方语义上对应的是安装脚本菜单里的这一项：

> 「安装 小雅Alist -> 1 1」（`sources/01_raw_githubusercontent_com.md:75`）

而它旁边紧挨着的另一项就是「安装 Emby全家桶（一键） -> 2 1」（`sources/01_raw_githubusercontent_com.md:76`）——两个是**不同的菜单项**，这正是「只装 AList 是官方承认的独立装法」的依据。

> [!warning] 别把「纯净版」当成官方产品名
> 「纯净版」是**社区叫法，非官方术语**。你去搜索时，官方文档里对应的是「安装 小雅Alist」这一菜单项，或直接运行官方镜像 `xiaoyaliu/alist`。记住这一点，可以避免把社区黑话当成官方说法去问、去找，结果找不到。

## 1.6 这篇怎么读：全文路线图

全篇 7 章，顺序是「先判断、再动手、后收口」，你可以按需跳读：

| 章节 | 类型 | 你要做的事 | 大概耗时 |
| --- | --- | --- | --- |
| **第 1–2 章** | 判断 | 决定要不要用 Emby、最终选哪条路线 | 约 30 分钟 |
| **第 3–5 章** | 动手 | 备清单 → 单容器部署 → 飞牛影视接入 | 约 30–60 分钟 |
| **第 6–7 章** | 收口 | 遇到问题回查避坑清单；做长期运维（清理转存缓存） | 约 20 分钟 |

如果你只是想「先把部署跑通」，核心路径是**第 3 → 4 → 5 章**；第 1、2 章是给还在犹豫「到底要不要 Emby」的读者判断用的。命令与解释是分开的：每章的解释走正文，完整的命令片段集中在各章的「动手实践」小节，不熟悉命令的读者可以先跳过命令、只读解释。

## 本章小结

- **小雅 = 资源层（仓库），不是播放器**：它把阿里云盘上持续更新的影视目录聚合成可访问的服务，负责「有什么片」，不负责「怎么看」。
- **你不必用 Emby**：所有来源里没有任何一处断言「必须 Emby」，且已有「全家桶去掉 Emby」的真实社区实践。
- **单容器 = 只装资源层**：官方脚本把「安装 小雅Alist」与「安装 Emby全家桶（一键）」列为不同菜单项，只装 Alist 是官方承认的装法。
- **分层是理解全篇的钥匙**：资源层（小雅/AList）× 播放层（飞牛影视/Emby），换播放端不影响片源，所以「不想用 Emby」是换电视、不是丢仓库。
- **「纯净版」是社区叫法、非官方术语**，官方语义约等于菜单里的「安装 小雅Alist」。

**下一章预告**：既然「不必须 Emby」，那飞牛影视到底靠不靠谱？第 2 章把两种方案在**刮削与元数据、播放链路、播放兼容性、外网可达性**四个维度上逐项摊开对比，并补一张「单容器 vs 全家桶」的资源门槛表，最后落到适合你这种「已有飞牛影视、不想装 Emby」场景的选型建议。

## 引文对照（原文 / 中译）

> 本章引用的逐字原文与说人话对照如下。本章的原始来源以中文为主，故「中译」列对中文原文给的是**说人话**的复述；出现英文片段时给出中译。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `小雅 Alist 是基于阿里云盘的影视聚合方案，维护着一份持续更新的影音资源目录，省去了自己找片、管片的麻烦。` | 小雅是一套基于阿里云盘的影视聚合方案，帮你不自己找片 | `sources/p2/newzone-xiaoya.md:10` |
| 2 | `我把 alist.xiaoya.pro 的内容，内嵌在容器里发布了，并添加了alist本身没有的搜索功能。` | 官方镜像作者把 alist.xiaoya.pro 的内容内嵌进容器，并加了搜索 | `sources/01_hub_docker_com.md:10` |
| 3 | `Alist: 提供资源在线播放，WebDav服务` | Alist 负责资源在线播放与 WebDAV | `sources/p2/monlor-144.md:88` |
| 4 | `Emby: 用家庭影视库的方式，可视化展示Alist中的资源` | Emby 用家庭影视库的方式把 Alist 的资源可视化 | `sources/p2/monlor-144.md:90` |
| 5 | `部署 小雅的全家桶 除了emby` | 装了全家桶但把 Emby 去掉 | `sources/forum/tid-73955.md:32` |
| 6 | `安装 小雅Alist -> 1 1` | 安装脚本里「只装小雅 Alist」这一项 | `sources/01_raw_githubusercontent_com.md:75` |
| 7 | `安装 Emby全家桶（一键） -> 2 1` | 安装脚本里「装 Emby 全家桶」这一项 | `sources/01_raw_githubusercontent_com.md:76` |
| 8 | `strm 只是 URL 指针` | STRM 文件只存一个 URL 指针，本身不是视频 | `sources/lens-b/fntvproxy/01_github_com.md:266` |
| 9 | `Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器` | STRM 能实现 302 直链播放，流量不经过媒体服务器 | `sources/lens-b/mediawarp/01_github_com.md:53` |

---

# 第 2 章 选型对比——飞牛影视能不能替代 Emby

## 本章要解决的问题

结论先行：**不必须用 Emby**。我们检索到的全部来源里，**没有任何一处**断言「小雅必须配 Emby」；相反，已经有人实打实地跑着「全家桶去掉 Emby」的方案。但这不等于两者没差别——本章会把两种播放端在**刮削与元数据、播放链路、播放兼容性、外网可达性**四个维度上逐项摊开，再补一张「单容器 vs 全家桶」的资源门槛对比，最后落到适合你的选型建议。

本章的对比对象只有两个：**路线 E**（Emby 全家桶：AList + 元数据服务 + Emby）和**路线 F**（单容器：仅 AList + 飞牛影视作前端）。读完你应该能自己回答：我这台机器、我这些片源习惯，到底该走哪条。

## 2.1 结论先行：没有任何来源说「必须 Emby」

先把最大的疑虑打消。社区里已经有明确走「不用 Emby」这条路的帖子，发帖者原话是：

> 「我把 xiaoyaemby 刮削好的 strm 文件放到飞牛影音里，这样既不占用 nas 空间，也不用科学版本的 emby，搜索更友好，使用起来更舒适……部署 小雅的全家桶 除了emby，用刮削好的 strm文件，完美适配」（`sources/forum/tid-73955.md:32`）

这位用户的做法有三点值得注意：他把「Emby 刮削好的 STRM」直接喂给**飞牛影音**（fnOS 的影视应用）；他明确「不用 Emby」；他评价「完美适配」。这至少说明：飞牛影视作为播放端，**不是不能替代 Emby**。

至于「能不能全量替代、有没有短板」，就是下面四个维度要回答的事。

## 2.2 两条路线分别是什么

对比之前，先把两条路线的组成摆出来。

**路线 E（Emby 全家桶）**，官方脚本的菜单项叫「安装 Emby全家桶（一键）」（`sources/01_raw_githubusercontent_com.md:76`）。它的组成部分，维护者的项目简介说得很清楚——「使用 Docker Compose 以更优雅的方式来部署小雅服务，支持一键部署 Alist + Emby + Jellyfin，全平台支持，Linux/Windows/Mac/群晖，X86/Arm架构」（`sources/p2/monlor-144.md:14`）。各组件分工是：

- `Alist: 提供资源在线播放，WebDav服务`（`sources/p2/monlor-144.md:88`）
- `Metadata: Emby和Jellyfin的元数据管理`（`sources/p2/monlor-144.md:89`）
- `Emby: 用家庭影视库的方式，可视化展示Alist中的资源`（`sources/p2/monlor-144.md:90`）

**路线 F（单容器 + 飞牛影视）**，就是只装资源层（AList）那一项——官方脚本的菜单项叫「安装 小雅Alist -> 1 1」（`sources/01_raw_githubusercontent_com.md:75`），播放/刮削交给 fnOS 自带的飞牛影视。

两条路线的差别可以一句话记住：**E 是「资源层 + 自带播放层 + 自带元数据服务」的全家桶；F 是「只装资源层，播放层用你已有的飞牛影视」。**

> [!tip] 大白话
> 把两条路线想成**买整机 vs 自己配一台**：路线 E 是厂商配好的「主机 + 显示器 + 音响」套装，插电即用，但占地方、贵；路线 F 是「只要你已有的显示器和音响，再自己接一个机顶盒」。你的机器上**本来就有飞牛影视**（相当于已有显示器），所以路线 F 才是「不浪费已有东西」的那种。



## 2.3 四个维度逐项对比

先给总表，再逐项展开差异与依据：

| 维度 | 路线 E（Emby 全家桶） | 路线 F（单容器 + 飞牛影视） |
| --- | --- | --- |
| **刮削与元数据来源** | 配套 `Metadata` 服务管理元数据；官方脚本还提供整套现成元数据包下载 | 让飞牛影视自己刮，或复用 Emby 侧刮好的 STRM |
| **播放链路** | 播放层与 AList 同栈部署，Emby 代理走 `:8095` | 需把播放地址指向飞牛代理端口 `:28005` |
| **播放兼容性** | 成熟播放器生态；脚本明确「没有计划支持硬解」 | 支持 `stream.mp4`/`stream.MOV` 等；网盘转码支持仍是待办 |
| **外网 / 蜂窝网可达性** | 同样要解决内网直链问题（代理改 302） | 关键坑同左：飞牛原生响应里的直链仍是内网地址 |

### 2.3.1 刮削与元数据来源

路线 E 的元数据是「配套供给」的：全家桶里有独立的元数据服务——`Metadata: Emby和Jellyfin的元数据管理`（`sources/p2/monlor-144.md:89`）；官方脚本里更是列了一长串「下载并解压 全部元数据」「解压 115.mp4 的指定元数据目录」「单独 下载 json.mp4」之类的手动元数据项（`sources/01_raw_githubusercontent_com.md:90-107`）。也就是说，Emby 路线有一套**现成的元数据宝库**，装完就有海报墙。

路线 F 的元数据来源则有两种做法，都来自那位「不用 Emby」的用户：一是把已经用 Emby 刮好的 STRM 直接搬进飞牛影视（「我把 xiaoyaemby 刮削好的 strm 文件放到飞牛影音里」），二是让飞牛影视自己按需刮削（「想刮削那个就刮削那个」）（`sources/forum/tid-73955.md:32`）。

**差异落点**：Emby 路线胜在「开箱有元数据包」；飞牛影视路线要自己解决刮削来源——要么复用 Emby 的刮削产物，要么靠飞牛影视自己刮。这是两条路线**最实际的差别**，但它不是「能不能用」的问题，而是「元数据从哪来」的问题。

### 2.3.2 播放链路

两条路线在底层其实共用同一套机制：**STRM + 302 直链**——`Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器`（`sources/lens-b/mediawarp/01_github_com.md:53`）。STRM 本身只是个 URL 指针（`strm 只是 URL 指针`，`sources/lens-b/fntvproxy/01_github_com.md:266`），真正决定能不能播的是那一步 302 重定向。

差别在**谁来扮演那个代理端口**：Emby 路线的代理默认走 Emby 端口；飞牛影视路线则不同，客户端要连的是飞牛这一侧的入口——`将播放器地址指向代理端口（飞牛 :28005，Emby :8095）`（`sources/lens-b/fntvproxy/01_github_com.md:71`）。

这条链路的具体原理（STRM 怎么生成、302 怎么改）是第 5 章的主线，想先深入可读同域笔记 [[流媒体与影音/Strm流文件与302播放详解]]。

### 2.3.3 播放兼容性

飞牛影视作为播放端，第三方工具的实测给它提供了旁证：代理工具明确「基于**飞牛影视 0.9.3** 版本」（`sources/lens-b/fntvproxy/01_github_com.md:45`），并在问答里说明「飞牛代理支持 `stream.mp4`、`stream.MOV` 等所有格式」（`sources/lens-b/fntvproxy/01_github_com.md:281`）。

但有一处要如实说明：**硬件解码/转码不在全家桶脚本的规划里**。维护者直言「脚本没有计划支持硬解，在我看来这个功能没有必要」（`sources/p2/monlor-144.md:58`）；而飞牛影视侧的「网盘转码」支持，在中间件的待办清单里还挂着一项「支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）」（`sources/lens-b/mediawarp/01_github_com.md:87`）——**待办 = 还没完成**，不能当成已有能力。

硬解与软解的取舍另有专文，延伸阅读见 [[流媒体与影音/硬件解码vs软件解码]]。

### 2.3.4 外网 / 蜂窝网可达性

这是两条路线**共同的坑**，也是最容易让「局域网能放、出门就播不动」的地方。帖子里记录得很直白：

> 「飞牛服务端通过原 STRM 能探测、读取片段，但飞牛原生 /stream 响应里的直链仍是内网地址（`xiaoya.host:5678`）。手机在蜂窝网络上无法使用 NAS 内部域名」（`sources/forum/tid-73955.md:42`）

也就是说，**原生飞牛影视对 302 直链 / 内网地址的处理不完善**，出门用手机看会卡在「解析不了内网域名」这一步。解法是加一层代理把内网地址改掉/转发——第 5 章会给具体做法（MediaWarp 或 fntv-proxy 二选一）。这一点对**两条路线同样成立**，不构成 Emby 与飞牛影视的优劣差，而是「有没有修 302」的差。

> [!tip] 大白话
> 把「内网地址」想成**家里的门牌号**：在家（局域网）路熟，门牌 `xiaoya.host:5678` 找得到；一出小区、上了蜂窝网，这个「只在小区的门牌」就没人认得了。要出门也能找到，就得在小区门口立一块公共指示牌（代理），把「小区门牌」换成「公网可达的地址」。这块牌子不是 Emby 或飞牛影视特有的，**谁都需要**。



## 2.4 单容器 vs 全家桶：为什么可以不用 Emby（资源门槛）

除了功能，还有一个很硬的选型因素：**机器扛不扛得住**。维护者给了一张部署配置推荐表（`sources/p2/monlor-144.md:74-80`）：

| 部署方案 | CPU | 内存 | 硬盘 |
| --- | --- | --- | --- |
| **仅部署 Alist** | 1 核 | 512M | 512M |
| **Alist + Emby** | 2 核 | 4G | 150G |
| **Alist + Emby + Jellyfin** | 2 核 | 4G | 200G |
| **Alist + Jellyfin** | 2 核 | 4G | 150G |

看数字就很清楚：**仅 AList 只要 1 核 / 512M / 512M；一旦加上 Emby，内存从 512M 跳到 4G、硬盘从 512M 跳到 150G**——差了一个数量级。

> [!warning] 这张表是「维护者推荐」，不是官方硬性要求
> 这张资源表出自 monlor 的项目博客（维护者推荐），**不是官方硬性指标**，也未在官方仓库出现。实际能跑多少负载取决于片源数量、并发人数等，请把它当参考量级，不要当验收标准。

**这张表是「为什么可以不用 Emby」最直接的反衬**：你说不想用 Emby，除了功能偏好，往往还因为**不想为播放层付出 4G 内存 + 150G 硬盘的代价**——而单容器（仅 AList）恰好把这个代价压到了 1 核 / 512M / 512M。

## 2.5 飞牛影视可作前端的旁证，与一处必须并列保留的未决

**正面旁证**（说明飞牛影视确实被当成正经播放端对待）：

- MediaWarp 的自我定位是「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」（`sources/lens-b/mediawarp/01_github_com.md:51`）——把飞牛影视和 Emby、Jellyfin 并列在同一位；
- fntv-proxy 直接「基于飞牛影视 0.9.3 版本」开发（`sources/lens-b/fntvproxy/01_github_com.md:45`）。

**但有一处必须并列保留、不合并、不下结论的**：同一个 MediaWarp 仓库，README 正文虽已把飞牛影视列为可代理对象，**它的待办清单（TODO LIST）里却仍挂着一项**——「适配 飞牛影视」（`sources/lens-b/mediawarp/01_github_com.md:86`）。

> [!warning] 一处未决：别把「已列出」读成「已完善」
> MediaWarp 对飞牛影视的**成熟度是未决的**：正文把它列为可代理对象，TODO 又仍列「适配 飞牛影视」。证据相互矛盾，本笔记**不合并、不裁断**——只能说「飞牛影视已被主流中间件纳入支持方向」，**不能说它已被完整适配**。实际以你部署时的实测为准。

## 2.6 Jellyfin 路线：官方安装方案已长久未维护

如果你考虑的是「全家桶里加 Jellyfin」，这里有一条明确的官方提示：

> 「注意：目前官方 Jellyfin 安装方案已经长久未维护！」（`sources/01_raw_githubusercontent_com.md:180`）

所以「加 Jellyfin」不建议走官方脚本（官方在该提示下方另指了一个第三方脚本，并注明「风险自担」）。这条信息对选型的影响是：**别把 Jellyfin 当默认选项**，除非你愿意走非官方路径。

## 2.7 选型建议：落到你的场景

把上面几条收敛成建议——你的场景是「已有飞牛影视 + 不想装 Emby」：

1. **首选路线 F：单容器（仅 AList）+ 飞牛影视作前端。** 理由：无来源要求 Emby；资源门槛低一个数量级（1 核 / 512M / 512M，`sources/p2/monlor-144.md:78`）；且飞牛影视已被主流中间件纳入支持方向。
2. **元数据提前想清楚。** 路线 F 没有现成元数据包：要么复用你已有的 Emby 刮削产物，要么接受飞牛影视按需刮削（`sources/forum/tid-73955.md:32`）。
3. **无论走哪条，都要修 302。** 外网/蜂窝网的坑和选型无关（`sources/forum/tid-73955.md:42`），第 5 章统一处理。
4. **若你确实想要「开箱即用的元数据宝库 + 成熟播放器生态」，再考虑路线 E**，并接受 4G 内存 / 150G 硬盘的门槛；但**不要**顺手把 Jellyfin 也加上——官方方案已弃维护（`sources/01_raw_githubusercontent_com.md:180`）。

一句话总括：**「能不能不用 Emby」——能；「要不要用 Emby」——取决于你愿不愿意用元数据来源和资源开销去换一个开箱即用的影视库。**

## 本章小结

- **不必须 Emby**：全部来源无一处断言「必须」，已有社区实践走「全家桶去掉 Emby」，把 Emby 刮削的 STRM 喂给飞牛影视。
- **四维差异**：刮削元数据（E 有现成元数据包 / F 要自备来源）、播放链路（共用 STRM + 302，只是代理端口不同）、播放兼容性（飞牛侧网盘转码仍是待办）、外网可达性（**两条路线共同的坑**）。
- **资源门槛差一个数量级**：仅 AList 1 核 / 512M / 512M，加 Emby 跳到 2 核 / 4G / 150G（维护者推荐、非官方硬性）。
- **旁证与未决并列**：MediaWarp / fntv-proxy 都把飞牛影视当正经播放端，但 MediaWarp 的 TODO 仍列「适配 飞牛影视」——**成熟度未决，不下结论**。
- **Jellyfin 官方安装方案已长久未维护**，不建议走官方脚本加装。

**下一章预告**：判断做完，接下来该动手了。但在敲命令之前，第 3 章先把三张清单备好——**目录（哪些路径映射进容器）、端口（容器内端口和宿主映射要分开看）、凭据（阿里云盘三件套 + WebDAV 账号）**，并顺带确认 fnOS 在官方兼容性表里的状态。

## 引文对照（原文 / 中译）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译」列对中文原文给的是**说人话**的复述；含英文术语的片段保留英文原名。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `我把xiaoyaemby刮削好的strm文件放到飞牛影音里` | 把 Emby 刮好的 STRM 文件搬进飞牛影视用 | `sources/forum/tid-73955.md:32` |
| 2 | `部署 小雅的全家桶 除了emby` | 装了全家桶但把 Emby 去掉 | `sources/forum/tid-73955.md:32` |
| 3 | `安装 Emby全家桶（一键） -> 2 1` | 安装脚本里「装 Emby 全家桶」这一项 | `sources/01_raw_githubusercontent_com.md:76` |
| 4 | `使用 Docker Compose 以更优雅的方式来部署小雅服务，支持一键部署 Alist + Emby + Jellyfin，全平台支持，Linux/Windows/Mac/群晖，X86/Arm架构` | 用 Docker Compose 一键部署 Alist/Emby/Jellyfin 全家桶，全平台支持 | `sources/p2/monlor-144.md:14` |
| 5 | `Alist: 提供资源在线播放，WebDav服务` | Alist 负责资源在线播放与 WebDAV | `sources/p2/monlor-144.md:88` |
| 6 | `Metadata: Emby和Jellyfin的元数据管理` | Metadata 服务管 Emby 与 Jellyfin 的元数据 | `sources/p2/monlor-144.md:89` |
| 7 | `Emby: 用家庭影视库的方式，可视化展示Alist中的资源` | Emby 用家庭影视库的方式把 Alist 的资源可视化 | `sources/p2/monlor-144.md:90` |
| 8 | `Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器` | STRM 能实现 302 直链播放，流量不经过媒体服务器 | `sources/lens-b/mediawarp/01_github_com.md:53` |
| 9 | `strm 只是 URL 指针` | STRM 文件只存一个 URL 指针，本身不是视频 | `sources/lens-b/fntvproxy/01_github_com.md:266` |
| 10 | `将播放器地址指向代理端口（飞牛 :28005，Emby :8095）` | 把播放器指到代理端口：飞牛用 28005、Emby 用 8095 | `sources/lens-b/fntvproxy/01_github_com.md:71` |
| 11 | `基于飞牛影视 0.9.3 版本` | 这个代理工具是针对飞牛影视 0.9.3 版本做的 | `sources/lens-b/fntvproxy/01_github_com.md:45` |
| 12 | `前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器` | 一个架在 Emby/Jellyfin/飞牛影视前面的反向代理 | `sources/lens-b/mediawarp/01_github_com.md:51` |
| 13 | `适配 飞牛影视` | （待办清单里的一项）适配飞牛影视 | `sources/lens-b/mediawarp/01_github_com.md:86` |
| 14 | `注意：目前官方 Jellyfin 安装方案已经长久未维护！` | 官方 Jellyfin 安装方案已经很久没人维护了 | `sources/01_raw_githubusercontent_com.md:180` |
| 15 | `仅部署 Alist` | （资源表里的）「只部署 Alist」一行：1 核 / 512M / 512M | `sources/p2/monlor-144.md:78` |
| 16 | `脚本没有计划支持硬解，在我看来这个功能没有必要` | 全家桶脚本没打算支持硬解，维护者认为没必要 | `sources/p2/monlor-144.md:58` |

---

# 第 3 章 动手前准备——目录、端口与凭据（新手可跳过）

## 本章要解决的问题

动手部署之前，其实只需要备好**三张清单**：**目录**（哪些路径要映射进容器）、**端口**（容器内用什么端口、宿主机映射成什么端口）、**凭据**（阿里云盘三件套 + WebDAV 账号）。本章只准备清单，**不执行任何部署**——命令集中在下一章。标题里的「新手可跳过」指的是本章末尾那段配置片段，如果你只想先看懂结构，读三张清单即可，片段留到下一章照着用。

先说一条贯穿全章的纪律：**「容器内」和「宿主机」是两套端口，绝不能混写**；同样，「官方镜像」和「monlor 镜像」是两条路线，镜像名也不能混写。下面逐张清单来。

## 3.1 目录：哪些路径要映射进容器

先看落地后的目录长什么样。小雅容器需要一块**持久化目录**来存数据，社区实操把它映射到容器内的 `/data`：

```text
# 宿主机（示例路径，来自飞牛论坛实操）
/vol2/1000/docker2/xiaoya/data        ← 你自建的文件夹
        │  （映射）
        ▼
# 容器内
/data                                 ← AList 持久化数据目录
├── docker_address.txt                ← 记录自身访问地址（社区帖反复出现）
└── ...
```

对应到 compose 配置里，那行注释说得最明白：

> 「将容器中的 /data 目录映射到名为 xiaoya 的数据卷，用于持久化存储」（`sources/forum/tid-9690.md:38`）

除了 `/data`，全家桶路线里还有一路把配置挂到容器内的 `/etc/xiaoya`（元数据容器用，`sources/p2/monlor-144.md:182`）。两条挂载的用途：

| 容器内挂载点 | 用途 | 谁在用 | 出处 |
| --- | --- | --- | --- |
| `/data` | AList 持久化数据（含 `docker_address.txt` 等） | alist 容器 | `sources/forum/tid-9690.md:38` |
| `/etc/xiaoya` | 配置 / 凭据 / 元数据文件目录 | metadata 容器 | `sources/p2/monlor-144.md:182` |

> [!note] 凭据文件的**文件名**已坐实，「放哪」看路线
> 三份凭据文件的**文件名**现有多来源支撑：`mytoken.txt` 见官方仓库（`sources/01_github_com.md:65`），三件套对照见两份社区教程（`sources/p3/z-addone/01_www_cnblogs_com.md:23-25`、`sources/p3/gnz48/01_www_cnblogs_com.md:25`）。但**放进哪个目录**随路线而变（官方镜像读 `/data`，monlor 元数据容器用 `/etc/xiaoya`），且「其余文件由容器自动生成」目前只有社区说明（`sources/p3/z-addone/01_www_cnblogs_com.md:30`）。落地一律以你所用镜像的官方说明为准。

> [!tip] 大白话
> 把「目录映射」想成**给容器开一个抽屉**：容器是搬运工，它自己不带记忆；你把 NAS 上一个真实文件夹（上面那个 `data`）焊到它的 `/data` 抽屉上，它写进去的东西才留在你硬盘上、重启不丢。焊错了或者没焊，容器一重启，数据就没了。

## 3.2 端口：容器内端口与宿主映射要**分开看**

这是最容易写错的一处，务必分两张表读。

**表一：容器内端口**（容器自己监听什么）：

| 容器内端口 | 用途 | 出处 |
| --- | --- | --- |
| `5678` | AList Web 服务 | `sources/01_hub_docker_com.md:17`；`sources/forum/tid-9690.md:40` |
| `2345` | 备用端口 / 其他服务 | `sources/forum/tid-9690.md:41` |
| `2346` | 备用端口 / 其他服务 | `sources/forum/tid-9690.md:42` |

**表二：宿主机映射**（你在浏览器里访问的端口，飞牛论坛实操值）：

| 宿主机端口 | → 容器内端口 | 说明 | 出处 |
| --- | --- | --- | --- |
| `5677` | `5678` | AList Web 服务 | `sources/forum/tid-9690.md:40` |
| `5345` | `2345` | 备用端口 | `sources/forum/tid-9690.md:41` |
| `5346` | `2346` | 备用端口 | `sources/forum/tid-9690.md:42` |

映射关系在 compose 里写作 `"宿主机:容器"`，帖子的注释点明了方向：「宿主机端口 5677 映射到容器的 5678 端口」（`sources/forum/tid-9690.md:40`），并提示「冒号左侧为宿主机端口，可以修改为你需要使用的端口，右侧不需要修改」（`sources/forum/tid-9690.md:32`）。

> [!warning] 一处来源冲突，并列保留、不合并
> 关于「**官方镜像**的容器内端口是多少」，两份来源说法不同：官方镜像页写「端口：5678」（`sources/01_hub_docker_com.md:17`）；而另一份部署笔记用的是同一个官方镜像 `xiaoyaliu/alist:latest`，却把宿主 `6789` 映射到**容器 `80`**（`sources/p2/newzone-xiaoya.md:18-23`）。同一「官方镜像」两种内端口说法，**本笔记不裁断**——结论只保留到「以你实际镜像文档为准」，不写死某一个数字。

> [!tip] 大白话
> 把端口想成**门牌号**：容器内的 `5678` 是它在屋里自己的门牌，宿主机的 `5677` 是你从大门口进去的门牌。访客（浏览器）走的是大门那个号（`5677`），屋里那个号（`5678`）访客看不见。所以写配置时，「左边（外面）随你改，右边（屋里）别乱动」。

## 3.3 凭据：阿里云盘三件套 + WebDAV 账号

小雅要访问你的阿里云盘，就需要三样凭据。monlor 路线用**环境变量**注入，维护者特别注明这样「无需映射文件」：

> 「通过环境变量配置阿里云盘token，无需映射文件」（`sources/p2/monlor-144.md:21`）

三个变量的含义，配置注释里写得很清楚：

| 环境变量 | 含义（来源注释） | 出处 |
| --- | --- | --- |
| `ALIYUN_TOKEN` | 阿里云盘的访问令牌，需要用户填写 | `sources/forum/tid-9690.md:45` |
| `ALIYUN_OPEN_TOKEN` | 阿里云盘的开放访问令牌，需要用户填写 | `sources/forum/tid-9690.md:46` |
| `ALIYUN_FOLDER_ID` | 阿里云盘的文件夹 ID，用于指定操作目录 | `sources/forum/tid-9690.md:47` |

帖子把它们列为**必填项**：「`ALIYUN_TOKEN` `ALIYUN_OPEN_TOKEN` `ALIYUN_FOLDER_ID` 这三个是必填项」（`sources/forum/tid-9690.md:32`）。

**另一条注入路线（文件）：** 官方镜像路线不走环境变量，而是读容器内的凭据文件——把三样凭据各写进一个 `.txt`，丢进映射给容器的数据目录即可，**文件名是固定约定**：

| 凭据内容 | 文件名 | 出处 |
| --- | --- | --- |
| 阿里云盘 token（社区称 32 位） | `mytoken.txt` | `sources/01_github_com.md:65`（官方仓库）；`sources/p3/z-addone/01_www_cnblogs_com.md:23`、`sources/p3/gnz48/01_www_cnblogs_com.md:25`（社区教程） |
| 阿里云盘 Open Token / refresh_token（社区称约 280 位） | `myopentoken.txt` | `sources/p3/z-addone/01_www_cnblogs_com.md:24`、`sources/p3/gnz48/01_www_cnblogs_com.md:25` |
| 转存目录的 folder id | `temp_transfer_folder_id.txt` | `sources/p3/z-addone/01_www_cnblogs_com.md:25`、`sources/p3/gnz48/01_www_cnblogs_com.md:32` |

社区教程对放置位置的描述是「创建 _data_ 文件夹，将三个 txt 文件放入」（`sources/p3/z-addone/01_www_cnblogs_com.md:28`）、「上传至群晖 docker/xiaoya 文件夹」（`sources/p3/gnz48/01_www_cnblogs_com.md:32`）——也就是映射进容器的那块数据目录。**文件名一致，但放哪个目录要看路线**：官方镜像读 `/data`，monlor 元数据容器用 `/etc/xiaoya`。

**WebDAV 账号**（用来把资源库当文件夹挂载），多处来源一致：

> 「webdav 账号密码 用户: guest 密码: guest_Api789」（`sources/01_hub_docker_com.md:18`）

论坛实测答复也一致：「webdav的配置的用户名和密码是guest/guest_Api789」（`sources/forum/tid-9690.md:72`），路径为 `/dav`（`sources/forum/tid-9690.md:280`）。凭据三件套与 WebDAV 账号的语境，我在 [[流媒体与影音/网盘影视播放与本地存储的取舍]] 里也有铺垫。

> [!note] 「`dav` 还是 `guest`」其实是**两条路线**，不是同一个冲突
> 论坛帖的 compose 注释写「默认用户为 dav」（`sources/forum/tid-9690.md:55`），楼主实测答复写 `guest` / `guest_Api789`（`sources/forum/tid-9690.md:72`、官方镜像页 `sources/01_hub_docker_com.md:18`）。回头核对 monlor 仓库的 `env` 模板，能看到同一条注释的两半：
>
> | monlor `env` 原文 | 说人话 |
> | --- | --- |
> | `webdav用户名为dav，设置密码。默认用户密码：guest/guest_Api789` | monlor 路线把 WebDAV **用户名设成 `dav`**（密码由 `WEBDAV_PASSWORD` 设）；`guest` / `guest_Api789` 是**默认账号** |
>
> 出处：`sources/p3/monlor-env/01_raw_githubusercontent_com.md:32`。所以这不是「谁写错了」，而是**按路线取值**：官方镜像用 `guest` / `guest_Api789`，monlor 路线注意用户名是 `dav`。本笔记两条并记。

> [!tip] 大白话
> 把三件套想成**三把钥匙**：`ALIYUN_TOKEN` 是进阿里云盘大门的钥匙，`ALIYUN_OPEN_TOKEN` 是另一把「开放接口」的钥匙，`ALIYUN_FOLDER_ID` 则是告诉小雅「把临时借来的片放进哪个抽屉」。三者缺一，小雅就取不到片。WebDAV 的 `guest` / `guest_Api789` 则是给「挂载文件夹」用的门禁卡——只读、人人相同，别当成你自己的账号密码。

## 3.4 fnOS 兼容性：官方兼容表里是 ✅

你想用在 fnOS（飞牛私有云）上，这一条可以放心：官方仓库的**通用兼容性测试报告**里，fnOS 一行的三项脚本全部通过。表头三列是 `all_in_one.sh`、`emby_config_editor.sh`、`xiaoya_notify.sh（已弃用）`（`sources/01_raw_githubusercontent_com.md:236`），fnOS 一行三项均 ✅（`sources/01_raw_githubusercontent_com.md:277`）。

> [!note] 读表须知
> 第三列 `xiaoya_notify.sh` 表头已标注**「（已弃用）」**，所以「三项均 ✅」里含一个已弃用脚本，别把 ✅ 误读成「它还在维护」。真正对部署有意义的是前两项。

## 3.5 配置清单片段（新手可跳过）

下面只是**待填清单的形态**，不是可直接复制的成品（路径、凭据需你替换）。完整部署命令在下一章。

```yaml
# docker-compose.yml（端口与凭据片段，参考 sources/forum/tid-9690.md:34-47）
services:
  alist:
    image: ghcr.io/monlor/xiaoya-alist:latest   # monlor 路线镜像（非官方）
    volumes:
      - /vol2/1000/docker2/xiaoya/data:/data    # 左边换成你的数据目录
    ports:
      - "5677:5678"   # 左=宿主机端口(可改)  右=容器内端口(不改)
      - "5345:2345"
      - "5346:2346"
    environment:
      ALIYUN_TOKEN: ""        # 必填：访问令牌
      ALIYUN_OPEN_TOKEN: ""   # 必填：开放访问令牌
      ALIYUN_FOLDER_ID: ""    # 必填：文件夹 ID
```

> [!warning] 这里出现的镜像是 monlor 的，**不是**官方镜像
> `ghcr.io/monlor/xiaoya-alist` 是 monlor 维护者发布的镜像；官方镜像名是 `xiaoyaliu/alist`。**两者不可混写**：`ghcr.io` 侧**不是**「官方小雅镜像」。第 4 章会把两条镜像路线并排讲清楚，让你按凭据管理习惯二选一。

## 本章小结

- **只备清单，不部署**：本章给出目录、端口、凭据三张清单；命令集中在第 4 章。
- **目录**：核心是持久化的 `/data` 映射；`/etc/xiaoya` 属配置/元数据；凭据文件名（`mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt`）有多来源，但**放哪个目录随路线而变**。
- **端口务必分内外**：容器内 `5678` / `2345` / `2346`，宿主映射 `5677` / `5345` / `5346`；官方镜像的容器内端口存在 `5678` vs `80` 的**来源冲突，并列保留**。
- **凭据两条路线**：环境变量路线三件套 `ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID`（均必填）；文件路线三件套 `mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt`。WebDAV 默认账号 `guest` / `guest_Api789`；monlor 路线用户名是 `dav`（两条路线并记）。
- **fnOS 在官方兼容表里 ✅**（含一个已弃用脚本），部署前提无兼容性障碍。

**下一章预告**：清单齐了，第 4 章进入部署实战——把单容器的两条镜像路线（官方 `xiaoyaliu/alist` 与 monlor `ghcr.io/monlor/xiaoya-alist`）并排摆开，给出完整的 `docker run` 与 `docker-compose`，并说明两条路线在**凭据注入方式**上的根本差异，让你按自己的习惯二选一。

## 引文对照（原文 / 中译）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译」列对中文原文给的是**说人话**的复述；配置项、路径、文件名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `将容器中的 /data 目录映射到名为 xiaoya 的数据卷，用于持久化存储` | 把容器里的 /data 映射成宿主机卷，用来持久化存数据 | `sources/forum/tid-9690.md:38` |
| 2 | `端口：5678 访问： http://xxxxx:5678/` | 端口 5678，浏览器访问 http://该设备 IP:5678/ | `sources/01_hub_docker_com.md:17` |
| 3 | `宿主机端口 5677 映射到容器的 5678 端口，alist Web 服务` | 宿主 5677 对到容器 5678，跑 AList 网页服务 | `sources/forum/tid-9690.md:40` |
| 4 | `宿主机端口 5345 映射到容器的 2345 端口，备用端口或其他服务使用` | 宿主 5345 对到容器 2345，备用端口 | `sources/forum/tid-9690.md:41` |
| 5 | `通过环境变量配置阿里云盘token，无需映射文件` | 用环境变量注入阿里云盘 token，不用再映射文件 | `sources/p2/monlor-144.md:21` |
| 6 | `ALIYUN_TOKEN: "" # 阿里云盘的访问令牌，需要用户填写` | ALIYUN_TOKEN：阿里云盘访问令牌，必填 | `sources/forum/tid-9690.md:45` |
| 7 | `ALIYUN_OPEN_TOKEN: "" # 阿里云盘的开放访问令牌，需要用户填写` | ALIYUN_OPEN_TOKEN：开放访问令牌，必填 | `sources/forum/tid-9690.md:46` |
| 8 | `ALIYUN_FOLDER_ID: "" # 阿里云盘的文件夹 ID，用于指定操作目录` | ALIYUN_FOLDER_ID：指定操作用哪个文件夹 | `sources/forum/tid-9690.md:47` |
| 9 | `webdav 账号密码 用户: guest 密码: guest_Api789` | WebDAV 账号：用户 guest，密码 guest_Api789 | `sources/01_hub_docker_com.md:18` |
| 10 | `webdav的配置的用户名和密码是guest/guest_Api789` | WebDAV 用户名密码就是 guest/guest_Api789 | `sources/forum/tid-9690.md:72` |
| 11 | `WEBDAV_PASSWORD: "" # WebDAV 的用户密码，默认用户为 dav` | （yml 注释）WebDAV 密码，注释称默认用户为 dav（与实测冲突） | `sources/forum/tid-9690.md:55` |
| 12 | `自动刷新/etc/xiaoya/mycheckintoken.txt、/etc/xiaoya/mytoken.txt` | 自动刷新 /etc/xiaoya 下的 mycheckintoken.txt、mytoken.txt | `sources/01_github_com.md:65` |
| 13 | `fnOS (飞牛私有云)` | 兼容表里的 fnOS 一行，三项脚本均 ✅ | `sources/01_raw_githubusercontent_com.md:277` |
| 14 | `all_in_one.sh` | 兼容表列名之一（主安装脚本） | `sources/01_raw_githubusercontent_com.md:236` |
| 15 | `/data/docker_address.txt` | 报错日志里出现的容器内文件路径 | `sources/forum/tid-9690.md:96` |
| 16 | `6789:80` | 另一份笔记的端口映射：宿主 6789 对容器 80 | `sources/p2/newzone-xiaoya.md:23` |
| 17 | `mytoken.txt` | 凭据文件名：阿里云盘 token | `sources/p3/z-addone/01_www_cnblogs_com.md:23` |
| 18 | `myopentoken.txt` | 凭据文件名：Open Token / refresh_token | `sources/p3/z-addone/01_www_cnblogs_com.md:24` |
| 19 | `temp_transfer_folder_id.txt` | 凭据文件名：转存目录 folder id | `sources/p3/z-addone/01_www_cnblogs_com.md:25` |
| 20 | `webdav用户名为dav，设置密码。默认用户密码：guest/guest_Api789` | （monlor env 注释）WebDAV 用户名 dav，密码自设；默认账号 guest/guest_Api789 | `sources/p3/monlor-env/01_raw_githubusercontent_com.md:32` |

---

# 第 4 章 部署实战——单容器小雅（两条镜像路线）

## 本章要解决的问题

第 3 章备好了目录、端口、凭据三张清单，本章把**单容器**的小雅真正跑起来。同样是「跑一个小雅」，社区有两条主流镜像路线：官方镜像 `xiaoyaliu/alist`，与社区维护者 monlor 发布的 `ghcr.io/monlor/xiaoya-alist`。两条路线最大的差别不在功能，而在**凭据怎么注入**——一条读文件，一条读环境变量。一句话结论：**先按你的习惯选一条路线，再照着那条路线的命令复制；两条路线不可混用。**

## 4.1 先认路：两条镜像路线是什么

| 路线 | 镜像名 | 谁在维护 | 凭据注入 | 部署入口 | 出处 |
| --- | --- | --- | --- | --- | --- |
| 官方路线 | `xiaoyaliu/alist` | 小雅官方发布 | 文件（三件套 `.txt`） | 一键脚本 | `sources/01_hub_docker_com.md:16` |
| monlor 路线 | `ghcr.io/monlor/xiaoya-alist` | 社区（monlor） | 环境变量 | Compose / 一键脚本 | `sources/p2/monlor-144.md:21`；`sources/forum/tid-9690.md:36` |

> [!warning] 两个镜像名不可混写
> `ghcr.io/monlor/xiaoya-alist` 是 **monlor 的社区镜像**，**不是**官方小雅镜像；官方镜像名是 `xiaoyaliu/alist`。两条路线的**容器内端口、凭据注入方式都不同**，把 A 的命令和 B 的配置混着抄，会两头不靠。第 3 章已经就这一点留过警告，本章把两条路线并排讲透。

> [!tip] 大白话
> 把两条路线想成**两个牌子的同款电器**：都能干同样的活（放出小雅影音库），但一个是原厂、一个是第三方改装；插座（端口）和电池仓（凭据）位置不一样。**配件不能跨牌子装**，所以先选牌子，再按那本说明书接线。

## 4.2 路线一：官方镜像 `xiaoyaliu/alist`

官方镜像页给出的最短路径是一条一键脚本。页面上的原话是：

> 「一键安装和更新容器」（`sources/01_hub_docker_com.md:16`）

脚本命令为：

```bash
# 在 NAS 的 SSH 终端执行（官方镜像的一键安装/更新脚本）
# 出处：sources/01_hub_docker_com.md:16
bash -c "$(curl -s http://docker.xiaoya.pro/update_new.sh)"
```

官方镜像页同时交代了三件事：访问端口是 `5678`（`sources/01_hub_docker_com.md:17`）、WebDAV 默认账号是 `guest` / `guest_Api789`（`sources/01_hub_docker_com.md:18`）、以及「重启就会自动更新数据库及搜索索引文件」（`sources/01_hub_docker_com.md:19`）。这个镜像的特点，页面自己描述为把站点内容内嵌、并加了 AList 本身没有的搜索功能（`sources/01_hub_docker_com.md:10`）。

如果不用一键脚本、想手写容器命令，社区教程给过一条等价写法（**注意这是社区示例，不是官方页逐字给出的命令**）：

```bash
# 在 NAS 的 SSH 终端执行（官方镜像，社区示例写法）
# 出处：sources/p3/gnz48/01_www_cnblogs_com.md:39
docker run -d --restart=always --name="xiaoya" \
  -p 5678:80 -p 2345:2345 -p 2346:2346 \
  -v /volume1/docker/xiaoya:/data \
  xiaoyaliu/alist:latest
```

这行里 `-v` 左边是你自建的数据目录（换成第 3 章清单里你自己那个路径），右边是容器内的 `/data`。

> [!warning] 「容器内到底是几号端口」此处不裁断
> 上面这条社区命令把宿主 `5678` 对到**容器 `80`**；而官方镜像页只写「端口：`5678`」（`sources/01_hub_docker_com.md:17`）。同一「官方镜像」出现两种容器内端口说法，**第 3 章已并列保留、本章不重复裁断**——落笔时只保留「以你实际镜像文档为准」。

另有一个社区整合脚本（ddsrem 维护），可以一次装多种组件。菜单里对应项是「安装 小雅Alist -> 1 1」「安装 Emby全家桶（一键） -> 2 1」（`sources/01_raw_githubusercontent_com.md:75`、`sources/01_raw_githubusercontent_com.md:76`），入口是：

```bash
# 社区整合脚本入口（可装小雅 Alist / Emby 全家桶等）
# 出处：sources/01_raw_githubusercontent_com.md:39
bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"
```

## 4.3 路线二：monlor 镜像 `ghcr.io/monlor/xiaoya-alist`

monlor 路线用 Compose 编排，凭据走环境变量。维护者把这条差异点明：

> 「通过环境变量配置阿里云盘token，无需映射文件」（`sources/p2/monlor-144.md:21`）

它也有自己的**一键部署脚本**（`sources/p2/monlor-144.md:32`）：

```bash
# monlor 路线一键脚本
# 出处：sources/p2/monlor-144.md:32
bash -c "$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)"
```

一手写、只跑「单容器小雅」的 Compose 长这样（**先看完整文件，再逐点解释**）：

```yaml
# docker-compose.yml（monlor 路线，仅 alist 单容器）
# 出处：sources/forum/tid-9690.md:34-71
services:
  alist:
    image: ghcr.io/monlor/xiaoya-alist:latest   # monlor 社区镜像（非官方）
    volumes:
      - /vol2/1000/docker2/xiaoya/data:/data     # 左=你的数据目录，右=容器内 /data
    ports:
      - "5677:5678"   # 左=宿主机端口(可改)，右=容器内端口(不改)
      - "5345:2345"
      - "5346:2346"
    environment:
      TZ: Asia/Shanghai
      ALIYUN_TOKEN: ""          # 必填：阿里云盘访问令牌
      ALIYUN_OPEN_TOKEN: ""     # 必填：开放访问令牌
      ALIYUN_FOLDER_ID: ""      # 必填：文件夹 ID
      AUTO_UPDATE_ENABLED: "true"
      AUTO_CLEAR_ENABLED: "true"
      EMBY_ENABLED: "false"     # 只要单容器，这一项保持 false
      JELLYFIN_ENABLED: "false"
    restart: unless-stopped
    networks:
      - default

networks:
  default:
```

几个要点：

- **凭据三件套**（`ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID`）是必填项，含义与第 3 章一致（`sources/forum/tid-9690.md:45`、`:46`、`:47`）。
- `EMBY_ENABLED` / `JELLYFIN_ENABLED` 保持 `"false"`，就只起 alist 一个容器——这才是本章说的**单容器**形态；把它改成 `true`，monlor 会连带起 metadata、emby 等容器，那就落回第 2 章讲过的「全家桶」侧。
- 端口方向仍是「左宿主、右容器」（`sources/forum/tid-9690.md:40`）。

落地命令：

```bash
# 在 docker-compose.yml 所在目录执行
cd /vol2/1000/docker2/xiaoya
docker compose up -d
docker compose logs      # 看启动日志
```

> [!note] ghcr 镜像在国内可能拉不动
> monlor 镜像托管在 `ghcr.io`，社区实测有拉取失败的情况，报错形如读 `ghcr.io/v2/` 时连接被重置（`sources/forum/tid-9690.md:410`）。同一帖子给出的绕法是改用国内镜像源，把镜像地址里的 `ghcr.io` 换成 `ghcr.nju.edu.cn`（`sources/forum/tid-9690.md:942`）。这是**社区绕法**，能否拉通因网络而异。

## 4.4 两条路线差异对照

| 维度 | 官方路线 `xiaoyaliu/alist` | monlor 路线 `ghcr.io/monlor/xiaoya-alist` |
| --- | --- | --- |
| 维护方 | 小雅官方 | 社区（monlor） |
| 凭据注入 | 文件三件套（第 3 章表二） | 环境变量三件套 |
| 部署入口 | 一键脚本 / 手写 `docker run` | Compose / 一键脚本 |
| 容器内 Web 端口 | 官方页写 `5678`；社区示例映射到 `80`（并列保留） | `5678` |
| 与 Emby 的关系 | 全家桶另配 | Compose 里用 `EMBY_ENABLED` 开关 |
| 出处 | `sources/01_hub_docker_com.md:16-19` | `sources/p2/monlor-144.md:21`；`sources/forum/tid-9690.md:36` |

怎么选：习惯「三个 `.txt` 文件摆平一切」的，走官方路线；习惯「一个 `.env` / Compose 管到底」的，走 monlor 路线。两者都能停在**单容器**形态，之后接前端的方式（第 5 章）也一样。

## 4.5 部署后自检：该看到什么

按顺序核对，能少走很多弯路：

1. **容器状态**：`docker ps` 里应能看到容器在运行（重启策略为 `always` 或 `unless-stopped`）。
2. **首次打开网页会「失败」，这是正常的**。原帖把这一现象写得很直白：

   > 「刚开始页面会显示“获取设置失败”，这是正常情况」（`sources/p3/gnz48/01_www_cnblogs_com.md:46`）

   论坛里有人同样遇到「一直提示……获取设置失败：请稍后，正在加载储存」，楼主的答复只有一句：「等一会儿就好了！」（`sources/forum/tid-9690.md:200`）。初始化按网络情况**需要 1~5 分钟**（`sources/p3/gnz48/01_www_cnblogs_com.md:46`），别当成故障。
3. **能播放**：在网页里随便点开一个视频，确认能播（`sources/p3/gnz48/01_www_cnblogs_com.md:69`）。
4. **WebDAV 能挂**：用 `guest` / `guest_Api789`、路径 `/dav` 挂载（第 3 章已列，`sources/forum/tid-9690.md:72`、`:280`）。
5. **token 会过期**：出现「无法加载列表 / 播放失败」时，先更新 token（`sources/p2/newzone-xiaoya.md:32`）。

> [!warning] 两个高频报错
> 一是 `/data/docker_address.txt: Operation not permitted`（`sources/forum/tid-9690.md:96`）——容器往 `/data` 写文件被拒，多为目录**权限**问题，检查映射目录的读写权限。二是拉镜像时 `ghcr.io/v2/` 连接被重置（`sources/forum/tid-9690.md:410`）——网络到 ghcr 不通，换镜像源（见 4.3 注）。

> [!tip] 大白话
> 小雅**第一次启动在「组装」**：它在拉取并索引资源目录，所以头几分钟网页打不开还报「获取设置失败」，就像新买的书柜还没装好、你急着往里塞书当然塞不进去。**等它装完**，再刷新就好了。

## 本章小结

- **两条镜像路线**：官方 `xiaoyaliu/alist`（文件注入凭据）与 monlor `ghcr.io/monlor/xiaoya-alist`（环境变量注入凭据）；**镜像名不可混写**。
- **官方路线**：一键脚本 `docker.xiaoya.pro/update_new.sh`；社区示例的 `docker run` 把宿主 `5678` 对到容器 `80`。
- **monlor 路线**：Compose 起 alist，`EMBY_ENABLED` / `JELLYFIN_ENABLED` 保持 `false` 即单容器；ghcr 在国内可能需要换镜像源。
- **部署后自检五点**：容器在跑、首次「获取设置失败」属正常（1~5 分钟）、能播、WebDAV 能挂、token 会过期要更新。
- **两个高频报错**：`/data` 权限被拒、ghcr 拉取被重置。

**下一章预告**：小雅跑起来了，但飞牛影视默认还不认识它。第 5 章讲**前端接入**——为什么不能把整个小雅库直接喂给飞牛影视刮削，如何用 STRM 文件（只存 URL 指针）配合 302 直链把资源接进媒体库，以及 SmartStrm / MediaWarp / fntv-proxy 这几个工具各自站在哪一环。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译 / 说人话」列对中文原文给的是**复述**；配置项、路径、命令、文件名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `bash -c "$(curl -s http://docker.xiaoya.pro/update_new.sh)"` | 官方镜像的一键安装/更新脚本命令 | `sources/01_hub_docker_com.md:16` |
| 2 | `端口：5678 访问： http://xxxxx:5678/` | 官方镜像：端口 5678，浏览器访问该设备 IP 的 5678 | `sources/01_hub_docker_com.md:17` |
| 3 | `webdav 账号密码 用户: guest 密码: guest_Api789` | WebDAV 默认账号 guest / guest_Api789 | `sources/01_hub_docker_com.md:18` |
| 4 | `docker restart xiaoya` | 重启容器即自动更新数据库与搜索索引 | `sources/01_hub_docker_com.md:19` |
| 5 | `-p 5678:80 -p 2345:2345 -p 2346:2346 -v /volume1/docker/xiaoya:/data` | 社区示例：宿主 5678→容器 80，并挂载数据目录 | `sources/p3/gnz48/01_www_cnblogs_com.md:39` |
| 6 | `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"` | 社区整合脚本入口 | `sources/01_raw_githubusercontent_com.md:39` |
| 7 | `安装 小雅Alist -> 1 1` | 整合脚本菜单：装小雅 Alist | `sources/01_raw_githubusercontent_com.md:75` |
| 8 | `安装 Emby全家桶（一键） -> 2 1` | 整合脚本菜单：一键装 Emby 全家桶 | `sources/01_raw_githubusercontent_com.md:76` |
| 9 | `通过环境变量配置阿里云盘token，无需映射文件` | monlor 路线用环境变量注入凭据，不用映射文件 | `sources/p2/monlor-144.md:21` |
| 10 | `image: ghcr.io/monlor/xiaoya-alist:latest` | monlor 路线镜像（社区，非官方） | `sources/forum/tid-9690.md:36` |
| 11 | `宿主机端口 5677 映射到容器的 5678 端口，alist Web 服务` | 宿主 5677 → 容器 5678，跑 AList 网页服务 | `sources/forum/tid-9690.md:40` |
| 12 | `ALIYUN_TOKEN: "" # 阿里云盘的访问令牌，需要用户填写` | 环境变量：阿里云盘访问令牌，必填 | `sources/forum/tid-9690.md:45` |
| 13 | `image: xiaoyaliu/alist:latest` | 官方镜像名 | `sources/p2/newzone-xiaoya.md:18` |
| 14 | `6789:80` | 另一份笔记的端口映射：宿主 6789 → 容器 80 | `sources/p2/newzone-xiaoya.md:23` |
| 15 | `仅部署 Alist` | monlor 配置推荐表一行：仅部署 Alist = 1 核 / 512M / 512M | `sources/p2/monlor-144.md:78` |
| 16 | `刚开始页面会显示“获取设置失败”，这是正常情况` | 首次访问显示「获取设置失败」属正常 | `sources/p3/gnz48/01_www_cnblogs_com.md:46` |
| 17 | `/data/docker_address.txt: Operation not permitted` | 常见报错：容器写 /data 无权限 | `sources/forum/tid-9690.md:96` |
| 18 | `等一会儿就好了！` | 对「获取设置失败」的答复：等一会儿 | `sources/forum/tid-9690.md:200` |
| 19 | `docker_address.txt` | 小雅自身地址文件（TVBox 等会用） | `sources/p2/newzone-xiaoya.md:58` |

---

# 第 5 章 前端接入——让飞牛影视认到小雅

## 本章要解决的问题

小雅容器跑起来了，但飞牛影视默认并不认识它。直觉做法是「把整个小雅库当文件夹挂给飞牛影视，让它刮削出海报墙」——这个直觉正是社区里反复踩的坑（第 6 章会细讲风控）。本章给出一条更稳的路：**先让工具生成 STRM 文件（只存 URL 指针），再把飞牛影视的媒体库指向 STRM 目录**。一句话结论：**STRM 只存指针不存片，配合 302 直链，播放流量不经过你的 NAS。**

## 5.1 先纠正一个直觉：别把整个小雅库直接喂给刮削

社区里有人做过这件事，并留下了明确的提醒。原帖自己先说不要这么干：

> 「不建议挂载小雅的全部文件夹！」（`sources/forum/tid-40446.md:33`）

同一帖子后来给出的可行做法是缩小范围：

> 「直接挂载小雅小面的strm文件夹就可以，刮削的时候不会触发风控」（`sources/forum/tid-40446.md:161`）

为什么整库挂载会出事？因为小雅的机制是**把你点播的内容转存进你自己的网盘**再播放：

> 「小雅的机制就是把想看的内容转存到网盘里，然而它默认并不会自动删除。」（`sources/forum/tid-6046.md:71`）

刮削器会把整个库当成「要看的内容」逐一处理，于是转存量暴涨。原帖对这个现象的描述见第 6 章 6.2。**结论：媒体库只挂 STRM 子目录，不挂整个小雅库。**

> [!tip] 大白话
> 把「整库挂给刮削器」想成**让装修队把整栋楼挨个房间量一遍尺寸**：量一间，就往你家搬一堆材料，你家瞬间被塞满。**只挂 STRM 子目录**，等于只告诉装修队「就量我要的那几间」——要什么量什么，别的房间不碰。

## 5.2 STRM 是什么：一个只写一行 URL 的指针文件

STRM 文件的本质，fntv-proxy 的说明写得最直白：

> 「strm 只是 URL 指针」（`sources/lens-b/fntvproxy/01_github_com.md:266`）

也就是说，一个 `.strm` 文件**整个文件就只有一行内容**，那行是一个 URL：

```text
# 举例：某集.strm 文件内容（整个文件仅此一行）
https://你的公网域名/115/xxxxxx.mp4
```

播放器打开这个「文件」时，其实读到的是那行 URL，然后直接跳到真实地址去取流——**媒体文件本身始终在网盘上，不在 NAS 上**。

STRM 的价值，MediaWarp 的说明点得很清楚——它能让「流量不经过」媒体服务器：

> 「Strm 文件可以实现 302 直链播放」（`sources/lens-b/mediawarp/01_github_com.md:53`）

这里出现的两个词先扫盲：

| 名词 | 说人话 |
| --- | --- |
| STRM 文件 | 一行 URL 的「指针文件」，本身不含视频数据 |
| 302 直链 | HTTP 的重定向：服务器回一句「你直接去这个地址取」，客户端改去真实地址 |
| 转存 / 风控 | 小雅把点播内容复制进你的网盘；触发平台风控会限速或拒绝 |

关于 STRM 与 302 的完整原理，可参看 [[流媒体与影音/Strm流文件与302播放详解]]。

> [!warning] STRM 里写什么地址，决定它能不能出内网
> 论坛教程指出一个常见现实：
>
> > 「目前有些项目生成的strm文件，默认写入的是局域网 IP地址，这就意味着它只适用于内网环境，一旦离开家里的局域网，播放就会直接失败」（`sources/p2/tid-57134.md:32`）
>
> 所以「生成设置」里的**基础地址**要填成能公网访问的地址（域名 / 内网穿透 / 专属域名等），否则 STRM 只能在家里的局域网用。外网访问的具体坑见第 6 章 6.3。

## 5.3 生成 STRM：用 SmartStrm（应用中心或 Docker）

生成 STRM 的常用工具是 SmartStrm。它有**两条安装路线**，且自己声明：

> 「SmartStrm 已上架 fnOS，你可以在直接在应用中心搜索安装。」（`sources/01_smartstrm_github_io.md:77`）

**路线 A：飞牛应用中心安装**（最省事）。应用数据默认在 `应用文件/SmartStrm`，卸载不会自动删数据（`sources/01_smartstrm_github_io.md:79`）。要注意它的版本节奏：

> 「由于飞牛审核上架周期较长，通常会比 Docker 镜像滞后 1~2 个版本。」（`sources/01_smartstrm_github_io.md:82`）

**路线 B：Docker Compose 安装**（版本更新更及时）。先看完整文件：

```yaml
# docker-compose.yml（SmartStrm）
# 出处：sources/01_smartstrm_github_io.md:17-34
name: smartstrm
services:
  smartstrm:
    image: cp0204/smartstrm:latest
    container_name: smartstrm
    restart: unless-stopped
    network_mode: host          # 官方建议默认 host，便于在容器内改 302 代理端口
    volumes:
      - /yourpath/smartstrm/config:/app/config   # 配置目录
      - /yourpath/smartstrm/strm:/strm           # STRM 生成目录（重要）
      - /yourpath/smartstrm/logs:/app/logs       # 日志，可选
      - /yourpath/smartstrm/tools:/app/tools     # 工具，可选
    environment:
      PORT=8024                # 管理端口
      ADMIN_USERNAME=admin     # 管理用户名
      ADMIN_PASSWORD=admin123  # 管理密码
```

部署后「通过 `http://yourip:8024` 访问管理后台」（`sources/01_smartstrm_github_io.md:57`）。把 `/yourpath` 换成你实际的存放路径即可。

生成 STRM 的完整流程，飞牛论坛的实战教程按步骤给出过（`sources/p2/tid-57134.md:32`），可归纳为：

1. 在应用中心安装套件 SmartStrm（或用上面 Compose）；
2. 浏览器访问 `http://ip:8024` 登录管理后台；
3. 到「系统设置 → strm 设置 → 生成设置」，修改**默认 STRM 储存路径**与**基础地址**（基础地址填域名前缀，**结尾不能有斜杠 `/`**）；
4. 「储存管理 → 添加储存」挂载网盘（夸克、115 等）；
5. 创建任务，选好储存与扫描路径，手动执行一次，在日志里看进度；
6. 去 STRM 目录确认文件已生成，打开一个 `.strm` 看看里面是不是你要的基础地址；
7. 给飞牛影视的 STRM 目录加权限，再添加媒体库刮削。

> [!note] SmartStrm 的 302 代理是收费的，生成 STRM 免费
> 教程特意说明：
>
> > 「此应用其中302代理是收费的，但是我们不需要使用，用它免费的挂载网盘生成strm功能就行了」（`sources/p2/tid-57134.md:32`）
>
> 也就是说，本章只用到它**生成 STRM** 的免费功能；真正做 302 转发的是 5.4 那两个专门的中间件。

## 5.4 让 302 串起来：MediaWarp 与 fntv-proxy 站在哪一环

STRM 生成了，还要有人把「客户端请求 → 302 跳到真实直链」这一环接上。社区有两个专门的中间件，定位不同：

| 工具 | 定位原话 | 飞牛影视支持情况 | 关键端口 | 出处 |
| --- | --- | --- | --- | --- |
| MediaWarp | 「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」（`sources/lens-b/mediawarp/01_github_com.md:51`） | TODO 列表里「适配 飞牛影视」仍是**待办项**（`sources/lens-b/mediawarp/01_github_com.md:86`） | — | 同上 |
| fntv-proxy | 「飞牛影视 / Emby 代理工具 - 自动解析 .strm 文件并重定向到真实直链」（`sources/lens-b/fntvproxy/01_github_com.md:44`） | 原帖称「基于飞牛影视 0.9.3 版本」（`sources/lens-b/fntvproxy/01_github_com.md:45`） | 飞牛 `:28005` / Emby `:8095` | 同上 |

fntv-proxy 的用法很直接：

> 「将播放器地址指向代理端口（飞牛 `:28005`，Emby `:8095`）」（`sources/lens-b/fntvproxy/01_github_com.md:71`）

它的 Compose 会把 STRM 目录挂进容器（**关键**）：

```yaml
# docker-compose.yml（fntv-proxy 节选）
# 出处：sources/lens-b/fntvproxy/01_github_com.md:120-136
services:
  fntv-proxy:
    image: jimboo7339/fntv-proxy:latest
    ports:
      - "28005:28005"   # 飞牛影视代理
      - "8095:8095"     # Emby 代理（启用时才需要）
    volumes:
      - /vol00/strm:/vol00/strm:ro   # 挂载 STRM 目录（前后路径必须一致）
      - ./config.yaml:/app/config.yaml:ro
    restart: unless-stopped
```

> [!warning] STRM 目录必须挂进中间件容器
> 工具文档专门加粗提醒：
>
> > 「strm 路径一定要挂载到 Docker 容器中，否则播放失败，找不到 strm 文件。」（`sources/lens-b/fntvproxy/01_github_com.md:139`）
>
> 而且挂载时**前后路径要一致**（宿主机是什么路径，容器内就写什么路径）。

> [!tip] 大白话
> 把 302 直链想成**快递中转**：包裹（视频）一直放在网盘仓库，从来不用搬进你家。客户端下单后，中间件只负责回一句「你去仓库这个门牌直接取」。中转站（中间件）本身**不囤货**——所以它只在 NAS 上占一点点流量，不占你的硬盘。

## 5.5 纪律：只挂 STRM 子目录，并把它挂进中间件

把本章的两条纪律合起来记：

1. **对飞牛影视**：媒体库指到 STRM 子目录，别挂整个小雅库（5.1）。
2. **对中间件容器**：STRM 目录要挂进容器，且宿主机/容器路径一致（5.4）。

这两条落定后，整条链路就是：**网盘 → 小雅（AList）→ SmartStrm 生成 STRM → 中间件（302）→ 飞牛影视客户端**。

关于播放端的解码能力（要不要硬解、用哪种客户端），可参看 [[流媒体与影音/硬件解码vs软件解码]]。

## 5.6 没有阿里云盘会员、只有夸克会员怎么办

前几节都默认你有阿里云盘。如果你的情况是「**没有阿里云盘会员，只有夸克会员**」，这一节先分清「账号」和「会员」，再说清一件很容易想当然的事：**小雅没有「把小雅资源播放到夸克」这个开关。**

### 5.6.1 先分清：小雅「要账号」≠「要会员」

**① 小雅单容器必须要一个阿里云盘账号。** 原因藏在它的播放机理里：

> 「由于小雅本质是将别人阿里云盘的文件先转存到自己的阿里云盘内再进行播放，如此当时间久了就会是云盘空间不足」（`sources/p3/z-addone/01_www_cnblogs_com.md:33`）

小雅播放时，是把片源**转存进你自己的阿里云盘**，302 直链最终指向的是**阿里云盘上的那个文件**。所以第 3 章的「阿里云盘三件套」是**必填**，填的也是你自己的阿里云盘：

> 「`ALIYUN_TOKEN` `ALIYUN_OPEN_TOKEN` `ALIYUN_FOLDER_ID` 这三个是必填项」（`sources/01_club_fnnas_com.md:32`）

**② 但「必填账号」不等于「必须有会员」**——会员只决定**快不快**：

> 「目前阿里云盘推出了第三方应用权益包的月套餐，不付费就限速，问题是，付费了也只有1T，如果是刷剧，一下子就没了。」（`sources/p2/monlor-144.md:273`）

而且有人实测**充了会员也照样卡**：

> 「阿里云我充了一个月的svip试验，测试是还是限速的，在alist网页端能播放，但卡（380kb/s），所以就非常需要转存到115网盘。」（`sources/p2/monlor-144.md:279`）

**一句话**：没有阿里云盘会员，小雅照样能装、能看，但大概率被限速、体验差。

### 5.6.2 关键：小雅的资源现在主要靠 **115** 播放，跟夸克没关系

「用小雅的资源」这件事，得先知道小雅的资源**放在哪**。它最初全在阿里云盘，后来变了：

> 「于是乎小雅开始转战115网盘，因为115有个转存阿里云盘的功能，简单来说就是，如果这个阿里的资源在115网盘上也有，会立即转存到你自己的网盘中。这样就跳过了阿里云盘的限制。当然115这边也有限制，需要开通会员才可以实现这个功能。……所以想要玩小雅Alist，必须要办个115会员了。」（`sources/p4/ycyc-2878.md:13`）

说人话：**社区绕开阿里限速的套路是「阿里转存 115」**——配置项就叫 `ALIYUN_TO_115`（`sources/p3/monlor-env/01_raw_githubusercontent_com.md:19`），落地文件是 `ali2115.txt`：

> 「这个文件是用来加速阿里云盘资源的，如果你没有办理阿里云盘的会员，但是有115的会员，可以配置这个文件来转存阿里的资源到115网盘，实现流畅观看视频。」（`sources/p4/ycyc-2878.md:19`）

也就是说，**「换播放盘」的开关只有 115，没有夸克**。两个盘都没有会员会怎样，论坛说得很直白：

> 「115和夸克设置自己的token就可以了。没有115会员的话还是放弃吧。115速度时快时慢，体验差。」（`sources/forum/tid-21673.md:11`）

> 「现在在用alist tvbox，但是没有阿里或者115会员的话，会限速到100k」（`sources/forum/tid-21673.md:13`）

### 5.6.3 夸克在小雅里是「挂载你自己的夸克」，不是「把小雅资源转到夸克」

夸克在小雅里确实有一席之地，但标的是**非必填**——是「再挂一个盘」，不是「换掉阿里 / 115」：

> 「如有挂载夸克、115网盘的需求，也可以在配置文件里填写参数」（`sources/01_club_fnnas_com.md:32`）

它做的是**挂载你自己的夸克账号**（配置文件 `quark_cookie.txt`，或环境变量 `QUARK_COOKIE`，`sources/01_club_fnnas_com.md:48`），让小雅能列出 / 播放**你夸克里的**东西。论坛管这叫「小雅夸克玩法」：

> 「1、在小雅 alist 的配置目录下增加 quark_cookie.txt 文件，填入夸克账户的 cookie 并保存；」（`sources/forum/tid-8385880.md:26`）

它**不等于**「把小雅的阿里资源转存到夸克播放」——小雅没有「转存夸克」的开关（只有 `ALIYUN_TO_115`）。有人实测，填了夸克 cookie 也没把小雅资源变成夸克直链：

> 「我查日志发现，夸克cookie放进去etc/xiaoya，查日志还是只有阿里的直链，没有夸克的直链。」（`sources/forum/tid-8385880.md:30`）

论坛里也有人问过「只填夸克、不填阿里三件套行不行」，帖子过去也**没有**给出正面回答（`sources/01_club_fnnas_com.md:732`）。**所以：只有夸克会员，没有现成办法让小雅资源走夸克播放。**

> [!tip] 大白话
> 把 302 想成**快递中转**：仓库（网盘）永远不搬进你家，NAS 只当「目录 + 海报墙 + 中转站」，你能挑的只是「**仓库租在哪一家**」。可小雅的货**记在阿里 / 115 名下**——你想让它改从「夸克仓」发货，**小雅没这个改单入口**。填 `QUARK_COOKIE` 只是「把小雅跟你自己的夸克号对了个表」，不改变小雅自己的货从哪发。

### 5.6.4 只有夸克会员，你实际能选的三条路

| 你的情况 | 走哪条 |
| --- | --- |
| 就用小雅资源、能接受限速 | 小雅照装（三件套必填），不开阿里会员，接受限速（社区实测可低到 ~100KB/s，`sources/forum/tid-21673.md:13`） |
| 就用小雅资源、想要不卡 | **办 115 会员**，配 `ali2115.txt` 走「阿里转存 115」（`sources/p4/ycyc-2878.md:13`） |
| 不用小雅资源、只想用夸克 | **改挂你自己的夸克库**：夸克网盘 TV 驱动 → SmartStrm → fntv-proxy 302（见 5.6.5） |

> [!warning] 115 路线也不是万无一失
> 有用户反馈 115 转存直接报「非115会员不支持此操作」，而且**大于 5G 的文件不转**（甚至 5G 以下也报）（`sources/forum/tid-8385880.md:32`、`:34`）。这条链路能让小雅资源跑起来，但别当成百发百中。

### 5.6.5 备选：干脆改挂「你自己的夸克库」（不依赖小雅资源）

如果你能接受「看的不是小雅的资源，而是**你自己夸克里的片**」，那第 5 章这套链路照样成立——**小雅不是唯一方案**，5.3～5.4 的「挂网盘 → 生成 STRM → 中间件 302 → 飞牛影视」对**你自己的夸克库**同样适用：

1. 用**「夸克网盘 TV」驱动**挂上你的夸克——SmartStrm 的储存管理就支持挂「**夸克、115、天翼、123 等**」（`sources/p2/tid-57134.md:32`，即 5.3 步骤 4）；
2. STRM 生成目录、基础地址等设置同 5.3；
3. 中间件继续用 **fntv-proxy**——它的定位本就是「**主要针对夸克网盘**」：

> 「飞牛代理主要针对 **夸克网盘** 在 **openlist** 的 **夸克 TV 驱动** 挂载下实现 302」（`sources/lens-b/fntvproxy/01_github_com.md:300`）

也就是说，这条链路除了「片源从小雅的阿里库换成你自己的夸克库」，**其余与第 5 章完全一致**——而会员正好落在你已有的夸克上。

> [!warning] 夸克路线的专属坑：部分片源只有 HLS 流，取不到元数据
> 夸克 CDN 对**部分**内容只返回 **HLS 转码流**（`media.m3u8`）而不是 mp4 文件直链，飞牛/Emby 因此**取不到时长、码率、分辨率**。**代理只做透明 302，不会把 HLS 转成 mp4，也无法凭空补全元数据**（`sources/lens-b/fntvproxy/01_github_com.md:241`）。
> 应对：用 **TMDB 外部刮削**补时长/分辨率（不依赖文件 probe），也就是 5.1 说的「让飞牛自己按需刮削」。

## 本章小结

- **别整库刮削**：媒体库只挂 STRM 子目录，避免触发小雅的转存与风控（`sources/forum/tid-40446.md:33`、`:161`）。
- **STRM = 一行 URL 的指针文件**：「strm 只是 URL 指针」（`sources/lens-b/fntvproxy/01_github_com.md:266`），媒体文件始终在网盘。
- **生成 STRM 用 SmartStrm**：应用中心（滞后 1~2 版）或 Docker（版本更及时）；生成免费，302 代理收费、本章不用。
- **基础地址决定外网可用性**：默认写局域网 IP 就只能内网；外网要填可公网访问的地址。
- **接 302 用中间件**：MediaWarp（飞牛适配仍在 TODO）/ fntv-proxy（原帖称基于飞牛影视 0.9.3，播放器指向 `:28005`）；STRM 目录必须挂进容器且前后路径一致。

- **没有阿里云盘会员**：小雅必填的是阿里云盘**账号**、会员只影响速度（不付费即限速，`sources/p2/monlor-144.md:273`）；**「换播放盘」的开关只有 115**（`ali2115.txt` 走「阿里转存 115」，需 115 会员，`sources/p4/ycyc-2878.md:13`）；夸克在小雅里只是 `QUARK_COOKIE` 挂载**你自己的夸克**、**不能**把小雅资源转成夸克播放（实测填了也没夸克直链，`sources/forum/tid-8385880.md:30`）；只有夸克会员时见 5.6：要么忍阿里限速、要么补 115、要么改挂你自己的夸克库（`sources/lens-b/fntvproxy/01_github_com.md:300`）。

**下一章预告**：路走通了不等于走得稳。第 6 章把社区帖里反复出现的四类坑集中成「症状 → 原因 → 怎么避」——装错地方、整库刮削触发风控、外网播放失败、以及播放器 UA 不对就 403，逐条讲清。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。「中译 / 说人话」列对中文原文给的是**复述**；工具名、镜像名、端口、路径、文件名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `不建议挂载小雅的全部文件夹！` | 不要把小雅全部文件夹都挂给刮削器 | `sources/forum/tid-40446.md:33` |
| 2 | `直接挂载小雅小面的strm文件夹就可以，刮削的时候不会触发风控` | 只挂小雅的 strm 子目录即可，刮削不触发风控 | `sources/forum/tid-40446.md:161` |
| 3 | `小雅的机制就是把想看的内容转存到网盘里，然而它默认并不会自动删除。` | 小雅会把点播内容转存进你的网盘，且默认不自动删 | `sources/forum/tid-6046.md:71` |
| 4 | `strm 只是 URL 指针` | STRM 文件只是 URL 指针 | `sources/lens-b/fntvproxy/01_github_com.md:266` |
| 5 | `Strm 文件可以实现 302 直链播放` | STRM 文件可实现 302 直链播放 | `sources/lens-b/mediawarp/01_github_com.md:53` |
| 6 | `目前有些项目生成的strm文件，默认写入的是局域网 IP地址，这就意味着它只适用于内网环境，一旦离开家里的局域网，播放就会直接失败` | 有些工具生成的 STRM 默认写局域网 IP，只能内网用 | `sources/p2/tid-57134.md:32` |
| 7 | `SmartStrm 已上架 fnOS，你可以在直接在应用中心搜索安装。` | SmartStrm 已上架 fnOS，可在应用中心搜索安装 | `sources/01_smartstrm_github_io.md:77` |
| 8 | `由于飞牛审核上架周期较长，通常会比 Docker 镜像滞后 1~2 个版本。` | 应用中心版本通常比 Docker 镜像滞后 1~2 版 | `sources/01_smartstrm_github_io.md:82` |
| 9 | `image: cp0204/smartstrm:latest` | SmartStrm 镜像名 | `sources/01_smartstrm_github_io.md:20` |
| 10 | `network_mode: host` | SmartStrm 建议用 host 网络模式 | `sources/01_smartstrm_github_io.md:23` |
| 11 | `PORT=8024` | SmartStrm 管理端口 | `sources/01_smartstrm_github_io.md:31` |
| 12 | `此应用其中302代理是收费的，但是我们不需要使用，用它免费的挂载网盘生成strm功能就行了` | 302 代理收费，我们只用免费的 STRM 生成 | `sources/p2/tid-57134.md:32` |
| 13 | `前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器` | MediaWarp 是前置在三种媒体服务器前的反向代理 | `sources/lens-b/mediawarp/01_github_com.md:51` |
| 14 | `适配 飞牛影视` | MediaWarp 的 TODO 项：适配飞牛影视（尚未完成） | `sources/lens-b/mediawarp/01_github_com.md:86` |
| 15 | `飞牛影视 / Emby 代理工具 - 自动解析 .strm 文件并重定向到真实直链` | fntv-proxy 的定位：解析 STRM 并重定向到真实直链 | `sources/lens-b/fntvproxy/01_github_com.md:44` |
| 16 | `基于飞牛影视 0.9.3 版本` | fntv-proxy 原帖称基于飞牛影视 0.9.3 | `sources/lens-b/fntvproxy/01_github_com.md:45` |
| 17 | `将播放器地址指向代理端口（飞牛 :28005，Emby :8095）` | 播放器应连代理端口：飞牛 :28005，Emby :8095 | `sources/lens-b/fntvproxy/01_github_com.md:71` |
| 18 | `strm 路径一定要挂载到 Docker 容器中，否则播放失败，找不到 strm 文件。` | STRM 目录必须挂进容器，否则找不到文件、播放失败 | `sources/lens-b/fntvproxy/01_github_com.md:139` |
| 19 | `由于小雅本质是将别人阿里云盘的文件先转存到自己的阿里云盘内再进行播放，如此当时间久了就会是云盘空间不足` | 小雅本质是把片源转存进你自己的阿里云盘再播放，久则空间不足 | `sources/p3/z-addone/01_www_cnblogs_com.md:33` |
| 20 | `目前阿里云盘推出了第三方应用权益包的月套餐，不付费就限速，问题是，付费了也只有1T，如果是刷剧，一下子就没了。` | 阿里云盘不付费就限速，付费也只有 1T 配额 | `sources/p2/monlor-144.md:273` |
| 21 | `阿里云我充了一个月的svip试验，测试是还是限速的，在alist网页端能播放，但卡（380kb/s），所以就非常需要转存到115网盘。` | 用户实测：充 SVIP 仍限速（380kb/s），故需转存 115 | `sources/p2/monlor-144.md:279` |
| 22 | `如有挂载夸克、115网盘的需求，也可以在配置文件里填写参数` | 夸克/115 属「按需额外挂载」，非必填 | `sources/01_club_fnnas_com.md:32` |
| 23 | `QUARK_COOKIE: "" # 夸克网盘的 Cookie，需要用户填写，非必填。` | 配置里夸克 Cookie 明确标「非必填」 | `sources/01_club_fnnas_com.md:48` |
| 24 | `如果用夸克上面是不是只填写夸克的Cookie就可以了？就不需要填写阿里云盘的那三个参数了吧？` | 社区同问：只填夸克能否免填阿里三件套（帖中无正面回答） | `sources/01_club_fnnas_com.md:732` |
| 25 | `# 阿里云盘转存115播放` | 社区「阿里转存 115」思路（配置项 `ALIYUN_TO_115`） | `sources/p3/monlor-env/01_raw_githubusercontent_com.md:19` |
| 26 | `飞牛代理主要针对 夸克网盘 在 openlist 的 夸克 TV 驱动 挂载下实现 302` | fntv-proxy 主要面向夸克网盘（OpenList 夸克 TV 驱动） | `sources/lens-b/fntvproxy/01_github_com.md:300` |
| 27 | `代理只做透明 302 转发，不会 把 HLS 转成 mp4，也无法 凭空补全媒体库元数据。` | 代理只做 302，不转 HLS、不补元数据 | `sources/lens-b/fntvproxy/01_github_com.md:241` |
| 28 | `于是乎小雅开始转战115网盘，因为115有个转存阿里云盘的功能，简单来说就是，如果这个阿里的资源在115网盘上也有，会立即转存到你自己的网盘中。这样就跳过了阿里云盘的限制。当然115这边也有限制，需要开通会员才可以实现这个功能。而且最新的很多资源小雅都放到了115网盘中，所以想要玩小雅Alist，必须要办个115会员了。` | 小雅转战 115：115 有「转存阿里云盘」功能，播放时把资源转存到你的 115、绕开阿里限速，需 115 会员 | `sources/p4/ycyc-2878.md:13` |
| 29 | `这个文件是用来加速阿里云盘资源的，如果你没有办理阿里云盘的会员，但是有115的会员，可以配置这个文件来转存阿里的资源到115网盘，实现流畅观看视频。` | `ali2115.txt` 的作用：没阿里会员但有 115 会员时，把阿里资源转存到 115 播放 | `sources/p4/ycyc-2878.md:19` |
| 30 | `115和夸克设置自己的token就可以了。没有115会员的话还是放弃吧。115速度时快时慢，体验差。` | 论坛回复：115 / 夸克各填自己的 token；没有 115 会员就放弃 | `sources/forum/tid-21673.md:11` |
| 31 | `现在在用alist tvbox，但是没有阿里或者115会员的话，会限速到100k` | 没有阿里或 115 会员会被限速到 100k | `sources/forum/tid-21673.md:13` |
| 32 | `1、在小雅 alist 的配置目录下增加 quark_cookie.txt 文件，填入夸克账户的 cookie 并保存；` | 「小雅夸克玩法」：加 `quark_cookie.txt` 挂载自己的夸克 | `sources/forum/tid-8385880.md:26` |
| 33 | `我查日志发现，夸克cookie放进去etc/xiaoya，查日志还是只有阿里的直链，没有夸克的直链。` | 实测：填了夸克 cookie，日志里仍只有阿里直链、没有夸克直链 | `sources/forum/tid-8385880.md:30` |
| 34 | `已经不行了，日志提示非115会员不支持此操作` | 115 转存报「非115会员不支持此操作」 | `sources/forum/tid-8385880.md:32` |
| 35 | `如果刚好有115会员能行吗，它这个大于5G不支持是会员也不行吗` | 反馈：115 转存「大于 5G 不支持」，会员也存疑 | `sources/forum/tid-8385880.md:34` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-06 | 新增/重写 5.6「没有阿里云盘会员、只有夸克会员怎么办」：澄清小雅必填的是阿里云盘**账号**、会员只影响限速（`sources/p2/monlor-144.md:273`、`:279`）；说明「换播放盘」的开关只有 115（`ali2115.txt` / 阿里转存 115，需 115 会员，`sources/p4/ycyc-2878.md:13`、`:19`），没有「转存夸克」；夸克在小雅里只是 `quark_cookie.txt` / `QUARK_COOKIE` 挂载**你自己的夸克**、**不能**把小雅资源转成夸克播放（实测填了仍只有阿里直链，`sources/forum/tid-8385880.md:30`）；给出「只有夸克会员」的三条现实路径（`sources/forum/tid-21673.md:11`、`:13`），并保留「改挂你自己夸克库 + STRM + 302」备选链路（`sources/lens-b/fntvproxy/01_github_com.md:300`）及其 HLS 元数据坑（`:241`）。 |

---

# 第 6 章 避坑清单——装错地方、风控、外网与 UA

## 本章要解决的问题

前几章把路走通了，但「走得通」不等于「走得稳」。社区帖里反复出现的坑其实有规律，本章把它们归成四类，每条都按**症状 → 原因 → 怎么避**来写：装错地方、整库刮削触发风控、外网播放失败、以及播放器请求头（User-Agent）不对就 403。一句话结论：**能内网别急着外网、能挂 STRM 子目录就别整库刮削、装组件先想清楚装在哪、请求头不是随便设的。**

## 6.1 坑一：装错地方——应用中心版本「取不到数据」

**症状**：从飞牛应用中心装了自带的小雅，实测拿不到视频数据。

社区有一篇专门的修复帖，标题就点明了场景，正文写到：

> 「飞牛NAS应用中心自带的小雅Alist实测无法正常获取到视频数据，如果已经安装了应用中心的小雅Alist需要先卸载掉，然后按照本文的教程重新部署。」（`sources/forum/tid-9690.md:32`）

**怎么避**：需要哪个组件，优先按其**官方文档 / 仓库**给的安装方式（一键脚本或 Docker / Compose），而不是默认从应用中心装。

> [!warning] 这是一篇社区帖的实测，不是官方公告
> 上面那条只来自**一个**社区用户的帖子。本笔记**不**据此写「官方下架了应用中心版本」「应用中心版本停更」这类结论——那超出了该来源能支撑的范围。

> [!note] 一个容易合并错的点：两句话说的不是一回事
> 另有一句流传很广的社区意见：「给你个建议 所有的软件 都不要从飞牛官方应用商店安装 大多数都是阉割/过时」（`sources/forum/tid-40446.md:56`）——这是**一位用户对应用商店的整体看法**。
> 而 SmartStrm 那条「SmartStrm 已上架 fnOS，你可以在直接在应用中心搜索安装。」（`sources/01_smartstrm_github_io.md:77`）说的是**某个具体工具确实上架了**。
> 两者**对象不同**，**并列保留、不合并**：某工具能在商店里找到，不等于「商店里的软件都该装」，也不等于「商店里全都不该装」。装之前，回到第 4 章的原则——看该工具的官方说明。

## 6.2 坑二：风控——整库刮削把网盘撑爆

**症状**：飞牛影视一刮削就卡住，阿里云盘突然满了，账号被风控。

**原因**：小雅的工作方式是**把内容转存进你自己的网盘**再播（第 5 章 5.1 已引 `sources/forum/tid-6046.md:71`）。整库刮削等于让它把整个库都当成「要看的内容」去转存，量级瞬间失控。原帖是这么描述的（**按原帖称记录，不当作可复现的精确数值**）：

> 「飞牛影视在刮削的时候会在阿里云盘存储临时文件！！！基本上半分钟就需要几个T的存储，然后阿里云就满了！！！！！然后还会触发风控！！」（`sources/forum/tid-40446.md:33`）

另一位用户遇到的是同一机理的另一面——**卡在扫描**：

> 「小雅在安装后，使用飞牛影视扫描小雅网盘会将网盘内容转存到个人阿里网盘，但是个人网盘容量太小，导致飞牛影视会卡在扫描怎么解决？」（`sources/forum/tid-6046.md:33`）

**怎么避**：两条一起上——

1. **只挂 STRM 子目录**给飞牛影视，别挂整个小雅库：「直接挂载小雅小面的strm文件夹就可以，刮削的时候不会触发风控」（`sources/forum/tid-40446.md:161`）；
2. **开自动清理**（第 4 章的 `AUTO_CLEAR_ENABLED`，或小雅助手一类的清理工具）。原帖的建议也是这个方向：「挂个自动清理，不然看的时候也得手动清」（`sources/forum/tid-6046.md:71`）。

> [!tip] 大白话
> 把「触发风控」想成**银行卡被风控电话拦下**：短时间内你的账号出现「海量转存」这种异常行为，平台会先拦再说。整库刮削就是让账号「疯狂转账」，自己把风控招来；只挂 STRM 子目录、只对你要看的片子动手，才是正常用卡。

## 6.3 坑三：外网播放失败——内网地址出了门就失效

**症状**：在家里的局域网能播，手机切到蜂窝网络就播不了。

**原因**：STRM 里写的是**局域网地址**，出门后客户端根本解析不到。论坛一篇技术分析把它归到这一点（**该帖是单个用户的排查记录，此处按原帖称**）：

> 「手机在蜂窝网络上无法使用 NAS 内部域名」（`sources/forum/tid-73955.md:42`）

**怎么避**：生成 STRM 时把**基础地址**填成能公网访问的地址（公网域名、内网穿透、专属域名等），而不是局域网 IP。第 5 章 5.2 已引过同一提醒（`sources/p2/tid-57134.md:32`）。

> [!warning] 一个具体主机名不作结论
> 上面那篇帖子在描述里出现过具体的内网主机名（形如 `xiaoya.host`）。这属于**单个社区技术帖**的说法，本笔记**不把它当作「官方内网域名」的结论**，只保留「内网地址不能用于外网」这一语义——这一点在技术上是确定的。

> [!tip] 大白话
> 把内网地址想成**小区里才认的门牌号**：在小区里喊「三号楼」大家都懂，出了小区，快递员听的是一脸问号。要给外面用，就得换成一个全球都能查到的地址（域名）。

## 6.4 坑四：UA 不对就 403——请求头不是随便设的

**症状**：同一条 115 CDN 直链，一个播放器能取到媒体，另一个直接 403。

**原因**：网盘的 CDN 对请求头（User-Agent）有要求。同一篇技术分析帖做过一次受控对照（**原帖称，且原帖自己就限定了结论边界**）：

- 用 `User-Agent: trim_player` 请求那条 CDN 临时链接，返回 206，能取到真实媒体（`sources/forum/tid-73955.md:39`）；
- 把 UA 换成 `Mozilla/5.0`，同一条链接返回 403（`sources/forum/tid-73955.md:40`）。

原帖对这一点的表述很克制，明确说**只证明了「至少绑定 UA」**：

> 「CDN 链接不是任意播放器直接可用；请求头条件至少包含 UA。未证明是否还绑定 IP、Cookie 或其他条件。」（`sources/forum/tid-73955.md:40`）

**怎么避**：别手动改 UA 去硬凑；让请求走**正规中间件**（第 5 章的 fntv-proxy / MediaWarp），由它按工具约定去请求，并按 302 把结果交给播放器。

> [!tip] 大白话
> 把 UA 想成**入场券的票种**：同一张链接，拿「内部员工票」进得去，拿「普通访客票」就被拦。不要求你背票种，交给负责跑腿的中间件去核对就好——你自己乱换票，只会被拦在门外。

## 6.5 一句心态提醒：把它当「社区项目」

这不是一条坑，而是一句提醒。有社区用户对这类项目的评价是：

> 「总的来说小雅alsit并不是一个稳定的项目，依赖于阿里云盘，说不定哪天就给你封接口了；」（`sources/forum/tid-6046.md:156`）

把它当成**社区风险提示**，而不是结论。正因如此，第 1 章讲过的取舍才重要：**本地存储 vs 网盘播放**各有利弊，值不值得押注，先想清楚——相关讨论见 [[流媒体与影音/网盘影视播放与本地存储的取舍]]。

## 本章小结

- **坑一 装错地方**：应用中心自带的小雅取不到数据（`sources/forum/tid-9690.md:32`）；优先按官方文档/仓库安装。**该帖是社区单帖，不推导「官方下架/停更」**；与「商店都好/都不好」之类的说法对象不同，并列保留。
- **坑二 风控**：整库刮削会巨量转存并触发风控（`sources/forum/tid-40446.md:33`、「半分钟几个 T」按原帖称）；避法是只挂 STRM 子目录 + 开自动清理。
- **坑三 外网**：内网地址出门失效（`sources/forum/tid-73955.md:42`）；基础地址要填可公网访问的地址。
- **坑四 UA**：UA 不对同一链接 403（`sources/forum/tid-73955.md:39`、`:40`，原帖限定「至少绑定 UA」）；交给正规中间件处理。
- **心态**：项目依赖阿里云盘，有接口变动风险（`sources/forum/tid-6046.md:156`），自己评估取舍。

**下一章预告**：四类坑躲开后，第 7 章进入**运维与收尾**——日常怎么更新（镜像与元数据）、token 过期怎么续、缓存怎么定期清、以及这套东西接进 Obsidian 笔记与目录时怎么收尾。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。「中译 / 说人话」列对中文原文给的是**复述**；配置项、UA、域名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `飞牛NAS应用中心自带的小雅Alist实测无法正常获取到视频数据，如果已经安装了应用中心的小雅Alist需要先卸载掉，然后按照本文的教程重新部署。` | 应用中心的小雅取不到数据，需卸载后按帖重装 | `sources/forum/tid-9690.md:32` |
| 2 | `给你个建议 所有的软件 都不要从飞牛官方应用商店安装 大多数都是阉割/过时` | 社区意见：尽量别从应用商店装软件 | `sources/forum/tid-40446.md:56` |
| 3 | `SmartStrm 已上架 fnOS，你可以在直接在应用中心搜索安装。` | SmartStrm 这一工具确实已上架 fnOS（与上一条对象不同） | `sources/01_smartstrm_github_io.md:77` |
| 4 | `飞牛影视在刮削的时候会在阿里云盘存储临时文件！！！基本上半分钟就需要几个T的存储，然后阿里云就满了！！！！！然后还会触发风控！！` | 原帖称整库刮削会巨量转存并触发风控 | `sources/forum/tid-40446.md:33` |
| 5 | `小雅在安装后，使用飞牛影视扫描小雅网盘会将网盘内容转存到个人阿里网盘，但是个人网盘容量太小，导致飞牛影视会卡在扫描怎么解决？` | 扫描小雅网盘会转存到个人网盘，容量不足会卡在扫描 | `sources/forum/tid-6046.md:33` |
| 6 | `直接挂载小雅小面的strm文件夹就可以，刮削的时候不会触发风控` | 只挂 strm 子目录，刮削不触发风控 | `sources/forum/tid-40446.md:161` |
| 7 | `挂个自动清理，不然看的时候也得手动清` | 建议挂自动清理，否则要手动清 | `sources/forum/tid-6046.md:71` |
| 8 | `手机在蜂窝网络上无法使用 NAS 内部域名` | 手机走蜂窝网络时用不了 NAS 内网地址 | `sources/forum/tid-73955.md:42` |
| 9 | `User-Agent: trim_player` | 该 UA 请求 CDN 临时链接返回 206（原帖称） | `sources/forum/tid-73955.md:39` |
| 10 | `Mozilla/5.0` | 换成该 UA 后同一链接返回 403（原帖称） | `sources/forum/tid-73955.md:40` |
| 11 | `CDN 链接不是任意播放器直接可用；请求头条件至少包含 UA。未证明是否还绑定 IP、Cookie 或其他条件。` | 原帖限定：只证明至少绑定 UA，未证明是否还绑 IP/Cookie | `sources/forum/tid-73955.md:40` |
| 12 | `总的来说小雅alsit并不是一个稳定的项目，依赖于阿里云盘，说不定哪天就给你封接口了；` | 社区风险提示：项目依赖阿里云盘，接口可能变动 | `sources/forum/tid-6046.md:156` |

---

# 第 7 章 运维与收尾

部署能播，只算做完了一半——小雅真正难的地方不是「装起来」，而是「养起来」。转存缓存会越堆越多、镜像会过期、网盘 token 会失效，这三件事不管，前面几章搭好的链路迟早在某天早上悄悄断掉。这一章是整篇笔记的最后一章，先把「长期维护要做的三件事」讲清楚，再给你一张收尾自检清单和一份诚实的「还没搞明白」清单。

## 7.1 为什么装完还得「养」

第 5、6 章反复提到小雅的运行机制：**你看什么，它就把什么转存到你自己的网盘**（转存一份临时副本，再用 302 直链喂给播放器，见 [[流媒体与影音/Strm流文件与302播放详解]]）。这个转存是临时的，而且——

> [!warning] 小雅默认不帮你删
> 转存进你网盘的文件，小雅**不会自动清理**。看得越多，你网盘里攒的临时文件越多：轻则占容量，重则触发网盘风控（第 6 章讲过的那种「扫描卡住 / 库变空」）。

> [!tip] 大白话
> 把转存想成**在图书馆借书**：看完就该还回去，但图书馆（网盘）默认不会自动帮你办归还。你得自己定个规矩定期还书——不然借书证（网盘容量）哪天就被借满、被冻结了。
> 所以：装完小雅，第一件长期要做的事就是「定期清理转存缓存」。

## 7.2 第一件事：转存缓存定期清理

清理转存不需要你自己写脚本，社区有现成工具。本笔记用的是 **xiaoyakeeper**：仓库自述它的定位是「一劳永逸的小雅转存清理工具」，并且说明「本仓库镜像备份了xiaoyakeeper，意旨提供稳定高效的服务」。它的容器镜像地址是 `ddsderek/xiaoyakeeper`。

它按「模式」区分行为，一键脚本用 `-s <模式号>` 指定（下面命令来自工具仓库，`-tg` 是可选的 Telegram 消息推送参数）：

```bash
# 在 NAS 的 SSH 终端里执行；-s 后面就是模式号
# 模式 3：建一个名为 xiaoyakeeper 的 Docker 定时容器，定时清理 + 定时升级小雅镜像
bash -c "$(curl -sLk https://xiaoyahelper.ddsrem.com/aliyun_clear.sh | tail -n +2)" -s 3 -tg
```

下面这张表把各模式的差别一次列清（逐条照仓库原文按行号核对，原文留档见文末对照表）：

| 模式 | 干什么 | 怎么选 |
|---|---|---|
| 模式 0 | 每天自动清理一次；系统重启后需要你手动重新跑，或把命令加进系统启动 | 想要「跑一次、以后自管」可用 |
| 模式 1 | 一次性清理，一般用来测试效果 | 只用来试跑一次 |
| 模式 2 | **已废弃，不再支持** | 别用 |
| 模式 3 | 创建一个叫 `xiaoyakeeper` 的 Docker 定时容器，定时清理转存并升级小雅镜像 | 推荐 |
| 模式 4 | 与模式 3 相同 | 同模式 3 |
| 模式 5 | 与模式 3 的区别是**实时清理**：产生播放缓存后一分钟内立即清掉；签到和定时升级同模式 3 | 想更省空间可选 |

> [!warning] 模式 2 别再照抄
> 网上不少旧教程还在写模式 2。工具仓库已经明确它是「已废弃，不再支持」——照抄会白折腾。选模式 3（定时）或模式 5（实时）即可。

几点实用补充（同样来自工具仓库）：

- **什么时候跑**：模式 0/3/4/5 的定时任务默认从「你运行脚本的下一分钟」开始，每天跑一次；也可以手动建一个 `/etc/xiaoya/myruntime.txt` 把时间改成比如 `06:00,18:00`（早晚各一次）。
- **它顺带做的事**：完成清理和签到后，脚本会执行 `/etc/xiaoya/mycmd.txt` 里的命令，默认内容就是**升级小雅镜像**；把该文件删掉则变成「定时重启小雅」。
- **签到**：脚本自带网盘签到，可以手动建 `/etc/xiaoya/mycheckintoken.txt`，每行放一个 32 位 `refresh token`；不建该文件就是默认给小雅转存所用的网盘签到。
- **想改就别改脚本本体**：仓库也说了「也可以把脚本下载下来自己魔改」，但它自己维护的定时/升级逻辑更稳，不建议动。

> [!tip] 大白话
> xiaoyakeeper 就像给 NAS 定了一个**自动打扫的闹钟**：模式 3 是「每天固定时间扫一次」，模式 5 是「脏了立刻扫」。你不用记着去还书，闹钟会替你办。

## 7.3 第二件事：怎么更新

小雅是持续更新的项目，镜像会不断出新版。两条路线的更新方式，和第 4 章部署时完全对应，**不要混着记**：

| 你当初的路线 | 更新怎么做 | 出处 |
|---|---|---|
| 官方镜像 `xiaoyaliu/alist` | 重跑「一键安装和更新容器」脚本 | `sources/01_hub_docker_com.md:16` |
| 社区镜像 `ghcr.io/monlor/xiaoya-alist` | 重跑 monlor 的一键脚本（仓库说明「脚本支持重复执行」） | `sources/p2/monlor-144.md:29,32` |

```bash
# 官方路线：一键安装和更新容器
bash -c "$(curl -s http://docker.xiaoya.pro/update_new.sh)"

# 社区 monlor 路线：重复执行部署脚本即等于更新（会自动覆盖 compose 文件，但不覆盖 env 文件）
# 出处：sources/p2/monlor-144.md:32
bash -c "$(curl -fsSL https://raw.githubusercontent.com/monlor/docker-xiaoya/main/install.sh)"
```

官方镜像还有一个省事的地方：**重启就会自动更新数据库及搜索索引文件**，对应命令是 `docker restart xiaoya`（`sources/01_hub_docker_com.md:19`）。也就是说官方路线的基础数据不一定靠「更新镜像」，重启一次也常能刷新索引。

> [!warning] 更新前先看第 4 章的镜像名纪律
> 官方镜像是 `xiaoyaliu/alist`，社区镜像是 `ghcr.io/monlor/xiaoya-alist`（后者是 monlor 的社区镜像，**不是官方**）。更新脚本要和当初部署用的镜像对上，别拿 A 路的脚本去更新 B 路的容器。

> [!tip] 大白话
> 更新就像**给手机升系统**：官方路线是「跑一下官方升级包」，社区路线是「重跑一遍安装脚本（它自带更新）」；而自动重启刷新索引，相当于重启一下手机让新设置生效。

## 7.4 第三件事：这套东西要多少硬件

很多新人卡在「我的 NAS 够不够」。monlor 项目给了一张部署配置推荐表，其中有单容器方案：「仅部署 Alist」推荐 **CPU 1 核 / 内存 512M / 硬盘 512M**（`sources/p2/monlor-144.md:78`）。

> [!warning] 这是「维护者推荐」，不是官方硬性门槛
> 上表出自 monlor 项目文档，是**维护者给的推荐值**，不是任何官方标准，也不是「低于它就一定跑不动」。实际能不能跑，还取决于你的并发、是否挂前端、网盘速度等。

作为对照，这张表里更重的方案是这样的（同一个表，逐行核对过）：

| 方案 | CPU | 内存 | 硬盘 |
|---|---|---|---|
| 仅部署 Alist | 1 核 | 512M | 512M |
| Alist+Emby | 2 核 | 4G | 150G |
| Alist+Emby+Jellyfin | 2 核 | 4G | 200G |
| Alist+Jellyfin | 2 核 | 4G | 150G |

怎么读这张表：**只做「资源层」（单容器 AList + 在线播放 + WebDAV）非常轻**，1 核 512M 就够了；一旦把 Emby / Jellyfin 这类「媒体服务器」也算进来（它们要下载元数据、建库、做转码），CPU 和硬盘就跳一个档次。本笔记主推的「小雅 + 飞牛影视」属于前者+一个轻前端，比全家桶省得多。

> [!tip] 大白话
> 这张表像装修前的**「最小户型建议」**：一个人住，「一室一厅」就够（单容器）；非要塞下一大家子还要影音室、书房（Emby+Jellyfin），那就得换大房子。它是参考，不是硬性规定。

## 7.5 收尾自检：回到最开始的两个问题

现在整篇笔记读完了，回头检验一下——最初那两问，你能自己答上来了吗？

| 你的原始问题 | 现在应该能给出的答案 | 在哪一章 |
|---|---|---|
| ① 不用 Emby，能用飞牛影视当前端吗？ | 能。用 SmartStrm 生成 STRM，再用 MediaWarp（FNTV 类型）或 fntv-proxy 修好 302 与外网可达，飞牛影视只扫 STRM 子目录即可 | 第 5 章 |
| ①-a 刮削差异 | 飞牛影视直接扫整个小雅会触发转存/风控，只能挂已生成的 STRM 子目录；Emby 全家桶则自带专门的元数据服务 | 第 5、6 章 |
| ①-b 播放差异 | STRM 只存 URL 指针，302 直链让流量不过媒体服务器；但飞牛原生直链默认是内网地址，外网要额外处理 | 第 5、6 章 |
| ①-c 外网差异 | 手机在蜂窝网络下无法解析 NAS 内网域名；需要公网入口或代理端口 | 第 6 章 |
| ② 单容器部署步骤 | 官方镜像 `docker run` 或社区 monlor 的 compose，二选一；装完跑一次转存清理、验一次播放链路 | 第 3、4 章 |

如果上面每一行你都能不看笔记自己复述，这套「小雅 + 飞牛影视」你就真正跑通了。

## 7.6 老实说：这些还没搞明白

一篇负责任的笔记，也要把**证据不足、悬而未决**的地方标出来，避免把「传闻」当「结论」。以下几项在整篇笔记里一律**没有**写成结论：

| 未决项 | 目前证据到什么程度 | 本笔记怎么处理 |
|---|---|---|
| `ghcr.io` 有没有「官方」小雅镜像 | 没有。`ghcr.io/monlor/xiaoya-alist` 是 monlor 的镜像 | 全文按「社区路线」写，不叫它官方镜像 |
| `xiaoya.host` 是不是官方域名 | 未证，只有社区链路描述 | 只当作「内网地址」的举例，不宣称官方 |
| 飞牛影视从哪个版本开始支持 STRM | 来源冲突，未定 | 不写「起始版本号」这种硬结论 |
| `/data` 凭据文件名与目录 | 文件名三件套已证；但目录随路线（`/data` 或 `/etc/xiaoya`） | 第 3 章按「文件名已证、目录随路线」写 |
| MediaWarp 与 fntv-proxy 能否共存 / 版本矩阵 | 无来源 | 只作并列介绍，不写「可以共存」 |
| 知乎《用飞牛影视连接小雅，可行吗？》、官方 Notion 配置指南 | 均未获取（crawler 被拦 / SPA 壳页） | 未作为证据、未引用 |
| 「半分钟几个 T」的转存量级 | 原帖确有该说法，但属模糊定性、无精确值 | 只作「原帖称」引用，不当精确数据 |

> [!warning] 别把上表读成「结论」
> 这七行是**不确定清单**，不是答案。遇到二手教程把其中任何一条讲成板上钉钉时，请回到「有没有可核查的来源」这一步再判断。

## 本章小结

- **装完要养**：小雅默认不清理转存缓存，必须自己安排定期清理，否则占容量、还可能触发风控。
- **清理工具**：xiaoyakeeper（镜像 `ddsderek/xiaoyakeeper`）；模式 3 定时、模式 5 实时是推荐项，**模式 2 已废弃**；它还能顺带定时升级镜像和网盘签到。
- **更新口径**：官方路线重跑一键脚本、社区 monlor 路线重跑其安装脚本（可重复执行）；官方镜像重启即可自动更新数据库与索引。
- **硬件参考**：单容器「仅部署 Alist」维护者推荐 1 核 / 512M / 512M，属**推荐非硬性**；加 Emby/Jellyfin 会跳档。
- **诚实的收尾**：两问已有完整答案（见 7.5），同时有七项仍属未决，笔记里一律不做结论。

> 最后一句：技术方案会变（版本、域名、镜像都会更新），但这套「资源层（AList）+ 前端层（飞牛影视/Emby）+ 中间件（STRM/302）」的分层心智不会过时。以后哪一环出问题，你都能按这个骨架定位到是哪一层，再回对应章节找答案。想了解「网盘影视播放 vs 本地存储」的取舍，可继续读 [[流媒体与影音/网盘影视播放与本地存储的取舍]]。

## 引文对照（原文 / 中译 / 出处）

下表留档本章引用过的原文逐字片段。出处列中的 `—` 表示该片段无可回指的来源文件；行号指对应 `sources/` 快照文件中的行。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
|---|---|---|---|
| 1 | 一劳永逸的小雅转存清理工具 | 工具自述定位：装一次、长期自动清理 | sources/01_github_com.md:32 |
| 2 | 本仓库镜像备份了xiaoyakeeper，意旨提供稳定高效的服务 | 这是该工具的一个镜像备份仓库 | sources/01_github_com.md:33 |
| 3 | 已废弃，不再支持 | 模式 2 已作废，别再照抄 | sources/01_github_com.md:47 |
| 4 | 创建一个名为 xiaoyakeeper 的docker定时运行小雅转存清理并升级小雅镜像 | 模式 3：建一个定时容器，清理并升级 | sources/01_github_com.md:48 |
| 5 | 与模式3的区别是实时清理，只要产生了播放缓存一分钟内立即清理 | 模式 5 相比模式 3，改成了实时清理 | sources/01_github_com.md:55 |
| 6 | 请勿将 xiaoyahelper 用于商业用途 | 该工具明确不得商用 | sources/01_github_com.md:82 |
| 7 | 仅部署 Alist | 单容器方案行；对应推荐 1 核 / 512M / 512M | sources/p2/monlor-144.md:78 |
| 8 | 脚本支持重复执行 | monlor 安装脚本可反复跑，等于更新 | sources/p2/monlor-144.md:29 |
| 9 | 一键安装和更新容器 | 官方镜像的安装与更新是同一个脚本 | sources/01_hub_docker_com.md:16 |
| 10 | 重启就会自动更新数据库及搜索索引文件 | 官方路线重启即刷新索引 | sources/01_hub_docker_com.md:19 |
| 11 | 此脚本仅限发烧友使用，需要有一定的解决问题能力 | monlor 的测试版脚本只建议有排障能力的人用 | sources/p2/monlor-144.md:67 |
