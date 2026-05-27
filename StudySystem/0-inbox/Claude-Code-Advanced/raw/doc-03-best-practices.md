# Best Practices for Claude Code
- **Source**: https://code.claude.com/docs/en/best-practices
- **Author**: Anthropic
- **Date**: 2026
- **Type**: official

---
# Best Practices for Claude Code

Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.

## Core Constraint

Most best practices are based on one constraint: **Claude's context window fills up fast, and performance degrades as it fills.**

## Give Claude a Way to Verify Its Work

The single highest-leverage thing you can do: include tests, screenshots, or expected outputs so Claude can check itself.

| Strategy | Before | After |
|----------|--------|-------|
| Provide verification criteria | "implement email validation" | "test cases: user@example.com → true, invalid → false" |
| Verify UI visually | "make dashboard better" | "screenshot → implement → compare → fix differences |
| Address root causes | "build is failing" | "error: [paste]. fix root cause, don't suppress |

## Explore, Then Plan, Then Code

Use plan mode to separate research from implementation:

1. **Explore**: Enter plan mode, Claude reads files without making changes
2. **Plan**: Ask Claude to create implementation plan
3. **Implement**: Switch out of plan mode, let Claude code
4. **Commit**: Ask to commit and create PR

## Provide Specific Context in Prompts

| Strategy | Example |
|----------|---------|
| Scope the task | "test foo.py for logout edge case, avoid mocks" |
| Point to sources | "look through git history to understand API evolution" |
| Reference patterns | "follow HotDogWidget.php pattern" |
| Describe symptom | "login fails after timeout, check token refresh in src/auth/" |

Use `@` to reference files, paste images directly, give URLs for docs.

## Configure Your Environment

### Write an Effective CLAUDE.md

Include:
- Bash commands Claude can't guess
- Code style rules that differ from defaults
- Testing instructions and preferred test runners
- Repository etiquette
- Architectural decisions
- Common gotchas

Exclude:
- Anything Claude can figure out by reading code
- Standard language conventions
- Detailed API documentation (link to docs instead)
- Information that changes frequently

### Other Configurations

- **Permissions**: Use auto mode, allowlists, or sandboxing
- **CLI tools**: Tell Claude to use `gh`, `aws`, `gcloud`, etc.
- **MCP servers**: Connect external tools with `claude mcp add`
- **Hooks**: Use for actions that must happen every time
- **Skills**: Create for domain knowledge and reusable workflows
- **Subagents**: Define specialized assistants in `.claude/agents/`

## Communicate Effectively

### Ask Codebase Questions
Ask like you'd ask a senior engineer: "How does logging work?", "How do I make a new API endpoint?"

### Let Claude Interview You
For larger features, have Claude interview you first using AskUserQuestion tool.

## Manage Your Session

### Course-Correct Early and Often
- `Esc`: stop Claude mid-action
- `Esc + Esc` or `/rewind`: open rewind menu
- "Undo that": revert changes
- `/clear`: reset context between unrelated tasks

### Manage Context Aggressively
- Use `/clear` frequently between tasks
- Run `/compact <instructions>` for more control
- Customize compaction in CLAUDE.md
- Use `/btw` for quick questions without growing context

### Use Subagents for Investigation
Delegate research to subagents to keep main conversation clean.

### Rewind with Checkpoints
Every prompt creates a checkpoint. Restore conversation, code, or both.

### Resume Conversations
Name sessions with `/rename`. Use `claude --continue` or `claude --resume`.

## Automate and Scale

### Run Non-Interactive Mode
```bash
claude -p "prompt" --output-format json
```

### Run Multiple Sessions
- Worktrees: separate git checkouts
- Desktop app: manage multiple local sessions
- Web: cloud infrastructure
- Agent teams: automated coordination

### Fan Out Across Files
Loop through tasks with `claude -p` for each file.

## Avoid Common Failure Patterns

- **Kitchen sink session**: `/clear` between unrelated tasks
- **Correcting over and over**: After 2 failed corrections, `/clear` and write better prompt
- **Over-specified CLAUDE.md**: Prune ruthlessly
- **Trust-then-verify gap**: Always provide verification
- **Infinite exploration**: Scope investigations narrowly

## Develop Your Intuition

Pay attention to what works. Over time, develop intuition about when to be specific vs open-ended, when to plan vs explore, when to clear context vs let it accumulate.
