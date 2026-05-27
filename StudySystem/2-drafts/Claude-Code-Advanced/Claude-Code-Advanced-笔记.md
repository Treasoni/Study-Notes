---
type: concept
topic: Claude Code 高级使用技巧
difficulty: 入门
tags:
  - Claude Code
  - AI编程
  - 工作流优化
  - Token优化
  - 记忆持久化
created: 2026-05-27
updated: 2026-05-27
sources:
  - https://code.claude.com/docs/en/overview
  - https://code.claude.com/docs/en/how-claude-code-works
  - https://code.claude.com/docs/en/best-practices
  - https://x.com/affaan/status/2014040193557471352
  - https://x.com/affaan/status/2014040193557471352 (长篇指南)
  - https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to
concepts:
  - Agentic Loop
  - Context Window
  - Token Economics
  - Memory Persistence
  - Subagent Architecture
  - Verification Patterns
---

# Claude Code 高级使用技巧

## 一句话解释

Claude Code 是一个终端中的 Agentic 编程助手，通过 Agentic Loop（收集上下文 → 执行行动 → 验证结果）帮助你完成编码任务。核心约束是**上下文窗口填充越快，性能下降越明显**。

## 为什么存在？（解决什么问题）

没有 Claude Code 之前，开发者需要手动完成大量重复性编码任务（写测试、修复 bug、代码重构等），既耗时又容易出错。Claude Code 通过 Agentic Loop 自动化这些流程，让你描述想要什么，它就能自主完成。

核心痛点：**Token 消耗快**。一次复杂的调试会话可能消耗大量 Token，导致性能下降或成本飙升。

## 核心原理

### Agentic Loop

```
┌─────────────────────────────────────────────────────────┐
│                      Agentic Loop                        │
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────────┐    │
│   │  Gather  │───▶│   Take   │───▶│   Verify    │    │
│   │ Context  │    │  Action  │    │   Results   │    │
│   └──────────┘    └──────────┘    └──────┬───────┘    │
│                                          │             │
│                  ◀───────────────────────┘             │
│                   (loop until complete)                 │
└─────────────────────────────────────────────────────────┘
```

**类比**：就像一个高级工程师，你先告诉他目标（gather context），他制定计划并执行（take action），完成后自我检查（verify results）。不对就重来。

### 动态系统提示注入

使用 CLI 标志动态注入上下文，高于用户消息和工具结果的指令层级。

```bash
# 场景化上下文
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

**与 @ 文件引用的区别**：`[@memory.md](https://x.com/@memory.md)` 或 `.claude/rules/` 通过 Read 工具读取（工具输出），而 `--system-prompt` 注入到实际系统提示（更高指令层级）。

**适用场景**：严格行为规则、项目级约束、需要 Claude 优先处理的上下文。

### 上下文窗口管理

Claude 的上下文窗口 = 对话历史 + 文件内容 + 命令输出 + CLAUDE.md + skills + 系统指令

**类比**：就像工作台空间。工作台越小，能放的东西越少，放多了就开始混乱。Claude Code 的优化核心就是"保持工作台整洁"。

## 关键要点

### 1. Token 优化是关键

- **系统提示精简**：18k tokens → 10k tokens（节省 41%）
- **mgrep 替代 grep**：节省约 50% tokens
- **后台进程外执行**：用 tmux 运行长时间任务，减少输入 tokens
- **模型选择**：Haiku（简单）→ Sonnet（日常）→ Opus（复杂）

### 2. 记忆持久化三层体系

| 层级 | 工具 | 何时加载 |
|------|------|----------|
| 每次会话 | CLAUDE.md | 会话开始 |
| 按需 | Skills | 使用时加载 |
| 自动 | Auto Memory | 自动保存学习 |

### 3. 会话管理命令

- `/clear` - 重置上下文（任务切换时）
- `/compact` - 手动压缩上下文
- `/rewind` - 回溯到之前状态
- `/btw` - 快速提问，不进入历史

### 4. Strategic Compact（手动压缩策略）

Auto-compact 在任意时刻触发（经常在任务中途），而 Strategic Compact 在逻辑边界点手动执行，保留关键上下文。

**核心思路**：在探索阶段完成后、执行阶段开始前 compact；在完成里程碑后、开始下一个前 compact。

```bash
#!/bin/bash
# Strategic Compact Suggester
# 在 PreToolUse 时触发，建议在逻辑边界点手动 compact

COUNTER_FILE="/tmp/claude-tool-count-$$"
THRESHOLD=${COMPACT_THRESHOLD:-50}

if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
  count=$((count + 1))
  echo "$count" > "$COUNTER_FILE"
else
  echo "1" > "$COUNTER_FILE"
  count=1
fi

if [ "$count" -eq "$THRESHOLD" ]; then
  echo "[StrategicCompact] $THRESHOLD tool calls reached - consider /compact if transitioning phases" >&2
fi
```

**适用场景**：积累了大量探索上下文但不再适用于执行阶段时。

### 5. 给 Claude 验证标准

**单条最高杠杆的操作**：提供测试用例、截图、预期输出，让 Claude 自我验证。

```
❌ "实现邮箱验证"
✅ "实现 validateEmail。测试用例：user@example.com → true, invalid → false, user@.com → false。实现后运行测试。"
```

### 5. Subagent 是并行化的关键

- Subagent 有独立上下文，不污染主会话
- Tier 1（易用）：Subagents、Metaprompting
- Tier 2（难用）：Long-running agents、Parallel multi-agent

### 6. Git Worktrees 避免冲突

```bash
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
cd ../project-feature-a && claude
```

## 常见误区

### 误区 1：上下文越多越好
**正解**：上下文越多，性能越差。在不同任务之间用 `/clear` 重置上下文。

### 误区 2：所有任务都用 Opus
**正解**：Haiku vs Opus 价格差 5 倍，Sonnet vs Opus 仅 1.67 倍。日常任务用 Sonnet 即可。

### 误区 3：一次性说所有需求
**正解**：迭代式沟通。Claude 第一次尝试不对，立即纠正，比一次性说清楚效果更好。

### 误区 4：CLAUDE.md 越详细越好
**正解**：只放 Claude 猜不到的内容（自定义命令、特殊规范）。越长越容易被忽略。

### 误区 5：并行终端越多越好
**正解**：每次专注于 3-4 个任务。超过这个数量，认知负担超过收益。

## 与其他概念的关系

- Claude Code 是 Agentic AI 的具体实现
- Context Window 管理是所有优化的基础
- Skills 是记忆持久化的实战形式
- Subagents 是并行化的技术手段

## 代码示例

### CLAUDE.md 示例

```markdown
# Code style
- Use ES modules (import/export), not CommonJS
- Destructure imports when possible

# Workflow
- Typecheck after making series of changes
- Run single tests, not whole suite for performance

# Testing
- Use Vitest for this project
- Run `npm test -- --watch` during development
```

### Skill 定义示例

```markdown
# .claude/skills/fix-issue/SKILL.md
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get details
2. Search codebase for relevant files
3. Implement fix
4. Write and run tests
5. Create PR
```

### 动态系统提示注入

```bash
# 场景化上下文
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'

# 使用
claude-dev
```

### 记忆持久化 Hooks

```json
{
  "hooks": {
    "PreCompact": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/pre-compact.sh"
      }]
    }],
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/session-start.sh"
      }]
    }],
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/hooks/session-end.sh"
      }]
    }]
  }
}
```

## 一句话总结

**保持上下文整洁，任务要验证，模型按需选，会话常清理。**

## 思考题

1. **上下文窗口耗尽前，你会收到什么信号？如何在日常使用中预防？**

2. **什么场景适合用 Subagent 而不是直接在主会话中处理？Subagent 的上下文隔离有什么优缺点？**

3. **Haiku 和 Opus 的价格差是 5 倍，但实际使用中你如何判断任务是否值得用 Opus？有什么具体的判断标准？**

4. **Continuous Learning（Stop Hook 自动提取知识）和手动写 Skills，哪种方式更适合你目前的工作流？为什么？**

5. **探索-计划-实现模式（Explore-Plan-Implement）什么时候值得用，什么时候是过度工程？**

---

## 进阶实战技巧（来源：The Longform Guide）

### Continuous Learning / Memory

通过 Stop Hook 自动从错误中学习，避免重复踩坑。

**核心问题：** 重复发送相同提示、Claude 遇到同样问题、浪费 tokens 和时间

**解决方案：** 发现非平凡的调试技术、workaround、项目特定模式 → 保存为 Skill，下次自动加载

```bash
# 安装
git clone https://github.com/affaan-m/everything-claude-code.git ~/.claude/skills/everything-claude-code
```

**为什么用 Stop Hook 而不是 UserPromptSubmit？**
- UserPromptSubmit 每次消息都触发 → 延迟 +  overhead
- Stop 只在会话结束时触发 → 轻量 + 评估完整会话

```json
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

**Session Log 模式：** `~/.claude/sessions/YYYY-MM-DD-topic.tmp` — 每次会话一个文件

---

### Verification Loops and Evals

#### Checkpoint-Based vs Continuous

```
CHECKPOINT-BASED                    CONTINUOUS
─────────────────                   ──────────
  [Task 1]                             [Work]
     │                                    │
     ▼                                    ▼
  ┌─────────┐                        ┌─────────┐
  │Checkpoint│◄── verify             │ Timer/  │
  │   #1    │    criteria             │ Change  │
  └────┬────┘                        └────┬────┘
       │ pass?                              │
   ┌───┴───┐                              ▼
   │       │                          ┌──────────┐
  yes     no ──► fix ──┐              │Run Tests │
   │              │    │              │  + Lint  │
   ▼              └────┘              └────┬─────┘
  [Task 2]                               │
     ▼                               ┌────┴────┐
  ...                                 pass     fail
                                      │         │
                                    ▼         ▼
                               [Continue] [Stop & Fix]

适用：线性流程                   适用：长会话探索
```

**pass@k vs pass^k：**
- `pass@k`：k 次中至少一次成功（高成功率）
- `pass^k`：k 次全部成功（高一致性要求）

#### Grader Types

| 类型 | 优点 | 缺点 |
|------|------|------|
| Code-Based | 快速、便宜、客观 |  brittle |
| Model-Based | 灵活、处理 nuance | 非确定性、贵 |
| Human | 金标准质量 | 慢、贵 |

---

### Parallelization

**正交原则：** 分支作用域要明确，最小化代码重叠，选择正交任务防止干扰

**推荐模式：**
- 主聊天：代码改动
- 分支：代码库问题研究、外部服务文档、GitHub 搜索

**Cascade Method（级联法）：**
- 新任务开新 tab 在右侧
- 从左到右扫，最旧到最新
- 最多同时关注 3-4 个任务

**Git Worktrees 避免冲突：**

```bash
git worktree add ../project-feature-a feature-a
git worktree add ../project-feature-b feature-b
cd ../project-feature-a && claude
```

**何时扩展实例：**
- 多实例重叠代码 → 必须用 git worktrees
- 用 `/rename` 命名所有聊天避免混淆

---

### Groundwork

**双实例启动模式：**

| 实例 | 职责 |
|------|------|
| **实例 1：脚手架 Agent** | 搭建项目结构、配置 CLAUDE.md/rules/agents、确立规范 |
| **实例 2：深度研究 Agent** | 连接服务/搜索、创建 PRD、架构 Mermaid 图、编译参考文档 |

**llms.txt Pattern：**
- 很多文档站有 `llms.txt` 优化版本
- Claude 文档页面输入 `/llms.txt` 获取

**Philosophy：构建可复用模式**

投资优先级：
1. Subagents
2. Skills
3. Commands
4. Planning patterns
5. MCP tools
6. Context engineering patterns

> "这些 workflow 可以转移到其他 agent 如 Codex。" — [@omarsar0](https://x.com/@omarsar0)

---

### Best Practices for Agents & Sub-Agents

**Sub-Agent 上下文问题：**

Orchestrator 有语义上下文，Sub-agent 只有字面 query。Summaries 经常遗漏关键细节。

**Iterative Retrieval Pattern：**

```
┌─────────────────┐
│  ORCHESTRATOR   │
│  (has context)  │
└────────┬────────┘
         │ dispatch with query + objective
         ▼
┌─────────────────┐
│   SUB-AGENT     │
│ (lacks context) │
└────────┬────────┘
         │ returns summary
         ▼
┌─────────────────┐      ┌─────────────┐
│   EVALUATE      │─no──►│  FOLLOW-UP  │
│   Sufficient?   │      │  QUESTIONS  │
└────────┬────────┘      └──────┬──────┘
         │ yes                   │
         ▼                       │ sub-agent
    [ACCEPT]              fetches answers
                                │
         ◄──────────────────────┘
              (max 3 cycles)
```

**关键规则：**
1. 每个 agent 一个明确输入 → 一个明确输出
2. 输出成为下一阶段输入
3. 不跳阶段
4. agent 间用 `/clear` 保持上下文新鲜
5. 中间输出存文件

**Agent Abstraction Tierlist：**

| Tier | 模式 | 难度 |
|------|------|------|
| **Tier 1** | Subagents、Metaprompting | 易 |
| **Tier 2** | Long-running agents、Parallel multi-agent、Computer use | 难 |

---

### Tips and Tricks

**MCP 替代方案：**

MCP（如 GitHub、Supabase、Vercel）本质是 CLI 的包装，有 context 成本。

**替代方案：CLI + Skills**
- 不长期加载 MCP
- 用 Skills 包装 CLI 功能（如 `/gh-pr` 包装 `gh pr create`）
- 功能相同，context 自由

> 随着 Claude Code lazy loading MCP，context 问题已大部分解决。但 CLI + Skills 仍是 token 优化方法。
