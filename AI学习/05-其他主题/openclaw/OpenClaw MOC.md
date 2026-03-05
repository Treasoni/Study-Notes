---
tags: [openclaw, moc, 索引, 数字人]
created: 2026-03-04
updated: 2026-03-04
---

# OpenClaw 学习索引 (MOC)

> [!info] 概述
> OpenClaw 是一个**自托管 AI 网关**，连接聊天应用（WhatsApp、Telegram、Discord 等）与 AI 智能体。本索引整理了从入门到进阶的完整学习路径。

## 快速导航

| 我想... | 推荐文档 |
|---------|----------|
| 了解 OpenClaw 是什么 | [[OpenClaw核心概念]] |
| 安装 OpenClaw | [[OpenClaw安装教程]] |
| 安装后配置 | [[OpenClaw安装后配置指南]] |
| 局域网访问 Web 控制台 | [[OpenClaw Web控制台局域网访问配置]] |
| 设置开机自启 + HTTPS | [[OpenClaw网关开机自启与HTTPS配置]] |
| 对接第三方软件 | [[OpenClaw对接第三方软件指南]] |
| **多 Agent 协作** | [[OpenClaw多智能体协作指南]] |
| 了解商业应用 | [[OpenClaw数字人商业调查]] |
| 查常用命令 | [[OpenClaw常用命令速查]] |

---

## 文档列表

### 1. 核心概念

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[OpenClaw核心概念]] | `gateway`, `架构`, `概念` | 什么是 OpenClaw、为什么需要、Hub-and-Spoke 架构 |

### 2. 安装与配置

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[OpenClaw安装教程]] | `安装`, `部署` | 多平台安装指南（一键脚本、npm、Docker、源码编译） |
| [[OpenClaw安装后配置指南]] | `配置`, `终端`, `API` | 配置向导、命令行配置、API 设置 |
| [[OpenClaw Web控制台局域网访问配置]] | `web`, `局域网`, `cors`, `tailscale` | CORS、安全上下文、设备配对、Tailscale HTTPS |
| [[OpenClaw网关开机自启与HTTPS配置]] | `daemon`, `systemd`, `tailscale`, `https` | 开机自启配置、Tailscale Serve HTTPS |

### 3. 集成与应用

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[OpenClaw对接第三方软件指南]] | `集成`, `plugins`, `skills` | Skills 插件系统、第三方 API 对接、通讯软件集成 |
| [[OpenClaw多智能体协作指南]] | `multi-agent`, `协作`, `团队` | 多 Agent 架构、协作模式、异构模型配置 |
| [[OpenClaw数字人商业调查]] | `数字人`, `商业调查` | 数字人应用场景、API vs 本地部署、成本估算 |

### 4. 参考手册

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[OpenClaw常用命令速查]] | `命令`, `cli`, `速查` | 按使用场景整理的 CLI 命令速查表 |

---

## 学习路径

### 新手路径

```
1. [[OpenClaw核心概念]] - 理解什么是 AI 网关
   ↓
2. [[OpenClaw安装教程]] - 选择合适的方式安装
   ↓
3. [[OpenClaw安装后配置指南]] - 配置大模型 API
   ↓
4. [[OpenClaw Web控制台局域网访问配置]] - 远程访问配置
```

### 进阶路径

```
1. [[OpenClaw对接第三方软件指南]] - 扩展功能
   ↓
2. [[OpenClaw多智能体协作指南]] - 搭建 AI 团队
   ↓
3. [[OpenClaw数字人商业调查]] - 了解应用场景
```

---

## 文档关系图

```
OpenClaw 学习体系
│
├── 入门层
│   ├── OpenClaw核心概念（是什么）
│   └── OpenClaw安装教程（怎么装）
│
├── 配置层
│   ├── OpenClaw安装后配置指南（基础配置）
│   ├── OpenClaw Web控制台局域网访问配置（网络配置）
│   └── OpenClaw网关开机自启与HTTPS配置（服务部署）
│
├── 应用层
│   ├── OpenClaw对接第三方软件指南（功能扩展）
│   ├── OpenClaw多智能体协作指南（AI 团队）
│   └── OpenClaw数字人商业调查（商业应用）
│
└── 参考层
    └── OpenClaw常用命令速查（命令手册）
```

---

## 相关技术

| 技术                                              | 关系             | 相关文档                       |
| ----------------------------------------------- | -------------- | -------------------------- |
| [Tailscale使用指南](../../02-工具使用/Tailscale使用指南.md) | 用于远程安全访问       | [[OpenClaw Web控制台局域网访问配置]] |
| [[../../01-基础概念/MCP协议\|MCP]]                    | 类似的 AI 集成协议    | -                          |
| Skills                                          | OpenClaw 的插件系统 | [[OpenClaw对接第三方软件指南]]      |

---

## 外部资源

### 官方资源
- [OpenClaw 官网](https://openclaw.ai)
- [官方文档](https://docs.openclaw.ai)
- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.ai.ai/skills)

### 社区资源
- [OpenClaw 中文社区](https://github.com/openclaw/openclaw/discussions)
- [阿里云开发者社区](https://developer.aliyun.com)

---

## 相关文档

- [[../RAG技术入门指南]]
- [[../../02-工具使用/Tailscale使用指南]]
