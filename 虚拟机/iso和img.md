---
title: ISO 和 IMG 的区别
tags:
  - 虚拟机
  - 镜像
  - 镜像格式
  - ISO
  - IMG
  - qcow2
  - vmdk
  - pve
created: 2026-01-31
updated: 2026-09-17
status: active
---

# ISO 和 IMG 的区别

> [!info] 一句话总结
> **ISO = 安装光盘**  
> **IMG = 已经装好的硬盘**
>
> 这句话你可以直接刻进脑子里。

## 1. ISO 是什么？（.iso）

### 1.1 ISO 的本质

> **ISO = 光盘的完整镜像**

它是：

> - CD / DVD / 安装 U 盘
> - 按扇区复制出来的文件

> [!tip] 大白话
> ISO 就是"一张系统安装光盘的电子版"。把它当成一张虚拟光盘插进电脑，电脑会运行里面的安装程序，但在**装完系统之前，它里面并没有"装好的系统"**。打比方：ISO 是"装修工具"，不是"成品房"。

### 1.2 ISO 里一般有什么？

> - 启动引导（BIOS / UEFI）
> - 安装程序
> - 系统内核
> - 安装所需的所有文件

❗但**没有"安装到硬盘后的系统状态"**

### 1.3 ISO 用来干嘛？

> **用来"安装系统"**

流程是：

`ISO（安装介质）    ↓ 启动 VM    ↓ 安装器运行    ↓ 把系统写入硬盘`

### 1.4 PVE 里 ISO 的用法

- 放在：`local → ISO Images`
- 在创建 VM 时选择：
    - **Use CD/DVD ISO**

👉 等价于「插一张系统安装光盘」

## 2. IMG 是什么？（.img）

### 2.1 IMG 的本质

> **IMG = 硬盘的完整扇区镜像**

它是：

> - 一整块硬盘
> - 包含：
>     - 分区表
>     - 文件系统
>     - 引导区
>     - 已装好的操作系统

> [!tip] 大白话
> IMG 就是"一整块硬盘的克隆文件"，分区、引导、系统全都打包在里面，**拿到就能开机**。打比方：IMG 是"精装好的成品房"，拎包入住。

### 2.2 IMG 里一般有什么？

> - GPT / MBR
> - EFI 分区（如果是 UEFI）
> - rootfs
> - bootloader

👉 **开机就能跑**

### 2.3 IMG 用来干嘛？

> **直接作为系统盘使用**

流程是：

`IMG（系统盘）    ↓ 挂载为 VM 硬盘    ↓ 开机`

### 2.4 PVE 里 IMG 的用法

通常步骤是：

1. 创建 VM（不选 OS，即"不使用任何介质"）
2. 把下载好的镜像上传到 PVE：
    - 路径：`/var/lib/vz/template/iso/`
    - ⚠️ iStoreOS / OpenWRT 固件下载下来通常是 `.img.gz`，先解压成 `.img` 再上传
3. 导入磁盘：
    `qm importdisk 100 istoreos.img local-lvm`
4. 把导入的盘设为启动盘：
    - 硬件 → 找到"未使用的磁盘"→ 添加（总线建议 SATA / SCSI）
    - 选项 → 引导顺序 → 只勾选刚添加的硬盘并移到第一位
5. 开机

> [!warning] ⚠️ 存储位置说明
> 这里用的是 ==local-lvm==，具体讲解见 [[PVE的学习/01-安装配置/PVE存储库#PVE 里的"两种存储库"|PVE 里的"两种存储库"]]。

## 3. ISO vs IMG 全面对比（你一定要记住）

|对比点|ISO|IMG|
|---|---|---|
|类型|安装介质|系统磁盘|
|是否已装系统|❌|✅|
|能否直接运行|❌|✅|
|是否含分区表|❌（一般）|✅|
|是否含 bootloader|❌（仅安装器）|✅|
|PVE 用法|CD/DVD|硬盘|
|常见系统|Ubuntu / Win|iStoreOS / OpenWRT|

> [!tip] 记忆口诀
> **ISO 是"碟"，IMG 是"盘"。** 碟用来装系统，盘拿来直接开机。

## 4. 总结

### 4.1 关于 ISO

> **"iso 相当于一个装修工具，我们把这插入我们预先准备好的硬盘，然后电脑会自动用 iso 把这个房子装修好（房子在硬盘）"**

✔️ **完全正确**

换成技术话也一模一样：

> - ISO = 安装介质
> - 硬盘 = 目标磁盘
> - 启动 ISO = 运行安装程序
> - 安装完成 = 系统被写进硬盘

### 4.2 关于 IMG

> **"img 就是一个成品房，我们不需要介质，直接把装好的硬盘给我们就行"**

✔️ **完全正确**

技术上就是：

> - IMG = 整块系统盘的复制品
> - 已经包含：
>     - 分区
>     - 引导
>     - 系统
> - 直接作为启动盘使用

这正是 iStoreOS / OpenWRT 官方推荐的用法。

## 5. 其他常见镜像格式（一次认清）

> [!info] 先记住一个分类法
> 所有"镜像文件"只分三类，遇到陌生扩展名先归一下类：
>
> 1. **安装介质类**（光盘 / 软盘）——里面是**安装程序**，必须跑一遍安装才能变成系统
> 2. **磁盘镜像类**（一整块盘）——里面是**装好的系统**，挂上就能开机
> 3. **打包 / 备份 / 压缩类**（盒子里装着前两类）——先拆包、解压，拆完还是归到上面两类

> [!tip] 大白话
> 三类就是：**菜谱**（安装介质）、**料理包**（磁盘镜像）、**外卖打包盒**（打包 / 压缩格式）。
> 打包盒不能直接吃，得先拆开；拆开之后里面是菜谱还是料理包，再看内容。
> 所以遇到不认识的格式，先问一句：**这是"安装盘"，还是"一块盘"？**

### 5.1 总览速查表

| 扩展名 | 属于哪类 | 一句话说明 | 能直接开机 | 常见出处 |
|---|---|---|---|---|
| `.iso` | 安装介质 | 光盘镜像 | ❌ | Ubuntu / Windows / Debian |
| `.img` | 磁盘镜像 | 一整块硬盘的裸镜像 | ✅ | iStoreOS / OpenWrt / 树莓派 |
| `.raw` | 磁盘镜像 | 和 `.img` 是同一件东西，KVM / PVE 的叫法 | ✅ | PVE / OpenStack |
| `.qcow2` | 磁盘镜像 | QEMU 的"容器式"磁盘，支持快照 | ✅ | PVE 默认 |
| `.vmdk` | 磁盘镜像 | VMware 磁盘 | ✅ | ESXi / VMware Workstation |
| `.vdi` | 磁盘镜像 | VirtualBox 磁盘 | ✅ | VirtualBox |
| `.vhd` / `.vhdx` | 磁盘镜像 | Hyper-V / Azure 磁盘 | ✅ | Hyper-V / 云主机 |
| `.qcow` / `.qed` | 磁盘镜像 | 老格式，知道是什么就行 | ✅ | 旧版 QEMU |
| `.ova` | 打包 | tar 包 = `.ovf` 描述 + `.vmdk` 磁盘 | ❌ 先解包 | 跨平台迁移 / 厂商分发 |
| `.ovf` | 打包 | XML 描述文件（严格说不是镜像） | ❌ | 与 OVA 成对出现 |
| `.vma.zst` | 备份 | PVE 自己的虚拟机备份包 | ❌ 只能还原 | PVE 备份 |
| `.tar.gz` / `.tar.zst` | 打包 | LXC / CT 容器模板、系统 rootfs | ❌ | PVE 容器模板 |
| `.img.gz` / `.img.xz` / `.img.zst` | 压缩 | 压缩过的成品盘，解压后就是 `.img` | ❌ 先解压 | OpenWrt / 树莓派固件 |
| `.wim` / `.esd` | 安装介质 | Windows 映像（按文件存，不是扇区） | ❌ | Windows 安装盘 / PE |
| `.bin` + `.cue` | 安装介质 | 老式光盘镜像（数据 + 轨道表） | ❌ | 老软件 / 复古游戏 |
| `.gho` | 备份 | 老式 Ghost 整盘备份 | ❌ 只能还原 | 老 PE 维护盘 |
| `.squashfs` | 文件系统 | 只读压缩根文件系统 | ❌ | OpenWrt / 定制固件 |
| `.trx` / 固件 `.bin` | 固件 | 路由器固件（factory / sysupgrade） | ❌ | OpenWrt 刷机 |
| `.vfd` / `.flp` | 安装介质 | 虚拟软盘（1.44 MB） | ❌ | 刷 BIOS |
| `.e01` | 取证 | EnCase 取证镜像 | ❌ | 数据恢复 / 取证 |

### 5.2 `.qcow2`

> - 虚拟机专用磁盘
> - 支持快照
> - 稀疏分配（用到多少占多少）
> - 本质和 IMG 一样：**系统盘**

PVE 新建虚拟机时默认就用它，文件名形如 `vm-100-disk-0.qcow2`。

> [!tip] 大白话
> `.raw` / `.img` 是"把盘里每个字节都抄一遍"，哪怕 90% 是空的；`.qcow2` 是"只记下有内容的地方，再配一张索引表"。所以一块 100 GB 的盘，`.qcow2` 文件实际可能只有 2 GB。
> 代价是多一层索引，早期 QEMU 下性能略低于 raw（现代硬件上差距已经很小）。

### 5.3 `.raw`

> - 原始磁盘，逐字节
> - 性能最好（少一层"索引表"）
> - 和 `.img` 是同一个东西，只是 KVM / PVE 习惯叫 raw

⚠️ 别再用"文件大小"猜格式了——`qemu-img info` 会给出两个更靠谱的数字：

- `virtual size`（虚拟容量）：这块"盘"有多大
- `disk size`（实际占用）：真正占了你宿主多少空间

### 5.4 `.vmdk`（VMware）

> - VMware 家的磁盘格式（ESXi / Workstation / Fusion 通用）
> - 同一个 `.vmdk` 有几种形态，先看目录里有没有同名的"分身文件"：
>     - **单文件**（`disk.vmdk`）：数据就在这一个文件里，最常见
>     - **拆片**（`disk-s001.vmdk`、`disk-s002.vmdk`…，外加一个几 KB 的文本 `disk.vmdk` 当描述）：真正的数据在分片里，**别只拷那一个小文件**
>     - **带 `-flat`**（`disk-flat.vmdk`）：厚置备，一次占满

> [!tip] 大白话
> `.vmdk` 像"行李"：可能是一件大行李（单文件），也可能是拆成好几个小包（分片）。搬家的规则是——**要么整箱搬，要么一个都别落下**，只拿那个几 KB 的描述文件等于搬了个空箱子。

PVE 里可以直接导入，不用先转换：

```bash
qm disk import 100 vmware-disk.vmdk local-lvm
```

### 5.5 `.vdi`（VirtualBox）

> - VirtualBox 的默认磁盘格式
> - 同样支持快照、动态分配
> - 想给 PVE / KVM 用，先转换（命令见 5.7）

### 5.6 `.vhd` / `.vhdx`（Hyper-V / Azure）

> - `.vhd`：Hyper-V 旧格式，单盘上限 **2 TB**，Azure 也在用
> - `.vhdx`：新格式，单盘上限 **64 TB**，支持更大扇区、断电更不容易坏
> - 一句话记住区别：**同一块盘，vhdx 更大、更能扛**

### 5.7 虚拟磁盘互转：`qemu-img`

PVE / KVM 自带的 `qemu-img` 能读写主流磁盘格式，转换一条命令搞定：

| 格式 | 名称 | 读写 |
|---|---|---|
| `raw` | 裸磁盘（= `.img`） | 读写 |
| `qcow2` | QEMU 主力格式 | 读写 |
| `qcow` / `qed` | 老格式 | 读写 |
| `vmdk` | VMware | 读写 |
| `vdi` | VirtualBox | 读写 |
| `vpc` | Hyper-V 旧格式（= `.vhd`） | 读写 |
| `vhdx` | Hyper-V 新格式 | 读写 |

```bash
# 任何格式 → qcow2（-p 显示进度；-f 源格式，-O 目标格式）
qemu-img convert -p -f vmdk -O qcow2 source.vmdk target.qcow2

# qcow2 → raw：转完就是 .img，可以走写盘流程
qemu-img convert -p -f qcow2 -O raw source.qcow2 disk.img

# 转换完先看一眼再动手
qemu-img info target.qcow2
```

> [!warning] 顺序别弄反
> `-f` 写的是**源**格式，`-O`（大写）写的是**目标**格式。写反了 qemu-img 会直接报错——别猜，看报错信息改。

### 5.8 打包导出：`.ova` / `.ovf`

> - `.ovf`：一个 XML **描述文件**（几核 CPU、多少内存、几张网卡、磁盘在哪）
> - `.ova`：一个 **tar 包** = `.ovf` 描述 + 一个或多个 `.vmdk` 磁盘 + 清单文件
> - 规律：**OVF 是说明书，OVA 是"说明书 + 零件"打包好的快递箱**

`.ova` 其实就是一个 tar 包，可以直接拆开看：

```bash
tar -tf vm.ova        # 只列出内容：vm.ovf / vm-disk-1.vmdk / vm.mf
tar -xf vm.ova        # 拆开，得到 .ovf + .vmdk
```

拿到 `.ova` 之后怎么用：

- **PVE 8.3 及以上**：Web 界面可以直接导入 / 上传 OVA、OVF，不用敲命令
- **更早版本或命令行**：先 `tar` 拆包，再用 `qm importovf` 按 `.ovf` 建虚拟机
- **只想要里面的磁盘**：拆包后把 `.vmdk` 交给 `qm disk import`

### 5.9 PVE 备份与容器模板：`.vma.zst` / `.tar.zst`

这两种经常被误当成"镜像"，其实不是：

> - `.vma.zst`：PVE 的**虚拟机备份包**（`vzdump` 产物），只能在 PVE 里**还原**，不能挂载、不能开机
> - `.tar.zst` / `.tar.gz`：PVE 的**容器（CT / LXC）模板**，里面是一整个根文件系统（`/etc`、`/usr`、`/bin`…），创建容器时被解包成容器根目录

```bash
# 还原虚拟机备份成一台新 VM（101）
qmrestore vzdump-qemu-100-2026_09_17-00_00_00.vma.zst 101

# 容器模板：先看有哪些、再下载（模板名以 pveam available 的实际输出为准）
pveam available | grep debian
pveam download local debian-12-standard_12.7-1_amd64.tar.zst
```

> [!tip] 大白话
> `.vma.zst` 是"系统镜像的**备份**"，不是"系统镜像"。像**行李寄存单**和**行李**的区别：拿着寄存单不能住人，得先去柜台取出来（还原）。

### 5.10 压缩过的成品盘：`.img.gz` / `.img.xz` / `.img.zst`

> - OpenWrt / iStoreOS / 树莓派固件下载下来常见 `.img.gz`（也有 `.img.xz`，压得更小、解得更慢）
> - 本质就是 `.img` 套了一层压缩壳，**写盘 / 导入工具都不认这层壳**

```bash
gunzip istoreos-x86-64.img.gz                    # 解压成 .img（原文件消失）
zcat istoreos-x86-64.img.gz > istoreos-x86-64.img  # 或者保留原文件
```

> [!tip] 两个例外
> - **balenaEtcher 可以直接选压缩镜像**（如 `.img.xz` / `.img.gz`），它自己会解压——写 SD 卡时省一步
> - **`qm importdisk` / `dd` 必须先解压**，喂给它们压缩包只会报格式错误

### 5.11 安装介质家族：光盘之外的那些

`.iso` 不是唯一的安装介质，这些也属于"要跑安装 / 引导流程"的那一类：

| 扩展名 | 是什么 | 特点 | 现在还用吗 |
|---|---|---|---|
| `.bin` + `.cue` | 老式光盘镜像 | 数据在 `.bin`，`.cue` 记轨道；**两者必须成对**，只拷一个没用 | 老软件 / 复古游戏 |
| `.nrg` | Nero 光盘镜像 | 私有格式，靠 Nero 或转换工具处理 | 基本淘汰 |
| `.dmg` | macOS 磁盘映像 | HFS+ / APFS，macOS 原生挂载 | 只在 Mac 场景 |
| `.wim` | Windows 映像 | **按文件**存（不是扇区），一个包里能放多个版本 | Windows 安装 / PE / 批量部署 |
| `.esd` | 加密压缩的 WIM | 压得更狠、只读，Win10 之后安装盘里常见 `install.esd` | Windows 安装盘 |
| `.gho` | Norton Ghost 备份 | 老式整盘 / 分区备份，要用 Ghost 或 PE 工具还原 | 老 PE 维护盘 |
| `.vfd` / `.flp` | 虚拟软盘 | 1.44 MB，装 BIOS / 固件刷新工具用 | 刷 BIOS 时还会遇到 |

> [!tip] `.wim` 和 `.iso` 的关系（很多人绕不清）
> 一个 Windows `.iso` 里装的是"引导 + 安装程序 + `install.wim`"——**真正的系统文件其实住在 `.wim` 里**，`.iso` 只是把它装进了一张"光盘"。
> `.wim` 是按**文件**存的（像把一个完整的盘目录树塞进 zip），不是按扇区，所以它**永远不能直接开机**，必须经过"展开到硬盘"这一步。

### 5.12 嵌入式 / 系统专有格式

> - `.squashfs`：只读压缩文件系统。多数 OpenWrt / iStoreOS 固件的 rootfs 就是它——**固件本体不可改**，你的配置写在另一个可写分区（overlay）里，所以"恢复出厂设置"清的是 overlay
> - `.trx` / 固件 `.bin`：路由器固件封装（OpenWrt 常见的 `factory.bin` 首刷固件、`sysupgrade.bin` 升级固件）
> - Android 的 `.img` 家族：`boot.img`（内核 + ramdisk）、`recovery.img`、`system.img`、`super.img`（动态分区）——**名字带 img，但不是"整块盘"**，是"某一个分区的镜像"，要用 `fastboot` 刷到对应分区
> - ARM 单板的 `.img`：树莓派这类就是标准"成品盘"，写卡 → 开机，没有 ISO 可找

> [!warning] 两种 `.bin`，别再搞混
> - 旁边有 `.cue` → **光盘镜像**
> - 从 OpenWrt / 路由器官网下载 → **固件**

### 5.13 一张表：手上的文件在 PVE 里怎么处理

| 你手上的文件 | PVE 里怎么处理 |
|---|---|
| `.iso` | 上传到 `local → ISO Images` → 建 VM 时挂成虚拟光驱 |
| `.img` / `.raw` | 上传到 `/var/lib/vz/template/iso/` → `qm disk import`（= `qm importdisk`） |
| `.qcow2` / `.vmdk` / `.vdi` / `.vhd` / `.vhdx` | 同样走 `qm disk import`，PVE 会自动转换成存储格式 |
| `.ova` / `.ovf` | PVE 8.3+ 用 Web 界面导入；命令行 `qm importovf`（一般先 `tar` 拆包） |
| `.img.gz` / `.img.xz` | **先解压**成 `.img`，再按上面处理 |
| `.vma.zst` | `qmrestore` 还原成新 VM（不是导入） |
| `.tar.zst` / `.tar.gz`（容器模板） | `pveam download` + 建 CT 时选用 |

关于 `qm disk import` 的两条硬事实（来自 PVE 官方 `qm` 手册）：

- **输入**：官方说明是"镜像格式必须被 `qemu-img` 支持"——所以 `raw` / `qcow2` / `vmdk` / `vdi` / `vhd` / `vhdx` 等基本都能直接喂进去
- **输出**：`--format` 可选项只有 `qcow2` / `raw` / `vmdk` 三种（不指定就跟随存储默认）

> [!tip] 延伸阅读
> 拿到镜像之后"用什么工具写盘 / 烧录、物理机和虚拟机各走什么流程"，见 [[虚拟机/ISO与IMG镜像烧录方法对比.md]]。

## 6. 常见问题：虚拟机 vs 物理机，用哪个镜像？

### 6.1 一句话答案

- 要**开箱即用**（软路由 iStoreOS / OpenWRT）→ 用 **IMG**
- 要**干净安装、自己配置**（Windows / Ubuntu）→ 用 **ISO**

### 6.2 速查表

| 场景 | 用哪个 | 怎么用 |
|------|--------|--------|
| 物理机刷软路由（iStoreOS / OpenWRT） | **IMG** | 解压 `.img.gz` → Etcher / Rufus / `dd` 写盘 |
| 物理机装常规系统（Windows / Ubuntu） | **ISO** | 刻录到 U 盘 → 启动 → 安装 |
| 虚拟机装新系统（自己配置） | **ISO** | 挂载为虚拟光驱 → 启动 → 安装 |
| 虚拟机直接跑软路由成品 | **IMG** | 上传 `/var/lib/vz/template/iso/` → `qm importdisk` 导入 |

### 6.3 本质区别

- **IMG = 成品盘**：分区 + 引导 + 系统全都有，物理机写盘、虚拟机导入，拿来就能开机
- **ISO = 安装入口**：物理机刻 U 盘、虚拟机挂光驱，都要先跑一遍安装程序

> [!tip] 速记
> **要开箱即用 → IMG；要自己装 → ISO。** 两个场景通用。

## 更新记录

- 2026-08-27：完善 ISO 与 IMG 笔记
  - 补 frontmatter、H1 标题、`[!info] 一句话总结`
  - 修复 PVE 存储库失效链接（原指向不存在的目录/锚点 → `[[PVE的学习/01-安装配置/PVE存储库#PVE 里的"两种存储库"]]`）
  - 核心概念补充 `[!tip] 大白话`（装修工具 / 成品房）
  - 修正标题间距与 `[!warning]` Callout 格式
  - 完善 2.4 PVE 导入 IMG 步骤：补 `.img.gz` 解压提示、"未使用磁盘 → 引导顺序"细节
  - 新增 §6 常见问题：虚拟机 vs 物理机镜像选择（速查表）
- 2026-09-17：补全其他镜像类型（§5 由 2 个格式扩为完整格式地图）
  - §5 改名「其他常见镜像格式（一次认清）」，新增三大类分类法（安装介质 / 磁盘镜像 / 打包备份）+ 全格式总览速查表（20 行）
  - 新增虚拟磁盘格式：`.vmdk`（含单文件 / 拆片 / flat 三种形态）、`.vdi`、`.vhd` / `.vhdx`（2 TB vs 64 TB）、`.qcow` / `.qed`
  - 新增 §5.7 虚拟磁盘互转：`qemu-img` 读写格式表 + `convert` 命令（含 `-f` / `-O` 易错点）
  - 新增打包导出 `.ova` / `.ovf`（tar 拆包 + PVE 8.3+ Web 界面导入 / 命令行 `qm importovf`）
  - 新增 PVE 备份与容器模板 `.vma.zst` / `.tar.zst`（`qmrestore` / `pveam`）
  - 新增压缩成品盘 `.img.gz` / `.img.xz` / `.img.zst`（解压命令 + Etcher 例外）
  - 新增安装介质家族 `.bin+.cue` / `.nrg` / `.dmg` / `.wim` / `.esd` / `.gho` / `.vfd`
  - 新增嵌入式专有格式 `.squashfs` / `.trx` / 固件 `.bin` / Android `.img` / ARM 单板 `.img`
  - 新增 §5.13 PVE 导入路径对照表，并按官方 `qm` 手册核实 `qm disk import` 的输入约束与 `--format` 目标格式
  - 补充「延伸阅读」双链到 [[虚拟机/ISO与IMG镜像烧录方法对比.md]]；frontmatter 补 tags（镜像格式 / qcow2 / vmdk）
