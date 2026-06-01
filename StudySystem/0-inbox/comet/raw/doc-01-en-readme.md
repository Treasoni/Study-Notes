[![Comet logo](https://github.com/rpamis/comet/raw/master/img/title-log.png)](https://github.com/rpamis/comet/blob/master/img/title-log.png)

[![CI](https://camo.githubusercontent.com/0d5a6075ef3a2dc47ef386e77cb7fa099ffd478bca2f8eed5e3f6bd2d4eacffd/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f616374696f6e732f776f726b666c6f772f7374617475732f7270616d69732f636f6d65742f63692e796d6c3f6272616e63683d6d6173746572267374796c653d666c61742d737175617265266c6162656c3d4349)](https://github.com/rpamis/comet/actions/workflows/ci.yml) [![DeepWiki](https://camo.githubusercontent.com/917166f310dc7f230625351e3455db4bd145476ce227c7f3f0ba2dba92d43f4b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4465657057696b692d7270616d6973253246636f6d65742d626c75653f7374796c653d666c61742d737175617265)](https://deepwiki.com/rpamis/comet) [![npm version](https://camo.githubusercontent.com/8dc93644934fffe6d111e8768e710a0ee980eaab84ecc4479ca1d4c8c844441c/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f762f407270616d69732f636f6d65743f7374796c653d666c61742d737175617265)](https://www.npmjs.com/package/@rpamis/comet) [![npm download count](https://camo.githubusercontent.com/823321b7353060f37651e680a13d637d61d1efe0e58e495ca8554ad8b5c0ff1a/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f646d2f407270616d69732f636f6d65743f7374796c653d666c61742d737175617265266c6162656c3d446f776e6c6f6164732f6d6f)](https://www.npmjs.com/package/@rpamis/comet) [![npm weekly download count](https://camo.githubusercontent.com/b2c4d42ab03d5b2864e5a7d22432de66b9da7673ede93e65bff57ee277802e62/68747470733a2f2f696d672e736869656c64732e696f2f6e706d2f64772f407270616d69732f636f6d65743f7374796c653d666c61742d737175617265266c6162656c3d446f776e6c6f6164732f776b)](https://www.npmjs.com/package/@rpamis/comet) [![License: MIT](https://camo.githubusercontent.com/a7e65aee57b11d28e4caff8b945729a66be0bb663f7f93bd24c5aa65699f148e/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d626c75652e7376673f7374796c653d666c61742d737175617265)](https://github.com/rpamis/comet/blob/master/LICENSE)

## @rpamis/comet

```
██████╗ ██████╗ ███╗   ███╗███████╗████████╗
██╔════╝██╔═══██╗████╗ ████║██╔════╝╚══██╔══╝
██║     ██║   ██║██╔████╔██║█████╗     ██║
██║     ██║   ██║██║╚██╔╝██║██╔══╝     ██║
╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗   ██║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝   ╚═╝
```

> 中文版： [README-zh.md](https://github.com/rpamis/comet/blob/master/README-zh.md) [Bilibili video](https://www.bilibili.com/video/BV1y4Gi6CEo1/?spm_id_from=333.1387.homepage.video_card.click&vd_source=d22726fe6b108647dbebf1c5d8817377)

**OpenSpec + Superpowers dual-star development workflow** — one command from idea to archive.

OpenSpec handles **WHAT** (outlines, proposals, spec lifecycle, archiving).

Superpowers handles **HOW** (technical design, planning, execution, wrap-up).

Comet chains both into a five-phase automated pipeline.

## Why Comet

OpenSpec excels at managing requirements, creating proposals, managing Spec lifecycles, and archiving, but its proposals and tasks lack the detail of Superpowers brainstorming.

Superpowers generates Spec documents after brainstorming, but these documents typically lack stateful design — after completing requirements, Specs only have tasks checked off in the document, and Agents even forget to check them off. This causes the Agent to re-examine documents and project code to verify on resumption, wasting many tokens.

**Comet combines the strengths of both**, integrating the core workflow into 5 phases

The main entry `/comet` supports current Spec state detection, suitable for long tasks — after closing your AI coding session midway, just `/comet` and Comet will automatically read the active Spec (lists multiple for selection), dynamically identify which phase is currently executing, and continue.

At the same time, Comet provides full Spec lifecycle management. During execution, it links OpenSpec change/spec artifacts with Superpowers design and planning documents, then automates handoff, state updates, validation, and archive sync so users do not have to repeatedly remind the Agent to keep documents synchronized and connected.

## What You'll Learn

Many excellent Skill projects exist in the current Skill market, but they generally have preference issues — users may only like some features. For example, when using both OpenSpec and Superpowers, one might only use OpenSpec's Spec management capabilities, but prefer Superpowers' TDD-driven approach for coding.

Long-term Skill users know these capabilities can be freely combined, but exactly how to do so still requires real practice. The Comet project can serve as a reference:

- **How to reliably trigger nested Skills** — Not letting the Agent rely on document descriptions to perform "look-alike Skill trigger" operations (like writing files based on Skill descriptions), but truly triggering Skills (key feature: Skill trigger prints on CC). Comet triggers many capabilities from OpenSpec and Superpowers. How is this Prompt written?
- **How to make combined Skills flow automatically across phases** — Not relying on manual intervention. Comet's 5-phase flow can automatically trigger Skills for the core process except for necessary user choices, while the state machine also protects state transition reliability.
- **How to turn the Spec lifecycle into a resumable workflow** — Comet links OpenSpec change/spec artifacts with Superpowers design and planning documents, then records phase, execution mode, verification results, and archive status in `.comet.yaml`, so the Agent can resume after interruption instead of rereading documents and guessing progress.
- **How to turn document synchronization from "user reminders" into automation** — Comet puts handoff, state updates, validation, and archive sync into scripted flows, reducing repeated prompts like "remember to update the design doc", "remember to sync the spec", and "remember to archive the change".
- **How to design guard conditions that Agents can execute** — Comet does not simply trust the Agent saying "done" at phase exits. Scripts such as `comet-guard.sh`, `comet-yaml-validate.sh`, and `comet-state.sh` check tasks, state fields, verification evidence, and archive conditions before allowing the workflow to advance.
- **How to distribute and install Skills across platforms** — Comet supports multiple AI coding platforms, project/global installation, Chinese/English Skill choices, and platform-specific directory differences such as Antigravity using different project-level and global paths. It can be a reference for CLI installers and Skill package structure.
- **How to turn shell scripts into Agent workflow infrastructure** — Comet's scripts need to work across macOS, Linux, and Windows Git Bash while handling hashes, YAML fields, state machines, and archive flows. It shows how to move fragile workflow control out of scattered Prompt text and into testable, reusable tools.

## Install

Requirements:

- Node.js 20+
- npm/npx
- Git
- Bash-compatible shell for workflow scripts (Windows users should use Git Bash or an equivalent bash environment)
```
npm install -g @rpamis/comet
```

## Quick Start

```
cd your-project
comet init
```

`comet init` will:

1. Prompt you to select AI platforms (auto-detects existing configs)
2. Choose install scope: project-level (current directory) or global (home directory)
3. Select language for Comet skills: English or 中文
4. Install [OpenSpec](https://github.com/Fission-AI/OpenSpec) skills
5. Install [Superpowers](https://github.com/obra/superpowers) skills
6. Deploy Comet skills (in your chosen language) to selected platforms
7. Create `docs/superpowers/specs/` and `docs/superpowers/plans/` working directories for project-scope installs

> [!tip] Tip
> update version
> 
> `comet update` or `npm install -g @rpamis/comet@latest` to get the latest features and fixes.

## Support for OpenClaw and Hermes, and other AI platforms

For platforms that use the generic `skills` CLI directly, you can install the Comet skill package with:

```
npx skills add rpamis/comet
```

## Screenshots

[![runner](https://github.com/rpamis/comet/raw/master/img/runner.png)](https://github.com/rpamis/comet/blob/master/img/runner.png)

Auto-install OpenSpec & Superpowers, one-click dev environment setup

Multi-phase Skill entry, auto-detects current Spec stage, auto-triggers core flow, manual review at key nodes

## Commands

`comet init [path]` — Initialize Comet workflow

Initializes OpenSpec, Superpowers, and Comet skills for selected AI coding platforms.

| Option | Description |
| --- | --- |
| `--yes` | Non-interactive mode, auto-select detected platforms (or all if none detected) |
| `--scope <scope>` | Install scope: `project` or `global` |
| `--skip-existing` | Skip already installed components |
| `--overwrite` | Overwrite already installed components |
| `--json` | Output structured JSON |

When multiple existing components are found on the same platform, interactive init offers one bulk choice: overwrite all, skip all, or choose per component.

`comet status [path]` — Show active changes and next workflow command

Displays active changes, task progress, and the recommended next Comet workflow command.

| Option | Description |
| --- | --- |
| `--json` | Output active changes with `nextCommand` |

`comet doctor [path]` — Diagnose Comet installation health

Checks project/global installation health, working directories, installed skills, scripts, and Comet state files.

| Option | Description |
| --- | --- |
| `--json` | Output structured diagnostic results |
| `--scope <scope>` | Diagnose `auto`, `project`, or `global` scope (default: `auto`) |

`comet update [path]` — Update Comet package and skills

Updates the npm package and refreshes installed Comet skills in detected project/global targets.

| Option | Description |
| --- | --- |
| `--json` | Output npm and skill update results as JSON |
| `--language <lang>` | Override detected skill language (`en`, `zh`) |
| `--scope <scope>` | Update only `global` or `project` scope |

| Command | Description |
| --- | --- |
| `comet --help` | Show help |
| `comet --version` | Show version |

## Supported Platforms

`comet init` supports 28 AI coding platforms:

View full platform list

| Platform | Skills Dir | Platform | Skills Dir |
| --- | --- | --- | --- |
| Claude Code | `.claude/` | Cursor | `.cursor/` |
| Codex | `.codex/` | OpenCode | `.opencode/` |
| Windsurf | `.windsurf/` | Cline | `.cline/` |
| RooCode | `.roo/` | Continue | `.continue/` |
| GitHub Copilot | `.github/` | Gemini CLI | `.gemini/` |
| Amazon Q Developer | `.amazonq/` | Qwen Code | `.qwen/` |
| Kilo Code | `.kilocode/` | Auggie | `.augment/` |
| Kiro | `.kiro/` | Lingma | `.lingma/` |
| Junie | `.junie/` | CodeBuddy | `.codebuddy/` |
| CoStrict | `.cospec/` | Crush | `.crush/` |
| Factory Droid | `.factory/` | iFlow | `.iflow/` |
| Pi | `.pi/` | Qoder | `.qoder/` |
| Antigravity | `.agents/` | Bob Shell | `.bob/` |
| ForgeCode | `.forge/` | Trae | `.trae/` |

Some platforms use different project and global directories. For example, OpenCode global installs use `.config/opencode`, Lingma global installs use `.lingma`, and Antigravity global installs use `.gemini/antigravity`.

## Skills

After `comet init`, three groups of skills are installed to the selected platform's `skills/` directory:

### Comet Skills

View Comet skills

| Skill | Description |
| --- | --- |
| `/comet` | Main entry — auto-detects phase and dispatches to sub-commands |
| `/comet-open` | Phase 1: Open a change (proposal, design, task breakdown) |
| `/comet-design` | Phase 2: Deep design (brainstorming, Design Doc) |
| `/comet-build` | Phase 3: Plan and build (implementation plan, code commits) |
| `/comet-verify` | Phase 4: Verify and finish (testing, verification report) |
| `/comet-archive` | Phase 5: Archive (delta spec sync, status annotation) |
| `/comet-hotfix` | Preset: Quick bug fix (skips brainstorming) |
| `/comet-tweak` | Preset: Small change (skips brainstorming and full plan) |

### Guard & Automation Scripts

View script list

| Script | Purpose |
| --- | --- |
| `comet-env.sh` | Script discovery helper — exports bundled script paths such as `COMET_GUARD`, `COMET_STATE`, `COMET_HANDOFF`, and `COMET_ARCHIVE` |
| `comet-guard.sh` | Phase transition guard — validates exit conditions, `--apply` auto-updates `.comet.yaml` |
| `comet-handoff.sh` | Design handoff — generates deterministic context packages from OpenSpec artifacts with SHA256 tracing |
| `comet-archive.sh` | One-command archive — validates state, syncs specs, moves to archive, updates status |
| `comet-yaml-validate.sh` | Schema validator — validates `.comet.yaml` structure and field values |
| `comet-state.sh` | Unified state management — init/set/get/check/scale, agents' exclusive YAML interface |

### OpenSpec Skills

Spec lifecycle management: propose, explore, sync, verify, archive, and more.

### Superpowers Skills

Development methodology: brainstorming, TDD, subagent-driven development, code review, plan writing, and more.

## Workflow

```
/comet
  ↓ auto-detect
/comet-open  -->  /comet-design  -->  /comet-build  -->  /comet-verify  -->  /comet-archive
(OpenSpec)         (Superpowers)       (Superpowers)       (Both)           (OpenSpec)

/comet-hotfix (preset path, skips brainstorming)
  open  -->  build  -->  verify  -->  archive

/comet-tweak (preset path, skips brainstorming and full plan)
  open  -->  lightweight build  -->  light verify  -->  archive
```

### Five Phases

| Phase | Command | Owner | Artifacts |
| --- | --- | --- | --- |
| 1\. Open | `/comet-open` | OpenSpec | proposal.md, design.md, tasks.md |
| 2\. Deep Design | `/comet-design` | Superpowers | Design Doc, delta spec |
| 3\. Plan & Build | `/comet-build` | Superpowers | Implementation plan, code commits |
| 4\. Verify & Finish | `/comet-verify` | Both | Verification report, branch handling |
| 5\. Archive | `/comet-archive` | OpenSpec | delta→main spec sync, archive |

### Core Principles

- **Brainstorming is non-skippable** — every change must go through deep design (except hotfix/tweak)
- **Delta specs are living documents** — freely editable during Phase 3, synced at archive
- **Keep tasks.md in sync** — check off each task as completed
- **Commit frequently** — one commit per task, message reflects design intent
- **Verify before archive** — `/comet-verify` must pass before `/comet-archive`

### State Management

Comet uses a decoupled state architecture with separate YAML files:

| File | Owner | Purpose |
| --- | --- | --- |
| `.openspec.yaml` | OpenSpec | Spec lifecycle, change metadata |
| `.comet.yaml` | Comet | Workflow phase, execution mode, verification status |

All states and execution phases are updated via scripts, and each phase verifies that tasks are truly complete before advancing. Compared to storing complex state rules only in Skill text, this script-backed state machine gives Comet more reliable phase transitions, correct YAML, and easier breakpoint recovery; agents can read the current Spec situation through Comet's built-in commands.

View key.comet.yaml fields

**Key Fields in `.comet.yaml`:**

```
workflow: full
phase: build
build_mode: subagent-driven-development
isolation: branch
verify_mode: null
design_doc: docs/superpowers/specs/YYYY-MM-DD-topic-design.md
plan: docs/superpowers/plans/YYYY-MM-DD-feature.md
verify_result: pending
verification_report: null
branch_status: pending
verified_at: null
archived: false
direct_override: false
build_command: null
verify_command: null
handoff_context: openspec/changes/<name>/.comet/handoff/design-context.json
handoff_hash: <sha256>
```

In full workflow, `build_mode`, `isolation`, and `verify_mode` may temporarily be `null`; `build_mode` and `isolation` must be resolved before `build → verify`. `verification_report` stays `null` until verification writes a report, and `verify-pass` requires that report to exist plus `branch_status: handled`. Fields after `archived` in the example are optional or script-derived: `direct_override` is only needed for full-workflow direct builds, project commands may be absent unless configured, and `handoff_context` / `handoff_hash` are recorded by `comet-handoff.sh` before leaving design. Projects can configure `build_command` / `verify_command` in the change or repo root, and guard will run those commands first and print failure output.

### Reliability Features

Comet ensures agent execution reliability through automated state transitions:

View reliability features
1. **Entry Verification** — Each phase validates preconditions before execution
	- Checks file existence, state consistency, and phase transitions
		- Outputs `[HARD STOP]` with actionable suggestions if validation fails
2. **Automated State Transitions** — `comet-guard.sh --apply` updates `.comet.yaml` automatically
	- All phase transitions (open → design/build → verify → archive) use `guard --apply`
		- No manual state editing required — eliminates write-verification errors
		- `comet-state.sh` is the agents' exclusive interface for state operations
		- Guard and archive scripts use `comet-state.sh` internally for state management
3. **Schema Validation** — `comet-yaml-validate.sh` ensures data integrity
	- Validates required and optional fields
		- Validates enum values, including `direct_override`
		- Validates `design_doc`, `plan`, and `handoff_context` paths exist, plus `handoff_hash` format
		- Detects unknown/typos fields
4. **Build Decision Enforcement** — Guard and state transitions both block skipped build choices
	- `isolation` must be `branch` or `worktree`
		- `build_mode` must be selected before leaving build
		- Full workflow `build_mode: direct` requires `direct_override: true`
5. **Verification Evidence** — Guard enforces proof before phase advance
	- `verify-pass` transition requires `verification_report` pointing to an existing report file
		- `branch_status` must be `handled` before verify can pass
		- Guard checks `verification_report exists` and `branch_status=handled` as hard prerequisites
		- Prevents false phase advances when verification or branch handling was skipped
6. **Archive Automation** — `comet-archive.sh` handles the full archive flow in one command
	- Validates entry state, syncs delta specs to main specs
		- Annotates design doc and plan frontmatter
		- Moves change to archive directory and updates `archived: true`
		- Supports `--dry-run` for preview

## Project Structure

```
your-project/
├── .claude/skills/              # Platform skills dir (Comet + OpenSpec + Superpowers)
│   ├── comet/SKILL.md
│   │   └── scripts/
│   │       ├── comet-guard.sh       # Phase transition guard (--apply auto-updates state)
│   │       ├── comet-env.sh         # Script discovery helper
│   │       ├── comet-handoff.sh     # Design handoff (OpenSpec → Superpowers context tracing)
│   │       ├── comet-archive.sh     # One-command archive automation
│   │       ├── comet-yaml-validate.sh # Schema validator
│   │       └── comet-state.sh       # Unified state management (init/set/get/check/scale)
│   ├── comet-*/SKILL.md
│   ├── openspec-*/SKILL.md
│   └── brainstorming/SKILL.md
├── openspec/                    # OpenSpec — WHAT
│   ├── config.yaml
│   └── changes/
│       └── <name>/
│           ├── .openspec.yaml       # OpenSpec state
│           ├── .comet.yaml          # Comet workflow state (decoupled)
│           ├── proposal.md
│           ├── design.md
│           ├── specs/<capability>/spec.md
│           └── tasks.md
└── docs/superpowers/            # Superpowers — HOW
    ├── specs/                   # Design documents
    └── plans/                   # Implementation plans
```

## Development

See [CONTRIBUTING.md](https://github.com/rpamis/comet/blob/master/CONTRIBUTING.md) for development setup, commit conventions, PR process, and guidance for adding platforms or skills.

See [CHANGELOG.md](https://github.com/rpamis/comet/blob/master/CHANGELOG.md) for version history and updates.

## Roadmap

Track our development progress and upcoming features on the [Comet Roadmap](https://github.com/orgs/rpamis/projects/1).

## Star History

[![Star History Chart](https://camo.githubusercontent.com/040bbac2bb2b56e5a300c236c3c9855a373d5e00c2a3ce5e2e43ed7383feabfd/68747470733a2f2f6170692e737461722d686973746f72792e636f6d2f7376673f7265706f733d7270616d69732f636f6d657426747970653d44617465)](https://star-history.com/#rpamis/comet&Date)

## Contributors

[![](https://camo.githubusercontent.com/5930d8d74451de1120bb1a8d29d1c3fb3b71ea5624ecaeeb35a49a1bd31fe025/68747470733a2f2f636f6e747269622e726f636b732f696d6167653f7265706f3d7270616d69732f636f6d657426636f6c756d6e733d313226616e6f6e3d31)](https://github.com/rpamis/comet/graphs/contributors)

## License

[MIT](https://github.com/rpamis/comet/blob/master/LICENSE)

## Reference

[LINUX DO - 新的理想型社区](https://linux.do/)