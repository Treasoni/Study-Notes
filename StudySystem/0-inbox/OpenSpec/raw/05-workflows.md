Source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md
(also synthesized from https://deepwiki.com/Fission-AI/OpenSpec/3-workflows)

# Workflows

The OPSX (OpenSpec eXperience) Workflow System serves as the core engine of OpenSpec, delivering an action-based paradigm for spec-driven development. It replaces legacy phase-locked approaches with a fluid model where AI agents understand artifact dependencies, real-time project state, and granular creation rules.

## Philosophy: Actions, Not Phases

The transition from legacy OpenSpec to OPSX shifts from "Phase-Locked" to "Action-Based" workflows.

| Aspect | Legacy | OPSX (1.0+) |
|--------|--------|-------------|
| **Structure** | Linear: Proposal -> Apply -> Archive | Fluid: Any action at any time |
| **Instructions** | Hardcoded in TypeScript | Dynamic assembly from config.yaml |
| **Flexibility** | All-or-nothing artifact creation | Incremental creation via /opsx:continue |
| **Customization** | Fixed structure | Schema-driven (schema.yaml) |

### Action Command Mapping

Two primary profiles managed via `openspec config profile`:

1. **Core Profile**: 5 essential workflows — `propose`, `explore`, `apply`, `sync`, `archive`
2. **Custom Profile**: Selection from all 11 available workflows including `new`, `continue`, `ff`, `verify`, `bulk-archive`, `onboard`

## Core Profile Workflow (Quick Path)

The default workflow for most users:

```
/opsx:propose --> /opsx:apply --> /opsx:sync --> /opsx:archive
```

### Step-by-step

1. **Propose** — `/opsx:propose add-dark-mode`
   - AI generates proposal, delta specs, design, and tasks
   - You review and refine artifacts

2. **Apply** — `/opsx:apply`
   - AI works through tasks.md step by step
   - Writes code, checks off items
   - Can resume if interrupted

3. **Sync** — `/opsx:sync` (optional)
   - Merge delta specs into main specs
   - Useful for checkpoint commits

4. **Archive** — `/opsx:archive`
   - Merges remaining deltas
   - Moves change to archive/
   - Preserves all artifacts for audit

## Expanded Workflow (Custom Profile)

For more granular control:

```
/opsx:new --> /opsx:ff or /opsx:continue --> /opsx:apply --> /opsx:verify --> /opsx:archive
```

## Artifact Graph and State Machine

Every artifact in a change directory (e.g., `proposal`, `specs`, `tasks`) exists in one of three states:

- **BLOCKED** — Dependencies are not yet met
- **READY** — All dependencies exist, artifact can be created
- **DONE** — File exists at output path

### State Transitions

```
[*] --> BLOCKED: Artifact defined in schema
BLOCKED --> READY: All dependencies exist
READY --> DONE: File created at outputPath
DONE --> READY: File deleted
DONE --> [*]: Change Archived
```

The `openspec status` command provides this state to AI agents, allowing them to intelligently suggest the next step.

## Dynamic Instruction Assembly

OPSX instructions are assembled from three layers:

1. **Context**: Project-wide background (tech stack, conventions) from `openspec/config.yaml`
2. **Rules**: Artifact-specific constraints, e.g. "Use SHALL/MUST for requirements"
3. **Template**: The structural markdown that the AI must populate, loaded from the schema directory

This assembly is formatted for the agent using XML-like tags to separate concerns.

## Workflow Profiles

### Core Profile Commands

| Command | Purpose |
|---|---|
| `/opsx:propose` | Create change + all planning artifacts in one step |
| `/opsx:explore` | Think through ideas before committing to a change |
| `/opsx:apply` | Implement tasks from the change |
| `/opsx:sync` | Merge delta specs into main specs |
| `/opsx:archive` | Archive a completed change |

### Expanded Workflow Commands

| Command | Purpose |
|---|---|
| `/opsx:new` | Start a new change scaffold |
| `/opsx:continue` | Create the next artifact based on dependencies |
| `/opsx:ff` | Fast-forward: create all planning artifacts at once |
| `/opsx:verify` | Validate implementation matches artifacts |
| `/opsx:bulk-archive` | Archive multiple changes at once |
| `/opsx:onboard` | Guided tutorial through the complete workflow |

## When to Use Each Workflow

### Quick change (e.g., fix a small bug)
```
/opsx:propose fix-login-validation --> /opsx:apply --> /opsx:archive
```

### Complex feature (needs careful planning)
```
/opsx:new add-payment-gateway
/opsx:continue  (review proposal)
/opsx:continue  (review specs)
/opsx:continue  (review design)
/opsx:continue  (review tasks)
/opsx:apply     (implement)
/opsx:verify    (validate)
/opsx:archive   (complete)
```

### Fuzzy requirements (explore first)
```
/opsx:explore "best approach for auth"
--> user discusses options with AI
/opsx:propose implement-jwt-auth
/opsx:apply
/opsx:archive
```

### Parallel changes
```
/opsx:propose feature-a
/opsx:propose feature-b
/opsx:apply feature-a
/opsx:apply feature-b
/opsx:bulk-archive feature-a feature-b
```

## Integration and Tooling

The workflow system is exposed to AI tools through a registry of adapters that transform generic templates into tool-specific formats:

- **Skill Generation**: `openspec init` creates skills in directories like `.claude/skills/` or `.cursor/skills/`
- **Instruction Generation**: The `openspec instructions` command provides raw material for these skills to execute
- **Status Reporting**: The `openspec status` command allows agents to determine the current progress of a change
