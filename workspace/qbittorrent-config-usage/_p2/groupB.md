## 组 B：配置

### LB-1 · Explanation of Options in qBittorrent（qBittorrent 官方 Wiki）

- 文件: `sources/l2-1_options-explained.md` ｜ tier: 官方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方明确说明选项是**按标签页（tab）分组**组织的，不是单页堆叠；选项入口是 `Alt` + `O` 或 Tools → Options。 ｜ `sources/l2-1_options-explained.md:11`
  - 标签页一级标题依次为 `Behavior`、`Downloads`、`Connection`、`Speed`、`BitTorrent`、`Web UI`、`Advanced`，另有 `Deprecated options` 小节。 ｜ `sources/l2-1_options-explained.md:35,59,91,110,115,127,129,193`
  - 下载位置相关的设置项集中在 `Downloads` 标签页的 `Hard Disk` 小节，第一个就是默认保存位置。 ｜ `sources/l2-1_options-explained.md:66,67`
  - 「保存到哪」不是一个单值，wiki 至少列出四项路径型设置：默认保存位置、未完成种子临时目录、.torrent 备份目录、已完成种子的 .torrent 备份目录。 ｜ `sources/l2-1_options-explained.md:67,70,73,74`
  - 「未完成文件加扩展名」是独立开关，作用是把 `Hello.mp3` 暂存为 `Hello.!qb`，下载完成后再改回原文件名。 ｜ `sources/l2-1_options-explained.md:71`
  - 完成回调在 wiki 里的标题是 `Run an external program on torrent completion`，位于 `Downloads` 标签页下。 ｜ `sources/l2-1_options-explained.md:89`
  - **该小节正文只有一句话**，未列出任何占位符、示例命令或脚本要求：全文即「This allows you to run a program on finishing certain types of torrents in a certain location.」。 ｜ `sources/l2-1_options-explained.md:90`
  - `Advanced` 标签页的 qBittorrent 专有项，wiki 直接指向源码文件 `src/gui/advancedsettings.cpp` 作为一手文档，等于承认 wiki 不是设置项的唯一权威。 ｜ `sources/l2-1_options-explained.md:130`
  - `Advanced` 中唯一与「路径数量」有关的默认值是保存路径历史长度。 ｜ `sources/l2-1_options-explained.md:145`
- 关键实体（端口/路径/默认值等，逐字）: `Save path history length — (default: 8)`；`Append .!qb extension`；`Hello.!qb`；`Alt` + `O`；`Tools` → `Options`；`src/gui/advancedsettings.cpp`；`include/libtorrent/settings_pack.hpp`

### LB-2 · External programs How-to（qBittorrent 官方 Wiki）

- 文件: `sources/l2-2_external-programs.md` ｜ tier: 官方 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 官方 how-to 确认**存在**「完成时运行外部程序」这一能力，并给出设置位置：`Options` > `Downloads`。 ｜ `sources/l2-2_external-programs.md:12`
  - 对 bash 脚本的唯一硬性提示是必须先赋予可执行权限。 ｜ `sources/l2-2_external-programs.md:14`
  - **该页实质内容仅上述两句**，没有占位符说明、没有参数表、没有示例；页面其余部分是 wiki 导航模板。 ｜ `sources/l2-2_external-programs.md:12,14`
  - 因此「qBittorrent 官方 wiki 给出完成回调占位符清单」这一说法在本页**不成立**；占位符只能从源码取证（见 LB-6）。 ｜ `sources/l2-2_external-programs.md:12`
- 关键实体（端口/路径/默认值等，逐字）: `Options` > `Downloads`；`chmod 755 /path/to/script`

### LB-3 · MoviePilot Wiki 文件整理

- 文件: `sources/l2-3_moviepilot-reorganize.md` ｜ tier: 官方（项目方 Wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - MoviePilot 官方给出 qBittorrent 完成回调的**现成填法**：在 QB 设置→「下载完成时运行外部程序」处填入一条 curl，实现下载完成立即整理、不必等轮询。 ｜ `sources/l2-3_moviepilot-reorganize.md:15`
  - 该 curl 指向本机 `localhost:3000` 的 `transfer/now` 接口并带 `token=moviepilot`，文档同时声明地址、端口和 token 需按实际调整，curl 也可换成 wget。 ｜ `sources/l2-3_moviepilot-reorganize.md:15`
  - 整理模式在 `设定 -> 目录 -> 整理模式` 中调整，共六种：硬链接、软链接、复制、移动、Rclone 复制、Rclone 移动。 ｜ `sources/l2-3_moviepilot-reorganize.md:102,104-109`
  - **硬链接的前置条件被明确写为「同一磁盘/存储空间/映射路径」**，并说明可改硬链接后的文件名而不影响原文件做种、但不能改文件内容。 ｜ `sources/l2-3_moviepilot-reorganize.md:104`
  - 软链接的前置条件更严：原文件路径必须与生成软链接时一致，docker 环境下即**映射前后的目录路径需要一致**。 ｜ `sources/l2-3_moviepilot-reorganize.md:105`
  - 覆盖策略是独立设置项（`设定 -> 目录 -> 整理模式`），四档：从不覆盖 / 按大小覆盖 / 总是覆盖 / 仅保留最新版本。 ｜ `sources/l2-3_moviepilot-reorganize.md:112,114,116-119`
  - V2 起内建目录监控，无需第三方插件；下载器监控的自动整理间隔为固定轮询值。 ｜ `sources/l2-3_moviepilot-reorganize.md:81,82`
  - V1 的下载器监控需要手动打开 `下载文件自动整理` 开关，且多下载器时默认只监控第 1 个。 ｜ `sources/l2-3_moviepilot-reorganize.md:88,90`
  - 若使用插件式目录监控（实时）而非内建下载器监控，必须打开 qBittorrent 的「为不完整文件添加扩展名」选项，避免下载未完成就被移走。 ｜ `sources/l2-3_moviepilot-reorganize.md:94`
- 关键实体（端口/路径/默认值等，逐字）: `curl "http://localhost:3000/api/v1/transfer/now?token=moviepilot"`；`localhost:3000`；`token=moviepilot`；`5分钟`；`/moviepilot/.config/rclone`；rclone 网盘配置名 `MP`；`AI_AGENT_ENABLE`

### LB-4 · MoviePilot Wiki 下载

- 文件: `sources/l2-4_moviepilot-download.md` ｜ tier: 官方（项目方 Wiki） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 下载目录在 `设定` 中添加；docker 部署时下载目录对应的**根目录必须映射进容器**，否则文件落在容器内导致容器异常。 ｜ `sources/l2-4_moviepilot-download.md:13`
  - 路径口径的核心一句：**下载目录需要与下载器使用的目录一致**，docker 下通过映射路径对齐。 ｜ `sources/l2-4_moviepilot-download.md:15`
  - 手动下载时无法指定下载目录，目录由系统识别资源后自动判定。 ｜ `sources/l2-4_moviepilot-download.md:21`
  - 音乐整理同样要求「下载器路径与 MoviePilot 的目录映射一致」，且 MoviePilot 不建库、不播放，整理后交给外部媒体服务器扫描。 ｜ `sources/l2-4_moviepilot-download.md:27`
- 关键实体（端口/路径/默认值等，逐字）: `设定 -> 目录`；`AUTO_DOWNLOAD_USER`（V1 变量）

### LB-5 · TRaSH-Guides 硬链接与即时移动（Hardlinks and Instant Moves）

- 文件: `sources/l2-5_trash-hardlinks.md` ｜ tier: 社区经验 ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 硬链接的三条硬性限制被单独放进 danger 块：不能对目录建硬链接、不能跨文件系统/分区/卷/挂载点建硬链接、exFAT 等文件系统不支持硬链接。 ｜ `sources/l2-5_trash-hardlinks.md:30`
  - 限制的成因解释：每个文件本身就是一条硬链接（指向文件系统上的数据块），**这就是它们受限于同一文件系统**的原因。 ｜ `sources/l2-5_trash-hardlinks.md:39`
  - 硬链接的三个行为后果：删任一副本不影响其它副本、只有全部副本删除后才回收空间、修改任一副本内容会影响所有副本（如改 mp3 标签会破坏做种）。 ｜ `sources/l2-5_trash-hardlinks.md:43,47,49,51`
  - 「即时移动（Atomic Move）」的定义是真正的移动，而非先复制到媒体目录再删除下载目录文件。 ｜ `sources/l2-5_trash-hardlinks.md:61`
  - 硬链接与即时移动的**双重前置条件**：所有路径必须在同一个文件系统上，并且还要满足权限——各应用必须能互相读写对方的文件。 ｜ `sources/l2-5_trash-hardlinks.md:73`
  - 权限由「应用运行的用户与组」「`UMASK`」「ownership」三者共同决定，并指向 Servarr Docker Guide 详述。 ｜ `sources/l2-5_trash-hardlinks.md:73`
  - 用户/组设定方式取决于镜像：LinuxServer.io 一类用 `PUID`/`PGID` 环境变量，另一类用 Docker 原生 `--user` / `user:`（`uid:gid`）。 ｜ `sources/l2-5_trash-hardlinks.md:75`
  - 给出两套推荐组合：多用户 + 共享组配 `UMASK 002`（目录 775、文件 664）；单用户配 `UMASK 022`（目录 755、文件 644）；并明确警告不要用 `UMASK 000`。 ｜ `sources/l2-5_trash-hardlinks.md:79,80,86`
- 关键实体（端口/路径/默认值等，逐字）: `exFAT`；`PUID`；`PGID`；`--user` / `user:`；`uid:gid`；`UMASK 002`；`UMASK 022`；`UMASK 000`；`775` (`drwxrwxr-x`)；`664` (`-rw-rw-r--`)；`755` (`drwxr-xr-x`)；`644` (`-rw-r--r--`)；`777`；`666`

### LB-6 · 完成回调占位符的一手取证（qBittorrent 上游源码 master）

- 文件: `sources/l2-6_placeholder-source.md` ｜ tier: 官方（上游源码 primary） ｜ evidence_form: fetched ｜ 取回日期: 2026-10-07
- 要点:
  - 占位符**确实存在**，且实现与展示分处两个文件：UI 说明文本在 `src/gui/optionsdialog.cpp`，实际替换逻辑在 `src/app/application.cpp`。 ｜ `sources/l2-6_placeholder-source.md:33,52`
  - UI 明确标注参数清单区分大小写（`Supported parameters (case sensitive):`），共列出 **13 个**占位符。 ｜ `sources/l2-6_placeholder-source.md:33`
  - 13 个占位符为 `%N` `%L` `%G` `%F` `%R` `%D` `%C` `%Z` `%T` `%I` `%J` `%K` `%M`，每个都有官方一句英文解释（如 `%F: Content path (same as root path for multifile torrent)`、`%D: Save path`）。 ｜ `sources/l2-6_placeholder-source.md:34-46`
  - UI 附一条官方 tip：参数含空白会被截断，需要用引号包裹（例如 `"%N"`）。 ｜ `sources/l2-6_placeholder-source.md:47`
  - 这些文本在运行时由代码 `m_ui->labelAutoRunParam->setText(autoRunStr)` 填入，`.ui` 里对应控件是空标签。 ｜ `sources/l2-6_placeholder-source.md:48,262`
  - 替换实现是 `Application::runExternalProgram(const QString &programTemplate, const BitTorrent::Torrent *torrent)`，逐字符扫描 `%` 后按下一字符分派。 ｜ `sources/l2-6_placeholder-source.md:52`
  - switch 分支与 UI 清单**逐字对应**：`C→filesCount`、`D→savePath`、`F→contentPath`、`G→tags`、`I→infoHash v1`、`J→infoHash v2`、`K→torrent id`、`L→category`、`M→comment`、`N→name`、`R→rootPath`、`T→currentTracker`、`Z→totalSize`。 ｜ `sources/l2-6_placeholder-source.md:74,98`
  - `%I` 与 `%J` 取不到时替换为字面量 `-`（`u"-"_s`）。 ｜ `sources/l2-6_placeholder-source.md:84,87`
  - 扫描方向为从串尾向前，并有一个 `--i` 回退以避免重复替换，官方注释举例的转义写法是 `%%N`。 ｜ `sources/l2-6_placeholder-source.md:115`
  - **执行位置**：源码里有**两个**触发点——`Application::torrentFinished`（完成时）与 `Application::torrentAdded`（添加时），F 组问题里的「完成回调」对应前者。 ｜ `sources/l2-6_placeholder-source.md:133`
  - 完成回调仅在开关打开时才执行，配置键为 `AutoRun/enabled`。 ｜ `sources/l2-6_placeholder-source.md:138,171`
  - 三个相关配置键及其默认值：`AutoRun/enabled` 默认 `false`、`AutoRun/program` 无默认、`AutoRun/ConsoleEnabled` 默认 `false`。 ｜ `sources/l2-6_placeholder-source.md:171,184,198`
  - UI 侧已从单一「完成时运行」扩展为两个可勾选分组：`Run on torrent added:` 与 `Run on torrent finished:`，外层分组标题为 `Run external program`。 ｜ `sources/l2-6_placeholder-source.md:221,239,215`
  - 「添加时」触发点同样受独立开关与独立程序串控制，配置键为 `AutoRun/OnTorrentAdded/Enabled`（默认 `false`）与 `AutoRun/OnTorrentAdded/Program`。 ｜ `sources/l2-6_placeholder-source.md:145,158,129`
  - 源码注释说明默认不给用户 shell 环境，理由是防止通过种子名等参数做命令注入（引用 issue 10925）。 ｜ `sources/l2-6_placeholder-source.md:54,57`

  （`sources/l2-6_placeholder-source.md` 的引用行号是该快照文件的内部行号；每行前缀即为该行在上游原始文件中的行号，例如快照第 33 行前缀为 `731:`，对应 `src/gui/optionsdialog.cpp:731`。）
- 关键实体（端口/路径/默认值等，逐字）: 占位符 `%N` `%L` `%G` `%F` `%R` `%D` `%C` `%Z` `%T` `%I` `%J` `%K` `%M`；转义 `%%N`；配置键 `AutoRun/enabled`、`AutoRun/program`、`AutoRun/ConsoleEnabled`、`AutoRun/OnTorrentAdded/Enabled`、`AutoRun/OnTorrentAdded/Program`；默认值 `false`；上游文件 `src/gui/optionsdialog.cpp`、`src/gui/optionsdialog.ui`、`src/app/application.cpp`、`src/base/preferences.cpp`；分支 `master`；issue `10925`

### 矛盾与缺口

- **官方 wiki 落后于源码**：LB-1（末次编辑 2026-09-03）在 `Downloads` 标签页下只有 `Run an external program on torrent completion` 一个小节且正文一句话（`l2-1_options-explained.md:89,90`）；而 master 源码 UI 已拆成 `Run on torrent added:` 与 `Run on torrent finished:` 两个可勾选分组（`l2-6_placeholder-source.md:239`）。写笔记时应以源码为准，并注明 wiki 未更新。
- **占位符清单在官方 wiki 中不存在**：LB-1 与 LB-2 都不列占位符（`l2-1_options-explained.md:90`、`l2-2_external-programs.md:12`）。本组得到的完整一手清单只有 LB-6 的 13 项；任何二手占位符表若要引用，只能以 `sources/l2-6_placeholder-source.md:34-46` 与 `:74,98` 为唯一比对基准。
- **qBittorrent 自身没有「硬链接」设置项**：LB-1 全篇未出现硬链接相关选项；硬链接是整理侧（MoviePilot 的 `设定 -> 目录 -> 整理模式`，`l2-3_moviepilot-reorganize.md:104`）的行为，qB 只负责下载完成的触发。二者是「触发方 + 执行方」关系，不是同一个配置点。
- **硬链接前置条件的两份口径需合并看**：MoviePilot 侧写作「同一磁盘/存储空间/映射路径」（`l2-3_moviepilot-reorganize.md:104`），TRaSH 侧写作「same file system」并补充权限/UMASK 条件（`l2-5_trash-hardlinks.md:30,73`）。MoviePilot 的口径缺少权限维度，只用 LB-3 会漏掉 UMASK/PUID-PGID 这一整块。
- **完成回调的路径口径无人显式声明**：LB-3/LB-4 要求「下载目录与下载器使用的目录一致」（`l2-4_moviepilot-download.md:15`），但都没有说明回调里 curl 的 `localhost:3000` 在 docker 下应填宿主地址还是容器名。这是一个实际配置缺口，本组来源无法回源回答。
- **LB-4 篇幅极短**（41 行，其中 30 行是 frontmatter 与后续章节），下载目录章节只有 3 句正文，未给出任何默认路径值；「默认下载目录是什么」在本组无官方来源可回源。
- **未取到的来源**：qBittorrent 官方对「保存路径」的默认值（如 Linux 下的默认下载目录）在 LB-1 中未给出具体字符串，只有设置项名称；`Settings` 页面亦未列出。该值需另找来源（如 qB 默认配置或源码 `preferences.cpp`），本组记为缺口。
