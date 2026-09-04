# 虚拟机的概念和使用 - 探测结果（P1）

> 运行：[[workspace/workflow-runs/虚拟机的概念和使用.workflow.md]]
> 主题：虚拟机的概念和使用 ｜ 目标读者：零基础 ｜ 深度：入门 ｜ 日期：2026-09-04

三个并行探测 agent 分别覆盖：**① 基础概念 ② 桌面虚拟化实操 ③ 选型场景与常见坑**。已按规范 URL 去重，无跨方向重复。

## 一、候选信源（按方向）

### 方向 1：虚拟机基础概念
| 标题 | URL | 来源级别 | 日期 | 相关性 | 评分 |
|---|---|---|---|---|---|
| Oracle VirtualBox 手册 — Some Terminology（术语定义） | https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/virtintro.html | 官方文档 | unknown | 以朴素语言定义 Host/Guest/VM/虚拟硬件/快照，零基础名词底本 | 5 |
| Google Cloud — 什么是虚拟机 (VM) | https://cloud.google.com/learn/what-is-a-virtual-machine | 官方文档 | unknown | 总述「用软件把一台物理机虚拟成多台计算机」+ 宿主/客户机 + 虚拟磁盘 | 4 |
| Microsoft Learn — 虚拟化基础模块（含中文） | https://learn.microsoft.com/zh-cn/training/modules/cmu-virtualization/ | 官方文档 | unknown | 系统讲虚拟化原理、hypervisor、宿主/客户机、完全/半虚拟化 | 4 |
| TechTarget — Type 1 vs Type 2 hypervisor | https://www.techtarget.com/it-infrastructure/tip/Whats-the-difference-between-Type-1-vs-Type-2-hypervisor | 权威教程 | unknown | 用架构链图示清晰区分 Type1/Type2，含性能/适用场景 | 4 |
| Baeldung 中文 — Docker 和容器 vs 虚拟机 | https://baeldung.cn/cs/containers-vs-virtual-machines | 权威教程 | unknown | 「公寓 vs 隔间」比喻讲清 VM 与容器内核共享/隔离差异 | 4 |

### 方向 2：桌面虚拟化实操（VirtualBox / VMware Workstation）
| 标题 | URL | 来源级别 | 日期 | 相关性 | 评分 |
|---|---|---|---|---|---|
| Oracle VirtualBox User Guide 7.2 — Create a VM | https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/create-vm.html | 官方文档 | ©2022–2024 | 官方当前版图形向导建机步骤：选 ISO、分配内存/磁盘、无人值守安装 | 5 |
| Oracle VirtualBox User Manual — Networking Modes | https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/networkingmodes.html | 官方文档 | unknown | NAT/桥接/仅主机/内部网络权威定义与适用场景，回答「虚拟机如何联网」 | 5 |
| Oracle VirtualBox User Guide 7.2 — Working with VMs（快照） | https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html | 官方文档 | unknown | 快照拍摄/恢复/删除语义，「装好系统先打干净快照」的习惯依据 | 4 |
| Broadcom(VMware) 简体中文手册 — Workstation 安装 Windows 11 | https://techdocs.broadcom.com/cn/zh-cn/vmware-cis/desktop-hypervisors/workstation-pro/17-0/using-vmware-workstation-player-for-windows-17-0/creating-virtual-machines-in-workstation-player-help-win/install-windows-11-on-a-virtual-machine-in-workstation-win.html | 官方文档(中文) | unknown | 向导建机 + 加载 ISO + Win11 vTPM/加密注意点，中文可照做 | 5 |
| 博客园 pcdoctor（2026）VirtualBox 图文教程 | https://www.cnblogs.com/pcdoctor/p/20077169 | 社区 | 2026 | 中文零基础全流程：下载、查 VT-x、关 Hyper-V 冲突、建机、装系统、装增强功能、快照 | 3 |

### 方向 3：选型、使用场景与常见坑
| 标题 | URL | 来源级别 | 日期 | 相关性 | 评分 |
|---|---|---|---|---|---|
| Microsoft Learn — 容器与虚拟机（中文） | https://learn.microsoft.com/zh-cn/virtualization/windowscontainers/about/containers-vs-vm | 官方文档 | unknown | VM 各自独立内核+Hypervisor 隔离 vs 容器共享内核；「何时用哪个」立论 | 5 |
| Broadcom/VMware KB — 精简磁盘与快照越用越大 | https://knowledge.broadcom.com/external/article?legacyId=2019649 | 官方 KB | unknown | 解释快照 delta 与精简磁盘「只增不减」→ defragment/shrink 官方步骤 | 5 |
| MakeUseOf — VDI vs VHD vs VMDK vs VHDX 虚拟磁盘格式 | https://www.makeuseof.com/vdi-vs-vhd-vs-vmdk-vs-vhdx-virtual-disk-image-formats-explained/ | 权威教程 | unknown | 四种磁盘格式归属产品、固定/动态、可否互转，化解「vdi 还是 vmdk」 | 4 |
| 博客园 sunlong88 — VMware/Hyper-V/WSL2/VirtualBox 区别 | https://www.cnblogs.com/sunlong88/p/22498368 | 社区 | unknown | Windows 上四种方案取舍对比，回答「新手该装哪个」 | 4 |
| 160.com — 电脑 VT 开启图文教程 | https://www.160.com/article/10921.html | 权威教程 | unknown | BIOS 开启 Intel VT-x/AMD SVM + 任务管理器确认；注意来源含推广倾向 | 3 |

## 二、方向菜单

请选择 **P2 深度收集覆盖范围**：

- **A. 仅方向 1（概念）**：只深挖虚拟机/Hypervisor/VM vs 容器/WSL 概念。笔记偏理论，实操只点到为止。P2 素材量小。
- **B. 方向 1+2（概念 + 桌面实操）**：概念 + VirtualBox/VMware 建机/装系统/快照/网络步骤。P2 素材量中等。
- **C. 全三方向（概念 + 桌面实操 + 选型避坑）**（推荐）：最贴合「概念和使用」完整主题，产出含「何时用/平台怎么选/常见坑」章节。P2 素材量中偏大。

## 三、覆盖缺口（P2 需补查）

1. **VM vs WSL2 三向对比**：现有来源权威性不足 → P2 补 Microsoft Learn 官方 WSL 文档。
2. **克隆（clone）**：完整/链接克隆与克隆后个性化，需补 VirtualBox User Guide 克隆小节。
3. **VT-x/AMD-V 与 Hyper-V/VBS 冲突**：无单一官方支持页 → 组合官方说明 + 实操验证，标注经验结论。
4. **VirtualBox 无官方简体中文手册**：中文表述以社区图文转述辅助（1 篇已收录）。
5. **VBoxManage modifyhd --compact 等压缩命令**：缺官方 KB → 若写入正文需实测。
6. **网络不通、分配过多内存/CPU 反致宿主机卡顿**：属经验结论 → 引官方网络手册或显式标注为经验。

## 四、预计 P2 范围

- **核心精读**（约 9-11 个）：方向1 五个 + 方向2 前四个官方页 + 方向3 微软「容器与虚拟机」、VMware KB。
- **缺口补查**：Microsoft WSL 官方文档、VirtualBox 克隆小节、VT-x/Hyper-V 冲突权威说明、可选实测压缩命令。
- **产出**：`02_deep_research.md`（scope、source table、claim/source map、矛盾、实践指引、开放问题、下游交接）。
