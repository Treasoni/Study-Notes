# HAOS Tailscale 内网穿透与子路由 - 深度研究（P2）

- **项目**: haos-tailscale-subnet-router
- **阶段**: P2 深度收集
- **检索日期**: 2026-09-12
- **目标场景**: 标准 `192.168.1.0/24` 单层路由；HAOS 主机网段 = 要访问的网段（同网段）
- **用户基础**: 零基础（Tailscale 插件尚未安装）

---

## 1. 范围（Scope）

本阶段回答四个问题：

1. 在 HAOS 上如何安装并授权 Tailscale 插件（`hassio-addons/app-tailscale`，frenck 维护）。
2. 内网穿透：如何从外网访问 HA 界面与内网服务（Tailscale 直连 / Serve / Funnel 的取舍）。
3. 子路由：HAOS 上的 Tailscale 插件**能否**做 subnet router；在同网段场景下 SNAT 该开还是该关。
4. 验证与排错：路由不生效时按什么顺序排查；HAOS 特有的只读文件系统限制。

### 明确排除（不要写进笔记）

- `1024 条路由上限` 这一说法：P1 未找到任何一手出处，P2 亦未在任何官方文档中出现。**排除**。
- 已废弃的第二套插件 `hass-tailscale/hass-addons`（`auth_key` 登录那套）：仅作为「为什么网上教程互相矛盾」的背景说明，不做操作指引。
- 跨平台对比（fnOS / Docker 子路由）：已有独立运行 `tailscale-subnet-router-fnos`，本笔记只做一句对照链接。

### 主要来源与本地缓存

全部正文缓存在 `workspace/haos-tailscale-subnet-router/sources/`。P2 来源 ID → 文件映射：

| ID | 来源 | 层级 | 本地文件 |
| --- | --- | --- | --- |
| P2-S01 | `hassio-addons/app-tailscale` DOCS.md（main 分支） | T1 官方 | `08_raw_githubusercontent_com.md` |
| P2-S02 | Tailscale 官方：Subnet routers | T1 官方 | `14_tailscale_com.md` |
| P2-S03 | Tailscale 官方：Route injection | T1 官方 | `13_tailscale_com.md` |
| P2-S04 | Tailscale 官方：Manage client preferences | T1 官方 | `12_tailscale_com.md` |
| P2-S05 | Tailscale 官方博客：Remotely access Home Assistant（2026-07 更新） | T1 厂商 | `11_tailscale_com.md` |
| P2-S06 | Discussion #449（DNS / MagicDNS 与 hassio_dns） | T2 维护者 | `03_github_com.md` |
| P2-S07 | Issue #216（site-to-site，2 台 HA） | T2 维护者+一手复现 | `04_github_com.md` |
| P2-S08 | Issue #415（snat=false 失败案例） | T2 维护者+一手复现 | `06_github_com.md` |
| P2-S09 | Issue #430（同网段 ping 不通案例） | T3 社区 | `05_github_com.md` |
| P2-S10 | Forum 4374（另一套插件的 userspace 提示） | T3 社区 | `07_forum_tailscale_com.md` |
| P2-S11 | Issue #462（HA↔HA P2P 需开关 userspace） | T3 社区 | `09_github_com.md` |
| P2-S12 | Issue #96（多网段历史限制，现已解决） | T3 社区 | `10_github_com.md` |
| P2-S13 | `community.home-assistant.io/t/1011394`（仅 3 楼） | T4 无效 | 恢复后确认**不含**被归给它的主张，降级为「无关的未解决求助帖」 |
| P2-S14 | `docs.dev-eric.work` 非对称路由（站内已改路径） | T3 个人博客 | `16_docs_dev-eric_work.md` |
| P2-S15 | Issue #415 **完整评论串**（GitHub REST API） | T2 维护者实测 | `15_github_com.md` |

来源层级分布：T1 官方 5 条 / T2 维护者与一手复现 4 条 / T3 社区与个人博客 5 条 / T4 无效 1 条。

---

## 2. Claim / Source Map

### 2.1 安装与授权（探索方向 1）

| 编号 | 结论 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| C1.1 | 插件走 HA 插件商店安装，ID 为 `a0d7b954_tailscale`，仓库 `hassio-addons/repository` | P2-S01 | 文档底部 `[app]` 链接 |
| C1.2 | 安装后需点 **Start**，再 **Open Web UI** 完成登录授权，把 HA 挂到你的 tailnet | P2-S01 | `## Installation` 第 3–5 步 |
| C1.3 | 官方明确提示：**部分浏览器无法完成此步，建议在桌面/笔记本上用 Chrome** | P2-S01 | `## Installation` 第 5 步 Note |
| C1.4 | 建议关闭 key 过期（key expiry），否则连不上 HA | P2-S01 | `## Configuration` 首段 |
| C1.5 | HA 2026.8 起 **Add-ons 更名为 Apps**；HTTP 代理设置从 `configuration.yaml` 迁到 **Settings → System → Network → HTTP server** | P2-S05 | 正文与 Note |
| C1.6 | 插件配置项在 Tailscale 后台 Web UI 里是**只读**的，改了也会在重启后丢失——要改只能改插件 YAML | P2-S01 | `## Configuration` 的 `[!NOTE]` |

### 2.2 内网穿透（探索方向 2）

| 编号 | 结论 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| C2.1 | 不开口、不做反代即可远程访问 HA，这是 Tailscale 的默认能力 | P2-S05 | 开篇段 |
| C2.2 | 三种远程访问形态：① 直接用 tailnet IP `http://100.x.x.x:8123`；② **Serve**（tailnet 内、HTTPS + 自动证书）；③ **Funnel**（暴露到公网） | P2-S01 | `### Option: share_homeassistant` |
| C2.3 | Serve 前置条件：关闭 HA 的 **SSL/TLS**；在 **Settings → System → Network → HTTP server → Reverse proxy** 中启用 `Trust X-Forwarded-For`，并把 **`127.0.0.1`** 加入 **Trusted proxies**（不是 `100.64.0.0/10`） | P2-S01 / P2-S05 | 两处一致 |
| C2.4 | Serve 还需在 Tailscale 后台 DNS 页：改 tailnet 名、启用 MagicDNS、Enable HTTPS Certificates | P2-S01 | `### Option: share_homeassistant` 第 3 步 |
| C2.5 | Serve 使用 443 / 8443 / 10000 三个端口之一（默认 443）；上线后可能需最多 10 分钟生效 | P2-S01 | `### Option: share_on_port` 与 Note |
| C2.6 | 想用一个域名暴露插件商店里的其他服务（如 Audiobookshelf），用 `services` 选项（Tailscale Services）；该选项**不支持 Funnel，只支持 Serve**，且节点必须带 tag | P2-S01 | `### Option: services` |
| C2.7 | 官方博客把「HA 做 subnet router」直接描述为可用：*「if your Home Assistant box is on your home network at `192.168.1.50`, and you set it to offer routes at `192.168.1.0/24`, you could then access all the devices on your home network」* | P2-S05 | `## Use Home Assistant as an exit node or subnet router` |

### 2.3 子路由（探索方向 3）—— 本笔记的核心争议

**争议内容**：网上大量帖子称「HAOS 上的 Tailscale 插件做不了子路由 / 做不了跨网段转发」，但官方文档与维护者说的是「默认配置就能用」。

**关键证据链**

| 编号 | 结论 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| C3.1 | `advertise_routes` 是**列表**选项，直接写网段即可，如 `192.168.1.0/24` | P2-S01 | `### Option: advertise_routes` 及示例 YAML |
| C3.2 | `snat_subnet_routes` **默认开启**，作用是「让子网设备看到来自子网路由器的流量，从而简化路由配置」 | P2-S01 | `### Option: snat_subnet_routes`：「allows subnet devices to see the traffic originating from the subnet router, and this simplifies routing configuration.」 |
| C3.3 | 只有在做**进阶 site-to-site**（跨多网络）时才需要关掉 SNAT，并去照官方 site-to-site 指南走 | P2-S01 | 同上：「To support advanced Site-to-site networking … you can disable this functionality」 |
| C3.4 | **HAOS 上不要照抄 Linux 官方子路由教程的第 2 步**。插件已代做「IP address forwarding」和「Clamp the MSS to the MTU」；且 HAOS 根文件系统只读，`sysctl -p /etc/sysctl.d/99-tailscale.conf` 会直接报 **Read-only file system** | P2-S01 / P2-S08 | P2-S08：用户报错原文 + 维护者回复「Please read the docs, it says 'follow steps from step 3', because what you want to configure, is already set.」 |
| C3.5 | 维护者原话：*「With `snat_subnet_routes: true` it just works.」*，并称关掉 SNAT「requires much more config everywhere」 | P2-S08 | 维护者 lmagyar 评论 |
| C3.6 | 关掉 SNAT 后必须补一条回程路由：把 `100.64.0.0/10` 指向子网路由器的 **LAN IP**，否则 LAN 设备的回包进不了隧道 | P2-S02 | `--snat-subnet-routes=false` 小节 |
| C3.7 | 该条回程路由要落在**设备自身的操作系统 / 你的 VPC 设置 / 你的 DHCP 服务器**三处，且在官方支持的操作系统上才可控；HAOS 的根文件系统只读，很难照做 | P2-S02 / P2-S08 | P2-S02 `### Disable SNAT`：「You can configure this route in one of three places: On the device's operating system / In your VPC settings / Through your DHCP server」 |
| C3.8 | 实测失败案例 #430：`userspace_networking: false` + `snat_subnet_routes: false` + `accept_routes: true`，`ping 100.123.82.54`（tailnet 内）通，`ping 192.168.1.102`（同网段设备）不通 | P2-S09 | Issue 正文 |
| C3.9 | 实测失败案例 #415：同样 `snat_subnet_routes: false`，LAN→tailnet 方向不通；维护者指出方向搞反了，并补问「你是否也在管理端为源 LAN 启用了子网路由」 | P2-S08 | Issue 正文与评论 |
| C3.10 | 路由注入需要**同时**满足 4 个条件：① 路由器 advertise；② 管理端 approve；③ 控制面下发；④ 客户端 accept routes | P2-S03 | `## When routes are injected` |
| C3.11 | **ACL / grants 不会注入路由**。有路由没 ACL → 包进隧道被丢；有 ACL 没路由 → 包根本不进隧道。两者都要有 | P2-S03 | `## Route injection and access controls` |
| C3.12 | accept routes 的默认值按平台不同：**Windows / macOS / Android / iOS / tvOS 默认接受；Linux 默认不接受** | P2-S03 / P2-S04 | 两处一致 |
| C3.13 | 同网段冲突有安全兜底：*「In case your local subnets collide with subnet routes within your tailnet, your local network access has priority, and these addresses won't be routed toward your tailnet.」* 这是为了防止 HA 自己掉线；代价是无法用同网段做负载均衡/故障转移 | P2-S01 | `### Option: userspace_networking` Note |
| C3.14 | `userspace_networking` 当前默认**关闭**（即存在 `tailscale0` 接口） | P2-S01 | `### Option: userspace_networking`：「This option is disabled by default.」 |
| C3.15 | 但 2023 年维护者说的是相反的话：*「Current last released official add-on runs with userspace networking enabled, no tailscale0.」* → 默认值曾发生翻转 | P2-S07 | 维护者 2023-06-20 评论 |
| C3.16 | 2023 年 site-to-site 需要同时满足 5 条：① approve ② IP forwarding ③ **不用** `--tun=userspace-networking` ④ `--snat-subnet-routes=false` ⑤ 在本地 LAN 设备上加路由指向路由器的 eth0 | P2-S07 | 维护者同评论 |
| C3.17 | 单个 Tailscale 节点只 advertise 自己所在的 VLAN，不会自动 advertise 到别的 VLAN | P2-S10 | 论坛回复 |
| C3.18 | 多网段限制已是历史问题：#96 当时只能 advertise 第一个网段，诉求就是现在已实现的 `advertise_routes` 列表 | P2-S12 | Issue 正文 |

**争议判定（本笔记必须给出的明确结论）**

对于「HAOS 主机与目标设备同处 `192.168.1.0/24`、只想让远程 tailnet 设备访问家里局域网」这一场景：

1. **能做，且不需要关 SNAT。** 保持 `snat_subnet_routes: true`（默认值）即可。所有失败的复现（C3.8、C3.9）都出现在 SNAT 关闭的配置下，而维护者明确说开着「just works」（C3.5）。
2. **SNAT 是让这个场景「零额外配置即可用」的原因。** 远程 tailnet 客户端访问 `192.168.1.50` 时，目标设备不认识 `100.64.0.0/10`，它的回包只会发给默认网关然后被丢弃；SNAT 把源地址改写成路由器自己的 LAN 地址，回包就顺着原路回来了（即 C3.2 的「simplifies routing configuration」）。**但不要把它说成「关了必定不通」**——维护者的实测显示 SNAT 开或关都能工作，前提是在本地/上游路由器上补齐回程路由（见第 8 节 C8.3）。对零基础读者，「不需要补任何东西」本身就是选它的充分理由。
3. **不要照抄 Linux 官方子路由教程。** 官方 Linux 教程假定了完整的 Linux 主机控制权（可写 `/etc/sysctl.d/`、可改本地路由表）。HAOS 是只读托管系统，那两步要么已由插件代劳，要么根本做不了（C3.4、C3.7）。
4. **C3.13 的「本地优先」不是 bug。** HAOS 主机自己访问 `192.168.1.x` 时不会走隧道，这是保护机制，防止 HA 失联。子路由的收益对象是**远程的 tailnet 设备**，不是 HA 主机自己。
5. **只有当你确认要做 site-to-site（双向、跨多网段）时**，才需要关 SNAT + 开 `tailscale0` + 在各处补回程路由。对零基础的单点需求，这是明确的过度工程。

### 2.4 验证与排错（探索方向 4）

| 编号 | 结论 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| C4.1 | 排查顺序：① 管理端确认已 advertise（或 `tailscale status --json`）② 确认已 approve ③ Linux 客户端查 `tailscale debug prefs` 的 `RouteAll`，为 false 则 `tailscale set --accept-routes` ④ 查是否有更具体的本地路由抢了优先级（`ip route` / `netstat -rn`） | P2-S03 | `### Routes not appearing on client` |
| C4.2 | 路由存在但流量被挡：用 `tailscale debug netmap` 看 `PacketFilter` 段确认 ACL/grants；确认目标从路由器本机可达；查路由器/目标上的防火墙 | P2-S03 | `### Traffic blocked despite route existing` |
| C4.3 | key 过期会「fail close」：设备失去连接，且路由随之失效 | P2-S02 | key expiry 小节 |
| C4.4 | 上游若丢弃了 UDP，会出现「能 ping 通但网页卡死」的现象；此时才考虑 `always_use_derp: true` 兜底 | P2-S01 | `### Option: always_use_derp` |
| C4.5 | `log_suppression` 默认开启会在 200 行后压日志；排错时应先关掉它，Tailscale 日志很啰嗦 | P2-S01 | `### Option: log_suppression` |
| C4.6 | `tailscale ping <hostname-or-ip>` 用于验证 P2P 是否打通；打不通可尝试放行 `41641/udp` | P2-S01 | `## Network` |
| C4.7 | #462 的实操怪招：需要**先启用再关闭** `userspace_networking`，P2P 才生效（HA↔HA 场景，官方已 closed as not planned） | P2-S11 | Issue 正文 |

### 2.5 DNS（旁支，但「用名字访问」绕不开）

| 编号 | 结论 | 来源 | 原文锚点 |
| --- | --- | --- | --- |
| C5.1 | 要用 tailnet 名字访问，需 `userspace_networking` 关闭，且**不要**在 HA 的 Network 页把 Tailscale DNS 设为 DNS 服务器；改为命令行执行 `ha dns options --servers dns://100.100.100.100` | P2-S01 | `## DNS` 第 1–3 步 |
| C5.2 | 该命令是**持久化**的，只需执行一次；要用 `ha dns reset` + `ha dns restart` 才能清空 | P2-S01 | `## DNS` Note |
| C5.3 | 代价：**必须用 FQDN**，`ping device.tail1234.ts.net` 可以，`ping device` 不行 | P2-S01 | `## DNS` Note |
| C5.4 | 已知坑：MagicDNS 解析失败时**不返回** REFUSED/SERVFAIL/NXDOMAIN，而是回头去问系统原本的 DNS（在 HA 上就是 `hassio_dns`）→ 形成 loop → `hassio_dns` 崩溃 → 连带 supervisor、nginx 一起挂 | P2-S06 | 维护者 2025-01-15 评论（含 coredns `plugin/loop` 原文日志） |
| C5.5 | 维护者的修法是给 `tailscaled` 挂一个空的 `resolv.conf`，或跑一个对一切回 REFUSED 的 dnsmasq（`127.52.52.52:53`） | P2-S06 | 同评论 |
| C5.6 | 插件停下来时，配置在 HA 里的 `100.100.100.100` 会被**跳过**，不会导致 DNS 全挂（维护者已实测） | P2-S06 | 维护者 2025-01-15 回复 |
| C5.7 | `accept_dns: false` 的含义是「不接受管理端下发的**全局 nameserver**」，**不是**本地关闭 MagicDNS，也不是本地关闭 Tailscale DNS | P2-S06 | 维护者 2025-01-13 评论 |
| C5.8 | 早期结论「干脆全局关掉 MagicDNS」被维护者自己次日推翻：关掉后 Ubuntu / Win11 客户端的解析会连带失效，正解是修 `hassio_dns` 的 loop，而非关 MagicDNS | P2-S06 | 两日评论对照 |

---

## 3. 矛盾与分歧（Contradictions）

| # | 分歧 | 各方说法 | 判定 |
| --- | --- | --- | --- |
| D1 | `userspace_networking` 默认值 | 2023 维护者：默认开启（P2-S07）；当前 DOCS：默认关闭（P2-S01） | **默认值已翻转**。网上 2023–2024 的教程与论坛帖大量基于旧默认值，是本主题最大的误导来源。笔记必须提醒读者：以你装完那一刻配置页的实际值为准 |
| D2 | 谁在做子路由时是必需的 | 论坛：userspace 必须开，否则「route 会被 announce 但流量出不了容器」（P2-S10）；维护者：子路由与 userspace 无关（P2-S07） | P2-S10 讲的是**另一套已废弃插件**，且其结论与当前官方默认相冲突。**不采信为操作指引**，只作为「网上说法为何矛盾」的解释 |
| D3 | SNAT 该开还是该关 | 多个失败帖都是关了 SNAT（P2-S08、P2-S09）；维护者：开着 just works（P2-S08）；官方：关 SNAT 属进阶 site-to-site（P2-S01、P2-S02） | **同网段场景保持开启**。关 SNAT 是一个需要额外回程路由的进阶开关，不是「更彻底」的选项 |
| D4 | HAOS 能不能做子路由 | 社区大量「不能」的经验帖；官方博客与维护者认为默认配置即可（P2-S05、P2-S08） | 倾向「能做」。但 P2-S13 那篇被 Cloudflare 拦下的实操帖是反方最有力的证据，**尚未核验**，见第 5 节 |
| D5 | MagicDNS 是否要关 | 同一维护者先给「全局关掉」（P2-S06）次日又推翻为「别关，去修 loop」（P2-S06） | 采信**次日**的最终结论：不要关 MagicDNS；开 `accept_dns` 并按 DNS 章节配置 `100.100.100.100` |
| D6 | 插件运行时的网络接口归属 | 2023 讨论中作者观察到「HA core UI 两种情况都能访问」，怀疑 `tailscale0` 对其他容器并无威胁（P2-S07） | 现象属实但成因未定论。**标记为未解**，不影响实操结论 |

---

## 4. 实操指引（给下游章节写作的推荐基线）

### 4.1 目标场景的推荐配置

```yaml
accept_dns: true
accept_routes: false
advertise_routes:
  - 192.168.1.0/24
snat_subnet_routes: true      # 默认值，保持不动 —— 本场景的核心
userspace_networking: false   # 默认值，保持不动 —— tailscale0 存在才能双向
```

配套动作（缺一不可）：

1. 启动插件 → Open Web UI 完成登录授权（建议桌面 Chrome）。
2. Tailscale 管理后台 → Machines → 找到 `homeassistant` → `…` → Edit route settings → 勾选 `192.168.1.0/24`。
3. 在**远程客户端**上确认接受路由：Windows / macOS 默认已接受；**Linux 默认不接受**，需 `tailscale set --accept-routes`。
4. 客户端上 `ping 192.168.1.50` 之类的局域网地址验证。

### 4.2 三条「别照抄」警告（写笔记时必须显式提示）

1. **别去 HAOS 上跑 `sysctl` 开 IP 转发** —— 只读文件系统 + 插件已代劳。
2. **别把 `snat_subnet_routes` 改成 false** —— 除非你明确要做 site-to-site，且已准备好补 `100.64.0.0/10` 的回程路由。
3. **别把「HAOS 主机自己访问不到 `192.168.1.x` 走隧道」当成故障** —— 这是官方有意设计的本地优先保护。

### 4.3 验证清单（可直接作为排错章骨架）

依据 P2-S03 的四条件与 PA-S02 的 fail-close 行为，按此顺序查：

1. 管理端是否已 approve 该子网路由。
2. 客户端是否 accept routes（Linux 特别注意）。
3. 是否被更具体的本地路由抢了优先级。
4. `tailscale debug netmap` 的 `PacketFilter` 是否放行（ACL 与路由是两套东西）。
5. key 是否过期。
6. 路由器自身能否访问目标设备。

---

## 5. 未解与缺口（Open Questions）

| # | 缺口 | 影响 | 处理 |
| --- | --- | --- | --- |
| G1 | ~~P2-S13（`community.home-assistant.io/.../1011394/3`）被 Cloudflare JS 挑战拦截~~ | **已结案，且结论是「该来源不存在」**——恢复后确认该帖（仅 3 楼）根本没有承载被归给它的任何主张。原 P1 侦察对该帖的描述属**错误归属** | 见第 8 节 C8.1。该帖降级为「一个未解决的用户求助帖」，**不得**作为反方证据引用 |
| G2 | ~~P2-S14（`docs.dev-eric.work` 非对称路由文）返回 404~~ | **已恢复**，站内改路径，正文已缓存 | 见第 8 节 C8.4–C8.7。升级为 P2-S16，是本主题「同网段」场景最有价值的边角坑来源（但是个人博客，非官方） |
| G3 | P1 侦察得到的「#430 评论区提到换网段 / 软砖 HA / 规避顺序」等说法，在抓取到的正文中**不存在**（GitHub 评论需登录） | 若直接采信会构成伪造引用 | **标记为未核验**，不得写入笔记；如需，须重新取评论区 |
| G4 | 「1024 条路由上限」的说法无任何一手出处 | 属流言 | **已排除**，不写入笔记 |
| G5 | 插件版本 ↔ 内置 Tailscale 版本 ↔ `userspace_networking` 默认值的对应表未建立 | 读者可能反复疑惑「为什么文档和我看到的不一样」 | 笔记用「以你配置页实际默认值为准 + 附校验方法」的方式绕开，不去猜版本号 |
| G6 | 同网段场景下「远程客户端 → 局域网非 Tailscale 设备」是否真的开箱即用，尚无一手实测记录 | 这是本笔记的核心承诺，目前靠官方文档 + 维护者说法支撑，缺一手验证 | **建议作为笔记的「验收章节」**，让读者自己跑通并记录；不要写成「必定成功」 |

**给下游的诚实度要求**：G1、G2、G3 三条涉及未核验内容。写作阶段若引用相关说法，必须显式标注未核验，或改写为「官方文档未提及 / 社区有不同报告」。P2-S13 与 P2-S14 两条来源**不得**以「据某文章」的形式出现。

---

## 6. 下游交接（Downstream Handoff）

交给 `outline-generator` 与 `chapter-writer`：

**可直接使用的素材路径**

- 主线配置与选项语义：`sources/08_raw_githubusercontent_com.md`（P2-S01）
- 子路由官方机制与 SNAT 回程路由：`sources/14_tailscale_com.md`（P2-S02）
- 路由注入四条件与排错顺序：`sources/13_tailscale_com.md`（P2-S03）
- 客户端默认值（Linux 不接受路由）：`sources/12_tailscale_com.md`（P2-S04）
- 同网段的官方场景描述：`sources/11_tailscale_com.md`（P2-S05）
- DNS 坑与 `hassio_dns` loop：`sources/03_github_com.md`（P2-S06）
- site-to-site 五条件与 userspace 默认值翻转：`sources/04_github_com.md`（P2-S07）
- 「开着 SNAT just works」与只读文件系统报错原文：`sources/06_github_com.md`（P2-S08）
- 失败复现（snat=false）：`sources/05_github_com.md`（P2-S09）

**写作纪律**

- 引用官方口径时，回 `sources/` 里的原文核对，不要只凭本文件的转述；本文件的引号内文字已逐字核对，引号外的是归纳。
- 不要向 `chapter-writer` 传递转述过的「某某说过」，只传来源 ID、文件路径与锚点。
- 三个「别照抄」警告（4.2）与同网段 SNAT 结论（2.3 判定 1–5）是**必写**内容，不是可选补充。
- 含未核验标记的 5.1、5.2、5.3 三条不得进入正文。

---

## 7. P2 完成判据

- [x] 核心来源正文已缓存到 `sources/`（12 条成功，2 条失败并记录原因）
- [x] 每条实质结论均映射到来源 ID 或显式标记为推论/未核验
- [x] 争议已收敛为可执行的判定（2.3）
- [x] 缺口与诚实度要求已显式列出（第 5 节）
- [ ] 用户确认素材质量（**当前等待**）

---

## 8. P2 补遗：后台恢复任务结果（2026-09-12，P2 关闭后到达）

> 本节是 P2 关闭后由后台恢复任务补回的证据，**已在 P3 大纲生成前生效**。第 1–7 节保持原貌以保留判断过程，凡与本节冲突处，**以本节为准**。
> 两条来源均已重新落盘：`sources/15_github_com.md`（P2-S15）、`sources/16_docs_dev-eric_work.md`（P2-S14）。

### 8.1 P2-S13 是错误归属，必须撤回

原 P1 侦察把「路由已批准、同 tailnet 的 Windows 客户端能 ping 通、HA 自身终端不发包」三项主张归给 `community.home-assistant.io/t/1011394`。恢复后逐楼核对（全帖仅 3 楼，`posts_count: 3`，`reply_count: 0`）：

- 该帖 1 楼只是「刚装好 HA，访问不到 subnet router，求帮助」；2 楼要求贴网络发现结果；3 楼是转储 + 致谢。**没有任何结论**。
- 「approve」「Windows」「ping」在该帖中**一次都没出现**。
- 该帖环境是 `10.0.0.0/24`（HA `10.0.0.246`，网关 TP-Link ER7212PC），**不是** `192.168.0.0/16`。

**结论**：这是一次**错误归属**，不是「未核验」。我此前向你描述的「反方最有力的实操帖」**不存在**。该帖只能降级为「一个未解决、无结论的用户求助帖」，并在笔记中完全不引用。

### 8.2 新来源 P2-S15：维护者本人对 HAOS 子路由的完整实测（改变结论强度）

Issue #415 的完整 16 条评论（`sources/15_github_com.md`）里有维护者 lmagyar 的两条关键实测记录，**逐字引用**：

> "OK, I've tested meticuously the site-to-site networking (for another reason), and in short, it works flawlessly, no need for any extra iptables rule."
> "Test was done with rPIs running HASS OS."
> "So I think this is not a HASS OS or add-on issue, but a local net/VM config issue."

> "And tested on a VirtualBox VM running HA-OS: exact same results as with rPI+HA OS: it just works, with userspace enabled/disabled, snat enabled/disabled, local/router routing config."

**要点**：

1. **这是本主题最强的一条正面证据**：维护者在**两种 HAOS 部署形态**（树莓派实机 + VirtualBox 虚拟机）上做过严格测试，结论是**能工作**，且明确定性为「不是 HAOS 或插件的问题，是本地网络/VM 配置问题」。
2. **测试的是 site-to-site**（双向、跨网段），比本笔记用户的需求（远程 tailnet → 局域网单向）**更难**。更难的方向都过了，用户的需求在能力范围内。
3. **措辞修正**：维护者说 `with userspace enabled/disabled, snat enabled/disabled` 都能工作 —— 但注意他同时提到 "local/router routing config" 和一次防火墙问题（见下）。所以正确表述是「关 SNAT 也能通，但要补回程路由」，**不是**「关了必不通」。第 2.3 节判定 2 已据此修订。
4. **维护者亲述的一个真实坑**（对第 7 章排错有价值）：
   > "when I used the router to route toward my TS subnet router, while outgoing (LAN->tailnet) connections worked fine, I lost the returning/reply packets from the LAN back to the tailnet (different path for the returning packets, they go through the router, while the original packages from the tailnet was sent by the TS subnet router directly to the non-TS device), but this was a firewall issue"

   即：让**上游路由器**参与转发时，会制造回程包走另一条路径的非对称问题，需在防火墙上放行。这正是「同网段 + 路由器参与」时最容易踩的坑。

### 8.3 反方证据的真实形态（修订第 2.3 节与第 3 节 D4）

撤回 P2-S13 之后，「HAOS 做不了子路由」这一叙事剩下的真实依据是：

- **P2-S07（#216，2023）**：作者观察 `Supervisor eth0` 的默认路由把回包送回本地路由器，`"There is no route to any tailscale interface for the outbound traffic"`。这是**容器网络路径**层面的质疑。
- **P2-S15（#415）**：原提问者最终放弃，自述该部分在 HASS OS 上「不可配置」。

而反证是 **P2-S15 维护者的两种部署形态实测**。**判定：反方证据被显著削弱，正面结论增强。** 但注意两者讲的不是同一件事 —— 反方讲「去程进不去 `tailscale0`」，维护者讲「整体链路能通」。

### 8.4 新来源 P2-S14（原 P2-S14/S38）：同网段场景的非对称路由坑

来源：`sources/16_docs_dev-eric_work.md`，个人博客（**非官方**），原标题 `Tailscale Subnet Router and Asymmetric Routing on a Home LAN`，原路径已 404，改存 `/archive/` 路径。

| 编号 | 结论 | 原文锚点 |
| --- | --- | --- |
| C8.4 | 失效模式描述：子路由节点 advertise 了**其他 Tailscale 节点已经在用的同一个 LAN**，症状是「设备 tailnet IP 可达，但 LAN IP 不可达，从局域网内 ping 100% 丢包」 | `## Goal` |
| C8.5 | 机制：入包走 LAN（`Mac -> Pi Zero`），回包却被 table 52 里的 `192.168.68.0/22 dev tailscale0` 抢走（`Pi Zero -> tailscale0 -> Home Assistant`）→ 非对称路由 | `## What Goes Wrong` |
| C8.6 | **HAOS 自带保护**：`"Some systems, such as Home Assistant OS, protect local traffic with a higher-priority rule"`，规则形如 `5000: from all to 192.168.68.0/22 lookup main` 优先于 `5270: from all lookup 52`；而普通 Raspberry Pi OS 可能缺这条规则 | `## Why One Device Breaks but Another Does Not` |
| C8.7 | `--accept-routes=false` 的**语义澄清**：它**不**表示「别的设备无法通过子路由访问本机」，而是「本机不会用其他 peer 广播的子路由来做自己的出站路由决策」 | `## Fix Option 2 → A common misunderstanding` |

**注意（必须标注）**：

- C8.6「HAOS 自带 priority 5000 保护规则」**只有一个非官方来源**，未在任何 HAOS 或 Tailscale 官方材料中得到印证。笔记中若引用，**必须标注为单一来源、待官方核实**，或干脆只描述现象不引机制。
- 该文的 `192.168.68.0/22` 等具体值是作者自己的环境，**不可外推**。
- 该文的立场是**非对称路由/客户端侧配置问题**，**不是**「插件容器网络模式天生做不到」——不要把它读成反方证据。

### 8.5 对既有配置建议的影响

**核心推荐不变**（`advertise_routes: 192.168.1.0/24` + `snat_subnet_routes: true` + `userspace_networking: false` + `accept_routes: false`），而且**证据强度提升**：

1. `accept_routes: false` 从「顺手保持默认」升级为**有明文依据的主动选择**——C8.7 明确指出它正是防止本机被 peer 子路由劫持的官方手段之一。
2. 维护者实测把「HAOS 能不能做」从「官方文档说可以」提升到「维护者在两种 HAOS 部署上实测通过」。
3. 新增一条**同网段专属警告**（第 4 条「别照抄」）：如果这个 LAN 上还有**其他装了 Tailscale 的 Linux 节点**，它们可能被这条子路由搞成非对称路由而失去局域网可达性；HAOS 自身有保护，其他节点未必有。这是 P2-S14 的核心价值。

### 8.6 仍未解决

| # | 缺口 | 处理 |
| --- | --- | --- |
| G7 | C8.6 的 priority 5000 规则无官方印证 | 笔记中标为单一来源；或只写现象 |
| G8 | 维护者的实测未给出完整可复现步骤（只说「本地/上游路由器路由配置」） | 不写成分步教程，只作为结论强度背书 |
| G9 | P2-S14 代码块的多行输出在抓取时被压平 | 引用时只引单行命令（`ip rule show`、`ip route show table 52`、`ip route get`），不引拼接后的多行输出 |
