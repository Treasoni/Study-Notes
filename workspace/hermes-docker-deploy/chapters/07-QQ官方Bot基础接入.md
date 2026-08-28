---
title: "QQ 接入（上）：官方 QQ Bot 基础接入"
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - QQ
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
---

> [[06-飞书事件订阅与消息收发|⬅ 上一章]] · [[README|📖 返回目录]] · [[08-QQ进阶配置与NapCat替代|下一章 ➡]]

# QQ 接入（上）：官方 QQ Bot 基础接入

## 7.1 背景：QQ「原生接入」合入官方

前几章我们分别接入了企业微信（04）和飞书（05/06）。这一章轮到 QQ——但它和前面几位走的路完全不一样。2026 年 4 月，腾讯 QQ 的「原生接入」落地，QQ Bot 插件正式合入 Hermes 官方（[Q2](https://www.ithome.com/0/939/789.htm)），这意味着三件事：

- QQ 是国内三个平台里**唯一走「官方机器人」路线**的：你在 q.qq.com 建一个官方 QQ 机器人，Hermes 直接以机器人身份收发消息。
- **不需要任何第三方桥接**：既不用像微信那样扫 iLink、也不用像企微那样配回调，更不用后来那套 NapCat 非官方方案。
- 代价是它带一套其他平台没有的**「沙箱 → 发布」审核流程**，这就是本章后半段的主角。

> [!tip] 大白话
> 把 QQ 官方接入想成「商场给 Hermes 发了一张员工卡」。你（Hermes）直接走商场正门、亮卡进场，不需要从小巷后门绕（第三方桥 / 非官方协议）。所以它最稳、最正规；但商场要审核你的身份（机器人要过审），而且不允许你替普通顾客随便逛街（不能操作普通个人 QQ 号）。

## 7.2 架构：QQ Bot API v2（WS 收 + REST 发）

官方适配器基于 **QQ Bot API v2**（[Q1 §Overview](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot)），收发两个方向各用一种方式：

- **收（WebSocket）**：Hermes 与 QQ 服务器保持一条 WebSocket 长连接，QQ 有新消息就主动推过来。这是**出站连接**，和飞书的 WebSocket 模式一样，**不需要公网 URL**。
- **发（REST）**：回复消息时走 HTTP REST 接口主动调用 QQ 接口。

适配器覆盖三种场景：

| 场景 | 触发方式 | 说明 |
|------|----------|------|
| 私聊 C2C | 用户直接私聊机器人 | 最稳定，类似飞书单聊 |
| 群 @ | 群里 **@ 机器人** 才触发 | 不 @ 不理会，需 7.3 的群消息 intent |
| 频道 | 腾讯频道内消息 | 需频道消息 intent |

> [!tip] 大白话
> WebSocket 收消息 = 你在门口挂了个门铃，QQ 有消息就按铃喊你；REST 发消息 = 你要回话时主动把信寄出去。一个方向是「QQ 找上门」，另一个是「你找 QQ」，两者配合才构成完整的「来去」。

## 7.3 前置：q.qq.com 建机器人，就三件事

这一步全部在 q.qq.com（QQ 开放平台）浏览器操作，**不碰 Docker**（Q1 §Prerequisites）。

**第 1 步：注册机器人，拿凭证。** 登录 q.qq.com → 创建机器人应用 → 在「开发设置」里找到 `AppID` 和 `AppSecret`。AppID 对应后面的 `QQ_APP_ID`，AppSecret 对应 `QQ_CLIENT_SECRET`。

> [!warning]
> AppSecret 等价于机器人的「身份证 + 钥匙」，和企微 `WECOM_SECRET` 一个级别：**泄露 = 任何人都能冒充你的 bot 收发消息**。不要把它写进任何会提交 git 的文件，后面第十章的安全基线还会重点讲。

**第 2 步：启用 intents（事件订阅）。** 在「开发设置 → 事件订阅」里勾选需要的消息类型，逐项核对：

- [ ] 单聊消息（C2C）—— 私聊场景
- [ ] 群消息 @ 机器人 —— 群聊场景，仅 @ 时触发
- [ ] 频道消息 —— 频道场景

（控制台里事件名的具体措辞以 q.qq.com 为准，核心就是这三类；漏勾哪一类，那一类消息就永远收不到。）

> [!tip] 大白话
> intents 就是「订阅清单」。你告诉 QQ：「我只订阅这三类消息，其他别来烦我」。清单没勾全，那一类消息就永远进不来——不是 Hermes 坏了，是 QQ 压根不给你推。

**第 3 步：加沙箱成员 → 测通 → 提交发布。** 新机器人默认只在沙箱环境收消息，测通后要在开放平台提交发布，审核通过才对真实用户生效。具体流程见 7.5。

## 7.4 产物 I：`~/.hermes/.env` QQ 配置

在第一章 setup 生成的 `~/.hermes/.env` 末尾追加下面这一段 QQ 配置段。先看**完整文件**：

```env
# ~/.hermes/.env —— QQ Bot 配置段（追加在 setup 生成的 .env 末尾）

# === QQ 必填：机器人凭证 ===
QQ_APP_ID=1023456789                 # q.qq.com 的 AppID
QQ_CLIENT_SECRET=1a2b3c4d5e...       # q.qq.com 的 AppSecret

# === QQ 可选：白名单 ===
QQ_ALLOWED_USERS=10001,10002         # 允许 C2C 私聊的 QQ 号，逗号分隔
GROUP_ALLOWED_USERS=987654321        # 允许群 @ 的群号（格式以官方文档为准）

# === QQ 可选：沙箱入口（正式发布后注释掉这一行）===
# QQ_PORTAL_HOST=sandbox.q.qq.com
```

**逐段拆讲：**

- `QQ_APP_ID` / `QQ_CLIENT_SECRET`（必填）：就是 7.3 拿到的两个凭证，一个 id、一个密钥，缺一不可。Hermes 靠它们在 QQ 侧完成身份认证与鉴权。
- `QQ_ALLOWED_USERS`（可选）：C2C 私聊白名单，逗号分隔的 QQ 号列表。不填则按平台的默认私聊策略（与第八章 `dm_policy` 联动）。
- `GROUP_ALLOWED_USERS`（可选）：允许在群里 @ 机器人的群白名单。**格式以官方文档为准**，示例仅供占位——实际接入时建议先只放自己的测试群。
- `QQ_PORTAL_HOST`（可选）：QQ 接入入口 host。**默认走生产环境；设为 `sandbox.q.qq.com` 则切到沙箱环境**（7.5 详述）。还在测沙箱就保留这一行，发布后务必注释掉。

> [!warning] 常见坑
> - 改 `.env` 后必须**重启 gateway 容器**才生效（`docker compose restart hermes`），不是热加载。
> - 值不要带多余空格：`QQ_APP_ID= 1023456789` 会被当成带前导空格的值，认证直接失败。
> - 只填 `QQ_APP_ID` 忘填 `QQ_CLIENT_SECRET`，Hermes 会因凭证不完整而启动即断开。

## 7.5 沙箱测试与发布：`QQ_PORTAL_HOST=sandbox.q.qq.com`

QQ 官方机器人的「测试 → 上线」是其他平台都没有的硬性流程（Q1 §Advanced）：

**沙箱阶段**
1. 在 q.qq.com 后台把你的 QQ 号添加为「沙箱测试成员」。
2. 在 `~/.hermes/.env` 里设 `QQ_PORTAL_HOST=sandbox.q.qq.com`（即 7.4 完整文件里注释掉的那一行）。
3. 重启 gateway，让 Hermes 以沙箱模式连上 QQ。
4. 在沙盒测试频道里给机器人发消息。**沙箱模式下只收沙盒测试频道内的消息**，生产环境的真实用户消息一律收不到。

**发布阶段**
1. 沙箱测通后，去 q.qq.com 提交发布，等审核通过。
2. 通过后，把 `.env` 里 `QQ_PORTAL_HOST=sandbox.q.qq.com` 这一行**注释或删除**，恢复生产入口。
3. 重启 gateway，对真实用户生效。

> [!warning]
> 「沙箱收非沙箱流量」是 QQ 接入最常见的误判：沙箱模式一直测不出真实用户消息，**不是 Hermes 坏了，是你还停在沙箱里**；反过来，发布后忘删沙箱 host 行，真实用户的消息同样进不来。改 `QQ_PORTAL_HOST` 后记住重启容器。

## 7.6 能力边界

- ✅ 能做到：官方机器人身份收发 C2C 私聊、群 @、频道消息；免公网；过审后服务真实用户。
- ❌ 做不到：登录 / 操作普通个人 QQ 号（那是非官方 NapCat 的路线，见下一章）；在群里自由发言（必须被 @）；绕过开放平台审核直接对真实用户生效。

## 本章小结

- QQ 是三个国内平台里唯一走「官方机器人 + 沙箱 → 发布」路线的：Hermes 以 QQ Bot 身份收发，免第三方桥。
- 架构一句话：**WebSocket 收 + REST 发**，覆盖 C2C 私聊、群 @、频道三场景，免公网 URL。
- 前置三件事：q.qq.com 拿 `AppID` / `AppSecret` → 勾全 intents → 沙箱测通后发布。
- `.env` 必填 `QQ_APP_ID` / `QQ_CLIENT_SECRET`，可选 `QQ_ALLOWED_USERS` / `GROUP_ALLOWED_USERS` / `QQ_PORTAL_HOST`。
- 沙箱与生产靠 `QQ_PORTAL_HOST` 切换，发布后务必删掉沙箱行并重启容器。

下一章进入 QQ 接入（下）：`config.yaml` 的 `platforms.qqbot.extra` 进阶配置、语音双阶段转写，以及那几条著名的 WS 断连坑（4009 会话超时 / aiohttp 静默断连），最后对比非官方 NapCat 路线的取舍。
