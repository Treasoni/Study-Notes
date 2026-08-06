# Home Assistant 中 ha 命令的使用 - 意图文件

## 基本信息

- **主题**: Home Assistant 中 ha 命令的使用（Home Assistant CLI）
- **项目标识**: home-assistant-ha-command
- **创建时间**: 2026-08-06
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: `C:\note\Study-Notes`
- **笔记目录**: `homeassistant/ha-command`
- **MOC 路径**: `homeassistant/Home Assistant MOC.md`

## 学习目标

### 笔记类型
实战速查手册（concept + cheat_sheet 混合：先讲清 ha 命令是什么、怎么进终端，再给常用命令实战 + 完整速查表）

### 学习深度
上手速查（覆盖常用子命令 + 速查表 + 常见坑）

### 用户基础
有了解（已有 HAOS 部署环境）

## 研究计划

### 探索方向
1. ha CLI 概述与进入方式（SSH & Web Terminal / VS Code addon / 系统控制台）
2. 核心命令组实战：`ha core`、`ha supervisor`、`ha addons`
3. 系统级命令组：`ha host`、`ha os`、`ha network`、`ha hardware`
4. 运维命令组：`ha info`、`ha logs`、`ha update`、`ha backups`、`ha resolution`
5. 常见坑与最佳实践 + 完整速查表

### 重点收集
- **核心概念**: `ha` 命令与 Supervisor / HAOS / Docker 的关系；命令结构（`ha <group> <command>`）；权限与执行环境
- **实战代码**: 各子命令常用语法与示例（core update、supervisor logs、addons list/install、host reboot、os update、network info、hardware info、info 输出解读等）
- **常见坑**: 非 HAOS/Supervised 环境（Docker Container 直装）无 `ha` 命令；命令需在终端 addon 或宿主机执行；`ha` 与 `hass-cli` 是不同工具；部分命令耗时较长
- **工具链**: SSH & Web Terminal addon、Advanced SSH & Web Terminal、VS Code addon、HAOS 系统控制台

### 信源偏好
- 官方文档: 是（home-assistant.io 官方 CLI 文档）
- 技术博客: 是
- 社区讨论: 是

## 备注

- 命令范围：**只讲 `ha` 命令本身**，不扩展 hass-cli / REST API
- 与既有笔记互链：
  - [[homeassistant/haos-deploy/部署 HAOS 详细教程]]（HAOS 部署，含 `ha` 命令初见）
  - [[homeassistant/Home Assistant 部署方式对比]]（部署方式决定 `ha` 命令可用性）
  - [[homeassistant/Home Assistant MOC]]
