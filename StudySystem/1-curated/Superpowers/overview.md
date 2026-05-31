# Superpowers - Overview

## What Is It

Superpowers 是一套面向 AI 编码代理的**完整软件开发方法论**，由 Jesse Vincent (obra) 开发。以可组合的 Skills 库为核心，通过自动触发机制让 AI 代理在正确的时机使用正确的技能。

- **核心理念**：不让代理直接写代码，而是先澄清需求、设计、计划，再执行
- **技术实现**：Markdown SKILL.md 文件 + YAML frontmatter 触发条件 + 各平台适配
- **支持平台**：Claude Code、Codex CLI/App、Gemini CLI、Cursor、OpenCode、Factory Droid、GitHub Copilot CLI（共 8 个）
- **设计约束**：零依赖，纯 Markdown 实现
- **License**：MIT
- **来源**：[obra/superpowers](https://github.com/obra/superpowers)

## Core Workflow (7 步)

```
brainstorming → using-git-worktrees → writing-plans → subagent-driven-development → TDD → code-review → finishing-branch
```

| 步骤 | Skill | 作用 |
|------|-------|------|
| 1 | brainstorming | Socratic 式对话澄清需求，分段展示设计 |
| 2 | using-git-worktrees | 创建隔离工作区（新分支） |
| 3 | writing-plans | 拆分为 2-5 分钟粒度任务 |
| 4 | subagent-driven-development | 每任务派发子代理 + 双重审查 |
| 5 | test-driven-development | RED-GREEN-REFACTOR 循环 |
| 6 | requesting-code-review | 任务间自动代码审查 |
| 7 | finishing-a-development-branch | 验证/合并/PR/保留/丢弃 |

## Philosophy

- **Test-Driven Development** — 先写测试，永远如此
- **Systematic over ad-hoc** — 系统化流程优于临时猜测
- **Complexity reduction** — 简洁是首要目标
- **Evidence over claims** — 验证后再声明成功

## Key Design Decisions

1. **Skills 自动触发**：代理看到相关场景时必须调用对应 Skill，不可跳过
2. **用户指令最优先**：CLAUDE.md / GEMINI.md > Superpowers Skills > 默认行为
3. **Human Partner 术语**：刻意使用"human partner"而非"the user"，强调协作关系
4. **Anti-rationalization**：每个 Skill 都有红旗表和反合理化机制，防止代理找借口跳过流程
