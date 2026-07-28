---
tags: [linux, lvm, storage]
created: 2025-01-01
updated: 2026-07-28
---

# LVM 逻辑卷管理

> [!info] 概述
> **LVM 就像一个"动态空间池"** - 把多块硬盘的空间合并成一个池子，然后按需分配给不同的逻辑卷，可以随时扩容或缩小，无需重启系统。

## 核心概念 💡

### LVM 三层架构
```
PV（物理卷）→ VG（卷组）→ LV（逻辑卷）
```

### PV（Physical Volume，物理卷）
- **是什么**：被 LVM 接管的硬盘分区或整个硬盘
- **为什么需要**：将物理存储空间统一管理
- **与其他概念关系**：多个 PV 可以合并成一个 VG

### VG（Volume Group，卷组）
- **是什么**：一个"统一的空间仓库/池子"
- **为什么需要**：实现跨磁盘的空间分配
- **与其他概念关系**：VG 从多个 PV 获取空间，分配给多个 LV

### LV（Logical Volume，逻辑卷）
- **是什么**：真正能格式化、挂载、被系统使用的"假分区"
- **为什么需要**：灵活分配空间，支持动态扩容
- **与其他概念关系**：LV 从 VG 获取空间，挂载到目录树

> [!tip] 银行类比
> - 现金 → 存入银行（PV）
> - 银行账户（VG）
> - 取钱到卡上（LV）
> - 刷卡消费（挂载使用）

## 操作步骤

### 场景一：新增硬盘扩容

#### 流程总览
```
新硬盘 → 创建 PV → 加入 VG → 扩展 LV → 扩展文件系统
```

#### 1. 确认新硬盘
```bash
lsblk
```

输出示例：
```
sda   200G
sdb   200G   ← 新硬盘
```

#### 2. 创建分区（可选）
```bash
sudo fdisk /dev/sdb
```

交互式操作：
```
n   # 新建分区
p   # 主分区
回车 回车 回车  # 使用整块盘
t   # 修改类型
8e  # Linux LVM
w   # 写入保存
```

刷新分区表：
```bash
sudo partprobe
```

#### 3. 创建物理卷
```bash
sudo pvcreate /dev/sdb
# 或使用分区
sudo pvcreate /dev/sdb1
```

验证：
```bash
sudo pvs
```

#### 4. 扩展卷组
```bash
# 查看现有卷组
sudo vgs

# 将新 PV 加入现有 VG
sudo vgextend ubuntu-vg /dev/sdb
```

#### 5. 扩展逻辑卷（二选一）

**方法 A：扩展全部剩余空间**
```bash
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
```

**方法 B：扩展指定大小**
```bash
sudo lvextend -L +100G /dev/ubuntu-vg/ubuntu-lv
```

**方法 C：一步到位（推荐）**
```bash
# -r 参数同时扩展文件系统
sudo lvextend -l +100%FREE -r /dev/ubuntu-vg/ubuntu-lv
```

#### 6. 扩展文件系统（如果没用 -r 参数）

**ext4 文件系统**：
```bash
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

**xfs 文件系统**：
```bash
sudo xfs_growfs /
```

#### 7. 验证
```bash
df -h
```

### 场景二：创建新的逻辑卷

#### 1. 从 VG 分配空间创建 LV
```bash
# 创建 50G 的 LV
sudo lvcreate -L 50G -n data-lv ubuntu-vg

# 使用所有剩余空间
sudo lvcreate -l 100%FREE -n data-lv ubuntu-vg
```

#### 2. 格式化
```bash
# ext4（推荐）
sudo mkfs.ext4 /dev/ubuntu-vg/data-lv

# xfs
sudo mkfs.xfs /dev/ubuntu-vg/data-lv
```

#### 3. 挂载
```bash
sudo mkdir /data
sudo mount /dev/ubuntu-vg/data-lv /data
```

#### 4. 设置开机自动挂载
```bash
# 获取 UUID
sudo blkid /dev/ubuntu-vg/data-lv

# 编辑 fstab
sudo nano /etc/fstab
```

添加：
```
UUID=你的UUID /data ext4 defaults 0 2
```

测试：
```bash
sudo mount -a
```

### 场景三：LVM 快照备份

#### 创建快照
```bash
# 创建 10G 的快照
sudo lvcreate -L 10G -s -n ubuntu-lv-snap /dev/ubuntu-vg/ubuntu-lv
```

#### 挂载快照查看内容
```bash
sudo mkdir /mnt/snapshot
sudo mount /dev/ubuntu-vg/ubuntu-lv-snap /mnt/snapshot
ls /mnt/snapshot
```

#### 删除快照
```bash
sudo lvremove /dev/ubuntu-vg/ubuntu-lv-snap
```

### 场景四：缩小 LV（危险操作）

> [!warning] 重要限制
> - **xfs 文件系统不能缩小！**
> - 只能缩小 ext4/btrfs
> - 必须先缩小文件系统，再缩小 LV

#### 缩小 ext4 LV 的步骤
```bash
# 1. 卸载 LV
sudo umount /data

# 2. 检查文件系统（必须）
sudo e2fsck -f /dev/ubuntu-vg/data-lv

# 3. 先缩小文件系统到 30G
sudo resize2fs /dev/ubuntu-vg/data-lv 30G

# 4. 再缩小 LV 到 30G
sudo lvreduce -L 30G /dev/ubuntu-vg/data-lv

# 5. 重新挂载
sudo mount /dev/ubuntu-vg/data-lv /data
```

### 场景五：Thin Provisioning（精简配置）

> [!tip] 核心概念
> **Thin Provisioning = "超卖"** - 可以创建比实际物理空间"更大"的逻辑卷，真正写入数据时才占用磁盘块。适合虚拟化、容器环境。

#### 与传统厚配置的区别

| 对比项 | 厚配置 (Thick) | 精简配置 (Thin) |
|--------|---------------|----------------|
| 空间分配 | 创建时立即分配 | 按需分配，写入多少占多少 |
| 利用率 | 低（预留不用 = 浪费） | 高（共享池，超额分配） |
| 性能 | 稳定 | 池满时可能触发 STALL |
| 监控要求 | 低 | 高（必须监控池水位） |

#### Thin Pool 架构

```
Thin Pool（数据区 + 元数据区）
    ├── Thin LV-A（虚拟 100G，实际 20G）
    ├── Thin LV-B（虚拟 100G，实际 10G）
    └── Thin LV-C（虚拟 100G，实际 5G）
        ↑ 累计虚拟 300G，实际占用 35G
```

#### 1. 创建 Thin Pool

```bash
# 创建 200G 的 thin pool
sudo lvcreate -L 200G --thinpool thin_pool ubuntu-vg
```

为大型池指定元数据区大小：
```bash
sudo lvcreate -L 200G --thinpool thin_pool --poolmetadatasize 2G ubuntu-vg
```

#### 2. 从 Thin Pool 创建 Thin LV

```bash
# 创建虚拟 500G 的 thin LV（远超 pool 的 200G）
sudo lvcreate -V 500G --thin -n vm1-disk ubuntu-vg/thin_pool
sudo lvcreate -V 500G --thin -n vm2-disk ubuntu-vg/thin_pool

# 总虚拟 1000G，实际仅占 thin pool 的 200G
```

#### 3. 格式化和使用

```bash
sudo mkfs.ext4 /dev/ubuntu-vg/vm1-disk
sudo mount /dev/ubuntu-vg/vm1-disk /mnt/vm1
```

#### 4. 监控 Thin Pool 水位

> [!warning] 关键监控
> Thin pool 写满后所有 thin LV 都会写入失败！必须持续监控。

```bash
# 查看池使用百分比
sudo lvs -o lv_name,lv_size,data_percent,metadata_percent ubuntu-vg

# 输出示例
#   LV              LSize   Data%  Meta%
#   thin_pool       200.00g 45.00  12.50
```

#### 5. 自动扩展配置

```bash
# 编辑 /etc/lvm/lvm.conf
thin_pool_autoextend_threshold = 80    # 使用率超 80% 自动扩展
thin_pool_autoextend_percent = 20      # 每次扩展 20%

# 启用监控服务
sudo systemctl enable --now lvm2-monitor.service
```

#### 6. 手动扩展 Thin Pool

```bash
# 先添加硬盘到 VG
sudo pvcreate /dev/sdc
sudo vgextend ubuntu-vg /dev/sdc

# 扩展 thin pool
sudo lvextend -L +100G ubuntu-vg/thin_pool
```

#### 7. Thin 快照（空间高效）

```bash
# 创建 thin 快照（无需指定大小）
sudo lvcreate -s -n vm1-snap ubuntu-vg/vm1-disk

# 挂载只读快照（需要 -K 激活）
sudo lvchange -ay -K /dev/ubuntu-vg/vm1-snap
sudo mount -o ro /dev/ubuntu-vg/vm1-snap /mnt/snap
```

> [!tip] 实践建议
> - 虚拟化环境（KVM/Proxmox）强烈推荐 thin provisioning
> - 对虚拟机磁盘启用 discard（TRIM）以回收空间
> - 超额比例建议控制在 3-5 倍以内
> - 元数据也会满！同时监控 `data_percent` 和 `metadata_percent`

---

### 场景六：pvmove 在线迁移数据

> [!summary] 场景
> 当某块硬盘故障前兆或需要更换时，在线将其上所有 PV 数据迁移到其他 PV，无需停机。

#### 1. 查看 PV 使用情况

```bash
# 查看各 PV 的物理区段分配
sudo pvs -o pv_name,pe_alloc,pe_free,pv_used
```

#### 2. 迁移整个 PV

```bash
# 将 /dev/sdb 上的数据全部迁移到 /dev/sdc
sudo pvmove /dev/sdb

# 期间数据正常读写，完成后 /dev/sdb 变为空闲
```

#### 3. 迁移指定物理区段（分块迁移，防止中断重来）

```bash
# 先查看区段映射
sudo pvdisplay -m /dev/sdb

# 分块迁移（推荐）
sudo pvmove /dev/sdb:0-10000
sudo pvmove /dev/sdb:10001-20000
sudo pvmove /dev/sdb:20001-...
```

#### 4. 迁移后从 VG 移除 PV

```bash
# 数据已全部迁出后
sudo vgreduce ubuntu-vg /dev/sdb

# 移除 LVM 标记
sudo pvremove /dev/sdb
# 现在可以安全地拔掉 /dev/sdb
```

> [!tip] pvmove 特点
> - **在线操作**：无需卸载、无需停机
> - **断点续传**：即使重启/内核 panic，恢复后继续迁移
> - **速度**：相比 dd，pvmove 能跟踪已迁移的区段，更安全
> - 大硬盘建议分块迁移，避免单次操作时间过长

---

### 场景七：LVM 条带化（Striping）提升性能

> [!summary] 原理
> 将数据分散写入多块物理磁盘，类似 RAID 0，提升 I/O 吞吐量。
> **适合场景**：大文件顺序读写、数据库数据卷、视频处理。

#### 创建条带化 LV

```bash
# 在 /dev/sdb 和 /dev/sdc 上创建条带 LV（条带数=2）
sudo lvcreate -L 100G -n striped-lv -i 2 ubuntu-vg /dev/sdb /dev/sdc
```

参数说明：
- `-i 2`：条带数（使用几块磁盘）
- `-I 64`：条带大小（默认 64KB，可选 4/8/16/32/64/128/256/512）

```bash
# 指定条带大小
sudo lvcreate -L 100G -n striped-lv -i 2 -I 128 ubuntu-vg /dev/sdb /dev/sdc
```

#### 查看条带信息

```bash
sudo lvs -o+stripes,stripesize,segtype
# 输出：
#   LV          Stripes  StripeSize  Type
#   striped-lv  2        128.00k     striped
```

#### 注意事项

> [!warning] 条带化限制
> - **没有冗余**：一块盘坏 = 整卷数据丢失
> - 条带数不能超过 PV 数量
> - 更多磁盘不等于线性性能提升（受总线/控制器限制）
> - 建议配合 LVM 镜像或 RAID 硬件使用
> - 扩展现有条带 LV 后新增空间不会条带化

---

### 场景八：LVM Cache 缓存加速

> [!tip] 场景
> 用 SSD 为 HDD 大容量卷做缓存加速，实现"大容量+高性能"兼备。

#### 一键创建（推荐）

```bash
# /dev/sde 是 HDD，/dev/sdf 是 SSD
sudo pvcreate /dev/sde /dev/sdf
sudo vgcreate cache_vg /dev/sde /dev/sdf

# 创建 HDD 大容量 LV 作为慢速源卷
sudo lvcreate -L 4G -n slow-lv cache_vg /dev/sde

# 用 SSD 创建缓存（--cache 自动完成所有步骤）
sudo lvcreate -L 2G --cache cache_vg/slow-lv /dev/sdf
```

#### 传统分步创建（理解原理）

```bash
# 1. 创建源卷（HDD）
sudo lvcreate -L 100G -n data-lv cache_vg /dev/sde

# 2. 创建缓存数据卷和元数据卷（SSD）
sudo lvcreate -L 20G -n cache-data cache_vg /dev/sdf
sudo lvcreate -L 100M -n cache-meta cache_vg /dev/sdf

# 3. 合并为 cache pool
sudo lvconvert --type cache-pool --poolmetadata cache_vg/cache-meta \
  cache_vg/cache-data

# 4. 将 cache pool 附加到源卷
sudo lvconvert --type cache --cachepool cache_vg/cache-data \
  cache_vg/data-lv

# 查看缓存状态
sudo lvs -o+cache_settings,cache_mode,cache_used_blocks,cache_dirty_blocks
```

#### 缓存模式选择

| 模式 | 写策略 | 数据安全 | 性能 |
|------|--------|---------|------|
| writethrough | 同时写 HDD + SSD | ✅ 安全 | 写略慢 |
| writeback | 先写 SSD 后刷 HDD | ⚠️ SSD 故障丢数据 | 🚀 写极快 |
| writearound | 绕过缓存直接写 HDD | ✅ 安全 | 读加速 |

```bash
# 切换到 writeback 模式（性能最佳）
sudo lvchange --cachemode writeback cache_vg/data-lv
```

> [!tip] 实践建议
> - SSD 大小通常是 HDD 的 10-20%
> - 元数据卷大小约为数据卷的 1/1000
> - 热点数据密集的场景（数据库、频繁访问的文件）效果最明显
> - writeback 模式显著提升写入性能，但 SSD 故障会丢数据

---

## 维护与管理 🔧

### LV 重命名

```bash
# 卸载后重命名
sudo umount /data
sudo lvrename /dev/ubuntu-vg/data-lv data-new

# 或使用 VG/LV 名
sudo lvrename ubuntu-vg data-lv data-new

# 重挂载
sudo mount /dev/ubuntu-vg/data-new /data
# 记得更新 /etc/fstab
```

### VG/LV 激活与停用

```bash
# 停用 VG（所有 LV 不可用）
sudo vgchange -a n ubuntu-vg

# 激活 VG
sudo vgchange -a y ubuntu-vg

# 激活单个 LV
sudo lvchange -a y /dev/ubuntu-vg/data-lv

# 跳过激活标志（thin LV 快照等被标记跳过激活时）
sudo lvchange -a y -K /dev/ubuntu-vg/thin-snap
```

> [!tip] 应用场景
> - **迁移**：将硬盘移到另一台机器前停用 VG，移过去后激活
> - **维护**：单独停用某个 VG 不影响其他 VG
> - **故障恢复**：vgchange -ay 扫描激活所有可用 VG

### 查看高级信息

```bash
# 自定义输出字段（pvs/vgs/lvs 通用）
sudo pvs -o pv_name,pv_size,pv_used,pv_free,pv_allocatable

# VG 详情
sudo vgs -o vg_name,vg_size,vg_free,vg_extent_size,vg_extent_count

# LV 详情（含条带、缓存、池信息）
sudo lvs -o lv_name,lv_size,lv_layout,lv_role,segtype,stripes,stripesize

# 查看磁盘 PE 分配映射
sudo pvdisplay -m /dev/sdb

# 查看 VG 中所有 LV 的完整路径
sudo lvs -o lv_full_name,vg_name,lv_path

# 可用字段列表
sudo pvs -o help      # PV 可用字段
sudo vgs -o help      # VG 可用字段
sudo lvs -o help      # LV 可用字段
```

### 删除 LVM 组件的完整流程

```bash
# 正确顺序：LV → VG → PV（与创建相反）

# 1. 卸载和删除 LV
sudo umount /dev/ubuntu-vg/data-lv
sudo lvremove /dev/ubuntu-vg/data-lv

# 2. 从 VG 移除 PV
sudo pvmove /dev/sdb1           # 迁移数据
sudo vgreduce ubuntu-vg /dev/sdb1

# 3. 删除 PV 标签
sudo pvremove /dev/sdb1
```

## 故障排查 🔍

### 问题一：系统启动后 LVM 卷未激活

```bash
# 现象：/dev/mapper/ 下没有 LV，系统无法挂载
# 原因：lvm2 服务未运行或 VG 未自动激活

# 解决方法
sudo vgchange -a y        # 激活所有 VG
# 或
sudo vgchange -a y ubuntu-vg  # 激活指定 VG
```

### 问题二：LVM 元数据损坏

```bash
# 现象：vgs 报错 "Volume group not found"
# 预防：定期备份元数据

sudo vgcfgbackup       # 默认备份到 /etc/lvm/backup/

# 恢复元数据（谨慎操作）
sudo vgcfgrestore -f /etc/lvm/backup/ubuntu-vg ubuntu-vg
```

### 问题三：PV 设备被 LVM 识别不到

```bash
# 现象：pvs 不显示新加的硬盘
# 检查设备是否被 LVM 过滤

# 查看当前过滤器设置
sudo lvmconfig --type current | grep filter

# 检查 lvm.conf 中的 filter
sudo grep filter /etc/lvm/lvm.conf

# 临时手动扫描
sudo pvscan --cache

# 示例过滤器（在 /etc/lvm/lvm.conf 中）
# filter = [ "a|/dev/sd.*|", "r|/dev/ram.*|" ]
# a = accept, r = reject
```

### 问题四：Thin Pool 空间不足

```bash
# 现象：写入 thin LV 时报 "No space left" 或 dmesg 有 pool 相关错误
# 紧急处理

# 1. 检查池使用率
sudo lvs -o data_percent,metadata_percent ubuntu-vg/thin_pool

# 2. 立即扩展
sudo lvextend -L +50G ubuntu-vg/thin_pool

# 3. 如果元数据也满了
sudo lvextend --poolmetadataspare y -L +1G ubuntu-vg/thin_pool
```

### 问题五：误缩小了 xfs 文件系统

```bash
# 现象：xfs 缩容后无法挂载
# xfs 不支持缩容！如果已经操作了：

# 检查是否能恢复（只能通过备份还原）
# 预防方案：
# - 操作前确认文件系统类型
sudo df -T /data
# - xfs 只能用 xfs_growfs 扩容，不能缩
```

### 问题六：移除 PV 时数据迁不走

```bash
# 现象：pvmove 卡住或报错
# 可能原因：目标 PV 空间不够

# 1. 检查目标 PV 的可用区段
sudo pvs -o pv_name,pv_used,pv_pe_count,pv_pe_alloc

# 2. 添加更多 PV 或释放空间
sudo vgextend ubuntu-vg /dev/sdd   # 加新盘

# 3. 重新执行迁移
sudo pvmove /dev/sdb

# 4. 检查迁移进度
sudo pvmove -i 5 /dev/sdb  # 每5秒显示一次进度
```

## 注意事项 ⚠️

### 常见错误

**忘记扩展文件系统**：
```bash
# LV 扩展了，但文件系统没扩展
sudo lvextend -L +100G /dev/ubuntu-vg/ubuntu-lv
# 忘记运行 resize2fs

# 解决方法
sudo resize2fs /dev/ubuntu-vg/ubuntu-lv
```

**缩小 LV 顺序错误**：
```bash
# ❌ 错误：先缩小 LV，再缩小文件系统
sudo lvreduce -L 30G /dev/ubuntu-vg/data-lv
sudo resize2fs /dev/ubuntu-vg/data-lv 30G  # 数据丢失！

# ✅ 正确：先缩小文件系统，再缩小 LV
sudo resize2fs /dev/ubuntu-vg/data-lv 30G
sudo lvreduce -L 30G /dev/ubuntu-vg/data-lv
```

**xfs 文件系统尝试缩小**：
```bash
# xfs 不支持缩小
sudo xfs_growfs /  # 只能扩容
```

### 关键配置点

**文件系统限制**：
| 文件系统 | 支持扩容 | 支持缩容 | 备注 |
|----------|---------|---------|------|
| ext4 | ✅ | ✅ | 推荐 |
| xfs | ✅ | ❌ | 只能扩容 |
| btrfs | ✅ | ✅ | 高级功能 |

**引导限制**：
- **BIOS 系统**：/boot 分区不能在 LVM 上
- **UEFI 系统**：ESP 必须是 FAT32 分区

**性能考虑**：
- LVM 增加一层抽象，性能略有损耗（通常可忽略）
- 服务器推荐使用 LVM，桌面系统可选

## 常用命令速查

### 查看命令
| 命令 | 作用 |
|------|------|
| `pvs` / `pvdisplay` | 查看所有物理卷 |
| `vgs` / `vgdisplay` | 查看所有卷组 |
| `lvs` / `lvdisplay` | 查看所有逻辑卷 |
| `lsblk` | 查看整体磁盘结构 |

### 管理命令
| 命令 | 作用 |
|------|------|
| `pvcreate /dev/sdb1` | 创建物理卷 |
| `vgcreate myvg /dev/sdb1` | 创建卷组 |
| `vgextend myvg /dev/sdb2` | 扩展卷组（添加 PV）|
| `lvcreate -L 50G -n mylv myvg` | 创建逻辑卷 |
| `lvextend -L +100G /dev/myvg/mylv` | 扩展逻辑卷 |
| `lvreduce -L 50G /dev/myvg/mylv` | 缩小逻辑卷 |
| `lvremove /dev/myvg/mylv` | 删除逻辑卷 |

### 文件系统命令
| 命令 | 作用 |
|------|------|
| `resize2fs /dev/vg/lv` | 扩展/缩小 ext4 |
| `xfs_growfs /` | 扩展 xfs（只能扩）|
| `mkfs.ext4 /dev/vg/lv` | 格式化为 ext4 |

## 常见问题 ❓

**Q: 如何查看 VG 中还有多少剩余空间？**

A: 使用 `vgs` 命令查看 `VFree` 列：
```bash
sudo vgs
# 输出：
# VG        #PV #LV #SN Attr   VSize   VFree
# ubuntu-vg   2   2   0 wz--n- 398.00g 200.00g
```

**Q: LVM 和传统分区有什么区别？**

A: 主要区别：
| 对比项 | 传统分区 | LVM |
|--------|----------|-----|
| 扩容 | 需要停机 | 在线操作 |
| 调整大小 | 受限制 | 灵活 |
| 多磁盘 | 需要挂载到不同目录 | 可合并成一个 VG |
| 快照 | 不支持 | 支持 |

**Q: 如何删除 LVM 组件？**

A: 删除顺序与创建顺序相反：`LV → VG → PV`
```bash
# 删除 LV
sudo lvremove /dev/ubuntu-vg/data-lv

# 从 VG 中移除 PV（需要先迁移数据）
sudo pvmove /dev/sdb1
sudo vgreduce ubuntu-vg /dev/sdb1

# 删除 PV
sudo pvremove /dev/sdb1
```

**Q: 如何备份 LVM 元数据？**

A: 使用 `vgcfgbackup` 命令：
```bash
# 备份 VG 元数据
sudo vgcfgbackup -f /backup/vg-backup.conf ubuntu-vg

# 恢复元数据（谨慎使用）
sudo vgcfgrestore -f /backup/vg-backup.conf ubuntu-vg
```

**Q: LVM 可以加密吗？**

A: 可以，使用 LUKS 加密：
```bash
# 创建加密 PV
sudo cryptsetup luksFormat /dev/sdb
sudo cryptsetup open /dev/sdb crypt_sdb
sudo pvcreate /dev/mapper/crypt_sdb
```

## 相关文档
- [[linux MOC]] - Linux 学习笔记索引
- [[linux磁盘相关的知识]] | [[cpu的线程和内核]]

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-07-28 | 新增场景五~八（Thin Provisioning、pvmove 迁移、条带化、LVM Cache）|
| 2026-07-28 | 新增维护与管理（重命名、激活/停用、高级查看、完整删除流程）|
| 2026-07-28 | 新增故障排查六种常见问题 |
| 2026-07-28 | 补充 frontmatter（created/updated）|
| 初始 | 基础 LVM 操作（扩容、新建 LV、快照、缩容）|
