# 虚拟机固件选择 —— BIOS(Legacy/SeaBIOS) vs UEFI(OVMF/EFI) — 探测结果（P1）

> 运行：vm-bios-uefi（learning-note-flow P1）
> 日期：2026-09-18
> 方法：3 个并行透镜 subagent 探测，候选源按官方文档 > 高可信报告 > 社区实操排序；同 URL 已按规范去重。
> 抓取环境：`crawl.sh --help` 退出 0，crawl4ai 环境就绪，P2 可直接精读。

---

## 方向菜单

以下方向来自 3 个透镜，互补不冲突，可任选其一为主，或综合。

- **方向 A：选型决策优先** —— 回答「我到底该选哪个」：按客户机系统与用途给决策树 + 一页速查表
  - 关键线索：Windows 11 硬性要求 UEFI + Secure Boot + TPM 2.0（虚拟机需 Gen2/硬件版本 14+）；PVE 侧 x86 默认是 SeaBIOS，OVMF 的官方换用前提是 PCIe 直通；PCIe 直通仅在 q35 机型可用
- **方向 B：三平台实操优先** —— VMware Workstation / VirtualBox / PVE 各一节，讲清选项在哪、每个选项什么含义、创建后还能不能改
  - 关键线索：VMware 侧 UEFI 需硬件版本 8+、Secure Boot 需 14+，**装完系统后再改固件官方明确不支持**；VirtualBox 默认 BIOS、EFI 长期标记为实验性；PVE 的 `bios` 默认值 `seabios`，UEFI 必须配 `efidisk0`，其 `efitype` 为 `4m` 才支持 Secure Boot
- **方向 C：UEFI 排错优先** —— 症状 → 根因 → 修复，专治「选 UEFI 总是出问题」
  - 关键线索：BIOS↔EFI 来回切不转分区表，MBR/GPT 不匹配即启动失败（VMware 官方 KB 确认）；PVE 无引导项时回退 `BOOTX64.efi`，失败就落进 EFI Shell；缺/坏 ESP 分区有官方定位法与修复手段
- **方向 D：综合（推荐）** —— A+B+C 合并为「先决策 → 再实操 → 出错照排错」，正好对应你的原始诉求「不知道用哪个 + 选 UEFI 老出问题」

---

## 候选源记录（按透镜分组）

### 透镜 L1：桌面虚拟化固件选型（VMware / VirtualBox / Windows 11 硬性要求）

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| L1-1 | [Configure a Firmware Type（VMware Workstation Pro 用户指南）](https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/workstation-pro/25H2/using-vmware-workstation-pro/using-virtual-machines-in-workstation-pro-user-guide/starting-virtual-machines/configure-a-firmware-type.html) | 官方文档 | UEFI 需硬件版本 8+、Secure Boot 需 14+；装完系统后改固件可能无法引导 | 未知 | 5 |
| L1-2 | [Alternative Firmware (EFI) — VirtualBox 用户手册 6.0](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/efi.html) | 官方文档 | 官方标注 EFI 为实验性；默认仍走 BIOS；Win7 客户机无法引导 | 未知 | 4 |
| L1-3 | [Alternative Firmware (UEFI) — VirtualBox 手册主干源文件 efi.dita](https://raw.githubusercontent.com/VirtualBox/virtualbox/refs/heads/main/doc/manual/en_US/dita/topics/efi.dita) | 官方文档 | 现行手册同章节措辞已去掉「实验性」；Arm 客户机强制 UEFI，可对照支持态度演变 | 未知 | 3 |
| L1-4 | [Windows 11 requirements — Microsoft Learn](https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements) | 官方文档 | 硬性要求 UEFI + Secure Boot capable + TPM 2.0；虚拟机需 Gen2 且启用安全启动与 vTPM | 2026-07-14 | 5 |
| L1-5 | [Windows 11 Installation Fails on ESXi 7.0U3（Broadcom KB 408976）](https://knowledge.broadcom.com/external/article/408976/windows-11-installation-fails-on-esxi-70.html) | 官方文档 | 把「固件设 EFI + 启 Secure Boot + vTPM」串成可操作清单，落地时可直接照抄顺序 | 未知 | 4 |

**透镜 L1 缺口**：VMware 官方没有「什么场景推荐哪一种」的成文对照表，只有前置条件与警告，该维度需靠社区或实践经验补齐；VirtualBox 7.x 在线手册 EFI 章节（`docs.oracle.com/.../7.1/user/efi.html`）抓取返回 404，未能核对现行版本措辞与 7.2 新增的 `modifynvram` / Secure Boot 密钥管理页。

### 透镜 L2：PVE 固件与机型组合

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| L2-1 | [Proxmox VE Administration Guide — Qemu/KVM Virtual Machines（含 BIOS and UEFI、Machine Type 节）](https://pve.proxmox.com/pve-docs/chapter-qm.html) | 官方文档 | 官方定义 SeaBIOS 为 x86 默认、OVMF 适用场景、q35 与 i440fx 差异，是本透镜主干 | 未知（随版本滚动） | 5 |
| L2-2 | [qm.conf(5) 手册页 — `bios` 与 `efidisk0`](https://pve.proxmox.com/pve-docs/qm.conf.5.html) | 官方文档 | `bios` 默认 `seabios`；`efidisk0` 各子键与默认值；`efitype` 为 `4m` 才支持 Secure Boot | 未知（随版本滚动） | 5 |
| L2-3 | [Proxmox VE Wiki — OVMF/UEFI Boot Entries](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries) | 官方文档 | 无引导项时回退 `BOOTX64.efi`，失败即进入 EFI Shell；含手工添加引导项步骤 | 2026-03-20 | 4 |
| L2-4 | [pve-docs 源文件 qm-pci-passthrough.adoc — PCI(e) Passthrough](https://raw.githubusercontent.com/proxmox/pve-docs/master/qm-pci-passthrough.adoc) | 官方文档 | 明文给出 q35 + OVMF + PCIe 为直通最佳组合；GPU 需 UEFI ROM，否则退回 SeaBIOS | 未知 | 4 |
| L2-5 | [Best Practice Configurations for Virtual Machines on Proxmox VE（Starline）](https://www.starline.de/en/magazine/technical-articles/best-practice-configurations-for-virtual-machines-on-proxmox-ve) | 社区实操 | 按客户机系统选固件与机型的对照表；新机优先 OVMF+q35，TPM 2.0 需 UEFI | 2026-06-26 | 3 |

**透镜 L2 缺口**：官方未见「i440fx + OVMF 组合是否受支持」的明文表述；机型与 TPM 的前置关系仅见于社区来源；社区有「`bios` 只能在创建时设定」的说法，与 PVE 支持 `qm set --bios` 的用法冲突，**须在 P2 回官方文档核实后落笔**。

### 透镜 L3：选 UEFI 后的故障现象与排错

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| L3-1 | [Virtual Machine fails to boot when changing the Firmware from BIOS to EFI（Broadcom KB 384912）](https://knowledge.broadcom.com/external/article/384912/) | 官方文档 | 官方确认 BIOS↔EFI 切换不受支持；MBR/GPT 分区表不匹配即启动失败，需重建 VM 或 `mbr2gpt` | 未知 | 5 |
| L3-2 | [OVMF/UEFI Boot Entries — Proxmox VE](https://pve.proxmox.com/wiki/OVMF/UEFI_Boot_Entries) | 官方文档 | 与 L2-3 同 URL（**已去重**，仅在 L2 计入一次）：EFI Shell 现象的成因与 `Add Boot Option` 恢复步骤 | 2026-03-20 | 5 |
| L3-3 | [Troubleshoot UEFI boot failures with Azure Linux images — Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/azure/virtual-machines/linux/azure-linux-vm-uefi-boot-failures) | 官方文档 | 按 ESP 缺失 / ESP 损坏 / boot 分区被删三种场景给定位法；`gdisk` 重建 ESP、`fsck.vfat` 修复 | 2026-07-21 | 4 |
| L3-4 | [Linux 系统启动引导固件类型设置为 UEFI 时系统无法正常启动（华为企业支持）](https://support.huawei.com/enterprise/zh/knowledge/EKB1100154009?idAbsPath=7919749%7C251364444%7C251364849%7C254217435%7C8576912) | 官方文档 | 中文官方案例：NVRAM 引导项丢失后经 `Boot From File` 选 `grub.efi` 恢复 | 未知 | 4 |
| L3-5 | [EFI shell not shown when VMSVGA or VBoxSVGA is chosen（VirtualBox ticket #18282）](https://www.virtualbox.org/ticket/18282) | 社区实操 | 解释无引导介质时为何不出现 EFI Shell；6.0.5 之后修复 | 2019 | 3 |

**透镜 L3 缺口**：未找到「PVE 缺 `efidisk0` 导致启动失败」的官方文档页，只有邮件列表与第三方教程；OVMF 回退行为的官方正文有限；VirtualBox 官方手册 EFI 章节与 Hyper-V 第 2 代虚拟机排错页本轮未验证到可用 URL；Secure Boot 拦截缺直接可引用的官方条目（目前靠 VMware 案例间接覆盖）。

---

## Coverage Gaps（综合）

1. **缺「选哪个」的单一权威决策表** —— VMware 侧尤其明显，官方只给前置条件不给推荐场景 → P2 需多源拼合，凡拼合出的结论必须显式标注为「推理」而非官方口径。
2. **Hyper-V 第 2 代虚拟机**（UEFI + 无 Legacy）本轮未取到可用官方 URL，而意图文件把 Hyper-V 纳入简短对照 → P2 补源。
3. **PVE 的 `efidisk0` 缺失、SeaBIOS↔OVMF 切换**缺官方排错正文 → P2 补邮件列表/第三方教程，并标注来源层级。
4. **VirtualBox 7.x 现行 EFI 章节**需换检索路径复取（含 7.2 的 `modifynvram` 与 Secure Boot 密钥管理）。
5. **待你补料**：你实际遇到的 UEFI 报错原文/截图（VMware / VirtualBox / PVE 均可）。意图文件已登记该待补项；收到后并入排错章按真实报错写。

**源统计**：去重后 14 个候选源 —— 官方文档 12、社区实操 2；官方文档占比 86%。

## P2 范围估算

- 核心深读 3–5 源（建议）：**L1-1、L1-4、L2-1、L2-2、L3-1** —— 覆盖 VMware 前置条件、Win11 硬性要求、PVE 官方定性、配置项事实、切换失败机理。
- 补源仅针对上面 5 条显式缺口，不扩散；每个补源保持一次委托处理一组来源，不按源逐一派发。
- 产出 `02_deep_research.md`：scope、source table、claim/source map、contradictions、practical guidance、open questions。
