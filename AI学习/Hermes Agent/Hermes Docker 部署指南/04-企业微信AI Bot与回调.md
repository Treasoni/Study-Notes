---
title: 企业微信接入：AI Bot 与自建应用回调
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - 企业微信
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
---

> [[03-微信个人号iLink接入|⬅ 上一章]] · [[README|📖 返回目录]] · [[05-飞书建应用与WebSocket|下一章 ➡]]

# 企业微信接入：AI Bot 与自建应用回调

上一章接入的是个人微信，适合个人使用；而企业办公场景通常要求「消息在企业微信里跑」。本章回答的问题很直接：**Hermes 接入企业微信有哪两条路，我该选哪条，配置怎么写，有什么限制和坑？** 掌握这些，你就能把同一个 Hermes 从个人号无缝延伸到企业工作台。

## 4.1 两种模式：AI Bot WebSocket vs 自建应用回调

企业微信接入有两条官方路线，核心差别在**连接方向**和**是否要公网**。[^c4-W3]

| 维度 | AI Bot（WebSocket） | 自建应用回调（Webhook） |
|------|---------------------|--------------------------|
| 连接方向 | Hermes **出站**主动连 `wss://openws.work.weixin.qq.com` | 企业微信**入站** POST 事件到你的 URL |
| 是否需要公网 URL | **否**，免公网 | **是**，需要公网可达的 HTTP 端点 |
| 实时性 | 实时双向 + **流式**输出 | 实时事件回调，无流式推送 |
| 连接维护 | SDK 自动心跳 / 自动重连 | 依赖你的服务稳定暴露在公网 |
| 适用场景 | 个人 / 小团队快速跑通、无公网环境 | 已有公网基础设施、需要自定义回调处理 |
| 上手复杂度 | 低 | 中（要域名、校验 token、回调路由） |

> [!tip] 大白话
> 把两种模式想成**取信 vs 送信上门**：AI Bot WebSocket 是 Hermes 每天自己跑到企业微信的邮局门口取信、送信（出站连接），你不需要把自家门牌号告诉别人；自建应用回调则是企业微信当快递员，把消息**送到你的公网地址**——可快递的前提是你得有公开门牌号（公网 URL）。所以前者免公网，后者必须先解决公网暴露。

**推荐结论**：绝大多数 Docker 部署选 **AI Bot WebSocket**——和上一章微信 iLink 一样免公网，还多了流式回复与自动重连，少操一份公网反代的心。本章也以这条路线为主线。

## 4.2 gateway setup 入口

在容器里跑交互式向导选择企业微信：

```bash
# 用一次性容器挂同一数据卷跑 CLI（原因见 4.5）
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent gateway setup
```

社区实操记录里，企业微信两个模式对应的菜单选项号是：**企微 AI Bot ≈ 12**、**企微回调 ≈ 13**。[^c4-W4]

> [!warning]
> 选项号是社区记录，官方文档没有给数字，不同版本很可能漂移。**以你 setup 菜单里显示的实际文字为准**，别死记「12 / 13」这两个数字。

## 4.3 产物 F：`~/.hermes/.env` 企微配置

向导跑完会在 `~/.hermes/.env` 里写入企微配置段。完整文件先睹为快：

```bash
# ~/.hermes/.env  企业微信配置段（首次 setup 后生成，可手工修改）

# 必填：AI Bot 的唯一标识（企微管理后台创建 AI Bot 后获取，通常 ww_ 开头）
WECOM_BOT_ID=ww_your_bot_id_here

# 必填：与 Bot ID 配套的密钥，用于签名与身份校验
WECOM_SECRET=your_wecom_bot_secret_here

# 若走「自建应用回调」模式：还需在企微后台配置回调 URL / Token / EncodingAESKey，
# 并把公网地址指向 Hermes 的收件端点；具体环境变量名以官方文档为准
```

逐段拆讲：

- **`WECOM_BOT_ID`**：这是企业微信里那个 AI Bot 的身份证号。去 `work.weixin.qq.com` 管理后台创建一个 AI Bot，后台会给你一串以 `ww_` 开头的 ID，填到这里。
- **`WECOM_SECRET`**：与 Bot ID 配对的密钥，作用是「证明你就是这个 Bot」。它不参与业务逻辑，只负责身份，所以它也是本章 4.6 的安全焦点。
- **回调模式**：如果你确实选了自建应用回调，改动不在 `.env` 单方面，而是**两边都要配**——企微后台要填你的回调 URL、Token 和 EncodingAESKey，Hermes 侧要有公网收件端点。这部分具体变量名官方文档并未在正文完整罗列，动手前建议以官方文档为准核对一遍。[^c4-W3]

> [!tip] 大白话
> 把 `WECOM_BOT_ID` 想成**工牌上的姓名**，`WECOM_SECRET` 想成**门禁卡**。企业微信看到「姓名 + 门禁卡」才能确认「哦，是 Hermes 本尊」，才肯把消息交给它。门禁卡这一节先记着，4.6 再讲它丢了会怎样。

## 4.4 出站限制与能力边界

接入之前，先给期望「设个上限」。企业微信对 AI Bot 出站消息有明确的体积限制：[^c4-W3]

| 消息类型 | 出站上限 |
|----------|----------|
| text 文本 | 4k |
| img 图片 | 10MB |
| doc 文档 | 20MB |
| voice 语音 | 2MB |
| **任意消息** | **20MB 硬顶** |

> [!tip] 大白话
> 把出站限制想成**快递公司的包裹规格**：文字是信封（4k），图片是中小纸箱（10MB），文档是大纸箱（20MB），语音是特小信封（2MB）。但不管哪种，都逃不过总闸门 20MB——这是所有包裹的**硬顶**。想给同事甩一个 300MB 的安装包？先压缩再说。

能力边界明确如下：

- **做得到**：文本对话、图片 / 文档 / 语音的收发，流式回复，实时双向。
- **做不到 / 需注意**：超出 20MB 的单条内容发不出去；语音只有 2MB 额度，长录音要裁剪；交互卡片、按钮这类富媒体不是 AI Bot 的强项，需要富交互建议对比后续飞书、QQ 章节的能力再选平台。

## 4.5 Docker 场景排错

企微接入里两个高频 Docker 坑，都来自「把容器当普通进程用」：[^c4-W4]

**坑一：`docker exec` 找不到二进制。** 想在容器里补跑 `gateway setup` 或看日志，直接执行

```bash
docker exec -it hermes hermes gateway setup   # ❌ 报 command not found
```

会失败，因为官方镜像**没有把 `hermes` 作为独立可执行文件装进 PATH**。正确姿势是用一次性容器挂同一数据卷来跑 CLI：

```bash
docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent gateway setup   # ✅
```

**坑二：前台跑 gateway，断线即停。** 用不带 `-d` 的 `docker run` 前台运行 gateway，一旦你的终端断开或网络抖动，进程收到 SIGHUP 就退出，Bot 随之掉线。**必须用 Compose 以 detached 方式常驻**：

```bash
docker compose up -d hermes   # ✅ 守护进程方式常驻
```

> [!warning]
> 企微排错时最典型的两连击：用 `docker exec` 想改配置 → 报 `command not found`；用前台 `docker run` 跑 gateway → 一断终端 Bot 就没了。记住口诀：**CLI 用 `docker run -it --rm -v 同卷`，常驻用 `compose up -d`。** 改完 `.env` 后记得 `docker compose restart hermes` 让配置生效。[^c4-D1]

## 4.6 安全提示：密钥即身份

`WECOM_SECRET` 不是普通配置项，它是 Bot 的**门禁卡**。只要它泄露，任何人都可以冒充你的 Bot 收发消息——企业微信只认「ID + Secret」，不认别的。[^c4-W3]

- 它明文落在 `~/.hermes/.env`，意味着**数据卷本身就是泄露面**：谁拿到你的 `~/.hermes` 备份或容器卷，谁就拿到 Bot 的钥匙。[^c4-W4]
- 不要把 `~/.hermes` 同步到云盘、提交进 Git 或发给同事。
- 定期轮换：在企微后台重置 Secret 后，同步更新 `.env` 并 `docker compose restart hermes`。
- 尽量让容器以非 root 降权运行（UID 10000），避免数据卷权限过宽。密钥与公网暴露的完整基线，第 10 章专门展开。

> [!warning]
> 一句话记住本章的安全底线：**`WECOM_SECRET` = 门禁卡，数据卷 = 挂卡包的地方。** 卡包（`~/.hermes`）千万别随手扔（云盘 / Git / 共享盘）。

## 本章小结

- 企业微信两条路线：AI Bot WebSocket **免公网 + 实时双向 + 流式 + 自动重连**；自建应用回调需公网 URL，适合已有公网基础设施的场景。[^c4-W3]
- gateway setup 菜单里企微 AI Bot≈12、企微回调≈13（社区记录，**以菜单实际为准**）。[^c4-W4]
- `.env` 必填 `WECOM_BOT_ID` + `WECOM_SECRET`，走回调模式还要在企微后台配回调 URL / Token / EncodingAESKey。[^c4-W3]
- 出站限制：text 4k / img 10MB / doc 20MB / voice 2MB，**20MB 硬顶**。[^c4-W3]
- Docker 排错口诀：CLI 用 `docker run -it --rm -v 同卷`，常驻用 `compose up -d`，别用 `docker exec` 找不存在的二进制、别前台跑 gateway。[^c4-W4]
- `WECOM_SECRET` 泄露 = 可冒充 Bot；密钥明文落数据卷，卷即泄露面。

下一章我们接入飞书（上）：飞书建应用的两条路线和 WebSocket 长连接。你会看到，飞书的玩法和企业微信很像——同样是「免公网 WebSocket 优先」，但建应用与权限配置的细节完全是另一套体系。

---

[^c4-W3]: 企业微信（WeCom）官方文档：https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom
[^c4-W4]: CSDN 实操记录《Hermes 微信 / 企业微信 Gateway + Docker Compose》：https://blog.csdn.net/WeLoveCn/article/details/161239172
[^c4-D1]: Hermes Docker 官方文档：https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker
