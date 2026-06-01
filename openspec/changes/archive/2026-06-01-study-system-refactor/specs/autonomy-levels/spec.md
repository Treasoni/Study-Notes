## ADDED Requirements

### Requirement: System SHALL support configurable autonomy levels

The system SHALL support 4 autonomy levels (0-3) that control confirmation frequency.

#### Scenario: Level 0 - Full confirmation
- **WHEN** autonomy level is set to 0
- **THEN** Main Agent SHALL call AskUserQuestion before every phase transition
- **AND** Main Agent SHALL wait for explicit user confirmation before proceeding

#### Scenario: Level 1 - Phase confirmation
- **WHEN** autonomy level is set to 1
- **THEN** Main Agent SHALL call AskUserQuestion only at phase boundaries
- **AND** Main Agent SHALL NOT confirm subphase transitions (e.g., within collect)

#### Scenario: Level 2 - Key point confirmation
- **WHEN** autonomy level is set to 2
- **THEN** Main Agent SHALL call AskUserQuestion only at critical decision points:
  - Note type selection
  - Execution plan approval
  - Final result review
- **AND** Main Agent SHALL auto-proceed through routine transitions

#### Scenario: Level 3 - Full auto
- **WHEN** autonomy level is set to 3
- **THEN** Main Agent SHALL auto-proceed through all phases
- **AND** Main Agent SHALL only call AskUserQuestion for final result review
- **AND** Main Agent SHALL display progress summary after each phase

### Requirement: Autonomy level SHALL be configurable

Users SHALL be able to set autonomy level via configuration.

#### Scenario: Global configuration
- **WHEN** user sets `autonomy.level` in `.study-config.yaml`
- **THEN** Main Agent SHALL use that level for all phases
- **AND** configuration SHALL persist across sessions

#### Scenario: Per-phase override
- **WHEN** user sets `autonomy.overrides` for specific phases
- **THEN** Main Agent SHALL use the override level for those phases
- **AND** other phases SHALL use the global level

### Requirement: Main Agent SHALL respect autonomy level during execution

Main Agent SHALL check autonomy level before each confirmation point.

#### Scenario: Confirmation check
- **WHEN** Main Agent reaches a confirmation point
- **THEN** Main Agent SHALL check current autonomy level
- **AND** if current point requires confirmation at this level, call AskUserQuestion
- **AND** if not, auto-proceed and log the transition

#### Scenario: Level display
- **WHEN** Main Agent auto-proceeds due to autonomy level
- **THEN** Main Agent SHALL display brief status message:
  - "[Auto] Phase X complete, proceeding to Phase Y (autonomy level: N)"
