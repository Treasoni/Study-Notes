# Updating Existing Notes

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

When the user wants to add content to or refresh an existing published note, invoke `/update` — do NOT re-run the full creation pipeline.

## Two Modes

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

## Key Rules for Updates

- **Minimal diff**: Only modify the target section, do not re-beautify the whole note
- **Match existing style**: New content uses the same callout types, table conventions, code block languages
- **Preserve wikilinks**: Do not touch or break existing `[[links]]`
- **Update frontmatter**: Set `updated: YYYY-MM-DD` to current date
