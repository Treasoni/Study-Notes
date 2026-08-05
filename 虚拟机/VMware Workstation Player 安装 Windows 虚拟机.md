---
title: VMware Workstation Player 安装 Windows 虚拟机
tags:
  - VMware
  - Windows
  - 虚拟机
  - 教程
created: 2026-07-30
updated: 2026-07-30
status: seedling
---

# VMware Workstation Player 安装 Windows 10/11 虚拟机

> [!info] 概述
> VMware Workstation Player 是 VMware 提供的**免费**桌面虚拟化软件，可以在个人电脑上运行隔离的 Windows 虚拟机。本文以 Windows 10/11 为例，从零开始完整演示创建、安装和优化流程。

---

## 1. 准备工作

### 1.1 下载 VMware Workstation Player

| 项目 | 说明 |
|------|------|
| 官方网站 | https://www.vmware.com/products/workstation-player.html |
| 当前版本 | VMware Workstation 17 Player（截至 2026 年） |
| 费用 | **免费**（个人使用） |
| 系统要求 | 64 位 x86 CPU、4GB+ 内存（推荐 8GB+）、20GB+ 磁盘空间 |

> [!tip] 下载提示
> 访问官网后点击 **Download for Free**，选择 Windows 版本下载。Broadcom 收购 VMware 后，个人版依然免费，但需要注册账户获取许可密钥（输入邮箱即可获得免费密钥）。

### 1.2 下载 Windows ISO

| 系统 | 官方下载 |
|------|----------|
| Windows 11 | https://www.microsoft.com/software-download/windows11 |
| Windows 10 | https://www.microsoft.com/software-download/windows10 |

> [!tip] 选择建议
> - **Windows 11**：推荐新机器使用，需要支持 TPM 2.0（VMware 可虚拟化）
> - **Windows 10**：硬件兼容性更好，低配机器首选
> - 都选择 **64 位**版本

### 1.3 硬件要求参考

| 用途 | CPU | 内存 | 磁盘 | 说明 |
|------|-----|------|------|------|
| 轻量体验 | 2 核 | 4GB | 40GB | 仅桌面操作 |
| 日常使用 | 4 核 | 8GB | 60GB | 办公 + 轻度开发 |
| 开发/测试 | 4-8 核 | 16GB | 80GB+ | 编译、多服务运行 |

---

## 2. 安装 VMware Workstation Player

### 2.1 安装步骤

1. 双击下载的 `VMware-player-full-*.exe` 安装包
2. 勾选 **"I accept the terms in the license agreement"**
3. 选择安装路径（默认即可）
4. 勾选 **"Check for product updates on startup"**（可选，建议取消）
5. 勾选 **"Help improve VMware Workstation Player"**（可选，建议取消）
6. 点击 **Install**
7. 安装完成后点击 **Finish**

### 2.2 激活免费许可

1. 打开 VMware Workstation Player
2. 点击 **"Workstation 17 Player for non-commercial use"** → 点击 **Finish**
3. 首次启动会提示输入许可密钥
4. 点击 **"Get a free license key from the VMware website"** 跳转到官网
5. 注册账户并获取免费密钥
6. 在软件中输入密钥完成激活

> [!warning] 关于许可
> 个人非商业用途完全免费。如果你在公司用，需要购买商业许可。不要使用网上找的盗版密钥，注册一个 VMware 账户就能免费获取。

---

## 3. 创建虚拟机

### 3.1 新建虚拟机向导

1. 打开 VMware Workstation Player
2. 点击主页的 **"Create a New Virtual Machine"**
3. 选择安装方式（参考下方表格）：

| 选项 | 说明 |
|------|------|
| **Installer disc image file (iso)** | 直接选择下载的 Windows ISO（推荐） |
| **I will install the operating system later** | 先创建空虚拟机，稍后安装 |

> [!tip] 推荐方式
> 选择 **"I will install the operating system later"** 更方便后续调整硬件配置，不会跳过 Windows 安装的硬件检测。

### 3.2 选择客户机操作系统

| 字段 | 值 |
|------|-----|
| Guest Operating System | **Microsoft Windows** |
| Version | **Windows 10 x64** 或 **Windows 11 x64** |

### 3.3 设置虚拟机名称和位置

| 字段 | 建议 |
|------|------|
| Virtual machine name | Windows 11（根据实际系统命名） |
| Location | 存放在空间充足的盘（如 `D:\VMs\Windows 11\`） |

> [!warning] 磁盘空间
> 虚拟机文件会随使用越来越大（快照、日志等），不要放在 C 盘系统分区，除非你 C 盘空间充裕。

### 3.4 指定磁盘容量

| 配置项 | 建议值 |
|--------|--------|
| Maximum disk size | 60GB+（Windows 11 建议 80GB） |
| **Store virtual disk as a single file** | ✅ 推荐（性能更好） |
| Split virtual disk into multiple files | 仅在需要跨文件系统传输时选 |

### 3.5 自定义硬件

在完成向导前，点击 **"Customize Hardware"** 调整关键配置：

#### CPU 配置

| 配置项 | 建议值 |
|--------|--------|
| Number of processors | 1 |
| Number of cores per processor | 根据宿主机情况分配（建议 2-4 核） |
| **Virtualize Intel VT-x/EPT or AMD-V/RVI** | ✅ 勾选（启用嵌套虚拟化） |

> [!tip] CPU 分配原则
> 给虚拟机分配的 CPU 核心数**不要超过宿主机物理核心数的一半**，否则会影响宿主机性能。例如 8 核宿主机给 VM 分配 2-4 核。

#### 内存配置

| 配置项 | 建议值 |
|--------|--------|
| Recommended memory | Windows 10: **4GB** / Windows 11: **8GB** |
| 最低 | Windows 10: 2GB / Windows 11: 4GB |

#### 网络适配器

| 配置项 | 说明 |
|--------|------|
| **NAT** | 共享宿主机 IP，虚拟机可上网但局域网其他设备不可见（推荐） |
| **Bridged** | 虚拟机获取独立 IP，像一台独立设备（需要路由器有空闲 IP） |
| **Host-only** | 仅宿主机和虚拟机通信，不能上网 |

> [!info] 网络模式选择
> - **新手推荐 NAT**：开箱即用，无需配置
> - **需要局域网访问**：选 Bridged（如搭建服务器让手机访问）
> - 详细对比见 [[虚拟机/虚拟网络模式/06_虚拟机网络模式.md]]

#### 其他配置

| 配置项 | 建议 |
|--------|------|
| **USB Controller** | ✅ 勾选 USB 3.0 |
| **Sound Card** | ✅ 勾选（如需音频） |
| **Printer** | ❌ 不需要则取消勾选 |
| **Display** | ✅ 勾选 **Accelerate 3D graphics**（Windows 10/11 Aero 效果需要） |

### 3.6 完成创建

点击 **Finish** 完成虚拟机创建。此时虚拟机列表会出现刚创建的项目，**先不要启动**。

---

## 4. 挂载 ISO 并安装 Windows

### 4.1 挂载系统 ISO

1. 在虚拟机列表中选择刚创建的 VM
2. 点击 **"Edit virtual machine settings"**
3. 在 CD/DVD 项中：
   - 选择 **"Use ISO image file"**
   - 点击 **Browse** 选择下载的 Windows ISO
4. 点击 **OK** 保存

### 4.2 启动并安装 Windows

1. 点击 **"Play virtual machine"** 启动
2. 看到 "Press any key to boot from CD or DVD..." 时按任意键
3. 进入 Windows 安装界面（安装步骤和注意事项见下方）

#### Windows 10 安装关键步骤

| 步骤 | 操作 |
|------|------|
| 语言选择 | 中文或 English，按需选择 |
| **Install now** | 点击安装 |
| 激活 | 可先跳过（点击 "I don't have a product key"） |
| 版本选择 | 一般选 **Windows 10 Pro** 或 **Windows 10 Home** |
| 许可条款 | 勾选后下一步 |
| 安装类型 | 选 **Custom: Install Windows only (advanced)** |
| 磁盘 | 选中未分配空间 → 下一步（无需手动分区） |

#### Windows 11 额外注意

   > [!warning] Windows 11 TPM 检查
   > Windows 11 安装时会检查 TPM 2.0 和安全启动。VMware Workstation 17 Player **默认支持虚拟 TPM**，但需要手动启用：
   >
   > 1. 关机状态下 → **Edit virtual machine settings**
   > 2. 点击 **Add...** → 选择 **Trusted Platform Module** → **Finish**
   > 3. 启动虚拟机即可通过 TPM 检查

   如果遇到 "This PC can't run Windows 11" 提示，也可以通过以下方式绕过：

   ```reg
   # 在安装界面按 Shift + F10 打开命令行，输入 regedit
   # 定位到：
   HKEY_LOCAL_MACHINE\SYSTEM\Setup
   # 新建 Key: LabConfig
   # 新建 DWORD (32-bit):
     BypassTPMCheck     = 1
   BypassSecureBootCheck = 1
   BypassRAMCheck      = 1
   BypassStorageCheck  = 1
   # 关闭注册表，关闭命令行，返回安装界面重试
   ```

### 4.3 安装过程中的注意事项

| 阶段 | 说明 |
|------|------|
| 自动重启 | 安装过程会重启多次，**这是正常的** |
| 用户名设置 | Windows 10 可以创建本地账户；Windows 11 会强制要求 Microsoft 账户登录 |
| 网络连接 | 装完系统后再配置，安装过程中如果网络慢可以跳过 |

> [!tip] Windows 11 绕过 Microsoft 账户
> 安装到"让我们为你连接到网络"时，点击 **"我没有 Internet 连接"** 或 **"我没有 Internet"**，即可创建本地账户。如果没显示这个选项，在连接网络的页面按 `Shift + F10`，输入 `OOBE\BYPASSNRO` 回车，系统重启后就会出现跳过选项。

---

## 5. 安装 VMware Tools

### 5.1 什么是 VMware Tools

VMware Tools 是一组驱动和工具，安装后能大幅提升虚拟机体验：

| 功能 | 效果 |
|------|------|
| 显示驱动 | 自适应屏幕分辨率、更高帧率 |
| 鼠标驱动 | 鼠标在宿主机和虚拟机之间平滑移动（无需按 Ctrl+Alt 释放） |
| 拖放/复制粘贴 | 在宿主机和虚拟机之间直接拖放文件、共享剪贴板 |
| 时间同步 | 自动与宿主机时间同步 |
| 性能优化 | 内存管理、网络性能提升 |

### 5.2 安装方法

1. 在虚拟机中启动 Windows
2. 在 VMware 菜单栏选择 **Player → Manage → Install VMware Tools**
3. 虚拟机中会弹出一个光驱，双击运行安装向导
4. 选择 **"Typical"** 安装模式
5. 一路 Next，点击 **Install**
6. 安装完成后根据提示**重启虚拟机**

> [!tip] 安装失败的处理
> 如果 VMware Tools 安装程序没有自动弹出，在虚拟机中打开"此电脑" → 双击 DVD 驱动器（标记为 VMware Tools）手动运行 `setup.exe`。

### 5.3 验证安装

安装完成后应该能体验到的功能：

- [x] 鼠标可以在宿主机和虚拟机之间**无缝移动**
- [x] 虚拟机窗口可以**自由调整大小**，分辨率自动适应
- [x] 可以从宿主机**拖放文件**到虚拟机
- [x] 宿主机和虚拟机**剪贴板共享**（复制粘贴）

如果以上功能没有生效，检查 VMware Tools 是否安装成功：

```
设备管理器 → 系统设备 → 应看到 "VMware 相关的设备"
```

---

## 6. 虚拟机常用设置

### 6.1 虚拟化引擎（嵌套虚拟化）

如果需要在虚拟机中再运行 WSL2、Docker 或模拟器：

1. 关机 → **Edit virtual machine settings**
2. 选择 **Processors**
3. 勾选 **"Virtualize Intel VT-x/EPT or AMD-V/RVI"**
4. 勾选 **"Virtualize IOMMU (IO memory management unit)"**

### 6.2 共享文件夹（Host-Guest File Sharing）

不想用拖放功能时，可以用共享文件夹方式访问宿主机目录：

1. 关机 → **Edit virtual machine settings**
2. 切换到 **Options** 标签（完整版 Player 支持，如果找不到则用拖放功能代替）
3. 选择 **Shared Folders**
4. 选择 **"Always enabled"**
5. 添加共享目录 → 设置名称和路径
6. 勾选 **"Map as a network drive in Windows guests"**

### 6.3 快照功能

> [!warning] 注意
> VMware Workstation Player **免费版不支持快照**（Snapshots），此功能仅 Workstation Pro 提供。如果需要快照功能，考虑使用 Pro 版或换用 VirtualBox。

替代方案：
- 在 Windows 虚拟机内使用**系统还原点**
- 定期手动备份 `.vmdk` 虚拟磁盘文件

### 6.4 虚拟机启动与暂停

| 操作 | 方式 |
|------|------|
| 启动 | 点击 **Play virtual machine** |
| 挂起（暂停） | 点击 **Suspend**（保存当前状态到磁盘，下次快速恢复） |
| 关机 | 在虚拟机内正常关机，或点击 **Power Off** |
| 重启 | 在虚拟机内重启，或 Player → Power → Restart Guest |

> [!tip] 日常使用建议
> 临时不用虚拟机时用 **Suspend（挂起）** 代替关机，下次启动只要几秒钟就能恢复到之前的工作状态。

---

## 7. 网络配置

### 7.1 切换网络模式

| 模式 | 场景 | 如何设置 |
|------|------|----------|
| NAT | 只需上网，不需要局域网访问 | 默认模式，无需修改 |
| Bridged | 需要局域网 IP，如搭建 Web 服务器 | VM Settings → Network Adapter → Bridged |
| Host-only | 仅宿主机与 VM 通信 | VM Settings → Network Adapter → Host-only |

### 7.2 端口转发（NAT 模式下暴露服务）

NAT 模式下虚拟机拥有私有 IP（通常为 `192.168.x.x`），局域网其他设备不能直接访问。如果需要外部访问虚拟机中的服务：

1. 打开 **VMware Workstation Player** 菜单
2. **Edit → Virtual Network Editor**（需要管理员权限）
3. 选择 **VMnet8（NAT 模式）**
4. 点击 **NAT Settings...**
5. 添加端口转发规则（示例见下方表格）：

| 宿主机端口 | 虚拟机 IP | 虚拟机端口 | 说明 |
|------------|-----------|------------|------|
| 3389 | 192.168.xxx.xxx | 3389 | 远程桌面（RDP） |
| 8080 | 192.168.xxx.xxx | 80 | HTTP Web 服务 |

### 7.3 Windows 防火墙注意

虚拟机中的 Windows 默认开启防火墙，外部的连接请求会被拦截。需要放行端口：

```powershell
# 在虚拟机中以管理员身份运行 PowerShell
# 放行 3389 端口（远程桌面）
New-NetFirewallRule -DisplayName "Allow RDP" -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Allow

# 放行 80 端口（Web 服务）
New-NetFirewallRule -DisplayName "Allow HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
```

---

## 8. 性能优化

### 8.1 宿主机设置

| 优化项 | 操作 |
|--------|------|
| 关闭 Hyper-V | 以管理员身份运行 PowerShell：`bcdedit /set hypervisorlaunchtype off` → 重启 |
| 关闭 Core Isolation | Windows 安全中心 → 设备安全性 → 内核隔离 → **关闭** 内存完整性 |
| 启用 VT-x/AMD-V | 进入 BIOS 开启 Intel VT-x 或 AMD-V 虚拟化支持 |

> [!warning] Hyper-V 冲突
> Windows 的 Hyper-V、WSL2、Credential Guard 会和 VMware Workstation 冲突。如果 VMware 启动虚拟机时报错 "Intel VT-x is not available"，通常是 Hyper-V 占用了虚拟化硬件。关闭 Hyper-V 并重启即可修复。

### 8.2 虚拟机设置优化

| 优化项 | 建议 |
|--------|------|
| 内存 | 不要超过宿主机内存的 50% |
| CPU | 核心数不超过宿主机物理核心的一半 |
| 磁盘 | 使用 **SCSI** 控制器（比 IDE 快） |
| 虚拟磁盘 | 选择 **"Store as single file"** |
| 显卡 | 勾选 **Accelerate 3D graphics** |

### 8.3 Windows 内优化

```powershell
# 以管理员身份在虚拟机中运行 PowerShell
# 关闭 Windows 视觉效果（低配机器）
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2

# 关闭 Windows 搜索索引（减少后台 I/O）
Stop-Service WSearch
Set-Service WSearch -StartupType Disabled

# 设置电源计划为高性能
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

---

## 9. 常见问题

### 9.1 启动报错

**Q: 启动报 "Intel VT-x is not available"**
A: 通常是因为 Hyper-V 或 Windows 沙盒占用了虚拟化硬件:
1. 关闭 Hyper-V：`bcdedit /set hypervisorlaunchtype off` → 重启
2. 进入 BIOS 确认 VT-x 已开启
3. 检查 Windows 功能，关闭 Windows 沙盒、Credential Guard

**Q: 启动报 "VMware Authorization Service is not running"**
A: 以管理员身份运行：
```cmd
net start "VMware Authorization Service"
```

### 9.2 网络问题

**Q: 虚拟机无法上网**
A: 排查顺序：
1. 确认网络模式为 NAT（最通用的模式）
2. 检查 Windows 防火墙是否阻挡
3. `ipconfig` 检查是否获取到 IP（应看到 192.168.x.x 网段）
4. 重启 VMware NAT 服务：`net start "VMware NAT Service"`

**Q: 宿主机和虚拟机互相 ping 不通**
A: 检查：
1. Windows 防火墙是否放行 ICMP（ping）
2. NAT 模式下宿主机不能直接 ping 虚拟机（因为 NAT 是单向的）
3. 互相 ping 需求请使用 Bridged 模式

### 9.3 性能问题

**Q: 虚拟机运行卡顿**
A:
1. 检查是否分配给宿主机的资源过多（CPU/内存/磁盘 I/O）
2. 确认 VMware Tools 已安装
3. 关闭虚拟机的透明效果和动画
4. 检查宿主机磁盘是否充足（SSD 剩余空间 < 20% 会降速）
5. 虚拟机磁盘碎片整理（虚拟机内执行磁盘优化）

**Q: 宿主机变卡**
A: 虚拟机占用资源过多，适当降低 CPU 核心数或内存分配

### 9.4 显示问题

**Q: 屏幕分辨率无法调整**
A: 安装 VMware Tools 即可解决。如果已安装仍无法调整：
1. 重启 VMware Tools 服务：虚拟机中打开服务管理器 → 重启 "VMware Tools" 服务
2. 或在 Player 菜单选择：**View → Autofit Window** / **Autofit Guest**

**Q: 3D 加速不工作**
A: 确认已勾选 **Accelerate 3D graphics**，且 VMware Tools 正确安装。

### 9.5 USB/SMB 问题

**Q: USB 设备无法被虚拟机识别**
A:
1. 虚拟机设置中确认 USB Controller 已启用
2. 确保宿主机的 USB 设备驱动正常
3. 在 VMware 菜单选择：**Player → Removable Devices → [您的设备] → Connect**
4. 注意：USB 设备同一时间只能被宿主机或虚拟机之一使用

**Q: 如何让虚拟机直接使用物理磁盘？**
A: 使用 Raw Disk Mapping 功能（需要 Workstation Pro，Player 不支持）。如果需要在虚拟机中访问宿主机磁盘文件，用拖放或共享文件夹功能更简单。

### 9.6 相关报错：获取虚拟机所有权失败

如果启动时遇到 "获取该虚拟机的所有权失败" 或 "主机上的某个应用程序正在使用该虚拟机"：

> 原因：虚拟机异常关闭或 VMware 崩溃，残留了 `.lck` 锁文件。
> 解决方法：到虚拟机目录删除所有 `.lck` 文件和文件夹即可。
> 详见 [[虚拟机/VMware 获取虚拟机所有权失败.md]]

---

## 10. 总结与扩展

### VMware Player 的局限

| 功能 | Player | Workstation Pro |
|------|--------|-----------------|
| 创建/运行虚拟机 | ✅ | ✅ |
| VMware Tools | ✅ | ✅ |
| 快照 | ❌ | ✅ |
| 克隆 | ❌ | ✅ |
| 加密虚拟机 | ❌ | ✅ |
| 虚拟网络编辑器 | 部分支持 | ✅ |
| 团队共享 | ❌ | ✅ |

### 替代方案

| 方案 | 优势 | 不足 |
|------|------|------|
| **VirtualBox** | 完全免费开源、支持快照 | 性能略低于 VMware |
| **Hyper-V** | Windows 内置、性能好 | 需要 Windows Pro/Enterprise |
| **PVE (Proxmox)** | 专业级虚拟化平台 | 需要独立服务器或 Linux 安装 |
| **VMware Workstation Pro** | 功能最全 | 需要付费 |

> 如果你对 PVE 上创建 Windows 虚拟机感兴趣，参考 [[PVE的学习/02-虚拟机管理/PVE创建window.md]]

### 下一步学习

- [[虚拟机/虚拟网络模式/06_虚拟机网络模式.md]] - 深入了解虚拟网络原理
- [[虚拟机/VMware 获取虚拟机所有权失败.md]] - 常见故障处理
- [[iso和img.md]] - 镜像文件格式介绍

---

> [!summary] 一句话总结
> 下载 VMware Player → 创建新虚拟机 → 指定 CPU/内存/磁盘 → 挂载 Windows ISO 安装系统 → 安装 VMware Tools 提升体验。按此流程走，30-60 分钟即可拥有一台可用的 Windows 虚拟机。
