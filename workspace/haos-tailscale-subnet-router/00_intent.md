# 如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由 - 意图文件

## 基本信息

- **主题**: 如何用 HAOS 部署的 Home Assistant 中的 Tailscale 插件实现内网穿透和子路由（Subnet Router）
- **项目标识**: haos-tailscale-subnet-router
- **运行标识**: haos-tailscale-subnet-router
- **工作流**: learning-note-flow
- **工作流状态文件**: `workspace/workflow-runs/haos-tailscale-subnet-router.workflow.md`
- **创建时间**: 2026-09-12
- **当前阶段**: 阶段 0（意图澄清）
- **输出目标**: project-output（先写入项目 `workspace/haos-tailscale-subnet-router/output/`，阶段 6 再确认是否发布到 Obsidian vault）
- **Vault 路径**: 待指定
- **笔记目录**: 待指定
- **MOC 路径**: 待指定（阶段 7 需同步 MOC）

## 学习目标

### 笔记类型
实战笔记（可直接照做；每步给出可操作的插件配置与验证命令，原理只讲到够用）

### 学习深度
上手

### 用户基础
零基础（尚未安装 Tailscale 插件，从零开始；已有 HAOS 部署环境）

## 研究计划

### 探索方向
1. **HAOS 中 Tailscale 插件的安装与登录授权**：插件商店安装、插件选项配置（auth key / 交互登录 / 主机名）、首次启动与状态确认，以及 Home Assistant 侧需要配合的配置。
2. **内网穿透**：通过 Tailscale 从外网访问 HAOS 本身（Home Assistant Web UI，8123 端口）与局域网内的其他服务；说明 Tailscale 直连与中继（DERP）的差别，以及 MagicDNS 的用法。
3. **子路由（Subnet Router）**：`advertise-routes` 的配置位置与写法（插件选项 vs `tailscale up` 参数）、管理控制台的路由授权、客户端 `Use Tailscale subnets` 开关；重点说明 HAOS 插件运行在容器中的网络可见性限制，以及可行的做法（如 host 网络 / `TS_ROUTES` 选项 / 是否需要额外放行）。
4. **验证与排错**：`tailscale status` / `tailscale ping` / 路由表检查 / 从远端访问内网 IP 的连通性测试；路由未授权、路由不下发、回程路由缺失、DNS（`--accept-dns`）、exit node 与 subnet router 混淆等常见失败点。

### 重点收集
- **核心概念**: Tailscale overlay 网络、WireGuard、CGNAT 网段 `100.64.0.0/10`、subnet router / route advertisement、路由授权（route approval）、内网穿透与子路由的区别、HAOS 插件容器网络（host network）、MagicDNS、exit node
- **实战代码**: Tailscale 插件的配置项（YAML / 表单）、`advertise-routes` 配置示例、控制台路由授权步骤、客户端开关、验证用 CLI 命令
- **常见坑**: 子网路由未在控制台授权导致不下发、`advertise-routes` 写法错误、插件容器对本地网段的可见性限制、DNS 被覆盖导致内网域名解析异常、把 exit node 当成 subnet router 使用
- **工具链**: HAOS、Home Assistant Supervisor 插件商店中的 Tailscale 插件、Tailscale 管理控制台、`tailscale` CLI、PC/手机 Tailscale 客户端

### 信源偏好
- 官方文档: 是（Tailscale 官方 Subnet Router / Site-to-site 文档、Home Assistant 插件文档优先）
- 技术博客: 是
- 社区讨论: 是（Home Assistant 社区论坛、Tailscale 论坛）
- 学术论文: 否

## 备注

- **与既有笔记的关系**: 独立新笔记。同主题已有 `tailscale-usage`（通用使用教程）与 `tailscale-subnet-router-fnos`（fnOS + Docker 部署），本文聚焦 HAOS 插件这一部署形态，发布时可双链引用作为对比。
- **用户当前状态**: 从零开始，笔记需要包含「安装插件 → 登录授权 → 开启内网穿透 → 配置子路由」的完整首步链路。
- **输出策略**: 先写项目 `output/`，阶段 6 发布前再确认 Obsidian vault 与笔记目录，阶段 7 按约定同步 MOC。
