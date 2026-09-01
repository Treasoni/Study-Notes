---
title: "第 2 章：安装 mihomo 内核"
tags:
  - ubuntu
  - linux
  - 代理
  - 翻墙
  - docker
  - mihomo
created: 2026-08-29
updated: 2026-08-29
status: 已完成
source_project: ubuntu-server-proxy-docker
---

> [[01_总览与方案选型|← 上一章]] · [[README|🏠 首页]] · [[03_配置config.yaml|下一章 →]]

# 第 2 章：安装 mihomo 内核

> [!note] 本章目标
> 把 mihomo 内核二进制装到 `/usr/local/bin/`，再用 systemd 把它守护起来，实现开机自启、崩溃自动重启，最后验证服务存活。订阅节点与完整 `config.yaml` 留到下一章，本章先放一个最小占位配置让它能跑起来。

> 章节产物：`/usr/local/bin/mihomo` + `/etc/mihomo/config.yaml`（占位）+ `/etc/systemd/system/mihomo.service`

## 2.1 按架构下载二进制

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

## 2.2 解压、改名、放入 /usr/local/bin/

```bash
gzip -d "mihomo-linux-${ARCH}-${VERSION}.gz"          # 解出同名二进制
mv "mihomo-linux-${ARCH}-${VERSION}" mihomo          # 改成统一的名字
sudo mv mihomo /usr/local/bin/                        # 放进 PATH 搜索目录
sudo chmod +x /usr/local/bin/mihomo                   # 加执行权限
mihomo -v                                             # 验证版本，能打印就说明装好了
```

> [!note] 为什么放 `/usr/local/bin/`
> 它默认在 `PATH` 里，systemd 的 `ExecStart` 和命令行直接敲 `mihomo` 都能找到，不用写绝对路径（systemd 里我们仍写绝对路径更稳妥）。改名 `mihomo` 只是统一命名，不强制。

## 2.3 创建配置目录 /etc/mihomo/（最小占位）

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

## 2.4 用 systemd 守护 mihomo

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

## 2.5 查看运行日志

```bash
journalctl -u mihomo -ocat -e    # 只看最近几行，-ocat 去掉多余前缀
journalctl -u mihomo -f          # 实时滚动跟踪
```

日志里出现 `Start initial provider` 或 `RESTful API listening` 之类即说明内核正常启动；有报错就按日志排查（最常见是 `config.yaml` 语法问题或端口被占）。

## 2.6 自检：服务是否存活

```bash
curl -I https://www.gstatic.com/generate_204
```

预期返回 `HTTP/2 200`。这一步能打通，说明 mihomo 的入站端口在监听、且链路能出网。

> [!warning] 如果暂时不是 200，别慌
> `gstatic.com` 是 Google 的连通性检测端点。占位配置下还没有订阅节点，**真正拿到 200 需要下一章把节点订阅写进 config.yaml**。本章的即时验收标准是：`systemctl status mihomo` 显示 `active (running)`，`journalctl` 无致命错误，`curl -I http://127.0.0.1:7890` 能建立 TCP 连接即可。

## 本章小结

- 先用 `uname -m` 确定架构（amd64 / arm64），再下载对应 `.gz` 包；下载源被墙可用镜像或本地上传。
- 解压、改名、放进 `/usr/local/bin/`、加执行权限，`mihomo -v` 验证。
- 建 `/etc/mihomo/` 目录并放一份最小占位 config.yaml，声明 `mixed-port: 7890`。
- systemd unit 让 mihomo 开机自启、崩溃自愈，并通过 `LimitNOFILE`、Capabilities 做资源与权限准备。
- 用 `systemctl status` 和 `journalctl` 验收服务存活；`generate_204` 的 200 需要等节点就绪。

下一章会往 `/etc/mihomo/config.yaml` 里写进订阅节点、节点分组和规则，让这台刚"醒来"的内核真正具备分流出网的能力。

## 脚注

[^c2-s1]: mihomo 官方 GitHub Releases（内核二进制下载）— https://github.com/MetaCubeX/mihomo/releases
[^c2-s5]: mihomo 官方文档·systemd 服务示例 — https://wiki.metacubex.one/start/

> [[01_总览与方案选型|← 上一章]] · [[README|🏠 首页]] · [[03_配置config.yaml|下一章 →]]
