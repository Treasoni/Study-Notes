## ADDED Requirements

### Requirement: Skill filtering configuration
The system SHALL support a `skills` configuration section in `.study-config.yaml` with `include` and `exclude` lists to control which skills are loaded into the system prompt.

#### Scenario: Default behavior (no config)
- **WHEN** `.study-config.yaml` has no `skills` section or both lists are empty
- **THEN** system loads all available skills (current behavior preserved)

#### Scenario: Exclude specific skills
- **WHEN** `skills.exclude` contains `["comet", "opencli-adapter-author"]`
- **THEN** system SHALL NOT load those skills' SKILL.md content into the system prompt

#### Scenario: Include only specific skills
- **WHEN** `skills.include` contains `["collect", "curate", "write", "beautify"]`
- **THEN** system SHALL load only those skills and ignore all others

### Requirement: Skill filtering at Resource Discovery
The system SHALL apply skill filtering during the Resource Discovery phase in CLAUDE.md, after Glob results are obtained but before skills are presented to the user.

#### Scenario: Filtering applied after Glob
- **WHEN**主 Agent executes `Glob .claude/skills/*/SKILL.md` for Resource Discovery
- **THEN** system SHALL filter the results against `skills.include` / `skills.exclude` before processing

#### Scenario: Filtered skills not presented
- **WHEN** a skill is excluded by configuration
- **THEN** system SHALL NOT list it in available skills and SHALL NOT load its SKILL.md content

### Requirement: Skill filtering validation
The system SHALL validate skill filter configuration at startup and warn if excluded skill names do not match any existing skill.

#### Scenario: Invalid exclude name
- **WHEN** `skills.exclude` contains a name that does not match any skill directory
- **THEN** system SHALL log a warning but continue with valid exclusions

#### Scenario: Include references non-existent skill
- **WHEN** `skills.include` contains a name that does not match any skill directory
- **THEN** system SHALL log a warning and skip the missing skill
