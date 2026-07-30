---
title: "Codex 完整配置体系"
tags: [codex, claude-code, configuration]
created: 2026-07-31
updated: 2026-07-31
status: completed
source_project: codex-config
---

# 第七章：CLI 与调试 —— 日常操作与故障排查
前六章我们把 Codex 的配置体系拆了个遍——从 config.toml 到 AGENTS.md，从 skills 到 hooks，每个子系统都有自己的配置文件和加载规则。但配置再多，最终你每天打交道的是 CLI。本章不做命令参考手册，只聚焦高频的日常操作命令、环境变量管理和配置验证技巧。

### 1. 核心 CLI 命令

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

`--cd` 的重要性：它在会话初始化前就设置了工作目录，确保 AGENTS.md 发现、`.codex/config.toml` 加载、技能索引等工作都基于正确的目录上下文。

```bash
# 查看当前 workspace 状态（加载了哪些配置、指令、技能）
codex status

# 临时覆盖单个配置项
codex -c model=gpt-5.4-mini -c approval_policy=never

# 使用特定配置档
codex --profile fast

# 管理 MCP 服务器
codex mcp add
```

一条经验法则：
- **长期变更** → 修改 `config.toml` 或创建新 profile
- **临时实验** → `-c key=value`
- **按场景切换** → `--profile NAME`

### 2. 交互式命令

```bash
# 技能管理
/skills

# 钩子管理
/hooks

# 交互式配置（仅当前会话生效）
/config
/config set model=gpt-5.4-mini
/config get sandbox_mode

# 提交反馈
/feedback
```

### 3. 环境变量

```bash
# CODEX_HOME — 重定向全局配置目录
export CODEX_HOME=/path/to/custom/codex-home

# API 认证
export OPENAI_API_KEY=sk-...

# .env 自动加载（会话启动时自动加载项目根目录的 .env 文件）
echo "OPENAI_API_KEY=sk-..." > .env
```

`.env` 加载规则：
- 只在项目根目录搜索，不遍历子目录
- 不会覆盖已存在的环境变量
- 加载时机在 AGENTS.md 发现和 config.toml 加载之前

### 4. 调试与验证方法

```bash
# 验证指令加载
codex status
codex exec --cd /path/to/project "请列出你当前加载的所有指令文件和规则"

# 验证技能发现（在交互式会话中）
/skills

# 验证 hook 注册（在交互式会话中）
/hooks

# 审计 session JSONL
ls ~/.codex/transcripts/
head -100 ~/.codex/transcripts/session_20240731_001.jsonl

# 查看日志
export CODEX_LOG_LEVEL=debug
codex
```

### 5. 配置审计技巧

快速诊断清单：

```text
1. 配置文件在哪层？   → codex status | findstr "Config"
2. 配置项生效了吗？   → 检查是否写入了项目级但该键是"静默忽略"键
3. 指令文件加载了吗？ → codex exec "请列出所有加载的指令文件"
4. 技能发现了吗？     → /skills
5. Hook 注册了吗？    → /hooks
6. MCP 服务器能连吗？ → codex status 中查看 MCP 状态
```

常见故障案例：

| 案例 | 症状 | 根因 | 对策 |
|------|------|------|------|
| 模型提供商配置不生效 | 设了 ollama 但仍调 OpenAI | `model_provider` 是静默忽略键 | 移到用户级配置 |
| 技能没有被自动加载 | description 匹配不上 | 触发词不够精准 | 调整 description 措辞 |
| SessionStart hook 没执行 | 启动时无效果 | 新 hook 默认 untrusted | 执行 `/hooks trust` |
| 配置文件变更后无效果 | 重启后配置未生效 | `CODEX_HOME` 指向了别处 | 确认正在修改的是正确路径 |

> **本章小结**：四条核心 CLI 命令覆盖日常操作——`codex`、`codex exec`、`codex status`、`codex --cd`。`/skills`、`/hooks`、`/config` 三个交互式命令管理运行时状态。CODEX_HOME、OPENAI_API_KEY、.env 三个环境变量控制运行时行为。调试优先用 `codex status` + 直接询问 agent。常见故障按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序排查，覆盖 90% 场景。

---


---

> [!note] 导航
> [[06 Hooks 与插件|← 上一章]] | [[08 对照表与迁移实战|下一章 →]]



