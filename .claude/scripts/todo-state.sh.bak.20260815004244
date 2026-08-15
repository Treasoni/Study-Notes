#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> start P1
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> confirm P1 "user approval"
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> complete P1
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> skip P3 "reason"
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> block P2 "reason"
  <agent-dir>/scripts/todo-state.sh <workflow-state.md> mode P2 freeform "reason"

Enforces confirmed phase completion, bounded skips, and configured mode changes.
USAGE
}

if [ "$#" -lt 3 ]; then
  usage
  exit 2
fi

TODO_FILE="$1"
ACTION="$2"
PHASE="$3"
REASON=""
SELECTED_MODE=""

if [ ! -f "$TODO_FILE" ]; then
  echo "todo-state: file not found: $TODO_FILE" >&2
  exit 1
fi

case "$ACTION" in
  start|complete) ;;
  confirm|skip|block)
    if [ "$#" -ge 4 ]; then REASON="$4"; fi
    ;;
  mode)
    if [ "$#" -ge 4 ]; then SELECTED_MODE="$4"; fi
    if [ "$#" -ge 5 ]; then REASON="$5"; fi
    ;;
  *)
    echo "todo-state: unknown action: $ACTION" >&2
    usage
    exit 2
    ;;
esac

case "$PHASE" in
  P[0-9]*) ;;
  *)
    echo "todo-state: phase must look like P0, P1, ..." >&2
    exit 2
    ;;
esac

if ! grep -qE "^> \[$PHASE\] " "$TODO_FILE"; then
  echo "todo-state: phase line not found: $PHASE" >&2
  exit 1
fi

TODAY="$(date +%Y-%m-%d)"
NOW="$(date '+%Y-%m-%d %H:%M')"
PHASE_NUM="${PHASE#P}"

yaml_quote() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '"%s"' "$value"
}

ensure_frontmatter() {
  if [ "$(sed -n '1p' "$TODO_FILE")" = "---" ]; then
    return
  fi

  local tmp
  tmp="$(mktemp "${TODO_FILE}.XXXXXX")"
  {
    printf '%s\n' '---'
    printf '%s\n' 'workflow: unknown'
    printf '%s\n' 'topic: ""'
    printf '%s\n' 'project_slug: ""'
    printf '%s\n' 'created_at: ""'
    printf 'last_updated: "%s"\n' "$TODAY"
    printf 'current_phase: %s\n' "$PHASE"
    printf '%s\n' 'current_status: unknown'
    printf '%s\n' 'mode: standard'
    printf '%s\n' 'confirmed_phases: ""'
    printf '%s\n' 'skippable_phases: ""'
    printf '%s\n' 'mode_dependent_skips: ""'
    printf '%s\n' 'allowed_modes: ""'
    printf '%s\n' 'mode_change_phase: ""'
    printf '%s\n' 'blocked_reason: ""'
    printf '%s\n' '---'
    cat "$TODO_FILE"
  } > "$tmp"
  mv "$tmp" "$TODO_FILE"
}

set_frontmatter_key() {
  local key="$1"
  local value="$2"
  local tmp
  tmp="$(mktemp "${TODO_FILE}.XXXXXX")"
  awk -v key="$key" -v value="$value" '
    NR == 1 && $0 == "---" { in_fm = 1; print; next }
    in_fm && $0 == "---" {
      if (!done) print key ": " value
      in_fm = 0
      print
      next
    }
    in_fm && index($0, key ":") == 1 {
      print key ": " value
      done = 1
      next
    }
    { print }
  ' "$TODO_FILE" > "$tmp"
  mv "$tmp" "$TODO_FILE"
}

set_recovery_state() {
  local current_phase="$1"
  local current_status="$2"
  local blocked_reason="${3:-}"

  ensure_frontmatter
  set_frontmatter_key "last_updated" "$(yaml_quote "$TODAY")"
  set_frontmatter_key "current_phase" "$current_phase"
  set_frontmatter_key "current_status" "$current_status"
  set_frontmatter_key "blocked_reason" "$(yaml_quote "$blocked_reason")"
}

set_visible_current_phase() {
  local current_phase="$1"
  local label="$current_phase"

  case "$current_phase" in
    P[0-9]*) label="阶段 ${current_phase#P}" ;;
    done) label="完成" ;;
  esac

  LABEL="$label" perl -0pi -e 's/(^> 当前阶段：).*$/$1$ENV{LABEL}/m' "$TODO_FILE"
}

replace_phase_status() {
  local label="$1"
  PHASE="$PHASE" LABEL="$label" perl -0pi -e '
    my $phase = $ENV{PHASE};
    my $label = $ENV{LABEL};
    my $changed = s/(^> \[\Q$phase\E\] ).*$/$1$label/m;
    die "todo-state: could not update phase line\n" unless $changed;
  ' "$TODO_FILE"
}

phase_has_status() {
  local label="$1"
  grep -qF "> [$PHASE] $label" "$TODO_FILE"
}

frontmatter_value() {
  local key="$1"
  awk -v key="$key" '
    $0 == "---" { if (seen) exit; seen = 1; next }
    seen && index($0, key ":") == 1 {
      value = substr($0, length(key) + 2)
      sub(/^[[:space:]]+/, "", value)
      sub(/[[:space:]]+$/, "", value)
      if (value ~ /^".*"$/) { sub(/^"/, "", value); sub(/"$/, "", value) }
      print value
      exit
    }
  ' "$TODO_FILE"
}

csv_contains() {
  case ",$1," in *",$2,"*) return 0 ;; *) return 1 ;; esac
}

require_nonempty_reason() {
  if [ -z "$2" ]; then
    echo "todo-state: $1 requires a non-empty reason" >&2
    exit 1
  fi
}

require_phase_in_progress() {
  if ! phase_has_status "🔲 进行中"; then
    echo "todo-state: phase must be in progress: $PHASE" >&2
    exit 1
  fi
}

append_table_row() {
  local heading="$1" row="$2" tmp
  if ! grep -qF "$heading" "$TODO_FILE"; then
    echo "todo-state: missing audit table: $heading" >&2
    exit 1
  fi
  tmp="$(mktemp "$TODO_FILE.XXXXXX")"
  if ! awk -v heading="$heading" -v row="$row" '
    $0 == heading { print; in_section = 1; next }
    in_section && /^\|[-:| ]+\|$/ { print; print row; in_section = 0; inserted = 1; next }
    { print }
    END { if (!inserted) exit 3 }
  ' "$TODO_FILE" > "$tmp"; then
    rm -f "$tmp"
    echo "todo-state: could not append audit row for $heading" >&2
    exit 1
  fi
  mv "$tmp" "$TODO_FILE"
}

append_confirmation() {
  local confirmed
  confirmed="$(frontmatter_value confirmed_phases)"
  if csv_contains "$confirmed" "$PHASE"; then
    echo "todo-state: phase is already confirmed: $PHASE" >&2
    exit 1
  fi
  if [ -n "$confirmed" ]; then confirmed="$confirmed,$PHASE"; else confirmed="$PHASE"; fi
  set_frontmatter_key "confirmed_phases" "$(yaml_quote "$confirmed")"
  append_table_row "## 用户确认记录" "| $PHASE | $REASON | $NOW |"
  set_frontmatter_key "last_updated" "$(yaml_quote "$TODAY")"
}

append_skip_record() {
  append_table_row "## 跳过记录" "| $PHASE | user approved skip | $REASON | $NOW |"
  set_frontmatter_key "last_updated" "$(yaml_quote "$TODAY")"
}

require_skippable_phase() {
  if csv_contains "$(frontmatter_value skippable_phases)" "$PHASE"; then return; fi
  if csv_contains "$(frontmatter_value mode_dependent_skips)" "$PHASE" && [ "$(frontmatter_value mode)" = "freeform" ]; then return; fi
  echo "todo-state: phase is not skippable in the current workflow mode: $PHASE" >&2
  exit 1
}

append_mode_record() {
  if grep -qF "## 方向调整记录" "$TODO_FILE"; then
    append_table_row "## 方向调整记录" "| $NOW | $1 | $2 | $REASON |"
  fi
}

previous_open_phase_before() {
  PHASE_NUM="$PHASE_NUM" perl -ne '
    if (/^> \[P(\d+)\] (.*)$/ && $1 < $ENV{PHASE_NUM}) {
      my $status = $2;
      if ($status !~ /^✅ 已完成/ && $status !~ /^⏭️ 跳过/) {
        print "P$1\n";
        exit;
      }
    }
  ' "$TODO_FILE"
}

ensure_previous_phases_closed() {
  local open_phase
  open_phase="$(previous_open_phase_before || true)"
  if [ -n "$open_phase" ]; then
    echo "todo-state: previous phase is not complete or skipped: $open_phase" >&2
    exit 1
  fi
}

next_pending_phase_after() {
  PHASE_NUM="$PHASE_NUM" perl -ne '
    if (/^> \[P(\d+)\] .*⬜ 未开始/ && $1 > $ENV{PHASE_NUM}) {
      print "P$1\n";
      exit;
    }
  ' "$TODO_FILE"
}

append_exception_record() {
  local issue="$1"
  local handling="$2"
  issue="${issue//|//}"
  handling="${handling//|//}"
  NOW="$NOW" PHASE="$PHASE" ISSUE="$issue" HANDLING="$handling" perl -0pi -e '
    my $row = "| $ENV{NOW} | $ENV{PHASE} | $ENV{ISSUE} | $ENV{HANDLING} |\n";
    s/(## 异常记录\n\n\|[^\n]*\n\|[^\n]*\n)/$1$row/s;
  ' "$TODO_FILE"
}

case "$ACTION" in
  start)
    ensure_previous_phases_closed
    if phase_has_status "✅ 已完成" || phase_has_status "⏭️ 跳过" || phase_has_status "🔲 进行中"; then
      echo "todo-state: cannot start closed or active phase: $PHASE" >&2
      exit 1
    fi
    replace_phase_status "🔲 进行中"
    set_recovery_state "$PHASE" "in_progress"
    set_visible_current_phase "$PHASE"
    ;;
  confirm)
    require_phase_in_progress
    require_nonempty_reason "confirm" "$REASON"
    append_confirmation
    ;;
  complete)
    ensure_previous_phases_closed
    if phase_has_status "⏭️ 跳过"; then
      echo "todo-state: cannot complete skipped phase: $PHASE" >&2
      exit 1
    fi
    if ! phase_has_status "🔲 进行中"; then
      echo "todo-state: phase must be in progress before complete: $PHASE" >&2
      exit 1
    fi
    if ! csv_contains "$(frontmatter_value confirmed_phases)" "$PHASE"; then
      echo "todo-state: phase requires recorded user confirmation before completion: $PHASE" >&2
      exit 1
    fi
    replace_phase_status "✅ 已完成"
    NEXT_PHASE="$(next_pending_phase_after || true)"
    if [ -n "$NEXT_PHASE" ]; then
      set_recovery_state "$NEXT_PHASE" "ready"
      set_visible_current_phase "$NEXT_PHASE"
    else
      set_recovery_state "done" "complete"
      set_visible_current_phase "done"
    fi
    ;;
  skip)
    ensure_previous_phases_closed
    require_phase_in_progress
    require_nonempty_reason "skip" "$REASON"
    require_skippable_phase
    replace_phase_status "⏭️ 跳过"
    append_skip_record
    append_exception_record "跳过阶段：${REASON:-未填写原因}" "继续推进到下一未完成阶段"
    NEXT_PHASE="$(next_pending_phase_after || true)"
    if [ -n "$NEXT_PHASE" ]; then
      set_recovery_state "$NEXT_PHASE" "ready"
      set_visible_current_phase "$NEXT_PHASE"
    else
      set_recovery_state "done" "complete"
      set_visible_current_phase "done"
    fi
    ;;
  block)
    ensure_previous_phases_closed
    require_phase_in_progress
    require_nonempty_reason "block" "$REASON"
    set_recovery_state "$PHASE" "blocked" "$REASON"
    set_visible_current_phase "$PHASE"
    append_exception_record "阻塞：${REASON:-未填写原因}" "停在当前阶段，等待用户确认或补充资料"
    ;;
  mode)
    require_phase_in_progress
    require_nonempty_reason "mode" "$REASON"
    if [ -z "$SELECTED_MODE" ]; then
      echo "todo-state: mode requires a mode value" >&2
      exit 1
    fi
    if [ "$PHASE" != "$(frontmatter_value mode_change_phase)" ]; then
      echo "todo-state: mode can change only at $(frontmatter_value mode_change_phase)" >&2
      exit 1
    fi
    if ! csv_contains "$(frontmatter_value allowed_modes)" "$SELECTED_MODE"; then
      echo "todo-state: unsupported mode: $SELECTED_MODE" >&2
      exit 1
    fi
    OLD_MODE="$(frontmatter_value mode)"
    set_frontmatter_key "mode" "$SELECTED_MODE"
    append_mode_record "$OLD_MODE" "$SELECTED_MODE"
    set_frontmatter_key "last_updated" "$(yaml_quote "$TODAY")"
    ;;
esac
