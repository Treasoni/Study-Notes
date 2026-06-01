# Updating Existing Notes

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

When the user wants to add content to or refresh an existing published note, invoke `/update-workflow` — do NOT re-run the full creation pipeline.

## Workflow Diagram

```
User: "add this to my X note" / "update the Y section"
│
├─ Step 1: 定位笔记 + 解析结构
│   ├─ 多级搜索: 精确路径 → OUTPUT_PATH → 3-published/ → vault 根目录
│   └─ 解析: frontmatter, heading tree, callouts, tables, wikilinks
│
├─ Step 2: 检测意图 (INSERT / REFRESH)
│   ├─ INSERT: 用户提供了具体文本，指定插入位置
│   ├─ REFRESH: 用户描述"哪里过时"，需二次决策
│   │   ├─ 提供新内容 → 转入 INSERT 模式
│   │   └─ 未提供内容 → 询问: 直接替换 or 重新搜集？
│   └─ 显式指定 update_mode → 跳过自动检测
│
├─ Step 3: 备份原笔记 + 调度 /update Skill
│   ├─ 备份: cp "{笔记}" "{SYSTEM_ROOT}/4-meta/backups/{note}-{timestamp}.md"
│   ├─ 传递上下文 (heading_tree, callout_types, table_format, wikilinks, frontmatter)
│   └─ Skill(skill="update", args={...})
│       └─ REFRESH 时内部执行 mini collect→write 循环
│
├─ Step 4: 轻量验证
│   ├─ 标题层级一致性 (无越级)
│   ├─ Wikilink 完整性 (抽查 ≥3 个)
│   ├─ Frontmatter updated 字段已更新
│   └─ 无多余内容
│
├─ Step 5: 展示 diff 摘要 + 硬停止
│   └─ 等待用户确认 / 修改 / 取消
│
└─ Step 5b: 用户确认循环
    ├─ 修改 → 调整内容 → 重新 Step 4 → 重新展示
    ├─ 确认 → 任务完成
    └─ 取消 → 恢复备份, 任务终止
```

## Two Modes

**INSERT** — User provides new content directly:
```
User: "add this paragraph about useEffect cleanup to my React hooks note"
→ /update-workflow locates the note, inserts at the right spot,
  matches surrounding formatting, and updates the frontmatter updated field.
```

**REFRESH** — Content is outdated, may need fresh research:
```
User: "the React hooks section is outdated, update it with current patterns"
→ /update-workflow detects REFRESH intent, then:
  - User provides new content → replaces in-place (INSERT mode, no TODO.md)
  - User needs fresh research → runs focused mini collect→write for that section
```

When re-research is chosen, the `/update` skill creates a mini `{SYSTEM_ROOT}/TODO.md`:

```markdown
# TODO - REFRESH: {topic}
- [ ] mini-collect - 定向资料收集
- [ ] mini-curate - 定向资料整理
- [ ] mini-write - 定向更新笔记
```

Before each mini-phase: MUST execute Read tool on TODO.md, verify prior phases are `[x]`.
After each mini-phase: MUST execute Write tool to mark it `[x]`.
After all done: MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"`.

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `note_query` | 笔记名称或完整路径 | ✅ |
| `user_content` | 用户提供的新内容（INSERT 模式） | INSERT 时必填 |
| `target_section` | 要刷新的章节名（REFRESH 模式） | REFRESH 时必填 |
| `update_mode` | 显式指定 INSERT/REFRESH（省略时自动检测） | ❌ |

## Step Details

### Step 1: 定位笔记 + 解析结构

**多级搜索策略**（按优先级递减）：

1. **精确路径**：如果查询是合法文件路径，直接读取
2. **OUTPUT_PATH**：在 `{OUTPUT_PATH}/3-published/` 中搜索匹配文件
3. **全 3-published/**：在 `{VAULT_PATH}/StudySystem/3-published/` 中搜索
4. **vault 根目录**：在 `{VAULT_PATH}/` 中按文件名模糊匹配（最后手段）

搜索工具：优先用 `Glob` 按文件名模式匹配，必要时用 `Grep` 按内容关键词定位。

**多个匹配**：列出候选笔记，让用户选择。不要猜测。

**找不到**：告知用户未找到匹配笔记，请确认名称或路径。

**解析结构**：

1. 读取完整内容
2. 解析 YAML frontmatter：`type`、`tags`、`created`、`updated`、`aliases`
3. 提取标题层级树（heading tree）
4. 识别 Callout 块类型和分布
5. 识别表格格式约定
6. 提取所有 `[[wikilinks]]` 列表

### Step 2: 检测意图

**自动检测逻辑**：

| 信号 | 倾向 INSERT | 倾向 REFRESH |
|------|------------|-------------|
| 关键词 | "加一段"、"插入"、"补充"、"追加"、"添加" | "更新"、"刷新"、"过时了"、"替换" |
| 内容 | 用户提供了具体文本 | 用户描述了"哪里不对"或"需要更新" |
| 上下文 | 指定了插入位置 | 指定了要更新的章节名 |

**REFRESH 二次决策**：用户提供了新内容 → 直接替换（INSERT 模式）；未提供 → 询问用户选择。

**显式指定 `update_mode`**：跳过自动检测，直接使用指定模式。

### Step 3: 备份 + 调度 /update

> 详见 `.claude/skills/update/SKILL.md`

在调用 `/update` skill 前，备份原笔记：

```
Bash: cp "{笔记路径}" "{SYSTEM_ROOT}/4-meta/backups/{note-name}-{timestamp}.md"
```

传递结构解析结果和意图检测结果，调度 `/update` skill 执行实际更新操作。orchestrator 需传递以下上下文：

- 父主题名
- 父笔记类型
- 目标章节标题层级
- 格式约定
- 目录隔离参数

**REFRESH mini 研究循环**：/update 内部执行 mini collect→write 循环，遵循 TODO.md 状态机规则。

### Step 4: 轻量验证

/update skill 返回后执行轻量验证（结构性检查，不重新解析整篇语义）：

1. **标题层级一致性**：修改后的标题层级是否仍连贯，无越级
2. **Wikilink 完整性**：抽查至少 3 个现有 `[[wikilinks]]`，确认未被破坏
3. **Frontmatter 已更新**：`updated` 字段是否已设为当前日期
4. **无多余内容**：确认没有生成笔记类型之外的内容

验证失败 → 从备份恢复原笔记，记录问题到 `error-log.md`，告知用户并请求是否需要修复。

### Step 5: 展示 diff 摘要 + 硬停止

向用户展示更新摘要：

```
**更新完成** — {笔记名称}

- 模式：{INSERT / REFRESH}
- 目标章节：{章节名}
- 变更摘要：
  - {具体改了什么，新增/替换了多少内容}
  - {如有：REFRESH 模式下的研究来源}
- 验证结果：{通过 / 存在问题}
```

确认前不得继续。等待用户明确确认或要求修改。

### Step 5b: 用户确认循环

- **用户要求修改** → 根据反馈调整内容 → 重新执行 Step 4 验证 → 重新展示摘要
- **确认**（"确认"/"没问题"/"可以"） → 任务完成
- **取消**（"算了"/"取消"） → 恢复备份，任务终止

## Key Rules for Updates

- **Minimal diff**: Only modify the target section, do not re-beautify the whole note
- **Match existing style**: New content uses the same callout types, table conventions, code block languages
- **Preserve wikilinks**: Do not touch or break existing `[[links]]`
- **Update frontmatter**: Set `updated: YYYY-MM-DD` to current date

## Prohibited Actions

- Do not skip Step 1 multi-level search and assume the note does not exist
- Do not skip intent detection and execute the update directly
- Do not add information the user did not provide in INSERT mode
- Do not start a research cycle for unrelated sections in REFRESH mode
- Do not modify unrelated sections
- Do not delete or break existing `[[wikilinks]]`
- Do not change the note's template type (e.g. concept to practice)
- Do not skip verification and show results directly
- Do not skip user confirmation and write directly

## 产出

- 原笔记文件（in-place 更新）
- 更新后的 frontmatter（`updated` 字段已更新）
- 更新摘要（修改章节、内容变化行数）
