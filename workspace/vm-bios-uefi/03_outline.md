## 学习笔记大纲：《虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI)》

> 笔记类型：对比笔记 + 实战笔记（混合）
> 预计总篇幅：长（6 章，约 18–25 页）
> 章节数：6

> **为什么混合**：用户的两个真实痛点分别是「不知道用哪个」（属选型对比）与「选 UEFI 总出问题」（属落地排错），任何单一类型都装不下。
> **采用的骨架**：对比笔记的「分别介绍 → 逐项对比 → 选型建议」压缩进第 1、2 章（概念对齐 + 决策表）；实战笔记的「环境搭建 → 核心功能 → 进阶优化 → 排错」落到第 3–6 章（三平台各一章 + 排错专章）。
> **依赖顺序**：概念与启动链路 → 选型决策 → 三平台实操 → 排错。第 3/4/5 章之间无依赖，可按需跳读。

---

### 第一章：固件做什么、BIOS 与 UEFI 差在哪

- **篇幅**：中
- **覆盖要点**：固件在虚拟机中的角色（启动早期执行、做基本硬件初始化、提供接口）[L2-1]；VMware 官方口径「客户机固件类型只有 UEFI 与 Legacy BIOS 两项，无第三项」[L1-1]；固件与分区表的绑定关系（BIOS 用 MBR、EFI 需 GPT，切固件后无法启动被官方定性为预期行为）[L3-1]；UEFI 启动链路（固件需知道从 ESP 启动哪个 bootloader → EFIVARS 无 boot entry 时回退加载 `$ESP/EFI/BOOT/BOOTX64.efi` → 回退还失败则进入 EFI Shell）[L2-3]；Secure Boot 机制（只放行 UEFI 数据库中受信签名的引导加载程序与 UEFI 驱动 / option ROM）[L1-1 / GEN12 / GEN2SEC]；**Hyper-V 简短对照**（本节，不独立成章：第 1 代 = Legacy BIOS，第 2 代 = UEFI firmware + Secure Boot，代次固件独立于宿主上装了什么）[GEN12]；术语提醒（属素材归纳，标为推理：“MBR”一词在两来源中含义不同——前者指纯 MBR 分区方案，后者的 GPT 磁盘带 `MBR: protective` 兼容外壳，不可混读）[L3-1 / L3-3]；**缺口标注**：CSM 在本轮 16 个来源中零命中，本章不写 CSM 结论
- **素材引用**：L2-1, L1-1, L3-1, L2-3, L3-3, GEN12, GEN2SEC
- **代码示例**：无

### 第二章：什么时候必须用 UEFI —— 选型决策

- **篇幅**：中
- **覆盖要点**：两平台的默认值（PVE 默认 SeaBIOS 且官方称适合大多数标准场景 [L2-1]；VirtualBox 默认使用 BIOS 固件 [L1-3]）；本轮最有价值的一条官方判据——PVE「多数情况下，只有计划使用 PCIe 直通时才需要从 SeaBIOS 换到 OVMF」[L2-1]；**六条硬性触发条件**（逐条可回源）：① Windows 11 客户机 [L1-4] ② 需要 Secure Boot [L1-1 / L2-1] ③ 需要 PCIe / GPU 直通 [L2-1 / L2-4] ④ 客户机是 Arm [L1-3 / L2-1] ⑤ 需要 Hyper-V 第 2 代语义 [GEN12] ⑥ 客户机系统自身声明只支持 UEFI 启动 [L1-4 / L2-1]；决策表（场景 → 选谁 → 依据 → 来源层级）；「创建时就定死，别装完再改」（官方明文装后改固件可能导致启动过程失败 [L1-1]，MBR/GPT 不匹配是切换后无法启动的官方根因 [L3-1]）；口径并列（社区主张新 VM 一律 OVMF、SeaBIOS 只留给 legacy 系统 [L2-5, community 层级]，与 PVE 官方默认口径取向不同而非直接互斥）；**推理标注**：VMware 官方只给前置条件与警告、未给任何场景建议 [L1-1]，凡超出上述六条的推荐表述均标为推理；**大容量引导盘这一条要如实分层**（跨平台口径与 Hyper-V 硬数据分开写）：跨平台的「>2TB 系统盘需 UEFI」本轮素材无官方结论，不得写成通用官方口径；但 Hyper-V 侧有可直接引用的官方硬数据——第 2 代（UEFI）最大引导卷 **64 TB**，第 1 代（Legacy BIOS）为 **2 TB**（`.VHDX`）/ 2040 GB（`.VHD`），原文在「使用第 2 代虚拟机的优势」下以 **Larger boot volume** 列出 [GEN12]，引用时须注明这是 Hyper-V 引导卷上限，不是通用结论
- **素材引用**：L2-1, L2-4, L2-5, L1-1, L1-3, L1-4, L3-1, GEN12
- **代码示例**：无

### 第三章：VMware Workstation 实操

- **篇幅**：中
- **覆盖要点**：设置入口与选项（Settings → Options → Advanced → **Firmware type**，只有 Legacy BIOS 与 UEFI 两项）[L1-1]；选 UEFI 的四项前置（客户机系统支持 UEFI、未启用 VBS、硬件版本 ≥ 8、客户机为 Windows 8/10/2012/2016）[L1-1]；选 Secure Boot 的额外前置（固件类型已是 UEFI 且硬件版本 ≥ 14）[L1-1]；启用 VBS 时固件类型被固定为 UEFI 并勾选 Secure Boot，且两项均不可编辑 [L1-1]；后果反例（装完系统再改固件类型可能使虚拟机启动过程失败）[L1-1]；**附：Windows 11 在 ESXi 上的落地清单**（固件设 EFI、必须启用 Secure Boot、需 vTPM 而 vTPM 需虚拟机加密、加密需 KMS、硬件版本 ≥ 14、最低 64 GB 虚拟磁盘）——须显式注明适用环境是 ESXi 7.x/8.x，不是 Workstation [L1-5]；迁移参考（改固件前须先转 GPT，且需客户机系统厂商支持）[L3-1]
- **素材引用**：L1-1, L1-5, L3-1
- **代码示例**：无（该平台素材只含 GUI 入口、选项条件与官方警告，无可写进笔记的命令）

### 第四章：VirtualBox 实操

- **篇幅**：中
- **覆盖要点**：默认固件是 BIOS；启用 EFI 的路径（GUI 勾选或 `VBoxManage modifyvm --firmware efi`，回退 `--firmware bios`）[L1-2]；**定位随版本变化，引用须带版本**（6.0 手册标注 EFI 支持为 experimental [L1-2]；主干同节标题已改为 Alternative Firmware (UEFI)、全节不再出现 experimental，并新增「多数现代 macOS 与 Windows 需要 UEFI」「所有 Arm VM 需要 UEFI」[L1-3]）；6.0 手册记载的限制清单（Windows 7 客户机无法在 EFI 下启动；运行中的客户机内无法操作 EFI 变量，替代做法是用 `setextradata` 写 `VBoxInternal2/EfiBootArgs`；EFI 默认分辨率 1024x768 且仅关机状态下可改；EFI 提供 GOP 与 UGA 两种视频接口）[L1-2]；已知具体失败行为（2019 年 ticket #18282：图形控制器不是 VBoxVGA 且未提供可引导介质时 EFI Shell 始终不出现、安装无法进行，且 `EfiGopMode`、`EfiGraphicsResolution` 等 ExtraData 全部被忽略；根因是当时 EFI 固件里没有处理 VMSVGA/VBoxSVGA 的图形驱动；报告者以 r128870（6.0.5）确认修复）[L3-5, community 层级]；规避建议（标为推理：升级到 6.0.5 及以上，避开「非 VBoxVGA 图形控制器 + 无引导介质」组合）；**缺口标注**：VirtualBox 7.2 的 `modifynvram` 与 Secure Boot 密钥管理本轮零覆盖，本章不写
- **素材引用**：L1-2, L1-3, L3-5
- **代码示例**：有（`VBoxManage modifyvm --firmware efi|bios`；`setextradata ... VBoxInternal2/EfiBootArgs`）

### 第五章：PVE 实操（SeaBIOS vs OVMF）

- **篇幅**：长
- **覆盖要点**：默认与切换判据（默认 SeaBIOS [L2-1]；官方判据是 PCIe 直通 [L2-1]；客户机系统的硬性要求会压过默认，如 Windows 11 时「you must use OVMF instead」[L2-1]；arm64 主机上 `bios=ovmf` 是唯一受支持设置，因 SeaBIOS 仅支持 x86 [L2-1]）；**EFI Disk**（用 OVMF 时必须有 EFI Disk 保存 boot order 等信息，会纳入备份与快照，且只能有一个）[L2-1]；创建命令 `qm set <vmid> -efidisk0 <storage>:1,format=<format>,efitype=4m,pre-enrolled-keys=1` [L2-1]；efitype 应始终用 4m（GUI 默认即 4m，2m 仅为向后兼容；已有 2m 想启用 Secure Boot 必须删除重建，且会重置 OVMF 菜单里的自定义配置）[L2-1 / L2-2]；pre-enrolled-keys 会默认启用 Secure Boot，仍可在 VM 内 OVMF 菜单关闭 [L2-1]；选项语义（`bios: <ovmf|seabios>` 默认 seabios，手册对这一项的全部说明只有一句「Select BIOS implementation.」[L2-2]；`efidisk0` 六个子项 file/efitype/format/ms-cert/pre-enrolled-keys/size，其中 `size` 纯属信息性、没有实际作用 [L2-2]）；机型与固件的耦合（Intel vIOMMU 需机型为 q35 [L2-2]；PCIe 直通仅在 q35 可用，PCI 直通在 i440fx 与 q35 都可用 [L2-4]；GPU 直通最佳兼容组合是 q35 + OVMF + PCIe，GPU 必须有 UEFI-capable ROM，否则应改用 SeaBIOS [L2-4]）；进 OVMF 菜单与添加引导项（splash 出现时恰好按一次 ESC，当前版本还需选 "EFI Firmware Setup" 条目；Boot Maintenance Manager → Boot Options → Add Boot Option，再选带 ESP 的磁盘）[L2-3, 官方 wiki 层级]；口径差异标注（社区把机型与固件列为两个独立选项 [L2-5, community]；社区称 TPM 2.0 的前提是 q35 + OVMF，官方未声明该前提，不得当作官方口径 [L2-5 / L2-1]）；**缺口标注**：`bios` 项创建后能否修改官方无明文（既无支持证据也无反驳证据）；i440fx + OVMF 是否受官方支持三份官方来源均未表态
- **素材引用**：L2-1, L2-2, L2-3, L2-4, L2-5
- **代码示例**：有（`qm set <vmid> -efidisk0 ...`）

### 第六章：UEFI 排错 —— 症状、根因、处置

- **篇幅**：长
- **覆盖要点**：开篇说明本章以**通用原理**覆盖（用户真实报错原文/截图尚未提供，收到后按真实报错重写对应行）[缺口]；① **切固件后无法启动**（根因：MBR/GPT 不匹配，官方定性为预期行为、切换不会转换分区表；处置：重建 VM 选定固件后挂原有硬盘，或切 EFI 前先把磁盘转 GPT）[L3-1]；② **停在 EFI Shell / 没有引导项**（根因：EFIVARS 中无 boot entry 且回退路径 `$ESP/EFI/BOOT/BOOTX64.efi` 也失败；处置：进 OVMF 菜单 Add Boot Option，手法见第五章）[L2-3]；③ **找不到 UEFI 引导加载程序**（启动诊断报 `The boot loader did not load an operating system`；根因：EFI 系统分区被删除或缺失；处置：用 `gdisk` 以类型码 `ef00` 在正确扇区重建 ESP）[L3-3]；④ **UEFI 启动分区损坏**（报 `The UEFI boot partition is corrupted`；根因：ESP 文件系统损坏；处置：`fsck.vfat` 清理修复）[L3-3]；⑤ **/boot 分区内容被删除且无法恢复**（官方原文明确「从备份恢复虚拟机是唯一选项」）[L3-3]；⑥ **Secure Boot 拦下引导程序/驱动**（官方表述：只放行 UEFI 数据库中受信签名的 bootloader 与 option ROM，未正确签名时须关闭 Secure Boot；须并注 VMware 侧 VBS 场景下该项不可编辑）[GEN12 / GEN2SEC / L1-1]；⑦ **VirtualBox 无引导介质时看不到 EFI Shell**（指向第四章）[L3-5]；⑧ **PVE UEFI 虚拟机启动异常 / 缺 efidisk0**（官方参考手册未描述该失败现象与修复，仅有 wiki 侧的回退与 EFI Shell 链路；**此格标为未闭合缺口，不得写成已解决的结论**）[L2-1 / L2-3]；**迁移路径两条**（客户机内先 `mbr2gpt` 再改固件为 UEFI——不能转非系统盘、MBR 最多三个主分区、转换后固件须重新配置为 UEFI 模式引导、Windows 7/8/8.1 离线转换不受官方支持，且该页不含虚拟机字样 [MBR2GPT]；或保留磁盘、新建一台 UEFI 虚拟机把盘挂过去 [L3-1]）；术语歧义专节（“MBR”一词的两种含义，见第一章）[L3-1 / L3-3]
- **素材引用**：L3-1, L3-3, L2-3, L2-1, L3-5, L1-1, GEN12, GEN2SEC, MBR2GPT
- **代码示例**：有（`gdisk` 类型码 `ef00`、`fsck.vfat`、`mbr2gpt.exe`）

---

## 学习路径说明

### 前置要求
- 已用 VMware Workstation / VirtualBox / PVE 中至少一个建过虚拟机，能进入虚拟机的固件或硬件设置界面
- 知道虚拟机磁盘有「分区表」这一层即可；MBR / GPT 的具体差别第一章会给，不必预学
- 遇到报错时能描述或截图现象（本期排错章按通用原理写，真实报错后续补入）

### 学完能做什么
- 拿到一个新虚拟机需求，能对照决策表在几分钟内定下固件类型，并说清依据来源（官方条件 / 社区取向 / 推理）
- 能在 VMware Workstation、VirtualBox、PVE 三处正确开启 UEFI，并补齐各自前置（VMware 硬件版本、VirtualBox 版本与图形控制器、PVE 的 efidisk0 与 efitype）
- 遇到「切 UEFI 后起不来 / 停在 EFI Shell / 找不到引导加载程序 / Secure Boot 拦截」时，能按症状表定位根因并选定处置路径，知道哪一步只能靠备份恢复

### 建议学习顺序
- 第一章 → 第二章：概念与决策，约 40 分钟；只读这两章已足够应付日常选型
- 第三章 / 第四章 / 第五章：按实际使用的平台读，三章之间无依赖；PVE 章最长，做直通或 Windows 11 客户机时必读
- 第六章：可随时回查；建议读完前五章后通读一遍，记住症状表结构（症状 → 根因 → 处置三列）
- 用户真实报错原文补齐后，回读第六章对应行并替换
