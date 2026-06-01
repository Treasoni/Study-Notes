## MODIFIED Requirements

### Requirement: Main Agent SHALL coordinate subagents without executing heavy computation

The system SHALL use a Hub-and-Spoke architecture where Main Agent acts as coordinator and delegates computation-heavy tasks to subagents.

#### Scenario: Collect phase delegation
- **WHEN** user confirms collect phase start
- **THEN** Main Agent SHALL spawn a Collect Subagent with the topic and source list
- **AND** Collect Subagent SHALL read raw files, extract key information, and write to `{SYSTEM_ROOT}/0-inbox/{topic}/raw/`
- **AND** Main Agent SHALL NOT read raw files directly

#### Scenario: Curate phase delegation
- **WHEN** user confirms curate phase start
- **THEN** Main Agent SHALL spawn a Curate Subagent with the inbox path
- **AND** Curate Subagent SHALL score sources on 4 dimensions (authority, freshness, completeness, readability), deduplicate, classify, and write to `{SYSTEM_ROOT}/1-curated/{topic}/`
- **AND** Main Agent SHALL NOT perform scoring or classification directly

### Requirement: Subagents SHALL operate in isolated context windows

Each subagent SHALL have its own context window, receiving only the necessary inputs and returning structured outputs.

#### Scenario: Subagent context isolation
- **WHEN** Main Agent spawns a subagent
- **THEN** subagent SHALL receive only: topic, input paths, output paths, and task description
- **AND** subagent SHALL NOT have access to Main Agent's conversation history
- **AND** subagent's context usage SHALL NOT exceed 8k tokens

### Requirement: Subagent definitions SHALL include global instruction exemptions

Each subagent definition file SHALL include a 全局指令豁免 section that explicitly exempts the subagent from Main Agent initialization steps (Resource Discovery, Pre-Task Initialization, Mandatory Triggered Reads). This section SHALL reference a shared source to avoid duplication across 4 agent files.

#### Scenario: Subagent skips global init
- **WHEN** a subagent is spawned by Main Agent
- **THEN** subagent SHALL NOT execute Glob for skills/agents/templates
- **AND** subagent SHALL NOT Read TODO.md or .obsidian-config.md
- **AND** subagent SHALL NOT follow Mandatory Triggered Reads table

#### Scenario: Exemption block is maintainable
- **WHEN** the exemption list needs to be updated
- **THEN** all 4 agent definition files SHALL contain a comment referencing the shared source (`docs/todo-state-machine.md` or agent definition template) to facilitate synchronized updates
