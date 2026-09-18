# 把 SMB/CIFS 共享文件夹挂载到 Linux 服务器

## 目录

- [第一章：协议选型：什么时候该用 SMB/CIFS](#第一章协议选型什么时候该用-smbcifs)
  - [1.1 写作定位：只写「怎么判断」，不写「谁更好」](#11-写作定位只写怎么判断不写谁更好)
  - [1.2 SMB/CIFS 的协议定位（历史一手层面）](#12-smbcifs-的协议定位历史一手层面)
  - [1.3 三个必须先确认的概念](#13-三个必须先确认的概念)
  - [1.4 判断清单：进入第 2 章前的自检项](#14-判断清单进入第-2-章前的自检项)
  - [本章小结](#本章小结)
  - [本章来源](#本章来源)
- [第二章：手动挂载：从零到挂上](#第二章手动挂载从零到挂上)
  - [2.1 前置：cifs-utils 与版本基线](#21-前置cifs-utils-与版本基线)
  - [2.2 挂载前先探测（推荐）](#22-挂载前先探测推荐)
  - [2.3 最小可用挂载命令](#23-最小可用挂载命令)
  - [2.4 选项语义逐项](#24-选项语义逐项)
  - [2.5 两个落地例](#25-两个落地例)
  - [2.6 挂载后核对：实际协商到哪一版方言](#26-挂载后核对实际协商到哪一版方言)
  - [2.7 常见坑](#27-常见坑)
  - [本章小结](#本章小结)
  - [本章来源](#本章来源)
- [第三章：凭据文件与开机自动挂载](#第三章凭据文件与开机自动挂载)
  - [3.1 凭据文件规范](#31-凭据文件规范)
  - [3.2 凭据文件的解析限制](#32-凭据文件的解析限制)
  - [3.3 /etc/fstab 行写法](#33-etcfstab-行写法)
  - [3.4 开机顺序机制](#34-开机顺序机制)
  - [3.5 服务器离线时的回落路线](#35-服务器离线时的回落路线)
  - [3.6 限制单次等待时间：x-systemd.mount-timeout=](#36-限制单次等待时间x-systemdmount-timeout)
  - [3.7 按需挂载的其余相关选项](#37-按需挂载的其余相关选项)
  - [3.8 其他：guest 在开机挂载中的可靠性](#38-其他guest-在开机挂载中的可靠性)
  - [3.9 常见坑](#39-常见坑)
  - [本章小结](#本章小结)
  - [本章来源](#本章来源)
- [第四章：排错：从错误码回到证据链](#第四章排错从错误码回到证据链)
  - [4.1 mount error(13) 的完整证据链](#41-mount-error13-的完整证据链)
  - [4.2 errno 名称↔数值对照](#42-errno-名称数值对照)
  - [4.3 方言协商的核对方法](#43-方言协商的核对方法)
  - [4.4 Windows 共享连不上时的优先排查方向](#44-windows-共享连不上时的优先排查方向)
  - [4.5 两条必须写明的未闭环](#45-两条必须写明的未闭环)
  - [4.6 常见坑](#46-常见坑)
  - [本章小结](#本章小结)
  - [本章来源](#本章来源)
- [第五章：容器内挂载](#第五章容器内挂载)
  - [5.1 容器内直接挂载 CIFS：现象与争议](#51-容器内直接挂载-cifs现象与争议)
  - [5.2 更稳妥的替代路径](#52-更稳妥的替代路径)
  - [本章小结](#本章小结)
  - [本章来源](#本章来源)

## 第一章：协议选型：什么时候该用 SMB/CIFS

你要把一台 Windows 或 NAS 上的共享文件夹挂到 Debian/Ubuntu 服务器上，第一件该做的事不是敲 `mount`，而是先判断「这个场景到底该不该走 SMB/CIFS、我的共享端支持哪一种」。这一章不给你「谁更好」的结论——现有资料不足以支撑——而是给你一份能自己走完的判断清单：共享端是什么、用哪一版方言、挂上以后谁来管权限。

### 1.1 写作定位：只写「怎么判断」，不写「谁更好」

本笔记的资料台账（`02_deep_research.md` §一）把「SMB/NFS/WebDAV 的现代边界」归入**只能标为社区经验 / 未经一手证实的内容**。也就是说，[缺口] 没有可靠的一手来源能支撑「什么时候该选 NFS、什么时候该选 SMB」这类选型结论。材料薄有两层原因：唯一从协议设计层面直接对比 SMB/CIFS 与 NFS 的一手文献是 S16，而它**发表于 2007 年**（下文 1.2 详述）；现有官方文档（Samba、Debian man page、Microsoft Learn）都是「怎么配」的文档，不是「该选谁」的文档。所以本章只把判断维度列全、把缺口显式写出来，**让读者以自己共享端的实际能力为依据做决定**。

### 1.2 SMB/CIFS 的协议定位（历史一手层面）

在**协议设计意图与边界**这一个层面上，S16 可用。该文为 S. French（IBM / Samba Team）在 OLS 发表的《A New Network File System is Born: Comparison of SMB2, CIFS, and NFS》，其观点是：

- SMB/CIFS 可称为「部署最广的网络文件系统协议」，NFS v3/v4 次之（S16）。
- 作者认为 HTTP 对通用网络文件系统是差协议——缺锁、元数据少、无目录操作——因而催生了 WebDAV；但 WebDAV 并未取代 CIFS/NFS，且几乎没有可用的内核态实现（S16）。

> [!warning] 这份材料的使用边界
> 该文自述为 **2007 年**发表，当时 SMB2 刚部署、WebDAV 还是 RFC 2518（S16）。它**只能用于「协议设计意图 / 边界」层面，不能用于现代现状**。任何「今天 SMB 与 NFS 谁更适合虚拟化」的推论都不能从 S16 推出来。

### 1.3 三个必须先确认的概念

> [!note] 核心概念
> 方言（`vers=`）、UNC 路径写法、挂载点属主语义——这三个概念在第 2 章会被逐项展开，在第 4 章排错时还会再用到。

进入第 2 章之前，这三个概念要在此先立住。

#### 1.3.1 SMB 版本与方言

「方言」（dialect）指的是客户端与服务端商量好用哪一版 SMB 协议来对话。对挂载端而言，可控的旋钮是 `mount` 的 `vers=` 选项，取值集合为 `1.0` / `2.0` / `2.1` / `3.0` / `3.02` / `3.1.1` / `3` / `default`；**不指定时即为 `vers=default`**（S01a `vers=`、S13 `vers=`）。而「default」不等于某个固定版本，而是随内核版本变化的协商策略：

| 内核版本 | 未指定 `vers=` 时的协商默认 |
| --- | --- |
| < 4.13 | `1.0` |
| 4.13 – 4.13.5 | `3.0` |
| ≥ 4.13.5 | 协商 ≥ 2.1 的最高版本 |

（S13 `vers=`）

这就是第 2 章会反复强调「别把 `vers=` 写死」的原因：在 ≥ 4.13.5 的内核上，不写 `vers=` 反而能协商到客户端与服务端都支持的最高版本。

> [!tip] 大白话
> 把「方言」想成打电话前先商量说普通话还是方言：谁也不会预设对方只会讲哪一口，而是**先试探、取双方都会的最高一档**。所以 `vers=default` 不是「某一版协议」，而是「先商量」这个动作本身；`vers=1.0` 则像强行要求对方只讲老家话——老服务器听得懂，新服务器可能压根不理你。

#### 1.3.2 UNC 路径与共享名写法

SMB 的共享路径没有 URL 那种 scheme，写法是 `//服务器/共享名`。有一个容易被忽略的硬约束：**共享名后不能加尾随 `/`**——`//SERVER/share/` 这种写法不工作（S06 `Manual mounting`）。

#### 1.3.3 挂载点语义：挂上以后由谁决定属主与权限

这是最容易在第一次挂载时被绊住的地方：CIFS 挂载点的属主与权限**不是**由 Linux 本地文件系统按常规规则决定的。

- `uid`/`gid` 未指定时**默认为 0**，且它们**只在服务器不提供属主信息时才生效**（S01a `uid=`）。
- `forceuid`/`forcegid` 会忽略服务器给回的属主，一律使用 `uid=`/`gid=` 指定的值；同时 man page 明确写着：**没有任何选项能覆盖 mode**（S01a `forceuid`、`FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）。

完整展开（`file_mode`/`dir_mode` 的生效条件、`perm`/`noperm` 的客户端权限检查）在第 2 章 2.4.1 与 2.4.2。这里先记住一句：**挂载点上的属主和权限是「谁在管」，和本地 `chown`/`chmod` 的直觉不是一回事。**

### 1.4 判断清单：进入第 2 章前的自检项

动手前按顺序回答下面四项。

1. **共享端是什么？** Windows 主机、NAS、还是飞牛 FNOS？这决定了服务端支持的方言范围与认证方式，也决定你该参考第 2 章哪个落地例。
2. **认证方式是什么？** 需要账号密码，还是匿名的无认证共享？后者在 CIFS 侧对应 `username=*` 的写法（S06 `Manual mounting`），可靠性讨论见第 3 章 3.8。
3. **要不要开机自动挂载？** 如果只是临时用，第 2 章的手动挂载就够了；如果要持久化，直接看第 3 章，并预先想好「服务器离线时开机该怎么表现」。
4. **Windows 侧的方言与签名现状是什么？** SMBv1 在 Windows 11 与 Server 2019+ 的所有 SKU 中**默认不安装**（S04 开头段）；SMBv2 引入于 Vista/Server 2008，SMBv3 引入于 Win8/Server 2012（S04 `Disable SMBv2 or SMBv3`）。签名强制问题在第 4 章 4.4 展开，这里只需先建立预期：**Windows 连不上时，第一顺位要查的是签名，不是协议版本**（S04 开头段、S07）。

> [!warning] 常见坑（认知层面）
> 最典型的认知坑是「连不上就把协议版本往下降」。它在今天的 Windows 侧基本无效甚至有害：SMBv1 默认不安装，你降不到那一档（S04 开头段）；微软也明确反对用关闭协议版本或关闭签名来绕过连接失败（S04 开头段）。先把方向搞对——**认证问题查凭据（第 3 章）、连不通查签名（第 4 章）**，再考虑 `vers=`。

### 本章小结

- 只给判断维度，不给选型结论：现代 SMB/NFS/WebDAV 边界归入「社区经验 / 未经一手证实」，[缺口] 无一手来源支持「谁更好」。
- S16 是唯一的协议对比一手文献，但**发表于 2007 年**，只能用于理解设计意图与边界（S16）。
- 「方言」是协商的结果，`vers=default` 在 ≥ 4.13.5 的内核上会协商 ≥ 2.1 的最高版本（S13 `vers=`）。
- 共享名写作 `//服务器/共享名`，**不能加尾随 `/`**（S06 `Manual mounting`）。
- 挂载点属主由 `uid`/`gid` 控制（默认 0），且**没有选项能覆盖 mode**（S01a `uid=`、`FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）。

下一章进入实操：装 `cifs-utils`、写出你的第一条 `mount -t cifs` 命令，并逐项拆开 `uid`/`file_mode`/`iocharset`/`vers`/`sec` 的语义与边界。

### 本章来源

| SID | 本章用途 |
| --- | --- |
| S01a | `vers=` 取值集合与 `vers=default` 默认；`uid`/`gid` 默认 0；`forceuid` 与「无选项可覆盖 mode」 |
| S04 | SMBv1 在 Win11/Server 2019+ 默认不安装；SMBv2/v3 引入版本；微软反对关协议/关签名绕过失败 |
| S06 | 共享名 `//SERVER/share` 且不能加尾随 `/`；`username=*` |
| S13 | `vers=` 协商默认随内核变化的三档；`vers=default` |
| S16 | 协议设计意图与边界（2007 历史一手），及其过时边界 |

## 第二章：手动挂载：从零到挂上

这一章要把共享真正挂到你的 Debian/Ubuntu 服务器上，并且让你说得清每一个选项在干什么、它的边界在哪里。我们不从 fstab 开始——那是第 3 章的事。先把命令在手动模式下跑通、跑懂，再谈持久化，否则开机挂载失败时你连该怀疑哪个选项都不知道。

### 2.1 前置：`cifs-utils` 与版本基线

Linux 侧的 CIFS 挂载能力来自 `cifs-utils` 包，它提供 `mount.cifs` 这个挂载辅助程序。先安装：

```bash
sudo apt update
sudo apt install cifs-utils
```

本笔记的两个版本基线如下（后续所有选项默认值都以此为据）：

| 发行版 | 包版本 | man page 页面更新日 |
| --- | --- | --- |
| Debian 13（trixie） | cifs-utils **2:7.4-1** | 2025-06-12（S01a） |
| Debian 12（bookworm） | cifs-utils **2:7.0-2** | 2022-08-26（S01b） |

> [!note] 为什么本章每条选项都要带版本号
> 这不是形式主义。两个版本的选项集合确实不同，而且差异已经落地到具体选项上：`credentials=` 文件支持的键，**7.4-1 支持 `username`/`password`/`password2`/`domain`；7.0-2 只有前三项**（S01a / S01b `credentials=`）。也就是说，你在 Debian 13 的文档上看到 `password2=`，照抄到 Debian 12 就超出了那个版本的文档范围（`02_deep_research.md` §四.8）。反向的差集为空——7.4-1 的 91 个选项中，11 个是该版新增的（`02_deep_research.md` §四.8）。**所以：以你目标发行版的 man page 为准，本笔记引用时一律带版本。**

### 2.2 挂载前先探测（推荐）

在盲挂之前，先用 `smbclient` 确认「共享名到底叫什么、我能不能进去」。它属于 Samba 套件，Debian 包名就叫 `smbclient`（S17a）。

```bash
sudo apt install smbclient

# 列出服务器上有哪些共享；-N 表示不提示输入密码
smbclient -L //fileserver -N
```

它能替你回答两个常见困惑：

- **目标共享名是否真的存在**（S17a `-L|--list`）。Windows 侧共享名和你以为的名字不一致是高频事故。
- **服务是否需要密码**。服务不需要密码时**必须显式加 `-N`**，否则客户端仍会提示你输密码；而如果命令行同时给了密码又给了 `-N`，命令行密码会被**静默忽略**（S17a `-N|--no-pass`）。

两条容易踩的限制：

- 目标写作 `//server/service`，其中 `server` 是 **NetBIOS 名，不一定是 IP 或 DNS 主机名**；NetBIOS 名与 DNS 名不一致或跨网段时，要补 `-I <ip>` 指定地址（S17a `DESCRIPTION`）。
- 脚本场景不要用命令行传密码，改用 `-A` 指定凭据文件（文件内为 `username =` / `password =` / `domain =` 三行），并**收紧该文件权限**（S17a `-A|--authentication-file`）。

确认能连上之后，进到 `smb:\>` 交互提示符下做两件事（S17a `OPERATIONS`）：

```bash
smbclient //fileserver/data -N
```

```text
smb: \> dir
smb: \> posix_whoami
```

`dir` 验证可读；`posix_whoami` 查看**服务端认定的 guest 状态与用户**——当你怀疑自己其实是「以匿名身份混进去」而不是用某个账号登录时，这是最直接的判断依据（S17a `OPERATIONS`）。

### 2.3 最小可用挂载命令

先建挂载点，再挂载：

```bash
sudo mkdir -p /mnt/share

# 最小可用形：凭据文件 + uid/gid + 字符集
sudo mount -t cifs //服务器/共享名 /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

（`02_deep_research.md` §五.1、S01a、S06）

这条命令里有三条必须知道的约束：

1. **共享名后不能加尾随 `/`**。`//SERVER/share/` 这种写法不工作（S06 `Manual mounting`）。
2. **`-o` 内部用逗号分隔选项**，因此含逗号的密码写在 `-o password=` 里会解析失败；把它放进凭据文件、`PASSWD` 环境变量或改成交互输入则正常（S01a `BUGS`，7.0-2 与此一致）。
3. **凭据文件必须先存在且权限正确**，否则这一条命令会因为读不到凭据而失败。凭据文件的完整规范在第 3 章 3.1；本章后续示例统一假定 `/root/.smbcred` 已按该规范建好。

> [!tip] 大白话
> `-o` 后面那一串，可以想成一张**授权清单**：逗号是清单条目的分隔符，每一项说的是「这个挂载点上的某个行为，按我说的来」。既然是清单，条目里当然不能再塞逗号——所以密码里有逗号时，写成 `-o password=ab,cd` 会被理解成「密码是 ab，另外还有一个叫 cd 的选项」，自然就崩了（S01a `BUGS`）。

### 2.4 选项语义逐项

这一节是本章的核心。每个选项都给出「它管什么 / 什么条件下才生效 / 边界在哪」，而不是只给一句「加上就好了」。

#### 2.4.1 属主与权限：`uid`/`gid`、`forceuid`/`forcegid`、`perm`/`noperm`

先给结论，再给可对比的命令。

- `uid`/`gid` **未指定时默认为 0**，且它们**只在服务器不提供属主信息时才生效**（S01a `uid=`）。
- `forceuid`/`forcegid` 的作用是**忽略服务器返回的属主**，一律使用 `uid=`/`gid=` 指定的值（S01a `forceuid`）。
- 客户端的权限检查**默认开启**（即默认相当于 `perm`）；`noperm` 会关掉它，后果是**本机其他用户也能访问**这个挂载点（S01a `noperm`）。
- 服务器端做的权限检查依据是**挂载时使用的凭据**，而不是访问者的身份（S01a `noperm`）。

三种写法并排看，差别只在「要不要信服务器」和「本地要不要自己把关」：

```bash
# ① 只在服务器不给属主信息时，才把文件显示为 1000:1000
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000

# ② 强制忽略服务器给回的属主，一律显示为 1000:1000
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,forceuid,forcegid

# ③ 关闭客户端权限检查（本机其他用户也能访问挂载点）
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,noperm
```

> [!warning] `forceuid` 换不来「一切都归我」
> man page 讲得很清楚：`forceuid`/`forcegid` 只管**属主**，**没有任何选项能覆盖 mode**（S01a `FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）。所以不要指望用 `forceuid` 顺带解决「文件权限是 755 不是 777」这类问题——那是 mode 类选项的职责，见下一节。

#### 2.4.2 mode 类选项：`file_mode`/`dir_mode`、`fmask`/`dmask`、`mapposix`

**`file_mode`/`dir_mode` 的生效条件**：它们**只在服务器不支持 CIFS Unix extensions 时**才用于覆盖默认 mode（S01a `file_mode=`）。

[缺口] **原文未给默认数值。** man page 只说 "overrides the default file mode"，全文搜 `0755`/`0644` 零命中（`02_deep_research.md` §六.7）。因此本笔记**不写 `file_mode`/`dir_mode` 的具体默认值**——你在别处看到的任何「默认 0755」说法，都不来自这两版 man page。

```bash
# 显式指定 mode（仅在服务器不支持 CIFS Unix extensions 时起作用，S01a file_mode=）
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,file_mode=0644,dir_mode=0755
```

**`fmask`/`dmask` 的争议必须并列呈现**（`02_deep_research.md` §四.1）：

| 说法 | 出处 | 证据强度 |
| --- | --- | --- |
| 称 `fmask`/`dmask`「已废弃，改用 `dir_mode`/`file_mode`」 | S05（Ubuntu Wiki，2008 年段落，官方 wiki，部分内容陈旧） | 旧资料说法，**不是官方结论文档** |
| 全文**没有** `fmask`/`dmask` 条目，既未写「废弃」也未写换算关系 | S01a / S01b | 现版 man page 的事实 |

结论只能说到这一步：**现版 man page 中不存在这两个条目；旧资料称应改用 `file_mode`/`dir_mode`（来源为 2008 年 Ubuntu wiki 段落）**。不得把「已废弃」写成官方结论（`02_deep_research.md` §四.1）。

**`mapposix` 同样并列呈现**（`02_deep_research.md` §四.2）：

- S01a 只把 `mapposix` 列为翻译选项，**未提默认值**。
- S06（ArchWiki）称「自内核 3.18 起默认启用」，并把用于关闭它的 `nomapposix` 称为未文档化选项。

[推断] 这两条不能合并成一句「mapposix 默认开启」。笔记的处理是：**并列写出两种说法，并标注「ArchWiki 说法未在 man page 中得到确认」**（`02_deep_research.md` §四.2）。

#### 2.4.3 字符集：`iocharset`

- `iocharset` 未指定时使用**内核构建时的 `nls_default`**（S01a `iocharset`）。
- 如果**服务器不支持 Unicode**，该参数不生效（S01a `iocharset`）。

```bash
# 中文文件名乱码时的常用写法
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

> [!tip] 大白话
> 字符集这事像**两个人对暗号**：`iocharset=utf8` 是你这边声明「我按 UTF-8 解读文件名」。但如果对面压根不用 Unicode 那套编码传名字，你这边声明的暗号再标准也没用——man page 明说了服务器不支持 Unicode 时该参数不生效（S01a `iocharset`）。所以乱码排查不能只盯着本地这一个参数。

#### 2.4.4 协议版本：`vers=`

取值集合为 `1.0` / `2.0` / `2.1` / `3.0` / `3.02` / `3.1.1` / `3` / `default`，未指定即 `vers=default`（S01a `vers=`、S13 `vers=`）。协商默认随内核变化：

| 内核版本 | 未指定 `vers=` 时的协商默认 |
| --- | --- |
| < 4.13 | `1.0` |
| 4.13 – 4.13.5 | `3.0` |
| ≥ 4.13.5 | 协商 ≥ 2.1 的最高版本 |

（S13 `vers=`；S01a 同）

[推断] `02_deep_research.md` §六.9 明确：**Windows 侧自动协商「在何种条件下选中哪个方言」是未解问题**，S04/S07 均未说明。因此本章**不写 Windows 侧协商选择规则**，只写默认方言与手工 `vers=`。

```bash
# 只在与老服务器对不上时才显式指定；新内核上不写 vers= 通常更好
sudo mount -t cifs //old-server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,vers=2.1
```

> [!tip] 大白话
> `vers=default` 不是「某一版协议」，而是「**先商量**」这个动作。老内核（< 4.13）之所以默认只到 `1.0`，是因为当年的商量策略保守；≥ 4.13.5 的内核改成「商量出 ≥ 2.1 里最高的一档」。所以显式写 `vers=1.0` 相当于**主动把天花板压到最低**——只在对面真的只会那一档时才这么做（S13 `vers=`）。

#### 2.4.5 安全与加密：`sec=`、`seal`

- `sec=` 默认值有明确分界：内核 **< 3.8 为 `ntlm`；≥ 3.8 为 `ntlmssp`**（S01a `sec=`、S13 `sec=`）。
- `seal` 请求 SMB 层加密（AES-128-CCM），**需要 SMB3+ 才可用**（S13 `seal`）。

```bash
# 要求 SMB 层加密（前提：协商到 SMB3 及以上）
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,sec=ntlmssp,seal
```

#### 2.4.6 文件系统类型：`smb3` 与 `mount.smb3`

`smb3` 这个**文件系统类型在内核 4.18 加入**；存在一个对应的挂载辅助程序 `mount.smb3`，它**只挂 SMB3**（S13 `Name`）。

```bash
# 用 smb3 fstype 挂载
sudo mount -t smb3 //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000
```

对比一眼：

| 写法 | 允许协商到的最高方言 | 用途 |
| --- | --- | --- |
| `mount -t cifs` | 由 `vers=` 决定，默认协商 ≥2.1 的最高版本 | 通用，兼容老服务器 |
| `mount -t smb3` / `mount.smb3` | 仅 SMB3 | 明确只走 SMB3 的场景 |

（S13 `Name`、S13 `vers=`）

另外，**无认证共享**可用 `username=*` 的写法（S06 `Manual mounting`）。它在开机挂载中的可靠性存在争议，见第 3 章 3.8。

#### 2.4.7 本章有意不展开的选项

`serverino`/`noserverino`：man page 原文**只说「默认启用」**，没有给「什么情况下该改用 `noserverino`」的建议（`02_deep_research.md` §六.10）。所以此处标「**原文未给建议**」，不展开——与其编一个使用场景，不如告诉你这个问题的答案不存在于现有材料里。

### 2.5 两个落地例

#### 2.5.1 Windows 共享

挂载侧的命令与上面 2.3 完全一致，差别只在**服务端前置条件**：

- Windows 侧要存在你连接的用户账号，且该账号对该共享有访问权。
- Windows 11 与 Server 2019+ 的 SMBv1 **默认不安装**（S04 开头段），别指望降版本能解决连通性问题。
- 若连接失败且报 `STATUS_INVALID_SIGNATURE` / `0xc000a000`，问题方向是**签名**，排查方法见第 4 章 4.4（S04、S07）。

```bash
# Windows 共享：命令形态与通用写法一致
sudo mount -t cifs //winhost/docs /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

#### 2.5.2 飞牛 FNOS 共享

> [!warning] 整段为社区经验，不写默认值
> FNOS 侧的默认方言、SMB1 状态、签名默认值**无任何官方文档**，`02_deep_research.md` §一、§六.5 明确归入「只能标为社区经验 / 未经一手证实」。以下内容来自社区帖 S10 / S11，**仅作社区经验**，本段不写任何默认方言值。

社区帖 S10 给出的做法是：fstab 中写一行 `cifs`，含 `iocharset`/`uid`/`gid`/`file_mode`/`dir_mode`，再配合 `mount -a` 与 `@reboot` 延迟补挂（S10，[社区]）。**它的凭据部分是反面示例：密码明文写进了 fstab**（S10，[社区]）。

我们引用它只是为了说明「有人这么干过」，**不复制它的凭据写法**——正确做法见第 3 章 3.1 与 3.3。

S11（飞牛官方论坛）提供的是 Linux 挂载 FNOS 共享时的路径写法与权限排查讨论（S11，[社区]）。同样只作社区经验参考。

### 2.6 挂载后核对：实际协商到哪一版方言

**「挂上了」不等于「用你期望的方言挂上的」。** 旧内核默认 `1.0` 也能挂上，只是后续性能和安全性完全不同；命令行成功不会告诉你用了哪一档（S13 `vers=`）。所以挂载之后要主动核对。

```bash
# 确认这个挂载点是否真的存在
findmnt -T /mnt/share

# 严格匹配该挂载点，并按类型过滤（-t 会让输出自动切换为 list 格式）
findmnt -M /mnt/share -t cifs

# 查看实际协商到的 Dialect
grep -i dialect /proc/fs/cifs/DebugData
```

（S17b `-t` / `-T` / `-M`；S13 `vers=`）

`findmnt` 两个选项的差别值得记住：

| 选项 | 匹配方式 |
| --- | --- |
| `-T /mnt/share` | 逐级向上回溯，找到承载该路径的挂载点 |
| `-M /mnt/share` | 严格匹配挂载点本身 |

（S17b `-T` / `-M`）

你也可以直接看退出码判断存在性：**0 = 有内容可显示；1 = 任何错误**（含按过滤条件无匹配、设备或挂载点不存在）（S17b `EXIT STATUS`）。

**为什么不能靠「挂上了」反推方言？** 因为挂载命令的返回值只回答「成功了没有」，不回答「用哪一档成功的」。两种完全不同的结果会给出同一个「成功」：

| 情形 | 命令结果 | 实际方言 |
| --- | --- | --- |
| 老内核（< 4.13），未写 `vers=` | 成功 | `1.0`（该内核的协商默认） |
| 新内核（≥ 4.13.5），未写 `vers=` | 成功 | ≥ 2.1 的最高版本 |

（S13 `vers=`）

两者在命令行上没有任何可见差别，差别只体现在安全性、性能以及后续能不能用 `seal` 这类需要 SMB3+ 的选项上。所以核对方言**必须**去读 `/proc/fs/cifs/DebugData`，而不是看挂载命令有没有报错（S13 `vers=`）。

### 2.7 常见坑

> [!warning] 手动挂载的四个高频坑
> 1. **共享名加了尾随 `/`**：`//SERVER/share/` 不工作（S06 `Manual mounting`）。
> 2. **密码含逗号却写在 `-o password=`**：会被逗号解析掉。改用凭据文件 / `PASSWD` 环境变量 / 交互输入（S01a `BUGS`）。
> 3. **指望 `forceuid` 顺带改掉 mode**：做不到，没有任何选项能覆盖 mode（S01a `FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）。
> 4. **以为 `file_mode`/`dir_mode` 总是生效**：它们只在服务器不支持 CIFS Unix extensions 时才用于覆盖默认 mode（S01a `file_mode=`）；而且它们的默认数值在现有 man page 中**根本没有记载**（`02_deep_research.md` §六.7）。

### 本章小结

- 版本基线：cifs-utils **7.4-1**（trixie）/ **7.0-2**（bookworm）；差异是实打实的，例如 `credentials=` 文件键（S01a / S01b `credentials=`）。
- 最小可用命令是 `mount -t cifs //服务器/共享名 /挂载点 -o credentials=...,uid=...,gid=...,iocharset=utf8`；共享名不能加尾随 `/`（S06 `Manual mounting`）。
- 属主与权限：`uid`/`gid` 默认 0 且只在服务器不给属主时生效；`forceuid`/`forcegid` 强制覆盖属主，但**没有选项能覆盖 mode**；`noperm` 关闭客户端权限检查会让本机其他用户也能访问（S01a）。
- `file_mode`/`dir_mode` 仅在服务器不支持 CIFS Unix extensions 时生效，**默认数值无来源**；`fmask`/`dmask` 的「已废弃」说法来自 2008 年旧资料，现版 man page 无该条目（S01a `file_mode=`、S05、`02_deep_research.md` §四.1）。
- 方言：默认协商随内核分三档（< 4.13 → 1.0；4.13–4.13.5 → 3.0；≥ 4.13.5 → ≥2.1 最高版本）；挂载后读 `/proc/fs/cifs/DebugData` 才是确认手段（S13 `vers=`）。
- 探测与核对：挂载前 `smbclient -L //server -N`，挂载后 `findmnt -M /mnt -t cifs`（S17a、S17b）。

下一章把密码从命令行里挪走，写进凭据文件与 `/etc/fstab`，并解决那个真正让人熬夜的问题：服务器没开机时，服务器自己的开机流程该怎么办。

### 本章来源

| SID | 本章用途 |
| --- | --- |
| S01a | 7.4-1 基线；`credentials=` 键集合；`uid=`；`forceuid` 与「无选项可覆盖 mode」；`noperm`；`file_mode=`；`iocharset`；`vers=`；`sec=`；`BUGS`（逗号密码、空格开头凭据） |
| S01b | 7.0-2 基线；`credentials=` 键集合；`file_mode`/`fmask` 条目缺失的比对依据 |
| S04 | Windows 侧 SMBv1 默认不安装；方言引入版本（2.5.1 前置条件） |
| S05 | `fmask`/`dmask`「已废弃」说法的出处（2008 年，官方 wiki 部分内容陈旧） |
| S06 | 共享名尾随 `/` 不工作；`username=*`；`As mount entry` 相关写法 |
| S07 | Windows 侧签名现象与排查指向（2.5.1） |
| S10 | FNOS 社区实测例（含密码明文反面示例） |
| S11 | FNOS 挂载侧社区经验 |
| S13 | `vers=` 三档协商默认；`seal`；`smb3` fstype 与 `mount.smb3`；`/proc/fs/cifs/DebugData` |
| S17a | `smbclient -L` 探测、`-N`、`-A`、`posix_whoami`、NetBIOS 名说明 |
| S17b | `findmnt -T`/`-M`/`-t` 与退出码语义 |

> 标注说明：2.5.2 全段为 `[社区]`（S10/S11）；2.4.2 的 `mapposix` 为 `[推断]`；`file_mode`/`dir_mode` 默认数值、2.4.7 的 `serverino` 使用建议为 `[缺口]`；2.4.2 的 `fmask`/`dmask` 争议按 §四.1 并列呈现，未写成官方结论。

## 第三章：凭据文件与开机自动挂载

手动挂载能用了，接下来要解决两个新问题：密码不能再出现在命令行和 `/etc/fstab` 里，以及——服务器重启时，如果共享端没开机、网络还没起来，你的机器会不会卡在开机界面。这一章先把凭据收进一个权限正确的文件，再逐层拆开 systemd 处理网络挂载的开机顺序，最后给出服务器离线时的三条回落路线。

### 3.1 凭据文件规范

**第一条原则：不要把密码写进 `/etc/fstab`。** 理由很直接——fstab 是人人可读的；正确做法是密码放进凭据文件，再 `chmod 600`（S03 `Create a credentials file`、S05）。社区帖 S10 里那种把 `password` 明文写进 fstab 的做法，就是本章通篇要你避开的反面示例（S10，[社区]）。

凭据文件的内容如下（三行，等号两侧不留空格）：

```ini
# /root/.smbcred
username=smbuser
password=your-password-here
domain=SALES
```

权限与属主：

```bash
# 文件 600，属主 root:root；存放目录建议 700（S06 Storing share passwords）
sudo chmod 600 /root/.smbcred
sudo chown root:root /root/.smbcred
sudo chmod 700 /root
```

两条语法硬约束（S03 `Login errors`）：

- **等号两侧不能有空格**：写 `password=x`，不能写 `password = x`。
- **域写在 `domain=` 键里**，而不是塞进用户名：写 `domain=SALES`，不要写成 `SALES\username` 那种形式。

一条容易被忽略的路径约束：**fstab 里的 `credentials=` 必须写绝对路径，`~` 不会被展开**（S05 `Use of tilde in pathnames`）。这条出自 S05 的 2008 年段落，但结论至今仍有效——systemd 解析 fstab 时不会替你做 shell 的波浪号展开。注意 S05 是官方 wiki，**部分内容陈旧**（含 2008/9.04/12.04 遗留），引用时以此为前提。

[缺口] 还有一个版本边界要记住：`password2=` 键在 **7.4-1（trixie）** 中受支持，但在 **7.0-2（bookworm）** 上**超出该版本文档范围**，只有 `username`/`password`/`domain` 三项（S01a / S01b `credentials=`、`02_deep_research.md` §四.8）。以 Debian 12 为目标时，别用 `password2=`。

### 3.2 凭据文件的解析限制

凭据文件不是万能容器，它有两个已记录的解析限制（S01a `BUGS`，7.0-2 与此一致）：

1. **以空格开头的用户名或密码不被处理**。你的密码如果以空格打头，写进凭据文件不会得到你想要的结果（S01a `BUGS`）。
2. **含逗号的密码不能写在 `-o password=` 里**，会解析失败。可用的路径有三条：写进凭据文件、用 `PASSWD` 环境变量、或改成交互式输入（S01a `BUGS`）。

```bash
# 含逗号密码的可用路径之一：凭据文件（内容见 3.1）
sudo mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred

# 路径之二：PASSWD 环境变量
sudo PASSWD='pa,ss' mount -t cifs //server/share /mnt/share -o username=smbuser

# 路径之三：交互输入（不给 password= 时由 mount.cifs 提示）
sudo mount -t cifs //server/share /mnt/share -o username=smbuser
```

### 3.3 `/etc/fstab` 行写法

Ubuntu 官方文档给出的最小示例，形态是**只有 `credentials=` 加结尾的 `0 0`**，完全没有 `_netdev`/`nofail`/`x-systemd.*` 这些选项（S03 `Mount password-protected network folders`）。而且该文档**自承**：服务器离线时，开机可能报错（S03 `Mount password-protected network folders`）。

```ini
# /etc/fstab —— 官方最小形态：只有 credentials= 和结尾 0 0
//server/share  /mnt/share  cifs  credentials=/root/.smbcred  0  0
```

要写完整一点、覆盖开机场景时，本笔记采用的形态是（`02_deep_research.md` §五.3）：

```ini
# /etc/fstab
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail  0  0
```

几个写法细节：

- **路径含空格写成 `\040`**（S03 `Mount unprotected (guest) network folders`、S06 `As mount entry`）。fstab 用空格分隔字段，所以路径里的空格必须转义。
- **让普通用户挂载要用 `users`（复数）**，其他文件系统才是 `user`（S06 `As mount entry`）。
- 改完 fstab 先校验再重启：`findmnt --verify` 会检查 fstab 的**可解析性与可用性**，加 `--verbose` 可看细节；`-s` 用于在 `/etc/fstab` 中搜索条目（S17b `-x|--verify`、`-s|--fstab`）。

```bash
# 改完 fstab 先校验可解析性，再考虑重启
sudo findmnt --verify --verbose
```

> [!warning] `--verify` 不验证远端共享能不能挂上
> `findmnt --verify` 原文只说校验 "parsability and usability"，**未列具体检查项**；它**不会**替你验证远端共享是否真的能挂上（S17b `-x|--verify` → [推断]）。所以通过校验不等于挂载会成功，别把它当验收。

### 3.4 开机顺序机制

fstab 里的条目会被 systemd 生成挂载单元，而 systemd 对「网络挂载」有一整套默认依赖安排。先看默认行为：

**网络挂载单元会自动获得**以下依赖关系——`After=remote-fs-pre.target`、`network.target`、`network-online.target`，以及 `Before=remote-fs.target`（并带相应的 `Wants=`）；**除非你设了 `nofail`**（S02 `Default Dependencies`，systemd 252.36）。

**`_netdev` 的作用是「覆盖」按 fstype 的自动判定**：它让该挂载被排在 `remote-fs-pre` → `remote-fs` 之间，并 pull in `network-online.target`（S02 `_netdev`）。

[推断] 这里有一个必须标为推断的点：**「cifs 会被 systemd 自动识别为网络挂载、因而 `_netdev` 可能冗余」这个说法没有一手依据**。`systemd.mount(5)` 只说「按文件系统类型规范区分」，**全文未出现 cifs/smbfs**（`02_deep_research.md` §六.3）。所以：**`_netdev` 用不用，属于 `[推断]` 层面的选择**，不要当成官方定论。

**`nofail` 的语义**：它让该挂载**只 wanted、不 required**，并且**不再被排到 target 之前**，于是服务器离线时开机可以继续走过去（S02 `nofail`）。

[推断] 关于 `nofail`「取消依赖」的粒度，`02_deep_research.md` §六.4 明确要求：**只写「取消 required 身份与 target 排序」，不逐条断言它到底取消了哪几条依赖**。原因是 systemd 252 与 257/262 的措辞不同（后者扩为 `nofail`/`x-systemd.wanted-by=`/`x-systemd.required-by=`），原文从未逐条说明（`02_deep_research.md` §六.4）。本笔记严格按这个粒度写。

把三个选项的分工整理成一张对照表：

| 选项 | 它解决的问题 | 代价 / 边界 |
| --- | --- | --- |
| `_netdev` | 明确声明这是网络挂载，覆盖按 fstype 的自动判定（S02 `_netdev`） | 「cifs 是否已被自动判定为网络挂载」本身无一手依据（`[推断]`，§六.3） |
| `nofail` | 服务器离线时开机不卡住，挂载只 wanted 不 required，且不再排到 target 之前（S02 `nofail`） | 精确取消了哪几条依赖原文未逐条说明（§六.4）；关机阶段存在社区报告的顺序问题（见 3.5.4） |
| `noauto` + `x-systemd.automount` | 彻底改成按需挂载，不用等开机（S02 `noauto, auto`） | 此时 `auto`/`noauto` 均失效，target 依赖由 automount 单元接管（S02 `noauto, auto`）；另有社区报告的 90 秒等待问题（见 3.5.4） |

> [!tip] 大白话
> 把开机想成早上给一整栋楼开门：
> **`_netdev`** 是跟门卫说「这间屋子要等网络线路通了才进去检查」——只是**调整做事顺序**。
> **`nofail`** 是说「这间屋子检查不了就先跳过，别把整栋楼的门都堵着不让开」——**降低这间屋子的重要性**。
> **`noauto` + `x-systemd.automount`** 更彻底：**早上压根不查这间屋子**，谁要进去谁再刷门禁卡现开——把「开机时做」改成「用时才做」。
> 三者不是叠加越多越好：它们各自换来的代价写在右列，选哪个取决于是「顺序不对」「怕卡住」还是「根本不想在开机时做」。

### 3.5 服务器离线时的回落路线

#### 3.5.1 `noauto` + 登录后挂载

官方文档给出的**唯一**回落策略是：加 `noauto`，把挂载从开机阶段改到登录后（或改用 libpam-mount）（S03 `Mount after login instead of boot`；S05 同）。

```ini
# /etc/fstab —— noauto：开机不挂，登录后手动 mount
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto  0  0
```

```bash
# 登录后手动挂上
sudo mount /mnt/share
```

#### 3.5.2 `noauto` + `x-systemd.automount`

更彻底的做法是改用 systemd 原生的按需挂载：`noauto` 配合 `x-systemd.automount`（S02 `noauto, auto`、S06、S09）。

```ini
# /etc/fstab —— 按需挂载：访问挂载点时才真正挂载
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto,x-systemd.automount  0  0
```

关键约束：**使用 `x-systemd.automount` 时，`auto`/`noauto` 均失效**，target 依赖由 automount 单元接管（S02 `noauto, auto`）。也就是说这个组合里的 `noauto` 不再按字面意义起作用，挂载时机完全由 automount 单元决定。

#### 3.5.3 必须写明的事实：官方指南未覆盖 systemd 原生做法

这一点不能含糊：**Ubuntu 官方文档全文未提 `x-systemd.automount`**（S03 全文未提，`02_deep_research.md` §四.5）。所以 3.5.2 的做法虽然更彻底，但它**不是官方指南给出的路线**——官方给的只有 3.5.1。两条路线并列呈现，读者自行取舍（`02_deep_research.md` §四.5）。

#### 3.5.4 `[社区]` 两条附带报告

以下两条来自 systemd-devel 邮件列表的一封**提问帖**，**原帖归档后没有任何回复**，属于**未获上游确认的用户报告**（S09，secondary）：

- 带 `nofail` 的挂载，在关机时可能在 `After=*-fs.target` 的服务停止**之前**就被卸载，导致这些服务挂起甚至数据丢失；原帖举的例子是 qBittorrent + CIFS。发帖人的建议是改用 `noauto` + `x-systemd.automount`（S09）。
- `x-systemd.automount` 虽然规避了 `nofail` 的问题，但当**服务器不可达时默认停 90 秒**，如果在开机期触发，可能造成永久挂起（S09）。

> [!warning] 证据强度说明
> 上面两条**均为未获上游确认的用户报告**（原帖是提问，无任何回复），**不能当作 systemd 的既定行为**。它们只说明「有人报告过这个现象」，是否复现取决于你的环境。

### 3.6 限制单次等待时间：`x-systemd.mount-timeout=`

这个选项用于配置 **systemd 等待 `mount` 命令完成的时长**，超时即放弃该 fstab 条目（S02 `x-systemd.mount-timeout=`）。

关于它的存在性与引入版本（S02）：

- 选项**存在且长期存在**，`Added in version 233`，在 257 / 262 / 252 三版中均有定义（S02 `x-systemd.mount-timeout=`）。
- 但要注意：**bookworm 页面不显示 `Added in version` 标注行**。所以「这个选项何时引入」的判定，在 bookworm 页上只能靠三版对照得出（`02_deep_research.md` §七.2 也记录了这类标注行「存在性因文档而异」的规律）。

**最关键的约束：它只能写在 `/etc/fstab`。写进单元文件的 `Options=` 会被忽略**（S02 `x-systemd.mount-timeout=`）。

```ini
# /etc/fstab —— 只等 30 秒，超时放弃该条目
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,_netdev,nofail,x-systemd.mount-timeout=30  0  0
```

超时之后发生什么？实际行为落在 `TimeoutSec=` 上：该挂载被视为失败并被关闭，流程是 SIGTERM → 再等同样长的时间 → SIGKILL；默认值取自 `DefaultTimeoutStartSec=`（S02 `TimeoutSec=`）。

还要区分一个名字相近但作用不同的选项：`x-systemd.device-timeout=` 管的是**「等设备出现」**，与 `mount-timeout` 不是一回事（S02）。

### 3.7 按需挂载的其余相关选项

- **`x-systemd.idle-timeout=`**：配置 automount 的空闲超时，对应单元侧的 `TimeoutIdleSec=`（S02 `x-systemd.idle-timeout=`）。
- **`x-systemd.requires=`**：同时建立 `Requires=` 与 `After=` 两种依赖；而 `x-systemd.before=` / `x-systemd.after=` **只建排序**（S02 `x-systemd.requires=`）。

```ini
# /etc/fstab —— 按需挂载 + 空闲 10 分钟后卸载
//server/share  /mnt/share  cifs  credentials=/root/.smbcred,noauto,x-systemd.automount,x-systemd.idle-timeout=10  0  0
```

值得注意的一点：man page **明说**这三个选项适合处理**带 `nofail` 的异步挂载**的排序问题（S02 `x-systemd.requires=`）。也就是说，官方给它们的使用场景描述里，「配合 `nofail` 使用」是被点名的。

### 3.8 其他：`guest` 在开机挂载中的可靠性

这个问题存在一份**互相冲突**的材料，按 `02_deep_research.md` §四.3 并列呈现：

| 说法 | 出处 | 具体内容 |
| --- | --- | --- |
| `guest` 可行 | S03 | 把 `guest,uid=1000` 当作可行做法（S03 `Mount unprotected (guest) network folders`） |
| `guest` 开机不挂载 | S05 | 报告称 guest 在开机时不挂载，但 `mount -a` 却成功；改用 `username=guest,password=` 后解决 |

[社区] 关于 S05 那一条，必须**注明「报告者自认无法解释原因」**（`02_deep_research.md` §四.3）——它是一个现象报告，不是一个有机制解释的结论。另外 S05 为官方 wiki 且**部分内容陈旧**，引用时同样要带这个前提。

### 3.9 常见坑

> [!warning] fstab 与凭据的五个高频坑
> 1. **密码写进 `/etc/fstab`**：fstab 人人可读，必须改用凭据文件 + `chmod 600`（S03 `Create a credentials file`、S05）。
> 2. **凭据文件里等号两侧留了空格**：`password = x` 不生效，必须写 `password=x`；域要写 `domain=SALES`，不能写成 `SALES\username`（S03 `Login errors`）。
> 3. **fstab 里 `credentials=` 用了 `~`**：不会展开，必须写绝对路径（S05 `Use of tilde in pathnames`）。
> 4. **以为 `x-systemd.mount-timeout=` 写哪都行**：只能写在 `/etc/fstab`，写进单元文件的 `Options=` 会被忽略（S02 `x-systemd.mount-timeout=`）。
> 5. **以为加了 `nofail` 就万事大吉**：它解决的是开机不被卡住（S02 `nofail`），但关机阶段的顺序问题有社区报告，且 `x-systemd.automount` 路线在服务器不可达时有 90 秒等待的报告（均为未获上游确认的用户报告，S09）。

### 本章小结

- 凭据文件的规范是：等号两侧不留空格、域写 `domain=`、目录 700 / 文件 600 / 属主 `root:root`，fstab 中必须写绝对路径（S03、S05、S06）。
- 两个解析限制：以空格开头的用户名或密码不被处理；含逗号的密码不能用 `-o password=`，要走凭据文件 / `PASSWD` / 交互输入（S01a `BUGS`）。
- Ubuntu 官方最小 fstab 形态只有 `credentials=` + `0 0`，且**自承服务器离线时开机可能报错**；官方给的唯一回落策略是 `noauto` + 登录后挂载（S03）。
- 开机顺序三件套的分工：`_netdev` 覆盖按 fstype 的自动判定；`nofail` 让挂载只 wanted 不 required 且不再排到 target 之前；`noauto` + `x-systemd.automount` 改成按需挂载（此时 `auto`/`noauto` 均失效）（S02）。
- `x-systemd.mount-timeout=` 存在且长期存在（`Added in version 233`），**只能写在 fstab**；超时后的行为落在 `TimeoutSec=`（S02）。
- 两处证据强度提醒：`_netdev` 对 cifs 是否冗余属 `[推断]`（§六.3）；`nofail` 关机顺序与 automount 90 秒等待是未获上游确认的用户报告（S09）。

下一章换一个方向：不再追求「挂上」，而是当它挂不上时，怎么从错误码一步步回溯到证据。我们会从 `mount error(13)` 的完整证据链讲起，并纠正一个普遍误解——`13` 表示「被拒绝」，不等于「网络不通」。

### 本章来源

| SID | 本章用途 |
| --- | --- |
| S01a | 凭据文件解析限制（`BUGS`：空格开头、含逗号密码）；`password2=` 的版本边界（7.4-1） |
| S01b | 7.0-2 的 `credentials=` 键集合（`password2=` 超出该版本文档范围） |
| S02 | 网络挂载默认依赖（252.36）；`_netdev`；`nofail`；`noauto, auto` 与 `x-systemd.automount`；`x-systemd.mount-timeout=` 与 `Added in version 233`；`TimeoutSec=`；`x-systemd.device-timeout=`；`x-systemd.idle-timeout=`；`x-systemd.requires=` |
| S03 | 凭据文件与 `chmod 600`；`Login errors`；fstab 最小形态与其离线自承；`noauto` 回落；`guest,uid=1000` |
| S05 | `~` 不展开（2008 年段落，官方 wiki 部分内容陈旧）；`guest` 开机挂载失败报告；`noauto` 回落 |
| S06 | 凭据文件权限建议；`\040`；`users` 复数；`x-systemd.automount` |
| S09 | `nofail` 关机乱序与 automount 90 秒等待（未获上游确认的用户报告） |
| S10 | fstab 密码明文反面示例（[社区]） |
| S17b | `findmnt --verify` 校验 fstab、`-s` 搜索条目 |

> 标注说明：3.5.4 与 3.8 的 S05 条目为 `[社区]` / 未获上游确认；3.4 中「cifs 自动判为网络挂载」为 `[推断]`；`nofail` 逐条依赖未写；`password2=` 为 `[缺口]`（bookworm 超范围）；`findmnt --verify` 不验证远端共享为 `[推断]`。

## 第四章：排错：从错误码回到证据链

`mount error(13)` 是这套工具链里最会误导人的一行输出：它看起来像结论，实际上只是入口。数字本身不携带原因，原因分散在三条不同的证据带上——内核日志、同现的 NT 状态码、以及 `mount -vvv` 暴露的实际下发参数。本章按「从现象到证据」的顺序组织，错误码只作为链条上的节点：跑完这条链，你要能判断问题落在认证、网络还是方言协商上，而不是背下一张错误码清单。

> [!note] 核心概念：证据链
> 「证据链」指从现象出发、每一步都落在一个可复现的命令输出上，直到方向被唯一确定。它的反面是「错误码清单」：把 `13` 当结论背下来，换个内核、换个服务器就不适用了。

### 4.1 `mount error(13)` 的完整证据链

#### 第零步：先确认共享名真的存在

很多「认证失败」其实是共享名写错。挂载前先用 `smbclient` 列一次服务器上的共享：

```bash
# 在 Debian/Ubuntu 上列出 //server 提供的共享（包名 smbclient，属 Samba 套件）
smbclient -L //server -N
```

`-L` 用于列出服务器上的共享，确认目标共享名存在；当 NetBIOS 名与 DNS 名不一致或跨网段时，补 `-I <ip>`（S17a `-L|--list`）。服务端确实不需要密码时**必须显式加 `-N`**，否则客户端仍会提示输入密码；命令行同时给出密码与 `-N` 时，命令行上的密码会被静默忽略（S17a `-N|--no-pass`）。

如果目标是「是不是以匿名身份进去了」，连上共享后在 `smb:\>` 提示符下执行 `posix_whoami`，它会显示服务端认定的 guest 状态与用户（S17a `OPERATIONS`）。

#### 第一步：在内核日志里找到 CIFS 那一行

挂载报错的用户态输出很短，真正的现场记录在内核日志里。红帽 KB 的 Issue 小节记录的现象是 `mount error(13)`，内核侧留下的原文形态是 `CIFS VFS: cifs_mount failed w/return code = -13`（S08 `Issue`）。

```bash
# 查看内核环形缓冲区中的 CIFS 记录
dmesg | grep -i cifs

# 若 dmesg 已被轮转/清空，换 messages 日志
grep -i cifs /var/log/messages
```

期望输出（形态取自 S08 `Issue`）：

```text
CIFS VFS: cifs_mount failed w/return code = -13
```

注意搜的是 `-13` 这种带负号的内核写法，而不是 `13`：内核侧与用户态的这两处数字是同一个现象的两端，只 `grep 13` 很容易漏掉（S08 `Issue`）。

```bash
# journalctl 形态——本笔记素材未收录 journalctl 的手册锚点，
# 此行仅作命令用法出现，不作为官方依据
journalctl -k --since "10 min ago" | grep -i cifs
```

#### 第二步：看同现的状态码，它决定方向

这是本章最有价值的一条：如果内核日志里同时出现 `Status code returned 0xc000006d NT_STATUS_LOGON_FAILURE`，方向就是**凭据 / 认证**，而不是网络（S08 `Issue`）。很多人看到 `13` 第一反应是去 ping 服务器，方向从第一步就错了。

> [!warning] 素材的边界
> S08 的 Issue 小节列出的是**伴随** `NT_STATUS_LOGON_FAILURE` 的情形（S08 `Issue`）。如果内核日志里只有 `cifs_mount failed w/return code = -13` 而没有这条 NT 状态码，本笔记素材没有给出进一步的官方判据——此时不要自己补一个结论，继续走第三步取证据。

#### 第三步：手工挂载与 `mount -a` 两条路径都复现

S08 的 Issue 小节记录：同一错误在手工挂载与经由 fstab / `mount -a` 两条路径上都出现（S08 `Issue`）。这条对照的意义是把两类怀疑分开：如果问题只出现在开机流程里（例如 `credentials=` 写了相对路径、`~` 未展开，见第 3 章），手工挂载会成功；两边都失败，说明问题在下发的参数本身，与「是否开机」无关。

```bash
# 路径 A：手工前台挂载，看即时输出
mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred

# 路径 B：按 fstab 走一遍，作为对照
mount -a
```

#### 第四步：`mount -vvv` 看实际下发的参数

`mount -vvv` 会打印 `Credential formatted incorrectly: (null)`，并暴露真正传给内核的参数（如 `ver=1`、`prefixpath=DOMAIN/USER`）（S08 `Issue`）。

```bash
mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred -vvv
```

期望输出（形态取自 S08 `Issue`）：

```text
Credential formatted incorrectly: (null)
...
ver=1
prefixpath=DOMAIN/USER
```

> [!example] 这两行怎么用
> `(null)` 说明凭据没有被解析出内容，`prefixpath=DOMAIN/USER` 说明域与用户名被拼进了路径——这两处都值得回头核对第 3 章的凭据文件语法限制（等号两侧不留空格；域写 `domain=SALES` 而不是 `SALES\`）。这个「回头核对」是排查动作，不是对成因的官方解释：S08 记录的是输出形态本身（S08 `Issue`，并见 S03 `Login errors`）。

### 4.2 errno 名称↔数值对照

在解读任何数字之前先钉死前提：本笔记能确证的只有**符号名↔数值**的硬对应，来自内核 uapi 头文件（S15 `errno-base.h` / `errno.h`）。`mount.cifs(8)` 全文没有任何「`mount error` 后面的数字 = errno 数字」的映射表；本轮素材收集中，cifs-utils 源码的三次抓取均被 HTTP 429 拒绝（02 §六.1）。因此**下文所有数值解读都写作「按 errno 推断」**，不写成官方定义。

| 符号名 | 数值 | 语义 | 来源 |
| --- | --- | --- | --- |
| `ENOENT` | 2 | No such file or directory（无此文件或目录） | S15（硬对应）／S14（语义） |
| `EACCES` | 13 | Permission denied（权限不足） | S15／S14 |
| `EHOSTDOWN` | **112** | Host is down（主机已关闭） | S15／S14 |
| `EHOSTUNREACH` | **113** | No route to host（无路由到主机） | S15／S14 |
| `EINPROGRESS` | **115** | Operation now in progress（操作正在进行） | S15／S14 |
| `EREMOTEIO` | 121 | Remote I/O error（远端 I/O 错误） | S15／S14 |

> [!warning] 112 与 113 不是同一个符号
> `EHOSTDOWN` 是 **112**，`EHOSTUNREACH` 是 **113**（S15）。两个数字相邻、字面相近，是本章最容易记错的一处：把 112 读成「no route to host」会把排查方向带到路由上，而它对应的名称是「host is down」。挂载日志里出现 112 或 115 时，请一律按 errno 推断来表述，并回到 4.1 的第一步取 `dmesg` 证据（02 §八）。

为什么 `errno(3)` 明确不列数值？因为同一个符号名在不同 UNIX 系统与架构上的编号并不相同，手册只保证名称与语义，把数值交给各平台的头文件（S14 `Error numbers and names`）。这也是「背数字」在本主题里格外不可靠的原因。

> [!tip] 大白话
> 把 `mount error(13)` 想成小区保安对你说「你不能进」。这句话只说明**被拒绝**，完全没说清是「你证件不对」（认证问题）还是「门根本锁着」（网络问题）。所以别看到 13 就去 ping 服务器，先去门卫室（`dmesg`）翻当天的登记本，看保安写下的理由是哪一条；登记本上那句 `NT_STATUS_LOGON_FAILURE`，才是「证件不对」的签名。

### 4.3 方言协商的核对方法

「挂上了」不等于「用对了方言」。判断当前连接实际谈成了哪一版，要分两步：先知道默认会谈到哪，再读内核给出的实际结果。

第一步是默认值随内核变化的三档关系（S13 `vers=`）：

| 内核版本 | 未指定 `vers=` 时的行为 |
| --- | --- |
| < 4.13 | 默认 1.0 |
| 4.13 – 4.13.5 | 默认 3.0 |
| ≥ 4.13.5 | 协商 ≥ 2.1 的最高版本 |

第二步是读实际结果：挂载成功后查 `/proc/fs/cifs/DebugData`，可以确认这条连接实际协商到的 Dialect（S13 `vers=`）。

```bash
# 在内核导出的 CIFS 调试信息里找协商结果
# 字段名与取值以本机内核的实际输出为准（本笔记素材未抄录样本输出）
grep -i dialect /proc/fs/cifs/DebugData
```

什么时候才需要显式写 `vers=`？`vers=` 的取值集合是 1.0 / 2.0 / 2.1 / 3.0 / 3.02 / 3.1.1 / 3 / default，不指定即 `vers=default`（S01a `vers=`、S13 `vers=`）；换句话说，只有在服务端是老系统、协商结果不理想时，才需要手工指定（02 §五.4）。旧内核（< 4.13）默认 1.0，是常见失败根因（S13 `vers=`）。

另一头是 Windows 侧的现状：SMBv1 在 Windows 11 与 Server 2019+ 的所有 SKU 中**默认不安装**（S04 开头段）。所以「老服务端只支持 SMB1」这类假设，放到今天的 Windows 共享上基本不成立。

核对挂载本身用 `findmnt`（S17b）：

```bash
# 按挂载点逐级向上回溯查询（-T），或严格匹配挂载点（-M）
findmnt -T /mnt/share
findmnt -M /mnt/share

# 只看 cifs 类型的挂载（-t 过滤时输出会自动切为 list 格式）
findmnt -t cifs
```

判定存在性可以直接读退出码：0 表示有内容可显示，1 表示任何错误（含按过滤条件无匹配、设备或挂载点不存在）（S17b `EXIT STATUS`）。这条在脚本化的排错里比解析输出文本更稳。

### 4.4 Windows 共享连不上时的优先排查方向

优先级只有一句话：**先查签名，而不是先降协议版本**（S04 开头段、S07）。

签名强制是三档，不要合并成一句「Windows 默认要求签名」（S07 `How SMB signing works`）：

| Windows 版本 | 出站签名 | 入站签名 |
| --- | --- | --- |
| Windows 11 24H2 企业版 / 专业版 / 教育版 | 要求 | 要求 |
| Windows Server 2025 | 要求 | 不要求 |
| Windows 11 24H2 家庭版 | 不要求 | 不要求 |

按 S07 的细粒度表述读这张表：Server 2025 要求的是**出站**签名，不要求入站（02 §四.6）。如果只记得「Win11 24H2 / Server 2025 默认要求签名」这种粗粒度说法（S04 开头段），很容易误判方向。

签名机制本身是把整条消息的哈希写入 SMB 头，用于防中继与欺骗（S07 `How SMB signing works`）。当 Linux 客户端连的是不支持签名的第三方 SMB 服务器时，会报 `0xc000a000` / `STATUS_INVALID_SIGNATURE`；**改协议版本不能绕过**（S07 `SMB signing behavior`、S04 开头段）。处置方向是在远端服务器启用签名，而不是关掉客户端签名或降协议（02 §五.10、S04 开头段）——微软明确反对用关闭协议版本或签名来绕过连接失败（S04 开头段）。

在 Windows 侧确认客户端是否要求签名：

```powershell
# Windows PowerShell：查看客户端签名要求（True 即启用）
Get-SmbClientConfiguration | FL RequireSecuritySignature
```

（S07 `Verify SMB signing status`）

还有一条容易漏的连带效应：要求签名会**同时禁用来宾访问**，来宾路径可能报 `0x80070035`（S07 `Disable SMB signing`、`SMB signing behavior`）。也就是说，你在 4.1 里用 `smbclient -N` 能列出的匿名共享，未必能被 Windows 客户端以同样方式访问。

> [!note] 引用 S04 时的版本标注
> S04 页面标注为 2025-03-12；02 记录的探测阶段（`ms.date` 2025-02-28 / updated 2026-09-08）与深读阶段（2025-03-12）两处日期不一致，本章引用一律以页面实际标注的 2025-03-12 为准（02 §四.7）。

### 4.5 两条必须写明的未闭环

排错这一章有两处**不能闭环**，写清楚比补一个漂亮结论更有用。

**其一：`mount error(N)` 的数字是否直接等于 errno。** 未证实。`mount.cifs(8)` 全文没有映射表；cifs-utils 源码三次抓取都被 HTTP 429 拒绝（02 §六.1）。本笔记因此把「`mount.cifs` 直接打印 errno」标为 `[推断]`——能写的是「数值与 errno 的对应关系」，判断时以同现的内核日志为准（S08 `Issue`），不靠数字本身。

**其二：红帽 KB 的 Resolution 步骤在订阅墙后**，不可读（02 §六.2）。本章只引用其 Issue / Environment 可见小节（S08），不补写墙后的处置步骤。

### 4.6 常见坑

> [!warning] 排错时最容易踩的四处
> - **看到 13 就去查网络**：先看内核日志里同现的状态码，`NT_STATUS_LOGON_FAILURE` 指向凭据/认证（S08 `Issue`）。
> - **把 112 记成 `EHOSTUNREACH`**：112 是 `EHOSTDOWN`，`EHOSTUNREACH` 是 113（S15）。
> - **把 errno 数值当官方映射表背**：`errno(3)` 明确不列数值，因为同一符号名在不同 UNIX/架构上编号不同（S14 `Error numbers and names`）。
> - **Windows 连不上先降 `vers=`**：签名才是优先方向，且 `STATUS_INVALID_SIGNATURE` / `0xc000a000` 改协议版本绕不过去（S07 `SMB signing behavior`、S04 开头段）。

### 本章小结

- 排错的主线是证据链：`dmesg` 找 `cifs_mount failed w/return code = -13` → 看同现的 NT 状态码定方向 → 手工挂载与 `mount -a` 两条路径对照 → `mount -vvv` 看实际下发参数（S08 `Issue`）。
- 数值只是节点：`ENOENT`=2、`EACCES`=13、`EHOSTDOWN`=112、`EHOSTUNREACH`=113、`EINPROGRESS`=115、`EREMOTEIO`=121 是硬对应；112 与 113 不是同一个符号，且一切数值解读都按 errno 推断（S15、S14、02 §六.1）。
- 方言要核对而不是猜：默认协商随内核三档变化（<4.13 → 1.0；4.13–4.13.5 → 3.0；≥4.13.5 → 协商 ≥2.1），挂载后读 `/proc/fs/cifs/DebugData` 看实际 Dialect（S13 `vers=`）。
- Windows 连不上先查签名：三档强制粒度不同（Server 2025 要求出站、不要求入站），`0xc000a000` 的处置在远端服务器开签名，不是降协议版本（S07、S04 开头段）。
- 两处不闭环要记住：`mount error(N)` 是否直接等于 errno 仍是推断（源码抓取被 429 拒绝），红帽 KB 的 Resolution 在订阅墙后、本章不补写（02 §六.1、§六.2）。

到这一章为止，共享都挂在宿主机上。如果真正要用这个共享的是容器里的服务，问题会变成另一个样子——下一章（可选小节）把 Docker 论坛里的社区经验摆出来，并给出比「给容器加权限」更稳妥的两条替代路径。

### 本章来源

- **S08** → `mount error(13)` 的证据链四步（`dmesg`/messages 的 `cifs_mount failed w/return code = -13`、同现的 `NT_STATUS_LOGON_FAILURE`、手工挂载与 `mount -a` 双路径复现、`mount -vvv` 的 `Credential formatted incorrectly: (null)` 与 `ver=1`/`prefixpath=DOMAIN/USER`）；红帽 KB 的 Issue 小节。
- **S15** → errno 名称↔数值硬对应表（2/13/112/113/115/121）；112 与 113 非同一符号的易错点。
- **S14** → `errno(3)` 明确不列数值的原因（跨 UNIX/架构编号不同）；表中语义列。
- **S13** → 协商默认随内核变化的三档关系、`vers=` 取值集合、`/proc/fs/cifs/DebugData` 确认 Dialect。
- **S01a** → `vers=` 取值集合与「未指定即 `vers=default`」（与 S13 并列引用）。
- **S17a** → `smbclient -L` / `-N` / `-I` 用法、`posix_whoami` 判定匿名身份。
- **S17b** → `findmnt -T` / `-M` / `-t cifs` 用法与退出码语义（0 = 有内容，1 = 任何错误）。
- **S07** → 签名强制三档粒度、签名机制、`STATUS_INVALID_SIGNATURE` / `0xc000a000`、签名与来宾访问的关联、`Get-SmbClientConfiguration | FL RequireSecuritySignature`。
- **S04** → SMBv1 在 Windows 11 / Server 2019+ 默认不安装；微软反对用关协议/关签名绕过连接失败；页面日期标注 2025-03-12。
- **S03** → 凭据文件语法限制（`Login errors` 小节，作为 `mount -vvv` 输出后的核对方向）。

## 第五章：容器内挂载

如果真正要读这个共享的是容器里的服务（下载器、媒体库之类），第一反应往往是在容器里也 `mount` 一次。这一小节只做一件事：把这条路上的社区经验摆出来，说明它为什么不稳，以及更稳妥的两条替代路径。

> [!warning] 整章来源层级：社区经验
> 本章唯一来源 S12 是 Docker 论坛帖（2018-12-19 起帖，续帖至 2026-01-07）；02 §一 与 §三.3 末行明确「无 Docker 官方 capability 说明」，且帖内说法互相矛盾。以下全部为社区经验，不构成官方结论，也不给出「需要哪些 capability」的确定清单。

### 5.1 容器内直接挂载 CIFS：现象与争议

帖内被反复尝试的是「给容器加 capability 后直接挂载」。并列呈现两种说法，本章不作裁决（S12）：

- 有报告称即便给了 `SYS_ADMIN` 与 `DAC_READ_SEARCH`，容器内挂载仍然失败并报 `mount error 13`（S12）。
- 另一条路径是使用 `--privileged`：有报告称该做法可行，但它在帖内被版主反对（S12）。

```bash
# 形式示意：容器内直接挂载的尝试形态（社区帖中的做法，非本笔记推荐方案）
# 全部标社区经验，无 Docker 官方依据
docker run --cap-add SYS_ADMIN --cap-add DAC_READ_SEARCH \
  -v /host/path:/container/path myimage
```

（S12，社区经验）

两种说法之所以互相矛盾，是因为它们来自不同环境下的个案：02 §六.6 记录，Docker 官方对容器内挂载所需的 capability **没有任何说明**，只有论坛经验且说法互相矛盾。因此本章不写「需要哪些 capability」的清单，也不把 `--privileged` 当默认方案——它在 S12 中被版主反对（S12）。

### 5.2 更稳妥的替代路径

帖内给出的两条稳妥路径，方向都与「在容器里加权限」相反：把挂载留在宿主机（S12）。

1. **宿主机挂载 + bind mount**：先在宿主机按第 2、3 章把共享挂到某个挂载点，再把这个挂载点以 `-v` 的形式绑进容器。容器内不需要任何额外 capability，权限问题也回到宿主机这一层来解（S12）。
2. **本地驱动 named volume**：用本地驱动的 named volume 承载数据，而不是在容器内直接挂远端共享（S12）。

```bash
# 更稳妥路径的形式示意：宿主机先挂好，再 bind 进容器（社区经验）
# 宿主机侧：mount -t cifs //server/share /mnt/share -o credentials=/root/.smbcred
docker run -v /mnt/share:/data myimage
```

（S12，社区经验）

> [!note] 本小节的定位
> 以上结论均为社区经验（S12），生产环境请自行验证；它不是 Docker 官方口径。

### 本章小结

- 容器内直接挂载 CIFS 在社区帖里说法互相矛盾：`SYS_ADMIN` + `DAC_READ_SEARCH` 仍可能报 `mount error 13`，`--privileged` 可行但被版主反对（S12）。
- Docker 官方对所需 capability 没有任何说明，本笔记不给确定清单（02 §六.6、S12）。
- 更稳妥的两条路是宿主机挂载 + bind mount，以及本地驱动 named volume（S12）。

> [!note] 本章为可选小节
> 本章删去不影响第 1–4 章的连贯性。

### 本章来源

- **S12** → 容器内直接挂载 CIFS 的两种矛盾说法（`SYS_ADMIN` + `DAC_READ_SEARCH` 仍失败并报 `mount error 13`；`--privileged` 可行但被版主反对）、两条替代路径（宿主机挂载 + bind mount、本地驱动 named volume）。

## 附录：来源总表

本表汇总第 1–5 章「本章来源」小节中列出的全部来源（去重）；层级与版本/日期取自 `02_deep_research.md` §二「来源总表」，仅作合并，不新增来源、不改写来源描述。

| SID | 层级 | 版本 / 日期 | 涉及章节 |
| --- | --- | --- | --- |
| S01a | official | cifs-utils **2:7.4-1**，页面更新 2025-06-12 | 第 1、2、3、4 章 |
| S01b | official | cifs-utils **2:7.0-2**，页面更新 2022-08-26 | 第 2、3 章 |
| S02 | official | systemd **252.36** / **257.13** / **262~rc3** | 第 3 章 |
| S03 | official | **页面无版本/日期标注** | 第 3、4 章 |
| S04 | official | 页面标注 **2025-03-12**（探测阶段记录为 ms.date 2025-02-28 / updated 2026-09-08，**两处不一致，写作以页面实际标注为准**） | 第 1、2、4 章 |
| S05 | official | 标 2024-04-18，**正文含 2008/9.04/12.04 遗留** | 第 2、3 章 |
| S06 | official | scraped 2026-09-18 | 第 1、2、3 章 |
| S07 | official | ms.date 2025-08-13（updated 2025-09-15） | 第 2、4 章 |
| S08 | official | 2025-12-03，**Resolution 正文在订阅墙后** | 第 4 章 |
| S09 | secondary | 2024-06-29，**原帖无任何回复** | 第 3 章 |
| S10 | community | 2026-01-12 | 第 2、3 章 |
| S11 | community | n/a | 第 2 章 |
| S12 | community | 2018-12-19（续帖至 2026-01-07） | 第 5 章 |
| S13 | official | 手册自述对应 cifs vfs 2.18（≈ Linux 5.0） | 第 1、2、4 章 |
| S14 | official | n/a | 第 4 章 |
| S15 | official | 内核源码 master | 第 4 章 |
| S16 | 历史一手 | **2007**，对 SMB3.1.1/NFSv4.2 已过时 | 第 1 章 |
| S17a | official | Samba **4.17.12**（2023-10-10）／ **4.22.8**（2026-02-19），两版相关段落逐字一致 | 第 2、4 章 |
| S17b | official | util-linux 2.43.devel-1062-f，2026-08-03 | 第 2、3、4 章 |
