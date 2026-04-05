---
tags: [ai, 工具使用, cli, claude-code]
created: 2026-04-05
updated: 2026-04-05
---

# Claude Code CLI 完整参考

> [!info] 概述
> **一句话定义**：Claude Code CLI 是在终端中与 Claude 交互的命令行工具，支持交互式会话和脚本化自动化两种模式。
> **🎯 比喻**：就像一个住在终端里的 AI 编程助手，既能和你聊天对话，也能像 Unix 管道一样处理自动化任务。

## 核心概念

### 是什么

Claude Code CLI（Command Line Interface）是与 Claude Code 交互的主要方式，提供强大的选项来运行查询、管理会话、配置模型，并将 Claude 集成到开发工作流中。

### 为什么需要

- **终端原生**：无需离开命令行即可使用 AI
- **脚本化**：支持管道操作，可集成到 CI/CD
- **灵活模式**：交互式 REPL 和非交互式 Print 模式
- **完整控制**：精细的权限、工具、模型配置

### 通俗理解

**🎯 比喻**：
- **交互模式**：像和一个坐在旁边的程序员对话，多轮交流
- **Print 模式**：像 Unix 管道命令，输入→处理→输出，一锤子买卖

**📦 架构图**：
```
┌─────────────────┐     "claude [options] [query]"     ┌──────────────────┐
│  User Terminal  │ ─────────────────────────────────▶ │ Claude Code CLI  │
└─────────────────┘                                    └──────────────────┘
                                                              │
                           ┌──────────────────────────────────┼──────────────────────────────────┐
                           │                                  │                                  │
                           ▼                                  ▼                                  ▼
                    ┌─────────────┐                    ┌─────────────┐                    ┌─────────────┐
                    │ REPL Mode   │                    │ Print Mode  │                    │  Resume     │
                    │ (Interactive)│                   │ (SDK/Script)│                    │  Session    │
                    └─────────────┘                    └─────────────┘                    └─────────────┘
                           │                                  │                                  │
                           └──────────────────────────────────┼──────────────────────────────────┘
                                                              ▼
                                                      ┌───────────────┐
                                                      │  Claude API   │
                                                      └───────────────┘
                                                              │
                                                              ▼
                                                      ┌───────────────┐
                                                      │    Output     │
                                                      │ text/json/    │
                                                      │ stream-json   │
                                                      └───────────────┘
```

---

## 两种核心模式

### 交互模式（Interactive Mode）

**默认模式**，启动多轮对话会话。

```bash
# 启动交互会话
claude

# 带初始提示启动
claude "解释这个项目的认证流程"

# 带命名启动
claude -n "auth-refactor" "开始重构认证模块"
```

**特点**：
- ✅ 多轮对话
- ✅ Tab 补全
- ✅ 历史记录
- ✅ 斜杠命令
- ✅ 实时交互

### Print 模式（非交互）

**脚本化模式**，单次查询后退出。

```bash
# 单次查询
claude -p "这个函数做什么的？"

# 处理管道内容
cat error.log | claude -p "解释这个错误"

# 链式处理
claude -p "列出待办事项" | grep "紧急"
```

**特点**：
- ✅ 单次查询
- ✅ 可脚本化
- ✅ 支持管道
- ✅ JSON 输出
- ✅ 适合 CI/CD

**模式对比图**：
```
                    claude
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    ┌───────────┐           ┌───────────┐
    │  默认     │           │  -p 标志  │
    │ 交互模式  │           │ Print模式 │
    └───────────┘           └───────────┘
          │                       │
          ▼                       ▼
    ┌───────────┐           ┌───────────┐
    │多轮对话   │           │单次查询   │
    │Tab补全    │           │可脚本化   │
    │历史记录   │           │支持管道   │
    │斜杠命令   │           │JSON输出   │
    └───────────┘           └───────────┘
```

---

## CLI 命令速查

### 基础命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `claude` | 启动交互式 REPL | `claude` |
| `claude "query"` | 带初始提示启动 | `claude "解释这个项目"` |
| `claude -p "query"` | Print 模式，查询后退出 | `claude -p "解释这个函数"` |
| `cat file \| claude -p "query"` | 处理管道内容 | `cat logs.txt \| claude -p "解释"` |
| `claude -c` | 继续最近的对话 | `claude -c` |
| `claude -c -p "query"` | Print 模式继续 | `claude -c -p "检查类型错误"` |
| `claude -r "<session>" "query"` | 按ID或名称恢复会话 | `claude -r "auth-refactor" "完成这个PR"` |
| `claude update` | 更新到最新版本 | `claude update` |

### 管理命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `claude mcp` | 配置 MCP 服务器 | 详见 MCP 文档 |
| `claude mcp serve` | 将 Claude Code 作为 MCP 服务器运行 | `claude mcp serve` |
| `claude agents` | 列出所有配置的子代理 | `claude agents` |
| `claude auto-mode defaults` | 打印自动模式默认规则（JSON） | `claude auto-mode defaults` |
| `claude remote-control` | 启动远程控制服务器 | `claude remote-control` |
| `claude plugin` | 管理插件（安装、启用、禁用） | `claude plugin install my-plugin` |

### 认证命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `claude auth login` | 登录（支持 `--email`、`--sso`） | `claude auth login --email user@example.com` |
| `claude auth logout` | 登出当前账户 | `claude auth logout` |
| `claude auth status` | 检查认证状态（已登录返回0，未登录返回1） | `claude auth status` |

> [!info] 📚 来源
> - [Claude Code 官方文档 - Quickstart](https://code.claude.com/docs/en/quickstart)
> - [GitHub - claude-howto CLI Reference](https://github.com/luongnv89/claude-howto/tree/main/10-cli)

---

## 核心标志（Flags）

### 会话管理

| 标志 | 描述 | 示例 |
|------|------|------|
| `-p, --print` | Print 模式，非交互输出 | `claude -p "query"` |
| `-c, --continue` | 加载最近的对话 | `claude --continue` |
| `-r, --resume` | 按ID或名称恢复特定会话 | `claude --resume auth-refactor` |
| `-n, --name` | 会话显示名称 | `claude -n "auth-refactor"` |
| `--session-id` | 使用特定会话ID（UUID） | `claude --session-id "550e8400-..."` |
| `--fork-session` | 恢复时创建新会话 | `claude --resume abc123 --fork-session` |

### 项目与工作区

| 标志 | 描述 | 示例 |
|------|------|------|
| `-w, --worktree` | 在隔离的 git worktree 中启动 | `claude -w` |
| `--add-dir` | 添加额外的工作目录 | `claude --add-dir ../apps ../lib` |
| `--from-pr <number>` | 恢复与 GitHub PR 关联的会话 | `claude --from-pr 42` |

### 远程与协作

| 标志 | 描述 | 示例 |
|------|------|------|
| `--remote "task"` | 在 claude.ai 创建 Web 会话 | `claude --remote "实现 API"` |
| `--remote-control, --rc` | 带远程控制的交互会话 | `claude --rc` |
| `--teleport` | 在本地恢复 Web 会话 | `claude --teleport` |
| `--teammate-mode` | 代理团队显示模式 | `claude --teammate-mode tmux` |

### 模式控制

| 标志 | 描述 | 示例 |
|------|------|------|
| `--bare` | 最小模式（跳过 hooks、skills、plugins、MCP、auto memory、CLAUDE.md） | `claude --bare` |
| `--enable-auto-mode` | 解锁自动权限模式 | `claude --enable-auto-mode` |
| `--disable-slash-commands` | 禁用所有 skills 和斜杠命令 | `claude --disable-slash-commands` |
| `--no-session-persistence` | 禁用会话保存（Print 模式） | `claude -p --no-session-persistence "query"` |

---

## 模型配置

### 模型选择标志

| 标志 | 描述 | 示例 |
|------|------|------|
| `--model` | 设置模型（sonnet、opus、haiku 或完整名称） | `claude --model opus` |
| `--fallback-model` | 过载时自动回退模型 | `claude -p --fallback-model sonnet "query"` |
| `--agent` | 指定会话使用的代理 | `claude --agent my-custom-agent` |
| `--agents` | 通过 JSON 定义自定义子代理 | 详见代理配置 |
| `--effort` | 设置思考努力级别（low、medium、high、max） | `claude --effort high` |

### 可用模型

| 模型 | ID | 上下文窗口 | 说明 |
|------|-----|-----------|------|
| Opus 4.6 | `claude-opus-4-6` | 1M tokens | 最强大，支持自适应努力级别 |
| Sonnet 4.6 | `claude-sonnet-4-6` | 1M tokens | 平衡速度和能力 |
| Haiku 4.5 | `claude-haiku-4-5` | 1M tokens | 最快，适合快速任务 |

### 模型选择示例

```bash
# 使用简短名称
claude --model opus "设计缓存策略"
claude --model sonnet "实现这个功能"
claude --model haiku -p "格式化这个 JSON"

# 使用 opusplan 别名（Opus 规划，Sonnet 执行）
claude --model opusplan "设计并实现 API 缓存层"

# 使用完整模型名称
claude --model claude-sonnet-4-6-20250929 "审查这段代码"

# 带回退配置
claude -p --model opus --fallback-model sonnet "分析架构"
```

### 努力级别（Opus 4.6 专属）

```bash
# 通过 CLI 标志设置
claude --effort high "复杂审查"

# 通过斜杠命令设置
/effort high

# 通过环境变量设置
export CLAUDE_CODE_EFFORT_LEVEL=high   # low, medium, high, 或 max
```

> [!tip] ultrathink 关键词
> 在提示词中使用 "ultrathink" 可激活深度推理。`max` 努力级别仅 Opus 4.6 可用。

> [!info] 📚 来源
> - [Claude Code 官方文档](https://code.claude.com/docs/en/overview)
> - [GitHub - claude-howto Models](https://github.com/luongnv89/claude-howto/tree/main/10-cli#models)

---

## 系统提示词定制

### 标志对比

| 标志 | 行为 | 交互模式 | Print 模式 |
|------|------|---------|-----------|
| `--system-prompt` | 替换整个默认系统提示 | ✅ | ✅ |
| `--system-prompt-file` | 从文件加载提示 | ❌ | ✅ |
| `--append-system-prompt` | 追加到默认系统提示 | ✅ | ✅ |

### 使用示例

```bash
# 完全自定义角色
claude --system-prompt "你是一名资深安全工程师。专注于漏洞分析。"

# 追加特定指令
claude --append-system-prompt "代码示例始终包含单元测试"

# 从文件加载复杂提示（仅 Print 模式）
claude -p --system-prompt-file ./prompts/code-reviewer.txt "审查 main.py"
```

> [!warning] 注意
> `--system-prompt-file` 仅在 Print 模式下可用。交互模式请使用 `--system-prompt` 或 `--append-system-prompt`。

---

## 工具与权限管理

### 权限标志

| 标志 | 描述 | 示例 |
|------|------|------|
| `--tools` | 限制可用的内置工具 | `claude -p --tools "Bash,Edit,Read" "query"` |
| `--allowedTools` | 无需提示即可执行的工具 | `"Bash(git log:*)" "Read"` |
| `--disallowedTools` | 从上下文中移除的工具 | `"Bash(rm:*)" "Edit"` |
| `--dangerously-skip-permissions` | 跳过所有权限提示 | `claude --dangerously-skip-permissions` |
| `--permission-mode` | 以指定权限模式开始 | `claude --permission-mode auto` |
| `--permission-prompt-tool` | 用于权限处理的 MCP 工具 | `claude -p --permission-prompt-tool mcp_auth "query"` |
| `--enable-auto-mode` | 解锁自动权限模式 | `claude --enable-auto-mode` |

### 权限配置示例

```bash
# 只读模式代码审查
claude --permission-mode plan "审查这个代码库"

# 仅限安全工具
claude --tools "Read,Grep,Glob" -p "查找所有 TODO 注释"

# 允许特定 git 命令无需提示
claude --allowedTools "Bash(git status:*)" "Bash(git log:*)"

# 阻止危险操作
claude --disallowedTools "Bash(rm -rf:*)" "Bash(git push --force:*)"

# 安全意识开发
claude --permission-mode plan \
  --tools "Read,Grep,Glob" \
  "审计这个代码库的安全漏洞"

# 受限自动化
claude -p --max-turns 2 \
  --allowedTools "Read" "Glob" \
  "查找所有硬编码的凭证"
```

---

## 输出格式

### 输出标志

| 标志 | 描述 | 选项 | 示例 |
|------|------|------|------|
| `--output-format` | 指定输出格式（Print 模式） | `text`, `json`, `stream-json` | `claude -p --output-format json "query"` |
| `--input-format` | 指定输入格式（Print 模式） | `text`, `stream-json` | `claude -p --input-format stream-json` |
| `--verbose` | 启用详细日志 | | `claude --verbose` |
| `--include-partial-messages` | 包含流式事件 | 需要 `stream-json` | `claude -p --output-format stream-json --include-partial-messages "query"` |
| `--json-schema` | 获取匹配 schema 的验证 JSON | | `claude -p --json-schema '{"type":"object"}' "query"` |
| `--max-budget-usd` | Print 模式的最大花费 | | `claude -p --max-budget-usd 5.00 "query"` |

### 输出格式示例

```bash
# 纯文本（默认）
claude -p "解释这段代码"

# JSON 格式（程序化使用）
claude -p --output-format json "列出 main.py 中的所有函数"

# 流式 JSON（实时处理）
claude -p --output-format stream-json "生成一份长报告"

# 带 schema 验证的结构化输出
claude -p --json-schema '{"type":"object","properties":{"bugs":{"type":"array"}}}' \
  "找出这段代码的 bug 并以 JSON 返回"
```

### jq 解析示例

```bash
# 提取特定字段
claude -p --output-format json "分析这段代码" | jq '.result'

# 过滤数组元素
claude -p --output-format json "列出问题" | jq -r '.issues[] | select(.severity=="high")'

# 转换为 CSV
claude -p --output-format json "列出函数" | jq -r '.functions[] | [.name, .lineCount] | @csv'

# 条件处理
claude -p --output-format json "检查安全" | jq 'if .vulnerabilities | length > 0 then "不安全" else "安全" end'
```

---

## 会话管理

### 会话示例

```bash
# 继续上次对话
claude -c

# 恢复命名会话
claude -r "feature-auth" "继续实现登录功能"

# 分叉会话进行实验
claude --resume feature-auth --fork-session "尝试替代方案"

# 使用特定会话 ID
claude --session-id "550e8400-e29b-41d4-a716-446655440000" "继续"
```

### 会话分叉（Fork）

**用途**：
- 尝试替代实现而不丢失原始会话
- 并行实验不同方法
- 从成功的工作创建变体分支
- 测试破坏性更改而不影响主会话

```bash
# 分叉会话尝试不同方法
claude --resume abc123 --fork-session "尝试替代实现"

# 带自定义消息分叉
claude -r "feature-auth" --fork-session "测试不同架构"
```

> [!info] 📚 来源
> - [GitHub - claude-howto Session Management](https://github.com/luongnv89/claude-howto/tree/main/10-cli#session-management)

---

## 代理配置（Agents）

### 代理 JSON 格式

```json
{
  "agent-name": {
    "description": "必需：何时调用此代理",
    "prompt": "必需：代理的系统提示",
    "tools": ["可选", "工具", "数组"],
    "model": "可选：sonnet|opus|haiku"
  }
}
```

**必需字段**：
- `description` - 何时使用此代理的自然语言描述
- `prompt` - 定义代理角色和行为的系统提示

**可选字段**：
- `tools` - 可用工具数组（省略则继承所有）
- `model` - 使用的模型：`sonnet`、`opus` 或 `haiku`

### 完整代理示例

```json
{
  "code-reviewer": {
    "description": "专家代码审查员。代码更改后主动使用。",
    "prompt": "你是资深代码审查员。专注于代码质量、安全和最佳实践。",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "错误和测试失败的调试专家。",
    "prompt": "你是调试专家。分析错误、识别根因并提供修复。",
    "tools": ["Read", "Edit", "Bash", "Grep"],
    "model": "opus"
  },
  "documenter": {
    "description": "生成指南的文档专家。",
    "prompt": "你是技术写作人员。创建清晰、全面的文档。",
    "tools": ["Read", "Write"],
    "model": "haiku"
  }
}
```

### 代理命令示例

```bash
# 内联定义自定义代理
claude --agents '{
  "security-auditor": {
    "description": "漏洞分析安全专家",
    "prompt": "你是安全专家。发现漏洞并建议修复。",
    "tools": ["Read", "Grep", "Glob"],
    "model": "opus"
  }
}' "审计这个代码库的安全问题"

# 从文件加载代理
claude --agents "$(cat ~/.claude/agents.json)" "审查认证模块"

# 与其他标志组合
claude -p --agents "$(cat agents.json)" --model sonnet "分析性能"
```

### 代理优先级

1. **CLI 定义**（`--agents` 标志）- 会话特定
2. **用户级别**（`~/.claude/agents/`）- 所有项目
3. **项目级别**（`.claude/agents/`）- 当前项目

> [!info] 📚 来源
> - [GitHub - claude-howto Agents Configuration](https://github.com/luongnv89/claude-howto/tree/main/10-cli#agents-configuration)

---

## MCP 配置

### MCP 标志

| 标志 | 描述 | 示例 |
|------|------|------|
| `--mcp-config` | 从 JSON 加载 MCP 服务器 | `claude --mcp-config ./mcp.json` |
| `--strict-mcp-config` | 仅使用指定的 MCP 配置 | `claude --strict-mcp-config --mcp-config ./mcp.json` |
| `--channels` | 订阅 MCP 频道插件 | `claude --channels discord,telegram` |

### MCP 示例

```bash
# 加载 GitHub MCP 服务器
claude --mcp-config ./github-mcp.json "列出开放的 PR"

# 严格模式 - 仅使用指定服务器
claude --strict-mcp-config --mcp-config ./production-mcp.json "部署到预发布环境"
```

> [!tip] 详细说明
> 完整的 MCP 配置教程请参阅 [[03-进阶应用/Claude MCP 使用指南]]

---

## 高级功能

### 高级标志

| 标志 | 描述 | 示例 |
|------|------|------|
| `--chrome` | 启用 Chrome 浏览器集成 | `claude --chrome` |
| `--no-chrome` | 禁用 Chrome 浏览器集成 | `claude --no-chrome` |
| `--ide` | 如果可用，自动连接 IDE | `claude --ide` |
| `--max-turns` | 限制代理轮次（非交互） | `claude -p --max-turns 3 "query"` |
| `--debug` | 启用带过滤的调试模式 | `claude --debug "api,mcp"` |
| `--enable-lsp-logging` | 启用详细 LSP 日志 | `claude --enable-lsp-logging` |
| `--betas` | API 请求的 Beta 头 | `claude --betas interleaved-thinking` |
| `--init` / `--init-only` | 运行初始化 hooks | `claude --init` |
| `--maintenance` | 运行维护 hooks 并退出 | `claude --maintenance` |

### 高级示例

```bash
# 限制自主操作
claude -p --max-turns 5 "重构这个模块"

# 调试 API 调用
claude --debug "api" "测试查询"

# 启用 IDE 集成
claude --ide "帮我处理这个文件"
```

---

## 关键环境变量

| 变量 | 描述 |
|------|------|
| `ANTHROPIC_API_KEY` | 认证 API 密钥 |
| `ANTHROPIC_MODEL` | 覆盖默认模型 |
| `ANTHROPIC_BASE_URL` | API 基础 URL（第三方平台） |
| `MAX_THINKING_TOKENS` | 设置扩展思考 token 预算 |
| `CLAUDE_CODE_EFFORT_LEVEL` | 设置努力级别（`low`/`medium`/`high`/`max`） |
| `CLAUDE_CODE_SIMPLE` | 最小模式，由 `--bare` 标志设置 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | 禁用自动 CLAUDE.md 更新 |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | 禁用后台任务执行 |
| `CLAUDE_CODE_ENABLE_TASKS` | 启用任务列表功能 |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | 启用实验性代理团队 |
| `CLAUDE_CODE_SUBAGENT_MODEL` | 子代理执行的模型 |

---

## 高价值用例

### 1. CI/CD 集成

**GitHub Actions 示例**：

```yaml
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p --output-format json \
            --max-turns 1 \
            "审查此 PR 的更改：
            - 安全漏洞
            - 性能问题
            - 代码质量
            以 JSON 输出，包含 'issues' 数组" > review.json
```

### 2. 脚本管道

```bash
# 分析错误日志
tail -1000 /var/log/app/error.log | claude -p "总结这些错误并建议修复"

# 分析 git 历史
git log --oneline -50 | claude -p "总结最近的开发活动"

# 审查特定文件
cat src/auth.ts | claude -p "审查这段认证代码的安全问题"

# 生成文档
cat src/api/*.ts | claude -p "以 markdown 生成 API 文档"
```

### 3. 批量处理

```bash
# 处理多个文件
for file in src/*.ts; do
  echo "处理 $file..."
  claude -p --model haiku "总结这个文件：$(cat $file)" >> summaries.md
done

# 批量代码审查
find src -name "*.py" -exec sh -c '
  echo "## $1" >> review.md
  cat "$1" | claude -p "简要代码审查" >> review.md
' _ {} \;
```

### 4. JSON API 集成

```bash
# 获取结构化分析
claude -p --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array"},"complexity":{"type":"string"}}}' \
  "分析 main.py 并返回函数列表和复杂度评级"

# 脚本中使用
RESULT=$(claude -p --output-format json "这段代码安全吗？回答 {secure: boolean, issues: []}" < code.py)
if echo "$RESULT" | jq -e '.secure == false' > /dev/null; then
  echo "发现安全问题！"
  echo "$RESULT" | jq '.issues[]'
fi
```

---

## 常用命令组合

### 快速参考表

| 用途 | 命令 |
|------|------|
| 快速代码审查 | `cat file \| claude -p "审查这个"` |
| 结构化输出 | `claude -p --output-format json "query"` |
| 安全探索 | `claude --permission-mode plan` |
| 带安全的自主模式 | `claude --enable-auto-mode --permission-mode auto` |
| CI/CD 集成 | `claude -p --max-turns 3 --output-format json` |
| 恢复工作 | `claude -r "session-name"` |
| 自定义模型 | `claude --model opus "复杂任务"` |
| 最小模式 | `claude --bare "快速查询"` |
| 预算限制 | `claude -p --max-budget-usd 2.00 "分析代码"` |

---

## 故障排除

### 命令未找到

**问题**：`claude: command not found`

**解决方案**：
```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 检查 PATH 包含 npm 全局 bin 目录
npm config get prefix

# 尝试使用完整路径
npx claude
```

### API Key 问题

**问题**：认证失败

**解决方案**：
```bash
# 设置 API Key
export ANTHROPIC_API_KEY=your-key

# 检查密钥有效且有足够余额
# 验证密钥对请求模型的权限
```

### 会话未找到

**问题**：无法恢复会话

**解决方案**：
- 列出可用会话查找正确的名称/ID
- 会话可能在一段时间不活动后过期
- 使用 `-c` 继续最近的会话

### 输出格式问题

**问题**：JSON 输出格式错误

**解决方案**：
- 使用 `--json-schema` 强制结构
- 在提示中添加明确的 JSON 指令
- 使用 `--output-format json`（而非仅在提示中要求 JSON）

### 权限被拒绝

**问题**：工具执行被阻止

**解决方案**：
- 检查 `--permission-mode` 设置
- 审查 `--allowedTools` 和 `--disallowedTools` 标志
- 使用 `--dangerously-skip-permissions` 进行自动化（谨慎使用）

---

## 与其他概念的关系

| 概念 | 关系 |
|------|------|
| [[02-工具使用/如何使用Claude code]] | CLI 的安装配置基础 |
| [[02-工具使用/Claude Code 常用功能]] | 功能速查手册 |
| [[02-工具使用/Claude Code 会话管理]] | 会话管理详解 |
| [[03-进阶应用/Claude MCP 使用指南]] | MCP 协议配置 |
| [[01-基础概念/Skills 是什么]] | Skills 技能系统 |
| [[04-高级应用/Claude Subagent 使用指南]] | 自定义代理创建 |
| [[03-进阶应用/CLAUDE.md 使用指南]] | 项目级配置 |

---

## 个人笔记

> [!personal] 💡 我的理解与感悟
> （此处记录个人学习心得，更新时会被保留）

---

## 参考资料

### 官方资源
- [Claude Code 官方文档](https://code.claude.com/docs/en/overview) - 完整技术文档
- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) - 快速入门指南
- [anthropics/claude-code - GitHub](https://github.com/anthropics/claude-code) - 官方仓库

### 社区资源
- [GitHub - claude-howto CLI Reference](https://github.com/luongnv89/claude-howto/tree/main/10-cli) - 详细 CLI 参考指南
- [Claude Code CLI: The Complete Guide](https://blakecrosley.com/guides/claude-code) - 社区完整指南

### 相关文档
- [[02-工具使用/如何使用Claude code]]
- [[02-工具使用/Claude Code 常用功能]]
- [[02-工具使用/Claude Code 会话管理]]
- [[03-进阶应用/Claude MCP 使用指南]]
