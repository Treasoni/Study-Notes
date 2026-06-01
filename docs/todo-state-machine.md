# TODO.md State Machine

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

Single authoritative reference for TODO.md lifecycle rules. All files listed in Referenced By must defer to this document for TODO.md behavior.

## Referenced By

| File | References |
|------|-----------|
| [CLAUDE.md](../CLAUDE.md) | Resume Check, Create, Check, Mark, Delete rules |
| [docs/phases.md](phases.md) | Phase 0-5 gate checks and TODO.md mutations |
| [docs/experience-notes.md](experience-notes.md) | Experience 7-step TODO.md mutations |
| [docs/updating-notes.md](updating-notes.md) | REFRESH mini loop TODO.md lifecycle |

## State Definitions

| State | Description | TODO.md Exists? | File Content |
|-------|-------------|-----------------|--------------|
| **No TODO** | No active workflow. Fresh session or after deletion. | No | N/A |
| **Active** | Workflow in progress. Phases/steps are partially `[x]`. | Yes | Checkboxes with at least one `[ ]` |
| **Complete** | All phases/steps are `[x]`. Ready for deletion. | Yes | All checkboxes are `[x]` |
| **Terminated** | User stopped early. TODO.md has been deleted. | No | N/A |

## Tool Mapping

Every TODO.md mutation uses an explicit tool name. Never use natural-language verbs ("check", "mark", "update") — always specify the tool.

| Operation | Tool | Action | When |
|-----------|------|--------|------|
| **Check existence** | `Read` | Read `{SYSTEM_ROOT}/TODO.md` | Session start, before every phase |
| **Create** | `Write` | Write TODO.md with `- [ ]` checkboxes | After user confirms execution plan |
| **Mark complete** | `Write` | Update checkbox from `- [ ]` to `- [x]` | After phase/step completes |
| **Delete** | `Bash` | `rm "{SYSTEM_ROOT}/TODO.md"` | All phases done or early termination |

**Prohibited**: Do not use `Edit` tool for TODO.md. Always use `Write` to rewrite the full file when marking checkboxes, to avoid partial-update failures.

## Phase Gate Rule

Before **every** phase or step, enforce this gate:

```
1. MUST execute Read tool on {SYSTEM_ROOT}/TODO.md
2. If TODO.md does NOT exist → STOP (no active workflow)
3. If TODO.md exists:
   a. Read all checkboxes
   b. Verify ALL prior phases/steps are [x]
   c. If any prior phase is still [ ] → STOP, do not proceed
   d. If all prior phases are [x] → proceed with current phase
4. After phase completes → MUST execute Write tool to mark current phase [x]
5. STOP. Wait for user confirmation before next phase.
```

**Quality gate** (in addition to checkbox verification): Verify output files from prior phases exist and are non-empty. If fail → log to `error-log.md` → ask user.

## TODO.md Format

TODO.md uses a consistent format across all workflow variants:

```markdown
# TODO - {topic}
- [ ] Phase 1: {name} - {description}
- [ ] Phase 2: {name} - {description}
- [ ] Phase 3: {name} - {description}
...
```

- Title line: `# TODO - {topic}`
- Each phase/step: `- [ ] Phase N: {name} - {description}`
- Checked: `- [x] Phase N: {name} - {description}`
- No other content (no notes, no metadata inside TODO.md)

## Workflow Variants

### Variant A: Full 5-Phase (Research Notes)

Created after Phase 0 (Requirement Discovery) confirms the plan:

```markdown
# TODO - {topic}
- [ ] Phase 1: collect - 资料收集与整理
- [ ] Phase 2: write - 生成笔记
- [ ] Phase 3: beautify - 美化排版
- [ ] Phase 4: evaluate - 质量评估
- [ ] Phase 5: digest - 自我学习
```

- Phases 4-5 are optional (user opts in at boundary)
- If user skips Phase 4-5 after Phase 3: early termination → delete TODO.md

### Variant B: Experience Notes (7-Step)

Created after execution plan confirmation:

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

- Step 1 is marked `[x]` immediately (user already provided content)
- Steps 6-7 are optional

### Variant C: REFRESH Mini Loop (Update Workflow)

Created by `/update` skill when REFRESH mode requires re-research:

```markdown
# TODO - REFRESH: {topic}
- [ ] mini-collect - 定向资料收集
- [ ] mini-curate - 定向资料整理
- [ ] mini-write - 定向更新笔记
```

- Only 3 phases, no optional steps
- All 3 must complete → delete TODO.md
- If user cancels mid-loop → early termination → delete TODO.md

## Early Termination

Early termination occurs when the user decides to stop before all phases are complete.

**Rules:**

1. Confirm with user: "Task complete. Cleaning up workflow."
2. MUST execute Bash tool: `rm "{SYSTEM_ROOT}/TODO.md"`
3. TODO.md must NOT be left behind — orphaned TODO.md causes false "resume" prompts on next session
4. This applies to all workflow variants (A, B, and C)

**Common early termination points:**

| Variant | Typical Stop Point | Trigger |
|---------|-------------------|---------|
| A (Full) | After Phase 3 (beautify) | User says "done" / "可以了" |
| B (Experience) | After Step 5 (beautify) | User says "done" / "可以了" |
| C (REFRESH) | Any mini-phase | User says "取消" / "算了" |

## Resume Check

At the start of **every new session**, before entering any phase or step:

1. MUST execute Read tool on `{SYSTEM_ROOT}/TODO.md`
2. **If TODO.md does NOT exist** → no active workflow → proceed normally
3. **If TODO.md exists**:
   a. Read all checkboxes to determine which phases are `[x]`
   b. Ask user: `"Detected unfinished workflow ({topic}). Resume from Phase [N]?"`
      - `[N]` = first phase that is still `[ ]`
   c. **User says yes** → jump to that phase (still enforce phase gate for that phase)
   d. **User says no** → ask: "Archive or delete TODO.md?"
      - Archive → move TODO.md to `4-meta/` with timestamp
      - Delete → `rm "{SYSTEM_ROOT}/TODO.md"`
      - Then start fresh

**Never skip the resume check.** An orphaned TODO.md from a crashed/interrupted session must be surfaced, not silently ignored.
