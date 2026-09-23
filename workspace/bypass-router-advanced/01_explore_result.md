# 旁路由进阶使用 - 阶段 1 探测结果

> 工作流：learning-note-flow ｜ 运行：bypass-router-advanced
> 阶段：P1 探测式收集 ｜ 日期：2026-09-23
> 上游：`00_intent.md`（主线 A 原理深化 / B 配置进阶 / D 功能扩展，精通型）

## 一、探测范围与方法

三路并行 subagent 探测，各带独立 lens：

| Lens | 覆盖 | 产出候选数 |
|------|------|-----------|
| L1 配置进阶 | 透明代理接管、DHCP 下发、DNS 分层、分流规则、IPv6、防火墙/NAT、多出口 | 8 |
| L2 排错实战 | 非对称路由、网关互指、DHCP 冲突、DNS 泄漏、IPv6 泄漏、conntrack 疑难、硬件加速、环路/MTU | 8 |
| L3 原理与扩展 | 转发路径与 SNAT、三种接管模式、网关指向配法、DNS 架构、高可用、功能扩展、方案对比、可观测性 | 8 |

去重标准：canonical URL 去重；同主题不同表述合并取信息量最大者。

## 二、来源核对结果（本阶段最重要的产出）

**背景**：探测确认「旁路由」这一层没有权威单一文档，OpenWrt / mihomo / MosDNS 官方只覆盖到组件层。因此本阶段对将作为章节锚点的来源逐条做了可达性核对，**推翻了两条错误引用**。

### ✅ 已核对通过（Tier 1 官方）

| ID | 来源 | 核对结论 | 检索日 |
|----|------|---------|--------|
| S1 | `xtls.github.io/document/level-2/transparent_proxy/transparent_proxy.html` | 存在。标题「透明代理入门」，Project X 文档。明确给出 iptables-redirect「已过时，不建议使用」的判断，正文以 tproxy 为主线讲 PREROUTING 链、策略路由、标记录由、OUTPUT 环回规避，并指出 ipv6 需换 ip6tables | 2026-09-23 |
| S2 | `doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html` | 存在。iStoreOS 官方「旁路由最佳实践」。给出 6 种方案：手动静态 IP、旁路由 DHCP、（华硕）浮动网关、（iStoreOS）浮动网关、（iStoreOS 分身）浮动网关，并附方案对照表 | 2026-09-23 |
| S3 | `wiki.metacubex.one/config/inbound/` | 存在。mihomo 官方「入站配置」。透明代理与系统接管一类下含 Redirect / TProxy / TUN 三个 listener 条目 | 2026-09-23 |
| S4 | `irine-sistiana.gitbook.io/mosdns-wiki/` | 存在。项目作者 namespace 下的 mosdns 官方 wiki（非第三方镜像），自我描述仅一句「一个 DNS 转发器」，分 v5 / v4 文档 | 2026-09-23 |
| S5 | `openwrt.org/docs/guide-user/base-system/dhcp` | 存在。官方「DHCP and DNS configuration /etc/config/dhcp」。含 `dhcp_option` 条目，原文示例 `"3,192.168.1.1 6,192.168.1.1" to give out gateway and DNS server addresses` | 2026-09-23 |
| S6 | `openwrt.org/docs/guide-user/network/wan/multiwan/mwan3` | 存在。官方 mwan3 文档，最后修改 2026/07/25。明确为 **iptables 版**，并指向独立的 **nftables 版**文档页 | 2026-09-23 |
| S7 | `github.com/istoreos/istoreos/issues/2066` | 存在，Open 状态，2025-01-17 创建。含三个问题，其中第 2 点（忽略 DHCP 后客户端仍被下发旁路由网关）与本笔记相关 | 2026-09-23 |
| S8 | `wusiyu.me/openwrt-bypass-gateway-tcp-not-work/` | 存在。标题「备忘：OpenWrt在旁路由下Ping通但TCP不通的解决办法」。归因 conntrack 未正确追踪二段式连接，解法为关闭「丢弃无效数据包」+ WAN Zone 允许 invalid。**作者自注机制「有待进一步验证」** | 2026-09-23 |

### ❌ 核对不通过，已废弃（探测阶段的错误引用）

| 原引用 | 问题 | 处置 |
|--------|------|------|
| `openwrt.org/docs/guide-user/base-system/dnsmasq` | 页面**不存在**（官方 wiki 返回 "This topic does not exist yet"），是空页而非 dnsmasq 文档 | 废弃。DHCP option 3/6 改用 S5 + `.../dhcp_configuration` |
| `github.com/dl12345/mwan3`（作为 mwan3 官方 README） | 仓库确实存在，但只是 `openwrt-25.12` 的 nftables 移植分支，非权威源；`/blob/master` 路径 404 | 废弃。改用 S6 官方文档 |

### ✅ 已核对通过（Tier 2 社区一手实践，需与 Tier 1 交叉印证）

| ID | 来源 | 核对结论 |
|----|------|---------|
| S9 | `chonglangbiji.com/guide/openwrt-bypass-router-gateway-dns-transparent-proxy-2026/` | 存在。标题「OpenWrt 旁路由新手教程：网关、DNS、DHCP 和透明代理 2026 \| 排查清单」，作者「程屿」，标注 2026-04-19 / 更新 2026-05-24。核心方法论：先固定基础网络再开透明代理 |
| S10 | `koolcenter.com/t/topic/14218` | 存在。标题「使用VRRP实现高性能浮动网关实现秒级自动切换」。iStoreOS 旁路由作 MASTER(priority 150) + 华硕 AX86U 作 BACKUP(100)，`virtual_router_id 50`，实测故障切换 |
| S11 | `cnblogs.com/airoot/p/18718858` | 存在（旁路由必要设置，MASQUERADE 相关） |
| S12 | `blog.hellowood.dev/posts/openwrt-tag-specific-device-bypass-gateway-dns/` | 存在（用 DHCP tag 指定部分设备走旁路网关） |
| S13 | `blog.isyyo.com/posts/mutual_point_architecture/` | 存在（互指架构：主路由 WAN 从旁路由取 IP） |
| S14 | `blog.rickyel.org/tool/tailscale/openwrt-pve-self-hosted-tailscale-derp` | 存在（OpenWrt + PVE + Tailscale DERP 与旁路由全方案） |
| S15 | `github.com/giuliomagnifico/openwrt-nlbwmon-prometheus-collector` | 存在（nlbwmon → Prometheus 采集） |
| S16 | `github.com/K3ndaar/OpenWRT-Keepalived` | 存在（OpenWrt keepalived 配置参考） |

### ⚠️ 社群材料（Tier 3，只用于佐证现象，不引用结论）

恩山 `right.com.cn`（masquerade 规则讨论、旁路由奇难杂症、IPv6 最优解、flow offloading 讨论）、V2EX（旁路由故障、单臂路由、mihomo vs sing-box）、Chiphell（IPv6 共存、处理器选型）、什么值得买、知乎。

**明确排除**：CSDN 问答/文库类内容（含 SEO/AI 生成痕迹与无出处数据，如「73.6% 用户」），只可用于佐证现象存在。

### 🔴 已发现的来源分歧（必须在笔记中并列标注，不得单取一方）

| 分歧点 | 一方结论 | 另一方结论 |
|--------|---------|-----------|
| TUN vs TProxy 性能 | DeepWiki 表格显示 TUN 明显占优（除 sing-box auto_redirect 外其余组合效率相当） | 安卓实践者认为开 GSO 后差异不大 |
| 网关「互指」的定义 | 社区常说「主路由与旁路由 LAN 网关互设」 | iStoreOS 官方口径：真正的问题是**主路由 DHCP 下发旁路由网关**，并非两边 LAN 网关互设 |
| redirect 模式 | 仍在教程中广泛使用 | S1（Project X 官方）明确判定 iptables-redirect「已过时，不建议使用」 |
| mwan3 文档版本 | — | S6 官方同时存在 iptables 版与 nftables 版两份文档，配置语法不通用 |

## 三、方向菜单（P1 交付物）

按用户已确认的三条主线重组，并标注与已有笔记的边界。

### 主线 A：原理深化线（地基，建议最先写）

| 编号 | 方向 | 核心问题 | 主锚点来源 | 建议篇幅 |
|------|------|---------|-----------|---------|
| A1 | 旁路由流量为什么绕一圈 | 单网口旁挂、终端网关指向它、上行经它转发，下行为何断 | S1、S11、S13 | 中 |
| A2 | 三种接管模式的数据路径 | REDIRECT（nat/仅 TCP/SO_ORIGINAL_DST）vs TProxy（mangle/IP_TRANSPARENT/支持 UDP）vs TUN（L3 虚拟网卡） | **S1、S3** | 大 |
| A3 | 非对称路由与 MASQUERADE | 为什么必须 SNAT、什么情况不需要、代价（多层 NAT、NAT 类型退化、硬加速失效） | S8、S11、S2 | 大 |
| A4 | 硬件加速为何让代理静默失效 | flow offloading / ECM / SFE 让已建立连接绕过 netfilter/NFQUEUE | 恩山 tid 8406263（T3） | 中 |

### 主线 B：配置进阶线

| 编号 | 方向 | 核心问题 | 主锚点来源 | 建议篇幅 |
|------|------|---------|-----------|---------|
| B1 | DHCP option 3/6 + tag 精细化下发 | 用 tag 只让部分设备走旁路由，替代逐台手改 | **S5**、S12 | 中 |
| B2 | 网关指向的三档配法与故障域 | 手动静态 / 主路由 DHCP 下发 / 旁路由接管 DHCP，各档的故障边界 | **S2、S7**、S9 | 大 |
| B3 | DNS 分层架构与防泄漏 | dnsmasq + AdGuardHome + MosDNS 抢 53、FakeIP vs redir-host、链路归属 | **S4** | 大 |
| B4 | 分流规则体系 | geosite/geoip 库与远程 rule-set 两条独立管线、规则顺序、GEOIP 兜底误伤 | mihomo 文档（T1，待 P2 补锚点） | 大 |
| B5 | IPv6 旁路由（横切议题） | IPv4 走代理 IPv6 直连的根因（RA/RDNSS 独立下发通道） | 待 P2 补 | 大 |

### 主线 D：功能扩展线

| 编号 | 方向 | 核心问题 | 主锚点来源 | 建议篇幅 |
|------|------|---------|-----------|---------|
| D1 | 多出口与故障转移 | mwan3 的 Interface/Member/Policy/Rule 四层模型；策略路由 ≠ 带宽叠加 | **S6** | 大 |
| D2 | 浮动网关高可用 | VRRP/keepalived 做 VIP 秒级漂移；ARP 缓存滞后是固有局限 | **S10、S16**、S2 | 中 |
| D3 | 可观测性与性能边界 | nlbwmon 按主机审计、NAT 与加解密的 CPU 瓶颈、N100 级选型 | S15 | 中 |

### 贯穿性小节（不单独成线，按用户 P0 决定并入各章）

- **排错方法论**：单变量分层排查、tcpdump/conntrack/nft/ip route get 工具链、一次只改一个变量层
- **来源可靠性说明**：本笔记为何必须多来源交叉印证（官方只覆盖组件层）

## 四、覆盖缺口（P2 需补齐）

| 缺口 | 说明 | 优先级 |
|------|------|--------|
| B4 分流规则官方锚点 | 探测只拿到二手教程站（clashhelp/clashfaq/chonglangbiji），缺 mihomo 官方 rule-provider 文档锚点 | 高 |
| B5 IPv6 官方锚点 | 仅有社区帖与 V2EX/Chiphell 讨论，缺 odhcpd / RA 的官方文档锚点 | 高 |
| D3 性能数据 | 缺可引用的实测吞吐数据，只有定性描述与选型讨论 | 中 |
| A4 硬加速机制 | 缺 OpenWrt 官方关于 flow offloading 与 NFQUEUE 交互的文档锚点 | 中 |
| MosDNS 配置锚点 | S4 是 wiki 首页，需下钻到具体的转发器/分流配置页 | 中 |

## 五、P2 工作量估算

- **核心来源**：约 12–16 条（Tier 1 官方 7–9 条 + Tier 2 实践 5–7 条）
- **需下钻抓取的页面**：S1、S2、S3、S5、S6 及其 nftables 版、S9、S10，加上第四节 4 个缺口的补齐来源
- **预计产出**：`02_deep_research.md` 含来源表、claim/source 映射、矛盾并列、实践指引、开放问题
- **抓取环境**：需先探测 `crawl4ai` 环境（`bash scripts/crawl.sh --help`），必要时 `bash scripts/setup.sh` 引导

## 六、待用户确认

1. 第三节方向菜单中，A1–A4 / B1–B5 / D1–D3 共 12 个方向，**哪些进笔记、哪些砍掉**？
2. B5（IPv6）是否保留？它在 P0 已被标注为横切议题，会显著增加篇幅。
3. 是否需要保留「贯穿性小节」中的排错方法论单独成节？
