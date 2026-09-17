---

两个桌面平台都过了一遍，下一章转向服务器侧的 PVE。它是三个平台里唯一必须额外创建一块磁盘（EFI Disk）才能启用 UEFI 的，而且机型（q35 / i440fx）与固件之间还有一层耦合——这两点在前面两章都没有出现过。

## 第五章：PVE 实操（SeaBIOS vs OVMF）

在 PVE 里创建虚拟机，固件不是一个孤零零的下拉框：它旁边还有机型（Machine Type），底下还会牵出一块专门的小磁盘（EFI Disk），而这块磁盘的类型又决定了 Secure Boot 能不能开。这一章按「默认值 → 切换判据 → 必须补的配套 → 选项逐项语义 → 与机型和直通的牵制 → 进 OVMF 菜单」的顺序讲清楚，让你建机时一次就选对，而不是装完系统再回来返工。

本章出现的来源有四种层级，读的时候请留意：`L2-1`（PVE 管理指南）与 `L2-2`（`qm.conf` 手册页）、`L2-4`（pve-docs 直通源文件）是**官方参考手册**；`L2-3` 是**官方 wiki**（不是参考手册）；`L2-5` 是 **community**（第三方最佳实践文章）。同一件事如果两类来源口径不同，我会并列写出来。

---

### 5.1 默认是 SeaBIOS，官方的切换判据只有一条

官方对固件在虚拟机里的角色给出的定义是：为了正确模拟一台计算机，QEMU 需要使用一份固件 —— 在普通 PC 上通常称为 BIOS 或 (U)EFI，它在虚拟机启动的最初几步执行，负责基本硬件初始化，并给操作系统提供访问固件与硬件的接口 [^c5-L2-1]。

默认值很明确：`"By default QEMU uses SeaBIOS for this, which is an open-source, x86 BIOS implementation."` 紧接着官方给了它一个定位 —— `"SeaBIOS is a good choice for most standard setups."`（适合多数标准配置）[^c5-L2-1]。

**最有价值的一条官方判据**出现在「System Settings」小节，原文是：

> `"In most cases you want to switch from the default SeaBIOS to OVMF only if you plan to use PCIe passthrough."` [^c5-L2-1]

翻译成操作语言：**多数情况下，只有当你要做 PCIe 直通时，才需要把默认的 SeaBIOS 换成 OVMF**。这条比任何「新机器都该用 UEFI」的说法都更贴 PVE 的官方立场。

官方在同一节还补了一句同类场景：`"There are other scenarios in which the SeaBIOS may not be the ideal firmware to boot from, for example if you want to do VGA passthrough."`（例如做 VGA 直通时，SeaBIOS 可能不是理想固件）[^c5-L2-1]。

#### 但客户机系统的硬性要求会压过默认值

官方原文：`"Some operating systems (such as Windows 11) may require use of an UEFI compatible implementation. In such cases, you must use OVMF instead, which is an open-source UEFI implementation."` [^c5-L2-1]

注意 `"you must use OVMF instead"` 的强度 —— 这不是「建议」，而是「必须」。也就是说默认值让位于客户机系统自身的启动要求，这一条与你手上那台 Windows 11 客户机直接相关。

#### arm64 主机上没得选

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

### 5.2 用 OVMF 就必须有 EFI Disk，而且只能有一块

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

### 5.3 efitype 一律用 4m

官方管理指南的措辞是：

> `"For new VMs, this should always be 4m, as it supports Secure Boot and has more space allocated to support future development (this is the default in the GUI)."` [^c5-L2-1]

参考手册对 `efitype` 的定义是：`efitype=<2m | 4m>`，**默认 `2m`**；`4m` 更新且被推荐，**是 Secure Boot 的必需条件**；为向后兼容，未指定时使用 `2m`；该项对 `arch=aarch64`（ARM）的虚拟机被忽略 [^c5-L2-2]。

#### 一个容易踩的口径差：GUI 默认 4m，命令行默认 2m

把上面两段并排读，会发现一个必须知道的差异：

| 入口 | 不给 efitype 时落到哪 | 依据 |
| --- | --- | --- |
| GUI 新建（Add → EFI Disk） | **4m**（官方明说 4m 是 GUI 里的默认） | 官方管理指南 [^c5-L2-1] |
| 手写命令行 `qm set ... -efidisk0 ...` 不给 `efitype=` | **2m**（参考手册的默认值是 2m） | 官方参考手册 [^c5-L2-2] |

**所以手敲命令时一定要把 `efitype=4m` 写上**（就是 5.2 那条命令里的写法）。不写不会报错，但你会悄悄拿到一块 2m 的 EFI 磁盘，等你哪天想开 Secure Boot 才发现不够用。

#### 已经建了 2m 想改用 4m：只能删了重建

官方原文：

> `"If you want to start using Secure Boot in an existing VM (that still uses a 2m efidisk), you need to recreate the efidisk. To do so, delete the old one (qm set <vmid> -delete efidisk0) and add a new one as described above. This will reset any custom configurations you have made in the OVMF menu!"` [^c5-L2-1]

两个后果都要知道：① **必须删除重建**（原文 `"you need to recreate the efidisk"`）；② 重建会**重置你在 OVMF 菜单里做过的所有自定义配置** —— 而 5.8 节会讲，给客户机加引导项正是要在 OVMF 菜单里做，所以「先定 efitype，再进菜单调」是正确顺序，反过来就要重做一遍。

> [!tip] 大白话
> `efitype` 像给固件本子选纸张规格：2m 是旧规格，4m 是新规格且是开 Secure Boot 的硬门槛。换规格不能把纸抽出来换一张，只能整本重来 —— 而整本重来，你之前在本子上做的所有标注（OVMF 菜单里的自定义项）都会没。

---

### 5.4 `efidisk0` 六个子项逐个说

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

### 5.5 顺手提醒：微软的 2011 证书已在 2026 年 6 月到期

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

### 5.6 机型与固件是两件事，但会互相牵制

**先把两者的官方定义分开**：机型的官方说明是「VM 的 Machine Type 定义了虚拟机主板（virtual motherboard）的硬件布局」，可选默认的 Intel 440FX 或 Q35 芯片组；Q35「还提供一条虚拟 PCIe 总线，因此在你想要直通 PCIe 硬件时可能是想要的」；此外还可选择 vIOMMU 实现 [^c5-L2-1]。固件是另一个选项（`bios`）[^c5-L2-1]。

**官方给定的三条耦合关系**：

1. **Intel vIOMMU 需要机型为 q35** —— 参考手册在 `viommu` 子项下写得很短：`"Enable and set guest vIOMMU variant (Intel vIOMMU needs q35 to be set as machine type)."` [^c5-L2-2]
2. **PCIe 直通只在 q35 上可用；PCI 直通在 i440fx 与 q35 上都能用** —— 直通文档原文：`"Note that, while PCI passthrough is available for i440fx and q35 machines, PCIe passthrough is only available on q35 machines."` 同一段还解释：把 PCIe 设备当作 PCI 设备直通**不会**让它只跑 PCI 速度，`"Passing through devices as PCIe just sets a flag for the guest"`（只是给客户机设一个标志，告诉它这是 PCIe 设备而不是「很快的旧式 PCI 设备」），部分客户机应用会因此受益 [^c5-L2-4]。
3. **GPU 直通的最佳兼容组合是 q35 + OVMF + PCIe，且有附加条件** —— 直通文档原文：`"When passing through a GPU, the best compatibility is reached when using 'q35' as machine type, 'OVMF' ('UEFI' for VMs) instead of SeaBIOS and PCIe instead of PCI."` 紧接着的条件是：`"Note that if you want to use 'OVMF' for GPU passthrough, the GPU needs to have a UEFI-capable ROM, otherwise use SeaBIOS instead."` [^c5-L2-4]

最后这条特别值得记住：**显卡如果没有支持 UEFI 的 ROM，官方要求改回 SeaBIOS**。也就是说「做直通就上 OVMF」并不总成立，硬件本身会把你推回 Legacy 一侧。

**社区口径（community 层级，非官方）**：`L2-5` 把机型与固件列为**两个独立**的选项来推荐 —— 机型推荐 q35（理由是已有现代 PCIe 支持，且是 TPM 2.0、PCIe 直通等特性的前提），固件推荐 OVMF 并称「SeaBIOS 只应用于 legacy 系统或较老的操作系统版本」（原文 `"SeaBIOS should only be used for legacy systems or older operating system versions"`）[^c5-L2-5]。注意这是**这家的实践经验建议**（文章开头自述基于实践经验），与 5.1 节官方「多数情况下只有做 PCIe 直通才需要切」的取向不同 —— **是取向不同，不是直接互斥**，两边都可以各自成立。

---

### 5.7 `bios` 这一项在参考手册里只有一句话

参考手册对 `bios` 的完整定义是：

> `bios: <ovmf | seabios> (default = seabios)` —— `"Select BIOS implementation."` [^c5-L2-2]

就这么多。**没有**附任何限制、机型约束或不可变标注。

#### 缺口一：`bios` 创建后能不能改，官方无明文

这一格必须标为缺口：

- 参考手册的 `bios` 项**没有任何**「创建后不可修改」的标注 [^c5-L2-2]；
- 管理指南全文也**没有** `qm set --bios` 的示例 [^c5-L2-1]；
- 两者合起来意味着：**既没有支持证据，也没有反驳证据**。

社区里「只能创建时设定」的说法本轮**未证实**，不得写成结论。请按「创建时就定好」来操作，遇到需要改的情况自行验证后再动。

#### 一处引文归属要写准（本轮已更正）

本轮素材核对时发现有一句话被挂错了出处，落笔必须用准确版本：

- 「创建后不能改（只能删除）」这句原文 `"cannot be changed (only removed) once created"` 出自**管理指南 `L2-1` 的 TPM / `tpmstate` 小节**，讲的是 **TPM 状态卷**，不是 `bios`、也不是 `efidisk0`。原文是：`"A TPM is added by specifying a tpmstate volume. This works similar to an efidisk, in that it cannot be changed (only removed) once created."` [^c5-L2-1]
- 参考手册 `L2-2` 侧**不存在**这句话；它对应的不可变标注在 `tpmstate` 的 `version` 子项：`"v2.0 is newer and should be preferred. Note that this cannot be changed later on."` [^c5-L2-2]

**结论不变**（`bios` 项确实没有任何不可变标注），但引用时必须用上面的准确出处 —— 否则读者会以为官方说过 `efidisk0` 或 `bios` 不可改。

#### 缺口二：i440fx + OVMF 是否受官方支持，三份官方来源均未表态

`L2-1`（管理指南）、`L2-2`（参考手册）、`L2-4`（直通文档）三份官方来源**都没有**说明 i440fx 与 OVMF 的这种组合是否受支持；社区侧则把它当作一个独立可选项在用 [^c5-L2-5]。**没有表态不等于支持，也不等于不支持** —— 这一格保持缺口。

同理，`L2-5` 称 TPM 2.0 的前提是「机型 q35 + 固件 OVMF」，而官方 `L2-1` 只讲了「通过指定 `tpmstate` 卷来添加 TPM」，**未写任何机型或固件前提** [^c5-L2-1]。这属于「一方声明、另一方未声明」，**不得当作官方口径**。

---

### 5.8 进 OVMF 菜单，手动加一个引导项

以下内容出自 **Proxmox VE 官方 wiki**（`L2-3`）—— 它是官方 wiki，但**不是**参考手册，引用时请保留这层区别。

#### 固件怎么找到引导程序（理解这一层，才对得上后面的操作）

wiki 的原话是：如果虚拟机通过 OVMF（UEFI）启动，**固件必须知道它要从 ESP 启动哪个 bootloader**（`"the firmware has to know which bootloader it has to start from the ESP"`）；**当 EFIVARS 存储里不存在任何 boot entry 时，它会尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`；如果这一步也失败，虚拟机就会被引导进入 EFI Shell** [^c5-L2-3]。

这条三步链路（查 boot entry → 退到固定回退路径 → 再失败进 EFI Shell）是第 6 章排错的骨架，请先记住形状。

#### 操作步骤

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

#### 两条与显示、PXE 相关的官方补充

- **OVMF + 虚拟显示（非 VGA 直通）时，客户机分辨率需要在 OVMF 菜单里设置**（就是上面那个启动时按 ESC 的入口），或者干脆把显示类型选成 SPICE [^c5-L2-1]。
- **OVMF 走 PXE 启动时，必须给虚拟机加一个 RNG 设备** —— 官方理由是：出于安全考虑，OVMF 固件会**禁用**没有随机数生成器的客户机的 PXE 启动 [^c5-L2-1]。

---

### 5.9 本章明确不写的两格（缺口汇总）

1. **`bios` 项创建后能否修改**：官方无明文，既无支持证据也无反驳证据（见 5.7）。
2. **i440fx + OVMF 是否受官方支持**：三份官方来源均未表态（见 5.7）。

另外，`L2-5` 关于 TPM 2.0 前置条件（q35 + OVMF）的说法属 community，官方未声明，本章已按此标注，未升级为官方口径 [^c5-L2-5]。

---

### 本章小结

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

---

三个平台的操作都讲完了。最后一章把前面散落各处的失败模式收拢成一张「症状 → 根因 → 处置」表，作为遇到问题时的回查入口——它同时也是第 1 章那条「固件与分区表绑定」链条的落地清单。

## 第六章：UEFI 排错 —— 症状、根因、处置

这一章解决的是最初那个痛点：「使用 UEFI 时总是出问题」。做法不是罗列一堆可能原因，而是把每条已知故障压成同一张表的三列 —— **症状 → 根因 → 处置** —— 让你从看到的现象倒推到该敲哪条命令。

> **本章的覆盖方式**：用户实际遇到的报错原文/截图尚未提供，本章按**通用原理**覆盖。等你把真实报错（原文或截图）发过来，会回读本表并**按真实报错重写对应行**，而不是另起一章。

读之前先把三类信息的分辨方法定下来，本章每一格都按这个标准标注：

| 标注 | 含义 | 你该怎么用 |
| --- | --- | --- |
| **官方口径** | 来源有明确原文支持 | 可以直接照做 |
| **推理** | 本章或素材的归纳，来源无明文 | 可以当方向，动手前自行确认 |
| **缺口** | 来源未覆盖 | 不要当作已解决，也不要拿别处的说法补齐 |

---

### 6.1 症状总表

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

#### 关于「先确认当前固件」这一步

排错常从「这台机器现在用的到底是哪种固件」开始。**本轮素材没有提供任何读取该设置的命令**，所以本章不写，也不要用记忆里的 `showvminfo` 一类命令顶替。

素材里**确有来源**的可见性判断只有两条，都是「看现象」而不是「查配置」：

- 虚拟机启动时**能看到 OVMF 菜单**（splash 画面出现时按一次 ESC 能进去）→ 说明用的是 OVMF/UEFI 固件 [^c6-L2-3]；
- 虚拟机启动后**直接落进 EFI Shell** → 说明走的是 UEFI 固件，并且引导已经失败到最后一层（回退路径也没成功）[^c6-L2-3]。

其余确认手段属**缺口**，需要你到各平台的设置界面自行查看。

---

### 6.2 症状 1：切了固件就起不来 —— 固件与分区表是绑定的

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

### 6.3 症状 2：停在 EFI Shell 或根本没有引导项

**根因（官方 wiki 层级）**：如果虚拟机走 OVMF（UEFI）启动，固件必须知道它要从 ESP 启动哪个 bootloader；当 **EFIVARS 存储里不存在任何 boot entry** 时，它会尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`；**如果这一步也失败，虚拟机就会被引导进入 EFI Shell** [^c6-L2-3]。

**处置**：进 OVMF 菜单手工把引导项补上 —— splash 画面出现时**恰好按一次 ESC**（当前版本还需选 `EFI Firmware Setup` 条目），然后 `Boot Maintenance Manager` → `Boot Options` → `Add Boot Option` → 选择带 EFI System Partition 的磁盘 → 导航到 EFI 可执行文件（Debian 示例 `EFI/debian/grubx64.efi`，Fedora 示例 `EFI/fedora/shimx64-fedora.efi`）→ 命名并 `Commit Change` → 用 `Change Boot Order` 把它挪到最前 [^c6-L2-3]。

完整步骤与截图式路径见第 5.8 节。

> [!tip] 大白话
> 停在 EFI Shell 就像是门卫找不到名单上该敲的门，最后只能站在大厅等你吩咐。EFI Shell 本身不是错误界面，它是「固件还活着、但不知道下一步干什么」的状态 —— 所以处置也简单：把名单（boot entry）补上，而不是重装系统。

---

### 6.4 症状 3：找不到 UEFI 引导加载程序

**症状原文**（Azure 第 2 代 Linux 虚拟机的启动诊断截图里）[^c6-L3-3]：

```text
Virtual Machine Boot Summary
    1. Unknown Device The boot loader did not load an operating system.
    2. SCSI Disk (0,0) The boot loader did not load an operating system.
    3. SCSI Disk (0,1) The boot loader did not load an operating system.
    4. Network Adapter (000D3A4DD64D) A boot image was not found.
No operating system was loaded. Your virtual machine may be configured incorrectly.
```

**根因（官方原文）**：`"If the EFI System Partition (ESP) has been deleted or is missing, the VM cannot locate the UEFI boot loader and startup will fail."` [^c6-L3-3]

**处置**：把目标磁盘挂到一台修复机上，用 `gdisk` 重建 EFI 分区。关键动作是**把分区类型改成 `ef00`**，扇区起止必须正确。下面是该文档给出的操作片段（逐字引用）[^c6-L3-3]：

```text
Command (? for help): n
Partition number (3-128, default 3):
First sector (34-134217694, default = 10240) or {+-}size{KMGTP}: 10240
Last sector (10240-1026047, default = 1026047) or {+-}size{KMGTP}: 1026047
Current type is 'Linux filesystem'
Hex code or GUID (L to show codes, Enter = 8300): ef00
Changed type of partition to 'EFI System'
```

重建后 `p` 打印出的分区表长这样 [^c6-L3-3]：

```text
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

### 6.5 症状 4：UEFI 启动分区损坏

**症状原文**：`"The UEFI boot partition is corrupted"` [^c6-L3-3]

**根因（官方原文）**：`"If the UEFI boot partition is corrupted, the generation 2 Linux VM will fail to boot."` —— 即 ESP 的文件系统损坏 [^c6-L3-3]。

**处置**：用 `fsck.vfat` 清理。文档先给出**干跑**（`-n`）再看结果的做法，片段逐字引用 [^c6-L3-3]：

```text
root@repair-centos7:~# fsck.vfat -n /dev/sdc3
fsck.fat 4.1 (2017-01-24)
0x25: Dirty bit is set. Fs was not properly unmounted and some data may be corrupt.
 Automatically removing dirty bit.
Leaving filesystem unchanged.
/dev/sdc3: 19 files, 1438/63326 clusters
```

确认无误后再执行修复（交互式确认，`1` 表示移除 dirty bit，最后再跑一次确认已干净）[^c6-L3-3]：

```text
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

### 6.6 症状 5：`/boot` 内容被删除且无法恢复

**根因**：引导所需内容整体丢失 [^c6-L3-3]。

**处置**：官方原文很直接 —— `"restoring the VM from a backup is the only option"`（**从备份恢复虚拟机是唯一选项**）[^c6-L3-3]。

这一格请记住它的意义：它划出了「能救」与「只能回滚」的分界线。前面几格都还能靠 `gdisk`、`fsck.vfat`、加引导项救回来，只有内容整体没了这一格没有技术手段。

---

### 6.7 症状 6：Secure Boot 把引导程序或驱动拦下来了

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

### 6.8 症状 7：VirtualBox 里看不到 EFI Shell

**现象**：图形控制器不是 VBoxVGA、且没有提供可引导介质时，EFI Shell 始终不出现，安装无法进行；报告者补充实际是「完全不启动」（`"No booting, no go"`），并且 `EfiGopMode`、`EfiGraphicsResolution` 等 ExtraData 全部被忽略 [^c6-L3-5]。

**根因**：当时 EFI 固件里**没有**处理 VMSVGA / VBoxSVGA 的图形驱动（开发者原文 `"no graphics driver in the EFI firmware"`）[^c6-L3-5]。

**处置与时间线（务必连读）**：这是 **2019 年**的社区 ticket（community 层级），报告者已用 `r128870`（对应 **6.0.5**）确认修复，ticket 于 2019-04-17 关闭为 `fixed` [^c6-L3-5]。

**所以这一格的正确读法是**：它不是当前版本的问题，而是「黑屏且无报错」这类现象的一个历史实例 —— 根因在**图形路径**而不是引导路径。完整时间线与规避建议见第 4.4 节，那里同样按「带版本」的纪律写。

---

### 6.9 症状 8：PVE 的 UEFI 启动异常 —— 未闭合缺口

这一格必须明确标为**缺口**，不要写成已解决的结论：

- 官方参考手册对 OVMF 的说明只到「为了保存 boot order 这类信息，**需要**有一块 EFI Disk」这一步 [^c6-L2-1]；
- 官方参考手册**没有描述**「缺少 `efidisk0` 时会出现什么失败现象、该怎么修」；
- 官方 wiki 那边只有 6.3 节那条引导链路（boot entry → 回退路径 → EFI Shell），它讲的是**引导项缺失**，不是**缺 EFI 磁盘** [^c6-L2-3]。

**目前的处置只能是**：先按 6.3 的 EFI Shell / 无引导项那条路径查；同时确认这台用 OVMF 的虚拟机确实配了 `efidisk0`（创建命令与选项语义见第 5.2、5.4 节）。

**这是缺口而非结论** —— 记成「官方未描述该失败与修复」即可，不要写成「缺 efidisk0 会导致某某报错」。

---

### 6.10 迁移路径：把一台 Legacy 虚拟机改成 UEFI 启动

如果你不想重建虚拟机，而是想把现有磁盘改成能被 UEFI 启动，有两条路。

#### 路径 A：先在客户机内转 GPT，再改固件为 UEFI

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

```text
X:\> mbr2gpt.exe /validate /disk:0
MBR2GPT: Attempting to validate disk 0
MBR2GPT: Retrieving layout of disk
MBR2GPT: Validating layout, disk sector size is: 512
MBR2GPT: Validation completed successfully
```

完整语法是 `MBR2GPT /validate|convert [/disk:<diskNumber>] [/logs:<logDirectory>] [/map:<source>=<destination>] [/allowFullOS]` [^c6-MBR2GPT]。实操建议是先 `/validate` 再 `/convert` —— 官方说明里也写明：校验不通过时**转换不会进行**，会返回错误 [^c6-MBR2GPT]。

关于 `/allowFullOS` 有一条容易被忽略的后果：默认情况下 `MBR2GPT.exe` **只能从 Windows PE 运行**，在完整 Windows 中会被阻止；该选项解除这一阻止，但**由于在完整 Windows 下运行时现有的 MBR 系统分区正在被使用、无法复用，工具会通过缩小 OS 分区来新建一个 EFI 系统分区** [^c6-MBR2GPT]。

#### 路径 B：保留磁盘，新建一台 UEFI 虚拟机把盘挂过去

这是 VMware 官方给的第一条处置：**重建 VM、选定固件后再把同一批硬盘挂上去** [^c6-L3-1]。它的好处是不需要在客户机里做转换，代价是要重建虚拟机配置。

#### ⚠️ 引用 MBR2GPT 页时必须带的一句边界

`MBR2GPT` 这一页**全文不含** `virtual machine`、`Hyper-V`、`vSphere` 字样 —— 也就是说它讲的是**物理设备**的转换，**虚拟机场景的专属约束不在这一页**，而由 `L3-1` 给出（先转 GPT 再切 EFI，且需客户机系统厂商支持）[^c6-MBR2GPT][^c6-L3-1]。

> **推理**：把 `mbr2gpt` 用在虚拟机客户机里，前提是该客户机的磁盘布局能满足上表的校验项（例如系统盘、主分区不超过三个、无扩展分区）。这是本章的归纳，不是官方对虚拟机的明文许可。

---

### 6.11 术语专节：「MBR」这个词在同一批资料里有三种读法

这一节是为了防止一个具体的误读，它在本轮素材里有真实来源：

1. **`L3-1` 说的 MBR = 纯 MBR 分区方案**。官方原文 `"BIOS uses MBR (Master Boot Record) partitioning"` 指的是整块盘采用 MBR 分区方式 [^c6-L3-1]。
2. **`gdisk` 输出里的 `MBR: protective` = GPT 的兼容外壳**。在 6.4 节的 `gdisk` 会话里，分区表扫描结果打印的是：

   ```text
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

### 6.12 本章缺口汇总

以下几处本轮素材未覆盖，本章不写结论：

1. **「确认当前固件」的读取命令**：本轮素材未提供（见 6.1）。
2. **`L3-1` 页面里的控制台报错原文**：缓存中该处为空（见 6.2）。
3. **PVE 缺 `efidisk0` 的官方失败现象与修复**：官方参考手册未描述，wiki 侧只有引导项缺失的链路（见 6.9）。
4. **VirtualBox 7.2 的 Secure Boot 密钥管理**：本轮零覆盖，本章因此不涉及在 VirtualBox 上关闭 / 管理 Secure Boot 的具体做法。
5. **Hyper-V 第 2 代启动失败的官方排错文档**：本轮只取到代次规划页与安全设置页，排错页未纳入；因此本章的 Secure Boot 部分引用 Hyper-V 来源时只讲机制，不讲 Hyper-V 侧的排错步骤。
6. **用户真实报错原文/截图**：尚未提供，本章按通用原理覆盖（见开篇说明）。

---

### 本章小结

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

---

回到最初那个下拉框：**没有特殊需求就守平台默认（Legacy BIOS / SeaBIOS / BIOS），命中那六条硬性触发条件之一才换 UEFI**，并且尽量在创建虚拟机时一次决定——因为固件与分区表是绑定的，切换不会转换分区表，官方把「切完起不来」定性为预期行为。

真的选错、或者非改不可，路径只有两条：重建虚拟机后挂原盘，或先在客户机内把磁盘转成 GPT 再改固件。而 UEFI 侧那些「起不来」的现象，绝大多数能在第六章的症状表里找到对应的根因与处置——只有「引导内容整体丢失」那一格，官方明说**从备份恢复是唯一选项**。

用户真实报错的原文/截图补齐后，回读第六章对应行替换即可；在那之前，第六章程按通用原理覆盖。

