# Linux 网络信息获取与概念 - 深度资料

收集时间: 2026-07-29
收集方式: 4 路并行 subagent 搜索 + 自身知识库补充
搜索维度: 网络概念 / 查询命令 / 配置体系 / 监控排障

---

## 第一阶段：粗筛结果汇总

### 维度 1：网络核心概念

| # | 标题 | 评分 | 来源 | 摘要 |
|---|------|------|------|------|
| 1 | 十分钟掌握网络基础四要素：IP地址、子网掩码、网关与DNS解析 | 5/5 | 教程 | IPv4 32-bit 结构、子网掩码连续1规则、网关跨子网转发、DNS域名解析 |
| 2 | Linux 数据链路层详解：以太网帧、MAC 地址、MTU 与 ARP 协议 | 5/5 | 博客 | MTU=1500、TCP MSS=1460、UDP免分片上限=1472、ARP广播请求 |
| 3 | Linux Networking & DNS Essentials | 4/5 | 教程 | 排查顺序：DNS→IP→子网掩码→路由表→网关 |
| 4 | 网络协议格式 | 以太网帧/ARP/IP/UDP/TCP 头部 | 4/5 | 教程 | TCP头=20B、UDP头=8B、以太网Type=0x0800标识IP |
| 5 | Networking Basics (KodeKloud) | 4/5 | 教程 | Socket类型=stream/dgram/raw、NAT共享公网IP、私有IP范围 |

### 维度 2：网络查询命令

| # | 标题 | 评分 | 来源 | 摘要 |
|---|------|------|------|------|
| 1 | Linux ip command 完整指南 | 5/5 | 官方/教程 | iproute2 四大子命令、JSON输出(-j)、简洁模式(-br)、邻居状态机 |
| 2 | SS Network Troubleshooting Guide | 5/5 | 社区 | ss比netstat快10-100倍、原生TCP状态过滤、RTT/cwnd查看 |
| 3 | DNS Troubleshooting with dig/nslookup/host | 4/5 | 教程 | dig+trace追踪委派链、+short简化、@指定DNS服务器 |
| 4 | Network Debugging (Arch Wiki) | 5/5 | 官方 | mtr合并ping+traceroute、逐跳丢包率/延迟/标准差、ICMP限速假阳性 |
| 5 | arp versus ip neighbour (Red Hat) | 5/5 | 官方博客 | ip neigh统一ARP+NDP、状态过滤、批量flush、ARP表溢出排障 |

### 维度 3：配置体系与工具

| # | 标题 | 评分 | 来源 | 摘要 |
|---|------|------|------|------|
| 1 | Netplan 配置指南 - Ubuntu 26.04 | 5/5 | 教程 | Netplan作为抽象层、YAML缩进2空格、优先级/runtc/etc/lib |
| 2 | Linux DNS 配置指南 - /etc/hosts/resolv.conf/nsswitch.conf | 5/5 | 教程 | nameserver最多3个、ndots:5、getent hosts测试NSS链 |
| 3 | resolvectl / systemd-resolved 手册 | 5/5 | 官方文档 | stub resolver在127.0.0.53、flush-caches刷新缓存、每接口DNS |
| 4 | nmcli 命令指南 | 5/5 | 官方文档 | connection show、device wifi connect、store配置权限600 |
| 5 | systemd-networkd 与 systemd-resolved 集成 | 4/5 | 官方 | .network文件DNS=配置、MulticastDNS=yes启用mDNS |

### 维度 4：监控与抓包

| # | 标题 | 评分 | 来源 | 摘要 |
|---|------|------|------|------|
| 1 | Linux网络接口与带宽监控详解 | 5/5 | 教程 | iftop按连接排序、nethogs按PID归因、bmon支持CSV导出 |
| 2 | Master Network Monitoring on Linux | 5/5 | 教程 | ethtool -S查CRC错误、tcpdump -C -W轮转抓包、ss -tunap |
| 3 | Replacing iwconfig with iw (Kernel.org) | 4/5 | 官方文档 | iw dev wlan0 link/link iwconfig、iw scan/iwlist scanning |
| 4 | Linux 以太网流量监控：从基础到实践 | 4/5 | 博客 | nload默认bit/s、bmon ASCII图表、/proc/net/dev底层原理 |
| 5 | How to Monitor Network Throughput on Linux | 4/5 | 博客 | >10Gbps链路优先统计型工具、iftop 2s/10s/40s移动平均 |

---

## 第二阶段：精读笔记

由于 WebFetch 无法访问部分国内站点和国外站点，以下精读内容综合了搜索结果摘要与自身知识库。

---

### 核心概念体系

#### 1. 网络分层模型与信息映射

Linux 网络信息可以按照 OSI/TCP-IP 模型分层理解：

```
应用层     →   Socket、DNS 查询           →  ss -tunap、dig
传输层     →   TCP/UDP 端口、连接状态     →  ss、netstat
网络层     →   IP 地址、路由表            →  ip addr、ip route
数据链路层 →   MAC 地址、ARP 表           →  ip link、ip neigh、ethtool
物理层     →   网卡状态、速率             →  ethtool、ip link
```

每条"信息"都属于特定层次，对应的查询命令也不同。

#### 2. IP 地址与子网掩码

- **IPv4**：32 位，分为网络位 + 主机位
- **CIDR 表示法**：`192.168.1.0/24` 表示前 24 位是网络位
- **子网掩码**：连续 1 的位掩码，如 `255.255.255.0` = `/24`
- **特殊地址**：
  - `127.0.0.0/8` - loopback（本机回环）
  - `0.0.0.0/0` - 默认路由（匹配所有地址）
  - `169.254.0.0/16` - DHCP 失败时的链路本地地址
- **私有地址范围**：`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`

#### 3. 路由表

- **默认网关**：`0.0.0.0/0` 匹配所有非特定目标，via 指向网关 IP
- **路由优先级**：最长前缀匹配（最精确的掩码优先）
- **路由来源**：直连（设备本身）、静态（手动配置）、动态（路由协议）
- **策略路由**：基于源地址、TOS 等多维度的路由选择（`ip rule`）

#### 4. TCP/UDP 与 Socket

- **TCP**：面向连接、可靠、有序，头部 20 字节，含序列号/确认号/窗口/标志位
- **UDP**：无连接、尽力交付，头部 8 字节
- **Socket**：`IP:Port` 对，`SOCK_STREAM`(TCP) / `SOCK_DGRAM`(UDP)
- **TCP 状态机**：LISTEN→SYN-SENT→ESTABLISHED→CLOSE-WAIT→TIME-WAIT→CLOSED
- **连接数限制**：由 `fs.file-max`、`net.ipv4.ip_local_port_range` 等控制

#### 5. ARP 与邻居表

- **ARP**：通过广播请求目标 IP 对应的 MAC 地址
- **邻居状态机**：
  - `REACHABLE` - 可达（正常）
  - `STALE` - 过期（仍需验证）
  - `DELAY` - 延迟验证
  - `PROBE` - 正在探测
  - `FAILED` - 不可达
  - `PERMANENT` - 静态配置永不超时
- **IPv6 使用 NDP**（Neighbor Discovery Protocol）替代 ARP

#### 6. DNS 解析

- **解析顺序**（由 `/etc/nsswitch.conf` 控制）：`hosts: files dns` 表示先查 `/etc/hosts`，再查 DNS
- **`/etc/resolv.conf`**：配置 DNS 服务器（最多 3 个 nameserver）、搜索域、ndots
- **systemd-resolved**：Ubuntu 16.04+ 默认，stub resolver 监听 `127.0.0.53`
- **DNS 记录类型**：A(IPv4)、AAAA(IPv6)、CNAME(别名)、MX(邮件)、NS(域名服务器)、TXT(文本)、SOA(区域权威)

---

### 查询命令详解

#### 1. iproute2 命令族（现代推荐）

`iproute2` 是 Linux 内核网络配置的标准工具集，已全面替代旧的 `net-tools`。

**ip link** - 网络接口层（L2）
```bash
ip link show                 # 查看所有网卡状态
ip -br link show             # 简洁模式（仅名称 + 状态）
ip link show dev eth0        # 查看指定网卡
ip -s link show eth0         # 含统计信息（收发字节/包/错误/丢包）
```
关键输出字段：`state UP/DOWN`、`mtu 1500`、`qdisc`、`mac address`

**ip addr** - 网络层（L3）
```bash
ip addr show                 # 查看所有 IP 配置
ip -br addr show             # 简洁输出（接口名 + IP）
ip addr show dev eth0        # 查看指定接口 IP
ip -j addr show eth0         # JSON 格式输出（可配合 jq 解析）
```
关键输出字段：`inet 192.168.1.100/24`、`scope global`、`dynamic`(DHCP)

**ip route** - 路由表
```bash
ip route show                # 查看路由表
ip route show default        # 查看默认路由
ip route get 8.8.8.8         # 查看到某 IP 的路由决策（策略路由）
ip -j route show             # JSON 格式
```
关键输出：`default via 192.168.1.1 dev eth0`、`/24 dev eth0 proto kernel scope link src 192.168.1.100`

**ip neigh** - 邻居表（ARP/NDP）
```bash
ip neigh show                # 查看所有邻居
ip neigh show dev eth0       # 查看指定接口的邻居
ip neigh flush all           # 清空邻居表
ip neigh add 192.168.1.5 lladdr aa:bb:cc:dd:ee:ff nud permanent dev eth0  # 静态添加
```
关键状态：`REACHABLE`、`STALE`、`FAILED`、`PERMANENT`

#### 2. ss（Socket 统计）

ss 读取 netlink 直连内核，比 netstat 快 10-100 倍。

```bash
ss -tulnp                   # 查看所有监听端口（TCP+UDP，显示进程名）
ss -tanp                    # 查看所有 TCP 连接及其状态
ss -s                       # 连接统计总览
ss -i                       # 显示 TCP 内部信息（RTT/cwnd/MSS）
ss state established        # 按状态过滤
ss '( dport = :443 or sport = :443 )'  # 按端口过滤
ss -tunap | grep 192.168.1.100         # 按 IP 过滤
```

**Recv-Q/Send-Q 排障**：
- Recv-Q > 0：应用从 socket 读取数据慢
- Send-Q > 0：对端接收慢 / 网络拥塞

**TCP 状态过滤**：
```bash
ss state time-wait           # TIME-WAIT 状态的连接
ss state close-wait          # CLOSE-WAIT（可能有泄漏）
ss state all                 # 所有状态
```

#### 3. DNS 工具

**dig** - 详细 DNS 查询（首选）
```bash
dig baidu.com                # 基本查询
dig baidu.com +short         # 简化输出
dig baidu.com +trace         # 追踪完整委派链（.→com→baidu.com）
dig @8.8.8.8 baidu.com       # 指定 DNS 服务器
dig baidu.com A              # 查 A 记录
dig baidu.com MX             # 查 MX 记录
dig -x 8.8.8.8               # 反向查询（IP→域名）
```

**nslookup** - 快速查询
```bash
nslookup baidu.com           # 基本查询
nslookup -type=MX baidu.com  # 查特定记录类型
```

**host** - 简洁查询（适合脚本）
```bash
host baidu.com               # 简洁结果
host -t MX baidu.com         # 查 MX 记录
```

**resolvectl** - systemd-resolved 管理
```bash
resolvectl status            # 查看全局和每接口 DNS 配置
resolvectl query baidu.com   # 通过 systemd-resolved 查询
resolvectl statistics        # 查看缓存命中率/DNSSEC 状态
resolvectl flush-caches      # 刷新 DNS 缓存
resolvectl dns eth0          # 查看 eth0 的 DNS 配置
```

#### 4. 网络性能与连通性工具

**ping** - 基础连通性测试
```bash
ping 8.8.8.8                 # 持续 ping
ping -c 10 192.168.1.1       # 指定次数
ping -i 0.2 baidu.com        # 200ms 间隔
```

**traceroute / mtr** - 路由追踪
```bash
traceroute baidu.com         # 传统路由追踪
mtr baidu.com                # 持续追踪（合并 ping + traceroute）
mtr -rwn baidu.com           # 报告模式（适合脚本）
mtr -c 100 baidu.com         # 100 次探测得到统计显著性
```

mtr 输出字段：`Loss%`(丢包率)、`Snt`(已发数)、`Last`(最新延迟)、`Avg`(平均延迟)、`Best`(最佳)、`Wrst`(最差)、`StDev`(标准差)

#### 5. 无线网络工具

**iw** - 现代无线管理（替代 iwconfig）
```bash
iw dev                       # 查看无线网卡
iw dev wlan0 link            # 查看连接状态（SSID、信号强度、速率）
iw dev wlan0 scan            # 扫描 AP（需要 root）
iw reg get                   # 查看无线监管区域
```

**iwconfig** - 旧版（已弃用，需 wireless-tools 包）
```bash
iwconfig                     # 查看无线配置
```

#### 6. 网卡信息工具

**ethtool** - 网卡硬件信息与统计
```bash
ethtool eth0                 # 查看网卡参数（速率、双工、自动协商）
ethtool -i eth0              # 查看驱动信息
ethtool -S eth0              # 查看网卡统计（CRC错误、丢包、冲突）
ethtool -s eth0 speed 1000 duplex full  # 强制设置速率（谨慎使用）
```

#### 7. 网络连接管理工具

**nmcli** - NetworkManager CLI
```bash
nmcli device status          # 查看所有设备状态
nmcli connection show        # 查看所有连接配置
nmcli connection show --active  # 活动连接
nmcli dev wifi list          # 扫描 WiFi
nmcli -t -f NAME,TYPE conn show  # 脚本化输出
```

---

### 网络配置文件体系

| 文件 | 用途 | 管理工具 |
|------|------|---------|
| `/etc/netplan/*.yaml` | 网络配置声明（Ubuntu） | `netplan apply`、`netplan try` |
| `/etc/network/interfaces` | 旧式网络配置（Debian） | `ifup`、`ifdown` |
| `/etc/resolv.conf` | DNS 配置（常为 symlink） | `resolvectl`(systemd-resolved) |
| `/etc/hosts` | 静态主机名→IP 映射 | 手动编辑 |
| `/etc/nsswitch.conf` | 名称解析顺序 | 手动编辑 |
| `/etc/systemd/network/*.network` | systemd-networkd 配置 | `networkctl reload` |
| `/etc/NetworkManager/system-connections/*` | NetworkManager 配置存储 | `nmcli` |

**/etc/nsswitch.conf DNS 解析顺序控制**：
```
hosts: files dns           # 先查 /etc/hosts，再查 DNS
hosts: dns files           # 先查 DNS，再查 /etc/hosts
hosts: files mdns4_minimal [NOTFOUND=return] dns  # 先查 hosts，再查 mDNS，最后 DNS
```

---

### 网络监控工具

#### 实时带宽监控

```bash
iftop -i eth0                # 按连接查看带宽
iftop -n                     # 不反解 DNS
nload eth0                   # 简洁实时流量图（默认 bit/s）
nload -u M eth0              # 以 MB/s 显示
bmon -p eth0                 # ASCII 图表 + 详细统计
```

#### 进程级流量

```bash
nethogs eth0                 # 按进程查看带宽占用
```

#### 历史统计

```bash
vnstat -i eth0               # 日/月流量统计
vnstat -l                    # 实时统计
```

---

### 抓包基础：tcpdump

```bash
# 基础用法
tcpdump -i eth0              # 监听 eth0
tcpdump -i any               # 监听所有接口
tcpdump -c 100               # 抓 100 包后退出

# 过滤表达式
tcpdump host 192.168.1.1     # 按 IP 过滤
tcpdump port 80              # 按端口过滤
tcpdump tcp                  # 只抓 TCP
tcpdump udp and port 53      # DNS 流量
tcpdump -n                   # 不反解 DNS（更快）

# 存储与读取
tcpdump -w capture.pcap      # 写文件
tcpdump -r capture.pcap      # 读文件
tcpdump -C 100 -W 10         # 轮转：每 100MB，最多 10 个

# 高级过滤
tcpdump 'tcp[tcpflags] & tcp-syn != 0'  # 只抓 SYN 包
tcpdump 'src net 192.168.1.0/24'        # 源网段
tcpdump 'icmp'                           # ICMP 包

# 输出解读
# 12:34:56.789012 IP 192.168.1.100.54321 > 93.184.216.34.80: Flags [S], seq 12345, ...
# ^            ^    ^源IP:端口        ^目标IP:端口     ^SYN标志    ^序列号
```

---

### 关键数据汇总

| 指标 | 值 | 说明 |
|------|-----|------|
| 以太网 MTU | 1500 字节 | 超过需 IP 分片 |
| TCP 头部 | 20 字节 | 不含选项 |
| UDP 头部 | 8 字节 | 固定长度 |
| TCP MSS | 1460 字节 | MTU - IP头(20) - TCP头(20) |
| UDP 免分片上限 | 1472 字节 | MTU - IP头(20) - UDP头(8) |
| MAC 地址长度 | 6 字节 (48 bit) | 如 aa:bb:cc:dd:ee:ff |
| IPv4 地址 | 4 字节 (32 bit) | 约 43 亿个 |
| nameserver 上限 | 3 个 | /etc/resolv.conf |
| ss vs netstat | 快 10-100x | netlink vs /proc |
| systemd-resolved stub | 127.0.0.53:53 | 本地 DNS 代理 |

---

### 最佳实践与常见坑

#### 最佳实践
1. **优先 iproute2**：始终使用 `ip` 和 `ss`，而非 `ifconfig`、`netstat`、`arp`
2. **排查顺序**：`ip addr` → `ip route` → `ping` → `dig` → `mtr`
3. **JSON 输出**：`ip -j` + `jq` 适合脚本解析
4. **mtr 替代 ping**：更全面，包含逐跳性能
5. **dig 替代 nslookup**：更详细，支持 `+trace`

#### 常见坑
1. **/etc/resolv.conf 被覆盖**：Ubuntu 16.04+ 由 systemd-resolved 管理，手动编辑会失效，应使用 `resolvectl`
2. **ifconfig 未预装**：Ubuntu 24.04+ 不再预装 net-tools，默认使用 iproute2
3. **netstat 慢**：生产环境有大量连接时 netstat 读取 `/proc` 很慢，始终用 `ss`
4. **nload 单位**：默认显示 bit/s 而非 Byte/s，`nload -u M` 切换
5. **tcpdump 权限**：需要 root 或 `CAP_NET_RAW`、`CAP_NET_ADMIN` 能力
6. **ARP 表溢出**：超过 `gc_thresh3` 会导致内核丢包
7. **ping 结果不可靠**：ICMP 限速可能造成假阳性，配合 mtr 交叉验证

---

### 参考链接

- [Linux ip command guide (Thomas-Krenn)](https://www.thomas-krenn.com/en/wiki/Linux_ip_command)
- [SS Network Troubleshooting Guide (GitHub)](https://github.com/ryzendev/Linux-Tips-and-Tricks/wiki/SS-Network-Troubleshooting)
- [Network Debugging (Arch Wiki)](https://wiki.archlinux.org/title/Network_Debugging)
- [arp versus ip neighbour (Red Hat)](https://www.redhat.com/en/blog/arp-versus-ip)
- [Netplan configuration guide (Ubuntu 26.04)](https://linuxconfig.org/netplan-configuration-guide-on-ubuntu-26-04)
- [resolvectl man page](https://manpages.ubuntu.com/manpages/noble/man1/resolvectl.1.html)
- [iw replacing iwconfig (kernel.org)](https://wireless.docs.kernel.org/en/latest/en/users/documentation/iw/replace-iwconfig.html)
- [Linux DNS configuration guide (/etc/hosts/resolv.conf/nsswitch.conf)](https://sadservers.com/labs/dns/guide)
- [Master Network Monitoring on Linux](https://vps.do/linux-network-monitoring/)
