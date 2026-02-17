---
tags: [pve]
---

# IOMMU 分组详解

> [!info] 概述
> IOMMU Group 是 PCIe 设备的分组单位，决定了哪些设备可以安全地直通给虚拟机。
> 类比：就像"一栋楼的电闸"，每个电闸控制一组设备。如果只想给某个房间断电（直通），但这个房间和其他房间共用一个电闸，就不能单独操作。

## 核心概念 💡
- **IOMMU Group**：一个"要么一起直通，要么谁都别直通"的安全单元
- **隔离机制**：IOMMU 提供设备间的内存隔离，防止虚拟机访问其他设备的内存
- **分组原则**：理想情况下，每个可直通设备应该独立成组

## IOMMU Group 是什么？

> **一个 IOMMU Group = 一个安全单元**

如果你只直通组中的一个设备：
- 宿主机还在用组内的其他设备
- **风险：黑屏/死机/重启/数据损坏**

### 安全直通的前提

| 条件 | 说明 |
|------|------|
| 独立分组 | 设备在独立的 IOMMU Group 中 |
| 完整直通 | 同一 Group 内的所有设备一起直通 |
| 不涉及核心设备 | Host Bridge、SATA 控制器等不能直通 |

## 查看 IOMMU 分组

```bash
for d in /sys/kernel/iommu_groups/*/devices/*; do
  echo "IOMMU Group ${d#*/iommu_groups/*}: $(lspci -nns ${d##*/})"
done
```

## 理想的 IOMMU 分组（教科书级）

这是在**服务器主板/高端平台**上能看到的情况：

```
Group 1:
  01:00.0 VGA controller (NVIDIA RTX 3060)
  01:00.1 Audio device (HDMI Audio)

Group 2:
  02:00.0 USB controller (ASMedia ASM1142)

Group 3:
  03:00.0 Ethernet controller (Intel I350)

Group 4:
  04:00.0 SATA controller (LSI 9211-8i)
```

### 这个分组的含义

| 设备 | 状态 | 说明 |
|------|------|------|
| GPU | ✅ 可直通 | GPU + audio 在一起，正常 |
| USB | ✅ 可直通 | 独立组，安全 |
| 网卡 | ✅ 可直通 | 独立组，安全 |
| SATA | ✅ 可直通 | 独立组，安全 |

**结论：你想直通谁，就拿谁**

## 正常但"略差一点"的分组（很常见）

消费级主板、较新平台常见：

```
Group 5:
  01:00.0 VGA controller
  01:00.1 Audio device

Group 6:
  00:14.0 USB controller
  00:14.2 USB controller

Group 7:
  00:1f.3 Audio device
  00:1f.4 SMBus
```

### 如何判断？

| 分组情况 | 评估 |
|---------|------|
| GPU + audio 在一起 | ✅ 正常，可以一起直通 |
| USB 控制器有两个 | ⚠️ 整个 group 直通则安全 |
| 芯片组杂项一组 | 不动它就行 |

## 异常但很常见的分组（家用平台）

很多家用低端平台会出现：

```
Group 0:
  00:00.0 Host bridge
  00:02.0 VGA compatible controller (Intel 核显)
  00:14.0 USB controller
  00:17.0 SATA controller
  00:1f.0 ISA bridge
  00:1f.3 Audio device
  00:1f.4 SMBus
  03:00.0 Ethernet controller
```

### 这个分组的含义

| 设备 | 能否直通 | 原因 |
|------|---------|------|
| Host Bridge | ❌ 绝对不能 | CPU ↔ 内存 ↔ PCIe 的总枢纽 |
| 核显 | ❌ 不能安全直通 | 与核心设备在同一组 |
| USB 控制器 | ❌ 不能安全直通 | 宿主机键盘鼠标会失效 |
| SATA 控制器 | ❌ 绝对不能 | PVE 系统盘在这 |
| 网卡 | ❌ 不能安全直通 | 与核心设备在同一组 |

### 现实世界的比喻

> 🏠 **一整栋楼只有一个电闸**

你想做的是：
- 只给「某一个房间（核显）」断电 → 直通

但现实是：
- 这个电闸一拉 → **整栋楼（CPU/硬盘/USB/网卡）一起断**

### 这说明什么？

- 所有设备走**同一个 Root Complex**
- 没有 ACS（Access Control Services）
- 没有硬件隔离
- **这是"家用低端平台的常态"**

并不是坏，是**定位不同**

## 解决分组问题的方法

### 方法 1：使用 ACS Override 补丁

在 GRUB 配置中添加参数：

```bash
pcie_acs_override=downstream,multifunction
```

> [!warning] 注意
> 这是"强制拆组"，**不是硬件级隔离**
> 可以尝试，但不能保证 100% 安全

### 方法 2：使用 PCIe 扩展卡

将设备插在独立的 PCIe 插槽上，可能获得独立分组。

### 方法 3：更换硬件

服务器级主板通常有更好的 IOMMU 分组。

## 分组中的设备识别

### 常见设备类型

| 代码 | 类型 | 说明 |
|------|------|------|
| 0300 | VGA compatible controller | 显卡 |
| 0403 | Audio device | 声卡 |
| 0200 | Ethernet controller | 网卡 |
| 0106 | SATA controller | SATA 控制器 |
| 0c03 | USB controller | USB 控制器 |
| 0600 | Host bridge | 主机桥（不能动） |

## 注意事项 ⚠️

1. **不要试图直通核心设备**
   - Host Bridge（00:00.0）
   - SATA 控制器（如果 PVE 系统盘在上面）

2. **同一个 Group 要么全直通，要么都不直通**
   - 部分直通 = 系统不稳定

3. **ACS Override 是"软方案"**
   - 可以尝试，但不是硬件级隔离
   - 成功率不是 100%

4. **核显直通需要特别小心**
   - 通常和很多设备在同一组
   - 需要额外参数防止宿主机占用

## 常见问题 ❓

**Q: 为什么我的设备分这么乱？**
A: 家用主板通常不会为每个设备做完整的 IOMMU 隔离，这是成本和定位决定的。

**Q: ACS Override 有风险吗？**
A: 理论上有风险，因为是"软隔离"。但很多用户正常使用，建议测试后再决定。

**Q: 核显能直通吗？**
A: 理论上可以，但家用平台核显通常和核心设备在同一组。可以使用 `initcall_blacklist=sysfb_init` 参数尝试。

**Q: 怎么知道分组是否正常？**
A: 运行查看命令，如果每个可直通设备（GPU、网卡）都在独立或只包含附属设备的组里，就是正常的。

## 相关文档

[[PVE直通]] | [[绑定vfio驱动]] | [[PVE学习笔记MOC]]
