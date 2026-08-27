# fnOS Docker 部署 Tailscale 子网路由器 - P1 探测结果

> 运行：tailscale-subnet-router-fnos · 阶段 P1 探测式收集 · 2026-08-28
> 三个独立视角并行探测，共收集 14 条候选源（按 canonical URL 去重，`route-injection` 同时服务原理与排错两视角）。

## 一、候选来源清单

### 视角 1：fnOS 部署全流程

| # | 评分 | 来源层级 | 标题 | URL | 相关性 | 日期 |
|---|------|----------|------|-----|--------|------|
| 1 | 5 | official | Subnet routers — Tailscale 官方文档 | https://tailscale.com/kb/1019/subnets | 官方子网路由器权威指南：开启 IP 转发、`--advertise-routes` 宣告、后台批准路由的标准步骤，是各 fnOS Docker 教程的命令基础 | 持续更新 |
| 2 | 5 | primary | 飞牛上使用 Docker Compose 部署 Tailscale（飞牛官方论坛） | https://club.fnnas.com/forum.php?mod=viewthread&tid=13887 | fnOS 官方社区帖：完整 compose、host 网络、NET_ADMIN/NET_RAW、TUN 挂载、子网路由后台批准全流程 | 2025-02-07 |
| 3 | 4 | primary | Tailscale 内网穿透部署教程（飞牛论坛·徐大大） | https://club.fnnas.com/forum.php?mod=viewthread&tid=28001 | 更详细的 Docker Compose 教程：注册、Auth Key、compose、子网批准、客户端组网 | 2025-06-06 |
| 4 | 3 | community | 在飞牛NAS Docker中部署Tailscale（hiir.cn） | https://www.hiir.cn/4945.html | 第三方博客，fnOS 部署全流程 + 子网路由 + 远程访问 | unknown |
| 5 | 3 | community | 飞牛NAS(fnos)通过Docker部署Tailscale（CSDN） | https://blog.csdn.net/weixin_29214335/article/details/158248927 | CSDN 实测：compose 参数、子网宣告、常见避坑 | unknown |

### 视角 2：原理与架构

| # | 评分 | 来源层级 | 标题 | URL | 相关性 | 日期 |
|---|------|----------|------|-----|--------|------|
| 6 | 5 | official | Tailscale IP 地址概念（100.64.0.0/10 与 CGNAT） | https://tailscale.com/docs/concepts/tailscale-ip-addresses.md | 官方解释为何选用 100.64.0.0/10（RFC 6598 CGNAT）、与私有网段不冲突、内部保留段及 MagicDNS | unknown |
| 7 | 5 | official | Route injection 参考文档 | https://tailscale.com/docs/reference/route-injection | 子网路由注入四条件：宣告→审批→控制面下发→客户端 accept-routes；L3 路由与 ACL 分层 | unknown |
| 8 | 5 | official | Docker 数据包过滤与防火墙（FORWARD DROP / DOCKER-USER） | https://docs.docker.com/engine/network/packet-filtering-firewalls/ | Docker 官方明确 FORWARD 默认 DROP、DOCKER-USER 链、`ip-forward-no-drop`，是容器内子网路由被阻断的根因 | unknown |
| 9 | 4 | primary | tailscale/tailscale Issue #13754：FORWARD 链顺序错误 | https://github.com/tailscale/tailscale/issues/13754 | Docker 28 下 ts-forward 排在 DROP 之后导致路由失效，社区解法（移到 DOCKER-USER） | unknown |
| 10 | 4 | community | How Tailscale Works（God Mode） | https://god.ad/learn/how-tailscale-works | 社区深度文：控制面/数据面分离、CGNAT 寻址、NAT 穿透与 DERP 中继 | unknown |

### 视角 3：验证与排错深化

| # | 评分 | 来源层级 | 标题 | URL | 相关性 | 日期 |
|---|------|----------|------|-----|--------|------|
| 11 | 5 | official | Troubleshoot IP forwarding（Tailscale 官方） | https://tailscale.com/docs/reference/troubleshooting/network-configuration/ip-forwarding-errors-advertise | 官方排错页：ip_forward 未开、FORWARD 链与转发失败，直接对应「tracert 第一跳通但打不开内网网页」 | unknown |
| 12 | 5 | primary | tailscale/tailscale Issue #9605：TS_ROUTES 参数文档错误 | https://github.com/tailscale/tailscale/issues/9605 | 官方 issue 解释 `invalid subnet route`（末尾逗号产生空字符串）的报错与正确写法 | unknown |
| 13 | 5 | primary | tailscale/tailscale Issue #12407：同宿主机流量被二次 MASQUERADE | https://github.com/tailscale/tailscale/issues/12407 | 目标与 Tailscale 同宿主机时被 mark 0x40000 二次 MASQUERADE 丢弃，ping 通但 HTTP 超时，与 fnOS Docker 场景高度吻合 | unknown |
| 14 | 3 | community | TUN device busy（hassio-addons app-tailscale #392） | https://github.com/hassio-addons/app-tailscale/discussions/392 | 社区实操：宿主机已有 tailscaled 时 Docker 内实例报 `TUN device tailscale0 is busy`，`lsof /dev/net/tun` 杀进程或换 tun 名 | unknown |

> 注：`route-injection`（#7）同时是验证「路由是否批准/下发」的依据，两视角共用。
> 补充观察（未单列）：`luizmoreiradev/tailscale-router` 镜像说明指出原生 Tailscale 镜像不自动装 FORWARD/MASQUERADE 规则，Docker 子网路由需手动补规则 —— 与你草稿中 iptables 两步完全对应。

## 二、方向菜单

请选择 P2 深度收集的方向（可多选）：

- **A. 全部深挖（推荐）** — 三视角均衡：全流程 + 原理 + 排错，产出最完整
- **B. 侧重部署全流程** — 以 fnOS 实操步骤为主线（视角 1 + 必要排错）
- **C. 侧重原理与架构** — 深挖 overlay / CGNAT / NAT 转发机理（视角 2）
- **D. 侧重验证与排错深化** — 深挖 tailscale CLI 验证与坑位（视角 3）

> 与你 P0 确认的「补充重点：原理与架构 + 验证与排错深化」对应，推荐 A 或 C+D。

## 三、覆盖缺口

1. **页面正文未逐页复核**：本环境 WebFetch 被网络策略拦截，各条目的标题/摘要/URL 来自搜索引擎结果相互印证，未编造；P2 精读时再尝试抓取，失败则以摘要 + 明确来源归属为准。
2. **fnOS 专属细节偏少**：官方 Tailscale/Docker 文档不含 fnOS 专属操作（飞牛 Docker 界面、`/etc/sysctl.d` 写入方式），需以飞牛论坛两帖为主源补全。
3. **日期信息稀疏**：多数官方页未标注发布/更新日期，P2 记录时将标注检索日期 2026-08-28。
4. **同宿主机场景**：#12407（二次 MASQUERADE）与 fnOS 上「Docker 内跑 Tailscale + 访问同宿主服务」场景强相关，但搜索结果未给完整复现步骤，P2 需重点精读该 issue。

## 四、P2 范围估计

- **核心精读源（4-6 条）**：#1、#7、#8、#11（官方四件套）+ #12、#13（两条关键 issue）+ #2/#3（fnOS 主源）按所选方向取舍。
- **产出**：`02_deep_research.md`，含来源表、主张↔来源映射、冲突点、实践指引、未决问题与下游交接。
- **预计采集主张数**：全流程 8-12 条，原理 6-10 条，排错 8-12 条。
