# 为什么是 Docker 版 —— 部署架构与能力边界

在动手之前，先回答一个最关键的问题：**同样是 Home Assistant，为什么选 Docker Container 版？** 很多读者是从 HAOS 入门的，习惯了界面里点一点就装好的 Add-on 商店，换到 Docker 版后会猛然发现「怎么啥都没有」。本章帮你认清 Docker 版在三种部署方式中的定位与能力边界，建立「缺什么、补什么」的全局观——这是后面 8 章所有操作的前提。

## 三种部署方式：先看清地图再上路

Home Assistant 官方截至 2026 年只正式支持两种安装方式：**HAOS**（推荐大多数用户）与 **HA Container**（已有 Docker 环境的熟练用户）；Supervised 方式已弃用[^official-install]。三者对比如下：

| 对比维度 | HAOS | Supervised | HA Container |
|---------|------|-----------|--------------|
| 本质 | 专用操作系统，含 HA 内核 | 在 Debian 系 Linux 上装 Supervisor + HA | 只跑 HA 核心的 Docker 容器 |
| Add-on Store | ✅ 自带 | ✅ 有 | ❌ 无 |
| ha CLI | ✅ | ✅ | ❌ |
| 内置备份 | ✅ | ✅ | ❌ |
| 更新/回滚 | 界面操作 | 界面操作 | Docker 侧自管 |
| 官方支持状态 | ✅ 官方推荐 | ⚠️ 2025 起弃用 | ✅ 官方支持 |
| 适合人群 | 多数用户、专用硬件 | 不建议新装 | 已有 Docker 环境的熟练用户 |

官方推荐逻辑很直白：**能装 HAOS 就装 HAOS**，它把全家桶都替你管好；只有当你已经有一个跑着 Docker 的服务器、不想为 HA 单独占一台机器时，才走 Container 路线[^official-install]。本教程就是这条「已有 Docker 环境」的路。

> [!tip] 大白话
> 把 Supervisor 想成 **容器「管家」**：它负责自动安装、卸载、管理一个个 addon 容器，还顺手提供 ha CLI 和内置备份。HAOS 和 Supervised 自带管家；Docker Container 版没有管家——**你自己当管家**。

## Supervised 已弃用（2025），新装别选它

Supervised 曾经是「既有 Linux 又想用 Add-on Store」的折中方案，但官方 2025 年起将其弃用。它的硬伤在于要求对宿主机的完全控制：你一旦在宿主机上跑 Portainer、Watchtower 这类常用运维工具，HA 就会把系统标记为 **Unsupported/Unhealthy**，官方也不再兜底[^research-a1]。所以新部署不要选这条路——要么 HAOS，要么 Docker Container。

## Container 版能力边界：缺什么，补什么

Docker Container 版的本质是**无 Supervisor 的单容器**，能力边界可以一句话概括[^research-synthesis]：

- **无 Add-on Store**：官方 addon 设计为专与 Supervisor 配合，Container 版没有「应用商店」；
- **无 ha CLI**：`hassio-cli` / `ha` 这类走 Supervisor API 的命令全部不可用；
- **无内置备份**：没有一键备份/恢复按钮，备份要自己 `tar`。

但「缺失」不等于「做不到」。addon 本质就是容器镜像，官方文档原文明确说「addon 底层就是发布到容器仓库的应用镜像」[^official-addon]，所以 **整个 Docker Hub 就是你的 Add-on Store**——只是从「商店自动安装」变成「自己 `docker compose up`」；备份也有标准命令序列。这正是本教程第 7、8、9 章要补的课。

> [!tip] 大白话
> addon = 一个**预装好软件的容器**。HAOS 的「Add-on Store」就是管家替你把容器拉下来、配置好、再启动；Docker 版没了这个商店，你手动 `docker compose up` 就是「手动安装 App」。HACS 装的是集成和前端卡片，不是容器，两者不冲突、也不能互相替代。

## 全文主线：一份 compose 贯穿始终

认清定位后，本教程的路线已经清晰，后续 8 章围绕「缺什么、补什么」展开，并始终围绕**一份可直接上线的 docker-compose.yml** 这条主线：

1. **部署**（第 2–3 章）：先用 `docker run` 快速起跑，再升级为工程化 compose；
2. **HACS**（第 4–5 章）：Docker 三种安装路径 + 国内加速 + 首次授权；
3. **稳定运维**（第 6–7 章）：锁版本、镜像加速、更新、回滚、备份三件套；
4. **addon 补足**（第 8–9 章）：把 Docker Hub 当 Add-on Store，打通通信与权限。

## 本章小结

- 官方只正式支持 HAOS 与 HA Container 两种方式；Supervised 已弃用（2025），新装不要选。
- Container 版的能力边界 = 无 Supervisor：无 Add-on Store、无 ha CLI、无内置备份，全部自管。
- 「缺失」不等于「做不到」：addon 本质是容器镜像，整个 Docker Hub 就是你的 Add-on Store。
- Docker 版没有「管家」，你得自己负责更新、备份、伴生服务——这正是本教程的实战主线。
- 记住这份地图：**部署 → HACS → 稳定运维 → addon**，接下来每一步都会回到这条主线上。

## 下一章预告

地图看完了，下一章立刻动手：用官方 `docker run` 命令在几分钟内拉起你的第一个 HA 容器，搞懂 `/config` 目录和首次启动机制，为升级成 compose 打底。

[^official-install]: [Home Assistant Installation](https://www.home-assistant.io/installation/)
[^official-addon]: [Home Assistant Developer Docs: Add-ons](https://developers.home-assistant.io/docs/add-ons/)
[^research-a1]: 深度素材方向 A1「官方推荐部署方式（截至 2026）」：Supervised 弃用、跑 Portainer/Watchtower 会被标 Unsupported/Unhealthy。
[^research-synthesis]: 深度素材综合分析「关键共识」：Docker Container 版 = 无 Supervisor 的单容器，无 Add-on Store、ha CLI、内置备份，伴生服务用独立容器自管。
