# Open-Source AI Agent Frameworks Compared — 2026

> 来源：FutureAGI
> URL: https://futureagi.com/blog/oss-agent-frameworks-2026/
> 作者：Nikhil Pareek
> 日期：2025年7月17日（2026年5月14日更新）

## 核心框架对比

### 1. LangGraph（MIT）
- **架构：** Graph-based state runtime（图状态运行时）
- **最适合：** Durable, stateful multi-agent workflows
- LangChain v1 agents 构建于LangGraph之上
- 当状态、分支、重试和人工审核主导设计时的首选

### 2. CrewAI（MIT）
- **架构：** Role and task orchestration
- **最适合：** 具有清晰角色的Agent团队
- 纯编排代码，"框架无需任何API密钥即可运行"
- Agents可通过Ollama、vLLM或LiteLLM指向本地提供商

### 3. AutoGen（MIT，维护模式）
- **架构：** 对话式多Agent运行时
- **状态：** 维护模式，新用户指向Microsoft Agent Framework
- Microsoft导向团队应使用**Microsoft Agent Framework**替代

### 4. smolagents（Apache 2.0）
- **架构：** CodeAgent模式（Hugging Face）
- **最适合：** 紧凑、最小代码的原型

### 5. AGNO（Apache 2.0）
- **架构：** SDK + AgentOS运行时
- **最适合：** 低开销的生产Agent
- 原Phidata，2026年5月7日改为Apache 2.0

### 6. Letta（Apache 2.0，原MemGPT）
- **架构：** 持久内存运行时
- **最适合：** 需要长期可编辑记忆的Agent
- 当"持久记忆是产品行为"时选择（个人助手、编码Agent）

### 7. LlamaIndex Agent（MIT）
- **架构：** 基于数据和工具的AgentWorkflow
- **最适合：** 检索中心的应用
- 当"文档加载、索引、解析、检索和工具调用属于一个系统"时选择

## 决策指南

| 优先级 | 起点 |
|--------|------|
| 状态工作流（分支、重试、人工审核） | LangGraph |
| 清晰的角色/任务分解 | CrewAI |
| 紧凑原型 | smolagents |
| 低开销生产部署 | AGNO |
| 持久可编辑记忆 | Letta |
| 检索密集型/数据中心的系统 | LlamaIndex |
| Microsoft导向新项目 | Microsoft Agent Framework |

## 许可证速查

| 框架 | 许可证 |
|------|--------|
| LangGraph | MIT |
| CrewAI | MIT |
| AutoGen | MIT + CC-BY-4.0（维护模式） |
| smolagents | Apache 2.0 |
| AGNO | Apache 2.0 |
| Letta | Apache 2.0 |
| LlamaIndex Agent | MIT |

## 核心结论

>"没有通用的最佳选择。" 应将框架与问题的主要约束相匹配：编排复杂度指向LangGraph或CrewAI，记忆需求指向Letta，检索需求指向LlamaIndex，低开销生产部署指向AGNO或smolagents。
