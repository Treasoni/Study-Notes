# OpenVort — 开源AI员工平台

> 来源：GitHub - openvort/openvort
> URL: https://github.com/openvort/openvort
> 日期：2026年

## 概述

OpenVort是一个开源AI员工平台，让AI员工与真人团队一起在企业微信、钉钉、飞书里协作。采用 AGPL-3.0 协议，Python 3.11+ (FastAPI) + Vue 3.5 技术栈。

- 网站：openvort.com
- GitHub Stars: 452（较新项目）
- 最新版本：v0.13.0

## 核心特性

### AI驱动的智能体循环
基于Claude tool use，Agent自主决定调用哪些工具，支持多模型故障转移

### AI员工
绑定角色和技能的虚拟成员，可自动执行日报、代码审查、测试等任务
支持一键创建Docker工作空间

### 异步任务执行
Agent执行与SSE解耦，用户离开页面AI仍可继续工作
完成后自动通知，支持进度查看、中断、追加指令

### 通知系统
聊天即消息目的地，IM即门铃
实时WebSocket未读标记、声音/Toast/桌面提醒

### MCP Server
所有已注册工具自动通过Streamable HTTP暴露
可直接从Cursor、Claude Desktop调用

### 多IM支持
企业微信、钉钉、飞书，以及OpenClaw多平台网关
支持语音消息收发（ASR/TTS）

### 10个内置插件
VortFlow（敏捷工作流）、VortGit（代码仓库）、VortSketch（AI原型生成）
Jenkins CI/CD、知识库（RAG）、报告管理、定时任务、浏览器自动化

### 四级Skill体系
内置Skill / 公共Skill / 个人Skill / 市场Skill

## 架构

```
Users → IM Platform → Channel Adapter → Dispatcher → Agent Runtime → Plugin Tools → External Systems
      (WeCom/DingTalk/Feishu)                                    ↕
                                                            LLM(Claude)
```

## 部署

### Docker部署（推荐）
```bash
curl -fsSL https://raw.githubusercontent.com/openvort/openvort/master/docker-compose.yml -o docker-compose.yml
docker compose up -d
```

### pip安装
```bash
pip install openvort
openvort start
```

## 扩展市场
浏览、安装和发布Skills与Plugins
```bash
openvort marketplace install skill author/my-skill
openvort marketplace publish ./my-extension
```
