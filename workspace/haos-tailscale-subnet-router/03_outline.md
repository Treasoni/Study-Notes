# 用 HAOS 上的 Tailscale 插件打通内网穿透与子路由（同网段 `192.168.1.0/24` 实战）

> 目标读者：已经跑着 HAOS、还没装过 Tailscale，想从外网访问 HA 和家里局域网设备的人
> 笔记类型：实战笔记 | 深度：上手 | 预计总字数：约 8100 中文字
> 素材来源：workspace/haos-tailscale-subnet-router/02_deep_research.md 与 sources/ 下缓存正文
> **修订说明（2026-09-12）**：P2 关闭后，后台来源恢复任务返回两条结果，本大纲已同步修订 —— ① 原定的「反方关键帖」经核实为**错误归属**，已撤回（见 02_deep_research.md 第 8.1 节）；② 找回一篇同网段非对称路由文并新增一章内容（4.5）；③ 新增维护者对 HAOS 的两种部署形态实测，结论强度上调。本节起生效。

## 大纲总览

| 章 | 标题 | 篇幅 | 核心素材 |
| --- | --- | --- | --- |
| 1 | 结论前置：同网段到底要不要开 SNAT | 约 1000 字 | P2-S01、P2-S02、P2-S03、P2-S05、P2-S08 |
| 2 | 装插件并完成登录授权 | 约 800 字 | P2-S01、P2-S05 |
| 3 | 内网穿透：不开口、不做反代就远程访问 | 约 1000 字 | P2-S01、P2-S05 |
| 4 | 子路由：把 HAOS 变成 tailnet 的网关 | 约 1700 字 | P2-S01、P2-S02、P2-S03、P2-S08、P2-S09、P2-S12、P2-S14、P2-S15 |
| 5 | 在远程客户端上接收路由 | 约 700 字 | P2-S03、P2-S04 |
| 6 | 验收：你自己跑一遍六步 | 约 900 字 | P2-S03、P2-S01、P2-S02、P2-S05、P2-S15 |
| 7 | 排错：按顺序查，别猜 | 约 1400 字 | P2-S03、P2-S01、P2-S02、P2-S08、P2-S11、P2-S06、P2-S14、P2-S15 |
| 8 | 边界、未核验声明与下一步 | 约 600 字 | P2-S01、P2-S02、P2-S07、P2-S14、P2-S15 |

全篇四个方向全部落地：① 安装与登录授权 = 第 2 章；② 内网穿透 = 第 3 章；③ 子路由 subnet router = 第 4、5 章；④ 验证与排错 = 第 6、7 章。第 1 章负责把同网段 SNAT 结论与三条「别照抄」警告一次性讲清楚。

## 第 1 章 结论前置：同网段到底要不要开 SNAT

- 篇幅：约 1000 字
- 素材引用：P2-S01（workspace/haos-tailscale-subnet-router/sources/08_raw_githubusercontent_com.md）、P2-S02（workspace/haos-tailscale-subnet-router/sources/14_tailscale_com.md）、P2-S03（workspace/haos-tailscale-subnet-router/sources/13_tailscale_com.md）、P2-S05（workspace/haos-tailscale-subnet-router/sources/11_tailscale_com.md）、P2-S08（workspace/haos-tailscale-subnet-router/sources/06_github_com.md）
- 代码/配置示例：一份「本文推荐配置」YAML 预览块（`accept_dns` / `accept_routes` / `advertise_routes` / `snat_subnet_routes` / `userspace_networking` 五行，正文第 4 章展开）；无 shell 命令块
- 学习目标：读者在动手前就知道最终配置长什么样、为什么 SNAT 不能关，并知道本篇不做哪些事

### 1.1 这篇笔记解决什么、不解决什么

- 要点：场景三要素——单层 `192.168.1.0/24` 家用路由器、HAOS 主机与要访问的设备同处这个网段、远程客户端是手机/笔记本
- 要点：三个明确目标——外网访问 HA 界面、用 tailnet 域名 + HTTPS 访问、让远程设备访问家里不装 Tailscale 的设备（打印机/摄像头/路由器）
- 要点：明确不覆盖 exit node、Taildrop、Taildrive、多站点对比；与既有 `tailscale-subnet-router-fnos` 的对照只放在第 8 章一句话，不展开
- 素材引用：P2-S05、P2-S01

### 1.2 结论：能做，而且保持 `snat_subnet_routes: true` 不动

- 要点：同网段单点需求属于官方文档描述的标准可做场景，不需要关 SNAT，不需要动 `userspace_networking`
- 要点：为什么这条结论要前置——网上大量「HAOS 做不了子路由」的经验帖都出现在 SNAT 被关掉的配置下
- 素材引用：P2-S05、P2-S01、P2-S08

#### 1.2.1 为什么保持 SNAT 开着是「零额外配置」的那条路

- 要点：远程 tailnet 客户端访问 `192.168.1.50` 时，目标设备本身不认识 `100.64.0.0/10`，它的回包只会发给默认网关然后被丢弃
- 要点：SNAT 把源地址改写成子路由器的 LAN 地址，回包才能顺着原路回到隧道，这正是官方文档说的「simplifies routing configuration」
- 要点：**别把它讲成「关了就必定不通」**——维护者的实测显示 SNAT 开或关都能工作，但关掉后必须在一堆地方补回程路由；对零基础读者，「不需要补任何东西」本身就是选它的充分理由
- 要点：官方把「关 SNAT」定位成进阶 site-to-site 才会用的开关，不是「更彻底」的选项
- 素材引用：P2-S01、P2-S02、P2-S15（sources/15_github_com.md）

### 1.3 四条「别照抄」警告，以及它们在后文的落点

- 要点：警告① 别去 HAOS 上跑 `sysctl` 开 IP 转发（HAOS 根文件系统只读，插件已代做）——展开在第 4 章 4.2.1，报错现场在第 7 章 7.4.3
- 要点：警告② 别把 `snat_subnet_routes` 改成 `false`，除非你确定要做 site-to-site 并已准备好补 `100.64.0.0/10` 回程路由——展开在第 4 章 4.2.2，代价在第 8 章 8.1
- 要点：警告③ 别把「HAOS 主机自己访问 `192.168.1.x` 不走隧道」当成故障——这是官方有意设计的本地优先保护，展开在第 6 章 6.2.1 和第 7 章 7.5
- 要点：警告④（同网段专属）如果你的 `192.168.1.0/24` 上还有**其他装了 Tailscale 的 Linux 节点**，它们可能被这条子路由搞成非对称路由、失去局域网可达性——展开在第 4 章 4.5，现象与自查在 7.5
- 素材引用：P2-S01、P2-S02、P2-S08、P2-S09、P2-S14（sources/16_docs_dev-eric_work.md）

### 1.4 为什么你必须以自己配置页的实际默认值为准

- 要点：`userspace_networking` 的默认值发生过翻转——2023 年维护者说当时官方插件是 userspace networking 开启、没有 `tailscale0`；当前文档写的是 disabled by default
- 要点：网上 2023–2024 年的教程和论坛帖大量基于旧默认值，这是本主题最大的误导来源
- 要点：不要靠背版本号规避，方法是以你装完那一刻配置页显示的值 + 一条校验命令为准（方法放第 5 章 5.3）
- 素材引用：P2-S01、P2-S07（workspace/haos-tailscale-subnet-router/sources/04_github_com.md）

## 第 2 章 装插件并完成登录授权

- 篇幅：约 800 字
- 素材引用：P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S05（sources/11_tailscale_com.md）
- 代码/配置示例：无 YAML 块、无 shell 命令块（本章全部是 HA 界面与 Tailscale 控制台操作，逐屏给出点击路径）
- 学习目标：读者能把插件装上、看到 Machines 列表里出现 `homeassistant` 且是绿点，并知道插件后台 Web UI 里改配置无效

### 2.1 开工前的准备

- 要点：注册 Tailscale 账号（个人/爱好项目免费额度），明白 tailnet 是你自己的私有网络
- 要点：先关闭该设备的 key 过期，否则过期后会失联，且路由会 fail-close（对应第 7 章 7.4.1）
- 要点：顺手把 tailnet 名改成好记的名字（第 3 章 Serve 要用）
- 素材引用：P2-S01、P2-S05

### 2.2 在 HA 应用商店里安装

- 要点：Settings → Apps（2026.8 起由 Add-ons 更名而来）→ Install app → 搜索 Tailscale → Install
- 要点：确认装的是哪个插件——本笔记操作的是 `hassio-addons/app-tailscale`，插件 ID `a0d7b954_tailscale`，来自仓库 `hassio-addons/repository`，维护者 frenck
- 要点：背景说明，不构成操作指引——另一套 `hass-tailscale/hass-addons`（填 `auth_key` 那套）已废弃，网上教程互相矛盾多源于此，只需要认识它、不需要照它做
- 素材引用：P2-S01、P2-S05

### 2.3 启动并完成登录授权

- 要点：点 Start，再点 Open Web UI 完成授权，把 HA 挂到你的 tailnet 上
- 要点：官方明确提示部分浏览器无法完成这一步，建议用桌面/笔记本上的 Chrome
- 要点：可选打开 Watchdog / Auto update / Show in sidebar
- 素材引用：P2-S01、P2-S05

### 2.4 确认上线，以及一个会浪费你半天的坑

- 要点：回到控制台 Machines 页，看到名为 `homeassistant` 的设备，绿点表示已连接
- 要点：插件后台 Web UI 里那些选项是只读的，在那里改了重启就会丢；要改配置只能改插件自己的 YAML——这决定了第 4 章的配置方式
- 要点：已知的界面不一致现象——有人在 UI 上看到的值和实际生效值对不上，因此第 5 章给了一条校验命令
- 素材引用：P2-S01、P2-S11

## 第 3 章 内网穿透：不开口、不做反代就远程访问

- 篇幅：约 1000 字
- 素材引用：P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S05（sources/11_tailscale_com.md）
- 代码/配置示例：`share_homeassistant` / `share_on_port` 的 YAML 片段一处；`always_use_derp` 的 YAML 片段一处（作为「不要急着开」的对照）；shell 命令块：`ha dns options --servers dns://100.100.100.100`、`ha dns reset`、`ha dns restart`
- 学习目标：读者能从外网打开 HA，并且能用域名 + HTTPS 访问；知道 MagicDNS 该怎么接、什么时候不该接

### 3.1 最小可用路径：先能用

- 要点：授权完成后，直接用 tailnet IP 加端口访问 HA 就是可用的，这是 Tailscale 的默认能力，不需要端口转发、不需要反代
- 要点：先在本机验证这条路径，再去做 Serve
- 素材引用：P2-S05、P2-S01

### 3.2 更好的路径：Serve 给一个域名和证书

- 要点：HA 侧前置——关闭 `SSL/TLS`；到 Settings → System → Network → HTTP server → Reverse proxy 启用 `Trust X-Forwarded-For`，并把 `127.0.0.1` 加进 `Trusted proxies`
- 要点：控制台 DNS 页前置——改 tailnet 名、启用 MagicDNS、Enable HTTPS Certificates
- 要点：端口只能用 443 / 8443 / 10000 之一（默认 443）；首次设置后域名生效可能最多 10 分钟
- 要点：别再用原来那个端口号拼 URL；浏览器行为异常时先清站点 cookie 与缓存
- 素材引用：P2-S01、P2-S05

#### 3.2.1 为什么 `Trusted proxies` 填 `127.0.0.1` 而不是 `100.64.0.0/10`

- 要点：HA 侧看到的是本机代理转发过来的连接，所以可信代理写回环地址；这一条在两份官方材料里一致，也是新手最容易填错的地方
- 素材引用：P2-S01、P2-S05

### 3.3 Funnel 与 `services`：先别急着开

- 要点：Funnel 会把 HA 暴露到公网，与「不开口」的初衷相反，普通需求不要开
- 要点：`services` 选项可以在同一个域名下暴露插件商店里的其他服务（例如 audiobookshelf），但它只支持 Serve 不支持 Funnel，而且要先把节点打上 tag
- 素材引用：P2-S01

### 3.4 用 tailnet 名字访问：MagicDNS 怎么接才不炸

- 要点：想用 tailnet 名字，前提是 `userspace_networking` 处于关闭状态（这样才有 `tailscale0` 和 `100.100.100.100`）
- 要点：不要在 HA 的 Network 页把 Tailscale DNS 设成 DNS 服务器，改用命令行执行 `ha dns options --servers dns://100.100.100.100`
- 要点：这条命令是持久化的，只需执行一次；要清空得用 `ha dns reset` + `ha dns restart`
- 要点：代价是必须用 FQDN——`ping device.tail1234.ts.net` 可以，`ping device` 不行
- 要点：`accept_dns: false` 的含义是「不接受控制台下发的全局 nameserver」，不是本地关掉 MagicDNS，也不是本地关掉 Tailscale DNS
- 要点：这条命令有一个已知的严重后果，修法与现象放在第 7 章 7.4.4，照做前请先读那一节
- 素材引用：P2-S01、P2-S06（workspace/haos-tailscale-subnet-router/sources/03_github_com.md）

### 3.5 直连还是中继：要不要开 `always_use_derp`

- 要点：默认不要开；只有当出现「能 ping 通但网页/App 卡死」这种上游丢弃 UDP 的特征时才考虑兜底
- 要点：P2P 是否打通交给第 7 章的 `tailscale ping` 与 `41641/udp` 检查
- 素材引用：P2-S01

## 第 4 章 子路由：把 HAOS 变成 tailnet 的网关

- 篇幅：约 1400 字
- 素材引用：P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S02（sources/14_tailscale_com.md）、P2-S03（sources/13_tailscale_com.md）、P2-S08（sources/06_github_com.md）、P2-S09（sources/05_github_com.md）、P2-S12（sources/10_github_com.md）、P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）
- 代码/配置示例：插件完整 YAML 配置块（`accept_dns`、`accept_routes`、`advertise_routes`、`snat_subnet_routes`、`userspace_networking`）并在逐项解释时按项拆开引用；反面示例两处——Linux 官方教程的 `sysctl` 三行命令 + 只读文件系统报错原文（引用块），`tailscale up --snat-subnet-routes=false` 一行（标注「本场景不要执行」）
- 学习目标：读者能写出正确的插件配置、理解每一项为什么取这个值、并在控制台完成路由授权

### 4.1 子路由在做什么：一句话和一条边界

- 要点：子路由让不能装 Tailscale 的设备也能被 tailnet 访问；对端设备看到的是网关在转发，不需要在自己身上装任何东西
- 要点：与 exit node 的边界——子路由只暴露指定网段，exit node 接管全部出站流量，两者别混用也别混谈
- 素材引用：P2-S02、P2-S01

### 4.2 本文推荐配置与逐项解释

- 要点：给出完整 YAML 块，并说明「其余选项保持默认，不要一起抄进来」
- 要点：`advertise_routes` 是列表，写你要暴露的网段，例如 `192.168.1.0/24`；过去只支持单个网段的多网段限制已是历史问题，现在这就是一个列表（对应 P2-S12 的旧 issue 已由该选项满足）
- 要点：`accept_routes: false` 在本场景的理由——HAOS 自己不需要接受别人的网段；更重要的是它正是防止本机被 peer 广播的子路由劫持的标准手段（它的准确语义是「本机不用其他 peer 的子路由做自己的出站路由决策」，**不**等于「别人访问不到本机」）
- 要点：`accept_dns: true`（默认）保持不动，与第 3 章的 DNS 章节配合
- 要点：`snat_subnet_routes: true`（默认）保持不动 —— 本章核心
- 要点：`userspace_networking: false`（默认）保持不动；改配置后记得重启插件
- 素材引用：P2-S01、P2-S02、P2-S12

#### 4.2.1 警告①：不要照抄 Linux 子路由教程的第 2 步

- 要点：官方 Linux 教程要你写 `/etc/sysctl.d/99-tailscale.conf` 再 `sysctl -p`，那一步假定你有完整可写的 Linux 主机
- 要点：在 HAOS 上照抄会直接报错，给出报错原文的引用块（`Read-only file system`）
- 要点：维护者回复原话——「follow steps from step 3」，因为你想配置的东西已经设好了；插件已代做 IP address forwarding 与 Clamp the MSS to the MTU
- 素材引用：P2-S01、P2-S08

#### 4.2.2 警告②：不要关 `snat_subnet_routes`

- 要点：关掉之后必须补一条回程路由，把 `100.64.0.0/10` 指向子路由器的 LAN IP，否则 LAN 设备的回包进不了隧道
- 要点：那条回程路由要落在设备自身、上游路由器或 DHCP 上，且在官方支持的操作系统上才可控——HAOS 只读，很难照做
- 要点：官方语义与维护者原话（`just works`）的引用；以及官方提示「只有完全理解后果才关」
- 要点：把「关 SNAT 是进阶 site-to-site 的开关」与「失败案例都出现在 snat=false」两件事并列，让读者自己看出因果
- 素材引用：P2-S01、P2-S02、P2-S08、P2-S09

### 4.3 在管理控制台授权这条路由

- 要点：Machines 页 → 用 Subnets 标记/过滤找到 HA → 打开 Subnets 段 → Edit route settings → 在 Subnet routes 下勾选 `192.168.1.0/24` → Save
- 要点：不授权的后果——路由不会被下发到任何客户端，表现为「配了没生效」，这是第 7 章第 1 顺位要查的
- 要点：给服务器关闭 key 过期，避免反复重新认证（第 2 章已做一次，这里复核）
- 素材引用：P2-S01、P2-S02、P2-S03

### 4.4 「HAOS 做不了子路由」这个说法从哪来

- 要点：读者会遇到的矛盾——社区大量「不能」的经验帖 vs 官方材料说默认配置就行
- 要点：反方的真实依据，两类——容器网络路径层面的质疑（`Supervisor eth0` 的默认路由把回包送回本地路由器，没有到 tailscale 接口的出站路由）；以及用户照抄 Linux 教程失败后放弃，失败复现里反复出现 `snat_subnet_routes: false`
- 要点：**正方的强度要讲清楚**——维护者在**两种 HAOS 部署形态**（树莓派实机 + VirtualBox 虚拟机）上做过严格测试，结论是能工作，并明确定性为「不是 HAOS 或插件的问题，是本地网络/VM 配置问题」。而且他测的是**双向 site-to-site**，比本场景的单向需求更难
- 要点：那两种解释讲的不是同一件事——反方讲「去程进不去 `tailscale0`」，测试讲「整体链路能通」；把这一层说破，读者就不会被两边绕晕
- 要点：读者可能观察到的界面差异——不同版本下 UI 显示的值与文档写的不一致（第 5 章给校验方法）
- 要点：**引用纪律**——本篇不引用任何未核验来源、不转述其内容；尤其是网上流传的那条「HAOS 同网段不能跨段转发」的求助帖，经核实并不含该结论，不得作为证据出现
- 素材引用：P2-S05、P2-S07、P2-S09、P2-S11、P2-S15（sources/15_github_com.md）

### 4.5 同网段专属警告：别把同一个 LAN 上的其他 Linux 节点搞成非对称路由

- 要点：为什么这一节专门给同网段场景——你 advertise 的 `192.168.1.0/24` 正是 HAOS 自己所在的网段，这个网段上如果还有别的装了 Tailscale 的 Linux 节点，它们会同时看到「本机 LAN 路由」和「peer 广播的子路由」两条路
- 要点：失效现象（照实描述，不做机制断言）——设备用 tailnet IP 能访问，但用普通 LAN IP 访问不了，从局域网内 ping 100% 丢包
- 要点：机制——入包走 LAN，回包被 Tailscale 的路由表抢走改走 `tailscale0`，一去一回路径不同，即非对称路由
- 要点：**诚实标注**——「HAOS 自带一条更高优先级的本地路由保护规则」这一说法目前**只有一个非官方个人博客来源**，未获官方印证；正文可描述「HAOS 侧通常有保护」，但不得写成官方结论
- 要点：可行的自查手段（用第 7 章统一的排错口吻）——`ip route get <目标> from <源>` 看回包会不会走 `tailscale0`
- 要点：**本场景的正确做法**——你自己的 HAOS 上保持 `accept_routes: false`（4.2 已配）；真正要操心的是同一网段上的**其他** Linux 节点，以及让上游路由器参与转发时可能出现的回程路径问题
- 要点：给读者的取舍——家用单点需求下，最省事的做法就是「HAOS 保持 accept_routes 关闭 + 不给同一网段的其他 Linux 节点装 Tailscale」；真要装，再按上面的自查手段处理
- 素材引用：P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）、P2-S03

## 第 5 章 在远程客户端上接收路由

- 篇幅：约 700 字
- 素材引用：P2-S03（sources/13_tailscale_com.md）、P2-S04（sources/12_tailscale_com.md）
- 代码/配置示例：shell 命令块三个——`tailscale set --accept-routes`、`tailscale set --accept-routes=false`、`tailscale debug prefs`（看 `RouteAll`）；无 YAML
- 学习目标：读者能在任意一台远程客户端上确认路由被接受，并知道自己的平台默认是开还是关

### 5.1 路由注入的四个条件

- 要点：① 子路由节点 advertise ② 管理端 approve ③ 控制面把路由放进下发给客户端的 network map ④ 客户端 accept
- 要点：四条是「与」的关系，缺哪一条的表现都是「配了没生效」；客户端不会去 ping 路由器来发现路由
- 要点：官方明确的常见误解——ACL / grants 不注入路由。有路由没 ACL → 包进隧道被丢；有 ACL 没路由 → 包根本不进隧道。两者都要有
- 素材引用：P2-S03

### 5.2 各平台默认值不一样，Linux 最容易踩

- 要点：Windows / macOS / Android / iOS / tvOS 默认接受子路由；Linux 默认不接受
- 要点：这意味着「手机一配就通、Linux 服务器死活不通」大概率不是 HAOS 的问题
- 素材引用：P2-S03、P2-S04

### 5.3 客户端上怎么打开，以及那条校验命令

- 要点：图形界面里对应 `Use Tailscale subnets` 开关，取消勾选就是不接受
- 要点：命令行对应 `tailscale set --accept-routes`，关闭用 `--accept-routes=false`
- 要点：校验命令 `tailscale debug prefs` 看 `RouteAll` 是否为 true——这也是第 1 章留下的「以实际生效值为准」的兑现方式
- 素材引用：P2-S03、P2-S04

## 第 6 章 验收：你自己跑一遍六步

- 篇幅：约 900 字
- 素材引用：P2-S03（sources/13_tailscale_com.md）、P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S02（sources/14_tailscale_com.md）、P2-S05（sources/11_tailscale_com.md）
- 代码/配置示例：shell 命令块——`tailscale status --json`、`tailscale ip -4`、`tailscale ping <hostname-or-ip>`、`tailscale debug prefs`、客户端侧 `ping 192.168.1.50`；无 YAML。另附一张验收记录表（Markdown 表格，非代码）
- 学习目标：读者能独立判定自己的部署成没成，并把结果记录下来；失败时知道带着哪些信息进第 7 章

### 6.1 把测试环境摆对

- 要点：测试端必须是真正在家庭网络之外的 tailnet 客户端（手机关掉 Wi-Fi 走蜂窝最省事）
- 要点：目标设备要选一台明确没有装 Tailscale、且平时能从家里电脑 ping 通的设备（打印机、摄像头、路由器管理页面都可以）
- 要点：先把目标 IP 记下来，后面每一步都用同一个 IP，避免变量
- 素材引用：P2-S02、P2-S05

### 6.2 六步验收清单，按顺序执行

- 要点：第 1 步 在子路由节点上确认已经在 advertise（`tailscale status --json`），并记下 `tailscale ip -4` 便于后面 `tailscale ping`
- 要点：第 2 步 在管理端确认路由已 approve（对应第 4.3 节）
- 要点：第 3 步 在客户端确认已 accept routes，Linux 尤其注意（`tailscale debug prefs` 看 `RouteAll`）
- 要点：第 4 步 从客户端 `tailscale ping` 通 HAOS 的 tailnet IP —— 先证明隧道本身通
- 要点：第 5 步 从客户端 ping 局域网目标 IP —— 这才是子路由的最终验收
- 要点：第 6 步 反过来确认「路由器自身能访问目标设备」，把问题限定在转发链路上而不是目标设备本身
- 素材引用：P2-S03、P2-S02、P2-S01

#### 6.2.1 警告③：HAOS 主机自己不走隧道，是设计不是故障

- 要点：读者一定会发现的现象——在 HA 终端里访问 `192.168.1.x` 并不经过隧道，看到路由像没生效
- 要点：官方语义——当本地子网与 tailnet 里的子路由冲突时，本地网络访问优先，这些地址不会被送往 tailnet；目的是防止 HA 自己失联
- 要点：所以子路由的收益对象是**远程 tailnet 设备**，不是 HA 主机自己；代价是无法用同网段做负载均衡与故障转移
- 素材引用：P2-S01

### 6.3 把结果记下来

- 要点：验收表字段建议——节点名、是否 advertise、是否 approve、客户端平台、是否 accept、隧道是否通、局域网 IP 是否通、失败时停在第几步
- 要点：诚实声明——本篇结论由官方文档 + 维护者在**两种 HAOS 部署形态**上的实测背书，但维护者测的是**双向 site-to-site**、不是你这套同网段单向场景；请仍以你自己的实测为准，而不是期待「必定成功」
- 要点：验收不通过就直接进第 7 章，按顺序查，不要回头乱改 SNAT
- 素材引用：P2-S03、P2-S08

## 第 7 章 排错：按顺序查，别猜

- 篇幅：约 1200 字
- 素材引用：P2-S03（sources/13_tailscale_com.md）、P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S02（sources/14_tailscale_com.md）、P2-S08（sources/06_github_com.md）、P2-S11（sources/09_github_com.md）、P2-S06（sources/03_github_com.md）、P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）
- 代码/配置示例：shell 命令块——`ip route` / `netstat -rn`、`tailscale debug netmap`（看 `PacketFilter`）、`tailscale status --json`、`tailscale debug prefs`、`tailscale set --accept-routes`、`tailscale ping`、`ha dns info` / `ha dns reset` / `ha dns restart`；YAML 片段两处——`log_suppression: false`、`always_use_derp: true`
- 学习目标：读者遇到「路由不通」时能按固定顺序定位到具体一环，而不是反复改 SNAT 或去跑 `sysctl`

### 7.1 路由根本没出现在客户端的路由表里

- 要点：按官方顺序查：节点是否 advertise（管理端或 `tailscale status --json`）→ 是否 approve → Linux 上 `tailscale debug prefs` 的 `RouteAll` 是否为 false（是则 `tailscale set --accept-routes`）→ 是否有更具体的本地路由抢了优先级（`ip route` / `netstat -rn`）
- 要点：提醒这是第 5 章四条件的前三条，先别怀疑 HAOS
- 素材引用：P2-S03

### 7.2 路由在、隧道也通，但目标不通

- 要点：用 `tailscale debug netmap` 看 `PacketFilter` 段确认 ACL / grants；确认目标从子路由节点本机可达；检查路由器或目标设备上的防火墙
- 要点：把「路由控制哪些包进隧道」和「访问控制决定哪些包被放行」明确分开讲
- 素材引用：P2-S03

### 7.3 路由和 ACL 是两套东西

- 要点：给出反直觉的两个例子——advertise 了 `10.0.0.0/8` 但没有对应 grant，客户端拿到路由但流量被丢；grant 允许 `192.168.0.0/16` 并不会额外注入任何路由
- 要点：把这一节定位成「避免在错误的地方改配置」
- 素材引用：P2-S03、P2-S02

### 7.4 HAOS 特有的坑

#### 7.4.1 key 过期导致 fail-close

- 要点：连接器 key 过期后，路由在其他设备上仍然保留但不可达，这是官方有意为之的 fail-close；预防办法是关闭该节点的 key 过期，或配置高可用
- 要点：排查时把「最近有没有到期/重认证」当成一条固定检查项
- 素材引用：P2-S02

#### 7.4.2 排错前先关掉日志压制

- 要点：`log_suppression` 默认开启，200 行之后开始压日志；排错时应先设成 `false`，因为 Tailscale 日志很啰嗦，线索就藏在里面
- 要点：给出 YAML 片段
- 素材引用：P2-S01

#### 7.4.3 `sysctl` 报 `Read-only file system`（警告① 的报错现场）

- 要点：把第 4.2.1 的结论在这里兑现成排查动作——看到这个报错不是配置错误，是路径错误：不该在 HAOS 上做这一步
- 要点：明确「不要为了绕过只读而去找 remount 之类的野路子」，插件已经代做
- 素材引用：P2-S08、P2-S01

#### 7.4.4 DNS loop 会让 `hassio_dns` 崩溃

- 要点：现象——MagicDNS 解析不了时不返回 REFUSED/SERVFAIL/NXDOMAIN，而是回头去问系统原本的 DNS（在 HA 上就是 `hassio_dns`），形成 loop 后 `hassio_dns` 崩溃，连带 supervisor、nginx 一起出问题（引用 coredns `plugin/loop` 日志原文）
- 要点：`accept_dns: false` 不是解法（会让控制台下发的全局 nameserver 也失效）；维护者早前「干脆全局关 MagicDNS」的结论次日被自己推翻，因为会影响 Ubuntu / Win11 客户端的解析
- 要点：插件停止时配置在 HA 里的 `100.100.100.100` 会被跳过、不会导致 DNS 全挂（维护者已实测）——把这条作为安抚性结论给出
- 要点：用 `ha dns info` 确认 `servers: []`，需要清空时 `ha dns reset` + `ha dns restart`
- 素材引用：P2-S06、P2-S01

### 7.5 四种常见误判，以及一个不要当步骤的「怪招」

- 要点：误判一——把 exit node 当子路由用（子路由只暴露指定网段，exit node 接管全部出站，配置位置与授权位置都不同）
- 要点：误判二——把 HAOS 主机本地优先当故障（回到 6.2.1，这是设计）
- 要点：误判三——**局域网内的 Linux 节点自己掉线**：症状是「tailnet IP 通、LAN IP 不通、局域网内 ping 丢包」，这不是 HAOS 的问题，是那个节点接受了子路由后回包走了 `tailscale0`（回到 4.5）。排查命令 `ip rule show` / `ip route show table 52` / `ip route get <目标> from <源>`；判定标准是 `ip route get` 对局域网目标返回了 `tailscale0` 而不是 `eth0` / `wlan0`
- 要点：误判四——让**上游路由器**参与转发时，出向（LAN→tailnet）能通但回包丢失（回程包走路由器，而去包是子路由节点直接发给非 Tailscale 设备的），这多半是路由器/防火墙问题，不是 HAOS 的问题
- 要点：现象与解释——「能 ping 通但网页卡死」多半是上游丢弃 UDP，先查 `41641/udp` 与端口转发，再考虑 `always_use_derp: true` 兜底（给出 YAML 片段，并保留官方「基本上你不会想开它」的口径）
- 要点：把「先启用再关闭 `userspace_networking` 才生效」的记录标注为社区个案、官方已 closed as not planned，只作为现象记录，不作为操作步骤
- 素材引用：P2-S01、P2-S02、P2-S11、P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）

## 第 8 章 边界、未核验声明与下一步

- 篇幅：约 500 字
- 素材引用：P2-S01（sources/08_raw_githubusercontent_com.md）、P2-S02（sources/14_tailscale_com.md）、P2-S07（sources/04_github_com.md）、P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）
- 代码/配置示例：一行反面示例 `--snat-subnet-routes=false` 与所需回程路由条目（`100.64.0.0/10` → 子路由器 LAN IP），明确标注「本文场景不要执行」；无其他 YAML
- 学习目标：读者清楚自己的需求属于哪一档，知道什么时候才需要进入 site-to-site，也知道本篇哪些结论还缺一手实测

### 8.1 什么时候才需要关 SNAT

- 要点：三个门槛——要双向、跨多个网段、两端都要能主动发起；这才叫 site-to-site
- 要点：代价清单——关 SNAT、确保不走 userspace、在各处补 `100.64.0.0/10` 回程路由；对单点需求是明确的过度工程
- 要点：给出「不要执行」的反面示例，让读者对成本有直观认识
- 素材引用：P2-S01、P2-S02、P2-S07

### 8.2 本篇的边界与未核验声明

- 要点：明确不在本篇范围的能力——exit node、Taildrop、Taildrive、多站点对比
- 要点：口径分歧声明——对「HAOS 同网段转发能力」存在社区与官方不一致的说法；本篇只陈述**已核实**的反方依据与维护者的实测，不引用未核验来源、不转述其内容
- 要点：结论强度声明——本篇给的是「官方文档 + 维护者在树莓派实机与 VirtualBox 两种 HAOS 部署上的实测」支撑的可执行路径，并明确指出维护者测的是双向 site-to-site；验收请以第 6 章你自己跑出来的结果为准
- 要点：单一来源声明——第 4.5 节提到的「HAOS 自带本地路由保护规则」只有个人博客一个来源，未获官方印证，读者按需自行核实
- 素材引用：P2-S01、P2-S02、P2-S14（sources/16_docs_dev-eric_work.md）、P2-S15（sources/15_github_com.md）

### 8.3 下一步

- 要点：一句对照链接——同主题的 `tailscale-usage`（通用使用）与 `tailscale-subnet-router-fnos`（fnOS + Docker 部署）作为不同部署形态的参照，本篇只给链接不展开
- 要点：可选延伸方向——把远程客户端也纳入 tailnet、给 HA 之外的服务用 Serve 暴露（对应第 3.3 节）
- 素材引用：P2-S01、P2-S05

## 学习路径说明

### 前置要求

- 一台已经跑起来的 HAOS，能进 Settings 界面，知道自己的局域网网段（本篇按 `192.168.1.0/24` 写，其他网段直接替换）
- 一个 Tailscale 账号，以及一台不在家庭网络里的测试设备（手机即可）
- 不需要 WireGuard、路由表、SNAT 这些网络知识，本篇遇到才解释

### 学完能做什么

- 从外网用 tailnet IP 或域名 + HTTPS 访问家里的 Home Assistant，不开端口、不做反代
- 让远程 tailnet 设备访问 `192.168.1.0/24` 里不装 Tailscale 的设备（打印机、摄像头、路由器等）
- 独立完成一遍六步验收，并在失败时按顺序定位到 advertise / approve / accept / ACL / key / DNS 中的具体一环
- 知道哪些广为流传的做法（`sysctl`、关 SNAT）在本场景是错的，以及错在哪

### 建议学习顺序

1. 第 1 章 结论前置（约 10 分钟）——先建立判断力，避免照着网上教程走弯路
2. 第 2 章 安装授权（约 15 分钟）——动手
3. 第 3 章 内网穿透（约 20 分钟）——先拿到「能远程访问 HA」这个确定的成果
4. 第 4 章 子路由配置 + 控制台授权（约 30 分钟）——本篇核心，配置改完记得重启插件
5. 第 5 章 客户端接收路由（约 10 分钟）——换到远程设备上操作
6. 第 6 章 六步验收（约 15 分钟）——必须做，本篇的结论强度依赖你自己的实测
7. 第 7 章 排错（验收不过时才读）——按小节顺序查，不要跳着改配置
8. 第 8 章 边界与下一步（约 5 分钟）——确认自己有没有走到 site-to-site 的必要
