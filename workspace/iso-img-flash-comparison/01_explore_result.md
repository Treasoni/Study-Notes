# ISO 与 IMG 镜像烧录/写盘方法对比 — 探测结果（P1）

> 运行：iso-img-flash-comparison（learning-note-flow P1）
> 日期：2026-09-09
> 方法：3 个并行透镜 subagent 探测，候选源按官方文档 > 高可信报告 > 社区实操排序。

---

## 方向菜单

以下方向来自 3 个透镜，互补不冲突，可任选其一为主，或综合。

- **方向 A：写盘工具实操对比** —— balenaEtcher / Rufus / dd / Ventoy 对 ISO 与 IMG 的处理是否一致
  - 关键线索：Etcher 对 .img/.iso 一律逐位写入、无差别；Rufus 区分 ISO Image 模式（解包重建）与 DD Image 模式（逐扇区直写）；Ventoy 对普通 ISO 拷贝即启动、对 OpenWrt IMG(vdisk) 需插件；dd 不解析内容、只做块级拷贝。
- **方向 B：物理机刷机流程对比** —— ISO 刻 U 盘「启动安装」 vs IMG 全盘写入「即开即用」
  - 关键线索：Ubuntu/Windows 走安装器流程；OpenWrt/iStoreOS/Raspberry Pi 走写镜像即启动、无安装向导。
- **方向 C：虚拟机镜像流程对比** —— ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入直启（PVE 为主）
  - 关键线索：PVE `qm importdisk` 导入为 unused 磁盘再挂载设引导；virt-install 区分 `--cdrom/--location/--import` 三条路径。
- **方向 D：综合对比（推荐）** —— A+B+C 合并为一份「操作是否相同」的总对照 + 分场景速查

---

## 候选源记录（按透镜分组）

### 透镜 A：写盘工具对 ISO / IMG 的处理

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| A1 | [balenaEtcher User Documentation](https://etcher-docs.balena.io/USER-DOCUMENTATION/) | 官方文档 | Etcher 对 .img/.iso 均逐位写入、不转换，处理无差别；Windows ISO 建议改用 Rufus/WoeUSB | 未知 | 5 |
| A2 | [Rufus Issue #843: ISO Image Mode vs DD Image Mode](https://github.com/pbatard/rufus/issues/843) | 官方文档 | 维护者确认 Rufus 区分 ISO 模式（解包重建）与 DD 模式（逐扇区直写）；.img/raw 应走 DD | 未知 | 5 |
| A3 | [Ventoy OpenWrt IMG 直启文档](https://www.ventoy.net/cn/doc_openwrt.html) | 官方文档 | IMG(vdisk) 与 ISO 差异：OpenWrt 需 ventoy_openwrt.xz 插件，仅部分 img 可直启 | 未知 | 5 |
| A4 | [GNU Coreutils 手册：dd 调用](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html) | 官方文档 | dd 只做块级转换拷贝、不解析内容，对 iso/img 无差别；差异只在目标是整盘还是普通文件 | 未知(Coreutils 9.11) | 4 |
| A5 | [Ventoy 官网首页（EN）](https://www.ventoy.net/en/index.html) | 官方文档 | 产品定位：ISO/WIM/IMG/VHD(x)/EFI 免解压拷贝即启动（已测 1400+ 镜像） | 2026-07 | 3 |

**透镜 A 缺口**：缺单一权威源做四种工具并排对比；Rufus 对 VHD/VHDX 语义官方表述模糊；Ventoy 对 iStoreOS/RAW 等其它 IMG 无官方限制说明。

### 透镜 B：物理机刷机流程对比

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| B1 | [iStoreOS X86 物理机安装官方文档](https://doc.linkease.com/zh/guide/istoreos/install_x86.html) | 官方文档 | .img.gz 用 Rufus 写入 U 盘 → U 盘引导 live → quickstart Install X86 装到内置盘 | 未知 | 5 |
| B2 | [Ubuntu 官方教程 Create a bootable USB stick on Windows](https://ubuntu.com/tutorials/create-a-usb-stick-on-windows) | 官方文档 | ISO 经 Rufus 写入 U 盘 → 启动进入 Try/Install Ubuntu 安装器 | 未知 | 5 |
| B3 | [OpenWrt 官方文档 Installing OpenWrt on x86](https://openwrt.org/docs/guide-user/installation/openwrt_x86) | 官方文档 | combined .img 解压后用 dd/Rufus/Etcher 整盘写入，无安装向导、写后即启动 | 未知 | 5 |
| B4 | [Raspberry Pi 官方文档 Installing OS images](https://github.com/raspberrypi/documentation/blob/master/documentation/asciidoc/computers/getting-started/install.adoc) | 官方文档 | Raspberry Pi Imager 把系统 .img 写入 SD 卡即启动，无独立安装器 | 未知 | 4 |
| B5 | [Rufus 官方 FAQ（ISO/DD Image mode）](https://github.com/pbatard/rufus/wiki/FAQ) | 官方文档 | ISO 模式重建分区与引导、DD 模式逐字节克隆；解释 ISOHybrid 双写法分界 | 未知 | 4 |

**透镜 B 缺口**：缺官方来源把「安装器式 ISO」与「整盘镜像」两种范式并列对照；IMG 直写后扩展分区、UEFI/GPT 细节分散；balenaEtcher、MS 官方介质工具未取到可验证文档链接。

### 透镜 C：虚拟机镜像流程对比

| # | 标题 | 来源 | 相关度 | 日期 | 分 |
|---|------|------|--------|------|----|
| C1 | [Proxmox VE qm 手册（qm.1.html）](https://pve.proxmox.com/pve-docs/qm.1.html) | 官方文档 | `qm importdisk` 将 raw/qcow2/vmdk 导入为 unused 磁盘；ZFS 仅收 raw | 未知(滚动) | 5 |
| C2 | [virt-install(1) 手册](https://manpages.ubuntu.com/manpages/jammy/man1/virt-install.1.html) | 官方文档 | 区分 --disk、--cdrom（物理光驱引导）、--location、--import（跳过安装直启既有镜像） | 未知(Ubuntu 22.04) | 5 |
| C3 | [QCOW2 Image - Import in Proxmox VE（Thomas-Krenn）](https://www.thomas-krenn.com/en/wiki/QCOW2_Image_-_Import_in_Proxmox_VE) | 高可信报告 | 实操：qcow2 经 qm importdisk 导入 → 挂载 unused → 设启动顺序 | 未知 | 4 |
| C4 | [PVE 官方补丁：import storage + import-from](https://lore.proxmox.com/all/20250408142239.3527806-1-d.csapak@proxmox.com/) | 官方文档 | 创建 VM 时直接引用 qcow2/raw/vmdk 自动复制转换的最新导入法 | 2025-04 | 4 |
| C5 | [virt-manager #296: --cdrom vs --location](https://github.com/virt-manager/virt-manager/issues/296) | 社区实操 | 维护者澄清 --cdrom 整盘引导 ISO、无法传内核参数、Windows ISO 只能用此 | 未知 | 3 |

**透镜 C 缺口**：PVE GUI 挂 ISO 安装 guest OS 无独立官方分步页；img→unused→attach 边界散落官方论坛；VirtualBox attach ISO vs raw 镜像的系统对比未纳入。

---

## Coverage Gaps（综合）

1. 缺「ISO vs IMG 写盘操作」单一权威总对照 → 需 P2 多源拼合。
2. Rufus VHD/VHDX、Ventoy 非 OpenWrt IMG（iStoreOS/RAW）官方限制说明薄弱。
3. PVE GUI 图形化安装路径官方分步文档命中率低（qm CLI 与第三方 wiki 可补）。
4. Windows 官方介质工具（Media Creation Tool）链路未验证。

## P2 范围估算

- 按方向选择取 3–5 个核心源深读（建议至少含 A1-A3、B1/B3、C1-C2）。
- 补源仅针对上述显式缺口，避免扩散。
- 产出 `02_deep_research.md`：scope、source table、claim/source map、contradictions、practical guidance、open questions。
