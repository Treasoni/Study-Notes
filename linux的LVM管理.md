
#linux 
我们在进行lin

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

