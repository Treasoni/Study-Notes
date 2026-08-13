# 第三章：配置体系 opencode.json——从 settings.json 迁移

> 笔记类型：实战笔记 ｜ 学习深度：精通 ｜ 主线：Claude Code → opencode 迁移

前两章你已经装好 opencode、完成认证并跑通了第一个会话。现在遇到的核心问题是：怎么把在 Claude Code 里积累的整套配置体系搬过来？Claude Code 的配置散落在 `~/.claude/settings.json`、项目级 `.claude/settings.local.json`、`CLAUDE.md` 和 `mcpServers` 里；而 opencode 把行为收敛到一份声明式 JSONC 文件 `opencode.json`，用 8 层优先级做合并。本章逐层拆开这套体系，并把 Claude Code 的每一项配置翻译成 opencode 的写法。

## 3.1 先找到配置：JSONC 与 $schema

opencode 的配置是**一份带注释的 JSON 文件**（JSONC，JSON with Comments），位置按作用域不同有三层落点：

| 作用域 | 路径 | 对应 Claude Code |
|--------|------|------------------|
| 全局 | `~/.config/opencode/opencode.json` | `~/.claude/settings.json` |
| 项目 | 项目根 `opencode.json`（向上找最近 Git 目录） | `.claude/settings.local.json` |
| 远程/组织 | `.well-known/opencode` | 企业托管 settings |

文件第一行通常是 `$schema`，它指向 JSON Schema 定义，让编辑器（VS Code 等）在你写配置时实时校验字段名和类型：

- `https://opencode.ai/config.json` — 运行时配置 schema
- `https://opencode.ai/tui.json` — TUI 界面配置 schema（状态栏、主题等界面项）

> [!tip] 大白话：把 `$schema` 想成作文考试的评分标准
> 把 `$schema` 想成作文考试的评分标准——编辑器拿着这份标准帮你检查哪句拼错了、哪个字段名不规范。所以配置第一行写 `$schema` 不是为了运行，而是为了让编辑器在写配置时就报错，把「字段名打错、类型写错」这类坑挡在运行之前。

## 3.2 8 层配置优先级：合并而非替换

这是 opencode 配置体系与 Claude Code 最本质的差异。Claude Code 是「用户 settings + 项目 settings + 托管 settings」三处叠加；opencode 把叠加拆成了 **8 层**，从高到低：

| 优先级 | 配置来源 | 说明 |
|-------|----------|------|
| 1（最高） | macOS 托管偏好（MDM `ai.opencode.managed`） | 公司/组织强制下发 |
| 2 | 托管配置文件（macOS `/Library/Application Support/opencode/`、Linux `/etc/opencode/`、Windows `%ProgramData%\opencode`） | 管理员统一部署 |
| 3 | `OPENCODE_CONFIG_CONTENT` 环境变量 | 内联一段配置 JSON，适合 CI/临时覆盖 |
| 4 | `.opencode` 目录 | 项目级扩展目录（agents、commands、plugins…），等价于 Claude Code 的 `.claude/` |
| 5 | 项目根 `opencode.json` | 从当前目录向上找最近 Git 目录 |
| 6 | `OPENCODE_CONFIG=/path/to/config.json` | 显式指定一份配置文件 |
| 7 | 全局 `~/.config/opencode/opencode.json` | 你的个人默认配置 |
| 8（最低） | 远程 `.well-known/opencode` | 组织默认基线 |

关键规则：**配置是合并（merge）而非替换（replace）**。高层配置只覆盖与低层冲突的键，低层配置里高层没提的部分依然生效。项目覆盖全局、全局覆盖远程、托管设置覆盖一切。

> [!tip] 大白话：把 8 层配置想成公司群发的 8 条通知
> 把 8 层配置想成公司群发的通知：总部（托管）的最大、部门（项目）次之、你个人（全局）最小；小通知和大通知冲突时以大为准，但大通知没管到的事项照常执行。所以配置是层层叠加，改项目里的 `opencode.json` 就能覆盖全局默认，不必担心「动了这层就推倒重来」。

这个合并机制带来一个实用推论：**你不需要在项目里复制整份全局配置**。全局放通用偏好（默认模型、通用 provider），项目只写差异项（项目专属 model、权限收紧、MCP），两者自动叠加。

## 3.3 核心配置键逐个讲解

opencode.json 顶层键大致分五类：模型、接入层、行为扩展、安全边界、外部集成。

### 模型与智能体：model / small_model / default_agent / subagent_depth

| 键 | 作用 | 默认值 |
|----|------|--------|
| `model` | 主模型，格式 `provider/model`（如 `anthropic/claude-sonnet-4-5`） | 无 |
| `small_model` | 轻量任务模型（上下文压缩、小规模分诊等），省钱 | 无 |
| `default_agent` | 默认启动的 agent | `build`（无效时回退） |
| `subagent_depth` | 子代理递归深度 | `1` |

`small_model` 没有 Claude Code 的直接对应，是 opencode 控成本的关键：把开销小的杂活甩给便宜模型，主模型专注重活。这也是第 1 章提到的「逐步路由控成本」的配置基础。

### provider：模型接入层

`provider` 定义「如何连接某个模型供应商」，是 opencode 模型解耦的落地处（Claude Code 无对应——它只认 Anthropic）。每个 provider 是一个对象：

- `options.apiKey`：API key，支持 `{env:VAR}`、`{file:path}`，或留空走 `/connect` 图形化认证。
- `options.timeout`：请求超时，默认 `300000` ms。
- `options.chunkTimeout`：流式分块超时。
- `disabled_providers` / `enabled_providers`：禁用/启用供应商列表（`disabled_providers` 优先）。

> [!tip] 大白话：把 provider 想成电源插头转换器
> 把 provider 想成电源插头转换器——不同厂商的 API「插座规格」各不相同，opencode 靠 provider 配置让同一套框架插进 Anthropic、OpenAI、本地 Ollama 等任何插座。所以换模型不用换工具，改一行 `provider` 引用即可。

### agent 与 command：扩展行为

- `agent`：自定义智能体，字段为 `description`、`model`、`prompt`、`tools`；也可以用 Markdown 文件定义（第 8 章细讲）。
- `command`：自定义 Slash 命令，字段为 `template`（提示模板）、`description`、`agent`、`model`。

两者分别对应 Claude Code 的 `.claude/agents/*.md` 与自定义 slash 命令，只是 opencode 把它们声明式地收进了配置。

### permission 与 tools：安全边界

- `permission`：opencode 的权限核心，三值模型 `allow` / `ask` / `deny`。**默认全部允许**（比 Claude Code 宽松得多），需要主动收紧，例如 `{ "edit": "ask", "bash": "ask" }`。
- `tools`：旧式布尔开关，如 `{ "write": false }`；**v1.1.1 起废弃并并入 `permission`**。

权限系统是第 5 章的主题，这里只需记住：迁移时别沿用 Claude Code 的「默认询问」心智，opencode 默认放开、靠 `/undo` 兜底，安全靠你自己写 `permission` 收紧。

### mcp / plugin / instructions：外部集成

- `mcp`：MCP server 配置，等价于 Claude Code 的 `mcpServers`（第 7 章细讲）。
- `plugin`：npm 插件数组，opencode 的官方扩展点之一（Claude Code 无直接对应）。
- `instructions`：指令文件路径/glob 数组，把额外的上下文文件注入会话（类似追加多份 `CLAUDE.md`）。

### 其余键：server / shell / snapshot / autoupdate / share 等

这些键在官方文档中仅有键名、缺少展开说明，按命名和使用场景可理解如下（以 `https://opencode.ai/docs/config` 为准）：

| 键 | 大致用途 |
|----|----------|
| `server` | `opencode serve` 无头服务器的相关配置 |
| `shell` | 执行 bash 命令所用的 shell 配置 |
| `snapshot` | Git 快照安全网（`/undo` 支撑）的行为配置 |
| `autoupdate` | 是否自动升级、升级通道 |
| `share` | 会话分享（`/share`）的配置 |
| `formatter` | 代码格式化器配置 |
| `lsp` | LSP 集成的行为配置 |
| `compaction` | 上下文压缩策略配置 |
| `experimental` | 实验性功能开关 |

## 3.4 变量替换：{env:VAR} 与 {file:path}

配置里允许两种占位符，在加载时被替换成真实值：

- `{env:VARIABLE_NAME}` → 环境变量的值；**未设置则为空字符串**。
- `{file:path}` → 文件内容；相对路径以配置文件所在目录为基准，支持 `/` 与 `~`。

> [!tip] 大白话：把 `{env:VAR}` 想成便签上的「见附件」
> 把 `{env:VAR}` 想成便签上的「见附件」——配置文件里不写真密钥，只写占位符，运行时去环境变量里取。所以密钥留在 shell 环境里，`opencode.json` 可以放心提交 Git，别人拿到你的配置也看不到 key。而 `{file:path}` 相当于「钥匙在保险箱里」，适合从本地文件读密钥。

注意这里的坑：第 9 章会展开 issue #34388——如果环境变量未设置，`{env:VAR}` 会被替换成空串 `""`，而 provider 回退 auth.json 用严格相等 `=== undefined`，空串会阻断回退导致 401。**用 `{env:VAR}` 时务必保证变量已导出**。

## 3.5 基础配置示例逐行解读

这是一份「从 Claude Code 迁过来的最小可用配置」，JSONC 格式允许注释：

```jsonc
{
  // 1. 编辑器校验：字段名/类型写错立刻标红
  "$schema": "https://opencode.ai/config.json",

  // 2. 主模型：格式 provider/model，对应 Claude Code settings 的 "model"
  "model": "anthropic/claude-sonnet-4-5",

  // 3. 轻量模型：压缩上下文等杂活用便宜模型
  "small_model": "anthropic/claude-haiku-4-5",

  // 4. 接入层：告诉 opencode 怎么连 Anthropic
  "provider": {
    "anthropic": {
      "options": {
        // 5. 密钥从环境变量读，不写死、可提交 Git
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  },

  // 6. 安全边界：opencode 默认全允许，这里主动收紧到"改动前询问"
  "permission": {
    "edit": "ask",
    "bash": { "*": "ask", "rm *": "deny" }
  },

  // 7. 额外上下文：把 docs 下的说明文档注入会话
  "instructions": ["docs/**/*.md"]
}
```

逐行要点：

1. **`$schema`** 让编辑器校验配置（见 3.1）。
2. **`model`** 决定默认智能体用哪个模型，格式必须是 `provider/model` 两段式。
3. **`small_model`** 承担轻量任务，是 opencode 控成本的第一道闸。
4. **`provider.anthropic.options`** 声明连接 Anthropic 所需的参数。
5. **`apiKey: "{env:ANTHROPIC_API_KEY}"`** 从环境变量注入密钥（见 3.4），对应 Claude Code 的 `apiKeyHelper` 注入思路。
6. **`permission`** 收紧默认的「全允许」：改文件、跑命令前询问，`rm *` 直接拒绝。这是从 Claude Code 迁移时最容易忽略的一步。
7. **`instructions`** 注入额外上下文文件，等效于把多份 `CLAUDE.md` 一起塞给模型。

配合第二份示例看变量替换的 `{file:}` 用法（自定义 OpenAI 兼容 provider 时的密钥读取）：

```jsonc
{
  "provider": {
    "venice": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "https://api.venice.ai/api/v1",
        "apiKey": "{file:~/.secrets/venice.key}" // 从本地文件读，支持 ~
      }
    }
  }
}
```

## 3.6 Claude Code 配置迁移映射

### 配置体系对照

| 作用域 | Claude Code | opencode |
|--------|-------------|----------|
| 全局设置 | `~/.claude/settings.json` | `~/.config/opencode/opencode.json` |
| 项目设置 | `.claude/settings.local.json` | 项目根 `opencode.json` |
| 上下文/指令 | `CLAUDE.md` | `AGENTS.md`（原生加载） |
| 项目扩展目录 | `.claude/`（skills、agents、commands） | `.opencode/` |
| 托管/企业 | Enterprise managed settings | 8 层中的 1、2、8 层 |

### settings.json → opencode.json 键级映射表

| Claude Code settings | opencode.json | 差异说明 |
|----------------------|---------------|----------|
| `model` | `model` / `small_model` | opencode 多了轻量模型位 |
| `permissions.allow/deny/ask`（数组式） | `permission`（三值 + glob） | 模型差异大，见第 5 章 |
| `apiKeyHelper` | `provider.<id>.options.apiKey` | 注入方式从脚本改为 `{env:}` / `{file:}` |
| `env` | 无顶层键 | 改用 `{env:VAR}` 引用 + shell 环境 |
| `mcpServers` | `mcp` | 见第 7 章 |
| `hooks` | `hooks` | 仅支持 4 个共享 hook，见第 8 章 |
| `includeCoAuthoredBy` / `cleanupPeriodDays` 等 | 无直接对应 | 忽略 |
| `enableAllProjectSkills` | 无需开关 | Skills 按 6 个位置自动发现，见第 8 章 |

### CLAUDE.md → AGENTS.md

- `CLAUDE.md` 是 Claude Code 的上下文文件；opencode 原生加载 **`AGENTS.md`**，`/init` 也会生成它（第 2 章的 `/init` 命令）。
- 迁移时直接把 `CLAUDE.md` 内容搬进 `AGENTS.md` 即可，两份文件的写法（项目规范、指令、注意事项）互通。
- 额外的上下文文件可用 `instructions` 键按 glob 追加。

### 迁移三步清单

1. **搬默认**：把全局 `~/.claude/settings.json` 的 `model`、provider 认证翻译到 `~/.config/opencode/opencode.json`。
2. **搬项目**：项目级 `.claude/settings.local.json` 的差异项（模型、权限、MCP）翻译到项目根 `opencode.json`。
3. **搬上下文与权限**：`CLAUDE.md` → `AGENTS.md`；把 Claude Code 的 `permissions` 数组翻译成 opencode 的 `permission` 三值+glob（务必主动收紧默认的「全允许」）。

## 本章小结

- opencode 用一份 JSONC 文件 `opencode.json` 收敛配置，`$schema` 让编辑器实时校验，`config.json` 管运行时、`tui.json` 管界面。
- 配置按 8 层优先级**合并而非替换**：项目覆盖全局、全局覆盖远程、托管设置最大；改项目文件即可覆盖全局默认。
- 核心键分五类：`model`/`small_model`（模型）、`provider`（接入层）、`agent`/`command`（行为扩展）、`permission`/`tools`（安全边界）、`mcp`/`plugin`/`instructions`（外部集成）。
- 变量替换 `{env:VAR}`（环境变量，未设置变空串）与 `{file:path}`（文件内容，支持 `~`）是「密钥不进配置文件」的关键。
- 迁移三步：搬全局 → 搬项目 → 搬上下文（`CLAUDE.md`→`AGENTS.md`）并重写权限；`permission` 默认全允许，务必主动收紧。

## 下一章预告

配置体系搬完了，接下来是日常使用：第 4 章把 Claude Code 的命令逐个翻译成 opencode 的 TUI 交互、slash 命令和 `opencode run` 非交互模式，并给出完整命令对照速查表。
