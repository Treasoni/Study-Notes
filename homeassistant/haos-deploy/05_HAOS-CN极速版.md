---
title: "第五章：HAOS-CN 极速版——一键国内化替代方案"
tags:
  - 智能家居/HomeAssistant
  - HAOS/部署教程
  - 学习笔记
created: 2026-08-06
updated: 2026-08-06
status: 已完成
source_project: haos-deploy-tutorial
chapter: 5
---

# 第五章：HAOS-CN 极速版——一键国内化替代方案

> [!summary] 本章讲什么
> 前四章走的是「官方原版 + 手动配置国内源」路线：每一项源都可解释、可掌控，但都要自己动手。本章介绍替代路线 **HAOS-CN 极速版**（官方英文名「Home Assistant OS Turbo」）——一个面向国内网络环境改造再分发的社区开源版本。读完你会搞清楚三件事：它凭什么能「装完即用」（内置加速机制）、怎么下载和互转（OTA 脚本 + A/B 分区）、以及接受它要付出什么代价（风险清单）。选型边界：本章不重复 [[Home Assistant 三种部署方式对比与选型]] 里的 HAOS / Docker / Supervised 对比，只回答「要不要用这个替代发行版」。

## 5.1 项目概述与信任模型

[[05_HAOS-CN极速版|HAOS-CN]] 是 GitHub 社区项目 `ha-china/HAOS-CN`，把官方 [[01_绪论|HAOS]] 重新构建成「更适合中国网络环境」的版本。先区分两组容易混淆的名字：

| 项目 | 开源 | 说明 |
| ---- | ---- | ---- |
| HAOS-CN 极速版 | 开源 | ha-china 社区维护，GitHub 仓库公开，官方英文名 Home Assistant OS Turbo |
| 冬瓜 HAOS | 闭源 | 瀚思彼岸（Hassbian）社区的定制版，源码与构建脚本不公开 |

极速版的核心改动有两处：**官方加载项源替换为国内加速源**，以及**集成 HACS 极速版**——装上就有 HACS，不需要 GitHub 账号，也不需要科学上网。（官方原版用户想单独装 HACS + 国内源的，见 [[09_HACS安装与国内源|第九章]]。）

更新走**自建 OTA**（`ota.hasscn.top`，由深圳酷宅 CoolKit 赞助，仅限中国 IP 访问）。构建节奏固定：每月 27 日构建新版本、28 日自动检查更新；项目声明不商业化、公司可免费使用。本文采集时主版本为 **18.2**，具体以官网为准。

有意思的是，即便在「手动配置国内源」的社区方法论里，HAOS-CN 也被排在推荐序列首位（国内定制版 > Supervisor `registries_mirror` > udev bind-mount > 手拉镜像改名）。也就是说，第四章那套手动配置不是要你「拒绝极速版」，而是提供一条官方原版路线下可解释、可掌控的加速方案——两条路线是**互补**关系，不是互斥关系。

> [!warning] 信任模型要自己掂量
> 虽然项目仓库公开，但**端点配置是构建时经私有脚本注入的，公开仓库里看不到完整生成过程**。最终刷进设备的镜像到底改了什么，只能信任项目方。这与官方原版（代码全量公开、镜像可复现）的信任模型有本质差别。

## 5.2 下载、格式选择与校验缺口

下载站提供与官方一致的格式矩阵：`img.xz`、`qcow2.xz`、`vdi.zip`、`vmdk.zip`、`ova`、`vhdx.zip`，覆盖 generic x86-64 / generic aarch64 / HA Green / HA Yellow / Sonoff iHost / OrangePi CM4 / Panther X2 / Raspberry Pi 3/4/5 / Hyper-V 等平台。

下载时先分清两种包：

| 类型 | 行为 | 适用 |
| ---- | ---- | ---- |
| 在线式 | 与官方一致，装完需联网拉依赖 | 网络可用、能等首次初始化 |
| 完整包（`-full`） | 装完即用、免初始化等待 | 网络差、想开箱即用 |

> [!warning] 一个已知缺口
> x86-64 的 `qcow2` / `vdi` / `vmdk` **在线式列表缺失**，只有 `-full` 完整包；而完整包目前标记为**公测**，存在「装完进不了系统」的风险。下载前务必核对官网当前的格式列表。

下载链路也有讲究：优先用 **gh-proxy.org 原始加速链接**；酷宅下载点禁止手机访问且有 WAF 限流。格式选对、平台对号入座后，底层刷写/导入动作与官方版完全一致，第二章的方法全部复用。

> [!example] 通过 gh-proxy.org 加速下载
> ```bash
> # 示例，实际完整链接以官网 https://www.hasscn.top/download.html 为准
> wget -c https://gh-proxy.org/<完整下载路径>/haos_generic-x86-64-18.2.img.xz
> 
> # 校验：系统镜像未公布 SHA256，只能对照官方 checksum 手工核对
> # sha256sum haos_generic-x86-64-18.2.img.xz
> ```

> [!warning] 校验和缺口
> 目前**只有刷机程序 `green_factory_CN` 公布了 SHA256**，各系统镜像没有列校验和。你无法像官方版那样先验哈希再刷写——这是完整包风险被放大的另一个原因。

## 5.3 内置加速机制解析

极速版把第四章手动做的那些事全部**内置**了，而且更彻底，共 **8 类网络重定向**：

| 重定向对象 | 目标 | 说明 |
| ---- | ---- | ---- |
| 版本检查 | version.hasscn.top | 绕过 GitHub 慢速/被墙 |
| 连通性检查 | 腾讯 BGP | HTTP 204 |
| NTP 时间 | 阿里 / 腾讯国内源 | 时间同步国内化 |
| 容器镜像 `ghcr.io/home-assistant/*` | ota.hasscn.top | Registry API V2 + CDN |
| OTA 更新 | 腾讯 BGP | 保留 RAUC 签名 + A/B 原子更新 |
| 错误上报 | 腾讯 BGP | — |
| Docker 镜像 | 12 源故障转移 | 见下 |

Docker 镜像层内置 **12 个国内源故障转移链**（优先级从高到低）：

```text
docker.1panel.live → docker.1ms.run → dytt.online → docker-0.unsee.tech
→ lispy.org → docker.xiaogenban1993.com → 666860.xyz → hub.rat.dev
→ docker.m.daocloud.io → demo.52013120.xyz → proxy.vvvv.ee → registry.cyou
→ 全部失败回退 docker.io
```

首个源挂掉约 5–10 秒自动切下一个，正好应对公益镜像「隔天失效」的通病。

实现方式决定了它的双刃剑属性：**构建时硬编码（只读 EROFS）+ 运行时 rootfs-overlay（Docker/NTP 配置）**。好处是配置项不可被误改；坏处是**安装后不可修改、没有关闭开关**——你选了它，就得接受内置的全部重定向。数据目录独立放在 `data-root: /mnt/data/docker`（独立分区），A/B 更新切换系统槽位后镜像仍然保留。

提速数据（来自项目方，建议实测验证）：镜像下载提速 5–10 倍，1Gbps 网络下 Core + Add-on 约 1–1.5 分钟；500MB Core 无镜像 30–120 秒 → 有镜像 5–30 秒；版本检查 20–50ms vs 国际 200–500ms。

## 5.4 安装差异、官方互转与 A/B 分区

**安装差异极小**：底层刷写/导入流程与官方版基本相同（`img.xz` 刷盘、`qcow2` 导入 PVE、`vmdk` 导入 VMware/群晖），唯一差异在首次启动——完整包免初始化等待，在线式仍需联网拉依赖。

**官方版 → 极速版**是最常用的路径，一键 OTA、保留现有配置。前提是先做一次完整备份，且必须用系统终端（不是网页版 Terminal）：

> [!example] 官方版一键转极速版
> ```bash
> login
> curl -fsSL https://ota.hasscn.top/upgrade.sh | bash
> ```

脚本执行后自动重启。重启后分两步验证：

> [!example] OTA 后验证
> ```bash
> # 1) 启动日志确认已切换：出现 "OTA service kindly sponsored by Coolkit" 即为极速版
> # 2) 先看诊断页全绿，再进 Web UI
> curl http://homeassistant.local:4357/    # 4357 = HassOS Observer 诊断状态
> ```

**极速版 → 官方没有 OTA 脚本**：官方只推荐「备份 → 重装官方镜像 → 还原备份」。方向是单向便利——跳进去容易，跳回来要整机重装。

如果 OTA 后系统异常，用 A/B 分区排查——极速版保留了官方 RAUC 的 **A/B 双槽位原子更新**，坏槽可回滚：

> [!example] A/B 槽位排查
> ```bash
> ha os info          # 查看当前 boot: 槽位
> ha os boot-slot A   # 或 ha os boot-slot B，切换到另一槽
> ha host reboot      # 重启生效
> ```

## 5.5 风险清单与使用边界

把接受极速版要付的账一次算清（采集时间 2026-08-06，均以实际官方站为准）：

> [!warning] 风险清单
> 1. **非官方发行版**：端点配置经私有构建脚本注入，公开仓库不可见完整生成过程，信任模型依赖项目方。
> 2. **校验和缺口**：系统镜像未列 SHA256，无法自行验证镜像完整性。
> 3. **版本标注不一致**：ihost、rpi5 两处已确认标注与镜像不符。
> 4. **完整包为公测**：存在「装完进不了系统」风险，生产环境慎用。
> 5. **硬依赖中国大陆网络**：酷宅 OTA 仅限中国 IP，海外节点可能无法更新。
> 6. **第三方源合规风险**：12 个 Docker 镜像源均非官方，有失效与合规不确定性；系统内只能同时存在一个加速方案。

> [!tip] 使用边界建议
> 极速版适合**国内网络环境下的个人折腾、快速起服务**；生产环境先自行评估，务必保留官方镜像与 SHA256 作为备路——哪天公益源失效或信任模型出问题，还能备份重装回到官方原版。

## 本章 Checklist

- [ ] 我能区分 HAOS-CN（开源）与冬瓜 HAOS（闭源）的信任模型差异
- [ ] 我能分清在线式与 `-full` 完整包，并避开公测包进不了系统的坑
- [ ] 我知道极速版 8 类网络重定向与 12 源故障转移的实现方式（只读硬编码 + rootfs-overlay）
- [ ] 我能用 `curl -fsSL https://ota.hasscn.top/upgrade.sh | bash` 从官方版一键转极速版，并用 4357 状态页验证
- [ ] 我知道反向（极速→官方）必须备份重装，且能用 `ha os boot-slot` 排查 A/B 槽
- [ ] 我已确认接受：不可修改、无关闭开关、校验缺口、中国 IP 依赖、第三方源风险，并保留官方备路

---

> ⬅️ 上一章：[[04_手动配置国内源|第四章：HAOS 国内换源（Docker / Supervisor / OTA 三层全解）]] ｜ 📖 [[部署 HAOS 详细教程|返回索引]] ｜ 下一章：[[06_双路线对比与选型建议|第六章：双路线对比与选型建议]] ➡️
