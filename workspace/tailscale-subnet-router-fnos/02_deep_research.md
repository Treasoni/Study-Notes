# fnOS Docker 部署 Tailscale 子网路由器 - P2 深度素材

> 运行：tailscale-subnet-router-fnos · 阶段 P2 深度收集 · 2026-08-28
> 范围：A. 全部深挖（全流程 + 原理 + 排错三视角）。已精读 11 个源（官方 5 + 一手 issue 4 + 官方社区 2），补充用户草稿作为实践源（S0）。

## 一、来源表

| ID | 层级 | 来源 | 抓取字数 | 用途 |
|----|------|------|----------|------|
| S0 | primary（用户实践） | 用户草稿五部分（Compose/sysctl/iptables/控制台与客户端/排错表） | — | 核心实战基线 |
| S1 | official | Tailscale KB: Subnet routers（tailscale.com/kb/1019/subnets） | 24,732 | 部署标准步骤、SNAT、HA、重叠路由 |
| S2 | primary | 飞牛论坛 tid=13887 Docker Compose 部署 Tailscale | 5,482 | fnOS Compose 实操（stable/privileged/卷） |
| S3 | primary | 飞牛论坛 tid=28001 Tailscale 内网穿透教程 | 11,601 | fnOS Compose 实操（无 privileged 变体）、控制台批准、坑 |
| S6 | official | Tailscale IP 地址概念（100.64.0.0/10 CGNAT） | 2,546 | 原理：CGNAT 三原因 |
| S7 | official | Tailscale Route injection 参考 | 9,230 | 原理：路由注入四条件、路由 vs ACL |
| S8 | official | Docker 数据包过滤与防火墙 | 8,215 | 原理+排错：FORWARD DROP、DOCKER-USER、ip-forward-no-drop |
| S9 | primary | tailscale Issue #13754 FORWARD 链顺序 | 8,352 | 排错：ts-forward 顺序、启动顺序依赖 |
| S10 | community | How Tailscale Works (god.ad) | 42,381 | 原理：控制/数据面分离、WireGuard、DERP |
| S11 | official | Tailscale IP forwarding 排错页 | 868 | 排错入口：ip_forward 未开 |
| S12 | primary | tailscale Issue #9605 TS_ROUTES 文档错误 | 8,640 | 排错：TS_ROUTES 解析失败（布尔值/非 CIDR） |
| S13 | primary | tailscale Issue #12407 同宿主二次 MASQUERADE | 7,326 | 排错：ping 通但 HTTP 超时、mark 0x40000 |

层级分布：official 5 · primary 4 · 官方社区 2 · community 1 · 用户实践 1。检索日期统一 2026-08-28。

## 二、主张 ↔ 来源映射

### A. 部署全流程

| 主张 | 来源 |
|------|------|
| 子网路由器 6 步：安装客户端→以子网路由器连接→后台批准→访问规则→验证→其他设备使用 | S1 |
| Linux 作子网路由器需 ①开启 IP forwarding ②通告子网路由（`tailscale set --advertise-routes=`） | S1 |
| sysctl 开启转发：写入 `/etc/sysctl.d/99-tailscale.conf` 后 `sysctl -p`（无 sysctl.d 时用 /etc/sysctl.conf） | S1, S11, S0 |
| 通告前应确认防火墙默认拒绝转发（ufw/firewalld 默认如此），firewalld 可能需 `--add-masquerade`（issue #3416） | S1 |
| Compose 基线：`tailscale/tailscale` 镜像 + `network_mode: host` + `TS_STATE_DIR=/var/lib/tailscale` + `TS_ROUTES=<内网段>` + `/dev/net/tun` 挂载 + `restart: unless-stopped` | S2, S3, S0 |
| Compose 变体一（S2/tid=13887）：`image: tailscale/tailscale:stable` + `privileged: true` + `cap_add: net_admin` + 命名卷绝对路径 | S2 |
| Compose 变体二（S3/tid=28001）：`image: tailscale/tailscale`（无 tag）+ 无 privileged + `cap_add: NET_ADMIN, NET_RAW` + 相对路径命名卷 | S3 |
| 用户草稿用 `TS_AUTHKEY`（生成时须开 reusable，否则 single-use 密钥用完导致容器重启闪退） | S0, S2(回帖) |
| `TS_HOSTNAME` 控制后台显示名（S2 用 fnos，S0 用 fons-subnet-router） | S0, S2 |
| 后台批准子网路由：Machines → 设备 Subnets 区 → Edit route settings → 勾选网段 → Save；用 autoApprovers 可自动批准 | S1, S3 |
| 客户端自动获取：Android/iOS/macOS/tvOS/Windows 默认接受路由；Linux 需 `tailscale set --accept-routes` | S1, S7 |
| 容器重启会换 Tailscale IP；可用禁用 key expiry + 子路由稳定访问内网 IP（社区争论，见冲突节） | S3(回帖) |
| Docker 部署想开 exit node 比较麻烦 | S2(回帖) |

### B. 原理与架构

| 主张 | 来源 |
|------|------|
| Tailscale IP 取自 RFC 6598 CGNAT 段 100.64.0.0/10（100.64.0.0–100.127.255.255），不随位置变化 | S6, S10 |
| 选 CGNAT 三原因：①不与 10/8、192.168/16 等常用私有段冲突 ②用于需中间 NAT 的流量 ③面向 ISP 不暴露公网 | S6 |
| 子网路由器是 tailnet 内通告路由的网关，默认对转发流量启用 SNAT（`--snat-subnet-routes=false` 可关，仅 Linux） | S1, S10 |
| 关闭 SNAT 后内网设备需手动加回程路由（100.64.0.0/10 → 网关局域网 IP），否则无法回包 | S1 |
| 路由注入四条件：①路由器 `--advertise-routes` 通告 ②管理员批准（admin console 或 autoApprovers）③控制面下发进网络地图 ④客户端 accept-routes | S7 |
| 路由（L3，能否进隧道）与 ACL/grants（包过滤，能否通行）是两层独立机制，流量成功需两者同时满足 | S7 |
| 有路由无 ACL：包进隧道被过滤器丢弃；有 ACL 无路由：包永不会进隧道 | S7 |
| 路由出现＝客户端收到"通告且已批准"的路由，不会先 ping 探测再安装 | S7 |
| 多路由器 HA：仅精确同前缀互为故障切换候选；OS 按最长前缀匹配（LPM）选路，更具体路由离线不回退到宽松路由 | S1, S7 |
| Docker 会为 bridge 网络创建 iptables 规则；对 host/ipvlan/macvlan 不创建规则 | S8 |
| Docker 启动时自动开启 ip_forward，并把 FORWARD 默认策略设为 DROP（`ip-forward-no-drop: true` 可阻止） | S8 |
| 控制面/数据面分离：协调服务器只管身份/密钥/网络地图，不在数据路径；数据面是 WireGuard 隧道 | S10 |
| 数据面：用户态 WireGuard L3 封装 UDP；NAT 穿透（STUN+打洞）、DERP 中继回退（TCP 443）、92%+ 最终直连（作者主张） | S10 |
| magicsock：单一 UDP socket 复用所有对端流量，动态切换直连/中继 | S10 |

### C. 验证与排错深化

| 主张 | 来源 |
|------|------|
| 排错入口：子网路由/出口节点要求开启 IP forwarding，未开会报错 | S11 |
| 路由不出现排查：①确认路由器在通告（admin console / `tailscale status --json`）②确认已批准 ③Linux `tailscale debug prefs` 查 RouteAll，false 则 `--accept-routes` ④`ip route` 查本地更具体路由占优 | S7 |
| 流量被阻排查：`tailscale debug netmap` 看 PacketFilter（ACL 是否放行）、路由器自身能否达目标、两端防火墙 | S7 |
| Docker FORWARD DROP 是「tracert 第一跳通但打不开内网网页」的根因之一；解法：放行 FORWARD + 回程 NAT | S8, S0, S11 |
| 用户草稿 iptables 修复：`iptables -P FORWARD ACCEPT` + `iptables -t nat -A POSTROUTING -s 100.64.0.0/10 -j MASQUERADE` | S0 |
| 更外科手术式替代：把放行规则加进 DOCKER-USER 链（官方推荐自定义位置），而非全局 `-P FORWARD ACCEPT` | S8 |
| 同宿主二次 MASQUERADE（S13）：目标与 Tailscale 同宿主机时，包带 mark 0x40000 重入 ts-forward→ts-postrouting 二次 NAT 被内核丢弃 → ping 通但 HTTP 超时 | S13 |
| S13 解法一：`iptables -t raw -A PREROUTING -m mark --mark 0x40000/0xff0000 -j MARK --set-mark 0`；解法二：`FORWARD` 首条 `-m mark ! --mark 0x40000/0xff0000 -j ts-forward`（报告者验证有效） | S13 |
| TS_ROUTES 解析失败：官方 issue #9605 记录填布尔值 `true` → `netip.ParsePrefix` 报错；正确值须为 IP/CIDR | S12 |
| 用户草稿场景：TS_ROUTES 末尾逗号 → `netip.ParsePrefix(""): no '/'`，去掉末尾逗号即可 | S0（与 S12 同根：非合法 CIDR 触发 ParsePrefix） |
| TUN device busy：宿主机已装 Tailscale 时容器内 tailscaled 建 tailscale0 冲突；`lsof /dev/net/tun` 找进程/杀进程、换 tun 名，或删除冗余容器 | S0, S14（hassio #392，社区） |
| ts-forward 链顺序（S9）：Tailscale 与 Docker 同机，`ts-forward` 须排在 FORWARD 链 Docker 规则之前；先起容器再 `tailscale up` 可规避 | S9 |
| S9 运维修复：`ExecStartPost` 脚本把 ts-input/ts-forward 移到链尾（`move_rule` 循环：iptables -C 确认→-D 删→-A 追加） | S9 |
| 注意：#12407 与 #13754 根因不同（前者二次 NAT 丢弃、后者链顺序），但都表现为"能 ping 通但服务访问异常"，需区分 | S9, S13 |

## 三、冲突与注意点

1. **Compose 配置变体冲突**：S2 用 `privileged: true` + 仅 `net_admin`；S3 用 `NET_ADMIN+NET_RAW` + 无 privileged。两者社区均验证可用；官方推荐至少 NET_ADMIN + /dev/net/tun，privileged 更省心。教程建议给出「推荐 + 最小权限」两版。
2. **TS_ROUTES 报错归因**：官方 issue #9605 记录的是布尔值 `true` 触发 ParsePrefix；用户草稿的「末尾逗号」是同类根因（非合法 CIDR → `netip.ParsePrefix("")`）的实践变体，官方 issue 未直接记录。写作时标注为「同类解析错误 + 用户实战案例」。
3. **手动 MASQUERADE 与 ts-postrouting 的关系**：Tailscale 自身会用 ts-postrouting 做 SNAT；用户草稿再手动加 `MASQUERADE 100.64.0.0/10` 属于兜底。若出现「ping 通但 HTTP 超时」且目标在宿主机，需按 #12407 排查是否二次 MASQUERADE——两条规则可能叠加。
4. **TS_ROUTES 副作用争论（S3 回帖）**：有用户称设子网路由导致内网互访绕行、NAS 关机后内网 ping 不通；另一用户反驳称只有启用 exit node 才强制走 Tailscale。结论：正常子网路由不影响内网直连，除非客户端开了 exit node 或接受全局路由。
5. **Compose `version` 属性过时警告**：S3 回帖提示仅警告可忽略，建议移除。

## 四、实践指引（合并为教程骨架）

1. **Compose 推荐版**：host 网络 + `privileged: true` + `TS_AUTHKEY`（reusable）+ `TS_STATE_DIR` + `TS_ROUTES=<网段，无尾逗号>` + `TS_HOSTNAME` + `/dev/net/tun` + `restart: unless-stopped`；最小权限变体用 `NET_ADMIN+NET_RAW`。
2. **宿主机转发**：写入 `/etc/sysctl.d/99-tailscale.conf`（ipv4/ipv6 forwarding）→ `sysctl -p` 验证返回 `net.ipv4.ip_forward = 1`。
3. **防火墙放行**：基线 `iptables -P FORWARD ACCEPT` + `MASQUERADE 100.64.0.0/10`（用户草稿）；进阶推荐 DOCKER-USER 链外科手术式放行；fnOS 若用 nftables 后端需对应调整。
4. **后台批准**：Admin Console → 设备 → Edit route settings → 勾选网段 → Save（未批准不下发）。
5. **客户端**：移动/桌面端勾 Use Tailscale subnets；Linux 加 `--accept-routes`。
6. **验证**：`tailscale status` 看路由；`tailscale ping <内网IP>` 或 ping 子网网关；远端设备 ping 内网设备；`tracert` 看第一跳是否 tailscale0/100.x。
7. **排错决策树**：报错信息 → 末尾逗号/非 CIDR（TS_ROUTES）；TUN busy → 冗余容器/残留网卡；ping 通但网页超时 → FORWARD 拦截、回程路由、同宿主二次 MASQUERADE、ts-forward 顺序。

## 五、未决问题

1. **fnOS 防火墙后端**：fnOS 的 Docker 是否用 nftables 后端、`iptables -P FORWARD ACCEPT` 在重启/防火墙重置后是否持久化，待用户实机确认。
2. **手动 MASQUERADE 与 ts-postrouting 是否冲突**：#12407 提示可能二次 NAT；教程需给出「先不加手动规则，出现问题再按决策树处理」或「保留但遇到同宿主超时则移除」的指引。
3. **fnOS Docker UI 精确路径**（Docker → Compose 新建项目界面）以用户草稿为准，社区帖与界面可能随版本变化。
4. **ip-forward-no-drop 在 fnOS 是否可用**：Docker 官方机制，fnOS 定制版未必暴露 daemon.json 配置入口。

## 六、下游交接（给 outline-generator / chapter-writer）

- **素材重心**：S0 用户草稿为实战主线；S1 官方步骤为权威基准；S7 原理四条件；S8 Docker FORWARD 机制；S12/S13 两条关键 issue 对应排错核心。
- **建议章节骨架**（参考，P3 可调整）：
  1. 背景与原理（为什么需要子网路由器；CGNAT/overlay/路由注入四条件）
  2. Docker Compose 部署（推荐版 + 最小权限版 + fnOS 界面操作）
  3. 宿主机内核转发与防火墙放行（sysctl + iptables/DOCKER-USER + 持久化注意）
  4. 控制台批准与客户端配置（批准路由、Use Tailscale subnets、--accept-routes）
  5. 验证方法与排错表（tailscale 验证命令 + 排错决策树 + 用户四坑扩充）
- **引用风格**：正文双链 [[内网穿透/Tailscale使用教程.md]]；外部引用保留 URL 与来源层级标注。
