![Spec-driven development patterns across OpenSpec, Superpowers, Spec Kit, and Spec Coding](https://spec-coding.dev/images/blog/spec-driven-development-tools-openspec-spec-kit-superpowers.svg)

Spec Coding Editorial Team · Spec-driven development notes

OpenSpec vs Superpowers vs GitHub Spec Kit is not a winner-takes-all comparison. Each approach starts from a different place, but they converge on the same practical idea: make intent, constraints, tasks, tests, and review evidence visible before an AI coding agent changes production code.

## The useful part of SDD is not the tool name

Spec-driven development has become a crowded label. Some teams mean formal specifications. Some mean executable acceptance criteria. Some mean AI-agent workflows that turn a product idea into specs, plans, tasks, and implementation. The useful question is not which label wins. The useful question is what artifact exists before code starts, who approves it, and how the final diff proves it followed that artifact.

That is why [OpenSpec](https://github.com/Fission-AI/OpenSpec), [Superpowers](https://github.com/obra/superpowers), and [GitHub Spec Kit](https://github.com/github/spec-kit) are worth studying together. They are not identical products, and Spec Coding is not a wrapper around any of them. But they expose a set of patterns that can make AI-assisted software delivery less vague and more reviewable.

## Pattern 1: create a durable artifact before implementation

OpenSpec organizes a change around artifacts such as a proposal, specs, design, and tasks. Spec Kit creates a lifecycle around project principles, the functional spec, a technical plan, a task list, and implementation. Superpowers starts by teasing a spec out of the conversation before planning and coding. Different vocabulary, same move: the agent should not jump straight from a chat prompt to a diff.

For a team, the concrete rule can be simple. Before code generation, a feature should have at least one durable file that names the goal, non-goals, acceptance criteria, owner, dependencies, and evidence requirement. A chat transcript is not enough. If the requirement only exists in the model context, nobody can review it later, rerun it, or compare the final code to it. For the lightweight version of this practice, see the [Spec as Code Hub](https://spec-coding.dev/spec-as-code).

## Pattern 2: separate product intent from technical planning

Spec Kit makes this separation explicit: specify what and why first, then plan implementation with the stack and architecture choices. OpenSpec similarly separates the proposal and specs from design and tasks. This matters because AI coding tools are quick to collapse product ambiguity into implementation detail. The moment a model chooses the database shape, API boundary, and UI behavior before the product question is settled, the team has lost control of the decision path.

A strong Spec Coding workflow keeps those layers separate:

| Layer | Question | Artifact |
| --- | --- | --- |
| Principles | What rules should guide decisions? | `constitution.md` or team guidelines |
| Intent | What user or system behavior must change? | `spec.md` |
| Plan | How will the change be implemented safely? | `design.md` or implementation plan |
| Work | What tasks can be executed and verified? | `tasks.md` |
| Proof | How do reviewers know it worked? | `evidence.md`, tests, logs, screenshots |

## Pattern 3: avoid rigid ceremony unless risk demands it

One reason OpenSpec is interesting is its explicit preference for workflows that are fluid rather than rigid, iterative rather than waterfall, and usable for brownfield codebases. That is a useful correction to the worst version of SDD: a big pile of Markdown that blocks work without improving review quality. A spec process should scale with risk. Authentication, payments, data migrations, public APIs, and AI-generated changes need stronger gates than a typo fix.

The minimum useful version is a one-page spec packet. The maximum useful version may include a constitution, requirements, technical design, task breakdown, migration plan, risk register, and test evidence. The key is to choose the smallest artifact set that still prevents hidden decisions from landing in code review.

## Pattern 4: turn tasks into verifiable units

Superpowers is especially strong on the idea that a plan should be clear enough for an implementation agent to follow without inventing context. It also emphasizes test-driven development and review gates. That is the missing bridge in many AI coding workflows. A spec alone is not enough if the next step is a giant prompt that asks the model to "build everything."

Break the plan into tasks that include file scope, acceptance criteria, test expectations, and review notes. A good task is not just "add retry logic." It is closer to:

```
Task: add timeout retry to refund worker
Write scope:
- src/billing/refund-worker.ts
- src/billing/refund-worker.test.ts

Acceptance:
- timeout once -> retry with same idempotency key
- timeout twice -> keep pending status, no duplicate refund_id

Evidence:
- test: refund_timeout_replay
- log query: duplicate_refund_attempts remains zero
```

That kind of task gives the coding agent room to implement, but not room to decide the product policy.

## Pattern 5: make review evidence part of the workflow

All three projects are ultimately trying to reduce the gap between "the assistant produced code" and "the team can trust the change." The missing word is evidence. The spec should not end at implementation. It should define what proof the reviewer expects: tests, fixture names, logs, screenshots, contract checks, migration dry runs, or rollout metrics.

This is where Spec Coding differs from a pure tooling comparison. We care less about which command starts the workflow and more about the artifact chain a reviewer can inspect. The chain should look like this:

```
ticket.md
  -> spec.md
  -> design.md
  -> tasks.md
  -> tests + evidence.md
  -> PR review
```

If any link is missing, the team should know why. If an AI-generated PR cannot map its changes back to a task and a criterion, the PR is not ready.

## Where each tool shines

| Tool or approach | Best lesson to borrow | Risk to avoid |
| --- | --- | --- |
| OpenSpec | Keep each change organized around proposal, specs, design, and tasks without making the process too heavy. | Letting the artifact folder become storage instead of a review contract. |
| Superpowers | Use skills and mandatory workflows to stop agents from skipping brainstorming, planning, TDD, and review. | Letting automation feel like approval. Humans still own scope and risk. |
| Spec Kit | Separate constitution, specification, planning, tasks, and implementation into a repeatable lifecycle. | Applying a full lifecycle to small work where a short checklist would be enough. |
| Spec Coding | Turn those patterns into copyable templates, criteria, risk registers, and evidence gates that fit existing teams. | Writing educational content without a practical artifact the reader can use. |

## A repo layout that works without buying into any tool

You can adopt the core of SDD without choosing a framework first. Start with a simple repository layout that any coding agent can read and any human can review:

```
/specs
  /active
    refund-retry/
      spec.md
      design.md
      tasks.md
      evidence.md
  /archive
    2026-05-11-refund-retry/
/templates
  feature.spec.md
  api-contract.spec.md
  ai-coding-review.md
/docs
  engineering-principles.md
```

That layout borrows from OpenSpec's change folders, Spec Kit's lifecycle separation, and Superpowers' insistence on planning before execution. It also stays portable. If the team later adopts a tool, the artifacts are already in the right shape.

## How to use these projects as references without copying them

Do not turn your internal process into a clone of a public README. Public tools need generic workflows because they serve many teams. Your team needs a workflow that reflects its actual risk: release cadence, API consumers, test maturity, compliance rules, and how much AI-generated code enters review.

Use the projects as pattern libraries:

- Borrow OpenSpec's change folder idea when a feature crosses multiple artifacts.
- Borrow Superpowers' planning and review discipline when AI agents are allowed to implement tasks.
- Borrow Spec Kit's constitution/spec/plan/tasks sequence when teams need repeatable governance.
- Keep Spec Coding templates as the lightweight entry point when the team needs something useful today.

## Decision guide

Use a lightweight spec packet when the change is narrow, low risk, and can be reviewed in one pull request. Use an OpenSpec-style change folder when the change needs proposal, design, tasks, and archival history. Use a Spec Kit-style lifecycle when the team needs project principles and repeatable planning. Use a Superpowers-style skills workflow when you want the agent to enforce behavior such as brainstorming, TDD, and review before declaring work complete.

The important thing is not to let the workflow become theatrical. A good SDD process should reduce clarification comments, make tests easier to write, and make PR review less subjective. If it only creates more documents, tighten it until every artifact changes a decision or proves a behavior.

## Quick Answers

- **OpenSpec vs GitHub Spec Kit:** both keep implementation behind a written spec, but OpenSpec centers the change folder while Spec Kit centers a repeatable lifecycle.
- **Where Superpowers fits:** it is strongest when AI coding agents need enforced skills, planning, TDD, and verification before they can claim the work is done.
- **Small-team starting point:** begin with a one-page spec packet, then add OpenSpec-style or Spec Kit-style artifacts only when risk justifies the extra structure.

## Worked artifact: one change in three SDD styles

Here is how the same small request changes shape when you borrow from OpenSpec, Superpowers, and Spec Kit. The point is not to copy a tool; it is to choose the smallest artifact that still protects review.

| Input | Artifact choice | Review evidence |
| --- | --- | --- |
| “Let admins refund failed invoices.” | Spec Coding packet: one `spec.md`, task list, acceptance criteria, evidence checklist. | One reviewer can verify policy, idempotency, audit log, and rollback. |
| Refund affects billing API, support console, and ledger export. | OpenSpec-style change folder with proposal, design, task split, and archived decision. | Each touched surface has an owner and a migration note. |
| An agent will implement the tasks. | Superpowers-style skill workflow: clarify, plan, write tests, implement, review. | The agent cannot mark work done before tests and review notes exist. |
| The team wants repeatable governance. | Spec Kit-style constitution, spec, plan, tasks sequence. | Every feature follows the same gates without inventing process each sprint. |