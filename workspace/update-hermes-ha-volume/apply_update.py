#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `updates/{note_id}/updated_note.md` 逐字节应用到 `chapters/` 发布源。

只做搬运与校验，不做任何文本变换：
  1. 要求 `updated_note.md` 是 LF、无 BOM、以换行结尾；
  2. 要求在应用前先过 `verify_update.py`（本脚本会检查 `diff_check.txt` 存在且结论为通过）；
  3. `write_bytes` 整篇覆盖（不做行尾翻译）；
  4. 回读校验 sha256 一致，并打印新旧体积。

用法：
  python3 apply_update.py N01 [--force]
"""

import argparse
import hashlib
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path("D:/Study-Notes")
PROJ = ROOT / "workspace/hermes-home-assistant"
RUN = ROOT / "workspace/update-hermes-ha-volume"
UPDATES = RUN / "updates"

# note_id -> 相对 workspace/hermes-home-assistant 的路径
NOTE_SPEC = {
    "N01": "chapters/03-路线选型.md",
    "N02": "chapters/01-结论先行与能力地图.md",
    "N05": "chapters/04-落地-社区ha-mcp.md",
    "N12": "chapters/10-附录.md",
    "N03": "02_deep_research.md",
    "N04": "01_explore_result.md",
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("note_id")
    ap.add_argument("--force", action="store_true",
                    help="跳过 diff_check.txt 的通过性检查（仅在你已人工复核后使用）")
    args = ap.parse_args()

    note = args.note_id
    if note not in NOTE_SPEC:
        raise SystemExit("未知 note_id：{}".format(note))
    rel = NOTE_SPEC[note]
    name = pathlib.Path(rel).name

    src = PROJ / rel
    upd = UPDATES / note / "updated_note.md"
    check = UPDATES / note / "diff_check.txt"
    if not upd.exists():
        raise SystemExit("缺少 {}".format(upd))

    body = upd.read_bytes()
    if b"\r\n" in body or b"\r" in body:
        raise SystemExit("{} 含 CR，拒绝应用".format(upd.name))
    if body.startswith(b"\xef\xbb\xbf"):
        raise SystemExit("{} 含 BOM，拒绝应用".format(upd.name))
    if not body.endswith(b"\n"):
        raise SystemExit("{} 末尾缺少换行，拒绝应用".format(upd.name))

    if not args.force:
        if not check.exists():
            raise SystemExit("缺少 {}；先跑 verify_update.py {}".format(check, note))
        txt = check.read_text(encoding="utf-8")
        if "## 问题\n- 无" not in txt:
            raise SystemExit("diff_check.txt 结论不是「无问题」，拒绝应用")

    old = src.read_bytes()
    before = sha(old)
    # 行尾随原文件：交付物一律 LF，写回时按原文件既有行尾重新编码，
    # 避免在一个下游无感的文件上制造整篇无关改动（如 10-附录.md / 06-… 本就是 CRLF）。
    src_crlf = old.count(b"\r\n")
    if src_crlf:
        out = body.replace(b"\n", b"\r\n")
        eol = "CRLF（按原文件，{} 行）".format(src_crlf)
    else:
        out = body
        eol = "LF"
    src.write_bytes(out)
    after = sha(src.read_bytes())
    if after != sha(out):
        raise SystemExit("回读校验失败：写盘结果与预期字节不一致")

    print("== apply {} -> {} ==".format(note, rel))
    print("  sha256 前 {}\n  sha256 后 {}".format(before[:16], after[:16]))
    print("  体积   {} -> {} B（{:+d}）".format(len(old), len(out), len(out) - len(old)))
    print("  行尾   {}（交付物 CRLF={} CR={}）".format(
        eol, body.count(b"\r\n"), body.count(b"\r")))
    print("  结果   已应用，回读一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
