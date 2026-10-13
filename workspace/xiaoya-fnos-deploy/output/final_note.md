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

拆开这句看两层意思：**资源在哪**——在网盘上，由维护者持续更新，你不用自己找片；**你怎么拿到**——通过一个叫 AList 的程序把它变成一个能访问的服务。**提醒一句**：上面那句把它概括成「基于阿里云盘」，但这几年已经变了——小雅的资源现在分**本体库**（在**阿里云盘与 115 网盘**）和**分享区**（另有**夸克**、PikPak 等）两块，详见第 5 章 5.6。

所以「小雅」不是一个播放器，它更像一个**片源仓库**：它负责「有什么片、片在哪」，至于海报墙怎么排、点了之后怎么播，是另一层的事。这一层由 AList 承担——官方镜像页把「端口：5678 访问： `http://xxxxx:5678/`」与「webdav 账号密码 用户: guest 密码: guest_Api789」**并列**给出（`sources/01_hub_docker_com.md:17`、`:18`），正说明资源层对外提供**网页访问**与 **WebDAV 挂载**两条取用通道。

> [!tip] 大白话
> 把「资源层」想成**仓库**：仓库里堆满了别人的片子，你去仓库能拿到货（播放链接）。但仓库本身不负责「放映」——它不排片单、不做海报墙、不放电影。所以「小雅」两个字，指的是仓库，不是放映厅。

## 1.2 你的两个问题，先给简答

本篇是从你提出的两个问题长出来的，这里先各给一句结论，细节分别落在第 2 章和第 3–5 章。

**问题一（选型）：不想用 Emby，直接用飞牛影视行不行？**
结论：**行，不必须 Emby**。在我们检索到的所有来源里，**没有任何一处**断言「小雅必须配 Emby」；而且已经有社区实践走的是「全家桶去掉 Emby」——发帖者原话是：「部署 小雅的全家桶 除了emby，用刮削好的 strm文件，完美适配」（`sources/forum/tid-73955.md:32`）。也就是说，飞牛影视当播放端这条路，既有官方工具的旁证，也有真实用户在跑。第 2 章会把「能不能替代」拆成四个维度逐项对比。

**问题二（部署）：单容器方案具体怎么部署？**
结论：**只装资源层（仅 AList）就是单容器**，本笔记用的整合脚本把「只装小雅 Alist」和「装 Emby 全家桶」列成了两个不同的菜单项（`sources/01_raw_githubusercontent_com.md:75-76`），说明「只装 Alist」是脚本明确支持的独立装法。具体命令集中在第 4 章，第 3 章先备清单。

## 1.3 先立一个比喻：资源层是仓库，播放层是电视

要理解「为什么可以不用 Emby」，得先把这套系统分成两层。这个分层是理解全篇的钥匙：

| 层 | 谁承担 | 决定什么 | 具体产物 |
| --- | --- | --- | --- |
| **资源层** | 小雅（以 AList 为载体） | 「有什么片」 | 一份持续更新的网盘影视目录 + 在线播放 + WebDAV 挂载 |
| **播放层** | 飞牛影视 / Emby / Jellyfin | 「怎么看」 | 海报墙、元数据刮削、播放器、外网访问入口 |

两层的分工，从来源措辞上能看得更清楚。AList 那层对外给的是网页访问与 WebDAV（`sources/01_hub_docker_com.md:17-18`）；而 Emby 那层，看**服务它们的周边工具**怎么措辞就明白了——「MediaWarp 是**前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器**」（`sources/lens-b/mediawarp/01_github_com.md:51`）：把 Emby、Jellyfin、**飞牛影视**三者并列成同一类对待。换句话说，这三者在架构里是同一个位置——**播放层**。

**这个分层解释了你最关心的问题：** 既然「怎么看」是一层，而播放层不是只有 Emby 一家（飞牛影视、Jellyfin 干的是同一类事），那么「不想用 Emby」就是**换一个播放层**，而不是放弃整个方案——仓库照旧，只换电视。

> [!tip] 大白话
> 把资源层想成**仓库**、播放层想成**电视**：仓库决定「有什么片」，电视决定「怎么看」（有没有海报墙、能不能刮削出简介、外网点开卡不卡）。你不想用 Emby，本质是「换台电视」，不是「不要仓库」。仓库和小雅没关系的那部分——片源在网盘上——一点都没变。

这套「资源在网盘、不落本地」的取舍，我在同域笔记 [[流媒体与影音/网盘影视播放与本地存储的取舍]] 里展开过，想先补背景的读者可以先读那篇；本章只需要记住：**小雅解决的是「片源从哪来」，不解决「怎么放」。**

## 1.4 名词扫盲表

后面几章会反复出现下面这些词，第一次见就到这张表里查一眼：

| 名词 | 一句话大白话 | 在本篇里的角色 |
| --- | --- | --- |
| **小雅** | 一套基于网盘（阿里 / 115，另有夸克等分享区）的影视聚合方案，维护着持续更新的资源目录 | 本篇的「资源层」主体 |
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

本篇标题里的「纯净版」，**不是官方术语**。在我们核对过的来源（本笔记用的整合脚本仓库、官方镜像页等）里，**都没有出现过「纯净版」这个词**。它在社区里约定俗成地指「只装小雅 Alist、不装 Emby 全家桶」的那套轻量装法，在脚本菜单里对应的是这一项：

> 「安装 小雅Alist -> 1 1」（`sources/01_raw_githubusercontent_com.md:75`）

而它旁边紧挨着的另一项就是「安装 Emby全家桶（一键） -> 2 1」（`sources/01_raw_githubusercontent_com.md:76`）——两个是**不同的菜单项**，这正是「只装 AList 是脚本明确支持的独立装法」的依据。

> [!warning] 别把「纯净版」当成官方产品名
> 「纯净版」是**社区叫法，非官方术语**。你去搜索时，整合脚本的 README 里对应的是「安装 小雅Alist」这一菜单项。记住这一点，可以避免把社区黑话当成官方说法去问、去找，结果找不到。

> [!note] 术语校正：这套笔记里的「官方」指什么
> 本篇会用「官方」这个词，先把它钉死，免得后面几章越读越糊：
> - **官方**：镜像 `xiaoyaliu/alist`，作者 `xiaoyaliu`，内容源 `alist.xiaoya.pro`（`sources/01_hub_docker_com.md:8`、`:10`）。
> - **本笔记用的**：`xiaoyaDev/xiaoya-alist`，是一个**社区整合脚本**项目（作者 DDSRem）——README 自称「整合安装脚本，内置所有相关软件的安装」（`sources/01_raw_githubusercontent_com.md:33-34`）。它内部**使用的正是上面那个官方镜像**（`sources/xiaoyaDev/all_in_one.sh:1376`）。
>
> 所以本笔记的路线是「**社区整合脚本 + 官方镜像**」。之后找文档、报问题时请分清这两层——去整合脚本项目里问镜像的事，或去官方文档里找菜单的事，都会扑空。

## 1.6 这篇怎么读：全文路线图

全篇 7 章，顺序是「先判断、再动手、后收口」，你可以按需跳读：

| 章节 | 类型 | 你要做的事 | 大概耗时 |
| --- | --- | --- | --- |
| **第 1–2 章** | 判断 | 决定要不要用 Emby、最终选哪条路线 | 约 30 分钟 |
| **第 3–5 章** | 动手 | 备清单 → 单容器部署 → 飞牛影视接入 | 约 30–60 分钟 |
| **第 6–7 章** | 收口 | 遇到问题回查避坑清单；做长期运维（清理转存缓存） | 约 20 分钟 |

如果你只是想「先把部署跑通」，核心路径是**第 3 → 4 → 5 章**；第 1、2 章是给还在犹豫「到底要不要 Emby」的读者判断用的。命令与解释是分开的：每章的解释走正文，完整的命令片段集中在各章的「动手实践」小节，不熟悉命令的读者可以先跳过命令、只读解释。

## 本章小结

- **小雅 = 资源层（仓库），不是播放器**：它把网盘（阿里 / 115，另有夸克等分享区）上持续更新的影视目录聚合成可访问的服务，负责「有什么片」，不负责「怎么看」。
- **你不必用 Emby**：所有来源里没有任何一处断言「必须 Emby」，且已有「全家桶去掉 Emby」的真实社区实践。
- **单容器 = 只装资源层**：整合脚本把「安装 小雅Alist」与「安装 Emby全家桶（一键）」列为不同菜单项，只装 Alist 是脚本明确支持的装法。
- **分层是理解全篇的钥匙**：资源层（小雅/AList）× 播放层（飞牛影视/Emby），换播放端不影响片源，所以「不想用 Emby」是换电视、不是丢仓库。
- **「纯净版」是社区叫法、非官方术语**，脚本语义约等于菜单里的「安装 小雅Alist」。
- **「官方」= 镜像 `xiaoyaliu/alist`**；本笔记用的 `xiaoyaDev/xiaoya-alist` 是**社区整合脚本**，它内部用的才是官方镜像——两层别混。

**下一章预告**：既然「不必须 Emby」，那飞牛影视到底靠不靠谱？第 2 章把两种方案在**刮削与元数据、播放链路、播放兼容性、外网可达性**四个维度上逐项摊开对比，并补一张「单容器 vs 全家桶」的资源门槛表，最后落到适合你这种「已有飞牛影视、不想装 Emby」场景的选型建议。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。本章的原始来源以中文为主，故「中译」列对中文原文给的是**说人话**的复述；出现英文片段时给出中译。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `小雅 Alist 是基于阿里云盘的影视聚合方案，维护着一份持续更新的影音资源目录，省去了自己找片、管片的麻烦。` | 小雅是一套基于阿里云盘的影视聚合方案，帮你不自己找片 | `sources/p2/newzone-xiaoya.md:10` |
| 2 | `端口：5678 访问： http://xxxxx:5678/ （xxxx 为你alist所在设备的 IP）` | 资源层对外提供网页访问（端口 5678） | `sources/01_hub_docker_com.md:17` |
| 3 | `webdav 账号密码 用户: guest 密码: guest_Api789` | 资源层对外提供的第二条通道：WebDAV | `sources/01_hub_docker_com.md:18` |
| 4 | `MediaWarp 是**前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器** ，修改了原媒体服务器返回响应以实现特殊功能` | Emby / Jellyfin / 飞牛影视 被并列成同一类，即「播放层」 | `sources/lens-b/mediawarp/01_github_com.md:51` |
| 5 | `By [xiaoyaliu](https://hub.docker.com/u/xiaoyaliu)` | 官方镜像作者栏署名 `xiaoyaliu` | `sources/01_hub_docker_com.md:8` |
| 6 | `我把 alist.xiaoya.pro 的内容，内嵌在容器里发布了，并添加了alist本身没有的搜索功能。` | 官方镜像作者自述：内容来自 `alist.xiaoya.pro` | `sources/01_hub_docker_com.md:10` |
| 7 | `整合安装脚本，内置所有相关软件的安装。` | 整合脚本自述：它把相关软件都包进来了 | `sources/01_raw_githubusercontent_com.md:33-34` |
| 8 | `xiaoyaliu/alist:latest` | 整合脚本内部使用的官方镜像 | `sources/xiaoyaDev/all_in_one.sh:1376` |
| 9 | `部署 小雅的全家桶 除了emby` | 装了全家桶但把 Emby 去掉 | `sources/forum/tid-73955.md:32` |
| 10 | `安装 小雅Alist -> 1 1` | 安装脚本里「只装小雅 Alist」这一项 | `sources/01_raw_githubusercontent_com.md:75` |
| 11 | `安装 Emby全家桶（一键） -> 2 1` | 安装脚本里「装 Emby 全家桶」这一项 | `sources/01_raw_githubusercontent_com.md:76` |
| 12 | `strm 只是 URL 指针` | STRM 文件只存一个 URL 指针，本身不是视频 | `sources/lens-b/fntvproxy/01_github_com.md:266` |
| 13 | `Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器` | STRM 能实现 302 直链播放，流量不经过媒体服务器 | `sources/lens-b/mediawarp/01_github_com.md:53` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线换为 xiaoyaDev/xiaoya-alist（DDSRem）整合脚本，并补「整合脚本 ≠ 官方」术语校正（第 1 篇）**。1.1 与 1.3 的「资源层 / 播放层」描述不再挂 monlor README 的组件注释，改为回源官方镜像页（`01_hub_docker_com.md:17-18`：网页访问与 WebDAV 两条通道）与 MediaWarp README（`lens-b/mediawarp/01_github_com.md:51`：Emby / Jellyfin / 飞牛影视 三者被并列）。1.2、1.5、本章小结中「官方安装脚本 / 官方承认的独立装法」等措辞修正为「整合脚本 / 脚本明确支持的装法」。1.5 新增 `[!note]`「术语校正：这套笔记里的『官方』指什么」：官方＝镜像 `xiaoyaliu/alist`（`01_hub_docker_com.md:8`、`:10`），本笔记用的是社区整合脚本，它内部才是官方镜像（`all_in_one.sh:1376`）。本章小结由五条增为六条。引文对照重编为 13 条（新增镜像页 3 条、README 与 `all_in_one.sh` 2 条，删除 monlor 组件注释 2 条），表头补全「出处」列。 |
| 2026-10-06 | **整套笔记统一为 monlor 单一路线，删除官方镜像路线（第 4 篇）**：删去 1.1 中「小雅官方镜像的作者自述」引文及其引导句（`sources/01_hub_docker_com.md:10`）；1.5 的「官方来源（官方镜像页、官方脚本仓库）」收窄为「官方来源（官方脚本仓库等）」，warning 里删去「或直接运行官方镜像 `xiaoyaliu/alist`」一句。引文对照删去官方镜像页 1 条（原第 2 行），重编号为 1–8。 |
---

# 第 2 章 选型对比——飞牛影视能不能替代 Emby

## 本章要解决的问题

结论先行：**不必须用 Emby**。我们检索到的全部来源里，**没有任何一处**断言「小雅必须配 Emby」；相反，已经有人实打实地跑着「全家桶去掉 Emby」的方案。但这不等于两者没差别——本章会把两种播放端在**刮削与元数据、播放链路、播放兼容性、外网可达性**四个维度上逐项摊开，再补一张「单容器 vs 全家桶」的门槛对比，最后落到适合你的选型建议。

本章的对比对象只有两个：**路线 E**（Emby 全家桶：AList + 元数据服务 + Emby）和**路线 F**（单容器：仅 AList + 飞牛影视作前端）。读完你应该能自己回答：我这台机器、我这些片源习惯，到底该走哪条。

## 2.1 结论先行：没有任何来源说「必须 Emby」

先把最大的疑虑打消。社区里已经有明确走「不用 Emby」这条路的帖子，发帖者原话是：

> 「我把 xiaoyaemby 刮削好的 strm 文件放到飞牛影音里，这样既不占用 nas 空间，也不用科学版本的 emby，搜索更友好，使用起来更舒适……部署 小雅的全家桶 除了emby，用刮削好的 strm文件，完美适配」（`sources/forum/tid-73955.md:32`）

这位用户的做法有三点值得注意：他把「Emby 刮削好的 STRM」直接喂给**飞牛影音**（fnOS 的影视应用）；他明确「不用 Emby」；他评价「完美适配」。这至少说明：飞牛影视作为播放端，**不是不能替代 Emby**。

至于「能不能全量替代、有没有短板」，就是下面四个维度要回答的事。

## 2.2 两条路线分别是什么

对比之前，先把两条路线的组成摆出来。两条都出自**同一个整合脚本**的菜单——区别只在于你选哪一项。

**路线 E（Emby 全家桶）**，菜单项叫「安装 Emby全家桶（一键） -> 2 1」（`sources/01_raw_githubusercontent_com.md:76`）。它装的不止一个容器：菜单里另有一整段「Emby手动全家桶配置」（`sources/01_raw_githubusercontent_com.md:89`）。各组件分工是：

- **Alist（资源层）**：对外提供网页访问与 WebDAV 两条取用通道（`sources/01_hub_docker_com.md:17-18`）。
- **元数据服务**：脚本把元数据单列成可独立安装的组件——「安装 小雅元数据定时爬虫 -> `2 5 1`」（`sources/01_raw_githubusercontent_com.md:77`）、「安装 小雅元数据爬虫（Web 版本）-> `2 6 1`」（`:78`），并提供整套现成元数据包：「单独 下载并解压 全部元数据 -> `2 2 1`」（`:90`）。
- **Emby（播放层）**：脚本里被重点照料的独立组件——「单独 安装Emby（可选择版本，支持官方，amilys，lovechen）-> `2 3`」（`:109`）、「图形化编辑 emby_config.txt -> `2 4`」（`:110`）、「一键升级Emby容器（可选择镜像版本） -> `2 7`」（`:115`）、「关闭 Emby 6908 端口访问 -> `2 9 2`」（`:118`）。

**路线 F（单容器 + 飞牛影视）**，就是只装资源层（AList）那一项——菜单项叫「安装 小雅Alist -> 1 1」（`sources/01_raw_githubusercontent_com.md:75`），播放/刮削交给 fnOS 自带的飞牛影视。

两条路线的差别可以一句话记住：**E 是「资源层 + 自带播放层 + 自带元数据服务」的全家桶；F 是「只装资源层，播放层用你已有的飞牛影视」。**

> [!tip] 大白话
> 把两条路线想成**买整机 vs 自己配一台**：路线 E 是厂商配好的「主机 + 显示器 + 音响」套装，插电即用，但占地方、贵；路线 F 是「只要你已有的显示器和音响，再自己接一个机顶盒」。你的机器上**本来就有飞牛影视**（相当于已有显示器），所以路线 F 才是「不浪费已有东西」的那种。

## 2.3 四个维度逐项对比

先给总表，再逐项展开差异与依据：

| 维度 | 路线 E（Emby 全家桶） | 路线 F（单容器 + 飞牛影视） |
| --- | --- | --- |
| **刮削与元数据来源** | 配套**元数据爬虫**容器管元数据；脚本还提供整套现成元数据包下载 | 让飞牛影视自己刮，或复用 Emby 侧刮好的 STRM |
| **播放链路** | 播放层与 AList 同栈部署，Emby 代理走 `:8095` | 需把播放地址指向飞牛代理端口 `:28005` |
| **播放兼容性** | 成熟播放器生态；Emby 硬解要**手动开启**（脚本的可选参数） | 支持 `stream.mp4`/`stream.MOV` 等；AlistStrm 模式下支持网盘转码内容 |
| **外网 / 蜂窝网可达性** | 同样要解决内网直链问题（代理改 302） | 关键坑同左：飞牛原生响应里的直链仍是内网地址 |

### 2.3.1 刮削与元数据来源

路线 E 的元数据是「配套供给」的：脚本把元数据单列成组件（元数据定时爬虫 `2 5 1`、Web 版爬虫 `2 6 1`，`sources/01_raw_githubusercontent_com.md:77-78`），并列了一长串「单独 下载并解压 全部元数据」「解压 `115.mp4` 的指定元数据目录」「单独 下载 json.mp4」之类的手动元数据项（`sources/01_raw_githubusercontent_com.md:90-107`）。也就是说，Emby 路线有一套**现成的元数据宝库**，装完就有海报墙。

路线 F 的元数据来源则有两种做法，都来自那位「不用 Emby」的用户：一是把已经用 Emby 刮好的 STRM 直接搬进飞牛影视（「我把 xiaoyaemby 刮削好的 strm 文件放到飞牛影音里」），二是让飞牛影视自己按需刮削（「想刮削那个就刮削那个」）（`sources/forum/tid-73955.md:32`）。

**差异落点**：Emby 路线胜在「开箱有元数据包」；飞牛影视路线要自己解决刮削来源——要么复用 Emby 的刮削产物，要么靠飞牛影视自己刮。这是两条路线**最实际的差别**，但它不是「能不能用」的问题，而是「元数据从哪来」的问题。

### 2.3.2 播放链路

两条路线在底层其实共用同一套机制：**STRM + 302 直链**——`Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器`（`sources/lens-b/mediawarp/01_github_com.md:53`）。STRM 本身只是个 URL 指针（`strm 只是 URL 指针`，`sources/lens-b/fntvproxy/01_github_com.md:266`），真正决定能不能播的是那一步 302 重定向。

差别在**谁来扮演那个代理端口**：Emby 路线的代理默认走 Emby 端口；飞牛影视路线则不同，客户端要连的是飞牛这一侧的入口——`将播放器地址指向代理端口（飞牛 :28005，Emby :8095）`（`sources/lens-b/fntvproxy/01_github_com.md:71`）。

这条链路的具体原理（STRM 怎么生成、302 怎么改）是第 5 章的主线，想先深入可读同域笔记 [[流媒体与影音/Strm流文件与302播放详解]]。

### 2.3.3 播放兼容性

飞牛影视作为播放端，第三方工具的实测给它提供了旁证：代理工具明确「基于**飞牛影视 0.9.3** 版本」（`sources/lens-b/fntvproxy/01_github_com.md:45`），并在问答里说明「飞牛代理支持 `stream.mp4`、`stream.MOV` 等所有格式」（`sources/lens-b/fntvproxy/01_github_com.md:281`）。

硬解这一项，新路线是**「可选，但要手动开」**：脚本在装 Emby 时提示「如果需要开启Emby硬件转码请先返回主菜单开启容器运行额外参数添加 -> `72`」（`sources/xiaoyaDev/all_in_one.sh:3479`）——也就是说，**默认不开**，要硬解得先去菜单里打开「容器运行额外参数添加」（状态项见 `sources/xiaoyaDev/all_in_one.sh:6061`），再填设备参数；脚本给 Intel 核显/独显的默认值是 `--device /dev/dri:/dev/dri --privileged -e GIDLIST=0,0 -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all`（`sources/xiaoyaDev/all_in_one.sh:3485`）。

飞牛影视侧则不同——**MediaWarp 已完成对飞牛影视的适配**，并且在 **AlistStrm 模式**下支持播放网盘转码内容（待办清单里这两项均为 `[x]`：`sources/lens-b/mediawarp/02_readme_todo.md:23`、`:24`）。

> [!note] 一条旧结论已作废：不再说「全家桶不支持硬解」
> 本笔记早期版本的这一节写着「脚本没有计划支持硬解」——那是从一条**已停更**的旧路线文档里引来的。按现在这条主线，脚本的措辞正相反：Emby 硬解是**可选功能**，只是需要你手动打开容器额外参数（`sources/xiaoyaDev/all_in_one.sh:3479`）。旧说法已随旧路线一并撤下（见文末更新记录）。

硬解与软解的取舍另有专文，延伸阅读见 [[流媒体与影音/硬件解码vs软件解码]]。

### 2.3.4 外网 / 蜂窝网可达性

这是两条路线**共同的坑**，也是最容易让「局域网能放、出门就播不动」的地方。帖子里记录得很直白：

> 「飞牛服务端通过原 STRM 能探测、读取片段，但飞牛原生 /stream 响应里的直链仍是内网地址（`xiaoya.host:5678`）。手机在蜂窝网络上无法使用 NAS 内部域名」（`sources/forum/tid-73955.md:42`）

也就是说，**原生飞牛影视对 302 直链 / 内网地址的处理不完善**，出门用手机看会卡在「解析不了内网域名」这一步。解法是加一层代理把内网地址改掉/转发——第 5 章会给具体做法（MediaWarp 或 fntv-proxy 二选一）。这一点对**两条路线同样成立**，不构成 Emby 与飞牛影视的优劣差，而是「有没有修 302」的差。

**在外网远程观影（用 5G 或公司网络看飞牛影视）**

- **注意陷阱：** 飞牛影视后台的「网盘优先使用直链播放（302）」开关，**目前主要针对飞牛「原生挂载」的网盘**；而小雅是走 **WebDAV 协议**挂进来的，飞牛系统把它当成一块**普通网络硬盘**——所以**通常套不上 302 直链**。
- **实际流向：** 外网播放时，视频流一般是「**NAS 先连网盘拉流 → NAS 再把流上传中转给外网的手机**」。于是流畅度受限于你家的**上行带宽**（或飞牛 Connect 穿透通道的带宽），这跟「网盘自己限不限速」是两回事。

两条播放路径的流量走法完全不同，别混为一谈：

| 播放路径 | 文件从哪来 | 流量经过 NAS 吗 | 瓶颈在哪 |
| --- | --- | --- | --- |
| **直接挂载（WebDAV）** | NAS 连网盘拉流，再上传给客户端 | **经过**（NAS 中转） | 家里**上行带宽** / 飞牛 Connect 通道 |
| **STRM + 302**（第 5 章主线） | 客户端直连网盘真实直链 | **不经过**（`sources/lens-b/mediawarp/01_github_com.md:53`） | 公网出口 + 网盘限速 |

> [!tip] 大白话
> 把「内网地址」想成**家里的门牌号**：在家（局域网）路熟，门牌 `xiaoya.host:5678` 找得到；一出小区、上了蜂窝网就不认了。要在外网也能看，有两条路——**要么在小区门口立一块公共指示牌**（代理把「小区门牌」换成公网可达地址：这是第 5 章的 302 路线，**片子不经过你家**）；**要么自己来回跑腿转寄**（WebDAV 直接挂载：NAS 先把片拉回来、再转寄给外网的你，**每一趟都占你家的上行**）。

**一句话**：想「外网流畅、又不占家里上行」，正解是把播放切到**第 5 章的 STRM + 302**；WebDAV 直接挂载省事，代价就是长期吃你家上行带宽。

## 2.4 单容器 vs 全家桶：为什么可以不用 Emby（要装多少东西）

除了功能，还有一个很硬的选型因素：**你这台机器上要多跑几个容器**。这一节用「要装的组件数量」当尺子——因为它最容易回源、也最直观。菜单里两条路线要碰的东西摆在一起看：

| 维度 | 路线 E（Emby 全家桶） | 路线 F（单容器） | 出处 |
| --- | --- | --- | --- |
| **要装的容器** | Alist + **Emby** + **元数据爬虫**（可另装定时版 / Web 版） | 只有 Alist 一个 | `sources/01_raw_githubusercontent_com.md:75-78` |
| **要下的数据** | 另有整套「元数据包」要下载并解压（`2 2 1` 等十余个手动项） | 无 | `sources/01_raw_githubusercontent_com.md:90-107` |
| **谁负责刮削** | 脚本自带的元数据服务 | 飞牛影视自己刮，或复用 Emby 产物 | `sources/01_raw_githubusercontent_com.md:77-78`；`sources/forum/tid-73955.md:32` |
| **镜像本体** | — | 官方镜像在 Docker Hub 上标 22 MB | `sources/01_hub_docker_com.md:30` |

看这张表就很清楚：**路线 F 只有一个容器**；路线 E 除了 Emby 本体，还要多养一个（或两个）元数据爬虫容器、再下载解压一整套元数据包。多出来的每一个组件，都要占内存、占硬盘、多一份要维护的东西——这正是「不想用 Emby」除了功能偏好之外的另一个现实理由。

> [!warning] 本笔记不给具体 CPU / 内存数字
> 你可能会在别处看到「仅 AList 1 核 / 512M / 512M，加 Emby 变 2 核 / 4G / 150G」这类表格。**本笔记不采用**——那个数字出自一条**已经停更**的旧路线文档，随项目一起撤下了（见文末更新记录）。在这里能给的、可回源的，是上面那张「**要装几个组件、要不要下元数据包**」的对照；具体多少内存够用，请按你实际要装的组件 × 各自官方文档的说明估算，不要照抄一个来路不明的数字。

**这张表是「为什么可以不用 Emby」最直接的反衬**：你说不想用 Emby，除了功能偏好，往往还因为**不想为一个播放层多养元数据爬虫、多下整套元数据包**——而单容器（仅 AList）恰好把这件事压到「一个容器」。

## 2.5 飞牛影视可作前端的旁证

**正面旁证**（说明飞牛影视确实被当成正经播放端对待）：

- MediaWarp 的自我定位是「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」（`sources/lens-b/mediawarp/01_github_com.md:51`）——把飞牛影视和 Emby、Jellyfin 并列在同一位；其待办清单里 **`- [x] 适配 飞牛影视`** 为**已完成**（`sources/lens-b/mediawarp/02_readme_todo.md:23`）。
- fntv-proxy 直接「基于飞牛影视 0.9.3 版本」开发（`sources/lens-b/fntvproxy/01_github_com.md:45`）。

> [!note] 一处旧结论的更正：MediaWarp 对飞牛影视**已经支持**
> 本笔记早前把 README 待办清单里的「适配 飞牛影视」读成**待办项**，据此判断「成熟度未决」。核对 raw Markdown 后确认，该行原文是 **`- [x] 适配 飞牛影视`（已完成）**，紧随的 `- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` 也已完成（`sources/lens-b/mediawarp/02_readme_todo.md:23`、`:24`）。误判根源是抓取存档在 HTML 转文本时丢了 checkbox 状态。**更正结论：飞牛影视是主流中间件的正式支持对象，不是「待适配」。**

## 2.6 Jellyfin 路线：官方安装方案已长久未维护

如果你考虑的是「全家桶里加 Jellyfin」，这里有一条明确的提示——**而且它被放在「弃用菜单」下面**：整合脚本 README 在「弃用菜单（此菜单下的功能不再维护，不建议使用）」（`sources/01_raw_githubusercontent_com.md:169`）里列着「安装 Jellyfin全家桶（一键） -> `6 8 3 1`」（`:173`），并紧跟着写明：

> 「注意：目前官方 Jellyfin 安装方案已经长久未维护！」（`sources/01_raw_githubusercontent_com.md:180`）
> 「如果您需要安装 小雅Jellyfin 全家桶，请使用 AI老G 的脚本安装，风险自担。」（`sources/01_raw_githubusercontent_com.md:181`）

所以「加 Jellyfin」不建议走这条脚本主线——它连菜单都被归进了「不再维护、不建议使用」那一档，且官方方案本身长久未维护，只能用第三方脚本并「风险自担」。这条信息对选型的影响是：**别把 Jellyfin 当默认选项**，除非你愿意走非官方路径。

## 2.7 选型建议：落到你的场景

把上面几条收敛成建议——你的场景是「已有飞牛影视 + 不想装 Emby」：

1. **首选路线 F：单容器（仅 AList）+ 飞牛影视作前端。** 理由：无来源要求 Emby；要装的组件最少（只有一个容器，`sources/01_raw_githubusercontent_com.md:75`）；且飞牛影视已被主流中间件纳入支持方向。
2. **元数据提前想清楚。** 路线 F 没有现成元数据包：要么复用你已有的 Emby 刮削产物，要么接受飞牛影视按需刮削（`sources/forum/tid-73955.md:32`）。
3. **无论走哪条，都要修 302。** 外网/蜂窝网的坑和选型无关（`sources/forum/tid-73955.md:42`），第 5 章统一处理。
4. **若你确实想要「开箱即用的元数据宝库 + 成熟播放器生态」，再考虑路线 E**，并接受多养元数据爬虫、多下整套元数据包的开销；但**不要**顺手把 Jellyfin 也加上——官方方案已弃维护（`sources/01_raw_githubusercontent_com.md:180-181`）。

一句话总括：**「能不能不用 Emby」——能；「要不要用 Emby」——取决于你愿不愿意用元数据来源和额外组件开销去换一个开箱即用的影视库。**

## 本章小结

- **不必须 Emby**：全部来源无一处断言「必须」，已有社区实践走「全家桶去掉 Emby」，把 Emby 刮削的 STRM 喂给飞牛影视。
- **四维差异**：刮削元数据（E 有现成元数据包 / F 要自备来源）、播放链路（共用 STRM + 302，只是代理端口不同）、播放兼容性（飞牛侧经 MediaWarp 的 AlistStrm 可播网盘转码内容；Emby 硬解需手动开启）、外网可达性（**两条路线共同的坑**）。
- **门槛差在「要装几个组件」**：F 只有一个容器；E 还要多养元数据爬虫 + 下整套元数据包（本笔记不给 CPU/内存数字，原因见 2.4）。
- **旁证已确证**：MediaWarp / fntv-proxy 都把飞牛影视当正经播放端，且 MediaWarp 的待办清单明确 **`[x] 适配 飞牛影视`**（已完成）——**飞牛影视已被主流中间件正式支持**。
- **Jellyfin 官方安装方案已长久未维护**，且被列在「弃用菜单」里，不建议走这条脚本主线加装。

**下一章预告**：判断做完，接下来该动手了。但在敲命令之前，第 3 章先把三张清单备好——**目录（哪些路径映射进容器）、端口（容器内端口和宿主映射要分开看）、凭据（阿里云盘三件套 + WebDAV 账号）**，并顺带确认 fnOS 在整合脚本的兼容性表里的状态。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译」列对中文原文给的是**说人话**的复述；含英文术语的片段保留英文原名。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `我把xiaoyaemby刮削好的strm文件放到飞牛影音里` | 把 Emby 刮好的 STRM 文件搬进飞牛影视用 | `sources/forum/tid-73955.md:32` |
| 2 | `部署 小雅的全家桶 除了emby` | 装了全家桶但把 Emby 去掉 | `sources/forum/tid-73955.md:32` |
| 3 | `安装 小雅Alist -> 1 1` | 安装脚本里「只装小雅 Alist」这一项 | `sources/01_raw_githubusercontent_com.md:75` |
| 4 | `安装 Emby全家桶（一键） -> 2 1` | 安装脚本里「装 Emby 全家桶」这一项 | `sources/01_raw_githubusercontent_com.md:76` |
| 5 | `安装 小雅元数据定时爬虫 -> 2 5 1` | 元数据爬虫是可单独安装的组件 | `sources/01_raw_githubusercontent_com.md:77` |
| 6 | `安装 小雅元数据爬虫（Web 版本）-> 2 6 1` | 元数据爬虫另有 Web 版，同样可单装 | `sources/01_raw_githubusercontent_com.md:78` |
| 7 | `单独 下载并解压 全部元数据 -> 2 2 1` | 全家桶另有整套元数据包要下载解压 | `sources/01_raw_githubusercontent_com.md:90` |
| 8 | `单独 安装Emby（可选择版本，支持官方，amilys，lovechen）-> 2 3` | Emby 本体是脚本里被重点照料的独立组件 | `sources/01_raw_githubusercontent_com.md:109` |
| 9 | `图形化编辑 emby_config.txt -> 2 4` | Emby 的配置在脚本里有专门的图形化入口 | `sources/01_raw_githubusercontent_com.md:110` |
| 10 | `一键升级Emby容器（可选择镜像版本） -> 2 7` | Emby 容器可单独升级 | `sources/01_raw_githubusercontent_com.md:115` |
| 11 | `关闭 Emby 6908 端口访问 -> 2 9 2` | Emby 另有独立性开关（如端口访问） | `sources/01_raw_githubusercontent_com.md:118` |
| 12 | `注意：目前官方 Jellyfin 安装方案已经长久未维护！` | 官方 Jellyfin 安装方案已经很久没人维护了 | `sources/01_raw_githubusercontent_com.md:180` |
| 13 | `如果您需要安装 小雅Jellyfin 全家桶，请使用 AI老G 的脚本安装，风险自担。` | 要装 Jellyfin 只能用第三方脚本，风险自担 | `sources/01_raw_githubusercontent_com.md:181` |
| 14 | `弃用菜单（此菜单下的功能不再维护，不建议使用）` | Jellyfin 全家桶被归进「不再维护、不建议使用」的菜单 | `sources/01_raw_githubusercontent_com.md:169` |
| 15 | `安装 Jellyfin全家桶（一键） -> 6 8 3 1` | Jellyfin 的安装项就在上面那个弃用菜单里 | `sources/01_raw_githubusercontent_com.md:173` |
| 16 | `端口：5678 访问： http://xxxxx:5678/ （xxxx 为你alist所在设备的 IP）` | 资源层对外提供网页访问 | `sources/01_hub_docker_com.md:17` |
| 17 | `webdav 账号密码 用户: guest 密码: guest_Api789` | 资源层对外提供的第二条通道：WebDAV | `sources/01_hub_docker_com.md:18` |
| 18 | `22 MB` | 官方镜像在 Docker Hub 上标的体积 | `sources/01_hub_docker_com.md:30` |
| 19 | `如果需要开启Emby硬件转码请先返回主菜单开启容器运行额外参数添加 -> 72` | Emby 硬解默认不开，要先去菜单打开容器额外参数 | `sources/xiaoyaDev/all_in_one.sh:3479` |
| 20 | `请输入其他参数（默认 --device /dev/dri:/dev/dri --privileged -e GIDLIST=0,0 -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all ）` | 脚本给硬解预设的设备参数（Intel 核显 / NVIDIA） | `sources/xiaoyaDev/all_in_one.sh:3485` |
| 21 | `2、开启/关闭 容器运行额外参数添加             当前状态：${_container_run_extra_parameters}` | 硬解开关在菜单里的样子（状态项） | `sources/xiaoyaDev/all_in_one.sh:6061` |
| 22 | `Strm 文件可以实现 302 直链播放，流量不经过 Emby Server / Jellyfin Server / 飞牛影视服务器` | STRM 能实现 302 直链播放，流量不经过媒体服务器 | `sources/lens-b/mediawarp/01_github_com.md:53` |
| 23 | `strm 只是 URL 指针` | STRM 文件只存一个 URL 指针，本身不是视频 | `sources/lens-b/fntvproxy/01_github_com.md:266` |
| 24 | `将播放器地址指向代理端口（飞牛 :28005，Emby :8095）` | 把播放器指到代理端口：飞牛用 28005、Emby 用 8095 | `sources/lens-b/fntvproxy/01_github_com.md:71` |
| 25 | `基于飞牛影视 0.9.3 版本` | 这个代理工具是针对飞牛影视 0.9.3 版本做的 | `sources/lens-b/fntvproxy/01_github_com.md:45` |
| 26 | `前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器` | 一个架在 Emby/Jellyfin/飞牛影视前面的反向代理 | `sources/lens-b/mediawarp/01_github_com.md:51` |
| 27 | `- [x] 适配 飞牛影视` | MediaWarp 已完成对飞牛影视的适配（待办清单勾选项） | `sources/lens-b/mediawarp/02_readme_todo.md:23` |
| 28 | `- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` | 飞牛影视 AlistStrm 模式下支持播放网盘转码内容（已完成） | `sources/lens-b/mediawarp/02_readme_todo.md:24` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线换为 xiaoyaDev/xiaoya-alist（DDSRem）整合脚本，路线 E/F 的组成与门槛口径整体换源（第 2 篇）**。2.2 删去 monlor 项目的 compose 简介与三条组件注释（`monlor-144.md:14/88/89/90`），改为一律回源整合脚本菜单：Alist（hub `:17-18`）、元数据（`01_raw_githubusercontent_com.md:77-78`、`:90`）、Emby（`:109/:110/:115/:118`）。2.3 总表「刮削与元数据来源」中的「官方脚本」改为「脚本」，播放兼容性一行占位由「没有计划支持硬解」改为「Emby 硬解要手动开启」。2.3.1 元数据来源改为脚本菜单口径。2.3.3 硬解段**整段重写**：由「维护者说没有计划支持硬解」（`monlor-144.md:58`）改为「硬解是可选功能、默认不开」——回源 `all_in_one.sh:3479`（提示先开容器额外参数）、`:3485`（预设设备参数）、`:6061`（菜单状态项），并新增一条「旧结论已作废」note。2.4 整节重写：删去 monlor 的四行配置推荐表（`monlor-144.md:74-80`）与「维护者推荐」warning，改为「要装几个组件」四行对照表（容器数 / 元数据包 / 谁刮削 / 镜像体积）+「本笔记不给 CPU / 内存数字」warning；2.7 第 1 条与本章小结对应改写。2.6 Jellyfin 一节补「该菜单属弃用菜单」的依据（`:169`、`:173`）与「风险自担」原话（`:181`），措辞由「官方提示」改为「整合脚本 README 的提示」。下一章预告的「官方兼容性表」改为「整合脚本的兼容性表」。引文对照由 17 条重编为 28 条，来源改挂整合脚本 README、官方镜像页、`all_in_one.sh` 与 lens-b 来源；monlor 的 6 条（compose 简介、组件注释 3 条、硬解、资源表）移出正文。 |
| 2026-10-06 | **口径修正（MediaWarp）**：更正 2.5 与 2.3.3——此前把 MediaWarp README 的「适配 飞牛影视」读成**待办项**，据此判「成熟度未决」。核对 raw Markdown 后确认该行为 `- [x] 适配 飞牛影视`（已完成），`- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` 亦已完成（`sources/lens-b/mediawarp/02_readme_todo.md:23`、`:24`）；误判根源是旧抓取存档丢失 checkbox 状态。2.5 标题与结论由「未决」改为**已确证**；2.2 表「网盘转码仍是待办」改为「AlistStrm 模式下支持」；引文对照表原 13 行改为 `[x]` 口径并新增 14。 |
| 2026-10-06 | 2.3.4 补充「外网远程观影」小节：区分**直接挂载（WebDAV）→ NAS 中转载流、吃上行带宽**与 **STRM + 302 → 客户端直连网盘、不过 NAS**（`sources/lens-b/mediawarp/01_github_com.md:53`）；说明飞牛「网盘优先直链（302）」主要面向飞牛原生挂载的网盘，小雅经 WebDAV 挂载时通常套不上 302 直链。 |
---

# 第 3 章 动手前准备——目录、端口与凭据（新手可跳过）

## 本章要解决的问题

动手部署之前，其实只需要备好**三张清单**：**目录**（哪些路径要映射进容器）、**端口**（容器内用什么端口、宿主机映射成什么端口）、**凭据**（阿里云盘三件套，加可选的夸克 / 115 / UC，以及 WebDAV 账号）。本章只准备清单，**不执行任何部署**——命令集中在下一章。标题里的「新手可跳过」指的是本章末尾那段配置片段，如果你只想先看懂结构，读三张清单即可，片段留到下一章照着用。

先说两条贯穿全章的纪律：**「容器内」和「宿主机」是两套端口，绝不能混写**；镜像名同理——本笔记全程只用**官方镜像** `xiaoyaliu/alist`（由 `xiaoyaDev/xiaoya-alist` 的整合脚本安装），别跟别的镜像名混写。下面逐张清单来。

## 3.1 目录：哪些路径要映射进容器

小雅容器需要一块**持久化目录**来存数据与配置。本笔记的整合脚本会在安装时问你「配置文件路径」，默认值就是 `/etc/xiaoya`（`sources/xiaoyaDev/all_in_one.sh:156`），你可以在安装时改成别的。这个目录在宿主机上长出这样一棵树：

```text
# 宿主机（默认路径，安装时可改）
/etc/xiaoya/                            ← 配置目录（脚本自称「配置文件路径」）
├── mytoken.txt                         ← 阿里云盘访问令牌
├── myopentoken.txt                     ← 阿里云盘开放令牌
├── temp_transfer_folder_id.txt         ← 转存文件夹 ID
├── quark_cookie.txt                    ← 夸克 Cookie（可选）
├── 115_cookie.txt                      ← 115 Cookie（可选）
├── uc_cookie.txt                       ← UC Cookie（可选）
├── docker_address.txt                  ← 脚本写入的小雅自身地址
├── guestlogin.txt / guestpass.txt      ← 「强制登入」账号与密码（可选）
└── data/                               ← 元数据 / 站点数据
```

安装时脚本会把这个目录挂进容器两次（`sources/xiaoyaDev/all_in_one.sh:1392`）：

| 宿主机路径 | → 容器内挂载点 | 用途 | 出处 |
| --- | --- | --- | --- |
| `/etc/xiaoya`（默认值，可改） | `/data` | 配置与凭据文件所在 | `sources/xiaoyaDev/all_in_one.sh:1392` |
| `/etc/xiaoya/data` | `/www/data` | 元数据 / 站点数据 | `sources/xiaoyaDev/all_in_one.sh:1392` |

其中 `docker_address.txt` 值得单独记一笔：它是**小雅自己的地址文件**，脚本启动时写进去（`sources/xiaoyaDev/all_in_one.sh:1367-1369`），TVBox 一类的外部工具会读它。

> [!tip] 大白话
> 把「目录映射」想成**给容器开一个抽屉**：容器是搬运工，它自己不带记忆；你把 NAS 上一个真实文件夹（上面那棵 `/etc/xiaoya`）焊到它的 `/data` 抽屉上，它写进去的东西才留在你硬盘上、重启不丢。焊错了或者没焊，容器一重启，数据就没了。

> [!note] 这棵树就是「凭据放哪」的答案
> 第 3.3 节要讲的 `mytoken.txt` 等文件，全都长在上面这棵树里。安装时你在终端里被问到的每个问题，最后都落成这里的一个文件——所以**这里看懂了，下一节就只是「每个文件填什么值」**。

## 3.2 端口：容器内端口与宿主映射要**分开看**

这是最容易写错的一处，务必分两张表读。

**表一：容器内端口**（容器自己监听什么）：

| 容器内端口 | 用途 | 出处 |
| --- | --- | --- |
| `80` | AList Web 服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2345` | 备用端口 / 其他服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2346` | 备用端口 / 其他服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2347` | 备用端口 / 其他服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |

**表二：宿主机映射**（脚本默认值，你在浏览器里访问的端口）：

| 宿主机端口 | → 容器内端口 | 说明 | 出处 |
| --- | --- | --- | --- |
| `5678` | `80` | AList Web 服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2345` | `2345` | 备用端口 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2346` | `2346` | 备用端口 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| `2347` | `2347` | 备用端口 | `sources/xiaoyaDev/all_in_one.sh:1377` |

映射关系写作 `"宿主机:容器"`，方向恒为「左宿主、右容器」。安装时脚本给出的访问地址就是按这个映射拼的：`alist: http://ip:5678`（`sources/xiaoyaDev/all_in_one.sh:1398`）。

> [!warning] 注意：容器内是 `80`，不是 `5678`
> 本笔记早期版本（monlor 路线）容器内是 `5678`、宿主映射到 `5677`。**本路线反过来**：容器内是 `80`，宿主默认 `5678`（`sources/xiaoyaDev/all_in_one.sh:1377`）。如果你照着旧教程配过端口转发或防火墙，或者 `5678` 已经被别的服务占用，**先处理这里**再往下一章走。

> [!tip] 大白话
> 把端口想成**门牌号**：容器内的 `80` 是它在屋里自己的门牌，宿主机的 `5678` 是你从大门口进去的门牌。访客（浏览器）走的是大门那个号（`5678`），屋里那个号访客看不见。所以「左边（外面）随脚本默认，右边（屋里）别乱动」。

## 3.3 凭据：阿里云盘三件套（+ 可选夸克 / 115 / UC）+ WebDAV 账号

小雅要访问你的阿里云盘，就需要三样凭据。本笔记的整合脚本用**「安装时问答 + 落盘文件」**注入：脚本逐个问你，问完写进配置目录（第 3.1 节那棵树）下的 `.txt`（`sources/xiaoyaDev/all_in_one.sh:1230`、`:1237-1245`）。

| 脚本问的 | 落盘文件 | 含义 | 出处 |
| --- | --- | --- | --- |
| 阿里云盘 refresh token | `mytoken.txt` | 阿里云盘的访问令牌 | `sources/xiaoyaDev/all_in_one.sh:569` |
| 阿里云盘 Open Token | `myopentoken.txt` | 阿里云盘的开放访问令牌 | `sources/xiaoyaDev/all_in_one.sh:628` |
| 转存文件夹 ID | `temp_transfer_folder_id.txt` | 指定「转存」落到哪个目录 | `sources/xiaoyaDev/all_in_one.sh:948` |

脚本在开工前会把这三个文件列为必建项（`sources/xiaoyaDev/all_in_one.sh:1230-1236`），填不出可用值它会反复追问。

**那么这三个值怎么拿到？** 上面说的是「填什么」，这里补「怎么拿」。**前两样现在都走「手机扫码」**——这是当前的主推方式（下面称**方案 A**），也是本笔记推荐的做法；旧的「按 `F12` 复制网页代码 → 解码站」那一套（方案 B）已被阿里云盘接口变更淘汰，见本节后面的提醒。三步对照如下：

| 要拿的东西 | 操作（主推：扫码） | 出处 |
| --- | --- | --- |
| 阿里云盘 token（`mytoken.txt`） | 电脑浏览器打开 AList 文档的**阿里云盘**页 `https://alist.nn.ci/zh/guide/drivers/aliyundrive`，用**手机阿里云盘 App 扫码**授权，页面给出的 **32 位** token 就是它 | `sources/p5/slarker/01_wiki_slarker_me.md:29` |
| Open Token（`myopentoken.txt`） | 同样扫码：打开 `https://alist.nn.ci/tool/aliyundrive/request.html`，点「Go to login」，用阿里云盘**手机 APP 扫码**登录，下一个页面的方框里给出的 **280 位** Open Token 就是它（另一份教程记作 **288~335 位**） | `sources/p3/gnz48/01_www_cnblogs_com.md:30`；`sources/p5/slarker/01_wiki_slarker_me.md:30` |
| folder id（`temp_transfer_folder_id.txt`） | 登录阿里云盘网页版，在**资源盘**下新建一个文件夹（教程命名为 `xiaoya`），点进去后复制地址栏 URL 里的那串 folder id | `sources/p3/gnz48/01_www_cnblogs_com.md:31` |

近期教程把扫码的每一步写得更细，可照着做（`sources/p5/wsisp/01_www_wsisp_com.md:21-25`）：电脑浏览器打开**阿里云盘 Token 生成页** → 点「获取 Token」，页面出现**二维码** → 用**手机阿里云盘 App 扫码**（须最新版）→ 手机端点「授权」后，**电脑页面会显示一串字符** → 把这一串字符填进第一个问题（`sources/p5/wsisp/01_www_wsisp_com.md:21-25`）。

> [!note] 来源给的位数不一，照抄即可、不必数
> 同一样东西，不同来源的位数写法不同：阿里云盘 token，AList 文档与老教程写 **32 位**（`sources/p5/slarker/01_wiki_slarker_me.md:29`、`sources/p3/gnz48/01_www_cnblogs_com.md:26-29`），近期教程写 **40 位**（`sources/p5/wsisp/01_www_wsisp_com.md:24`）；Open Token 则写 **280 位**（`sources/p3/gnz48/01_www_cnblogs_com.md:30`）与 **288~335 位**（`sources/p5/slarker/01_wiki_slarker_me.md:30`）两种。差异可能来自页面改版，**本笔记不裁断**；你照着页面复制即可，别去数位数。

另一份社区教程把获取方式列成对照表：三样分别指向 AList 文档的「阿里云盘 / 分享」「阿里云盘 Open」两页，并额外提醒第三样要**先转存小雅的分享**到自己网盘，再取自己的 folder id（`sources/p3/z-addone/01_www_cnblogs_com.md:21-25`）。论坛里也有人问「Open 拿到的是 refresh_token，要怎么填」，楼主给的答复就是上面那个 `request.html` 链接（`sources/01_club_fnnas_com.md:904`）。

> [!warning] 三个提醒
> 1. **token 会过期，扫码后要「二次确认」**：阿里云盘 token 的有效期**通常只有 2~3 个月**（`sources/p5/wsisp/01_www_wsisp_com.md:11`）；论坛也有用户反馈 token 第二天就失效、需重新获取（`sources/01_club_fnnas_com.md:157`）。另外扫码后**要在手机上点「授权 / 确认」**，否则拿到的可能是无效 token（`sources/p5/wsisp/01_www_wsisp_com.md:11`）。这是教程提醒加单条用户反馈、不是官方结论，但足以说明：别指望填一次管一辈子。**新版下换 token 更省事**：文件就在宿主机上，直接改 `mytoken.txt` 再重启容器即可。
> 2. **旧方法（方案 B）已失效，降为备选**：老教程教的是「登录网页版 → 按 `F12` → 复制 `login.do?appName=aliyun` 的响应 → 丢进第三方解码站 `media.cooluc.com/decode_token/` 解码」（`sources/p3/gnz48/01_www_cnblogs_com.md:26-29`）。**这条路已被阿里云盘接口变更淘汰**——近期教程明确写「旧版教程里直接复制网页代码的方法已经失效」（`sources/p5/wsisp/01_www_wsisp_com.md:17`）。因此本笔记把**扫码法（方案 A）列为主推**，F12 法**降为备选**：优先扫码，只在扫码页实在打不开时再试，且要意识到它很可能已经不灵。
> 3. **第三方工具要留意**：凡是把你的登录响应 / 扫码交给**非阿里官方的第三方站点**处理的，都要多一分谨慎；别把任何单一工具当唯一出路。

> [!tip] 大白话
> 三样东西对应三件事：**「你是谁」**（`mytoken.txt`，证明这个盘是你的）、**「开放接口的通行证」**（`myopentoken.txt`，小雅走开放接口取文件要用）、**「东西先放哪儿」**（`temp_transfer_folder_id.txt`，临时转存来的片先落在这个文件夹）。前两样都靠**手机扫码**换取，第三样是你在自己网盘里建个文件夹、把它地址栏里那串字符抄下来。

### 3.3.1 如何选用夸克、115 和 UC

**可选凭据：夸克 / 115 / UC。** 如果你**主用夸克**（或想挂 115、UC），还要多一份对应 cookie。它不是「换掉阿里」，而是「再挂一个盘」：

| 凭据内容 | 落盘文件 | 出处 |
| --- | --- | --- |
| 夸克网盘 cookie | `quark_cookie.txt` | `sources/xiaoyaDev/all_in_one.sh:740` |
| 115 网盘 cookie | `115_cookie.txt` | `sources/xiaoyaDev/all_in_one.sh:292` |
| UC 网盘 cookie | `uc_cookie.txt` | `sources/xiaoyaDev/all_in_one.sh:259` |

好消息是**这三样在新版里都支持扫码自动获取**：脚本会先问「是否使用扫码自动获取 … Cookie [Y/n]（默认 Y）」，选默认就出二维码，扫码失败才提示你手动粘贴（夸克 `sources/xiaoyaDev/all_in_one.sh:740-742`；115 `sources/xiaoyaDev/all_in_one.sh:680`）。所以「手抓 cookie」从「唯一办法」降级成了「扫码失败时的后手」。

夸克 cookie 管的是**小雅的夸克分享区**（`/🌀我的夸克分享`）与**挂载你自己的夸克**——它值不值得配、能覆盖多少，第 5 章 5.6 讲清了。**手动抓时**仍可用浏览器开发者工具，AList 官方文档给的就是一句：

> 「按F12打开“调试”，选中“网络”，随意在左侧选择请求，找到携带 `Cookie` 参数的就可以」（`sources/p5/alist-docs/01_raw_githubusercontent_com.md:47`）

拆成四步：① 用 **Chrome** 打开并登录**夸克网盘网页版** `pan.quark.cn`；② 按 `F12` 打开「调试」→ 切到「网络」；③ 刷新一下，在左边请求列表里**随便点一个**，找到**请求头里带 `Cookie` 参数**的那个；④ 把 **Cookie 整串**复制下来，粘贴给脚本（它会替你写进 `quark_cookie.txt`）。

> [!warning] 手抓夸克 cookie 的两个坑
> 1. **要用 Chrome 抓**：官方文档专门注明「请使用Chrome浏览器来获取Cookies，使用Firefox获取的Cookies或仍将停留在访客并请求登录。」（`sources/p5/alist-docs/01_raw_githubusercontent_com.md:63`）——Firefox 抓到的可能是「访客态」，填了也不认。
> 2. **它会过期，而且很短**：官方仓库的修复 PR 说明，夸克的 `__puus` 会话 cookie **约 3 小时**就过期，且只有「请求不带 `__puus`」时夸克才重新签发；而客户端总是带上已存的 cookie，于是过期后**列表还能看、下载却 403，要重启才恢复**（`sources/gh/alist-9596.md:11`）。这正好解释了论坛那种「夸克 cookie 填进去却不出效果」的反馈（`sources/forum/tid-8385880.md:30`）。

### 3.3.2 WebDAV 账号

**WebDAV 账号**用来把资源库当文件夹挂载，地址是 `http://<你的IP>:5678/dav`。要填的用户名/密码**取决于你安装时有没有开「强制登入」**——这是两个分支，不是两种说法：

| 安装时的选择 | 用户名 | 密码 | 出处 |
| --- | --- | --- | --- |
| **开了强制登入**（脚本默认选 `y`，推荐） | `dav`（脚本注明「无法修改」） | 你安装时自己设的那个 | `sources/xiaoyaDev/all_in_one.sh:1304`、`:1401` |
| 没开强制登入 | `guest` | `guest_Api789` | `sources/01_hub_docker_com.md:18` |

两条分支的**路径都是 `/dav`**。「历史上用户名到底是 `dav` 还是 `guest`」的反复，根源就在这里：**`/dav` 是路径，`dav` 是强制登入的用户名**，两回事被记成了一件事。

脚本推荐你开强制登入，理由它自己写了两条：不开的话「暴露到公网可能被坏人扫描到并无限制使用」，且「多人异地访问可能触发网盘风控甚至封禁账号」（`sources/xiaoyaDev/all_in_one.sh:1293-1294`）。开了之后，脚本会把你设的密码写进 `guestpass.txt`（`sources/xiaoyaDev/all_in_one.sh:1329`）。

> [!tip] 大白话
> 三件套想成**三把钥匙**：`mytoken.txt` 是进阿里云盘大门的钥匙，`myopentoken.txt` 是另一把「开放接口」的钥匙，`temp_transfer_folder_id.txt` 则是告诉小雅「把临时借来的片放进哪个抽屉」。三者缺一，小雅就取不到片。WebDAV 那套则是给「挂载文件夹」用的门禁卡——**开了强制登入就是你自己设的卡（`dav` + 自设密码），没开就是通用的那张（`guest` / `guest_Api789`）**，别把通用卡当成你自己的账号密码。顺带一提，凭据与播放的取舍，我在 [[流媒体与影音/网盘影视播放与本地存储的取舍]] 里也有铺垫。

## 3.4 fnOS 兼容性：兼容表里是 ✅

你想用在 fnOS（飞牛私有云）上，这一条可以放心：整合脚本项目的 README 里那份**通用兼容性测试报告**中，fnOS（飞牛私有云）一行的三项脚本全部通过（`sources/01_raw_githubusercontent_com.md:277`）。表头三列是 `all_in_one.sh`、`emby_config_editor.sh`、`xiaoya_notify.sh（已弃用）`（`sources/01_raw_githubusercontent_com.md:236`）——**第一列 `all_in_one.sh` 就是我们第 4 章要跑的那个脚本**，它 ✅ 意味着这条路在飞牛上是被测过的。

> [!note] 读表须知
> 第三列 `xiaoya_notify.sh` 表头已标注**「（已弃用）」**，所以「三项均 ✅」里含一个已弃用脚本，别把 ✅ 误读成「它还在维护」。真正对部署有意义的是前两项。

## 3.5 配置清单片段（新手可跳过）

下面只是**待填清单的形态**，不是可直接复制的成品（路径、凭据需你替换）。完整部署命令在下一章。

**主路线**：一条命令进菜单，选 `1 1`，凭据由脚本逐个问你（第 4 章详述）：

```bash
# 出处：sources/01_raw_githubusercontent_com.md:39
bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"
```

**如果你更想自己掌控（备选）**：脚本用的是官方镜像 `xiaoyaliu/alist`，等价的手写 Compose 长这样——

```yaml
# docker-compose.yml（官方镜像等价写法）
# 参数出处：sources/xiaoyaDev/all_in_one.sh:1373-1392
services:
  xiaoya:
    image: xiaoyaliu/alist:latest      # 官方镜像
    container_name: xiaoya
    privileged: true
    volumes:
      - /etc/xiaoya:/data              # 左=宿主机配置目录(可改)  右=容器内(不改)
      - /etc/xiaoya/data:/www/data
    ports:
      - "5678:80"                      # 左=宿主机端口(可改)      右=容器内(不改)
      - "2345:2345"
      - "2346:2346"
      - "2347:2347"
    restart: always
```

> [!warning] 备选路线要自己填凭据文件
> 手写 Compose 时**没有问答环节**——上面那些 `mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt` 得你自己放进 `/etc/xiaoya/`。所以除非你有特别理由，否则**直接用一键脚本更省事**：它替你问、替你写、还替你等启动（第 4 章）。

> [!note] 术语校正：整合脚本 vs 官方镜像
> 本笔记用的是 `xiaoyaDev/xiaoya-alist`，它是**社区整合脚本**，**不是官方**；它内部用的才是**官方镜像** `xiaoyaliu/alist`（作者 xiaoyaLiu，站点 `alist.xiaoya.pro`）。之后排查问题、找文档时请分清这两层——去整合脚本项目里找镜像问题、或去官方文档里找菜单问题，都会扑空。

## 本章小结

- **只备清单，不部署**：本章给出目录、端口、凭据三张清单；命令集中在第 4 章。
- **目录**：配置目录默认 **`/etc/xiaoya`**（安装时可改），挂到容器 `/data`；其下 `data/` 挂到 `/www/data`。凭据文件全在这棵树里。
- **端口务必分内外**：容器内 `80` / `2345` / `2346` / `2347`，宿主默认 `5678` / `2345` / `2346` / `2347`；映射方向恒为「左宿主、右容器」。注意**容器内是 `80` 而不是 `5678`**，与旧笔记不同。
- **凭据走「问答 + 落盘文件」**：`mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt`（三样必填），不用自己写环境变量。
- **三件套怎么拿**：第 1、2 样都走**手机扫码**（方案 A，`sources/p5/slarker/01_wiki_slarker_me.md:29`、`sources/p5/wsisp/01_www_wsisp_com.md:21-25`）；旧的 `F12` + 解码站法已被接口变更淘汰、降为备选（`sources/p5/wsisp/01_www_wsisp_com.md:17`）。
- **夸克 / 115 / UC 属可选凭据**：对应 `quark_cookie.txt` / `115_cookie.txt` / `uc_cookie.txt`；三样在脚本里都**支持扫码自动获取**（夸克 `all_in_one.sh:740-742`、115 `:680`），手抓（Chrome + `F12`）只是后手。主用夸克时正是靠它用上小雅的**夸克分享区**——注意夸克 cookie 约 3 小时会过期，详见第 5 章 5.6。
- **WebDAV 是双分支**：地址 `http://<IP>:5678/dav`；开强制登入（默认、推荐）→ 用户名 `dav` + 自设密码；没开 → `guest` / `guest_Api789`。
- **fnOS 在兼容表里 ✅**（含一个已弃用脚本），部署前提无兼容性障碍。

**下一章预告**：清单齐了，第 4 章进入部署实战——用 `xiaoyaDev/xiaoya-alist` 的**一键菜单脚本**（菜单 `1 1`）把**单容器**的小雅跑起来，并给出部署后的自检清单。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译」列对中文原文给的是**说人话**的复述；配置项、路径、文件名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `-v ${CONFIG_DIR}:/data -v ${CONFIG_DIR}/data:/www/data` | 配置目录挂到容器 `/data`，其下 `data/` 再挂 `/www/data` | `sources/xiaoyaDev/all_in_one.sh:1392` |
| 2 | `xiaoya_alist_config_dir` → `/etc/xiaoya` | 配置目录默认值就是 `/etc/xiaoya`（探测到大盘时会换成该盘的 `xiaoya`） | `sources/xiaoyaDev/all_in_one.sh:156-158` |
| 3 | `-p 5678:80` | 宿主 5678 对到容器 80，跑 AList 网页服务 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| 4 | `-p 2345:2345 -p 2346:2346 -p 2347:2347` | 三个辅助端口，宿主与容器同号 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| 5 | `files=("mytoken.txt" "myopentoken.txt" "temp_transfer_folder_id.txt")` | 脚本开工前必建这三个凭据文件 | `sources/xiaoyaDev/all_in_one.sh:1230` |
| 6 | `mytoken.txt` | 阿里云盘访问令牌（refresh token）的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:569` |
| 7 | `myopentoken.txt` | 阿里云盘开放令牌（Open Token）的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:628` |
| 8 | `temp_transfer_folder_id.txt` | 转存文件夹 ID 的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:948` |
| 9 | `quark_cookie.txt` | 夸克 Cookie 的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:740` |
| 10 | `115_cookie.txt` | 115 Cookie 的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:292` |
| 11 | `uc_cookie.txt` | UC Cookie 的落盘文件 | `sources/xiaoyaDev/all_in_one.sh:259` |
| 12 | `是否使用扫码自动获取 夸克 Cookie [Y/n]（默认 Y）` | 夸克 cookie 可扫码自动获取，默认选 Y | `sources/xiaoyaDev/all_in_one.sh:742` |
| 13 | `是否使用扫码自动获取 115 Cookie [Y/n]（默认 Y）` | 115 cookie 可扫码自动获取，默认选 Y | `sources/xiaoyaDev/all_in_one.sh:680` |
| 14 | `强制登入用户名：dav（无法修改）` | 开强制登入后，WebDAV 用户名固定为 `dav` | `sources/xiaoyaDev/all_in_one.sh:1304` |
| 15 | `暴露到公网可能被坏人扫描到并无限制使用` | 脚本建议开强制登入的第一条理由 | `sources/xiaoyaDev/all_in_one.sh:1293` |
| 16 | `多人异地访问可能触发网盘风控甚至封禁账号` | 第二条理由：防多人异地访问触发风控 | `sources/xiaoyaDev/all_in_one.sh:1294` |
| 17 | `webdav 账号密码 用户: guest 密码: guest_Api789` | （官方 hub 页）未开强制登入时的默认 WebDAV 账号 | `sources/01_hub_docker_com.md:18` |
| 18 | `docker_address.txt` | 脚本写入的「小雅自身地址」文件 | `sources/xiaoyaDev/all_in_one.sh:1367-1369` |
| 19 | `fnOS (飞牛私有云)` | 兼容表里的 fnOS 一行，三项脚本均 ✅ | `sources/01_raw_githubusercontent_com.md:277` |
| 20 | `all_in_one.sh` | 兼容表列名之一，也就是第 4 章要跑的主安装脚本 | `sources/01_raw_githubusercontent_com.md:236` |
| 21 | `阿里云盘 Token（32 位长度）， [使用阿里云盘 App 点此扫码](https://alist.nn.ci/zh/guide/drivers/aliyundrive) 获取备用。` | 拿 32 位 token：手机阿里云盘 App 扫该链接指向的码 | `sources/p5/slarker/01_wiki_slarker_me.md:29` |
| 22 | `阿里云盘 OpenToken（288~335 位长度）， [使用阿里云盘 App 点此扫码](https://alist.nn.ci/tool/aliyundrive/request.html) 获取备用。` | 拿 OpenToken：同样用手机 App 扫码（该教程记作 288~335 位） | `sources/p5/slarker/01_wiki_slarker_me.md:30` |
| 23 | `②myopentoken 获取链接：<https://alist.nn.ci/tool/aliyundrive/request.html> ，点击“Go to login”，然后直接用自己的阿里云盘手机端APP扫码登录。` | 拿 Open Token：打开该页点「Go to login」，用手机 APP 扫码 | `sources/p3/gnz48/01_www_cnblogs_com.md:30` |
| 24 | `在资源盘下新建文件夹（xiaoya）,点击进入后复制阿里云盘转存目录folder` | 拿 folder id：在资源盘建文件夹，进去后复制转存目录的 folder id | `sources/p3/gnz48/01_www_cnblogs_com.md:31` |
| 25 | `①Mytoken获取链接：<https://media.cooluc.com/decode_token/> 点击顶部“进入移动端网页登录入口` | （旧法）拿 token：到解码站，点「进入移动端网页登录入口」 | `sources/p3/gnz48/01_www_cnblogs_com.md:26` |
| 26 | `先转存这个[阿里云盘分享](https://www.aliyundrive.com/s/rP9gP3h9asE)到自己网盘。` | 取 folder id 之前，先把小雅这个分享转存到自己网盘 | `sources/p3/z-addone/01_www_cnblogs_com.md:25` |
| 27 | `<https://alist.nn.ci/zh/tool/aliyundrive/request.html>` | 楼主对「Open 拿到的是 refresh_token，要怎么填」的答复链接 | `sources/01_club_fnnas_com.md:904` |
| 28 | `PS:ALIYUN_TOKEN 第二天就失效了，需要重新获取` | 有用户反馈 token 第二天就失效，需重新获取 | `sources/01_club_fnnas_com.md:157` |
| 29 | `最近阿里云盘更新了接口，旧版教程里直接复制网页代码的方法已经失效。` | 阿里云盘改了接口，旧教程「复制网页代码」那招已失效 | `sources/p5/wsisp/01_www_wsisp_com.md:17` |
| 30 | `阿里云盘的Token就像是你家的门禁卡，有效期通常只有2-3个月。` | token 像门禁卡，有效期通常只有 2~3 个月 | `sources/p5/wsisp/01_www_wsisp_com.md:11` |
| 31 | `有些用户获取Token时操作不规范，比如扫码后没有点击二次确认，导致拿到的根本是无效Token。` | 有人扫码后没点「二次确认」，拿到的是无效 token | `sources/p5/wsisp/01_www_wsisp_com.md:11` |
| 32 | `用手机阿里云盘APP扫码（必须是最新版本）` | 扫码要用最新版手机 App | `sources/p5/wsisp/01_www_wsisp_com.md:23` |
| 33 | `手机端点击授权后，电脑页面会显示40位字符串` | 手机端点授权后，电脑页面显示 40 位字符串 | `sources/p5/wsisp/01_www_wsisp_com.md:24` |
| 34 | ``按F12打开“调试”，选中“网络”，随意在左侧选择请求，找到携带 `Cookie` 参数的就可以`` | 手抓夸克 cookie：F12 → 网络 → 随便点一个请求 → 复制带 `Cookie` 参数的那个 | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:47` |
| 35 | `注意：请使用Chrome浏览器来获取Cookies，使用Firefox获取的Cookies或仍将停留在访客并请求登录。` | 抓夸克 cookie 要用 Chrome；Firefox 抓的会停在访客、要求登录 | `sources/p5/alist-docs/01_raw_githubusercontent_com.md:63` |
| 36 | ``The __puus session cookie expires after about 3 hours (see #830). Quark only re-issues it when a request does not carry the __puus field, but the driver always sends the stored cookie, so once it expires the driver can never refresh it in-process: file listing keeps working while downloads fail with 403 until restart.`` | 夸克 `__puus` 会话 cookie 约 3 小时过期；只有「请求不带 `__puus`」时夸克才重发，而客户端总带已存 cookie → 过期后列表可看、下载 403，重启才恢复 | `sources/gh/alist-9596.md:11` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **凭据注入方式由「环境变量」改为「安装问答 + 落盘文件」**：3.1 目录树重画为 `/etc/xiaoya` 本路线实况（列出 `mytoken.txt` 等凭据文件与 `data/` 子目录），挂载表由「`/data` + metadata 的 `/etc/xiaoya`」改为「`/etc/xiaoya`→`/data`、`/etc/xiaoya/data`→`/www/data`」，新增「这棵树就是凭据放哪」note；3.2 端口表重排（容器内 `80`/`2345`/`2346`/`2347`，宿主 `5678`/…），新增「容器内是 80 不是 5678」warning；3.3 三件套由 `ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID` 改为 `mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt`，「怎么拿」三步与位数 note 保留但只换落点；3.3.1 夸克/115/UC 改为文件口径并**补充扫码自动获取**（夸克 `all_in_one.sh:742`、115 `:680`）与手抓后手地位；3.3.2 WebDAV 改为**强制登入双分支**（`dav`+自设密码 / `guest`+`guest_Api789`），并说明 `dav` 与 `/dav` 的历史混淆；3.4 修「官方仓库」为「整合脚本项目 README」，点明兼容表第一列 `all_in_one.sh` 即主脚本；3.5 片段由 monlor compose 改为「一键脚本（主）+ 官方镜像等价 compose（备）」并加「整合脚本 ≠ 官方」note。全篇镜像名由 `ghcr.io/monlor/xiaoya-alist` 改为 `xiaoyaliu/alist`；章内纪律句同步。引文对照重编为 36 条，出处改挂 `sources/xiaoyaDev/all_in_one.sh`、`sources/01_raw_githubusercontent_com.md`、`sources/01_hub_docker_com.md` 与通用教程来源；monlor 语境行（`ALIYUN_TOKEN` 三条、`WEBDAV_PASSWORD`、`QUARK_COOKIE` 注释、端口 `5677` 三条、`/data` 映射注释）移出正文。表头由「（原文 / 中译）」补全为「（原文 / 中译 / 出处）」。 |
| 2026-10-06 | **补充 3.3 缺失的「怎么拿」**：原文只写了三件套的**文件名与放置位置**，未写**获取方式**。新增三件套获取三步（`sources/p3/gnz48/01_www_cnblogs_com.md:25-31`：解码站取 32 位 `mytoken.txt`、`request.html` 扫码取 Open Token、资源盘建文件夹取 folder id），补另一份教程的「获取方式」对照与「先转存小雅分享」提醒（`sources/p3/z-addone/01_www_cnblogs_com.md:21-25`）、论坛楼主答复（`sources/01_club_fnnas_com.md:904`），以及 token 过期反馈（`sources/01_club_fnnas_com.md:157`）与第三方解码站风险提示；引文对照新增第 23–29 行。 |
| 2026-10-06 | **改推「扫码法（方案 A）」，旧 F12 法降为备选**：阿里云盘接口变更后，老教程「复制网页代码 → 第三方解码站」取 token 的路已失效（`sources/p5/wsisp/01_www_wsisp_com.md:17`）。3.3「怎么拿」第 1 步由 F12 + 解码站改为**手机扫码**（`sources/p5/slarker/01_wiki_slarker_me.md:29`、`sources/p5/wsisp/01_www_wsisp_com.md:21-25`）；补 token 有效期 2~3 个月与扫码「二次确认」（`sources/p5/wsisp/01_www_wsisp_com.md:11`）；`[!warning]` 改为三条、新增位数差异 `[!note]`；引文对照新增第 30–37 行。 |
| 2026-10-06 | **补 3.3「可选凭据」的「夸克 cookie 怎么拿」**：夸克 cookie 无扫码，靠浏览器手抓——官方文档「`F12` → 网络 → 找一个带 `Cookie` 参数的请求 → 复制整串」（`sources/p5/alist-docs/01_raw_githubusercontent_com.md:47`），且**要用 Chrome**（`:63`）；补「`__puus` 约 3 小时过期、过期后下载 403」的官方 PR 依据（`sources/gh/alist-9596.md:11`）。引文对照新增第 38–40 行。 |
| 2026-10-06 | **整套笔记统一为 monlor 单一路线，删除官方镜像路线（第 2 篇）**：删去 3.3「另一条注入路线（文件）」小节（`mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt` 三件套与其放置说明）与 3.1 的凭据文件名 Callout；3.3「怎么拿」三行由文件名改为环境变量（`ALIYUN_TOKEN` / `ALIYUN_OPEN_TOKEN` / `ALIYUN_FOLDER_ID`）；夸克由「文件 `quark_cookie.txt` 或环境变量」收敛为**只用环境变量 `QUARK_COOKIE`**；3.2 删去「官方镜像容器内端口 5678 vs 80」来源冲突段，`5678` 行出处只留 `sources/forum/tid-9690.md:40`；WebDAV 由「官方 `guest`、monlor `dav` 两条并记」收敛为**用户名 `dav` + 默认密码 `guest_Api789` + 路径 `/dav`**（回源 `sources/p3/monlor-env/01_raw_githubusercontent_com.md:32`），原两条路线 Callout 改为「用户名是 `dav` 不是 `guest`」提醒；第 7 行纪律句、3.5 镜像 Callout、本章小结、下一章预告按第 4 章新章名回填。引文对照删除官方镜像页 2 条、文件凭据 4 条、端口冲突 1 条，共 10 行，重编号为 1–30。 |
| 2026-10-06 | **修正 WebDAV 默认用户：`dav` → `guest`（实战反证）**。原稿据 monlor env 注释「webdav用户名为dav」写成「用户名固定是 `dav`，不是 `guest`」，与实战相反。3.3.2 改为**用户名 `guest`、密码 `guest_Api789`、路径 `/dav`**；warning 改写为「用户名填 `guest`；`dav` 是**路径**不是用户名」；3.3.2 大白话与本章小结同步。新增独立来源回源 `sources/01_hub_docker_com.md:18`、`sources/forum/tid-9690.md:262`、`:280`、`sources/p3/z-addone/01_www_cnblogs_com.md:44`（引文对照新增第 31–33 行，第 8、12 行中译同步）；monlor env 注释出处由 `:32` 校正为 `:31`（注释在第 31 行，`:32` 为 `WEBDAV_PASSWORD=`）。 |
---

# 第 4 章 部署实战——单容器小雅（一键脚本）

## 本章要解决的问题

第 3 章备好了目录、端口、凭据三张清单，本章把**单容器**的小雅真正跑起来。本笔记改用社区整合脚本项目 `xiaoyaDev/xiaoya-alist`（作者 DDSRem）提供的**一键菜单脚本**：一条命令进终端菜单，选 `1 1`，脚本自己建目录、问凭据、拉镜像、起容器。一句话结论：**一条命令 + 一个菜单选择，得到的就是「只有 alist 一个容器」的纯净版小雅，全程不用手写 `docker-compose.yml`。**

## 4.1 为什么改用这个一键脚本

先交代换路线的背景。本笔记早期用的是社区维护者 monlor 的镜像（项目 `monlor/docker-xiaoya`），但那个项目**最后一次提交停在 2025-03-27**，此后近一年半没有再更新；而 `xiaoyaDev/xiaoya-alist` 一直在维护（最后一次提交 2026-10-06）。所以本章把部署主线换成后者——它同样给出单容器形态，而且把「建目录、填凭据、拉镜像、等启动」全包进了菜单。

| 维度 | 它的做法 | 出处 |
| --- | --- | --- |
| 维护方 | 社区整合脚本项目 `xiaoyaDev/xiaoya-alist`（作者 DDSRem） | `sources/01_raw_githubusercontent_com.md:33-34` |
| 一键命令 | 下载并运行整合脚本，进终端菜单逐级选 | `sources/01_raw_githubusercontent_com.md:39` |
| 容器镜像 | 内部使用**官方**镜像 `xiaoyaliu/alist` | `sources/xiaoyaDev/all_in_one.sh:1376` |
| 凭据注入 | 安装时**交互式**录入，落成配置目录下的 `.txt` | `sources/xiaoyaDev/all_in_one.sh:1230` |
| 部署形态 | 终端菜单选择，不用写 compose | `sources/01_raw_githubusercontent_com.md:66` |
| 单容器形态 | 菜单只选 `1 1`（不碰 Emby 全家桶 `2 1`） | `sources/01_raw_githubusercontent_com.md:75-76` |

> [!note] 「整合脚本」不等于「官方」
> 这两条线要分清，之后找文档才不会找错地方：
> - **官方**：镜像 `xiaoyaliu/alist`，作者是 xiaoyaLiu（站点 `alist.xiaoya.pro`），见 `sources/01_hub_docker_com.md:8`、`:18`。
> - **本笔记用的**：`xiaoyaDev/xiaoya-alist`，是一个**社区整合脚本**项目——README 自称「整合安装脚本，内置所有相关软件的安装」（`sources/01_raw_githubusercontent_com.md:33-34`）。它内部使用的正是上面那个官方镜像（`sources/xiaoyaDev/all_in_one.sh:1376`）。
>
> 所以本章的做法是「**社区整合脚本 + 官方镜像**」。顺带一提，README 只把 monlor 那条路线列在「小雅周边工具集合」里（`sources/01_raw_githubusercontent_com.md:295`）。

> [!tip] 大白话
> 把它想成**上门安装的师傅**：以前你得自己照着说明书买零件、装电池、接线（手写 compose + 逐个填环境变量）；现在打一个电话（跑脚本），师傅上门，一边问你一边装——问你东西放哪（配置目录）、要哪些账号（云盘凭据）、走哪种网络（host / bridge）、要不要设门禁（强制登入）——装完还替你试机（等日志出现成功标志才说「安装完成」）。

## 4.2 一键脚本部署（菜单 1 1）

### 一条命令进菜单

```bash
# 主命令
# 出处：sources/01_raw_githubusercontent_com.md:39
bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"
```

拉不动 `ddsrem.com` 时，README 还给了几个备用地址（`sources/01_raw_githubusercontent_com.md:45`、`:49`、`:53`），换其中任意一条即可。

进菜单后按 README 的规则逐级选：**数字代表先选哪一个、再选哪一个**（`sources/01_raw_githubusercontent_com.md:66-67`）。本笔记要跑单容器，选：

```text
安装 小雅Alist -> 1 1
# 出处：sources/01_raw_githubusercontent_com.md:75
```

对照一下：想做「Emby 全家桶」要走 `2 1`（`sources/01_raw_githubusercontent_com.md:76`）。**只选 `1 1`，就只装 alist 一个容器**——这就是本章说的单容器形态。

### 脚本会依次问你什么

安装过程是一个交互问答，问题不多，但每个都对应一个文件或一个开关。先看全表，再展开解释：

| 脚本里的问题 | 落到哪里 | 作用 | 出处 |
| --- | --- | --- | --- |
| 配置文件路径 | 默认 `/etc/xiaoya` | 所有配置文件的根目录 | `sources/xiaoyaDev/all_in_one.sh:156` |
| 阿里云盘 refresh token | `mytoken.txt` | 阿里云盘登录凭据 | `sources/xiaoyaDev/all_in_one.sh:569` |
| 阿里云盘 open token | `myopentoken.txt` | 开放接口令牌 | `sources/xiaoyaDev/all_in_one.sh:628` |
| 转存文件夹 ID | `temp_transfer_folder_id.txt` | 「转存」时把文件转到哪个目录 | `sources/xiaoyaDev/all_in_one.sh:948` |
| 夸克 Cookie | `quark_cookie.txt` | 夸克网盘分享区（可选） | `sources/xiaoyaDev/all_in_one.sh:740` |
| UC Cookie | `uc_cookie.txt` | UC 网盘分享区（可选） | `sources/xiaoyaDev/all_in_one.sh:259` |
| 115 Cookie | `115_cookie.txt` | 115 网盘分享区（可选） | `sources/xiaoyaDev/all_in_one.sh:292` |
| 是否开启强制登入 | `guestlogin.txt` + `guestpass.txt` | 给 WebDAV 加一道门禁 | `sources/xiaoyaDev/all_in_one.sh:1289-1330` |

前七项与第 3 章的凭据清单一一对应，只是**从「你自己写进环境变量」变成了「脚本问你、脚本落盘」**。

第八项要单独说清楚，因为它是笔记里最容易记混的一处：

> [!note] WebDAV 的账号到底是 `dav` 还是 `guest`？
> 取决于你有没有开**强制登入**——这是两个分支，不是两种说法：
> - **开了强制登入**（脚本默认选 `y`）：脚本会打印「强制登入用户名：dav（无法修改）」，用户名固定为 **`dav`**，密码是你在安装时自己设的那个（`sources/xiaoyaDev/all_in_one.sh:1304`、`:1401`）。
> - **没开强制登入**：回落到镜像自带的默认账号 **`guest`** / 密码 **`guest_Api789`**（官方镜像文档口径，`sources/01_hub_docker_com.md:18`）。
>
> 两条路径的 WebDAV 地址都是 `http://<你的IP>:5678/dav`。历史上「用户名是 `dav`」和「用户名是 `guest`」两种记录打架，根源就在这里：**`/dav` 是路径，`dav` 是强制登入的用户名**，两回事被记成了一件事。
>
> 建议开强制登入。脚本自己也提示了理由：不开的话「暴露到公网可能被坏人扫描到并无限制使用」，且「多人异地访问可能触发网盘风控甚至封禁账号」（`sources/xiaoyaDev/all_in_one.sh:1293-1294`）。

### 脚本实际执行了什么

确认完上面的问答，脚本会拼出这样一条 `docker run`（等价写法，参数取自脚本源码）：

```bash
# 脚本内部拼装的启动命令（等价示意）
# 出处：sources/xiaoyaDev/all_in_one.sh:1371-1392
docker run -itd --privileged \
  -p 5678:80 -p 2345:2345 -p 2346:2346 -p 2347:2347 \
  -v /etc/xiaoya:/data \
  -v /etc/xiaoya/data:/www/data \
  --restart=always \
  --name=xiaoya \
  xiaoyaliu/alist:latest
```

要点：

- **镜像**是 `xiaoyaliu/alist:latest`（官方镜像）。如果前面选了 host 网络，则改用 `xiaoyaliu/alist:hostmode` 并加 `--network=host`（`sources/xiaoyaDev/all_in_one.sh:1373`、`:1376`）。
- **端口方向仍是「左宿主、右容器」**：宿主 `5678` → 容器 `80`，另有 `2345` / `2346` / `2347`（`sources/xiaoyaDev/all_in_one.sh:1377`）。
- **配置目录**默认挂到容器 `/data`，其下的 `data/` 再挂到 `/www/data`（`sources/xiaoyaDev/all_in_one.sh:1392`）。
- **重启策略** `--restart=always`（同上）；**容器名**默认 `xiaoya`（`sources/xiaoyaDev/all_in_one.sh:5848`）。

> [!warning] 这套端口和第 3 章老清单不一样
> 本笔记早期（monlor 路线）用宿主端口 `5677`；**本路线用 `5678`**，且容器内是 `80` 而不是 `5678`。如果你之前照着旧教程配过端口转发、防火墙规则，或者机器上已经跑着占 `5678` 的服务，**先改这里**再往下走。

> [!tip] 镜像拉不动怎么办
> 脚本内置了镜像源选择：主菜单进高级配置选 `6 6`「Docker镜像源选择」（`sources/01_raw_githubusercontent_com.md:163`）。启动前脚本还会自己探一次镜像仓库是否可达，不通就提示你「请输入 66 进入 Docker 镜像源设置更改镜像源」（`sources/xiaoyaDev/all_in_one.sh:6232-6236`）。

> [!warning] 脚本要 root
> 在 Linux / NAS 上这个脚本必须以 **root** 运行；在 macOS 上反而要求**不能**是 root（`sources/xiaoyaDev/all_in_one.sh:6484`、`:6488`）。飞牛 OS 上按第 3 章的方式用 SSH 提权执行即可。

## 4.3 部署后自检：该看到什么

按顺序核对，能少走很多弯路：

1. **脚本说「安装完成」**。脚本不会装完就跑——它会轮询容器日志，直到出现 `success load storage: [/©️` 才判就绪（`sources/xiaoyaDev/all_in_one.sh:202`、`:204`）。
2. **脚本打印三个地址**（`sources/xiaoyaDev/all_in_one.sh:1398-1405`）：alist `http://ip:5678`、webdav `http://ip:5678/dav`、tvbox `http://ip:5678/tvbox/my_ext_jar.json`。记下 alist 那个。
3. **容器在跑**：`docker ps` 里能看到容器 `xiaoya`（重启策略 `always`）。
4. **首次打开网页仍可能先「失败」，这是正常的**。原帖写得很直白：

   > 「刚开始页面会显示“获取设置失败”，这是正常情况」（`sources/p3/gnz48/01_www_cnblogs_com.md:46`）

   论坛里同样有人遇到「一直提示……获取设置失败：请稍后，正在加载储存」，楼主的答复只有一句：「等一会儿就好了！」（`sources/forum/tid-9690.md:200`）。初始化按网络情况**需要 1~5 分钟**（`sources/p3/gnz48/01_www_cnblogs_com.md:46`），别当成故障。
5. **能播放**：在网页里随便点开一个视频，确认能播（`sources/p3/gnz48/01_www_cnblogs_com.md:69`）。
6. **WebDAV 能挂**：地址 `http://<你的IP>:5678/dav`，账号按 4.2 里那张 note 的两个分支填——开了强制登入就用 `dav` + 你自设的密码，没开才用 `guest` / `guest_Api789`。
7. **token 会过期**：出现「无法加载列表 / 播放失败」时，先更新 `mytoken.txt`（`sources/p2/newzone-xiaoya.md:33`）。

> [!warning] 一个高频报错：写 `/data` 被拒
> 容器启动时报 `/data/docker_address.txt: Operation not permitted`（`sources/forum/tid-9690.md:96`）——容器往配置目录写文件被拒，多为**目录权限**问题：检查 `${CONFIG_DIR}`（默认 `/etc/xiaoya`）的属主与读写权限，或确认它被正确挂到了容器 `/data`。这个文件是脚本写进去的、记录小雅自身地址用的（`sources/xiaoyaDev/all_in_one.sh:1367-1369`），不是可有可无的垃圾文件。

> [!tip] 大白话
> 小雅**第一次启动在「组装」**：它在拉取并索引资源目录，所以头几分钟网页打不开还报「获取设置失败」，就像新买的书柜还没装好、你急着往里塞书当然塞不进去。**等它装完**，再刷新就好了。

## 本章小结

- **本笔记用的是社区整合脚本** `xiaoyaDev/xiaoya-alist`（作者 DDSRem），它**不是官方**；它内部用的是**官方镜像** `xiaoyaliu/alist`。术语上分清这两层。
- **部署只有两步**：跑 `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"`，菜单选 `1 1`（安装 小雅Alist）。
- **单容器的含义**：只选 `1 1` 就只起 alist 一个容器；全家桶要走 `2 1`，本笔记不选。
- **脚本问你的东西都落成文件**：配置文件路径默认 `/etc/xiaoya`，凭据是 `mytoken.txt` / `myopentoken.txt` / `temp_transfer_folder_id.txt` 等。
- **端口**：宿主 `5678` → 容器 `80`，另有 `2345` / `2346` / `2347`；恒为「左宿主、右容器」。这与早期笔记的 `5677` 不同，务必留意。
- **WebDAV**：地址 `http://<IP>:5678/dav`；账号看有没有开**强制登入**——开了是 `dav` + 自设密码，没开是 `guest` / `guest_Api789`。
- **就绪由脚本判定**：等到日志出现 `success load storage: [/©️`；网页层仍可能先显示「获取设置失败」，等一会儿即可。
- **镜像拉不动**：菜单 `6 6` 换 Docker 镜像源。

**下一章预告**：小雅跑起来了，但飞牛影视默认还不认识它。第 5 章讲**前端接入**——为什么不能把整个小雅库直接喂给飞牛影视刮削，如何用 STRM 文件（只存 URL 指针）配合 302 直链把资源接进媒体库，以及 SmartStrm / MediaWarp / fntv-proxy 这几个工具各自站在哪一环。

## 引文对照（原文 / 中译 / 出处）

> 本章引用的逐字原文与说人话对照如下。本章原始来源以中文为主，「中译 / 说人话」列对中文原文给的是**复述**；配置项、路径、命令、文件名等保留原文。「出处」列写不出具名来源的记 `—`。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
| --- | --- | --- | --- |
| 1 | `整合安装脚本，内置所有相关软件的安装。` | 这是一个整合脚本，把相关软件都包进来了 | `sources/01_raw_githubusercontent_com.md:33-34` |
| 2 | `bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"` | 主命令：下载并运行整合脚本 | `sources/01_raw_githubusercontent_com.md:39` |
| 3 | `数字代表先选x，再选x，再选x` | 菜单是逐级选择，如 `2 2 8` = 先 2、再 2、最后 8 | `sources/01_raw_githubusercontent_com.md:66-67` |
| 4 | `安装 小雅Alist -> 1 1` | 只装小雅 Alist，就是菜单 `1 1` | `sources/01_raw_githubusercontent_com.md:75` |
| 5 | `安装 Emby全家桶（一键） -> 2 1` | 装全家桶走 `2 1`（本笔记不选） | `sources/01_raw_githubusercontent_com.md:76` |
| 6 | `Docker镜像源选择 -> 6 6` | 拉不动镜像时，进高级配置 `6 6` 换镜像源 | `sources/01_raw_githubusercontent_com.md:163` |
| 7 | `monlor/docker-xiaoya` | README 只把 monlor 列为「周边工具」，不是主线 | `sources/01_raw_githubusercontent_com.md:295` |
| 8 | `xiaoyaliu/alist:latest` | 脚本内部使用的官方镜像 | `sources/xiaoyaDev/all_in_one.sh:1376` |
| 9 | `-p 5678:80` | 宿主 5678 → 容器 80 | `sources/xiaoyaDev/all_in_one.sh:1377` |
| 10 | `-v ${CONFIG_DIR}:/data -v ${CONFIG_DIR}/data:/www/data` | 配置目录挂到容器 `/data`，其下 `data/` 再挂 `/www/data` | `sources/xiaoyaDev/all_in_one.sh:1392` |
| 11 | `TARGET_LOG_LINE_SUCCESS="success load storage: [/©️"` | 脚本以这条日志判定「已就绪」 | `sources/xiaoyaDev/all_in_one.sh:202` |
| 12 | `强制登入用户名：dav（无法修改）` | 开了强制登入，WebDAV 用户名固定为 `dav` | `sources/xiaoyaDev/all_in_one.sh:1304` |
| 13 | `默认用户密码: dav/guest_Api789` | 未开强制登入时脚本给出的提示 | `sources/xiaoyaDev/all_in_one.sh:1403` |
| 14 | `webdav 账号密码 用户: guest 密码: guest_Api789` | 官方镜像文档记的默认 WebDAV 账号 | `sources/01_hub_docker_com.md:18` |
| 15 | `刚开始页面会显示“获取设置失败”，这是正常情况` | 首次访问显示「获取设置失败」属正常 | `sources/p3/gnz48/01_www_cnblogs_com.md:46` |
| 16 | `等一会儿就好了！` | 对「获取设置失败」的答复：等一会儿 | `sources/forum/tid-9690.md:200` |
| 17 | `/data/docker_address.txt: Operation not permitted` | fnOS 用户常见报错：容器写配置目录无权限 | `sources/forum/tid-9690.md:96` |
| 18 | `出现"无法加载列表 / 播放失败"时先更新 token。` | token 过期会表现为加载/播放失败，先换 token | `sources/p2/newzone-xiaoya.md:33` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线由 monlor 镜像整体换为 xiaoyaDev/xiaoya-alist（DDSRem）一键菜单脚本**。4.1 替换原「为什么用 monlor 镜像」整节，改为「为什么改用这个一键脚本」（新增维护方/一键命令/容器镜像/凭据注入/部署形态/单容器形态六行表 + 「整合脚本 ≠ 官方」术语校正 note）；4.2 由「一键脚本 + 手写 Compose」改为「菜单 `1 1` 全程」，新增「脚本会依次问你什么」对照表（八项问答→落盘文件）与 WebDAV 双分支 note、实际 `docker run` 等价命令（端口改为宿主 `5678`→容器 `80`，新增 `2347`；配置目录默认 `/etc/xiaoya`；镜像 `xiaoyaliu/alist:latest`）、镜像源 `6 6` 与 root 要求两个 warning；删除原两张 monlor 界面截图（正文改纯文字+代码）。4.3 自检七点重排：就绪判定改为脚本内置等待（`success load storage: [/©️`），WebDAV 账号改用双分支写法，原 ghcr 拉取失败条目替换为镜像源条目。章名由「单容器小雅（monlor 镜像）」改为「单容器小雅（一键脚本）」。引文对照重编为 18 条，来源改挂 `sources/01_raw_githubusercontent_com.md`、`sources/xiaoyaDev/all_in_one.sh`、`sources/01_hub_docker_com.md` 与现象类来源；monlor 相关 9 条移出正文。 |
| 2026-10-06 | **整套笔记统一为 monlor 单一路线，删除官方镜像路线**：删去原 4.2「路线一：官方镜像 `xiaoyaliu/alist`」整节（含官方一键脚本 `docker.xiaoya.pro/update_new.sh`、社区 `docker run` 示例、容器内端口 `5678` vs `80` 的来源冲突段、整合脚本入口）；原 4.3 monlor 部署升为 **4.2**；原 4.1「两条镜像路线」与原 4.4「两条路线差异对照」合并重写为 **4.1 为什么用 monlor 镜像**（含维护方、凭据注入、编排、单容器形态、镜像地址五行表）；章名由「单容器小雅（两条镜像路线）」改为「单容器小雅（monlor 镜像）」。4.3 自检第 4 条 WebDAV 账号由「两条路线并记」收敛为 monlor 的 `dav` / `guest_Api789`（新增回源 `sources/p3/monlor-env/01_raw_githubusercontent_com.md:32`）。引文对照删除官方镜像相关 9 条（原第 1–8、13、14 行）并重编号为 1–11。 |
| 2026-10-06 | **修正 WebDAV 默认用户：`dav` → `guest`（实战反证）**。4.3 自检第 4 条「WebDAV 能挂」改为**用户名 `guest`、密码 `guest_Api789`、路径 `/dav`**（回源改 `sources/01_hub_docker_com.md:18`、`sources/forum/tid-9690.md:72`、`:280`）；本章小结「部署后自检五点」同步；引文对照第 5 行中译改注「注释里的 `dav` 实为**路径**」，其 monlor env 出处由 `:32` 校正为 `:31`（注释在第 31 行）。 |
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
3. 到「系统设置 → strm 设置 → 生成设置」，修改**基础地址**（基础地址填域名前缀，**结尾不能有斜杠 `/`，这里是因为`.strm` 里写的是**你手机/播放器要去请求的地址。如果你写 `192.168.1.100`，那只有在家里的局域网才找得到；你出门用 4G 就找不到——因为 `192.168.x.x` 是你家内网专用地址，公网根本不认识。所以这里需要填写你可以在外网也能使用的地址）；
![](assets/05%20前端接入/file-20261006213051252.png)
4. 「储存管理 → 添加储存」挂载网盘（夸克、115 等）；
这里就是把小雅的资源作为webdav放入
![](assets/05%20前端接入/file-20261006213307990.png)
5. 创建任务，选好储存与扫描路径，手动执行一次，在日志里看进度；
这里注意填写路径为/dav才能被发现
![](assets/05%20前端接入/file-20261006213345887.png)

![](assets/05%20前端接入/file-20261006213509562.png)

6. 去 STRM 目录确认文件已生成，打开一个 `.strm` 看看里面是不是你要的基础地址；

这里的strm是你你当时创建smartstrm容器是配置的路径不是你的小雅的webdav

![](assets/05%20前端接入/file-20261006220714767.png)

.strm最前面就是你之前配置的“基础地址”

![](assets/05%20前端接入/file-20261006220834978.png)
7. 给飞牛影视的 STRM 目录加权限，再添加媒体库刮削。


> [!note] SmartStrm 的 302 代理是收费的，生成 STRM 免费
> 教程特意说明：
>
> > 「此应用其中302代理是收费的，但是我们不需要使用，用它免费的挂载网盘生成strm功能就行了」（`sources/p2/tid-57134.md:32`）
>
> 也就是说，本章只用到它**生成 STRM** 的免费功能；真正做 302 转发的是 5.4 那两个专门的中间件。

## 5.4 让 302 串起来：MediaWarp 与 fntv-proxy 站在哪一环

STRM 生成了，还要有人把「客户端请求 → 302 跳到真实直链」这一环接上。**MediaWarp 和 fntv-proxy 站的是同一环**——都是夹在「飞牛影视服务端」和「客户端」之间的**前置反向代理**。位置一样，区别只在能力与配套。本节以 MediaWarp 为主，fntv-proxy 作轻量备选。

| 工具 | 定位原话 | 飞牛影视支持情况 | 关键端口 | 出处 |
| --- | --- | --- | --- | --- |
| **MediaWarp** | 「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」 | **已适配**（待办清单该项为 `[x] 适配 飞牛影视`） | 自定义（官方示例 `9000`） | `sources/lens-b/mediawarp/01_github_com.md:51`、`02_readme_todo.md:23` |
| fntv-proxy | 「飞牛影视 / Emby 代理工具 - 自动解析 .strm 文件并重定向到真实直链」 | 原帖称「基于飞牛影视 0.9.3 版本」 | 飞牛 `:28005` / Emby `:8095` | `sources/lens-b/fntvproxy/01_github_com.md:44`、`:45` |

> [!note] 一处旧结论的更正：MediaWarp 对飞牛影视**已经支持**
> 本笔记早前把 README 的「适配 飞牛影视」读成**待办项**，据此判「成熟度未决」。核对 raw Markdown 后确认，该行原文是 **`- [x] 适配 飞牛影视`（已完成）**，紧随的 `- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` 也已完成（`sources/lens-b/mediawarp/02_readme_todo.md:23`、`:24`）。误判根源是抓取存档在 HTML 转文本时丢了 checkbox 状态，把已完成项显示成了裸列表项。**更正结论：飞牛影视是 MediaWarp 的正式支持对象。**

### 5.4.1 为什么可以选 MediaWarp

MediaWarp 对自己的定位是一句话：

> 「MediaWarp 定位于服务端于客户端的一个中间件（也就是名字中为什么会带有 Warp），客户端请求原画播放时流量不再经过客户端，需要转码时服务端也能正确推流」（`sources/lens-b/mediawarp/03_blog_akimio_top.md:34`）

说人话：**能直连的就直连（302），直连不了的回退到服务器推流**——不是「一刀切禁止中转」，而是「尽量不让流量经过你的 NAS」。除了 302，它还能顺带提供（`sources/lens-b/mediawarp/02_readme_todo.md:38`）：

- **屏蔽特定客户端**（按 User-Agent 黑白名单）；
- **自定义 Web 前端样式 / 注入脚本**（弹幕、一起看等）；
- **AlistStrm 模式下，飞牛影视可播放网盘转码内容**（`[x]` 已完成，`sources/lens-b/mediawarp/02_readme_todo.md:24`）。

> [!warning] 一个例外：Web 页面美化对飞牛影视**不生效**
> 官方教程：「Web 页面修改 (Web) 支持 Emby 和 Jellyfin，FNTV（飞牛影视）不支持」（`sources/lens-b/mediawarp/03_blog_akimio_top.md:143`）。冲着「美化飞牛影视界面」去选 MediaWarp 会落空——它的价值在 **302 与播放链**上。

### 5.4.2 部署 MediaWarp（官方逐字骨架）

官方教程以 0.2.0 版为例，Docker Compose 部署：

```yaml
# docker-compose.yml（MediaWarp）
# 出处：sources/lens-b/mediawarp/03_blog_akimio_top.md:67-77
services:
  mediawarp:
    image: akimio/mediawarp:0.2.0
    container_name: MediaWarp
    restart: unless-stopped
    ports:
      - 9000:9000
    volumes:
      - ./mediawarp/config:/config
      - ./mediawarp/logs:/logs
      - ./mediawarp/static:/static
```

配置要映射进容器的 `/config` 目录。两条纪律：**配置文件只支持 YAML**（旧版的 JSON/TOML 已弃用）；「具体配置以发布对应版本中的 `config.yaml.example` 为准」（`sources/lens-b/mediawarp/03_blog_akimio_top.md:92`、`:86`）——版本间字段会变，以你下载版本内的示例为准。(这里你需要先去mediawarp这个项目把config.yaml.example放到你的项目改成config.yaml然后按你的需求进行修改)

对接飞牛影视，关键是把服务器类型写成 **`FNTV`**（`sources/lens-b/mediawarp/03_blog_akimio_top.md:98`、`:111`）——但**别只写 `type`**，`config.yaml` 的最小可用配置是下面几行：

```yaml
# config.yaml（MediaWarp 的配置文件，不是 docker-compose.yml）
# 出处：sources/lens-b/mediawarp/04_config_yaml_example.md:8-13
port: 9000                            # MediaWarp 监听端口（客户端要连的就是它）
server:                               # 媒体服务器相关设置
  type: FNTV                          # 对于飞牛影视
  addr: http://<飞牛影视地址>:8005     # 媒体服务器地址（FNTV 默认端口 8005，不是 Emby 的 8096）
  # auth 不用写——官方注释：FNTV 不需要这一项
```

这几个字段各有分工（`sources/lens-b/mediawarp/04_config_yaml_example.md:8`、`:12`、`:13`）：

| 字段 | 管什么 | 取值 |
| --- | --- | --- |
| `port` | MediaWarp 自己的**监听端口** | 示例 `9000`；**客户端要连的就是它** |
| `server.type` | 前面站的是哪种媒体服务器 | 飞牛影视写 `FNTV` |
| `server.addr` | **真正的飞牛影视在哪** | 官方示例是 Emby 的 `http://localhost:8096`；注释点明 **FNTV 默认端口 8005** |
| `server.auth` | 媒体服务器认证 | FNTV **不需要**这一项 |

> [!warning] 漏了 `server.addr`，MediaWarp 用不起来
> 只写 `server.type`，只是告诉它「类型是飞牛影视」，**没告诉它飞牛影视在哪**，请求无处转发。`addr` 要填你飞牛影视的地址与端口（FNTV 默认 `8005`，以实机为准）。改完 `config.yaml` 记得**重启容器**才生效。

> [!warning] `server.type` 属于 `config.yaml`，别贴进 `docker-compose.yml`
> 上面两个代码块是**两个不同的文件**，不要拼成一个：
>
> - `services:` 那一块是 **`docker-compose.yml`**；
> - `server: type: FNTV` 这一段是 MediaWarp 的**配置文件 `config.yaml`**——「需要映射进容器的 `/config` 目录下」（`sources/lens-b/mediawarp/03_blog_akimio_top.md:54`），也就是宿主机映射到容器 `/config` 的那个目录（如 `./mediawarp/config/config.yaml`），由 MediaWarp 自己读取。
>
> 常见错误：把 `server: type: FNTV` 直接贴到 `docker-compose.yml` 顶层。实测会报错，`docker compose config` 的输出是：
>
> ```text
> additional properties 'server' not allowed
> ```
>
> （`server` 不是 Compose 的合法顶层键）**一句话：compose 文件里只放 `services`；`server.type` 归 `config.yaml`。**
>
> 另外，`volumes:` 左侧是**宿主机路径**，写 `./mediawarp/config` 或 `/vol2/1000/download/mediawarp/config` 都可以，只要该目录真实存在。

### 5.4.3 选哪种 STRM 模式：HTTPStrm 还是 AlistStrm

MediaWarp 认两种 STRM 内容形态，**取决于你的 `.strm` 里写的是什么**（`sources/lens-b/mediawarp/02_readme_todo.md:44`、`:45`）：

| 模式 | STRM 内容 | 谁需要能访问到目标 | 备注 |
| --- | --- | --- | --- |
| **HTTPStrm** | 一个 HTTP 链接 | **客户端**要能访问该链接；MediaWarp 不必 | 与本章 5.3 用 SmartStrm 生成的「基础地址 + 路径」相符 |
| **AlistStrm** | AList 上视频文件的路径（utf-8 编码） | **MediaWarp** 要能访问 AList 及其 `raw_url`；客户端不必 | 仅支持 AList v3 API（OpenList 兼容）；**不支持转码**、兼容性较差，可挂真实目录缓解 |

两条实用建议：客户端在公网、Alist 在内网时，AlistStrm 的 `raw_url` 建议设为 `true`（直接回网盘直链，客户端不必访问 AList，`sources/lens-b/mediawarp/03_blog_akimio_top.md:133`）；若 `.strm` 只是普通 HTTP(S) 链接，就用 HTTPStrm，并**关掉 AlistStrm**。

> [!tip] 把 302 直链想成**快递中转**
> 包裹（视频）一直放在网盘仓库，从来不用搬进你家。客户端下单后，中间件只回一句「你去仓库这个门牌直接取」。中转站本身**不囤货**——只在 NAS 上占一点点流量，不占你的硬盘。**选谁做中转站，看你要不要它有额外功能**：只要 302 选 fntv-proxy；想要屏蔽客户端 / 注入脚本 / 飞牛侧网盘转码，选 MediaWarp。

### 5.4.4 fntv-proxy：更轻的备选

只要「STRM → 302」这一件事，fntv-proxy 更轻。用法很直接：

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

> [!warning] STRM 目录必须挂进中间件容器（两个工具都适用）
> 工具文档专门加粗提醒：
>
> > 「strm 路径一定要挂载到 Docker 容器中，否则播放失败，找不到 strm 文件。」（`sources/lens-b/fntvproxy/01_github_com.md:139`）
>
> 而且挂载时**前后路径要一致**（宿主机是什么路径，容器内就写什么路径）。

### 5.4.5 装完不等于用上：让客户端改连中间件端口

MediaWarp 是**前置反向代理**——「前置于 EmbyServer/Jellyfin/飞牛影视 的反向代理服务器」（`sources/lens-b/mediawarp/01_github_com.md:51`）。它不改变飞牛影视本身，而是让你**从它这扇门进**。所以部署完还有最后一步：**把客户端的服务器地址，改成 MediaWarp 的监听端口**。

```text
客户端（飞牛影视 App / Infuse / Fileball / Vidhub …）
        │  服务器地址填 http://<NAS 的 IP 或域名>:9000   ← 走 MediaWarp
        ▼
   MediaWarp:9000 ──(strm 播放)──▶ 302 跳到网盘直链（流量不经 NAS）
        │
        └──(直连不了)──▶ 回退转发给飞牛影视（server.addr）推流
```

- **必须走 `port` 那个口（示例 `9000`）**；若继续用飞牛影视原来的端口，播放照样经过 NAS、照样吃上行带宽。
- 这与 fntv-proxy 的用法同构——它也是「将播放器地址指向代理端口（飞牛 `:28005`，Emby `:8095`）」（`sources/lens-b/fntvproxy/01_github_com.md:71`）。
- 前提：`port` 已**映射到宿主机**（5.4.2 的 compose 里 `9000:9000` 已做）；若改成 bridge 网络又换过端口，端口映射要同步改。

> [!note] 直连不了会「回退」是正常设计
> 客户端因浏览器跨域拦截、需要转码、或不支持该编码（如 H265）而**无法直连**时，MediaWarp 会把请求**转发回飞牛影视推流**，此时流量才再次经过 NAS（`sources/lens-b/mediawarp/03_blog_akimio_top.md:32`）。所以偶尔走 NAS 不是故障，是兜底。

> [!tip] 验证有没有生效
> 播一个由 SmartStrm 生成（5.3）的小雅 STRM 影片，应是**秒开、拖进度快**，且顺着 `:9000` 这个口进去、流量 302 出去不经过 NAS；去 MediaWarp 的日志里能确认。

## 5.5 纪律：只挂 STRM 子目录，并把它挂进中间件

把本章的两条纪律合起来记：

1. **对飞牛影视**：媒体库指到 STRM 子目录，别挂整个小雅库（5.1）。
2. **对中间件容器**：STRM 目录要挂进容器，且宿主机/容器路径一致（5.4）。

这两条落定后，整条链路就是：**网盘 → 小雅（AList）→ SmartStrm 生成 STRM → 中间件（302）→ 飞牛影视客户端**。

关于播放端的解码能力（要不要硬解、用哪种客户端），可参看 [[流媒体与影音/硬件解码vs软件解码]]。

## 5.6 没有阿里云盘会员、只有夸克会员怎么办

前几节都默认你有阿里云盘。如果你的情况是「**没有阿里云盘会员，主要靠夸克会员**」，这一节先把一件事说准：**小雅里确实有夸克的东西**——它自带一块**夸克分享区**（挂载目录 `/🌀我的夸克分享`），配好夸克 cookie 后，这一区**走夸克直链、吃夸克会员速度**；但小雅**本体库**（阿里 / 115）**没法转成夸克播放**。这两件事必须分开看，混起来就会得出「夸克根本用不上」的错误结论。

### 5.6.1 先分清：小雅「要账号」≠「要会员」

**① 小雅单容器必须要一个阿里云盘账号。** 原因藏在它的播放机理里：

> 「由于小雅本质是将别人阿里云盘的文件先转存到自己的阿里云盘内再进行播放，如此当时间久了就会是云盘空间不足」（`sources/p3/z-addone/01_www_cnblogs_com.md:33`）

早期小雅播放时，是把片源**转存进你自己的阿里云盘**，302 直链最终指向的是**阿里云盘上的那个文件**。所以第 3 章的「阿里云盘三件套」是**必填**，填的也是你自己的阿里云盘：

> 「`ALIYUN_TOKEN` `ALIYUN_OPEN_TOKEN` `ALIYUN_FOLDER_ID` 这三个是必填项」（`sources/01_club_fnnas_com.md:32`）

**② 但「必填账号」不等于「必须有会员」**——会员只决定**快不快**：

> 「现在在用alist tvbox，但是没有阿里或者115会员的话，会限速到100k」（`sources/forum/tid-21673.md:13`）

而且即使开了会员，速度也不见得多稳：

> 「115和夸克设置自己的token就可以了。没有115会员的话还是放弃吧。115速度时快时慢，体验差。」（`sources/forum/tid-21673.md:11`）

**一句话**：没有阿里云盘会员，小雅照样能装、能看，但大概率被限速、体验差——所以你想借夸克会员的速度，方向是对的。

### 5.6.2 先搞清「小雅的片放在哪」：本体库 + 分享区（含夸克）

要借夸克的速度，先得知道夸克的片在小雅的**哪一层**。小雅的资源分**两类**：

| 类别 | 放在哪 | 播放时走哪个盘 |
| --- | --- | --- |
| **本体资源（主库）** | 小雅自己的**阿里云盘 + 115 网盘** | 阿里 / 115 |
| **分享资源** | **阿里分享 / 115分享 / 夸克分享 / PikPak 分享** 等 | 各自来源盘（**夸克分享就走夸克**） |

「分享区」在小雅里对应几个带 emoji 的目录，AList-TvBox 的一份 issue 把它们列得很清楚：

| 分享区目录 | 列表文件 | 来源盘 |
| --- | --- | --- |
| `/🈴我的阿里分享` | `alishare_list.txt` | 阿里 |
| `/🏷️我的115分享` | `115share_internal.txt` | 115 |
| **`/🌀我的夸克分享`** | **`quarkshare_list.txt`** | **夸克** |
| `/🕸️我的PikPak分享` | `pikpakshare_list.txt` | PikPak |

> 「index.quark.txt #夸克分享（通过手动在资源中添加小雅资源配置 data 目录中的 quarkshare_list.txt ，挂载目录为 /🌀我的夸克分享）」（`sources/gh/alist-tvbox-721.md:33`）

**关键就在这一行**：`/🌀我的夸克分享` 这一区里的片**就在夸克上**，播放时走的是**夸克直链**——也就是说，**你能用上夸克会员的速度**。

而**本体资源**那一层，最初全在阿里云盘，后来变了：

> 「于是乎小雅开始转战115网盘，因为115有个转存阿里云盘的功能，简单来说就是，如果这个阿里的资源在115网盘上也有，会立即转存到你自己的网盘中。这样就跳过了阿里云盘的限制。当然115这边也有限制，需要开通会员才可以实现这个功能。而且最新的很多资源小雅都放到了115网盘中，所以想要玩小雅Alist，必须要办个115会员了。」（`sources/p4/ycyc-2878.md:13`）

绕开阿里限速的套路是「**阿里转存 115**」，落地文件是 `ali2115.txt`；**本笔记用的整合脚本已经把这一项做进了菜单**——账号管理里就有「6、阿里转存115播放（ali2115.txt）」，后面跟着 `未配置 / 已配置` 的状态（`sources/xiaoyaDev/all_in_one.sh:1154`）；选中后会问一句「是否配置 阿里转存115播放（ali2115.txt）」（`sources/xiaoyaDev/all_in_one.sh:912`），确认后脚本把 115 cookie、`purge_pan115_temp`、`dir_id` 写进 `ali2115.txt`（`sources/xiaoyaDev/all_in_one.sh:895`）：

> 「这个文件是用来加速阿里云盘资源的，如果你没有办理阿里云盘的会员，但是有115的会员，可以配置这个文件来转存阿里的资源到115网盘，实现流畅观看视频。」（`sources/p4/ycyc-2878.md:19`）

也就是说，**「把本体库换别的盘播放」的开关只有 115，没有夸克**——这一点 5.6.3 会再钉一次。

### 5.6.3 夸克在小雅里的两条正路，和一条走不通的路

关于夸克，把三件事一次分清。

**正路 ①：小雅的夸克分享区（`/🌀我的夸克分享`）** —— 这是「**小雅里自带的夸克片**」，配好夸克 cookie 后走夸克直链，**正是你想借的夸克会员速度**。

**正路 ②：挂你自己的夸克**（配置文件 `quark_cookie.txt`，或环境变量 `QUARK_COOKIE`）—— 让小雅能列出、播放**你自己夸克账号里**的东西：

> 「如有挂载夸克、115网盘的需求，也可以在配置文件里填写参数」（`sources/01_club_fnnas_com.md:32`）

> 「1、在小雅 alist 的配置目录下增加 quark_cookie.txt 文件，填入夸克账户的 cookie 并保存；」（`sources/forum/tid-8385880.md:26`）

**走不通的那条：把小雅的「本体库」（阿里 / 115）转成夸克播放。** 小雅**没有**「转存夸克」这个开关（只有 `ali2115.txt` 这条「阿里转存 115」）。社区有人实测过：

> 「我查日志发现，夸克cookie放进去etc/xiaoya，查日志还是只有阿里的直链，没有夸克的直链。」（`sources/forum/tid-8385880.md:30`）

论坛里也有人问过「只填夸克、不填阿里三件套行不行」，帖子过去**没有**给出正面回答（`sources/01_club_fnnas_com.md:732`）——按官方口径，阿里三件套仍是**必填**。

**一句话**：**本体库走不了夸克，但夸克分享区能走夸克**。所以「只有夸克会员」≠「用不上小雅里的夸克片」。

> [!warning] 但别把夸克分享区当成「片海」——覆盖没有保证
> 小雅自带不止一份索引，可它**默认只加载一部分**（如 `index.video.txt`、`index.share.txt` 等）；**夸克分享索引很可能不在默认之列**，要你手动把 `quarkshare_list.txt` 放进小雅的 data 目录才挂得上——原话是「在使用小雅资源的时候，只使用了部分索引数据，导致很多挂载的资源无法被搜索到，例如小雅的夸克分享索引，115分享索引以及部分电影等。」（`sources/gh/alist-tvbox-721.md:16`）。
>
> 同一份 issue 还明说小雅的索引数据「有大量目录路径实际不存在……大部分在三级或四级目录前就已经失效」（`sources/gh/alist-tvbox-721.md:39`）。
>
> 所以夸克分享区**有多少片、能不能搜到，以你实机为准**——这也解释了为什么有人配了 cookie 仍只看到阿里直链（`sources/forum/tid-8385880.md:30`）。

> [!tip] 大白话
> 把 302 想成**快递中转**：仓库（网盘）永远不搬进你家，NAS 只当「目录 + 海报墙 + 中转站」，你能挑的是「**这单从哪家仓发货**」。小雅的**主库**记在阿里 / 115 名下，你**改不了单**（没有「转夸克」入口）；但小雅**另设了一个「夸克仓」窗口**（`/🌀我的夸克分享`），那一窗口的货**就从夸克发**——你手里的夸克会员卡，正好用在这个窗口上。

### 5.6.4 主要用夸克，你实际能走的四条路

| 你想怎样 | 走哪条 |
| --- | --- |
| **借夸克会员速度，看小雅里的夸克片** | **用小雅夸克分享区**：配 `QUARK_COOKIE`，看 `/🌀我的夸克分享`（走夸克直链）；**覆盖多少以实机为准** |
| 看**你自己夸克账号**里的片 | **挂你自己的夸克**：`quark_cookie.txt` / `QUARK_COOKIE`；或干脆改挂你的夸克库（见 5.6.5） |
| 就用小雅本体库、能接受限速 | 小雅照装（三件套必填），不开阿里会员，接受限速（社区实测可低到 ~100KB/s，`sources/forum/tid-21673.md:13`） |
| 就用小雅本体库、想要不卡 | **办 115 会员**，配 `ali2115.txt` 走「阿里转存 115」（`sources/p4/ycyc-2878.md:13`） |

> [!warning] 115 路线也不是万无一失
> 有用户反馈 115 转存直接报「非115会员不支持此操作」，而且**大于 5G 的文件不转**（甚至 5G 以下也报）（`sources/forum/tid-8385880.md:32`、`:34`）。这条链路能让本体库跑起来，但别当成百发百中。

另外，两个盘都没有会员时会被限速到 ~100k（`sources/forum/tid-21673.md:13`）；论坛也有人直说「115和夸克设置自己的token就可以了。没有115会员的话还是放弃吧。115速度时快时慢，体验差。」（`sources/forum/tid-21673.md:11`）

### 5.6.5 备选：干脆改挂「你自己的夸克库」

如果你想看的**主要是你自己夸克里的片**（而不是小雅主库的片），那 5.3～5.4 这套「挂网盘 → 生成 STRM → 中间件 302 → 飞牛影视」对**你自己的夸克库**同样适用——**小雅不是唯一方案**：

1. 用**「夸克网盘 TV」驱动**挂上你的夸克——SmartStrm 的储存管理就支持挂「**夸克、115、天翼、123 等**」（`sources/p2/tid-57134.md:32`，即 5.3 步骤 4）；
2. STRM 生成目录、基础地址等设置同 5.3；
3. 中间件继续用 **fntv-proxy**——它的定位本就是「**主要针对夸克网盘**」：

> 「飞牛代理主要针对 **夸克网盘** 在 **openlist** 的 **夸克 TV 驱动** 挂载下实现 302」（`sources/lens-b/fntvproxy/01_github_com.md:300`）

也就是说，这条链路除了「片源从小雅主库换成你自己的夸克库」，**其余与第 5 章完全一致**——而会员正好落在你已有的夸克上。

> [!warning] 夸克路线的专属坑：部分片源只有 HLS 流，取不到元数据
> 夸克 CDN 对**部分**内容只返回 **HLS 转码流**（`media.m3u8`）而不是 mp4 文件直链，飞牛/Emby 因此**取不到时长、码率、分辨率**。**代理只做透明 302，不会把 HLS 转成 mp4，也无法凭空补全元数据**（`sources/lens-b/fntvproxy/01_github_com.md:241`）。
> 应对：用 **TMDB 外部刮削**补时长/分辨率（不依赖文件 probe），也就是 5.1 说的「让飞牛自己按需刮削」。

## 本章小结

- **别整库刮削**：媒体库只挂 STRM 子目录，避免触发小雅的转存与风控（`sources/forum/tid-40446.md:33`、`:161`）。
- **STRM = 一行 URL 的指针文件**：「strm 只是 URL 指针」（`sources/lens-b/fntvproxy/01_github_com.md:266`），媒体文件始终在网盘。
- **生成 STRM 用 SmartStrm**：应用中心（滞后 1~2 版）或 Docker（版本更及时）；生成免费，302 代理收费、本章不用。
- **基础地址决定外网可用性**：默认写局域网 IP 就只能内网；外网要填可公网访问的地址。
- **接 302 用中间件**：**MediaWarp**（**已适配飞牛影视**，README 待办清单该项为 `[x]`；对接飞牛把 `server.type` 写 `FNTV`）作首选；fntv-proxy（原帖称基于飞牛影视 0.9.3，播放器指向 `:28005`）作轻量备选。两者站**同一环**（客户端 ↔ 飞牛影视之间的前置反向代理）。STRM 目录必须挂进容器且前后路径一致。

- **没有阿里云盘会员、主要用夸克**：小雅必填的是阿里云盘**账号**、会员只影响速度（`sources/forum/tid-21673.md:13`）；夸克在小雅里有**两条正路**——**小雅的夸克分享区**（`/🌀我的夸克分享`，走夸克直链、吃夸克会员速度，`sources/gh/alist-tvbox-721.md:33`）与**挂你自己的夸克**（`QUARK_COOKIE`，`sources/forum/tid-8385880.md:26`）；但**本体库**没有「转夸克」开关，只能「阿里转存 115」（需 115 会员，`sources/p4/ycyc-2878.md:13`）。夸克分享区的实际覆盖以实机为准（索引默认未必加载，`sources/gh/alist-tvbox-721.md:16`、`:39`）。详见 5.6。

**下一章预告**：路走通了不等于走得稳。第 6 章把社区帖里反复出现的五类坑集中成「症状 → 原因 → 怎么避」——装错地方、整库刮削触发风控、外网播放失败、播放器 UA 不对就 403，以及 WebDAV 的端口与用户名写错，逐条讲清。

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
| 14 | `- [x] 适配 飞牛影视` | MediaWarp 已完成对飞牛影视的适配（待办清单勾选项） | `sources/lens-b/mediawarp/02_readme_todo.md:23` |
| 15 | `- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` | 飞牛影视 AlistStrm 模式下支持播放网盘转码内容（已完成） | `sources/lens-b/mediawarp/02_readme_todo.md:24` |
| 16 | `MediaWarp 定位于服务端于客户端的一个中间件（也就是名字中为什么会带有 Warp），客户端请求原画播放时流量不再经过客户端，需要转码时服务端也能正确推流` | MediaWarp 是客户端与服务端之间的中间件：原画播放不经过 NAS，需要转码时再由服务器推流 | `sources/lens-b/mediawarp/03_blog_akimio_top.md:34` |
| 17 | `Web 页面修改 (Web) 支持 Emby 和 Jellyfin，FNTV（飞牛影视）不支持。` | Web 页面美化支持 Emby/Jellyfin，飞牛影视不支持 | `sources/lens-b/mediawarp/03_blog_akimio_top.md:143` |
| 18 | `飞牛影视 / Emby 代理工具 - 自动解析 .strm 文件并重定向到真实直链` | fntv-proxy 的定位：解析 STRM 并重定向到真实直链 | `sources/lens-b/fntvproxy/01_github_com.md:44` |
| 19 | `基于飞牛影视 0.9.3 版本` | fntv-proxy 原帖称基于飞牛影视 0.9.3 | `sources/lens-b/fntvproxy/01_github_com.md:45` |
| 20 | `将播放器地址指向代理端口（飞牛 :28005，Emby :8095）` | 播放器应连代理端口：飞牛 :28005，Emby :8095 | `sources/lens-b/fntvproxy/01_github_com.md:71` |
| 21 | `strm 路径一定要挂载到 Docker 容器中，否则播放失败，找不到 strm 文件。` | STRM 目录必须挂进容器，否则找不到文件、播放失败 | `sources/lens-b/fntvproxy/01_github_com.md:139` |
| 22 | `由于小雅本质是将别人阿里云盘的文件先转存到自己的阿里云盘内再进行播放，如此当时间久了就会是云盘空间不足` | 小雅本质是把片源转存进你自己的阿里云盘再播放，久则空间不足 | `sources/p3/z-addone/01_www_cnblogs_com.md:33` |
| 23 | `是否配置 阿里转存115播放（ali2115.txt） [Y/n]（默认 n 不配置）` | 脚本菜单里确认「要不要配阿里转存 115」（默认不配） | `sources/xiaoyaDev/all_in_one.sh:912` |
| 24 | `6、阿里转存115播放（ali2115.txt）` | 整合脚本账号管理菜单里的「阿里转存 115」项（后面显示 已配置 / 未配置） | `sources/xiaoyaDev/all_in_one.sh:1154` |
| 25 | `如有挂载夸克、115网盘的需求，也可以在配置文件里填写参数` | 夸克/115 属「按需额外挂载」，非必填 | `sources/01_club_fnnas_com.md:32` |
| 26 | `QUARK_COOKIE: "" # 夸克网盘的 Cookie，需要用户填写，非必填。` | 配置里夸克 Cookie 明确标「非必填」 | `sources/01_club_fnnas_com.md:48` |
| 27 | `如果用夸克上面是不是只填写夸克的Cookie就可以了？就不需要填写阿里云盘的那三个参数了吧？` | 社区同问：只填夸克能否免填阿里三件套（帖中无正面回答） | `sources/01_club_fnnas_com.md:732` |
| 28 | `echo -e "cookie=\"${set_115_cookie}\"\npurge_pan115_temp=${purge_pan115_temp}\ndir_id=${dir_id}" > ${1}/ali2115.txt` | 脚本把 115 cookie、purge 开关、dir_id 三行写进 `ali2115.txt` | `sources/xiaoyaDev/all_in_one.sh:895` |
| 29 | `飞牛代理主要针对 夸克网盘 在 openlist 的 夸克 TV 驱动 挂载下实现 302` | fntv-proxy 主要面向夸克网盘（OpenList 夸克 TV 驱动） | `sources/lens-b/fntvproxy/01_github_com.md:300` |
| 30 | `代理只做透明 302 转发，不会 把 HLS 转成 mp4，也无法 凭空补全媒体库元数据。` | 代理只做 302，不转 HLS、不补元数据 | `sources/lens-b/fntvproxy/01_github_com.md:241` |
| 31 | `于是乎小雅开始转战115网盘，因为115有个转存阿里云盘的功能，简单来说就是，如果这个阿里的资源在115网盘上也有，会立即转存到你自己的网盘中。这样就跳过了阿里云盘的限制。当然115这边也有限制，需要开通会员才可以实现这个功能。而且最新的很多资源小雅都放到了115网盘中，所以想要玩小雅Alist，必须要办个115会员了。` | 小雅转战 115：115 有「转存阿里云盘」功能，播放时把资源转存到你的 115、绕开阿里限速，需 115 会员 | `sources/p4/ycyc-2878.md:13` |
| 32 | `这个文件是用来加速阿里云盘资源的，如果你没有办理阿里云盘的会员，但是有115的会员，可以配置这个文件来转存阿里的资源到115网盘，实现流畅观看视频。` | `ali2115.txt` 的作用：没阿里会员但有 115 会员时，把阿里资源转存到 115 播放 | `sources/p4/ycyc-2878.md:19` |
| 33 | `115和夸克设置自己的token就可以了。没有115会员的话还是放弃吧。115速度时快时慢，体验差。` | 论坛回复：115 / 夸克各填自己的 token；没有 115 会员就放弃 | `sources/forum/tid-21673.md:11` |
| 34 | `现在在用alist tvbox，但是没有阿里或者115会员的话，会限速到100k` | 没有阿里或 115 会员会被限速到 100k | `sources/forum/tid-21673.md:13` |
| 35 | `1、在小雅 alist 的配置目录下增加 quark_cookie.txt 文件，填入夸克账户的 cookie 并保存；` | 「小雅夸克玩法」：加 `quark_cookie.txt` 挂载自己的夸克 | `sources/forum/tid-8385880.md:26` |
| 36 | `我查日志发现，夸克cookie放进去etc/xiaoya，查日志还是只有阿里的直链，没有夸克的直链。` | 实测：填了夸克 cookie，日志里仍只有阿里直链、没有夸克直链 | `sources/forum/tid-8385880.md:30` |
| 37 | `已经不行了，日志提示非115会员不支持此操作` | 115 转存报「非115会员不支持此操作」 | `sources/forum/tid-8385880.md:32` |
| 38 | `如果刚好有115会员能行吗，它这个大于5G不支持是会员也不行吗` | 反馈：115 转存「大于 5G 不支持」，会员也存疑 | `sources/forum/tid-8385880.md:34` |
| 39 | `index.quark.txt #夸克分享（通过手动在资源中添加小雅资源配置 data 目录中的 quarkshare_list.txt ，挂载目录为 /🌀我的夸克分享）` | 小雅有专门的**夸克分享区**，挂载目录 `/🌀我的夸克分享`，列表文件 `quarkshare_list.txt` | `sources/gh/alist-tvbox-721.md:33` |
| 40 | `在使用小雅资源的时候，只使用了部分索引数据，导致很多挂载的资源无法被搜索到，例如小雅的夸克分享索引，115分享索引以及部分电影等。` | 小雅索引**默认只加载一部分**，夸克分享索引等常搜不到 | `sources/gh/alist-tvbox-721.md:16` |
| 41 | `小雅资源自己的索引数据有大量目录路径实际不存在，并且大部分在三级或四级目录前就已经失效` | 小雅的索引数据大量路径实际不存在，多在三四级目录前失效 | `sources/gh/alist-tvbox-721.md:39` |
| 42 | `随后需要映射进容器的/config目录下` | MediaWarp 的 `config.yaml` 需映射进容器 `/config` 目录（不是写进 compose） | `sources/lens-b/mediawarp/03_blog_akimio_top.md:54` |
| 43 | `port: 9000                                  # MideWarp 监听端口` | MediaWarp 监听端口（示例 9000）；客户端要连的就是它 | `sources/lens-b/mediawarp/04_config_yaml_example.md:8` |
| 44 | `  addr: http://localhost:8096               # 媒体服务器地址（FNTV默认端口号为8005而不是5666）` | 媒体服务器地址；注释点明 **FNTV 默认端口 8005** | `sources/lens-b/mediawarp/04_config_yaml_example.md:12` |
| 45 | `  auth: 2eaxxxxxxxxxa8                      # 媒体服务器认证方式（FNTV不需要这一项）` | 媒体服务器认证；FNTV **不需要** | `sources/lens-b/mediawarp/04_config_yaml_example.md:13` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线换为 xiaoyaDev/xiaoya-alist（DDSRem）整合脚本，5.6 的「限速 / 转存 115」口径换源（第 5 篇）**。5.6.1 ②的两条论据不再取 monlor 博客评论区（`p2/monlor-144.md:273`、`:279`），改挂论坛实测（`forum/tid-21673.md:13` 没会员限速 100k、`:11` 会员也「时快时慢」）。5.6.2 的「换播放盘」开关由环境变量 `ALIYUN_TO_115`（`p3/monlor-env/01_raw_githubusercontent_com.md:19`）改为**整合脚本菜单项**「6、阿里转存115播放（ali2115.txt）」（`all_in_one.sh:1154`、`:912`、`:895`），说明脚本已把该配置做进账号管理。引文对照第 23/24/28 行同步换源为 `all_in_one.sh`。前端工具链（SmartStrm / MediaWarp / fntv-proxy）与 STRM / 302 链路未动。另因第 6 章新增「坑五 WebDAV 端口与用户名」，本章「下一章预告」由「四类坑」改为「五类坑」（第 6 篇章名同步扩为「…、UA 与登录」）。另将 5.4.2 的 `docker compose config` 报错原文改为带语言标识的代码块（命令输出不是散文引文），并同步调整 2026-10-06 行的措辞。 |
| 2026-10-06 | 5.4.2 补全 `config.yaml` **最小可用配置**（`port` / `server.type` / `server.addr` / `auth`）与字段分工表，并加「漏 `server.addr` 用不起来」警告；新增 **5.4.5**「装完不等于用上：让客户端改连中间件端口（示例 `9000`）」，含链路图、回退说明与验收；新增来源存档 `sources/lens-b/mediawarp/04_config_yaml_example.md`（官方 `config.yaml.example` 逐字）；引文对照表加 43–45 行。 |
| 2026-10-06 | 5.4.2 补一条实操警告：MediaWarp 的 `server: type: FNTV` 属于**配置文件 `config.yaml`**（映射进容器 `/config`，`sources/lens-b/mediawarp/03_blog_akimio_top.md:54`），**不能**贴进 `docker-compose.yml` 顶层；实测 `docker compose config` 会报 `server` 不是合法顶层键（原文见 5.4.2 的输出块）。同时说明 `volumes:` 左侧宿主机路径可自定义。引文对照表加第 42 行。 |
| 2026-10-06 | **口径修正（MediaWarp）**：更正 5.4——此前把 MediaWarp README 的「适配 飞牛影视」读成**待办项**，据此判「成熟度未决」。核对 raw Markdown 后确认该行为 `- [x] 适配 飞牛影视`（已完成），`- [x] 支持播放网盘转码内容（仅飞牛影视 AlistStrm 模式）` 亦已完成（`sources/lens-b/mediawarp/02_readme_todo.md:23`、`:24`）；误判根源是旧抓取存档丢失 checkbox 状态。5.4 改写为**以 MediaWarp 为主**：补 `server.type: FNTV`、HTTPStrm/AlistStrm 选择、官方 Compose 骨架与「Web 美化不支持 FNTV」例外；fntv-proxy 降为轻量备选。引文对照表同步（原 14 行改为 `[x]` 口径并新增 15–17）。 |
| 2026-10-06 | 新增/重写 5.6「没有阿里云盘会员、只有夸克会员怎么办」：澄清小雅必填的是阿里云盘**账号**、会员只影响限速（`sources/p2/monlor-144.md:273`、`:279`）；说明「换播放盘」的开关只有 115（`ali2115.txt` / 阿里转存 115，需 115 会员，`sources/p4/ycyc-2878.md:13`、`:19`），没有「转存夸克」；夸克在小雅里只是 `quark_cookie.txt` / `QUARK_COOKIE` 挂载**你自己的夸克**、**不能**把小雅资源转成夸克播放（实测填了仍只有阿里直链，`sources/forum/tid-8385880.md:30`）；给出「只有夸克会员」的三条现实路径（`sources/forum/tid-21673.md:11`、`:13`），并保留「改挂你自己夸克库 + STRM + 302」备选链路（`sources/lens-b/fntvproxy/01_github_com.md:300`）及其 HLS 元数据坑（`:241`）。 |
| 2026-10-06 | **口径修正（夸克）**：更正 5.6——此前把「小雅没有夸克来源」写得过绝。小雅**确有夸克分享区**（`/🌀我的夸克分享`，走夸克直链、吃夸克会员速度，`sources/gh/alist-tvbox-721.md:33`）；「换播放盘开关只有 115」限定为**本体库**。5.6 重写为「本体库走不了夸克、但夸克分享区能走夸克」，并补「覆盖以实机为准」警示（索引默认未必加载、大量路径失效，`sources/gh/alist-tvbox-721.md:16`、`:39`）。 |
---

# 第 6 章 避坑清单——装错地方、风控、外网、UA 与登录

## 本章要解决的问题

前几章把路走通了，但「走得通」不等于「走得稳」。社区帖里反复出现的坑其实有规律，本章把它们归成五类，每条都按**症状 → 原因 → 怎么避**来写：装错地方、整库刮削触发风控、外网播放失败、播放器请求头（User-Agent）不对就 403，以及 WebDAV 的端口 / 用户名写错。一句话结论：**能内网别急着外网、能挂 STRM 子目录就别整库刮削、装组件先想清楚装在哪、请求头不是随便设的、WebDAV 的路径与用户名要对上。**

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
2. **开自动清理**，但「清理」要**分两处**、别搞混：
   - **网盘侧的转存缓存**（风控的根因）：主力是**小雅助手（xiaoyahelper）**——README 称它「一劳永逸的小雅转存清理工具」（`sources/01_raw_githubusercontent_com.md:292`），第 7 章详述；同类还有「安装 115清理助手 -> `4 1`」（`sources/01_raw_githubusercontent_com.md:80`）。
   - **本地磁盘上的元数据 mp4**（撑爆的是你自己的硬盘）：整合脚本菜单里有「开启/关闭 解压成功后自动清理 mp4 元数据文件 -> `2 9 1 1`」与「一键清理当前所有 mp4 元数据文件 -> `2 9 1 2`」（`sources/01_raw_githubusercontent_com.md:116-117`）。

   原帖的建议也是这个方向：「挂个自动清理，不然看的时候也得手动清」（`sources/forum/tid-6046.md:71`）。

   > [!note] 旧写法 `AUTO_CLEAR_ENABLED` 去哪了
   > 早期版本这里让读者设环境变量 `AUTO_CLEAR_ENABLED`（=「是否启用阿里云盘自动清理功能」，`sources/01_club_fnnas_com.md:51`）。它**依然有效**，但只在 **env / compose 装法**里设置；本笔记主线走一键脚本，没有那一层 env 文件，因此改用上面的菜单项与小雅助手（见文末更新记录）。

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

## 6.5 坑五：WebDAV 进不去——端口与用户名写错

**症状**：想用 WebDAV 把小雅挂成文件夹，客户端一直连不上、或报 401。

**原因**：三处最容易写错，且都不是「坏了」：

1. **地址漏了 `/dav`**。WebDAV 的路径是 `http://<你的IP>:5678/dav`，不是 `http://<你的IP>:5678`（`sources/xiaoyaDev/all_in_one.sh:1401`、`:1403`）。
2. **用户名填错分支**。装的时候选没选「强制登入」，用户名是两套：开了（脚本默认、推荐）→ `dav`，脚本注明「无法修改」（`sources/xiaoyaDev/all_in_one.sh:1304`）；没开 → 官方默认 `guest` / `guest_Api789`（`sources/01_hub_docker_com.md:18`）。
3. **端口记成容器内的号**。「`5678`」是**宿主机**映射出去的口，容器内其实是 `80`（`sources/xiaoyaDev/all_in_one.sh:1377`）；`2345`/`2346`/`2347` 三个是辅助口，其中 `2347`「与 6908 逻辑一致」，用于 Emby 走服务端流量（`sources/xiaoyaDev/all_in_one.sh:3830`）。

**怎么避**：照第 3 章 **3.3.2 的双分支表**填（那里有完整对照）。一句话——**路径带 `/dav`；用户名看「强制登入」开关：开了是 `dav`，没开是 `guest`**。

> [!tip] 大白话
> 把 WebDAV 地址想成**「大楼 + 具体房间」**：`http://IP:5678` 只说明楼在哪，`/dav` 才是「WebDAV 这个房间」的门牌；漏了它，等于站在楼门口说「我来办业务」却不说去哪个柜台。用户名那套则是**两种门禁卡**——开了强制登入发的是你自制的卡（`dav` + 自设密码），没开才是那张通用卡（`guest` / `guest_Api789`），拿错卡自然刷不开。

## 6.6 一句心态提醒：把它当「社区项目」

这不是一条坑，而是一句提醒。有社区用户对这类项目的评价是：

> 「总的来说小雅alsit并不是一个稳定的项目，依赖于阿里云盘，说不定哪天就给你封接口了；」（`sources/forum/tid-6046.md:156`）

把它当成**社区风险提示**，而不是结论。正因如此，第 1 章讲过的取舍才重要：**本地存储 vs 网盘播放**各有利弊，值不值得押注，先想清楚——相关讨论见 [[流媒体与影音/网盘影视播放与本地存储的取舍]]。

顺带一提：「依赖阿里云盘」这件事本身，**第 5 章 5.6 专门回答了**——如果你的阿里云盘没有会员、只有夸克会员，能走哪几条路（**用小雅的夸克分享区** / 忍限速 / 补 115 / 改挂自己的夸克库），见 [[流媒体与影音/小雅 fnOS 单容器部署/05 前端接入#5.6 没有阿里云盘会员、只有夸克会员怎么办|第 5 章 5.6]]。

## 本章小结

- **坑一 装错地方**：应用中心自带的小雅取不到数据（`sources/forum/tid-9690.md:32`）；优先按官方文档/仓库安装。**该帖是社区单帖，不推导「官方下架/停更」**；与「商店都好/都不好」之类的说法对象不同，并列保留。
- **坑二 风控**：整库刮削会巨量转存并触发风控（`sources/forum/tid-40446.md:33`、「半分钟几个 T」按原帖称）；避法是只挂 STRM 子目录 + 开自动清理。
- **坑三 外网**：内网地址出门失效（`sources/forum/tid-73955.md:42`）；基础地址要填可公网访问的地址。
- **坑四 UA**：UA 不对同一链接 403（`sources/forum/tid-73955.md:39`、`:40`，原帖限定「至少绑定 UA」）；交给正规中间件处理。
- **坑五 端口与登录**：WebDAV 路径要带 `/dav`；用户名看「强制登入」——开了是 `dav`（`sources/xiaoyaDev/all_in_one.sh:1304`），没开是 `guest` / `guest_Api789`（`sources/01_hub_docker_com.md:18`）；宿主 `5678` 对容器 `80`，`2347` 是 Emby 走服务端流量的备用口（`:3830`）。
- **心态**：项目依赖阿里云盘，有接口变动风险（`sources/forum/tid-6046.md:156`），自己评估取舍。

**下一章预告**：五类坑躲开后，第 7 章进入**运维与收尾**——日常怎么更新（镜像与元数据）、token 过期怎么续、转存缓存怎么定期清、以及这套东西接进 Obsidian 笔记与目录时怎么收尾。

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
| 13 | `- [Xiaoyahelper](https://github.com/xiaoyaDev/xiaoyahelper): 一劳永逸的小雅转存清理工具` | README 把小雅助手列为转存清理工具 | `sources/01_raw_githubusercontent_com.md:292` |
| 14 | `安装 115清理助手 -> 4 1` | 脚本菜单另有「115清理助手」 | `sources/01_raw_githubusercontent_com.md:80` |
| 15 | `开启/关闭 解压成功后自动清理 mp4 元数据文件 -> 2 9 1 1` | 菜单里可开启「解压后自动清理本地 mp4 元数据」 | `sources/01_raw_githubusercontent_com.md:116` |
| 16 | `一键清理当前所有 mp4 元数据文件 -> 2 9 1 2` | 菜单里可一键清理当前所有 mp4 元数据文件 | `sources/01_raw_githubusercontent_com.md:117` |
| 17 | `AUTO_CLEAR_ENABLED: "true" # 是否启用阿里云盘自动清理功能，"true" 启用，"false" 禁用` | 旧写法那个 `AUTO_CLEAR_ENABLED` 的含义（阿里云盘自动清理开关） | `sources/01_club_fnnas_com.md:51` |
| 18 | `webdav: http://ip:5678/dav，默认用户密码: dav/guest_Api789` | WebDAV 路径是 `:5678/dav`，开了强制登入用户名为 `dav` | `sources/xiaoyaDev/all_in_one.sh:1403` |
| 19 | `强制登入用户名：dav（无法修改）` | 开强制登入后，WebDAV 用户名固定为 `dav` | `sources/xiaoyaDev/all_in_one.sh:1304` |
| 20 | `-p 5678:80` | 宿主 `5678` 对到容器内 `80`（容器内不是 5678） | `sources/xiaoyaDev/all_in_one.sh:1377` |
| 21 | `如果您需要访问 Emby 并且走服务端流量，可以访问 2347 端口，此端口与 6908 逻辑一致！！！` | `2347` 是 Emby 走服务端流量的端口（与 6908 逻辑一致） | `sources/xiaoyaDev/all_in_one.sh:3830` |
| 22 | `webdav 账号密码 用户: guest 密码: guest_Api789` | 未开强制登入时的官方默认 WebDAV 账号 | `sources/01_hub_docker_com.md:18` |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线换为 xiaoyaDev/xiaoya-alist（DDSRem）整合脚本；6.2 清理口径换源、新增坑五（第 6 篇）**。6.2 避法 ② 的「第 4 章的 `AUTO_CLEAR_ENABLED`」改为**分两处**讲：网盘侧转存清理（小雅助手 `README:292`、115清理助手 `README:80`）与本地 mp4 元数据清理（菜单 `2 9 1 1` / `2 9 1 2`，`README:116-117`），并加 `[!note]` 说明旧写法 `AUTO_CLEAR_ENABLED` 的适用面（仅在 env / compose 装法）。**新增 6.5 坑五**「WebDAV 进不去——端口与用户名写错」（症状 → 原因三条 → 避法，指向第 3 章 3.3.2 双分支表），原 6.5「心态提醒」顺延为 6.6。章名由「装错地方、风控、外网与 UA」扩为「…、UA 与登录」；导语由「四类」改为「五类」；本章小结新增坑五一条、下一章预告由「四类」改「五类」。引文对照由 12 条扩为 22 条（新增 `01_raw_githubusercontent_com.md` 4 条、`all_in_one.sh` 3 条、`01_club_fnnas_com.md` 1 条、`01_hub_docker_com.md` 1 条）。 |
---

# 第 7 章 运维与收尾

部署能播，只算做完了一半——小雅真正难的地方不是「装起来」，而是「养起来」。转存缓存会越堆越多、镜像会出新版、网盘 token 会失效，这三件事不管，前面几章搭好的链路迟早在某天早上悄悄断掉。这一章是整篇笔记的最后一章，先把「长期维护要做的三件事」讲清楚，再给你一张收尾自检清单和一份诚实的「还没搞明白」清单。

## 7.1 为什么装完还得「养」

第 5、6 章反复提到小雅的运行机制：**你看什么，它就把什么转存到你自己的网盘**（转存一份临时副本，再用 302 直链喂给播放器，见 [[流媒体与影音/Strm流文件与302播放详解]]）。这个转存是临时的，而且——

> [!warning] 小雅默认不帮你删
> 转存进你网盘的文件，小雅**不会自动清理**。看得越多，你网盘里攒的临时文件越多：轻则占容量，重则触发网盘风控（第 6 章讲过的那种「扫描卡住 / 库变空」）。

> [!tip] 大白话
> 把转存想成**在图书馆借书**：看完就该还回去，但图书馆（网盘）默认不会自动帮你办归还。你得自己定个规矩定期还书——不然借书证（网盘容量）哪天就被借满、被冻结了。
> 所以：装完小雅，第一件长期要做的事就是「定期清理转存缓存」。

## 7.2 第一件事：转存缓存定期清理

清理转存不需要你自己写脚本，官方周边工具里就有现成的。本笔记用的是 **xiaoyahelper**（作者与本笔记用的整合脚本同属 `xiaoyaDev` 组织）：仓库自述它的定位是「一劳永逸的小雅转存清理工具」，并说明「本仓库镜像备份了xiaoyakeeper，意旨提供稳定高效的服务！」；实际干活的容器镜像是 `ddsderek/xiaoyakeeper`。

它有两个用法，**本路线推荐走菜单**：

| 怎么跑 | 命令 / 菜单 | 出处 |
| --- | --- | --- |
| 菜单路线（推荐） | 跑主脚本进菜单，选「安装/更新 小雅助手（xiaoyahelper）-> `3 1`」 | `sources/01_raw_githubusercontent_com.md:79` |
| 手动路线 | `bash -c "$(curl -sLk https://xiaoyahelper.ddsrem.com/aliyun_clear.sh \| tail -n +2)" -s <模式号> -tg` | `sources/01_github_com.md:38,51,58` |

手动路线的模式号差别如下（逐条照仓库原文按行号核对，原文留档见文末对照表）：

| 模式 | 干什么 | 怎么选 |
|---|---|---|
| 模式 0 | 每天自动清理一次；系统重启后需要你手动重新跑，或把命令加进系统启动 | 想要「跑一次、以后自管」可用 |
| 模式 1 | 一次性清理，一般用来测试效果 | 只用来试跑一次 |
| 模式 2 | **已废弃，不再支持** | 别用 |
| 模式 3 | 创建一个叫 `xiaoyakeeper` 的 Docker 定时容器，定时清理转存并升级小雅镜像 | 推荐 |
| 模式 4 | 与模式 3 相同 | 同模式 3 |
| 模式 5 | 与模式 3 的区别是**实时清理**：产生播放缓存后一分钟内立即清掉；签到和定时升级同模式 3 | 想更省空间可选 |

```bash
# 手动路线的模式 3（推荐值）：
# 建一个名为 xiaoyakeeper 的 Docker 定时容器，定时清理 + 定时升级小雅镜像
# 出处：sources/01_github_com.md:48,51
bash -c "$(curl -sLk https://xiaoyahelper.ddsrem.com/aliyun_clear.sh | tail -n +2)" -s 3 -tg
```

> [!warning] 模式 2 别再照抄
> 网上不少旧教程还在写模式 2。工具仓库已经明确它是「已废弃，不再支持」——照抄会白折腾。选模式 3（定时）或模式 5（实时）即可。

几点实用补充（同样来自工具仓库）：

- **什么时候跑**：模式 0/3/4/5 的定时任务默认从「你运行脚本的下一分钟」开始，每天跑一次；也可以手动建一个 `/etc/xiaoya/myruntime.txt` 把时间改成比如 `06:00,18:00`（早晚各一次）。
- **它顺带做的事**：完成清理和签到后，脚本会执行 `/etc/xiaoya/mycmd.txt` 里的命令，默认内容就是**升级小雅镜像**；把该文件删掉则变成「定时重启小雅」。
- **签到**：脚本自带网盘签到，可以手动建 `/etc/xiaoya/mycheckintoken.txt`，每行放一个 32 位 `refresh token`；不建该文件就是默认给小雅转存所用的网盘签到。
- **想改就别改脚本本体**：仓库也说了「也可以把脚本下载下来自己魔改」，但它自己维护的定时/升级逻辑更稳，不建议动。

> [!tip] 大白话
> xiaoyahelper 就像给 NAS 定了一个**自动打扫的闹钟**：模式 3 是「每天固定时间扫一次」，模式 5 是「脏了立刻扫」。你不用记着去还书，闹钟会替你办。

## 7.3 第二件事：怎么更新

小雅是持续更新的项目，镜像会不断出新版。**本路线的更新走菜单，不靠重跑安装命令**——这是最容易和旧教程对不上的地方，表格一次列清：

| 你要做的事 | 菜单 | 出处 |
| --- | --- | --- |
| **更新** 小雅Alist | `1 2` | `sources/01_raw_githubusercontent_com.md:120` |
| **卸载** 小雅Alist | `1 3` | `sources/01_raw_githubusercontent_com.md:132` |
| 安装 / 更新 小雅助手（xiaoyahelper，转存清理） | `3 1` | `sources/01_raw_githubusercontent_com.md:79` |
| 卸载 小雅助手（xiaoyahelper） | `3 3` | `sources/01_raw_githubusercontent_com.md:136` |

命令与第 4 章部署时是**同一条**，只是进菜单后选的数字不同：

```bash
# 进菜单后选：更新 小雅Alist -> 1 2
# 出处：sources/01_raw_githubusercontent_com.md:39,120
bash -c "$(curl --insecure -fsSL https://ddsrem.com/xiaoya_install.sh)"
```

> [!warning] 跑 `1 1` 是「安装」，跑 `1 2` 才是「更新」
> 本笔记早期版本的更新办法是「重跑安装脚本」——**本路线不是**。同一条命令，`1 1` 走的是安装流程（会重新问你凭据、建目录），`1 2` 才是更新。照旧教程去重跑安装命令，会白跑一遍问答，还可能覆盖你调好的设置。**要更新，认准 `1 2`。**

> [!warning] 卸载前先备份 `/etc/xiaoya`
> 菜单里有 `1 3 卸载 小雅Alist`，但 README 只列了入口、**没说明它是否保留配置目录**。所以在确认这一点之前，先把 `/etc/xiaoya` 整棵目录（第 3.1 节那棵树，里面是你的 `mytoken.txt` 等凭据）备份一份——凭据重填一次很麻烦。

> [!tip] 大白话
> 更新就像**给手机升系统**：不用重装 App、不用重新登录，点一下「更新」就好。凭据（`mytoken.txt` 那些）还在原来的抽屉里，一个字都不用重填。

## 7.4 第三件事：这套东西要多少硬件

很多新人卡在「我的 NAS 够不够」。先说结论：**本路线只装一个容器**——小雅本体就是 `xiaoyaliu/alist`（第 4 章菜单 `1 1`），镜像本体在 Docker Hub 上标的是 **22 MB**（`sources/01_hub_docker_com.md:30`）。也就是说，光跑「资源层」（AList + 在线播放 + WebDAV），负担非常轻；真正吃 CPU 和硬盘的是 Emby / Jellyfin 这类要下载元数据、建库、做转码的「媒体服务器」，而本笔记**不装它们**。

下面这三条是**可回源**的硬性相关事实：

| 项 | 事实 | 出处 |
| --- | --- | --- |
| 镜像体积 | 官方镜像 `xiaoyaliu/alist` 在 Docker Hub 上标 22 MB | `sources/01_hub_docker_com.md:30` |
| 盘位预期 | 脚本会优先挑一块**容量大于 200 G** 的盘来放配置与媒体目录；挑不到才回落到 `/etc/xiaoya`、`/opt/media` | `sources/xiaoyaDev/all_in_one.sh:145-163` |
| CPU 架构 | 兼容表里「小雅Alist」一行在 x86-64 / arm64 / armhf **三列全 ✅** | `sources/01_raw_githubusercontent_com.md:218-234` |

> [!warning] 本笔记不给「最小配置」的数字
> 你可能会在别处看到「单容器 1 核 / 512M / 512M」这类推荐值。**本笔记不采用**——那个数字出自一条已经停更的旧路线文档，随项目一起撤下了（见文末更新记录）。本路线能拿出来的，就是上面三条能回源的事实：镜像小、盘位够、架构合。至于「你这台机器到底跑不跑得动」，还取决于并发、是否挂前端、网盘速度，**请自己按上面三条 + 实测量判**，而不是照抄一个来路不明的数字。

> [!tip] 大白话
> 这就像装修问「要多大房子」：本笔记只告诉你**住几个人、要不要影音室**（单容器、不装 Emby/Jellyfin），具体多少平米得看你自己怎么摆家具。网上那个「一室一厅 40 平」的旧表格，房东已经跑路了，别再照它量尺。

## 7.5 收尾自检：回到最开始的两个问题

现在整篇笔记读完了，回头检验一下——最初那两问，你能自己答上来了吗？

| 你的原始问题 | 现在应该能给出的答案 | 在哪一章 |
|---|---|---|
| ① 不用 Emby，能用飞牛影视当前端吗？ | 能。用 SmartStrm 生成 STRM，再用 MediaWarp（FNTV 类型）或 fntv-proxy 修好 302 与外网可达，飞牛影视只扫 STRM 子目录即可 | 第 5 章 |
| ①-a 刮削差异 | 飞牛影视直接扫整个小雅会触发转存/风控，只能挂已生成的 STRM 子目录；Emby 全家桶则自带专门的元数据服务 | 第 5、6 章 |
| ①-b 播放差异 | STRM 只存 URL 指针，302 直链让流量不过媒体服务器；但飞牛原生直链默认是内网地址，外网要额外处理 | 第 5、6 章 |
| ①-c 外网差异 | 手机在蜂窝网络下无法解析 NAS 内网域名；需要公网入口或代理端口 | 第 6 章 |
| ② 单容器部署步骤 | 用社区整合脚本 `xiaoyaDev/xiaoya-alist` 的菜单 `1 1`（内部即官方镜像 `xiaoyaliu/alist`）；装完跑一次转存清理、验一次播放链路 | 第 3、4 章 |

如果上面每一行你都能不看笔记自己复述，这套「小雅 + 飞牛影视」你就真正跑通了。

## 7.6 老实说：这些还没搞明白

一篇负责任的笔记，也要把**证据不足、悬而未决**的地方标出来，避免把「传闻」当「结论」。以下几项在整篇笔记里一律**没有**写成结论：

| 未决项 | 目前证据到什么程度 | 本笔记怎么处理 |
|---|---|---|
| 单容器「最小硬件配置」 | 没有来自**在维护来源**的推荐值；旧路线的推荐表随项目停更一并撤下 | 只给可回源的盘位 / 镜像体积 / 架构三条事实，不给 CPU / 内存数字（见 7.4） |
| `1 3 卸载` 会不会删掉 `/etc/xiaoya` 配置 | README 只列了菜单入口，未说明保留策略 | 正文只写「备份后再卸」，不当结论 |
| `xiaoya.host` 是不是官方域名 | 未证，只有社区链路描述 | 只当作「内网地址」的举例，不宣称官方 |
| 飞牛影视从哪个版本开始支持 STRM | 来源冲突，未定 | 不写「起始版本号」这种硬结论 |
| MediaWarp 与 fntv-proxy 能否共存 / 版本矩阵 | 无来源 | 只作并列介绍，不写「可以共存」 |
| 知乎《用飞牛影视连接小雅，可行吗？》、官方 Notion 配置指南 | 均未获取（crawler 被拦 / SPA 壳页） | 未作为证据、未引用 |
| 「半分钟几个 T」的转存量级 | 原帖确有该说法，但属模糊定性、无精确值 | 只作「原帖称」引用，不当精确数据 |

> [!warning] 别把上表读成「结论」
> 这七行是**不确定清单**，不是答案。遇到二手教程把其中任何一条讲成板上钉钉时，请回到「有没有可核查的来源」这一步再判断。

## 本章小结

- **装完要养**：小雅默认不清理转存缓存，必须自己安排定期清理，否则占容量、还可能触发风控。
- **清理工具**：xiaoyahelper（容器镜像 `ddsderek/xiaoyakeeper`）；本路线**走菜单 `3 1`** 安装，手动路线跑 `-s 3`（定时）/ `-s 5`（实时）；**模式 2 已废弃**；它还能顺带定时升级镜像和网盘签到。
- **更新口径**：进同一条主脚本，选 **`1 2` 更新**、**`1 3` 卸载**——`1 1` 是安装，不是更新。
- **硬件**：本路线只装一个容器（官方镜像 `xiaoyaliu/alist`，22 MB），盘位看脚本那条「>200 G 优先」，架构看兼容表「小雅Alist 三列全 ✅」；**本笔记不给最小配置数字**，旧路线那张推荐表已撤下。
- **诚实的收尾**：两问已有完整答案（见 7.5），同时有七项仍属未决，笔记里一律不做结论。

> 最后一句：技术方案会变（版本、域名、镜像都会更新），但这套「资源层（AList）+ 前端层（飞牛影视/Emby）+ 中间件（STRM/302）」的分层心智不会过时。以后哪一环出问题，你都能按这个骨架定位到是哪一层，再回对应章节找答案。想了解「网盘影视播放 vs 本地存储」的取舍，可继续读 [[流媒体与影音/网盘影视播放与本地存储的取舍]]。

## 引文对照（原文 / 中译 / 出处）

下表留档本章引用过的原文逐字片段。出处列中的 `—` 表示该片段无可回指的来源文件；行号指对应 `sources/` 快照文件中的行。

| # | 原文（逐字） | 中译 / 说人话 | 出处 |
|---|---|---|---|
| 1 | 一劳永逸的小雅转存清理工具 | 工具自述定位：装一次、长期自动清理 | sources/01_github_com.md:32 |
| 2 | 本仓库镜像备份了xiaoyakeeper，意旨提供稳定高效的服务！ | 这是该工具的一个镜像备份仓库 | sources/01_github_com.md:33 |
| 3 | 已废弃，不再支持 | 模式 2 已作废，别再照抄 | sources/01_github_com.md:47 |
| 4 | 创建一个名为 xiaoyakeeper 的docker定时运行小雅转存清理并升级小雅镜像 | 模式 3：建一个定时容器，清理并升级 | sources/01_github_com.md:48 |
| 5 | 与模式3的区别是实时清理，只要产生了播放缓存一分钟内立即清理 | 模式 5 相比模式 3，改成了实时清理 | sources/01_github_com.md:55 |
| 6 | 也可以把脚本下载下来自己魔改 | 仓库允许自行改脚本，但不建议 | sources/01_github_com.md:61 |
| 7 | 请勿将 xiaoyahelper 用于商业用途 | 该工具明确不得商用 | sources/01_github_com.md:82 |
| 8 | 安装/更新 小雅助手（xiaoyahelper）-> 3 1 | 菜单里就有装/更新转存清理助手的入口 | sources/01_raw_githubusercontent_com.md:79 |
| 9 | 更新 小雅Alist -> 1 2 | 更新小雅走菜单 `1 2`，不是重跑安装命令 | sources/01_raw_githubusercontent_com.md:120 |
| 10 | 卸载 小雅Alist -> 1 3 | 卸载小雅走菜单 `1 3` | sources/01_raw_githubusercontent_com.md:132 |
| 11 | 卸载 小雅助手（xiaoyahelper）-> 3 3 | 卸载转存清理助手走菜单 `3 3` | sources/01_raw_githubusercontent_com.md:136 |
| 12 | [Xiaoyahelper](https://github.com/xiaoyaDev/xiaoyahelper): 一劳永逸的小雅转存清理工具 | 整合脚本的 README 把该工具列为「小雅周边工具」 | sources/01_raw_githubusercontent_com.md:292 |
| 13 | 22 MB | 官方镜像 `xiaoyaliu/alist` 在 Docker Hub 上标的体积 | sources/01_hub_docker_com.md:30 |
| 14 | `if auto_path="$(df -h \| awk '$2 ~ /G/ && $2+0 > 200 {print $6}' \| grep -E -v ... \| head -n 1)"` | 脚本自动挑一块「容量 >200 G」的盘放配置/媒体目录 | sources/xiaoyaDev/all_in_one.sh:145 |
| 15 | `\| 小雅Alist \| ✅ \| ✅ \| ✅ \|` | 兼容表：小雅Alist 在 x86-64 / arm64 / armhf 三列均 ✅（原表为对齐补了空格，此处已归一） | sources/01_raw_githubusercontent_com.md:218-234 |

## 更新记录

| 日期 | 变更摘要 |
|------|----------|
| 2026-10-07 | **主线由 monlor 镜像整体换为 xiaoyaDev/xiaoya-alist（DDSRem）一键菜单脚本（第 3 篇）**。7.2 补「菜单 `3 1` 装 xiaoyahelper」这条路线并把工具归属改为 `xiaoyaDev` 组织（回源 `01_raw_githubusercontent_com.md:79,292`），手动命令补 `-tg`，两处引文出处校正到 `01_github_com.md:38/48/51/55/58`。7.3 整节重写：更新口径由「重跑 monlor 一键安装脚本」改为**菜单 `1 2`**，新增**卸载 `1 3`** 与「跑 `1 1` 是安装、`1 2` 才是更新」warning、卸载前备份 `/etc/xiaoya` 的 warning；原 monlor 更新命令与 `ghcr.io/monlor/xiaoya-alist` 镜像名纪律段删除。7.4 整节重写：删去 monlor 项目的「1 核 / 512M / 512M」四行推荐表与「维护者推荐」warning，改为三条可回源事实（镜像 22 MB、脚本挑 >200 G 盘位、兼容表小雅Alist 三列全 ✅）并新增「本笔记不给最小配置数字」的 warning；另增一条大白话。7.5 自检第 ② 行由「monlor 社区镜像」改为「社区整合脚本 `xiaoyaDev/xiaoya-alist` 菜单 `1 1`」。7.6 未决项仍为七行：「`ghcr.io` 有无官方镜像」一行因术语已澄清（官方＝`xiaoyaliu/alist`，第 4 章「整合脚本 ≠ 官方」note 已交代）而移除，原「`/data` 与 `/etc/xiaoya`」一行因第 3 章已给出文件级口径而移除，新增「单容器最小硬件配置」与「`1 3 卸载` 是否删配置」两行。本章小结五条同步改写。引文对照由 9 条扩为 15 条，来源改挂 `sources/01_github_com.md`（xiaoyahelper 仓库）与 `sources/01_raw_githubusercontent_com.md`、`sources/01_hub_docker_com.md`、`sources/xiaoyaDev/all_in_one.sh`。 |
| 2026-10-06 | **整套笔记统一为 monlor 单一路线，删除官方镜像路线（第 3 篇）**：7.3「怎么更新」的更新口径表由「你当初的路线 / 更新怎么做」双列改为单列（只留 monlor 一键脚本可重复执行），删去官方路线命令 `docker.xiaoya.pro/update_new.sh` 与「官方镜像重启即自动更新数据库及搜索索引（`docker restart xiaoya`）」整段；7.2 代码块保留；7.3 镜像名对照 warning 与「给手机升系统」比喻改为单一路线口径；7.5 收尾自检第 ② 行由「官方 `docker run` 或 monlor compose 二选一」改为「monlor 社区镜像：一键脚本或 compose」；7.6 未决项表两行重写（`ghcr.io` 无官方镜像、`/data` 与 `/etc/xiaoya` 的目录用途口径）；本章小结更新口径一条改为单一路线。引文对照删去官方镜像页 2 条（原第 9、10 行），重编号为 1–9。 |
