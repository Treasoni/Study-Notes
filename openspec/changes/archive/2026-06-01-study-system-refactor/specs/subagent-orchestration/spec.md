## ADDED Requirements

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
- **AND** Curate Subagent SHALL score sources on 4 dimensions, deduplicate, classify, and write to `{SYSTEM_ROOT}/1-curated/{topic}/`
- **AND** Main Agent SHALL NOT perform scoring or classification directly

### Requirement: Subagents SHALL operate in isolated context windows

Each subagent SHALL have its own context window, receiving only the necessary inputs and returning structured outputs.

#### Scenario: Subagent context isolation
- **WHEN** Main Agent spawns a subagent
- **THEN** subagent SHALL receive only: topic, input paths, output paths, and task description
- **AND** subagent SHALL NOT have access to Main Agent's conversation history
- **AND** subagent's context usage SHALL NOT exceed 8k tokens

### Requirement: Main Agent SHALL handle subagent errors gracefully

The system SHALL handle subagent failures without losing user progress.

#### Scenario: Subagent timeout
- **WHEN** a subagent does not complete within 5 minutes
- **THEN** Main Agent SHALL terminate the subagent
- **AND** Main Agent SHALL inform user of timeout
- **AND** Main Agent SHALL offer retry or manual execution options

#### Scenario: Subagent output validation
- **WHEN** a subagent completes execution
- **THEN** Main Agent SHALL verify output files exist and are non-empty
- **AND** if validation fails, Main Agent SHALL inform user and offer retry

### Requirement: Subagents SHALL produce structured outputs

Subagents SHALL return results in a consistent format that Main Agent can parse.

#### Scenario: Successful subagent output
- **WHEN** a subagent completes successfully
- **THEN** subagent SHALL write a status file `{output_path}/.status.json` with:
  - `status`: "success" | "partial" | "failed"
  - `summary`: brief description of what was done
  - `artifacts`: list of created files
  - `context_usage`: estimated token count used

#### Scenario: Partial completion
- **WHEN** a subagent completes some but not all tasks
- **THEN** subagent SHALL set status to "partial"
- **AND** subagent SHALL list completed and pending items in summary
- **AND** Main Agent SHALL offer to continue from last checkpoint
