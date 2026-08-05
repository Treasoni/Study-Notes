---
title: "Home Assistant 三种部署方式对比与选型"
tags:
  - 智能家居/HomeAssistant
  - 学习笔记
  - 部署方式
  - MOC
created: 2026-08-05
updated: 2026-08-05
status: 已完成
source_project: home-assistant-deployment-methods
---
# Home Assistant 三种部署方式对比与选型

> **主题**：Home Assistant 三种部署方式（HAOS 虚拟机 / Docker Container / HA Supervised）的区别与选型
> **笔记类型**：对比笔记 + 实战指南（侧重选型决策）
> **发布**：2026-08-05

## 核心结论

> [!summary] 一句话结论
> 官方只有两条正式路径：**HAOS（推荐，全托管）** 与 **Container（自托管 Core）**。Supervised 已于 2025.12 弃用。**默认选 HAOS**；已有 Docker 主机想与其他服务共存就选 Container。

> [!warning] 注意时效性
> Supervised 与 Core 安装方式官方支持已于 **2025.12 终止**（公告 2025-05-22）。网上「三选一」的旧教程已过时，本文以「官方两条路径 + 一条弃用旧路径」为框架。

## 目录

1. [[01_三种部署方式全景|第一章：三种部署方式全景]]
2. [[02_核心对比表|第二章：核心对比表]]
3. [[03_HAOS虚拟机详解|第三章：HAOS 虚拟机详解]]
4. [[04_DockerContainer详解|第四章：Docker Container 详解]]
5. [[05_HASupervised详解|第五章：HA Supervised 详解（含弃用现状）]]
6. [[06_选型决策树与建议|第六章：选型决策树与建议]]
7. [[07_迁移路径与操作|第七章：迁移路径与操作]]
8. [[08_部署实操附录|第八章（附录）：部署实操步骤]]

## 如何阅读

- **只看结论**：读「核心结论」+ 第六章（选型决策树）
- **完整对比**：第 1-2 章建立全景与对比框架，第 3-5 章按需精读
- **动手部署**：第八章（附录）有全套可复制命令
- **旧用户迁移**：第七章讲 Core/Supervised → HAOS/Container 的迁移路径

## 参考来源

- Home Assistant 官方安装指南：https://www.home-assistant.io/installation/
- Home Assistant 官方 Linux / VM 安装：https://www.home-assistant.io/installation/linux
- HAOS 官方镜像发布：https://github.com/home-assistant/operating-system/releases
- ADR-0014（Supervised 架构决策，已 revert）：https://github.com/home-assistant/architecture/blob/master/adr/0014-home-assistant-supervised.md
- supervised-installer 仓库：https://github.com/home-assistant/supervised-installer
- 官方弃用公告（Core / Supervised / 32 位）：https://community.home-assistant.io/t/deprecating-core-and-supervised-installation-methods-and-32-bit-systems/893617
- 社区安装方式详解：https://community.home-assistant.io/t/installation-options-explained/835564
- Proxmox HAOS 部署指南：https://mintlify.wiki/community-scripts/ProxmoxVE/guides/home-assistant

## 关联笔记

- [[Home Assistant MOC]] - Home Assistant 目录
