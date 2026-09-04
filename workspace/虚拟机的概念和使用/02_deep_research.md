# 虚拟机的概念和使用 - 深度素材（P2）

> 运行：[[workspace/workflow-runs/虚拟机的概念和使用.workflow.md]]
> 主题：虚拟机的概念和使用 ｜ 目标读者：零基础 ｜ 深度：入门 ｜ 日期：2026-09-04
> P2 覆盖：全三方向（概念 + 桌面虚拟化实操 + 选型避坑）

## 一、Scope

面向零基础读者、入门深度的「概念 + 桌面虚拟化使用」笔记素材。三方向：
1. 基础概念：VM 定义、Hypervisor Type1/2、宿主/客户机、虚拟硬件/磁盘、快照、VM vs 容器 vs WSL2。
2. 桌面实操：VirtualBox 与 VMware Workstation 建机、装系统、快照、网络。
3. 选型与坑：何时用 VM、Windows 平台怎么选、磁盘格式、磁盘膨胀与常见坑。

## 二、Source Table

抓取物存于 `workspace/虚拟机的概念和使用/sources/`。文件按抓取序号命名，映射如下：

| 文件 | 来源 | 级别 | 提供内容 | 可用性备注 |
|---|---|---|---|---|
| 01_docs_oracle_com.md | Oracle VirtualBox 7.2 User Guide — Create a VM | 官方 | 建机向导全步骤 + VBoxManage CLI | 完整可用 |
| 02_docs_oracle_com.md | Oracle VirtualBox 7.2 — Working with VMs | 官方 | 启动/键盘鼠标/关闭方式/快照机制/网络默认 | ~110k 字含导航噪音，已抽样核心节 |
| 03_docs_oracle_com.md | Oracle VirtualBox 6.0 — Some Terminology | 官方 | Host/Guest/VM/Guest Additions 术语 | 正文很短，仅 4 术语；快照/磁盘只出现在导航 |
| 04_docs_oracle_com.md | Oracle VirtualBox 6.0 — Networking Modes | 官方 | NAT/Bridged/Internal/Host-only/NAT Network | 关键对照表 Table 6.1 抓取为空；端口转发仅有链接 |
| 05_cloud_google_com.md | Google Cloud — What is a VM | 官方 | VM 定义/架构/类型/用途/VM vs 容器 | 完整可用；进程 VM 例证不够严谨 |
| 06_knowledge_broadcom_com.md | VMware KB — 整理与收缩虚拟磁盘 | 官方 KB | 稀疏/预分配盘、收缩三步、中断风险 | 权威；命令需本机实测 |
| 07_learn_microsoft_com.md | Microsoft Learn — WSL 1 vs WSL 2 | 官方 | WSL2=托管 VM、与 VBox/VMware 共存、文件 IO | 完整可用，填补 VM vs WSL 缺口 |
| 08_www_cnblogs_com.md | 博客园 sunlong88 — 四款方案对比 | 社区 | Hyper-V/VMware/WSL2/VirtualBox 选型 | 个人经验，观点性强，标注为社区经验 |
| 09_techdocs_broadcom_com.md | VMware Workstation 简体中文手册 — 装 Win11 | 官方(中文) | 向导建机、vTPM/加密、Win11 注意点 | 完整可用 |
| 10_www_makeuseof_com.md | MakeUseOf — 虚拟磁盘格式 | 权威教程 | VDI/VHD/VHDX/VMDK、转换 | 有自相矛盾处，需交叉核对 |
| 11_www_techtarget_com.md | TechTarget — Type 1 vs Type 2 | 权威教程 | Type1/2 架构、产品归类、VT-x | 一处说法与常理冲突，见矛盾节 |
| 12_baeldung_cn.md | Baeldung 中文 — Docker/容器 vs VM | 权威教程 | 容器/VM 对比、快照回滚语义 | 完整可用 |
| 13_learn_microsoft_com.md | Microsoft Learn — 容器与虚拟机 | 官方(中文) | 隔离/资源/更新/容错逐项对比 | 完整可用 |
| 14_learn_microsoft_com.md | Microsoft Learn — 虚拟化基础模块 | 官方(培训) | 仅学习目标列表 | **stub**，无正文，仅作覆盖面印证 |

**tier 混合**：官方 9 / 权威教程 3 / 社区 1 / stub 1。主体论断均有官方或权威来源支撑；社区与自相矛盾处已显式标注。

## 三、Claim / Source Map（按方向）

### 方向 1：基础概念

| 论断 | 来源 |
|---|---|
| VM = 基于软件的计算机，在宿主硬件上提供隔离环境，可跑 OS/程序/存数据/联网 | 05, 11, 12 |
| Host = 跑 hypervisor/虚拟化软件的物理机；Guest = 跑在 VM 里的系统；VirtualBox 是装在 Host OS 上的 Type 2 hypervisor | 03, 05, 11 |
| Hypervisor（原名虚拟机监视器 VMM）把宿主 CPU/内存/存储/网络划成资源池分配给 guest | 05, 11 |
| Type 1（裸机）直接跑硬件上：VMware ESXi、Hyper-V、KVM、Xen；Type 2（托管）跑在既有 OS 上：VirtualBox、VMware Workstation、QEMU | 11（产品归类与 03 定位一致）|
| VM 本质是"一组参数 + 状态"：硬件设置（内存/CPU/网卡/虚拟磁盘）+ 运行状态 | 03, 05 |
| 虚拟硬盘是宿主上的镜像文件，动态增长或固定大小；VDI/VMDK/VHD 等是具体格式 | 05, 10 |
| 快照 = 记录 VM 设置的 XML + 虚拟磁盘差异镜像（differencing image），运行中拍还含内存状态；用于改动前留安全网、可整体回滚 | 02, 12 |
| VM vs 容器：VM 虚拟化整个硬件栈并自带完整 OS（更重、隔离强、可跑异构 OS）；容器共享宿主内核、只打包应用+运行时（更轻、启动快）；二者常互补（容器跑在 VM 上） | 05, 12, 13 |
| WSL1 非 VM（系统调用转换层）；WSL2 是微软后台托管的"轻量实用 VM"，跑真正 Linux 内核，免运维；与旧版 VBox 不兼容 | 07 |
| 硬件虚拟化扩展 Intel VT-x / AMD-V 是加速基础，服务器标配、桌面可能要 BIOS 开启 | 11, 12 |

### 方向 2：桌面虚拟化实操

| 论断 | 来源 |
|---|---|
| VirtualBox 建机：Home→New；VM 名=显示名+文件名；选 VM Folder（要快照留足空间）；自备 OS ISO（VBox 不提供系统/许可） | 01 |
| 默认无人值守安装（Windows 建管理员/Linux 建 root、可选装 Guest Additions）；手动装取消勾选即可 | 01 |
| 内存按建议、不超宿主余量（宿主同时不可用该内存）；处理器≤宿主线程一半；磁盘默认动态分配 | 01 |
| 首次启动：无人值守自动装；否则跟随屏幕；键盘/鼠标被抢占用 Host key（默认右 Ctrl）交还；Ctrl+Alt+Del = Host key+Del | 02 |
| Guest Additions 提升体验：消除第二鼠标指针、窗口自适应、共享文件夹 | 02, 03 |
| 关闭方式：Save State（整机冻结续跑）/ Shut Down（ACPI 正常关机）/ Power Off（=拔电源，勿用；有快照时可用来回滚当前状态） | 02 |
| 快照：Machine→Take Snapshot；恢复=整机（含磁盘）回滚、其后改动丢失；删除只释放磁盘、可能慢/需关机 | 02 |
| 网络默认 NAT（上网够用）；Bridged 供 guest 跑服务给外部/局域网；Host-only 仅宿主+VM；Internal 仅 VM 间 | 02, 04 |
| VMware Workstation 装 Win11：向导 Typical→选 ISO→选 Windows 11 x64→命名/目录→**自动加 vTPM 并要求加密**（可只加密最小文件）→设磁盘→Customize Hardware→创建 | 09 |
| VMware Win11 要点：装后勿移除加密/vTPM；远程 VM 不支持 Win11 guest | 09 |
| VBox 7.2 建机向导无 vTPM/TPM 步骤（仅 Use EFI 选项）——VBox 装 Win11 的 TPM 路径本批缺源 | 01（缺口） |

### 方向 3：选型与避坑

| 论断 | 来源 |
|---|---|
| 何时用 VM：需要强隔离安全边界、跑异构 OS、完整内核兼容；容器更轻但隔离弱、需同 OS 版本；更新上 VM 重、容器重建镜像即可 | 13 |
| 桌面四方案选型（社区经验，需实测）：WSL2 轻量/一键/开发；Hyper-V Type1/多节点；VMware 图形化最全/付费/教程多；VirtualBox 开源免费/入门 | 08 |
| VirtualBox=开源 Type2、VMware Workstation=商业 Type2、Hyper-V=Windows 内置 Type1、WSL2=轻量子系统 | 08, 11 |
| 虚拟磁盘格式：VDI(VBox 开源)、VMDK(VMware，2011 起开放)、VHD/VHDX(微软，VHDX 支持更大/更稳)；长期用建议宿主原生格式 | 10 |
| 磁盘膨胀机理：稀疏盘"只增不减"，删文件后镜像不自动缩小；VM 目录大还可能因快照/挂起状态文件/日志 | 06 |
| 收缩三步：guest 内碎片整理 → VMware Tools 收缩（9.x+ 用 VM > Manage > Clean up Disks）→ 宿主清理；仅稀疏盘可用；**有快照必须先删**；中断可致磁盘不可修复 | 06 |

## 四、矛盾与存疑（写作时注意）

1. **TechTarget「Type 2 VM 比 Type 1 更小更快、占用资源少、单机可承载更多」**：与「guest 开销由 guest OS 决定、hypervisor 类型只影响 hypervisor 层」的常理及 Google/Baeldung 框架冲突，疑似混淆桌面 VM 与容器。**建议不采用**，改用「Type 2 经宿主 OS 转发、有额外延迟、宿主 OS 是共同威胁点」表述。
2. **容器引擎是否算 hypervisor**：TechTarget 称容器引擎是"专门化 Type 2 hypervisor"；Google/Baeldung/Microsoft 均称容器共享宿主内核、无 hypervisor。**建议采用后一口径**（容器无 hypervisor）。
3. **MakeUseOf 磁盘格式文自相矛盾**：VDI「性能优于 VHD/VHDX」与「慢于 VMDK/VHDX」冲突；VMDK「不兼容 Hyper-V」与正文「可被 Hyper-V 运行」冲突。磁盘格式性能结论**只写归属与生态**，不写绝对性能排序。
4. **Google「进程 VM」举例（Cloud Run 容器）**：例证不严谨，概念笔记中进程 VM/系统 VM 二分可简化或省略。
5. **WSL2 与 VirtualBox/Hyper-V 共存**：07 中「VBox 6+ 不兼容」为较旧结论；当前 VirtualBox 7.x 与 WSL2/Hyper-V 并存需注明"以当前版本实测为准"。
6. **cnblogs 四方案性能排序**无基准，只作社区经验、建议标注"以实测为准"。

## 五、实践指引（给下游写作的浓缩步骤）

- **VirtualBox 入门线**：前提(装 VBox + 备 ISO + 留足磁盘/内存) → New 向导(命名/选 Folder/选 ISO/无人值守或手动) → 硬件(内存按建议、CPU≤一半、磁盘默认动态) → Start(被抢占按右 Ctrl 还宿主) → 装 Guest Additions → 打快照(Machine→Take Snapshot) → 关机优先 Save State/Shut Down → 改网络(关机后 Settings→Network)。
- **VMware 入门线**：新建向导 → Typical → ISO → Windows 11 x64 → 命名/目录 → 加密+自动 vTPM(选最小加密即可) → 磁盘 → Customize Hardware(可选) → 创建并装系统；装后勿删 vTPM/加密。
- **磁盘瘦身（VMware 官方）**：仅稀疏盘 → 先删快照 → guest 内碎片整理 → Tools 收缩/ Clean up Disks → 宿主清理；全程勿关机/取消。
- **给零基础的网络速记**：上网用 NAT；给局域网/外部提供服务改 Bridged；只要宿主↔VM 通选 Host-only；仅 VM 互通选 Internal。

## 六、开放问题（写作/补源时处理）

1. **VirtualBox 装 Win11 的 TPM/UEFI 路径**无来源 → 需补 VBox 官方 Win11 要求说明或换演示 OS（如装 Linux 或 Windows 10），避免给错步骤。
2. **NAT 端口转发实操步骤**缺失（04 仅链接到 6.3.1）→ 若笔记要写「让宿主访问 guest 内服务」需补 7.2 官方网络页或 VBox 实测。
3. **VT-x/AMD-V 与 Hyper-V/VBS 冲突**的权威说明缺失 → 写"BIOS 开虚拟化 + Windows 功能冲突"章节时以官方通用说明 + 标注实测。
4. **快照差异镜像链导致膨胀的机制**只被隐式提及 → 概念层补 1-2 句原理（快照基于 differencing image、只记差异）即可，深度无需到 delta 链实现。
5. **VirtualBox 侧 VDI 压缩命令**（VBoxManage modifyhd --compact）无官方 KB → 引用需实测或标注经验。
6. **VMware 许可现状**（2023 Broadcom 收购后）与 MakeUseOf 2023-11 数据可能过时 → 涉及定价/授权处写"以官网为准"。
7. 14 号文件（MS Learn 虚拟化模块）是 stub，未采用其正文；仅印证概念覆盖与官方课程结构。

## 七、Downstream Handoff（给 outline-generator / chapter-writer）

- **建议章节骨架**（≤3 级，供大纲参考，最终以大纲确认为准）：
  1. 虚拟机是什么 / 为什么需要（host/guest、hypervisor、Type1/2 一句话 + 实例、典型用途）
  2. 虚拟机 vs 容器 vs WSL2（零基础比喻：整套 OS vs 共享内核）
  3. 核心概念速览：虚拟硬件、虚拟磁盘、镜像、快照（每个给"是什么/为什么用/一个坑"）
  4. 实操 · VirtualBox：建机 → 装系统 → Guest Additions → 快照 → 网络（默认 NAT），配避坑
  5. 实操 · VMware Workstation（可选或对比节）：建机 → 装 Win11（vTPM/加密注意）
  6. 选型与常见坑：何时用 VM / 桌面四方案怎么选 / 磁盘膨胀与收缩 / VT-x 与 Hyper-V 冲突
- **事实红线**：Type2 性能表述按本文矛盾节处理；容器无 hypervisor；磁盘格式只写归属生态；社区结论标"经验，以实测为准"。
- **素材引用**：官方页面锚点见 sources/ 下对应文件；引用时优先官方 9 篇，社区仅作转述辅助。
