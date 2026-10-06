#!/usr/bin/env python3
"""Prompt-cache guard: freeze a baseline, then compare post-change usage against it.

Modes:
  --freeze    Compute a baseline JSON from the current ledger and write it.
  (default)   Compare post-baseline events against the newest baseline.

Acceptance protocol (frozen 2026-09-14):
  - Primary metric: full-price input per context (sum of input_tokens), median over contexts.
  - main layer:     PASS <= 0.70x baseline, STRETCH <= 0.50x, WARN > 0.90x, REGRESS > 1.00x.
  - subagent layer: PASS <= 0.50x baseline, WARN > 0.90x, REGRESS > 1.00x.
  - A verdict needs >= 10 post-change contexts in that layer (7 days or 10 contexts).
  - Config knobs (effortLevel / thinkingBudget / savedProviderEffort.claude) must keep the
    frozen values: silent drift invalidates the measurement, so it fails the guard outright.

Exit codes: 0 = ok or insufficient data, 1 = actionable problem (regression or knob drift),
2 = error. The freeze and compare paths share one stats function on purpose: generation-side
and check-side must not drift apart.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENTS = ROOT / ".llm" / "prompt-cache" / "usage-events.jsonl"
DEFAULT_SETTINGS = ROOT / ".claudian" / "claudian-settings.json"
DEFAULT_BASELINE_DIR = ROOT / ".llm" / "prompt-cache"
BASELINE_GLOB = "baseline-*.json"
KNOB_KEYS = ("effortLevel", "thinkingBudget", "savedProviderEffort.claude")


def load_events(path: str | Path) -> list[dict]:
    path = Path(path).expanduser()
    events = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def layer_of(event: dict) -> str:
    return "subagent" if (event.get("metadata") or {}).get("layer") == "subagent" else "main"


def stats(events: list[dict], cache_read_price_ratio: float) -> dict:
    groups: dict[str, list[int]] = collections.defaultdict(lambda: [0, 0, 0])
    for event in events:
        group = groups[event.get("input_reference") or "?"]
        group[0] += event.get("input_tokens") or 0
        group[1] += event.get("cache_read_tokens") or 0
        group[2] += 1
    fresh = sorted(g[0] for g in groups.values())
    cread = sorted(g[1] for g in groups.values())
    count = len(fresh)

    def percentile(values: list[int], fraction: float) -> int:
        return values[min(count - 1, int(fraction * count))] if count else 0

    fresh_total = sum(fresh)
    cread_total = sum(cread)
    return {
        "contexts": count,
        "events": sum(g[2] for g in groups.values()),
        "fresh_total": fresh_total,
        "cread_total": cread_total,
        "hit_rate": round(cread_total / (cread_total + fresh_total), 4) if (cread_total + fresh_total) else 0.0,
        "fresh_median_per_context": statistics.median(fresh) if count else 0,
        "fresh_p25": percentile(fresh, 0.25),
        "fresh_p75": percentile(fresh, 0.75),
        "cread_median_per_context": statistics.median(cread) if count else 0,
        "events_per_context": round(sum(g[2] for g in groups.values()) / count, 2) if count else 0,
        # Billed estimate: cache reads are cheaper, not free. The ratio is an assumption from
        # pricing, never a measured value; the primary metric stays full-price input.
        "billed_estimate": round(fresh_total + cread_total * cache_read_price_ratio),
    }


def read_knobs(path: str | Path) -> tuple[dict, str | None]:
    """Return only the guard-relevant knobs; never echo unrelated settings."""
    path = Path(path).expanduser()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, f"settings file not found: {path}"
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"cannot read settings: {exc}"
    knobs: dict[str, str] = {}
    if isinstance(data.get("effortLevel"), str):
        knobs["effortLevel"] = data["effortLevel"]
    if isinstance(data.get("thinkingBudget"), str):
        knobs["thinkingBudget"] = data["thinkingBudget"]
    saved = data.get("savedProviderEffort")
    if isinstance(saved, dict) and isinstance(saved.get("claude"), str):
        knobs["savedProviderEffort.claude"] = saved["claude"]
    return knobs, None


def verdict_for(layer: str, current: dict, baseline: dict, targets: dict) -> tuple[str, float | None, bool]:
    """Return (verdict, ratio, actionable)."""
    min_contexts = targets["min_contexts"]
    if current["contexts"] < min_contexts:
        return f"insufficient data ({current['contexts']}/{min_contexts} contexts)", None, False
    base_median = baseline["fresh_median_per_context"]
    if not base_median:
        return "no baseline median", None, False
    ratio = current["fresh_median_per_context"] / base_median
    pass_threshold = targets["main_pass"] if layer == "main" else targets["subagent_pass"]
    if ratio <= pass_threshold:
        verdict = "PASS"
        if layer == "main" and ratio <= targets["main_stretch"]:
            verdict = "STRETCH"
    elif ratio > 1.0:
        verdict = "REGRESS"
    elif ratio > targets["warn"]:
        verdict = "WARN"
    else:
        verdict = "OK"
    return verdict, round(ratio, 3), verdict == "REGRESS"


def newest_baseline(directory: Path) -> Path:
    candidates = sorted(directory.glob(BASELINE_GLOB))
    if not candidates:
        raise SystemExit(f"error: no baseline file ({BASELINE_GLOB}) in {directory}; run --freeze first")
    return candidates[-1]


def cmd_freeze(args: argparse.Namespace) -> int:
    if not Path(args.events).expanduser().exists():
        print(f"error: ledger not found: {args.events}", file=sys.stderr)
        return 2
    events = load_events(args.events)
    if not events:
        print(f"error: no events in {args.events}", file=sys.stderr)
        return 2
    cut = max(event.get("timestamp") or "" for event in events)
    knobs, knob_error = read_knobs(args.settings)
    if knob_error:
        print(f"warning: {knob_error}", file=sys.stderr)
    targets = {
        "main_pass": 0.30,
        "main_stretch": 0.50,
        "subagent_pass": 0.50,
        "warn": 0.90,
        "min_contexts": 10,
    }
    # Targets are reductions, stored as thresholds the ratio must fall under.
    targets["main_pass"] = 1 - targets["main_pass"]
    targets["main_stretch"] = 1 - targets["main_stretch"]
    targets["subagent_pass"] = 1 - targets["subagent_pass"]
    ratio = args.cache_read_price_ratio
    by_layer = {layer: stats([e for e in events if layer_of(e) == layer], ratio) for layer in ("main", "subagent")}
    main_contexts = by_layer["main"]["contexts"] or 1
    baseline = {
        "schema": "prompt-cache-baseline/v1",
        "frozen_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "freeze_cut_utc": cut,
        "events_total": len(events),
        "pricing": {
            "cache_read_price_ratio": ratio,
            "note": "billed_estimate = fresh + ratio*cread; ratio is an assumption, not a measured price",
        },
        "targets": targets,
        "knobs": knobs,
        "layers": by_layer,
        "fanout": {
            "subagent_contexts_per_main_session": round(by_layer["subagent"]["contexts"] / main_contexts, 2),
            "subagent_fresh_share": round(
                by_layer["subagent"]["fresh_total"]
                / max(by_layer["main"]["fresh_total"] + by_layer["subagent"]["fresh_total"], 1),
                4,
            ),
        },
    }
    out = Path(args.out).expanduser() if args.out else DEFAULT_BASELINE_DIR / f"baseline-{datetime.now().date().isoformat()}.json"
    if out.exists() and not args.force:
        print(f"error: {out} exists; pass --force to overwrite (post-change data would be baked in)", file=sys.stderr)
        return 2
    out.write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"frozen baseline -> {out}")
    print(f"freeze cut (UTC): {cut}; events: {len(events)}")
    for layer in ("main", "subagent"):
        s = by_layer[layer]
        print(
            f"  {layer:<8} contexts={s['contexts']} events={s['events']} fresh={s['fresh_total']} "
            f"cread={s['cread_total']} hit={s['hit_rate']} fresh/ctx median={s['fresh_median_per_context']}"
        )
    print(f"  fanout={baseline['fanout']['subagent_contexts_per_main_session']} subagent fresh share={baseline['fanout']['subagent_fresh_share']}")
    print(f"  knobs frozen: {json.dumps(knobs)}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    baseline_path = Path(args.baseline).expanduser() if args.baseline else newest_baseline(DEFAULT_BASELINE_DIR)
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    cut = baseline["freeze_cut_utc"]
    ratio = baseline["pricing"]["cache_read_price_ratio"]
    events_path = Path(args.events).expanduser()
    # A machine without a local ledger cannot be measured, but that is absence of data,
    # not a regression: compare against zero post-change events instead of failing.
    events = [e for e in load_events(events_path) if (e.get("timestamp") or "") > cut] if events_path.exists() else []
    by_layer = {layer: stats([e for e in events if layer_of(e) == layer], ratio) for layer in ("main", "subagent")}
    knobs_now, knob_error = read_knobs(args.settings)
    expected = baseline.get("knobs") or {}
    knob_problems: list[str] = []
    knob_notes: list[str] = []
    if knob_error:
        # Same reasoning: a missing settings file on a non-Claudian machine is not drift.
        knob_notes.append(knob_error)
    for key in KNOB_KEYS:
        if knob_error:
            break
        want = expected.get(key)
        got = knobs_now.get(key)
        if want is not None and got != want:
            knob_problems.append(f"{key}={got!r} expected {want!r}")

    rows = []
    actionable = False
    for layer in ("main", "subagent"):
        verdict, rel, bad = verdict_for(layer, by_layer[layer], baseline["layers"][layer], baseline["targets"])
        actionable = actionable or bad
        rows.append((layer, by_layer[layer], verdict, rel))
    if knob_problems:
        actionable = True

    if args.json:
        print(json.dumps({
            "baseline": str(baseline_path),
            "freeze_cut_utc": cut,
            "post_change_events": len(events),
            "layers": {layer: s for layer, s, _v, _r in rows},
            "verdicts": {layer: {"verdict": v, "ratio": r} for layer, _s, v, r in rows},
            "knobs": {"expected": expected, "actual": knobs_now, "problems": knob_problems, "notes": knob_notes},
            "actionable": actionable,
        }, indent=2, ensure_ascii=False))
        return 1 if actionable else 0

    if args.quiet and not actionable:
        return 0

    print(f"prompt-cache guard — baseline {baseline_path.name} (frozen {baseline.get('frozen_at')})")
    print(f"freeze cut: {cut}; post-change events: {len(events)}")
    print(f"{'layer':<9} {'ctx':>5} {'fresh':>12} {'cread':>13} {'hit':>7} {'fresh/ctx med':>14} {'vs base':>8}  verdict")
    for layer, s, verdict, rel in rows:
        rel_text = f"{rel:.3f}x" if rel is not None else "—"
        print(
            f"{layer:<9} {s['contexts']:>5} {s['fresh_total']:>12} {s['cread_total']:>13} "
            f"{s['hit_rate']:>7.4f} {s['fresh_median_per_context']:>14.0f} {rel_text:>8}  {verdict}"
        )
    for line in knob_problems:
        print(f"KNOB DRIFT: {line}")
    for line in knob_notes:
        print(f"note: {line}")
    if not knob_problems and not knob_notes:
        print("knobs: " + ", ".join(f"{k}={knobs_now.get(k)}" for k in KNOB_KEYS) + "  OK")
    if actionable:
        sys.stdout.flush()
        print("verdict: ACTIONABLE — investigate before trusting further measurements", file=sys.stderr)
    elif all(v.startswith("insufficient") for _l, _s, v, _r in rows):
        print(f"verdict: PENDING — need >={baseline['targets']['min_contexts']} post-change contexts per layer")
    else:
        print("verdict: see per-layer verdicts above")
    return 1 if actionable else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--events", default=str(DEFAULT_EVENTS), help=f"usage ledger (default: {DEFAULT_EVENTS})")
    parser.add_argument("--settings", default=str(DEFAULT_SETTINGS), help="Claudian settings file to check knobs in")
    parser.add_argument("--baseline", default=None, help="baseline JSON (default: newest baseline-*.json next to this script)")
    parser.add_argument("--freeze", action="store_true", help="write a new baseline instead of comparing")
    parser.add_argument("--out", default=None, help="--freeze output path (default: baseline-<date>.json)")
    parser.add_argument("--force", action="store_true", help="allow --freeze to overwrite an existing baseline")
    parser.add_argument("--cache-read-price-ratio", type=float, default=0.1, help="assumed cache-read price ratio for the billed estimate (default 0.1)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--quiet", action="store_true", help="print nothing unless actionable (for health checks)")
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    return cmd_freeze(args) if args.freeze else cmd_compare(args)


if __name__ == "__main__":
    raise SystemExit(main())
