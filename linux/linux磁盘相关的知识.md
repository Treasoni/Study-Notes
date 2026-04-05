---
tags: [linux]
---

# Linux 磁盘管理

> [!info] 概述
> **Linux 磁盘管理就像整理一个大仓库** - 把不同大小的货柜（硬盘）分区、标记（格式化），然后放到指定位置（挂载），方便存取货物（文件）。

## 核心概念 💡

### 磁盘命名规则

**传统硬盘**：
- `/dev/sda` - 第一块 SATA/SCSI/SAS 硬盘
- `/dev/sdb` - 第二块硬盘
- `/dev/sda1` - 第一块硬盘的第一个分区

**NVMe SSD**：
- `/dev/nvme0n1` - 第一块 NVMe 硬盘
- `/dev/nvme0n1p1` - 第一块 NVMe 硬盘的第一个分区
- `/dev/nvme1n1` - 第二块 NVMe 硬盘

**其他设备**：
- `/dev/mmcblk0` - eMMC 嵌入式存储
- `/dev/sr0` - 光驱设备

### 分区表类型

| 类型 | MBR（老式） | GPT（新式，推荐） |
|------|-------------|------------------|
| 磁盘容量 | 最大 2TB | 理论 8ZB |
| 分区数量 | 最多 4 个主分区 | 默认 128 个 |
| 引导方式 | BIOS | UEFI |
| 备份分区表 | 无 | 有（主表+备份表）|

### 文件系统类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| **ext4** | 通用、稳定，Linux 默认 | 桌面、服务器 |
| **xfs** | 性能好，适合大文件 | 服务器、数据库 |
| **btrfs** | 支持快照、压缩 | 高级功能需求 |
| **FAT32** | 跨平台兼容 | U 盘、移动硬盘 |
| **NTFS** | Windows 原生 | 与 Windows 共用 |

### 挂载（Mount）

挂载就是把分区"接"到目录树的某个节点上。例如：
```bash
sudo mount /dev/sdb1 /mnt/data
```

执行后，访问 `/mnt/data/file.txt` 实际上是在访问 `/dev/sdb1` 这个分区。

## 操作步骤

### 场景一：添加新硬盘

#### 流程总览
```
查看硬盘 → 分区 → 格式化 → 挂载 → 设置自动挂载
```

#### 1. 查看硬盘
```bash
lsblk
```

输出示例：
```
sda    8:0  0 100G 0 disk
├─sda1 8:1  0 50G  0 part /
└─sda2 8:2  0 50G  0 part /home
sdb    8:16 0 500G 0 disk    ← 新硬盘
```

#### 2. 分区
```bash
sudo fdisk /dev/sdb
```

交互式操作：
```
m   # 帮助
p   # 查看分区表
n   # 新建分区
d   # 删除分区
w   # 写入保存
q   # 退出不保存
```

创建分区示例：
```
n   # 新建分区
p   # 主分区
回车  # 使用默认分区号
回车  # 默认起始位置
+100G  # 分区大小 100G
w   # 写入
```

刷新分区表：
```bash
sudo partprobe
```

#### 3. 格式化
```bash
# ext4（推荐）
sudo mkfs.ext4 /dev/sdb1

# xfs
sudo mkfs.xfs /dev/sdb1
```

#### 4. 挂载
```bash
sudo mkdir /mnt/data
sudo mount /dev/sdb1 /mnt/data
```

验证：
```bash
df -h
```

#### 5. 设置开机自动挂载

获取 UUID：
```bash
sudo blkid /dev/sdb1
```

编辑 `/etc/fstab`：
```bash
sudo nano /etc/fstab
```

添加一行：
```
UUID=你的UUID /mnt/data ext4 defaults 0 2
```

测试配置：
```bash
sudo mount -a
```

### 场景二：扩展现有分区

> [!warning] 重要提示
> 扩展分区涉及删除分区表，操作不当会导致数据丢失。建议先备份重要数据！

#### 1. 查看当前分区
```bash
lsblk
sudo fdisk -l
```

#### 2. 删除并重建分区

```bash
sudo fdisk /dev/sda
```

操作步骤：
```
d   # 删除分区
2   # 选择要删除的分区号（如 sda2）
n   # 新建分区
p   # 主分区
2   # 分区号
<起始扇区：和原来一模一样>
<直接回车，用满剩余空间>
```

如果提示 "Do you want to remove the signature?"，选择 **N**（保留 LVM 签名）。

```
w   # 写入保存
```

刷新分区表：
```bash
sudo partprobe
```

#### 3. 扩展 LVM（如果使用 LVM）

```bash
# 扩展物理卷
sudo pvresize /dev/sda2

# 扩展逻辑卷
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv

# 扩展文件系统（ext4）
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

#### 4. 验证
```bash
df -h
```

### 场景三：Swap 交换分区

#### 创建 Swap 文件（推荐）
```bash
# 创建 4GB 文件
sudo fallocate -l 4G /swapfile

# 设置权限
sudo chmod 600 /swapfile

# 格式化为 swap
sudo mkswap /swapfile

# 启用
sudo swapon /swapfile
```

#### 设置开机自动启用
```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### 查看 Swap 使用情况
```bash
free -h
```

输出示例：
```
              total        used        free      shared  buff/cache   available
Mem:           15Gi        3.1Gi        10.8Gi       200Mi       2.2Gi       11Gi
Swap:          2Gi          0Mi         2Gi
```

## 注意事项 ⚠️

### 常见错误

**忘记刷新分区表**：
```bash
# 分区后直接格式化报错
sudo mkfs.ext4 /dev/sdb1
# Could not access /dev/sdb1

# 解决：刷新分区表
sudo partprobe
```

**fstab 配置错误导致无法开机**：
```bash
# 测试配置
sudo mount -a

# 如果报错，修复 fstab 后再测试
```

**UUID 变化导致挂载失败**：
```bash
# 重新获取 UUID
sudo blkid /dev/sdb1

# 更新 fstab 中的 UUID
```

### 关键配置点

**/etc/fstab 格式**：
```
<设备>  <挂载点>  <文件系统>  <挂载选项>  <dump>  <fsck>
```

**常用挂载选项**：
- `defaults` - 等同于 `rw,suid,dev,exec,auto,nouser,async`
- `noatime` - 不更新访问时间（提高性能）
- `ro` - 只读
- `rw` - 可读写

**Swap 大小推荐**：
| 内存大小 | 推荐 Swap 大小 |
|----------|---------------|
| ≤ 2GB | 内存的 2 倍 |
| 4GB ~ 8GB | 与内存相同 |
| ≥ 16GB | 2GB ~ 4GB |
| 需要休眠 | ≥ 内存大小 |

## 常用命令速查

### 查看命令
| 命令 | 作用 |
|------|------|
| `lsblk` | 查看磁盘和分区结构 |
| `df -h` | 查看已挂载分区的使用情况 |
| `free -h` | 查看内存和 Swap 使用情况 |
| `blkid` | 查看分区 UUID 和类型 |
| `du -sh 目录` | 查看目录占用空间 |

### 分区命令
| 命令 | 作用 |
|------|------|
| `fdisk /dev/sda` | 交互式分区（MBR/GPT）|
| `gdisk /dev/sda` | 交互式分区（GPT 专用）|
| `partprobe` | 刷新分区表 |

### 文件系统命令
| 命令 | 作用 |
|------|------|
| `mkfs.ext4 /dev/sdb1` | 格式化为 ext4 |
| `mkfs.xfs /dev/sdb1` | 格式化为 xfs |
| `resize2fs /dev/sdb1` | 扩展/缩小 ext4 |
| `xfs_growfs /` | 扩展 xfs（只能扩）|

### 挂载命令
| 命令 | 作用 |
|------|------|
| `mount /dev/sdb1 /mnt` | 挂载分区 |
| `umount /mnt` | 卸载分区 |
| `mount -a` | 挂载 /etc/fstab 中的所有项 |

## 常见问题 ❓

**Q: 磁盘满了怎么办？**

A: 按以下步骤排查：
```bash
# 1. 查看整体情况
df -h

# 2. 找出占用空间最大的目录
sudo du -h --max-depth=1 / | sort -h

# 3. 检查常见占用位置
sudo du -sh /var/log      # 日志
du -sh ~/.cache           # 缓存
sudo du -sh /var/lib/docker  # Docker
```

**Q: 如何安全地卸载分区？**

A: 确保没有程序在使用：
```bash
# 查看哪些进程在使用
sudo lsof /mnt/data

# 卸载
sudo umount /mnt/data

# 如果提示"目标忙"，使用延迟卸载
sudo umount -l /mnt/data
```

**Q: NVMe 硬盘和 SATA 硬盘有什么区别？**

A: 主要区别：
- **性能**：NVMe 使用 PCIe 通道，速度远超 SATA
- **命名**：NVMe 使用 `/dev/nvme0n1`，SATA 使用 `/dev/sda`
- **分区**：NVMe 分区带 `p`（如 `nvme0n1p1`），SATA 直接加数字（如 `sda1`）

**Q: 如何检查磁盘健康状态？**

A: 使用 `smartctl` 工具：
```bash
# 安装
sudo apt install smartmontools

# 检查磁盘健康
sudo smartctl -H /dev/sda

# 查看详细信息
sudo smartctl -a /dev/sda
```

**Q: 如何修复文件系统错误？**

A: 使用 `fsck` 工具：
```bash
# 卸载分区
sudo umount /dev/sdb1

# 检查并修复
sudo fsck /dev/sdb1

# 重新挂载
sudo mount /dev/sdb1 /mnt
```

## 相关文档
- [[linux MOC]] - Linux 学习笔记索引
- [[linux的LVM管理]] | [[linux的文件权限]]
