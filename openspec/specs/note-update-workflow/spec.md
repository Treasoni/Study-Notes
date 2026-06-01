## MODIFIED Requirements

### Requirement: Locate target note
The system SHALL locate the target note by name or path when the user requests an update. The system SHALL parse the note's YAML frontmatter and identify its structural elements (headings, callout types, table conventions, wikilinks).

#### Scenario: Note found by name
- **WHEN** user says "更新我的 React hooks 笔记" and a note matching "React hooks" exists in `3-published/`
- **THEN** system reads the note, extracts frontmatter (type, tags, created, updated), and identifies the heading structure

#### Scenario: Note not found
- **WHEN** user requests an update but no matching note is found
- **THEN** system reports the issue and asks user to provide the exact path

### Requirement: Detect update intent
The system SHALL classify the user's update intent as either INSERT (user provides new content to add) or REFRESH (user wants to update outdated content). The classification SHALL be based on whether the user provides concrete content or describes a need for fresh research.

#### Scenario: INSERT intent detected
- **WHEN** user says "给 React hooks 笔记加上 useEffect cleanup 的内容" and provides or describes specific content
- **THEN** system classifies as INSERT mode and proceeds to insertion

#### Scenario: REFRESH intent detected
- **WHEN** user says "React hooks 笔记的 hooks 规则部分过时了，更新一下"
- **THEN** system classifies as REFRESH mode and asks whether to replace in-place or re-research

### Requirement: Execute REFRESH with research
The system SHALL support REFRESH mode with an optional mini research cycle. When re-research is chosen, the system SHALL execute mini-collect → mini-curate → mini-write for the target subsection only, using directory isolation and parent topic context. The mini research cycle SHALL reference `docs/todo-state-machine.md` for TODO.md management rules instead of duplicating them.

#### Scenario: REFRESH with direct replacement
- **WHEN** user chooses to replace content directly in REFRESH mode
- **THEN** system proceeds with INSERT mode using user-provided replacement content

#### Scenario: REFRESH with mini research cycle
- **WHEN** user chooses to re-research in REFRESH mode
- **THEN** system creates a mini TODO.md following `docs/todo-state-machine.md` rules, runs collect → curate → write for the subsection, and inserts the result into the target note

#### Scenario: Mini research uses isolated directories
- **WHEN** mini research cycle runs for a subsection
- **THEN** system writes to `0-inbox/{subtopic}/`, `1-curated/{subtopic}/`, `2-drafts/{subtopic}/` and passes parent topic context (parent name, note type, heading level, formatting conventions) to each skill
