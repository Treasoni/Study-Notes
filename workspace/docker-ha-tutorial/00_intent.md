# 用 Docker 配置 Home Assistant（HA）详细教程 - 意图文件

## 基本信息

- **主题**: 用 Docker 配置 Home Assistant（HA）详细教程：HACS、国内环境稳定使用与更新、Docker 部署 addon
- **项目标识**: docker-ha-tutorial
- **创建时间**: 2026-08-08
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: C:\note\Study-Notes
- **笔记目录**: homeassistant/docker-ha/
- **MOC 路径**: homeassistant/Home Assistant MOC.md

## 学习目标

### 笔记类型
实战教程（practice）

### 学习深度
精通进阶

### 用户基础
有了解（知道 Docker 基本概念，可能装过 HAOS，但不熟 Docker 版 HA）

## 用户核心需求

1. 使用 Docker 部署 Home Assistant（HA），给出完整可用的配置
2. 包括如何使用 HACS（安装、国内网络环境下的访问）
3. 如何稳定使用、如何更新（在国内环境中：镜像源、更新策略、版本锁定）
4. 如何用 Docker 部署 addon 给 HA（Docker Container 无内置 Addon Store，需用容器方式补足）

## 研究计划

### 探索方向
1. Docker 版 HA 部署（docker run / docker-compose，目录映射、设备映射、网络配置）
2. HACS 安装与使用（下载、国内加速、常用前端仓库、社区集成）
3. 国内环境稳定使用与更新（镜像加速、更新策略、版本锁定、备份/回滚）
4. Docker 方式部署 addon（官方 addon 容器化、自定义容器 addon、与 HA 的通信方式）

### 重点收集
- **核心概念**: HA Container 部署架构、configuration.yaml、docker-compose 服务编排、HACS 下载源、addon 容器原理
- **实战代码**: docker-compose.yml 完整示例、HACS 安装命令、国内镜像源配置、addon docker run/compose 示例
- **常见坑**: Docker 版没有 Supervisor/Addon Store、设备映射权限、网络 host 模式、国内拉镜像失败、更新后配置不兼容
- **工具链**: Docker / Docker Compose、HACS、ghcr/github 代理、容器镜像加速器

### 信源偏好
- 官方文档: 是（HA 官方 Docker 部署文档、HACS 官方文档）
- 技术博客: 是
- 社区讨论: 是

## 与既有笔记的关系

- [[Home Assistant 三种部署方式对比与选型]]：已有 Docker Container 概览章节，本笔记做 Docker 专项深度展开
- [[部署 HAOS 详细教程]]：HAOS 部署（非 Docker），本笔记聚焦 Docker Container 路线
- 本笔记重点补齐：HACS 实战、国内环境稳定运行、Docker 部署 addon

## 备注

- 输出到 Obsidian `homeassistant/docker-ha/`，拆分多文件（索引页 + 章节），同步更新 MOC
- 国内环境是硬约束：所有镜像拉取、HACS 下载、更新检查都需考虑国内可访问性
