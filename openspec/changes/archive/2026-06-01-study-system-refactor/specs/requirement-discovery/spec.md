## ADDED Requirements

### Requirement: System SHALL conduct requirement discovery before note generation

The system SHALL ask structured questions to understand user's learning intent before generating notes.

#### Scenario: Discovery phase initiation
- **WHEN** user says "I want to learn X" or similar
- **THEN** Main Agent SHALL enter requirement discovery phase
- **AND** Main Agent SHALL NOT proceed to collect phase until discovery is complete

#### Scenario: Discovery questions
- **WHEN** requirement discovery starts
- **THEN** Main Agent SHALL ask 4-6 structured questions:
  1. Learning purpose (exam/work/interest)
  2. Target audience (self/team/community)
  3. Depth requirement (beginner/advanced/expert)
  4. Note usage (review/learning/sharing)
- **AND** each question SHALL have 2-4 preset options + "Other" option

### Requirement: System SHALL infer note type from discovery answers

The system SHALL automatically recommend note type combination based on user's answers.

#### Scenario: Type inference
- **WHEN** user answers all discovery questions
- **THEN** Main Agent SHALL analyze answers and recommend note type combination
- **AND** recommendation SHALL include:
  - Primary type (e.g., concept)
  - Secondary types (e.g., practice, cheat_sheet)
  - Rationale for the combination

#### Scenario: Type override
- **WHEN** user disagrees with recommended type
- **THEN** Main Agent SHALL allow user to select different type(s)
- **AND** Main Agent SHALL update execution plan accordingly

### Requirement: System SHALL generate execution plan from discovery

The system SHALL create a customized execution plan based on discovery results.

#### Scenario: Plan generation
- **WHEN** requirement discovery is complete
- **THEN** Main Agent SHALL generate execution plan with:
  - Selected note types
  - Autonomy level for each phase
  - Estimated time/effort
  - Key checkpoints
- **AND** plan SHALL be displayed to user for approval

#### Scenario: Plan approval
- **WHEN** execution plan is displayed
- **THEN** Main Agent SHALL call AskUserQuestion for approval
- **AND** user can approve, modify, or skip discovery and use defaults

### Requirement: System SHALL support skipping discovery

Users SHALL be able to skip discovery and use default settings.

#### Scenario: Skip discovery
- **WHEN** user chooses to skip discovery
- **THEN** Main Agent SHALL use default configuration:
  - Note type: concept (or inferred from topic)
  - Autonomy level: 1
  - Depth: intermediate
- **AND** Main Agent SHALL proceed directly to collect phase
