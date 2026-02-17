---
tags: [pve]
---

# vfio 驱动绑定详解

> [!info] 概述
> vfio 驱动绑定是将 PCIe 设备从宿主机默认驱动"抢"过来，交给虚拟机专用驱动（vfio-pci）管理的过程。
> 类比：就像把一个员工从原来的部门调出来，专门为另一个部门工作，原来的部门不能再使用这个员工。

## 核心概念 💡
- **vfio-pci**：虚拟机专用的"占坑驱动"，唯一的目的是占住设备，不让宿主机碰
- **设备归属权**：每个 PCI 设备只能被一个驱动占用
- **绑定时机**：PVE 启动时，vfio-pci 必须比默认驱动先加载

## vfio 绑定是干嘛的？

> **vfio 绑定 = 把某个硬件设备"从宿主机手里抢走"，专门留给虚拟机用**

### 一句话理解

| 状态 | 结果 |
|------|------|
| 不绑定 vfio | 设备默认归 **PVE（宿主机 Linux）** 用 |
| 绑定 vfio | 设备被"封印"，宿主机不用，**只能被虚拟机使用** |

## Linux 世界里设备的"归属权"

每一个 PCI 设备**只能被一个驱动占用**：

| 驱动 | 角色 |
|------|------|
| i915 | Intel 核显驱动 |
| r8169 | Realtek 网卡驱动 |
| xhci_hcd | USB 控制器驱动 |
| ahci | SATA 控制器驱动 |
| **vfio-pci** | 虚拟机专用"占坑驱动" |

> [!tip] vfio-pci 的唯一目的
> 占住设备，不让宿主机碰

## 为什么一定要绑定 vfio？

### 不绑定会发生什么？

启动顺序：
1. PVE 启动
2. Linux 内核加载默认驱动
   - 核显 → `i915`
   - 网卡 → `r8169`
3. 设备**已经被宿主机占用**
4. VM 启动想要这个设备
5. ❌ **拿不到/报错/黑屏**

### 绑定后的顺序

1. PVE 启动
2. vfio-pci **提前绑定设备**
3. 默认驱动（i915/r8169）**根本没机会加载**
4. VM 启动
5. ✅ 设备是"空的"，可以直接用

> [!important] 核心区别
> ⭐ **IOMMU 决定"能不能直通"**
> ⭐ **vfio 决定"谁来用"**

## 什么时候"必须"绑定 vfio？

### ✅ 必须绑定的情况

| 设备类型 | 说明 |
|---------|------|
| PCIe 显卡 | 独显、核显（要直通的话） |
| 独立 USB 卡 | PCIe 转 USB 扩展卡 |
| 独立网卡 | PCIe 网卡 |
| HBA/RAID 卡 | LSI 9211、RAID 卡等 |

👉 **100% 要绑定**

### ❌ 不需要绑定的情况

| 场景 | 说明 |
|------|------|
| 用宿主机核显硬解 | 没有直通，只是用 `/dev/dri` |
| Docker/CT 用 GPU | 容器级共享，不是 PCI 直通 |
| 没有做 PCI Passthrough | 任何"模拟设备"场景 |

## vfio 绑定的完整过程（PVE 标准做法）

> [!warning] 前提条件
> 设备**已经在独立 IOMMU Group**，否则**不要绑**

### 第 1 步：确认设备 PCI ID

```bash
lspci -nn
```

示例输出：
```
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP106 [10de:1c03]
01:00.1 Audio device [0403]: NVIDIA Corporation GP106 HDMI Audio [10de:10f1]
```

👉 **记住中括号里的 `厂商ID:设备ID`**
- `10de:1c03` → GPU
- `10de:10f1` → GPU Audio

### 第 2 步：加载 vfio 模块

```bash
nano /etc/modules
```

添加以下内容：
```bash
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```

### 第 3 步：指定哪些设备用 vfio-pci

```bash
nano /etc/modprobe.d/vfio.conf
```

写入（示例）：
```bash
options vfio-pci ids=10de:1c03,10de:10f1
```

👉 多个设备用逗号分隔

### 第 4 步：禁止宿主机原驱动加载

创建黑名单文件（可选，但推荐）：

```bash
nano /etc/modprobe.d/blacklist.conf
```

添加（针对 NVIDIA 显卡示例）：
```bash
blacklist nvidia
blacklist nouveau
```

### 第 5 步：更新 initramfs 并重启

```bash
update-initramfs -u
reboot
```

### 第 6 步：确认绑定成功（一定要做）

```bash
lspci -nnk -s 01:00.0
```

**正确结果：**
```
Kernel driver in use: vfio-pci
```

**如果还是：**
```
Kernel driver in use: nvidia
Kernel driver in use: i915
```

👉 绑定失败，**不能直通**

## 不同设备的 ID 查询示例

### Intel 核显
```bash
lspci -nn | grep VGA
# 00:02.0 VGA compatible controller [0300]: Intel Corporation HD Graphics 530 [8086:1912]
# IDs: 8086:1912
```

### NVIDIA 独显
```bash
lspci -nn | grep -i nvidia
# 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP106 [10de:1c03]
# IDs: 10de:1c03
```

### Realtek 网卡
```bash
lspci -nn | grep -i ethernet
# 03:00.0 Ethernet controller [0200]: Realtek RTL8111 [10ec:8168]
# IDs: 10ec:8168
```

## 注意事项 ⚠️

1. **PCI ID 格式必须正确**
   - 使用小写
   - 格式：`厂商ID:设备ID`
   - 多个设备用逗号分隔

2. **设备必须在独立 IOMMU Group**
   - 用 [[IOMMU分组情况]] 中的命令检查
   - 否则不要绑定

3. **重启后必须验证**
   - 用 `lspci -nnk -s 设备ID` 检查
   - 确认显示 `vfio-pci`

4. **核显直通的额外注意事项**
   - 需要在 GRUB 添加 `initcall_blacklist=sysfb_init`
   - 防止宿主机 framebuffer 占用

5. **绑定失败不要强行直通**
   - 会导致虚拟机启动失败
   - 可能影响宿主机稳定性

## 常见问题 ❓

**Q: 怎么知道设备当前被哪个驱动占用？**
A: 运行 `lspci -nnk -s 设备ID`，查看 "Kernel driver in use" 字段。

**Q: 绑定后还能在宿主机看到这个设备吗？**
A: 能看到（lspci），但宿主机不能用。设备被 vfio-pci 占住了。

**Q: 多个 GPU 怎么绑定？**
A: 在 vfio.conf 中把所有 GPU 的 ID 用逗号分隔：`ids=10de:1c03,10de:1c82,8086:1912`

**Q: 绑定后虚拟机还是不能用？**
A: 检查：1）IOMMU 是否启用，2）设备是否在独立 Group，3）虚拟机配置是否正确（勾选 All Functions）。

**Q: 如何取消绑定？**
A: 删除或注释 `/etc/modprobe.d/vfio.conf` 中的内容，运行 `update-initramfs -u && reboot`。

**Q: vfio-pci 和原驱动有什么区别？**
A: vfio-pci 不做任何硬件初始化，只是把设备"占"着等虚拟机来用。原驱动会把硬件初始化并提供功能。

## 相关文档

[[PVE直通]] | [[IOMMU分组情况]] | [[PVE学习笔记MOC]]
