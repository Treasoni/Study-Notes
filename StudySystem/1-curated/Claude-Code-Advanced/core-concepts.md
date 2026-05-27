# 核心概念 - Claude Code 高级使用技巧

## 1. Agentic Loop（Agentic 循环）

**定义**：Claude 处理任务的三个阶段循环：gather context → take action → verify results

**来源**：
- [How Claude Code Works - Anthropic](https://code.claude.com/docs/en/how-claude-code-works)

**关键点**：
- 由模型（reasoning）和工具（action）驱动
- 工具使用返回信息反馈给下一步决策
- 复杂任务会循环多个周期并自我修正

---

## 2. Context Window（上下文窗口）

**定义**：Claude 能理解和操作的 token 总量，包括对话历史、文件内容、命令输出等

**来源**：
- [Best Practices for Claude Code - Anthropic](https://code.claude.com/docs/en/best-practices)
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**关键点**：
- 上下文窗口填充越满，性能下降越明显
- Claude 自动压缩，但关键代码片段和请求会保留
- 持久化规则应放在 CLAUDE.md 而非对话历史

---

## 3. CLAUDE.md

**定义**：项目根目录下的特殊文件，Claude 每次会话开始时读取

**来源**：
- [Best Practices for Claude Code - Anthropic](https://code.claude.com/docs/en/best-practices)

**关键点**：
| 应包含 | 不应包含 |
|--------|----------|
| Claude 无法猜测的 Bash 命令 | Claude 可从代码推断的内容 |
| 与默认风格不同的代码规范 | 标准语言惯例 |
| 测试指令和测试运行器偏好 | 详细 API 文档（链接即可）|
| 仓库规范（分支命名、PR 约定）| 频繁变化的信息 |
| 项目特定架构决策 | 文件逐个描述代码库 |
| 常见陷阱或非显而易见的行为 | 不言自明的实践 |

---

## 4. Skills（技能）

**定义**：打包为 `.claude/skills/{skill-name}/SKILL.md` 的可复用工作流

**来源**：
- [Best Practices for Claude Code - Anthropic](https://code.claude.com/docs/en/best-practices)
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**关键点**：
- 按需加载，只有使用时才加载完整内容
- 可设置 `disable-model-invocation: true` 防止自动触发
- 描述在会话开始时可见，但不占用上下文

---

## 5. Subagents（子代理）

**定义**：在独立上下文中运行的专门助手

**来源**：
- [Best Practices for Claude Code - Anthropic](https://code.claude.com/docs/en/best-practices)
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**关键点**：
- 完全独立的新上下文，不污染主会话
- 返回摘要而非全部内容
- 可指定模型（haiku/sonnet/opus）
- 定义在 `.claude/agents/` 目录

---

## 6. Memory Persistence Hooks（记忆持久化钩子）

**定义**：三个会话生命周期钩子协同实现跨会话记忆

**来源**：
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**三个关键钩子**：
1. **PreCompact Hook**：压缩前保存重要状态
2. **SessionComplete Hook**：会话结束时持久化学习
3. **SessionStart Hook**：新会话时加载历史上下文

---

## 7. Token Economics（Token 经济）

**定义**：理解和优化 Claude 使用成本的核心概念

**来源**：
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)
- [32 Claude Code Tips - YK](https://agenticcoding.substack.com/p/32-claude-code-tips-from-basics-to)

**关键点**：
- 系统提示默认 ~18k tokens，可精简至 ~10k
- mgrep 替代 grep 可节省约 50% tokens
- 背景进程外执行减少输入 tokens
- 模型价格差：Haiku vs Opus = 5x，Sonnet vs Opus = 1.67x

---

## 8. Verification Patterns（验证模式）

**定义**：让 Claude 能够验证自己工作的模式

**来源**：
- [Best Practices for Claude Code - Anthropic](https://code.claude.com/docs/en/best-practices)
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**两种评估类型**：
| 类型 | 适用场景 |
|------|----------|
| Checkpoint-Based | 线性流程，有明确里程碑 |
| Continuous | 长时间会话，探索性重构 |

---

## 9. Agent Abstraction Tierlist（Agent 抽象层级）

**定义**：Agent 模式按易用性分层

**来源**：
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

| 层级 | 模式 | 难度 |
|------|------|------|
| Tier 1 | Subagents、Metaprompting | 易用 |
| Tier 2 | Long-running agents、Parallel multi-agent、Role-based multi-agent | 难用 |

---

## 10. Continuous Learning（持续学习）

**定义**：让 Claude 从会话中自动提取和保存可复用知识

**来源**：
- [The Longform Guide - @affaan](https://x.com/affaan/status/2014040193557471352)

**工作流程**：
1. Stop Hook 在会话结束时触发
2. 评估会话，提取有价值模式（错误解决、调试技术、项目特定模式）
3. 保存到 `~/.claude/skills/learned/`
4. 下次类似问题时自动加载
