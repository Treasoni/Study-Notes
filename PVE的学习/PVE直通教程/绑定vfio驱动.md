
**vfio 绑定是干嘛的？（一句话版）**

> **vfio 绑定 = 把某个硬件设备“从宿主机手里抢走”，专门留给虚拟机用**

**用一句非常形象的话说**

- **不绑定 vfio**：  
    👉 设备默认归 **PVE（宿主机 Linux）** 用
- **绑定 vfio**：  
    👉 设备被“封印”，宿主机不用  
    👉 **只能被虚拟机使用**

# 1. Linux 世界里设备的“归属权”

每一个 PCI 设备 **只能被一个驱动占用**：

|驱动|角色|
|---|---|
|i915|Intel 核显|
|r8169|Realtek 网卡|
|xhci_hcd|USB 控制器|
|ahci|SATA|
|**vfio-pci**|虚拟机专用“占坑驱动”|

👉 **vfio-pci 的唯一目的：占住设备，不让宿主机碰**

# 2. 为什么一定要绑定 vfio？

如果你**不绑定**，会发生什么？

## 2.1 例子：直通核显（或网卡 / USB）

启动顺序是这样的：

1️⃣ PVE 启动  
2️⃣ Linux 内核加载默认驱动

- 核显 → `i915`
- 网卡 → `r8169`  
    3️⃣ 设备 **已经被宿主机占用**  
    4️⃣ VM 启动想要这个设备  
    👉 ❌ **拿不到 / 报错 / 黑屏**

**绑定 vfio 后，顺序变成：**

1️⃣ PVE 启动  
2️⃣ vfio-pci **提前绑定设备**  
3️⃣ 默认驱动（i915 / r8169）**根本没机会加载**  
4️⃣ VM 启动  
👉 ✅ 设备是“空的”，可以直接用

> [!important]

> ⭐ 
> **IOMMU 决定“能不能直通”  
> vfio 决定“谁来用”**

# 3. 什么时候“必须”绑定 vfio？

## 3.1 ✅ 必须绑定的情况

- PCIe 直通：
    - GPU
    - 独立 USB 卡
    - 独立网卡
    - HBA / RAID 卡

👉 **100% 要绑定**

## 3.2 ❌ 不需要绑定的情况

- 你只是：
    - 用宿主机核显硬解
    - Docker / CT 用 `/dev/dri`
- 没有做 PCI Passthrough

# 4. vfio 绑定的完整过程（PVE 标准做法）

⚠️ 前提：

- 设备 **已经在独立 IOMMU Group**
- 否则 **不要绑**

## 4.1 第 1 步：确认设备 PCI ID

```bash
lspci -nn
```

示例：

```bash
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GP106 [10de:1c03]
01:00.1 Audio device [0403]: NVIDIA Corporation GP106 HDMI Audio [10de:10f1]
```

👉 **记住中括号里的 `厂商ID:设备ID`**

## 4.2 第 2 步：加载 vfio 模块

```bash
nano /etc/modules
```

加入：

```bash
vfio
vfio_iommu_type1
vfio_pci
vfio_virqfd
```


## 4.3 第 3 步：指定哪些设备用 vfio-pci

```bash
nano /etc/modprobe.d/vfio.conf
```

写入：

```bash
options vfio-pci ids=10de:1c03,10de:10f1
```

👉 多个设备用逗号分隔

## 4.4 第 4 步（非常重要）：禁止宿主机原驱动加载

然后：
```bash
update-initramfs -u
reboot
```


## 4.5 第 5 步：确认绑定成功（一定要做）

```bash
lspci -nnk -s 01:00.0
```

正确结果：

`Kernel driver in use: vfio-pci`

如果还是：

`Kernel driver in use: i915 / r8169`

👉 绑定失败，**不能直通**
