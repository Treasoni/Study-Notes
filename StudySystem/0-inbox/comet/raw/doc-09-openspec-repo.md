[![OpenSpec logo](https://github.com/Fission-AI/OpenSpec/raw/main/assets/openspec_bg.png)](https://github.com/Fission-AI/OpenSpec)

[![CI](https://github.com/Fission-AI/OpenSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/Fission-AI/OpenSpec/actions/workflows/ci.yml) [![npm version](https://camo.githubusercontent.com/92a019ce6fd31fc491a16699f7aa9c4335ef1524dfdfff013ff2f452ee0c0a12/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f762f4066697373696f6e2d61692f6f70656e737065633f7374796c653d666c61742d737175617265)](https://www.npmjs.com/package/@fission-ai/openspec) [![License: MIT](https://camo.githubusercontent.com/a7e65aee57b11d28e4caff8b945729a66be0bb663f7f93bd24c5aa65699f148e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d626c75652e7376673f7374796c653d666c61742d737175617265)](https://github.com/Fission-AI/OpenSpec/blob/main/LICENSE) [![Discord](https://camo.githubusercontent.com/16ee4b54d4a90482064b54dc0d6e98634e967c2c2083965d8a7ed3031401dc3e/68747470733a2f2f696d672e736869656c64732e696f2f646973636f72642f313431313635373039353633393630313135343f7374796c653d666c61742d737175617265266c6f676f3d646973636f7264266c6f676f436f6c6f723d7768697465266c6162656c3d446973636f7264267375666669783d2532306f6e6c696e65)](https://discord.gg/YctCnvvshC)

**The most loved spec framework.**

[![Stars](https://camo.githubusercontent.com/eb498313abafd00ced2c50720e4848b77f9698259a7b135e6c5e76d7e813c9cf/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f73746172732f46697373696f6e2d41492f4f70656e537065633f7374796c653d666c61742d737175617265266c6162656c3d5374617273)](https://github.com/Fission-AI/OpenSpec/stargazers) [![Downloads](https://camo.githubusercontent.com/f7d69851f27d4a01df2825849a8347443c94e89a5d7cbabdb6a7a04cbfea8581/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f646d2f4066697373696f6e2d61692f6f70656e737065633f7374796c653d666c61742d737175617265266c6162656c3d446f776e6c6f6164732f6d6f)](https://www.npmjs.com/package/@fission-ai/openspec) [![Contributors](https://camo.githubusercontent.com/23f6dc42c098714108cc16e29333a10fe1dcb4eedd54cab134111250b6d213d5/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f636f6e7472696275746f72732f46697373696f6e2d41492f4f70656e537065633f7374796c653d666c61742d737175617265266c6162656c3d436f6e7472696275746f7273)](https://github.com/Fission-AI/OpenSpec/graphs/contributors)  Our philosophy:

```
→ fluid not rigid
→ iterative not waterfall
→ easy not complex
→ built for brownfield not just greenfield
→ scalable from personal projects to enterprises
```

> [!tip] Tip
> **New workflow now available!** We've rebuilt OpenSpec with a new artifact-guided workflow.
> 
> Run `/opsx:propose "your idea"` to get started. → [Learn more here](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)

Follow [@0xTab on X](https://x.com/0xTab) for updates · Join the [OpenSpec Discord](https://discord.gg/YctCnvvshC) for help and questions.

## See it in action

```
You: /opsx:propose add-dark-mode
AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — why we're doing this, what's changing
     ✓ specs/       — requirements and scenarios
     ✓ design.md    — technical approach
     ✓ tasks.md     — implementation checklist
     Ready for implementation!

You: /opsx:apply
AI:  Implementing tasks...
     ✓ 1.1 Add theme context provider
     ✓ 1.2 Create toggle component
     ✓ 2.1 Add CSS variables
     ✓ 2.2 Wire up localStorage
     All tasks complete!

You: /opsx:archive
AI:  Archived to openspec/changes/archive/2025-01-23-add-dark-mode/
     Specs updated. Ready for the next feature.
```

**OpenSpec Dashboard**

[![OpenSpec dashboard preview](https://github.com/Fission-AI/OpenSpec/raw/main/assets/openspec_dashboard.png)](https://github.com/Fission-AI/OpenSpec/blob/main/assets/openspec_dashboard.png)

## Quick Start

**Requires Node.js 20.19.0 or higher.**

Install OpenSpec globally:

```
npm install -g @fission-ai/openspec@latest
```

Then navigate to your project directory and initialize:

```
cd your-project
openspec init
```

Now tell your AI: `/opsx:propose <what-you-want-to-build>`

If you want the expanded workflow (`/opsx:new`, `/opsx:continue`, `/opsx:ff`, `/opsx:verify`, `/opsx:bulk-archive`, `/opsx:onboard`), select it with `openspec config profile` and apply with `openspec update`.

> [!note] Note
> Not sure if your tool is supported? [View the full list](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) – we support 25+ tools and growing.
> 
> Also works with pnpm, yarn, bun, and nix. [See installation options](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md).

## Docs

→ **[Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)**: first steps  
→ **[Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)**: combos and patterns  
→ **[Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)**: slash commands & skills  
→ **[CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)**: terminal reference  
→ **[Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)**: tool integrations & install paths  
→ **[Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)**: how it all fits  
→ **[Multi-Language](https://github.com/Fission-AI/OpenSpec/blob/main/docs/multi-language.md)**: multi-language support  
→ **[Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)**: make it yours

## Community schemas

Third-party schema bundles distributed via standalone repositories — these provide opinionated workflows that integrate OpenSpec with other tools, similar to how [github/spec-kit's community extension catalog](https://github.com/github/spec-kit/tree/main/extensions) handles tool integrations.

→ **[Browse the catalog](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md#community-schemas)** in the customization docs.

## Why OpenSpec?

AI coding assistants are powerful but unpredictable when requirements live only in chat history. OpenSpec adds a lightweight spec layer so you agree on what to build before any code is written.

- **Agree before you build** — human and AI align on specs before code gets written
- **Stay organized** — each change gets its own folder with proposal, specs, design, and tasks
- **Work fluidly** — update any artifact anytime, no rigid phase gates
- **Use your tools** — works with 20+ AI assistants via slash commands

### How we compare

**vs. [Spec Kit](https://github.com/github/spec-kit)** (GitHub) — Thorough but heavyweight. Rigid phase gates, lots of Markdown, Python setup. OpenSpec is lighter and lets you iterate freely.

**vs. [Kiro](https://kiro.dev/)** (AWS) — Powerful but you're locked into their IDE and limited to Claude models. OpenSpec works with the tools you already use.

**vs. nothing** — AI coding without specs means vague prompts and unpredictable results. OpenSpec brings predictability without the ceremony.

## Updating OpenSpec

**Upgrade the package**

```
npm install -g @fission-ai/openspec@latest
```

**Refresh agent instructions**

Run this inside each project to regenerate AI guidance and ensure the latest slash commands are active:

```
openspec update
```

## Usage Notes

**Model selection**: OpenSpec works best with high-reasoning models. We recommend Codex 5.5 and Opus 4.7 for both planning and implementation.

**Context hygiene**: OpenSpec benefits from a clean context window. Clear your context before starting implementation and maintain good context hygiene throughout your session.

## Contributing

**Small fixes** — Bug fixes, typo corrections, and minor improvements can be submitted directly as PRs.

**Larger changes** — For new features, significant refactors, or architectural changes, please submit an OpenSpec change proposal first so we can align on intent and goals before implementation begins.

When writing proposals, keep the OpenSpec philosophy in mind: we serve a wide variety of users across different coding agents, models, and use cases. Changes should work well for everyone.

**AI-generated code is welcome** — as long as it's been tested and verified. PRs containing AI-generated code should mention the coding agent and model used (e.g., "Generated with Claude Code using claude-opus-4-5-20251101").

### Development

- Install dependencies: `pnpm install`
- Build: `pnpm run build`
- Test: `pnpm test`
- Develop CLI locally: `pnpm run dev` or `pnpm run dev:cli`
- Conventional commits (one-line): `type(scope): subject`

## Other

**Telemetry**

OpenSpec collects anonymous usage stats.

We collect only command names and version to understand usage patterns. No arguments, paths, content, or PII. Automatically disabled in CI.

**Opt-out:** `export OPENSPEC_TELEMETRY=0` or `export DO_NOT_TRACK=1`