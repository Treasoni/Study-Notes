---

选型规则到这里就定完了，剩下的问题只剩「在哪个界面点哪里」。接下来的三章按平台分头落地——桌面端两个（VMware Workstation、VirtualBox）在前，服务器端（PVE）在后；三章之间没有依赖，可以只读你实际在用的那一章。

## 第三章：VMware Workstation 实操

第二章给出了决策表，但那张表是在纸上的。这一章把它落到 VMware Workstation 的界面上：入口在哪、选 UEFI 要满足哪些条件、选 Secure Boot 又要在那个条件之上再加什么、以及哪一步会让你后悔。

需要先交代一句：**本章没有命令**。VMware 官方关于固件类型的素材只有 GUI 入口、前置条件和警告，没有任何可写进笔记的命令行操作。所以本章全程是「点哪里、看什么、什么情况下点不动」——不虚构任何命令输出。

---

### 1. 入口：三个点击，一个下拉框

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

### 2. 想选 UEFI：四项前置条件，缺一不可

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

### 3. 想选 Secure Boot：在 UEFI 之上再加两项

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

### 4. 启用 VBS 时：两个选项都被锁死

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

### 5. 后果反例：装完系统再改，可能直接把虚拟机改废

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

### 6. 附：Windows 11 在 ESXi 上的落地清单

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

### 7. 已经装好系统了怎么办：迁移参考

如果虚拟机已经装好系统、而你现在必须用 UEFI，官方给的不是「改一下设置」，而是两条路：

| 路径 | 官方原文要点 | 来源 |
| --- | --- | --- |
| 重建虚拟机 | "Rebuild the VM by choosing EFI/BIOS as firmware and attach the same hard disks to it to make it bootable."（重建虚拟机、选定固件后挂原有硬盘） | [^c3-L3-1] |
| 先转分区表再切 | "Convert the VM's disks to GPT **before** switching to EFI"，可用 Windows 侧工具完成，且 "needs to be supported by Guest OS vendor"（需客户机系统厂商支持） | [^c3-L3-1] |

关键在先后的顺序：**转 GPT 必须在切 EFI 之前**，反过来做没有意义（切完就已经启动不了了）。第二条路的工具约束、可转与不可转的磁盘范围、以及不受支持的系统版本，属于第六章的迁移路径专节，本章不展开。

---

### 本章小结

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

---

VMware Workstation 是一页设置加两组前置条件，讲完就到另一款桌面虚拟化产品 VirtualBox——它在固件这件事上多了一层「同一份手册，不同版本说法不同」的读法，还有一个「勾了 EFI 却什么都不发生」的真实缺陷记录。

## 第四章：VirtualBox 实操

在 VirtualBox 里新建一台虚拟机，跟固件有关的开关只有一行；勾了之后，有时系统装到一半就卡住，有时干脆一片黑，连安装界面都不给。这一章要回答的就是三个具体问题：这个开关在哪、命令行怎么写、以及「勾了 EFI 反而起不来」到底是版本问题还是用法问题。

本章只讲 VirtualBox。术语沿用第 1 章术语表里的那一行：**BIOS = 默认固件 / UEFI = efi 固件**。在 VirtualBox 的语境里这不是泛称，而是同一个参数 `--firmware` 的两个合法取值。

---

### 4.1 默认是 BIOS，切 UEFI 有两条路

两个版本的官方手册都以同一句话开头：默认使用 BIOS 固件。

- 6.0 手册原文：`"By default, Oracle VM VirtualBox uses the BIOS firmware for virtual machines."` [^c4-L1-2]
- 主干手册原文：`"By default, ... uses the BIOS firmware for virtual machines."` [^c4-L1-3]

也就是说 VirtualBox 出厂就站在 Legacy 一侧，这与第 2 章决策表里「不命中硬性触发条件就用平台默认固件」的取向一致 —— 你不需要为了「跟上时代」而先去勾 UEFI。

> [!tip] 大白话
> 把默认固件想成新电脑出厂预装的那套系统：开机就能用，不动它是最省事的路线。VirtualBox 的出厂预装就是 BIOS，UEFI 属于「要用的时候才去换」的那一档。

切换到 UEFI 有两条路，效果等价。

#### 路线 A：GUI 勾选

6.0 手册把入口指向 Settings 对话框的 Motherboard 标签页（原文指向 `Section 3.5.1, "Motherboard Tab"`）[^c4-L1-2]；主干手册的措辞相同，也是「enable EFI in the machine's Settings」[^c4-L1-3]。

> **缺口**：两版手册的缓存正文都只给到「Settings → Motherboard 页」这一层，没有给出复选框的原文文案。所以本章不写界面上的具体字样，请你以本机版本实际勾选项为准（位置就在 Motherboard 页的扩展特性区域一带）。

#### 路线 B：命令行

两条命令的形式在 6.0 与主干手册中完全一致 [^c4-L1-2][^c4-L1-3]：

```bash
# 切换为 EFI 固件；"win11" 是虚拟机名，换成 VBoxManage list vms 里列出的那个名字
VBoxManage modifyvm "win11" --firmware efi

# 切回默认的 BIOS 固件
VBoxManage modifyvm "win11" --firmware bios
```

- `"VM name"` 这个占位符在手册原文里就是 `"VM name"` [^c4-L1-2]，指的是你在 VirtualBox 管理器左侧列表里看到的名称（带引号是因为名称里可能有空格）。
- 取值只有 `efi` 与 `bios` 两个，分别对应 GUI 里的勾选与不勾选。

| 你要的结果 | 命令行取值 | GUI 对应动作 | 出处 |
| --- | --- | --- | --- |
| 用 UEFI 固件 | `--firmware efi` | Motherboard 页启用 EFI | 6.0 手册 / 主干手册 [^c4-L1-2][^c4-L1-3] |
| 用默认 BIOS 固件 | `--firmware bios` | Motherboard 页不启用 EFI | 同上 |

**为什么值得学命令行这条路**（推理）：GUI 的勾选状态藏在多层设置面板里，事后要确认「这台到底是哪种固件」得一层层点进去；`--firmware` 这一项可读可写，脚本化建机、批量核对、把配置写进你自己的建机记录时都不依赖界面。这一条是本章的归纳，不是手册原话。

> **缺口**：本轮素材没有给出「读取当前固件设置」的命令（例如 `showvminfo` 那一类），所以本章不写读取侧的命令，核对时请回 GUI 的 Motherboard 页看勾选状态。
>
> **另需注意**：`VBoxManage modifyvm` 是否要求虚拟机关机执行，6.0 与主干手册本节均未写明。按 `modifyvm` 的一般惯例应当先关机，但这属于（推理），操作前请自行确认。

---

### 4.2 定位随版本变过：6.0 说「实验性」，主干已不提

这是本章最需要小心的一节。同一份官方手册，两个版本的措辞不一样，引用时**必须带版本号**。

| 对比项 | 6.0 手册 [^c4-L1-2] | 主干手册 [^c4-L1-3] |
| --- | --- | --- |
| 小节标题 | Alternative Firmware (**EFI**) | Alternative Firmware (**UEFI**) |
| 定位措辞 | `"includes experimental support for the Extensible Firmware Interface (EFI)"` | `"includes support for the Unified Extensible Firmware Interface (UEFI)"` |
| 是否出现 experimental | 出现 | 全节不再出现 |
| 默认固件 | BIOS | BIOS（未变） |
| 切换命令 | `--firmware efi` / `--firmware bios` | 完全相同 |
| 客户机范围表述 | 「Mac OS X、Linux 和较新的 Windows 已知可用」；Windows 7 例外 | 新增 `"Most modern macOS and Windows releases require UEFI. All Arm VMs require UEFI."` |
| 另一用途 | 开发测试 EFI 应用 | 开发测试 UEFI 应用 |

两条引用纪律，请跟着记：

1. **不要说「7.x 手册说 EFI 是实验性的」。** `experimental` 这个词只出现在 6.0 手册。本轮素材能支持的表述只有：「6.0 手册标注为实验性支持，主干同节已不再出现该措辞」。
2. **不要把主干说成某个具体版本号。** 主干是开发分支的源文件快照，不代表某个已发布版本的行为；引用时写「主干手册」，不要折算成版本号。

> [!tip] 大白话
> 「experimental」就像厂家在功能旁边写的那行小字「试用中，可能还会改」。新版文档把这三个字擦掉了，说明它现在按正式功能对待了 —— 但这不等于它当年不是试用功能，也不等于某个具体版本号那天恰好擦了字。所以引用哪一版都得说清是哪一版。

**这三条主干表述值得单独记住**（都能回源到同一节 [^c4-L1-3]）：

- 多数现代 macOS 与 Windows 发行版需要 UEFI（`"Most modern macOS and Windows releases require UEFI"`）；
- **所有 Arm 虚拟机都需要 UEFI**（`"All Arm VMs require UEFI"`）—— 这条与第 2 章决策表里的 Arm 触发条件互为印证，只是这里是 VirtualBox 侧的口径；
- 除装系统外，UEFI 还能用于「不启动操作系统的 UEFI 应用开发与测试」。

---

### 4.3 6.0 手册记载的限制清单

下面四条**全部出自 6.0 手册的 3.14 节** [^c4-L1-2]。请把它们当作「6.0 时代的已知限制」读，不要当成当前版本的性能清单（原因见本节末尾）。

**① Windows 7 客户机无法在 EFI 下启动**

6.0 手册原文：`"Windows 7 guests are unable to boot with the Oracle VM VirtualBox EFI implementation."` 同一段还写明 Mac OS X、Linux 与较新的 Windows 已知可用。

**② 运行中的客户机内部无法操作 EFI 变量，替代做法是用 `setextradata`**

6.0 手册原文：`"It is currently not possible to manipulate EFI variables from within a running guest."` 手册举的例子是：在 Mac 客户机里用 `nvram` 工具设置 `boot-args` 不会生效。

替代路径是从宿主机侧写入：

```bash
# 从宿主机把 boot-args 的值塞进虚拟机配置；<value> 的具体取值语义由客户机系统决定
VBoxManage setextradata "win11" VBoxInternal2/EfiBootArgs <value>
```

- 命令形式与手册一致，手册原话是「`VBoxInternal2/EfiBootArgs` extradata can be passed to a VM in order to set the `boot-args` variable」[^c4-L1-2]。
- `<value>` 填什么由客户机系统决定 —— 手册给的场景是 macOS 的 `boot-args` [^c4-L1-2]，换了别的客户机系统，取值含义也随之不同。
- **机制解释（推理）**：既然客户机内部改不动这个变量，就把宿主机侧当作唯一的写入口，在虚拟机启动前把值写进它的配置里，固件启动时读这个值。手册只说明了「怎么做」，没有解释「为什么这样做能生效」，上面这句是本章的归纳。

> [!tip] 大白话
> 把 EFI 变量想成房间里的门禁设置：这间屋子有规定，人在屋里时改不了门禁，只能由机房在外面先把新设置贴上去。`setextradata` 就是那张从外面贴进去的纸条 —— 你人（客户机系统）还没进屋，纸条已经在那儿等着了。

**③ EFI 默认分辨率 1024x768，且只能在关机状态下改**

6.0 手册原文：`"The default resolution is 1024x768."` 以及 `"The EFI default video resolution settings can only be changed when the VM is powered off."` [^c4-L1-2]

修改用的也是 `setextradata`，形式同样出自 6.0 手册 3.14.1 节 [^c4-L1-2]：

```bash
# HxV 形式；下面给几个手册分辨率表里列的取值
VBoxManage setextradata "win11" VBoxInternal2/EfiGraphicsResolution 1280x1024
```

手册列出的可选值包括 `640x480`、`800x600`、`1024x768`（默认）、`1280x720`、`1280x1024`、`1600x900`、`1920x1080`、`2560x1440`、`3840x2160` 等 [^c4-L1-2]。手册还说：自定义分辨率需要显式指定色深，接受 8 / 16 / 24 / 32，EFI 默认按 32 位色深处理。

**④ EFI 提供 GOP 与 UGA 两种视频接口**

6.0 手册原文说明 EFI 有两个不同的视频接口 —— GOP（Graphics Output Protocol）与 UGA（Universal Graphics Adapter）：现代系统（如 Mac OS X）一般用 GOP，一些较老系统仍用 UGA；VirtualBox 给两者各提供一个分辨率配置项，因此对用户来说这个差别基本可以忽略 [^c4-L1-2]。

#### 为什么要把「6.0」标这么重

主干手册的同一节**一项限制都不列** [^c4-L1-3]，上面四条在主干里全部找不到。这是版本演进，不是同版本内的两处冲突（素材把这类情况归为「口径差异 · 版本差异」）。

⚠️ 所以看到别人贴「VirtualBox 的 UEFI 限制」清单时，第一个问题应该是：**哪一版手册的？** 本章给的这四条，请一律带「6.0」两个字引用。

---

### 4.4 一个真实的「勾了 EFI 却什么都不发生」：ticket #18282

这是一个**社区层级**（community）的缺陷报告，不是官方文档；下面的时间线请连着读，否则很容易误当成当前版本的问题。

**现象**（报告者原文）：`"If the Graphics Controller is not set as a VBoxVGA, and a bootable medium is not provided, then the EFI shell never comes up."` —— 图形控制器不是 VBoxVGA、且没有提供可引导介质时，EFI Shell 始终不出现。报告者随后补充实际比「看不到 Shell」更糟：`"no booting happens"`、`"No booting, no go"`。同一报告还记录：选了 VMSVGA 时，`VBoxInternal2/EfiGopMode`、`VBoxInternal2/EfiGraphicsResolution`、`VBoxInternal2/EfiHorizontalResolution`、`VBoxInternal2/EfiVerticalResolution` 这些 ExtraData **全部被忽略**，分辨率退回 `640x480` [^c4-L3-5]。

**根因**（开发者 Klaus Espenlaub 的解释，原文）：`"as of today there's no graphics driver in the EFI firmware which handles VMSVGA or VBoxSVGA."` —— 当时的 EFI 固件里**没有**能驱动 VMSVGA 或 VBoxSVGA 的图形驱动；VBoxSVGA 因为与 VBoxVGA 大体兼容，做起来工作量有限，VMSVGA 则更费事 [^c4-L3-5]。

**时间线** [^c4-L3-5]：

| 时间 | 事件 |
| --- | --- |
| 2019-01-04 | 报告提交；同日补充「完全不启动」、并把标题改为「No installation is possible.」 |
| 2019-01-07 | 开发者给出上述根因解释 |
| 2019-02-15 | 开发者称最新 6.0 testbuild 应已修复（VBoxSVGA 与 VMSVGA 两条路径都修） |
| 2019-02-15 | 报告者确认：`"Confirmed as fixed with version 6.0.5 r128870"`，测试环境为 Win10-64 客户机配 VBoxSVGA、Ubuntu 18.10 客户机配 VMSVGA |
| 2019-04-17 | ticket 关闭，Resolution 记为 `fixed` |

⚠️ **别误读**：这是 **2019 年、6.0.5 之前**的缺陷，早已修复。今天用较新版本不会遇到这一条。它值得留在笔记里的原因是**机制**（推理）：EFI Shell 是固件自己画出来的界面，图形控制器没有对应驱动时固件画不出来，你看到的就是一片黑 —— 这类「黑屏但没有任何报错」的现象，根因往往在图形路径而不是引导路径，排查方向完全不同。

**规避建议（推理，非官方结论）**：用 6.0.5（`r128870`）及以上版本；若因故必须留在更老的版本，避开「图形控制器不是 VBoxVGA + 没有可引导介质」这个组合 —— 例如先挂好安装 ISO 再开机，或临时把图形控制器换回 VBoxVGA。

> [!tip] 大白话
> 这就像投影仪没装驱动：电脑本身跑得好好的，墙上却什么都投不出来。EFI Shell 是「投在墙上」的画面，图形控制器是那台投影仪 —— 投影仪没驱动，你只会看到黑墙，不会看到任何错误提示。所以「黑屏不报错」要往图形那一侧找，而不是以为虚拟机没启动。

---

### 4.5 本章明确不写的内容（缺口）

按本章素材覆盖情况，以下几处**本轮无法取证**，所以不写结论，也请不要用别处看到的说法自行补齐：

1. **VirtualBox 7.2 的 `VBoxManage modifynvram` 与 Secure Boot 密钥管理**：本轮 4 个 VirtualBox 来源（6.0 手册、主干手册、ticket #18282 及来源表其余项）全部零命中，官方页面是否存在也未确认。本章因此完全不涉及这两项。
2. **GUI 复选框的原文文案**：两版手册缓存都只到 Motherboard 页这一层（见 4.1）。
3. **「读取当前固件设置」的命令**：本轮素材未提供（见 4.1）。
4. **`modifyvm --firmware` 是否要求关机执行**：本节两版手册均未写明（见 4.1）。
5. **6.0.5 修复之后，该限制在新版手册中的现状**：6.0 手册的限制清单在主干里整段不存在，因此无法从手册侧确认 ticket 那条缺陷的当前表述，只能依据 ticket 自身的 `fixed` 标记 [^c4-L3-5]。这是素材覆盖的边界，不是「问题仍存在」的意思。

---

### 本章小结

- **VirtualBox 默认固件是 BIOS**，6.0 与主干手册口径一致；切换到 UEFI 用 GUI 的 Motherboard 页，或 `VBoxManage modifyvm "VM name" --firmware efi`，切回用 `--firmware bios`。
- **引用 VirtualBox 手册的结论必须带版本**：`experimental` 只在 6.0 手册出现，主干同节标题已改为 Alternative Firmware (UEFI) 且不再提这个词；主干不是一个版本号。
- **6.0 手册的四条限制**（Windows 7 无法在 EFI 下启动、运行中客户机无法操作 EFI 变量、默认分辨率 1024x768 且仅关机可改、GOP/UGA 两种视频接口）在主干手册中一条都没有，属于版本演进。
- **EFI 变量改不动时，用宿主机侧的 `setextradata "VM name" VBoxInternal2/EfiBootArgs <value>`** 写入；分辨率用 `VBoxInternal2/EfiGraphicsResolution HxV`，两者都出自 6.0 手册。
- **ticket #18282 是 2019 年、6.0.5 已修复的社区报告**，不要当作当前版本的问题；它留下的有效知识是「黑屏无报错要先怀疑图形路径」。

下一章进入 PVE：同样是从默认固件切到 UEFI，但 PVE 侧多了一个 VirtualBox 没有的强制配套动作 —— UEFI 必须配一块 EFI Disk（`efidisk0`），磁盘的 `efitype` 与 `pre-enrolled-keys` 还会直接决定 Secure Boot 能不能用；机型（q35 / i440fx）与固件的耦合也是 PVE 独有的一层。

---

[^c4-L1-2]: **L1-2** · Oracle VM VirtualBox User Manual for Release 6.0 — 3.14. Alternative Firmware (EFI) · https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html
[^c4-L1-3]: **L1-3** · VirtualBox 手册主干源文件（master 分支）— Alternative Firmware (UEFI) · https://raw.githubusercontent.com/VirtualBox/virtualbox/refs/heads/main/doc/manual/en_US/dita/topics/efi.dita
[^c4-L3-5]: **L3-5（community 层级）** · VirtualBox ticket #18282 — EFI shell not shown when VMSVGA or VBoxSVGA is chosen. No installation is possible. => fixed in svn · https://www.virtualbox.org/ticket/18282

