---
tags: [pve]
---

# WinPE 详解

> [!info] 概述
> WinPE（Windows Preinstallation Environment）是微软提供的轻量级 Windows 系统，通常运行在 U 盘上，用于系统安装、维护和修复。
> 类比：就像一个"装在 U 盘里的迷你 Windows"，可以用来处理硬盘分区、系统救援等任务。

## 核心概念 💡
- **WinPE**：Windows 预安装环境，基于 Windows 的轻量级操作系统
- **分区表**：MBR（旧格式，最大 2TB）vs GPT（新格式，支持大硬盘）
- **隐藏分区**：EFI 分区、MSR 保留分区、恢复分区等系统特殊分区

## 为什么 PVE 安装需要 WinPE？

> [!warning] 重要说明
> PVE 官方安装器**技术上不需要** WinPE，但**现实中经常需要**。

### 为什么"经常需要"？

PVE 安装器是基于 Linux 的，对磁盘的"历史遗留问题"很敏感：

| 问题现象 | 原因 | 解决方案 |
|---------|------|----------|
| 安装界面看不到硬盘 | 有旧的分区表/引导信息 | 用 WinPE 清空 |
| 选择硬盘后报错 | 分区表格式混乱（GPT/MBR 混合） | 用 WinPE 统一格式 |
| ZFS/LVM 创建失败 | 有隐藏分区或残留数据 | 用 WinPE 删除 |
| 装完无法启动 | 引导信息冲突 | 用 WinPE 清理 |

## WinPE 在 PVE 安装中的作用

### 1. 清空旧分区表（最重要）

硬盘之前可能装过：
- Windows
- ESXi / 黑群晖
- Linux / OpenWrt
- 被 Ventoy / PE 折腾过

这些都会留下**奇怪的分区表和引导信息**，导致 PVE 安装器识别异常。

WinPE 格式化硬盘 = **把这些全抹掉，还硬盘一个清白**

### 2. 统一分区表格式（GPT/MBR）

| BIOS 模式 | 分区表类型 | 结果 |
|-----------|-----------|------|
| Legacy BIOS | GPT | 启动失败 |
| UEFI | MBR | PVE 安装异常 |
| 混合引导 | 混乱 | 各种玄学问题 |

在 WinPE 里可以明确设置：
- UEFI → GPT
- Legacy BIOS → MBR

### 3. 删除隐藏/保留分区

这些分区在 Windows 里有时都删不干净：
- EFI 分区（UEFI 启动必需）
- MSR（微软保留分区）
- 恢复分区（系统恢复用）
- OEM 分区（厂商自定义）

**在 WinPE 里可以一刀全清**

## 常见 WinPE 工具

| 工具 | 特点 | 下载地址 |
|------|------|----------|
| **FirPE** | 功能全面，界面友好，国内使用较多 | https://www.firpe.cn |
| 微心 PE | 轻量级，适合简单维护 | 各大软件站 |
| 微PE（WePE） | 老牌工具，稳定可靠 | https://www.wepe.com.cn |

## 操作步骤

### 使用 WinPE 准备 PVE 安装硬盘

1. **下载 WinPE 镜像**
   - 推荐 FirPE：https://www.firpe.cn
   - 下载 ISO 格式文件

2. **制作 WinPE 启动盘**
   - 使用 [[写盘工具]]（Rufus/Etcher）
   - 将 WinPE ISO 写入 U 盘

3. **从 WinPE 启动**
   - 插入 U 盘，开机选择从 U 盘启动
   - 进入 WinPE 桌面

4. **使用磁盘工具清理硬盘**
   - 打开 DiskGenius 或类似工具
   - 选择目标硬盘
   - **删除所有分区**
   - **转换分区表类型**（GPT 用于 UEFI，MBR 用于 Legacy）
   - **保存更改**

5. **重启开始 PVE 安装**
   - 从 PVE 启动盘启动
   - 现在应该可以正常识别硬盘了

## 注意事项 ⚠️

1. **WinPE 会清空硬盘所有数据**，操作前确认选对了硬盘
2. **分区表类型要与 BIOS 模式匹配**：
   - UEFI + GPT
   - Legacy BIOS + MBR
3. **PVE 安装器也可以格式化硬盘**，但遇到问题时用 WinPE 更可靠
4. **下载 ISO 格式**的 WinPE，不要下载 exe 版本

## 常见问题 ❓

**Q: 不用 WinPE 就不能装 PVE 吗？**
A: 不是必须的。如果硬盘是全新的或已经清理干净，PVE 安装器可以直接格式化。WinPE 主要用于解决"有问题的硬盘"。

**Q: WinPE 里用什么工具格式化硬盘？**
A: 推荐 DiskGenius，功能强大且直观。也可以使用 Windows 自带的磁盘管理，但功能有限。

**Q: 如何选择 GPT 还是 MBR？**
A: 新电脑/UEFI 启动用 GPT，老电脑/Legacy BIOS 用 MBR。不确定时优先选 GPT。

**Q: 格式化后硬盘显示"未分配"正常吗？**
A: 正常，这正是我们需要的。PVE 安装器会自动在未分配空间上创建分区。

## 相关文档

[[写盘工具]] | [[安装和使用PVE]] | [[PVE学习笔记MOC]]
