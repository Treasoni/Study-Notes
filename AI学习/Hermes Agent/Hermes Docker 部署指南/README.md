---
title: "Hermes Docker 部署指南"
tags:
  - AI学习
  - Agent
  - Hermes
  - Docker
created: 2026-08-28
updated: 2026-08-28
status: 完成
source_project: hermes-docker-deploy
moc: "[[Hermes Agent MOC]]"
---

# Hermes Docker 部署指南

> **定位**：用 Docker 部署 Hermes Agent，并配置国内消息平台接入（微信 / 企业微信 / 飞书 / QQ）。
> **前置**：已读《Hermes Agent 上手实战》《Hermes Tool 配置指南》两册，了解 Hermes 基本概念。

## 本册解决什么问题

把 Hermes 从「本机跑跑」变成「**常驻在 Docker 里的 7×24 消息机器人**」，并连上三个国内消息平台：

1. **Docker 部署基础**：官方镜像、数据卷持久化、首次 setup、gateway 常驻、docker-compose 编排、权限模型、升级排错（第 1~2 章）
2. **国内平台接入**：微信个人号 iLink、企业微信 AI Bot、飞书 WebSocket、QQ 官方 Bot（第 3~8 章）
3. **部署后运维**：多平台日志、升级回滚、安全基线（第 9~10 章）

[!tip] 大白话
把本册想象成给 Hermes「**买一台专属服务器并接上三条电话线**」：第 1~2 章把服务器装好并让它 24 小时开机；第 3~8 章分别接上微信、企微、飞书、QQ 四部电话；第 9~10 章教你日常维护和上锁。每一章都独立可照抄，产物（命令 / .env / compose 文件）先睹为快再逐段拆讲。

## 目录

| # | 章节 | 一句话 | 标签 |
|---|------|--------|------|
| 01 | [[01-镜像数据卷与首次setup\|镜像、数据卷与首次 setup]] | 官方镜像 + `~/.hermes` 数据卷 + setup 向导 | 基础 |
| 02 | [[02-Gateway常驻与Compose编排\|Gateway 常驻与 Compose 编排]] | `docker run` 常驻 + 完整 `docker-compose.yaml` + 权限模型 | 基础 |
| 03 | [[03-微信个人号iLink接入\|微信个人号接入：iLink 扫码直连]] | 个人号扫码直连、长轮询免公网、私聊为主 | 微信 |
| 04 | [[04-企业微信AI Bot与回调\|企业微信接入：AI Bot 与自建应用回调]] | AI Bot WebSocket（推荐）/ 自建应用回调，出站限制 | 企微 |
| 05 | [[05-飞书建应用与WebSocket\|飞书接入（上）：建应用与 WebSocket 长连接]] | 扫码/手动建应用 + 默认 WebSocket 免公网 | 飞书 |
| 06 | [[06-飞书事件订阅与消息收发\|飞书接入（下）：事件订阅、权限与消息收发]] | 事件订阅、权限 scope、消息收发能力 | 飞书 |
| 07 | [[07-QQ官方Bot基础接入\|QQ 接入（上）：官方 QQ Bot 基础接入]] | q.qq.com 建机器人、intents、沙箱到发布 | QQ |
| 08 | [[08-QQ进阶配置与NapCat替代\|QQ 接入（下）：进阶配置、语音转写与 NapCat 替代]] | `qqbot.extra` 进阶、双阶段语音转写、断连坑、NapCat 替代 | QQ |
| 09 | [[09-多平台运维与日志\|多平台运维：日志、升级与日常管理]] | 日志四来源、升级回滚、多平台并存红线 | 运维 |
| 10 | [[10-安全基线\|安全基线：密钥、API Server 与公网暴露]] | API Server 三件套、密钥落盘泄露面、fail-closed | 安全 |

## 阅读建议

- **只想尽快跑通一个平台**：读完第 1~2 章（部署基础），跳到对应平台的章节（微信→03、企微→04、飞书→05+06、QQ→07+08）。
- **要长期生产使用**：全册读完，第 9~10 章的日志定位与安全基线不能省。
- **追求免公网**：微信 iLink（长轮询）、企微 AI Bot（WS）、飞书（WS）、QQ（WS 收+REST 发）**全部免公网**，无需内网穿透。

## 关键技术结论

- 官方镜像：`nousresearch/hermes-agent`，tag 用 `:latest` 或日期式 tag（如 `v2026.8.27`），无 `RELEASE_v0.6.0.md`。
- 数据卷：容器内 `/opt/data` ↔ 宿主机 `~/.hermes/`，是唯一状态源。
- 三个国内平台均为 Hermes **官方原生支持**，无需 wechaty / OneBot 等桥。
- 免公网是常态：长轮询或 WebSocket 出站连接即可。

## 需实测项

写作时基于官方文档与社区实操，以下点标注为「需实测」，请以实际版本为准：

- 健康端点的具体 HTTP 路径
- 官方镜像 tag pin 策略（`:latest` vs 日期 tag）
- QQ 文件发送根因、`markdown_support` 生效条件、TTS 401
- gateway setup 各平台选项数字（社区记录，以菜单为准）
- 微信 iLink 群消息是否真完全不可用、多账号边界

## 相关分册

- [[Hermes Agent MOC|Hermes Agent MOC]]
- [[Hermes Agent 上手实战/README|Hermes Agent 上手实战]]
- [[Hermes Tool 配置指南/README|Hermes Tool 配置指南]]
