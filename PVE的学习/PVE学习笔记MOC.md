---
tags:
  - pve
  - moc
---

# PVE 学习笔记 MOC

## 目录

- [📝 写盘准备](#📝%20写盘准备)
- [🏗️ 安装 PVE](#🏗️%20安装%20PVE)
- [⚙️ PVE 基础配置](#⚙️%20PVE%20基础配置)
- [💻 创建虚拟机](#💻%20创建虚拟机)
- [🐳 创建容器](#🐳%20创建容器)
- [🌐 网络配置](#🌐%20网络配置)
- [📦 存储管理](PVE学习笔记MOC.md#📦%20存储管理)
- [🔌 设备直通](#🔌%20设备直通)
- [🛠️ 系统优化](#🛠️%20系统优化)

---

## 📝 写盘准备

### 我要制作启动盘

**场景：准备将 PVE 安装到 U 盘或硬盘**

| 需求 | 笔记 |
|------|------|
| 了解各种写盘工具的对比和选择 | [[写盘工具]] |
| 理解 WinPE 的作用和用法 | [[WinPE]] |

### 关键要点

- **Rufus**：最常用，成功率最高，适合 Windows/Linux 启动盘
- **balenaEtcher**：最无脑，适合 Linux 镜像和树莓派
- **Ventoy**：一个 U 盘放多个系统，适合折腾党
- **WinPE**：用于清空旧分区表、统一分区表格式（GPT/MBR）、删除隐藏分区

---

## 🏗️ 安装 PVE

### 我要全新安装 PVE

**场景：从零开始安装 PVE 系统**

| 步骤 | 笔记 |
|------|------|
| 下载 PVE 镜像和准备写盘工具 | [[安装和使用PVE教程/安装和使用PVE#1下载pve系统及写盘软件]] |
| 准备 WinPE 用于格式化硬盘 | [[安装和使用PVE教程/安装和使用PVE#2下载相应的winpe]] |
| BIOS 虚拟化设置（VT-x、VT-d 等） | [[安装和使用PVE教程/安装和使用PVE#3进入bios系统]] |
| 安装和初始配置 | [[安装和使用PVE教程/安装和使用PVE#4进入配置pve]] |

### BIOS 关键设置

| 选项 | 作用 | 是否必须 |
|------|------|----------|
| Intel VT-x / AMD SVM | CPU 虚拟化基础 | ✅ 必须 |
| Intel VT-d / AMD IOMMU | 设备直通支持 | ✅ 直通必须 |
| Above 4G Decoding | PCIe 设备使用 4GB 以上地址 | ✅ 直通必须 |
| SR-IOV | 一块网卡变成多块虚拟网卡 | 可选 |
| 禁用 Secure Boot | 避免 Win11 安装限制 | 推荐 |

---

## ⚙️ PVE 基础配置

### 我要修改 PVE 的网络信息

**场景：安装后修改 IP 地址、网关等网络配置**

| 方法 | 笔记 |
|------|------|
| Web UI 修改（官方推荐） | [[安装和使用PVE教程/修改PVE的网络信息#1方法一官方推荐用-pve-web-ui-改]] |
| 命令行修改 | [[安装和使用PVE教程/修改PVE的网络信息#2方法二用命令行修改]] |

### 注意事项

- 修改后需执行 `ifreload -a` 或重启生效
- 网卡名要使用真实存在的名称（通过 `ip link` 查看）

---

## 💻 创建虚拟机

### 我要创建虚拟机

**场景：在 PVE 中创建新的虚拟机**

| 步骤 | 笔记 |
|------|------|
| 完整创建流程和配置说明 | [[安装和使用PVE教程/如何创建PVE虚拟机]] |

### 关键配置点

| 配置项 | 说明 | 笔记 |
|--------|------|------|
| BIOS | SeaBIOS（老系统）vs OVMF/UEFI（现代系统） | [[安装和使用PVE教程/如何创建PVE虚拟机#231-bios]] |
| EFI Disk | UEFI 启动必须的启动配置盘 | [[安装和使用PVE教程/如何创建PVE虚拟机#efi-disk-是干嘛的重点]] |
| 机型 | q35（新）vs i440fx（老） | [[安装和使用PVE教程/如何创建PVE虚拟机#232-机型]] |
| SCSI Controller | VirtIO SCSI 性能最好 | [[安装和使用PVE教程/如何创建PVE虚拟机#23-scsi-controller]] |
| CPU 类别 | 通常使用 host | [[安装和使用PVE教程/如何创建PVE虚拟机#24-cpu]] |

### 我要创建 Windows 虚拟机

**场景：在 PVE 中安装 Windows 系统**

| 步骤 | 笔记 |
|------|------|
| 准备 Windows ISO 和 VirtIO 驱动 | [[安装和使用PVE教程/assets/PVE创建window]] |
| 安装 VirtIO 驱动以获得最佳性能 | [[安装和使用PVE教程/assets/PVE创建window#2创建window虚拟机]] |
| 配置网络 | [[安装和使用PVE教程/assets/PVE创建window#3-配置网络]] |

### VirtIO 驱动说明

- **不用 VirtIO**：Windows 也能用，但性能差、CPU 占用高
- **使用 VirtIO**：获得直通级性能、IOPS 高、延迟小
- **下载地址**：https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers

---

## 🐳 创建容器

### 我要创建 LXC 容器

**场景：创建轻量级容器**

| 步骤 | 笔记 |
|------|------|
| 理解 CT（容器）和虚拟机的区别 | [[安装和使用PVE教程/PVE的CT]] |
| CT vs Docker 的对比 | [[安装和使用PVE教程/PVE的CT#4-ct-vs-docker重点]] |
| 下载 CT 模板和创建容器 | [[安装和使用PVE教程/PVE的CT#5-创建ct容器]] |

### CT 特点

- **性能**：接近裸机，无虚拟化损耗
- **启动速度**：1-3 秒，比虚拟机快很多
- **资源占用**：非常低
- **适合场景**：旁路由、NAS 服务、Home Assistant、Docker 宿主等

---

## 🌐 网络配置

### 我要理解 PVE 的网络逻辑

**场景：理解网桥、直通、虚拟网卡等概念**

| 概念 | 说明 | 笔记 |
|------|------|------|
| 网桥（vmbr） | 二层交换机，MAC 转发 | [[安装和使用PVE教程/PVE的网络逻辑讲解#1-网桥bridge--vmbr]] |
| 直通 | 物理网卡完全交给某个 VM | [[安装和使用PVE教程/PVE的网络逻辑讲解#2-直通pci-passthrough--网卡直通]] |
| 虚拟网卡（vNIC） | 给虚拟机用的网卡 | [[安装和使用PVE教程/PVE的网络逻辑讲解#3-虚拟网卡vnic]] |
| 内交换 | 流量不出宿主机 | [[安装和使用PVE教程/PVE的网络逻辑讲解#41-内交换internal-switching]] |
| 外交换 | 流量走物理网络 | [[安装和使用PVE教程/PVE的网络逻辑讲解#42-外交换external-switching]] |

### 网络类型对比

| 类型 | 特点 | 适合场景 |
|------|------|----------|
| 网桥（vmbr） | 二层交换机，不 NAT | 多个 VM 共享网络 |
| 直通通 | 物理网卡独占，性能最好 | 软路由、防火墙 |
| 虚拟网卡（vNIC） | VirtIO 性能最优 | 通用 VM 网络 |

---

## 📦 存储管理

### 我要理解 PVE 的存储库

**场景：理解 Storage 和 Repository 的区别和用途**

| 概念 | 说明 | 笔记 |
|------|------|------|
| 更新存储库 | 系统和组件的更新源 | [[安装和使用PVE教程/PVE存储库#2-更新存储库]] |
| 存储库 | 放 VM 磁盘 / ISO / 备份 | [[安装和使用PVE教程/PVE存储库#3-存储库]] |

### 默认存储库

| 存储库名称 | 类型 | 用途 | 能存内容 |
|------------|------|------|----------|
| local | 普通目录 | ISO、备份、模板 | ISO、Backup、Snippets |
| local-lvm | LVM Thin Pool | VM 磁盘、容器磁盘 | VM Disk、CT Disk |

### 什么时候需要新建存储库

- 加了一块新盘
- 挂了 NAS
- 想把备份单独放
- 想做快照 / ZFS
- VM 太多想分流

---

## 🔌 设备直通

### 我要做设备直通（PCI Passthrough）

**场景：将显卡、网卡、USB 控制器等物理设备直通给虚拟机**

| 步骤 | 说明 | 笔记 |
|------|------|------|
| BIOS 设置（VT-d、Above 4G Decoding） | 硬件层启用 | [[PVE直通教程/PVE直通#11-step-1bios-设置硬件层]] |
| PVE 启用 IOMMU | 系统层启用 | [[PVE直通教程/PVE直通#12-step-2pve-启用-iommu系统层关键]] |
| 验证 IOMMU 生效 | 检查是否成功 | [[PVE直通教程/PVE直通#14-step-4验证-iommu-是否生效]] |
| 确认 IOMMU 分组 | 查看设备分组情况 | [[PVE直通教程/IOMMU分组情况]] |
| 绑定 vfio 驱动 | 防止宿主机占用 | [[PVE直通教程/绑定vfio驱动]] |
| PVE Web 添加 PCI 设备 | 在 VM 中添加设备 | [[PVE直通教程/PVE直通#47-step-7pve-web-里添加-pci-设备]] |

### IOMMU 分组理解

**场景：理解为什么某些设备可以直通，某些不能**

| 主题 | 说明 | 笔记 |
|------|------|------|
| IOMMU Group 概念 | 一个 IOMMU Group = 一个安全单元 | [[PVE直通教程/IOMMU分组情况#1-iommu-group-是什么一句话版]] |
| 理想分组情况 | 教科书级的正常分组 | [[PVE直通教程/IOMMU分组情况#41-最理想的-iommu-分组教科书级]] |
| 异常分组情况 | 消费级主板常见问题 | [[PVE直通教程/IOMMU分组情况#43-你现在这种异常但很常见的分组差]] |

### vfio 驱动绑定

**场景：理解为什么需要绑定 vfio 驱动**

| 主题 | 说明 | 笔记 |
|------|------|------|
| vfio 绑定作用 | 把设备从宿主机抢走，留给虚拟机 | [[PVE直通教程/绑定vfio驱动]] |
| 什么时候必须绑定 | PCIe 直通设备 | [[PVE直通教程/绑定vfio驱动#3-什么时候必须绑定-vfio]] |
| 完整绑定过程 | 标准 PVE 做法 | [[PVE直通教程/绑定vfio驱动#4-vfio-绑定的完整过程pve-标准做法]] |

### 直通总结

> **BIOS 是"许可"，GRUB 是"执行"，vfio 是"接管"**

---

## 🛠️ 系统优化

### 我要修改 PVE 的软件源

**场景：更换国内源、禁用企业源**

| 操作 | 说明 | 笔记 |
|------|------|------|
| 禁用企业源和 Ceph 源 | 避免更新报错 | [[安装和使用PVE教程/PVE的基础优化设置#11.科学环境下源修改]] |
| 添加非订阅 PVE 源 | 免费个人用户源 | [[安装和使用PVE教程/PVE的基础优化设置#11.科学环境下源修改]] |
| 移除订阅提示 | PVE 8.0/9.0 去除弹窗 | [[安装和使用PVE教程/PVE的基础优化设置#移除订阅提示]] |
| 更换国内源 | 中科大源、清华源 | [[安装和使用PVE教程/PVE的基础优化设置#22-直连网络更换国内源]] |

### CPU 节能模式

**场景：调整 CPU 性能模式**

| 模式 | 命令 | 笔记 |
|------|------|------|
| 全核高性能 | `cpupower frequency-set -g performance` | [[安装和使用PVE教程/PVE的基础优化设置#4.2执行以下命令开启高性能或者省电模式]] |
| 全核省电 | `cpupower frequency-set -g powersave` | [[安装和使用PVE教程/PVE的基础优化设置#4.2执行以下命令开启高性能或者省电模式]] |
| 指定核心高性能 | `cpupower -c 0-15 frequency-set -g performance` | [[安装和使用PVE教程/PVE的基础优化设置#4.2执行以下命令开启高性能或者省电模式]] |

---

## 快速参考

### 常用命令

```bash
# 修改网络配置
nano /etc/network/interfaces
ifreload -a

# 启用 IOMMU
nano /etc/default/grub
update-grub

# 绑定 vfio
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

# 更新 PVE
apt update
apt dist-upgrade
```

### 相关资源

- PVE 官方下载：https://www.proxmox.com/en/downloads
- PVE VirtIO 驱动：https://pve.proxmox.com/wiki/Windows_VirtIO_Drivers
- FirPE 下载：https://www.firpe.cn
- 中科大 PVE 源：https://mirrors.ustc.edu.cn/help/proxmox.html
- 清华 PVE 源：https://mirrors.tuna.tsinghua.edu.cn/help/proxmox

---

*最后更新：2026-02-05*
