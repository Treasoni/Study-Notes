## 第 4 章：环节三——让 Claude Code 接入本地 Ollama

上一章的 `ollama run` 让你能在终端里跟本地模型对话，但那只是「纯聊天」。现在进入环节三：把 Claude Code——面向 AI 编程的 CLI 助手——接到你本地的 Ollama 上。从此写代码、改 bug 都走本地推理，数据不出本机。

### 前提：版本与安装

要让 Claude Code 直连本地 Ollama，靠的是 Ollama 自带的 **Anthropic Messages API 兼容端点**（原生支持，无需第三方代理），但有版本门槛：

| 前提 | 要求 |
|------|------|
| Ollama 版本 | v0.14.0+（v0.15.0+ 另有 `ollama launch` 一键命令，下文会讲） |
| Claude Code | 已安装即可 |

Claude Code 的安装命令按系统选一种：

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

装好之后，终端里就能直接用 `claude` 命令了。

> [!tip] 大白话：ANTHROPIC_BASE_URL 是什么
> 把 Claude Code 想成寄信人，它默认把「请求信」寄到 Anthropic 官方服务器（出国）。`ANTHROPIC_BASE_URL` 就是「改地址」——把收件地址改成 `http://localhost:11434`，信就投进你本机的 Ollama 邮箱。所以设了这个变量，Claude Code 的一切请求都不再出国，只在你自己电脑里打转。

### 环境变量配置（核心）

接入的关键是四个环境变量，其中前三个**一个都不能错**：

| 变量 | 填什么 | 为什么 |
|------|--------|--------|
| `ANTHROPIC_BASE_URL` | `http://localhost:11434`（**不要加 `/v1` 后缀或尾斜杠**） | Claude Code 会自己在后面拼 `/v1/messages`，加多了反而 404 |
| `ANTHROPIC_AUTH_TOKEN` | `ollama`（任意非空值） | Ollama 端要求这个字段存在但内容被忽略，只作占位 |
| `ANTHROPIC_API_KEY` | **必须显式空字符串 `""`**（不是不设置） | 防止回落官方认证，见下方大白话 |
| `ANTHROPIC_MODEL` | 本地模型名（如 `qwen3-coder`） | 等价于启动时 `claude --model <名>` |

> [!tip] 大白话：为什么 API_KEY 要设空串
> 把 Anthropic 官方认证想成一张「门禁卡」。Claude Code 默认会先去刷官方门禁；如果你只是「不设置」`ANTHROPIC_API_KEY`，它手里可能还残留旧卡，就会反复尝试走官方认证、一直要求你登录。显式设成空串 `""` 等于「把旧卡没收」，逼它只能走 `ANTHROPIC_BASE_URL` 指的那个本机门。所以空串不是没意义，而是故意把官方通道关掉。

### 两种配置命令：Bash 与 PowerShell

**macOS / Linux（Bash/Zsh）**，在终端临时生效：

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
export ANTHROPIC_API_KEY=""
claude --model qwen3-coder
```

**Windows（PowerShell）**，写法对应改写：

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_AUTH_TOKEN = "ollama"
$env:ANTHROPIC_API_KEY = ""
claude --model qwen3-coder
```

这样启动后，`claude` 就会去连本机 Ollama 上的 `qwen3-coder` 模型。

### 一键方式：`ollama launch claude`（v0.15+）

如果你装的是 v0.15.0+ 的 Ollama，可以更省事——让 Ollama 自动选模型并直接拉起 Claude Code：

```bash
ollama launch claude                        # 自动选模型并启动
ollama launch claude --model qwen3-coder    # 指定模型
ollama launch claude --model gpt-oss:20b --yes -- -p "..."   # 非交互直接给提示词
```

### 持久化配置（推荐）

export 的方式只在当前终端窗口生效，新开一个终端就失效。想一劳永逸，把配置写进 `~/.claude/settings.json`（Windows 为 `%USERPROFILE%\.claude\settings.json`）的 `env` 块，新终端、后台 agent 都会自动生效：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://localhost:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "ANTHROPIC_API_KEY": "",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

其中 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` 用来进一步关闭非必要外联，让流量更干净地留在本机。

### 工作原理：数据不出本机

配好之后，请求链路是这样的：

```
Claude Code → http://localhost:11434/v1/messages → Ollama → 本地模型推理
```

- 端点：`POST http://localhost:11434/v1/messages`，这是 Ollama 实现的 Anthropic Messages API
- 全程只在本机回环地址 `localhost` 上传输，**数据不出本机**
- 支持：`messages`（含 image / tool_use / tool_result / thinking）、`stream`、`tools`
- 不支持：`tool_choice`、`metadata`、`count_tokens`、`batches`、prompt caching、PDF 等

### 模型选型与硬件

连哪个模型，直接决定 Claude Code 好不好用：

| 模型 | 说明 |
|------|------|
| `qwen3-coder` | 官方推荐的编码模型（30B，至少 24GB 显存） |
| `gpt-oss:20b` | 官方推荐 |
| `glm-4.7:cloud` | 云端模型，免下载 |

- **上下文**：至少 32K，处理大仓库建议 64K：`OLLAMA_CONTEXT_LENGTH=64000 ollama serve`
- **工具调用**：小模型（如 `gemma3:4b`、多数 7B）工具调用弱甚至缺失，会让 Claude Code 退化成纯文本生成器；量化档不建议低于 Q4_K_M
- **硬件预期**：本地推理「慢」是常态，先把预期放低，链路跑通再谈体验

### 备选方案对比（何时才需要）

官方原生方案是主线，多数人用不上备选。以下两个方案在「Ollama 版本过旧、对接非 Ollama 引擎、需要多供应商路由」时才需要考虑：

| 方案 | 用途 | 关键要点 |
|------|------|---------|
| claude-code-router | 多提供商路由 / 会话内 `/model` 切换 | 拦截请求按 model 字段转发；新版：`npm i -g @musistudio/claude-code-router && ccr ui` |
| LiteLLM | Anthropic ⇄ OpenAI 协议翻译代理 | 必须用 `ollama_chat/` 前缀（不是 `ollama/`）+ `drop_params: true`；`ANTHROPIC_BASE_URL=http://localhost:4000` |

判断标准：只要你的 Ollama ≥ v0.14，且只需要连本地模型，就用官方原生方案；要切换多家云端厂商、或接 LM Studio / vLLM 时，再引入备选。

### 接入环节常见坑

| 症状 | 解决办法 |
|------|---------|
| 模型 404 | `ollama ls` 查确切模型名；`ANTHROPIC_BASE_URL` 不带 `/v1` 或尾斜杠 |
| 一直要求登录 | 把凭据写进 `~/.claude/settings.json` 的 env 或 shell export，且 `ANTHROPIC_API_KEY=""` |
| 上下文不足 | `OLLAMA_CONTEXT_LENGTH=64000 ollama serve`；会话内 `/compact` |
| 工具调用失败 | 换编码向/工具向模型（`qwen3-coder`、`gpt-oss`、GLM-4）；量化不低于 Q4_K_M |
| Connection refused | 先确认 `ollama serve` 在跑；端口冲突改 `OLLAMA_HOST` 并同步改 base URL |
| VS Code 扩展不生效 | 在 VS Code 用户设置 `claudeCode.environmentVariables` 里配置 |

### 本章小结

- 前提是 Ollama v0.14.0+，提供原生 Anthropic Messages API 兼容端点；Claude Code 安装：Windows 用 `irm`，macOS/Linux 用 `curl`
- 核心是四个环境变量：`ANTHROPIC_BASE_URL` 不带 `/v1`、`ANTHROPIC_AUTH_TOKEN=ollama` 占位、`ANTHROPIC_API_KEY=""` 必须显式空串、`ANTHROPIC_MODEL` 指定模型
- v0.15+ 可 `ollama launch claude` 一键接入；推荐把配置持久化到 `~/.claude/settings.json` 的 env 块
- 请求全程走 `localhost:11434/v1/messages`，数据不出本机；但注意它不支持 prompt caching、PDF 等高级特性
- 编码干活选 `qwen3-coder`（30B / 24GB+ 显存）或 `gpt-oss:20b`；上下文给足 32K-64K，量化别低于 Q4_K_M
- 备选方案（claude-code-router / LiteLLM）只在 Ollama 过旧或对接非 Ollama 引擎时才需要

### 下一章预告

三环节已经逐个打通。下一章把这些步骤串成一条完整命令流，从零开始一路跑到 Claude Code 起来，并给出入门选型建议——先用 7B 模型跑通链路，再按显存升级编码模型。
