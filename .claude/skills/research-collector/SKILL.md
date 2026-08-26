---
name: research-collector
description: Collect and curate technical research in two gated stages with compact source records. Use for systematic research, source gathering, research materials, or when a learning-note workflow is at collection phase P1 or P2.
---

# Research Collector

Produce reusable, source-backed research without repeatedly loading page bodies or reopening settled decisions.

## Contract

- Read `.claude/rules/common/prompt-cache.md` and the active `WORKFLOW_STATE_FILE` before work.
- The YAML frontmatter in the state file is authoritative. Use `.claude/scripts/todo-state.sh` for every phase transition.
- Run only P1 when P1 is pending; run only P2 when P1 is complete and P2 is pending. Stop at every user gate.
- Write artifacts under `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/`; never require a vault path.

## Source policy

Rank sources: official documentation and primary research first; reputable implementation reports second; community material only for labelled operational experience. Record URL, publisher, publication/update date when available, source tier, claim support, and retrieval date. Do not invent facts or silently merge conflicting claims.

## Environment preparation

P2 deep reading depends on the `crawl4ai` conda environment managed by `scripts/setup.sh` (idempotent; safe to re-run). The crawler entry point is `scripts/crawl.sh`.

Before the first crawl of a run:

1. Probe the environment with a lightweight call: `bash scripts/crawl.sh --help`.
2. If it exits 2 (conda missing, or the `crawl4ai` env missing), bootstrap once with `bash scripts/setup.sh`, then retry the crawl. Do not ask the user to install manually.
3. `setup.sh` pins `crawl4ai>=0.9,<1`; keep the pin — `crawl.py` is a 0.x compatibility layer and 1.x breaks its API.
4. If the crawl still exits 2 after a fresh setup, report the error to the user instead of retrying blindly.

## P1 — Explore

1. Read the intent artifact and select at most three independent research lenses.
2. Dispatch the smallest useful parallel set. Each delegate receives the same immutable role, output schema, source policy, and a final `Parameters` block containing only the lens and query.
3. Require 3–5 compact candidates per lens: title, URL, source tier, one-sentence relevance, date, and a 1–5 score. Delegates must return records, not copied page text.
4. Deduplicate by canonical URL and publish `01_explore_result.md` with a direction menu, coverage gaps, and estimated P2 scope.
5. Complete P1 and wait for the user's direction choice.

## P2 — Deep research

1. Reuse the accepted P1 candidates. Fetch only the selected 3–5 core sources and add sources solely to fill explicit gaps.
2. Extract claim-level notes with anchors or section names; keep quotations short and preserve source attribution.
3. Write `02_deep_research.md` with: scope, source table, claim/source map, contradictions, practical guidance, open questions, and a concise downstream handoff.
4. Keep full source bodies in local cache only when necessary for reproducibility; downstream stages receive paths, anchors, summaries, and source IDs.
5. Complete P2 and present source counts, tier mix, unresolved gaps, and the next user decision.

## Token and cache discipline

- Keep role, schema, quality bar, and tool set byte-stable within a request family; put query, dates, file excerpts, state, and URLs in the final parameter block.
- Read only the relevant sections of `01_explore_result.md` and `02_deep_research.md`; do not paste them into subagent prompts.
- Cap delegate output at 150 Chinese characters per source record and return source IDs plus conclusions to the parent.
- Reuse the same `template_id`, `template_version`, model, and fixed tool set for comparable runs. Record usage only through the project telemetry contract when the runtime supplies it.

## Completion criteria

- Every material claim maps to a source record or is explicitly marked as an inference.
- P1 or P2 output is present, compact, and matches the active state phase.
- The next phase is not started without the user gate.
