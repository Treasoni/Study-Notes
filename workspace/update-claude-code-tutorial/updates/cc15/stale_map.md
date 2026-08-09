# cc15 过时点映射（Stale Map）

- **note_id**: cc15
- **笔记**: `AI学习/Claude Code 教程/04-高级功能/如何编写Skills.md`
- **更新日期**: 2026-08-10
- **更新目标**: 同步 2026-08 Skills 规范（`disable-model-invocation` 手动触发、Slash/Skill 叠加调用、SKILL.md 编写规范核对、`[!tip] 大白话`）

## 依据条目

| 来源 | 内容 |
|------|------|
| SB-18 | skill frontmatter 支持 `disable-model-invocation`（禁止模型自动调用，让用户手动运行）；设置后 Claude 会请你运行该 skill；Slash/Skill 可叠加加载（最多 5 个前置）。日期 v2.1.222 / v2.1.199 |
| SB-11 | 可叠加 `/skill-a /skill-b do XYZ` 形式连续加载最多 5 个前置 skill。日期 v2.1.199 |
| 官方 docs（skills 页） | `disable-model-invocation: true` 仅用户可调用，Claude 无法自动加载，description 不进上下文，Claude 尝试调用会被拦截并请你手动 `/skill-name`；`user-invocable: false` 反向。所有 frontmatter 字段可选，仅 `description` 推荐。`name` 默认取目录名。叠加：第一个 skill + 最多 5 个，尾部文本作为 `$ARGUMENTS` 同时传给每个。`SKILL.md` 控制在 500 行内。命名参数用 `arguments` 字段 + `$name`。调试用 `claude --debug` 看 frontmatter 解析错误 |

## 过时点清单（更新）

| # | 位置 | 原文（过时） | 问题 | 处置 |
|---|------|-------------|------|------|
| 1 | frontmatter `updated` | `2026-07-12` | 需同步到本次更新 | 改为 `2026-08-10` |
| 2 | 标题 `### 当前 Skills 格式（v2.1.207）` | `v2.1.207` | 版本号过时，Skills 变更已到 v2.1.222 | 改为 `（2026-08 现行规范）`，不锁死版本号 |
| 3 | Frontmatter 表 `name` 行 | 必填 ✅ | 官方规范所有字段可选，`name` 默认取目录名 | 必填列改 `❌（默认取目录名）` |
| 4 | Frontmatter 表 `description` 行 | 必填 ✅ | 官方规范为「推荐」，未写则取正文首段 | 必填列改 `✅ 推荐（未写取正文首段）` |
| 5 | Frontmatter 表字段缺失 | 无 `when_to_use` / `arguments` / `user-invocable` | 新规范补齐；`model: haiku` 字段名不标准 | 补 3 个字段，`model: haiku` 归一为 `model` |
| 6 | Frontmatter 表 `disable-model-invocation` 行 | `禁止 Claude 自动触发`（说明太薄） | SB-18 新行为：仅用户手动运行，Claude 会请你运行 | 扩写说明 + 新增「调用控制」小节 |
| 7 | 「描述要 pushy」tip | 只讲提高自动调用率 | 未区分「想要自动触发」与「想手动触发」两条路 | 追加一句：不想自动触发时用 `disable-model-invocation` |
| 8 | 命名参数 tip | 通过 `$ARGUMENTS.param_name` 引用 | 现行机制为 `arguments` 字段 + `$name` 占位符；`argument-hint` 仅作提示 | 改写为 `arguments` + `$name`，保留 v2.1.199+ 标注 |
| 9 | 参数 Q&A 示例 | `argument-hint: [database_type]` + `$ARGUMENTS.database_type` | 混淆 `argument-hint`（提示）与 `arguments`（定义参数） | 改为 `arguments: [database_type]` + `$database_type` |
| 10 | 调试 Q&A | `cat metadata.json \| jq .` | 旧 metadata.json 格式已废弃，SKILL.md frontmatter 出错时 skill 以空元数据加载 | 改为检查 SKILL.md frontmatter；用 `claude --debug` 看解析错误 |
| 11 | 「AI 不调用 Skill」 | 只列排查原因 | 缺少「若根本不想让模型自动触发」的正解 | 追加 `disable-model-invocation: true` 提示 |
| 12 | 缺「调用控制」 | 无 | SB-18：谁可以调用由两个字段控制 | 新增「调用控制（谁可以触发）」小节 + 对比表 |
| 13 | 缺「叠加调用」 | 无 | SB-11：`/a /b do XYZ` 连续加载 | 新增「Slash / Skill 叠加调用」小节 |
| 14 | 缺 FAQ | 无 | 新行为常见疑问 | 新增「如何防止 Claude 自动触发 Skill？」 |
| 15 | 与旧格式对比「参数传递」行 | `命名参数（v2.1.199+）` | 机制名称更新 | 改为 `命名参数（arguments + $name，v2.1.199+）` |
| 16 | 示例 frontmatter description | `description: 根据...当用户说"写查询"...时触发。` | YAML 值含引号等特殊字符，需加引号 | 加引号：`description: "..."`（单引号替换内部双引号） |
| 17 | 核心概念 | 无大白话 | 用户偏好 | 新增 3 处 `[!tip] 大白话` |
| 18 | 末尾 | 无 `## 更新记录` | 规范要求追加 | 新增 `## 更新记录` 2026-08-10 行 |

## 新增点

| # | 位置 | 新增内容 | 依据 |
|---|------|---------|------|
| N1 | 核心概念·格式段 | `[!tip] 大白话`（SKILL.md = 带说明书的提示词；不想自动触发加 disable-model-invocation） | 用户偏好 + SB-18 |
| N2 | 核心概念·Frontmatter 段 | `[!tip] 大白话（谁可以调用）`（两个开关控制谁触发） | 用户偏好 + 官方 docs |
| N3 | 核心概念·Frontmatter 段 | 「调用控制（谁可以触发）」小节 + 三行对比表 + `[!warning]` 拦截行为 | 官方 docs（Control who invokes a skill） |
| N4 | 核心概念·新小节 | 「Slash / Skill 叠加调用」+ `[!tip] 大白话（叠加）` | SB-11 + 官方 docs |
| N5 | FAQ | 「如何防止 Claude 自动触发 Skill？」 | SB-18 + 官方 docs |
| N6 | 更新记录 | 追加 2026-08-10 行 | 规范 |

## 保留（无过时证据）

- **标准结构**（`.claude/skills/<name>/SKILL.md`，kebab-case）：官方 docs 一致
- **500 行限制**：官方 docs「Keep SKILL.md under 500 lines」一致
- **支持文件拆分**（examples.md / scripts/）：官方 docs 一致
- **`allowed-tools` / `disallowed-tools` / `context: fork` / `model`**：官方 docs 仍支持
- **description 要 pushy（关键词触发）**：对可自动触发的 skill 仍成立
- **Skills vs Subagents 区别、Skills vs Dynamic Workflows 区别**：无变更证据
- **与旧格式对比表**（单文件 / YAML frontmatter / Agent Skills 开放标准）：仍成立
