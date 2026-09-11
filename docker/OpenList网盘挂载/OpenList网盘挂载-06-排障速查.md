---
title: OpenList 网盘挂载 · 第 6 册 排障速查
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
volume: 6/6
---

# 第 6 章 排障速查

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-05-Docker映射]] ｜ 目录：[[OpenList网盘挂载-00-总目录]]

前五章是一条正向链路：跑容器 → 挂网盘 → 开 WebDAV → rclone 挂到本地 → 映射进 Docker。本章反过来走一遍：**每一段出一个毛病，症状是什么、原因在哪、动手改哪里**。它的用法不是通读，而是出事时按"你卡在第几段"直接跳到对应小节查表——所以每条都标了它出自哪份来源、哪一节，方便你回原文核。

---

## 6.1 使用前提：本章只覆盖一种环境

先划边界，否则你会拿着一张不适用的表排查一个它根本不管的场景。

| 环境 | 覆盖状态 | 说明 |
| --- | --- | --- |
| **Linux 宿主机**（含 NAS） | **本章覆盖** | 全部前五章与本表均以 Linux 宿主机 + Docker 为前提 |
| **Windows / WSL** | **未覆盖（缺口 G4）** | 全部来源未讨论 Windows 侧；Windows 的 `rclone mount` 依赖 WinFsp，本阶段未收集任何相关来源，因此**不给结论、不给命令** |
| **中文文件名编码** | **待补收集** | 意图文件把"中文文件名编码"列为常见坑，但 S01–S18 中**没有任何来源**涉及它。本节不编造解释，出现乱码请先另找来源 |

> [!warning] 别把这张表用到 Windows 上
> 第 4 章的 `--allow-other`、`--uid/--gid`、`--umask` 在 rclone 官方选项表里都标注"不支持 Windows"；本章的 FUSE、`fusermount3`、`/etc/fuse.conf`、systemd 各项更全都是 Linux 概念。Windows 用户看到"未覆盖"三个字，就是本章的诚实答复，不是省略。

> [!tip] 大白话
> 把本章想成**一台车的故障速查表**。6.2–6.6 按"车头到车尾"（第 1 章到第 5 章）排；6.1 是表头的车型说明——**这张表只配 Linux 这台车**，你开的要是 Windows，表里的螺丝位置全对不上。

---

## 6.2 第 1 章段：容器起来了，但页面或数据不对

| 症状 | 原因 | 动作 | 来源 |
| --- | --- | --- | --- |
| `docker ps` 显示容器 `Up`，但浏览器打不开 `http://<IP>:5244` | 启动时漏了端口映射（`-p 5244:5244`）或映射到了别的宿主机端口 | 用 `docker ps -a` 看 `PORTS` 列是否出现 `5244`；核对启动命令里的 `-p` | S01「使用 Docker 安装」 |
| 重建容器后**配置与账号全丢** | 数据目录没映射。容器内数据目录是 `/opt/openlist/data`；只有把它映射到宿主机，数据才留在容器外 | 启动命令里必须有 `-v /etc/openlist:/opt/openlist/data` 这一项（`/etc/openlist` 只是官方示例的宿主机目录名，可以换，关键是**要映射到 `/opt/openlist/data`**） | S01「数据目录」 |
| 新版镜像加 `-e PUID`/`-e PGID` 完全不生效 | v4.1.0 以后（不含 v4.1.0）镜像**已移除** `PUID`/`PGID`，改用内置 `openlist(1001)` 用户，运行身份靠 `user:` / `--user` 指定 | 换用下表的三种形式之一；**别把 PUID/PGID 与 `user:` 混用在同一镜像上** | S01（OpenList 官方口径）；对照 S12（**镜像维护方口径**） |
| 忘了初始密码 | —— | 首次运行：`docker logs openlist`，日志里会给初始密码；之后：`docker exec -it openlist ./openlist admin random`（随机重生成）或 `./openlist admin set NEW_PASSWORD`（手动设定） | S01「管理员密码」 |
| 登录突然提示密码错误、且怎么输都不对 | 连续输入 6 次错误密码，**当前 IP 被封禁 30 分钟**；这只针对该 IP，不影响其他 IP | 等 30 分钟，或**重启容器立即解除封禁**。另注意：密码对**游客（guest）无效**，游客默认关闭 | S03「登录密码」 |

**v4.1.0 前后的三种运行身份写法**（来自 S01，逐字）：写作 `user:` / `--user` 这一侧，指的是"运行容器时直接指定容器内 OpenList 运行的用户和组"。

| 版本 | 形态 | 官方命令 |
| --- | --- | --- |
| v4.1.0 以后（不含 v4.1.0） | 以当前用户运行 | `docker run --user $(id -u):$(id -g) -d ... openlistteam/openlist:latest` |
| v4.1.0 以后（不含 v4.1.0） | 以容器内置 1001 运行 | `sudo chown -R 1001:1001 /etc/openlist` 后 `docker run -d ...`（不带 `--user`） |
| v4.1.0 及以前 | 旧写法 | `docker run -d ... -e PUID=0 -e PGID=0 ...` |

> [!warning] 缺口 G5 的邻居——运行身份与文件属主
> "命令里的 `user:` 写对了"**不等于**"容器内进程能读写挂载进来的文件"。这两个镜像还涉及一个 `--user` 与 `PUID/PGID` 的兼容性分岔：**S12 是 LinuxServer.io 这个镜像维护方的口径**（不是 Docker 官方文档），它明说其镜像**尚不兼容 `--user`**、建议继续用 PUID/PGID；而 OpenList 官方镜像（S01）反过来推荐 `user:`。判断依据只有一条：**看镜像由谁维护**。属主与权限的完整规则见 6.6 第 3 行。

> [!warning] 待核实（Q3）
> **rootful Docker 下 `--user 0:0` 的确切含义是什么？** S01 只在 **rootless** 语境下解释过 `--user 0:0`，**rootful 场景官方未说明**，也未说明它与镜像内 `openlist(1001)` 的优先级。这是一个**未证实**项，不要把它写成结论。

> [!tip] 大白话
> 把运行身份想成"以谁的名义进门"：`--user 1000:1000` 是**直接报身份证号**，保安照号放行；`PUID`/`PGID` 是**发一张临时工牌**，镜像的启动脚本先把工牌号改成你给的两个数字，进程再拿着改过号的工牌去访问文件。两者目的相同（都让容器里的进程和宿主机上某个用户对上号），**但机制不同，所以不能互相替换**。

---

## 6.3 第 2 章段：存储挂不进来

| 症状 | 原因 | 动作 | 来源 |
| --- | --- | --- | --- |
| 保存存储时报 `Key: 'Storage.MountPath' Error: Field validation for 'MountPath' failed on the 'required' tag` | `Mount Path` 是必填项，被留空了 | 想挂到根目录就填 `/` | S17「Mount Path」 |
| 保存存储时报 `Failed to create storage in database: UNIQUE constraint failed: x_storages.mount_path` | `Mount Path` **重名**——它同时是挂载项的唯一标识、对外展示名和挂载位置，不允许重复 | 用 alias（别名）驱动**聚合多个挂载项**，而不是让它们同名 | S17「Mount Path」 |
| 想让两个网盘**共用一个 Token**，写了 `ref:` 却不生效 | `ref:/mount_path` 只支持**限定的驱动**：中国移动云盘、阿里云盘 Open、天翼云盘客户端、123 云盘分享（引用 123 云盘）、Cloudreve V3/V4 | 把 `备注(Remark)` 的**第一行**写成 `ref:/挂载路径`；注意 `ref:/` **必须小写英文和符号** | S17「挂载引用 ref」 |
| 改了 `Web proxy` 却对 WebDAV 客户端毫无影响（或反之） | `Web proxy` 与 `Webdav policy` **是两套不同配置**：前者管**网页**访问时走不走代理，后者管**WebDAV**功能走什么策略 | 要改 WebDAV 的传输策略，改的是 `Webdav policy`。默认走本地代理；有 302 选项时默认 302；想用代理 URL 必须**手动切换**到代理 URL 策略 | S17「代理策略 / Webdav policy」 |
| 以为删掉的文件还能从回收站找回 | 本地存储的回收站为空时，**删除即永久删除** | 删除前确认回收站是否有内容 | S16「本地存储」 |

> [!tip] 大白话
> `Mount Path` 想成**书架上的标签**：它既是这本书的编号（唯一标识），又是你看到的名字（展示名），还是它插在哪一格（挂载位置）。所以**空标签不行**（不知道往哪插），**两张一样的标签也不行**（分不清哪本是哪本）——官方为此分别给了上面两条报错原文。

---

## 6.4 第 3 章段：WebDAV 连不上，或连上了不能写

| 症状 | 原因 | 动作 | 来源 |
| --- | --- | --- | --- |
| WebDAV 客户端返回 **401 / 403** | 权限项没开齐，这是最常见的一类。**只开 `WebDAV 管理` 还不够！** 还必须同时开启计划执行操作所需的**具体文件系统权限**（`重命名` / `删除` / `复制` / `创建目录或上传` 等） | 在 `用户 => 权限` 里核对：只想读/播放，开 `WebDAV 读取` 即可；要写，则 `WebDAV 管理` **加**对应具体权限一并开 | S02「权限」；S03「权限项」 |
| 客户端连不上、连接被拒 | **端口与网页端不一致**。官方：`The port must be identical to the one used for accessing the OpenList web interface` | 第 1 章监听的是 `5244`，WebDAV 就填 `5244`，不要改成 80/443 | S02「基础连接配置」 |
| 明文凭证在公网传输，有安全顾虑 | 官方**强烈建议使用 https** | 客户端 `Protocol` 用 `https` | S02「基础连接配置」 |
| 想在复制文件时顺手重命名，但操作失败 | 该功能**官方明确不支持**：`Renaming during copy is not currently supported.` / `暂不支持复制时重命名。` | 拆成两步：先复制，再单独重命名（前提是已开 `复制` 与 `重命名` 两项权限） | S02「已知限制」 |
| 用**游客（guest）**登录，密码怎么填都不对 | 密码对游客无效；游客默认关闭 | 用正常用户登录；需要给游客开权限时，先确认是否真的要让游客可访问 | S03「登录密码」 |

> [!note] 上游旁证（不是 OpenList 官方结论）
> AList 上游文档（⚠️ **上游 AList 口径，2022-09-07 发布、未标注更新日期**）说的是同一件事，可作旁证：`≥ v3.42.0` 起，写入 WebDAV 不仅需要 `Webdav Manage`，还需要 `rename`、`delete`、`copy` 等基础权限[^c6-s04]。它与 OpenList 现行文档（S02）口径一致，但**不能当 OpenList 的官方结论引用**。

> [!tip] 大白话
> `WebDAV 读取` 是**进馆阅览证**，`WebDAV 管理` 是**可以动手改东西的许可**。但光有后者不够——你得一项一项说清楚要动哪类东西：改名有改名的许可，删除有删除的许可，上传有上传的许可。**401/403 十有八九是某一项许可没批。**

---

## 6.5 第 4 章段：mount 不成功、不生效、不刷新

| 症状 | 原因 | 动作 | 来源 |
| --- | --- | --- | --- |
| `rclone mount` 直接失败 | 挂载点不合规。官方要求挂载点是**已存在的空目录** | `mkdir` 一个空目录再挂；非空目录默认拒绝，需要时用 `--allow-non-empty`（官方注明"不支持 Windows"） | S06「Mounting on Linux / Options」 |
| 加了 `--allow-other`，但其他用户仍访问不了挂载点 | FUSE 默认**只允许 root** 使用 `allow_other`，该限制需要一个**用户态配置项**来解除（S09 官方口径，S09 **全文没有出现 `/etc/fuse.conf` 这个路径**） | 解除限制的具体位置来自社区经验：`sudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf`，用 `grep user_allow_other /etc/fuse.conf` 复核（应输出 `user_allow_other`） | S09（官方：默认仅 root）；S10（**社区经验**：`/etc/fuse.conf` 的位置） |
| systemd 托管时，报错说找不到 `fusermount` / `fusermount3` | systemd 的 mount unit **不携带任何环境变量，包括 `PATH` 和 `HOME`**；因此 `~` 不展开，rclone 只能回退到 `/bin:/usr/bin` 找 `fusermount` | 把 `--config`、`--cache-dir` 写成**显式绝对路径**，不要用 `~`；确认 `fusermount`/`fusermount3` 确实位于 `/bin` 或 `/usr/bin` | S06「systemd」 |
| 挂载报 `fusermount: exit status 1`，权限被拒 | 新版 Ubuntu 的 **AppArmor** 限制。官方给出的报错原文：`NOTICE: mount helper error: fusermount3: mount failed: Permission denied CRITICAL: Fatal error: failed to mount FUSE fs: fusermount: exit status 1` | 官方给的解法是 `sudo aa-disable /usr/bin/fusermount3`（可能需先 `sudo apt install apparmor-utils`） | S06「Mounting on Linux」 |
| 应用写文件失败，或**读的时候不能 seek** | 没设 `--vfs-cache-mode`。官方：不启用它时只能**顺序写**、读时才能 seek，"很多应用"因此无法工作 | 视需要加 `--vfs-cache-mode writes` 或 `--vfs-cache-mode full` | S06「Limitations」 |
| 用了 `full` 模式，性能却极差、日志刷 ERROR | 缓存目录所在的文件系统**不支持稀疏文件**，官方特别点名 **FAT/exFAT** | 把缓存目录（`--cache-dir`）放到支持稀疏文件的文件系统上 | S06「VFS File Caching」 |
| 网盘里新增/删除的文件，挂载点不刷新 | 目录缓存未过期。`--dir-cache-time` 默认 `5m0s`；`--poll-interval` 默认 `1m0s`，官方要求它**必须小于** `dir-cache-time` | 缩短 `--dir-cache-time`，或手动刷：`kill -SIGHUP $(pidof rclone)`（官方：刷新全部目录缓存，不论新旧）；配了 remote control 还可用 `rclone rc vfs/forget` | S06「VFS Directory Cache」 |
| 看到的大小 / 修改时间不对 | 属性缓存 `--attr-timeout` 默认 `1s`；多个 rclone 实例同时挂同一远端会加大损坏概率 | 按需调 `--attr-timeout`；确需多实例时用独立的 `--cache-dir` | S06「Attribute caching」 |
| **中文文件名出现乱码** | **全部来源未覆盖** | **待补收集**——本节不给解释、不给命令，请另找来源 | （无来源） |

> [!tip] 大白话
> `--vfs-cache-mode` 想成**暂存筐**：关掉它的时候，rclone 只能把文件当作**一条流水**顺序读写，不能"倒回去"（seek）；启用 `writes` 或 `full` 等于给 rclone 一个可以反复翻的暂存筐，应用才能像操作本地文件那样改来改去。筐放在哪也有讲究——**架在 FAT/exFAT 这种不能"留白"（稀疏文件）的地面上，筐就变笨。**

> [!tip] 大白话
> `--dir-cache-time` 是**"目录清单多久重抄一遍"**，`--poll-interval` 是**"多久去远端问一次有没有变动"**，两者都必须能被"提前打断"——这就是 `kill -SIGHUP $(pidof rclone)`（等于喊一声"清单作废，重抄"）存在的原因。

---

## 6.6 第 5 章段：映射给容器之后

| 症状 | 原因 | 动作 | 来源 |
| --- | --- | --- | --- |
| 用 `-v <宿主机文件>:<容器内路径>` 挂配置文件，容器里读到的却是**空目录** | `-v` 对宿主机上**不存在**的路径会**自动创建**，而且**始终创建为目录**——你想要的是文件，它给你建了个同名空目录 | 改用 `--mount`：源路径不存在时它**当场报错**（官方错误原文 `docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: ...`），能立刻暴露问题；确需自动创建再用 `bind-create-src` | S11 |
| 挂进去之后，容器里原本该有的文件"不见了" | bind mount 挂进**非空目录**会**遮蔽**原有内容，且**没有简单办法恢复** | 挑一个容器里本来就空的路径（如 `/media/openlist`）。改尺寸不如改位置：一旦被遮蔽，只能**去掉挂载、重建容器** | S11 |
| 容器内进程**只读 / 无权限**，写不进去挂载点 | **属主与权限不匹配**。但这里有一条硬边界：**Docker 官方没有定义 bind mount 的属主/权限规则**（缺口 G5） | 见下方「待核实」块 | S11/S18 无此内容；S12（**镜像维护方口径**）；S06 |
| 起了容器才发现挂载点是空的 | **启动顺序错了**。bind mount 只把宿主机上**已有**的目录搬进容器，它不会替你挂 rclone | 硬顺序：先跑第 4 章 `rclone mount`、确认能 `ls` 出内容，**再** `docker compose up -d` | S11（容器与宿主机强绑定）；第 5 章 §5.7 |
| 容器内看不到宿主机上挂载点里**嵌套**的子挂载 | 传播默认为 **`rprivate`**——双向都不传 | 需要容器内可见子挂载时，用 `rslave`（`-v ...:ro,rslave` 或 `--mount ...,bind-propagation=rslave`）。注意：**只在 Linux 宿主机可配，Docker Desktop 下不工作** | S11 |
| 宿主机开了 SELinux，容器读不到挂载文件 | 需要给 bind mount 打标签 `z`（多容器共享）或 `Z`（私有） | 注意两条：该标签改的是**宿主机文件本身**；且 **`--mount` 无法修改 SELinux 标签**，要用 `z`/`Z` 只能用 `-v <宿主机路径>:<容器内路径>:z` | S11 |

> [!warning] 待核实（Q4 / G5）：挂载点能不能写，没有官方一句话
> **S11 与 S18 两篇 Docker 官方文档都没有讨论 bind mount 的 uid/gid 属主规则**（缺口 G5）。因此"容器能不能写挂载点"**不能引用任何 Docker 官方规则**，只能用两侧来源推断：
> - **镜像侧**（S12，**镜像维护方口径，非 Docker 官方**）：容器默认在 root 用户域下运行，容器内创建的文件归 root 所有，需要 PUID/PGID 之类的机制把内部用户映射到宿主机用户；
> - **宿主机侧**（S06，rclone 官方）：`--uid`/`--gid` 默认都是 `1000`，`--umask` 默认 `002`，"不支持 Windows"。
>
> 实操请**两边对照**：宿主机上 `ls -ln /mnt/openlist` 看实际数字属主，容器内 `id` 看进程实际 uid/gid。二者匹配才可能写成功。

> [!tip] 大白话
> bind mount 的权限像**合租房**：房东（宿主机）把房间钥匙（目录）交给租客（容器），但钥匙上写的名字（uid/gid）如果不属于租客，租客照样进不去。**问题不在"有没有给房间"，而在"钥匙上的名字对不对"**——而"房间归谁"这件事，Docker 官方没规定，得你两边各看一次。

---

## 6.7 抓取缺陷「不能照抄」清单

下面这些片段在抓取时**结构被破坏**（§4.4）。本章与前面各章凡涉及它们的**都做了重写**，你在别处看到"原文如此"之外的形态时，请以来源的官方语义为准。

| 源 | 缺陷 | 处理 |
| --- | --- | --- |
| S01 | compose 段 YAML 列表项 `- ` 引导符与缩进被剥离，volumes/ports 行顶格（形如 `'./data:/opt/openlist/data'`） | **不能直接照抄该 YAML**；本章涉及处一律以抓取完整的 `docker run` 一行命令为准 |
| S11 | compose 示例整段丢失换行与缩进（仅键名 `type: bind` / `source: ./static` / `target: /opt/app/static` 可用）；`--volume` 选项表中 SELinux 那行的选项名丢失 | compose 片段**按官方字段重写**，不声称逐字引用 |
| S12 | 正文空格被去掉（如 `dockercreate--name=beets-ePUID=1000-ePGID=1000linuxserver/beets`） | 该文件里的命令串**不可直接复制**，涉及处按语义重写 |
| S18 | compose 示例被抓取时压成一行 | 同上，按官方字段重写 |
| S15 | 驱动索引页是**空壳**，只有导航，无任何正文 | **不引用该来源**；需要官方驱动全清单时另找站点 `sitemap.xml` |

---

## 6.8 未决清单（Q1–Q7 / G1–G7）

以下条目在来源补齐前**只能写"未证实"**，不得给出结论。这是本章的收口：它是"还没有答案"的清单，本身也是交付物的一部分。

**开放问题（Q）**

| ID | 问题 | 现状 |
| --- | --- | --- |
| Q1 | OpenList 是否存在**全局**「开启 WebDAV」开关？ | 倾向"没有"（S02 只讲用户权限项；S17 的 `Webdav policy` 是**每存储**设置），但**未证实** |
| Q2 | `/dav/<挂载路径>` 的路径结构是否为官方定义？ | `/dav/` 来自 S02，`Mount Path` 是 S17 的存储位置字段，两者拼接**属于推断**，未经官方证实 |
| Q3 | rootful Docker 下 `--user 0:0` 的确切含义？与镜像内 `openlist(1001)` 的优先级？ | S01 只在 **rootless** 语境解释过，**rootful 未说明** |
| Q4 | bind mount 的属主 / 权限官方行为 | **无官方来源**（同 G5）。实操中最易踩的坑，却缺一手依据 |
| Q5 | 终点容器是哪个？ | **未定**（同 G2）。本章因此只给通用模式，不绑定具体镜像 |
| Q6 | `Mount Path` 是否可嵌套（如 `/A/B`）？是否影响 WebDAV 路径？ | S17 **未说明** |
| Q7 | v4.1.0 的确切发布日期与变更单 | S01 **未给** |

**覆盖缺口（G）**

| ID | 缺口 | 本章/正文的影响 |
| --- | --- | --- |
| G1 | 没有官方来源把 OpenList + WebDAV + rclone + 终点容器串进**完整 compose** | 端到端片段只能是**拼装**，且须逐段标注官方字段 vs 编排 |
| G2 | **终点容器未定**（qBittorrent？Jellyfin？） | 消费者侧只写通用 `:ro` / 读写模式 |
| G3 | 官方**无 systemd 页面**，开机自启只有社区来源 | systemd 结论标**社区经验**；仅 `Type=notify`、PATH 回退有 S06 官方支撑 |
| G4 | 全文**未覆盖 Windows / WSL** | 见 6.1，本章表头显式声明"仅适用 Linux 宿主机" |
| G5 | bind mount / volume 的**属主与权限行为无官方来源** | 见 6.6「待核实」；**不得声称 Docker 官方定义了 bind mount 属主规则** |
| G6 | OpenList 驱动索引页**无正文**（S15 为空壳） | 需列驱动时注明来源为站点 `sitemap.xml`；本笔记不引用 S15 |
| G7 | S04 为 **2022-09-07 发布的上游 AList 口径**，未标注更新日期 | 引用能力矩阵时必须标明口径与日期 |

---

## 6.9 本章来源与层级标注

本章全部条目均回源核对后写成，引用来源如下；标注了口径层级的来源，请连同层级一起理解：

S01[^c6-s01]、S02[^c6-s02]、S03[^c6-s03]、S04[^c6-s04]、S06[^c6-s06]、S09[^c6-s09]、S10[^c6-s10]、S11[^c6-s11]、S12[^c6-s12]、S16[^c6-s16]、S17[^c6-s17]、S18[^c6-s18]。

其中三处层级必须记住：**S04 = 上游 AList 口径（2022-09-07）**，只能作旁证；**S10 = 社区经验**（`/etc/fuse.conf` 的位置出自它）；**S12 = 镜像维护方口径**（LinuxServer.io 自家约定，**不是 Docker 官方文档**）。此外 S15 为空壳页、S05/S08/S13/S14 无文件，本章一律不引用。

---

## 本章小结

- **本章只适用 Linux 宿主机**：Windows/WSL 是缺口 G4，全表不给结论；中文文件名编码是**待补收集**，来源未覆盖，不编造。
- **按段查表**：6.2 容器/数据/运行身份与密码（S01/S03）；6.3 存储挂载（S17/S16）；6.4 WebDAV 权限与端口（S02/S03，S04 上游旁证）；6.5 rclone 挂载、systemd、FUSE、缓存（S06/S09/S10）；6.6 映射给容器（S11/S12/S06）。**每条都指回具体源文件与段落**，便于回原文核对。
- **两个必须标层级的来源**：`/etc/fuse.conf` 的具体位置是**社区经验**（S10），FUSE"默认仅 root 使用 `allow_other`"才是官方口径（S09）；S04 是**上游 AList 口径（2022-09-07）**，只能当旁证。
- **三个"未证实"高发点**：Q3（rootful 下 `--user 0:0`）、Q4/G5（bind mount 属主与权限**无官方来源**）、Q2（`/dav/<路径>` 结构是推断）。属主问题一律用 `ls -ln`（宿主机）+ `id`（容器内）两边对照，不给结论。
- **抓取缺陷"不能照抄"**：S01 compose、S11 compose、S12 命令串、S18 compose 均被破坏，正文章节已重写；S15 是空壳页，不引用。
- **未决清单**（Q1–Q7 / G1–G7）是本章交付物的一部分：它明确告诉你哪些条目在来源补齐前只能写"未证实"。

---

## 相关笔记

- [[docker容器搭建错误的知识讲解]] —— Docker 侧常见错误的系统梳理
- [[docker镜像拉取DNS解析超时排错]] —— 第 1 册段「拉不到镜像」的深入排查
- [[Docker容器服务访问宿主机文件]] —— 第 5 册段权限问题的展开

[^c6-s01]: OpenList Docs — 使用 Docker 安装（T1，OpenList 官方口径），本地文件 `sources/S01_openlist_docker_install.md`。该文件 compose 段 YAML 缩进被抓取破坏（§4.4）。
[^c6-s02]: OpenList Docs — WebDAV（T1，OpenList 官方口径），本地文件 `sources/S02_openlist_webdav.md`。
[^c6-s03]: OpenList Docs — User / 用户与权限（T1，OpenList 官方口径），本地文件 `sources/S03_openlist_user_permission.md`。
[^c6-s04]: AList Docs — WebDav（**上游 AList 口径**，页面标注 2022-09-07 发布且未标注更新日期），本地文件 `sources/S04_alist_webdav_upstream.md`。
[^c6-s06]: rclone — mount 命令文档（T1，rclone 官方口径），本地文件 `sources/S06_rclone_mount.md`。
[^c6-s09]: FUSE 内核文档（T1，内核/FUSE 官方口径），本地文件 `sources/S09_fuse_kernel_doc.md`。该文只说存在"a (userspace) configuration option"，**未出现 `/etc/fuse.conf` 路径**。
[^c6-s10]: rclone 社区 systemd 帖（**社区经验，非官方**），本地文件 `sources/S10_rclone_systemd_forum.md`。`/etc/fuse.conf` + `user_allow_other` 的具体位置出自该帖。
[^c6-s11]: Docker Docs — Bind mounts（T1，Docker 官方），本地文件 `sources/S11_docker_bind_mounts.md`。该页 compose 示例抓取时丢失换行与缩进（§4.4），相关片段为**按官方字段重写**。
[^c6-s12]: LinuxServer.io — Understanding PUID and PGID（**镜像维护方口径，非 Docker 官方文档**），本地文件 `sources/S12_linuxserver_puid_pgid.md`。该文件正文空格被去掉，其命令串**不可直接复制**。
[^c6-s16]: OpenList Docs — Local 驱动（T1，OpenList 官方口径），本地文件 `sources/S16_openlist_driver_local.md`。
[^c6-s17]: OpenList Docs — Common 驱动设置（T1，OpenList 官方口径），本地文件 `sources/S17_openlist_driver_common.md`。
[^c6-s18]: Docker Docs — Volumes（T1，Docker 官方），本地文件 `sources/S18_docker_volumes.md`。该页 compose 示例抓取时压成一行。

---

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-05-Docker映射]] ｜ 目录：[[OpenList网盘挂载-00-总目录]]
