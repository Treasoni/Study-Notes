---
tags: [pve, moc]
---

# PVE 学习笔记 MOC

> [!info] 概述
> Proxmox Virtual Environment (PVE) 是一个开源的虚拟化管理平台，基于 KVM 虚拟机和 LXC 容器。
> 类比：就像一个"虚拟机版的瑞士军刀"，可以同时跑 Windows、Linux、OpenWRT 等多个系统。

## 核心概念 💡
- **KVM 虚拟机**：完整虚拟化，每个 VM 有独立内核，适合 Windows、不同 Linux 发行版
- **LXC 容器**：系统级容器，共用宿主机内核，性能接近裸机，适合轻量级服务
- **网桥（vmbr）**：虚拟二层交换机，连接虚拟机和物理网络
- **设备直通**：将物理硬件（GPU、网卡、USB）直接交给虚拟机使用
- **存储库（Storage）**：统一管理虚拟机磁盘、ISO 镜像、备份文件的抽象层

## 学习路径

### 📝 准备阶段
了解基础知识，准备安装环境

| 主题 | 说明 | 笔记 |
|------|------|------|
| 写盘工具对比 | Rufus、balenaEtcher、Ventoy 各自特点 | [[00-准备工具/写盘工具]] |
| WinPE 的作用 | 磁盘清理、分区表统一、隐藏分区删除 | [[00-准备工具/WinPE]] |

### 🏗️ 安装阶段
从零开始安装 PVE 系统

| 步骤 | 说明 | 笔记 |
|------|------|------|
| 下载镜像和写盘 | 准备 PVE ISO 和写盘工具 | [[安装和使用PVE#1-下载pve系统及写盘软件]] |
| BIOS 虚拟化设置 | VT-x、VT-d、Above 4G Decoding 等配置 | [[安装和使用PVE#3-进入bios系统]] |
| 安装和初始配置 | 系统安装、网络配置 | [[安装和使用PVE#4-进入配置pve]] |

### ⚙️ 基础配置
安装后的系统优化和配置

| 操作 | 说明 | 笔记 |
|------|------|------|
| 修改网络信息 | IP 地址、网关等网络配置修改 | [[01-安装配置/修改PVE的网络信息]] |
| 存储库管理 | Storage vs Repository 的区别和使用 | [[01-安装配置/PVE存储库]] |
| 软件源设置 | 国内源配置、企业源禁用、订阅提示移除 | [[01-安装配置/PVE的基础优化设置#1-软件源设置]] |

### 💻 虚拟机管理
创建和管理虚拟机

| 主题 | 说明 | 笔记 |
|------|------|------|
| 创建虚拟机流程 | 完整的 VM 创建步骤和配置说明 | [[02-虚拟机管理/如何创建PVE虚拟机]] |
| 创建 Windows 虚拟机 | VirtIO 驱动安装、网络配置 | [[02-虚拟机管理/PVE创建window]] |
| 虚拟机网络配置 | 网桥、直通、虚拟网卡的理解 | [[02-虚拟机管理/PVE的网络逻辑讲解]] |

### 🐳 容器管理
LXC 容器的创建和使用

| 主题 | 说明 | 笔记 |
|------|------|------|
| CT 基础概念 | 容器 vs 虚拟机 vs Docker 的区别 | [[03-容器管理/PVE的CT]] |
| 创建 CT 容器 | 模板下载、容器创建步骤 | [[03-容器管理/PVE的CT#5-创建ct容器]] |

### 🔌 设备直通
物理硬件直通给虚拟机

| 步骤 | 说明 | 笔记 |
|------|------|------|
| BIOS 设置 | VT-d、Above 4G Decoding 等硬件层配置 | [[04-设备直通/PVE直通#11-step-1bios-设置硬件层]] |
| 启用 IOMMU | 系统层 IOMMU 启用和验证 | [[04-设备直通/PVE直通#12-step-2pve-启用-iommu系统层关键]] |
| IOMMU 分组理解 | 设备分组检查和问题诊断 | [[04-设备直通/IOMMU分组情况]] |
| vfio 驱动绑定 | 防止宿主机占用直通设备 | [[04-设备直通/绑定vfio驱动]] |

### 🛠️ 系统优化
性能调优和维护

| 操作 | 说明 | 笔记 |
|------|------|------|
| CPU 性能模式 | 高性能 vs 省电模式切换 | [[01-安装配置/PVE的基础优化设置#4-开启cpu节能模式]] |
| 系统更新 | apt update 和 dist-upgrade | [[01-安装配置/PVE的基础优化设置#23-更新-pve]] |

## BIOS 设置速查表 ⚠️

| 选项 | Intel 选项 | AMD 选项 | 作用 | 是否必须 |
|------|-----------|----------|------|----------|
| CPU 虚拟化 | VT-x | SVM | 虚拟机基础 | ✅ 必须 |
| 设备直通 | VT-d | IOMMU/AMD-Vi | PCIe 设备直通 | ✅ 直通必须 |
| 大地址解码 | Above 4G Decoding | Above 4G Decoding | PCIe 设备使用 4GB+ 地址 | ✅ 直通必须 |
| 网卡虚拟化 | SR-IOV | SR-IOV | 一块网卡变多块虚拟网卡 | 可选 |
| 安全启动 | Secure Boot | Secure Boot | 避免系统安装限制 | 推荐关闭 |

## 常用命令

```bash
# 网络配置
nano /etc/network/interfaces
ifreload -a

# IOMMU 配置
nano /etc/default/grub
update-grub

# vfio 驱动绑定
nano /etc/modprobe.d/vfio.conf
update-initramfs -u

# 查看 IOMMU 分组
for d in /sys/kernel/iommu_groups/*/devices/*; do
  echo "IOMMU Group ${d#*/iommu_groups/*}: $(lspci -nns ${d##*/})"
done

# 查看 PCI 设备和驱动
lspci -nnk

# CPU 频率控制
cpupower frequency-set -g performance  # 高性能
cpupower frequency-set -g powersave    # 省电

# 系统更新
apt update && apt dist-upgrade
```

## 相关资源

- PVE 官方下载：https://www.proxmox.com/en/downloads（当前最新版本：Proxmox VE 9.1-1，2025年11月发布）
- PVE VirtIO 驱动：https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers（推荐版本：virtio-win 0.1.271）
- VirtIO 驱动下载：https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/
- FirPE 下载：https://www.firpe.cn（当前版本：V2.0.3，2025年4月更新）
- 中科大 PVE 源：https://mirrors.ustc.edu.cn/help/proxmox.html
- 清华 PVE 源：https://mirrors.tuna.tsinghua.edu.cn/help/proxmox

## 相关文档

[[00-准备工具/写盘工具]] | [[00-准备工具/WinPE]] | [[01-安装配置/安装和使用PVE]] | [[01-安装配置/修改PVE的网络信息]] | [[01-安装配置/PVE存储库]] | [[01-安装配置/PVE的基础优化设置]] | [[02-虚拟机管理/如何创建PVE虚拟机]] | [[02-虚拟机管理/PVE创建window]] | [[02-虚拟机管理/PVE的网络逻辑讲解]] | [[03-容器管理/PVE的CT]] | [[04-设备直通/PVE直通]] | [[04-设备直通/IOMMU分组情况]] | [[04-设备直通/绑定vfio驱动]]
