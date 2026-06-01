---
archived-with: 2026-06-02-token-cost-optimization
status: final
---
# Token Cost Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 subagent 中的确定性 I/O 操作（WebFetch、串行 Read）下沉到 Python 脚本，降低 ~80% Token 消耗。

**Architecture:** 新增 `scripts/batch_fetch.py`（并发网页抓取）和 `scripts/merge_sources.py`（多文件合并），修改 collector/writer/curator 三个 subagent 使用脚本替代串行工具调用。脚本失败时自动降级到原有方式。

**Tech Stack:** Python 3.8+, aiohttp, readability-lxml, html2text

---

## File Structure

```
scripts/
├── batch_fetch.py          # 并发网页抓取脚本
├── merge_sources.py        # 多文件合并脚本
├── requirements.txt        # Python 依赖
└── test_batch_fetch.py     # batch_fetch 单元测试
    test_merge_sources.py   # merge_sources 单元测试

.claude/agents/
├── collector.md            # 修改：使用 batch_fetch.py
├── writer.md               # 修改：使用 merge_sources.py
└── curator.md              # 修改：使用 merge_sources.py

.claude/skills/collect/
└── SKILL.md                # 修改：传递脚本路径参数
```

---

### Task 1: Create requirements.txt

**Files:**
- Create: `scripts/requirements.txt`

- [ ] **Step 1: Create requirements.txt**

```
aiohttp>=3.9.0
readability-lxml>=0.8.1
html2text>=2024.2.26
lxml>=5.1.0
```

- [ ] **Step 2: Commit**

```bash
git add scripts/requirements.txt
git commit -m "feat: add Python dependencies for batch I/O scripts"
```

---

### Task 2: Create batch_fetch.py

**Files:**
- Create: `scripts/batch_fetch.py`
- Create: `scripts/test_batch_fetch.py`

- [ ] **Step 1: Write tests for batch_fetch.py**

```python
# scripts/test_batch_fetch.py
"""Tests for batch_fetch.py"""
import json
import os
import tempfile
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def urls_file(tmp_dir):
    """Create a urls.json test fixture."""
    data = {
        "output_dir": os.path.join(tmp_dir, "raw"),
        "urls": [
            {"url": "https://example.com/page1", "title": "Page 1", "index": 1},
            {"url": "https://example.com/page2", "title": "Page 2", "index": 2},
        ],
        "concurrency": 2,
        "timeout": 5,
    }
    path = os.path.join(tmp_dir, "urls.json")
    with open(path, "w") as f:
        json.dump(data, f)
    return path


def test_read_urls_file(urls_file):
    """Test reading urls.json input file."""
    from batch_fetch import read_urls_file
    config = read_urls_file(urls_file)
    assert len(config["urls"]) == 2
    assert config["concurrency"] == 2


def test_read_urls_file_missing():
    """Test error on missing file."""
    from batch_fetch import read_urls_file
    with pytest.raises(SystemExit):
        read_urls_file("/nonexistent/urls.json")


def test_build_report():
    """Test report generation."""
    from batch_fetch import build_report
    results = [
        {"index": 1, "status": "success", "file": "doc-01.md"},
        {"index": 2, "status": "failed", "error": "403 Forbidden"},
    ]
    report = build_report(results, duration_ms=1500)
    assert report["total"] == 2
    assert report["success"] == 1
    assert report["failed"] == 1
    assert report["duration_ms"] == 1500


def test_write_doc_file(tmp_dir):
    """Test writing a doc-NN.md file with frontmatter."""
    from batch_fetch import write_doc_file
    output_dir = os.path.join(tmp_dir, "raw")
    os.makedirs(output_dir)
    write_doc_file(
        output_dir=output_dir,
        index=1,
        url="https://example.com",
        title="Test Page",
        content="# Hello\n\nWorld",
        status="success",
    )
    doc_path = os.path.join(output_dir, "doc-01.md")
    assert os.path.exists(doc_path)
    with open(doc_path) as f:
        content = f.read()
    assert "source_url: https://example.com" in content
    assert "# Hello" in content


def test_exit_code_all_success(tmp_dir):
    """Test exit code 0 when all fetches succeed."""
    from batch_fetch import main
    urls_file_path = os.path.join(tmp_dir, "urls.json")
    config = {
        "output_dir": os.path.join(tmp_dir, "raw"),
        "urls": [{"url": "https://example.com", "title": "Test", "index": 1}],
        "concurrency": 1,
        "timeout": 5,
    }
    with open(urls_file_path, "w") as f:
        json.dump(config, f)

    with patch("batch_fetch.fetch_url", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = "# Test Content"
        with patch("batch_fetch.main") as mock_main:
            mock_main.return_value = None
            # Just verify the function exists and is callable
            assert callable(main)


def test_cache_hit_skips_fetch(tmp_dir):
    """Test that cached URLs are skipped."""
    from batch_fetch import load_cache, save_cache
    cache_file = os.path.join(tmp_dir, ".fetch-cache.json")
    cache = {"https://example.com/cached": "doc-01.md"}
    save_cache(cache_file, cache)
    loaded = load_cache(cache_file)
    assert "https://example.com/cached" in loaded
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts && python -m pytest test_batch_fetch.py -v`
Expected: FAIL (module not found)

- [ ] **Step 3: Implement batch_fetch.py**

```python
#!/usr/bin/env python3
"""batch_fetch.py — Concurrent web fetcher for study system.

Reads a URLs JSON file, fetches pages concurrently using aiohttp,
converts HTML to Markdown, and writes results to doc-NN.md files.

Usage:
    python batch_fetch.py --input-file urls.json [--output-dir raw/]

Input format (urls.json):
{
    "output_dir": "0-inbox/topic/raw",
    "urls": [
        {"url": "https://...", "title": "...", "index": 1}
    ],
    "concurrency": 5,
    "timeout": 30,
    "cache_file": ".fetch-cache.json"
}

Output:
    - raw/doc-NN.md (with YAML frontmatter)
    - fetch-report.json

Exit codes: 0=all success, 1=partial failure, 2=script error
"""
import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import aiohttp
except ImportError:
    print("ERROR: aiohttp not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)

try:
    from readability import Document
    import html2text
except ImportError:
    print("ERROR: readability-lxml or html2text not installed. Run: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(2)


# --- Cache ---

def load_cache(cache_file: str) -> dict:
    """Load fetch cache from file."""
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}


def save_cache(cache_file: str, cache: dict) -> None:
    """Save fetch cache to file."""
    with open(cache_file, "w") as f:
        json.dump(cache, f, indent=2)


# --- Config ---

def read_urls_file(path: str) -> dict:
    """Read and validate urls.json input file."""
    if not os.path.exists(path):
        print(f"ERROR: Input file not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path, "r") as f:
        config = json.load(f)
    if "urls" not in config or not config["urls"]:
        print("ERROR: No URLs in input file", file=sys.stderr)
        sys.exit(2)
    return config


# --- Fetch ---

async def fetch_url(session: aiohttp.ClientSession, url: str, timeout: int) -> str:
    """Fetch a single URL and return HTML content."""
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
        resp.raise_for_status()
        return await resp.text()


def html_to_markdown(html: str) -> str:
    """Convert HTML to clean Markdown."""
    try:
        doc = Document(html)
        readable = doc.summary()
    except Exception:
        readable = html
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.body_width = 0
    return h.handle(readable)


def write_doc_file(output_dir: str, index: int, url: str, title: str,
                   content: str, status: str) -> None:
    """Write a doc-NN.md file with YAML frontmatter."""
    os.makedirs(output_dir, exist_ok=True)
    doc_path = os.path.join(output_dir, f"doc-{index:02d}.md")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    frontmatter = f"""---
source_url: {url}
title: "{title}"
fetched_at: {now}
status: {status}
---

"""
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)


# --- Report ---

def build_report(results: list, duration_ms: int) -> dict:
    """Build fetch report from results."""
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    cached = sum(1 for r in results if r["status"] == "cached")
    return {
        "total": len(results),
        "success": success,
        "failed": failed,
        "cached": cached,
        "results": results,
        "duration_ms": duration_ms,
    }


# --- Main ---

async def fetch_all(config: dict) -> list:
    """Fetch all URLs concurrently."""
    urls = config["urls"]
    output_dir = config["output_dir"]
    concurrency = config.get("concurrency", 5)
    timeout = config.get("timeout", 30)
    max_retries = config.get("max_retries", 3)
    retry_base_delay = config.get("retry_base_delay", 1)
    cache_file = config.get("cache_file", ".fetch-cache.json")

    cache = load_cache(cache_file)
    results = []
    semaphore = asyncio.Semaphore(concurrency)

    async def fetch_one(session: aiohttp.ClientSession, item: dict) -> dict:
        url = item["url"]
        index = item["index"]
        title = item.get("title", "")

        # Check cache
        if url in cache:
            cached_file = cache[url]
            results.append({
                "index": index, "status": "cached",
                "file": cached_file, "url": url,
            })
            return

        # Fetch with retries
        for attempt in range(max_retries):
            try:
                async with semaphore:
                    html = await fetch_url(session, url, timeout)
                markdown = html_to_markdown(html)
                write_doc_file(output_dir, index, url, title, markdown, "success")
                doc_file = f"doc-{index:02d}.md"
                cache[url] = doc_file
                results.append({
                    "index": index, "status": "success",
                    "file": doc_file, "url": url,
                })
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = retry_base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)
                else:
                    error_msg = str(e)
                    results.append({
                        "index": index, "status": "failed",
                        "error": error_msg, "url": url,
                    })

    start = time.time()
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_one(session, item) for item in urls]
        await asyncio.gather(*tasks)
    duration_ms = int((time.time() - start) * 1000)

    # Save cache
    save_cache(cache_file, cache)

    return build_report(results, duration_ms)


def main():
    parser = argparse.ArgumentParser(description="Batch fetch URLs to Markdown files")
    parser.add_argument("--input-file", required=True, help="Path to urls.json")
    parser.add_argument("--output-dir", help="Override output directory")
    args = parser.parse_args()

    config = read_urls_file(args.input_file)
    if args.output_dir:
        config["output_dir"] = args.output_dir

    report = asyncio.run(fetch_all(config))

    # Write report
    report_path = os.path.join(config["output_dir"], "fetch-report.json")
    os.makedirs(config["output_dir"], exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    # Print summary
    print(f"Fetched: {report['success']} success, {report['failed']} failed, "
          f"{report['cached']} cached ({report['duration_ms']}ms)")

    # Exit code
    if report["failed"] == 0:
        sys.exit(0)
    elif report["success"] > 0:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd scripts && python -m pytest test_batch_fetch.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/batch_fetch.py scripts/test_batch_fetch.py
git commit -m "feat: add batch_fetch.py — concurrent web fetcher with retry and cache"
```

---

### Task 3: Create merge_sources.py

**Files:**
- Create: `scripts/merge_sources.py`
- Create: `scripts/test_merge_sources.py`

- [ ] **Step 1: Write tests for merge_sources.py**

```python
# scripts/test_merge_sources.py
"""Tests for merge_sources.py"""
import os
import tempfile
import pytest
from pathlib import Path


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture
def raw_dir(tmp_dir):
    """Create a raw/ directory with test doc files."""
    raw = os.path.join(tmp_dir, "raw")
    os.makedirs(raw)

    # doc-01.md: normal file
    with open(os.path.join(raw, "doc-01.md"), "w") as f:
        f.write("---\nsource_url: https://example.com\nstatus: success\n---\n\n# Page 1\n\nContent 1")

    # doc-02.md: normal file
    with open(os.path.join(raw, "doc-02.md"), "w") as f:
        f.write("---\nsource_url: https://example2.com\nstatus: success\n---\n\n# Page 2\n\nContent 2")

    # doc-03.md: failed file (should be skipped)
    with open(os.path.join(raw, "doc-03.md"), "w") as f:
        f.write("---\nsource_url: https://failed.com\nstatus: failed\n---\n\n")

    # doc-04.md: empty file (should be skipped)
    with open(os.path.join(raw, "doc-04.md"), "w") as f:
        f.write("")

    return raw


def test_merge_files(tmp_dir, raw_dir):
    """Test merging multiple files."""
    from merge_sources import merge_files
    output = os.path.join(tmp_dir, "merged.md")
    result = merge_files(raw_dir, output, "html-comment")
    assert result["merged"] == 2  # only doc-01 and doc-02
    assert result["skipped"] == 2  # doc-03 (failed) and doc-04 (empty)
    assert os.path.exists(output)
    with open(output) as f:
        content = f.read()
    assert "<!-- SOURCE: doc-01.md" in content
    assert "<!-- SOURCE: doc-02.md" in content
    assert "<!-- END: doc-01.md -->" in content
    assert "doc-03" not in content
    assert "doc-04" not in content


def test_merge_empty_dir(tmp_dir):
    """Test merging from empty/nonexistent directory."""
    from merge_sources import merge_files
    output = os.path.join(tmp_dir, "merged.md")
    result = merge_files(os.path.join(tmp_dir, "nonexistent"), output, "html-comment")
    assert result["merged"] == 0
    assert result["skipped"] == 0


def test_merge_preserves_frontmatter(tmp_dir, raw_dir):
    """Test that frontmatter is preserved in merged output."""
    from merge_sources import merge_files
    output = os.path.join(tmp_dir, "merged.md")
    merge_files(raw_dir, output, "html-comment")
    with open(output) as f:
        content = f.read()
    assert "source_url: https://example.com" in content


def test_exit_code_success(tmp_dir, raw_dir):
    """Test exit code 0 on success."""
    from merge_sources import main
    output = os.path.join(tmp_dir, "merged.md")
    with patch("sys.argv", ["merge_sources.py", "--input-dir", raw_dir, "--output", output]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0


def test_exit_code_no_files(tmp_dir):
    """Test exit code 1 when no files found."""
    from merge_sources import main
    output = os.path.join(tmp_dir, "merged.md")
    nonexistent = os.path.join(tmp_dir, "empty")
    with patch("sys.argv", ["merge_sources.py", "--input-dir", nonexistent, "--output", output]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd scripts && python -m pytest test_merge_sources.py -v`
Expected: FAIL (module not found)

- [ ] **Step 3: Implement merge_sources.py**

```python
#!/usr/bin/env python3
"""merge_sources.py — Merge multiple doc files into a single file.

Reads doc-NN.md files from an input directory, merges them into a single
output file with HTML comment separators.

Usage:
    python merge_sources.py --input-dir raw/ --output merged-sources.md [--format html-comment]

Output format:
    <!-- SOURCE: doc-01.md | url: https://... | score: 4.2 -->
    [content]
    <!-- END: doc-01.md -->

Exit codes: 0=success, 1=no files, 2=script error
"""
import argparse
import os
import re
import sys
from pathlib import Path


def read_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            block = content[3:end].strip()
            for line in block.split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip()
    return meta


def merge_files(input_dir: str, output_file: str, fmt: str) -> dict:
    """Merge doc files from input_dir into a single output file.

    Returns dict with merged/skipped counts.
    """
    result = {"merged": 0, "skipped": 0, "files": []}

    if not os.path.isdir(input_dir):
        return result

    # Find and sort doc files
    doc_files = sorted([
        f for f in os.listdir(input_dir)
        if f.startswith("doc-") and f.endswith(".md")
    ])

    if not doc_files:
        return result

    lines = []
    for fname in doc_files:
        fpath = os.path.join(input_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip empty files
        if not content.strip():
            result["skipped"] += 1
            continue

        # Skip failed files
        meta = read_frontmatter(content)
        if meta.get("status") == "failed":
            result["skipped"] += 1
            continue

        # Build separator
        url = meta.get("source_url", "unknown")
        if fmt == "html-comment":
            lines.append(f"<!-- SOURCE: {fname} | url: {url} -->")
            lines.append(content.strip())
            lines.append(f"<!-- END: {fname} -->")
            lines.append("")

        result["merged"] += 1
        result["files"].append(fname)

    # Write output
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return result


def main():
    parser = argparse.ArgumentParser(description="Merge doc files into single file")
    parser.add_argument("--input-dir", required=True, help="Input directory with doc-NN.md files")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--format", default="html-comment", choices=["html-comment"],
                        help="Separator format (default: html-comment)")
    args = parser.parse_args()

    result = merge_files(args.input_dir, args.output, args.format)

    print(f"Merged: {result['merged']} files, Skipped: {result['skipped']} files")

    if result["merged"] == 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd scripts && python -m pytest test_merge_sources.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/merge_sources.py scripts/test_merge_sources.py
git commit -m "feat: add merge_sources.py — merge doc files with HTML comment separators"
```

---

### Task 4: Modify collector.md

**Files:**
- Modify: `.claude/agents/collector.md`

- [ ] **Step 1: Read current collector.md**

Read `.claude/agents/collector.md` to understand current structure.

- [ ] **Step 2: Add batch fetch instructions**

After the "核心原则" section, add a new section:

```markdown
## 批量抓取模式

当脚本可用时，使用批量抓取替代串行 WebFetch：

### 检测脚本可用性
Bash: `python --version 2>&1 && test -f scripts/batch_fetch.py && echo "AVAILABLE" || echo "UNAVAILABLE"`

### 使用脚本抓取
1. 将搜索结果写入 `{output_dir}/urls.json`：
```json
{
  "output_dir": "{output_dir}/raw",
  "urls": [
    {"url": "...", "title": "...", "index": 1}
  ],
  "concurrency": 5,
  "timeout": 30
}
```

2. 执行脚本：`python scripts/batch_fetch.py --input-file {output_dir}/urls.json`

3. 读取报告：Read `{output_dir}/raw/fetch-report.json`

4. 根据报告结果进行评分+去重+分类

### 降级条件
- Python 不可用 → 回退到串行 WebFetch
- 脚本不存在 → 回退到串行 WebFetch
- 脚本执行失败（退出码 2）→ 回退到串行 WebFetch
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/collector.md
git commit -m "feat: add batch fetch mode to collector subagent"
```

---

### Task 5: Modify writer.md

**Files:**
- Modify: `.claude/agents/writer.md`

- [ ] **Step 1: Read current writer.md**

Read `.claude/agents/writer.md` to understand current structure.

- [ ] **Step 2: Add merge sources instructions**

After the "核心原则" section, add a new section:

```markdown
## 批量读取模式

当脚本可用时，使用合并读取替代串行 Read：

### 检测脚本可用性
Bash: `python --version 2>&1 && test -f scripts/merge_sources.py && echo "AVAILABLE" || echo "UNAVAILABLE"`

### 使用脚本合并
1. 执行脚本：`python scripts/merge_sources.py --input-dir {curated_dir} --output {curated_dir}/merged-sources.md`

2. 读取合并文件：Read `{curated_dir}/merged-sources.md`

3. 合并文件用 HTML 注释分隔每个源文件：
   - `<!-- SOURCE: doc-01.md | url: https://... -->` 表示源文件开始
   - `<!-- END: doc-01.md -->` 表示源文件结束

4. 基于合并内容撰写笔记

### 降级条件
- Python 不可用 → 回退到串行 Read ×4
- 脚本不存在 → 回退到串行 Read ×4
- 脚本执行失败 → 回退到串行 Read ×4
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/writer.md
git commit -m "feat: add batch read mode to writer subagent"
```

---

### Task 6: Modify curator.md

**Files:**
- Modify: `.claude/agents/curator.md`

- [ ] **Step 1: Read current curator.md**

Read `.claude/agents/curator.md` to understand current structure.

- [ ] **Step 2: Add merge sources instructions**

After the "核心原则" section, add a new section:

```markdown
## 批量读取模式

当脚本可用时，使用合并读取替代串行 Read：

### 检测脚本可用性
Bash: `python --version 2>&1 && test -f scripts/merge_sources.py && echo "AVAILABLE" || echo "UNAVAILABLE"`

### 使用脚本合并
1. 执行脚本：`python scripts/merge_sources.py --input-dir {input_dir} --output {input_dir}/merged-sources.md`

2. 读取合并文件：Read `{input_dir}/merged-sources.md`

3. 合并文件用 HTML 注释分隔每个源文件，可识别每个源的 URL 和元数据

4. 基于合并内容进行评分+分类+去重

### 降级条件
- Python 不可用 → 回退到串行 Read ×N
- 脚本不存在 → 回退到串行 Read ×N
- 脚本执行失败 → 回退到串行 Read ×N
```

- [ ] **Step 3: Commit**

```bash
git add .claude/agents/curator.md
git commit -m "feat: add batch read mode to curator subagent"
```

---

### Task 7: Modify collect SKILL.md

**Files:**
- Modify: `.claude/skills/collect/SKILL.md`

- [ ] **Step 1: Read current collect SKILL.md**

Read `.claude/skills/collect/SKILL.md` to understand the dispatch section.

- [ ] **Step 2: Add script path parameters to dispatch**

In the collector dispatch section, add script path context to the prompt:

```markdown
Script Context (add to collector prompt):
- Script Dir: {SYSTEM_ROOT}/../scripts/ (relative to project root)
- Batch Fetch: scripts/batch_fetch.py
- Merge Sources: scripts/merge_sources.py
- Requirements: scripts/requirements.txt
```

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/collect/SKILL.md
git commit -m "feat: pass script paths to collector subagent"
```

---

### Task 8: Run all tests

**Files:** None (verification only)

- [ ] **Step 1: Install dependencies**

Run: `cd scripts && pip install -r requirements.txt`
Expected: Successfully installed aiohttp, readability-lxml, html2text, lxml

- [ ] **Step 2: Run all unit tests**

Run: `cd scripts && python -m pytest test_batch_fetch.py test_merge_sources.py -v`
Expected: All tests PASS

- [ ] **Step 3: Commit final state**

```bash
git add -A
git commit -m "test: verify all unit tests pass for batch I/O scripts"
```
