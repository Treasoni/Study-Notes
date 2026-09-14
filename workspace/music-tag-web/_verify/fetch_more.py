import sys, pathlib, subprocess

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = pathlib.Path("workspace/music-tag-web/_verify/src")
OUT.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

TARGETS = [
    ("README_dev_1.0.md",
     "https://raw.githubusercontent.com/xhongc/music-tag-web/dev_1.0/README.md"),
    ("fnos_thread_4152.html",
     "https://club.fnnas.com/forum.php?mod=viewthread&tid=4152"),
    ("cnblogs_22696323.html",
     "https://www.cnblogs.com/ivoink/articles/22696323"),
]

for name, url in TARGETS:
    r = subprocess.run(["curl", "-sL", "--retry", "3", "-A", UA, url], capture_output=True)
    data = r.stdout
    (OUT / name).write_bytes(data)
    print("%-28s %8d bytes" % (name, len(data)))
