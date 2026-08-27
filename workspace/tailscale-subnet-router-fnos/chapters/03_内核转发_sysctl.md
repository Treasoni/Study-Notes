# 第三章 宿主机内核转发——sysctl 开启 IP forwarding

> 子网路由器的本职是"把包从 tailnet 转发进内网"，这一步由宿主机内核完成。本章开启并验证内核转发。

## 本章要解决什么问题

容器起来了、Tailscale 认证了，但外网 ping 内网设备仍不通。高频原因：**宿主机内核默认不允许转发 IP 包**。Linux 开关 `net.ipv4.ip_forward` 默认是 0，而子网路由器正是靠它把从 `tailscale0` 进来的包转到内网网卡（来源 S1, S11）。

> [!tip] 大白话
> 内核转发像大楼的**货运电梯**，默认锁着。隧道把包裹送到大楼门口（tailscale0），电梯不开，包裹到不了内网。sysctl 就是开电梯的钥匙。

## 3.1 写入 sysctl 配置

持久化写入，重启不丢。新建 `/etc/sysctl.d/99-tailscale.conf`：

```ini
# /etc/sysctl.d/99-tailscale.conf
net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```

- `net.ipv4.ip_forward = 1`：必开，IPv4 转发总开关。
- `net.ipv6.conf.all.forwarding = 1`：可选，仅当要通告 IPv6 子网。
- 无 `/etc/sysctl.d/` 时，同样内容写进 `/etc/sysctl.conf`（来源 S1, S11）。

## 3.2 加载并验证

```bash
sysctl -p /etc/sysctl.d/99-tailscale.conf   # 立即加载
sysctl net.ipv4.ip_forward                  # 期望：net.ipv4.ip_forward = 1
cat /proc/sys/net/ipv4/ip_forward           # 期望：1
```

`/etc/sysctl.d/` 配置开机自动加载，属持久化设置。

## 3.3 没开转发的表现

- `tailscale up` 提示子网路由/出口节点功能**要求开启 IP forwarding**（来源 S11）。
- 数据面：客户端能 ping 通 100.x 网关（隧道通），但包到路由器后被拒转发，打不开内网任何设备。

> [!tip] 大白话
> "能 ping 通 100.x 网关"只说明隧道修到了楼下，不代表电梯（转发）开了。转发开没开，直接看 `sysctl net.ipv4.ip_forward` 是不是 1，别靠猜。

> [!warning] 症状重叠提醒
> "转发未开"和"FORWARD DROP"（第 4 章）症状几乎相同：首跳通、内网不通。排错先确认 `sysctl net.ipv4.ip_forward = 1`，再查 FORWARD 链，两步都要做。

## 本章小结

- 子网路由器必须开内核 IP 转发（来源 S1, S11）。
- 持久化写法：`/etc/sysctl.d/99-tailscale.conf` 写 `net.ipv4.ip_forward = 1`。
- `sysctl -p` 加载，`sysctl net.ipv4.ip_forward` 验证。
- 未开转发症状与 FORWARD DROP 重叠，排错两者都查。

转发开关开了，但 Docker 的 FORWARD 链还在"锁门"。下一章处理防火墙放行与 NAT。

**参考来源**：S0 用户草稿 · S1 Tailscale KB: Subnet routers · S11 Tailscale IP forwarding 排错页。
