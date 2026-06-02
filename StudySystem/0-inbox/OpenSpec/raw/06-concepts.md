Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md

# Concepts

This guide explains the core ideas behind OpenSpec and how they fit together.

## Philosophy

OpenSpec is built around four principles:

```
fluid not rigid — no phase gates, work on what makes sense
iterative not waterfall — learn as you build, refine as you go
easy not complex — lightweight setup, minimal ceremony
brownfield-first — works with existing codebases, not just greenfield
```

### Why These Principles Matter

**Fluid not rigid.** Traditional spec systems lock you into phases. OpenSpec is more flexible — you can create artifacts in any order that makes sense.

**Iterative not waterfall.** Requirements change and understanding deepens. OpenSpec embraces this reality.

**Easy not complex.** Some spec frameworks require extensive setup. OpenSpec stays out of your way. Initialize in seconds, start working immediately.

**Brownfield-first.** Most software work modifies existing systems. OpenSpec's delta-based approach makes it easy to specify changes to existing behavior.

## The Big Picture

OpenSpec organizes work into two main areas:

```
openspec/
├── specs/          # Source of truth: How your system currently works
└── changes/        # Proposed modifications: Each change = one folder
    └── <name>/
        ├── proposal.md
        ├── specs/      # Delta specs
        ├── design.md
        └── tasks.md
```

**Specs** are the source of truth — they describe how your system currently behaves.

**Changes** are proposed modifications — they live in separate folders until you're ready to merge them.

This separation lets you work on multiple changes in parallel without conflicts. Review a change before it affects the main specs. When archived, deltas merge cleanly into the source of truth.

## Coordination Workspaces

Workspace support is in beta. A workspace provides machine-local coordination views over linked repos and folders for cross-repo work.

The workspace mental model:

```
workspace = private local view over context stores, initiatives, repos, and folders
context store = durable shared context container
initiative = durable coordination context inside a context store
link = a stable name for a repo or folder the workspace can resolve locally
change = one planned piece of work; implementation belongs in the owning repo
```

A workspace has a different shape from a repo-local project:

```
~/.local/share/openspec/workspaces/<workspace-name>/
├── workspace.yaml   # Private local view record
├── AGENTS.md        # Generated runtime guidance
└── <workspace-name>.code-workspace  # Generated editor workspace file
```

## Specs

Specs describe your system's behavior using structured requirements and scenarios.

### Structure

```
openspec/specs/
├── auth/           # Spec: Authentication behavior
├── payments/       # Spec: Payment processing
├── notifications/  # Spec: Notification system
└── ui/             # Spec: UI behavior and themes
```

Organize specs by domain — logical groupings for your system:
- **By feature area:** `auth/`, `payments/`, `search/`
- **By component:** `api/`, `frontend/`, `workers/`
- **By bounded context:** `ordering/`, `fulfillment/`, `inventory/`

### Spec Format

A spec contains requirements, and each requirement has scenarios:

```markdown
# Auth Specification

## Purpose
Authentication and session management for the application.

## Requirements

### Requirement: User Authentication
The system SHALL issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard

#### Scenario: Invalid credentials
- GIVEN invalid credentials
- WHEN the user submits login form
- THEN an error message is displayed
- AND no token is issued
```

**Key elements:**

| Element | Purpose |
|---------|---------|
| `## Purpose` | High-level description of this spec's domain |
| `### Requirement:` | A specific behavior the system must have |
| `#### Scenario:` | A concrete example of the requirement in action |
| SHALL/MUST/SHOULD | RFC 2119 keywords indicating requirement strength |

### What a Spec Is (and Is Not)

A spec is a **behavior contract**, not an implementation plan.

Good spec content:
- Observable behavior users or downstream systems rely on
- Inputs, outputs, and error conditions
- External constraints (security, privacy, reliability, compatibility)
- Scenarios that can be tested or explicitly validated

Avoid in specs:
- Internal class/function names
- Library or framework choices
- Step-by-step implementation details
- Detailed execution plans (those belong in `design.md` or `tasks.md`)

### Keep It Lightweight: Progressive Rigor

**Lite spec (default):**
- Short behavior-first requirements
- Clear scope and non-goals
- A few concrete acceptance checks

**Full spec (for higher risk):**
- Cross-team or cross-repo changes
- API/contract changes, migrations, security/privacy concerns
- Changes where ambiguity is likely to cause expensive rework

### Human + Agent Collaboration

1. Human provides intent, context, and constraints.
2. Agent converts this into behavior-first requirements and scenarios.
3. Agent keeps implementation detail in `design.md` and `tasks.md`, not `spec.md`.
4. Validation confirms structure and clarity before implementation.

## Changes

A change is a proposed modification to your system, packaged as a folder with everything needed to understand and implement it.

### Change Structure

```
openspec/changes/add-dark-mode/
├── proposal.md        # Why and what
├── design.md          # How (technical approach)
├── tasks.md           # Implementation checklist
├── .openspec.yaml     # Change metadata (optional)
└── specs/             # Delta specs
    └── ui/
        └── spec.md    # What's changing in ui/spec.md
```

### Why Changes Are Folders

1. **Everything together.** Proposal, design, tasks, and specs live in one place.
2. **Parallel work.** Multiple changes can exist simultaneously without conflicts.
3. **Clean history.** When archived, changes move to `changes/archive/` with full context preserved.
4. **Review-friendly.** A change folder is easy to review.

## Artifacts

Artifacts are the documents within a change that guide the work.

### The Artifact Flow

```
proposal --> specs --> design --> tasks --> implement
  |           |          |          |
 why        what       how        steps
+scope     changes   approach    to take
```

### Artifact Types

#### Proposal (proposal.md)

The proposal captures **intent**, **scope**, and **approach** at a high level.

```markdown
# Proposal: Add Dark Mode

## Intent
Users have requested a dark mode option to reduce eye strain
during nighttime usage and match system preferences.

## Scope
In scope:
- Theme toggle in settings
- System preference detection
- Persist preference in localStorage

Out of scope:
- Custom color themes (future work)
- Per-page theme overrides

## Approach
Use CSS custom properties for theming with a React context
for state management.
```

#### Design (design.md)

The design captures **technical approach** and **architecture decisions**.

```markdown
# Design: Add Dark Mode

## Technical Approach
Theme state managed via React Context to avoid prop drilling.
CSS custom properties enable runtime switching without class toggling.

## Architecture Decisions

### Decision: Context over Redux
Using React Context for theme state because:
- Simple binary state (light/dark)
- No complex state transitions
- Avoids adding Redux dependency
```

#### Tasks (tasks.md)

Tasks are the **implementation checklist** — concrete steps with checkboxes.

```markdown
# Tasks

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for colors
- [ ] 1.3 Implement localStorage persistence

## 2. UI Components
- [ ] 2.1 Create ThemeToggle component
- [ ] 2.2 Add toggle to settings page
```

**Task best practices:**
- Group related tasks under headings
- Use hierarchical numbering (1.1, 1.2, etc.)
- Keep tasks small enough to complete in one session
- Check tasks off as you complete them

## Delta Specs

Delta specs are the key concept that makes OpenSpec work for brownfield development. They describe **what's changing** rather than restating the entire spec.

### The Format

```markdown
# Delta for Auth

## ADDED Requirements

### Requirement: Two-Factor Authentication
The system MUST support TOTP-based two-factor authentication.

#### Scenario: 2FA enrollment
- GIVEN a user without 2FA enabled
- WHEN the user enables 2FA in settings
- THEN a QR code is displayed for authenticator app setup

## MODIFIED Requirements

### Requirement: Session Expiration
The system MUST expire sessions after 15 minutes of inactivity.
(Previously: 30 minutes)

## REMOVED Requirements

### Requirement: Remember Me
(Deprecated in favor of 2FA.)
```

### Delta Sections

| Section | Meaning | What Happens on Archive |
|---------|---------|------------------------|
| ADDED | New requirements | Added to the main spec |
| MODIFIED | Existing requirements changing | Updated in the main spec |
| REMOVED | Requirements being eliminated | Deleted from the main spec |

### Why Deltas Instead of Full Specs

- **Less redundancy** — only describe what's different
- **Clearer review** — reviewers see exactly what changed
- **Easier merging** — on archive, changes apply cleanly to the source of truth
- **Brownfield-friendly** — works naturally with existing behavior

## Schemas

Schemas define valid structures for artifacts and specs. They enforce consistency and provide guardrails.

### How Schemas Work

Schemas are applied per subdirectory. Custom schemas can be specified via `.openspec.yaml` in any spec or change subdirectory.

### Built-in Schemas

OpenSpec includes default schemas for `spec.md`, `proposal.md`, `design.md`, and `tasks.md`. These enforce the heading hierarchy (Purpose -> Requirements -> Scenarios) and other structural conventions.

### Custom Schemas

Teams can define their own schemas for domain-specific needs (e.g., an API endpoint schema for an `api/spec.md` that requires path, method, request/response shapes).

## Archive

Archiving completes a change, merging its deltas into the main specs and preserving the full change folder for future reference.

### What Happens When You Archive

1. Delta specs from the change are applied to the main specs (ADDED -> added, MODIFIED -> updated, REMOVED -> deleted).
2. The change folder moves from `openspec/changes/<name>/` to `openspec/changes/archive/<name>/`.
3. All artifacts (proposal, design, tasks) are preserved for historical context.

### Why Archive Matters

- **Auditable history** — every change is preserved with full context
- **Clean workspace** — active changes are what's in progress
- **Traceability** — look up any archived change to understand why a spec says what it says

## Glossary

| Term | Definition |
|------|-----------|
| **Spec** | A behavior contract describing how the system currently works |
| **Change** | A proposed modification packaged as a folder with artifacts and deltas |
| **Delta spec** | A spec describing what's changing (ADDED/MODIFIED/REMOVED) |
| **Artifact** | A document within a change (proposal, design, tasks) |
| **Archive** | The process of completing a change and merging deltas into main specs |
| **Workspace** | A machine-local coordination view over linked repos/folders |
| **Context store** | A durable shared context container for cross-repo coordination |
| **Initiative** | A durable coordination context inside a context store |
| **Link** | A stable name mapping to a repo or folder path |
