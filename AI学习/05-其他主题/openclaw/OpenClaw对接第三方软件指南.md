---
tags: [openclaw, 集成, plugins, skills]
created: 2026-03-02
updated: 2026-03-02
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

**官方技能市场地址**：https://clawhub.ai/skills

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

## 六、最佳实践

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
- [[AI学习/05-其他主题/openclaw/OpenClaw安装教程]] - OpenClaw 安装指南
- [[AI学习/05-其他主题/openclaw/OpenClaw数字人商业调查]] - 数字人商业调研

## 参考资料
- [OpenClaw 官方网站](https://openclaw.ai)
- [ClawHub 技能市场](https://clawhub.ai/skills)
- [OpenClaw GitHub](https://github.com/openclaw)
- [Awesome OpenClaw Skills](https://github.com/VoltAgent/awesome-openclaw-skills)
- [OpenClaw Discord 社区](https://discord.gg/openclaw)

---

**最后更新**：2026-03-02
