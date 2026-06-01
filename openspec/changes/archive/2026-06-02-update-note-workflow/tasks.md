# Tasks: Update Note Workflow

## Phase 1: Create update-workflow skill

- [x] 1.1 Create `.claude/skills/update-workflow/SKILL.md` — skill definition
  - Step 1: Locate target note + parse structure
  - Step 2: Detect intent (INSERT vs REFRESH)
  - Step 3: Delegate to `update` skill for execution
  - Step 4: Light verification (heading levels, wikilinks, frontmatter)
  - Step 5: User confirmation with diff summary
  - REFRESH mode: orchestrate mini collect→curate→write cycle

## Phase 2: Update documentation

- [x] 2.1 Update `docs/updating-notes.md` — reflect new workflow orchestration
  - Add workflow diagram
  - Update mode descriptions to reference update-workflow skill
  - Keep existing rules and hard stops

## Phase 3: Test & verify

- [x] 3.1 Test INSERT mode — add content to an existing note
- [x] 3.2 Test REFRESH mode with direct replacement
- [x] 3.3 Test REFRESH mode with mini research cycle
- [x] 3.4 Verify light verification catches heading level issues
- [x] 3.5 Verify wikilink integrity check works
