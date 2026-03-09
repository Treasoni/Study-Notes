---
tags: [openclaw, 集成, plugins, skills, mcp]
created: 2026-03-02
updated: 2026-03-04
---

# OpenClaw 对接第三方软件指南

> [!info] 概述
> **OpenClaw 本身不具备 AI 能力，所有功能都通过对接大模型和第三方服务实现**。将其想象成"万能转换器"——通过 Skills 插件连接各种软件和服务。

## 核心概念

### OpenClaw 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                     OpenClaw 网关                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐               │
│  │Skills系统│  │ 第三方API │  │ 通讯软件集成  │               │
│  │         │  │           │  │              │               │
│  └────┬────┘  └─────┬─────┘  └──────┬───────┘               │
│       │            │              │                        │
│       ▼            ▼              ▼                        │
│  ┌─────────┐  ┌──────────┐  ┌─────────────┐               │
│  │邮件服务  │  │云存储API │  │IM通讯平台    │               │
│  │日历API  │  │文件管理  │  │协作平台      │               │
│  └─────────┘  └──────────┘  └─────────────┘               │
└─────────────────────────────────────────────────────────┘
```

### 集成方式对比

| 类型 | 说明 | 难度 | 典型场景 |
|------|------|------|----------|
| **官方 Skills** | ClawHub 官方市场，开箱即用 | ⭐ | 邮件、日历、天气等 |
| **社区 Skills** | GitHub 社区贡献 | ⭐⭐ | 特定网站、自定义功能 |
| **第三方 API** | 通过 HTTP/JSON 接入 | ⭐⭐⭐ | 自研服务、企业内部系统 |
| **通讯平台** | Telegram、飞书、微信等 | ⭐⭐⭐ | 消息推送、群聊机器人 |

---

## 一、官方 Skills 安装

### 1.1 ClawHub 技能市场

**官方技能市场地址**：https://clawhub.ai.ai/skills

> [!info] 来源
> - [OpenClaw 官方文档](https://docs.openclaw.ai/zh-CN) - Skills 系统说明
> - [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills) - 700+ 社区技能收录

### 1.2 安装方式

#### 命令行安装

```bash
# 列出已安装的 Skills
openclaw skills list

# 从 ClawHub 安装
openclaw skills install <skill-name>

# 从 GitHub 直接安装
openclaw skills install github:user/repo

# 查看技能详情
openclaw skills info <skill-name>

# 卸载技能
openclaw skills remove <skill-name>
```

#### 对话中安装

```bash
# 直接在 OpenClaw 对话中输入
/install skill-name

# 或
openclaw install skill-name
```

### 1.3 推荐官方 Skills

| Skill | 功能 | 用途 |
|-------|------|------|
| `mail-reader` | 邮件读取 | 邮件摘要、待办事项提取 |
| `google-calendar` | 日历集成 | 日程管理、事件提醒 |
| `github` | GitHub 集成 | PR 管理、issue 跟踪 |
| `notion` | Notion 集成 | 笔记同步、数据库操作 |
| `supabase` | 数据库 | 数据存储、查询 |

---

## 二、第三方 API 对接

> [!info] 来源
> - [OpenClaw 第三方 API 接入指南](https://blog.csdn.net/zhouzongxin94/article/details/158544866) - CSDN
> - [OpenClaw 配置文档](https://docs.openclaw.ai/zh-CN/configuration) - 官方文档

### 2.1 配置大模型 API

OpenClaw 需要对接大模型才能工作，常用平台：

#### 阿里云百炼（推荐国内用户）

```bash
# 配置阿里云百炼
openclaw config set llm.model qwen3-max-2026-01-23
openclaw config set llm.api_key sk-xxxxxxxxxxxxxxxx

# 设置温度参数
openclaw config set llm.temperature 0.7

# 重启服务生效
openclaw restart
```

#### DeepSeek

```bash
openclaw config set llm.model deepseek-chat
openclaw config set llm.api_key sk-xxxxxxxxxxxxxxxx
openclaw config set llm.base_url https://api.deepseek.com
```

#### Anthropic Claude

```bash
openclaw config set llm.model claude-sonnet-4
openclaw config set llm.api_key sk-ant-xxxxxxxxxxxxxxxx
```

### 2.2 对接自定义 API

配置文件位置：`~/.openclaw/config.json`

```json
{
  "llm": {
    "model": "your-model-name",
    "api_key": "your-api-key",
    "base_url": "https://your-api-endpoint",
    "temperature": 0.7
  }
}
```

---

## 三、通讯软件集成

### 3.1 Telegram 集成

> [!info] 来源
> - [OpenClaw Telegram 集成教程](https://developer.aliyun.com/article/1712751) - 阿里云开发者社区
> - [OpenClaw + Telegram 实操指南](https://www.cnblogs.com/weipo0105/p/19605771) - 博客园
> - [Telegram Bot 官方文档](https://core.telegram.org/bots/api) - Telegram

#### 创建 Telegram Bot

```bash
# 1. 向 @BotFather 发送 /newbot
# 2. 按提示设置 bot 名称
# 3. 获取 API Token
```

#### 配置 OpenClaw

```bash
# 安装 Telegram skill
openclaw skills install telegram

# 配置 Telegram Bot Token
openclaw config set telegram.bot_token "your-bot-token"

# 配置允许的 Chat ID
openclaw config set telegram.allowed_chat_ids "your-chat-id"

# 启动服务
openclaw restart
```

#### 使用方式

```bash
# 在 Telegram 中向 Bot 发送指令
/help         # 查看帮助
/status       # 查看状态
/summary      # 获取日报
```

### 3.2 飞书集成

> [!info] 来源
> - [OpenClaw 飞书集成完整指南](https://developer.aliyun.com/article/1710416) - 阿里云开发者社区
> - [飞书开放平台文档](https://open.feishu.cn/document) - 飞书官方
> - [OpenClaw + 飞书集成指南](https://openclawguide.org/zh/integrations/openclaw-feishu) - OpenClaw Guide

#### 配置飞书机器人

```bash
# 安装飞书 skill
openclaw skills install feishu

# 配置飞书应用凭证
openclaw config set feishu.app_id "your-app-id"
openclaw config set feishu.app_secret "your-app-secret"
```

#### 设置事件订阅

1. 在飞书开放平台配置事件订阅
2. 设置接收服务器 URL
3. 配置加密密钥

### 3.3 WhatsApp 集成

通过 Beeper 平台集成：

```bash
# 安装 WhatsApp skill（通过 Beeper Bridge）
openclaw skills install whatsapp

# 配置 Beeper 账户
openclaw config set beeper.account "your-account"
```

---

## 四、生产力工具集成

> [!info] 来源
> - [OpenClaw Skills 生态介绍](https://web-note.cn/article/Interesting-tools/1459.html) - Web Note
> - [OpenClaw 办公自动化实战](https://developer.aliyun.com/article/1713896) - 阿里云开发者社区

### 4.1 邮件集成

#### Gmail 集成

```bash
# 安装 Gmail skill
openclaw skills install gmail

# 配置 OAuth 认证
openclaw config set gmail.client_id "your-client-id"
openclaw config set gmail.client_secret "your-client-secret"
```

#### 邮件摘要功能

```bash
# 设置每日邮件摘要 cron 任务
# 添加到 ~/.openclaw/crontab
0 8 * * * openclaw skill run mail-reader --summary
```

### 4.2 日历集成

#### Google Calendar

```bash
openclaw skills install google-calendar

# 配置日历 API
openclaw config set calendar.api_key "your-api-key"
openclaw config set calendar.calendar_id "primary"
```

### 4.3 笔记软件集成

#### Obsidian 集成

```bash
openclaw skills install obsidian

# 配置 Obsidian Vault 路径
openclaw config set obsidian.vault_path "/path/to/vault"
```

#### Notion 集成

```bash
openclaw skills install notion

# 配置 Notion Integration Token
openclaw config set notion.token "your-integration-token"
openclaw config set notion.database_id "your-database-id"
```

---

## 五、开发工具集成

> [!info] 来源
> - [OpenClaw 开发者文档](https://docs.openclaw.ai/zh-CN/development) - 官方文档
> - [GitHub Skills 集成示例](https://github.com/VoltAgent/awesome-openclaw-skills) - GitHub

### 5.1 GitHub 集成

```bash
openclaw skills install github

# 配置 GitHub Token
openclaw config set github.token "your-github-token"

# 配置默认仓库
openclaw config set github.default_owner "your-username"
openclaw config set github.default_repo "default-repo"
```

### 5.2 开发协作集成

#### Git 仓库管理

```bash
# 管理 Pull Request
openclaw skills install git-pr

# 自动代码审查
openclaw skills install code-review
```

---

## 六、MCP 协议集成

> [!info] 概述
> **MCP（Model Context Protocol）是 Anthropic 提出的标准化协议，让 AI 模型能通过统一接口连接外部工具和数据源**。OpenClaw 通过内置的 **mcporter** 插件原生支持 MCP 协议。

### 6.1 什么是 MCP？

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP 架构示意                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  AI 模型 (Claude/GPT)                                       │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐                                           │
│  │ MCP Client  │  ← 统一接口                                │
│  │ (OpenClaw)  │                                           │
│  └──────┬──────┘                                           │
│         │                                                   │
│    ┌────┼────┬────────┬────────┐                           │
│    ▼    ▼    ▼        ▼        ▼                           │
│ ┌────┐┌────┐┌────┐┌────────┐┌─────┐                       │
│ │文件││数据库││GitHub││高德地图││Slack│  ← 各种 MCP Server   │
│ └────┘└────┘└────┘└────────┘└─────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 mcporter 插件

**mcporter** 是 OpenClaw 的官方内置 Skill，用于支持标准 MCP 协议适配：

| 特性 | 说明 |
|------|------|
| **开箱即用** | 无需额外安装，OpenClaw 内置 |
| **协议支持** | 支持 stdio 和 streamable-http |
| **兼容性** | 兼容各类标准 MCP Server |

> [!info] 来源
> - [OpenClaw 阿里云+高德MCP配置](https://developer.aliyun.com/article/171) - 阿里云开发者社区
> - [OpenClaw + Apify MCP 集成](https://developer.aliyun.com/article/1714190) - 阿里云开发者社区

### 6.3 配置 MCP Server

#### 安装 MCP Skill

```bash
# mcporter 已内置，直接配置即可
# 查看当前 MCP 配置
openclaw config get mcp

# 添加 MCP Server
openclaw config set mcp.servers.filesystem '{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
}'
```

#### 配置示例：文件系统 MCP

```json
// ~/.openclaw/config.json
{
  "mcp": {
    "servers": {
      "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
      }
    }
  }
}
```

#### 配置示例：高德地图 MCP

```bash
# 配置高德地图 API Key
openclaw config set mcp.servers.amap '{
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server-amap"],
  "env": {
    "AMAP_API_KEY": "your-amap-api-key"
  }
}'
```

### 6.4 常用 MCP Server 列表

| MCP Server | 功能 | 安装命令 |
|------------|------|----------|
| `@modelcontextprotocol/server-filesystem` | 文件系统访问 | `npx -y @modelcontextprotocol/server-filesystem /path` |
| `@modelcontextprotocol/server-github` | GitHub 操作 | `npx -y @modelcontextprotocol/server-github` |
| `@modelcontextprotocol/server-postgres` | PostgreSQL 数据库 | `npx -y @modelcontextprotocol/server-postgres` |
| `@anthropic/mcp-server-amap` | 高德地图 | `npx -y @anthropic/mcp-server-amap` |
| `@anthropic/mcp-server-slack` | Slack 集成 | `npx -y @anthropic/mcp-server-slack` |

### 6.5 验证 MCP 连接

```bash
# 重启服务使配置生效
openclaw restart

# 检查 MCP 状态
openclaw mcp list

# 测试 MCP 工具调用
openclaw mcp test filesystem
```

### 6.6 MCP vs Skills 对比

| 对比项 | MCP | Skills |
|--------|-----|--------|
| **协议** | 标准化协议 | OpenClaw 专有 |
| **生态** | 跨平台通用 | OpenClaw 专属 |
| **配置** | JSON 配置文件 | 安装即用 |
| **适用场景** | 需要标准化的企业集成 | 快速功能扩展 |
| **开发难度** | 需了解 MCP 协议 | 编写 Skill 模板 |

> [!tip] 💡 选择建议
> - 需要对接 **多个 AI 平台**？选择 **MCP**（一次配置，多平台通用）
> - 只在 **OpenClaw 内使用**？选择 **Skills**（更简单快捷）

> [!info] 来源
> - [MCP 官方文档](https://modelcontextprotocol.io) - Anthropic
> - [Awesome MCP Servers](https://github.com/modelcontextprotocol/servers) - GitHub

---

## 七、最佳实践

### 集成前准备

| 准备项 | 说明 |
|--------|------|
| **明确需求**：搞清楚要解决什么问题 |
| **API 文档**：仔细阅读目标服务的 API 文档 |
| **权限配置**：确保有足够的 API 权限 |
| **测试环境**：先在测试环境验证 |

### 技能开发流程

```bash
# 1. 查看官方示例技能
git clone https://github.com/openclaw-skills/example-skill

# 2. 参考官方模板创建技能
# 技能包含 metadata.json 和 skill.md 两个文件

# 3. 本地测试技能
openclaw skills link /path/to/skill

# 4. 发布到 ClawHub（可选）
openclaw skills publish
```

### 配置管理

```bash
# 查看所有配置
openclaw config list

# 重置配置
openclaw config reset

# 备份配置
cp ~/.openclaw/config.json ~/.openclaw/config.json.bak
```

---

## 常见问题

### Q1：Skill 安装后无法使用？

```bash
# 检查 Skill 状态
openclaw skills list

# 查看 Skill 日志
openclaw logs <skill-name>

# 重新安装
openclaw skills reinstall <skill-name>
```

### Q2：第三方 API 调用失败？

```bash
# 测试 API 连通性
curl -X POST https://your-api-endpoint \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json"

# 检查 OpenClaw 配置
openclaw config list | grep api
```

### Q3：如何调试集成问题？

```bash
# 启用调试模式
openclaw --verbose

# 查看完整日志
tail -f ~/.openclaw/logs/current.log
```

---

## 个人笔记
> [!personal] 💡 我的理解与感悟
>
> 1. **OpenClaw 的核心价值在于"连接"**：它本身不产生 AI，而是连接各种服务和 AI
>
> 2. **Skills 生态很强大**：1700+ 技能几乎涵盖所有场景
>
> 3. **配置建议**：
>    - 国内用户优先用阿里云百炼（稳定、便宜、有免费额度）
>    - Telegram 是最成熟的集成方案（文档全、社区活跃）
>    - 不要一次装太多技能，容易冲突
>
> 4. **踩坑记录**：
>    - API 密钥不要直接写在配置文件中，使用环境变量
>    - 安装新 Skill 后记得重启服务
>    - 第三方 API 注意调用频率限制

---

## 相关文档

- [[../OpenClaw MOC]] - OpenClaw 文档索引
- [[../入门层/OpenClaw核心概念]] - 核心概念
- [[../配置层/OpenClaw安装后配置指南]] - 配置指南
- [[../入门层/OpenClaw安装教程]] - OpenClaw 安装指南
- [[OpenClaw数字人商业调查]] - 数字人商业调研

## 参考资料

### 官方资源
- [OpenClaw 官方网站](https://openclaw.ai) - 产品介绍与下载
- [OpenClaw 官方文档](https://docs.openclaw.ai/zh-CN) - 完整技术文档
- [ClawHub 技能市场](https://clawhub.ai/skills) - 官方插件市场
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw) - 源代码
- [OpenClaw 中文社区](https://www.moltcn.com) - 中文用户社区

### 社区资源
- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills) - 700+ 社区技能收录
- [OpenClaw Discord 社区](https://discord.gg/openclaw) - 官方 Discord

### 教程参考
- [OpenClaw 第三方 API 接入实战](https://blog.csdn.net/zhouzongxin94/article/details/158544866) - CSDN
- [阿里云 OpenClaw 部署指南](https://developer.aliyun.com/article/1713896) - 阿里云开发者社区
- [OpenClaw Telegram 集成教程](https://developer.aliyun.com/article/1712751) - 阿里云开发者社区
- [OpenClaw 飞书集成指南](https://developer.aliyun.com/article/1710416) - 阿里云开发者社区
- [OpenClaw 小白到大师完全教程](https://m.sohu.com/a/990999944_122611832) - 搜狐

### 第三方服务文档
- [Telegram Bot API](https://core.telegram.org/bots/api) - Telegram 官方
- [飞书开放平台](https://open.feishu.cn/document) - 飞书官方
- [Gmail API 文档](https://developers.google.com/gmail/api) - Google
- [Google Calendar API](https://developers.google.com/calendar) - Google
- [Notion API 文档](https://developers.notion.com/) - Notion 官方

### MCP 协议相关
- [MCP 官方文档](https://modelcontextprotocol.io) - Anthropic 官方协议文档
- [Awesome MCP Servers](https://github.com/modelcontextprotocol/servers) - 官方 MCP Server 合集
- [OpenClaw 阿里云+高德MCP配置](https://developer.aliyun.com/article/171) - 阿里云开发者社区
- [OpenClaw + Apify MCP 集成](https://developer.aliyun.com/article/1714190) - 阿里云开发者社区

---

**最后更新**：2026-03-04
