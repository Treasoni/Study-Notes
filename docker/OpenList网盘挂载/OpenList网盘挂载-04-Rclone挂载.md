---
title: OpenList 网盘挂载 · 第 4 册 用 Rclone 挂到本地
tags:
  - Docker
  - OpenList
  - WebDAV
  - Rclone
  - 网盘
  - 实战笔记
  - OpenList网盘挂载
created: 2026-09-12
updated: 2026-09-13
status: 已完成
source_project: openlist-webdav-rclone-docker
series: OpenList → WebDAV → Rclone → Docker 全链路实战
volume: 4/6
---

# 第 4 章 用 Rclone 挂到本地

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-03-WebDAV服务]] ｜ 目录：[[OpenList网盘挂载-00-总目录]] ｜ 下一册：[[OpenList网盘挂载-05-Docker映射]]

第 3 章结束时，我们手里只有一份**连接参数表**——Url 形如 `http[s]://your-domain:port/dav/`、Path 填 `dav`、账号即网页端账号密码。那份参数表从没被真正"打"过一次，第 3 章也明确把**端点验证**推到了本章：只有当真有一个客户端去连它，你才知道端口、路径、权限三项是不是同时对了。

本章就用 Linux 官方推荐的 rclone 完成这第一次真实连接，并把它变成一台**开机就在的本地磁盘**。这是全链路里参数最多、最容易选错档的一环，请按顺序做，不要跳步。

## 4.1 概念：rclone 与 FUSE

**rclone** 是一个命令行云存储工具：用 `rclone copy`、`rclone sync` 这类命令在网络存储之间搬文件。而 `rclone mount` 是它的另一副面孔——把同一个远端**挂载成本地文件系统**，于是 `ls`、`cp`、播放器、下载器都能像访问本地目录一样访问网盘。官方定义：

> Rclone mount allows Linux, FreeBSD, macOS and Windows to mount any of Rclone's cloud storage systems as a file system with FUSE.

关键词是 **FUSE** —— Filesystem in Userspace（用户态文件系统）。内核本身只认识 ext4、xfs 这些内置文件系统；FUSE 提供了一套通用框架，让一个**普通用户进程**也能对外提供文件系统。rclone 就是这个进程：它把 WebDAV 的 HTTP 请求翻译成"目录、文件、大小、读写"这些文件系统语义。

> [!tip] 大白话：rclone 是"翻译官"，FUSE 是"标准插座"
> FUSE 就像墙上的一个标准插座：任何电器（文件系统）只要做成这个插头的形状，插上去就能通电。网盘本来不是"文件系统"，rclone 负责把它改造成能插进这个插座的样子。所以 `rclone mount` 不是把网盘"下载到本地"，而是**在本地开了一扇窗**——你看到的每个文件，读的时候才去云端取。

### FUSE 三件套与自检

FUSE 由三部分组成，缺一不可：

| 组件 | 形态 | 作用 | 缺失时的现象 |
|---|---|---|---|
| `fuse.ko` | 内核模块 | 内核侧的框架，提供 `/dev/fuse` 设备 | `mount` 报 `unknown filesystem type 'fuse'` |
| `libfuse.*` | 用户态共享库（`libfuse2` / `libfuse3`） | rclone 调用的 API 库 | rclone 起不来或提示找不到 libfuse |
| `fusermount` / `fusermount3` | 挂载工具（可执行文件） | 替非特权用户完成 `mount()` 系统调用 | 报 `fusermount: executable file not found in $PATH` |

先做一次自检，确认三件套齐了：

```bash
# 内核模块（有输出即已加载；没有可 modprobe fuse 后再试）
lsmod | grep fuse

# 用户态库
ldconfig -p | grep libfuse

# 挂载工具（FUSE2 与 FUSE3 可能只有一个，也可能都在）
which fusermount fusermount3

# 若上面都没输出，按发行版安装（Debian/Ubuntu 系）
sudo apt install fuse3
```

预期结果：`lsmod` 能看到 `fuse`；`ldconfig` 能看到 `libfuse.so.2` 或 `libfuse3.so.3`；`which` 至少给出一个绝对路径。**这个路径要记住**，4.6 节的 systemd 会依赖它。

> [!tip] 为什么普通用户也能挂载
> `mount()` 是特权操作，普通用户本不该调用。FUSE 的做法是引入一个 **setuid root** 的辅助程序 `fusermount` 代劳。代价是必须防止挂载者借这个能力提权，所以 fusermount 对非特权挂载**总是**自动加上两个选项：`nosuid`（挂载点里的 setuid 程序执行时不生效）和 `nodev`（挂载点里的设备文件不被当真设备打开）。这两条不用你手写，知道它默认存在就行。

## 4.2 名词对齐与环境边界

动手之前先统一三个词，后面会反复出现：

| 术语              | 含义                                             | 本章具体指                                     |
| --------------- | ---------------------------------------------- | ----------------------------------------- |
| remote（远端）      | rclone 配置里的一条连接，名字由你起                          | `openlist:`，指向 `http://<宿主机IP>:5244/dav/` |
| mountpoint（挂载点） | 本机上一个**已存在且为空**的目录                             | `/mnt/openlist`                           |
| VFS             | rclone 在远端对象存储与本地文件系统之间加的一层适配，含内存目录缓存与可选磁盘文件缓存 | 决定 `--vfs-cache-mode` 那一堆行为               |

> [!warning] 环境边界：本册命令一律以 Linux 宿主机为准
> 你本机是 Windows + Git Bash，所以上述命令请在 **WSL / NAS / 远程 Linux 宿主机**上执行——Git Bash 里没有 `fusermount`，也没有 FUSE 内核模块，`rclone mount` 无法按本文方式工作。Windows 侧 rclone mount 走的是 **WinFsp**（另一套机制），不在本册范围内。
>
> 官方明确标注为**不支持 Windows** 的参数包括 `--allow-other`、`--allow-root`、`--allow-non-empty`、`--uid`、`--gid`、`--umask`。如果你在 Windows 上照样抄 `--allow-other`，它不会报错也不会生效，属于"静默失效"，尤其难查。

## 4.3 配置远端：把第 3 章的参数写进 rclone

配置里有**两件事必须做对**：URL 要指到 `/dav/`，密码必须被 obscure。
### 1. 安装 rclone 与挂载依赖 fuse3

运行安装命令：

Bash

```
sudo apt update && sudo apt install -y rclone fuse3
```

_在提示输入密码时输入你的 Ubuntu 用户密码（输入时屏幕不会显示字符，直接输完按回车即可）。_

### 2. 验证安装

安装完成后，查看版本号以验证是否成功：

Bash

```
rclone version
```

**验证标准**：如果终端输出了类似 `rclone v1.60.x...` 的版本信息，说明安装成功。
### 方式一：交互式 `rclone config`（推荐首次使用）

`rclone config` 是一个**问答式配置向导**：你不用手写配置文件，它问什么你答什么，答完自动把结果写进 `~/.config/rclone/rclone.conf`。

先建立一个关键认知：**这不是一段要你"看懂"的程序输出，而是一次交互对话。** 转录里绝大多数行是程序打印给你的**菜单**（不要照抄），只有结尾是 `>` 的那几行才是**等你输入**的地方。

#### 完整示范（已填入真实值）

假设 OpenList 跑在 `192.168.1.10`、账号是 `admin`，一次成功的会话长这样（`←` 后面是讲解，实际屏幕不会显示）：

```text
$ rclone config
No remotes found, make a new one?
n/s/q> n                              ← 新建一条连接
name> openlist                        ← 起名；后面命令与 systemd 都写成 openlist:
Storage> webdav                       ← 连接类型
url> http://192.168.1.10:5244/dav/    ← 换成你的真实 IP，结尾 /dav/ 不能少
vendor> 7                             ← 即 other，理由见下
user> admin                           ← 网页登录 OpenList 的账号
y/g/n> y                              ← 我自己输密码
Enter the password:                   ← 盲打密码，屏幕上不显示任何字符
Confirm the password:                 ← 再盲打一遍
```

打完回车后**什么都不显示、直接回到 shell 提示符** —— 这就是成功，配置已经落盘。

#### 逐行对照：哪行是提示、你要输入什么

| 屏幕上显示的（程序打印，别照抄）                    | 你要输入的                               | 为什么                                                             |
| ----------------------------------- | ----------------------------------- | --------------------------------------------------------------- |
| `No remotes found, make a new one?` | —                                   | 只是提示：目前一条连接都没有                                                  |
| `n) New remote`                     | **`n`**                             | ⚠️ 这里的 `n` 是 **New（新建）**，不是"否"                                  |
| `name> openlist`                    | **`openlist`**                      | 连接名，随便起；**后面的命令与 systemd 都用它**，写作 `openlist:`                   |
| `Type of storage to configure.`     | **`webdav`**                        | 列表很长（中间 `[snip]` 是官方原文的省略标记），`webdav` 藏在里面；**直接输单词，不用输编号**      |
| `url> http://<宿主机IP>:5244/dav/`     | **`http://192.168.1.10:5244/dav/`** | ⚠️ `<宿主机IP>` 是占位符，**必须换成自己的真实 IP**                              |
| `vendor> 7`                         | **`7`**（或 `other`）                  | 对端是哪套 WebDAV 软件，OpenList 不属于前 6 类，只能选最后一档                       |
| `user> <OpenList 用户名>`              | **`admin`**                         | ⚠️ 同样是占位符，换成网页登录 OpenList 的账号                                   |
| `y/g/n> y`                          | **`y`**                             | `y` = 自己输密码；`g` = 让 rclone 随机生成；`n` = 不设                        |
| `Enter the password:`               | **你的密码**                            | ⚠️ **屏幕上不显示任何字符**（连 `*` 都没有），这是 Linux 密码输入的正常行为，**不是卡住**，盲打完按回车 |
| `Confirm the password:`             | **再打一遍**                            | 同上，确认没打错                                                        |

#### 收尾还有几问

官方转录到 `Confirm the password:` 就截断了，实际会话还会再问两三次（具体行文以你装的版本为准）：

| 提示 | 你输入 | 含义 |
|---|---|---|
| `Edit advanced config?` | **`n`** | 是否进高级项，本章用不到 |
| `y) Yes this is OK` | **`y`** | 把生成的配置打印一遍让你确认，其中密码显示为 `*** ENCRYPTED ***` |
| `e/n/d/r/c/s/q>`（回到主菜单） | **`q`** | 退出配置向导 |

> [!warning] 三处必须与第 3 章对齐
> - `url` 的**端口必须与网页端完全一致**（第 3 章的硬约束），结尾要带 `/dav/`；
> - `user` / `password` 就是网页端登录账号密码，不需要单独建 WebDAV 账号；
> - `vendor` 选 **`7 / Other site/service or software`**（即 `other`），理由见下。

#### 完成后验证

```bash
# 能看到配置内容（密码应是一串密文，不是你的明文）
cat ~/.config/rclone/rclone.conf

# 或只列连接名，应输出 openlist:
rclone listremotes
```

填错了不必重来：向导主菜单里的 `e) Edit existing remote` 可以改已有连接。

#### 官方原文转录（供对照，可跳过）

（`[snip]` 是官方原文自带的省略标记。）

```text
$ rclone config
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n
name> openlist
Type of storage to configure.
Choose a number from below, or type in your own value
[snip]
XX / WebDAV
   \ "webdav"
[snip]
Storage> webdav
URL of http host to connect to
Choose a number from below, or type in your own value
 1 / Connect to example.com
   \ "https://example.com"
url> http://<宿主机IP>:5244/dav/
Name of the WebDAV site/service/software you are using
Choose a number from below, or type in your own value
 1 / Fastmail Files
   \ (fastmail)
 2 / Nextcloud
   \ (nextcloud)
 3 / Owncloud
   \ (owncloud)
 4 / Sharepoint Online, authenticated by Microsoft account
   \ (sharepoint)
 5 / Sharepoint with NTLM authentication, usually self-hosted or on-premises
   \ (sharepoint-ntlm)
 6 / rclone WebDAV server to serve a remote over HTTP via the WebDAV protocol
   \ (rclone)
 7 / Other site/service or software
   \ (other)
vendor> 7
User name
user> <OpenList 用户名>
Password.
y) Yes type in my own password
g) Generate random password
n) No leave this optional password blank
y/g/n> y
Enter the password:
password:
Confirm the password:
password:
```

### 方式二：直接写 `rclone.conf`

配置文件默认在 `~/.config/rclone/rclone.conf`（Linux）。一段可直接使用的片段：

```ini
[openlist]
type = webdav
url = http://<宿主机IP>:5244/dav/
vendor = other
user = <OpenList 用户名>
pass = <obscure 后的密码>
```

字段的名字与必填性来自 rclone 官方 WebDAV 文档：

| 键 | 官方字段名 | 必填 | 说明 |
|---|---|---|---|
| `url` | `--webdav-url` | **是** | 要连接的 http host 的 URL |
| `vendor` | `--webdav-vendor` | 否 | 声明对端是哪套 WebDAV 实现，用来开启额外特性 |
| `user` | `--webdav-user` | 否 | 用户名 |
| `pass` | `--webdav-pass` | 否 | **必须 obscure** |
| `bearer_token` | `--webdav-bearer-token` | 否 | 用令牌替代账号密码 |

`pass` 的官方原文提示是：**Input to this must be obscured - see rclone obscure.** 两种生成方式：

- 走上面的交互式 `rclone config`，它会在你输入明文后自动存成密文，回显为 `pass: *** ENCRYPTED ***`；
- 或者手写配置前先用 obscure 命令生成密文串，再粘到 `pass =` 后面：

```bash
rclone obscure '<你的明文密码>'
# 把输出的密文串整段填进 rclone.conf 的 pass = 后面
```

> [!warning] 不要把明文密码直接写进 `pass =`
> 官方要求该字段输入必须经过 obscure。直接填明文，rclone 会把它当成一段**密文**去解密，得到的是乱码密码——现象就是无论账号多正确都 401，而且报错完全不会提示你"密码没加密"。这是本章最容易卡住的一个假故障。

### 为什么 `vendor` 填 `other`

`vendor` 的官方取值有八档：

| 取值 | 对应系统 |
|---|---|
| `fastmail` | Fastmail Files |
| `nextcloud` | Nextcloud |
| `owncloud` | Owncloud 10 PHP based WebDAV server |
| `infinitescale` | ownCloud Infinite Scale |
| `sharepoint` | Sharepoint Online，Microsoft 账号认证 |
| `sharepoint-ntlm` | 使用 NTLM 认证的 Sharepoint，通常自建或本地部署 |
| `rclone` | rclone 自己 `serve webdav` 提供的 WebDAV 服务 |
| `other` | Other site/service or software |

OpenList 是自己实现的 WebDAV 服务，不属于 `fastmail` / `nextcloud` / `owncloud` / `infinitescale` / `sharepoint` / `sharepoint-ntlm` 中的任何一类，也不是 rclone 自己 serve 出来的，因此只能落在最后一档 `other`。

代价是 rclone 会按**普通 WebDAV** 对待它，而普通 WebDAV 缺两样东西：

| 能力 | 普通 WebDAV（含 OpenList） | Fastmail / ownCloud / Nextcloud |
|---|---|---|
| 修改时间（mtime） | **不支持** | 支持 |
| 哈希（SHA1 / MD5） | **不支持** | 支持 |
| rclone 判断"文件有没有变" | 只能靠大小等有限信息 | 大小 + mtime + hash |

这直接影响 `rclone sync` / `copy` 这类命令的准确性：没有 mtime 与 hash，两端文件大小相同而内容不同时，rclone 可能判断不出差异。对"挂载起来当本地盘用"（本章目标）影响较小，但如果你打算用同一个 remote 做定期同步备份，就要知道这个先天短板。

## 4.4 先验证再挂载：用 `rclone ls` 探端点

第 3 章之所以把端点验证推到这里，是因为只有客户端能给出可观察的结果。rclone 提供了非挂载的读取命令，正好当探针用：

```bash
# 列出远端顶层目录（只列目录，最轻量）
rclone lsd openlist:

# 列出远端所有文件
rclone ls openlist:

# 把本地目录拷上去（写入方向的验证，可选）
rclone copy /home/source openlist:backup
```

**这一步是本章的分水岭**，请按症状对照：

| 现象 | 最可能的原因 | 回查章节 |
|---|---|---|
| `401 Unauthorized` | `pass` 填了明文没 obscure；或用户权限项没开齐 | 本章 4.3 / 第 3 章权限项 |
| `403 Forbidden` | 只开了 `WebDAV 管理` 没开读写所需的具体权限项 | 第 3 章 |
| `404 Not Found` | `url` 少了或错写成别的路径，未指向 `/dav/` | 第 3 章连接参数表 |
| 连不上 / 超时 | 端口与网页端不一致，或防火墙 | 第 3 章 |
| 能列出但看不到第 2 章挂的目录 | OpenList 用户 `Base path` 限制了可见范围 | 第 2 章 |

只要 `rclone lsd openlist:` 能打印出你在第 2 章挂进来的存储目录名，第 3、4 章之间那条断口就接上了。**先过这一步，再碰 mount**——不要跳过验证直接装 systemd，否则后面出问题时分不清是权限、端点还是挂载配置的锅。

## 4.5 挂载

### 挂载点必须是"已存在且为空"的目录

官方对挂载点的要求是 `/path/to/local/mount` 必须是一个 **empty existing** directory —— 注意是**两个条件同时成立**：目录要先存在（`mkdir`），而且里面是空的。常见报错正是把这两条搞混。

```bash
# 先建空目录（/mnt 归 root，建完把属主改成自己，之后才能用普通用户挂载，不一定要用这，只是这个路径适合服务器后台服务）
sudo mkdir -p /mnt/openlist
sudo chown "$USER" /mnt/openlist

# 确认它是空的（应无输出）
ls -A /mnt/openlist

# 最简挂载（前台）
rclone mount openlist: /mnt/openlist
```

`openlist:` 后面不带路径表示挂载整个远端根；也可以只挂某个子目录，写成 `openlist:子目录`。如果你确实需要挂到一个非空目录，rclone 提供了 `--allow-non-empty`，但它会让原有内容被挂载**遮蔽**（不是把文件合并进去），能不用就不用。
**1. `openlist:` 和 `openlist:子目录` 是什么区别？**

这决定了你挂载出来的**目录层级**：

- **`openlist:`（后面不加东西）**：
    - 把 OpenList 的**全部内容**都挂出来。
    - 你打开本地文件夹，第一层看到的是 `夸克网盘` 这个文件夹；以后如果你在 OpenList 里又添加了百度网盘、阿里云盘，它们也会并排显示在里面。
- **`openlist:夸克网盘/影视`（指定某个子路径）**：
    - **只挂载这一层**。
    - 你打开本地文件夹，直接看到的就是《星际穿越》、《头号玩家》等视频文件，跳过了外面的“夸克网盘”文件夹，适合专门给影视播放器当专用媒体库。

### 前台还是后台

- **默认前台**：命令会占住当前终端，这时另开一个窗口去做 `ls`。按 `Ctrl+C`（或收到 SIGINT / SIGTERM）时挂载会自动停止。
- **`--daemon` 强制后台**：主程序启动子进程维护挂载，等到就绪或超时后自行退出。

后台模式的代价是**必须手动卸载**：

```bash
# 后台模式下的卸载（按系统上安装的是哪个 fusermount 二选一）
fusermount -u /mnt/openlist
# …或
fusermount3 -u /mnt/openlist
# macOS，或 Linux 上使用 nfsmount 时
umount /mnt/openlist
```

> [!warning] 卸载可能失败：挂载点忙
> 如果挂载点正在被使用（有进程在里面读写），`umount` 会失败，此时需要你自己先停掉占用进程。排查时先 `lsof +D /mnt/openlist` 看谁占着。

### 本章主坑：`--vfs-cache-mode` 四档选型

这是全章最容易选错、也最影响体感的一个参数。官方默认值是 **`off`**，但默认值不等于推荐值——官方在 Limitations 里直说：

> Without the use of `--vfs-cache-mode` this can only write files sequentially, it can only seek when reading. This means that many applications won't work with their files on an rclone mount without `--vfs-cache-mode writes` or `--vfs-cache-mode full`.

四档的定位一句话概括：**档位越高，兼容性越好，占磁盘越多。**

| | `off`（默认） | `minimal` | `writes` | `full` |
|---|---|---|---|---|
| 只读文件 | 直连远端 | 直连远端 | 直连远端 | 缓存到磁盘 |
| 只写 / 读写文件 | 直连远端 | 缓冲到磁盘 | 缓冲到磁盘 | 缓冲到磁盘 |
| 读+写同时打开 | ❌ | ✅ | ✅ | ✅ |
| 写时 seek | ❌ | ❌ | ✅ | ✅ |
| 上传失败重试 | ❌ | ❌ | ✅（指数递增，最长 1 分钟） | ✅ |
| 磁盘占用 | 无 | 最小 | 中 | 可能很大 |
| 稀疏文件依赖 | 无 | 无 | 无 | **有**（FAT/exFAT 不行） |
| 适用 | 只读为主 | 小磁盘 + 读写同开 | **日常写入推荐** | 读多、要快、磁盘充足 |

各档要点：

- **`off`**：读写都直连远端，磁盘占用为 0。代价是一组操作被明确禁掉：不能同时以读写方式打开、以写方式打开不能 seek、已存在文件以写方式打开必须带 `O_TRUNC`、`O_APPEND` / `O_TRUNC` 被忽略，以及最伤的一条——**上传失败不能重试**（一次网络抖动就可能导致写失败且不自动补偿）。适合只读为主、或写入量小且能容忍偶发失败、且磁盘紧张的场景。
- **`minimal`**：只为"读写同开"兜底，是**磁盘占用最小**的兼容性改善，不解决 seek，也不解决上传重试。
- **`writes`**：只读文件仍**直连远端**（省磁盘，代价是读没加速），只写 / 读写文件先缓冲到磁盘；**支持全部常规文件系统操作**，且**上传失败会按指数递增间隔重试，最长到 1 分钟**。对"挂载给下载器 / 媒体库做写入"的常见用途，这一档通常是**性价比最优解**。
- **`full`**：读写全部落盘，连**读**过的文件也缓存，第二次读走本地，播放 / 重复读取体验最好；代价是磁盘占用可能很大，读时会预读 `--buffer-size`（内存）+ `--vfs-read-ahead`（磁盘）字节。缓存文件是**稀疏文件**——一个 10GB 视频只读了开头，`ls -l` 显示 10GB，实际磁盘占用可能只有几十 MB。

> [!warning] `full` 专属警告：缓存目录不能放在 FAT/exFAT 上
> 不是所有文件系统都支持稀疏文件，**FAT/exFAT 就不支持**。缓存目录落在这种文件系统上，rclone 表现会非常差并记录一条 ERROR 日志。所以用 `full` 之前先确认 `--cache-dir` 落在 ext4 / xfs / btrfs 这类文件系统上——很多 U 盘、SD 卡、部分外置硬盘出厂就是 FAT/exFAT。

> [!tip] 大白话：四档像"门口暂存筐的大小"
> `off` = 不放筐，快递直接塞门缝，掉了就掉了（失败不重试）；`minimal` = 放个小筐，只接"边读边写"的件；`writes` = 放个正常筐，所有写件先落筐、失败还能重投；`full` = 干脆把整间屋当仓库，连读过的件也存一份，取第二次特别快，但屋子必须是**结实的地板**（支持稀疏文件），放在烂地板（FAT/exFAT）上反而会塌。

本章建议的推进方式：**先用 `off` 把挂载本身跑通**（确认路径、权限、端点都对），确认无误后再按用途调到 `writes` 或 `full`。第一次挂载就上 `full`，会把"挂载失败"和"缓存目录选错"两类问题混在一起，很难定位。

### 关键默认值速查

调参前先知道起点在哪：

| 参数 | 默认值 | 一句话说明 |
|---|---|---|
| `--vfs-cache-mode` | `off` | 四档选型，见上 |
| `--vfs-cache-max-age` | `1h0m0s` | 按**最后访问时间**淘汰缓存中的对象 |
| `--vfs-cache-poll-interval` | `1m0s` | 检查缓存是否过期的间隔 |
| `--vfs-cache-max-size` | `off`（不限制） | 缓存总大小上限 |
| `--vfs-write-back` | `5s` | 文件关闭且 5 秒未被访问后才回写远端 |
| `--dir-cache-time` | `5m0s` | 目录条目缓存时长 |
| `--poll-interval` | `1m0s` | 轮询远端变更的间隔，**必须小于 `--dir-cache-time`** |
| `--attr-timeout` | `1s` | 内核缓存文件属性的时长 |
| `--uid` / `--gid` | `1000` / `1000` | 覆盖文件系统报告的 uid/gid（Windows 不支持） |
| `--umask` | `002` | 覆盖权限位（Windows 不支持） |
| `--file-perms` | `666` | 文件权限 |
| `--dir-perms` | `777` | 目录权限 |
| `--daemon-wait` | `1m0s` | 后台模式下等待挂载就绪的最长时间 |
| `--transfers`（全局） | `4` | 使用写缓存时，从缓存并行上传的文件数 |

其中三条值得单独提醒：

- **`--vfs-cache-max-age` 按访问时间算，不是入缓存时间。** 访问一次，1 小时的计时就重置一次。
- **`--vfs-cache-max-size` 可能被超出。** 它只每 `--vfs-cache-poll-interval` 检查一次，而且"打开中的文件不能被淘汰"（open files cannot be evicted from the cache），实际占用可能高于你设的上限。
- **写缓存的并行度看 `--transfers`，不是 `--checkers`。** 使用 `writes` / `full` 时，全局 `--transfers` 决定从缓存并行上传的数量，而 `--checkers` 对 VFS **没有影响**。调上传并发时改错参数会白忙一场。

文件回写时机也值得记一句：文件只在**被关闭**、且**连续 `--vfs-write-back` 秒未被访问**时才回写远端；如果 rclone 在此期间退出或被杀，未上传的文件会在下次以**相同参数**运行时继续上传。

### 两条风险要主动隔离

**风险一：多实例共用 VFS 缓存可能损坏数据。** 只要 `--vfs-cache-mode` 不是 `off`，就**不要**让两个 rclone 实例用同一份缓存去操作同一个（或互相重叠的）远端，否则可能造成数据损坏。解法是给每个实例独立的缓存目录：

```bash
# 实例 A
rclone mount openlist: /mnt/openlist-a \
  --vfs-cache-mode writes --cache-dir /var/cache/rclone/instance-a

# 实例 B（即使指向同一远端，也要用不同缓存目录）
rclone mount openlist: /mnt/openlist-b \
  --vfs-cache-mode writes --cache-dir /var/cache/rclone/instance-b
```

官方补了一句"如果两个远端不重叠，就无需担心"，但实践中判断"是否重叠"很容易出错，**养成每个实例独立 `--cache-dir` 的习惯最省事**。调不通时加 `-vv` 运行，rclone 会打印文件缓存的实际位置，可以用它确认缓存到底落在哪。

**风险二：`--attr-timeout` 窗口内的截断 / 乱码。** 机制是内核会把文件属性（大小、修改时间等）缓存 `--attr-timeout` 这么久；在这段时间内如果**远端文件长度发生了变化**（比如你从网页端或另一台机器改了它），内核仍按旧长度去读，就会读到截断的尾部或末尾乱码。调大它（如 10s、1m）能减少内核对 rclone 的回调、提升效率，但**窗口越大概率越高**；默认 `1s` 是权衡后的最低有效值，不建议随意调大。反过来，如果文件不会在 rclone 控制之外发生变化，就没有损坏的可能——对稳定不改的媒体库，这个风险基本可忽略。

### 挂载与 sync/copy 的可靠性差异

理解 VFS 缓存的前提，是知道这两者根本不是一类东西：

- `rclone sync` / `copy` 是**一次性任务**：传完就走，失败就重试整块，可靠性靠"大量重试"堆出来。
- `rclone mount` 是**长期文件系统**：应用以为自己在写本地磁盘，写一半失败时，文件系统没法像同步任务那样"整块重来"——除非先把上传内容落到本地磁盘，也就是上面选的 VFS 缓存。

> [!tip] 大白话：快递 vs 自家信箱
> `sync/copy` 像**发快递**：递送失败可以退回重发，直到成功为止。`mount` 像**你家门口的投递口**：别人把信塞进来就走了，塞到一半掉地上没法"重投整封"，除非你在门口先放一个暂存筐（VFS 缓存）接住。缓存模式选得对不对，决定了这个筐有多大、能不能接住失败的投递。

## 4.6 开机自启：systemd

把 `rclone mount` 丢在终端里跑显然不能算"挂到本地"，必须交给 systemd。

### 第一步：启用 FUSE 的 `user_allow_other`

FUSE 默认只允许 root 使用 `allow_other`，这个限制可以由一个用户态配置项 `user_allow_other` 解除；该配置项写在 `/etc/fuse.conf`：

```bash
# 取消 /etc/fuse.conf 里 user_allow_other 的注释
sudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf

# 验证
grep user_allow_other /etc/fuse.conf
# 预期输出：user_allow_other
```

`allow_other` 在 OpenList 场景下为什么重要：第 5 章要把这个挂载点交给 Docker 容器，而容器里的进程 UID 往往不是你的登录用户，没有 `allow_other` 就会直接 `Permission denied`。

> [!tip] 大白话：`allow_other` 是"门禁授权"
> 默认情况下，FUSE 挂载点只对**挂载者本人**开门——就像你刷自己的工牌进自己的工位。`allow_other` 相当于给同部门的同事也发了临时工牌；但它只发给你所在这个 user namespace 及其下属小组，跨命名空间（比如容器自建的 userns）还是进不来。

### 第二步：建日志目录

服务以普通用户身份运行，写不了 `/var/log/`，改用用户自己的目录：

```bash
mkdir -p ~/.local/log
```

### 第三步：写 unit

`Type=notify` 是关键：**服务进入 started 状态的那一刻，挂载点已经就绪**。如果写成 `Type=simple`，systemd 会在进程刚起来、挂载还没完成时就算"启动成功"，此时依赖它的服务（比如第 5 章要挂载给它的容器）会看到一个空目录或直接失败。

```ini
# /etc/systemd/system/rclone-openlist.service
[Unit]
Description=rclone OpenList
AssertPathIsDirectory=/mnt/openlist
After=network-online.target

[Service]
Type=notify
User=YOUR_USER
ExecStart=/usr/bin/rclone mount --config=/home/YOUR_USER/.config/rclone/rclone.conf --vfs-cache-mode full --vfs-cache-max-age 4h --vfs-fast-fingerprint --vfs-refresh --allow-other --log-file=/home/YOUR_USER/.local/log/rclone_openlist.log --log-level INFO "openlist:" /mnt/openlist
ExecStop=/bin/fusermount3 -u /mnt/openlist
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

指令逐条说明：

| 指令 | 作用 |
|---|---|
| `Type=notify` | 挂载点就绪后服务才进入 started |
| `AssertPathIsDirectory=` | 挂载点目录不存在时服务启动失败，而不是悄悄跑空 |
| `After=network-online.target` | 等网络就绪再启动 |
| `User=YOUR_USER` | 以普通用户运行（`allow_other` 场景下的常见安排） |
| `ExecStop=` | 停止服务时手动卸载 |
| `Restart=always` / `RestartSec=10` | 挂载掉线后自动重启，间隔 10 秒 |
| `WantedBy=default.target` | 开机自启 |

其中三个参数单独解释一下：

- `--vfs-cache-max-age 4h`：缓存对象在最后一次访问后保留 4 小时；
- `--vfs-fast-fingerprint`：指纹计算时跳过快操作，**准确度略降但快得多**，能改善缓存文件的打开速度；
- `--vfs-refresh`：启动时在后台递归刷新目录缓存。

> [!warning] 两个容易写错的地方
> **① `ExecStop` 里写 `fusermount` 还是 `fusermount3` 是发行版差异。** Fedora 用 FUSE3 所以写 `fusermount3`；Debian/Ubuntu 上取决于系统装的是 FUSE2 还是 FUSE3——用 4.1 节 `which fusermount fusermount3` 的结果决定。写错名字的表现是停止服务时卸载失败，但服务本身看起来"启动了"，很容易漏查。
> **② systemd 下没有环境变量。** mount unit 运行时没有 `PATH`、`HOME`，所以 `~` 不展开，`--config`、`--cache-dir` 一律要写**绝对路径**（官方在 mount helper 一节也重复了这条）。此外 rclone 会使用回退 PATH `/bin:/usr/bin` 去找 `fusermount`，请确认 4.1 节查到的路径就落在这两个目录里。

另外，新版 Ubuntu 的 AppArmor 可能拦截挂载，报错形如 `fusermount3: mount failed: Permission denied`。官方给出的处理是 `sudo aa-disable /usr/bin/fusermount3`（可能需要先 `apt install apparmor-utils`）。禁用安全模块本身有代价，只在你确实撞上、且确认是 AppArmor 导致时才用。

### 第四步：启用并验证

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rclone-openlist.service

systemctl status rclone-openlist.service
# 预期：Active: active (running)
```

服务失败时优先直接看日志文件而不要只看 `journalctl`（信息更详细）：

```bash
cat ~/.local/log/rclone_openlist.log
```

### 附：目录缓存刷新

| 需求 | 命令 |
|---|---|
| 强制刷新**全部**目录缓存 | `kill -SIGHUP $(pidof rclone)` |
| 通过远程控制接口刷新全部 | `rclone rc vfs/forget` |
| 定向失效单个文件 / 目录 | `rclone rc vfs/forget file=path/to/file dir=path/to/dir` |

前两条都有个前提：`kill` 方式假设**只有一个 rclone 实例在跑**（`pidof rclone` 会取所有实例）；`rclone rc` 方式需要事先配置好远程控制接口。日常最常用的是 SIGHUP。

另外，`--poll-interval` **必须小于 `--dir-cache-time`**，设为 `0` 可禁用轮询，且仅对支持的 remote 有效。如果后端不支持轮询，那么"在网页端或另一台机器上做的改动"要等目录缓存过期（默认 5 分钟）才会被看到——这也是很多"目录不刷新"问题的根因。

## 4.7 章末可跑产出

完成后应当满足三条：

**1. 挂载点能 `ls` 到第 2 章挂进来的内容**

```bash
ls -l /mnt/openlist
```

看得到内容，说明这条链路真的通了：

```text
rclone 进程
  → openlist: 远端（WebDAV over HTTP）
    → OpenList /dav/ 端点
      → 用户权限项（WebDAV 读取）
        → 第 2 章挂载的存储
          → 网盘 / 本地目录
```

**2. `systemctl status` 见 `active (running)`**

因为是 `Type=notify`，看到 `running` 差不多同时意味着**挂载点已就绪**，而不只是进程活着。

**3. reboot 后自动恢复**

```bash
sudo systemctl reboot
# 重新登录后
ls -l /mnt/openlist
systemctl status rclone-openlist.service
```

若重启后没挂上，按这个顺序查：

| 症状 | 查什么 |
|---|---|
| `fusermount: executable file not found in $PATH` | `/bin` 与 `/usr/bin` 下是否有 fusermount / fusermount3 |
| 报路径找不到 | `ExecStart` 里的 `--config`（以及 `--cache-dir`，若写了）是否为绝对路径 |
| 挂载点空 / 权限拒绝 | `/etc/fuse.conf` 里的 `user_allow_other` 是否已启用 |
| `fusermount3: mount failed: Permission denied` | Ubuntu 是否被 AppArmor 拦截 |
| 启动"成功"但挂载点空 | `Type=` 是否误写成 `simple` |

## 本章小结

- `rclone mount` 用 **FUSE** 把云存储变成本地文件系统；FUSE 由内核模块 `fuse.ko`、用户态库 `libfuse.*`、挂载工具 `fusermount` 三件套组成，`fusermount` 以 setuid root 安装并对非特权挂载自动加 `nosuid` + `nodev`。
- 远端配置的关键是 `type = webdav`、**必填的 `url`**（要指到 `/dav/`，端口与网页端一致）、以及**必须 obscure 的 `pass`**；`vendor = other` 是唯一合适的一档，后果是只能按普通 WebDAV 工作——**不支持修改时间，也不支持哈希**。
- `--vfs-cache-mode` 默认 `off`，四档是本章主坑：`off` 读写直连远端、不支持读写同开、写不能 seek、上传失败**不能重试**；`writes` 支持全部常规操作并按指数间隔重试上传（最长 1 分钟）；`full` 连读也缓存、缓存是稀疏文件，**FAT/exFAT 上会性能崩并记 ERROR**。
- 两条风险要主动隔离：多个 rclone 实例共用同一远端缓存**可能损坏数据**（用 `--cache-dir` 隔离）；`--attr-timeout` 窗口内远端文件长度变化可能表现为**截断或末尾乱码**。
- systemd 集成：`Type=notify` 保证"服务 started 时挂载点已就绪"；systemd 下没有环境变量、`~` 不展开、PATH 回退到 `/bin:/usr/bin`，所以 `--config` / `--cache-dir` 必须写绝对路径。
- 本机是 Windows + Git Bash，上述命令需在 WSL / NAS / 远程 Linux 宿主机执行；`--allow-other`、`--uid`、`--umask` 等参数**不支持 Windows**。

## 相关笔记

- [[WSL-Windows子系统forLinux]] —— 本册未覆盖的 Windows / WSL 路线
- [[linux磁盘相关的知识]] —— 挂载点与文件系统的基础
- [[linux的文件权限]] —— `allow_other` 与权限问题的 Linux 侧基础

## 来源

- rclone 官方文档 — [rclone mount](https://rclone.org/commands/rclone_mount/)
- rclone 官方文档 — [WebDAV](https://rclone.org/webdav/)
- Linux 内核官方文档 — [FUSE Overview](https://docs.kernel.org/filesystems/fuse/fuse.html)
- rclone 论坛帖 — [How to mount Rclone persistently on Fedora Linux (on boot)](https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738) —— systemd unit 写法与 `/etc/fuse.conf` 路径出自这篇社区经验，非官方推荐写法

---

> 🧭 分册导航 ｜ 上一册：[[OpenList网盘挂载-03-WebDAV服务]] ｜ 目录：[[OpenList网盘挂载-00-总目录]] ｜ 下一册：[[OpenList网盘挂载-05-Docker映射]]
