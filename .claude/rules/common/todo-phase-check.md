# Todo Phase Check

Copied ahead of time: stable shared step-0 preamble for all subagents and skills. Each agent/skill only needs a one-liner referencing its own phase section.

## Common Preamble (all agents and skills)

```bash
# Read project slug from intent file
PROJECT_SLUG=$(grep "项目标识" ${WORKSPACE_PATH:-./workspace}/*/00_intent.md 2>/dev/null | head -1 | sed 's/.*：//')

# If multiple projects, prompt user to select
if [ -z "$PROJECT_SLUG" ]; then
  echo "Found projects:"
  ls -d ${WORKSPACE_PATH:-./workspace}/*/ 2>/dev/null | xargs -I {} basename {}
  echo "Please specify project name"
  exit 1
fi

PROJECT_DIR="${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}"

# Read todo.md
cat ${PROJECT_DIR}/todo.md 2>/dev/null || echo "NOT FOUND"
```

## Phase 3: outline-generator

Status check:
- If todo.md does not exist: Inform user to run `/research-planner` first
- If todo.md exists but Phase 2 is ⬜ or 🔲: Inform user "Deep research phase not completed. Please complete `/research-collector` first"
- If todo.md exists and Phase 2 is ✅, Phase 3 is ⬜: Allow execution, update Phase 3 to 🔲
- If todo.md exists and Phase 3 is already ✅: Ask user "Outline already exists. Regenerate?"

Start:
```bash
sed -i '' 's/\[P3\] ⬜ 未开始/[P3] 🔲 进行中/' ${PROJECT_DIR}/todo.md
```

Complete:
```bash
sed -i '' 's/\[P3\] 🔲 进行中/[P3] ✅ 已完成/' ${PROJECT_DIR}/todo.md
sed -i '' 's/当前阶段：阶段 [0-9]/当前阶段：阶段 4/g' ${PROJECT_DIR}/todo.md
```

## Phase 4: chapter-writer

Status check:
- If todo.md does not exist: Inform user to run `/research-planner` first
- If todo.md exists but Phase 3 is ⬜ or 🔲: Inform user "Outline not completed. Please complete `outline-generator` first"
- If todo.md exists and Phase 3 is ✅, Phase 4 is ⬜: Allow execution, update Phase 4 to 🔲
- If todo.md exists and Phase 4 is partially complete: Resume from last completed chapter

Start:
```bash
sed -i '' 's/\[P4\] ⬜ 未开始/[P4] 🔲 进行中/' ${PROJECT_DIR}/todo.md
```

Each chapter complete:
- Update the corresponding chapter checkbox in todo.md to ✅
- Track completed chapters in todo.md

All chapters complete:
```bash
sed -i '' 's/\[P4\] 🔲 进行中/[P4] ✅ 已完成/' ${PROJECT_DIR}/todo.md
sed -i '' 's/当前阶段：阶段 [0-9]/当前阶段：阶段 5/g' ${PROJECT_DIR}/todo.md
```

## Phase 5: note-assembler

Status check:
- If todo.md does not exist: Inform user to run `/research-planner` first
- If todo.md exists but Phase 4 is ⬜ or 🔲: Inform user "Chapter writing not completed. Please complete `chapter-writer` first"
- If todo.md exists and Phase 4 is ✅, Phase 5 is ⬜: Allow execution, update Phase 5 to 🔲
- If todo.md exists and Phase 5 is already ✅: Ask user "Assembly already exists. Reassemble?"

Start:
```bash
sed -i '' 's/\[P5\] ⬜ 未开始/[P5] 🔲 进行中/' ${PROJECT_DIR}/todo.md
```

Complete:
```bash
sed -i '' 's/\[P5\] 🔲 进行中/[P5] ✅ 已完成/' ${PROJECT_DIR}/todo.md
sed -i '' 's/当前阶段：阶段 [0-9]/当前阶段：阶段 6/g' ${PROJECT_DIR}/todo.md
```

## Phase 6: note-beautifier

Status check:
- If todo.md does not exist: Inform user to run `/research-planner` first
- If todo.md exists but Phase 5 is ⬜ or 🔲: Inform user "Note assembly not completed. Please complete `note-assembler` first"
- If todo.md exists and Phase 5 is ✅, Phase 6 is ⬜: Allow execution, update Phase 6 to 🔲
- If todo.md exists and Phase 6 is already ✅: Ask user "Beautification already done. Redo?"

Start:
```bash
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" start P6
```

Complete:
```bash
.claude/scripts/todo-state.sh "${PROJECT_DIR}/todo.md" complete P6
```
