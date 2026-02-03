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
为什么选择amd64
**装 Windows 时，VirtIO 只选 `amd64`，不管你是 Intel 还是 AMD CPU。**

👉 **不要选 x86**  
👉 **选 amd64 = 64 位 Windows**
---

## 二、为什么是 amd64？（关键概念）

### 1️⃣ `amd64` 是什么？

**amd64 = x86-64 = 64 位 x86 架构**

历史原因是：

- 最早的 64 位 x86 是 **AMD 先做出来的**
    
- 所以名字叫 **amd64**
    
- 后来 Intel 也完全兼容
    

📌 所以现在：

|名字|实际意思|
|---|---|
|amd64|64 位 x86（主流）|
|x86|32 位 x86（老古董）|

---

### 2️⃣ 和你的 CPU 厂商 **完全无关**

这点非常重要 👇

- 你是 **Intel CPU** → 用 amd64
    
- 你是 **AMD CPU** → 用 amd64
    
- 你是 **PVE / ESXi / KVM** → 用 amd64
    

👉 **99.9% 的现代系统 = amd64**

---

## 三、什么时候才会用 x86（几乎不会）

只有这几种情况才选 x86（32 位）：

- 非常老的 CPU
    
- 老旧嵌入式
    
- 特殊旧软件只能跑 32 位
    

❌ Windows 10 / 11  
❌ PVE  
❌ Docker  
❌ 现代 Linux

👉 **全都不用 x86**

我们创建window中这里我们选择==**加载驱动程序**==
![](assets/PVE创建window/截屏2026-02-03%2020.20.06.png)
这里我们选择**浏览**
![](assets/PVE创建window/截屏2026-02-03%2020.19.45.png)
![](assets/PVE创建window/截屏2026-02-03%2020.22.54.png)