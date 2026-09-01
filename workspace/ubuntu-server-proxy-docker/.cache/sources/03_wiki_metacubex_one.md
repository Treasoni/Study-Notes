---
url: "https://wiki.metacubex.one/en/config/general/"
title: "General configuration - mihomo docs"
scraped_at: 2026-08-29T08:38:58+00:00
---

#  [General configuration](https://wiki.metacubex.one/en/config/general/#general-configuration)[¶](https://wiki.metacubex.one/en/config/general/#general-configuration "Permanent link")
##  [Allow LAN](https://wiki.metacubex.one/en/config/general/#allow-lan)[¶](https://wiki.metacubex.one/en/config/general/#allow-lan "Permanent link")
Allows other devices to access the internet through Clash [proxy port](https://wiki.metacubex.one/en/config/inbound/port/).
Optional values: `true/false`  
| 
```
allow-lan:true

```
 |  
| --- |  
Binding address, only allows other devices to access through this address.
  * `"*"` binds to all IP addresses.
  * `"192.168.31.31"` binds to a single IPV4 address.
  * `"[aaaa::a8aa:ff:fe09:57d8]"` binds to a single IPV6 address.

  
| 
```
bind-address:"*"

```
 |  
| --- |  
Allowed IP address ranges for connection, applicable only when `allow-lan` is set to `true`. Default values are `0.0.0.0/0` and `::/0`.  
| 
```
lan-allowed-ips:
-0.0.0.0/0
-::/0

```
 |  
| --- |  
Disallowed IP address ranges for connection. Blacklist takes precedence over whitelist, default is empty.  
| 
```
lan-disallowed-ips:
-192.168.0.3/32

```
 |  
| --- |  
###  [User Authentication](https://wiki.metacubex.one/en/config/general/#user-authentication)[¶](https://wiki.metacubex.one/en/config/general/#user-authentication "Permanent link")
User authentication for http(s), socks, and mixed proxies.  
| 
```
authentication:
-"user1:pass1"
-"user2:pass2"

```
 |  
| --- |  
Set the IP ranges allowed to skip authentication.  
| 
```
skip-auth-prefixes:
-127.0.0.1/8
-::1/128

```
 |  
| --- |  
##  [Operation Mode](https://wiki.metacubex.one/en/config/general/#operation-mode)[¶](https://wiki.metacubex.one/en/config/general/#operation-mode "Permanent link")
  * `rule` Rule-based matching
  * `global` Global proxy (requires selecting proxy/strategy in GLOBAL proxy group)
  * `direct` Global direct connection


defaulting to `rule` mode.  
| 
```
mode:rule

```
 |  
| --- |  
##  [Log Level](https://wiki.metacubex.one/en/config/general/#log-level)[¶](https://wiki.metacubex.one/en/config/general/#log-level "Permanent link")
Controls the logging level of Clash core, only output to console and control page.  
| 
```
log-level:info

```
 |  
| --- |  
  * `silent` Silent, no output.
  * `error` Outputs logs of errors and unusable logs.
  * `warning` Outputs logs of errors that do not affect operations, and logs of error level.
  * `info` Outputs general operational logs, as well as logs of error and warning levels.
  * `debug` Outputs as much information as possible during runtime.


Whether to allow the kernel to accept IPv6 traffic.
Available values: `true/false`. Default: `true`.  
| 
```
ipv6:true

```
 |  
| --- |  
##  [TCP Keep Alive Settings](https://wiki.metacubex.one/en/config/general/#tcp-keep-alive-settings)[¶](https://wiki.metacubex.one/en/config/general/#tcp-keep-alive-settings "Permanent link")
Modify this item to reduce the [power consumption issue](https://github.com/vernesong/OpenClash/issues/2614) on mobile devices
The interval for TCP Keep Alive packets, measured in seconds.  
| 
```
keep-alive-interval:15

```
 |  
| --- |  
The maximum idle time for TCP Keep Alive.  
| 
```
keep-alive-idle:15

```
 |  
| --- |  
Disable TCP Keep Alive; on Android, this is forcibly enabled by default.  
| 
```
disable-keep-alive:false

```
 |  
| --- |  
##  [Process Matching Mode](https://wiki.metacubex.one/en/config/general/#process-matching-mode)[¶](https://wiki.metacubex.one/en/config/general/#process-matching-mode "Permanent link")
Controls whether Clash matches processes.
  * `always` Enables, forces matching of all processes.
  * `strict` Default, Clash determines whether to enable.
  * `off` Does not match processes, recommended for use on routers.

  
| 
```
find-process-mode:strict

```
 |  
| --- |  
##  [External Control (API)](https://wiki.metacubex.one/en/config/general/#external-control-api)[¶](https://wiki.metacubex.one/en/config/general/#external-control-api "Permanent link")
External controller, allows controlling your Clash kernel using RESTful API.
API listening address, you can change `127.0.0.1` to `0.0.0.0` to listen on all IPs.  
| 
```
external-controller:127.0.0.1:9090

```
 |  
| --- |  
API CORS Header Configuration  
| 
```
external-controller-cors:
allow-origins:
-'*'
allow-private-network:true

```
 |  
| --- |  
Unix socket API listening address
Accessing API endpoints via Unix socket does not verify secrets. If enabled, please ensure security measures are in place.  
| 
```
external-controller-unix:mihomo.sock

```
 |  
| --- |  
Windows Named Pipe API Listening Address
Accessing the API interface via Windows Named Pipe does not validate the secret. If enabled, please ensure your security.  
| 
```
external-controller-pipe:\\.\pipe\mihomo

```
 |  
| --- |  
HTTPS-API listening address, requires configuring the tls section for certificate and private key configuration, external-controller must also be filled in.  
| 
```
external-controller-tls:127.0.0.1:9443

```
 |  
| --- |  
Sets the routing mark for the listening sockets of `external-controller` and `external-controller-tls`. Linux only.  
| 
```
external-controller-routing-mark:0

```
 |  
| --- |  
Starts a DoH server on the RESTful API port.
This URL does not verify the API secret. If enabled, make sure it is secured appropriately.  
| 
```
external-doh-server:/dns-query

```
 |  
| --- |  
Access key for the API.  
| 
```
secret:""

```
 |  
| --- |  
##  [External User Interface](https://wiki.metacubex.one/en/config/general/#external-user-interface)[¶](https://wiki.metacubex.one/en/config/general/#external-user-interface "Permanent link")
Allows running static webpage resources (such as Clash-dashboard) on Clash API, path is API address/ui.  
| 
```
external-ui:/path/to/ui/folder

```
 |  
| --- |  
Can be an absolute path or a relative path to the Clash working directory.
Note
Note that if the path is not in the Clash working directory, please manually set the `SAFE_PATHS` environment variable to add it to the safe path. The syntax of this environment variable is the same as the PATH environment variable parsing rules of this operating system (i.e., semicolon-separated in Windows and colon-separated in other systems).
##  [Custom External User Interface Name](https://wiki.metacubex.one/en/config/general/#custom-external-user-interface-name)[¶](https://wiki.metacubex.one/en/config/general/#custom-external-user-interface-name "Permanent link")  
| 
```
external-ui-name:xd# Merged into external-ui/xd

```
 |  
| --- |  
Not mandatory, will be updated to the specified folder during updates, if not configured, it will be updated directly to the `external-ui` directory.
##  [Custom External User Interface Download URL](https://wiki.metacubex.one/en/config/general/#custom-external-user-interface-download-url)[¶](https://wiki.metacubex.one/en/config/general/#custom-external-user-interface-download-url "Permanent link")  
| 
```
external-ui-url:"https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip"# Get from GitHub Pages branch

```
 |  
| --- |  
| 
```





```
 | 
```
profile:
store-selected:true
# Stores API selections for strategy groups for use on the next start
store-fake-ip:true
# Stores the fakeip mapping table, using the original mapping address when the domain connects again

```
 |  
| --- | --- |  
##  [Unified Delay](https://wiki.metacubex.one/en/config/general/#unified-delay)[¶](https://wiki.metacubex.one/en/config/general/#unified-delay "Permanent link")
When unified delay is enabled, RTT is calculated to eliminate latency differences caused by connection handshakes and other variations between proxy types.
Available values: `true/false`.  
| 
```
unified-delay:true

```
 |  
| --- |  
##  [TCP Concurrency](https://wiki.metacubex.one/en/config/general/#tcp-concurrency)[¶](https://wiki.metacubex.one/en/config/general/#tcp-concurrency "Permanent link")
Enable TCP concurrent connections, which will use all IP addresses resolved by DNS for connections, using the first successful connection.
Available values: `true/false`.  
| 
```
tcp-concurrent:true

```
 |  
| --- |  
##  [Outbound Interface](https://wiki.metacubex.one/en/config/general/#outbound-interface)[¶](https://wiki.metacubex.one/en/config/general/#outbound-interface "Permanent link")
mihomo's traffic outbound interface.  
| 
```
interface-name:en0

```
 |  
| --- |  
##  [Routing Mark](https://wiki.metacubex.one/en/config/general/#routing-mark)[¶](https://wiki.metacubex.one/en/config/general/#routing-mark "Permanent link")
Provides a default traffic mark for outbound connections on Linux.  
| 
```
routing-mark:6666

```
 |  
| --- |  
Currently only used for https in API.  
| 
```










```
 | 
```
tls:
certificate:string# Certificate PEM format or certificate path
private-key:string# Private key PEM format corresponding to the certificate, or private key path
ech-key:|-
-----BEGIN ECH KEYS-----
ACATwY30o/RKgD6hgeQxwrSiApLaCgU+HKh7B6SUrAHaDwBD/g0APwAAIAAgHjzK
madSJjYQIf9o1N5GXjkW4DEEeb17qMxHdwMdNnwADAABAAEAAQACAAEAAwAIdGVz
dC5jb20AAA==
-----END ECH KEYS-----
# ECH keys, if not empty, ECH will be enabled.

```
 |  
| --- | --- |  
Note
Starting from version v1.19.18, automatic reloading is supported when `certificate`, `private-key`, or `ech-key` are local files.
##  [Global Client Fingerprint](https://wiki.metacubex.one/en/config/general/#global-client-fingerprint)[¶](https://wiki.metacubex.one/en/config/general/#global-client-fingerprint "Permanent link")
Warning
Global TLS fingerprinting has been deprecated. Please set the [client-fingerprint](https://wiki.metacubex.one/en/config/proxies/tls/#client-fingerprint) directly within the proxy.
##  [GEO Data Mode](https://wiki.metacubex.one/en/config/general/#geo-data-mode)[¶](https://wiki.metacubex.one/en/config/general/#geo-data-mode "Permanent link")
Changes the file used for GeoIP data between `mmdb` and `dat`. Available values: `true/false`; `true` selects `dat`. Default: `false`.  
| 
```
geodata-mode:true

```
 |  
| --- |  
##  [GEO File Loading Mode](https://wiki.metacubex.one/en/config/general/#geo-file-loading-mode)[¶](https://wiki.metacubex.one/en/config/general/#geo-file-loading-mode "Permanent link")
Optional loading modes are as follows:
  * `standard`: Standard loader
  * `memconservative`: Loader optimized for memory-limited (small memory) devices (default)

  
| 
```
geodata-loader:memconservative

```
 |  
| --- |  
##  [Auto Update GEO](https://wiki.metacubex.one/en/config/general/#auto-update-geo)[¶](https://wiki.metacubex.one/en/config/general/#auto-update-geo "Permanent link")  
| 
```
geo-auto-update:false

```
 |  
| --- |  
Update interval, unit is hours  
| 
```
geo-update-interval:24

```
 |  
| --- |  
##  [Custom GEO Download Address](https://wiki.metacubex.one/en/config/general/#custom-geo-download-address)[¶](https://wiki.metacubex.one/en/config/general/#custom-geo-download-address "Permanent link")  
| 
```





```
 | 
```
geox-url:
geoip:"https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geoip.dat"
geosite:"https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/geosite.dat"
mmdb:"https://testingcf.jsdelivr.net/gh/MetaCubeX/meta-rules-dat@release/country.mmdb"
asn:"https://github.com/xishang0128/geoip/releases/download/latest/GeoLite2-ASN.mmdb"

```
 |  
| --- | --- |  
##  [Custom Global UA](https://wiki.metacubex.one/en/config/general/#custom-global-ua)[¶](https://wiki.metacubex.one/en/config/general/#custom-global-ua "Permanent link")
Custom UA used when downloading external resources, default is clash.meta.  
| 
```
global-ua:clash.meta

```
 |  
| --- |  
##  [ETag Support](https://wiki.metacubex.one/en/config/general/#etag-support)[¶](https://wiki.metacubex.one/en/config/general/#etag-support "Permanent link")
ETag support for external resource downloads is enabled by default.  
| 
```
etag-support:true

```
 |  
| --- |  
Back to top 
