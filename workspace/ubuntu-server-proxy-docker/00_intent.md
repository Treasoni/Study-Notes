# 在 ubuntu-server 中配置翻墙（代理），并让 Docker 容器和其他应用可以正常使用 - 意图文件

## 基本信息

- **主题**: 在 ubuntu-server 中配置翻墙（代理），并让 Docker 容器和其他应用可以正常使用
- **项目标识**: ubuntu-server-proxy-docker
- **创建时间**: 2026-08-29
- **当前阶段**: 阶段 0
- **输出目标**: project-output（先存项目 workspace，发布 Obsidian 时再指定目录）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: docker/Docker MOC.md（默认挂载）

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手实战

### 用户基础
有了解（有 Linux/Docker 基础）

## 研究计划

### 探索方向
1. Ubuntu Server 上 Clash/Mihomo 内核的安装与配置（订阅节点、systemd 服务）
2. 系统级代理接管：bash/zsh 环境变量、apt、curl/git 等命令行工具
3. Docker 走代理的三种路径：daemon.json 镜像拉取、容器 HTTP_PROXY 环境变量、透明代理全局接管

### 重点收集
- **核心概念**: 代理协议（HTTP/SOCKS5）、TUN 模式、iptables 透明代理、环境变量代理、Docker 代理优先级
- **实战代码**: 订阅导入命令、systemd unit、docker daemon.json、docker-compose 代理环境变量、透明代理脚本
- **常见坑**: 容器内不能用 127.0.0.1 访问宿主机代理、daemon.json 修改需重启 docker、TUN 与网卡冲突、代理回环
- **工具链**: Clash/Mihomo、订阅服务、curl、docker、docker-compose、iptables

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是
- 学术论文: 否

## 备注

- 与既有笔记衔接：`docker/docker进行代理.md`（宿主机已有 Clash 时 Docker 走 HTTP_PROXY）、`外网如何使用代理进行翻墙.md`（Clash 认证）、`docker/镜像加速器vs代理-概念对比.md`
- 方向已确认：方案 A（Clash/Mihomo 客户端为主），可补充透明代理要点
- 本笔记聚焦「服务器端完整落地」，非 Windows/Docker Desktop 场景
