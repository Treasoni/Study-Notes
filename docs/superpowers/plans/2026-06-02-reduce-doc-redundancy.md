---
archived-with: 2026-06-02-reduce-doc-redundancy-and-skill-bloat
status: final
---
# Reduce Doc Redundancy and Skill Bloat Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate ~10,000 tokens of documentation redundancy and implement skill mode filtering to reduce ~300KB of unused skill context per session.

**Architecture:** Extract TODO.md state machine into a single authoritative reference doc, consolidate duplicate scoring rubrics, merge overlapping update-workflow docs, and add a `skills.mode` config to filter project vs dev skills.

**Tech Stack:** Markdown documentation, YAML configuration, no code changes.

---

## File Structure

| Action | File | Purpose |
|--------|------|---------|
| Create | `docs/todo-state-machine.md` | Single authoritative TODO.md state machine definition |
| Modify | `CLAUDE.md` | Replace TODO.md rules with reference |
| Modify | `docs/phases.md` | Replace Phase Gate instructions with reference |
| Modify | `docs/experience-notes.md` | Replace Phase Gate instructions with reference |
| Modify | `docs/updating-notes.md` | Replace REFRESH mini TODO instructions with reference |
| Modify | `.claude/skills/update-workflow/SKILL.md` | Slim down to routing logic only |
| Modify | `.claude/skills/collect/SKILL.md` | Replace scoring rubric with reference |
| Modify | `.claude/agents/collector.md` | Add source annotation comment |
| Modify | `.claude/agents/writer.md` | Add source annotation comment |
| Modify | `.claude/agents/curator.md` | Add source annotation comment |
| Modify | `.claude/agents/beautifier.md` | Add source annotation comment |
| Modify | `.study-config.yaml` | Add `skills.mode` config |

---

### Task 1: Create docs/todo-state-machine.md

**Files:**
- Create: `docs/todo-state-machine.md`

- [ ] **Step 1: Create the authoritative TODO.md state machine reference**

```markdown
# TODO.md State Machine

> **Single authoritative reference** for TODO.md lifecycle rules. All other files should reference this document instead of duplicating these rules.

## Referenced By

- `CLAUDE.md` — Critical Rules section
- `docs/phases.md` — Phase Gate instructions
- `docs/experience-notes.md` — Step Gate instructions
- `docs/updating-notes.md` — REFRESH mini TODO instructions
- `.claude/skills/collect/SKILL.md` — TODO.md path reference
- `.claude/skills/write/SKILL.md` — TODO.md path reference
- `.claude/skills/beautify/SKILL.md` — TODO.md path reference

## State Definitions

| State | Condition | Description |
|-------|-----------|-------------|
| **No TODO** | `{SYSTEM_ROOT}/TODO.md` does not exist | Default state; ready for new workflow |
| **Active** | `{SYSTEM_ROOT}/TODO.md` exists with `[ ]` items | Workflow in progress |
| **Complete** | All items marked `[x]` | Workflow done, pending cleanup |
| **Terminated** | User decides to stop early | Must clean up TODO.md |

## Tool Mapping

| Action | Tool | Command |
|--------|------|---------|
| **Read/Check** | Read | `Read("{SYSTEM_ROOT}/TODO.md")` |
| **Create** | Write | `Write("{SYSTEM_ROOT}/TODO.md", content)` |
| **Mark Complete** | Write | Rewrite file with `[x]` for completed phase |
| **Delete** | Bash | `rm "{SYSTEM_ROOT}/TODO.md"` |

**CRITICAL**: Use explicit tool names — NEVER natural-language verbs like "check" or "mark".

## Phase Gate Rule

Before ANY phase/step, MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

## Workflow Variants

### A. Full Workflow (5 phases)

Created after user confirms execution plan:

```markdown
# TODO - {topic}
- [ ] Phase 1: collect - 资料收集与整理
- [ ] Phase 2: write - 生成笔记
- [ ] Phase 3: beautify - 美化排版
- [ ] Phase 4: evaluate - 质量评估
- [ ] Phase 5: digest - 自我学习
```

- Phase 0 (requirement discovery) has no checkbox — it precedes TODO.md creation
- Phases 4-5 are optional — if user declines, skip to deletion

### B. Experience Notes (7 steps)

Created after execution plan confirmed:

```markdown
# TODO - {topic}
- [ ] Step 1: user input (done)
- [ ] Step 2: review - 内容审核
- [ ] Step 3: research - 可选研究
- [ ] Step 4: write - 生成笔记
- [ ] Step 5: beautify - 美化排版
- [ ] Step 6: evaluate - 质量评估
- [ ] Step 7: digest - 自我学习
```

- Step 1 is marked `[x]` immediately after creation

### C. REFRESH Mini Loop

Created during REFRESH mode re-research:

```markdown
# TODO - REFRESH: {subtopic}
- [ ] mini-collect - 定向资料收集
- [ ] mini-curate - 定向资料整理
- [ ] mini-write - 定向更新笔记
```

- Uses isolated directories: `0-inbox/{subtopic}/`, `1-curated/{subtopic}/`, `2-drafts/{subtopic}/`

## Early Termination

If user decides to stop at any point, MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"` after confirming "task complete". The TODO.md must not be left behind.

## Resume Check

When starting ANY new session, before entering any phase:
1. MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`
2. If it exists → read `[x]` states → ask user: "Resume from Phase [N]?"
3. If user says yes → jump to that phase (still enforce Phase Gate for that phase)
4. If user says no → ask whether to archive or delete TODO.md and start fresh
5. If TODO.md does NOT exist → proceed normally
```

- [ ] **Step 2: Verify file exists and is non-empty**

Run: `cat docs/todo-state-machine.md | wc -l`
Expected: > 50 lines

- [ ] **Step 3: Commit**

```bash
git add docs/todo-state-machine.md
git commit -m "docs: create single authoritative TODO.md state machine reference"
```

---

### Task 2: Simplify CLAUDE.md TODO.md Rules

**Files:**
- Modify: `CLAUDE.md:21-31`

- [ ] **Step 1: Replace TODO.md State Machine section with reference**

In CLAUDE.md, replace the entire "### TODO.md State Machine (CRITICAL)" section (lines 21-31) with:

```markdown
### TODO.md State Machine (CRITICAL)

See [docs/todo-state-machine.md](docs/todo-state-machine.md) for complete rules. Key invariants:
- Use explicit tool names (Read/Write/Bash) — NEVER natural-language verbs
- Phase Gate: Read TODO.md before every phase, verify prior `[x]`
- Delete TODO.md via Bash when workflow completes
```

- [ ] **Step 2: Verify CLAUDE.md line count**

Run: `wc -l CLAUDE.md`
Expected: ≤ 160 lines (currently ~147, reduction of ~5 lines)

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: replace CLAUDE.md TODO.md rules with reference to todo-state-machine.md"
```

---

### Task 3: Simplify phases.md Phase Gate Instructions

**Files:**
- Modify: `docs/phases.md:127,139,152,168,180`

- [ ] **Step 1: Replace Phase 1 Gate instruction**

In phases.md, replace line 127:

OLD:
```
**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]` (Phase 0 has no checkbox).
```

NEW:
```
**Phase Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule. (Phase 0 has no checkbox.)
```

- [ ] **Step 2: Replace Phase 2 Gate instruction**

Replace line 139 with:
```
**Phase Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.
```

- [ ] **Step 3: Replace Phase 3 Gate instruction**

Replace line 152 with:
```
**Phase Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.
```

- [ ] **Step 4: Replace Phase 4 Gate instruction**

Replace line 168 with:
```
**Phase Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.
```

- [ ] **Step 5: Replace Phase 5 Gate instruction**

Replace line 180 with:
```
**Phase Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.
```

- [ ] **Step 6: Replace rm TODO.md instructions**

Replace the three `rm "{SYSTEM_ROOT}/TODO.md"` references (lines 160, 164, 188) with references to the todo-state-machine.md "Early Termination" section.

- [ ] **Step 7: Commit**

```bash
git add docs/phases.md
git commit -m "docs: replace phases.md Phase Gate instructions with references to todo-state-machine.md"
```

---

### Task 4: Simplify experience-notes.md

**Files:**
- Modify: `docs/experience-notes.md:33,53,66,74,82,86,89,94,98`

- [ ] **Step 1: Replace Step 2 Gate instruction**

In experience-notes.md, replace line 33:

OLD:
```
**Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify Step 1 is `[x]`.
```

NEW:
```
**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.
```

- [ ] **Step 2: Replace Steps 3-7 Gate instructions**

Replace lines 53, 66, 74, 82, 86, 89 with the same reference pattern.

- [ ] **Step 3: Replace rm TODO.md instructions**

Replace lines 94 and 98 with references to todo-state-machine.md.

- [ ] **Step 4: Commit**

```bash
git add docs/experience-notes.md
git commit -m "docs: replace experience-notes.md gate instructions with references to todo-state-machine.md"
```

---

### Task 5: Simplify updating-notes.md REFRESH TODO Instructions

**Files:**
- Modify: `docs/updating-notes.md:61-72`

- [ ] **Step 1: Replace REFRESH mini TODO section**

In updating-notes.md, replace lines 61-72 (the inline TODO.md format and gate instructions) with:

```markdown
When re-research is chosen, the `/update` skill creates a mini TODO.md following the [todo-state-machine.md](todo-state-machine.md) REFRESH Mini Loop workflow variant.
```

- [ ] **Step 2: Commit**

```bash
git add docs/updating-notes.md
git commit -m "docs: replace updating-notes.md REFRESH TODO instructions with reference"
```

---

### Task 6: Merge update-workflow/SKILL.md

**Files:**
- Modify: `.claude/skills/update-workflow/SKILL.md`

- [ ] **Step 1: Read current SKILL.md and identify unique content**

Read `.claude/skills/update-workflow/SKILL.md` fully. Compare with `docs/updating-notes.md`.

Unique content in SKILL.md (not in updating-notes.md):
- Input parameters table (lines 15-21)
- Execution model diagram (lines 27-39)
- Backup step details (lines 97-101)
- Skill dispatch format (lines 106-122)
- Error handling details (lines 140-153)

- [ ] **Step 2: Rewrite SKILL.md as routing layer**

```markdown
---
name: update-workflow
description: 笔记更新编排层。定位目标笔记、解析结构、自动检测 INSERT/REFRESH 意图，调度 /update skill 执行更新。
---

# Skill: update-workflow（笔记更新编排）

> 完整工作流规范见 `docs/updating-notes.md`

## 触发时机

用户要求修改、添加或更新已有笔记内容时。

## 执行模型

本 skill 采用 **Operator Pattern**：主 Agent 作为编排调度员，`/update` skill 作为执行者。

1. **定位笔记** → 多级搜索（精确路径 → OUTPUT_PATH → 3-published/ → vault 根目录）
2. **检测意图** → INSERT（用户提供内容）或 REFRESH（内容过时）
3. **备份 + 调度 /update** → 传递结构解析结果和意图检测结果
4. **轻量验证** → 标题层级、wikilink 完整性、frontmatter
5. **展示 diff + 硬停止** → 等待用户确认

> 详见 `docs/updating-notes.md` Step 1-5 完整规范

## 输入参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `note_query` | 笔记名称或完整路径 | ✅ |
| `user_content` | 用户提供的新内容（INSERT 模式） | INSERT 时必填 |
| `target_section` | 要刷新的章节名（REFRESH 模式） | REFRESH 时必填 |
| `update_mode` | 显式指定 INSERT/REFRESH（省略时自动检测） | ❌ |

## 禁止行为

- 不要跳过多级搜索，直接假设笔记不存在
- 不要跳过意图检测，直接执行更新
- 不要在 INSERT 模式下添加用户未提供的信息
- 不要修改不相关章节的内容
- 不要跳过验证步骤直接展示结果
- 不要跳过用户确认直接写入文件
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/update-workflow/SKILL.md
git commit -m "docs: slim update-workflow/SKILL.md to routing logic, reference updating-notes.md"
```

---

### Task 7: Scoring Rubric Single Source

**Files:**
- Modify: `.claude/skills/collect/SKILL.md:166-175`

- [ ] **Step 1: Replace inline rubric in collect/SKILL.md**

In collect/SKILL.md, replace the scoring rubric table (lines 166-175) with:

```markdown
#### 4b. 评分（内联 curate 逻辑）

对每个收集到的文件进行四维度评分。评分标准见 `.claude/agents/collector.md` Step 2。

**综合得分** = 四个维度的平均值（四舍五入到一位小数）。
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/collect/SKILL.md
git commit -m "docs: replace collect/SKILL.md scoring rubric with reference to collector.md"
```

---

### Task 8: Skill Mode Filtering

**Files:**
- Modify: `.study-config.yaml`
- Modify: `CLAUDE.md` (Resource Discovery section)

- [ ] **Step 1: Add skills.mode to .study-config.yaml**

Append to `.study-config.yaml`:

```yaml

skills:
  mode: project  # "project" | "dev" | "all" (default: project)
```

- [ ] **Step 2: Add filtering step to CLAUDE.md Resource Discovery**

In CLAUDE.md, after the Resource Discovery section (after line 67), add:

```markdown

> **Skill Filtering**: After Glob results, filter by `skills.mode` in `.study-config.yaml`:
> - `project` → only study-system runtime skills (collect, curate, write, beautify, evaluate, digest, update, update-workflow, requirement-discovery, moc, generate-links, fix-broken-links, delete-file, obsidian-cli, obsidian-markdown)
> - `dev` → only development skills (comet-*, opencli-*, brainstorming, openspec-*, writing-plans, executing-plans, subagent-driven-development, test-driven-development, systematic-debugging, using-git-worktrees, finishing-a-development-branch, dispatching-parallel-agents, using-superpowers, requesting-code-review, receiving-code-review, verification-before-completion, sortspec-generator, tool-registry, smart-search, defuddle, json-canvas, writing-skills)
> - `all` → no filtering (current behavior)
```

- [ ] **Step 3: Verify CLAUDE.md line count**

Run: `wc -l CLAUDE.md`
Expected: ≤ 160 lines

- [ ] **Step 4: Commit**

```bash
git add .study-config.yaml CLAUDE.md
git commit -m "feat: add skills.mode config for project/dev/all skill filtering"
```

---

### Task 9: Agent Exemption Block Annotations

**Files:**
- Modify: `.claude/agents/collector.md:12-18`
- Modify: `.claude/agents/writer.md:12-18`
- Modify: `.claude/agents/curator.md:12-18`
- Modify: `.claude/agents/beautifier.md:12-18`

- [ ] **Step 1: Add source annotation to collector.md**

In collector.md, replace the 全局指令豁免 block (lines 12-18) with:

```markdown
## 全局指令豁免

> **Source**: This exemption block is shared across all 4 agent definitions (collector, writer, curator, beautifier). Update all files when changing.

你是 subagent，以下 CLAUDE.md 指令**不适用于你**，忽略它们：
- Resource Discovery（Glob skills/agents/templates）
- Pre-Task Initialization（Read TODO.md、.obsidian-config.md 等）
- Mandatory Triggered Reads 表格

只执行主 Agent 传给你的任务。你已拥有完成任务所需的全部输入路径。
```

- [ ] **Step 2: Add same annotation to writer.md, curator.md, beautifier.md**

Apply the same pattern to the other 3 agent files.

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/collector.md .claude/agents/writer.md .claude/agents/curator.md .claude/agents/beautifier.md
git commit -m "docs: add shared source annotation to agent exemption blocks"
```

---

### Task 10: Final Verification

**Files:**
- Verify: `docs/todo-state-machine.md`
- Verify: `CLAUDE.md`
- Verify: `.study-config.yaml`

- [ ] **Step 1: Verify all reference paths are valid**

Check that every file listed in "Referenced By" in todo-state-machine.md actually exists and contains the expected reference.

- [ ] **Step 2: Verify CLAUDE.md line count**

Run: `wc -l CLAUDE.md`
Expected: ≤ 160 lines

- [ ] **Step 3: Verify .study-config.yaml syntax**

Check that the new `skills.mode` field is valid YAML.

- [ ] **Step 4: Verify no orphaned references**

Search for any remaining inline TODO.md rules that should have been replaced:
```
grep -rn "MUST execute Read tool on.*TODO.md" docs/ CLAUDE.md
```
Expected: Only references in todo-state-machine.md itself.

- [ ] **Step 5: Final commit (if any fixes needed)**

```bash
git add -A
git commit -m "docs: final verification fixes for doc deduplication"
```
