# 旁路由进阶使用 - 意图文件

## 基本信息

- **主题**：旁路由进阶使用（旁路由原理深化、配置进阶与功能扩展）
- **项目标识**：bypass-router-advanced
- **运行标识**：bypass-router-advanced
- **创建时间**：2026-09-23
- **当前阶段**：阶段 0
- **输出目标**：obsidian
- **Vault 路径**：/Users/zhqznc/Documents/项目
- **笔记目录**：软路由教程
- **MOC 路径**：软路由教程/软路由教程MOC.md

## 学习目标

### 笔记类型

概念 + 实战（精通型，机制与取舍优先）

### 学习深度

精通：解释每个配置背后的机制、设计取舍与失效场景，使读者能自己推导新问题，而不是照抄步骤。

### 用户基础

有基础。已把软路由（iStoreOS）配置为旁路由，能实现基础上网与转发；只掌握最基础的使用。

### 学习主线（用户多选确认）

| 主线 | 内容 | 定位 |
|------|------|------|
| A 原理深化线 | 透明代理三种接管模式（REDIRECT / TProxy / TUN）的数据路径与选型；非对称路由与 MASQUERADE/SNAT 的必要性与代价；硬件加速（flow offloading / ECM / SFE）为何让代理静默失效 | 地基，其余主线的解释基础 |
| B 配置进阶线 | DHCP option 3/6 + tag 精细化下发（部分设备走旁路由）；DNS 分层架构（dnsmasq + AdGuardHome + MosDNS + FakeIP）与 DNS 泄漏防护；geosite/geoip 与远程 rule-set 分流规则体系 | 把「怎么配」做细 |
| D 功能扩展线 | 多出口 mwan3 负载均衡与故障转移；VRRP/Keepalived 浮动网关高可用；nlbwmon 流量审计与性能边界（NAT 与加解密的 CPU 瓶颈） | 旁路由能力的边界扩展 |

未选 C 排错实战线。进阶配置天然需要排错支撑，排错内容作为各章内部小节处理，不单独成线。

### 明确排除（用户已有笔记，不重复）

| 已有笔记 | 已覆盖内容 |
|---------|-----------|
| 软路由教程/旁路由原理详解.md | 基础原理、拓扑、网关设置本质、MASQUERADE 概念、基础排错 |
| 软路由教程/iStoreOS爬梯配置指南.md | 插件对比、Passwall 安装配置 |
| 软路由教程/主流软路由系统对比与选择指南.md | 系统选型、部署模式 |
| 软路由教程/飞牛安装配置iStoreOS旁路由.md | 安装接入（已完结） |

## 研究计划

### 探索方向

planner 引导阶段已于 2026-09-23 派出三路并行 subagent 完成初步探测（配置进阶 / 排错实战 / 原理与扩展），候选方向归并为下面 8 条。该结果将在阶段 1 由 research-collector 正式归档为 `01_explore_result.md`。

1. 透明代理接管机制与数据路径
2. 非对称路由、NAT 回程与硬件加速干扰
3. DHCP 精细化下发与设备分流策略
4. DNS 分层架构与防泄漏
5. 分流规则体系（geosite/geoip 与 rule-set）
6. IPv6 旁路由与泄漏（贯穿 B 主线的横切议题）
7. 多出口、高可用与可观测性
8. 排错方法论与工具链（作为各章内部小节）

### 重点收集

- **核心概念**：非对称路由、SNAT/MASQUERADE、conntrack、fwmark 与策略路由、透明代理接管模式、FakeIP vs redir-host、RA/RDNSS、flow offloading
- **实战配置**：dnsmasq option 3/6 + tag、MosDNS/AdGuardHome 分层链路、mihomo 规则集与 rule-provider、mwan3 四层模型、VRRP 浮动网关
- **常见坑**：国外通国内不通、时通时不通、代理对路由器本机生效对客户端失效、DNS 泄漏、IPv6 绕过旁路由、双 DHCP 冲突
- **工具链**：tcpdump、conntrack-tools、nft/iptables、dig/drill、ip route get、logread、nlbwmon、vnstat
- **进阶路径**：多出口与高可用、流量审计与性能边界（N100 级选型判断）

### 信源偏好

- 官方文档：是（OpenWrt Wiki、mihomo/metacubex 文档、MosDNS Wiki、mwan3 README）
- 技术博客：是（社区一手实践文，需核对）
- 社区讨论：是（恩山、V2EX、Chiphell、OpenWrt 官方论坛、GitHub issues）
- 学术论文：否

### 信源可靠性要求（阶段 2 强制）

探测已确认一个关键事实：**「旁路由」这一层没有权威单一文档**，OpenWrt / mihomo / MosDNS 官方只覆盖到组件层，旁路由实践写法主要来自社区事实标准。因此：

1. 结论至少两个独立来源交叉印证后才写入笔记。
2. 社区口径冲突时，必须在笔记中并列标注分歧与来源，不得单取一方（已发现实例：TUN 与 TProxy 的性能优劣结论互相矛盾）。
3. CSDN 问答/文库类内容只用于佐证现象，不引用其结论（部分带 SEO/AI 生成痕迹与无出处数据）。

## 备注

- 已有同目录 MOC：软路由教程/软路由教程MOC.md，阶段 7 由 moc-organizer 追加索引项。
- 发布目标为项目根目录（同时是 Obsidian vault 根）。附件目录沿用 软路由教程/assets。
- 本笔记为新建笔记，不是对既有笔记的更新；若后续发现应改写既有笔记，改走 note-updater，不重跑本流程。
