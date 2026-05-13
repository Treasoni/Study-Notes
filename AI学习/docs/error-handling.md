# Error Handling

> Part of the Study System. See [CLAUDE.md](../CLAUDE.md) for the top-level map.

During Phase 1-4 execution, if any error occurs or you manually intervene to correct the model's output, **record only, do not analyze**. Append a plain-text entry to `{SYSTEM_ROOT}/4-meta/error-log.md`:

```
[YYYY-MM-DD HH:MM] {phase} - {brief description of what went wrong}
{correction taken, if any}
```

## Rules

- Plain text only — no markdown headers, no bold, no analysis
- One entry per incident, separated by blank line
- Just state what happened and what was done — no root cause analysis, no impact assessment
- After recording, ask user how to proceed (retry / skip / abort / manual fix)
