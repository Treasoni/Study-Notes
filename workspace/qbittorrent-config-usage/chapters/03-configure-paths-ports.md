## 第 3 章 配好（上）：端口、下载目录与硬链接口径

上一章把容器装起来了，但那只是「容器能跑」。「配好」才是让 qBittorrent 和你家庭影院里其它部件接上：文件从哪下、下到哪、谁来看，以及别人能不能主动连上你。这一章把「配好」拆成最小的一组动作——**四条路径 + 一个端口**，最后讲透「硬链接口径」，因为它是很多人「下完了却整理不动」的真正根因。

### 3.1 结论先行：配好 = 四条路径 + 一个端口

先把要动的东西一次列清：

| 要配的 | 在哪配 | 为什么 |
| --- | --- | --- |
| 路径① 默认保存位置 | qBittorrent `Options` → `Downloads` → `Hard Disk` → `Save files to location` | 决定下载文件落在容器里的哪个目录（3.3） |
| 路径② 容器的 `/downloads` 卷 | `docker-compose.yml` 的 `volumes:` | 把容器内目录接到硬盘上的真实宿主目录（第 2 章已配） |
| 路径③ MoviePilot 的下载目录 | MoviePilot `设定` → 下载目录 | 让整理端知道去哪儿取文件 |
| 路径④ MoviePilot 容器的目录映射 | MoviePilot 的 compose | 让两边「看到同一份文件」，硬链接才成立（3.4） |
| 端口 BT 端口（默认 `6881`） | compose 的 `ports:` 与环境变量 | 让别的下载者能主动连上你（3.2） |

> [!tip] 大白话
> 把宿主目录想成**同一间仓库**：qBittorrent 放货、MoviePilot 取货，四条路径就是让两人**认同一间仓库、同一个货位**；认的仓库不同，MoviePilot 就得把货搬（复制）一遍，多花一倍空间。

### 3.2 端口：BT 端口必须映射，改端口要「两侧同改」

容器内的端口和宿主机端口是两回事；`ports:` 负责「把宿主端口转到容器端口」。BT 端口（默认 `6881`[^c3-la1-60]）要映射出去，才能成为「主动节点」：

| 官方原文 | 说人话 |
| --- | --- |
| 「A bittorrent client can be an active or a passive node.」[^c3-la2-31] | BT 客户端可以是主动节点，也可以是被动节点；当主动节点能连上更多同伴、带来更多入站连接。 |
| 「This requires an open port on the host machine which might differ from container's internal one.」[^c3-la2-31] | 这要求宿主机上有一个对外开放的端口，而它**可能和容器内部端口不是同一个**。 |

关键在最后一句的「可能不是同一个」：改端口时**两边都要改**——LinuxServer 文档把这条写得很死：

| 官方原文 | 说人话 |
| --- | --- |
| 「Due to issues with CSRF and port mapping, should you require to alter the port for the web UI you need to change both sides of the -p 8080 switch AND set the WEBUI_PORT variable to the new port.」[^c3-la2-28] | 因为 CSRF 与端口映射的坑，你要改 WebUI 端口时，必须**同时改 `-p 8080` 这个映射的两侧**，并把 `WEBUI_PORT` 变量也设成新端口。 |

> [!warning] 「两侧同改」只改一边会怎样
> 只改 `ports:` 不改环境变量（或反过来），映射端口和服务真正监听的端口就对不上——改了端口却怎么也连不上。

> [!tip] 大白话
> 把端口想成**快递柜格口号**：映射（`ports:`）是门牌，环境变量告诉服务「住哪个格口」；两边数字一致，快递才找得到。

「防火墙 / NAT 下要转发端口」这条，本册只有 Deluge 的 ArchWiki 页可借其连通性原理[^c3-lc3-77][^c3-lc3-79]——**该页非 qB 来源**，端口号不作 qB 默认值，只借原理（F10）。

### 3.3 下载目录：四项路径设置都在「Downloads → Hard Disk」

qBittorrent 的设置按「标签页」组织，官方只维护**一张**合并说明页[^c3-lb1-11]——不存在 Connection / Downloads / BitTorrent 各自独立的官方页。与路径有关的四项都集中在 `Downloads` → `Hard Disk`：

| 设置项 | 管什么 | 一般要不要动 |
| --- | --- | --- |
| `Save files to location`[^c3-lb1-67] | 默认保存位置：下载中和完成后的文件都落这里 | 要，指向你的下载目录 |
| `Keep incomplete torrents in`[^c3-lb1-70] | 未完成文件的临时目录 | 可选；要和保存位置在**同一文件系统**内 |
| `Copy .torrent files to`[^c3-lb1-73] | 把每个种子文件另存一份 | 可选 |
| `Copy .torrent files for finished downloads to`[^c3-lb1-74] | 只对完成的种子另存种子文件 | 可选 |

**这里只讲「在哪改」，不讲「默认值是多少」**：该默认值本册没有一手来源，与其写个可能对不上的数，不如打开标签页看你自己的当前值。真正要改的是第一项 `Save files to location`——指到你已映射进容器的下载目录。

> [!tip] 大白话
> `Save files to location` 就是**收货地址**：地址写错，包裹送到别处，MoviePilot 按原地址取就扑空。临时目录（`Keep incomplete torrents in`）像**中转站**——不和收货地址同在一个院子（同一文件系统），货到了还得再搬一趟。

### 3.4 硬链接为什么对：同一文件系统 + 同一映射路径 + 权限（F8）

先纠一个误会：**qBittorrent 本身没有「硬链接」设置项**（F8）。硬链接是整理侧——MoviePilot「整理模式」的一个选项[^c3-lb3-102]——干的事，qB 只负责把文件下到目录。

三个名词先扫盲：

| 名词 | 一句话解释 | 出处 |
| --- | --- | --- |
| 硬链接 | 同一份文件起多个「名字」，不额外占空间；删掉一个名字，文件仍在其它名字下 | LB-5[^c3-lb5-36] |
| 软链接 | 像快捷方式，指向原文件的路径；原文件一删，快捷方式就失效 | LB-3[^c3-lb3-105] |
| 文件系统 | 一块存储上组织文件的方式（如 ext4、NTFS、exFAT）；硬链接**不能跨文件系统** | LB-5[^c3-lb5-30] |

硬链接**不能跨文件系统**：它本质是**给同一块数据再挂一个名字**，而「名字 → 数据」只在一块文件系统内成立[^c3-lb5-39]——所以它不能跨文件系统 / 分区 / 卷，也不能给目录做，exFAT 更不支持[^c3-lb5-30]。

落到部署上，这条推出**本章最重要的一句**：**qBittorrent 的下载目录，必须和 MoviePilot 的媒体目录映射到宿主机上的同一份路径**。MoviePilot 同样要求下载目录「需要与下载器使用的目录一致」，docker 靠映射路径让两边一致[^c3-lb4-15]；其「整理模式」也要求硬链接在「同一磁盘 / 存储空间 / 映射路径下」才成立[^c3-lb3-104]。

一句话：**两边认同一宿主目录 = 同一文件系统 = 能硬链接 = 不必复制**；否则只能退回「复制」，空间翻倍。权限交给下一节的 `UMASK`。

> [!tip] 大白话
> 硬链接像**给同一个抽屉贴第二张标签**：不是新买柜子，而是再挂一个名字；标签只能贴在**同一个档案柜**里（同一文件系统），跨楼就贴不上。

### 3.5 动手实践（新手可跳过）

> [!tip] 新手可跳过
> 这一节是可直接照改的片段；不手动改配置的读者可跳过。

**改端口：两侧同改。**把 WebUI 端口改到 `8123`[^c3-la2-29]：

```yaml
# docker-compose.yml（片段）
    ports:
      - 8123:8123        # 左边=宿主端口，右边=容器端口，两个写一样
    environment:
      - WEBUI_PORT=8123  # 与上面 ports 右侧保持一致的容器端口
```

BT 端口同理，而且 tcp / udp 都要映射[^c3-la2-32]：

```yaml
# docker-compose.yml（片段）
    ports:
      - 6887:6887
      - 6887:6887/udp
    environment:
      - TORRENTING_PORT=6887
```

**查属主 / 属组**：`PUID` / `PGID` 默认都是 `1000`[^c3-la2-97]，要确认你自己的，就跑[^c3-la2-128]：

```shell
id your_user
```

**UMASK 组合表**：UMASK 决定新建文件 / 目录的默认权限，语义是「减」不是「加」——`umask` 从权限里**减掉**权限位[^c3-la2-124]。按你的用户方案二选一[^c3-lb5-79][^c3-lb5-80]：

| 方案 | 用户 | `UMASK` | 结果权限 |
| --- | --- | --- | --- |
| 每应用独立用户 + 共享组（推荐） | 每个应用一个用户，同在一个共享组 | `002` | 目录 `775`、文件 `664` |
| 单一共享用户（简单些） | 所有应用共用一个用户 | `022` | 目录 `755`、文件 `644` |

> [!warning] 不要用 `UMASK 000`
> `000` 会让新建的目录变成 `777`、文件变成 `666`，也就是**所有人可读可写**，属于糟糕的 Linux 习惯[^c3-lb5-86]。共享目录请用上表的 `002` 或 `022`。

### 本章小结

- 配好 = **四条路径 + 一个端口**：默认保存位置、容器 `/downloads` 卷、MoviePilot 下载目录、MoviePilot 容器映射，加一个 BT 端口。
- BT 端口要映射才能当「主动节点」被连上；改端口必须**两侧同改**（`ports:` 与环境变量）[^c3-la2-28]。
- 路径四项都在 `Downloads` → `Hard Disk`（F5）；本册只写「在哪改」，不写默认值。
- 硬链接不是 qB 的功能，是 MoviePilot「整理模式」的选项（F8）；它要求**同一文件系统 + 同一映射路径 + 权限**——下载目录必须和媒体端映射**同一宿主目录**。
- 权限用 `UMASK 002`（推荐）或 `022`，**绝不用 `000`**。

### 下一章预告

端口和路径立好，第 4 章让下载「自动收尾」：分类与标签、限速、代理，以及最关键的一环——**完成回调**，你会看到 MoviePilot 为什么能「一下完就自动整理」。

## 引文对照（原文 / 中译 / 出处）

本章正文里出现过的英文引文，逐字原文与中译对照如下。出处一律写作「来源 ID · sources/文件:行号」；本章每条引文都能定位到 `sources/` 下的原始快照，故没有出现 `—`（`—` 的约定含义是「查不到出处」，此时宁可空着也不猜）。

| # | 原文（逐字） | 中译 | 出处 |
| --- | --- | --- | --- |
| 1 | `A bittorrent client can be an active or a passive node.` | BT 客户端可以是主动节点，也可以是被动节点。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:31` |
| 2 | `This requires an open port on the host machine which might differ from container's internal one.` | 这要求宿主机上有一个对外开放的端口，而它可能和容器内部端口不是同一个。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:31` |
| 3 | `Due to issues with CSRF and port mapping, should you require to alter the port for the web UI you need to change both sides of the -p 8080 switch AND set the WEBUI_PORT variable to the new port.` | 因为 CSRF 与端口映射的坑，你要改 WebUI 端口时，必须同时改 `-p 8080` 映射的两侧，并把 `WEBUI_PORT` 变量也设成新端口。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:28` |
| 4 | `For example, to set the port to 8123 you need to set -p 8123:8123 and -e WEBUI_PORT=8123` | 例如要把端口设成 8123，你需要设 `-p 8123:8123` 和 `-e WEBUI_PORT=8123`。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:29` |
| 5 | `Similarly to the WEBUI_PORT, to set the port to 6887 you need to pass -p 6887:6887, -p 6887:6887/udp and -e TORRENTING_PORT=6887 arguments to Docker.` | 与 `WEBUI_PORT` 类似，要把端口设成 6887，你需要给 Docker 传 `-p 6887:6887`、`-p 6887:6887/udp` 和 `-e TORRENTING_PORT=6887` 这几个参数。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:32` |
| 6 | `Having a file in multiple locations without using double your storage space.` | 让一份文件出现在多个位置，却不占用双份存储空间。 | `LB-5 · sources/l2-5_trash-hardlinks.md:36` |
| 7 | `Keep in mind umask is not chmod it subtracts from permissions based on it's value it does not add.` | 请记住 umask 不是 chmod：它按自身取值从权限里做减法，而不是加法。 | `LA-2 · sources/l1-2_linuxserver-qbittorrent.md:124` |

## 脚注

[^c3-la1-60]: LA-1 · `sources/l1-1_official-docker-readme.md:58-60`（`QBT_TORRENTING_PORT`，未设时默认 `6881`）。
[^c3-la2-28]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:28`（`WEBUI_PORT` 一节：WebUI 端口两侧同改）。
[^c3-la2-29]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:29`（示例：`-p 8123:8123` 与 `-e WEBUI_PORT=8123`）。
[^c3-la2-31]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:31-32`（`TORRENTING_PORT` 一节：主动 / 被动节点与宿主机开放端口）。
[^c3-la2-32]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:32`（示例：`-p 6887:6887`、`-p 6887:6887/udp`、`-e TORRENTING_PORT=6887`）。
[^c3-la2-97]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:97`（`PUID=1000` 参数表）。
[^c3-la2-124]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:124`（umask 语义说明）。
[^c3-la2-128]: LA-2 · `sources/l1-2_linuxserver-qbittorrent.md:128`（用 `id your_user` 查 PUID/PGID）。
[^c3-lb1-11]: LB-1 · `sources/l2-1_options-explained.md:11`（设置按标签页分组，官方只有一张合并说明页）。
[^c3-lb1-67]: LB-1 · `sources/l2-1_options-explained.md:66-67`（`Downloads` → `Hard Disk` → `Save files to location`）。
[^c3-lb1-70]: LB-1 · `sources/l2-1_options-explained.md:70`（`Keep incomplete torrents in`）。
[^c3-lb1-73]: LB-1 · `sources/l2-1_options-explained.md:73`（`Copy .torrent files to`）。
[^c3-lb1-74]: LB-1 · `sources/l2-1_options-explained.md:74`（`Copy .torrent files for finished downloads to`）。
[^c3-lb3-102]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:102`（整理模式位置）。
[^c3-lb3-104]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:104`（硬链接：要求同一磁盘 / 存储空间 / 映射路径）。
[^c3-lb3-105]: LB-3 · `sources/l2-3_moviepilot-reorganize.md:105`（软链接说明）。
[^c3-lb4-15]: LB-4 · `sources/l2-4_moviepilot-download.md:15`（下载目录需与下载器使用的目录一致）。
[^c3-lb5-30]: LB-5 · `sources/l2-5_trash-hardlinks.md:30`（硬链接限制：不能对目录、不能跨文件系统、exFAT 不支持）。
[^c3-lb5-36]: LB-5 · `sources/l2-5_trash-hardlinks.md:36`（「硬链接是什么」一节的短答）。
[^c3-lb5-39]: LB-5 · `sources/l2-5_trash-hardlinks.md:39`（硬链接受限于同一文件系统）。
[^c3-lb5-79]: LB-5 · `sources/l2-5_trash-hardlinks.md:79`（`UMASK 002` → 目录 `775`、文件 `664`）。
[^c3-lb5-80]: LB-5 · `sources/l2-5_trash-hardlinks.md:80`（`UMASK 022` → 目录 `755`、文件 `644`）。
[^c3-lb5-86]: LB-5 · `sources/l2-5_trash-hardlinks.md:86`（不要用 `UMASK 000`）。
[^c3-lc3-77]: LC-3 · `sources/l3-3_archwiki-deluge.md:77`（UPnP 与本地防火墙的说明；**该页为 Deluge（非 qB）ArchWiki，仅借连通性原理，F10**）。
[^c3-lc3-79]: LC-3 · `sources/l3-3_archwiki-deluge.md:79`（连接跟踪 conntrack 说明；同上，非 qB 来源）。
