# Phases

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

## Resume Check (NEW SESSION)

When starting ANY new session, before entering any phase:

1. MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`
2. If it exists → read `[x]` states → ask user: "Detected unfinished workflow ({topic}). Resume from Phase [N]?"
3. If user says yes → jump to that phase (still enforce Check/Mark for that phase)
4. If user says no → ask whether to archive or delete TODO.md and start fresh
5. If TODO.md does NOT exist → proceed to Phase 0 normally

## Orchestration Flow

### Phase 0: Requirement Discovery (需求发现)

When user expresses intent to learn something ("I want to learn X"), enter requirement discovery.

**If `.study-config.yaml` has `requirement_discovery.enabled: false` → skip to Step 5 (Path Configuration) with defaults.**

#### Step 1: Assess Topic Complexity

Based on topic length and keywords, determine question count:
- Simple (1-2 words) → 4 questions
- Medium (3-4 words) → 5 questions
- Complex (phrase/sentence) → 6 questions

#### Step 2: Structured Questions (4-6)

Ask all questions in a single prompt. Each question has 2-4 preset options + "Other":

1. **Learning purpose** → influences note type
   - 考试准备 (Exam preparation)
   - 工作需要 (Work requirement)
   - 兴趣探索 (Interest exploration)

2. **Target audience** → influences depth and style
   - 自己 (Personal learning)
   - 团队 (Team sharing)
   - 社区 (Public publishing)

3. **Depth requirement**
   - 入门 (Beginner: basic concepts + simple examples)
   - 进阶 (Advanced: principles + best practices)
   - 专家 (Expert: deep mechanics + edge cases)

4. **Note usage**
   - 快速回顾 (Quick review → cheat sheet)
   - 深度学习 (Deep learning → concept + practice)
   - 分享传播 (Sharing → complete + diagrams)

5. *(optional, for complex topics)* **Specific focus areas** (open-ended)
   > "Which aspect do you most want to understand deeply?"

6. *(optional)* **Current knowledge level**
   - 完全新手 (Complete beginner)
   - 有一些基础 (Some foundation)
   - 已有经验，想深入 (Experienced, want depth)

#### Step 3: Recommend Note Type

Based on answers, recommend hybrid note type combination:
- Exam → concept + cheat_sheet
- Work → practice + compare
- Interest → concept (or experience + concept)
- Sharing → add practice to primary type

Present recommendation with rationale. User can accept or override.

#### Step 4: Generate Execution Plan

Present customized plan:

```
## Execution Plan
- Topic: {topic}
- Recommended type: {primary} + {secondary}
- Autonomy level: {level from .study-config.yaml}
- Output path: {output_path}
- Phases: collect → curate → write → beautify → [evaluate] → [digest]

Proceed?
```

For experience notes, adjust phases to match the 7-step workflow.

**Skip option**: User can say "skip" or "use defaults" to bypass discovery. Defaults: concept type, autonomy level 1, intermediate depth, default output path.

#### Step 5: Path Configuration

Ask the user:
1. "Where to save the final note?"
   - Default: `{SYSTEM_ROOT}/3-published/{topic}/`
   - Can specify any path within the vault, e.g. `Notes/前端/React/`
2. "Topic name for folder?" (default: sanitized topic name)

#### Step 6: Finalize

Write plan to `{SYSTEM_ROOT}/4-meta/execution-log.md`:
```markdown
## [{date}] {topic}
- Purpose: {purpose}
- Audience: {audience}
- Depth: {depth}
- Note type: {note_type}
- Output path: {output_path}
- Status: started
```

After user confirms → MUST execute Write tool to create `{SYSTEM_ROOT}/TODO.md` with all planned phases as `- [ ]` checkboxes:

```markdown
# TODO - {topic}
- [ ] Phase 1: collect - 资料收集
- [ ] Phase 2: curate - 资料整理
- [ ] Phase 3: write - 生成笔记
- [ ] Phase 4: beautify - 美化排版
- [ ] Phase 5: evaluate - 质量评估
- [ ] Phase 6: digest - 自我学习
```

For experience notes, adjust phases to match the 7-step workflow.

### Phase 1: Collect (资料收集)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]` (Phase 0 has no checkbox).

1. Invoke `/collect` — it dispatches a collector subagent to search for official docs and community content, fetch and save raw materials to `0-inbox/{topic}/`（主 Agent 不直接搜索，避免上下文污染）
2. Present summary to user:
   - How many sources collected
   - Which sub-topics are covered
   - Any obvious gaps
3. MUST execute Write tool to mark Phase 1 `[x]` in `{SYSTEM_ROOT}/TODO.md`.
4. **STOP here. DO NOT invoke `/curate`.** Wait for user to explicitly say "继续" or "进入下一阶段".

### Phase 2: Curate (资料整理)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

1. Invoke `/curate` — it dispatches a curator subagent to score, deduplicate, and categorize all sources, write curated files to `1-curated/{topic}/`（主 Agent 不直接读取 raw 文件，避免上下文污染）
2. Present summary to user:
   - Knowledge map overview
   - Which sources were discarded and why
   - Which sub-topics lack sufficient material
3. MUST execute Write tool to mark Phase 2 `[x]` in `{SYSTEM_ROOT}/TODO.md`.
4. **STOP here. DO NOT invoke `/write`.** Wait for user to explicitly confirm.

### Phase 3: Write (生成笔记)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

1. Confirm note type preference (skip if already set in Phase 0)
2. Invoke `/write` — it dispatches a writer subagent to select template, extract info from curated materials, write draft to `2-drafts/{topic}/`（主 Agent 不直接读取 curated 文件，避免上下文污染）
3. Present draft to user:
   - Structure review
   - Accuracy check
   - Any missing content
4. MUST execute Write tool to mark Phase 3 `[x]` in `{SYSTEM_ROOT}/TODO.md`.
5. **STOP here. DO NOT invoke `/beautify`.** Wait for user to explicitly confirm.

### Phase 4: Beautify (美化排版)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

1. Invoke `/beautify` — it dispatches a beautifier subagent to apply Obsidian Markdown formatting, add wikilinks, tags, callouts, Mermaid diagrams, write final note to the user-specified output path（主 Agent 不加载 Obsidian 语法规范，避免上下文污染）
2. **STOP. DO NOT invoke `/evaluate`. DO NOT proceed to Phase 5.** Present final result and ask: "Any changes needed?" Wait for user to explicitly confirm before proceeding.
3. User reviews and may request modifications
4. When user gives feedback: **implement minimal, targeted fixes only** — do NOT regenerate the entire note. Fix just what was flagged, keeping other content untouched
5. Repeat 2-4 until user approves
6. When user approves: MUST execute Write tool to mark Phase 4 `[x]` in `{SYSTEM_ROOT}/TODO.md`.
7. User: confirm → proceed to Phase 5 (if desired). If user says "done" (no more phases) → MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"`.

### Early Termination

If user decides to stop at any point (e.g., after Phase 4, skipping Phase 5-6), MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"` after confirming "task complete" with the user. The TODO.md must not be left behind.

### Phase 5 (Optional): Evaluate (质量评估)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

1. DO NOT auto-evaluate. Ask the user: "Evaluate this note's quality?" Only invoke evaluate skill if user explicitly says yes.
2. If yes, invoke the `evaluate` skill — it will:
   - Score on 5 dimensions (completeness, accuracy, readability, practicality, connectivity)
   - Cross-validate claims against curated source materials
   - Write evaluation report to `4-meta/evaluation/{topic}-eval.md`
3. Present evaluation results and improvement suggestions
4. MUST execute Write tool to mark Phase 5 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

### Phase 6 (Optional): Digest (自我学习)

**Phase Gate**: MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`. Verify all prior phases are `[x]`. If any prior phase is still `[ ]`, STOP — do not proceed.

1. DO NOT auto-digest. Ask the user: "Capture session learnings for continuous improvement?" Only invoke digest skill if user explicitly says yes.
2. If yes, invoke the `digest` skill — it will:
   - Review the session for learnings and errors
   - Log entries to `.learnings/LEARNINGS.md` and `.learnings/ERRORS.md`
   - Run digest compression if thresholds exceeded
3. Present captured learnings summary
4. All phases complete → MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"`.
