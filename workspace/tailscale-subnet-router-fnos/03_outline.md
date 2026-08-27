## 学习笔记大纲：《fnOS Docker 部署 Tailscale 子网路由器（Subnet Router）实战教程》

> 笔记类型：实战笔记（上手深度，可直接照做 + 原理要点 + 排错深化）
> 预计总篇幅：约 18-22 页
> 章节数：6

### 第一章：为什么需要子网路由器——原理与架构速览
- **篇幅**：中
- **覆盖要点**：Tailscale overlay 与控制面/数据面分离、WireGuard 数据面与 magicsock / DERP 回退、100.64.0.0/10 CGNAT 网段由来（RFC 6598）、子网路由器（Subnet Router）定位与默认 SNAT 行为、路由注入四条件（通告 → 批准 → 控制面下发 → 客户端 accept-routes）、路由（L3）与 ACL 两层机制、多路由器 HA 与最长前缀匹配、Docker FORWARD 默认 DROP 的根因铺垫
- **素材引用**：S1, S6, S7, S8, S10
- **代码示例**：无（配 1 张 overlay 架构示意图）

### 第二章：Docker Compose 部署 Tailscale 容器
- **篇幅**：中
- **覆盖要点**：fnOS Docker → Compose 新建项目入口、Compose 推荐版（host 网络 + privileged + TS_AUTHKEY 须 reusable + TS_STATE_DIR + TS_ROUTES + TS_HOSTNAME + /dev/net/tun + restart: unless-stopped）、最小权限变体（NET_ADMIN + NET_RAW、无 privileged）、TS_AUTHKEY 单次密钥导致的容器闪退、TS_ROUTES 正确写法（合法 CIDR、无末尾逗号）、部署侧 TUN busy 预防、`version` 字段过时警告
- **素材引用**：S0, S2, S3, S12
- **代码示例**：有（docker-compose.yml 推荐版 + 最小权限版）

### 第三章：宿主机内核转发——sysctl 开启 IP forwarding
- **篇幅**：短
- **覆盖要点**：子网路由器为何依赖内核 IPv4 转发、写入 /etc/sysctl.d/99-tailscale.conf（含 ipv6）、sysctl -p 加载与验证、未开启时的报错表现与排错入口
- **素材引用**：S0, S1, S11
- **代码示例**：有（sysctl 配置文件内容 + 验证命令）

### 第四章：防火墙放行与 NAT——iptables 规则
- **篇幅**：中
- **覆盖要点**：根因：Docker FORWARD 默认 DROP、基线修复（-P FORWARD ACCEPT + POSTROUTING MASQUERADE 100.64.0.0/10）、进阶：DOCKER-USER 链外科手术式放行、同宿主二次 MASQUERADE（#12407，mark 0x40000）与手动 NAT 规则叠加风险、ts-forward 链顺序（#13754）与启动顺序依赖、持久化注意（fnOS 防火墙后端待实机确认）
- **素材引用**：S0, S8, S9, S13
- **代码示例**：有（iptables 基线命令 + DOCKER-USER 变体）

### 第五章：控制台批准与客户端配置
- **篇幅**：短
- **覆盖要点**：Admin Console 批准子网路由（Machines → Edit route settings → 勾选网段 → Save）、autoApprovers 可选、客户端开启 Use Tailscale subnets（移动/桌面端）、Linux 客户端 --accept-routes、未授权不下发的表现
- **素材引用**：S1, S3, S7
- **代码示例**：有（tailscale set --accept-routes）

### 第六章：验证方法与排错表（扩充）
- **篇幅**：长
- **覆盖要点**：验证命令集（tailscale status / tailscale ping / ping 子网网关 / tracert / nc / 从 tailscale0 网卡观测）、深入排查（tailscale debug netmap / prefs / status --json、ip route）、排错决策树（按症状 → 根因归类）、排错表扩充（保留用户四坑：TS_ROUTES 末尾逗号、TUN device busy、tracert 首跳通但打不开内网网页；扩充：路由未授权、路由冲突、防火墙放行、同宿主二次 MASQUERADE、ts-forward 链顺序）、与既有教程双链 [[内网穿透/Tailscale使用教程.md]]
- **素材引用**：S0, S1, S7, S9, S11, S12, S13
- **代码示例**：有（tailscale / iptables / ip route 排查命令）

## 学习路径说明

### 前置要求
- 已有 fnOS 设备并能访问 Docker / Compose 功能
- 已注册 Tailscale 账号并创建 tailnet
- 知道自己的内网网段（如 192.168.x.0/24）
- 具备基础 Linux 命令行能力（能编辑 /etc/sysctl.d 下的文件、执行 sysctl / iptables）

### 学完能做什么
- 在 fnOS 上用 Docker Compose 部署 Tailscale 子网路由器
- 从外网任意 Tailscale 客户端直接访问家庭内网设备（无需逐台安装 Tailscale）
- 看懂「tracert 首跳通但打不开内网网页」这类故障，并按决策树独立定位
- 理解 subnet route 完整链路（通告 → 批准 → 下发 → accept-routes），能判断路由「没生效」卡在哪一环

### 建议学习顺序
- 主线：第 1 章（原理）→ 第 2-5 章（部署）→ 第 6 章（验证与排错）
- 若已能跑通现有草稿：可先对照第 6 章排错表自查，再回补第 1 章原理
- 预计总耗时：完整照做约 1-2 小时；排错深入另需 1-2 小时实机复现
