# 飞牛上安装配置 iStoreOS（软路由）- 探测结果

> 主题：在飞牛 NAS 上通过虚拟机安装 iStoreOS 作为软路由
> 阶段：P1 探测式收集
> 创建时间：2026-09-01
> 笔记类型：实战教程 ｜ 深度：上手

## 探测透镜

| 透镜 | 关注点 |
|------|--------|
| L1 飞牛 fnOS 虚拟化 | 创建虚拟机、资源分配、导入磁盘镜像（img/qcow2/iso）、网卡直通前提 |
| L2 iStoreOS 安装引导 | 固件选择（x86_64）、写盘/引导、虚拟机导入、首次启动与后台访问 |
| L3 软路由网络配置 | LAN/WAN、旁路由模式、与主路由及 NAS 互通、常见排错 |

## 候选来源（按透镜，已去重）

### L1 飞牛 fnOS 虚拟化

| # | 标题 | 发布方 | 层级 | 日期 | 相关性 | 分 |
|---|------|--------|------|------|--------|-----|
| 1 | [如何安装和使用虚拟机？](https://help.fnnas.com/articles/v1/virtual-machine/install) | 飞牛官方帮助中心 | tier1 | 持续更新 | 官方教程：安装虚拟机应用、启用 OVS 虚拟网络、BIOS 开 VT-x/AMD-V、新建 VM 配置 CPU/内存/ISO、VirtIO 驱动 | 5 |
| 2 | [虚拟机（专题，含硬件直通）](https://help.fnnas.com/articles/v1/virtual-machine) | 飞牛官方帮助中心 | tier1 | 持续更新 | 官方虚拟机专题，涵盖第三方平台安装 fnOS、虚拟机使用与硬件直通（IOMMU 前提） | 4 |
| 3 | [fnOS 虚拟机 v0.9.0 支持导入 img/qcow2](https://www.ithome.com/0/855/243.htm) | IT之家 | tier2 | 2025-05 | 时间节点：v0.9.0 起原生支持 img、img.gz、qcow2 与 OVA 导入导出 | 4 |
| 4 | [fnOS 虚拟 iStoreOS 软路由](https://mynas.chat/fnos/istoreos) | 个人站 | tier3 | 2025-01-25 | 双网口主/旁路由方案、qemu-img convert 转 qcow2、硬件直通与 IOMMU 步骤 | 3 |

### L2 iStoreOS 安装引导

| # | 标题 | 发布方 | 层级 | 日期 | 相关性 | 分 |
|---|------|--------|------|------|--------|-----|
| 5 | [iStoreOS 官方 x86 安装文档](https://doc.istoreos.com/zh/guide/istoreos/install_x86.html) | iStoreOS 官方文档 | tier1 | — | 固件选择、Rufus/Ventoy 写盘、U 盘引导、quickstart 安装及首次启动访问 | 5 |
| 6 | [iStoreOS 官方固件下载目录（x86_64）](https://fw.koolcenter.com/iStoreOS/x86_64/) | iStoreOS / KoolCenter | tier1 | — | Legacy 与 UEFI 的 squashfs-combined img.gz 镜像，导入虚拟机的固件来源 | 5 |
| 7 | [万物皆可 iStoreOS](https://site.istoreos.com/about) | iStoreOS 官网 | tier1 | — | 基于 OpenWrt 的路由兼轻 NAS 系统、三套 UI、软件中心与沙箱机制 | 4 |
| 8 | [飞牛虚拟机部署 iStoreOS 做旁路由教程](https://club.fnnas.com/forum.php?mod=viewthread&tid=26481) | 飞牛官方论坛 | tier2* | 约 2025 | 跨 L1/L2 综合帖：新建 VM、导入 img、磁盘分配、网络设置到初始化全流程 | 4 |
| 9 | [飞牛 fnos 安装 iStoreOS 软路由踩坑](https://blog.csdn.net/u013262414/article/details/155347617) | CSDN 博客 | tier3 | — | 踩坑：默认 IP 无法访问、VNC 黑屏、磁盘扩容、Docker 目录迁移 | 3 |

### L3 软路由网络配置

| # | 标题 | 发布方 | 层级 | 日期 | 相关性 | 分 |
|---|------|--------|------|------|--------|-----|
| 10 | [如何更好地使用旁路由](https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html) | iStoreOS 官方文档 | tier1 | 持续更新 | 手动静态 IP、DHCP 接管、浮动网关三方案；关 DHCP、网关/DNS 指向、MASQUERADE | 5 |
| 11 | [Merlin 跟 iStoreOS 网络问题排查](https://doc.istoreos.com/zh/guide/istoreos/question/about_network.html) | iStoreOS 官方文档 | tier1 | 持续更新 | 单 LAN 口旁路由向导、固定 IP 失联、接口网关勾选、防火墙入站等排错 | 4 |
| 12 | [旁路由·手动静态 IP 方案](https://www.koolcenter.com/t/topic/797) | 酷友社社区 | tier2 | — | LAN 口静态 IP 同网段、网关/DNS 指向主路由、必须关 DHCP 的基线 | 4 |
| 13 | [旁路由防火墙设置](https://www.koolcenter.com/t/topic/2681) | 酷友社社区 | tier2 | — | iptables MASQUERADE、LAN 区域 IP 动态伪装、避免双 DHCP 冲突 | 4 |
| 14 | [折腾 qwrt 旁路由经验（NAS/容器互通）](https://club.fnnas.com/forum.php?mod=viewthread&tid=59080) | 飞牛私有云论坛 | tier3 | — | 飞牛 NAS 场景：旁路由配置验证、NAS/容器互通、网关自动切换 | 4 |

\* 飞牛官方论坛帖，介于 tier2/3 之间，按社区实操标注 tier2 偏高，P2 复核时再定。

## 方向菜单（请选择主学习路径）

- **A. 完整主线：飞牛建 VM → 导入 iStoreOS → 配成旁路由**
  覆盖 L1+L2+L3 全链路，从零到可用的综合实战教程。
- **B. 侧重飞牛虚拟化与硬件直通**
  深挖 L1：虚拟机创建、资源分配建议、网卡直通/IOMMU、磁盘与镜像转换。
- **C. 侧重 iStoreOS 网络配置与排错**
  深挖 L3：旁路由三方案、防火墙、双 DHCP、NAS 互通与失联排查。

## 覆盖缺口

1. 飞牛官方帮助中心与 doc.istoreos.com 等域名在当前网络环境无法直接抓取验证，P2 写作时需人工复核版本号与默认密码（password/123456/空 跨版本差异）。
2. fnOS 底层是否 Debian、虚拟化基于 KVM/QEMU 缺少官方单点说明，多为社区间接印证。
3. 官方资源分配建议值（CPU/内存/磁盘最小配置）缺失，多为社区经验（磁盘常建议 20GB+）。
4. 网卡硬件直通场景（主路由形态）权威资料偏少，现有资料多以旁路由为样本。

## P2 深度收集范围预估

- 核心来源：L1-1/L1-2（飞牛官方）、L2-5/L2-6/L2-7（iStoreOS 官方）、L3-10/L3-11（iStoreOS 官方）
- 按方向菜单选择结果，补充 3–5 篇核心来源精读 + 按缺口补齐社区实操帖
- 产出 `02_deep_research.md`：范围、来源表、观点/来源映射、矛盾点、实操指引、开放问题、下游交接
