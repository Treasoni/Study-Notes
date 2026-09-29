import sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 有序替换：长模式在前，避免留下别扭措辞
REPL = [
    ("17 轴 source-verified 对照", "source-verified 对照（15 行属性）"),
    ("17 轴对照表", "15 行属性对照表"),
    ("17 轴对照专页", "15 行属性对照专页"),
    ("17 轴对照页", "15 行属性对照专页"),
    ("官方 17 轴对照", "官方对照（15 行属性）"),
    ("迁移命令、17 轴对照、", "迁移命令、对照专页、"),
    ("17 轴", "15 行属性"),
]

total = 0
for name in ["01_explore_result.md", "02_deep_research.md", "03_outline.md"]:
    p = pathlib.Path(name)
    t = p.read_text(encoding="utf-8")
    n = 0
    for old, new in REPL:
        c = t.count(old)
        if c:
            t = t.replace(old, new)
            n += c
    if n:
        p.write_text(t, encoding="utf-8")
    print(f"{name}: 替换 {n} 处")
    total += n
print("合计:", total)
