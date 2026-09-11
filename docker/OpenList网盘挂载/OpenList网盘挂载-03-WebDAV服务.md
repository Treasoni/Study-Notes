---
title: OpenList 网盘挂载 · 第 3 册 开出 WebDAV 服务
tags:
  - Docker
  - OpenList
  - WebDAV
  - Rclone
  - 网盘
  - 实战笔记
  - OpenList网盘挂载
created: 2026-09-12
updated: 2026-09-12
status: 已完成
source_project: openlist-webdav-rclone-docker
series: OpenList → WebDAV → Rclone → Docker 全链路实战
volume: 3/6
---

# 第 3 章 开出 WebDAV 服务

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-02-网盘聚合]] ｜ 目录：[[OpenList网盘挂载-00-总目录]] ｜ 下一册：[[OpenList网盘挂载-04-Rclone挂载]]

第 1 章把 OpenList 用 Docker 跑了起来，第 2 章把网盘作为存储挂了进去。但到目前为止，能访问这些内容的还只有浏览器里的 OpenList 网页。要让 OpenList 之外的程序——文件管理器、rclone、下游容器——也能读到同一批文件，就需要把 WebDAV 服务"开出来"。本章只做服务侧：给哪个用户开、开哪些权限、客户端该填什么参数。真正的挂载动作留到第 4 章。

## 3.1 先弄清 WebDAV 在这里是什么

WebDAV 不是一套全新的传输协议，而是 HTTP 的扩展集。官方原文：

> WebDAV (Web Distributed Authoring and Versioning) is a set of extensions to the Hypertext Transfer Protocol (HTTP) that enables users to collaboratively create, edit, and manage files directly on a web server.[^c3-s02]

紧接着的一句才是关键——OpenList 自己就能当这台 WebDAV 服务器：

> OpenList can be served as a WebDAV server, allowing users to access and modify files through a web interface.[^c3-s02]

这意味着你不需要额外装 Nginx、Apache 或任何 WebDAV 服务端。第 1 章那个 5244 端口的进程，除了给浏览器看网页，同时也能说 WebDAV 协议。

> [!tip] 大白话
> 把 WebDAV 想成 HTTP 的一门"方言"：浏览器说的是网页这门话，文件管理器 / rclone 说的是 WebDAV 这门话。OpenList 两种都会说，所以同一个端口，既能开网页，也能接 WebDAV 客户端。

## 3.2 核心认知：这里没有"全局开关"

新手的第一个动作通常是翻后台设置，找"启用 WebDAV"的开关。找不到——因为不存在这样一个开关。

官方对"怎么启用"只给了一条路径：在 `用户 => 权限` 设置里，为特定用户开启相应的权限项。

> 要使特定用户能够使用 WebDAV，需在 `用户 => 权限` 设置中为其开启以下权限：[^c3-s02]

换句话说，WebDAV 能不能用，取决于**登录的那个用户**有没有被授权，而不是服务端有没有一个总闸。

> [!warning] 待核实（Q1）
> 是否存在**全局**的"开启 WebDAV"开关？S02 通篇只讲用户权限项，没有出现任何全局开关字段；第 2 章见过的是**每个存储各自的** `Webdav policy` 字段（那是针对单个存储的传输策略，不是全局开关）。因此倾向"没有全局开关"，但这一点未经官方文档明确证实，标为**未证实**。

> [!tip] 大白话
> 不是"打开总闸"，而是"给某张门禁卡单独开权限"。能不能走 WebDAV，看的是这张卡（这个用户）被批了什么，跟服务端有没有一个总开关无关。

## 3.3 权限两件套，外加一条官方警告

导航到后台的用户列表，编辑目标用户，找到"权限"区块。需要开的权限分成职责完全不同的三类：

| 权限项 | 作用 | 什么时候必须开 |
|---|---|---|
| `WebDAV 读取` | 查看和读取 WebDAV 中的文件和目录 | 想看到内容就必须开；**只读 / 只看 / 只播放，开这一项就够** |
| `WebDAV 管理` | 进行写入操作（创建、修改、删除等） | 需要写入时才开 |
| 具体文件系统权限 | `创建目录或上传` / `重命名` / `移动` / `复制` / `删除` 等[^c3-s03] | 计划做哪一类写操作，就必须**同时**开对应那一项 |

两条官方原文，分别对应前两个权限项：

> 必须开启此权限才能**查看和读取** WebDAV 中的文件和目录。[^c3-s02]

> 如果用户**仅需查看或播放文件**，开启此权限即可。[^c3-s02]

> 必须开启此权限才能进行**写入操作**（创建、修改、删除等）。[^c3-s02]

然后是本章最容易被忽略的一句：

> **仅开启`WebDAV 管理` 还不够！** 需要同时开启 `WebDAV 管理` **以及** 其计划执行操作所需的具体文件系统权限（如 `重命名`、`删除`、`复制`、`创建目录或上传` 等）。[^c3-s02]

"管理"只是一个资格门槛，它不会把底层的重命名 / 删除 / 复制等具体权限自动一起给你。想删文件，还得单独开 `删除`；想上传，还得单独开 `创建目录或上传`。权限是一对一开出来的，不是开一个大类就全有。

上游 AList 文档（⚠️ **这是上游 AList 的口径，2022-09-07 发布、未标注更新日期，只能当旁证，不能当 OpenList 官方结论**）说的是同一件事：

> ≥ v3.42.0 The above versions need to open the two permissions of `Webdav Read` and `Webdav Manage` in User => Permissions[^c3-s04]

> since v3.42.0, writing to WebDAV not only requires the `Webdav Manage` permission but also basic permissions such as `rename`, `delete`, and `copy`.[^c3-s04]

两边对"读 / 写两件套 + 写操作还需具体权限"的说法一致，可互相印证。

> [!tip] 大白话
> `WebDAV 读取` 像"进馆阅览证"，`WebDAV 管理` 像"可以动手改东西的许可"。但光有后者还不够——你得说清楚要动哪一类东西：改名的许可、删除的许可、上传的许可，都是一项一项单独批的。

## 3.4 连接参数表（本章交付物）

权限开好后，客户端只需要下面这几个参数。官方"基础连接配置"给出的字段如下[^c3-s02]：

| 配置项 | 值 | 说明 |
|---|---|---|
| **Url** | `http[s]://<域名>:<端口>/dav/` | 官方写作 `http[s]://your-domain:port/dav/` |
| **Host** | 你的域名 | 官方示例 `openlist.example.com`；自建环境填宿主机 IP 或域名 |
| **Path** | `dav` | 客户端若提供单独"路径"字段，就填 `dav` |
| **Protocol** | `http` 或 `https` | 官方**强烈建议 https** |
| **Port** | 与网页端**完全一致** | 第 1 章映射的是 `5244`，这里就填 `5244` |
| **Username** | 网页端登录用户名 | 即你登录 OpenList 后台用的用户名 |
| **Password** | 网页端登录密码 | 即你登录 OpenList 后台用的密码 |

三条关键约束，官方原文：

> The port **must be identical** to the one used for accessing the OpenList web interface[^c3-s02]

> 你在 OpenList 网页端登录使用的**用户名**[^c3-s02]

> `http` 或 `https` (强烈建议使用 **https** 以保障安全)[^c3-s02]

也就是：端口不要另开一个，也别在客户端里随手改成 80/443——网页端用哪个端口，WebDAV 就用哪个。账号密码就是你登录后台的那一套，不需要单独建 WebDAV 账号。

> [!tip] 大白话
> 把 `/dav/` 想成这栋楼的"后门入口"：正门是浏览器访问的网页，后门专供 WebDAV 客户端进出；但门牌号（端口）和门禁卡（账号密码）跟正门是同一套。

> [!warning] 本章没有可跑验证命令
> S02 与上游 S04 都只给了上面这张参数表，**没有给出任何端点验证示例**（没有 `curl`，也没有 `PROPFIND`）。因此本章**不编造**探测命令。**可脚本化的端点验证放到第 4 章**——那一章会配置 rclone remote，remote 本身就是对这条链路的实测。

## 3.5 已知限制与"存储支持"现状

先记一条会踩到的限制：

> 暂不支持复制时重命名。[^c3-s02]

另外，官方的"存储支持"章节目前没有正文，只有一句：

> WIP, please stay tuned[^c3-s02]

也就是说，哪些存储驱动在 WebDAV 下支持 list / download / mkdir / rename / move / copy / upload，官方页面**尚未列出**。上游 AList 页面倒是有一张驱动能力矩阵，但那同属 2022-09-07 的上游口径，不代表 OpenList 的现状，本章不展开、也不拿它代替 OpenList 的结论。

> [!warning] 待核实（Q2）
> `/dav/` 之后能否再接第 2 章的挂载路径（形如 `/dav/<挂载路径>`）？`/dav/` 来自 S02，`Mount Path` 是第 2 章存储的挂载字段，把两者拼接起来**属于推断**，来源中没有这个路径结构。要确认某个存储究竟出现在哪个路径下，以第 4 章实际挂载后看到的目录为准。

## 3.6 官方推荐客户端

官方按平台列了推荐客户端，其中与本链路直接相关的是[^c3-s02]：

| 平台 | 官方推荐 | 官方说明原文 |
|---|---|---|
| Linux | `rclone` | Recommended, feature-rich / 推荐, 功能强大 |
| Linux | `davfs2` | System-level mounting, requires configuration / 系统级挂载, 需配置 |
| Windows | RaiDrive | Recommended for mounting / 推荐挂载 |

Linux 这条线上，官方把 rclone 排在推荐位，正好接上第 4 章——我们就是用它把 WebDAV 挂成本地目录，并顺便完成本章欠下的端点验证。

## 3.7 章末可跑产出

1. **权限开齐**：为目标用户开启 `WebDAV 读取`；需要写入时，再加 `WebDAV 管理` **以及**计划操作对应的具体权限（如 `创建目录或上传`、`重命名`、`删除`、`复制`、`移动`）。
2. **参数表填好**：按 §3.4 的表，把 Url / Host / Path / Protocol / Port / Username / Password 填进 WebDAV 客户端。
3. **能登入并看到内容**：用一个 WebDAV 客户端登录成功，并看到第 2 章挂载进来的那个存储的内容（正式挂载与命令行验证见第 4 章）。

## 本章小结

- WebDAV 是 HTTP 的扩展集；OpenList 自身即可充当 WebDAV 服务器，无需另装服务端。
- 启用 WebDAV 不是打开某个全局开关，而是在 `用户 => 权限` 里给特定用户开权限项。
- `WebDAV 读取` 管查看 / 读取 / 播放；`WebDAV 管理` 管写入；但**只开"管理"不够**，计划做的写操作对应的具体权限（重命名 / 删除 / 复制 / 创建目录或上传 / 移动）也必须一并开启。
- 连接参数：Url `http[s]://<域名>:<端口>/dav/`、Path `dav`、端口必须与网页端完全一致、凭证即网页端登录账号密码、官方强烈建议 https。
- 已知限制：不支持"复制时重命名"；官方"存储支持"章节仍是 WIP。本章不含可跑验证命令，端点实测留到第 4 章。

## 相关笔记

- [[网络协议详解-WebDAV_Samba_FTP_iSCSI]] —— WebDAV 与 Samba / FTP / iSCSI 的横向对比，本章协议背景的展开
- [[域名完全上手]] —— 本章提到的「反向代理前缀」场景

[^c3-s02]: OpenList Docs — WebDAV（OpenList 官方），https://doc.oplist.org/guide/advanced/webdav
[^c3-s03]: OpenList Docs — User / 用户与权限（OpenList 官方），https://doc.oplist.org/guide/advanced/user
[^c3-s04]: AList Docs — WebDav（**上游 AList 口径**，页面标注 2022-09-07 发布且未标注更新日期），https://alistgo.com/guide/webdav.html

---

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-02-网盘聚合]] ｜ 目录：[[OpenList网盘挂载-00-总目录]] ｜ 下一册：[[OpenList网盘挂载-04-Rclone挂载]]
