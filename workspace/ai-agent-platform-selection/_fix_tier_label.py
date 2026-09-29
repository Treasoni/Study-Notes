import re, sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 冻结口径：ch.2 §2.1 锚表 + 03_outline.md:15 硬约束行均用「准入与很窄的分级」
PAT = re.compile(r"准入\s*[+加]\s*很窄的分级")
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
        print(f"{name}: {n} 处 → {CANON}")
    total += n
print("合计:", total)

# 复核
left = PAT.findall("\n".join(pathlib.Path(f).read_text(encoding="utf-8") for f in files if pathlib.Path(f).exists()))
print("残留异体:", len(left))
