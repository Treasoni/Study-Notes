---
title: Claude Code 项目动态技能发现机制
type: practice
difficulty: intermediate
tags:
  - claude-code
  - architecture
  - agent-system
  - skills
created: 2026-05-12
sources:
  - 个人经验
concepts:
  - 动态发现机制
  - 规则寻址
  - 热插拔
---

# Claude Code 项目动态技能发现机制

> [!tip] 核心问题
> 当 Skills 和 Subagents 数量增多时，将它们全部写在 CLAUDE.md 中会导致：初始加载冗长、模型注意力分散、核心逻辑"失焦"。

## 问题背景

在一个持续演进的项目中，技能和代理数量会不断增长：

| 场景 | 问题 |
|------|------|
| 20+ Skills | CLAUDE.md 变得臃肿 |
| 5+ Subagents | 每次对话都加载冗余信息 |
| 持续迭代 | 维护成本不断增加 |

## 解法一：规则寻址法（Globbing）—— 推荐方案

> [!info] 为什么适合 Claude Code
> Claude Code 原生具备 `Glob`、`ls`、`Read` 等工具能力，可以动态发现资源而非硬编码路径。

### 核心思路

将"静态的硬编码列表"升级为"动态的发现机制（Dynamic Discovery）"。

### 实现方式

在根目录的 `CLAUDE.md` 中只需简短的一段话：

```markdown
## 动态技能调用机制 (Dynamic Skill Routing)

本系统的所有扩展功能均已模块化，存放在 `./.claude/skills/` 目录下。

**执行规则：**
当你收到以 `/` 开头的指令时：
1. 使用 `Glob` 或 `ls` 工具列出 `./.claude/skills/` 目录下的可用子文件夹
2. 找到名称匹配的技能文件夹后，读取该目录下的 `SKILL.md`
3. 严格按照 `SKILL.md` 中的指示执行
```

### 优势

> [!success] 为什么优雅？
> - **热插拔**：新增技能无需修改 CLAUDE.md
> - **自描述**：每个技能独立，有自己的说明书
> - **零维护**：根目录指令永远简洁

## 解法二：入口注册表（Index）—— 适合大规模系统

当技能数量多到连 `ls` 列出来都觉得长时，可以采用二级目录策略。

### 实现方式

1. 在 `.claude/skills/` 根部创建 `INDEX.md` 注册表
2. `CLAUDE.md` 只保留一句话指向注册表

```markdown
本系统包含多个自定义技能与子代理。执行任何扩展任务前，请先读取 ./.claude/skills/INDEX.md 获取全局技能注册表与调用路径。
```

### 运作逻辑

```
启动 → 读取 INDEX.md → 获取路由 → 读取具体 SKILL.md → 执行
```

> [!abstract] 类比
> 这相当于在操作系统中注册了环境变量，隔离了主配置文件的复杂度。

## 最佳实践建议

> [!warning] 针对 Study System
> 强烈建议直接采用 **解法一（规则寻址法）**。

原因：
1. 利用大模型自主使用工具的特性
2. 免去每次新建技能还要去别的文件注册登记的繁琐步骤
3. 实现真正的"热插拔"

## 总结

| 方案 | 适用规模 | 复杂度 | 维护成本 |
|------|----------|--------|----------|
| 解法一（Globbing） | 小中型（<20 Skills） | 低 | 几乎为零 |
| 解法二（Index） | 大型（>20 Skills） | 中 | 需维护注册表 |

> [!quote]
> 无论你以后增加多少个技能，根目录的 CLAUDE.md 永远只有这几行字。Claude Code 会像一个聪明的操作员一样，收到指令后先去"仓库"看一眼目录，然后精准拿出对应的说明书。
