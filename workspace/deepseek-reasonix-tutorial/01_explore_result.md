# DeepSeek-Reasonix 配置教程 - 探测式收集结果

收集时间: 2026-08-10
状态: 阶段 1 探测式收集（3 个并行 subagent）

## 探测维度

| Subagent | 维度 | 覆盖方向 |
|----------|------|----------|
| 1 | 定位与对比 | 是什么、前缀缓存原理、与 Claude Code 关系 |
| 2 | 安装与配置 | 安装路径、setup 向导、reasonix.toml、运行模式、多模型协同 |
| 3 | CLI 与进阶 | CLI 命令、会话内命令、权限模式、MCP、ACP、缓存与成本 |

## 关键发现汇总

### 1. 定位与核心价值
- **是什么**: DeepSeek 原生的终端 AI 编程 agent（MIT 开源，单 Go 静态二进制），定位「可以一直开着跑的编码 Agent」，对标 Claude Code。
- **核心原理**: 围绕 DeepSeek **精确字节前缀缓存**做系统性工程。三区上下文设计：不可变前缀（system+工具定义，钉住只算一次）+ 只追加日志（绝不重写）+ 易变草稿（每轮重置不上送）。
- **实测效果**: 缓存命中率从普通 agent 的 <20% 提升到 2-3 轮后 ~94%，真实用户 4.35 亿 token 命中 99.82%；有缓存 $12 vs 无缓存 $61（节省约 80%）。
- **与 Claude Code 差异**: Claude Code 是通用多模型闭源 harness；Reasonix 是 DeepSeek 原生、专为一种缓存机制深度调优（明确不支持非 DeepSeek 后端）。但交互层刻意向 Claude Code 对齐（PR #6431 引入同款选择器、模式切换、headless 参数）。

### 2. 安装与配置
- **安装路径**（4 条，共用同一本地引擎）:
  - `npm i -g reasonix`（任意系统）
  - `brew install esengine/reasonix/reasonix`（macOS）
  - `npx reasonix code`（免安装临时用，需 Node≥22 + API Key）
  - 桌面端 `reasonix.io/?download=desktop`；VS Code 扩展 `SivanLiu.reasonix-agent`（需先装 CLI）
  - 源码 `make build` → 单静态二进制 `bin/reasonix`（darwin/linux/windows × amd64/arm64）
- **首次配置**: `reasonix setup` 向导（粘贴 API Key → 选 profile → 可选 MCP）。API Key 存 `~/.reasonix/config.json`（或全局 `<home>/.env`）。
- **配置文件**: `reasonix.toml`。关键字段：`default_model`；`[[providers]]`（name/kind/base_url/models/api_key_env/context_window/effort/prices）；`[agent]`（system_prompt/temperature/recovery_model/planner_model/subagent_models/max_subagent_concurrency）；`[tools].enabled`（空=全部内置）；`[[plugins]]`（MCP stdio/http）；`[sandbox]`、`[skills]`、`[ui]`、`[bot]`。API Key 绝不写入本文件，只写变量名 `api_key_env`。
- **配置优先级**: flag > `./reasonix.toml` > `~/.reasonix/config.toml`（v1.8.1+）。
- **运行模式澄清**: 官方无 smart/fast/max 三档（那是社区通俗说法）。官方是 **profile 三档**：`--profile economy|balanced|delivery`（TUI 内 `/work-mode` 切换）+ **effort** 深度（`/effort`，DeepSeek high|max）。
- **双模型协同**: `[agent] planner_model="deepseek-pro"` 一行启用（执行器+规划器），planner 看 REASONIX.md/AGENTS.md 记忆+只读工具，写入工具只给执行器，确定性路由。

### 3. CLI 与进阶
- **核心命令**: `reasonix` / `reasonix code [dir]`（默认 TUI 模式）、`chat`（纯聊天）、`run "<task>"`（无头一次性，适合 CI）、`doctor`（健康检查）、`update`、`acp`（stdio 后端，供编辑器/IDE 接入）、`sessions`/`prune-sessions`/`replay`/`diff`/`stats`/`mcp`/`index`/`commit`。
- **启动参数**: `--model`、`--profile`、`--effort`、`--max-steps`、`--dir`/`--add-dir`、`-c/--continue`、`-r/--resume`、`--permission-mode`、`--yolo`、`--budget <usd>`（成本上限）、`--metrics`、`--output-format text|json|stream-json`。
- **会话内命令**: `/init`（生成项目指令）、`/effort`、`/status`、`/model`、`/work-mode`、`/mcp`、`/skills`、`/memory`、`/rewind`、`/reload`、`/plan`、`/mode`、`/budget`、`/preset auto|flash|pro`。
- **权限模式 6 种**: manual/ask、auto、acceptEdits、dontAsk、plan、bypassPermissions(YOLO)。快捷键 `Shift+Tab` 循环 Ask→Auto→Plan，`Ctrl+Y` 独立切 YOLO，`Ctrl+P/Ctrl+N`/`j/k` 导航。
- **MCP**: 支持 stdio、Streamable HTTP、SSE。MCP over ACP。
- **ACP 协议**: NDJSON JSON-RPC 2.0 over stdio，能力协商含 loadSession、mcpCapabilities；session 生命周期 new/load/resume/prompt/cancel/list/close/delete；协作模式 normal/plan/goal。

### 4. 注意事项 / 常见坑
- 官方无 smart/fast/max 档位（社区混淆），官方为 profile 三档 + effort。
- `bash="enforce"` 在无 OS 沙箱的 Windows 上会拒绝执行。
- 无头模式默认 fail closed，需加 `--auto`。
- 旧字段（max_steps、auto_plan 等）会被自动忽略清理。
- v1 与 main-v2 文档 CLI 命令列表略有差异，以应用内 `/help`、`/keys` 为实时权威。
- 单请求成本实测可降至约 ¥0.0087（约 1 分钱/轮）。

## 方向菜单

基于探测结果，教程内容可按以下方向侧重。用户已选定「完整系列」，以下选项用于确定系列的结构侧重：

- **A. 完整四层结构（对齐 Claude Code 教程）**: 01-入门 / 02-基础功能 / 03-进阶应用 / 04-高级功能 + MOC
- **B. 配置为中心**: reasonix.toml 深度讲解、provider/agent/工具/插件声明、双模型协同
- **C. 对比迁移为中心**: 熟悉 Claude Code 的用户如何迁移，命令/交互/概念对照表
- **D. 成本优化为中心**: 前缀缓存原理、命中率调优、预算控制

## 核心信源

| 资料 | URL | 评分 | 类型 |
|------|-----|------|------|
| 官方 README（中文） | github.com/esengine/DeepSeek-Reasonix/blob/main-v2/README.zh-CN.md | 5/5 | 官方 |
| 官方配置示例 reasonix.example.toml | github.com/esengine/DeepSeek-Reasonix/blob/main-v2/reasonix.example.toml | 5/5 | 官方 |
| 官方配置指南 GUIDE.zh-CN.md | github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/GUIDE.zh-CN.md | 5/5 | 官方 |
| CLI 参考 CLI-REFERENCE.md (v1) | github.com/esengine/DeepSeek-Reasonix/blob/v1/docs/CLI-REFERENCE.md | 5/5 | 官方 |
| CLI.zh-CN.md (main-v2) | github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/CLI.zh-CN.md | 5/5 | 官方 |
| ACP 协议文档 | github.com/esengine/DeepSeek-Reasonix/blob/main-v2/docs/ACP.md | 5/5 | 官方 |
| 架构文档 ARCHITECTURE.md | github.com/esengine/DeepSeek-Reasonix/blob/v1/docs/ARCHITECTURE.md | 5/5 | 官方 |
| PR #6431 对齐 Claude Code CLI | github.com/esengine/DeepSeek-Reasonix/pull/6431 | 5/5 | 社区 |
| Issue #7907 缓存成本实测 | github.com/esengine/DeepSeek-Reasonix/issues/7907 | 5/5 | 社区 |
| CSDN 安装使用教程 | blog.csdn.net/qq_26086231/article/details/161143038 | 4/5 | 博客 |
| BAAI Hub 实测报道 | hub.baai.ac.cn/view/54971 | 4/5 | 博客 |
