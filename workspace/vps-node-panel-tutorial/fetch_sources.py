#!/usr/bin/env python3
"""抓取 P2 素材并归一为稳定来源 ID 文件名。

背景：crawl.sh 的 out_name() 按域名命名（{idx:02d}_{host}.md），多个同域来源
无法区分，且重跑时 index 从 01 重新开始会静默覆盖别的来源正文。本脚本改为
每源独立临时目录 + 归一为 sources/{ID}.md，任何异常一律非零退出。
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

# 已抓取的核心 5 篇：旧名 -> 稳定 ID
RENAME = {
    "01_arxiv_org.md": "A-2.md",
    "02_xtls_github_io.md": "A-1.md",
    "03_github_com.md": "B-1.md",
    "04_developers_cloudflare_com.md": "C-2.md",
    "05_shadowsocks_org.md": "A-4.md",
}

# 待抓取来源：ID -> URL
PENDING = {
    "A-3": "https://github.com/MHSanaei/3x-ui",
    "B-2": "https://racknerd.com/kvm-vps",
    "B-3": "https://bandwagonhost.com/vps-hosting.php",
    "B-4": "https://www.hostbuf.com/t/988.html",
    "B-5": "https://wise-vegetarian-da6.notion.site/VPS-2daacc0097d38077a769e8a98051fec1",
    "B-6": "https://cloudcone.com/vps/",
    "C-1": "https://developers.cloudflare.com/dns/proxy-status/",
    "C-3": "https://fail2ban.readthedocs.io/en/latest/",
    "C-4": "https://man.openbsd.org/sshd_config",
    "C-5": "https://docs.digitalocean.com/products/droplets/how-to/rebuild/",
    "C-6": "https://help.aliyun.com/zh/ecs/product-overview/what-is-ecs",
    "C-7": "https://docs.vultr.com/how-to-configure-networking-on-vultr-cloud-servers",
}


def fail(msg):
    print(f"FETCH-FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def normalize_existing():
    """幂等：已完成的重命名跳过；状态矛盾（两边都在/都在缺）则失败退出。"""
    changed = 0
    for old, new in RENAME.items():
        src = os.path.join(SOURCES, old)
        dst = os.path.join(SOURCES, new)
        if os.path.exists(dst) and not os.path.exists(src):
            continue  # 已归一
        if not os.path.exists(src):
            fail(f"expected crawled file missing: {src}")
        if os.path.exists(dst):
            fail(f"both old and new exist, refusing to overwrite: {src} / {dst}")
        os.rename(src, dst)
        changed += 1
    print(f"本次重命名 {changed} 处")


def crawl_one(sid, url):
    dst = os.path.join(SOURCES, f"{sid}.md")
    if os.path.exists(dst):
        print(f"[skip] {sid} 已存在")
        return "skip"
    tmpdir = os.path.join(TMP, sid)
    if os.path.isdir(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir, exist_ok=True)
    proc = subprocess.run(
        ["bash", CRAWL, "--url", url, "--output-dir", tmpdir],
        capture_output=True, timeout=420,
    )
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
    print(f"[ok] {sid} -> {os.path.relpath(dst, ROOT)} ({os.path.getsize(dst)} B)")
    return "ok"


def main():
    os.makedirs(SOURCES, exist_ok=True)
    normalize_existing()
    only = sys.argv[1:] or None
    results = {}
    for sid, url in PENDING.items():
        if only and sid not in only:
            continue
        try:
            results[sid] = crawl_one(sid, url)
        except subprocess.TimeoutExpired:
            print(f"[warn] {sid} 超时")
            results[sid] = "timeout"
    ok = sum(1 for v in results.values() if v in ("ok", "skip"))
    print(f"\n汇总：成功/跳过 {ok}，其余 {len(results) - ok}："
          f"{ {k: v for k, v in results.items() if v not in ('ok', 'skip')} }")
    print("\nsources/ 现状：")
    for f in sorted(os.listdir(SOURCES)):
        p = os.path.join(SOURCES, f)
        if os.path.isfile(p):
            print(f"  {f}  {os.path.getsize(p)} B")


if __name__ == "__main__":
    main()
