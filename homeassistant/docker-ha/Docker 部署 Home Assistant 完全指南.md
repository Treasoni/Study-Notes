---
title: "Docker 部署 Home Assistant 完全指南：HACS、国内稳定运行与 Addon 实战"
tags:
  - Home-Assistant
  - Docker
  - HACS
  - 智能家居
  - 运维
  - 实战教程
created: 2026-08-08
updated: 2026-08-08
status: 已完成
source_project: docker-ha-tutorial
type: index
---

# Docker 部署 Home Assistant 完全指南：HACS、国内稳定运行与 Addon 实战

> 本篇实战笔记把 Home Assistant 的 Docker Container 路线完整走通：从认清三种部署方式的定位，到用 `docker run` / `docker-compose` 把 HA 跑起来；从安装 HACS 补足社区生态，到锁版本、备份、回滚建立稳定运维闭环；最后用 Docker 把 addon 一个一个「装」回来。全程以国内网络为硬约束，镜像拉取、HACS 下载与更新策略都给出了可落地的加速方案。

## 学习路径

主线：**部署（1-3）→ HACS 生态（4-5）→ 稳定运维（6-7）→ addon 补齐（8-9）**

| 章 | 标题 | 内容 |
|----|------|------|
| 1 | [[01_为什么是Docker版_部署架构与能力边界\|为什么是 Docker 版]] | 部署架构与能力边界：无 Supervisor 的全局观 |
| 2 | [[02_快速起跑_docker-run部署与config目录结构\|快速起跑]] | `docker run` 部署 + config 目录结构 |
| 3 | [[03_工程化部署_docker-compose完整配置与三大关键决策\|工程化部署]] | `docker-compose` 完整配置 + 网络/设备/镜像三大决策 |
| 4 | [[04_HACS安装_Docker三种路径与国内加速\|HACS 安装]] | Docker 三种安装路径 + 国内加速 |
| 5 | [[05_HACS首次配置与常用仓库实战\|HACS 配置]] | HACS 3.x 首次配置 + 常用仓库 |
| 6 | [[06_国内稳定运行_版本锁定与镜像加速策略\|国内稳定运行]] | 版本锁定 + 镜像加速策略 |
| 7 | [[07_更新回滚与备份_运维三件套\|更新、回滚与备份]] | 运维三件套完整闭环 |
| 8 | [[08_Docker部署addon_把DockerHub变成你的AddonStore\|Docker 部署 addon]] | 把 Docker Hub 变成你的 Addon Store |
| 9 | [[09_addon通信网络架构与权限避坑\|addon 通信与避坑]] | 通信、网络架构与权限避坑 |

## 学完能做什么

- compose 从零部署 Docker 版 HA，含国内镜像加速、设备直通
- 独立安装 HACS 并在国内网络完成授权
- 锁版本 + 备份 + 回滚的完整运维闭环
- 用 Docker 部署 addon 等价容器（MQTT / Node-RED / ESPHome / Zigbee2MQTT）并与 HA 打通

## 前置要求

- Docker 基本概念、Linux 命令行、HA 基础概念
- 建议先读 [[Home Assistant 三种部署方式对比与选型]]

## 相关笔记

- [[Home Assistant 三种部署方式对比与选型]] - 三种部署方式全景与选型决策
- [[部署 HAOS 详细教程]] - HAOS 部署路线（非 Docker）
- [[Home Assistant ha 命令使用]] - HAOS/HA Supervised 下 ha 命令速查
- [[Home Assistant MOC]] - Home Assistant 学习笔记总目录
