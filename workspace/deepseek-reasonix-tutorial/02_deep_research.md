# DeepSeek-Reasonix 配置教程 - 深度素材

收集时间: 2026-08-10
状态: 阶段 2 深度收集（4 个并行精读 subagent，官方文档 + 社区实测）
信源: 官方仓库 esengine/DeepSeek-Reasonix（README.zh-CN / GUIDE.zh-CN / reasonix.example.toml / CLI-REFERENCE(v1) / CLI.zh-CN(main-v2) / ACP.md / ARCHITECTURE.md）+ PR #6431 + Issue #7907 + 第三方实测

---

## 一、产品定位与核心原理

### 1.1 是什么
- DeepSeek 原生的终端 AI 编程 agent，MIT 开源，**单 Go 静态二进制**（CGO_ENABLED=0），定位「可以一直开着跑的编码 Agent」。
- 一套本地引擎，四个入口：终端 / 桌面 / 浏览器 / ACP 编辑器。
- 用计划模式、权限、工作区沙箱与逐轮 checkpoint 保证长时自治运行可读、可撤销。
- 仓库：https://github.com/esengine/DeepSeek-Reasonix （33.6k stars / 2.2k forks）
- **注意**：provider 体系是插件式、`reasonix.toml` 声明、内核无硬编码模型。官方文档未出现「不支持非 DeepSeek 后端」的显式断言，教程写作应以 provider 声明机制为准，不绝对断言。

### 1.2 前缀缓存原理（架构文档 ARCHITECTURE.md）
- DeepSeek 自动前缀缓存只在「上一请求的**精确字节前缀**完全匹配」时生效；前缀内任何早期改动都会使缓存失效。
- 命中缓存输入按**未命中的 ~10%** 计费。
- 无纪律的 agent 循环每轮重排/重写/注入时间戳，实测命中率 **<20%**。
- **三区上下文设计**（CacheFirstLoop）：
  | 区域 | 内容 | 行为 |
  |------|------|------|
  | IMMUTABLE PREFIX 不可变前缀 | system + tool_specs + few_shots | 会话内固定，每会话算一次并钉住 |
  | APPEND-ONLY LOG 只追加日志 | [assistant₁][tool₁][assistant₂]... | 单调追加，绝不重写 |
  | VOLATILE SCRATCH 易变草稿 | R1 思维、临时计划 | 每轮重置，永不直接上送，先经 Tool-Call Repair 蒸馏 |
- 三条不变量：前缀只算一次并固定；日志按追加顺序序列化不重写；草稿先蒸馏再折叠进日志。
- 可观测性：命中率 = `prompt_cache_hit_tokens / (hit + miss)`，逐轮计算，显示在 TUI 顶栏缓存单元格。

### 1.3 缓存友好工程实践
- 并行工具分发：工具声明 `parallelSafe?: boolean`，`Promise.allSettled` 竞争，但工具结果与历史追加**仍按声明顺序落盘**。环境变量 `REASONIX_PARALLEL_MAX`（默认 3，上限 16）、`REASONIX_TOOL_DISPATCH=serial` 强制串行。
- **Pillar 2 Tool-Call Repair 四轮修复**：flatten（压平深层 schema）、scavenge（从 reasoning_content 回收漏写的工具调用）、truncation（补不平衡 JSON）、storm（滑动窗口抑制重复 (tool,args) 元组）。
- 轮末自动压缩：日志中超过 `TURN_END_RESULT_CAP_TOKENS`（3000）的工具结果在轮末压缩，读到的那轮保留全文，后续看紧凑摘要可重读。
- 辅助调用分层定价：摘要、subagent 生成、截断修复一律硬编码 `v4-flash + effort=high`，不随 preset 走。

### 1.4 成本实测数据
- 官方口径：无纪律 <20% 命中；前沿模型活跃用户 $150–250/月；北极星 =「便宜到可以常开的编码 agent」。
- Issue #7907 用户实测（本地 stats 与计费控制台对账）：8/8 命中率 **99.6%**；成本 ¥1.37/全天 158 请求，单请求 **¥0.00869**（约 1 分钱/轮）；优化后成本 -55~60%；最大 miss 约 2K/请求，无 >10K 缓存打穿。
- 第三方实测（智源社区报道，项目自报非独立评测）：单日 4.35 亿输入 token 命中率 **99.82%**；$61 → $12（约 2 折，节省约 80%）；长会话保证命中率 90%+。

---

## 二、安装与首次配置

### 2.1 安装路径（4 条，共用同一本地引擎）
| 路径 | 命令/操作 | 前置要求 | 适用场景 |
|------|-----------|---------|---------|
| A. CLI (npm) | `npm i -g reasonix` | Node/npm | 任意系统，自动拉平台原生二进制 |
| A. CLI (brew) | `brew install esengine/reasonix/reasonix` | Homebrew | macOS |
| B. 免安装 | `npx reasonix code` | Node≥22 + API Key | 临时用，每次自动拉最新版 |
| C. 桌面端 | 官方下载页 `reasonix.io/?download=desktop` | — | macOS `.dmg`/`.zip`，Windows `.exe`/`.zip`，Linux `.deb`/`.tar.gz` |
| D. VS Code 扩展 | Marketplace/Open VSX 安装 `SivanLiu.reasonix-agent` | **先装 CLI**，扩展启动本地 `reasonix acp` 后端 | VS Code / VSCodium |
| E. 源码 | `git clone` + `make build` → `bin/reasonix` | Go 工具链 | 定制构建；`make cross` 跨 6 平台 |

### 2.2 首次配置 `reasonix setup`
- 作用：配置 provider 和模型；统一管理 provider、模型列表、凭据、连接测试、默认模型。
- 交互：修改暂存到「保存并退出」统一生效；同步维护桌面端 provider access。
- API Key 存储：config 只存 `api_key_env` **变量名**，真实密钥在全局 `<Reasonix home>/.env`（macOS/Linux `~/.reasonix/`，Windows `%AppData%\reasonix\`）。
- 项目 `.env` 只作 MCP/plugin 的 `${VAR}` 展开来源，**不导入 provider key**。
- 需要项目指令时在会话中运行 `/init` 生成 `REASONIX.md` / `AGENTS.md`。

---

## 三、reasonix.toml 配置详解（配置为中心的核心素材）

### 3.1 顶层与 providers
```toml
default_model = "deepseek"           # provider 名或 "provider/model"
# language = "zh"

[[providers]]
name = "deepseek"
kind = "openai"                      # openai|anthropic
base_url = "https://api.deepseek.com"
models = ["deepseek-v4-flash", "deepseek-v4-pro"]
default = "deepseek-v4-flash"
api_key_env = "DEEPSEEK_API_KEY"
context_window = 1000000
effort = "high"                      # high|max；DeepSeek 思考恒开

[[providers]]
name = "claude"
kind = "anthropic"                   # 用 Messages API，不发送 temperature
model = "claude-opus-4-8"
api_key_env = "ANTHROPIC_API_KEY"
context_window = 1000000
thinking = "adaptive"
effort = "high"                      # low|medium|high|xhigh|max
```
- 单模型共用 `model = "..."`；多模型共享端点用 `models = [...]`。
- 可选字段：`reasoning_protocol`（auto|deepseek|openai|none）、`supported_efforts`、`default_effort`、`auth_header`（bool，Bearer 鉴权网关用）、`prices`（自定义计价）。
- Anthropic 兼容端点示例：`kind = "anthropic"` + `base_url = "https://api.deepseek.com/anthropic"`。

### 3.2 [agent]
```toml
[agent]
# system_prompt / system_prompt_file
temperature = 0.0
# recovery_model = ""
# reasoning_language = "auto"        # auto|zh|en
soft_compact_ratio = 0.5             # 缓存优先压缩提示
tool_result_snip_ratio = 0.6
compact_ratio = 0.8
compact_force_ratio = 0.9
# planner_model = "deepseek-pro"     # 双模型协同
# subagent_model = "deepseek-pro"
# subagent_models = { review = "deepseek-pro", security_review = "deepseek-pro" }
# max_subagent_concurrency = 6
# max_parallel_writers = 3
# output_style = "explanatory"       # explanatory|learning|concise
```

### 3.3 [environment] / [tools] / [permissions]
```toml
[environment]
enabled = true
offline = false

[tools]
enabled = []                         # 空 = 启用全部内置工具
bash_timeout_seconds = 120
mcp_startup_timeout_seconds = 30
mcp_call_timeout_seconds = 300

[permissions]
mode = "ask"                         # ask|allow|deny 兜底
deny  = ["Bash(rm -rf*)", "Bash(git push*)"]
allow = ["Bash(go test:*)"]
```

### 3.4 [sandbox] / [skills] / [[plugins]] / [ui] / [serve] / [bot]
```toml
# [sandbox]
# workspace_root = ""
# allow_write = ["/tmp"]
# forbid_read = ["${HOME}/.ssh"]
# bash = "enforce"                   # enforce|off；Windows 强制 off
# network = true

# [skills]
# paths = ["~/my-skills", "../shared/skills"]
# excluded_paths = ["~/.agents/skills"]
# disable_implicit_invocation = true
# disabled_skills = ["review"]

# [[plugins]]                        # MCP/外部 stdio 插件
# name = "example"
# command = "reasonix-plugin-example"

[ui]
theme = "auto"                       # auto|dark|light
show_turn_usage = true               # 显示每次请求 token 与费用

[notifications]
enabled = false
turn_done = true
approval_request = true

# [bot]  # QQ/飞书/微信多通道机器人，见 reasonix.example.toml
```

### 3.5 运行模式与模型（重要澄清）
- **官方无 smart/fast/max 三档**（那是社区对 `/effort` 的通俗说法）。
- **Profile 三档**：`--profile economy|balanced|delivery`，TUI 内 `/work-mode` 热切换（`/profile` 为兼容别名）。
  - **Economy**：初始只带 9 个工具，其余按需连接。
  - **Balanced**：完整工具面的默认档。
  - **Delivery**：完整工具面 + 稳定能力代理 `use_capability`，强制交付合约。
- **effort**：`/effort` 控制推理深度（DeepSeek high|max）。
- **双模型协同**：`[agent] planner_model = "deepseek-pro"` 一行启用（执行器 + 规划器）。Planner 看 REASONIX.md/AGENTS.md 记忆 + 只读研究工具，写入工具只给执行器，确定性路由不额外调 classifier。

### 3.6 配置优先级与安全
- 解析顺序：**flag > `./reasonix.toml` > 用户全局配置（`~/.reasonix/config.toml`）> 内置默认**。
- API Key 安全：config 只存变量名，真实值在全局 `.env`；项目 `.env` 不导入 provider key；Reasonix 从工具子进程移除已保存凭据。
- Hooks 不在 reasonix.toml，而在 `<Reasonix home>/settings.json`（全局）与 `<project>/.reasonix/settings.json`（项目）。

---

## 四、CLI 与会话（基础功能/进阶素材）

### 4.1 核心命令
| 命令 | 用途 | 示例 |
|------|------|------|
| `reasonix` / `reasonix code [dir]` | 交互式代码模式 TUI（默认） | `reasonix code .` |
| `reasonix chat` | 纯聊天，无文件系统/shell | `reasonix chat` |
| `reasonix run "<task>"` | 无头一次性执行，CI 友好 | `reasonix run "把 main.go 的 TODO 实现掉"` |
| `reasonix setup` | 首次配置向导 | `reasonix setup` |
| `reasonix doctor` | 健康检查（API/配置/hooks/项目） | `reasonix doctor` |
| `reasonix upgrade` / `update` | 升级（别名） | `reasonix upgrade --check` |
| `reasonix acp` | ACP stdio 后端，供编辑器/IDE | `reasonix acp --model deepseek-pro` |
| `reasonix sessions` / `prune-sessions --days N` | 会话管理 | `reasonix sessions` |
| `reasonix stats [transcript]` | 一次性 cost/cache 分解 | `reasonix stats` |
| `reasonix mcp list/search/install/inspect` | MCP 管理 | `reasonix mcp list` |
| `reasonix replay <jsonl>` / `diff <a> <b>` | 转录重放/对比 | — |
| `reasonix commit` | git add + commit（LLM 写信息） | `reasonix commit` |
| `reasonix index` | 本地语义索引 | — |

### 4.2 常用启动参数
| 参数 | 作用 |
|------|------|
| `--model NAME` | 选 provider 或 `provider/model` |
| `--profile economy\|balanced\|delivery` | 运行时工作模式 |
| `--effort LEVEL` | 覆盖推理强度 |
| `--max-steps N` | 工具调用轮数上限，0=自动 |
| `--dir PATH` | 工作区根目录 |
| `--add-dir PATH` | 追加可写目录（可重复） |
| `-c` / `--continue` | 恢复最近会话 |
| `-r` / `--resume [QUERY]` | 会话选择器 / 按子串恢复 |
| `--copy` | 复制会话在可写副本继续 |
| `--allowed-tools RULES` | 仅本次会话权限放行（可重复） |
| `--permission-mode MODE` | ask/auto/acceptEdits/dontAsk/plan/bypassPermissions |
| `--yolo` | 跳过权限（bypassPermissions 别名） |
| `-p` / `--print` | 一次性只输出最终答案 |
| `--output-format text\|json\|stream-json` | 结构化输出 |
| `--auto` / `-y` | permission-mode auto 别名（不能与显式 --permission-mode 组合） |
| `--budget <usd>` | 会话成本上限（80% 警告/100% 拒绝）【v1】 |
| `--ablate LIST` | 基准测量，禁用子系统（测量工具非调优） |
| `--trajectory PATH` / `--metrics PATH` | 事件流/指标输出 |

### 4.3 会话内斜杠命令
- **main-v2**：`/help` `/model` `/provider` `/resume` `/status` `/work-mode`（`/profile` 别名）`/theme` `/currency` `/effort` `/output-style` `/verbose` `/sandbox` `/goal` `/docs [问题]` `/mcp` `/skills` `/hooks` `/remember <note>` `/memory` `/rewind` `/tree` `/branch` `/switch` `/reload` `/paste-image` `/mouse`
- **v1 特有**：`/new` `/retry` `/compact` `/copy` `/preset auto|flash|pro` `/cost` `/context` `/stats` `/doctor` `/keys` `/prompt` `/resource` `/skill` `/init [force]` `/apply` `/discard` `/walk` `/undo` `/commit` `/mode review|auto|yolo` `/plan` `/checkpoint` `/restore` `/cwd` `/jobs` `/kill` `/budget` `/search-engine` `/permissions` `/loop <interval> <prompt>` `/exit`
- **版本差异提醒**：main-v2 的 CLI.zh-CN **未收录** `/init`、`/plan`、`/mode`、`/budget`、`/preset` 等（这些在 v1 CLI-REFERENCE）；main-v2 强调 `/work-mode`、`/currency`、`/docs`、`/reload`。教程应以应用内 `/help` 为实时权威。

### 4.4 权限模式与快捷键
- **6 种权限模式**：`manual/ask`（弹审批）、`auto`（自动批准普通操作）、`acceptEdits`（只放行文件编辑）、`dontAsk`（拒绝不弹窗）、`plan`（只读 Plan）、`bypassPermissions`（YOLO）。
- **非交互 fail-closed**：默认 ask/manual 拒绝显式 Ask 决定与普通写 fallback；bypassPermissions 仍遵守 deny、Sandbox、需人工审批的工具。
- **快捷键**：`Up/Down`、`Ctrl+P/Ctrl+N` 选择器移动；`j/k` 搜索为空时移动；`Shift+Tab` 循环 Ask→Auto→Plan；`Ctrl+Y` 独立切 YOLO；`Enter` 选中、`Esc` 取消；`y/a/p/n`+数字对应审批动作。
- 编辑门控：`y/n` 接受/丢弃待定编辑；`u` 撤销最近自动应用批次。
- 图片粘贴：mac/Linux `Ctrl+V`、Windows `Alt+V`、或 `/paste-image`。

---

## 五、进阶能力（高级功能素材）

### 5.1 MCP
- 支持 **stdio、Streamable HTTP、legacy SSE** 三类 server。
- 命令行管理：`reasonix mcp list/search/install/inspect/browse`。
- MCP over ACP：`session/new`、`session/load`、`session/resume` 可带 `mcpServers`。
- stdio 的 `env` 与 HTTP 的 `headers` 支持官方 ACP 形状 `[{"name":"...","value":"..."}]`。

### 5.2 ACP 协议（供编辑器/IDE 接入）
- **ACP v1**：NDJSON JSON-RPC 2.0 over stdio；stdout 专用 ACP 消息、诊断走 stderr。
- 启动：`reasonix acp`、`reasonix acp --model deepseek-pro`、`reasonix acp --profile delivery`。
- 能力协商：`agentCapabilities` 含 `loadSession`、`sessionCapabilities`、`promptCapabilities`（embeddedContext: true）、`mcpCapabilities`（http: true, sse: false）、`_meta["reasonix.io"]`（sessionSteer/sessionInbox/reloadExtensions）。
- **session 生命周期**：`session/new`、`session/load`、`session/resume`、`session/prompt`、`session/cancel`、`session/list`、`session/close`、`session/delete`。
- **协作模式**：`normal` / `plan` / `goal`（旧 default/auto 映射 Normal+Ask / Normal+Yolo）。
- **工具审批**：`configOptions.tool_approval` = `ask`/`auto`/`yolo`，经 `session/set_config_option` 设置（**字段是 `configId`** 而非 optionId）。
- 客户端通告 `fs.readTextFile`/`fs.writeTextFile`/`terminal` 时，文件操作路由到编辑器未保存缓冲区、前台命令路由到客户端终端。

### 5.3 插件与扩展
- **Extension Protocol v1 Sidecar**：MCP server 提供工具/提示词/资源；Sidecar 拦截运行时事件、提供 Provider 与结构化 UI，经**版本化插件包分发**。
- 详细文档：`docs/EXTENSIONS.zh-CN.md`、`docs/EXTENSION_PROTOCOL.zh-CN.md`、`docs/PLUGIN_PACKAGES.zh-CN.md`、`sdk/go/README.md`。
- 插件管理走 `reasonix.toml` 配置声明，无独立插件子命令。

### 5.4 自动化与 CI
- `reasonix run "<task>"` 无头执行，支持管道输入 `echo "..." | reasonix run`。
- 结构化输出：`--output-format json` / `stream-json`。结果对象字段：`type:"result"`、`subtype`、`is_error`、`duration_ms`、`num_turns`、`result`、`session_id`、`total_cost`、`currency`（ISO）、`total_cost_usd`（同值不换算）、`usage`（input/output/cache_read_input/cache_creation_input tokens）。
- `--events-jsonl PATH`：脱敏生命周期遥测，不能与 `--output-format` 组合。
- CI 只读接口：`session list/show/status/recovery`、`task list/show`、`task monitor ...`、`hook list/status`，支持 `--json`。
- 参数错误退出码 2，状态/查询错误退出码 1。

---

## 六、与 Claude Code 对比迁移（对比迁移为中心素材）

### 6.1 命令对照表
| Claude Code | Reasonix | 说明 |
|---|---|---|
| `claude` | `reasonix` | 交互式 CLI |
| `claude -p "<task>"` | `reasonix -p "<task>"` / `reasonix run "<task>"` | 一次性模式 |
| `claude --output-format json` | `reasonix --output-format json` | 另支持 stream-json |
| `claude --allowed-tools <t>` | `reasonix --allowed-tools <t>` | session-allow 作用域 |
| `claude --add-dir <path>` | `reasonix --add-dir <path>` | 可重复 |
| `claude --permission-mode <m>` | `reasonix --permission-mode <m>` | auto/dontAsk/yolo/bypassPermissions |
| `claude --continue` | `reasonix --continue` | 保留 |
| `claude --resume` | `reasonix --resume=true/false` | 保留 |
| `/model`、`/provider`、`/resume` | 对齐（picker 方向键/Vim/Ctrl+P/N） | PR #6431 |
| `Shift+Tab` 模式循环 | Ask / Auto / Plan | Ctrl+Y 独立 YOLO |
| Ask/Auto/Yolo 审批 | `configOptions.tool_approval` = ask/auto/yolo | ACP surface |
| `claude` MCP 配置 | `mcpServers` | MCP over ACP |

### 6.2 概念对照
- 协作模式三态 `normal`/`plan`/`goal`（对应 Claude 的交互/plan 模式）。
- 工具审批三态 `ask`/`auto`/`yolo`。
- 工作 profile：`economy`/`balanced`/`delivery`。
- 记忆文件：Claude Code 用 `CLAUDE.md`；Reasonix 用 `REASONIX.md` / `AGENTS.md`（`/init` 生成）。
- Hooks：Claude Code 用 `settings.json` hooks；Reasonix hooks 也在 settings.json（`<Reasonix home>/settings.json` 全局 + `<project>/.reasonix/settings.json` 项目）。

### 6.3 差异点
- **核心差异**：Claude Code 是通用多模型闭源 harness；Reasonix 围绕 DeepSeek 前缀缓存深度调优。Provider 机制是插件式，可在 reasonix.toml 声明其他 OpenAI/Anthropic 兼容端点（教程以文档为准，不做绝对断言）。
- 工具审批经 ACP 协议暴露（`session/set_config_option` + `session/request_permission`），不是本地键盘循环——影响 ACP host 集成方。
- headless 一次性路径审批超时默认 infinite；`--copy` 提示转 stderr 保证 stdout 纯 machine-readable。
- 成本：DeepSeek 缓存价约 ¥0.02/1M vs 未缓存 ¥1/1M（约 50 倍单价差）；Reasonix 命中率 94-99.8%，长会话输入成本约 1/5。

---

## 七、常见坑与最佳实践（贯穿各章）

1. **配置优先级**：flag > `./reasonix.toml` > 全局 `~/.reasonix/config.toml` > 内置默认。
2. **API Key 安全**：config 只写 `api_key_env` 变量名，真实值只在全局 `<Reasonix home>/.env`；项目 `.env` 不导入 provider key。
3. **Windows 沙箱**：Reasonix 不在 Windows 提供 OS 级 Bash 沙箱，`bash="enforce"` 解析为 off；无沙箱环境 enforce 会拒绝 bash 执行（macOS 用 Seatbelt、Linux 用 bubblewrap）。
4. **无头 fail-closed**：无人值守需 `reasonix run --auto` / `-y` / `--permission-mode auto`。
5. **`--allowed-tools` 是权限覆盖不是 schema 过滤**；配置 deny 永远压过 CLI allow。
6. **`--auto` 不能与显式 `--permission-mode` 组合**；`--events-jsonl` 不能与 `--output-format` 组合。
7. **破坏缓存命中的操作**：重排上下文、重写旧日志、每轮注入时间戳 → 命中率 <20%。三区设计就是对抗这些。
8. **旧字段废弃**：`agent.auto_plan`、`agent.max_steps`、MCP 旧字段会被忽略并在保存时移除；改用 `--max-steps`。
9. **版本差异**：v1 与 main-v2 的 CLI 文档命令列表不同，教程以应用内 `/help`、`/keys` 为实时权威。
10. **`--ablate` 是测量工具不是调优开关**，禁用子系统只会让 Reasonix 更差。

---

## 八、进阶路径 / 学习资源

- 官方仓库 README：https://github.com/esengine/DeepSeek-Reasonix
- 中文 README：`main-v2/README.zh-CN.md`
- 配置指南：`main-v2/docs/GUIDE.zh-CN.md`、`docs/CONFIG_PATHS.zh-CN.md`
- 配置示例：`main-v2/reasonix.example.toml`
- CLI 参考：`v1/docs/CLI-REFERENCE.md`、`main-v2/docs/CLI.zh-CN.md`
- ACP：`main-v2/docs/ACP.md`（+ ACP.zh-CN.md）
- 架构：`v1/docs/ARCHITECTURE.md`
- 扩展/插件：`docs/EXTENSIONS.zh-CN.md`、`docs/EXTENSION_PROTOCOL.zh-CN.md`、`docs/PLUGIN_PACKAGES.zh-CN.md`、`sdk/go/README.md`
- 对齐 PR：https://github.com/esengine/DeepSeek-Reasonix/pull/6431
- 成本实测：https://github.com/esengine/DeepSeek-Reasonix/issues/7907
- 社区教程：CSDN https://blog.csdn.net/qq_26086231/article/details/161143038
- 第三方报道：https://hub.baai.ac.cn/view/54971

## 素材质量统计

- 官方文档：10+ 篇（README/README.zh-CN/GUIDE/CONFIG_PATHS/CLI-REFERENCE/CLI.zh-CN/ACP/ARCHITECTURE/EXTENSIONS/PLUGIN_PACKAGES）
- 官方示例：reasonix.example.toml（262 行，权威字段来源）
- 社区实测：Issue #7907（命中率/成本对账）、PR #6431（Claude Code 对齐）
- 教程/博客：CSDN 教程、智源 BAAI 报道
