---
title: "飞书接入（上）：建应用与 WebSocket 长连接"
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - 飞书
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
---

> [[04-企业微信AI Bot与回调|⬅ 上一章]] · [[README|📖 返回目录]] · [[06-飞书事件订阅与消息收发|下一章 ➡]]

# 飞书接入（上）：建应用与 WebSocket 长连接

上一章接入企业微信，这一章轮到飞书（海外版 Lark）。飞书默认走 **WebSocket 长连接**，免公网 URL、免内网穿透。本章建出飞书应用、定下连接模式；事件与消息收发留到第 6 章。

## 5.1 两种建应用路线

飞书收发消息的前提是先有一个**应用**（App），Hermes 给两条路。

**路线 A：`hermes gateway setup` 扫码自动建**。跑向导选飞书选项，手机扫码确认，工具自动建好应用并写入 `~/.hermes/.env`。选项号以菜单实际为准（社区数字可能漂移）。

**路线 B：手动 open.feishu.cn 建**。创建企业自建应用 → 取 App ID（`cli_xxx`）/ App Secret → 开「机器人」能力（不开收不了消息）→ 配权限/事件（第 6 章）→ 发布。个人即时生效；**企业租户需管理员审批**。

> [!tip] 大白话：建应用 = 给机器人办门禁卡
> 把建应用想成给机器人办一张进飞书大楼（开放平台）的门禁卡：App ID 是**工号**（公开），App Secret 是**门禁密码**（保密）。

> [!warning] 企业审批是第一个卡点
> 企业租户发布应用常需管理员审批，卡住则后面全白搭。可先开发者模式验证，或提前让管理员放行。

## 5.2 连接模式：WebSocket 默认，Webhook 可选

官方给两种连接模式（[F1 §Step2]）。

**WebSocket（默认且推荐）**：出站连飞书开放平台；免公网 URL / 反代 / 穿透；SDK（`lark-oapi`）自动心跳重连；依赖 `websockets` 包。

> [!tip] 大白话：WebSocket 是自己上门取件
> WebSocket 像定时去快递驿站取件，飞书一来消息就顺常开的线递来，不用告诉飞书你家住址（不需公网 URL）；Webhook 是快递送货上门，必须给可访问的收货地址。没公网 IP 就选 WebSocket。

**Webhook（可选）**：`aiohttp` 起本地 HTTP 服务，端点默认 `/feishu/webhook`，`FEISHU_WEBHOOK_HOST` 默认 `127.0.0.1`、PORT 默认 `8765`、PATH 可改；限流 **120 req/60s**（[F1]）。

> [!warning] `127.0.0.1` 不代表飞书能回调进来
> `127.0.0.1` 只有宿主机本机能访问。让公网飞书回调进来，要改绑定地址 + 公网 IP/反代 + 放行防火墙，等于暴露无认证 HTTP 服务。能用 WebSocket 就别开 Webhook。

## 5.3 产物 G：`~/.hermes/.env` 飞书配置

凭证最终都写进 `~/.hermes/.env`，先看完整文件再拆。

```bash
# ~/.hermes/.env
# ===== 飞书 / Feishu 接入 =====

# 必填：应用凭证（open.feishu.cn 创建应用后获取）
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=your_app_secret_here

# 可选：连接模式（默认 websocket，本册推荐）
CONNECTION_MODE=websocket

# 可选：选择域。国内版默认 feishu.cn，海外 Lark 才改 larksuite.com
# FEISHU_DOMAIN=feishu.cn

# 可选：消息接收范围与群聊策略（第 6 章展开）
# ALLOWED_USERS=ou_xxxxxxxx,ou_yyyyyyyy
# HOME_CHANNEL=oc_xxxxxxxxxxxxxxxx
# GROUP_POLICY=disabled
# REQUIRE_MENTION=true

# ===== 仅 Webhook 模式需要（默认不启用）=====
# FEISHU_WEBHOOK_HOST=127.0.0.1
# FEISHU_WEBHOOK_PORT=8765
# FEISHU_WEBHOOK_PATH=/feishu/webhook
```

**拆讲**：

- `FEISHU_APP_ID`：`cli_` 开头工号，公开。
- `FEISHU_APP_SECRET`：门禁密码，**必须保密**——明文落数据卷，泄露=可冒充你的机器人收发消息。
- `CONNECTION_MODE`：`websocket`（默认、推荐）或 `webhook`。
- `FEISHU_DOMAIN`：国内默认 `feishu.cn`；海外 Lark 租户才指到 `larksuite.com`。
- `ALLOWED_USERS` / `HOME_CHANNEL` / `GROUP_POLICY` / `REQUIRE_MENTION`：群聊与接收策略，先落位，第 6 章展开。
- `FEISHU_WEBHOOK_*`：仅 `webhook` 模式有意义，默认注释。

> [!tip] 大白话：App Secret 是保险箱钥匙
> App ID 是保险箱编号谁都能看，App Secret 是开箱钥匙。钥匙随手放桌上（明文 `.env`、贴聊天记录、提交 Git），等于请人随便搬。第 10 章收口。

**常见坑**：key 拼错下划线会被**静默忽略**（表现是「没反应」而非报错）；`.env` 启动时读取、不热加载，改完记得重启 gateway。

## 5.4 依赖检查

飞书是官方 bundled plugin（`plugins/platforms/feishu/`，[F2]），依赖三个包（[F1 §Troubleshooting]）：

| 包 | 作用 | 缺失后果 |
|------|------|----------|
| `lark-oapi` | 飞书 SDK，建连与 API 调用 | 插件无法加载，平台不可用 |
| `websockets` | WebSocket 传输 | websocket 模式报缺依赖 / 连不上 |
| `aiohttp` | Webhook HTTP 服务 | webhook 模式服务起不来 |

> [!tip] 大白话：缺依赖 = 机器人缺零件
> lark-oapi 是大脑接口，websockets 是对讲天线，aiohttp 是快递柜。官方镜像通常已装齐，只有源码 / 精简镜像才要自查。

```bash
# 容器内自查（镜像无独立 hermes 可执行文件，用 python 直接 import）
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent \
  python -c "import lark_oapi, websockets, aiohttp; print('ok')"
```

输出 `ok` 即齐全；报 `ModuleNotFoundError` 则缺哪个补哪个。

## 5.5 勘误：官方文档没有「WebSocket 仅限企业自建应用」

社区流传「飞书 WebSocket 仅限企业自建应用」。对照官方文档 [F1 §Step2]，**没有这个表述**——普通自建应用即可用 WebSocket，无需企业版、无需特殊资格。后文不再复述。

## 本章小结

- **两条路线**：`gateway setup` 扫码自动建（最快，选项号以菜单为准）；手动 open.feishu.cn（可控，企业需审批）。
- **WebSocket 默认且推荐**：出站、免公网、SDK 管心跳重连，只需 `websockets` 包。
- **Webhook 可选**：`aiohttp` 起 `/feishu/webhook`，默认 `127.0.0.1:8765`，限流 120 req/60s。
- **`.env` 必填二键**：`FEISHU_APP_ID` + `FEISHU_APP_SECRET`；可选键第 6 章展开。
- **勘误**：官方文档没有「WebSocket 仅限企业自建应用」的表述。

下一章进入飞书下半场：事件订阅、权限 scope 与消息收发，把应用变成能收能发的机器人。

> [[04-企业微信AI Bot与回调|⬅ 上一章]] · [[README|📖 返回目录]] · [[06-飞书事件订阅与消息收发|下一章 ➡]]
