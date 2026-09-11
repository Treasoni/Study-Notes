#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

this_dir=".codex"
# Skills do not live under this_dir: the profile's skill root is the shared
# template-kit directory, and the sync rewrites this line per runtime so each
# runtime guards its own tree. Do not point this at the retired .codex/skills
# legacy copy, or the guards below will scan stale files and miss real drift.
skills_dir=".claude/skills"

status=0

fail() {
  printf '\nFAIL: %s\n' "$1" >&2
  status=1
}

run_forbidden_pattern() {
  local label="$1"
  local pattern="$2"
  shift 2

  local tmp
  tmp="$(mktemp "${TMPDIR:-/tmp}/workflow-health.XXXXXX")"

  # `rg` is not guaranteed to exist in a child process: in the Claude Code
  # runtime it is only a shell function in the interactive shell, so this
  # script (and any pre-commit / CI caller) sees "command not found". Letting
  # that fall through to "no matches" would make the guards below silently pass
  # forever, so fall back to grep -E, which is always available.
  if command -v rg >/dev/null 2>&1; then
    rg -n --hidden -g '!.git/**' -g '!workspace/**' "$pattern" "$@" > "$tmp" || true
  else
    grep -rnE --exclude-dir=.git --exclude-dir=workspace "$pattern" "$@" > "$tmp" || true
  fi

  if [ -s "$tmp" ]; then
    printf '\n%s\n' "$label" >&2
    cat "$tmp" >&2
    fail "$label"
  fi
  rm -f "$tmp"
}

echo "Workflow health check"

run_forbidden_pattern \
  "Project-scoped todo.md references in active workflow instructions:" \
  '\$\{PROJECT_DIR\}/todo\.md|\$PROJECT_DIR/todo\.md' \
  "$this_dir/agents" \
  "$skills_dir/research-collector" \
  "$skills_dir/note-beautifier" \
  "$skills_dir/workflow-orchestrator" \
  "$this_dir/workflows"

run_forbidden_pattern \
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

# The validator lives at a fixed .agent-sync path, not under this_dir: it is a
# single canonical script both runtimes share, so the sync must not rewrite this
# line into two divergent copies. Without a caller it was dead code, which is how
# a host-absolute interpreter path reached a Windows checkout unnoticed.
if ! python3 .agent-sync/validate_portability.py --root .; then
  fail "Shared agent assets are not portable across machines."
fi

if [ "$status" -eq 0 ]; then
  echo "Workflow health check passed."
fi

exit "$status"
