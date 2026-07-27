# Vercel AI SDK 深度研究

> 研究日期：2026-07-27
> 状态：完成

---

## 资料摘要

### 1. AI SDK 7 官方发布公告

| 字段 | 内容 |
|------|------|
| **标题** | AI SDK 7 is now available |
| **URL** | https://vercel.com/changelog/ai-sdk-7 |
| **来源类型** | 官方发布公告 |
| **核心观点** | AI SDK 7 将 SDK 从模型调用和聊天原语库演进为完整的 Agent 平台，涵盖开发、运行、集成和观测 TypeScript Agent 的全生命周期。 |
| **关键数据点** | 最低 Node.js 22 + ESM 强制；支持 25+ 模型提供商；新增 `HarnessAgent` 统一调用 Claude Code/Codex 等 Agent 框架；`WorkflowAgent` 支持持久化可恢复执行；全局遥测 `registerTelemetry()` 兼容 OpenTelemetry/Langfuse/Datadog 等。 |

---

### 2. Vercel AI SDK 完整开发指南 (GUVI)

| 字段 | 内容 |
|------|------|
| **标题** | Vercel AI SDK: A Complete Guide to Building AI Apps in 2026 |
| **URL** | https://www.guvi.in/blog/vercel-ai-sdk/ |
| **来源类型** | 第三方教程 |
| **核心观点** | Vercel AI SDK 是 2026 年构建 AI Web 应用的事实标准，通过 provider-agnostic 架构将 OpenAI、Anthropic、Google Gemini 等模型统一在相同 API 下。 |
| **关键数据点** | `generateText` / `streamText` 双核心函数；`maxSteps` 多步 Agent 循环；Zod schema 驱动的类型安全工具调用；`useChat` hook 一行管理完整聊天状态（流式渲染、自动滚动、停止/重载）。 |

---

### 3. build AI Agents with Vercel AI SDK (官方 Knowledge Base)

| 字段 | 内容 |
|------|------|
| **标题** | How to build AI Agents with Vercel and the AI SDK |
| **URL** | https://examples.vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk |
| **来源类型** | 官方教程（最后更新 2026-06-29） |
| **核心观点** | 演示如何使用 `ToolLoopAgent`、Zod 工具定义、`stopWhen(stepCountIs(n))` 多步控制、Fluid compute 部署和 Observability 监控来构建生产级 Agent。 |
| **关键数据点** | `stepCountIs` 精准控制 Agent 循环步数；Fluid compute 支持长时间运行 Agent；内置 Observability 和 Logs 面板。 |

---

### 4. Vercel AI SDK vs LangChain 对比 (Strapi / Render)

| 字段 | 内容 |
|------|------|
| **标题** | LangChain vs Vercel AI SDK vs OpenAI SDK: Choose Wisely |
| **URL** | https://strapi.io/blog/langchain-vs-vercel-ai-sdk-vs-openai-sdk-comparison-guide |
| **来源类型** | 深度对比分析 |
| **核心观点** | Vercel AI SDK 适合 React/Next.js 流式聊天界面和 Edge 部署；LangChain 适合复杂 Agent 编排、RAG 管线和有状态工作流。2026 年最常见的生产模式是将两者结合使用。 |
| **关键数据点** | Vercel AI SDK gzip 67.5kB vs LangChain 101.2kB；5 分钟 vs 15 分钟上手时间；25+ vs 50+ 提供商支持；内置 React hooks vs 无前端集成；Edge Runtime 原生支持 vs 不兼容（依赖 Node.js `fs`）。 |

---

### 5. Build AI agents with AI Gateway and AI SDK (官方 Knowledge Base)

| 字段 | 内容 |
|------|------|
| **标题** | Build AI agents with AI Gateway and AI SDK |
| **URL** | https://examples.vercel.com/kb/guide/ai-gateway-and-ai-sdk |
| **来源类型** | 官方教程（最后更新 2026-06-19） |
| **核心观点** | 展示 AI Gateway + AI SDK 的完整集成方案：OIDC 认证、`generateText`/`streamText` 文本生成、`generateObject` 结构化输出、模型 fallback、Vercel Sandbox 安全代码执行、Chat SDK 多平台聊天机器人和 `WorkflowAgent` 持久化可恢复工作流。 |
| **关键数据点** | `models` 数组实现自动 fallback；`needsApproval` 人机协作审批；Vercel Connect 短期提供商 Token；支持 Slack/Teams/Discord 多平台部署。 |

---

### 6. Ai SDK 7 核心新特性详解 (Vercel Blog)

| 字段 | 内容 |
|------|------|
| **标题** | AI SDK 7 is now available (full blog post) |
| **URL** | https://vercel.com/blog/ai-sdk-7 |
| **来源类型** | 官方博客 |
| **核心观点** | SDK 7 的五大支柱：开发 Agent（推理控制/类型化上下文/MCP Apps/TUI）、生产运行（工具审批/持久化执行/超时控制/Sandbox）、集成 Agent 框架（`HarnessAgent`）、观测 Agent（全局遥测/生命周期回调/性能统计）、超越文本（实时语音/视频生成/语音合成与转录/图片生成/重排序）。 |
| **关键数据点** | `reasoning` 顶层参数映射所有主流提供商原生推理设置；HMAC 签名的工具审批防篡改；`WorkflowAgent` 持久化状态跨部署和进程重启；`@ai-sdk/tui` 终端交互式测试；`@ai-sdk/otel` 专用 OpenTelemetry 包。 |

---

### 7. Vercel AI SDK Next.js/React `useChat` 集成模式 (多家来源综合)

| 字段 | 内容 |
|------|------|
| **标题** | Learning Vercel AI SDK (Telerik Series) |
| **URL** | https://www.telerik.com/blogs/learning-vercel-ai-sdk-part-1 |
| **来源类型** | 教程系列（Part 1 + Part 2） |
| **核心观点** | Part 1 覆盖项目搭建、`generateText`/`streamText`、多模态图片输入。Part 2 构建 `ToolLoopAgent`，含自定义工具（时间/问候）、`stepCountIs` 控制、调试步骤，以及基于 Cheerio+Resend 的博客摘要邮件 Agent 实战。 |
| **关键数据点** | `useChat` 一行 hook 替代约 200 行手动 SSE 解析代码；工具调用通过 `m.toolInvocations` 在客户端渲染中间状态；`maxSteps: 5` 是多步 Agent 的关键配置。 |

---

### 8. Tencent Cloud 中文教程系列 (腾讯云开发者社区)

| 字段 | 内容 |
|------|------|
| **标题** | Vercel AI SDK 6 完整教程系列 - 第一部分：基础入门篇 |
| **URL** | https://cloud.tencent.com.cn/developer/article/2630363 |
| **来源类型** | 中文社区教程 |
| **核心观点** | 从中文开发者视角介绍 SDK 6 的提供商统一抽象、`generateText`/`streamText` 核心 API，侧重实际开发体验。 |
| **关键数据点** | 适合中文开发者入门；覆盖提供商切换、流式输出、结构化输出、工具调用等核心场景。 |

---

## 综合分析

### 核心功能架构

```
@ai-sdk/core (ai)
├── generateText()     # 非流式：完整响应用于后端处理
├── streamText()       # 流式：逐 token 输出用于前端交互
├── generateObject()   # 结构化 JSON 输出（Zod 驱动）
├── streamObject()     # 流式结构化输出
├── generateSpeech()   # 语音合成（SDK 7 稳定）
├── transcribe()       # 语音转录（SDK 7 稳定）
│
@ai-sdk/react          # React hooks
├── useChat()          # 聊天状态管理 + 流式渲染
├── useCompletion()    # 文本补全
├── useObject()        # 结构化对象流式接收
│
Provider Packages (@ai-sdk/*)
├── openai / anthropic / google / mistral / groq
├── deepseek / xai / togetherai / fireworks
└── 25+ providers 统一 API
```

### 版本演进关键节点

| 版本 | 关键变化 |
|------|---------|
| v4 | 基础 `generateText`/`streamText`，Provider 抽象 |
| v5 | `Agent` 类（含 `ToolLoopAgent`）、`stopWhen(stepCountIs(n))`、`parameters` -> `inputSchema` 等 breaking changes |
| v6 | 视频生成（实验性）、`@ai-sdk/rsc`/`@ai-sdk/react` 包拆分、`maxTokens` -> `maxOutputTokens` |
| v7 | 完整 Agent 平台：`WorkflowAgent` 持久化、`HarnessAgent` 统一框架、工具审批 HMAC、全局遥测 `registerTelemetry()`、实时语音、MCP Apps、`@ai-sdk/tui`、最低 Node.js 22 + ESM |

### generateText vs streamText 对比

| 维度 | generateText | streamText |
|------|-------------|-----------|
| 输出方式 | 完整响应一次性返回 | 逐 token 流式返回 |
| 适用场景 | 批处理、摘要、分类、报告生成 | 聊天机器人、实时交互界面 |
| 返回格式 | `{ text, usage }` | `toDataStreamResponse()` / `toTextStreamResponse()` |
| 前端配合 | 手动处理 | `useChat` hook 自动管理状态 |
| 工具调用 | 支持（含 `maxSteps` 多步） | 支持（含 `maxSteps` 多步） |

### 支持的模型提供商（25+）

**主流**: OpenAI (GPT-4o/mini), Anthropic (Claude Sonnet 4.6/Haiku 4.5), Google (Gemini 2.0 Pro), Mistral, Groq

**其他**: xAI (Grok), DeepSeek, Together AI, Fireworks, Replicate, fal.ai, ByteDance Seedance, Kling AI, Prodia, Venice.ai 等

### 与 Next.js/React 的集成模式

标准三步骤：
1. **服务端 Route Handler**: `app/api/chat/route.ts` 中 `streamText()` + `result.toDataStreamResponse()`
2. **客户端组件**: `'use client'` + `useChat({ api: '/api/chat' })`
3. **工具定义**: Zod schema 驱动类型安全工具声明，自动生成 JSON Schema 供 LLM 调用

关键配置：`export const runtime = 'edge'` + `export const maxDuration = 30`（默认 10-15s 不够 LLM 流式响应）

### Vercel AI SDK vs LangChain 决策矩阵

| 决策维度 | 选 Vercel AI SDK | 选 LangChain |
|----------|-----------------|-------------|
| 前端框架 | React/Next.js | 任意（无前端 hooks）|
| 部署环境 | Edge/Serverless | 需要 Node.js `fs` |
| 包体积 | 67.5 kB gzip | 101.2 kB gzip |
| Agent 复杂度 | 简单到中等（`maxSteps` 循环）| 复杂（ReAct/Plan-and-Execute/StateGraph）|
| RAG 需求 | 需外部适配器 | 内置完整 Pipeline |
| 学习成本 | 5 分钟上手 | 15 分钟 + 多概念 |
| 可观测性 | 内置 hooks | LangSmith（付费附加）|

**2026 常见生产模式**: Vercel AI SDK 负责前端流式渲染 + `useChat`，LangChain/LangGraph 负责后端 Agent 编排和 RAG，通过 `@ai-sdk/langchain` 适配器互通。

---

## 关键资源 Top 5

1. **AI SDK 7 官方公告** — https://vercel.com/changelog/ai-sdk-7 — 官方/必读
2. **GUVI 完整开发指南** — https://www.guvi.in/blog/vercel-ai-sdk/ — 第三方教程/全面
3. **LangChain vs Vercel AI SDK 对比** — https://strapi.io/blog/langchain-vs-vercel-ai-sdk-vs-openai-sdk-comparison-guide — 深度对比/中立
4. **Build AI Agents (官方 KB)** — https://examples.vercel.com/kb/guide/how-to-build-ai-agents-with-vercel-and-the-ai-sdk — 官方教程/实战
5. **腾讯云中文教程系列** — https://cloud.tencent.com.cn/developer/article/2630363 — 中文社区/入门

---

## 研究结论

Vercel AI SDK 已从 2024 年的模型调用封装库，进化为 2026 年 TypeScript AI 开发的**标准工具链**。SDK 7 将其定位从"模型调用库"升级为"Agent 全生命周期平台"，核心优势在于：

1. **Provider 无关性**: 25+ 提供商统一 API，切换模型只需改一行字符串
2. **流式优先设计**: `streamText` + `useChat` 是同类中最优雅的流式方案
3. **TypeScript 原生**: 类型安全的工具调用、结构化输出、Zod 集成
4. **Vercel 生态整合**: Edge/Serverless/Fluid Compute 原生支持
5. **版本快速迭代**: 4 -> 5 -> 6 -> 7 每个大版本都有显著的平台化升级

主要不足：RAG 和复杂 Agent 编排仍需 LangChain 配合，SDK 自身仅提供轻量级模式（`maxSteps` 循环）。
