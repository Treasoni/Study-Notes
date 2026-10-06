import sys, pathlib, subprocess, re, hashlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = pathlib.Path("workspace/music-tag-web/_verify/src")
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = [
    "https://xiers-organization.gitbook.io/music-tag-web-v2/llms.txt",
    "https://xiers-organization.gitbook.io/music-tag-web/llms.txt",
]

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def fetch(url):
    r = subprocess.run(
        ["curl", "-sL", "--retry", "3", "-A", UA, url],
        capture_output=True,
    )
    return r.stdout.decode("utf-8", "replace")


urls = set(SEEDS)
for s in SEEDS:
    body = fetch(s)
    for m in re.finditer(r"https://xiers-organization\.gitbook\.io/[^\s\)\]\"<>]+?\.md", body):
        urls.add(m.group(0))

urls = sorted(urls)
print("待抓取页面数:", len(urls))

manifest = []
for u in urls:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", u.split("gitbook.io/")[-1]).strip("-")[:90]
    p = OUT / (slug + ".md")
    if not p.exists() or p.stat().st_size < 200:
        p.write_bytes(fetch(u).encode("utf-8"))
    data = p.read_bytes().decode("utf-8", "replace")
    manifest.append((u, p.name, len(data)))
    print("  %6d  %s" % (len(data), p.name))

pathlib.Path("workspace/music-tag-web/_verify/src/_manifest.tsv").write_text(
    "\n".join("%s\t%s\t%d" % t for t in manifest), encoding="utf-8"
)
print("完成，共", len(manifest), "个来源文件")
