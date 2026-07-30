# 第一章：Debian 概述与版本选择

Debian 是历史最悠久、影响最深远的 Linux 发行版之一。它不仅是 Ubuntu、Kali Linux、Linux Mint 等众多发行版的基石，其本身也是一套极其稳定可靠的操作系统。本章帮助你理解 Debian 的定位、版本管理体系，以及如何根据自己的需求选择合适的版本。

## 1.1 什么是 Debian

Debian 项目始于 1993 年，由 Ian Murdock 发起，是**社区驱动**的 Linux 发行版。与 Ubuntu（由 Canonical 公司商业主导）不同，Debian 的决策遵循 **Debian 社会契约**（Debian Social Contract）和 **Debian 自由软件准则**（DFSG），社区投票决定项目走向。

> Debian vs Ubuntu：两者的关系可以概括为"父子关系"。Ubuntu 每 2 年从 Debian 的 Testing 或 Unstable 分支取一个快照作为起点，在此基础上定制桌面体验、预装软件和驱动。因此 Debian 是"上游"，Ubuntu 是"下游"。

### 相同点
由于同源，Debian 和 Ubuntu 共享大量底层特性：

- 包管理：均使用 **apt/dpkg** 和 `.deb` 包格式
- Init 系统：均使用 **systemd**，systemctl/journalctl 命令行为完全一致
- 安全框架：均默认启用 **AppArmor**

### 核心差异

| 维度 | Debian | Ubuntu |
|------|--------|--------|
| 维护方 | 社区志愿者 | Canonical 公司 |
| 发布节奏 | 约 2 年，"准备好了才发布" | 固定双年 LTS（4 月） |
| 免费支持 | ~5 年（3 年全量 + 2 年 LTS） | 5 年 |
| 最长支持 | ~5 年 | 12 年（Ubuntu Pro） |
| 包管理 | APT 仅 | APT + Snap（默认） |
| 第三方源 | 无 PPA | PPA 生态 |
| 服务器资源 | ~512MB RAM 可运行 | ~1GB RAM 起 |

## 1.2 版本分支体系

Debian 有三条主要分支，理解它们的差异是入门的第一步。

### Stable（稳定版）

- **代号**：当前为 **Bookworm**（Debian 12）
- **特点**：经过长期测试，软件包冻结后只接受安全修复和关键补丁
- **适合**：生产服务器、要求长期稳定的桌面、任何"设好就不用管"的场景
- **软件版本**：相对保守，但从不出其不意地坏掉

### Testing（测试版）

- **当前代号**：**Trixie**（Debian 13，下一个稳定版）
- **特点**：持续从 Unstable 流入经过一定测试的软件包，滚动更新
- **适合**：桌面用户、开发者，希望使用较新软件但不希望太激进
- **稳定性**：比 Stable 差但比 Unstable 好，偶有回归

### Unstable（不稳定版/Sid）

- **代号**：永远叫 **Sid**（取自《玩具总动员》中总搞破坏的小孩）
- **特点**：持续滚动，永远在接收上游最新软件
- **适合**：Debian 开发者和打包者、愿意频繁维护的高级用户
- **稳定性**：不承诺稳定，可能出现包依赖断裂

> [!tip] 选哪个？
> - 新手或生产环境 → **Stable（Bookworm）**
> - 桌面用户想用新软件 → **Testing（Trixie）**
> - 参与开发或打包 → **Unstable（Sid）**

## 1.3 Debian 12 Bookworm 新特性

Debian 12（2023 年 6 月发布）引入了几项重要变化，对安装和使用影响显著：

### non-free-firmware

**最大的变化**：之前 Debian 将非自由固件放在 `non-free` 仓库，默认不启用。Bookworm 起新增加 **`non-free-firmware`** 组件，专门存放固件类闭源驱动。

安装时若选择包含非自由固件的安装镜像（推荐），Wi-Fi 和某些有线网卡可以开箱即用；若使用纯自由软件镜像，仍需手动启用此源。

### 其他亮点

- 默认搭载 **Linux 6.1 LTS** 内核（长期支持）
- 官方支持 **RISC-V 64** 架构（实验性）
- Wayland 取代 X11 成为默认显示服务器（GNOME 桌面）
- 安装器改进：更好的 NVMe 磁盘支持
- 超过 **11,000 个新软件包**，总量超 60,000

## 1.4 架构支持

Debian 12 官方支持以下架构：

| 架构 | 说明 | 常见场景 |
|------|------|---------|
| **amd64** (x86_64) | 64 位 x86 架构 | 桌面 PC、服务器（最常用） |
| **arm64** (AArch64) | 64 位 ARM 架构 | 树莓派、ARM 服务器、Apple Silicon |
| **armhf** | 32 位 ARM hard-float | 嵌入式设备、旧款树莓派 |
| **i386** | 32 位 x86 | 老旧 PC（Debian 12 起不再包含在稳定版中，仅 Testing/Unstable 保留） |
| **ppc64el** | PowerPC 小端序 | IBM POWER 服务器 |
| **s390x** | IBM System z | 大型机 |
| **RISC-V 64** | 开放指令集架构 | 实验性，Debian 12 首发 |

> 对比 Ubuntu：Ubuntu 26.04 LTS 主要面向 amd64 和 arm64，Debian 的架构覆盖更广，尤其在非 x86 领域优势明显。

## 章节总结

- Debian 是社区驱动的 Linux 发行版，是 Ubuntu 的"上游"
- 三条分支各有定位：Stable 求稳、Testing 求新、Unstable 求变
- Debian 12 Bookworm 新增 `non-free-firmware` 组件，改善了硬件驱动体验
- Debian 支持的硬件架构远多于 Ubuntu

**下一章**：当你选定了版本，下一步是下载镜像、制作安装介质，并了解安装前的硬件和 BIOS 设置准备。
