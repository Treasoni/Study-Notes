# 1. 创建虚拟机，本质在做哪些事？

先给你一句**总纲**：

> **创建虚拟机 = 给一台“假电脑”分配硬件资源 + 接好网络 + 准备装系统**

这台“假电脑”会有：

|真实电脑|虚拟机|
|---|---|
|主板|虚拟主板|
|CPU|vCPU|
|内存|虚拟内存|
|硬盘|虚拟磁盘|
|网卡|虚拟网卡|
|U 盘 / 光驱|ISO|
# 2. PVE 中「创建虚拟机」完整流程
## 2.1  常规配置
![](assets/如何创建PVE虚拟机/截屏2026-01-31%2013.39.50.png)
这里我们一般是配置这里的==**VM ID**==和==**名称**==
![](assets/如何创建PVE虚拟机/截屏2026-01-31%2013.43.29.png)
## 2.2 OS（操作系统）

 **核心问题：**

👉 **这台虚拟机是“怎么启动的”？**

### 2.2.1 常见选择

**✔ Use CD/DVD disc image file (iso)**

>- 用 ISO 装系统（Linux / Windows）

**✔ Do not use any media**

>- iStoreOS / OpenWRT 常用
>- 稍后手动导入磁盘

### 2.2.2 ISO 文件从哪来？

👉 **PVE 的存储库（local）里**
`Datacenter → Storage → local → ISO Images`
## 2.3 System（系统）

这里是**很多人第一次会懵的地方**，但你现在能懂。
### 🔹 BIOS

|选项|建议|
|---|---|
|SeaBIOS|老系统 / 简单|
|OVMF (UEFI)|**现代系统推荐**|

👉 **Linux / Windows 10+ / iStoreOS → UEFI**

---

### 🔹 Machine

- `q35`（新）
    
- `i440fx`（老）
    

👉 **选 q35**

---

### 🔹 EFI Disk（如果用 UEFI）

⚠️ **必须加！**

- 这是 UEFI 的“启动配置盘”
    
- 不是真正的系统盘
    

---

### 🔹 SCSI Controller

👉 **VirtIO SCSI**

性能最好，CPU 占用低。

---