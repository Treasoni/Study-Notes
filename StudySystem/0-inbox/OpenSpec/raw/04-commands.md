Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md

# Commands Reference

Reference for OpenSpec's slash commands. These commands are invoked in your AI coding assistant's chat interface (e.g., Claude Code, Cursor, Windsurf).

For workflow patterns and when to use each command, see [Workflows](workflows.md). For CLI commands, see [CLI Reference](cli.md).

## Quick Reference

### Default Quick Path (`core` profile)

| Command | Purpose |
|---|---|
| `/opsx:propose` | Create a change and generate planning artifacts in one step |
| `/opsx:explore` | Think through ideas before committing to a change |
| `/opsx:apply` | Implement tasks from the change |
| `/opsx:sync` | Merge delta specs into main specs |
| `/opsx:archive` | Archive a completed change |

### Expanded Workflow Commands (custom workflow selection)

| Command | Purpose |
|---|---|
| `/opsx:new` | Start a new change scaffold |
| `/opsx:continue` | Create the next artifact based on dependencies |
| `/opsx:ff` | Fast-forward: create all planning artifacts at once |
| `/opsx:verify` | Validate implementation matches artifacts |
| `/opsx:bulk-archive` | Archive multiple changes at once |
| `/opsx:onboard` | Guided tutorial through the complete workflow |

## Command Reference

### `/opsx:propose`

Create a new change and generate planning artifacts in one step. This is the default start command in the `core` profile.

**Syntax:** `/opsx:propose [change-name-or-description]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name-or-description` | No | Kebab-case name or plain-language change description |

**What it does:**
- Creates `openspec/changes/<change-name>/`
- Generates artifacts needed before implementation (for `spec-driven`: proposal, specs, design, tasks)
- Stops when the change is ready for `/opsx:apply`

**Example:**
```
You: /opsx:propose add-dark-mode

AI: Created openspec/changes/add-dark-mode/
 ✓ proposal.md
 ✓ specs/ui/spec.md
 ✓ design.md
 ✓ tasks.md
 Ready for implementation. Run /opsx:apply.
```

**Tips:**
- Use this for the fastest end-to-end path
- If you want step-by-step artifact control, enable expanded workflows and use `/opsx:new` + `/opsx:continue`

---

### `/opsx:explore`

Think through ideas, investigate problems, and clarify requirements before committing to a change.

**Syntax:** `/opsx:explore [topic]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `topic` | No | What you want to explore or investigate |

**What it does:**
- Opens an exploratory conversation with no structure required
- Investigates the codebase to answer questions
- Compares options and approaches
- Creates visual diagrams to clarify thinking
- Can transition to `/opsx:propose` (default) or `/opsx:new` (expanded workflow) when insights crystallize

**Example:**
```
You: /opsx:explore

AI: What would you like to explore?

You: How should we handle authentication for the mobile app?

AI: Let me investigate your current auth setup...
 [Analyzes codebase]

 I see you're using session-based auth for the web app.
 For mobile, we have three main options:
 1. JWT tokens (stateless, works offline)
 2. OAuth2 (if you need third-party login)
 3. Extend current sessions (simpler, but requires connectivity)

 Your API already has CORS configured. Which direction interests you?

You: Let's go with JWT. Can we start a change for that?

AI: Ready when you are. Run /opsx:propose add-jwt-auth to begin.
```

**Tips:**
- Use when requirements are unclear or you need to investigate
- No artifacts are created during exploration
- Good for comparing multiple approaches before deciding
- Can read files and search the codebase

---

### `/opsx:new`

Start a new change scaffold. Creates the change folder and waits for you to generate artifacts with `/opsx:continue` or `/opsx:ff`.

This command is part of the expanded workflow set (not included in the default `core` profile).

**Syntax:** `/opsx:new [change-name] [--schema <schema-name>]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name` | No | Name for the change folder (prompted if not provided) |
| `--schema` | No | Workflow schema to use (default: from config or `spec-driven`) |

**What it does:**
- Creates `openspec/changes/<change-name>/` directory
- Creates `.openspec.yaml` metadata file in the change folder
- Shows the first artifact template ready for creation
- Prompts for change name and schema if not provided

**What it creates:**
```
openspec/changes/<change-name>/
└── .openspec.yaml   # Change metadata (schema, created date)
```

**Example:**
```
You: /opsx:new add-dark-mode

AI: Created openspec/changes/add-dark-mode/
 Schema: spec-driven

 Ready to create: proposal
 Use /opsx:continue to create it, or /opsx:ff to create all artifacts.
```

---

### `/opsx:continue`

Create the next artifact in the dependency chain. Creates one artifact at a time for incremental progress.

**Syntax:** `/opsx:continue [change-name]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name` | No | Which change to continue (inferred from context if not provided) |

**What it does:**
- Queries the artifact dependency graph
- Shows which artifacts are ready vs blocked
- Creates the first ready artifact
- Reads dependency files for context
- Shows what becomes available after creation

**Example:**
```
You: /opsx:continue

AI: Change: add-dark-mode

 Artifact status:
 ✓ proposal (done)
 ◆ specs (ready)
 ◆ design (ready)
 ○ tasks (blocked - needs: specs)

 Creating specs...

 [Reads proposal.md, creates specs based on requirements]

 ✓ Created openspec/changes/add-dark-mode/specs/ui/spec.md

 Now available: tasks
 Run /opsx:continue to create the next artifact.
```

---

### `/opsx:ff`

Fast-forward through artifact creation. Creates all planning artifacts at once.

**Syntax:** `/opsx:ff [change-name]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name` | No | Which change to fast-forward (inferred from context if not provided) |

**What it does:**
- Creates all artifacts in dependency order
- Tracks progress via todo list
- Stops when all `apply-required` artifacts are complete
- Reads each dependency before creating the next artifact

**Example:**
```
You: /opsx:ff add-dark-mode

AI: Fast-forwarding add-dark-mode...

 ✓ Creating proposal.md
 ✓ Creating specs/ui/spec.md
 ✓ Creating design.md
 ✓ Creating tasks.md

 All planning artifacts complete!
 Ready for implementation. Run /opsx:apply to begin.
```

---

### `/opsx:apply`

Implement tasks from the change. Works through the task list, writing code and checking off items.

**Syntax:** `/opsx:apply [change-name]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name` | No | Which change to implement (inferred from context if not provided) |

**What it does:**
- Reads `tasks.md` and identifies incomplete tasks
- Works through tasks one by one
- Writes code, creates files, runs tests as needed
- Marks tasks complete with checkboxes `[x]`

**Example:**
```
You: /opsx:apply

AI: Implementing add-dark-mode...

 Reading tasks.md:
 - [ ] 1.1 Create ThemeContext
 - [ ] 1.2 Add CSS custom properties
 - [ ] 1.3 Implement localStorage persistence

 Working on 1.1: Create ThemeContext...
 [Creates src/context/ThemeContext.tsx]

 ✓ 1.1 Complete
 ...
```

**Tips:**
- Can resume where you left off if interrupted
- Use for parallel changes by specifying the change name
- Completion state is tracked in `tasks.md` checkboxes

---

### `/opsx:verify`

Validate that implementation matches your change artifacts. Checks completeness, correctness, and coherence.

**Syntax:** `/opsx:verify [change-name]`

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `change-name` | No | Which change to verify (inferred from context if not provided) |

**Verification dimensions:**

| Dimension | What it validates |
|---|---|
| **Completeness** | All tasks done, all requirements implemented, scenarios covered |
| **Correctness** | Implementation matches spec intent, edge cases handled |
| **Coherence** | Design decisions reflected in code, patterns consistent |

**Example:**
```
You: /opsx:verify

AI: Verifying add-dark-mode...

 COMPLETENESS
 ✓ All 8 tasks in tasks.md are checked
 ✓ All requirements in specs have corresponding code
 ⚠ Scenario "System preference detection" has no test coverage

 CORRECTNESS
 ✓ Implementation matches spec intent
 ✓ Edge cases from scenarios are handled

 COHERENCE
 ✓ Design decisions reflected in code structure
 ⚠ Design mentions "CSS variables" but implementation uses Tailwind classes

 SUMMARY
 ─────────────────────────────
 Critical issues: 0
 Warnings: 2
 Ready to archive: Yes (with warnings)
```

---

### `/opsx:sync`

Optional command. Merge delta specs from a change into main specs. Archive will prompt to sync if needed, so you typically don't need to run this manually.

**Syntax:** `/opsx:sync [change-name]`

**What it does:**
- Reads delta specs from change folder
- Parses ADDED/MODIFIED/REMOVED sections
- Merges changes into main `openspec/specs/` directory
- Preserves existing content not mentioned in delta
- Does not archive the change (remains active)

---

### `/opsx:archive`

Archive a completed change. Finalizes the change and moves it to the archive folder.

**Syntax:** `/opsx:archive [change-name]`

**What it does:**
- Checks artifact completion status
- Checks task completion (warns if incomplete)
- Offers to sync delta specs if not already synced
- Moves change folder to `openspec/changes/archive/YYYY-MM-DD-<name>/`
- Preserves all artifacts for audit trail

**CLI options:** `-y, --yes` (skip prompts), `--skip-specs`, `--no-validate`

---

### `/opsx:bulk-archive`

Archive multiple completed changes at once. Handles spec conflicts between changes.

**Syntax:** `/opsx:bulk-archive [change-names...]`

**What it does:**
- Lists all completed changes
- Validates each change before archiving
- Detects spec conflicts across changes
- Resolves conflicts by checking what's actually implemented
- Archives in chronological order

---

### `/opsx:onboard`

Guided onboarding through the complete OpenSpec workflow. An interactive tutorial using your actual codebase.

**Syntax:** `/opsx:onboard`

**Phases:**
1. Welcome and codebase analysis
2. Finding an improvement opportunity
3. Creating a change (`/opsx:new`)
4. Writing the proposal
5. Creating specs
6. Writing the design
7. Creating tasks
8. Implementing tasks (`/opsx:apply`)
9. Verifying implementation
10. Archiving the change
11. Summary and next steps

Takes 15-30 minutes to complete.

## Command Syntax by AI Tool

Different AI tools use slightly different command syntax:

| Tool | Syntax Example |
|---|---|
| Claude Code | `/opsx:propose`, `/opsx:apply` |
| Cursor | `/opsx-propose`, `/opsx-apply` |
| Windsurf | `/opsx-propose`, `/opsx-apply` |
| Copilot (IDE) | `/opsx-propose`, `/opsx-apply` |
| Kimi CLI | `/skill:openspec-propose`, `/skill:openspec-apply-change` |
| Trae | `/openspec-propose`, `/openspec-apply-change` |

## Legacy Commands

These commands use the older "all-at-once" workflow. They still work but OPSX commands are recommended.

| Command | What it does |
|---|---|
| `/openspec:proposal` | Create all artifacts at once |
| `/openspec:apply` | Implement the change |
| `/openspec:archive` | Archive the change |

## Troubleshooting

### "Change not found"
The command couldn't identify which change to work on.

**Solutions:**
- Specify the change name explicitly: `/opsx:apply add-dark-mode`
- Check that the change folder exists: `openspec list`
- Verify you're in the right project directory

### "No artifacts ready"
All artifacts are either complete or blocked by missing dependencies.

**Solutions:**
- Run `openspec status --change <name>` to see what's blocking
- Check if required artifacts exist
- Create missing dependency artifacts first

### "Schema not found"
The specified schema doesn't exist.

**Solutions:**
- List available schemas: `openspec schemas`
- Check spelling of schema name
- Create the schema if it's custom: `openspec schema init <name>`

### Commands not recognized
The AI tool doesn't recognize OpenSpec commands.

**Solutions:**
- Ensure OpenSpec is initialized: `openspec init`
- Regenerate skills: `openspec update`
- Check that `.claude/skills/` directory exists (for Claude Code)
- Restart your AI tool to pick up new skills
