---
title: "Linux 软件包管理"
created: 2026-07-29
updated: 2026-07-29
tags: [linux, 包管理, apt]
status: completed
source_project: linux-commands
---

> [!note]
> 软件包管理是 Linux 日常使用中最频繁的操作之一。安装软件、更新系统、卸载不需要的程序，都离不开包管理器。不同发行版使用不同的包管理器，但核心操作逻辑是相通的。本章覆盖三大主流包管理器（apt、dnf/yum、pacman）的常用操作，并提供跨发行版对照表和常见问题的解决方案。

---

## 8.1 apt — Debian/Ubuntu 系

`apt` 是 Debian 及其衍生版（Ubuntu、Debian、Linux Mint 等）的包管理工具。它管理 `.deb` 格式的软件包，从配置好的软件源（repository）中下载安装。

### 基础命令

```bash
# 更新软件包列表（首次使用或定期执行）
sudo apt update

# 升级所有已安装的软件包
sudo apt upgrade

# 安装软件包
sudo apt install nginx

# 卸载软件包（保留配置文件）
sudo apt remove nginx

# 卸载并清除配置文件
sudo apt purge nginx

# 搜索软件包
apt search nginx

# 查看已安装的包
apt list --installed

# 查看某个包的信息
apt show nginx

# 清理不再需要的依赖
sudo apt autoremove
```

**输出示例**：
```bash
$ apt search nginx
Sorting... Done
Full Text Search... Done
nginx/stable 1.24.0-1 amd64
  small, powerful, scalable web/proxy server

nginx-extras/stable 1.24.0-1 amd64
  nginx web/proxy server with extra modules
```

### 常用组合

```bash
# 标准更新流程（先更新列表，再升级）
sudo apt update && sudo apt upgrade -y

# 安装时自动确认
sudo apt install -y htop

# 查看可升级的包
apt list --upgradable

# 清理本地下载的缓存（.deb 包）
sudo apt clean

# 只清理过时的缓存
sudo apt autoclean
```

> [!tip]
> 养成习惯：**安装前先 `sudo apt update`**。如果跳过这一步，apt 会使用过时的包列表，可能导致找不到最新版本或安装失败。

> [!warning]
> **不要混用 `apt-get` 和 `apt`？** 两者底层相同，`apt` 是 `apt-get` 的精简优化版，日常使用推荐 `apt`。但写脚本时建议用 `apt-get`，它的输出格式更稳定，适合程序解析。

---

## 8.2 dnf/yum — Red Hat 系

RHEL/CentOS/Fedora 系发行版使用 RPM 包格式。早期用 `yum`，从 RHEL 8 / CentOS 8 起 `dnf` 取代了 `yum` 成为默认包管理器。

### dnf 基础命令

```bash
# 安装软件包
sudo dnf install nginx

# 卸载软件包
sudo dnf remove nginx

# 更新所有包
sudo dnf update

# 搜索包
dnf search nginx

# 查看包信息
dnf info nginx

# 列出已安装
dnf list installed

# 清理缓存
sudo dnf clean all
```

### dnf 特色功能：事务回滚

`dnf` 的一个亮点是支持事务历史记录，可以撤销之前的操作：

```bash
# 查看历史操作
dnf history

# 撤销某次操作（按序号）
sudo dnf history undo 3

# 回滚到某个历史点
sudo dnf history rollback 2
```

### yum（历史兼容）

在 CentOS 7 及更早版本中使用 `yum`，其命令格式与 `dnf` 基本一致：

```bash
yum install nginx
yum remove nginx
yum update
yum search nginx
```

> [!note]
> `yum` 在 RHEL 8+ / CentOS 8+ 中已标记为淘汰。虽然很多系统上 `yum` 命令仍然存在（作为 `dnf` 的符号链接），但建议直接使用 `dnf`。

---

## 8.3 pacman — Arch 系

Arch Linux 及其衍生版（Manjaro、EndeavourOS 等）使用 `pacman`，它管理 `.pkg.tar.zst` 格式的包。

```bash
# 同步包数据库并更新系统
sudo pacman -Syu

# 安装包
sudo pacman -S nginx

# 卸载包（保留配置及依赖）
sudo pacman -R nginx

# 卸载包及其依赖
sudo pacman -Rs nginx

# 卸载包、依赖及配置文件
sudo pacman -Rns nginx

# 搜索包
pacman -Ss nginx

# 查看包信息
pacman -Qi nginx

# 列出所有显式安装的包
pacman -Qe

# 清理未使用的依赖（orphans）
sudo pacman -Rns $(pacman -Qtdq)
```

> [!tip]
> `pacman` 的操作选项很有规律：`-S` 表示同步（sync，安装/搜索），`-R` 表示移除（remove），`-Q` 表示查询（query）。结合后缀字母，`-Ss` 搜索、`-Si` 查看信息、`-Su` 更新。记住这个规律后基本不用查文档。

> [!warning]
> Arch 是滚动更新（rolling release）发行版，建议**定期执行 `pacman -Syu`**（至少每周一次）。长时间不更新会导致系统状态过老，下次更新时可能遇到大量冲突，解决起来更麻烦。

---

## 8.4 跨发行版命令对照

以下表格整理了三大包管理器在相同操作下的对应命令，方便你在不同发行版之间切换时快速参考：

| 操作 | apt (Debian/Ubuntu) | dnf (RHEL 8+/Fedora) | pacman (Arch) |
|------|---------------------|---------------------|--------------|
| 更新包列表 | `apt update` | `dnf check-update` | `pacman -Sy` |
| 安装包 | `apt install pkg` | `dnf install pkg` | `pacman -S pkg` |
| 卸载包 | `apt remove pkg` | `dnf remove pkg` | `pacman -R pkg` |
| 清除配置卸载 | `apt purge pkg` | — | `pacman -Rns pkg` |
| 更新所有包 | `apt upgrade` | `dnf update` | `pacman -Su` |
| 搜索包 | `apt search kw` | `dnf search kw` | `pacman -Ss kw` |
| 查看包信息 | `apt show pkg` | `dnf info pkg` | `pacman -Qi pkg` |
| 列出已安装 | `apt list --installed` | `dnf list installed` | `pacman -Q` |
| 清理缓存 | `apt clean` | `dnf clean all` | `pacman -Sc` |
| 清理孤立依赖 | `apt autoremove` | `dnf autoremove` | `pacman -Rns $(pacman -Qtdq)` |
| 回滚事务 | — | `dnf history undo N` | — |

> [!note]
> `apt` 没有原生的事务回滚功能，但可以通过查看 `/var/log/apt/history.log` 来追溯安装记录。在关键操作前使用快照（如 `timeshift`）是更稳妥的备份方式。

### 快速识别你用的是哪个包管理器

```bash
# 查看系统发行版
cat /etc/os-release

# 或使用 hostnamectl
hostnamectl

# 如果分不清，试试哪个命令存在
which apt dnf yum pacman zypper 2>/dev/null
```

---

## 8.5 常见问题与解决

### 换源（更换国内镜像源）

默认软件源在海外，下载速度可能很慢。更换为国内镜像源是最常见的优化操作。

**apt 换源（Ubuntu 示例）**：

```bash
# 备份原始源文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 编辑源列表
sudo vim /etc/apt/sources.list

# 将 archive.ubuntu.com 替换为国内镜像
# 例如：中科大镜像 mirrors.ustc.edu.cn
# 或：阿里云 mirrors.aliyun.com
# 或：清华 mirrors.tuna.tsinghua.edu.cn

# 替换后更新
sudo apt update && sudo apt upgrade
```

**dnf 换源（Fedora 示例）**：

```bash
# 启用最快的镜像（自动选择）
sudo dnf install dnf-plugin-fastestmirror

# 或手动指定源配置文件
# /etc/yum.repos.d/ 下的 .repo 文件可逐个编辑
```

> [!tip]
> 换源后务必执行 `apt update` 或 `dnf check-update` 刷新包列表，否则新源不会生效。

### 依赖修复

**apt**：

```bash
# 修复破损的依赖
sudo apt --fix-broken install

# 重新配置所有未完成的包
sudo dpkg --configure -a

# 如果某个包下载中断，重新安装
sudo apt install --reinstall package-name
```

**dnf**：

```bash
# 检查并修复依赖问题
sudo dnf check
sudo dnf reinstall package-name

# 如果问题复杂，尝试 distro-sync（同步到发行版版本）
sudo dnf distro-sync
```

**pacman**：

```bash
# 重新安装某个包
sudo pacman -S package-name

# 检查损坏的包
pacman -Qk

# 强制刷新并更新
sudo pacman -Syyu
```

### 锁定版本（防止误升级）

有时需要固定某个包的版本，不让它随系统更新：

```bash
# apt：标记为 hold
sudo apt-mark hold nginx
sudo apt-mark showhold          # 查看所有锁定的包
sudo apt-mark unhold nginx      # 解锁

# dnf：在配置中添加 exclude
sudo dnf update --exclude=nginx
# 或写入 /etc/dnf/dnf.conf: exclude=nginx kernel*

# pacman：编辑 /etc/pacman.conf，在 IgnorePkg 中加入包名
IgnorePkg = nginx
```

### 常见问题速查

| 现象 | 大概率原因 | 解决 |
|------|-----------|------|
| `Unable to locate package` | 包列表过期（或包名手误） | 先 `apt update` 再试 |
| `Could not get lock /var/lib/dpkg/lock` | 有其他 apt 进程在运行 | 等它结束，或 `sudo kill` 进程后 `sudo rm /var/lib/dpkg/lock`（慎用） |
| `dpkg: error processing package xxx` | 包安装中断或损坏 | `sudo dpkg --configure -a` |
| `The following packages have been kept back` | 依赖冲突或配置变更 | `apt upgrade --with-new-pkgs` 或 `apt dist-upgrade` |
| `404 Not Found [IP: ...]` | 源地址失效 | 换源或更新源配置 |
| `GPG error: ... NO_PUBKEY` | 缺少 GPG 公钥 | `sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys <KEY_ID>` |

> [!warning]
> `apt` 操作时如果遇到 `Could not get lock` 错误，**优先确认是否有其他进程在运行**（如后台自动更新），不要直接删锁文件。只有确认没有其他 apt 进程时，才删除锁文件。

---

## 本章总结

- **apt** 是 Debian/Ubuntu 系的包管理器，操作直觉且成熟稳定，日常记住 `update` / `install` / `remove` / `autoremove` 四个核心命令即可。
- **dnf** 是 Red Hat 系的新一代包管理器，替代了旧版 `yum`，支持事务回滚是它的一大优势。
- **pacman** 是 Arch 系的包管理器，命令选项规律性极强（`-S` 同步、`-R` 移除、`-Q` 查询），学会规律后效率很高。
- **跨发行版对照表** 可以在不同系统间快速切换，核心操作逻辑是相通的。
- **换源和依赖修复** 是最常见的包管理问题，掌握对应的修复命令能节省大量时间。
- 锁定版本功能在**生产环境**中非常实用，可以防止关键服务被意外升级。

### 下一步

包管理是系统运维的基础，下一章我们将跳出单个命令的视角，学习 **Shell 实用技巧与命令组合**，看看如何通过管道、重定向和别名等技巧，把学过的命令串起来解决更复杂的实际问题。
