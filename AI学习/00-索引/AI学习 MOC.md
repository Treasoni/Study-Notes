---
title: "AI学习 MOC"
tags: [moc]
created: 2026-05-14
updated: 2026-05-14
---

# AI学习 MOC

> [!info] 说明
> 本索引涵盖 AI 学习相关笔记，包括基础概念、通用工具、技术专题、项目实践和 Claude Code 教程。

---

## 目录结构

```mermaid
graph TD
    Root[{AI学习}]
    Root --> Index[00-索引]
    Root --> Basics[01-基础概念]
    Root --> Tools[02-通用工具]
    Root --> Topics[03-技术专题]
    Root --> Projects[04-项目实践]
    Root --> Claude[Claude Code 教程]

    Basics --> Agent[AI Agents/Agent 智能体]
    Basics --> MCP[MCP 协议]
    Basics --> Skills[Skills 技能系统]
    Basics --> SubAgent[SubAgent 子代理]
    Basics --> Teams[Agent Teams 智能体团队]
    Basics --> Hook[Hook 钩子]
    Basics --> Prompt[Prompt 提示词]
    Basics --> Harness[Harness Engineering]
    Basics --> Path[AI学习路径/职业路线图]

    Topics --> ModelComparison[AI模型对比]
    Topics --> RAG[RAG 技术]
    Topics --> OCR[OCR 概念]

    Projects --> OpenClaw[openclaw]
    OpenClaw --> OpenClawLayers[5个子层次]
    OpenClawLayers --> Entry[入门层]
    OpenClawLayers --> Config[配置层]
    OpenClawLayers --> Ref[参考层]
    OpenClawLayers --> App[应用层]
    OpenClawLayers --> Selection[选型层]

    Claude --> ClaudeAdvanced[高级功能]
```

---

## 笔记索引

### 00-索引

- [[MOC]]
- [[../../Git/sortspec]]

### 01-基础概念

- [[AI Agents 详解]] #ai-agents #llm #autonomous-systems #智能体
- [[Agent 智能体]] #ai #agent
- [[Agent Teams 智能体团队]] #ai #agent-teams
- [[../01-基础概念/AI学习路径与技能图谱]] #ai #career #learning-path #skills #roadmap
- [[../01-基础概念/AI工程师学习路线图]] #ai-engineer #career #roadmap #llm #machine-learning
- [[2026 AI职业角色与路线图]] #ai #career #roadmap #2026
- [[AI 工程范式演进：从 Prompt 到 Harness]] #ai-engineering #prompt-engineering #context-engineering #harness-engineering #paradigm-evolution
- [[../01-基础概念/AI缓存命中与未命中]] #AI #LLM #缓存 #性能优化
- [[Harness Engineering（系统治理工程）]] #ai-engineering #harness-engineering #agent #system-governance #coding-agent
- [[Hook 钩子]] #ai #hook #自动化
- [[MCP 协议]] #ai #mcp
- [[Prompt 提示词]] #ai #prompt
- [[../01-基础概念/Skills 是什么]] #ai #skills
- [[SubAgent 子代理]] #ai #subagent
- [[../01-基础概念/人工智能重要的六大概念体系]] #ai #基础概念 #中级

### 02-通用工具

- [[../02-通用工具/Tailscale使用指南]] #tailscale #vpn #networking #wireguard

### 03-技术专题

#### AI模型对比

- [[../03-技术专题/AI模型对比/GLM系列模型完整对比]] #glm #ai模型 #模型对比 #智谱AI

#### 根目录

- [[../03-技术专题/OCR概念笔记]]
- [[../03-技术专题/RAG技术入门指南]] #ai #RAG #检索增强生成 #知识库

### 04-项目实践

#### openclaw

##### 入门层

- [[../04-项目实践/openclaw/入门层/OpenClaw安装教程]] #openclaw #配置 #终端 #安装
- [[../04-项目实践/openclaw/入门层/OpenClaw核心概念]] #openclaw #gateway #架构 #概念

##### 配置层

- [[../04-项目实践/openclaw/配置层/OpenClaw Web控制台局域网访问配置]] #openclaw #web #局域网 #control-ui #cors
- [[../04-项目实践/openclaw/配置层/OpenClaw安装后配置指南]] #openclaw #配置 #终端 #安装
- [[../04-项目实践/openclaw/配置层/OpenClaw网关开机自启与HTTPS配置]] #openclaw #daemon #systemd #tailscale #https #开机自启

##### 参考层

- [[../04-项目实践/openclaw/参考层/OpenClaw常用命令速查]] #openclaw #命令 #速查 #cli

##### 应用层

- [[../04-项目实践/openclaw/应用层/OpenClaw多智能体协作指南]] #openclaw #multi-agent #协作 #团队 #编排
- [[../04-项目实践/openclaw/应用层/OpenClaw对接第三方软件指南]] #openclaw #集成 #plugins #skills #mcp
- [[../04-项目实践/openclaw/应用层/OpenClaw本地智能助手搭建指南]] #openclaw #企业文档 #知识库 #RAG #智能助手 #飞书
- [[../04-项目实践/openclaw/应用层/OpenClaw数字人商业调查]] #OpenClaw #数字人 #AI代理 #商业调查 #技术方案

##### 选型层

- [[../04-项目实践/openclaw/选型层/OpenClaw与国内仿制品对比]] #openclaw #企业选型 #工具对比 #ai-agent #国内替代品

### Claude Code 教程

- [[../Claude Code 教程/Claude Code Checkpoints 使用指南]] #ai #claude-code #checkpoints #session-management
- [[../Claude Code 教程/Claude Code CLI 完整参考]] #ai #工具使用 #cli #claude-code
- [[../Claude Code 教程/Claude Code Hooks 使用指南]] #claude #ai #工具使用 #hook #自动化
- [[../Claude Code 教程/Claude Code Memory 完整指南]] #claude #ai #工具使用 #memory #claude-md #持久化上下文
- [[../Claude Code 教程/Claude Code Slash Commands 完整参考]] #claude #ai #工具使用 #斜杠命令 #slash-commands
- [[../Claude Code 教程/Claude Code Subagents 完整指南]] #claude #ai #工具使用 #subagents #代理 #任务委托
- [[../Claude Code 教程/Claude Code 会话管理]] #claude #ai #工具使用
- [[../Claude Code 教程/Claude Code 定时任务自动化指南]] #claude-code #自动化 #定时任务 #launchd #hooks #调度 #macos #loop
- [[../Claude Code 教程/Claude Code 常用功能]] #claude #ai #工具使用
- [[../Claude Code 教程/Claude Code 插件系统使用指南]] #ai #进阶应用 #插件
- [[../Claude Code 教程/Claude Code 模型与推理设置]] #claude #ai #工具使用 #模型配置
- [[../Claude Code 教程/Claude Code 高级功能]] #claude #ai #进阶应用 #高级功能
- [[../Claude Code 教程/Claude MCP 使用指南]] #ai #进阶应用
- [[../Claude Code 教程/Claude-Code-多Agent流程设计]] #Claude-Code #多Agent #AI工作流 #Agent协作
- [[../Claude Code 教程/Subagent 实战练习]] #ai #高级应用 #练习
- [[../Claude Code 教程/如何使用Claude code]] #ai #工具使用
- [[../04-项目实践/openclaw/OpenClaw MOC]]

#### 高级功能

- [[../Claude Code 教程/高级功能/CLAUDE.md 使用指南]] #claude #ai #进阶应用 #配置
- [[../Claude Code 教程/高级功能/如何编写Skills]] #ai #进阶应用

---

## 概览

- 📂 目录：`AI学习`
- 📝 笔记总数：46
- 📁 子目录数：6
- 📅 生成日期：2026-05-14
