# cc15 更新报告（Update Report）

- **note_id**: cc15
- **笔记**: `AI学习/Claude Code 教程/04-高级功能/如何编写Skills.md`
- **更新日期**: 2026-08-10
- **更新方式**: 局部 patch（未重写未过时段落，保留原结构和写作风格）
- **输出**: `updates/cc15/updated_note.md`（未改动原 vault 文件）

## 变更摘要

共定位 **18 处过时点 + 6 处新增**，全部已应用：

### 调用控制（核心，SB-18）
- 新增「调用控制（谁可以触发）」小节：`disable-model-invocation: true` 时仅用户可手动运行、Claude 无法自动加载、description 不进上下文；`user-invocable: false` 反向（仅 Claude 可调用）
- 扩写 frontmatter 表 `disable-model-invocation` 行，并补充 `[!warning]`：Claude 尝试自动调用被禁 skill 会被拦截，并会请你手动运行 `/skill-name`
- 新增大白话 tip 说明两个开关的区别
- 新增 FAQ「如何防止 Claude 自动触发 Skill？」

### Slash/Skill 叠加调用（SB-11）
- 新增「Slash / Skill 叠加调用（v2.1.199+）」小节：`/skill-a /skill-b do XYZ`，尾部文本作为 `$ARGUMENTS` 同时传给每个 skill；第一个之后最多再叠加 5 个（合计最多 6 个）
- 标注展开停止条件（`/code-review` 子代理、`/loop` 参数以 `/` 开头）

### SKILL.md 编写规范核对
- `name` / `description` 必填列修正：官方规范所有字段可选，仅 `description` 推荐（未写取正文首段），`name` 默认取目录名
- 表内补 `when_to_use` / `arguments` / `user-invocable` 三字段；`model: haiku` 归一为 `model`
- 命名参数机制修正：原 `$ARGUMENTS.param_name` → `arguments` 字段 + `$参数名`；`argument-hint` 明确「仅提示不定义参数」
- 调试 Q&A 修正：移除已废弃的 `metadata.json` 引用，改为检查 SKILL.md frontmatter + `claude --debug`
- 标题版本号 `v2.1.207` → `2026-08 现行规范`（避免锁死版本号）
- 示例 frontmatter description 加引号（YAML 特殊字符）

### 用户偏好
- 核心概念新增 3 处 `[!tip] 大白话`（格式、谁可调用、叠加）
- 追加 `## 更新记录` 2026-08-10 行
- frontmatter `updated` → 2026-08-10

## 依据来源

- SB-18（`disable-model-invocation` 手动触发 + Claude 请你运行）、SB-11（Slash/Skill 叠加，最多 5 个前置）
- 官方 docs `https://code.claude.com/docs/en/skills`（frontmatter 全字段、调用控制对比表、叠加细节、500 行限制、调试方法）

## 风险项

1. **叠加数量表述差异**：SB-11/任务目标写「最多 5 个前置 skill」，官方 docs 原文为「第一个 skill 之后最多再叠加 5 个（合计最多 6 个）」。笔记按官方 docs 精确表述；如需严格对齐任务目标措辞可改。
2. **`arguments` 机制**：笔记原 `$ARGUMENTS.param_name` 语法在现行官方 docs 无对应，已按官方改为 `arguments` + `$name`。若某版本仍兼容旧语法，不影响新写法可用性。
3. **版本号**：标题不再锁死具体版本号，改为「2026-08 现行规范」，避免小版本变更再次过时。

## needs-review

**是（低优先级）**。`disable-model-invocation` 与叠加调用的行为均有 SB-18/SB-11 + 官方 docs 双重支撑，可信度高；仅「叠加数量（5 vs 6）」「旧参数语法兼容性」两项措辞差异建议在写回前由用户确认。
