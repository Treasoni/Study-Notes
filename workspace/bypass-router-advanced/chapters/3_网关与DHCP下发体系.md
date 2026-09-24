# 第 3 章 网关与 DHCP 下发体系

第 1、2 章讨论包在转发路径上「被谁接管」；这一章前移一层：**客户端的网关和 DNS，究竟由谁、在什么时候、用什么机制告诉它。** 透明代理要生效，前提是客户端流量先走到旁路由上；而把流量「引」过来的动作，多数场景既不在旁路由身上、也不在接管规则里，而在 DHCP 的一行 option 里。

## 3.1 iStoreOS 官方的五种方案骨架

iStoreOS 官方文档的「主旁方案」共有 **5 个方案小节**：手动静态 IP、旁路由 DHCP、（华硕）浮动网关、（iStoreOS）浮动网关、（iStoreOS 分身）浮动网关[^c3-s2]。一个易被抹平的细节：**官方对照表只列了 4 行**，第 5 种（iStoreOS 分身浮动网关）只作独立小节存在、**未进表**[^c3-s2]——「对照表列出五种」与页面不符。本章以官方 5 方案为骨架，而非社区常见的「三档」。

| 方案 | 主路由职责 | 旁路由职责 | 关键前提 / 代价 |
|------|-----------|-----------|----------------|
| 手动静态 IP | 「任何路由器，默认开启DHCP，不需要其他任何设置」 | 「关闭DHCP」 | 每台设备**手动**指定网关/DNS；**完全不改主路由任何设置** |
| 旁路由 DHCP | 「默认关闭DHCP，网关设为旁路由IP」 | 「开启DHCP，全面接管局域网」 | 让旁路由独占 DHCP |
| (华硕)浮动网关 | 刷入 ASUSGO 改版固件的华硕路由器，默认开启 DHCP，安装「浮动网关」软件 | 搭载 iStoreOS 的设备，关闭 DHCP，安装「浮动网关」软件 | 设备侧：手动分配静态 IP、网关/DNS 设为浮动网关 IP；另经「加强版『手动指定功能』」直接为设备指定网关/DNS。**固件硬依赖**：ASUSGO 梅林改版固件「102.4及以上版本」（BE88U、BE86U、AX88U-Pro、AX86U-Pro 等，及 ROG 魔盒最新官改固件） |
| (iStoreOS)浮动网关 | 搭载 iStoreOS 的设备，默认开启 DHCP，安装「浮动网关」软件 | 搭载 iStoreOS 的设备，关闭 DHCP，安装「浮动网关」软件 | 设备侧：通过 iStoreOS 主路由上的「局域网设备管理」自由分配网关为主/旁路由/浮动网关 IP |

（表中引文出自官方文档[^c3-s2]。）其中一条常被误读：**浮动网关是按设备分配网关，而非让主副路由互设网关**[^c3-s2]——3.5 节展开。

> [!tip] 大白话
> 把「下发网关」想成老师发座位表：手动静态 IP 是各桌自己写便签；旁路由 DHCP 是换一个班长统一发；浮动网关是主路由按名字点名发。差别说到底是「谁手里握着那份座位表」。

**X5（官方并列口径）**：默认关哪一侧 DHCP，官方没有单一答案——「旁路由 DHCP」方案要求主路由关闭 DHCP，而「手动静态 IP」方案与社区教程 S9 则关掉旁路由 DHCP、由主路由统一分配[^c3-s2][^c3-s9]。两者并列，**本笔记不替你裁决**；判据见 3.5 节的「下发点」。

## 3.2 dnsmasq 的 option 3/6 与 force 语义

dnsmasq 靠 `dhcp_option` 下发 DHCP 选项。官方第一条规则是书写形式：**「The ID dhcp_option here must be with written with an underscore.」**——配置里用下划线，OpenWrt 会「translate this to --dhcp-option, with a hyphen, as ultimately used by dnsmasq.」[^c3-s5]。option 3 是网关、6 是 DNS，官方示例把两者串在一行：

```bash
# option ID 用下划线；多个 option 用空格分隔；逗号是 option 内部的分隔符
uci set dhcp.lan.dhcp_option="3,192.168.1.1 6,192.168.1.1"
uci commit dhcp
/etc/init.d/dnsmasq restart
```

若该接口已有其他 `dhcp_option` 条目、需要保留，必须改用 `uci add_list` 逐条追加，否则 `set` 会把原有条目整体覆盖。

官方对这段的说明是给它 `"3,192.168.1.1 6,192.168.1.1" to give out gateway and DNS server addresses`[^c3-s5]。两个易错点都在这一行：**option ID 用下划线**（不是 `dhcp-option`）、**多个 option 用空格分隔**（不是逗号）。

另有「强制下发」条目 `dhcp_option_force`：官方定义「Exactly the same as dhcp_option (note the underscores), but it will be translated to --dhcp-option-force」，「meaning that the DHCP option will be sent regardless on whether the client requested it.」，并注明 `dhcp_option_force available since 18.06`[^c3-s5]。**必须切开两个长得像、语义完全不同的东西：**

| 条目 | 出处 | 语义 |
|------|------|------|
| `dhcp_option_force` | S5 正式条目（since 18.06） | 把该 option **强制**下发，不管客户端是否请求 |
| `dhcp.lan.force="1"` | S5a | **跳过竞争 DHCP 检查**（pool 段里的 "force" 是另一回事） |

两者不可混用[^c3-s5][^c3-s5a]。此外，`dhcp_option_force` 在**旁路由场景**的实测行为**未找到来源支持**——标 **[未证]**。

> [!tip] 大白话
> `dhcp_option` 是「随信附说明，客户端要就给」；`dhcp_option_force` 是「不管你要不要，我都塞给你」；而 `dhcp.lan.force="1"` 是「别等别人，我自己当 DHCP 班长」。同名不同义，最容易踩坑。

## 3.3 tag 精细化下发：让部分设备走旁路由

option 3/6 是「广播式」下发；**「只让部分设备走旁路由」则要靠 dnsmasq 的 tag**。官方对此只有两句话[^c3-s5]：

| 它管什么 | 官方原文 | 说人话 |
|---------|---------|--------|
| tag 能做的事 | 「you can use the dhcp_option list to add DHCP options to be sent to hosts with this tag (or networkid).」 | 用 `dhcp_option` 列表，给「带这个 tag（或 networkid）的主机」附加 DHCP 选项 |
| tag 段本身 | 「have one configuration option: values of DHCP options to assign to this tag.」 | tag 段里只有一个可填项：要发给这个 tag 的 DHCP 选项值 |

官方把写法拆成两段：

```bash
# 1) tag 段：定义 tag 及其下发的 DHCP 选项（官方示例用 uci set）
uci set dhcp.tag1="tag"
uci set dhcp.tag1.dhcp_option="6,8.8.8.8,8.8.4.4"

# 2) host 段：先把设备固定为静态 IP，再挂到 tag 上
uci add dhcp host
uci set dhcp.@host[-1].name="mydevice"
uci set dhcp.@host[-1].mac="AA:BB:CC:DD:EE:FF"
uci set dhcp.@host[-1].ip="192.168.1.100"
uci set dhcp.@host[-1].tag="tag1"
uci commit dhcp
/etc/init.d/dnsmasq restart
```

（说明：上例中 `uci add dhcp host` 与 `name`/`mac`/`ip` 三行是为保证示例可执行、按标准 uci 用法补全，不是官方该段原文；官方该段只给出 host 侧的 `tag` 一行。）

tag 段与 host 侧的 `dhcp.@host[-1].tag="tag1"` 出自官方[^c3-s5a]。**硬前提**：必须**先给设备分配静态 IP 并添加 tag**——tag 依赖 host 条目（社区经验）[^c3-s12]；且 LuCI **没有**直接配置 tag 网关与 DNS 的选项，「需要通过命令行来配置」（社区经验）[^c3-s12]。

官方还提供 **MAC classifier**，直接按 MAC 建「带 tag 的组」：

```bash
# Use the `mac` classifier to create a tagged group.
uci set dhcp.mac1="mac"
uci set dhcp.mac1.mac="00:FF:*:*:*:*"
uci set dhcp.mac1.networkid="vpn"
uci add_list dhcp.mac1.dhcp_option="3"
uci add_list dhcp.mac1.dhcp_option="6,192.168.1.3"
uci commit dhcp
/etc/init.d/dnsmasq restart
```

这段是小节导语「Use the `mac` classifier to create a tagged group.」的示例，目的是「Disable default gateway and specify custom DNS.」[^c3-s5a]。两点须强调：一是 **`dhcp_option` 是 list 字段，这里用 `uci add_list` 而非 `uci set`**[^c3-s5a]，写成 `set` 则第二条 `6,...` 覆盖第一条 `3`，网关就没被压掉；二是**不要把「Disable default gateway」当成取值 `3` 的字段释义**，它只是该示例的目的说明，页面在选项清单里对 `3` 的释义是另一句「alternative default gateway」[^c3-s5a]。

一处**可核验的事实**：官方页面在 **tag 段**用 `uci set`、在 **MAC classifier 段**用 `uci add_list`[^c3-s5a]——两段同为 list 字段却写法不同。这是页面实况，两处**各自照抄原样、不作统一**，本笔记只记录、不为其解释原因。

再一处**这属于推断**（标 [推断]）：在 tag 段叠加 `force` 语义（想强制下发 tag 的 option）。**这是推断，没有文档锚点**——该组合语义仅由 `dnsmasq.init` 源码支撑，不要当官方保证的行为[^c3-s5a]。

客户端侧实测（社区经验）：`route -n` 默认网关变为 `10.0.0.2`，`resolvectl status eth0` 显示「DNS Servers: 10.0.0.2 1.1.1.1」，且「其他没有配置 tag 的设备依然使用主路由的网关和 DNS 地址」；tag 渲染结果为 `dhcp-option=tag:proxynode,3,10.0.0.2` 与 `dhcp-option=tag:proxynode,6,10.0.0.2,1.1.1.1`，作者解释「3 是网关地址，6 是 DNS 地址，多个 DNS 地址用逗号分隔；不同的 dhcp_option 使用空格分隔」[^c3-s12]。**这是社区经验（S12），不是官方文档。**

> [!tip] 大白话
> tag 想成「给设备贴标签、再按标签发不同说明」：慢的是先登记静态 IP 再挂标签，一把抓的是按 MAC 直接划组。`add_list` 与 `set` 的区别，就像往清单上**加一行**和**重写整张单子**——用错了，前一样东西就没了。

## 3.4 官方方案的已知反例：S7 的真实缺陷

官方方案有已知反例，且**这是 iStoreOS 官方仓库 issue 里的实测报告与维护者回帖，不是官方文档**[^c3-s7]。issue 正文记录两点：一是「istoreos利用自带的设置向导设置为旁路由时，不会自动关闭DHCP，需要手动勾选忽略此接口。」[^c3-s7]；二是即使手动勾选忽略，「即便你手动在DHCP勾选忽略此接口，但是当电脑网卡设置成自动获取IP后，IP是不会获取了，但网关会获取成istoreOS旁路由的IP。」，复测补充「发现有的电脑会获取到网关，有的不会。」[^c3-s7]

**X6（并列，不替线程收束）**：就「网关来自谁」，issue 里有两个方向、线程未收束——

| 方向 | 原文 | 归属 |
|------|------|------|
| 旁路由「仍在」下发网关 | 「网关会获取成istoreOS旁路由的IP」 | issue 发帖用户[^c3-s7] |
| 故障域归给**实际下发租约的 DHCP 服务** | 「如果istoreos的dhcp服务都关了，那你的电脑获取不到网关跟istoreos有什么关系？应该要去检查dhcp服务啊。」 | 维护者 jjm2473（Contributor）[^c3-s7] |

两方并列，**本笔记不替你裁决**；但维护者把「谁在发租约、谁才是权威」立成了判据（3.5、3.6 节展开）。

## 3.5 「主路由与旁路由 LAN 网关互设＝互指」的来源核查

社区流传：旁路由要把主路由当网关、主路由也要把旁路由当网关，两边 LAN 网关「互指」。**这条说法在本批素材中未找到来源支持，且与本批所有锚点方向相反**[^c3-s2][^c3-s9][^c3-s7]。真正的判据不是「两边怎么设」，而是**下发点在哪**：

- 官方「手动静态 IP」方案里，主路由「不需要其他任何设置」——**根本不碰主路由**[^c3-s2]。
- 社区流程 S9 的拓扑表建议主路由「保持不变」，只做旁路由侧单向指向（S9 无署名，仅作流程参考）[^c3-s9]。
- S7 维护者把故障域直接指向「实际下发租约的 DHCP 服务」[^c3-s7]。

三处指向同一条：**该关心的是客户端从哪个 DHCP 服务拿到网关，而非两个路由器的 LAN 网关是否互设成对方**。

## 3.6 下发顺序与单 DHCP 权威

以下三点来自社区教程 S9，**均为社区经验**；S9 **无署名、无发布日期**，**不得作为配置语义依据**，只用于流程与排查方法论[^c3-s9]。

**操作顺序**（与本项目 P0 一致）：「先固定旁路由 LAN IP，关闭旁路由 DHCP；再在主路由 DHCP 中下发网关和 DNS；确认普通上网正常后，最后开启透明代理插件。」[^c3-s9] 每步只引入一个变量。

**单 DHCP 权威**：「网络里同时出现两个 DHCP 服务时，客户端可能拿到随机网关，表现为有时能上网、有时不行。」[^c3-s9] 遇到「时通时不通」，先数网里有几个 DHCP 在发租约。

**三个下发层次与代价**[^c3-s9]：

| 下发层次 | 改动范围 | 代价 |
|---------|---------|------|
| 网关指向旁路由 | 设备/全局 | 「旁路由故障会影响测试设备上网」 |
| 只改 DNS | 设备/全局 | 「不是所有流量都会进旁路由」 |
| 手动单设备 | 单台设备 | 范围最小，适合先小范围验证 |

落地建议是「先只改一台电脑或手机，确认没有问题后，再通过主路由 DHCP 下发给更多设备」[^c3-s9]。

**两处未填补（如实记录，不补白）**：① **DHCP 租约续期与旁路由宕机后的故障切换行为未找到来源支持**；② **双栈网关竞争**（RA + DHCPv6 + DHCPv4 并发下发）同样**未找到来源支持**（IPv6 本轮不做，仅记录）。

> [!tip] 大白话
> 单 DHCP 权威想成「一个班只能有一个班长发座位表」：两个班长同时发，学生一会儿坐这一会儿坐那，表现就是「有时能上、有时不能」。排「时通时不通」，第一步是数清有几个发牌的。

## 小结

- iStoreOS 官方「主旁方案」共 **5 个方案小节**，但对照表**只列 4 行**，第 5 种只作独立小节存在[^c3-s2]。
- 网关与 DNS 靠 `dhcp_option` 下发：**option ID 用下划线**、**多个 option 用空格分隔**（`3` 网关、`6` DNS）[^c3-s5]；`dhcp_option_force` 与 `dhcp.lan.force="1"` 语义不同、不可混用，前者在旁路由场景的实测**未找到来源支持（[未证]）**[^c3-s5][^c3-s5a]。
- tag 实现「部分设备走旁路由」：依赖先分配静态 IP 并挂 tag、LuCI 无对应界面（社区）；MAC classifier 用 `uci add_list`（`dhcp_option` 是 list）；tag 段与 force 的组合语义**是推断**，仅由源码支撑[^c3-s5a][^c3-s12]。
- **X4** 社区「LAN 网关互指」说法**缺乏来源支持**且与锚点反向，判据是**下发点在哪**[^c3-s2][^c3-s7]；**X5** 官方并列，不裁决[^c3-s2][^c3-s9]；**X6** S7 为官方仓库实测报告与维护者回帖（非官方文档），两方未收束[^c3-s7]。

DNS 分层（B3）、分流规则（B4）与 IPv6（B5）不在本轮范围，本笔记不展开。网关设置本质与基础 MASQUERADE 概念见既有笔记 [[软路由教程/旁路由原理详解]]；iStoreOS 安装与接入见 [[软路由教程/飞牛安装配置iStoreOS旁路由]]；系统选型与部署模式见 [[软路由教程/主流软路由系统对比与选择指南]]。

下一章把「下发点」再往上扩一层：当一个主机或局域网要按策略走不同出口、并在出口故障时自动切换，mwan3 的四层模型如何表达这件事，以及它为什么不等同于带宽叠加。

[^c3-s2]: iStoreOS 官方文档《旁路由》(BypassRouter)，https://doc.istoreos.com/zh/guide/istoreos/practice/BypassRouter.html
[^c3-s5]: OpenWrt Wiki《DHCP and DNS》，https://openwrt.org/docs/guide-user/base-system/dhcp
[^c3-s5a]: OpenWrt Wiki《DHCP configuration》，https://openwrt.org/docs/guide-user/base-system/dhcp_configuration
[^c3-s7]: iStoreOS 官方仓库 Issue #2066（实测报告与维护者回帖，非官方文档），https://github.com/istoreos/istoreos/issues/2066
[^c3-s9]: 社区教程《OpenWrt 旁路由网关与 DNS 透明代理》（无署名、无发布日期，仅作流程参考），https://chonglangbiji.com/guide/openwrt-bypass-router-gateway-dns-transparent-proxy-2026/
[^c3-s12]: 社区博客《OpenWrt 按 tag 为特定设备配置旁路由网关与 DNS》，https://blog.hellowood.dev/posts/openwrt-tag-specific-device-bypass-gateway-dns/
