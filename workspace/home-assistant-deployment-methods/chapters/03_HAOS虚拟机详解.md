# 第三章：HAOS 虚拟机详解

上一章的对比表里，HAOS 在功能完整度上几乎全面占优，但「官方推荐」到底是营销话术还是实打实的好处，需要落到它究竟怎么运行、怎么维护上来验证。这一章拆解 HAOS 的本质（嵌入式只读 OS）、官方推荐的理由、虚拟机部署的硬性要求、Supervisor 的托管机制，并给出社区在 Proxmox 上部署的推荐配置与可复制的命令，最后收束到优缺点与适用场景，帮你判断「独占一台机器」这个代价是否值得。

## 3.1 是什么：为 HA 定制的嵌入式操作系统

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

## 3.2 官方为什么推荐

官方文档把 HAOS 定义为 "recommended installation type for most users"，理由直接写成 "most convenient"（最省心）[素材 §一.1]。这不是空泛的评价，背后是三个具体能力：

1. **刷完即用**：镜像烧录或导入虚拟机后，首次开机进入引导页（`homeassistant.local:8123`），按向导创建账户、可选恢复备份即可，全程不需要碰命令行。
2. **全托管体验**：Supervisor 替你管理 Add-on 安装、快照备份、系统更新。你面对的是一个「电器」而不是「服务器」。
3. **自动更新链路**：Supervisor 约每 8 小时检查一次，可自动更新 OS 内核、Supervisor 自身以及 Core，无需手工介入 [素材 §一.1]。

把这三个能力放在一起看，官方推荐的逻辑就清晰了：HA 的用户画像里，绝大多数人想要的是「智能家居能一直稳定跑」，而不是「学会运维一套 Linux」。HAOS 把运维复杂度全部封装进 Supervisor，正是为了服务这个主流需求。对照第二章对比表中「维护难度：低」那一行，HAOS 是三种方式里唯一把更新、备份、扩展全部托管的。

需要再次强调：官方安装文档的正式分类里，只有 HAOS 和 Container 两条路径（第一章已详述）。HAOS 是其中「全功能 + 零维护」的一端，这也是它成为官方口中 most users 默认选择的原因。

## 3.3 虚拟机部署要求（官方）

HAOS 可以刷到专用硬件（树莓派、工控机等），也可以作为虚拟机运行在 Proxmox / VirtualBox / VMware / Hyper-V 上。官方给出了一套明确的虚拟机部署要求 [素材 §一.1]。

### 硬件最低要求

| 资源 | 最低 | 推荐 |
|------|------|------|
| 内存 | 2GB | 4GB |
| vCPU | 2 核 | 2+ 核 |
| 磁盘 | 32GB | 更大（含快照与备份缓冲） |

注意 32GB 只是最低磁盘，HA 的数据库、媒体、快照会持续增长，实际建议预留 40-64GB，并配合快照策略。

### UEFI：必须启用

HAOS 的引导要求 UEFI 固件，缺了它虚拟机无法启动 [素材 §一.1]。为什么必须是 UEFI？HAOS 的引导流程基于 UEFI 规范（systemd-boot / OVMF），其引导逻辑不兼容传统 BIOS 的 MBR 启动流程。因此无论哪个虚拟化平台，固件设置里都必须把启动模式切到 UEFI，而不是「能开机就万事大吉」：



- **VirtualBox**：虚拟机设置里勾选 "Use EFI"（默认是 BIOS，必须手动改）。
- **KVM / Proxmox**：BIOS 选项选 OVMF（UEFI）固件，注意选非 secureboot 的 OVMF，并给 VM 挂一块 EFI 盘。
- **VMware / Hyper-V**：同样在固件设置中把 BIOS 切换为 UEFI。

这是新手部署 HAOS VM 最常见的失败点之一：镜像正确、配置看着没问题，但忘了 UEFI，开机就黑屏。

### 镜像格式

官方按虚拟化平台提供不同格式的虚拟磁盘镜像，统一命名为 `haos_ova-{version}`，下载后需先解压再使用 [素材 §一.1]：

| 格式 | 对应平台 | 说明 |
|------|---------|------|
| qcow2 | KVM / Proxmox | QEMU 原生格式，支持快照 |
| vdi | VirtualBox | VirtualBox 默认格式 |
| vmdk | VMware | VMware 系列产品 |
| vhdx | Hyper-V | 微软 Hyper-V 格式 |
| ova | 跨平台 | 打包格式，内含虚拟机和磁盘 |

部署的本质动作是：建一台开启 UEFI 的虚拟机 → 把解压后的磁盘镜像挂给这台 VM（Proxmox 里是 `qm importdisk` 导入）→ 启动 → 浏览器访问 `homeassistant.local:8123` 完成初始化。完整的 Proxmox 操作步骤见第八章附录，本节聚焦参数层面的要求。

## 3.4 Supervisor 机制拆解

Supervisor 是 HAOS「省心」的核心引擎。理解它的三个机制，就理解了 HAOS 为什么比 Container 方式省事 [素材 §一.1]。

### Add-on 本质是 Docker 容器

Add-on 商店里那些「插件」（Thread、Z-Wave JS、ESPHome、Node-RED、Samba、SSH 等），本质都是 Supervisor 托管的 Docker 容器 [素材 §一.1]。Supervisor 负责：从商店拉取镜像、创建容器、按依赖关系启动、崩溃自动重启、在设置页暴露配置入口。

这与「集成」（Integration）有本质区别：集成跑在 Core 进程内，Add-on 是独立容器。需要系统级能力（如操作 Zigbee 协调器、编译 ESPHome 固件）的功能，都以 Add-on 形式提供——这也是 Container 方式「开箱不支持 Thread / Z-Wave」的根本原因（见第二章对比表）。

Supervisor 对 Add-on 的生命周期是全程托管的：安装时校验依赖、拉取镜像并创建容器，运行时按 restart 策略守护，卸载时清理容器与镜像。用户不接触 Docker CLI，一切通过商店界面完成——这是「容器技术」与「家电式体验」之间的关键桥梁。

### 快照备份与一键还原

Supervisor 提供托管快照（Snapshot）：把 HA 配置、集成状态、Add-on 及其数据、媒体全部打包成压缩归档，可下载到本地，也可存到 Google Drive / OneDrive / NAS 等备份位置。还原时在初始化向导或设置页一键导入即可，甚至可以做到任意安装方式之间、跨架构恢复（第七章会详述迁移）。

对普通用户的意义：备份不再是一个需要自己写 cron + rsync 的工程问题，而是设置页里的一个开关。

### OTA 式自动更新链路

Supervisor 约每 8 小时检查一次更新 [素材 §一.1]，更新对象包括：

- **OS**（HAOS 底层镜像）
- **内核**（随 OS 一起）
- **Supervisor 自身**
- **Core**（可选，可按更新策略设置）

更新方式接近 OTA：Supervisor 拉取新镜像、创建新分区/新容器、原子切换，失败可回滚，而不是在现有系统上「原地打补丁」。用户可以设置自动更新策略（如只自动更 Supervisor，Core 手动确认），兼顾省心与稳妥。

## 3.5 Proxmox 推荐配置（社区实践）

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

### 实操命令（原样摘录）

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

## 3.6 优点 / 缺点 / 适用场景

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

## 本章小结

- HAOS 是只读、无 apt、独占整机的嵌入式 Linux，内建 Core + Supervisor，是官方定位 most users 的推荐方式。
- 虚拟机部署硬性要求：最低 2GB / 2vCPU / 32GB（推荐 4GB）、必须启用 UEFI（VirtualBox 勾 EFI，KVM 用非 secureboot 的 OVMF）、镜像按平台选 qcow2 / vdi / vmdk / vhdx / ova。
- Supervisor 三件套：Add-on 是托管的 Docker 容器、快照一键备份与还原、约每 8 小时 OTA 自动更新 OS / 内核 / Supervisor。
- Proxmox 社区配置：q35 + UEFI + virtio-scsi-pci + 32GB 磁盘，CPU 用 kvm64（可迁移）或 host（性能最好），内存 4096MB + 内存气球。
- 优点集中在省心与功能完整，代价是只读系统、独占整机、资源开销大；适合愿意用一台专用机器换零维护的用户。

## 下一章预告

第四章转向天平的另一端：Docker Container。它只跑 Core、无 Supervisor 与 Add-on，官方 compose 模板如何逐行拆解、升级与维护怎么做、有哪些常见坑，将一一拆给你看。
