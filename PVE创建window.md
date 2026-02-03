---
tags:
  - pve
---

# 1. 前提准备
- window的iso镜像
```http
https://www.microsoft.com/zh-cn/software-download/windows10ISO
```
- virtio的镜像
```http
https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers#virtio-win_Releases
```
> **VirtIO 是“让 Windows 知道：我现在是在虚拟机里，请用最省 CPU、最快的方式跟硬件打交道”的一套专用驱动协议。**

不用 VirtIO —— 也能用  
用了 VirtIO —— **更快、更稳、更省资源**

## 1.1 如果不用 VirtIO，会发生什么？

我们对比一下 👇

### 1.1.1 不用 VirtIO（用 SATA / IDE / E1000）

虚拟机里的 Windows 会以为：

> “我在一台老旧的实体电脑上”

于是：

- 磁盘：走 **老式 SATA / IDE 模拟**
- 网卡：走 **E1000 模拟网卡**
- 特点：
    - ❌ 模拟开销大
    - ❌ I/O 慢
    - ❌ CPU 占用高
    - ✅ 兼容性好（Windows 自带）

👉 **能用，但很“虚”**

### 1.1.2 用 VirtIO（推荐）

Windows 会被明确告诉：

> “你在 PVE/KVM 虚拟机里，这是专门给你的高速接口”

于是：

- 磁盘：VirtIO Block / VirtIO SCSI
- 网卡：VirtIO Network
- 特点：
    - ✅ 几乎直通级性能
    - ✅ IOPS 高
    - ✅ CPU 占用低
    - ✅ 延迟小

👉 **这才是“虚拟机的正确打开方式”**

# 2. 创建window虚拟机
当我们按照PVE创建虚拟机的你可以看[如何创建PVE虚拟机](PVE的学习/安装和使用PVE教程/如何创建PVE虚拟机.md)。我们要在==**硬件**==中新增一个==**CD/DVD Drive**==来添加我们的virtio镜像。
![](assets/PVE创建window/截屏2026-02-03%2020.16.22.png)
改变启动循序：先window镜像，再是virtio镜像。
## 在“选择安装磁盘”那一步：
- 选择：
    `virtio-win.iso  └─ vioscsi / viostor/win10/amd64`
- Windows 才能：
    - 看见硬盘
    - 正常安装
    - 启动不蓝屏
为什么选择amd64看[安装window一般是amd64](系统架构.md#安装window一般是amd64)


我们创建window中这里我们选择==**加载驱动程序**==
![](assets/PVE创建window/截屏2026-02-03%2020.20.06.png)
这里我们选择**浏览**
![](assets/PVE创建window/截屏2026-02-03%2020.19.45.png)
![](assets/PVE创建window/截屏2026-02-03%2020.22.54.png)
window