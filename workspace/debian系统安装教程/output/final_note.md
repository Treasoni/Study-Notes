# Debian 系统安装教程

本教程从零开始，完整覆盖 Debian 操作系统的安装、配置与维护全流程。无论你是从 Ubuntu 转过来的有经验的 Linux 用户，还是第一次接触 Debian 的新手，这份教程都能帮你理清 Debian 的版本体系、完成系统安装、做好基础与安全配置，并掌握日常管理中的关键技能。全文共八章，逐层递进，从概述到实战再到排错，形成一条完整的学习路径。

---

## 目录

1. [第一章：Debian 概述与版本选择](#第一章debian概述与版本选择)
   - [1.1 什么是 Debian](#11-什么是-debian)
   - [1.2 版本分支体系](#12-版本分支体系)
   - [1.3 Debian 12 Bookworm 新特性](#13-debian-12-bookworm-新特性)
   - [1.4 架构支持](#14-架构支持)
2. [第二章：安装前的准备工作](#第二章安装前的准备工作)
   - [2.1 选择并下载镜像](#21-选择并下载镜像)
   - [2.2 制作安装介质](#22-制作安装介质)
   - [2.3 硬件要求](#23-硬件要求)
   - [2.4 UEFI vs Legacy BIOS](#24-uefi-vs-legacy-bios)
   - [2.5 Secure Boot](#25-secure-boot)
3. [第三章：安装步骤全流程](#第三章安装步骤全流程图形安装器)
   - [3.1 启动安装](#31-启动安装)
   - [3.2 语言与区域设置](#32-语言与区域设置)
   - [3.3 网络配置](#33-网络配置)
   - [3.4 主机名和用户](#34-主机名和用户)
   - [3.5 磁盘分区](#35-磁盘分区)
   - [3.6 软件包选择](#36-软件包选择)
   - [3.7 GRUB 引导加载器](#37-grub-引导加载器)
   - [3.8 完成安装](#38-完成安装)
4. [第四章：安装后基础配置](#第四章安装后基础配置)
   - [4.1 首次登录与系统检查](#41-首次登录与系统检查)
   - [4.2 配置国内 APT 源](#42-配置国内-apt-源)
   - [4.3 配置 Sudo 权限](#43-配置-sudo-权限)
   - [4.4 系统更新](#44-系统更新)
   - [4.5 时区与时间同步](#45-时区与时间同步)
   - [4.6 防火墙基础配置](#46-防火墙基础配置)
5. [第五章：桌面环境与中文配置](#第五章桌面环境与中文配置)
   - [5.1 选择桌面环境](#51-选择桌面环境)
   - [5.2 配置中文语言支持](#52-配置中文语言支持)
   - [5.3 中文输入法配置](#53-中文输入法配置)
6. [第六章：服务器安全加固](#第六章服务器安全加固)
   - [6.1 创建 Sudo 用户](#61-创建-sudo-用户)
   - [6.2 SSH 密钥认证](#62-ssh-密钥认证推荐)
   - [6.3 SSH 加固](#63-ssh-加固)
   - [6.4 配置 UFW 防火墙](#64-配置-ufw-防火墙)
   - [6.5 Fail2ban 入侵防护](#65-fail2ban-入侵防护)
   - [6.6 自动安全更新](#66-自动安全更新)
   - [6.7 进阶加固](#67-进阶加固可选)
7. [第七章：软件包管理与版本升级](#第七章软件包管理与版本升级)
   - [7.1 APT 常用命令速查](#71-apt-常用命令速查)
   - [7.2 Backports 源](#72-backports-源)
   - [7.3 版本升级](#73-版本升级)
8. [第八章：常见问题与排错](#第八章常见问题与排错)
   - [8.1 GRUB 安装失败](#81-grub-安装失败)
   - [8.2 GRUB 引导损坏](#82-grub-引导损坏)
   - [8.3 网卡固件缺失](#83-网卡固件缺失)
   - [8.4 中文显示为方块](#84-中文显示为方块)
   - [8.5 双系统时间不一致](#85-双系统时间不一致)
   - [8.6 安装器找不到 U 盘](#86-安装器找不到-u-盘)
   - [8.7 APT GPG 密钥错误](#87-apt-gpg-密钥错误)

---

## 第一章：Debian 概述与版本选择

Debian 是历史最悠久、影响最深远的 Linux 发行版之一。它不仅是 Ubuntu、Kali Linux、Linux Mint 等众多发行版的基石，其本身也是一套极其稳定可靠的操作系统。本章帮助你理解 Debian 的定位、版本管理体系，以及如何根据自己的需求选择合适的版本。

### 1.1 什么是 Debian

Debian 项目始于 1993 年，由 Ian Murdock 发起，是**社区驱动**的 Linux 发行版。与 Ubuntu（由 Canonical 公司商业主导）不同，Debian 的决策遵循 **Debian 社会契约**（Debian Social Contract）和 **Debian 自由软件准则**（DFSG），社区投票决定项目走向。

> Debian vs Ubuntu：两者的关系可以概括为"父子关系"。Ubuntu 每 2 年从 Debian 的 Testing 或 Unstable 分支取一个快照作为起点，在此基础上定制桌面体验、预装软件和驱动。因此 Debian 是"上游"，Ubuntu 是"下游"。

### 相同点
由于同源，Debian 和 Ubuntu 共享大量底层特性：

- 包管理：均使用 **apt/dpkg** 和 `.deb` 包格式
- Init 系统：均使用 **systemd**，systemctl/journalctl 命令行为完全一致
- 安全框架：均默认启用 **AppArmor**

### 核心差异

| 维度 | Debian | Ubuntu |
|------|--------|--------|
| 维护方 | 社区志愿者 | Canonical 公司 |
| 发布节奏 | 约 2 年，"准备好了才发布" | 固定双年 LTS（4 月） |
| 免费支持 | ~5 年（3 年全量 + 2 年 LTS） | 5 年 |
| 最长支持 | ~5 年 | 12 年（Ubuntu Pro） |
| 包管理 | APT 仅 | APT + Snap（默认） |
| 第三方源 | 无 PPA | PPA 生态 |
| 服务器资源 | ~512MB RAM 可运行 | ~1GB RAM 起 |

### 1.2 版本分支体系

Debian 有三条主要分支，理解它们的差异是入门的第一步。

### Stable（稳定版）

- **代号**：当前为 **Bookworm**（Debian 12）
- **特点**：经过长期测试，软件包冻结后只接受安全修复和关键补丁
- **适合**：生产服务器、要求长期稳定的桌面、任何"设好就不用管"的场景
- **软件版本**：相对保守，但从不出其不意地坏掉

### Testing（测试版）

- **当前代号**：**Trixie**（Debian 13，下一个稳定版）
- **特点**：持续从 Unstable 流入经过一定测试的软件包，滚动更新
- **适合**：桌面用户、开发者，希望使用较新软件但不希望太激进
- **稳定性**：比 Stable 差但比 Unstable 好，偶有回归

### Unstable（不稳定版/Sid）

- **代号**：永远叫 **Sid**（取自《玩具总动员》中总搞破坏的小孩）
- **特点**：持续滚动，永远在接收上游最新软件
- **适合**：Debian 开发者和打包者、愿意频繁维护的高级用户
- **稳定性**：不承诺稳定，可能出现包依赖断裂

> [!tip] 选哪个？
> - 新手或生产环境 → **Stable（Bookworm）**
> - 桌面用户想用新软件 → **Testing（Trixie）**
> - 参与开发或打包 → **Unstable（Sid）**

### 1.3 Debian 12 Bookworm 新特性

Debian 12（2023 年 6 月发布）引入了几项重要变化，对安装和使用影响显著：

### non-free-firmware

**最大的变化**：之前 Debian 将非自由固件放在 `non-free` 仓库，默认不启用。Bookworm 起新增加 **`non-free-firmware`** 组件，专门存放固件类闭源驱动。

安装时若选择包含非自由固件的安装镜像（推荐），Wi-Fi 和某些有线网卡可以开箱即用；若使用纯自由软件镜像，仍需手动启用此源。

### 其他亮点

- 默认搭载 **Linux 6.1 LTS** 内核（长期支持）
- 官方支持 **RISC-V 64** 架构（实验性）
- Wayland 取代 X11 成为默认显示服务器（GNOME 桌面）
- 安装器改进：更好的 NVMe 磁盘支持
- 超过 **11,000 个新软件包**，总量超 60,000

### 1.4 架构支持

Debian 12 官方支持以下架构：

| 架构 | 说明 | 常见场景 |
|------|------|---------|
| **amd64** (x86_64) | 64 位 x86 架构 | 桌面 PC、服务器（最常用） |
| **arm64** (AArch64) | 64 位 ARM 架构 | 树莓派、ARM 服务器、Apple Silicon |
| **armhf** | 32 位 ARM hard-float | 嵌入式设备、旧款树莓派 |
| **i386** | 32 位 x86 | 老旧 PC（Debian 12 起不再包含在稳定版中，仅 Testing/Unstable 保留） |
| **ppc64el** | PowerPC 小端序 | IBM POWER 服务器 |
| **s390x** | IBM System z | 大型机 |
| **RISC-V 64** | 开放指令集架构 | 实验性，Debian 12 首发 |

> 对比 Ubuntu：Ubuntu 26.04 LTS 主要面向 amd64 和 arm64，Debian 的架构覆盖更广，尤其在非 x86 领域优势明显。

### 章节总结

- Debian 是社区驱动的 Linux 发行版，是 Ubuntu 的"上游"
- 三条分支各有定位：Stable 求稳、Testing 求新、Unstable 求变
- Debian 12 Bookworm 新增 `non-free-firmware` 组件，改善了硬件驱动体验
- Debian 支持的硬件架构远多于 Ubuntu

---

了解了 Debian 的版本体系和分支选择之后，接下来我们进入实际操作阶段。安装前的准备工作是确保整个安装过程顺利的关键——从选择合适的镜像、制作启动介质，到确认硬件兼容性和 BIOS 设置，下一章将为你一一梳理。

---

## 第二章：安装前的准备工作

安装 Debian 之前做好充分准备，可以避免安装过程中大部分常见问题。本章涵盖镜像下载与选择、安装介质制作、硬件要求，以及 UEFI 和 Secure Boot 等关键概念。

### 2.1 选择并下载镜像

### 镜像类型对比

| 镜像类型 | 大小 | 说明 |
|----------|------|------|
| **netinst**（网络安装） | ~600 MB | 仅含基础系统和安装器，其余软件包从网络下载 |
| **DVD-1** | ~4.7 GB | 单张 DVD，包含大部分常用软件包，可离线安装 |
| **BD-1** | ~12 GB | 蓝光盘，包含几乎所有软件包 |
| **Live** | ~3 GB | 可试用再安装，含桌面环境 |

> [!tip] 日常推荐
> 普通用户下载 **netinst** 镜像即可。安装时选择国内镜像源（如清华 TUNA），下载速度不比 DVD 慢。如果你的网络环境不稳定或无法联网，则选 DVD-1。

### 下载地址

**官方入口**：https://www.debian.org/download

**国内镜像（推荐，速度更快）**：

- 清华 TUNA：https://mirrors.tuna.tsinghua.edu.cn/debian-cd/current/amd64/iso-cd/
- 阿里云：https://mirrors.aliyun.com/debian-cd/current/amd64/iso-cd/
- 中科大 USTC：https://mirrors.ustc.edu.cn/debian-cd/current/amd64/iso-cd/

选择 `debian-12.x.x-amd64-netinst.iso` 文件，旁边有 `SHA256SUMS` 可验证完整性。

### 固件镜像（推荐）

如果硬件较新（尤其是 Intel/Realtek 无线网卡），建议下载**包含非自由固件的非官方镜像**，安装时网卡可直接识别：

https://cdimage.debian.org/images/unofficial/non-free/images-daily/

> Debian vs Ubuntu：Ubuntu 安装镜像开箱即包含大量闭源驱动，Debian 的纯自由软件镜像不含 non-free 固件。从 Ubuntu 转过来的用户如果发现安装器认不出网卡，很可能就是因为这个原因。

### 2.2 制作安装介质

### Linux / macOS（命令行）

```bash
# 1. 确认 U 盘设备名（⚠️ 确认正确，不要写错盘）
lsblk                    # Linux
diskutil list            # macOS

# 2. 写入镜像（/dev/sdX 替换为实际设备，如 /dev/sdb）
sudo dd if=debian-12.5.0-amd64-netinst.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

> [!warning] 注意
> `dd` 命令会**完全覆盖目标设备**的所有数据，务必再三确认设备名。写完后如果 Windows 弹出"未格式化"提示，直接关闭即可，**不要格式化**。

### Windows

- **Rufus**（推荐）：https://rufus.ie — 选择镜像后，在"镜像选项"中选择 **"DD 镜像写入"** 模式
- **BalenaEtcher**：https://www.balena.io/etcher — 操作简单，自动识别

### 2.3 硬件要求

| 场景 | 最低配置 | 推荐配置 |
|------|---------|---------|
| 桌面（GNOME） | 2 GB RAM, 10 GB 磁盘 | 4 GB RAM, 40 GB 磁盘 |
| 桌面（Xfce） | 1 GB RAM, 8 GB 磁盘 | 2 GB RAM, 20 GB 磁盘 |
| 服务器 | 512 MB RAM, 2 GB 磁盘 | 2 GB RAM, 20 GB 磁盘 |

> Debian vs Ubuntu：Debian 的资源占用显著低于 Ubuntu。一台 512MB RAM 的 VPS 可以流畅运行 Debian 服务器，但运行 Ubuntu Server 会非常吃力。这是低配机器选 Debian 而非 Ubuntu 的最大理由。

### 2.4 UEFI vs Legacy BIOS

现代电脑几乎都是 **UEFI** 模式，但也兼容 Legacy BIOS。关键区别：

| 项目 | UEFI | Legacy BIOS |
|------|------|-------------|
| 分区表 | GPT | MBR |
| 引导分区 | ESP（EFI System Partition, FAT32, ~512 MB） | 无专用分区 |
| 磁盘限制 | 无（支持 >2TB 磁盘） | 最大 2TB |
| 启动速度 | 较快 | 较慢 |
| Secure Boot | 支持 | 不支持 |

**实操建议**：保持 BIOS 中的默认 UEFI 模式即可。Debian 安装器会自动检测并选择匹配的引导方式。如需双系统，确保 Windows 和 Debian 使用相同的引导模式（通常是 UEFI）。

### 2.5 Secure Boot

Secure Boot 是 UEFI 的安全功能，防止未签名的引导加载器运行。Debian 12 的 GRUB 和内核均已签名，对 Secure Boot 的支持已比较完善。

> [!warning] 还是建议关闭
> 虽然 Debian 12 支持 Secure Boot，但某些显卡驱动（如 NVIDIA 闭源驱动）和 DKMS 模块在 Secure Boot 开启时可能无法加载。如果遇到引导问题，进 BIOS 关闭 Secure Boot 是最直接的排查方法。

**BIOS 进入快捷键**（各品牌不同）：

| 品牌 | 快捷键 |
|------|--------|
| 联想 / ThinkPad | F1 或 F2 |
| Dell | F2 |
| HP | Esc 或 F10 |
| 华硕 | F2 或 Del |
| 组装机 | Del |

启动设备选择通常在 F12（开机时屏幕通常有短暂提示）。

### 章节总结

- netinst 镜像对大多数场景够用，搭配国内源速度不慢
- 新硬件建议下载包含 non-free 固件的镜像确保网卡识别
- U 盘写入用 `dd` 或 Rufus（DD 模式），注意不要写错设备
- UEFI + GPT 是现代标准，Legacy BIOS + MBR 仅用于老机器
- Secure Boot 建议关闭以减少驱动兼容性问题

**下一章**：准备工作就绪后，插入 U 盘启动，进入安装器完成系统安装。

---

准备工作就绪后，就可以正式进入 Debian 的安装流程了。从启动安装介质开始，到磁盘分区、软件包选择，再到 GRUB 引导加载器的安装，下一章将带你完整走一遍图形安装器的每个步骤。

---

## 第三章：安装步骤全流程（图形安装器）

本章带你走完 Debian 12 的完整安装流程，从启动安装介质到重启进入桌面/终端。每种选择对应的原因和坑都会标注。

### 3.1 启动安装

1. 插入制作好的安装 U 盘
2. 开机按启动设备快捷键（通常是 F12），选择 U 盘
3. 看到 Debian 安装菜单后：

```
Debian GNU/Linux 安装菜单
┌──────────────────────────────────┐
│ Graphical install                │ ← 图形安装（推荐）
│ Install                          │ ← 文本模式安装
│ Advanced options                 │ ← 高级选项
│ Help                             │
└──────────────────────────────────┘
```

**选择 `Graphical install`**。如果显卡不兼容导致花屏，重启选 `Install`（文本模式），操作完全一致。

### 3.2 语言与区域设置

| 步骤 | 推荐选项 | 原因 |
|------|---------|------|
| 安装语言 | **English** | 减少终端乱码风险，中文可在装完后配置 |
| 所在位置 | other → Asia → China | 正确设置时区和镜像源候选 |
| locale | **zh_CN.UTF-8** | 后续中文支持需要此 locale |
| 键盘布局 | **American English** | 标准美式键盘布局 |

> [!note] 为什么不装时就选中文
> 安装界面选中文虽然方便，但会导致控制台更容易出现字符显示问题。建议装时用英文，装完后配置中文环境和输入法。

### 3.3 网络配置

安装器会自动检测网卡：

- **DHCP（默认）**：自动获取 IP，适合家庭路由器环境
- **静态 IP**：点击手动配置，输入 IP、掩码、网关、DNS

Wi-Fi 用户安装器会提示选择无线网络和输入密码。如果有线连接可用，建议先插网线，比 Wi-Fi 更稳定。

### 3.4 主机名和用户

```
Hostname: debian-server      # 主机名，局域网内唯一即可留空
Domain name: (留空)           # 非局域网环境可留空
Root password: (设置强密码)    # ⚠️ 重要：Debian 默认设置 root 密码
```

### Root 密码 vs Sudo

**Debian 的默认做法**：安装时必须设置 root 密码。如果不想每次用 root，有两个选择：

1. **设置 root 密码**，装完后自行将用户加入 sudo 组
2. **留空 root 密码** — 安装器会提示"root 密码为空"，确认后将第一个用户自动加入 sudo 组（行为和 Ubuntu 默认一致）

> Debian vs Ubuntu：Ubuntu 安装时不设 root 密码，第一个用户自动获得 sudo 权限。Debian 默认走传统路线——设 root 密码、用户需要手动加入 sudo。这是 Ubuntu 用户切换到 Debian 最容易困惑的地方之一。

**后续填入**：

```
Full name: Your Name          # 全名，仅用于显示
Username: your-username       # 登录用户名
Password: (用户密码)           # 日常使用的密码
```

### 3.5 磁盘分区

这是安装中最关键的步骤。Debian 安装器提供三种方案。

### 方案 A：全盘自动分区（推荐新手）

选择 **Guided - use entire disk**，然后选：

- **All files in one partition** — 最简方案，一个 `/` 分区 + swap
- **Separate /home partition** — `/home` 独立分区，重装系统时数据不丢
- **Separate /home, /var, /tmp** — 服务器隔离场景，提高安全性

### 方案 B：LVM 全盘加密

选择 **Guided - use entire disk and set up LVM encrypted**：

- 提供 LUKS 全盘加密，开机需输入解密密码
- 适合笔记本或存放敏感数据的服务器
- 性能开销极小（现代 CPU 有 AES 硬件加速）

### 方案 C：手动分区（有经验的用户）

| 挂载点 | 大小 | 文件系统 | 说明 |
|--------|------|----------|------|
| `/boot` | 1 GB | ext4 | 引导分区（UEFI 需要 EFI System Partition，格式 FAT32） |
| `/` | 20-50 GB | ext4 | 根分区，系统和软件 |
| `/home` | 剩余 | ext4 | 用户数据（可选独立分区） |
| `swap` | RAM 大小或 2 GB | swap | 交换空间（可选，有休眠需求时必须设置） |

> [!tip] 分区建议
> - 桌面用户：方案 A 的 "Separate /home" 即可，重装不丢数据
> - 服务器：方案 A 的分离式布局或手动分区，`/var` 独立防止日志写满根分区
> - 笔记本：方案 B 的加密方案

### 3.6 软件包选择

安装器会提示选择额外软件：

```
[*] Debian desktop environment      # 桌面环境（服务器不选）
[*] ... GNOME                       # 默认桌面
[ ] ... Xfce                        # 轻量桌面
[ ] ... KDE Plasma                  # 华丽桌面
[*] SSH server                      # 远程管理（建议必选）
[ ] web server                      # LAMP 栈
[ ] print server                    # 打印服务
[*] standard system utilities       # 常用命令行工具（建议必选）
```

> Debian vs Ubuntu：Ubuntu 安装器只有简化的分类勾选（"安装时下载更新"、"安装第三方软件"），Debian 使用 tasksel，选项更细。另外 Debian 默认不装 Snap，也不用 Snap 版的 Firefox。

### 3.7 GRUB 引导加载器

安装器自动检测引导模式（UEFI 或 Legacy）并安装对应的 GRUB：

- 提示"安装 GRUB 引导加载器到主引导记录" → 选择 **Yes**
- 如果有多个磁盘，选系统盘（通常是 `/dev/sda` 或 `/dev/nvme0n1`）

UEFI 模式下，安装器会自动创建或检测现有的 EFI System Partition 并挂载到 `/boot/efi`。

### 3.8 完成安装

安装进度条走完后，取出 U 盘，点击 **Continue** 重启。

重启后你应该看到 GRUB 菜单，默认选项会自动启动新安装的 Debian。首次启动会看到一些服务初始化日志，然后出现登录提示符（服务器）或登录管理器（桌面）。

### 章节总结

- 安装语言选 English 减少终端乱码，后续再配中文
- 磁盘分区：新手用全盘自动分区，隔离需求选分离式，敏感场景选 LUKS 加密
- SSH server 和 standard system utilities 建议必选
- 如果留空 root 密码，Debian 行为会与 Ubuntu 的 sudo 模式一致
- UEFI + GPT 下安装器自动处理 ESP 分区

**下一章**：系统装完了，第一步是配置国内 APT 源、更新系统和基础网络设置。

---

系统安装完成后，你面对的是一个干净的 Debian 基础系统——相当于刚建好的毛胚房。接下来需要进行一系列基础配置，包括更换国内 APT 源、配置 sudo 权限、设置时区和防火墙，让系统真正可用且安全。

---

## 第四章：安装后基础配置

Debian 装完只是一个"毛胚房"。本章带你完成系统级的基础配置，包括 APT 源优化、sudo 权限、系统更新、时区同步和防火墙。

### 4.1 首次登录与系统检查

以安装时创建的用户登录后，先做个基本检查：

```bash
# 查看 Debian 版本
cat /etc/debian_version
# 输出类似：12.5

# 查看内核版本
uname -a

# 查看系统信息
lsb_release -a

# 检查网络连通性
ping -c 4 debian.org
```

如果安装时选了桌面环境，直接看到登录管理器（GDM / LightDM / SDDM）的图形界面；如果只装了服务器，看到的是终端登录提示。

### 4.2 配置国内 APT 源

Debian 安装时的默认源指向 deb.debian.org（位于欧洲），在国内速度很慢。必须换成国内镜像。

```bash
# 备份原始源列表
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 使用清华镜像（Debian 12 Bookworm）
sudo tee /etc/apt/sources.list << 'EOF'
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
EOF
```

```bash
# 更新软件包索引并升级
sudo apt update && sudo apt upgrade -y
```

### sources.list 组件说明

| 组件 | 说明 | 是否需要 |
|------|------|---------|
| `main` | 符合 DFSG 的自由软件 | 必选 |
| `contrib` | 依赖非自由软件的自由软件 | 推荐 |
| `non-free` | 非自由软件（如某些驱动） | 按需 |
| `non-free-firmware` | 非自由固件（Wi-Fi 网卡、GPU 等） | **强烈推荐** |

> Debian vs Ubuntu：Ubuntu 安装后 `/etc/apt/sources.list` 已经预置了国内源选择并包含 `restricted/universe/multiverse` 组件。Debian 需要手动改源并添加 `non-free-firmware`。另外 Debian 不使用 PPA，装第三方软件用 Backports 或手动安装 `.deb`。

### 其他国内镜像源

```bash
# 阿里云
deb https://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware

# 中科大 USTC
deb https://mirrors.ustc.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.ustc.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

### 4.3 配置 Sudo 权限

如果安装时设置了 root 密码，当前用户还没有 sudo 权限：

```bash
# 切换到 root
su -

# 将用户加入 sudo 组
usermod -aG sudo your-username

# 退出并重新登录使生效
exit
```

退出当前会话重新登录后，验证：

```bash
sudo whoami
# 输出应为：root
```

### 4.4 系统更新

```bash
sudo apt update && sudo apt upgrade -y
```

`apt update` 更新软件包索引，`apt upgrade` 升级所有可升级的包。首次安装后通常有几十个安全更新。

### 4.5 时区与时间同步

```bash
# 设置时区
sudo timedatectl set-timezone Asia/Shanghai

# 查看时间状态（确认 NTP 已启用）
timedatectl status
```

输出应包含：

```
Local time: Thu 2026-07-29 20:00:00 CST
Universal time: Thu 2026-07-29 12:00:00 UTC
Time zone: Asia/Shanghai (CST, +0800)
NTP enabled: yes
NTP synchronized: yes
```

如果 `NTP synchronized: no`，手动启动：

```bash
sudo timedatectl set-ntp true
```

### 4.6 防火墙基础配置

Debian 默认不启用防火墙。配置 UFW（Uncomplicated Firewall）是最简单的方式：

```bash
# 安装 UFW
sudo apt install ufw

# 设置默认策略：拒绝入站，允许出站
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许 SSH（务必先做，否则远程会被断连）
sudo ufw allow ssh

# 按需开启其他端口
sudo ufw allow http     # 80/tcp
sudo ufw allow https    # 443/tcp

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status verbose
```

> [!warning] 远程 SSH 操作
> 如果是通过 SSH 远程连接，在启用 UFW 之前**必须**先执行 `sudo ufw allow ssh`，否则防火墙一开 SSH 连接立刻断开，你将被锁在服务器外。

### 章节总结

- 更换国内 APT 源是安装后的第一要务，建议用清华/阿里/中科大
- 务必添加 `non-free-firmware` 组件，否则某些硬件无法工作
- 如果安装了 root 密码，主动将日常用户加入 sudo 组
- 配置时区和 NTP 同步，避免日志时间混乱
- UFW 防火墙三步走：设默认策略 → 允许 SSH → 启用

**下一章**：如果是桌面用户，接下来配置中文环境和输入法；如果是服务器场景，可跳至第六章进行安全加固。

---

如果你安装的是桌面环境，还需要额外配置中文支持和输入法才能获得舒适的日常使用体验。如果安装的是纯服务器，可以跳过下一章直接进入安全加固环节。

---

## 第五章：桌面环境与中文配置

如果安装时选择了桌面环境，重启后即可进入图形界面。本章涵盖桌面环境选择、中文语言配置和中文字体、输入法安装。

### 5.1 选择桌面环境

Debian 12 提供了多种桌面环境，安装时只能选一个，但后期可以随时添加。

### 桌面对比

| 桌面 | 资源占用 | 特点 | 适合谁 |
|------|---------|------|--------|
| **GNOME** | 较高（2GB+） | Debian 默认桌面，功能完整，Wayland 原生 | 喜欢现代简约风格的用户 |
| **KDE Plasma** | 中等 | 高度可定制，界面华丽，Fcitx5 支持最佳 | 喜欢自定义、Windows 迁移用户 |
| **Xfce** | 低（1GB 可跑） | 经典传统桌面，稳定快速 | 旧硬件、追求性能 |
| **LXDE / LXQt** | 极低 | 最轻量级桌面 | 极低配置设备 |
| **Cinnamon** | 中等 | 类 Windows 传统布局 | Linux Mint 用户习惯 |

> Debian vs Ubuntu：Ubuntu 的 GNOME 经过深度定制（左侧 dock、自定义主题），Debian 的 GNOME 是**上游原版**，更简洁。Firefox 在 Debian 上是以 APT 包安装的，不是 Snap 版，启动更快、资源更少。

### 后期安装桌面

如果安装时没有装桌面，可以后续补充：

```bash
# GNOME（推荐，默认）
sudo apt install task-gnome-desktop

# KDE Plasma
sudo apt install task-kde-desktop

# Xfce（轻量）
sudo apt install task-xfce-desktop

# 安装后重启进入图形界面
sudo systemctl reboot
```

### 5.2 配置中文语言支持

### 安装 locale 和语言支持

```bash
# 安装 locale 支持
sudo apt install locales

# 配置 locale（勾选 zh_CN.UTF-8 和 en_US.UTF-8）
sudo dpkg-reconfigure locales
```

在弹出的界面中：
1. 用方向键滚动找到 `zh_CN.UTF-8 UTF-8`，按空格选中（带 `*`）
2. 按 Tab 跳到 OK，回车
3. 在默认 locale 界面选择 `zh_CN.UTF-8`

```bash
# 验证当前 locale
locale
```

输出应包含 `LANG=zh_CN.UTF-8`。

### 安装中文字体

```bash
# 推荐：Noto CJK 字体（Google 出品，覆盖中/日/韩）
sudo apt install fonts-noto-cjk

# 或文泉驿字体（传统中文微米黑/正黑）
sudo apt install fonts-wqy-microhei fonts-wqy-zenhei
```

验证字体安装：

```bash
fc-list :lang=zh | head -5
```

### 5.3 中文输入法配置

Debian 12 主流的输入法方案有两种：**Fcitx5**（通用推荐）和 **IBus**（GNOME 原生）。

### 方案一：Fcitx5（推荐，全桌面通用）

```bash
# 安装 Fcitx5 核心和拼音引擎
sudo apt install fcitx5 fcitx5-chinese-addons fcitx5-config-qt
```

配置环境变量（编辑 `~/.bashrc`，在末尾添加）：

```bash
export GTK_IM_MODULE=fcitx5
export QT_IM_MODULE=fcitx5
export XMODIFIERS=@im=fcitx5
```

设置 Fcitx5 为默认输入法框架：

```bash
im-config -n fcitx5
```

**重启或注销重新登录**后，在系统托盘找到 Fcitx5 键盘图标，右键进入配置，在"输入法"中添加 "拼音"。

### 方案二：IBus（GNOME 原生）

```bash
# 安装 IBus 和智能拼音
sudo apt install ibus ibus-libpinyin

# 设置默认框架
im-config -n ibus
```

GNOME 用户打开 **设置 → 键盘 → 输入源**，点击 "+" 添加 **汉语（智能拼音）**。

| 方案 | 适用桌面 | 特点 |
|------|---------|------|
| Fcitx5 | KDE / Xfce / GNOME | 功能全面，配置灵活，Wayland 兼容性好 |
| IBus | GNOME（原生） | 开箱即用，系统深度整合 |

> [!tip] 建议
> KDE 和 Xfce 用户选 Fcitx5，GNOME 用户两个都行，推荐 Fcitx5。

### 中文输入法常见问题

**Wayland 下浏览器无法输入中文**：Chrome/Chromium 在 Wayland 下使用 Fcitx5 偶有问题。解决方案：

```bash
# 方案1：切换到 X11 会话（登录界面右下角选择）
# 方案2：安装 GNOME Shell 扩展 "Input Method Panel"
```

**Fcitx5 托盘图标不显示**：确认 `fcitx5` 已加入开机自启动。KDE 自动管理，Xfce 需手动添加：

```bash
# Xfce：设置 → 会话和启动 → 应用程序自启动 → 添加 fcitx5 -d
```

**终端中文乱码**：确认 locale 正确，终端编码为 UTF-8。GNOME Terminal 默认就是 UTF-8。

### 章节总结

- Debian 桌面是上游原版 GNOME，比 Ubuntu 的 GNOME 更简洁、资源更少
- 安装中文支持三步骤：locale → 字体 → 输入法
- Fcitx5 + 拼音 是全桌面通用的推荐方案
- Firefox 在 Debian 上走 APT 而非 Snap，体验更好

**下一章**：如果是服务器场景，或者想加固桌面系统的安全性，继续阅读安全配置。

---

无论你的 Debian 是作为桌面还是服务器使用，安全都是一项不可忽视的工作。下一章针对服务器场景深入介绍 SSH 加固、防火墙策略、Fail2ban 防护和自动安全更新等核心措施。

---

## 第六章：服务器安全加固

新装好的服务器默认配置以满足"能用"为目标，远未达到"安全"的标准。本章介绍 Debian 服务器初始化必须做的安全加固措施。

### 6.1 创建 Sudo 用户

如果安装时设置了 root 密码，应该创建一个日常使用的普通用户：

```bash
# 创建新用户
adduser deploy

# 加入 sudo 组
usermod -aG sudo deploy
```

日常操作使用此用户而非 root，可以防止误操作破坏系统。

> Debian vs Ubuntu：Ubuntu 安装时第一个用户默认就是 sudo 用户，不需要额外配置。

### 6.2 SSH 密钥认证（推荐）

密码登录容易被暴力破解，SSH 密钥认证既安全又方便。

```bash
# 本地机器上生成密钥对（如果还没有）
ssh-keygen -t ed25519 -f ~/.ssh/debian_server

# 将公钥复制到服务器
ssh-copy-id -i ~/.ssh/debian_server.pub deploy@your-server-ip
```

如果 `ssh-copy-id` 不可用，手动复制：

```bash
# 本地
cat ~/.ssh/debian_server.pub

# 服务器上
mkdir -p ~/.ssh && chmod 700 ~/.ssh
echo "your-public-key-content" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 6.3 SSH 加固

Debian 12 引入了 drop-in 配置目录 `/etc/ssh/sshd_config.d/`，推荐在此目录下创建自定义配置文件，避免直接修改主配置（方便后续升级）。

```bash
# 创建加固配置
sudo tee /etc/ssh/sshd_config.d/90-hardening.conf << 'EOF'
# 禁止 root 直接登录
PermitRootLogin no

# 禁用密码认证（仅密钥登录）
PasswordAuthentication no
KbdInteractiveAuthentication no

# 公钥认证
PubkeyAuthentication yes

# 限制登录尝试次数
MaxAuthTries 3

# 关闭 X11 转发
X11Forwarding no

# 客户端保活（300秒无操作发探测包，2次失败断开）
ClientAliveInterval 300
ClientAliveCountMax 2

# 限制可登录用户
AllowUsers deploy
EOF
```

验证配置并重启：

```bash
# 检查配置语法
sudo sshd -t

# 重启 SSH 服务
sudo systemctl restart sshd
```

> [!warning] 防锁死
> 重启 SSH 服务前保持一个已连接的会话窗口，万一配置有误还可以回滚。密钥登录测试通过后再关闭密码登录。

### 6.4 配置 UFW 防火墙

第四章介绍了 UFW 基础配置，服务器场景需要更严格的端口控制。只开放必要的端口：

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 只有 SSH 允许入站（按实际端口修改）
sudo ufw allow 22/tcp

# 如果跑 Web 服务，后续再开
# sudo ufw allow 80/tcp
# sudo ufw allow 443/tcp

sudo ufw enable
sudo ufw status verbose
```

### 6.5 Fail2ban 入侵防护

Fail2ban 监控日志文件，在检测到多次失败登录后临时封禁源 IP。

```bash
sudo apt install fail2ban
```

Debian 12 下 SSH 日志通过 systemd journal 记录，需要配置 backend：

```bash
# 创建 jail.local 覆盖默认配置
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
# 封禁时间 1 小时
bantime = 1h
# 检测窗口 10 分钟
findtime = 10m
# 最多失败 5 次
maxretry = 5

[sshd]
enabled = true
# 使用 systemd journal 作为日志后端
backend = systemd
EOF

sudo systemctl restart fail2ban
sudo fail2ban-client status sshd
```

### 6.6 自动安全更新

系统需要及时安装安全更新。Debian 提供了 `unattended-upgrades` 包：

```bash
sudo apt install unattended-upgrades apt-listchanges

# 配置自动更新
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

配置完成后确认定期更新策略：

```bash
sudo tee /etc/apt/apt.conf.d/20auto-upgrades << 'EOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
EOF
```

### 6.7 进阶加固（可选）

### 内核参数调优

```bash
sudo tee /etc/sysctl.d/99-hardening.conf << 'EOF'
# 防止 IP 欺骗
net.ipv4.conf.all.rp_filter = 1
# 禁止 ICMP 重定向
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
# 禁止源路由
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
# 开启 TCP SYN Cookie（防 SYN Flood）
net.ipv4.tcp_syncookies = 1
EOF

sudo sysctl -p
```

### AppArmor

Debian 默认启用 AppArmor（相比 Ubuntu 的 AppArmor 配置更轻量）：

```bash
# 检查状态
sudo aa-status

# 安装额外的 AppArmor 配置文件
sudo apt install apparmor-profiles apparmor-profiles-extra
```

### 安全审计

```bash
sudo apt install lynis
sudo lynis audit system
```

Lynis 会扫描系统并给出安全评分和改进建议。

### 其他

- **AIDE**：文件完整性监控，检测关键文件是否被篡改
- **Rkhunter**：Rootkit 扫描
- **debsecan**：查看已安装包中已知 CVE 漏洞

> Debian vs Ubuntu：Ubuntu Pro 内置 Livepatch（内核热修补）、CIS 合规基线、FIPS 模式，这些都是商业订阅覆盖的功能。Debian 社区提供等价的工具但需要手动配置。另外 Debian 资源占用低，可以在 512MB 的 VPS 上跑完整安全栈，Ubuntu 同配置会吃力很多。

### 章节总结

- 日常使用 sudo 用户，禁止 root 直接 SSH 登录
- SSH 密钥认证 + 禁用密码是最有效的单点安全措施
- UFW 防火墙只开放必要端口
- Fail2ban 防暴力破解，unattended-upgrades 保证安全更新及时到位
- AppArmor + sysctl 内核调优提供额外纵深防御

**下一章**：了解 Debian 的软件包管理哲学，从 APT 命令到 Backports 再到版本升级。

---

系统安全和基础配置都完成后，我们来深入了解一下 Debian 引以为傲的软件包管理体系。从日常的 APT 命令到 Backports 源的使用，再到版本跨级升级，掌握这些技能才能长期维护好你的 Debian 系统。

---

## 第七章：软件包管理与版本升级

Debian 的软件包管理是它最强的竞争力之一。本章从日常 APT 命令入手，延伸到 Backports 源和版本升级。

### 7.1 APT 常用命令速查

```bash
# 更新软件包索引（建议每次安装前执行）
sudo apt update

# 升级所有可升级的包
sudo apt upgrade

# 升级包括依赖变更（慎用，生产环境先手动检查变更）
sudo apt full-upgrade

# 安装软件包
sudo apt install package-name

# 删除软件包（保留配置文件）
sudo apt remove package-name

# 彻底删除（包括配置文件）
sudo apt purge package-name

# 搜索软件包
apt search keyword

# 查看软件包详细信息
apt show package-name

# 列出已安装的包
apt list --installed

# 清理没用到的依赖
sudo apt autoremove

# 清理下载缓存
sudo apt autoclean

# 修复 broken dependencies
sudo apt --fix-broken install
```

### dpkg 基础

APT 在底层依赖 dpkg。有时需要直接操作 dpkg：

```bash
# 安装 .deb 文件
sudo dpkg -i package.deb

# 查看已安装包
dpkg -l

# 查看某个文件属于哪个包
dpkg -S /path/to/file

# 重新配置已安装的包（如修改 locale）
sudo dpkg-reconfigure package-name
```

> Debian vs Ubuntu：命令完全一致。区别在于 Debian 默认不预装 Snap 和 PPA 机制。在 Debian 上装第三方软件，通常有三种方式：Backports（推荐）、Flatpak、或手动下载 `.deb`。没有 `add-apt-repository` 命令，但你可以用 `apt-get install python3-launchpadlib` 装上。

### 7.2 Backports 源

Backports 是从 Debian Testing 中精选较新软件包、重新编译以兼容 Stable 的仓库。让你在保持 Stable 主线稳定的同时，用上较新版本的特定软件（如新内核、新浏览器）：

```bash
# 查看有哪些软件可以从 backports 安装
apt search -t bookworm-backports package-name

# 安装 backports 版本的新内核
sudo apt install -t bookworm-backports linux-image-amd64

# 安装 backports 版本的软件
sudo apt install -t bookworm-backports wireguard
```

> Debian vs Ubuntu：Backports 的功能定位类似于 Ubuntu 的 HWE（Hardware Enablement）内核 + PPAs 的组合，但更保守——Backports 中的软件在 Testing 中已测试过再移植，不会像 PPA 一样由个人维护。

### 7.3 版本升级

在 Debian 稳定版之间升级（如 Bullseye → Bookworm → Trixie）是支持的，但需要遵循标准流程。

### 升级前注意事项

- 备份重要数据（至少 `/etc`、数据库、应用数据）
- 检查第三方源是否支持新版本
- 预留足够维护时间窗口
- **先在测试环境验证**

### Bullseye (11) → Bookworm (12) 升级步骤

```bash
# 1. 确保当前系统已完全更新
sudo apt update && sudo apt upgrade -y && sudo apt full-upgrade

# 2. 备份 /etc
sudo tar czf ~/backup-etc-$(date +%Y%m%d).tgz /etc

# 3. 修改源列表：替换 bullseye → bookworm
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/*.list 2>/dev/null || true

# 4. 更新索引并做最小升级
sudo apt update
sudo apt upgrade --without-new-pkgs -y

# 5. 完整升级
sudo apt full-upgrade -y

# 6. 清理
sudo apt autoremove --purge -y
sudo apt autoclean

# 7. 重启
sudo systemctl reboot

# 8. 验证
cat /etc/debian_version
```

### 升级后检查

```bash
# 检查是否有残留问题
sudo apt --fix-broken install

# 检查服务状态
systemctl --failed

# 确认关键服务正常运行
sudo systemctl status ssh nginx 2>/dev/null || true
```

### 多内核默认启动管理

升级后可能安装了多个内核版本，GRUB 默认选择最新。如需指定：

```bash
# 查看当前内核
uname -r

# 查看已安装的内核
dpkg -l | grep linux-image

# 查看 GRUB 菜单中可用的内核列表
grep -E "^menuentry" /boot/grub/grub.cfg

# 编辑 /etc/default/grub，设置 GRUB_DEFAULT
# 注意：GRUB 2.00+ 需要用长格式 ID
sudo vim /etc/default/grub

# 更新 GRUB 配置
sudo update-grub
```

### 章节总结

- APT 命令 Debain 和 Ubuntu 完全通用，不需要额外学习成本
- Backports 是在稳定系统上用新软件的安全方式
- Debian 的版本升级是可支持的，但需要提前备份和验证
- 升级后务必检查服务状态和清理旧内核
- 多内核管理：`update-grub` + `apt autoremove` 清理旧内核

**下一章**：遇到问题怎么办？从 GRUB 修复到网卡固件，从中文乱码到双系统时间。

---

即使准备工作做得很充分，使用过程中也难免遇到各种问题。最后一章汇总了 Debian 安装和日常使用中最常见的故障场景及其解决方案，从 GRUB 修复到网卡固件、从中文乱码到双系统时间不一致，覆盖了最实用的排错技巧。

---

## 第八章：常见问题与排错

本章汇总了 Debian 安装和使用中最常见的问题及解决方案，按问题类型分类。

### 8.1 GRUB 安装失败

### 现象
安装过程中出现 `Executing 'grub-install /dev/sda' failed` 错误。

### 根因
90% 的情况是**磁盘设备名漂移**。配置文件（或 preseed.cfg）中写死的 `/dev/sda` 与实际硬件设备不匹配。例如 NVMe 磁盘是 `/dev/nvme0n1`，但安装器仍尝试写入 `/dev/sda`。

### 排查

```
# 进入安装器调试终端（Ctrl+Alt+F2），执行：
lsblk -o NAME,TYPE,SIZE,MOUNTPOINT,LABEL

# 检查引导模式
[ -d /sys/firmware/efi ] && echo "UEFI" || echo "Legacy BIOS"
```

### 修复

```bash
# 进入 Rescue Mode 后
# 挂载根分区
mount /dev/nvme0n1p2 /mnt
mount /dev/nvme0n1p1 /mnt/boot/efi   # UEFI 需要
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# chroot 进入系统
chroot /mnt

# 重新安装 GRUB（BIOS）
grub-install /dev/nvme0n1

# 或（UEFI）
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=debian

# 生成配置
update-grub

# 退出并重启
exit
umount -R /mnt
reboot
```

### 8.2 GRUB 引导损坏

### 现象
开机直接进入 `grub>` 命令行，或黑屏。

### 修复（使用 Rescue Mode）

1. 插入 Debian 安装 U 盘启动
2. 选择 **Advanced options → Rescue mode**
3. 安装器扫描已安装的系统，选择要修复的系统
4. 或选择"不使用根文件系统"进入最小环境，手动挂载

手动修复步骤：

```bash
# 挂载文件系统（根据实际布局调整）
mount /dev/sda2 /mnt          # 根分区
mount /dev/sda1 /mnt/boot     # /boot 分区（如有）
mount /dev/sda1 /mnt/boot/efi # UEFI ESP 分区
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

chroot /mnt
grub-install /dev/sda
update-grub
exit
umount -R /mnt
reboot
```

### 8.3 网卡固件缺失

### 现象
安装后没有网络，`ip link show` 看不到网卡，或 `dmesg` 中有固件报错。

### 排查

```bash
# 查看固件相关错误
dmesg | grep -i firmware
dmesg | grep -iE "eth|wlan|net|link"

# 查看网卡硬件
lspci -nn | grep -iE "network|ethernet"
```

### 修复

```bash
# 先确保 non-free-firmware 源已启用
sudo apt update

# 根据网卡型号安装对应固件
sudo apt install firmware-iwlwifi    # Intel 无线网卡
sudo apt install firmware-realtek    # Realtek 有线/无线
sudo apt install firmware-atheros    # Qualcomm/Atheros
sudo apt install firmware-ralink     # Ralink

# 或自动检测缺失固件
sudo apt install isenkram
sudo isenkram-autoinstall-firmware

# 安装后重启或重载驱动
sudo modprobe -r iwlwifi && sudo modprobe iwlwifi  # Intel 示例
# 或直接重启
sudo reboot
```

> [!tip]
> 如果想在安装阶段就避免这个问题，使用包含 non-free 固件的非官方安装镜像。从 Ubuntu 转过来的用户最容易在这里卡住，因为 Ubuntu 安装镜像默认包含这些固件。

### 8.4 中文显示为方块

### 现象
中文文件名、系统界面或浏览器中的中文字显示为方块 "□□□"。

### 修复

```bash
# 安装中文字体
sudo apt install fonts-noto-cjk
sudo fc-cache -fv

# 确认 locale 正确
locale
# 若 LANG 不是 zh_CN.UTF-8，执行：
sudo dpkg-reconfigure locales  # 勾选 zh_CN.UTF-8
sudo update-locale LANG=zh_CN.UTF-8

# 重启或注销重新登录
```

### 8.5 双系统时间不一致

### 现象
Windows 和 Debian 双系统切换后，其中一个系统的时间不对（通常差 8 小时）。

### 根因
两个系统对硬件时钟（RTC）的解读不同：

- **Linux（默认）**：硬件时钟 = UTC，系统启动时转换为本地时间
- **Windows（默认）**：硬件时钟 = 本地时间

### 修复

在 Debian 中执行以下命令，让 Linux 也把硬件时钟当作本地时间：

```bash
sudo timedatectl set-local-rtc 1
```

验证：

```bash
timedatectl
# 应显示：RTC in local TZ: yes
```

> 副作用：`timedatectl` 会提示"将 RTC 设为本地时间可能导致某些问题"，但双系统场景下这是最简单的解决方案。另一个方案（不推荐）是在 Windows 中开启 UTC 支持（修改注册表）。

### 8.6 安装器找不到 U 盘

### 现象
BIOS 中能看到 U 盘，但安装器启动后提示找不到安装介质或直接进了当前系统。

### 排查

1. **更换 USB 接口**：插到 USB 2.0 接口（黑色）而非 USB 3.0（蓝色），兼容性更好
2. **换 U 盘品牌**：某些 U 盘（特别是廉价杂牌）的引导兼容性差
3. **确认写入模式**：Rufus 中选择 **DD image writing** 而非 ISO 模式
4. **关闭 Secure Boot**：进 BIOS 关闭 Secure Boot

### 8.7 APT GPG 密钥错误

### 现象
`apt update` 输出中有 `NO_PUBKEY` 错误。

### 修复

```bash
# 错误信息会给出缺失的密钥 ID
# 例如：W: GPG error: ... NO_PUBKEY A4B469963BF863CC
# 导入该密钥
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC
```

> 注：`apt-key` 在 Debian 12 已被标记为 deprecated，推荐将 `.asc` 文件放在 `/etc/apt/trusted.gpg.d/` 中。上述命令在 Bookworm 仍可使用。

### 章节总结

| 问题 | 一句话解法 |
|------|-----------|
| GRUB 安装失败 | 检查磁盘设备名，用 `/dev/disk/by-id/` 避免漂移 |
| GRUB 损坏 | 使用安装 U 盘的 Rescue Mode 重装 |
| 网卡不工作 | 装对应的 firmware 包，或直接用包含固件的安装镜像 |
| 中文方块 | 装中文字体 + 配 zh_CN.UTF-8 locale |
| 双系统时间差 8h | `timedatectl set-local-rtc 1` |
| 找不到 U 盘 | 换 USB 2.0 接口、换 DD 写入模式 |

---

## 总结

至此，你已经完整走完了 Debian 系统从选型到安装、从基础配置到安全加固、从包管理到故障排错的全部流程。以下是这份教程的核心脉络回顾：

**第一步：理解 Debian 的定位。** Debian 是社区驱动的 Linux 发行版，Ubuntu 的上游。它的 Stable（Bookworm）、Testing（Trixie）和 Unstable（Sid）三条分支分别服务于不同场景——生产环境用 Stable，桌面尝鲜用 Testing，参与开发用 Sid。

**第二步：做好安装前的准备。** 选择合适的镜像（推荐 netinst + 国内源），写入 U 盘时注意用 DD 模式，了解 UEFI/GPT 与 Legacy/MBR 的区别，并建议关闭 Secure Boot 以减少驱动兼容性风险。

**第三步：完成系统安装。** 安装语言推荐 English 以减少终端乱码，磁盘分区按使用场景选择自动、加密或手动方案，务必勾选 SSH server 和 standard system utilities。安装时留空 root 密码可使行为与 Ubuntu 的 sudo 模式一致。

**第四步：执行基础配置。** 更换国内 APT 源（清华/阿里/中科大）是安装后的第一要务，同时配置 sudo 权限、设置时区和 NTP 同步、启用 UFW 防火墙。

**第五步：根据场景选择路径。** 桌面用户需要额外配置中文 locale、中文字体和输入法（推荐 Fcitx5）；服务器管理员则需进行 SSH 密钥认证、禁用密码登录、配置 Fail2ban 和自动安全更新。

**第六步：掌握包管理。** APT 命令与 Ubuntu 完全一致，零学习成本。Backports 源可在保持稳定版的同时使用较新软件。版本升级需要备份和按步骤操作。

**第七步：具备排错能力。** 从 GRUB 修复到网卡固件、从中文乱码到双系统时间不一致，掌握这些常见问题的排查思路，才能在遇到问题时从容应对。

通过这八章的学习，你应该能够独立完成 Debian 系统的安装、配置与日常维护。Debian 以其稳定性和社区驱动的哲学赢得了广泛信赖，希望这份教程能帮助你顺利上手并长期受益于这个优秀的操作系统。
