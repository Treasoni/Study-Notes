---
tags: [linux]
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
