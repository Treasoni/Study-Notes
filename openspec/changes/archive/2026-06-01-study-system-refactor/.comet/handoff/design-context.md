# Comet Design Handoff

- Change: study-system-refactor
- Phase: design
- Mode: compact
- Context hash: 571f20bf7de53bc1f7d74a05d9d5e42d82718f12ac085996cf932e55f5a30a93

Generated-by: comet-handoff.sh

OpenSpec remains the canonical capability spec. This handoff is a deterministic, source-traceable context pack, not an agent-authored summary.

## openspec/changes/study-system-refactor/proposal.md

- Source: openspec/changes/study-system-refactor/proposal.md
- Lines: 1-36
- SHA256: 39e9c99ee6e25093e82f7d1ddbaecca2014d61eaa371a229d03e6ef1fd508d5f

```md
## Why

Study System 的当前工作流存在四个核心痛点，严重影响使用体验和笔记质量：

1. **上下文爆满**：Main Agent 承担所有重计算（读取、打分、生成），单阶段上下文可达 20k+ tokens，容易超出限制
2. **确认过多**：Phase 边界强制 STOP，每个阶段都需要用户确认，5 个阶段至少 5 次中断
3. **类型不确定**：5 种笔记类型（concept/practice/compare/cheat-sheet/experience）必须在开始时选定，用户 often 不清楚自己想要什么类型
4. **质量不达标**：缺少需求发现阶段，系统假设用户已明确目标，但实际用户 often 不知道自己想要达到什么效果

## What Changes

- **引入 Subagent 分担机制**：将重计算任务（资料采集、打分整理、笔记生成）委托给专用 subagent，Main Agent 仅负责协调
- **添加自治分级系统**：支持 Level 0-3 四级自治，用户可配置确认频率（每步确认 → 每阶段确认 → 关键点确认 → 全自动）
- **支持混合笔记类型**：允许笔记包含多种类型的元素（如概念解释 + 实战示例），支持自动推断最佳类型组合
- **新增讨论澄清阶段**：在正式开始前，通过问答明确学习目的、目标读者、深度要求、笔记用途，生成定制化执行计划

## Capabilities

### New Capabilities

- `subagent-orchestration`: Subagent 调度与协调机制，包括任务分发、结果聚合、错误处理
- `autonomy-levels`: 自治分级系统，支持用户配置确认频率，Main Agent 根据级别决定是否自动推进
- `requirement-discovery`: 需求发现阶段，通过结构化问答明确用户意图，生成执行计划
- `hybrid-note-types`: 混合笔记类型系统，支持多类型元素组合，自动推断最佳类型

### Modified Capabilities

<!-- 无现有 capability 需要修改，这是全新重构 -->

## Impact

- **Core Workflow**：Phase 0-4 流程需要重构，新增讨论澄清阶段
- **Skills**：`collect`、`curate`、`write`、`beautify` 需要适配 subagent 调用
- **Templates**：需要支持混合类型模板或动态组合
- **Configuration**：需要新增 autonomy level 配置项
- **Documentation**：CLAUDE.md、docs/phases.md 需要更新
```

## openspec/changes/study-system-refactor/design.md

- Source: openspec/changes/study-system-refactor/design.md
- Lines: 1-167
- SHA256: ee5795852349a1c38757a85e8e9cf36449fbbdbe2cad578c8a64528fa3ee6eb9

[TRUNCATED]

```md
## Context

Study System 是一个基于 Claude Code + Obsidian 的半自动化技术学习笔记系统。当前架构采用单体 Main Agent 模式，所有阶段（collect → curate → write → beautify → evaluate）都由同一个 Agent 执行，通过文件传递数据。

**当前状态**：
- 5 个阶段，每个阶段有独立的 skill
- Phase 边界强制 STOP + 用户确认
- 5 种固定笔记类型模板
- 无 subagent 支持
- 无自治分级机制

**约束**：
- 必须保持向后兼容，不破坏现有笔记
- 依赖 Claude Code 的 Agent/Workflow 工具
- 系统文件必须保持在 StudySystem/ 目录下

## Goals / Non-Goals

**Goals:**
- 将单阶段上下文使用量从 20k+ tokens 降低到 5k-8k tokens
- 减少 50%-80% 的用户确认次数（根据自治级别）
- 支持混合笔记类型，提高笔记质量
- 通过需求发现阶段，明确用户意图后再生成笔记

**Non-Goals:**
- 不改变 Obsidian 的使用方式
- 不引入外部依赖（如数据库）
- 不改变文件存储结构（仍使用 markdown）
- 不实现全自动流水线（仍需用户参与关键决策）

## Decisions

### Decision 1: Subagent 调度模式

**选择**: Hub-and-Spoke 模式

```
┌─────────────────────────────────────────────────────────┐
│                    Main Agent (Hub)                      │
│  - 协调者角色，不执行重计算                               │
│  - 管理状态流转                                          │
│  - 处理用户交互                                          │
└─────────────────────────────────────────────────────────┘
           │           │           │
           ▼           ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Collect  │ │  Curate  │ │   Write  │
    │ Subagent │ │ Subagent │ │ Subagent │
    └──────────┘ └──────────┘ └──────────┘
```

**替代方案**:
- Pipeline 模式：每个 subagent 自动触发下一个 → 放弃，因为需要用户在阶段间确认
- Mesh 模式：任意 subagent 可调用其他 → 放弃，过于复杂

**理由**: Hub-and-Spoke 保持了 Main Agent 的控制权，同时将重计算委托出去。

### Decision 2: 自治级别实现

**选择**: 配置驱动 + 运行时检查

```yaml
# .study-config.yaml
autonomy:
  level: 1  # 0-3
  overrides:
    - phase: write
      level: 0  # 写笔记时 always 确认
```

**实现方式**:
- 每个阶段开始前检查 autonomy level
- Level 0: 调用 AskUserQuestion 等待确认
- Level 1: 仅在阶段边界确认
- Level 2: 仅在关键点确认（如笔记类型选择）
- Level 3: 仅在最终结果确认

**理由**: 配置驱动允许用户灵活调整，运行时检查确保行为一致。

### Decision 3: 混合笔记类型
```

Full source: openspec/changes/study-system-refactor/design.md

## openspec/changes/study-system-refactor/tasks.md

- Source: openspec/changes/study-system-refactor/tasks.md
- Lines: 1-54
- SHA256: 87adb26fd4439b91fa68c6b1df8e7d087a7840752de4e2160b2edad661073708

```md
## 1. 配置系统

- [ ] 1.1 创建 `.study-config.yaml` 配置文件结构
- [ ] 1.2 实现配置读取工具函数
- [ ] 1.3 添加 autonomy level 配置项（默认 Level 1）
- [ ] 1.4 添加 per-phase override 配置支持

## 2. 需求发现阶段

- [ ] 2.1 创建 `requirement-discovery` skill 框架
- [ ] 2.2 实现结构化问答流程（4-6 个问题）
- [ ] 2.3 实现笔记类型推断逻辑
- [ ] 2.4 实现执行计划生成
- [ ] 2.5 添加"跳过发现"支持（使用默认配置）

## 3. Subagent 调度系统

- [ ] 3.1 创建 `subagent-dispatcher` 工具模块
- [ ] 3.2 实现 Collect Subagent（读取 + 提取）
- [ ] 3.3 实现 Curate Subagent（打分 + 分类）
- [ ] 3.4 实现 Write Subagent（笔记生成）
- [ ] 3.5 实现 Beautify Subagent（排版美化）
- [ ] 3.6 添加 subagent 超时处理（5 分钟）
- [ ] 3.7 添加输出验证逻辑

## 4. 自治级别系统

- [ ] 4.1 创建 `autonomy-manager` 工具模块
- [ ] 4.2 实现 Level 0：每步确认
- [ ] 4.3 实现 Level 1：每阶段确认
- [ ] 4.4 实现 Level 2：关键点确认
- [ ] 4.5 实现 Level 3：全自动
- [ ] 4.6 添加自治级别检查点逻辑

## 5. 混合笔记类型

- [ ] 5.1 定义混合类型章节顺序模板
- [ ] 5.2 实现章节合并逻辑
- [ ] 5.3 实现概念类型贡献的章节
- [ ] 5.4 实现实战类型贡献的章节
- [ ] 5.5 实现对比类型贡献的章节
- [ ] 5.6 实现速查类型贡献的章节
- [ ] 5.7 实现心得类型贡献的章节
- [ ] 5.8 添加来源追踪逻辑

## 6. 集成与测试

- [ ] 6.1 更新 CLAUDE.md 文档
- [ ] 6.2 更新 docs/phases.md
- [ ] 6.3 创建集成测试用例
- [ ] 6.4 测试需求发现 → 收集 → 整理 → 写作完整流程
- [ ] 6.5 测试自治级别 0-3 的行为
- [ ] 6.6 测试混合笔记类型生成
- [ ] 6.7 性能测试：subagent 并行执行
```

## openspec/changes/study-system-refactor/specs/autonomy-levels/spec.md

- Source: openspec/changes/study-system-refactor/specs/autonomy-levels/spec.md
- Lines: 1-58
- SHA256: 4745543102cc8a57d3108f679f5ca6188c26d164f6cf6cac208bbda826c11e60

```md
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
```

## openspec/changes/study-system-refactor/specs/hybrid-note-types/spec.md

- Source: openspec/changes/study-system-refactor/specs/hybrid-note-types/spec.md
- Lines: 1-87
- SHA256: 69bac5870384fc617c1ad1c31f3194b857b278bdaa4baa860e78363d721ed1c9

[TRUNCATED]

```md
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
```

Full source: openspec/changes/study-system-refactor/specs/hybrid-note-types/spec.md

## openspec/changes/study-system-refactor/specs/requirement-discovery/spec.md

- Source: openspec/changes/study-system-refactor/specs/requirement-discovery/spec.md
- Lines: 1-66
- SHA256: 65f2aeaac13ba0da457236b2b98460c479abeb7384e3ba9f978942a87a6caade

```md
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
```

## openspec/changes/study-system-refactor/specs/subagent-orchestration/spec.md

- Source: openspec/changes/study-system-refactor/specs/subagent-orchestration/spec.md
- Lines: 1-60
- SHA256: eddf72ab9c4ae7350c6de074b813f1908e2e2a3b3d5918be55178b593aa1f52a

```md
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
```

