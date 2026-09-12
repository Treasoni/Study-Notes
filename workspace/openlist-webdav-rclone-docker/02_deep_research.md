# 02 深度素材 — OpenList → WebDAV → Rclone → Docker

- **运行标识**: openlist-webdav-rclone-docker
- **阶段**: P2 深度收集
- **方向**: 方向 A（全链路主线版，聚焦 Linux 宿主机 + Docker Compose）
- **完成日期**: 2026-09-12
- **抓取工具**: `.claude/skills/research-collector/scripts/crawl.sh`（crawl4ai 0.9.x，JS 渲染开）
- **素材存放**: `workspace/openlist-webdav-rclone-docker/sources/`

## 1. 范围

本阶段回答「OpenList 聚合网盘 → 开启 WebDAV → Rclone 挂载到本地 → 映射给 Docker 容器」这条链路每一步的**官方口径是什么、配置文件长什么样、哪一步最容易崩**。

**不在范围**（方向 A 明确排除）：容器内运行 rclone mount 的架构对比、多网盘聚合策略调优、直链与限速、监控告警。

**环境基线**：命令与配置一律以 **Linux 宿主机 + Docker Compose** 为准；Windows/WSL 侧差异只在必要处标注。

## 2. 来源表

### 2.1 已抓取并可引用（18 篇）

| 源ID | 标题 | Tier | 本地文件 | 一句话定位 |
|---|---|---|---|---|
| S01 | OpenList Docs — 使用 Docker 安装 | T1 | `sources/S01_openlist_docker_install.md` | 第 1 章主干：镜像、端口、数据目录、运行身份、升级 |
| S02 | OpenList Docs — WebDAV | T1 | `sources/S02_openlist_webdav.md` | 第 3 章主干：端点、Path、端口与账号要求、权限项 |
| S03 | OpenList Docs — 用户与权限 | T1 | `sources/S03_openlist_user_permission.md` | 第 2 章主干：用户字段、权限项全清单、安全警告 |
| S04 | AList Docs — WebDav（**上游口径**） | T1\* | `sources/S04_alist_webdav_upstream.md` | 驱动 WebDAV 能力矩阵；**不可当作 OpenList 官方结论** |
| S06 | rclone — mount 命令文档 | T1 | `sources/S06_rclone_mount.md` | 第 4 章主干：mount 语义、VFS 缓存四档、系统集成 |
| S07 | rclone — WebDAV 远端 | T1 | `sources/S07_rclone_webdav_remote.md` | 第 4 章配置：`type=webdav` 字段与能力限制 |
| S09 | Linux 内核文档 — FUSE | T1 | `sources/S09_fuse_kernel_doc.md` | `allow_other` 的权威语义与默认限制 |
| S10 | rclone 论坛 — systemd 持久挂载 | T3 | `sources/S10_rclone_systemd_forum.md` | 完整 unit 写法；**社区经验，非官方** |
| S11 | Docker Docs — Bind mounts | T1 | `sources/S11_docker_bind_mounts.md` | 第 5 章主干：bind mount 语义、`:ro`、传播 |
| S12 | LinuxServer.io — PUID/PGID | T1 | `sources/S12_linuxserver_puid_pgid.md` | 容器内用户的宿主机映射；**镜像维护方口径** |
| S15 | OpenList Docs — 驱动索引页 | T1 | `sources/S15_openlist_drivers_index.md` | ⚠️ **空壳页**（277 字节），无正文，见 §4 缺口 G6 |
| S16 | OpenList Docs — 本地存储驱动 | T1 | `sources/S16_openlist_driver_local.md` | 第 2 章示例驱动：字段与缩略图 |
| S17 | OpenList Docs — 驱动通用字段 | T1 | `sources/S17_openlist_driver_common.md` | 第 2 章主干：挂载路径、序号、WebDAV 策略、代理 |
| S18 | Docker Docs — Volumes | T1 | `sources/S18_docker_volumes.md` | 第 5 章选型依据：何时**不该**用 volume |
| S19 | OpenList Docs — WebDav 驱动 | T1 | `sources/S19_openlist_driver_webdav.md` | **2026-09-12 追加**：第 3 册 §3.6 主干——驱动字段、默认值、302/代理 |
| S20 | OpenList 源码 — WebDAV 驱动 | T1（源码级） | `sources/S20_openlist_source_webdav_driver.md` | **2026-09-12 追加**：`drivers/webdav` + `internal/driver/item.go` + `pkg/gowebdav`，支撑"地址必须带协议头" |
| S21 | 坚果云帮助中心 — 第三方应用授权 WebDAV | T1（**坚果云官方口径，非 OpenList 官方**） | `sources/S21_jianguoyun_webdav_help.md` | **2026-09-12 追加**：应用密码、额度限制 |
| S22 | Synology 知识中心 — WebDAV Server | T1（**群晖官方口径**；⚠️ 页面 JS 渲染，**未取到正文**） | `sources/S22_synology_webdav_kb.md` | **2026-09-12 追加**：默认端口 5005/5006；只登记事实、**不可当引文** |

**Tier 分布**：T1 × 17（含 1 篇标注为上游口径、2 篇为第三方服务官方口径、1 篇源码级）、T3 × 1。

> **2026-09-12 追加说明**：S19–S22 为第 3 册 §3.6「反向对照：OpenList 也能当 WebDAV 客户端」新增，
> 对应本轮单篇笔记更新（走 `note-updater` 路径，未重开 `learning-note-flow`）。
> S20 是**源码级**来源（不是文档），本项目中首次引入这一层级；S22 **未取到正文**，只能当"事实登记"用。

### 2.2 P1 候选但**未抓取**（禁止引用）

`S05`（凡凡小站 OpenList 部署帖）、`S08`（rclone 文档总览）、`S13`（jellyfin-rclone README）、`S14`（群晖 OpenList+rclone+Plex 帖）。

> 这四篇只出现在 `01_explore_result.md` 的候选清单里，**本阶段没有读过它们的正文**。下游不得据其编号引用任何内容。

## 3. 断言 → 来源映射

### 3.1 OpenList 部署（第 1 章）

| 断言 | 来源 | 层级 |
|---|---|---|
| 镜像名 `openlistteam/openlist:latest`，另可用 `v*.*.*`、`beta`、`latest-lite`、`latest-aio`、`latest-aria2`、`latest-ffmpeg` | S01 | 官方配置字段 |
| 端口映射 `5244:5244`；容器内数据目录 `/opt/openlist/data` | S01 | 官方示例 |
| `/etc/openlist` 只是**默认**映射目录，可改 | S01 | `请注意：/etc/openlist 仅为默认映射的目录，您可以根据需要修改为其他目录。` |
| **v4.1.0 边界**：`v4.1.0` 以后的版本（不包含 `v4.1.0`）镜像已移除 `PUID`/`PGID` | S01 | `在 v4.1.0 以后的版本中（不包含 v4.1.0），OpenList 镜像已经移除了 PUID、PGID` |
| 镜像改用 `useradd` 建 `openlist`（UID **1001**）/ 组 `openlist`（GID **1001**），并以该用户跑 `openlist server` | S01 | 官方默认 |
| 官方要求用户**自行处理映射目录权限**，使容器内 `openlist(1001)` 可访问 | S01 | `确保容器内的 openlist(1001) 用户有权限访问映射的目录` |
| 三种运行身份写法：compose `user: '0:0'`；CLI `--user $(id -u):$(id -g)`；或 `chown -R 1001:1001` 后用内置用户 | S01 | 官方示例（逐字见 §5.1） |
| rootless Docker 下 `--user 0:0` 代表当前用户的 UID 和 GID | S01 | `--user 0:0 代表当前用户的 UID 和 GID` |
| 环境变量：`PUID`/`PGID`（v4.1.0 以后废弃）、`UMASK` 默认 `022`、`UTC` 默认 UTC、`RUN_ARIA2` 视镜像是否预装而定、`OPENLIST_ADMIN_PASSWORD` | S01 | 官方环境变量表 |
| 镜像默认以 `--no-prefix` 运行，故无需 `OPENLIST_` 前缀 | S01 | `runs by default with the --no-prefix flag, so you don't need to add the OPENLIST_ prefix` |
| 首次运行从 `docker logs openlist` 看初始管理员密码 | S01 | `你在日志中看到密码。` |
| 重设密码：`./openlist admin random` 或 `./openlist admin set NEW_PASSWORD` | S01 | 官方示例 |
| 更新三法：watchtower `--run-once`、Docker CLI 四步、compose `pull`/`down`/`up -d` | S01 | 官方示例 |
| 官方另附「增强版 compose」，除 openlist 外还定义 aria2-pro、ariang、qbittorrent、transmission 四个容器，**默认整段被注释** | S01 | 官方示例 |

### 3.2 聚合网盘与用户权限（第 2 章）

| 断言 | 来源 | 层级 |
|---|---|---|
| 本地存储驱动字段：`Root folder path`（中文界面「根文件夹ID」），示例 Linux `/root`、Windows `C:` | S16 | 官方配置字段 |
| 本地存储视频缩略图需外部 `ffmpeg` | S16 | `You need to use the ffmpeg tool to add.` |
| 本地存储 PDF 缩略图默认关闭，仅 macOS 可用，需依次开 `Thumbnail`、`PDF thumbnail`，建议配 `Thumb cache folder` | S16 | 官方默认 + 配置字段 |
| 回收站路径为空则永久删除；填写后删除会移入该目录 | S16 | 官方配置字段 + 行为 |
| **`Mount Path`（挂载路径）三义**：挂载项唯一标识 / 对外展示名称 / 要挂载到的位置；填 `/` 表示挂到根 | S17 | `The unique identifier for the mount point, the name displayed externally, and the location where it should be mounted.` |
| `Mount Path` **必填**，留空校验失败 | S17 | `The mount path name is a required field and cannot be left empty` |
| 留空时的**官方报错原文**：`Key: 'Storage.MountPath' Error: Field validation for 'MountPath' failed on the 'required' tag` | S17 | 官方报错原文（页面出现两次，一次 `Error:` 后有空格、一次无） |
| 挂载路径**不可重名**，重名报 `UNIQUE constraint failed: x_storages.mount_path`；官方给的解法是**用别名存储聚合** | S17 | 官方报错原文 |
| `Order` 数字越小越靠前，可填负数 | S17 | 官方配置字段 |
| `Remark` 首行写 `ref:/mount_path` 可复用另一已挂载存储的认证令牌 | S17 | 官方配置字段 |
| `ref:` 机制当前仅支持 139Yun、AliyundriveOpen、189CloudPC、123PanShare、Cloudreve V3/V4 | S17 | 官方限制 |
| `Cache Expiration` 是**目录结构**的缓存时间；`Custom Cache Policies` 按路径设缓存分钟数，支持 `*`（单层）与 `**`（多层） | S17 | 官方配置字段 |
| **`Webdav policy`（WebDAV 策略）三选一**：302 重定向真实链接 / 使用代理 URL / 本机代理 | S17 | 官方配置字段 |
| WebDAV 策略默认值取决于驱动：有 302 选项则默认 302，无则默认本地代理 | S17 | 官方默认 |
| `Web proxy`（Web 代理）与 `Webdav policy` 是**两个不同配置** | S17 | 官方说明 |
| 下载代理 URL 留空时默认用本机传输 | S17 | 官方默认 |
| 用户字段：`Username`、`Password`（对游客无效）、`Base path`（用户登录时看到的根路径） | S03 | 官方配置字段 |
| 连续 6 次密码错误封禁该 IP 30 分钟，重启服务可立刻解封 | S03 | 官方行为 |
| 游客账户默认停用，需手动取消停用 | S03 | `游客账户默认停用，如果要启用游客账户请手动关闭停用。` |
| 权限项清单：`创建目录或上传`、`重命名`、`移动`、`复制`、`删除`、`WebDAV 读取`、`WebDAV 管理`、`可以看到隐藏`、`无密码访问`、`读取压缩文件`、`解压`、FTP 读取 / FTP 管理 | S03 / S02 | 官方配置字段 |
| 官方安全警告：授予远程文件读写权限 = 赋予其利用服务器网络环境（含内网地址）访问资源的能力，仅应授予完全可信用户 | S03 | `授予用户远程文件读写权限，同时也赋予了其利用服务器网络环境(包括内部网络地址)访问资源的能力。` |
| 权限管理不当引发的安全事件由管理员承担 | S03 | `因用户或权限管理不当而导致的安全事件，由管理员用户承担责任。` |

### 3.3 WebDAV 服务（第 3 章）

| 断言 | 来源 | 层级 |
|---|---|---|
| OpenList 自身可作为 WebDAV 服务器 | S02 | `OpenList can be served as a WebDAV server, allowing users to access and modify files through a web interface.` |
| 启用方式是到 `用户 => 权限` 为特定用户开权限项，**不是**找某个全局开关 | S02 | `要使特定用户能够使用 WebDAV，需在 用户 => 权限 设置中为其开启以下权限：` |
| `WebDAV 读取`：必须开启才能**查看和读取**；仅查看/播放只需此项 | S02 | `必须开启此权限才能查看和读取 WebDAV 中的文件和目录。` |
| `WebDAV 管理`：必须开启才能进行**写入操作**（创建、修改、删除等） | S02 | `必须开启此权限才能进行写入操作 （创建、修改、删除等）。` |
| **仅开 `WebDAV 管理` 还不够**，必须同时开启计划操作对应的具体文件系统权限 | S02 | `仅开启 WebDAV 管理 还不够！` |
| 客户端 URL 形如 `http[s]://your-domain:port/dav/`，Path 填 `dav` | S02 | 官方配置字段 |
| 端口必须与访问网页端所用端口**完全一致** | S02 | `与访问 OpenList 网页端使用的端口完全一致` |
| 用户名密码即网页端登录账号密码 | S02 | 官方配置字段 |
| 协议 `http`/`https`，官方**强烈建议 https** | S02 | `强烈建议使用 https 以保障安全` |
| 目前**不支持**「复制时重命名」 | S02 | `暂不支持复制时重命名。` |
| 官方推荐客户端：Linux 用 `rclone`（功能丰富）或 `davfs2`；Windows 用 RaiDrive | S02 | 官方推荐 |
| （上游 AList 口径）≥ v3.42.0 需在 User => Permissions 开 `Webdav Read` 与 `Webdav Manage` | S04 | **AList 口径**，与 S02 互相印证 |
| （上游 AList 口径）驱动能力矩阵：`copy` 列为 ❌ 的有 GoogleDrive、123pan、FTP、SFTP；其余（LocalStorage、AliyunDrive、Onedrive、189Cloud、PikPak、S3、USS、WebDAV、Teambition、Mediatrack、139yun、YandexDisk、BaiduNetdisk、Quark、KodBox）`copy` 为 ✅ | S04 | **AList 口径，2022-09-07 发布，未标注更新** |

**2026-09-12 追加：第 3 册 §3.6「反向对照（OpenList 当 WebDAV 客户端）」新增断言**

| 断言 | 来源 | 层级 |
|---|---|---|
| WebDAV 驱动字段：`Vendor`(`vendor`, select `sharepoint`/`other` 默认 `other`)、`Address`(`address`)、`Username`、`Password`、`Root folder path`(`root_folder_path`)、`Tls insecure skip verify`(`tls_insecure_skip_verify` 默认 `false`) | S19 + S20 | 官方字段 + 源码 `drivers/webdav/meta.go` |
| `Address`/`Username`/`Password` 三项**均为必填**（`required:"true"`） | S20 | 源码 `drivers/webdav/meta.go` |
| 「根文件夹路径」默认值为 `/` | S20 | 源码 `driver.Config{DefaultRoot: "/"}` |
| 界面「根文件夹路径」= 官方文档页所写「根文件夹ID」，同一字段 `root_folder_path` | S19 + S20 | 文档中文名与界面名不一致，**同一配置键** |
| `Root folder path` 语义是**拼接在地址之后**：官方 `The path of fodler you want to mount, same as join in address` / 「要挂载的文件夹路径，与加入地址相同」 | S19 | 官方原文（英文原文含 `fodler` 拼写错误，逐字保留） |
| **地址必须带 `http://` / `https://`**：驱动把 `d.Address` 原样交给 `gowebdav.NewClient`，客户端只做 `FixSlash`（补末尾 `/`），**不补协议头** | S20 | **源码级**（文档页未写此要求） |
| 「跳过 SSL 证书验证」针对**自签名证书**场景，启用会降低安全性 | S19 | 官方原文 |
| 挂 OneDrive/SharePoint 才需要把 `vendor` 选为 `sharepoint`（国际版/世纪互联） | S19 | 官方原文 |
| 坚果云 WebDAV 需用**应用密码**（账户信息 → 安全选项 → 第三方应用管理 → 添加应用密码），非登录密码；应用密码只显示一次 | S21 | **坚果云官方口径** |
| 坚果云 WebDAV 额度：免费版 ≤600 次请求/30 分钟、付费版 ≤1500 次请求/30 分钟；单次请求文件+文件夹数上限 750 | S21 | **坚果云官方口径** |
| 群晖 WebDAV Server 默认端口 HTTP `5005` / HTTPS `5006` | S22 | **群晖官方口径，但未逐字取证**（页面 JS 渲染）→ 按"事实"呈现，不给引文 |
| 「地址与根文件夹路径重复拼接会拼出 `.../dav/work/work`」 | —（**推断**） | **未证实**：由官方"拼接"语义推出，官方无此示例 |

### 3.4 Rclone 概念与挂载（第 4 章）

| 断言 | 来源 | 层级 |
|---|---|---|
| `rclone mount` 把任意云存储挂载成本地文件系统，底层用 FUSE | S06 | `mount any of Rclone's cloud storage systems as a file system with FUSE.` |
| 挂载点必须是**已存在且为空**的目录 | S06 | `is an empty existing directory` |
| 默认前台运行；`--daemon` 强制后台；Windows 只支持前台 | S06 | 官方默认 |
| 后台模式需手动卸载：`fusermount -u` / 某些系统 `fusermount3 -u` / nfsmount 用 `umount` | S06 | 官方行为 |
| **mount 与 sync/copy 的可靠性差异**：sync/copy 靠大量重试应对云存储不可靠；mount 不能同样重试，除非对上传做本地拷贝，可靠性要靠 VFS File Caching 解决 | S06 | `rclone mount can't use retries in the same way without making local copies of the uploads` |
| `--vfs-cache-mode` 四档，默认 **off** | S06 | 官方默认 |
| `off`：读写都直连远端不落盘；不支持读+写同时打开、写不能 seek、必须带 O_TRUNC、上传失败**不能重试** | S06 | 官方行为 |
| `minimal`：与 off 类似，但读+写的文件会缓冲到磁盘；磁盘占用最小 | S06 | 官方行为 |
| `writes`：只读文件仍直连远端，只写与读写文件先缓冲到磁盘；支持全部常规文件系统操作；上传失败按**指数递增间隔重试最长 1 分钟** | S06 | 官方行为 |
| `full`：所有读写都经磁盘缓冲，读取也落盘；缓存文件是**稀疏文件**（只存已下载部分但显示完整大小）；读时会预读 `--buffer-size` + `--vfs-read-ahead` | S06 | 官方行为 |
| ⚠️ 不是所有文件系统支持稀疏文件，**FAT/exFAT 尤其不支持**，放上去性能非常差并记 ERROR | S06 | `IMPORTANT not all file systems support sparse files. In particular FAT/exFAT do not.` |
| 默认值：`--vfs-cache-max-age 1h0m0s`、`--vfs-write-back 5s`、`--vfs-cache-poll-interval 1m0s`、`--dir-cache-time 5m0s`、`--poll-interval 1m0s`、`--attr-timeout 1s`、`--daemon-wait 1m0s` | S06 | 官方默认 |
| `--vfs-cache-max-age` 依**最后访问时间**而非入缓存时间，访问会重置计时 | S06 | 官方行为 |
| `--vfs-cache-max-size` 可能被超出：只每 `--vfs-cache-poll-interval` 检查一次，且**已打开文件不能被淘汰** | S06 | `open files cannot be evicted from the cache` |
| ⚠️ 用 `--vfs-cache-mode > off` 时不应让两个 rclone 实例共用相同/重叠 remote 的同一 VFS 缓存，否则可能数据损坏；可用 `--cache-dir` 隔离 | S06 | `This can potentially cause data corruption if you do.` |
| ⚠️ `--attr-timeout` 窗口内远端文件长度变化可能出现损坏，表现为文件被截断或末尾乱码；默认 1s 下极不可能但非不可能 | S06 | `It will show up as either a truncated file or a file with garbage on the end.` |
| `--uid`/`--gid` 覆盖文件系统设置的 uid/gid 字段，**默认均为 1000**；`--umask` 默认 **002**；`--file-perms` 默认 666、`--dir-perms` 默认 777 | S06 | 官方默认 |
| `--allow-other`、`--allow-root`、`--allow-non-empty`、`--uid`/`--gid`/`--umask` 均**不支持 Windows** | S06 | 官方限制 |
| systemd 下可用 `Type=notify`，挂载点建好后服务才进入 started | S06 | `the service will enter the started state after the mountpoint has been successfully set up` |
| ⚠️ systemd 运行 mount unit 时**没有环境变量**（含 PATH、HOME），`~` 不展开，须显式传绝对路径的 `--config`、`--cache-dir`；rclone 会回退用 `/bin:/usr/bin`，须确保其中有 fusermount/fusermount3 | S06 | `rclone will use the fallback PATH of /bin:/usr/bin in this scenario` |
| 新版 Ubuntu 可能因 Apparmor 限制报 fusermount3 权限错误，可用 `sudo aa-disable /usr/bin/fusermount3` 关闭 | S06 | 官方提示 |
| `--poll-interval` 必须小于 `--dir-cache-time`，设为 0 可禁用，且仅支持的 remote 有效 | S06 | 官方默认 |
| 可发 `SIGHUP` 刷新全部目录缓存（`kill -SIGHUP $(pidof rclone)`），或用 `rclone rc vfs/forget` | S06 | 官方行为 |
| （rclone WebDAV 远端）`type = webdav`，`url` **必填**；`pass` 输入必须经过 obscure 处理 | S07 | `Required: true` / `Input to this must be obscured` |
| `vendor` 取值：`fastmail`、`nextcloud`、`owncloud`、`infinitescale`、`sharepoint`、`sharepoint-ntlm`、`rclone`、`other` | S07 | 官方配置字段 |
| ⚠️ **普通 WebDAV 不支持修改时间，也不支持哈希**；仅当配合 Fastmail Files、ownCloud 或 Nextcloud 时才支持 | S07 | `Plain WebDAV does not support modified times.` / `Likewise plain WebDAV does not support hashes` |
| `--webdav-auth-redirect` 默认 false：服务器重定向到新域名时 rclone 默认丢掉 `Authorization:` 头 | S07 | 官方默认 |
| 使用 `writes`/`full` 写缓存时，全局 `--transfers`（默认 4）决定从缓存并行上传的数量；`--checkers` 对 VFS 无效 | S06 | `the related global flag --checkers has no effect on the VFS` |
| （内核口径）`allow_other` 会**覆盖**「仅挂载用户可访问」的安全限制 | S09 | `This option overrides the security measure restricting file access to the user mounting the filesystem.` |
| （内核口径）`allow_other` **默认只允许 root 使用**，该限制可通过一个用户态配置项解除 | S09 | `This option is by default only allowed to root` |
| （内核口径）设置 `user_allow_other` 配置项后，挂载用户即可添加 `allow_other` | S09 | `the mounting user can add the 'allow_other' mount option which disables the check for other users' processes` |
| （内核口径）FUSE 由内核模块 `fuse.ko`、用户态库 `libfuse.*`、挂载工具 `fusermount` 三部分组成 | S09 | 官方定义 |
| （内核口径）`fusermount` 以 setuid root 安装；对非特权挂载总是添加 `nosuid` 与 `nodev` | S09 | 官方行为 |
| （内核口径）FUSE 默认**不检查**文件访问权限，由文件系统自行实现访问策略；`default_permissions` 启用权限检查，通常与 `allow_other` 同用 | S09 | 官方默认 |
| （内核口径）`allow_other` 只允许**同一 userns 或其后代**中的用户访问 | S09 | 官方限制 |
| （社区经验）`--allow-other` 需要 `/etc/fuse.conf` 中的显式许可，「没有它就不会工作」；启用命令 `sudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf` | S10 | **T3 社区经验** |
| （社区经验）unit 放 `/etc/systemd/system/<name>.service`，`Type=notify`、`User=`、`After=network-online.target`、`Restart=always`、`RestartSec=10`、`WantedBy=default.target`、`AssertPathIsDirectory=`、ExecStop 用 `fusermount3 -u` | S10 | **T3 社区经验** |

### 3.5 映射给 Docker 容器（第 5 章）

| 断言 | 来源 | 层级 |
|---|---|---|
| bind mount 把宿主机文件/目录挂进容器；volume 则由 Docker 在自身存储目录内创建并维护 | S11 / S18 | 官方定义 |
| **选型关键**：需要**从主机访问这些文件**时 volume 不是好选择，因为 volume 完全由 Docker 管理；需要容器与主机同时访问文件/目录应使用 **bind mount** | S18 | `Volumes are not a good choice if you need to access the files from the host` |
| volume 使用 `rprivate` bind propagation，且**不可配置** | S18 | `Volumes use rprivate (recursive private) bind propagation, and bind propagation isn't configurable for volumes.` |
| volume 存放在 Docker 主机目录，`docker inspect` 中 `Source` 形如 `/var/lib/docker/volumes/<name>/_data`，`Type` 为 `volume` | S18 | 官方示例 |
| 一般更推荐 `--mount`，它更显式且支持全部可用选项 | S11 / S18 | `In general, --mount is preferred.` |
| `-v`/`--volume` 挂载宿主机上**尚不存在**的路径时，Docker 会自动创建该目录，且**始终创建为目录** | S11 | `Docker automatically creates the directory on the host for you. It's always created as a directory.` |
| `--mount` 默认**不会**自动创建不存在的源路径，而是报错 | S11 | `docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.` |
| bind mount **默认对宿主机文件有写权限**，可用 `readonly`/`ro` 阻止容器写入 | S11 | `Bind mounts have write access to files on the host by default.` |
| 把 bind mount 挂进容器内**非空目录**时，原有内容被**遮蔽**（obscured）；且容器内没有直接卸下挂载恢复原内容的办法，只能重建容器 | S11 / S18 | `the pre-existing files are obscured by the mount` / `there's no straightforward way of removing a mount to reveal the obscured files again` |
| ⚠️ S11 明说该遮蔽行为**与 volume 不同** | S11 | `However, it can also be surprising and this behavior differs from that of volumes.` ← 第 5 章 bind mount vs volume 的直接依据 |
| bind mount 创建于 **Docker daemon 所在主机**，不是客户端 | S11 | `Bind mounts are created to the Docker daemon host, not the client.` |
| bind propagation 默认 `rprivate`（双向都不传播）；可取值 `rprivate`/`private`/`rshared`/`shared`/`rslave`/`slave`；**仅 bind mount 可配置，且仅限 Linux 宿主机** | S11 | `Bind propagation defaults to rprivate for both bind mounts and volumes.` |
| `shared` 为双向传播，`rshared` 在此基础上扩展到嵌套挂载点；**挂载传播在 Docker Desktop 下不工作** | S11 | `Mount propagation doesn't work with Docker Desktop.` |
| 递归只读挂载需 **Linux 内核 5.12+**；低于 5.12 时子挂载默认自动以读写挂载 | S11 | `Recursive read-only mounts require Linux kernel version 5.12 or later.` |
| `bind-recursive` 选项**仅 `--mount` 支持**，`-v`/`--volume` 不支持 | S11 | `This option is only supported with the --mount flag, not with -v or --volume.` |
| SELinux：`z` 表示内容在多个容器间共享，`Z` 表示私有不共享；**改动作用于宿主机文件本身** | S11 | `The Z option indicates that the bind mount content is private and unshared.` |
| 用 `--mount` **无法**修改 SELinux 标签；且与 services 一起用时 `:Z`/`:z` 与 `:ro` 会被忽略 | S11 | `It is not possible to modify the SELinux label using the --mount flag.` |
| （LinuxServer.io 口径）Docker 把容器都跑在 `root` 用户域下，因此容器内进程也以 root 运行；容器生命周期内创建的文件都归 `root` 所有，从而你无法访问 | S12 | `all files and directories created during the container's lifespan will be owned by root` |
| （LinuxServer.io 口径）PUID/PGID 用于把容器内部用户**映射到宿主机上的某个用户** | S12 | `map the container's internal user to a user on the host machine` |
| （LinuxServer.io 口径）取值最常用自己的 `id`，经 `id $user` 获取，关注 `uid` 与 `gid` 两项 | S12 | `The two values you will be interested in are the uid and gid.` |
| （LinuxServer.io 口径）⚠️ 该组织的镜像**尚不兼容** `--user` flag，建议继续用 PUID/PGID | S12 | `Our images are not yet compatible with this, so we recommend continuing usage of PUID and PGID.` |

## 4. 矛盾、更正与缺口

### 4.1 ⚠️ P1 阶段的三条**伪引证**（已核实推翻）

P1 的 subagent 把**自己训练知识里的内容**挂上了来源 ID。P2 回源逐条核对后确认如下——三条都**不得进入正文**，除非另找来源：

| P1 原表述 | 声称来源 | 核实结果 |
|---|---|---|
| 「OpenList 内置 WebDAV …也可为**单个存储加子路径**」 | S02 | ❌ **S02 全文无此内容**。S02 只给 `/dav/` 端点与 Path=`dav`。S04（上游 AList）也无「按存储追加子路径」。→ 见开放问题 Q2 |
| 「架构二：容器内跑 `rclone mount`，需 `--device /dev/fuse`、`SYS_ADMIN`、`apparmor:unconfined`、`/etc/passwd` 只读挂载、`:shared` 传播」 | S06 | ❌ **S06 完全没有容器相关内容**（提取器 Gaps 明确列出：未提及 `/dev/fuse`、`SYS_ADMIN`、mount propagation、Docker）。该表述来自模型自身知识。→ 方向 A 不需要它，已排除 |
| 「S12 明确 PUID/PGID **不是 Docker 特性**而是镜像 entrypoint 读的环境变量；`chown` 只覆盖 `/config` 不覆盖媒体挂载点；UMASK=002、setgid 2775、911:911」 | S12 | ❌ **S12 全都没有**。实际 S12 只有：容器默认 root 域运行、创建文件归 root、PUID/PGID 映射到宿主机用户、`id $user` 取值、以及「镜像尚不兼容 `--user`」。 |

> 同类更正：P1 称 S11 记载「宿主机 UID/GID 直接带入容器导致 permission denied」——**S11 全文未讨论 uid/gid 属主**（见缺口 G5）。

**处置**：以上更正已记录在 `01_explore_result.md` 的对应条目之外（本文件为权威）。第 5 章的两条断言（选型依据、`:ro` 写法）改由 S18 与 S11 的**实际原文**支撑，均已在 §3.5 重新映射。

### 4.2 真实的路线冲突：PUID/PGID vs `user:`

这不是矛盾，而是一个**必须让读者知道的分岔点**，取决于镜像由谁维护：

| | OpenList 官方镜像（S01） | LinuxServer.io 镜像（S12） |
|---|---|---|
| v4.1.0 之后 | **移除** `PUID`/`PGID`，内置 `openlist(1001)`，用 `user:` / `--user` | 仍推荐 `-e PUID` / `-e PGID` |
| 对 `--user` 的态度 | 官方推荐用法之一 | **明确说镜像尚不兼容** |

> 本笔记终点容器若选 LinuxServer.io 系（qBittorrent、Jellyfin 等常见镜像），则**两个容器用两套不同机制**——这正是第 5 章最该讲清的一点。

### 4.3 `allow_other` 的配置位置：来源层级要分清

- **内核文档（S09）**只说存在「a (userspace) configuration option」，**全文没有出现 `/etc/fuse.conf` 这个路径**，也没给未设置时的默认值或报错文案。
- **`/etc/fuse.conf` + `user_allow_other`** 这个具体位置来自 **T3 社区帖（S10）**，且该帖未给出任何报错原文。

→ 写正文时可断言「FUSE 默认只允许 root 使用 `allow_other`，需用户态配置项解除」（S09 官方）；但断言「配置项在 `/etc/fuse.conf`」时必须标为**社区经验**，或另找 libfuse 文档补源。

### 4.4 ⚠️ 抓取缺陷（下游不得逐字照抄）

| 源 | 缺陷 | 影响 |
|---|---|---|
| S01 | compose 段落中 YAML 列表项的 `- ` 引导符被剥离，volumes/ports 行丢失缩进，形如 `'./data:/opt/openlist/data'` 顶格 | **不能直接照抄该 YAML**。第 1 章需按官方页面结构还原缩进，或改以 `docker run` 一行命令为准（`docker run` 那几条抓取完整） |
| S12 | 正文空格被去掉，如 `dockercreate--name=beets-ePUID=1000-ePGID=1000linuxserver/beets` | 该文件里的命令串不可直接复制 |
| S11 | Compose 示例整段被去掉换行与缩进，仅键名 `type:bind` / `source:./static` / `target:/opt/app/static` 可用；`--volume` 选项表中 SELinux 那行的选项名（`z`/`Z`）在表格里丢失 | 第 5 章的 compose 片段需依官方语义重写，不要声称逐字引用 |
| S15 | 驱动索引页只有导航壳，**无任何正文**（277 字节） | 见 G6 |

### 4.5 覆盖缺口

| ID | 缺口 | 影响与建议 |
|---|---|---|
| G1 | **没有官方来源串起 OpenList + WebDAV + rclone + 目标容器的完整 compose** | 第 5 章的端到端片段必须由 S11/S18/S01/S02 的语义**拼装**，并在正文标注哪部分是官方字段、哪部分是编排 |
| G2 | **目标容器未定**（qBittorrent？Jellyfin？） | 第 5 章的消费者侧只能是通用模式（`:ro` 只读 vs 读写），或请用户先定终点容器 |
| G3 | 官方无 systemd 页面，开机自启只有 T3 来源 | 该节结论标为社区经验；或用 S06 的 systemd 段落（Type=notify、PATH 回退）作官方支撑 |
| G4 | 全文未覆盖 **Windows / WSL** 侧（Windows 的 `rclone mount` 依赖 WinFsp） | 正文须明确「以 Linux 宿主机为准」，避免用户照抄失败 |
| G5 | **bind mount / volume 的属主与权限行为无官方来源**（S11、S18 均未讨论 uid/gid） | 第 5 章的权限结论只能用 S12 的镜像侧口径 + S06 的 `--uid/--gid/--umask` 支撑，**不能声称 Docker 官方定义了 bind mount 属主规则** |
| G6 | **OpenList 驱动索引页无正文**，官方驱动全清单只能从站点 `sitemap.xml` 得到 | 正文如需列驱动，注明来源为站点 sitemap；`http://doc.oplist.org/sitemap.xml` 实测 200 |
| G7 | S04 为 **2022-09-07 发布的上游 AList 口径**，未标注更新日期 | 能力矩阵引用时必须标口径与日期 |

## 5. 实战素材（逐字，可直接进正文）

### 5.1 OpenList 三种运行身份（S01，`docker run` 行逐字完整）

```bash
# A. v4.1.0 以后（不含 v4.1.0）——以「当前用户」运行
mkdir -p /etc/openlist
docker run --user $(id -u):$(id -g) -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e UMASK=022 --name="openlist" openlistteam/openlist:latest

# B. v4.1.0 以后（不含 v4.1.0）——以容器内置 1001 用户运行
sudo chown -R 1001:1001 /etc/openlist
docker run -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e UMASK=022 --name="openlist" openlistteam/openlist:latest

# C. v4.1.0 及以前
docker run -d --restart=unless-stopped -v /etc/openlist:/opt/openlist/data -p 5244:5244 -e PUID=0 -e PGID=0 -e UMASK=022 --name="openlist" openlistteam/openlist:latest
```

### 5.2 管理员密码（S01，逐字）

```bash
# 首次运行：日志里会给初始密码
docker logs openlist        # Successfully created the admin user and the initial password is: xYZabHGf

# 非首次：随机重生成 / 手动设定
docker exec -it openlist ./openlist admin random
docker exec -it openlist ./openlist admin set NEW_PASSWORD
```

### 5.3 更新（S01，逐字）

```bash
# watchtower 一次性更新
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock containrrr/watchtower openlist --cleanup --run-once

# compose 方式
docker compose pull
docker compose down
docker compose up -d
```

### 5.4 rclone WebDAV 远端（S07 字段 + 对 OpenList 的取值推断）

```ini
[openlist]
type = webdav
url = http://<宿主机IP>:5244/dav/
vendor = other
user = <OpenList 用户名>
pass = <obscure 后的密码>
```

> ⚠️ `url` 与 `user`/`pass` 的**字段名与必填性**来自 S07（官方）；`vendor = other` 是基于 S07 的 `vendor` 取值表 + 「普通 WebDAV 不支持 mtime/hash」做出的**推断**——OpenList 不属于 fastmail/nextcloud/owncloud/infinitescale/sharepoint 任何一类。推断理由必须在正文写出。
> ⚠️ `pass` 不能直接填明文，须经 `rclone obscure` 或交互式 `rclone config` 生成（S07 官方要求）。

### 5.5 关键默认值速查（S06 官方）

| 参数 | 默认值 |
|---|---|
| `--vfs-cache-mode` | `off` |
| `--vfs-cache-max-age` | `1h0m0s` |
| `--vfs-cache-max-size` | `off`（不限制） |
| `--vfs-cache-poll-interval` | `1m0s` |
| `--vfs-write-back` | `5s` |
| `--dir-cache-time` | `5m0s` |
| `--poll-interval` | `1m0s` |
| `--attr-timeout` | `1s` |
| `--buffer-size`（正文提及，Options 表未列默认） | — |
| `--uid` / `--gid` | `1000` / `1000` |
| `--umask` | `002` |
| `--file-perms` / `--dir-perms` | `666` / `777` |
| `--daemon-wait` | `1m0s` |
| `--transfers`（全局） | `4` |
| `--max-read-ahead` | `128Ki` |
| `--vfs-read-wait` / `--vfs-write-wait` | `20ms` / `1s` |

### 5.6 systemd unit（S10，社区经验，逐字）

```ini
[Unit]
Description=rclone Google Drive
AssertPathIsDirectory=/home/YOUR_USER/google_drive
After=network-online.target

[Service]
Type=notify
User=YOUR_USER
ExecStart=/usr/bin/rclone mount --config=/home/YOUR_USER/.config/rclone/rclone.conf --vfs-cache-mode full --vfs-cache-max-age 4h --vfs-fast-fingerprint --vfs-refresh --allow-other --log-file=/home/YOUR_USER/.local/log/rclone_gdrive.log --log-level INFO "YourRemote:" /home/YOUR_USER/google_drive
ExecStop=/bin/fusermount3 -u /home/YOUR_USER/google_drive
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
sudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf
grep user_allow_other /etc/fuse.conf            # 应输出 user_allow_other
mkdir -p ~/.local/log
sudo systemctl daemon-reload
sudo systemctl enable --now rclone-gdrive.service
systemctl status rclone-gdrive.service          # 应见 Active: active (running)
```

> 注：`ExecStop` 用 `fusermount3` 是因该帖用 Fedora / FUSE3；Debian/Ubuntu 视 FUSE 版本而定。
> `Type=notify` 有 S06 官方佐证（挂载就绪后服务才 started）；其余 unit 指令为社区经验。

### 5.7 Docker 挂载两种写法（S11 / S18 逐字）

```bash
# bind mount（把宿主机 rclone 挂载点交给容器）
docker run --mount type=bind,src=<宿主机路径>,dst=<容器内路径>,ro
docker run -v <宿主机路径>:<容器内路径>:ro

# 传播（需要容器内子挂载可见时）
docker run -v "$(pwd)"/target:/app2:ro,rslave
docker run --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave

# named volume
docker run --mount type=volume,src=<volume名>,dst=<容器内路径>,ro
docker run -v <volume名>:<容器内路径>:ro
```

Compose（S18 抓取残缺，仅键名可用）：`type: bind` / `source: ./static` / `target: /opt/app/static`。
Compose volume 段同理：`type: volume` / `source: <name>` / `target: <path>`。

## 6. 开放问题（需用户或实操确认）

| ID | 问题 | 现状 |
|---|---|---|
| Q1 | OpenList 是否存在**全局**「开启 WebDAV」开关？ | S02 只讲用户权限项，未提全局开关；S17 显示 WebDAV 是**每存储**的 `Webdav policy`。倾向「没有全局开关」，但**未证实** |
| Q2 | `/dav/<挂载路径>` 的路径结构是否为官方定义？ | S02 只给 `/dav/`；`Mount Path` 系 S17 的存储位置字段。二者拼接是**推断**，未经官方文档证实 |
| Q3 | rootful Docker 下 `--user 0:0` 的确切含义？与镜像内 `openlist(1001)` 的优先级？ | S01 只在 **rootless** 语境解释过；rootful 未说明 |
| Q4 | bind mount 的**属主/权限**官方行为 | 无官方来源（G5）。实操中最可能踩的坑，却缺一手依据 |
| Q5 | 目标容器是哪个？ | 未定（G2）。影响第 5 章是否能给完整 compose |
| Q6 | `Mount Path` 是否可嵌套（如 `/A/B`）？是否影响 WebDAV 路径？ | S17 未说明 |
| Q7 | v4.1.0 的确切发布日期与变更单 | S01 未给（其 Gaps 明确指出） |

## 7. 下游交接（给 outline-generator / chapter-writer）

**必须遵守的三条**

1. **不要相信本文件的转述**。本文件 §3 的每一行都给了源 ID 与锚点，写章节时**必须打开 `sources/S<ID>_*.md` 回原文核对**，尤其是标了引号的部分。P1 阶段已经因为转述产生过三条伪引证（§4.1）。
2. **`sources/S05`、`S08`、`S13`、`S14` 不存在**，禁止引用这四个编号。
3. **区分层级**：官方口径（T1）/ 上游口径（S04，须标注）/ 社区经验（S10，须标注）。§4.3 的 `allow_other` 配置位置就是典型反例。

**章节骨架建议（方向 A，6 章）**

| 章 | 主题 | 主用来源 | 核心坑 |
|---|---|---|---|
| 1 | 用 Docker 跑起 OpenList | S01 | v4.1.0 运行身份分岔；`/opt/openlist/data` 持久化；首启密码 |
| 2 | 把网盘聚合进来 | S17 S16 S03 | `Mount Path` 三义且必填唯一；重名报 DB 约束错；代理与 WebDAV 策略 |
| 3 | 开出 WebDAV 服务 | S02 S03 S04 | 不是找开关而是开权限；只开「管理」不够；端口必须与网页端一致 |
| 4 | 用 Rclone 挂到本地 | S07 S06 S09 S10 | `vendor` 取值与 mtime/hash 缺失；`--vfs-cache-mode` 选档；`allow_other` 与 fuse.conf |
| 5 | 映射给 Docker 容器 | S18 S11 S12 | 为什么必须 bind mount 而不是 volume；`-v` 会自动建目录；PUID/PGID 与 `user:` 两套机制 |
| 6 | 排障速查 | 全部 | 见 §4.5 缺口与 §4.4 抓取缺陷 |

**体量提示**：6 章 + 大量配置片段，成品预计超过 30KB。按项目经验（learnings），组装后**建议拆分**为「分册子目录 + README + 每章独立文件 + 前后导航」，但最终听用户选择。

**P2 素材质量自评**

- 官方来源数：13（T1）／社区 1（T3）——主干不依赖社区帖
- 深度文章数：N/A（本主题无需学术或综述类）
- 未解缺口：7 项（Q1–Q7），其中 Q5（终点容器）需用户输入

## 8. 进阶路径（仅收录有来源支撑的部分）

方向 A 主线上手即可，以下仅作「跑通之后可以往哪走」的路标，来源均已核实：

| 方向 | 可用抓手 | 来源 | 备注 |
|---|---|---|---|
| 直链与代理 | 存储级 `Webdav policy` 三选一（302 重定向 / 代理 URL / 本机代理）；`Download proxy URL`；Cloudflare Workers、`OpenList-Proxy` 二进制、自建 `PROXY_URL/path?sign=sign_value` | S17 | 官方字段与官方文档链接 |
| 读写加速 | `--vfs-cache-mode full` + `--vfs-read-ahead` / `--buffer-size` / `--vfs-read-chunk-size` | S06 | 官方参数；注意 §3.4 的稀疏文件与 exFAT 警告 |
| 缓存调优 | `--vfs-cache-max-size`、`--vfs-cache-max-age`、`--vfs-cache-poll-interval` 组合；`--cache-dir` 隔离多实例 | S06 | 官方参数与默认值见 §5.5 |
| 目录刷新 | `SIGHUP` 刷新全部目录缓存；`rclone rc vfs/forget` 细粒度失效 | S06 | 官方行为 |
| 多网盘聚合 | 用别名存储规避 `Mount Path` 唯一约束；`ref:/mount_path` 复用令牌；按路径设缓存策略（`*` / `**` 通配） | S17 | 官方字段 |
| 挂载健康监控 | `rclone rc` 远程控制接口（配合 `--rc` 开启） | S06 | 官方行为；具体指标需另找来源 |

> ⚠️ 未覆盖（方向 A 明确排除，如需展开须另开 P2）：限速与并发控制、告警集成、多用户配额、反向代理前置（Nginx/Caddy）——`00_intent.md` 的「WebDAV 反代前缀」坑项因此**尚无来源**，正文若要写须先补收集。
