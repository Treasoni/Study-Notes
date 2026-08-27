## 生态对比与排错

功能都配通了，接下来三个问题绕不开：Tailscale 跟 frp、ZeroTier、ngrok 比到底快多少？直连打洞失败时会怎样？出了问题怎么定位？本章先给出一组实测数据回答「怎么选」，再讲清打洞与 DERP 回退的机制，接着给一套可直接照做的排错流程，最后盘点免费版限制。

### 4.1 四工具实测对比与选型

以下数据来自**单一测试环境**（裸金属 1Gbps 公网、iperf3 测速）的实测[^c4-1]，仅作选型参考：

| 工具 | 实测带宽 | 延迟 | CPU 占用 | 关键限制与备注 |
|---|---|---|---|---|
| frp | 320 Mbps | 12ms | 15% | 加密+压缩同开会打爆 CPU，建议仅加密 |
| ZeroTier | 566 Mbps | 8ms | 8% | 默认 MTU 2800 需改 1500 |
| Tailscale | 632 Mbps | 5ms | 5% | 裸金属需 `--accept-routes` |
| ngrok | 71.8 Mbps | 20ms+ | — | 免费版 ≤10 并发，易触发 too many connections |

> [!warning] 单一测试环境，结论只作选型参考
> 这是同一台裸金属服务器、同一网络的单次实测[^c4-1]，数值会随网络、设备与版本变化。真正选型时，最好在自己的链路上用同样的方法各跑一遍。

几点值得注意：frp 在加密与压缩同时开启时 CPU 飙到 15%，实测建议**只开加密**；ZeroTier 默认 MTU 2800 在多数公网链路会被分片拖慢，要改成 1500（改完用 `zerotier-cli listpeers` 确认 `DIRECT`）；Tailscale 是四者中**综合表现最高**的——632Mbps 带宽、5ms 延迟，CPU 占用反而最低（5%），Linux 上默认走内核态 WireGuard，若内核模块不可用而退回用户态实现，性能约降 30%[^c4-1]。带宽与吞吐的影响因素可参考 [[内网穿透带宽性能分析]]。

选型建议[^c4-1]：

- **生产高吞吐** → Tailscale 或 ZeroTier，两者 P2P 直连，吞吐远高于中继方案；
- **传统大量端口映射** → frp，思路直观、控制力强；
- **快速调试/临时暴露** → ngrok，零配置开箱即用，但免费版并发与带宽都受限。

想自己复测，iperf3 命令参考（对端为 tailnet 内设备）：

```bash
# 对端（服务器）启动服务端
iperf3 -s

# 本机发起测速，-t 指定时长
iperf3 -c 100.x.y.z -t 30
```

### 4.2 打洞机制与 DERP 回退

Tailscale 并不保证一上来就是直连。连接建立时，节点**默认从 DERP 中继起步**——先用它交换对端端点与 WireGuard 公钥，同时并行探测直连路径，两条路径选最优；一旦打洞成功，就**无缝切换为直连**，后续流量走端到端加密的 WireGuard，中继不再参与[^c4-2]。

> [!note] 直连优先，DERP 仅回退
> 官方口径是「优先直连、DERP 仅回退」[^c4-2]。看到 `relay "sea"` 不代表系统「偏爱」中继，只是此刻直连还没成功或已失败。典型环境下官方称直连成功率超过 90%[^c4-2]。

> [!tip] 大白话：直连 vs 中继
> 把直连打洞想成「两户人家窗户对窗户，喊话直达」；DERP 中继想成「楼道里站个传话人」。能直达就直达，传话人只在喊不通时兜底——所以看到 `relay "sea"` 不是故障，只是暂时没人能直达而已。

这里有个易误解点：打洞与回退的状态机是**被动检测**，不是「等一个超时就强制切换」[^c4-2]。系统持续观察路径质量，检测到更优的直连就立即升级，不会主动打断当前连接。官方**没有暴露任何「打洞/回退超时」参数，不可用户调节**；社区偶有「可调超时」的说法，以官方口径为准，不采用[^c4-2]。

打洞失败主要有三类原因[^c4-2]：

- **对称 NAT**：每次连接都换出站端口，无法预测，最难穿透；
- **多层 NAT**：家庭路由器叠加运营商 NAT，端点映射层层嵌套；
- **严格防火墙**：如 UniFi 默认拦截 UDP，直接断掉打洞通道。

> [!warning] UDP 失败是「沉默」的
> UDP 打洞失败**不会有任何错误报文返回**，系统只能靠超时或对端确认来判定失败[^c4-2]。排查时别干等报错——走了中继不代表故障，可能只是打不通直连。

缓解思路：尽量用支持端点独立映射（Endpoint-Independent Mapping）的路由器、加大 UDP 会话数上限、在拓扑中保留一个稳定 UDP 节点或 Peer Relay，关键链路直接走专线或强制 TCP 443[^c4-2]。

### 4.3 排错流程

遇到「设备在线却连不上 / 访问很慢」，按下面四步定位[^c4-3][^c4-4]。

**第一步：`tailscale status` 看走没走中继**

```bash
tailscale status
```

设备状态列若出现 `relay "sea"`，说明流量正经过 DERP（`sea` 是西雅图中继的代码）；没有 relay 行、状态列为 direct 的才是直连[^c4-3]。

```text
# 示意：第 5 列 relay "sea" = 走中继；"-" = 直连
100.101.102.103  device-a   user@   linux    -
100.101.102.104  device-b   user@   windows  relay "sea"
```

**第二步：`tailscale ping` 判别直连还是中继**

```bash
tailscale ping --until-direct device-b   # 直连成功后立即停止（默认 true）
tailscale ping --c=5 device-b            # 只探测 5 次（默认最多 10 次）
```

输出 `via DERP(sea) in 242ms` = 中继；`via 1.2.3.4:1234 in 8ms` = 已打通直连[^c4-3]。

**第三步：`tailscale netcheck` 检查底层网络**

```bash
tailscale netcheck
```

重点看 UDP 一栏：若为 `false`，说明当前网络**无法 P2P 打洞**，流量只能回落加密 TCP 中继；同时该命令会报告最近的 DERP、NAT 映射方式（UPnP / NAT-PMP / PCP）与 HairPinning 支持情况[^c4-4]。

**第四步：对照常见坑检查**

- **ACL 误配**：规则只允许 A→B，反向未放行；
- **子网路由未审批**：`--advertise-routes` 广播了，但 admin console 没勾选审批；
- **exit node 流量路径**：自定义 ACL 后忘记加 `dst: ["autogroup:internet"]`；
- **key 过期**：认证密钥过期后 advertised routes 会 fail close，宁可断流量也不泄漏[^c4-3]。

仍定位不了，用 `tailscale bugreport` 生成一份带 `BUG-` 标识符的诊断包，发给官方或社区[^c4-4]。

### 4.4 免费版限制盘点

免费版 Personal 的关键边界[^c4-5]：

- **单 tailnet 最多 6 个免费用户**，支持节点分享（node sharing）；
- 设备数上限官方免费页未写死，**以 Pricing 页为准**——旧「100 设备」的说法已废弃，不要信。

付费专属能力（免费版用替代方案即可）[^c4-5]：

- **端口级 ACL**：免费版 ACL 目标只能写 Any / IP / CIDR / Group / User / Tag 等粒度，指定端口与协议是 Premium/Enterprise 专属；
- **ssh 检查模式（checkPeriod）**：免费版 SSH 规则用 `accept` 放行即可，周期性校验是付费功能。

> [!tip] 免费版够用判断
> 个人 6 用户以内、不需要按端口精细授权、SSH 不需要「每次检查」——免费版基本够用，不必急着升级。

另有两条折扣/免费路径[^c4-5]：符合 OSI 协议的开源项目可申请 **Community 免费版**（需 GitHub 认证，不能走 Billing 自助开通）；慈善、非营利与教育机构可享 **50% 折扣**。

### 本章小结

- 四工具实测（单一环境）：Tailscale 综合表现最高（带宽最大、CPU 最低）；frp 适合大量端口映射、ngrok 适合快速调试。
- Tailscale 连接默认从 DERP 起步，并行探测直连，成功即无缝切换；状态机是被动检测，超时参数不可调。
- 打洞失败主因是对称 NAT、多层 NAT 与严格防火墙；UDP 失败「沉默」，只能靠超时判定。
- 排错四步：`status` 看 relay code → `ping` 判别直连/中继 → `netcheck` 查 UDP/NAT → 核对 ACL、路由审批、exit node、key 过期。
- 免费版：单 tailnet 6 用户 + 分享；端口级 ACL 与 ssh checkPeriod 是付费功能。

下一章进入进阶用法：policy 的 tags/groups、Headscale 自建控制面、自建 DERP 与容器/K8s 集成——当免费版或官方中继满足不了你时，这些就是解药。

## 参考来源

[^c4-1]: 裸金属内网穿透对决：frp vs ZeroTier vs Tailscale vs ngrok — https://www.qingyunl.com/news/361.html
[^c4-2]: Tailscale UDP 打洞失败检测与中继回退状态机 — https://blog.hotdry.top/posts/2026/02/19/tailscale-udp-hole-punching-failure-detection/
[^c4-3]: Tailscale Docs：Troubleshoot DERP traffic routing — https://tailscale.com/docs/reference/troubleshooting/network-configuration/derp-routing
[^c4-4]: Tailscale Docs：tailscale CLI reference — https://tailscale.com/docs/reference/tailscale-cli
[^c4-5]: Tailscale Docs：Free pricing plans — https://tailscale.com/docs/account/manage-plans/free-plans-discounts
