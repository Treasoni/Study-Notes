---
title: Codex CLI 与调试
tags: [codex, ai, 工具使用, 基础功能, cli]
created: 2026-07-31
updated: 2026-08-10
status: updated
source_project: codex-config
---

# Codex CLI 与调试

> [!info] 文档定位
> **一句话定位** - 本篇覆盖 Codex CLI 的高频日常操作与故障排查：核心命令、交互式命令、环境变量管理与配置验证技巧。适合已经完成配置、需要日常操作与排障参考的用户。

---

## 核心 CLI 命令

### 交互式 REPL 与单次执行

```bash
# 交互式 REPL（最常用）
codex

# 单次执行，输出结果后退出
codex exec "解释这个项目的 .gitignore"
```

### 工作目录与模型选择

```bash
# 指定工作目录启动
codex --cd /path/to/project

# 指定模型
codex --model gpt-5.4-mini

# 指定审批模式
codex --approval-mode on-request
```

`--cd` 的重要性：它在会话初始化前就设置了工作目录，确保 AGENTS.md 发现、`.codex/config.toml` 加载、技能索引等工作都基于正确的目录上下文。

### 状态查看、配置覆盖与配置档

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

### 选择原则

一条经验法则：

- **长期变更** → 修改 `config.toml` 或创建新 profile
- **临时实验** → `-c key=value`
- **按场景切换** → `--profile NAME`

---

## 交互式命令

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

---

## 环境变量

```bash
# CODEX_HOME — 重定向全局配置目录
export CODEX_HOME=/path/to/custom/codex-home

# API 认证
export OPENAI_API_KEY=sk-...

# .env 自动加载（会话启动时自动加载项目根目录的 .env 文件）
echo "OPENAI_API_KEY=sk-..." > .env
```

### .env 加载规则

- 只在项目根目录搜索，不遍历子目录
- 不会覆盖已存在的环境变量
- 加载时机在 AGENTS.md 发现和 config.toml 加载之前

---

## 调试与验证方法

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

---

## 配置审计技巧

### 快速诊断清单

```text
1. 配置文件在哪层？   → codex status | findstr "Config"
2. 配置项生效了吗？   → 检查是否写入了项目级但该键是"静默忽略"键
3. 指令文件加载了吗？ → codex exec "请列出所有加载的指令文件"
4. 技能发现了吗？     → /skills
5. Hook 注册了吗？    → /hooks
6. MCP 服务器能连吗？ → codex status 中查看 MCP 状态
```

### 常见故障案例

| 案例 | 症状 | 根因 | 对策 |
|------|------|------|------|
| 模型提供商配置不生效 | 设了 ollama 但仍调 OpenAI | `model_provider` 是静默忽略键 | 移到用户级配置 |
| 技能没有被自动加载 | description 匹配不上 | 触发词不够精准 | 调整 description 措辞 |
| SessionStart hook 没执行 | 启动时无效果 | 新 hook 默认 untrusted | 执行 `/hooks trust` |
| 配置文件变更后无效果 | 重启后配置未生效 | `CODEX_HOME` 指向了别处 | 确认正在修改的是正确路径 |

---

## 常见问题

### Q: 修改配置后不生效怎么办？

**回答**：按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序排查。先用 `codex status` 确认配置文件在哪一层、`CODEX_HOME` 是否指向正确路径；再确认该配置键是否属于项目级的"静默忽略"键（如 `model_provider`），若是则需移到用户级配置；最后用 `codex exec "请列出所有加载的指令文件"`、`/skills`、`/hooks` 逐项验证。

### Q: 如何确认当前加载了哪些配置、指令和技能？

**回答**：`codex status` 可以查看当前 workspace 状态，包括加载了哪些配置、指令和技能。`codex exec --cd /path/to/project "请列出你当前加载的所有指令文件和规则"` 可验证指令加载；技能发现和 hook 注册则在交互式会话中用 `/skills`、`/hooks` 验证。

### Q: CODEX_HOME 起什么作用？为什么改了配置没变化？

**回答**：`CODEX_HOME` 用于重定向全局配置目录。如果它指向了别处，你修改的配置文件可能不是实际生效的那一份，导致"重启后配置未生效"。排查时先确认 `CODEX_HOME` 的指向，再确认正在修改的是正确路径。

---

## 最佳实践

### Do's（推荐）

- 长期变更写入 `config.toml` 或创建新 profile；临时实验用 `-c key=value`；按场景切换用 `--profile NAME`
- 用 `codex --cd /path/to/project` 指定工作目录，确保 AGENTS.md 发现、`.codex/config.toml` 加载、技能索引都基于正确的目录上下文
- 调试优先用 `codex status` + 直接询问 agent（`codex exec "..."`）
- 排查故障按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序，覆盖 90% 场景

### Don'ts（避免）

- ❌ 把"静默忽略"键（如 `model_provider`）写在项目级配置里却不生效——应移到用户级配置
- ❌ 修改配置前不确认 `CODEX_HOME` 的指向——可能改的不是实际生效的配置文件
- ❌ 忘记新 hook 默认 untrusted——SessionStart hook 没执行时先 `/hooks trust`
- ❌ 只凭直觉猜测配置层级，而不用 `codex status` 验证

---

## 小结

四条核心 CLI 命令覆盖日常操作——`codex`、`codex exec`、`codex status`、`codex --cd`。`/skills`、`/hooks`、`/config` 三个交互式命令管理运行时状态。CODEX_HOME、OPENAI_API_KEY、.env 三个环境变量控制运行时行为。调试优先用 `codex status` + 直接询问 agent，常见故障按"配置层 → 指令加载 → 技能发现 → hook 状态 → MCP 状态"的顺序排查即可覆盖 90% 场景。

---

## 相关文档

| 文档 | 说明 |
|------|------|
| [[config.toml 核心配置]] | 核心配置文件与配置项 |
| [[Hooks 与插件]] | 生命周期钩子与插件体系 |
| [[快速参考卡片]] | CLI 命令速记与默认值速查 |
| [[Codex MOC]] | 返回目录 |

---

## 参考资料

- [OpenAI Codex 文档](https://developers.openai.com/codex/)
- [OpenAI Codex GitHub](https://github.com/openai/codex)

---

## 更新记录

- 2026-08-10：重构为 Claude Code 教程风格，重排分节并补齐 FAQ/最佳实践/相关文档。
