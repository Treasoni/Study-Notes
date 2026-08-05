# Home Assistant 三种部署方式对比与选型

> [!summary] 笔记说明
> - **主题**：Home Assistant 三种部署方式（HAOS 虚拟机 / Docker Container / HA Supervised）的区别、对比与选型
> - **笔记类型**：对比 + 实战指南（practice + compare，侧重选型决策）
> - **学习深度**：精通
> - **章节结构**：8 章（第 1-7 章为概念、对比、决策与迁移；第 8 章为部署实操附录）
> - **素材引用**：文中 `[素材 §X.Y]` 指向深度研究文件 `02_deep_research.md` 的对应小节（§一.1=HAOS 虚拟机、§一.2=Docker Container、§一.3=HA Supervised、§二=官方声明/迁移/生态、§三=对比表、§四=决策树、§五=社区立场）
> - **信息来源**：官方文档（home-assistant.io）+ 社区实践（Home Assistant 社区论坛、ProxmoxVE 社区脚本）交叉验证

## 目录

1. [第一章：三种部署方式全景](#第一章三种部署方式全景)
   - [1.1 核心概念澄清](#11-核心概念澄清)
   - [1.2 官方对三种方式的定位](#12-官方对三种方式的定位)
   - [1.3 官方安装分类：只有两条正式路径](#13-官方安装分类只有两条正式路径)
   - [1.4 关键纠偏：先破除过期认知](#14-关键纠偏先破除过期认知)
2. [第二章：核心对比表](#第二章核心对比表)
   - [2.1 十维对比总表](#21-十维对比总表)
   - [2.2 最核心差异：功能完整性 vs 灵活性](#22-最核心差异功能完整性-vs-灵活性)
   - [2.3 决策关键差异速查](#23-决策关键差异速查)
3. [第三章：HAOS 虚拟机详解](#第三章haos-虚拟机详解)
   - [3.1 是什么：为 HA 定制的嵌入式操作系统](#31-是什么为-ha-定制的嵌入式操作系统)
   - [3.2 官方为什么推荐](#32-官方为什么推荐)
   - [3.3 虚拟机部署要求（官方）](#33-虚拟机部署要求官方)
   - [3.4 Supervisor 机制拆解](#34-supervisor-机制拆解)
   - [3.5 Proxmox 推荐配置（社区实践）](#35-proxmox-推荐配置社区实践)
   - [3.6 优点 / 缺点 / 适用场景](#36-优点---缺点---适用场景)
4. [第四章：Docker Container 详解](#第四章docker-container-详解)
   - [4.1 是什么：仅 Core 的容器方式](#41-是什么仅-core-的容器方式)
   - [4.2 官方 compose 模板逐行拆解](#42-官方-compose-模板逐行拆解)
   - [4.3 升级与维护流程](#43-升级与维护流程)
   - [4.4 常见坑](#44-常见坑)
   - [4.5 优点 / 缺点 / 适用场景](#45-优点---缺点---适用场景)
5. [第五章：HA Supervised 详解（含弃用现状）](#第五章ha-supervised-详解含弃用现状)
   - [5.1 历史定位与 ADR-0014（已 revert）](#51-历史定位与-adr-0014已-revert)
   - [5.2 官方支持约束（历史定义）](#52-官方支持约束历史定义)
   - [5.3 安装原理与脚本步骤](#53-安装原理与脚本步骤)
   - [5.4 弃用时间线与现状](#54-弃用时间线与现状)
   - [5.5 社区立场与 BYPASS_OS_CHECK 风险](#55-社区立场与-bypass_os_check-风险)
   - [5.6 优点 / 缺点 / 适用场景](#56-优点---缺点---适用场景)
6. [第六章：选型决策树与建议](#第六章选型决策树与建议)
   - [6.1 决策树（完整版）](#61-决策树完整版)
   - [6.2 典型用户画像建议](#62-典型用户画像建议)
   - [6.3 不推荐的组合与原因](#63-不推荐的组合与原因)
   - [6.4 决策背后的权衡原则](#64-决策背后的权衡原则)
7. [第七章：迁移路径与操作](#第七章迁移路径与操作)
   - [7.1 官方迁移原则](#71-官方迁移原则)
   - [7.2 各路径迁移详解](#72-各路径迁移详解)
   - [7.3 跨架构迁移可行性](#73-跨架构迁移可行性)
   - [7.4 迁移注意事项](#74-迁移注意事项)
8. [第八章（附录）：部署实操步骤](#第八章附录部署实操步骤)
   - [8.1 Docker Compose 完整模板与启动](#81-docker-compose-完整模板与启动)
   - [8.2 Proxmox 部署 HAOS VM 完整步骤](#82-proxmox-部署-haos-vm-完整步骤)
   - [8.3 HAOS 直接刷机简述（专用硬件）](#83-haos-直接刷机简述专用硬件)
   - [8.4 HA Supervised 安装脚本（附弃用警告）](#84-ha-supervised-安装脚本附弃用警告)
   - [8.5 初始化引导与备份恢复](#85-初始化引导与备份恢复)

---

## 第一章：三种部署方式全景

选 HA 部署方式时，网上常见的「HAOS / Docker Container / Supervised 三选一」框架在 2025 年后已过时：Supervised 不再是官方正式路径。这一章先厘清 Core、Supervisor、OS、Add-on 四个概念的关系，再给出官方视角下的部署全景，为后续对比与选型打地基。

### 1.1 核心概念澄清

四个名词分属不同层级：主程序、管家、操作系统、托管容器。

- **Home Assistant Core**：HA 的应用本体，集成、自动化、前端都运行在此进程，可跑在容器或操作系统中；是「HA 本身」，不具备系统管理能力 [素材 §一.1]。
- **Supervisor**：Docker 之上的容器管理器「管家」，负责 Add-on 商店、快照备份、自动更新，HAOS 的省心正源于它；Container 方式没有此组件 [素材 §一.1]。
- **HAOS**：专为 HA 定制的嵌入式极简 Linux，只读文件系统、无 apt、独占整机，内建 Core + Supervisor [素材 §一.1]。
- **Add-on**：Supervisor 托管的 Docker 容器（Thread、Z-Wave、ESPHome 等），经商店一键安装，可加第三方源；区别于 Core 内运行的「集成」[素材 §一.1]。

关系图：

```text
HAOS（嵌入式只读 Linux）
├── Supervisor（管家）
│   ├── Add-on 容器（Thread / Z-Wave / ESPHome …）
└── Core（HA 主程序本体）
```

HAOS 三层全有；Container 只有 Core；Supervised 在自管理 Linux 上装 Supervisor + Core。

### 1.2 官方对三种方式的定位

| 部署方式 | 官方定位 | 正式支持 | 维护难度 |
|---------|---------|---------|---------|
| HAOS | recommended for most users，most convenient | ✅ 推荐 | 低 |
| Container | 支持，仅限 Core | ✅ | 中（需 Docker） |
| Supervised | 曾「only for advanced users」 | ⚠️ 已弃用 | 高（Expert） |

- **HAOS**：官方推荐给大多数用户，最省心——Supervisor 全托管 Add-on、约每 8 小时自动更新、一键快照备份 [素材 §一.1]。
- **Container**：官方支持但仅 Core，无 Supervisor/Add-on/OTA，Thread、Z-Wave 开箱不支持 [素材 §一.2]。
- **Supervised**：历史定位「only for advanced users」，已随弃用失效（见 1.4）[素材 §一.3]。

### 1.3 官方安装分类：只有两条正式路径

官方安装文档的正式分类只有 **HA OS** 和 **Container**，Supervised 不在其列 [素材 §一.1]。由此，「三选一」教程基于过时框架需警惕；真正权衡的是「全托管（HAOS）」与「自托管 Core（Container）」两条主线；Supervised 章节的意义在理解历史与迁移，而非推荐。

### 1.4 关键纠偏：先破除过期认知

**ADR-0014 已 revert**：该 ADR 曾定义 Supervised 为官方支持的安装方式，现标记 **reverted**（已撤销）；网上大量教程基于这份已撤销的正式支持，属过期认知 [素材 §一.3]。

**弃用时间线**：

| 时间 | 事件 |
|------|------|
| 2025-05-22 | 公告弃用 Core、Supervised 及 32 位系统 |
| 2025.6 起 | 受影响系统显示「支持将在六个月后结束」通知 |
| 2025.12 | 官方支持终止（supervised-installer 标注 unsupported with HA OS 2025.12.0） |

弃用后仍可继续使用更新，但官方不再接受问题报告、移除端用户文档 [素材 §二]。使用率数据也解释了清理动因：Core 约 2.5%、Supervised 约 3.3%。

**正确视角**：把「三选一」改写为「**官方两条路径 + 一条弃用中的旧路径**」：正式路径为 **HAOS**（全托管）与 **Container**（自托管 Core）；旧路径为 **Supervised**（仅 Debian）。

### 本章小结

- 四概念层级：Core 主程序、Supervisor 管家、HAOS 内建两者的只读系统、Add-on 托管容器。
- 官方正式路径只有 HAOS 与 Container，「三选一」已过时。
- HAOS 官方推荐（most convenient）；Container 仅 Core；Supervised 已弃用。
- ADR-0014 已 revert，Supervised 支持于 2025.12 终止。
- 阅读视角：官方两条路径 + 一条弃用中的旧路径。

---

*接下来：第二章给出十维对比总表，把三种方式在功能、维护、资源上的差异一次看清，并提炼选型最关键的两三条差异。*

## 第二章：核心对比表

把三种部署方式放进同一张表横向比较，是选型决策最快的一条路。这一章先用一张十维对比总表把 HAOS、Container、Supervised 的差异一次摆平，再拆出两条最核心的权衡轴，最后给出三个「看一眼就能决定大多数场景」的速查要点。

### 2.1 十维对比总表

下表数据基于官方文档与社区实践交叉验证，一行一个维度，覆盖定位、功能、资源与维护四个层面 [素材 §三]。

| 维度 | HAOS VM | Docker Container | HA Supervised |
|------|---------|------------------|---------------|
| 官方定位 | 推荐（most users） | 支持 | 已弃用（2025.12 终止） |
| 含 Supervisor | ✅ | ❌ | ✅ |
| Add-on 商店 | ✅ | ❌ | ✅ |
| 自动更新 OS/Core | ✅（约每 8h 检查） | ❌（手动 pull） | 部分（Supervisor 停更） |
| 托管快照备份 | ✅ | ❌ | ❌ |
| Thread/Z-Wave 集成 | ✅（Add-on） | ❌ 开箱不支持 | ✅ |
| 可与其他服务共存 | ❌ 独占 | ✅ | ⚠️ 会被标记 Unsupported |
| 资源占用 | 2-4GB（推荐 4GB） | 空闲约 300-400MB | 视宿主 |
| 维护难度 | 低 | 中（需 Docker 技能） | 高（Expert） |
| 底层系统 | 只读嵌入式 OS | 自己管理的 Linux | 必须 Debian（无衍生版） |
| 更新方式 | Supervisor 自动 | docker pull 重建 | Supervisor（已停更） |

读表顺序建议，不要逐行看，而是按三个「块」扫：

- **功能块**（含 Supervisor / Add-on 商店 / 自动更新 / 托管快照备份 / Thread-Z-Wave）：HAOS 全 ✅，Container 全 ❌，Supervised 半 ✅。这一块决定了「这个部署方式能干什么」。
- **资源与维护块**（资源占用 / 维护难度 / 可共存）：HAOS 最重但最省心，Container 最轻但要全手动，Supervised 维护成本最高且官方已退出。
- **系统与生命线块**（官方定位 / 底层系统 / 更新方式）：HAOS 只读独占、官方推荐；Container 完全自管、官方支持；Supervised 被锁死在纯 Debian 且处于弃用边缘 [素材 §三、§一.3]。

### 2.2 最核心差异：功能完整性 vs 灵活性

十一个维度里，绝大多数差异都能被一条主线解释：**功能完整性**与**灵活可控性**的此消彼长。

- **功能完整性**指「全托管能力」：Supervisor、Add-on 商店、自动更新、托管快照备份、Thread/Z-Wave 开箱即用，本质是把运维职责交给系统本身。
- **灵活可控性**指「你自己能决定什么」：能否与其他服务共存、能否随意装系统组件、备份反代更新是否由你掌控。

三个端点的取舍：

- **HAOS 端**：功能完整、零维护，代价是独占整机、只读系统、无 apt，无法在宿主机上跑任何其他服务 [素材 §一.1]。
- **Container 端**：轻量灵活、可共存，代价是无 Add-on、备份/反代/更新全手动，需要 Docker 技能 [素材 §一.2]。
- **Supervised 端**：理论上是「全功能 + 宿主控制权」的兼得解，但官方已弃用，宿主约束极严（仅 Debian 无衍生版、必须专用于 HA），实际被排除在正式路径之外 [素材 §一.3]。

#### 两条轴如何交叉

把「功能完整性」作横轴、「灵活可控性」作纵轴，三者的位置一目了然：

| | 功能完整 | 功能精简 |
|---|---|---|
| 高灵活（自管理） | Supervised（理论） | **Container** |
| 低灵活（托管） | **HAOS** | —（无意义） |

- **右下格是 Container**：功能精简 + 高灵活，把 HA 当作一个普通容器与 NAS/VPS 上其他服务共存。
- **左下格是 HAOS**：功能完整 + 低灵活，用「独占整机」换「零维护 + 全功能」。
- **左上格是 Supervised**：它承诺的正是这个格子，但官方弃用 + 严格宿主约束让这个位置名存实亡，选它等于选中右上角的「无意义」风险。
- **右上格无意义**：功能精简还不灵活，没有任何理由选它。

再叠加一条子轴：**省心 ↔ 资源占用**。HAOS 用 2-4GB 内存换省心；Container 用约 300-400MB 的空闲占用换手动维护 [素材 §三]。两条轴交叉后，选型本质是在「多花钱买省心、全功能」与「少花钱自己维护」之间选一个落点。

### 2.3 决策关键差异速查

如果只记三条差异，就能覆盖大多数选型场景：

1. **最核心功能差异**：Container 无 Add-on 商店、无 Thread/Z-Wave 开箱支持、无自动更新——这三项是它与 HAOS 之间最本质的功能缺失 [素材 §五.4]。需要 Add-on 生态、Thread 或 Z-Wave 集成，就只能走 HAOS（Supervised 已不推荐）；只需要 HA 核心自动化与集成，Container 完全够用。
2. **资源量级分水岭**：HAOS 虚拟机推荐 4GB 内存（最低 2GB），Container 空闲约 300-400MB，两者差了一个量级以上 [素材 §三]。这是「独占一台设备」与「共存在 NAS/VPS 上」的资源边界。
3. **维护成本阶梯**：低（HAOS，Supervisor 全托管）→ 中（Container，需 Docker 技能、手动更新与备份）→ 高（Supervised，Expert 级、仅 Debian 且已弃用）[素材 §三]。维护阶梯与官方支持状态严格正相关，选型时应当把「官方支持的终止时间」也算进长期成本。

一句话收束：想要全功能 + 低维护 → **HAOS**；想要低占用 + 高灵活且能接受手动维护 → **Container**；官方在这两者之间不再提供推荐的中间态。

### 本章小结

- 十维对比总表一次看清三者的定位、功能、资源与维护差异。
- 核心权衡轴：功能完整性 ↔ 灵活可控，省心 ↔ 资源占用，两轴交叉后只有两个有效落点（HAOS / Container）。
- 最核心功能差异：Container 缺 Add-on / Thread / Z-Wave / 自动更新。
- 资源分水岭：HAOS 推荐 4GB vs Container 空闲约 300-400MB。
- 维护阶梯：低 / 中 / 高，与官方支持状态正相关。

---

*接下来：第三章深挖 HAOS 虚拟机——官方为什么推荐、Supervisor 托管机制如何运转、虚拟机官方要求与 Proxmox 推荐配置，以及「零维护」光环背后的真实代价。*

## 第三章：HAOS 虚拟机详解

上一章的对比表里，HAOS 在功能完整度上几乎全面占优，但「官方推荐」到底是营销话术还是实打实的好处，需要落到它究竟怎么运行、怎么维护上来验证。这一章拆解 HAOS 的本质（嵌入式只读 OS）、官方推荐的理由、虚拟机部署的硬性要求、Supervisor 的托管机制，并给出社区在 Proxmox 上部署的推荐配置与可复制的命令，最后收束到优缺点与适用场景，帮你判断「独占一台机器」这个代价是否值得。

### 3.1 是什么：为 HA 定制的嵌入式操作系统

HAOS（Home Assistant Operating System）是 Home Assistant 官方为 HA 量身定制的嵌入式极简 Linux [素材 §一.1]。说「嵌入式」，不是指它只能跑在开发板上，而是指它的设计哲学与消费级固件一致：镜像烧录、只读根文件系统、无需也不允许用户安装系统级软件，一切面向「开机即用」。

三个关键特征决定了它的性格：

- **只读文件系统**：根分区以只读方式挂载，用户无法（也不需要）像管理普通 Linux 那样写系统文件。系统更新走的是整镜像级别的 OTA，而不是 `apt upgrade` 式的增量修补。
- **无 apt、无包管理**：想装系统级软件（比如 `nginx`、`vim`）是做不到的。需要在 HA 里扩展功能，走的是 Supervisor 的 Add-on 商店，而不是 Linux 包管理器。这既是限制，也是它长期稳定、不被打爆的保证。
- **独占整机**：HAOS 启动后整台机器的资源只为 HA 服务，不能同时跑 Plex、NAS 等别的服务。在虚拟机里部署时，这意味着这个 VM 就是一台「专用设备」。

用一个类比来理解：普通 Linux 像一台「通用电脑」，你可以在上面装任何软件、改任何配置，但代价是要自己负责它的健康；HAOS 则像一台「专用家电」——就像空气净化器只负责净化空气，HAOS 只负责跑 HA，系统层面被锁死，你不必（也不能）去动它。绝大多数智能家居用户需要的是后者：机器能一直稳定跑，而不是一个可以自由折腾的服务器。

结构上，HAOS 内建了完整的 Core + Supervisor 组合 [素材 §一.1]：

```text
HAOS（嵌入式只读 Linux）
├── Docker（容器运行时）
├── Supervisor（管家：Add-on 商店 / 快照备份 / 自动更新）
│   └── Add-on 容器（Thread / Z-Wave / ESPHome …）
└── Home Assistant Core（HA 主程序本体）
```

对比第一章里提到的 Container 方式，HAOS 多出的是整个 Supervisor 层以及由它托管的 Add-on 生态；对比 Supervised，HAOS 多出的是官方严格封装、只读、不可乱改的底层系统——上层省心、下层也锁死，这正是它「零维护」的根基。

### 3.2 官方为什么推荐

官方文档把 HAOS 定义为 "recommended installation type for most users"，理由直接写成 "most convenient"（最省心）[素材 §一.1]。这不是空泛的评价，背后是三个具体能力：

1. **刷完即用**：镜像烧录或导入虚拟机后，首次开机进入引导页（`homeassistant.local:8123`），按向导创建账户、可选恢复备份即可，全程不需要碰命令行。
2. **全托管体验**：Supervisor 替你管理 Add-on 安装、快照备份、系统更新。你面对的是一个「电器」而不是「服务器」。
3. **自动更新链路**：Supervisor 约每 8 小时检查一次，可自动更新 OS 内核、Supervisor 自身以及 Core，无需手工介入 [素材 §一.1]。

把这三个能力放在一起看，官方推荐的逻辑就清晰了：HA 的用户画像里，绝大多数人想要的是「智能家居能一直稳定跑」，而不是「学会运维一套 Linux」。HAOS 把运维复杂度全部封装进 Supervisor，正是为了服务这个主流需求。对照第二章对比表中「维护难度：低」那一行，HAOS 是三种方式里唯一把更新、备份、扩展全部托管的。

需要再次强调：官方安装文档的正式分类里，只有 HAOS 和 Container 两条路径（第一章已详述）。HAOS 是其中「全功能 + 零维护」的一端，这也是它成为官方口中 most users 默认选择的原因。

### 3.3 虚拟机部署要求（官方）

HAOS 可以刷到专用硬件（树莓派、工控机等），也可以作为虚拟机运行在 Proxmox / VirtualBox / VMware / Hyper-V 上。官方给出了一套明确的虚拟机部署要求 [素材 §一.1]。

#### 硬件最低要求

| 资源 | 最低 | 推荐 |
|------|------|------|
| 内存 | 2GB | 4GB |
| vCPU | 2 核 | 2+ 核 |
| 磁盘 | 32GB | 更大（含快照与备份缓冲） |

注意 32GB 只是最低磁盘，HA 的数据库、媒体、快照会持续增长，实际建议预留 40-64GB，并配合快照策略。

#### UEFI：必须启用

HAOS 的引导要求 UEFI 固件，缺了它虚拟机无法启动 [素材 §一.1]。为什么必须是 UEFI？HAOS 的引导流程基于 UEFI 规范（systemd-boot / OVMF），其引导逻辑不兼容传统 BIOS 的 MBR 启动流程。因此无论哪个虚拟化平台，固件设置里都必须把启动模式切到 UEFI，而不是「能开机就万事大吉」：

- **VirtualBox**：虚拟机设置里勾选 "Use EFI"（默认是 BIOS，必须手动改）。
- **KVM / Proxmox**：BIOS 选项选 OVMF（UEFI）固件，注意选非 secureboot 的 OVMF，并给 VM 挂一块 EFI 盘。
- **VMware / Hyper-V**：同样在固件设置中把 BIOS 切换为 UEFI。

这是新手部署 HAOS VM 最常见的失败点之一：镜像正确、配置看着没问题，但忘了 UEFI，开机就黑屏。

#### 镜像格式

官方按虚拟化平台提供不同格式的虚拟磁盘镜像，统一命名为 `haos_ova-{version}`，下载后需先解压再使用 [素材 §一.1]：

| 格式 | 对应平台 | 说明 |
|------|---------|------|
| qcow2 | KVM / Proxmox | QEMU 原生格式，支持快照 |
| vdi | VirtualBox | VirtualBox 默认格式 |
| vmdk | VMware | VMware 系列产品 |
| vhdx | Hyper-V | 微软 Hyper-V 格式 |
| ova | 跨平台 | 打包格式，内含虚拟机和磁盘 |

部署的本质动作是：建一台开启 UEFI 的虚拟机 → 把解压后的磁盘镜像挂给这台 VM（Proxmox 里是 `qm importdisk` 导入）→ 启动 → 浏览器访问 `homeassistant.local:8123` 完成初始化。完整的 Proxmox 操作步骤见第八章附录，本节聚焦参数层面的要求。

### 3.4 Supervisor 机制拆解

Supervisor 是 HAOS「省心」的核心引擎。理解它的三个机制，就理解了 HAOS 为什么比 Container 方式省事 [素材 §一.1]。

#### Add-on 本质是 Docker 容器

Add-on 商店里那些「插件」（Thread、Z-Wave JS、ESPHome、Node-RED、Samba、SSH 等），本质都是 Supervisor 托管的 Docker 容器 [素材 §一.1]。Supervisor 负责：从商店拉取镜像、创建容器、按依赖关系启动、崩溃自动重启、在设置页暴露配置入口。

这与「集成」（Integration）有本质区别：集成跑在 Core 进程内，Add-on 是独立容器。需要系统级能力（如操作 Zigbee 协调器、编译 ESPHome 固件）的功能，都以 Add-on 形式提供——这也是 Container 方式「开箱不支持 Thread / Z-Wave」的根本原因（见第二章对比表）。

Supervisor 对 Add-on 的生命周期是全程托管的：安装时校验依赖、拉取镜像并创建容器，运行时按 restart 策略守护，卸载时清理容器与镜像。用户不接触 Docker CLI，一切通过商店界面完成——这是「容器技术」与「家电式体验」之间的关键桥梁。

#### 快照备份与一键还原

Supervisor 提供托管快照（Snapshot）：把 HA 配置、集成状态、Add-on 及其数据、媒体全部打包成压缩归档，可下载到本地，也可存到 Google Drive / OneDrive / NAS 等备份位置。还原时在初始化向导或设置页一键导入即可，甚至可以做到任意安装方式之间、跨架构恢复（第七章会详述迁移）。

对普通用户的意义：备份不再是一个需要自己写 cron + rsync 的工程问题，而是设置页里的一个开关。

#### OTA 式自动更新链路

Supervisor 约每 8 小时检查一次更新 [素材 §一.1]，更新对象包括：

- **OS**（HAOS 底层镜像）
- **内核**（随 OS 一起）
- **Supervisor 自身**
- **Core**（可选，可按更新策略设置）

更新方式接近 OTA：Supervisor 拉取新镜像、创建新分区/新容器、原子切换，失败可回滚，而不是在现有系统上「原地打补丁」。用户可以设置自动更新策略（如只自动更 Supervisor，Core 手动确认），兼顾省心与稳妥。

### 3.5 Proxmox 推荐配置（社区实践）

Proxmox 是社区跑 HAOS 的主流平台——多数老用户的做法就是「Proxmox 上 HAOS VM + 其他服务用独立 LXC/VM」，不把杂项服务塞进 HA [素材 §二]。社区实践沉淀了一套推荐配置 [素材 §一.1]：

| 项 | 推荐 | 原因 |
|----|------|------|
| 机型 | q35 | 现代芯片组，支持 UEFI |
| BIOS | UEFI（OVMF + EFI 盘） | HAOS 引导必需 |
| 存储控制器 | virtio-scsi-pci | 性能好，社区标准 |
| 磁盘 | 32GB（可扩容） | 满足官方最低要求 |
| CPU | kvm64 2 核（可迁移）/ host（性能最好） | 见下方权衡 |
| 内存 | 4096MB + `-balloon 2048` 内存气球 | 预留 4GB，气球可回收 |
| 网络 | vmbr0 | 桥接，走局域网 |

- **q35 + UEFI**：3.3 节已说明 HAOS 强制 UEFI。Proxmox 默认机型 i440fx 是兼容老系统的芯片组，虽然也能挂 OVMF，但社区一致推荐 q35——它是现代芯片组，PCIe、热插拔、UEFI 支持更完整，与 HAOS 引导的兼容性最稳。
- **kvm64 vs host**：`kvm64` 是对齐虚拟化的通用 CPU 型号，性能略低但 VM 可在不同节点间迁移；`host` 直通宿主 CPU 特性、性能最好，但 VM 绑定当前节点、不可迁移。家里单机跑选 host；想为将来在集群里迁移留余地选 kvm64。
- **内存气球**：`-balloon 2048` 表示给 VM 的内存上限仍是 4096MB，但最小可收缩到 2048MB——Proxmox 通过 balloon 驱动在 VM 内存空闲时回收多余部分给其他 VM，缓解宿主机内存竞争。注意气球压力过大时（宿主机紧张触发回收）可能影响 HA 实时性，建议实际运行观察，若出现卡顿可调高下限或直接去掉气球。

#### 实操命令（原样摘录）

以下命令来自社区脚本与 Proxmox CLI，按场景直接复制使用 [素材 §一.1]。

**一键部署脚本**（自动完成下载镜像、建 VM、导盘、配 UEFI）：

```bash
# 一键脚本
bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
```

**USB 直通**（Zigbee / Z-Wave / 蓝牙适配器，先 stop VM 再操作）：

```bash
# USB 直通（先 stop VM，用 lsusb 查 vendor:product）
qm set <VMID> -usb0 host=10c4:ea60
qm stop <VMID> && qm start <VMID>
```

`host=10c4:ea60` 是 `lsusb` 输出的 `vendor:product`。直通前必须停止 VM，直通后重启 VM 才生效。这步对智能家居至关重要——Zigbee / Z-Wave 协调器必须被 VM 独占访问。

**快照备份**（VM 不停机 + zstd 压缩）：

```bash
# 备份（snapshot 模式 + zstd）
vzdump <VMID> --mode snapshot --compress zstd --storage local
```

`--mode snapshot` 让 VM 运行时也能做一致性备份；`--compress zstd` 显著减小体积。配合 Supervisor 的快照，形成「宿主机整机备份 + HA 配置快照」双保险。

**扩容磁盘**：

```bash
# 扩容
qm resize <VMID> scsi0 +32G
```

扩容后需在 HAOS 内部分区扩容，通常重启后系统会自动识别扩大分区。

### 3.6 优点 / 缺点 / 适用场景

| 维度 | 说明 |
|------|------|
| 优点 | 零维护、Add-on 生态完整、一键快照备份、更新省心、官方推荐 |
| 缺点 | 只读系统、无 apt、独占整机、排障困难、资源开销大 |
| 适用 | 专用智能家居设备、想要零维护、能接受独占一台机器 |

展开来看：

**优点**

- 刷完即用，Supervisor 全托管，日常几乎不用碰命令行。
- Add-on 生态完整：Thread、Z-Wave、ESPHome 等系统级能力开箱即用。
- 一键快照备份，且跨安装方式 / 跨架构可恢复（第七章详述）。
- 自动更新链路成熟，OS / 内核 / Supervisor 约每 8 小时检查更新，用户无感。

**缺点**

- 只读文件系统、无 apt：无法在系统层自由安装软件，系统级需求只能靠 Add-on。
- 独占整机：这台机器（或这个 VM）只为 HA 服务，不能同时跑其他服务。
- 排障困难：系统不透明，出问题时不像普通 Linux 那样容易深入排查。
- 资源开销大：官方推荐 4GB 内存，比 Container 方式（空闲约 300-400MB）重一个量级。

**适用场景**

- 想零维护、功能完整地跑 HA，且能接受一台机器（或一个 VM）专门服务 HA。
- 已经用 Proxmox / VMware 等虚拟化平台，顺手建一个 HAOS VM（社区主流做法）。
- 看重 Add-on 生态（Thread / Z-Wave / ESPHome），又不愿意手工维护 Linux 环境。
- 不适合：想在 NAS / VPS 上与其他服务共存、能接受手动维护的用户——那更适合第四章的 Container 方式。

### 本章小结

- HAOS 是只读、无 apt、独占整机的嵌入式 Linux，内建 Core + Supervisor，是官方定位 most users 的推荐方式。
- 虚拟机部署硬性要求：最低 2GB / 2vCPU / 32GB（推荐 4GB）、必须启用 UEFI（VirtualBox 勾 EFI，KVM 用非 secureboot 的 OVMF）、镜像按平台选 qcow2 / vdi / vmdk / vhdx / ova。
- Supervisor 三件套：Add-on 是托管的 Docker 容器、快照一键备份与还原、约每 8 小时 OTA 自动更新 OS / 内核 / Supervisor。
- Proxmox 社区配置：q35 + UEFI + virtio-scsi-pci + 32GB 磁盘，CPU 用 kvm64（可迁移）或 host（性能最好），内存 4096MB + 内存气球。
- 优点集中在省心与功能完整，代价是只读系统、独占整机、资源开销大；适合愿意用一台专用机器换零维护的用户。

---

*接下来：第四章转向天平的另一端 Docker Container——只跑 Core、无 Supervisor 与 Add-on，看官方 compose 模板逐行拆解、升级维护与常见坑。*

## 第四章：Docker Container 详解

上一章的 HAOS 虚拟机是官方推荐的全托管方案，但它独占整机、无法与别的服务共存。如果你手里已经有一台 NAS 或 VPS，想把 HA 塞进去而不是再开一台机器，Docker Container 就是官方两条正式路径里更轻的那条。这一章回答三个问题：Container 版到底少了什么、官方 compose 模板每一行在做什么、以及日常升级和踩坑怎么处理。

### 4.1 是什么：仅 Core 的容器方式

Container 方式 = **你自己的 Linux 系统 + Docker 编排，只运行 Home Assistant Core 这一个容器**。官方定义是「自带系统（Linux）+ Docker 编排，只运行 Home Assistant Core」[素材 §一.2]。这里「自带系统」指宿主 OS 由你管理（Debian、Ubuntu、NAS 的 DSM 等），Docker 负责把 Core 圈在容器里跑。

#### 它有什么、没有什么

| 能力 | Container | HAOS |
|------|-----------|------|
| Core | ✅ | ✅ |
| Supervisor | ❌ | ✅ |
| Add-on 商店 | ❌ | ✅ |
| OTA 自动更新 | ❌（手动 pull） | ✅（约每 8h 检查） |
| 托管快照备份 | ❌ | ✅ |
| Thread / Z-Wave | ❌ 开箱不支持 | ✅（由 Add-on 提供） |
| 与其他服务共存 | ✅ | ❌ 独占 |

一句话总结：**Container 是「裸 Core」**。因为 Add-on 本质是 Supervisor 托管的 Docker 容器，没有 Supervisor 就没有 Add-on 商店；Thread、Z-Wave 这类硬件协议集成依赖 Add-on 提供运行环境，Container 开箱即不支持 [素材 §一.2]。这正是它与 HAOS 最核心的功能差异。

#### 硬性要求

- **Docker Engine ≥ 23.0.0**（Docker CE 或 Linux 发行版仓库里的新版均可）。
- **Docker Desktop 不可用**：HA 依赖 host 网络模式和 USB 设备直通，这两者依赖 Linux 内核能力；Docker Desktop 在 macOS / Windows 上运行在虚拟机层之上，host 网络行为不兼容、设备直通不可用，官方不视为受支持环境 [素材 §一.2]。

> [!warning] 平台边界
> 不要在 macOS / Windows 桌面上直接跑 Container 版 HA。要么改用 WSL2 内的原生 Docker Engine（Linux 语义），要么干脆选 HAOS 虚拟机。

### 4.2 官方 compose 模板逐行拆解

官方提供了一份开箱即用的 docker-compose 模板，完整给出如下 [素材 §一.2]：

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /PATH_TO_YOUR_CONFIG:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro      # 蓝牙集成必需
    restart: unless-stopped
    privileged: true
    network_mode: host
    environment:
      TZ: Europe/Amsterdam          # 必须是 tz database 名称
    devices:                        # USB 直通 Zigbee/Z-Wave
      - /dev/ttyUSB0:/dev/ttyUSB0
```

#### image：镜像来源

`ghcr.io/home-assistant/home-assistant:stable` —— 官方镜像发布在 GitHub Container Registry（ghcr.io）。`stable` 是稳定版标签；想回滚到特定版本时，把它改成具体版本号（如 `2025.7.4`）即可，见 4.3。

#### volumes：三个挂载各自为什么

| 挂载 | 作用 | 说明 |
|------|------|------|
| `/PATH_TO_YOUR_CONFIG:/config` | 配置持久化 | HA 的 `configuration.yaml`、数据库、custom_components 全在 /config，必须挂到宿主持久目录，否则容器重建即全部丢失 |
| `/etc/localtime:/etc/localtime:ro` | 时区文件 | 只读挂载宿主时区，让容器内日志与调度时间和宿主一致 |
| `/run/dbus:/run/dbus:ro` | 蓝牙集成必需 | 宿主 D-Bus 是蓝牙栈（BlueZ）的通信通道，只读挂载后 HA 才能发现并控制蓝牙适配器 |

其中 `:ro` 表示只读挂载，防止容器内误写宿主的系统文件。

#### restart: unless-stopped

容器异常退出时自动重启，但手动 `docker stop` 后不会再被拉起。适合常驻服务，避免断电、崩溃后 HA 一直掉线。

#### privileged: true

特权模式。HA 需要访问大量底层硬件（USB、部分内核接口），官方模板直接用特权模式换取最广的硬件兼容性。若想收敛权限，需要逐项用 `capabilities` + `devices` 替代，但官方模板并不保证精简后仍完整可用——能跑官方默认配置就先用默认配置。

#### network_mode: host：模板里最重要的一行

直接使用宿主的网络栈，容器不拥有独立 IP。必须用 host 网络的原因是：**mDNS 设备发现和蓝牙发现依赖在宿主网络接口上广播 / 监听，bridge 网络会隔离这些广播包**。代价是端口无法用 `ports` 映射管理（见下节）。

#### environment: TZ

时区必须是 tz database 标准名称（如 `Asia/Shanghai`），不是 `UTC+8` 这种偏移量写法。即使挂载了 `/etc/localtime`，仍建议显式设置，避免容器内运行时差异。

#### devices：USB 设备直通

把宿主的 USB 串口设备映射进容器，典型场景是 Zigbee（Conbee、自制 CC2531 等）或 Z-Wave 适配器。可以先用 `lsusb` 查设备的 vendor:product ID，也可以直接用 `/dev/ttyUSB0` 这种设备路径。直通后还要保证容器用户有权限访问，见 4.4。

#### 为什么没有 ports 段

这是新手最容易疑惑的点。既然 `network_mode: host`，容器与宿主共享网络栈，HA 的 8123 端口直接暴露在宿主所有网卡上，**不需要、也无法再用 `ports` 做端口映射** [素材 §一.2]。反过来，网上有些教程既保留 host 网络又让你写 `ports:`，那是矛盾的配置。只有放弃 mDNS/蓝牙发现、改用 bridge 网络时，`ports` 才派得上用场，但会失去发现能力。

#### 启动与验证

```bash
docker compose up -d
docker ps                         # 看容器状态是否为 Up
docker logs homeassistant         # 观察启动日志，直到出现 Home Assistant 启动完成
```

首次启动后浏览器访问 `http://<宿主IP>:8123`，进入初始化向导。

### 4.3 升级与维护流程

Container 没有 OTA，更新 = **拉新镜像 + 重建容器**，配置与数据留在 /config 挂载目录里不受影响 [素材 §一.2]。

#### 方式 A：compose 项目（推荐）

```bash
docker compose pull
docker compose up -d
```

`pull` 拉取新镜像，`up -d` 用新镜像重建容器并沿用 compose 里的全部配置。升级前建议先备份 /config。

#### 方式 B：纯 docker run

```bash
docker pull ghcr.io/home-assistant/home-assistant:stable
docker stop homeassistant
docker rm homeassistant
# 用与首次启动完全相同的参数重新 run
docker run -d --name homeassistant \
  --restart unless-stopped \
  --privileged \
  --network host \
  -e TZ=Asia/Shanghai \
  -v /PATH_TO_YOUR_CONFIG:/config \
  -v /etc/localtime:/etc/localtime:ro \
  -v /run/dbus:/run/dbus:ro \
  --device /dev/ttyUSB0:/dev/ttyUSB0 \
  ghcr.io/home-assistant/home-assistant:stable
```

> [!tip] 回滚
> 新版翻车时，把镜像 tag 指回上一个可用版本，再走一遍重建流程即可。HA 配置文件向后兼容，回滚不会丢 /config 数据。

#### 三件「手动」的事

| 事项 | 说明 |
|------|------|
| 备份 | 无托管快照，需自行定期备份 /config（tar、rsync、NAS 快照均可） |
| 反向代理 | 公网访问需自己配置 Nginx / Caddy 反代，官方不提供托管入口 |
| 更新 | 无自动检查通知，需关注官方 release 公告或自行接入更新提示 |

HA 官方约每月发布一个大版本，习惯了 HAOS「自动升级」的用户，用 Container 后要自己记着这个节奏。

### 4.4 常见坑

#### ARM64 SoC 页大小 >4K：DISABLE_JEMALLOC

部分 ARM64 开发板（内存页大小 >4KB）启动时崩溃，日志报：

```
<jemalloc>: Unsupported system page size
```

解决：在 environment 里加 `DISABLE_JEMALLOC=true`，让 HA 不使用 jemalloc 内存分配器 [素材 §一.2]。

```yaml
    environment:
      TZ: Asia/Shanghai
      DISABLE_JEMALLOC: "true"
```

#### /dev/tty* 权限不足

USB 直通后容器内可能仍打不开串口。确保容器运行用户属于宿主的 `dialout` / `plugdev` 组，或通过 udev 规则放开 `/dev/ttyUSB0` 的访问权限 [素材 §一.2]。症状通常是日志里出现 `Permission denied`、集成反复「设备不可用」。

#### 防火墙挡住 8123

容器能跑但外部访问不了时，先查宿主防火墙。Ubuntu 的 ufw 默认会拦掉入站端口，需要放行 [素材 §一.2]：

```bash
sudo ufw allow 8123/tcp
```

#### 别把 host 网络改成 bridge

为了「安全」把 `network_mode` 改成 bridge 后，mDNS 设备发现、蓝牙发现会失效，常见症状是「设备一直搜索不到、自动发现全没了」。host 网络是官方模板的默认配置，改动前先想清楚取舍 [素材 §一.2]。

### 4.5 优点 / 缺点 / 适用场景

| 维度 | 结论 |
|------|------|
| 优点 | 最灵活；资源占用低（空闲约 300-400MB）；可与其他容器共存（NAS / VPS）；崩溃不影响宿主 |
| 缺点 | 无 Add-on 生态；备份 / 反代 / 更新全手动；需要 Docker 技能 |
| 适用 | 已有 Docker 主机 / NAS 用户；想与其他服务共存；能接受手动维护 |

- **最适合**：手里已有群晖 / 威联通 / 自建 NAS 或 VPS，不想为 HA 独占一台机器。Core 的空闲占用约 300-400MB，在 NAS 上几乎无感 [素材 §一.2]。
- **最不适合**：想要 Add-on 商店、Thread / Z-Wave 开箱支持、零维护体验的用户——这些正是 HAOS 的强项（第三章）。
- **定位提醒**：Container 是官方两条正式路径之一（另一条是 HAOS）。选它是「以功能减配换取共存与轻量」，不是「更差」，是取舍不同。

### 本章小结

- Container 只跑 Core：无 Supervisor、无 Add-on、无 OTA，Thread / Z-Wave 开箱不支持。
- 硬性要求 Docker Engine ≥ 23.0.0，Docker Desktop 不可用（host 网络 + USB 直通依赖 Linux）。
- host 网络是模板核心：mDNS / 蓝牙发现依赖它，因此模板里没有 ports 段。
- 升级 = docker pull + 重建（compose 则 `pull && up -d`）；备份 / 反代 / 更新全手动。
- 常见坑：DISABLE_JEMALLOC、/dev/tty* 权限、ufw 放行 8123、勿改 bridge。

---

*接下来：第五章补上第三条旧路径 HA Supervised——它曾在完整 Linux 上提供 Core + Supervisor，因宿主约束严苛、官方已于 2025.12 终止支持，社区普遍不再推荐。*

## 第五章：HA Supervised 详解（含弃用现状）

前两章讲完了官方两条正式路径——HAOS（全托管）与 Container（轻量 Core）。这一章补上第三条：HA Supervised。它曾在完整 Linux 上同时提供 Supervisor 与 Add-on，理论上兼得「全功能」与「宿主控制权」，但官方支持已于 2025.12 终止。这一章回答：它到底是什么、安装器在做什么、为什么被弃用、社区怎么看，以及它是否还有保留价值。

> [!warning] 先记住结论
> HA Supervised 已于 **2025.12 官方支持终止**，本文按「一条弃用中的旧路径」对待：不推荐新用户使用，仅在需要 Add-ons 又要宿主控制权时作过渡。读本章的目的是理解原理与迁移，而不是获得推荐。

### 5.1 历史定位与 ADR-0014（已 revert）

**定义**：Supervised = 在你自己管理的 Linux 上，用安装器部署 Supervisor + Core，从而获得「完整 HA 组件（除 HAOS 之外）」[素材 §一.3]。它保留了宿主 OS 的控制权——apt、systemd、自定义服务都可以继续用——同时拥有 HAOS 才有的 Supervisor 与 Add-on 商店。正因如此，历史上官方定位是 **「only for advanced users」**，要求精通 Linux / Docker / 网络，维护难度列为 Expert [素材 §一.3]。

**ADR-0014 与 revert**：Supervised 的官方支持曾由一份架构决策记录（ADR）正式定义，编号 ADR-0014。但该 ADR 状态已标记 **reverted（已撤销）**，官方不再承认 Supervised 是受支持的安装方式 [素材 §一.3]。网上大量 Supervised 教程写于 ADR 有效期内，内容基于这份已撤销的正式支持——阅读这类教程前，先给它打个问号。

官方定位的演进脉络：

| 阶段 | 官方态度 |
|------|---------|
| ADR-0014 有效期 | 正式支持；「only for advanced users」 |
| ADR-0014 revert 后 | 不再列为正式安装方式 |
| 2025-05-22 起 | 公告弃用，进入倒计时 |
| 2025.12 起 | 官方支持终止 |

> [!warning] 过时教程警告
> 2025 年后仍宣称 Supervised「官方支持」的教程，基本都基于已 revert 的 ADR-0014 或更早材料。先核实发布日期，再决定是否采信。

### 5.2 官方支持约束（历史定义）

Supervised 的「全功能」代价，是一长串对宿主系统的硬性要求。这些约束是官方支持的前提条件（即 ADR 有效期内，满足才算「受支持」）；如今虽然已弃用，理解它们仍是判断「自己装不装得起来」的关键。

#### 宿主 OS：仅 Debian 12，无衍生版

官方唯一支持的宿主操作系统是 **Debian 12 Bookworm**，且**不接受任何衍生版**——Raspberry Pi OS、Ubuntu 等都会被安装器直接拦截 [素材 §一.3]。注意这是硬性检查，不是「强烈建议」：树莓派用户想跑 Supervised，必须先刷纯 Debian 12，而不是常见的 Raspberry Pi OS，否则安装器第一步就过不去。

#### 依赖清单

| 依赖 | 最低版本 |
|------|---------|
| Docker CE | ≥ 20.10.17 |
| systemd | ≥ 239 |
| NetworkManager | ≥ 1.14.6 |
| udisks2 | ≥ 2.8 |
| AppArmor | 内核启用 |
| cgroup | v1 |
| 文件系统 | overlayfs2 |
| journald | systemd 自带 |

这张表本质上是「Supervisor 在宿主上运行的运行时环境」：Docker 提供容器、systemd 管理服务、NetworkManager 处理网络（HA 的网络管理依赖它）、udisks2 负责磁盘与 USB 存储、AppArmor 做容器安全、cgroup v1 是 Supervisor 容器资源控制的必需版本、overlayfs2 是 Docker 存储驱动。

#### 宿主必须「专用于 HA」

比依赖清单更苛刻的是一条隐含约束：**宿主必须专用于 HA，不得安装额外软件**。因为几乎任何对系统状态的改动，都可能让 Supervised 的自检从 Healthy 变成 Unsupported / Unhealthy [素材 §一.3]。这带来一个反直觉的结论：Supervised 虽然跑在你的 Linux 上，但你想在它旁边装别的服务，恰恰是最容易触发 Unsupported 的行为之一。

### 5.3 安装原理与脚本步骤

官方曾维护安装脚本仓库 `supervised-installer`，负责把一套 Debian 12 系统变成 Supervised 宿主。安装分四步 [素材 §一.3]：

```bash
# 1. 安装 network-manager + systemd-resolved
#    注意：这一步会切换网络服务，宿主的 IP 可能变化
apt install network-manager systemd-resolved

# 2. 安装 curl、udisks2，并安装 Docker CE
apt install curl udisks2
curl -fsSL get.docker.com | sh

# 3. 安装 OS-Agent（Supervisor 与宿主通信的守护进程）
#    从 GitHub releases 下载 os-agent_*_linux_*.deb
dpkg -i os-agent_*_linux_*.deb

# 4. 下载并安装 homeassistant-supervised.deb（核心包）
#    装完即部署 Supervisor + Core，并注册为 systemd 服务
dpkg -i homeassistant-supervised.deb
```

四步各司其职：

| 步骤 | 装了什么 | 为什么需要 |
|------|---------|-----------|
| 1 | network-manager + systemd-resolved | Supervisor 接管网络配置，两者必须存在；切换服务时 IP 可能变化 |
| 2 | curl、udisks2、Docker CE | Docker 是 Supervisor 的容器运行时；udisks2 负责磁盘 / USB 管理 |
| 3 | OS-Agent | 宿主机与 Supervisor 之间通信的守护进程，负责上报系统状态 |
| 4 | homeassistant-supervised.deb | 主安装包，部署 Supervisor + Core 并注册为 systemd 服务 |

两个补充细节：

- **数据目录**：默认 `/var/lib/homeassistant`，可用环境变量 `DATA_SHARE` 自定义 [素材 §一.3]。
- **支持机型**：列表有限——generic-x86-64、qemux86-64、qemuarm-64、odroid-c2 / c4 / n2、khadas-vim3、raspberrypi3-64 / 4-64 / 5-64 等 [素材 §一.3]。注意树莓派条目只认 64 位，且必须跑纯 Debian。

> [!warning] 弃用后的安装器
> `supervised-installer` 仓库顶部已标注「unsupported with HA OS 2025.12.0」——即该安装器对 2025.12 之后的 HA 版本不再提供支持 [素材 §二]。照抄上面命令之前，先确认你接受「无人维护」的现实。

### 5.4 弃用时间线与现状

官方对 Supervised（连同 Core、32 位系统）的弃用，有一条清晰的时间线 [素材 §二]：

| 时间 | 事件 |
|------|------|
| 2025-05-22 | 官方公告弃用 Core、Supervised 安装方式及 32 位系统 |
| 2025.6 版本起 | 受影响系统更新后显示「支持将在六个月后结束」通知 |
| 2025.12 版本 | **官方支持终止**；supervised-installer 同步标注 unsupported |

弃用之后，Supervised 仍可继续使用和更新，但官方不再接受问题报告、并移除了端用户文档。换句话说：用下去没人拦你，但出了 bug 官方不会管，连官方排障指南都没了。

官方公告里用使用率数据解释了清理动因 [素材 §二]：

| 安装方式 | 使用率 |
|---------|--------|
| Core | 约 2.5% |
| Supervised | 约 3.3% |
| i386 / armhf | < 0.5% |
| armv7 | 约 0.95%（其中过半实际支持 64 位） |

Supervised 约 3.3% 的使用率，叠加宿主约束带来的高维护成本，让官方认为不值得持续投入维护资源。

### 5.5 社区立场与 BYPASS_OS_CHECK 风险

#### 社区共识：「less supported (and liked)」

早在弃用之前，社区对 Supervised 的评价就是 **「less supported (and liked)」**——处于受支持边缘地带，选它等于自负维护责任 [素材 §二]。弃用公告之后这个立场更明确：多数老用户的实际选择是「Proxmox 上跑 HAOS VM，杂项服务用独立 LXC/VM 跑，不塞进 HA」[素材 §二]。社区并不是讨厌 Supervised 的功能，而是厌倦了它与宿主系统之间脆弱的耦合。

#### BYPASS_OS_CHECK：社区流传，官方不背书

Supervised 的安装器会做宿主 OS 检查（非 Debian 12 / 衍生版直接拦截）。社区流传一种绕过方式：设置环境变量 **BYPASS_OS_CHECK**，跳过检查把包强装上去。关于它，必须把话说清楚：

> [!warning] 不要臆造细节，也不要指望官方兜底
> BYPASS_OS_CHECK 的记载主要来自社区指南，**官方文档不背书、不保证、不负责** [素材 §五]。目前能确认的事实只有两点：一是这个变量确实被社区多次提及；二是即使绕过成功，系统也几乎必然被判 Unsupported / Unhealthy，官方支持随之失效。至于它在某个具体版本怎么生效、会不会被新版本移除，**没有官方口径**——任何声称「详细教程」的帖子都应视为社区经验，需自行验证。

换句话说：BYPASS_OS_CHECK 不是「解锁官方支持的钥匙」，恰恰相反，它是「主动放弃官方支持」的按钮。

### 5.6 优点 / 缺点 / 适用场景

| 维度 | 结论 |
|------|------|
| 优点 | 兼具 Add-on 商店与宿主 OS 控制权；Thread / Z-Wave 可用（由 Add-on 提供） |
| 缺点 | 安装繁琐；维护成本高（Expert）；易被判 Unsupported / Unhealthy；仅支持纯 Debian 12；已弃用（2025.12 终止） |
| 适用 | 基本不推荐新用户；仅在需要 Add-ons 又要宿主控制权时作过渡 |

理论上，Supervised 是「功能完整性」与「灵活性」两条权衡轴上的理想折中：它有 HAOS 的 Supervisor / Add-on / Thread / Z-Wave，又有 Container 那样的宿主控制权。但它的成立前提——宿主必须专用于 HA、仅支持纯 Debian、任何改动都可能触发 Unsupported——让这个折中名存实亡：真把宿主「专用」了，与独占一台 HAOS 没有本质区别；真在共享宿主上跑，又必然触碰 Unsupported 红线 [素材 §三]。

> [!tip] 一句话判断
> 需要 Add-on 生态，选 HAOS（第三章）；需要宿主控制权且愿意手动维护，选 Container（第四章）。Supervised 夹在中间两头都想要，却两头都难做好——而且已经失去官方支持。

### 本章小结

- Supervised = 在完整 Linux 上装 Supervisor + Core；曾由 ADR-0014 定义官方支持，现已 revert。
- 官方约束极严：仅纯 Debian 12、依赖清单长、宿主必须专用，否则易被判 Unsupported / Unhealthy。
- 安装器四步：network-manager + systemd-resolved → Docker CE / curl / udisks2 → OS-Agent → dpkg -i homeassistant-supervised.deb。
- 弃用时间线：2025-05-22 公告 → 2025.6 六个月倒计时通知 → 2025.12 官方支持终止；使用率仅约 3.3%。
- BYPASS_OS_CHECK 是社区流传、官方不背书的绕过手段，强装必然 Unsupported，不构成推荐理由。

---

*接下来：第六章把三种部署方式浓缩成一张选型决策树，按硬件条件与维护偏好一步步走到推荐答案，并给出不推荐组合清单。*

## 第六章：选型决策树与建议

前五章把 HAOS、Docker Container、Supervised 各自的特性、维护方式和适用场景都拆开了，但「知道区别」和「做出选择」之间还差一步：当三者的信息同时摆在面前，该按什么顺序问自己问题、哪些组合其实是陷阱？这一章把前面拆散的信息收拢成一张完整的决策树，配合典型用户画像与不推荐组合，最后落到三条权衡原则，帮你得到一个可执行的选型答案。

### 6.1 决策树（完整版）

选型不是选「最好的方式」，而是选「最适合你的方式」。先把问题按重要性排序：省心程度 > 资源约束 > 特殊需求。下面是完整决策树 [素材 §四]：

```text
开始：先想清楚你更在意「省心的功能完整」还是「灵活的控制权」

┌─ 主线一：想省心、功能完整，愿意让一台设备专职跑 HA？
│   ├─ 是 → HAOS
│   │       ├─ 已有 Proxmox / VMware / VirtualBox 等平台 → HAOS 虚拟机（社区主流）
│   │       ├─ 有闲置专用硬件（树莓派 / 工控机 / NUC）   → HAOS 直接刷机
│   │       └─ 都没有 → 专门为 HA 开一台 VM，跑 HAOS
│   └─ 否 → 进入主线二
│
├─ 主线二：已有一台常开的 Docker 主机（NAS / VPS），想与其他服务共存？
│   ├─ 是 → Docker Container（只跑 Core）
│   │       ├─ 需要 Add-on / Thread / Z-Wave？→ 此路没有这些，回到主线一
│   │       └─ 能接受手动备份 / 反代 / 更新  → 就是它
│   └─ 否 → 进入主线三
│
└─ 主线三：必须保留 Add-on，又坚持要宿主的系统控制权？
    ├─ 是 → 谨慎评估 Supervised（官方已弃用）
    │       ⚠️ 仅支持 Debian 12 无衍生版、宿主须专机专用、易被标 Unsupported
    │       → 现实最优解：Proxmox 里跑 HAOS VM，宿主控制权交给物理机
    └─ 否 → 默认回到主线一 → HAOS
```

#### 主线一：省心与功能完整优先 → HAOS

这一支的回答是「愿意为 HA 专门准备一台设备（物理机或 VM）」。得到的是最完整的体验：Add-on 商店、Thread / Z-Wave 开箱支持、自动更新、托管快照备份，全由 Supervisor 包办 [素材 §一.1]。剩下的分叉只取决于你手头有什么：有虚拟化平台就建 HAOS VM，有闲置硬件就刷机，两者都没有就为 HA 开一台 VM——VM 的好处是以后还能用宿主机的快照做整机备份（第三章 3.5 节）。

#### 主线二：已有 Docker 主机 → Container

如果你的 NAS / VPS 上已经跑着其他容器，不想再开一台设备，Container 是唯一让 HA 与其他服务共存的方式 [素材 §一.2]。代价是功能减配：无 Add-on、无自动更新、无托管备份，Thread / Z-Wave 开箱不支持。走这条线的前提是你能接受「自己维护」——定期备份 /config、手动拉镜像更新、自己配反代。

#### 主线三：Add-on 与宿主控制权都要 → 谨慎评估 Supervised

这是决策树里唯一的「陷阱分支」。Supervised 曾在完整 Linux 上同时提供 Add-on 与宿主控制权，但它已被官方弃用（2025.12 终止支持）、仅支持 Debian 12 无衍生版、宿主稍有改动就易被判 Unsupported/Unhealthy [素材 §一.3]。如果你确实两者都要，社区的现实解法不是硬上 Supervised，而是在 Proxmox 等虚拟化平台上跑 HAOS VM——把「宿主系统控制权」放在 HAOS 所在 VM 的物理机层面，HA 内部仍享受完整的 Add-on 生态 [素材 §二]。

> [!warning] 决策树的关键提醒
> 三条主线不是并列的「三选一」，而是有优先级的漏斗：**先问能否接受独占设备，再问是否有 Docker 主机，最后才轮到 Supervised**。绝大多数人会落在主线一或主线二。

### 6.2 典型用户画像建议

| 用户画像 | 推荐方式 | 一句话理由 |
|---------|---------|-----------|
| NAS / 已有 Docker 主机的用户 | Container | 复用现有资源、空闲仅约 300-400MB、可共存 [素材 §一.2] |
| 有 Proxmox / VMware 环境的用户 | HAOS VM | 社区主流做法，功能完整 + 虚拟化快照 / 迁移优势 [素材 §二] |
| 有专用硬件（树莓派 / 工控机 / NUC） | HAOS 刷机 | 刷完即用、零维护，硬件物尽其用 |
| 只想零维护跑 HA 的用户 | HAOS VM | 全托管，自动更新 + 一键备份，无需 Docker 技能 |
| 老 Supervised 用户 | 迁移到 HAOS / Container | 官方支持已终止，需主动迁移（第七章详述） |

逐类展开：

- **NAS / 已有 Docker 主机的用户** → Container。群晖、威联通或自建 NAS 上通常已经跑着大量容器，HA 作为其中一个即可。Core 空闲占用约 300-400MB，几乎无感 [素材 §一.2]。前提是你已经具备 Docker 操作习惯，愿意手动处理备份与更新。
- **有 Proxmox / VMware 环境的用户** → HAOS VM。这是社区老用户的主流做法：在虚拟化平台里给 HA 一个专用 VM，其他杂项服务放独立的 LXC / VM，不塞进 HA [素材 §二]。既享受 HAOS 的功能完整，又用 VM 隔离性保住宿主机的可控性。
- **有专用硬件的用户** → HAOS 直接刷机。闲置树莓派 4/5、工控机或 NUC 直接刷 HAOS 镜像，开机即用。适合不想折腾虚拟化、有一台设备愿意专职跑 HA 的人。
- **只想零维护跑 HA 的用户** → HAOS VM。不论硬件从哪来，只要目标是「装上就不管」，HAOS 的全托管就是最短路径。
- **老 Supervised 用户** → 尽快规划迁移。Supervised 官方支持已于 2025.12 终止，弃用后仍可继续使用与更新，但官方不再接受问题报告 [素材 §二]。目标状态：需要宿主控制权就迁到 Proxmox 上的 HAOS VM，否则迁到 Container（第七章给完整路径）。

### 6.3 不推荐的组合与原因

三种典型「看上去合理、实际踩坑」的组合：

| 组合 | 为什么不推荐 |
|------|-------------|
| 新用户直接上 Supervised | 已弃用、仅支持 Debian 12、维护难度 Expert，新手极易在安装与合规上耗尽耐心 [素材 §一.3] |
| 在共享宿主上跑 Supervised | Supervisor 要求宿主「专用于 HA」，共享宿主上几乎必然被判 Unsupported/Unhealthy [素材 §一.3] |
| 要 Add-on / Thread / Z-Wave 却选 Container | Container 没有 Supervisor，这些功能开箱不支持，选了就是功能缺失 [素材 §一.2] |

逐个说明：

- **新用户直接上 Supervised**。Supervised 的定位一直是「only for advanced users」，现在更是官方弃用状态 [素材 §一.3]。新用户没有 Docker / Linux 排障经验，在安装（纯 Debian、依赖清单）、维护（宿主改动即 Unsupported）、更新（Supervisor 已停更）三个环节都会受挫。新用户的两个正确答案是 HAOS（要省心）或 Container（要共存），没有第三个。
- **在共享宿主上跑 Supervised**。Supervised 的宿主约束非常严格：必须专用于 HA，不得安装额外软件 [素材 §一.3]。你不可能在一台既跑 Plex 又跑 NAS 服务的机器上装 Supervised 还保持 Supported 状态。如果你的目标是「和其他服务共存」，Container 才是为此设计的。
- **要 Add-on / Thread / Z-Wave 却选 Container**。这是最常见的「功能预期错配」。Add-on 商店、Thread、Z-Wave 都是 Supervisor 层提供的，Container 只有裸 Core，这些开箱不支持 [素材 §一.2]。想要这些能力，选 HAOS；能放弃这些能力，才轮到 Container。

> [!tip] 反推选型法
> 与其正向背决策树，不如反向排除：先问「我绝对不能失去什么」。如果答案是 Add-on 生态 → 排除 Container；如果答案是宿主共存 → 排除 HAOS；如果两者都要 → 排除 Supervised，改用「物理机 + HAOS VM」的组合。

### 6.4 决策背后的权衡原则

前面所有建议，底层都是三条权衡原则在起作用。理解它们，才能在遇到「画像没覆盖到的情况」时自己推答案。

#### 功能完整性 ↔ 灵活可控

这是最核心的一条轴 [素材 §二]。HAOS 站在功能完整一端：Add-on 生态、自动更新、托管备份全部内置，代价是系统只读、独占整机、不可自由扩展。Container 站在灵活可控一端：宿主是你的、想跑什么跑什么，代价是 HA 的功能要靠自己一点点补齐。**没有「既完整又灵活」的免费午餐**——Supervised 曾经试图兼得，结果是在宿主约束和弃用状态中两边都不讨好。

#### 省心程度 ↔ 资源占用

第二条轴是运维成本与硬件成本的交换。HAOS 用约 4GB 内存换「装上就不管」，Container 用约 300-400MB 内存换「样样自己来」 [素材 §二]。注意这条轴不是「越省心越好」：如果你的宿主资源紧张，省心的代价可能反过来变成性能瓶颈；如果你的时间紧张，省内存的代价可能变成每周一次的维护负担。选型的本质是**拿你富余的资源，换你稀缺的资源**——富余的是硬件，就换省心；富余的是时间，就换轻量。

#### 官方支持生命周期

第三条原则最容易被忽略，但对长期选择影响最大。官方对安装方式的支持会随时间变化：ADR-0014 被 revert、Supervised / Core 在 2025.12 终止支持，都是活生生的例子 [素材 §二]。**选择时应优先落在官方正式路径内**（HAOS / Container），因为弃用状态意味着：不再有问题修复、端用户文档移除、社区与生态逐渐离心。反过来，当官方文档说某条路「recommended」时，选它的长期风险最低。

> [!summary] 三条原则合起来看
> 功能完整与灵活可控不可兼得；省心与轻量不可兼得；而「官方是否长期支持」决定了前两条权衡是否值得下注。落点：默认 HAOS，除非你有明确的共存需求 → Container；Supervised 只作为理解历史与迁移的参照。

### 本章小结

- 决策树是有优先级的漏斗：先问能否接受独占设备（→HAOS），再问是否有 Docker 主机（→Container），最后才评估 Supervised（默认不选）。
- 典型画像：NAS / Docker 用户 → Container；Proxmox / VMware 用户 → HAOS VM；专用硬件 → 刷机；零维护需求 → HAOS VM；老 Supervised 用户 → 主动迁移。
- 三大不推荐组合：新用户直接 Supervised、共享宿主跑 Supervised、要 Add-on 却选 Container。
- 三条权衡原则：功能完整 ↔ 灵活可控、省心 ↔ 资源占用、官方支持生命周期决定长期风险。
- 核心落点：默认 HAOS；有共存需求再考虑 Container；Supervised 作为弃用旧路径仅作参考。

---

*接下来：第七章讲官方迁移三步走（备份 → 下载 → 初始化时恢复）、各路径迁移详解与跨架构恢复注意事项，帮助从旧方式迁移过来。*

## 第七章：迁移路径与操作

第六章帮你做出了部署方式选型，但如果你已经跑着一套 Home Assistant，换方式不是「删掉重装」，而是一次有讲究的迁移。官方给出的原则出奇地简单——备份、下载、在新系统初始化时恢复。这一章把这条官方原则落到每条迁移路径上，讲清 Core→Container、Supervised→HAOS、32 位→64 位分别怎么走，以及跨架构迁移的可行性边界和迁移前后的注意事项。

### 7.1 官方迁移原则

官方对「换系统」这件事的定义非常轻量：

> "Switching systems is as easy as making a backup, downloading it, and restoring it during the initialization of your new system."
> —— Home Assistant 官方文档 [素材 §二]

翻译成操作就是三步：

1. **备份（making a backup）**：在旧系统上做一份完整快照备份。HAOS 用 Supervisor 的托管快照，Container 则需手动备份 /config。
2. **下载（downloading it）**：把备份文件下载到本地或上传云端，供新系统使用。
3. **初始化时恢复（restoring it during the initialization）**：装好新系统后，在首次初始化向导里选择「从备份恢复」，而不是登录后再手动导入。

关键在第三步：**恢复动作发生在初始化阶段**。新系统第一次引导时，向导会让你选择「全新初始化」还是「从备份恢复」，选后者并上传备份文件即可，后续配置、集成、Add-on 会一并还原。

> [!note] 迁移的本质
> 迁移 ≠ 复制文件。官方把换系统简化为「备份 → 下载 → 初始化时恢复」三件事，意味着你的全部状态（配置、数据库、集成、Add-on）都被封装在备份里，新系统只需在初始化时解包一次。

### 7.2 各路径迁移详解

官方根据迁移起点不同给出了三条推荐路径 [素材 §二]：

| 迁移起点 | 官方推荐去向 | 适合的场景 |
|---------|------------|-----------|
| Core（Container） | Container（独占设备则 HAOS） | 已有 Docker 主机继续容器化；想零维护则转 HAOS |
| Supervised | HAOS（可在 Proxmox 等 VM 里跑，或用 Container） | 需要宿主控制权 → VM 里跑 HAOS；能接受无 Add-on → Container |
| 32 位设备 | 装 64 位系统后恢复备份 | 想保留旧硬件 |

#### Core 用户：首选 Container，独占设备则 HAOS

Core 用户本就在自己管理的 Linux 上跑，官方首选目标是换用官方 Container 方式——本质是「同一套 Core，换成官方 compose 模板」。迁移时把原 /config 目录接回新容器即可，配置与数据基本原样可用 [素材 §二]。

如果你愿意为 HA 独占一台设备、想要零维护体验，则直接上 HAOS：新系统初始化时恢复备份即可。

#### Supervised 用户：推荐 HAOS，需要宿主控制权则 VM 里跑

Supervised 已弃用（2025.12 终止官方支持），官方推荐迁移到 HAOS [素材 §二]。当年选 Supervised 多半是为了「既要有 Add-on 又要宿主控制权」，这两个诉求在 HAOS VM 上都能保留：

- **想要宿主控制权** → 在 Proxmox 等虚拟化平台上跑 HAOS VM（见 3.5 节），宿主控制权收敛到虚拟化层，HA 内部仍是全托管的 HAOS；
- **能接受无 Add-on** → 改用 Container，但会失去 Add-on 商店与 Thread / Z-Wave 开箱支持。

#### 32 位设备：重装 64 位系统，恢复备份保留硬件

32 位系统与 Core、Supervised 一同于 2025.12 被终止支持 [素材 §二]。若硬件本身是 64 位 CPU、只是系统装成了 32 位，官方路径是：**重装 64 位系统 → 在初始化时恢复备份**，硬件无需更换。

### 7.3 跨架构迁移可行性

官方明确：**备份可以在任意安装方式之间、甚至跨架构恢复** [素材 §二]。换句话说，x86 的 HAOS 备份恢复到 ARM 的树莓派上，或 Container 的备份恢复到 HAOS 上，都是受支持的路径。

原因在于 HA 的备份是自包含归档，恢复时新系统会按当前架构重新解析并拉取对应架构的 Add-on 容器镜像。少数依赖原生二进制的自编译组件可能需要在新架构下重新构建，但常规配置、数据库与集成不受影响。

另外，**Home Assistant Cloud 订阅用户支持异地凭密码恢复** [素材 §二]：备份可上传到 HA Cloud，在新设备初始化时凭账号密码直接拉取，无需手动搬运文件——这对异地重建、换设备时格外省事。

> [!tip] 跨架构恢复的边界
> 官方保证的是「配置、数据库、集成」可跨架构恢复；个别 Add-on 或自定义组件若依赖特定架构的原生二进制，首次启动可能要重新拉取或重建。迁移后在设置里确认各 Add-on 均正常启动即可。

### 7.4 迁移注意事项

#### 备份完整性：不止 configuration.yaml

HAOS 的托管快照面向的是完整状态，会把配置、数据库、Add-on 及其配置、设备集成一并封装，而不仅是单个配置文件 [素材 §一.1]。迁移前请确认：

- 快照备份**完整成功**，包含 Add-on 与设备集成，而不是只导出了 configuration.yaml；
- Container 用户无托管快照，务必连同 /config 下的数据库、custom_components 一起备份；
- 有条件时先做一次「备份可恢复性」验证，避免迁移中途才发现备份损坏。

#### 迁移后验证硬件直通

恢复只是第一步，硬件接入需要在新环境重新确认 [素材 §一.1][素材 §一.2]：

| 硬件 | 验证要点 |
|------|---------|
| USB / Zigbee / Z-Wave | 适配器是否被识别。HAOS VM 需配置 USB 直通（Proxmox 上 `qm set <VMID> -usb0 host=10c4:ea60`）；Container 需在 `devices` 中映射 `/dev/ttyUSB0`。对应集成应显示设备在线 |
| 蓝牙 | Container 依赖 `/run/dbus` 挂载、HAOS 由 Supervisor 托管。验证蓝牙集成能发现并控制设备 |
| 网络 / mDNS | 新系统接入同一网段后，设备自动发现是否恢复（依赖 host 网络 / 同网段广播） |

```bash
# 以 Proxmox 上的 HAOS VM 为例，确认 USB 直通已配置
qm set <VMID> -usb0 host=10c4:ea60   # 先停 VM，用 lsusb 查 vendor:product
qm stop <VMID> && qm start <VMID>
```

#### 并行期数据一致性

新旧系统并行的窗口期内，要防止两个实例写同一份数据：

- **同一时间只让一个实例接管**。HA 的数据库与设备状态由单一实例维护，迁移完成后旧系统应尽快停用，避免两套系统同时连接同一设备，导致自动化重复触发或状态互踩。
- **正式切换前做最后一次备份**。从首次备份到正式切换之间新增的配置，用切换前的最终备份兜底，避免丢失最后一段改动。

### 本章小结

- 官方迁移原则：备份 → 下载 → 初始化时恢复，恢复动作发生在新系统首次初始化向导。
- Core 用户首选 Container，独占设备则 HAOS；Supervised 用户推荐 HAOS，需要宿主控制权就在 VM 里跑。
- 32 位设备：重装 64 位系统后恢复备份即可保留硬件。
- 备份可在任意安装方式之间、甚至跨架构恢复；HA Cloud 订阅用户可凭密码异地恢复。
- 迁移前验证备份完整性（含 Add-on 与设备集成），迁移后验证 USB / Zigbee / 蓝牙直通，并行期保持单实例接管。

---

*接下来：第八章（附录）是实操收尾——Docker Compose 完整模板、Proxmox 部署 HAOS VM、HAOS 直接刷机与 Supervised 安装脚本（附弃用警告）、初始化引导与备份恢复，迁移部署所需的每条命令都可直接复制使用。*

## 第八章（附录）：部署实操步骤

前三章把 HAOS、Container、Supervised 的机制和取舍讲透了，但「知道怎么选」和「真能部署起来」之间还差一步。这一章把全文涉及的可复制命令集中成一份实操附录：Docker Compose 完整模板与启停、Proxmox 部署 HAOS VM 全流程、专用硬件直接刷机概述、Supervised 旧安装脚本（存档）以及首次初始化与备份恢复。命令按「复制 → 替换占位符 → 运行」组织，供你部署时逐节查阅。

> [!note] 使用前提
> 本章是实操参考，不是选型指南。选型逻辑看第一、二、六章；三种方式的机制拆解看第三、四、五章。命令中的占位符（如 `<VMID>`、`<STORAGE>`、`/PATH_TO_YOUR_CONFIG`）必须替换为你环境里的真实值。

### 8.1 Docker Compose 完整模板与启动

适用 Container 方式（第四章）。前提：一台 Linux 主机或 NAS，Docker Engine ≥ 23.0.0；Docker Desktop 不可用 [素材 §一.2]。

#### 完整 compose 模板（官方原样）

把下面内容保存为 `docker-compose.yml`，其中蓝牙挂载、时区、USB 直通、特权模式都已包含 [素材 §一.2]：

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /PATH_TO_YOUR_CONFIG:/config
      - /etc/localtime:/etc/localtime:ro
      - /run/dbus:/run/dbus:ro      # 蓝牙集成必需
    restart: unless-stopped
    privileged: true
    network_mode: host
    environment:
      TZ: Europe/Amsterdam          # 必须是 tz database 名称
    devices:                        # USB 直通 Zigbee/Z-Wave
      - /dev/ttyUSB0:/dev/ttyUSB0
```

部署前替换三处：

| 占位符 | 替换为 | 说明 |
|------|--------|------|
| `/PATH_TO_YOUR_CONFIG` | 宿主上存放 HA 配置的绝对路径 | `/config` 内是 configuration.yaml、数据库、custom_components 等全部数据 |
| `Europe/Amsterdam` | 你的 tz database 时区（如 `Asia/Shanghai`） | 不能写 `UTC+8` 这种偏移写法 |
| `/dev/ttyUSB0` | 你的 Zigbee / Z-Wave 适配器设备路径 | 可先用 `lsusb` 确认 |

模板没有 `ports:` 段，因为 `network_mode: host` 直接共享宿主网络，8123 端口已经暴露在宿主所有网卡上，而 mDNS / 蓝牙发现也依赖这个模式，不要擅自改成 bridge [素材 §一.2]。

#### 启动、状态与日志

```bash
docker compose up -d          # 首次启动 / 按模板创建容器
docker compose ps             # 查看容器状态是否为 Up
docker logs -f homeassistant  # 跟随日志，直到出现初始化就绪
docker compose stop           # 停止容器（配置保留）
docker compose down           # 停止并删除容器（/config 数据仍在）
```

首次启动后浏览器访问 `http://<宿主IP>:8123`，进入初始化向导（见 8.5）。

#### 防火墙放行

Ubuntu 的 ufw 默认拦截入站端口，外部访问不了时先放行 [素材 §一.2]：

```bash
sudo ufw allow 8123/tcp
```

#### 升级与回滚

Container 没有 OTA，升级 = 拉新镜像 + 重建容器，`/config` 挂载数据不受影响 [素材 §一.2]。compose 方式：

```bash
docker compose pull
docker compose up -d
```

纯 `docker run` 方式则先拉新镜像、删旧容器、再用与首次启动完全相同的参数重新 run（参数见第四章 4.3 方式 B）。

> [!tip] 回滚
> 新版翻车时，把镜像 tag 指回上一个可用版本（如 `2025.7.4`），再走一遍重建流程即可。HA 配置文件向后兼容，回滚不丢 /config 数据。

### 8.2 Proxmox 部署 HAOS VM 完整步骤

适用场景：有 Proxmox 环境，想用社区主流的「HAOS VM」方式。q35 / UEFI / virtio-scsi-pci 等参数的含义见第三章 3.5。

#### 方式 A：一键脚本（推荐）

社区脚本自动完成「下载镜像 → 建 VM → 导入磁盘 → 配 UEFI」，直接运行 [素材 §一.1]：

```bash
bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
```

#### 方式 B：手动（下载 → 解压 → 导入 → 创建 VM）

手动流程需要先建一台空 VM，再把磁盘镜像导入并设为启动盘。以下命令把 3.5 节的社区推荐配置翻译成 `qm` CLI，占位符按实际环境替换（`<VMID>` 是 VM 编号，`<STORAGE>` 是 Proxmox 存储名，如 `local-lvm`）：

```bash
# 1) 下载 HAOS 镜像（qcow2 对应 KVM/Proxmox，官方命名 haos_ova-{version}，需解压）
wget <OFFICIAL_RELEASE_URL>/haos_ova-<VERSION>.qcow2.xz

# 2) 解压（.qcow2.xz 是压缩包，必须解压后才能导入）
xz -d haos_ova-<VERSION>.qcow2.xz

# 3) 创建空 VM：q35 机型 + OVMF(UEFI) + EFI 盘 + virtio-scsi-pci + 社区推荐资源
qm create <VMID> --name haos --machine q35 --bios ovmf \
  --efidisk0 <STORAGE>:4,efitype=4m,pre-enrolled-keys=0 \
  --scsihw virtio-scsi-pci --cpu cputype=host \
  --cores 2 --memory 4096 --balloon 2048 \
  --net0 virtio,bridge=vmbr0 --ostype l26

# 4) 导入磁盘并设为启动盘
qm importdisk <VMID> haos_ova-<VERSION>.qcow2 <STORAGE>
qm set <VMID> --scsi0 <STORAGE>:<导入后生成的卷ID> --boot order=scsi0

# 5) 启动
qm start <VMID>
```

> [!note] 手动流程说明
> 第 3 步的 `qm create` 参数是对素材 §一.1「Proxmox 推荐配置」表（q35 / UEFI / virtio-scsi-pci / kvm64·host / 4096MB+balloon / vmbr0）的直接翻译；`qm importdisk` 是 Proxmox 导入磁盘的标准命令。`--cpu cputype=host` 性能最好但不可跨节点迁移，需要迁移改为 `cputype=kvm64` [素材 §一.1]。

启动后浏览器访问 `http://homeassistant.local:8123`，进入 8.5 的初始化。

#### USB 直通（Zigbee / Z-Wave / 蓝牙适配器）

```bash
# 先 stop VM，用 lsusb 查 vendor:product，再直通
qm set <VMID> -usb0 host=10c4:ea60
qm stop <VMID> && qm start <VMID>
```

> [!warning] 必须先停机再挂 USB
> USB 直通要求在 VM **停止**状态下执行 `qm set`，否则设备可能无法正确枚举；直通后重启 VM 才生效。Zigbee / Z-Wave 协调器必须被 HAOS VM 独占访问 [素材 §一.1]。

> [!warning] 不要在 Proxmox 侧「升级」HAOS
> HAOS 是家电式只读系统，OS / 内核 / Supervisor 的升级由 HA 设置里的 Supervisor 自动 OTA 完成（约每 8 小时检查一次）[素材 §一.1]。从宿主机侧强行升级镜像或改引导配置可能破坏系统；日常升级一律在 HA 的「设置 → 系统 → 更新」里进行。

#### 快照备份

```bash
# snapshot 模式：VM 运行时也能做一致性备份；zstd 压缩显著减小体积
vzdump <VMID> --mode snapshot --compress zstd --storage local
```

配合 Supervisor 的 HA 配置快照，形成「宿主机整机备份 + HA 配置快照」双保险。

#### 扩容磁盘

```bash
qm resize <VMID> scsi0 +32G
```

扩容后重启 VM，HAOS 系统内会自动识别并扩大分区。

### 8.3 HAOS 直接刷机简述（专用硬件）

如果你有一台专用硬件（树莓派、x86 工控机、NUC 等），可以不走虚拟机，直接把 HAOS 镜像烧写到 SD 卡或 eMMC。HAOS 镜像按硬件架构分平台提供，下载后写入介质、插到机器上开机即可 [素材 §一.1]。

烧写属于通用镜像烧写流程：用常见的镜像写入工具（如 BalenaEtcher、Raspberry Pi Imager）把下载的 HAOS 镜像写到目标介质即可，不需要额外配置分区。写入时注意目标盘会被整个覆盖，别选错盘。

首次引导后与虚拟机方式完全一致：机器启动后浏览器访问 `http://homeassistant.local:8123`，进入 8.5 的初始化向导。第三章 3.3 的虚拟机部署要求（2GB / 2vCPU / 32GB、UEFI 等）主要针对虚拟机场景；专用硬件按官方为该硬件提供的镜像直接刷即可。

### 8.4 HA Supervised 安装脚本（附弃用警告）

> [!warning] 该方式已于 2025.12 终止官方支持
> 官方于 2025-05-22 公告弃用 Core 与 Supervised，2025.12 版本起官方支持终止 [素材 §二]。以下步骤仅存档参考：官方不再接受问题报告、端用户文档已移除。**新部署请走 HAOS 或 Container**。

Supervised 的安装脚本来自 `supervised-installer` 仓库，核心是四步 [素材 §一.3]：

```bash
# 1. 安装 network-manager + systemd-resolved（会切换网络服务，IP 可能变化）
# 2. 安装 curl、udisks2，并用官方脚本安装 Docker CE
curl -fsSL get.docker.com | sh
# 3. 安装 OS-Agent（os-agent_*_linux_*.deb，从 supervised-installer 仓库获取）
# 4. 下载 homeassistant-supervised.deb 并安装
dpkg -i homeassistant-supervised.deb
```

安装约束（历史定义，务必知晓）：

| 约束 | 内容 |
|------|------|
| 唯一支持的宿主 OS | Debian 12 Bookworm，不接受任何衍生版（Raspberry Pi OS、Ubuntu 会被安装器拦截） |
| 关键依赖 | Docker CE ≥20.10.17、systemd ≥239、NetworkManager ≥1.14.6、udisks2 ≥2.8、AppArmor、cgroup v1、overlayfs2、journald |
| 宿主专用 | 必须「专用于 HA」，不得安装额外软件，否则易被判 Unsupported / Unhealthy |
| 数据目录 | 默认 `/var/lib/homeassistant`，可用 `DATA_SHARE` 自定义 |
| 支持机型 | generic-x86-64、qemux86-64、qemuarm-64、odroid-c2/c4/n2、khadas-vim3、raspberrypi3-64/4-64/5-64 |

> [!warning] 不要绕过 OS 检查
> 社区流传可用 `BYPASS_OS_CHECK` 环境变量绕过宿主 OS 校验，但会导致 Unsupported / Unhealthy 状态。此为社区流传信息，官方文档不背书，绕过后的问题官方不负责 [素材 §五]。

### 8.5 初始化引导与备份恢复

无论 HAOS VM、直接刷机还是（已弃用的）Supervised，首次启动后的入口都是同一个地址：

```
http://homeassistant.local:8123
```

打开后进入初始化向导：第一步创建本地账户（设置用户名、密码），第二步选择初始化方式，二选一：

| 初始化方式 | 操作 | 结果 |
|-----------|------|------|
| 全新初始化 | 创建账户后直接进入配置 | 从零添加集成、设备与自动化 |
| 从备份恢复 | 上传 Supervisor 快照文件（或从云备份恢复） | 一键还原配置、Add-on、集成状态 |

官方迁移原则原话是："Switching systems is as easy as making a backup, downloading it, and restoring it during the initialization of your new system" [素材 §二]。这句话对三条路径都成立：

- **跨安装方式**：任意方式之间（HAOS ↔ Container ↔ Supervised）都能通过「旧机做备份 → 新机初始化时恢复」迁移 [素材 §二]。
- **甚至跨架构**：32 位设备装 64 位系统后恢复备份，可保留硬件继续用 [素材 §二]。
- **异地恢复**：Home Assistant Cloud 订阅用户可凭密码异地恢复备份 [素材 §二]。

因此「从备份恢复」和「全新初始化」并不冲突：就算现在选了全新初始化，以后任何时候都可以用快照一键还原到某个历史状态。

### 本章小结

- 8.1：官方 compose 模板原样可用，蓝牙 / 时区 / USB 直通 / privileged 全在一份 yaml 里；升级 = `docker compose pull && up -d`，回滚 = 改 tag 重建。
- 8.2：Proxmox 部署 HAOS VM 首选一键脚本；手动流程 = 下载 → `xz -d` 解压 → `qm create`（q35 + OVMF + EFI 盘）→ `qm importdisk` → 启动；USB 直通必须先停 VM。
- 8.3：专用硬件直接刷机走通用镜像烧写工具，首次引导入口与虚拟机相同。
- 8.4：Supervised 四步安装脚本仅为存档，2025.12 已终止官方支持，新部署勿选。
- 8.5：所有路径统一从 `homeassistant.local:8123` 初始化，备份可在任意方式、任意架构间恢复。

到这里，三种部署方式「是什么、怎么选、怎么部署」的闭环已经完成：前七章负责判断，这一章负责落地。
