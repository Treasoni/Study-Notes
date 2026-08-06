# Home Assistant 部署方式对比 - 探测结果

收集时间: 2026-08-05

## 探测概要

针对三种部署方式（HAOS VM、Docker Container、HA Supervised）并行派出 3 个 subagent 探测，共获取 18 条高相关资料（官方文档 7 条、社区 6 条、博客 4 条、新闻 1 条）。

## 关键发现

### 1. HAOS 虚拟机（官方推荐）
- **本质**: 专为 Home Assistant 设计的嵌入式极简操作系统，内含 Core + Supervisor
- **特性**: Supervisor 负责 Add-on 商店、快照备份、约每 8 小时检查并自动更新 OS/内核
- **镜像格式**: qcow2(KVM/Proxmox)、vdi(VirtualBox)、vmdk(VMware)、vhdx(Hyper-V)、ova
- **硬件要求**: 最低 2GB RAM / 2 vCPU / 32GB 磁盘，推荐 4GB；必须启用 UEFI/OVMF
- **优点**: 刷完即用、全托管、一键备份、Add-on 生态完整
- **缺点**: 只读文件系统、无 apt、独占整机、无法运行其他服务、排障困难

### 2. Docker Container（纯 Core）
- **本质**: 仅运行 Home Assistant Core 容器，无 Supervisor、无 Add-on、无 OTA 自动更新
- **关键配置**: `--privileged`、`--network=host`（保 mDNS/蓝牙发现）、挂载 `/config`、`--device` 直通 USB（Zigbee/Z-Wave）
- **要求**: Docker Engine ≥23.0.0；Docker Desktop 不可用
- **优点**: 最灵活、资源占用低（空闲约 300-400MB RAM）、可与其他容器共存（NAS/VPS）
- **缺点**: 无 Add-on 生态、备份/反代/更新全手动、需 Docker 技能
- **风险**: 与 Supervised 共存时可能出现 systemd-resolved 端口 53、CGroup 冲突

### 3. HA Supervised（已弃用）
- **本质**: 在现有 Linux（仅官方支持 Debian 11+，不接受衍生版）上安装 Supervisor + Core
- **要求**: Docker CE ≥19.03、Systemd ≥239、NetworkManager ≥1.18.0、Avahi、AppArmor；安装器会校验 OS
- **优点**: 兼具 Add-on 与宿主 OS 控制权
- **缺点**: 维护负担大、易被判 Unsupported/Unhealthy、官方仅支持 Debian
- **⚠️ 重要时效性**: 官方 2025-05 公告弃用 Core/Supervised 方式，2025.6 起推送迁移通知，2025.12 后停止官方支持（Supervised 使用率约 3.3%），推荐迁移到 HAOS 或 Container

### 4. 对比要点
| 维度 | HAOS VM | Docker Container | Supervised |
|------|---------|-----------------|------------|
| 含 Supervisor | ✅ | ❌ | ✅ |
| Add-on 商店 | ✅ | ❌ | ✅ |
| 自动更新 (OS/Core) | ✅ | ❌（手动 pull） | 部分 |
| 托管快照备份 | ✅ | ❌ | ❌ |
| 可与其他服务共存 | ❌ 独占 | ✅ | ⚠️ 会被标记 Unsupported |
| 官方支持状态 | 推荐 | 支持 | 已弃用（2025.12 停止） |
| 资源占用 | 2-4GB | ~300-400MB | 视宿主 |
| 维护难度 | 低 | 中（需 Docker 技能） | 高 |

## 参考信源（高相关 Top 8）
1. 官方安装指南: https://www.home-assistant.io/installation/
2. 官方 Linux/VM 安装: https://www.home-assistant.io/installation/linux
3. HAOS 官方镜像发布: https://github.com/home-assistant/operating-system/releases
4. 社区安装方式详解: https://community.home-assistant.io/t/installation-options-explained/835564
5. ADR-0014 Supervised 架构决策: https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md
6. 官方弃用公告: https://community.home-assistant.io/t/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/893617
7. supervised-installer 仓库: https://github.com/home-assistant/supervised-installer
8. Proxmox HAOS 部署: https://mintlify.wiki/community-scripts/ProxmoxVE/guides/home-assistant

## 建议方向

主题本身明确（三方式对比），建议按「对比 + 实战」展开，方向菜单见用户确认。
