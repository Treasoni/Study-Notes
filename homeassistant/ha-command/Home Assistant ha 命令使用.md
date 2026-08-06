---
title: "Home Assistant 中 ha 命令的使用"
tags:
  - 智能家居/HomeAssistant
  - HA/ha命令
  - 学习笔记
  - MOC
created: 2026-08-06
updated: 2026-08-06
status: 已完成
source_project: home-assistant-ha-command
type: tutorial-index
---

# Home Assistant 中 ha 命令的使用

> [!summary] 全文摘要
> 面向 HAOS / HA Supervised 环境的 `ha` 命令（Home Assistant CLI）实战速查手册。先讲清 `ha` 是什么、只活在哪些环境、怎么进终端；再按命令组逐个实战：核心组（core/supervisor/addons）、系统组（host/os/network/hardware）、诊断组（info/jobs/resolution）、备份组（backups）；随后串成升级与运维流程，拆解 11 条高频坑，最后用一张 19 命令组全量速查表收尾。素材采集时间 2026-08-06，命令细节以 `ha --help` 实际输出为准。

## 目录

- [[01_认识 ha 命令|第一章：认识 ha 命令]] - 本质、环境、进入方式、命名澄清
- [[02_核心命令组实战|第二章：核心命令组实战]] - core / supervisor / addons
- [[03_系统级命令组|第三章：系统级命令组]] - host / os / network / hardware
- [[04_诊断命令组|第四章：诊断命令组]] - info / jobs / resolution
- [[05_备份与恢复|第五章：备份与恢复]] - backups 备份恢复链路
- [[06_升级与运维流程|第六章：升级与运维流程]] - 升级顺序、配置生效、远程调用
- [[07_常见坑与排障|第七章：常见坑与排障]] - 11 条坑 + 排障路径
- [[08_完整速查表|第八章：完整速查表]] - 19 命令组全量速查

## 学习路径

本手册沿「认识 → 实战 → 流程 → 排障 → 速查」展开。第 1 章建立 `ha` 命令的心智模型（本质、环境、入口）；第 2-5 章按命令组实战，覆盖日常 80% 运维场景；第 6 章把命令串成升级与运维 SOP；第 7 章提供高频坑排障；第 8 章是日常不翻正文直接查的全量速查表。

本文与 [[Home Assistant 三种部署方式对比与选型]] 分工明确：选型笔记回答「HAOS / Docker Container / Supervised 该选哪个」；本文默认你已在 HAOS / HA Supervised 环境，只讲 `ha` 命令本身。部署实操见 [[homeassistant/haos-deploy/部署 HAOS 详细教程]]。

## 笔记信息

- **笔记类型**：实战速查手册（concept + cheat_sheet）
- **学习深度**：上手速查
- **命令范围**：只讲 `ha` 命令本身（不覆盖已弃用的 hass-cli 与 REST API）
- **采集时间**：2026-08-06
- **时效性声明**：命令子命令随版本演化（如开发版 `ha addons` 改名 `ha apps`、`ha host update` 已废弃），执行前以 `ha <group> --help` 实际输出为准。
