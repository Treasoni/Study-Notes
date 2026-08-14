
# 技能调用指南

当用户请求涉及技能（skill）领域时，优先调用对应技能，而非自行实现。

## 核心原则

1. **技能优先**：用户请求匹配到已有技能时，必须通过 `Skill` 工具调用，不要手动实现技能已覆盖的功能
2. **精准匹配**：根据用户意图和触发词选择最合适的技能，避免误触发或漏触发
3. **不要猜测**：不确定是否有对应技能时，查阅下方技能列表再决定
4. **单一技能**：每次调用一个技能；如需多个技能协作，按顺序逐个调用

## Obsidian 说明

本项目不依赖全局 Obsidian plugin skills。Obsidian 相关能力由项目本地规则和 skills 承担：

- `note-beautifier`：处理 Obsidian Markdown、frontmatter、标签、Callout、双链和发布位置。
- `legacy-note-importer`：处理已有旧笔记的批量盘点、迁移计划和规范化入口。
- `batch-note-updater`：处理多篇旧笔记的批量更新计划、批次编排和逐篇 note-updater 调用。
- `moc-organizer`：生成或更新 MOC 目录笔记。
- `.codex/rules/obsidian/note-system.md`：Obsidian 输出规范。

## 技能列表
<!-- skill-registry:managed ["ask-matt","claude-handoff","code-review","codebase-design","diagnosing-bugs","digest","domain-modeling","git-guardrails-claude-code","grill-me","grill-with-docs","grilling","handoff","implement","improve-codebase-architecture","loop-me","maintain-learnings","manifest-platform","migrate-to-shoehorn","prompt-cache-optimizer","prototype","research","resolving-merge-conflicts","scaffold-exercises","setup-matt-pocock-skills","setup-pre-commit","setup-ts-deep-modules","sync-skill-registry","tdd","teach","to-questionnaire","to-spec","to-tickets","triage","wait-what","wayfinder","wizard","workflow-todo-state","writing-beats","writing-for-agents","writing-fragments","writing-shape"] -->

#### 图表与可视化

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `excalidraw-diagram` | 生成 Excalidraw 流程图、思维导图、架构图 | 画图、流程图、思维导图、Excalidraw、可视化、diagram |
| `json-canvas` | 生成 JSON Canvas 格式的可视化画布 | canvas、画布、JSON Canvas |

#### 学习笔记工作流

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `workflow-todo-state` | Create or retrofit reusable named workflow state machines for multi-step agen… | Create or retrofit reusable named workfl… |
| `note-assembler` | 将章节组装成完整笔记（由 agent 调用） | 组装、合并章节、收尾、拼装、assemble |

#### 内容提取

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `defuddle` | 从网页提取正文内容 | 提取网页、网页正文、defuddle |

#### 工具发现

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `sync-skill-registry` | 技能注册表同步工具。扫描任意 agent skill 目录中的 */SKILL.md 并自动更新对应 skill-invocation.md 中的技能列表… | 同步注册表、更新技能列表、sync skill registry、update skill registration、刷新技能列表、同步技能表格 |

#### 自我学习

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `digest` | 自我学习阶段。回顾本次会话，记录真实发生的学习点和错误到 .learnings/； | 自我学习阶段 |

#### 开发工具

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `manifest-platform` | Install, configure, migrate, and validate a portable manifest registry for ag… | Install, configure, migrate, and validat… |
| `prompt-cache-optimizer` | 审计并优化 LLM 提示缓存命中率、输入 token、延迟与调用成本。 | 优化缓存命中、降低 token 成本、审计 LLM 调用、提示词缓存优化、优化 AI 调用费用 |

#### 未分类

| 技能 | 触发场景 | 关键触发词 |
|------|----------|-----------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this… | Ask which skill or flow fits your situat… |
| `claude-handoff` | Hand the current conversation off to a fresh background agent that picks up t… | Hand the current conversation off to a f… |
| `code-review` | Review the changes since a fixed point (commit, branch, tag | review since X |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to desi… | Shared vocabulary for designing deep mod… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user s… | diagnose、debug this |
| `domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin do… | Build and sharpen a project's domain mod… |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard | Set up Claude Code hooks to block danger… |
| `grill-me` | A relentless interview to sharpen a plan or design. | A relentless interview to sharpen a plan… |
| `grill-with-docs` | A relentless interview to sharpen a plan or design | A relentless interview to sharpen a plan… |
| `grilling` | Grill the user relentlessly about a plan, decision | Grill the user relentlessly about a plan… |
| `handoff` | Compact the current conversation into a handoff document for another agent to… | Compact the current conversation into a … |
| `implement` | "Implement a piece of work based on a spec or set of tickets." | Implement a piece of work based on a spec or set of tickets. |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities | Scan a codebase for deepening opportunit… |
| `loop-me` | Grill me about specs for the workflows I want to build, within this workspace. | Grill me about specs for the workflows I… |
| `maintain-learnings` | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则失效问题聚类诊断，追溯并修改对应 skill、模板、hook、校验脚本或项目规则； | 维护 .learnings/ 经验库，把过多或反复出现的学习记录、错误日志、规则… |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. U… | Migrate test files from `as` type assert… |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the user wa… | Build a throwaway prototype to answer a … |
| `research` | Investigate a question against high-trust primary sources and capture the fin… | Investigate a question against high-trus… |
| `resolving-merge-conflicts` | "Use when you need to resolve an in-progress git merge/rebase conflict." | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `scaffold-exercises` | Create exercise directory structures with sections, problems, solutions | Create exercise directory structures wit… |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker | Configure this repo for the engineering … |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking | Set up Husky pre-commit hooks with lint-… |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep modu… | Wire dependency-cruiser into a TypeScrip… |
| `tdd` | Test-driven development. Use when the user wants to build features or fix bug… | red-green-refactor |
| `teach` | Teach the user a new skill or concept, within this workspace. | Teach the user a new skill or concept, w… |
| `to-questionnaire` | Turn a decision you can't fully answer into a questionnaire for someone else … | Turn a decision you can't fully answer i… |
| `to-spec` | Turn the current conversation into a spec and publish it to the project issue… | Turn the current conversation into a spe… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bullet t… | Break a plan, spec, or the current conve… |
| `triage` | Move issues and external PRs through a state machine of triage roles — catego… | Move issues and external PRs through a s… |
| `wait-what` | Stop. That last message did not land — re-pitch it. | Stop |
| `wayfinder` | Plan a huge chunk of work — more than one agent session can hold — as a share… | Plan a huge chunk of work — more than on… |
| `wizard` | Generate an interactive bash wizard that walks a human through steps only the… | Generate an interactive bash wizard that… |
| `writing-beats` | Writing, exploit — assemble raw material into a journey of beats | Writing, exploit — assemble raw material… |
| `writing-for-agents` | Writing documents for agents. Use when creating or editing skills | Writing documents for agents |
| `writing-fragments` | Writing, explore — mine raw fragments, no structure yet. | Writing, explore — mine raw fragments, n… |
| `writing-shape` | Writing, exploit — shape raw material into an article, paragraph by paragraph. | Writing, exploit — shape raw material in… |

### 1. 分析意图

- 用户想做什么？（创建、读取、修改、删除、转换）
- 涉及什么文件类型？（.pdf、.docx、.xlsx、.md）
- 是否属于特定平台？（Obsidian、Excalidraw）

### 2. 匹配技能

- 优先匹配**最具体**的技能
- 触发词可能出现在用户消息的任何位置
- 中英文触发词同等对待


### 错误处理

- 技能调用失败时，向用户说明原因并建议替代方案
- 不要静默失败，明确告知用户发生了什么
- 如果技能不支持某个操作，如实告知而非强行实现
