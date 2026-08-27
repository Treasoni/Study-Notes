# 第二章 Docker Compose 部署 Tailscale 容器

> 对应路由注入四条件的**第一环——通告**。给「推荐版」与「最小权限版」两套 Compose，并拆解关键环境变量。Docker/Compose 基础可对照 [[内网穿透/Tailscale使用教程.md]]。

## 2.1 fnOS 界面入口

fnOS 桌面打开 **Docker → Compose → 新建项目**，粘贴 YAML，填项目名（如 `tailscale-subnet-router`）并部署。

> [!warning] 界面路径以实机为准
> 社区帖路径（来源 S2, S3）可能随 fnOS 版本微调（待实机确认）。核心逻辑不变：新建 Compose 项目 → 粘贴 YAML → 部署。

## 2.2 推荐版 Compose（privileged，省心）

```yaml
# docker-compose.yml（推荐版）
services:
  tailscale:
    image: tailscale/tailscale:stable   # 固定 stable 标签
    container_name: tailscale-subnet-router
    hostname: fnos-subnet-router
    network_mode: host                    # 关键：直接用宿主机网络栈
    privileged: true                      # 省心：完整设备访问权限
    cap_add:
      - NET_ADMIN                         # 建 tun、改路由所需（privileged 下为双保险）
    volumes:
      - /var/lib/tailscale:/var/lib/tailscale   # 状态持久化
      - /dev/net/tun:/dev/net/tun               # 挂载 TUN 设备
    environment:
      - TS_AUTHKEY=tskey-auth-xxxxxxxx      # 生成时必须勾选 Reusable
      - TS_STATE_DIR=/var/lib/tailscale     # 状态目录
      - TS_ROUTES=192.168.1.0/24            # 内网网段，无末尾逗号
      - TS_HOSTNAME=fnos-subnet-router      # 后台显示名，可自定
    restart: unless-stopped                 # 开机自启 + 异常自动拉起
```

> [!note] 为什么用 host 网络
> Docker 对 host 网络不额外创建 iptables 规则（来源 S8），且 tailscaled 需在宿主机网络命名空间建 `tailscale0`、改路由。这是社区共识基线（来源 S2, S3, S0）。

## 2.3 最小权限版 Compose（无 privileged）

社区验证可用的更克制变体（来源 S3）：

```yaml
# docker-compose.yml（最小权限版）
services:
  tailscale:
    image: tailscale/tailscale            # 无 tag：跟随最新
    container_name: tailscale-subnet-router
    hostname: fnos-subnet-router
    network_mode: host
    cap_add:
      - NET_ADMIN                         # 建 tun、改路由、iptables
      - NET_RAW                           # 原始 socket，部分场景建 tun 需要
    volumes:
      - tailscale-state:/var/lib/tailscale
      - /dev/net/tun:/dev/net/tun
    environment:
      - TS_AUTHKEY=tskey-auth-xxxxxxxx
      - TS_STATE_DIR=/var/lib/tailscale
      - TS_ROUTES=192.168.1.0/24
      - TS_HOSTNAME=fnos-subnet-router
    restart: unless-stopped

volumes:
  tailscale-state:                        # 命名卷，路径交给 Docker 管理
```

> [!tip] 两版怎么选
> 像"全套装修"vs"简装"：`privileged` 省心，适合直接照做；最小权限版更安全但排查面更大。**推荐先跑推荐版，再考虑收敛权限**（来源 S2, S3）。

## 2.4 关键环境变量

- **`TS_AUTHKEY`**：Admin Console → Settings → Keys 生成时**必须勾选 Reusable**；否则 single-use 密钥在容器重启后无法再认证 → 反复闪退（来源 S0, S2 回帖）。
- **`TS_STATE_DIR`**：tailscaled 状态目录，配合卷持久化；否则每次重建都重新认证、换 IP。
- **`TS_ROUTES`**：要通告的内网网段，**必须是合法 CIDR**。
- **`TS_HOSTNAME`**：后台显示名，可自定（社区用 fnos，用户草稿用 fons-subnet-router，来源 S2, S0）。

> [!tip] 大白话
> `TS_AUTHKEY` 是**临时工牌**：reusable 长期可进出，single-use 刷一次作废。工牌用完没人补发，门卫不让你进门——容器就闪退了。

> [!warning] TS_ROUTES 最容易踩的坑
> 必须是 **IP/CIDR**。填布尔值 `true`、或末尾多逗号（`192.168.1.0/24,`），都会触发 `netip.ParsePrefix` 解析失败，报错如 `netip.ParsePrefix(""): no '/'`（来源 S12, S0）。**合法示例：`TS_ROUTES=192.168.1.0/24`，无空格、无尾逗号。**

## 2.5 部署侧 TUN busy 预防

宿主若已装 Tailscale（或残留 tailscaled、冗余容器），会占用 `/dev/net/tun`，容器建 `tailscale0` 报 **TUN device busy**（来源 S0）。部署前先查：

```bash
lsof /dev/net/tun      # 看谁占用 tun
pgrep -a tailscaled    # 查宿主机是否已有 tailscaled
```

## 2.6 其他注意点

- **`version` 字段**：老教程的 `version: '3'` 只是过时警告，建议删掉（来源 S3 回帖）。
- **容器重启会换 Tailscale IP**（来源 S3 回帖）：对子网路由器影响不大——客户端走子网路由而非容器 IP；如需长期稳定可禁用该设备 key expiry。

## 本章小结

- 部署入口：fnOS Docker → Compose → 新建项目（来源 S2, S3；界面细节待实机确认）。
- 基线：host 网络 + `/dev/net/tun` + `TS_STATE_DIR` + `TS_ROUTES` + `restart: unless-stopped`（来源 S2, S3, S0）。
- 两变体：推荐版 `privileged`；最小权限版 `NET_ADMIN + NET_RAW`（来源 S2, S3）。
- `TS_AUTHKEY` 必须 reusable；`TS_ROUTES` 必须合法 CIDR、无尾逗号（来源 S0, S2, S12）。
- 部署前 `lsof /dev/net/tun` 排查占用（来源 S0）。

容器起来了、通告发了，但包还出不去——内核默认不允许转发。下一章开转发开关。

**参考来源**：S0 用户草稿 · S2 飞牛论坛 tid=13887 · S3 飞牛论坛 tid=28001 · S8 Docker 数据包过滤与防火墙 · S12 tailscale Issue #9605。
