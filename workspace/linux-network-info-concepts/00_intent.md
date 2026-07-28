# Linux 网络信息获取与概念 - 意图文件

## 基本信息

- **主题**: Linux 网络信息获取与概念
- **项目标识**: linux-network-info-concepts
- **创建时间**: 2026-07-29
- **当前阶段**: 阶段 0（已完成）
- **输出目标**: Obsidian vault
- **Vault 路径**: `C:\note\Study-Notes`
- **笔记目录**: `linux/Linux网络信息获取与概念/`
- **MOC 路径**: `linux/linux MOC.md`

## 学习目标

### 笔记类型
实战笔记（概念 + 命令操作结合）

### 学习深度
系统掌握

### 用户基础
有了解（知道一些基本命令如 `ifconfig`、`ping`，但想系统学习所有常用网络查询命令和底层概念）

## 研究计划

### 学习方向
系统学习 Linux 上**获取/查询网络信息**的各种命令，以及这些网络信息背后的核心概念。

### 核心内容范围
1. **网络接口信息** - 网卡、链路状态、MAC 地址
2. **IP 地址与子网** - IPv4/IPv6、子网掩码、CIDR
3. **路由表** - 默认网关、静态路由、策略路由
4. **DNS 解析** - 域名解析流程、`/etc/resolv.conf`、systemd-resolved
5. **网络连接与 Socket** - TCP/UDP 连接状态、监听端口
6. **ARP 与邻居发现** - MAC 地址解析、邻居表
7. **网络统计与监控** - 带宽、连接数、丢包
8. **无线网络信息** - WiFi 信号、连接信息
9. **网络性能与排障** - 延迟、路由追踪、吞吐量

### 重点收集
- **核心概念**: IP、子网掩码、网关、DNS、路由表、MAC 地址、ARP、Socket、TCP/UDP、MTU
- **查询命令**: `ip`（全套子命令）、`ss`、`dig`/`nslookup`、`ping`、`traceroute`、`arp`、`nmcli`、`resolvectl`、`ethtool`、`iw`/`iwconfig`、`tcpdump`
- **配置文件**: `/etc/netplan/*.yaml`、`/etc/resolv.conf`、`/etc/hosts`、`/etc/nsswitch.conf`
- **常见坑**: net-tools vs iproute2、systemd-resolved 的行为、NetworkManager 的冲突
- **工具链**: iproute2、net-tools、NetworkManager、systemd-networkd

### 信源偏好
- 官方文档: 是
- 技术博客: 是
- 社区讨论: 否
- 学术论文: 否

## 与现有笔记的关系

- [[linux/linux如何修改网络信息.md]] - 侧重**修改**配置，本笔记侧重**查询/获取**和**概念理解**
- [[linux/linux常用命令/Linux 网络诊断与排障.md]] - 侧重排障诊断，本笔记侧重系统性概念 + 信息获取
- 两者互补不重复

## 备注

- 主题明确，无须探测式收集（P1），直接从 P0 跳转到 P2 深度收集
- 产出结构建议：按"概念"分篇，每篇包含概念解释 + 对应查询命令 + 实战示例
- 如果内容过多（超过 3000 行），按主题拆分为多篇笔记放入目标文件夹
