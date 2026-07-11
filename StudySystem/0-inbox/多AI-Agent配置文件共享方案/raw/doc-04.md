# AGENTS.md 规范与跨工具配置策略

## Source

Compiled from: morphllm.com/agents-md-guide, developer.aliyun.com article 1742259, cloud.tencent.cn article 2686951, tembo.io/blog/agents-md

## Overview

AGENTS.md is an open standard stewarded by the Agentic AI Foundation under the Linux Foundation -- backed by OpenAI, Google, Cursor, Factory, and others. It has been adopted by 60,000+ open-source projects and 30+ AI coding tools. It serves as "a README for agents."

## What is AGENTS.md?

AGENTS.md is a plain Markdown file at your project root that gives AI coding agents build commands, test instructions, conventions, and boundaries. Key design principles:

- **Simple**: Pure standard Markdown, no required fields, no frontmatter, no conditional loading
- **Open**: Supported by 30+ tools (Codex, Jules, Cursor, Windsurf, Aider, VS Code, JetBrains Junie, GitHub Copilot, Gemini CLI, etc.)
- **Inclusive**: Any tool can adopt it without permission

## Typical Example

```markdown
# AGENTS.md

## Commands
- Install deps: `pnpm install`
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`

## Code style
- TypeScript strict mode
- Single quotes, no semicolons
```

## AGENTS.md vs CLAUDE.md vs .cursorrules

| Feature | AGENTS.md | CLAUDE.md | .cursorrules |
|---------|-----------|-----------|--------------|
| Scope | 30+ agents | Claude Code only | Cursor only |
| Format | Plain Markdown | Markdown + @imports | Markdown / .mdc |
| Hierarchy | Nearest file wins | Global + project + subdir + local | Single file + .cursor/rules/ |
| @imports | No | Yes (max 4 hops) | No |
| Personal override | Nearest file wins | CLAUDE.local.md | @ruleName |
| Hooks | No | Yes Pre/post tool hooks | No |
| Size limit | 32 KiB (Codex default) | ~200 lines recommended | No hard limit |
| Conditional loading | No | Yes (paths frontmatter) | Yes (Auto Attached glob) |
| Governance | Linux Foundation | Anthropic | Cursor Inc. |

**90%+ of content is identical** across these files. Only advanced features differ.

## Best Practices (2026 Consensus)

### 1. Keep it short: <=200 lines or ~32 KiB

- 50-line files: 94% rule adherence
- 400-line files: 71% rule adherence
- Codex enforces a 32 KiB hard cap (silently truncated beyond)
- Windsurf enforces 6,000 chars/file, 12,000 total

### 2. Only include what the agent cannot infer from code

| Include | Exclude |
|---------|---------|
| Exact build/test commands with flags | Commands already in package.json |
| Rules that differ from language defaults | Standard conventions (PEP 8, Prettier) |
| Architectural constraints | Full API documentation (link instead) |
| Explicit boundaries | Obvious practices |

### 3. Use positive, verifiable instructions

- Bad: "Don't use class components"
- Good: "Use React functional components with Hooks"

### 4. Structure for scalability

**Monorepos**: Place nested AGENTS.md files in each subpackage. The nearest file to the edited file wins. OpenAI's Codex repo uses 88 AGENTS.md files.

**Large projects**: Split rules into subdirectories.

### 5. Prefer commands over prose

Agents act on executable commands, not descriptions.

### 6. Iterate from real failures

Add rules only after an agent makes the same mistake twice.

## The Multi-Tool Strategy: One Source of Truth

### Strategy A: AGENTS.md as Core (Diverse Tools Team)

```
project/
├── AGENTS.md              # Core rules (shared by all tools)
├── CLAUDE.md              # @AGENTS.md + Claude-specific extras
├── .cursor/rules/         # Cursor-specific (optional)
└── .windsurfrules         # Windsurf-specific (optional)
```

### Strategy B: CLAUDE.md as Core (Claude Code Heavy Team)

```
project/
├── CLAUDE.md              # Core rules
├── AGENTS.md -> symlink to CLAUDE.md
└── .cursorrules           # Content synced from CLAUDE.md
```

### Monorepo Nested Pattern

```
monorepo/
├── CLAUDE.md / AGENTS.md     # Global rules for entire repo
├── packages/
│   ├── frontend/CLAUDE.md    # Frontend rules (overrides parent)
│   └── backend/CLAUDE.md     # Backend rules (overrides parent)
```

Claude Code loads from root to working directory -- closer files have higher priority.
AGENTS.md resolution: "nearest file wins; user chat overrides everything."

## Research & Data

### Princeton Study (2026)

- 28.6% median runtime reduction with AGENTS.md present
- 16.6% fewer tokens consumed
- Measured across 10 repos, 124 PRs using Codex

### ETH Zurich Warning (2026)

- LLM-generated AGENTS.md files slightly reduced task success (+23% cost)
- Human-written files improved success by ~4%
- Key takeaway: low-quality configs are worse than none at all

## Team Workflow Recommendations

| Practice | Recommendation |
|----------|---------------|
| Version control | Commit AGENTS.md and CLAUDE.md to the repo |
| Code review | Include config file changes in PR reviews |
| Drift prevention | Quarterly review alongside docs |
| Onboarding | New devs inherit team standards automatically |
| Auto-generation | Avoid LLM-generated files; write by hand |
