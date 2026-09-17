# 第四章：VirtualBox 实操

在 VirtualBox 里新建一台虚拟机，跟固件有关的开关只有一行；勾了之后，有时系统装到一半就卡住，有时干脆一片黑，连安装界面都不给。这一章要回答的就是三个具体问题：这个开关在哪、命令行怎么写、以及「勾了 EFI 反而起不来」到底是版本问题还是用法问题。

本章只讲 VirtualBox。术语沿用第 1 章术语表里的那一行：**BIOS = 默认固件 / UEFI = efi 固件**。在 VirtualBox 的语境里这不是泛称，而是同一个参数 `--firmware` 的两个合法取值。

---

## 4.1 默认是 BIOS，切 UEFI 有两条路

两个版本的官方手册都以同一句话开头：默认使用 BIOS 固件。

- 6.0 手册原文：`"By default, Oracle VM VirtualBox uses the BIOS firmware for virtual machines."` [^c4-L1-2]
- 主干手册原文：`"By default, ... uses the BIOS firmware for virtual machines."` [^c4-L1-3]

也就是说 VirtualBox 出厂就站在 Legacy 一侧，这与第 2 章决策表里「不命中硬性触发条件就用平台默认固件」的取向一致 —— 你不需要为了「跟上时代」而先去勾 UEFI。

> [!tip] 大白话
> 把默认固件想成新电脑出厂预装的那套系统：开机就能用，不动它是最省事的路线。VirtualBox 的出厂预装就是 BIOS，UEFI 属于「要用的时候才去换」的那一档。

切换到 UEFI 有两条路，效果等价。

### 路线 A：GUI 勾选

6.0 手册把入口指向 Settings 对话框的 Motherboard 标签页（原文指向 `Section 3.5.1, "Motherboard Tab"`）[^c4-L1-2]；主干手册的措辞相同，也是「enable EFI in the machine's Settings」[^c4-L1-3]。

> **缺口**：两版手册的缓存正文都只给到「Settings → Motherboard 页」这一层，没有给出复选框的原文文案。所以本章不写界面上的具体字样，请你以本机版本实际勾选项为准（位置就在 Motherboard 页的扩展特性区域一带）。

### 路线 B：命令行

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

## 4.2 定位随版本变过：6.0 说「实验性」，主干已不提

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

## 4.3 6.0 手册记载的限制清单

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

### 为什么要把「6.0」标这么重

主干手册的同一节**一项限制都不列** [^c4-L1-3]，上面四条在主干里全部找不到。这是版本演进，不是同版本内的两处冲突（素材把这类情况归为「口径差异 · 版本差异」）。

⚠️ 所以看到别人贴「VirtualBox 的 UEFI 限制」清单时，第一个问题应该是：**哪一版手册的？** 本章给的这四条，请一律带「6.0」两个字引用。

---

## 4.4 一个真实的「勾了 EFI 却什么都不发生」：ticket #18282

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

## 4.5 本章明确不写的内容（缺口）

按本章素材覆盖情况，以下几处**本轮无法取证**，所以不写结论，也请不要用别处看到的说法自行补齐：

1. **VirtualBox 7.2 的 `VBoxManage modifynvram` 与 Secure Boot 密钥管理**：本轮 4 个 VirtualBox 来源（6.0 手册、主干手册、ticket #18282 及来源表其余项）全部零命中，官方页面是否存在也未确认。本章因此完全不涉及这两项。
2. **GUI 复选框的原文文案**：两版手册缓存都只到 Motherboard 页这一层（见 4.1）。
3. **「读取当前固件设置」的命令**：本轮素材未提供（见 4.1）。
4. **`modifyvm --firmware` 是否要求关机执行**：本节两版手册均未写明（见 4.1）。
5. **6.0.5 修复之后，该限制在新版手册中的现状**：6.0 手册的限制清单在主干里整段不存在，因此无法从手册侧确认 ticket 那条缺陷的当前表述，只能依据 ticket 自身的 `fixed` 标记 [^c4-L3-5]。这是素材覆盖的边界，不是「问题仍存在」的意思。

---

## 本章小结

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
