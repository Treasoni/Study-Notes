# Comet Design Handoff

- Change: reduce-doc-redundancy-and-skill-bloat
- Phase: design
- Mode: compact
- Context hash: abbac4121f724b6a697ae5066ca7f515ef789e24a98db50b5cb903668ec53b28

Generated-by: comet-handoff.sh

OpenSpec remains the canonical capability spec. This handoff is a deterministic, source-traceable context pack, not an agent-authored summary.

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/proposal.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/proposal.md
- Lines: 1-38
- SHA256: ddae3fb33abe22843c3422ba43fc4be1f5071a31e68d5f5259273e43cd350d69

```md
## Why

Study System 的文档和 skill 定义存在严重的冗余问题，导致每次会话消耗大量无用 token：

1. **TODO.md 状态机规则分散在 17 个文件中**，同一规则（Phase Gate、rm TODO.md 等）重复定义 9-12 次，总计 ~7000 tokens 冗余
2. **update-workflow/SKILL.md 与 docs/updating-notes.md 60-70% 内容重复**（~3000 tokens）
3. **scoring rubric 在 3 个文件中完全相同**（~400 tokens）
4. **37 个非 study-system skills（~300KB）每次会话全量注入系统提示**，但从未被引用

这些问题不仅浪费 token，还增加了维护成本——修改一个规则需要同步更新多个文件。

## What Changes

- **抽取 TODO.md 状态机为单一权威参考文档**，其他文件改为引用而非重复定义
- **合并 update-workflow/SKILL.md 与 docs/updating-notes.md**，消除 60-70% 重复
- **scoring rubric 单一来源**，只在 collector.md 定义，其他位置引用
- **研究并实现 skill 过滤/分组机制**，让 .study-config.yaml 能控制哪些 skill 注入系统提示
- **精简 4 个 agent 定义中的重复豁免块**

## Capabilities

### New Capabilities

- `skill-filtering`: 机制控制哪些 skills 注入系统提示，减少 ~300KB 无用上下文

### Modified Capabilities

- `note-update-workflow`: 合并 update-workflow 与 updating-notes.md，统一文档来源
- `subagent-orchestration`: 精简 agent 定义中的重复豁免块

## Impact

- **docs/** 目录：phases.md、experience-notes.md、updating-notes.md 内容精简
- **.claude/skills/**：update-workflow/SKILL.md 合并或删除
- **.claude/agents/**：4 个 agent 定义精简
- **.study-config.yaml**：新增 skill 过滤配置项
- **CLAUDE.md**：TODO.md 状态机规则改为引用新参考文档
- **Token 节省**：预计每次会话减少 ~10,000+ tokens（不含 skill 过滤的额外节省）
```

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/design.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/design.md
- Lines: 1-110
- SHA256: 20f39950151d58abc62ba31304e3673758c7d9b3859d09d86e9c682385b4c597

[TRUNCATED]

```md
## Context

Study System 的文档体系经过多次迭代，产生了大量重复：
- TODO.md 状态机规则分散在 17 个文件中，同一指令重复 9-12 次
- update-workflow/SKILL.md 与 docs/updating-notes.md 60-70% 重复
- scoring rubric 在 3 个文件中完全相同
- 51 个 skills 全量注入系统提示，其中 37 个与 study-system 无关

当前每次会话的系统提示包含 ~381KB SKILL.md 内容 + ~10,000 tokens 文档冗余。

## Goals / Non-Goals

**Goals:**
- 消除文档冗余，预计每次会话减少 ~10,000+ tokens
- 实现 skill 过滤机制，减少 ~300KB+ 无用 skill 上下文
- 建立单一权威来源模式，防止未来再次出现冗余
- 保持所有现有功能不变（纯重构，无行为变更）

**Non-Goals:**
- 不改变 TODO.md 状态机的运行时行为
- 不重命名或重新组织 skills 目录结构
- 不修改任何 skill 的执行逻辑
- 不影响非 study-system 的 skills（comet、opencli 等保留原位）

## Decisions

### D1: TODO.md 状态机抽取为独立参考文档

**选择**：创建 `docs/todo-state-machine.md` 作为唯一权威定义，其他文件改为引用。

**替代方案**：
- 方案 B：在 CLAUDE.md 中保留完整定义 → 仍然分散，且 CLAUDE.md 已接近 160 行上限
- 方案 C：用脚本强制执行 → 过度工程化，状态机本质是线性的

**理由**：
- 线性状态机的规则简单（Read→Write→Bash），问题只是分散
- 抽取后 CLAUDE.md 只需一行引用，phases.md/experience-notes.md 各减少 ~500 tokens
- 17 个文件的引用改为指向同一来源

**实现**：
```
docs/todo-state-machine.md  ← 唯一权威定义
├─ 状态定义（create → phase gates → delete）
├─ 工具映射（Read/Write/Bash）
├─ 三种工作流变体（5-phase / 7-step / REFRESH mini）
└─ 路径约定（{SYSTEM_ROOT}/TODO.md）

CLAUDE.md  → 一行引用：See docs/todo-state-machine.md
phases.md  → Phase Gate 改为引用，不再重复定义
experience-notes.md → 同上
updating-notes.md → 同上
```

### D2: 合并 update-workflow 与 updating-notes.md

**选择**：保留 `docs/updating-notes.md` 作为权威文档，`update-workflow/SKILL.md` 精简为路由逻辑（如何调用 /update skill）。

**替代方案**：
- 方案 B：删除 updating-notes.md，全部移入 SKILL.md → 不符合现有模式（docs/ 是权威来源）
- 方案 C：创建新的合并文档 → 不必要的新文件

**理由**：
- 现有模式是 docs/ 存放规范，skills/ 存放执行逻辑
- updating-notes.md 已包含完整的 INSERT/REFRESH 工作流定义
- SKILL.md 只需保留：意图检测 + 路由到 /update skill + 读取 docs/updating-notes.md 的引用

### D3: Scoring rubric 单一来源

**选择**：scoring rubric 只在 `collector.md` agent 定义中完整保留，`collect/SKILL.md` 和 `phases.md` 改为引用。

**理由**：
- collector.md 是实际执行评分的 agent，是自然的权威来源
- collect/SKILL.md 是调度逻辑，不需要内联评分标准
- phases.md 是概览文档，引用即可

### D4: Skill 过滤机制

**选择**：在 `.study-config.yaml` 中新增 `skills.include` / `skills.exclude` 配置项，主 Agent 在 Resource Discovery 阶段根据配置过滤 skill 列表。

**替代方案**：
```

Full source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/design.md

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/tasks.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/tasks.md
- Lines: 1-48
- SHA256: 9c7ab63ad7116414f4e545bfcdfe48edab1f32415793a50d3086ad52fc1f8d83

```md
## 1. 创建 docs/todo-state-machine.md 权威文档

- [ ] 1.1 创建 `docs/todo-state-machine.md`，包含：状态定义、工具映射（Read/Write/Bash）、三种工作流变体（5-phase / 7-step / REFRESH mini）、路径约定
- [ ] 1.2 在文件顶部添加"被引用文件列表"，标注所有引用此文档的文件

## 2. 精简 CLAUDE.md 中的 TODO.md 规则

- [ ] 2.1 将 CLAUDE.md 中 TODO.md State Machine 部分（~10 行）替换为一行引用：`See docs/todo-state-machine.md`
- [ ] 2.2 验证 CLAUDE.md 行数仍 ≤ 160

## 3. 精简 phases.md 中的 Phase Gate 重复

- [ ] 3.1 将 phases.md 中 5 个 Phase Gate 指令（lines 127, 139, 152, 168, 180）替换为引用 `docs/todo-state-machine.md`
- [ ] 3.2 将 phases.md 中 `rm TODO.md` 指令替换为引用

## 4. 精简 experience-notes.md 中的重复

- [ ] 4.1 将 experience-notes.md 中 7 个 Phase Gate 指令替换为引用 `docs/todo-state-machine.md`
- [ ] 4.2 将 experience-notes.md 中 `rm TODO.md` 指令替换为引用

## 5. 合并 update-workflow 与 updating-notes.md

- [ ] 5.1 逐行对比 update-workflow/SKILL.md 与 docs/updating-notes.md，识别 30-40% 独特内容
- [ ] 5.2 将 update-workflow/SKILL.md 精简为：意图检测 + 路由逻辑 + 引用 docs/updating-notes.md
- [ ] 5.3 确保 docs/updating-notes.md 中的 REFRESH mini 循环引用 `docs/todo-state-machine.md`

## 6. Scoring rubric 单一来源

- [ ] 6.1 将 collect/SKILL.md 中的 scoring rubric 替换为引用 collector.md
- [ ] 6.2 将 phases.md 中 Phase 1 的 scoring rubric 替换为引用 collector.md

## 7. Skill 过滤机制

- [ ] 7.1 在 `.study-config.yaml` 中添加 `skills.include` 和 `skills.exclude` 配置项（默认为空）
- [ ] 7.2 在 CLAUDE.md 的 Resource Discovery 部分添加过滤步骤说明
- [ ] 7.3 添加配置验证逻辑：启动时检查 exclude/include 中的名称是否匹配现有 skill，不匹配时输出警告

## 8. Agent 豁免块标注来源

- [ ] 8.1 在 4 个 agent 定义（collector.md、writer.md、curator.md、beautifier.md）的全局指令豁免块中添加注释，标注共同来源
- [ ] 8.2 确认 4 个文件的豁免内容一致

## 9. 验证与清理

- [ ] 9.1 运行 `bash scripts/validate-structure.sh` 验证结构完整性
- [ ] 9.2 检查所有引用路径是否正确（docs/todo-state-machine.md 被正确引用）
- [ ] 9.3 验证 .study-config.yaml 新增字段格式正确
- [ ] 9.4 验证 CLAUDE.md 行数 ≤ 160
```

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/note-update-workflow/spec.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/note-update-workflow/spec.md
- Lines: 1-38
- SHA256: 5a41429f2662b98d3a0382fa72601b5a09c9a10eb77b8d1f4f8947135cd956a6

```md
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
```

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/skill-filtering/spec.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/skill-filtering/spec.md
- Lines: 1-38
- SHA256: 929b5cc33e27b2af5d02426849e5eca2f64cf2def9e17b00f6917ae86e1fe6d4

```md
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
```

## openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/subagent-orchestration/spec.md

- Source: openspec/changes/reduce-doc-redundancy-and-skill-bloat/specs/subagent-orchestration/spec.md
- Lines: 1-41
- SHA256: 2da91c67b16eb8221d4c3866e510087932c0427cc48c7c9cc69451e0c0097304

```md
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
```

