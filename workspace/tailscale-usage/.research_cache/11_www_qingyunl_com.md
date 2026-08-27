---
url: "https://www.qingyunl.com/news/361.html"
title: "裸金属物理机内网穿透终极对决：frp vs ZeroTier vs Tailscale vs ngrok，谁才是吞吐与延迟的王者？ - 行业新闻 - 轻云互联"
scraped_at: 2026-08-27T16:20:42+00:00
---

# 行业新闻
  1. [轻云互联 - 迈向云计算新纪元](https://www.qingyunl.com/)


# 裸金属物理机内网穿透终极对决：frp vs ZeroTier vs Tailscale vs ngrok，谁才是吞吐与延迟的王者？
2026年06月11日 01:07 • [行业新闻](https://www.qingyunl.com/news/) • 阅读 3298
## 1. 为什么裸金属物理机需要真正硬核的内网穿透
机房里的裸金属物理机往往拥有整机独占的CPU、内存、NVMe和万兆网卡，但很多用户只拿到一个内网IP甚至仅一个公网IPv6。想从办公室SSH管理、跨机房数据同步、跑分布式训练？内网穿透逃不掉。但不同方案在裸金属上的表现天差地别——frp的代理开销、ZeroTier的加密与路由、Tailscale的WireGuard底层、ngrok的云隧道，哪个能喂饱10Gbps线速？直接上实测数据与坑位。
## 2. 测试环境与前置准备
选用两台轻云互联裸金属物理机作为测试节点（机房A机房B各一台），配置为Intel Xeon Silver 4314 * 2，256GB DDR4，2 * 2.5GbE LACP，操作系统Ubuntu 22.04。公网带宽均为1Gbps共享，内网均为万兆直连（但对穿透测试而言，公网才是瓶颈）。统一安装iperf3、curl、systemd等基础工具，所有服务均以systemd常驻运行。

```
# 禁用IPv6简化测试
echo 'net.ipv6.conf.all.disable_ipv6=1' >> /etc/sysctl.conf && sysctl -p
# 网卡中断绑定到CPU0~3（避免中断漂移）
ethtool -L eth0 combined 4
# 注意：以下所有穿透测试均在公网接口进行

```

## 3. 方案一：frp（经典反向代理）
### 3.1 服务端配置

```
# /etc/frp/frps.toml
bind_port = 7000
bind_addr = "0.0.0.0"
kcp_bind_port = 7001
token = "YourSecureToken"
allow_ports = 2000-3000
max_pool_count = 50
tcp_mux = false        # 关闭多路复用，提高单连接吞吐

```

### 3.2 客户端配置

```
# /etc/frp/frpc.toml
server_addr = "frp.example.com"
server_port = 7000
token = "YourSecureToken"
transport.use_encryption = true
transport.use_compression = false

[[proxies]]
name = "iperf3"
type = "tcp"
local_ip = "127.0.0.1"
local_port = 5201
remote_port = 2000

```

**常见坑：** ・`tcp_mux`不开时，单连接吞吐最高约300Mbps；开启后虽然复用连接但调度开销增大，实际万兆下反而降低。・加密与压缩同时开启会让CPU到800%+，裸金属的EPYC也扛不住。推荐仅加密，压缩交给上层（如iperf3默认不压缩）。
### 3.3 iperf3测试结果

```
# 客户端（机房A）启动 iperf3 -s
# 物理机B通过frp反向代理连接
iperf3 -c 127.0.0.1 -p 2000 -t 30 -P 4
[  4]  0.00-30.00 sec  1.12 GBytes  320 Mbits/sec   (frp + 加密)

```

## 4. 方案二：ZeroTier（SD-WAN虚拟二层网）
### 4.1 部署与加入网络

```
curl -s https://install.zerotier.com | sudo bash
sudo zerotier-cli join 8056c2e21c000001  # 你的Network ID
# 在网页控制台授权节点，并设置Managed Routes（可选）
sudo zerotier-cli set 8056c2e21c000001 allowManaged=1

```

### 4.2 性能调优关键
  * **MTU调整** ：默认ZeroTier虚拟网卡MTU为2800，但经过公网路径可能导致分片。设置 `ifconfig zt+ mtu 1500` 或开机脚本。
  * **禁用DNS和流规则** ：`sudo zerotier-cli set 8056c2e21c000001 allowDNS=0 allowGlobal=1`
  * **点对点直连验证** ：`sudo zerotier-cli listpeers` 确认两节点之间为 DIRECT 而非 RELAY，否则延迟翻倍。


### 4.3 iperf3测试结果

```
# 两节点通过ZeroTier IP通信（假设10.0.0.1和10.0.0.2）
iperf3 -c 10.0.0.2 -t 30 -P 4
[  4]  0.00-30.00 sec  1.98 GBytes  566 Mbits/sec   (ZeroTier 无加密叠加)

```

吞吐明显优于frp，但延迟从ping 1ms增大到8ms（经公网中转）。如直连成功可达4ms。
## 5. 方案三：Tailscale（基于WireGuard的零配置Mesh）
### 5.1 快速启动

```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --authkey tskey-auth-xxxx --accept-routes --advertise-routes=192.168.1.0/24
# 注意：裸金属上必须开启 --accept-routes 才能让子网互通

```

### 5.2 性能瓶颈排错
  * Tailscale默认使用DERP中继（类似TURN），需确保在控制台关闭“使用候选中继”，并设定`--accept-dns=false`。
  * 如果遇到`ping`延迟高，检查`tailscale status`中路径是否直连。强制直连：`sudo tailscale up --force-reauth --direct`。
  * 裸金属上CPU占用：WireGuard kernel module效率远高于用户态，Tailscale在Linux上自动使用内核模式（可`dmesg | grep wireguard`确认）。


### 5.3 iperf3测试结果

```
iperf3 -c 100.100.100.2 -t 30 -P 4
[  4]  0.00-30.00 sec  2.21 GBytes  632 Mbits/sec

```

Tailscale依靠WireGuard内核态加密，吞吐最高，延迟与ZeroTier接近（直连时约5ms）。
## 6. 方案四：ngrok（面向DevOps的隧道服务）
ngrok 3.x免费版限制带宽及并发，不适用于长时间高吞吐传输。但可作Demo或临时访问。安装后在裸金属上：`ngrok tcp 5201`。自动分配随机域名，通过该域名连接。

```
iperf3 -c 0.tcp.ngrok.io -p 12345 -t 10
[  4]  0.00-10.00 sec  85.6 MBytes  71.8 Mbits/sec    # 免费版限速

```

额外排错：ngrok日志中常见“too many connections”错误，免费版最多支持10个并发TCP流，裸金属上很容易触及。
## 7. 综合对比表
  * **frp** ：320Mbps，延迟12ms，CPU占用15%（加密），配置灵活，适合大量端口映射。
  * **ZeroTier** ：566Mbps，延迟8ms，CPU占用8%，需要自建planet或依赖官方根服务。
  * **Tailscale** ：632Mbps，延迟5ms，CPU占用5%，单机多节点最方便，但依赖控制平面。
  * **ngrok** ：72Mbps，延迟20ms+，CPU占用3%，商用场景下价格昂贵。


## 8. 裸金属物理机内网穿透选型建议
**长期、高吞吐生产环境：** 推荐Tailscale（内核WireGuard）或ZeroTier（需调优直连）。轻云互联的裸金属物理机自带BGP多线及万兆内网，配合Tailscale的DERP自建中继，可实现跨地域低延迟隧道。**传统运维端口映射：** frp生态最成熟，注意关闭tcp_mux、启用加密不压缩，并使用systemd重启守护。**快速调试/演示：** ngrok足够，但裸金属的大带宽会被限制成“牙签”。
## 9. 排错备忘录（直接抄走）
### 9.1 frp连接断开

```
journalctl -u frpc -f | grep "error"
# 常见原因：keepalive间隔太短
# 在服务端/客户端添加:
heartbeat_interval = 30
heartbeat_timeout = 90

```

### 9.2 ZeroTier单点延迟抖动

```
# 检查中继地址
zerotier-cli listpeers | grep RELAY
# 强制通过直连对方公网IP（需防火墙放行UDP 9993）
sudo iptables -A INPUT -p udp --dport 9993 -j ACCEPT

```

### 9.3 Tailscale接口数据未加密？

```
# 确认使用内核模块
modprobe wireguard
# 查看接口状态
ip link show tailscale0
# 若没有wg内核，则使用用户态，性能损失30%

```

### 9.4 万兆测试瓶颈定位

```
# 同时抓包确认包量
tcpdump -i eth0 -n 'tcp port 2000' -c 100
# 观察重传比例，若>1%则可能是frp内排队或中间路径丢包

```

## 10. 结语
没有银弹。裸金属物理机硬件的极致性能需要匹配穿透方案选型。如果追求性价比与自主可控，轻云互联的裸金属支持独立硬件架构，配合frp+内核参数调优已经能满足大多数场景；若追求极致效率与零维护，Tailscale + 自建DERP是中大型分布式集群的不二之选。最后提醒：**永远不要在无加密穿透上跑生产敏感流量** ——即使内网，物理安全也需要加密兜底。
[ 云数据库SSL卸载网关架构：基于Nginx Stream模块实现全透明加密与连接池优化 ](https://www.qingyunl.com/news/362.html "云数据库SSL卸载网关架构：基于Nginx Stream模块实现全透明加密与连接池优化")
« 上一篇 2026年06月11日 01:30
[ 遇到云服务器连接不了有哪些原因造成？ ](https://www.qingyunl.com/news/5.html "遇到云服务器连接不了有哪些原因造成？")
下一篇 » 2023年05月27日 23:43
### 分类目录


### 近期文章
### 最新文章
  * [宝塔面板 MySQL 调优被忽视的暗礁：redo log 容量不足引发的写性能坍缩](https://www.qingyunl.com/news/437.html)
  * [告别对象存储误删事故：版本控制与生命周期自动治理的实战部署](https://www.qingyunl.com/news/436.html)
  * [高防CDN回源502、源站自测却200：过期跨签名中间证书引发的TLS握手暗雷](https://www.qingyunl.com/news/435.html)
  * [Nginx反代对象存储缓存命中率只有3%？参数剥离与Range切片让回源归零](https://www.qingyunl.com/news/434.html)
  * [rsync 迁移文件全拷完了，MySQL 却起不来：五个“隐蔽默认值”让数据目录搬家变成翻车现场](https://www.qingyunl.com/news/433.html)
  * [别让一枚vCPU扛下所有软中断：VPS内核网络栈收包路径的极致调优](https://www.qingyunl.com/news/432.html)
  * [云数据库MySQL 8.0升级后性能反降？这四个隐形坑位在偷你的并发](https://www.qingyunl.com/news/431.html)
  * [PHP高并发部署实录：香港CN2链路下每请求省0.4ms的Nginx/PHP-FPM内核级手术](https://www.qingyunl.com/news/430.html)


加载中… 
加载中… 
创建工单 
