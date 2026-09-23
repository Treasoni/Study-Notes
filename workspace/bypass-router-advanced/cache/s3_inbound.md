---
url: "https://wiki.metacubex.one/config/inbound/"
title: "入站配置 - 虚空终端 Docs"
scraped_at: 2026-09-23T06:05:38+00:00
---

mihomo 可以通过代理端口、TUN 和 Listeners 接收流量。入站是否能从公网访问取决于监听地址、系统路由和防火墙配置，而不是协议所属的分类。
顶层的 `port`、`socks-port`、`mixed-port`、`redir-port` 和 `tproxy-port` 适合只需要一组固定代理端口的配置。
参阅[代理端口](https://wiki.metacubex.one/config/inbound/port/)。
顶层 `tun` 配置用于接管系统流量，适合需要自动路由、DNS 劫持或按应用分流的场景。
参阅 [TUN](https://wiki.metacubex.one/config/inbound/tun/)。
`listeners` 可以同时创建多个不同类型、监听地址和端口的入站，并为每个入站单独设置 `rule`、`proxy` 等通用字段。  
| 
```








```
 | 
```
listeners:
-name:socks5-in-1
type:socks
port:10808
#listen: 0.0.0.0 # 默认监听 0.0.0.0
# rule: sub-rule-name1 # 默认使用 rules,如果未找到 sub-rule 则直接使用 rules
# proxy: proxy # 如果不为空则直接将该入站流量交由指定proxy处理
# udp: false # 默认 true

```
 |  
| --- | --- |  
参阅 [Listener 通用字段](https://wiki.metacubex.one/config/inbound/listeners/)。
Warning
`listen: 0.0.0.0` 会监听所有网络接口。未启用 TLS 的 HTTP、SOCKS、Mixed 等入站不应直接暴露到公网。
##  [Listener 类型](https://wiki.metacubex.one/config/inbound/#listener)[¶](https://wiki.metacubex.one/config/inbound/#listener "Permanent link")  
| 用途  | 类型  |  
| --- | --- |  
| 应用代理  |  
| 透明代理与系统接管  |  [Redirect](https://wiki.metacubex.one/config/inbound/listeners/redirect/)、[TProxy](https://wiki.metacubex.one/config/inbound/listeners/tproxy/)、[TUN](https://wiki.metacubex.one/config/inbound/listeners/tun/)  |  
| 端口转发  |  
| 加密代理服务端  |  [Shadowsocks](https://wiki.metacubex.one/config/inbound/listeners/ss/)、[VMess](https://wiki.metacubex.one/config/inbound/listeners/vmess/)、[VLESS](https://wiki.metacubex.one/config/inbound/listeners/vless/)、[Trojan](https://wiki.metacubex.one/config/inbound/listeners/trojan/)、[AnyTLS](https://wiki.metacubex.one/config/inbound/listeners/anytls/)、[Snell](https://wiki.metacubex.one/config/inbound/listeners/snell/)、[Mieru](https://wiki.metacubex.one/config/inbound/listeners/mieru/)、[Sudoku](https://wiki.metacubex.one/config/inbound/listeners/sudoku/)、[TrustTunnel](https://wiki.metacubex.one/config/inbound/listeners/trusttunnel/)  |  
| QUIC / UDP 服务端  |  [TUIC v4](https://wiki.metacubex.one/config/inbound/listeners/tuic-v4/)、[TUIC v5](https://wiki.metacubex.one/config/inbound/listeners/tuic-v5/)、[Hysteria2](https://wiki.metacubex.one/config/inbound/listeners/hysteria2/)、[Hysteria2 Realm](https://wiki.metacubex.one/config/inbound/listeners/hysteria2-realm/)、[ShadowQUIC](https://wiki.metacubex.one/config/inbound/listeners/shadowquic/)  |  
Note
Listener 中的 TUN 面向高级使用场景。普通用户应优先使用顶层 [TUN](https://wiki.metacubex.one/config/inbound/tun/) 配置。
`ss-config`、`vmess-config` 和 `tuic-server` 仍可用于快速创建对应入站。这些快捷入口与对应的 Listener 等价，传入流量与其他入站一样按照配置的 `mode` 处理。  
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
token:# TUIC v4，与 users 不能同时配置
-TOKEN
# users: # TUIC v5，与 token 不能同时配置
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
快捷入口适合兼容已有配置或简单场景。新配置需要更多协议选项或独立路由时，建议使用 `listeners`。
回到页面顶部 
