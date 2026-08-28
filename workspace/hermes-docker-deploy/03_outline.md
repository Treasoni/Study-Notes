## 学习笔记大纲：《用 Docker 部署 Hermes 并配置国内消息平台接入》

> 笔记类型：实战笔记（上手深度，详细步骤 + 配置方法）
> 预计总篇幅：约 35-45 页（短×1 + 中×7 + 长×2）
> 章节数：10 章 + README
> 输出格式：Obsidian 分册（README + 每章独立文件 + 前后导航双链）
> 目标位置：`AI学习/Hermes Agent/Hermes Docker 部署指南/`

### 分册定位

本册是《[[Hermes Agent 上手实战/README|Hermes Agent 上手实战]]》与《[[Hermes Tool 配置指南/README|Hermes Tool 配置指南]]》的姊妹分册，专讲「**用 Docker 把 Hermes 部署成常驻服务，并接入三个国内消息平台**」。上手实战第 8 章已概览 Docker 部署，本册不重复，而是把「部署 + 国内平台接入」这一专项做深：微信/企业微信、飞书、QQ 各自完整跑通，最后收束到运维与安全基线。

### 写作约定（贯穿全册）

- **核心概念**一律配 `[!tip] 大白话` 通俗解释 + 打比方类比。
- **代码块**统一带文件头注释标注所属路径（如 `# ~/.hermes/.env`）；有完整文件的章节遵循「**完整文件先睹为快 → 逐段拆讲 → 常见坑**」三拍结构。
- **易错点**用 `[!warning]`，**综合示例**用 `[!example]`，与姊妹分册风格一致。
- **版本表述**：镜像用「最新 tag / 日期式 tag（如 v2026.8.27）」，不引用不存在的 `RELEASE_v0.6.0.md`；gateway setup 的选项号标注「以 setup 菜单实际为准」。
- 每个平台章节都含一个「**能力边界**」小节，明确什么做得到、什么做不到，避免社区误导。

---

### 目录（章节目录）

| 编号 | 文件 | 标题 | 一句话说明 |
|------|------|------|-----------|
| README | `README.md` | 分册入口 | 定位、目录、与姊妹分册的关系、快速上手 |
| 01 | `01-镜像数据卷与首次setup.md` | 镜像、数据卷与首次 setup | 认识官方镜像、理解持久化、跑通首次 setup 向导 |
| 02 | `02-Gateway常驻与Compose编排.md` | Gateway 常驻与 Compose 编排 | gateway 模式 + 完整 docker-compose.yaml + 权限模型 + 升级 |
| 03 | `03-微信个人号iLink接入.md` | 微信个人号接入：iLink 扫码直连 | 扫码建号、长轮询免公网、5 种消息类型、群不可用边界 |
| 04 | `04-企业微信AI Bot与回调.md` | 企业微信接入：AI Bot 与自建应用回调 | 两种模式对比、WebSocket 免公网、出站限制 |
| 05 | `05-飞书建应用与WebSocket.md` | 飞书接入（上）：建应用与 WebSocket 长连接 | 两种建应用路线、WebSocket 免公网连接 |
| 06 | `06-飞书事件订阅与消息收发.md` | 飞书接入（下）：事件订阅、权限与消息收发 | 事件订阅、权限 scope、markdown/媒体发送、已知坑 |
| 07 | `07-QQ官方Bot基础接入.md` | QQ 接入（上）：官方 QQ Bot 基础接入 | q.qq.com 建机器人、intents、沙箱→发布 |
| 08 | `08-QQ进阶配置与NapCat替代.md` | QQ 接入（下）：进阶配置、语音转写与 NapCat 替代 | 语音双阶段转写、WS 断连坑、非官方 NapCat 路线对比 |
| 09 | `09-多平台运维与日志.md` | 多平台运维：日志、升级与日常管理 | 日志四来源、升级回滚、多平台并存约束 |
| 10 | `10-安全基线.md` | 安全基线：密钥、API Server 与公网暴露 | API Server 三件套、密钥落盘即泄露面、公网 fail-closed |

> 说明：用户原建议「运维安全（1 章）」，此处拆为「09 运维」+「10 安全」两章（总量 10 章仍在 9-11 建议区间内），因为安全基线素材足够独立成章且对「上手」用户价值高。若你希望合并为一章，我可直接合并为「第 9 章 多平台运维与安全基线」。

---

### 第一章：镜像、数据卷与首次 setup
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 1.1 认识官方镜像 `nousresearch/hermes-agent`：tag 策略（:latest vs 日期式 tag v2026.8.27）、镜像内置环境（Python 3.13+uv、Node 26、Playwright、docker-cli、s6-overlay）
  - 1.2 大白话：数据卷持久化 = 容器是临时工、`~/.hermes` 是档案柜（打比方）
  - 1.3 产物 A：数据卷目录树 `~/.hermes/`（.env / config.yaml / SOUL.md / sessions / memories / skills / cron / hooks / logs / skins）——带文件头注释的目录树先睹为快
  - 1.4 产物 B：首次 setup 命令 + 生成的 `~/.hermes/.env`（完整文件先睹为快 → 逐段拆讲关键键）
  - 1.5 常见坑：`PermissionError /opt/hermes/.env` 的准确机理（/opt/hermes 安装树 0700 锁 + UID 10000 降权）→ 修复 `HERMES_UID/GID` 或 `chmod -R 755 ~/.hermes`
- **素材引用**：D1（§快速开始 / §持久化卷 / §Dockerfile / §故障排查）、F2
- **代码示例**：有（docker run setup 命令、`~/.hermes/.env` 完整文件、目录树）

### 第二章：Gateway 常驻与 Compose 编排
- **篇幅**：长（5+ 页）
- **覆盖要点**：
  - 2.1 产物 C：gateway 常驻 `docker run -d --restart unless-stopped -p 8642:8642 ... gateway run`（先睹为快 → 拆讲各参数；纯聊天平台可省 -p）
  - 2.2 产物 D：`docker-compose.yaml` 完整示例（先睹为快）——含 8642 API、9119 dashboard、`HERMES_DASHBOARD=1`、memory 4G / cpus 2.0
  - 2.3 `docker-compose.yaml` 逐段拆讲：services / ports / volumes / environment / 资源限制
  - 2.4 权限模型：root 先 chown 卷 → `s6-setuidgid` 降权 UID 10000、`/opt/hermes` 只读安装树、`HERMES_ALLOW_ROOT_GATEWAY`、ENTRYPOINT 口径（英文版 entrypoint-dispatch.sh 为准）
  - 2.5 升级与重建：时间戳备份 → pull 新镜像 → 重建容器，数据卷不动
  - 2.6 常见坑：`docker exec` 报 PATH 找不到二进制（镜像无 hermes 可执行文件，须 `docker run -it --rm -v 同卷` 跑 CLI）、两个 gateway 共享数据目录排他锁、浏览器工具需 `--shm-size=1g`
- **素材引用**：D1（§gateway 模式 / §Compose / §权限模型 / §升级 / §故障排查）、F2、W4
- **代码示例**：有（gateway docker run、`docker-compose.yaml` 完整 + 逐段拆讲、备份/升级命令）

### 第三章：微信个人号接入：iLink 扫码直连
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 3.1 背景与定性：个人号经 iLink Bot API 接入（原生 iLink，**非 wechaty** 桥；扫码得 iLink bot 身份，非普通个人号自动化）
  - 3.2 gateway setup 扫码流程：二维码 → 手机确认 → 凭证存 `~/.hermes/weixin/accounts/`（选项号 14 为社区记录，以 setup 菜单实际为准）
  - 3.3 产物 E：`~/.hermes/.env` 微信配置（必填 `WEIXIN_ACCOUNT_ID` / `WEIXIN_TOKEN` + 可选 11 项，完整文件先睹为快 → 逐段拆讲）
  - 3.4 `config.yaml` 的 `platforms.weixin.extra` 片段
  - 3.5 收发机制与能力边界：长轮询 getupdates（35s 超时）免公网、5 种消息类型（text/image/video/file/voice，语音可转写否则 SILK 缓存）、无按钮/卡片走文本 slash 命令、**群消息默认不可用**（iLink 无法拉入普通群）、DM 最稳定、策略 open/allowlist/disabled/pairing
  - 3.6 已知坑：凭证过期自动刷新最多 3 次（-14）、token/secret 明文落盘
- **素材引用**：W1、W2、W4
- **代码示例**：有（`~/.hermes/.env` 微信配置完整文件、`config.yaml` 片段、gateway setup 流程命令）

### 第四章：企业微信接入：AI Bot 与自建应用回调
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 4.1 两种模式对比表：AI Bot WebSocket（`wss://openws.work.weixin.qq.com`，免公网、实时双向+流式+自动重连）vs 自建应用回调（inbound webhook，需公网 URL）
  - 4.2 gateway setup 选项：企微 AI Bot≈12、企微回调≈13（社区记录，以菜单为准）
  - 4.3 产物 F：`~/.hermes/.env` 企微配置（必填 `WECOM_BOT_ID` + `WECOM_SECRET`，完整文件先睹为快 → 逐段拆讲）
  - 4.4 出站限制与能力边界：text 4k / img 10MB / doc 20MB / voice 2MB，20MB 硬顶
  - 4.5 Docker 场景排错：`docker exec hermes` 找不到二进制、前台 gateway 断线即停 → 必须 compose detach
  - 4.6 安全提示：`WECOM_SECRET` 泄露 = 可冒充 bot
- **素材引用**：W3、W4
- **代码示例**：有（`~/.hermes/.env` 企微配置完整文件、模式对比配置片段）

### 第五章：飞书接入（上）：建应用与 WebSocket 长连接
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 5.1 两种建应用路线：A) `hermes gateway setup` 扫码自动建应用；B) 手动 open.feishu.cn 建应用（App ID `cli_xxx` / App Secret → 开 Bot → 配权限/事件 → 发布，企业需管理员审批）
  - 5.2 连接模式：WebSocket 长连接为默认且推荐（出站连接、免公网 URL、SDK 管心跳重连，需 `websockets` 包）；Webhook 可选（aiohttp 服务端点 `/feishu/webhook`、`FEISHU_WEBHOOK_HOST` 默认 127.0.0.1 / PORT 8765 / PATH、限流 120 req/60s）
  - 5.3 产物 G：`~/.hermes/.env` 飞书配置（必填 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` + 可选 `FEISHU_DOMAIN` / `CONNECTION_MODE` / `ALLOWED_USERS` / `HOME_CHANNEL` / `GROUP_POLICY` / `REQUIRE_MENTION` 等，完整文件先睹为快 → 逐段拆讲）
  - 5.4 依赖检查：缺 `lark-oapi` / `websockets` / `aiohttp` 的后果
  - 5.5 勘误：官方文档**没有**「WebSocket 仅限企业自建应用」表述
- **素材引用**：F1（§Step1 / §Step2 / §All Env / §Troubleshooting）
- **代码示例**：有（`~/.hermes/.env` 飞书配置完整文件、WebSocket/Webhook 二选一说明）

### 第六章：飞书接入（下）：事件订阅、权限与消息收发
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 6.1 事件订阅：`im.message.receive_v1`（必）、`card.action.trigger`（交互卡）、文档评论/会议邀请（可选）
  - 6.2 权限 scope 五件套：`im:message`、`im:message:send_as_bot`、`im:resource`、`im:chat`、`im:chat:readonly`
  - 6.3 消息发送能力：send（markdown 自动探测 rich post，被拒回退纯文本）、send_image / document / voice / video / animation（GIF 降级文件）
  - 6.4 产物 H：`config.yaml` 的 `platforms.feishu` 片段（CONNECTION_MODE / GROUP_POLICY / ALLOWED_USERS / REQUIRE_MENTION）
  - 6.5 已知坑：同 app_id 只能一个实例、群聊不响应 → 查 @ 提及 + GROUP_POLICY + allowlist、点按钮 200340 = 未开 Interactive Card、post 变纯文本 = 正常回退
- **素材引用**：F1（§Events / §Permissions / §Media / §Troubleshooting）、F2
- **代码示例**：有（`config.yaml` 飞书片段、事件/权限对照表）

### 第七章：QQ 接入（上）：官方 QQ Bot 基础接入
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 7.1 背景：2026-04 腾讯 QQ「原生接入」= QQ Bot 插件合入 Hermes 官方
  - 7.2 架构：官方适配器基于 QQ Bot API v2（WebSocket 收 + REST 发），覆盖私聊 C2C、群 @、频道
  - 7.3 前置：q.qq.com 注册机器人取 AppID / AppSecret → 启用 intents（C2C、群@、频道）→ 沙箱测 → 发布
  - 7.4 产物 I：`~/.hermes/.env` QQ 配置（必填 `QQ_APP_ID` / `QQ_CLIENT_SECRET` + 可选 `QQ_ALLOWED_USERS` / `GROUP_ALLOWED_USERS` / `PORTAL_HOST`，完整文件先睹为快 → 逐段拆讲）
  - 7.5 沙箱测试与发布：仅收沙盒测试频道消息、`QQ_PORTAL_HOST=sandbox.q.qq.com`
- **素材引用**：Q1（§Overview / §Prerequisites / §Advanced）、Q2
- **代码示例**：有（`~/.hermes/.env` QQ 配置完整文件、intents 清单）

### 第八章：QQ 接入（下）：进阶配置、语音转写与 NapCat 替代
- **篇幅**：长（5+ 页）
- **覆盖要点**：
  - 8.1 `config.yaml` 的 `platforms.qqbot.extra`：`markdown_support`、dm / group_policy、stt
  - 8.2 语音转写双阶段：QQ 内置 ASR（`asr_refer_text`）优先 → 失败回退 OpenAI 兼容 STT（默认 GLM/Whisper），`STT_*` env
  - 8.3 已知坑：快速断开 = 凭证无效 / 缺 intents / 沙箱收非沙箱流量；WS 静默断连（aiohttp 未设 heartbeat，issue #21633，修复 ≈ heartbeat 50s + 2 次无 ACK 强断）；WS 约 30 分钟 4009 会话超时 → watchdog + 重启
  - 8.4 非官方路线对比：NapCat（QR 登普通 QQ）+ OneBot v11 → NoneBot2 → Hermes API 8642；免官方审核、可进普通群，但风控/协议变化快 → 建议专用号 + 白名单 + @触发 + 限流
  - 8.5 产物 J：NapCat `docker-compose.yaml`（镜像 `mlikiowa/napcat-docker`、映射 6099 WebUI / 3001、挂 config/qq/plugins 三卷）
  - 8.6 需实测项：文件发送根因、`markdown_support` 生效条件、TTS 401（社区反馈官方未记录）
- **素材引用**：Q1、Q4、issue #21633
- **代码示例**：有（`config.yaml` qqbot 片段、NapCat `docker-compose.yaml` 完整文件）

### 第九章：多平台运维：日志、升级与日常管理
- **篇幅**：短（约 1-2 页）
- **覆盖要点**：
  - 9.1 日志四来源：docker logs（tee 到 `~/.hermes/logs/gateways/<profile>/current`）、dashboard 日志、container-boot.log、`hermes logs --follow`
  - 9.2 升级流程与回滚：pull 新镜像 + 重建容器，数据卷不动，先写时间戳备份再迁移
  - 9.3 多平台并存注意事项：禁止两个 gateway 共享数据目录（排他锁）、同 app_id 只能一个实例
  - 9.4 资源建议：memory 4G / cpus 2.0（复述 Compose 示例）
  - 9.5 需实测项：健康端点具体 HTTP 路径、官方镜像 tag pin 策略（:latest vs 日期 tag）
- **素材引用**：D1（§日志 / §升级 / §故障排查）、F1、F2
- **代码示例**：有（日志查看命令、升级/备份脚本）

### 第十章：安全基线：密钥、API Server 与公网暴露
- **篇幅**：中（约 3-5 页）
- **覆盖要点**：
  - 10.1 产物 K：API Server 安全三件套（`API_SERVER_ENABLED=true` + `API_SERVER_HOST=0.0.0.0`（外露才设）+ `API_SERVER_KEY` ≥8 字符，`openssl rand -hex 32` 生成）——`.env` 安全版先睹为快 → 逐段拆讲
  - 10.2 密钥落盘即泄露面：token/secret 明文落 `~/.hermes`（`.env`），数据卷 = 泄露面；WECOM_SECRET 泄露可冒充 bot
  - 10.3 公网暴露 fail-closed：`API_SERVER_HOST` 默认 loopback（官方未显式写 127.0.0.1，按默认仅本机处理）；不配 KEY 就不要开 0.0.0.0
  - 10.4 Docker 权限最小化：UID 10000 降权、`/opt/hermes` 只读安装树、`HERMES_UID/GID` / `HERMES_ALLOW_ROOT_GATEWAY` 的正确用法
  - 10.5 平台侧安全 checklist：allowlist / 群策略 / @ 提及 / 密钥轮换 / 专用号隔离
- **素材引用**：D1（§API env vars / §权限模型）、W1、W3、F1、Q1
- **代码示例**：有（`.env` 安全版完整文件、`openssl rand -hex 32` 命令、加固版 compose 片段）

---

## 学习路径说明

### 前置要求
- 已有《[[Hermes Agent 上手实战/README|Hermes Agent 上手实战]]》基础（至少读过第 2、8 章），了解 Hermes 的基本概念（模型 provider、`config.yaml`、`.env`、skill）。
- 本机装好 Docker Engine 与 Docker Compose（可用 `docker --version`、`docker compose version` 验证）。
- 至少一个国内消息平台账号：个人微信 / 企业微信管理员权限 / 飞书账号 / QQ 号（实名），并注册对应开放平台账号（open.feishu.cn、q.qq.com、work.weixin.qq.com）。

### 学完能做什么
- 用 Docker 把 Hermes 跑成常驻 gateway，数据持久化在宿主机 `~/.hermes`，重启不丢状态。
- 用 `docker-compose.yaml` 一键编排 API Server + Dashboard，并理解权限模型与升级流程。
- 三个国内平台各自完整接入：微信（个人号 iLink）、企业微信（AI Bot/回调）、飞书（WebSocket/Webhook）、QQ（官方 Bot/非官方 NapCat），均免公网收发消息。
- 对每个平台的能力边界心里有数：微信不能进普通群、飞书要配事件订阅与权限、QQ 有沙箱→发布流程、出站大小限制。
- 会看四类日志定位问题、安全地升级镜像、给 API Server 上安全三件套、按 checklist 加固密钥与公网暴露。

### 建议学习顺序
- **按平台选读**（推荐）：`01 → 02 → 你关心的平台章节 → 09 → 10`。平台章节互相独立，微信/企微 = 03+04，飞书 = 05+06，QQ = 07+08。
- **全平台通读**：`01 → 02 → 03/04 → 05/06 → 07/08 → 09 → 10`。
- **时间预估**：每章约 30-60 分钟（含动手验证），全册约 6-8 小时；`02`（Compose）与 `08`（NapCat）最长，可拆两次看。
- **动手建议**：每章末尾按「先睹为快」的完整文件照抄一遍到自己的 `~/.hermes/`，再逐段理解；平台接入前先跑通 `01` 的 setup 向导。
- 写作用源 ID 映射：D1 / W1 / W2 / W3 / W4 / F1 / F2 / Q1 / Q2 / Q4（见 02_deep_research.md 源表）。
