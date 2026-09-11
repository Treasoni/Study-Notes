## 学习笔记大纲：《OpenList 聚合网盘 → WebDAV → Rclone → Docker 全链路实战》

> 笔记类型：实战教程（practice 为主 + 少量 concept 铺垫）
> 预计总篇幅：约 30KB+（6 章，其中 5 章含配置/命令片段）
> 章节数：6
> 深度：上手
> 读者基线：已会基础 Docker / Linux（能读懂 `docker run`、`-v`、`compose.yaml`、`systemctl`），但首次接触这条链路
> 环境基线：**Linux 宿主机 + Docker Compose**；Windows/WSL 差异只在必要处标注
> 写法：逐章写作，每章写完停下等确认后再写下一章

---

## 全局写作红线（每章都必须遵守）

- **三条已推翻的归属不得复活。** `02_deep_research.md` §4.1 记录的三条 P1 伪造引证已被回源核对推翻；本大纲及其下游正文**不包含、不得以任何形式重新引入**这三条结论。若正文确需相关结论，必须另找来源，否则整段不写。
- **S05 / S08 / S13 / S14 不存在对应文件。** 禁止在任何章节引用这四个编号（它们只出现在 P1 候选清单里，正文从未被读取）。
- **不得把 `02_deep_research.md` 的转述当引文。** 凡需要官方措辞（引号内文本），写章节时必须回到 `sources/S<ID>_*.md` 打开原文核对；深研文件 §3 / §5 只能当索引用。
- **层级必须标注**：T1 官方口径 / **S04 为上游 AList 口径（须标出处与日期）** / **S10 为社区经验（须标注）**。
- **待核实节点不得写成结论。** 依赖 Q1 / Q2 / Q3 / Q4 / Q6 的段落按本大纲标注为 待核实。
- **不新编来源、统计数据、版本号、命令参数或 flag。**
- **S15（驱动索引页）是空壳页**（277 字节、无正文），不可作为素材；如需列官方驱动清单，来源只能标注为站点 `sitemap.xml`（缺口 G6）。

---

### 第一章：用 Docker 跑起 OpenList

- **篇幅**：中（约 5 页）
- **覆盖要点**：
  - 镜像与标签：`latest` / `v*.*.*` / `beta`，以及预装环境后缀 `-lite` / `-aio` / `-aria2` / `-ffmpeg` 的选择场景
  - 端口 `5244:5244`、容器内数据目录 `/opt/openlist/data`；`/etc/openlist` 只是**默认**映射目录、可换
  - **本章核心分岔：运行身份**。v4.1.0 以后（**不含 v4.1.0**）已移除 `PUID`/`PGID`，改用内置 `openlist`（UID 1001）/ 组（GID 1001）并以它跑 `openlist server`，官方要求用户**自行处理映射目录权限**；三种写法：compose `user: '0:0'` / CLI `--user $(id -u):$(id -g)` / `chown -R 1001:1001` 后走内置用户；v4.1.0 及以前用 `-e PUID=0 -e PGID=0`
  - 环境变量：`UMASK`（默认 `022`）、`UTC`、`RUN_ARIA2`（视镜像是否预装）、`OPENLIST_ADMIN_PASSWORD`；镜像默认以 `--no-prefix` 运行，故无需 `OPENLIST_` 前缀
  - 首次登录：`docker logs openlist` 取初始密码；`admin random` / `admin set NEW_PASSWORD`
  - 升级三法：watchtower `--run-once` / Docker CLI 四步 / compose `pull` + `down` + `up -d`
  - 概念铺垫（少量，1 段即可）：为什么数据目录必须显式映射，否则配置与账号在重建容器时丢失
- **素材引用**：**S01**（T1，本章唯一主干）。回源：`sources/S01_openlist_docker_install.md`（Docker CLI 段、Env 表、Image Versions、Update 段）。深研文件 §3.1 / §5.1–§5.3 只作导航。
- **代码示例**：有
  - 三种运行身份 `docker run`（S01 抓取**完整**，可逐字）
  - 密码获取与重设命令（S01）
  - 升级三法（S01）
  - ⚠️ **compose YAML 不可照抄**：S01 抓取时 YAML 列表项 `- ` 引导符被剥离、volumes/ports 行丢失缩进（§4.4）。正文须按官方页面结构**还原缩进**后使用，或本章只以 `docker run` 为准并把 compose 段明确标为"按官方结构还原"
- **待核实**：**Q3** — rootful Docker 下 `--user 0:0` 的确切含义，以及与镜像内 `openlist(1001)` 的优先级（S01 只在 **rootless** 语境解释过）。该小节标 待核实，不给结论。
- **章末可跑产出**：浏览器能打开 `http://<宿主机IP>:5244` 并登录；重启容器后账号与配置仍在。

---

### 第二章：把网盘聚合进来

- **篇幅**：中（约 5 页）
- **覆盖要点**：
  - 存储是"逐条添加"的模型：`Mount Path`（挂载路径）**三义**——挂载项唯一标识 / 对外展示名 / 要挂载到的位置；填 `/` 表示挂到根
  - 两条硬约束与**官方报错原文**：留空报 `MountPath ... 'required' tag` 校验失败；重名报 `UNIQUE constraint failed: x_storages.mount_path`，官方解法是**用别名存储聚合**
  - `Order`（越小越靠前，可填负数）、`Remark` 与 `ref:/mount_path` 令牌复用（当前仅支持 139Yun、AliyundriveOpen、189CloudPC、123PanShare、Cloudreve V3/V4）
  - 缓存两层：`Cache Expiration` 是**目录结构**的缓存时间；`Custom Cache Policies` 按路径设分钟数，`*` 匹配单层、`**` 匹配多层
  - 代理两件事别混：`Webdav policy`（302 重定向 / 使用代理 URL / 本机代理，默认值取决于驱动有没有 302 选项）与 `Web proxy` 是**两个不同配置**；`Download proxy URL` 留空时默认走本机传输
  - 示例驱动走一遍本地存储：`Root folder path`、回收站路径（留空=永久删除）、缩略图（视频需外部 `ffmpeg`；PDF 缩略图默认关、仅 macOS）
  - 权限前置（简短带入，详述留第三章）：用户字段 `Username` / `Password` / `Base path`；连续 6 次密码错误封 IP 30 分钟、重启服务可解；游客账户默认停用
  - 概念铺垫（少量）："挂载路径"这一抽象为什么重要——它是对外名称，也可能是 WebDAV 路径的组成部分（**此处只提出，不在本章下结论**，结论留给第三章）
- **素材引用**：**S17**（T1，主干）、**S16**（T1，示例驱动）、**S03**（T1，用户与权限）。回源：`sources/S17_openlist_driver_common.md`、`sources/S16_openlist_driver_local.md`、`sources/S03_openlist_user_permission.md`。**不得引用 S15**（空壳页）。
- **代码示例**：**无**（本章素材是界面配置字段 + 官方报错原文，不含可执行代码）。两条官方报错 JSON 原文可引用，但须回源核对字段名大小写——官方英文版与中文版报错文案不同。
- **待核实**：**Q6** — `Mount Path` 是否可嵌套（如 `/A/B`）、是否影响 WebDAV 路径，S17 未说明 → 标 待核实。
- **章末可跑产出**：至少挂上 1 个存储（建议先用本地存储驱动打通，再换真实网盘），在网页端根路径下看到它，并能浏览/下载一个文件。

---

### 第三章：开出 WebDAV 服务

- **篇幅**：短（约 2–3 页）
- **覆盖要点**：
  - 概念铺垫（核心概念之一，约 1 段）：WebDAV 是 HTTP 的扩展集；OpenList 自身即可作为 WebDAV 服务器
  - **核心认知：这里没有"全局开关"可找**——启用方式是在 `用户 => 权限` 里给特定用户开权限项
  - 两个权限项的分工：`WebDAV 读取`（查看/读取/播放，只需此项即可）；`WebDAV 管理`（写入）；**仅开"管理"还不够**，必须同时开启计划操作对应的具体文件系统权限（重命名 / 删除 / 复制 / 创建目录或上传 / 移动 等）
  - 连接参数表：Url `http[s]://<域名>:<端口>/dav/`、Path 填 `dav`；**端口必须与网页端完全一致**；用户名密码即网页端登录账号密码；协议官方**强烈建议 https**
  - 已知限制：暂不支持"复制时重命名"；官方"存储支持"章节目前是 WIP（无正文）
  - 官方推荐客户端（作为第四章入口）：Linux 用 `rclone`（功能丰富）或 `davfs2`；Windows 用 RaiDrive
  - **层级标注**：S04 是**上游 AList 口径（2022-09-07 发布，未标注更新日期）**，只能作为与 S02 互相印证的旁证；其驱动能力矩阵如被引用，必须写明口径与日期
- **素材引用**：**S02**（T1，主干）、**S03**（T1，权限项）、**S04**（⚠️ **上游 AList 口径**，须标注来源与 2022-09-07 日期）。回源：`sources/S02_openlist_webdav.md`、`sources/S03_openlist_user_permission.md`、`sources/S04_alist_webdav_upstream.md`。§4.3 式分层是硬要求：官方结论与社区/上游口径不得混写。
- **代码示例**：**无**——S02 与 S04 都**没有给出 WebDAV 端点的验证命令示例**。本章的"可跑"产出改为**一份可直接填进 WebDAV 客户端的连接参数表**，并在正文显式说明"可脚本化的端点验证归第四章"（把"本章无法自证"如实写出，不新编 `curl`/`PROPFIND` 之类未经来源支持的探测命令）。
- **待核实**：
  - **Q1** — 是否存在**全局**的"开启 WebDAV"开关？S02 只讲用户权限项，S17 显示 WebDAV 是**每存储**的 `Webdav policy`；倾向"没有全局开关"但**未证实** → 标 待核实。
  - **Q2** — `/dav/<挂载路径>` 的路径结构是否为官方定义？`/dav/` 来自 S02，`Mount Path` 来自 S17，**二者拼接属推断** → 标 待核实；正文如写必须说明是推断。
- **章末可跑产出**：权限开齐、参数表填好，能用一个 WebDAV 客户端登录，并看到第二章挂载进来的内容。

---

### 第四章：用 Rclone 挂到本地

- **篇幅**：长（约 8 页以上）
- **覆盖要点**：
  - 概念铺垫（核心概念之一，约 1 段半）：rclone 是什么；`rclone mount` 用 **FUSE** 把云存储挂成本地文件系统
  - **FUSE 三件套**（内核模块 `fuse.ko` / 用户态库 `libfuse.*` / 挂载工具 `fusermount`）；`fusermount` 以 setuid root 安装，对非特权挂载总是加 `nosuid` + `nodev`；FUSE 默认**不检查**访问权限（由文件系统自行实现策略，`default_permissions` 才启用检查，通常与 `allow_other` 同用）；`allow_other` 只允许同一 userns 或其后代访问
  - 远端配置：`type = webdav`、`url` **必填**、`pass` 必须经 obscure；`vendor` 取值表；**普通 WebDAV 不支持修改时间、不支持哈希**（只有 Fastmail / ownCloud / Nextcloud 例外）；`--webdav-auth-redirect` 默认 false 会丢掉 `Authorization:` 头
  - `rclone mount` 基本语义：挂载点必须是**已存在且为空**的目录；默认前台运行，`--daemon` 强制后台（Windows 只支持前台）；后台模式需手动 `fusermount -u` / `fusermount3 -u`
  - **本章主坑：`--vfs-cache-mode` 四档选型**（默认 `off`）。`off` 的代价：读写都直连远端、不支持读+写同时打开、写不能 seek、必须带 `O_TRUNC`、**上传失败不能重试**；`minimal` 磁盘占用最小；`writes` 支持全部常规操作且上传按指数间隔重试最长 1 分钟；`full` 全部经磁盘缓冲、缓存是**稀疏文件**（FAT/exFAT 不支持，会性能崩并记 ERROR）。顺带讲清 mount 与 sync/copy 的可靠性差异（S06 明文：mount 不能同样重试）
  - 关键默认值速查（正文内小表）：`--vfs-cache-mode off`、`--vfs-cache-max-age 1h0m0s`、`--vfs-write-back 5s`、`--dir-cache-time 5m0s`、`--attr-timeout 1s`、`--uid/--gid 1000`、`--umask 002`、`--file-perms 666`、`--dir-perms 777`、`--daemon-wait 1m0s`、全局 `--transfers 4`
  - 两条风险提示：多个 rclone 实例共用/重叠同一 remote 的 VFS 缓存**可能数据损坏**（用 `--cache-dir` 隔离）；`--attr-timeout` 窗口内远端文件长度变化可能出现**截断或末尾乱码**
  - 系统集成：systemd 下可用 `Type=notify`（S06 官方佐证：挂载点就绪后服务才进入 started）；⚠️ systemd 跑 mount unit 时**没有环境变量**（含 PATH、HOME）、`~` 不展开，须显式传绝对路径的 `--config` / `--cache-dir`，且 PATH 会回退到 `/bin:/usr/bin`（须确保其中有 fusermount/fusermount3）；新版 Ubuntu 可能因 Apparmor 报 fusermount3 权限错误；`--poll-interval` 必须小于 `--dir-cache-time`（设为 0 可禁用）；可 `kill -SIGHUP $(pidof rclone)` 或 `rclone rc vfs/forget` 刷新目录缓存
  - **`allow_other` 的层级分界（§4.3 的典型反例，必须写清）**：内核文档（S09）只说存在"a (userspace) configuration option"，**没有出现 `/etc/fuse.conf` 这个路径**、也没给默认值与报错文案；`/etc/fuse.conf` + `user_allow_other` 这个具体位置来自 **T3 社区帖（S10）**。可断言"FUSE 默认只允许 root 使用 `allow_other`，需用户态配置项解除"（S09 官方）；断言"配置项在 `/etc/fuse.conf`"必须标为**社区经验**
  - 开机自启（缺口 G3）：官方**没有** systemd 页面，unit 写法只能标为**社区经验（S10）**
- **素材引用**：**S07**（T1，remote 配置）、**S06**（T1，mount 与 VFS 主干）、**S09**（T1，内核口径的 FUSE）、**S10**（⚠️ **T3 社区经验**，systemd unit 与 `/etc/fuse.conf` 位置必须显式标注）。回源：`sources/S06_rclone_mount.md`、`sources/S07_rclone_webdav_remote.md`、`sources/S09_fuse_kernel_doc.md`、`sources/S10_rclone_systemd_forum.md`。
- **代码示例**：有
  - `rclone.conf` 远端片段——`url` / `user` / `pass` 的**字段名与必填性**来自 S07 官方；`vendor = other` 属**推断**（OpenList 不属于 fastmail/nextcloud/owncloud/infinitescale/sharepoint 任何一类），**推断理由必须写进正文**；`pass` 需 `rclone obscure` 或交互式 `rclone config` 生成
  - `rclone mount` 命令（参数取自 S06 官方）
  - systemd unit（S10，**标注为社区经验**；`ExecStop` 用 `fusermount3` 系因该帖环境为 Fedora/FUSE3，Debian/Ubuntu 视 FUSE 版本而定；`Type=notify` 有 S06 官方佐证，其余 unit 指令为社区经验）
  - `/etc/fuse.conf` 的 sed 启用与 `grep` 验证（S10，标社区经验）
  - ⚠️ S10 抓取时 unit 段的换行被压平（论坛渲染所致），正文须按 INI 结构**重排**，不要声称逐字
- **待核实**：本章无 Q 依赖；但 **G3**（无官方 systemd 来源）必须在正文标注，社区 unit 不得表述为官方推荐写法。
- **章末可跑产出**：挂载点能 `ls` 到第二章挂载的内容；`systemctl status` 见 `active (running)`；reboot 后自动恢复。

---

### 第五章：映射给 Docker 容器

- **篇幅**：中（约 5 页）
- **覆盖要点**：
  - 概念铺垫（核心概念之一）：bind mount 与 named volume 的差异；**本章为什么必须用 bind mount**——官方明文"需要从主机访问这些文件时 volume 不是好选择"（volume 完全由 Docker 管理），需要容器与主机**同时**访问同一文件/目录时应使用 bind mount
  - bind mount 语义：默认**对宿主机文件有写权限**，用 `readonly`/`ro` 阻止写入；bind mount 创建于 **Docker daemon 所在主机**（不是客户端）；挂载进容器的非空目录会**遮蔽**原有内容
  - 两种写法与选型：一般更推荐 `--mount`（更显式、支持全部选项）；`-v` 挂载宿主机上**尚不存在**的路径时会自动创建，且**始终创建为目录**；`--mount` 默认不自动创建而是**报错**（官方错误原文可用）
  - 传播：默认 `rprivate`（双向都不传播）；取值 `rprivate`/`private`/`rshared`/`shared`/`rslave`/`slave`；**仅 bind mount 可配置，且仅限 Linux 宿主机**；挂载传播在 Docker Desktop 下不工作；`bind-recursive` 选项**仅 `--mount` 支持**；递归只读需 Linux 内核 5.12+
  - SELinux：`z`（多容器共享）/ `Z`（私有不共享），改动**作用于宿主机文件本身**；`--mount` 无法修改 SELinux 标签；与 services 同用时 `:Z`/`:z` 与 `:ro` 会被忽略
  - **本章第二个必须讲清的点：运行身份的两套机制**。OpenList 官方镜像在 v4.1.0 之后**移除** `PUID`/`PGID`、改用 `user:` / `--user`；LinuxServer.io 系镜像**仍推荐** `-e PUID`/`-e PGID`，并明说其镜像**尚不兼容 `--user`**。若终点容器属 LinuxServer 系，则**同一条链路上的两个容器用两套不同机制**——这才是本章最该讲清的一点
  - **通用挂载模式（本章只写这个，不绑定具体终点容器）**：给出两条通用路径——「只读共享」（把 rclone 挂载点以 `:ro` 交给消费者容器）与「读写共享」，各自给 compose 段骨架与 `docker run` 等价写法
  - 选型反例（用来收口概念）：什么时候**确实该用** named volume（不需要宿主机访问、需要 Docker 自己管理、要跨容器安全共享、要高性能 I/O 时）
  - 可选旁支（路标，不展开）：S18 官方示例里存在 `rclone/docker-volume-rclone` 卷驱动插件，可以不经宿主机挂载点直接把远端当作 volume 使用；方向 A 主线不展开
- **素材引用**：**S18**（T1，选型依据）、**S11**（T1，bind mount 语义与传播）、**S12**（⚠️ **镜像维护方口径，非 Docker 官方，必须标注**）。回源：`sources/S11_docker_bind_mounts.md`、`sources/S18_docker_volumes.md`、`sources/S12_linuxserver_puid_pgid.md`。
- **代码示例**：有
  - bind mount 只读两种写法（S11 抓取完整，可逐字）
  - 传播示例（S11 抓取完整，可逐字）
  - named volume 对照写法（S18 抓取完整，可逐字）
  - ⚠️ **compose 片段必须重写，不能逐字**：S11 的 compose 示例整段被去掉换行与缩进（仅键名 `type: bind` / `source: ./static` / `target: /opt/app/static` 可用），S18 的 compose 示例同样被压成一行（§4.4）。正文须按 compose 语义重排，并标注"按官方字段重写"
  - ⚠️ **S12 的命令串不可复制**：正文空格被去掉（`dockercreate--name=beets-ePUID=1000-ePGID=1000...`）。如需 PUID/PGID 示例命令，须按语义重写
  - ⚠️ **G1：没有官方来源串起 OpenList + WebDAV + rclone + 目标容器的完整 compose。** 端到端片段必须由 S11/S18/S01/S02 的语义**拼装**，并在正文逐段标注哪部分是官方字段、哪部分是编排
- **待核实**：
  - **Q4 / G5** — bind mount 的**属主与权限行为无官方来源**（S11、S18 均未讨论 uid/gid）。**不得声称 Docker 官方定义了 bind mount 属主规则**；该小节只能用 S12 的镜像侧口径 + S06 的 `--uid/--gid/--umask` 支撑 → 标 待核实。
  - **Q5 / G2** — 终点容器未定，本章只写**通用**挂载模式，不绑定 qBittorrent / Jellyfin 等具体镜像；用户指定前不给完整 compose。
- **章末可跑产出**：用一个测试用容器把 rclone 挂载点以只读方式映射进去，`docker exec` 能在容器内看到文件、但写不进去；再改成读写验证一次。

---

### 第六章：排障速查

- **篇幅**：中（约 4–5 页）
- **覆盖要点**：按链路分段组织「症状 → 原因 → 动作」速查表，每段都指回具体来源
  - **第 1 章段**：容器起来但网页打不开；数据目录未映射导致重建后配置/账号全丢；v4.1.0 前后运行身份写法混用（PUID/PGID 与 `user:`）；忘记初始密码；**rootful 下 `--user 0:0` 含义未证实**（连 Q3）
  - **第 2 章段**：`Mount Path` 留空 / 重名的两条官方报错原文；`ref:` 只支持限定驱动；`Web proxy` 与 `Webdav policy` 混淆
  - **第 3 章段**：WebDAV 客户端 401/403（权限项没开齐，**只开"管理"不够**）；端口与网页端不一致；缺 https；"复制时重命名"不支持
  - **第 4 章段**：挂载点非空/不存在导致 mount 失败；`--allow-other` 不生效（`/etc/fuse.conf`，**标社区经验**）；systemd 下没有环境变量、`~` 不展开导致找不到 fusermount；AppArmor 拦 fusermount3；`--vfs-cache-mode` 选档不当导致写失败 / 不能 seek；FAT/exFAT 上 `full` 模式性能崩；目录不刷新（`--dir-cache-time` 与 `--poll-interval` 关系、SIGHUP）；**中文文件名编码**——来源未覆盖，标为"待补收集"（G4 连带）
  - **第 5 章段**：`-v` 自动建目录造成的"空目录"假象；容器内 UID 不匹配导致只读/无权限（**G5，无官方来源 → 标待核实**）；启动顺序（**先挂载再起容器**）；嵌套挂载与 `rslave`
  - **环境边界**：G4——全文未覆盖 Windows / WSL（Windows 的 `rclone mount` 依赖 WinFsp，本阶段未收集）。速查表开头必须显式声明"**仅适用 Linux 宿主机**"，Windows/WSL 条目标为未覆盖
  - **抓取缺陷"不能照抄"清单**（§4.4）汇总成一张小表，提醒读者这些片段在正文中是重写的：S01 compose YAML、S11 compose、S12 命令串、S18 compose、S15 空壳页
- **素材引用**：全部来源 S01 / S02 / S03 / S04 / S06 / S07 / S09 / S10 / S11 / S12 / S16 / S17 / S18（T1 为主；**S04 上游口径、S10 社区经验**须标注）。回源：每条速查项都要指到**具体源文件 + 段落锚点**，不得只写"见深研文件"。
- **代码示例**：有（复用前五章命令：`docker logs`、`docker inspect`、`systemctl status`、`grep user_allow_other /etc/fuse.conf`、`fusermount3 -u` 等）
- **待核实**：本章收口——把 **Q1–Q7** 与 **G1–G7** 集中列成"未决清单"，明确哪些条目在来源补齐前只能写"**未证实**"，不得给结论。

---

## 学习路径说明

### 前置要求

- 已会基础 Docker / Linux：能读懂 `docker run`、`-v`、`compose.yaml`、`systemctl`
- 一台 Linux 宿主机（或 NAS / WSL）并有 sudo 权限；Docker 与 Docker Compose 可用
- 内核支持 FUSE（第四章需要），并能安装 rclone
- 第二章起需要一个可用网盘账号；仅想打通链路时可先用本地存储驱动

### 学完能做什么

- 独立跑通整条链路：OpenList 聚合网盘 → 开启 WebDAV → rclone 挂载到本地 → 映射给 Docker 容器
- 能给任意容器做只读 / 读写两种映射，并说清为什么这里该用 bind mount 而不是 volume
- 能判断 `PUID`/`PGID` 与 `user:` 两套运行身份机制该用哪一套，以及为什么同一条链路上可能两套并存
- 能自行定位该链路的常见故障，并知道哪些结论有官方依据、哪些只是社区经验或推断

### 建议学习顺序

- 按 **1 → 2 → 3 → 4 → 5 → 6** 顺序逐章阅读；每章写完后停下确认，不要跳章
- 第二章可先用**本地存储驱动**打通闭环，再换成真实网盘，便于把"配置问题"和"驱动问题"分开定位
- 第四章先按 `--vfs-cache-mode off` 跑通，再按用途调档；不要在第一次挂载就上 `full`
- 第五章先用一个测试用容器验证映射，再换成真正的消费者容器
- 执行环境提示：本机为 Windows + Git Bash，上述命令需在 **WSL / NAS / 远程 Linux 宿主机**上执行；原文命令一律以 Linux 宿主机 + Docker Compose 为准

### 已知缺口与待核实（写作时须如实标注）

- 待核实：Q1（全局 WebDAV 开关是否存在）、Q2（`/dav/<挂载路径>` 结构是否官方定义）、Q3（rootful 下 `--user 0:0` 含义）、Q4（bind mount 属主/权限官方行为）、Q6（`Mount Path` 能否嵌套）
- 缺口：G1（无端到端官方 compose）、G2（终点容器未定）、G3（无官方 systemd 页面）、G4（未覆盖 Windows/WSL，含中文文件名编码坑项）、G5（bind mount 属主无官方来源）、G6（驱动索引页无正文）、G7（S04 无更新日期）
- 需用户输入：Q5（终点容器是哪个）——第五章给完整 compose 前必须确认

---

## 体量与拆装提示（仅标记，不在本阶段决定）

6 章 + 大量配置片段，**成品预计超过 30KB**。按项目历史经验，组装阶段（P5）建议考虑拆分为「分册子目录 + README + 每章独立文件 + 前后导航」的结构。**本阶段不决定**，待 P5 组装时由用户选择。
