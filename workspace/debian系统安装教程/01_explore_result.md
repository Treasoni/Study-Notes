# Debian 系统安装教程 - 探测式收集结果

收集时间: 2026-07-29

## 探测方向

| # | 方向 | 搜索关键词 | 发现条数 |
|---|------|-----------|---------|
| 1 | 官方安装指南 | Debian 12 Bookworm installation guide | 5 条 |
| 2 | 服务器安全加固 | Debian 12 server security post-installation | 5 条 |
| 3 | 桌面与中文配置 | Debian 12 桌面安装 中文配置 输入法 | 5 条 |
| 4 | Debian vs Ubuntu 差异 | Debian vs Ubuntu differences | 5 条 |
| 5 | 排错与常见问题 | Debian 安装 GRUB 修复 网络 排错 | 5 条 |

## 汇总结果

### 方向 1：官方安装指南
- Debian 12 Bookworm 官方安装信息入口（debian.org），支持 9 种架构
- amd64 完整安装手册（~580 页 HTML 文档）
- 简体中文版安装手册文本
- Debian-Installer 项目文档
- CD/DVD 镜像 FAQ（netinst ~600MB, DVD-1 ~4.7GB）

### 方向 2：服务器安全加固
- du_setup 自动化加固脚本（GitHub，覆盖 12+ 项任务）
- zero-trust-init 零信任初始化脚本（支持 --rollback 回滚）
- ComputingForGeeks Post-Install 指南（10+ 配置步骤）
- 中文 Debian 12 服务器初始化全流程
- CIS 合规加固脚本（100+ 安全检查项）

### 方向 3：桌面与中文配置
- Fcitx5 / IBus / 搜狗输入法三种方案对比
- GNOME、KDE Plasma、Xfce 各桌面配置差异
- locale 配置与中文字体安装（fonts-noto-cjk, fonts-wqy）
- Wayland 下浏览器中文输入兼容性问题

### 方向 4：Debian vs Ubuntu 差异
- Ubuntu 基于 Debian Testing，共享 apt/dpkg + systemd
- Ubuntu 软件更新（Kernel 7.0 vs 6.12 LTS）
- Ubuntu 预装 Snap/PPA；Debian 仅用 APT
- Ubuntu 商业支持（Canonical）；Debian 社区驱动
- Debian 资源占用更低（512MB RAM 可运行）

### 方向 5：排错与常见问题
- GRUB 安装失败 90% 因磁盘设备名漂移
- Debian 安装 ISO Rescue Mode 引导修复全流程
- 网卡固件缺失：dmesg | grep firmware 定位，安装对应包
- 中文 locale 配置：dpkg-reconfigure locales 选 zh_CN.UTF-8
- 双系统时间：timedatectl set-local-rtc 1

## 高质量精读候选

| # | 资料 | 评分 | 精读建议 |
|---|------|------|----------|
| 1 | Debian 官方安装手册 (amd64) | 5/5 | 官方权威，必读 |
| 2 | Debian Handbook - Network Config | 5/5 | 官方网络配置指南 |
| 3 | ComputingForGeeks Post-Install | 5/5 | 安装后配置标准参考 |
| 4 | Debian Network FAQ (Wiki) | 5/5 | 网络排错权威参考 |
| 5 | Fcitx5 中文输入法配置 | 5/5 | 桌面用户必备 |
