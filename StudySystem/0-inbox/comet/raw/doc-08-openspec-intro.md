> OpenSpec is an open-source framework that brings spec-driven development to AI coding agents. Write specs in Markdown, agree on the plan before writing code, and keep your project’s requirements versioned in Git. Three commands — propose, apply, archive — and your agent finally builds what you actually want.

- [Why bother with specs?](https://www.rushis.com/introduction-to-openspec/#why-bother-with-specs)
- [Setup in 60 seconds](https://www.rushis.com/introduction-to-openspec/#setup-in-60-seconds)
- [The three-step workflow](https://www.rushis.com/introduction-to-openspec/#the-three-step-workflow)
- [What delta specs look like](https://www.rushis.com/introduction-to-openspec/#what-delta-specs-look-like)
- [Expanded workflow (optional)](https://www.rushis.com/introduction-to-openspec/#expanded-workflow-optional)
- [Why OpenSpec over alternatives?](https://www.rushis.com/introduction-to-openspec/#why-openspec-over-alternatives)
- [Quick tips for getting the most out of it](https://www.rushis.com/introduction-to-openspec/#quick-tips-for-getting-the-most-out-of-it)
- [Get started](https://www.rushis.com/introduction-to-openspec/#get-started)

You’ve been there. You ask Claude Code or Cursor to build a feature, it generates 400 lines of code, and half of it misses the point. Not because the model is bad — because *your prompt was vague and the requirements lived nowhere*.

OpenSpec fixes this. It’s an open-source, spec-driven development (SDD) framework that makes you and your AI agent agree on **what to build** before a single line of code is written. Think of it as a lightweight planning layer that lives right inside your repo.

## Why bother with specs?

AI coding agents are great at generating code. They’re terrible at guessing what you actually want. The bottleneck isn’t model capability — it’s under-specification.

Without specs, your requirements exist only in chat history. They vanish when the session ends. They can’t be reviewed, versioned, or shared.

You might be thinking: “We already have requirements — they’re in Jira.” Fair point. Plenty of teams keep specs in external systems like Jira, Linear, Confluence, or Notion. That works for humans, but it creates a real problem for AI agents. Your agent can’t browse your Jira board mid-session (not reliably, anyway). Even if you paste a ticket into the chat, the agent loses that context the moment the session ends. External systems also introduce drift — the Jira ticket says one thing, the code does another, and nobody updates either. You end up with two sources of truth that quietly diverge.

The upside of external tools is obvious: they have mature workflows for prioritization, assignment, status tracking, and cross-team visibility. OpenSpec isn’t trying to replace that. But for the actual *specification* — the detailed requirements, scenarios, and design decisions your agent needs while writing code — keeping them in-repo as Markdown means they’re always accessible, always versioned, and always next to the code they describe. You can still link back to Jira tickets from your specs. But the spec itself lives where the work happens.

OpenSpec solves this by giving your project a persistent `openspec/` folder containing two things:

- **A spec library** (`openspec/specs/`) — living documentation of how your system works right now, organized by capability.
- **A changes system** (`openspec/changes/`) — where each new feature gets its own folder with a proposal, design doc, task list, and delta specs showing exactly what’s changing.

Everything is Markdown. Everything is checkable into Git. Your agent can always reference it.

## Setup in 60 seconds

You need Node.js 20.19.0+ installed.

```
# Install globally
npm install -g @fission-ai/openspec@latest

# Navigate to your project
cd your-project

# Initialize
openspec init
```

During init, OpenSpec asks which AI tool you’re using (Claude Code, Cursor, Windsurf, Copilot, Cline, etc.) and drops the right slash commands or skill files into your project. That’s it.

## The three-step workflow

OpenSpec’s core loop is dead simple: **Propose → Apply → Archive.**

### 1\. Propose

Tell your agent what you want to build. It creates a structured change folder with all the planning artifacts.

```
You: /opsx:propose add-user-authentication

AI: Created openspec/changes/add-user-authentication/
  ✓ proposal.md    — why we're doing this, what's changing
  ✓ specs/         — requirements and scenarios
  ✓ design.md      — technical approach
  ✓ tasks.md       — implementation checklist
```

This is where you **actually read the spec**, refine it, push back on design decisions, and catch misalignment — all *before* any code is written. Changes are cheap in Markdown. They’re expensive in code.

### 2\. Apply

Once you’re happy with the plan, tell the agent to implement it.

```
You: /opsx:apply

AI: Implementing tasks...
  ✓ 1.1 Add session middleware
  ✓ 1.2 Create login endpoint
  ✓ 2.1 Add password hashing
  ✓ 2.2 Wire up JWT tokens
All tasks complete!
```

The agent follows the spec, not a vague prompt. Every task traces back to a documented requirement.

### 3\. Archive

When the feature ships, archive the change. The delta specs merge back into your main spec library, keeping it up to date.

```
You: /opsx:archive

AI: Archiving add-user-authentication...
  ✓ Merged specs into openspec/specs/auth/spec.md
  ✓ Moved to openspec/changes/archive/2025-03-26-add-user-authentication/
Done!
```

Your spec library just grew. The next time someone (human or AI) asks “how does auth work in this project?”, the answer is already documented.

## What delta specs look like

Delta specs are the core concept. They clearly mark what’s being added, modified, or removed relative to the current system:

```
# Delta for Auth

## ADDED Requirements

### Requirement: Two-Factor Authentication
The system MUST require a second factor during login.

#### Scenario: OTP required
- GIVEN a user with 2FA enabled
- WHEN the user submits valid credentials
- THEN an OTP challenge is presented

## MODIFIED Requirements

### Requirement: Session Timeout
The system SHALL expire sessions after 30 minutes of inactivity.
(Previously: 60 minutes)
```

This format makes plan review straightforward. It’s easier to read a Markdown spec than a 500-line diff.

## Expanded workflow (optional)

The default profile gives you `propose`, `apply`, and `archive`. If you want more control, enable the expanded profile:

```
openspec config profile
openspec update
```

This unlocks additional commands:

- `/opsx:new` — create a change folder without generating artifacts yet
- `/opsx:ff` — “fast-forward” to generate all planning docs at once
- `/opsx:continue` — resume work on a change across sessions
- `/opsx:verify` — validate the implementation against the spec
- `/opsx:sync` — sync spec formatting
- `/opsx:onboard` — generate specs from an existing codebase

## Why OpenSpec over alternatives?

**vs. GitHub Spec Kit** — Spec Kit is thorough but heavier. It uses rigid phase gates, requires Python, and generates more boilerplate. OpenSpec is TypeScript-native and lets you iterate freely.

**vs. AWS Kiro** — Kiro is powerful but locks you into their IDE and limits your model choices. OpenSpec works with 20+ AI tools.

**vs. your agent’s plan mode** — Plan mode is great for a single session. But those plans vanish when you close the chat. OpenSpec persists your thinking across sessions and grows with your codebase.

**vs. doing nothing** — AI coding without specs means vague prompts, unpredictable output, and reviewing diffs instead of intentions.

## Quick tips for getting the most out of it

**Actually read the proposal.** OpenSpec is not a magic tool. It works best when you engage with the spec, push back on bad decisions, and refine requirements before implementation.

**Use it on brownfield projects.** OpenSpec was built for mature codebases where the real challenge is understanding how the current system works — not greenfield prototypes.

**Start with `/opsx:onboard`.** If you’re adding OpenSpec to an existing project, the onboard command generates initial specs from your codebase, giving your agent context from day one.

**Review plans, not just code.** Teams using OpenSpec are shifting from code review to plan review. It’s a better use of senior engineering time.

## Get started

```
npm install -g @fission-ai/openspec@latest
cd your-project
openspec init
```

Then tell your agent: `/opsx:propose <what-you-want-to-build>`

That’s it. Sixty seconds to install, three commands to learn, and your AI agent stops guessing what you want.

*OpenSpec is open source and available at [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec). The project is backed by Y Combinator (W26 batch) and has 34k+ GitHub stars.*

“A tool is only as powerful as your understanding of it; mastery of the ‘how’ is what determines the quality of the ‘what’.”-Rushi