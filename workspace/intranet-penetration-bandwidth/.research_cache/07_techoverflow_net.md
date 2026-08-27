---
url: "https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/"
title: "iperf3 基准测试：ZeroTier vs Netmaker vs Tailscale vs 直接交换连接 | TechOverflow"
scraped_at: 2026-08-27T14:52:14+00:00
---

[TechOverflow](https://techoverflow.net/)
在我们的设置中，运行在 XCP-NG 主机上的虚拟机连接到我的桌面（HP Z240，i7-6700 @3.4 GHz，运行 Ubuntu 22.04），在纯交换网络中使用 1Gbit 链路。两台设备都通过 MikroTik 10G 交换机（Marvell 芯片）连接
我在 VM 上运行 `iperf3 -s`，在桌面上运行 `iperf3 -c [IP 地址]`。未执行反向测试。
### 直接交换连接（无 VPN）[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#%E7%9B%B4%E6%8E%A5%E4%BA%A4%E6%8D%A2%E8%BF%9E%E6%8E%A5%E6%97%A0-vpn)
iperf_results.txt
Copy Download

```
Connecting to host 10.9.2.103, port 5201
[  5] local 10.9.2.10 port 56848 connected to 10.9.2.103 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  92.8 MBytes   779 Mbits/sec    0    444 KBytes
[  5]   1.00-2.00   sec  90.7 MBytes   761 Mbits/sec    0    543 KBytes
[  5]   2.00-3.00   sec  88.6 MBytes   743 Mbits/sec    0    816 KBytes
[  5]   3.00-4.00   sec  90.0 MBytes   755 Mbits/sec    0    816 KBytes
[  5]   4.00-5.00   sec  90.0 MBytes   755 Mbits/sec    0    856 KBytes
[  5]   5.00-6.00   sec  88.8 MBytes   744 Mbits/sec    0    946 KBytes
[  5]   6.00-7.00   sec  88.8 MBytes   745 Mbits/sec    0    946 KBytes
[  5]   7.00-8.00   sec  90.0 MBytes   755 Mbits/sec    0    993 KBytes
[  5]   8.00-9.00   sec  90.0 MBytes   755 Mbits/sec    0    993 KBytes
[  5]   9.00-10.00  sec  88.8 MBytes   744 Mbits/sec    0    993 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   898 MBytes   754 Mbits/sec    0             sender
[  5]   0.00-10.01  sec   896 MBytes   751 Mbits/sec                  receiver
```

Connecting to host 10.9.2.103, port 5201 [ 5] local 10.9.2.10 port 56848 connected to 10.9.2.103 port 5201 [ ID] Interval Transfer Bitrate Retr Cwnd [ 5] 0.00-1.00 sec 92.8 MBytes 779 Mbits/sec 0 444 KBytes [ 5] 1.00-2.00 sec 90.7 MBytes 761 Mbits/sec 0 543 KBytes [ 5] 2.00-3.00 sec 88.6 MBytes 743 Mbits/sec 0 816 KBytes [ 5] 3.00-4.00 sec 90.0 MBytes 755 Mbits/sec 0 816 KBytes [ 5] 4.00-5.00 sec 90.0 MBytes 755 Mbits/sec 0 856 KBytes [ 5] 5.00-6.00 sec 88.8 MBytes 744 Mbits/sec 0 946 KBytes [ 5] 6.00-7.00 sec 88.8 MBytes 745 Mbits/sec 0 946 KBytes [ 5] 7.00-8.00 sec 90.0 MBytes 755 Mbits/sec 0 993 KBytes [ 5] 8.00-9.00 sec 90.0 MBytes 755 Mbits/sec 0 993 KBytes [ 5] 9.00-10.00 sec 88.8 MBytes 744 Mbits/sec 0 993 KBytes - - - - - - - - - - - - - - - - - - - - - - - - - [ ID] Interval Transfer Bitrate Retr [ 5] 0.00-10.00 sec 898 MBytes 754 Mbits/sec 0 sender [ 5] 0.00-10.01 sec 896 MBytes 751 Mbits/sec receiver
### ZeroTier[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#zerotier)
iperf_zerotier_results_raw.txt
Copy Download

```
Connecting to host 10.80.246.34, port 5201
[  5] local 10.80.246.38 port 35474 connected to 10.80.246.34 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  59.9 MBytes   503 Mbits/sec  338    102 KBytes
[  5]   1.00-2.00   sec  60.2 MBytes   505 Mbits/sec  313    188 KBytes
[  5]   2.00-3.00   sec  63.9 MBytes   536 Mbits/sec  176   99.3 KBytes
[  5]   3.00-4.00   sec  74.3 MBytes   623 Mbits/sec  174    113 KBytes
[  5]   4.00-5.00   sec  67.7 MBytes   568 Mbits/sec  197   83.2 KBytes
[  5]   5.00-6.00   sec  72.5 MBytes   609 Mbits/sec  218    228 KBytes
[  5]   6.00-7.00   sec  61.3 MBytes   514 Mbits/sec  281   77.8 KBytes
[  5]   7.00-8.00   sec  72.0 MBytes   604 Mbits/sec  213   91.2 KBytes
[  5]   8.00-9.00   sec  65.4 MBytes   549 Mbits/sec  309    156 KBytes
[  5]   9.00-10.00  sec  53.9 MBytes   453 Mbits/sec  190    121 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   651 MBytes   546 Mbits/sec  2409             sender
[  5]   0.00-10.01  sec   650 MBytes   545 Mbits/sec                  receiver
```

Connecting to host 10.80.246.34, port 5201 [ 5] local 10.80.246.38 port 35474 connected to 10.80.246.34 port 5201 [ ID] Interval Transfer Bitrate Retr Cwnd [ 5] 0.00-1.00 sec 59.9 MBytes 503 Mbits/sec 338 102 KBytes [ 5] 1.00-2.00 sec 60.2 MBytes 505 Mbits/sec 313 188 KBytes [ 5] 2.00-3.00 sec 63.9 MBytes 536 Mbits/sec 176 99.3 KBytes [ 5] 3.00-4.00 sec 74.3 MBytes 623 Mbits/sec 174 113 KBytes [ 5] 4.00-5.00 sec 67.7 MBytes 568 Mbits/sec 197 83.2 KBytes [ 5] 5.00-6.00 sec 72.5 MBytes 609 Mbits/sec 218 228 KBytes [ 5] 6.00-7.00 sec 61.3 MBytes 514 Mbits/sec 281 77.8 KBytes [ 5] 7.00-8.00 sec 72.0 MBytes 604 Mbits/sec 213 91.2 KBytes [ 5] 8.00-9.00 sec 65.4 MBytes 549 Mbits/sec 309 156 KBytes [ 5] 9.00-10.00 sec 53.9 MBytes 453 Mbits/sec 190 121 KBytes - - - - - - - - - - - - - - - - - - - - - - - - - [ ID] Interval Transfer Bitrate Retr [ 5] 0.00-10.00 sec 651 MBytes 546 Mbits/sec 2409 sender [ 5] 0.00-10.01 sec 650 MBytes 545 Mbits/sec receiver
### NetMaker[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#netmaker)
Netmaker 内部使用普通（基于内核的）wireguard 连接，因此在某种程度上这是 Wireguard 性能的测试
iperf_netmaker_stdout.txt
Copy Download

```
Connecting to host 10.230.113.3, port 5201
[  5] local 10.230.113.1 port 35534 connected to 10.230.113.3 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec   105 MBytes   881 Mbits/sec    0   1.01 MBytes
[  5]   1.00-2.00   sec   104 MBytes   870 Mbits/sec   86    422 KBytes
[  5]   2.00-3.00   sec   101 MBytes   849 Mbits/sec    0    488 KBytes
[  5]   3.00-4.00   sec  98.8 MBytes   828 Mbits/sec    0    535 KBytes
[  5]   4.00-5.00   sec  98.8 MBytes   828 Mbits/sec    0    584 KBytes
[  5]   5.00-6.00   sec   104 MBytes   870 Mbits/sec    0    615 KBytes
[  5]   6.00-7.00   sec  97.5 MBytes   818 Mbits/sec    7    472 KBytes
[  5]   7.00-8.00   sec   104 MBytes   870 Mbits/sec    0    522 KBytes
[  5]   8.00-9.00   sec   101 MBytes   849 Mbits/sec    0    580 KBytes
[  5]   9.00-10.00  sec   102 MBytes   860 Mbits/sec    0    606 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec  1016 MBytes   852 Mbits/sec   93             sender
[  5]   0.00-10.00  sec  1014 MBytes   850 Mbits/sec                  receiver
```

Connecting to host 10.230.113.3, port 5201 [ 5] local 10.230.113.1 port 35534 connected to 10.230.113.3 port 5201 [ ID] Interval Transfer Bitrate Retr Cwnd [ 5] 0.00-1.00 sec 105 MBytes 881 Mbits/sec 0 1.01 MBytes [ 5] 1.00-2.00 sec 104 MBytes 870 Mbits/sec 86 422 KBytes [ 5] 2.00-3.00 sec 101 MBytes 849 Mbits/sec 0 488 KBytes [ 5] 3.00-4.00 sec 98.8 MBytes 828 Mbits/sec 0 535 KBytes [ 5] 4.00-5.00 sec 98.8 MBytes 828 Mbits/sec 0 584 KBytes [ 5] 5.00-6.00 sec 104 MBytes 870 Mbits/sec 0 615 KBytes [ 5] 6.00-7.00 sec 97.5 MBytes 818 Mbits/sec 7 472 KBytes [ 5] 7.00-8.00 sec 104 MBytes 870 Mbits/sec 0 522 KBytes [ 5] 8.00-9.00 sec 101 MBytes 849 Mbits/sec 0 580 KBytes [ 5] 9.00-10.00 sec 102 MBytes 860 Mbits/sec 0 606 KBytes - - - - - - - - - - - - - - - - - - - - - - - - - [ ID] Interval Transfer Bitrate Retr [ 5] 0.00-10.00 sec 1016 MBytes 852 Mbits/sec 93 sender [ 5] 0.00-10.00 sec 1014 MBytes 850 Mbits/sec receiver
### NetMaker[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#netmaker-1)
Netmaker 内部使用普通（基于内核的）wireguard 连接，因此在某种程度上这是 Wireguard 性能的测试
iperf_netmaker_results.txt
Copy Download

```
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  38.3 MBytes   321 Mbits/sec  389   60.0 KBytes
[  5]   1.00-2.00   sec  37.6 MBytes   315 Mbits/sec  366   43.2 KBytes
[  5]   2.00-3.00   sec  36.7 MBytes   308 Mbits/sec  431   52.8 KBytes
[  5]   3.00-4.00   sec  38.5 MBytes   323 Mbits/sec  488   80.3 KBytes
[  5]   4.00-5.00   sec  29.3 MBytes   246 Mbits/sec  356   38.4 KBytes
```

[ ID] Interval Transfer Bitrate Retr Cwnd [ 5] 0.00-1.00 sec 38.3 MBytes 321 Mbits/sec 389 60.0 KBytes [ 5] 1.00-2.00 sec 37.6 MBytes 315 Mbits/sec 366 43.2 KBytes [ 5] 2.00-3.00 sec 36.7 MBytes 308 Mbits/sec 431 52.8 KBytes [ 5] 3.00-4.00 sec 38.5 MBytes 323 Mbits/sec 488 80.3 KBytes [ 5] 4.00-5.00 sec 29.3 MBytes 246 Mbits/sec 356 38.4 KBytes
### Tailscale[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#tailscale)
此测试使用了 Tailscale 1.28.0。
在此测试期间，我确保 tailscale 连接是使用交换网络建立的，而不是通过 DERP 服务器或路由网络。
tailscale_ping_output.txt
Copy Download

```
$ tailscale ping 100.64.0.3
pong from vm (fd5d:7b60:4742::3) via 10.9.2.103:41641 in 1ms
```

$ tailscale ping 100.64.0.3 pong from vm (fd5d:7b60:4742::3) via 10.9.2.103:41641 in 1ms
### 总结[#](https://techoverflow.net/zh/2022/08/19/iperf3-jizhun-ceshi-zerotier-vs-netmaker-vs-tailscale-vs-zhijie-jiaohuan-lianjie/#%E6%80%BB%E7%BB%93)
结果：
iperf_tailscale_results.txt
Copy Download

```
Connecting to host 100.64.0.3, port 5201
[  5] local 100.64.0.2 port 40690 connected to 100.64.0.3 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  38.3 MBytes   321 Mbits/sec  389   60.0 KBytes
[  5]   1.00-2.00   sec  37.6 MBytes   315 Mbits/sec  366   43.2 KBytes
[  5]   2.00-3.00   sec  36.7 MBytes   308 Mbits/sec  431   52.8 KBytes
[  5]   3.00-4.00   sec  38.5 MBytes   323 Mbits/sec  488   80.3 KBytes
[  5]   4.00-5.00   sec  29.3 MBytes   246 Mbits/sec  356   38.4 KBytes
[  5]   5.00-6.00   sec  31.0 MBytes   260 Mbits/sec  351   86.3 KBytes
[  5]   6.00-7.00   sec  27.1 MBytes   227 Mbits/sec  287   50.4 KBytes
[  5]   7.00-8.00   sec  26.1 MBytes   219 Mbits/sec  210   46.8 KBytes
[  5]   8.00-9.00   sec  27.1 MBytes   227 Mbits/sec  261   39.6 KBytes
[  5]   9.00-10.00  sec  27.5 MBytes   231 Mbits/sec  222   40.8 KBytes
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bitrate         Retr
[  5]   0.00-10.00  sec   319 MBytes   268 Mbits/sec  3361             sender
[  5]   0.00-10.01  sec   318 MBytes   267 Mbits/sec                  receiver
```

Connecting to host 100.64.0.3, port 5201 [ 5] local 100.64.0.2 port 40690 connected to 100.64.0.3 port 5201 [ ID] Interval Transfer Bitrate Retr Cwnd [ 5] 0.00-1.00 sec 38.3 MBytes 321 Mbits/sec 389 60.0 KBytes [ 5] 1.00-2.00 sec 37.6 MBytes 315 Mbits/sec 366 43.2 KBytes [ 5] 2.00-3.00 sec 36.7 MBytes 308 Mbits/sec 431 52.8 KBytes [ 5] 3.00-4.00 sec 38.5 MBytes 323 Mbits/sec 488 80.3 KBytes [ 5] 4.00-5.00 sec 29.3 MBytes 246 Mbits/sec 356 38.4 KBytes [ 5] 5.00-6.00 sec 31.0 MBytes 260 Mbits/sec 351 86.3 KBytes [ 5] 6.00-7.00 sec 27.1 MBytes 227 Mbits/sec 287 50.4 KBytes [ 5] 7.00-8.00 sec 26.1 MBytes 219 Mbits/sec 210 46.8 KBytes [ 5] 8.00-9.00 sec 27.1 MBytes 227 Mbits/sec 261 39.6 KBytes [ 5] 9.00-10.00 sec 27.5 MBytes 231 Mbits/sec 222 40.8 KBytes - - - - - - - - - - - - - - - - - - - - - - - - - [ ID] Interval Transfer Bitrate Retr [ 5] 0.00-10.00 sec 319 MBytes 268 Mbits/sec 3361 sender [ 5] 0.00-10.01 sec 318 MBytes 267 Mbits/sec receiver
按类别查看类似文章：
如果这篇文章对您有帮助，请考虑请我喝杯咖啡或通过 PayPal 捐款，以支持 TechOverflow 上新文章的研究与发布
[ Buy me a coffee](http://buymeacoffee.com/ulikoehler)
