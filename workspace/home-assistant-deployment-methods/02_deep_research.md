# Home Assistant 部署方式对比 - 深度素材

收集时间: 2026-08-05
方向: 侧重选型决策（对比表+决策树为主线，部署步骤作附录）

## 素材质量概览

- 官方文档精读: 4 条（installation/、installation/linux、ADR-0014、supervised-installer）
- 社区精读: 3 条（installation options explained、官方弃用公告、Pi Supervised 指南）
- 实操精读: 2 条（Proxmox HAOS 部署、Docker compose 官方模板）
- 综合: 官方口径一致，且有关键纠偏（ADR-0014 已 revert；Supervised/Core 已于 2025.12 弃用）

---

## 一、三种方式深度精读

### 1. HAOS 虚拟机（Home Assistant Operating System）

**官方定义与定位**
- 专为 HA 设计的嵌入式极简操作系统，内含 Core + Supervisor，官方定义为"recommended installation type for most users"，理由是最省心（most convenient）
- 官方安装方式分类中正式只有两种：**HA OS** 和 **Container**（Supervised 已不算正式推荐路径）

**特性**
- Supervisor 负责 Add-on 商店、快照备份、约每 8 小时检查并自动更新 OS/内核/Supervisor
- Add-on 本质是 Supervisor 托管的 Docker 容器
- 只读文件系统、无 apt、独占整机

**虚拟机部署要求（官方）**
- 最低 2GB RAM / 2 vCPU / 32GB 磁盘，推荐 4GB
- 必须启用 UEFI（VirtualBox 勾 Use EFI；KVM 用非 secureboot 的 OVMF 固件）
- 镜像格式: qcow2(KVM/Proxmox)、vdi(VirtualBox)、vmdk(VMware)、vhdx(Hyper-V)、ova；命名 `haos_ova-{version}`，需解压
- 入口地址: `homeassistant.local:8123`

**Proxmox 推荐配置（社区实践）**
| 项 | 推荐 |
|---|---|
| 机型 | q35 |
| BIOS | UEFI（EFI 盘） |
| 存储控制器 | virtio-scsi-pci |
| 磁盘 | 32GB（可 `qm resize` 扩） |
| CPU | kvm64 2 核（可迁移）/ host（性能最好不可迁移） |
| 内存 | 4096MB（可用 `-balloon 2048` 内存气球） |
| 网络 | vmbr0 |

```bash
# 一键脚本
bash -c "$(wget -qO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/haos-vm.sh)"
# USB 直通（先 stop VM，用 lsusb 查 vendor:product）
qm set <VMID> -usb0 host=10c4:ea60
qm stop <VMID> && qm start <VMID>
# 备份（snapshot 模式 + zstd）
vzdump <VMID> --mode snapshot --compress zstd --storage local
# 扩容
qm resize <VMID> scsi0 +32G
```

**优点**: 刷完即用、全托管、一键快照备份、Add-on 生态完整、更新无需操心
**缺点**: 只读文件系统、无 apt、独占整机（无法跑其他服务）、排障困难、资源开销大
**适用**: 专用智能家居设备、想要零维护、能接受独占一台机器

### 2. Docker Container（仅 Core）

**官方定义**
- 自带系统（Linux）+ Docker 编排，只运行 Home Assistant Core，**无 Supervisor、无 Add-on、无 OTA 自动更新**
- 部分集成（Thread、Z-Wave）由 Add-on 控制，Container 方式开箱即不支持
- 要求 Docker Engine ≥ 23.0.0，**Docker Desktop 不可用**

**官方 compose 模板**
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

**升级方式**: `docker pull ghcr.io/home-assistant/home-assistant:stable` → stop/rm → 用相同参数重新 run（compose 则 `docker compose pull && docker compose up -d`）

**常见坑**
- 无 `ports:` 段（host 网络）；`--network=host` 保证 mDNS/蓝牙发现
- 部分 ARM64 SoC 页大小 >4K 需 `-e DISABLE_JEMALLOC=true`（报错 `<jemalloc>: Unsupported system page size`）
- 确保容器用户有权限访问 `/dev/tty*`
- 防火墙放行: `sudo ufw allow 8123/tcp`

**优点**: 最灵活、资源占用低（空闲约 300-400MB）、可与其他容器共存（NAS/VPS）、崩溃不影响宿主
**缺点**: 无 Add-on 生态、备份/反代/更新全手动、需 Docker 技能
**适用**: 已有 Docker 主机/NAS 用户、想与其他服务共存、能接受手动维护

### 3. HA Supervised（官方已弃用）

**定义（ADR-0014，注意已 revert）**
- 在现有 Linux 上安装 Supervisor + Core，使用完整 HA 组件除 HA OS 外
- **ADR-0014 状态已标记 reverted**：官方确认 Supervised 不再是被官方支持的安装方式
- 官方定位: "only for advanced users"（精通 Linux/Docker/网络），维护难度 Expert

**官方支持约束（历史定义）**
- 唯一支持主机 OS: **Debian 12 Bookworm，不接受任何衍生版**（Raspberry Pi OS、Ubuntu 都会被安装器拦截）
- 依赖: Docker CE ≥20.10.17、systemd ≥239、NetworkManager ≥1.14.6、udisks2 ≥2.8、AppArmor、cgroup v1、overlayfs2、journald
- 宿主必须"专用于 HA"，不得安装额外软件（几乎任何改动都可能让系统变 Unsupported/Unhealthy）
- 社区指南中存在绕过 OS 检查的环境变量（如 BYPASS_OS_CHECK），但会导致 Unsupported/Unhealthy 状态，官方不负责

**安装脚本步骤（supervised-installer 仓库）**
```bash
# 1. 装 network-manager + systemd-resolved（会切网络服务，IP 可能变化）
# 2. 装 curl、udisks2
curl -fsSL get.docker.com | sh
# 3. 装 OS-Agent（os-agent_*_linux_*.deb）
# 4. 下载 homeassistant-supervised.deb 并 dpkg -i 安装
```
- 数据目录默认 `/var/lib/homeassistant`（可用 `DATA_SHARE` 自定义）
- 支持机型: generic-x86-64、qemux86-64、qemuarm-64、odroid-c2/c4/n2、khadas-vim3、raspberrypi3-64/4-64/5-64

**优点**: 兼具 Add-on 与宿主 OS 控制权
**缺点**: 安装繁琐、维护成本高、易被判 Unsupported/Unhealthy、官方仅支持 Debian、已弃用
**适用**: 基本不推荐新用户选择；仅在需要 Add-ons 又要宿主控制权时作为过渡

---

## 二、选型与迁移（官方权威依据）

### 官方弃用时间线
| 时间 | 事件 |
|------|------|
| 2025-05-22 | 官方公告弃用 Core 和 Supervised 安装方式及 32 位系统 |
| 2025.6 版本起 | 受影响系统更新后显示"支持将在六个月后结束"通知 |
| 2025.12 版本 | **官方支持终止**（supervised-installer 顶部同样标注"unsupported with HA OS 2025.12.0"） |

### 关键数据
- 使用率: Core 约 2.5%、Supervised 约 3.3%、i386/armhf <0.5%、armv7 约 0.95%（其中过半实际支持 64 位）
- 弃用后仍可继续使用和更新 Core/Supervised，但官方不再接受问题报告，端用户文档移除

### 官方推荐迁移路径
- **Core 用户** → 首选 Container（若独占设备则 HAOS）
- **Supervised 用户** → 推荐 HAOS（需要宿主控制权时可在 Proxmox 等 VM 中跑 HAOS，或改用 Container）
- **32 位设备** → 装 64 位系统后恢复备份即可保留硬件

### 迁移方式（官方原话要点）
> "Switching systems is as easy as making a backup, downloading it, and restoring it during the initialization of your new system"
- 任意安装方式之间、**甚至跨架构**都能恢复备份
- Home Assistant Cloud 订阅用户异地备份可凭密码恢复

### 社区选型共识
- 多数老用户在 Proxmox 上用 HAOS VM；杂项服务用独立 LXC/VM 跑，不塞进 HA
- Supervised 在社区公认 "less supported (and liked)"，处于受支持边缘地带，选它需自负维护责任
- 有 Docker 基础且排斥 VM 的用户才选 Container

---

## 三、对比表（核心产出）

| 维度 | HAOS VM | Docker Container | HA Supervised |
|------|---------|-----------------|---------------|
| 官方定位 | ✅ 推荐（most users） | ✅ 支持 | ⚠️ 已弃用（2025.12 终止） |
| 含 Supervisor | ✅ | ❌ | ✅ |
| Add-on 商店 | ✅ | ❌ | ✅ |
| 自动更新 OS/Core | ✅（约每 8h 检查） | ❌（手动 pull） | 部分（Supervisor 停更） |
| 托管快照备份 | ✅ | ❌ | ❌ |
| Thread/Z-Wave 集成 | ✅（Add-on） | ❌ 开箱不支持 | ✅ |
| 可与其他服务共存 | ❌ 独占 | ✅ | ⚠️ 会被标记 Unsupported |
| 资源占用 | 2-4GB（推荐 4GB） | ~300-400MB | 视宿主 |
| 维护难度 | 低 | 中（需 Docker 技能） | 高（Expert） |
| 底层系统 | 只读嵌入式 OS | 自己管理的 Linux | 必须 Debian（无衍生版） |
| 更新方式 | Supervisor 自动 | docker pull 重建 | Supervisor（已停更） |

## 四、选型决策树（草案）

```
想省心、功能完整、愿意独占一台设备？
├── 是 → HAOS（虚拟机或专用硬件）
│        ├── 有 Proxmox/VM 环境 → HAOS VM（推荐）
│        └── 有专用硬件 → HAOS 直接刷机
└── 否 → 已有 Docker 主机 / 想与其他服务共存？
         ├── 是 → Docker Container（需自行维护 Add-on/备份/更新）
         └── 否 → Supervised？（不推荐：已弃用、仅 Debian、维护成本高）
                  → 除非必须保留 Add-on 又要宿主控制权，否则选 HAOS
```

## 五、关键纠偏点（写笔记时注意）

1. **ADR-0014 已 revert**：网上的 Supervised 教程很多是过时的，官方已撤销其正式支持
2. **Supervised/Core 已弃用**（2025.12 终止）："三选一"实际应写成"官方两条路径 + 一条弃用中的旧路径"
3. **Supervised 仅支持 Debian 无衍生版**：树莓派必须刷纯 Debian 12，Raspberry Pi OS/Ubuntu 会被安装器拦截
4. **Container 无 Add-on/Thread/Z-Wave**：这是它与 HAOS 最核心的功能差异
5. **不要臆造细节**：如 BYPASS_OS_CHECK 属于社区流传，官方文档不背书，写时标注来源
