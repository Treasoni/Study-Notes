---
title: Claude Code 使用指南
tags: [ai, 工具使用, claude-code, 入门]
updated: 2026-07-12
status: updated
source_project: claude-code-tutorial
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
> - 安装后执行 `claude --version` 验证，当前最新为 **v2.1.207**（2026-07-11）

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
| `claude --model claude-sonnet-5` | 指定模型启动（默认 Sonnet 5） |
| `claude -m deepseek-chat` | 使用第三方模型 |
| `claude -p "query"` | 打印模式，执行后退出（自动化/CI） |
| `claude -c` | 继续最近会话 |
| `claude --resume <name>` | 恢复命名会话 |
| `claude agents` | 统一代理视图（运行/阻塞/完成的会话） |
| `claude --safe-mode` | 安全模式，禁用所有自定义项（排障用） |
| `claude --worktree` | Subagent 使用隔离 git worktree |
| `claude --version` | 查看版本 |
| `claude --debug` | 调试模式 |

### 会话中常用 `/` 命令

> [!tip] 2026 年新增命令
> `/cd` `/code-review` `/usage` `/effort` `/checkup` `/fast` `/plan` `/todos` `/goal` 均为 2026 年新引入，旧版参考中可能未收录。

| 命令 | 作用 |
|------|------|
| `/model` | 切换模型（列出可选） |
| `/model claude-opus-4.8` | 直接切换到指定模型 |
| `/plan` | 强制规划/只读模式 |
| `/effort` | 设置努力级别（standard/high/xhigh） |
| `/fast` | 切换速度优化 API 设置 |
| `/cd <path>` | 切换工作目录（不重建缓存） |
| `/todos` | 跨会话持久化任务列表 |
| `/goal` | 保持工作直到完成条件满足 |
| `/code-review` | 报告正确性错误，`--fix` 直接修复 |
| `/memory` | 编辑 CLAUDE.md（不离开会话） |
| `/checkup` | 自诊断工具（清理/优化配置） |
| `/usage` | 查看配额使用明细（按 skill/agent/插件） |
| `/compact` | 压缩会话上下文释放空间 |
| `/context` | 显示 token 消耗 |
| `/cost` | 查看 Token 消耗与费用 |
| `/rewind` | 回滚到检查点 |
| `/fork` | 创建临时会话分支 |
| `/diff` | 查看会话的 git diff |
| `/init` | 创建 CLAUDE.md |
| `/clear` | 清除当前会话 |
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
> 详细的**三层记忆体系**（CLAUDE.md + Auto Memory + 自建参考文档）见 → [[#八、记忆系统]]

```bash
# 自动生成（推荐）
claude
/init
```

| 文件 | 位置 | 作用域 | 提交到 Git |
|------|------|--------|------------|
| `CLAUDE.md` | 项目根目录 | 项目级 | ✅ |
| `CLAUDE.local.md` | 项目根目录 | 项目级 | ❌ |
| `~/.claude/CLAUDE.md` | 用户目录 | 全局级 | ❌ |

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

## 八、记忆系统

> Claude Code 的记忆体系由三层构成：**CLAUDE.md（明规则）→ Auto Memory（隐规则）→ 自建参考文档（专项知识）**。三者配合，cc 越用越懂你。

### 8.1 三层记忆总览

| 层 | 位置 | 优先级 | 加载方式 | 谁在维护 |
|----|------|--------|----------|----------|
| 1 | CLAUDE.md（三级） | 高 | 会话启动全量加载 | 你手动维护 |
| 2 | Auto Memory | 中 | 先读索引、按需读子文件 | cc 自己写、你校对修改 |
| 3 | 参考文档 | 按需 | cc 遇到对应任务才读 | 你手动维护 |

> **本质认知**：agent 的所有"记忆"，本质上都是在合适的时候向大模型注入压缩过的上下文。这些机制本质上还是提示词工程，只不过由 cc 帮你组织了层次。

**选层决策树：**

```
这条信息是...
├── 团队所有人都要遵守的硬性规矩？
│   └── → 第一层 CLAUDE.md（提交到 git）
├── 你个人的开发偏好？
│   └── → 第一层 ~/.claude/CLAUDE.md（用户级）
├── 项目积累的经验教训、踩坑记录？
│   └── → 第二层 Auto Memory（让 cc 自己记）
├── 太长太专门、不需要每次都读的内容？
│   └── → 第三层 参考文档（按需加载）
└── 只在某些文件/目录下才适用的规则？
    └── → .claude/rules/ + paths: 元数据（路径范围规则）
```

---

### 8.2 第一层：CLAUDE.md

> **你主动立下的规矩**，会话启动时全量加载，第一优先级。

**三级 CLAUDE.md：**

| 级别 | 文件位置 | 作用域 | 共享 | 最佳用途 |
|------|---------|--------|------|----------|
| 项目级 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 项目 | 团队（提交 git） | 编码规范、架构决策、常用命令 |
| 用户级 | `~/.claude/CLAUDE.md` | 全局 | 个人 | 开发偏好、编辑器快捷键、沟通风格 |
| 本地级 | `./CLAUDE.local.md` | 项目 | 个人（不提交 git） | 个人项目特定设置 |

> [!tip] 官方建议
> - 限制 **200 行以内**，超长降低依从性
> - 子目录 `CLAUDE.md` 仅当读取目录内文件时加载，适合 monorepo
> - `.claude/rules/` + `paths:` 元数据：路径范围规则，触及时才加载，节省上下文预算

**快速更新 Memory：**

```
# 这个项目始终使用 TypeScript 严格模式

# new rule into memory
始终使用 Zod schemas 验证用户输入

# remember this
所有版本发布使用语义化版本号
```

---

### 8.3 第二层：Auto Memory（cc 自己的笔记本）

如果说 CLAUDE.md 是**你主动立下的规矩**，那 Auto Memory 就是 **cc 在干活过程中默默记下的设计笔记**。你没显式写进 CLAUDE.md 的习惯、反馈、项目踩坑，会被一个后台 agent 静静记录。

**如何启用：**

```bash
# 在 cc 会话中输入
/memory

# 在弹出的菜单里选第一个选项"启用 Auto Memory"
# 启用后菜单里会多出"打开自动记忆文件夹"选项
```

**Auto Memory 在磁盘上的样子：**

```
~/.claude/projects/<项目标识>/memory/
├── MEMORY.md          # 索引文件，启动时加载前 200 行
├── user/              # 关于你的信息
│   └── preferences.md
├── feedback/          # 你给过的反馈
│   └── 2026-07-28_dont-override-config.md
└── project/           # 项目进度与决策
    └── architecture-decisions.md
```

**Auto Memory 会记哪几类东西：**

| 类型 | 含义 | 举例 |
|------|------|------|
| `user` | 关于你 | 你的角色、偏好（如"不喜欢深色 UI"） |
| `feedback` | 你给过的反馈 | "不要这样做"、"对，就这样" |
| `project` | 项目相关 | 进度、决策、技术选型 |
| `reference` | 外部资源索引 | "某份设计文档在 docs/design.md" |

**使用手感（重要）：**

- 它只在当前项目生效（文件存在项目目录下），换项目需重新积累
- 启用后 cc 不会每次都把所有记忆全部加载进上下文，只会读一份 `MEMORY.md` 索引——**遇到具体问题才去读对应的子文件**，占 token 很少
- 随时可以用快捷键 `Ctrl+O` 在会话中查看实际被调用过的记忆内容
- 记错了就跟它说："忘掉刚刚说的不喜欢深色主题"，它会自己删掉
- 或者在 `/memory` 菜单里选"打开自动记忆文件夹"，直接编辑对应子文件

**已知局限性：**

- 记录频率有限——不会每句话都记，只在 cc 判断"值得记住"时才写
- 准确度取决于 cc 的判断，偶尔会记偏或漏记，建议定期校对

> 提示：**一句话区分 CLAUDE.md vs Auto Memory**：CLAUDE.md 是**第一优先级、全量注入的明规则**；Auto Memory 是**第二优先级、按需注入的隐规则**。两者配合，cc 越用越懂你。

---

### 8.4 第三层：自建参考文档（渐进式披露）

除了上面两层，你还可以仿照 Skill 的"渐进式披露"机制为 cc 手动打造一套**专项参考文档**。

**应用场景**：某些东西不适合全部塞进 CLAUDE.md（太长、太专门），但 cc 需要的时候必须能查到。比如：

- **品牌视觉规范**：颜色、字体、间距 → `docs/brand-visual.md`
- **产品文本风格**：语调、术语表 → `docs/copywriting-style.md`
- **API 约定**：请求响应格式、错误码 → `docs/api-conventions.md`

**两种实现模式：**

| 方式 | 做法 | 适合场景 |
|------|------|---------|
| CLAUDE.md 指引 | 在 CLAUDE.md 里写"改视觉时必读 docs/brand-visual.md" | 文档 1-3 份，内容稳定 |
| `@` 导入 | 在 CLAUDE.md 里用 `@docs/api-conventions.md` 直接引入 | 文档 4+ 份，或内容经常变 |

**CLAUDE.md 指引模式示例：**

```markdown
## 外部参考文档

- 修改前端视觉、调颜色、调间距时 → 必读 `docs/brand-visual.md`
- 写产品文案、按钮文字、提示语时 → 必读 `docs/copywriting-style.md`
- 写 API、定义返回格式时 → 必读 `docs/api-conventions.md`
```

这样 cc 只在"需要的时候"才去读完整文档，既保证了准确性，又不占多余上下文。

---

### 8.5 .claudeignore 文件

类似于 `.gitignore`，用来告诉 Claude Code 哪些文件/目录不需要关注。

**与 .gitignore 的核心区别：**

| 特性   | .gitignore        | .claudeignore           |
| ---- | ----------------- | ----------------------- |
| 控制谁  | git add/commit    | Claude Code 文件读取        |
| 默认忽略 | 无                 | `node_modules/`、`.git/` |
| 语法   | gitignore 风格 glob | 相同语法                    |
| 互相影响 | 不                 | 不                       |

**什么时候一定要配：**

| 情况 | 不配的后果 | 推荐规则 |
|------|-----------|---------|
| 有 `node_modules/` | cc 遍历巨量依赖文件，token 暴涨 | `node_modules/` |
| 有 `dist/`、`build/`、`.next/` | 构建产物干扰 cc 理解源码 | `dist/` `.next/` `build/` |
| 有 `.env` 等敏感文件 | 可能被 cc 读取并意外展示 | `.env` `.env.*` |
| 有大文件（如 `.pkl`、`.onnx`） | 尝试读取时超时或浪费 token | `*.pkl` `*.onnx` |

**实用模板：**

```gitignore
# === 依赖 ===
node_modules/
.pnp/
.pnp.js

# === 构建产物 ===
dist/
build/
.next/
out/
.cache/
.turbo/

# === 环境与密钥 ===
.env
.env.*
*.pem
*.key

# === 大文件 ===
*.onnx
*.pkl
*.bin
*.pt

# === 自动生成 ===
generated/
coverage/
.nyc_output/

# === 日志 ===
*.log
npm-debug.log*
```

**最佳实践：**

- 把 `.claudeignore` 提交到 Git，团队共享
- 只影响 cc 的**文件探索**，不影响你通过 `Read` 工具明确要求读取的文件

---

### 8.6 settings.json 记忆相关配置

```json
{
  // 排除某些 CLAUDE.md 不被加载（monorepo 场景）
  "claudeMdExcludes": [
    "packages/legacy-app/CLAUDE.md",
    "vendors/**/CLAUDE.md"
  ],

  // 自定义 Auto Memory 目录
  "autoMemoryDirectory": "/path/to/custom/memory",

  // 显式加载指定规则文件
  "rules": [
    "~/.claude/rules/security.md",
    ".claude/rules/api-design.md"
  ]
}
```

**环境变量控制 Auto Memory：**

| 变量 | 值 | 行为 |
|------|----|------|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `0` | 强制开启 |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `1` | 强制关闭 |
| （未设置） | — | 默认启用 |

```bash
# 禁用 Auto Memory
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude

# 强制启用
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0 claude
```

> settings.json 完整配置详解 → [[settings.json 配置详解]]

---

## 九、关联文档

[[Agent智能体]] · [[Claude Code 常用功能]] · [[Claude Code CLI 完整参考]] · [[Claude Code 会话管理]] · [[Claude Code 模型与推理设置]] · [[Claude MCP 使用指南]] · [[CLAUDE.md 使用指南]] · [[Subagents 完整指南]] · [[如何编写Skills]] · [[Skills 是什么]] · [[人工智能重要的六大概念体系]] · [[Git 入门教程]] · [[Git 命令速查]]

---

## 参考资料

### 官方
- [Claude Code 文档](https://code.claude.com/docs/en/overview)
- [What's New - 官方更新日志](https://code.claude.com/docs/en/whats-new)
- [Changelog](https://code.claude.com/docs/en/changelog)
- [GitHub 仓库](https://github.com/anthropics/claude-code)
- [Auto Mode 官方博客](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Subagents 官方博客](https://claude.com/blog/subagents-in-claude-code)
- [定制 Claude Code 官方博客](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

### 社区
- [claude-howto 学习指南](https://github.com/luongnv89/claude-howto)（21,800+ ⭐）
- [安装指南](https://www.morphllm.com/install-claude-code)
- [第三方 API 免登录配置](https://www.xugj520.cn/archives/windows-claude-code-api-setup-no-login.html)

### 跳过认证
- [CC-Switch（可视化供应商切换）](https://github.com/farion1231/cc-switch)
- [settings.json 详解](https://blog.csdn.net/tirestay/article/details/158808038)
