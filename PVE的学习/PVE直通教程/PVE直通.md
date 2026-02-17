---
tags: [pve]
---

# PVE 设备直通完整教程

> [!info] 概述
> 设备直通（PCI Passthrough）是指将物理硬件（显卡、网卡、USB 控制器等）直接分配给虚拟机使用，虚拟机可以独占该硬件，获得接近物理机的性能。
> 类比：就像把显卡从一台电脑拔下来，直接插到另一台电脑上用一样。

## 核心概念 💡
- **IOMMU**：输入输出内存管理单元，是实现设备直通的硬件基础
- **BIOS 是"许可"**：硬件层允许操作系统玩直通
- **GRUB 是"执行"**：系统层真正启用 IOMMU 功能
- **vfio 是"接管"**：驱动层把设备从宿主机"抢"给虚拟机

## Intel x86 平台完整直通流程

> [!success] 适用场景
> - Intel 桌面/笔记本/小主机/NUC
> - 直通：核显/独显/网卡/HBA/USB 控制器

### Step 1：BIOS 设置（硬件层）

进入 BIOS 方法：[[安装和使用PVE#3-进入bios系统]]

| 选项 | 必须 | 说明 |
|------|------|------|
| Intel VT-x | ✅ | CPU 虚拟化基础 |
| **Intel VT-d** | ✅ | IOMMU（直通核心） |
| Above 4G Decoding | ✅ | 显卡/大 BAR 支持 |
| SR-IOV | 可选 | 网卡虚拟化 |
| CSM | ❌ | 关闭，使用 UEFI |

> [!tip] 这一步的意义
> BIOS 只是说一句话："我这个硬件，允许你（操作系统）玩直通"
> 但此时 PVE 还不能直通，需要在系统层面启用。

### Step 2：PVE 启用 IOMMU（系统层，关键）

#### 修改 GRUB 配置

```bash
nano /etc/default/grub
```

找到这一行：
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
```

**改成（推荐通用稳定版）：**
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt pcie_acs_override=downstream,multifunction initcall_blacklist=sysfb_init"
```

#### 参数说明

| 参数 | 作用 |
|------|------|
| `intel_iommu=on` | 真正启用 VT-d |
| `iommu=pt` | 非直通设备走直通模式，性能更好 |
| `pcie_acs_override=downstream,multifunction` | 强制拆 IOMMU 组（解决分组问题） |
| `initcall_blacklist=sysfb_init` | 防止宿主机抢核显 |

### Step 3：更新并重启

```bash
update-grub
reboot
```

### Step 4：验证 IOMMU 是否生效

```bash
dmesg | grep -e DMAR -e IOMMU
```

看到类似输出表示成功：
```
DMAR: IOMMU enabled
```

> [!danger] 如果没有看到这行
> 说明前面步骤失败，需要检查 BIOS 设置和 GRUB 配置

### Step 5：确认 IOMMU 分组情况

```bash
for d in /sys/kernel/iommu_groups/*/devices/*; do
  echo "IOMMU Group ${d#*/iommu_groups/*}: $(lspci -nns ${d##*/})"
done
```

> [!tip] 理想状态
> - 显卡、显卡音频、USB 控制器
> - **各在一个独立的 IOMMU Group**

详细讲解：[[IOMMU分组情况]]

### Step 6：绑定 vfio 驱动（防止宿主机占用）

#### 创建 vfio 配置

```bash
nano /etc/modprobe.d/vfio.conf
```

写入（示例）：
```bash
options vfio-pci ids=10de:1c82,10de:0fb9
```

> `10de:xxxx` 格式来自 `lspci -nn` 命令

#### 更新 initramfs 并重启

```bash
update-initramfs -u
reboot
```

详细讲解：[[绑定vfio驱动]]

### Step 7：PVE Web 里添加 PCI 设备

1. 打开 PVE Web 界面
2. 选择虚拟机 → Hardware → Add → PCI Device
3. 选择要直通的设备
4. **勾选关键选项**：
   - ✅ All Functions（直通设备的所有功能）
   - ✅ PCI-Express（启用 PCIe 特性）
   - ✅ ROM-Bar（部分显卡需要）

## AMD 平台注意事项

AMD 平台的步骤类似，主要区别：

| Intel | AMD |
|-------|-----|
| VT-x | SVM/AMD-V |
| VT-d | IOMMU/AMD-Vi |
| `intel_iommu=on` | `amd_iommu=on` |

GRUB 配置改为：
```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt pcie_acs_override=downstream,multifunction"
```

## 注意事项 ⚠️

1. **IOMMU 分组很重要**
   - 只有独立的 IOMMU Group 才能安全直通
   - 核心设备（Host Bridge、SATA 控制器）绝对不能直通

2. **vfio 绑定必须正确**
   - 绑定后用 `lspci -nnk -s 设备ID` 验证
   - 应该显示 `Kernel driver in use: vfio-pci`

3. **虚拟机配置**
   - 使用 UEFI（OVMF）
   - CPU 类型设置为 `host`
   - 足够的内存分配

4. **显卡直通特别注意事项**
   - 需要勾选 ROM-Bar
   - 可能需要修改 VBIOS
   - 核显直通需要额外防止宿主机占用

## 常见问题 ❓

**Q: BIOS 里找不到 VT-d 选项？**
A: 不是所有主板都支持 VT-d，查阅主板手册或联系厂商确认。

**Q: IOMMU 启用后 PVE 启动变慢？**
A: 正常现象，IOMMU 初始化需要时间。

**Q: 设备可以直通，但虚拟机蓝屏/死机？**
A: 可能是 IOMMU 分组问题，检查该 Group 是否包含其他必需设备。

**Q: 核显直通后宿主机没显示？**
A: 正常，核显已经给虚拟机了。需要安装另一张显卡给宿主机，或者使用无头模式。

**Q: 直通后性能没有提升？**
A: 检查是否正确安装了虚拟机内的驱动，确认使用的是直通设备而不是模拟设备。

## 直通总结

> **BIOS 是"许可"，GRUB 是"执行"，vfio 是"接管"**

三层缺一不可：
1. **BIOS 允许**：硬件层面支持直通
2. **GRUB 执行**：系统层面启用 IOMMU
3. **vfio 接管**：驱动层面把设备给虚拟机

## 相关文档

[[IOMMU分组情况]] | [[绑定vfio驱动]] | [[安装和使用PVE]] | [[PVE学习笔记MOC]]
