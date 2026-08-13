# 第八章：Skills、自定义 Agent 与 AGENTS.md

对熟悉 Claude Code 的你来说，`CLAUDE.md` 和 `.claude/skills/` 是日常定制的两大支柱。这一章把这两根支柱搬到 opencode：`AGENTS.md` 如何原生加载、SKILL.md 的六个发现位置怎样兼容你的存量技能、`skill()` 怎么调用、自定义 Agent 与 hooks 有哪些限制。把这些差异吃透，你就能把 Claude Code 的整套定制"平移"到 opencode，而不是从零重写。

## AGENTS.md 原生加载（与 CLAUDE.md 对应）

opencode 原生读取 `AGENTS.md` 作为项目上下文文件，语义上等价于 Claude Code 的 `CLAUDE.md`。在 TUI 里执行 `/init` 会创建或更新项目的 `AGENTS.md`——对照表里它正是 Claude Code `/init` 生成 `CLAUDE.md` 的对应物。

| 操作 | opencode | Claude Code |
|------|----------|-------------|
| 项目上下文文件 | `AGENTS.md` | `CLAUDE.md` |
| 生成命令 | `/init` | `/init` |

一个值得注意的差异：`AGENTS.md` 是跨工具的标准文件名（Cursor、Codex、opencode 都在读），所以同一份项目规范天然能在多个工具间复用；而 `CLAUDE.md` 是 Anthropic 专属约定，出了 Claude Code 就没用了。[官方 Skills 文档](https://opencode.ai/docs/skills)

> [!tip] 大白话
> 把 `AGENTS.md` 想成「给 AI 同事的项目说明书」——和 `CLAUDE.md` 是同一件东西，只是牌子换成了行业通用款。所以你在 Claude Code 里写在 `CLAUDE.md` 的"项目怎么跑、有哪些约定"，原样搬进 `AGENTS.md` 就能在 opencode 生效，还能顺带给别的工具看。

## SKILL.md 发现顺序与 frontmatter

SKILL.md 的存放模式是 `<base>/skills/<name>/SKILL.md`，opencode 按六个位置发现技能：

1. 项目 `.opencode/skills/`
2. 全局 `~/.config/opencode/skills/`
3. 项目 `.claude/skills/`
4. 全局 `~/.claude/skills/`
5. 项目 `.agents/skills/`
6. 全局 `~/.agents/skills/`

> [!tip] 大白话
> 把六个位置想成「厨房里六个调料抽屉」——只要技能放进任何一个抽屉，opencode 都能翻到。重点看第三、四个抽屉：`.claude/skills` 被 opencode 直接兼容读取，你在 Claude Code 里攒下的技能一个都不用搬，它自己就能找到。

frontmatter 字段比 Claude Code 更精简，只认五个：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 小写 + 连字符（如 `git-release`） |
| `description` | 是 | 1-1024 字符，模型据此决定何时调用 |
| `license` | 否 | 技能许可 |
| `compatibility` | 否 | 兼容的工具/版本 |
| `metadata` | 否 | 自由扩展信息 |

素材中缺一个完整的最小 SKILL.md 示例，这里补一个最小可用的：

```markdown
---
name: git-release
description: Create a semantic version release, tag it, push tags, and print a changelog.
license: MIT
compatibility:
  - opencode
  - claude-code
metadata:
  author: you
---

## What it does

Cuts a new release: bumps the version, commits, tags, pushes, and prints a short changelog.

## Steps

1. Read `package.json` to confirm the current version.
2. Ask the user for the next version.
3. Run `npm version <next>` and `git push --tags`.
4. Print the commit list since the last tag as the changelog.
```

要点：`name` 必须小写 + 连字符（模型用它在 `skill()` 里精确点名），`description` 是模型判断"什么时候该用这个技能"的唯一依据，值得写清楚触发场景。

## skill 调用语法与权限

模型在对话中通过 `skill()` 函数调用技能：

```
skill({ name: "git-release" })
```

技能是否允许被执行，由权限键 `permission.skill` 控制，三值 `allow` / `ask` / `deny` 加通配符，沿用第五章的"last matching rule wins"规则：

```json
{
  "permission": {
    "skill": { "*": "ask", "git-release": "allow" }
  }
}
```

上面配置的含义：默认所有技能先弹窗询问，只有 `git-release` 直接放行。

> [!tip] 大白话
> `skill()` 想成「给熟练工友打内线电话」——模型拨号（写 `skill({ name: ... })`），总机（`permission.skill`）决定这通电话是直接接通还是先请示你。所以技能写好了不算完，权限放行才真正可用。

## 自定义 Agent 与 hooks 限制

自定义 Agent 有两种定义方式：Markdown 文件或 `agent create` 命令。

**Markdown 文件**：放在 `.opencode/agents/`（项目）或 `~/.config/opencode/agents/`（全局），用 frontmatter 声明属性，正文是系统提示词：

```markdown
---
model: anthropic/claude-sonnet-4-5
description: 只读代码审查助手，不改代码
---

你是资深工程师，只做分析、给出修改建议，不执行任何编辑。
```

**CLI 引导**：`opencode agent create` 交互式创建，可用 `--permissions` / `--tools` 指定该 agent 的权限与工具；`opencode agent list` 查看已有 agent。这比 Claude Code 手写 `.claude/agents/*.md` 多了一条可视化入口。[官方 Agents 文档](https://opencode.ai/docs/agents)

此外也能在 `opencode.json` 里用 `agent` 键声明式定义（字段为 `description`、`model`、`prompt`、`tools`），与第三、五章的配置体系一脉相承。

**hooks 限制**：opencode 只支持 4 个共享 hook，Claude Code 的整套 hooks 体系不会照搬：

| hook | 大致用途 | 对应 Claude Code 思路 |
|------|----------|----------------------|
| `guard-shell` | shell 命令执行前守卫 | PreToolUse 守卫 |
| `guard-read-large` | 大文件读取守卫 | 超大读取保护 |
| `inject-types-on-read` | 读取时注入类型上下文 | 上下文注入 |
| `check-on-edit` | 编辑后检查 | PostToolUse |

迁移提醒：如果现有 Claude Code 配置挂了很多自定义 hook，只有这 4 个在 opencode 有对应物，其余要么换用权限规则（第五章），要么用插件机制替代。

> [!tip] 大白话
> hooks 想成「机场安检口」——opencode 目前只开了四个口（上表），你在 Claude Code 里装的那一排"特殊通道"（自定义 hook）大多过不来。迁移前先盘点：哪些守卫能落到这四个口子上，哪些要改写成权限规则。

## 跨工具复用（Claude Code / OpenCode / Cursor / Codex）

把整套 skills/agents/guardrails 做成"一套资产、多工具适配"是更省力的终局，典型思路是 spine 这类适配器项目：以工具无关的 `.agents/skills/` 和 `AGENTS.md` 为核心，通过薄适配层接到各工具的加载机制。[spine 项目](https://github.com/kenoxa/spine)

结合本章的六个发现位置，推荐一条渐进迁移路径：

1. **零改动过渡**：先保留技能在 `.claude/skills/`（位置 3/4），opencode 直接读取，Claude Code 也照常工作——双工具并行期无感知。
2. **工具无关化**：把希望跨工具复用的技能挪到 `.agents/skills/`（位置 5/6），项目规范交给 `AGENTS.md`，让 Cursor / Codex 也能消费。
3. **薄适配层**：工具间差异（`skill()` 语法、permission 键名、hook 名）用适配器抹平，核心资产只维护一份。

这样，你花在 Claude Code 上的定制沉淀不会锁死在单一工具里，换工具只是换适配层，而不是重写资产。

## 本章小结

- `AGENTS.md` 是 opencode 原生加载的项目上下文文件，`/init` 生成，对应 Claude Code 的 `CLAUDE.md`，且是跨工具标准文件名。
- SKILL.md 有六个发现位置，其中 `.claude/skills/` 被 opencode 兼容读取，存量技能零迁移即用。
- frontmatter 只认五个字段：`name`（必填，小写+连字符）、`description`（必填）、`license`、`compatibility`、`metadata`。
- 技能用 `skill({ name: "..." })` 调用，`permission.skill` 控制 allow/ask/deny；自定义 Agent 用 Markdown 文件或 `agent create`。
- hooks 仅支持 4 个共享 hook，Claude 专属 hooks 不生效；用 `.agents/skills/` + 适配器可实现跨工具复用。

下一章进入收尾：把迁移过程中最容易踩的认证失败、模型不出现、配置误配整理成排错清单，作为你在 opencode 里"随用随查"的手册。
