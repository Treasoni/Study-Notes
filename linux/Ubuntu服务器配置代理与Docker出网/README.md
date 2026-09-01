---
title: "Ubuntu 服务器配置代理与 Docker 出网"
tags:
  - ubuntu
  - linux
  - 代理
  - 翻墙
  - docker
  - mihomo
  - MOC
created: 2026-08-29
updated: 2026-08-29
status: 已完成
source_project: ubuntu-server-proxy-docker
---

# Ubuntu 服务器配置代理与 Docker 出网

这是一篇实战向的部署笔记，面向有 Linux/Docker 基础、想在 Ubuntu Server 上给整条出网链路（命令行 / apt / git / Docker）统一配一个翻墙代理的开发者。全文按「方案选型 → 安装 mihomo 内核 → 配置 config.yaml → 系统级代理接管 → Docker 走代理 → 验证清单与常见坑」共六章组织：先选定「显式代理 + mihomo 内核」的路线，装好内核并写一份能跑的 config.yaml，随后用环境变量、apt、git 配置把系统命令接入代理，再区分 Docker 拉镜像与容器内应用出网两条路径分别配置，最后用一张端到端验证清单和常见坑速查表收尾。

## 目录

- [[01_总览与方案选型]] — 方案选型：为什么服务器端用 mihomo + 显式代理
- [[02_安装mihomo内核]] — 下载安装 mihomo 二进制，并用 systemd 守护
- [[03_配置config.yaml]] — 入站端口、订阅导入、节点分组与最小配置
- [[04_系统级代理接管]] — 环境变量 / apt / git，让系统命令走代理
- [[05_Docker走代理]] — daemon 拉镜像与容器内应用出网两条路径
- [[06_验证清单与常见坑]] — 端到端验证清单与常见坑速查表

## 学习路径

1. **第 1-2 章**：选型与落地——确定显式代理方案，装好 mihomo 内核并用 systemd 守护。
2. **第 3 章**：写 config.yaml，把订阅节点、分组、规则接进去，让内核真正具备分流能力。
3. **第 4 章**：发三张「通知单」——环境变量、apt 配置、git 配置，让系统命令走代理。
4. **第 5 章**：Docker 拉镜像与容器出网两条路径，分别配置并验证。
5. **第 6 章**：端到端验证清单与常见坑速查表，随时回查。

## 相关笔记

- [[linux MOC]]
- [[docker/docker进行代理]]
- [[docker/镜像加速器vs代理-概念对比]]
- [[外网如何使用代理进行翻墙]]
- [[linux/GitHub 国内网络连接超时解决方案/README|GitHub 国内网络连接超时解决方案]]

## 笔记信息

- **创建/更新**：2026-08-29 · **状态**：已完成
- **源项目**：ubuntu-server-proxy-docker
- **类型**：实战笔记（部署 + 原理）
