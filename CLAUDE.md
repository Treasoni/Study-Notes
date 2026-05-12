		# CLAUDE.md

This repository contains the **Study System** — a semi-automated technical learning note system built with Claude Code + Obsidian.

## How It Works

1. User says "I want to learn X" or "I want to write about my experience with X" — use [Resource Discovery](#resource-discovery规则寻址) glob patterns to locate the right skill/agent
2. For research-driven notes: Main Claude orchestrates 6 phases: collect → curate → write → beautify → evaluate → [digest]
3. For experience notes (心得笔记): user provides content → review → optional research → write → beautify → evaluate → [digest]
4. Each phase reads/writes files under `{VAULT_PATH}/StudySystem/`
5. User reviews and approves at each phase boundary

## Phase Boundary Rules (CRITICAL)

After completing ANY phase, you MUST STOP. DO NOT invoke the next phase's skill.
Present results to the user and WAIT for explicit confirmation (e.g. "继续", "proceed", "进入下一阶段").

NEVER chain phases together. NEVER skip a phase. NEVER assume user approval.

## Resource Discovery（规则寻址）

Claude 使用 glob 模式发现项目资源，无需硬编码路径。新增资源时放入对应目录并写好 frontmatter `description`，Claude 自动可发现。

### Skills

- 发现: `Glob .claude/skills/*/SKILL.md`
- 匹配: 读每个 skill 的 YAML frontmatter `description` 字段，匹配用户意图
- 调用: `Skill(skill="{name}")` — skill 名称取目录名

### Agents

- 发现: `Glob .claude/agents/*.md`
- 匹配: 读每个 agent 的 YAML frontmatter `name`、`description`、`tools` 字段
- 调用: `Agent(subagent_type="{name}")` — agent 名称取 frontmatter `name`

### Templates

- 发现: `Glob templates/*.md`
- 匹配: 读 frontmatter `type` 字段（concept / practice / compare / cheat-sheet / experience）
- 使用: Read 后按模板结构填充内容

### Learnings

- 发现: `Glob .learnings/RULES.md`
- 使用: 每次新任务前 Read，内化 Do / Don't / Watch For

### 配置

- 发现: `Glob .obsidian-config.md`
- 使用: Read 获取 Obsidian vault 路径

## Configuration

Vault path is set in `.obsidian-config.md`. On first run, Pre-Task Initialization
detects an empty VAULT_PATH and prompts you to set it.

## Orchestration Flow

## Pre-Task Initialization

Before starting any new Study System task (Phase 0), resolve the vault path
and internalize past learnings.

### Vault Path Validation (Critical Gate)

1. Read `.obsidian-config.md`
2. Check the `VAULT_PATH:` value:
   - **Empty**: this is the first run. Proactively ask the user:
     - "This appears to be your first time using the Study System. I need your Obsidian vault path to proceed."
     - "Please provide the absolute path to your Obsidian vault (e.g., `/Users/name/obsidian` or `C:/Users/name/obsidian`)."
     - After user provides a path, write it to `.obsidian-config.md`:
       ```
       VAULT_PATH: "/the/path"
       ```
     - Re-read `.obsidian-config.md` to confirm
     - If still empty, STOP — do not proceed without a valid path
   - **Non-empty**: validate the directory exists:
     - `ls "{VAULT_PATH}"` — if missing, warn the user and ask for correction
3. Resolve `SYSTEM_ROOT` and `OUTPUT_PATH` from the config values. All subsequent
   path references must use the resolved values.

### Internalize Past Learnings

1. Read `.learnings/RULES.md` — compact, actionable rules from past sessions
2. Note what to do, what to avoid, what patterns to watch for

If `.learnings/RULES.md` doesn't exist yet, skip this step.

### Phase 0: Requirement Clarification + Path Confirmation

When user expresses intent to learn something, ask in two rounds:

**Round 1: Learning goals**
Ask the user:
1. "Which direction?"
   - a) 概念理解 (Understand concepts and principles)
   - b) 实战上手 (Hands-on practice)
   - c) 体系梳理 (Build complete knowledge system)
   - d) 问题排查 (Solve a specific problem)
2. "What depth?" → 入门 / 进阶 / 深入源码
3. "What note type?" → 概念笔记 / 实战笔记 / 对比笔记 / 速查表 / 心得笔记

**Round 2: Path configuration**
Ask the user:
1. "Where to save the final note?"
   - Default: `{SYSTEM_ROOT}/3-published/{topic}/`
   - Can specify any path within the vault, e.g. `Notes/前端/React/`
2. "Topic name for folder?" (default: sanitized topic name)

**After user answers → Generate and present execution plan:**

For research-driven notes (概念/实战/对比/速查):
```
## Execution Plan
- Topic: {topic}
- Direction: {direction}
- Depth: {depth}
- Note type: {note_type}
- Output path: {output_path}
- Phases: collect → curate → write → beautify → [evaluate] → [digest]

Proceed?
```

For experience notes (心得笔记):
```
## Execution Plan
- Topic: {topic}
- Note type: 心得笔记
- Output path: {output_path}
- Phases: user input → review → [optional research] → write → beautify → [evaluate] → [digest]

Proceed?
```

Write plan to `{SYSTEM_ROOT}/4-meta/execution-log.md`:
```markdown
## [{date}] {topic}
- Direction: {direction}
- Depth: {depth}
- Note type: {note_type}
- Output path: {output_path}
- Status: started
```

### Phase 1: Collect (资料收集)

1. Invoke `/collect` — it will search for official docs and community content, fetch and save raw materials to `0-inbox/{topic}/`
2. Present summary to user:
   - How many sources collected
   - Which sub-topics are covered
   - Any obvious gaps
3. **STOP here. DO NOT invoke `/curate`.** Wait for user to explicitly say "继续" or "进入下一阶段".

### Phase 2: Curate (资料整理)

1. Invoke `/curate` — it will score, deduplicate, and categorize all sources, write curated files to `1-curated/{topic}/`
2. Present summary to user:
   - Knowledge map overview
   - Which sources were discarded and why
   - Which sub-topics lack sufficient material
3. **STOP here. DO NOT invoke `/write`.** Wait for user to explicitly confirm.

### Phase 3: Write (生成笔记)

1. Confirm note type preference (skip if already set in Phase 0)
2. Invoke `/write` — it will select template from `templates/`, extract info from curated materials, write draft to `2-drafts/{topic}/`
3. Present draft to user:
   - Structure review
   - Accuracy check
   - Any missing content
4. **STOP here. DO NOT invoke `/beautify`.** Wait for user to explicitly confirm.

### Phase 4: Beautify (美化排版)

1. Invoke `/beautify` — it will apply Obsidian Markdown formatting, add wikilinks, tags, callouts, Mermaid diagrams, write final note to the user-specified output path
2. **STOP. DO NOT invoke `/evaluate`. DO NOT proceed to Phase 5.** Present final result and ask: "Any changes needed?" Wait for user to explicitly confirm before proceeding.
3. User reviews and may request modifications
4. When user gives feedback: **implement minimal, targeted fixes only** — do NOT regenerate the entire note. Fix just what was flagged, keeping other content untouched
5. Repeat 2-4 until user approves
6. User: confirm → proceed to Phase 5 (if desired)

### Phase 5 (Optional): Evaluate (质量评估)

1. DO NOT auto-evaluate. Ask the user: "Evaluate this note's quality?" Only invoke evaluate skill if user explicitly says yes.
2. If yes, invoke the `evaluate` skill — it will:
   - Score on 5 dimensions (completeness, accuracy, readability, practicality, connectivity)
   - Cross-validate claims against curated source materials
   - Write evaluation report to `4-meta/evaluation/{topic}-eval.md`
3. Present evaluation results and improvement suggestions

### Phase 6 (Optional): Digest (自我学习)

1. DO NOT auto-digest. Ask the user: "Capture session learnings for continuous improvement?" Only invoke digest skill if user explicitly says yes.
2. If yes, invoke the `digest` skill — it will:
   - Review the session for learnings and errors
   - Log entries to `.learnings/LEARNINGS.md` and `.learnings/ERRORS.md`
   - Run digest compression if thresholds exceeded
3. Present captured learnings summary

## Experience Notes (心得笔记)

When the user selects "心得笔记" in Phase 0, the workflow is **user-input-first** instead of research-first. The content comes from the user's own project experiences and insights, not external research.

### Workflow

**Step 1: User provides content**
Ask the user to share their experience — free-form text, bullet points, or a rough draft. Save raw input to `0-inbox/{topic}/raw-input.md`.

**Step 2: Review for accuracy**
Review the user's content with these rules:

| DO | DO NOT |
|----|--------|
| Flag factual/technical errors, suggest corrections | Rewrite the user's content |
| Identify claims that need verification | Change overall structure |
| Suggest where external research could fill gaps | Alter the user's voice or style |
| Mark uncertain claims with `[待验证]` | Add information the user didn't provide |

Present review findings to the user as a checklist:
- Items flagged as potentially incorrect
- Claims marked `[待验证]`
- Suggested research topics (if any)

**Step 3: User decides on research**
For each flagged item, ask the user:
- "This needs verification" → run mini collect→curate for that specific point
- "This is fine as-is" → keep original wording
- "Add more about X" → optional mini research for expansion

When mini research is needed, use the same targeted approach as the Update skill's REFRESH mode: isolate to `0-inbox/{topic}/{subtopic}/` and `1-curated/{topic}/{subtopic}/`.

**Step 4: Write draft**
Invoke `/write` with note type `experience`. The write skill uses `experience-template.md` and marks sources as `[来源: 个人经验]`. Draft goes to `2-drafts/{topic}/`.

**Step 5: Beautify**
Same as Phase 4 — apply Obsidian formatting, write to user-specified output path. User reviews and approves.

**Step 6: Optional evaluate**
Same as Phase 5 — score quality, cross-validate.

**Step 7: Optional digest**
Same as Phase 6 — log session learnings.

### When the User is Unsure About Research

If the user says "I don't know if I need to research this", review their content and give a clear recommendation:
- "Claim X about Y — I'm not confident this is correct. Recommend verifying."
- "Section Z is experience-based and doesn't need external verification."
- "This part would benefit from an official doc reference. Want me to find one?"

## Updating Existing Notes

When the user wants to add content to or refresh an existing published note, invoke `/update` — do NOT re-run the full creation pipeline.

### Two Modes

**INSERT** — User provides new content directly:
```
User: "add this paragraph about useEffect cleanup to my React hooks note"
→ Invoke /update — it will locate the note, insert at the right spot,
  match surrounding formatting, and update the frontmatter updated field.
```

**REFRESH** — Content is outdated, may need fresh research:
```
User: "the React hooks section is outdated, update it with current patterns"
→ Invoke /update — it will ask: replace in-place or re-research first?
  - Replace in-place: user provides new content → INSERT mode
  - Re-research: runs focused collect→curate→write for just that section
```

### Key Rules for Updates

- **Minimal diff**: Only modify the target section, do not re-beautify the whole note
- **Match existing style**: New content uses the same callout types, table conventions, code block languages
- **Preserve wikilinks**: Do not touch or break existing `[[links]]`
- **Update frontmatter**: Set `updated: YYYY-MM-DD` to current date

## Error Handling (Phase 1-4)

During Phase 1-4 execution, if any error occurs or you manually intervene to correct the model's output, **record only, do not analyze**. Append a plain-text entry to `{SYSTEM_ROOT}/4-meta/error-log.md`:

```
[YYYY-MM-DD HH:MM] {phase} - {brief description of what went wrong}
{correction taken, if any}
```

Rules:
- Plain text only — no markdown headers, no bold, no analysis
- One entry per incident, separated by blank line
- Just state what happened and what was done — no root cause analysis, no impact assessment
- After recording, ask user how to proceed (retry / skip / abort / manual fix)

## Learnings Digest

To prevent `.learnings/` files from growing unbounded, the digest skill runs a digest cycle when thresholds are exceeded.

### Thresholds

| File | Threshold | Action |
|------|-----------|--------|
| `.learnings/LEARNINGS.md` | > 100 lines | Compress before logging new entries |
| `.learnings/ERRORS.md` | > 100 lines | Compress before logging new entries |
| `.learnings/RULES.md` | > 50 lines | Review and promote to CLAUDE.md, trim RULES.md |

### Digest Process

When triggered manually:

1. Read all entries in `.learnings/LEARNINGS.md` and `.learnings/ERRORS.md`
2. Group similar entries, deduplicate, extract patterns
3. Write compact rules to `.learnings/RULES.md`:
   - One rule per line under `## Do` / `## Don't` / `## Watch For`
   - Merge recurring entries with a counter: `(3x) Use X not Y`
   - Drop one-off noise that never recurred
4. Promote critical rules to CLAUDE.md if they affect the core orchestration flow
5. Archive old entries to `.learnings/archive/YYYY-MM-DD.md`
6. Truncate `.learnings/LEARNINGS.md` and `.learnings/ERRORS.md` — keep headers only

### RULES.md Format

```markdown
# Rules
Compressed, deduplicated learnings from past sessions.

## Do
- Prefer X over Y for Z scenarios (2x)
- Always check A before B (3x)

## Don't
- Never skip cross-validation (2x)

## Watch For
- opencli adapters can return empty results for Chinese queries
```

## Quality Gates

Between each phase, check:
- Previous phase output files exist and are non-empty
- Output content is consistent with input
- If checks fail → log to error-log.md → ask user how to proceed

## Directory Convention

```
{VAULT_PATH}/StudySystem/
├── templates/       # Note templates
├── 0-inbox/         # Phase 1: raw collected materials
├── 1-curated/       # Phase 2: organized and scored materials
├── 2-drafts/        # Phase 3: draft notes
├── 3-published/     # Phase 4: final beautified notes (default output)
└── 4-meta/          # Logs, errors, evaluations
```

## Key Principles

1. All system files live under `StudySystem/` — don't pollute the vault root
2. Output path is set by user in Phase 0 — never hardcoded
3. Each skill only handles its own phase — no crossing boundaries
4. Data passes through files, not memory — each phase's output is the next phase's input
5. User reviews after every phase — no full automation
6. Prefer official docs and primary sources
7. Every claim must be traceable to its source
