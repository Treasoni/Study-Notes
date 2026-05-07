---
tags: [ai, 学习指南, index]
---

# MOC - 内容索引

> [!info] 说明
> 本页面是 AI 学习资料的**内容索引（Map of Content）**，按主题分类整理所有文档。

## 目录结构

```
AI学习/
├── 00-索引/           # 总索引和路线图
├── 01-基础概念/       # Agent、Prompt、MCP、SubAgent等核心概念
├── 02-通用工具/       # Tailscale等通用工具
├── Claude Code 教程/   # Claude Code 完整教程体系
├── 03-技术专题/       # RAG、OCR、AI模型对比
└── 04-项目实践/       # OpenClaw数字人项目
```

---

## 按主题分类

### 基础概念

理解 AI Agent 生态的核心概念。

#### 六大核心概念

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[01-基础概念/人工智能重要的六大概念体系]] | `ai`, `基础概念` | Prompt、Agent、MCP、SubAgent、Skills、Agent Teams 核心概念详解 |
| [[01-基础概念/Prompt提示词]] | `ai`, `基础概念`, `prompt` | 提示词工程原理、System/User Prompt、2025趋势、最佳实践 |
| [[01-基础概念/Agent智能体]] | `ai`, `基础概念`, `agent` | Agent架构、Agentic AI、工作模式、与普通AI区别 |
| [[01-基础概念/AI-Agents]] | `ai`, `基础概念`, `agent` | AI Agents核心概念、LLM vs Agent区别、核心组件架构、主流框架 |
| [[01-基础概念/MCP协议]] | `ai`, `基础概念`, `mcp` | MCP原理、三层架构、2025生态发展、Tools/Resources/Prompts |
| [[01-基础概念/SubAgent子代理]] | `ai`, `基础概念`, `subagent` | 上下文隔离、并行处理、与Agent区别、适用场景 |
| [[01-基础概念/Skills 是什么]] | `ai`, `基础概念`, `skills` | Skills机制、三层架构、渐进式加载、与SubAgent对比 |
| [[01-基础概念/Agent Teams智能体团队]] | `ai`, `基础概念`, `agent-teams` | 多智能体协作、主流框架、协作模式、与SubAgent区别 |
| [[01-基础概念/Hook钩子]] | `ai`, `基础概念`, `hook`, `自动化` | Hook事件驱动机制、4种类型、23种事件、与Skills/MCP区别 |

#### 学习规划

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[01-基础概念/2026-AI职业角色与路线图]] | `ai`, `基础概念`, `career`, `roadmap` | 2026年AI职业角色与学习路径 |
| [[01-基础概念/AI工程师学习路线图]] | `ai`, `career`, `roadmap` | AI工程师8个月学习计划 |
| [[01-基础概念/AI学习路径与技能图谱]] | `ai`, `learning-path`, `skills` | 14周快速学习路径 |
| [[01-基础概念/AI工程范式演进-Prompt到Harness]] | `ai`, `工程范式` | Prompt → Context → Harness 演进 |

> [!tip] 学习建议
> - **入门** → 先读 [[01-基础概念/人工智能重要的六大概念体系]] 获得全局视角
> - **深入学习** → 逐一阅读六大核心概念的独立笔记

---

### Claude Code 教程

Claude Code 系统的完整教程体系。

#### 入门

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[Claude Code 教程/如何使用Claude code]] | `ai`, `工具使用` | 完整安装配置指南，包含多平台配置、代理设置、MCP/Skills 配置 |

#### 基础功能

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[Claude Code 教程/Claude Code 常用功能]] | `claude`, `ai`, `工具使用` | 功能速查手册，快速查找常用命令和操作 |
| [[Claude Code 教程/Claude Code CLI 完整参考]] | `ai`, `工具使用`, `cli` | CLI 完整命令参考，交互模式与 Print 模式 |
| [[Claude Code 教程/Claude Code 会话管理]] | `claude`, `ai`, `工具使用` | 会话创建、恢复、清除等管理技巧 |
| [[Claude Code 教程/Claude Code 模型与推理设置]] | `claude`, `ai`, `工具使用` | CLI 和 VSCode 插件的模型配置、推理参数 |

#### 进阶功能

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[Claude Code 教程/Claude Code Subagents 完整指南]] | `ai`, `工具使用`, `subagents` | Subagent 完整指南，包含内置类型、自定义 Agent 创建 |
| [[Claude Code 教程/Claude Code Hooks 使用指南]] | `claude`, `ai`, `工具使用`, `hook`, `自动化` | Hook配置详解、Matcher语法、实战示例 |
| [[Claude Code 教程/Claude Code Memory 完整指南]] | `claude`, `ai`, `工具使用`, `memory` | Memory 系统详解、层级架构、Auto Memory |
| [[Claude Code 教程/Claude Code Checkpoints 使用指南]] | `ai`, `claude-code`, `checkpoints` | Checkpoints 自动快照、Rewind 回滚、Summarize 压缩 |
| [[Claude Code 教程/Claude Code 插件系统使用指南]] | `ai`, `进阶应用`, `插件` | 插件系统架构、安装、创建自定义插件 |

#### 高级功能

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[Claude Code 教程/Claude Code 高级功能]] | `ai`, `进阶应用` | Claude Code 高级功能详解 |
| [[Claude Code 教程/Claude Code Slash Commands 完整参考]] | `claude`, `ai`, `工具使用`, `斜杠命令` | 55+ 内置命令参考 |
| [[Claude Code 教程/Claude Code 定时任务自动化指南]] | `claude-code`, `自动化`, `launchd`, `cron` | 定时自动化配置 |
| [[Claude Code 教程/Claude-Code-多Agent流程设计]] | `Claude-Code`, `多Agent`, `AI工作流` | 多 Agent 流程设计完整指南 |
| [[Claude Code 教程/Claude MCP 使用指南]] | `ai`, `进阶应用` | MCP 协议原理、配置文件管理 |
| [[Claude Code 教程/高级功能/如何编写Skills]] | `ai`, `进阶应用` | Skills 编写实战指南，包含 metadata.json 和 skill.md 结构 |
| [[Claude Code 教程/高级功能/CLAUDE.md 使用指南]] | `claude`, `ai`, `进阶应用`, `配置` | 项目级 CLAUDE.md 配置指南 |
| [[Claude Code 教程/高级功能/LLM-Prompt-Caching-提示缓存]] | `llm`, `缓存`, `成本优化` | LLM API 提示缓存原理、各厂商定价对比 |

#### 实战练习

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[Claude Code 教程/Subagent 实战练习]] | `ai`, `高级应用`, `练习` | 5个渐进式练习，从简单到复杂掌握 Subagent |

> [!tip] 文档选择
> - **首次安装** → 阅读 [[Claude Code 教程/如何使用Claude code]]
> - **快速查命令** → 查看 [[Claude Code 教程/Claude Code 常用功能]]
> - **编写 Skills** → 阅读 [[Claude Code 教程/高级功能/如何编写Skills]]
> - **定时任务** → 阅读 [[Claude Code 教程/Claude Code 定时任务自动化指南]]

---

### 通用工具

其他实用工具教程。

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[02-通用工具/Tailscale使用指南]] | `tailscale`, `vpn`, `networking` | 基于 WireGuard 的零配置 VPN 组网工具 |

---

### 技术专题

独立的技术领域学习资料。

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[03-技术专题/RAG技术入门指南]] | `ai`, `RAG` | RAG 检索增强生成技术完整指南，从基础概念到进阶技术 |
| [[03-技术专题/OCR概念笔记]] | `技术`, `OCR` | OCR 光学字符识别技术概念、工具和应用场景 |
| [[03-技术专题/AI模型对比/GLM系列模型完整对比]] | `glm`, `ai模型`, `模型对比` | GLM 全系列模型详细对比 |
| [[03-技术专题/AI模型对比/DeepSeek-V4]] | `deepseek`, `ai模型`, `模型对比` | DeepSeek-V4 预览版笔记 |

---

### 项目实践

数字人项目相关资料。

| 文档 | 标签 | 摘要 |
|------|------|------|
| [[04-项目实践/openclaw/OpenClaw MOC]] | `数字人`, `openclaw` | OpenClaw 完整文档索引与学习路径 |
| [[04-项目实践/openclaw/入门层/OpenClaw核心概念]] | `数字人`, `openclaw`, `架构` | OpenClaw 核心概念：网关、工作原理、Hub-and-Spoke 架构 |
| [[04-项目实践/openclaw/入门层/OpenClaw安装教程]] | `数字人`, `openclaw` | OpenClaw 数字人项目安装配置指南 |
| [[04-项目实践/openclaw/配置层/OpenClaw安装后配置指南]] | `数字人`, `openclaw`, `配置` | OpenClaw 安装后终端配置全过程 |
| [[04-项目实践/openclaw/配置层/OpenClaw Web控制台局域网访问配置]] | `数字人`, `openclaw`, `web`, `局域网` | Web 控制台局域网访问配置 |
| [[04-项目实践/openclaw/配置层/OpenClaw网关开机自启与HTTPS配置]] | `openclaw`, `daemon`, `https` | 开机自启配置、Tailscale Serve HTTPS |
| [[04-项目实践/openclaw/应用层/OpenClaw对接第三方软件指南]] | `数字人`, `openclaw`, `集成` | Skills 插件系统、MCP 协议、第三方 API 对接 |
| [[04-项目实践/openclaw/应用层/OpenClaw多智能体协作指南]] | `数字人`, `openclaw`, `multi-agent` | 多智能体协作指南 |
| [[04-项目实践/openclaw/应用层/OpenClaw本地智能助手搭建指南]] | `数字人`, `openclaw`, `本地助手` | 本地智能助手搭建 |
| [[04-项目实践/openclaw/应用层/OpenClaw数字人商业调查]] | `数字人`, `openclaw`, `商业调研` | 数字人行业商业调查报告 |
| [[04-项目实践/openclaw/参考层/OpenClaw常用命令速查]] | `openclaw`, `cli`, `命令`, `速查` | CLI 命令速查表 |
| [[04-项目实践/openclaw/选型层/OpenClaw与国内仿制品对比]] | `openclaw`, `选型` | 与国内仿制品对比 |

> [!tip] 索引导航
> 📚 **[[04-项目实践/openclaw/OpenClaw MOC]]** - OpenClaw 完整文档索引与学习路径

---

## 学习路径

### 新手路径

```
1. [[01-基础概念/人工智能重要的六大概念体系]] - 获得全局视角
   ↓
2. [[Claude Code 教程/如何使用Claude code]] - 安装配置
   ↓
3. [[Claude Code 教程/Claude Code 常用功能]] - 功能速查
   ↓
4. [[01-基础概念/Prompt提示词]] - 理解提示词
   ↓
5. [[01-基础概念/Skills 是什么]] - 理解 Skills
   ↓
6. [[Claude Code 教程/高级功能/如何编写Skills]] - 编写实战
```

### 进阶路径

```
1. [[01-基础概念/Agent智能体]] - 理解 Agent
   ↓
2. [[01-基础概念/MCP协议]] - 理解 MCP
   ↓
3. [[Claude Code 教程/Claude MCP 使用指南]] - 配置 MCP
   ↓
4. [[Claude Code 教程/高级功能/CLAUDE.md 使用指南]] - 配置项目规则
   ↓
5. [[01-基础概念/SubAgent子代理]] - 理解 SubAgent
   ↓
6. [[Claude Code 教程/Claude Code Subagents 完整指南]] - 创建自定义 Agent
   ↓
7. [[Claude Code 教程/Subagent 实战练习]] - 实战巩固
```

### 高级路径

```
1. [[01-基础概念/Agent Teams智能体团队]] - 理解多智能体协作
   ↓
2. [[Claude Code 教程/Claude-Code-多Agent流程设计]] - 学习多 Agent 设计模式
   ↓
3. 探索主流框架（CrewAI、LangGraph、AutoGen）
   ↓
4. 构建复杂的多智能体系统
```

---

## 按标签索引

### ai - 所有 AI 学习相关文档

#### 基础概念
- [[01-基础概念/人工智能重要的六大概念体系]]
- [[01-基础概念/Prompt提示词]]
- [[01-基础概念/Agent智能体]]
- [[01-基础概念/AI-Agents]]
- [[01-基础概念/MCP协议]]
- [[01-基础概念/SubAgent子代理]]
- [[01-基础概念/Skills 是什么]]
- [[01-基础概念/Agent Teams智能体团队]]
- [[01-基础概念/Hook钩子]]

#### Claude Code
- [[Claude Code 教程/如何使用Claude code]]
- [[Claude Code 教程/Claude Code 常用功能]]
- [[Claude Code 教程/Claude Code CLI 完整参考]]
- [[Claude Code 教程/Claude Code 会话管理]]
- [[Claude Code 教程/Claude Code 模型与推理设置]]
- [[Claude Code 教程/Claude Code Subagents 完整指南]]
- [[Claude Code 教程/Claude Code Hooks 使用指南]]
- [[Claude Code 教程/Claude Code Memory 完整指南]]
- [[Claude Code 教程/Claude Code Checkpoints 使用指南]]
- [[Claude Code 教程/Claude Code 插件系统使用指南]]

#### 进阶应用
- [[Claude Code 教程/高级功能/如何编写Skills]]
- [[Claude Code 教程/Claude MCP 使用指南]]
- [[Claude Code 教程/高级功能/CLAUDE.md 使用指南]]
- [[Claude Code 教程/高级功能/LLM-Prompt-Caching-提示缓存]]

### 数字人

数字人相关项目文档。

- [[04-项目实践/openclaw/OpenClaw安装教程]]
- [[04-项目实践/openclaw/OpenClaw安装后配置指南]]
- [[04-项目实践/openclaw/OpenClaw数字人商业调查]]
- [[04-项目实践/openclaw/OpenClaw对接第三方软件指南]]

### vpn

VPN 和网络组网相关文档。

- [[02-通用工具/Tailscale使用指南]]

---

## 快速查找

### 我想...

| 目标 | 推荐文档 |
|------|----------|
| 了解六大核心概念 | [[01-基础概念/人工智能重要的六大概念体系]] |
| 学习提示词工程 | [[01-基础概念/Prompt提示词]] |
| 理解 Agent 智能体 | [[01-基础概念/Agent智能体]] |
| 了解 MCP 协议 | [[01-基础概念/MCP协议]] |
| 理解 SubAgent 子代理 | [[01-基础概念/SubAgent子代理]] |
| 学习 Skills 技能系统 | [[01-基础概念/Skills 是什么]] |
| 了解多智能体协作 | [[01-基础概念/Agent Teams智能体团队]] |
| 首次安装 Claude Code | [[Claude Code 教程/如何使用Claude code]] |
| CLI 完整命令参考 | [[Claude Code 教程/Claude Code CLI 完整参考]] |
| 快速查找命令 | [[Claude Code 教程/Claude Code 常用功能]] |
| 查看内置斜杠命令 | [[Claude Code 教程/Claude Code Slash Commands 完整参考]] |
| 配置 Memory 记忆系统 | [[Claude Code 教程/Claude Code Memory 完整指南]] |
| 配置 Hook 自动化 | [[Claude Code 教程/Claude Code Hooks 使用指南]] |
| 编写自定义 Skill | [[Claude Code 教程/高级功能/如何编写Skills]] |
| 配置 MCP | [[Claude Code 教程/Claude MCP 使用指南]] |
| 创建自定义 Agent | [[Claude Code 教程/Claude Code Subagents 完整指南]] |
| 设计多 Agent 流程 | [[Claude Code 教程/Claude-Code-多Agent流程设计]] |
| 练习 Subagent | [[Claude Code 教程/Subagent 实战练习]] |
| 配置项目规则 | [[Claude Code 教程/高级功能/CLAUDE.md 使用指南]] |
| 了解插件系统 | [[Claude Code 教程/Claude Code 插件系统使用指南]] |
| 回滚代码和对话 | [[Claude Code 教程/Claude Code Checkpoints 使用指南]] |
| Claude Code 定时自动化 | [[Claude Code 教程/Claude Code 定时任务自动化指南]] |
| 学习 RAG 技术 | [[03-技术专题/RAG技术入门指南]] |
| 了解 GLM 模型对比 | [[03-技术专题/AI模型对比/GLM系列模型完整对比]] |
| 了解 LLM API 缓存定价 | [[Claude Code 教程/高级功能/LLM-Prompt-Caching-提示缓存]] |
| 学习 Tailscale 组网 | [[02-通用工具/Tailscale使用指南]] |
| 了解数字人项目 | [[04-项目实践/openclaw/OpenClaw安装教程]] |

---

## 相关文档

- [[00-索引/README]] - 项目入口
- [[00-索引/00-学习路线图]] - 详细学习路径规划
