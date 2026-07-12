#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  install.sh <target-project> [--with-skill] [--update-agents] [--force]

Options:
  --with-skill      Copy the whole workflow-todo-state skill into the target project.
  --update-agents   Add an idempotent Workflow Todo State block to AGENTS.md.
  --force           Replace existing installed files by moving them to timestamped backups.

Examples:
  .claude/skills/workflow-todo-state/scripts/install.sh ../other-project
  .claude/skills/workflow-todo-state/scripts/install.sh ../other-project --with-skill --update-agents
USAGE
}

if [ "$#" -lt 1 ]; then
  usage
  exit 2
fi

TARGET_PROJECT="$1"
shift

WITH_SKILL=false
UPDATE_AGENTS=false
FORCE=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --with-skill) WITH_SKILL=true ;;
    --update-agents) UPDATE_AGENTS=true ;;
    --force) FORCE=true ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "install: unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
  shift
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
STAMP="$(date +%Y%m%d%H%M%S)"

if [ ! -d "$TARGET_PROJECT" ]; then
  echo "install: target project does not exist: $TARGET_PROJECT" >&2
  exit 1
fi

TARGET_PROJECT="$(cd "$TARGET_PROJECT" && pwd)"

backup_existing_file() {
  local path="$1"
  local source="$2"
  if [ -e "$path" ]; then
    if [ -f "$path" ] && cmp -s "$source" "$path"; then
      echo "skipped: unchanged ${path}"
      return 2
    fi
    if [ "$FORCE" != true ]; then
      echo "install: already exists, use --force to replace: $path" >&2
      exit 1
    fi
    mv "$path" "${path}.bak.${STAMP}"
  fi
  return 0
}

backup_existing_path() {
  local path="$1"
  local source="${2:-}"
  if [ -e "$path" ]; then
    if [ -n "$source" ] && [ -d "$path" ] && [ -d "$source" ] && diff -qr "$source" "$path" >/dev/null 2>&1; then
      echo "skipped: unchanged ${path}"
      return 2
    fi
    if [ "$FORCE" != true ]; then
      echo "install: already exists, use --force to replace: $path" >&2
      exit 1
    fi
    mv "$path" "${path}.bak.${STAMP}"
  fi
  return 0
}

install_state_script() {
  local target_dir="${TARGET_PROJECT}/.claude/scripts"
  local target_script="${target_dir}/todo-state.sh"

  mkdir -p "$target_dir"
  if ! backup_existing_file "$target_script" "${SCRIPT_DIR}/todo-state.sh"; then
    return
  fi
  cp "${SCRIPT_DIR}/todo-state.sh" "$target_script"
  chmod +x "$target_script"
  echo "installed: ${target_script}"
}

install_skill() {
  local target_skills="${TARGET_PROJECT}/.claude/skills"
  local target_skill="${target_skills}/workflow-todo-state"

  mkdir -p "$target_skills"
  if ! backup_existing_path "$target_skill" "$SKILL_DIR"; then
    return
  fi
  cp -R "$SKILL_DIR" "$target_skill"
  chmod +x "${target_skill}/scripts/todo-state.sh" "${target_skill}/scripts/install.sh"
  echo "installed: ${target_skill}"
}

update_agents() {
  local agents_file="${TARGET_PROJECT}/AGENTS.md"
  local start_marker="<!-- workflow-todo-state:start -->"
  local end_marker="<!-- workflow-todo-state:end -->"

  if [ -f "$agents_file" ] && grep -qF "$start_marker" "$agents_file"; then
    echo "skipped: AGENTS.md already contains workflow-todo-state block"
    return
  fi

  if [ ! -f "$agents_file" ]; then
    printf '# Project Instructions\n' > "$agents_file"
  fi

  cat >> "$agents_file" <<'AGENTS_BLOCK'

<!-- workflow-todo-state:start -->
## Workflow Todo State

Multi-phase agent workflows must use a project-local `todo.md` as the source of truth.

- Read the target project `todo.md` before starting any phase.
- Do not skip prerequisite phases.
- Change phase state only through `.claude/scripts/todo-state.sh`.
- Use one unique phase status line per phase, for example `> [P0] ⬜ 未开始`.
- On resume after interruption, inspect the YAML frontmatter and current phase before acting.
<!-- workflow-todo-state:end -->
AGENTS_BLOCK

  echo "updated: ${agents_file}"
}

install_state_script

if [ "$WITH_SKILL" = true ]; then
  install_skill
fi

if [ "$UPDATE_AGENTS" = true ]; then
  update_agents
fi

cat <<EOF

Done.

Next:
  1. Create or retrofit a todo.md in the target project.
  2. Test: .claude/scripts/todo-state.sh path/to/todo.md start P0
EOF
