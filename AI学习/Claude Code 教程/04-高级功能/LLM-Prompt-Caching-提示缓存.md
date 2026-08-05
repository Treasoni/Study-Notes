---
title: LLM Prompt Caching 提示缓存
tags: [claude, ai, 进阶应用, 性能优化, 提示工程]
created: 2026-07-31
updated: 2026-07-31
status: draft
source_project: claude-code-tutorial
---

# LLM Prompt Caching 提示缓存

> [!info] 概述
> **Prompt Caching（提示缓存）是 Claude API 和 Claude Code 的核心成本优化机制**——将不变的提示前缀缓存复用，避免重复计费和传输，可降低 **90% 的输入 token 成本** 和 **80% 的延迟**。理解缓存原理是高效使用 Claude Code 的关键。

---

## 一、什么是 Prompt Caching

### 通俗理解

> 提示缓存就像**教室里的黑板**——老师把公式写一次在黑板上，全班同学反复看，不需要每问一道题就重新写一遍。

在 LLM 调用中，每次请求都会带上系统提示、工具定义、历史对话等。这些内容在连续对话中大量重复。如果每次都传完整的上下文：
- Token 浪费巨大（相同内容反复计费）
- 延迟高（传输和编码时间）
- API 成本线性增长

**Prompt Caching 的解决方案**：标记提示中可复用的前缀/后缀，服务端缓存计算结果，后续请求只传变化部分。

### 缓存命中 vs 未命中

```
未命中（首轮）:
┌──────────────────────────────────┐
│ 系统提示 │ CLAUDE.md │ tools │ query │  ← 全部传输 + 全部计费
└──────────────────────────────────┘

缓存命中（后续轮）:
┌──────────────────────────────────┐
│ 系统提示 │ CLAUDE.md │ tools │ ██ │  ← 缓存部分免费/低价
│                              │   │
└──────────────────────────────┴───┘
                               ↑
                          只传新的 query
```

> [!tip] 核心收益
> - **写入成本**：比未缓存高 10%（一次性代价）
> - **读取成本**：比未缓存低 **90%**（每次复用都赚）
> - **适用场景**：多轮对话、系统提示稳定的应用

---

## 二、缓存什么内容

### 缓存机制

Claude API 会对以下内容自动缓存：

| 缓存对象 | 最小长度 | 缓存 TTL | 说明 |
|---------|---------|---------|------|
| System Prompt | 1024 tokens | 5 分钟 | 系统提示词 |
| Tools 定义 | 1024 tokens | 5 分钟 | 工具描述和 schema |
| Messages 前缀 | 1024 tokens | 5 分钟 | 连续的对话前缀 |
| 图片 | 100 tokens | 5 分钟 | 图片内容 |

> [!warning] 关键约束
> - **最小缓存块 1024 tokens** — 小于 1024 的不缓存
> - **5 分钟 TTL** — 两次请求间隔超过 5 分钟，缓存自动失效
> - **必须精确匹配** — 哪怕改一个空格，缓存也作废，需要重新写入

### 缓存断点

提示中可以被缓存的"断点"位置：

```
[ SYSTEM PROMPT ]       ← 缓存点 1（多轮不变的固定前缀）
[ TOOLS ]               ← 缓存点 2（工具定义）
[ Messages:             
    [user]: "问题1"     
    [assistant]: "回答1" ← 缓存点 3（历史消息前缀）
    [user]: "问题2"     
    [assistant]: "回答2" 
    [user]: "问题3"     ]  ← 仅这部分是新内容，需要传输
```

---

## 三、Claude Code 中的缓存架构

### 三层缓存结构

```
请求结构（从稳定到动态）:
┌─────────────────────────────────┐
│ ① System Prompt                  │ ← 可用期内 100% 缓存
│   (角色、任务、安全规则)           │
├─────────────────────────────────┤
│ ② CLAUDE.md + Project Memory     │ ← 项目不变时缓存
│   (项目规则、编码规范)             │
├─────────────────────────────────┤
│ ③ Tools 定义                     │ ← 工具集不变时缓存
│   (Read/Write/Bash 等描述)       │
├─────────────────────────────────┤
│ ④ 历史消息前缀                    │ ← 5 分钟 TTL 刷新
│   (前 N-1 轮对话)                │
├─────────────────────────────────┤
│ ⑤ 当前用户输入                    │ ← 不缓存，每次变化
└─────────────────────────────────┘
```

### 项目中的缓存优化实践

你的项目 `.claude/rules/common/prompt-cache.md` 已经定义了完整的缓存策略：

> **核心原则**：稳定内容在前，动态内容在后。

```markdown
# Prompt Cache Rules - 提示顺序

1. 稳定的角色、任务边界、安全规则
2. 稳定的工具约束、输出格式、质量要求
3. 稳定的示例（仅在显著改善结果时）
4. 动态参数：用户请求、文件摘录、日期、运行时状态
```

### JSON Schema 断点

Claude Code 中有一个重要的缓存优化机制——**JSON Schema 缓存断点**：

```json
{
  "type": "object",
  "properties": {
    "response": { "type": "string" }
  }
}
```

如果最终输出始终包含相同的 JSON Schema 定义，应放在系统提示的稳定区域，使其可被缓存。这对 `/review-pr`、`/commit` 等固定输出格式的命令尤其有效。

---

## 四、影响缓存命中的因素

### ✅ 这些操作会保持缓存

| 操作 | 对缓存的影响 |
|------|------------|
| 同一会话连续对话 | 历史前缀持续命中 |
| 修改用户查询内容 | 无影响（查询在动态部分） |
| 使用相同的 CLAUDE.md | 稳定前缀不变 |
| 短时间内继续对话 | 在 5 分钟 TTL 内 |

### ❌ 这些操作会破坏缓存

| 操作 | 原因 |
|------|------|
| `/clear` | 清空所有上下文，重置缓存 |
| `/compact` | 对话被压缩摘要替代，缓存点重置 |
| 修改 CLAUDE.md | 缓存前缀变更 |
| 修改 settings.json（工具相关） | 工具定义变化 |
| 间隔超过 5 分钟再发消息 | 缓存 TTL 过期 |
| 切换模型 | 不同模型独立缓存 |
| `/rewind` | 对话状态变更 |

### 缓存命中率诊断表

| 现象 | 原因 | 解决 |
|------|------|------|
| `/context` 显示 token 消费高 | 缓存命中率低 | 检查前缀稳定性 |
| 连续发送消息间隔长 | 5 分钟 TTL 过期 | 缩短思考/操作时间 |
| 工具定义频繁变化 | 每次调用不同工具集 | 合并工具调用 |
| CLAUDE.md 过长 | 超过缓存有效区 | 精简到 200 行以内 |

---

## 五、缓存优化实践

### 1. 稳定前缀设计

```markdown
# ❌ 差 — 动态内容在前面
{{current_date}} {{user_name}}
You are a coding assistant.
Project rules: ...

# ✅ 好 — 稳定内容在前面
You are a coding assistant.         ← 缓存
Project rules: ...                  ← 缓存
{{current_date}} {{user_name}}     ← 动态
```

### 2. CLAUDE.md 优化

```markdown
# ❌ 差 — 太长，降低有效缓存密度
- 包含大量示例代码
- 500+ 行规则文件
- 动态时间戳

# ✅ 好 — 精简稳定
- 只写核心规则（≤ 200 行）
- 示例代码用 @ 引用外部文件
- 不含动态内容
```

### 3. Skill 设计原则

Skills 的 `SKILL.md` 本质上是注入到上下文的提示前缀：

```markdown
# 稳定前缀（可缓存）
role: code-reviewer
rules: [check security, check performance]
output: JSON schema

# 动态参数（不可缓存，放最后）
target_file: {{user_input}}
focus_area: {{user_selection}}
```

### 4. Subagent 调用优化

每个 Subagent 有独立上下文，缓存也是独立的：

```markdown
# ❌ 差 — 每个 Subagent 自定义系统提示
agent A: "Review this code for bugs..."
agent B: "Review this code for style..."

# ✅ 好 — 共享稳定模板
agent A: uses template "reviewer" + query "bugs"
agent B: uses template "reviewer" + query "style"
```

### 5. 监控缓存效果

```bash
# 查看当前token消耗
/context

# 查看费用明细
/cost

# 调试模式查看缓存命中
claude --debug
```

---

## 六、与其它优化手段对比

| 机制 | 解决的问题 | 作用层 | 配置难度 |
|------|----------|--------|---------|
| **Prompt Caching** | 重复前缀的 token 成本 | API 层（自动） | ⭐ 无需配置 |
| **`/compact`** | 对话过长导致 token 浪费 | 会话层（手动） | ⭐ 一条命令 |
| **`.claudeignore`** | 遍历无关文件 | 文件层（手动） | ⭐⭐ 写规则 |
| **`claudeMdExcludes`** | 加载过多 CLAUDE.md | 配置层（手动） | ⭐⭐ 写配置 |
| **Skill 渐进披露** | 一次性加载太多指令 | 架构层（设计） | ⭐⭐⭐ 需规划 |

> [!tip] 关系
> Prompt Caching 是**透明的底层优化**，不需要你做任何事就能生效。但你写的 CLAUDE.md、Skills、Subagent 设计**决定了缓存能有多高的命中率**。

---

## 七、常见误区

### ❌ "缓存命中了就不用付钱"

缓存命中仍然需要付费——只是费用大幅降低（约 10% 的原价）。完全免费的是"剪枝"（某些前缀被完全剪裁）。

### ❌ "内容一样就一定能缓存"

必须**逐字节精确匹配**。格式化的差异（如 Markdown vs 纯文本）、换行符差异都会导致缓存失效。

### ❌ "缓存越大越好"

缓存块有最小 1024 token 的要求。对于短消息链，缓存反而没有意义。同时，如果前缀变化频繁，缓存写入成本反而更高。

### ❌ "5 分钟 TTL 很短，不实用"

在活跃的编程会话中，每轮对话通常只需 10-60 秒。只要连续工作不断，5 分钟足够覆盖整场编码会话。

---

## 相关文档

- [[settings.json 配置详解]] - 缓存相关配置项
- [[CLAUDE.md 使用指南]] - 稳定前缀的最佳载体
- [[Claude Code Memory 完整指南]] - Memory 与缓存的配合
- [[如何编写Skills]] - Skill 设计中的缓存考虑
- [[Claude Code 会话管理]] - /compact 与缓存的关系

---

## 参考资料

- [Anthropic Prompt Caching 官方文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Claude Code 项目 prompt-cache.md 规则](.claude/rules/common/prompt-cache.md)
- [Prompt Caching 技术博客](https://www.anthropic.com/news/prompt-caching)
