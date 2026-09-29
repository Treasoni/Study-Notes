---
name: research-collector
description: Collect and curate technical research in two gated stages with compact source records. Use for systematic research, source gathering, research materials, or when a learning-note workflow is at collection phase P1 or P2.
---

# Research Collector

Produce reusable, source-backed research without repeatedly loading page bodies or reopening settled decisions.

## Contract

- Read `.codex/rules/common/prompt-cache.md` and the active `WORKFLOW_STATE_FILE` before work.
- The YAML frontmatter in the state file is authoritative. Use `.codex/scripts/todo-state.sh` for every phase transition.
- Run only P1 when P1 is pending; run only P2 when P1 is complete and P2 is pending. Stop at every user gate.
- Write artifacts under `${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG}/`; never require a vault path.

## Source policy

Rank sources: official documentation and primary research first; reputable implementation reports second; community material only for labelled operational experience. Record URL, publisher, publication/update date when available, source tier, claim support, and retrieval date. Do not invent facts or silently merge conflicting claims.

**Never paraphrase a source claim into a dispatch prompt.** When handing work to a downstream writer, pass source IDs, paths, and anchors — not a rewritten sentence carrying a source ID. A writer cannot tell your summary from the original wording, so it will copy your phrasing and keep the citation, turning your paraphrase into a fabricated quotation. If a claim must appear in the prompt, quote it verbatim inside quotation marks, or label it explicitly as an unverified summary. When reviewing a chapter, re-open the source for every "官方口径是" / "the official wording is" claim instead of only checking that a source ID is attached.

**The intermediate artifact is not an authority.** `01_explore_result.md` and `02_deep_research.md` are **handoff artifacts, not trusted endpoints**. Every downstream writer that copies a quote or a number out of them inherits any corruption left there, and the corruption stays invisible because the citation still looks intact. So, at write-out time — not later, not at review time:

- A **verbatim quotation** enters the artifact only after a character-by-character comparison against the fetched source; record the source ID **and line number**. Never reconstruct a quote from memory or from an earlier summary of it. A single changed pronoun (`and argue that` → `we argue that`) survives every downstream check that only verifies "the cited sentence is present".
- A **number, default, version, or count** is recounted against the original, never re-transcribed. Counting rows in a fetched table means counting the **data rows** — header and separator rows are not properties (a 15-property comparison table was recorded as "17 axes" and propagated into three artifacts and 12 downstream locations).
- An artifact that carries quotes or numbers says so in its own handoff header, e.g. `> 本文件是中间产物：引文与数值请回 sources/ 按行号核对`, so the next reader does not have to infer it.
- If a value cannot be re-verified at write-out time, write the **semantics without the value** instead of a plausible number.

**Verify federal / aggregated registries at their own index, not in a local directory.** For a Skills Hub, plugin marketplace, package index, or model repository, find that registry's own central index or API endpoint and query **it**; a directory listing inside one repository is only one source among many (Hermes Skills Hub: an `official` branch of 150 entries out of 97,986). Before writing a universal negative ("there is no X", "nothing installable exists"), ask whether the scope you checked **equals** the scope of the sentence, and put that scope into the sentence itself ("only `openhue` in the `official` branch", not "only `openhue` in the Hub"). Index evidence carries a time qualifier ("as of YYYY-MM-DD").

## Retrieval pitfalls

A failed retrieval is not the same as an unavailable source. When the fetched artifact simply lacks the target passage, treat it as a **retrieval-method problem first** and try another path before downgrading the evidence.

- Discourse forums (`community.home-assistant.io`, `community.simon42.com` — URLs shaped `/t/<slug>/<id>`) expose **post bodies** only via `curl 'https://<host>/t/<id>.json'` (pagination `?page=N`, or read `post_stream.stream`). HTML / crawl4ai paths return 403/522, or **silently return only the SPA shell and the first-post teaser** without erroring — easy to misread as "source unavailable".
- Land every snapshot inside the repository (`${WORKSPACE_PATH}/${PROJECT_SLUG}/sources/…`) and read it back by repository-relative path. Do not use `/tmp` as a staging area between Bash calls: the sandbox `/tmp` mapping is not guaranteed stable across calls.
- Probe availability before designing around a tool: "the command exists" is not "the command is usable" (the `obsidian` binary was present while the CLI was not enabled). A one-call probe that reads a config file or a `--help` exit code is enough to change the plan.

## Environment preparation

P2 deep reading depends on the `crawl4ai` conda environment managed by `scripts/setup.sh` (idempotent; safe to re-run). The crawler entry point is `scripts/crawl.sh`.

Before the first crawl of a run:

1. Probe the environment with a lightweight call: `bash scripts/crawl.sh --help`.
2. If it exits 2 (conda missing, or the `crawl4ai` env missing), bootstrap once with `bash scripts/setup.sh`, then retry the crawl. Do not ask the user to install manually.
3. `setup.sh` pins `crawl4ai>=0.9,<1`; keep the pin — `crawl.py` is a 0.x compatibility layer and 1.x breaks its API.
4. If the crawl still exits 2 after a fresh setup, report the error to the user instead of retrying blindly.

## P1 — Explore

1. Read the intent artifact and select at most three independent research lenses.
2. Dispatch the smallest useful parallel set — **at most 3 delegates per phase** (one per lens). Each delegate receives the same immutable role, output schema, source policy, and a final `Parameters` block containing only the lens and query. Never dispatch one delegate per source.
3. Require 3–5 compact candidates per lens: title, URL, source tier, one-sentence relevance, date, and a 1–5 score. Delegates must return records, not copied page text. Mark every candidate's **evidence form** — `snippet-only` (search-result text only) or `fetched` (body retrieved) — and never let the two mix silently in `01_explore_result.md`: a search snippet restated later as if it were a fetched source is the same class of error as a paraphrase carrying a citation. P2 treats `snippet-only` rows as leads to fetch, not as evidence.
4. Deduplicate by canonical URL and publish `01_explore_result.md` with a direction menu, coverage gaps, and estimated P2 scope.
5. Complete P1 and wait for the user's direction choice.

## P2 — Deep research

1. Reuse the accepted P1 candidates. Fetch every `snippet-only` candidate that the chosen direction relies on, and add sources solely to fill explicit gaps. Batch deep reading into ≤3 delegates (one per source group) instead of one delegate per source.
2. Extract claim-level notes with anchors or section names; keep quotations short and preserve source attribution.
3. **Self-check the artifact before writing it** (this is the gate that downstream writers cannot provide): run the shared checker on the artifact itself —

   ```bash
   python .codex/scripts/note-citation-check.py ${WORKSPACE_PATH:-./workspace}/${PROJECT_SLUG} \
       --mode verbatim --file 02_deep_research.md
   ```

   It hard-fails on a quotation that traces nowhere (未命中) and on one that traces **only into your own intermediates**; for each weak hit it prints how far the quote traces into the raw sources plus the nearest corpus text, so the verdict 「提取件标记差异 / 跨项目来源 / 我自己的概括被当成引文」 is one glance instead of a hunt. Do not hand-roll another checker for this — add the missing judgement to `.codex/scripts/note-citation-check.py` (`--mode verbatim --file` exists precisely for this check; ERR-20260929-013 is the defect it was built for). Then recount every number, default, version, and row count against the original. The script covers **English整句引文 only**; Chinese quotations and all numbers remain a manual character-by-character comparison — do not let the script's green light stand for those. Report the check as a line in the handoff (`引文 N 处逐字核对（校验器 V 全绿）/ 数值 M 处重新计数`); if any item cannot be re-verified, drop the value and keep the semantics.
4. **Quotes taken from another workspace must be reachable from here.** A project sometimes quotes a capture that lives in a sibling project's tree, written as a pointer that resolves in *this* project's `research/` — that file does not exist, so the citation chain is cut the moment the reader follows it. Add the other tree explicitly (`--corpus ../<other-project>/research`) and cite the full cross-project path, not a bare-looking `research/04_..._honcho.md`.
5. Write `02_deep_research.md` with: scope, source table, claim/source map, contradictions, practical guidance, open questions, and a concise downstream handoff — including the intermediate-artifact header described in the source policy.
6. Keep full source bodies in local cache only when necessary for reproducibility; downstream stages receive paths, anchors, summaries, and source IDs.
7. Complete P2 and present source counts, tier mix, unresolved gaps, and the next user decision.

## Token and cache discipline

- Keep role, schema, quality bar, and tool set byte-stable within a request family; put query, dates, file excerpts, state, and URLs in the final parameter block.
- Read only the relevant sections of `01_explore_result.md` and `02_deep_research.md`; do not paste them into subagent prompts.
- Cap delegate output at 150 Chinese characters per source record and return source IDs plus conclusions to the parent.
- Fan-out caps: ≤3 delegates per phase, ≤4 same-type subagents concurrently in a session; prefer resuming one delegate over spawning siblings that re-read the same material.
- Reuse the same `template_id`, `template_version`, model, and fixed tool set for comparable runs. Record usage only through the project telemetry contract when the runtime supplies it.

## Completion criteria

- Every material claim maps to a source record or is explicitly marked as an inference.
- Every verbatim quotation in the artifact has a re-verified source ID plus line number, and every number has a counting basis; the self-check line is present, and the checker's `V` line for the artifact itself reads 未命中 0 / 仅中间产物命中 0 (or every remaining weak hit is named and explained in the handoff).
- Every candidate is marked `snippet-only` or `fetched`, and no `snippet-only` row is treated as evidence.
- P1 or P2 output is present, compact, and matches the active state phase.
- The next phase is not started without the user gate.
