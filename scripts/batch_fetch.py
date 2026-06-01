#!/usr/bin/env python3
"""batch_fetch.py — concurrent web fetcher with retry and local cache.

Reads a URLs JSON manifest, fetches pages concurrently via aiohttp,
converts HTML to Markdown, and writes results with YAML frontmatter.

Usage:
    python batch_fetch.py urls.json

Output:
    raw/doc-NN.md files with YAML frontmatter
    fetch-report.json with success/failed/cached counts

Exit codes:
    0  all fetches succeeded (or cached)
    1  partial failure
    2  script error (bad input, file not found, etc.)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiohttp
import html2text
from readability import Document


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def load_cache(cache_file: str) -> dict:
    """Load fetch cache from disk. Returns empty dict if missing or corrupt."""
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_cache(cache_file: str, cache: dict) -> None:
    """Persist fetch cache to disk."""
    os.makedirs(os.path.dirname(cache_file) or ".", exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Config reader
# ---------------------------------------------------------------------------

def read_urls_file(path: str) -> dict:
    """Read and validate the urls.json manifest. Exits 2 on failure."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: Cannot read urls file: {exc}", file=sys.stderr)
        sys.exit(2)

    required_keys = {"output_dir", "urls"}
    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        print(f"ERROR: urls.json missing keys: {missing}", file=sys.stderr)
        sys.exit(2)

    # Set defaults for optional keys
    data.setdefault("concurrency", 5)
    data.setdefault("timeout", 30)
    data.setdefault("cache_file", ".fetch-cache.json")
    return data


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

async def fetch_url(session: aiohttp.ClientSession, url: str, timeout: int,
                    max_retries: int = 3) -> str:
    """Fetch a single URL with exponential backoff retry.

    Returns the HTML body as a string.
    Raises RuntimeError after exhausting retries.
    """
    last_error: Exception | None = None
    for attempt in range(max_retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                if resp.status == 200:
                    return await resp.text()
                last_error = RuntimeError(f"HTTP {resp.status}")
        except (aiohttp.ClientError, asyncio.TimeoutError) as exc:
            last_error = exc

        # Exponential backoff: 1s, 2s, 4s ...
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)

    raise RuntimeError(f"Failed after {max_retries} attempts: {last_error}")


# ---------------------------------------------------------------------------
# HTML → Markdown
# ---------------------------------------------------------------------------

def html_to_markdown(html: str) -> str:
    """Extract readable content from HTML and convert to Markdown."""
    try:
        doc = Document(html)
        readable_html = doc.summary()
    except Exception:
        # Fallback: use raw HTML if readability fails
        readable_html = html

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # no wrapping
    return h.handle(readable_html).strip()


# ---------------------------------------------------------------------------
# Output writing
# ---------------------------------------------------------------------------

def write_doc_file(output_dir: str, index: int, url: str, title: str,
                   content: str, status: str) -> None:
    """Write a doc-NN.md file with YAML frontmatter."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"doc-{index:02d}.md"
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    frontmatter = (
        f"---\n"
        f"source_url: {url}\n"
        f"title: \"{title}\"\n"
        f"fetched_at: {fetched_at}\n"
        f"status: {status}\n"
        f"---\n\n"
    )

    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content + "\n")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def build_report(results: list[dict[str, Any]], duration_ms: int) -> dict:
    """Build a summary report from a list of result dicts.

    Each result dict must contain a 'status' key:
        "ok"      → success
        "cached"  → served from cache
        "failed: …" → failure with reason
    """
    success = sum(1 for r in results if r["status"] == "ok")
    cached = sum(1 for r in results if r["status"] == "cached")
    failed = sum(1 for r in results if r["status"].startswith("failed"))
    return {
        "total": len(results),
        "success": success,
        "cached": cached,
        "failed": failed,
        "duration_ms": duration_ms,
    }


# ---------------------------------------------------------------------------
# Main fetch pipeline
# ---------------------------------------------------------------------------

async def fetch_all(config: dict) -> list[dict[str, Any]]:
    """Fetch all URLs from the config concurrently.

    Returns a list of result dicts with keys: url, title, index, status.
    """
    urls = config["urls"]
    concurrency = config["concurrency"]
    timeout = config["timeout"]
    output_dir = config["output_dir"]
    cache_file = config.get("cache_file", ".fetch-cache.json")

    cache = load_cache(cache_file)
    results: list[dict[str, Any]] = []
    sem = asyncio.Semaphore(concurrency)

    async def process_one(entry: dict, session: aiohttp.ClientSession) -> dict:
        url = entry["url"]
        title = entry.get("title", "")
        index = entry.get("index", 0)

        async with sem:
            # Check cache
            if url in cache and "content" in cache[url]:
                md_content = cache[url]["content"]
                write_doc_file(output_dir, index, url, title, md_content, "cached")
                return {"url": url, "title": title, "index": index, "status": "cached"}

            try:
                html = await fetch_url(session, url, timeout)
                md_content = html_to_markdown(html)
                cache[url] = {"content": md_content, "fetched_at": datetime.now(timezone.utc).isoformat()}
                write_doc_file(output_dir, index, url, title, md_content, "ok")
                return {"url": url, "title": title, "index": index, "status": "ok"}
            except Exception as exc:
                reason = str(exc)[:80]
                write_doc_file(output_dir, index, url, title, "", f"failed: {reason}")
                return {"url": url, "title": title, "index": index, "status": f"failed: {reason}"}

    async with aiohttp.ClientSession() as session:
        tasks = [process_one(entry, session) for entry in urls]
        results = await asyncio.gather(*tasks)

    # Persist cache
    save_cache(cache_file, cache)
    return list(results)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concurrent web fetcher with retry and cache."
    )
    parser.add_argument(
        "urls_file",
        help="Path to urls.json manifest",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Read config and validate but do not fetch",
    )
    args = parser.parse_args()

    config = read_urls_file(args.urls_file)

    if args.dry_run:
        print(json.dumps(config, indent=2, ensure_ascii=False))
        sys.exit(0)

    start = asyncio.get_event_loop().time()
    try:
        results = asyncio.run(fetch_all(config))
    except Exception as exc:
        print(f"ERROR: fetch_all failed: {exc}", file=sys.stderr)
        sys.exit(2)

    duration_ms = int((asyncio.get_event_loop().time() - start) * 1000)
    report = build_report(results, duration_ms)

    # Write report
    report_path = os.path.join(config["output_dir"], "fetch-report.json")
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Determine exit code
    if report["failed"] == 0:
        sys.exit(0)
    elif report["failed"] < report["total"]:
        sys.exit(1)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
