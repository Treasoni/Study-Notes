## 学习笔记大纲：《Debian 系统安装教程》

> **笔记类型**：实战笔记（面向有 Ubuntu 基础的用户，进阶级深度）
> **结构模式**：环境搭建 → 核心功能 → 进阶优化 → 运维管理
> **预计总篇幅**：中（约 8-10 页 A4）
> **章节数**：8 章

### 第一章：Debian 概述与版本选择
- **篇幅**：短
- **覆盖要点**：Debian 简介、稳定版/Testing/Sid 分支选择与适用场景、Debian 12 Bookworm 新特性（non-free-firmware）、架构支持（amd64/arm64/i386）
- **Debian vs Ubuntu 对比**：Ubuntu 基于 Debian Testing 的关系定位、发布节奏差异（固定时间表 vs "准备好了才发布"）、支持周期对比（Ubuntu Pro 12年 vs Debian LTS 5年）
- **素材引用**：#1.1（官方手册概述）、#4（差异对比）
- **代码示例**：无

### 第二章：安装前的准备工作
- **篇幅**：中
- **覆盖要点**：下载镜像（netinst/DVD/live 对比及国内镜像源）、制作安装介质（dd/Rufus）、硬件要求、UEFI vs Legacy BIOS 区别、Secure Boot 注意事项
- **Debian vs Ubuntu 对比**：Debian 对非 free 固件默认不包含（需手动处理）、Ubuntu 安装镜像预装大量驱动开箱即用
- **素材引用**：#1.1（准备工作、获取介质章节）、#4（实践差异）
- **代码示例**：有（dd 写入命令）

### 第三章：安装步骤全流程（图形安装器）
- **篇幅**：长
- **覆盖要点**：启动安装 → 语言/区域设置 → 网络配置 → 主机名与用户 → 磁盘分区三种方案（全自动/LVM加密/手动） → 软件包选择 → GRUB 配置 → 完成安装
- **Debian vs Ubuntu 对比**：Debian 默认设置 root 密码（Ubuntu 用 sudo）、安装器提问更多更细、软件包选择界面差异（tasksel vs 分类勾选）、默认不预装 Snap
- **素材引用**：#1.1（第 5-6 章安装流程、附录 C 分区方案）、#4（安装器差异）
- **代码示例**：有（分区表参考、各步骤命令）

### 第四章：安装后基础配置
- **篇幅**：中
- **覆盖要点**：首次登录与系统检查、国内 APT 源配置（清华/阿里/中科大）、sudo 配置、系统更新、时区与时间同步（NTP）、防火墙基础配置（UFW）
- **Debian vs Ubuntu 对比**：non-free-firmware 源需手动添加（Ubuntu 预置）、Debian 的 APT 源不使用 PPA 机制、软件版本相对保守但更稳定
- **素材引用**：#1.2（网络配置）、#2.1（安全基线：UFW、系统更新）、#4（APT 源差异）
- **代码示例**：有（sources.list 配置、timedatectl、UFW 命令）

### 第五章：桌面环境与中文配置
- **篇幅**：长
- **覆盖要点**：GNOME/KDE Plasma/Xfce 安装与选择、locale 配置与中文语言包、中文字体安装（Noto CJK/文泉驿）、Fcitx5 vs IBus 输入法方案对比与配置、Wayland 下浏览器中文输入问题
- **Debian vs Ubuntu 对比**：Debian 桌面是上游原版 GNOME（无 Ubuntu 的定制主题/侧栏）、Firefox 使用 APT 版（非 Snap）、资源占用更低
- **素材引用**：#3（桌面与中文配置全章）、#4（桌面体验差异）
- **代码示例**：有（安装命令、环境变量、im-config）

### 第六章：服务器安全加固
- **篇幅**：中
- **覆盖要点**：创建 sudo 用户、SSH 密钥认证与配置文件加固（Debian 12 推荐 drop-in 方式）、Fail2ban 安装与配置（systemd backend）、自动安全更新（unattended-upgrades）、内核参数调优、进阶措施（AppArmor/Lynis）
- **Debian vs Ubuntu 对比**：Debian 无 Livepatch（Ubuntu Pro 可热修补内核）、CIS 合规依赖第三方（Ubuntu Pro 内置）、资源开销更低适合小规格 VPS
- **素材引用**：#2.1（安全基线所有条目）、#4（安全对比）
- **代码示例**：有（sshd_config.d、fail2ban 配置、sysctl）

### 第七章：软件包管理与版本升级
- **篇幅**：中
- **覆盖要点**：APT 常用命令详解、dpkg 基础、Backports 源使用、从 Bullseye 升级到 Bookworm 完整流程、升级注意事项与回滚策略
- **Debian vs Ubuntu 对比**：Debian 无 Snap/PPA（但有 Flatpak 可选）、软件版本更新频率策略、Backports 机制类似 Ubuntu 的 HWE
- **素材引用**：#1.1（第 8 章包管理）、#5.6（多内核默认启动）、#4（包管理差异）
- **代码示例**：有（APT 命令、升级 sed 替换、GRUB 默认配置）

### 第八章：常见问题与排错
- **篇幅**：长
- **覆盖要点**：GRUB 安装失败（磁盘漂移）、GRUB 引导损坏修复（Rescue Mode chroot）、网卡固件缺失排查、中文乱码与 locale 修复、双系统时间不一致、安装器找不到 U 盘
- **Debian vs Ubuntu 对比**：Ubuntu 用户换 Debian 最常遇到的坑（固件缺失、root 密码、locale 未配置）、提示排查优先级差异
- **素材引用**：#5（排错全章）
- **代码示例**：有（dmesg、chroot 修复、locale 配置、timedatectl）

---

## 学习路径说明

### 前置要求
- 了解 Linux 基本概念（终端、文件系统、用户权限）
- 有 Ubuntu 或其他发行版的使用经验（便于对比理解差异）
- 一台可用的电脑或虚拟机用于安装练习
- 一个 4GB+ U 盘（如需实体机安装）

### 学完能做什么
- 独立完成 Debian 系统的安装与初始配置
- 根据场景选择合适的桌面环境或服务器配置
- 对新安装的 Debian 系统进行安全加固
- 解决常见的安装和配置问题（GRUB、网络、中文、时间）
- 理解 Debian 与 Ubuntu 的差异，能在两者间灵活切换
- 在 Debian 稳定版之间进行版本升级

### 建议学习顺序
1. 第 1-3 章为核心流程，建议按顺序依次阅读
2. 第 4 章（基础配置）是装完系统后的必做步骤，紧接第 3 章
3. 第 5 章（桌面）和第 6 章（服务器）按实际场景选择其中一条路径
4. 第 7 章（包管理与升级）和 第 8 章（排错）作为参考手册，遇到对应场景时查阅
5. 每章末的"Debian vs Ubuntu 对比"段落，有 Ubuntu 基础的用户重点关注
