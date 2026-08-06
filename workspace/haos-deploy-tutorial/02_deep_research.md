# 部署 HAOS 详细教程 - 深度收集（P2）

收集时间: 2026-08-06
工作流状态: workspace/workflow-runs/haos-deploy-tutorial.workflow.md（P2 进行中）
已选方向: **C. 双路线对比**（官方原版 + 手动国内源 vs HAOS-CN 极速版）

## 搜索关键词
`HAOS 国内镜像下载 加速`、`Home Assistant OS 国内源`、`docker 国内镜像加速器 daemon.json`、`HAOS 虚拟机安装 PVE 教程`、`home assistant os 安装 官方 教程`、`home assistant 常见问题 排障`、`HAOS NTP 时间同步`、`home assistant 升级 回滚 快照`、`haos 常见错误码`

---

## 第二阶段：精读笔记

### 一、官方原版 HAOS 安装路线

#### 1. 实体机 x86-64（官方文档）
- **URL**: https://www.home-assistant.io/installation/generic-x86-64
- **步骤**：
  1. 下载 `haos_generic-x86-64-{ver}.img.xz`（写入即启动，会清空目标盘，无安装器）
  2. BIOS 开 UEFI、关 Secure Boot（F2/Del 进 BIOS）
  3. 写入：方法 A 用 Ubuntu Live USB 的 Disks → Restore Disk Image；方法 B 用 balenaEtcher（先解压 .xz，选 Flash from file，勿用 Flash from URL）
  4. 首次启动必须联网（会下载最新 Core）；访问 `http://homeassistant.local`，备选 `homeassistant` / `http://<IP>`，80 被占用加 `:8123`
- **坑**：Disks 报 target is busy（Swap 分区占用 → 卸载）；找不到引导介质 → UEFI 下手动指定 `\EFI\BOOT\bootx64.efi` 或 `efibootmgr --create ... --loader '\EFI\BOOT\bootx64.efi'`

#### 2. VMware Workstation（官方文档）
- **URL**: https://www.home-assistant.io/installation/windows
- **步骤**：
  1. 下载 `haos_ova-{ver}.vmdk.zip` 解压
  2. 新建 VM：Linux → Other Linux 5.x kernel 64-bit；内存 ≥2048MB、CPU ≥2 核；网络 **Bridged 桥接**（仅勾选真实物理以太网适配器）
  3. 删除向导生成的 vmdk，把 HAOS vmdk 改名 `home-assistant.vmdk` 复制进去
  4. **关键**：编辑 `.vmx` 加一行 `firmware = "efi"`
  5. 启动 → 访问 `http://homeassistant.local`
- **坑**：side channel mitigations 提示点 OK；vmdk 找不到=误复制文件夹

#### 3. PVE（Proxmox VE）
- **URL**: https://wiki.slarker.me/pve/haos.html
- **步骤**：
  1. 下载 `haos_ova-{ver}.qcow2.xz` 解压
  2. 新建 VM：i440fx；BIOS `OVMF(UEFI)` **取消勾选添加 EFI 磁盘**；删除默认 SCSI 盘；CPU 2 核 host；内存 2048MB
  3. `scp` 上传 qcow2 到 `/tmp`（qcow2 不能走 ISO 上传）
  4. `qm importdisk 100 /tmp/haos_ova-{ver}.qcow2 local`
  5. 硬件出现"未使用的磁盘0" → 添加 → 总线改 **SATA**
  6. 引导顺序把 `sata0` 置顶
  7. 启动 → 访问 `http://<IP>:8123`
- **替代配置**：q35 + OVMF + VirtIO SCSI + `scsi0` 置首亦可；PVE 8.3 起支持 OVA 直接导入
- **坑**：默认 SCSI 盘必须删；导入盘默认未使用需手动添加；磁盘空间不足或加速源被墙会卡住

#### 4. 群晖 VMM
- **URL**: https://www.cnblogs.com/mingyue5826/p/18958567（该文用冬瓜 ISO 流程，官方 VMM 走 vmdk/ova）
- **要点**：装 Virtual Machine Manager（DSM 7.0+），建议开 **Open vSwitch**；导入 vmdk/ova；**固件必须 UEFI**；磁盘控制器 **SATA**、≥32GB；首次启动 20 分钟–数小时正常；访问 `http://<IP>:8123`
- **坑**：虚拟机起不来查固件/SATA；与宿主机不通查 Open vSwitch

**跨平台共性**：UEFI/EFI 引导（关 Secure Boot、无需 TPM）、2 vCPU + 2GB 起、磁盘 ≥32GB、SATA 总线、首次启动需联网拉组件（国内约 700MB 可能很慢）、访问地址统一 `homeassistant.local:8123` 或 `http://<IP>:8123`。

---

### 二、手动配置国内源（官方原版路线）

#### 1. Docker 加速 registry-mirrors（12 源故障转移链）
- **URL**: https://deepwiki.com/ha-china/HAOS-CN/2.2-docker-registry-mirrors
- **配置**（/etc/docker/daemon.json）：
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
- 其他可用源：`docker.nju.edu.cn`、`docker.mirrors.ustc.edu.cn`、阿里云专属 `<id>.mirror.aliyuncs.com`（需申请）
- 验证：`docker info | grep -A5 "Registry Mirrors"`
- **坑**：公益镜像站隔天失效常见，多配几个；`registry-mirrors` **只对 docker.io 生效，对 ghcr.io 无效**（HA 核心/官方 Add-on 在 ghcr.io，需 Supervisor 层配置）；原版 HAOS 根文件系统只读，此文件不可直接改

#### 2. Supervisor 镜像源（ghcr.io 加速核心）
- **URL**: https://community.home-assistant.io/t/how-to-set-a-docker-registry-mirrors/999940 ；https://bbs.hassbian.com/forum.php?mod=viewthread&tid=25022
- **配置**：
```bash
# /etc/hassio.json：改 supervisor 自身镜像
#   "supervisor": "ghcr.nju.edu.cn/xjboss/{arch}-hassio-supervisor"  # {arch}=amd64/aarch64
# /usr/share/hassio/docker.json：
vi /usr/share/hassio/docker.json
{
  "registries": {},
  "registries_mirror": { "ghcr.io": "ghcr.nju.edu.cn", "docker.io": "docker.nju.edu.cn" }
}
systemctl restart hassio-supervisor
```
- **坑**：这是 HAOS/Supervised 下解决 ghcr.io 的核心路径，与 daemon.json 互补；HAOS 升级可能重置该文件，需备份；只解决镜像拉取，不解决 GitHub 源码/OTA

#### 3. Add-on 国内仓库（ha-china/hassio-addons）
- **URL**: https://github.com/ha-china/hassio-addons
- **配置**：设置 → 加载项商店 → 右上角三个点 → 仓库 → 添加：
```
https://gitee.com/desmond_GT/hassio-addons
```
- **镜像映射表**：ghcr.io → `ghcr.nju.edu.cn`；docker.io / lscr.io → `docker.1panel.live`；github.com → `gh-proxy.org`
- **坑**：无需翻墙，翻墙反而可能失败；国内镜像首次安装偶发失败，重试一次即可；GitHub 仓库仅用于更新，安装走 Gitee 地址

#### 4. NTP 时间同步（国内源）
- **URL**: https://bbs.hassbian.com/archiver/?tid-28537.html ；https://blog.csdn.net/weixin_28691741/article/details/160267845
- **配置**（SSH root 端口 22222）：
```ini
# /etc/systemd/timesyncd.conf
[Time]
NTP=ntp1.aliyun.com ntp2.aliyun.com ntp3.aliyun.com
FallbackNTP=ntp.tencent.com cn.pool.ntp.org
```
```bash
systemctl restart systemd-timesyncd.service
timedatectl   # System clock synchronized: yes 即成功
```
- 首次启动前预置：在 `hassio-boot/CONFIG/timesyncd.conf`（权限 644），同步缩至 10 秒内
- 容器环境用 **chrony 加载项**（ntp_pool 改 `cn.pool.ntp.org` + 开机自启）
- 判别：差整 8 小时=时区未设；差几分钟且持续增大=NTP 失败

#### 5. DNS 与首次启动 ghcr 拉取加速（社区 udev 覆盖方案）
- **URL**: https://github.com/home-assistant/operating-system/discussions/2797
- 原版 HAOS 根只读，社区用 udev bind-mount 覆盖 daemon.json（加 `proxies` 走 ghcr 代理）
- **坑**：该 udev 方案在 **2026.2.1 失效**，新版本原样照抄会 boot loop，需精简字段
- **推荐排序**：国内定制版（HAOS-CN）> Supervisor registries_mirror > udev bind-mount > 手拉镜像改名

---

### 三、HAOS-CN「极速版」详解

#### 1. 项目概述
- **URL**: https://www.hasscn.top/download.html ；https://hasscn.top/QandA
- 官方英文名「🇨🇳 Home Assistant OS Turbo」，定位「更适合中国网络环境」的 HAOS 改造再分发；**开源**（GitHub ha-china/HAOS-CN），区别于瀚思彼岸的**闭源**「冬瓜HAOS」
- 核心变化：官方加载项源替换为国内加速源 + 集成 HACS 极速版（免 GitHub 账号、免科学上网）
- 更新机制：自建 OTA（ota.hasscn.top，深圳酷宅 CoolKit 赞助，仅限中国 IP）；每月 27 日构建、28 日自动检查；不商业化，公司可免费
- **当前主版本 18.2**

#### 2. 下载与格式
- 格式：`img.xz` / `qcow2.xz` / `vdi.zip` / `vmdk.zip` / `ova` / `vhdx.zip`
- 平台：generic aarch64 / generic x86-64 / HA Green / HA Yellow / Sonoff iHost / OrangePi CM4 / Panther X2 / Raspberry Pi 3/4/5 / Hyper-V
- **完整包（-full，公测）** vs **在线式**：在线式=官方一致，装完需联网拉依赖；完整包=装完即用、免等待。x86-64 的 qcow2/vdi/vmdk 在线列缺失
- 下载建议：优先 **gh-proxy.org** 原始加速链接；酷宅下载点禁手机 + WAF 限流
- **校验**：仅刷机程序 green_factory_CN 公布 SHA256；各系统镜像未列校验和（需对照官方 checksum）

#### 3. 内置加速机制
- **URL**: https://deepwiki.com/ha-china/HAOS-CN/2.1-network-service-redirection ；https://deepwiki.com/ha-china/HAOS-CN/2.2-docker-registry-mirrors
- **8 类网络重定向**：版本检查→version.hasscn.top；连通性检查→腾讯 BGP（HTTP 204）；NTP→阿里/腾讯国内源；容器镜像 `ghcr.io/home-assistant/*`→ota.hasscn.top（Registry API V2 + CDN）；OTA→腾讯 BGP（保留 RAUC 签名 + A/B 原子更新，每月 28 日）；错误上报→腾讯 BGP；Docker 镜像→12 源故障转移
- **12 个 Docker 镜像源**（优先级）：docker.1panel.live → docker.1ms.run → dytt.online → docker-0.unsee.tech → lispy.org → docker.xiaogenban1993.com → 666860.xyz → hub.rat.dev → docker.m.daocloud.io → demo.52013120.xyz → proxy.vvvv.ee → registry.cyou；全失败回退 docker.io；首个挂掉约 5-10 秒切换
- 实现：构建时硬编码（只读 EROFS）+ 运行时 rootfs-overlay（Docker/NTP 配置）；**安装后不可修改、无关闭开关**
- 数据目录 `data-root: /mnt/data/docker`（独立分区，A/B 更新后镜像保留）
- **提速数据**：镜像下载提速 5-10 倍（1Gbps 核心+Add-on 1-1.5 分钟）；500MB Core 无镜像 30-120s → 有镜像 5-30s；版本检查 20-50ms vs 国际 200-500ms

#### 4. 安装差异与互转
- 底层刷写/导入流程与官方**基本相同**；差异在首次启动（完整包免等待）
- **官方版→极速版**（保留配置，先备份，系统终端非网页 Terminal）：
```bash
login
curl -fsSL https://ota.hasscn.top/upgrade.sh | bash
```
  自动重启；验证：启动出现 `OTA service kindly sponsored by Coolkit`；重启后先看 `http://homeassistant.local:4357` 状态全绿，再进 `:8123`
- **极速版→官方：无 OTA 脚本**，官方只推荐备份→重装→还原
- A/B 分区排查：`ha os info` 看 `boot:` → `ha os boot-slot A|B` → `ha host reboot`

#### 5. 风险与注意事项
- 非官方发行版：端点配置经私有构建脚本注入、公开仓库不可见；信任模型依赖项目方
- 校验和缺口：系统镜像未列 SHA256，无法自行验证完整性
- 版本标注不一致（ihost、rpi5 两处已确认）；完整包为公测，有"装完进不了系统"风险
- 硬依赖中国大陆网络；酷宅 OTA 仅限中国 IP
- 12 个第三方镜像源均非官方，有失效/合规风险；系统内只能做一个加速方案
- 生产适用性需自行评估；保留官方镜像备路

---

### 四、稳定运行与故障排查

#### 1. SSD 迁移（终结 TF 卡损坏）
- **URL**: https://evezone.evetech.co.za/deep-dives/best-ssd-for-home-assistant-in-2026-stop-sd-card-corruption-for-good
- 根因：HA 数据库约 **15 次写入/秒**，microSD 闪存寿命远低于此负载，数月即损坏（介质不匹配，非质量问题）
- 选型：Pi4 及更早→SATA SSD + USB3.0 硬盘盒；Pi5→PCIe NVMe；迷你主机/NUC→内置 SATA/NVMe；容量不用大
- 迁移：完整备份 → 官方镜像写入 SSD → SSD 引导 → 恢复备份

#### 2. Google Drive 备份插件
- **URL**: https://github.com/sabeechen/hassio-google-drive-backup
- 世代保留：`generational_days/weeks/months/years`（如 3/4/12/5）；`days_between_backups: 1`（每天一次）；`max_backups_in_drive: 24`
- 可加密；OAuth 仅申请 `drive.file` 权限；备份目录固定 "Home Assistant Backups"
- 恢复三场景：插件可用→Load into HA；全新安装→**创建用户前**上传备份；已装 HA→Samba 拷入 `/backup`
- **升级前自动建快照**（升级回滚点）；建议 3-2-1 备份规则

#### 3. 升级与回滚
- **URL**: https://github.com/home-assistant/supervisor/issues/5738 ；https://github.com/home-assistant/core/issues/157987
- 机制：升级 Core 超时/崩溃自动回滚，日志 `/config/home-assistant-rollback.log`
- 常见原因：启动超时（`STARTUP_API_RESPONSE_TIMEOUT` 3→5→10 分钟，可调大）；Supervised 缺 `/run/supervisor` bind mount；配置/自定义集成崩溃（`unique_id` 非字符串）；跨大版本跳升
- 命令：`ha supervisor repair`；`ha core update --version X`（强制指定版本）；建议**逐大版本升级 + 每步备份**；Supervisor 自身更新不随 Core 回滚

#### 4. 排障错误码
- **URL**: https://github.com/home-assistant/operating-system/issues/1998 ；https://blog.51cto.com/u_16213309/14792310
- **无 IP**：断电后 HAOS 比 DHCP 先启动，接口不重试 → `network update enp1s0 --ipv4-method auto`；建议静态 IP
- **错误码**：1001 网络接口错误；1002 依赖工具缺失；1003 启动失败；1004 数据库不存在；1005 配置文件格式错误
- **数据库损坏**：SQLite `.recover` 重建；长期高频写入改 MariaDB 或 SSD；正确重启走「设置→系统→硬件」
- **端口**：8123 Core/Web UI；8124 Supervisor API；4357 HassOS Observer 诊断（Core 起不来时 `curl http://homeassistant.local:4357/`）

#### 5. NTP 与国内远程访问
- 国内 NTP 源：`ntp1~7.aliyun.com`、`ntp.tencent.com`、`ntp.ntsc.ac.cn`、`cn.pool.ntp.org`
- 判别：整 8 小时=时区；持续增大=NTP
- **远程访问方案**：Tailscale（个人首选，官方插件，`.ts.net:8123`）；Cloudflare Tunnel（需自有域名，国内部分地区被污染需测连通）；FRP（需公网 VPS）；公网 IP+端口映射（建议 Nginx 反代，勿裸映射 8123）

---

## 综合分析

### 双路线对比（核心决策）

| 维度 | 官方原版 HAOS | HAOS-CN 极速版 |
|------|--------------|----------------|
| 来源 | Home Assistant 官方 | 社区开源再发行（ha-china/HAOS-CN） |
| 安装流程 | 官方镜像刷写/导入（同上） | 与官方基本相同，-full 包免初始化等待 |
| 国内源 | 需手动配置（Docker/Supervisor/Add-on/NTP/DNS） | **内置**：12 Docker 源 + 8 类网络重定向 |
| 首次启动 | ghcr 拉取 700MB，国内可能数小时 | 在线式数十分钟 / 完整包即装即用 |
| 可配置性 | 每项源可解释、可掌控 | 安装后**不可改**、无关闭开关 |
| 完整性校验 | 官方 SHA256 齐全 | 系统镜像无校验和 |
| 信任模型 | 官方背书 | 依赖项目方与第三方镜像站（WAF/失效风险） |
| 更新 | 官方 OTA（慢） | 国内 OTA（快，A/B 原子更新可回滚） |
| 生产适用 | 推荐 | 需自行评估，保留官方备路 |
| 互转 | — | 官方→极速版一键 OTA 脚本；反向需备份重装 |

### 关键共识（两路线通用）
1. **存储先用 SSD**：TF 卡必坏，这是稳定第一要素
2. **UEFI + SATA** 是所有安装的共同坑
3. **首次启动别断电**：拉镜像慢是正常的，国内网络可预置 timesyncd.conf 加速
4. **备份是安全网**：升级前快照、Google Drive 世代备份、3-2-1 规则
5. **正确重启**：避免非正常断电导致数据库损坏
6. **NTP/DNS 国内化** 是"稳定"的隐性基础（证书、自动化、更新全依赖时间）

### 时效性风险
- Docker 公益镜像站隔天失效常见 → 教程提供多源清单 + 故障转移思想
- HAOS-CN 版本/校验标注不一致（ihost、rpi5）→ 教程标注"以官方站为准"
- udev 覆盖方案已随版本失效 → 不推荐作为主线，仅作原理说明
- 错误码表来自社区博客 → 标注"以实际日志为准"
