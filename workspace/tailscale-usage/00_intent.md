# Tailscale 使用教程 - 意图文件

## 基本信息

- **主题**: 学习使用 Tailscale（Tailscale 使用教程）
- **项目标识**: tailscale-usage
- **创建时间**: 2026-08-28
- **当前阶段**: 阶段 0
- **输出目标**: obsidian
- **Vault 路径**: D:\Study-Notes
- **笔记目录**: 内网穿透
- **MOC 路径**: 待指定

## 学习目标

### 笔记类型
实战笔记

### 学习深度
上手

### 用户基础
有了解

## 研究计划

### 探索方向
1. **Tailscale 基础与安装**：账号体系、登录鉴权、各平台客户端（Windows/Linux/macOS/移动端）、节点接入与 `tailscale up`
2. **常用功能实战**：组网与节点管理（`tailscale status/ip`）、ACL 权限配置、子网路由（subnet router）、Exit Node、端口暴露（`tailscale serve` / `tailscale funnel`）、MagicDNS 与 Tailscale SSH、分享节点
3. **生态与排错**：与 ZeroTier / frp 的对比与选型、Headscale 自建控制面、自建 DERP、常见坑（登录鉴权、打洞失败走中继、ACL 误配、exit node 流量路径）

### 重点收集
- **核心概念**: 控制面/数据面、WireGuard 协议、MagicDNS、ACL（tailnet policy）、子网路由、exit node、tailscale serve/funnel、DERP 中继、节点密钥与认证
- **实战代码**: 安装命令、`tailscale up` / `status` / `ip` / `ping` / `set`、ACL JSON 示例、`tailscale up --advertise-routes`、`--exit-node`、`tailscale serve` 命令、Tailscale SSH
- **常见坑**: 账号登录与设备上限、打洞失败静默走 DERP、ACL 误配置导致不通、exit node 流量被限、子网路由未开启 IP forwarding、企业/个人套餐限制
- **工具链**: Tailscale CLI、Web 管理台（login.tailscale.com）、Headscale、自建 DERP、`tailscale ping` 排错

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 是（排错经验）
- 学术论文: 否

## 备注

- 用户已了解 NAT、P2P/中继、上行带宽等内网穿透概念（此前完成《内网穿透带宽性能分析》）。
- 输出到 Obsidian vault `D:\Study-Notes\内网穿透\`，与上一篇同目录，可形成「内网穿透」主题系列。
- 深度为「上手」：以能独立安装、组网、做端口转发、掌握常用命令与常见排错为目标，不深入自建控制面（作为进阶方向提及即可）。
