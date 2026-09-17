# 第三章：VMware Workstation 实操

第二章给出了决策表，但那张表是在纸上的。这一章把它落到 VMware Workstation 的界面上：入口在哪、选 UEFI 要满足哪些条件、选 Secure Boot 又要在那个条件之上再加什么、以及哪一步会让你后悔。

需要先交代一句：**本章没有命令**。VMware 官方关于固件类型的素材只有 GUI 入口、前置条件和警告，没有任何可写进笔记的命令行操作。所以本章全程是「点哪里、看什么、什么情况下点不动」——不虚构任何命令输出。

---

## 1. 入口：三个点击，一个下拉框

官方给出的操作路径是三步：

1. 在 Workstation Pro 界面中打开 **Settings**；
2. 点 **Options** 标签，再点 **Advanced**；
3. 在 **Firmware type** 区域进行选择。[^c3-L1-1]

对应的界面路径就是 **Settings → Options → Advanced → Firmware type**。这个区域里只有第一章讲过的两个选项：**UEFI** 与 **Legacy BIOS**，没有第三个。[^c3-L1-1]

操作前有两条官方前提，都写在文档开头：

| 官方前提 | 原文 | 含义 |
| --- | --- | --- |
| 客户机必须关机 | "To change the firmware type of an existing virtual machine, the guest operating system is powered off." | 不能热改，必须断电后再进设置 [^c3-L1-1] |
| 选项可见性有条件 | "If the guest operating system is supported and the prerequisites are met, the following firmware types are selectable." | **条件不满足时选项可能根本不可选**，不是灰掉了事 [^c3-L1-1] |

第二条是本章后半段的主线：为什么有的人打开这个界面只有一项、或者 UEFI 选不动——因为**下拉框的可选性由前置条件决定**。下面逐层拆。

> [!tip] 大白话：把这个下拉框想成「药店的处方药柜台」
> 柜台里摆着两种药（UEFI / Legacy BIOS），但其中一种要凭处方（前置条件）才卖。
> 所以：**选项点不动不是软件坏了，是你的「处方」没齐**。别急着重装 Workstation，先对照下一节的条件。

---

## 2. 想选 UEFI：四项前置条件，缺一不可

官方明确列出了选 UEFI 必须满足的四项条件：

| # | 前置条件（官方原文） | 通俗理解 |
| --- | --- | --- |
| ① | "The guest operating system to be installed on the virtual machine supports UEFI firmware." | 你要装的系统本身得支持 UEFI |
| ② | "The virtual machine does not have virtualization-based security (VBS) enabled." | 虚拟机未启用 VBS（基于虚拟化的安全） |
| ③ | "The virtual machine uses hardware version 8 or later." | 硬件版本 ≥ 8 |
| ④ | "The virtual machine has a Windows 8, Windows 10, Windows 2012, or Windows 2016 guest operating system." | 客户机系统是 Windows 8 / 10 / 2012 / 2016 |

[^c3-L1-1]

逐条说明，尤其是落地时容易卡住的地方：

- **① 是「系统层」条件**：由你打算装的操作系统决定，不是 Workstation 能帮你补的。
- **② 是「配置层」条件**：VBS 是 Windows 侧的一项安全功能。注意它与下一节的机制有关联，先记住「启用 VBS 会改变这个下拉框的行为」。
- **③ 是「虚拟机版本号」条件**：每台虚拟机有一个 hardware version（硬件版本），新建时选定。这是四项里最容易在旧虚拟机上卡住的一项。
- **④ 是四项里最值得注意的一项**：官方把 UEFI 的客户机系统范围**写死在这四个 Windows 版本上**。这个范围明显偏窄——它没有提 Linux、没有提更新的 Windows、也没有提 macOS。

关于 ③ 和 ② 具体在界面的哪里看，以及 ④ 之外的系统是否可行：

> **缺口**：本轮 Workstation 官方来源只列出这四个条件，**未给出**查看 hardware version 的具体界面路径，也**未说明**条件 ④ 之外的操作系统（如 Linux、macOS）在 Workstation 上选 UEFI 会怎样。本笔记不补写这两处。

关于 ④ 的偏窄范围，还有一处需要留意的口径差异：

> **口径差异（非冲突）**：Workstation 官方把 UEFI 客户机范围限定在上述四个 Windows 版本 [^c3-L1-1]；而 VirtualBox 官方手册的表述是「多数现代 macOS 与 Windows 版本需要 UEFI」。这是两家厂商各自的范围声明，宽窄不一，不构成对同一事实的对立结论。VirtualBox 侧的具体表述见第四章。

> [!tip] 大白话：把这四项想成「优惠券的使用门槛」
> 满减券要满足起送价、指定门店、指定时段、指定商品——少一条就用不了。
> 所以：**四项条件是 AND 关系，不是 OR**。别看到自己满足了三条就以为能选。

---

## 3. 想选 Secure Boot：在 UEFI 之上再加两项

Secure Boot 不是与 UEFI 并列的第三个选项，而是 **UEFI 的下级选项**。官方的表述是「如果你想选择 UEFI Secure Boot，验证以下条件满足」，共两项：

| # | 前置条件（官方原文） |
| --- | --- |
| ① | "The virtual machine uses the UEFI firmware type." |
| ② | "The virtual machine uses hardware version 14 or later." |

[^c3-L1-1]

把这套层级关系画出来会更直观：

```text
Legacy BIOS ────────────────► 到此为止，没有下级选项

UEFI ──┬── 需要四项前置（系统支持 / 未启用 VBS / 硬件版本 ≥ 8 / 指定的 Windows 版本）
       │
       └── UEFI Secure Boot ──┬── 需要 UEFI 固件类型（上位条件，必须先满足）
                              └── 需要硬件版本 ≥ 14
```

这里有一个落地时最容易踩的数字陷阱：

| 你的硬件版本 | 能选 UEFI 吗 | 能选 Secure Boot 吗 |
| --- | --- | --- |
| 8 ≤ 版本 < 14 | 能（满足 ③） | **不能**——Secure Boot 要 ≥ 14 [^c3-L1-1] |
| ≥ 14 | 能 | 能 |

也就是说，「我明明能选 UEFI，为什么 Secure Boot 是灰的」这个常见疑问，答案通常就是硬件版本卡在 8 到 13 之间。

> **推理**：上述用「灰掉」描述界面表现，是按前置条件不满足时的常规交互推断的；官方原文只写「验证条件是否满足」与「可选性由条件决定」，没有逐项描述具体控件的禁用样式。本节表格的结论（版本区间与可选性的对应关系）由官方两条版本下限直接得出，不属推理；仅「灰掉」这一界面描述属推理。

> [!tip] 大白话：把 Secure Boot 想成「大楼里的内部门禁」
> 你得先进大楼（选上 UEFI），才能走到那扇内门（Secure Boot）；而进内门还要更高一级的权限（硬件版本 ≥ 14）。
> 所以：**Secure Boot 报错时先回头看固件类型选上了没**——上位条件没满足，内门根本不会开。

---

## 4. 启用 VBS 时：两个选项都被锁死

这一节讲第 2 节条件 ② 的另一面。官方在注意事项里写了两句：

> "If VBS is enabled, the firmware type is set to UEFI and the UEFI Secure Boot option is selected."
> "You cannot edit the firmware type or the UEFI Secure Boot setting when VBS is enabled."

——若启用 VBS，固件类型会被设为 UEFI 并勾选 UEFI Secure Boot；且在启用 VBS 期间，**这两项都无法编辑**。[^c3-L1-1]

这里有两点值得琢磨：

1. **VBS 是「强制升级」而非「禁止升级」**：一旦启用 VBS，固件会被自动顶到 UEFI + Secure Boot，而不是被拦住。
2. **顶上去之后你失去控制权**：两项都不可编辑，说明你既改不回 Legacy BIOS，也关不掉 Secure Boot。

这和上一节的条件 ②（「选择 UEFI 时要求虚拟机未启用 VBS」）读起来像矛盾，需要说清楚：

> **推理**：同一页文档里，一处把「未启用 VBS」列为**手动选择 UEFI 的前置条件**，另一处又写明**启用 VBS 时固件类型会被自动设为 UEFI**。这两句可以这样理解——前者约束的是「你手动去选」这个动作，后者描述的是「VBS 强制配置」这条路径；两者作用对象不同，因此不必然冲突。但**官方未对此做任何解释**，本笔记不把它当作已解决的结论。落到实操上有一条无争议的推论：如果你的虚拟机启用了 VBS，那它的固件模式已经不由你决定了。

> [!tip] 大白话：把 VBS 想成「装修队接手后收回钥匙」
> 装修队（VBS）进场后会自动把房子改成它要的样子（固件设为 UEFI + Secure Boot），改完把钥匙收走，你进不去操作面板了。
> 所以：**动固件设置之前先确认 VBS 的状态**——它开着的话，你在那一页的改动可能根本无效，或者那条路径压根轮不到你手选。

---

## 5. 后果反例：装完系统再改，可能直接把虚拟机改废

官方在这一页给了一句很重的警告：

> "Once a guest operating system is installed, changing the firmware type might cause the virtual machine boot process to fail."

——一旦客户机操作系统已安装，更改固件类型**可能导致虚拟机启动过程失败**。[^c3-L1-1]

这句话要和第一章的机制连起来读，才能理解为什么它用 "might" 而不是绝对语气：

| 层次 | 说明 | 来源 |
| --- | --- | --- |
| 界面层面 | 下拉框是可点的（客户机已关机即可改） | [^c3-L1-1] |
| 官方警告 | 装完系统再改，**可能**导致启动过程失败 | [^c3-L1-1] |
| 机制层面 | 因为 BIOS 用 MBR、EFI 要 GPT，而切换**不会**转换分区表 | [^c3-L3-1] |
| 官方定性 | 切换固件后无法启动属 **expected behavior**（预期行为），不受支持 | [^c3-L3-1] |

「可点」和「该点」是两件事。官方之所以用 "might"，是因为如果客户机磁盘恰好是匹配的分区表，改完可能没事；但一旦不匹配，就落进那条「预期行为」里——不受支持、没有补丁、只能走重建或转 GPT 两条路。

具体处置（重建虚拟机后挂原盘、或切 EFI 前先把磁盘转 GPT 且需客户机系统厂商支持）见第六章。[^c3-L3-1]

> [!tip] 大白话：把这句警告想成「开车时换挡」
> 挡杆是能推动的（下拉框可点），但车速不对时推它，变速箱就打坏了。
> 所以：**能改 ≠ 该改**。官方都写「可能导致启动失败」了，就把它当成创建时的一次性决定来对待。

---

## 6. 附：Windows 11 在 ESXi 上的落地清单

> [!warning] 适用范围先看清：这一节讲的是 **ESXi 7.x / 8.x**，不是 Workstation
> 这一节的来源是一篇 Broadcom 知识库文章，其标题即《Windows 11 Installation Fails on ESXi 7.0U3》，Environment 一栏标注 **ESXi 7.x**，处置段落也明确写的是 "when deploying a Windows 11 VM on **ESXi 7.0U3**"。[^c3-L1-5]
> 也就是说，下面的清单**不能直接照搬到 VMware Workstation**。把它放在本章的理由是：它是本轮素材里唯一一份把「Windows 11 客户机需要什么固件相关配置」讲完整的官方清单；而 Workstation 侧的 Windows 11 要求，本轮 Workstation 官方来源（L1-1）**没有覆盖**。

该文给出的完整清单如下（原文为编号列表）：

| # | 项目 | 官方要求（原文要点） |
| --- | --- | --- |
| 1 | VM Hardware Compatibility | 使用 "hardware version 14 or later" |
| 2 | Firmware Type | "Set to **EFI**"——原文特别加注 "this is VMware's term for UEFI" |
| 3 | Secure Boot | "**Must be enabled** in VM settings" |
| 4 | vTPM（虚拟 TPM） | Windows 11 必需；"This needs VM encryption, which in turn requires a Key Management Server (KMS)" |
| 5 | RAM | 最低 4 GB（推荐 8 GB 以上） |
| 6 | Storage | 最低 64 GB 虚拟磁盘 |
| 7 | ISO | 使用微软官方 Windows 11 ISO |

[^c3-L1-5]

三点解读：

- **第 2 条解释了一个术语困惑**：VMware 界面上写的是 **EFI**，而本文档正文里说 UEFI——两者是同一个东西，官方自己在这篇里做了注释。[^c3-L1-5]
- **第 4 条是这条链上最容易被低估的一环**：Windows 11 要 vTPM，vTPM 要虚拟机加密，加密要 KMS。三者是串联的，缺一环整条链就断。原文的 Additional Information 还给出了补救路径：若因缺少加密支持而无法添加 vTPM，需在 vCenter 中配置 KMS 以启用虚拟机加密。[^c3-L1-5]
- **第 1 / 3 条与本章前几节可以对应上**：硬件版本 ≥ 14 正是 Secure Boot 的门槛（第 3 节），而 Secure Boot 必须以 UEFI 为上位条件。

客户机系统侧还有两条平行的官方要求，来自微软自己的 Windows 11 要求页：物理设备要求是 "System firmware: **UEFI, Secure Boot capable**" 与 "TPM … **version 2.0**"；虚拟机场景下则写 "Generation: **2**"，并要求 Hyper-V 场景下 "Secure boot capable, virtual TPM enabled"，并附注 "**In-place upgrade of existing generation 1 VMs to Windows 11 isn't possible.**"（已存在的第 1 代虚拟机无法就地升级到 Windows 11）。[^c3-L1-4]

> **缺口**：本轮来源**没有**给出 VMware Workstation 上安装 Windows 11 的固件相关要求清单。Workstation 侧可直接引用的，只有「选 UEFI 的四项前置」与「选 Secure Boot 的两项前置」（本章第 2、3 节）。如果你要在 Workstation 上装 Windows 11，本笔记目前只能给到这些，无法给出该平台专属的 vTPM / 加密路径说明。

> [!tip] 大白话：把这份清单想成「办签证的材料清单」
> 护照、照片、流水、机票，缺一样就退回重办；而且不同国家的清单不能混用。
> 所以：**这份清单是「ESXi 国」的，别拿去「Workstation 国」递签**。但清单的骨架（固件要 EFI、Secure Boot 必开、vTPM 要加密）是通用的参照。

---

## 7. 已经装好系统了怎么办：迁移参考

如果虚拟机已经装好系统、而你现在必须用 UEFI，官方给的不是「改一下设置」，而是两条路：

| 路径 | 官方原文要点 | 来源 |
| --- | --- | --- |
| 重建虚拟机 | "Rebuild the VM by choosing EFI/BIOS as firmware and attach the same hard disks to it to make it bootable."（重建虚拟机、选定固件后挂原有硬盘） | [^c3-L3-1] |
| 先转分区表再切 | "Convert the VM's disks to GPT **before** switching to EFI"，可用 Windows 侧工具完成，且 "needs to be supported by Guest OS vendor"（需客户机系统厂商支持） | [^c3-L3-1] |

关键在先后的顺序：**转 GPT 必须在切 EFI 之前**，反过来做没有意义（切完就已经启动不了了）。第二条路的工具约束、可转与不可转的磁盘范围、以及不受支持的系统版本，属于第六章的迁移路径专节，本章不展开。

---

## 本章小结

- **入口是三步**：Settings → Options → Advanced → **Firmware type**，只有 Legacy BIOS 与 UEFI 两项；改之前客户机必须已关机，且选项可见性本身由前置条件决定。[^c3-L1-1]
- **选 UEFI 要四项条件同时满足**：客户机系统支持 UEFI、未启用 VBS、硬件版本 ≥ 8、客户机为 Windows 8/10/2012/2016。[^c3-L1-1]
- **选 Secure Boot 要在 UEFI 之上再加两项**：固件类型已是 UEFI（上位条件）、硬件版本 ≥ 14。硬件版本落在 8–13 时会出现「UEFI 能选、Secure Boot 不能选」。[^c3-L1-1]
- **启用 VBS 会锁死这两项**：固件被自动顶为 UEFI 并勾选 Secure Boot，且两项均不可编辑；这与「选 UEFI 要求未启用 VBS」的表述关系，官方未作解释（本章标为推理）。[^c3-L1-1]
- **装完系统再改固件可能导致启动过程失败**，官方定性为预期行为、不受支持；处置只有「重建虚拟机挂原盘」或「先转 GPT 再切 EFI」两条路。[^c3-L1-1] [^c3-L3-1]
- **Windows 11 落地清单的来源是 ESXi 7.x/8.x，不是 Workstation**，照搬前务必留意适用范围；Workstation 侧的 Windows 11 专属要求本轮素材未覆盖（缺口）。[^c3-L1-5]

VMware 侧的操作面比较干净：一页设置、两组条件、一句警告。VirtualBox 侧则不同——它有一处随版本演进的「定位变化」，还有一个具体的、有 ticket 记录的失败模式。下一章讲 VirtualBox 时，你会看到「同一份手册的不同版本说法不一样」这个问题该怎么读。

---
[^c3-L1-1]: **L1-1** · VMware Workstation Pro — Configure a Firmware Type（官方文档）· https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/25H2/using-vmware-workstation-pro/using-virtual-machines-in-workstation-pro-user-guide/starting-virtual-machines/configure-a-firmware-type.html
[^c3-L1-4]: **L1-4** · Microsoft Learn — Windows 11 requirements（官方文档）· https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements
[^c3-L1-5]: **L1-5** · Broadcom KB 408976 — Windows 11 Installation Fails on ESXi 7.0U3（官方知识库，**适用 ESXi 7.x/8.x，非 Workstation**）· https://knowledge.broadcom.com/external/article/408976/windows-11-installation-fails-on-esxi-70.html
[^c3-L3-1]: **L3-1** · Broadcom KB 384912 — Virtual Machine fails to boot when changing the Firmware from BIOS to EFI（官方知识库）· https://knowledge.broadcom.com/external/article/384912/
