# 用 Docker 部署 Hermes 并配置消息平台接入 - 意图文件

## 基本信息

- **主题**: 用 Docker 部署 Hermes 并配置消息平台接入（Telegram / Discord）
- **项目标识**: hermes-docker-deploy
- **创建时间**: 2026-08-28
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: /Users/zhqznc/Documents/项目
- **笔记目录**: AI学习/Hermes Agent/Hermes Docker 部署指南
- **MOC 路径**: AI学习/Hermes Agent/Hermes Agent MOC.md

## 学习目标

### 笔记类型
实战笔记（上手实战，详细步骤 + 配置方法）

### 学习深度
上手

### 用户基础
有了解（已有《Hermes Agent 上手实战》《Hermes Tool 配置指南》两册）

## 研究计划

### 探索方向
1. Hermes 本体 Docker 部署的完整步骤（docker run / Compose / 数据卷挂载 / 首次 setup 向导）
2. 国内消息平台接入：微信 / 飞书 / QQ（bot/webhook 桥接到 Hermes API Server 或 Gateway）
3. 平台接入后的日常运维：日志、升级、常见坑、安全基线

### 重点收集
- **核心概念**: Docker 数据卷持久化、Gateway 模式、国内平台 bot/webhook 桥接、API Server 安全三件套
- **实战代码**: docker run 命令、docker-compose.yaml 完整示例、微信（wechaty 类）/ 飞书 / QQ（官方或 go-cqhttp）接入片段
- **常见坑**: PermissionError /opt/hermes/.env、数据目录排他锁、bot token 泄露、公网暴露无认证、国内平台风控
- **工具链**: Docker / Docker Compose、微信（wechaty 等）、飞书开放平台、QQ 开放平台 / go-cqhttp

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 与已有笔记的分工：本册聚焦「部署 + 国内消息平台配置」专项，与《上手实战》第 8 章（Docker 部署进阶）互补，避免大段重复。
- 用户已确认：国内平台 = 微信（A）+ 飞书（D）+ QQ（E）。
- 发布为独立分册：README + 每章独立文件 + 前后导航，同步更新 Hermes Agent MOC。
