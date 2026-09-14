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
  - subagent files  -> any <session>/subagents/agent-*.jsonl; request_type is "subagent" and
                       metadata carries layer / parent_session / attribution_agent.
                       (Added 2026-09-14: subagent spend was previously invisible here.)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
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


def hook_transcript_path() -> str | None:
    """Return Claude Code's current transcript path when invoked as a hook."""
    if sys.stdin.isatty():
        return None
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return None
    transcript_path = payload.get("transcript_path") if isinstance(payload, dict) else None
    return transcript_path if isinstance(transcript_path, str) and transcript_path else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project",
        help="Directory containing Claude Code session transcripts.",
    )
    parser.add_argument(
        "--transcript",
        default=hook_transcript_path(),
        help="One Claude Code transcript; supplied automatically by a hook.",
    )
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parent / "usage-events.jsonl"),
        help="Output events file (default: <skill-dir>/usage-events.jsonl).",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report how many events would be added without writing.")
    args = parser.parse_args()

    if args.transcript:
        transcript_path = Path(args.transcript).expanduser()
        if not transcript_path.is_file() or transcript_path.suffix != ".jsonl":
            parser.error("--transcript must name an existing .jsonl file")
        session_paths = [transcript_path]
        project_dir = transcript_path.parent
    elif args.project:
        project_dir = Path(args.project).expanduser()
        if not project_dir.is_dir():
            parser.error("--project must name an existing transcript directory")
        session_paths = sorted(project_dir.glob("*.jsonl"))
    else:
        parser.error("provide --project, --transcript, or invoke from a Claude Code hook")
    # Subagent transcripts live under <project>/<session>/subagents/agent-*.jsonl.
    sub_paths = sorted(project_dir.glob("*/subagents/agent-*.jsonl"))

    out_path = Path(args.out)
    state_path = out_path.with_name(".collect-state.json")
    state: dict = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}

    new_events = []
    processed_pairs = 0
    for session_path in session_paths + sub_paths:
        rel_name = session_path.name
        is_subagent = session_path.parent.name == "subagents"
        if is_subagent:
            key = f"{session_path.parent.parent.name}/subagents/{rel_name}"
            request_type = "subagent"
        else:
            key = rel_name
            request_type = classify_request_type(first_user_text(session_path))
        attribution_agent = None
        done_keys = set(state.get(key, []))
        for line in open(session_path, encoding="utf-8", errors="replace"):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if attribution_agent is None and rec.get("attributionAgent"):
                attribution_agent = rec["attributionAgent"]
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
            metadata = {"source": "claude-code-transcript", "message_id": msg_id}
            if is_subagent:
                metadata["layer"] = "subagent"
                metadata["parent_session"] = session_path.parent.parent.name
                if attribution_agent:
                    metadata["attribution_agent"] = attribution_agent
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
                "metadata": metadata,
            }
            new_events.append(event)
        state[key] = sorted(done_keys)

    if args.dry_run:
        print(
            f"would add {processed_pairs} events ({processed_pairs} new messages scanned; "
            f"{len(session_paths)} session + {len(sub_paths)} subagent transcripts)"
        )
        return 0

    with open(out_path, "a", encoding="utf-8") as fh:
        for event in new_events:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"added {len(new_events)} events to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
