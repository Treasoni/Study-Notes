---
title: SMB/CIFS 挂载到 Linux · 第 2 册 手动挂载
tags:
  - SMB
  - CIFS
  - Linux
  - 挂载
  - cifs-utils
  - NAS
  - 飞牛FNOS
  - Windows
  - 实战笔记
  - SMB挂载
created: 2026-09-18
updated: 2026-09-18
status: 已完成
source_project: smb-cifs-mount-linux
series: SMB/CIFS 共享文件夹挂载到 Linux 服务器
volume: 2/5
---

# 第二章：手动挂载：从零到挂上

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-01-协议选型]] ｜ 下一册：[[SMB挂载-03-凭据与开机自动挂载]]

这一章要把共享真正挂到你的 Debian/Ubuntu 服务器上，并且让你说得清每一个选项在干什么、它的边界在哪里。我们不从 fstab 开始——那是第 3 章的事。先把命令在手动模式下跑通、跑懂，再谈持久化，否则开机挂载失败时你连该怀疑哪个选项都不知道。

## 2.1 前置：`cifs-utils` 与版本基线

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

## 2.2 挂载前先探测（推荐）

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

## 2.3 最小可用挂载命令

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

## 2.4 选项语义逐项

这一节是本章的核心。每个选项都给出「它管什么 / 什么条件下才生效 / 边界在哪」，而不是只给一句「加上就好了」。

### 2.4.1 属主与权限：`uid`/`gid`、`forceuid`/`forcegid`、`perm`/`noperm`

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

### 2.4.2 mode 类选项：`file_mode`/`dir_mode`、`fmask`/`dmask`、`mapposix`

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

### 2.4.3 字符集：`iocharset`

- `iocharset` 未指定时使用**内核构建时的 `nls_default`**（S01a `iocharset`）。
- 如果**服务器不支持 Unicode**，该参数不生效（S01a `iocharset`）。

```bash
# 中文文件名乱码时的常用写法
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

> [!tip] 大白话
> 字符集这事像**两个人对暗号**：`iocharset=utf8` 是你这边声明「我按 UTF-8 解读文件名」。但如果对面压根不用 Unicode 那套编码传名字，你这边声明的暗号再标准也没用——man page 明说了服务器不支持 Unicode 时该参数不生效（S01a `iocharset`）。所以乱码排查不能只盯着本地这一个参数。

### 2.4.4 协议版本：`vers=`

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

### 2.4.5 安全与加密：`sec=`、`seal`

- `sec=` 默认值有明确分界：内核 **< 3.8 为 `ntlm`；≥ 3.8 为 `ntlmssp`**（S01a `sec=`、S13 `sec=`）。
- `seal` 请求 SMB 层加密（AES-128-CCM），**需要 SMB3+ 才可用**（S13 `seal`）。

```bash
# 要求 SMB 层加密（前提：协商到 SMB3 及以上）
sudo mount -t cifs //server/share /mnt/share \
  -o credentials=/root/.smbcred,sec=ntlmssp,seal
```

### 2.4.6 文件系统类型：`smb3` 与 `mount.smb3`

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

### 2.4.7 本章有意不展开的选项

`serverino`/`noserverino`：man page 原文**只说「默认启用」**，没有给「什么情况下该改用 `noserverino`」的建议（`02_deep_research.md` §六.10）。所以此处标「**原文未给建议**」，不展开——与其编一个使用场景，不如告诉你这个问题的答案不存在于现有材料里。

## 2.5 三个落地例

### 2.5.1 Windows 共享

挂载侧的命令与上面 2.3 完全一致，差别只在**服务端前置条件**：

- Windows 侧要存在你连接的用户账号，且该账号对该共享有访问权。
- Windows 11 与 Server 2019+ 的 SMBv1 **默认不安装**（S04 开头段），别指望降版本能解决连通性问题。
- 若连接失败且报 `STATUS_INVALID_SIGNATURE` / `0xc000a000`，问题方向是**签名**，排查方法见第 4 章 4.4（S04、S07）。

```bash
# Windows 共享：命令形态与通用写法一致
sudo mount -t cifs //winhost/docs /mnt/share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

**Windows 侧两个值的查法**（`username` / `domain`）：在 cmd 里跑 `whoami` 与 `echo %USERDOMAIN%`。`whoami` 输出形如 `DESKTOP-ABC\smbuser`，反斜杠后面那半截是 `username=`；`echo %USERDOMAIN%` 的输出是 `domain=`。三个键的完整对照见第 3 册 3.1.1。

### 2.5.2 飞牛 FNOS 共享

> [!warning] 整段为社区经验，不写默认值
> FNOS 侧的默认方言、SMB1 状态、签名默认值**无任何官方文档**，`02_deep_research.md` §一、§六.5 明确归入「只能标为社区经验 / 未经一手证实」。以下内容来自社区帖 S10 / S11，**仅作社区经验**，本段不写任何默认方言值。

社区帖 S10 给出的做法是：fstab 中写一行 `cifs`，含 `iocharset`/`uid`/`gid`/`file_mode`/`dir_mode`，再配合 `mount -a` 与 `@reboot` 延迟补挂（S10，[社区]）。**它的凭据部分是反面示例：密码明文写进了 fstab**（S10，[社区]）。

我们引用它只是为了说明「有人这么干过」，**不复制它的凭据写法**——正确做法见第 3 章 3.1 与 3.3。

S11（飞牛官方论坛）提供的是 Linux 挂载 FNOS 共享时的路径写法与权限排查讨论（S11，[社区]）。同样只作社区经验参考。

**FNOS 侧的凭据怎么填**：`username` 填 FNOS 后台建的共享用户（不是 NAS 管理员账号），`domain` 填后台「文件服务 / SMB」里的工作组名。对照表见第 3 册 3.1.1——注意该小节的这两条是实操惯例，本笔记未为它们挂来源。

### 2.5.3 Home Assistant 的 Samba share 插件

Home Assistant OS 装上 `Samba share` 插件之后，HA 本身就是一台 SMB 服务器。挂载侧命令与 2.3 完全一致，要改的只有插件侧那几项（S18a、S18b）。

| 插件选项 | 默认值 | 对应到挂载侧 |
| --- | --- | --- |
| `username` | `homeassistant` | 凭据文件的 `username=` |
| `password` | 无（必填） | 凭据文件的 `password=` |
| `workgroup` | `WORKGROUP` | 凭据文件的 `domain=` |
| `enabled_shares` | 七项全开 | 决定 `//IP/共享名` 里存在哪些路径 |
| `allow_hosts` | 见下方警告块 | 决定你的客户端**能不能连上** |
| `compatibility_mode` | `false` | 一般不用动 |

插件文档特别说明：插件的用户名与密码**与 Home Assistant 的登录账号没有任何关系**（S18b `Options`）——别把 HA 登录密码填进去。

`enabled_shares` 的合法值由正则限定，旧名 `addons` / `addon_configs` 仍被接受（S18a `enabled_shares`）。文档里各共享对应的内容如下（S18b `Sharing`）：

| 共享名 | 里面是什么 | 建议 |
| --- | --- | --- |
| `share` | 插件与 HA 之间共享的数据 | 想往服务器上放文件就留它 |
| `media` | 本地媒体文件 | 按需 |
| `backup` | 备份文件 | 按需（体积大，不建议自动挂载） |
| `config` | 整个 Home Assistant 配置目录 | 不建议长期挂载 |
| `ssl` | SSL 证书（含私钥） | 不建议长期挂载 |
| `local_apps` | 本地插件（旧名 `addons`） | 不做插件开发就移除 |
| `app_configs` | 插件的配置文件（旧名 `addon_configs`） | 不做插件开发就移除 |

旧名与新名**同时暴露、指向同一目录**；**从列表里移除的共享将不可访问**（S18b `Sharing`、`enabled_shares`）。`config` 与 `ssl` 等于把运行中的 HA 配置和私钥挂成一块可写网络盘，除非明确需要，不要长期挂着。

> [!warning] `allow_hosts` 是这个场景独有的坑
> 它是 schema 里的**必填项**，语义是「允许访问共享的主机/网络列表」，默认值为 `10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`、`169.254.0.0/16`、`fe80::/10`、`fc00::/7`（S18a、S18b `allow_hosts`）。
> **挂载端 IP 不在这几段里会被直接拒绝**，现象是连不上，而不是挂载参数不对——所以先查这一项，再回头读错误码（第 4 章 4.6）。
> 常见家庭网段 `192.168.x.x` 与 `10.x.x.x` 已在默认值内，无需改动；服务器若在别的网段（例如 `100.64.0.0/10` 这类默认列表之外的地址），必须显式加上。
> 不要图省事改成 `0.0.0.0/0`：那等于把 HA 的配置目录向整个网络敞开。

**`compatibility_mode` 保持关闭。** 文档对它的原文是：开启后会启用旧版 Samba 协议，"might solve issues with some clients that cannot handle the newer protocols, however, it lowers security"，并建议 "Only use this when you absolutely need it and understand the possible consequences"（S18b `compatibility_mode`）。客户端是 Linux 内核的 `cifs.ko`，默认协商到 SMB 2.1+，用不上它；只有方言协商失败时才临时开来验证一次（方言排查见第 4 章 4.3）。

```bash
# HA 的 Samba 插件：把共享名换成 enabled_shares 里的项即可
sudo mount -t cifs //192.168.1.10/share /mnt/ha-share \
  -o credentials=/root/.smbcred,uid=1000,gid=1000,iocharset=utf8
```

## 2.6 挂载后核对：实际协商到哪一版方言

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

## 2.7 常见坑

> [!warning] 手动挂载的四个高频坑
> 1. **共享名加了尾随 `/`**：`//SERVER/share/` 不工作（S06 `Manual mounting`）。
> 2. **密码含逗号却写在 `-o password=`**：会被逗号解析掉。改用凭据文件 / `PASSWD` 环境变量 / 交互输入（S01a `BUGS`）。
> 3. **指望 `forceuid` 顺带改掉 mode**：做不到，没有任何选项能覆盖 mode（S01a `FILE AND DIRECTORY OWNERSHIP AND PERMISSIONS`）。
> 4. **以为 `file_mode`/`dir_mode` 总是生效**：它们只在服务器不支持 CIFS Unix extensions 时才用于覆盖默认 mode（S01a `file_mode=`）；而且它们的默认数值在现有 man page 中**根本没有记载**（`02_deep_research.md` §六.7）。

## 本章小结

- 版本基线：cifs-utils **7.4-1**（trixie）/ **7.0-2**（bookworm）；差异是实打实的，例如 `credentials=` 文件键（S01a / S01b `credentials=`）。
- 最小可用命令是 `mount -t cifs //服务器/共享名 /挂载点 -o credentials=...,uid=...,gid=...,iocharset=utf8`；共享名不能加尾随 `/`（S06 `Manual mounting`）。
- 属主与权限：`uid`/`gid` 默认 0 且只在服务器不给属主时生效；`forceuid`/`forcegid` 强制覆盖属主，但**没有选项能覆盖 mode**；`noperm` 关闭客户端权限检查会让本机其他用户也能访问（S01a）。
- `file_mode`/`dir_mode` 仅在服务器不支持 CIFS Unix extensions 时生效，**默认数值无来源**；`fmask`/`dmask` 的「已废弃」说法来自 2008 年旧资料，现版 man page 无该条目（S01a `file_mode=`、S05、`02_deep_research.md` §四.1）。
- 方言：默认协商随内核分三档（< 4.13 → 1.0；4.13–4.13.5 → 3.0；≥ 4.13.5 → ≥2.1 最高版本）；挂载后读 `/proc/fs/cifs/DebugData` 才是确认手段（S13 `vers=`）。
- 探测与核对：挂载前 `smbclient -L //server -N`，挂载后 `findmnt -M /mnt -t cifs`（S17a、S17b）。

下一章把密码从命令行里挪走，写进凭据文件与 `/etc/fstab`，并解决那个真正让人熬夜的问题：服务器没开机时，服务器自己的开机流程该怎么办。

## 本章来源

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
| S18a | HA Samba 插件的选项名与默认值（`allow_hosts` 白名单、`enabled_shares` 合法值）；2.5.3 |
| S18b | HA Samba 插件的选项语义、共享名清单、兼容模式原文、凭据与 HA 登录无关；2.5.3 |
| S13 | `vers=` 三档协商默认；`seal`；`smb3` fstype 与 `mount.smb3`；`/proc/fs/cifs/DebugData` |
| S17a | `smbclient -L` 探测、`-N`、`-A`、`posix_whoami`、NetBIOS 名说明 |
| S17b | `findmnt -T`/`-M`/`-t` 与退出码语义 |

> 标注说明：2.5.2 全段为 `[社区]`（S10/S11）；2.4.2 的 `mapposix` 为 `[推断]`；`file_mode`/`dir_mode` 默认数值、2.4.7 的 `serverino` 使用建议为 `[缺口]`；2.4.2 的 `fmask`/`dmask` 争议按 §四.1 并列呈现，未写成官方结论。

## 相关笔记

- [[Linux的文件系统结构]] —— 先看懂「挂载点」在本机文件系统里是什么，再理解 CIFS 挂载点属主的特殊性
- [[linux磁盘相关的知识]] —— 分区、格式化与 mount 的基础语义
- [[linux的文件权限]] —— 本地 `chown`/`chmod` 的直觉，与 CIFS 挂载点权限规则的差异对照
- [[软路由教程/飞牛安装配置iStoreOS旁路由]] —— 飞牛 FNOS 作为共享端的环境背景（本册 2.5.2 的 FNOS 例子）

---

> 🧭 分册导航 ｜ 总目录：[[SMB挂载-00-总目录]] ｜ 上一册：[[SMB挂载-01-协议选型]] ｜ 下一册：[[SMB挂载-03-凭据与开机自动挂载]]
