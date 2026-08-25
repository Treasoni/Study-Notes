# stremio-web 项目研究 - 意图文件

## 基本信息

- **主题**: stremio-web 项目：能看高质量资源吗？如何部署与接入影视资源？
- **项目标识**: stremio-web
- **创建时间**: 2026-08-26
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: GitHub项目
- **MOC 路径**: GitHub项目/GitHub项目 MOC.md

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手实战

### 用户基础
有了解（已跑通 lunatv 影视聚合，聚合播放器概念相通）

## 研究计划

### 探索方向
1. **A. stremio-web 是什么 + 核心能力**：项目定位、插件/Addon 生态、Torrent 流媒体原理、画质上限
2. **B. 部署与接入**：自部署方式（Docker/Vercel）、Addon 配置、Real-Debrid / 网盘 / PT 等高质量源接入
3. **C. 高质量资源路线**：4K / Remux 资源怎么来、与 lunatv 对比、哪个更适合高质量观影

### 重点收集
- **核心概念**: Stremio 架构、Addon/插件系统、Torrent 流媒体、Debrid 服务（Real-Debrid）、自部署、目录（Catalog）/元数据/流（Stream）协议
- **实战代码**: 部署命令（Docker compose）、Addon 安装链接、Debrid 配置示例
- **常见坑**: 种子速度慢/被墙、版权/磁力限制、Debrid 配置、4K 播放卡顿、无 Meta/图片刮削
- **工具链**: stremio-web、Stremio 官方客户端、Addon 生态（社区）、Real-Debrid、网盘

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 用户之前做完 lunatv（LunaTV导入影视网站），核心诉求是「高质量资源」——本篇需要明确回答 stremio-web 在画质上的上限与获取路径，并可与 lunatv 对比。
- 最终发布到 `GitHub项目/`，与 lunatv 笔记同目录。
