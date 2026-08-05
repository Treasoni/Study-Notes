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

<!-- CONTINUE -->
