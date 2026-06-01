---
name: update-workflow
description: 笔记更新编排层。定位目标笔记、解析结构、自动检测 INSERT/REFRESH 意图，调度 /update skill 执行更新，轻量验证后展示 diff 摘要供用户确认。触发时机：用户要求修改、添加或更新已有笔记内容时。
---

# Skill: update-workflow（笔记更新编排）

> 详见 `docs/updating-notes.md`

## 触发时机

用户要求修改、添加或更新已有笔记内容时（如 "在 XX 笔记里加一段"、"更新 XX 的 YY 章节"、"这篇笔记过时了"）。

## 输入参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `note_query` | 目标笔记的查询信息（名称/路径/关键词） | "React Hooks 总结"、`3-published/react-hooks.md` |
| `user_content` | 用户提供的新内容（INSERT 模式下必需） | "useEffect 的 cleanup 用法..." |
| `target_section` | 目标章节名或位置 | "## Cleanup 模式"、"末尾" |
| `update_mode` | 显式指定模式（可选，省略则自动检测） | `insert` / `refresh` |

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为编排调度员，`/update` skill 作为执行者。

```
主 Agent (编排层)                   /update Skill (执行层)
    │                                    │
    ├─ Step 1: 定位笔记 + 解析结构       │
    ├─ Step 2: 检测意图 (INSERT/REFRESH) │
    ├─ Step 3: 备份原笔记 + 调度 /update ──►│
    │                                    ├─ 执行更新（含自身用户确认）
    │                                    ├─ REFRESH 时内部调度 mini collect→write
    │◄──── 更新结果 ───────────────────┤
    ├─ Step 4: 轻量验证                  │
    ├─ Step 5: 展示 diff 摘要            │
    ├─ Step 5b: 硬停止 — 等待用户确认    │
```

**核心原则**：主 Agent 不直接修改笔记文件，所有写操作通过 `/update` skill 完成。

## 执行步骤

### Step 1: 定位笔记 + 解析结构

**多级搜索策略**（按优先级递减）：

1. **精确路径**：如果 `note_query` 是合法文件路径，直接读取
2. **OUTPUT_PATH**：在 `{OUTPUT_PATH}/3-published/` 中搜索匹配文件
3. **全 3-published/**：在 `{VAULT_PATH}/StudySystem/3-published/` 中搜索
4. **vault 根目录**：在 `{VAULT_PATH}/` 中按文件名模糊匹配（最后手段）

搜索工具：优先用 `Glob` 按文件名模式匹配，必要时用 `Grep` 按内容关键词定位。

**如果找到多个匹配**：列出候选笔记，让用户选择。不要猜测。

**如果找不到**：告知用户未找到匹配笔记，请确认笔记名称或路径。

**解析结构**（找到笔记后）：

1. 读取完整内容
2. 解析 YAML frontmatter：`type`、`tags`、`created`、`updated`、`aliases`
3. 提取标题层级树（heading tree）：所有 `#` ~ `######` 标题及其层级关系
4. 识别 Callout 块类型和分布
5. 识别表格格式约定
6. 提取所有 `[[wikilinks]]` 列表

将解析结果暂存，传递给 Step 2 和 Step 3 使用。

### Step 2: 检测意图（INSERT vs REFRESH）

**自动检测逻辑**：

| 信号 | 倾向 INSERT | 倾向 REFRESH |
|------|------------|-------------|
| 关键词 | "加一段"、"插入"、"补充"、"追加"、"添加" | "更新"、"刷新"、"过时了"、"改一下"、"替换" |
| 内容 | 用户提供了具体文本 | 用户描述了"哪里不对"或"需要更新" |
| 上下文 | 指定了插入位置 | 指定了要更新的章节名 |

**REFRESH 二次决策**：

当检测到 REFRESH 意图后，需进一步判断：

- 用户提供了新内容 → 直接替换，转入 INSERT 模式
- 用户未提供新内容 → 询问用户：
  > "你是想直接替换这部分内容（请提供新内容），还是需要我重新搜集资料后更新？"
  - 选择"提供新内容" → 转入 INSERT 模式
  - 选择"重新搜集" → 确认 REFRESH 模式，进入 Step 3 执行 mini 研究循环

**用户显式指定 `update_mode` 时**：跳过自动检测，直接使用指定模式。

### Step 3: 备份原笔记 + 调度 /update Skill

> 传入 mode 参数后，/update skill 跳过自身的意图检测步骤。

**备份原笔记**：在调用 /update 前，保存原笔记副本用于取消时恢复：

```
Bash: cp "{笔记路径}" "{SYSTEM_ROOT}/4-meta/backups/{note-name}-{timestamp}.md"
```

将 Step 1 的结构解析结果和 Step 2 的意图检测结果打包，调度 `/update` skill：

```
Skill(
  skill="update",
  label: `update:{note-name}`,
  phase: "Phase 3: Update",
  args={
    note_path: "{解析出的笔记路径}",
    mode: "{insert|refresh}",
    user_content: "{用户提供的内容，INSERT 模式}",
    target_section: "{目标章节名}",
    heading_tree: "{标题层级树}",
    callout_types: "{Callout 类型列表}",
    table_format: "{表格格式约定}",
    wikilinks: "{现有 wikilink 列表}",
    frontmatter: "{frontmatter 内容}"
  }
)
```

**REFRESH 模式（mini 研究循环）特别说明**：

当 mode 为 refresh 且需要重新搜集时，/update skill 内部会执行 mini collect→write 循环。

**mini TODO.md 管理**：在启动 mini 研究循环前，创建临时 TODO 文件跟踪进度：

```
# TODO - REFRESH: {subtopic}
- [ ] mini-collect - 定向资料收集
- [ ] mini-curate - 定向资料整理
- [ ] mini-write - 定向更新笔记
```

- 每完成一个 mini-phase，通过 Write 工具将对应的 `[ ]` 标记为 `[x]`
- mini 研究循环完成后，通过 Bash 工具删除临时 TODO：`rm "{SYSTEM_ROOT}/TODO.md"`

**/update 失败处理**：

如果 /update 报错或 Step 4 验证发现严重问题：
1. 如有备份 → 恢复原始笔记：`cp "{SYSTEM_ROOT}/4-meta/backups/{note-name}-{timestamp}.md" "{笔记路径}"`
2. 记录错误到 `{SYSTEM_ROOT}/4-meta/error-log.md`
3. 告知用户错误原因，请求指示

编排层需确保传入以下上下文：

- **父主题名**：从笔记 frontmatter 或标题中提取
- **父笔记类型**：concept / practice / compare / cheat-sheet
- **目标章节标题层级**：如 `###`
- **父笔记格式约定**：Callout 类型、表格风格、代码块语言标注等
- **目录隔离参数**：mini 循环写入 `0-inbox/{subtopic}/`、`1-curated/{subtopic}/`、`2-drafts/{subtopic}/`，与父主题目录分离

### Step 4: 轻量验证

/update skill 返回后，编排层执行轻量验证（读取修改后的文件，只做结构性检查——标题层级、双链、frontmatter——不重新解析整篇语义）：

1. **标题层级一致性**：修改后的标题层级是否仍然连贯，无越级（如 `##` 下面直接出现 `####`）
2. **Wikilink 完整性**：抽查至少 3 个现有 `[[wikilinks]]`，确认未被破坏
3. **Frontmatter 已更新**：`updated` 字段是否已设为当前日期
4. **无多余内容**：确认没有生成笔记类型之外的内容（如 INSERT 模式下不应出现 frontmatter）

如果验证失败，记录问题并告知用户，请求是否需要修复。

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

用户可能要求修改。此时进入确认循环：

1. **用户要求修改** → 根据用户反馈调整内容
2. **重新执行 Step 4 验证** → 对修改后的结果再次做轻量验证
3. **重新展示更新摘要** → 展示调整后的 diff 摘要
4. **重复** → 直到用户明确确认（"确认"/"没问题"/"可以"）或取消（"算了"/"取消"）

**确认** → 任务完成（文件已由 /update 写入）。
**取消** → 恢复备份：`cp "{SYSTEM_ROOT}/4-meta/backups/{note-name}-{timestamp}.md" "{笔记路径}"`，任务终止。

## 产出

- 原笔记文件（in-place 更新）
- 更新后的 frontmatter（`updated` 字段已更新）
- 更新摘要（修改章节、内容变化行数）

## 禁止行为

- 不要跳过 Step 1 的多级搜索，直接假设笔记不存在
- 不要跳过意图检测，直接执行更新
- 不要在 INSERT 模式下添加用户未提供的信息
- 不要在 REFRESH 模式下对不相关的章节启动研究循环
- 不要修改不相关章节的内容
- 不要删除或破坏现有的 `[[wikilinks]]`
- 不要改变笔记的 template type（如把 concept 改成 practice）
- 不要跳过验证步骤直接展示结果
- 不要跳过用户确认直接写入文件
