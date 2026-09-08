# Ventoy 使用实战 — 阶段 1 探测结果

> 运行：`ventoy-usage`（learning-note-flow）｜主题：如何使用 Ventoy（多系统启动U盘）
> 检索日期：2026-09-08
> 用途：给出方向菜单，等待用户选择后进入 P2 深度收集

## 方向菜单

### 方向 A：核心概念与定位
Ventoy 是什么、双分区原理、与 Rufus/balenaEtcher 烧录工具的差异。

| # | 候选 | 来源层级 | 日期 | 相关度 | 评分 |
|---|------|---------|------|--------|------|
| A1 | [Ventoy 官方 README](https://github.com/ventoy/Ventoy/blob/master/README.md) | official | 持续更新 | 官方一手定位：免重复格式化、直接拷贝 ISO/WIM/IMG/VHD(x)/EFI、开机菜单直启；1300+ 镜像兼容清单 | 5 |
| A2 | [官方磁盘布局（中文）](https://ventoy.net/cn/doc_disk_layout.html) | official | unknown | 双分区结构权威说明：exFAT 数据盘 + ~32MB VTOYEFI 引导区、MBR/GPT 规则 | 5 |
| A3 | [官方安装与使用 doc_start](https://www.ventoy.net/cn/doc_start.html)（中英重复，取中文） | official | unknown | 装一次 → 两分区 → 镜像拷入第一分区任意目录，递归搜索列菜单 | 4 |
| A4 | [Arch Wiki：Ventoy](https://wiki.archlinux.org/title/Ventoy) | report | unknown | 交叉印证双分区成因、固定布局、按扇区升级原理（另有[中文镜像](https://wiki.archlinux.org.cn/title/Ventoy)） | 4 |
| A5 | [notebookcheck：Ventoy vs Rufus/BalenaEtcher 测评](https://www.notebookcheck.net/Rufus-BalenaEtcher-My-current-USB-boot-tool-beats-them-all.1182591.0.html) | report | unknown | 媒体一手测评：烧写单 ISO vs 装一次引导器后只复制镜像 | 3 |

**覆盖缺口**：官方无“Ventoy vs Rufus”直接对比页；双分区成因散见 Arch Wiki/论坛；中文社区实操兼容性坑待补充。

### 方向 B：安装与制作（实战主线）
Windows / Linux 安装 Ventoy 到 U 盘，日常增删镜像。

| # | 候选 | 来源层级 | 日期 | 相关度 | 评分 |
|---|------|---------|------|--------|------|
| B1 | [官方使用说明（中文 doc_start）](https://www.ventoy.net/cn/doc_start.html) | official | unknown | Ventoy2Disk.exe / VentoyGUI / VentoyWeb / Ventoy2Disk.sh 各平台装法，首次安装格式化提醒 | 5 |
| B2 | [Release Ventoy 1.1.17](https://github.com/ventoy/Ventoy/releases/tag/v1.1.17) | official | 2026-07-24 | 当前最新稳定版下载与更新日志锚点，教程据此定版本与校验 | 4 |
| B3 | [Thomas-Krenn：Multi-ISO U 盘实操](https://www.thomas-krenn.com/en/wiki/Creation_of_bootable_Multi-ISO_USB_stick_with_Ventoy) | report | unknown | 运维 wiki：Windows GUI + Linux 命令行安装、双分区确认、多 ISO 拷贝与启动验证 | 4 |
| B4 | [Arch Wiki：Ventoy](https://wiki.archlinux.org/title/Ventoy) | report | unknown | Ventoy2Disk.sh 的 -i/-I/-u/-g/-s 参数语义与 -u 升级验证 | 4 |
| B5 | [博客园：制作启动U盘的工具——Ventoy](https://www.cnblogs.com/mq0036/p/17746092.html) | community | unknown | 中文图文实操（Windows 为主），社区经验佐证官方步骤 | 3 |

**覆盖缺口**：“如何确认安装成功/查看已装版本”官方无集中步骤；Linux GUI 细节分散；Secure Boot 新 CA 影响未纳入本视角。

### 方向 C：兼容性、安全启动与排错/进阶
Secure Boot、UEFI/Legacy、启动失败修复、持久化与插件。

| # | 候选 | 来源层级 | 日期 | 相关度 | 评分 |
|---|------|---------|------|--------|------|
| C1 | [官方 Secure Boot 文档](https://www.ventoy.net/en/doc_secure.html) | official | unknown | Secure Boot 支持版本、默认开启、shim/MOK 密钥注册及两类失败绕过方案 | 5 |
| C2 | [官方 FAQ](https://www.ventoy.net/en/faq.html) | official | unknown | 综合排错：识别 BIOS/UEFI、Secure Boot 0x1A、老机 Legacy ~128GB 限制、VTOYEFI 损坏恢复 | 5 |
| C3 | [官方持久化插件文档](https://www.ventoy.net/en/plugin_persistence.html) | official | unknown | Live Linux 持久化：ventoy.json + .dat 数据文件、CreatePersistentImg.sh | 4 |
| C4 | [官方 VentoyPlugson 文档](https://www.ventoy.net/en/plugin_plugson.html) | official | unknown | 免手写生成/校验 ventoy.json，插件生态统一配置入口 | 4 |
| C5 | [Ventoy 1.1.14 修复 UEFI CA 2023 Secure Boot 撤销](https://www.linuxcompatible.org/story/ventoy-1114-released-fixes-uefi-ca-2023-secure-boot-issues-and-adds-new-policy-controls/) | report | unknown | UEFI CA 2023 吊销证书导致旧版启动失败的实录与对策 | 3 |

**覆盖缺口**：plugin_theme 主题与手写 ventoy.json 总纲未深挖；社区一手排错案例少；部分页面对 1.1.17 版本需校准。

## 建议

- 本笔记定位 **实战操作指南 / 上手会用**，推荐 **综合全流程**：A（概念）→ B（安装制作主线）→ C（排错附录）。
- P2 深度收集按所选方向抓取 3–5 个核心源：A≈4 页、B≈3 页、C≈9 页（官方页为主）。
- 当前最新稳定版为 **Ventoy 1.1.17（2026-07-24）**。
