# 虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI) — 深度素材（P2）

> 运行：vm-bios-uefi（learning-note-flow P2）｜日期：2026-09-18｜方向：D 综合（选型决策 + 三平台实操 + UEFI 排错）
> 方法：3 个深读子代理按来源组分批精读，页面正文经 `crawl.sh` 落入本地缓存后逐条抽取论断。
> 引文核对：**94 条引文逐条回源比对，93 条逐字命中；1 条归属错误已更正**（见 §3.4 注）。
> 缓存布局：`.cache/p2_sources/{组}/{来源ID}_{域名}.md`（16 个来源）。

---

## 1. Scope

- **覆盖**：通用固件概念与启动链路；VMware Workstation、VirtualBox、PVE 三平台的固件选项与后果；客户机系统（Windows 11、Hyper-V 代次）的硬性要求；选 UEFI 后的故障现象与排查。
- **不在范围**：物理机 BIOS/UEFI 设置（宿主侧 VT-x 开启见既有笔记 [[虚拟机/虚拟机的概念和使用.md]]）；其他 hypervisor（Xen/KVM 原生）未纳入。
- **范围外但需要的一句话结论**：Hyper-V 仅作代次对照（第 2 代 = UEFI，第 1 代 = Legacy BIOS）[GEN12]。

## 2. Source Table

| ID | 标题（简） | 层级 | 日期 | 缓存路径 |
| --- | --- | --- | --- | --- |
| L1-1 | VMware Workstation Pro — Configure a Firmware Type | official | 2026-03-06 | `desktop-fw/L1-1_techdocs_broadcom_com.md` |
| L1-2 | VirtualBox 用户手册 6.0 — Alternative Firmware (EFI) | official | 未知（Release 6.0，© 2004–2020） | `desktop-fw/L1-2_docs_oracle_com.md` |
| L1-3 | VirtualBox 手册主干源文件 — Alternative Firmware (UEFI) | official | 未知（master 分支） | `desktop-fw/L1-3_raw_githubusercontent_com.md` |
| L3-5 | VirtualBox ticket #18282 — EFI shell 不出现 | community | 2019-01-04，2019-04-17 关闭 | `desktop-fw/L3-5_www_virtualbox_org.md` |
| L2-1 | Proxmox VE Administration Guide — Qemu/KVM Virtual Machines | official | 2026-09-15（v9.2.11 构建） | `pve-fw/L2-1_pve_proxmox_com.md` |
| L2-2 | Proxmox VE — qm.conf(5) 手册页 | official | 2026-09-15（v9.2.11 构建） | `pve-fw/L2-2_pve_proxmox_com.md` |
| L2-3 | Proxmox VE Wiki — OVMF/UEFI Boot Entries | 官方 wiki（保守按 community 计） | 未知（仅得 oldid=12527） | `pve-fw/L2-3_pve_proxmox_com.md` |
| L2-4 | pve-docs 源文件 — PCI(e) Passthrough | official | 未知（master 快照） | `pve-fw/L2-4_raw_githubusercontent_com.md` |
| L2-5 | Best Practice Configurations for VMs on Proxmox VE（Starline） | community | 2026-06-26 | `pve-fw/L2-5_www_starline_de.md` |
| L1-4 | Windows 11 requirements — Microsoft Learn | official | 2026-07-14 | `guest-os/L1-4_learn_microsoft_com.md` |
| L1-5 | Windows 11 Installation Fails on ESXi 7.0U3（Broadcom KB 408976） | official | 未知（Updated On 为空） | `guest-os/L1-5_knowledge_broadcom_com.md` |
| L3-1 | VM fails to boot when changing the Firmware from BIOS to EFI（Broadcom KB 384912） | official | 未知（Updated On 为空） | `guest-os/L3-1_knowledge_broadcom_com.md` |
| L3-3 | Troubleshoot UEFI boot failures with Azure Linux images — MS Learn | official | 2026-08-31 | `guest-os/L3-3_learn_microsoft_com.md` |
| GEN12 | Should I create a generation 1 or 2 VM in Hyper-V? | official | 2025-06-18 | `guest-os/GEN12_learn_microsoft_com.md` |
| GEN2SEC | Generation 2 VM security settings for Hyper-V | official | 2025-07-01 | `guest-os/GEN2SEC_learn_microsoft_com.md` |
| MBR2GPT | MBR2GPT.EXE — Microsoft Learn | official | 2026-07-14 | `guest-os/MBR2GPT_learn_microsoft_com.md` |

**层级统计**：16 个来源 —— official 13、官方 wiki 1、community 2。官方占比 81%。

**相对 P1 的两处修正**：
1. L2-3（Proxmox wiki）在 P1 记为「官方文档」，深读后按 wiki（非参考手册）保守降为 community 层级。
2. **L3-4（华为企业支持页）不可取证，已从来源表剔除**：`crawl.sh` 报 `Blocked by anti-bot protection: Structural: minimal_text, no_content_elements, script_heavy_shell`；两次 `curl` 兜底分别只拿到反爬 JS（446 B）与 SPA 外壳（3800 B），无可读正文。**该来源的任何说法均不得写入笔记**。

## 3. Claim / Source Map

引用格式：`[来源ID · 小节]`；加引号者为逐字原文（已回源核对）；标 `(推理)` 者为无直接原文支持的归纳。

### 3.1 通用：固件做什么、两种模式的本质差异

- 虚拟机需要一份固件来模拟 PC；它在启动早期执行、负责基本硬件初始化并提供接口，PC 上通常称 BIOS 或 (U)EFI [L2-1 · BIOS and UEFI]。
- VMware 把客户机固件类型限定为两个选项：UEFI 与 Legacy BIOS，无第三项（选项表原文 `"Legacy BIOS | Standard BIOS firmware."`）[L1-1 · Configure a Firmware Type]。
- **BIOS/EFI 与 MBR/GPT 是绑定的**：官方定性切换固件后无法启动属于预期行为，因为改固件不受支持 —— 原文 `"BIOS uses MBR (Master Boot Record) partitioning and EFI requires GPT (GUID Partition Table) partitioning on the VM disks"`，且切换时界面会警告已装客户机可能变得无法启动 [L3-1 · Cause]。
- VMware 官方对 UEFI 相对 BIOS 的说明只有一句「架构上有优势」，**未给任何选型场景建议**（选项表原文片段 `"architectural advantages over"`）[L1-1 · Configure a Firmware Type]（推理：官方只给前置条件与警告，场景建议需自行归纳）。
- 官方解释 Secure Boot 的机制是拒绝加载签名不被接受的驱动与加载器 [L1-1 · Configure a Firmware Type]（原文片段 `"not signed with an acceptable digital signature"`）。

### 3.2 VMware Workstation / ESXi

- **选 UEFI 的四项前置条件**：客户机系统支持 UEFI、未启用 VBS、硬件版本 ≥ 8、客户机为 Windows 8/10/2012/2016 [L1-1 · Configure a Firmware Type]（原文片段 `"hardware version 8 or later"`）。
- **选 Secure Boot 的额外前置**：固件类型已是 UEFI 且硬件版本 ≥ 14（原文片段 `"hardware version 14 or later"`）[L1-1]。
- ⚠️ **装完系统再改固件类型，可能导致虚拟机启动过程失败**：原文 `"might cause the virtual machine boot process to fail"` [L1-1 · 注意事项]。
- 启用 VBS 时，固件类型被固定为 UEFI 并勾选 Secure Boot，且两项**均不可编辑**：原文 `"You cannot edit the firmware type"` [L1-1 · 注意事项]。
- 设置入口：Settings → Options → Advanced → **Firmware type** 区域 [L1-1 · 步骤 1-3]（原文片段 `"In the Firmware type section"`）。
- Windows 11 在 **ESXi** 上的落地清单（注意适用环境是 ESXi 7.x/8.x，不是 Workstation）：固件设为 EFI —— 原文标注 `"Set to EFI (this is VMware's term for UEFI)"`；必须启用 Secure Boot（`"Must be enabled in VM settings"`）；需要 vTPM，而 vTPM 需要虚拟机加密、加密需要 KMS（`"This needs VM encryption"`）；硬件版本 ≥ 14（`"Use hardware version 14 or later"`）；最低 64 GB 虚拟磁盘（`"Minimum 64 GB virtual disk"`）[L1-5 · Resolution]。

### 3.3 VirtualBox

- 6.0 手册把 EFI 支持标注为**实验性**：原文 `"EFI support is experimental"`；默认固件为 BIOS；切换用 `VBoxManage modifyvm --firmware efi`，回退用 `--firmware bios` [L1-2 · 3.14]。
- 6.0 手册记载的限制：Windows 7 客户机**无法**在 EFI 实现下启动（`"unable to boot with the Oracle VM"`）；运行中的客户机内**无法操作 EFI 变量**（`"not possible to manipulate EFI variables"`，如 Mac 客户机用 nvram 设 boot-args 不生效），替代做法是 `setextradata` 写 `VBoxInternal2/EfiBootArgs`；EFI 默认分辨率 1024x768（`"The default resolution is 1024x768"`），且**只能在虚拟机关机状态下修改**（`"only be changed when the VM is powered off"`）；EFI 提供 GOP 与 UGA 两种视频接口 [L1-2 · 3.14.1 / 3.14.2]。
- 现行主干手册同节标题已改为 **Alternative Firmware (UEFI)**，正文称产品支持 UEFI（`"includes support for the Unified Extensible Firmware Interface"`），**全节不再出现 experimental**；仍写明默认使用 BIOS 固件（`"uses the BIOS firmware"`）；命令行仍是 `--firmware efi`；**新增**「多数现代 macOS 与 Windows 需要 UEFI、所有 Arm VM 需要 UEFI」（`"All Arm VMs require UEFI"`）；另可用于 UEFI 应用开发测试（`"development and testing of UEFI applications"`）[L1-3 · Alternative Firmware (UEFI)]。
- **已知具体失败行为**（2019，已于 6.0.5 修复）：当图形控制器不是 VBoxVGA（即选 VMSVGA 或 VBoxSVGA）且未提供可引导介质时，**EFI shell 始终不出现、安装无法进行**（`"the EFI shell never comes up"`），且 `EfiGopMode`、`EfiGraphicsResolution` 等 ExtraData 全部被忽略（`"none of the following ExtraData are honored"`）；报告者补充现象是**完全不启动**（`"No booting, no go"`）；开发者的根因解释是当时 EFI 固件里**没有**处理 VMSVGA/VBoxSVGA 的图形驱动（`"no graphics driver in the EFI firmware"`）；报告者以 `r128870`（6.0.5）确认修复，ticket 关闭为 fixed [L3-5 · Description / comment 5 / comment 12]。

### 3.4 PVE

- 默认固件是 SeaBIOS，官方称其适合大多数标准场景：原文 `"By default QEMU uses SeaBIOS"` [L2-1 · BIOS and UEFI]。
- **官方给出的切换判据（最有价值的一条）**：「多数情况下，只有当你计划使用 PCIe 直通时，才需要从默认的 SeaBIOS 换到 OVMF」—— 原文 `"In most cases you want to switch from the default SeaBIOS to OVMF only if you plan to use PCIe passthrough."` [L2-1 · System Settings]。
- 但客户机系统的硬性要求会**压过**上述默认：部分操作系统（如 Windows 11）可能需要 UEFI 实现，此时原文写明 `"you must use OVMF instead"` [L2-1 · BIOS and UEFI]。
- arm64 主机上 OVMF 是默认且唯一选项：原文 `"bios=ovmf is the only supported setting"`，因为 SeaBIOS 仅支持 x86 [L2-1 · BIOS and UEFI]。
- 用 OVMF 时**必须存在 EFI Disk** 来保存 boot order 等信息：原文 `"there needs to be an EFI Disk"`；该盘会纳入备份与快照，且**只能有一个** [L2-1 · BIOS and UEFI]。
- 创建命令：`qm set <vmid> -efidisk0 <storage>:1,format=<format>,efitype=4m,pre-enrolled-keys=1` [L2-1 · BIOS and UEFI]。
- **efitype 应始终用 4m**（支持 Secure Boot、空间更大），GUI 默认即 4m，2m 仅为向后兼容：原文 `"this should always be _4m_"`；已有 2m efidisk 想启用 Secure Boot **必须删除重建**（原文 `"you need to recreate the efidisk"`），且会**重置 OVMF 菜单里的自定义配置** [L2-1 · BIOS and UEFI]。
- `pre-enroll-keys` 会**默认启用 Secure Boot**，但仍可在 VM 内的 OVMF 菜单关闭 [L2-1 · BIOS and UEFI]。
- `bios` 选项取值与默认：`bios: <ovmf | seabios>`，默认 `seabios`；手册对这一项的**全部说明只有一句** `"Select BIOS implementation."`，未附任何限制或机型约束 [L2-2 · Options / bios]。
- `efidisk0` 的完整签名含六个子项：`file`、`efitype`、`format`、`ms-cert`、`pre-enrolled-keys`、`size` [L2-2 · Options / efidisk0]。
- `efitype` 默认 2m，4m「更新且被推荐，是 Secure Boot 的必需条件」（原文片段 `"required for Secure Boot"`）[L2-2 · Options / efidisk0]。
- `efidisk0` 的 `size` 子项**纯属信息性、没有实际作用**：原文 `"purely informational and has no effect"` [L2-2 · Options / efidisk0]。
- 机型选项：Intel vIOMMU 要求机型为 q35（原文片段 `"Intel vIOMMU needs q35"`）[L2-2 · Options / machine]。
- **直通场景的三条官方结论**：GPU 直通最佳兼容组合是 q35 + OVMF（而非 SeaBIOS）+ PCIe（原文片段 `"best compatibility is reached when using 'q35'"`）；若用 OVMF 做 GPU 直通，GPU 必须有 UEFI-capable ROM，否则原文要求 `"otherwise use SeaBIOS instead"`；PCIe 直通**只在 q35 上可用**（`"PCIe passthrough is only available on q35"`），而 PCI 直通在 i440fx 与 q35 都可用 [L2-4 · VM Configuration / PCI(e) Passthrough]。
- 引导解析链路：固件必须知道从 ESP 启动哪个 bootloader（`"the firmware has to know which bootloader"`）；当 EFIVARS 里没有 boot entry 时，固件尝试加载回退路径 `$ESP/EFI/BOOT/BOOTX64.efi`（`"it tries to load the fallback"`）；若回退也失败，**虚拟机会被引导进入 EFI Shell**（`"the VM gets booted into the EFI Shell"`）[L2-3 · Introduction]。
- 进入 OVMF 菜单：splash 出现时**恰好按一次 ESC**（`"press ESC exactly once"`），当前版本还需选择 "EFI Firmware Setup" 条目；添加引导项的路径是 Boot Maintenance Manager → Boot Options → **Add Boot Option**（`"Add Boot Option"`），然后选带 ESP 的磁盘 [L2-3 · Add a Boot Option]。

> **⚠️ 引文归属更正（本轮核对发现）**：子代理把 `"cannot be changed (only removed) once created"` 挂在 L2-2 名下，但该句在 L2-2 **不存在**（`only removed` 在该文件 0 命中）。逐字原文出自 **L2-1** 的 TPM 小节：`"A TPM is added by specifying a tpmstate volume. This works similar to an efidisk, in that it cannot be changed (only removed) once created."`；L2-2 里对应的不可变标注在 `tpmstate` 的 `version` 子项：`"v2.0 is newer and should be preferred. Note that this cannot be changed later on."`。**结论不变**（`bios` 项确实没有任何不可变标注），但落笔时必须用上面的准确出处。

### 3.5 客户机系统的硬性要求

- Windows 11 硬件要求（物理设备）原文：「System firmware: **UEFI, Secure Boot capable**」；「**TPM**: Trusted Platform Module (TPM) **version 2.0**」[L1-4 · Hardware requirements]。
- Windows 11 在**虚拟机**中的配置要求原文：`Generation: 2`；并附 Note：`"In-place upgrade of existing generation 1 VMs to Windows 11 isn't possible."`；Hyper-V 场景要求 `"Secure boot capable, virtual TPM enabled"`；内存 4 GB 以上；处理器 `"Two or more virtual processors"`；宿主处理器需在 BIOS 中启用虚拟化（`"must be enabled in the BIOS"`）[L1-4 · Virtual machine support]。
- **Hyper-V 代次对照的官方表达方式**是设备替换表而非否定句：Generation 1 的 Device 列 `Legacy BIOS` 对应 Generation 2 的 Replacement 列 `UEFI firmware`，Enhancements 列 `Secure Boot`；另有原文「For generation 2 VMs, Hyper-V provides virtual firmware to virtual machines that is independent of what's on the Hyper-V host.」[GEN12 · 代次对照表 / Use UEFI firmware]。
- **Secure Boot 的两条官方表述**（可支撑「未签名即被拦」的说法）：`"Secure Boot verifies the boot loader is signed by a trusted authority in the UEFI database."`；`"If these applications aren't digitally signed correctly, you must disable Secure Boot for the virtual machine."` [GEN12 · Secure Boot / Use UEFI firmware]。
- Secure Boot 的作用范围原文还包括 UEFI 驱动（option ROM）：`"helps prevent unauthorized firmware, operating systems, or Unified Extensible Firmware Interface (UEFI) drivers (also known as option ROMs) from running at boot time. Secure Boot is enabled by default."` [GEN2SEC · Secure Boot]。
- **MBR → GPT 的官方约束**：`mbr2gpt` **不能**用于非系统盘（`"The tool can't be used to convert non-system disks from MBR to GPT"`）；MBR 分区表最多三个主分区（`"at most three primary partitions in the MBR partition table"`）；转换完成后**固件必须改配为 UEFI 模式引导**（`"the firmware must be reconfigured to boot in UEFI mode"`）；Windows 7/8/8.1 的离线转换不受官方支持；**该页全文不含 virtual machine / Hyper-V / vSphere 字样**，即虚拟机场景的专属限制不在此页，而由 [L3-1 · Resolution] 给出（须先转 GPT 再切 EFI，且需客户机系统厂商支持）[MBR2GPT]。

## 4. 排错层：症状 → 根因 → 处置

| # | 症状 | 根因（来源） | 处置（来源） |
| --- | --- | --- | --- |
| 1 | 把固件从 BIOS 切到 EFI 后虚拟机无法启动 | 官方定性为预期行为：改固件不受支持，BIOS 用 MBR、EFI 需 GPT，切换不会转换分区表 [L3-1 · Cause] | ① 重建 VM、选定固件后挂原有硬盘；② 切 EFI **前**先把磁盘转 GPT（`mbr2gpt.exe`，需客户机系统厂商支持）[L3-1 · Resolution] |
| 2 | 启动后停在 EFI Shell / 没有引导项 | EFIVARS 中无 boot entry，回退加载 `$ESP/EFI/BOOT/BOOTX64.efi` 也失败 [L2-3 · Introduction] | 进 OVMF 菜单（splash 时按一次 ESC）→ Boot Maintenance Manager → Boot Options → Add Boot Option，选带 ESP 的磁盘 [L2-3] |
| 3 | 找不到 UEFI 引导加载程序（启动诊断报 `"The boot loader did not load an operating system"`） | EFI 系统分区被删除或缺失 [L3-3 · Scenario 1] | 用 `gdisk` 以类型码 `ef00` 在正确扇区重建 EFI 系统分区 [L3-3 · Scenario 1] |
| 4 | UEFI 启动分区损坏（`"The UEFI boot partition is corrupted"`） | ESP 文件系统损坏 [L3-3 · Scenario 2] | `fsck.vfat` 清理修复 [L3-3 · Scenario 2] |
| 5 | /boot 分区内容被删除且无法恢复 | 引导所需内容整体丢失 [L3-3 · Scenario 3] | 原文明确：`"restoring the VM from a backup is the only option"` [L3-3 · Scenario 3] |
| 6 | VirtualBox：无引导介质时看不到 EFI Shell、安装无法进行 | 当时 EFI 固件缺 VMSVGA/VBoxSVGA 图形驱动（图形控制器非 VBoxVGA 时触发）[L3-5] | 升级到 6.0.5（`r128870`）及以上；临时规避可改图形控制器 [L3-5 · comment 5/12] |
| 7 | PVE：UEFI 虚拟机启动异常 | 官方手册只说明「用 OVMF 需要 EFI Disk 保存 boot order」，**未描述缺失 efidisk0 的失败现象** [L2-1]；wiki 侧只有第 2 行的 EFI Shell 链路 | 按第 2 行处置；**此格属未闭合缺口**（见 §7） |
| 8 | Secure Boot 导致引导程序/驱动无法加载 | Secure Boot 只放行 UEFI 数据库中受信签名的引导加载程序与 option ROM [GEN12 / GEN2SEC] | 为对象签名，或在 VM 内/设置中关闭 Secure Boot（VMware 侧可用 VBS 场景不可编辑，见 §3.2）[GEN12 / GEN2SEC / L1-1] |

## 5. Contradictions / 口径差异

1. **OVMF 是否该作为新 VM 默认**：官方说默认 SeaBIOS、多数情况只有做 PCIe 直通才需切换 [L2-1]；社区实践主张新 VM 一律 OVMF、`"SeaBIOS should only be used for legacy systems"` [L2-5]。**取向不同，非直接互斥**，落笔时须并列并标明各自层级。
2. **vTPM/TPM 2.0 的前置条件**：社区来源明确写前提是「机型 q35 + BIOS OVMF」（`"Machine Type **q35** and BIOS **OVMF (UEFI)**"`）[L2-5]；官方 [L2-1] 只讲通过 `tpmstate` 卷添加、**未写机型或固件前提** —— 属「一方声明、另一方未声明」，不能当作官方口径。
3. **机型与固件的耦合程度**：官方直通文档建议 GPU 直通用 q35 + OVMF [L2-4]；官方机型说明称 PCI 直通在 i440fx 与 q35 都可用 [L2-1]；社区把机型与固件列为两个**独立**选项 [L2-5]。三者宽严不一。
4. **VirtualBox 限制清单的版本差异**：6.0 手册列了多项限制 [L1-2]，主干同节**一项都不列** [L1-3] —— 属版本演进，不是同版本冲突；引用时须带版本。
5. **VMware 对 UEFI 客户机范围的声明**窄于 VirtualBox：前者限 Windows 8/10/2012/2016 [L1-1]，后者称多数现代 macOS/Windows 可用 [L1-3]。不同厂商的范围声明，不构成同一事实的对立。
6. **「MBR」一词的歧义**（引用时须说明）：[L3-1] 用 MBR 指**纯 MBR 分区方案**，而 [L3-3] 的 `gdisk` 输出显示 GPT 磁盘带 `MBR: protective`（GPT 的兼容外壳）。直接把 L3-1 那句读成「GPT 磁盘没有 MBR」是误读。

## 6. Practical Guidance（可直接落进笔记的要点）

- **默认选 Legacy/SeaBIOS**，除非命中下列**硬性触发条件**之一；这些条件都能追到来源，其余场景属推理：
  1. 客户机是 Windows 11（要求 UEFI + Secure Boot 能力 + TPM 2.0）[L1-4]
  2. 需要 Secure Boot [L1-1 / L2-1]
  3. 需要 PCIe 直通 / GPU 直通 [L2-1 / L2-4]
  4. 客户机是 Arm [L1-3 / L2-1]
  5. 客户机需要 Hyper-V 第 2 代语义 [GEN12]
  6. 客户机系统自身声明只支持 UEFI 启动 [L1-4 / L2-1]
- **创建时就定死，别装完再改**：官方明文装后改固件可能导致启动失败 [L1-1]，且 MBR/GPT 不匹配是切换后无法启动的官方根因 [L3-1]。
- **PVE 侧的成套动作**：UEFI ⟹ 必须加 `efidisk0`；`efitype` 用 `4m`；要 Secure Boot 可加 `pre-enrolled-keys=1`（会默认启用 Secure Boot，仍可在 VM 内关闭）[L2-1]。
- **直通场景的成套动作**：机型 q35 + OVMF + PCIe；GPU 必须有 UEFI-capable ROM，否则退回 SeaBIOS [L2-4]。
- **VirtualBox 侧**：EFI 曾是实验性支持且有一串已知限制；用新版并避开「非 VBoxVGA 图形控制器 + 无引导介质」的组合 [L1-2 / L1-3 / L3-5]。
- **迁移路径**：先在客户机系统内 `mbr2gpt`（须厂商支持、不能转非系统盘）再改固件为 UEFI；或保留磁盘、新建一台 UEFI 虚拟机把盘挂过去 [L3-1 / MBR2GPT]。

## 7. Open Questions / 未闭合缺口

1. **PVE `bios` 创建后能否修改**：官方无明文。[L2-2] 的 `bios` 项无任何不可变标注（而 `tpmstate` 有），[L2-1] 全文无 `qm set --bios` 示例 —— 既无支持证据也无反驳证据，社区「只能创建时设定」的说法**未证实**，不得写成结论。
2. **i440fx + OVMF 是否受官方支持**：三份官方来源（L2-1/L2-2/L2-4）均未表态；社区侧把它当独立可选项用 [L2-5]。
3. **PVE 缺 `efidisk0` 的官方失败描述**：官方参考手册未描述该失败与修复，仅有 wiki 的回退/EFI Shell 链路 [L2-1 / L2-3]。
4. **VirtualBox 7.2 的 `modifynvram` 与 Secure Boot 密钥管理**：本组 4 个来源均未出现相关内容，官方页面是否存在未确认。
5. **L3-4（华为页）不可取证**：反爬导致无正文，该来源的「NVRAM 引导项丢失后用 Boot From File 选 grub.efi 恢复」说法**不得引用**。
6. **VMware 官方无「何时选 UEFI」的场景建议**：决策表里凡属场景推荐的表述必须标为推理 [L1-1]。
7. **Hyper-V 官方排错页未取**：本轮只取到代次规划页与安全设置页，第 2 代启动失败的官方排错文档未纳入。
8. **用户实际报错待补**：原诉求中的「使用 UEFI 时总是出问题」尚无具体报错原文；收到后并入 §4 排错表。

## 8. Downstream Handoff

- **派发纪律**：给 chapter-writer / outline-generator 只传 `来源ID + 缓存路径 + 小节名`，**不要转述本文件的论断**；本章笔记凡引「官方口径」，落笔前回 `.cache/p2_sources/` 对应文件核对原文。
- **可引用来源**：§2 表中 16 个（L3-4 除外，已剔除）。
- **层级标注要求**：L2-3 属官方 wiki、L2-5 与 L3-5 属 community —— 引用时须标层级，不得与参考手册等同。
- **推理标注要求**：§6 第 1 条中未列出触发条件的场景判断、[L1-1] 的场景建议缺失部分，均须标为推理。
- **别丢的细节**：PVE 官方那条 `"only if you plan to use PCIe passthrough"` 是最能回答「何时该换 UEFI」的官方原文；VMware 的 `"might cause the virtual machine boot process to fail"` 是「创建时就要定」的官方依据。
