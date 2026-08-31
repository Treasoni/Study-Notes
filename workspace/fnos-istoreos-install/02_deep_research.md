# 飞牛上安装配置 iStoreOS（软路由）- 深度研究素材

> 主题：在飞牛 NAS 上通过虚拟机安装 iStoreOS 作为软路由（旁路由）
> 阶段：P2 深度收集
> 创建时间：2026-09-01
> 方向：A 完整主线（建 VM → 导入 iStoreOS → 配旁路由）
> 笔记类型：实战教程 ｜ 深度：上手

---

## 1. 研究范围与结论速览

在飞牛 fnOS 上通过**虚拟机**安装 iStoreOS 作为**旁路由/软路由**的完整可行路径已确认，存在**两条主流安装路线**：

- **方法 A（官方论坛精华帖，推荐新手）**：在 fnOS 虚拟机 UI 中**直接导入 img 镜像** → quickstart 初始化 → 网络向导配成旁路由。依赖 fnOS 虚拟机 v0.9.0+（已支持 img/img.gz/qcow2 直接导入）。
- **方法 B（temp ISO + SSH virsh，偏进阶）**：用官方预制 `fnOS_temp.iso` 引导虚拟机，再通过 SSH `virsh attach-disk` 挂载正式 iStoreOS 的 efi 镜像。适用于 UI 直导引导失败或想用 UEFI/efi 固件的场景。

官方文档（iStoreOS 与飞牛 help）提供了完整的旁路由三种方案、网络排错与硬件直通前提，社区帖补充了大量真实踩坑点。

---

## 2. 来源表

| ID | 来源 | 发布方 | 层级 | 日期 | 状态 |
|----|------|--------|------|------|------|
| S1 | [如何安装和使用虚拟机？](https://help.fnnas.com/articles/v1/virtual-machine/install) | 飞牛官方帮助中心 | tier1 | 持续更新 | ✅ 已抓取 |
| S2 | [如何使用虚拟机硬件直通？](https://help.fnnas.com/articles/v1/virtual-machine/passthrough) | 飞牛官方帮助中心 | tier1 | 持续更新 | ✅ 已抓取 |
| S3 | [x86 物理机安装 iStoreOS](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html) | iStoreOS 官方文档 | tier1 | — | ✅ 已抓取 |
| S4 | [如何更好地使用旁路由](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html) | iStoreOS 官方文档 | tier1 | 持续更新 | ✅ 已抓取 |
| S5 | [Merlin 跟 iStoreOS 网络问题排查](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html) | iStoreOS 官方文档 | tier1 | 持续更新 | ✅ 已抓取 |
| S6 | [iStoreOS x86_64 固件仓库](https://fw.koolcenter.com/iStoreOS/x86_64/) | iStoreOS / KoolCenter | tier1 | 持续更新 | ✅ 已抓取 |
| S7 | [万物皆可 iStoreOS](https://site.istoreos.com/about) | iStoreOS 官网 | tier1 | — | ✅ 已抓取 |
| S8 | [飞牛虚拟机部署 iStoreOS 做旁路由教程](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481) | 飞牛官方论坛（精华帖） | tier2 | 2025-05 | ✅ 已抓取 |
| S9 | [飞牛 fnOS 安装 iStoreOS 作为软路由（旁路由）](https://blog.csdn.net/u013262414/article/details/155347617) | CSDN 个人博客 | tier3 | 2025-11 | ✅ 已抓取 |
| S10 | [fnOS 虚拟机 v0.9.0 支持 img 等格式](https://www.ithome.com/0/855/243.htm) | IT之家 | tier2 | 2025-05 | ✅ 已抓取 |
| S11 | [fnOS 虚拟 iStoreOS 软路由](https://mynas.chat/fnos/istoreos) | 个人站 | tier3 | 2025-01 | ⚠️ P1 候选，未抓取 |
| S12 | [旁路由·手动静态 IP 方案](https://www.koolcenter.com/t/topic/797) | 酷友社论坛 | tier2 | — | ⚠️ P1 候选，未抓取 |
| S13 | [旁路由防火墙设置](https://www.koolcenter.com/t/topic/2681) | 酷友社论坛 | tier2 | — | ⚠️ P1 候选，未抓取 |
| S14 | [折腾 qwrt 旁路由经验（NAS/容器互通）](https://club.fnnas.com/forum.php?mod=viewthread&tid=59080) | 飞牛私有云论坛 | tier3 | — | ⚠️ P1 候选，未抓取 |

层级分布：tier1×7、tier2×3、tier3×4。核心官方一手来源已全部抓取；S11-S14 作为补充参考，未抓取但相关性已在 P1 记录。

---

## 3. 核心概念

### 3.1 iStoreOS 是什么（S7）
- 基于 **OpenWrt 深度优化**的开源智能路由系统，保留 OpenWrt 灵活性，简化交互、增强稳定性。
- 内置 **iStore 软件中心**，一键安装应用；支持 **Docker**（Jellyfin/Emby、HomeAssistant 等）。
- 全开源、多硬件适配、安全沙箱。

### 3.2 软路由 / 旁路由（S4）
- 旁路由 = 在主路由器上**通过 LAN 口接入**一台额外路由设备（如 iStoreOS），分担特定网络任务，**不直接连接互联网**，也不改变主网络拓扑与 IP。
- 数据流控制靠**网关设置**实现：手动指定设备 IP 或由 DHCP 分配。

### 3.3 飞牛 fnOS 虚拟机前提（S1）
- 虚拟机是 fnOS **应用中心**里的一个应用，安装后桌面出现图标。
- 需为宿主网络连接**启用 OVS**（Open vSwitch）提供隔离虚拟网络；**仅有线网口和聚合网口支持 OVS，无线网口不支持**。
- 需在 **BIOS/UEFI 开启硬件虚拟化**：Intel VT-x / AMD SVM(AMD-V)。
- Linux 系统（含 OpenWrt/iStoreOS）**自带 VirtIO 驱动**，不需要额外装驱动。

### 3.4 硬件直通（S2）
- 允许 VM 直接访问物理硬件（显卡/声卡/USB/**网卡**），性能更高但**有风险**。
- 前置：BIOS 开 VT-x/AMD-V + **IOMMU**（Intel VT-d / AMD-Vi），GRUB 声明 IOMMU、禁设备驱动加载、IOMMU 分组隔离。
- ⚠️ 网卡直通风险：**必须确保宿主机保留可用网卡**，否则宿主机断网失联。非专业用户不建议。

---

## 4. 主线安装流程（方法 A：UI 直导 img）【S8 为主】

### 4.1 准备
1. 从 [fw.koolcenter.com/iStoreOS/x86_64/](https://fw.koolcenter.com/iStoreOS/x86_64/) 下载最新 x86_64 镜像（如 `istoreos-24.10.8-2026073111-x86-64-squashfs-combined.img.gz`，约 230 MiB）。
   - 命名规律：`istoreos-{版本}-{日期}-x86-64-squashfs-combined.img.gz`；越前面越新，选日期最新。
   - 官方 x86 实机文档 S3：下载后**不需要解压**（Rufus/Ventoy 写盘时直接选 gz）。但**导入飞牛虚拟机时，S8 教程是解压成 img 后导入**（见 7.3 矛盾点）。
2. 把 img.gz 上传到飞牛任意目录，**解压出 img 文件**。

### 4.2 创建虚拟机（S8 + S1）
1. 应用中心安装「虚拟机」应用；系统设置 → 网络管理 → 启用 OVS。
2. 打开虚拟机应用 → 创建虚拟机 → 名称 + 操作系统类型（Linux）。
3. 选择刚解压的 **img 镜像** → 下一步 → **格式转换**（耐心等待）。
4. 添加储存空间：第一个虚拟磁盘初始 `2433 MB` **创建时不可改/不可删**，创建后可编辑扩容；可再加磁盘（最多 8 个）。
5. 添加网卡：多网口小主机可加多个（选 OVS 网口、网络类型、MAC）。
6. 硬件直通：可选，用不到就下一步。
7. 完成创建后，**先不启动**，编辑虚拟机 → 磁盘 → 把 2433 MB 扩容（iStoreOS 一般 **20G 足够**）。

### 4.3 安装与初始化（S8）
1. 开机，通过 **VNC** 连接访问。
2. 等待自动安装镜像，出现提示时**敲回车**。
3. 输入 `quickstart` 回车（或 `qu` + Tab 自动补全）。
4. 选 **Change LAN IP** → 设置**静态 IP**（局域网未被占用的 IP）+ **子网掩码**。
5. 浏览器访问该静态 IP；默认账号 `root` / 密码 `password`。
6. 若系统显示英文，终端执行修复（见 7.6）。

### 4.4 配置旁路由（S8 + S4）
1. 点击 **网络向导** → **配置为旁路由**。
2. 填入与前面一致的静态 IP、子网掩码、**网关地址**、DNS（默认阿里 DNS，可改）。
3. **关闭 DHCPv4 服务**；开启自动获取 IPv6（可选，后续可 DDNS 远程访问）。
4. 保存配置。首页右上角可看到静态 IP 与获取到的 IPv6 公网地址。

### 4.5 剩余空间与 Docker（S8）
1. 默认 iStoreOS 系统根目录**只占 2G**，其余空间需**手动格式化**：磁盘「三个点」→ 未分区 → 格式化。格式化后分区 `sda4`（挂载点 `/mnt/vio2-4`）。
2. **Docker 目录迁移**：快速配置 → 目录迁移到刚格式化的分区。

---

## 5. 备选安装流程（方法 B：temp ISO + SSH virsh）【S9】

适用：UI 直导引导失败，或想用 **UEFI/efi 固件**、走 virsh 精确控制。

1. 下载两个镜像：
   - 预制引导包 `fnOS_temp.iso`：<https://fw0.koolcenter.com/iStoreOS/Virtual/fnOS_temp.iso>
   - 正式 efi 镜像：<https://fw.koolcenter.com/iStoreOS/x86_64_efi/>（如 `istoreos-24.10.4-…-x86-64-squashfs-combined-efi.img.gz`）
   - 上传到飞牛，**记录镜像所在目录路径**（后续 SSH 要用，如 `/vol1/1001/downloads/`）。
2. 飞牛：系统设置 → 开启 **SSH**（仅管理员账户）；安装虚拟机套件；开启 OVS。
3. 新建虚拟机：操作系统选 **Linux，6.x-2.6 kernel**；**主板固件必须选 UEFI**；系统镜像选 temp ISO。
4. SSH 连接 fnOS（`ssh 用户@飞牛IP`）→ `sudo -i` → 进入镜像目录 → 解压：
   ```bash
   cd /vol1/1001/downloads/
   gzip -d istoreos-24.10.4-…-x86-64-squashfs-combined-efi.img.gz
   ```
5. 挂载 img 到 VM：
   ```bash
   virsh list --all
   virsh attach-disk <VM名> /vol1/1001/downloads/…-efi.img vdb --driver qemu --subdriver raw --persistent
   ```
6. 回到虚拟机 UI 编辑，确认新增磁盘，开机 → VNC。
7. `quickstart` → 设 IP → 浏览器访问 → 设置管理员密码 → 网络配置（旁路由）。

---

## 6. 网络配置（旁路由核心规则）【S4 + S5】

### 6.1 官方三种旁路由方案（S4）
| 方案 | 主路由 | 旁路由 | 优点 |
|------|--------|--------|------|
| 手动静态 IP | 任意路由，默认开 DHCP | iStoreOS **关 DHCP** | 最简单、适合新手 |
| 旁路由 DHCP 接管 | 任意路由，**关 DHCP**、网关设旁路由 | iStoreOS **开 DHCP** 全面接管 | 适应性最广 |
| (华硕)浮动网关 | 华硕 ASUSGO 固件 | iStoreOS + 浮动网关插件 | 自动切换 |

**铁律（S5）**：一个局域网**不能同时存在两个 DHCP**。

### 6.2 让设备走旁路由（S8 回帖 / S12）
- 需要走旁路由的设备：改成**手动 IP**，**网关和 DNS 都指向旁路由的 IP** 即可。
- 不需要多网口机器；**单网口也可以**做旁路由。

### 6.3 无法上网排查（S5）
1. 「网络 → 接口 → LAN」**使用默认网关**确保打勾。
2. 「网络 → 防火墙 → 区域里的 LAN」把 **IP 动态伪装**打勾（小米等主路由常见）。
3. 单 LAN 口设备（如树莓派形态）只能用「旁路由配置向导」设为固定 IP。

---

## 7. 常见坑与排错汇总（社区实操）

| # | 现象 | 原因/解决 | 来源 |
|---|------|-----------|------|
| 7.1 | iStoreOS img.gz **直接导入飞牛引导失败**（报错）；immortalwrt 可直导 | iStoreOS 的 gz 压缩格式特殊；**先解压成 img 再导入**；或改试方法 B | S8 回帖 |
| 7.2 | VNC 黑屏无显示，但可通过 IP 访问 | 正常现象，改用浏览器访问 | S8 回帖 |
| 7.3 | 虚拟机**启用 OVS 后重启宿主失联** | OVS 配置导致网络中断；注意保留可用管理网卡 | S8 回帖 |
| 7.4 | 默认 192.168.100.1 访问不了后台 | 确认 LAN 口与网段；用 quickstart 改同网段静态 IP | S3/S8 |
| 7.5 | 改 LAN IP 后**重启又恢复** 192.168.100.1 | 配置未保存/未生效；重新走网络向导保存 | S8 回帖 |
| 7.6 | 系统显示**英文无中文** | 终端执行：`uci set luci.languages.zh_cn='中文 (Chinese)'; uci set luci.main.lang='zh_cn'; uci commit luci` | S8 回帖 |
| 7.7 | 固件默认**无科学上网插件** | 官方默认固件不含，需自行下载安装（Are-u-ok 等） | S8 回帖 |
| 7.8 | 磁盘根目录只有 2G 空间 | 其余空间需手动格式化后挂载，Docker 目录迁移 | S8 |
| 7.9 | 网卡直通导致宿主失联 | 直通前**保留宿主可用网卡**；需要 IOMMU/VT-d；非专业用户不建议 | S2 |
| 7.10 | 设置后设备无法上网 | 网关/DNS 指向；LAN 默认网关打勾；防火墙 IP 动态伪装 | S5/S8 |

---

## 8. 矛盾点与待核实

1. **img 直导 vs 解压后导入**：S3（官方实机文档）说下载后不需解压；S8（飞牛论坛教程）在 VM 导入前先解压成 img；S8 回帖反馈 iStoreOS img.gz 直导有时引导失败。→ 写作时建议主流程「先解压成 img 导入」，并提示若直导失败可用方法 B。
2. **默认密码**：S3 官方说默认 `password`；S9（CSDN）说初始未设密码、直接登录再设置。跨版本/跨固件存在差异 → 写作时标注「默认 root/password，若无则直接登录后设置」。
3. **固件版本差异**：22.03.x 与 24.10.x 并存，UI 与默认行为可能不同（S6 目录同时含两系列）。
4. **fnOS 底层/虚拟化实现**：社区普遍认为 fnOS 基于 Debian、虚拟机基于 KVM/libvirt（S9 用 virsh 佐证），但官方无单点说明 → 标注为社区推断。

---

## 9. 开放问题

1. 用户手上飞牛的**硬件形态**（单网口小主机 / 多网口 / 已有独立主路由）？影响旁路由拓扑选择与是否走网卡直通。
2. 是否已有**独立主路由**？旁路由方案需要主路由配合（关 DHCP 或设备改网关）。
3. 是否需要 **Docker/科学上网/DDNS** 等进阶配置？（决定教程是否扩展）
4. 飞牛 fnOS 当前**虚拟机版本**是否 ≥ v0.9.0？（决定能否用方法 A 直导 img）

---

## 10. 下游交接（大纲/写作要点）

- **章节建议（实战教程，≤3 级层级）**：
  1. 概念与方案选型（iStoreOS/软路由/旁路由；方法 A vs B）
  2. 前置准备（固件下载、fnOS 虚拟机应用、OVS、BIOS 虚拟化）
  3. 方法 A：创建虚拟机并导入 iStoreOS
  4. 初始化与后台访问（quickstart、改 IP、默认账号）
  5. 配置旁路由（网络向导、DHCP 规则、设备走旁路由）
  6. 进阶：磁盘扩容、Docker 目录迁移、硬件直通（可选）
  7. 常见问题排查（7.x 表）
- **必须引用官方一手来源**：S1/S2（飞牛）、S3/S4/S5/S6/S7（iStoreOS）。
- **实操类声明标注社区来源**：S8（论坛精华帖）、S9（CSDN）、S12-S14（补充）。
- 所有默认密码、固件文件名、路径等写「以官方最新页面为准」。

---
*抓取缓存：`workspace/fnos-istoreos-install/.research_cache/*.md`（10 个来源全文）*
