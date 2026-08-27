# 第四章 防火墙放行与 NAT——iptables 规则

> 第 3 章转发开关负责"内核允许转发"，本章负责"防火墙放行 + 回程路径"。同时交代两个易混淆 issue：#12407 二次 NAT 与 #13754 链顺序。

## 4.1 根因回顾：Docker 的 FORWARD DROP

Docker 启动时自动开启 ip_forward，并把 **FORWARD 链默认策略设为 DROP**（来源 S8）。虽用 host 网络（Docker 不为 host 网络建规则，来源 S8），但 FORWARD 默认策略被改 DROP 仍生效，`tailscale0` → 内网网卡的转发被丢。

Docker 提供 `ip-forward-no-drop: true`（daemon.json）阻止改默认策略，但 fnOS 定制版未必暴露入口（待实机确认）。

## 4.2 基线修复（用户草稿方案）

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

## 4.3 进阶：DOCKER-USER 链外科手术式放行

官方推荐把自定义规则放进 **DOCKER-USER** 链而非全局改默认策略，因为 Docker 管理 FORWARD 但保留 DOCKER-USER 给用户放自定义规则（来源 S8）。

```bash
iptables -I DOCKER-USER -i tailscale0 -o eth0 -j ACCEPT   # 入向：tailscale0 → 内网（eth0 换成实际网卡）
iptables -I DOCKER-USER -i eth0 -o tailscale0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT  # 回向
```

> [!warning] 网卡名要换
> `eth0` 是示例，须换成 fnOS 实际内网网卡名（`ip addr` 查）。DOCKER-USER 只放行指定方向，比全局 ACCEPT 更收敛（来源 S8）。

## 4.4 同宿主二次 MASQUERADE（#12407）

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

## 4.5 ts-forward 链顺序（#13754）

**症状**：客户端能建隧道，但子网流量时通时断，或重启后必现故障。

**根因**：Tailscale 与 Docker 同机时，`ts-forward` 须排在 FORWARD 链中 **Docker 规则之前**，否则 Docker 的 DROP 先命中。先起容器再 `tailscale up` 可规避大部分顺序问题（来源 S9）。

**运维修复**：`ExecStartPost` 脚本把 `ts-input`/`ts-forward` 移到链尾，核心是"确认存在 → 删除 → 追加"（来源 S9）：

```bash
iptables -C FORWARD -j ts-forward && iptables -D FORWARD -j ts-forward   # 先确认再删
iptables -A FORWARD -j ts-forward                                         # 追加到链尾
```

## 4.6 持久化与 fnOS 防火墙后端（待实机确认）

`iptables` 命令默认只生效到下次重启。fnOS 防火墙后端（iptables 还是 nftables）及重启后规则是否保留，**尚未实机确认**。建议开机自动加载：

```bash
iptables-save > /etc/tailscale-iptables.rules     # 保存
iptables-restore < /etc/tailscale-iptables.rules  # 开机脚本恢复
```

> [!warning] nftables 后端
> 若 fnOS 用 nftables 后端，`iptables` 会被透明翻译，但 `iptables-save/restore` 持久化可能不适用（待实机确认后更新本章）。

## 本章小结

- 根因：Docker 把 FORWARD 默认策略设为 DROP（来源 S8）。
- 基线修复：`-P FORWARD ACCEPT` + `POSTROUTING MASQUERADE 100.64.0.0/10`（来源 S0）。
- 更收敛方案：DOCKER-USER 链放行（来源 S8）。
- #12407 同宿主二次 NAT：ping 通但 HTTP 超时（来源 S13）。
- #13754 链顺序：`ts-forward` 须在 Docker 规则之前（来源 S9）。
- 持久化与 fnOS 防火墙后端待实机确认。

防火墙放行、NAT 兜底完成，但路由还要在控制台批准、客户端还要开接受。下一章处理这两环。

**参考来源**：S0 用户草稿 · S8 Docker 数据包过滤与防火墙 · S9 tailscale Issue #13754 · S13 tailscale Issue #12407。
