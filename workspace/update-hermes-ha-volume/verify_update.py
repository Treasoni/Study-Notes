#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""父流程用的确定性验收器：把 `updates/{note_id}/updated_note.md` 与发布源原文逐行比。

它不解内容对错（那是子代理与 source_bank 的事），只回答三个机械问题：
  1. 发布源自基线以来是否被动过？（应该没动，动手的是父流程自己）
  2. `updated_note.md` 与原文的差异，是否**只**落在允许的区域内？
  3. 有没有夹带行尾 / 尾随空白 / BOM 之类的隐性改动？

用法：
  python3 verify_update.py N01 --allow-hunk 34-34 --allow-hunk 64-64 ...
  python3 verify_update.py N01 --report-only       # 只打印，不判定

--allow-hunk 给的是**原文行号区间**（起止用 - 连接，单行就写两次同一个数）。
一个 hunk 的旧侧行区间与任一允许区间有交集即算命中；未命中即失败。
"""

import argparse
import difflib
import hashlib
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("D:/Study-Notes")
PROJ = ROOT / "workspace/hermes-home-assistant"
RUN = ROOT / "workspace/update-hermes-ha-volume"
UPDATES = RUN / "updates"

# note_id -> (相对 workspace/hermes-home-assistant 的路径, 基线分组)
NOTE_SPEC = {
    "N01": ("chapters/03-路线选型.md", "chapters"),
    "N02": ("chapters/01-结论先行与能力地图.md", "chapters"),
    "N05": ("chapters/04-落地-社区ha-mcp.md", "chapters"),
    "N12": ("chapters/10-附录.md", "chapters"),
    "N03": ("02_deep_research.md", "research"),
    "N04": ("01_explore_result.md", "research"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_lines(p):
    """按 LF 语义取行，同时回报原始字节。

    行尾按语义归一：CRLF 文件在逐行比对时不当成「整篇都改了」。
    若不做这一步，一个 CRLF 源文件配上 LF 的 updated_note.md 会产出
    与行数等量的假 hunk，把真正的改动淹掉。
    """
    b = p.read_bytes()
    lines = [x[:-1] if x.endswith("\r") else x for x in b.decode("utf-8").split("\n")]
    return b, lines


def parse_allow(items):
    out = []
    for it in items:
        m = re.fullmatch(r"(\d+)(?:-(\d+))?", it)
        if not m:
            raise SystemExit("--allow-hunk 格式错误：{}".format(it))
        a = int(m.group(1))
        b = int(m.group(2) or a)
        out.append((min(a, b), max(a, b)))
    return out


def overlaps(a1, a2, b1, b2):
    return not (a2 < b1 or b2 < a1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("note_id")
    ap.add_argument("--allow-hunk", action="append", default=[])
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    note = args.note_id
    if note not in NOTE_SPEC:
        raise SystemExit("未知 note_id：{}（可选 {}）".format(note, "/".join(NOTE_SPEC)))
    name = pathlib.Path(NOTE_SPEC[note][0]).name

    rel, group = NOTE_SPEC[note]
    src = PROJ / rel
    upd = UPDATES / note / "updated_note.md"
    base_json = RUN / "_hash_baseline.json"
    report = UPDATES / note / "diff_check.txt"

    problems = []
    notes = []

    if not upd.exists():
        raise SystemExit("缺少 {}".format(upd))
    if not base_json.exists():
        raise SystemExit("缺少基线 {}".format(base_json))

    base = json.loads(base_json.read_text(encoding="utf-8"))
    want = base.get(group, {}).get(name, {}).get("sha256")
    cur_b, cur_l = read_lines(src)
    if want and sha(cur_b) != want:
        problems.append("发布源已被改动，与预检基线不符：{}".format(rel))
    src_crlf = cur_b.count(b"\r\n")
    if src_crlf:
        notes.append("原文件行尾为 CRLF（{} 行）；apply_update.py 会按原行尾写回，"
                     "不产生无关的行尾改动".format(src_crlf))

    up_b, up_l = read_lines(upd)
    if b"\r" in up_b:
        problems.append("updated_note.md 含 CR（本流程的交付物一律要求 LF）")
    if up_b.startswith(b"\xef\xbb\xbf"):
        problems.append("updated_note.md 含 BOM")
    if not up_b.endswith(b"\n"):
        problems.append("updated_note.md 末尾缺少换行")

    sm = difflib.SequenceMatcher(a=cur_l, b=up_l, autojunk=False)
    allow = parse_allow(args.allow_hunk)
    hunks = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old_lo, old_hi = i1 + 1, max(i2, i1 + 1)
        new_lo, new_hi = j1 + 1, max(j2, j1 + 1)

        def label(lo, hi, empty):
            if empty:
                return "L{}（插入点）".format(lo)
            if lo == hi:
                return "L{}".format(lo)
            return "L{}-{}".format(lo, hi)

        old_nos = label(old_lo, old_hi, i2 == i1)
        new_nos = label(new_lo, new_hi, j2 == j1)
        # 纯空白/行尾差异（去掉所有空白后完全相同的等长块）
        old_txt = [x.strip() for x in cur_l[i1:i2]]
        new_txt = [x.strip() for x in up_l[j1:j2]]
        whitespace_only = (tag == "replace" and old_txt == new_txt)
        hit = any(overlaps(old_lo, old_hi, a, b) for a, b in allow) if allow else None
        hunks.append({
            "tag": tag, "old": old_nos, "new": new_nos,
            "old_range": (old_lo, old_hi),
            "del": i2 - i1, "add": j2 - j1,
            "old_lines": cur_l[i1:i2], "new_lines": up_l[j1:j2],
            "whitespace_only": whitespace_only, "allowed": hit,
        })

    lines = []
    lines.append("== diff check：{} <- {} ==".format(name, upd.name))
    lines.append("原文行数 {} -> 新文行数 {}；差异块 {} 个".format(len(cur_l), len(up_l), len(hunks)))
    total_del = sum(h["del"] for h in hunks)
    total_add = sum(h["add"] for h in hunks)
    lines.append("合计 删除 {} 行 / 新增 {} 行".format(total_del, total_add))
    lines.append("")

    for k, h in enumerate(hunks, 1):
        flag = ""
        if h["whitespace_only"]:
            flag = "  ⚠ 纯空白差异"
        elif allow:
            flag = "  ✅ 在允许区内" if h["allowed"] else "  ❌ 不在允许区内"
        lines.append("--- hunk {} [{}] 原 {} -> 新 {}{}".format(k, h["tag"], h["old"], h["new"], flag))
        for x in h["old_lines"]:
            lines.append("  - {}".format(x))
        for x in h["new_lines"]:
            lines.append("  + {}".format(x))
        if h["whitespace_only"]:
            problems.append("hunk {} 是纯空白差异（{}）".format(k, h["old"]))
        elif allow and not h["allowed"]:
            problems.append("hunk {} 越出允许区（原行 {}）".format(k, h["old"]))
        if h["tag"] != "replace":
            notes.append("hunk {} 是 {}（不是纯替换）".format(k, h["tag"]))

    lines.append("")
    if allow:
        touched = [h["old_range"] for h in hunks]
        covered = [a for a in allow
                   if not any(overlaps(t[0], t[1], a[0], a[1]) for t in touched)]
        if covered:
            notes.append("以下允许区没有任何改动：{}".format(
                ", ".join("{}-{}".format(a, b) for a, b in covered)))

    if notes:
        lines.append("## 提示（非失败）")
        lines += ["- " + n for n in notes]
        lines.append("")
    if problems:
        lines.append("## 问题")
        lines += ["- " + p for p in problems]
    else:
        lines.append("## 问题\n- 无")

    text = "\n".join(lines) + "\n"
    report.write_bytes(text.encode("utf-8"))
    print(text)

    if args.report_only:
        return 0
    if problems:
        print("验收未通过：{} 个问题".format(len(problems)), file=sys.stderr)
        return 1
    print("验收通过：{}".format(note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
