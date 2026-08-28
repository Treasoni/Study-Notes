---
title: QQ 接入（下）：进阶配置、语音转写与 NapCat 替代
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
  - QQ
created: 2026-08-28
updated: 2026-08-28
status: 已完成
source_project: hermes-docker-deploy
---

> [[07-QQ官方Bot基础接入|⬅ 上一章]] · [[README|📖 返回目录]] · [[09-多平台运维与日志|下一章 ➡]]

# QQ 接入（下）：进阶配置、语音转写与 NapCat 替代

## 本章要解决什么问题

上一章我们走通了官方 QQ Bot 的「建号 → intents → 沙箱 → 发布」全流程，Hermes 已经能收 C2C 私聊、群 @ 和频道消息。但把机器人真正放进日常使用，你会发现还差几块拼图：**怎么让机器人在群里更听话（群策略）、怎么处理语音消息、为什么 WebSocket 会悄悄断线、以及——官方号过不了审核时有没有别的路？**

本章就是回答这四个问题。我们会先改 `config.yaml` 把 QQ 平台调到「可上生产」的状态，再讲语音转写的双阶段兜底机制，然后花一半篇幅处理两类「不稳定」：一类是官方 WS 连接的断连坑，另一类是完全绕过官方体系的 **NapCat 非官方路线**——它免审核、能进普通群，但要拿风控和安全去换。最后列出官方文档没写清楚、需要你实测确认的几件事。

> [!tip] 大白话：本章一条主线
> 把接入 QQ 想成「给 Agent 办一张进 QQ 的门禁卡」：官方通道是**工牌上盖了章（审核）的正式卡**，NapCat 是**走员工通道刷脸进去的普通卡**。上一章办的是正式卡，本章先教你把正式卡刷得更顺（配置 + 语音 + 排断连），再给你看普通卡怎么用、以及用它要担什么风险。

---

## 8.1 `config.yaml` 的 `platforms.qqbot.extra`：把策略调到生产态

第 7 章的 `.env` 解决的是「**能不能连**」（AppID/AppSecret/白名单），而 `config.yaml` 的 `platforms.qqbot.extra` 解决的是「**连上之后怎么表现**」。它管三件事：消息要不要按 markdown 渲染、私聊和群分别用哪种接收策略、语音要不要转文字。

完整片段先睹为快（以官方文档 Q1 的键为准，键名随版本可能有微调）：

```yaml
# ~/.hermes/config.yaml —— platforms.qqbot.extra 完整片段
platforms:
  qqbot:
    enabled: true
    extra:
      # 群/频道消息按 QQ 富文本 markdown 渲染，而不是纯文本
      markdown_support: true

      # 私聊（C2C）策略：open=来者不拒 / allowlist=只收白名单 / disabled=关私聊
      dm_policy: allowlist

      # 群聊策略：mention=只在被 @ 时响应 / allowlist=只回白名单群 / disabled=不进群
      group_policy: mention

      # 语音转写：先走 QQ 内置 ASR，失败回退到 STT_* 指定的 OpenAI 兼容服务
      stt:
        fallback: true
```

逐段拆讲：

- **`markdown_support: true`**：打开后，Hermes 给群/频道发的消息会带上 QQ 的富文本 markdown 格式（标题、列表、加粗等），可读性明显更好。但它**不是所有场景都生效**——QQ 对不同消息类型和场景有白名单，这属于本章 8.6 的「需实测项」。
- **`dm_policy` 与 `group_policy`**：和微信（第 3 章）、飞书（第 5/6 章）的 `GROUP_POLICY` 是同一套思路，只是 QQ 把私聊和群拆成两个键。生产建议：私聊开 `allowlist` 配合 `QQ_ALLOWED_USERS`，群开 `mention`——只在你 @ 它的时候才回，能挡住绝大多数误触和刷屏。

> [!tip] 大白话：`dm_policy` / `group_policy`
> 把机器人想成一个「门卫」。`dm_policy` 是**私人会客厅的门禁**：`open` 是任何人敲门都开，`allowlist` 是只放通讯录上的人。`group_policy` 是**大厅广播规则**：`mention` 是只在有人喊你名字（@）时才应一声，`disabled` 是压根不参与大厅话题。一般你不想让机器人在每个群里都自动接话，所以默认 `mention` 最稳。

---

## 8.2 语音转写双阶段：QQ 内置 ASR 优先，失败回退 OpenAI 兼容 STT

QQ 里经常有人发语音。Hermes 的语音处理是「**双阶段兜底**」：先用 QQ 官方内置的语音识别拿到参考文本，如果这一步拿不到（格式不支持、识别失败、被限流），再回退到你配的 OpenAI 兼容语音转写服务（官方默认指向 GLM / Whisper 一类的兼容端点）。

这个兜底链路由 `platforms.qqbot.extra.stt` 和一组 `STT_*` 环境变量共同驱动：

```bash
# ~/.hermes/.env —— QQ 语音回退 STT 部分（键名按实际版本为准）
STT_PROVIDER=openai_compatible   # 回退服务类型，默认走 OpenAI 兼容协议
STT_BASE_URL=https://api.openai.com/v1   # 换成你的 GLM / Whisper / 自建端点
STT_MODEL=whisper-1              # 具体转写模型名，按服务商填
STT_API_KEY=sk-...               # 回退服务的密钥，明文落盘，注意保管
```

双阶段的实际顺序是：

1. **QQ 内置 ASR**：Hermes 把收到的语音消息喂给 QQ Bot API 自带的语音识别，取回 `asr_refer_text`（参考文本）作为转写结果。这一步免费、无需额外配置，是默认首选。
2. **回退 STT**：当内置 ASR 拿不到可用文本时，把语音缓存文件交给 `STT_*` 指定的 OpenAI 兼容端点转写，再进入 Agent 的文本处理管线。

> [!tip] 大白话：双阶段语音转写
> 把它想成**餐厅点单**：第一选择是找店里跑堂的（QQ 内置 ASR）——不用花钱、顺手就记了；可要是跑堂的没听清（识别失败），就请门外那个会多国语言的大厨（OpenAI 兼容 STT）来听，只是这顿要加钱（消耗你的 STT API 配额）。所以默认先让跑堂试，实在不行才请大厨。

**实践建议**：平时可以不配 `STT_*`，靠内置 ASR 就够了；等你在日志里看到「语音转写失败 / asr_refer_text 为空」的告警，再补上回退端点不迟。密钥会明文落在 `~/.hermes/.env`（数据卷即泄露面，详见第 10 章），STT 密钥建议单独申请、额度受限，别拿主 key 顶。

---

## 8.3 已知坑：官方连接的三大不稳定源

官方 QQ Bot 接入最常见的排障场景不是「连不上」，而是「连上了又掉」。按出现顺序排，有三大类：

### 坑一：快速断开 = 凭证无效 / 缺 intents / 沙箱收非沙箱流量

如果 WebSocket 建立后**几秒内就被服务端断开**，优先按以下顺序排查（Q1 §Prerequisites）：

1. **凭证无效**：`QQ_APP_ID` / `QQ_CLIENT_SECRET` 抄错、或机器人被停用——回 q.qq.com 核对，必要时重置 Secret。
2. **缺 intents**：第 7 章说过必须在 q.qq.com 后台勾选对应的 intents（C2C、群 @、频道）。**漏勾哪一项，那一路连接就会被服务端判为非法直接断开**，不是「不推消息」而是「断开」，这是最容易误判的点。
3. **沙箱收非沙箱流量**：处于沙箱期时，官方只接受沙盒测试频道消息；如果你拿 `QQ_PORTAL_HOST=sandbox.q.qq.com` 却往正式场景发消息，会被当作异常流量断开。

> [!warning] 快速断开 ≠ 网络问题
> 先查应用层（凭证 / intents / 沙箱），别急着怪网络或镜像。快速断连 90% 是上面三件事之一，查 q.qq.com 后台的 intents 勾选是最快的一步。

### 坑二：WS 静默断连（aiohttp 未设 heartbeat，issue #21633）

这是社区确认的「**静默**」断连：连接看起来还活着，没有报错，但消息已经不推了。根因是底层 aiohttp 的 WebSocket 客户端**没设置 heartbeat**，中间设备（负载均衡 / NAT）会把长时间无流量的连接悄悄回收，而客户端完全感知不到。对应的修复方案社区记为 **heartbeat ≈ 50 秒 + 连续 2 次无 ACK 即强断重连**——把「探测心跳」和「对端失联判定」都做上，让假活连接在 2 分钟内暴露并自愈（issue #21633）。

> [!tip] 大白话：静默断连
> 像两个人打电话，聊到一半都不说话了，谁也没挂，可中间的电话交换机以为你们打完了就把线路掐了——两边还举着话筒以为对方在听。heartbeat 就是**每隔 50 秒互相「喂」一声**确认还在；连喂两声都没回，就说明真断了，赶紧重拨。这是保活 WebSocket 的标准动作。

### 坑三：WS 约 30 分钟 4009 会话超时 → watchdog + 重启

即使 heartbeat 正常，QQ Bot API 的 WS 会话还有一个**大约 30 分钟的服务端会话超时**，表现为收到 `4009` 错误码。这不是你配置错了，而是平台侧的会话生命周期到了。应对方式是让 gateway 具备「**看到 4009 → 主动重建连接**」的自愈能力：在 Hermes 侧就是依赖 watchdog 监控连接健康度并触发重启，部署侧则可以配合 `--restart unless-stopped` + 容器内 supervisor 兜底。

> [!warning] 4009 是预期内的回收信号
> 不要把它当成事故去翻配置。真正要做的是**确保有东西盯着连接并在 4009 后自动重连**，否则 30 分钟到点后 bot 会静默变哑，而你毫无察觉。日志里周期性出现 4009 而随后成功重连，属于正常现象。

---

## 8.4 非官方路线对比：NapCat + OneBot v11 + NoneBot2 → Hermes

官方 Bot 有两道坎：**要过审核**、**进不了普通群**。社区给出的替代路线（Q4）是把「登录层」和「对话层」拆开：

```text
普通 QQ 号
   │  QR 扫码登录（NapCat，容器内）
   ▼
NapCat（模拟官方客户端协议，把消息转成 OneBot v11 事件）
   │  正向/反向 WebSocket（默认端口 3001）
   ▼
NoneBot2（OneBot 协议框架，负责路由 + 权限 + 回复格式）
   │  HTTP 调用 Hermes API Server（端口 8642，需开 API_SERVER_ENABLED）
   ▼
Hermes Agent
```

走这条路的**动机**非常明确：免官方审核、能进普通群、能用普通 QQ 号长期挂着。但它不是免费的午餐，付出的是三样东西：

| 维度 | 官方 QQ Bot（第 7 章 + 本章前半） | NapCat 非官方路线 |
|------|----------------------------------|--------------------|
| 账号类型 | q.qq.com 注册的 Bot 机器人 | 任意普通 QQ 号 |
| 审核 | 需过平台审核 | 免审核 |
| 进普通群 | ❌ 不支持 | ✅ 支持 |
| 风控风险 | 低（官方授权） | 高（协议模拟，号可能被风控/冻结） |
| 协议稳定性 | 官方 API，稳定 | 协议变化快，要跟随 NapCat 更新 |
| 接入成本 | 改 `.env` + `config.yaml` 即可 | 多一层容器（NapCat）+ 一套框架（NoneBot2） |
| 适用场景 | 正规、长期、可过审的 bot | 测试 / 自用 / 进普通群刚需 |

> [!warning] NapCat 路线的风控是「账号级」的
> 协议模拟有被腾讯风控识别并冻结普通 QQ 号的风险，**不是**「最多消息发不出去」这么轻。所以社区共识是：**专用小号、不加任何白名单以外的群、消息触发只认 @、给回复频率上限流**——四个措施一起上，把风险压到可接受范围（Q4）。绝不要拿自己的主号去跑。

**接入 Hermes 的最后一公里**：NapCat + NoneBot2 只负责「把普通 QQ 的消息收进来」，真正干活的是 Hermes。两者靠 Hermes 的 API Server 对接——即第 10 章的 `API_SERVER_ENABLED=true` + `API_SERVER_KEY`，NoneBot2 把收到的用户消息 POST 给 `http://hermes:8642/...` 换取回复。**这意味着走这条路的前提是先开好 API Server 并配上密钥**，密钥与公网暴露的安全要点请同步阅读第 10 章。

---

## 8.5 产物 J：NapCat `docker-compose.yaml`

NapCat 官方推荐用 Docker 跑，镜像为 `mlikiowa/napcat-docker`。完整文件先睹为快：

```yaml
# ~/qq-napcat/docker-compose.yaml —— NapCat 完整示例
services:
  napcat:
    image: mlikiowa/napcat-docker:latest   # 社区镜像，tag 随版本迭代
    container_name: napcat
    restart: unless-stopped                # 断线自动拉起，配合 4009 自愈
    ports:
      - "6099:6099"   # NapCat WebUI 管理面板（扫码登录 / 查看状态）
      - "3001:3001"   # OneBot v11 正向 WebSocket，给 NoneBot2 用
    volumes:
      - ./config:/app/napcat/config        # 卷 1：NapCat 配置
      - ./qq:/root/.config/QQ              # 卷 2：QQ 登录态（数据持久化，重启不掉登录）
      - ./plugins:/app/napcat/plugins      # 卷 3：插件目录
    environment:
      - NAPCAT_UID=1000                    # 与宿主机 UID 对齐，避免卷权限问题
      - NAPCAT_GID=1000
```

逐段拆讲：

- **`image: mlikiowa/napcat-docker`**：社区维护的 NapCat 镜像（Q4 记录）。**镜像较活跃、tag 变化快**，`latest` 适合跟随更新；要稳定就 pin 到具体日期 tag。
- **端口**：`6099` 是 NapCat 的 WebUI（在这里扫码登录普通 QQ、看连接状态）；`3001` 是 OneBot v11 正向 WebSocket，NoneBot2 从这里订阅消息。**这两个端口都可以只绑 `127.0.0.1`**（写成 `127.0.0.1:6099:6099`），没必要暴露到公网。
- **三卷**：`config`（NapCat 自身配置）、`qq`（**QQ 登录态**——必须持久化，否则容器一重启就要重新扫码）、`plugins`（插件目录，供 OneBot/NoneBot 扩展用）。
- **`NAPCAT_UID/GID`**：和 Hermes 镜像的 UID 降权同一套思路（见第 2 章权限模型），对齐宿主机 UID 能避免卷里文件属主混乱。

常见坑：

1. **登录态不持久 = 天天扫码**：`./qq:/root/.config/QQ` 这卷是命根子，漏挂或目录权限不对，容器每次重启都会掉登录。
2. **端口直接绑 0.0.0.0**：`3001` 和 `6099` 都暴露到公网且无鉴权的话，等于把「控制你 QQ 号的入口」挂网上——绑定 `127.0.0.1` 即可挡住外部扫描。
3. **镜像版本漂移**：协议更新后老镜像可能连不上 QQ，升级前先看镜像仓库的 release 说明。

> [!warning] 这是「需实测」产物
> 上面 `6099` / `3001` 端口含义与三卷的容器内路径，是社区通用写法（Q4）。NapCat 镜像版本更新可能调整挂载路径——**首次部署以你拉到的镜像实际目录为准**，跑起来后进 WebUI 核对。

---

## 8.6 需实测项：官方文档没写清楚的三件事

以下三点来自社区反馈，官方文档 Q1 没有明确记录，**写进笔记但不做定论**，你实际部署时留意：

1. **文件发送根因**：社区反馈官方 QQ Bot「发不了文件」，但根因（是类型白名单、大小限制还是 markdown 模式冲突）**官方未记录**。需要实测：构造不同文件类型/大小，看日志里发送接口的真实报错码。
2. **`markdown_support` 生效条件**：官方只提了有这个开关，没说它在哪些消息类型/哪些场景下生效。需实测：普通群 vs 频道、文字 vs 卡片，`markdown_support` 是否真的渲染。
3. **TTS 401**：社区有人反馈语音合成（TTS）请求返回 401，但官方文档**没有该限制的记录**。需实测：401 是凭证问题还是平台侧未开放，若反复出现建议走官方工单确认。

> [!warning] 社区反馈 ≠ 官方行为
> 上述三条来自 Q4 等社区渠道，可能随版本和平台策略变化。**别把社区单点反馈当成官方 bug 表**；遇到时按「日志实际报错 → 版本核对 → 官方工单」的顺序处理，并把你实测到的结论回补到本笔记。

---

## 本章小结

- `platforms.qqbot.extra` 三键管三件事：`markdown_support` 管渲染、`dm_policy`/`group_policy` 管私聊与群的接收策略、`stt` 管语音回退。生产建议私聊 `allowlist` + 群 `mention`。
- 语音转写是双阶段兜底：QQ 内置 ASR（`asr_refer_text`）优先，拿不到文本再回退到 `STT_*` 指定的 OpenAI 兼容端点（默认 GLM/Whisper）。
- 官方 WS 的三大不稳定源：快速断开查凭证/intents/沙箱；静默断连是 aiohttp 未设 heartbeat（issue #21633），修复 ≈ 50s 心跳 + 2 次无 ACK 强断；30 分钟 4009 会话超时是预期行为，靠 watchdog + 重启自愈。
- 官方 vs NapCat 的本质是「审核与普通群」换「风控与协议稳定性」；选 NapCat 必须专用号 + 白名单 + @ 触发 + 限流四件套。
- 产物 J：NapCat `docker-compose.yaml` 一份，`6099`/`3001` + config/qq/plugins 三卷，QQ 登录态卷必须持久化。
- 文件发送根因、`markdown_support` 生效条件、TTS 401 三件事**需实测**，社区反馈不代表官方行为。

> **下一章**：QQ 这条线到这里就跑通了。但多个平台一起挂上之后，怎么在四类日志里定位「到底是哪个平台掉线」、怎么安全升级镜像、两个 gateway 为什么不能共享数据目录——交给下一章 [[09-多平台运维与日志|多平台运维与日志]]。
