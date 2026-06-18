# Claude Code - Overview & Feature Map (for Dynamic Workflows context)

> Source: https://code.claude.com/docs/en/overview.md
> Title: Overview

## What is Claude Code?

Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

## What You Can Do (High-Level Capabilities)

### Build features and fix bugs
Describe what you want in plain language. Claude Code plans the approach, writes the code across multiple files, and verifies it works.

### Create commits and pull requests
Claude Code works directly with git. It stages changes, writes commit messages, creates branches, and opens pull requests.

### Connect your tools with MCP
The Model Context Protocol (MCP) is an open standard for connecting AI tools to external data sources. With MCP, Claude Code can read your design docs in Google Drive, update tickets in Jira, pull data from Slack, or use your own custom tooling.

### Customize with instructions, skills, and hooks
- **CLAUDE.md** - markdown file you add to your project root that Claude Code reads at the start of every session. Use it to set coding standards, architecture decisions, preferred libraries, and review checklists. Claude also builds auto memory as it works, saving learnings like build commands and debugging insights across sessions.
- **Skills** - Create to package repeatable workflows your team can share, like `/review-pr` or `/deploy-staging`.
- **Hooks** - Run shell commands before or after Claude Code actions, like auto-formatting after every file edit or running lint before a commit.

### Run agent teams and build custom agents
Spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results.

- To run several full sessions in parallel and watch them from one screen, use **background agents** (agent view).
- For fully custom workflows, the **Agent SDK** lets you build your own agents powered by Claude Code's tools and capabilities.

## Dynamic Workflows in Context

The overview positions dynamic workflows within the broader Claude Code capability stack:

> "Run agent teams and build custom agents: Spawn multiple Claude Code agents that work on different parts of a task simultaneously. A lead agent coordinates the work, assigns subtasks, and merges results."

Dynamic workflows are an evolution of this concept where the orchestration itself is codified as a JavaScript script that the runtime executes. This makes them well-suited for:
- Tasks too large for a single conversation to coordinate
- Tasks requiring cross-checking of results across agents
- Tasks that need to be rerunnable and reviewable as code

## Feature Map: How Dynamic Workflows Relate to Other Features

| Feature | Layer | Purpose | Relationship to Dynamic Workflows |
|---|---|---|---|
| **CLAUDE.md** | Persistent context | Project-specific instructions loaded every session | Workflows can read CLAUDE.md for project context |
| **Auto memory** | Persistent context | Notes Claude writes itself across sessions | Workflows can use the same memory mechanism |
| **MCP** | External integration | Connect to external tools and data sources | Workflows use MCP through subagents they spawn |
| **Skills** | Reusable prompts | Prompt-based workflows that load into context | Distinct from workflows: skills run in main context, workflows run scripts |
| **Slash Commands** | Reusable prompts | Built-in and custom commands | `/workflows` is a slash command for watching workflows; `/deep-research` is a bundled workflow |
| **Subagents** | Worker primitive | Isolated context for delegated tasks | Subagents are what workflows orchestrate |
| **Hooks** | Lifecycle control | Deterministic shell commands at lifecycle events | Hooks fire for subagent events in workflows; PreToolUse still enforces policy |
| **Agent Teams** | Multi-session coordination | Lead coordinates peer sessions via shared task list | Alternative model - workflow is "script-coordinated", team is "lead-coordinated" |
| **Agent View** | Background sessions | One screen to monitor multiple background sessions | Different approach - manual handoff rather than Claude/coordinated |
| **Worktrees** | File isolation | Separate git checkout for parallel sessions | Complementary - use with workflows to avoid file conflicts |
| **Agent SDK** | Programmatic access | Build your own agents with Claude Code tools | Use SDK to host workflow runtimes externally |

## Where Dynamic Workflows Fit

Dynamic workflows are positioned as the **scale and quality** layer. When subagents are insufficient (a few delegated tasks per turn) and when the work benefits from cross-verification, workflows provide a way to script the orchestration while Claude writes the script for you.

The key innovation is moving the "plan" from Claude's turn-by-turn context to a JavaScript script that:
1. Holds the loop and branching explicitly
2. Tracks intermediate results in script variables
3. Can be saved and rerun
4. Can be inspected, edited, and diffed between runs
5. Applies quality patterns (adversarial review, multi-angle drafting) that aren't possible in single-pass execution

## Use Cases Mentioned

- **Codebase audits** - search whole codebase for patterns
- **Large migrations** - hundreds of files transformed in parallel
- **Cross-checked research** - multiple agents independently investigate
- **Plan drafting from multiple angles** - independent plans compared before commitment
