---
title: VMware 启动出现 "No Media" 报错
tags:
  - VMware
  - 虚拟机
  - 故障排查
  - Windows
created: 2026-07-31
updated: 2026-07-31
status: seedling
---

# VMware 启动出现 "No Media" 报错

> [!danger] 报错现象
> 启动 VMware 虚拟机时出现以下信息，无法进入系统：
> ```
> Attempting to start up from:
>  → EFI VMware Virtual NVMe Namespace (NSID 1)... No Media.
>  → EFI VMware Virtual SATA CDROM Drive (1.0)... No Media.
> ```
> 虚拟机**没有检测到任何可引导的操作系统或系统安装镜像（ISO 文件）**。

![](assets/VMware%20启动出现%20No%20Media%20报错/file-20260731001315730.png)

---

## 1. 原因分析

"No Media" 表示虚拟机在启动时遍历了所有可引导设备（NVMe 硬盘、SATA 光驱），但**全部没有检测到可引导介质**。常见的三种原因：

| 原因 | 说明 |
|------|------|
| ❌ 光驱未挂载 ISO | 刚创建虚拟机准备装系统，但 CD/DVD 没有连接安装镜像 |
| ❌ 虚拟硬盘丢失连接 | 之前能开机的虚拟机，虚拟硬盘（.vmdk）从设备列表中丢失或被移除 |
| ❌ 引导模式设置错误 | 固件类型（EFI vs BIOS）与操作系统不匹配，导致找不到引导程序 |

---

## 2. 解决方案

### 2.1 挂载 ISO 安装镜像（新建虚拟机最常见）

> [!tip] 适用场景
> 刚创建完虚拟机，正准备安装操作系统时遇到此问题。

1. **关闭虚拟机**（电源菜单 → 关闭客户机或关闭电源）
2. 右键虚拟机 → **设置（Settings）**
3. 在硬件列表中找到 **CD/DVD (SATA)**
4. 右侧勾选 **使用 ISO 镜像文件（Use ISO image file）**
5. 点击 **浏览** 选中你的操作系统安装 ISO（如 Windows 10/11、Linux 等）
6. **关键：** 确保勾选 **启动时连接（Connect at power on）**
7. 点击 **确定** 保存，重新启动虚拟机

> [!warning] 注意
> - ISO 文件路径不要包含中文或特殊字符，以免 VMware 无法识别
> - 确保 ISO 文件本身**没有损坏**，可通过校验 MD5/SHA1 确认

### 2.2 检查虚拟硬盘连接（已有系统突然报错）

> [!tip] 适用场景
> 之前能正常使用的虚拟机，某次开机突然出现 "No Media"。

1. 关闭虚拟机
2. 右键虚拟机 → **设置（Settings）**
3. 检查硬件列表中是否有 **硬盘（NVMe 或 SATA）** 设备
4. 如果没有 → 点击 **添加（Add...）** → **硬盘** → 选择 **使用现有虚拟磁盘（Use an existing virtual disk）**
5. 浏览找到对应的 `.vmdk` 文件
6. 如果有但显示异常 → 检查 **磁盘文件路径是否有效**，或者磁盘文件已被误删/移动
7. 确认勾选 **启动时连接**（Connect at power on）

> [!warning] 虚拟硬盘丢失的常见原因
> - 手动移动或重命名了 `.vmdk` 文件
> - 从快照恢复后磁盘连接异常
> - 虚拟机目录被复制/迁移后路径未更新

### 2.3 切换引导模式（EFI ↔ BIOS）

> [!tip] 适用场景
> 修改过虚拟机固件类型，或者安装了旧版系统后无法引导。

1. 关闭虚拟机
2. 右键虚拟机 → **设置（Settings）**
3. 进入 **选项（Options）** 选项卡
4. 找到 **高级（Advanced）** → **固件类型（Firmware type）**
5. 尝试切换：
   - **Windows 10/11、现代 Linux** → 使用 **EFI**
   - **Windows 7 及更早、旧版 Linux** → 使用 **BIOS**
6. 点击确定保存后重新开机

> [!info] 如何判断该用哪种？
> - 如果你安装的是 **Windows 7 或更早版本**，尝试切换到 BIOS
> - 如果你安装的是 **Windows 10/11 或现代 Linux（如 Ubuntu 20.04+）**，使用 EFI
> - 不确定时可以**交替尝试两种模式**

---

## 3. 预防建议

- ✅ 创建虚拟机时**确认 ISO 已挂载**再开机
- ✅ 使用 **EFI** 模式安装 Windows 11（TPM + 安全启动要求）
- ✅ 虚拟机文件迁移后，检查所有设备路径是否正确
- ✅ 重要虚拟机**定期备份 `.vmdk` 文件**，避免误删导致启动失败

---

## 相关笔记

- [[虚拟机/VMware Workstation Player 安装 Windows 虚拟机.md]] - 从零开始创建 VMware 虚拟机的完整教程
- [[虚拟机/VMware 获取虚拟机所有权失败.md]] - VMware 锁文件（.lck）报错的解决方法
