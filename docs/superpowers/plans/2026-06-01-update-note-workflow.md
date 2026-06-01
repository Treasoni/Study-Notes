---
archived-with: 2026-06-02-update-note-workflow
status: final
---
# Update Note Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 新增 `update-workflow` skill，作为笔记更新的工作流编排层，支持 INSERT（追加内容）和 REFRESH（定向刷新章节）两种场景。

**Architecture:** 单个 SKILL.md 文件定义完整工作流，包装现有 `update` skill（INSERT 模式），内部直接调度 mini collect→curate→write 研究循环（REFRESH 模式），提供结构验证和用户确认。

**Tech Stack:** Markdown (SKILL.md), Bash (comet scripts for state management)

---

## File Structure

| 操作 | 文件 | 职责 |
|------|------|------|
| Create | `.claude/skills/update-workflow/SKILL.md` | 工作流编排 skill 定义 |
| Modify | `docs/updating-notes.md` | 更新工作流文档 |

---

### Task 1: Create update-workflow SKILL.md

**Files:**
- Create: `.claude/skills/update-workflow/SKILL.md`

- [ ] **Step 1: Create skill directory**

```powershell
New-Item -ItemType Directory -Force -Path ".claude/skills/update-workflow" | Out-Null
```

- [ ] **Step 2: Write SKILL.md with frontmatter**

Write `.claude/skills/update-workflow/SKILL.md`:

```markdown
---
name: update-workflow
description: 笔记更新工作流。编排层：定位目标笔记、检测更新意图（INSERT/REFRESH）、执行更新、轻量验证、用户确认。触发时机：用户要求更新已有笔记时。
---

# Skill: update-workflow（笔记更新工作流）

## 触发时机

用户要求更新、修改、添加内容到已有笔记时。

## 与 update skill 的关系

- `update-workflow`：工作流编排层（本 skill）
- `update`：底层执行者，负责实际的内容插入操作

INSERT 模式委托 `update` skill；REFRESH 模式的 mini research cycle 由本 skill 内部调度。

## 输入

- `note_query`：笔记名称或完整路径
- `user_content`：用户提供的新内容（INSERT 模式）
- `target_section`：要刷新的章节名（REFRESH 模式）
- `update_mode`：可选，显式指定 INSERT/REFRESH（省略时自动检测）

## 执行步骤

### Step 1: 定位目标笔记 + 解析结构

#### 1a. 定位笔记

1. 如果 `note_query` 是路径（含 `/` 或 `.md` 后缀）→ 直接定位
2. 如果是名称 → 多级搜索：
   - 优先搜索用户配置的 `OUTPUT_PATH`（来自 `.obsidian-config.md`）
   - 再搜索 `{SYSTEM_ROOT}/3-published/`
   - 再搜索整个 vault 根目录
3. 找到多个匹配 → 列出候选让用户选择
4. 找不到 → 报错并建议用户指定路径

#### 1b. 解析笔记结构

读取目标笔记后，提取：
- YAML frontmatter：`type`（concept/practice/compare/cheat-sheet/experience）、`tags`、`created`、`updated`
- 标题层级树（`#` → `##` → `###` ...）
- Callout 类型（`> [!note]`、`> [!tip]` 等）
- 表格格式和代码块语言
- 现有 wikilinks 列表

产出 `note_context` 对象，传递给后续步骤。

### Step 2: 检测更新意图

#### 自动检测规则

| 关键词/模式 | → 意图 |
|-------------|--------|
| "加上"、"添加"、"补充"、"追加" + 用户提供内容 | INSERT |
| "过时"、"更新"、"刷新"、"替换" + 指定章节 | REFRESH |
| "在 XXX 章节后加"、"在末尾追加" | INSERT |
| 模糊不清 | → 询问用户 |

#### REFRESH 二级决策

检测到 REFRESH 后，询问用户：
1. "直接替换此章节内容？" → 走 INSERT（用户提供替换内容）
2. "先重新搜集资料再更新？" → 走 mini research cycle（Step 3b）

### Step 3: 执行更新

#### Step 3a: INSERT 模式

委托 `/update` skill，传入：
- 目标笔记路径
- 用户提供的新内容
- 目标位置（章节名或"追加到末尾"）
- note_context 中的格式约定（Callout 类型、表格风格等）

**禁止行为**：
- 不要重新格式化整篇笔记
- 不要修改不相关章节
- 不要删除或破坏现有 `[[wikilinks]]`

#### Step 3b: REFRESH 模式（Mini Research Cycle）

**范围限定**：仅针对目标子主题，不重新搜集整个笔记的资料。

**目录隔离**：
- `0-inbox/{subtopic}/raw/`
- `1-curated/{subtopic}/`
- `2-drafts/{subtopic}/`

**传递父主题上下文**（调用各 skill 时必须传入）：
- 父主题名（如 "React"）
- 父笔记类型（concept/practice/compare/cheat-sheet/experience）
- 目标章节的标题层级（如 `###`）
- 父笔记中观察到的格式约定（Callout 类型、表格风格等）

**执行流程**：

1. 创建 mini TODO.md：
```markdown
# TODO - REFRESH: {subtopic}
- [ ] mini-collect - 定向资料收集
- [ ] mini-curate - 定向资料整理
- [ ] mini-write - 定向更新笔记
```

2. 调用 `/collect`：
   - topic 设为子主题名（如 "useEffect cleanup"）
   - 搜索词附加父主题上下文（如 "React useEffect cleanup pattern 2025"）
   - 输出到 `0-inbox/{subtopic}/raw/`
   - 完成后标记 TODO.md `[x]`

3. 调用 `/curate`：
   - 仅整理新搜集的资料
   - 按四维度评分（权威性/时效性/完整性/可读性）
   - 输出到 `1-curated/{subtopic}/`
   - 完成后标记 TODO.md `[x]`

4. 调用 `/write`：
   - **必须要求只生成目标章节的正文内容**
   - **不要**生成 YAML frontmatter
   - **不要**生成完整笔记结构（标题、概述、总结等）
   - **保留父主题上下文**：告知 "这是 {父主题} 笔记中 {章节名} 章节的内容更新"
   - **匹配格式约定**：告知父笔记中使用的 Callout 类型、表格风格等
   - 输出纯章节正文
   - 完成后标记 TODO.md `[x]`

5. 委托 `/update` skill 将纯章节正文插入父笔记

6. 清理 mini TODO.md：`rm "{SYSTEM_ROOT}/TODO.md"`

### Step 4: 轻量验证

更新完成后自动执行以下检查：

| 检查项 | 方法 | 失败处理 |
|--------|------|----------|
| 标题层级连贯性 | 扫描所有 `#` 标题，检查是否跳级（如 `##` → `####`） | 报告具体位置，建议修正 |
| 双链完整性 | 提取所有 `[[wikilinks]]`，检查目标文件是否存在 | 报告断链，建议修复或删除 |
| frontmatter updated | 检查 `updated` 字段是否为当前日期 | 自动修正 |

**验证不阻塞**：发现问题时向用户报告并询问是否继续。不自动阻止写入。

### Step 5: 用户确认

展示 diff 摘要：

```
📝 更新摘要
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
目标笔记: {note_path}
更新模式: {INSERT|REFRESH}
修改章节: {section_name}
内容变化: +{added_lines} 行 / ~{modified_lines} 行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**确认流程**：
1. 展示 diff 摘要
2. 用户确认 → 保存文件，流程结束
3. 用户要求修改 → 调整后重新展示摘要
4. 用户取消 → 不保存，流程结束

## 硬停止

本阶段任务完成。向用户展示 diff 摘要（修改了哪个章节、新增/替换了多少内容）。

确认前不得继续。等待用户明确确认或要求修改。

## 禁止行为

- 不要重新格式化整篇笔记 — 只动需要改的部分
- 不要修改不相关章节的内容
- 不要删除或破坏现有的 `[[wikilinks]]`
- 不要改变笔记的 template type
- 不要在 INSERT 模式下添加用户未提供的信息
- 不要在 REFRESH 模式下对不相关的章节启动研究循环
- 主 Agent 不要直接读取 curated/ 目录下的文件内容（交给各子 skill）
```

- [ ] **Step 3: Verify file exists and is non-empty**

```powershell
Get-Item ".claude/skills/update-workflow/SKILL.md" | Select-Object Name, Length
```

Expected: Name="SKILL.md", Length > 500

- [ ] **Step 4: Commit**

```powershell
git add .claude/skills/update-workflow/SKILL.md
git commit -m "feat: add update-workflow skill for note update orchestration"
```

---

### Task 2: Update documentation

**Files:**
- Modify: `docs/updating-notes.md`

- [ ] **Step 1: Read current doc**

```powershell
Get-Content "docs/updating-notes.md" -Raw
```

- [ ] **Step 2: Rewrite docs/updating-notes.md**

Replace the entire content with:

```markdown
# Updating Existing Notes

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

When the user wants to add content to or refresh an existing published note, invoke `/update-workflow` — do NOT re-run the full creation pipeline.

## Workflow Overview

```
用户: "更新我的 XXX 笔记"
         │
         ▼
  ┌──────────────┐
  │ Step 1: 定位  │  找到目标笔记，解析结构
  │ + 意图识别    │  判断 INSERT / REFRESH
  └──────┬───────┘
         │
   ┌─────┴─────┐
   ▼           ▼
┌────────┐  ┌────────────┐
│ INSERT │  │  REFRESH   │
│ 用户提 │  │ 刷新过时   │
│ 供内容 │  │ 章节       │
└───┬────┘  └─────┬──────┘
    │             │
    │        ┌────┴────┐
    │        ▼         ▼
    │   ┌────────┐ ┌────────┐
    │   │直接替换│ │重新搜集│ ← mini collect→curate→write
    │   └───┬────┘ └───┬────┘
    │       │          │
    ▼       ▼          ▼
  ┌──────────────────────┐
  │ Step 3: 执行更新      │  委托 update skill 插入
  └──────────┬───────────┘
             │
  ┌──────────▼───────────┐
  │ Step 4: 轻量验证     │  标题层级 + 双链完整性
  └──────────┬───────────┘
             │
  ┌──────────▼───────────┐
  │ Step 5: 用户确认     │  审核 diff，确认或回退
  └──────────────────────┘
```

## Two Modes

**INSERT** — User provides new content directly:
```
User: "add this paragraph about useEffect cleanup to my React hooks note"
→ invoke /update-workflow — it locates the note, detects INSERT intent,
  delegates to /update skill for format-matching insertion
```

**REFRESH** — Content is outdated, may need fresh research:
```
User: "the React hooks section is outdated, update it with current patterns"
→ invoke /update-workflow — detects REFRESH intent, asks:
  1. "Replace in-place?" → user provides new content → INSERT mode
  2. "Re-research first?" → runs mini collect→curate→write → inserts result
```

## Key Rules for Updates

- **Minimal diff**: Only modify the target section, do not re-beautify the whole note
- **Match existing style**: New content uses the same callout types, table conventions, code block languages
- **Preserve wikilinks**: Do not touch or break existing `[[links]]`
- **Update frontmatter**: Set `updated: YYYY-MM-DD` to current date

## Verification

After update, the system automatically checks:
1. Heading level consistency (no skipped levels)
2. Wikilink integrity (no broken `[[links]]`)
3. Frontmatter `updated` field is current

Verification issues are reported but do not block the update — user decides whether to fix.
```

- [ ] **Step 3: Verify file updated**

```powershell
Get-Content "docs/updating-notes.md" -First 5
```

Expected: First line should be `# Updating Existing Notes`

- [ ] **Step 4: Commit**

```powershell
git add docs/updating-notes.md
git commit -m "docs: update updating-notes.md with new workflow orchestration"
```

---

### Task 3: Test INSERT mode

**Prerequisite:** Tasks 1-2 complete

- [ ] **Step 1: Identify a test note**

Find an existing note in the vault to use as test target:
```powershell
Get-ChildItem -Path (Get-Content ".obsidian-config.md" | Select-String "OUTPUT_PATH" | ForEach-Object { $_ -replace '.*OUTPUT_PATH:\s*', '' }) -Recurse -Filter "*.md" | Select-Object -First 3 FullName
```

- [ ] **Step 2: Run INSERT test**

Invoke `/update-workflow` with:
- note_query: (one of the found notes)
- user_content: "## Test Section\n\nThis is a test paragraph inserted by the workflow."
- target_section: "追加到末尾"

Verify:
- Note is located correctly
- INSERT intent detected
- Content appended with correct formatting
- frontmatter `updated` is set to today
- Heading levels are consistent
- User sees diff summary

- [ ] **Step 3: Verify test note is correct**

Read the modified note and confirm:
- New section exists at the end
- Heading level matches note structure
- No existing content was modified

- [ ] **Step 4: Revert test changes**

```powershell
git checkout -- <test-note-path>
```

---

### Task 4: Test REFRESH mode with direct replacement

**Prerequisite:** Task 3 complete

- [ ] **Step 1: Run REFRESH (direct) test**

Invoke `/update-workflow` with:
- note_query: (same test note)
- target_section: (an existing section name)
- user_content: "Replacement content for testing."

When asked "直接替换还是重新搜集？" → choose "直接替换"

Verify:
- REFRESH intent detected
- Direct replacement chosen
- Section content replaced
- Surrounding content untouched
- frontmatter `updated` is set

- [ ] **Step 2: Revert test changes**

```powershell
git checkout -- <test-note-path>
```

---

### Task 5: Test REFRESH mode with mini research cycle

**Prerequisite:** Task 4 complete

- [ ] **Step 1: Run REFRESH (research) test**

Invoke `/update-workflow` with:
- note_query: (same test note)
- target_section: (an existing section name)

When asked "直接替换还是重新搜集？" → choose "重新搜集"

Verify:
- mini TODO.md created
- collect runs with parent topic context
- curate scores and categorizes sources
- write produces section-only content (no frontmatter)
- Content inserted into parent note
- mini TODO.md cleaned up

- [ ] **Step 2: Revert test changes**

```powershell
git checkout -- <test-note-path>
rm -rf {SYSTEM_ROOT}/0-inbox/{subtopic} {SYSTEM_ROOT}/1-curated/{subtopic} {SYSTEM_ROOT}/2-drafts/{subtopic}
```

---

### Task 6: Test light verification

**Prerequisite:** Task 5 complete

- [ ] **Step 1: Test heading level detection**

Create a test note with a heading jump (e.g., `##` directly to `####`):
```markdown
---
type: concept
created: 2026-06-01
updated: 2026-06-01
---

# Test Note

## Section A

#### Subsection (skips ###)
```

Run `/update-workflow` with a small INSERT. Verify the verification step reports the heading skip.

- [ ] **Step 2: Test wikilink integrity**

Create a test note with a broken wikilink:
```markdown
---
type: concept
created: 2026-06-01
updated: 2026-06-01
---

# Test Note

See [[nonexistent-note]] for more info.
```

Run `/update-workflow` with a small INSERT. Verify the verification step reports the broken link.

- [ ] **Step 3: Clean up test notes**

```powershell
Remove-Item <test-note-path>
```

---

### Task 7: Final commit

- [ ] **Step 1: Review all changes**

```powershell
git status
git diff --stat
```

- [ ] **Step 2: Final commit (if not already committed)**

```powershell
git add -A
git commit -m "feat: complete update-note-workflow change"
```
