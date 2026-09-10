#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

this_dir=".codex"
skills_dir=".codex/skills"

status=0

fail() {
  printf '\nFAIL: %s\n' "$1" >&2
  status=1
}

run_forbidden_rg() {
  local label="$1"
  local pattern="$2"
  shift 2

  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/workflow-health.XXXXXX")"
  if rg -n --hidden -g '!.git/**' -g '!workspace/**' "$pattern" "$@" > "$tmp"; then
    printf '\n%s\n' "$label" >&2
    cat "$tmp" >&2
    fail "$label"
  fi
  rm -f "$tmp"
}

echo "Workflow health check"

run_forbidden_rg \
  "Project-scoped todo.md references in active workflow instructions:" \
  '\$\{PROJECT_DIR\}/todo\.md|\$PROJECT_DIR/todo\.md' \
  "$this_dir/agents" \
  "$skills_dir/research-collector" \
  "$skills_dir/note-beautifier" \
  "$skills_dir/workflow-orchestrator" \
  "$this_dir/workflows"

run_forbidden_rg \
  "Manual phase-status sed edits in active workflow instructions:" \
  'sed -i .*\[P[0-9]' \
  "$this_dir/agents" \
  "$skills_dir/research-collector" \
  "$skills_dir/note-beautifier" \
  "$skills_dir/workflow-orchestrator" \
  "$this_dir/workflows"

if [ -d "$skills_dir/workflow-orchestrator/templates" ] &&
  find "$skills_dir/workflow-orchestrator/templates" -type f -name '*-todo.md' | grep -q .; then
  find "$skills_dir/workflow-orchestrator/templates" -type f -name '*-todo.md' >&2
  fail "Legacy workflow-orchestrator todo templates are still present."
fi

# State templates must declare the frontmatter keys the current todo-state.sh
# actually reads. The script only touches current_phase / current_status /
# blocked_reason / quality_gate / quality_gate_owner / quality_gate_due, and it
# refuses to complete the final phase without `quality_gate: passed`.
for template in "$this_dir"/workflows/*/state-template.md; do
  [ -f "$template" ] || continue

  if ! grep -qE '^quality_gate: ' "$template"; then
    printf '%s\n' "$template" >&2
    fail "Workflow state template is missing a quality_gate key: $template"
  fi

  if grep -nE '^(confirmed_phases|skippable_phases|mode_dependent_skips|allowed_modes|mode_change_phase):' "$template" >&2; then
    fail "Workflow state template still declares retired frontmatter keys: $template"
  fi
done

if ! "$this_dir/scripts/sync-workflow-routing.sh" --check; then
  fail "Workflow routing table is stale."
fi

if ! python3 "$this_dir/platform/manifest-registry.py" --root . validate; then
  fail "Agent Platform manifest registry validation failed."
fi

if [ "$status" -eq 0 ]; then
  echo "Workflow health check passed."
fi

exit "$status"
