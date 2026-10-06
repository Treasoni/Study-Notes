#!/usr/bin/env python3
"""抓取 P2 素材并归一为稳定来源 ID 文件名（vps-node-cdn-rescue）。

来源 ID 与 01_explore_result.md 的来源表一一对应。
每源独立临时目录 + 归一为 sources/{ID}.md；失败源逐一打印并计入汇总，不静默通过。
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.join(ROOT, "sources")
TMP = os.path.join(SOURCES, ".tmp")
CRAWL = os.path.join(
    os.path.dirname(os.path.dirname(ROOT)),
    ".claude", "skills", "research-collector", "scripts", "crawl.sh",
)

# ID -> URL（与 01_explore_result.md 一致；B-9 营销页按计划不抓）
SOURCES_MAP = {
    "A-1": "https://www.cloudflare.com/learning/cdn/what-is-a-cdn/",
    "A-2": "https://developers.cloudflare.com/reference-architecture/architectures/cdn/",
    "A-3": "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/HowCloudFrontWorks.html",
    "A-4": "https://developer.mozilla.org/en-US/docs/Glossary/CDN",
    "A-5": "https://www.usenix.org/conference/usenixsecurity21/presentation/wei",
    "A-6": "https://gfw.report/publications/usenixsecurity23/en/",
    "B-1": "https://developers.cloudflare.com/dns/proxy-status/",
    "B-2": "https://developers.cloudflare.com/dns/proxy-status/limitations/",
    "B-3": "https://developers.cloudflare.com/fundamentals/reference/network-ports/",
    "B-4": "https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/",
    "B-5": "https://developers.cloudflare.com/dns/zone-setups/",
    "B-6": "https://developers.cloudflare.com/dns/zone-setups/full-setup/",
    "B-7": "https://developers.cloudflare.com/dns/zone-setups/partial-setup/",
    "B-8": "https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/full-strict/",
    "C-1": "https://xtls.github.io/config/transports/websocket.html",
    "C-2": "https://github.com/MHSanaei/3x-ui/wiki/Configuration",
    "C-3": "https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-525/",
    "C-4": "https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-413/",
    "C-5": "https://ooni.org/support/glossary/",
    "C-6": "https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-526/",
    "C-7": "https://xtls.github.io/config/features/fallback.html",
}

# 已知会产出噪声/正文过短的源，抓到后仍保留，但需人工过一眼
SMALL_OK = {"C-4"}


def crawl_one(sid, url):
    dst = os.path.join(SOURCES, f"{sid}.md")
    if os.path.exists(dst):
        print(f"[skip] {sid} 已存在 ({os.path.getsize(dst)} B)")
        return "skip"
    tmpdir = os.path.join(TMP, sid)
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir, exist_ok=True)
    try:
        proc = subprocess.run(
            ["bash", CRAWL, "--url", url, "--output-dir", tmpdir],
            capture_output=True, timeout=420,
        )
    except subprocess.TimeoutExpired:
        print(f"[timeout] {sid} {url}")
        return "timeout"
    # 不用 text=True：本机 locale 为 GBK，会解码失败并吞掉错误信息
    err = (proc.stderr or b"").decode("utf-8", "replace")
    out = (proc.stdout or b"").decode("utf-8", "replace")
    produced = sorted(f for f in os.listdir(tmpdir) if f.endswith(".md"))
    if proc.returncode != 0 or len(produced) != 1:
        print(f"[warn] {sid} 抓取异常 rc={proc.returncode} files={produced}")
        print((err or out)[-400:])
        return "failed"
    shutil.move(os.path.join(tmpdir, produced[0]), dst)
    shutil.rmtree(tmpdir)
    size = os.path.getsize(dst)
    flag = "" if size >= 2000 or sid in SMALL_OK else "  <- 正文偏短，需人工过目"
    print(f"[ok] {sid} -> sources/{sid}.md ({size} B){flag}")
    return "ok"


def main():
    os.makedirs(SOURCES, exist_ok=True)
    only = sys.argv[1:] or None
    results = {}
    for sid, url in SOURCES_MAP.items():
        if only and sid not in only:
            continue
        results[sid] = crawl_one(sid, url)

    good = {k: v for k, v in results.items() if v in ("ok", "skip")}
    bad = {k: v for k, v in results.items() if v not in ("ok", "skip")}
    print(f"\n汇总：成功/跳过 {len(good)}/{len(results)}；异常 {len(bad)}：{bad}")

    print("\nsources/ 现状：")
    total = 0
    for f in sorted(os.listdir(SOURCES)):
        p = os.path.join(SOURCES, f)
        if os.path.isfile(p):
            total += 1
            print(f"  {f}  {os.path.getsize(p)} B")
    print(f"  合计 {total} 篇")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
