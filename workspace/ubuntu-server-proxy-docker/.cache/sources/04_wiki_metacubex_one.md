---
url: "https://wiki.metacubex.one/en/config/inbound/"
title: "inbound configuration - mihomo docs"
scraped_at: 2026-08-29T08:38:58+00:00
---

#  [Inbound Configuration](https://wiki.metacubex.one/en/config/inbound/#inbound-configuration)[¶](https://wiki.metacubex.one/en/config/inbound/#inbound-configuration "Permanent link")
mihomo can receive traffic through proxy ports, TUN, and Listeners. Whether an inbound is reachable from the internet depends on its listening address, system routing, and firewall configuration, not on its protocol category.
##  [Configuration Methods](https://wiki.metacubex.one/en/config/inbound/#configuration-methods)[¶](https://wiki.metacubex.one/en/config/inbound/#configuration-methods "Permanent link")
###  [Proxy Ports](https://wiki.metacubex.one/en/config/inbound/#proxy-ports)[¶](https://wiki.metacubex.one/en/config/inbound/#proxy-ports "Permanent link")
The top-level `port`, `socks-port`, `mixed-port`, `redir-port`, and `tproxy-port` options are suitable when only one fixed set of proxy ports is required.
See [Proxy Ports](https://wiki.metacubex.one/en/config/inbound/port/).
The top-level `tun` configuration captures system traffic and is suitable for automatic routing, DNS hijacking, and per-application routing.
See [TUN](https://wiki.metacubex.one/en/config/inbound/tun/).
`listeners` can create multiple inbounds with different types, listening addresses, and ports. Common fields such as `rule` and `proxy` can be configured independently for each inbound.  
| 
```








```
 | 
```
listeners:
-name:socks5-in-1
type:socks
port:10808
#listen: 0.0.0.0 # Listens on 0.0.0.0 by default
# rule: sub-rule-name1 # Uses rules by default; falls back to rules if the sub-rule is not found
# proxy: proxy # When non-empty, sends inbound traffic directly to the specified proxy
# udp: false # true by default

```
 |  
| --- | --- |  
See [Common Listener Fields](https://wiki.metacubex.one/en/config/inbound/listeners/).
Warning
`listen: 0.0.0.0` listens on every network interface. HTTP, SOCKS, and Mixed inbounds without TLS should not be exposed directly to the internet.
##  [Listener Types](https://wiki.metacubex.one/en/config/inbound/#listener-types)[¶](https://wiki.metacubex.one/en/config/inbound/#listener-types "Permanent link")  
| Purpose  | Types  |  
| --- | --- |  
| Application proxies  |  
| Transparent proxying and system capture  |  [Redirect](https://wiki.metacubex.one/en/config/inbound/listeners/redirect/), [TProxy](https://wiki.metacubex.one/en/config/inbound/listeners/tproxy/), [TUN](https://wiki.metacubex.one/en/config/inbound/listeners/tun/)  |  
| Port forwarding  |  
| Encrypted proxy servers  |  [Shadowsocks](https://wiki.metacubex.one/en/config/inbound/listeners/ss/), [VMess](https://wiki.metacubex.one/en/config/inbound/listeners/vmess/), [VLESS](https://wiki.metacubex.one/en/config/inbound/listeners/vless/), [Trojan](https://wiki.metacubex.one/en/config/inbound/listeners/trojan/), [AnyTLS](https://wiki.metacubex.one/en/config/inbound/listeners/anytls/), [Snell](https://wiki.metacubex.one/en/config/inbound/listeners/snell/), [Mieru](https://wiki.metacubex.one/en/config/inbound/listeners/mieru/), [Sudoku](https://wiki.metacubex.one/en/config/inbound/listeners/sudoku/), [TrustTunnel](https://wiki.metacubex.one/en/config/inbound/listeners/trusttunnel/)  |  
| QUIC / UDP servers  |  [TUIC v4](https://wiki.metacubex.one/en/config/inbound/listeners/tuic-v4/), [TUIC v5](https://wiki.metacubex.one/en/config/inbound/listeners/tuic-v5/), [Hysteria2](https://wiki.metacubex.one/en/config/inbound/listeners/hysteria2/), [Hysteria2 Realm](https://wiki.metacubex.one/en/config/inbound/listeners/hysteria2-realm/), [ShadowQUIC](https://wiki.metacubex.one/en/config/inbound/listeners/shadowquic/)  |  
Note
The TUN Listener is intended for advanced use cases. Most users should prefer the top-level [TUN](https://wiki.metacubex.one/en/config/inbound/tun/) configuration.
##  [Shortcut Inbounds](https://wiki.metacubex.one/en/config/inbound/#shortcut-inbounds)[¶](https://wiki.metacubex.one/en/config/inbound/#shortcut-inbounds "Permanent link")
`ss-config`, `vmess-config`, and `tuic-server` remain available for quickly creating their corresponding inbounds. These shortcut inbounds are equivalent to their corresponding Listeners, and incoming traffic is processed like other inbounds according to the configured `mode`.  
| 
```



















```
 | 
```
ss-config:ss://2022-blake3-aes-256-gcm:vlmpIPSyHH6f4S8WVPdRIHIlzmB+GIRfoH3aNJ/t9Gg=@:23456
vmess-config:vmess://1:9d0cb9d0-964f-4ef6-897d-6c6b3ccf9e68@:12345

tuic-server:
enable:true
listen:127.0.0.1:10443
token:# TUIC v4; cannot be used together with users
-TOKEN
# users: # TUIC v5; cannot be used together with token
#   00000000-0000-0000-0000-000000000000: PASSWORD-0
#   00000000-0000-0000-0000-000000000001: PASSWORD-1
certificate:./server.crt
private-key:./server.key
congestion-controller:bbr
max-idle-time:15000
authentication-timeout:1000
alpn:
-h3
max-udp-relay-packet-size:1500

```
 |  
| --- | --- |  
Note
Shortcut inbounds are useful for existing configurations and simple use cases. Prefer `listeners` when a new configuration needs additional protocol options or independent routing.
Back to top 
