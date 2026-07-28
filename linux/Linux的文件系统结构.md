---
title: Linux 文件系统结构
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 基础, filesystem]
---

# Linux 文件系统结构

> [!info] 概述
> **Linux 的文件系统是一个树状层次结构**，从根目录 `/` 开始向下延伸。所有设备、文件、目录都挂载在这个树上的某个节点。理解这个结构是掌握 Linux 系统管理的第一步。

---

## FHS 标准

Linux 的文件系统遵循 **FHS（Filesystem Hierarchy Standard，文件系统层次结构标准）**，定义了各目录的用途和存放内容。

| 标准 | 说明 |
|------|------|
| **FHS 3.0** | 最新版本（2015），大多数主流发行版遵循 |
| **适用范围** | Linux、类 Unix 系统 |
| **目的** | 统一目录布局，方便跨发行版管理和开发 |

> [!tip] 为什么重要
> 懂 FHS 意味着你能在任意 Linux 系统上迅速找到配置（`/etc`）、日志（`/var/log`）、程序（`/usr/bin`），无需猜测。

---

## 根目录层级

```text
/
├── bin      → /usr/bin      (符号链接，近年发行版)
├── boot                    (引导文件)
├── dev                     (设备文件)
├── etc                     (配置文件)
├── home                    (用户家目录)
├── lib      → /usr/lib     (符号链接)
├── media                   (可移动介质)
├── mnt                     (临时挂载)
├── opt                     (可选软件)
├── proc                    (虚拟进程文件系统)
├── root                    (root 用户家目录)
├── run                     (运行时数据)
├── sbin     → /usr/sbin    (符号链接)
├── srv                     (服务数据)
├── sys                     (内核与设备信息)
├── tmp                     (临时文件)
├── usr                     (用户程序与数据)
└── var                     (可变数据：日志、缓存)
```

> [!note] 现代 Linux 的合并趋势
> 许多发行版（如 Arch、Fedora、Ubuntu）已采用 **usrmerge**，将 `/bin`、`/sbin`、`/lib` 合并到 `/usr/` 下，根目录中的同名路径变为符号链接。

---

## 各目录详解

### `/boot` — 引导加载程序

存放启动 Linux 所需的核心文件。

| 文件/目录 | 用途 |
|-----------|------|
| `vmlinuz-*` | 压缩的内核镜像 |
| `initrd.img-*` / `initramfs-*` | 初始内存磁盘（加载驱动用） |
| `grub/` | GRUB 引导配置 |
| `config-*` | 内核编译配置 |
| `System.map-*` | 内核符号表 |

```bash
# 查看当前使用的内核
ls /boot/vmlinuz-*
```

> [!warning] 空间敏感
> `/boot` 通常只有 500MB-1GB，内核升级后记得清理旧版本，否则系统可能无法更新。

---

### `/etc` — 系统配置文件

**最重要的配置目录**，保存系统级配置文件，纯文本格式，可直接编辑。

| 常见文件 | 用途 |
|----------|------|
| `/etc/passwd` | 用户账户信息 |
| `/etc/shadow` | 用户密码哈希（仅 root 可读） |
| `/etc/group` | 用户组定义 |
| `/etc/fstab` | 文件系统挂载表（开机自动挂载） |
| `/etc/hosts` | 静态主机名解析 |
| `/etc/resolv.conf` | DNS 解析器配置 |
| `/etc/apt/sources.list` | apt 软件源列表（Debian/Ubuntu） |
| `/etc/ssh/sshd_config` | SSH 服务端配置 |
| `/etc/hostname` | 主机名 |
| `/etc/crontab` | 系统定时任务 |
| `/etc/network/` | 网络配置（传统） |
| `/etc/netplan/` | Netplan 网络配置（Ubuntu 18.04+） |
| `/etc/sudoers` | sudo 权限配置 |
| `/etc/environment` | 系统环境变量 |
| `/etc/systemd/` | systemd 单元和服务配置 |

```bash
# 查看所有配置文件列表（不包含子目录）
ls -d /etc/*.conf | head -20
```

> [!tip] 备份习惯
> 修改 `/etc/` 下的配置前，养成备份的习惯：`cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`

---

### `/home` — 用户家目录

每个普通用户的家目录默认在此，用户对自己的家目录拥有完整权限。

| 路径 | 说明 |
|------|------|
| `/home/alice/` | 用户 alice 的家目录 |
| `/home/bob/` | 用户 bob 的家目录 |
| `~/` | 当前用户家目录的简写（等价于 `$HOME`） |

```bash
# 查看所有用户家目录
ls -la /home/

# 常用家目录子目录
~/.config/      # 用户级配置
~/.local/       # 用户级程序/数据
~/.cache/       # 用户级缓存
~/.ssh/         # SSH 密钥和配置
~/.bashrc       # Bash 个性化配置
```

> [!note] root 的家目录
> root 用户的家目录在 `/root`，而不是 `/home/root`。

---

### `/var` — 可变数据

存放经常变化的数据：日志、缓存、队列、数据库文件等。

| 子目录 | 用途 |
|--------|------|
| `/var/log/` | 系统日志文件（最常用） |
| `/var/log/syslog` 或 `/var/log/messages` | 系统总日志 |
| `/var/log/auth.log` | 认证日志（Ubuntu/Debian） |
| `/var/log/nginx/` | Nginx 访问/错误日志 |
| `/var/log/journal/` | systemd journal 持久日志 |
| `/var/cache/` | 应用程序缓存（apt、pacman 等） |
| `/var/lib/` | 应用程序状态数据（数据库、容器） |
| `/var/spool/` | 任务队列（邮件、打印） |
| `/var/tmp/` | 重启后保留的临时文件 |
| `/var/run/` | → `/run` 的符号链接 |
| `/var/mail/` | 用户邮箱 |

```bash
# 查看磁盘空间占用最大的日志
du -sh /var/log/* | sort -rh | head -10

# 定期用 logrotate 轮转日志，避免占满磁盘
```

> [!warning] 日志爆炸
> `/var/log` 是系统盘空间告警的常见原因，建议用 `journalctl --disk-usage` 和 `logrotate` 管理日志大小。

---

### `/usr` — 用户系统资源

**第二大的目录**，存放系统程序、库、文档、源代码等。现代系统大部分二进制文件都在此处。

| 子目录 | 用途 |
|--------|------|
| `/usr/bin/` | 用户可执行命令（`ls`、`cp`、`vim` 等） |
| `/usr/sbin/` | 系统管理命令（`fdisk`、`mkfs` 等） |
| `/usr/lib/` | 系统库文件（`.so` 共享库） |
| `/usr/lib/modules/` | 内核模块 |
| `/usr/share/` | 架构无关的共享数据（文档、图标、man 手册） |
| `/usr/man/` 或 `/usr/share/man/` | man 帮助文档 |
| `/usr/include/` | C/C++ 头文件 |
| `/usr/local/` | 本地安装的软件（编译安装默认位置） |
| `/usr/src/` | 内核源码 |

```bash
# 统计 /usr 下各子目录大小
du -sh /usr/* | sort -rh | head -10

# 查看 /usr/bin 中可执行文件数量
ls /usr/bin | wc -l
```

> [!tip] `/usr/local/` 的正确用法
> 编译安装软件时尽量安装到 `/usr/local/`（如 `./configure --prefix=/usr/local`），与系统包管理器管理的文件隔离，方便管理。

---

### `/proc` — 虚拟进程文件系统

**伪文件系统**，不占用磁盘空间，反映内核与进程的实时状态。

```bash
# CPU 信息
cat /proc/cpuinfo

# 内存信息
cat /proc/meminfo

# 系统运行时间
cat /proc/uptime

# 当前进程列表（数字编号的子目录）
ls /proc | grep -E '^[0-9]+$' | head -10

# 根文件系统挂载参数
cat /proc/mounts | head -5
```

| 虚拟文件 | 用途 |
|----------|------|
| `/proc/cpuinfo` | CPU 详细信息 |
| `/proc/meminfo` | 内存使用详情 |
| `/proc/loadavg` | 系统负载平均值 |
| `/proc/uptime` | 系统启动时长 |
| `/proc/version` | 内核版本 |
| `/proc/[PID]/` | 指定进程的状态、环境变量、文件描述符 |
| `/proc/sys/` | 内核运行时参数（`sysctl` 接口） |

```bash
# 通过 /proc/sys 查看/修改内核参数（等价于 sysctl）
cat /proc/sys/net/ipv4/ip_forward
# 输出 0 表示未开启 IP 转发
```

> [!note] `/proc` vs `/sys`
> - `/proc`：以进程为中心的接口，包含 CPU、内存、进程信息
> - `/sys`：以设备为中心的接口，提供内核设备模型的详细视图

---

### `/dev` — 设备文件

Linux 将硬件设备抽象为文件，统一通过文件 I/O 操作。

| 设备文件 | 对应硬件 |
|----------|----------|
| `/dev/sda` | 第一块 SATA 硬盘 |
| `/dev/nvme0n1` | 第一块 NVMe 固态硬盘 |
| `/dev/tty` | 当前终端 |
| `/dev/null` | 黑洞设备（丢弃所有写入） |
| `/dev/zero` | 无限输出 \x00 字节 |
| `/dev/random` | 随机数生成器 |
| `/dev/urandom` | 随机数（非阻塞） |
| `/dev/sr0` | 光驱 |
| `/dev/loop0` | 回环设备（挂载镜像文件） |

```bash
# 查看块设备（硬盘、分区）
lsblk

# 查看所有设备文件（非常多的条目）
ls /dev/ | head -20

# 向 /dev/null 丢弃输出
echo "这条消息会消失" > /dev/null
```

---

### `/tmp` — 临时文件

所有用户可写，但**重启后通常被清空**。

```bash
# 查看 /tmp 所在文件系统
df -h /tmp

# 查看 /tmp 是否挂载为 tmpfs（内存中，重启丢失）
mount | grep /tmp
```

| 特性 | 说明 |
|------|------|
| 权限 | 所有用户可读写（但不可删除他人的文件，sticky bit） |
| 持久性 | 大部分发行版重启清空（有些保留 10 天未访问的文件） |
| 大小 | 若为 tmpfs，默认物理内存的一半 |

---

### `/run` — 运行时数据

启动后存放运行时数据，使用 tmpfs（内存），重启自动清空。

```bash
# 查看进程 PID 文件（常见于 /run）
ls /run/*.pid
```

---

### `/opt` — 可选软件包

第三方商业软件或独立安装的软件包。

```bash
# 典型结构
/opt/google/chrome/          # Google Chrome
/opt/VirtualBox/             # VirtualBox
/opt/sublime_text/           # Sublime Text
```

---

### `/srv` — 服务数据

存放系统提供的服务数据，如 Web 站点文件、FTP 数据等。

```bash
# 常见用途
/srv/www/           # Web 站点
/srv/ftp/           # FTP 共享
/srv/git/           # Git 仓库
```

---

## 权限与特殊权限

### 文件类型标记

```bash
$ ls -la
-rw-r--r--  1 alice alice  1024 Jul 29 10:00 file.txt
^
| 文件类型标志
```

| 标记 | 类型 |
|------|------|
| `-` | 普通文件 |
| `d` | 目录 |
| `l` | 符号链接 |
| `b` | 块设备（硬盘） |
| `c` | 字符设备（终端） |
| `s` | 套接字 |
| `p` | 命名管道 |

### 特殊目录权限：Sticky Bit

`/tmp` 目录的权限为 `drwxrwxrwt`，最后的 `t` 表示 sticky bit：

- 所有用户可在 `/tmp` 创建文件
- 用户只能删除/修改自己的文件，不能动别人的

```bash
# 查看 sticky bit
ls -ld /tmp
# drwxrwxrwt ...

# 手动设置 sticky bit
chmod +t /tmp/mydir
```

---

## 常用路径速查表

| 你想找什么 | 路径 |
|-----------|------|
| 系统日志 | `/var/log/` |
| SSH 配置 | `/etc/ssh/` |
| 网络配置 | `/etc/netplan/` 或 `/etc/network/` |
| apt 源列表 | `/etc/apt/sources.list` |
| 定时任务 | `/etc/crontab` 或 `crontab -e` |
| 用户加键 | `~/.ssh/authorized_keys` |
| 环境变量 | `/etc/environment` 或 `~/.bashrc` |
| systemd 服务 | `/etc/systemd/system/` 或 `/usr/lib/systemd/system/` |
| 内核模块 | `/usr/lib/modules/$(uname -r)/` |
| man 手册 | `/usr/share/man/` |
| Docker 数据 | `/var/lib/docker/` |
| Nginx 站点 | `/etc/nginx/sites-available/` |
| Web 根目录 | `/var/www/html/`（传统）或 `/srv/` |

---

## 常用命令

```bash
# 查看当前目录
pwd

# 列出目录内容
ls -la /etc

# 切换目录
cd /var/log

# 查看目录树结构（需安装 tree）
tree -L 2 /usr/local

# 查看磁盘挂载
df -h

# 查看各目录磁盘占用
du -sh /var/log

# 查看文件系统类型
lsblk -f

# 查看挂载信息
mount | grep "^/dev"
```

---

## 知识关联

- [[linux磁盘相关的知识]] — 磁盘分区、格式化、挂载
- [[linux的文件权限]] — chmod、chown、特殊权限详解
- [[linux常用命令/Linux 文件与目录操作]] — 文件操作命令实战
- [[linux常用命令/Linux 系统信息与硬件管理]] — 系统信息查询

---

> [!summary] 核心要点
> - Linux 文件系统从 `/` 根目录开始，遵循 FHS 标准
> - `/etc` 存配置，`/var/log` 存日志，`/home` 存用户数据
> - `/proc` 和 `/sys` 是虚拟文件系统，不占磁盘空间
> - `/tmp` 临时文件重启清空，不要放重要数据
> - 现代发行版将 `/bin`、`/sbin`、`/lib` 合并到 `/usr/` 下
> - 理解目录结构 = 知道任何配置文件/日志/程序应该在哪找
