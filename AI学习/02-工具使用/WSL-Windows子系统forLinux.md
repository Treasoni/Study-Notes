---
tags: [wsl, windows, linux, 开发环境, 虚拟化]
created: 2026-03-29
updated: 2026-03-29
---

# WSL (Windows Subsystem for Linux)

> [!info] 概述
> **WSL 是 Windows 内置的 Linux 子系统，让你在 Windows 上直接运行 Linux 环境**，无需虚拟机或双系统。
>
> **🎯 比喻**：就像在你的 Windows 房子里建了一个「Linux 小隔间」，你可以随时进出，两边工具都能用。

---

## 一、核心概念

### 1.1 什么是 WSL？

**WSL (Windows Subsystem for Linux)** 是 Windows 10/11 内置的功能，允许开发者直接在 Windows 上运行 Linux 环境，包括：

- 运行多种 Linux 发行版（Ubuntu、Debian、Kali 等）
- 使用 Bash 命令行工具（grep、sed、awk 等）
- 运行 Linux 应用程序和服务（Node.js、Python、MySQL、Docker 等）
- 在 Linux 中调用 Windows 程序，反之亦然

```
┌─────────────────────────────────���───────────────────────────┐
│                    Windows 操作系统                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│   │  Windows    │    │    WSL      │    │  Windows    │    │
│   │  应用程序   │    │  (Linux)    │    │  应用程序   │    │
│   └─────────────┘    └─────────────┘    └─────────────┘    │
│                              │                              │
│                              ▼                              │
│                    ┌─────────────────┐                     │
│                    │  Linux Kernel   │                     │
│                    │   (WSL 2)       │                     │
│                    └─────────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 📚 来源
> - [What is WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/about) - 微软官方文档

### 1.2 为什么需要 WSL？

| 痛点 | WSL 的解决方案 |
|------|---------------|
| 想用 Linux 但不想装双系统 | 直接在 Windows 里运行 Linux |
| 虚拟机太重、太慢 | WSL 轻量级，秒启动 |
| 需要同时用 Windows 和 Linux 工具 | 两边无缝切换 |
| 开发环境配置麻烦 | 一条命令安装完整 Linux 环境 |

**🎯 比喻**：
- **传统虚拟机** = 在房子旁边另建一栋房子（重、慢、资源占用大）
- **双系统** = 两栋房子，只能住一栋（切换麻烦）
- **WSL** = 同一栋房子里的两个房间，随时来回走动

### 1.3 WSL 1 vs WSL 2

| 特性 | WSL 1 | WSL 2 |
|------|-------|-------|
| **架构** | 翻译层 | 真实 Linux 内核 + 轻量虚拟机 |
| **系统调用** | 部分兼容 | **100% 兼容** |
| **文件性能** | 跨系统访问更快 | Linux 内部更快（2-20倍） |
| **Docker 支持** | ❌ 不支持 | ✅ **完美支持** |
| **systemd 支持** | ❌ | ✅ |
| **启动速度** | 快 | 快 |
| **内存占用** | 更小 | 稍大（动态分配） |

> [!tip] 推荐
> **默认使用 WSL 2**，除非你的项目文件必须存储在 Windows 文件系统中（WSL 1 跨系统访问更快）。

> [!info] 📚 来源
> - [Comparing WSL 1 and WSL 2 | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) - 微软官方文档

---

## 二、如何使用 WSL

### 2.1 安装 WSL（一条命令）

**前提条件**：Windows 10 (Build 19041+) 或 Windows 11

```powershell
# 以管理员身份运行 PowerShell
wsl --install
```

这条命令会：
1. 启用 WSL 功能
2. 启用虚拟机平台
3. 下载并安装 Ubuntu（默认发行版）
4. 安装 WSL 2 Linux 内核

**安装完成后重启电脑**，然后设置 Linux 用户名和密码。

> [!info] 📚 来源
> - [Install WSL | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/install) - 微软官方文档

### 2.2 安装其他 Linux 发行版

```powershell
# 查看可用的发行版
wsl --list --online

# 安装指定发行版
wsl --install -d Debian
wsl --install -d Ubuntu-22.04

# 常见发行版
# Ubuntu, Debian, Kali Linux, OpenSUSE, Oracle Linux
```

### 2.3 常用命令速查表

| 操作 | 命令 |
|------|------|
| **查看已安装的发行版** | `wsl --list --verbose` 或 `wsl -l -v` |
| **进入默认 Linux** | `wsl` |
| **进入指定发行版** | `wsl -d Ubuntu` |
| **在 Linux 中执行命令** | `wsl ls -la` |
| **关闭 WSL** | `wsl --shutdown` |
| **更新 WSL** | `wsl --update` |
| **设置默认版本** | `wsl --set-default-version 2` |
| **设置默认发行版** | `wsl --set-default Ubuntu` |
| **切换 WSL 版本** | `wsl --set-version Ubuntu 2` |
| **注销发行版** | `wsl --unregister Ubuntu` |

### 2.4 启动 Linux 的几种方式

```
┌─────────────────────────────────────────────────────────────┐
│                   启动 WSL 的方式                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  方式 1: Windows Terminal（推荐）                            │
│  ├── 支持多标签页                                           │
│  ├── 可自定义主题                                           │
│  └── 快速切换 PowerShell / Linux                            │
│                                                             │
│  方式 2: 开始菜单                                           │
│  └── 搜索 "Ubuntu" 直接打开                                 │
│                                                             │
│  方式 3: PowerShell 命令                                    │
│  ├── wsl          # 进入默认 Linux                          │
│  ├── ubuntu       # 直接启动 Ubuntu                         │
│  └── wsl ls -la   # 执行命令后返回                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 文件系统访问

**从 Windows 访问 Linux 文件**：
```
# 在文件资源管理器地址栏输入
\\wsl$\Ubuntu\home\username

# 或在 PowerShell 中
cd \\wsl$\Ubuntu\home\username
```

**从 Linux 访问 Windows 文件**：
```bash
# Windows C 盘挂载在 /mnt/c
cd /mnt/c/Users/YourName
ls
```

> [!warning] 性能提示
> - **Linux 程序操作 Linux 文件** → 最快
> - **Windows 程序操作 Windows 文件** → 最快
> - **跨系统访问** → 有性能损耗
>
> **建议**：将项目文件放在 Linux 文件系统（`~/projects`）以获得最佳性能。

---

## 三、实战场景

### 3.1 搭建开发环境

```bash
# 进入 WSL
wsl

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装常用工具
sudo apt install git curl wget vim build-essential -y

# 安装 Node.js (使用 nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts

# 安装 Python
sudo apt install python3 python3-pip -y
```

### 3.2 配合 VS Code 使用（推荐）

1. 安装 VS Code 扩展：**WSL** (ms-vscode-remote.remote-wsl)
2. 在 WSL 项目目录中运行：
   ```bash
   code .
   ```
3. VS Code 会自动连接到 WSL，实现：
   - 在 Windows 上编辑
   - 在 Linux 上运行和调试

### 3.3 运行 Docker 容器

WSL 2 完美支持 Docker：

```bash
# 确保 Docker Desktop 已安装并启用 WSL 2 后端
docker run hello-world

# 运行 Nginx
docker run -d -p 8080:80 nginx

# 访问 http://localhost:8080
```

> [!tip] 相关文档
> 详细的 Docker 安装配置见 [[docker/Windows-DockerDesktop安装指南-国内网络版]]

---

## 四、常见问题

### 4.1 安装失败怎么办？

**问题**：`wsl --install` 卡住或失败

```powershell
# 方案 1：手动启用功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启电脑后
wsl --update

# 方案 2：离线安装
# 从 GitHub 下载 MSI 包
# https://github.com/microsoft/wsl/releases
```

### 4.2 WSL 2 内核未安装

**错误信息**：`WSL 2 requires an update to its kernel component`

```powershell
# 更新内核
wsl --update

# 或手动下载安装
# https://aka.ms/wsl2kernel
```

### 4.3 内存占用过高

**问题**：WSL 2 占用大量内存

**解决方案**：创建 `.wslconfig` 配置文件

```powershell
# 在 Windows 用户目录创建 %USERPROFILE%\.wslconfig
notepad $env:USERPROFILE\.wslconfig
```

写入以下内容：
```ini
[wsl2]
memory=4GB
processors=2
swap=2GB
```

然后重启 WSL：
```powershell
wsl --shutdown
```

### 4.4 网络问题（国内环境）

**问题**：Ubuntu apt 更新很慢

**解决方案**：更换国内镜像源

```bash
# 备份原文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 替换为阿里云镜像（Ubuntu 22.04）
sudo sed -i 's@archive.ubuntu.com@mirrors.aliyun.com@g' /etc/apt/sources.list

# 更新
sudo apt update
```

---

## 五、与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[docker/Windows-DockerDesktop安装指南-国内网络版]] | Docker Desktop 依赖 WSL 2 运行 Linux 容器 |
| 虚拟机 (VM) | WSL 2 使用轻量级虚拟机，但比传统 VM 更轻量 |
| Hyper-V | WSL 2 底层使用 Hyper-V 技术 |
| Windows Terminal | 推荐的 WSL 终端工具 |

```
┌─────────────────────────────────────────────────────────────┐
│                    技术栈关系图                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │              Windows Terminal (终端)                 │  │
│   └─────────────────────────────────────────────────────┘  │
│                            │                               │
│              ┌─────────────┼─────────────┐                │
│              ▼             ▼             ▼                │
│        ┌─────────┐   ┌─────────┐   ┌─────────┐           │
│        │  CMD    │   │  WSL    │   │PowerShell│           │
│        └─────────┘   └────┬────┘   └─────────┘           │
│                          │                                │
│                          ▼                                │
│                   ┌─────────────┐                        │
│                   │   WSL 2     │                        │
│                   │ (Linux VM)  │                        │
│                   └──────┬──────┘                        │
│                          │                                │
│                          ▼                                │
│                   ┌─────────────┐                        │
│                   │   Docker    │                        │
│                   │  Containers │                        │
│                   └─────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> （此处记录个人学习心得，更新时会被保留）

---

## 参考资料

### 官方资源
- [WSL 官方文档 | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/) - 微软官方文档
- [WSL 安装指南 | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/install) - 安装步骤
- [WSL 1 vs WSL 2 对比 | Microsoft Learn](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) - 版本对比
- [WSL GitHub 仓库](https://github.com/microsoft/WSL) - 源码和 Issue
- [WSL 开源文档](https://wsl.dev/) - wsl.dev

### Linux 发行版文档
- [Ubuntu on WSL](https://documentation.ubuntu.com/wsl/stable/) - Ubuntu 官方 WSL 文档
- [Debian on WSL](https://wiki.debian.org/InstallingDebianOn/Microsoft/Windows/SubsystemForLinux) - Debian 安装指南

### 社区资源
- [Windows Command Line Blog](https://devblogs.microsoft.com/commandline/) - 微软官方博客

---

**最后更新**：2026-03-29
