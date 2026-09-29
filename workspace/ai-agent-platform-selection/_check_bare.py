import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

bad = 0
for p in sorted(pathlib.Path("chapters").glob("0*.md")):
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        for m in re.finditer("多用户", line):
            s, e = m.start(), m.end()
            if line[max(0, s - 1):s] in "「“":
                continue
            if line[e:e + 1] in "」”":
                continue
            if line[e:e + 2] == "平台":          # 层名，ch.1 已就地定义
                continue
            if "不作改动" in line:               # 引号内为官方原句，已在引号外加限定语
                continue
            bad += 1
            print(f"  x {p.name}:{i}  ...{line[max(0, s - 16):e + 16]}...")
print("剩余裸用:", bad)
