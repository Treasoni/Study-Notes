## ADDED Requirements

### Requirement: System SHALL support hybrid note types

The system SHALL allow notes to contain elements from multiple note types.

#### Scenario: Hybrid type selection
- **WHEN** user selects multiple note types
- **THEN** Main Agent SHALL accept type combination (e.g., concept + practice)
- **AND** Main Agent SHALL generate note with elements from all selected types

#### Scenario: Auto-hybrid detection
- **WHEN** topic requires multiple types (e.g., "React hooks" needs concept + practice)
- **THEN** Main Agent SHALL recommend hybrid combination
- **AND** recommendation SHALL include rationale

### Requirement: Hybrid notes SHALL have coherent structure

The system SHALL organize hybrid notes with logical chapter ordering.

#### Scenario: Chapter ordering
- **WHEN** generating hybrid note with types [concept, practice]
- **THEN** system SHALL use ordering:
  1. Concept explanation (from concept template)
  2. Practical examples (from practice template)
  3. Common patterns (merged)
  4. Thinking questions (merged)
- **AND** sections SHALL have clear transitions

#### Scenario: Section merging
- **WHEN** multiple types have similar sections (e.g., "Key Points" in concept and practice)
- **THEN** system SHALL merge into single section
- **AND** merged section SHALL contain elements from both types

### Requirement: System SHALL support type-specific sections

Each note type SHALL contribute specific sections to hybrid notes.

#### Scenario: Concept sections
- **WHEN** concept type is included
- **THEN** note SHALL contain:
  - Core Definition
  - Key Principles
  - Common Misconceptions
  - Related Concepts (wikilinks)

#### Scenario: Practice sections
- **WHEN** practice type is included
- **THEN** note SHALL contain:
  - Real-world Examples
  - Code Snippets
  - Step-by-step Guide
  - Common Pitfalls

#### Scenario: Compare sections
- **WHEN** compare type is included
- **THEN** note SHALL contain:
  - Comparison Table
  - When to Use X vs Y
  - Trade-offs
  - Decision Framework

#### Scenario: Cheat sheet sections
- **WHEN** cheat_sheet type is included
- **THEN** note SHALL contain:
  - Quick Reference Commands
  - Common Patterns
  - Troubleshooting Guide
  - One-liner Examples

#### Scenario: Experience sections
- **WHEN** experience type is included
- **THEN** note SHALL contain:
  - Background Context
  - Learning Process
  - Key Insights
  - Lessons Learned
  - Future Directions

### Requirement: Hybrid notes SHALL maintain source attribution

All content in hybrid notes SHALL have proper source attribution.

#### Scenario: Source tracking
- **WHEN** content is added from different sources
- **THEN** each section SHALL include `[来源: R1]` style attribution
- **AND** hybrid notes SHALL have complete references section
