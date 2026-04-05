---
title: Linux 学习笔记 MOC
created: 2026-04-06
updated: 2026-04-06
tags: [linux, moc, 索引]
---

# Linux 学习笔记 MOC

> [!info] 概述
> 本 MOC 整理了 Linux 系统学习的核心笔记，��盖系统安装、磁盘管理、网络配置、系统基础等内容。

---

## 📚 快速导航

### 入门必读

| 笔记 | 说明 |
|------|------|
| [[Ubuntu Server 安装教程]] | Ubuntu Server 完整安装指南，包含分区、LVM 配置 |
| [[Ubuntu Server SSH 配置指南]] | SSH ���程连接配置，密钥认证最佳实践 |
| [[Linux换源]] | 国内镜像源配置，加速软件下载 |
| [[WSL-Windows子系统forLinux]] | Windows 内置 Linux 子系统使用指南 |

### 磁盘与存储

| 笔记 | 说明 |
|------|------|
| [[linux磁盘相关的知识]] | 磁盘分区、格式化、挂载基础 |
| [[linux的LVM管理]] | LVM 逻辑卷管理，动态扩容 |

### 系统基础

| 笔记 | 说明 |
|------|------|
| [[cpu的线程和内核]] | CPU 核心与线程概念，性能监控 |
| [[linux的文件权限]] | chmod、chown 权限管理 |

### 网络配置

| 笔记 | 说明 |
|------|------|
| [[linux如何修改网络信息]] | Netplan 静态 IP、DHCP 配置 |
| [[Ubuntu curl SSL连接问题排查]] | 旁路由环境 SSL 连接故障排查 |

---

## 🗂️ 主题分类

### 一、系统安装与配置

```mermaid
flowchart LR
    A[Ubuntu Server 安装] --> B[SSH 配置]
    A --> C[换源]
    A --> D[网络配置]
    B --> E[远程管理]
    C --> F[加速下载]
    D --> G[静态IP/DHCP]
```

#### 1.1 Ubuntu Server 安装教程
- **适用场景**：服务器部署、虚拟机安装
- **关键点**：LVM 分区、OpenSSH 安装
- **相关**：[[linux的LVM管理]] | [[linux磁盘相关的知识]]

#### 1.2 Ubuntu Server SSH 配置指南
- **适用场景**：远程服务器管理
- **关键点**：密钥认证、禁用 root 登录
- **相关**：[[Ubuntu Server 安装教程]]

#### 1.3 Linux换源
- **适用场景**：国内网络环境
- **关键点**：清华/阿里云镜像、DEB822 格式
- **相关**：[[linux如何修改网络信息]]

#### 1.4 WSL (Windows Subsystem for Linux)
- **适用场景**：Windows 开发环境
- **关键点**：WSL 2、VS Code 集成、Docker 支持
- **相关**：无

---

### 二、磁盘与存储管理

```mermaid
flowchart TD
    A[磁盘管理] --> B[分区]
    A --> C[格式化]
    A --> D[挂载]
    E[LVM] --> F[物理卷 PV]
    E --> G[卷组 VG]
    E --> H[逻辑卷 LV]
    F --> G --> H
```

#### 2.1 Linux 磁盘相关知识
- **核心概念**：分区表（MBR/GPT）、文件系统（ext4/xfs）、挂载
- **常用命令**：`lsblk`、`fdisk`、`mkfs`、`mount`
- **相关**：[[linux的LVM管理]] | [[linux的文件权限]]

#### 2.2 Linux LVM 管理
- **核心概念**：PV → VG → LV 三层架构
- **常用场景**：动态扩容、快照备份
- **相关**：[[linux磁盘相关的知识]] | [[cpu的线程和内核]]

---

### 三、系统基础

#### 3.1 CPU 核心与线程
- **核心概念**：物理核心 vs 逻辑线程、超线程技术
- **常用命令**：`lscpu`、`top`、`htop`
- **相关**：[[linux磁盘相关的知识]] | [[linux的LVM管理]]

#### 3.2 Linux 文件权限
- **核心概念**：rwx 权限、chmod/chown、用户组管理
- **常用命令**：`chmod`、`chown`、`usermod`
- **相关**：[[linux磁盘相关的知识]] | [[linux的LVM管理]]

---

### 四、网络配置与故障排查

```mermaid
flowchart LR
    A[网络配置] --> B[Netplan]
    A --> C[NetworkManager]
    B --> D[静态IP]
    B --> E[DHCP]
    F[故障排查] --> G[SSL 问题]
    G --> H[旁路由环境]
```

#### 4.1 Linux 网络配置
- **核心概念**：Netplan YAML 配置、静态 IP/DHCP
- **常用命令**：`ip a`、`netplan apply`、`nmcli`
- **相关**：[[Linux换源]] | [[Ubuntu curl SSL连接问题排查]]

#### 4.2 Ubuntu curl SSL 连接问题排查
- **核心问题**：旁路由 ICMP 重定向导致 SSL 握手失败
- **解决方案**：MASQUERADE、禁用 ICMP 重定向
- **相关**：[[linux如何修改网络信息]]

---

## 🔗 知识关联图

```mermaid
graph TB
    subgraph 入门
        A[Ubuntu Server 安装教程]
        B[SSH 配置指南]
        C[Linux换源]
    end

    subgraph 磁盘
        D[磁盘管理]
        E[LVM 管理]
    end

    subgraph 网络
        F[网络配置]
        G[SSL 故障排查]
    end

    subgraph 基础
        H[文件权限]
        I[CPU 核心]
    end

    A --> D
    A --> F
    A --> B
    A --> C
    D --> E
    F --> G
    E --> H
```

---

## 📝 学习路径建议

### 路径一：服务器管理员
1. [[Ubuntu Server 安装教程]] → [[Ubuntu Server SSH 配置指南]] → [[Linux换源]]
2. [[linux磁盘相关的知识]] → [[linux的LVM管理]]
3. [[linux如何修改网络信息]] → [[linux的文件权限]]

### 路径二：开发环境搭建
1. [[WSL-Windows子系统forLinux]] → [[Linux换源]]
2. [[linux的文件权限]] → [[cpu的线程和内核]]

### 路径三：故障排查
1. [[Ubuntu curl SSL连接问题排查]] → [[linux如何修改网络信息]]

---

## 📌 最近更新

| 文件 | 更新日期 |
|------|----------|
| [[Ubuntu curl SSL连接问题排查]] | 2026-03-29 |
| [[WSL-Windows子系统forLinux]] | 2026-03-29 |
| [[linux如何修改网络信息]] | 2026-03-07 |

---

## 相关文档

- [[../00-索引/MOC|主索引]]
