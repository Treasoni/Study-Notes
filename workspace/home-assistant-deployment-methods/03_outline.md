# 学习笔记大纲：《Home Assistant 三种部署方式对比与选型》

> 笔记类型：对比 + 实战指南（practice + compare 混合，侧重选型决策）
> 预计总篇幅：约 25,000 字
> 章节数：8（含 1 个附录）
> 素材引用说明：文中「素材 §X.Y」指向 `02_deep_research.md` 的对应小节（如 §一.1 = HAOS 虚拟机、§三 = 对比表）

---

## 第一章：三种部署方式全景

> **篇幅**：中（约 2,500 字）
> **覆盖要点**：Core/Supervisor/OS/Add-on 概念关系、官方对三种方式的定位、官方"两条正式路径"分类、ADR-0014 已 revert 纠偏、弃用时间线总览
> **素材引用**：素材 §一、§五
> **代码示例**：无

### 1.1 核心概念澄清
- 什么是 Home Assistant Core：HA 主程序本体，可在容器或操作系统中运行
- 什么是 Supervisor：负责 Add-on 商店、快照备份、自动更新的"管家"，本质是容器管理器
- 什么是 HAOS：专为 HA 设计的嵌入式极简 Linux（只读文件系统），内建 Core + Supervisor
- 什么是 Add-on：Supervisor 托管的 Docker 容器（如 Thread、Z-Wave、ESPHome），非官方仓库也有第三方源
- 各概念之间的包含关系与运行形态差异

### 1.2 官方对三种方式的定位
- HAOS：官方明确为"recommended installation type for most users"，理由是最省心（most convenient）
- Docker Container：官方支持但仅限 Core，无 Supervisor/Add-on
- HA Supervised：官方历史上标注"only for advanced users"，现已弃用

### 1.3 官方安装分类：只有两条正式路径
- 官方安装文档中正式分类只有 HAOS 和 Container 两种
- Supervised 已不在官方正式推荐路径之列，网上"三选一"的说法已过时
- 这对后续章节阅读的指引作用

### 1.4 关键纠偏：先破除过期认知
- ADR-0014 状态已 revert：网上大量 Supervised 教程基于已撤销的正式支持
- Supervised / Core 弃用时间线（2025-05 公告 → 2025.12 官方支持终止）
- 阅读本文时的正确视角："官方两条路径 + 一条弃用中的旧路径"

---

## 第二章：核心对比表

> **篇幅**：中（约 2,000 字，以表格为主）
> **覆盖要点**：十维对比总表、功能完整性 vs 灵活性权衡轴、决策关键差异速查
> **素材引用**：素材 §三
> **代码示例**：无

### 2.1 十维对比总表
- 官方定位、是否含 Supervisor、Add-on 商店、自动更新、托管快照备份、Thread/Z-Wave 支持、是否可与其他服务共存、资源占用、维护难度、底层系统、更新方式
- 表格独立段落呈现（Obsidian 规范：表格不嵌套列表）

### 2.2 最核心差异：功能完整性 vs 灵活性
- HAOS 端：功能完整、零维护，但独占整机、只读系统、无法跑其他服务
- Container 端：轻量灵活、可共存，但无 Add-on、备份/反代/更新全手动
- Supervised 端：理论上兼得，实际因弃用 + 严格宿主约束而不推荐
- 两条权衡轴（功能完整 ↔ 手动可控；省心 ↔ 资源占用）如何交叉

### 2.3 决策关键差异速查
- "无 Add-on / 无 Thread / 无 Z-Wave / 无自动更新"是 Container 与 HAOS 之间最核心的功能差异
- 资源占用量级对比（HAOS 推荐 4GB vs Container 空闲约 300-400MB）
- 维护成本阶梯（低 / 中 / 高）

---

## 第三章：HAOS 虚拟机详解

> **篇幅**：长（约 4,500 字）
> **覆盖要点**：HAOS 定位与推荐理由、虚拟机部署要求、Supervisor 机制、Proxmox 推荐配置、优缺点与适用场景
> **素材引用**：素材 §一.1
> **代码示例**：有（Proxmox 一键脚本、USB 直通、备份、扩容）

### 3.1 是什么：为 HA 定制的嵌入式操作系统
- 只读文件系统、无 apt、独占整机
- 内含 Core + Supervisor 的完整组合

### 3.2 官方为什么推荐
- 刷完即用、全托管体验
- Supervisor 负责 Add-on 商店、快照备份、约每 8 小时自动更新 OS/内核/Supervisor

### 3.3 虚拟机部署要求（官方）
- 最低 2GB RAM / 2 vCPU / 32GB 磁盘，推荐 4GB
- 必须启用 UEFI（VirtualBox 勾 Use EFI；KVM 用非 secureboot 的 OVMF 固件）
- 镜像格式：qcow2 / vdi / vmdk / vhdx / ova，命名 `haos_ova-{version}`，需解压
- 入口地址 `homeassistant.local:8123`

### 3.4 Supervisor 机制拆解
- Add-on 本质是 Supervisor 托管的 Docker 容器
- 快照备份与一键还原
- OTA 式自动更新链路

### 3.5 Proxmox 推荐配置（社区实践）
- 机型 q35、BIOS UEFI（EFI 盘）、virtio-scsi-pci、32GB 磁盘
- CPU kvm64（可迁移）/ host（性能最好）、内存 4096MB + 内存气球
- 实操命令：一键脚本、USB 直通、vzdump 快照备份、qm resize 扩容

### 3.6 优点 / 缺点 / 适用场景
- 优点：零维护、Add-on 生态完整、一键快照备份、更新省心
- 缺点：只读系统、无 apt、独占整机、排障困难、资源开销大
- 适用：专用智能家居设备、想要零维护、能接受独占一台机器

---

## 第四章：Docker Container 详解

> **篇幅**：长（约 4,000 字）
> **覆盖要点**：Container 定位、官方 compose 模板拆解、升级与维护、常见坑、优缺点与适用场景
> **素材引用**：素材 §一.2
> **代码示例**：有（官方 compose 模板、升级命令）

### 4.1 是什么：仅 Core 的容器方式
- 自带系统 + Docker 编排，只运行 Home Assistant Core
- 无 Supervisor、无 Add-on、无 OTA 自动更新
- 要求 Docker Engine ≥ 23.0.0，Docker Desktop 不可用

### 4.2 官方 compose 模板逐行拆解
- 镜像 ghcr.io/home-assistant/home-assistant:stable
- 关键 volume：/config、/etc/localtime、/run/dbus（蓝牙必需）
- privileged、network_mode: host 的含义与必要性
- devices 设备直通（Zigbee / Z-Wave USB 适配器）
- 为什么没有 ports 段（host 网络保证 mDNS/蓝牙发现）

### 4.3 升级与维护流程
- 手动拉取新镜像重建容器：`docker pull` → stop/rm → 同参数重新 run
- compose 方式：`docker compose pull && docker compose up -d`
- 手动备份 /config、手动反代配置

### 4.4 常见坑
- ARM64 SoC 页大小 >4K 需 `-e DISABLE_JEMALLOC=true`（报错 `<jemalloc>: Unsupported system page size`）
- 确保容器用户有权限访问 /dev/tty*
- 防火墙放行 `sudo ufw allow 8123/tcp`
- 蓝牙 / mDNS 发现依赖 host 网络，别轻易改成 bridge

### 4.5 优点 / 缺点 / 适用场景
- 优点：最灵活、资源占用低（空闲约 300-400MB）、可与其他容器共存（NAS/VPS）、崩溃不影响宿主
- 缺点：无 Add-on 生态、备份/反代/更新全手动、需 Docker 技能
- 适用：已有 Docker 主机/NAS 用户、想与其他服务共存、能接受手动维护

---

## 第五章：HA Supervised 详解（含弃用现状）

> **篇幅**：中（约 3,500 字）
> **覆盖要点**：历史定位与 ADR-0014、官方支持约束、安装原理、弃用时间线、社区立场、优缺点与适用场景
> **素材引用**：素材 §一.3、§二、§五
> **代码示例**：有（supervised-installer 安装步骤）

### 5.1 历史定位与 ADR-0014（已 revert）
- 定义：在现有 Linux 上安装 Supervisor + Core，使用完整 HA 组件（除 HAOS 外）
- ADR-0014 曾定义官方支持，后标记 reverted
- 官方定位演进：曾"only for advanced users"，现已被弃用

### 5.2 官方支持约束（历史定义）
- 唯一支持宿主 OS：Debian 12 Bookworm，不接受任何衍生版（Raspberry Pi OS、Ubuntu 会被安装器拦截）
- 依赖清单：Docker CE ≥20.10.17、systemd ≥239、NetworkManager ≥1.14.6、udisks2 ≥2.8、AppArmor、cgroup v1、overlayfs2、journald
- 宿主必须"专用于 HA"，不得安装额外软件，否则易被判 Unsupported/Unhealthy

### 5.3 安装原理与脚本步骤
- supervised-installer 四步：装 network-manager + systemd-resolved → 装 curl、udisks2 → 装 OS-Agent → dpkg -i homeassistant-supervised.deb
- 数据目录默认 /var/lib/homeassistant，可用 DATA_SHARE 自定义
- 支持机型列表（generic-x86-64、qemux86-64、raspberrypi3-64/4-64/5-64 等）

### 5.4 弃用时间线与现状
- 2025-05-22 公告 → 2025.6 版本显示支持将于六个月后结束 → 2025.12 官方支持终止
- 弃用后仍可继续使用和更新，但官方不再接受问题报告、端用户文档移除
- 使用率数据：Core 约 2.5%、Supervised 约 3.3%

### 5.5 社区立场与 BYPASS_OS_CHECK 风险
- 社区公认 Supervised"less supported (and liked)"，处于受支持边缘地带
- 绕过 OS 检查的环境变量（BYPASS_OS_CHECK）会导致 Unsupported/Unhealthy，官方不背书、不负责
- 标注：此为社区流传信息，官方文档不背书

### 5.6 优点 / 缺点 / 适用场景
- 优点：兼具 Add-on 与宿主 OS 控制权
- 缺点：安装繁琐、维护成本高、易被判 Unsupported/Unhealthy、官方仅支持 Debian、已弃用
- 适用：基本不推荐新用户；仅在需要 Add-ons 又要宿主控制权时作为过渡

---

## 第六章：选型决策树与建议

> **篇幅**：中（约 2,500 字）
> **覆盖要点**：完整决策树、典型用户画像建议、不推荐的组合、决策权衡原则
> **素材引用**：素材 §四、§二
> **代码示例**：无（含决策树文本图）

### 6.1 决策树（完整版）
- 主线一：想省心、功能完整、愿意独占设备？→ HAOS（VM 或专用硬件）
- 主线二：已有 Docker 主机 / 想与其他服务共存？→ Docker Container
- 主线三：需要 Add-on 又要宿主控制权？→ 谨慎评估 Supervised，默认转向 HAOS
- 决策树以文本图形式完整呈现

### 6.2 典型用户画像建议
- NAS / 已有 Docker 主机的用户 → Container
- 有 Proxmox / VMware 环境的用户 → HAOS VM（社区主流）
- 有专用硬件的用户 → HAOS 直接刷机
- 只想零维护跑 HA 的用户 → HAOS VM
- 老 Supervised 用户 → 迁移到 HAOS / Container

### 6.3 不推荐的组合与原因
- 新用户直接上 Supervised（已弃用、仅 Debian、维护成本高）
- 在共享宿主上跑 Supervised（几乎必然 Unsupported）
- 想用 Add-on / Thread / Z-Wave 却选 Container（功能缺失）

### 6.4 决策背后的权衡原则
- 功能完整性 ↔ 灵活可控
- 省心程度 ↔ 资源占用
- 官方支持生命周期对长期选择的影响

---

## 第七章：迁移路径与操作

> **篇幅**：中（约 2,000 字）
> **覆盖要点**：官方迁移原则、各路径迁移详解、跨架构迁移、迁移注意事项
> **素材引用**：素材 §二
> **代码示例**：无（少量备份/恢复操作示意）

### 7.1 官方迁移原则
- "Switching systems is as easy as making a backup, downloading it, and restoring it during the initialization of your new system"
- 备份 → 下载 → 初始化时恢复 三步走

### 7.2 各路径迁移详解
- Core 用户 → 首选 Container（若独占设备则 HAOS）
- Supervised 用户 → 推荐 HAOS（需要宿主控制权时可在 Proxmox 等 VM 中跑 HAOS，或改用 Container）
- 32 位设备 → 装 64 位系统后恢复备份即可保留硬件

### 7.3 跨架构迁移可行性
- 任意安装方式之间、甚至跨架构都能恢复备份
- Home Assistant Cloud 订阅用户可凭密码异地恢复

### 7.4 迁移注意事项
- 备份完整性检查（含 Add-on 配置与设备集成）
- 迁移后验证 USB / Zigbee / 蓝牙直通是否生效
- 旧系统与新系统并行期的数据一致性

---

## 第八章（附录）：部署实操步骤

> **篇幅**：长（约 4,500 字，以代码为主）
> **覆盖要点**：Docker Compose 完整模板、Proxmox 部署 HAOS VM、HAOS 直接刷机、Supervised 安装脚本、初始化与备份恢复
> **素材引用**：素材 §一.1、§一.2、§一.3
> **代码示例**：有（全部为可复制命令/模板）

### 8.1 Docker Compose 完整模板与启动
- 官方 compose 模板（含蓝牙、时区、USB 直通、特权模式）
- 启动 / 停止 / 查看日志命令
- 升级与回滚操作

### 8.2 Proxmox 部署 HAOS VM 完整步骤
- 下载并解压镜像 → 导入磁盘 → 创建 VM（q35/UEFI/机型/网络）
- 一键脚本与手动两种方式
- USB 直通、快照备份、扩容命令

### 8.3 HAOS 直接刷机简述（专用硬件）
- 镜像烧写工具与步骤概述
- 首次引导与初始化

### 8.4 HA Supervised 安装脚本（附弃用警告）
- 四步安装命令
- 显式标注：该方式已于 2025.12 终止官方支持，仅存档参考

### 8.5 初始化引导与备份恢复
- 首次登录、创建账户
- 从备份恢复 / 全新初始化的入口差异

---

## 学习路径说明

### 前置要求
- 熟悉 Home Assistant 基本概念（集成、自动化、设备），理解"Add-on / 集成"的区别
- 了解 Linux 基础操作（命令行、systemd、Docker 基本概念）
- 对虚拟机（VM）与容器（Container）的差异有基本认识
- 不需要精通 Docker，但 Container 章节假设会执行基本 CLI 命令

### 学完能做什么
- 能准确说出 HAOS、Container、Supervised 三者在功能、维护、资源上的核心差异，不被过时教程误导
- 能根据自身硬件与使用场景独立做出部署方式选型决策
- 能在 Proxmox 上部署 HAOS VM，或在自己已有 Docker 主机上跑起 Container 版 HA
- 能完成 Core/Supervised 旧安装到新方式的备份迁移
- 知道官方弃用状态和"2025.12 之后"的选择边界

### 建议学习顺序
- 顺序：第 1 章 → 第 2 章（建立全景与对比框架）→ 第 3-5 章（按需精读与你相关的部署方式）→ 第 6 章（决策）→ 第 7 章（迁移）→ 第 8 章（实操附录，边做边查）
- 时间预估：
  - 通读第 1、2、6 章（决策主线）：约 1 小时
  - 精读 3-5 章中与你选型相关的 1-2 章：约 1.5 小时
  - 实操第 8 章部署一遍：约 2-3 小时
  - 若涉及迁移：第 7 章 + 实际操作约 1-2 小时
- 建议：先做选型（1/2/6 章），再按选型结果精读对应部署章节，最后动手部署时查阅附录
