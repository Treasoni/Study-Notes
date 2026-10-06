"""把正文（代码块外）里成对的 ASCII 直引号 "..." 归一为 「...」，无语义变化。
用法: python3 normalize_quotes.py <file...>
"""
import sys, pathlib

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

for arg in sys.argv[1:]:
    p = pathlib.Path(arg)
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    in_code = False
    changed_lines = 0
    changed_marks = 0
    out = []
    for ln in lines:
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            out.append(ln)
            continue
        if in_code or '"' not in ln:
            out.append(ln)
            continue
        buf = []
        n = 0
        for ch in ln:
            if ch == '"':
                buf.append("「" if n % 2 == 0 else "」")
                n += 1
            else:
                buf.append(ch)
        if n % 2:
            print("  !! %s 第 %d 行引号数为奇数(%d)，未处理" % (p.name, len(out) + 1, n))
            out.append(ln)
            continue
        if n:
            changed_lines += 1
            changed_marks += n
        out.append("".join(buf))
    p.write_text("".join(out), encoding="utf-8")
    print("%-34s 改动 %d 行 / %d 个引号" % (p.name, changed_lines, changed_marks))
