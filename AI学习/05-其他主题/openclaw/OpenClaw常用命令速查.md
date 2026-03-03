---
tags: [openclaw, 命令, 速查, cli]
created: 2026-03-04
updated: 2026-03-04
---

# OpenClaw 常用命令速查

> [!info] 概述
> **按使用场景整理的 OpenClaw CLI 命令速查手册**。不同于按字母排序的传统手册，这里按实际使用场景分类，让你快速找到需要的命令。

## 快速查找

| 我想... | 跳转章节 |
|---------|----------|
| 启动/停止服务 | [[#一、日常启动与停止]] |
| 排查问题 | [[#二、诊断与排错]] |
| 修改配置 | [[#三、配置管理]] |
| 切换 AI 模型 | [[#四、模型管理]] |
| 连接聊天平台 | [[#五、通道管理]] |
| 安装插件 | [[#六、技能管理]] |
| 更新版本 | [[#七、系统维护]] |
| 打开聊天界面 | [[#八、交互界面]] |

---

## 一、日常启动与停止

### 场景：每天启动 OpenClaw

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw gateway` | 前台启动网关 | 本地测试、查看实时日志 |
| `openclaw gateway --daemon` | 后台启动网关 | 服务器部署、长期运行 |
| `openclaw gateway --port 8080` | 指定端口启动 | 默认端口被占用时 |

### 场景：停止/重启服务

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw stop` | 停止所有服务 | 临时关闭、维护期间 |
| `openclaw restart` | 重启服务 | 修改配置后生效 |
| `openclaw gateway stop` | 仅停止网关 | 其他组件继续运行 |

> [!tip] 💡 最佳实践
> 修改任何配置后，记得运行 `openclaw restart` 使配置生效。

> [!info] 来源
> - [OpenClaw CLI命令详解](https://blog.csdn.net/sgr011215/article/details/158461994) - CSDN
> - [OpenClaw 正确用法总结指南](https://m.blog.csdn.net/ailuloo/article/details/157762560) - CSDN

---

## 二、诊断与排错

### 场景：服务出问题时

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw doctor` | 健康检查 | 服务异常、启动失败 |
| `openclaw doctor --fix` | 自动修复 | 检测并自动修复问题 |
| `openclaw status` | 查看运行状态 | 确认服务是否正常运行 |
| `openclaw status --deep` | 深度状态检测 | 详细诊断各组件状态 |
| `openclaw logs` | 查看日志 | 排查具体错误信息 |
| `openclaw logs --follow` | 实时日志 | 监控运行情况 |

### 场景：API 调用失败

```bash
# 1. 先检查服务状态
openclaw status

# 2. 查看错误日志
openclaw logs

# 3. 运行诊断
openclaw doctor

# 4. 尝试自动修复
openclaw doctor --fix
```

> [!info] 来源
> - [OpenClaw 常用操作命令完整速查手册](https://m.blog.csdn.net/qq_44866828/article/details/158266497) - CSDN
> - [OpenClaw 最常用命令速查](https://m.blog.csdn.net/u011701632/article/details/158458451) - CSDN

---

## 三、配置管理

### 场景：查看/修改配置

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw config list` | 查看所有配置 | 了解当前设置 |
| `openclaw config get <key>` | 获取单项配置 | 查看特定设置 |
| `openclaw config set <key> <value>` | 修改配置 | 更改设置 |
| `openclaw config file` | 定位配置文件 | 手动编辑配置 |
| `openclaw config unset <key>` | 删除配置 | 移除设置项 |

### 场景：配置 API Key

```bash
# 查看当前模型配置
openclaw config get models.providers

# 设置 DeepSeek API
openclaw config set models.providers.deepseek '{
  "baseUrl": "https://api.deepseek.com/v1",
  "apiKey": "sk-your-key",
  "api": "openai-completions",
  "models": [{"id": "deepseek-chat", "name": "DeepSeek Chat"}]
}'

# 设置默认模型
openclaw config set agents.defaults.model.primary "deepseek-chat"

# 重启生效
openclaw restart
```

### 场景：配置局域网访问

```bash
# 允许局域网访问
openclaw config set gateway.bind "0.0.0.0"

# 设置 CORS（允许特定域名）
openclaw config set gateway.controlUi.allowedOrigins '["https://example.ts.net"]'
```

> [!info] 来源
> - [OpenClaw 配置大模型API](https://m.blog.csdn.net/qq_39329902/article/details/157542782) - CSDN
> - [OpenClaw 国内大模型配置指南](https://blog.csdn.net/weixin_45110225/article/details/157724298) - CSDN

---

## 四、模型管理

### 场景：切换 AI 模型

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw models list` | 列出已配置模型 | 查看可用模型 |
| `openclaw models set <模型名>` | 设置默认模型 | 切换主力模型 |

### 场景：多模型切换

```bash
# 查看已配置的模型
openclaw models list

# 切换到 DeepSeek
openclaw models set deepseek-chat

# 切换到 Claude
openclaw models set claude-sonnet-4
```

> [!info] 来源
> - [OpenClaw 使用 DeepSeek API 配置教程](https://juejin.cn/post/7605419006682791978) - 掘金

---

## 五、通道管理

### 场景：连接聊天平台

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw channels login whatsapp` | 登录 WhatsApp | 连接 WhatsApp |
| `openclaw channels login telegram` | 登录 Telegram | 连接 Telegram Bot |
| `openclaw channels login discord` | 登录 Discord | 连接 Discord Bot |
| `openclaw channels logout <平台>` | 登出平台 | 断开连接 |

### 场景：WhatsApp 配置

```bash
# 生成登录二维码
openclaw channels login whatsapp

# 扫描二维码后，查看连接状态
openclaw status
```

> [!info] 来源
> - [OpenClaw 阿里云/本地部署实战指南](https://developer.aliyun.com/article/1713915) - 阿里云

---

## 六、技能管理

### 场景：安装插件/技能

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw skills list` | 列出已安装技能 | 查看当前插件 |
| `openclaw skills install <name>` | 安装技能 | 添加新功能 |
| `openclaw skills install github:user/repo` | 从 GitHub 安装 | 安装社区技能 |
| `openclaw skills info <name>` | 查看技能详情 | 了解技能功能 |
| `openclaw skills remove <name>` | 移除技能 | 卸载不需要的技能 |
| `openclaw skills update <name>` | 更新技能 | 升级到最新版 |

### 场景：安装常用技能

```bash
# 安装官方技能
openclaw skills install browser

# 从 GitHub 安装
openclaw skills install github:openclaw/skill-filesystem

# 查看已安装
openclaw skills list
```

> [!info] 来源
> - [OpenClaw 对接第三方软件指南](OpenClaw对接第三方软件指南.md) - 本地文档

---

## 七、系统维护

### 场景：版本管理

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw --version` | 查看当前版本 | 确认版本号 |
| `openclaw update` | 自动更新 | 升级到最新版 |
| `openclaw --help` | 查看帮助 | 了解所有命令 |

### 场景：更新 OpenClaw

```bash
# 检查当前版本
openclaw --version

# 自动更新（推荐）
openclaw update

# 手动更新（npm）
npm i -g openclaw@latest

# 手动更新（pnpm）
pnpm add -g openclaw@latest
```

> [!info] 来源
> - [OpenClaw v2026.3.1版发布](https://www.landiannews.com/archives/111965.html) - 蓝点网

---

## 八、交互界面

### 场景：与 AI 对话

| 命令 | 说明 | 使用时机 |
|------|------|----------|
| `openclaw tui` | 终端聊天界面 | 命令行对话（推荐新手） |
| `openclaw dashboard` | 打开网页控制台 | 浏览器管理 |
| `openclaw chat` | 管道输入对话 | 脚本中使用 |

### 场景：终端对话

```bash
# 启动 TUI 界面（推荐）
openclaw tui

# 管道方式发送消息
echo "解释什么是 MCP 协议" | openclaw chat

# 打开网页控制台
openclaw dashboard
# 或直接访问 http://localhost:18789
```

> [!info] 来源
> - [OpenClaw 从入门到进阶完整实战教程](https://m.blog.csdn.net/2301_81108348/article/details/158356909) - CSDN

---

## 命令速查表

### 高频命令 Top 10

| 排名 | 命令 | 使用场景 |
|------|------|----------|
| 1 | `openclaw gateway` | 每天启动 |
| 2 | `openclaw restart` | 配置后生效 |
| 3 | `openclaw status` | 检查状态 |
| 4 | `openclaw logs` | 排查问题 |
| 5 | `openclaw doctor` | 诊断故障 |
| 6 | `openclaw config set` | 修改配置 |
| 7 | `openclaw tui` | 终端聊天 |
| 8 | `openclaw update` | 更新版本 |
| 9 | `openclaw skills install` | 安装插件 |
| 10 | `openclaw models set` | 切换模型 |

---

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[OpenClaw核心概念]] | Gateway 是核心组件 |
| [[OpenClaw安装教程]] | 安装后的命令使用 |
| [[OpenClaw安装后配置指南]] | config 命令详解 |
| [[OpenClaw对接第三方软件指南]] | skills 命令详解 |

---

## 常见问题

### Q1：修改配置后不生效？

```bash
# 记得重启服务
openclaw restart
```

### Q2：端口被占用？

```bash
# 查看端口占用
lsof -i :18789

# 使用其他端口启动
openclaw gateway --port 8080

# 或修改配置
openclaw config set gateway.port 8080
openclaw restart
```

### Q3：忘记配置了什么？

```bash
# 查看所有配置
openclaw config list

# 定位配置文件
openclaw config file
```

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
>
> 1. **最常用的命令**：`openclaw gateway`、`openclaw restart`、`openclaw logs`
>
> 2. **排错流程**：
>    - 先 `openclaw status` 看状态
>    - 再 `openclaw logs` 看日志
>    - 最后 `openclaw doctor` 诊断
>
> 3. **配置技巧**：
>    - 修改配置后必须 `restart`
>    - 复杂配置可以直接编辑文件（`openclaw config file`）
>    - 记得备份配置文件

---

## 相关文档

- [[OpenClaw MOC]] - OpenClaw 文档索引
- [[OpenClaw核心概念]] - 理解 Gateway 架构
- [[OpenClaw安装后配置指南]] - 详细配置说明
- [[OpenClaw对接第三方软件指南]] - Skills 插件使用

---

## 参考资料

### 官方资源
- [OpenClaw 官方文档](https://docs.openclaw.ai) - 完整技术文档
- [OpenClaw GitHub](https://github.com/openclaw/openclaw) - 源代码

### 命令参考
- [OpenClaw CLI命令详解](https://blog.csdn.net/sgr011215/article/details/158461994) - CSDN
- [OpenClaw 最常用命令速查](https://m.blog.csdn.net/u011701632/article/details/158458451) - CSDN
- [OpenClaw 命令速查手册](https://www.cnblogs.com/liuziyi1/p/19632738) - 博客园
- [OpenClaw 常用操作命令完整速查手册](https://m.blog.csdn.net/qq_44866828/article/details/158266497) - CSDN

### 实战教程
- [阿里云部署指南+命令大全](https://developer.aliyun.com/article/1713532) - 阿里云开发者社区
- [OpenClaw 从入门到进阶完整实战教程](https://m.blog.csdn.net/2301_81108348/article/details/158356909) - CSDN
- [OpenClaw v2026.3.1版发布](https://www.landiannews.com/archives/111965.html) - 蓝点网

---

**最后更新**：2026-03-04
