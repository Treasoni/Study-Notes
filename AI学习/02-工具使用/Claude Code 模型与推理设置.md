---
tags: [claude, ai, 工具使用, 模型配置]
created: 2026-03-08
updated: 2026-03-08
---

# Claude Code 模型与推理设置

> [!info] 概述
> **模型与推理设置是 Claude Code 的核心配置** - 控制使用哪个 Claude 模型（Opus、Sonnet、Haiku）以及推理行为（Effort Level、Extended Thinking）。

> [!info] 文档定位
> **本文档聚焦于模型选择和推理参数配置** - CLI 和 VSCode 插件的模型设置、推理参数调整、第三方平台配置。完整安装配置请参阅 [[如何使用Claude code]]

---

## 核心概念

### 是什么

**模型配置** = 选择使用哪个 AI 模型来处理你的请求
**推理设置** = 控制 AI 如何"思考"（思考深度、上下文长度等）

### 为什么需要

- **不同任务需要不同模型**：简单任务用快速模型，复杂推理用强力模型
- **成本控制**：按需选择合适的模型，避免不必要的开销
- **性能优化**：调整推理参数以获得最佳响应质量和速度

### 通俗理解

**🎯 比喻**：选择模型就像选择不同专业度的专家

```
┌─────────────────────────────────────────────────────────────┐
│                    模型选择类比                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Haiku    →  实习生：快速、便宜，适合简单任务              │
│  Sonnet   →  资深工程师：平衡性能和成本，日常工作首选        │
│  Opus     →  首席架构师：最强推理能力，解决复杂问题          │
│                                                             │
│  Effort Level → 思考深度：                                   │
│    low   →  快速反应                                        │
│    medium →  标准思考                                       │
│    high   →  深度推理                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## CLI 模型配置

### 模型别名系统

Claude Code 使用**模型别名**来简化模型选择，别名总是指向最新版本：

| 别名 | 对应模型 | 使用场景 | Token 上下文 |
|------|----------|----------|-------------|
| `default` | 根据账户自动选择 | 系统推荐 | 200K |
| `sonnet` | Claude Sonnet 4.6 | 日常编码任务 | 200K |
| `opus` | Claude Opus 4.6 | 复杂推理任务 | 200K |
| `haiku` | Claude Haiku 4.5 | 简单快速任务 | 200K |
| `sonnet[1m]` | Sonnet + 1M 上下文 | 长会话/大型代码库 | 1M |
| `opusplan` | 智能混合模式 | 规划用 Opus，执行用 Sonnet | 200K |

> [!info] 📚 来源
> - [Model configuration - Claude Code Docs](https://code.claude.com/docs/en/model-config) - 官方模型配置文档

### 模型切换方式

配置优先级从高到低：

```
┌─────────────────────────────────────────────────────────────┐
│                  模型配置优先级（高→低）                       │
├─────────────────────────────────────────────────────────────┤
│  1. 会话中 /model 命令                    │
│  2. 启动时 --model 参数                           │
│  3. 环境变量 ANTHROPIC_MODEL                          │
│  4. settings.json 中的 model 字段                         │
└─────────────────────────────────────────────────────────────┘
```

#### 方式一：会话中切换

```bash
# 交互式选择（显示可用模型列表）
/model

# 直接切换到指定别名
/model sonnet
/model opus
/model haiku

# 切换到 1M 上下文版本
/model sonnet[1m]

# 切换到 opusplan 混合模式
/model opusplan

# 查看当前使用的模型
/status
```

#### 方式二：启动时指定

```bash
# 使用 --model 参数（推荐）
claude --model opus
claude --model sonnet
claude --model haiku

# 使用 -m 简写
claude -m opusplan

# 指定完整模型名称（固定版本）
claude --model claude-opus-4-6
claude --model claude-sonnet-4-6
```

#### 方式三：环境变量

```bash
# 临时设置（当前终端会话）
export ANTHROPIC_MODEL=opus
claude

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export ANTHROPIC_MODEL=sonnet' >> ~/.zshrc
source ~/.zshrc
```

#### 方式四：配置文件

**全局配置** (`~/.claude/settings.json`)：
```json
{
  "model": "sonnet"
}
```

**项目配置** (`.claude/settings.json`)：
```json
{
  "model": "opusplan"
}
```

> [!tip] 配置建议
> - 全局设置：使用 `sonnet` 作为默认（平衡性能和成本）
> - 项目设置：复杂项目使用 `opusplan`，大型代码库使用 `sonnet[1m]`

### 推理参数配置

#### Effort Level（推理努力级别）

控制自适应推理的深度，影响模型分配多少"思考 budget"：

| 级别 | 说明 | Token 预算 | 适用场景 |
|------|------|-----------|----------|
| `low` | 快速响应 | 最少 | 简单问答、代码补全 |
| `medium` | 标准思考（Opus 默认） | 平衡 | 日常开发任务 |
| `high` | 深度推理 | 最多 | 复杂架构设计、调试 |

**设置方式**：

```bash
# 方式一：在 /model 命令中使用左右箭头调整滑块
/model
# 使用箭头键选择 Effort Level

# 方式二：环境变量
export CLAUDE_CODE_EFFORT_LEVEL=low
export CLAUDE_CODE_EFFORT_LEVEL=medium
export CLAUDE_CODE_EFFORT_LEVEL=high

# 方式三：settings.json
{
  "effortLevel": "medium"
}
```

> [!info] 当前状态显示
> 当前 Effort Level 会显示在 logo 和 spinner 旁边，如 "with low effort"，方便确认当前设置。

#### 禁用自适应推理

```bash
# 禁用后使用固定 thinking budget
export CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1
```

#### Extended Thinking（扩展思考）

通过关键词触发不同级别的深度思考：

| 关键词 | Token 预算 | 触发词 |
|--------|-----------|--------|
| ~1.5K | `think` | 在提示中包含 "think" |
| ~3K | `think hard` | 在提示中包含 "think hard" |
| ~8K | `think harder` | 在提示中包含 "think harder" |
| ~16K | `ultrathink` | 在提示中包含 "ultrathink" |

**示例**：
```bash
# 触发深度思考
"请 think hard 分析这个架构设计"
"使用 ultrathink 模式重构这段代码"
```

> [!tip] 技能中的使用
> 在 Skills 文件中包含 "ultrathink" 可启用扩展思考模式。

### 第三方平台配置

通过 `providers` 字段配置第三方 AI 平台：

**配置示例** (`~/.claude/settings.json`)：
```json
{
  "providers": {
    "deepseek": {
      "baseUrl": "https://api.deepseek.com",
      "apiKey": "sk-xxx",
      "defaultModel": "deepseek-chat"
    },
    "volces": {
      "baseUrl": "https://ark.cn-beijing.volces.com/v1",
      "apiKey": "ep-xxxxx",
      "defaultModel": "ep-xxxxx"
    },
    "aliyun": {
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "sk-xxx",
      "defaultModel": "qwen-max"
    },
    "zhipu": {
      "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
      "apiKey": "xxx",
      "defaultModel": "glm-4-plus"
    },
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "apiKey": "ollama",
      "defaultModel": "llama3.2"
    }
  },
  "defaultProvider": "deepseek"
}
```

**使用第三方模型**：
```bash
# 启动时指定
claude --model deepseek-chat

# 会话中切换
/model deepseek-chat
```

> [!warning] 重要说明
> 根据 [claude-task-master 文档](https://github.com/eyaltoledano/claude-task-master/blob/main/docs/examples/claude-code-usage.md)，**部分 AI SDK 参数（如 temperature、maxTokens）在 Claude Code CLI 中不被支持或会被忽略**。

### 扩展上下文（1M Tokens）

Opus 4.6 和 Sonnet 4.6 支持 **100 万 token 上下文窗口**，适用于大型代码库。

**使用方式**：
```bash
# 使用别名
/model sonnet[1m]
/model opus[1m]

# 或附加到完整模型名
/model claude-sonnet-4-6[1m]
/model claude-opus-4-6[1m]
```

**计费说明**：
- 前 200K tokens：标准费率
- 超过 200K tokens：长上下文定价 + 独立速率限制
- 订阅用户：超出部分按额外使用计费

**禁用 1M 上下文**：
```bash
export CLAUDE_CODE_DISABLE_1M_CONTEXT=1
```

> [!info] 📚 来源
> - [Model configuration - Extended context](https://code.claude.com/docs/en/model-config#extended-context) - 官方文档

---

## VSCode 插件配置

### 通过 settings.json 配置

VSCode 插件通过 VS Code 的 `settings.json` 进行配置，支持**用户级**和**工作区级**配置。

**用户级配置** (`~/.config/Code/User/settings.json` 或 `~/Library/Application Support/Code/User/settings.json`)：
```json
{
  "claudeCode.enabled": true,
  "claudeCode.model": "sonnet"
}
```

**工作区配置** (`.vscode/settings.json`)：
```json
{
  "claudeCode.model": "opusplan",
  "claudeCode.environmentVariables": [
    {
      "name": "API_KEY",
      "value": "sk-xxx"
    },
    {
      "name": "HTTP_PROXY",
      "value": "http://127.0.0.1:7890"
    }
  ]
}
```

### VSCode 插件特有配置项

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| `claudeCode.enabled` | 启用/禁用插件 | `true` / `false` |
| `claudeCode.model` | 默认模型选择 | `"sonnet"` / `"opus"` |
| `claudeCode.environmentVariables` | 环境变量数组 | 见上方示例 |
| `claudeCode.mcp.enabled` | 启用 MCP | `true` |

### 与 CLI 的配置共享

VSCode 插件与 CLI **共享以下配置**：

1. **用户级设置**：`~/.claude/settings.json`
2. **MCP 服务器配置**：可从 Claude Desktop 导入
3. **API 密钥和认证**：通过 Keychain 共享

**配置优先级**：
```
VSCode 工作区设置 > VSCode 用户设置 > ~/.claude/settings.json
```

> [!info] 📚 来源
> - [Visual Studio Code - Claude Code Docs](https://code.claude.com/docs/en/vs-code) - 官方 VSCode 文档

---

## 推理模式详解

### opusplan 混合模式

`opusplan` 是一个智能混合模式，自动在不同阶段使用不同模型：

```
┌─────────────────────────────────────────────────────────────┐
│                    opusplan 工作流程                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Plan Mode（规划阶段）                                      │
│       │                                                     │
│       ▼                                                     │
│  使用 Opus 4.6 ──────→ 深度推理、架构设计、任务分解        │
│       │                                                     │
│       ▼                                                     │
│  Execution Mode（执行阶段）                                 │
│       │                                                     │
│       ▼                                                     │
│  使用 Sonnet 4.6 ────→ 代码生成、实现、编辑                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**适用场景**：
- 需要深度规划但大量编码的项目
- 架构设计 + 实现的混合任务
- 想要 Opus 的推理能力但不想承担全部成本

### Prompt Caching 配置

Claude Code 自动使用 prompt caching 优化性能和成本，可以按需禁用：

| 环境变量 | 作用 |
|----------|------|
| `DISABLE_PROMPT_CACHING=1` | 禁用所有模型的 prompt caching |
| `DISABLE_PROMPT_CACHING_HAIKU=1` | 仅禁用 Haiku |
| `DISABLE_PROMPT_CACHING_SONNET=1` | 仅禁用 Sonnet |
| `DISABLE_PROMPT_CACHING_OPUS=1` | 仅禁用 Opus |

> [!tip] 全局优先
> `DISABLE_PROMPT_CACHING` 优先级高于按模型的设置。

---

## 配置最佳实践

### 不同场景的模型选择

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| **日常编码** | `sonnet` | 平衡性能和成本 |
| **复杂调试** | `opus` | 更强的推理能力 |
| **快速补全** | `haiku` | 响应最快 |
| **架构设计** | `opusplan` | 规划深度，执行高效 |
| **大型代码库** | `sonnet[1m]` | 1M 上下文支持 |

### 成本优化策略

```
┌─────────────────────────────────────────────────────────────┐
│                    成本优化金字塔                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        ┌─────────┐                          │
│       Haiku (最便宜)    │         │                          │
│       日常简单任务        └─────────┘                          │
│           │                                                 │
│      ┌────▼─────┐                                            │
│      │  Sonnet  │         (平衡点)                          │
│      │  日常开发  │                                            │
│      └────┬─────┘                                            │
│           │                                                 │
│      ┌────▼─────┐                                            │
│      │  Opus    │         (按需使用)                          │
│      │  复杂任务  │                                            │
│      └─────────┘                                            │
│                                                             │
│  建议：默认 Sonnet，复杂任务升级 Opus，简单任务降级 Haiku    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 性能调优建议

1. **使用 Effort Level**：
   - 简单任务用 `low` 快速完成
   - 复杂任务用 `high` 获得更好结果

2. **利用 opusplan**：
   - 大型项目自动优化模型使用
   - 规划阶段深度推理，执行阶段高效编码

3. **启用 1M 上下文**：
   - 大型代码库使用 `sonnet[1m]`
   - 注意 200K 后的额外计费

---

## 常见问题

**Q: temperature 参数支持吗？**

A: 根据社区文档，Claude Code CLI 对 `temperature` 等 AI SDK 参数的支持**有限或会被忽略**。建议使用 Effort Level 来控制输出行为。

**Q: 如何查看当前使用的模型？**

A: 使用 `/status` 命令，会显示当前模型和 Effort Level。

**Q: opusplan 一定会省钱吗？**

A: 不一定。opusplan 在规划阶段使用 Opus（更贵），执行阶段使用 Sonnet。对于规划简单、执行复杂的任务可能更贵；对于规划复杂的任务可能更省。需根据实际场景评估。

**Q: 第三方平台可以用模型别名吗？**

A: 可以，但需要配置 providers。配置后可以直接使用 `/model` 切换，或设置 `defaultProvider`。

**Q: Effort Level 和 Extended Thinking 有什么区别？**

A:
- **Effort Level**: 控制模型分配多少"思考 budget"来处理任务
- **Extended Thinking**: 触发特定级别的深度思考（1.5K~16K tokens）

两者可以同时使用：设置 `effortLevel: high` 并使用 `think hard` 会同时生效。

**Q: VSCode 插件和 CLI 的配置有冲突怎么办？**

A: 配置优先级为：VSCode 工作区设置 > VSCode 用户设置 > `~/.claude/settings.json`。如需统一，建议在 `~/.claude/settings.json` 中配置，两者都会读取。

---

## 相关文档

- [[02-工具使用/如何使用Claude code]] - 完整安装配置指南
- [[02-工具使用/Claude Code 常用功能]] - 功能速查手册
- [[02-工具使用/Claude Code 会话管理]] - 会话管理技巧
- [[03-进阶应用/Claude MCP 使用指南]] - MCP 配置教程

---

## 参考资料

### 官方资源
- [Model configuration - Claude Code Docs](https://code.claude.com/docs/en/model-config) - 模型配置文档
- [Claude Code settings - Claude Code Docs](https://code.claude.com/docs/en/settings) - 设置文档
- [Visual Studio Code - Claude Code Docs](https://code.claude.com/docs/en/vs-code) - VSCode 插件文档

### 社区资源
- [How to Setup Claude Code in VSCode (2026)](https://www.youtube.com/watch?v=m2xE5O81mSg) - YouTube 教程
- [Claude Code Complete Guide 2026]((https://www.jitendrazaa.com/blog/ai/claude-code-complete-guide-2026-from-basics-to-advanced-mcp-2/) - 完整指南

### GitHub 资源
- [claude-task-master - Claude Code usage examples](https://github.com/eyaltoledano/claude-task-master/blob/main/docs/examples/claude-code-usage.md) - 使用示例和限制说明
