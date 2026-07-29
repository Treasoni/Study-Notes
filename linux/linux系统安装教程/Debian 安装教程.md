---
title: Debian 安装教程
tags:
  - Linux
  - Debian
  - 安装
  - 入门
created: 2026-07-29
updated: 2026-07-29
status: published
source_project: linux-system-install
---

# Debian 安装教程

## 概述

Debian 是一个遵循 GNU 自由软件协议的通用操作系统，以稳定、安全和包管理完善著称。它是 Ubuntu、Kali Linux、Linux Mint（Debian 版）等众多发行版的基石。

### 版本选择

| 版本 | 代号 | 说明 |
|------|------|------|
| Debian 12 | Bookworm | 当前稳定版（推荐），2023 年 6 月发布 |
| Debian 11 | Bullseye | 旧稳定版，仍在安全支持期内 |
| Debian Testing | Trixie | 滚动更新，含较新软件包，稳定性低于 stable |
| Debian Unstable | Sid | 持续滚动，用于开发和测试，不推荐生产使用 |

> [!tip] 建议
> 新手或生产环境选择 Debian 12 (Bookworm) Stable。桌面用户如果追求较新软件，可考虑 Testing 分支，但要做好遇到小问题的心理准备。

### 架构支持

Debian 官方支持多种 CPU 架构：

- **amd64** (x86_64) — 最常用，Intel/AMD 64 位
- **arm64** (AArch64) — 树莓派、ARM 服务器
- **i386** — 32 位 x86（Debian 12 起不再包含在 stable 中，仅 Testing/Unstable 保留）

---

## 1. 准备工作

### 1.1 下载镜像

从官方站点下载 ISO：

```
# Debian 12 Bookworm 最新版
https://www.debian.org/download

# 国内镜像（推荐，速度更快）
# 清华镜像
https://mirrors.tuna.tsinghua.edu.cn/debian-cd/current/amd64/iso-cd/
# 阿里云镜像
https://mirrors.aliyun.com/debian-cd/current/amd64/iso-cd/
# 中科大镜像
https://mirrors.ustc.edu.cn/debian-cd/current/amd64/iso-cd/
```

三种主要镜像类型：

| 镜像类型 | 大小 | 说明 |
|----------|------|------|
| **netinst** | ~600 MB | 网络安装 CD，仅含基础系统和安装器，其余软件包在安装时从网络下载（推荐） |
| **DVD-1** | ~4 GB | 单张 DVD，包含大部分常用软件包 |
| **BD-1** | ~12 GB | 蓝光盘，包含几乎所有软件包 |
| **live** | ~3 GB | 可试用再安装，含桌面环境 |

> [!note] 日常推荐
> 普通用户下载 **netinst** 即可，安装时选择国内镜像源，速度不比 DVD 慢。

### 1.2 制作安装介质

**Linux/macOS（命令行）：**

```bash
# 确认 U 盘设备名
lsblk
# 或
diskutil list   # macOS

# 写入镜像（⚠️ 确认设备名正确，/dev/sdX 替换为实际设备）
sudo dd if=debian-12.5.0-amd64-netinst.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

**Windows：**

- [Rufus](https://rufus.ie/) — 推荐，选择「DD 镜像写入」模式
- [BalenaEtcher](https://www.balena.io/etcher/) — 简单易用

> [!warning] 注意
> dd 写入会**覆盖 U 盘所有数据**，务必确认设备名无误。写完后 Windows 可能提示"未格式化"，关闭提示即可，不要格式化。

### 1.3 硬件要求

| 环境 | 最低 | 推荐 |
|------|------|------|
| 桌面环境 | 1 GB RAM, 10 GB 磁盘 | 4 GB RAM, 40 GB 磁盘 |
| 服务器 | 256 MB RAM, 2 GB 磁盘 | 2 GB RAM, 20 GB 磁盘 |

---

## 2. 安装步骤（图形安装器）

### 2.1 启动安装

1. 插入安装介质，开机选择从 U 盘启动
   - BIOS 启动快捷键：F12 / F2 / Del / Esc（各品牌不同，屏幕通常有提示）
2. 出现 Debian 安装菜单后选择 **Graphical install**（图形化安装），如果遇到显示问题则选 **Install**（文本模式）

> [!tip] UEFI vs Legacy BIOS
> 现代电脑默认 UEFI 模式。如果启动时没有安装菜单直接进入系统，请进 BIOS 关闭 Secure Boot 或切换启动模式。Debian 12 对 UEFI + Secure Boot 支持已大幅改善，但仍建议关掉 Secure Boot。

### 2.2 语言和区域设置

| 步骤 | 推荐选项 |
|------|----------|
| 安装语言 | **English**（优先选英语，减少终端乱码问题；中文可在安装后配置） |
| 所在位置 | **other** → **Asia** → **China** |
| 区域配置 | **zh_CN.UTF-8**（locale） |
| 键盘布局 | **American English**（非中文键盘选对应布局） |

> [!note] 为什么不推荐安装时选中文
> 安装界面选中文后，控制台更容易出现乱码、字符显示不全等问题。建议安装时用英语，装完再配置中文输入法和 locale。

### 2.3 网络配置

- **DHCP（默认）**：自动获取 IP，适合家庭路由器环境
- **静态 IP**：服务器环境建议手动分配

如果使用笔记本的 Wi-Fi，安装器会提示选择无线网络并输入密码。服务器建议使用有线连接。

### 2.4 主机名和用户

```
Hostname: debian-server   # 主机名，局域网唯一即可
Domain name: (留空)       # 非局域网环境可留空
Root password: (设置强密码)
Full name: Your Name
Username: your-username
Password: (用户密码)
```

> [!warning] Root 密码
> Debian 安装时必须设置 root 密码（而 Ubuntu 默认不设置 root，用 sudo）。如果不想每次用 root，也可以留空 root 密码，安装器会自动将第一个用户加入 sudo 组。

### 2.5 磁盘分区

以下是三种常见方案：

**方案 A：全盘自动分区（推荐新手）**

选择 **Guided - use entire disk**，安装器自动处理剩余步骤：

1. 选择磁盘
2. 选择分区方案：
   - **All files in one partition** — 最简单的方案
   - **Separate /home partition** — 重装系统时保留 `/home` 数据
   - **Separate /home, /var, /tmp** — 服务器隔离场景
3. 确认并写入磁盘

**方案 B：LVM 全盘加密**

选择 **Guided - use entire disk and set up LVM encrypted**：

- 提供全盘加密（LUKS），开机需输入解密密码
- 适合笔记本或存敏感数据的服务器

**方案 C：手动分区（有经验的用户）**

| 挂载点 | 大小 | 文件系统 | 说明 |
|--------|------|----------|------|
| `/boot` | 1 GB | ext4 | UEFI 引导分区（UEFI 时需 EFI System Partition） |
| `/` | 20-50 GB | ext4 | 根分区，系统和软件安装 |
| `/home` | 剩余 | ext4 | 用户数据（可选独立分区） |
| `swap` | RAM 大小或 2 GB | swap | 交换分区（可选，有 hibernation 需要时设置） |

> [!note] EFI System Partition (ESP)
> UEFI 模式安装时，引导分区格式必须为 FAT32，挂载点为 `/boot/efi`，大小约 512 MB。安装器在 Guided 模式下会自动处理。

### 2.6 软件包选择

安装器会提示选择额外软件：

```
[*] Debian desktop environment      # 桌面环境（服务器不选）
[*] ... GNOME                       # 默认桌面，资源消耗较大
[ ] ... Xfce                        # 轻量桌面，适合旧机器
[ ] ... KDE Plasma                  # 现代桌面，较华丽
[*] web server                      # 服务器软件栈
[*] SSH server                      # 远程管理（建议必选）
[ ] print server                    # 打印服务
[*] standard system utilities       # 常用命令行工具（建议必选）
```

> [!tip] 服务器安装建议
> 只选 SSH server 和 standard system utilities，不装桌面环境以节省资源。

### 2.7 GRUB 引导

- 安装 GRUB 引导加载器到主引导记录：选择 **Yes**
- 如果有多块磁盘，选择安装到系统盘（通常是 `/dev/sda` 或 `/dev/nvme0n1`）

### 2.8 完成安装

安装完成后取出安装介质，选择 **Continue** 重启。

---

## 3. 安装后配置

### 3.1 首次登录与基本检查

```bash
# 登录后查看系统信息
cat /etc/debian_version
uname -a
lsb_release -a

# 检查网络连通性
ip addr
ping -c 4 debian.org
```

### 3.2 配置国内 APT 源

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

# 更新软件包索引
sudo apt update && sudo apt upgrade -y
```

> [!note] non-free-firmware
> Debian 12 Bookworm 起增加了 `non-free-firmware` 组件，用于包含固件类闭源驱动（如 Wi-Fi、NVIDIA 显卡）。新装系统后务必加上此源。

### 3.3 安装 sudo 并配置用户（如果没有设置）

如果安装时没有给第一个用户 sudo 权限：

```bash
# 切换 root
su -

# 安装 sudo
apt install sudo

# 将用户加入 sudo 组
usermod -aG sudo your-username

# 退出重新登录使生效
exit
```

### 3.4 配置中文支持

```bash
# 安装中文字体和输入法
sudo apt install fonts-noto-cjk fcitx5 fcitx5-chinese-addons fcitx5-mozc

# 配置 locale
sudo dpkg-reconfigure locales
# 确保选中 zh_CN.UTF-8，设为系统默认（可选）
```

### 3.5 安装常用工具

```bash
# 基础工具
sudo apt install curl wget git vim htop net-tools dnsutils tree

# 开发工具（按需）
sudo apt install build-essential gcc g++ make cmake

# 网络诊断
sudo apt install mtr traceroute nmap
```

### 3.6 配置防火墙

```bash
# 安装并启用 UFW
sudo apt install ufw

# 设置默认策略
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许 SSH（务必先做，否则会断开连接）
sudo ufw allow ssh

# 允许其他服务（按需）
sudo ufw allow http    # 80
sudo ufw allow https   # 443

# 启用防火墙
sudo ufw enable

# 查看状态
sudo ufw status verbose
```

> [!warning] 远程操作
> 如果通过 SSH 远程连接，在启用 UFW 之前必须执行 `sudo ufw allow ssh`，否则防火墙会阻断当前 SSH 连接。

### 3.7 配置 SSH 安全加固

```bash
# 编辑 SSH 配置
sudo vim /etc/ssh/sshd_config
```

推荐的安全配置：

```ini
# 禁止 root 直接登录
PermitRootLogin no

# 使用密钥认证（推荐）
PubkeyAuthentication yes
PasswordAuthentication no

# 修改默认端口（可选，减少被扫描）
Port 2222

# 限制登录用户
AllowUsers your-username
```

```bash
# 重启 SSH 服务
sudo systemctl restart ssh

# 注意：如果改了端口，新连接需指定端口
ssh -p 2222 your-username@your-server-ip
```

---

## 4. 桌面环境安装

如果安装时没有选择桌面环境，也可以后期安装：

### 4.1 安装 GNOME（默认）

```bash
sudo apt install task-gnome-desktop
```

### 4.2 安装 Xfce（轻量）

```bash
sudo apt install task-xfce-desktop
```

### 4.3 安装 KDE Plasma

```bash
sudo apt install task-kde-desktop
```

安装完成后重启：

```bash
sudo systemctl reboot
```

> [!summary] 桌面选择建议
> - GNOME：功能完整，资源占用高（2 GB+ RAM）
> - Xfce：轻量快速，适合旧硬件或虚拟机
> - KDE Plasma：界面美观，可定制性强，资源适中

---

## 5. 服务器初始化（无桌面环境）

### 5.1 主机名修改

```bash
sudo hostnamectl set-hostname debian-server
```

### 5.2 时区和时间同步

```bash
# 设置时区
sudo timedatectl set-timezone Asia/Shanghai

# 查看时间状态
timedatectl status

# 确保 NTP 同步开启
sudo timedatectl set-ntp true

# 安装 NTP 服务（可选）
sudo apt install ntp
```

### 5.3 优化内核参数（/etc/sysctl.conf）

```bash
# 开启 IP 转发（如果需要做路由器/NAT）
net.ipv4.ip_forward = 1

# 增加文件描述符限制
fs.file-max = 100000

# 网络优化
net.core.somaxconn = 65535
net.ipv4.tcp_fastopen = 3
```

```bash
# 立即生效
sudo sysctl -p
```

### 5.4 配置自动安全更新

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## 6. 软件包管理速查

### 6.1 APT 常用命令

```bash
# 更新索引
sudo apt update

# 升级所有软件
sudo apt upgrade

# 升级包括依赖变更（慎用，生产环境先手动检查）
sudo apt full-upgrade

# 安装软件
sudo apt install package-name

# 删除软件
sudo apt remove package-name
sudo apt purge package-name    # 同时删除配置文件

# 搜索软件
apt search keyword

# 查看软件信息
apt show package-name

# 查看已安装
apt list --installed

# 清理无用依赖
sudo apt autoremove
sudo apt autoclean
```

### 6.2 Backports 源使用

Backports 包含从 Testing 移植到 Stable 的较新软件，适合需要新功能但又不想切换分支的场景：

```bash
# 搜索 backports 中的软件
apt search -t bookworm-backports package-name

# 从 backports 安装
sudo apt install -t bookworm-backports package-name

# 示例：安装较新的内核
sudo apt install -t bookworm-backports linux-image-amd64
```

---

## 7. 常见问题与排错

### 7.1 安装后没有网络

```bash
# 检查网卡是否识别
ip link show
lspci | grep -i ethernet

# 如果是无线网卡，安装 firmware
sudo apt install firmware-iwlwifi   # Intel
sudo apt install firmware-realtek    # Realtek

# 重启网络服务
sudo systemctl restart networking
```

### 7.2 安装器找不到 U 盘

- 更换 USB 2.0 接口
- 换一个 U 盘（部分品牌 U 盘兼容性差）
- 确保写入模式为 DD（Rufus 中选 DD image writing）

### 7.3 GRUB 修复

如果引导损坏无法进入系统：

```bash
# 使用 Debian live CD 启动，进入救援模式
# 或使用安装光盘的 Rescue mode

# 挂载根分区到 /mnt
sudo mount /dev/sdaX /mnt

# 挂载其他必要目录
sudo mount --bind /dev /mnt/dev
sudo mount --bind /proc /mnt/proc
sudo mount --bind /sys /mnt/sys
sudo mount --bind /boot/efi /mnt/boot/efi   # UEFI

# chroot 并修复 GRUB
sudo chroot /mnt
grub-install /dev/sda
update-grub
```

### 7.4 中文显示为方块

```bash
# 安装中文字体
sudo apt install fonts-noto-cjk
sudo fc-cache -fv

# 检查 locale
locale
sudo dpkg-reconfigure locales
```

### 7.5 时间显示不正确（双系统）

```bash
# Debian 默认将硬件时钟设为 UTC，Windows 设为本地时间
# 让 Debian 也使用本地时间：
sudo timedatectl set-local-rtc 1
```

---

## 8. 升级到 Debian 新版本

以 Debian 11 → 12 为例：

```bash
# 1. 确保系统最新
sudo apt update && sudo apt upgrade -y && sudo apt full-upgrade

# 2. 备份重要数据
sudo tar czf ~/backup-etc.tgz /etc

# 3. 修改源列表：bullseye → bookworm
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sudo sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/*.list 2>/dev/null

# 4. 更新索引并执行升级
sudo apt update
sudo apt upgrade --without-new-pkgs -y
sudo apt full-upgrade -y

# 5. 清理旧依赖
sudo apt autoremove

# 6. 重启
sudo systemctl reboot

# 7. 验证
cat /etc/debian_version
```

> [!warning] 升级前注意
> - 生产环境升级前务必在测试环境验证
> - 升级过程不可逆，做好备份
> - 检查第三方源（如 Docker、PostgreSQL 等）是否支持新版本
> - 建议预留充足维护时间窗口

---

## 9. 参考资料

- [Debian 官方安装手册](https://www.debian.org/releases/stable/installmanual)
- [Debian Administrator's Handbook](https://debian-handbook.info/)
- [Debian Wiki](https://wiki.debian.org/)
- [清华 Debian 镜像源帮助](https://mirrors.tuna.tsinghua.edu.cn/help/debian/)
