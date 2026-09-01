---
url: "https://wiki.metacubex.one/en/config/proxies/"
title: "Common fields - mihomo docs"
scraped_at: 2026-08-29T08:38:58+00:00
---

#  [Common Fields](https://wiki.metacubex.one/en/config/proxies/#common-fields)[¶](https://wiki.metacubex.one/en/config/proxies/#common-fields "Permanent link")  
| 
```



























```
 | 
```
proxies:
-name:"ss"
type:ss
server:server
port:443
ip-version:ipv4
udp:true
interface-name:eth0
routing-mark:1234
tfo:false
mptcp:false

dialer-proxy:ss1

smux:
enabled:true
protocol:smux
max-connections:4
min-streams:4
max-streams:0
statistic:false
only-tcp:false
padding:true
brutal-opts:
enabled:true
up:50
down:100

```
 |  
| --- | --- |  
Proxy nodes are written as an array.
Required, proxy name. Must be unique.
Required, proxy node type.
Required, proxy node server (domain/IP).
Required, proxy node port.
##  [ip-version](https://wiki.metacubex.one/en/config/proxies/#ip-version)[¶](https://wiki.metacubex.one/en/config/proxies/#ip-version "Permanent link")
IP version used by outbound proxy connections. If the proxy is not `direct`, this affects which IP address is used when `server` is a domain name.
Available values: `dual`/`ipv4`/`ipv6`/`ipv4-prefer`/`ipv6-prefer`. Default: `dual`.
  * `ipv4`: use IPv4 only.
  * `ipv6`: use IPv6 only.
  * `ipv4-prefer`: prefer IPv4. For TCP, dual-stack resolution is performed and connections are raced, but IPv4 connections are preferred. For UDP, dual-stack resolution is performed and the first IPv4 result is used.
  * `ipv6-prefer`: prefer IPv6. For TCP, dual-stack resolution is performed and connections are raced, but IPv6 connections are preferred. For UDP, dual-stack resolution is performed and the first IPv6 result is used.


Whether to allow UDP through the proxy. Default: `false`.
Note
This option is enabled by default for UDP-based protocols such as `TUIC`, and for the `direct` and `dns` types.
##  [interface-name](https://wiki.metacubex.one/en/config/proxies/#interface-name)[¶](https://wiki.metacubex.one/en/config/proxies/#interface-name "Permanent link")
Specifies the interface bound by the node. Connections are initiated from this interface.
##  [routing-mark](https://wiki.metacubex.one/en/config/proxies/#routing-mark)[¶](https://wiki.metacubex.one/en/config/proxies/#routing-mark "Permanent link")
Routing mark attached when the node initiates connections.
Enables `TCP Fast Open`. Only effective for the `TCP` protocol.
Enables `TCP Multi Path`. Only effective for the `TCP` protocol.
##  [dialer-proxy](https://wiki.metacubex.one/en/config/proxies/#dialer-proxy)[¶](https://wiki.metacubex.one/en/config/proxies/#dialer-proxy "Permanent link")
Specifies that the current `proxies` entry establishes network connections through `dialer-proxy`. The value can be the `name` of a [proxy group](https://wiki.metacubex.one/en/config/proxy-groups/) or an [outbound proxy](https://wiki.metacubex.one/en/config/proxies/). See the [dialer-proxy documentation](https://wiki.metacubex.one/en/config/proxies/dialer-proxy/) for usage.
sing-mux, only for protocols using TCP transport.
###  [smux.enabled](https://wiki.metacubex.one/en/config/proxies/#smuxenabled)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxenabled "Permanent link")
Whether to enable multiplexing.
###  [smux.protocol](https://wiki.metacubex.one/en/config/proxies/#smuxprotocol)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxprotocol "Permanent link")
Multiplexing protocol. The following protocols are supported. Default: `h2mux`.  
| Protocol  | Description  |  
| --- | --- |  
| `smux`  | <https://github.com/xtaci/smux>  |  
| `yamux`  | <https://github.com/hashicorp/yamux>  |  
| `h2mux`  | <https://golang.org/x/net/http2>  |  
###  [smux.max-connections](https://wiki.metacubex.one/en/config/proxies/#smuxmax-connections)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxmax-connections "Permanent link")
Maximum number of connections.
Conflicts with `max-streams`.
###  [smux.min-streams](https://wiki.metacubex.one/en/config/proxies/#smuxmin-streams)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxmin-streams "Permanent link")
Minimum number of multiplexed streams in a connection before opening a new connection.
Conflicts with `max-streams`.
###  [smux.max-streams](https://wiki.metacubex.one/en/config/proxies/#smuxmax-streams)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxmax-streams "Permanent link")
Maximum number of multiplexed streams in a connection before opening a new connection.
Conflicts with `max-connections` and `min-streams`.
###  [smux.statistic](https://wiki.metacubex.one/en/config/proxies/#smuxstatistic)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxstatistic "Permanent link")
Controls whether the underlying connection is displayed in the dashboard, making it easier to interrupt the underlying connection.
###  [smux.only-tcp](https://wiki.metacubex.one/en/config/proxies/#smuxonly-tcp)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxonly-tcp "Permanent link")
Allows TCP only. If set to true, smux settings do not take effect for UDP; UDP connections use the node's default UDP transport directly.
###  [smux.padding](https://wiki.metacubex.one/en/config/proxies/#smuxpadding)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxpadding "Permanent link")
Enables padding.
###  [smux.brutal-opts](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-opts)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-opts "Permanent link")
TCP Brutal settings.
####  [smux.brutal-opts.enabled](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-optsenabled)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-optsenabled "Permanent link")
Enables the TCP Brutal congestion control algorithm.
####  [smux.brutal-opts.up/down](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-optsupdown)[¶](https://wiki.metacubex.one/en/config/proxies/#smuxbrutal-optsupdown "Permanent link")
Upload and download bandwidth. Defaults to Mbps.
Back to top 
