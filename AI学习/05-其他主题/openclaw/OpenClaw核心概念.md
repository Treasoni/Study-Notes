---
tags: [openclaw, gateway, 架构, 概念]
created: 2026-03-04
updated: 2026-03-04
---

# OpenClaw 核心概念

> [!info] 概述
> **OpenClaw 是一个自托管的 AI 网关，它像"翻译官+调度中心"一样，连接你的聊天应用和 AI 智能体**。你只需运行一个 Gateway 进程，就能从任何地方通过 WhatsApp、Telegram、Discord 等与 AI 对话。

## 核心概念

### 是什么

OpenClaw 是一个 **开源 AI 网关和编排框架**：

```
┌─────────────────────────────────────────────────────────────┐
│                      OpenClaw 是什么                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  自托管（Self-hosted）                                       │
│  ├─ 运行在你自己的硬件上                                     │
│  └─ 数据完全由你控制                                         │
│                                                             │
│  多渠道（Multi-channel）                                     │
│  ├─ 一个 Gateway 同时服务 WhatsApp、Telegram、Discord...    │
│  └─ 统一的消息入口                                           │
│                                                             │
│  Agent 原生（Agent-native）                                  │
│  ├─ 专为 AI Agent 设计                                       │
│  ├─ 支持工具调用、会话、记忆、多 Agent 路由                   │
│  └─ 内置 3000+ 官方 Skills                                   │
│                                                             │
│  开源（Open source）                                         │
│  └─ MIT 许可证，社区驱动                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!quote] 官方定义
> "OpenClaw is a **self-hosted gateway** that connects your favorite chat apps — WhatsApp, Telegram, Discord, iMessage, and more — to AI coding agents like Pi."
> — [OpenClaw 官方文档](https://docs.openclaw.ai)

### 为什么需要

| 问题 | OpenClaw 的解决方案 |
|------|---------------------|
| 想在任何聊天应用中使用 AI | 统一网关，一次配置多平台可用 |
| 不想依赖云服务 | 自托管，数据在本地 |
| 需要 AI 执行工具/操作 | Skills 系统，3000+ 预置工具 |
| 多设备访问 | Gateway 作为中心，各设备作为节点连接 |

### 通俗理解

**🎯 比喻 1：万能翻译官**

```
你（在微信）     翻译官（OpenClaw）     AI 大脑（Claude/GPT）
    │                  │                      │
    │  "帮我写代码"    │                      │
    │ ───────────────> │                      │
    │                  │  转换为标准格式        │
    │                  │ ───────────────────> │
    │                  │                      │  思考...
    │                  │ <─────────────────── │
    │                  │  返回结果             │
    │ <─────────────── │                      │
    │  "代码写好了"    │                      │
```

**🎯 比喻 2：餐厅点餐系统**

```
┌────────────┐     ┌────────────┐     ┌────────────┐
│  顾客 A    │     │  顾客 B    │     │  顾客 C    │
│ (微信点餐)  │     │ (电话点餐)  │     │ (APP点餐)  │
└─────┬──────┘     └─────┬──────┘     └─────┬──────┘
      │                  │                  │
      └──────────────────┼──────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     服务员           │
              │   (OpenClaw 网关)    │
              │                     │
              │  - 接收所有订单      │
              │  - 统一格式          │
              │  - 分发给对应厨房    │
              └──────────┬──────────┘
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
┌──────────┐      ┌──────────┐      ┌──────────┐
│ 中式厨房  │      │ 西式厨房  │      │ 日式厨房  │
│ (Claude) │      │  (GPT)   │      │ (DeepSeek)│
└──────────┘      └──────────┘      └──────────┘
```

---

## 网关（Gateway）是什么

### 定义

**Gateway 是 OpenClaw 的核心枢纽**，是一个 Node.js 服务，运行在你的机器上，作为所有消息的"单一真理来源"。

> [!quote] 官方定义
> "The Gateway is the single source of truth for sessions, routing, and channel connections."
> — [OpenClaw 官方文档](https://docs.openclaw.ai)

### Gateway 的角色

```
┌─────────────────────────────────────────────────────────────┐
│                    Gateway 的三大职责                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ 会话管理（Sessions）                                    │
│     ├─ 每个用户有独立会话                                    │
│     ├─ 记住对话历史                                          │
│     └─ 管理会话状态                                          │
│                                                             │
│  2️⃣ 路由（Routing）                                         │
│     ├─ 消息从哪来 → Telegram/WhatsApp/Discord               │
│     ├─ 消息到哪去 → 哪个 AI Agent                           │
│     └─ 工具调用 → 哪个 Skill 处理                            │
│                                                             │
│  3️⃣ 通道连接（Channel Connections）                         │
│     ├─ 维护与各聊天平台的连接                                │
│     ├─ WhatsApp Web、Telegram Bot、Discord Bot...           │
│     └─ 处理认证、心跳、重连                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Gateway 技术细节

| 组件 | 说明 |
|------|------|
| **WebSocket 服务器** | 默认端口 `18789`，所有通信通过 WebSocket |
| **HTTP 服务器** | 提供 Control UI、Canvas、A2UI 界面 |
| **Token 认证** | 通过 `OPENCLAW_GATEWAY_TOKEN` 环境变量配置 |
| **配置文件** | `~/.openclaw/openclaw.json` |

**启动 Gateway**：

```bash
# 基本启动
openclaw gateway

# 指定端口
openclaw gateway --port 18789

# 详细日志
openclaw gateway --verbose
```

---

## 工作原理

### Hub-and-Spoke 架构

OpenClaw 采用 **Hub-and-Spoke（轮毂-辐条）** 架构：

```
                    ┌─────────────────────┐
                    │     Gateway         │
                    │     (Hub)           │
                    │                     │
                    │  - 会话管理          │
                    │  - 消息路由          │
                    │  - 状态存储          │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌────────────┐      ┌────────────┐      ┌────────────┐
    │   Spoke 1  │      │   Spoke 2  │      │   Spoke 3  │
    │  WhatsApp  │      │  Telegram  │      │  Discord   │
    │  (输入源)   │      │  (输入源)   │      │  (输入源)   │
    └────────────┘      └────────────┘      └────────────┘
```

### 消息流转过程

以 Telegram 消息为例：

```
┌─────────────────────────────────────────────────────────────┐
│                    消息流转完整过程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ 用户发送消息                                            │
│     └─ Telegram: "帮我分析这段代码"                          │
│                                                             │
│  2️⃣ Gateway 接收                                            │
│     ├─ 识别来源：Telegram 用户 @user123                      │
│     ├─ 查找/创建会话                                         │
│     └─ 加载历史上下文                                        │
│                                                             │
│  3️⃣ 调用 AI Agent                                           │
│     ├─ 选择模型（Claude/GPT/DeepSeek）                       │
│     ├─ 组装 Prompt（历史 + 用户消息 + 系统提示）              │
│     └─ 发送到 LLM API                                        │
│                                                             │
│  4️⃣ Agent 思考 & 工具调用（可选）                            │
│     ├─ Agent 决定需要调用工具                                │
│     ├─ 如：读取文件、执行代码                                │
│     └─ 执行工具，获取结果                                    │
│                                                             │
│  5️⃣ 生成响应                                                 │
│     ├─ 整合所有信息                                          │
│     └─ 生成最终回复                                          │
│                                                             │
│  6️⃣ 返回用户                                                 │
│     ├─ Gateway 路由回 Telegram                               │
│     └─ 用户收到回复                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 四层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw 四层架构                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  第 1 层：用户交互层                                         │
│  ├─ Web 控制台 (http://127.0.0.1:18789)                     │
│  ├─ CLI 命令行                                              │
│  └─ IM 通道 (Telegram/Discord/WhatsApp)                     │
│                                                             │
│  第 2 层：Gateway 层（核心）                                  │
│  ├─ WebSocket 服务器                                        │
│  ├─ 消息路由                                                │
│  ├─ 会话隔离                                                │
│  └─ 授权验证                                                │
│                                                             │
│  第 3 层：AI 执行层                                          │
│  ├─ Agent 运行时                                            │
│  ├─ LLM 调用 (Claude/GPT/DeepSeek)                         │
│  ├─ 记忆 & 上下文管理                                        │
│  └─ 多 Agent 路由                                           │
│                                                             │
│  第 4 层：Skills 扩展层                                      │
│  ├─ 文件操作                                                │
│  ├─ 浏览器自动化                                            │
│  ├─ 系统命令                                                │
│  └─ 自定义工具                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> [!info] 来源
> - [OpenClaw 官方文档](https://docs.openclaw.ai) - 架构概述
> - [OpenClaw Gateway Remote](https://docs.openclaw.ai/gateway/remote) - 远程访问架构

---

## Gateway vs Node

### 概念区分

| 概念 | 角色 | 运行位置 |
|------|------|----------|
| **Gateway** | 主节点，"大脑"所在地 | 服务器/主机 |
| **Node** | 从节点，外设 | iOS/Android/macOS App |

```
┌─────────────────────────────────────────────────────────────┐
│                    Gateway vs Node                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Gateway（主机）                                             │
│  ├─ 拥有会话、认证、通道、状态                               │
│  ├─ 运行 Agent                                              │
│  └─ 只能有一个 Gateway 在运行                                │
│                                                             │
│  Node（外设）                                                │
│  ├─ 连接到 Gateway WebSocket                                │
│  ├─ 可以有多个 Node 同时连接                                 │
│  └─ 不运行 Agent，只是输入/输出终端                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 命令流示例

```
Telegram 消息 → Gateway → Node 工具调用：

1. Telegram 消息到达 Gateway
2. Gateway 运行 Agent，决定调用 Node 工具
3. Gateway 通过 WebSocket 调用 Node (node.* RPC)
4. Node 执行工具，返回结果
5. Gateway 回复到 Telegram
```

> [!quote] 官方说明
> "Nodes do not run the gateway service. Only one gateway should run per host."
> — [OpenClaw Remote 文档](https://docs.openclaw.ai/gateway/remote)

---

## 与其他概念的关系

| 概念 | 关系 | 说明 |
|------|------|------|
| [[AI学习/05-其他主题/openclaw/OpenClaw安装教程]] | 安装部署 | 如何安装 OpenClaw |
| [[AI学习/05-其他主题/openclaw/OpenClaw安装后配置指南]] | 配置使用 | 安装后的配置方法 |
| [[AI学习/05-其他主题/openclaw/OpenClaw Web控制台局域网访问配置]] | 网络配置 | 如何让局域网设备访问 |
| [[AI学习/05-其他主题/openclaw/OpenClaw对接第三方软件指南]] | 扩展集成 | Skills 和第三方集成 |

---

## 最佳实践

### 部署建议

| 场景 | 推荐配置 |
|------|----------|
| **个人使用** | 笔记本运行 Gateway，本机访问 |
| **多设备** | 服务器运行 Gateway，各设备作为 Node 连接 |
| **家庭/团队** | VPS 运行 Gateway，Tailscale 内网穿透 |

### 安全原则

> [!quote] 官方安全建议
> "**Keep the Gateway loopback-only** unless you're sure you need a bind."
> — [OpenClaw Security](https://docs.openclaw.ai/gateway/remote)

1. **默认只绑定 loopback**（127.0.0.1）
2. 需要远程访问时使用 SSH 隧道或 Tailscale
3. 必须暴露时设置 Token/Password 认证
4. 生产环境配置 `allowedOrigins`

---

## 常见问题

### Q1：Gateway 和 Agent 是什么关系？

**Gateway 是"调度中心"，Agent 是"AI 大脑"**：
- Gateway 负责：消息路由、会话管理、通道连接
- Agent 负责：AI 推理、工具调用、生成响应

```
用户 → Gateway（调度）→ Agent（思考）→ Gateway → 用户
```

### Q2：为什么叫"Gateway"（网关）？

网关（Gateway）在网络中是"连接不同网络的入口点"。OpenClaw 之所以叫网关：

1. **连接不同世界**：聊天应用 ↔ AI 模型
2. **统一入口**：所有消息都经过这一个入口
3. **协议转换**：不同聊天协议 → 统一的 AI 请求格式

### Q3：可以运行多个 Gateway 吗？

**同一台主机上只能运行一个 Gateway**。但可以：
- 在不同主机运行多个 Gateway（隔离配置）
- 多个 Node 连接到同一个 Gateway

### Q4：Gateway 必须一直运行吗？

**是的，如果需要随时响应消息**：
- 服务器/VPS：推荐后台运行（`openclaw gateway --daemon`）
- 笔记本：按需启动，或使用 macOS App 的后台模式

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **Gateway 是核心**：所有功能都围绕 Gateway 展开，它是"单一真理来源"
>
> 2. **Hub-and-Spoke 架构很优雅**：
>    - 新增聊天平台只需添加新的 Spoke
>    - 不影响核心 Gateway 逻辑
>
> 3. **安全设计很严格**：
>    - 默认只绑定 loopback
>    - 需要远程访问必须配置认证
>    - 设备配对机制防止未授权访问
>
> 4. **学习建议**：
>    - 先在本地跑起来，理解基本流程
>    - 再尝试多设备连接
>    - 最后研究 Skills 扩展

---

## 相关文档

- [[OpenClaw MOC]] - OpenClaw 文档索引
- [[OpenClaw安装教程]] - 安装指南
- [[OpenClaw安装后配置指南]] - 配置指南

- [[AI学习/05-其他主题/openclaw/OpenClaw安装教程]] - 安装部署指南
- [[AI学习/05-其他主题/openclaw/OpenClaw Web控制台局域网访问配置]] - 网络配置
- [[AI学习/05-其他主题/openclaw/OpenClaw对接第三方软件指南]] - Skills 集成

---

## 参考资料

### 官方资源

- [OpenClaw 官方文档](https://docs.openclaw.ai) - 完整技术文档
- [OpenClaw Gateway Remote](https://docs.openclaw.ai/gateway/remote) - 远程访问架构
- [OpenClaw Web 文档](https://docs.openclaw.ai/web) - Web 界面配置
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 源代码

### 社区资源

- [OpenClaw 中文社区](https://www.moltcn.com) - 中文用户社区
- [OpenClaw Discord](https://discord.gg/openclaw) - 官方 Discord

---

**最后更新**：2026-03-04
