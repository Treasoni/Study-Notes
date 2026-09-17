# 第五章：PVE 实操（SeaBIOS vs OVMF）

在 PVE 里创建虚拟机，固件不是一个孤零零的下拉框：它旁边还有机型（Machine Type），底下还会牵出一块专门的小磁盘（EFI Disk），而这块磁盘的类型又决定了 Secure Boot 能不能开。这一章按「默认值 → 切换判据 → 必须补的配套 → 选项逐项语义 → 与机型和直通的牵制 → 进 OVMF 菜单」的顺序讲清楚，让你建机时一次就选对，而不是装完系统再回来返工。

本章出现的来源有四种层级，读的时候请留意：`L2-1`（PVE 管理指南）与 `L2-2`（`qm.conf` 手册页）、`L2-4`（pve-docs 直通源文件）是**官方参考手册**；`L2-3` 是**官方 wiki**（不是参考手册）；`L2-5` 是 **community**（第三方最佳实践文章）。同一件事如果两类来源口径不同，我会并列写出来。

---

## 5.1 默认是 SeaBIOS，官方的切换判据只有一条

官方对固件在虚拟机里的角色给出的定义是：为了正确模拟一台计算机，QEMU 需要使用一份固件 —— 在普通 PC 上通常称为 BIOS 或 (U)EFI，它在虚拟机启动的最初几步执行，负责基本硬件初始化，并给操作系统提供访问固件与硬件的接口 [^c5-L2-1]。

默认值很明确：`"By default QEMU uses SeaBIOS for this, which is an open-source, x86 BIOS implementation."` 紧接着官方给了它一个定位 —— `"SeaBIOS is a good choice for most standard setups."`（适合多数标准配置）[^c5-L2-1]。

**最有价值的一条官方判据**出现在「System Settings」小节，原文是：

> `"In most cases you want to switch from the default SeaBIOS to OVMF only if you plan to use PCIe passthrough."` [^c5-L2-1]

翻译成操作语言：**多数情况下，只有当你要做 PCIe 直通时，才需要把默认的 SeaBIOS 换成 OVMF**。这条比任何「新机器都该用 UEFI」的说法都更贴 PVE 的官方立场。

官方在同一节还补了一句同类场景：`"There are other scenarios in which the SeaBIOS may not be the ideal firmware to boot from, for example if you want to do VGA passthrough."`（例如做 VGA 直通时，SeaBIOS 可能不是理想固件）[^c5-L2-1]。

### 但客户机系统的硬性要求会压过默认值

官方原文：`"Some operating systems (such as Windows 11) may require use of an UEFI compatible implementation. In such cases, you must use OVMF instead, which is an open-source UEFI implementation."` [^c5-L2-1]

注意 `"you must use OVMF instead"` 的强度 —— 这不是「建议」，而是「必须」。也就是说默认值让位于客户机系统自身的启动要求，这一条与你手上那台 Windows 11 客户机直接相关。

### arm64 主机上没得选

官方原文：`"SeaBIOS, and thus bios=seabios, is available for x86 guests only. On arm64 hosts, virtual machines always boot through UEFI, using the ARM build of OVMF (AAVMF), so bios=ovmf is the only supported setting there."` [^c5-L2-1]

即：SeaBIOS 只支持 x86 客户机；arm64 主机上虚拟机一律走 UEFI（用的是 OVMF 的 ARM 构建，名为 AAVMF），`bios=ovmf` 是那边唯一受支持的设置。顺带一句与机型相关的官方说明：Intel 440FX 与 Q35 芯片组都只针对 x86 客户机；arm64 主机上虚拟机使用的是 `virt` 机型 [^c5-L2-1]。

| 你的场景 | 固件该选 | 依据（层级） |
| --- | --- | --- |
| 普通 x86 客户机，无直通 | `seabios`（默认） | 官方：「适合多数标准配置」[^c5-L2-1] |
| 要做 PCIe 直通 | `ovmf` | 官方：「多数情况下，只有计划用 PCIe 直通时才需要切换」[^c5-L2-1] |
| 要做 VGA 直通 | `ovmf`（官方列为 SeaBIOS 可能不理想的场景） | 官方 [^c5-L2-1] |
| 客户机是 Windows 11 一类要求 UEFI 的系统 | `ovmf`（官方用词是 must） | 官方 [^c5-L2-1] |
| 主机是 arm64 | `ovmf`（唯一受支持） | 官方 [^c5-L2-1] |

> [!tip] 大白话
> 把 PVE 的默认固件想成店里配好的「标准套餐」：SeaBIOS 就是那份套餐，官方自己说它适合大多数常规场景。只有当你点了某个特殊加菜（PCIe 直通），或者客人自己带了个必须用另一套家伙的胃口（Windows 11），才需要换。所以「我该不该换」的答案不在潮流里，在你这台客户机要干什么。

---

## 5.2 用 OVMF 就必须有 EFI Disk，而且只能有一块

这是 PVE 相对 VMware、VirtualBox 多出来的一步，也是最容易漏的一步。官方原文：

> `"In order to save things like the boot order, there needs to be an EFI Disk. This disk will be included in backups and snapshots, and there can only be one."` [^c5-L2-1]

三件事一次说清：① 为了保存 **boot order** 这类信息，**需要**有一块 EFI Disk；② 这块盘**会纳入备份与快照**（所以它不是可有可无的临时文件，是配置的一部分）；③ **只能有一块**。

创建命令（官方原文形式）[^c5-L2-1]：

```bash
# 为 VMID 为 100 的虚拟机添加一块 EFI 磁盘
# <storage> 换成你要存放它的存储名（如 local-lvm），<format> 换成该存储支持的一种格式
qm set 100 -efidisk0 local-lvm:1,format=qcow2,efitype=4m,pre-enrolled-keys=1
```

官方对两个占位符的说明是：`<storage>` 是「你想放这块盘的存储」，`<format>` 是「该存储支持的一种格式」[^c5-L2-1]。命令行之外还有 GUI 路径：在虚拟机的硬件区域 `Add` → `EFI Disk` [^c5-L2-1]。

> [!tip] 大白话
> 这块 EFI Disk 像是固件的「便利贴本」：机器每次开机要从哪儿启动、上次记住了什么引导项，都记在这本小本子上。用 OVMF 就得给它配一本（`there needs to be an EFI Disk`），而且只能配一本（`there can only be one`）—— 两本会打架。它还会跟着备份和快照一起走，所以别把它当成随手可删的临时文件。

---

## 5.3 efitype 一律用 4m

官方管理指南的措辞是：

> `"For new VMs, this should always be 4m, as it supports Secure Boot and has more space allocated to support future development (this is the default in the GUI)."` [^c5-L2-1]

参考手册对 `efitype` 的定义是：`efitype=<2m | 4m>`，**默认 `2m`**；`4m` 更新且被推荐，**是 Secure Boot 的必需条件**；为向后兼容，未指定时使用 `2m`；该项对 `arch=aarch64`（ARM）的虚拟机被忽略 [^c5-L2-2]。

### 一个容易踩的口径差：GUI 默认 4m，命令行默认 2m

把上面两段并排读，会发现一个必须知道的差异：

| 入口 | 不给 efitype 时落到哪 | 依据 |
| --- | --- | --- |
| GUI 新建（Add → EFI Disk） | **4m**（官方明说 4m 是 GUI 里的默认） | 官方管理指南 [^c5-L2-1] |
| 手写命令行 `qm set ... -efidisk0 ...` 不给 `efitype=` | **2m**（参考手册的默认值是 2m） | 官方参考手册 [^c5-L2-2] |

**所以手敲命令时一定要把 `efitype=4m` 写上**（就是 5.2 那条命令里的写法）。不写不会报错，但你会悄悄拿到一块 2m 的 EFI 磁盘，等你哪天想开 Secure Boot 才发现不够用。

### 已经建了 2m 想改用 4m：只能删了重建

官方原文：

> `"If you want to start using Secure Boot in an existing VM (that still uses a 2m efidisk), you need to recreate the efidisk. To do so, delete the old one (qm set <vmid> -delete efidisk0) and add a new one as described above. This will reset any custom configurations you have made in the OVMF menu!"` [^c5-L2-1]

两个后果都要知道：① **必须删除重建**（原文 `"you need to recreate the efidisk"`）；② 重建会**重置你在 OVMF 菜单里做过的所有自定义配置** —— 而 5.8 节会讲，给客户机加引导项正是要在 OVMF 菜单里做，所以「先定 efitype，再进菜单调」是正确顺序，反过来就要重做一遍。

> [!tip] 大白话
> `efitype` 像给固件本子选纸张规格：2m 是旧规格，4m 是新规格且是开 Secure Boot 的硬门槛。换规格不能把纸抽出来换一张，只能整本重来 —— 而整本重来，你之前在本子上做的所有标注（OVMF 菜单里的自定义项）都会没。

---

## 5.4 `efidisk0` 六个子项逐个说

参考手册给出的完整签名是 `efidisk0: [file=]<volume> [,efitype=<2m|4m>] [,format=<enum>] [,ms-cert=<enum>] [,pre-enrolled-keys=<1|0>] [,size=<DiskSize>]`，一句话作用说明是「Configure a disk for storing EFI vars」（配置一块存储 EFI 变量的磁盘）[^c5-L2-2]。

| 子项 | 取值 | 官方说明 | 你该怎么对待 |
| --- | --- | --- | --- |
| `file` | `<volume>` | 该盘的承载卷 | 由 `qm set` 从 `-efidisk0 <storage>:...` 里的存储名自动落成，一般不用手写 |
| `efitype` | `2m` / `4m`（默认 2m） | 4m 更新且被推荐，是 Secure Boot 必需条件；未指定则 2m；ARM 下被忽略 [^c5-L2-2] | **显式写 `4m`** |
| `format` | `cloop` / `qcow` / `qcow2` / `qed` / `raw` / `vmdk` | 承载文件的格式 [^c5-L2-2] | 填你的存储支持的那种 |
| `ms-cert` | `2011` / `2023` / `2023k` / `2023w`（默认 `2011`） | 「信息性标记」，表示 PVE 已登记的微软 UEFI 证书版本；`2023k` 表示已包含 Microsoft UEFI CA 2023、Windows UEFI CA 2023 与 Microsoft Corporation KEK 2K CA 2023；`2023` 与 `2023w` 已弃用、仅为兼容 [^c5-L2-2] | **只读看作状态**，不要当开关去改 |
| `pre-enrolled-keys` | `<boolean>`（默认 `0`） | 当与 `efitype=4m` 配合使用时，使用一份预置了发行版专用密钥与微软标准密钥的 EFI vars 模板；**注意这会默认启用 Secure Boot**，但仍可在虚拟机内部关闭 [^c5-L2-2] | 想要 Secure Boot 就设 `1` |
| `size` | `<DiskSize>` | `"Disk size. This is purely informational and has no effect."`（纯属信息性，没有任何实际作用）[^c5-L2-2] | **不要试图靠它调整容量** |

关于 `pre-enrolled-keys` 再多一句：官方管理指南在讲创建命令时也重复了同一层意思 —— 它会「默认启用 Secure Boot」，但**仍可以在虚拟机内的 OVMF 菜单里关掉** [^c5-L2-1]。也就是说这个选项是「开箱即开 Secure Boot」，不是「锁死」。

> [!tip] 大白话
> 这六个子项里，两个是真开关（`efitype`、`pre-enrolled-keys`），一个是纯装饰（`size` —— 官方明说它没有任何实际作用，写了也不改变磁盘大小），一个是状态标签（`ms-cert`，告诉你证书登记到哪一步了），剩下两个是「盘放哪儿、用什么格式」的常规参数。

---

## 5.5 顺手提醒：微软的 2011 证书已在 2026 年 6 月到期

这一节只在你用 Secure Boot 时才需要考虑，但时间是敏感的。官方给的信息是 [^c5-L2-1]：

- 微软 2011 年签发的那套证书（Windows 与常见 Linux 发行版用于 Secure Boot 的）**在 2026 年 6 月到期**；微软在 2023 年签发了替代证书。
- 固件**只允许**用 EFI 磁盘上存在的证书签过名的引导加载程序启动。具体地，**只有 2011 证书的 EFI 磁盘会拒绝用 2023 证书签名的引导加载程序**。
- 配置里出现 `ms-cert=2023k` 标记，表示新证书已经登记。
- 若 `pve-edk2-firmware` 包版本不低于 `4.2025.05-1`，**新建的 EFI 磁盘会同时包含 2011 与 2023 证书**并带 `ms-cert=2023k` 标记；早于该版本创建的磁盘则需要手动登记。
- 登记方式：在 UI 的硬件视图里选中该 EFI 磁盘，用 `Disk Action > Enroll Updated Certificates`；或走 API；命令行等价命令是：
  ```bash
  qm enroll-efi-keys 100
  ```
  官方注明这条 CLI 命令**要求虚拟机处于关机状态**，登记在虚拟机下次启动时生效 [^c5-L2-1]。
- 官方另有一条**硬警告**：如果 Windows 客户机用了 BitLocker，在登记之前**必须**先对每个启用了 BitLocker 的驱动器执行（在客户机内的 PowerShell 里）：
  ```powershell
  manage-bde -protectors -disable C:
  ```
  否则**下次启动会被要求输入 BitLocker 恢复密钥** [^c5-L2-1]。
- 启动任务的日志里如果出现 `ms-cert=2023` 或 `ms-cert=2023w` 标记，官方提示那可能表示**部分登记**，应当在启动日志中留意警告，并对这类 EFI 磁盘同样执行登记流程 [^c5-L2-1]。

> **边界**：以上是官方参考手册的口径，适用于 PVE 侧。客户机系统内部的后续步骤（在 Windows 里更新 Secure Boot、用 2023 证书重签引导程序）官方文档把读者指向了微软的支持文章，不在本章范围内 [^c5-L2-1]。

---

## 5.6 机型与固件是两件事，但会互相牵制

**先把两者的官方定义分开**：机型的官方说明是「VM 的 Machine Type 定义了虚拟机主板（virtual motherboard）的硬件布局」，可选默认的 Intel 440FX 或 Q35 芯片组；Q35「还提供一条虚拟 PCIe 总线，因此在你想要直通 PCIe 硬件时可能是想要的」；此外还可选择 vIOMMU 实现 [^c5-L2-1]。固件是另一个选项（`bios`）[^c5-L2-1]。

**官方给定的三条耦合关系**：

1. **Intel vIOMMU 需要机型为 q35** —— 参考手册在 `viommu` 子项下写得很短：`"Enable and set guest vIOMMU variant (Intel vIOMMU needs q35 to be set as machine type)."` [^c5-L2-2]
2. **PCIe 直通只在 q35 上可用；PCI 直通在 i440fx 与 q35 上都能用** —— 直通文档原文：`"Note that, while PCI passthrough is available for i440fx and q35 machines, PCIe passthrough is only available on q35 machines."` 同一段还解释：把 PCIe 设备当作 PCI 设备直通**不会**让它只跑 PCI 速度，`"Passing through devices as PCIe just sets a flag for the guest"`（只是给客户机设一个标志，告诉它这是 PCIe 设备而不是「很快的旧式 PCI 设备」），部分客户机应用会因此受益 [^c5-L2-4]。
3. **GPU 直通的最佳兼容组合是 q35 + OVMF + PCIe，且有附加条件** —— 直通文档原文：`"When passing through a GPU, the best compatibility is reached when using 'q35' as machine type, 'OVMF' ('UEFI' for VMs) instead of SeaBIOS and PCIe instead of PCI."` 紧接着的条件是：`"Note that if you want to use 'OVMF' for GPU passthrough, the GPU needs to have a UEFI-capable ROM, otherwise use SeaBIOS instead."` [^c5-L2-4]

最后这条特别值得记住：**显卡如果没有支持 UEFI 的 ROM，官方要求改回 SeaBIOS**。也就是说「做直通就上 OVMF」并不总成立，硬件本身会把你推回 Legacy 一侧。

**社区口径（community 层级，非官方）**：`L2-5` 把机型与固件列为**两个独立**的选项来推荐 —— 机型推荐 q35（理由是已有现代 PCIe 支持，且是 TPM 2.0、PCIe 直通等特性的前提），固件推荐 OVMF 并称「SeaBIOS 只应用于 legacy 系统或较老的操作系统版本」（原文 `"SeaBIOS should only be used for legacy systems or older operating system versions"`）[^c5-L2-5]。注意这是**这家的实践经验建议**（文章开头自述基于实践经验），与 5.1 节官方「多数情况下只有做 PCIe 直通才需要切」的取向不同 —— **是取向不同，不是直接互斥**，两边都可以各自成立。

---

## 5.7 `bios` 这一项在参考手册里只有一句话

参考手册对 `bios` 的完整定义是：

> `bios: <ovmf | seabios> (default = seabios)` —— `"Select BIOS implementation."` [^c5-L2-2]

就这么多。**没有**附任何限制、机型约束或不可变标注。

### 缺口一：`bios` 创建后能不能改，官方无明文

这一格必须标为缺口：

- 参考手册的 `bios` 项**没有任何**「创建后不可修改」的标注 [^c5-L2-2]；
- 管理指南全文也**没有** `qm set --bios` 的示例 [^c5-L2-1]；
- 两者合起来意味着：**既没有支持证据，也没有反驳证据**。

社区里「只能创建时设定」的说法本轮**未证实**，不得写成结论。请按「创建时就定好」来操作，遇到需要改的情况自行验证后再动。

### 一处引文归属要写准（本轮已更正）

本轮素材核对时发现有一句话被挂错了出处，落笔必须用准确版本：

- 「创建后不能改（只能删除）」这句原文 `"cannot be changed (only removed) once created"` 出自**管理指南 `L2-1` 的 TPM / `tpmstate` 小节**，讲的是 **TPM 状态卷**，不是 `bios`、也不是 `efidisk0`。原文是：`"A TPM is added by specifying a tpmstate volume. This works similar to an efidisk, in that it cannot be changed (only removed) once created."` [^c5-L2-1]
- 参考手册 `L2-2` 侧**不存在**这句话；它对应的不可变标注在 `tpmstate` 的 `version` 子项：`"v2.0 is newer and should be preferred. Note that this cannot be changed later on."` [^c5-L2-2]

**结论不变**（`bios` 项确实没有任何不可变标注），但引用时必须用上面的准确出处 —— 否则读者会以为官方说过 `efidisk0` 或 `bios` 不可改。

### 缺口二：i440fx + OVMF 是否受官方支持，三份官方来源均未表态

`L2-1`（管理指南）、`L2-2`（参考手册）、`L2-4`（直通文档）三份官方来源**都没有**说明 i440fx 与 OVMF 的这种组合是否受支持；社区侧则把它当作一个独立可选项在用 [^c5-L2-5]。**没有表态不等于支持，也不等于不支持** —— 这一格保持缺口。

同理，`L2-5` 称 TPM 2.0 的前提是「机型 q35 + 固件 OVMF」，而官方 `L2-1` 只讲了「通过指定 `tpmstate` 卷来添加 TPM」，**未写任何机型或固件前提** [^c5-L2-1]。这属于「一方声明、另一方未声明」，**不得当作官方口径**。

---

## 5.8 进 OVMF 菜单，手动加一个引导项

以下内容出自 **Proxmox VE 官方 wiki**（`L2-3`）—— 它是官方 wiki，但**不是**参考手册，引用时请保留这层区别。

### 固件怎么找到引导程序（理解这一层，才对得上后面的操作）

wiki 的原话是：如果虚拟机通过 OVMF（UEFI）启动，**固件必须知道它要从 ESP 启动哪个 bootloader**（`"the firmware has to know which bootloader it has to start from the ESP"`）；**当 EFIVARS 存储里不存在任何 boot entry 时，它会尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`；如果这一步也失败，虚拟机就会被引导进入 EFI Shell** [^c5-L2-3]。

这条三步链路（查 boot entry → 退到固定回退路径 → 再失败进 EFI Shell）是第 6 章排错的骨架，请先记住形状。

### 操作步骤

wiki 的 Short How-To 五步 [^c5-L2-3]：

1. 启动虚拟机，**在 splash 画面出现时恰好按一次 ESC**（原文 `"press ESC exactly once"`）。
   - **当前版本的 PVE**：还需要选择 `"EFI Firmware Setup"` 条目才能进入 OVMF 菜单；
   - **较老版本的 PVE**：按完 ESC 就已经在 OVMF 菜单里了。
2. 依次进入 `Boot Maintenance Manager` → `Boot Options` → `Add Boot Option` → 选择**带 EFI System Partition 的那块磁盘**。
3. 找到 EFI 可执行文件。wiki 举的例子是：Debian 为 `EFI/debian/grubx64.efi`，Fedora 为 `EFI/fedora/shimx64-fedora.efi` [^c5-L2-3]。
4. 给它起个名字（`"Input the description"`），然后 `Commit Change`。
5. 用 `Change Boot Order` 把新建的这一项挪到最前面。

详细版里补的路径示例是：进入 Boot Maintenance Manager → 选 `Boot Options` → 选 `Add Boot Option` → 选带 ESP 的硬盘 → 在目录结构里导航到你的 bootloader（详细版示例用 `EFI/debian/shimx64.efi`）→ 命名并提交 → 再改启动顺序把它设为默认 [^c5-L2-3]。

> [!tip] 大白话
> 把固件想成一个记性不太好又很守规矩的门卫：它手里有一张名单（EFIVARS 里的 boot entry），写着「先去敲这扇门」。名单空了，他就去敲那个约定俗成的默认门（`$ESP/EFI/BOOT/BOOTX64.efi`）；那扇门也打不开，他就不干活了，站在那儿等你来教（EFI Shell）。5.8 这一节做的事，就是进他的值班室，把该敲哪扇门重新写进名单，再挪到第一位。

### 两条与显示、PXE 相关的官方补充

- **OVMF + 虚拟显示（非 VGA 直通）时，客户机分辨率需要在 OVMF 菜单里设置**（就是上面那个启动时按 ESC 的入口），或者干脆把显示类型选成 SPICE [^c5-L2-1]。
- **OVMF 走 PXE 启动时，必须给虚拟机加一个 RNG 设备** —— 官方理由是：出于安全考虑，OVMF 固件会**禁用**没有随机数生成器的客户机的 PXE 启动 [^c5-L2-1]。

---

## 5.9 本章明确不写的两格（缺口汇总）

1. **`bios` 项创建后能否修改**：官方无明文，既无支持证据也无反驳证据（见 5.7）。
2. **i440fx + OVMF 是否受官方支持**：三份官方来源均未表态（见 5.7）。

另外，`L2-5` 关于 TPM 2.0 前置条件（q35 + OVMF）的说法属 community，官方未声明，本章已按此标注，未升级为官方口径 [^c5-L2-5]。

---

## 本章小结

- **PVE 默认固件是 SeaBIOS**，官方自己说它适合多数标准配置；**官方给出的切换判据是「多数情况下只有计划用 PCIe 直通时才需要换到 OVMF」**，此外 VGA 直通、客户机系统硬性要求（Windows 11 用 `must`）与 arm64 主机（`bios=ovmf` 唯一受支持）会要求改选 [^c5-L2-1]。
- **用 OVMF 就必须有一块 EFI Disk**（保存 boot order 等信息，纳入备份与快照，只能有一块）；创建命令 `qm set <vmid> -efidisk0 <storage>:1,format=<format>,efitype=4m,pre-enrolled-keys=1` [^c5-L2-1]。
- **`efitype` 一律显式写 `4m`**：GUI 默认就是 4m，但手写命令不给该参数会落到参考手册默认的 2m；已有 2m 想开 Secure Boot 必须**删除重建**，且会重置 OVMF 菜单里的自定义配置 [^c5-L2-1][^c5-L2-2]。
- **`efidisk0` 六项语义**：`efitype` 与 `pre-enrolled-keys` 是真开关，`pre-enrolled-keys=1` 默认启用 Secure Boot（VM 内仍可关），`ms-cert` 是证书登记状态标记，`size` 纯属信息性、没有实际作用 [^c5-L2-2]。
- **机型与固件会互相牵制**：Intel vIOMMU 需 q35；PCIe 直通只在 q35 可用（PCI 直通两者皆可）；GPU 直通最佳组合是 q35 + OVMF + PCIe，但**显卡没有 UEFI-capable ROM 时官方要求改用 SeaBIOS** [^c5-L2-2][^c5-L2-4]。
- **引导失败的链路**（官方 wiki 层级）：EFIVARS 无 boot entry → 回退加载 `$ESP/EFI/BOOT/BOOTX64.efi` → 仍失败则进 EFI Shell；修复入口是启动时按一次 ESC 进 OVMF 菜单，`Boot Maintenance Manager → Boot Options → Add Boot Option` [^c5-L2-3]。

下一章是排错专章，会把这一章的两条线索接上：一条是 OVMF 的三步引导链路（boot entry → 回退路径 → EFI Shell），另一条是固件与分区表的绑定关系（BIOS 配 MBR、EFI 需 GPT，切换不会自动转换分区表）。症状表按「症状 → 根因 → 处置」三列组织，并明确标出哪些格子目前只能靠备份恢复、哪些格子还没有官方说法。

---

[^c5-L2-1]: **L2-1（official 参考手册）** · Proxmox VE Administration Guide — Qemu/KVM Virtual Machines（含 BIOS and UEFI / System Settings / Secure Boot Certificate Expiration / Trusted Platform Module 各小节） · https://pve.proxmox.com/pve-docs/chapter-qm.html
[^c5-L2-2]: **L2-2（official 参考手册）** · Proxmox VE — qm.conf(5) 手册页（含 `bios` / `efidisk0` / `machine` / `tpmstate0` 各条目） · https://pve.proxmox.com/pve-docs/qm.conf.5.html
[^c5-L2-3]: **L2-3（官方 wiki，非参考手册）** · Proxmox VE Wiki — OVMF/UEFI Boot Entries · https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries
[^c5-L2-4]: **L2-4（official 参考手册源文件）** · pve-docs（master 快照）— PCI(e) Passthrough · https://raw.githubusercontent.com/proxmox/pve-docs/master/qm-pci-passthrough.adoc
[^c5-L2-5]: **L2-5（community）** · Best Practice Configurations for Virtual Machines on Proxmox VE（Starline） · https://www.starline.de/en/magazine/technical-articles/best-practice-configurations-for-virtual-machines-on-proxmox-ve
