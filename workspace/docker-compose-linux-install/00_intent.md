# Docker 与 Docker Compose 安装（国内环境）- 意图文件

## 基本信息

- **主题**: Docker 与 Docker Compose 安装（国内环境）
- **项目标识**: docker-compose-linux-install
- **创建时间**: 2026-08-03
- **当前阶段**: 阶段 0
- **输出目标**: project-output（暂存，Phase 6 时再确认具体 vault 目录）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定（可能与 [[docker/Docker MOC]] 关联）

## 学习目标

### 笔记类型
实战安装教程（practice）

### 学习深度
上手

### 用户基础
有了解（知道 docker run/pull 等基础命令，安装配置和 Compose 编排不熟）

## 研究计划

### 探索方向
1. Linux（Ubuntu/Debian/CentOS）下 Docker Engine 的国内安装方案与换源
2. Docker Compose 的安装方式（plugin / standalone / apt）与版本选择
3. 国内环境下拉取镜像的加速方案（registry-mirrors、镜像源可用性 2026）
4. 安装后验证、常见坑（权限、systemd、daemon.json、内核版本、iptables）

### 重点收集
- **核心概念**: Docker Engine 组成（dockerd / containerd / runc / CLI）、Compose plugin vs standalone 区别、daemon.json 配置
- **实战代码**: 各发行版安装命令（apt / dnf/yum 仓库）、compose plugin 安装命令、registry-mirrors 配置 JSON、hello-world/nginx 验证命令
- **常见坑**: 国内 apt/dnf 源替换、Docker Hub 拉取超时、镜像加速器失效清单、`docker: permission denied`、systemd 启动失败、内核版本要求
- **工具链**: 阿里云/腾讯云镜像源、国内 Docker 镜像加速器（1Panel、DaoCloud 等）、docker compose v2

### 信源偏好
- 官方文档: 是（Docker Docs 官方安装页）
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- vault 已有 [[docker/Windows-DockerDesktop安装指南-国内网络版]]，本笔记聚焦 **Linux 服务器原生安装**，避免重复 Windows 内容。
- vault 已有 [[docker/DockerDesktop镜像加速器配置]]、[[docker/镜像加速器vs代理-概念对比]]，镜像加速部分应互相引用而非照搬。
- Docker Compose 目前没有独立安装指南，本笔记是 Compose 安装的首篇覆盖。
- 国内镜像源可用性变化快（2026），素材收集时应优先近期可用源并标注验证日期。
- 表格不得嵌套在列表项内（Obsidian 渲染限制）；YAML frontmatter 的 sources 含特殊字符须正确引用。
