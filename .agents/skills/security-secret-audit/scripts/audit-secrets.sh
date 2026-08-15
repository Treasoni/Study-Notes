#!/usr/bin/env bash

# Report locations and rule names only. Matched content must never reach stdout.
set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DETECTOR="$SCRIPT_DIR/detect-secrets.pl"
RISK_DETECTOR="$SCRIPT_DIR/detect-risks.pl"
MODE="working-tree"
MAX_COMMITS=0
PROJECT_AUDIT=0
STRICT=0
FIX=0
SECRET_FINDINGS=0
RISK_FINDINGS=0
POLICY_FINDINGS=0
FAILURES=0
IGNORE_BEGIN='# security-secret-audit: local credentials'
IGNORE_END='# security-secret-audit: end local credentials'

usage() {
  cat <<'USAGE'
Usage: audit-secrets.sh [--staged | --history | --all] [--max-commits N] [--project] [--strict] [--fix]

  --staged          Scan files as staged in the Git index.
  --history         Scan each unique file version reachable from Git history.
  --all             Scan working tree, staged files, and history.
  --max-commits N   Limit commits used to collect historical file versions; 0 means all (default).
  --project         Also scan project-owned source/configuration risks and sensitive-file policy.
  --strict          Make project-risk findings fail with exit code 2; credential findings always fail.
  --fix             Preview, then add an idempotent local-credential block to .gitignore when safe.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --staged) MODE="staged" ;;
    --history) MODE="history" ;;
    --all) MODE="all" ;;
    --project) PROJECT_AUDIT=1 ;;
    --strict) STRICT=1 ;;
    --fix) FIX=1 ;;
    --max-commits)
      shift
      if [ "$#" -eq 0 ] || ! [[ "$1" =~ ^[0-9]+$ ]]; then
        printf '%s\n' 'error: --max-commits requires a non-negative integer' >&2
        exit 1
      fi
      MAX_COMMITS="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'error: unknown option: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

if [ "$STRICT" -eq 1 ] && [ "$PROJECT_AUDIT" -ne 1 ]; then
  printf '%s\n' 'error: --strict requires --project' >&2
  exit 2
fi
if [ "$FIX" -eq 1 ] && [ "$PROJECT_AUDIT" -ne 1 ]; then
  printf '%s\n' 'error: --fix requires --project' >&2
  exit 2
fi

if ! command -v perl >/dev/null 2>&1; then
  printf '%s\n' 'error: perl is required for the bundled detectors' >&2
  exit 1
fi

if [ ! -f "$DETECTOR" ] || { [ "$PROJECT_AUDIT" -eq 1 ] && [ ! -f "$RISK_DETECTOR" ]; }; then
  printf '%s\n' 'error: a bundled security detector is missing' >&2
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf '%s\n' 'error: run this command inside a Git working tree' >&2
  exit 1
fi

record_status() {
  local status="$1"
  local label="$2"
  local category="$3"

  case "$status" in
    0) ;;
    2)
      if [ "$category" = "secret" ]; then
        SECRET_FINDINGS=1
      else
        RISK_FINDINGS=1
      fi
      ;;
    *)
      printf 'error: could not scan %s\n' "$label" >&2
      FAILURES=1
      ;;
  esac
}

scan_file_with() {
  local detector="$1"
  local path="$2"
  local label="$3"
  local category="$4"
  local status=0

  perl "$detector" --label "$label" --path "$path" < "$path"
  status=$?
  record_status "$status" "$label" "$category"
}

scan_index_file_with() {
  local detector="$1"
  local path="$2"
  local label="$3"
  local category="$4"
  local status=0

  git show ":$path" 2>/dev/null | perl "$detector" --label "$label" --path "$path"
  status=${PIPESTATUS[1]}
  record_status "$status" "$label" "$category"
}

scan_history_blob() {
  local object="$1"
  local path="$2"
  local short_object="${object:0:12}"
  local source_path="${path:-history-blob-$short_object}"
  local label="history:$source_path"
  local status=0

  git cat-file blob "$object" 2>/dev/null | perl "$DETECTOR" --label "$label" --path "$source_path"
  status=${PIPESTATUS[1]}
  record_status "$status" "$label" "secret"
}

is_vendor_risk_path() {
  case "$1" in
    .obsidian/plugins/*) return 0 ;;
    *) return 1 ;;
  esac
}

scan_working_tree_file() {
  local path="$1"
  local label="$2"

  [ -f "$path" ] || return 0
  scan_file_with "$DETECTOR" "$path" "$label" "secret"
  if [ "$PROJECT_AUDIT" -eq 1 ] && ! is_vendor_risk_path "$path"; then
    scan_file_with "$RISK_DETECTOR" "$path" "$label" "risk"
  fi
}

scan_staged_file() {
  local path="$1"
  local label="index:$path"

  scan_index_file_with "$DETECTOR" "$path" "$label" "secret"
  if [ "$PROJECT_AUDIT" -eq 1 ] && ! is_vendor_risk_path "$path"; then
    scan_index_file_with "$RISK_DETECTOR" "$path" "$label" "risk"
  fi
}

history_objects() {
  if [ "$MAX_COMMITS" -gt 0 ]; then
    git rev-list --objects --all --max-count="$MAX_COMMITS"
  else
    git rev-list --objects --all
  fi
}

scan_working_tree() {
  local path

  while IFS= read -r -d '' path; do
    scan_working_tree_file "$path" "worktree:$path"
  done < <(git ls-files -z)

  while IFS= read -r -d '' path; do
    scan_working_tree_file "$path" "untracked:$path"
  done < <(git ls-files --others --exclude-standard -z)
}

scan_staged() {
  local path

  while IFS= read -r -d '' path; do
    scan_staged_file "$path"
  done < <(git diff --cached --name-only --diff-filter=ACMR -z)
}

scan_history() {
  local object
  local type
  local path

  while IFS=' ' read -r object type path; do
    [ "$type" = 'blob' ] || continue
    scan_history_blob "$object" "$path"
  done < <(history_objects | git cat-file --batch-check='%(objectname) %(objecttype) %(rest)' | awk '$2 == "blob"' | sort -u -k1,1)
}

record_policy_finding() {
  local path="$1"
  local rule="$2"

  printf 'policy:%s:0:%s\n' "$path" "$rule"
  POLICY_FINDINGS=1
}

audit_sensitive_file_policy() {
  local path

  while IFS= read -r -d '' path; do
    case "$path" in
      .env|.env.*)
        case "$path" in *.example|*.sample|*.template) ;; *) record_policy_finding "$path" "sensitive-file-tracked" ;; esac
        ;;
      *.key|*.p12|*.pfx) record_policy_finding "$path" "sensitive-file-tracked" ;;
    esac
  done < <(git ls-files -z)
}

audit_ignore_policy() {
  local pattern

  if [ ! -f .gitignore ] || ! grep -Fqx "$IGNORE_BEGIN" .gitignore || ! grep -Fqx "$IGNORE_END" .gitignore; then
    record_policy_finding '.gitignore' 'missing-local-credential-ignore-block'
    return
  fi
  while IFS= read -r pattern; do
    if ! grep -Fqx "$pattern" .gitignore; then
      record_policy_finding '.gitignore' 'incomplete-local-credential-ignore-block'
      return
    fi
  done <<'EOF'
.env
.env.*
!.env.example
!.env.sample
!.env.template
!.env.*.example
!.env.*.sample
!.env.*.template
*.key
*.p12
*.pfx
EOF
}

print_safe_ignore_block() {
  cat <<EOF
$IGNORE_BEGIN
.env
.env.*
!.env.example
!.env.sample
!.env.template
!.env.*.example
!.env.*.sample
!.env.*.template
*.key
*.p12
*.pfx
$IGNORE_END
EOF
}

apply_safe_ignore_fix() {
  local action='append-local-credential-ignore-block'
  local temporary

  if [ -f .gitignore ] && grep -Fqx "$IGNORE_BEGIN" .gitignore && grep -Fqx "$IGNORE_END" .gitignore; then
    if ignore_policy_is_current; then
      printf '%s\n' 'remediation-preview:.gitignore:0:local-credential-ignore-block-already-present'
      return 0
    fi
    action='replace-local-credential-ignore-block'
    temporary="$(mktemp "${TMPDIR:-/tmp}/security-secret-audit-gitignore.XXXXXX")"
    awk -v begin="$IGNORE_BEGIN" -v end="$IGNORE_END" '
      $0 == begin { managed = 1; next }
      managed && $0 == end { managed = 0; next }
      !managed { print }
    ' .gitignore > "$temporary"
    mv "$temporary" .gitignore
  elif [ -f .gitignore ] && grep -Fqx "$IGNORE_BEGIN" .gitignore; then
    printf '%s\n' 'error: managed .gitignore block has no end marker' >&2
    FAILURES=1
    return 1
  fi

  printf 'remediation-preview:.gitignore:0:%s\n' "$action"
  if [ -s .gitignore ]; then
    printf '\n' >> .gitignore
  fi
  print_safe_ignore_block >> .gitignore
  printf 'remediation-applied:.gitignore:0:%s\n' "$action"
}

ignore_policy_is_current() {
  local previous_policy="$POLICY_FINDINGS"

  POLICY_FINDINGS=0
  audit_ignore_policy >/dev/null
  if [ "$POLICY_FINDINGS" -eq 0 ]; then
    POLICY_FINDINGS="$previous_policy"
    return 0
  fi
  POLICY_FINDINGS="$previous_policy"
  return 1
}

case "$MODE" in
  working-tree)
    scan_working_tree
    ;;
  staged)
    scan_staged
    ;;
  history)
    scan_history
    ;;
  all)
    scan_working_tree
    scan_staged
    scan_history
    ;;
esac

if [ "$PROJECT_AUDIT" -eq 1 ]; then
  audit_sensitive_file_policy
  audit_ignore_policy
  if [ "$FIX" -eq 1 ]; then
    if [ "$SECRET_FINDINGS" -ne 0 ]; then
      printf '%s\n' 'remediation-skipped: credentials require manual removal and rotation; .gitignore alone is insufficient.' >&2
    else
      POLICY_FINDINGS=0
      apply_safe_ignore_fix
      audit_sensitive_file_policy
      audit_ignore_policy
    fi
  fi
fi

if [ "$FAILURES" -ne 0 ]; then
  printf '%s\n' 'Security audit did not finish successfully.' >&2
  exit 1
fi

if [ "$SECRET_FINDINGS" -ne 0 ]; then
  printf '%s\n' 'Potential credentials found. Do not commit or push until they are removed and, if real, rotated.' >&2
  exit 2
fi

if [ "$RISK_FINDINGS" -ne 0 ] || [ "$POLICY_FINDINGS" -ne 0 ]; then
  if [ "$STRICT" -eq 1 ]; then
    printf '%s\n' 'Project security audit found blocking risks.' >&2
    exit 2
  fi
  printf '%s\n' 'Project security audit completed with risks; review findings or rerun with --strict.' >&2
  exit 0
fi

printf '%s\n' 'Security audit passed: no potential credentials or selected project risks found.'
