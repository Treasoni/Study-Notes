Source: https://arctic-shift.photon-reddit.com/api/posts/ids?ids=1q182tf (Reddit r/ClaudeCode)

# Testing Claude Code with OpenSpec and Beads

**Author:** nicoracarlo (Senior Developer)
**Platform:** Reddit r/ClaudeCode
**Score:** 21 (96% upvote ratio)
**Date:** 2026

## Why OpenSpec

Brings structure to features or large fixes without excessive complexity, helping create solid code context.

## Why Beads

Beads (by Steve Yegge) is great at creating atomic context on specific tasks, reducing hallucination and context loss.

## Why Together

OpenSpec alone: generates good plans but "tends to write great code for a while, and then it starts hallucinating" when plans grow too big.

Beads alone: requires too much manual tracking for large features.

Combined: "best of both worlds."

## Workflow (4 Stages)

### 1. Analysis
Prompt CC with `ultrathink` to thoroughly analyze code before planning.

### 2. OpenSpec Proposal
Once analysis is satisfactory, ask CC to create an OpenSpec proposal.

### 3. OpenSpec Validation
"I THOROUGHLY VALIDATE THEM. Skipping this validation part is like asking for troubles."
Read and fix the spec until fully satisfied.

### 4. Beads Creation & Execution
Command: "Import the tasks from MY-OPENSPEC OpenSpec change into Beads"

## Configuration (CLAUDE.md Excerpt)

### OpenSpec Instructions
Open `@/openspec/AGENTS.md` when requests involve planning, proposals, new capabilities, breaking changes, or ambiguous situations.

### Working Style: "Think First, Code Once"
7-step process: analyze thoroughly, map the system, clarify requirements, design a complete solution, present the plan, implement carefully, stick to the plan.

### Beads/Issue Tracking Rules
- Always use `bd` (Beads) for issue tracking
- EVERY `bd create` MUST include `-d` (full context flag)
- Description must include: spec file reference, relevant requirements, acceptance criteria, technical context

### AGENTS.md -- Beads Usage Table

| Situation | Tool | Action |
|---|---|---|
| New feature | OpenSpec | proposal first |
| Approved spec | Both | Import tasks to Beads |
| Bug/small task | Beads | `bd create` directly |
| Discovered issue | Beads | `bd create --discovered-from` |
| Ready to work | Beads | `bd ready` |
| Feature complete | OpenSpec | archive |

### Session Completion ("Landing the Plane")
Mandatory 7-step workflow: file remaining issues, run quality gates, update tracking, sync and push, clean up, verify final state, provide handoff context block.

## Results

"Very positive" outcomes: clear feature definitions, code matching the author's style, less hallucination, "less swearing."
