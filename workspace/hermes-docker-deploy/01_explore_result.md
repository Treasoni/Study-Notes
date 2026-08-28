# 01 探测结果 - Hermes Docker 部署 + 国内消息平台接入

> 项目：hermes-docker-deploy | 阶段：P1 探测式收集
> 生成时间：2026-08-28

## 核心结论

**Hermes Agent 已官方原生支持全部目标国内平台**，无需 wechaty / OneBot 等第三方桥。Docker 部署 + 各平台接入都可走官方镜像 `nousresearch/hermes-agent` 完成。

| 平台 | 原生支持 | 接入方式 | 免公网 | 最小版本 | 主要限制 |
|------|---------|---------|--------|---------|---------|
| 微信 Weixin | ✅ | iLink Bot API + 扫码登录 + 长轮询 | ✅ | v0.9.0 | 群消息基本不可用，仅私聊稳定 |
| 企业微信 WeCom | ✅ | 自建应用回调 / AI Bot WebSocket | ✅ | v0.6.0 | — |
| 飞书 Feishu/Lark | ✅ | WebSocket（默认）/ webhook 兜底 | ✅（WS） | v0.6.0 | WS 仅限企业自建应用 |
| QQ | ✅ | QQ Bot API v2：WebSocket 收 + REST 发 | ✅ | 2026-04 后 | 需开放平台审核 + 事件订阅权限 |

## 候选源记录（已去重，按 canonical URL）

### 通用：Docker 部署（跨平台复用）

| # | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
|---|------|-----|------|--------|------|-----|
| D1 | Docker · Hermes Agent 官方文档（中文） | https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/docker | official | 官方镜像、/opt/data 数据卷、gateway run、8642 暴露 API | 2026-03 | 5 |
| D2 | RELEASE_v0.6.0.md | https://github.com/NousResearch/hermes-agent/blob/main/RELEASE_v0.6.0.md | official | 确认 v0.6.0 新增飞书/Lark + 企微网关适配器 | 2026-03-30 | 4 |

### 微信 Weixin / 企业微信 WeCom

| # | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
|---|------|-----|------|--------|------|-----|
| W1 | Weixin (WeChat) 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/weixin | official | iLink Bot API、扫码登录、长轮询免公网、群消息不可用 | 2026-04 | 5 |
| W2 | PR #7166: native Weixin support via iLink Bot API | https://github.com/NousResearch/hermes-agent/pull/7166 | official | v0.9.0 合并原生微信适配器，能力与限制清单 | 2026-04-10 | 5 |
| W3 | WeCom（企业微信）官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/wecom | official | 自建应用回调 / AI Bot WebSocket 两模式，免公网 | 2026-03 | 4 |
| W4 | 服务器部署 Hermes（二）：微信 Gateway + Docker Compose | https://blog.csdn.net/WeLoveCn/article/details/161239172 | report | Docker Compose 跑微信网关实操，扫码登录与权限坑 | 2026 | 4 |
| W5 | 接入微信个人号：wechat-bridge 桥接 | https://cloud.tencent.com.cn/developer/article/2655902 | community | 社区桥方案，封号风险高，已被原生 iLink 取代 | 2026 | 3 |

### 飞书 Feishu / Lark

| # | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
|---|------|-----|------|--------|------|-----|
| F1 | Feishu / Lark 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/feishu | official | WebSocket(默认)/webhook 两模式，仅需 APP_ID/APP_SECRET | 2026-03 | 5 |
| F2 | 云上 Hermes Agent 快速接入飞书指南 | https://developer.cloud.tencent.cn/article/2660600 | report | 云服务器实操，建应用与事件订阅配置 | 2026 | 3 |
| F3 | OpenClaw 飞书 Webhook 内网穿透 | https://open-claw.online/zh/docs/feishu-webhook-tunnel | community | webhook 兜底隧道方案（CF Tunnel/natapp/cpolar） | 2026 | 2 |

### QQ

| # | 标题 | URL | 层级 | 相关性 | 日期 | 分 |
|---|------|-----|------|--------|------|-----|
| Q1 | QQ Bot 官方文档 | https://hermes-agent.nousresearch.com/docs/user-guide/messaging/qqbot | official | WebSocket 收 + REST 发，需 AppID/AppSecret | 2026 | 5 |
| Q2 | 腾讯 QQ 原生接入 Hermes Agent（IT之家） | https://www.ithome.com/0/939/789.htm | report | 官方合作新闻 | 2026-04 | 4 |
| Q3 | GitHub Issue #9166: hermes-qqbot 社区适配器 | https://github.com/NousResearch/hermes-agent/issues/9166 | community | 已关闭未合并，被官方实现取代 | 2026-04-13 | 3 |
| Q4 | NapCat + NoneBot2 把 Hermes 放进 QQ 群 | https://nbility.ai/blog/hermes-agent-qq-group | community | 个人号路线，多一层桥，有风控风险 | 2026-05-25 | 4 |

## 覆盖缺口

- [ ] **微信个人号 iLink** 的具体消息类型限制（官方称仅 5 种）与私聊稳定性实测——P2 需从 W1/W2 深挖
- [ ] **QQ 官方 Bot** 的开放平台审核流程 + 沙箱模式说明——P2 从 Q1 深挖
- [ ] **三个平台并存**时 Docker 数据卷 / gateway 多 profile 的资源占用与端口规划——需综合 D1 + 各平台文档
- [ ] 各平台密钥管理（`~/.hermes/.env`）与安全基线——沿用上手实战第 8 章已有内容，仅补差异

## P2 范围预估

- **核心源**（精读）：D1、W1、W2、F1、Q1（全部官方，共 5 篇）
- **补充源**（按需）：W3（企微）、Q4（非官方路线对比）、W4（实操经验）
- **产出物**：`02_deep_research.md`，含 scope、源表、claim/source map、每平台接入步骤草稿、矛盾与开放问题
- **预估篇幅**：9-11 章（Docker 部署基础 2 章 + 微信/企微 2-3 章 + 飞书 2-3 章 + QQ 2-3 章 + 运维安全 1 章）

## 方向菜单（请用户选择）

- **A. 三平台全收（推荐）**：Docker 部署基础 + 微信/企业微信 + 飞书 + QQ 全写，覆盖最全，篇幅最大
- **B. 三平台全收 + 非官方路线对比**：在 A 基础上补 NapCat/wechaty 等非官方方案的风险对比章节
- **C. 精简单平台**：只写 Docker 部署 + 你最常用的一个平台，篇幅最小、最快产出
- **D. 聚焦部署基础**：以 Docker 部署/运维为主，平台只附接入配置速查表
