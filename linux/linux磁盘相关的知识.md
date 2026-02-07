---
tags:
  - linux
---

# Linux 磁盘管理

## 一句话概括

在 Linux 中，所有文件都存在分区上，但用户只看到一个统一的目录树。分区通过"挂载"连接到这棵树的不同节点上。

---

# 1. 基础概念

## 1.1 核心概念对比

| 概念 | 作用 | 举例 |
|------|------|------|
| **磁盘** | 物理存储设备 | /dev/sda、/dev/nvme0n1 |
| **分区** | 磁盘的逻辑划分 | /dev/sda1、/dev/sdb2 |
| **文件系统** | 分区内组织文件的结构 | ext4、xfs、ntfs |
| **挂载点** | 把文件系统接入目录树 | /、/home、/mnt/data |

## 1.2 Linux 目录树结构

Linux 只有一个统一的目录树，没有 Windows 的 C 盘、D 盘概念：

```
/                    ← 根目录
├── bin/            → 系统命令
├── boot/           → 启动文件
├── etc/            → 配置文件
├── home/           → 用户主目录
├── var/            → 日志/缓存
└── mnt/            → 临时挂载点
```

无论你有多少块磁盘，所有文件最终都挂载到这棵树上。

## 1.3 什么是挂载（Mount）？

挂载就是把分区"接"到目录树的某个节点上。

例如：
```bash
sudo mount /dev/sdb1 /home
```

执行后，访问 `/home/user/file.txt` 实际上是在访问 `/dev/sdb1` 这个分区。

---

# 2. 硬盘命名规则

## 2.1 磁盘类型与命名

| 硬盘类型 | 命名示例 | 说明 |
|----------|----------|------|
| SATA/SCSI/SAS | /dev/sda、/dev/sdb、/dev/sdc | 传统硬盘，a=第一块、b=第二块 |
| NVMe SSD | /dev/nvme0n1、/dev/nvme1n1 | PCIe 固态硬盘 |
| USB 移动硬盘 | /dev/sdb、/dev/sdc | 插入顺序决定 |
| eMMC（嵌入式） | /dev/mmcblk0 | 板载闪存 |

## 2.2 分区命名

| 硬盘 | 第一个分区 | 第二个分区 |
|------|-----------|-----------|
| /dev/sda | /dev/sda1 | /dev/sda2 |
| /dev/nvme0n1 | /dev/nvme0n1p1 | /dev/nvme0n1p2 |
| /dev/mmcblk0 | /dev/mmcblk0p1 | /dev/mmcblk0p2 |

**注意**：NVMe 和 eMMC 需要 `p` 分隔符（如 p1、p2）。

---

# 3. 分区表类型

## 3.1 MBR vs GPT

| 对比项 | MBR（老式） | GPT（新式，推荐） |
|--------|-------------|------------------|
| 磁盘容量 | 最大 2TB | 理论 8ZB（几乎无限） |
| 分区数量 | 最多 4 个主分区 | 默认 128 个 |
| 引导方式 | BIOS | UEFI |
| 备份分区表 | 无 | 有（主表+备份表） |

## 3.2 MBR 的限制（历史遗留）

MBR 最多只能有 4 个主分区。为了分更多，引入了：

- **扩展分区**：容器，不存数据
- **逻辑分区**：存在扩展分区内部，可以有很多个

## 3.3 推荐

现代 Linux 系统（特别是 UEFI 启动）几乎都使用 **GPT**，不需要考虑主/扩展/逻辑分区的复杂问题。

---

# 4. 文件系统类型

| 类型 | 特点 | 适用场景 |
|------|------|----------|
| **ext4** | 通用、稳定，Linux 默认 | 桌面、服务器 |
| **xfs** | 性能好，适合大文件 | 服务器、数据库 |
| **btrfs** | 支持快照、压缩 | 需要 advanced 功能 |
| **FAT32** | 跨平台兼容 | U 盘、移动硬盘 |
| **NTFS** | Windows 原生 | 与 Windows 共用 |

**注意**：xfs 只能扩容，不能缩小；ext4 两者都支持。

---

# 5. 添加新硬盘的完整流程

## 5.1 流程总览

```
查看硬盘 → 分区 → 格式化 → 挂载 → 设置自动挂载
```

## 5.2 具体步骤

### 步骤 1：查看硬盘

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

### 步骤 2：分区

使用 `fdisk`（简单）或 `gdisk`（GPT）：

```bash
sudo fdisk /dev/sdb
```

常用命令：
- `m` - 帮助
- `p` - 查看分区表
- `n` - 新建分区
- `d` - 删除分区
- `w` - 写入保存
- `q` - 退出不保存

创建分区示例：
```
n                     # 新建分区
p                     # 主分区
回车                   # 使用默认分区号
回车                   # 默认起始位置
+100G                 # 分区大小 100G
w                     # 写入
```

刷新分区表：
```bash
sudo partprobe
```

### 步骤 3：格式化

```bash
sudo mkfs.ext4 /dev/sdb1    # 格式化为 ext4
```

### 步骤 4：挂载

```bash
sudo mkdir /mnt/data        # 创建挂载点
sudo mount /dev/sdb1 /mnt/data
```

验证：
```bash
df -h
```

### 步骤 5：设置开机自动挂载

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
sudo mount -a    # 无报错则成功
```

# 6. 如何扩充先有的分区
**关键认知：分区 ≠ 数据本身**

- 分区表（GPT / MBR）只是一张 **“指路牌”**
- 真正的数据：
    - 文件系统
    - LVM 元数据
    - 文件内容  
        👉 **都在磁盘扇区里**

## 6.1 删除分区时发生了什么？

`❌ 没发生：清零磁盘 / 删除文件 ✅ 只发生：分区表里那一行记录没了`

就像：

> 把“房产证”撕了  
> 房子本身 **还在原地**

## 6.2 正确操作顺序（不会丢数据）

### 6.2.1 删除分区（只是表）

```
fdisk /dev/sda
d   # 删除 sda2
```

⚠️ 此时：

- **PV / VG / LV 都还在**
- 只是 Linux 暂时“找不到入口”

### 6.2.2  立刻重建分区（关键！）

```bash
n
p
2
<起始扇区：和原来一模一样>
<直接回车，用满剩余空间>
```

✔ 起始扇区一样  
✔ 覆盖原数据区 + 新空间

这时可能会出现提示：
```bash
Do you want to remove the signature? [Y]es/[N]o:  
```
这个提示到底在问什么？🧠
这是 LVM 的“身份证”，里面记录着：

- 这个分区属于哪个 PV
- 属于哪个 VG
- 逻辑卷结构信息

👉 没有它，LVM 就认不出你的数据了

### 6.2.3 保存并刷新

```
w
partprobe
```

---

### 6.2.4 LVM 扩容（这一步才真正“用上”新空间）

#### ① 扩展物理卷（PV）

```bash
sudo pvresize /dev/sda3
```

验证一下：

```bash
pvs
```

你应该能看到 `PFree` 变大了。

---

#### ② 扩展逻辑卷（LV）

把 **VG 里所有空闲空间** 全部给 `/`：

```bash
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

你会看到类似：

`Size of logical volume ubuntu-vg/ubuntu-lv changed from 193.50 GiB to 278.00 GiB`

---

### ③ 扩展文件系统（ext4）

你这个 `/` 基本可以确定是 **ext4**：

```
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

> 这个命令 **在线执行即可**，不用卸载 `/`

---


# 7. /etc/fstab 配置详解

格式：
```
<设备>  <挂载点>  <文件系统>  <挂载选项>  <dump>  <fsck>
```

## 7.1 各字段说明

| 字段 | 说明 | 常用值 |
|------|------|--------|
| 设备 | 要挂载的分区 | `UUID=xxx` 或 `/dev/sdb1` |
| 挂载点 | 挂载到哪个目录 | `/mnt/data`、`/home` |
| 文件系统 | 分区类型 | `ext4`、`xfs`、`swap` |
| 挂载选项 | 挂载行为 | `defaults` 或 `rw,noatime` |
| dump | 是否备份 | `0`（不备份） |
| fsck | 开机检查顺序 | `0`（不检查）、`1`（根分区）、`2`（其他） |

## 7.2 常用挂载选项

`defaults` 等同于：`rw,suid,dev,exec,auto,nouser,async`

| 选项 | 作用 |
|------|------|
| `rw` | 可读写 |
| `ro` | 只读 |
| `noatime` | 不更新访问时间（提高性能） |
| `auto` | 开机自动挂载 |

---

# 8. Swap 交换分区

## 8.1 什么是 Swap？

Swap 是磁盘上的一块区域，当内存不够时，系统会把不用的数据"搬"到 Swap 里。

类比：
- **内存** = 办公桌，快速但空间小
- **Swap** = 旁边的柜子，慢但容量大

## 8.2 Swap 的大小推荐

| 内存大小 | 推荐 Swap 大小 |
|----------|---------------|
| ≤ 2GB | 内存的 2 倍 |
| 4GB ~ 8GB | 与内存相同 |
| ≥ 16GB | 2GB ~ 4GB |
| 需要休眠 | ≥ 内存大小 |

## 8.3 创建 Swap 文件（推荐）

```bash
sudo fallocate -l 4G /swapfile    # 创建 4GB 文件
sudo chmod 600 /swapfile           # 设置权限
sudo mkswap /swapfile              # 格式化为 swap
sudo swapon /swapfile              # 启用
```

开机自动启用，编辑 `/etc/fstab`：
```
/swapfile none swap sw 0 0
```

## 8.4 查看 Swap 使用情况

```bash
free -h
```

输出示例：
```
              total        used        free      shared  buff/cache   available
Mem:           15Gi        3.1Gi        10.8Gi       200Mi       2.2Gi       11Gi
Swap:          2Gi          0Mi         2Gi
```

重点看：
- `available`：真正可用的内存
- `Swap used`：如果非 0，说明内存紧张

---

# 9. 常用命令速查

## 9.1 查看命令

| 命令 | 作用 |
|------|------|
| `lsblk` | 查看磁盘和分区结构 |
| `df -h`' | 查看已挂载分区的使用情况 |
| `free -h` | 查看内存和 Swap 使用情况 |
| `blkid` | 查看分区 UUID 和类型 |
| `du -sh 目录` | 查看目录占用空间 |

## 9.2 分区命令

| 命令 | 作用 |
|------|------|
| `fdisk /dev/sda` | 交互式分区（MBR/GPT） |
| `gdisk /dev/sda` | 交互式分区（GPT 专用） |
| `partprobe` | 刷新分区表 |

## 9.3 文件系统命令

| 命令 | 作用 |
|------|------|
| `mkfs.ext4 /dev/sdb1` | 格式化为 ext4 |
| `mkfs.xfs /dev/sdb1` | 格式化为 xfs |
| `resize2fs /dev/sdb1` | 扩展/缩小 ext4 |
| `xfs_growfs /` | 扩展 xfs（只能扩） |

## 9.4 挂载命令

| 命令 | 作用 |
|------|------|
| `mount /dev/sdb1 /mnt` | 挂载分区 |
| `umount /mnt` | 卸载分区 |
| `mount -a` | 挂载 /etc/fstab 中的所有项 |

---

# 10. 磁盘满了怎么办？

## 10.1 查看整体情况

```bash
df -h
```

如果 `/` 使用率 >90%，就需要清理了。

## 10.2 找出占用空间最大的目录

```bash
sudo du -h --max-depth=1 / | sort -h
```

输出示例：
```
500M    /boot
1.2G    /usr
8.5G    /var
25G     /home
```

对着最大的目录继续深挖：
```bash
sudo du -h --max-depth=1 /var | sort -h
```

## 10.3 常见占用空间的位置

| 位置 | 查看 | 说明 |
|------|------|------|
| 日志 | `sudo du -sh /var/log` | 系统日志可能很大 |
| 缓存 | `du -sh ~/.cache` | pip、conda、HuggingFace 缓存 |
| Docker | `sudo du -sh /var/lib/docker` | Docker 镜像和容器 |
| Snap | `sudo du -sh /var/lib/snapd` | Snap 包占用 |

---

# 11. 进阶：LVM 逻辑卷管理

传统的分区方式一旦创建，大小就很难调整。

**LVM（Logical Volume Manager）** 提供了更灵活的管理方式，特点：
- 在线扩容/缩容（无需停机）
- 多磁盘合并使用
- 支持快照

LVM 的三层架构：
```
PV（物理卷）→ VG（卷组）→ LV（逻辑卷）
```

详细内容请参考：[[linux的LVM管理]]
[linux磁盘相关的知识](#8.3%20文件系统命令)