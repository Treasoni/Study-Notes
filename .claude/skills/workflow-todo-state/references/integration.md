# Integration Guide

## Install Into Another Project

Recommended one-command install from this source project:

```bash
.claude/skills/workflow-todo-state/scripts/install.sh /path/to/target-project --with-skill --update-agents
```

Script-only install:

```bash
.claude/skills/workflow-todo-state/scripts/install.sh /path/to/target-project
```

Manual fallback:

```bash
mkdir -p /path/to/target-project/.claude/scripts
cp .claude/skills/workflow-todo-state/scripts/todo-state.sh /path/to/target-project/.claude/scripts/todo-state.sh
chmod +x /path/to/target-project/.claude/scripts/todo-state.sh
```

## Add Project Rule

Add this to the project entry instructions:

```markdown
Every workflow phase must read the project `todo.md` before acting. Do not skip phases. Change phase state only through `.claude/scripts/todo-state.sh`.
```

## Retrofit Existing Todo Templates

1. Add YAML frontmatter:
   ```yaml
   ---
   workflow: your-flow
   topic: "{topic}"
   project_slug: "{project_slug}"
   created_at: "{date}"
   last_updated: "{date}"
   current_phase: P0
   current_status: not_started
   mode: standard
   blocked_reason: ""
   ---
   ```
2. Add a visible current phase line:
   ```markdown
   > 当前阶段：阶段 0
   ```
3. Ensure each phase has one unique status line:
   ```markdown
   > [P3] ⬜ 未开始
   ```
4. Replace manual edits:
   ```bash
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" start P3
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P3
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" skip P3 "optional phase not needed"
   .claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" block P3 "waiting for confirmation"
   ```

## Validation Checklist

- `bash -n .claude/scripts/todo-state.sh`
- Start and complete P0 on a copied todo file.
- Try starting P2 before P1 is complete; it should fail.
- Try skipping an optional phase; `current_phase` should advance to the next pending phase.
- Confirm `## 异常记录` receives skip/block rows when present.
