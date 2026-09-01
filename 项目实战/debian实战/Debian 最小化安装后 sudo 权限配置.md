---
title: Debian 最小化安装后 sudo 权限配置
tags:
  - Debian
  - sudo
  - Linux
  - 运维
  - 实战
created: 2026-08-04
updated: 2026-08-31
status: 已完成
source_project: debian-practice
type: 实战笔记
---

# Debian 最小化安装后 sudo 权限配置

> [!summary] 笔记速览
> 一份从零配置 Debian 最小化系统 sudo 权限的实战指南。先弄清「最小化安装为什么没有 sudo」以及 su/sudo 与 sudo 组机制的原理，再走一遍「安装 sudo → 加组授权 → 验证」三步标准流程（含 sudo 密码机制），随后进阶到 visudo 与 sudoers 语法、NOPASSWD 免密，最后覆盖三类常见故障的排错与安全最佳实践。共八章，按顺序阅读即可完整掌握。

---

## 目录

- [第 1 章：为什么最小化安装后没有 sudo](#第-1-章为什么最小化安装后没有-sudo)
- [第 2 章：原理基础——su、sudo 与组机制](#第-2-章原理基础su-sudo-与组机制)
- [第 3 章：标准配置流程——三步安装与授权](#第-3-章标准配置流程三步安装与授权)
- [第 4 章：进阶——visudo 与 sudoers 语法](#第-4-章进阶visudo-与-sudoers-语法)
- [第 5 章：进阶——NOPASSWD 免密配置（可选）](#第-5-章进阶nopasswd-免密配置可选)
- [第 6 章：排错——「user is not in the sudoers file」（zhq 实战案例）](#第-6-章排错user-is-not-in-the-sudoers-filezhq-实战案例)
- [第 7 章：排错——sudo command not found 与 sudoers 损坏恢复](#第-7-章排错sudo-command-not-found-与-sudoers-损坏恢复)
- [第 8 章：安全最佳实践与总结](#第-8-章安全最佳实践与总结)

---

## 第 1 章：为什么最小化安装后没有 sudo

**结论先行**：Debian 最小化安装默认没有 sudo，这不是故障，而是安装器依据「root 密码是否留空」做出的设计选择。先弄清分叉规则，才能判断自己的系统属于哪条路、下一步该怎么走。

### 1.1 Debian 最小化安装的两种行为分叉

Debian Wiki 明确区分两种安装行为 [Debian Wiki — sudo](https://wiki.debian.org/sudo)：

- **root 密码留空**：sudo 自动安装，且安装时创建的普通用户已加入 `sudo` 组，装完即开箱即用，无需额外配置。
- **root 密码已设置**：sudo 不会被安装，可选创建的普通用户也不在 `sudo` 组，需手动三步配置（第 3 章展开）。

两者的本质区别：留空 root 密码，系统默认信任「首个用户」为管理员，把提权工具与授权一次配好；显式设置 root 密码，管理权默认交给 root，普通用户不自动获得任何提权能力。

**`sudo: command not found` 的根因**

最小化安装（Docker 镜像、VPS 初始系统）多属第二种情况，且往往连普通用户都没创建。此时输入 `sudo` 会直接报：

```plaintext
sudo: command not found
```

根因是 `/usr/bin/sudo` 这个二进制根本没有安装，而不是 PATH 缺目录 [linuxconfig — sudo command not found](https://linuxconfig.org/sudo-command-not-found-solution)。遇到 `command not found`，第一反应应是「命令是否存在」，而非「路径里有没有」。

### 1.2 笔记目标与整体路径

本笔记的目标：**让普通用户在最小化 Debian 上获得安全可用的 sudo 权限**。学完能独立跑通「安装 sudo → 加组授权 → 验证」全链路，会用 `visudo` 做安全精细授权，并排查三类最常见的 sudo 故障。

整体路径分五段：

1. **原理**（第 2 章）：`su` vs `su -`、sudo 的定位、Debian `sudo` 组机制
2. **标准配置**（第 3 章）：手动三步安装与授权
3. **进阶语法**（第 4-5 章）：visudo、sudoers 条目、免密（可选）
4. **排错**（第 6-7 章）：三类常见故障与恢复
5. **安全总结**（第 8 章）：最佳实践与速查清单

下一章先补原理——`su` 与 `su -` 的差别、为什么「加组后还要重新登录」。不弄清这两点，第 3 章的标准配置每一步都会踩坑。

---

## 第 2 章：原理基础——su、sudo 与组机制

**结论先行**：第 3 章的标准三步里，第一步 `su -` 和第三步「加 sudo 组」背后各藏一个原理坑——`su` 不带 `-` 会保留一个"脏环境"，导致切到 root 后命令找不到；而 Debian 的授权不是逐用户写规则，而是靠 `sudo` 组批量生效。本章把这两块地基打牢。

### 2.1 `su` 与 `su -`：一个 `-` 决定环境

**结论**：用 `su` 切用户必须带 `-`（即 `su -` / `su --login`）。man 手册明确建议**总是用 `--login`**，避免混合环境副作用 [su(1) manual](https://man7.org/linux/man-pages/man1/su.1.html)。

原因在于两者对环境的处理完全不同：

| 行为 | `su`（非登录 shell） | `su -`（登录 shell） |
|------|---------------------|---------------------|
| 环境变量 | 只设 HOME、SHELL（目标非 root 时再加 USER、LOGNAME），**其余原样保留** | 清空除 TERM 等白名单外的全部变量，重建 HOME/SHELL/USER/LOGNAME/PATH |
| 工作目录 | 不切换 | 切到目标用户主目录 |
| 污染风险 | 调用者的 `LD_PRELOAD`、`LD_LIBRARY_PATH` 会被带进 root 会话 | 无 |

> [!note] 核心概念：`su -` 才是"真正的登录"
> `su` 只设置 HOME 和 SHELL 就完事，调用者的 PATH、`LD_PRELOAD` 等变量原样带进 root 会话；`su -` 会清空环境并**重建 PATH**、切到目标用户主目录。管理任务请一律用 `su -`。

「脏环境」的直接后果是 **PATH 没有重建**。普通用户 PATH 默认只有 `/usr/local/bin:/bin:/usr/bin`，而 root 走 ENV_SUPATH，默认是 `/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin`。系统管理命令（如 `/usr/sbin`、`/usr/local/sbin` 下的工具）在普通用户 PATH 里根本不存在：

```plaintext
# 普通用户 PATH
/usr/local/bin:/bin:/usr/bin
# root PATH（su - 后）
/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
```

这正是「su 切 root 后 apt 找不到」「PATH 没有 /sbin」这类坑的通用根因——第 3 章第一步必须用 `su -`。

### 2.2 `su` 与 `sudo`：切换身份 vs 单条提权

**结论**：日常提权用 `sudo`，不用 `su`。`su` 是**切换身份**——开一个目标用户的交互式 shell；`sudo` 是**以目标身份执行单条命令**，命令跑完就回到原用户 [Debian Wiki — sudo](https://wiki.debian.org/sudo)。

在最小化安装场景，`su` 只是**安装 sudo 的前置手段**：sudo 包还没装，只能先用 root 身份把它装上。

**密码机制的区别（易混点）**：`sudo <命令>` 要求输入的密码是**当前登录用户自己的密码**，而不是 root 的密码——它只是验证你的身份、确认你有权以管理员身份执行该命令；`su -` 要求输入的才是 **root 用户的密码**，用于直接切换身份到 root 超级管理员账户：

| 命令 | 需要输入的密码 | 密码的作用 | 身份机制 |
|------|----------------|------------|----------|
| `sudo <命令>` | **当前用户的密码** | 验证你的身份，确认你有权限以管理员身份执行该命令 | 单条命令提权，命令跑完回到原用户 |
| `su -` | **root 用户的密码** | 直接切换身份到 root 超级管理员账户 | 开一个 root 交互式 shell，全程以 root 身份操作 |

> [!note] 核心概念：sudo 输自己的密码，su - 才输 root 的密码
> 不少人以为 sudo 输的是 root 密码，其实是「当前登录用户自己的密码」——它验证的是**你**是否有权提权；真正需要 root 密码的是 `su -`。这也是为什么第 3 章里「加完 sudo 组就能用自己密码执行 sudo」成立：授权看的是用户身份（第 2.3 节组机制），密码验证的也是用户自己的身份。

sudo 相比 su 的三个核心优势：

| 能力 | 说明 |
|------|------|
| 凭据缓存 | 默认 15 分钟（`timestamp_timeout`），期间免密重复执行 |
| 审计日志 | 每次提权都被记录，可追溯谁干了什么 |
| 细粒度授权 | 精确到「哪个用户、哪台主机、以谁执行、哪条命令」 |

### 2.3 Debian 的 sudo 组机制

**结论**：Debian 默认不写用户级规则，而是用 `sudo` 组批量授权——**入组即获完整 sudo 权限** [Debian Wiki — sudo](https://wiki.debian.org/sudo)。

- `sudo` 组 GID 为 **27**。
- Debian 默认 sudoers 里已内置一条 `%sudo ALL=(ALL:ALL) ALL`，`%` 前缀表示"组"；所以 `adduser <用户> sudo`（等价 `usermod -aG sudo <用户>`）后，用户自动套上这条完整规则，无需再改 sudoers。
- 验证入组是否成功：`id` / `groups` 输出里应看到 `27(sudo)`。

管理组命名在不同发行版/文档间有差异：

| 发行版 | 管理组 | 备注 |
|--------|--------|------|
| Debian / Ubuntu | `sudo`（GID 27） | 默认 sudoers 已含 `%sudo` 授权行 |
| RHEL 系 | `wheel` | 对应约定，规则格式相同 |
| 旧文档 / 部分镜像 | `admin` | 旧式约定（如 Rackspace 旧文档），现代 Debian 已弃用 |

注意：加组只改 `/etc/group`，**不碰 sudoers**——这也是第 6 章排错时「先验组、再查 `%sudo` 行」顺序的依据。

### 本章小结

- `su` 保留调用者环境、不切目录；`su -` 清环境重建 PATH 并切主目录，切 root 务必用 `su -`。
- root 的 PATH 含 `/usr/sbin`、`/usr/local/sbin`，普通用户没有——「切 root 后命令找不到」的通用根因。
- `su` 切换身份，`sudo` 单条提权；sudo 凭据缓存 15 分钟、有审计日志、支持细粒度授权。
- 密码机制不同：`sudo <命令>` 输**当前用户自己的密码**（验证身份、确认有权提权）；`su -` 输 **root 的密码**（直接切换身份到 root）。
- Debian 用 `sudo` 组（GID 27）配合默认 `%sudo ALL=(ALL:ALL) ALL` 实现「入组即授权」；RHEL 系是 `wheel`，旧文档是 `admin`。
- 加组只改组文件、不写 sudoers；组身份在登录时读取，改完要重新登录才生效。

下一章就动手：`su -` → `apt update && apt install sudo` → `usermod -aG sudo`，三步完成配置并用 `27(sudo)` 与 `sudo whoami` 验证。

---

## 第 3 章：标准配置流程——三步安装与授权

**结论先行**：第 2 章的原理现在落地。标准配置只有三步：`su -` 切到 root、`apt update && apt install sudo -y` 安装 sudo、`usermod -aG sudo <用户名>` 把用户放进 sudo 组，最后重新登录用 `sudo whoami` 验证。全程建议在真实环境逐条执行，别只看。

### 3.1 切换到 root

安装 sudo 需要 root 权限，而最小化安装（root 密码已设的那种）还没有 sudo 可借，所以先用 `su -` 切到 root：

```bash
su -
```

- 会提示输入 root 密码，成功后提示符从 `$` 变成 `#`（`root@host:~#`）。
- 必须带 `-`（`--login`）。第 2 章讲过：不带 `-` 只保留调用者的「脏环境」，PATH 不重建，`apt` 这类 `/usr/sbin` 下的命令可能找不到 [su(1) manual](https://man7.org/linux/man-pages/man1/su.1.html)。

预期输出：

```text
$ su -
密码：
root@host:~#
```

### 3.2 安装 sudo

进入 root 后，先刷新包索引再装包：

```bash
apt update && apt install sudo -y
```

- `apt update` 必须先于 `apt install`：它把软件源的包列表同步到本地，`apt` 才知道 `sudo` 这个包是否存在、最新版本是什么。跳过它会报 `Unable to locate package sudo` [linuxconfig — sudo command not found](https://linuxconfig.org/sudo-command-not-found-solution)。
- `-y` 自动确认所有交互提问，避免卡在 `Do you want to continue? [Y/n]`。

装完确认二进制已就位：

```bash
which sudo
```

预期输出 `/usr/bin/sudo`。

### 3.3 将用户加入 sudo 组

sudo 装好了，但普通用户还没有权限。Debian 的授权模型是「入组即授权」——把用户加进 `sudo` 组（GID 27），自动套上默认的 `%sudo ALL=(ALL:ALL) ALL` 规则，无需再改 sudoers [Debian Wiki — sudo](https://wiki.debian.org/sudo)：

```bash
usermod -aG sudo zhq
```

把 `zhq` 换成你的用户名。

- 必须带 `-a`（append）。`-G` 指定要加入的附属组列表，**没有 `-a` 会整个覆盖**用户的附属组，把用户从其他组里踢出去；`-a` + `-G` 才是「追加」 [Rackspace — Grant sudo access](https://docs.rackspace.com/FI/docs/grant-sudo-access-in-debian-and-the-ubuntu-operating-system)。
- Debian 官方同样推荐等价的 `adduser zhq sudo`，效果完全一样。

确认组已加入：

```bash
id zhq
```

预期输出含 `27(sudo)`：

```text
uid=1001(zhq) gid=1001(zhq) groups=1001(zhq),27(sudo)
```

### 3.4 重新登录并验证

> [!warning] 易错点：组身份只在登录时读取
> 刚加完组，当前会话仍持有旧的组列表，直接跑 `sudo` 大概率报错 [Debian Wiki — sudo](https://wiki.debian.org/sudo)：
>
> ```text
> zhq is not in the sudoers file.  This incident will be reported.
> ```
>
> （或 `Sorry, user zhq is not allowed to execute '/usr/bin/whoami' as root on ...`。）
>
> 这不是配置错了，是会话没刷新。三种刷新方式按优先级：

| 方式 | 命令 / 操作 | 适用场景 |
|------|-------------|----------|
| ① 注销重登（推荐） | 完全退出会话再登录 | 最干净，组身份彻底重建 |
| ② 当场重登 | `su - $USER` | 不想中断当前终端时 |
| ③ 临时生效 | `newgrp sudo` | 只对当前 shell 生效，新 shell 失效 |

完成任一种后，按验证链走一遍：

```bash
id              # groups 里应有 27(sudo)
groups          # 同上，更简
sudo whoami     # 应输出 root
```

预期：

```text
$ id
uid=1001(zhq) gid=1001(zhq) groups=1001(zhq),27(sudo)
$ sudo whoami
root
```

`sudo whoami` 输出 `root`，说明 sudo 已安装、授权已生效、凭据缓存已建立（默认 15 分钟），标准配置完成。

### 3.5 密码机制：sudo 要的密码是什么

**结论先行**：`sudo whoami` 敲下去后提示的密码，是**当前用户的登录密码**，不是 root 密码。Debian 默认 sudoers 没有开 `rootpw`/`targetpw`，sudo 拿你的身份去认证——密码对，才继续查你有没有提权规则。所以「配置 sudo 密码」改的是自己账号的密码；root 密码由 `su -` 单独使用、单独管理。

#### 3.5.1 修改 sudo 要的密码

改你自己账号的密码即可：

```bash
passwd
```

会先要旧密码，再输两遍新密码；改完以后 `sudo` 就用新密码。用有 sudo 权限的账号重置别人的密码：

```bash
sudo passwd <用户名>
```

#### 3.5.2 设置 / 修改 root 密码

`su -` 用的 root 密码和 sudo 无关。最小化安装走「root 密码已设置」分支时，装系统时已定好；要改或当初留空，执行：

```bash
sudo passwd root
```

#### 3.5.3 让 sudo 改问 root 密码（可选）

一般不需要，但语法上支持——在 sudoers 里加：

```text
Defaults rootpw        # 一律问 root 密码
# Defaults targetpw     # 问目标用户（提权到 root 就问 root）密码
```

必须经 `visudo` 改（第 4 章红线）。

#### 3.5.4 密码缓存时长

sudo 会缓存认证结果，默认 15 分钟（`timestamp_timeout`）内免密重复执行：

```text
Defaults timestamp_timeout=10   # 10 分钟；0 表示每次都要输；负数永不超时
```

> [!note] 免密是另一回事
> 「让 sudo 不输密码」是第 5 章的 `NOPASSWD:` 标签，只应对低风险命令开。

### 本章小结

- 标准三步：`su -` 切 root → `apt update && apt install sudo -y` → `usermod -aG sudo <用户名>`。
- `su` 必须带 `-`；`apt update` 必须先于 `apt install sudo`；`usermod` 必须带 `-a` 追加。
- Debian 推荐 `adduser <用户名> sudo`，与 `usermod -aG sudo` 等价。
- 组身份登录时读取，加组后必须重登（或 `su - $USER` / `newgrp sudo`），否则报 `not in the sudoers file` / `Sorry`。
- 验证链：`id` 见 `27(sudo)` → `sudo whoami` 输出 `root`。
- sudo 要的是**当前用户密码**，不是 root：改它用 `passwd`，改 root 用 `sudo passwd root`，缓存时长由 `Defaults timestamp_timeout` 控制（默认 15 分钟）。

下一章进入进阶：`visudo` 与 sudoers 语法——为什么一个语法错误能让全部 sudo 失效，以及如何安全地做「只允许某条命令」的精细授权。

---

## 第 4 章：进阶——visudo 与 sudoers 语法

**结论先行**：第 3 章用的是「入组即授权」——把用户丢进 sudo 组，套用现成的宽泛规则。但生产环境往往需要更细的控制：只让某个部署用户能 reload nginx，而不给它整个 root。这一切都要改 sudoers，而 sudoers 是「改错一行就全盘崩溃」的配置文件。本章讲清楚为什么必须用 visudo、sudoers 的条目语法、片段文件，以及改完如何校验。

### 4.1 为什么必须用 visudo

sudo 启动时会读取 `/etc/sudoers` 并逐行解析。如果文件里有语法错误，sudo 会认为整个配置非法而拒绝工作——结果是**所有用户的 sudo 全部失效** [DigitalOcean — How To Edit the Sudoers File](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。

visudo 是 sudo 官方提供的 sudoers 专属编辑器，提供三重保障：

| 保障 | 作用 |
|------|------|
| 排他锁 | 同一时刻只允许一个管理员编辑，防止并发写入互相覆盖 |
| 保存时语法校验 | 编辑无效时拒绝保存，并保留上一可用版本 |
| 语法错误回滚 | 已保存但解析失败时，自动回滚到备份，不至于锁死 |

对比：用 vim/nano 直接编辑 `/etc/sudoers`，保存退出后如果语法错了，sudo 直接罢工，而你可能已经退出了唯一能提权的会话——被锁在 sudo 之外 [Baeldung — Guide to Linux visudo Command](https://www.baeldung.com/linux/visudo-command-tutorial)。

> [!warning] 核心规则：任何时候都不要用 vim/nano 直接编辑 `/etc/sudoers`，只经 visudo
> visudo 会调用系统默认编辑器（Debian 上是 nano），想换成 vim 只需 `export EDITOR=vim`。

### 4.2 sudoers 条目格式

sudoers 一条规则的基本格式：

```text
user host=(runas:runas) command
```

| 字段 | 含义 | 说明 |
|------|------|------|
| `user` | 授权对象 | 用户名、`%组名` 或别名 |
| `host` | 主机范围 | `ALL` = 任意主机 |
| `(runas:runas)` | 以谁的身份执行 | `用户:组`；省略默认以 root 执行 |
| `command` | 允许的命令 | 必须写**绝对路径** |

**`%` 前缀表示组，无 `%` 是用户**。两个典型示例 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)：

```text
myuser  ALL=(ALL:ALL) ALL
%deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx
```

逐条解读：
- `myuser ALL=(ALL:ALL) ALL`：用户 `myuser` 可在任意主机、以任意用户身份（含 root）执行任意命令，需要密码。这就是第 3 章 `%sudo` 规则的单用户版。
- `%deploy ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx`：`deploy` 组的成员可在任意主机、**只**以 root 身份执行 `/usr/bin/systemctl reload nginx` 这一条命令，且免密。

命令必须写绝对路径：`/usr/bin/systemctl reload nginx`，而不是 `systemctl reload nginx`，否则 sudo 无法匹配命令 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)。

**别名**：规则变多时可把命令、用户分组。别名定义以 `_Alias` 结尾，名字全大写 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)：

```text
Cmnd_Alias OPS = /bin/systemctl reload nginx, /bin/systemctl status nginx
User_Alias DEV = zhq, alice

%DEV  ALL=(root) OPS
```

**主机限制**：`host` 字段可写具体主机名，规则只在对应主机生效，如 `zhq webserver01=(ALL) ALL` [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)。

> [!note] 匹配规则：冲突时"最后匹配项生效"
> sudoers 从上到下读取，冲突时**最后匹配的规则生效** [RHEL9 — 管理 sudo 访问](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)。这就是为什么第 6 章会讲到片段文件可能「覆盖」主配置——后面的规则盖住前面的。

### 4.3 片段文件 `/etc/sudoers.d/`

官方建议：本地定制规则放 `/etc/sudoers.d/` 下的新文件，而不是直接改主文件——系统更新期间能保留、也更好修 [RHEL9](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)。Debian 同样支持。

用 visudo 定向编辑片段文件：

```bash
sudo visudo -f /etc/sudoers.d/99-custom-ops
```

文件名规范（**来源：sudoers(5) man page / Debian 打包约定**，非博客正文）：
- **文件名不得含点 `.`**，如 `99.custom` 会被忽略。
- **不得以 `~` 结尾**，编辑器备份如 `99-custom-ops~` 会被忽略。
- 建议前缀数字控制加载顺序，如 `99-custom-ops`。

**权限要求（来源：sudoers(5) man page / Debian 打包约定）**：mode `0440`、属主 `root:root`。权限不对（例如组/其他用户可写）sudo 会拒绝读取：

```bash
chown root:root /etc/sudoers.d/99-custom-ops
chmod 0440 /etc/sudoers.d/99-custom-ops
```

片段能生效的前提是主文件里有 `#includedir /etc/sudoers.d`。注意这一行的 `#` 是**语法的一部分，不是注释**——不要把它当成注释删掉 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。向该目录添加新片段即生效，无需重启服务。

### 4.4 校验与验证命令

改完配置，按下面这条链走一遍，避免把坏语法留到下次：

```bash
sudo visudo -c        # 语法校验，确认 parsed OK
sudo -k               # 清空凭据缓存，强制下次重新认证
sudo -v               # 预验证：做一次模拟 sudo，刷新凭据租约
sudo -l               # 列出当前用户的有效规则
```

预期输出：

```text
$ sudo visudo -c
/etc/sudoers: parsed OK

$ sudo -l
User zhq may run the following commands on host:
    (ALL : ALL) ALL
```

如果语法出错，`visudo -c` 会精确定位到行 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)：

```text
>>> /etc/sudoers.d/99-custom-ops: syntax error near 'ALL'  <<<
```

想看**指定用户**被允许哪些命令，用 `-U`，无需切换到那个用户 [Baeldung](https://www.baeldung.com/linux/visudo-command-tutorial)：

```bash
sudo -l -U deploy
```

输出 `deploy` 用户能执行的规则列表。

### 本章小结

- sudoers 一个语法错误会让全部 sudo 失效，所以只经 visudo 编辑：排他锁 + 保存时校验 + 回滚三重保障。
- 规则格式 `user host=(runas:runas) command`；`%` 是组、无 `%` 是用户；命令必须绝对路径；省略 `(runas)` 默认以 root 执行。
- 用 `Cmnd_Alias` / `User_Alias` 分组、用 host 字段做主机限制；规则冲突时最后匹配的生效。
- 本地定制放 `/etc/sudoers.d/`：文件名不得含 `.`、不得以 `~` 结尾，权限 0440 root:root（来源 sudoers(5) / Debian 打包约定）；`#includedir` 的 `#` 是语法不是注释。
- 改完用 `sudo visudo -c` 校验，验证链 `sudo -k` → `sudo -v` → `sudo -l`；查指定用户用 `sudo -l -U <user>`。

下一章把语法里的 `NOPASSWD:` 展开：哪些场景值得免密、哪些必须避免。

---

## 第 5 章：进阶——NOPASSWD 免密配置（可选）

第 4 章在 `%deploy` 规则里出现过 `NOPASSWD:` 标签，它能让特定命令免输密码。但它是 sudoers 里最容易被滥用的特性——攻破你的账号的人只要拿到一条免密命令，往往就等于拿到 root。所以本章把它单列为「可选/谨慎」小节：先讲语法与示例，再讲清安全边界，**默认不推荐**。

### 5.1 免密语法

`NOPASSWD:` 是一个**标签（tag）**，加在命令列表前，让它**后面的连续命令**都免密：

```text
user host=(runas) NOPASSWD: 命令1, 命令2
```

两种典型形态：

| 形态 | 示例 | 含义 |
|------|------|------|
| 单命令免密 | `zhq ALL=(ALL) NOPASSWD: /usr/bin/systemctl` | 仅 `systemctl` 免密，其余命令仍需密码 |
| 全免密 | `zhq ALL=(ALL) NOPASSWD: ALL` | 所有命令免密，**强烈不推荐** |

命令仍必须是**绝对路径**（沿用第 4 章规则），否则 sudo 匹配不上 [Baeldung — Guide to Linux visudo Command](https://www.baeldung.com/linux/visudo-command-tutorial)。

**孪生标签 `PASSWD:`**：标签持续生效，直到被同行的 `PASSWD:` 重新打开。混用可以做到「多数命令免密、个别高危命令仍要密码」：

```text
GROUPTWO ALL = NOPASSWD: /usr/bin/updatedb, PASSWD: /bin/kill
```

解读：`/usr/bin/updatedb` 免密；到 `/bin/kill` 时 `PASSWD:` 重新生效，执行它仍需输入密码 [DigitalOcean — How To Edit the Sudoers File](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。改完照第 4 章的验证链走一遍：`sudo visudo -c` 应输出 `parsed OK`，再用 `sudo -l` 确认规则。

### 5.2 安全边界与建议

> [!warning] 免密 = 拆掉最后一道确认门槛
> 有人拿到你的账号后，不需要再拿到你的密码就能提权 [Debian Wiki — sudo](https://wiki.debian.org/sudo)。只该对**小范围、低风险、绝对路径**的命令开免密，例如只读的状态查询；任何「写操作」或能派生出 shell 的命令（编辑器、`python`、包管理器）都不该免密 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。

| 做法 | 结论 |
|------|------|
| `NOPASSWD: ALL` 全免密 | 实际等于 root，通常应避免 [Debian Wiki](https://wiki.debian.org/sudo) |
| 宽泛 `ALL=(ALL) ALL` | 用户「实际就是 root」，同理慎用 [Debian Wiki](https://wiki.debian.org/sudo) |
| 单命令免密（低风险） | 可接受，仅限自动化 / 脚本 / CI 场景 |

一句话边界：本章是**选项，不是默认推荐**。日常手动操作沿用第 3 章「入组 + 输密码」就足够；免密只在无人值守的自动化场景里才真正有价值。

### 本章小结

- `NOPASSWD:` 是标签，对其后连续命令生效；`PASSWD:` 是孪生标签，可重新打开密码门槛。
- `user ALL=(ALL) NOPASSWD: /usr/bin/systemctl` 只对单命令免密；`NOPASSWD: ALL` 全免密，强烈不推荐。
- 命令仍需绝对路径；改完用 `sudo visudo -c` 校验。
- 免密等于拆掉最后一道确认门槛，只对低风险命令开；`NOPASSWD: ALL` 与宽泛 `ALL=(ALL) ALL` 实际就是 root，通常应避免。
- 适用场景：自动化 / 脚本 / CI；手动日常操作不做默认推荐。

下一章回到最常见的故障：用户报 `user is not in the sudoers file`，第 2-4 章学的组机制与 sudoers 语法会在排错里派上用场。

---

## 第 6 章：排错——「user is not in the sudoers file」（zhq 实战案例）

按第 3 章做完 `usermod -aG sudo`，满心期待地敲下 `sudo whoami`，屏幕却弹出一句 `<user> is not in the sudoers file. This incident will be reported.` 很多人第一反应是「我被系统拉黑了吗」。这句报错是 Debian 上最常见的 sudo 故障。本章用 zhq 的真实排错过程，把它拆开讲清：它到底在说什么、有哪几类根因、按什么顺序查。

### 6.1 错误原文解读

这句话可以拆成两半看：

- `<user> is not in the sudoers file`——sudo 在 `/etc/sudoers`（及 `/etc/sudoers.d/`）里**找不到这个用户的授权**，这是真正的问题描述。
- `This incident will be reported`——只是说「这次失败的提权尝试已被记入本地审计日志」，通常写在 `/var/log/auth.log`。它是**本地日志警告，不是封禁**：系统不会因此拉黑账号或锁死你 [Unix & Linux SE — Debian 12 sudoers 配置坑](https://unix.stackexchange.com/questions/772500/)。

同样「sudo 不可用」还有另外两句常见变体，含义不同，别混为一谈 [RHEL9 — 管理 sudo 访问](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)：

| 错误原文 | 含义 |
| --- | --- |
| `<user> is not in the sudoers file. This incident will be reported.` | **无授权**：用户不在组、或规则缺失 |
| `is not allowed to run sudo on <host>` | **配置未完成**（host 段没匹配上） |
| `Sorry, user ... is not allowed to execute '...' as root on ...` | **命令不在规则中**：用户有 sudo 权限，但这条命令没被授权 |

> [!note] 区分思路
> 报错越具体，越说明「规则存在但没覆盖到」；而第一句「not in the sudoers file」通常指向「规则压根没有」。

### 6.2 根因清单与排查顺序

三类根因，**先验证、再改配置**，按下面顺序走，不要一上来就改文件 [Unix & Linux SE](https://unix.stackexchange.com/questions/772500/)：

| 步 | 动作 | 目的 |
| --- | --- | --- |
| 1 | `id <用户>` 或 `groups` | 确认已在 `sudo` 组（输出应含 `27(sudo)`） |
| 2 | 注销重登 / `su - $USER` / `newgrp sudo` | 刷新会话组身份 |
| 3 | `sudo visudo` 查 `%sudo ALL=(ALL:ALL) ALL` | 确认授权行存在且未注释 |
| 4 | `sudo -l` | 验证规则生效 |

**根因一：已入组但当前会话未刷新（最常见）**。组身份只在登录时读取，刚加组的旧会话还带着旧身份。先看第 1 步：

```bash
id zhq
# 成功在组：uid=1001(zhq) gid=1001(zhq) groups=1001(zhq),27(sudo)
# 没有 27(sudo)：说明根本没加进组，回头补 usermod -aG sudo zhq
```

输出有 `27(sudo)` 却仍报错，才是会话问题，走第 2 步刷新。

**根因二：sudoers 缺 `%sudo` 授权行或被注释**。入组只是「成为组员」，真正给权限的是 sudoers 里这行 [Debian Wiki — sudo](https://wiki.debian.org/sudo)：

```text
%sudo   ALL=(ALL:ALL) ALL
```

用 `sudo visudo` 打开确认它存在且行首没有 `#`。被注释或缺失，组员身份就毫无用处。

**根因三：`@includedir` 片段干扰**。`/etc/sudoers.d/` 里若有不兼容的片段，可能覆盖主配置；把片段文件暂时改名排除测试。

### 6.3 zhq 案例复盘

zhq 的真实场景是这样：`usermod -aG sudo zhq` 加组、注销重登后 `id` 确认 `27(sudo)` 已在，但 `sudo whoami` 依旧报 `zhq is not in the sudoers file`。按 6.2 逐条走：组没问题、会话已刷新，查到第 3 步——sudoers 里缺 `%sudo ALL=(ALL:ALL) ALL`。此时有两条路：

| 做法 | 示例 | 取舍 |
| --- | --- | --- |
| 加组管理（推荐） | 补上 `%sudo ALL=(ALL:ALL) ALL` 行，维持 `usermod -aG sudo` | 可逆、易审计、可批量撤销；但要先修好配置 |
| 逐用户写规则 | `zhq ALL=(ALL:ALL) ALL` 直接写进 sudoers | 直观、当场生效；绕过组机制、逐人维护麻烦 |

> [!tip] 实战取舍
> 临时直接写 `zhq ALL=(ALL:ALL) ALL` 能立刻解燃眉之急，但它绕过了「组」这个统一授权层。从审计与撤销的角度，长期应回补 `%sudo` 行、回到加组管理 [RHEL9](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)、[Rackspace](https://docs.rackspace.com/FI/docs/grant-sudo-access-in-debian-and-the-ubuntu-operating-system)。

### 本章小结

- `is not in the sudoers file` 只表示「找不到授权」，`This incident will be reported` 只是本地审计日志警告，不是封禁。
- 三句报错要区分：无授权 / 配置未完成 / 命令不在规则中。
- 排查顺序：验组 → 刷新会话 → 查 `%sudo` 行 → `sudo -l` 验证，先验证再改配置。
- 最常被忽视的根因是「入组了但旧会话没刷新」，先看 `id` 里的 `27(sudo)`。
- 临时直接写 `zhq ALL=(ALL:ALL) ALL` 可用，但长期应回补 `%sudo` 行、回归加组管理。

下一章处理另两类故障：`sudo: command not found` 和 sudoers 文件损坏后的恢复。

---

## 第 7 章：排错——sudo command not found 与 sudoers 损坏恢复

第 6 章解决的是「授权没配上」的故障；本章处理剩下两类更「硬」的问题：`sudo: command not found`（命令本身不存在）和 sudoers 文件损坏（配置坏了导致 sudo 直接罢工）。前者多半是包没装，后者是配置被改坏，两者都需要先从 sudo 之外拿到 root 才能修复。

### 7.1 sudo not found 的根因区分

`sudo: command not found` 看起来简单，但根因有两种，别急着改 PATH。先做一个关键判定：看 `/usr/bin/sudo` 到底存不存在 [linuxconfig — sudo command not found](https://linuxconfig.org/sudo-command-not-found-solution)。

| 根因 | 现象 | 判定方式 |
| --- | --- | --- |
| sudo 包未安装 | `/usr/bin/sudo` 不存在 | 最小化安装（Docker 镜像、VPS 初始系统）最常见 |
| 包已装但 PATH 缺 `/usr/bin` | `/usr/bin/sudo` 存在 | `which sudo` 找不到但文件在 |

```bash
ls -l /usr/bin/sudo
# 报 No such file or directory → 没装包，走下面的修复
# 有输出 → 包在，才去查 echo $PATH 是否含 /usr/bin
```

确认是没装包后，按第 3 章的路径修复（前提是掌握 root 密码）：

```bash
su -                          # 切 root，必须带 -（加载完整环境）
apt update && apt install sudo -y    # apt update 必须先于 install
usermod -aG sudo <你的用户名>   # Debian 系加入 sudo 组
su - <你的用户名>               # 切回普通用户
sudo whoami                   # 输出 root 即成功
```

注意 `<你的用户名>` 要替换成实际用户名；`apt update` 必须先跑，否则可能装到过期索引而失败 [linuxconfig](https://linuxconfig.org/sudo-command-not-found-solution)。

### 7.2 sudoers 损坏的症状与恢复分级

「not found」是包没装，而 sudoers 损坏是「装好了但配置坏了」——通常由**绕过 visudo 直接编辑 `/etc/sudoers`**（用 vim/nano）或**误改权限**引起。损坏后 sudo 一启动就报三段式错误 [Unix & Linux SE — sudoers 损坏恢复](https://unix.stackexchange.com/questions/650920/)：

```text
sudo: /etc/sudoers is world writable
sudo: no valid sudoers sources found. quitting
sudo: unable to initialize policy plugin
```

`is world writable` 指权限过宽。sudoers 的标准权限是 **0440、属主 root:root**；`/etc/sudoers.d/` 目录本身是 775，目录里的 `README` 是 440。

这段错误出现时，**sudo 已经完全不可用**——连 `sudo visudo` 都起不来。要修复，必须先通过 sudo 之外的方式拿 root，按可用手段分级：

| 级别 | 前提 | 做法 |
| --- | --- | --- |
| ① | root 密码已知 | `su -` 切 root → `chmod 440 /etc/sudoers` |
| ② | 系统有 polkit | `pkexec bash`（或 `pkexec chmod 0440 /etc/sudoers`） |
| ③ | 以上都没有 | Live CD / 安装盘启动，挂载根分区到 `/mnt`，`chmod 440 /mnt/etc/sudoers`；云主机可拆盘挂到别的机器修 |

两个细节要注意：

- 走 ② 时，SSH 场景通常需要**双终端**：先在一个终端跑 `pkttyagent` 注册 polkit 会话，再在另一个终端跑 `pkexec`，否则会报 polkit session cookie 错误。
- 走 ③ 时，`/mnt` 换成你实际挂载根分区的目录，文件路径对应写成 `/mnt/etc/sudoers`。

> [!warning] 修复后必须校验
> 修好权限回到正常系统后，必须校验一次才能确认真的恢复了：
>
> ```bash
> sudo visudo -c
> # /etc/sudoers: parsed OK
> ```
>
> 只有输出 `parsed OK` 才算修好，否则 sudo 可能再次罢工。这两类故障的共同源头是「绕过 visudo 直接碰 sudoers」——visudo 提供排他锁、保存时语法校验和错误回滚，是唯一安全的编辑方式 [Unix & Linux SE](https://unix.stackexchange.com/questions/650920/)。

### 本章小结

- `sudo: command not found` 先判 `ls /usr/bin/sudo`：文件不存在→没装包；文件在→才查 PATH。
- 修复路径：`su -` → `apt update && apt install sudo` → `usermod -aG sudo <用户>` → `sudo whoami`。
- sudoers 损坏的三段式错误（world writable / no valid sources / policy plugin）出现时，sudo 已完全不可用。
- 标准权限 0440、root:root；恢复分级：`su -` → `pkexec` → Live CD/挂盘。
- 修复后必跑 `sudo visudo -c`；永远用 visudo 编辑 sudoers，别用 vim/nano 直接改。

下一章（最后一章）把第 3 到第 7 章的命令串成一张从最小化安装到安全使用 sudo 的总结清单，并沉淀安全最佳实践。

---

## 第 8 章：安全最佳实践与总结

最后一章不再介绍新操作，把第 3 到第 7 章沉淀成两条可以带走的东西：一份安全使用 sudo 的原则清单，和一张从最小化安装到安全使用 sudo 的完整步骤速查表。安全不是某一刻的配置动作，而是贯穿「编辑方式、授权粒度、验证习惯」的日常纪律。

### 8.1 核心安全要点

> [!warning] 三条红线
> 它们决定了 sudo 配置是「可维护」还是「炸弹」[Debian Wiki — sudo](https://wiki.debian.org/sudo)：
>
> - **只经 `visudo` 编辑，绝不直接改 `/etc/sudoers`**。sudoers 故意设为只读（root 也只读），`visudo` 提供排他锁、保存时语法校验和错误回滚；vim/nano 直接编辑一旦写错，sudo 会整个失效。本地改动应放 `/etc/sudoers.d/` 片段文件，避开系统包升级覆盖 [RHEL9 官方文档](https://docs.redhat.com/zh-cn/documentation/red_hat_enterprise_linux/9/html/configuring_basic_system_settings/managing-sudo-access_configuring-basic-system-settings)。
> - **避免 `NOPASSWD: ALL` 与宽泛 `ALL=(ALL) ALL`**。这类规则对「任何命令、任何运行用户」放行，拿到该账号的人就等于拿到了 root；免密只应针对小范围、低风险的绝对路径命令 [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)。
> - **按组管理，不逐用户写规则**。Debian 用 `sudo` 组、组规则 `%sudo ALL=(ALL:ALL) ALL` 一处维护，比在 sudoers 里逐个用户加 `ALL` 行更容易审计与撤销；免密（NOPASSWD）本身也应作为安全审计项定期复查。

权限底线再强调一次：`/etc/sudoers` 与片段文件必须是 **0440、属主 root:root**；违反它会触发第 7 章的「world writable」类错误。

### 8.2 总结清单

#### 从最小化安装到安全使用 sudo：完整步骤速查表

| 阶段 | 命令 / 操作 | 关键点 |
| --- | --- | --- |
| ① 切到 root | `su -` | 必须带 `-`，加载完整 PATH，否则 apt 找不到 |
| ② 安装 sudo | `apt update && apt install sudo -y` | `apt update` 必须先跑（第 7 章） |
| ③ 加入 sudo 组 | `usermod -aG sudo <用户名>`（或 `adduser <用户名> sudo`） | 必须 `-a` 追加，别覆盖已有附属组（第 3 章） |
| ④ 刷新会话 | 注销重登 / `su - $USER` / `newgrp sudo` | 组身份只在登录时读取（第 3 章） |
| ⑤ 验证 | `id` 看 `27(sudo)`，再 `sudo whoami` 输出 `root` | 第 3 章验证链 |
| ⑥ 安全编辑（可选） | `sudo visudo -c` 校验；片段用 `sudo visudo -f /etc/sudoers.d/99-custom-ops` | 文件 0440、root:root（第 4 章） |
| ⑦ 密码管理（可选） | `passwd` 改自己的（即 sudo 要的密码）；`sudo passwd root` 改 root 密码 | sudo 默认要当前用户密码，非 root（3.5） |

#### 常见坑速查

| 常见坑 | 现象 | 正确做法 |
| --- | --- | --- |
| 加组未重登 | `Sorry, user ... is not allowed to execute` | 注销重登或 `su - $USER` 刷新会话（第 6 章） |
| `%sudo` 行被注释/缺失 | `user is not in the sudoers file` | `visudo` 确认 `%sudo ALL=(ALL:ALL) ALL` 存在未注释（第 6 章） |
| 直接改 sudoers | 语法错误 → sudo 全部失效 | 只用 `visudo`；权限保持 0440（第 7 章） |
| `su` 不带 `-` | 切 root 后命令找不到 | 统一用 `su -`（第 2 章） |
| `apt update` 未先跑 | `apt install sudo` 失败 | 先 `apt update` 再 install（第 3 章） |
| 拿 root 密码去输 sudo | `sudo` 一直报密码错误 | sudo 要的是**当前用户密码**；root 密码只在 `su -` 用（3.5） |

### 本章小结

- 三条红线：只经 `visudo` 编辑、避免 `NOPASSWD: ALL` 与宽泛 `ALL=(ALL) ALL`、按组管理便于审计撤销。
- sudoers 及片段权限必须 0440、root:root。
- 完整链路：`su -` → 装 sudo → 加组 → 刷新会话 → 验证 → 需要时用 `visudo` 管理片段。
- 五类常见坑各有对应修复，都能回溯到前面章节的具体章节。

到此，从「最小化安装为什么没有 sudo」到「sudoers 损坏恢复」的全流程已经闭环。把这些表和红线截图或抄到你的运维速查里，日常遇到 sudo 问题时按「验证会话 → 查 `%sudo` 行 → 校验配置」的顺序排查，就能覆盖绝大多数场景。

---

## 更新记录

- 2026-08-29：第 3 章新增 3.5「密码机制：sudo 要的密码是什么」，补充密码修改、root 密码管理、缓存时长配置；第 8 章速查表同步更新。

## 相关笔记

- [[linux/linux MOC]] — Linux 系统学习索引
- [[项目实战/debian实战/Debian 最小化安装后 sudo 权限配置]] — 本文
