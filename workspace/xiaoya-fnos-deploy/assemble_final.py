#!/usr/bin/env python3
"""把 chapters/01..07 重新装配进 output/final_note.md（单文件合并版）。

保守做法（与 publish_copies.py 同思路）：
- 装配件自身的框架（头部说明 + 章间 `---` 分隔）**从原装配件推导**，不硬编码；
- 只把每章正文区替换为当前 chapters/0N_*.md 的内容；
- 未改动的章必须重算后逐字节一致，否则报错退出。

用法：
    python3 assemble_final.py --check      # 只报告哪些章会变
    python3 assemble_final.py --apply      # 实际写回
"""
import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
CH = ROOT / "chapters"
FINAL = ROOT / "output" / "final_note.md"


def parse(t):
    lines = t.split("\n")
    assert lines[-1] == "", "装配件不是以换行结尾"
    seps = [i for i, l in enumerate(lines) if l == "---"]
    heads = [i for i, l in enumerate(lines) if re.match(r"^# 第 \d+ 章", l)]
    if len(seps) != len(heads):
        raise SystemExit(f"装配件结构异常：--- 行 {len(seps)} 个、章标题 {len(heads)} 个")
    pre = lines[: seps[0]]
    bodies = []
    for i, h in enumerate(heads):
        end = seps[i + 1] if i + 1 < len(seps) else len(lines) - 1
        bodies.append(lines[h:end])
    return pre, heads, bodies


def build(pre, bodies):
    out = list(pre)
    for b in bodies:
        out += ["---", ""] + list(b)
    out.append("")
    return "\n".join(out)


def chapter_files():
    files = sorted(CH.glob("*.md"))
    return [f for f in files if re.match(r"^\d\d_", f.name)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    t = FINAL.read_text()
    pre, heads, bodies = parse(t)

    # 自证：用原正文重建必须与原文逐字节相同
    if build(pre, bodies) != t:
        raise SystemExit("自证失败：按推导出的框架重建原文不一致，拒绝继续")

    cfs = chapter_files()
    if len(cfs) != len(bodies):
        raise SystemExit(f"章文件 {len(cfs)} 个 vs 装配件 {len(bodies)} 章，不匹配")

    new_bodies, changed = [], []
    for cf, old in zip(cfs, bodies):
        new = cf.read_text().rstrip("\n").split("\n")
        new_bodies.append(new)
        if new != old:
            changed.append(cf.name)

    print(f"装配件：{FINAL.relative_to(ROOT)}  ｜ 章数 {len(bodies)}")
    for cf in cfs:
        mark = "DIFF" if cf.name in changed else "OK  "
        print(f"[{mark}] {cf.name}")
    print(f"\n需更新 {len(changed)} 章：{', '.join(changed) if changed else '（无）'}")

    if args.apply:
        FINAL.write_text(build(pre, new_bodies))
        print("已写回。")
    elif not args.check:
        print("（未加 --apply，未写回）")


if __name__ == "__main__":
    main()
