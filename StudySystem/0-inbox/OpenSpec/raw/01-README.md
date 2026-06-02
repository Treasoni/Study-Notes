Source: https://github.com/Fission-AI/OpenSpec
(synthesized from GitHub repo metadata, npm package page, and search results)

# OpenSpec

Spec-driven development (SDD) for AI coding assistants.

## Overview

OpenSpec is an open-source, AI-native framework for Spec-Driven Development (SDD). It adds a lightweight spec layer on top of AI coding assistants so that humans and AI agree on what to build before any code is written.

- **License:** MIT
- **Package:** `@fission-ai/openspec` on npm
- **Website:** https://openspec.dev/
- **Latest Stable:** v1.3.1 (as of June 2026)
- **Requires:** Node.js 20.19.0+
- **GitHub Stars:** 28k+

## Philosophy

OpenSpec is built on four principles:

- **Fluid not rigid** — No phase gates; work on what makes sense
- **Iterative not waterfall** — Learn as you build, refine as you go
- **Easy not complex** — Lightweight setup, minimal ceremony
- **Brownfield-first** — Works with existing codebases, not just greenfield

## Quick Start

```bash
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init
```

Then tell your AI: `/opsx:propose <what-you-want-to-build>`

## How It Works

Each change gets its own folder with artifacts:

| Artifact | Purpose |
|---|---|
| `proposal.md` | Why and what (intent, scope, approach) |
| `specs/` | What's changing (requirements + scenarios) |
| `design.md` | How (technical approach, architecture decisions) |
| `tasks.md` | Implementation checklist |

**Slash commands** drive the workflow (supported in 25+ AI tools):

| Command | Purpose |
|---|---|
| `/opsx:propose` | Create a change + generate planning artifacts |
| `/opsx:explore` | Think through ideas before committing |
| `/opsx:apply` | Implement tasks from the plan |
| `/opsx:verify` | Validate implementation matches specs |
| `/opsx:sync` | Merge delta specs into main specs |
| `/opsx:archive` | Archive completed changes |
| `/opsx:new` | Start a change scaffold (expanded workflow) |
| `/opsx:continue` | Create next artifact step-by-step (expanded) |
| `/opsx:ff` | Fast-forward: create all artifacts (expanded) |
| `/opsx:bulk-archive` | Archive multiple changes (expanded) |
| `/opsx:onboard` | Guided tutorial (expanded) |

## Project Structure

```
openspec/
├── specs/              # Source of truth (system behavior)
│   └── <domain>/
│       └── spec.md
├── changes/            # Proposed modifications
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs
│           └── <domain>/
│               └── spec.md
└── config.yaml
```

## Supported Tools (29+)

Claude Code, Cursor, Windsurf, GitHub Copilot, Amazon Q Developer, Gemini CLI, Codex, Cline, RooCode, Continue, Factory Droid, OpenCode, Kilo Code, Junie, Kimi CLI, Trae, and many more.

## Comparisons

- **vs. Spec Kit (GitHub):** OpenSpec is lighter and more iterative; Spec Kit has rigid phase gates and heavyweight Markdown requirements.
- **vs. Kiro (AWS):** Kiro locks you into their IDE and limited models; OpenSpec works with the tools you already use.
- **vs. nothing:** AI coding without specs leads to vague prompts and unpredictable results.

## Community & Ecosystem

- **Discord:** https://discord.gg/YctCnvvshC
- **npm:** `@fission-ai/openspec`
- **Forks:** `@novaraworks/openspec`, `@studyzy/openspec-cn`, `@bobby_z/openspec`, `openspec-plus`
- **Chinese docs:** radebit.github.io/OpenSpec-Docs-zh/
