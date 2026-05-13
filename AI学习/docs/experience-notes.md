# Experience Notes (心得笔记)

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

When the user selects "心得笔记" in Phase 0, the workflow is **user-input-first** instead of research-first. The content comes from the user's own project experiences and insights, not external research.

## Workflow

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

## When the User is Unsure About Research

If the user says "I don't know if I need to research this", review their content and give a clear recommendation:
- "Claim X about Y — I'm not confident this is correct. Recommend verifying."
- "Section Z is experience-based and doesn't need external verification."
- "This part would benefit from an official doc reference. Want me to find one?"
