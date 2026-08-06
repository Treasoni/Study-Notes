---
title: "第三章：官方原版 HAOS 安装实战（实体机 + 虚拟机全平台）"
tags:
  - 智能家居/HomeAssistant
  - HAOS/部署教程
  - 学习笔记
created: 2026-08-06
updated: 2026-08-06
status: 已完成
source_project: haos-deploy-tutorial
chapter: 3
---

# 第三章：官方原版 HAOS 安装实战（实体机 + 虚拟机全平台）

> [!summary] 本章讲什么
> 本章是全文的实操核心：用官方原版 [[HAOS]] 镜像，在四类最常见平台上完成安装——实体机 x86-64、VMware Workstation、Proxmox VE（PVE）、群晖 Virtual Machine Manager（VMM）。每一节都按「取镜像 → 刷写/导入 → 引导设置 → 首次启动」的完整链路展开，并点出各平台独有的坑位（UEFI 引导项、PVE 默认 SCSI 盘、EFI 磁盘、磁盘控制器）。读完本章，你应该能在其中任意一个平台上把 HAOS 跑起来，看到 `http://homeassistant.local:8123` 的初始化向导。

> 前置提醒：镜像下载、SHA256 校验与烧录工具链已在第二章备好；为什么优先用 SSD、为什么要关 Secure Boot，请回看第二章。本章只讲「怎么装上」，国内源加速放到第四章——首次启动的漫长等待不是卡死，先别急着重装。安装过程中的所有参数都来自官方安装文档与社区验证过的教程，标注「替代配置」的地方表示可换成另一种同样可行的组合。

### 3.1 实体机 x86-64 刷写与 UEFI 引导

官方文档：[Generic x86-64 安装](https://www.home-assistant.io/installation/generic-x86-64)

实体机路线适合手里有 x86-64 迷你主机、NUC 或旧 PC 的场景。它的好处是硬件独占、性能上限最高，代价是刷写后目标盘会被清空、没有安装器可后悔。整条链路可以概括为四步：进 BIOS 改引导 → 刷写镜像 → 修正 UEFI 引导项 → 联网首次启动。

**镜像特性：写入即启动，无安装器**

`haos_generic-x86-64-{ver}.img.xz` 是「写入即启动」的整盘镜像：写进目标盘后，HAOS 的 OS + Supervisor + Core 一次到位，没有传统安装器。副作用是**写入会清空目标盘全部数据**，写入前务必确认选中的是目标盘，且该盘不需要保留任何其他数据。也正因为它没有安装器，第二章强调的「先校验 SHA256、再写盘」在这里格外重要——刷错镜像只能整盘重来。

**第一步：进 BIOS 开 UEFI、关 Secure Boot**

开机按 F2/Del 进 BIOS：引导模式设为 UEFI，关闭 Secure Boot。不需要 TPM。这里最容易漏的是「只开了 UEFI 但忘了关 Secure Boot」——Secure Boot 会拒绝未签名的引导程序，而 HAOS 的引导链不在它的白名单里，结果就是启动时被安全策略拦下、黑屏或回到 BIOS。判断是否漏关的标志：开机后没有任何 HAOS 相关文字就直接弹回 BIOS 设置界面。

**第二步：刷写（两种方法任选其一）**

> [!example] 方法 A：balenaEtcher
> 1. 先把 `.img.xz` 解压成 `.img`（Windows 用 7-Zip，Linux 用 `xz -dk`）；
> 2. 打开 balenaEtcher，选 **Flash from file** 指向解压后的 `.img`，再选目标盘，点 Flash；
> 3. 注意：**不要用 Flash from URL**。URL 刷写在镜像较大的 HAOS 场景容易中断，且无法先做完整性校验。

> [!example] 方法 B：Ubuntu Live USB + Disks
> 用 Ubuntu Live 启动后，打开 "Disks" 工具 → 选中目标盘 → 菜单里选 **Restore Disk Image** → 指向 `.img.xz` 或解压后的 `.img`。Disks 的好处是能直接吃 `.img.xz` 压缩格式，不用先解压，适合磁盘空间吃紧的环境。

> [!warning] 坑：target is busy
> Disks 恢复时报 "target is busy"，是因为目标盘的 Swap 分区仍被 Live 系统占用。先卸载目标盘所有分区并关闭 swap，再重新执行恢复：
> ```bash
> umount /dev/sdX* ; swapoff /dev/sdX1
> ```
> 这里 `sdX` 换成你的实际盘符（如 `sda`）。卸载后如果 Disks 仍报 busy，可在终端确认没有进程还在读写该盘（`lsof | grep /dev/sdX`）后再试一次。

**第三步：UEFI 引导与 bootx64.efi**

刷写完成后从目标盘重启。若提示找不到引导介质，是 UEFI 引导项没被正确登记——HAOS 的引导文件其实已经写在 EFI 分区里，只是缺一条 NVRAM 引导记录指向它。两个修法：

```bash
efibootmgr --create ... --loader '\EFI\BOOT\bootx64.efi'
```

`...` 处需按你的实际磁盘补 `--disk /dev/sdX --part N` 参数（N 是 EFI 分区序号，一般从 1 开始试）。更省事的办法是开机进 BIOS 启动菜单，手动选择 `\EFI\BOOT\bootx64.efi` 这一项——它通常是 HAOS 写入的标准引导路径，选一次即可。

**第四步：首次启动**

第一次开机**必须联网**——系统会自动下载最新版 Core 组件，断网会卡在等待界面。访问 `http://homeassistant.local`（备选主机名 `homeassistant`，或直接 `http://<IP>`）；若 80 端口被占用，访问 `http://homeassistant.local:8123`。

### 3.2 VMware Workstation 安装（含 .vmx EFI 配置）

官方文档：[Windows/VMware 安装](https://www.home-assistant.io/installation/windows)

VMware 路线适合「不想动实体机、只想在现有 Windows 上跑一个隔离环境」的场景。整体比实体机多一个关键动作：手动改 `.vmx` 让虚拟机用 EFI 引导。这也是 VMware 路径最容易翻车的一步，务必按顺序做。

**取镜像与解压**

下载 `haos_ova-{ver}.vmdk.zip`，解压得到 HAOS 的 vmdk 虚拟磁盘。注意要解压出 **vmdk 文件本体**，而不是只解压出一个文件夹——后续替换磁盘时如果复制错对象，VMware 会报找不到磁盘。

**新建虚拟机**

VMware Workstation 新建 VM，类型选 Linux → **Other Linux 5.x kernel 64-bit**。硬件参数：

- 内存 ≥ 2048 MB；
- CPU ≥ 2 核；
- 网络选 **Bridged 桥接**，且只在「复制物理网络连接状态」里勾选真实物理以太网适配器（不要选仅主机模式或无线网卡）。

网络用桥接是有原因的：HAOS 需要出现在局域网里，才能被 `homeassistant.local` 和手机 App 直接发现。如果选 NAT 或仅主机模式，虚拟机可能能上网，但局域网内的设备发现会出问题，App 会找不到 HA。

**替换虚拟磁盘**

> 一句话：把「VMware 新建向导自动生成的**空白硬盘**」换成「HAOS 自带的**系统硬盘**」。HAOS 的 vmdk 本身就是一个装好系统的完整硬盘，我们要让虚拟机从它启动，而不是从向导随手建的空盘启动。

新建虚拟机时，VMware 会自动创建一块空白虚拟硬盘——文件名就是虚拟机名（`home-assistant.vmdk`），相当于一块没装系统的空盘。按下面三步把它换掉：

| 步骤 | 操作 | 为什么 |
|------|------|--------|
| 1 | 删除向导自动生成的 vmdk | 空盘没用，留着会干扰启动 |
| 2 | 把 HAOS 解压出的 vmdk **改名为** `home-assistant.vmdk` | 见下方「为什么改名」 |
| 3 | 复制进该 VM 的目录 | 让 VMware 找到它 |

**为什么改名最稳妥**：VM 目录里的 `.vmx` 配置文件写死了「系统盘 = `home-assistant.vmdk`」。HAOS 盘改成同名文件放进去，等于直接顶替原盘——配置文件一字不用改，VMware 开机自动就从 HAOS 启动。改名不是必须的，但社区验证这样做最稳，能避免 VMware 把 HAOS 盘当成「额外挂载的数据盘」、从而不从它启动，还得手动删空盘、调启动顺序。

**关键：编辑 .vmx 加 EFI**

> [!warning] VMware 路径最容易翻车的一步
> VMware 新建虚拟机默认用 BIOS 引导，而 HAOS 只认 UEFI。必须用文本编辑器打开 VM 目录下的 `.vmx` 文件，追加一行并保存：

```text
firmware = "efi"
```

不加这一行，VM 启动后会一直黑屏或进不了系统。加完后可以用记事本或任意编辑器保存，注意 `.vmx` 是纯文本，保存后 VMware 下次开机才会读取到新配置。

**启动与验证**

启动虚拟机。若弹出 "side channel mitigations" 提示，点 OK 继续。等网络就绪后访问 `http://homeassistant.local`。

> [!warning] 坑：vmdk 找不到
> 提示找不到 vmdk，通常是解压后复制了**整个文件夹**而不是 vmdk 文件本体；确认复制到 VM 目录的是 `home-assistant.vmdk` 这个文件，而不是一个包含它的目录。

### 3.3 PVE 安装（qcow2 导入 + 总线/引导顺序修正）

社区权威教程：[PVE 安装 HAOS](https://wiki.slarker.me/pve/haos.html)

PVE 路线适合已经跑着 Proxmox 虚拟化平台、想把 HAOS 作为一台虚拟机托管起来的场景。它比 VMware 多两个概念：qcow2 需要命令行导入，且导入后必须修正磁盘总线与引导顺序。全流程可以概括为「建 VM → scp 上传 → qm importdisk → 改 SATA → 引导置顶」。

**取镜像与解压**

下载 `haos_ova-{ver}.qcow2.xz`，解压得到 qcow2 磁盘镜像。

**新建虚拟机（关键参数）**

- 机型（Machine）：**i440fx**；
- BIOS：**OVMF(UEFI)**，且**取消勾选「添加 EFI 磁盘」**——HAOS 自带 EFI 分区，不需要 PVE 再建一个；
- **删除默认的 SCSI 磁盘**——这是后续引导顺序乱的根源；
- CPU 2 核、类型 host；
- 内存 2048 MB。

两个参数最容易踩坑：其一，勾选「添加 EFI 磁盘」会在导入后多出一块空的 EFI 盘抢占引导顺序，所以必须取消；其二，默认创建的 SCSI 盘是空盘，不删掉它，引导顺序里它会排在 HAOS 盘前面，导致反复重启也进不了系统。

**上传 qcow2（不能走 ISO 上传）**

qcow2 不属于 ISO 镜像，不能从 Web 界面的 ISO 上传通道走，用 `scp` 传到 PVE 的 `/tmp`：

```bash
scp haos_ova-{ver}.qcow2 root@<PVE-IP>:/tmp/
```

**导入为虚拟磁盘**

在 PVE 节点的 shell 里执行（`100` 换成你的实际 VMID）：

```bash
qm importdisk 100 /tmp/haos_ova-{ver}.qcow2 local
```

`local` 是存储名，如果你的 PVE 存储不是这个名字，按实际存储名替换。导入完成后，命令会提示生成了一块新磁盘。

**总线与引导顺序修正**

导入后回到 Web 界面，硬件列表会出现一块「未使用的磁盘0」：

1. 选中它 → 添加；
2. **总线改 SATA**（这是与默认 SCSI 的关键差异）；
3. 到「选项 → 引导顺序」，把 `sata0` 置顶。

> [!tip] 替代配置
> 如果你更熟悉 VirtIO，q35 + OVMF + VirtIO SCSI、把 `scsi0` 置首同样可行（即上述 i440fx + SATA 的反向组合）。另外 PVE 8.3 起支持直接导入 OVA，可以少走一步。按你的习惯二选一即可，不要混合使用——混合总线配置会让引导顺序变得难以排查。

**启动与访问**

启动虚拟机。HAOS 首次启动会联网拉组件，国内网络下较慢属正常。访问 `http://<IP>:8123`（PVE 环境下 `homeassistant.local` 不一定总是解析成功，直接用 IP 最稳）。

> [!warning] 坑：卡在启动
> 磁盘空间不足，或默认 SCSI 盘没删、导入盘没改 SATA，都会导致卡住或引导顺序异常。按上面步骤逐项核对，尤其是「未使用的磁盘0」有没有真的挂上并置顶。

### 3.4 群晖 VMM 安装（固件与磁盘控制器关键参数）

官方 VMM 走 vmdk/ova 导入；社区参考文章 [mingyue5826 的群晖 VMM 部署](https://www.cnblogs.com/mingyue5826/p/18958567)（该文用冬瓜 ISO 流程，原理与本节一致）。

群晖路线适合「已经有了群晖 NAS、不想再添一台主机」的场景。它的问题在于 VMM 对虚拟机的默认设置偏保守，HAOS 对固件和磁盘控制器的要求又很具体，因此本节把三个关键参数单独拎出来讲。

**前置**

DSM 7.0+ 安装套件 **Virtual Machine Manager**。网络建议开启 **Open vSwitch**——它是 HAOS 虚拟机与宿主机/局域网互通的关键，不开会导致「虚拟机开得起来但访问不到」。如果已经建过其他虚拟机，注意 VMM 的虚拟交换机设置里要确保 HAOS 走的是桥接出来的局域网网段，而不是 NAT。

**导入与关键参数**

在 VMM 里「新增 → 导入」选择 vmdk 或 ova。三个参数必须盯死：

- **固件必须 UEFI**（BIOS 兼容模式起不来）；
- **磁盘控制器 SATA**；
- **磁盘容量 ≥ 32GB**（Home Assistant 数据库长期高频写入，容量太小会频繁触发存储告警）。

这三个参数在 VMM 向导里不一定显眼，默认值往往不是 HAOS 要的——固件默认可能是 BIOS，磁盘控制器默认可能是 IDE/VirtIO。导入后如果发现不对，可以在 VM 设置里改，但某些版本改固件需要重建虚拟机，所以**导入前先确认**更省事。

**首次启动**

VMM 启动 HAOS 后，第一次开机 20 分钟到数小时都算正常——尤其在国内网络下首次拉取组件。这期间不要断电、不要反复重启。访问 `http://<IP>:8123`。

> [!warning] 坑：虚拟机起不来 / 网络不通
> 起不来：先查固件是否 UEFI、磁盘控制器是否 SATA；能起来但访问不到：查 Open vSwitch 是否开启，必要时在 VMM 网络设置里重新选择 Open vSwitch。另外群晖 VMM 对虚拟机磁盘空间是「占用量」而非「预分配」，容量给 32GB 不会立刻吃掉 NAS 32GB 空间，放心配置。

### 3.5 跨平台共性、首次启动验证与常见安装坑速查

**跨平台共性（四个平台全部适用）**

- 引导：UEFI/EFI，关闭 Secure Boot，不需要 TPM；
- 资源：2 vCPU + 2GB 内存起步；
- 磁盘：≥ 32GB，总线用 SATA；
- 首次启动必须联网，会自动拉取组件（国内约 700MB，可能很慢）；
- 访问地址统一：`http://homeassistant.local:8123` 或 `http://<IP>:8123`。

把这五条记牢，等于掌握了所有平台的「最小公共约束」。其余差异只是不同平台把这些约束摆在了不同的设置入口里——实体机在 BIOS、VMware 在 `.vmx`、PVE 在 VM 硬件面板、群晖在 VMM 向导。

**首次启动验证流程**

1. 浏览器打开 `http://homeassistant.local:8123`（备选 `homeassistant` 或 `http://<IP>`）；
2. 看到「创建用户、设置住宅名称与地区」的初始化向导，说明 Core 已就绪，安装成功；
3. 若长时间停在加载页/转圈：先确认是否拿到 IP（看路由器后台或 VM 控制台），再检查时间同步（见第四章与第八章），不要盲目重装。

**常见安装坑速查**

| 平台 | 现象 | 根因 | 解决 |
|------|------|------|------|
| 实体机 | Disks 报 target is busy | 目标盘 Swap 分区被占用 | 先 `umount /dev/sdX*` + `swapoff` 再恢复 |
| 实体机 | 找不到引导介质 | UEFI 引导项未登记 | 手动指定 `\EFI\BOOT\bootx64.efi` 或 `efibootmgr --create ... --loader '\EFI\BOOT\bootx64.efi'` |
| VMware | 开机黑屏 / 起不来 | 默认 BIOS 引导 | `.vmx` 加 `firmware = "efi"` |
| VMware | vmdk 找不到 | 复制了文件夹而非文件 | 复制 vmdk 文件本体并改名 `home-assistant.vmdk` |
| PVE | 引导顺序混乱 | 默认 SCSI 盘未删 | 删除默认 SCSI 盘 |
| PVE | 导入盘没挂上 | 导入后默认「未使用」 | 手动添加、总线改 SATA、`sata0` 置首 |
| 群晖 VMM | 虚拟机起不来 | 固件/磁盘控制器错误 | 固件 UEFI + SATA 控制器 + 容量 ≥32GB |
| 群晖 VMM | 能开但访问不到 | Open vSwitch 未开启 | 在 VMM 网络设置里开启 Open vSwitch |

> [!tip] 下一步预告
> 装完只能算「跑起来」。国内网络下你会立刻撞上两个问题：Add-on 商店加载慢、Docker 镜像拉不动。这正是第四章要解决的手动国内源配置。进入第四章前，先确认你的 [[HAOS]] 能通过 `homeassistant.local:8123` 进入向导——这是后续所有配置的前提。也可以对照既有的 [[Home Assistant 三种部署方式对比与选型]]，确认 HAOS 路径符合你的选型判断。

---

## 本章 Checklist

- [ ] 实体机：已开 UEFI、关 Secure Boot，用 balenaEtcher / Disks 刷入 `haos_generic-x86-64-{ver}.img.xz`
- [ ] 实体机：遇 target is busy 时已卸载 Swap 分区；引导失败时已指定 `\EFI\BOOT\bootx64.efi`
- [ ] VMware：虚拟机类型 Other Linux 5.x 64-bit，内存 ≥2048MB、CPU ≥2 核、网络 Bridged 桥接
- [ ] VMware：已替换为 `home-assistant.vmdk`，并在 `.vmx` 中加入 `firmware = "efi"`
- [ ] PVE：i440fx + OVMF(UEFI)（未添加 EFI 磁盘），已删除默认 SCSI 盘
- [ ] PVE：已 `scp` 上传 qcow2 并执行 `qm importdisk`，导入盘总线改 SATA、`sata0` 置顶
- [ ] 群晖 VMM：固件 UEFI、磁盘控制器 SATA、容量 ≥32GB，已开启 Open vSwitch
- [ ] 已确认首次启动保持联网，能通过 `http://homeassistant.local:8123`（或 `http://<IP>:8123`）进入初始化向导

---

> ⬅️ 上一章：[[02_部署前置准备|第二章：部署前置准备——存储、固件、镜像与工具链]] ｜ 📖 [[部署 HAOS 详细教程|返回索引]] ｜ 下一章：[[04_手动配置国内源|第四章：手动配置国内源（官方原版加速核心）]] ➡️
