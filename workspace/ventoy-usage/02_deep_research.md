# Ventoy 使用实战 — 阶段 2 深度研究

> 运行：`ventoy-usage`（learning-note-flow）｜主题：如何使用 Ventoy（多系统启动U盘）
> 检索/抓取日期：2026-09-08｜抓取缓存：`cache/`（crawl4ai，4 个官方页）
> 方向：综合全流程（概念 → 安装制作 → 排错进阶）

## 范围

- 目标：为「上手会用 / 实战操作指南」提供可照做的事实底座。
- 覆盖：概念与原理、Windows/Linux 安装与升级、日常使用、Secure Boot/常见排错。
- 不深入：插件主题制作、从源码构建、持久化(persistence)深水区（可做一节进阶速览）。

## 来源表

| ID | 来源 | URL | 层级 | 日期 | 用途 |
|----|------|-----|------|------|------|
| S1 | 官方《Ventoy 使用说明（中文）》 | https://www.ventoy.net/cn/doc_start.html | official | unknown（©2020-2026） | 安装/升级主线、镜像拷贝、Linux CLI |
| S2 | 官方《磁盘布局（中文 MBR）》 | https://ventoy.net/cn/doc_disk_layout.html | official | unknown | 双分区结构、MBR/GPT、保留空间 |
| S3 | 官方 FAQ | https://www.ventoy.net/en/faq.html | official | unknown | 安装/启动/菜单/插件 FAQ 排错索引 |
| S4 | 官方《About Secure Boot》 | https://www.ventoy.net/en/doc_secure.html | official | unknown | Secure Boot 默认支持、key 注册流程 |
| S5 | GitHub Release：Ventoy 1.1.17 | https://github.com/ventoy/Ventoy/releases/tag/v1.1.17 | official | 2026-07-24 | 当前最新稳定版锚点（P1 经搜索核实） |
| S6 | Arch Wiki：Ventoy | https://wiki.archlinux.org/title/Ventoy | report | unknown | 交叉印证 Linux CLI 参数与升级流程 |
| S7 | Thomas-Krenn：Multi-ISO U 盘实操 | https://www.thomas-krenn.com/en/wiki/Creation_of_bootable_Multi-ISO_USB_stick_with_Ventoy | report | unknown | 第三方实操步骤佐证 |
| S8 | 博客园：制作启动U盘的工具——Ventoy | https://www.cnblogs.com/mq0036/p/17746092.html | community | unknown | 中文社区经验（Windows 为主） |

层级统计：official 5（S1-S5）｜report 2（S6-S7）｜community 1（S8）。

## 核心主张 → 来源映射

### 概念 / 原理
| 主张 | 来源 |
|------|------|
| 新一代多系统启动 U 盘方案：引导器只装一次，之后直接拷贝 ISO/WIM/VHD(x)/EFI 镜像到分区即可，免重复烧录 | S1 |
| 安装后磁盘分成两个分区：分区 1 = 镜像数据区（默认 exFAT，可改 FAT32/NTFS/UDF/XFS/Ext2/3/4）；分区 2 = 32MB VTOYEFI EFI 引导分区；另有 1MB MBR 间隙放 Legacy 启动文件 | S2 |
| 分区 2 放后面的原因：UEFI 规范要求 EFI 分区为 FAT；早期 Windows 只挂载 U 盘第一个分区，放第二分区可防误改 | S2 |
| Ventoy 默认递归搜索分区 1 所有目录/子目录的镜像文件，按字母排序显示在启动菜单 | S1、S3 |
| 镜像分区可兼作普通 U 盘存文件，不影响 Ventoy 功能 | S1 |
| 支持 x86 Legacy BIOS、IA32/x86_64 UEFI、ARM64 UEFI、MIPS64EL UEFI | S3 |
| 启动模式（Legacy/UEFI）由主板 BIOS 决定，Ventoy 不能自行选择 | S3 |

### 安装与制作
| 主张 | 来源 |
|------|------|
| Windows GUI：解压 `ventoy-*.zip` → 运行 `Ventoy2Disk.exe` → 选目标盘 → 点「安装」（仅首次需要） | S1 |
| ⚠️ 首次安装会格式化磁盘、清空全部数据；必须提前备份 | S1 |
| 默认只列出 U 盘；勾选「配置选项 → 显示所有设备」才会列出所有磁盘（含系统盘），选错会清空系统盘 | S1、S3 |
| 安装只做一次，之后用「升级」按钮更新；升级只覆盖 32MB VTOYEFI 引导文件，不动镜像分区，镜像不丢失、文件系统不被改回 exFAT | S1 |
| Linux CLI：解压 `ventoy-*.tar.gz`，`cd` 到该目录并以 root 执行 `sudo sh Ventoy2Disk.sh -i /dev/sdX`（-i 安装 / -I 强装 / -u 升级 / -l 查看信息）；选项：`-r SIZE_MB` 保留空间、`-s` 启用 Secure Boot 支持（默认关）、`-g` GPT（默认 MBR）、`-L` 卷标 | S1、S6 |
| Linux 必须 `cd` 到解压目录执行，务必确认设备名，Ventoy 不校验是 U 盘还是系统盘 | S1 |
| 镜像分区可在安装后重新格式化；普通 U 盘建议 exFAT，大容量移动硬盘/SSD 建议 NTFS（XFS/Ext 系仅适合纯 Linux，Windows 不可见） | S1、S2 |
| 安装时可预留磁盘末尾空间（Windows「分区设置」/ Linux `-r`）；保留空间只在安装时生效；分区 1/2 不可移动或改大小，保留空间可自建分区 3/4 | S2 |

### Secure Boot / 排错
| 主张 | 来源 |
|------|------|
| Secure Boot 自 1.0.76 起默认支持；Ventoy2Disk.exe 的 `Option → Secure Boot Support` 或 `.sh` 的 `-s` 可开关 | S4 |
| BIOS 开启 Secure Boot 时首次引导会进入蓝色 key 注册界面，按指引注册即可（每台电脑只需一次）；出现错误界面（如 Linpus lite）说明方案不兼容，需在 BIOS 关闭 Secure Boot | S4 |
| Ventoy 1.1.13+ 因 UEFI CA 2023 问题需重新注册新 key；部分机器需在固件开启 `Allow Microsoft 3rd Party UEFI CA` | S4 |
| Ventoy 默认策略是「完全绕过 Secure Boot」；要严格遵循 UEFI 策略需用 Global Control Plugin（VTOY_SECURE_BOOT_POLICY） | S4 |
| 启动菜单左下角标识当前模式：`BIOS`=Legacy、`UEFI`、`IA32`、`AA64`、`MIPS` | S3 |
| Ventoy2Disk.exe 找不到 U 盘/装失败：常因进程占用（Paragon ExtFS、DokanMounter、ext2fsd、DiskGenius、Intel DSA 等） | S3 |
| 启动进 grub shell 或失败：先排除扩容/假 U 盘、老主板 Legacy BIOS 访问范围限制（约 128GB）、镜像损坏（做 checksum） | S3 |
| 「Ventoy scanning files, please wait...」卡住：文件过多 → 用搜索路径配置；某目录放 `.ventoyignore` 文件可让 Ventoy 跳过该目录 | S3 |
| VTOYEFI 分区损坏导致无法启动：删除损坏分区（diskgenius/diskpart）→ 用 Non-destructive install（非破坏安装）修复 | S3 |
| `ventoy.json` 必须放在第一分区 `\ventoy\ventoy.json`，不要放进 32MB VTOYEFI | S3 |

## 矛盾与不确定

1. **Secure Boot 支持起始版本措辞不一**：FAQ 写「since Ventoy-1.0.07」，doc_secure 写「supported by default from 1.0.76」。判断：1.0.07 为早期实验支持，1.0.76 起默认开启。以 doc_secure 为准（S4 权威性更高），正文可写「1.0.76 起默认支持」。
2. **Ventoy 1.1.17 新特性细节未深挖**：S5 仅作版本/日期锚点，release notes 未抓取。若大纲需要「版本新特性」，需补抓。
3. **FAQ 折叠内容部分截断**：crawl 保留了可展开区块的首段，个别条目（如 fuzzy screen 详细说明）以官方对应专页为准。

## 实操要点提炼（给下游）

1. 下载：GitHub Releases 取最新 `ventoy-x.y.z-windows.zip` / `ventoy-x.y.z-linux.tar.gz`（当前 1.1.17，2026-07-24）。
2. Windows：解压 → `Ventoy2Disk.exe` → 选对盘 → 安装（会清空）→ 拷镜像到数据分区。
3. Linux：`sudo sh Ventoy2Disk.sh -i /dev/sdX`；Secure Boot 环境加 `-s`；后续 `-u` 升级。
4. 日常：镜像用「复制」增删；升级安全不动镜像；可当普通 U 盘用。
5. Secure Boot：首次引导注册 key；失败 → 关 Secure Boot / 换注册方式。
6. 排错索引：安装失败查占用进程；启动卡/花屏查搜索路径、镜像完整性、老机 Legacy 128GB 限制；VTOYEFI 损坏 → 非破坏安装。

## 开放问题

- Windows 命令行模式（doc_windows_cli）是否纳入？对「上手」非必需，可留进阶参考。
- 是否需要「持久化(persistence)」小节？属进阶，建议仅作一句引导不展开。
- Obsidian 输出目录与 MOC 仍未定 → 阶段 6 确认。

## 给下游的交接（→ 大纲生成）

候选章节结构（供 outline-generator 使用）：
1. Ventoy 是什么：原理、双分区、适用场景、与 Rufus/balenaEtcher 对比
2. 准备工作：下载、版本、校验、U 盘选择与备份
3. Windows 安装与制作（GUI + 可选 CLI）
4. Linux 安装与制作（GUI/WebUI + CLI 参数表）
5. 日常使用与升级：增删镜像、当普通 U 盘用、搜索控制与 `.ventoyignore`
6. 常见问题与排错：Secure Boot 注册、Legacy 限制、占用进程、VTOYEFI 恢复、启动卡顿
7.（可选）进阶速览：Secure Boot 策略、持久化、插件与 ventoy.json

素材文件：`00_intent.md`、`01_explore_result.md`、`cache/*.md`（S1-S4 全文）。
