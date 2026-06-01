"""Tests for batch_fetch.py — concurrent web fetcher."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Import the module under test
import batch_fetch as bf


# ---------------------------------------------------------------------------
# read_urls_file
# ---------------------------------------------------------------------------

class TestReadUrlsFile:
    def test_valid_file(self, tmp_path):
        urls_file = tmp_path / "urls.json"
        urls_file.write_text(json.dumps({
            "output_dir": "0-inbox/topic/raw",
            "urls": [
                {"url": "https://example.com", "title": "Example", "index": 1}
            ],
            "concurrency": 5,
            "timeout": 30,
            "cache_file": ".fetch-cache.json",
        }), encoding="utf-8")

        result = bf.read_urls_file(str(urls_file))
        assert result["output_dir"] == "0-inbox/topic/raw"
        assert len(result["urls"]) == 1
        assert result["concurrency"] == 5
        assert result["timeout"] == 30

    def test_missing_file(self, tmp_path):
        with pytest.raises(SystemExit) as exc_info:
            bf.read_urls_file(str(tmp_path / "nonexistent.json"))
        assert exc_info.value.code == 2

    def test_invalid_json(self, tmp_path):
        urls_file = tmp_path / "bad.json"
        urls_file.write_text("not json {{{", encoding="utf-8")
        with pytest.raises(SystemExit) as exc_info:
            bf.read_urls_file(str(urls_file))
        assert exc_info.value.code == 2


# ---------------------------------------------------------------------------
# load_cache / save_cache
# ---------------------------------------------------------------------------

class TestCache:
    def test_load_missing_cache_returns_empty_dict(self, tmp_path):
        cache = bf.load_cache(str(tmp_path / ".cache.json"))
        assert cache == {}

    def test_load_existing_cache(self, tmp_path):
        cache_file = tmp_path / ".cache.json"
        cache_file.write_text(json.dumps({"https://a.com": {"status": "ok"}}), encoding="utf-8")
        cache = bf.load_cache(str(cache_file))
        assert "https://a.com" in cache

    def test_save_and_reload_cache(self, tmp_path):
        cache_file = tmp_path / ".cache.json"
        data = {"https://x.com": {"status": "ok", "content": "# Hello"}}
        bf.save_cache(str(cache_file), data)
        loaded = bf.load_cache(str(cache_file))
        assert loaded == data


# ---------------------------------------------------------------------------
# html_to_markdown
# ---------------------------------------------------------------------------

class TestHtmlToMarkdown:
    def test_basic_conversion(self):
        html = "<html><body><h1>Title</h1><p>Hello world</p></body></html>"
        md = bf.html_to_markdown(html)
        assert "Title" in md
        assert "Hello world" in md

    def test_empty_body(self):
        md = bf.html_to_markdown("<html><body></body></html>")
        # Should return empty string or whitespace — no crash
        assert isinstance(md, str)


# ---------------------------------------------------------------------------
# write_doc_file
# ---------------------------------------------------------------------------

class TestWriteDocFile:
    def test_writes_frontmatter(self, tmp_path):
        output_dir = str(tmp_path / "raw")
        os.makedirs(output_dir, exist_ok=True)

        bf.write_doc_file(
            output_dir,
            index=1,
            url="https://example.com",
            title="Example",
            content="# Hello",
            status="ok",
        )

        written = Path(output_dir) / "doc-01.md"
        assert written.exists()
        text = written.read_text(encoding="utf-8")
        assert "source_url: https://example.com" in text
        assert "title:" in text
        assert "status: ok" in text
        assert "# Hello" in text

    def test_zero_padded_index(self, tmp_path):
        output_dir = str(tmp_path / "raw")
        os.makedirs(output_dir, exist_ok=True)
        bf.write_doc_file(output_dir, index=10, url="u", title="t", content="c", status="ok")
        written = Path(output_dir) / "doc-10.md"
        assert written.exists()

    def test_failed_status(self, tmp_path):
        output_dir = str(tmp_path / "raw")
        os.makedirs(output_dir, exist_ok=True)
        bf.write_doc_file(
            output_dir, index=1, url="https://fail.com", title="Fail",
            content="", status="failed: timeout",
        )
        text = (Path(output_dir) / "doc-01.md").read_text(encoding="utf-8")
        assert "status: failed: timeout" in text


# ---------------------------------------------------------------------------
# build_report
# ---------------------------------------------------------------------------

class TestBuildReport:
    def test_all_success(self):
        results = [
            {"url": "https://a.com", "status": "ok"},
            {"url": "https://b.com", "status": "ok"},
        ]
        report = bf.build_report(results, duration_ms=123)
        assert report["total"] == 2
        assert report["success"] == 2
        assert report["failed"] == 0
        assert report["cached"] == 0
        assert report["duration_ms"] == 123

    def test_mixed_results(self):
        results = [
            {"url": "https://a.com", "status": "ok"},
            {"url": "https://b.com", "status": "cached"},
            {"url": "https://c.com", "status": "failed: timeout"},
        ]
        report = bf.build_report(results, duration_ms=500)
        assert report["success"] == 1
        assert report["cached"] == 1
        assert report["failed"] == 1

    def test_empty_results(self):
        report = bf.build_report([], duration_ms=0)
        assert report["total"] == 0
        assert report["success"] == 0


# ---------------------------------------------------------------------------
# fetch_url  (unit test — mock the network)
# ---------------------------------------------------------------------------

class TestFetchUrl:
    @pytest.mark.asyncio
    async def test_fetch_returns_html(self):
        session = MagicMock()

        # Simulate aiohttp response with async text() method
        resp = AsyncMock()
        resp.status = 200
        resp.text.return_value = "<html><body>asyncio-coroutine returning HTML</body></html>"

        # session.get() must return an object usable with `async with`
        ctx = AsyncMock()
        ctx.__aenter__.return_value = resp
        ctx.__aexit__.return_value = False
        session.get.return_value = ctx

        result = await bf.fetch_url(session, "https://example.com", timeout=10)
        assert "HTML" in result

    @pytest.mark.asyncio
    async def test_fetch_retries_on_failure(self):
        session = MagicMock()
        attempt_count = {"n": 0}

        async def fake_text():
            return "ok"

        class FakeResponse:
            status = 500

        class GoodResponse:
            status = 200

        async def fake_text_ok():
            return "ok"

        async def mock_enter(self):
            attempt_count["n"] += 1
            if attempt_count["n"] < 3:
                return FakeResponse()
            r = GoodResponse()
            r.text = fake_text_ok
            return r

        ctx = MagicMock()
        ctx.__aenter__ = mock_enter
        ctx.__aexit__ = AsyncMock(return_value=False)
        session.get.return_value = ctx

        # Patch sleep to avoid actual delay
        async def mock_sleep(delay):
            pass

        with patch("batch_fetch.asyncio.sleep", side_effect=mock_sleep):
            result = await bf.fetch_url(session, "https://example.com", timeout=10)
        assert "ok" in result


# ---------------------------------------------------------------------------
# build_report  — edge cases
# ---------------------------------------------------------------------------

class TestBuildReportEdge:
    def test_all_cached(self):
        results = [{"url": "a", "status": "cached"}, {"url": "b", "status": "cached"}]
        report = bf.build_report(results, duration_ms=10)
        assert report["cached"] == 2
        assert report["success"] == 0
        assert report["failed"] == 0

    def test_all_failed(self):
        results = [
            {"url": "a", "status": "failed: 403"},
            {"url": "b", "status": "failed: timeout"},
        ]
        report = bf.build_report(results, duration_ms=0)
        assert report["failed"] == 2
        assert report["success"] == 0


# ---------------------------------------------------------------------------
# main() — exit code behavior
# ---------------------------------------------------------------------------

class TestMainExitCode:
    def test_missing_urls_file_exits_2(self, tmp_path):
        with patch("sys.argv", ["batch_fetch.py", str(tmp_path / "nope.json")]):
            with pytest.raises(SystemExit) as exc_info:
                bf.main()
            assert exc_info.value.code == 2

    def test_valid_urls_with_mocked_fetch(self, tmp_path):
        urls_file = tmp_path / "urls.json"
        output_dir = tmp_path / "out"
        urls_file.write_text(json.dumps({
            "output_dir": str(output_dir),
            "urls": [{"url": "https://example.com", "title": "Ex", "index": 1}],
            "concurrency": 1,
            "timeout": 10,
            "cache_file": str(tmp_path / ".cache.json"),
        }), encoding="utf-8")

        mock_loop = MagicMock()
        mock_loop.time.return_value = 100.0

        with patch("batch_fetch.fetch_all", return_value=[
            {"url": "https://example.com", "status": "ok"}
        ]), patch("batch_fetch.asyncio") as mock_asyncio:
            mock_asyncio.run.return_value = [
                {"url": "https://example.com", "status": "ok"}
            ]
            mock_asyncio.get_event_loop.return_value = mock_loop
            mock_asyncio.ClientSession.return_value.__aenter__ = AsyncMock()
            mock_asyncio.ClientSession.return_value.__aexit__ = AsyncMock(return_value=False)
            with patch("sys.argv", ["batch_fetch.py", str(urls_file)]):
                with pytest.raises(SystemExit) as exc_info:
                    bf.main()
                # exit code 0 = all success
                assert exc_info.value.code == 0
