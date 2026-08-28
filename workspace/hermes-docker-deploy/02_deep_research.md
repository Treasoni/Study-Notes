# 02 深度研究 - Hermes Docker 部署 + 国内消息平台接入

> 项目：hermes-docker-deploy | 阶段：P2 深度收集
> 生成时间：2026-08-28

## Scope 范围

本册覆盖三块：
1. **Hermes 本体 Docker 部署**（官方镜像、数据卷、setup 向导、gateway 常驻、Compose、权限模型、升级排错）
2. **三个国内消息平台接入**：微信/企业微信、飞书、QQ（均为官方原生支持）
3. **部署后运维**：安全基线、密钥管理、资源建议、升级策略

不覆盖：Tool Gateway/自定义工具（见《Hermes Tool 配置指南》）、记忆/技能体系（见《上手实战》）。

## 源表

| ID | 标题 | URL | 层级 | 日期 | 用途 |
|----|------|-----|------|------|------|
| D1 | Docker 官方文档（zh-Hans + EN 互补） | https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker | official | 现行 | Docker 部署全章 |
| W1 | Weixin 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin | official | 现行 | 微信接入章 |
| W2 | PR #7166 native Weixin | https://github.com/NousResearch/hermes-agent/pull/7166 | official | 2026-04-10 | 微信能力/限制 |
| W3 | WeCom 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom | official | 现行 | 企业微信章 |
| W4 | CSDN 微信 Gateway + Compose 实操 | https://blog.csdn.net/WeLoveCn/article/details/161239172 | report | 2026 | 实操坑 |
| F1 | Feishu/Lark 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu | official | 现行 | 飞书接入章 |
| F2 | 仓库源码（版本/plugin/Dockerfile） | github.com/NousResearch/hermes-agent | official | 现行 | 版本勘误 |
| Q1 | QQ Bot 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot | official | 现行 | QQ 接入章 |
| Q2 | IT之家：腾讯 QQ 原生接入 Hermes | https://www.ithome.com/0/939/789.htm | report | 2026-04 | 背景 |
| Q4 | NapCat+NoneBot2 非官方路线 | https://nbility.ai/blog/hermes-agent-qq-group | community | 2026-05 | 非官方对比 |

## Claim / Source 映射

### A. Docker 部署（核心）

| Claim | 来源 |
|-------|------|
| 镜像 `nousresearch/hermes-agent`，官方示例用 `:latest`，无固定版本 tag 建议 | D1 §快速开始 |
| 数据卷：容器内 `/opt/data` ↔ 宿主机 `~/.hermes/`，唯一状态源（.env/config.yaml/SOUL.md/sessions/memories/skills/home/cron/hooks/logs/skins） | D1 §持久化卷 |
| 首次 setup 向导：`mkdir -p ~/.hermes && docker run -it --rm -v ~/.hermes:/opt/data nousresearch/hermes-agent setup`，写入 `.env` | D1 §快速开始 |
| gateway 常驻：`docker run -d --name hermes --restart unless-stopped -v ~/.hermes:/opt/data -p 8642:8642 nousresearch/hermes-agent gateway run`；纯聊天平台可省 `-p` | D1 §gateway 模式 |
| API Server 安全三件套：`API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0`（外露才设）+ `API_SERVER_KEY`（≥8 字符，`openssl rand -hex 32`） | D1 §API env vars |
| Compose 完整示例（含 8642 API、9119 dashboard、`HERMES_DASHBOARD=1`、memory 4G/cpus 2.0） | D1 §Compose |
| 镜像内置：debian:13.4、Python 3.13+uv、Node 26+npm、Playwright+Chromium、docker-cli（可 bind /var/run/docker.sock 驱动宿主 Docker）、openssh-client、s6-overlay v3 作 PID1 | D1 §Dockerfile |
| 权限模型：root 先 chown 卷 → `s6-setuidgid` 降权 hermes（UID 10000）；root 跑 gateway 默认被拒需 `HERMES_ALLOW_ROOT_GATEWAY=1`；`/opt/hermes` 只读安装树 | D1 §权限模型 |
| 日志四来源：docker logs（tee 到 `~/.hermes/logs/gateways/<profile>/current`）、dashboard 日志、container-boot.log、`hermes logs --follow` | D1 §日志 |
| 升级：pull 新镜像 + 重建容器，数据卷不动，先写时间戳备份再迁移 | D1 §升级 |
| 已知坑：权限 denied → `HERMES_UID/GID`（或 PUID/PGID）或 `chmod -R 755 ~/.hermes`；2026-08 前旧镜像 `/opt/hermes` 锁 0700 → `docker exec -u root hermes chmod 0755 /opt/hermes`；浏览器工具需 `--shm-size=1g`；禁止两 gateway 共享数据目录 | D1 §故障排查 |
| 版本：无 `RELEASE_v0.6.0.md`，官方用日期式 tag（如 v2026.8.27），pyproject 版本 0.20.6；飞书为 bundled plugin | F2 |

### B. 微信 / 企业微信

| Claim | 来源 |
|-------|------|
| 微信 = 个人号经 iLink Bot API 接入（ilinkai.weixin.qq.com），扫码得 iLink bot 身份，非普通个人号自动化 | W1 |
| 扫码流程：gateway setup → 二维码 → 手机确认 → 凭证存 `~/.hermes/weixin/accounts/`，过期自动刷新最多 3 次 | W1 |
| 长轮询 getupdates（35s 超时）→ 免公网，无 frp/webhook/WS 需求 | W1, W2 |
| 支持 5 种消息类型：text/image/video/file/voice（语音可转写否则 SILK 缓存）；无按钮/卡片，走文本 slash 命令 | W1, W2 |
| **群消息默认不可用**（iLink 无法拉入普通群）；DM 最稳定；策略 open/allowlist/disabled/pairing | W1 |
| 必填 `WEIXIN_ACCOUNT_ID`、`WEIXIN_TOKEN`；可选 11 个 env；config.yaml `platforms.weixin.extra` | W1, W2 |
| gateway setup 选项：微信个人号=选项 14（社区记录，官方未标数字，可能漂移）；企微 AI Bot=12、企微回调=13 | W4 |
| 企微两模式：AI Bot WebSocket（wss://openws.work.weixin.qq.com，免公网、实时双向+流式+自动重连）；自建应用回调（inbound webhook，需公网） | W3 |
| 企微必填 `WECOM_BOT_ID`+`WECOM_SECRET`；出站上限 text 4k/img 10MB/doc 20MB/voice 2MB，20MB 硬顶 | W3 |
| Docker 坑：`docker exec hermes` 报 PATH 找不到二进制（镜像无 hermes 可执行文件）→ 须 `docker run -it --rm -v 同卷` 跑 CLI；前台 gateway 断线即停，必须 compose detach | W4 |
| 安全：`WECOM_SECRET` 泄露=可冒充 bot；token/secret 明文落盘 `/root/.hermes`，数据卷即泄露面 | W3, W1 |
| **非 wechaty**：PR #7166 明确原生 iLink，非 wechaty 桥（旧 PR #2502 用 iLink 2.1.7） | W2 |

### C. 飞书 Feishu / Lark

| Claim | 来源 |
|-------|------|
| WebSocket 长连接为默认且推荐：出站连接、免公网 URL、SDK 管心跳重连；需 `websockets` 包 | F1 §Step2 |
| Webhook 可选：aiohttp 服务端点 `/feishu/webhook`，`FEISHU_WEBHOOK_HOST`(默认127.0.0.1)/PORT(8765)/PATH；需 `aiohttp`；限流 120 req/60s | F1 |
| 前置：A) `hermes gateway setup` 扫码自动建应用；B) 手动 open.feishu.cn 建应用 → App ID(cli_xxx)/App Secret → 开 Bot → 配权限/事件 → 发布（企业需管理员审批） | F1 §Step1 |
| 必填 `FEISHU_APP_ID`/`FEISHU_APP_SECRET`；可选 FEISHU_DOMAIN/CONNECTION_MODE/ALLOWED_USERS/HOME_CHANNEL/GROUP_POLICY/REQUIRE_MENTION 等 | F1 §All Env |
| 事件订阅：`im.message.receive_v1`（必）；`card.action.trigger`（交互卡）；文档评论/会议邀请可选 | F1 §Events |
| 权限 scope 必需：im:message、im:message:send_as_bot、im:resource、im:chat、im:chat:readonly | F1 §Permissions |
| 发送能力：send（markdown 自动探测 rich post，被拒回退纯文本）、send_image/document/voice/video/animation（GIF 降级文件） | F1 §Media |
| 已知坑：缺 lark-oapi/websockets/aiohttp；同 app_id 只能一个实例；群聊不响应查 @提及+GROUP_POLICY+allowlist；点按钮 200340=未开 Interactive Card；post 变纯文本=正常回退 | F1 §Troubleshooting |
| 勘误：官方文档**没有**「WebSocket 仅限企业自建应用」表述 | F1 |
| 版本：日期式 tag，飞书为 bundled plugin（plugins/platforms/feishu/），无 RELEASE_v0.6.0.md | F2 |

### D. QQ

| Claim | 来源 |
|-------|------|
| 官方适配器基于 QQ Bot API v2：WebSocket 收 + REST 发；覆盖私聊 C2C、群@、频道 | Q1 §Overview |
| 语音转写双阶段：QQ 内置 ASR（asr_refer_text）优先，失败回退 OpenAI 兼容 STT（默认 GLM/Whisper） | Q1 |
| 前置：q.qq.com 注册机器人取 AppID/AppSecret，启用 intents（C2C、群@、频道）；沙箱测→发布 | Q1 §Prerequisites |
| 必填 `QQ_APP_ID`/`QQ_CLIENT_SECRET`；可选 QQ_ALLOWED_USERS/GROUP_ALLOWED_USERS/PORTAL_HOST/STT_*；config.yaml `platforms.qqbot.extra`（markdown_support、dm/group_policy、stt） | Q1 |
| 沙箱：仅收沙盒测试频道消息；`QQ_PORTAL_HOST=sandbox.q.qq.com` | Q1 §Advanced |
| 已知坑：快速断开=凭证无效/缺 intents/沙箱收非沙箱流量；WS 静默断连（aiohttp 未设 heartbeat，issue #21633，修复=heartbeat≈50s+2 次无 ACK 强断）；WS 约 30 分钟 4009 会话超时需 watchdog+重启 | Q1, issue #21633 |
| 非官方路线：NapCat(QR 登普通 QQ)+OneBot v11→NoneBot2→Hermes API 8642；免官方审核、可进普通群，但风控/协议变化快；建议专用号+白名单+@触发+限流 | Q4 |
| NapCat Docker：镜像 `mlikiowa/napcat-docker`，映射 6099(WebUI)/3001，挂 config/qq/plugins 三卷 | Q4 |
| 背景：2026-04 腾讯 QQ「原生接入」= QQ Bot 插件合入 Hermes 官方 | Q2 |
| 未证实：TTS 401、无法发文件（社区反馈，官方文档无记录） | Q1 vs 社区 |

## 矛盾与需注意

1. **版本号**：P1 曾称「飞书 ≥v0.6.0」「微信 v0.9.0」——P2 勘误：官方用日期式 tag（当前 0.20.6 / v2026.8.27），无 RELEASE_v0.6.0.md；「v0.9.0」来自 PR #7166 合入窗口，仅供参考。写作时以「较新镜像/最新 tag」表述，避免引用不存在的版本文件。
2. **微信群消息**：官方 + 社区一致 = 不支持，勿写「能拉群」。
3. **选项号漂移**：gateway setup 的选项数字（微信 14 等）来自社区，官方未标，写作时标注「以 setup 菜单实际为准」。
4. **`PermissionError /opt/hermes/.env`**：上手实战第 8 章有记载；D1 官方文档未直接出现该表述，更准确的是「/opt/hermes 安装树 0700 锁 + UID 10000 降权」→ 修复 chmod 0755。新册以此为准，并可与旧册互补。
5. **ENTRYPOINT**：zh-Hans 说 s6 /init，英文版说 entrypoint-dispatch.sh（Fly/K8s 直跑 stage2），以英文版为准。
6. **API_SERVER_HOST 默认值**：文档仅暗示 loopback，未显式写 127.0.0.1。

## 开放问题（实测项，笔记中标注「需实测」）

- 健康端点具体 HTTP 路径
- 微信 iLink 群消息是否真完全不可用、多账号边界、token 过期(-14)自愈
- 飞书最低版本、Docker 无 TTY 时扫码建应用的替代
- QQ 生产模式审核门槛/时长、文件发送根因、markdown_support 生效条件
- 官方镜像 tag pin 策略（:latest vs 日期 tag）

## 实战指南（下游写作骨架）

1. Docker 部署基础：镜像/数据卷/setup/gateway/Compose/权限/升级
2. 微信接入：gateway setup 扫码 → 环境变量 → 长轮询免公网 → 私聊为主
3. 企业微信：AI Bot WebSocket 或自建应用回调 → WECOM_BOT_ID/SECRET
4. 飞书：手动建应用或扫码 → FEISHU_APP_ID/SECRET → WebSocket 免公网 → 事件订阅
5. QQ：q.qq.com 建机器人 → QQ_APP_ID/CLIENT_SECRET → intents → 沙箱→发布
6. 安全基线：API Server 三件套、密钥落盘即泄露面、公网暴露 fail-closed

## 下游交接

- **P3 大纲**：建议 9-11 章（Docker 部署 2 + 微信/企微 2-3 + 飞书 2 + QQ 2 + 运维安全 1）
- **写作用源 ID**：D1/W1/W2/W3/W4/F1/F2/Q1/Q2/Q4
- **用户偏好**：教程类「一章一节一文件」，核心概念加 `[!tip] 大白话`，代码块带文件头注释
