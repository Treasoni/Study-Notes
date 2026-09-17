---
title: ISO 与 IMG / raw / qcow2 镜像烧录/写盘方法对比
tags:
  - 镜像
  - 烧录
  - 写盘
  - ISO
  - IMG
  - raw
  - qcow2
  - 虚拟机
  - 软路由
created: 2026-09-09
updated: 2026-09-17
status: active
source_project: iso-img-flash-comparison
---

# ISO 与 IMG / raw / qcow2 镜像烧录/写盘方法对比

> [!note] 标题里的三个后缀
> 正文不加限定时，「**IMG**」指的是**磁盘镜像这一整类**，包含：
> - `.img`（及 `.img.gz` / `.img.xz` 压缩变体）
> - `.raw`
> - `.qcow2`
>
> 三者的共同点是「一整块盘」；**关键差异在于 `.img` / `.raw` 是「裸镜像」、`.qcow2` 是「容器格式」**，详见 [[#第二章 镜像结构差异 —— 为什么处理方式会不一样]]。

> [!info] 一句话结论
> ISO 与 IMG / raw / qcow2 的烧录/写盘**不能一概而论，要分两层看**：
> - **工具层**看工具——Etcher / `dd` 对 ISO 和 IMG / raw 一视同仁；Rufus 区分「ISO Image 模式 / DD 模式」；Ventoy 把镜像当文件、不烧录。
> - **流程层**看场景——ISO 无论物理机还是虚拟机都要**先进一遍安装器**；IMG / raw / qcow2 写入/导入**即启动**，没有安装向导这一站。
> - **`qcow2` 还多一道门槛**——`.img` / `.raw` 是裸盘，可以逐字节直接写；`.qcow2` 是 QEMU 容器格式，写物理盘前必须先用 `qemu-img convert -O raw` 拆成 raw。
>
> 概念区分见 [[iso和img.md]]（「概念篇」）；本文是它的「操作篇」。

## 目录

1. 第一章 一句话结论 —— ISO 与 IMG / raw / qcow2 烧录方法「分两层看」
2. 第二章 镜像结构差异 —— 为什么处理方式会不一样（含 IMG / raw / qcow2 三者关系）
3. 第三章 工具层对比 —— Etcher / Rufus / Ventoy / dd 对 ISO 与磁盘镜像的处理
4. 第四章 物理机两种刷机流程 —— IMG / raw 成品盘式 vs ISO 安装器式（qcow2 需先转换）
5. 第五章 虚拟机两种用法 —— ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入直启
6. 第六章 速查表、常见坑与延伸 —— 实操前必看

---

## 第一章 一句话结论 —— ISO 与 IMG / raw / qcow2 烧录方法「分两层看」

> 配套关系：[[iso和img.md]] 是「概念篇」，回答 ISO/IMG **是什么**；本篇是「操作篇」，只回答一个问题：**ISO 与 IMG / raw / qcow2 的烧录/写盘方法和操作，到底一不一样？**
>
> 答案是：**不能一概而论，要分两层看。**

> [!note] 一句话结论
> - **工具层**（用什么工具写）：取决于工具。Etcher / `dd` 对 ISO 和 IMG / raw 操作几乎一样；Rufus 区分两种模式；Ventoy 干脆不烧录，把镜像当文件；`.qcow2` 则是四类工具都不能直接写。
> - **流程层**（写完之后怎么用）：取决于场景。无论物理机还是虚拟机，**ISO 都要先进一遍安装器**才有系统；**IMG / raw / qcow2 写入/导入即启动**，没有安装向导这一站（`.qcow2` 只在虚拟机上享受这条待遇）。

---

### 第一层：工具层 —— 是否一样，看工具

同样是「把镜像弄到 U 盘/硬盘上」，不同工具对 ISO 与磁盘镜像（IMG / raw / qcow2）的态度截然不同，大致分三类：

| 工具 | 是否区分 ISO / 磁盘镜像 | 工作机制 | 详见 |
|---|---|---|---|
| balenaEtcher | 不区分 | 逐字节整盘写入，无模式可选 | 第三章 |
| `dd` | 不区分 | 块级「转换并拷贝」，同样不解析内容 | 第三章 |
| Rufus | 区分两种模式 | ISO Image mode（解包重建）vs DD Image mode（逐扇区直写）；`.img` 自动走 DD | 第三章 |
| Ventoy | 把两者都当「文件」 | 不烧录，拷入分区后由引导菜单启动 | 第三章 |

- **纯写盘器（Etcher / `dd`）对 ISO、IMG / raw 几乎无差别。** balenaEtcher 官方明确说它对镜像逐字节复制、不做任何转换，因此没有「模式」这回事，`.iso`、`.img` 还是 `.raw` 对它只是同一串字节。[balenaEtcher 官方文档](https://etcher-docs.balena.io/USER-DOCUMENTATION/) 反过来说：正因为不做转换，它依赖镜像自己可引导，像 Windows 这种需要特殊处理的 ISO 官方就建议改用 Rufus/WoeUSB。
- **Rufus 是「分得最清」的工具。** 官方 FAQ 把写盘分成两种策略：ISO Image mode 把 ISO 当作安装盘来「解包重建文件系统」；DD Image mode 把文件当作磁盘镜像「逐扇区直写」。遇到 `.img` 磁盘镜像它会自动走 DD。[Rufus 官方 Wiki FAQ](https://github.com/pbatard/rufus/wiki/FAQ) 所以同是 Rufus，写 ISO 和写 IMG 时界面上的选项不一样。
- **Ventoy 的哲学完全不同：不烧录。** 它把 ISO/IMG 当作普通文件放进 U 盘分区，由启动菜单来引导。普通发行版 ISO「拷贝即启动」，但 IMG 是整盘镜像，要让引导菜单直接启动它需要额外插件（`ventoy_openwrt.xz`），且只支持特定 OpenWrt 镜像 —— **不能默认 Ventoy 通吃所有 IMG**。[Ventoy 官方文档](https://www.ventoy.net/cn/doc_openwrt.html)
- **`.qcow2` 是个例外：四类工具都不能直接写。** 前三条说的都是「裸镜像」（`.iso` / `.img` / `.raw`，文件字节就是盘上字节）；`.qcow2` 是 QEMU 的**容器格式**，文件字节不是盘上字节，写盘工具拿到的只是「装盘的盒子」。要写物理盘，先转换（见 [[#qcow2：同一块盘，被装进了 QEMU 的「容器」]]）。

> [!tip] 大白话
> 把「逐字节写盘」想成**用刻录机原样复制一盘母带**——里面是歌还是程序它不关心，只保证每一个字节都对得上。所以 Etcher / `dd` 这类纯写盘器眼里，ISO、IMG、raw 没区别，反正都是「整盘照抄」。
>
> Rufus 则像一台**有两种刻录模式的机器**：ISO 模式会照着镜像「重新排版一张能引导的盘」，DD 模式才是「原样整盘照抄」。模式选错，结果天差地别——这就是工具层「为什么不能一概而论」的根源。
>
> 而 `.qcow2` 是**裹了包装的盘**：工具能把它搬走，但搬到 U 盘上铺不平。得先拆包装（`qemu-img convert`），这一步不属于「写盘」。

> [!warning] 一个高频误解
> 「Rufus 能写 `.img`，那 `.qcow2` 换个后缀改成 `.img` 不就行了？」
> **不行，而且更糟。** 改后缀只是改名字，文件内容还是容器格式 —— 写出来的盘第 0 扇区是 qcow2 文件头而不是分区表，固件读不懂，直接变砖。**必须真正转换**（`qemu-img convert`），不是重命名。

---

### 第二层：流程层 —— 是否一样，看场景

把镜像写进介质只是第一步；**写完之后能不能开机、要不要再装一遍**，才是用户最关心的差异。这一层与物理机/虚拟机无关，只取决于镜像本身是「安装介质」还是「成品盘」：

| 维度      | ISO（安装器式）                    | IMG / raw（成品盘式）                    |
| ------- | ---------------------------- | ---------------------------------- |
| 物理机     | 刻 U 盘 → 引导 → 走安装向导，系统现场装进目标盘 | 写 U 盘/内置盘 → 引导（必要时「复制到内置盘」）→ 直接进系统 |
| 虚拟机     | 挂虚拟光驱 → 从空盘引导安装器             | 导入为虚拟磁盘 → 开机即系统                    |
| 是否经过安装器 | **是，绕不开**                    | 否（最多是把自己整盘复制到目标盘）                  |
| 本质      | 引导安装程序的介质                    | 已经装好系统的磁盘克隆                        |

- **ISO 是「安装器式」。** 载体无论是物理 U 盘还是虚拟光驱，引导起来后进入的是一个**安装程序**，要经过语言、键盘、分区等向导，系统才被现场装进目标盘。Ubuntu 官方在 Windows 下用 Rufus 制作启动 U 盘的教程，走的就是这条路。[Ubuntu 官方教程](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
- **IMG / raw 是「成品盘式」。** 镜像本身就是一块完整系统盘（分区表 + 引导 + 文件系统都在里面）。物理机上把它整盘写入后即可引导进入系统，比如 iStoreOS 官方 X86 流程：下载 `.img.gz` 固件 → Rufus 写入 U 盘 → 目标机从 U 盘引导 → 在临时系统里用 quickstart 把固件写到内置盘 → 拔盘直启。[iStoreOS 官方文档](https://doc.linkease.com/zh/guide/istoreos/install_x86.html) 全程没有传统意义的安装向导。
- **`.qcow2` 只有在虚拟机里才享受同一条待遇。** 它是容器格式，物理机上必须先 `qemu-img convert -f qcow2 -O raw` 拆成裸镜像，之后才谈得上按 `IMG` 流程写盘；虚拟机里则可直接导入（PVE 的 `qm disk import` 要求「镜像格式必须被 `qemu-img` 支持」）。[Proxmox qm 手册](https://pve.proxmox.com/pve-docs/qm.1.html) 细节见 [[#qcow2：同一块盘，被装进了 QEMU 的「容器」]] 与第五章。

> [!tip] 大白话
> 把 ISO 想成**装修**：房子（目标盘）本来是毛坯，得让装修队（安装器）进场干一遍才能住。把 IMG / raw 想成**精装二手房**：拎包入住，把「钥匙」（写入/导入）拿到手就能开机。
>
> 所以流程层的规律是：**ISO 永远多一步「装系统」，IMG / raw 是「拿来即用」。** 这和你在物理机还是虚拟机上操作无关。
>
> `.qcow2` 像**打包好的精装二手房（只能走虚拟机这条内部通道）**：内部通道直达，物理机那条路它走不了，得先开箱。

---

### 为什么会有这两层？

因为工具和流程的差异，都源于同一个根：**ISO 与磁盘镜像的文件结构本质不同** —— ISO 是光盘文件系统的镜像（安装介质）；`.img` / `.raw` 是整块磁盘的扇区镜像（自带分区表 + 引导 + 系统）；`.qcow2` 装的是同一块盘，但外面套了一层 QEMU 的容器格式。结构决定了「能否被当作磁盘镜像直写、直启」，也决定了「要不要先转换」。

这一点是全文的分界点，下一章（第二章）专门展开。

---

### 这篇笔记怎么读

- **前提**：建议先读过 [[iso和img.md]]（或已了解 ISO=安装介质、IMG=成品盘），本文不再重复定义，专注「怎么烧、怎么装、怎么导入」。
- **顺序通读**：第一章定框架 → 第二章补结构 → 第三~五章按需精读 → 第六章对照速查与避坑。
- **跳读**：只刷软路由固件 → 重点第四、六章；只玩虚拟机 → 重点第五、六章；只纠结工具选择 → 重点第三、六章。
- 每个结论尽量保留了官方源链接，可随时点回去核对。

---

### 本章小结

- 回答原问题：ISO 与 IMG / raw / qcow2 烧录/写盘**不能一概而论**，要分「工具层」和「流程层」两层看。
- 工具层：Etcher / `dd` 逐字节写盘、对 ISO 与 IMG / raw 几乎无差别；Rufus 区分 ISO Image 与 DD Image 两种模式；Ventoy 不烧录，IMG 直启有插件前提；`.qcow2` 是容器格式，四类工具都不能直接写，必须先转换。
- 流程层：ISO 无论物理机还是虚拟机都要先进安装器；IMG / raw 写入/导入即启动，没有安装向导；`.qcow2` 只在虚拟机里能直接导入直启。
- 两层差异的根源是镜像结构（安装介质 vs 整盘镜像 vs 容器格式）——下一章展开。

---

## 第二章 镜像结构差异 —— 为什么处理方式会不一样

> 上一章给了结论：ISO 与磁盘镜像的烧录方法要分「工具层 + 流程层」看。这一章回答**为什么**——因为它们根本不是同一种东西。结构决定命运：ISO 是「一张光盘」，`.img` / `.raw` 是「一整块硬盘」，`.qcow2` 是「这块硬盘装进了盒子」。

---

### ISO：一张光盘的文件系统镜像

`.iso` 全称是 ISO 9660 / UDF **光盘文件系统镜像**。它复制的不是硬盘，而是**光盘**——所以里面装的是光盘的目录结构、引导目录（Boot Catalog）和安装程序文件。

正因为它本质是「光盘」：

- **虚拟机上**，它被当成一张**虚拟光驱里的光盘**插进 VM，机器从光驱引导后运行光盘上的安装程序；
- **物理机上**，它被写进 U 盘后，机器能不能引导，取决于 U 盘固件是否把它当作一张「光盘」来读。

关键点：**普通 ISO 内部没有硬盘意义上的分区表**（GPT/MBR）。而 BIOS/UEFI 要从 USB 硬盘引导，通常期望介质上有一个带分区表 + 引导代码的「磁盘结构」。这就是「为什么 ISO 不能总是像 IMG 一样整盘直写就完事」的根源之一。

> [!tip] 大白话
> ISO 是「装修队的光盘说明书」：上面写清了怎么装，但**它自己不是一间能住的房子**。要让它起作用，得先让机器「读这张盘」，再照着说明书把房子（目标盘）装出来。

---

### isohybrid：让 ISO 也能「装」成 U 盘的混血

既然 ISO 缺硬盘分区表，为什么 Etcher 把 Ubuntu 的 ISO 逐字节写进 U 盘后能引导？

因为很多发行版提供的是 **isohybrid（混合）ISO**：在保留 ISO 9660 结构的同时，**在镜像尾部附加了一份 MBR/GPT 分区表和引导代码**。同一份文件，放进光驱是光盘、写进 U 盘又是一块可引导的「小硬盘」——不需要工具做任何转换。

- Ubuntu 官方教程里，Rufus 检测到 Ubuntu ISO 是 **ISOHybrid image**，并提示「保留 Write in ISO Image mode」，就是这个原因。[Ubuntu 官方教程](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)
- balenaEtcher 官方也确认：Ubuntu 这类发行版镜像「不经修改即可从 CD 与 USB 双介质引导」。[balenaEtcher 官方文档](https://etcher-docs.balena.io/USER-DOCUMENTATION/)

**但 isohybrid 是一种妥协，不是万能钥匙：**

- Rufus 官方 FAQ 明确警告：用 **DD 模式**把 GPT 型 isohybrid ISO 写进 U 盘，可能出现**容量变小、Windows 无法挂载其后 Linux 分区、备份 GPT 未落在盘末**等问题，挑剔的 UEFI 固件可能拒绝引导。[Rufus 官方 Wiki FAQ](https://github.com/pbatard/rufus/wiki/FAQ)
- 换句话说：isohybrid ISO「能当磁盘镜像用」，但**不代表按磁盘镜像处理是最优解**——这正是 Rufus 要保留 ISO 模式、区分两种写法的原因。

> [!warning] 易错点
> 遇到「非混合」的普通 ISO（尤其某些精简版、专用镜像），用 Etcher/DD 逐字节写进 U 盘往往**无法引导**。这时要靠 Rufus 的 ISO Image mode 重新解包排版，把引导结构做出来。

---

### IMG / raw：一整块硬盘的「克隆」（裸镜像）

`.img`（以及几乎等价的 `.raw`）是**整块磁盘的扇区级镜像**。它不是光盘，而是把一整块硬盘从第 0 扇区开始原样复制出来的文件，里面**已经包含**：

- 分区表（GPT 或 MBR）
- 引导程序（UEFI/BIOS bootloader）
- 文件系统
- 装好的操作系统

所以它长得**和真实硬盘一模一样**：

- **物理机上**：把 IMG / raw 整盘写入 U 盘或内置盘，固件看到的就是一块「正常的盘」，直接引导进系统——不需要任何安装向导。iStoreOS / OpenWrt x86 的 `.img.gz` 固件走的就是这条路。[iStoreOS 官方文档](https://doc.linkease.com/zh/guide/istoreos/install_x86.html)
- **虚拟机上**：IMG / raw / qcow2 都可以直接**作为虚拟磁盘**导入并设为启动盘，开机即系统，无需安装阶段。[Proxmox qm 手册](https://pve.proxmox.com/pve-docs/qm.1.html)

> [!note] 同一类里的几个后缀
> - `.img`：最常见的叫法，整块盘的扇区镜像。
> - `.raw`：QEMU 语境下对「未压缩的原始磁盘镜像」的叫法，**本质 ≈ `.img`**，两者对写盘工具是同一串字节。[qemu-img 手册](https://www.qemu.org/docs/master/tools/qemu-img.html)
> - `.qcow2`：QEMU 的**容器格式**，装的是同一块盘，但外面多了一层格式头与簇索引（支持快照、压缩、backing file）。**它不是裸盘**——详见下一节。
> - `.img.gz` / `.img.xz`：压缩过的 IMG，写盘前通常要解压（部分工具如 Rufus 也能直接识别）。iStoreOS 官方说明其 `.img.gz` 固件「下载后不需要解压」即可写入。

---

### qcow2：同一块盘，被装进了 QEMU 的「容器」

`.img` / `.raw` 是**裸镜像**：文件第 0 字节就是磁盘第 0 字节，把文件原样写进设备，设备上就是那块盘。
`.qcow2` 不是裸的：它是 **QEMU 的块设备容器格式**，同一块盘被包了一层。

到底差在哪：

| 对比项 | `.img` / `.raw`（裸镜像） | `.qcow2`（容器格式） |
| --- | --- | --- |
| 文件第 0 字节是什么 | 目标盘的第 0 扇区（MBR / GPT） | qcow2 **文件头**（v2 固定 72 字节，v3 至少 104 字节） |
| 文件大小 | 与盘容量基本 1:1 | 按簇（cluster）分配，只占实际用到的部分，通常小得多 |
| 能否直接写物理盘 | ✅ 逐字节写即可 | ❌ 写下去的是「盒子」，固件在第 0 扇区读不到分区表 |
| 附加能力 | 无 | 内部快照、zlib 压缩、backing file（增量镜像） |
| 典型场景 | 刷机固件、可引导 U 盘 | PVE / KVM 里的虚拟机系统盘、云镜像 |

> [!summary] 结论
> **`.img` / `.raw` 是「裸的」，可以直接写盘；`.qcow2` 是「包的」，必须先拆开。**

**要从 qcow2 得到能写盘的东西，用 `qemu-img` 转换：**

```bash
# 1) 先看镜像信息：格式、虚拟容量、实际占用（qcow2 的"占用"通常远小于"容量"）
qemu-img info istoreos.qcow2

# 2) qcow2（容器）→ raw（裸盘）：转换后再按 IMG 流程写 U 盘/硬盘
qemu-img convert -f qcow2 -O raw istoreos.qcow2 istoreos.img

# 3) 反过来：把裸镜像收成 qcow2，省空间，还能享受 PVE 快照
qemu-img convert -f raw -O qcow2 istoreos.img istoreos.qcow2
```

- `-f` 指定**源**格式，`-O` 指定**目标**格式；
- 转换是「按内容重排」，不是复制文件——所以 qcow2 转 raw 后体积会涨到接近磁盘容量（除非文件系统支持稀疏文件）；
- PVE 的 `qm disk import` 明确要求「镜像格式必须被 `qemu-img` 支持」，`.img` / `.raw` / `.qcow2` / `.vmdk` 都在其中。[Proxmox qm 手册](https://pve.proxmox.com/pve-docs/qm.1.html)

> [!tip] 大白话
> `.img` / `.raw` 是**一整块预制板**：搬过去直接铺，就是地面。
> `.qcow2` 是**打了包装的同一块预制板**——外面裹了气泡膜（压缩）、贴了层压标签（格式头）、还预留了「以后能换板子」的接口（快照 / backing file）。包装让存储和搬运更省，但你不能连包装一起铺到地上。
> `qemu-img convert` 就是**拆包装 / 打包装**：`-O raw` 拆成裸板，`-O qcow2` 打回包装。
>
> 还有一点容易混：**改后缀不等于转换**。把 `x.qcow2` 改名成 `x.img` 只是换了标签，里面还是那个盒子。

> 出处：[QEMU qcow2 格式规范](https://www.qemu.org/docs/master/interop/qcow2.html)（首个簇为文件头、v2 头 72 字节 / v3 至少 104 字节、按簇分配、支持内部快照与 backing file）、[qemu-img 手册](https://www.qemu.org/docs/master/tools/qemu-img.html)（`convert` 语义与 `-f` / `-O` 参数）、[QEMU 磁盘镜像文档](https://www.qemu.org/docs/master/system/images.html)（raw 与 qcow2 的定位）

---

### 一张表看懂：结构差异如何决定「能不能直写直启」

| 维度 | ISO | IMG / raw（裸镜像） | qcow2（容器格式） |
| --- | --- | --- | --- |
| 本质 | 光盘文件系统镜像（安装介质） | 整块硬盘的扇区镜像（成品盘） | 同一块成品盘，外面套了 QEMU 容器 |
| 是否含硬盘分区表 | ❌（除非 isohybrid 附加） | ✅ GPT/MBR | ✅（在容器内部） |
| 是否含引导程序 | 只有光盘引导目录；硬盘引导需 isohybrid/工具重建 | ✅ | ✅（在容器内部） |
| 是否已装系统 | ❌ | ✅ | ✅ |
| 写盘/导入后 | 进入**安装器**，系统现场安装 | **直接引导**进入系统 | 虚拟机里可**导入直启**；写物理盘前要先 `qemu-img convert -O raw` |
| 典型用途 | Ubuntu / Windows 等系统安装 | iStoreOS / OpenWrt 固件、预装系统镜像 | PVE / KVM 虚拟机系统盘、云镜像 |
| 工具怎么处理 | Rufus 分 ISO/DD 模式；Etcher 整盘照抄（依赖 isohybrid） | 一律整盘直写 / 磁盘导入即可 | 写盘工具都不认；先转换成 raw，或走 `qm disk import` 导入虚拟机 |

---

### 小结

- **ISO = 光盘**：结构上是光驱用的，引导要「安装器」配合；只有 isohybrid 附加了分区表后才能被当磁盘用，且仍有坑。
- **IMG / raw = 硬盘**：结构上就是一块可引导的成品盘，写入/导入即启动。
- **qcow2 = 装进容器的硬盘**：块数据还是那块盘，但多了格式头 / 簇分配 / 快照；虚拟机里能当盘用，物理机必须先 `qemu-img convert -O raw`。
- 工具之所以对它们「区别对待」（Rufus 双模式、Ventoy 对 IMG 加插件限制、写盘工具不认 qcow2），**根因全在结构差异**。

---

## 第三章 工具层对比 —— Etcher / Rufus / Ventoy / dd 对 ISO 与磁盘镜像的处理

> 前两章建立了「结构差异决定处理方式」的认知。这一章落到具体工具：写盘时 ISO 与 IMG / raw / qcow2 是不是一回事，**取决于你手里拿的是哪个工具**。四类主流工具大致分三种哲学：纯写盘器（Etcher / dd）、双模式工具（Rufus）、拷贝式引导器（Ventoy）。**而 `.qcow2` 是它们共同的盲区**——没有一款写盘工具能直接写容器格式。

---

### balenaEtcher：ISO 与 IMG / raw 无差别，逐字节照抄

balenaEtcher 是最典型的「纯写盘器」：

- 对镜像**逐字节复制到设备，不做任何转换**，`.iso`、`.img` 还是 `.raw` 对它只是同一串字节——**没有模式之分，界面完全一样**。
- 正因为不做转换，它**依赖镜像自己可引导**：发行版 isohybrid ISO（如 Ubuntu）能直接写 U 盘引导；而需要「特殊处理」的镜像（典型是 **Windows 官方 ISO**）写进去无法引导，官方明确建议改用 Rufus / WoeUSB 等专用工具。
- 不支持持久化存储配置（例如 Linux live USB 的 persistence 分区）。
- **`.qcow2` 不能喂给 Etcher**：Etcher 不解析内容，会把 qcow2 文件头当成盘的第 0 扇区写下去，结果是一块无法引导的盘。要写先转换（见 [[#qcow2：同一块盘，被装进了 QEMU 的「容器」]]）。

**结论：Etcher 眼里 ISO ≈ IMG ≈ raw，操作完全一样；代价是它不替你「修」或「拆」任何镜像。**

> 出处：[balenaEtcher 官方用户文档](https://etcher-docs.balena.io/USER-DOCUMENTATION/)

---

### Rufus：分得最清 —— ISO Image mode vs DD Image mode

Rufus 是「对 ISO 与 IMG 区别最大」的工具，官方 FAQ 把写盘分成两种策略：

| 模式 | 英文名 | 机制 | 适用对象 |
|---|---|---|---|
| ISO 模式 | ISO Image mode | 把 ISO 当安装光盘，**解包重建**文件系统/分区结构，让 U 盘可引导 | 发行版 ISO（含 isohybrid） |
| DD 模式 | DD Image mode | **逐扇区直写**，把文件原样克隆到设备 | `.img` / `.raw` / `.vhd` / `.vhdx` 等线性磁盘镜像 |

关键行为：

- 遇到 `.img` 磁盘镜像，Rufus **自动走 DD 模式**（无法选 ISO 模式）；`.raw` 同理。
- Rufus 面向的是**线性磁盘镜像**——官方 FAQ 明确它「可以像打开 `.iso` 一样直接打开并写入 `.vhd` / `.vhdx`」。[Rufus 官方 Wiki FAQ](https://github.com/pbatard/rufus/wiki/FAQ) 这类文件的字节就是盘上字节，DD 模式照抄即可。
- 遇到 isohybrid ISO，Rufus **默认推荐 ISO Image mode**（而不是 DD），因为 DD 写 isohybrid 有一串坑：
  - U 盘容量可能**变小**、Windows 之后无法挂载其上的 Linux 分区；
  - GPT 型 isohybrid 用 DD 写会因**备份 GPT 未落在盘末**而被部分 UEFI 固件判为「损坏盘」拒绝引导；
  - 写入后镜像内嵌校验可能与盘上内容不一致。
- 有些系统只给 ISO 不给磁盘镜像时，Rufus 也会引导你换思路——例如 **OpenBSD** 官方 FAQ 示例就是让用户改下 `.img` 再走 DD。
- **`.qcow2` 要先转换**：它属于容器格式，字节不是盘上字节，Rufus 拿到的只是「盒子」。先 `qemu-img convert -f qcow2 -O raw x.qcow2 x.img`，转换出来的 `.img` 会被 Rufus 自动按 DD 处理。

**结论：同一个 Rufus，写 ISO 和写磁盘镜像时界面/模式不一样；`.img` / `.raw` 一律 DD，`.iso` 默认 ISO 模式、不推荐强行 DD，`.qcow2` 转换后才进得来。**

> 出处：[Rufus 官方 Wiki FAQ](https://github.com/pbatard/rufus/wiki/FAQ)、[Rufus Issue #843（ISO vs DD 模式讨论）](https://github.com/pbatard/rufus/issues/843)

---

### Ventoy：不烧录，把镜像当文件（IMG 有前提，qcow2 不在列）

Ventoy 的哲学与前两者**完全不同**——它不是烧录工具：

1. 把 U 盘做成 Ventoy 引导盘，得到一个普通分区；
2. 你只需把 ISO/IMG **当文件拷进分区**；
3. 开机从 U 盘引导，Ventoy 菜单列出镜像，选哪个启动哪个。

对普通发行版 ISO，这几乎「拷贝即启动」，体验极佳。**但 IMG 不是免费的：**

- Ventoy 从 1.0.41 起支持启动 **OpenWrt 的 IMG 镜像**，前提是先把 `ventoy_openwrt.xz` 插件放进 Ventoy 分区（它为镜像补上缺失的 `dm` 内核模块）；
- 支持范围**仅限 x86 的两种 OpenWrt 镜像**：`combined-ext4.img`（解压 gz 后直接可用）与 `combined-squashfs.img`（还需用脚本预处理）；
- 其它 IMG（包括 iStoreOS 固件等）**官方没有承诺**能通吃。
- Ventoy 官网列出的可启动类型是「**支持启动 ISO/WIM/IMG/VHD(x)/EFI 等类型的文件**」，另有 Linux vDisk 插件覆盖 `vhd` / `vdi` / `raw`——这份列表里**没有 `.qcow2`**。[Ventoy 官网](https://www.ventoy.net/cn/index.html)

**结论：Ventoy 把 ISO 和 IMG / raw 都当「文件」，但 IMG 要引导起来需要插件 + 特定镜像类型，不能默认「拷进去就能启动」；`.qcow2` 则不在其支持列表内。**

> 出处：[Ventoy 官方 OpenWrt 直启文档](https://www.ventoy.net/cn/doc_openwrt.html)

---

### dd：命令行的「逐字节照抄」，目标要写整盘

`dd` 是 Linux/macOS 下的块级拷贝命令，和 Etcher 同属「纯写盘器」：它只做**转换并拷贝**，不解析文件内容，因此对 `.iso` / `.img` / `.raw` **本身没有差别**。

```bash
# 把磁盘镜像写进整块设备（危险：目标盘所有数据会被覆盖）
sudo dd if=固件.img of=/dev/sdX bs=4M status=progress conv=fsync

# qcow2 不能直接 dd：先拆成裸镜像，再写盘
qemu-img convert -f qcow2 -O raw 固件.qcow2 固件.img
sudo dd if=固件.img of=/dev/sdX bs=4M status=progress conv=fsync
```

三个高频错误点：

- `of=` 必须指向**整块设备**（如 `/dev/sdX`、`/dev/sdb`），不能写分区（`/dev/sdb1`）；
- 用 `dd` 写**非混合 ISO** 到 U 盘通常无法引导（它不会像 Rufus ISO 模式那样重建引导结构）；
- **把 `.qcow2` 直接 `dd` 到 U 盘**：`dd` 不解析内容，写下去的是 qcow2 容器本身，盘无法引导——它只认裸镜像。

**结论：dd 与 Etcher 一样对 ISO / IMG / raw 无差别；能否引导取决于镜像自身是否 isohybrid / 可磁盘引导，而 `.qcow2` 必须先 `qemu-img convert` 成 raw。**

> 出处：GNU Coreutils `dd` 语义为通用知识（详见研究文件 gap #5，未做官方页深读）

---

### 工具层速览

| 工具 | 区分 ISO / 裸镜像？ | ISO 怎么处理 | IMG / raw 怎么处理 | `.qcow2` 怎么办 | 一句话 |
| --- | --- | --- | --- | --- | --- |
| balenaEtcher | ❌ | 逐字节整盘写 | 逐字节整盘写 | ❌ 不能直接写 | 无差别，但依赖镜像自己可引导 |
| Rufus | ✅ | ISO Image mode（默认） | DD Image mode（自动） | ❌ 先转成 raw | 分得最清，isohybrid 别硬用 DD |
| Ventoy | ⚠️ 都当文件 | 拷贝即启动 | 需插件 + 特定镜像 | ❌ 不在支持列表 | 不烧录，IMG 有前提 |
| dd | ❌ | 块级照抄 | 块级照抄 | ❌ 先转成 raw | 目标写整盘，能否引导看镜像 |

> **小结**：工具层的规律不是「ISO=安装器 / IMG=整盘」这么简单，而是——**纯写盘器**对 ISO / IMG / raw 一视同仁；**Rufus** 用两种模式管理两者的结构差异；**Ventoy** 用「当文件 + 菜单引导」绕开烧录，却因此对 IMG 附加了插件限制；而 **`.qcow2` 是四者共同的盲区**，因为它是容器格式不是裸盘，写盘前一律要先 `qemu-img convert -O raw`。

---

## 第四章 物理机两种刷机流程 —— IMG / raw 成品盘式 vs ISO 安装器式

> 第三章讲了「工具怎么对待镜像」。这一章看物理机真实操作：同样是拿一个镜像让一台真机跑起来，**IMG / raw 系固件**和 **ISO 系安装盘**走的是两条不同的路——差在「写盘之后还有没有安装阶段」。**`.qcow2` 在物理机上没有自己的流程**：先 `qemu-img convert` 成 raw，再走流程 A。

---

### 流程 A：IMG / raw 成品盘式 —— 以 iStoreOS X86 为例

iStoreOS（OpenWrt 系）官方给 x86 物理机提供的固件是 `xxx.img.gz`，本质是一块**装好系统的成品盘**。官方刷机流程如下：[iStoreOS X86 物理机安装官方文档](https://doc.linkease.com/zh/guide/istoreos/install_x86.html)

1. **准备**：一台 Windows 电脑、一个 U 盘、给目标机接上显示器/键盘。
2. **下载固件**：从官网下载对应 `x86_64` 的 `.img.gz` 固件——**官方说明下载后不需要解压**。
3. **做启动盘**：Windows 上用 **Rufus** 选择该固件写入 U 盘，做成可启动 USB 盘（`.img` 会自动走 DD 整盘写入）。
4. **U 盘引导**：把 U 盘插到目标机，开机一般按 **F11**（或对应快捷启动键）选择从 U 盘启动；找不到 U 盘视为兼容性问题。
5. **进入临时系统**：从 U 盘引导后进入的是一个**临时 live 系统**（固件其实已在 U 盘里跑起来了），登录后命令行输入：

   ```
   quickstart
   ```

6. **Install X86 写内置盘**：在 quickstart 界面选择 **Install X86**，一路按确定，把固件**整盘写入机器内置硬盘**（而不是停在 U 盘上运行）。
7. **拔盘直启**：写入完成，拔掉 U 盘等外接设备再通电，直接进入已装好的系统——**没有二次安装向导**。
8. **进后台**：默认后台 `http://192.168.100.1/` 或 `http://iStoreOS.lan/`，默认密码 `password`；多网口机型默认第一口为 WAN。

> [!tip] 为什么 iStoreOS 不像 Windows 那样「装系统」？
> 因为 IMG 本身就是**完整的成品盘**（分区 + 引导 + 系统全在镜像里）。U 盘引导的临时系统里那步 Install X86，本质只是**把这块成品盘复制到内置硬盘**，再把引导指向它——不是传统意义的安装器。

---

### 流程 B：ISO 安装器式 —— 以 Ubuntu 为例

Ubuntu 等通用系统提供的是 ISO「安装盘」。官方在 Windows 下的做法是：[Ubuntu 官方教程：用 Rufus 制作启动 U 盘](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows)

1. **下载 ISO**：从官网下载 Ubuntu ISO（注意：不要直接把 ISO 下载到 U 盘）。
2. **Rufus 选 ISO**：打开 Rufus，插入 U 盘，确认 Device 选对，在 Boot selection 选择下载的 Ubuntu ISO。
3. **ISOHybrid 提示**：Rufus 会检测到这是 **ISOHybrid image**，并提示 **保留 “Write in ISO Image mode”** 点击 OK（此时不要切成 DD 模式）。
4. **写入**：点 START 开始写入，进度完成显示 READY。
5. **U 盘引导**：把 U 盘插入目标机，开机（通常 F12）从 U 盘启动。
6. **进入安装器**：引导后进入 **Try or Install Ubuntu**——注意，到这里系统**还没有安装**。
7. **走安装向导**：选择语言、键盘、分区、用户等，安装器才把系统**现场装进目标盘**，最后重启进入新系统。

> [!warning] 两种流程的本质差异
>
> | | IMG / raw 成品盘式（iStoreOS） | ISO 安装器式（Ubuntu） |
> |---|---|---|
> | 镜像内容 | 已是完整系统 | 只是安装程序 + 文件 |
> | 写盘后 | 引导 → 复制到内置盘 → 直启 | 引导 → **现场安装** → 重启 |
> | 有没有安装向导 | 无（quickstart 只是选目标盘） | 有（分区/账号/引导器） |
> | 首次进系统时间 | 分钟级 | 通常更久（含安装过程） |

---

### 一句话对照

- **刷成品固件（软路由 iStoreOS / OpenWrt 等）→ 走 IMG / raw 流程**：写盘（可选先进临时系统复制到内置盘），写完成品即系统。
- **装通用系统（Windows / Ubuntu）→ 走 ISO 流程**：写 U 盘只是拿到了「安装器的入场券」，系统要现场装。
- **手里只有 `.qcow2` → 先转换，再走 IMG 流程**：`qemu-img convert -f qcow2 -O raw x.qcow2 x.img`。它和 iStoreOS 固件的差别只在「多一道拆包装」，拆完之后的写盘与引导完全一样。

> [!note] 一个说明
> OpenWrt 官网的 x86 安装页在收集时被反爬拦截、正文未能抓取，本处以同源的 iStoreOS 官方文档代表 OpenWrt 系 IMG 流程；两者刷机逻辑一致（`.img.gz` → 写盘 → 引导）。如需引用 OpenWrt 官网原文，建议人工浏览器复核后再补充。

---

## 第五章 虚拟机两种用法 —— ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入直启

> 物理机上「刻 U 盘 vs 写整盘」的差别，在虚拟机里变成了**「挂光驱装系统」vs「导磁盘即启动」**。本章以 **Proxmox VE（PVE）** 和 **libvirt/virt-install** 两套入口为例，命令层面看差异。

---

### 共同逻辑

虚拟机里区分两种介质：

- **CD-ROM（光驱）**：只读，用来**引导安装程序**，装完就退出引导；
- **Disk（系统盘）**：可写，是系统真正落盘的地方。

「装新系统」= 挂一个 **ISO 光驱** + 给一块**空系统盘**，让安装器把系统写进空盘；
「用现成镜像」= 把 **IMG/raw/qcow2** 直接作为**系统盘**导入，开机即系统——没有安装阶段。

---

### PVE 侧

**路径 1：ISO → 虚拟光驱安装**

1. 先把 ISO 上传到某个存储的 **ISO 区**（如 `local:iso`）；
2. 创建 VM：一块空系统盘 + 挂 ISO 光驱。PVE 里 `-cdrom` 实为 `ide2` 且 `media=cdrom` 的别名：

```bash
qm create 300 -ide0 local-lvm:4 -net0 e1000 -cdrom local:iso/ubuntu-24.04.iso
```

3. 开机后 VM 从光驱引导进入安装器，安装器把系统写进 `-ide0` 那块空盘。ISO 光驱只读，安装完不再参与引导。

> 出处：[Proxmox VE qm 手册](https://pve.proxmox.com/pve-docs/qm.1.html)

**路径 2：IMG/raw/qcow2 → 导入磁盘直启**

这是「用成品镜像」的路径，无需安装器：

```bash
# 1) 把外部磁盘镜像导入为 VM 的「未使用磁盘」(qm importdisk 是 qm disk import 的别名)
qm disk import 100 istoreos.img local-lvm --format qcow2

# 2) 到 Web 界面：硬件 → 找到"未使用磁盘"→ 添加（总线建议 SATA/SCSI）

# 3) 设引导顺序：选项 → 引导顺序 → 只勾选刚添加的硬盘并移到第一位

# 4) 开机直启
```

导入格式必须是 qemu-img 支持的格式（`qcow2` / `raw` / `vmdk` 等）；源镜像默认保留为 unused 磁盘，可后续删除。

> [!tip] 三种后缀在 PVE 里的待遇
> - `.img` / `.raw`：直接导入，**不用你手动转换**（PVE 会按目标存储支持的格式落盘，通常是 qcow2）。
> - `.qcow2`：直接导入。
> - `.img.gz` / `.img.xz`：先解压成 `.img` 再导入。
>
> 反过来，想把 PVE 里的虚拟磁盘导出成裸镜像、拿去写物理盘：
> `qemu-img convert -O raw /var/lib/vz/images/100/vm-100-disk-0.qcow2 vm-100-disk-0.img`

**更新的写法（免先建空盘）**：用 `import-from` 在创建/设置磁盘时**直接导入即挂盘**：

```bash
qm set 9000 --scsi0 local-lvm:0,import-from=/path/istoreos.img
```

直启建议配套：

```bash
qm set 9000 --scsihw virtio-scsi-pci --boot order=scsi0
```

- `--boot order=scsi0` 限定只从该盘引导，BIOS 会跳过光驱探测，加快启动。
- 若是 **Cloud-Init 镜像**，还要加一个 cloud-init 数据盘光驱：`qm set 9000 --ide2 local-lvm:cloudinit`，并常配 `serial0`。

> 一句话：PVE 里 **ISO 走「挂光驱 + 空盘 + 安装器」**，**IMG / raw / qcow2 走「导入 → attach → 设引导」**，对应命令完全不同；而且 `.img` / `.raw` 不需要你预先转换，PVE 会自己按目标存储的格式落盘。

---

### virt-install（KVM/QEMU）侧

libvirt 的 `virt-install` 用不同选项表达这两种路径：[virt-install(1) 手册](https://manpages.ubuntu.com/manpages/jammy/man1/virt-install.1.html)

**路径 1：ISO → `--cdrom` / `--location`**

```bash
# 用本地 ISO 作为安装介质（整盘式引导，类似插光盘）
virt-install \
  --name my-win10 \
  --memory 4096 \
  --disk size=40 \
  --osinfo win10 \
  --cdrom /path/to/Win10.iso
```

- `--cdrom`：把 ISO/光盘设备作为安装介质，引导后进入安装器，ISO 装完被弹出；
- `--location`：从发行树（HTTP/FTP/本地目录/部分 ISO）只抓最小 kernel/initrd 来远程安装，可配 `--extra-args` 传内核参数、`--initrd-inject` 注入文件；
- 两者都必须**另配一块系统盘**（上面 `--disk size=40` 新建空盘）供安装器落盘。

**路径 2：磁盘镜像 → `--import` 直启**

```bash
# --import：完全跳过安装阶段，直接用现有磁盘镜像建 guest 并引导
virt-install \
  --name my-router \
  --memory 512 \
  --disk /home/user/VMs/istoreos.img \
  --osinfo debian9 \
  --import
```

- `--import` 会用第一个 `--disk`/`--filesystem` 设备作为引导盘，不进入安装器；
- `--boot` 单独给出（不带安装选项）时行为等同 `--import`。
- `--disk` 指到的文件可以是 `.img`、`.raw` 或 `.qcow2`——libvirt 直接交给 QEMU 解析，**容器格式在这里同样认**。
- 同一条 `--disk` 体系内，用子选项区分介质与系统盘：

```bash
--disk /path/to/image.iso,device=cdrom   # 介质盘
--disk /path/to/image.img,bus=scsi       # 系统盘（bus 可选 ide/sata/scsi/usb/virtio）
```

> 出处：[virt-install(1) 手册](https://manpages.ubuntu.com/manpages/jammy/man1/virt-install.1.html)

---

### 命令对照速查

| 动作 | PVE | virt-install |
|---|---|---|
| 挂 ISO 光驱安装 | `qm create … -cdrom local:iso/x.iso -ide0 local-lvm:4` | `virt-install … --cdrom /path/x.iso --disk size=40` |
| 远程/最小安装 | — | `--location http://mirror/… --extra-args …` |
| 导入磁盘直启 | `qm disk import <vmid> x.img <storage>` + attach | `virt-install … --import --disk /path/x.img` |
| 导入即挂盘（免空盘） | `qm set … --scsi0 s:0,import-from=/path/x.img` | — |
| 介质 vs 系统盘 | 光驱=ide2 cdrom；盘=ide/sata/scsi | `device=cdrom` vs 默认 disk |

> **小结**：虚拟机平台的规律与物理机一致——**ISO 永远先走「安装器」**（挂光驱 + 空盘），**IMG / raw / qcow2 走「导入即启动」**。差异只在命令入口：PVE 用 `-cdrom`/`qm disk import`/`import-from`，virt-install 用 `--cdrom`/`--location`/`--import`。
>
> 另外要记住一条不对称：**虚拟机是 `.qcow2` 唯一能「直接当盘用」的地方**。物理机上它必须先 `qemu-img convert -O raw` 拆开，虚拟机里则原样导入即可。

---

## 第六章 速查表、常见坑与延伸 —— 实操前必看

> 前五章把原理、工具和两条流程都过了一遍。这一章把它压成**可执行清单**：拿到任意镜像先判类型 → 按场景选工具 → 避开高频坑。写完这篇，「ISO 与 IMG / raw / qcow2 烧录方法是否相同」就能自己判断了。

---

### 第一步：先判镜像类型

| 看到的后缀 | 本质 | 默认怎么处理 |
|---|---|---|
| `.iso` | 光盘安装介质 | 当「安装盘」：写 U 盘/挂光驱 → 走安装器 |
| `.img` / `.raw` | 整块硬盘镜像（**裸镜像**） | 当「成品盘」：整盘写入 / 导入磁盘 → 直启 |
| `.qcow2` | QEMU **容器格式**的虚拟磁盘（可快照/压缩） | 虚拟机：直接导入直启；**物理机：先 `qemu-img convert -O raw`** |
| `.img.gz` / `.img.xz` | 压缩过的成品盘 | 解压后写盘（部分工具可直接识别） |
| `.vhd` / `.vhdx` | 微软虚拟硬盘（同样是线性镜像） | Rufus 可直接写；虚拟化平台也能导入 |

> [!tip] 记忆
> **ISO 是「碟」，IMG / raw 是「裸盘」，qcow2 是「装进盒子的盘」。**
> 碟用来装系统，裸盘拿来直接开机，盒子要先拆（`qemu-img convert -f qcow2 -O raw`）。（概念细节见 [[iso和img.md]]）

---

### 第二步：工具 × 镜像速查

| 你想做什么 | 推荐工具 | 关键设置 |
|---|---|---|
| 发行版 ISO → U 盘（装 Windows/Ubuntu） | **Rufus** | 保留 **ISO Image mode**（默认） |
| 刷 `.img` / `.raw` 固件 → U 盘/整盘（iStoreOS/OpenWrt） | **Rufus** 或 **balenaEtcher** | Rufus 自动走 **DD**；Etcher 直接写 |
| Linux/macOS 命令行写盘 | **dd** | `if=镜像 of=/dev/sdX`（**整盘**非分区） |
| **把 `.qcow2` 用到物理机** | **`qemu-img` + Rufus/Etcher** | 先 `qemu-img convert -f qcow2 -O raw x.qcow2 x.img`，再按 IMG 流程写盘 |
| 一个 U 盘装多个 ISO | **Ventoy** | ISO 直接拷贝；**不要默认 Ventoy 通吃 IMG**，`.qcow2` 不在其支持列表 |
| Windows ISO | **Rufus / WoeUSB / MS 官方工具** | 不要用 balenaEtcher（无法引导） |
| 虚拟机装新系统 | PVE `-cdrom` / virt-install `--cdrom` | 挂光驱 + 新建空盘 |
| 虚拟机直启成品镜像 | PVE `qm disk import` / virt-install `--import` | **`.img` / `.raw` / `.qcow2` 都可直接导入** → attach → 设引导 |
| 查看/转换镜像格式 | **`qemu-img info` / `qemu-img convert`** | `-f` 源格式、`-O` 目标格式 |

---

### 第三步：高频坑清单

1. **`.img.gz` 没解压就写盘**：多数情况要先解压成 `.img`（iStoreOS 官方流程例外，Rufus 可直接识别其固件）。看到写入失败或无法引导先检查这一步。
2. **选错目标盘**：Rufus/Etcher 里 Device 选错、`dd of=/dev/sda` 写错整盘，数据直接全没。**写盘前只保留目标 U 盘/硬盘**，确认盘符/容量再动手。
3. **isohybrid ISO 误用 DD 模式**：Rufus 对 Ubuntu 等 isohybrid 提示保留 ISO Image mode 时别切成 DD——DD 写 GPT isohybrid 可能导致容量变小、Windows 无法挂载、部分 UEFI 拒启。（[Rufus FAQ](https://github.com/pbatard/rufus/wiki/FAQ)）
4. **刷完不引导（Secure Boot / 引导顺序 / GPT）**：优先排查三件事——关 Secure Boot、进 BIOS 把 U 盘/新盘设为首启、确认是 GPT/MBR 与固件匹配。
5. **用 Ventoy 刷任意 IMG**：Ventoy 只对特定 OpenWrt x86 img（配合 `ventoy_openwrt.xz` 插件）提供官方支持，**iStoreOS 等其它 IMG 不要默认 Ventoy 能启动**。
6. **用 balenaEtcher 写 Windows ISO**：Etcher 逐字节不转换，Windows ISO 需要特殊处理，官方建议换 Rufus/WoeUSB。
7. **虚拟机里把 ISO 当系统盘挂着不装**：ISO 只读，只能引导安装器；系统要装进另一块**空盘**（`--disk size=N` / `-ide0`），装完记得把引导顺序设回硬盘。
8. **把 `.qcow2` 当裸镜像直接写盘（或改后缀蒙混）**：`.qcow2` 是 QEMU 容器格式，文件第 0 字节是 qcow2 文件头而不是分区表。用 Rufus / Etcher / `dd` 直接写，得到的是**一块无法引导的盘**；把 `x.qcow2` 改名成 `x.img` 也一样（只改名字不改内容）。**唯一正解是真正转换**：`qemu-img convert -f qcow2 -O raw x.qcow2 x.img`。

---

### 回答最初的问题（最终版）

> **ISO 与 IMG / raw / qcow2 烧录/写盘的方法和操作，一样吗？**
>
> - **工具层**：**看工具**。Etcher / `dd` 对 ISO、IMG、raw 几乎无差别（逐字节照抄）；Rufus 明确区分 ISO Image / DD 两种模式（`.img` / `.raw` 自动 DD）；Ventoy 把镜像都当文件，但 IMG 有插件和镜像类型限制；`.qcow2` 是四类工具共同的盲区，必须先 `qemu-img convert -O raw`。
> - **流程层**：**看场景，且规律跨物理机/虚拟机一致**——ISO 永远是「先启动安装器、现场装系统」；IMG / raw / qcow2 是「写入/导入即启动的成品盘」，其中 `.qcow2` 只在虚拟机上能直接走这条路。
>
> 所以准确说法是：**不能一概而论**。判断方法是先看后缀判类型（碟 / 裸盘 / 盒子），再看你用什么工具、装到物理机还是虚拟机。

---

### 延伸

- **概念篇**：ISO 与 IMG 的定义、本质、对比总表 → [[iso和img.md]]
- **本目录索引**：[[虚拟机 MOC]]
- **工具细分**：Ventoy 对 OpenWrt IMG 的插件机制 → [Ventoy 官方文档](https://www.ventoy.net/cn/doc_openwrt.html)
- **PVE 导入磁盘**：`qm disk import` 与 `import-from` 完整语义 → [Proxmox qm 手册](https://pve.proxmox.com/pve-docs/qm.1.html)
- **格式转换**：`qemu-img convert` 的 `-f` / `-O` 与支持的格式 → [qemu-img 手册](https://www.qemu.org/docs/master/tools/qemu-img.html)
- **qcow2 格式细节**：文件头、簇分配、内部快照、backing file → [QEMU qcow2 格式规范](https://www.qemu.org/docs/master/interop/qcow2.html)

---

### 本章小结

- 拿到镜像先判类型：`.iso` = 碟（安装介质），`.img` / `.raw` = 裸盘（成品盘，可直接写），`.qcow2` = 装进 QEMU 盒子的盘（写物理盘前先转换）。
- 选工具看场景：装机用 Rufus ISO 模式；刷固件用 Rufus DD / Etcher / dd；多 ISO 用 Ventoy（勿通吃 IMG）；`.qcow2` 一律先用 `qemu-img convert -f qcow2 -O raw` 拆开。
- 八个高频坑集中在：`.img.gz` 解压、目标盘写错、isohybrid 误用 DD、Secure Boot/引导顺序、Ventoy 局限、Windows ISO + Etcher、虚拟机光驱与系统盘混淆、**把 `.qcow2` 当裸镜像直接写（或改后缀）**。
- 核心结论一句话：**ISO 多一步「装」，IMG / raw 拿来即用、qcow2 先拆盒——工具是否一视同仁、流程是否一样，都取决于镜像类型和你的场景。**

---

## 更新记录

| 日期 | 变更 |
| --- | --- |
| 2026-09-09 | 初版：ISO 与 IMG 烧录/写盘双视角对比（工具层 + 流程层，六章） |
| 2026-09-17 | 把 `.img` / `.raw` / `.qcow2` 三种磁盘镜像格式统一纳入全篇框架：标题与 tags 加入 `raw` / `qcow2`；第二章新增「qcow2：同一块盘，被装进了 QEMU 的「容器」」小节（裸镜像 vs 容器格式对照表、`qemu-img info` / `convert` 用法、大白话类比）；各章框架与三张速查表统一为「ISO / IMG·raw / qcow2」三分法；第六章新增高频坑第 8 条「把 `.qcow2` 当裸镜像直接写盘（或改后缀）」；补充 QEMU 官方出处（qcow2 格式规范、qemu-img 手册、QEMU 磁盘镜像文档）与 Ventoy 官网支持列表 |
