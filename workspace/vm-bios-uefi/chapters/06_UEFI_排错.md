# 第六章：UEFI 排错 —— 症状、根因、处置

这一章解决的是最初那个痛点：「使用 UEFI 时总是出问题」。做法不是罗列一堆可能原因，而是把每条已知故障压成同一张表的三列 —— **症状 → 根因 → 处置** —— 让你从看到的现象倒推到该敲哪条命令。

> **本章的覆盖方式**：用户实际遇到的报错原文/截图尚未提供，本章按**通用原理**覆盖。等你把真实报错（原文或截图）发过来，会回读本表并**按真实报错重写对应行**，而不是另起一章。

读之前先把三类信息的分辨方法定下来，本章每一格都按这个标准标注：

| 标注 | 含义 | 你该怎么用 |
| --- | --- | --- |
| **官方口径** | 来源有明确原文支持 | 可以直接照做 |
| **推理** | 本章或素材的归纳，来源无明文 | 可以当方向，动手前自行确认 |
| **缺口** | 来源未覆盖 | 不要当作已解决，也不要拿别处的说法补齐 |

---

## 6.1 症状总表

| # | 症状 | 根因（来源） | 处置（来源） | 详见 |
| --- | --- | --- | --- | --- |
| 1 | 把固件从 BIOS 切到 EFI 后虚拟机无法启动 | 官方定性为**预期行为**：BIOS 用 MBR 分区、EFI 需要 GPT 分区，切换**不会**转换分区表 [^c6-L3-1] | ① 重建 VM、选定固件后挂原有硬盘；② 切 EFI **之前**先把磁盘转 GPT [^c6-L3-1] | 6.2 |
| 2 | 启动后停在 EFI Shell / 没有引导项 | EFIVARS 里没有 boot entry，回退加载 `$ESP/EFI/BOOT/BOOTX64.efi` 也失败 [^c6-L2-3] | 进 OVMF 菜单 → Boot Maintenance Manager → Boot Options → Add Boot Option [^c6-L2-3] | 6.3 |
| 3 | 找不到 UEFI 引导加载程序（启动诊断报 `The boot loader did not load an operating system`） | EFI 系统分区（ESP）被删除或缺失 [^c6-L3-3] | 用 `gdisk` 以类型码 `ef00` 在正确扇区重建 ESP [^c6-L3-3] | 6.4 |
| 4 | UEFI 启动分区损坏（报 `The UEFI boot partition is corrupted`） | ESP 文件系统损坏 [^c6-L3-3] | `fsck.vfat` 清理修复 [^c6-L3-3] | 6.5 |
| 5 | `/boot` 分区内容被删除且无法恢复 | 引导所需内容整体丢失 [^c6-L3-3] | 官方原文：**从备份恢复虚拟机是唯一选项** [^c6-L3-3] | 6.6 |
| 6 | Secure Boot 拦下引导程序或 UEFI 驱动 | Secure Boot 只放行 UEFI 数据库中受信签名的引导加载程序与 option ROM [^c6-GEN12][^c6-GEN2SEC] | 为对象正确签名，或在设置/VM 内关闭 Secure Boot [^c6-GEN12][^c6-GEN2SEC][^c6-L1-1] | 6.7 |
| 7 | VirtualBox：无引导介质时看不到 EFI Shell，安装无法进行 | 当时 EFI 固件缺 VMSVGA/VBoxSVGA 图形驱动（2019 年缺陷，6.0.5 已修复）[^c6-L3-5] | 升级到 6.0.5 及以上；老版本避开该组合 [^c6-L3-5] | 6.8 |
| 8 | PVE：UEFI 虚拟机启动异常 / 疑似缺 `efidisk0` | 官方参考手册只说明「用 OVMF 需要 EFI Disk 保存 boot order」，**未描述缺失 efidisk0 的失败现象** [^c6-L2-1] | 按第 2 行处置；**本格属未闭合缺口** [^c6-L2-1][^c6-L2-3] | 6.9 |

### 关于「先确认当前固件」这一步

排错常从「这台机器现在用的到底是哪种固件」开始。**本轮素材没有提供任何读取该设置的命令**，所以本章不写，也不要用记忆里的 `showvminfo` 一类命令顶替。

素材里**确有来源**的可见性判断只有两条，都是「看现象」而不是「查配置」：

- 虚拟机启动时**能看到 OVMF 菜单**（splash 画面出现时按一次 ESC 能进去）→ 说明用的是 OVMF/UEFI 固件 [^c6-L2-3]；
- 虚拟机启动后**直接落进 EFI Shell** → 说明走的是 UEFI 固件，并且引导已经失败到最后一层（回退路径也没成功）[^c6-L2-3]。

其余确认手段属**缺口**，需要你到各平台的设置界面自行查看。

---

## 6.2 症状 1：切了固件就起不来 —— 固件与分区表是绑定的

这是所有 UEFI 故障里最根本的一条，也是唯一一条官方直接定性为「不是 bug」的。

VMware 知识库文章（Article ID 384912，适用环境为 vSphere ESXi 7.x/8.x 与 vCenter 7.x/8.x）的记录是：把固件从 BIOS 改成 EFI（或反向）后，虚拟机将无法启动，控制台会显示错误信息；**根因**被明确定性为预期行为 ——

> `"This is an expected behavior as changing the firmware is not supported since BIOS uses MBR (Master Boot Record) partitioning and EFI requires GPT (GUID Partition Table) partitioning on the VM disks."` [^c6-L3-1]

同一段还写明：改固件时界面**会显示警告**，提示已安装的客户机操作系统可能变得无法启动 [^c6-L3-1]。也就是说这不是「你没看到提示」，而是「提示出现过，但你点了继续」。

**官方给出两条处置** [^c6-L3-1]：

1. **重建 VM**：选择 EFI 或 BIOS 作为固件，把**同一批硬盘**挂到新虚拟机上，让它能启动；
2. **在切换到 EFI 之前先把虚拟机的磁盘转成 GPT**：官方指出这可以用 **`mbr2gpt.exe`**（Windows 下）之类的工具完成，**并且需要客户机操作系统厂商的支持**。

> **推理（跨平台适用性）**：这篇 KB 是 VMware 侧文章，「改固件不受支持」这句官方定性的适用范围也限于其环境。但其中「BIOS 用 MBR、EFI 需要 GPT」是**分区表层面的机制**，不依赖具体 hypervisor —— 把它作为其他平台同类现象的解释方向是本章的归纳，请作为方向使用，不要当成其他平台的官方结论。

> **缺口**：该 KB 页面里「虚拟机将在控制台显示以下错误信息」后面应当有一段报错原文，但本轮缓存中**该处为空**。我不代填报错文字，等你的真实报错来补。

---

## 6.3 症状 2：停在 EFI Shell 或根本没有引导项

**根因（官方 wiki 层级）**：如果虚拟机走 OVMF（UEFI）启动，固件必须知道它要从 ESP 启动哪个 bootloader；当 **EFIVARS 存储里不存在任何 boot entry** 时，它会尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`；**如果这一步也失败，虚拟机就会被引导进入 EFI Shell** [^c6-L2-3]。

**处置**：进 OVMF 菜单手工把引导项补上 —— splash 画面出现时**恰好按一次 ESC**（当前版本还需选 `EFI Firmware Setup` 条目），然后 `Boot Maintenance Manager` → `Boot Options` → `Add Boot Option` → 选择带 EFI System Partition 的磁盘 → 导航到 EFI 可执行文件（Debian 示例 `EFI/debian/grubx64.efi`，Fedora 示例 `EFI/fedora/shimx64-fedora.efi`）→ 命名并 `Commit Change` → 用 `Change Boot Order` 把它挪到最前 [^c6-L2-3]。

完整步骤与截图式路径见第 5.8 节。

> [!tip] 大白话
> 停在 EFI Shell 就像是门卫找不到名单上该敲的门，最后只能站在大厅等你吩咐。EFI Shell 本身不是错误界面，它是「固件还活着、但不知道下一步干什么」的状态 —— 所以处置也简单：把名单（boot entry）补上，而不是重装系统。

---

## 6.4 症状 3：找不到 UEFI 引导加载程序

**症状原文**（Azure 第 2 代 Linux 虚拟机的启动诊断截图里）[^c6-L3-3]：

```
Virtual Machine Boot Summary
    1. Unknown Device The boot loader did not load an operating system.
    2. SCSI Disk (0,0) The boot loader did not load an operating system.
    3. SCSI Disk (0,1) The boot loader did not load an operating system.
    4. Network Adapter (000D3A4DD64D) A boot image was not found.
No operating system was loaded. Your virtual machine may be configured incorrectly.
```

**根因（官方原文）**：`"If the EFI System Partition (ESP) has been deleted or is missing, the VM cannot locate the UEFI boot loader and startup will fail."` [^c6-L3-3]

**处置**：把目标磁盘挂到一台修复机上，用 `gdisk` 重建 EFI 分区。关键动作是**把分区类型改成 `ef00`**，扇区起止必须正确。下面是该文档给出的操作片段（逐字引用）[^c6-L3-3]：

```
Command (? for help): n
Partition number (3-128, default 3):
First sector (34-134217694, default = 10240) or {+-}size{KMGTP}: 10240
Last sector (10240-1026047, default = 1026047) or {+-}size{KMGTP}: 1026047
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): ef00
Changed type of partition to 'EFI System'
```

重建后 `p` 打印出的分区表长这样 [^c6-L3-3]：

```
Number  Start (sector)    End (sector)  Size       Code  Name
   1         1026048         3123199   1024.0 MiB  0700
   2         3123200       134215679   62.5 GiB    8E00
   3           10240         1026047   496.0 MiB   EF00  EFI System
  14            2048           10239   4.0 MiB     EF02
```

文档对这一段给了三条操作提醒 [^c6-L3-3]：

- `/dev/sdc` 要换成**对应的系统盘设备**；
- 分区编号本身无所谓，**只要扇区的起止点正确** —— 文档的说法是「正确的起止扇区之所以能选出来，是因为操作系统有能力判断出缺失的扇区」；
- 结尾扇区**不能**与其他分区重叠，用默认值即可。

**适用边界（缺口提醒）**：这份文档针对的是 **Azure 上的第 2 代 Linux 虚拟机**，它的分区表里还有编号 1、2、14 等 Azure 特有布局（例如 `EF02` 的 BIOS boot 分区）。把 `gdisk` 重建 ESP 这个手法搬到本地 PVE / VMware 的虚拟机上是**推理**，扇区参数必须按你自己的磁盘实际情况取值，不要照抄本文档的数字。

---

## 6.5 症状 4：UEFI 启动分区损坏

**症状原文**：`"The UEFI boot partition is corrupted"` [^c6-L3-3]

**根因（官方原文）**：`"If the UEFI boot partition is corrupted, the generation 2 Linux VM will fail to boot."` —— 即 ESP 的文件系统损坏 [^c6-L3-3]。

**处置**：用 `fsck.vfat` 清理。文档先给出**干跑**（`-n`）再看结果的做法，片段逐字引用 [^c6-L3-3]：

```
root@repair-centos7:~# fsck.vfat -n /dev/sdc3
fsck.fat 4.1 (2017-01-24)
0x25: Dirty bit is set. Fs was not properly unmounted and some data may be corrupt.
 Automatically removing dirty bit.
Leaving filesystem unchanged.
/dev/sdc3: 19 files, 1438/63326 clusters
```

确认无误后再执行修复（交互式确认，`1` 表示移除 dirty bit，最后再跑一次确认已干净）[^c6-L3-3]：

```
root@repair-centos7:~# fsck.vfat /dev/sdc3
0x25: Dirty bit is set. Fs was not properly unmounted and some data may be corrupt.
1) Remove dirty bit
2) No action
? 1
Perform changes ? (y/n) y
/dev/sdc3: 19 files, 1438/63326 clusters
root@repair-centos7:~# fsck.vfat /dev/sdc3
fsck.fat 4.1 (2017-01-24)
/dev/sdc3: 19 files, 1438/63326 clusters
```

文档的硬性前置提醒 [^c6-L3-3]：

- **务必先给系统盘做备份**，并且**在执行文件系统检查前先用 `-n` 干跑一次**；
- `dosfsck` 与 `fsck.vfat` 是同一个工具，两个名字都可用。

> [!tip] 大白话
> ESP 是块小容量的 FAT 分区，`fsck.vfat` 就是它的「磁盘检修」。注意手法和普通检修一样：先拆下来看（挂到修复机上）、先空转一遍（`-n`）确认会修什么，再动手 —— 直接在上面下刀，修坏了就只能走 6.6 那条路了。

---

## 6.6 症状 5：`/boot` 内容被删除且无法恢复

**根因**：引导所需内容整体丢失 [^c6-L3-3]。

**处置**：官方原文很直接 —— `"restoring the VM from a backup is the only option"`（**从备份恢复虚拟机是唯一选项**）[^c6-L3-3]。

这一格请记住它的意义：它划出了「能救」与「只能回滚」的分界线。前面几格都还能靠 `gdisk`、`fsck.vfat`、加引导项救回来，只有内容整体没了这一格没有技术手段。

---

## 6.7 症状 6：Secure Boot 把引导程序或驱动拦下来了

**机制（两处官方表述，合起来构成完整图景）**：

- Secure Boot「验证引导加载程序是由 **UEFI 数据库中的受信机构**签名的」—— 原文 `"Secure Boot verifies the boot loader is signed by a trusted authority in the UEFI database."` [^c6-GEN12]
- 它的作用范围还包括 UEFI 驱动：「帮助阻止未授权的固件、操作系统或 **UEFI 驱动（也就是 option ROM）** 在启动时运行」，并且 `"Secure Boot is enabled by default."` [^c6-GEN2SEC]
- VMware 侧对同一机制的表述是：UEFI Secure Boot「通过阻止加载**未以可接受数字签名签名**的驱动与操作系统加载器来保护启动过程」[^c6-L1-1]

**处置**：两条路 —— 为对象正确签名，或者在虚拟机设置里关闭 Secure Boot。官方原文写的是：`"If these applications aren't digitally signed correctly, you must disable Secure Boot for the virtual machine."` [^c6-GEN12]

**⚠️ 一个必须知道的例外**：VMware 侧，**如果启用了 VBS（virtualization-based security）**，固件类型会被设为 UEFI 并且勾选 Secure Boot，同时官方明确 —— `"You cannot edit the firmware type or the UEFI Secure Boot setting when VBS is enabled."` [^c6-L1-1]

也就是说：VBS 场景下**「关闭 Secure Boot」这条路被堵死了**，界面上那两项根本不可编辑。这时能动的只有「为对象签名」这一条，或者先处理 VBS（这已超出本章素材范围）。

> [!tip] 大白话
> Secure Boot 像一份只有白名单的放行规定：名单在 UEFI 数据库里，不在名单上的引导程序和驱动一律不许进。你遇到拦截时有两个选择 —— 把要进的东西登记进名单（签名），或者跟门卫说今天不看名单（关掉 Secure Boot）。但 VMware 开了 VBS 的那台机器上，第二个选择被厂商直接锁掉了，你只能走签名这条路。

---

## 6.8 症状 7：VirtualBox 里看不到 EFI Shell

**现象**：图形控制器不是 VBoxVGA、且没有提供可引导介质时，EFI Shell 始终不出现，安装无法进行；报告者补充实际是「完全不启动」（`"No booting, no go"`），并且 `EfiGopMode`、`EfiGraphicsResolution` 等 ExtraData 全部被忽略 [^c6-L3-5]。

**根因**：当时 EFI 固件里**没有**处理 VMSVGA / VBoxSVGA 的图形驱动（开发者原文 `"no graphics driver in the EFI firmware"`）[^c6-L3-5]。

**处置与时间线（务必连读）**：这是 **2019 年**的社区 ticket（community 层级），报告者已用 `r128870`（对应 **6.0.5**）确认修复，ticket 于 2019-04-17 关闭为 `fixed` [^c6-L3-5]。

**所以这一格的正确读法是**：它不是当前版本的问题，而是「黑屏且无报错」这类现象的一个历史实例 —— 根因在**图形路径**而不是引导路径。完整时间线与规避建议见第 4.4 节，那里同样按「带版本」的纪律写。

---

## 6.9 症状 8：PVE 的 UEFI 启动异常 —— 未闭合缺口

这一格必须明确标为**缺口**，不要写成已解决的结论：

- 官方参考手册对 OVMF 的说明只到「为了保存 boot order 这类信息，**需要**有一块 EFI Disk」这一步 [^c6-L2-1]；
- 官方参考手册**没有描述**「缺少 `efidisk0` 时会出现什么失败现象、该怎么修」；
- 官方 wiki 那边只有 6.3 节那条引导链路（boot entry → 回退路径 → EFI Shell），它讲的是**引导项缺失**，不是**缺 EFI 磁盘** [^c6-L2-3]。

**目前的处置只能是**：先按 6.3 的 EFI Shell / 无引导项那条路径查；同时确认这台用 OVMF 的虚拟机确实配了 `efidisk0`（创建命令与选项语义见第 5.2、5.4 节）。

**这是缺口而非结论** —— 记成「官方未描述该失败与修复」即可，不要写成「缺 efidisk0 会导致某某报错」。

---

## 6.10 迁移路径：把一台 Legacy 虚拟机改成 UEFI 启动

如果你不想重建虚拟机，而是想把现有磁盘改成能被 UEFI 启动，有两条路。

### 路径 A：先在客户机内转 GPT，再改固件为 UEFI

VMware 官方给的方向是「切 EFI **之前**先把磁盘转成 GPT」，工具举例为 `mbr2gpt.exe`，且**需要客户机操作系统厂商支持** [^c6-L3-1]。微软对 `MBR2GPT.EXE` 的官方说明里有几条硬约束，逐条列在这里：

| 约束 | 原文 |
| --- | --- |
| 位置 | `MBR2GPT.EXE` 位于任何运行受支持 Windows 版本的设备的 `Windows\System32` 目录下 [^c6-MBR2GPT] |
| 做什么 | 「把磁盘从 MBR 转换为 GPT 分区样式，**不修改也不删除磁盘上的数据**」；可从 Windows PE 命令提示符运行，加上 `/allowFullOS` 也可在完整 Windows 中运行 [^c6-MBR2GPT] |
| **不能转非系统盘** | `"The tool can't be used to convert non-system disks from MBR to GPT."` [^c6-MBR2GPT] |
| **主分区上限** | 校验项包括 `"There are at most three primary partitions in the MBR partition table"`；此外磁盘不得有扩展/逻辑分区 [^c6-MBR2GPT] |
| **转换后必须改固件** | `"After the disk has been converted to GPT partition style, the firmware must be reconfigured to boot in UEFI mode."` 并且「尝试转换前请确认设备支持 UEFI」[^c6-MBR2GPT] |
| **旧系统离线转换不受支持** | 「对装有 Windows 7、8 或 8.1 等更早版本 Windows 的系统盘进行离线转换**不受官方支持**」；官方推荐做法是先把操作系统升级到受支持版本，再做转换 [^c6-MBR2GPT] |
| BitLocker | 只要保护处于挂起状态，就可以转换带 BitLocker 加密卷的 MBR 磁盘；转换后要恢复 BitLocker，需删除并重建现有保护器 [^c6-MBR2GPT] |

命令与输出（官方示例，逐字引用）[^c6-MBR2GPT]：

```
X:\> mbr2gpt.exe /validate /disk:0
MBR2GPT: Attempting to validate disk 0
MBR2GPT: Retrieving layout of disk
MBR2GPT: Validating layout, disk sector size is: 512
MBR2GPT: Validation completed successfully
```

完整语法是 `MBR2GPT /validate|convert [/disk:<diskNumber>] [/logs:<logDirectory>] [/map:<source>=<destination>] [/allowFullOS]` [^c6-MBR2GPT]。实操建议是先 `/validate` 再 `/convert` —— 官方说明里也写明：校验不通过时**转换不会进行**，会返回错误 [^c6-MBR2GPT]。

关于 `/allowFullOS` 有一条容易被忽略的后果：默认情况下 `MBR2GPT.exe` **只能从 Windows PE 运行**，在完整 Windows 中会被阻止；该选项解除这一阻止，但**由于在完整 Windows 下运行时现有的 MBR 系统分区正在被使用、无法复用，工具会通过缩小 OS 分区来新建一个 EFI 系统分区** [^c6-MBR2GPT]。

### 路径 B：保留磁盘，新建一台 UEFI 虚拟机把盘挂过去

这是 VMware 官方给的第一条处置：**重建 VM、选定固件后再把同一批硬盘挂上去** [^c6-L3-1]。它的好处是不需要在客户机里做转换，代价是要重建虚拟机配置。

### ⚠️ 引用 MBR2GPT 页时必须带的一句边界

`MBR2GPT` 这一页**全文不含** `virtual machine`、`Hyper-V`、`vSphere` 字样 —— 也就是说它讲的是**物理设备**的转换，**虚拟机场景的专属约束不在这一页**，而由 `L3-1` 给出（先转 GPT 再切 EFI，且需客户机系统厂商支持）[^c6-MBR2GPT][^c6-L3-1]。

> **推理**：把 `mbr2gpt` 用在虚拟机客户机里，前提是该客户机的磁盘布局能满足上表的校验项（例如系统盘、主分区不超过三个、无扩展分区）。这是本章的归纳，不是官方对虚拟机的明文许可。

---

## 6.11 术语专节：「MBR」这个词在同一批资料里有三种读法

这一节是为了防止一个具体的误读，它在本轮素材里有真实来源：

1. **`L3-1` 说的 MBR = 纯 MBR 分区方案**。官方原文 `"BIOS uses MBR (Master Boot Record) partitioning"` 指的是整块盘采用 MBR 分区方式 [^c6-L3-1]。
2. **`gdisk` 输出里的 `MBR: protective` = GPT 的兼容外壳**。在 6.4 节的 `gdisk` 会话里，分区表扫描结果打印的是：

   ```
   Partition table scan:
     MBR: protective
     BSD: not present
     APM: not present
     GPT: present

   Found valid GPT with protective MBR; using GPT.
   ```
   [^c6-L3-3]

   这里 `MBR: protective` 是 GPT 为了保护自己不被只认 MBR 的老工具破坏而加上的兼容层，**磁盘本身是 GPT**。

3. **因此**：把 `L3-1` 那句读成「GPT 磁盘上没有 MBR」是**误读**。正确的理解是 —— 那块盘用的是 GPT 分区方案，同时带一个 protective MBR 外壳；两者说的是不同层面的东西 [^c6-L3-1][^c6-L3-3]。

> [!tip] 大白话
> 这就像「信封」这个词：`L3-1` 说的是「你寄信用的是信封还是明信片」（分区方案），而 `gdisk` 报的 `MBR: protective` 是说「这个快递盒外面贴了一张旧规格的条码，好让老扫描枪也能扫」（兼容外壳）。看到旧条码不等于里面装的是旧规格的东西。

---

## 6.12 本章缺口汇总

以下几处本轮素材未覆盖，本章不写结论：

1. **「确认当前固件」的读取命令**：本轮素材未提供（见 6.1）。
2. **`L3-1` 页面里的控制台报错原文**：缓存中该处为空（见 6.2）。
3. **PVE 缺 `efidisk0` 的官方失败现象与修复**：官方参考手册未描述，wiki 侧只有引导项缺失的链路（见 6.9）。
4. **VirtualBox 7.2 的 Secure Boot 密钥管理**：本轮零覆盖，本章因此不涉及在 VirtualBox 上关闭 / 管理 Secure Boot 的具体做法。
5. **Hyper-V 第 2 代启动失败的官方排错文档**：本轮只取到代次规划页与安全设置页，排错页未纳入；因此本章的 Secure Boot 部分引用 Hyper-V 来源时只讲机制，不讲 Hyper-V 侧的排错步骤。
6. **用户真实报错原文/截图**：尚未提供，本章按通用原理覆盖（见开篇说明）。

---

## 本章小结

- **最根本的一条**：固件与分区表是绑定的 —— BIOS 用 MBR、EFI 需要 GPT，**切换固件不会转换分区表**，官方把「切完起不来」定性为预期行为。所以「创建时就定死」是性价比最高的一条纪律 [^c6-L3-1]。
- **能救的三格**：停在 EFI Shell（补 boot entry）、找不到引导加载程序（`gdisk` 以 `ef00` 重建 ESP）、ESP 损坏（`fsck.vfat` 清理，先备份、先 `-n` 干跑）[^c6-L2-3][^c6-L3-3]。
- **只能回滚的一格**：`/boot` 内容整体被删且无法恢复时，官方明说**从备份恢复是唯一选项** [^c6-L3-3]。
- **Secure Boot 拦截**的处置是「签名」或「关掉」；但 VMware 在 VBS 启用时**两项都不可编辑**，「关掉」这条路走不通 [^c6-GEN12][^c6-GEN2SEC][^c6-L1-1]。
- **两条迁移路径**：客户机内先 `mbr2gpt` 再改固件为 UEFI（不能转非系统盘、主分区不超过三个、转换后固件必须重配、Win7/8/8.1 离线转换不受官方支持，且该页不含虚拟机字样），或保留磁盘、新建 UEFI 虚拟机把盘挂过去 [^c6-MBR2GPT][^c6-L3-1]。
- **一个防误读的术语**：`L3-1` 的 MBR 指分区方案，`gdisk` 的 `MBR: protective` 指 GPT 的兼容外壳，两者不可混读 [^c6-L3-1][^c6-L3-3]。

---

至此六章正文结束：第 1、2 章给出概念对齐与选型决策，第 3、4、5 章分别落到 VMware Workstation、VirtualBox、PVE 三处操作，第 6 章把失败现象收敛成症状表。**下一步是组装与发布** —— 把六章按顺序拼接成完整笔记、统一标题层级与引用编号、补上章间过渡语，随后按 Obsidian 规范补 frontmatter、标签与 Callout，发布到你的 vault，并在 MOC 里加一条索引。你手上那台机器的真实报错（原文或截图）随时发过来，会回读第 6 章对应行并按真实报错重写。

---

[^c6-L3-1]: **L3-1（official 知识库）** · Virtual Machine fails to boot when changing the Firmware from BIOS to EFI（Broadcom KB Article ID 384912） · https://knowledge.broadcom.com/external/article/384912/
[^c6-L3-3]: **L3-3（official 排错文档）** · Troubleshoot UEFI boot failures with Azure Linux images — Microsoft Learn · https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/azure-linux-vm-uefi-boot-failures
[^c6-L2-3]: **L2-3（官方 wiki，非参考手册）** · Proxmox VE Wiki — OVMF/UEFI Boot Entries · https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries
[^c6-L2-1]: **L2-1（official 参考手册）** · Proxmox VE Administration Guide — Qemu/KVM Virtual Machines · https://pve.proxmox.com/pve-docs/chapter-qm.html
[^c6-L3-5]: **L3-5（community）** · VirtualBox ticket #18282 — EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. => fixed in svn · https://www.virtualbox.org/ticket/18282
[^c6-L1-1]: **L1-1（official 参考手册）** · VMware Workstation Pro — Configure a Firmware Type · https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/25H2/using-vmware-workstation-pro/using-virtual-machines-in-workstation-pro-user-guide/starting-virtual-machines/configure-a-firmware-type.html
[^c6-GEN12]: **GEN12（official 参考手册）** · Should I create a generation 1 or 2 virtual machine in Hyper-V? — Microsoft Learn · https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
[^c6-GEN2SEC]: **GEN2SEC（official 参考手册）** · Hyper-V Generation 2 Virtual Machine Security Features — Microsoft Learn · https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/learn-more/Generation-2-virtual-machine-security-settings-for-Hyper-V
[^c6-MBR2GPT]: **MBR2GPT（official 参考手册）** · MBR2GPT.EXE — Microsoft Learn · https://learn.microsoft.com/en-us/windows/deployment/mbr-to-gpt
