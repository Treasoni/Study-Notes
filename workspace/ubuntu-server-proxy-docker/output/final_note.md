# 在 Ubuntu Server 中配置翻墙（代理），并让 Docker 容器和其他应用正常使用

## 目录

1. [第一章：总览与方案选型](#第一章总览与方案选型)
2. [第二章：安装 mihomo 内核](#第二章安装-mihomo-内核)
3. [第三章：配置 config.yaml](#第三章配置-configyaml)
4. [第四章：系统级代理接管](#第四章系统级代理接管)
5. [第五章：Docker 走代理](#第五章docker-走代理)
6. [第六章：验证清单与常见坑](#第六章验证清单与常见坑)

---

## 第一章：总览与方案选型

本章回答一个前置问题：**服务器到底「怎么翻墙」最合适**。先看清痛点，再对比两条技术路线，选定本笔记「显式代理 + mihomo 内核」的方案，最后列出自备清单。本章不写配置，只规划路线。

---

### 1.1 场景痛点：命令行与 Docker 都被墙卡住

在 Ubuntu Server 上，被墙是日常：`apt update` 超时、`git clone` GitHub 失败、`docker pull` 拉镜像无限转圈。命令本身没问题，问题是它们要访问的**海外服务器**（apt 源、GitHub、Docker Hub）无法直连。

> [!note] 一条链路、多个入口
> 被墙的不是某一条命令，而是「命令行 / apt / git / Docker daemon / 容器内应用」这一整条出网链路。本笔记要在这台服务器上搭一个「中转站」，让整条链路都走它出去。

### 1.2 为什么服务器端选 mihomo 内核

mihomo（Clash.Meta 内核）是 Clash 的活跃维护分支，特别适合**无图形界面的服务器**：

- **轻量**：单二进制、无桌面依赖、内存占用小[^c1-1]。
- **订阅友好**：`proxy-providers` 直接填订阅链接，定时拉取节点，不用手动导入[^c1-4]。
- **可被 systemd 守护**：开机自启、崩溃自动重启，服务器重启后无需手动拉起[^c1-2]。

> [!tip] 大白话：mihomo 是「小区门卫室」，订阅是「料理包」
> 你要寄到海外的包裹（apt/git/Docker 的请求）不直接出门，先交给门卫室（mihomo），由门卫挑一条路（节点）转交出去。**订阅链接像料理包套餐**——一个链接打包好整批可用的「菜式」（节点），mihomo 定期自动补货。

### 1.3 显式代理 vs TUN：路线对比

| 维度 | 显式代理（本笔记） | TUN / 透明代理（进阶） |
|------|--------------------|------------------------|
| 原理 | 各程序被告知「经 7890 转发」 | 内核层建虚拟网卡，拦截所有流量 |
| 配置 | 各程序单独配置 | 全局接管，无需逐程序配置 |
| 优点 | 可控、可分流、好排查 | 不认代理的老程序也能覆盖 |
| 缺点 | 不认代理的程序会漏网 | 配置复杂，易与 VPN/NAT 冲突 |
| 适用 | 服务器 + 命令行 + Docker | 想无感全代理、设备多 |

> [!tip] 大白话：显式代理是「逐个通知」，TUN 是「改整条路」
> 显式代理像公司访客制度，每个程序得自己去前台登记（设环境变量）才放行；TUN 像给整栋楼新装专用通道，所有人自动走。本笔记选显式代理：**服务器场景下可控、可排查更重要**。

### 1.4 架构总览

```text
        ┌─────────────────────────────────────────────┐
        │              Ubuntu Server                  │
        │  系统命令 curl/wget ──────┐                  │
        │  apt（软件源）   ─────────┤ 环境变量          │
        │  git（GitHub）   ─────────┤ http_proxy       │
        │                           │                  │
        │  Docker daemon（拉镜像）──┤ daemon.json      │
        │  Docker 容器（应用出网）──┤ config.json      │
        │                           ▼                  │
        │               ┌──────────────────┐           │
        │               │  mihomo 内核      │           │
        │               │ mixed-port:7890  │           │
        │               └────────┬─────────┘           │
        └────────────────────────┼─────────────────────┘
                                 ▼
                      订阅节点服务器（海外出口）
```

四个接入方（命令行 / apt / git / Docker）最终都汇聚到 mihomo 的 **mixed-port: 7890** 一个端口出去[^c1-3]，由内核按规则分流。

> [!tip] 大白话：mixed-port 是「三合一充电线」
> 一个端口同时听懂 HTTP 和 SOCKS5，像三合一充电线——不同设备插同一个口就能充电，你只需记住 7890 这一个数字。

### 1.5 前置准备清单

动手前逐项打勾：

- [ ] **root / sudo 权限**：后续操作需要
- [ ] **已安装 Docker**：熟悉 `pull / run / build`
- [ ] **标准 Clash 订阅链接**：机场或自建
- [ ] **确认架构**：`uname -m` → `x86_64`(amd64) / `aarch64`(arm64)，第二章按它选包[^c1-1]
- [ ] **确认订阅格式**：Clash 标准（含 `proxies`/`proxy-groups`/`rules`）还是 sing-box——后者需先转换[^c1-4]
- [ ] **公网 DNS**：能解析订阅域名，否则拉不到节点

> [!warning] 动手前先确认订阅格式
> 最常见的翻车点：把 sing-box 格式订阅直接填进 Clash 配置会加载失败。拿不准就先向机场要「Clash 订阅链接」。

### 1.6 与既有笔记衔接

本笔记与项目里三篇既有笔记互补，概念可交叉阅读：

- [[docker/docker进行代理]] — 宿主机已有 Clash 时，Docker 容器如何走代理[^c1-5]
- [[docker/镜像加速器vs代理-概念对比]] — 加速器与代理的定位区别，避免混淆
- [[外网如何使用代理进行翻墙]] — 代理鉴权（`authentication`）与安全注意[^c1-6]

---

### 本章小结

- 被墙的是「命令行 / apt / git / Docker」整条链路，需要统一中转站。
- 服务器端选 **mihomo 内核**：轻量、订阅友好、能被 systemd 守护。
- 路线定为**显式代理**；TUN 留作第六章末尾的进阶方向。
- 所有流量汇聚到 mihomo 的 `mixed-port: 7890`；动手前按 1.5 清单备齐资源。

下一章开始动手：下载 mihomo 二进制、安装，并用 systemd 把它守护起来。

---

**素材引用**：S1（Releases/架构）、S2（general/allow-lan）、S3（订阅导入）、S4（mixed-port 入站）、S5（systemd）、S6（Docker daemon）、S7（Docker CLI）、S12（既有笔记）。

路线和清单都备好了。接下来第二章开始动手：下载 mihomo 内核二进制、安装到系统，并用 systemd 把它守护起来。

---

## 第二章：安装 mihomo 内核

> [!note] 本章目标
> 把 mihomo 内核二进制装到 `/usr/local/bin/`，再用 systemd 把它守护起来，实现开机自启、崩溃自动重启，最后验证服务存活。订阅节点与完整 `config.yaml` 留到下一章，本章先放一个最小占位配置让它能跑起来。

> 章节产物：`/usr/local/bin/mihomo` + `/etc/mihomo/config.yaml`（占位）+ `/etc/systemd/system/mihomo.service`

### 2.1 按架构下载二进制

mihomo 在 GitHub Releases 发布的是 `.gz` 压缩的静态二进制，下载即用、无需编译[^c2-s1]。关键是选对 CPU 架构的包：x86_64 的服务器选 **amd64** 包，ARM 的服务器选 **arm64** 包，装错会直接报 `Exec format error`。

先确认架构：

```bash
uname -m
# 输出 x86_64  → 选 amd64 包
# 输出 aarch64 → 选 arm64 包
```

> [!tip] 大白话：架构 = CPU 的鞋码
> 把 `uname -m` 想成量鞋码。不同架构的 CPU 像不同鞋码，买错码的鞋穿不进去。所以先量（`uname -m`）再买（选对应架构的包），装错包时系统会回一句 `Exec format error`——相当于鞋码不对，塞不进去。

用变量把版本和架构写清楚，方便以后升级换版本：

```bash
ARCH=amd64        # aarch64 机器改成 arm64
VERSION=v1.18.10  # 以 GitHub Releases 页最新 tag 为准

wget "https://github.com/MetaCubeX/mihomo/releases/download/${VERSION}/mihomo-linux-${ARCH}-${VERSION}.gz"
```

改用 curl 下载的话是：`curl -fL -O "https://github.com/MetaCubeX/mihomo/releases/download/${VERSION}/mihomo-linux-${ARCH}-${VERSION}.gz"`

> [!warning] 下载源被墙了怎么办
> GitHub Releases 的下载域名（`objects.githubusercontent.com`）在国内经常连不上。三种绕法：
> 1. 如果这台服务器已能走某个代理，先 `export https_proxy=...` 再下载；
> 2. 用可信的镜像加速前缀（如 `ghproxy` 一类）替换 URL 里的 `github.com`，注意甄别；
> 3. 在本地电脑用浏览器打开 Releases 页下载对应的 `.gz`，再 `scp mihomo-linux-*.gz user@服务器IP:/tmp/` 传到服务器上。

### 2.2 解压、改名、放入 /usr/local/bin/

```bash
gzip -d "mihomo-linux-${ARCH}-${VERSION}.gz"          # 解出同名二进制
mv "mihomo-linux-${ARCH}-${VERSION}" mihomo          # 改成统一的名字
sudo mv mihomo /usr/local/bin/                        # 放进 PATH 搜索目录
sudo chmod +x /usr/local/bin/mihomo                   # 加执行权限
mihomo -v                                             # 验证版本，能打印就说明装好了
```

> [!note] 为什么放 `/usr/local/bin/`
> 它默认在 `PATH` 里，systemd 的 `ExecStart` 和命令行直接敲 `mihomo` 都能找到，不用写绝对路径（systemd 里我们仍写绝对路径更稳妥）。改名 `mihomo` 只是统一命名，不强制。

### 2.3 创建配置目录 /etc/mihomo/（最小占位）

mihomo 启动时必须指定工作目录，订阅、规则、日志等相对路径都以此目录为基准[^c2-s5]。这里先放一个只声明入站端口的最小占位配置，证明服务能跑起来：

```bash
sudo mkdir -p /etc/mihomo
sudo tee /etc/mihomo/config.yaml >/dev/null <<'EOF'
mixed-port: 7890        # HTTP + SOCKS5 混合入站端口
allow-lan: true         # 允许局域网设备（含后续的 Docker 容器）接入
bind-address: "*"       # 绑定所有网卡 IP
mode: rule              # 规则分流模式
log-level: info
EOF
```

> [!tip] 大白话：mixed-port = 一个门牌号，两种业务
> 把 `mixed-port: 7890` 想成楼下收发室只留了一个门牌号，既能收 HTTP 快递也能收 SOCKS5 快递。这样 curl、apt、git、Docker 都用 `127.0.0.1:7890` 这一个地址找它，不用记两个端口。
>
> 这一份是"占位牌"，还没有真正的订阅节点——下一章会拿完整配置覆盖它。

### 2.4 用 systemd 守护 mihomo

没有守护，mihomo 一断线或服务器重启就没了。创建 systemd unit 让它开机自启、崩溃自愈：

```ini
# /etc/systemd/system/mihomo.service
[Unit]
Description=mihomo Daemon, Another Clash Kernel.
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/mihomo -d /etc/mihomo
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5
LimitNOFILE=1000000
LimitNPROC=500
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_DAC_READ_SEARCH
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

写入文件后依次执行：

```bash
sudo tee /etc/systemd/system/mihomo.service >/dev/null <<'EOF'
# 把上面完整 unit 内容粘贴进来
EOF

sudo systemctl daemon-reload          # 让 systemd 重新读取 unit 文件
sudo systemctl enable mihomo          # 开机自启
sudo systemctl start mihomo           # 立即启动
systemctl status mihomo               # 查看状态，应显示 active (running)
```

> [!tip] 大白话：这几个配置各管什么事
> - `Type=simple`：把 systemd 想成"前台登记处"，进程一跑起来就算启动成功，不额外等它喊"我准备好了"。
> - `Restart=always`：给进程装了个"复活甲"，只要非正常退出，5 秒后（`RestartSec=5`）自动拉起来，服务器重启后也能开机自启。
> - `CapabilityBoundingSet` / `AmbientCapabilities`：把 `CAP_NET_ADMIN`、`CAP_NET_RAW` 想成两张门禁卡——mihomo 平时权限受限，拿到这两张卡才有资格管理网络配置，为后续开 TUN/透明代理等能力预留（本笔记暂不用，提前发卡）。
> - `LimitNOFILE=1000000`：把"文件描述符"想成快递分拣员手上能同时端的包裹数。代理连接一多，默认上限不够会报 `too many open files`，调到 100 万基本够用。

`ExecReload=/bin/kill -HUP $MAINPID` 表示改配置后 `sudo systemctl reload mihomo` 即可热重载，不必重启进程（第 3 章会用到）。

### 2.5 查看运行日志

```bash
journalctl -u mihomo -ocat -e    # 只看最近几行，-ocat 去掉多余前缀
journalctl -u mihomo -f          # 实时滚动跟踪
```

日志里出现 `Start initial provider` 或 `RESTful API listening` 之类即说明内核正常启动；有报错就按日志排查（最常见是 `config.yaml` 语法问题或端口被占）。

### 2.6 自检：服务是否存活

```bash
curl -I https://www.gstatic.com/generate_204
```

预期返回 `HTTP/2 200`。这一步能打通，说明 mihomo 的入站端口在监听、且链路能出网。

> [!warning] 如果暂时不是 200，别慌
> `gstatic.com` 是 Google 的连通性检测端点。占位配置下还没有订阅节点，**真正拿到 200 需要下一章把节点订阅写进 config.yaml**。本章的即时验收标准是：`systemctl status mihomo` 显示 `active (running)`，`journalctl` 无致命错误，`curl -I http://127.0.0.1:7890` 能建立 TCP 连接即可。

### 本章小结

- 先用 `uname -m` 确定架构（amd64 / arm64），再下载对应 `.gz` 包；下载源被墙可用镜像或本地上传。
- 解压、改名、放进 `/usr/local/bin/`、加执行权限，`mihomo -v` 验证。
- 建 `/etc/mihomo/` 目录并放一份最小占位 config.yaml，声明 `mixed-port: 7890`。
- systemd unit 让 mihomo 开机自启、崩溃自愈，并通过 `LimitNOFILE`、Capabilities 做资源与权限准备。
- 用 `systemctl status` 和 `journalctl` 验收服务存活；`generate_204` 的 200 需要等节点就绪。

下一章会往 `/etc/mihomo/config.yaml` 里写进订阅节点、节点分组和规则，让这台刚"醒来"的内核真正具备分流出网的能力。

mihomo 内核已经跑起来，但目前只有占位配置、还没有真实节点。第三章就把订阅节点、节点分组和分流规则写进 config.yaml，让这台内核真正具备代理出网的能力。

---

## 第三章：配置 config.yaml

上一章我们已经把 mihomo 二进制装好并跑起了一个能启动的服务，但此时它还没有任何节点可用——代理是空的。本章解决的核心问题是：**怎样写一份能让 mihomo 真正代理流量的 `config.yaml`**，包括开几个入口端口、如何导入订阅节点、如何把节点分组，以及一份可直接复制的最小配置。这是整个代理链路里最容易被「抄了配置却连不上」的一章，值得放慢速度读完。

### 3.1 顶层入站配置：先看门面

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

### 3.2 `allow-lan: true` + `bind-address: "*"`：让 Docker 容器能用代理

这两个选项是后面第五章节 Docker 容器能出网的前提，先在这里埋好：

- **`allow-lan: true`**：允许除本机外的设备接入代理端口。
- **`bind-address: "*"`**：把监听地址绑定到所有网卡 IP，而不是默认的 `127.0.0.1`。

为什么要同时开？因为 Docker 容器访问宿主机时走的是 **docker0 网桥**，源地址是网桥网段的 IP（如 `172.17.0.1`），**不是** `127.0.0.1`。只有 `allow-lan: true` 且 `bind-address: "*"` 时，mihomo 才愿意接受来自 docker0 网桥的连接。换句话说：`allow-lan` 决定「允不允许别人进」，`bind-address` 决定「门开在哪些墙」[^c3-1][^c3-2]。

> [!warning] 安全警告
> 一旦 `bind-address: "*"`，如果你的服务器有公网 IP，代理端口对公网也是开放的。**HTTP/SOCKS 明文代理被公网扫描到后极易被劫持做跳板**。如果服务器暴露在公网，务必在顶层加 `authentication`（用户名+密码），或者用 ufw 只放行内网来源（`ufw allow from 192.168.0.0/16 to any port 7890 proto tcp`）。不推荐为图省事直接公网开放代理端口[^c3-1]（可对照既有笔记 [[外网如何使用代理进行翻墙]] 里的 Clash 认证部分）。

> [!tip] 大白话：allow-lan 像「门禁开放」
> 默认门禁只放行自己人（127.0.0.1）；`allow-lan: true` 是把公司访客也放进来（局域网设备）；`bind-address: "*"` 则是把所有大门（所有网卡 IP）都装上这套门禁。Docker 容器走的是后门（docker0 网桥），不开后门它们就进不来——但门全开了，小偷（公网扫描）也可能进来，所以要加锁（authentication）或拉警戒线（ufw）。

### 3.3 订阅导入：`proxy-providers`

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

### 3.4 节点分组：`proxy-groups`

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

### 3.5 `rules`：规则分流简介

规则决定「这个请求走代理还是直连」，从上到下逐条匹配，命中即停。最小可运行配置只需一条兜底：

```yaml
rules:
  - MATCH,PROXY    # 其余全部走 PROXY 组
```

- **`MATCH`**：兜底规则，放在最后，匹配所有没被前面规则命中的流量。没有它，未知域名会被直接拒绝或直连，经常导致「有规则但就是不代理」的困惑。
- **`GEOIP,CN,DIRECT`（可选）**：按目标 IP 归属地分流，国内 IP 直连、国外走代理，可放在 `MATCH` 之前。它依赖 geoip 数据库（mihomo 会自动拉取），本笔记最小配置先不引入，第四章会用「域名级」验证代替。

### 3.6 最小可运行 config.yaml（可直接复制）

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

### 3.7 落地提示：格式确认、SAFE_PATHS 与重载

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

config.yaml 配置完成，mihomo 已经能真正代理流量。第四章接着解决「系统里的命令怎么自动走这个代理」——通过环境变量、apt 配置和 git 配置，让命令行工具、apt、git 都从 7890 端口出门。

---

## 第四章：系统级代理接管

mihomo 内核已经跑起来、`7890` 端口正在监听，但你可能发现一个尴尬的事实：`curl https://www.google.com` 依然超时。原因很简单——mihomo 只是「开了一扇门」，系统里的命令根本不知道要往这扇门走。本章要做的，就是发三张「通知单」：环境变量通知 curl/wget 全家，apt 配置通知软件包管理器，git 配置通知版本控制工具，让它们全部乖乖从代理端口出门。

> [!note] 本章成果
> - `/etc/profile.d/proxy.sh`：curl / wget 等所有命令行工具走代理
> - `/etc/apt/apt.conf.d/proxy.conf`：apt 走代理
> - `~/.gitconfig`：git 走代理
> - 四条验证命令确认链路打通

### 为什么系统命令需要环境变量才能走代理

非 TUN 模式下，mihomo 只在你指定的端口监听 HTTP/SOCKS5 入站，它**不会**去劫持系统里每个进程的网络流量。每个程序要不要走代理，得由程序自己决定。好在绝大多数命令行工具（curl、wget、git 的 http 传输等）都基于 libcurl，而 libcurl 有一个统一约定：读取环境变量 `[scheme]_proxy`，决定某个协议该走哪个代理 [^c4-1]。

> [!tip] 大白话
> 把 mihomo 想成一个「收发室」，7890 是收发室的门。系统命令默认都是自己直接出门寄信，压根不知道有收发室存在。环境变量就是发给每个命令的「通知单」：喂，你的 http 信件统一从 7890 那个门走。没有通知单，命令们照旧直连，当然连不上被墙的站点。

### 全局环境变量：/etc/profile.d/proxy.sh

把代理变量写进 `/etc/profile.d/proxy.sh`，所有登录 shell（SSH 会话、新开的终端）都会自动加载。完整文件如下（先睹为快，下面逐段拆解）：

```bash
# /etc/profile.d/proxy.sh
# 小写形式：libcurl 认这套
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
export all_proxy="socks5://127.0.0.1:7890"

# 大写形式：部分应用（如部分 java/go 程序）只读大写
export HTTP_PROXY="http://127.0.0.1:7890"
export HTTPS_PROXY="http://127.0.0.1:7890"
export ALL_PROXY="socks5://127.0.0.1:7890"

# 不走代理的地址：本机与局域网
export no_proxy="localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,.local"
export NO_PROXY="$no_proxy"
```

#### 大小写坑：为什么小写、大写都要写

libcurl 有一个著名的历史规矩：对 `http` 协议它**只认小写 `http_proxy`**，大写 `HTTP_PROXY` 会被主动忽略（早期有人利用该环境变量做 CGI 注入攻击，libcurl 便对大写形式特殊处理以免被劫持）。而 `https_proxy`、`all_proxy` 的大小写形式则都认 [^c4-1]。所以最稳妥的写法是小写、大写各写一份，值相同，互不冲突。

> [!warning] 大小写坑
> 只写 `export HTTP_PROXY=...`（全大写）时，`curl http://xxx` 不会走代理！务必保证小写 `http_proxy` 存在。这也是「矛盾表」里系统命令与 Docker 文档示例的差异根源——Docker 容器会自动注入大小写两套，而系统命令必须自己补齐。

#### export 与 source 的生效说明

- `export`：把变量标记为「可传给子进程」。不加 `export` 时变量只是当前 shell 私有，curl / git 这些子进程根本看不到。
- `source`：改完 `/etc/profile.d/proxy.sh` 后，**已打开的终端不会自动生效**。要么重新登录，要么执行 `source /etc/profile.d/proxy.sh` 让当前 shell 立即重读。

> [!tip] 大白话
> export 就像把工牌挂到胸前，孩子进程才认；只写 `VAR=xxx` 不 export，等于工牌揣在兜里。source 是「现在就重新读一遍通知」；不 source 就只能重开终端（重新登录）才生效。

### apt 代理：/etc/apt/apt.conf.d/proxy.conf

apt 其实也读 `http_proxy` 环境变量，但写进独立配置文件更持久、更明确，且对无 shell 的 systemd 服务场景也生效。新建：

```
// /etc/apt/apt.conf.d/proxy.conf
Acquire::http::Proxy "http://127.0.0.1:7890";
Acquire::https::Proxy "http://127.0.0.1:7890";
```

两个进阶要点 [^c4-2]：

- 支持 `socks5h://127.0.0.1:7890`：走 SOCKS5，且 **DNS 在远端解析**，可解析被污染的域名、更隐私。
- 特殊值 `Acquire::http::Proxy "DIRECT";`：对该协议**强制直连**，完全不走代理。

改完立即生效，无需重启任何服务，直接 `apt update` 验证即可。

### git 代理：~/.gitconfig

git 的 http 传输同样会读环境变量，但更推荐在 git 自己的配置里显式声明，避免污染全局环境。代理 URL 语法：`[protocol://][user[:password]@]proxyhost[:port]` [^c4-3]。

```bash
# 全局默认走代理
git config --global http.proxy "http://127.0.0.1:7890"
git config --global https.proxy "http://127.0.0.1:7890"

# 只对某个远程仓库覆盖（例如公司内网仓库直连，github 走代理）
git config --global http.https://github.com/.proxy "http://127.0.0.1:7890"
git config --global http.http://gitlab.internal/.proxy ""
```

`http.<url>.proxy` 的匹配规则是「`http.` + 仓库 URL 前缀 + `.proxy`」，git 会选**最长匹配**的那条覆盖全局设置；写成空字符串 `""` 表示该 URL 直连。生成的 `~/.gitconfig` 形如：

```ini
[http]
	proxy = http://127.0.0.1:7890
	https://github.com/.proxy = http://127.0.0.1:7890
[http "http://gitlab.internal/"]
	proxy =
```

> [!tip] 大白话
> 全局 `http.proxy` 像「所有外发信件统一送收发室」，`http.<url>.proxy` 像「给某个特定客户单独指定寄件地址」。git 寄信时先看有没有专属地址（最长匹配优先），没有才退回全局默认。这样内网仓库照旧直连，被墙的 GitHub 走代理，互不干扰。

### 验证：四条命令确认链路

```bash
# 1. 走代理：应返回 200（Google 需代理才能访问）
curl -I https://www.google.com

# 2. 规则分流直连：应返回 200（mihomo 规则放行 baidu 直连）
curl -I https://www.baidu.com

# 3. apt 走代理拉取索引
sudo apt update

# 4. git 走代理访问 GitHub
git ls-remote https://github.com/git/git.git HEAD
```

预期：前两条 `curl -I` 输出首行都是 `HTTP/2 200`；`apt update` 不再超时、正常拉取索引；`git ls-remote` 输出一串 commit hash。

> [!tip] 大白话
> 这四条命令就是「验货」：google 验证代理真的通，baidu 验证规则分流没有把所有流量都硬塞进代理（否则反而变慢），apt 和 git 验证两个最常踩坑的应用也接上了代理。四条全绿，系统级代理接管就算完成了。

### 本章小结

- 非 TUN 模式下，每个命令要自己决定走不走代理；libcurl 系工具统一认 `[scheme]_proxy` 环境变量。
- `/etc/profile.d/proxy.sh` 小写、大写都写，重点保证小写 `http_proxy` 存在；改完要 `source` 或重开终端才生效。
- apt 用 `/etc/apt/apt.conf.d/proxy.conf` 持久配置，支持 `socks5h://` 远端 DNS 与 `DIRECT` 直连。
- git 用 `git config --global http.proxy` 显式声明，`http.<url>.proxy` 可按单个仓库精确覆盖。
- 用 google / baidu / apt update / git ls-remote 四条命令，分别验证「走代理」「规则直连」「apt」「git」四条链路。

下一章轮到 Docker：它比系统命令更讲究，**拉镜像**和**容器内应用出网**是两条路径、两个配置文件，搞混了怎么配都不通。

系统命令、apt、git 都已接管。第五章轮到 Docker——拉镜像和容器内应用出网是两条独立路径，分别在 daemon.json 和 ~/.docker/config.json 里配置。

---

## 第五章：Docker 走代理

> 本章目标：让 Docker 的两类"上网"行为——`docker pull` 拉镜像、容器内应用出网——都走前面搭好的 mihomo 代理。[^c5-1] [^c5-2]

镜像仓库（Docker Hub、ghcr.io、registry.k8s.io）和国内直连一样会被墙，而容器里的程序（npm、pip、爬虫、各色服务）也要访问外网。很多人在这一步最困惑：为什么配了代理，`docker pull` 还是超时？为什么容器里 curl 又没走代理？答案只有一个——**Docker 有两条互相独立的网路，配置位置完全不同**。

### 5.1 先分清两条路径

| 对比项 | 拉镜像 | 容器内应用出网 |
| --- | --- | --- |
| 谁负责 | dockerd（Docker 守护进程） | 容器进程本身 |
| 配置位置 | `/etc/docker/daemon.json` 或 systemd drop-in | `~/.docker/config.json` 或 `docker run --env` |
| 生效时机 | 重启 dockerd 后 | 只对新容器/新构建生效 |
| 代理地址 | 宿主机 `127.0.0.1:7890` 即可 | 必须用**宿主机局域网 IP**，不能用 `127.0.0.1` |

> [!tip] 大白话
> 把 dockerd 想成**仓库管理员**，容器是**在仓库里租了办公室的住户**。拉镜像是管理员"进货"，要走管理员的专用进货通道（daemon.json）；容器里应用出网是住户"自己出门办事"，得给住户发门禁卡（config.json / --env）。两条通道互不相通——配好了进货通道，不代表住户也能出门。

**关键结论**：先确认你要解决的是"拉镜像"还是"容器出网"，再去对应的位置配置。

### 5.2 路径一：让 dockerd 走代理（拉镜像）

#### 5.2.1 推荐：daemon.json 的 proxies 段

先睹为快，完整文件 `/etc/docker/daemon.json`：

```json
{
  "proxies": {
    "http-proxy": "http://127.0.0.1:7890",
    "https-proxy": "http://127.0.0.1:7890",
    "no-proxy": "*.local,localhost,127.0.0.1"
  }
}
```

逐段拆讲：

- `http-proxy` / `https-proxy`：dockerd 拉镜像时走的代理。这里用 `127.0.0.1` 是**对的**——dockerd 和 mihomo 同在宿主机网络，不属于容器网络。
- `no-proxy`：**直连白名单**，逗号分隔。`.local` 匹配所有 `.local` 域（含子域）；`localhost,127.0.0.1` 保证访问本机时绕过代理。

写完后**必须重启 Docker 才生效**（易错点之一）：[^c5-1]

```bash
sudo systemctl restart docker
```

> [!warning] 优先级
> daemon.json 的 proxies **优先级高于环境变量**。如果你同时用了下面的 systemd drop-in 环境变量方式，以 daemon.json 为准；两者二选一即可，不要同时维护两处。[^c5-1]

#### 5.2.2 替代方案：systemd drop-in

不想碰 JSON，或想用环境变量的，可以给 dockerd 注入环境变量。完整文件 `/etc/systemd/system/docker.service.d/http-proxy.conf`：

```conf
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1,.local"
```

生效需要两步：

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d
sudo systemctl daemon-reload    # 重新读取 drop-in 文件
sudo systemctl restart docker
```

验证 dockerd 实际拿到的环境变量：

```bash
systemctl show --property=Environment docker
```

> [!warning] systemd 特殊字符
> 代理 URL 里若含 `# ? ! ( ) [ ] { }` 等特殊字符（常见于带密码的代理），systemd 会把它当指令解析，需要**双重转义**：`%` 写成 `%%`。例如密码 `pa%ss` 应写成 `Environment="HTTP_PROXY=http://user:pa%%ss@127.0.0.1:7890"`。[^c5-1]

### 5.3 路径二：让容器内应用走代理（出网）

#### 5.3.1 推荐：~/.docker/config.json 的 proxies.default

先睹为快，完整文件 `~/.docker/config.json`：

```json
{
  "proxies": {
    "default": {
      "httpProxy": "http://192.168.1.100:7890",
      "httpsProxy": "http://192.168.1.100:7890",
      "noProxy": "*.local,localhost,127.0.0.1"
    }
  }
}
```

逐段拆讲：

- 键名是**驼峰**（`httpProxy`/`httpsProxy`/`noProxy`），和 daemon.json 的 kebab-case（`http-proxy`）不同。
- **必须把 `192.168.1.100` 换成你宿主机的局域网 IP**（`ip addr` 可查），不能用 `127.0.0.1`，原因见 5.4。[^c5-3] [^c5-4]

保存即生效，**不需要重启 Docker**。但关键点是：**只对新创建的容器和新构建生效，已存在的容器不受影响**（易错点之一）。[^c5-2] 它会在创建容器/构建时自动注入一组环境变量：`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`（大小写都会注入）。

> [!tip] 大白话
> config.json 像是**入职时发的门禁卡**：只发给"之后入职的新员工"，老员工拿不到。所以改完 config.json 后，想让某个老容器走代理，唯一的办法是**重建**它（`docker compose down && up -d`），而不是 `docker restart`。

#### 5.3.2 单容器临时指定：docker run --env

不想改全局配置，只想让某一个容器走代理：

```bash
docker run --rm -it \
  --env HTTP_PROXY=http://192.168.1.100:7890 \
  --env HTTPS_PROXY=http://192.168.1.100:7890 \
  alpine sh
```

`--env` 是单次覆盖，不写进任何配置文件，适合临时测试。

#### 5.3.3 构建镜像时：docker build --build-arg

构建阶段（`RUN` 步骤里的 npm、pip 等）要走代理，用 `--build-arg` 传入：

```bash
docker build \
  --build-arg HTTP_PROXY=http://192.168.1.100:7890 \
  --build-arg HTTPS_PROXY=http://192.168.1.100:7890 \
  .
```

`HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` 是 Docker **预定义构建参数**，无需在 Dockerfile 里额外 `ARG` 声明，`RUN` 阶段即可读到。

> [!warning] 不要在 Dockerfile 里用 ENV 硬编码代理
> `ENV HTTP_PROXY=http://...` 会把代理地址（含可能的账号密码）**永久写进镜像的配置层**，任何拿到镜像的人都能看到，换台机器也会失效。正确做法就是上面的 `--build-arg`，只在构建时临时传入，不固化进镜像。[^c5-2]

### 5.4 最容易踩的坑：容器内访问宿主机代理

容器是**隔离的网络命名空间**，容器内的 `127.0.0.1` 指向容器自己，而不是宿主机。所以在容器里把代理配成 `127.0.0.1:7890`，连的是一个容器内不存在的端口，自然不通。[^c5-3] [^c5-4]

> [!tip] 大白话
> 每个容器是一间**独立的酒店房间**，`127.0.0.1` 是"这间房自己"的门牌。mihomo 在宿主机，相当于**酒店前台**。你在房间里拨 `127.0.0.1`，只会打到房间内部的分机，永远打不到前台。要联系前台，得拨前台的外线号码（宿主机 IP）。

容器内访问宿主机代理，三种正确写法任选其一：

1. **宿主机局域网 IP**：`http://192.168.1.100:7890`（最直观，5.3 的 config.json 用的就是它）
2. **docker0 网关**：默认桥接网络的网关就是宿主机，`http://172.17.0.1:7890`
3. **host-gateway 魔法域名**：
   ```bash
   docker run --add-host=host.docker.internal:host-gateway \
     --env HTTP_PROXY=http://host.docker.internal:7890 alpine sh
   ```

> [!warning] 前提：mihomo 必须允许局域网访问
> 以上三种方式能通，是因为第 3 章的 config.yaml 里开了 `allow-lan: true` + `bind-address: "*"`。如果没开，宿主机代理端口只监听 `127.0.0.1`，容器从外部网段访问会被拒绝。安全起见，确认该端口没有暴露到公网（详见下一章安全注意）。

### 5.5 端到端验证

按顺序跑一遍，全部通过说明两条路径都通了：

```bash
# 1) 拉镜像：找一个被墙仓库的镜像，能拉下来就说明 daemon 代理生效
docker pull registry.k8s.io/pause:3.9

# 2) 查看容器内自动注入的代理环境变量（config.json 生效的标志）
docker run --rm alpine sh -c 'env | grep -i proxy'
# 预期输出（IP 换成你的宿主机 IP）：
# HTTP_PROXY=http://192.168.1.100:7890
# HTTPS_PROXY=http://192.168.1.100:7890
# NO_PROXY=*.local,localhost,127.0.0.1
# 以及对应的小写 http_proxy / https_proxy / no_proxy

# 3) 容器内访问外网（alpine 自带 wget；要 curl 可用 curlimages/curl 镜像）
docker run --rm --env HTTP_PROXY=http://192.168.1.100:7890 \
  alpine sh -c 'wget -qO- https://www.google.com | head -c 200'
```

如果第 1 步失败：检查 daemon.json 是否已重启、`no-proxy` 是否误伤了目标域名。如果第 2/3 步失败：多半是代理地址用了 `127.0.0.1`，或 mihomo 没开 `allow-lan`。

---

### 本章小结

- Docker 有两条独立网路：**拉镜像（daemon 级）**和**容器出网（CLI 级）**，配置位置、生效时机都不同，先定位问题再动手。
- 拉镜像用 `/etc/docker/daemon.json` 的 `proxies` 段（或 systemd drop-in 环境变量），改完必须 `systemctl restart docker`；daemon.json 优先级高于环境变量。
- 容器出网用 `~/.docker/config.json` 的 `proxies.default`（写**宿主机 IP**），只对新容器/新构建生效，老容器要重建；单容器临时用 `docker run --env`，构建用 `docker build --build-arg`。
- **绝不要**在 Dockerfile 用 `ENV` 写代理地址——会固化进镜像、泄露敏感信息。
- 容器内访问宿主机代理：用宿主机局域网 IP / `172.17.0.1` / `host.docker.internal`，前提是 mihomo 开了 `allow-lan` + `bind-address: "*"`。

下一章把整条链路（mihomo → 系统命令 → apt/git → Docker）串成一份端到端验证清单，并把所有易错点汇总成一张速查表，方便以后随时回查。

---

第五章把 Docker 的拉镜像与容器出网两条路径都配好了。第六章把整条链路串成一份端到端验证清单，并汇总常见坑与安全注意，作为日后回查的速查表。

---

## 第六章：验证清单与常见坑

> 本章是整本笔记的"验收"章节：按顺序跑一遍端到端验证清单，确认前几章的每一步都真实生效；再对照常见坑汇总表，快速定位"链路哪里断了"。建议把本章当作一张贴在服务器旁的自查表，随时回查。

### 端到端验证清单（按图索骥）

> [!tip] 大白话
> 把整条代理链路想成一根水管：从水龙头（mihomo 内核）到最末端的用户（Docker 容器），每一段都要通。按下面的顺序从近到远逐段检查，哪一段断了就先修哪一段——这就是排障的"按图索骥"。

按顺序执行，任何一步不符合期望，就停在这一步排查：

```bash
# 1. mihomo 进程是否存活
systemctl status mihomo --no-pager
# 期望：● mihomo.service - active (running)
```

```bash
# 2. 内核本身能否出网（HTTP 探活端点）
curl -I https://www.gstatic.com/generate_204
# 期望：HTTP/1.1 204 No Content（任何 2xx 都算连通）
```

```bash
# 3. 被墙站点是否走代理
curl -I https://www.google.com
# 期望：HTTP/2 200 —— 说明系统环境变量已把 curl 指向 mihomo
```

```bash
# 4. 国内站点是否按规则直连
curl -I https://www.baidu.com
# 期望：HTTP/2 200 —— 规则分流，百度命中直连策略
```

```bash
# 5. apt 软件源
sudo apt update
# 期望：命中代理、不再超时，正常拉取软件索引
```

```bash
# 6. git 访问 GitHub
git ls-remote https://github.com/<你的用户名>/<仓库>.git
# 期望：返回 refs/heads/main 等引用，而非 Connection timed out
```

```bash
# 7. Docker 拉取被墙镜像
docker pull alpine
# 期望：daemon 经代理拉取成功
```

```bash
# 8. 容器内出网（最后一公里）
docker run --rm alpine wget -qO- https://www.gstatic.com/generate_204 && echo CONTAINER_OK
# 期望：输出 CONTAINER_OK，说明容器已通过宿主机代理出网
```

全部通过，说明 **系统命令 → apt → git → Docker daemon → Docker 容器** 五条链路全部打通。

### NO_PROXY 匹配规则：白名单怎么填

> [!tip] 大白话
> 把 `NO_PROXY` 想成快递的"白名单"：名单上的地址，快递员（代理）不接单，直接送货上门（直连）；不在名单上的地址，一律走代理。

> [!note] 核心概念
> `NO_PROXY`（小写 `no_proxy`）是代理设置里的"排除名单"，命中规则的主机名/IP 将绕过代理直连。Docker daemon、容器环境变量和 libcurl 都遵守这套规则。常用写法如下：

| 写法 | 匹配范围 | 示例说明 |
|------|---------|---------|
| `example.com` | 匹配域名本身 + 其所有子域 | `example.com` 和 `foo.example.com` 都直连 |
| `.example.com` | 只匹配子域，不含域名本身 | 仅 `foo.example.com` 直连；`example.com` 仍走代理 |
| `192.168.1.5` | 精确匹配该 IP | 该 IP 直连 |
| `192.168.1.0/24` | CIDR 网段内全部 IP | 该网段全部直连 |
| `example.com:8080` | 仅该域名 + 该端口 | `example.com` 的 8080 端口直连，其他端口走代理 |
| `*` | 全部直连 | 相当于关闭代理 |

规则用逗号分隔，例如 `no_proxy=localhost,127.0.0.1,.local`。

### 常见坑汇总表

> [!note] 核心概念
> 排障时先看"现象"对上哪一行，再按"解法"操作。多数"代理不生效"都不是配置写错，而是"改了没重启 / 只对旧的生效 / 大小写不对"这三类。

| 坑位 | 现象 | 解法 |
|------|------|------|
| daemon.json 改后未重启 docker | `docker pull` 仍走直连 | `sudo systemctl restart docker`，改配置后必须重启 |
| `~/.docker/config.json` 只对新容器生效 | 已存在容器仍直连 | 删除旧容器重新 `docker run`；config.json 只在创建/构建时注入代理变量 |
| `http_proxy` 大小写 | 大写 `HTTP_PROXY` 下，curl 走 http 仍直连 | libcurl 只认小写 `http_proxy`；小写+大写都写，或用 `all_proxy` 兜底 |
| systemd 代理 URL 特殊字符 | systemd 启动失败或 Environment 被截断 | URL 中 `#?!()[]{}` 等字符每个加 `%%` 双重转义 |
| 订阅 `path` 不在 `-d` 目录内 | mihomo 拉订阅失败，日志报路径/权限错误 | `path` 用相对路径放在 `/etc/mihomo/` 内，或设置 `SAFE_PATHS` 环境变量 |
| 容器内用 `127.0.0.1` 访问宿主机代理 | 容器内程序连 `127.0.0.1:7890` 失败 | 容器内 127.0.0.1 是容器自己；改用宿主机局域网 IP / docker0 网关 `172.17.0.1` / `host.docker.internal` |
| 订阅 URL 本身被墙（bootstrap 死结） | mihomo 刚启动时订阅拉不下来 | 代理要靠订阅、订阅又要代理，形成死结；先在有代理的机器上把订阅文件下载到本地导入，或临时手动放文件 |

### 安全注意：别把代理裸奔在公网

> [!tip] 大白话
> 把在公网开放代理端口想成把家门钥匙挂在门口：任何路过的人都能开门（用你的代理）。没有 `authentication` 的开放代理会被全网扫描器盯上，被用来蹭流量、刷接口，甚至成为违法流量的跳板——IP 被封时追查的还是你。

- `listen: 0.0.0.0` / `bind-address: "*"` 让 Docker 容器能用代理，但也等于对公网敞开大门；**必须**在 config.yaml 配置 `authentication`（用户名/密码）。mihomo 默认对 `127.0.0.1/8` 跳过鉴权，只有本机直连才免密码。
- 若服务器有 ufw：`sudo ufw allow 7890/tcp` 只在确实需要局域网设备访问代理时才放行；本机使用无需放行。
- **不建议**把 7890 等代理端口开放到公网；容器/局域网访问优先用内网 IP + 认证。
- `external-controller` 保持 `127.0.0.1:9090`，**不要**改为 `0.0.0.0` 暴露公网，否则控制 API 可被远程调用。

### 进阶方向：TUN / 透明代理（本笔记不含）

本笔记走"显式代理"路线，需要每个应用显式设置代理变量。若遇到不读环境变量的程序（GUI 应用、某些守护进程），可继续扩展：

- **mihomo TUN 模式**：在 config.yaml 加 `tun:` 段（`enable: true`、`stack: system` 或 `gvisor`），由内核接管路由，全局无感代理；需要 `CAP_NET_ADMIN` / `CAP_NET_RAW` 能力。
- **iptables + redsocks**：把 TCP 流量透明重定向到本机代理端口，经典但配置繁琐。
- 两者的共同代价：配置不当会**影响全部流量**（含 SSH），建议在测试机先行验证。

### 本章小结

- 端到端验证按"mihomo → curl → apt → git → Docker 拉取 → 容器出网"的顺序逐段排查，哪段断修哪段。
- `NO_PROXY` 是白名单：域名、子域、IP、CIDR、端口都能精确控制，`*` 则全部直连。
- 绝大多数"不生效"是三类原因：改了没重启、只对新容器生效、代理变量大小写不对。
- 公网开放代理端口必须加 `authentication`；`external-controller` 永不暴露公网。
- TUN/透明代理是后续扩展方向，能让不读环境变量的应用也走代理。

至此六章全部完成。需要在真实服务器上从零落地时，第二章 → 第五章的顺序就是部署路径，本章则作为验收与排查手册。相关既有笔记可交叉参考：[[docker/docker进行代理]]、[[外网如何使用代理进行翻墙]]。

---

## 脚注

[^c1-1]: 素材来源 S1：mihomo GitHub Releases，按 amd64/arm64 选 `.gz` 二进制。
[^c1-2]: 素材来源 S5：systemd 示例，`Restart=always` 崩溃自愈。
[^c1-3]: 素材来源 S4：`mixed-port` 同时提供 HTTP 与 SOCKS5。
[^c1-4]: 素材来源 S3/S2：`proxy-providers` 订阅导入；sing-box 需转换。
[^c1-5]: 素材来源 S12：既有笔记（容器用宿主机 IP 而非 127.0.0.1）。
[^c1-6]: 素材来源 S4/S2：入站暴露公网需加 `authentication`。

[^c2-s1]: mihomo 官方 GitHub Releases（内核二进制下载）— https://github.com/MetaCubeX/mihomo/releases
[^c2-s5]: mihomo 官方文档·systemd 服务示例 — https://wiki.metacubex.one/start/

[^c3-1]: S2：mihomo 官方文档 General config（allow-lan / bind-address / authentication / external-controller / mode / log-level）。
[^c3-2]: S4：mihomo 官方文档 inbound（mixed-port / port / socks-port；`listen: 0.0.0.0` 明文代理安全警告）。
[^c3-3]: S3：mihomo 官方文档 proxy-providers（type / url / path / interval / health-check；SAFE_PATHS；filter / exclude-filter / exclude-type）。

[^c4-1]: [libcurl-env — 环境变量代理](https://everything.curl.dev/usingcurl/proxies)（S8）
[^c4-2]: [apt-transport-http(1) — apt 手动页](https://manpages.debian.org/stable/apt/apt-transport-http.1.en.html)（S10）
[^c4-3]: [git-config — http.proxy](https://git-scm.com/docs/git-config)（S9）

[^c5-1]: Docker Docs — Configure the Docker daemon to use a proxy. <https://docs.docker.com/engine/daemon/proxy/>
[^c5-2]: Docker Docs — Configure proxy using the CLI. <https://docs.docker.com/engine/cli/proxy/>
[^c5-3]: Docker Forums 社区讨论：容器内访问宿主机代理需用 docker0 网关 / host-gateway（结合既有笔记交叉验证）。
[^c5-4]: 既有笔记 [[docker进行代理]] — 宿主机已有 Clash 时，容器 HTTP_PROXY 要用宿主机 IP 而非 127.0.0.1。
