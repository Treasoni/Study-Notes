# Overview - Claude Code Docs
- **Source**: https://code.claude.com/docs/en/overview
- **Author**: Anthropic
- **Date**: 2026
- **Type**: official

---
# Overview

Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

Claude Code is an AI-powered coding assistant that helps you build features, fix bugs, and automate development tasks. It understands your entire codebase and can work across multiple files and tools to get things done.

## Get started

Choose your environment to get started. Most surfaces require a Claude subscription or Anthropic Console account. The Terminal CLI and VS Code also support third-party providers.

## What you can do

- Automate tedious tasks: writing tests, fixing lint errors, resolving merge conflicts, updating dependencies
- Build features and fix bugs: describe what you want in plain language, Claude plans, writes, and verifies
- Create commits and pull requests
- Connect tools with MCP (Model Context Protocol)
- Customize with instructions (CLAUDE.md), skills, and hooks
- Run agent teams and build custom agents
- Pipe, script, and automate with the CLI
- Schedule recurring tasks
- Work from anywhere (terminal, VS Code, JetBrains, Desktop, Web)

## Environments

| Environment | Where code runs | Use case |
|-------------|-----------------|----------|
| Local | Your machine | Default. Full access |
| Cloud | Anthropic-managed VMs | Offload tasks |
| Remote Control | Your machine, controlled from browser | Use web UI while keeping everything local |

## Sessions

- Each new session starts with fresh context
- Claude persists learnings via auto memory and CLAUDE.md
- Sessions tied to directories, can use git worktrees for parallel sessions
- Resume with `claude --continue` or fork with `--fork-session`

## Context Window

Claude's context window holds conversation history, file contents, command outputs, CLAUDE.md, auto memory, skills, and system instructions. Claude compacts automatically when approaching limits.

## Safety Mechanisms

- **Checkpoints**: Every file edit is reversible (local to session, separate from git)
- **Permissions**: Control what Claude can do without asking

## Permission Modes

- Default: asks before file edits and shell commands
- Auto-accept edits: edits files and common filesystem commands without asking
- Plan mode: read-only, creates plan you can approve
- Auto mode: evaluates all actions with background safety checks
