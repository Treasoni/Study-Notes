import re, sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 收口：把「准入 + 很窄分级」等无「的」异体也归到 canonical
PAT = re.compile(r"准入\s*[+加]\s*很窄分级")
CANON = "准入与很窄的分级"

files = ["01_explore_result.md", "02_deep_research.md", "03_outline.md"]
files += sorted(str(p) for p in pathlib.Path("chapters").glob("0*.md"))

total = 0
for name in files:
    p = pathlib.Path(name)
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8")
    t2, n = PAT.subn(CANON, t)
    if n:
        p.write_text(t2, encoding="utf-8")
        print(f"{name}: {n} 处")
    total += n
print("合计:", total)
