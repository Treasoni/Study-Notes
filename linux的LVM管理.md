
#linux 
# 1. Linux服务器的磁盘
我们在进行linux服务器搭建的时候，我们的硬盘经常是这样的情况：

```text
硬盘 sda        200G
├─ sda2         2G        → /boot
└─ sda3         198G      → LVM 物理卷（PV）
    └─ ubuntu-vg
        └─ ubuntu-lv     99G → /
```
关键点在这里 👇
>- sda3：198G
>- / 实际用的 ubuntu-lv：99G

👉 中间差的 ~99G：
>- 已经在 Volume Group（VG）里
>- 但 没有分配给 Logical Volume（LV）

## 1.1 为什么会这样？（不是你装错）

这是 **Ubuntu 安装器的“保守默认行为”**：

- 使用 LVM
- **只给 `/` 分一半空间**
- 留一半：
    - 方便以后加 `/home`
    - 或快照
    - 或扩容
👉 服务器上这是**好习惯**，但你现在想全用，那就扩。
# 2. 理论讲解