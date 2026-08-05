---
title: CLI 与调试 — 日常操作与故障排查
tags: [codex, cli, debugging, troubleshooting, environment-variables, configuration-audit]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: codex-config
---

# CLI 与调试 — 日常操作与故障排查

前六章我们把 Codex 的配置体系拆了个遍——从 config.toml 到 AGENTS.md，从 skills 到 hooks，每个子系统都有自己的配置文件和加载规则。但配置再多，最终你每天打交道的是 CLI。本章不做命令参考手册（附录里有速查表），只聚焦高频的日常操作命令、环境变量管理和配置验证技巧——那些你配完新东西后一定会用到的"检查回路"。

---

## 1. 核心 CLI 命令

### 1.1 启动与执行

```bash
# 交互式 REPL（最常用）
codex

# 单次执行，输出结果后退出
codex exec "解释这个项目的 .gitignore"

# 指定工作目录启动
codex --cd /path/to/project

# 指定模型
codex --model gpt-5.4-mini

# 指定审批模式
codex --approval-mode on-request
```

`codex exec` 适合脚本集成和 CI/CD 场景——不需要交互式终端，一次执行一个任务。普通开发中大部分时间用 `codex` 进入交互模式即可。

`--cd` 比先 `cd` 再启动 `codex` 更可靠，因为它在会话初始化前就设置了工作目录，确保 AGENTS.md 发现、`.codex/config.toml` 加载、技能索引等工作都基于正确的目录上下文。具体来说，`--cd` 会影响以下加载逻辑：

- **AGENTS.md 路径**：从 `--cd` 指定的目录向上遍历到 Git 根，构建指令链
- **项目配置**：加载 `--cd` 指定目录下的 `.codex/config.toml`
- **工作区信任**：基于 `--cd` 指定的目录匹配 `[projects]` 信任规则

这与先 `cd` 再启动的效果等价，但更加显式——适合在脚本或 `codex exec` 中使用。

### 1.2 状态检查与配置审计

```bash
# 查看当前 workspace 状态（加载了哪些配置、指令、技能）
codex status

# 查看当前会话加载了哪些指令文件
codex --cd subdir "请列出当前加载的所有指令文件"

# 验证特定目录下的配置加载情况
codex --cd /path/to/project status
```

`codex status` 是你最频繁使用的诊断命令。它输出当前会话的关键状态：

- **项目根目录**：当前 workspace 所在路径
- **已加载的指令文件**：AGENTS.md 链中的所有文件（全局 + 项目各级目录）
- **已发现的技能**：各作用域下注册的技能列表
- **配置来源**：使用了哪个层级的 config.toml
- **活跃的 profile**：当前生效的配置档
- **MCP 服务器状态**：已注册的 MCP 服务器及其运行状态

> **提示**：`codex status` 的输出比你想的更丰富。每次修改配置后，先跑一遍 status，看是否出现了意料之外的加载路径或缺失项。

### 1.3 配置档与临时覆盖

```bash
# 使用特定配置档
codex --profile fast

# 临时覆盖单个配置项
codex -c model=gpt-5.4-mini -c approval_policy=never

# 查看当前活跃的 profile
codex status  # 在输出中找 Active Profile 行
```

`-c key=value` 是 CLI 参数级覆盖（最高优先级），适用于临时调整——比如一次性的快速实验。它优于修改 `config.toml` 再改回来的方式，省去了"改文件—验证—改回去"的循环。

一条经验法则：
- **长期变更** → 修改 `config.toml` 或创建 new profile
- **临时实验** → `-c key=value`
- **按场景切换** → `--profile NAME`（参见第二章 profiles 配置）

### 1.4 MCP 管理

```bash
# 交互式添加 MCP 服务器
codex mcp add

# 示例：添加一个文件系统 MCP 服务器
# 运行 codex mcp add 后，CLI 会引导你输入：
#   - 服务名称
#   - 命令（如 npx）
#   - 参数（如 -y @modelcontextprotocol/server-filesystem /path）
```

`codex mcp add` 的最大价值在于：**它自动将 MCP 配置写入正确的 config.toml 层级**。你不需要记住 TOML 区块的格式，也不需要判断应该写用户级还是项目级——CLI 为你处理这些细节。

---

## 2. 交互式命令

在交互式 REPL 会话中，以 `/` 开头的命令用于操作 Codex 自身而非与 agent 对话。

### 2.1 `/skills` — 技能管理

```bash
# 列出所有可用技能
/skills

# 输出示例：
Available Skills:
  REPO:
    - code-explorer    — 探索代码库结构，定位关键文件（~/.agents/skills/code-explorer）
    - test-generator   — 生成单元测试代码
  USER:
    - note-taker       — 记录开发笔记到 Obsidian
    - git-helper       — Git 工作流辅助
  SYSTEM:
    - skill-creator    — 创建新技能
    - workflow-orchestrator — 工作流编排

# 匹配到的技能会在对话中自动加载
# 用户也可以直接引用 /skills 中的名称来显式调用
```

详见第四章技能系统的加载机制。

### 2.2 `/hooks` — 钩子管理

```bash
# 查看所有已注册的钩子
/hooks

# 输出示例：
Known Hooks:
  1. SessionStart — ~/.codex/hooks.json → python3 ~/.codex/hooks/session_start.py
     Status: ENABLED   Trust: trusted
  2. PreToolUse — .codex/hooks.json → python3 .codex/hooks/audit.py
     Status: ENABLED   Trust: untrusted  [Pending your approval]

  Commands: trust <id> | untrust <id> | disable <id> | enable <id> | status

# 信任特定钩子
/hooks trust 2
# 输出: Hook #2 (PreToolUse) now trusted
```

详见第六章 hooks 的信任机制。

### 2.3 `/config` — 交互式配置

```bash
# 查看当前配置
/config

# 修改配置项
/config set model=gpt-5.4-mini
/config set approval_policy=on-request

# 查看特定配置维度的当前值
/config get model
/config get sandbox_mode
```

`/config` 命令在交互式会话中修改配置，修改即时生效。与 `-c` 不同的是，`/config set` 的影响范围仅限于当前会话，不会写入任何配置文件。适合快速试错——你可以在一次会话中反复调整配置，找到合适的组合后再固化到文件。

### 2.4 `/feedback` — 反馈

```bash
# 提交反馈给 Codex 开发团队
/feedback
```

打开一个反馈编辑器，填写内容后提交。这不仅仅是用户体验渠道——它也可以用于报告配置异常或功能建议。

---

## 3. 环境变量

### 3.1 CODEX_HOME

`CODEX_HOME` 指定全局配置目录，默认是 `~/.codex`。设置后：

```bash
# 在 shell profile 中设置
export CODEX_HOME=/path/to/custom/codex-home

# 目录结构（设置后所有全局配置都移到这里）
$CODEX_HOME/
├── config.toml          # 用户级全局配置
├── AGENTS.md            # 全局指令文件
├── AGENTS.override.md   # 全局指令覆盖
├── agents/              # 用户级 agent 定义
├── hooks.json           # 全局钩子
├── plugins/             # 全局插件
└── skills/              # 全局 skills（REPO/USER 路径）
```

改变 `CODEX_HOME` 后，所有路径解析都基于新目录，包括 `~/.codex` 中所有配置文件的查找。如果你有多套 Codex 配置环境（比如工作用的安全配置和个人实验配置），可以通过切换 `CODEX_HOME` 快速切换。

> **迁移注意**：改变 `CODEX_HOME` 不会自动迁移原 `~/.codex` 中的内容。你需要手动复制或重建所需的配置文件。

### 3.2 OPENAI_API_KEY

API 认证通过环境变量提供，不写入配置文件：

```bash
# 直接设置
export OPENAI_API_KEY=sk-...

# 通过 .env 文件（见 3.3 节）
echo "OPENAI_API_KEY=sk-..." > .env
```

Codex 不要求你在 config.toml 中硬编码 API key——这是安全设计。多提供商场景（如 Azure、OpenRouter）也通过各自的环境变量（如 `AZURE_API_KEY`、`OPENROUTER_API_KEY`）传递。

### 3.3 .env 自动加载

Codex 在会话启动时自动加载项目根目录的 `.env` 文件（如果存在）：

```text
# 项目根目录/.env
OPENAI_API_KEY=sk-...
MY_CUSTOM_VAR=value
DEBUG=false
```

加载规则：
- **只在项目根目录搜索** `.env`，不遍历子目录
- **不会覆盖已存在的环境变量**——如果你已在 shell 中 `export` 了同名变量，`.env` 中的值被忽略
- 支持 `${VAR}` 格式的变量展开（如果 shell 环境支持）

加载时机：**在 AGENTS.md 发现和 config.toml 加载之前**，所以 `.env` 中定义的变量可以影响后续的配置解析。这意味着你可以在 `.env` 中设置 `CODEX_HOME` 的覆盖，或者在 `.env` 中定义 MCP 服务器配置中引用的 `bearer_token_env_var`。

> **安全提醒**：`.env` 不应提交到 Git。确保它在 `.gitignore` 中。

---

## 4. 调试与验证方法

### 4.1 验证指令加载

配置 AGENTS.md 后，验证它是否被正确加载：

```bash
# 方法一：通过 codex status 查看
codex status
# 在输出中寻找 "Loaded Instruction Files" 部分
# 应列出 AGENTS.md 链中的所有文件

# 方法二：直接用 prompt 询问（推荐）
codex exec --cd /path/to/project "请列出你当前加载的所有指令文件和规则，并告诉我它们的来源路径"
```

方法二的优势在于：它实际模拟了 agent 的视角。如果 agent 回答说"我没有加载任何指令文件"，说明配置链有问题。如果它列出了预期的文件链，则说明指令文件被正确发现和加载。

### 4.2 验证技能发现

```bash
# 在交互式会话中
/skills
# 确认你的新技能出现在对应作用域下

# 如果是隐式匹配，触发后观察 agent 是否使用了该技能
# 可以在 prompt 中包含技能的 description 触发词来测试
```

如果你在 `/skills` 输出中看不到刚放进去的技能，按以下顺序排查：

1. 技能目录是否放在正确的发现路径下？（REPO: `.agents/skills/` vs USER: `~/.agents/skills/`）
2. `SKILL.md` 的文件名是否包含在技能目录名中？（技能目录名即技能加载名）
3. `SKILL.md` 的 frontmatter 是否格式正确？（YAML 解析失败会导致技能被跳过）
4. 技能列表是否因为 token 预算限制被截断？（参见第四章的渐进式延迟加载——描述被截断是典型信号）

### 4.3 验证 hook 注册

```bash
# 在交互式会话中
/hooks
# 确认新 hook 出现在列表中
# 确认它的 Trust 状态不是 untrusted

# 测试 hook 触发
# 执行一个会触发该 hook 的操作
# 观察 hook 脚本是否成功执行
```

如果 hook 没有触发，常见原因（按概率排序）：

1. **信任状态**：新注册的 hook 默认是 `untrusted`——不会执行。需要 `/hooks trust <id>`。
2. **配置文件格式**：`hooks.json` 的 JSON 格式错误（比如多了一个逗号）导致整个文件被忽略。用 `jq . hooks.json` 验证。
3. **matcher 不匹配**：事件触发了，但 matcher 条件不匹配。检查 matcher 字段的拼写和格式。
4. **脚本路径不对**：hook 脚本的路径是相对路径时，解析可能不如预期。推荐使用绝对路径或在 hooks.json 中确认 CWD。
5. **脚本退出码不对**：如果脚本自身出错但退出码是 1，Codex 不视其为明确的阻断信号（参见第六章退出码约定）。

### 4.4 审计 session JSONL

Codex 将每次会话的完整记录保存为 JSONL 文件：

```bash
# 默认位置
ls ~/.codex/transcripts/

# 找到最近的 session JSONL
ls -t ~/.codex/transcripts/ | head -1

# 查看原始交互记录（每行一个 JSON 对象）
head -100 ~/.codex/transcripts/session_20240731_001.jsonl
```

Session JSONL 记录了完整的交互过程——用户输入的 prompt、agent 的工具调用、返回值等。它主要用于：

- **调试 hook 行为**：查看 PreToolUse 钩子是否拦截了预期的工具调用
- **分析 agent 决策**：理解 agent 为何执行了某个操作
- **排查 MCP 工具调用失败**：查看传递给 MCP 工具的参数是否正确

每条 JSONL 记录包含时间戳、事件类型（user_prompt / tool_use / tool_result / assistant_message 等）和完整的数据载荷。直接 `grep` 关键词是快速定位问题的方法。

### 4.5 查看日志

```bash
# Codex 的运行时日志
# 默认不输出到终端，需通过环境变量启用
export CODEX_LOG_LEVEL=debug
codex

# 或将日志输出到文件
codex 2> codex-debug.log
```

日志级别通常包括 `error`、`warn`、`info`、`debug`。`debug` 级别最详细，会输出配置加载过程、技能索引、hook 注册等底层信息——这些在标准输出的 `codex status` 中看不到。

---

## 5. 配置审计技巧

### 5.1 快速诊断清单

当你发现 Codex 的行为不符合预期时，按以下顺序排查：

```text
1. 配置文件在哪层？
   → codex status | findstr "Config"
   → 确认正在使用你期望的那个 config.toml

2. 配置项生效了吗？
   → 检查是否写入了项目级但该键是"静默忽略"键（如 model_provider）
   → 检查是否有更高优先级的覆盖（profile？CLI 参数？）

3. 指令文件加载了吗？
   → codex exec "请列出所有加载的指令文件"
   → 确认 AGENTS.md 链中没有缺失的文件

4. 技能发现了吗？
   → /skills
   → 确认技能在正确的作用域下

5. Hook 注册了吗？
   → /hooks
   → 确认 hook 的 Trust 状态

6. MCP 服务器能连吗？
   → codex status 中查看 MCP 状态
   → 如果显示 error，检查 startup_timeout_sec 是否太短
```

### 5.2 验证配置优先级

如果同一个配置项在不同层级被设置了不同值，验证最终生效的值：

```bash
# 方法一：通过 codex status
codex status
# 输出包含各配置层的来源路径

# 方法二：直接问 agent
codex exec "告诉我当前的 sandbox_mode 和 approval_policy 是什么，以及它们的配置来源"

# 方法三：使用 /config 命令
codex -c /config  # 进入交互模式后
/config get sandbox_mode
/config get approval_policy
```

### 5.3 常见故障案例

#### 案例 1：模型提供商配置不生效

**症状**：设置了 `model_provider = "ollama"`，但 agent 仍然调用 OpenAI API。

**排查**：
```
1. 检查 model_provider 在哪个配置层
   → 发现设在 .codex/config.toml（项目级）
2. 翻阅第二章的安全限定表
   → model_provider 是「静默忽略」键，只能放在 ~/.codex/config.toml（用户级）
3. 修正：移到用户级配置
```

**根因**：安全限定规则——某些键在项目级写入会被静默忽略，不报错，不警告。

#### 案例 2：技能没有被自动加载

**症状**：一个自建的 Code Review 技能，在对话中提到 code review 时 agent 没有使用它。

**排查**：
```
1. /skills 查看技能列表
   → 技能存在于列表中，description 包含 "code review"
2. 检查 session JSONL
   → 发现 agent 确实收到了技能列表，但选择了不同的工具
3. 调整 description 触发词，增加显式性
   → description: "审查代码变更，提供改进建议。当你需要做 Code Review 时使用"
```

**根因**：隐式匹配依赖 description 中的触发词，但触发词不够精准。同时，agent 不一定会使用匹配到的技能——它可能认为自己的内置能力已经足够。调整 description 的措辞可以提升匹配率。

#### 案例 3：SessionStart hook 没有执行

**症状**：配置了 SessionStart hook 用于加载工作笔记，但每次启动都没有效果。

**排查**：
```
1. /hooks 查看状态
   → Hook #1 Status: ENABLED   Trust: untrusted
2. 执行信任操作
   → /hooks trust 1
3. 重新启动会话，hook 生效
```

**根因**：新注册的 hook 默认信任状态为 `untrusted`，不会执行。这是安全设计，但初次使用者容易忽略。

#### 案例 4：配置文件变更后无效果

**症状**：修改了 `~/.codex/config.toml` 或 `.codex/config.toml`，但重启后配置未生效。

**排查**：
```
1. codex status 确认配置来源路径
   → 发现加载的是另一个目录的 config.toml
2. 检查是否有 CODEX_HOME 环境变量
   → 发现 CODEX_HOME 指向了一个自定义路径
3. 确认正在修改的是 CODEX_HOME 指向的 config.toml
```

**根因**：`CODEX_HOME` 环境变量改变了全局配置目录的查找路径。之前配了 `CODEX_HOME` 但忘记了。

---

## 本章小结

- **四条核心 CLI 命令覆盖日常操作**：`codex`（交互模式）、`codex exec`（单次执行）、`codex status`（状态审计）、`codex --cd`（指定工作目录）。`-c key=value` 用于临时覆盖配置项，`--profile NAME` 用于按场景切换配置档。
- **交互式命令管理运行时状态**：`/skills` 列出可用技能，`/hooks` 管理钩子信任和状态，`/config` 实时查看和修改配置（仅当前会话生效），`/feedback` 提交反馈。
- **三个环境变量控制运行时行为**：`CODEX_HOME` 重定向全局配置目录，`OPENAI_API_KEY` 提供 API 认证，`.env` 文件自动加载项目级环境变量（不会覆盖已存在的 `export`）。
- **调试优先用 `codex status` + 直接询问 agent**：`codex status` 输出配置层、指令链、技能列表等关键状态；直接让 agent 列出已加载的指令文件是最直观的验证方法。Session JSONL 和 debug 日志提供更底层的诊断信息。
- **常见故障有规律可循**：静默忽略键只能放用户级、新 hook 需先 trust、技能隐式匹配依赖 description 触发词、`CODEX_HOME` 改变配置查找路径。按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序排查，覆盖 90% 场景。

## 下一章预告

CLI 命令和调试技巧让你在日常操作中游刃有余，但一个更大的问题始终存在：**如果你是一个 Claude Code 的老用户，如何把整套配置体系迁移到 Codex？** 最后一章将把前七章的所有知识点整合起来——一份完整的 Codex vs Claude Code 配置对照表，一套四步迁移策略，以及常见陷阱和最佳实践。准备好从"理解"走向"迁移"了吗？
