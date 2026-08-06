# 部署 HAOS 详细教程 - 探测式收集结果（P1）

收集时间: 2026-08-06
工作流状态: workspace/workflow-runs/haos-deploy-tutorial.workflow.md（P1 进行中）

## 探测策略

3 个并行 subagent 分别探测三个方向：
1. HAOS 镜像获取与国内加速源
2. 实体机 + 虚拟机完整安装路线
3. 稳定运行保障（存储/网络/备份/升级/排障）

---

## 方向 1：国内加速源

### 核心发现：HAOS-CN「冬瓜极速版」是国内源最优解

- **HAOS-CN 官方下载站**（https://www.hasscn.top/download.html）：面向中国大陆用户的 HAOS 镜像站，提供 img.xz / qcow2 / vmdk / vdi / vhdx / ova 格式，覆盖 x86-64、树莓派 3/4/5、HA Green/Yellow、黑豹 X2、PVE/VMware/ESXi/Hyper-V 等。分「完整包 -full」（装完免下依赖）与「在线式」。加速机制：version.home-assistant.io → version.hasscn.top、ghcr.io → ota.hasscn.top。
- **Docker 镜像加速**（HAOS-CN 内置 12 个国内源，写入 /etc/docker/daemon.json）：docker.1panel.live、docker.1ms.run、hub.rat.dev、docker.m.daocloud.io 等，按序故障转移，全失败回落 Docker Hub。Core 镜像拉取 30–120s → 5–30s。
- **社区 Add-on 加速仓库**（ha-china/hassio-addons）：ghcr.io → ghcr.nju.edu.cn（南大）、docker.io / lscr.io → docker.1panel.live、github.com → gh-proxy.org；强调「无需翻墙，翻墙反而可能失败」。
- **通用 Docker 加速配置**：/etc/docker/daemon.json 的 registry-mirrors 数组（aliyun 需登录、第三方站波动大，多备几个）。
- **镜像校验**：官方 Release 提供 SHA256（18.0: x86-64 img.xz 548MB、aarch64 343MB）；OVA 用 home-assistant.mf 清单校验。HAOS-CN 仅刷机程序公布 SHA256，OS 镜像建议对照官方 checksum。
- 清华/中科大镜像站本身不托管 HAOS 系统镜像（它们主要加速宿主系统 apt/pip）。

## 方向 2：实体机 + 虚拟机安装路线

### 实体机（Generic x86-64）
- 官方文档：下载 `haos_generic-x86-64-XX.img.xz` → balenaEtcher 烧录（Flash from file，勿用 Flash from URL）→ BIOS 开 UEFI、关 Secure Boot → 首次联网启动，访问 `homeassistant.local:8123`。
- 要求：64 位 UEFI、内存 ≥2GB、存储 ≥32GB；烧录清空全盘。

### VMware Workstation
- 官方文档：下载 `haos_ova-18.2.vmdk.zip` → 新建 Linux/Other Linux 5.x 64 位 VM，2GB/2 核，网卡桥接 → **关键：.vmx 末尾加 `firmware = "efi"`** → 替换 vmdk → 启动。

### PVE
- 下载 `haos_ova-XX.qcow2` → `qm importdisk` 导入 → i440fx + OVMF(UEFI)，删默认 SCSI 盘 → 磁盘总线改 **SATA**、引导顺序 sata0 置首 → CPU host、内存 2048MB+（社区建议 4GB）→ 启动访问 `IP:8123`。PVE 8.3 起支持 OVA 直接导入。

### 群晖 VMM
- DSM 7.0+ 装 Virtual Machine Manager，建议开 Open vSwitch → 导入 .vmdk/.ova → **固件必须选 UEFI**、磁盘控制器 SATA、≥32GB → 首次启动可能 20 分钟到数小时。

### 共性坑
- 三条虚拟化路线共同坑：**UEFI/EFI 引导**（缺此步骤黑屏 / "Operating System not found"）。
- 磁盘总线用 SATA 而非默认 SCSI。
- 首次访问 `homeassistant.local:8123`，mDNS 失败直接改用 IP；建议路由器绑定静态 IP。
- 首次启动下载 Supervisor/HA 核心镜像（约 700MB，ghcr.io）国内可能需数小时，不要中途断电。

## 方向 3：稳定运行保障

### 存储介质
- **SSD 优先**：HA 数据库约 15 次写入/秒，microSD/TF 卡数月即磨损损坏（负载与介质不匹配，非质量问题）。Pi4 用 SATA SSD+USB3.0 硬盘盒，Pi5 用 PCIe NVMe，迷你主机用内置 SATA/NVMe。迁移：备份→写镜像→SSD 启动→恢复备份。

### 备份
- Google Drive 备份插件（hassio-google-drive-backup）：自动备份 + 世代保留（每日/周/月/年），升级自动生成快照可回滚。回滚：可访问时 Web UI 恢复；全新安装先上传备份再建用户。遵循 3-2-1 规则。

### 时间同步（NTP 国内源）
- chrony addon 把 ntp_pool 改为 `cn.pool.ntp.org`；或 /etc/systemd/timesyncd.conf 填 `NTP=ntp.aliyun.com`、`FallbackNTP=cn.pool.ntp.org`。
- 时间偏差持续增大基本可判定 NTP 问题，虚拟机尤其明显。

### 国内网络优化（HAOS-CN 已集成）
- 8 类网络服务从国际端点重定向到腾讯 BGP：NTP 用阿里/腾讯源、版本检查/OTA 走国内节点、Docker 镜像 12 源故障转移、DNS 用阿里/腾讯（不推荐 8.8.8.8）。
- OTA 保留 RAUC 签名 + A/B 原子更新可回滚；每月 28 日自动检查更新。
- 远程访问推荐 DDNS-GO + Nginx Proxy Manager（开 WebSocket，配 trusted_proxies）。

### 排障
- 无 IP：`network update eth0 --ipv4-method auto`、`network reload`、`network info`；建议静态 IP。
- 数据库损坏多因非正常断电/强制重启；正确重启走「设置→系统→硬件」；SQLite `.recover` 或改 MariaDB。
- 启动失败查 8124/4357 端口日志；`ha core restart` / `ha core rebuild`。

---

## 初步方向菜单（待用户选择）

| 选项 | 主线 | 特点 |
|------|------|------|
| **A. HAOS-CN 国内极速版为主线** | 直接推荐「冬瓜版」HAOS-CN（内置国内源自动加速）| 最贴合"如何用国内源"诉求，安装即国内源，省心；来源为国内社区站，需注意非官方 |
| **B. 官方原版 HAOS + 手动配置国内源** | 官方镜像安装，再逐项配置 Docker 加速 / NTP / DNS / Add-on 国内仓库 | 纯净官方版、每项配置可解释可掌控；步骤更多 |
| **C. 双路线对比** | 先官方原版 + 手动国内源配置，再介绍 HAOS-CN 极速版作替代，做对比 | 最完整、篇幅最大；适合"想理解原理再选"的读者 |
| **D. 其他** | 用户自定义侧重（如只写 PVE、只写稳定运行）| 可补充 |

> 注意：HAOS-CN 是社区项目（hasscn.top / 冬瓜），非 Home Assistant 官方发行版；教程需说明其来源与取舍。

---

## 用户选择（P1 确认 2026-08-06）

**方向 C：双路线对比**
- 先讲官方原版 HAOS 安装 + 手动配置国内源（Docker 加速 / Add-on 国内仓库 / NTP / DNS）
- 再介绍 HAOS-CN「冬瓜极速版」作为国内替代方案
- 对比两者取舍，给出选型建议
- 配套稳定运行保障章节（存储/备份/升级/排障）贯穿两条路线
