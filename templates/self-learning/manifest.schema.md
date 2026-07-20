# Agent Component Manifest

`manifest.yaml` is the registration contract for platform components. It keeps
discovery, versioning, permissions, dependencies, and events in one place while
letting each component keep its own native implementation file.

This template uses:

```yaml
apiVersion: agent-platform/v1alpha1
kind: Skill
```

Supported `kind` values:

- `Workflow`: ordered orchestration that connects skills, hooks, and subagents.
- `Skill`: reusable instruction package, usually backed by `SKILL.md`.
- `Subagent`: delegated agent profile with an isolated prompt and tool contract.
- `Hook`: event-triggered automation such as `SessionStart`.

## Common Shape

```yaml
apiVersion: agent-platform/v1alpha1
kind: Skill

metadata:
  name: component-name
  version: 0.1.0
  description: Short user-facing capability description.
  tags:
    - self-learning

spec:
  runtime: markdown-skill
  entrypoint: SKILL.md

permissions:
  filesystem:
    read:
      - ".learnings/**"
    write:
      - ".learnings/**"
  network: false
  tools:
    - file.edit

dependencies:
  skills: []
  workflows: []
  subagents: []
  hooks: []

events:
  triggers:
    - onDemand

compatibility:
  platforms:
    - codex
    - claude-code
```

## Kind Specific Fields

### Workflow

Required:

- `spec.runtime`
- `spec.steps`

Each step must include `id` and either `uses` or `action`.

```yaml
spec:
  runtime: declarative-workflow
  steps:
    - id: record-digest
      uses: skill:digest
    - id: repair-recurring-errors
      uses: skill:maintain-learnings
      when: learnings.recurring_errors
```

### Skill

Required:

- `spec.runtime`
- `spec.entrypoint`

Recommended:

- `spec.activation.description`
- `spec.inputs`
- `spec.outputs`

### Subagent

Required:

- `spec.runtime`
- `spec.entrypoint`

Recommended:

- `spec.model`
- `spec.delegation`
- `spec.tools`

### Hook

Required:

- `spec.runtime`
- `spec.entrypoint`
- `spec.event`

Recommended:

- `spec.blocking`
- `spec.timeoutSeconds`

## Validation

After installing the template in a target project, validate component manifests:

```bash
python3 .agents/skills/maintain-learnings/scripts/manifest_registry.py --root . --scan .agents --scan .codex/hooks
```

For Claude Code side:

```bash
python3 .claude/skills/maintain-learnings/scripts/manifest_registry.py --root . --scan .claude --scan .claude/hooks
```

