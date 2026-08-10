#!/usr/bin/env python3
"""Collect LLM usage events from Claude Code transcripts into .llm/prompt-cache/usage-events.jsonl.

Event shape follows llm-usage-event.schema.json (same directory).
Idempotent: tracks processed (source file, message id) pairs in .collect-state.json.
Never logs raw prompts, responses, or personal data.

Known mapping (documented compatible equivalent):
  - latency_ms      -> null; Claude Code transcripts do not record per-request latency.
  - template_id     -> "claude-code.session"; every request is the session-level prompt.
  - cache_write     -> usage.cache_creation_input_tokens (0 in this environment).
  - request_type    -> inferred from the session's first user message via keyword rules.
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
from pathlib import Path

REQUIRED_FIELDS = [
    "timestamp", "request_type", "template_id", "template_version", "model",
    "input_tokens", "output_tokens", "latency_ms",
]

CLASSIFIER_RULES = [
    (r"更新|过时|refresh", "note_update"),
    (r"导入|迁移|已有笔记|import", "note_import"),
    (r"美化|发布|beautif|vault", "note_beautify"),
    (r"MOC|目录|索引", "moc_sync"),
    (r"缓存|token|审计.*调用|prompt.?cache", "prompt_cache"),
    (r"想学|研究|整理|学一下|了解|explore", "learning_note"),
    (r"技能|skill|agent|工作流|workflow", "system_workflow"),
]


def classify_request_type(first_user_text: str) -> str:
    for pattern, label in CLASSIFIER_RULES:
        if re.search(pattern, first_user_text, re.IGNORECASE):
            return label
    return "claude_code_general"


def first_user_text(session_path: Path) -> str:
    for line in open(session_path, encoding="utf-8", errors="replace"):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") != "user":
            continue
        msg = rec.get("message") or {}
        if not isinstance(msg, dict):
            continue
        content = msg.get("content")
        if isinstance(content, str) and content.strip() and not content.startswith("<system-reminder>"):
            return content.strip()[:200]
        if isinstance(content, list):
            texts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
            joined = " ".join(texts).strip()
            if joined and not joined.startswith("<system-reminder>"):
                return joined[:200]
    return ""


def default_project_dir() -> str:
    """Locate this vault's Claude Code transcript directory.

    The project slug is derived from the vault path by the harness (CJK paths
    are slugified into dashes), so it cannot be reconstructed from the vault
    path here. Resolution order:
      1. Known current slug for this vault (from the real transcript dir).
      2. Legacy slug used before the vault path changed.
      3. Fallback: the directory under ~/.claude/projects containing the
         most recently modified *.jsonl (the SessionEnd hook runs right after
         a session in this vault ends, so its transcript is the newest).
    """
    candidates = [
        Path.home() / ".claude" / "projects" / "-Users-zhqznc-Documents-----",
        Path.home() / ".claude" / "projects" / "c--note-Study-Notes",
    ]
    for c in candidates:
        if c.is_dir():
            return str(c)

    proj_root = Path.home() / ".claude" / "projects"
    best_dir, best_mtime = None, -1.0
    if proj_root.is_dir():
        for p in sorted(proj_root.iterdir()):
            if not p.is_dir():
                continue
            for f in p.glob("*.jsonl"):
                try:
                    mtime = f.stat().st_mtime
                except OSError:
                    continue
                if mtime > best_mtime:
                    best_mtime, best_dir = mtime, p
        if best_dir is not None:
            return str(best_dir)

    return str(Path.home() / ".claude" / "projects" / "c--note-Study-Notes")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        default=default_project_dir(),
        help="Directory of Claude Code session transcripts (default: this project's transcripts).",
    )
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent / "usage-events.jsonl"),
        help="Output events file (default: <skill-dir>/usage-events.jsonl).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report how many events would be added without writing.")
    args = parser.parse_args()

    out_path = Path(args.out)
    state_path = out_path.with_name(".collect-state.json")
    state: dict = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}

    new_events = []
    processed_pairs = 0
    for source_file in sorted(glob.glob(os.path.join(args.project, "*.jsonl"))):
        session_path = Path(source_file)
        rel_name = session_path.name
        request_type = classify_request_type(first_user_text(session_path))
        done_keys = set(state.get(rel_name, []))
        for line in open(source_file, encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("type") != "assistant":
                continue
            msg = rec.get("message") or {}
            usage = msg.get("usage") or {}
            if not usage or "input_tokens" not in usage:
                continue
            msg_id = msg.get("id") or rec.get("uuid") or ""
            if not msg_id or msg_id in done_keys:
                continue
            done_keys.add(msg_id)
            processed_pairs += 1
            if args.dry_run:
                continue
            event = {
                "timestamp": rec.get("timestamp", ""),
                "request_type": request_type,
                "template_id": "claude-code.session",
                "template_version": "v1",
                "model": msg.get("model") or "unknown",
                "input_tokens": usage.get("input_tokens", 0),
                "output_tokens": usage.get("output_tokens", 0),
                "cache_read_tokens": usage.get("cache_read_input_tokens"),
                "cache_write_tokens": usage.get("cache_creation_input_tokens"),
                "latency_ms": None,  # transcripts do not record per-request latency
                "status": "success",
                "input_reference": rel_name,  # safe: file name only, no content
                "metadata": {"source": "claude-code-transcript", "message_id": msg_id},
            }
            new_events.append(event)
        state[rel_name] = sorted(done_keys)

    if args.dry_run:
        print(f"would add {processed_pairs} events ({processed_pairs} new messages scanned, {len(state)} sessions tracked)")
        return 0

    with open(out_path, "a", encoding="utf-8") as fh:
        for event in new_events:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"added {len(new_events)} events to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
