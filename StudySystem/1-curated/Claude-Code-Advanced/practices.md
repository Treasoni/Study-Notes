# 实战示例 - Claude Code 高级使用技巧

## 1. 环境配置

### 1.1 编写有效的 CLAUDE.md

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible

# Workflow
- Typecheck after making series of code changes
- Prefer running single tests, not whole suite for performance
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

### 1.2 创建 Skills

```markdown
# .claude/skills/fix-issue/SKILL.md
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get issue details
2. Search codebase for relevant files
3. Implement changes
4. Write and run tests
5. Ensure code passes linting
6. Create PR
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

### 1.3 定义 Subagent

```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities
- Authentication flaws
- Secrets in code
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

---

## 2. 会话管理

### 2.1 战略性上下文压缩

```bash
# 禁用自动压缩，获得更多控制
/claude --config disable-auto-compact

# 手动在逻辑断点压缩
/compact Focus on API changes
```

**来源**：[32 Tips - YK](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)

### 2.2 动态系统提示注入

```bash
# 使用 CLI 标志动态注入上下文
claude --system-prompt "$(cat memory.md)"

# 创建场景别名
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 2.3 记忆持久化钩子配置

```json
{
  "hooks": {
    "PreCompact": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/pre-compact.sh"
      }]
    }],
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/session-start.sh"
      }]
    }],
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/memory-persistence/session-end.sh"
      }]
    }]
  }
}
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

---

## 3. Token 优化

### 3.1 模型选择策略

| 场景 | 推荐模型 | 原因 |
|------|----------|------|
| 重复性任务 | Haiku | 便宜快速 |
| 90% 编码任务 | Sonnet | 性价比高 |
| 5+ 文件任务 | Opus | 强推理能力 |
| 架构决策 | Opus | 复杂推理 |
| 安全关键代码 | Opus | 最高质量 |

```bash
# 切换模型
/model haiku
/model sonnet
/model opus
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 3.2 工具优化

```bash
# 用 mgrep 替代 grep（节省约 50% tokens）
mgrep -r "pattern" .

# 在 agent 定义中指定模型
---
name: quick-search
description: Fast file search
tools: Glob, Grep
model: haiku
---
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 3.3 后台进程外执行

```bash
# 用 tmux 运行长时间任务，不让 Claude 处理全部输出
tmux new -d -s long-running 'npm run build'
# 稍后查看输出或汇总
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

---

## 4. 验证工作流

### 4.1 带验证标准的任务

```
"implement validateEmail function.
Test cases: user@example.com → true, invalid → false, user@.com → false.
Run tests after implementation."
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

### 4.2 探索-计划-实现模式

```text
# Phase 1: Explore (plan mode)
Shift+Tab twice to enter plan mode
"Read src/auth and understand session handling"

# Phase 2: Plan (plan mode)
"Create a plan for adding OAuth support"

# Phase 3: Implement (default mode)
"Implement the OAuth flow from your plan"

# Phase 4: Commit
"commit with descriptive message and open PR"
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

### 4.3 Checkpoint-Based Evals 工作流

```
[Task 1]
    │
    ▼
┌─────────┐
│Checkpoint│◄── verify criteria
│   #1    │
└────┬────┘
     │ pass?
   ┌─┴───┐
  yes    no ──► fix ──┐
   │              │    │
   ▼              └────┘
[Task 2]
   ...
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

---

## 5. 并行化

### 5.1 Git Worktrees 并行工作

```bash
# 创建隔离的工作树
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
git worktree add ../project-refactor refactor-branch

# 在每个工作树中启动独立 Claude
cd ../project-feature-a && claude
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 5.2 级联法管理多会话

- 新任务在新标签页中打开（从左到右）
-  sweep 从左到右，最旧到最新
- 每次最多关注 3-4 个任务
- 根据需要检查特定任务

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 5.3 扇出批量任务

```bash
# 生成任务列表
claude -p "List all files needing migration" > files.txt

# 循环处理每个文件
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue" \
    --allowedTools "Edit,Bash(git commit *)"
done
```

**来源**：[Best Practices - Anthropic](https://code.claude.com/docs/en/best-practices)

---

## 6. 编排器模式

### 6.1 顺序阶段编排

```markdown
Phase 1: RESEARCH (Explore agent)
- Gather context
- Identify patterns
- Output: research-summary.md

Phase 2: PLAN (planner agent)
- Read research-summary.md
- Create implementation plan

Phase 3: IMPLEMENT (tdd-guide agent)
- Write tests first
- Implement code

Phase 4: REVIEW (code-reviewer agent)
- Review all changes

Phase 5: VERIFY
- Run tests
- Fix issues
```

**关键规则**：
- 每个 agent 获得一个明确输入，产生一个明确输出
- 输出成为下一阶段的输入
- 永远不要跳过阶段
- agent 之间使用 `/clear`

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 6.2 双实例启动模式

**Instance 1: Scaffolding Agent**
- 搭建项目脚手架
- 创建项目结构
- 设置配置（CLAUDE.md, rules, agents）
- 建立规范

**Instance 2: Deep Research Agent**
- 连接所有服务和网络搜索
- 创建详细 PRD
- 创建架构 Mermaid 图表
- 整理参考资料

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

---

## 7. 持续学习

### 7.1 连续学习技能

```bash
# 安装
git clone https://github.com/affaan-m/everything-claude-code.git ~/.claude/skills/everything-claude-code

# Stop Hook 配置
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

### 7.2 手动提取 /learn

```bash
# 会话中途解决非平凡问题后
/learn
# 提示提取模式，生成技能草稿
```

**来源**：[The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)
