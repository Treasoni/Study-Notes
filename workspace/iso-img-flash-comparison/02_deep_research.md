# ISO 与 IMG 镜像烧录/写盘方法对比 — 深度素材（P2）

> 运行：iso-img-flash-comparison（learning-note-flow P2，方向 D 综合对比）
> 日期：2026-09-09
> 生成方式：crawl4ai 抓取 8 个官方源 + 3 个并行精读 agent 提取 claim 级笔记

---

## 1. Scope

回答用户问题「ISO 与 IMG 镜像烧录/写盘的方法和操作是否一样」：
- 维度 1：主流写盘工具（Etcher / Rufus / Ventoy / dd）是否对 ISO 与 IMG 一视同仁
- 维度 2：物理机刷机两种范式（ISO 安装器式 vs IMG 成品盘式）
- 维度 3：虚拟机两种用法（ISO 虚拟光驱安装 vs IMG/raw/qcow2 磁盘导入直启）
- 收敛为：操作差异的本质 = 镜像文件结构（安装介质 vs 整盘镜像）决定处理方式，工具/平台只是放大了这一差异。

## 2. Source Table

| ID | 标题 / URL | 层级 | 状态 | 覆盖 |
|----|-----------|------|------|------|
| S1 | balenaEtcher 官方用户文档 https://etcher-docs.balena.io/USER-DOCUMENTATION/ | 官方 | 已深读 | Etcher 逐字节写盘、不转换；Windows ISO 例外；Ubuntu isohybrid |
| S2 | Rufus Issue #843 (ISO vs DD mode) https://github.com/pbatard/rufus/issues/843 | 官方仓库 | 部分（仅开帖正文，无维护者回复） | 用户侧困惑；官方结论以 S3 为准 |
| S3 | Rufus 官方 Wiki FAQ https://github.com/pbatard/rufus/wiki/FAQ | 官方 | 已深读（大文件按关键词精读） | ISO Image mode vs DD Image mode；isohybrid 坑；OpenBSD ISO 需换 .img |
| S4 | Ventoy 官方 OpenWrt/IMG 直启文档 https://www.ventoy.net/cn/doc_openwrt.html | 官方 | 已深读 | Ventoy 拷贝+菜单引导；IMG 需 ventoy_openwrt.xz；支持范围仅特定 OpenWrt img |
| S5 | iStoreOS X86 物理机安装官方文档 https://doc.linkease.com/zh/guide/istoreos/install_x86.html | 官方 | 已深读 | IMG 式物理机刷机完整流程（.img.gz→Rufus→U盘启动→quickstart→写内置盘） |
| S6 | OpenWrt 官方 Installing OpenWrt on x86 https://openwrt.org/docs/guide-user/installation/openwrt_x86 | 官方 | ❌ 不可读（Anubis PoW 反爬拦截，JS 重试仍失败） | 缺口：需人工复核 |
| S7 | Ubuntu 官方 Create a bootable USB stick (Rufus) https://ubuntu.com/tutorials/create-a-usb-stick-on-windows | 官方 | 已深读 | ISO 式流程；ISOHybrid 提示保留 ISO Image mode；启动后进安装器 |
| S8 | Proxmox VE qm 手册 https://pve.proxmox.com/pve-docs/qm.1.html | 官方 | 已深读（关键词定位 importdisk/cdrom） | `qm disk import`、`import-from`、`-cdrom`、boot order、cloud-init |
| S9 | virt-install(1) 手册 https://manpages.ubuntu.com/manpages/jammy/man1/virt-install.1.html | 官方 | 已深读（关键词定位） | `--cdrom` / `--location` / `--import` / `--disk` device=cdrom |

补充阅读（P1 候选但未深读）：Raspberry Pi 官方 img 写卡文档、Thomas-Krenn qcow2 导入指南、virt-manager #296（--cdrom vs --location）。

**Tier mix：官方 8 / 高可信 0 / 社区 0（已深读）；官方文档为主，无社区依赖。**

## 3. Claim / Source Map

### Q1 工具对 ISO 与 IMG 是否一视同仁？→ 否，差异明显

| Claim | 来源 |
|-------|------|
| balenaEtcher 对镜像**逐字节复制、不做转换**，.iso/.img 无模式之分，写盘方式一致 | S1 |
| Etcher 无转换，因此依赖镜像自身可引导；**Windows 等需特殊处理的 ISO 不适用**，官方建议换 Rufus/WoeUSB | S1 |
| Ubuntu 等发行版 ISO 是**混合镜像（isohybrid）**，同一文件可作 DVD 与 U 盘引导，无需工具转换 | S1, S7 |
| Rufus 区分 **ISO Image mode（解包重建文件系统/分区）** 与 **DD Image mode（逐扇区直写磁盘镜像）** | S3 |
| Rufus 对 **.img 磁盘镜像统一走 DD 模式**；OpenBSD 只有 ISO 时官方建议改用 .img 走 DD | S3 |
| Rufus 对 **isohybrid ISO 默认推荐 ISO 模式**而非 DD：DD 会使 U 盘容量变小、Windows 无法挂载后续分区、破坏 least astonishment | S3 |
| DD 写 GPT isohybrid 会因备份 GPT 位置问题被部分挑剔 UEFI 拒启；内嵌校验在 DD 后可能失败 | S3 |
| Ventoy **不烧录**：把 ISO/IMG 作为文件放入分区，由引导菜单启动 | S4 |
| Ventoy 对 ISO 普遍“拷贝即启动”；对 OpenWrt **IMG(vdisk) 需 ventoy_openwrt.xz 插件**（补 dm 内核模块），且仅支持 x86 combined-ext4/combined-squashfs 两种 | S4 |
| GNU dd 是块级“转换并拷贝”，不解析内容；对 iso/img 本身无差别，差异在**目标是整块设备还是普通文件** | P1-A4（推论，未 P2 深读） |

### Q2 物理机刷机：两种范式

| Claim | 来源 |
|-------|------|
| **IMG 式（成品盘）**：固件 `xxx.img.gz` 即完整可启动磁盘镜像，官方下载后**不解压** | S5 |
| Windows 下用 Rufus 选该固件写入 U 盘做启动盘（IMG 走整盘写入）；目标机 U 盘引导 | S5 |
| 引导后进入**临时 live 系统**，运行 `quickstart` → 选 **Install X86** → 写入内置磁盘，拔盘即直启，无二次安装器 | S5 |
| iStoreOS 默认后台 http://192.168.100.1/，默认密码 password（多网口默认第一口 WAN） | S5 |
| **ISO 式（安装器）**：Ubuntu 官方教程用 Rufus 选 ISO，遇 **ISOHybrid 提示保留 “Write in ISO Image mode”** | S7 |
| 写完后目标机从 U 盘启动，进入 **Try/Install** 安装器，需完成安装向导才能得到系统 | S7 |
| 本质：IMG 是“**预装系统的整盘克隆**”，写入即完成；ISO 只负责**引导安装程序**，最终系统由安装器现场生成 | S5+S7 综合 |

### Q3 虚拟机：两种用法

| Claim | 来源 |
|-------|------|
| **ISO 安装路径**：镜像须先传至存储的 iso 区；创建 VM 时 `-cdrom`（实为 ide2 media=cdrom 别名）挂为只读光驱 + `-ide0` 空盘；由安装器写入空盘 | S8 |
| virt-install 侧对应：`--cdrom`（整盘式引导 ISO，不能传内核参数）或 `--location`（仅取最小 kernel/initrd 远程安装，可 `--extra-args`） | S9 |
| **磁盘镜像直启路径**：`qm disk import <vmid> <source> <storage> [--format qcow2\|raw\|vmdk]` 先导入为 **unused 磁盘**，再绑定控制器槽位并设引导顺序，无安装阶段 | S8 |
| PVE 新写法：`qm create/set` 磁盘参数 `import-from=…` **导入即挂盘**，无需先建空盘 | S8 |
| 直启建议 `-scsihw virtio-scsi-pci` + `-boot order=scsi0`；cloud-init 镜像额外 `-ide2 …:cloudinit` | S8 |
| virt-install 侧对应：`--import` 完全跳过安装、以第一个 `--disk` 作为引导设备直启既有镜像 | S9 |
| 介质与系统盘在同一 `--disk` 体系内用 `device=cdrom` vs 默认 `device=disk` 区分 | S9 |

### Q4 为什么不一样（结构层解释，多源拼合）

| Claim | 来源 |
|-------|------|
| ISO 本质是**光盘文件系统镜像**（光学介质），isohybrid 通过在镜像尾部附加分区表/引导让其也能从 U 盘引导——它仍是“安装介质” | S1, S7, S3 |
| IMG/raw 本质是**整块磁盘的扇区镜像**：自带分区表（GPT/MBR）+ 引导 + 文件系统 + 系统，写盘后可直接被 BIOS/UEFI 启动 | S5, S8, P1-A3 推论 |
| 因此 ISO 是否可按“磁盘镜像”方式处理，取决于工具是否做转换 + 镜像是否 isohybrid（Rufus 两种模式正是对该分界的管理） | S3, S1 |
| Ventoy 把两者都“当文件”，反而暴露 IMG 需要内核模块（dm）等**运行期依赖**才能被 GRUB 菜单启动 | S4 |

## 4. Contradictions

1. **Etcher “逐字节即可、无需转换” vs Rufus “isohybrid 用 DD 模式有坑，默认 ISO 模式”**：Etcher 是纯整盘写入器（等价于 Rufus DD 模式），对 isohybrid ISO 它能用但会丢掉 ISO 模式带来的“可分盘/可扩容”便利，Rufus 因此默认不推荐 DD。→ 表述为“两种工具哲学不同”，而非 Etcher 错误。
2. **Ventoy “IMG 也能拷入 U 盘直启” vs 传统烧录 “IMG 必须逐扇区写盘”**：Ventoy 成立有前提——仅特定 OpenWrt x86 img + 插件补内核模块，不可外推到所有 IMG（如 iStoreOS 固件 Ventoy 官方未承诺）。
3. **S6 OpenWrt 官方页不可读**：不能引用其正文，IMG 物理机路径以同源 iStoreOS 官方文档代表（OpenWrt 系固件流程一致：img.gz→写盘→引导）。

## 5. Practical Guidance

- **先判断镜像类型**：`.iso` 优先视为安装介质；`.img`/`.raw` 一律视为磁盘镜像（整盘写入或导入）。
- **工具速查**：
  - **Rufus**：发行版 ISO → ISO Image mode（默认）；.img/.raw → 自动走 DD 模式；注意 GPT isohybrid 别用 DD。
  - **balenaEtcher**：ISO 与 IMG 都整盘写，无选项；**勿用于 Windows ISO**。
  - **Ventoy**：把 ISO 当文件拷贝即启；OpenWrt img 需 ventoy_openwrt.xz，仅限特定镜像。
  - **dd**（命令行）：`dd if=x.img of=/dev/sdX bs=4M status=progress conv=fsync`，目标**整盘**非分区。
- **物理机**：
  - 刷成品软路由固件（iStoreOS/OpenWRT 系）→ 解压 `.img.gz` → Rufus/Etcher/dd 写 U 盘或直写目标盘 → 引导后 quickstart/自动展开。
  - 装通用系统（Windows/Ubuntu）→ ISO 写 U 盘 → 启动进入安装器。
- **虚拟机**：
  - ISO → 挂虚拟光驱 + 新建空盘，让安装器落盘（PVE `-cdrom` / virt-install `--cdrom`/`--location`）。
  - IMG/raw/qcow2 → `qm importdisk` 导入 unused → attach → boot order；或新法 `import-from`；virt-install `--import` 直启。
- **回答原问题**：**“方法和操作”不能一概而论**——在“工具层”Etcher/dd 对两者操作几乎一样，Rufus 则区分两种模式；在“流程层”物理机/虚拟机的 ISO 路径都要“先安装”，IMG 路径“导入即启动”。相同的是最终都落在“把镜像变成可启动介质/磁盘”上，不同的是 ISO 多一步安装器、IMG 直接是成品。

## 6. Open Questions / Gaps

1. OpenWrt 官方 x86 页面被 Anubis 拦截（S6）→ 建议人工浏览器复核或改用镜像站。
2. Rufus Issue #843 仅抓到用户提问正文，维护者回复未抓到；官方结论以 FAQ（S3）为准。
3. Ventoy 对 iStoreOS / img.gz / 其它 raw 镜像的官方支持说明缺失（官方只承诺 OpenWrt 两类 img）。
4. Rufus 对 VHD/VHDX “可写镜像”与仅枚举目标盘语义在 FAQ 中表述模糊，不影响本主题主线。
5. dd 的写盘细节（bs/conv 参数）基于通用知识，未在 P2 深读 GNU manual（如需精确引用可补抓）。

## 7. Downstream Handoff

- **大纲输入（03_outline）**：建议章节骨架 = ① 一句话结论 → ② 镜像结构差异（为什么不同）→ ③ 工具层对比（Etcher/Rufus/Ventoy/dd）→ ④ 物理机两种流程 → ⑤ 虚拟机两种流程 → ⑥ 速查表与坑。全文应**双链 [[iso和img.md]]** 作为“概念篇”。
- **结论可复用**：工具是否一致（视工具）+ 流程是否一致（视场景：安装器 vs 成品盘）。
- **引用素材**：见上表 source IDs；正文引用保留 URL 与官方名即可。
