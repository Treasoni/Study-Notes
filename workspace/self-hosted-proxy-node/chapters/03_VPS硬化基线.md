# 第三章：落地前的 VPS 硬化基线

本章回答一个问题：在第 5 章把服务端口对外暴露之前，这台 VPS 应该先处于什么状态。正确顺序是「先缩小暴露面，再放服务」——把硬化当作上线前的基线，而不是被扫到之后的补丁。

## 3.1 安全策略与风险模型

先定策略，再挑工具。Debian 手册把「风险」定义为三个问题的答案：要保护什么、要防止什么发生、谁会尝试使其发生；三者答清，策略才有落点[^c3-S10]。手册还否定「装个工具就安全」的错觉：「Security is a process, not a product」[^c3-S10]。

对单台 VPS 可归纳出三条要点。其一，**短边界优于长边界**：边界短而明确比漫长曲折的边界更好防守，敏感服务应集中在少量机器、只经最少检查点访问（据 S-10 归纳）[^c3-S10]。其二，**优先停用不需要的服务**：与其用包过滤阻止对某服务的访问，不如让服务根本不监听不该开放的接口，或直接停用、卸载不需要的服务[^c3-S10a]。其三，**包过滤只是补充而非唯一防线**：防火墙只对确实经过它的数据包有效[^c3-S10a]。

> [!tip] 大白话
> 把 VPS 想成仓库：与其在门口摆安检机（包过滤），不如先把不需要的门砌死（停用服务）。

## 3.2 防火墙 nftables

包过滤是「最少检查点」的执行者。Debian 自 Buster 起默认使用 nftables 框架，旧 `iptables` 命令已改为走 nftables 内核 API[^c3-S10a]。

与 iptables 不同，**nftables 没有默认表**，表的数量与内容都由用户自建；每张表必须且只能属于 `ip`、`ip6`、`inet`、`arp`、`bridge` 五个 family 之一，未指定时默认 `ip`[^c3-S10a]。链分两类：**base chain** 注册进 Netfilter hook，是数据包进入网络栈的入口，能看到流量；**regular chain** 不挂 hook，只能作为 `jump` 目标组织规则[^c3-S10a]。规则由「匹配表达式 + verdict」组成，verdict 取值有 `accept`、`drop`、`queue`、`continue`、`return`、`jump chain`、`goto chain`[^c3-S10a]。

持久化与开机装载：`nft` 的改动不会自动持久化，规则存于 `/etc/nftables.conf`，可用 `nft list ruleset > /etc/nftables.conf` 保存，开机装载需 `systemctl enable nftables`[^c3-S10a]。迁移路径：单条命令用 `iptables-translate` / `ip6tables-translate`，整份规则集先用 `iptables-save` 导出、再经 `iptables-restore-translate` 转换；`iptables-nft` 一类命令只作向后兼容[^c3-S10a]。

下面的最小规则集是我据 S-10a 语法自行编写的（**推断**）；S-10a 只给语法与装载方式，未提供面向 VPS 的现成规则集[^c3-S10a]。

```nft
# /etc/nftables.conf —— 推断：非手册原文，按最小开放原则编写
table inet filter {
    chain input {
        type filter hook input priority filter; policy drop;   # 默认拒绝
        ct state established,related accept   # 放行已建立连接的回包
        iif "lo" accept                        # 放行回环
        tcp dport { 22, 443 } accept           # 只开 SSH 与节点端口，按需增删
        icmp type echo-request accept          # 允许 ping
    }
    chain forward { type filter hook forward priority filter; policy drop; }
    chain output  { type filter hook output  priority filter; policy accept; }
}
```

> [!tip] 大白话
> 把 nftables 想成门禁账簿：表是账本，base chain 是站门口的门、regular chain 只是备注页，verdict 是放行 / 丢弃 / 转交。规则不写回 `/etc/nftables.conf`，重启即失效。

## 3.3 fail2ban

**定位与机制**。暴力破解的缓解思路是限制同一来源的登录尝试次数、临时封禁该 IP——这正是 Fail2Ban 的定位，它能监控任何把登录尝试写进日志的服务[^c3-S10b]。它扫描日志（如 `/var/log/auth.log`），对失败登录过多的 IP 更新防火墙规则、拒绝其新连接；开箱支持 sshd、Apache 等日志，自 v0.10 起支持 IPv6[^c3-S11]。

**能力边界**。它只能降低失败认证的速率，无法消除弱认证本身的风险（官方建议改用双因素或公私钥认证）[^c3-S11]；也无法应对分布式暴力破解（大量机器分散尝试）[^c3-S10b]。

**配置与覆盖约定**。四类配置文件都在 `/etc/fail2ban/`：`fail2ban.conf`（全局）、`filter.d/*.conf`（识别认证失败）、`action.d/*.conf`（封禁/解封命令）、`jail.conf`（filter 与 action 的组合即 jail）[^c3-S10b]。约定是**不要直接修改 `jail.conf`**，启用或配置 jail 要写进 `/etc/fail2ban/jail.d/defaults-debian.conf` 或同目录文件，以免升级被覆盖[^c3-S10b]。以 sshd jail 为例，手册默认值是 `bantime = 10m`、`findtime = 10m`、`maxretry = 5`：10 分钟内 5 次失败，封来源 IP 10 分钟[^c3-S10b]。

```ini
# /etc/fail2ban/jail.d/defaults-debian.conf —— 推断：覆盖写法示意，取值取自 S-10b
[sshd]
bantime  = 10m
findtime = 10m
maxretry = 5
```

> [!warning] 两处口径不要混用
> S-11 的 README 面向**源码安装**，讲的是复制 `init.d` 脚本、`update-rc.d` 那套步骤，且未给出任何默认 jail 数值[^c3-S11]。Debian 用 apt 包安装时，默认值与配置目录以 S-10b 为准[^c3-S10b]。两处不能混用。

## 3.4 拥塞控制 sysctl

本节只讲键名与语义，不涉及具体算法的收益。五个键都属于 `net.ipv4.tcp_*`：

| 键名 | 类型 | 语义 |
| --- | --- | --- |
| `tcp_congestion_control` | STRING | 为新连接选择拥塞控制算法；`reno` 始终可用，其他取决于内核配置；默认由内核配置阶段决定；被动连接继承监听套接字的选择[^c3-S12] |
| `tcp_available_congestion_control` | STRING（只读） | 显示已注册的可用算法；更多算法可能以模块形式存在但尚未加载[^c3-S12] |
| `tcp_allowed_congestion_control` | STRING | 显示/设置非特权进程可用的选项，是上者的子集[^c3-S12] |
| `tcp_ecn` | INTEGER | 仅当两端都表示支持时使用 ECN；让支持的路由器在丢包前发出拥塞信号；协商选出双方都支持的最高反馈变体[^c3-S12] |
| `tcp_slow_start_after_idle` | BOOLEAN | 启用时按 RFC2861 行为，空闲期（以当前 RTO 界定）后使拥塞窗口超时；关闭则空闲后不重置窗口[^c3-S12] |

切换算法的前提（**推断**）：目标算法须出现在 `tcp_available_congestion_control` 中（模块已加载）；若由非特权进程选择，还须落在 `tcp_allowed_congestion_control` 白名单内[^c3-S12]。

```ini
# /etc/sysctl.d/90-net.conf —— 推断：写入方式示意，键名与语义见上表
net.ipv4.tcp_congestion_control = <已注册的算法名>
net.ipv4.tcp_slow_start_after_idle = 0
```

> [!warning]
> 这份内核文档全文未点名 BBR，因此本节只给参数名与语义，**不做任何吞吐或延迟收益断言**[^c3-S12]。

## 小结

- 硬化先定策略：把风险模型三问答清，记住「Security is a process, not a product」[^c3-S10]。
- 最有效的一步是缩小边界：停用不需要的服务，包过滤只作补充[^c3-S10a]。
- nftables 无默认表，规则靠 `/etc/nftables.conf` + `systemctl enable nftables` 持久化，旧命令走 `iptables-translate` 迁移[^c3-S10a]。
- fail2ban 只缓解暴力破解、不消除弱认证风险；改配置写进 `jail.d/`，默认 `10m/10m/5`[^c3-S10b][^c3-S11]。
- 拥塞控制只认键名与语义；内核文档未点名 BBR，不做性能断言[^c3-S12]。

日志监控（logcheck）、文件完整性与被入侵后的处置属于「长期在线后要看的东西」，另见第 4 章。

[^c3-S10]: Debian 管理员手册，第 14 章《Security》（含 14.1 定义安全策略）。https://debian-handbook.info/browse/stable/security.html
[^c3-S10a]: 同上，14.2《Firewall or Packet Filtering》。https://debian-handbook.info/browse/stable/sect.firewall-packet-filtering.html
[^c3-S10b]: 同上，14.3《Supervision: Prevention, Detection, Deterrence》。https://debian-handbook.info/browse/stable/sect.supervision.html
[^c3-S11]: fail2ban 官方仓库 README。https://github.com/fail2ban/fail2ban
[^c3-S12]: Linux Kernel Documentation — IP Sysctl。https://docs.kernel.org/networking/ip-sysctl.html
