# 在飞牛 fnOS 上搭建 nastool 家庭影院 - 意图文件

## 基本信息

- **主题**: 在飞牛 fnOS 上搭建 nastool 家庭影院（以最新可用方案为主线）
- **项目标识**: nastool-fnos-deploy
- **运行标识**: nastool-fnos-deploy
- **创建时间**: 2026-10-06
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: `/Users/zhqznc/Documents/项目`
- **笔记目录**: `流媒体与影音/nastool 家庭影院 fnOS 部署`
- **MOC 路径**: `流媒体与影音 MOC.md`
- **触发来源（视频）**: https://www.bilibili.com/video/BV1egF7eFERT/
  - 标题：《飞牛Nas小课堂之部署nastool家庭影院（图形化篇）》
  - UP 主 / 发布：双栈工坊工作室 / 2025-01-31
  - 标签：Docker 部署、飞牛 Nas；简介指向 `blog.010322.xyz` 搜索 nastool 取配置文件

## 学习目标

### 笔记类型
实战笔记（跟着做就能搭起来）

### 学习深度
入门优先 · 照做即用

### 用户基础
已装 fnOS + Docker，未装过 nastool

### 已确认的关键口径
- **版本口径**：以**当前仍活跃的方案**为主线，原版 nastool 只作背景与沿革提及（用户在四个选项中选了「直接写最新可用方案」）。
- **准备章节起点**：用户已有 Docker 环境，从「有 Docker 之后」讲起，**不铺** Docker / fnOS 系统安装。
- **输出形态**：直接发布到 vault「流媒体与影音」目录，风格对齐库内 `[[流媒体与影音/小雅 fnOS 单容器部署（总览）]]`——小白友好、结论先行、术语扫盲表、Callout、引文对照（原文 / 中译 / 出处）、章节小结。

## 研究计划

### 探索方向
1. **现状与选型**：原版 nastool 的沿革与停止维护情况；当前主流替代方案（初步指向 MoviePilot）的活跃度、版本与镜像来源；哪些方案在 fnOS 上有成熟部署路径。
2. **部署实操**：Docker Compose / fnOS 应用中心图形化部署；目录规划与权限（UID/GID）；端口与网络模式；配置文件关键字段；与飞牛影视 / Jellyfin 的对接。
3. **生态与对接**：下载器（qBittorrent / Transmission）、站点索引（PT）、媒体服务器、硬件解码、外网访问、常见坑与 FAQ。

### 重点收集
- **核心概念**：「nastool 家庭影院」到底解决什么问题；它与下载器、媒体服务器、站点索引三者的关系；订阅 / 刮削 / 硬链接整理的基本机制。
- **实战代码**：`docker-compose.yml` 骨架、环境变量表、关键路径示例。
- **常见坑**：权限（UID/GID）、路径映射、端口冲突、站点认证失败、外网播放失败、日志排错。
- **工具链**：Docker、qBittorrent / Transmission、Jellyfin / 飞牛影视、TMDB、站点索引。

### 信源偏好
- 官方文档：是
- 技术博客：是（含视频简介指向的 `blog.010322.xyz`）
- 社区讨论：是
- 学术论文：否

## 备注

- **视频不是唯一主线**：视频是动机与参考来源之一，成品以最新可用方案为准。
- **待核实的关键判断**：原版 `jxxghp/nas-tools` 已停止维护、作者转向 MoviePilot —— 该判断必须由 `research-collector` 用最新来源核实，**不得直接当结论写入成品**；若不成立，须回来修正本意图文件。
- 遵守 `.claude/rules/obsidian/note-system.md`（frontmatter、标签、Callout、双链、引文语言）与 `.claude/rules/obsidian/note-style.md`（入门优先档全套契约）。
