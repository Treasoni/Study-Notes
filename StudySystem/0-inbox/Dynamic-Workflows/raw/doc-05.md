# Claude Code Changelog - Dynamic Workflows

> Source: https://code.claude.com/docs/en/changelog.md

## Dynamic Workflows Release Timeline

### Version 2.1.154 (May 28, 2026) - Initial Release
> **Introducing dynamic workflows**: ask Claude to create a workflow and it orchestrates work across tens to hundreds of agents in the background, so you can take on larger, more complex tasks. Run `/workflows` to view your runs.

### Version 2.1.152 (May 27, 2026) - Workflow Tool Refinement
Simplified the Workflow tool's inline progress display - live agent counts now show only in the persistent workflow status row below the prompt.

### Version 2.1.157 (May 29, 2026) - Skills Integration
Plugins in `.claude/skills` directories are now automatically loaded, no marketplace required.

### Version 2.1.160 (June 2, 2026) - Keyword Rename + Dismiss Behavior
- Renamed the dynamic-workflow trigger keyword from `workflow` to `ultracode`. The word "workflow" no longer triggers a run; asking for one in your own words still works. The trigger keyword is highlighted in violet in the prompt input.
- Pressing backspace right after a workflow trigger keyword now dismisses the workflow request (same as alt+w) instead of deleting a character.
- Fixed Workflow agents spawned with `isolation: "worktree"` in background sessions being blocked from editing files inside their own worktree.

### Version 2.1.172 (June 10, 2026) - Hierarchical Subagents
Sub-agents can now spawn their own sub-agents (up to 5 levels deep), enabling hierarchical workflow orchestration.

### Version 2.1.178 - Project Workflow Resolution
Saving to the project location writes to the closest `.claude/workflows/` directory that already exists between your working directory and the repository root, or to the repository root if none exists yet. Project workflows also load from every `.claude/workflows/` along that path, and when more than one defines the same name Claude Code runs the one closest to the working directory.

## Summary

Dynamic Workflows is a relatively new feature (released late May 2026). It integrates with:
- **Skills** - loaded automatically from `.claude/skills` directories
- **Subagents** - nested up to 5 levels deep for hierarchical orchestration
- **Slash Commands** - triggered via `/workflows` or the `ultracode` keyword
- **Hooks** - lifecycle hooks like `PostToolUse` support `continueOnBlock` for workflow control
- **Effort Levels** - ultracode is a session-only effort level that combines xhigh reasoning with automatic workflow orchestration
