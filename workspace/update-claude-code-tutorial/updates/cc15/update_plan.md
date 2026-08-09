# cc15 更新计划（Update Plan）

- **note_id**: cc15
- **模式**: 局部 patch（不重写未过时段落，保留原结构与写作风格）
- **产出**: `updates/cc15/updated_note.md`（先写工作区，不直接改原 vault 文件）

## 编辑步骤（按文件顺序）

### 1. frontmatter
- `updated: 2026-07-12` → `2026-08-10`
- `status: updated` 保持不变

### 2. 核心概念·格式段
- 标题 `### 当前 Skills 格式（v2.1.207）` → `### 当前 Skills 格式（2026-08 现行规范）`
- 「2026 年格式变更」info callout 后新增 `[!tip] 大白话`：SKILL.md = 带说明书的提示词文件；不想让模型自动触发就在 frontmatter 加 `disable-model-invocation: true`

### 3. Frontmatter 关键字段表
- `name` 必填 ✅ → `❌`，说明改为「显示名（默认取目录名；命令名来自目录/文件名）」
- `description` 必填 ✅ → `✅ 推荐`，说明追加「未写则取正文首段」
- `model: haiku` → 归一为 `model`
- 表内补 3 个字段：`when_to_use`（触发场景补充）、`arguments`（命名位置参数）、`user-invocable`（仅 Claude 调用）
- `disable-model-invocation` 行说明扩写：设为 `true` 时禁止 Claude 自动触发，仅用户手动运行
- 表后新增 `[!tip] 大白话（谁可以调用）`

### 4. 新增「调用控制（谁可以触发）」小节
插在「描述要 pushy」tip 之后、与旧格式对比之前：
- 三行对比表：（默认）/ `disable-model-invocation: true` / `user-invocable: false`（用户可调用 / Claude 可调用 / description 进上下文）
- `[!warning]` 拦截行为：Claude 尝试自动调用被禁用 skill 时会被拦截，并建议你手动运行 `/skill-name`

### 5. 新增「Slash / Skill 叠加调用（v2.1.199+）」小节
插在「调用控制」之后：
- `/skill-a /skill-b do XYZ` 尾部文本作为 `$ARGUMENTS` 同时传给每个 skill
- 第一个 skill 之后最多再叠加 5 个（合计最多 6 个）
- 遇到非内联用户可调用 skill（`/code-review` 子代理、`/loop` 参数以 `/` 开头）提前停止
- v2.1.199 之前只有第一个 skill 会加载
- 末尾 `[!tip] 大白话（叠加）`

### 6. 与旧格式对比表
- 「参数传递」行：`命名参数（v2.1.199+）` → `命名参数（arguments + $name，v2.1.199+）`

### 7. 步骤 2 示例 frontmatter
- `description:` 值加引号（YAML 特殊字符）：`"根据自然语言描述生成 SQL 查询语句。当用户说'写查询'、'查数据库'、'SQL'时触发。"`

### 8. 命名参数 tip（步骤 2 后）
- 改写为：`arguments` 字段声明命名参数，正文 `$参数名` 引用；`argument-hint` 仅提示不定义参数；`$ARGUMENTS[N]` / `$N` 按位置取参，`$ARGUMENTS` 取全部

### 9. 注意事项·AI 不调用 Skill
- 三个 ❌ 排查点后追加一个提示块：若根本不想让模型自动触发，直接加 `disable-model-invocation: true`，不要靠写模糊 description 来阻止

### 10. FAQ
- 参数 Q&A：`argument-hint: [database_type]` + `$ARGUMENTS.database_type` → `arguments: [database_type]` + `$database_type`
- 调试 Q&A：`cat metadata.json | jq .` → 检查 SKILL.md frontmatter；`claude --debug` 看解析错误；补充 `/skill-name` 手动触发测试
- 新增 FAQ：「如何防止 Claude 自动触发 Skill？」（`disable-model-invocation: true`，Claude 会请你手动运行；相对地 `user-invocable: false` 从 `/` 菜单隐藏）

### 11. 更新记录
- 在 `## 相关文档` 前插入 `## 更新记录`，追加 2026-08-10 行

## 不修改的段落

- 标准结构、500 行限制、支持文件拆分、allowed-tools / disallowed-tools / context: fork、Skills vs Subagents、Skills vs Dynamic Workflows、与旧格式对比表其余行

## 风险与假设

1. **叠加数量表述**：SB-11/任务目标写「最多 5 个前置 skill」，官方 docs 原文为「第一个 skill 之后最多再叠加 5 个（合计最多 6 个）」。笔记按官方 docs 精确表述，并在报告中标注差异。
2. **版本号**：标题不锁死具体版本号（改「2026-08 现行规范」），避免后续小版本变更再次过时。
3. **`arguments` 机制**：笔记原 `$ARGUMENTS.param_name` 语法在现行官方 docs 无对应，改为 `arguments` + `$name`，依据官方 docs。
4. **YAML 引号**：示例 description 加引号并用单引号替换内部双引号，仅影响示例可读性，不影响 skill 实际语义。
