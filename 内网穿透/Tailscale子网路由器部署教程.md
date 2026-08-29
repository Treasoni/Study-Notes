---
title: Tailscale子网路由器部署教程
tags:
  - 内网穿透
  - Tailscale
  - Docker
  - 子网路由
  - WireGuard
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: tailscale-subnet-router-fnos
---

# fnOS Docker 部署 Tailscale 子网路由器（Subnet Router）实战教程

本教程是一篇实战笔记，定位"上手"深度：既能照着一步步部署成功，也讲清关键原理要点，并深化排错能力。目标是在 fnOS 上用 Docker Compose 部署一台 Tailscale 子网路由器（Subnet Router），让外网任意 Tailscale 客户端无需在每台内网设备上安装客户端，即可直接访问整个内网网段。全篇共 6 章：第 1 章建立原理与架构认知，第 2~5 章按部署顺序依次完成容器部署、内核转发、防火墙与 NAT、控制台批准与客户端配置，第 6 章给出验证命令集与扩充版排错表。建议按顺序阅读；若已能跑通，可先对照第 6 章排错表自查，再回补第 1 章原理。

## 目录

1. [第一章 为什么需要子网路由器——原理与架构速览](#第一章-为什么需要子网路由器原理与架构速览)
   - [本章要解决什么问题](#本章要解决什么问题)
   - [1.1 控制面与数据面](#11-控制面与数据面)
   - [1.2 100.64.0.0/10：Tailscale 的虚拟网段](#12-100640010tailscale-的虚拟网段)
   - [1.3 路由注入四条件](#13-路由注入四条件)
   - [1.4 路由与 ACL：两层独立机制](#14-路由与-acl两层独立机制)
   - [1.5 多路由器 HA 与最长前缀匹配](#15-多路由器-ha-与最长前缀匹配)
   - [1.6 Docker FORWARD 默认 DROP：埋下伏笔](#16-docker-forward-默认-drop埋下伏笔)
   - [本章小结](#本章小结)
2. [第二章 Docker Compose 部署 Tailscale 容器](#第二章-docker-compose-部署-tailscale-容器)
   - [2.1 fnOS 界面入口](#21-fnos-界面入口)
   - [2.2 推荐版 Compose（privileged，省心）](#22-推荐版-composeprivileged省心)
   - [2.3 最小权限版 Compose（无 privileged）](#23-最小权限版-compose无-privileged)
   - [2.4 关键环境变量](#24-关键环境变量)
   - [2.5 部署侧 TUN busy 预防](#25-部署侧-tun-busy-预防)
   - [2.6 其他注意点](#26-其他注意点)
   - [本章小结](#本章小结-1)
3. [第三章 宿主机内核转发——sysctl 开启 IP forwarding](#第三章-宿主机内核转发sysctl-开启-ip-forwarding)
   - [本章要解决什么问题](#本章要解决什么问题-1)
   - [3.1 写入 sysctl 配置](#31-写入-sysctl-配置)
   - [3.2 加载并验证](#32-加载并验证)
   - [3.3 没开转发的表现](#33-没开转发的表现)
   - [本章小结](#本章小结-2)
4. [第四章 防火墙放行与 NAT——iptables 规则](#第四章-防火墙放行与-natiptables-规则)
   - [4.1 根因回顾：Docker 的 FORWARD DROP](#41-根因回顾docker-的-forward-drop)
   - [4.2 基线修复（用户草稿方案）](#42-基线修复用户草稿方案)
   - [4.3 进阶：DOCKER-USER 链外科手术式放行](#43-进阶docker-user-链外科手术式放行)
   - [4.4 同宿主二次 MASQUERADE（#12407）](#44-同宿主二次-masquerade12407)
   - [4.5 ts-forward 链顺序（#13754）](#45-ts-forward-链顺序13754)
   - [4.6 持久化与 fnOS 防火墙后端（待实机确认）](#46-持久化与-fnos-防火墙后端待实机确认)
   - [本章小结](#本章小结-3)
5. [第五章 控制台批准与客户端配置](#第五章-控制台批准与客户端配置)
   - [5.1 Admin Console 批准子网路由](#51-admin-console-批准子网路由)
   - [5.2 autoApprovers 自动批准（可选）](#52-autoapprovers-自动批准可选)
   - [5.3 客户端开启"接受子网路由"](#53-客户端开启接受子网路由)
   - [5.4 未授权不下发的表现](#54-未授权不下发的表现)
   - [本章小结](#本章小结-4)
6. [第六章 验证方法与排错表（扩充）](#第六章-验证方法与排错表扩充)
   - [6.1 验证命令集](#61-验证命令集)
   - [6.2 深入排查](#62-深入排查)
   - [6.3 排错决策树](#63-排错决策树)
   - [6.4 排错表（扩充）](#64-排错表扩充)
   - [6.5 与既有教程衔接](#65-与既有教程衔接)
   - [本章小结](#本章小结-5)
7. [总结](#总结)

---

## 第一章 为什么需要子网路由器——原理与架构速览

> 通用概念可先看 [[Tailscale使用教程]]。本章建立全局认知，后续所有配置都在兑现本章的某一环条件。

### 本章要解决什么问题

家中设备散落在 `192.168.1.0/24`，打印机、摄像头、IoT 网关大多装不了 Tailscale。子网路由器只在一台设备上跑 Tailscale，把整个内网网段通告进 tailnet，其他设备零安装即可被外网访问。本章讲清链路零件。

### 1.1 控制面与数据面

Tailscale 协调服务器**不在数据路径上**，只负责身份、密钥、下发网络地图（netmap）；真正传数据的是设备间的加密隧道（来源 S10）。

> [!tip] 大白话
> 像房产中介只牵线搭桥，真正交谈的是你和房东。中介不参与聊天、不占带宽。

数据面是用户态 WireGuard（IP 封装进 UDP），用 `magicsock` 单一 socket 复用所有对端流量，先 NAT 穿透（STUN+打洞）直连，失败回退 DERP 中继（TCP 443）兜底（来源 S10）。官方称 92%+ 流量最终直连，瓶颈通常在 NAS 转发能力与上行带宽。

```text
[控制面]  协调服务器 ──(身份/密钥/网络地图)──> 所有节点（不转发数据）
[数据面]  设备A ──WireGuard over UDP──> 设备B（打洞失败→DERP 兜底）
```

### 1.2 100.64.0.0/10：Tailscale 的虚拟网段

节点 IP 取自 RFC 6598 CGNAT 段 `100.64.0.0/10`，不随位置变（来源 S6）。选它三因：不与 `10/8`、`192.168/16` 冲突；本就是运营商级中间 NAT 地址；面向 ISP 不暴露公网（来源 S6）。

> [!tip] 大白话
> 这是划给"运营商内部中转"的保留地。Tailscale 借用当门牌号，绝不会和 `192.168.1.x` 撞号。

### 1.3 路由注入四条件

通告 ≠ 生效。子网路由要出现在客户端，需同时满足（来源 S7）：

1. **通告**：路由器 `--advertise-routes`（或 `TS_ROUTES`）声明"能带路去 `192.168.1.0/24`"。
2. **批准**：管理员在 Admin Console（或 autoApprovers）批准。
3. **下发**：控制面把已批准路由写进客户端网络地图。
4. **接受**：客户端开启 accept-routes（Linux 用 `--accept-routes`）。

关键点：**路由只要"通告且已批准"就会下发**，不会先 ping 探测再安装（来源 S7）。"路由没生效"先查卡在哪一环。

### 1.4 路由与 ACL：两层独立机制

路由（L3）决定"包能不能进隧道"，ACL（PacketFilter）决定"进了隧道能不能通行"，两者独立（来源 S7）：有路由无 ACL → 包进隧道被丢；有 ACL 无路由 → 包永不进隧道。

> [!tip] 大白话
> 路由是"门禁卡"，ACL 是"楼内保安"。有卡进楼，进电梯前保安还查权限。缺一不可。

### 1.5 多路由器 HA 与最长前缀匹配

多台路由器做 HA，**只有通告完全相同前缀的互为故障切换候选**（来源 S1）。系统按最长前缀匹配（LPM）选路，更具体路由离线时不回退到宽松路由（来源 S7）。

> [!warning] 实战提醒
> 同时通告 `192.168.0.0/16` 和 `192.168.1.0/24`，客户端永远优先后者；后者离线不会自动用前者。这个"不回退"特性易造成"有兜底却不通"的假象。

### 1.6 Docker FORWARD 默认 DROP：埋下伏笔

Docker 启动时自动开启 ip_forward，并把 **iptables FORWARD 默认策略设为 DROP**（来源 S8），导致 `tailscale0` → 内网网卡的转发被丢弃。这就是"ping 通第一跳却打不开内网网页"的根因之一（来源 S8, S11）。第 4 章专门修。

### 本章小结

- 控制面只管身份与路由下发，数据面是 WireGuard 直连隧道，DERP 仅兜底（来源 S10）。
- 节点 IP 来自 `100.64.0.0/10`，不与内网冲突（来源 S6）。
- 路由生效需"通告 → 批准 → 下发 → accept-routes"四条件（来源 S7）。
- 路由与 ACL 是两层独立机制（来源 S7）。
- Docker 默认 FORWARD DROP，是"能 ping 通却打不开网页"根因之一（来源 S8）。

下一章开始动手：用 Docker Compose 把容器跑起来，先兑现"通告"。

**参考来源**：S1 Tailscale KB: Subnet routers · S6 Tailscale IP 地址概念 · S7 Route injection 参考 · S8 Docker 数据包过滤与防火墙 · S10 How Tailscale Works。

---

上一章建立了全链路原理：子网路由要生效，需满足"通告 → 批准 → 下发 → 接受"四条件。接下来动手，先用 Docker Compose 把容器跑起来，兑现第一环"通告"。

## 第二章 Docker Compose 部署 Tailscale 容器

> 对应路由注入四条件的**第一环——通告**。给「推荐版」与「最小权限版」两套 Compose，并拆解关键环境变量。Docker/Compose 基础可对照 [[Tailscale使用教程]]。

### 2.1 fnOS 界面入口

fnOS 桌面打开 **Docker → Compose → 新建项目**，粘贴 YAML，填项目名（如 `tailscale-subnet-router`）并部署。

> [!warning] 界面路径以实机为准
> 社区帖路径（来源 S2, S3）可能随 fnOS 版本微调（待实机确认）。核心逻辑不变：新建 Compose 项目 → 粘贴 YAML → 部署。

### 2.2 推荐版 Compose（privileged，省心）

```yaml
# docker-compose.yml（推荐版）
services:
  tailscale:
    image: tailscale/tailscale:stable   # 固定 stable 标签
    container_name: tailscale-subnet-router
    hostname: fnos-subnet-router
    network_mode: host                    # 关键：直接用宿主机网络栈
    privileged: true                      # 省心：完整设备访问权限
    cap_add:
      - NET_ADMIN                         # 建 tun、改路由所需（privileged 下为双保险）
    volumes:
      - /var/lib/tailscale:/var/lib/tailscale   # 状态持久化
      - /dev/net/tun:/dev/net/tun               # 挂载 TUN 设备
    environment:
      - TS_AUTHKEY=tskey-auth-xxxxxxxx      # 生成时必须勾选 Reusable
      - TS_STATE_DIR=/var/lib/tailscale     # 状态目录
      - TS_ROUTES=192.168.1.0/24            # 内网网段，无末尾逗号
      - TS_HOSTNAME=fnos-subnet-router      # 后台显示名，可自定
    restart: unless-stopped                 # 开机自启 + 异常自动拉起
```

> [!note] 为什么用 host 网络
> Docker 对 host 网络不额外创建 iptables 规则（来源 S8），且 tailscaled 需在宿主机网络命名空间建 `tailscale0`、改路由。这是社区共识基线（来源 S2, S3, S0）。

### 2.3 最小权限版 Compose（无 privileged）

社区验证可用的更克制变体（来源 S3）：

```yaml
# docker-compose.yml（最小权限版）
services:
  tailscale:
    image: tailscale/tailscale            # 无 tag：跟随最新
    container_name: tailscale-subnet-router
    hostname: fnos-subnet-router
    network_mode: host
    cap_add:
      - NET_ADMIN                         # 建 tun、改路由、iptables
      - NET_RAW                           # 原始 socket，部分场景建 tun 需要
    volumes:
      - tailscale-state:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    environment:
      - TS_AUTHKEY=tskey-auth-xxxxxxxx
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_ROUTES=192.168.1.0/24
      - TS_HOSTNAME=fnos-subnet-router
    restart: unless-stopped

volumes:
  tailscale-state:                        # 命名卷，路径交给 Docker 管理
```

> [!tip] 两版怎么选
> 像"全套装修"vs"简装"：`privileged` 省心，适合直接照做；最小权限版更安全但排查面更大。**推荐先跑推荐版，再考虑收敛权限**（来源 S2, S3）。

### 2.4 关键环境变量

- **`TS_AUTHKEY`**：Admin Console → Settings → Keys 生成时**必须勾选 Reusable**；否则 single-use 密钥在容器重启后无法再认证 → 反复闪退（来源 S0, S2 回帖）。
- **`TS_STATE_DIR`**：tailscaled 状态目录，配合卷持久化；否则每次重建都重新认证、换 IP。
- **`TS_ROUTES`**：要通告的内网网段，**必须是合法 CIDR**。
- **`TS_HOSTNAME`**：后台显示名，可自定（社区用 fnos，用户草稿用 fons-subnet-router，来源 S2, S0）。

> [!tip] 大白话
> `TS_AUTHKEY` 是**临时工牌**：reusable 长期可进出，single-use 刷一次作废。工牌用完没人补发，门卫不让你进门——容器就闪退了。

> [!warning] TS_ROUTES 最容易踩的坑
> 必须是 **IP/CIDR**。填布尔值 `true`、或末尾多逗号（`192.168.1.0/24,`），都会触发 `netip.ParsePrefix` 解析失败，报错如 `netip.ParsePrefix(""): no '/'`（来源 S12, S0）。**合法示例：`TS_ROUTES=192.168.1.0/24`，无空格、无尾逗号。**

### 2.5 部署侧 TUN busy 预防

宿主若已装 Tailscale（或残留 tailscaled、冗余容器），会占用 `/dev/net/tun`，容器建 `tailscale0` 报 **TUN device busy**（来源 S0）。部署前先查：

```bash
lsof /dev/net/tun      # 看谁占用 tun
pgrep -a tailscaled    # 查宿主机是否已有 tailscaled
```

### 2.6 其他注意点

- **`version` 字段**：老教程的 `version: '3'` 只是过时警告，建议删掉（来源 S3 回帖）。
- **容器重启会换 Tailscale IP**（来源 S3 回帖）：对子网路由器影响不大——客户端走子网路由而非容器 IP；如需长期稳定可禁用该设备 key expiry。

### 本章小结

- 部署入口：fnOS Docker → Compose → 新建项目（来源 S2, S3；界面细节待实机确认）。
- 基线：host 网络 + `/dev/net/tun` + `TS_STATE_DIR` + `TS_ROUTES` + `restart: unless-stopped`（来源 S2, S3, S0）。
- 两变体：推荐版 `privileged`；最小权限版 `NET_ADMIN + NET_RAW`（来源 S2, S3）。
- `TS_AUTHKEY` 必须 reusable；`TS_ROUTES` 必须合法 CIDR、无尾逗号（来源 S0, S2, S12）。
- 部署前 `lsof /dev/net/tun` 排查占用（来源 S0）。

容器起来了、通告发了，但包还出不去——内核默认不允许转发。下一章开转发开关。

**参考来源**：S0 用户草稿 · S2 飞牛论坛 tid=13887 · S3 飞牛论坛 tid=28001 · S8 Docker 数据包过滤与防火墙 · S12 tailscale Issue #9605。

---

容器已通过 Compose 跑起来并通告了子网路由，但包要真正进入内网，还依赖宿主机内核允许转发。这一章开启并验证内核转发开关。

## 第三章 宿主机内核转发——sysctl 开启 IP forwarding

> 子网路由器的本职是"把包从 tailnet 转发进内网"，这一步由宿主机内核完成。本章开启并验证内核转发。

### 本章要解决什么问题

容器起来了、Tailscale 认证了，但外网 ping 内网设备仍不通。高频原因：**宿主机内核默认不允许转发 IP 包**。Linux 开关 `net.ipv4.ip_forward` 默认是 0，而子网路由器正是靠它把从 `tailscale0` 进来的包转到内网网卡（来源 S1, S11）。

> [!tip] 大白话
> 内核转发像大楼的**货运电梯**，默认锁着。隧道把包裹送到大楼门口（tailscale0），电梯不开，包裹到不了内网。sysctl 就是开电梯的钥匙。

### 3.1 写入 sysctl 配置

持久化写入，重启不丢。新建 `/etc/sysctl.d/99-tailscale.conf`：

```ini
# /etc/sysctl.d/99-tailscale.conf
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

- `net.ipv4.ip_forward = 1`：必开，IPv4 转发总开关。
- `net.ipv6.conf.all.forwarding = 1`：可选，仅当要通告 IPv6 子网。
- 无 `/etc/sysctl.d/` 时，同样内容写进 `/etc/sysctl.conf`（来源 S1, S11）。

### 3.2 加载并验证

```bash
sysctl -p /etc/sysctl.d/99-tailscale.conf   # 立即加载
sysctl net.ipv4.ip_forward                  # 期望：net.ipv4.ip_forward = 1
cat /proc/sys/net/ipv4/ip_forward           # 期望：1
```

`/etc/sysctl.d/` 配置开机自动加载，属持久化设置。

### 3.3 没开转发的表现

- `tailscale up` 提示子网路由/出口节点功能**要求开启 IP forwarding**（来源 S11）。
- 数据面：客户端能 ping 通 100.x 网关（隧道通），但包到路由器后被拒转发，打不开内网任何设备。

> [!tip] 大白话
> "能 ping 通 100.x 网关"只说明隧道修到了楼下，不代表电梯（转发）开了。转发开没开，直接看 `sysctl net.ipv4.ip_forward` 是不是 1，别靠猜。

> [!warning] 症状重叠提醒
> "转发未开"和"FORWARD DROP"（第 4 章）症状几乎相同：首跳通、内网不通。排错先确认 `sysctl net.ipv4.ip_forward = 1`，再查 FORWARD 链，两步都要做。

### 本章小结

- 子网路由器必须开内核 IP 转发（来源 S1, S11）。
- 持久化写法：`/etc/sysctl.d/99-tailscale.conf` 写 `net.ipv4.ip_forward = 1`。
- `sysctl -p` 加载，`sysctl net.ipv4.ip_forward` 验证。
- 未开转发症状与 FORWARD DROP 重叠，排错两者都查。

转发开关开了，但 Docker 的 FORWARD 链还在"锁门"。下一章处理防火墙放行与 NAT。

**参考来源**：S0 用户草稿 · S1 Tailscale KB: Subnet routers · S11 Tailscale IP forwarding 排错页。

---

转发开关已打开，但 Docker 把 FORWARD 链默认策略设为 DROP，包仍可能被丢弃。这一章处理防火墙放行与回程 NAT。

## 第四章 防火墙放行与 NAT——iptables 规则

> 第 3 章转发开关负责"内核允许转发"，本章负责"防火墙放行 + 回程路径"。同时交代两个易混淆 issue：#12407 二次 NAT 与 #13754 链顺序。

### 4.1 根因回顾：Docker 的 FORWARD DROP

Docker 启动时自动开启 ip_forward，并把 **FORWARD 链默认策略设为 DROP**（来源 S8）。虽用 host 网络（Docker 不为 host 网络建规则，来源 S8），但 FORWARD 默认策略被改 DROP 仍生效，`tailscale0` → 内网网卡的转发被丢。

Docker 提供 `ip-forward-no-drop: true`（daemon.json）阻止改默认策略，但 fnOS 定制版未必暴露入口（待实机确认）。

### 4.2 基线修复（用户草稿方案）

用户草稿（来源 S0）的两条命令是社区流传最广的基线修复：

```bash
iptables -P FORWARD ACCEPT                                        # 放行 FORWARD（宽放）
iptables -t nat -A POSTROUTING -s 100.64.0.0/10 -j MASQUERADE     # 回程 NAT
```

> [!tip] 大白话
> `-P FORWARD ACCEPT` 给货运电梯**解锁**；`MASQUERADE` 是**快递代发**——把内网设备真实地址藏起来，统一用路由器自己的地址回信，内网设备无需知道 100.x 也能收到回包。

**但这条 MASQUERADE 是"兜底"**：Tailscale 自身会用 `ts-postrouting` 做 SNAT，手动再加一条属双保险，极少数会叠加成二次 NAT（见 4.4）。

> [!warning] 宽放的安全代价
> `-P FORWARD ACCEPT` 是全局宽放。若 NAS 还跑着需隔离的容器，建议改用 4.3 的 DOCKER-USER 方案（来源 S8）。

### 4.3 进阶：DOCKER-USER 链外科手术式放行

官方推荐把自定义规则放进 **DOCKER-USER** 链而非全局改默认策略，因为 Docker 管理 FORWARD 但保留 DOCKER-USER 给用户放自定义规则（来源 S8）。

```bash
iptables -I DOCKER-USER -i tailscale0 -o eth0 -j ACCEPT   # 入向：tailscale0 → 内网（eth0 换成实际网卡）
iptables -I DOCKER-USER -i eth0 -o tailscale0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT  # 回向
```

> [!warning] 网卡名要换
> `eth0` 是示例，须换成 fnOS 实际内网网卡名（`ip addr` 查）。DOCKER-USER 只放行指定方向，比全局 ACCEPT 更收敛（来源 S8）。

### 4.4 同宿主二次 MASQUERADE（#12407）

**症状**：外网能 ping 通内网设备，但访问**与 Tailscale 同宿主机**的服务（如 NAS 本机 Web）时 HTTP 超时。

**根因**：目标与 Tailscale 同机时，包带 mark `0x40000` 重新进入 `ts-forward → ts-postrouting` 被二次伪装，内核丢弃（来源 S13）。手动加的 `MASQUERADE` 可能与 `ts-postrouting` 叠加放大问题。

> [!tip] 大白话
> 快递被**贴了两张回程单**：Tailscale 贴一张（ts-postrouting），你又手动贴一张（MASQUERADE），快递员不知按哪张送干脆不送——ping 通（包裹到门口）但服务打不开（回程地址乱了）。

官方修法（来源 S13）：

```bash
iptables -t raw -A PREROUTING -m mark --mark 0x40000/0xff0000 -j MARK --set-mark 0   # 修法一：清 mark
iptables -I FORWARD -m mark ! --mark 0x40000/0xff0000 -j ts-forward                  # 修法二：mark 包跳过 ts-forward
```

> [!note] 判断是否命中 #12407
> 先临时移除 4.2 的手动 `MASQUERADE`，若同宿主访问立即恢复即是二次 NAT 叠加；仍超时再试修法。**#12407 与 #13754 根因不同，症状都是"ping 通但服务异常"，先区分**（来源 S9, S13）。

### 4.5 ts-forward 链顺序（#13754）

**症状**：客户端能建隧道，但子网流量时通时断，或重启后必现故障。

**根因**：Tailscale 与 Docker 同机时，`ts-forward` 须排在 FORWARD 链中 **Docker 规则之前**，否则 Docker 的 DROP 先命中。先起容器再 `tailscale up` 可规避大部分顺序问题（来源 S9）。

**运维修复**：`ExecStartPost` 脚本把 `ts-input`/`ts-forward` 移到链尾，核心是"确认存在 → 删除 → 追加"（来源 S9）：

```bash
iptables -C FORWARD -j ts-forward && iptables -D FORWARD -j ts-forward   # 先确认再删
iptables -A FORWARD -j ts-forward                                         # 追加到链尾
```

### 4.6 持久化与 fnOS 防火墙后端（待实机确认）

`iptables` 命令默认只生效到下次重启。fnOS 防火墙后端（iptables 还是 nftables）及重启后规则是否保留，**尚未实机确认**。建议开机自动加载：

```bash
iptables-save > /etc/tailscale-iptables.rules     # 保存
iptables-restore < /etc/tailscale-iptables.rules  # 开机脚本恢复
```

> [!warning] nftables 后端
> 若 fnOS 用 nftables 后端，`iptables` 会被透明翻译，但 `iptables-save/restore` 持久化可能不适用（待实机确认后更新本章）。

### 本章小结

- 根因：Docker 把 FORWARD 默认策略设为 DROP（来源 S8）。
- 基线修复：`-P FORWARD ACCEPT` + `POSTROUTING MASQUERADE 100.64.0.0/10`（来源 S0）。
- 更收敛方案：DOCKER-USER 链放行（来源 S8）。
- #12407 同宿主二次 NAT：ping 通但 HTTP 超时（来源 S13）。
- #13754 链顺序：`ts-forward` 须在 Docker 规则之前（来源 S9）。
- 持久化与 fnOS 防火墙后端待实机确认。

防火墙放行、NAT 兜底完成，但路由还要在控制台批准、客户端还要开接受。下一章处理这两环。

**参考来源**：S0 用户草稿 · S8 Docker 数据包过滤与防火墙 · S9 tailscale Issue #13754 · S13 tailscale Issue #12407。

---

转发、放行、NAT 都就绪后，还差"批准"与"接受"两环，路由才会真正下发到客户端。这一章补齐控制台批准与客户端配置。

## 第五章 控制台批准与客户端配置

> 补齐路由注入四条件的**第二环（批准）与第四环（客户端接受）**。容器通告了、转发开了、防火墙放行了，但没批准、没开接受，路由照样不生效。控制台与 tailnet 管理可对照 [[Tailscale使用教程]]。

### 5.1 Admin Console 批准子网路由

路由通告后必须由管理员批准才会下发（来源 S1, S3）：

1. 打开 Admin Console（login.tailscale.com）→ 进入 **Machines**。
2. 找到子网路由器设备，在 **Subnets** 区点击 **Edit route settings**。
3. 勾选要通告的网段（如 `192.168.1.0/24`）→ 点击 **Save**。

> [!tip] 大白话
> 容器通告路由只是**自荐**："我能带路！"。管理员点批准，才是**正式聘用**。没批准之前，控制面不会把这条路写进其他设备的网络地图（来源 S7）。

### 5.2 autoApprovers 自动批准（可选）

路由器频繁新增时，可在 Access Controls（ACL）策略里配 `autoApprovers`，匹配条件的路由自动批准（来源 S1, S3）：

```jsonc
// ACL 策略片段（示意）：自动批准指定用户通告的 192.168.x 网段
"autoApprovers": {
  "routes": {
    "192.168.0.0/16": ["youruser@example.com"]
  }
}
```

### 5.3 客户端开启"接受子网路由"

路由批准下发后，**客户端还得同意接受**。各平台默认不同（来源 S1, S7）：

| 平台 | 是否需要手动开启 |
|------|------------------|
| Android / iOS / macOS / tvOS / Windows | 默认接受 |
| Linux | 需显式开启 accept-routes |

```bash
# Linux 客户端
tailscale set --accept-routes=true
```

> [!note] 为什么 Linux 默认不接受
> 出于安全考虑，Linux 客户端默认不把下发的路由写进系统路由表，须显式声明 `--accept-routes`（来源 S1, S7）。图形客户端可在设置里确认 **Use Tailscale subnets** 开关开启。

> [!tip] 大白话
> 移动端默认"来者不拒"，Linux 却要你点头——`--accept-routes` 就是那句"我同意装这条路由"。没点这个头，控制面下发的路由在 Linux 上就是一张没人签收的快递单。

### 5.4 未授权不下发的表现

路由未批准时：**路由器侧** `tailscale status` 能看到自己在通告；**客户端侧**路由完全不出现在网络地图——`ip route` 查不到，`tailscale status` 也没有 `192.168.1.0/24`（来源 S7）。

> [!warning] 别在"没批准"上白耗时间
> "客户端看不到路由"优先怀疑批准环节而非网络问题。用 `tailscale status --json` 确认路由是否存在；不存在就去后台查批准状态。

### 本章小结

- 批准路径：Admin Console → Machines → Edit route settings → 勾选网段 → Save（来源 S1, S3）。
- autoApprovers 可自动批准（来源 S1, S3）。
- 移动/桌面端默认接受；Linux 需 `tailscale set --accept-routes=true`（来源 S1, S7）。
- "未批准不下发"是客户端看不到路由的常见原因（来源 S7）。

四环全通，接下来是验证和排错。最后一章给验证命令集与扩充版排错表。

**参考来源**：S1 Tailscale KB: Subnet routers · S3 飞牛论坛 tid=28001 · S7 Route injection 参考。

---

至此"通告 → 批准 → 下发 → 接受"四条件全部兑现。最后一章给出由浅入深的验证命令集与扩充版排错表，帮你确认并定位问题。

## 第六章 验证方法与排错表（扩充）

> 前半给由浅入深的验证命令，后半是从用户实战草稿（来源 S0）扩充的排错表与决策树。通用操作可对照 [[Tailscale使用教程]]。

### 6.1 验证命令集

先在**路由器机器**确认隧道与通告状态：

```bash
tailscale status              # 本机地址、对端、通告的路由
tailscale status --json       # 结构化输出，可 grep 路由与 peer 状态
```

在**远端客户端**逐层验证：

```bash
tailscale ping 100.x.x.x      # 1) 隧道层：走隧道，不受 ICMP 策略影响
ping 192.168.1.1              # 2) 路由层：ping 子网网关
nc -vz 192.168.1.50 22        # 3) 应用层：测内网某设备端口
tracert 192.168.1.50          # 4) 路径层：Windows tracert / Linux traceroute
```

**从网卡观测**（路由器上）：

```bash
ip addr show tailscale0       # 确认 tailscale0 存在且有 100.x 地址
ip route                      # 确认子网路由/回程路由已写入
```

> [!note] 首跳判定法
> 远端 `tracert` 内网设备，**第一跳就是 100.x** 说明包已进隧道、路由链路通；第一跳是公网/家宽网关，说明路由没进系统路由表，回头查 5.3 的 accept-routes 和 5.1 的批准。

> [!tip] 大白话
> "tracert 第一跳是不是 100.x"是最好用的探针：是 = 路由链路没问题，问题在后面的转发/防火墙；不是 = 路由根本没下发。一句话就能把排查范围砍半。

### 6.2 深入排查

验证不够时，用 debug 命令扒开链路内部（来源 S7）：

```bash
tailscale debug netmap        # 网络地图：路由是否下发、ACL(PacketFilter) 是否放行
tailscale debug prefs         # 偏好：RouteAll 是否 true；false 说明 accept-routes 未开
ip route                      # 本地更具体路由可能抢占 Tailscale 路由（LPM，见第 1 章）
```

### 6.3 排错决策树

```text
容器起不来？
├─ 反复闪退 ──────────────→ TS_AUTHKEY 用了 single-use？→ 换 reusable
│                            TS_ROUTES 解析报错？→ 6.4 表第 1/2 行
└─ 报 TUN device busy ─────→ /dev/net/tun 被占用 → lsof 排查

tailscale 起来了，但客户端用不了？
├─ 客户端看不到子网路由 ──→ 后台批准了吗？→ 5.1；Linux 开 accept-routes？→ 5.3
│                            ip route 有更具体路由抢占？→ 6.4 第 6 行
├─ 首跳通、内网打不开 ────→ 转发开关？→ 第 3 章；FORWARD 放行？→ 第 4 章
│                            ts-forward 链顺序？→ 6.4 第 9 行
└─ ping 通但 HTTP 超时 ───→ 目标是宿主机本机？→ 二次 MASQUERADE #12407
                            防火墙（ufw/firewalld）拦截？→ 6.4 第 10 行
```

> [!tip] 大白话
> 决策树像**修水管先看哪层漏水**：报错（容器层）→ 路由有没有下发（路由层）→ 包有没有被放行（防火墙层）。按症状逐层剥，别乱试命令。

### 6.4 排错表（扩充）

| # | 症状 | 可能根因 | 定位命令 | 修复 |
|---|------|----------|----------|------|
| 1 | 容器报 `netip.ParsePrefix(""): no '/'` | `TS_ROUTES` **末尾逗号**（用户实战坑，来源 S0） | `docker logs` 看报错 | 去掉尾逗号 |
| 2 | 同上，或 `ParsePrefix("true")` | `TS_ROUTES` 填**布尔值/非 CIDR**（来源 S12） | 同上 | 填合法 CIDR |
| 3 | tailscaled 报 **TUN device busy** | 宿主已有 Tailscale/残留进程/冗余容器占用 tun（来源 S0） | `lsof /dev/net/tun` | 停宿主服务或删冗余容器 |
| 4 | 客户端看不到子网路由 | **路由未批准**，控制面不下发（来源 S7） | 客户端 `tailscale status --json` | Admin Console 批准，见 5.1 |
| 5 | 路由下发但客户端不安装 | Linux 未开 accept-routes（来源 S1, S7） | `tailscale debug prefs` 看 RouteAll=false | `tailscale set --accept-routes=true` |
| 6 | 路由下发但走不通 | **路由冲突**：更具体路由按 LPM 抢占或前缀重叠（来源 S7） | `ip route` 对比前缀长度 | 调整通告前缀，注意 LPM 不回退 |
| 7 | tracert 首跳通、内网网页打不开（用户实战坑，来源 S0） | **转发未开**（第 3 章）/ **FORWARD DROP**（第 4 章）/ 回程 NAT 缺失 / 链顺序（来源 S8, S11, S9） | `sysctl net.ipv4.ip_forward`；`iptables -L FORWARD -n` | 开转发 → 放行 FORWARD → 补 MASQUERADE → 调链序 |
| 8 | ping 通但 HTTP 超时，目标是**宿主机本机** | 同宿主**二次 MASQUERADE**（#12407，mark 0x40000）（来源 S13） | 临时移除手动 MASQUERADE 观察 | raw 清 mark 或让 mark 包跳过 ts-forward，见 4.4 |
| 9 | 重启后子网流量时通时断 | **ts-forward 链顺序**在 Docker 规则之后（#13754）（来源 S9） | `iptables -L FORWARD -n --line-numbers` | 先起容器再 `tailscale up` 或移到链尾 |
| 10 | 内网能通但被防火墙拦截 | **宿主机防火墙**（ufw/firewalld）默认拒转发（来源 S1） | `systemctl status firewalld/ufw` | 放行 FORWARD/MASQUERADE（firewalld 常需 `--add-masquerade`） |

> [!note] 两行易混淆的坑
> 第 8 行（#12407）与第 9 行（#13754）**根因不同**：前者是二次 NAT 被内核丢弃，后者是 FORWARD 链规则顺序错误；但都表现为"能 ping 通、服务异常"。先看目标是否在宿主机、再看链顺序（来源 S9, S13）。

### 6.5 与既有教程衔接

本章覆盖"子网路由器"专项；Tailscale 的登录、tailnet、ACL 编写、DERP 自建等通用概念在 [[Tailscale使用教程]] 系统讲过。遇到通用问题先回那边查，再对本章排错表。

> [!note] 长期稳定性建议
> 容器重启会换 Tailscale IP（来源 S3 回帖），建议在控制台为该设备**禁用 key expiry**；多台路由器做 HA 时只让完全相同前缀互为故障切换候选（来源 S1）。

### 本章小结

- 验证由浅入深：`tailscale status` → `tailscale ping` → `ping` 子网网关 → `nc` → `tracert` 看首跳（来源 S0, S1）。
- 深入排查：`debug netmap` 看路由下发与 ACL、`debug prefs` 看 RouteAll、`ip route` 看路由冲突（来源 S7）。
- 决策树：容器层 → 路由层 → 防火墙层，按症状逐层定位。
- 排错表 10 行：覆盖用户草稿三坑 + 路由未授权、路由冲突、防火墙、二次 NAT（#12407）、链顺序（#13754）（来源 S0, S7, S8, S9, S11, S12, S13）。
- #12407 与 #13754 都表现为"ping 通但服务异常"，根因不同（来源 S9, S13）。

六章全部完成：原理（1）→ 部署（2）→ 转发（3）→ 防火墙与 NAT（4）→ 批准与客户端（5）→ 验证与排错（6）。

**参考来源**：S0 用户草稿 · S1 Tailscale KB · S7 Route injection · S8 Docker 防火墙 · S9 Issue #13754 · S11 IP forwarding 排错页 · S12 Issue #9605 · S13 Issue #12407。

---

## 总结

从原理到落地，本教程完整走通了在 fnOS 上用 Docker Compose 部署 Tailscale 子网路由器（Subnet Router）的全流程，六个环节环环相扣：

1. **原理（第 1 章）**：Tailscale 控制面/数据面分离，节点 IP 落在 `100.64.0.0/10`；子网路由生效需满足"通告 → 批准 → 下发 → 接受"四条件，且路由（L3）与 ACL 是两层独立机制。
2. **部署（第 2 章）**：以 host 网络 + `TS_STATE_DIR` + `TS_ROUTES` 为基线，用 Compose 把容器跑起来；`TS_AUTHKEY` 必须 reusable，`TS_ROUTES` 必须是合法 CIDR 且无尾逗号。
3. **转发（第 3 章）**：在宿主机开启 `net.ipv4.ip_forward`，这是包从 `tailscale0` 进入内网的前提。
4. **防火墙与 NAT（第 4 章）**：Docker 把 FORWARD 默认策略设为 DROP，是"首跳通却打不开内网"的根因；用 `-P FORWARD ACCEPT` + MASQUERADE 基线修复，或改用更收敛的 DOCKER-USER 方案，并留意 #12407 二次 NAT 与 #13754 链顺序。
5. **批准与客户端（第 5 章）**：管理员在 Admin Console 批准子网路由，Linux 客户端需显式 `--accept-routes`。
6. **验证与排错（第 6 章）**：用 `tailscale status → tailscale ping → ping 子网网关 → nc → tracert 首跳` 逐层验证，按决策树把排查范围砍半。

贯穿全篇的排错心法：

- **"路由没生效"先定位卡在哪一环**——没通告、没批准、没下发，还是没接受；
- **"首跳通但打不开内网"**——优先查内核转发（第 3 章）与 FORWARD 链（第 4 章）；
- **"ping 通但 HTTP 超时"**——区分 #12407 二次 NAT 与 #13754 链顺序，先看目标是否在宿主机、再看链顺序。

通用 Tailscale 概念（登录、tailnet、ACL 编写、DERP 自建等）可回查 [[Tailscale使用教程]]。
