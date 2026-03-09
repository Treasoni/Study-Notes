---
tags: [openclaw, 企业文档, 知识库, RAG, 智能助手, 飞书]
created: 2026-03-09
updated: 2026-03-09
---

# OpenClaw 本地智能助手搭建指南

> [!info] 概述
> **一句话定义**：使用 OpenClaw + 本地知识库搭建**企业文档智能助手**，让员工通过对话快速查询制度、流程、技术文档。
>
> **🎯 比喻**：就像给每个员工配备了一个"24小时在线的企业百科全书"，随时回答关于公司制度、流程、文档的问题。
>
> **💼 核心场景**：企业文档智能助手（本文重点）

---

## 一、整体架构

### 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    本地智能助手架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                 用户交互层                           │    │
│  │  飞书 │ 钉钉 │ 微信 │ Telegram │ Web 控制台        │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              OpenClaw 核心层                         │    │
│  │  ├─ memorySearch（语义搜索知识库）                   │    │
│  │  ├─ Skills（技能扩展：搜索、PDF处理等）              │    │
│  │  └─ 配置文件（定义 AI 角色和行为）                   │    │
│  │      ├─ SOUL.md - AI 角色/行为准则                  │    │
│  │      ├─ USER.md - 用户背景/偏好                     │    │
│  │      ├─ MEMORY.md - 知识库路径                      │    │
│  │      └─ AGENTS.md - 多 Agent 配置                   │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              知识库层                                │    │
│  │  ├─ 企业文档（Markdown/PDF）                        │    │
│  │  ├─ 培训材料                                        │    │
│  │  ├─ 操作手册                                        │    │
│  │  └─ 向量索引（自动生成）                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              大模型层                                │    │
│  │  DeepSeek │ Qwen │ 本地模型（Ollama）               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件说明

| 组件 | 作用 | 状态 |
|------|------|------|
| **OpenClaw** | AI Agent 框架，连接用户和知识库 | 需部署 |
| **memorySearch** | 内置语义搜索，索引知识库 | 需配置 |
| **知识库** | Markdown/PDF 文件存储 | 需准备 |
| **大模型 API** | 提供推理能力 | 需配置 |

---

## 二、本地部署 OpenClaw

### 2.1 环境准备

#### 系统要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|----------|----------|
| **内存** | 2GB RAM | 4GB+ RAM |
| **CPU** | 2 核 | 4 核+ |
| **存储** | 5GB | 20GB+ |
| **系统** | macOS / Linux / Windows | macOS / Linux |

#### 软件依赖

```bash
# 检查 Node.js 版本（需要 18+）
node -v

# 检查 npm 版本
npm -v

# 如果未安装，使用 nvm 安装
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### 2.2 安装步骤

#### 方式一：一键脚本安装（推荐新手）

```bash
# macOS / Linux
curl -fsSL https://get.openclaw.ai | bash

# Windows (PowerShell)
iwr -useb https://get.openclaw.ai/windows | iex
```

#### 方式二：npm 安装

```bash
# 全局安装
npm install -g openclaw

# 验证安装
openclaw --version
```

#### 方式三：Docker 部署

```bash
# 拉取镜像
docker pull openclaw/openclaw:latest

# 运行容器
docker run -d \
  --name openclaw \
  -v ~/openclaw/workspace:/root/.openclaw/workspace \
  -p 3000:3000 \
  openclaw/openclaw:latest
```

### 2.3 基础配置

#### 初始化工作区

```bash
# 创建工作目录
mkdir -p ~/openclaw-workspace
cd ~/openclaw-workspace

# 初始化配置
openclaw init
```

#### 配置大模型 API

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "models": {
    "default": "deepseek",
    "providers": {
      "deepseek": {
        "type": "openai-compatible",
        "baseURL": "https://api.deepseek.com",
        "apiKey": "YOUR_DEEPSEEK_API_KEY"
      },
      "qwen": {
        "type": "openai-compatible",
        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "YOUR_QWEN_API_KEY"
      }
    }
  }
}
```

> [!tip] 💡 模型选择建议
> - **成本敏感**：DeepSeek（便宜、中文好）
> - **企业合规**：通义千问 Qwen（国产、稳定）
> - **隐私优先**：Ollama 本地模型（完全离线）

> [!info] 📚 来源
> - [OpenClaw 官方文档](https://docs.openclaw.ai/)
> - [OpenClaw 本地部署教程](https://www.53ai.com/news/Openclaw/2026030691254.html)

---

## 三、搭建本地知识库

### 3.1 知识库方案对比

| 方案 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| **memorySearch** | OpenClaw 内置 | 零配置、自动索引、混合搜索 | 仅支持 Markdown |
| **ClawRAG** | 外部 RAG 集成 | 支持 PDF、Word、多格式 | 需额外部署 |

**推荐**：新手先用 **memorySearch**，后续按需升级 ClawRAG。

### 3.2 memorySearch 配置详解

#### 基础配置（新手推荐）

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "sync": {
          "watch": true
        }
      }
    }
  }
}
```

#### 完整配置（进阶）

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "gemini",
        "model": "gemini-embedding-001",
        "remote": {
          "apiKey": "YOUR_GEMINI_API_KEY"
        },
        "sync": {
          "watch": true,
          "watchDebounceMs": 1500
        },
        "query": {
          "maxResults": 8,
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3,
            "candidateMultiplier": 4,
            "mmr": {
              "enabled": true,
              "lambda": 0.7
            },
            "temporalDecay": {
              "enabled": true,
              "halfLifeDays": 30
            }
          }
        },
        "cache": {
          "enabled": true,
          "maxEntries": 50000
        }
      }
    }
  }
}
```

#### 配置参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `provider` | auto | Embedding 提供商（openai/gemini/voyage/mistral/local） |
| `sync.watch` | true | 自动监听文件变化并索引 |
| `watchDebounceMs` | 1500 | 文件变化后等待多久再索引 |
| `maxResults` | 8 | 返回的最大结果数 |
| `vectorWeight` | 0.7 | 语义搜索权重 |
| `textWeight` | 0.3 | 关键词搜索权重 |

### 3.3 知识文件组织

#### 推荐目录结构

```
openclaw-workspace/
├── memory/                    # 知识库目录
│   ├── company/              # 公司资料
│   │   ├── intro.md          # 公司介绍
│   │   ├── org-structure.md  # 组织架构
│   │   └── products.md       # 产品资料
│   ├── training/             # 培训材料
│   │   ├── onboarding.md     # 入职培训
│   │   ├── sop.md            # 标准操作流程
│   │   └── faq.md            # 常见问题
│   ├── docs/                 # 技术文档
│   │   ├── api-guide.md      # API 指南
│   │   └── troubleshooting.md # 故障排查
│   └── policies/             # 规章制度
│       ├── leave-policy.md   # 请假制度
│       └── security.md       # 安全规范
├── SOUL.md                   # AI 角色定义
├── USER.md                   # 用户信息
└── MEMORY.md                 # 记忆配置
```

#### Markdown 文件格式建议

```markdown
---
title: 入职培训指南
tags: [培训, 新人, HR]
date: 2026-03-09
---

# 入职培训指南

## 第一周安排

### Day 1：公司介绍
- 公司历史与发展
- 组织架构
- 核心业务

### Day 2：工具使用
- 邮箱配置
- OA 系统使用
- 开发环境搭建

## 常见问题

Q: 如何申请办公设备？
A: 联系行政部门，填写设备申请表...

Q: 报销流程是什么？
A: 1. 收集发票 2. 填写报销单 3. 提交财务...
```

### 3.4 Embedding 提供商选择

| 提供商 | 成本 | 中文支持 | 推荐场景 |
|--------|------|----------|----------|
| **DeepSeek** | 低 | ⭐⭐⭐⭐⭐ | 国内首选 |
| **通义千问** | 低 | ⭐⭐⭐⭐⭐ | 企业合规 |
| **OpenAI** | 中 | ⭐⭐⭐⭐ | 国际化 |
| **Gemini** | 低（有免费额度） | ⭐⭐⭐⭐ | 预算有限 |
| **local（Ollama）** | 免费 | ⭐⭐⭐ | 隐私优先 |

> [!info] 📚 来源
> - [memorySearch 完整指南](https://dev.to/czmilo/2026-complete-guide-to-openclaw-memorysearch-supercharge-your-ai-assistant-49oc)
> - [OpenClaw RAG 配置](https://medium.com/@C.Dalrymple/customising-my-openclaw-instance-with-rag-retrieval-augmented-generation-0a4fc933c639)

---

## 四、培训新人场景实现

### 4.1 配置文件说明

#### SOUL.md - 定义 AI 角色

```markdown
# SOUL.md - AI 助手角色定义

## 角色定位
你是一个专业的企业培训助手，帮助新员工快速融入团队。

## 核心能力
1. 解答公司相关问题
2. 提供操作指南和培训材料
3. 协助新员工完成入职流程

## 行为准则
- 回答前先搜索知识库
- 提供准确、具体的信息
- 如信息不确定，明确告知
- 引用来源文档

## 回答风格
- 友好、耐心
- 结构清晰（使用列表、步骤）
- 主动提供相关链接
```

#### USER.md - 用户背景

```markdown
# USER.md - 用户信息

## 用户类型
企业新员工

## 常见需求
- 了解公司制度
- 学习工作流程
- 获取培训资料
- 解决日常问题

## 偏好设置
- 语言：中文
- 回答详细程度：详细
- 是否需要引用来源：是
```

#### MEMORY.md - 知识库配置

```markdown
# MEMORY.md - 记忆系统配置

## 知识库路径
- ./memory/company/    # 公司资料
- ./memory/training/   # 培训材料
- ./memory/docs/       # 技术文档
- ./memory/policies/   # 规章制度

## 记忆类型
- 语义记忆：通过 memorySearch 搜索知识库
- 对话记忆：记住用户上下文
- 长期记忆：重要信息持久化存储
```

### 4.2 知识库内容规划

#### 新人培训知识库清单

```
memory/training/
├── 00-入职指南/
│   ├── 公司介绍.md
│   ├── 组织架构.md
│   ├── 联系方式.md
│   └── 第一周安排.md
├── 01-工具使用/
│   ├── 邮箱配置.md
│   ├── OA系统.md
│   ├── VPN使用.md
│   └── 开发环境.md
├── 02-工作流程/
│   ├── 请假流程.md
│   ├── 报销流程.md
│   ├── 采购流程.md
│   └── 会议预订.md
├── 03-技术文档/
│   ├── 代码规范.md
│   ├── Git使用.md
│   ├── API文档.md
│   └── 部署流程.md
└── 99-FAQ/
    ├── 常见问题.md
    └── 故障排查.md
```

### 4.3 交互示例

#### 示例1：查询公司制度

```
用户：公司的请假流程是什么？

AI 助手：
根据《请假流程》文档，请假流程如下：

1. **提前申请**：至少提前 1 个工作日
2. **填写申请**：在 OA 系统提交请假单
3. **审批流程**：
   - 1-3 天：直属领导审批
   - 3-7 天：部门经理审批
   - 7 天以上：总监审批
4. **交接工作**：请假前完成工作交接

📚 来源：memory/policies/leave-policy.md

💡 相关问题：
- 年假有多少天？
- 病假需要什么证明？
```

#### 示例2：新人培训

```
用户：我刚入职，需要做什么？

AI 助手：
欢迎加入！根据《入职培训指南》，你第一周的安排如下：

## Day 1：公司介绍
- [ ] 完成入职手续
- [ ] 领取办公设备
- [ ] 配置邮箱和账号

## Day 2：工具使用
- [ ] 配置开发环境
- [ ] 学习 OA 系统
- [ ] 加入团队群组

## Day 3：团队融入
- [ ] 参加团队会议
- [ ] 了解当前项目
- [ ] 分配导师

📚 来源：memory/training/00-入职指南/第一周安排.md

需要我详细介绍某一天的安排吗？
```

---

## 五、企业文档智能助手实战

> [!tip] 💼 核心场景
> 本章节重点聚焦**企业文档智能助手**的搭建，这是 OpenClaw 最有价值的企业应用场景。

### 5.1 场景概述

**什么是企业文档智能助手？**

> 一句话定义：让员工通过对话方式，快速查询和理解企业内部各类文档（制度、流程、技术文档、合同等）。

**🎯 核心价值**

| 痛点 | 解决方案 | 效果 |
|------|----------|------|
| 文档散落各处 | 统一知识库 | 一站式查询 |
| 查找耗时 | 语义搜索 | 秒级响应 |
| 新人培训成本高 | AI 自动答疑 | 7x24 服务 |
| 文档更新不及时 | 自动索引 | 实时同步 |

### 5.2 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│              企业文档智能助手架构                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  员工端                                                      │
│  ├─ 飞书机器人（推荐）                                       │
│  ├─ 企业微信                                                 │
│  ├─ 钉钉机器人                                               │
│  └─ Web 控制台                                               │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              OpenClaw 核心层                         │    │
│  │  ├─ memorySearch（语义搜索）                         │    │
│  │  ├─ 必装 Skills：                                    │    │
│  │  │   ├─ nano-pdf（PDF 处理）                        │    │
│  │  │   ├─ tavily-search（网络搜索）                   │    │
│  │  │   └─ Bio-MemoryPro（记忆增强）                   │    │
│  │  └─ 配置文件（SOUL.md 定义文档助手角色）             │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              企业文档知识库                          │    │
│  │  ├─ 制度文档（请假/报销/采购流程）                  │    │
│  │  ├─ 技术文档（API文档/架构设计/代码规范）           │    │
│  │  ├─ 产品文档（需求文档/用户手册/FAQ）               │    │
│  │  ├─ 合同模板（NDA/服务协议/销售合同）               │    │
│  │  └─ 培训材料（入职指南/操作手册/视频脚本）          │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ↓                                   │
│  大模型：DeepSeek / 通义千问 / 本地 Ollama                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 必装 Skills 清单

> [!info] 📚 来源
> - [OpenClaw 官方 53 个技能完整指南](https://www.53ai.com/news/Openclaw/2026022738691.html)
> - [OpenClaw Skills 军火库](https://zhuanlan.zhihu.com/p/2010926090475045346)

| Skill | 功能 | 安装命令 | 优先级 |
|-------|------|----------|--------|
| **nano-pdf** | PDF 提取、编辑、生成 | `npx openclaw skills install nano-pdf` | ⭐⭐⭐⭐⭐ |
| **tavily-search** | 网络搜索补充知识 | `npx openclaw skills install tavily-search` | ⭐⭐⭐⭐ |
| **Bio-MemoryPro** | 长期记忆增强 | `npx openclaw skills install bio-memorypro` | ⭐⭐⭐⭐ |
| **obsidian** | 知识库管理 | `npx openclaw skills install obsidian` | ⭐⭐⭐ |
| **notion** | Notion 集成 | `npx openclaw skills install notion` | ⭐⭐⭐ |

### 5.4 企业文档知识库规划

#### 推荐目录结构

```
enterprise-knowledge-base/
├── 01-公司制度/
│   ├── 行政管理/
│   │   ├── 考勤制度.md
│   │   ├── 请假流程.md
│   │   ├── 报销流程.md
│   │   └── 采购流程.md
│   ├── 人力资源/
│   │   ├── 招聘流程.md
│   │   ├── 入职指南.md
│   │   ├── 离职流程.md
│   │   └── 薪酬制度.md
│   └── 财务管理/
│       ├── 预算流程.md
│       ├── 合同审批.md
│       └── 发票管理.md
├── 02-技术文档/
│   ├── 架构设计/
│   │   ├── 系统架构.md
│   │   ├── 技术选型.md
│   │   └── 部署架构.md
│   ├── API文档/
│   │   ├── 接口规范.md
│   │   ├── 认证授权.md
│   │   └── 错误码说明.md
│   ├── 开发规范/
│   │   ├── 代码规范.md
│   │   ├── Git规范.md
│   │   └── 代码审查.md
│   └── 运维文档/
│       ├── 部署流程.md
│       ├── 监控告警.md
│       └── 故障排查.md
├── 03-产品文档/
│   ├── 需求文档/
│   ├── 用户手册/
│   ├── FAQ/
│   └── 版本说明/
├── 04-合同模板/
│   ├── NDA模板.md
│   ├── 服务协议.md
│   └── 销售合同.md
└── 05-培训材料/
    ├── 新人培训/
    ├── 岗位培训/
    └── 技能提升/
```

#### 文档模板示例

```markdown
---
title: 报销流程指南
tags: [财务, 报销, 流程]
department: 财务部
updated: 2026-03-09
---

# 报销流程指南

## 适用范围
本流程适用于公司全体员工日常费用报销。

## 报销类型

| 类型 | 额度限制 | 审批人 | 时效 |
|------|----------|--------|------|
| 交通费 | ≤500元/次 | 直属领导 | 3个工作日 |
| 餐饮费 | ≤200元/次 | 直属领导 | 3个工作日 |
| 差旅费 | 按标准 | 部门经理 | 5个工作日 |
| 培训费 | 需预审批 | 总监 | 7个工作日 |

## 报销步骤

1. **收集票据**
   - 确保发票抬头正确
   - 保留消费凭证

2. **填写报销单**
   - 登录 OA 系统
   - 选择「费用报销」
   - 填写明细并上传附件

3. **提交审批**
   - 根据金额自动流转
   - 可查看审批进度

4. **财务打款**
   - 审批通过后 3 个工作日内到账

## 常见问题

**Q: 发票抬头写什么？**
A: XXX科技有限公司，税号：XXXXXX

**Q: 跨月发票能报销吗？**
A: 可以，但需在发票开具后 3 个月内完成报销。
```

### 5.5 SOUL.md 配置（企业文档助手版）

```markdown
# SOUL.md - 企业文档智能助手

## 角色定位
你是企业的智能文档助手，帮助员工快速查询和理解公司各类文档。

## 核心能力
1. **文档查询**：快速检索公司制度、流程、技术文档
2. **流程指引**：提供详细的操作步骤和注意事项
3. **政策解读**：用通俗语言解释复杂的公司政策
4. **模板提供**：提供各类文档模板和示例

## 行为准则

### 搜索优先
- 回答任何问题前，先使用 memory_search 搜索知识库
- 确认信息准确后再回答
- 如知识库无相关信息，明确告知

### 回答规范
- 引用来源：每条回答标注文档来源
- 结构清晰：使用列表、表格、步骤
- 提供链接：告知原文档位置
- 相关推荐：主动提供相关文档

### 回答格式
```
## 📋 答案
[具体回答内容]

📚 来源：[文档路径]
🔄 相关流程：[相关文档链接]
💡 小提示：[注意事项]
```

## 限制边界
- 不回答知识库外的猜测性问题
- 不提供个人建议或评价
- 敏感信息需提醒用户确认
- 无法回答时建议联系相关部门

## 对话风格
- 专业但不生硬
- 简洁但不遗漏关键信息
- 主动但不过度
```

### 5.6 部署步骤

#### Step 1：安装 OpenClaw

```bash
# 一键安装
curl -fsSL https://get.openclaw.ai | bash

# 初始化
openclaw init
```

#### Step 2：配置大模型

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "models": {
    "default": "deepseek",
    "providers": {
      "deepseek": {
        "type": "openai-compatible",
        "baseURL": "https://api.deepseek.com",
        "apiKey": "YOUR_API_KEY"
      }
    }
  }
}
```

#### Step 3：配置知识库

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "sync": {
          "watch": true
        },
        "query": {
          "maxResults": 10,
          "hybrid": {
            "enabled": true,
            "vectorWeight": 0.7,
            "textWeight": 0.3
          }
        }
      }
    }
  }
}
```

#### Step 4：安装必装 Skills

```bash
# PDF 处理
npx openclaw skills install nano-pdf

# 网络搜索（可选）
npx openclaw skills install tavily-search

# 记忆增强
npx openclaw skills install bio-memorypro
```

#### Step 5：准备知识库

```bash
# 创建知识库目录
mkdir -p ~/openclaw-workspace/memory

# 复制企业文档（支持 .md 格式）
cp -r /path/to/your/docs/* ~/openclaw-workspace/memory/

# 如果是 PDF，先转换为 Markdown
# 可使用 pandoc 或在线工具
```

#### Step 6：配置 SOUL.md

```bash
# 编辑角色配置
nano ~/openclaw-workspace/SOUL.md

# 粘贴上面的「企业文档智能助手」配置
```

#### Step 7：启动服务

```bash
# 启动 OpenClaw
openclaw start

# 访问 Web 控制台
open http://localhost:3000
```

### 5.7 接入企业通讯工具

#### 飞书机器人（推荐）

```bash
# 1. 在飞书开放平台创建企业自建应用
# 2. 获取 App ID 和 App Secret
# 3. 配置 OpenClaw

# 编辑配置
nano ~/.openclaw/channels.json

# 添加飞书配置
{
  "lark": {
    "enabled": true,
    "appId": "YOUR_APP_ID",
    "appSecret": "YOUR_APP_SECRET"
  }
}

# 重启服务
openclaw restart
```

> [!info] 📚 来源
> - [OpenClaw 飞书应用场景与私有化部署](https://news.qiniu.com/archives/post-1772592283328-0)

### 5.8 效果评估

| 指标 | 部署前 | 部署后 | 提升 |
|------|--------|--------|------|
| 文档查询时间 | 10 分钟 | 30 秒 | 95% ↓ |
| 新人培训周期 | 2 周 | 3 天 | 78% ↓ |
| HR 答疑工作量 | 100% | 30% | 70% ↓ |
| 文档使用率 | 20% | 80% | 300% ↑ |

---

## 六、其他实战案例

### 案例1：技术文档助手

**场景**：研发团队需要快速查询 API 文档和代码规范

**解决方案**：

```
架构：
├── OpenClaw 本地部署
├── 知识库：
│   ├── API 文档
│   ├── 架构设计
│   ├── 代码规范
│   └── 故障排查手册
├── 接入：飞书 / Web
└── 模型：DeepSeek API

特色功能：
- 代码示例自动生成
- API 参数说明
- 错误码查询
- 最佳实践推荐
```

### 案例2：新人培训助手

**场景**：HR 部门希望自动化新人培训

**解决方案**：

```
架构：
├── OpenClaw 本地部署
├── 知识库：
│   ├── 公司介绍
│   ├── 规章制度
│   ├── 岗位培训
│   └── FAQ
├── 接入：企业微信
└── 模型：通义千问 API

功能：
- 7x24 小时答疑
- 自动推送培训内容
- 收集常见问题
- 培训进度跟踪
```

---

## 六、常见问题

### Q1：知识库支持哪些文件格式？

**A**：
| 格式 | 支持方式 | 推荐工具 |
|------|----------|----------|
| **Markdown (.md)** | 原生支持 | 直接使用 |
| **PDF** | 需转换或使用 Skills | nano-pdf Skill / pandoc |
| **Word (.docx)** | 需转换为 Markdown | pandoc |
| **Excel (.xlsx)** | 需转换为 Markdown | 手动整理 |

**PDF 处理方案**：

```bash
# 方案1：安装 nano-pdf Skill（推荐）
npx openclaw skills install nano-pdf

# 方案2：使用 pandoc 转换
pandoc input.pdf -o output.md

# 方案3：使用在线工具转换后导入
# 如：Adobe PDF to Word、Smallpdf 等
```

### Q2：如何保证知识库数据安全？

**A**：
- 所有数据存储在本地
- 可使用本地 Embedding 模型（Ollama）
- 配置文件系统权限
- 定期备份 knowledge 目录

### Q3：Embedding API 费用大概多少？

**A**：以 Gemini 为例（有免费额度）：
- 免费额度：每天 100 次请求
- 付费：约 $0.0001/1K tokens
- 月成本预估：小型企业 < ¥100

### Q4：如何更新知识库？

**A**：
- 方式1：直接编辑 Markdown 文件（自动索引）
- 方式2：添加新文件到 memory 目录
- 方式3：通过对话让 AI 记录新信息

### Q5：能否支持多语言？

**A**：可以。推荐使用：
- DeepSeek（中英文都好）
- OpenAI（英文最佳）
- 通义千问（中文最佳）

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 相关文档

### OpenClaw 学习系列
- [[../入门层/OpenClaw核心概念]] - 理解什么是 AI 网关
- [[../入门层/OpenClaw安装教程]] - 详细安装指南
- [[../配置层/OpenClaw安装后配置指南]] - 配置大模型 API
- [[../OpenClaw MOC]] - 完整学习索引
- [[../选型层/OpenClaw与国内仿制品对比]] - 企业选型参考

### 相关技术
- [[../RAG技术入门指南]] - RAG 技术原理

---

## 参考资料

### 官方资源
- [OpenClaw 官方文档](https://docs.openclaw.ai/)
- [GitHub 仓库](https://github.com/openclaw/openclaw)
- [ClawHub 技能市场](https://clawhub.ai.ai/skills)

### 教程文章
- [memorySearch 完整指南](https://dev.to/czmilo/2026-complete-guide-to-openclaw-memorysearch-supercharge-your-ai-assistant-49oc)
- [OpenClaw 本地部署教程](https://www.53ai.com/news/Openclaw/2026030691254.html)
- [阿里云/本地部署指南](https://developer.aliyun.com/article/1713447)
- [OpenClaw 实战指南](https://zhuanlan.zhihu.com/p/2005252288558674437)

### 视频教程
- [OpenClaw 完整课程](https://www.youtube.com/watch?v=vte-fDoZczE) - 设置、技能、语音、记忆
- [DeepSeek+RAGFlow 本地部署](https://www.youtube.com/watch?v=u9PD4yN2f88)
