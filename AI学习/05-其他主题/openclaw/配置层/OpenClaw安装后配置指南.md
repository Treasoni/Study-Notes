---
tags: [openclaw, 配置, 终端, 安装]
created: 2026-03-03
updated: 2026-03-03
---

# OpenClaw 安装后配置指南

> [!info] 概述
> **OpenClaw 安装只是第一步，配置才是让它"活"起来的关键**。就像买了新手机需要开机设置一样，配置过程就是让 OpenClaw 连接大模型、理解你的指令。

## 核心概念

### 是什么
OpenClaw 安装后的配置是指设置大模型 API、配置通信通道、设置基本参数的过程。

### 为什么需要
- **连接大模型**：OpenClaw 本身没有 AI，需要配置大模型 API 才能工作
- **个性化设置**：配置让 OpenClaw 按你的方式工作
- **安全验证**：设置 API Key 确保服务可用

### 通俗理解
**🎯 比喻**：OpenClaw 就像一个"万能遥控器"，配置过程就是给它"装电池"和"配对设备"。没有配置的 OpenClaw 就像没有电池的遥控器，再强大也用不了。

**📦 配置三大件**：
1. **大模型配置**（电池）→ 选择 AI 模型
2. **API Key**（激活码）→ 验证服务权限
3. **通信通道**（信号）→ 连接聊天平台

---

## 一、配置向导（推荐新手）

### 1.1 启动配置向导

安装完成后，运行以下命令启动配置向导：

```bash
# 启动交互式配置向导
openclaw onboard

# 或者带守护进程安装（开机自启）
openclaw onboard --install-daemon
```

> [!info] 来源
> - [OpenClaw 安装与运行教程](https://juejin.cn/post/7605907293932847147) - 掘金
> - [OpenClaw 完整部署指南](https://baijiahao.baidu.com/s?id=1856027674234615671) - 百度百家号

### 1.2 配置向导步骤

**步骤 1：选择 AI 模型提供商**

```
? 选择你的 AI 模型提供商:
  ❯ Anthropic Claude (推荐)
    OpenAI GPT-4
    DeepSeek (国内推荐)
    阿里云百炼
    本地模型 (Ollama)
```

**步骤 2：输入 API Key**

```
? 请输入你的 API Key: sk-ant-xxxxxxxxxxxxx
```

**步骤 3：设置网关端口**

```
? 设置网关端口 (默认 18789): 18789
```

**步骤 4：配置数据目录**

```
? 设置数据目录 (默认 ~/.openclaw): ~/.openclaw
```

---

## 二、终端命令配置（推荐进阶用户）

### 2.1 配置文件位置

OpenClaw 的所有配置都集中在一个 JSON 文件中：

| 操作系统 | 配置文件路径 |
|----------|--------------|
| Windows | `C:\Users\你的用户名\.openclaw\openclaw.json` |
| macOS/Linux | `~/.openclaw/openclaw.json` |

> [!info] 来源
> - [OpenClaw 第三方 API 接入实战](https://blog.csdn.net/zhouzongxin94/article/details/158544866) - CSDN
> - [OpenClaw 配置大模型API](https://m.blog.csdn.net/qq_39329902/article/details/157542782) - CSDN

### 2.2 命令行快速配置

#### 查看当前配置

```bash
# 查看所有配置
openclaw config list

# 查看特定配置
openclaw config get models.providers
```

#### 配置 DeepSeek（推荐国内用户）

```bash
# 设置 DeepSeek API
openclaw config set models.providers.deepseek '{
  "baseUrl": "https://api.deepseek.com/v1",
  "apiKey": "sk-your-deepseek-api-key",
  "api": "openai-completions",
  "models": [
    {"id": "deepseek-chat", "name": "DeepSeek Chat (V3)"}
  ]
}'

# 设置默认模型
openclaw config set agents.defaults.model.primary "deepseek-chat"

# 重启服务生效
openclaw restart
```

#### 配置阿里云百炼

```bash
# 设置阿里云百炼 API
openclaw config set models.providers.qwen '{
  "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
  "apiKey": "sk-your-qwen-api-key",
  "api": "openai-completions",
  "models": [
    {"id": "qwen-max", "name": "Qwen Max"}
  ]
}'

openclaw config set agents.defaults.model.primary "qwen-max"
openclaw restart
```

#### 配置 Anthropic Claude

```bash
# 设置 Claude API
openclaw config set models.providers.anthropic '{
  "baseUrl": "https://api.anthropic.com/v1",
  "apiKey": "sk-ant-your-api-key",
  "api": "anthropic-completions",
  "models": [
    {"id": "claude-sonnet-4", "name": "Claude Sonnet 4"}
  ]
}'

openclaw config set agents.defaults.model.primary "claude-sonnet-4"
openclaw restart
```

> [!info] 来源
> - [OpenClaw 使用 DeepSeek API 配置教程](https://juejin.cn/post/7605419006682791978) - 掘金
> - [OpenClaw 国内大模型配置指南](https://blog.csdn.net/weixin_45110225/article/details/157724298) - CSDN

### 2.3 手动编辑配置文件

如果命令行配置不方便，也可以直接编辑 JSON 文件：

```bash
# 1. 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# 2. 编辑配置文件
nano ~/.openclaw/openclaw.json  # Linux/macOS
# 或
notepad C:\Users\你的用户名\.openclaw\openclaw.json  # Windows
```

**配置文件示例**：

```json
{
  "models": {
    "providers": {
      "deepseek": {
        "baseUrl": "https://api.deepseek.com/v1",
        "apiKey": "sk-your-api-key",
        "api": "openai-completions",
        "models": [
          {"id": "deepseek-chat", "name": "DeepSeek Chat"}
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek-chat"
      }
    }
  },
  "gateway": {
    "port": 18789
  }
}
```

---

## 三、验证配置

### 3.1 检查配置状态

```bash
# 综合诊断
openclaw doctor

# 查看服务状态
openclaw status

# 查看日志
openclaw logs
```

> [!info] 来源
> - [OpenClaw 常用命令速查](https://m.blog.csdn.net/u011701632/article/details/158458451) - CSDN
> - [OpenClaw 部署教程](https://m.blog.csdn.net/qq_39183034/article/details/157911457) - CSDN

### 3.2 测试对话

```bash
# 启动网关
openclaw gateway

# 访问 Web 控制台
# 浏览器打开 http://localhost:18789
```

或在终端直接测试：

```bash
# 发送测试消息
echo "你好，请用一句话介绍你自己" | openclaw chat
```

---

## 四、常见配置场景

### 4.1 配置 ClawHub 镜像（国内用户）

```bash
# 设置阿里云镜像源
openclaw config set clawhub.mirror "https://mirror.aliyun.com/clawhub/"

# 设置淘宝 npm 镜像
npm config set registry https://registry.npmmirror.com
```

### 4.2 配置本地模型（Ollama）

```bash
# 安装 Ollama
brew install ollama  # macOS
# 或
curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# 拉取模型
ollama pull qwen2.5:7b

# 配置 OpenClaw 使用本地模型
openclaw config set models.providers.ollama '{
  "baseUrl": "http://localhost:11434/api/chat",
  "models": [
    {"id": "qwen2.5:7b", "name": "Qwen 2.5 7B"}
  ]
}'
```

### 4.3 配置多模型（混合使用）

```bash
# 主力用 DeepSeek（便宜）
openclaw config set agents.defaults.model.primary "deepseek-chat"

# 复杂任务用 Claude（质量）
openclaw config set agents.defaults.model.reasoning "claude-sonnet-4"
```

---

## 五、最佳实践

### 配置管理建议

| 建议 | 说明 |
|------|------|
| **备份配置** | 修改前先备份 `openclaw.json` |
| **使用环境变量** | API Key 不要硬编码，使用环境变量 |
| **测试后再生产** | 先在测试环境验证配置 |
| **定期更新** | 保持 OpenClaw 和模型版本最新 |

### 安全建议

```bash
# 设置配置文件权限（仅自己可读写）
chmod 600 ~/.openclaw/openclaw.json  # Linux/macOS

# 使用环境变量存储敏感信息
export OPENCLAW_API_KEY="sk-your-api-key"
```

> [!info] 来源
> - [OpenClaw 环境部署与配置全指南](https://developer.baidu.com/article/detail.html?id=5925806) - 百度开发者
> - [OpenClaw 安全配置指南](https://www.cnblogs.com/RUIOVO/p/19595389) - 博客园

---

## 六、故障排查

### 6.1 常见问题

**Q1：配置后无法使用大模型？**

```bash
# 检查 API Key 是否正确
openclaw config get models.providers.deepseek.apiKey

# 测试 API 连通性
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json"
```

**Q2：配置文件格式错误？**

```bash
# 验证 JSON 格式
cat ~/.openclaw/openclaw.json | jq .

# 恢复备份
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
```

**Q3：端口被占用？**

```bash
# 查找占用端口的进程
lsof -i :18789  # Linux/macOS
netstat -ano | findstr :18789  # Windows

# 更换端口
openclaw config set gateway.port 8080
```

> [!info] 来源
> - [OpenClaw 常见问题解答](https://www.appinn.com/openclaw-common-commands/) - 小众软件
> - [OpenClaw 问题排查指南](https://m.blog.csdn.net/jsw110/article/details/157871097) - CSDN

---

## 个人笔记
> [!personal] 💡 我的理解与感悟
>
> 1. **配置是核心**：OpenClaw 安装很容易，配置才是关键一步
>
> 2. **国内用户建议**：
> >    - 优先用 DeepSeek（便宜、稳定）
> >    - 配置镜像源加速下载
> >    - API Key 从官网获取，不要用第三方
>
> 3. **踩坑记录**：
> >    - 修改配置后记得 `openclaw restart` 重启服务
> >    - API Key 格式要正确，包含 `sk-` 前缀
> >    - 本地模型需要足够的显存（7B 模型至少 8GB）
>
> 4. **进阶技巧**：
> >    - 可以配置多个模型，按需切换
> >    - 使用 `openclaw doctor` 快速诊断问题
> >    - 定期备份配置文件

---

## 相关文档
- [[../入门层/OpenClaw安装教程]] - OpenClaw 安装指南
- [[../应用层/OpenClaw对接第三方软件指南]] - 第三方软件对接
- [[../应用层/OpenClaw数字人商业调查]] - 商业应用调研

---

## 参考资料

### 官方资源
- [OpenClaw 官方文档](https://docs.openclaw.ai/zh-CN/start/getting-started) - 快速开始指南
- [OpenClaw GitHub 仓库](https://github.com/openclaw/openclaw) - 源代码和文档
- [OpenClaw 中文社区](https://www.moltcn.com) - 中文官方社区

### 教程参考
- [OpenClaw 保姆级安装配置教程](https://m.blog.csdn.net/liwang0113/article/details/157579187) - CSDN
- [OpenClaw 安装教程（Windows+Linux）](https://www.cnblogs.com/RUIOVO/p/19595389) - 博客园
- [OpenClaw 完整安装教程](https://m.blog.csdn.net/2401_82786637/article/details/158570745) - CSDN
- [OpenClaw 完全配置指南](https://m.blog.csdn.net/qq_39679118/article/details/158155191) - CSDN

### 命令参考
- [OpenClaw 常用命令速查手册](https://m.blog.csdn.net/qq_44866828/article/details/158266497) - CSDN
- [OpenClaw CLI 所有命令整理](https://m.blog.csdn.net/qq_42618566/article/details/158239577) - CSDN
- [OpenClaw 最常用命令](https://m.blog.csdn.net/u011701632/article/details/158458451) - CSDN

### API 配置
- [OpenClaw 使用 DeepSeek API 配置](https://juejin.cn/post/7605419006682791978) - 掘金
- [OpenClaw 国内大模型配置指南](https://blog.csdn.net/weixin_45110225/article/details/157724298) - CSDN
- [OpenClaw 配置大模型API](https://m.blog.csdn.net/qq_39329902/article/details/157542782) - CSDN

### 服务提供商
- [DeepSeek 官网](https://www.deepseek.com) - 获取 DeepSeek API Key
- [阿里云百炼](https://bailian.console.aliyun.com) - 获取 Qwen API Key
- [Anthropic 官网](https://console.anthropic.com) - 获取 Claude API Key
- [Ollama 官网](https://ollama.ai) - 本地模型运行

---

**最后更新**：2026-03-03
