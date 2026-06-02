Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md

# Getting Started Guide

This guide covers how OpenSpec works after installation and initialization. For installation steps, see the main README.

## How It Works

OpenSpec facilitates agreement between a developer and their AI coding assistant on what to build "before any code is written."

**Default quick path (core profile):**

```
/opsx:propose --> /opsx:apply --> /opsx:sync --> /opsx:archive
```

**Expanded path (custom workflow selection):**

```
/opsx:new --> /opsx:ff or /opsx:continue --> /opsx:apply --> /opsx:verify --> /opsx:archive
```

The default global profile is `core`, which bundles `propose`, `explore`, `apply`, `sync`, and `archive`. Enabling the expanded workflow commands requires `openspec config profile` followed by `openspec update`.

## What OpenSpec Creates

After `openspec init`, the project structure looks like this:

```
openspec/
├── specs/              # Source of truth (your system's behavior)
│   └── <domain>/
│       └── spec.md
├── changes/            # Proposed updates (one folder per change)
│   └── <change-name>/
│       ├── proposal.md
│       ├── design.md
│       ├── tasks.md
│       └── specs/      # Delta specs (what's changing)
│           └── <domain>/
│               └── spec.md
└── config.yaml         # Project configuration (optional)
```

**Two key directories:**

- **`specs/`** — The source of truth describing current system behavior, organized by domain (e.g., `specs/auth/`, `specs/payments/`).
- **`changes/`** — Proposed modifications each get their own folder with all related artifacts. Completed changes have their specs merged into the main `specs/` directory.

## Understanding Artifacts

Each change folder contains these artifacts:

| Artifact | Purpose |
|----------|---------|
| `proposal.md` | The "why" and "what" — captures intent, scope, and approach |
| `specs/` | Delta specs showing ADDED/MODIFIED/REMOVED requirements |
| `design.md` | The "how" — technical approach and architecture decisions |
| `tasks.md` | Implementation checklist with checkboxes |

**Artifacts build on each other:**

```
proposal --> specs --> design --> tasks --> implement
   ^           ^          ^                    |
   |           |          |                    |
   +-----------+----------+--------------------+
            update as you learn
```

The guide notes that you can "go back and refine earlier artifacts as you learn more during implementation."

## How Delta Specs Work

Delta specs represent the core concept in OpenSpec, showing what changes relative to current specs.

### The Format

Delta specs use sections to indicate the type of change:

```markdown
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

#### Scenario: Idle timeout
- GIVEN an authenticated session
- WHEN 30 minutes pass without activity
- THEN the session is invalidated

## REMOVED Requirements

### Requirement: Remember Me
(Deprecated in favor of 2FA)
```

### What Happens on Archive

When archiving a change:

1. **ADDED** requirements get appended to the main spec
2. **MODIFIED** requirements replace the existing version
3. **REMOVED** requirements are deleted from the main spec

The change folder moves to `openspec/changes/archive/` for audit history.

## Example: Your First Change

The guide walks through adding dark mode to an application.

### 1. Start the Change (Default)

```
You: /opsx:propose add-dark-mode

AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — why we're doing this, what's changing
     ✓ specs/       — requirements and scenarios
     ✓ design.md    — technical approach
     ✓ tasks.md     — implementation checklist
     Ready for implementation!
```

With the expanded workflow profile enabled, this can be done as two steps: `/opsx:new` then `/opsx:ff` (or `/opsx:continue` incrementally).

### 2. What Gets Created

**proposal.md** captures the intent:

```markdown
# Proposal: Add Dark Mode

## Intent
Users have requested a dark mode option to reduce eye strain
during nighttime usage.

## Scope
- Add theme toggle in settings
- Support system preference detection
- Persist preference in localStorage

## Approach
Use CSS custom properties for theming with a React context
for state management.
```

**specs/ui/spec.md** shows the delta with new requirements:

```markdown
# Delta for UI

## ADDED Requirements

### Requirement: Theme Selection
The system SHALL allow users to choose between light and dark themes.

#### Scenario: Manual toggle
- GIVEN a user on any page
- WHEN the user clicks the theme toggle
- THEN the theme switches immediately
- AND the preference persists across sessions

#### Scenario: System preference
- GIVEN a user with no saved preference
- WHEN the application loads
- THEN the system's preferred color scheme is used
```

**tasks.md** provides the implementation checklist:

```markdown
# Tasks

## 1. Theme Infrastructure
- [ ] 1.1 Create ThemeContext with light/dark state
- [ ] 1.2 Add CSS custom properties for colors
- [ ] 1.3 Implement localStorage persistence

## 2. UI Components
- [ ] 2.1 Create ThemeToggle component
- [ ] 2.2 Add toggle to settings page
- [ ] 2.3 Update Header to include quick toggle

## 3. Styling
- [ ] 3.1 Define dark theme color palette
- [ ] 3.2 Update components to use CSS variables
```

### 3. Implement

```
You: /opsx:apply

AI:  Working through tasks...
     ✓ 1.1 Created ThemeContext with light/dark state
     ✓ 1.2 Added CSS custom properties to globals.css
     ✓ 1.3 Implemented localStorage persistence
     ✓ 2.1 Created ThemeToggle component
     ...
     All tasks complete!
```

During implementation, if the design needs adjustment, the guide says to "just update the artifact and continue."

### 4. Archive

```
You: /opsx:archive

AI:  Archiving add-dark-mode...
     ✓ Merged specs into openspec/specs/ui/spec.md
     ✓ Moved to openspec/changes/archive/2025-01-24-add-dark-mode/
     Done! Ready for the next feature.
```

The delta specs then become part of the main specs, documenting the system's behavior.

## Verifying and Reviewing

Use the CLI to inspect changes:

```bash
# List active changes
openspec list

# View change details
openspec show add-dark-mode

# Validate spec formatting
openspec validate add-dark-mode

# Interactive dashboard
openspec view
```

## Next Steps

The guide points to four follow-up resources:

- **[Workflows](workflows.md)** — "Common patterns and when to use each command"
- **[Commands](commands.md)** — "Full reference for all slash commands"
- **[Concepts](concepts.md)** — "Deeper understanding of specs, changes, and schemas"
- **[Customization](customization.md)** — "Make OpenSpec work your way"
