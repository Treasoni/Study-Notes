# 虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI)

> 笔记类型：对比 + 实战（混合）｜ 覆盖平台：VMware Workstation · VirtualBox · Proxmox VE（Hyper-V 仅作对照）｜ 规模：6 章

虚拟机创建界面上那个 **Firmware type** 下拉框只有两个选项，但它决定了客户机磁盘该用 MBR 还是 GPT、引导项记在哪里、以及系统装完之后还能不能改。用户最常见的两个问题——「不知道用哪个」和「选了 UEFI 总出问题」——根子在同一个地方：**固件不是一个孤立开关，它和客户机磁盘上的分区表、和固件自己记住的引导项，是一条链上的三节**。

本笔记按四段推进：第 1 章对齐概念，第 2 章给出选型决策表，第 3–5 章分别落到 VMware Workstation、VirtualBox、Proxmox VE 三个平台（三章之间无依赖，可以只读你实际在用的那一章），第 6 章把 UEFI 相关的失败现象收敛成一张「症状 → 根因 → 处置」表。

全篇的一条纪律：**每一条结论都标出来源层级**（官方口径 / 社区主张 / 本笔记推理 / 素材缺口）。写着「推理」或「缺口」的地方，请不要当作官方说法使用。

## 目录

- [第一章：固件做什么、BIOS 与 UEFI 差在哪](#第一章固件做什么bios-与-uefi-差在哪)
- [第二章：什么时候必须用 UEFI —— 选型决策](#第二章什么时候必须用-uefi--选型决策)
- [第三章：VMware Workstation 实操](#第三章vmware-workstation-实操)
- [第四章：VirtualBox 实操](#第四章virtualbox-实操)
- [第五章：PVE 实操（SeaBIOS vs OVMF）](#第五章pve-实操seabios-vs-ovmf)
- [第六章：UEFI 排错 —— 症状、根因、处置](#第六章uefi-排错--症状根因处置)

---

## 第一章：固件做什么、BIOS 与 UEFI 差在哪

你在 VMware 里新建虚拟机，翻到 Settings → Options → Advanced，看到一个 **Firmware type** 下拉框，两个选项：Legacy BIOS、UEFI。选哪个？随手选一个，装完系统，日子照过——直到某天你要装 Windows 11、要做 GPU 直通，或者手滑把固件改了一下，虚拟机从此起不来。

这一章不讲操作，先把「这个下拉框到底是什么」说清楚。因为你的两个痛点——「不知道用哪个」和「选 UEFI 总出问题」——根子在同一个地方：**固件不是一个孤立开关，它和客户机磁盘上的分区表、和固件自己记住的引导项，是一条链上的三节**。链上任何一节对不上，虚拟机就停在启动画面上。

---

### 1. 固件是虚拟机的第一段代码

虚拟机本质是一个进程。这个进程启动时，CPU 是「裸」的——内存里没有操作系统，磁盘上的系统也还没有被读。此时必须先跑一段程序，让这台「假电脑」看起来像真电脑：初始化基本硬件、准备好给操作系统用的接口，然后把控制权交给系统。

这段程序就是固件。Proxmox VE 官方手册把它讲得很直白：

> "In order to properly emulate a computer, QEMU needs to use a firmware. Which, on common PCs often known as BIOS or (U)EFI, is executed as one of the first steps when booting a VM. It is responsible for doing basic hardware initialization and for providing an interface to the firmware and hardware for the operating system."

——固件在启动的最早阶段执行，负责基本硬件初始化，并为操作系统提供访问固件与硬件的接口。[^c1-L2-1]

三个关键点从这句话里拆出来：

1. **它最早执行**：比操作系统早，比引导加载程序也早。所以它出问题，现象一定是「还没进系统就卡住」——黑屏、停在某个菜单、报找不到引导设备。这决定了第六章排错时的观察窗口。
2. **它做硬件初始化**：虚拟机里这块是模拟出来的，固件选择会连带影响「这台虚拟机对外呈现成什么机器」——包括后面会讲到的机型（q35 / i440fx）、显卡直通能力。
3. **它提供接口**：操作系统后续通过固件留下的接口读时间、读设备信息。Proxmox 手册在同一章举过一个具体例子：Windows 期望 BIOS 时钟用本地时间，Unix 系期望用 UTC，所以创建虚拟机时要选对 OS 类型，PVE 才能优化这些底层参数。[^c1-L2-1]

> [!tip] 大白话：把固件想成「开机自检员 + 前台」
> 你进一栋大楼，先有个人检查水电、把灯打开（硬件初始化），再告诉你去几楼找谁（提供接口）。这个人就是固件。
> 所以：**固件坏了或者配置不对，你连大厅都进不去**，后面「找哪个房间」的事根本无从谈起。你在排错时看到的所有「进不去系统」，都要先在「前台」这一层找原因。

#### 固件在虚拟机里长什么样：三个看得见的落点

抽象地说「固件」容易飘。落到你实际能点、能看的界面，它其实是三个具体的产物：

| 产物 | 存在哪里 | 谁读它 | 换固件模式后会不会跟着变 |
| --- | --- | --- | --- |
| 固件程序本体 | 平台自己带（VMware 内置、PVE 的 pve-edk2-firmware 包等），你不直接接触 | 虚拟机启动时的第一个执行者 | 会换（换的就是它） |
| 分区表（MBR / GPT） | **客户机虚拟磁盘**的头部扇区 | 固件 | **不会变**——这是问题的根源 |
| 引导项 / 引导顺序记录 | UEFI 侧在 NVRAM（EFIVARS）；PVE 用一块单独的 EFI Disk 存 boot order | 固件 | 不会自动重建 |
| ESP（EFI 系统分区） | 客户机磁盘上的一个分区，里面放 `.efi` 引导程序 | UEFI 固件 | Legacy 模式下这个分区不被使用 |

这张表是本章的骨架。后面几节会逐格展开。

> [!tip] 大白话：把固件想成「换锁的门禁系统」
> 换了门禁系统（固件），但楼里的房间编号规则（分区表）没换、员工卡（引导项）也没重办。
> 所以：**换固件不会顺手帮你改造楼里的结构**，这正是「切完 UEFI 就起不来」的官方解释（第 3 节）。

---

### 2. 选项只有两个，但每个厂商叫法不同

VMware 官方文档把客户机固件类型限定为两项，没有第三个：

| 选项 | 官方原文描述 |
| --- | --- |
| UEFI | "UEFI is an interface between the operating system and the platform firmware. UEFI has architectural advantages over Basic Input/Output System (BIOS) firmware." |
| Legacy BIOS | "Standard BIOS firmware." |

[^c1-L1-1]

注意这里有个信息量很大的细节：**VMware 官方对「UEFI 比 BIOS 好在哪」的全部说明，就是「架构上有优势」这半句**。它没有给任何「什么场景该选哪个」的建议，只给了选择 UEFI 的前置条件（第 3 章会逐条列）。所以——

> **推理（非官方结论）**：本章和第二章里凡属「什么场景推荐选谁」的判断，都不是 VMware 官方说的，而是我们依据各来源条件归纳出来的。VMware 官方只给条件与警告。[^c1-L1-1]

再看 PVE 侧的措辞。同样是这两个选项，PVE 用的是不同的名字：

> "By default QEMU uses **SeaBIOS** for this, which is an open-source, x86 BIOS implementation. SeaBIOS is a good choice for most standard setups."

——PVE 默认使用 SeaBIOS，一个开源的 x86 BIOS 实现；官方称它适合大多数标准配置。[^c1-L2-1]

于是三套术语指的是同一件事，第一次见很容易以为是三种东西：

| 平台 | 「旧模式」叫什么 | 「新模式」叫什么 | 界面上在哪选 |
| --- | --- | --- | --- |
| VMware Workstation | Legacy BIOS | UEFI | Settings → Options → Advanced → Firmware type |
| Proxmox VE | SeaBIOS（`bios=seabios`） | OVMF（`bios=ovmf`） | 虚拟机硬件设置里的 BIOS 选项 |
| Hyper-V | 第 1 代虚拟机 | 第 2 代虚拟机 | 创建时就定，之后不可改 |
| VirtualBox | BIOS（默认） | EFI（手册章节名 Alternative Firmware，主干版已改称 UEFI） | 虚拟机 Settings 中启用 EFI，或命令行切换 |

> 说明：VMware 的字段名与其官方文档口径见 [^c1-L1-1]；PVE 的 `bios=seabios` / `bios=ovmf` 取值与默认值见 [^c1-L2-1]；Hyper-V 的代次绑定见 [^c1-GEN12]；VirtualBox 的默认值与「EFI/BIOS」两种叫法见 [^c1-L1-2]（6.0 手册，章节标题为 Alternative Firmware (EFI)）与 [^c1-L1-3]（主干手册，章节标题已改为 Alternative Firmware (UEFI)）。

一个必须记住的词：**SeaBIOS 是「BIOS 的一种实现」，OVMF 是「UEFI 的一种实现」**。你在 PVE 文档里看到 OVMF，在 VMware 文档里看到 UEFI，说的是同一类东西。

> [!tip] 大白话：把固件想成「同一份说明书的不同译本」
> Legacy BIOS = BIOS = SeaBIOS = Hyper-V 第 1 代，四个名字一个东西；UEFI = EFI = OVMF = Hyper-V 第 2 代，也是四个名字一个东西。
> 所以：**看到陌生名词先别慌，先归类到「旧」还是「新」**。真正要判断的从来只有这一个二选一。

---

### 3. 两种模式真正的分界线：固件与分区表是绑死的

这是本章最重要的一节，也是你「选 UEFI 总出问题」最可能的病根。

Broadcom 官方知识库有一篇专门讲这个故障的文章，标题就是《Virtual Machine fails to boot when changing the Firmware from BIOS to EFI》。它的 Cause 段落写道：

> "This is an expected behavior as changing the firmware is not supported since BIOS uses **MBR (Master Boot Record)** partitioning and EFI requires **GPT (GUID Partition Table)** partitioning on the VM disks. While changing the Firmware, a warning is also displayed that the installed guest operating system might become unbootable."

——改固件不受支持；BIOS 使用 MBR 分区，EFI 要求 GPT 分区；切换时界面会警告已安装的客户机系统可能变得无法启动。[^c1-L3-1]

请逐句读这句话，它有三个层次：

1. **绑定关系**：BIOS ↔ MBR，EFI ↔ GPT。不是「推荐搭配」，是要求。
2. **官方定性**：切完起不来是 **expected behavior**（预期行为），不是 bug，所以别指望厂商修复或给补丁。
3. **切换不会转换分区表**：文章给的解法是「重建虚拟机后挂原盘」或「切 EFI **前**先把磁盘转成 GPT」——两个解法都指向同一个事实：**切换动作本身不会动你的分区表**。[^c1-L3-1]

把这条绑定的后果做成表格：

| 你的操作 | 磁盘现状 | 结果 |
| --- | --- | --- |
| 一直是 Legacy BIOS 从没改过 | MBR | 正常 |
| 一直是 UEFI 从没改过 | GPT | 正常 |
| Legacy → UEFI，装完系统后改 | 仍是 MBR | **预期无法启动**（固件要 GPT，但盘上还是 MBR）[^c1-L3-1] |
| UEFI → Legacy，装完系统后改 | 仍是 GPT | 同样失败（原文覆盖双向："from BIOS to EFI or from EFI to BIOS"）[^c1-L3-1] |

> [!tip] 大白话：把分区表想成「楼里的房间编号规则」
> 老楼按「房间号 + 一条走廊索引」排（MBR），新楼要求按「全局唯一编号 + 一份完整目录」排（GPT）。
> 换了新的楼管（固件），可是楼的编号规则没动——新楼管拿着新规则去查号码，一个都对不上，于是直接宣布「这楼我管不了」。
> 所以：**固件模式和分区表是同一个决定的两半，必须在新建虚拟机时一次定好**。这也是为什么第二章会把「创建时就定死，别装完再改」单独拎出来讲。

#### Legacy 侧的分区表细节：本轮素材没有覆盖

上面这条官方原文只说了「BIOS 使用 MBR」，**没有**逐步描述 Legacy 从 MBR 到引导扇区的完整链路。所以：

> **推理**：Legacy 模式下固件读 MBR 分区表、再跳到活动分区的引导扇区去执行引导代码——这个机制属于通用常识补齐，本轮 16 个来源中没有明文覆盖。
> **缺口**：MBR 分区表的结构细节（主分区上限、扩展分区等）本章不展开，本轮素材只在 MBR→GPT 转换那个场景里提到过「MBR 分区表最多三个主分区」这一条限制，且那属于转换工具的约束，不是分区表本身的完整描述。[^c1-MBR2GPT]

---

### 4. UEFI 的启动链路：它到底在找什么

理解了「UEFI 要 GPT」，还要理解「UEFI 要的是一块**特定分区**」。这是第二条最容易踩空的地方。

Proxmox VE 的官方 wiki 有一页专门讲 OVMF 引导项，开头三句话就把整条链路说完了：

> "If a VM boots via OVMF (UEFI), the firmware has to know which bootloader it has to start from the ESP. When no boot entries exist in the EFIVARS store, it tries to load the fallback `$ESP/EFI/BOOT/BOOTX64.efi` loader. Should that also fail, the VM gets booted into the EFI Shell"

——如果虚拟机通过 OVMF (UEFI) 启动，固件必须知道该从 ESP 里启动哪个引导加载程序；当 EFIVARS 存储里没有引导项时，它会尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`；如果这也失败，虚拟机会被引导进入 EFI Shell。[^c1-L2-3]

> 层级说明：这一页是 Proxmox VE 的**官方 wiki**，不是参考手册（reference documentation）。它描述的是操作手法与机制说明，正式程度低于 `pve-docs` 手册，引用时请按此对待。[^c1-L2-3]

把这句话画成链路图：

```mermaid
flowchart TD
    A[固件启动<br/>UEFI/OVMF] --> B{EFIVARS 里有<br/>boot entry 吗?}
    B -- 有 --> C[按 boot entry 指向的路径<br/>从 ESP 加载 bootloader]
    B -- 没有 --> D[尝试回退路径<br/>$ESP/EFI/BOOT/BOOTX64.efi]
    D -- 成功 --> C
    D -- 失败 --> E[进入 EFI Shell<br/>停在命令行]
    C --> F[bootloader 接管<br/>加载操作系统]
```

同一件事用纯文本再写一遍，方便你复制到别处：

```text
UEFI 启动查表顺序
  1. 查 EFIVARS 里的 boot entry  →  有则按它指的路走
  2. 无 boot entry  →  试回退路径 $ESP/EFI/BOOT/BOOTX64.efi  →  成功则继续
  3. 回退也失败  →  落到 EFI Shell（一个停在命令行的界面）
```

这条链路上有三个名词需要落实：

| 名词 | 是什么 | 在链路上的角色 | 来源 |
| --- | --- | --- | --- |
| **ESP**（EFI System Partition） | 客户机磁盘上的一个分区，存放 `.efi` 引导程序 | 所有 UEFI 引导程序的存放地 | [^c1-L2-3] [^c1-L3-3] |
| **boot entry** | 固件记在 EFIVARS 里的一条「去哪个分区的哪个路径找哪个程序」的记录 | 首选路径；缺失就退回第 2 步 | [^c1-L2-3] |
| **EFI Shell** | 回退也失败时落到的命令行环境 | 失败终点，也是人工修复入口 | [^c1-L2-3] |

这里有一个反直觉但极其重要的推论：**UEFI 不靠「磁盘第一个扇区」找系统，它靠「一条记录 + 那个记录指向的文件在不在」**。所以当你在第六章看到「找不到引导程序」，根因几乎总是这两件事之一——记录丢了，或者 ESP（记录指向的分区）没了。Microsoft 的排错文档把第二件事说得很直接：

> "If the EFI System Partition (ESP) has been deleted or is missing, the VM cannot locate the UEFI boot loader and startup will fail."

——如果 EFI 系统分区被删除或缺失，虚拟机无法定位 UEFI 引导加载程序，启动将失败。[^c1-L3-3]

> [!tip] 大白话：把 boot entry 想成「前台桌上的访客预约本」
> 你（固件）去前台找一位访客（引导程序）。前台先翻预约本（EFIVARS 里的 boot entry）：有，就按上面写的房间号去找。
> 预约本上没有，前台按备用规则去一个固定房间碰运气（`$ESP/EFI/BOOT/BOOTX64.efi`）。
> 还是没人，前台就把你晾在一个空房间里站着——**这个空房间就是 EFI Shell**。
> 所以：**停在 EFI Shell 不代表系统坏了，只代表「预约本上没有、备用房间也是空的」**。对应到实操，就是去补一条预约记录（第六章的 Add Boot Option）。

#### Legacy 与 UEFI 的链路对照

| | Legacy BIOS | UEFI |
| --- | --- | --- |
| 分区表要求 | MBR | GPT [^c1-L3-1] |
| 引导程序放在哪 | MBR 的引导扇区（**推理**，本轮无明文） | ESP 分区里的 `.efi` 文件 [^c1-L2-3] |
| 固件怎么找到它 | 读磁盘固定位置（**推理**） | 读 EFIVARS 记录 → 回退固定路径 [^c1-L2-3] |
| 找不到时的表现 | 本轮素材未覆盖（**缺口**） | 进入 EFI Shell [^c1-L2-3] |
| 有无 Secure Boot | 无此机制 | 有（见下节） |

表格中标「推理」与「缺口」的两行，本轮来源确实没有给出，请不要在需要精确引用的场合（比如给别人解释、写工单）把这两行当作官方说法。

---

### 5. Secure Boot：UEFI 独有的一道额外检查

这是 UEFI 一侧独有的机制，也是「选 UEFI 后出问题」的高频来源：启动时多了一道签名检查。

> "Secure Boot verifies the boot loader is signed by a trusted authority in the UEFI database."

即验证引导加载程序是否由 UEFI 数据库中的受信机构签名。[^c1-GEN12] 被检查的还包括 UEFI 驱动（option ROM）：官方称它阻止未经授权的固件、操作系统或 UEFI 驱动在启动时运行，并在第 2 代虚拟机中默认启用。[^c1-GEN2SEC] VMware 侧口径一致，措辞是拒绝加载未使用「可接受数字签名」的驱动与系统加载器。[^c1-L1-1]

| 问题 | 答案 |
| --- | --- |
| 谁被检查 | 引导加载程序、UEFI 驱动、option ROM [^c1-GEN2SEC] |
| 不通过怎么办 | 官方明确：签名不正确时须为该虚拟机**关闭 Secure Boot** [^c1-GEN12] |
| 默认开还是关 | Hyper-V 第 2 代默认启用 [^c1-GEN2SEC]；PVE 加 `pre-enrolled-keys=1` 也默认启用，仍可在虚拟机内关闭 [^c1-L2-1] |
| Legacy 一侧 | 没有对应机制 |

> **推理**：自签名驱动、第三方 option ROM、非主流发行版引导程序是高风险对象——由「只放行名单内对象」推出；本轮素材无官方针对性结论。

> [!tip] 大白话：把 Secure Boot 想成「安检名单」
> 名单上有你名字才放行（受信签名），没有就一律拦下。
> 所以：**开 Secure Boot 后起不来，先怀疑「引导程序在不在名单上」**，而不是「系统坏了」。不在名单上，官方给的处置就是关掉它——这是官方许可的做法，不是「绕过安全」。

---

### 6. Hyper-V 最短对照：代次就是固件

按范围界定，Hyper-V 只作简短对照。它值得记的机关是：**固件选择被包装成「虚拟机代次」，而代次创建后不可更改**。[^c1-GEN12]

官方用设备替换表表达这层等价关系，其中一行是：

| Generation 1 Device | Generation 2 Replacement | Generation 2 Enhancements |
| --- | --- | --- |
| Legacy BIOS | UEFI firmware | Secure Boot |

即「第 1 代 = Legacy BIOS，第 2 代 = UEFI firmware」是官方用对照表给出的等价关系，而非一句否定式声明。[^c1-GEN12]

另有一条容易误解的说明：第 2 代虚拟机的虚拟固件**独立于宿主机上装的是什么**。[^c1-GEN12] 这解释了为什么在宿主机 BIOS 里折腾 Secure Boot 对客户机固件模式毫无影响。宿主侧开启虚拟化（如 VT-x）属既有笔记 [[虚拟机/虚拟机的概念和使用.md]] 的范围。

> [!tip] 大白话：把 Hyper-V 代次想成「买车时选油车还是电车」
> 不是「买回来再改」，是下单那一刻就定了（官方明文：代次创建后不可更改）。
> 所以：**Hyper-V 没有「装完再切固件」这个选项**，这最直观地印证了本章的核心结论——固件模式是新建虚拟机时的决定。

---

### 7. 一个容易读错的词：「MBR」的两种含义

这一节是术语提醒，属于**推理归纳**，不是任何来源的明文。

同一个词 `MBR`，在本轮的两份来源里指的是不同的东西：

- **来源 L3-1（Broadcom KB）** 用 MBR 指**纯 MBR 分区方案**——即 "BIOS uses MBR (Master Boot Record) partitioning"，是与 GPT 并列的另一种分区方式。[^c1-L3-1]
- **来源 L3-3（Microsoft 排错文档）** 里的 `gdisk` 输出，在一块**GPT 磁盘**上打印出 `MBR: protective`：

```text
Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Found valid GPT with protective MBR; using GPT.
```

[^c1-L3-3]

也就是说，GPT 磁盘上**也存在**一个 MBR——它是保护性 MBR（protective MBR），一个防止老工具误判的兼容外壳。

> **推理**：既然 GPT 磁盘也带 MBR 外壳，那么把 L3-1 那句读成「GPT 磁盘上没有 MBR」就是误读。两处说法不冲突，冲突的是「MBR」这个缩写在两种语境下的所指。本轮来源都未对此做术语声明，这条归纳由我们完成。

> [!tip] 大白话：把 `MBR: protective` 想成「新楼门口挂的一块旧牌子」
> 新楼用的是全新的门牌系统（GPT），但门口仍挂了一块老牌子（保护性 MBR），上面写着「这栋楼不要再按老方法查了」。
> 所以：**看到老字样不等于用的是老方案**。判断一块盘到底是 MBR 还是 GPT，要看 `GPT: present` 这类实质信息，不能看见 "MBR" 三个字母就下结论。

---

### 8. 本章明确的缺口：CSM

有一件事本章**刻意不写**，需要你知道原因，以免日后发现笔记里没提而以为漏了：

> **缺口**：CSM（Compatibility Support Module，兼容性支持模块，通常被描述为「让 UEFI 能引导 Legacy 系统的兼容层」）在**本轮 16 个来源中零命中**——没有任何一份来源提到它。因此本笔记**不给 CSM 的任何定义、行为或配置结论**。
> 如果你在某个平台的界面上看到 CSM 相关的选项，本笔记目前无法就该选项的含义或该不该开提供引用支持。补齐需要回到资料收集阶段补充来源。

---

### 本章小结

- **固件是虚拟机启动时执行的第一段代码**，负责基本硬件初始化并为操作系统提供接口；它出问题的现象必然是「进系统之前就卡住」。它只有两个模式，但有多套名字：Legacy BIOS = BIOS = SeaBIOS = Hyper-V 第 1 代；UEFI = EFI = OVMF = Hyper-V 第 2 代。[^c1-L2-1] [^c1-L1-1] [^c1-GEN12]
- **固件与分区表绑死**：BIOS 用 MBR、EFI 要 GPT；改固件不受支持，切完无法启动被官方定性为**预期行为**，且切换**不会**转换分区表。[^c1-L3-1]
- **UEFI 的查找顺序**：EFIVARS 里的 boot entry → 回退 `$ESP/EFI/BOOT/BOOTX64.efi` → 都不行就落到 EFI Shell。ESP 被删或缺失，就会「找不到 UEFI 引导加载程序」。[^c1-L2-3] [^c1-L3-3]
- **Secure Boot 是 UEFI 独有的签名检查**，拦的是引导加载程序、UEFI 驱动与 option ROM；签名不被接受时，官方许可的处置是关闭 Secure Boot。[^c1-GEN12] [^c1-GEN2SEC] [^c1-L1-1]
- **本章的推理与缺口**（引用时勿当官方结论）：「什么时候推荐选谁」的场景判断（推理）、Legacy 侧的引导链路细节（推理）、`MBR` 一词的两种含义归纳（推理）、CSM（零命中缺口）。

既然固件模式在创建虚拟机时就定死了，而且它牵连着分区表、ESP 和引导项——那下一个问题自然就是：**什么情况下必须选 UEFI，什么情况下用默认的 Legacy 反而更省事？** 下一章给出一张可以照着查的决策表，每条判断都标明依据与来源层级。

---

[^c1-L1-1]: **L1-1** · VMware Workstation Pro — Configure a Firmware Type（官方文档）· https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/25H2/using-vmware-workstation-pro/using-virtual-machines-in-workstation-pro-user-guide/starting-virtual-machines/configure-a-firmware-type.html
[^c1-L1-2]: **L1-2** · Oracle VirtualBox 用户手册 6.0 — 3.14 Alternative Firmware (EFI)（官方文档）· https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html
[^c1-L1-3]: **L1-3** · VirtualBox 手册主干源文件 — Alternative Firmware (UEFI)（官方文档，master 分支）· https://raw.githubusercontent.com/VirtualBox/virtualbox/refs/heads/main/doc/manual/en_US/dita/topics/efi.dita
[^c1-L2-1]: **L2-1** · Proxmox VE Administration Guide — QEMU/KVM Virtual Machines（官方参考手册，v9.2.11）· https://pve.proxmox.com/pve-docs/chapter-qm.html
[^c1-L2-3]: **L2-3** · Proxmox VE Wiki — OVMF/UEFI Boot Entries（官方 wiki 层级，oldid=12527）· https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries
[^c1-L3-1]: **L3-1** · Broadcom KB 384912 — Virtual Machine fails to boot when changing the Firmware from BIOS to EFI（官方知识库）· https://knowledge.broadcom.com/external/article/384912/
[^c1-L3-3]: **L3-3** · Microsoft Learn — Troubleshoot UEFI boot failures with Azure Linux images（官方排错文档）· https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/azure-linux-vm-uefi-boot-failures
[^c1-GEN12]: **GEN12** · Microsoft Learn — Should I create a generation 1 or 2 virtual machine in Hyper-V?（官方文档）· https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v
[^c1-GEN2SEC]: **GEN2SEC** · Microsoft Learn — Hyper-V Generation 2 Virtual Machine Security Features（官方文档）· https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/learn-more/Generation-2-virtual-machine-security-settings-for-Hyper-V
[^c1-MBR2GPT]: **MBR2GPT** · Microsoft Learn — MBR2GPT.EXE（官方文档）· https://learn.microsoft.com/en-us/windows/deployment/mbr-to-gpt

---

概念层到此结束：固件、分区表、引导项这三节链条已经对齐。下面进入决策层——把「选哪个」从技术细节变成一组可以照着查、并且标明来源层级的判断规则。

## 第二章：什么时候必须用 UEFI —— 选型决策

第一章的结论是：固件模式在创建虚拟机那一刻就定死了，而且它牵连着分区表、ESP 和引导项。那么问题就变成——**那一刻，怎么定？**

这一章只解决这一件事：给出一张可以照着查的决策表，每行都标明依据和来源层级。同时也会明确标出哪些说法**没有**来源支持——因为选型上最常见的错误不是选错，而是把某篇博客的推荐当成了官方要求。

---

### 1. 先看出厂默认值：三家平台的取向并不一致

在你做任何判断之前，先知道平台自己默认选了什么，因为这反映了厂商认为的「大多数情况」。

| 平台 | 默认固件 | 官方对默认值的表述 | 来源层级 |
| --- | --- | --- | --- |
| Proxmox VE | SeaBIOS | "By default QEMU uses **SeaBIOS**… SeaBIOS is a good choice for most standard setups." | 官方参考手册 [^c2-L2-1] |
| VirtualBox | BIOS | "By default, … uses the BIOS firmware for virtual machines."（用 EFI 需在 Settings 里启用） | 官方手册 [^c2-L1-3] |
| VMware Workstation | — | 官方**未声明**默认值，也未给任何场景建议 | 官方文档（缺口）[^c2-L1-1] |
| Hyper-V | 不适用（由代次决定） | "We recommend you create a generation 2 virtual machines to take advantage of features like Secure Boot unless one of the following statements is true" | 官方文档 [^c2-GEN12] |

两个值得注意的点：

1. **Proxmox VE 与 VirtualBox 的出厂默认都是旧模式**，且两家都用「适合大多数情况」这类措辞为默认值背书。
2. **Hyper-V 是反向的**：官方直接推荐第 2 代（即 UEFI），只在三种例外下才建议第 1 代——使用已存在的、与 UEFI 不兼容的预构建虚拟硬盘；第 2 代不支持你要跑的系统；第 2 代不支持你要用的引导方式。[^c2-GEN12]

这不是谁对谁错，而是三种不同的产品取向。你只需要记住一点：**「平台默认是 Legacy」这件事本身就是一条选型信号**——它意味着若你没有特殊需求，默认值大概率是对的。

> [!tip] 大白话：把默认值想成「餐馆的招牌菜」
> 厨师把这道菜放在菜单第一行，说明点它的人最多、翻车概率最低。
> 所以：**没有特殊忌口就点招牌菜**。想吃辣的（Windows 11、Secure Boot、直通）再换——下面第 3 节就是那张「忌口清单」。

---

### 2. 本轮最有价值的一条官方判据

如果你只记一句话，记这句。Proxmox VE 官方手册在系统设置一节给出了本轮唯一一句直接回答「何时该换 UEFI」的官方判据：

> "In most cases you want to switch from the default SeaBIOS to OVMF only if you plan to use PCIe passthrough."

——多数情况下，只有当计划使用 PCIe 直通时，才需要从默认的 SeaBIOS 换到 OVMF。[^c2-L2-1]

这句话的价值有三层：

1. **它是官方给的「换」的条件**，不是社区经验、不是博客建议；
2. **它用的是 "in most cases … only if"，把范围收得很窄**——不是「有好处就换」，而是「没直通就别换」；
3. **它反过来确认了默认值是正确的**。

直通场景的完整成套条件，官方在 PCI 直通文档里给全了：

| 项目 | 官方结论（原文片段） | 来源 |
| --- | --- | --- |
| 机型 | GPU 直通最佳兼容组合使用 `q35`（"best compatibility is reached when using 'q35'"） | [^c2-L2-4] |
| 固件 | 同上组合使用 OVMF（"OVMF" ("UEFI" for VMs)）而非 SeaBIOS | [^c2-L2-4] |
| 接口 | 同上组合使用 PCIe（"instead of PCI"）；且 "PCIe passthrough is only available on q35 machines" | [^c2-L2-4] |
| 显卡自身 | 若用 OVMF 直通 GPU，GPU 必须有 UEFI-capable ROM，**否则官方要求 "otherwise use SeaBIOS instead"** | [^c2-L2-4] |
| 普通 PCI 直通 | PCI 直通在 i440fx 与 q35 上都可用 | [^c2-L2-4] |

最后两行是这套条件里最容易被忽略的反转：**直通并不自动等于「换 UEFI」**。如果你的显卡没有 UEFI-capable 的 ROM，官方给的动作是改用 SeaBIOS——等于回到默认值。所以「我要做直通」不足以推出「我要换 UEFI」，还要看显卡。

> [!tip] 大白话：把这条判据想成「医生开的检查单」
> 医生不会让你把全身检查都做一遍，只会为某一个具体症状开单子（有直通需求 → 换 OVMF）。
> 所以：**换固件要有具体理由，而这个理由是「某项功能必须要它」**，不是「新的应该更好」。

---

### 3. 六条硬性触发条件

把散落在各来源里的条件集中起来，只有下面六条是**能逐条回源**的。命中任意一条，固件模式就不再是可选项，而是被客户机系统倒逼的硬性要求。

| # | 触发条件 | 官方依据 | 来源 | 层级 |
| --- | --- | --- | --- | --- |
| ① | 客户机是 **Windows 11** | 系统固件要求 "**UEFI, Secure Boot capable**"；另需 "TPM … version 2.0" | [^c2-L1-4] | official |
| ② | 需要 **Secure Boot** | Secure Boot 只存在于 UEFI 固件类型下（VMware 侧前置即「虚拟机使用 UEFI 固件类型」） | [^c2-L1-1] [^c2-L2-1] | official |
| ③ | 需要 **PCIe / GPU 直通** | PVE "only if you plan to use PCIe passthrough"；直通组合要求 q35 + OVMF + PCIe | [^c2-L2-1] [^c2-L2-4] | official |
| ④ | 客户机是 **Arm** | VirtualBox "**All Arm VMs require UEFI.**"；PVE arm64 主机上 "bios=ovmf is the only supported setting"，因 SeaBIOS 仅支持 x86 | [^c2-L1-3] [^c2-L2-1] | official |
| ⑤ | 需要 **Hyper-V 第 2 代语义** | 第 2 代 = UEFI firmware + Secure Boot；代次创建后不可更改 | [^c2-GEN12] | official |
| ⑥ | **客户机系统自身宣告只支持 UEFI 启动** | PVE：部分系统（如 Windows 11）可能需要 UEFI 实现，此时 "**you must use OVMF instead**" | [^c2-L1-4] [^c2-L2-1] | official |

几条使用说明：

- **① 与 ⑥ 是同一件事的两种表述**：① 是把 Windows 11 这个具体系统写死进表，⑥ 是把它抽象成「以客户机系统的要求为准」。实践中按 ⑥ 理解更稳——因为将来会有别的系统提出同样要求。
- **④ 是最「无条件」的一条**：Arm 客户机上不存在选择余地，`bios=ovmf` 是唯一受支持设置。[^c2-L2-1]
- **② 的成本最低、也最容易误触发**：很多人为了「更安全」打开 Secure Boot，却没先确认引导程序是否在受信签名之内（第一章第 5 节）。它不是免费的。

> [!tip] 大白话：把这六条想成「必须走人工窗口的情形」
> 平时自助机就能办（默认 Legacy），只有六种特殊情况才必须去人工窗口（UEFI）。
> 所以：**先对照这六条，一条都不沾就别换**；沾了就别犹豫——因为这时候「选不选」已经不由你决定了。

---

### 4. 决策表（本章主产物）

下面这张表是本章的成品。用法：从你的场景出发，找到对应行；「依据」列告诉你为什么，「层级」列告诉你这条有多硬。

| 场景 | 选谁 | 依据 | 来源与层级 |
| --- | --- | --- | --- |
| 没想好、也没有特殊需求 | **Legacy / SeaBIOS** | 平台默认值，官方称适合大多数标准配置 | official [^c2-L2-1] [^c2-L1-3] |
| 客户机是 Windows 11 | **UEFI + Secure Boot capable + TPM 2.0**，PVE 侧 "you must use OVMF instead" | 系统硬性要求 | official [^c2-L1-4] [^c2-L2-1] |
| 需要 Secure Boot | **UEFI** | Secure Boot 的前置条件就是固件类型为 UEFI | official [^c2-L1-1] |
| 需要 PCIe / GPU 直通 | **UEFI（OVMF）**，机型 q35；但显卡无 UEFI-capable ROM 时改用 SeaBIOS | 官方直通判据与组合要求 | official [^c2-L2-1] [^c2-L2-4] |
| 客户机是 Arm | **UEFI**，唯一可选 | 平台限制，无选择余地 | official [^c2-L1-3] [^c2-L2-1] |
| 新建 Hyper-V 虚拟机 | **第 2 代** | 官方推荐，三种例外除外 | official [^c2-GEN12] |
| PVE 上要加 vTPM / TPM 2.0 | 社区实践写作「机型 q35 + BIOS OVMF」 | 社区来源明确列为前提；**官方未声明该前提** | **community，勿当官方口径** [^c2-L2-5] |
| 新虚拟机一律上 UEFI、SeaBIOS 只留给 legacy 系统 | （社区主张） | 社区实践取向 | **community，取向与官方默认不同** [^c2-L2-5] |
| 客户机磁盘是已存在的、不兼容 UEFI 的预构建虚拟硬盘 | **Legacy（第 1 代）** | Hyper-V 官方列出的例外之一 | official [^c2-GEN12] |
| 想「反正新的更好」就先换了 | **别换** | 官方对所有场景建议**保持沉默**；超出上述触发条件的推荐无来源支持 | **推理，非官方结论** [^c2-L1-1] |

**关于最后一行的说明（重要的推理标注）**：VMware 官方文档对「UEFI 比 Legacy BIOS 好在哪」的全部说明只有一句「UEFI 在架构上有优势」，**没有给出任何选型场景建议**。因此凡属超出上文六条触发条件的场景推荐，都是我们的归纳，不是官方口径。[^c2-L1-1]

> [!tip] 大白话：把这张表想成「体检指标参考范围」
> 化验单上每项都有「参考范围」和「异常提示」，医生不会因为数值「更新」就给你开药。
> 所以：**照着列查，命中就用，没命中就守默认**。「来源与层级」那一列就是这张表可信度的标尺——写着 community 或推理的行，别拿去当规矩压人。

---

### 5. 口径并列：社区主张 vs 官方默认

决策表里有两行来源是社区。这里把它们的原话摆出来，让你看清分歧的性质。

社区来源在《Proxmox VE 上的虚拟机最佳实践配置》里写道：

> "For new VMs, we use **OVMF (UEFI)** provided that the guest operating system supports it. SeaBIOS should only be used for legacy systems or older operating system versions, but it is not strictly necessary."

——对新虚拟机，只要客户机系统支持，他们就使用 OVMF (UEFI)；SeaBIOS 只应用于 legacy 系统或较老的操作系统版本，**但并非严格必须**。[^c2-L2-5]

> **层级说明**：这条来自 community 层级来源（第三方技术文章），不是 Proxmox 官方文档。引用时必须让读者看出这一层级差别。

对照一下官方口径：PVE 官方说默认 SeaBIOS、多数情况只有做 PCIe 直通才需要换。[^c2-L2-1]

两者的关系需要精确描述：

- **不是直接互斥**：官方说「默认 SeaBIOS」，社区说「我们用 OVMF」——两边都没有禁止对方的选择。社区那句甚至还自带 "but it is not strictly necessary"（并非严格必须），等于承认这不是硬性要求。
- **是取向不同**：官方站在「默认值要照顾大多数、减少复杂度」的位置；社区站在「提前按现代标准配置、避免将来迁移」的位置。
- **落到你身上怎么用**：这条社区观点可以作为「如果你已经决定要用 UEFI，不必有心理负担」的支撑，但**不能**作为「所以新虚拟机都该上 UEFI」的官方依据。

---

### 6. 大容量引导盘：必须分层写，不能合并成一条通用结论

「系统盘超过 2TB 就必须用 UEFI」是流传很广的一条说法。本轮素材要求把它拆成两层写，因为两层证据强度完全不同。

**第一层：跨平台的通用结论——没有。**

> **缺口**：本轮 16 个来源中，没有任何一份给出「跨平台通用的、系统盘大于某个容量就必须用 UEFI」的官方结论。因此本笔记**不给出**这样的通用口径。

**第二层：Hyper-V 侧有可直接引用的官方硬数据。**

Hyper-V 官方在「使用第 2 代虚拟机的优势」下，以 **Larger boot volume** 为标题列出了明确数字：

| 代次 | 固件 | 最大引导卷 |
| --- | --- | --- |
| 第 2 代 | UEFI firmware | **64 TB**（`.VHDX` 支持的最大磁盘大小） |
| 第 1 代 | Legacy BIOS | **2 TB**（`.VHDX`）/ **2040 GB**（`.VHD`） |

[^c2-GEN12]

引用这一条时必须连带说明：**这是 Hyper-V 的引导卷上限，不是通用结论**。它说明的是 Hyper-V 产品在这一项上的能力边界，不能被外推成「所有平台的 UEFI 都能突破 2TB」或「所有平台的 Legacy 都限于 2TB」。

> [!tip] 大白话：把这两层想成「厂家说明书」和「坊间经验」
> 说明书上写着某型号最大载重 64 吨（Hyper-V 的 64 TB），这是可查的；坊间说「所有卡车都能拉 64 吨」，那是没依据的。
> 所以：**引用容量数字时，一定要连厂家和型号一起说**。只说「UEFI 支持 64TB」，等于把 Hyper-V 的规格安到了别的平台上。

---

### 7. 创建时就定死，别装完再改

这一节把第一章的结论转成一条可执行纪律。两家官方各给了一半依据：

| 依据 | 原文 | 来源 |
| --- | --- | --- |
| 装完之后改，可能把虚拟机改坏 | "Once a guest operating system is installed, changing the firmware type might cause the virtual machine boot process to fail." | [^c2-L1-1] |
| 根因是分区表不匹配，且切换不会转换分区表 | "changing the firmware is not supported since BIOS uses MBR … and EFI requires GPT … partitioning on the VM disks"；官方定性为 expected behavior | [^c2-L3-1] |

三平台在这一点的可控性并不相同：

| 平台 | 创建后能否改固件 | 官方说法 |
| --- | --- | --- |
| VMware Workstation | 界面上**可以**改（要求客户机已关机），但官方警告可能导致启动失败 | [^c2-L1-1] |
| Hyper-V | **不可改** | 代次创建后不可更改 [^c2-GEN12] |
| Proxmox VE | **无明文** | 本轮素材既无支持证据也无反驳证据（**缺口**，见下） |

> **缺口**：PVE 的 `bios` 项创建后能否修改，本轮官方来源没有明文。这一点在第 5 章会再说明一次：社区「只能创建时设定」的说法**未被证实**，本笔记不写成结论。

所以纪律只有一句：**把它当作创建时的一次性决定来对待**。即使界面上那个下拉框是亮着可点的，也不代表点了没事。

> [!tip] 大白话：把改固件想成「装修到一半换承重结构」
> 房子盖好、家具进场之后（系统已安装），再去换承重墙的做法（分区表），施工队会直接叫停。
> 所以：**要改就趁没装系统时改；已经装好了，走「重建虚拟机 + 挂原盘」这条路**（处置细节见第六章）。

---

### 本章小结

- **默认值就是选型基线**：PVE 与 VirtualBox 出厂默认都是旧模式，官方称其适合大多数标准配置；Hyper-V 反向，官方推荐第 2 代。[^c2-L2-1] [^c2-L1-3] [^c2-GEN12]
- **本轮唯一的官方「何时该换」判据**：PVE 的 "only if you plan to use PCIe passthrough"。直通不等于必须换 UEFI——显卡没有 UEFI-capable ROM 时，官方要求改回 SeaBIOS。[^c2-L2-1] [^c2-L2-4]
- **六条硬性触发条件**：Windows 11、需要 Secure Boot、需要 PCIe/GPU 直通、客户机是 Arm、需要 Hyper-V 第 2 代语义、客户机系统自身宣告只支持 UEFI。命中就用，未命中就守默认。[^c2-L1-4] [^c2-L1-1] [^c2-L2-1] [^c2-L2-4] [^c2-L1-3] [^c2-GEN12]
- **社区取向要标层级**：社区主张新虚拟机用 OVMF、SeaBIOS 只留给 legacy 系统，属 community 层级，与官方默认口径取向不同而非互斥，且其原文自带「并非严格必须」。[^c2-L2-5]
- **大容量引导盘分两层**：跨平台的通用结论本轮素材没有（缺口）；Hyper-V 侧有官方硬数据（第 2 代 64 TB、第 1 代 2 TB/2040 GB），引用时必须注明这是 Hyper-V 的引导卷上限。[^c2-GEN12]
- **创建时就定死**：官方明文装后改可能导致启动失败，根因是分区表不匹配且切换不转换分区表。[^c2-L1-1] [^c2-L3-1]

选型结束了，下一步是把它落到具体界面上。三个平台的落地方式差别不小：VMware Workstation 是一页设置加两条前置条件，VirtualBox 有一个版本演进的坑，PVE 则多出一块必须额外创建的磁盘。接下来的三章按平台各讲一章，你可以只读自己实际在用的那个。

---
[^c2-L1-1]: **L1-1** · VMware Workstation Pro — Configure a Firmware Type（官方文档）· https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/25H2/using-vmware-workstation-pro/using-virtual-machines-in-workstation-pro-user-guide/starting-virtual-machines/configure-a-firmware-type.html
[^c2-L1-3]: **L1-3** · VirtualBox 手册主干源文件 — Alternative Firmware (UEFI)（官方文档，master 分支）· https://raw.githubusercontent.com/VirtualBox/virtualbox/refs/heads/main/doc/manual/en_US/dita/topics/efi.dita
[^c2-L1-4]: **L1-4** · Microsoft Learn — Windows 11 requirements（官方文档）· https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements
[^c2-L2-1]: **L2-1** · Proxmox VE Administration Guide — QEMU/KVM Virtual Machines（官方参考手册，v9.2.11）· https://pve.proxmox.com/pve-docs/chapter-qm.html
[^c2-L2-4]: **L2-4** · pve-docs 源文件 — PCI(e) Passthrough（官方文档，master 快照）· https://raw.githubusercontent.com/proxmox/pve-docs/master/qm-pci-passthrough.adoc
[^c2-L2-5]: **L2-5** · Starline — Best Practice Configurations for Virtual Machines on Proxmox VE（**community 层级**，第三方文章）· https://www.starline.de/en/magazine/technical-articles/best-practice-configurations-for-virtual-machines-on-proxmox-ve
[^c2-L3-1]: **L3-1** · Broadcom KB 384912 — Virtual Machine fails to boot when changing the Firmware from BIOS to EFI（官方知识库）· https://knowledge.broadcom.com/external/article/384912/
[^c2-GEN12]: **GEN12** · Microsoft Learn — Should I create a generation 1 or 2 virtual machine in Hyper-V?（官方文档）· https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v

