# Comet Design Handoff

- Change: update-note-workflow
- Phase: design
- Mode: compact
- Context hash: 8543dc7fe7f6cbf2acbaaed79f5c2d6339e4a4a885744948beddb69659058a74

Generated-by: comet-handoff.sh

OpenSpec remains the canonical capability spec. This handoff is a deterministic, source-traceable context pack, not an agent-authored summary.

## openspec/changes/update-note-workflow/proposal.md

- Source: openspec/changes/update-note-workflow/proposal.md
- Lines: 1-30
- SHA256: 884705e10fa17b135e72f8ddebf4a76b831842f038d0c4c07567238f9c639eef

```md
## Why

创建笔记有完整的 6-phase 工作流（phases.md）和 TODO.md 状态追踪，但更新笔记只有一个孤立的 `update` skill，缺少编排层。当用户说"更新我的 React hooks 笔记"时，系统无法：
- 自动定位目标笔记并分析结构
- 根据用户意图（追加 vs 刷新）选择正确路径
- 在 REFRESH 模式下可靠地执行 mini collect→curate→write 循环
- 在更新后进行验证并让用户确认 diff

现有 `update` skill 定义了 INSERT 和 REFRESH 两种模式的步骤，但没有工作流级别的编排——没有阶段门禁、没有状态追踪、没有用户确认阻塞点。

## What Changes

- 新增 `update-workflow` skill：封装更新笔记的完整编排流程，委托现有 `update` skill 执行实际插入操作
- 更新 `docs/updating-notes.md`：补充工作流编排说明，与新 skill 保持一致
- 现有 `update` skill 保持不变，作为底层执行者被调用

## Capabilities

### New Capabilities
- `note-update-workflow`: 笔记更新工作流编排——定位目标笔记、识别更新意图（INSERT/REFRESH）、执行更新、轻量验证、用户确认

### Modified Capabilities
（无现有 spec 需要修改）

## Impact

- `.claude/skills/` 目录：新增 `update-workflow/SKILL.md`
- `docs/updating-notes.md`：内容更新
- 现有 `update` skill：不受影响，作为底层依赖被包装调用
- 子 agent 定义（`collector.md`、`curator.md`、`writer.md`）：不受影响，mini 循环复用现有 subagent
```

## openspec/changes/update-note-workflow/design.md

- Source: openspec/changes/update-note-workflow/design.md
- Lines: 1-72
- SHA256: 2868fd52106ff61780176139df86136d16b9ce5e0c8bf65929b560f17ca6a71a

```md
## Context

Study System 有两种笔记生命周期：
1. **创建**：完整的 6-phase 工作流（collect → curate → write → beautify → evaluate → digest），由 `phases.md` 编排，有 TODO.md 状态追踪和阶段门禁
2. **更新**：现有 `update` skill 支持 INSERT（插入新内容）和 REFRESH（刷新过时内容），但缺少工作流级别的编排

更新笔记的典型场景：
- "给我的 React hooks 笔记加上 useEffect cleanup 的内容" → INSERT
- "React hooks 笔记的 hooks 规则部分过时了，更新一下" → REFRESH
- REFRESH 模式可能需要 mini collect→curate→write 研究循环

现有 `update` skill 已定义了详细的执行步骤（分析笔记、确认模式、最小改动插入、验证），但它是一个独立 skill，没有编排层来管理多步骤流程、状态追踪和用户确认。

## Goals / Non-Goals

**Goals:**
- 提供一个编排层（`update-workflow` skill），封装更新笔记的完整流程
- 支持两种核心场景：追加新内容（INSERT）和定向刷新章节（REFRESH）
- 在 REFRESH 模式下可靠地执行 mini collect→curate→write 循环
- 更新后进行轻量验证（格式一致性、双链完整性）
- 保留用户确认阻塞点，让用户审核 diff 后决定

**Non-Goals:**
- 不替换现有 `update` skill — 新 skill 包装它作为底层执行者
- 不支持批量更新多个笔记
- 不支持模板迁移或元数据批量更新
- 不做完整的质量评估（evaluate）— 只做轻量验证
- 不修改现有 collect/curate/write 子 agent 定义

## Decisions

### D1: 包装现有 skill 而非替换

**选择**：新增 `update-workflow` skill 作为编排层，委托现有 `update` skill 执行实际插入操作。

**替代方案**：
- A) 废弃旧 skill，用新 skill 完全替代 → 风险：破坏已有的用户习惯和文档引用
- B) 在旧 skill 内部增加编排逻辑 → 风险：单个 skill 职责过重

**理由**：包装模式保持关注点分离。`update` skill 负责"怎么插入"，`update-workflow` 负责"什么时候插入什么"。

### D2: TODO.md 状态追踪用于 REFRESH 模式

**选择**：仅在 REFRESH 模式的 mini 研究循环中使用 TODO.md 追踪状态（mini-collect → mini-curate → mini-write）。INSERT 模式不需要状态追踪（单步操作）。

**理由**：REFRESH 的 mini 循环涉及多个阶段，需要状态追踪来支持中断恢复。INSERT 是单步操作，TODO.md 增加的复杂度不值得。

### D3: 轻量验证策略

**选择**：更新后执行三项检查：
1. 标题层级连贯性（不越级）
2. 双链完整性（不破坏现有 `[[wikilinks]]`）
3. frontmatter `updated` 字段已更新

**替代方案**：
- A) 调用 evaluate skill 做完整质量评估 → 过重，不适合小范围更新
- B) 不做任何验证 → 风险：格式错误和断链静默传播

**理由**：轻量验证覆盖最常见的更新引入问题（格式破坏、链接断裂），同时不增加不必要的复杂度。

### D4: 复用现有子 agent

**选择**：REFRESH 模式的 mini 循环直接调用现有 `/collect`、`/curate`、`/write` skill，不创建新的子 agent。

**理由**：现有子 agent 已经功能完整，只是调用范围缩小到子主题。通过传入父主题上下文和目录隔离来适配更新场景。

## Risks / Trade-offs

- **[Risk] REFRESH mini 循环的上下文传递可能不完整** → Mitigation: 在调用各 skill 时显式传入父笔记信息（父主题名、笔记类型、标题层级、格式约定）
- **[Risk] Windows 环境下 bash 脚本执行** → Mitigation: comet 脚本通过 Git Bash 执行，已在当前环境验证可用
- **[Trade-off] INSERT 模式不追踪状态** → 单步操作不需要，但如果用户在插入过程中中断，需要重新开始（可接受）
- **[Trade-off] 不支持批量更新** → 聚焦核心场景，批量需求可通过多次调用满足
```

## openspec/changes/update-note-workflow/tasks.md

- Source: openspec/changes/update-note-workflow/tasks.md
- Lines: 1-26
- SHA256: 056d71c01d5ff37c8380ae6b62fed4487bf3ad32b06895418582f8f2c9eca504

```md
# Tasks: Update Note Workflow

## Phase 1: Create update-workflow skill

- [ ] 1.1 Create `.claude/skills/update-workflow/SKILL.md` — skill definition
  - Step 1: Locate target note + parse structure
  - Step 2: Detect intent (INSERT vs REFRESH)
  - Step 3: Delegate to `update` skill for execution
  - Step 4: Light verification (heading levels, wikilinks, frontmatter)
  - Step 5: User confirmation with diff summary
  - REFRESH mode: orchestrate mini collect→curate→write cycle

## Phase 2: Update documentation

- [ ] 2.1 Update `docs/updating-notes.md` — reflect new workflow orchestration
  - Add workflow diagram
  - Update mode descriptions to reference update-workflow skill
  - Keep existing rules and hard stops

## Phase 3: Test & verify

- [ ] 3.1 Test INSERT mode — add content to an existing note
- [ ] 3.2 Test REFRESH mode with direct replacement
- [ ] 3.3 Test REFRESH mode with mini research cycle
- [ ] 3.4 Verify light verification catches heading level issues
- [ ] 3.5 Verify wikilink integrity check works
```

## openspec/changes/update-note-workflow/specs/note-update-workflow/spec.md

- Source: openspec/changes/update-note-workflow/specs/note-update-workflow/spec.md
- Lines: 1-71
- SHA256: e00d30e0c39d9e2fe5c3265116fac2476e785ca6956d88008bdac1e528498038

```md
## ADDED Requirements

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

### Requirement: Execute INSERT update
The system SHALL delegate to the existing `update` skill for content insertion. The insertion SHALL match the surrounding formatting (heading levels, callout types, table conventions, code block languages) and preserve existing wikilinks.

#### Scenario: Content inserted at specified section
- **WHEN** user provides new content and specifies a target section
- **THEN** system inserts content at the correct position, matching surrounding formatting, and updates the `updated` frontmatter field

#### Scenario: Content appended to end
- **WHEN** user says "追加到末尾"
- **THEN** system appends content at the end of the note, maintaining heading hierarchy

### Requirement: Execute REFRESH with research
The system SHALL support REFRESH mode with an optional mini research cycle. When re-research is chosen, the system SHALL execute mini-collect → mini-curate → mini-write for the target subsection only, using directory isolation and parent topic context.

#### Scenario: REFRESH with direct replacement
- **WHEN** user chooses to replace content directly in REFRESH mode
- **THEN** system proceeds with INSERT mode using user-provided replacement content

#### Scenario: REFRESH with mini research cycle
- **WHEN** user chooses to re-research in REFRESH mode
- **THEN** system creates a mini TODO.md, runs collect → curate → write for the subsection, and inserts the result into the target note

#### Scenario: Mini research uses isolated directories
- **WHEN** mini research cycle runs for a subsection
- **THEN** system writes to `0-inbox/{subtopic}/`, `1-curated/{subtopic}/`, `2-drafts/{subtopic}/` and passes parent topic context (parent name, note type, heading level, formatting conventions) to each skill

### Requirement: Light verification after update
The system SHALL verify the updated note for: (1) heading level consistency (no skipped levels), (2) wikilink integrity (no broken `[[links]]`), (3) frontmatter `updated` field is set to current date.

#### Scenario: Verification passes
- **WHEN** updated note has consistent heading levels, intact wikilinks, and updated frontmatter
- **THEN** system shows diff summary and asks user to confirm

#### Scenario: Verification fails
- **WHEN** updated note has broken heading levels or wikilinks
- **THEN** system reports the specific issues and offers to fix them before user confirmation

### Requirement: User confirmation with diff
The system SHALL present a diff summary showing which section was modified and how much content was added/replaced. The system SHALL wait for explicit user confirmation before finalizing the update.

#### Scenario: User confirms update
- **WHEN** diff summary is presented and user confirms
- **THEN** update is finalized, note is saved with updated frontmatter

#### Scenario: User requests changes
- **WHEN** diff summary is presented and user requests modifications
- **THEN** system applies the requested changes and re-presents the diff
```

