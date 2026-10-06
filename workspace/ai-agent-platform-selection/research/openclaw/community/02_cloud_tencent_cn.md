---
url: "https://cloud.tencent.cn/developer/article/2674122"
title: "三个 Agent Harness 框架对比：OpenClaw、Hermes Agent、OpenHuman 到底差在哪？-腾讯云开发者社区-腾讯云"
scraped_at: 2026-09-29T14:44:38+00:00
---

## 三个 Agent Harness 框架对比：OpenClaw、Hermes Agent、OpenHuman 到底差在哪？
[首页](https://cloud.tencent.cn/developer)
学习
活动
专区
圈层
工具
[MCP广场](https://cloud.tencent.cn/developer/mcp)
文章/答案/技术大牛搜索
[社区首页](https://cloud.tencent.cn/developer)[专栏](https://cloud.tencent.cn/developer/column)三个 Agent Harness 框架对比：OpenClaw、Hermes Agent、OpenHuman 到底差在哪？
# 三个 Agent Harness 框架对比：OpenClaw、Hermes Agent、OpenHuman 到底差在哪？
山行AI
发布于 2026-05-26 16:59:24
发布于 2026-05-26 16:59:24
## 前言
三类 Agent Harness 的不同重心
Agent 框架越来越多，但很多项目表面都在说“让 AI 调工具、执行任务、拥有记忆”，真正落到架构上，差异其实非常大。
这次选三个方向明显不同的项目放在一起看：
**•** openclaw/openclaw[1]
**•** NousResearch/hermes-agent[2]
**•** tinyhumansai/openhuman[3]
它们都可以被理解为某种 AI Agent harness，但重点完全不同：
**•OpenClaw** 解决的是入口与控制平面问题：怎么让 Agent 常驻在用户已有设备和聊天渠道里。
**•Hermes Agent** 解决的是自我演化运行时问题：怎么让 Agent 从经验中沉淀 skills、记住用户、跨环境执行。
**•OpenHuman** 解决的是个人上下文和产品体验问题：怎么让 Agent 快速接入个人数据，并通过桌面 UI 变得可用。
一句话概括：  
| 核心定位  | 架构关键词  |  
| --- | --- |  
| OpenClaw  | 跑在自己设备上的个人 AI 助理，通过各种聊天/设备入口驱动任务  | Local-first Gateway、Channels、Nodes、Skills、Plugins  |  
| Hermes Agent  | 会积累记忆、生成/改进 skills、跨平台运行的自改进 Agent  | AIAgent Loop、Tool Registry、SQLite/FTS5、Skills Learning、Gateway  |  
| OpenHuman  | UI 优先、连接个人账号数据并构建长期记忆树的桌面 AI 助理  | Tauri/Rust Core、Memory Tree、OAuth Integrations、MCP/Socket.io  |  
### OpenClaw：本地优先的个人助理网关
OpenClaw 架构重点
OpenClaw 的核心不是“做一个聊天机器人”，而是做一个**本地优先的个人 AI 控制平面** 。
它的 README 里明确强调：OpenClaw 是运行在用户自己设备上的 personal AI assistant。用户可以从 WhatsApp、Telegram、Slack、Discord、Signal、iMessage、WeChat、QQ 等渠道和它交互。
也就是说，它不是只解决“模型如何调用工具”，而是在解决一个更贴近日常的问题：
> _AI 助理应该住在哪里？用户应该从哪里唤起它？它如何连接桌面、手机、聊天软件和工具？_
#### 架构模式：Gateway-centric
OpenClaw 的架构非常典型：以 Gateway 为中心。
Gateway 是长期运行的控制平面，负责：
**•** 消息渠道接入
**•** 会话管理
**•** 工具执行
**•** 事件分发
**•** 节点连接
**•** 权限与路由
CLI、macOS App、Web UI、自动化任务可以通过 WebSocket 连接到 Gateway。macOS、iOS、Android、headless nodes 也可以接入，并声明自己的能力，例如 canvas、camera、screen、location 等。
Agent loop 大致经过：
**1** intake：接收用户输入
**2** context assembly：组装上下文
**3** model inference：模型推理
**4** tool execution：工具执行
**5** streaming：流式返回
**6** persistence：持久化记录
每个 session 会串行执行，避免工具调用和 transcript 写入互相打架。
#### 扩展方式
OpenClaw 的扩展主要来自两层：
**•Skills** ：采用 AgentSkills 兼容目录，支持 workspace、project、personal、managed、bundled 等多级优先级。
**•Plugins** ：用于 provider、channel、tool lifecycle hook 等更底层的扩展。
所以 OpenClaw 更像一个“AI 助理操作系统入口层”。它的价值不只是模型能力，而是把用户已有入口整合起来。
#### 适合什么场景？
OpenClaw 适合：
**•** 希望 AI 助理常驻在本机或个人服务器上
**•** 需要从多个聊天渠道发任务、收结果
**•** 需要连接桌面、手机节点、Canvas、语音等本地能力
**•** 愿意自己管理模型、配置、权限和安全边界
如果目标是“让 AI 助理住进用户已有设备和聊天入口”，OpenClaw 是三个项目里最贴近这个方向的。
### Hermes Agent：会自我改进的 Agent 运行时
Hermes Agent 架构重点
Hermes Agent 的关键词是 **self-improving** 。
它更像一个通用 Agent runtime：既能运行任务，也能积累记忆、生成 skills、改进 skills、搜索历史会话，并跨 session 建立对用户的长期理解。
和 OpenClaw 相比，它不那么强调“入口住在哪里”，而更强调：
> _Agent 如何从一次次执行中学到东西，并把经验沉淀为可复用能力？_
#### 架构模式：Agent-loop-centric runtime
Hermes 的中心是 `AIAgent`。
它负责：
**•** prompt builder
**•** provider resolution
**•** tool dispatch
**•** memory injection
**•** skill invocation
**•** session persistence
Hermes 支持多种入口：
**•** CLI
**•** Gateway
**•** ACP
**•** Batch Runner
**•** API Server
**•** Python Library
Provider 层支持多种 API 模式，例如 chat completions、Codex responses、Anthropic messages。
工具系统也很重：Tool Registry 集中注册 70+ tools 和约 28 个 toolsets。终端 backend 支持 local、Docker、SSH、Singularity、Modal、Daytona、Vercel Sandbox 等执行环境。
#### 记忆与自我改进
Hermes 的记忆机制很突出。
它使用 SQLite + FTS5 做 session storage 和历史检索，同时用 `MEMORY.md`、`USER.md` 这类 curated memory 注入 system prompt。
更关键的是，它强调 skills learning：
**•** 从经验中创建 skill
**•** 在使用中改进 skill
**•** 用历史会话检索辅助当前任务
**•** 通过 cron 和 gateway 让任务长期运行
这让 Hermes 的定位更接近“会成长的 Agent harness”。
#### 适合什么场景？
Hermes Agent 适合：
**•** 需要长期自我改进的个人或团队 Agent
**•** 希望复杂流程沉淀成 skills
**•** 需要在云 VM、Docker、SSH、serverless sandbox 等环境运行
**•** 重视 provider/model 灵活切换和工具运行环境可移植性
**•** 想用一个 Python runtime 管理工具、记忆、子代理、cron 和 gateway
如果目标是“让 Agent 从经验里变强”，Hermes 是三个项目里最强调这个方向的。
### OpenHuman：个人数据驱动的桌面 AI 助理
OpenHuman 架构重点
OpenHuman 的方向更产品化，也更 UI-first。
它强调的是：通过账号集成和自动拉取，让 AI 助理尽快理解用户的个人上下文。
这和前两个项目不太一样。OpenClaw 更像入口网关，Hermes 更像自我演化运行时，OpenHuman 则更像一个面向普通用户的桌面 AI 产品底座。
它想解决的问题是：
> _Agent 如何快速接入用户的真实工作数据，并把这些数据变成长期记忆？_
#### 架构模式：desktop-memory-first
OpenHuman 当前以桌面端为主。
架构上：
**•** 前端使用 React/Vite
**•** 桌面壳使用 Tauri
**•** 核心逻辑在 Rust `openhuman-core`
**•** WebView 负责 UI
**•** Rust core 负责 RPC、skills、memory、socket 等能力
**•** 前后端通过 Tauri IPC 和 HTTP JSON-RPC 通信
它的重点不是只做一个 agent loop，而是围绕个人数据构建一套同步、压缩、记忆和调用系统。
#### 集成与记忆
OpenHuman 提供大量第三方集成，例如 Gmail、Notion、GitHub、Slack、Stripe、Calendar、Drive、Linear、Jira 等，通过 OAuth 接入。
数据同步后，会进入 Memory Tree：
**•** 把不同来源的数据规范化为 Markdown chunks
**•** 存入 SQLite
**•** 写入 Obsidian-compatible vault
**•** 使用 TokenJuice 压缩工具结果、抓取内容、邮件正文等上下文
这意味着 OpenHuman 的核心竞争力不是“工具特别多”，而是“用户上下文来得快”。
#### 安全边界
OpenHuman 也很强调本地安全：
**•** 本地存储
**•** OS keychain
**•** AES-256-GCM
**•** Argon2id
**•** prompt injection guard
这对一个连接大量个人账号的桌面 AI 助理来说非常关键。
#### 适合什么场景？
OpenHuman 适合：
**•** 希望桌面 UI 开箱即用
**•** 希望连接 Gmail、Slack、Notion、Drive、Calendar 等个人工作数据
**•** 希望本地形成 Obsidian/Memory Tree 知识库
**•** 不想为每个能力单独配置 API key、插件和工具链
**•** 接受项目仍处于 early beta
如果目标是“让 Agent 先理解用户，再帮用户做事”，OpenHuman 的方向最直接。
### 横向对比  
| OpenClaw  | Hermes Agent  | OpenHuman  |  
| --- | --- | --- |  
| 本地常驻个人助理  | 自改进通用 Agent runtime  | UI-first 个人超级助理  |  
| 核心架构  | Gateway 控制平面  | AIAgent 统一执行环  | Tauri/Rust core + React UI  |  
| 多聊天渠道、CLI、App、Web、Nodes  | CLI、Messaging Gateway、ACP、API、Batch  | 桌面 UI、集成数据、消息渠道  |  
| 工具系统  | Gateway tools + plugins + skills  | 70+ tools、28 toolsets、MCP、terminal backends  | MCP tool catalog、skill bridge、native tools  |  
| Skills  | AgentSkills-compatible，多级优先级，ClawHub  | 自我创建/改进 skills，Skills Hub  | skill packages + managed Node runtime  |  
| session/workspace/context + skills；偏运行上下文  | MEMORY.md、USER.md、SQLite FTS5 session search  | Memory Tree、SQLite、Obsidian vault、auto-fetch  |  
| 集成取向  | 通讯渠道、设备节点、Canvas、语音、本地工具  | Provider、terminal、browser、messaging、cron、subagents  | OAuth SaaS 连接器、个人数据同步  |  
| 部署形态  | 本机/个人服务器 Gateway  | 本机、VPS、Docker、SSH、serverless sandbox  | 桌面 App 为主  |  
| 安全重点  | DM pairing、allowlist、sandbox、gateway auth  | command approval、DM pairing、container isolation、profile isolation  | 本地加密、OS keychain、prompt injection guard  |  
| AI 助理住在用户设备和聊天入口里  | Agent 持续学习并把流程沉淀成技能  | 快速接入个人数据并形成长期上下文  |  
### 怎么选？
如果目标是**让 AI 常驻在多个聊天渠道里，能控制本机、手机、Canvas、语音入口** ，优先看 OpenClaw。
如果目标是**构建一个能长期学习、搜索历史、生成技能、跨环境执行复杂任务的 Agent harness** ，优先看 Hermes Agent。
如果目标是**给普通用户一个桌面 AI 助理，快速连接个人账号、自动同步上下文、形成长期记忆库** ，优先看 OpenHuman。
更抽象一点：
**•** OpenClaw 解决的是**入口和控制平面** 问题。
**•** Hermes Agent 解决的是**Agent 自我演化和执行运行时** 问题。
**•** OpenHuman 解决的是**个人上下文获取和产品化体验** 问题。
这三个项目放在一起看，刚好对应 Agent 产品化的三条路径：
**1** 先把入口打通，让 Agent 能被随时唤起。
**2** 再把经验沉淀下来，让 Agent 越用越强。
**3** 最后把个人数据接进来，让 Agent 真正理解用户。
未来的 Agent 框架，很可能不会只走其中一条路。真正成熟的系统，最终会同时拥有入口、记忆、工具、数据和安全边界。但在当前阶段，先看清每个框架的重心，反而比追一个“大而全”的答案更重要。
参考来源：
**•** OpenClaw GitHub[4]
**•** Hermes Agent GitHub[5]
**•** OpenHuman GitHub[6]
声明：本文由山行整理自：OpenClaw[7]、Hermes Agent[8]、OpenHuman[9]，如果对您有帮助，请帮忙点赞、关注、收藏，谢谢～
**参考链接**
[1] openclaw/openclaw: https://github.com/openclaw/openclaw
[2] NousResearch/hermes-agent: https://github.com/NousResearch/hermes-agent
[3] tinyhumansai/openhuman: https://github.com/tinyhumansai/openhuman
[4] OpenClaw GitHub: https://github.com/openclaw/openclaw
[5] Hermes Agent GitHub: https://github.com/NousResearch/hermes-agent
[6] OpenHuman GitHub: https://github.com/tinyhumansai/openhuman
[7] OpenClaw: https://github.com/openclaw/openclaw
[8] Hermes Agent: https://github.com/NousResearch/hermes-agent
[9] OpenHuman: https://github.com/tinyhumansai/openhuman
本文参与 [腾讯云自媒体同步曝光计划](https://cloud.tencent.cn/developer/support-plan)，分享自微信公众号。
原始发表：2026-05-22，如有侵权请联系 cloudcommunity@tencent.com 删除
目录
  * 前言
    * OpenClaw：本地优先的个人助理网关
      * 架构模式：Gateway-centric
      * 适合什么场景？
    * Hermes Agent：会自我改进的 Agent 运行时
      * 架构模式：Agent-loop-centric runtime
      * 记忆与自我改进
      * 适合什么场景？
    * OpenHuman：个人数据驱动的桌面 AI 助理
      * 架构模式：desktop-memory-first
      * 集成与记忆
      * 适合什么场景？


相关产品与服务
云服务器
云服务器（Cloud Virtual Machine，CVM）提供安全可靠的弹性计算服务。 您可以实时扩展或缩减计算资源，适应变化的业务需求，并只需按实际使用的资源计费。使用 CVM 可以极大降低您的软硬件采购成本，简化 IT 运维工作。
[4核4G3M云服务器 新用户低至38元/年！](https://cloud.tencent.com/act/pro/featured-202607#MS?from=21344&from_column=21344)
  * ### 社区
  * ### 活动
  * ### 圈层
  * ### 关于


### 腾讯云开发者
扫码关注腾讯云开发者
领取腾讯云代金券
### 热门产品


### 热门推荐


### 更多推荐


Copyright © 2013 - 2026 Tencent Cloud. All Rights Reserved. 腾讯云 版权所有 
[深圳市腾讯计算机系统有限公司](https://qcloudimg.tencent-cloud.cn/raw/986376a919726e0c35e96b311f54184d.jpg) ICP备案/许可证号：[粤B2-20090059 ](https://beian.miit.gov.cn/#/Integrated/index)[粤公网安备44030502008569号](https://beian.mps.gov.cn/#/query/webSearch?code=44030502008569)
[腾讯云计算（北京）有限责任公司](https://qcloudimg.tencent-cloud.cn/raw/a2390663ee4a95ceeead8fdc34d4b207.jpg) 京ICP证150476号 | [京ICP备11018762号](https://beian.miit.gov.cn/#/Integrated/index)
[问题归档](https://cloud.tencent.cn/developer/ask/archives.html)[专栏文章](https://cloud.tencent.cn/developer/column/archives.html)[快讯文章归档](https://cloud.tencent.cn/developer/news/archives.html)[关键词归档](https://cloud.tencent.cn/developer/information/all.html)[开发者手册归档](https://cloud.tencent.cn/developer/devdocs/archives.html)[开发者手册 Section 归档](https://cloud.tencent.cn/developer/devdocs/sections_p1.html)
