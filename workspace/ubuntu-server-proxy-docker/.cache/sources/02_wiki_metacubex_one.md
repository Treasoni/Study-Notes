---
url: "https://wiki.metacubex.one/en/config/proxy-providers/"
title: "proxy-providers configuration - mihomo docs"
scraped_at: 2026-08-29T08:38:58+00:00
---

#  [Proxy Providers](https://wiki.metacubex.one/en/config/proxy-providers/#proxy-providers)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#proxy-providers "Permanent link")  
| 
```
































































```
 | 
```
proxy-providers:
provider1:
type:http
url:"http://test.com"
path:./proxy_providers/provider1.yaml
interval:3600
proxy:DIRECT
size-limit:0
age-secret-key:AGE-SECRET-KEY-1ZTQLLN0A4U3ZTT3DCZKYN0CGZEZQLWX2DFTXUWMT4ZHR0N2UG6LSW9NT0N
header:
User-Agent:
-"mihomo/1.18.3"
Authorization:
-'token1231231'
# X-Age-Public-Key:
# - 'age1xh86kh9v23vattr58yedspm3f57sxvnswu9krr6ns438amekx5gsd09uma'
health-check:
enable:true
url:https://www.gstatic.com/generate_204
interval:300
timeout:5000
lazy:true
expected-status:204
override:
tfo:false
mptcp:false
udp:true
udp-over-tcp:false
down:"50Mbps"
up:"10Mbps"
skip-cert-verify:true
name-cert-verify:example.com
dialer-proxy:proxy
interface-name:tailscale0
routing-mark:233
ip-version:ipv4-prefer
additional-prefix:"provider1prefix|"
additional-suffix:"|provider1suffix"
proxy-name:
-pattern:"IPLC-(.*?)倍"
target:"iplcx$1"
# override-expr:
#   - '.name = "[provider1] " + .name'                    
#   - '.plugin-opts.mode = "tls"'                        
#   - '.alpn[] |= upcase'                                
#   - 'del(.skip-cert-verify)'                           
#   - '.name = (.name | trim | upcase)'                  
#   - '.name = "[\(.type)] \(.name):\(.port)"'           
#   - '(select(.port == 443) | .tls) = true'             
#   - '.tags |= (unique | sort)'                         
#   - '.names = [.servers[] | select(.enabled) | .name]' 
#   - '.servers |= map(select(.enabled))'                
#   - '.options |= with_entries(.key |= upcase)'         
#   - '. | with_entries(.key |= upcase)'                 
filter:"(?i)港|hk|hongkong|hongkong"
exclude-filter:"xxx"
exclude-type:"ss|http"
payload:
-name:"ss1"
type:ss
server:server
port:443
cipher:chacha20-ietf-poly1305
password:"password"

```
 |  
| --- | --- |  
Required. For example, `provider1`. It must be unique and it is recommended not to duplicate names with [Proxy Groups](https://wiki.metacubex.one/en/config/proxy-groups/#name).
Required. The type of the `provider`. Available options: `http` / `file` / `inline`.
Required if the `type` is set to `http`.
Optional. The file path. It must be unique. If left empty, the MD5 hash of the URL will be used as the filename.
Due to security concerns, this path is restricted to the `HomeDir` (configured via the `-d` startup parameter) by default. If you wish to store it in another location, please specify additional safe paths by setting the `SAFE_PATHS` environment variable. The syntax of this environment variable follows the parsing rules of the host operating system's PATH variable (i.e., separated by semicolons on Windows, and by colons on other operating systems).
##  [interval](https://wiki.metacubex.one/en/config/proxy-providers/#interval)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#interval "Permanent link")
The update interval for the `provider`, in seconds.
Downloads/updates through the specified proxy.
##  [size-limit](https://wiki.metacubex.one/en/config/proxy-providers/#size-limit)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#size-limit "Permanent link")
Limits the maximum size of the downloaded file. Default is 0, which means no file size limit. The unit is bytes (`b`).
##  [age-secret-key](https://wiki.metacubex.one/en/config/proxy-providers/#age-secret-key)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#age-secret-key "Permanent link")
If configured, the core will attempt to decrypt the age armor-formatted configuration file using this secret key.
Note:
  * For encrypted content, only the official ASCII "armor" format of [age-encryption.org/v1](https://age-encryption.org/v1) is currently supported.
  * For the key format, only the x25519 recipient type of [age-encryption.org/v1](https://age-encryption.org/v1) and The mlkem768-x25519 hybrid post-quantum recipient type are currently supported.
  * Currently, the core will not actively send the public key to the server. Users need to manually set the `X-Age-Public-Key` in the header or upload the public key via other methods.
  * The core also supports loading encrypted configuration files via the `-age-secret-key` command-line parameter or the `CLASH_AGE_SECRET_KEY` environment variable.


Utilities:
  * You can generate a compliant x25519 key via `mihomo age keygen`.
  * You can generate a compliant mlkem768-x25519 key via `mihomo age keygen-pq`.
  * You can export the age-public-key from an age-secret-key via `mihomo age convert <secret_key>`.
  * You can decrypt an encrypted file via `mihomo age decrypt <secret_key> <source_file> <target_file>`. When `<source_file>` is `-`, it will read from standard input; when `<target_file>` is `-`, it will write to standard output.
  * You can encrypt an unencrypted file via `mihomo age encrypt <public_key> <source_file> <target_file>`. When `<source_file>` is `-`, it will read from standard input; when `<target_file>` is `-`, it will write to standard output.


Reference Implementations:
  * Golang: [FiloSottile/age](https://github.com/FiloSottile/age)
  * Rust: [str4d/rage](https://github.com/str4d/rage)
  * Typescript: [FiloSottile/typage](https://github.com/FiloSottile/typage)


Custom HTTP request headers.
##  [health-check](https://wiki.metacubex.one/en/config/proxy-providers/#health-check)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-check "Permanent link")
Health Check (Latency Test)
###  [health-check.enable](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkenable)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkenable "Permanent link")
Specifies whether to enable it. Available options: `true/false`.
###  [health-check.url](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkurl)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkurl "Permanent link")
The health check URL. It is recommended to use one of the following addresses:
CloudflareGoogle

```
https://cp.cloudflare.com

```


```
https://www.gstatic.com/generate_204

```

###  [health-check.interval](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkinterval)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkinterval "Permanent link")
The interval time for health checks, in seconds.
###  [health-check.timeout](https://wiki.metacubex.one/en/config/proxy-providers/#health-checktimeout)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checktimeout "Permanent link")
The timeout duration for health checks, in milliseconds.
###  [health-check.lazy](https://wiki.metacubex.one/en/config/proxy-providers/#health-checklazy)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checklazy "Permanent link")
Lazy state. Default is `true`. When the nodes in this provider are not in use, health checks will not be performed.
###  [health-check.expected-status](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkexpected-status)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#health-checkexpected-status "Permanent link")
See [Expected Status](https://wiki.metacubex.one/en/config/proxy-groups/#expected-status).
##  [override](https://wiki.metacubex.one/en/config/proxy-providers/#override)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#override "Permanent link")
Overrides the configuration of nodes when they are loaded. Supported fields are listed below:
###  [override.additional-prefix](https://wiki.metacubex.one/en/config/proxy-providers/#overrideadditional-prefix)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#overrideadditional-prefix "Permanent link")
Adds a fixed prefix to the node names.
###  [override.additional-suffix](https://wiki.metacubex.one/en/config/proxy-providers/#overrideadditional-suffix)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#overrideadditional-suffix "Permanent link")
Adds a fixed suffix to the node names.
###  [override.proxy-name](https://wiki.metacubex.one/en/config/proxy-providers/#overrideproxy-name)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#overrideproxy-name "Permanent link")
Replaces content in node names, supporting regular expressions. `pattern` represents the content to be replaced, and `target` represents the replacement target.
###  [override.Other Configurations](https://wiki.metacubex.one/en/config/proxy-providers/#overrideother-configurations)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#overrideother-configurations "Permanent link")
Refer to common fields [tfo](https://wiki.metacubex.one/en/config/proxies/#tfo)
Refer to common fields [mptcp](https://wiki.metacubex.one/en/config/proxies/#mptcp)
Refer to common fields [udp](https://wiki.metacubex.one/en/config/proxies/#udp).
Refer to `Shadowsocks` [udp-over-tcp](https://wiki.metacubex.one/en/config/proxies/ss/#udp-over-tcp)
Refer to `Hysteria`/`Hysteria2` [up](https://wiki.metacubex.one/en/config/proxies/hysteria2/#updown).
Refer to `Hysteria`/`Hysteria2` [down](https://wiki.metacubex.one/en/config/proxies/hysteria2/#updown).
Refer to common fields [skip-cert-verify](https://wiki.metacubex.one/en/config/proxies/tls/#skip-cert-verify).
Refer to common fields [name-cert-verify](https://wiki.metacubex.one/en/config/proxies/tls/#name-cert-verify).
Refer to common fields [dialer-proxy](https://wiki.metacubex.one/en/config/proxies/#dialer-proxy).
Refer to common fields [interface-name](https://wiki.metacubex.one/en/config/proxies/#interface-name).
Refer to common fields [routing-mark](https://wiki.metacubex.one/en/config/proxies/#routing-mark).
Refer to common fields [ip-version](https://wiki.metacubex.one/en/config/proxies/#ip-version).
##  [override.override-expr](https://wiki.metacubex.one/en/config/proxy-providers/#overrideoverride-expr)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#overrideoverride-expr "Permanent link")
This is a `yq v4` style subset for expression-based configuration overrides. The array items are executed sequentially and take effect after the fixed-field overrides mentioned above (such as `udp: true`, etc.).
Supported path forms include `.`, `.name`, `."a.b"`, `.["a.b"]`, `.items[0]`, and `.items[-1]`; `[]` can traverse arrays or mappings. Assignment creates missing mappings and non-negative array indexes, but does not update through scalars.
Supported operations include `=`, `|=`, `+=`, `-=`, `*=`, `del(.field)`, pipeline `|`, comma union, `select`, the `//` default operator, common comparisons, and boolean operations. Values support `null` / `~`, booleans, decimal/hex integers, floats, double-quoted strings, arrays, and mappings with double-quoted keys.
Supported functions include `length`, `keys`, `has`, `contains`, `select`, `reverse`, `sort`, `unique`, `flatten`, `any`, `all`, `map`, `map_values`, `filter`, `to_entries`, `from_entries`, `with_entries`, `any_c`, `all_c`, `test`, `sub`, `split`, `join`, `upcase`, `downcase`, `trim`, `tostring`, `tonumber`, `type`, and `not`.
Limitations & Notes
  * Each item must ultimately produce exactly one mapping. Uncollected multiple results and `del(.)` are not supported.
  * Parentheses are mandatory when using pipelines (`|`) or `and`/`or` on the right side of an assignment.
  * `from_entries` only accepts an entries array with string keys.
  * `sort` only supports arrays of scalars. `any`/`all` only support their parameterless forms.
  * `==`/`!=` compare the scalar textual value as per `yq` rules, rather than performing structural comparisons on arrays or mappings.
  * , `<=`, , `>=` only support numbers, strings, and `null`. Only `false` and `null` are treated as falsy values.
  * Standard function arguments must not yield multiple results; however, functions that receive expressions (such as `map`/`filter`) allow their arguments to yield result streams.
  * Function arguments can be separated by commas or semicolons.
  * Evaluation follows value semantics. Out-of-bounds reads do not extend the source array, and `flatten`/`map_values` on the right side do not implicitly modify the source path.
  * Use `|=` when you need to modify the source path. If there is no result on the right side, the target retains its original value instead of automatically creating `null`.
  * Mapping streams, `keys`, and entries transformations are sorted by key, as `map[string]any` does not preserve the original YAML key order.
  * Unsupported language features: Variables (`as/$x`), `reduce`, dynamic paths (`.[$key]`), recursive descent (`..`).
  * Unsupported external features: Multi-documents, file/environment access, YAML tag/style/comment handling, `yq` CLI arguments.
  * Any `yq` syntax, operators, or functions not explicitly listed above are also unsupported. Conditional branching can be achieved using `select` followed by multiple chained assignments.


Filters nodes that match keywords or [regular expressions](https://github.com/ziishaned/learn-regex/blob/master/README.md). Use ``` to separate multiple regular expressions.
##  [exclude-filter](https://wiki.metacubex.one/en/config/proxy-providers/#exclude-filter)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#exclude-filter "Permanent link")
Excludes nodes that match keywords or [regular expressions](https://github.com/ziishaned/learn-regex/blob/master/README.md). Use ``` to separate multiple regular expressions.
##  [exclude-type](https://wiki.metacubex.one/en/config/proxy-providers/#exclude-type)[¶](https://wiki.metacubex.one/en/config/proxy-providers/#exclude-type "Permanent link")
Does not support regular expressions. Separated by `|`. Excludes nodes based on their proxy type.
The `exclude-type` of the provider uses the `type` field defined within the configuration file to perform the exclusion.
Content. Only takes effect when `type` is set to `inline`.
When `http` or `file` parsing fails, the payload can also be used as a fallback backup proxy list.
Back to top 
