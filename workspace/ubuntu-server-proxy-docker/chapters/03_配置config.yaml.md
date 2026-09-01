# 第三章：配置 config.yaml

上一章我们已经把 mihomo 二进制装好并跑起了一个能启动的服务，但此时它还没有任何节点可用——代理是空的。本章解决的核心问题是：**怎样写一份能让 mihomo 真正代理流量的 `config.yaml`**，包括开几个入口端口、如何导入订阅节点、如何把节点分组，以及一份可直接复制的最小配置。这是整个代理链路里最容易被「抄了配置却连不上」的一章，值得放慢速度读完。

## 3.1 顶层入站配置：先看门面

`config.yaml` 的第一段是「顶层配置」，决定 mihomo 监听哪些端口、允许谁连进来。逐个拆解：

```yaml
mixed-port: 7890            # HTTP + SOCKS5 混合端口
allow-lan: true             # 允许局域网其他设备（含 Docker 容器）接入
bind-address: "*"           # 绑定所有网卡 IP
mode: rule                  # 规则分流模式
log-level: info             # 日志级别：silent/error/warning/info/debug
external-controller: 127.0.0.1:9090   # RESTful API，给 Web UI 或脚本控制用
ipv6: false                 # 服务器有 IPv6 但订阅不支持时可关掉，避免解析卡顿
```

- **`mixed-port`（HTTP+SOCKS5 混合端口）**：一个端口同时提供 HTTP 代理和 SOCKS5 代理，客户端无需区分协议，绝大多数场景只开它就够了（常用 7890）[^c3-1][^c3-2]。
- **`port` / `socks-port`**：如果需要把 HTTP 和 SOCKS5 分到两个端口（比如某些软件只认其中一个），可以再单独指定 `port: 7891`、`socks-port: 7892`；日常与 `mixed-port` 三选一即可[^c3-2]。
- **`mode`**：`rule`（按规则分流）是本笔记全程采用、也是 mihomo 默认的模式；另两种 `global`（全走代理）与 `direct`（全直连）用得少。
- **`log-level`**：`info` 足够排查，出问题时临时调成 `debug` 能看节点握手细节。
- **`external-controller`**：可选，提供 HTTP API（`127.0.0.1:9090`）。本笔记走 CLI 路线，先保持只监听本机；改成 `0.0.0.0` 可远程控制，但相当于把管理口暴露到公网，必须慎重[^c3-1]。

> [!tip] 大白话：把 mixed-port 想成「前台总机」
> 一个电话号码既接传真又接电话，别人不用知道你是哪种设备，打同一个号就行。所以 `mixed-port: 7890` 让 curl、浏览器、Docker 容器都指向同一个 `7890`，不用记两套端口。而 `port`/`socks-port` 就像把传真和电话拆成两个号码，只有少数强迫症场景才需要。

## 3.2 `allow-lan: true` + `bind-address: "*"`：让 Docker 容器能用代理

这两个选项是后面第五章节 Docker 容器能出网的前提，先在这里埋好：

- **`allow-lan: true`**：允许除本机外的设备接入代理端口。
- **`bind-address: "*"`**：把监听地址绑定到所有网卡 IP，而不是默认的 `127.0.0.1`。

为什么要同时开？因为 Docker 容器访问宿主机时走的是 **docker0 网桥**，源地址是网桥网段的 IP（如 `172.17.0.1`），**不是** `127.0.0.1`。只有 `allow-lan: true` 且 `bind-address: "*"` 时，mihomo 才愿意接受来自 docker0 网桥的连接。换句话说：`allow-lan` 决定「允不允许别人进」，`bind-address` 决定「门开在哪些墙」[^c3-1][^c3-2]。

> [!warning] 安全警告
> 一旦 `bind-address: "*"`，如果你的服务器有公网 IP，代理端口对公网也是开放的。**HTTP/SOCKS 明文代理被公网扫描到后极易被劫持做跳板**。如果服务器暴露在公网，务必在顶层加 `authentication`（用户名+密码），或者用 ufw 只放行内网来源（`ufw allow from 192.168.0.0/16 to any port 7890 proto tcp`）。不推荐为图省事直接公网开放代理端口[^c3-1]（可对照既有笔记 [[外网如何使用代理进行翻墙]] 里的 Clash 认证部分）。

> [!tip] 大白话：allow-lan 像「门禁开放」
> 默认门禁只放行自己人（127.0.0.1）；`allow-lan: true` 是把公司访客也放进来（局域网设备）；`bind-address: "*"` 则是把所有大门（所有网卡 IP）都装上这套门禁。Docker 容器走的是后门（docker0 网桥），不开后门它们就进不来——但门全开了，小偷（公网扫描）也可能进来，所以要加锁（authentication）或拉警戒线（ufw）。

## 3.3 订阅导入：`proxy-providers`

节点不用手写，从订阅链接自动拉取即可。这是最常用、也最容易踩坑的一段：

```yaml
proxy-providers:
  provider1:
    type: http
    url: "YOUR_SUBSCRIBE_URL"          # 你的 Clash 订阅链接
    path: ./proxy_providers/provider1.yaml   # 缓存的本地文件名
    interval: 3600                     # 每 3600 秒（1 小时）自动更新一次订阅
    health-check:
      enable: true                     # 启用节点健康检查（测速）
      url: https://www.gstatic.com/generate_204
      interval: 300                    # 每 300 秒测一次延迟
```

各字段含义[^c3-3]：

- **`type: http`**：从远程 URL 拉取订阅；另一种 `file` 类型读本地文件，日常用不上。
- **`url`**：订阅地址。注意它必须返回**标准 Clash 格式**（含 `proxies`/`proxy-groups`/`rules` 的 YAML 或 Base64），详见 3.7。
- **`path`**：订阅缓存落盘位置。**默认只能写在 mihomo 工作目录（`-d /etc/mihomo`）内**；写到别处会报路径不安全，需要额外设置 `SAFE_PATHS` 环境变量。上面的 `./proxy_providers/provider1.yaml` 相对 `-d` 目录解析，安全无需额外设置[^c3-3]。
- **`interval`**：订阅自动刷新周期，单位秒。
- **`health-check`**：周期性地对每个节点发一个请求（`generate_204` 是一个约定俗成的探活地址）测延迟，为 `url-test` 分组提供选路依据[^c3-3]。

另外三个筛选参数，订阅节点太多时用：`filter`（只保留名字匹配正则的节点）、`exclude-filter`（排除匹配的）、`exclude-type`（按类型排除，如 `ss`/`ssr`/`vmess`）。本笔记最小配置用不到，先认识即可[^c3-3]。

> [!tip] 大白话：订阅像「料理包」
> 你不用自己去菜市场挑每一样食材（手写每个节点），买一包料理包（订阅链接），厨子定期按菜单上货（`interval` 刷新）。但上货前得先验货——`health-check` 就是「每个食材戳一戳看新不新鲜」，不新鲜的自动标记出来，测速分组就不会选到它。

## 3.4 节点分组：`proxy-groups`

订阅拉进来的是「一堆节点」，但 mihomo 不会自动决定用哪个，要靠 `proxy-groups` 把它们编成组。两种最常用的组：

```yaml
proxy-groups:
  - name: PROXY                  # 手选组
    type: select
    use: [provider1]             # 引用上面订阅里的所有节点

  - name: AUTO                   # 自动测速组
    type: url-test
    use: [provider1]
    url: https://www.gstatic.com/generate_204
    interval: 300
```

- **`select`（手选）**：自己点选当前走哪个节点，最直观可控。
- **`url-test`（自动测速）**：按 `health-check`/这里 `url` 的延迟自动切换最快节点，适合不想手动切的场景。
- **`use: [provider1]`**：把 `proxy-providers` 里声明的 provider1 下所有节点整体引用进来；注意缩进，`use` 是组的字段，不是 provider 的字段[^c3-3]。

> [!tip] 大白话：proxy-groups 像「遥控器上的分组按钮」
> 订阅把 50 个频道（节点）装进机顶盒，但你看的时候总得有一个「当前频道」。`select` 是手动按频道，`url-test` 是「信号差就自动跳台」。`use: [provider1]` 就是把整个频道包挂到这两个按钮上。

## 3.5 `rules`：规则分流简介

规则决定「这个请求走代理还是直连」，从上到下逐条匹配，命中即停。最小可运行配置只需一条兜底：

```yaml
rules:
  - MATCH,PROXY    # 其余全部走 PROXY 组
```

- **`MATCH`**：兜底规则，放在最后，匹配所有没被前面规则命中的流量。没有它，未知域名会被直接拒绝或直连，经常导致「有规则但就是不代理」的困惑。
- **`GEOIP,CN,DIRECT`（可选）**：按目标 IP 归属地分流，国内 IP 直连、国外走代理，可放在 `MATCH` 之前。它依赖 geoip 数据库（mihomo 会自动拉取），本笔记最小配置先不引入，第四章会用「域名级」验证代替。

## 3.6 最小可运行 config.yaml（可直接复制）

把上面拼起来，得到一份完整可用的配置。先睹为快，复制后只需把 `YOUR_SUBSCRIBE_URL` 换成真实订阅地址：

```yaml
# /etc/mihomo/config.yaml
mixed-port: 7890
allow-lan: true
bind-address: "*"
mode: rule
log-level: info
external-controller: 127.0.0.1:9090
ipv6: false

proxy-providers:
  provider1:
    type: http
    url: "YOUR_SUBSCRIBE_URL"
    path: ./proxy_providers/provider1.yaml
    interval: 3600
    health-check:
      enable: true
      url: https://www.gstatic.com/generate_204
      interval: 300

proxy-groups:
  - name: PROXY
    type: select
    use: [provider1]

rules:
  - MATCH,PROXY
```

逐段解读：

1. **顶层**：开 `mixed-port: 7890`，允许局域网/Docker 接入，规则模式，日志 `info`。
2. **`proxy-providers`**：从订阅链接拉节点，缓存到 `./proxy_providers/provider1.yaml`，每小时刷新、每 5 分钟测延迟。
3. **`proxy-groups`**：建一个手选组 `PROXY`，挂载 provider1 全部节点。
4. **`rules`**：所有流量交给 `PROXY` 组，你在组里手选节点后即生效。

这份配置只依赖订阅链接，不依赖任何额外文件，是能跑通的最小闭环。

## 3.7 落地提示：格式确认、SAFE_PATHS 与重载

写完后，`systemctl reload`（热更新）或 `restart`（重启）让配置生效[^c3-1]：

```bash
sudo systemctl reload mihomo     # 热更新配置，推荐
sudo systemctl status mihomo     # 看是否 active
journalctl -u mihomo -ocat -e    # 有异常看日志
```

三个高频坑，写配置前就要确认：

1. **订阅格式必须是 Clash 标准**（内容含 `proxies`、`proxy-groups`、`rules`）。如果订阅是 **sing-box 格式**，`proxy-providers` 无法直接解析，需先用工具转换为 Clash 标准格式再填 URL，否则 mihomo 拉下来解析失败，服务报错但不退出。
2. **`path` 默认限制在 `-d` 目录内**。`-d /etc/mihomo` 是 mihomo 的工作目录，`path` 想写到别处必须设 `SAFE_PATHS` 环境变量，否则启动即报「path is not in safe path」[^c3-3]。
3. **改完必须 reload/restart**。config.yaml 不会自动热加载，忘记 reload 会出现「改了没反应」的错觉。

> [!note] 章节小结
> - 顶层 `mixed-port: 7890` 一个端口同时提供 HTTP+SOCKS5；`mode: rule` 是规则分流模式。
> - `allow-lan: true` + `bind-address: "*"` 是后续 Docker 容器能访问代理的前提，但也意味着暴露公网，必须加 `authentication` 或 ufw 限制。
> - `proxy-providers` 用 `type: http` + `url` 导入订阅，`path` 只能在 `-d` 目录内，`health-check` 负责测延迟。
> - `proxy-groups` 用 `select`（手选）或 `url-test`（自动测速），`use: [provider1]` 引用订阅节点。
> - `rules` 至少要有 `MATCH` 兜底，否则流量可能「不代理」。
> - 改完配置执行 `systemctl reload mihomo` 生效。

下一章我们把 mihomo 跑通之后，会解决「命令行工具、apt、git 怎么自动走这个代理」的问题——那就要开始写环境变量脚本了。

[^c3-1]: S2：mihomo 官方文档 General config（allow-lan / bind-address / authentication / external-controller / mode / log-level）。
[^c3-2]: S4：mihomo 官方文档 inbound（mixed-port / port / socks-port；`listen: 0.0.0.0` 明文代理安全警告）。
[^c3-3]: S3：mihomo 官方文档 proxy-providers（type / url / path / interval / health-check；SAFE_PATHS；filter / exclude-filter / exclude-type）。
