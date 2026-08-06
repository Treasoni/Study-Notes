# 学习笔记大纲：《部署 HAOS 详细教程：国内源 + 稳定运行》

> **笔记类型**：实战教程（practice）——双路线对比主线（官方原版 + 手动国内源 → HAOS-CN 极速版替代方案 → 选型建议），稳定运行保障（存储/备份/升级/排障）贯穿
> **学习深度**：精通（含排障 + 长期运维）
> **部署平台**：实体机 x86-64 + 虚拟机（VMware Workstation / PVE / 群晖 VMM）
> **预计总篇幅**：约 16,000–21,000 字
> **章节数**：8 章
> **输出目标**：Obsidian vault `C:\note\Study-Notes` → `homeassistant/haos-deploy/`

---

## 全篇写作约定

- 层级不超过三级：`# 标题` → `## 章` → `### 节`（→ `#### 小节`，仅特殊场景使用）。
- 表格一律平铺在正文中，**不嵌套在列表/引用块内**；代码块必须带语言标识（`bash`、`json`、`ini`、`yaml`、`text`）。
- 双链只加高价值概念：`[[Home Assistant 三种部署方式对比与选型]]`、`[[HAOS]]`、`[[HAOS-CN]]` 等。
- Callout 约定：`[!summary]` 每章结论、`[!tip]` 实操建议、`[!warning]` 易错点/时效性、`[!example]` 命令示例。
- 所有镜像站地址、HAOS-CN 版本号、错误码均标注"以实际日志/官网为准"，写明采集时间（2026-08-06）。
- 每章开头放 `[!summary]` 一章讲什么，结尾放"本章 Checklist"（可勾选项）。

---

### 第一章：绪论——为什么需要「国内源 + 稳定运行」
- **篇幅**：短（约 800–1,200 字）
- **覆盖要点**：国内网络下部署 HAOS 的核心痛点（ghcr 拉取慢/被墙、Add-on 商店加载失败、时间不同步）；本文双路线框架（官方原版 + 手动配置国内源 vs HAOS-CN 极速版）；与既有笔记 `[[Home Assistant 三种部署方式对比与选型]]` 的边界划分（不重复选型，聚焦"如何装 + 国内源 + 稳定运行"）；全文学习路线图（安装 → 加速 → 对比 → 稳定 → 排障）；时效性声明
- **素材引用**：02_deep_research.md「综合分析」→ 双路线对比表 / 关键共识 / 时效性风险
- **代码示例**：无
- **结构**：
  - 1.1 国内网络环境下的部署痛点
  - 1.2 双路线总览与本文定位
  - 1.3 学习路线图与前置知识（呼应既有选型笔记）

### 第二章：部署前置准备——存储、固件、镜像与工具链
- **篇幅**：中（约 1,500–2,000 字）
- **覆盖要点**：部署平台选择（实体机 vs 虚拟机，各自适用场景）；存储介质选型（SSD 优先，TF 卡必坏原理——HA 约 15 次写入/秒）；固件准备（UEFI、关闭 Secure Boot、无需 TPM）；官方镜像下载与国内加速获取、SHA256 校验；烧录/导入工具链（balenaEtcher、Rufus、Ventoy、`scp` + `qm importdisk`）
- **素材引用**：02_deep_research.md §一.1（实体机 x86-64）、§一.5（跨平台共性）、§四.1（SSD 迁移根因）
- **代码示例**：有（`sha256sum` 校验命令、烧录工具操作命令）
- **结构**：
  - 2.1 部署平台与硬件选型
  - 2.2 存储介质：SSD 优先原则
  - 2.3 固件与引导设置（UEFI / Secure Boot / TPM）
  - 2.4 镜像下载、校验与工具链准备

### 第三章：官方原版 HAOS 安装实战（实体机 + 虚拟机全平台）
- **篇幅**：长（约 3,000–4,000 字）
- **覆盖要点**：实体机 x86-64 刷写（`img.xz` → balenaEtcher / Ubuntu Disks，UEFI 引导，坑：target is busy、`bootx64.efi` 指定）；VMware Workstation（`haos_ova.vmdk`、编辑 `.vmx` 加 `firmware = "efi"`、Bridged 桥接网络）；PVE（`qcow2` → `qm importdisk`、i440fx + OVMF + SATA、删除默认 SCSI 盘、`scsi0` 置首）；群晖 VMM（vmdk/ova、固件必须 UEFI、SATA 控制器 ≥32GB、Open vSwitch）；跨平台共性总结（2 vCPU + 2GB 起、首次启动需联网、访问地址 `homeassistant.local:8123`）
- **素材引用**：02_deep_research.md §一.1–§一.5（官方原版安装全部小节）
- **代码示例**：有（`.vmx` 配置行、PVE `qm importdisk` / `scp` 命令、`efibootmgr` 引导修复命令）
- **结构**：
  - 3.1 实体机 x86-64 刷写与 UEFI 引导
  - 3.2 VMware Workstation 安装（含 `.vmx` EFI 配置）
  - 3.3 PVE 安装（qcow2 导入 + 总线/引导顺序修正）
  - 3.4 群晖 VMM 安装（固件与磁盘控制器关键参数）
  - 3.5 跨平台共性、首次启动验证与常见安装坑速查

### 第四章：手动配置国内源（官方原版加速核心）
- **篇幅**：长（约 3,000–4,000 字）
- **覆盖要点**：Docker `registry-mirrors` 12 源故障转移链（`/etc/docker/daemon.json`，坑：仅对 `docker.io` 生效）；Supervisor 层 ghcr.io 加速（`/etc/hassio.json`、`/usr/share/hassio/docker.json` 的 `registries_mirror`，重启 `hassio-supervisor`，坑：升级会重置需备份）；Add-on 国内仓库（ha-china/hassio-addons，Gitee 地址 + 镜像映射表，免翻墙）；NTP 时间同步（`/etc/systemd/timesyncd.conf` 国内源、首次启动预置 `hassio-boot`、chrony 加载项、8 小时 vs 持续增大判别）；首次启动 DNS/ghcr 加速补充（udev bind-mount 方案原理 + 2026.2.1 失效提醒 + 推荐排序）
- **素材引用**：02_deep_research.md §二.1–§二.5（手动配置国内源全部小节）
- **代码示例**：有（`daemon.json` JSON 示例、`/usr/share/hassio/docker.json` 示例、`timesyncd.conf` ini 示例、`systemctl` / `timedatectl` 验证命令、`docker info` 验证）
- **结构**：
  - 4.1 Docker 镜像加速：12 源故障转移链与验证
  - 4.2 Supervisor 镜像源：破解 ghcr.io 拉取瓶颈
  - 4.3 Add-on 商店国内仓库与镜像映射
  - 4.4 NTP 时间同步国内化（含首次启动预置）
  - 4.5 首次启动 DNS/ghcr 加速补充与方案失效提醒

### 第五章：HAOS-CN 极速版——一键国内化替代方案
- **篇幅**：中（约 2,000–2,500 字）
- **覆盖要点**：项目概述与信任模型（开源 HAOS-CN vs 闭源冬瓜 HAOS、集成 HACS 极速版、自建 OTA、主版本 18.2）；下载与格式选择（`img.xz`/`qcow2`/`vdi`/`vmdk`/`ova`/`vhdx`、`-full` 完整包 vs 在线式、校验和缺口）；内置加速机制（8 类网络重定向、12 源故障转移、数据目录 `/mnt/data/docker`、提速数据）；安装差异与互转（官方→极速 OTA 脚本、极速→官方需备份重装、A/B 分区排查）；风险清单（安装后不可改、中国 IP 依赖、第三方源风险、保留官方备路）
- **素材引用**：02_deep_research.md §三.1–§三.5（HAOS-CN 全部小节）、综合分析（互转列）
- **代码示例**：有（官方→极速 OTA 升级脚本 `curl -fsSL https://ota.hasscn.top/upgrade.sh | bash`、验证命令、`ha os info` / `ha os boot-slot` 排查命令）
- **结构**：
  - 5.1 项目概述与信任模型
  - 5.2 下载、格式选择与校验缺口
  - 5.3 内置加速机制解析
  - 5.4 安装差异、官方互转与 A/B 分区
  - 5.5 风险清单与使用边界

### 第六章：双路线对比与选型建议
- **篇幅**：短（约 800–1,200 字）
- **覆盖要点**：精简对比表（国内源、首次启动、可配置性、完整性校验、信任模型、更新机制、互转方向）；按场景选型建议（生产求稳 / 国内折腾 / 网络受限三档）；迁移路径与保留官方备路的策略；与既有选型笔记 `[[Home Assistant 三种部署方式对比与选型]]` 的分工说明
- **素材引用**：02_deep_research.md「综合分析」→ 双路线对比表、关键共识、时效性风险
- **代码示例**：无
- **结构**：
  - 6.1 双路线精简对比表（正文平铺表格）
  - 6.2 场景化选型建议
  - 6.3 迁移路径与官方备路策略

### 第七章：稳定运行保障——存储、备份与升级
- **篇幅**：长（约 2,500–3,500 字）
- **覆盖要点**：SSD 迁移实操（TF 卡损坏根因、按平台选型、备份→写 SSD→恢复）；备份策略（Google Drive 备份插件、世代保留参数、3-2-1 规则、升级前自动快照、恢复三场景）；升级与回滚（Core 自动回滚与日志、`ha supervisor repair`、`ha core update --version` 指定版本、逐大版本升级 + 每步备份、Supervisor 更新不随 Core 回滚）
- **素材引用**：02_deep_research.md §四.1（SSD 迁移）、§四.2（Google Drive 备份）、§四.3（升级与回滚）
- **代码示例**：有（Google Drive 备份插件 `options.json` 配置示例、`ha supervisor repair` / `ha core update` 命令、回滚日志路径）
- **结构**：
  - 7.1 SSD 迁移：终结 TF 卡损坏
  - 7.2 备份策略：Google Drive 世代备份与 3-2-1 规则
  - 7.3 升级与回滚：机制、命令与策略

### 第八章：故障排查手册与长期运维
- **篇幅**：中（约 2,000–3,000 字）
- **覆盖要点**：错误码速查（1001–1005、无 IP、数据库损坏与 `.recover` 重建）；端口与诊断（8123 / 8124 / 4357，正确重启走「设置→系统→硬件」）；NTP/时间排障（时区 vs NTP 判别）；国内远程访问方案（Tailscale、Cloudflare Tunnel、FRP、公网 IP + Nginx 反代，勿裸映射 8123）；长期运维检查清单（每周/每月，公益镜像源失效应对）
- **素材引用**：02_deep_research.md §四.4（排障错误码）、§四.5（NTP 与远程访问）、综合分析（关键共识）
- **代码示例**：有（`network update enp1s0 --ipv4-method auto`、`timedatectl`、SQLite `.recover`、`curl http://homeassistant.local:4357/` 诊断命令）
- **结构**：
  - 8.1 错误码速查与数据库修复
  - 8.2 端口、诊断通道与正确重启
  - 8.3 时间同步排障
  - 8.4 国内远程访问方案对比
  - 8.5 长期运维检查清单

---

## 学习路径说明

### 前置要求
- 已通读 `[[Home Assistant 三种部署方式对比与选型]]`，清楚 HAOS / Docker Container / Supervised 的定位差异（Supervised 已于 2025.12 弃用）。
- 有一台可用的部署主机：实体机（x86-64 迷你主机/NUC/旧 PC）或虚拟机平台（VMware Workstation / PVE / 群晖 VMM 任一）。
- 会基础 Linux/Shell：`vi`、`systemctl`、`curl`、`scp`、`docker info` 等命令能看懂并照着执行。
- 有国内网络环境（镜像站、Gitee、阿里云 NTP 均需国内可达）。

### 学完能做什么
- 从零把 HAOS 装上实体机或任意主流虚拟机平台（VMware / PVE / 群晖 VMM），并排掉 UEFI、SATA 总线、首次启动等常见坑。
- 手动为官方原版 HAOS 配置一整套国内加速：Docker 镜像 12 源、Supervisor ghcr.io 镜像、Add-on 国内仓库、NTP 国内时间源。
- 完整评估并可选部署 HAOS-CN 极速版，能通过 OTA 脚本在官方版与极速版之间互转（含 A/B 分区排查）。
- 制定并执行稳定运行策略：SSD 迁移、Google Drive 世代备份、升级前快照、逐版本升级与回滚。
- 独立排查无 IP、错误码 1001–1005、数据库损坏、时间不同步等问题，并选型国内远程访问方案。

### 建议学习顺序
- 第 1 章（30 分钟）：建立双路线心智模型，明确本文边界。
- 第 2–3 章（2–3 小时）：按你的平台走通官方原版安装，先跑起来。
- 第 4 章（2 小时）：手动配置国内源——这是官方路线的核心价值，建议逐节实操验证。
- 第 5 章（1 小时）：了解 HAOS-CN 极速版，作为替代/备路。
- 第 6 章（30 分钟）：读完对比表做选型决策。
- 第 7–8 章（2 小时，长期按需查阅）：稳定运行保障与排障手册，建议收藏后按清单周期性执行。
- 若只想要"最省心"方案：可直接跳到第 5 章用 HAOS-CN `-full` 完整包，但仍建议回看第 2、7 章的存储与备份原则。
