#!/usr/bin/env python3
"""Crawl4AI 精读 CLI（research-collector Phase 2 主深读引擎）。

用法:
  # 单 URL → stdout（干净 Markdown）
  crawl.py --url https://example.com

  # 批量并发 → 输出目录，每篇一个 <NN>_<host>.md（含 YAML frontmatter: url/title/scraped_at）
  crawl.py --url URL1 --url URL2 ... --output-dir ./out

退出码:
  0  全部成功
  1  存在失败 URL（失败的 URL 会打印到 stderr；成功的仍写盘/stdout）
  2  参数错误 / 环境问题

注意:
  - 依赖 crawl4ai conda env（见同目录 setup.sh 一键安装）
  - 默认总是重抓并刷新本地缓存（WRITE_ONLY，产出干净 fit_markdown）；
    加 --cache 才复用本地缓存。crawl4ai 0.9.x 缓存只保存 raw_markdown
    （fit_markdown 不落缓存），缓存命中的输出可能含少量导航噪声。
"""

from __future__ import annotations

import argparse
import asyncio
import pathlib
import sys
from datetime import datetime, timezone
from importlib import metadata as _imeta
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

# 内容过滤（生成更干净的 fit_markdown，去除导航/广告噪声）。版本不兼容时降级为默认生成器。
try:
    from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
    from crawl4ai.content_filter_strategy import PruningContentFilter

    MARKDOWN_GENERATOR = DefaultMarkdownGenerator(content_filter=PruningContentFilter())
except Exception:  # noqa: BLE001 - 旧版 crawl4ai 没有这些类时退回默认
    MARKDOWN_GENERATOR = None


# ---------------------------------------------------------------------------
# markdown 结果兼容层
# ---------------------------------------------------------------------------
def extract_markdown(result) -> str:
    """兼容新旧版本 result.markdown。

    - 旧版（<0.6）: `result.markdown` 是纯字符串。
    - 新版（0.6+）: `result.markdown` 是 `StringCompatibleMarkdown`（str 子类，
      值 = raw_markdown），同时通过属性暴露 `fit_markdown` / `raw_markdown`
      / `markdown_with_citations` 等 MarkdownGenerationResult 字段。

    取值优先级：fit_markdown（干净正文） > raw_markdown（全量） > markdown_with_citations > str()。
    """
    md = getattr(result, "markdown", None)
    if md is None:
        return ""
    for attr in ("fit_markdown", "raw_markdown", "markdown_with_citations"):
        try:
            value = getattr(md, attr, None)
        except Exception:
            value = None
        if value:
            return value
    # 纯字符串的旧版结果 / 其它兜底
    if isinstance(md, str):
        return md
    return str(md)


# ---------------------------------------------------------------------------
# 元数据 / frontmatter
# ---------------------------------------------------------------------------
def _title_of(container) -> str:
    """从 result.metadata 里取标题（可能没有，返回空串）。"""
    meta = _mark(container, "metadata")
    if isinstance(meta, dict):
        title = meta.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()[:200]
    return ""


def _yaml_quote(s: str) -> str:
    """YAML 双引号标量转义（标题/URL 含冒号、引号时保持可解析）。"""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_frontmatter(url: str, title: str) -> str:
    """批量输出 .md 的 YAML frontmatter，保留来源溯源。"""
    lines = ["---", f"url: {_yaml_quote(url)}"]
    if title:
        lines.append(f"title: {_yaml_quote(title)}")
    lines.append(f"scraped_at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# 抓取
# ---------------------------------------------------------------------------
async def crawl_one(crawler, url: str, run_config) -> tuple[str, str]:
    result = await crawler.arun(url=url, config=run_config)
    if not getattr(result, "success", False):
        err = getattr(result, "error_message", None) or "unknown error"
        raise RuntimeError(f"抓取失败 {url}: {err}")
    md = extract_markdown(result)
    if not md.strip():
        raise RuntimeError(f"抓取结果为空（可能是反爬拦截或无正文）: {url}")
    return url, md


def _mark(container, attr: str):
    """从 CrawlResultContainer / CrawlResult 上安全取字段。"""
    return getattr(container, attr, None)


async def crawl_many(crawler, urls: list[str], run_config) -> list[tuple[str, str | None, str | None, str]]:
    """批量并发抓取多个 URL，逐个隔离错误。

    优先用官方 `arun_many`（返回 CrawlResultContainer，内部已做并发调度）；
    若整体失败则退化为逐 URL 顺序 `arun`，保证单点错误不影响其它 URL。
    返回 [(url, markdown_or_None, error_or_None, title_or_empty)]。
    """
    results: list[tuple[str, str | None, str | None, str]] = []
    try:
        container = await crawler.arun_many(urls, config=run_config)
        for r in container:
            url = _mark(r, "url") or ""
            if not _mark(r, "success"):
                err = _mark(r, "error_message") or "unknown error"
                results.append((url, None, f"抓取失败 {url}: {err}", ""))
                continue
            md = extract_markdown(r)
            if not md.strip():
                results.append((url, None, f"抓取结果为空（可能是反爬拦截或无正文）: {url}", ""))
                continue
            results.append((url, md, None, _title_of(r)))
    except Exception as exc:  # noqa: BLE001 - arun_many 整体失败，退化为逐 URL
        for url in urls:
            try:
                _, md = await crawl_one(crawler, url, run_config)
                results.append((url, md, None, ""))
            except Exception as e2:  # noqa: BLE001 - 单 URL 失败不影响批量
                results.append((url, None, str(e2), ""))
    return results


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------
def out_name(url: str, index: int) -> str:
    host = urlparse(url).netloc or f"page_{index}"
    host = host.replace(":", "_").replace(".", "_")
    return f"{index:02d}_{host}.md"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="crawl",
        description="Crawl4AI 精读：把 URL 抓成干净 Markdown（支持批量并发 + 本地缓存）。",
    )
    p.add_argument("--url", action="append", required=True, dest="urls", metavar="URL",
                   help="要精读的 URL，可重复传入实现批量。")
    p.add_argument("--output-dir", metavar="DIR",
                   help="输出目录。指定后每篇写一个 .md；未指定时（仅单 URL）输出到 stdout。")
    p.add_argument("--no-js", action="store_true",
                   help="禁用 JS 渲染（默认渲染动态页面，SPA/懒加载也可抓全）。")
    p.add_argument("--cache", action="store_true",
                   help="复用本地缓存（默认总是重抓并刷新缓存；crawl4ai 0.9.x 缓存只存 raw，"
                        "命中输出可能含少量导航噪声）。")
    p.add_argument("--fresh", action="store_true",
                   help="强制重新抓取并刷新本地缓存（默认行为，显式声明用）。")
    p.add_argument("--no-cache", dest="fresh", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--verbose", action="store_true", help="打印详细日志。")
    return p


async def amain(args: argparse.Namespace) -> int:
    urls = [u for u in args.urls if u]
    if not urls:
        print("错误: 至少需要一个 --url", file=sys.stderr)
        return 2
    if not args.output_dir and len(urls) > 1:
        print("错误: 多 URL 时必须指定 --output-dir（否则输出无处安放）。", file=sys.stderr)
        return 2

    if args.output_dir:
        out_dir = pathlib.Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

    browser_config = BrowserConfig(
        headless=True,
        verbose=args.verbose,
        java_script_enabled=not args.no_js,
    )
    # 默认总是重抓并刷新缓存（WRITE_ONLY，产出干净 fit 正文）；--cache 显式复用缓存。
    use_cache = args.cache and not args.fresh
    run_config_kwargs: dict = {
        "cache_mode": CacheMode.ENABLED if use_cache else CacheMode.WRITE_ONLY,
        "verbose": args.verbose,
    }
    if MARKDOWN_GENERATOR is not None:
        run_config_kwargs["markdown_generator"] = MARKDOWN_GENERATOR
    run_config = CrawlerRunConfig(**run_config_kwargs)

    failures = 0
    async with AsyncWebCrawler(config=browser_config) as crawler:
        for i, (url, md, err, title) in enumerate(await crawl_many(crawler, urls, run_config)):
            if err is not None:
                failures += 1
                print(f"[失败] {url}: {err}", file=sys.stderr)
                continue

            if args.output_dir:
                name = out_name(url, i + 1)
                (out_dir / name).write_text(build_frontmatter(url, title) + md, encoding="utf-8")
                print(f"[完成] {url} -> {out_dir / name} ({len(md)} 字)")
            else:
                print(md)
                print(f"\n<!-- 来源: {url} -->")

    return 1 if failures else 0


def _check_crawl4ai_version() -> None:
    """crawl4ai 0.x API 与本兼容层匹配；主版本不符时告警而不是静默失败。"""
    try:
        version = _imeta.version("crawl4ai")
        major = version.split(".", 1)[0]
        if major != "0":
            print(
                f"警告: crawl4ai {version} 主版本与兼容层(0.x)不符，API 可能不兼容。"
                "setup.sh 已范围锁定 crawl4ai>=0.9,<1，请重跑安装。",
                file=sys.stderr,
            )
    except Exception:  # noqa: BLE001 - 元数据缺失时静默跳过
        pass


def main() -> int:
    _check_crawl4ai_version()
    args = build_parser().parse_args()
    try:
        return asyncio.run(amain(args))
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
