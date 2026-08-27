# fnOS Docker 部署 Tailscale 子网路由器（Subnet Router）实战教程 - 意图文件

## 基本信息

- **主题**: fnOS Docker 部署 Tailscale 子网路由器（Subnet Router）实战教程
- **项目标识**: tailscale-subnet-router-fnos
- **创建时间**: 2026-08-28
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: 内网穿透
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记（上手深度，可直接照做 + 原理要点 + 排错深化）

### 学习深度
上手

### 用户基础
有了解（已手写一份可用草稿，覆盖基本配置与常见排错）

## 研究计划

### 探索方向
1. **fnOS 部署全流程**：Docker Compose 配置（host 网络 / privileged / cap_add）、宿主机内核转发（sysctl）、放行 FORWARD 与 NAT 伪装（iptables）、Tailscale 控制台授权 Subnet route、外网客户端开启 Use Tailscale subnets。
2. **原理与架构**：Tailscale overlay / WireGuard 基础、100.64.0.0/10 CGNAT 网段、子网路由（subnet route）如何工作、Docker 默认 FORWARD DROP 与回程路由缺失的根因、NAT 伪装（MASQUERADE）的作用。
3. **验证与排错深化**：连通性测试命令（tailscale status / ping / traceroute / nc）、从 tailscale0 网卡观测、常见坑扩展（TS_ROUTES 末尾逗号、TUN busy、路由未授权不下发、多容器抢占、路由冲突、防火墙）。

### 重点收集
- **核心概念**: Tailscale overlay、WireGuard、CGNAT 100.64.0.0/10、subnet route、NAT 伪装、Docker host 网络、内核 IPv4 转发、tun 设备
- **实战代码**: Docker Compose 完整配置、sysctl 配置、iptables 规则、Tailscale 控制台操作、客户端开关配置
- **常见坑**: TS_ROUTES 末尾逗号、TUN device busy、FORWARD 链 DROP 拦截、内网设备回程路由缺失、Subnet route 未授权不下发
- **工具链**: fnOS、Docker Compose、Tailscale CLI（tailscale status/ping/up）、iptables、sysctl

### 信源偏好
- 官方文档: 是（Tailscale Subnet Router / Site-to-site 官方文档优先）
- 技术博客: 是
- 社区讨论: 是（fnOS 相关、Tailscale 论坛/Reddit 排错）
- 学术论文: 否

## 备注

- **与既有笔记关系**：独立新笔记，发布时双链引用 [[内网穿透/Tailscale使用教程.md]]（已存在的通用 Tailscale 教程）。
- **用户已提供草稿**：五部分（Compose 配置 / sysctl 转发 / iptables 放行与 NAT / 控制台与客户端配置 / 排错表），作为核心素材，重点补充「原理与架构」与「验证与排错深化」。
- **排错表扩展方向**：保留并扩充用户表格（TS_ROUTES 逗号、TUN busy、tracert 首跳通但打不开内网网页），补充路由未授权、路由冲突、防火墙放行等场景。
