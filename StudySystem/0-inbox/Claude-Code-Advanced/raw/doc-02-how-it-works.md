# How Claude Code Works
- **Source**: https://code.claude.com/docs/en/how-claude-code-works
- **Author**: Anthropic
- **Date**: 2026
- **Type**: official

---
# How Claude Code works

Understand the agentic loop, built-in tools, and how Claude Code interacts with your project.

## The Agentic Loop

When you give Claude a task, it works through three phases: **gather context**, **take action**, and **verify results**. These phases blend together.

The loop is powered by two components: **models** that reason and **tools** that act.

### Models

Claude Code uses Claude models to understand code and reason about tasks. Multiple models available:
- Sonnet: handles most coding tasks well
- Opus: stronger reasoning for complex architectural decisions
- Switch with `/model` during a session

### Tools

Tools are what make Claude Code agentic. Built-in tools fall into five categories:

| Category | What Claude can do |
|----------|-------------------|
| **File operations** | Read files, edit code, create new files, rename and reorganize |
| **Search** | Find files by pattern, search content with regex, explore codebases |
| **Execution** | Run shell commands, start servers, run tests, use git |
| **Web** | Search the web, fetch documentation, look up error messages |
| **Code intelligence** | See type errors and warnings after edits, jump to definitions, find references |

## What Claude Can Access

When you run `claude` in a directory, Claude Code gains access to:
- Your project (files in directory and subdirectories)
- Your terminal (any command you could run)
- Your git state
- Your CLAUDE.md
- Auto memory (learnings saved automatically)
- Extensions (MCP servers, skills, subagents, Claude in Chrome)

## Session Management

### Context Window Management

Claude's context window fills up as you work. Claude compacts automatically:
- Clears older tool outputs first
- Then summarizes conversation if needed
- Key code snippets and requests preserved
- Put persistent rules in CLAUDE.md

Run `/context` to see what's using space. MCP tool definitions are deferred by default.

### Manage Context with Skills and Subagents

- **Skills**: Load on demand. Descriptions visible at start, full content only when used.
- **Subagents**: Get their own fresh context, completely separate from main conversation.

## Checkpoints and Permissions

### Undo with Checkpoints

Every file edit is reversible. Press `Esc` twice to rewind to previous state, or ask Claude to undo.

Checkpoints are local to session, separate from git. Actions affecting remote systems (databases, APIs, deployments) can't be checkpointed.

### Permission Modes

Press `Shift+Tab` to cycle through permission modes:
- **Default**: asks before file edits and shell commands
- **Auto-accept edits**: edits files and common filesystem commands without asking
- **Plan mode**: read-only, creates plan you can approve
- **Auto mode**: evaluates all actions with background safety checks (research preview)

## Work Effectively

### Ask for Help
Claude Code can teach you how to use it. Built-in commands: `/init`, `/agents`, `/doctor`

### It's a Conversation
Start with what you want, then refine. Interrupt with `Esc` or type correction.

### Be Specific
Reference specific files, mention constraints, point to example patterns.

### Give Claude Something to Verify Against
Include test cases, paste screenshots, define expected output.

### Explore Before Implementing
Use plan mode (`Shift+Tab` twice) to analyze codebase first, then implement.

### Delegate, Don't Dictate
Give context and direction, trust Claude to figure out details.
