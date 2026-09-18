# 02 深度素材 — 把 SMB/CIFS 共享文件夹挂载到 Linux 服务器

- **运行标识**: smb-cifs-mount-linux
- **阶段**: P2 深度收集（未完成，等待用户确认素材质量与执行模式）
- **方向**: A 均衡实战（协议选型 → 手动挂载 → 凭据文件与 fstab → 排错 → 容器为可选小节）
- **深读日期**: 2026-09-18
- **深读分组**: G1 挂载语义 ／ G2 持久化与开机顺序 ／ G3 方言与错误码
- **来源规模**: 16 条（official 11 ／ secondary 1 ／ community 3 ／ 历史一手 1）

---

## 一、范围

**已确证可写的内容**：`mount -t cifs` 命令与选项语义、凭据文件写法与解析限制、`/etc/fstab` 持久化与 systemd 挂载单元的开机顺序机制、SMB 方言默认值与协商行为、Windows 侧签名强制对 Linux 客户端的影响、`mount error(13)` 的证据链排错、常见 errno 数值含义。

**只能标为「社区经验 / 未经一手证实」的内容**：飞牛 FNOS 侧默认方言与设置（无官方文档）、Docker 容器内挂载所需 capability、`fmask`/`dmask` 的废弃状态、`file_mode`/`dir_mode` 的具体默认数值、`mount.cifs` 打印的错误码是否直接等于 errno、SMB/NFS/WebDAV 的现代边界。

---

## 二、来源总表

| ID | 来源 | URL | 层级 | 版本/日期 | 用于 |
| --- | --- | --- | --- | --- | --- |
| S01a | mount.cifs(8) — Debian trixie | https://manpages.debian.org/trixie/cifs-utils/mount.cifs.8.en.html | official | cifs-utils **2:7.4-1**，页面更新 2025-06-12 | 选项语义与默认值主判据 |
| S01b | mount.cifs(8) — Debian bookworm | https://manpages.debian.org/bookworm/cifs-utils/mount.cifs.8.en.html | official | cifs-utils **2:7.0-2**，页面更新 2022-08-26 | Debian 12 兼容性基准 |
| S02 | systemd.mount(5) | bookworm https://manpages.debian.org/bookworm/systemd/systemd.mount.5.en.html ／ trixie https://manpages.debian.org/trixie/systemd/systemd.mount.5.en.html ／ unstable https://manpages.debian.org/unstable/systemd/systemd.mount.5.en.html | official | systemd **252.36** / **257.13** / **262~rc3** | fstab 选项与依赖排序判据 |
| S03 | How to mount CIFS shares permanently — Ubuntu Server Docs | https://ubuntu.com/server/docs/how-to/samba/mount-cifs-shares-permanently/ | official | **页面无版本/日期标注** | 发行版官方最小路径、凭据文件、回落策略 |
| S04 | Detect, enable, and disable SMBv1, SMBv2, and SMBv3 in Windows | https://learn.microsoft.com/en-us/windows-server/storage/file-server/troubleshoot/detect-enable-and-disable-smbv1-v2-v3 | official | 页面标注 **2025-03-12**（探测阶段记录为 ms.date 2025-02-28 / updated 2026-09-08，**两处不一致，写作以页面实际标注为准**） | Windows 侧 SMB1 现状、方言引入版本 |
| S05 | MountWindowsSharesPermanently — Ubuntu Wiki | https://wiki.ubuntu.com/MountWindowsSharesPermanently | official | 标 2024-04-18，**正文含 2008/9.04/12.04 遗留** | `chmod 600`、`~` 不展开、`noauto` 回落（须标陈旧） |
| S06 | Samba — ArchWiki | https://wiki.archlinux.org/title/Samba | official | scraped 2026-09-18 | 客户端挂载示例、`users` 复数、`\040`、`username=*` |
| S07 | Control SMB signing behavior | https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing | official | ms.date 2025-08-13（updated 2025-09-15） | 签名强制分档、`STATUS_INVALID_SIGNATURE` |
| S08 | Diagnosing CIFS permission denied / `cifs_mount failed w/return code = -13` | https://access.redhat.com/solutions/450913 | official | 2025-12-03，**Resolution 正文在订阅墙后** | `mount error(13)` 证据链 |
| S09 | [systemd-devel] mounts with "nofail" can be unmounted on shutdown before "After=\*-fs.target" units | https://lists.freedesktop.org/archives/systemd-devel/2024-June/050463.html | secondary | 2024-06-29，**原帖无任何回复** | `nofail` 关机乱序、`automount` 超时（未获上游确认） |
| S10 | 飞牛OS开机自动挂载SMB（jishuzhan.net，作者「好奇心害死薛猫」） | https://jishuzhan.net/article/2010524115405946881 | community | 2026-01-12 | FNOS 端唯一实测例（**密码明文，反面示例**） |
| S11 | 请问，LINUX系统下如何挂载NAS上的文件夹？（飞牛官方论坛） | https://club.fnnas.com/forum.php?mod=viewthread&tid=2318 | community | n/a | FNOS 挂载侧社区经验 |
| S12 | Best Solution to Mount a Windows Share within a Container — Docker Forums | https://forums.docker.com/t/best-solution-to-mount-a-windows-share-within-a-container/65424 | community | 2018-12-19（续帖至 2026-01-07） | 容器内挂载 CIFS（**无官方 capability 说明**） |
| S13 | mount.cifs(8) — man7.org（上游 man-pages） | https://man7.org/linux/man-pages/man8/mount.cifs.8.html | official | 手册自述对应 cifs vfs 2.18（≈ Linux 5.0） | `vers=` 协商默认、`seal`、`smb3` fstype、`/proc/fs/cifs/DebugData` |
| S14 | errno(3) — man7.org | https://man7.org/linux/man-pages/man3/errno.3.html | official | n/a | **明确不列数值**（跨架构不同），仅给名称与语义 |
| S15 | Linux 内核 uapi `errno-base.h` / `errno.h` | https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/errno-base.h ／ https://raw.githubusercontent.com/torvalds/linux/master/include/uapi/asm-generic/errno.h | official | 内核源码 master | 数值↔名称硬对应 |
| S16 | A New Network File System is Born: Comparison of SMB2, CIFS, and NFS（S. French, IBM/Samba Team, OLS） | https://www.kernel.org/doc/ols/2007/ols2007v1-pages-131-140.pdf | 历史一手 | **2007**，对 SMB3.1.1/NFSv4.2 已过时 | 协议设计意图与边界（仅此层面可用） |

**缓存路径**（正文不入仓，按需回查）：
- G1：`workspace/smb-cifs-mount-linux/.cache/p2_sources/g1_mount_semantics/{trixie,bookworm,archwiki}/`
- G2：`workspace/smb-cifs-mount-linux/.cache/p2_sources/g2_persistence/`（trixie 页另存 `trixie/` 子目录）
- G3：`workspace/smb-cifs-mount-linux/.cache/p2_sources/g3_dialect_errors/{S04,signing,01_access_redhat_com,GAP1,GAP1b2,GAP1c,GAP2b,GAP2c}`

---

## 三、主张 → 来源映射

### 3.1 挂载命令与选项

| 主张 | 来源 + 锚点 |
| --- | --- |
| `credentials=`/`cred=` 文件键：7.4-1 支持 `username`/`password`/`password2`/`domain`；7.0-2 只有前三项 | S01a / S01b `credentials=` |
| 凭据文件**不处理以空格开头的**用户名或密码；含逗号的密码写在 `-o password=` 会解析失败，放凭据文件/`PASSWD` 环境变量/交互输入则正常 | S01a `BUGS`（7.0-2 与此一致） |
| `uid`/`gid` 未指定时**默认 0**；只在服务器不提供属主信息时生效 | S01a `uid=` |
| `forceuid`/`forcegid` 忽略服务器给的属主，一律用 `uid=`/`gid=`；**没有任何选项能覆盖 mode** | S01a `forceuid`（`FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`） |
| 客户端权限检查**默认开启**（`perm`）；`noperm` 会让本机其他用户也能访问；服务器端检查按**挂载凭据**而非访问者身份 | S01a `noperm` |
| `file_mode`/`dir_mode` **只在服务器不支持 CIFS Unix extensions 时**覆盖默认 mode；**原文未给默认数值** | S01a `file_mode=` |
| `iocharset` 未指定时用内核构建时的 `nls_default`；服务器不支持 Unicode 时该参数不生效 | S01a `iocharset` |
| `vers=` 取值 1.0/2.0/2.1/3.0/3.02/3.1.1/3/default；未指定即 `vers=default` | S01a `vers=`、S13 `vers=` |
| 协商默认随内核变化：**< 4.13 → 1.0；4.13–4.13.5 → 3.0；≥ 4.13.5 → 协商 ≥2.1 的最高版本** | S13 `vers=`（S01a 同） |
| 挂载后查 `/proc/fs/cifs/DebugData` 可确认实际协商到的 Dialect | S13 `vers=` |
| `sec=` 默认：内核 < 3.8 为 `ntlm`，**≥ 3.8 为 `ntlmssp`** | S01a `sec=`、S13 `sec=` |
| `seal` 请求 SMB 层加密（AES-128-CCM），需 SMB3+ | S13 `seal` |
| `smb3` 文件系统类型在内核 4.18 加入；`mount.smb3` 只挂 SMB3 | S13 `Name` |
| 共享名后**不能加尾随 `/`**（`//SERVER/share/` 不工作）；无认证共享可用 `username=*` | S06 `Manual mounting` |
| 让普通用户挂载要用 **`users`（复数）**，其他文件系统才是 `user` | S06 `As mount entry` |
| 共享路径含空格写成 `\040` | S03 `Mount unprotected (guest) network folders`、S06 `As mount entry` |

### 3.2 凭据文件与持久化

| 主张 | 来源 + 锚点 |
| --- | --- |
| 别把密码写进 `/etc/fstab`（人人可读），用凭据文件 + `chmod 600` | S03 `Create a credentials file`、S05 |
| 凭据文件**不能有空格**：`password=x` 而非 `password = x`；域写 `domain=SALES` 而非用户名里的 `SALES\` | S03 `Login errors` |
| fstab 里 `credentials=` **必须写绝对路径**，`~` 不展开 | S05 `Use of tilde in pathnames`（2008 年段落，结论仍有效） |
| 凭据文件建议：目录 700、文件 600、属主 `root:root` | S06 `Storing share passwords` |
| **Ubuntu 官方最小示例只用 `0 0` + `credentials=`**，完全没有 `_netdev`/`nofail`/`x-systemd.*`，并自承服务器离线时开机可能报错 | S03 `Mount password-protected network folders` |
| 官方给的**唯一**回落策略是加 `noauto` 改为登录后挂载（或 libpam-mount）；**全文未提 `x-systemd.automount`** | S03 `Mount after login instead of boot` |

### 3.3 开机顺序与 systemd 机制

| 主张 | 来源 + 锚点 |
| --- | --- |
| 网络挂载单元**自动获得** `After=remote-fs-pre.target/network.target/network-online.target` 与 `Before=remote-fs.target`（+ `Wants=`），**除非设了 `nofail`** | S02 `Default Dependencies`（252.36） |
| `_netdev` 的作用是**覆盖**按 fstype 的自动判定；网络挂载被排在 `remote-fs-pre`→`remote-fs` 之间并 pull in `network-online.target` | S02 `_netdev` |
| `nofail`：只 wanted 不 required，且**不再排到 target 之前**，服务器离线时开机继续 | S02 `nofail` |
| 用 `x-systemd.automount` 时 **`auto`/`noauto` 均失效**，target 依赖由 automount 单元接管 | S02 `noauto, auto` |
| `x-systemd.idle-timeout=` 配置 automount 空闲超时（对应 `TimeoutIdleSec=`） | S02 `x-systemd.idle-timeout=` |
| `x-systemd.requires=` 同时建 `Requires=` 与 `After=`；`before=`/`after=` 只建排序；man page 明说这三者适合处理**带 `nofail` 的异步挂载**的排序问题 | S02 `x-systemd.requires=` |
| **`x-systemd.mount-timeout=` 存在且长期存在**（`Added in version 233`，257/262/252 三版均有定义）：配置 systemd 等 `mount` 命令完成的时长，超时即放弃该 fstab 条目；**只能写在 `/etc/fstab`，写进单元文件的 `Options=` 会被忽略** | S02 `x-systemd.mount-timeout=`（bookworm 页**不显示** "Added in version" 标注行） |
| 超时后的实际行为落在 `TimeoutSec=`：该挂载视为失败并被关闭，SIGTERM → 同长等待 → SIGKILL；默认取自 `DefaultTimeoutStartSec=` | S02 `TimeoutSec=` |
| `x-systemd.device-timeout=` 是**另一个**选项，管"等设备出现"，与 mount-timeout 不同 | S02 |
| 【secondary，未获上游确认】`nofail` 挂载关机时可能在 `After=*-fs.target` 的服务停止**之前**被卸载，导致服务挂起甚至数据丢失（原帖举例 qBittorrent + CIFS）；建议改用 `noauto` + `x-systemd.automount` | S09 标题/正文（**原帖为提问，归档无回复**） |
| 【secondary】`x-systemd.automount` 虽规避 `nofail`，但服务器不可达时默认停 90 秒，开机期触发可能永久挂起 | S09 |
| 容器内挂载 CIFS：`SYS_ADMIN`+`DAC_READ_SEARCH` 仍可能 `mount error 13`；`--privileged` 可行但被版主反对；推荐宿主机挂载后 bind mount 或用本地驱动 named volume | S12（**社区经验，无 Docker 官方说明**） |

### 3.4 方言、签名与 Windows 侧现状

| 主张 | 来源 + 锚点 |
| --- | --- |
| SMBv1 在 Windows 11 与 Server 2019+ 的所有 SKU 中**默认不安装** | S04 开头段 |
| SMBv2 引入于 Vista/Server 2008；SMBv3 引入于 Win8/Server 2012 | S04 `Disable SMBv2 or SMBv3` |
| 在 Win8/Server 2012 上开关 SMBv2 会**连带**开关 SMBv3（共用协议栈） | S04 `Use the command line...` |
| `SMB1`/`SMB2` 注册表值缺省即为 1（Enabled），默认状态不创建该键 | S04 同上 |
| 开启 `AuditSmb1Access` 后，客户端每次以 SMBv1 连接产生事件 **ID 3000** | S04 `Audit SMBv1 usage` |
| 关 SMBv3 会连带停用透明故障转移、横向扩展、多通道、SMB Direct、加密、目录租约等 | S04 `Disable SMBv2 or SMBv3` |
| 签名强制分档：**Win11 24H2 企业/专业/教育版 = 出站+入站；Server 2025 = 仅出站；Win11 24H2 家庭版 = 都不要求** | S07 `How SMB signing works` |
| 连不支持签名的第三方 SMB 服务器报 `0xc000a000` / `STATUS_INVALID_SIGNATURE`；**改协议版本不能绕过** | S07 `SMB signing behavior`、S04 开头段 |
| 微软明确反对用关闭协议版本或签名来绕过连接失败，应在远端服务器启用签名 | S04 开头段 |
| 要求签名会**同时禁用来宾访问**；来宾路径可能报 `0x80070035` | S07 `Disable SMB signing`、`SMB signing behavior` |
| 判定签名状态：`Get-SmbClientConfiguration \| FL RequireSecuritySignature`，True 即启用 | S07 `Verify SMB signing status` |
| 签名机制：把整条消息的哈希写入 SMB 头，用于防中继/欺骗 | S07 `How SMB signing works` |

### 3.5 错误码与排错

| 主张 | 来源 + 锚点 |
| --- | --- |
| `mount error(13)` 的证据链：`dmesg`/messages 中 `CIFS VFS: cifs_mount failed w/return code = -13` 若伴随 `Status code returned 0xc000006d NT_STATUS_LOGON_FAILURE`，方向是**凭据/认证**而非网络 | S08 `Issue` |
| 同一错误在手工挂载与 `mount -a`/fstab 两条路径都出现 | S08 `Issue` |
| `mount -vvv` 会打印 `Credential formatted incorrectly: (null)` 并暴露实际下发参数（如 `ver=1`、`prefixpath=DOMAIN/USER`） | S08 `Issue` |
| **数值↔名称硬对应**：`ENOENT` = 2 ｜ `EACCES` = 13 ｜ `EHOSTDOWN` = **112** ｜ `EHOSTUNREACH` = **113** ｜ `EINPROGRESS` = **115** ｜ `EREMOTEIO` = 121 | S15（`errno-base.h` / `errno.h`）、S14 示例输出佐证 2/13 |
| errno(3) **明确不列数值**，因为同一符号名在不同 UNIX/架构上编号不同 | S14 `Error numbers and names` |

### 3.6 协议选型（历史一手）

| 主张 | 来源 + 锚点 |
| --- | --- |
| SMB/CIFS 被称为「部署最广的网络文件系统协议」，NFS v3/v4 次之 | S16 |
| 作者认为 HTTP 对通用网络文件系统是差协议（缺锁、元数据少、无目录操作），因而有 WebDAV；但 WebDAV 并未取代 CIFS/NFS，且几乎没有可用的内核态实现 | S16 |
| **该文为 2007 年**，SMB2 刚部署、WebDAV RFC 2518；只能用于「协议设计意图/边界」，不能用于现代现状 | S16 |

### 3.7 FNOS 端（仅社区）

| 主张 | 来源 |
| --- | --- |
| fstab cifs 行含 `iocharset`/`uid`/`gid`/`file_mode`/`dir_mode`，配 `mount -a` 与 `@reboot` 延迟补挂 | S10（**password 明文，反面示例**） |
| Linux 挂载 FNOS 共享的路径写法与权限排查讨论 | S11 |

---

## 四、冲突与需并列呈现之处

| # | 冲突 | 处理建议 |
| --- | --- | --- |
| 1 | **`fmask`/`dmask` 是否废弃**：S05 有 2008 年旧注称"已废弃，改用 dir_mode/file_mode"；S01a/S01b **全文无 `fmask`/`dmask` 条目**，也没写废弃或换算关系 | 笔记中**不得**写「已废弃」为官方结论；可写「现版 man page 中不存在这两个条目；旧资料称改用 `file_mode`/`dir_mode`（来源为 2008 年 Ubuntu wiki 段落）」 |
| 2 | **`mapposix` 默认状态**：S01a 只把它列为翻译选项、未提默认；S06 称「自内核 3.18 起默认启用」，且把关闭它的 `nomapposix` 称为未文档化选项 | 并列呈现，标注"ArchWiki 说法未在 man page 中得到确认" |
| 3 | **guest 选项在开机挂载中的可靠性**：S03 把 `guest,uid=1000` 当可行做法；S05 报告 guest 开机不挂载、`mount -a` 却成功，改用 `username=guest,password=` 解决 | 并列，S05 那条注明"报告者自认无法解释原因" |
| 4 | **`nofail` 的关机顺序**：S02 只说 `nofail` 取消 `Before=remote-fs.target`；S09 进一步称会导致关机时早于 `After=*-fs.target` 的服务被卸载 | S09 为**未获上游确认的用户报告**（原帖无回复），笔记中须显式标注证据强度 |
| 5 | **回落策略的两条路线**：S03/S05 只有 `noauto` + 登录后挂载；S02/S06/S09 给出 `noauto` + `x-systemd.automount` | 呈现为「官方指南未覆盖 systemd 原生做法，但后者是更彻底的方案」 |
| 6 | **签名强制的粒度**：S04 开头段粗粒度称 Win11 24H2/Server 2025「默认要求签名」；S07 拆成三档（24H2 家庭版不要求、Server 2025 仅出站） | 用 S07 的细粒度表述，避免读者以为 Server 2025 要求入站签名 |
| 7 | **S04 页面日期**：探测阶段记 `ms.date 2025-02-28 / updated 2026-09-08`，深读阶段读到页面标 `2025-03-12` | 引用时以页面实际标注为准，并在来源表注明该不一致 |
| 8 | **凭据文件键差异**：按 trixie 文档写 `password2=`，在 bookworm（7.0-2）上超出该版本文档范围 | Debian 12 目标按 7.0-2 选项集合校验（7.4-1 的 91 个选项中，11 个为本版新增，**反向差集为空**） |

---

## 五、实操指引（可直接落笔）

1. **命令最小可用形**：`mount -t cifs //服务器/共享名 /挂载点 -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8`；共享名结尾不要加 `/`。[S01a, S06]
2. **凭据文件**：写 `username=`/`password=`/`domain=`（Debian 12 不要用 `password2=`），`chmod 600`、属主 `root:root`，等号两侧不留空格；fstab 中必须写绝对路径。[S01a, S01b, S03, S05, S06]
3. **fstab 行**：`//服务器/共享名 /挂载点 cifs credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail 0 0`；普通用户挂载把 `users`（复数）加进去；路径空格写 `\040`。[S02, S06]
4. **别把 `vers=` 写死**：不指定时默认协商 ≥2.1；只有老服务器才显式给 `vers=`。旧内核（<4.13）默认 1.0 是常见失败根因。[S01a, S13]
5. **核对实际方言**：挂载后看 `/proc/fs/cifs/DebugData`。[S13]
6. **开机不卡**：`nofail` 让服务器离线时也能开机；要彻底按需挂载用 `noauto` + `x-systemd.automount`（此时 `auto`/`noauto` 失效）。[S02]
7. **限制单次等待**：`x-systemd.mount-timeout=` 写在 **fstab** 里（写 unit 文件的 `Options=` 会被静默忽略）。[S02]
8. **`mount error(13)` 排错链**：`dmesg` 找 `cifs_mount failed w/return code = -13` + `NT_STATUS_LOGON_FAILURE` → 凭据/域/用户名方向；`mount -vvv` 看 `Credential formatted incorrectly`。[S08]
9. **错误码速查**：2 = `ENOENT`、13 = `EACCES`、112 = `EHOSTDOWN`、115 = `EINPROGRESS`（**不是** `EHOSTUNREACH`，那是 113）、121 = `EREMOTEIO`。[S15]
10. **Windows 连不上不是"协议版本问题"**：先查签名（`Get-SmbClientConfiguration | FL RequireSecuritySignature`）；`STATUS_INVALID_SIGNATURE`/`0xc000a000` 的处置是在**远端服务器**开签名，不是关客户端签名。[S04, S07]
11. **容器内挂载**：优先宿主机挂载 + bind mount，不要把 `--privileged` 当默认方案。[S12，社区经验]

---

## 六、未解问题（写作时必须显式标注，不得默认正确）

| # | 问题 | 现状 | 写作处理 |
| --- | --- | --- | --- |
| 1 | `mount error(N)` 的数字是否**直接等于** errno | 未证实。`mount.cifs(8)` 全文无映射表；cifs-utils 源码（git.samba.org / Debian sources）三次抓取均被 **HTTP 429** 拒绝。仅有名称↔数值的硬对应（S15）与 S08 的一条旁证（13 与内核 `SessSetup = -13` 同现） | 写「数值与 errno 的对应关系」，把"`mount.cifs` 直接打印 errno"标 `[推断]` |
| 2 | 红帽 KB 的 Resolution 步骤 | 订阅墙后不可读 | 不补写；只引用其 Issue/Environment 可见小节 |
| 3 | 哪些 fstype 被 systemd 判为「网络挂载」 | `systemd.mount(5)` 只说"按文件系统类型规范区分"，**全文未出现 cifs/smbfs** | 「cifs 会自动被识别为网络挂载、`_netdev` 可能冗余」必须标 `[推断]` |
| 4 | `nofail` 究竟取消哪几条依赖（是否含 `network-online.target` 的 `After=`/`Wants=`） | 252 与 257/262 措辞不同（后者扩为 `nofail`/`x-systemd.wanted-by=`/`x-systemd.required-by=`），原文从未逐条说明 | 只写"取消 required 身份与 target 排序"，不逐条断言 |
| 5 | 飞牛 FNOS 的默认方言 / SMB1 状态 / 签名默认值 | **无任何官方文档**；只有社区帖（S10/S11） | FNOS 段落标「社区经验」，不写默认值 |
| 6 | Docker 容器内挂载所需 capability | 只有论坛经验，说法互相矛盾（S12） | 标「社区经验」，给出"优先 bind mount"的稳妥建议 |
| 7 | `file_mode`/`dir_mode` 的默认数值 | man page 只说 "overrides the default file mode"，全文搜 `0755`/`0644` 零命中 | **不写具体数值** |
| 8 | `mount -a` 与 fstab 联动的语义 | 三份 G1 来源均无描述；`mount.cifs(8)` 全文只出现 1 次 umount | 不展开 `mount -a` 语义，只作命令使用 |
| 9 | Windows 侧自动协商"在何种条件下选中哪个方言" | S04/S07 均未说明 | 不写协商选择规则，只写默认方言与手工 `vers=` |
| 10 | `serverino` 何时该用 `noserverino` | 原文只说"默认启用" | 不提，或标"原文未给建议" |

---

## 七、工具与流程备忘（供后续运行复用）

1. **`crawl.sh` 输出文件名按域名生成，同域名不同 URL 会互相覆盖** —— 本次三组全部踩到（manpages.debian.org ×3、learn.microsoft.com ×2）。**不同 suite/不同页面必须建子目录**（`<dir>/trixie/`、`<dir>/signing/`）。G1 是靠字符数不匹配（51,093 vs 46,098）发现的，G3 是靠页面标题 + `Last updated` 行确认身份的。
2. **`Added in version` 标注行的存在性因文档而异**：`systemd.mount(5)` 的 trixie/unstable 页有（如 `Added in version 233`），bookworm 页没有；`mount.cifs(8)` **两版都没有**。据此判断"选项何时引入"时，先确认该页是否有此标注，否则只能用页脚版本行 + 选项表差集推得并标 `[推断]`。
3. **markdown 转换会压掉 man page 的 `<dt>` 结构**，选项名可能丢失；必要时回原始 HTML 取选项名。
4. **`git.samba.org` / Debian sources 对 cifs-utils 源码的抓取被 429 拒绝**，未解问题 1 因此无法闭环。

---

## 八、下游交接（给 outline-generator / chapter-writer）

- **建议骨架（方向 A，5 章）**：
  1. 协议选型与场景判断 —— 何时用 SMB/CIFS、与 NFS/WebDAV 的边界（材料薄，S16 已过时，写成"怎么判断"而非"谁更好"）
  2. 手动挂载：从零到挂上 —— 最小命令、选项含义（`uid`/`gid`/`file_mode`/`iocharset`/`vers`/`sec`）、FNOS 与 Windows 两个例子
  3. 凭据文件与开机自动挂载 —— 凭据文件规范、fstab 行、`_netdev`/`nofail`/`noauto`+`x-systemd.automount`、`x-systemd.mount-timeout`
  4. 排错 —— `mount error(13)` 证据链、errno 速查表（含 112/115 易错点）、方言协商核对、Windows 签名导致的连不上
  5. （可选，若用户要）容器内挂载 —— 一小节或独立章，全部标社区经验
- **写作纪律**（逐条对应 P1 缺口修正）：
  - FNOS 段落只能标 community（S10/S11），不写默认方言值。
  - `mount error(112/115/2)` 写「按 errno 推断」，给可复现的 `dmesg`/`journalctl` 查法。
  - `fmask`/`dmask`「已废弃」、`file_mode`/`dir_mode` 默认数值、`nofail` 逐条取消哪些依赖 —— 一律不得写成官方结论。
  - S05（Ubuntu Wiki）含 2008/12.04 遗留内容，引用时注明"官方 wiki，部分内容陈旧"。
  - S09（邮件列表）标注"未获上游确认的用户报告"。
  - 「官方文档说」类表述必须能回指到本文档的 SID + 锚点。
- **来源台账**：S01a/S01b 双版本、S02 三版本已就绪；引用选项默认值时必须带版本（如「cifs-utils 7.4-1」或「systemd 252」）。
