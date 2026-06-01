# Experience Notes (心得笔记)

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

When the user selects "心得笔记" in Phase 0, the workflow is **user-input-first** instead of research-first. The content comes from the user's own project experiences and insights, not external research.

## Resume Check (NEW SESSION)

See [todo-state-machine.md](todo-state-machine.md) — Resume Check section for complete rules.

## Workflow

**Step 1: User provides content**
Ask the user to share their experience — free-form text, bullet points, or a rough draft. Save raw input to `0-inbox/{topic}/raw-input.md`.

After the execution plan is confirmed → MUST execute Write tool to create `{SYSTEM_ROOT}/TODO.md`:

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

Mark Step 1 as `[x]` immediately in TODO.md.

**Step 2: Review for accuracy**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

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

After review complete → MUST execute Write tool to mark Step 2 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

**Step 3: User decides on research**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

For each flagged item, ask the user:
- "This needs verification" → run mini collect→curate for that specific point
- "This is fine as-is" → keep original wording
- "Add more about X" → optional mini research for expansion

When mini research is needed, use the same targeted approach as the Update skill's REFRESH mode: isolate to `0-inbox/{topic}/{subtopic}/` and `1-curated/{topic}/{subtopic}/`.

After research decisions are resolved → MUST execute Write tool to mark Step 3 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

**Step 4: Write draft**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

Invoke `/write` with note type `experience`. The write skill uses `experience-template.md` and marks sources as `[来源: 个人经验]`. Draft goes to `2-drafts/{topic}/`.

After draft complete → MUST execute Write tool to mark Step 4 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

**Step 5: Beautify**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

Same as Phase 3 — apply Obsidian formatting, write to user-specified output path. User reviews and approves.

After user approves → MUST execute Write tool to mark Step 5 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

**Step 6: Optional evaluate**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

Same as Phase 4 — score quality, cross-validate.

After evaluate complete → MUST execute Write tool to mark Step 6 `[x]` in `{SYSTEM_ROOT}/TODO.md`.

**Step 7: Optional digest**

**Gate**: See [todo-state-machine.md](todo-state-machine.md) — Phase Gate Rule.

Same as Phase 5 — log session learnings.

After digest complete → See [todo-state-machine.md](todo-state-machine.md) — Early Termination section.

### Early Termination

If user stops before Step 7 (e.g., after beautify, skipping evaluate/digest), see [todo-state-machine.md](todo-state-machine.md) — Early Termination section.

## When the User is Unsure About Research

If the user says "I don't know if I need to research this", review their content and give a clear recommendation:
- "Claim X about Y — I'm not confident this is correct. Recommend verifying."
- "Section Z is experience-based and doesn't need external verification."
- "This part would benefit from an official doc reference. Want me to find one?"
