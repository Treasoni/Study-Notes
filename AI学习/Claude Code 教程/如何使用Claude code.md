---
tags: [ai, 工具使用]
---

# Claude Code 使用指南

> [!info] 文档定位
> **日常操作速查手册** - 装好就能用，用的时候查。更适合中国宝宝体质的配置方案。
>
> 功能速查 → [[Claude Code 常用功能]] · CLI 命令参考 → [[Claude Code CLI 完整参考]]

---

## 一、快速安装

### 1️⃣ 一行命令安装（推荐）

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows CMD
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

> [!tip] 原生安装器优势
> - 自动更新 · 无需 Node.js · 体积约 60-80MB
> - 安装后执行 `claude --version` 验证，当前最新为 **v2.1.131**（2026-05-06）

### 2️⃣ 其他安装方式（备选）

| 平台 | 命令 | 更新方式 |
|------|------|---------|
| macOS Homebrew | `brew install --cask claude-code` | 手动 `brew upgrade claude-code` |
| Windows WinGet | `winget install Anthropic.ClaudeCode` | 手动 |
| ~~npm（已废弃）~~ | ~~`npm install -g @anthropic-ai/claude-code`~~ | 不推荐 |

### 3️⃣ 前置依赖

| 要求 | 说明 |
|------|------|
| **Git** | Claude Code 版本控制依赖，需安装并配置 `git config --global user.name/email` |
| **Node.js** | 仅废弃的 npm 方式需要 v18+，**原生安装器不需要** |
| **RAM** | 最低 4GB，推荐 8GB |

> [!tip] 企业代理注意
> v2.1.116+ 从 `https://downloads.claude.ai/claude-code-releases` 下载二进制文件，需将该域名加入代理白名单。

> [!info] 📚 来源
> - [GitHub 官方仓库](https://github.com/anthropics/claude-code) · [GitHub Releases](https://github.com/anthropics/claude-code/releases)
> - [Homebrew Cask](https://github.com/Homebrew/homebrew-cask) · [全平台安装指南](https://www.morphllm.com/install-claude-code)

---

## 二、跳过登录（免认证启动）

Claude Code **没有** `--no-auth` 参数，但有 4 种方式跳过 OAuth 登录：

### 方式一：apiKeyHelper ⭐ 官方推荐

在 `~/.claude/settings.json` 中配置 API Key 辅助脚本路径：

```json
{
  "apiKeyHelper": "/Users/你的用户名/.claude/api-key-helper.sh"
}
```

该脚本内容只需输出你的 API Key：

```bash
#!/bin/bash
echo "sk-ant-你的API密钥"
```

> [!warning] 注意
> - **不要**同时设置 `ANTHROPIC_API_KEY` 环境变量（会冲突）
> - 删除 `~/.claude.json` 中的 `oauthAccount` 条目
> - 如果嫌创建脚本麻烦，直接用下面的 `primaryApiKey` 方式，纯 JSON 一步到位

### 方式二：primaryApiKey ⭐ 直接配置

```json
{
  "primaryApiKey": "sk-ant-你的API密钥",
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

> **permissions 可选值**：
> - `"bypassPermissions"` — 自动批准所有操作（YOLO 模式）
> - `"acceptEdits"` — 仅自动批准文件编辑
> - `"default"` — 每次操作都询问

### 方式三：env 字段（走第三方 API，无需命令行）

不用每次 export，直接在 `~/.claude/settings.json` 的 `env` 字段配好就行：

**使用 OpenRouter：**

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "sk-or-v1-你的密钥",
    "ANTHROPIC_MODEL": "anthropic/claude-3.5-sonnet",
    "ANTHROPIC_API_KEY": ""
  }
}
```

**使用本地模型（LiteLLM + Ollama）：**

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:8000/v1",
    "ANTHROPIC_AUTH_TOKEN": "sk-123",
    "ANTHROPIC_API_KEY": ""
  }
}
```

先启动桥接：`ollama pull qwen2.5-coder:7b && litellm --model ollama/qwen2.5-coder:7b --port 8000`

> [!warning] 协议兼容性
> - Claude Code 使用 **Anthropic `/v1/messages`** 协议
> - OpenRouter ✅ · LiteLLM ✅（自动转换） · **Ollama 直连 ❌**（必须通过 LiteLLM）
> - 模型**必须支持 Tool Use / Function Calling**

### 方式四：CC-Switch ⭐ 可视化方案

> 跨平台桌面应用，**50K+ Star**，支持 Claude Code / Codex / Gemini CLI / OpenCode 等工具的供应商切换，内置 50+ 平台预设。

**开发者**：[farion1231](https://github.com/farion1231/cc-switch) · **开源协议**：MIT

#### 安装

| 平台 | 命令 / 方式 |
|------|-------------|
| macOS | `brew tap farion1231/ccswitch && brew install --cask cc-switch` |
| Windows | GitHub Releases 下载 `.msi` 安装包 |
| Linux | DEB / RPM / AppImage 任选 |

#### 配置步骤

1. 打开 CC-Switch，选中 **Claude Code**
2. 点击右上角 **+** 号，在预设中选择你的平台（如 SiliconFlow、DeepSeek、智谱等）
3. 自动填入端点地址和模型映射，只需填写 **API Key**
4. 在首页点击「启用」即可生效

> [!tip] CC-Switch 优势
> - **热切换**：切换供应商**无需重启终端**，即时生效
> - **故障转移**：某家供应商宕机自动切到下一家
> - **用量统计**：Token 消耗追踪、成本监控、趋势图表
> - **MCP 统一管理**：一处编辑，同步到所有工具
> - **云同步**：支持 WebDAV / Dropbox / OneDrive 多设备同步

> [!warning] 注意
> 如果同时配置了环境变量或 `settings.json`，可能会产生冲突。建议使用 CC-Switch 后，清空其他配置项，避免互相覆盖。

---

## 三、配置文件（最常用配置合集）

配置文件位置：**`~/.claude/settings.json`**

### 完整配置模板（复制粘贴即可用）

```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-xxx",
      "defaultModel": "deepseek-chat"
    }
  },
  "defaultProvider": "deepseek",
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

### 支持的第三方平台

| 平台 | baseUrl | defaultModel |
|------|---------|--------------|
| 火山引擎 | `https://ark.cn-beijing.volces.com/v1` | `ep-xxxxx` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-max` |
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-plus` |
| Ollama | `http://localhost:11434/v1` | `llama3.2` |

> **配置优先级**：环境变量 > settings.json > 默认值

### 多平台一键切换（纯配置）

在 `settings.json` 配好多个 provider，改 `defaultProvider` 就行：

```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-xxx",
      "defaultModel": "deepseek-chat"
    },
    "volc": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "ep-xxxxx",
      "defaultModel": "ep-xxxxx"
    },
    "qwen": {
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "sk-xxx",
      "defaultModel": "qwen-max"
    }
  },
  "defaultProvider": "deepseek"
}
```

想换平台？把 `defaultProvider` 改成 `"volc"` 或 `"qwen"` 就行，保存后重启 Claude Code 生效。

### 取消代理

```json
{ "env": { "HTTP_PROXY": "", "HTTPS_PROXY": "" } }
```

> [!tip] 配置常见坑
> - JSON 格式错误、路径不对、环境变量覆盖 → 重启 Claude Code 生效
> - 切换 Provider 时同时改 `defaultProvider` 和对应 key

---

## 四、代理配置

### 推荐：settings.json 配置（永久）

在 `~/.claude/settings.json` 的 `env` 字段中配置：

```json
{
  "env": {
    "HTTP_PROXY": "http://127.0.0.1:7890",
    "HTTPS_PROXY": "http://127.0.0.1:7890"
  }
}
```

### 取消代理

```json
{ "env": { "HTTP_PROXY": "", "HTTPS_PROXY": "" } }
```

### 常用代理端口

| 软件 | 默认端口 |
|------|---------|
| Clash | 7890 |
| V2Ray | 10808 |
| Shadowsocks | 1080 |

---

## 五、日常使用速查

### 启动命令

| 命令 | 作用 |
|------|------|
| `claude` | 启动交互会话 |
| `claude --model claude-sonnet-4` | 指定模型启动 |
| `claude -m deepseek-chat` | 使用第三方模型 |
| `claude --print < prompt.txt` | 非交互模式（自动化/CI） |
| `claude --version` | 查看版本 |
| `claude --debug` | 调试模式 |

### 会话中常用 `/` 命令

| 命令 | 作用 |
|------|------|
| `/model` | 切换模型（列出可选） |
| `/model claude-opus-4` | 直接切换到指定模型 |
| `/status` | 查看当前模型/状态 |
| `/new` | 创建新会话 |
| `/new my-project` | 创建命名会话 |
| `/resume` | 列出历史会话 |
| `/resume my-session` | 恢复特定会话 |
| `/clear` | 清除当前会话 |
| `/context` | 显示 token 消耗 |
| `/help` | 帮助 |
| `/mcp` | 查看 MCP 列表 |

### MCP 管理

```bash
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path
claude mcp list         # 查看所有
claude mcp remove fs    # 删除
claude mcp enable fs    # 启用
claude mcp disable fs   # 禁用
```

> 详细 MCP 教程 → [[03-进阶应用/Claude MCP 使用指南]]

### Skills 使用

```bash
/help              # 查看可用技能
/commit            # 提交代码
/review-pr 123     # 审查 PR
"帮我画一个流程图"   # 自然语言触发
```

> 了解 Skills → [[01-基础概念/Skills 是什么]] · 自定义技能 → [[03-进阶应用/如何编写Skills]]

---

## 六、CLAUDE.md

> **项目级记忆文件**，Claude Code 启动时自动读取，定义项目规范、工作流、禁止事项。

```markdown
# CLAUDE.md
## 项目概述
一句话描述

## 常用命令
- npm run dev - 启动开发
- npm test - 运行测试

## 代码规范
- 使用 ESLint + Prettier
- 组件命名 PascalCase

## 禁止事项
- 不要修改 package-lock.json
```

| 文件 | 位置 | 作用域 | 提交到 Git |
|------|------|--------|------------|
| `CLAUDE.md` | 项目根目录 | 项目级 | ✅ |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | ❌ |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | ❌ |

```bash
# 自动生成（推荐）
claude
/init
```

> 完整指南 → [[03-进阶应用/CLAUDE.md 使用指南]]

---

## 七、常见问题与坑

### 安装问题

#### Windows 原生安装后找不到命令

> [!warning] 问题现象
> 安装成功但运行 `claude --help` 报错"无法识别为 cmdlet"

> [!tip] 原因
> 原生安装器安装到了 `C:\Users\你的用户名\.local\bin`，但该路径未加入 PATH 环境变量

**解决方法**：

1. **复制路径**：`C:\Users\你的用户名\.local\bin`

2. **打开环境变量设置**：
   - 按 `Win` 键，搜索"环境变量"
   - 点击"编辑系统环境变量"

3. **添加 PATH**：
   - 点击"环境变量..."
   - 在"用户变量"中选中 `Path`，点击"编辑"
   - 点击"新建"，粘贴上述路径
   - 确认保存

4. **重启 PowerShell**：关闭当前窗口，重新打开后即可使用

---

#### Windows 安装时报 ECONNREFUSED

> [!warning] 问题现象
> 安装失败，提示 `ECONNREFUSED`
> ```
> × Installation failed
> Failed to fetch version from https://downloads.claude.ai/claude-code-releases/latest
> ```

> [!tip] 原因
> 网络连接被拒绝，通常是代理软件未接管命令行流量

**解决方法**：为 PowerShell 设置临时代理

```powershell
# 设置代理（将 7890 替换为你的代理端口）
$env:HTTP_PROXY="http://127.0.0.1:7890"
$env:HTTPS_PROXY="http://127.0.0.1:7890"

# 重新运行安装
irm https://claude.ai/install.ps1 | iex
```

> [!tip] 备选方案
> 把代理软件切换为全局模式

> [!info] 常用代理端口
> - Clash：7890
> - V2Ray：10809
> - Shadowsocks：1080

### 代理问题

| 问题 | 解决 |
|------|------|
| 设置了系统代理但终端连不上 | 终端需单独设 `HTTP_PROXY`/`HTTPS_PROXY` 环境变量 |
| settings.json 的代理不生效 | 环境变量优先级更高，先 `echo $HTTP_PROXY` 检查 |
| 代理速度慢 | 切换节点或检查网络质量 |
| 临时取消代理 | `unset HTTP_PROXY HTTPS_PROXY` |

### MCP 问题

| 问题 | 解决 |
|------|------|
| MCP 连接失败 | 确认 `npx` 已安装、命令正确、环境变量已设置 |
| 手动测试 | `npx -y @modelcontextprotocol/server-filesystem /test/path` |

### 其他

| 问题 | 解决 |
|------|------|
| 配置不生效 | 路径？JSON 格式？环境变量覆盖？重启 Claude Code？ |
| 模型切换失败 | 模型名称不正确？平台不支持？API Key 无效？ |

### 安全建议

```bash
# 把敏感文件加入 .gitignore
.env
.mcp.json
settings.json
```

> MCP vs Skills 区别 → [[Claude MCP 使用指南]] 提供工具，[[Skills 是什么]] 提供任务模板

---

## 八、关联文档

[[Agent智能体]] · [[Claude Code 常用功能]] · [[Claude Code CLI 完整参考]] · [[Claude Code 会话管理]] · [[Claude Code 模型与推理设置]] · [[Claude MCP 使用指南]] · [[CLAUDE.md 使用指南]] · [[Subagents 完整指南]] · [[如何编写Skills]] · [[Skills 是什么]] · [[人工智能重要的六大概念体系]] · [[Git 入门教程]] · [[Git 命令速查]]

---

## 参考资料

### 官方
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [GitHub 仓库](https://github.com/anthropics/claude-code)
- [Auto Mode 官方博客](https://www.anthropic.com/engineering/claude-code-auto-mode)

### 社区
- [claude-howto 学习指南](https://github.com/luongnv89/claude-howto)（21,800+ ⭐）
- [安装指南](https://www.morphllm.com/install-claude-code)
- [第三方 API 免登录配置](https://www.xugj520.cn/archives/windows-claude-code-api-setup-no-login.html)

### 跳过认证
- [apiKeyHelper 用法](https://github.com/lbjlaq/Antigravity-Manager/issues/362)
- [Desktop Developer Mode](https://developer.aliyun.com/article/1731254)
- [settings.json 详解](https://blog.csdn.net/tirestay/article/details/158808038)
