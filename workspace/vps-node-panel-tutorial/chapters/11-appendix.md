## 附录 A：速查表

> 本表**只汇总前文各章已经出现、且已挂来源**的命令与端口，不引入新事实；每条只给"做什么 + 去哪一章看"。凡涉及价格、套餐、版本号、星标数等易失信息，一律以**观测日 2026-09-23** 为准（来源：B-2 / B-6 / A-3 | Stars）。

### A.1 端口与放行清单

| 端口 / 位置 | 说明 | 参考 |
|---|---|---|
| SSH `22` | sshd 默认端口，可改 | 第 4 章（C-4 | KEYWORDS Port） |
| 面板端口 `2053` | Docker Compose 默认只发布该端口 | 第 5 章（B-1 | Using Docker Compose） |
| 入站（代理）端口 | 建节点时自定义；Docker 部署**不会自动暴露** | 第 5、6 章（B-1 | Using Docker Compose） |
| 系统防火墙 | `ufw` 或 `iptables` 放行 | 第 5 章 |
| 云厂商安全组 | 与系统防火墙是**两处**，漏一处就不通 | 第 5 章 |

放行要写两处：**云厂商安全组** + **系统防火墙**。只放一处，面板或节点就是连不上。

### A.2 命令速查

| 目的 | 命令 | 参考 |
|---|---|---|
| 一键安装面板 | `bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)` | 第 5 章（B-1 | Install in one-line） |
| 打开管理菜单 | `x-ui` | 第 5 章（B-1 | Install in one-line） |
| 查 CPU 架构 | `uname -m` | 第 5 章（B-1 | Manual installation） |
| 放行端口（ufw） | `ufw allow <PORT>/tcp` | 第 5 章 |
| 放行端口（iptables） | `iptables -I INPUT -p tcp --dport <PORT> -j ACCEPT` | 第 5 章 |
| SSH 登录（默认端口） | `ssh root@<VPS_IP>` | 第 4 章 |
| SSH 登录（自定义端口） | `ssh -p <PORT> root@<VPS_IP>` | 第 4 章 |
| ICMP 连通性 | `ping -c 4 <VPS_IP>` | 第 3、9 章 |
| 端口连通性 | `nc -vz <VPS_IP> <PORT>` | 第 3、9 章 |
| 路径探测 | `traceroute <VPS_IP>` | 第 9 章 |
| 生成预共享密钥 | `openssl rand -base64 32` | 第 2、6 章（A-8 | password 密钥长度表） |
| 域名解析查询 | `dig +short <DOMAIN>` | 第 7 章 |
| 取 HTTP 响应头 | `curl -I https://<DOMAIN>` | 第 7 章 |
| 代理连通自检 | `curl -x socks5h://127.0.0.1:10808 https://www.cloudflare.com/cdn-cgi/trace` | 第 8 章 |
| 重建后清理本地旧指纹 | `ssh-keygen -f "/root/.ssh/known_hosts" -R <IP>` | 第 9 章（C-5 | Control Panel 流程） |
| Docker 启动容器 | `docker compose up -d` | 第 5 章（B-1 | Using Docker Compose） |

### A.3 常见故障 → 对应章节

| 现象 | 可能原因 | 去哪一章 |
|---|---|---|
| 面板打不开 | 端口未放行（安全组或系统防火墙漏一处） | 第 5 章 |
| 面板路径或口令不对 | 随机凭据丢失 / Docker 默认凭据未改 | 第 5、10 章 |
| 节点连不上（端口层） | 入站端口未放行 / Docker 未暴露入站端口 | 第 5、6 章 |
| 域名不通 | 解析未生效 / 代理状态限制 / 域名 pending 窗口期 | 第 7 章 |
| 换 IP 后本地报 known_hosts 冲突 | 重建/恢复导致主机密钥变化 | 第 9 章 |
| 全链路连不通需排查 | 端口 → 节点参数 → 客户端本地端口 → 系统时间/加密协商 → 域名与代理状态 | 第 8 章 |

---

## 附录 B：与《自建代理节点搭建实战》的分工与互链

本篇（面板流）与既有笔记是一组互补关系，边界如下：

| 维度 | 本篇《VPS 自建节点零基础全流程（面板流）》 | 既有笔记 [[自建代理节点搭建实战]] |
|---|---|---|
| 目标 | **买与点选跑通**：从选 VPS 到客户端可用 | **原理与手写配置** |
| 配置方式 | 3x-ui 面板点选 | 手写 Xray JSON |
| 传输层 | 只交代"要选什么" | REALITY 原理 |
| 加固 | 最小加固（SSH + fail2ban） | nftables / suricata 深度加固 |

**以下三类只做指引、不在本篇展开**：

1. 手写 Xray JSON（内核直配）；
2. REALITY 原理；
3. nftables / suricata 深度加固。

需要这三块内容时，请转到 [[自建代理节点搭建实战]]（路径：`自建代理节点/自建代理节点搭建实战.md`）。

**双向链接**：本篇正文与第 10 章均已指向 [[自建代理节点搭建实战]]；请在既有笔记对应位置回链本篇，并在 [[自建代理节点 MOC]] 的「节点搭建」分组下同时收录本篇，使两篇在索引层互为参照。
