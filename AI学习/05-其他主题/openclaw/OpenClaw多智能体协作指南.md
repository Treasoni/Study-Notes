---
tags: [openclaw, multi-agent, 协作, 团队, 编排]
created: 2026-03-06
updated: 2026-03-06
---

# OpenClaw 多智能体协作指南

> [!info] 概述
> **多智能体协作（Multi-Agent Orchestration）是 OpenClaw 的核心高阶能力，让你从"单一对话"进化为"指挥 AI 团队"**。通过配置多个专业 Agent 并行工作，实现复杂任务的高效拆解与执行。

## 核心概念

### 为什么需要多 Agent？

| 单 Agent 痛点 | 多 Agent 解决方案 |
|---------------|-------------------|
| **上下文污染** - 任务切换导致记忆混乱 | 独立工作区，互不干扰 |
| **人设混乱** - 写作风格与技术调试混为一谈 | 专属人格设定，专业分工 |
| **Token 消耗高** - 每次加载全量上下文 | 按需加载，节省 40%+ 成本 |
| **效率低下** - 必须按顺序串行执行 | 并行处理，效率提升 3 倍 |
| **单点故障** - 一个错误导致全盘崩溃 | 局部失败不影响整体 |

### 通俗理解

**🎯 比喻：从"全能管家"到"专业团队"**

```
单 Agent 模式（全能管家）
┌─────────────────────────────────────────────┐
│  你 → AI 管家（一个人包揽所有）              │
│       ├─ 写文章                             │
│       ├─ 写代码                             │
│       ├─ 管财务                             │
│       ├─ 查资料                             │
│       └─ ... 精力分散，样样通样样松          │
└─────────────────────────────────────────────┘

多 Agent 模式（专业团队）
┌─────────────────────────────────────────────┐
│  你 → 主 Agent（指挥官）                     │
│        ├─ 文案 Agent → 专注写作             │
│        ├─ 编码 Agent → 专注代码             │
│        ├─ 财务 Agent → 专注记账             │
│        └─ 调研 Agent → 专注搜索             │
│       各司其职，并行高效                      │
└─────────────────────────────────────────────┘
```

---

## 多智能体协作的七种模式

### 模式对比表

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| **Supervisor**（主管模式） | 主 Agent 分配任务，子 Agent 执行 | 通用场景 |
| **Sequential**（串行链式） | Agent A → Agent B → Agent C 顺序执行 | 有明确步骤的工作流 |
| **Parallel**（并行模式） | 多个 Agent 同时处理，结果汇总 | 独立子任务批量处理 |
| **Ensemble**（集成交互） | 多 Agent 输出结果，由聚合器整合 | 需要多视角分析 |
| **Swarm**（蜂群模式） | 大量轻量级 Agent 自主协作，无明确层级 | 大规模探索性任务 |
| **Debate**（辩论模式） | Agent 之间相互质疑和反驳 | 需要多角度验证 |
| **Mesh**（网格模式） | 去中心化架构，通过共享上下文协作 | 复杂企业级应用 |

### 模式图解

```
┌─────────────────────────────────────────────────────────────┐
│                    多智能体协作模式                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1️⃣ Supervisor（主管模式）                                  │
│     ┌─────────┐                                             │
│     │ 主Agent  │ ──分派──> [子A] [子B] [子C]                │
│     └─────────┘ <──汇总──  [结果] [结果] [结果]             │
│                                                             │
│  2️⃣ Sequential（串行链式）                                  │
│     [Agent A] ──> [Agent B] ──> [Agent C] ──> 结果          │
│                                                             │
│  3️⃣ Parallel（并行模式）                                    │
│     ┌── [Agent A] ──┐                                       │
│     ├── [Agent B] ──┼──> 聚合器 ──> 结果                    │
│     └── [Agent C] ──┘                                       │
│                                                             │
│  4️⃣ Debate（辩论模式）                                      │
│     [Agent A] <──反驳──> [Agent B]                          │
│         │                      │                            │
│         └──────> 裁判 <───────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## OpenClaw 多 Agent 架构

### 两层支持

```
┌─────────────────────────────────────────────────────────────┐
│                  OpenClaw 多 Agent 架构                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  层面一：多 Agent 并行运行（Multi-Agent）                    │
│  ├─ 同一个 Gateway 进程中运行多个隔离 Agent                 │
│  ├─ 每个 Agent 有独立的：                                   │
│  │   ├─ Workspace（工作目录）                               │
│  │   ├─ Identity（人格设定 agent.md）                       │
│  │   ├─ Tools（工具白名单/黑名单）                          │
│  │   └─ Model（独立模型配置）                               │
│  └─ 通过 Bindings 路由消息                                  │
│                                                             │
│  层面二：子 Agent 动态 Spawn（Subagents）                    │
│  ├─ 主 Agent 可动态生成子 Agent                             │
│  ├─ 支持嵌套调用（Nested Orchestration）                    │
│  └─ 子 Agent 可再生自己的子 Agent，形成层级                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 配置示例

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "name": "Personal Assistant",
        "workspace": "~/.openclaw/workspace"
      },
      {
        "id": "coder",
        "name": "Coding Agent",
        "workspace": "~/.openclaw/workspace-coding",
        "model": {
          "primary": "anthropic/claude-sonnet-4-6"
        },
        "tools": {
          "allow": ["read", "exec", "write"],
          "deny": ["browser", "cron"]
        }
      },
      {
        "id": "researcher",
        "name": "Research Agent",
        "workspace": "~/.openclaw/workspace-research",
        "model": {
          "primary": "openai/gpt-5.2"
        },
        "tools": {
          "allow": ["tavily_search", "web_fetch", "read"]
        }
      }
    ]
  }
}
```

---

## 四大协作机制

### 1. 消息路由与绑定（Bindings）

Bindings 机制决定哪个 Agent 处理 incoming 消息：

```bash
# 查看当前绑定
openclaw agents list --bindings
```

**匹配规则**：最具体优先（Most Specific Wins）

```
发送给 #coding 频道 → 路由到 coder Agent
发送给 #research 频道 → 路由到 researcher Agent
其他消息 → 路由到 main Agent（默认）
```

### 2. Agent 间通信（agentToAgent）

默认 Agent 之间是隔离的，启用通信需要显式配置：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["coder", "reviewer", "tester"]
    }
  }
}
```

这允许一个 Agent 通过 `sessions_send` 向另一个 Agent 发送消息：

```json
{
  "sessionKey": "coder",
  "message": "已完成登录功能实现，请 review"
}
```

### 3. 动态分身（Dynamic Spawning）

按需创建子 Agent：

```bash
# 创建架构师 Agent
openclaw agents add architect \
  --model claude-opus-4-6 \
  --workspace ~/projects/my-app \
  --description "System architect — design decisions"

# 创建开发者 Agent
openclaw agents add developer \
  --model claude-sonnet-4-6 \
  --workspace ~/projects/my-app \
  --description "Full-stack developer"

# 创建审查者 Agent
openclaw agents add reviewer \
  --model claude-opus-4-6 \
  --workspace ~/projects/my-app \
  --description "Code reviewer"
```

### 4. 异构模型协作

为不同任务分配最适合的模型：

| Agent 角色 | 推荐模型 | 原因 |
|------------|----------|------|
| 复杂推理 | Claude Opus / o1 | 深度思考能力强 |
| 快速搜索/摘要 | GPT-4o-mini / Flash | 速度快、成本低 |
| 创意写作 | Claude Sonnet | 文采好、创意强 |
| 代码生成 | Claude Sonnet / DeepSeek | 编程能力强 |

> [!tip] 💡 成本优化
> 异构模型协作可节省 40%+ Token 成本——"好钢用在刀刃上"。

---

## 实战操作手册

### 第一步：创建多 Agent 体系

```bash
# 添加财务 Agent
openclaw agents add finance \
  --workspace ~/.openclaw/workspace-fin \
  --model deepseek-chat

# 添加文案 Agent
openclaw agents add writer \
  --workspace ~/.openclaw/workspace-writer \
  --model claude-sonnet-4-6

# 添加调研 Agent
openclaw agents add researcher \
  --workspace ~/.openclaw/workspace-research \
  --model gpt-4o
```

### 第二步：配置身份与人格

编辑每个 Agent 的 `IDENTITY.md` 文件：

```markdown
# ~/.openclaw/workspace-fin/IDENTITY.md

## 身份
我是您的财务管家「唐总」，精通成本核算与预算管理。

## 沟通风格
- 严谨细致
- 数据驱动
- 每次回复以「唐总好，我是您的财务管家」开头

## 专属 Emoji
💰
```

### 第三步：配置路由规则

```json
// ~/.openclaw/openclaw.json
{
  "agents": {
    "bindings": [
      {
        "match": { "channel": "feishu", "accountId": "finance_bot" },
        "agent": "finance"
      },
      {
        "match": { "channel": "feishu", "accountId": "writer_bot" },
        "agent": "writer"
      },
      {
        "match": { "channel": "*" },
        "agent": "main"
      }
    ]
  }
}
```

### 第四步：测试验证

```bash
# 重启 Gateway
openclaw gateway restart

# 在飞书中分别向不同机器人发送"你是谁"
# 验证是否得到不同风格的回答
```

---

## 典型应用场景

### 场景一：AI 自媒体团队

```
主 Agent（任务分配）
├── 公众号文案 Agent → 撰写深度文章
├── 小红书文案 Agent → 创作种草笔记
├── 配图 Agent → 生成配图
└── 发布 Agent → 定时发布
```

**工作流**：选题 → 并行创作 → 汇总审核 → 发布

### 场景二：项目管理团队

```
主 Agent（需求拆解）
├── 需求分析 Agent → 分析用户需求
├── 开发规划 Agent → 制定开发计划
└── 进度跟踪 Agent → 监控项目进度
```

### 场景三：数据处理团队

```
主 Agent（任务调度）
├── 数据抓取 Agent → 采集数据
├── 数据清洗 Agent → 清洗数据
└── 可视化 Agent → 生成图表
```

### 场景四：超级学习与研究

```
你 → 主 Agent
     ├── Agent A（历史学家）→ 梳理发展简史
     ├── Agent B（科普员）→ 解释核心原理
     └── Agent C（产业分析师）→ 分析市场格局
```

---

## 与飞书/Telegram 多机器人集成

### 飞书多机器人配置

```bash
# 1. 为每个 Agent 创建独立的飞书机器人
# 2. 获取每个机器人的 appId 和 appSecret

# 3. 配置 OpenClaw
openclaw config set channels.feishu.accounts.finance_bot.appId "cli_xxx1"
openclaw config set channels.feishu.accounts.finance_bot.appSecret "xxx1"

openclaw config set channels.feishu.accounts.writer_bot.appId "cli_xxx2"
openclaw config set channels.feishu.accounts.writer_bot.appSecret "xxx2"
```

### Telegram 多机器人配置

```bash
# 向 @BotFather 创建多个 Bot
# 获取各自的 Token

openclaw config set telegram.bots.finance.token "123456:ABC"
openclaw config set telegram.bots.writer.token "789012:DEF"
```

---

## 最佳实践

### 任务拆解原则

❌ **错误的拆解**（串行依赖，无法并行）：
> "先查特斯拉股价，然后写分析报告，最后翻译成英文"

✅ **正确的拆解**（独立并行）：
> 启动三个子 Agent：
> - Agent A：独立搜索特斯拉近三年财报数据
> - Agent B：独立收集用户对特斯拉的评价
> - Agent C：独立分析竞品（比亚迪、蔚来）的策略
> 最后汇总三人的结果

### 指令模板

```
请创建 [数量] 个子 Agent，分别扮演 [角色1]、[角色2]...

[角色1] 的任务是：[具体任务描述]
要求：[具体约束]

[角色2] 的任务是：[具体任务描述]
要求：[具体约束]

请在 [时间/条件] 后向我汇报。
```

### 成本优化建议

1. **模型混搭**：关键任务用顶级模型，日常任务用经济型模型
2. **记忆分层**：区分每日流水、长期记忆、语义检索，按需加载
3. **工具权限**：只授予必要的工具权限，减少误操作风险
4. **定期清理**：清理不活跃 Agent 的会话历史

---

## 常见问题

### Q1：多 Agent 会增加成本吗？

**不会，反而会降低**。专业分工避免了上下文污染，Token 消耗可降低 40%+。

### Q2：Agent 之间如何共享信息？

通过：
1. **共享工作区文件** - 读写同一目录下的文件
2. **agentToAgent 通信** - 显式配置后可互相发消息
3. **主 Agent 协调** - 结果汇总到主 Agent

### Q3：最多支持多少个 Agent？

理论上无限制，但建议：
- 个人使用：3-5 个 Agent
- 团队使用：5-10 个 Agent
- 超过 10 个建议拆分为多个 Gateway

### Q4：如何调试 Agent 间的协作问题？

```bash
# 启用详细日志
openclaw gateway --verbose

# 查看特定 Agent 日志
tail -f ~/.openclaw/agents/coder/logs/current.log
```

---

## 与其他概念的关系

| 概念 | 关系 | 说明 |
|------|------|------|
| [[OpenClaw核心概念]] | 基础 | Gateway 是多 Agent 的运行基础 |
| [[OpenClaw对接第三方软件指南]] | 扩展 | Skills 为 Agent 提供工具能力 |
| [[../../01-基础概念/Agent智能体]] | 理论 | Agent 的基础概念 |
| [[../../01-基础概念/Agent Teams智能体团队]] | 进阶 | 智能体团队的理论框架 |

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **多 Agent 是效率革命**：从"单线程对话"进化为"多线程指挥"，效率提升 3 倍+
>
> 2. **核心是"拆解"**：任务拆解正确，协作才能高效；拆解错误，再多的 Agent 也是乱跑
>
> 3. **成本不增反降**：专业分工避免了上下文污染，Token 消耗反而降低 40%
>
> 4. **学习建议**：
>    - 先从 2-3 个 Agent 开始体验
>    - 重点学习任务拆解的艺术
>    - 逐步尝试异构模型协作

---

## 相关文档

- [[OpenClaw MOC]] - OpenClaw 文档索引
- [[OpenClaw核心概念]] - 核心概念
- [[OpenClaw对接第三方软件指南]] - Skills 集成
- [[../../01-基础概念/Agent智能体]] - Agent 基础理论
- [[../../01-基础概念/Agent Teams智能体团队]] - 智能体团队理论

---

## 参考资料

### 官方资源
- [OpenClaw 官方文档](https://docs.openclaw.ai) - 完整技术文档
- [OpenClaw Multi-Agent 配置](https://docs.openclaw.ai/agents) - Agent 配置指南
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 源代码

### 社区资源
- [OpenClaw 多智能体实战指南](https://developer.aliyun.com/article/1713822) - 阿里云开发者社区
- [多智能体系统将成AI新趋势](https://blog.csdn.net/libaiup/article/details/158623689) - CSDN
- [从单线程到多智能体协作](https://m.blog.csdn.net/Stitch2001/article/details/158624152) - CSDN
- [OpenClaw 多智能体并行协作完全指南](https://m.blog.csdn.net/u014177256/article/details/158624065) - CSDN

### 视频教程
- [【保姆级】OpenClaw 全网最细教学](https://www.bilibili.com/video/BV1TpAZzeEiZ) - B站 AI学长小林

---

**最后更新**：2026-03-06
