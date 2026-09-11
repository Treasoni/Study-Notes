## 第 4 章 用 Rclone 挂到本地

前三章已经把 OpenList 跑起来、把网盘聚合进来、并且给用户开好了 WebDAV 权限。但到第 3 章结束时，我们手里只有一份**连接参数表**—— Url 形如 `http[s]://your-domain:port/dav/`、Path 填 `dav`、账号即网页端账号密码。那份参数表从没被真正"打"过一次，第 3 章也明确把**可脚本化的端点验证**推到了本章：因为只有当真有一个客户端去连它，你才知道端口、路径、权限三项是不是同时对了。

本章就用官方推荐的 Linux 客户端 rclone 来完成这第一次真实连接，并把它变成一台**开机就在的本地磁盘**。这是全链路里参数最多、最容易选错档的一环，请按顺序做，不要跳步。

### 4.1 核心概念：rclone 与 FUSE

rclone 本身是一个命令行云存储工具：它让你用 `rclone copy`、`rclone sync` 这类命令在网络存储之间搬文件。而 `rclone mount` 是它的另一副面孔——把同一个远端**挂载成本地文件系统**，于是 `ls`、`cp`、播放器、下载器都能像访问本地目录一样访问网盘。官方对它的定义是：

> Rclone mount allows Linux, FreeBSD, macOS and Windows to mount any of Rclone's cloud storage systems as a file system with FUSE. [^c4-1]

关键词是 **FUSE**。FUSE = Filesystem in Userspace（用户态文件系统）。内核本身只认识 ext4、xfs 这些内置文件系统；FUSE 提供了一套通用框架，让一个**普通用户进程**也能对外提供文件系统。rclone 就是这个进程——它把 WebDAV 的 HTTP 请求翻译成"目录、文件、大小、读写"这些文件系统语义。

> [!tip] 大白话：rclone 是"翻译官"，FUSE 是"接口"
> 把 FUSE 想成墙上的一个**标准插座**：任何电器（文件系统）只要做成这个插头的形状，就能插上去通电。网盘本来不是"文件系统"，rclone 就负责把它改造成能插进这个插座的样子。所以 `rclone mount` 不是把网盘"下载到本地"，而是**在本地开了一个窗**，你看到的每个文件，读的时候才去云端取。

#### FUSE 的三件套

内核文档把 FUSE 的组成写得很明确：

> FUSE is a userspace filesystem framework. It consists of a kernel module (fuse.ko), a userspace library (libfuse.*) and a mount utility (fusermount). [^c4-3]

三件套各自负责什么：

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

预期结果：`lsmod` 能看到 `fuse`；`ldconfig` 能看到 `libfuse.so.2` 或 `libfuse3.so.3`；`which` 至少给出一个 `fusermount` 或 `fusermount3` 的绝对路径。**这个路径要记住**，4.9 节的 systemd 会依赖它。

#### 为什么非特权用户也能挂载

`mount()` 是特权操作，普通用户本不该调用。FUSE 的做法是引入一个 setuid root 的辅助程序：

> Since the `mount()` system call is a privileged operation, a helper program (fusermount) is needed, which is installed setuid root. [^c4-3]

代价是必须防止挂载者借这个能力提权，于是 fusermount 对非特权挂载**总是**加上两个选项：

> to ensure this fusermount always adds "nosuid" and "nodev" to the mount options for non-privileged mounts. [^c4-3]

- `nosuid`：挂载点里就算放了 setuid 程序，执行时也不生效；
- `nodev`：挂载点里就算出现设备文件，也不会被当作真设备打开。

这两条你不需要手动写，是 fusermount 自动加的；知道它存在，是为了理解后面"为什么挂载点里的脚本不能靠 setuid 提权"这类问题。

#### FUSE 默认不检查权限

这一点首次接触会很反直觉：FUSE **默认不做权限检查**，而把访问策略交给文件系统自己实现——

> By default FUSE doesn't check file access permissions, the filesystem is free to implement its access policy or leave it to the underlying file access mechanism (e.g. in case of network filesystems). [^c4-3]

rclone 挂载的"文件系统"实现方是 rclone 自己，背后真正的权限判断发生在 WebDAV 服务器（也就是 OpenList 那一侧）。想让内核按文件 mode 位来拦截访问，要显式打开 `default_permissions`：

> This option enables permission checking, restricting access based on file mode. It is usually useful together with the 'allow_other' mount option. [^c4-3]

对应的 rclone 参数是 `--default-permissions`（注意名字多了连字符）。而 `allow_other` 的权威语义是：

> This option overrides the security measure restricting file access to the user mounting the filesystem. This option is by default only allowed to root, but this restriction can be removed with a (userspace) configuration option. [^c4-3]

并且它有命名空间边界：

> 'allow_other' restricts access to users in the same userns or a descendant. [^c4-3]

也就是说 `allow_other` **不是**"对所有用户开放"，而是"对同一个 user namespace 及其后代开放"。常规 Linux 宿主机上通常等价于"本机其他用户也能访问"，但如果你在用容器或自建 user namespace，就别指望它跨命名空间生效。

> [!tip] 大白话：`allow_other` 是"门禁授权"
> 默认情况下，FUSE 挂载点只对**挂载者本人**开门——就像你刷自己的工牌进自己的工位。`allow_other` 相当于给同部门的同事也发了临时工牌；但它只发给你所在这个部门（同一 userns）及其下属小组，跨部门的同事还是进不来。

`allow_other` 在 OpenList 场景下为什么重要：如果第 5 章要把这个挂载点交给 Docker 容器，容器里的进程 UID 往往不是你的登录用户，没有 `allow_other` 就会直接 `Permission denied`。

#### 环境边界（先读这段，能省下大量排查时间）

本笔记的命令一律以 **Linux 宿主机**为准。你本机是 Windows + Git Bash，所以：

- 上述命令请在 WSL / NAS / 远程 Linux 宿主机上执行；Git Bash 里没有 `fusermount`，也没有 FUSE 内核模块，`rclone mount` 无法按本文方式工作。
- Windows 侧 rclone mount 走的是 **WinFsp**（另一套机制），不在本笔记收集范围内（缺口 G4）。
- 官方明确标注为"不支持 Windows"的参数包括 `--allow-other`、`--allow-root`、`--allow-non-empty`、`--uid`、`--gid`、`--umask`。 [^c4-1] 如果你在 Windows 上照样抄 `--allow-other`，它不会报错也不会生效，属于"静默失效"，尤其难查。

### 4.2 名词对齐：远端、挂载点、VFS

在动手之前先统一三个词，后面会反复出现：

| 术语 | 含义 | 本章具体指 |
|---|---|---|
| remote（远端） | rclone 配置里的一条连接，名字由你起 | `openlist:`，指向 `http://<宿主机IP>:5244/dav/` |
| mountpoint（挂载点） | 本机上一个**已存在且为空**的目录 | `/mnt/openlist` |
| VFS | rclone 在远端对象存储与本地文件系统之间加的一层适配，含内存目录缓存与可选磁盘文件缓存 | 决定 `--vfs-cache-mode` 那一堆行为 |

### 4.3 配置远端：把第 3 章的端点写进 rclone

这是第 3 章那份参数表第一次真正接受检验的地方。rclone 的配置有两件事必须做对：**URL 要指到 `/dav/`**，**密码必须被 obscure**。

#### 方式一：交互式 `rclone config`（推荐首次使用）

官方给出的交互流程如下（此处按原文截取，`[snip]` 是原文自带的省略标记）：

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

[^c4-2]

这里有几处必须与第 3 章对齐：

- `url` 的**端口必须与网页端完全一致**（第 3 章的硬约束），结尾要带 `/dav/`；
- `user` / `password` 就是网页端登录账号密码；
- `vendor` 这里选 **`7 / Other site/service or software`**（即 `other`），理由见下。

#### 方式二：直接写 `rclone.conf`

配置文件默认在 `~/.config/rclone/rclone.conf`（Linux）。一段可直接使用的片段：

```ini
[openlist]
type = webdav
url = http://<宿主机IP>:5244/dav/
vendor = other
user = <OpenList 用户名>
pass = <obscure 后的密码>
```

字段的**名字与必填性**来自 rclone 官方 WebDAV 文档 [^c4-2]：

| 键 | 官方字段名 | 必填 | 说明 |
|---|---|---|---|
| `url` | `--webdav-url` | **Required: true** | "URL of http host to connect to." |
| `vendor` | `--webdav-vendor` | Required: false | 声明对端是哪套 WebDAV 实现，用来开启额外特性 |
| `user` | `--webdav-user` | Required: false | 用户名 |
| `pass` | `--webdav-pass` | Required: false | **必须 obscure** |
| `bearer_token` | `--webdav-bearer-token` | Required: false | 用令牌替代账号密码 |

`pass` 的官方原文提示是：

> **NB** Input to this must be obscured - see rclone obscure. [^c4-2]

两种生成方式：

- 走上面的交互式 `rclone config`，它会在你输入明文后自动存成密文，回显为 `pass: *** ENCRYPTED ***`；
- 或者手写配置前先用 obscure 命令生成密文串，再粘到 `pass =` 后面：

```bash
rclone obscure '<你的明文密码>'
# 把输出的密文串整段填进 rclone.conf 的 pass = 后面
```

> [!warning] 不要把明文密码直接写进 `pass =`
> 官方要求该字段输入必须经过 obscure。直接填明文，rclone 会把它当成一段**密文**去解密，得到的是乱码密码——现象就是无论账号多正确都 401，而且报错完全不会提示你"密码没加密"。这是本章最容易卡住的一个假故障。

#### `vendor` 为什么填 `other`（这是推断，写清理由）

`vendor` 的官方取值表如下 [^c4-2]：

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

**推断过程**：OpenList 是自己实现的 WebDAV 服务，不属于 fastmail、nextcloud、owncloud、infinitescale、sharepoint、sharepoint-ntlm 中的任何一类，也不是 rclone 自己 serve 出来的。因此只能落在最后一档 `other`。

> [!note] 这是推断，不是官方结论
> `vendor` 的**取值列表**和"`other` = 其他站点/服务/软件"这句话是 rclone 官方定义（S07）。但"**OpenList 应该填 `other`**"这个结论，是本章根据取值表与 OpenList 的实现性质做的推断——没有一份官方文档写着"OpenList 配 rclone 时 vendor 填 other"。推断依据充分，但它属于编排层结论。

#### 这个 `vendor` 选择带来的实际后果（重要）

选 `other` 意味着 rclone 会按**普通 WebDAV**对待它，而普通 WebDAV 缺两样东西：

> Plain WebDAV does not support modified times. [^c4-2]

> Likewise plain WebDAV does not support hashes, however when used with Fastmail Files, ownCloud or Nextcloud rclone will support SHA1 and MD5 hashes. [^c4-2]

翻译成后果：

| 能力 | 普通 WebDAV（含 OpenList） | Fastmail / ownCloud / Nextcloud |
|---|---|---|
| 修改时间（mtime） | **不支持** | 支持 |
| 哈希（SHA1 / MD5） | **不支持** | 支持 |
| rclone 判断"文件有没有变" | 只能靠大小等有限信息 | 大小 + mtime + hash |

这直接影响 `rclone sync` / `copy` 这类命令的准确性：没有 mtime 与 hash，rclone 在两端文件大小相同但内容不同时可能判断不出差异。对"挂载起来当本地盘用"（本章目标）影响较小，但如果你打算用同一个 remote 做定期同步备份，就要知道这个先天短板。

#### 另一个默认值：`--webdav-auth-redirect`

> If the server redirects rclone to a new domain when it is trying to read a file then normally rclone will drop the Authorization: header from the request. [^c4-2]

官方默认是 `false`（即**默认丢弃** `Authorization:` 头）。这是标准安全实践——避免把凭据发给未知域名。如果你遇到读取文件时莫名 `401 Unauthorized`，官方给的排查方向就是这个选项；但注意开启它同时允许凭据经明文 HTTP 发送：

> Note that enabling this also permits sending your credentials over a plaintext HTTP connection if the server redirects from HTTPS to HTTP, which rclone otherwise refuses to do. [^c4-2]

对本章的内网 http 直连场景，一般保持默认即可；真出现读取 401 再按需打开。

### 4.4 兑现第 3 章的欠账：先用 `rclone ls` 验证端点

第 3 章之所以把端点验证推到这里，是因为只有客户端能给出可观察的结果。rclone 提供了非挂载的读取命令，正好当探针用——官方示例 [^c4-2]：

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
| `401 Unauthorized` | `pass` 填了明文没 obscure；或用户权限项没开齐 | 本章 4.3 / 第 3 章 权限项 |
| `403 Forbidden` | 只开了 `WebDAV 管理` 没开读写所需的具体权限项 | 第 3 章 |
| `404 Not Found` | `url` 少了或错写成别的路径，未指向 `/dav/` | 第 3 章 连接参数表 |
| 连不上 / 超时 | 端口与网页端不一致，或防火墙 | 第 3 章 |
| 能列出但看不到第 2 章挂的目录 | OpenList 用户 `Base path` 限制了可见范围 | 第 2 章 |

只要 `rclone lsd openlist:` 能打印出你在第 2 章挂进来的存储目录名，第 3、4 章之间那条断口就接上了。**先过这一步，再碰 mount**——不要跳过验证直接装 systemd，否则后面出问题时分不清是权限、端点还是挂载配置的锅。

### 4.5 第一次挂载：`rclone mount` 的基本语义

#### 挂载点必须是"已存在且为空"的目录

官方对挂载点的要求：

> On Linux/macOS/FreeBSD start the mount like this, where `/path/to/local/mount` is an **empty** **existing** directory. [^c4-1]

注意是**两个条件同时成立**：目录要先存在（`mkdir`），而且里面是空的。常见报错正是把这两条搞混——目录不存在、或者目录里已经有文件。

```bash
# 先建空目录（/mnt 归 root，建完把属主改成自己，之后才能用普通用户挂载）
sudo mkdir -p /mnt/openlist
sudo chown "$USER" /mnt/openlist

# 确认它是空的（应无输出）
ls -A /mnt/openlist

# 最简挂载（前台）
rclone mount openlist: /mnt/openlist
```

如果你确实需要挂到一个非空目录，rclone 提供了 `--allow-non-empty`（"Allow mounting over a non-empty directory"）；但它会让原有内容被挂载**遮蔽**，不是把文件合并进去，能不用就不用。

`openlist:` 后面不带路径表示挂载整个远端根；也可以只挂某个子目录，写成 `openlist:子目录`。

#### 前台还是后台

> On Linux and macOS, you can run mount in either foreground or background (aka daemon) mode. Mount runs in foreground mode by default. Use the `--daemon` flag to force background mode. On Windows you can run mount in foreground only, the flag is ignored. [^c4-1]

- **默认前台**：命令会占住当前终端。这时另开一个窗口去做 `ls`。按 `Ctrl+C`（或收到 SIGINT / SIGTERM）时挂载会自动停止。
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

[^c4-1]

> [!warning] 卸载可能失败：挂载点忙
> 官方提醒：如果挂载点正在被使用（有进程在里面读写），`umount` 会失败，此时需要你自己先停掉占用进程。排查时先 `lsof +D /mnt/openlist` 看谁占着。

#### mount 与 sync/copy 的可靠性差异（理解 VFS 缓存的前提）

这是本章最该先建立的一个认知，官方专门写了一节：

> File systems expect things to be 100% reliable, whereas cloud storage systems are a long way from 100% reliable. The rclone sync/copy commands cope with this with lots of retries. However rclone mount can't use retries in the same way without making local copies of the uploads. [^c4-1]

- `rclone sync` / `copy` 是**一次性任务**：传完就走，失败就重试整块，可靠性靠"大量重试"堆出来。
- `rclone mount` 是**长期文件系统**：应用以为自己在写本地磁盘，写一半失败时，文件系统没法像同步任务那样"整块重来"——除非先把上传内容落到本地磁盘（也就是 4.6 节要选的 VFS 缓存）。

> [!tip] 大白话：快递 vs 自家信箱
> `sync/copy` 像**发快递**：递送失败可以退回重发，直到成功为止。`mount` 像**你家门口的投递口**：别人把信塞进来就走了，塞到一半掉地上没法"重投整封"，除非你在门口先放一个暂存筐（VFS 缓存）接住。缓存模式选得对不对，决定了这个筐有多大、能不能接住失败的投递。

### 4.6 本章主坑：`--vfs-cache-mode` 四档选型

这是全章最容易选错、也最影响体感的一个参数。官方默认值是 **`off`**：

```text
--vfs-cache-mode CacheMode    Cache mode off|minimal|writes|full (default off)
```

[^c4-1]

要注意：`off` 是默认值不等于"推荐值"。官方在 Limitations 里直说：

> Without the use of `--vfs-cache-mode` this can only write files sequentially, it can only seek when reading. This means that many applications won't work with their files on an rclone mount without `--vfs-cache-mode writes` or `--vfs-cache-mode full`. [^c4-1]

四档的定位一句话概括：**档位越高，兼容性越好，占磁盘越多。**

#### `off`（默认）：读写都直连远端

> In this mode (the default) the cache will read directly from the remote and write directly to the remote without caching anything on disk. [^c4-1]

代价是一组明确被禁掉的操作 [^c4-1]：

> - Files can't be opened for both read AND write
> - Files opened for write can't be seeked
> - Existing files opened for write must have O_TRUNC set
> - Files open for read with O_TRUNC will be opened write only
> - Files open for write only will behave as if O_TRUNC was supplied
> - Open modes O_APPEND, O_TRUNC are ignored
> - If an upload fails it can't be retried

逐条翻译成你会在什么时候撞上：

| 限制 | 实际含义 | 谁会被坑 |
|---|---|---|
| 不能同时以读写方式打开 | 一个文件不能"边读边改" | 需要随机改字的编辑器、数据库文件 |
| 以写方式打开不能 seek | 只能顺序往下写，不能跳位置回改 | 几乎所有需要"改写中间一段"的程序 |
| 已存在文件以写方式打开必须带 `O_TRUNC` | 不能"只改写一部分"，只能整体截断重写 | 增量修改类工具 |
| `O_APPEND` / `O_TRUNC` 被忽略 | 追加模式不按你预期走 | 日志追写类程序 |
| **上传失败不能重试** | 一次网络抖动可能导致写失败且不自动补偿 | 弱网环境下的任何写操作 |

"上传失败不能重试"是 `off` 最伤的一条，呼应 4.5 节讲的 mount 与 sync/copy 的可靠性差异。

**`off` 适合谁**：只读为主、或写入量小且能容忍偶发失败、且磁盘空间紧张的场景。它磁盘占用为 0。

#### `minimal`：只为"读写同开"兜底

> This is very similar to "off" except that files opened for read AND write will be buffered to disk. This means that files opened for write will be a lot more compatible, but uses the minimal disk space. [^c4-1]

仍不可用的操作 [^c4-1]：

> - Files opened for write only can't be seeked
> - Existing files opened for write must have O_TRUNC set
> - Files opened for write only will ignore O_APPEND, O_TRUNC
> - If an upload fails it can't be retried

结论：**磁盘占用最小**的兼容性改善，只解决"读写同时打开"，不解决"上传重试"，也不解决 seek。适合"磁盘很小、又要跑一个边读边写的程序"的边缘场景。

#### `writes`：日常推荐档

> In this mode files opened for read only are still read directly from the remote, write only and read/write files are buffered to disk first. [^c4-1]

> This mode should support all normal file system operations. [^c4-1]

> If an upload fails it will be retried at exponentially increasing intervals up to 1 minute. [^c4-1]

三句话对应三个关键点：

1. **只读文件仍直连远端**——省磁盘，代价是读没加速；
2. **支持全部常规文件系统操作**——兼容性问题基本消失；
3. **上传失败会按指数递增间隔重试，最长到 1 分钟**——把 `off` 那条最伤的限制补上了。

对"挂载给下载器/媒体库做写入"的常见用途，这一档通常是**性价比最优解**：既有完整兼容性，又不会把整个远端的数据都拖到本地磁盘。

#### `full`：全部落盘，读也缓存

> In this mode all reads and writes are buffered to and from disk. When data is read from the remote this is buffered to disk as well. [^c4-1]

> In this mode the files in the cache will be sparse files and rclone will keep track of which bits of the files it has downloaded. [^c4-1]

两个必须理解的特性：

- **读也缓存**：第二次读同一文件走本地，播放/重复读取体验最好；代价是磁盘占用可能很大。读时会预读 `--buffer-size` 加 `--vfs-read-ahead` 字节，其中前者在内存、后者在磁盘。
- **缓存文件是稀疏文件**：只下载了一部分时，缓存文件"看起来是完整大小，实际只占已下载部分的磁盘"。比如一个 10GB 视频只读了开头，`ls -l` 显示 10GB，实际磁盘占用可能只有几十 MB。

**重要警告（`full` 专属）**：

> **IMPORTANT** not all file systems support sparse files. In particular FAT/exFAT do not. [^c4-1]

后果官方也写明了：如果缓存目录所在文件系统不支持稀疏文件，**rclone 表现会非常差，并会记录一条 ERROR 日志**。所以：**不要把 `--cache-dir` 放在 FAT/exFAT（比如很多 U 盘、SD 卡、部分外置硬盘的出厂格式）上**。用 `full` 之前先确认缓存目录落在 ext4 / xfs / btrfs 这类支持稀疏文件的文件系统上。

> [!tip] 大白话：四档像"门口暂存筐的大小"
> `off` = 不放筐，快递直接塞门缝，掉了就掉了（失败不重试）；`minimal` = 放个小筐，只接"边读边写"的件；`writes` = 放个正常筐，所有写件先落筐、失败还能重投；`full` = 干脆把整间屋当仓库，连读过的件也存一份，取第二次特别快，但屋子必须是**结实的地板**（支持稀疏文件），放在烂地板（FAT/exFAT）上反而会塌。

#### 四档对照速查

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

本章建议的推进方式：**先用 `off` 把挂载本身跑通**（确认路径、权限、端点都对），确认无误后再按用途调到 `writes` 或 `full`。第一次挂载就上 `full`，会把"挂载失败"和"缓存目录选错"两类问题混在一起，很难定位。

### 4.7 关键默认值速查

以下默认值均来自 rclone mount 官方文档 [^c4-1]，调参前先知道起点在哪：

| 参数 | 默认值 | 一句话说明 |
|---|---|---|
| `--vfs-cache-mode` | `off` | 四档选型，见 4.6 |
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

- **`--vfs-cache-max-age` 按访问时间算，不是入缓存时间。** 官方原文：它"is based on access time, not on when the file was first added to the cache"；访问一次，1 小时的计时就重置一次。
- **`--vfs-cache-max-size` 可能被超出。** 因为它只每 `--vfs-cache-poll-interval` 检查一次，而且"open files cannot be evicted from the cache"——打开中的文件不能被淘汰，所以实际占用可能高于你设的上限。
- **写缓存的并行度看 `--transfers`，不是 `--checkers`。** 官方明确：使用 `writes`/`full` 时全局 `--transfers` 决定从缓存并行上传的数量，而 "the related global flag --checkers has no effect on the VFS"。调上传并发时改错参数会白忙一场。

文件回写时机也值得记一句：官方说文件只在**被关闭**、且**连续 `--vfs-write-back` 秒未被访问**时才回写远端；如果 rclone 在此期间退出或被杀，未上传的文件会在下次以**相同参数**运行时继续上传。

### 4.8 两条风险提示

#### 风险一：多实例共用 VFS 缓存可能损坏数据

> You **should not** run two copies of rclone using the same VFS cache with the same or overlapping remotes if using `--vfs-cache-mode > off`. This can potentially cause data corruption if you do. [^c4-1]

也就是说，只要 `--vfs-cache-mode` 不是 `off`，就**不要**让两个 rclone 实例用同一份缓存去操作同一个（或互相重叠的）远端。官方给的解法是隔离缓存目录：

> You can work around this by giving each rclone its own cache hierarchy with `--cache-dir`. [^c4-1]

落地做法：给每个实例一个独立的缓存目录。

```bash
# 实例 A
rclone mount openlist: /mnt/openlist-a \
  --vfs-cache-mode writes --cache-dir /var/cache/rclone/instance-a

# 实例 B（即使指向同一远端，也要用不同缓存目录）
rclone mount openlist: /mnt/openlist-b \
  --vfs-cache-mode writes --cache-dir /var/cache/rclone/instance-b
```

官方补了一句"如果两个远端不重叠，就无需担心"，但实践中判断"是否重叠"很容易出错，**养成每个实例独立 `--cache-dir` 的习惯最省事**。顺带一提，`-vv` 运行时 rclone 会打印文件缓存的实际位置，调不通时可以用它确认缓存到底落在哪。

#### 风险二：`--attr-timeout` 窗口内的截断 / 乱码

> You may see corruption if the remote file changes length during this window. It will show up as either a truncated file or a file with garbage on the end. With `--attr-timeout 1s` this is very unlikely but not impossible. [^c4-1]

机制：内核会把文件属性（大小、修改时间等）缓存 `--attr-timeout` 这么久；在这段时间内如果**远端文件长度发生了变化**（比如你从网页端或另一台机器改了它），内核仍按旧长度去读，就会读到截断的尾部或末尾乱码。

调大 `--attr-timeout`（如 10s、1m）能减少内核对 rclone 的回调、提升效率，但**窗口越大概率越高**。默认 `1s` 是官方权衡后的最低有效值，不建议随意调大。官方也给了安心的前提："如果文件不会在 rclone 控制之外发生变化，就没有损坏的可能"——所以对稳定不改的媒体库，这个风险基本可忽略。

### 4.9 系统集成：systemd 与开机自启

把 `rclone mount` 丢在终端里跑显然不能算"挂到本地"，必须交给 systemd。但这里要先说清一个**来源层级问题**。

> [!warning] 缺口 G3：官方没有 systemd 页面
> rclone 官方文档里**没有**一篇"如何写 systemd unit 做开机自启"的教程。官方在 mount 文档里只提供了一小块 systemd **相关能力说明**（`Type=notify`、环境变量缺失、PATH 回退），其余部分——`AssertPathIsDirectory=`、`Restart=always`、`ExecStop=` 怎么写——本章只能来自一篇社区帖（S10，**T3 社区经验**）。下面的 unit 是**社区经验**，不是官方推荐写法。

#### 官方能背书的部分：`Type=notify`

> When running rclone mount as a systemd service, it is possible to use Type=notify. In this case the service will enter the started state after the mountpoint has been successfully set up. Units having the rclone mount service specified as a requirement will see all files and folders immediately in this mode. [^c4-1]

这就是把 unit 写成 `Type=notify` 的意义：**服务进入 started 状态的那一刻，挂载点已经就绪**。如果写成 `Type=simple`，systemd 会在进程刚起来、挂载还没完成时就算"启动成功"，此时依赖它的服务（比如第 5 章要挂载给它的容器）会看到一个空目录或直接失败。社区帖也持同样观点 [^c4-4]，但**这条判断的权威依据是 S06 官方**，不是社区帖。

#### 官方能背书的部分：systemd 下没有环境变量

> Note that systemd runs mount units without any environment variables including `PATH` or `HOME`. This means that tilde (`~`) expansion will not work and you should provide `--config` and `--cache-dir` explicitly as absolute paths via rclone arguments. Since mounting requires the `fusermount` or `fusermount3` program, rclone will use the fallback PATH of `/bin:/usr/bin` in this scenario. Please ensure that `fusermount`/`fusermount3` is present on this PATH. [^c4-1]

三条硬约束，全部来自官方：

| 约束 | 后果 | 正确做法 |
|---|---|---|
| 没有 `PATH`、`HOME` | `~` 不展开；写 `~/.config/...` 无效 | `--config`、`--cache-dir` 一律写**绝对路径** |
| PATH 回退到 `/bin:/usr/bin` | `fusermount` 不在该路径就找不到 | 确认 `which fusermount fusermount3` 落在 `/bin` 或 `/usr/bin`（用 4.1 节的检查结果） |
| 没有任何其他环境变量 | 依赖环境变量的写法全部失效 | 所有参数在 `ExecStart` 里显式给出 |

这条约束不只在写 unit 时成立，用 rclone 当 mount helper（`mount -t rclone` / systemd `.mount` unit / `/etc/fstab`）时同样成立，官方在 mount helper 一节也重复提醒要显式提供 `config=...,cache-dir=...`。

#### 官方能背书的部分：Ubuntu 上的 AppArmor 拦截

> NOTICE: mount helper error: fusermount3: mount failed: Permission denied CRITICAL: Fatal error: failed to mount FUSE fs: fusermount: exit status 1 [^c4-1]

官方说明这可能是新版 Ubuntu 的 Apparmor 限制所致，给出的处理是 `sudo aa-disable /usr/bin/fusermount3`（可能需要先 `sudo apt install apparmor-utils`）。[^c4-1] 注意：这是官方给的**可用手段**，但禁用安全模块本身有代价，只在你确实撞上这条报错、且确认是 AppArmor 导致时才用。

#### 官方能背书的部分：目录缓存刷新

| 需求 | 命令 | 来源 |
|---|---|---|
| 强制刷新**全部**目录缓存 | `kill -SIGHUP $(pidof rclone)` | [^c4-1] |
| 通过远程控制接口刷新全部 | `rclone rc vfs/forget` | [^c4-1] |
| 定向失效单个文件 / 目录 | `rclone rc vfs/forget file=path/to/file dir=path/to/dir` | [^c4-1] |

前两条都有个前提：`kill` 方式假设**只有一个 rclone 实例在跑**（`pidof rclone` 会取所有实例）；`rclone rc` 方式需要事先配置好远程控制接口。日常最常用的是 SIGHUP。

另外，`--dir-cache-time` 与 `--poll-interval` 的关系要记牢：

> `--poll-interval duration` Time to wait between polling for changes. Must be smaller than dir-cache-time. Only on supported remotes. Set to 0 to disable (default 1m0s) [^c4-1]

`--poll-interval` **必须小于 `--dir-cache-time`**；设为 `0` 可禁用轮询；且仅对支持的 remote 有效。如果后端不支持轮询，那么"在网页端或另一台机器上做的改动"要等目录缓存过期（默认 5 分钟）才会被看到——这也是很多"目录不刷新"问题的根因。

#### 社区经验：完整 unit 与 `/etc/fuse.conf`

以下**全部标注为社区经验（S10，T3）**。原帖抓取时论坛渲染把 unit 段落的换行压平了（缺陷清单 §4.4 记录在案），下面按 INI 结构**重排**，**不是逐字引用**。

**第一步：启用 FUSE 的 `user_allow_other`（社区经验）**

社区帖原话是「(without it, it will not work)」，并解释「The --allow-other flag (which lets other users access the mount) requires explicit permission in /etc/fuse.conf.」[^c4-4]

这里必须做层级区分（深研文件 §4.3 的典型反例）：

| 断言 | 可依据的来源 | 该怎么说 |
|---|---|---|
| FUSE 默认只允许 root 使用 `allow_other`，该限制可由一个用户态配置项解除 | **S09 内核文档（T1 官方）** | 可直接断言 |
| 这个配置项叫 `user_allow_other` | **S09 内核文档（T1 官方）**：原文提到 "With the 'user_allow_other' config option" | 可直接断言 |
| 配置项写在 **`/etc/fuse.conf`** | **仅 S10 社区帖（T3）** | **必须标注为社区经验**，内核文档从未出现这个路径 |

所以：**"需要用户态配置项"是官方结论，"文件在 `/etc/fuse.conf`"是社区经验。** 内核文档既没给这个路径，也没给未设置时的默认值或报错文案。

社区帖给的启用与验证命令 [^c4-4]：

```bash
# 社区经验（S10）：取消 /etc/fuse.conf 里 user_allow_other 的注释
sudo sed -i 's/# user_allow_other/user_allow_other/' /etc/fuse.conf

# 验证
grep user_allow_other /etc/fuse.conf
# 预期输出：user_allow_other
```

**第二步：建日志目录（社区经验）**

社区帖说明：服务以普通用户身份运行，写不了 `/var/log/`，改用用户自己的目录 [^c4-4]。

```bash
mkdir -p ~/.local/log
```

**第三步：写 unit（社区经验；`Type=notify` 一行有官方依据）**

原帖把 unit 放在 `/etc/systemd/system/rclone-gdrive.service` [^c4-4]。重排后如下（远程名 `YourRemote:` 与路径 `YOUR_USER` 要换成你自己的）：

```ini
# /etc/systemd/system/rclone-openlist.service
# 社区经验（S10 帖，按 INI 结构重排，非逐字引用）
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

指令逐条拆解与层级标注：

| 指令 | 作用 | 层级 |
|---|---|---|
| `Type=notify` | 挂载点就绪后服务才进入 started | **官方（S06）** |
| `AssertPathIsDirectory=` | 挂载点目录不存在时服务启动失败而不是悄悄跑空 | 社区经验（S10） |
| `After=network-online.target` | 等网络就绪再启动 | 社区经验（S10） |
| `User=YOUR_USER` | 以普通用户运行（`allow_other` 场景下的常见安排） | 社区经验（S10） |
| `ExecStop=/bin/fusermount3 -u ...` | 停止服务时手动卸载 | 社区经验（S10） |
| `Restart=always` / `RestartSec=10` | 挂载掉线后自动重启，间隔 10 秒 | 社区经验（S10） |
| `WantedBy=default.target` | 用户级/默认目标下开机自启 | 社区经验（S10） |
| `--config` / `--cache-dir`（若使用）必须写绝对路径 | 因为 systemd 无环境变量、`~` 不展开；本 unit 示例已含 `--config` | **官方（S06）** |

> [!warning] `ExecStop` 用 `fusermount3` 是发行版差异，不是通用写法
> 社区帖原文说明「fusermount3 instead of fusermount — Fedora uses FUSE3」[^c4-4]。**Fedora 用 FUSE3，所以写 `fusermount3`；Debian/Ubuntu 上具体用哪个，取决于系统装的是 FUSE2 还是 FUSE3**——用 4.1 节 `which fusermount fusermount3` 的结果决定。写错名字的表现是停止服务时卸载失败，但服务本身看起来"启动了"，很容易漏查。

**第四步：启用并验证（社区经验）**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now rclone-openlist.service

systemctl status rclone-openlist.service
# 预期：Active: active (running)
```

社区帖的原话是「You should see Active: active (running).」[^c4-4]

社区帖还提到一条实用建议：服务失败时优先直接看日志文件而不要只看 `journalctl`——「(It is more detailed this way)」。

```bash
cat ~/.local/log/rclone_openlist.log
```

**为什么这里会同时出现"官方"和"社区经验"**

这是本章最需要读者带走的判断力：**同一个 unit 文件里，`Type=notify` 有 rclone 官方文档背书，其余指令只是某个社区帖的个人实践。** 写自己的 unit 时，可以放心用官方那部分，社区那部分照抄没问题但要理解它为什么这么写（尤其是 `fusermount3` 的发行版差异，和"为什么日志不能写 `/var/log`"）。

### 4.10 章末可跑产出

把上面几步串起来，完成后应当满足三条：

**1. 挂载点能 `ls` 到第 2 章挂进来的内容**

```bash
ls -l /mnt/openlist
```

预期：列出你在第 2 章聚合进来的存储（若第 2 章用的是本地存储驱动，就看到那个目录下的文件）。看得到内容，说明这条链路真的通了：

```text
rclone 进程
  → openlist: 远端（WebDAV over HTTP）
    → OpenList /dav/ 端点
      → 用户权限项（WebDAV 读取）
        → 第 2 章挂载的存储
          → 网盘 / 本地目录
```

**2. `systemctl status` 见 `active (running)`**

```bash
systemctl status rclone-openlist.service
# Active: active (running)
```

因为是 `Type=notify`，看到 `running` 差不多同时意味着**挂载点已就绪**，而不只是进程活着。

**3. reboot 后自动恢复**

```bash
sudo systemctl reboot
# 重新登录后
ls -l /mnt/openlist
systemctl status rclone-openlist.service
```

若重启后没挂上，按这个顺序查（判据都在来源里）：

| 症状 | 查什么 | 依据 |
|---|---|---|
| `fusermount: executable file not found in $PATH` | `/bin` 与 `/usr/bin` 下是否有 fusermount / fusermount3 | S06 官方 |
| 报路径找不到 | `ExecStart` 里的 `--config`（以及 `--cache-dir`，若写了）是否为绝对路径 | S06 官方 |
| 挂载点空 / 权限拒绝 | `--allow-other` 是否被 fuse.conf 允许（**社区经验路径**） | S09 官方 + S10 社区 |
| `fusermount3: mount failed: Permission denied` | Ubuntu 是否 AppArmor 拦截 | S06 官方 |
| 启动"成功"但挂载点空 | `Type=` 是否误写成 `simple` | S06 官方 |

### 本章小结

- `rclone mount` 用 **FUSE** 把云存储变成本地文件系统；FUSE 由内核模块 `fuse.ko`、用户态库 `libfuse.*`、挂载工具 `fusermount` 三件套组成，`fusermount` 以 setuid root 安装并对非特权挂载自动加 `nosuid` + `nodev`。
- 远端配置的关键是 `type = webdav`、**必填的 `url`**（要指到 `/dav/`，端口与网页端一致）、以及**必须 obscure 的 `pass`**；`vendor = other` 是**推断**，后果是只能按普通 WebDAV 工作——**不支持修改时间，也不支持哈希**。
- `--vfs-cache-mode` 默认 `off`，四档是本章主坑：`off` 读写直连远端、不支持读写同开、写不能 seek、上传失败**不能重试**；`writes` 支持全部常规操作并按指数间隔重试上传（最长 1 分钟）；`full` 连读也缓存、缓存是稀疏文件，**FAT/exFAT 上会性能崩并记 ERROR**。
- 两条风险要主动隔离：多个 rclone 实例共用同一远端缓存**可能损坏数据**（用 `--cache-dir` 隔离）；`--attr-timeout` 窗口内远端文件长度变化可能表现为**截断或末尾乱码**。
- systemd 集成里 **`Type=notify` 与"无环境变量、PATH 回退 `/bin:/usr/bin`"有官方依据**；而完整 unit 与 `/etc/fuse.conf` 位置**只有社区经验（S10）**可依据（缺口 G3）——引用时务必分层标注。
- 本机是 Windows + Git Bash，上述命令需在 WSL / NAS / 远程 Linux 宿主机执行；`--allow-other`、`--uid`、`--umask` 等参数**不支持 Windows**。

[^c4-1]: rclone 官方文档 — *rclone mount*（T1 官方）。https://rclone.org/commands/rclone_mount/
[^c4-2]: rclone 官方文档 — *WebDAV*（T1 官方）。https://rclone.org/webdav/
[^c4-3]: Linux 内核官方文档 — *FUSE Overview*（T1 官方）。https://docs.kernel.org/filesystems/fuse/fuse.html
[^c4-4]: rclone 论坛帖 — *How to mount Rclone persistently on Fedora Linux (on boot)*（**T3 社区经验，非官方**）。https://forum.rclone.org/t/how-to-mount-rclone-persistently-on-fedora-linux-on-boot/53738
