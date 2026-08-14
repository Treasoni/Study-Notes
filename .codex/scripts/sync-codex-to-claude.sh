#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$BASH_SOURCE")/../.." && pwd)"
exec python3 "$ROOT/.codex/scripts/sync-codex-to-claude.py" "$@"
