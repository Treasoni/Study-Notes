# 更新报告：06-多平台接入与定时任务.md

> 日期：2026-08-28 · 模式：patch-in-place · 状态：已完成

## 变更摘要

1. **章节引言**：平台列表由「Telegram、Discord 等」扩为「Telegram、Discord、Home Assistant 等」。
2. **6.1 新增子节「Home Assistant：智能家居双向接入」**：
   - 一个 Long-Lived Access Token 激活两条通道（Gateway 事件通道 + 四个 `ha_*` 控制工具）
   - `HASS_TOKEN` / `HASS_URL` 配置与 `curl` 验证命令
   - 四工具表格（`ha_list_entities` / `ha_get_state` / `ha_list_services` / `ha_call_service`）+ 调用示例
   - 事件转发默认全关 + `watch_domains` / `watch_entities` / `ignore_entities` / `cooldown_seconds` 的 `config.yaml` 示例
   - 出站 persistent notification（标题 "Hermes Agent"）
   - 安全边界（`shell_command` 等拦截域、entity_id 正则校验）与连接管理（30s 心跳、指数退避重连、独立 REST 会话）
   - 大白话 tip（智能家居总钥匙卡）
3. **本章小结**追加 2 条：HA 双通道接入要点、HA 安全边界与连接管理。

## 来源

- S20：`https://raw.githubusercontent.com/NousResearch/hermes-agent/refs/heads/main/website/docs/user-guide/messaging/homeassistant.md`（官方文档）
- 已与官方文档逐条核对：Token 生成路径、环境变量默认值、工具签名、拦截域列表、重连退避参数。

## 未处理风险

- S20 仅在本篇内联标注，未回写 `workspace/hermes-agent/02_deep_research.md` 来源表（避免改动工作流研究产物）。
- 未改动 Obsidian 双链 / 标签；Hermes Agent MOC 只索引分册 README，无需更新。
- HA 各版本字段可能微调；以官方文档为准。

---

## 第二轮更新：常用平台接入教程

> 触发：用户选中「20+ 平台」文本，要求补充常用平台接入教程 · 2026-08-28 · 模式：patch-in-place

### 变更摘要

1. **6.1 新增子节「常用平台接入教程」**（位于「常驻与自愈边界」与「Home Assistant」之间）：
   - 顶部 7 行选型对比表（上手难度 / 是否要公网 / 典型用途）。
   - 9 个平台的最小 `.env` 变量集 + 最常踩的坑：
     - Telegram（@BotFather token、隐私模式坑）
     - Discord（Message Content Intent / Server Members Intent 坑、邀请 URL）
     - Slack（`hermes slack manifest`、Socket Mode `xapp-` token、事件订阅坑）
     - WhatsApp Cloud（`hermes whatsapp-cloud` 向导、Phone Number ID 头号填错点、cloudflared 公网回调、仅私聊）
     - Signal（signal-cli link + daemon、群策略）
     - Email（应用专用密码、Gmail/Outlook host）
     - 钉钉（Stream 模式免公网、扫码自动写凭据）
     - 飞书（WebSocket 模式、权限 scope 与事件订阅）
     - 企业微信（扫码自动建 bot、群策略）
   - 大白话 tip（各聊天软件"工牌"比喻）。
2. **本章小结**追加 1 条：常用平台接入路径速记。

### 新增来源

- S21：各平台接入文档 `/docs/user-guide/messaging/{telegram,discord,slack,whatsapp-cloud,signal,email,dingtalk,feishu,wecom}`（官方文档，同一目录树）。

### 未处理风险

- 每个平台只收录"最小变量集 + 高频坑"，未展开进阶选项（语音、流式、per-channel 配置等）；需要时可再逐平台深潜。
- 平台页字段可能随版本漂移；以官方文档为准。
- 章节 6.1 已较长（约 200 行）；若后续继续扩平台，建议把平台接入拆成独立笔记「06A-平台接入速查」，本笔记保留教程核心。

---

## 第三轮更新：个人微信（Weixin）接入

> 触发：用户问「微信如何接入」· 2026-08-28 · 模式：patch-in-place

### 变更摘要

1. **选型对比表**追加 1 行：微信（个人，iLink Bot）｜中｜否（长轮询）｜个人微信消息。
2. **「常用平台接入教程」新增「微信（Weixin，个人号）」块**（位于企业微信之后）：
   - 明确区分：个人微信走腾讯 **iLink Bot API**（扫码生成 iLink bot 身份），**无 AppID/AppSecret**；企业微信是另一套（WeCom AI Bot）。
   - 接入：`hermes gateway setup` 选 Weixin → 终端二维码 → 微信 App 扫码 → 凭据自动存盘 `~/.hermes/weixin/accounts/`。
   - 最小变量：`WEIXIN_ACCOUNT_ID`、`WEIXIN_DM_POLICY`、`WEIXIN_ALLOWED_USERS`。
   - 三个坑：iLink bot 拉不进普通微信群（群功能大概率不可用）、@个人微信 ≠ @ iLink bot、token 单实例锁 + session 过期（`errcode=-14`）需重跑 setup。
3. **平台数**由 9 → 10。
4. **本章小结**常用平台速记追加：个人微信走 iLink Bot 扫码（群聊大概率不可用）。

### 来源

- S21（`/docs/user-guide/messaging/weixin`）— 与既有平台教程共用同一来源编号。
