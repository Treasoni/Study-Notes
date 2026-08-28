---
title: 微信个人号接入：iLink 扫码直连
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - 微信
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
---

> [[02-Gateway常驻与Compose编排|⬅ 上一章]] · [[README|📖 返回目录]] · [[04-企业微信AI Bot与回调|下一章 ➡]]

# 微信个人号接入：iLink 扫码直连

> 本章解决一个问题：**怎么用 Hermes gateway 扫码接入微信个人号，让 AI 在微信私聊里收发消息？**
> 读完你会知道：这是 iLink Bot API 而不是 wechaty 桥；扫码流程的产物是什么；`~/.hermes/.env` 要配哪两个必填键；为什么它免公网；以及最关键的——**微信这条线能做什么、不能做什么**。

## 3.1 先定性：iLink Bot API，不是 wechaty，也不是"挂机自动化"

很多教程一提"微信接 AI"就想到 wechaty。但 Hermes 官方走的是**原生 iLink Bot API**（`ilinkai.weixin.qq.com`），微信适配器在 2026-04 的 PR #7166 合并进主仓库，明确走 iLink 而非 wechaty 桥（W2）。这不是实现细节之争，而是**身份与边界的差别**：

- **wechaty 式个人号自动化**：登录你本人的微信号模拟真人收发，高风险、易风控。
- **iLink Bot API**：扫码后拿到的是 **iLink bot 身份**，是微信生态里的机器人账号，不是把你日常微信号变成自动化工具。官方以此保证合规与稳定（W1）。

[!tip] 大白话
> 把 wechaty 想成"拿你手机号替你做客服"，把 iLink 想成"在微信里办了一张**机器人临时工牌**"。两者都能收发消息，但工牌是官方发的、有明确权限边界；替身随时可能被平台请出去。所以本册所有微信操作都按 iLink bot 身份来理解，别套普通个人号自动化。

对已有 Hermes 基础的同学：接入后微信只是一个**消息通道**，AI 逻辑（模型、工具、技能）完全复用。你要做的只是"把微信消息喂进来、把 AI 回复发出去"，其余不用动。

## 3.2 gateway setup 扫码流程

在宿主机起一次性容器，复用第 2 章同一个数据卷：

```bash
# 复用 ~/.hermes 数据卷，跑 gateway setup 添加微信平台
docker run -it --rm \
  -v ~/.hermes:/opt/data \
  nousresearch/hermes-agent \
  gateway setup
```

流程三步：

1. **选平台**：在菜单中选择「微信个人号」。选项号为 **14** 是社区实操记录（W4），官方菜单未标数字、可能漂移——**以 setup 菜单实际为准**。
2. **扫码确认**：终端打印二维码 → 用手机微信扫码 → 手机上确认授权。
3. **落盘凭证**：成功后凭证写入 `~/.hermes/weixin/accounts/`，向导把配置写进 `~/.hermes/.env`。

[!warning] 跑 CLI 别用 docker exec
> 第 2 章提过：官方镜像里没有 `hermes` 可执行文件，`docker exec hermes gateway setup` 会直接报 PATH 找不到二进制。要跑 CLI，必须用上面的 `docker run -it --rm -v 同卷` 起一次性容器（W4）。

## 3.3 产物 E：`~/.hermes/.env` 微信配置

扫码完成后，setup 会在 `~/.hermes/.env` 写入微信配置段。完整文件先睹为快：

```env
# ~/.hermes/.env —— 微信（个人号 iLink）配置段
# setup 扫码后生成；必填两项，其余为可选，可留空用默认值

# ── 必填：bot 身份 ───────────────────────────────
WEIXIN_ACCOUNT_ID=wx_xxxxxxxxxxxxxxxx   # iLink bot 账号 ID（扫码得到的身份）
WEIXIN_TOKEN=xxxxx                      # iLink 访问令牌

# ── 可选：轮询连接 ───────────────────────────────
WEIXIN_POLL_INTERVAL=2                  # 长轮询间隔（秒）
WEIXIN_POLL_TIMEOUT=35                  # 单次 getupdates 超时（秒）

# ── 可选：收件范围与策略 ─────────────────────────
WEIXIN_ALLOWED_USERS=                   # allowlist 模式下的允许用户列表
WEIXIN_GROUP_POLICY=disabled            # open / allowlist / disabled / pairing
WEIXIN_HOME_CHANNEL=                    # 默认私聊对象

# ── 可选：语音处理 ───────────────────────────────
WEIXIN_STT_ENABLED=false                # 语音转文字开关
WEIXIN_STT_PROVIDER=                    # 转写后端（OpenAI 兼容 STT 等）
WEIXIN_SILK_CACHE_DIR=~/.hermes/weixin/silk  # 未转写时 SILK 音频缓存目录

# ── 可选：维护与调试 ─────────────────────────────
WEIXIN_TOKEN_REFRESH_MAX=3              # 凭证过期自动刷新上限（默认 3 次）
WEIXIN_MAX_TEXT_LENGTH=                 # 单条文本消息长度上限
WEIXIN_LOG_LEVEL=info                   # 微信适配器日志级别
```

> 键名说明：必填两项（`WEIXIN_ACCOUNT_ID` / `WEIXIN_TOKEN`）来自官方文档（W1）；可选键按功能要点整理，不同镜像版本可能增减命名，**以你当前 setup 生成的默认文件为准**——这里的作用是让你看懂每行在管什么。

逐段拆讲：

**必填：bot 身份。** 同时配了这两个键，gateway 才知道"用哪个 iLink bot、拿什么凭证去轮询"。`WEIXIN_ACCOUNT_ID` 是扫码得到的 bot 身份 ID，`WEIXIN_TOKEN` 是对应令牌，两者缺一不可。

[!tip] 大白话
> 把 `WEIXIN_TOKEN` 想成**门禁卡**：iLink 服务器认卡不认人，卡对了才放你进去取消息。卡丢了/错了，gateway 就一直在门口转圈（轮询失败）。这张卡只给 gateway 用，别贴到博客或仓库里。

**可选：轮询连接。** `WEIXIN_POLL_TIMEOUT=35` 就是 3.5 节长轮询的单次超时；间隔越大越省请求，但消息响应越慢。

**可选：收件策略。** 三个键对应 3.5 节的策略体系，留空即用适配器默认值。

**可选：语音。** iLink 收到语音默认先存成 SILK 音频；开 `WEIXIN_STT_ENABLED` 并配好 `WEIXIN_STT_PROVIDER` 才能转成文字进 AI 上下文。

**可选：维护。** `WEIXIN_TOKEN_REFRESH_MAX` 对应 3.6 节的"凭证过期自动刷新最多 3 次"。

## 3.4 `config.yaml` 的 `platforms.weixin.extra` 片段

`.env` 管密钥与连接，策略层面常驻配置写在 `~/.hermes/config.yaml` 的 `platforms.weixin.extra`：

```yaml
# ~/.hermes/config.yaml —— platforms.weixin 片段
platforms:
  weixin:
    extra:
      group_policy: disabled        # 群消息策略：open/allowlist/disabled/pairing
      allowed_users: []             # allowlist 模式的白名单
      home_channel: ""              # 默认私聊对象
      poll_interval: 2              # 长轮询间隔（秒）
      poll_timeout: 35              # 单次 getupdates 超时（秒）
```

这些键与 3.3 的可选环境变量同名同义。适配器通常"环境变量优先、config.yaml 兜底"或二选一读取，**谁先生效以你镜像版本的实现为准（需实测）**。为少踩坑：密钥放 `.env`、策略放 `config.yaml`，不要两处都写造成困惑（W1、W4）。

## 3.5 收发机制与能力边界

### 收发机制：长轮询，免公网

微信适配器不走 webhook、不走 WebSocket，也不需要 frp / 内网穿透——它用**长轮询 getupdates**：gateway 主动向 iLink 服务器挂一个请求等着（单次超时 35s），有消息就返回，没消息超时后再挂下一个（W1、W2）。

[!tip] 大白话
> 把长轮询想成**守着电话等来电**：不主动打出去（不发 webhook），而是把听筒一直贴耳边，来一条接一条。所以你的服务器不需要公网地址，只要能"打外线"（出站访问 `ilinkai.weixin.qq.com`）就行——国内部署尤其省事，不用穿透、不用备案域名。

### 支持的消息类型

5 种：**text（文本）/ image（图片）/ video（视频）/ file（文件）/ voice（语音）**。语音可转写进上下文；未开转写或转写失败时，以 **SILK 音频缓存**形式落盘，不直接变文字（W1、W2）。

### 交互方式：没有按钮卡片，走文本 slash 命令

iLink 通道没有 Telegram 那种 Inline Button，也没有卡片消息。需要用户做选择或触发操作时，用文本 slash 命令（如 `/help`）——适配器会把命令交给 Hermes 的指令路由处理（W1、W2）。

### 能力边界（重要）

| 维度 | 结论 |
|---|---|
| 群消息 | **默认不可用**。iLink bot 无法被拉进普通微信群，群聊相关功能默认关闭（W1） |
| 私聊 DM | 最稳定、最推荐的使用方式 |
| 交互控件 | 无按钮/卡片，只能文本 slash 命令 |
| 公网要求 | 免公网（长轮询出站即可） |
| 消息类型 | 5 种：text / image / video / file / voice |
| 语音 | 可转写，否则 SILK 缓存落盘 |

[!warning] 别被社区带偏："微信能拉群"是假象
> 官方与社区记录一致：iLink bot **进不了普通微信群**，不要写"把 AI 拉进微信群"。想进群做群聊 AI，要么走企业微信（第 4 章），要么走 QQ 非官方 NapCat 路线（第 8 章）——那是另一套风控逻辑。

### 收件策略：open / allowlist / disabled / pairing

微信适配器策略体系有四种（W1）：

| 策略 | 含义 | 适用 |
|---|---|---|
| `open` | 所有人可收发 | 自己测试 / 完全信任环境 |
| `allowlist` | 只响应白名单用户 | 日常推荐 |
| `disabled` | 关闭该方向（如群方向） | 关闭不用的通道 |
| `pairing` | 用户主动配对后才响应 | 陌生人防骚扰 |

> 建议默认 `group_policy=disabled` + 私聊用 `allowlist`，这也是第 10 章安全基线的预演。

## 3.6 已知坑

[!warning] 凭证过期自动刷新，最多 3 次
> iLink 访问凭证会过期。适配器会**自动刷新**，但刷新不是无限的——**最多重试 3 次**（对应错误码 **-14**），超过后该 bot 失效，只能回到 `gateway setup` 重新扫码（W1）。看到日志里 -14 刷不出来，别死磕配置，直接重扫最快。

[!warning] token/secret 明文落盘，数据卷就是泄露面
> `WEIXIN_TOKEN` 以明文写在 `~/.hermes/.env`，扫码凭证也在 `~/.hermes/weixin/accounts/`，都在数据卷上——**谁拿到你的数据卷，谁就拿到你的微信 bot 身份**。备份、上传、共享 `~/.hermes` 时要当它是密钥文件（W1、W4）。第 10 章会系统讲密钥落盘与轮换。

## 本章小结

- 微信个人号接入走**官方 iLink Bot API**（PR #7166 合入），扫码拿到的是 **iLink bot 身份**，不是 wechaty 式个人号自动化。
- 流程一句话：`docker run -it --rm -v ~/.hermes:/opt/data ... gateway setup` → 选微信个人号（选项号 14 为社区记录，**以菜单实际为准**）→ 扫码确认 → 凭证存 `~/.hermes/weixin/accounts/`。
- `.env` 必填 `WEIXIN_ACCOUNT_ID` + `WEIXIN_TOKEN`；约 11 个可选键管轮询、策略、语音、凭证刷新（键名以 setup 生成文件为准）。
- 收发靠**长轮询 getupdates（35s 超时）**，免公网、免穿透；支持 5 种消息类型；无按钮卡片，走文本 slash 命令。
- 能力边界要牢记：**群消息默认不可用、DM 最稳**；策略用 open / allowlist / disabled / pairing。
- 两个坑：凭证过期自动刷新最多 3 次（-14）；token/secret 明文落盘，数据卷 = 泄露面。

**下一章**：微信个人号只能私聊，那"企业里的微信"怎么办？第 4 章接入企业微信 AI Bot——它能进群、又走 WebSocket 免公网，能力边界和微信完全不同。

---

**本章素材**：W1（[Weixin 官方文档](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin)）、W2（[PR #7166 native Weixin](https://github.com/NousResearch/hermes-agent/pull/7166)）、W4（[CSDN 微信 Gateway + Compose 实操](https://blog.csdn.net/WeLoveCn/article/details/161239172)）。
