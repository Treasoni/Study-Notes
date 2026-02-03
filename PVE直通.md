---
tags:
  - pve
---
# 1. Intel x86 CPU（VT-d）完整直通流程（推荐版）

**✅ 适用场景**

>- Intel 桌面 / 笔记本 / 小主机 / NUC
>- 直通：**核显 / 独显 / 网卡 / HBA / USB 控制器**

## 1.1. Step 1：BIOS 设置（硬件层）

**必开选项（名字可能略有不同）**
具体操作看[3.进入BIOS系统](PVE的学习/安装和使用PVE.md#3.进入BIOS系统)

|选项|必须|说明|
|---|---|---|
|Intel VT-x|✅|虚拟机基础|
|**Intel VT-d**|✅|IOMMU（直通核心）|
|Above 4G Decoding|✅|显卡 / 大 BAR|
|SR-IOV|可选|网卡虚拟化|
|CSM|❌|关闭，UEFI|

📌 **说明**  
BIOS 这里只是说一句话：

> “我这个硬件，允许你（操作系统）玩直通”

⚠️ **此时 PVE 还不能直通**

# 1.2 Step 2：PVE 启用 IOMMU（系统层，关键）

### 1.2.1 修改 GRUB

```bash
nano /etc/default/grub
```

找到这一行：

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
```

改成（推荐通用稳定版）：

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt pcie_acs_override=downstream,multifunction initcall_blacklist=sysfb_init"
```

### 1.2.2 参数解释（不是废话，是真正会用到的）

|参数|作用|
|---|---|
|intel_iommu=on|真正启用 VT-d|
|iommu=pt|非直通设备走直通模式，性能更好|
|pcie_acs_override=downstream,multifunction|强制拆 IOMMU 组|
|initcall_blacklist=sysfb_init|防止宿主机抢核显|


## 1.3 Step 3：更新并重启
```bash
update-grub
reboot
```


## 1.4 Step 4：验证 IOMMU 是否生效

```bash
dmesg | grep -e DMAR -e IOMMU
```

看到类似：

`DMAR: IOMMU enabled`

👉 **这一行没看到 = 前面白做**


## 1.5 Step 5：确认 IOMMU 分组情况

```bash
for d in /sys/kernel/iommu_groups/*/devices/*; do
  echo "IOMMU Group ${d#*/iommu_groups/*}: $(lspci -nns ${d##*/})"
done
```

📌 **理想状态**

- 显卡
- 显卡音频
- USB 控制器  
    👉 **各在一个组**
详细讲解看[IOMMU分组情况](IOMMU分组情况.md)
---

## Step 6：绑定 vfio 驱动（防止宿主机占用）

`nano /etc/modprobe.d/vfio.conf`

写入（示例）：

`options vfio-pci ids=10de:1c82,10de:0fb9`

> `10de:xxxx` 来自 `lspci -nn`

然后：

`update-initramfs -u reboot`

---

## Step 7：PVE Web 里添加 PCI 设备

- VM → Hardware → Add → PCI Device
    
- 勾选：
    
    - ✅ All Functions
        
    - ✅ PCI-Express
        
    - ✅ ROM-Bar（部分显卡）
        

---

### ✅ Intel 直通总结一句话

> **BIOS 是“许可”，GRUB 是“执行”，vfio 是“接管”**

---