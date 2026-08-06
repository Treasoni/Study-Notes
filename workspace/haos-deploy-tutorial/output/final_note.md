# 部署 HAOS 详细教程：国内源 + 稳定运行

> [!summary] 全文摘要
> 本文是一篇面向国内网络环境的 [[HAOS]] 专项部署实操教程，聚焦「怎么装、怎么配国内源、怎么稳定运行」三件事。全篇 8 章沿「安装 → 加速 → 对比 → 稳定 → 排障」主线展开：先备齐平台、存储、固件、镜像与工具链，再走通官方原版 HAOS 在实体机、VMware、PVE、群晖 VMM 四大平台的完整安装；随后为官方原版手动配置一套国内加速（Docker 12 源故障转移、Supervisor ghcr 镜像、Add-on 国内仓库、NTP 国内时间源），并介绍内置全套加速的一键替代方案 [[HAOS-CN]] 极速版；最后用双路线对比表完成选型，落定 SSD 迁移、Google Drive 世代备份、升级回滚等稳定运行策略，以及错误码速查与长期运维清单。文中所有镜像站地址、版本号、错误码均以实际官网/日志为准，素材采集时间 2026-08-06。

## 目录

1. [第一章：绪论——为什么需要「国内源 + 稳定运行」](#第一章绪论为什么需要国内源-稳定运行)
2. [第二章：部署前置准备——存储、固件、镜像与工具链](#第二章部署前置准备-存储固件镜像与工具链)
3. [第三章：官方原版 HAOS 安装实战（实体机 + 虚拟机全平台）](#第三章官方原版-haos-安装实战实体机-虚拟机全平台)
4. [第四章：手动配置国内源（官方原版加速核心）](#第四章手动配置国内源官方原版加速核心)
5. [第五章：HAOS-CN 极速版——一键国内化替代方案](#第五章haos-cn-极速版-一键国内化替代方案)
6. [第六章：双路线对比与选型建议](#第六章双路线对比与选型建议)
7. [第七章 稳定运行保障——存储、备份与升级](#第七章-稳定运行保障-存储备份与升级)
8. [第八章 故障排查手册与长期运维](#第八章-故障排查手册与长期运维)

---

## 第一章：绪论——为什么需要「国内源 + 稳定运行」

> [!summary] 本章讲什么
> 本章回答一个核心问题：为什么在大陆网络环境下部署 HAOS 不能照搬官方流程。你会看到三个最常见痛点（ghcr 拉取慢/被墙、Add-on 商店加载失败、时间不同步），理解本文的双路线框架（官方原版 + 手动配置国内源 vs HAOS-CN 极速版），并明确本文与既有选型笔记的边界。

### 1.1 国内网络环境下的部署痛点

官方安装文档假设的是「能顺畅访问 GitHub Container Registry（ghcr.io）」的网络环境。大陆网络环境下这个假设不成立，部署 [[HAOS]] 会卡在三个地方：

- **ghcr.io 拉取慢/被墙**：HAOS 首次启动需要从 ghcr.io 拉取约 700MB 的核心与镜像，国内网络下可能耗时数小时甚至直接失败。
- **Add-on 商店加载失败**：官方加载项的镜像同样托管在 ghcr.io，商店打不开、加载项装不上，是国内用户的高频问题。
- **时间不同步**：证书校验、自动化、OTA 更新都依赖系统时间。默认 NTP 源在墙外，时间持续漂移会引发证书失效、自动化不触发等「看起来莫名其妙」的问题。

> [!warning] 时效性说明
> 本文所有镜像站地址、[[HAOS-CN]] 版本号、错误码均以实际官网/日志为准。素材采集时间：2026-08-06。Docker 公益镜像站存在隔天失效的常见风险，本教程会提供多源清单与故障转移思想，而非依赖单一镜像站。

这三个痛点不是孤立的，而是同一个根因——默认依赖的海外服务在大陆网络不可达或极慢。解决思路只有两条：要么手动给官方原版配国内源，要么直接换一个内置国内加速的再发行版。这就引出了本文的双路线框架。

### 1.2 双路线总览与本文定位

本文围绕两条路线展开，全程对照：

| 维度 | 官方原版 HAOS | HAOS-CN 极速版 |
|------|--------------|----------------|
| 国内源 | 需手动配置（Docker / Supervisor / Add-on / NTP / DNS） | 内置：12 个 Docker 源 + 8 类网络重定向 |
| 首次启动 | ghcr 拉取 700MB，国内可能数小时 | 在线式数十分钟 / `-full` 完整包即装即用 |
| 可配置性 | 每项源可解释、可掌控 | 安装后不可改、无关闭开关 |
| 完整性校验 | 官方 SHA256 齐全 | 系统镜像无校验和 |
| 更新机制 | 官方 OTA（慢） | 国内 OTA（快，A/B 原子更新可回滚） |
| 信任模型 | 官方背书 | 依赖项目方与第三方镜像站 |

**路线 A（官方原版 + 手动配置国内源）**：每一层加速——Docker、Supervisor、Add-on、NTP、DNS——都可解释、可掌控，适合想理解机制、追求透明可控的用户，也是本文 3–4 章的主体。

**路线 B（[[HAOS-CN]] 极速版）**：社区开源再发行（ha-china/HAOS-CN），把国内加速内置到系统里，适合「装上就能用、不想折腾」的用户，代价是信任模型转移到项目方、系统内加速不可关闭。详见第 5 章。

两条路线的「稳定运行」共识是相通的：存储先用 SSD、UEFI + SATA、备份是安全网、NTP/DNS 国内化、正确重启。这些统一在第 7、8 章展开。

### 1.3 学习路线图与前置知识（呼应既有选型笔记）

本文是 HAOS 专项实操教程，不是选型教程。选型层面的对比——HAOS 与 Docker Container、Supervised 的差异——已由 [[Home Assistant 三种部署方式对比与选型]] 讲透（Supervised 已于 2025.12 弃用）。本文默认你已经选定 HAOS，只聚焦三件事：**怎么装、怎么配国内源、怎么稳定运行**。

全文共 8 章，学习路径是一条主线：安装 → 加速 → 对比 → 稳定 → 排障。

| 章节 | 主题 | 一句话目标 |
|------|------|-----------|
| 第 1 章 | 绪论 | 建立双路线心智模型，明确本文边界 |
| 第 2 章 | 部署前置准备 | 平台、存储、固件、镜像、工具链一次备齐 |
| 第 3 章 | 官方原版安装实战 | 实体机 + VMware / PVE / 群晖 VMM 全平台走通 |
| 第 4 章 | 手动配置国内源 | 官方路线核心价值，Docker / Supervisor / Add-on / NTP 逐个加速 |
| 第 5 章 | HAOS-CN 极速版 | 了解替代方案与风险边界 |
| 第 6 章 | 双路线对比与选型 | 读对比表做最终决策 |
| 第 7 章 | 稳定运行保障 | SSD 迁移、备份、升级与回滚 |
| 第 8 章 | 故障排查与长期运维 | 错误码速查、远程访问、运维清单 |

前置知识：能看懂基础 Linux/Shell（`vi`、`systemctl`、`curl`、`scp`、`docker info`），有一台可用的部署主机（实体机 x86-64，或 VMware / PVE / 群晖 VMM 任一），并有国内可用的网络环境。若只想要「最省心」方案，可以直接跳到第 5 章用 HAOS-CN `-full` 完整包，但仍建议回看第 2、7 章的存储与备份原则。

### 本章 Checklist

- [ ] 我能说出大陆网络下部署 HAOS 的三个核心痛点
- [ ] 我理解双路线框架：官方原版 + 手动国内源 vs [[HAOS-CN]] 极速版
- [ ] 我清楚本文与 [[Home Assistant 三种部署方式对比与选型]] 的边界：不重复选型，聚焦「如何装 + 国内源 + 稳定运行」
- [ ] 我已知晓素材采集时间（2026-08-06），镜像站/版本/错误码以实际官网为准

---

> 下一章预告：动手之前把硬件和材料一次备齐——平台选型、SSD 优先、固件设置、镜像下载校验与工具链准备。

## 第二章：部署前置准备——存储、固件、镜像与工具链

> [!summary] 本章讲什么
> 动手之前把硬件和材料一次备齐。你会确定部署平台（实体机 vs 虚拟机）、理解为什么存储优先选 SSD（TF 卡必坏原理）、完成固件设置（UEFI、关闭 Secure Boot、无需 TPM）、下载并校验官方镜像，最后备好烧录/导入工具链。

### 2.1 部署平台与硬件选型

[[HAOS]] 可以刷到实体机，也可以跑在虚拟机里。选哪个，取决于你手上有什么、这台机器还要不要干别的。

| 平台 | 适用场景 | 关键要求 |
|------|---------|---------|
| 实体机 x86-64 | 迷你主机 / NUC / 旧 PC 专机专用 | x86-64 架构；UEFI 引导；存储优先 SSD |
| VMware Workstation | 已在 Windows 上跑虚拟机 | 网络选 Bridged 桥接；固件改 EFI |
| PVE（Proxmox VE） | 已有虚拟化宿主机，多服务共存 | i440fx + OVMF(UEFI)；SATA 总线；导入 qcow2 |
| 群晖 VMM | 群晖 NAS 用户 | 固件必须 UEFI；磁盘控制器 SATA、≥32GB；建议 Open vSwitch |

无论哪种平台，官方/社区一致的资源底线是：**2 vCPU + 2GB 内存起、磁盘 ≥32GB、SATA 总线**。本文聚焦 x86-64 实体机 + 主流虚拟机平台，树莓派等 ARM 设备不在覆盖范围（选型与边界见 [[Home Assistant 三种部署方式对比与选型]]）。

> [!tip] 新手建议
> 如果只是想先跑起来验证，虚拟机（VMware 或 PVE）是试错成本最低的选择：镜像导入失败、配置错了，删掉 VM 重来即可，不碰实体硬件。

### 2.2 存储介质：SSD 优先原则

存储介质是 HAOS 稳定运行的第一要素。官方教程默认支持 TF 卡，但 TF 卡对 HA 的写入负载来说是**错误介质**。

根因是写入频率：HA 数据库每秒钟约产生 **15 次写入**，microSD 闪存寿命远低于这个负载，实际使用数月就会损坏。这不是卡的质量问题，而是「介质不匹配」（[Best SSD for Home Assistant in 2026](https://evezone.evetech.co.za/deep-dives/best-ssd-for-home-assistant-in-2026-stop-sd-card-corruption-for-good)）。

按平台选型 SSD：

| 平台 | 推荐存储方案 |
|------|-------------|
| 树莓派 Pi4 及更早 | SATA SSD + USB 3.0 硬盘盒 |
| 树莓派 Pi5 | PCIe NVMe |
| 迷你主机 / NUC | 内置 SATA 或 NVMe |

容量不用追求大，但 HA 数据库、媒体、快照会持续增长，预留 40–64GB 足够。迁移到 SSD 的完整操作留到第七章（完整备份 → 官方镜像写入 SSD → SSD 引导 → 恢复备份）。

> [!warning] 别把系统装在 TF 卡上长期跑
> 如果临时用 TF 卡验证，请把它当作「一次性试玩」，尽快迁移到 SSD。数据库写入导致的 TF 卡损坏是 HAOS 社区最高频的故障之一。

### 2.3 固件与引导设置（UEFI / Secure Boot / TPM）

HAOS 的引导基于 UEFI 规范（systemd-boot / OVMF），不兼容传统 BIOS 的 MBR 启动（[官方文档 generic-x86-64](https://www.home-assistant.io/installation/generic-x86-64)）。因此在实体机 BIOS 或虚拟机固件设置里，必须满足三点：

| 设置项 | 要求 | 原因 |
|--------|------|------|
| 引导模式 | 必须 **UEFI** | HAOS 引导逻辑只认 UEFI |
| Secure Boot | 必须 **关闭** | 官方文档明确要求关闭 |
| TPM | **无需** TPM | HAOS 不依赖 TPM，无需额外配置 |

实体机进 BIOS（常见 F2 / Del），把启动模式设为 UEFI 并关闭 Secure Boot；虚拟机平台在固件选项里选 UEFI/OVMF（VMware 需在 `.vmx` 加 `firmware = "efi"`，PVE 选 OVMF(UEFI) 并取消勾选添加 EFI 磁盘）。

> [!warning] UEFI 找不到引导介质
> 这是新手最常见的失败点：UEFI 下报「找不到引导介质」时，手动指定引导文件 `\EFI\BOOT\bootx64.efi`，或用 `efibootmgr` 重建引导项（完整命令见 3.1 节）。

### 2.4 镜像下载、校验与工具链准备

#### 镜像选择

官方按部署形态提供不同镜像，统一命名为 `haos_{platform}-{version}`：

| 镜像文件 | 对应场景 |
|---------|---------|
| `haos_generic-x86-64-{version}.img.xz` | 实体机刷写（写入即启动，会清空目标盘，无安装器） |
| `haos_ova-{version}.vmdk.zip` | VMware Workstation |
| `haos_ova-{version}.qcow2.xz` | PVE（KVM） |
| `haos_ova-{version}.vdi` | VirtualBox |
| `haos_ova-{version}.vhdx` | Hyper-V |

镜像托管在官方 GitHub Releases，大陆网络下下载可能很慢，可借助 gh-proxy 类加速前缀下载。具体加速地址以实际可用为准（素材采集时间：2026-08-06）。

> [!warning] 下载后务必校验
> 官方路线完整性校验的可靠来源是官方发布的 SHA256 校验和。经第三方网盘/加速站下载的镜像，更要先校验再写入，避免拿到被篡改的镜像。

#### SHA256 校验

```bash
# 下载校验和文件（与镜像同目录），再核对哈希
sha256sum haos_generic-x86-64-{version}.img.xz
cat haos_{version}.sha256
# 人工比对两行哈希是否一致；也可用 sha256sum -c 自动校验
```

#### 烧录 / 导入工具链

| 工具 | 用途 | 平台 |
|------|------|------|
| balenaEtcher | 镜像写入 U 盘/SSD（先解压 `.xz`；选 Flash from file，勿用 Flash from URL） | Win / macOS / Linux |
| Rufus | Windows 下写入 U 盘 | Windows |
| Ventoy | 多镜像 U 盘引导工具 | Win / Linux |
| Ubuntu Disks | Linux 下 Restore Disk Image 恢复镜像 | Linux |
| `xz` + `scp` + `qm importdisk` | PVE 解压、上传、导入虚拟磁盘（qcow2 不能走 ISO 上传） | PVE |

> [!example] PVE 上传并导入 qcow2 示例
> ```bash
> # 本地解压 .qcow2.xz
> xz -d haos_ova-{version}.qcow2.xz
> # 上传到 PVE 宿主 /tmp（qcow2 不走 ISO 上传通道）
> scp haos_ova-{version}.qcow2 root@<PVE_IP>:/tmp/
> # 在 PVE 宿主上导入到 VM 100（VMID 换成实际编号）
> qm importdisk 100 /tmp/haos_ova-{version}.qcow2 local
> ```

导入后进入 PVE 硬件页，把「未使用的磁盘0」添加到 VM，总线改成 **SATA**，并把引导顺序置为 `sata0` 优先（完整步骤见 3.3 节）。

### 本章 Checklist

- [ ] 我已确定部署平台（实体机 / VMware / PVE / 群晖 VMM 之一），资源 ≥ 2 vCPU + 2GB + 32GB 磁盘
- [ ] 我理解 TF 卡必坏原理（HA 约 15 次写入/秒），决定存储优先 SSD
- [ ] 我已确认固件：UEFI 开启、Secure Boot 关闭、无需 TPM
- [ ] 我已下载对应平台官方镜像，并用 `sha256sum` 核对 SHA256
- [ ] 我已备好烧录/导入工具（balenaEtcher / Rufus / Ventoy / Ubuntu Disks / PVE 导入命令）

---

> 下一章预告：正式进入安装实战——实体机刷写与 UEFI 引导，以及 VMware / PVE / 群晖 VMM 三大虚拟机平台的完整步骤。

## 第三章：官方原版 HAOS 安装实战（实体机 + 虚拟机全平台）

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

删除向导自动生成的 vmdk，把 HAOS 解压出的 vmdk 改名为 `home-assistant.vmdk`，复制进该 VM 的目录。改名不是必须的，但社区验证这样做最稳妥——避免 VMware 把 HAOS 磁盘当成普通数据盘处理。

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

### 本章 Checklist

- [ ] 实体机：已开 UEFI、关 Secure Boot，用 balenaEtcher / Disks 刷入 `haos_generic-x86-64-{ver}.img.xz`
- [ ] 实体机：遇 target is busy 时已卸载 Swap 分区；引导失败时已指定 `\EFI\BOOT\bootx64.efi`
- [ ] VMware：虚拟机类型 Other Linux 5.x 64-bit，内存 ≥2048MB、CPU ≥2 核、网络 Bridged 桥接
- [ ] VMware：已替换为 `home-assistant.vmdk`，并在 `.vmx` 中加入 `firmware = "efi"`
- [ ] PVE：i440fx + OVMF(UEFI)（未添加 EFI 磁盘），已删除默认 SCSI 盘
- [ ] PVE：已 `scp` 上传 qcow2 并执行 `qm importdisk`，导入盘总线改 SATA、`sata0` 置顶
- [ ] 群晖 VMM：固件 UEFI、磁盘控制器 SATA、容量 ≥32GB，已开启 Open vSwitch
- [ ] 已确认首次启动保持联网，能通过 `http://homeassistant.local:8123`（或 `http://<IP>:8123`）进入初始化向导

## 第四章：手动配置国内源（官方原版加速核心）

> [!summary] 本章讲什么
> 本章解决官方原版 [[HAOS]] 在国内网络下的五大拉取瓶颈：Docker 镜像（12 源故障转移链）、Supervisor 的 ghcr.io（`registries_mirror`）、Add-on 商店（国内仓库 + 镜像映射）、NTP 时间（国内时间源 + 首次启动预置）、首次启动 DNS/ghcr 加速（udev 方案及其失效提醒）。这是官方路线的核心价值章节，每一节都给出可直接复制的配置片段与验证命令。

> [!warning] 时效性说明
> 本章所有镜像站地址、仓库地址、GitHub 讨论链接均为采集时间（2026-08-06）可用的社区源。公益镜像站隔天失效是常态，请以实际拉取结果为准；遇到失效回到 4.1 / 4.2 换源即可，不要怀疑配置本身。udev 覆盖方案已在 2026.2.1 起失效，详见 4.5。

### 4.1 Docker 镜像加速：12 源故障转移链与验证

国内直连 Docker Hub（docker.io）拉镜像普遍慢或超时，根因是官方 Registry 节点没有覆盖大陆网络。Docker daemon 提供 `registry-mirrors` 配置：拉取 docker.io 镜像时自动改走镜像站，镜像站会回源缓存，命中缓存的镜像几乎秒下。

这段 12 源配置本质是一条"故障转移链"。daemon 会按数组顺序依次尝试，前面某个源连接超时或返回 429 时自动落到下一个，直到成功。这就是为什么公益源不稳定也不用怕——多配几个，坏一两个不影响整体。

配置写入 `/etc/docker/daemon.json`（完整 12 源示例）：

```json
{
  "registry-mirrors": [
    "https://docker.1panel.live", "https://docker.1ms.run", "https://dytt.online",
    "https://docker-0.unsee.tech", "https://lispy.org", "https://docker.xiaogenban1993.com",
    "https://666860.xyz", "https://hub.rat.dev", "https://docker.m.daocloud.io",
    "https://demo.52013120.xyz", "https://proxy.vvvv.ee", "https://registry.cyou"
  ]
}
```

改完后重启 Docker 并验证镜像源是否生效：

```bash
systemctl restart docker
docker info | grep -A5 "Registry Mirrors"
```

看到列出的 12 个地址即生效。再拉一个小镜像实测速度：

```bash
docker pull hello-world
```

能秒下说明至少有一个源是通的。除了这 12 个公益源，还有 `docker.nju.edu.cn`、`docker.mirrors.ustc.edu.cn`，以及需申请专属地址的阿里云加速器（`<你的ID>.mirror.aliyuncs.com`）。源越多，故障转移的兜底越厚。

两个关键坑必须记住：

> [!warning] 坑一：`registry-mirrors` 只对 docker.io 生效
> 它只改写 docker.io 的拉取地址，对 **ghcr.io 无效**。而 HA 的核心镜像和官方 Add-on 镜像恰恰托管在 ghcr.io——这部分需要走 4.2 的 Supervisor 层配置，两条路径互补，缺一不可。

> [!warning] 坑二：原版 HAOS 根文件系统只读
> 在 HAOS 里 `/etc/docker/daemon.json` 位于只读根文件系统，**无法直接编辑**。这条配置真正落地的场景是：你在跑普通 Linux + Docker（或 Supervised 安装）；HAOS 场景要靠 4.5 的 udev bind-mount 覆盖，或者直接用内置了 12 源故障转移的 [[HAOS-CN]]（见第 5 章）。

> [!tip] 实操建议
> 公益镜像站隔天失效很常见，所以"多配几个 + 故障转移"比"只信某一个"更重要。如果哪天发现镜像拉不动，先 `docker pull` 单测判断是不是源挂了，再决定是否替换清单里的失效项。配好之后把拉取命令存成脚本，每月巡检一次（第 8 章有周期性清单）。

### 4.2 Supervisor 镜像源：破解 ghcr.io 拉取瓶颈

这是官方原版解决 ghcr.io 的核心路径，也是本章最值钱的一节。先讲原理：HA 架构里 Supervisor 是"调度中枢"，Core 和所有 Add-on 的容器镜像都由它负责拉取，而这些镜像全部托管在 GitHub Container Registry（ghcr.io）。国内直连 ghcr.io 经常超时，表现就是 Add-on 装不上、Core 更新拉不动、系统卡在启动的转圈界面。

配置分两个文件，各管一件事：

**文件一：`/etc/hassio.json`** —— 改 Supervisor 自身的镜像地址，让 Supervisor 拉取/更新自身时走国内镜像：

```bash
# /etc/hassio.json：改 supervisor 自身镜像
#   "supervisor": "ghcr.nju.edu.cn/xjboss/{arch}-hassio-supervisor"
#   {arch} = amd64（x86_64 实体机/虚拟机）或 aarch64（ARM 派）
```

**文件二：`/usr/share/hassio/docker.json`** —— 加 `registries_mirror`，把 ghcr.io 和 docker.io 的拉取整体映射到国内镜像：

```bash
vi /usr/share/hassio/docker.json
```

```json
{
  "registries": {},
  "registries_mirror": { "ghcr.io": "ghcr.nju.edu.cn", "docker.io": "docker.nju.edu.cn" }
}
```

保存后重启 Supervisor 使配置生效：

```bash
systemctl restart hassio-supervisor
```

重启后去 Add-on 商店安装一个之前装不上的加载项，速度应明显改善。也可以观察 Supervisor 日志确认它走的是国内源，而不是卡在 ghcr 超时。

> [!warning] 易错点：升级会重置，必须先备份
> HAOS 系统升级时 `/usr/share/hassio/docker.json` 很可能被重置为默认值，导致加速悄悄失效。建议把这个文件复制一份备份，升级后对比恢复：

```bash
cp /usr/share/hassio/docker.json /usr/share/hassio/docker.json.bak
```

> [!note] 能力边界
> `registries_mirror` 只解决**镜像拉取**，不解决 GitHub 源码下载和 OTA 升级。Add-on 仓库从 GitHub 拉源码、系统更新走官方 OTA，这些在国内仍可能慢，需要配合 4.3 的国内仓库，以及第 5 章讲到的国内 OTA 方案。

### 4.3 Add-on 商店国内仓库与镜像映射

Add-on 商店默认的仓库列表大多指向 github.com / ghcr.io，国内加载经常转圈或直接失败。解决思路是双管齐下：添加一个托管在 Gitee 的国内仓库作为安装源，再用镜像映射表把拉取地址替换成国内可达地址。

添加国内仓库的入口在 Web 界面：

> [!example] 添加仓库
> 设置 → 加载项商店 → 右上角三个点 → 仓库 → 粘贴以下地址并添加：
>
> ```
> https://gitee.com/desmond_GT/hassio-addons
> ```

添加后，商店里出现的加载项安装时，镜像地址按下面这张映射表替换（正文平铺，可直接对照）：

| 原地址 | 国内镜像 | 用途 |
|--------|---------|------|
| ghcr.io | `ghcr.nju.edu.cn` | Add-on 容器镜像（核心加速项） |
| docker.io / lscr.io | `docker.1panel.live` | Docker Hub 与 LinuxServer 镜像 |
| github.com | `gh-proxy.org` | GitHub 仓库源码 / 更新 |

理解一下机制：每个 Add-on 的 manifest 里声明了 `image` 字段，Supervisor 拉取时按这张映射把镜像地址改写成国内镜像。所以映射表和 4.2 的 `registries_mirror` 是一套思路的两种实现，前者管 Add-on 声明，后者管全局镜像名。

> [!warning] 易错点
> 配置后**无需翻墙**，翻墙反而可能因为代理链路导致失败；国内镜像首次安装偶发失败是正常的，**重试一次即可**。另外注意 GitHub 仓库仅用于更新源列表，实际安装走 Gitee 地址，两者不冲突。如果添加仓库后列表不刷新，先在系统日志确认是网络问题还是地址过期。

### 4.4 NTP 时间同步国内化（含首次启动预置）

时间不同步是国内 HAOS 一个隐蔽的"稳定性杀手"：HTTPS 证书校验、自动化定时触发、更新检查、日志时间戳全部依赖准确时间。HAOS 默认指向国际 NTP 源，国内网络经常超时，导致系统时间持续偏移，轻则日志时间错乱，重则证书校验失败、更新拉不下来。

通过 SSH（root，端口 22222）登录后，编辑时间同步配置：

```ini
# /etc/systemd/timesyncd.conf
[Time]
NTP=ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com
FallbackNTP=ntp.tencent.com cn.pool.ntp.org
```

重启时间同步服务并验证：

```bash
systemctl restart systemd-timesyncd.service
timedatectl
```

看到 `System clock synchronized: yes` 即同步成功，此时时间已经对准国内源。除了阿里云（`ntp1~7.aliyun.com`）、腾讯（`ntp.tencent.com`），还可用 `ntp.ntsc.ac.cn`（中科院国家授时中心）作为备选。多填几个，一个挂了自动切换。

> [!tip] 首次启动前预置（强烈建议）
> 系统还没跑起来之前，在烧录后的 `hassio-boot` 分区的 `CONFIG/timesyncd.conf` 里放好同样的配置（**权限设为 644**），首次启动即可在 10 秒内完成时间同步。这一点对首次启动至关重要：首次启动要联网拉取约 700MB 的 Core 组件，如果时间没对齐，HTTPS 证书校验会失败，导致拉取莫名其妙失败或极慢。

容器环境（Supervised / 普通 Linux 跑 HA）没有 `timesyncd` 时，改用 **chrony 加载项**：把 `ntp_pool` 改成 `cn.pool.ntp.org`，并开启开机自启。

> [!warning] 时间异常判别法
> - 差**整 8 小时**：是时区未设（没设 Asia/Shanghai），不是 NTP 问题，去设置里改时区。
> - 差**几分钟且持续增大**：是 NTP 同步失败，回上面对比 `timedatectl` 的同步状态。
> 分不清时区问题与同步问题时，先 `timedatectl` 看 `Time zone` 一行再决定处理方向。确认时区用 `timedatectl set-timezone Asia/Shanghai`。

### 4.5 首次启动 DNS/ghcr 加速补充与方案失效提醒

由于原版 HAOS 根文件系统只读，社区曾用一个技巧绕开：用 **udev bind-mount** 在 Docker 服务启动前，把宿主机上的 `daemon.json`（含 `proxies` 配置走 ghcr 代理）覆盖挂载进系统，从而在首次启动拉 ghcr 镜像时实现加速。原理是在只读根上做一层"可写覆盖"，相当于把一个外部文件绑定到只读路径上。

> [!warning] 方案已失效（2026.2.1）
> 该 udev 覆盖方案在 **2026.2.1 版本起失效**。新版 HAOS 原样照抄旧教程的整套 udev 规则会 **boot loop**，需要精简字段才可能适配。采集时间（2026-08-06）的最新版本上，这个方案已不建议作为主线，只作原理理解。看到 2025 年及更早的教程让你"直接复制整套 udev 规则"，务必保持警惕。

> [!tip] ghcr 拉取困难的现实推荐排序
> 按"省心程度 + 有效性"排序，解决 ghcr 拉取瓶颈的优先顺序：
> 1. 国内定制版（[[HAOS-CN]]，第 5 章）——内置全套加速，最省心；
> 2. Supervisor `registries_mirror`（4.2）——官方原版的正路；
> 3. udev bind-mount——已被版本淘汰，仅当跑旧版时考虑；
> 4. 手拉镜像改名——手动 pull 国内源再 tag 成 ghcr.io 地址，最费事但永远可用作应急。

> [!tip] 首次启动实测预期
> 首次启动联网拉取约 700MB 组件，国内网络下慢是正常的（数小时也可能出现），**期间不要断电**。加速的正确姿势是：先按 4.4 预置 `timesyncd.conf` 保证时间对齐，再靠 4.2 的 Supervisor 镜像源加速 ghcr 拉取；等不了的话，直接换第 5 章的 `-full` 完整包免初始化等待。给这台机器配个静态 IP 也能避免重启后 DHCP 重试导致的等待（第 8 章有排查）。

### 本章 Checklist

- [ ] 理解 `registry-mirrors` 只对 docker.io 生效，对 ghcr.io 无效
- [ ] 知道原版 HAOS 根文件系统只读，`/etc/docker/daemon.json` 不可直接改
- [ ] 已在 `/usr/share/hassio/docker.json` 配置 `registries_mirror`（ghcr.io → ghcr.nju.edu.cn）
- [ ] 已 `systemctl restart hassio-supervisor` 并验证 Add-on 安装提速
- [ ] 已备份 `docker.json`，知道升级可能重置它
- [ ] 已在 Add-on 商店添加 Gitee 国内仓库（`https://gitee.com/desmond_GT/hassio-addons`）
- [ ] 知道镜像映射表：ghcr.io / docker.io / lscr.io / github.com 各自走哪个国内镜像
- [ ] 已配置 `timesyncd.conf` 国内 NTP 源并 `timedatectl` 确认 `System clock synchronized: yes`
- [ ] 首次启动前已在 `hassio-boot/CONFIG/timesyncd.conf` 预置时间源（权限 644）
- [ ] 能区分"差整 8 小时（时区）"与"持续增大（NTP）"
- [ ] 知道 udev bind-mount 方案已随 2026.2.1 失效，不在新版本原样照抄
- [ ] 理解 ghcr 加速的推荐排序：HAOS-CN > Supervisor registries_mirror > udev > 手拉镜像

---

> 下一章预告：官方原版的手动加速到这里已全部配齐。如果你不想逐层折腾，下一章介绍 [[HAOS-CN]] 极速版——内置全套国内加速的一键替代方案，并如实列出它的信任模型与风险边界。

## 第五章：HAOS-CN 极速版——一键国内化替代方案

> [!summary] 本章讲什么
> 前四章走的是「官方原版 + 手动配置国内源」路线：每一项源都可解释、可掌控，但都要自己动手。本章介绍替代路线 **HAOS-CN 极速版**（官方英文名「Home Assistant OS Turbo」）——一个面向国内网络环境改造再分发的社区开源版本。读完你会搞清楚三件事：它凭什么能「装完即用」（内置加速机制）、怎么下载和互转（OTA 脚本 + A/B 分区）、以及接受它要付出什么代价（风险清单）。选型边界：本章不重复 [[Home Assistant 三种部署方式对比与选型]] 里的 HAOS / Docker / Supervised 对比，只回答「要不要用这个替代发行版」。

### 5.1 项目概述与信任模型

[[HAOS-CN]] 是 GitHub 社区项目 `ha-china/HAOS-CN`，把官方 [[HAOS]] 重新构建成「更适合中国网络环境」的版本。先区分两组容易混淆的名字：

| 项目 | 开源 | 说明 |
| ---- | ---- | ---- |
| HAOS-CN 极速版 | 开源 | ha-china 社区维护，GitHub 仓库公开，官方英文名 Home Assistant OS Turbo |
| 冬瓜 HAOS | 闭源 | 瀚思彼岸（Hassbian）社区的定制版，源码与构建脚本不公开 |

极速版的核心改动有两处：**官方加载项源替换为国内加速源**，以及**集成 HACS 极速版**——装上就有 HACS，不需要 GitHub 账号，也不需要科学上网。

更新走**自建 OTA**（`ota.hasscn.top`，由深圳酷宅 CoolKit 赞助，仅限中国 IP 访问）。构建节奏固定：每月 27 日构建新版本、28 日自动检查更新；项目声明不商业化、公司可免费使用。本文采集时主版本为 **18.2**，具体以官网为准。

有意思的是，即便在「手动配置国内源」的社区方法论里，HAOS-CN 也被排在推荐序列首位（国内定制版 > Supervisor `registries_mirror` > udev bind-mount > 手拉镜像改名）。也就是说，第四章那套手动配置不是要你「拒绝极速版」，而是提供一条官方原版路线下可解释、可掌控的加速方案——两条路线是**互补**关系，不是互斥关系。

> [!warning] 信任模型要自己掂量
> 虽然项目仓库公开，但**端点配置是构建时经私有脚本注入的，公开仓库里看不到完整生成过程**。最终刷进设备的镜像到底改了什么，只能信任项目方。这与官方原版（代码全量公开、镜像可复现）的信任模型有本质差别。

### 5.2 下载、格式选择与校验缺口

下载站提供与官方一致的格式矩阵：`img.xz`、`qcow2.xz`、`vdi.zip`、`vmdk.zip`、`ova`、`vhdx.zip`，覆盖 generic x86-64 / generic aarch64 / HA Green / HA Yellow / Sonoff iHost / OrangePi CM4 / Panther X2 / Raspberry Pi 3/4/5 / Hyper-V 等平台。

下载时先分清两种包：

| 类型 | 行为 | 适用 |
| ---- | ---- | ---- |
| 在线式 | 与官方一致，装完需联网拉依赖 | 网络可用、能等首次初始化 |
| 完整包（`-full`） | 装完即用、免初始化等待 | 网络差、想开箱即用 |

> [!warning] 一个已知缺口
> x86-64 的 `qcow2` / `vdi` / `vmdk` **在线式列表缺失**，只有 `-full` 完整包；而完整包目前标记为**公测**，存在「装完进不了系统」的风险。下载前务必核对官网当前的格式列表。

下载链路也有讲究：优先用 **gh-proxy.org 原始加速链接**；酷宅下载点禁止手机访问且有 WAF 限流。格式选对、平台对号入座后，底层刷写/导入动作与官方版完全一致，第二章的方法全部复用。

> [!example] 通过 gh-proxy.org 加速下载
> ```bash
> # 示例，实际完整链接以官网 https://www.hasscn.top/download.html 为准
> wget -c https://gh-proxy.org/<完整下载路径>/haos_generic-x86-64-18.2.img.xz
> 
> # 校验：系统镜像未公布 SHA256，只能对照官方 checksum 手工核对
> # sha256sum haos_generic-x86-64-18.2.img.xz
> ```

> [!warning] 校验和缺口
> 目前**只有刷机程序 `green_factory_CN` 公布了 SHA256**，各系统镜像没有列校验和。你无法像官方版那样先验哈希再刷写——这是完整包风险被放大的另一个原因。

### 5.3 内置加速机制解析

极速版把第四章手动做的那些事全部**内置**了，而且更彻底，共 **8 类网络重定向**：

| 重定向对象 | 目标 | 说明 |
| ---- | ---- | ---- |
| 版本检查 | version.hasscn.top | 绕过 GitHub 慢速/被墙 |
| 连通性检查 | 腾讯 BGP | HTTP 204 |
| NTP 时间 | 阿里 / 腾讯国内源 | 时间同步国内化 |
| 容器镜像 `ghcr.io/home-assistant/*` | ota.hasscn.top | Registry API V2 + CDN |
| OTA 更新 | 腾讯 BGP | 保留 RAUC 签名 + A/B 原子更新 |
| 错误上报 | 腾讯 BGP | — |
| Docker 镜像 | 12 源故障转移 | 见下 |

Docker 镜像层内置 **12 个国内源故障转移链**（优先级从高到低）：

```text
docker.1panel.live → docker.1ms.run → dytt.online → docker-0.unsee.tech
→ lispy.org → docker.xiaogenban1993.com → 666860.xyz → hub.rat.dev
→ docker.m.daocloud.io → demo.52013120.xyz → proxy.vvvv.ee → registry.cyou
→ 全部失败回退 docker.io
```

首个源挂掉约 5–10 秒自动切下一个，正好应对公益镜像「隔天失效」的通病。

实现方式决定了它的双刃剑属性：**构建时硬编码（只读 EROFS）+ 运行时 rootfs-overlay（Docker/NTP 配置）**。好处是配置项不可被误改；坏处是**安装后不可修改、没有关闭开关**——你选了它，就得接受内置的全部重定向。数据目录独立放在 `data-root: /mnt/data/docker`（独立分区），A/B 更新切换系统槽位后镜像仍然保留。

提速数据（来自项目方，建议实测验证）：镜像下载提速 5–10 倍，1Gbps 网络下 Core + Add-on 约 1–1.5 分钟；500MB Core 无镜像 30–120 秒 → 有镜像 5–30 秒；版本检查 20–50ms vs 国际 200–500ms。

### 5.4 安装差异、官方互转与 A/B 分区

**安装差异极小**：底层刷写/导入流程与官方版基本相同（`img.xz` 刷盘、`qcow2` 导入 PVE、`vmdk` 导入 VMware/群晖），唯一差异在首次启动——完整包免初始化等待，在线式仍需联网拉依赖。

**官方版 → 极速版**是最常用的路径，一键 OTA、保留现有配置。前提是先做一次完整备份，且必须用系统终端（不是网页版 Terminal）：

> [!example] 官方版一键转极速版
> ```bash
> login
> curl -fsSL https://ota.hasscn.top/upgrade.sh | bash
> ```

脚本执行后自动重启。重启后分两步验证：

> [!example] OTA 后验证
> ```bash
> # 1) 启动日志确认已切换：出现 "OTA service kindly sponsored by Coolkit" 即为极速版
> # 2) 先看诊断页全绿，再进 Web UI
> curl http://homeassistant.local:4357/    # 4357 = HassOS Observer 诊断状态
> ```

**极速版 → 官方没有 OTA 脚本**：官方只推荐「备份 → 重装官方镜像 → 还原备份」。方向是单向便利——跳进去容易，跳回来要整机重装。

如果 OTA 后系统异常，用 A/B 分区排查——极速版保留了官方 RAUC 的 **A/B 双槽位原子更新**，坏槽可回滚：

> [!example] A/B 槽位排查
> ```bash
> ha os info          # 查看当前 boot: 槽位
> ha os boot-slot A   # 或 ha os boot-slot B，切换到另一槽
> ha host reboot      # 重启生效
> ```

### 5.5 风险清单与使用边界

把接受极速版要付的账一次算清（采集时间 2026-08-06，均以实际官方站为准）：

> [!warning] 风险清单
> 1. **非官方发行版**：端点配置经私有构建脚本注入，公开仓库不可见完整生成过程，信任模型依赖项目方。
> 2. **校验和缺口**：系统镜像未列 SHA256，无法自行验证镜像完整性。
> 3. **版本标注不一致**：ihost、rpi5 两处已确认标注与镜像不符。
> 4. **完整包为公测**：存在「装完进不了系统」风险，生产环境慎用。
> 5. **硬依赖中国大陆网络**：酷宅 OTA 仅限中国 IP，海外节点可能无法更新。
> 6. **第三方源合规风险**：12 个 Docker 镜像源均非官方，有失效与合规不确定性；系统内只能同时存在一个加速方案。

> [!tip] 使用边界建议
> 极速版适合**国内网络环境下的个人折腾、快速起服务**；生产环境先自行评估，务必保留官方镜像与 SHA256 作为备路——哪天公益源失效或信任模型出问题，还能备份重装回到官方原版。

### 本章 Checklist

- [ ] 我能区分 HAOS-CN（开源）与冬瓜 HAOS（闭源）的信任模型差异
- [ ] 我能分清在线式与 `-full` 完整包，并避开公测包进不了系统的坑
- [ ] 我知道极速版 8 类网络重定向与 12 源故障转移的实现方式（只读硬编码 + rootfs-overlay）
- [ ] 我能用 `curl -fsSL https://ota.hasscn.top/upgrade.sh | bash` 从官方版一键转极速版，并用 4357 状态页验证
- [ ] 我知道反向（极速→官方）必须备份重装，且能用 `ha os boot-slot` 排查 A/B 槽
- [ ] 我已确认接受：不可修改、无关闭开关、校验缺口、中国 IP 依赖、第三方源风险，并保留官方备路

第五章把替代路线的底牌全部亮出：内置加速有多省心，风险清单就有多重。看到这里，两条路线的优缺点都已经摆上台面——下一章用一张精简对比表，帮你五分钟锁定选型。

## 第六章：双路线对比与选型建议

> [!summary] 本章讲什么
> 把官方原版（手动国内源）与 [[HAOS-CN]] 极速版放到同一张表里做最终决策。到这里你不缺更多细节，缺的是「我到底该选哪条」。本章给出一张精简对比表、三档场景化建议和迁移与备路策略，帮你五分钟锁定路线。选型（HAOS vs Docker vs Supervised）已在 [[Home Assistant 三种部署方式对比与选型]] 讲透，本章不再重复。

### 6.1 双路线精简对比表

| 维度 | 官方原版 HAOS（手动国内源） | HAOS-CN 极速版 |
| ---- | ---- | ---- |
| 来源 | Home Assistant 官方 | 社区开源再发行（ha-china/HAOS-CN） |
| 国内源 | 需手动配置（Docker / Supervisor / Add-on / NTP / DNS） | 内置（12 Docker 源 + 8 类网络重定向） |
| 首次启动 | ghcr 拉取约 700MB，国内可能数小时 | 在线式数十分钟 / `-full` 完整包即装即用 |
| 可配置性 | 每项源可解释、可掌控 | 安装后不可改、无关闭开关 |
| 完整性校验 | 官方 SHA256 齐全 | 系统镜像无校验和 |
| 信任模型 | 官方背书、可复现 | 依赖项目方与第三方镜像站（WAF / 失效风险） |
| 更新机制 | 官方 OTA（慢） | 国内 OTA（快，A/B 原子更新可回滚） |
| 互转方向 | — | 官方→极速一键 OTA；反向需备份重装 |
| 生产适用性 | 推荐 | 需自行评估，保留官方备路 |

### 6.2 场景化选型建议

> [!tip] 生产求稳 → 官方原版 HAOS + 手动国内源
> 要的是「可解释、可掌控、可回退」：官方 SHA256 校验齐全、更新走官方链路、每一项源都能自己改。代价是首次部署动手多、国内首次启动慢。建议按第四章逐步配置，别走捷径。

> [!tip] 国内折腾 → HAOS-CN 极速版
> 想「装完即用、少操心」：内置加速 + HACS 极速版 + 国内 OTA，个人折腾体验最好。前提是接受不可修改、无校验和、信任项目方这三条。家用服务器、开发测试强烈适合。

> [!tip] 网络受限 → HAOS-CN `-full` 完整包
> 网络差到连 ghcr 那 700MB 都拉不动时，在线式再「官方一致」也没意义。完整包装完即用、免初始化等待。但它是公测版，先验证能进系统，再迁移正式数据。

### 6.3 迁移路径与官方备路策略

迁移是单向便利的：

| 方向 | 方式 | 配置 / 数据 |
| ---- | ---- | ---- |
| 官方 → 极速 | `curl -fsSL https://ota.hasscn.top/upgrade.sh | bash` | 保留，先备份再转 |
| 极速 → 官方 | 备份 → 重装官方镜像 → 还原 | 完整备份即可迁移 |

两条路线通用同一套稳定运行原则（SSD、备份、升级回滚），详见下一章。

> [!warning] 永远保留官方备路
> 公益镜像源隔天失效是常态。无论走哪条路线，都建议：留一份官方镜像 + SHA256、把备份插件（Google Drive）跑起来。哪天公益源整片失效或信任模型出问题，备份重装回官方原版是最后的安全网。

### 本章 Checklist

- [ ] 我能用对比表说出两条路线在信任模型、校验、可配置性上的本质差异
- [ ] 我能按自己场景（生产求稳 / 国内折腾 / 网络受限）锁定选型
- [ ] 我知道迁移是「官方→极速一键、极速→官方重装」的单向便利
- [ ] 我已确认保留官方镜像 + 校验和作为备路

无论你最后选官方原版还是 [[HAOS-CN]] 极速版，两条路线的「稳定运行」共识是相通的。选型定下来之后，下一章进入长期运维主题：怎么用 SSD 终结 TF 卡损坏、怎么用备份兜底、怎么敢升级还能回滚。

## 第七章 稳定运行保障——存储、备份与升级

> [!summary]
> 本章解决「装好之后怎么不坏」的问题：为什么 TF 卡必坏、怎么无损迁到 SSD；怎么用 Google Drive 做世代备份并落实 3-2-1 规则；升级与回滚的机制和命令，让你敢升级、能回滚。全文命令与参数来自深度研究素材 §四，采集时间 2026-08-06。

### 7.1 SSD 迁移：终结 TF 卡损坏

#### 7.1.1 根因：写入强度与介质不匹配

把 [[HAOS]] 部署在树莓派 / TF 卡上"几个月就坏"不是偶然。HA 的数据库日常写入强度大约在 **15 次/秒**，这个量级远超 microSD 闪存的擦写寿命设计——SD 卡本身没有坏，是负载与介质不匹配。

> [!warning] 这不是质量问题
> TF 卡损坏是"介质选错"的必然结果，不是卡的质量问题。换更贵的卡只能延后损坏，不能根治。凡是长期运行 HA 的主机，存储都应该落在 SSD 上。

#### 7.1.2 按平台选型

| 平台 | 推荐方案 | 说明 |
|------|----------|------|
| Raspberry Pi 4 及更早 | SATA SSD + USB3.0 硬盘盒 | USB3.0 带宽足够，优先选支持 UASP 的硬盘盒 |
| Raspberry Pi 5 | PCIe NVMe | Pi5 的 PCIe 接口可直连 NVMe 盘 |
| 迷你主机 / NUC | 内置 SATA / NVMe | 直接占用机箱内硬盘位，无需外接 |

容量不用大：HA 本体 + 数据库 + 备份，128–256GB 绰绰有余；后期若数据库膨胀，可按第八章迁移到 MariaDB 或换更大的 SSD。

#### 7.1.3 迁移三步：备份 → 写 SSD → 恢复

迁移的核心思路是把系统整体搬过去，而不是重装。步骤如下：

1. 在旧系统上做一次完整备份（见 7.2，这一步是安全网）。
2. 用官方 `img.xz` 镜像写入新 SSD（方法与第二章相同：balenaEtcher 或 Ubuntu Disks）。
3. 用 SSD 引导启动，首次初始化完成后，从备份恢复。

> [!tip] 顺序别反
> 先备份、再写盘、后恢复。若跳过备份直接写 SSD，等于丢掉了全部配置与自动化历史。

### 7.2 备份策略：Google Drive 世代备份与 3-2-1 规则

#### 7.2.1 Google Drive 备份插件

官方推荐路线是 `hassio-google-drive-backup` 插件：定时把 HAOS 完整备份上传到你的 Google Drive，支持加密，OAuth 只申请 `drive.file` 权限（应用只能读写自己创建的备份目录，目录固定为 "Home Assistant Backups"）。

核心是**世代保留**策略：不只留最近 N 份，而是同时按天/周/月/年各留几份，避免"今天备份把昨天唯一一份顶掉"的尴尬。一份参考配置（加载项 → Google Drive Backup → 配置）：

```json
{
  "days_between_backups": 1,
  "max_backups_in_drive": 24,
  "generational_days": 3,
  "generational_weeks": 4,
  "generational_months": 12,
  "generational_years": 5
}
```

- `days_between_backups: 1`：每天备份一次；
- `max_backups_in_drive: 24`：Drive 里最多保留 24 份；
- `generational_days/weeks/months/years`：分别保留最近 3 天、4 周、12 个月、5 年的世代副本。

> [!tip] 加密可选但推荐
> 备份里包含摄像头录像、门锁日志等家庭隐私。插件支持设置加密密码，建议开启，恢复时输入同一密码即可。

#### 7.2.2 3-2-1 规则

生产环境建议遵守 3-2-1 规则：

| 规则 | 含义 | 在本项目中的落地 |
|------|------|------------------|
| 3 | 保留 3 份数据副本 | 本机 + 外接 SSD + 云盘 |
| 2 | 使用 2 种不同介质 | 本机 SSD + Google Drive 云盘 |
| 1 | 至少 1 份异地 | Google Drive（不在家） |

Google Drive 插件天然满足"异地 + 不同介质"两项；再配合本机一份，就齐了。

#### 7.2.3 升级前自动快照

每次升级 Core / Supervisor / 加载项前，[[HAOS]] 会自动生成一个快照作为回滚点。这是升级的安全网——不要把升级当成"赌一把"，要当成"先存档再动手"。

#### 7.2.4 恢复三场景

| 场景 | 操作 |
|------|------|
| 插件可用 | 设置 → 系统 → 备份 → 选择备份 → 还原（Load into HA） |
| 全新安装 | 创建用户之前上传备份，按向导还原 |
| 已装好 HA | 用 Samba / File Editor 把备份拷入 `/backup` 目录，再在界面还原 |

> [!warning] 全新安装的坑
> 如果是重装后恢复，必须在**创建用户之前**上传备份；一旦先建了用户，还原时可能因凭据冲突走弯路。

### 7.3 升级与回滚：机制、命令与策略

#### 7.3.1 自动回滚机制

Core 升级时若超时或崩溃，Supervisor 会自动回滚到上一个可用版本，回滚日志在：

```text
/config/home-assistant-rollback.log
```

常见的回滚触发原因：

- 启动超时（`STARTUP_API_RESPONSE_TIMEOUT` 默认 3 → 5 → 10 分钟递增，可调大）；
- 配置或自定义集成崩溃（例如集成 `unique_id` 不是字符串）；
- 跨大版本跳升（跳过中间大版本直接升到最新）。

#### 7.3.2 常用命令

SSH 进 HAOS 终端（root 端口 22222）后，用 `ha` CLI 操作：

```bash
# 排查并修复 Supervisor 状态
ha supervisor repair

# 强制指定 Core 版本升级
ha core update --version X

# 重启 Core（注意：正确重启走「设置 → 系统 → 硬件」，见第八章）
ha core restart
```

> [!example] 命令用途
> `ha supervisor repair` 用于修复损坏的 Supervisor；`ha core update --version X` 用于把 Core 钉到指定版本——既可以把"最新版"退回来，也可以在跨大版本升级时逐版本前进。

#### 7.3.3 升级策略

建议**逐大版本升级，且每步先备份**：

1. 升级前确认 7.2 的备份已成功、Drive 里能查到最新备份；
2. 只升一个主版本，观察运行稳定后再升下一个；
3. 若回滚，用 `ha core update --version X` 回到上一版，或用备份还原。

#### 7.3.4 一个关键区分：Supervisor 更新不随 Core 回滚

`ha core update` 只影响 Core。Supervisor（supervisor）是独立组件，它的更新**不会**因为 Core 回滚而一起回滚——这意味着如果这次升级既动了 Core 又动了 Supervisor，回滚 Core 后 Supervisor 仍是新版本。排查问题时别漏掉这一层。

> [!warning] 回滚边界
> Core 回滚 ≠ 整体回滚。Supervisor 与 OS 各自的更新互相独立，出问题时先看 `/config/home-assistant-rollback.log` 和 Supervisor 日志，分清是哪一层在报错。

### 本章 Checklist

- [ ] 已理解 TF 卡损坏根因是 15 次写入/秒的负载与介质不匹配
- [ ] 已按平台选好 SSD（Pi4 → USB SATA / Pi5 → PCIe NVMe / 迷你主机 → 内置盘）
- [ ] 已完成一次「备份 → 写 SSD → 恢复」迁移
- [ ] 已配置 Google Drive 备份插件，设置世代保留参数
- [ ] 已按 3-2-1 规则确认本机 + 云盘至少两份备份
- [ ] 已确认升级前自动快照可用，并知道 `/config/home-assistant-rollback.log` 路径
- [ ] 已记住 `ha supervisor repair` 与 `ha core update --version X` 用法
- [ ] 已了解 Supervisor 更新不随 Core 回滚

存储、备份、升级都安排妥当之后，剩下的是运行时躲不开的意外。第八章把错误码速查、端口诊断、时间排障、远程访问方案与长期运维清单一次打包，遇到问题按图索骥即可。

## 第八章 故障排查手册与长期运维

> [!summary]
> 本章是排障手册 + 运维清单：错误码 1001–1005 与数据库 `.recover` 重建、8123 / 8124 / 4357 端口与正确重启方式、时区与 NTP 判别、四种国内远程访问方案对比，以及每周 / 每月的长期检查清单。命令与参数来自深度研究素材 §四，采集时间 2026-08-06。

### 8.1 错误码速查与数据库修复

#### 8.1.1 错误码速查

> [!warning] 来源说明
> 下表为社区博客整理，以实际系统日志与官方文档为准（采集时间 2026-08-06）。

| 错误码 | 含义 | 常见处理 |
|--------|------|----------|
| 1001 | 网络接口错误 | 检查网卡是否识别、接口名是否正确 |
| 1002 | 依赖工具缺失 | 补装 / 修复依赖，重跑安装校验 |
| 1003 | 启动失败 | 查看 `journalctl` 与启动日志定位崩溃点 |
| 1004 | 数据库不存在 | 检查数据库文件是否丢失 / 被误删，必要时重建 |
| 1005 | 配置文件格式错误 | 校验 YAML 缩进与类型，回滚最近改动 |

#### 8.1.2 无 IP 问题

断电重启后 [[HAOS]] 常比 DHCP 先启动，接口不再重试就"拿不到 IP"。社区解法是手动把接口切回自动获取：

```bash
network update enp1s0 --ipv4-method auto
```

> [!tip] 建议静态 IP
> 给 [[HAOS]] 配固定 IP（路由器 DHCP 绑定或静态配置），既避免断电后无 IP，也让远程访问、自动化回调更稳定。

#### 8.1.3 数据库损坏与 .recover 重建

HA 长期高频写入（尤其装在 TF 卡 / 异常断电）可能让 SQLite 数据库损坏。用 SQLite 自带的 `.recover` 把数据恢复到新库：

```bash
# 先按 8.2 的"正确重启"停掉 HA，再在配置目录执行
sqlite3 database.sqlite3 ".recover" | sqlite3 new.db
mv database.sqlite3 database.sqlite3.bak
mv new.db database.sqlite3
```

若重建后仍频繁出问题：把数据库迁移到 MariaDB，或确认存储已迁到 SSD（见第七章）。

> [!warning] 非正常断电是主要诱因
> 数据库损坏多来自直接断电。[[HAOS]] 里"正确重启"必须走界面，而不是拔电或硬关机。

### 8.2 端口、诊断通道与正确重启

#### 8.2.1 三个端口各管什么

| 端口 | 归属 | 用途 |
|------|------|------|
| 8123 | Core / Web UI | 日常访问的仪表盘 |
| 8124 | Supervisor API | Supervisor 管理接口 |
| 4357 | HassOS Observer | 系统级诊断，Core 起不来时也能用 |

Core 完全起不来、8123 打不开时，用 4357 通道确认系统状态：

```bash
curl http://homeassistant.local:4357/
```

返回系统健康信息，能帮你区分"是 Core 崩了"还是"整个系统起不来"。

#### 8.2.2 正确重启

[[HAOS]] 的"正确重启"路径是：**设置 → 系统 → 硬件**，从界面触发重启 / 关机。走界面等于通知各组件优雅退出，数据库落盘后再断电。

> [!warning] 别拔电
> 直接断电十有八九会留下损坏的 SQLite 数据库。真遇到"卡死"需要强制重启，重启后第一件事是跑 8.1.3 的 `.recover` 检查。

### 8.3 时间同步排障

时间错乱会让 HTTPS 证书校验失败、自动化不触发、更新拉不下来。先看状态：

```bash
timedatectl
```

看 `System clock synchronized: yes` 即为成功。时间不对时，先判别是时区还是 NTP：

| 现象 | 根因 | 处理 |
|------|------|------|
| 差整 8 小时 | 时区未设 | 设置时区（Asia/Shanghai） |
| 差几分钟且持续增大 | NTP 同步失败 | 检查 NTP 源连通、配置国内源 |

国内 NTP 源（配置方法见第四章 `/etc/systemd/timesyncd.conf`）：`ntp1~7.aliyun.com`、`ntp.tencent.com`、`ntp.ntsc.ac.cn`、`cn.pool.ntp.org`。容器环境用 chrony 加载项，把 `ntp_pool` 改成 `cn.pool.ntp.org`。

> [!tip] 时间是一切更新的前提
> 证书、自动化、OTA 全依赖准确时间。NTP 国内化是"稳定"的隐性基础，别只当小事。

### 8.4 国内远程访问方案对比

| 方案 | 前提条件 | 优点 | 注意点 |
|------|----------|------|--------|
| Tailscale | 无 | 官方插件、零配置、个人首选 | 访问地址形如 `.ts.net:8123` |
| Cloudflare Tunnel | 自有域名 | 无需公网 IP、可叠加访问控制 | 国内部分地区被污染，需先测连通 |
| FRP | 一台公网 VPS | 可控性强、性能好 | 需要维护 VPS |
| 公网 IP + Nginx 反代 | 运营商给公网 IP | 最直接 | 勿裸映射 8123，务必套 Nginx 反代 + HTTPS |

> [!warning] 勿裸映射 8123
> 把 8123 直接端口映射到公网等于裸奔，会招来扫描与爆破。即使走"公网 IP + 端口映射"，也必须用 Nginx 反代加 HTTPS、加访问鉴权。

### 8.5 长期运维检查清单

#### 每周

- [ ] 打开 [[HAOS]] 界面，确认 Core / Supervisor 运行正常
- [ ] 检查 Google Drive 里最新备份时间戳（应不早于 2 天）
- [ ] 看 `/config/home-assistant-rollback.log` 有无意外回滚记录
- [ ] `timedatectl` 确认时间同步正常

#### 每月

- [ ] 确认可用性：`curl http://homeassistant.local:4357/` 返回正常
- [ ] 清点备份：按世代保留策略清理过期备份
- [ ] 检查更新：Core / Supervisor / 加载项是否有待升级，按 7.3 策略逐版本升级
- [ ] 检查国内源是否仍有效（Docker 公益镜像站失效常见，失效则按第四章更换源）

> [!warning] 公益镜像源会"隔天失效"
> Docker 公益镜像站失效非常常见。平时多配几个源（第四章 12 源故障转移链），并在每月清单里实际验证一次 `docker info` 的 Registry Mirrors 是否命中。

### 本章 Checklist

- [ ] 能识别 1001–1005 错误码并知道大致方向
- [ ] 遇到无 IP 会跑 `network update enp1s0 --ipv4-method auto`
- [ ] 数据库损坏时会用 `.recover` 重建
- [ ] 知道 8123 / 8124 / 4357 三个端口各管什么
- [ ] 重启只走「设置 → 系统 → 硬件」，不拔电
- [ ] 时间不对能判别是时区还是 NTP
- [ ] 已选定远程访问方案（Tailscale / Cloudflare Tunnel / FRP / Nginx 反代）
- [ ] 已建立每周 + 每月运维清单节奏

---

## 结语

到这里，一条「安装 → 加速 → 对比 → 稳定 → 排障」的完整主线就走通了：第二章把平台、存储、固件、镜像和工具链一次备齐；第三章在实体机与 VMware / PVE / 群晖 VMM 上把官方原版跑起来；第四章为官方原版配齐 Docker、Supervisor、Add-on、NTP 四层国内加速；第五章给出内置加速的 [[HAOS-CN]] 极速版作为省心替代；第六章用对比表完成选型；第七章落定 SSD、备份、升级回滚的稳定运行策略；第八章则把错误码、时间排障、远程访问与运维清单备好待查。

最后重申三点：第一，公益镜像源「隔天失效」是常态，多源 + 故障转移 + 每月巡检比依赖单一镜像站可靠；第二，无论走哪条路线，都请保留官方镜像 + SHA256 与一份云端备份作为安全网；第三，文中所有镜像站地址、版本号、错误码均以实际官网/日志为准（采集时间 2026-08-06）。祝你部署顺利，HA 稳定运行。
