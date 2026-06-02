Source: https://segmentfault.com/a/1190000047677830

# OpenSpec Initial Guide

**Date:** March 26, 2026
**Author:** ruanjianershu
**Publication:** SegmentFault
**Language:** Chinese

## What Is OpenSpec?

An AI-native, spec-driven development (SDD) system built for AI coding assistants. Before writing any code, developers and AI should first align on requirements.

### Problems It Solves

1. **Architecture drift** -- AI-generated code diverges from overall system design
2. **Context loss** -- Requirements exist only in chat logs, hard to track
3. **Tech debt** -- Lack of specs leads to inconsistent code quality
4. **Frequent rework** -- Misunderstandings cause repeated revisions

## Core Principles

**Design philosophy:** Flowing not rigid -> iterative not waterfall -> simple not complex

**Core idea:** Specs are the source of truth; code implements the specs (vs. traditional: code is the source of truth)

**Delta specs:** Central innovation -- describe changes using ADDED/MODIFIED/REMOVED markers

## Installation Methods

1. Global npm: `npm install -g @fission-ai/openspec@latest`
2. npx: `npx @fission-ai/openspec@latest init`
3. Other: pnpm, yarn, bun

## Workflow Profiles

- **core** -- Default fast path, recommended for beginners
- **extended** -- More granular control for advanced users

## Iteration Flow

```
Proposal -> Specs -> Design -> Tasks -> Apply -> Verify
                                         ^        |
                                         |   (fail)
                                         +--------+
                                              |
                                         (success)
                                              v
                                         Archive
```

## Best Practices

| Correct | Incorrect |
|---|---|
| Focus on "What" not "How" | Describe implementation details |
| Use GIVEN-WHEN-THEN scenarios | Use vague requirement descriptions |
| Ensure testability | Write unverifiable requirements |
| Keep concise, one change at a time | Try to do too much at once |

### Change Management Tips

1. Keep each change as one logical unit
2. Use clear names like `add-dark-mode`, avoid `feature-1`
3. Archive completed changes promptly
4. Initial specs don't need to be perfect; iterate as you go

### Team Collaboration

- Share `.openspec/` directory in the code repository
- Review `proposal.md` and `design.md` before implementing
- Use `/opsx:sync` regularly

## FAQ

**Q: OpenSpec vs. Git?** Git tracks code changes; OpenSpec tracks requirements. Complementary, not competitive.

**Q: Is OpenSpec required for every project?** Best for AI-assisted programming and team collaboration. Simple personal projects can use traditional approaches.

**Q: Which AI tools are supported?** Over 20 tools including Claude Code, Cursor, Windsurf, GitHub Copilot, Trae.

**Q: How to update?** Re-install the global npm package, then run `openspec update` within the project.
