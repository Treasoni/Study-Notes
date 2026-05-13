# Learnings Digest

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

To prevent `.learnings/` files from growing unbounded, the digest skill runs a digest cycle when thresholds are exceeded.

## Thresholds

| File | Threshold | Action |
|------|-----------|--------|
| `.learnings/LEARNINGS.md` | > 100 lines | Compress before logging new entries |
| `.learnings/ERRORS.md` | > 100 lines | Compress before logging new entries |
| `.learnings/RULES.md` | > 50 lines | Review and promote to CLAUDE.md, trim RULES.md |

## Digest Process

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

## RULES.md Format

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
